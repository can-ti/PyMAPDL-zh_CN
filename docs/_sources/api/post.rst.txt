.. _post_processing_api:


``PostProcessing`` class
========================

``PostProcessing`` 类支持直接从 MAPDL 实时实例进行后处理。如果您想在 PyMAPDL 之外对 MAPDL 结果文件进行后处理，可以使用这些软件包之一：

* `PyDPF-Core <dpf_core_docs_>`_ : 使用数据处理框架（DPF）进行后处理。DPF-Core 提供更复杂、更强大的后处理 API。
* `PyDPF-Post <dpf_post_docs_>`_ : 简化的 DPF 后处理。PyDPF-Post 是一个使用 PyDPF-Core 的高级软件包。
* `PyMAPDL Reader <legacy_reader_docs_>`_: 传统结果文件阅读器。PyMAPDL 阅读器支持 MAPDL 14.5 及更高版本的结果文件。

.. currentmodule:: ansys.mapdl.core

.. autosummary::
   :toctree: _autosummary

   post.PostProcessing
