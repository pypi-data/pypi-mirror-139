import torch
import ts_cpp
import asyncio
from dataclasses import dataclass
from typing import Any, Callable, List, Optional, Union
from concurrent.futures import ProcessPoolExecutor
import gc

__all__ = ['create_preprocessor', 'create_cuda_compute_stage', 'create_cpu_compute_stage', 'Stage']

@dataclass()
class StageData:
    """
    Data class between preprocess stage and compute stage. This class is used internally, and should not be used by users.
    """
    tensors: List[torch.Tensor]
    extra_args: Optional[Any]
    to_result: Optional[Callable[[List[torch.Tensor], Any], Any]]


def _preprocess_real_call(req: Any) -> StageData:
    result = MultiProcessesPreprecessor.instance(req)
    return MultiProcessesPreprecessor.result_to_stage_data(result)


class MultiProcessesPreprecessor:
    """
    Multiple processes preprocessor.

    Args:
        instance_creator: A function that creates an instance of the preprocessor function.
        concurrency: The maximum number of concurrent processes.

    Note:
        Preprocessor function should returns:
        * A PyTorch tensor.
        * Sequance[Unoin[Tensor, Any]]
        * Dict[Any, Unoin[Tensor, Any]]
    """
    def __init__(self, instance_creator, concurrency: int) -> None:
        torch.multiprocessing.set_sharing_strategy('file_system')
        self.pool = ProcessPoolExecutor(max_workers=concurrency, mp_context=torch.multiprocessing.get_context("forkserver"), 
            initializer=MultiProcessesPreprecessor.process_init, initargs=(instance_creator,))


    async def __call__(self, req: Any) -> StageData:
        loop = asyncio.get_running_loop()
        try:
            return await loop.run_in_executor(self.pool, _preprocess_real_call, req)
        except Exception as e:
            print(e)
            raise

    def shutdown(self):
        self.pool.shutdown()


    @staticmethod
    def real_call(req: Any) -> StageData:
        result = MultiProcessesPreprecessor.instance(req)
        return MultiProcessesPreprecessor.result_to_stage_data(result)


    @staticmethod
    def result_to_stage_data(result)->StageData:
        if isinstance(result, StageData):
            return result
        elif isinstance(result, torch.Tensor):
            return StageData([result], None, MultiProcessesPreprecessor._to_result_from_torch_tensor)

        elif isinstance(result, list) or isinstance(result, tuple):
            tensors = []
            tensors_pos = []
            extra_args = []
            for i, item in enumerate(result):
                if isinstance(item, torch.Tensor):
                    tensors.append(item)
                    tensors_pos.append(i)
                else:
                    extra_args.append((i,item))
            

            return StageData(tensors, (tensors_pos, extra_args), MultiProcessesPreprecessor._to_result_from_list)
        elif isinstance(result, dict):
            tensors = []
            tensors_key = []
            extra_dict = dict()
            for key, item in result.items():
                if isinstance(item, torch.Tensor):
                    tensors.append(item)
                    tensors_key.append(key)
                else:
                    extra_dict[key] = item
            return StageData(tensors, (tensors_key, extra_dict), MultiProcessesPreprecessor._to_result_from_dict)

        else:
            raise ValueError("not support")

    @staticmethod
    def _to_result_from_dict(tensors:List[torch.Tensor], args):
        keys, result_dict = args
        d = {k: t for k, t in zip(keys, tensors)}
        d.update(result_dict)
        return d


    @staticmethod
    def _to_result_from_list(tensors:List[torch.Tensor], args):
        tensors_pos, extra_args = args
        for i, tensor in zip(tensors_pos, tensors):
            extra_args.append((i, tensor))
        
        return [item[1] for item in  extra_args.sort(key=lambda x: x[0])]

    @staticmethod
    def _to_result_from_torch_tensor(tensors: List[torch.Tensor], _: Any) -> Any:
        return tensors[0]

    @staticmethod
    def process_init(creator):
        torch.multiprocessing.set_sharing_strategy('file_system')
        torch.set_grad_enabled(False)
        MultiProcessesPreprecessor.instance = creator()
        gc.freeze()

class InstanceCreator:
    """
    Just call the class constructor. It is used internally, and only used to make lambda: cls(*args, **kwargs) pickleable.
    """
    def __init__(self, cls, args, kwargs) -> None:
        self._cls = cls
        self._args = args
        self._kwargs = kwargs
    
    def __call__(self) -> Any:
        return self._cls(*self._args, **self._kwargs)


def _parse_args(cls, kwargs: dict, cls_field_name: str, default_value:Any,  kwarg_field_name: Optional[str] = None):
    """
    Parse the arguments from create_xxx method. It will first try to parse the argument from class attributes. 
    If not found, it will try to parse the argument from kwargs. If not found, it will use the default value.

    It is used internally, and should not be used by users.
    """
    tdefault = type(default_value)
    if hasattr(cls, cls_field_name) and isinstance(getattr(cls, cls_field_name), tdefault):
        return getattr(cls, cls_field_name)
    
    if kwarg_field_name is None:
        kwarg_field_name = cls_field_name.lower()
    
    if kwarg_field_name in kwargs and isinstance(kwargs[kwarg_field_name], tdefault):
        return kwargs[kwarg_field_name]
    
    return default_value

def create_preprocessor(cls, *args, **kwargs):
    """
    Create a async/multiple process preprocessor from a processor class.

    The created preprocessor will contains an async '__call__', and will return StageData. The StageData is an internal data structure.
    You can use the return value, and result.to_result(result.tensors, result.extra_args) to get the original data.

    The `*args` and `**kwargs` will be passed to the processor class constructor.

    The preprocessor class can has attributes:
        * CONCURRENCY: the number of concurrent processes. Default is 1. It can be also set by `kwargs`.
    """
    concurrency = _parse_args(cls, kwargs, 'CONCURRENCY', 1)
    return MultiProcessesPreprecessor(InstanceCreator(cls, args, kwargs), concurrency)


class CUDAComputeStage:
    """
    CUDAComputeStage will take a call_method with type (StageData) -> Any, and make it pipeline parallelized.

    There are three stages in the pipeline:
    
        +----------------+                             +----------------+
        |  Copy Tensors  |       +---------------+     |  Copy Tensors  |
        | Host To Device |  -->  | Compute Stage | --> | Device To Host |
        |   (h2d stage)  |       |   (c stage)   |     |   (d2h stage)  |
        +----------------+       +---------------+     +----------------+

    Each stage's parallel can be configurated. All pipeline is run in a different thread from the main thread. 
    So the `call_method` should be thread safe and release `GIL` as much as possible.
    Also the `call_method` should use the global PyTorch CUDA stream to compute.

    The pipeline concurrency is demonstrated as follows:

        | h2d | job1 | job2 | job3 | ...  | ...  |
        | c   | wait | job1 | job2 | job3 | ...  |
        | d2h | wait | wait | job1 | job2 | job3 |

    Since CUDA device is an async device, so the jobs from each stage will be pushed into devices and run in parallel.

    Args:
        device_id: The cuda device id to run compute.
        max_h2d_concurrency: The maximum number of concurrency h2d stage. i.e., the maximum number of HostToDevice copy jobs that is pushed to device and not finished.
        max_c_concurrency: The maximum number of concurrency c stage. i.e., the maximum number of Compute jobs that is pushed to device and not finished.
        max_d2h_concurrency: The maximum number of concurrency d2h stage. i.e., the maximum number of DeviceToHost copy jobs that is pushed to device and not finished.
        num_compute_threads: The maxnumber of compute threads to push compute job to device. Since CUDA devices are extremely fast, so it may be better to use more threads to push compute 
            job to device. However, the `call_method` is actually a Python code, and it suffers from GIL. So it is better to release GIL in `call_method`. (for example, use Cython or uses 
            TorchScript).
        call_method: A thread-safe method to compute. It takes a StageData as input, and return a result.
    """

    def __init__(self, device_id: int, max_h2d_concurrency: int, max_compute_concurrency: int, max_d2h_concurrency: int, num_compute_threads: int, call_method: Callable[[StageData], Any]) -> None:
        self._stage = ts_cpp.CUDAStage(device_id, max_h2d_concurrency, max_compute_concurrency, max_d2h_concurrency, num_compute_threads)
        self._call_method = call_method

    async def __call__(self, stage_data: StageData) -> Any:
        loop = asyncio.get_running_loop()
        future = loop.create_future()
        input_tensors = ts_cpp.TensorList()
        for tensor in stage_data.tensors:
            tensor.detach_()
            input_tensors.append(tensor.pin_memory())

        output_stage_data = [None]
        def actual_compute(input_tensors, outputs):
            stage_data.tensors = []
            for i in range(len(input_tensors)):
                stage_data.tensors.append(input_tensors[i])

            method_input = stage_data.to_result(stage_data.tensors, stage_data.extra_args)
            method_output = self._call_method(method_input)
            method_output = MultiProcessesPreprecessor.result_to_stage_data(method_output)
            output_stage_data[0] = method_output
            for tensor in method_output.tensors:
                outputs.append(tensor)


        def on_complete(output_tensors):
            method_output = output_stage_data[0]
            method_output.tensors = []
            for i in range(len(output_tensors)):
                method_output.tensors.append(output_tensors[i])
            result = method_output.to_result(method_output.tensors, method_output.extra_args)
            loop.call_soon_threadsafe(future.set_result, result)

        self._stage.call(input_tensors, actual_compute, on_complete)
        return await future
    
def create_cuda_compute_stage(cls, *args, **kwargs) -> CUDAComputeStage:
    """
    Creates a CUDAComputeStage from a compute class.

    NOTE: The compute class must be thread safe.
    NOTE: It is better to release GIL as much as possible in the `call_method`. (for example, use Cython or uses TorchScript). It is crucial for performance.

    The compute class can has attributes:
        * MAX_HOST_TO_DEVICE_CONCURRENCY: the maximum number of concurrency h2d stage. Default is 1. It can be also set by `kwargs`.
        * MAX_COMPUTE_CONCURRENCY: the maximum number of concurrency c stage. Default is 1. It can be also set by `kwargs`.
        * MAX_DEVICE_TO_HOST_CONCURRENCY: the maximum number of concurrency d2h stage. Default is 1. It can be also set by `kwargs`.
        * NUM_COMPUTE_THREADS: the maxnumber of compute threads to push compute job to device. Since CUDA devices are extremely fast, so it may be better 
                to use more threads to push compute jobs to device. It can be also set by `kwargs`.
    """
    max_host_to_device_concurrency = _parse_args(cls, kwargs, 'MAX_HOST_TO_DEVICE_CONCURRENCY', 1)
    max_compute_concurrency = _parse_args(cls, kwargs, 'MAX_COMPUTE_CONCURRENCY', 1)
    max_device_to_host_concurrency = _parse_args(cls, kwargs, 'MAX_DEVICE_TO_HOST_CONCURRENCY', 1)
    num_compute_threads = _parse_args(cls, kwargs, 'NUM_COMPUTE_THREADS', 1)
    if num_compute_threads <= 0:
        raise ValueError("NUM_COMPUTE_THREADS must be greater than 0")
    if 'device' not in kwargs:
        device_id = torch.cuda.current_device()
        kwargs['device'] = torch.device('cuda', device_id)
    else:
        device = kwargs['device']
        device_id = device.index
    model = cls(*args, **kwargs)
    return CUDAComputeStage(device_id = device_id, max_h2d_concurrency = max_host_to_device_concurrency, max_compute_concurrency = max_compute_concurrency,
        max_d2h_concurrency = max_device_to_host_concurrency, num_compute_threads = num_compute_threads, call_method = model)
    

class CPUComputeStage:
    """
    Create a CPUComputeStage from a compute class.
    It uses multiple processes to compute.

    Args:
        concurrency: The maximum number of processes to compute.
        num_threads: The number of threads to use in each process. If it is less then or equal to 0, it will use all the available threads.
        compute_creator: A function that creates a compute class.
    """
    def __init__(self, concurrency: int, num_threads: int, compute_creator: Callable[[], Callable]) -> None:
        if concurrency <= 0:
            raise ValueError("CONCURRENCY must be greater than 0")
        if num_threads <= 0:
            num_threads = 0
        torch.multiprocessing.set_sharing_strategy('file_system')
        self._process_pool = ProcessPoolExecutor(max_workers = concurrency,  mp_context=torch.multiprocessing.get_context("forkserver"), 
            initializer=CPUComputeStage.process_init, initargs=(num_threads, compute_creator))
    
    async def __call__(self, stage_data: StageData) -> Any:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self._process_pool, CPUComputeStage._real_call, stage_data)
    
    def _real_call(stage_data:StageData) -> Any:
        method_input = stage_data.to_result(stage_data.tensors, stage_data.extra_args)
        return CPUComputeStage.instance(method_input)

    def shutdown(self):
        self._process_pool.shutdown()

    @staticmethod
    def process_init(num_threads: int, compute_creator):
        if num_threads > 0:
            torch.set_num_threads(num_threads)
        torch.set_grad_enabled(False)
        CPUComputeStage.instance = compute_creator()
        gc.freeze()

def create_cpu_compute_stage(cls, *args, **kwargs) -> CPUComputeStage:
    """
    Creates a CPUComputeStage from a compute class.

    The class can has attributes:
        * CONCURRENCY: the maximum number of processes to compute. Default is 1. It can be also set by `kwargs`.
        * NUM_THREADS: the number of threads to use in each process. If it is less then or equal to 0, it will use all the available threads.
    """
    concurrency = _parse_args(cls, kwargs, 'CONCURRENCY', 1)
    num_threads = _parse_args(cls, kwargs, 'NUM_THREADS', 0)
    if 'device' in kwargs and kwargs['device'].type != 'cpu':
        raise ValueError("CPUComputeStage can only be used with CPU devices")
    kwargs['device'] = torch.device('cpu')
    return CPUComputeStage(concurrency, num_threads, InstanceCreator(cls, args, kwargs))



class Stage:
    """
    Stage just combine preprocess and compute stage together.

    The stages are described as follows:


                    ┌─────────────────────┐
                    │      Preprocess     │
                    │                     │
                    │  ┌───────────────┐  │
                    │  │               │  │
                    │  │ Process Pool  │  │
                    │  │  ┌────────┐   │  │
                    │  │  └────────┘   │  │        ┌────────────────────┐
                    │  │               │  │        │      Compute       │
       Request ───► │  │  ┌────────┐   │  │  ───►  │                    │ ───► Response
                    │  │  └────────┘   │  │        └───┬──────────────┬─┘
                    │  │               │  │            │              │
                    │  │  ┌────────┐   │  │            │              │
                    │  │  └────────┘   │  │            │              │
                    │  │               │  │            │ When         │                When
                    │  └───────────────┘  │            │ use          │                use
                    │                     │            │ CUDA         └─────────────┐  CPU
                    └─────────────────────┘            │                            │
                                                       ▼                            ▼
                                    ┌─────────────────────────────────────────┐   ┌─────────────────────────────────────┐
                                    │               CUDA Compute              │   │           CPU Compute               │
                                    │ ┌──────┐   ┌───────────────┐   ┌──────┐ │   │ ┌─────────────────────────────────┐ │
                                    │ │      │   │  Thread Pool  │   │      │ │   │ │            Process Pool         │ │
                                    │ │      │   │  ┌─────────┐  │   │      │ │   │ │                                 │ │
                                    │ │ H2D  │   │  │ Compute │  │   │ D2H  │ │   │ │  ┌──────────┐      ┌──────────┐ │ │
                                    │ │      ├──►│  ├─────────┤  ├──►│      │ │   │ │  │ P1       │      │ P2       │ │ │
                                    │ │ Copy │   │  │ Compute │  │   │ Copy │ │   │ │  │ Multi    │      │ Multi    │ │ │
                                    │ │      │   │  └─────────┘  │   │      │ │   │ │  │ Threads  │      │ Threads  │ │ │
                                    │ │      │   │               │   │      │ │   │ │  └──────────┘      └──────────┘ │ │
                                    │ └──────┘   └───────────────┘   └──────┘ │   │ │                                 │ │
                                    │                                         │   │ └─────────────────────────────────┘ │
                                    └──────────┬──────────────────────────────┘   │                                     │
                                               │                                  └─────────────────────────────────────┘
                                               │   Commit CUDA Kernel to Devices
                                               ▼
                                    ┌──────────────────────────────────────────┐
                                    │              CUDA Device                 │
                                    │     ┌─────────────────────────────────┐  │
                                    │  H2D│J1S1 | J2S2 | J3S1 | J4S2        │  │
                                    │     └─────────────────────────────────┘  │
                                    │                                          │
                                    │     ┌─────────────────────────────────┐  │
                                    │  C  │     | J1S1 | J2S2 | J3S1 | J4S2 │  │
                                    │     └─────────────────────────────────┘  │
                                    │                                          │
                                    │     ┌─────────────────────────────────┐  │
                                    │  D2H│     |      | J1S1 | J2S2 | J3S1 │  │
                                    │     └─────────────────────────────────┘  │
                                    │                                          │
                                    └──────────────────────────────────────────┘    

    """
    def __init__(self, preprocessor: MultiProcessesPreprecessor, compute: Union[CUDAComputeStage, CPUComputeStage]) -> None:
        self._preprocessor = preprocessor
        self._compute = compute
    
    async def __call__(self, req):
        input = await self._preprocessor(req)
        # TODO: Maybe add auto-batch here?
        return await self._compute(input)
        

    def shutdown(self):
        self._preprocessor.shutdown()
        if hasattr(self._compute, 'shutdown'):
            self._compute.shutdown()