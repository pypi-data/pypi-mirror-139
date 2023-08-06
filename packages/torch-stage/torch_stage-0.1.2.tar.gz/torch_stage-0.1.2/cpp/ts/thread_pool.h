#pragma once

#include <functional>

#include "ATen/ATen.h"
#include "blocking_queue.h"

namespace ts {

class ThreadPool {
 public:
  ThreadPool(size_t num_threads, std::function<void()> th_init) {
    TORCH_CHECK(num_threads > 0, "num_threads must be greater than 0");
    for (size_t i = 0; i < num_threads; ++i) {
      threads_.emplace_back([this, th_init] {
        th_init();
        while (true) {
          auto task = tasks_.Pop();
          if (task == nullptr) {
            break;
          }
          task();
        }
      });
    }
  }

  ~ThreadPool() {
    for (size_t i = 0; i < threads_.size(); ++i) {
      tasks_.Push(nullptr);
    }
    for (auto &thread : threads_) {
      thread.join();
    }
  }

  void Enqueue(std::function<void()> fn) { tasks_.Push(std::move(fn)); }

 private:
  std::vector<std::thread> threads_;
  BlockingQueue<std::function<void()>> tasks_;
};

}  // namespace ts