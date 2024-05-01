get_default_ansys_version
===========================

.. py:function:: ff_ansys.mapdl.core.launcher.get_default_ansys_version()

    在标准安装位置内搜索 ansys 路径，并返回已安装的最新 MAPDL 版本。

    :Returns:

    :class:`float``
        版本浮点数。例如，21.1 对应于 2021R1。

    :Examples:

    Within Windows

    >>> from ansys.mapdl.core.launcher import get_default_ansys
    >>> get_default_ansys_version()
    21.1

    Within Linux

    >>> get_default_ansys_version()
    21.1
    """