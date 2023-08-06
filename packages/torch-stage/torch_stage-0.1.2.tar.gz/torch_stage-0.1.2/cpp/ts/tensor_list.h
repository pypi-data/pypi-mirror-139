#pragma once
#include <torch/extension.h>

#include <optional>
#include <vector>
namespace ts {

class TensorList {
 public:
  TensorList() = default;
  ~TensorList() = default;

  explicit TensorList(size_t n) { tensors_.reserve(n); }

  TensorList(const TensorList &) = delete;
  TensorList &operator=(const TensorList &) = delete;
  TensorList(TensorList &&) = delete;
  TensorList &operator=(TensorList &&) = delete;

  void push_back(at::Tensor tensor);
  size_t size() const;
  at::Tensor operator[](int index);
  void clear();

 private:
  std::vector<at::Tensor> tensors_;
};

inline void TensorList::push_back(at::Tensor tensor) {
  tensors_.push_back(tensor);
}

inline void TensorList::clear() { tensors_.clear(); }

inline size_t TensorList::size() const { return tensors_.size(); }

inline at::Tensor TensorList::operator[](int index) { return tensors_[index]; }

}  // namespace ts