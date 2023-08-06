#include <pybind11/functional.h>
#include <pybind11/pybind11.h>
#include <torch/extension.h>

#include "cuda_stage.h"
#include "tensor_list.h"

namespace ts {

namespace py = pybind11;

PYBIND11_MODULE(TORCH_EXTENSION_NAME, m) {
  py::class_<TensorList, std::unique_ptr<TensorList>>(m, "TensorList")
      .def(py::init<>())
      .def("append", &TensorList::push_back)
      .def("__len__", &TensorList::size)
      .def("__getitem__", &TensorList::operator[])
      .def("clear", &TensorList::clear);

  py::class_<CUDAStageV2>(m, "CUDAStage")
      .def(py::init<int, uint32_t, uint32_t, uint32_t, uint32_t>())
      .def(
          "call",
          [](CUDAStageV2 *stage, TensorList *tensors,
             std::function<void(TensorList *, TensorList *)> callback,
             std::function<void(TensorList *)> on_complete) {
            stage->Call(
                tensors,
                [callback](TensorList *inputs) -> std::unique_ptr<TensorList> {
                  auto outputs = std::make_unique<TensorList>();
                  { callback(inputs, outputs.get()); }
                  return outputs;
                },
                [on_complete](std::unique_ptr<TensorList> outputs) {
                  on_complete(outputs.get());
                });
          },
          py::call_guard<py::gil_scoped_release>());
}
}  // namespace ts