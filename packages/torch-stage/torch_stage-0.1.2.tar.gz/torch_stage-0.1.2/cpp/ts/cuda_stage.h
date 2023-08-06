#pragma once
#include <deque>
#include <memory>
#include <queue>

#include "blocking_queue.h"
#include "c10/cuda/CUDAStream.h"
#include "c10/util/variant.h"
#include "cuda_event_pool.h"
#include "tensor_list.h"
#include "thread_pool.h"
namespace ts {
class CUDAStageV2 {
 public:
  CUDAStageV2(int device_id, uint32_t max_host_to_dev, uint32_t max_compute,
              uint32_t max_dev_to_host, uint32_t num_compute_threads = 1);

  ~CUDAStageV2();

  void Call(TensorList *tensors,
            std::function<std::unique_ptr<TensorList>(TensorList *)> compute,
            std::function<void(std::unique_ptr<TensorList>)> onComplete);

 private:
  struct Job {
    std::vector<at::Tensor> inputs_;
    std::function<std::unique_ptr<TensorList>(TensorList *)> compute_;
    std::function<void(std::unique_ptr<TensorList>)> on_complete_;
  };

  struct HostToDevJob {
    Job *job_;
  };

  struct ComputeJob {
    Job *job_;
    c10::cuda::CUDAStream stream_;
    TensorList *gpu_inputs_;
  };

  struct DevToHostJob {
    Job *job_;
    c10::cuda::CUDAStream stream_;
    TensorList *gpu_outputs_;
  };

  struct ComputeDone {
    DevToHostJob dev_to_host_job_;
    CUDAEvent event_;
  };

  using JobOrComputeDone = c10::variant<Job *, ComputeDone>;

  // returns true when exit
  bool onJobOrComputeDone(
      CUDAEventList *pending_events,
      std::unique_ptr<CUDAStageV2::JobOrComputeDone> job_or_compute_done);

  void hostToDev(CUDAEventList *list);
  void compute(CUDAEventList *list);
  void devToHost(CUDAEventList *list);

  int device_id_;
  uint32_t max_host_to_dev_;
  uint32_t max_compute_;
  uint32_t max_dev_to_host_;
  uint32_t num_host_to_dev_{0};
  uint32_t num_compute_{0};
  uint32_t num_dev_to_host_{0};
  std::shared_ptr<CUDAEventPool> event_pool_;
  BlockingQueue<std::unique_ptr<JobOrComputeDone>> jobs_;

  std::vector<c10::cuda::CUDAStream> streams_;
  std::queue<HostToDevJob> host_to_dev_jobs_;
  std::queue<ComputeJob> compute_jobs_;
  std::queue<DevToHostJob> dev_to_host_jobs_;
  std::unique_ptr<ThreadPool> worker_threadpool_;
  std::thread thread_;
};

}  // namespace ts