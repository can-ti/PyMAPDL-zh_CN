Logger
==========

.. py:class:: ff_ansys.mapdl.core.logging.Logger(level=10, to_file=False, to_stdout=True, filename='pymapdl.log')

    每个 PyMAPDL 会话使用的日志记录器。

    通过该类，您可以向日志记录器添加处理程序，以输出到文件或标准输出。

    :Parameters:

    level : int, optional
        日志级别，用于过滤日志记录器中允许的消息严重性。默认为 ``logging.DEBUG`` 。

    to_file : bool, optional
        将日志信息写入文件。默认为 ``False`` 。

    to_stdout : bool, optional
        将日志信息写入标准输出。默认为 ``True`` 。

    filename : str, optional
        写入日志信息的文件名。默认为 ``FILE_NAME`` 。

    :Examples:

    从实例 mapdl 演示日志记录器的使用。创建 Mapdl 实例时会自动创建该日志。

    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl(loglevel='DEBUG')
    >>> mapdl._log.info('This is a useful message')
    INFO -  -  <ipython-input-24-80df150fe31f> - <module> - This is LOG debug message.

    导入全局 pymapdl 日志记录器并添加文件输出处理程序。

    >>> import os
    >>> from ansys.mapdl.core import LOG
    >>> file_path = os.path.join(os.getcwd(), 'pymapdl.log')
    >>> LOG.log_to_file(file_path)

    :Methods:

    .. list-table:: Logger methods
        :widths: 10, 15
        :header-rows: 1

        * - Methods
          - Description
        * - :py:meth:`ff_Logger.add_child_logger`
          - 为主日志记录器添加子日志记录器。
        * - :py:meth:`ff_Logger.add_handling_uncaught_expections`
          - 这只是将异常输出重定向到日志记录器。
        * - :py:meth:`ff_Logger.add_instance_logger`
          - 为 MAPDL 实例创建日志记录器。
        * - :py:meth:`ff_Logger.log_to_file` 
          - 为日志程序添加文件处理程序。
        * - :py:meth:`ff_Logger.log_to_stdout` 
          - 为日志程序添加标准输出处理程序。
        * - :py:meth:`ff_Logger.setLevel` 
          - 更改对象和所附处理程序的日志级别。

    :Attributes:

    .. list-table:: Logger attributes
        :widths: auto

        * - :py:attr:`ff_Logger.file_handler`
        * - :py:attr:`ff_Logger.std_out_handler`



.. toctree::
    :hidden:
    :maxdepth: 1

    add_child_logger
    add_handling_uncaught_expections
    add_instance_logger
    log_to_file
    log_to_stdout
    setLevel
    file_handler
    std_out_handler
