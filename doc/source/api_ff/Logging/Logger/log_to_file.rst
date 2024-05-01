log_to_file
============

.. py:method:: ff_Logger.log_to_file(filename='pymapdl.log', level=10) -> None

    为日志程序添加文件处理程序。

    :Parameters:

    filename : str, optional
        记录日志的文件名。默认为 ``'pymapdl.log'`` 。
    level : str or int, optional
        日志记录级别。默认为 ``'DEBUG'``。

    :Examples:

    写入当前工作目录下的 ``pymapdl.log``。

    >>> from ansys.mapdl.core import LOG
    >>> import os
    >>> file_path = os.path.join(os.getcwd(), 'pymapdl.log')
    >>> LOG.log_to_file(file_path)

