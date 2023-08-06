#pragma once

#include <condition_variable>
#include <mutex>
#include <queue>

namespace ts {

template <typename T>
class BlockingQueue {
 public:
  void Push(T &&item) {
    std::lock_guard<std::mutex> lock(mutex_);
    queue_.emplace(std::move(item));
    not_empty_.notify_one();
  }

  T Pop() {
    std::unique_lock<std::mutex> lock(mutex_);
    not_empty_.wait(lock, [this] { return !queue_.empty(); });
    T item = std::move(queue_.front());
    queue_.pop();
    return item;
  }

  void PopNoWait(std::vector<T> *items) {
    items->clear();
    std::unique_lock<std::mutex> lock(mutex_);
    while (!queue_.empty()) {
      items->emplace_back(std::move(queue_.front()));
      queue_.pop();
      return;
    }
  }

 private:
  std::queue<T> queue_;
  std::mutex mutex_;
  std::condition_variable not_empty_;
};

}  // namespace ts