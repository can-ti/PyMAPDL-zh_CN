.. _api_logging_ff:

Logging
=======

为了使事件的日志记录保持一致，PyMAPDL 采用了特定的日志记录架构，包括全局日志记录实例和本地日志记录实例。

对于这两类日志记录器，默认日志信息格式为

.. code:: python

    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl()
    >>> mapdl._log.info("This is an useful message")

    LEVEL - INSTANCE NAME - MODULE - FUNCTION - MESSAGE
    INFO - GRPC_127.0.0.1:50052 -  test - <module> - This is an useful message

``instance_name`` 字段取决于 MAPDL 实例的名称，创建日志记录时（例如，在库初始化期间）可能尚未设置该名称。如果尚未创建 MAPDL 实例，则该字段可能为空。

由于这两种类型的日志记录器都基于 Python 模块 ``logging``，因此您可以使用该模块提供的任何工具来扩展或修改这些日志记录器。


该模块为 PyMAPDL 中的日志提供了一个通用框架。本模块建立在 `logging <https://docs.python.org/3/library/logging.html>`_ 库的基础上，并不打算取代它，而是提供一种在 ``logging`` 和 PyMAPDL 之间交互的方式。

模块中使用的日志记录器包括实例的名称，该名称必须是唯一的。该名称会打印在所有活动输出中，用于跟踪不同的 MAPDL 实例。


How to use
-----------

全局 logger
~~~~~~~~~~~~~
有一个名为 ``pymapdl_global```的全局日志记录器，它是在 ``ansys.mapdl.core.__init___`` 中创建的。如果要使用这个全局日志记录器，必须在模块顶部调用：

.. code:: python

   from ansys.mapdl.core import LOG

您还可以重命名它，以避免与其他 logger （如果有的话）发生冲突：

.. code:: python

   from ansys.mapdl.core import LOG as logger


应该注意的是，``LOG`` 的默认日志级别是 ``ERROR`` 。要更改并输出较低级别的信息，可以使用下一个代码段：

.. code:: python

   LOG.logger.setLevel("DEBUG")
   LOG.file_handler.setLevel("DEBUG")  # If present.
   LOG.std_out_handler.setLevel("DEBUG")  # If present.


或者：

.. code:: python

   LOG.setLevel("DEBUG")

这样可以确保所有处理程序都设置为输入日志级别。

默认情况下，此日志记录器不会将日志记录到文件中。如果希望这样做，可以使用以下命令添加文件处理程序：

.. code:: python

   import os

   file_path = os.path.join(os.getcwd(), "pymapdl.log")
   LOG.log_to_file(file_path)

这将使日志记录器也重定向到该文件。如果希望从执行之初就更改全局日志记录器的特性，则必须编辑目录 ``ansys.mapdl.core`` 中的文件 ``__init__``  。

要使用此日志记录器进行日志记录，只需像普通日志记录器一样调用所需的方法即可。

.. code:: pycon

    >>> import logging
    >>> from ansys.mapdl.core.logging import Logger
    >>> LOG = Logger(level=logging.DEBUG, to_file=False, to_stdout=True)
    >>> LOG.debug("This is LOG debug message.")

    DEBUG -  -  <ipython-input-24-80df150fe31f> - <module> - This is LOG debug message.


实例化记录器
~~~~~~~~~~~~~~~
每次创建 :class:`Mapdl <ansys.mapdl.core.mapdl.MapdlBase>` 的实例时，都会创建一个日志记录器并将其存储在两个地方：

* ``MapdlBase._log``. 向后兼容。
* ``LOG._instances``. 该字段是一个 ``dict`` 字段，其中的键是创建的日志记录器的名称。

除非另有说明，否则这些实例日志记录器将继承 ``pymapdl_global`` 输出处理程序和日志记录级别。
该日志记录器的工作方式与全局日志记录器非常相似。您可以使用 :func:`log_to_file() <PymapdlCustomAdapter.log_to_file>` 添加文件处理程序，或使用 :func:`logger.Logging.setLevel` 更改日志级别。

您可以这样使用该记录仪：

.. code:: pycon

    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl()
    >>> mapdl._log.info("This is a useful message")

    INFO - GRPC_127.0.0.1:50056 -  <ipython-input-19-f09bb2d8785c> - <module> - This is a useful message



Other loggers
~~~~~~~~~~~~~

您可以使用 python ``logging`` 库创建自己的日志记录器，就像在其他脚本中一样。这些日志记录器之间不会发生冲突。



Logging API
-----------

.. list-table:: 
    :widths: 10 15
    :header-rows: 1

    * - Class
      - Description
    * - :py:class:`ff_ansys.mapdl.core.logging.Logger([level, to_file, to_stdout, filename])`
      - 每个 Pymapdl 会话使用的日志记录器。


.. toctree::
    :hidden:
    :maxdepth: 1

    Logger/index