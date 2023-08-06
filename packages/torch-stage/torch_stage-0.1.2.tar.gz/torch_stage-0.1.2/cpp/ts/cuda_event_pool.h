#pragma once
#include <cuda_runtime.h>

#include <functional>
#include <iostream>
#include <list>
#include <memory>
#include <mutex>
#include <vector>

#include "c10/util/Exception.h"
namespace ts {

class CUDAEventPool;
class CUDAEvent {
 public:
  CUDAEvent() {
    TORCH_CHECK(false, "CUDAEvent is not supposed to be created directly");
  }
  CUDAEvent(const CUDAEvent &) = delete;
  CUDAEvent &operator=(const CUDAEvent &) = delete;

  CUDAEvent(CUDAEvent &&o) noexcept
      : event_(o.event_),
        pool_(std::move(o.pool_)),
        on_complete_(std::move(o.on_complete_)) {
    o.event_ = nullptr;
  }

  CUDAEvent &operator=(CUDAEvent &&o) noexcept {
    event_ = o.event_;
    pool_ = std::move(o.pool_);
    on_complete_ = std::move(o.on_complete_);
    o.event_ = nullptr;
    return *this;
  }

  bool TryWait();

  ~CUDAEvent();

 private:
  CUDAEvent(cudaEvent_t event, std::weak_ptr<CUDAEventPool> pool,
            std::function<void()> on_complete);

  cudaEvent_t event_{nullptr};
  std::weak_ptr<CUDAEventPool> pool_;
  std::function<void()> on_complete_;
  friend class CUDAEventPool;
};

class CUDAEventList {
 public:
  CUDAEventList();
  CUDAEventList(const CUDAEventList &) = delete;
  CUDAEventList &operator=(const CUDAEventList &) = delete;
  CUDAEventList(CUDAEventList &&) = delete;
  CUDAEventList &operator=(CUDAEventList &&) = delete;

  bool empty() const { return events_.empty(); }

  void push_back(CUDAEvent ev) { events_.push_back(std::move(ev)); }

  void TryWaitAndShrink();

 private:
  std::vector<CUDAEvent> events_;
};

class CUDAEventPool : public std::enable_shared_from_this<CUDAEventPool> {
 public:
  CUDAEventPool(size_t num_preallocated);
  ~CUDAEventPool();

  void RecordAndPushToList(CUDAEventList *list,
                           std::function<void()> on_event_done,
                           cudaStream_t stream);

  CUDAEvent RecordAndCreate(cudaStream_t stream,
                            std::function<void()> on_event_done);

 private:
  void freeEvent(cudaEvent_t ev);
  cudaEvent_t createOrGet();
  std::mutex mutex_;
  std::vector<cudaEvent_t> events_;
  friend class CUDAEvent;
};

}  // namespace ts