from setuptools import setup
from torch.utils.cpp_extension import BuildExtension, CUDAExtension
import torch


ExtensionModels = []
if torch.version.cuda is not None:
    ExtensionModels.append(CUDAExtension('ts_cpp', sources=[
            'cpp/ts/pybind.cpp',
            'cpp/ts/tensor_list.cpp',
            'cpp/ts/blocking_queue.cpp',
            'cpp/ts/cuda_stage.cpp',
            'cpp/ts/cuda_event_pool.cpp',
            'cpp/ts/thread_pool.cpp',
        ]))

setup(
    name='torch_stage',
    version='0.1.2',
    cmdclass={'build_ext': BuildExtension},
    ext_modules=ExtensionModels,
    packages=['ts'],
    requires=['torch'],
    tests_require=[
        'transformers',
        'aiounittest'
    ]
)