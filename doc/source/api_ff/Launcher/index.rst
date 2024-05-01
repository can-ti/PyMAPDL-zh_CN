.. _ref_launcher_api_ff:

Launcher
========

各种 PyMAPDL 特定的 launcher(启动器) 命令。这些命令大多从 `ansys-tools-path <ansys_tools_path_>`_ 库中调用。

.. list-table:: Launcher functions
    :widths: 10 15
    :header-rows: 1

    * - Functions
      - Description
    * - :py:func:`ff_ansys.mapdl.core.launcher.get_default_ansys()`
      - 在标准安装位置内搜索 ansys 路径，并返回已安装的最新 MAPDL 版本的路径和版本。
    * - :py:func:`ff_ansys.mapdl.core.launcher.get_default_ansys_path()`
      - 在标准安装位置内搜索 ansys 路径，并返回已安装的最新 MAPDL 版本的路径。
    * - :py:func:`ff_ansys.mapdl.core.launcher.get_default_ansys_version()`
      - 在标准安装位置内搜索 ansys 路径，并返回已安装的最新 MAPDL 版本。
    * - :py:func:`ff_ansys.mapdl.core.launcher.launch_mapdl()` 
      - 在本地启动 MAPDL。
    * - :py:func:`ff_ansys.mapdl.core.launcher.close_all_local_instances()` 
      - 关闭端口范围内的所有 MAPDL 实例。



.. toctree::
    :hidden:
    :maxdepth: 1

    get_default_ansys
    get_default_ansys_path
    get_default_ansys_version
    launch_mapdl
    close_all_local_instances