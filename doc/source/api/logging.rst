.. _api_logging:

Logging
=======

为了使事件的日志记录保持一致，PyMAPDL 采用了特定的日志记录架构，包括全局日志记录实例和本地日志记录实例。

对于这两类日志记录器，默认日志信息格式为

.. code:: pycon

    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl()
    >>> mapdl._log.info("This is an useful message")
      LEVEL - INSTANCE NAME - MODULE - FUNCTION - MESSAGE
      INFO - GRPC_127.0.0.1:50052 -  test - <module> - This is an useful message



``instance_name`` 字段取决于 MAPDL 实例的名称，创建日志记录时（例如，在库初始化期间）可能尚未设置该名称。如果尚未创建 MAPDL 实例，则该字段可能为空。

由于这两种类型的日志记录器都基于 Python 模块 ``logging``，因此您可以使用该模块提供的任何工具来扩展或修改这些日志记录器。


Logging API
-----------
.. currentmodule:: ansys.mapdl.core.logging

.. autosummary::
   :toctree: _autosummary

   Logger
