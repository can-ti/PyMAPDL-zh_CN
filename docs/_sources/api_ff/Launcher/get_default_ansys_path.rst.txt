get_default_ansys_path
======================

.. py:function:: ff_ansys.mapdl.core.launcher.get_default_ansys_path()

    在标准安装位置内搜索 ansys 路径，并返回已安装的最新 MAPDL 版本的路径。

    :Returns:

    :class:`str`
        ANSYS 可执行文件的完整路径。

    :Examples:

    Within Windows

    >>> from ansys.mapdl.core.launcher import get_default_ansys
    >>> get_default_ansys_path()
    'C:/Program Files/ANSYS Inc/v211/ANSYS/bin/winx64/ansys211.exe'

    Within Linux

    >>> get_default_ansys_path()
    '/usr/ansys_inc/v211/ansys/bin/ansys211'
