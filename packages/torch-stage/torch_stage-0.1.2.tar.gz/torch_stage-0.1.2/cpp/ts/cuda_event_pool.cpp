#include "cuda_event_pool.h"

#include <iostream>

#include "c10/cuda/CUDAException.h"
namespace ts {

CUDAEventPool::CUDAEventPool(size_t num_preallocated) {
  events_.reserve(num_preallocated);
  for (size_t i = 0; i < num_preallocated; ++i) {
    cudaEvent_t event;
    C10_CUDA_CHECK(cudaEventCreateWithFlags(&event, cudaEventDisableTiming));
    events_.emplace_back(event);
  }
}

CUDAEventPool::~CUDAEventPool() {
  std::lock_guard<std::mutex> lock(mutex_);
  for (auto event : events_) {
    cudaEventDestroy(event);
  }
}

void CUDAEventPool::freeEvent(cudaEvent_t ev) {
  std::lock_guard<std::mutex> lock(mutex_);
  events_.emplace_back(ev);
}

CUDAEvent::CUDAEvent(cudaEvent_t event, std::weak_ptr<CUDAEventPool> pool,
                     std::function<void()> on_complete)
    : event_(event),
      pool_(std::move(pool)),
      on_complete_(std::move(on_complete)) {}

CUDAEvent::~CUDAEvent() {
  if (pool_.lock() != nullptr) {
    std::cerr << "this event is not wait, it is a bug in code" << std::endl;
  }
}

bool CUDAEvent::TryWait() {
  if (cudaEventQuery(event_) == cudaSuccess) {
    on_complete_();
    auto p = pool_.lock();
    if (p != nullptr) {
      p->freeEvent(event_);
    }
    pool_.reset();
    on_complete_ = nullptr;
    return true;
  }
  return false;
}

CUDAEventList::CUDAEventList() { events_.reserve(256); }

void CUDAEventList::TryWaitAndShrink() {
  size_t to_remove_counter = 0;
  for (size_t i = 0; i < events_.size(); i++) {
    auto &ev = events_[events_.size() - 1 - i];
    bool ok = ev.TryWait();
    if (ok) {
      if (i != to_remove_counter) {
        std::swap(ev, events_[events_.size() - 1 - to_remove_counter]);
      }
      ++to_remove_counter;
    }
  }

  events_.resize(events_.size() - to_remove_counter);
}

cudaEvent_t CUDAEventPool::createOrGet() {
  std::lock_guard<std::mutex> lock(mutex_);
  if (events_.empty()) {
    cudaEvent_t event;
    C10_CUDA_CHECK(cudaEventCreateWithFlags(&event, cudaEventDisableTiming));
    events_.emplace_back(event);
  }
  auto event = events_.back();
  events_.pop_back();
  return event;
}

void CUDAEventPool::RecordAndPushToList(CUDAEventList *list,
                                        std::function<void()> on_event_done,
                                        cudaStream_t stream) {
  list->push_back(RecordAndCreate(stream, std::move(on_event_done)));
}

CUDAEvent CUDAEventPool::RecordAndCreate(cudaStream_t stream,
                                         std::function<void()> on_event_done) {
  auto ev = createOrGet();
  C10_CUDA_CHECK(cudaEventRecord(ev, stream));
  return CUDAEvent(ev, shared_from_this(), std::move(on_event_done));
}

}  // namespace ts