add_child_logger
================

.. py:method:: ff_Logger.add_child_logger(sufix, level=None)

    为主日志记录器添加子日志记录器。

    该日志记录器比实例日志记录器更通用，后者旨在跟踪 MAPDL 实例的状态。

    如果参数中包含 ``level`` ，则会创建一个引用了 ``_global`` 日志记录器处理程序的新日志记录器，而不是创建一个子日志记录器。

    :Parameters:

    sufix : str
        记录器的名称。
    level : str or int, optional
        日志记录级别

    :Returns:

    logging.logger
        Logger 类。
