#include "cuda_stage.h"

#include <unistd.h>

#include "c10/cuda/CUDAGuard.h"
#include "c10/cuda/CUDAStream.h"
#include "tensor_list.h"
namespace ts {

static std::vector<c10::cuda::CUDAStream> CreateStreams(uint32_t size,
                                                        int device_id) {
  std::vector<c10::cuda::CUDAStream> streams;
  for (uint32_t i = 0; i < size; ++i) {
    streams.push_back(c10::cuda::getStreamFromPool(false, device_id));
  }
  streams.shrink_to_fit();
  return streams;
}

CUDAStageV2::CUDAStageV2(int device_id, uint32_t max_host_to_dev,
                         uint32_t max_compute, uint32_t max_dev_to_host,
                         uint32_t num_compute_threads)
    : device_id_(device_id),
      max_host_to_dev_(max_host_to_dev),
      max_compute_(max_compute),
      max_dev_to_host_(max_dev_to_host),
      event_pool_(std::make_shared<CUDAEventPool>(128)),
      streams_(CreateStreams(
          std::max(std::max(max_compute, max_dev_to_host), max_host_to_dev),
          device_id)),
      worker_threadpool_(std::make_unique<ThreadPool>(
          num_compute_threads,
          [] { torch::InferenceMode *mode = new torch::InferenceMode(); })),
      thread_([this] {
        torch::InferenceMode infer_guard_;
        CUDAEventList pending_events;
        std::vector<std::unique_ptr<JobOrComputeDone>>
            job_or_compute_done_caches;
        job_or_compute_done_caches.reserve(max_host_to_dev_);
        while (true) {
          if (pending_events.empty() && host_to_dev_jobs_.empty() &&
              dev_to_host_jobs_.empty() && compute_jobs_.empty()) {
            if (onJobOrComputeDone(&pending_events, jobs_.Pop())) {
              return;
            }
          }

          {  // collect job from jobs.
            jobs_.PopNoWait(&job_or_compute_done_caches);
            for (auto &job : job_or_compute_done_caches) {
              if (onJobOrComputeDone(&pending_events, std::move(job))) {
                return;
              }
            }
          }

          if (!pending_events.empty()) {  // buzy wait & query events
            pending_events.TryWaitAndShrink();
            std::this_thread::yield();
          }

          while (num_host_to_dev_ < max_host_to_dev_ &&
                 !host_to_dev_jobs_.empty() && !streams_.empty()) {
            hostToDev(&pending_events);
          }

          while (num_compute_ < max_compute_ && !compute_jobs_.empty()) {
            compute(&pending_events);
          }

          while (num_dev_to_host_ < max_dev_to_host_ &&
                 !dev_to_host_jobs_.empty()) {
            devToHost(&pending_events);
          }
        }
      }) {}

void CUDAStageV2::hostToDev(CUDAEventList *events) {
  auto *job = host_to_dev_jobs_.front().job_;
  host_to_dev_jobs_.pop();

  // NOTE: DeviceGuard is not needed because CUDAStreamGuard will set current
  // device implicitly.
  auto stream = streams_.back();
  streams_.pop_back();
  c10::cuda::CUDAStreamGuard streamGuard(stream);

  auto *gpu_inputs = new TensorList(job->inputs_.size());
  for (auto &t : job->inputs_) {
    auto gpu_tensor = torch::empty_like(
        t, c10::TensorOptions().device(stream.device()).dtype(t.dtype()));
    gpu_tensor.copy_(t, /*non_blocking=*/true);
    gpu_inputs->push_back(gpu_tensor);
  }

  ++num_host_to_dev_;

  event_pool_->RecordAndPushToList(
      events,
      [this, job] {
        job->inputs_.clear();
        --num_host_to_dev_;
      },
      stream.stream());
  compute_jobs_.emplace(ComputeJob{job, stream, gpu_inputs});
}

void CUDAStageV2::compute(CUDAEventList *events) {
  auto compute_job = compute_jobs_.front();
  compute_jobs_.pop();

  ++num_compute_;

  worker_threadpool_->Enqueue([=] {
    c10::cuda::CUDAStreamGuard streamGuard(compute_job.stream_);
    auto *gpu_outputs =
        compute_job.job_->compute_(compute_job.gpu_inputs_).release();
    {
      auto ev = event_pool_->RecordAndCreate(
          compute_job.stream_.stream(),
          [this, gpu_inputs = compute_job.gpu_inputs_] {
            delete gpu_inputs;
            --num_compute_;
          });

      ComputeDone done{
          DevToHostJob{compute_job.job_, compute_job.stream_, gpu_outputs},
          std::move(ev)};
      jobs_.Push(std::make_unique<JobOrComputeDone>(std::move(done)));
    }
  });
}

void CUDAStageV2::devToHost(CUDAEventList *events) {
  auto dev_to_host_job = dev_to_host_jobs_.front();
  dev_to_host_jobs_.pop();

  c10::cuda::CUDAStreamGuard streamGuard(dev_to_host_job.stream_);

  auto *cpu_outputs = new TensorList(dev_to_host_job.gpu_outputs_->size());
  for (size_t i = 0; i < dev_to_host_job.gpu_outputs_->size(); i++) {
    auto t = (*dev_to_host_job.gpu_outputs_)[i];
    auto cpu_tensor = torch::empty_like(
        t, c10::TensorOptions().device(torch::kCPU).dtype(t.dtype()));
    cpu_tensor.copy_(t, /*non_blocking=*/true);
    cpu_outputs->push_back(cpu_tensor);
  }
  ++num_dev_to_host_;
  event_pool_->RecordAndPushToList(
      events,
      [this, outputs = dev_to_host_job.gpu_outputs_, job = dev_to_host_job.job_,
       cpu_outputs, stream = std::move(dev_to_host_job.stream_)] {
        delete outputs;
        job->on_complete_(std::unique_ptr<TensorList>(cpu_outputs));
        delete job;
        streams_.emplace_back(std::move(stream));
        --num_dev_to_host_;
      },
      dev_to_host_job.stream_.stream());
}

bool CUDAStageV2::onJobOrComputeDone(
    CUDAEventList *pending_events,
    std::unique_ptr<CUDAStageV2::JobOrComputeDone> job) {
  if (job == nullptr) {
    return true;
  }
  if (c10::holds_alternative<Job *>(*job)) {
    auto j = c10::get<Job *>(*job);
    host_to_dev_jobs_.emplace(HostToDevJob{j});
  } else {
    auto e = std::move(c10::get<ComputeDone>(*job));
    pending_events->push_back(std::move(e.event_));
    dev_to_host_jobs_.emplace(std::move(e.dev_to_host_job_));
  }
  return false;
}

CUDAStageV2::~CUDAStageV2() {
  jobs_.Push(nullptr);
  thread_.join();
}

void CUDAStageV2::Call(
    TensorList *tensors,
    std::function<std::unique_ptr<TensorList>(TensorList *)> compute,
    std::function<void(std::unique_ptr<TensorList>)> onComplete) {
  std::vector<at::Tensor> cpu_inputs_;
  cpu_inputs_.reserve(tensors->size());
  for (size_t i = 0; i < tensors->size(); i++) {
    auto t = (*tensors)[i];
    if (!t.device().is_cpu()) {
      throw std::runtime_error("CUDAStage::Call: tensor must be on CPU");
    }
    cpu_inputs_.emplace_back(t);
  }
  auto job = new Job();
  job->inputs_ = std::move(cpu_inputs_);
  job->compute_ = std::move(compute);
  job->on_complete_ = std::move(onComplete);

  jobs_.Push(std::make_unique<JobOrComputeDone>(job));
}

}  // namespace ts