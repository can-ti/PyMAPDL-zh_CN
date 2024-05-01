get_default_ansys
==================

.. py:function:: ff_ansys.mapdl.core.launcher.get_default_ansys()

    在标准安装位置内搜索 ansys 路径，并返回已安装的最新 MAPDL 版本的路径和版本。

    :Returns:

        ansys_path : :class:`str`
            ANSYS 可执行文件的完整路径。

        version : :class:`float`
            版本浮点数。例如，21.1 对应于 2021R1。

    :Examples:

    Within Windows

    >>> from ansys.mapdl.core.launcher import get_default_ansys
    >>> get_default_ansys()
    'C:/Program Files/ANSYS Inc/v211/ANSYS/bin/winx64/ansys211.exe', 21.1

    Within Linux

    >>> get_default_ansys()
    (/usr/ansys_inc/v211/ansys/bin/ansys211, 21.1)
    """
    return find_ansys(supported_versions=SUPPORTED_ANSYS_VERSIONS)


