

.. _ref_launch_pymapdl:


Launch PyMAPDL
==============

PyMAPDL 可以在本地启动 MAPDL，也可以连接到已经在本地或远程机器上运行的会话。

* `Launch PyMAPDL with a local MAPDL instance`_
* `Connect PyMAPDL to a local MAPDL instance`_
* `Connect PyMAPDL to a remote MAPDL instance`_

如果您在启动 PyMAPDL 时遇到任何问题，请参阅 :ref:`Launching issues <ref_launching_issue>`。


Launch PyMAPDL with a local MAPDL instance
------------------------------------------

您可以使用 :func:`launch_mapdl() <ansys.mapdl.core.launcher.launch_mapdl>` 函数启动 MAPDL 并自动连接到它：

.. code:: python

    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl()
    >>> print(mapdl)
    Product:             Ansys Mechanical Enterprise
    MAPDL Version:       24.1
    ansys.mapdl Version: 0.68.0


虽然这是启动和运行 PyMAPDL 最简单快捷的方法，但您必须能够在本地启动 MAPDL。

如果 PyMAPDL 找不到您的本地安装，请参阅 `Setting the MAPDL location in PyMAPDL`_.

有关控制 MAPDL 本地启动方式的详细信息，请参阅 :func:`launch_mapdl() <ansys.mapdl.core.launcher.launch_mapdl>` 函数的说明。


Connect PyMAPDL to a local MAPDL instance
-----------------------------------------

连接本地 MAPDL 实例需要两个步骤：启动本地 MAPDL 会话和连接。

.. _launch_grpc_madpl_session:

Launch a local gRPC MAPDL session
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

您可以从命令行启动 MAPDL，然后连接到它。

要在 Windows 上启动 MAPDL（假设 Ansys 安装在 :file:`C:/Program Files/ANSYS Inc/v241` 目录下），请使用此命令：

.. code:: pwsh-session

    C:/Program Files/ANSYS Inc/v241/ansys/bin/winx64/ANSYS211.exe -grpc

要在 Linux 上启动 MAPDL（假设 Ansys 安装在 :file:`/usr/ansys_inc` 目录下），请使用此命令：

.. code:: console

    /usr/ansys_inc/v241/ansys/bin/ansys211 -grpc

这将以 gRPC 模式启动 MAPDL。MAPDL 应显示此输出：

.. code:: output

     Start GRPC Server

     ##############################
     ### START GRPC SERVER      ###
     ##############################

     Server Executable   : MapdlGrpc Server
     Server listening on : 0.0.0.0:50052

您可以使用 ``-port`` 参数配置 MAPDL 的启动端口。例如，可以使用此命令启动服务器，在端口 50005 上侦听连接：

.. code:: console

    /usr/ansys_inc/v241/ansys/bin/ansys211 -port 50005 -grpc

从 v0.68 版开始，您可以使用命令行界面启动、停止和列出本地 MAPDL 实例。更多信息，请参阅 :ref:`ref_cli`。

.. _connect_grpc_madpl_session:

Connect to the local MAPDL instance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

使用此代码可从同一主机连接到 MAPDL gRPC 服务器：

.. code:: python

    >>> from ansys.mapdl.core import Mapdl
    >>> mapdl = Mapdl()

前面的代码假定 MAPDL 服务在本地默认 IP 地址（ ``127.0.0.1`` ）和默认端口（ ``50052`` ）上运行。

您也可以使用 :func:`launch_mapdl() <ansys.mapdl.core.launcher.launch_mapdl>` 方法，通过将 `start_instance` 参数设置为 ``False`` 来连接到已经启动的 MAPDL 实例：

.. code:: python

    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl(start_instance=False)

如果您连接的是 MAPDL Docker 映像，操作步骤是一样的。只需确保指定映射端口，而不是 MAPDL 内部端口。更多信息，请参阅 :ref:`pymapdl_docker`。


.. _connect_grpc_remote_madpl_session:

Connect PyMAPDL to a remote MAPDL instance
------------------------------------------

如果要连接到 **远程** 的 MAPDL 实例，必须知道该实例的 IP 地址。例如，如果在本地网络中，IP 地址为 ``192.168.0.1`` 的计算机上运行着 MAPDL，端口为 ``50052``，则可使用此代码与之连接：

.. code:: python

    >>> mapdl = Mapdl("192.168.0.1", port=50052)

或者，也可以使用主机名：

.. code:: python

    >>> mapdl = Mapdl("myremotemachine", port=50052)

请注意，您必须在具有引用 IP 地址和主机名的计算机上以 gRPC 模式启动一个 MAPDL 实例，因为 PyMAPDL 无法启动远程实例。


Setting the MAPDL location in PyMAPDL
-------------------------------------

要运行 PyMAPDL，必须知道 MAPDL 二进制文件的位置。大多数情况下，这可以自动确定，但对于非标准安装，必须提供 MAPDL 的位置。首次运行时，如果 PyMAPDL 无法自动找到 MAPDL 可执行文件，则会请求它的位置。

您可以运行 :func:`launch_mapdl() <ansys.mapdl.core.launcher.launch_mapdl>` 函数来测试 PyMAPDL 的安装并进行设置：

.. code:: python

    from ansys.mapdl.core import launch_mapdl

    mapdl = launch_mapdl()

Python 会根据环境变量自动检测您的 MAPDL 二进制文件。您可以使用两个环境变量中的一个来指定 MAPDL 的安装：

* ``AWP_ROOTXXX`` ，其中 ``XXX`` 是三位数的版本号。该环境变量包含版本与 ``XXX`` 匹配的 Ansys 安装路径。例如， ``AWP_ROOT222=/ansys_inc`` 包含 Ansys 2022 R2 的安装路径。

* ``PYMAPDL_MAPDL_EXEC`` 包含 Ansys MAPDL 可执行文件的路径。例如， ``PYMAPDL_MAPDL_EXEC=/ansys_inc/v222/ansys/bin/ansys222`` 。

如果 PyMAPDL 无法找到 MAPDL 的副本，系统会提示您 MAPDL 可执行文件的位置。

以下是 Windows 系统的提示和响应示例：

.. code:: output

    Enter location of MAPDL executable: C:\Program Files\ANSYS Inc\v222\ANSYS\bin\winx64\ansys222.exe

以下是 Linux 系统的提示和响应示例：

.. code:: output

    Enter location of MAPDL executable: /usr/ansys_inc/v222/ansys/bin/ansys222

设置文件存储在本地，这意味着不会再次提示您输入路径。如果必须更改默认的 Ansys 路径（即更改 MAPDL 的默认版本），请运行此代码：

.. code:: python

    from ansys.mapdl import core as pymapdl

    new_path = "C:\\Program Files\\ANSYS Inc\\v212\\ANSYS\\bin\\winx64\\ansys222.exe"
    pymapdl.change_default_ansys_path(new_path)

更多信息，请参阅 :func:`change_default_ansys_path() <ansys.mapdl.core.change_default_ansys_path>` 方法和 :func:`find_ansys() <ansys.mapdl.core.find_ansys>` 方法。

此外，还可以使用 ``exec_file`` 关键字参数在每个 PyMAPDL 脚本中指定可执行文件。


**On Windows:**

.. code:: python

    from ansys.mapdl.core import launch_mapdl

    mapdl = launch_mapdl(
        exec_file="C://Program Files//ANSYS Inc//v212//ANSYS//bin//winx64//ansys212.exe"
    )

**On Linux:**

.. code:: python

    from ansys.mapdl.core import launch_mapdl

    mapdl = launch_mapdl(exec_file="/usr/ansys_inc/v212/ansys/bin/ansys212")


您还可以在 ``additional_switches`` 关键字参数中添加相应的标志 (``-custom``)，指定由自定义 MAPDL 编译生成的自定义可执行文件：

.. code:: python

    from ansys.mapdl.core import launch_mapdl

    custom_exec = "/usr/ansys_inc/v212/ansys/bin/ansys212t"
    add_switch = f" -custom {custom_exec}"
    mapdl = launch_mapdl(additional_switches=add_switch)
