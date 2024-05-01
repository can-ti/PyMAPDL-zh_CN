.. _ref_troubleshooting:


Troubleshooting PyMAPDL
=======================


为了帮助您解决使用 PyMAPDL 时可能遇到的任何问题，这里发布了一些常见问题。


Debug in PyMAPDL
----------------

如果您在使用 PyMAPDL 时遇到问题，可以使用日志记录器将一些内部日志记录到文件中。
检查该文件有助于发现任何问题。

您可以在 Python 终端或脚本开头运行以下命令，将日志记录器输出文件设置为 ``mylog.log`` ：

.. code:: python

    from ansys.mapdl.core import LOG

    LOG.setLevel("DEBUG")
    LOG.log_to_file("mylog.log")

    from ansys.mapdl.core import launch_mapdl

    mapdl = launch_mapdl(loglevel="DEBUG")

您可以将此文件附加到 PyMAPDL GitHub 代码库的错误报告中，以便进一步调查。
如果无法确定问题，可以在 `PyMAPDL Discussions page <pymapdl_discussions_>`_ 上展开讨论。
如果您认为您发现了一个bug，请在 `PyMAPDL Issues page <pymapdl_issues_>`_ 页面上创建一个问题。

.. _ref_launching_issue:

Launching issues
----------------

有几个问题可能导致 MAPDL 无法启动，包括

- `Connection timeout`_
- `Testing MAPDL launching`_
- `Licensing issues`_
- `Virtual private network (VPN) issues`_
- `Missing dependencies on Linux`_
- `Conflicts with student version`_
- `Incorrect environment variables`_
- `Using a proxy server`_
- `Firewall settings`_

如果找不到问题，请参阅 `More help needed?`_ 。

Connection timeout
~~~~~~~~~~~~~~~~~~

在某些网络中，MAPDL 连接到许可证服务器或远程实例的时间可能比预期的要长。在这种情况下，您可能会看到此消息：


.. code:: output

    PyMAPDL is taking longer than expected to connect to an MAPDL session. Checking if there are any available licenses...
     | PyMAPDL 连接到 MAPDL 会话的时间比预期的长。正在检查是否有可用的许可证。。。


首先尝试使用此代码增加启动超时：

.. code:: python

    from ansys.mapdl.core import launch_mapdl

    mapdl = launch_mapdl(start_timeout=60)

或者，如果您正在连接远程实例，可以使用

.. code:: python

    from ansys.mapdl.core import Mapdl

    mapdl = Mapdl(timeout=60)


Testing MAPDL launching
~~~~~~~~~~~~~~~~~~~~~~~

在某些情况下，可能需要从命令行手动运行启动命令。


运行与版本相关的命令：


.. tab-set::

    .. tab-item:: Windows

        .. code:: pwsh-session

            "C:\Program Files\ANSYS Inc\v211\ansys\bin\winx64\ANSYS211.exe"

        .. note:: PowerShell 用户可以不加引号运行前面的命令。

    .. tab-item:: Linux

        .. code:: console

            /usr/ansys_inc/v211/ansys/bin/ansys211


您应该在临时工作目录中启动 MAPDL，因为 MAPDL 创建了几个临时文件。

可以通过从临时目录启动 MAPDL 来指定目录：

.. code:: pwsh-session

    mkdir temporary_directory
    cd temporary_directory
    & 'C:\Program Files\ANSYS Inc\v222\ansys\bin\winx64\ANSYS222.exe'

或者使用 ``-dir`` 标记指定目录：

.. code:: pwsh-session

    mkdir temporary_directory
    & 'C:\Program Files\ANSYS Inc\v222\ansys\bin\winx64\ANSYS222.exe' -dir "C:\ansys_job\mytest1"


如果该命令不能启动 MAPDL，请查看命令输出：

.. vale off

.. code:: pwsh-session

    (base) PS C:\Users\user\temp> & 'C:\Program Files\ANSYS Inc\v222\ansys\bin\winx64\ANSYS222.exe'
    *** ERROR ***
    Another Ansys job with the same job name (file) is already running in this
    directory or the file.lock file has not been deleted from an abnormally
    terminated Ansys run. To disable this check, set the ANSYS_LOCK environment
    variable to OFF. | 该目录中已经运行了另一个具有相同作业名（文件）的 Ansys 作业，或者在异常终止的 Ansys 运行中未删除 file.lock 文件。要禁用此检查，请将 ANSYS_LOCK 环境变量设置为 OFF。

.. vale on

Licensing issues
~~~~~~~~~~~~~~~~

许可证服务器配置不正确会导致 MAPDL 无法获得有效的许可证。在这种情况下，您可能会看到 **类似** 的输出：

.. code:: pwsh-session

   (base) PS C:\Users\user\temp> & 'C:\Program Files\ANSYS Inc\v222\ansys\bin\winx64\ANSYS222.exe'

   ANSYS LICENSE MANAGER ERROR:

   Maximum licensed number of demo users already reached. | 已达到最大许可演示用户数。


   ANSYS LICENSE MANAGER ERROR:

   Request name mech_2 does not exist in the licensing pool. | 许可池中不存在请求名称 mech_2。
   No such feature exists.
   Feature:          mech_2
   License path:  C:\Users\user\AppData\Local\Temp\\cb0400ba-6edb-4bb9-a333-41e7318c007d;
   FlexNet Licensing error:-5,357


PADT 有一个很好的关于 ANSYS 问题的博客，而许可总是一个常见问题。例如，请参阅 `Changes to Licensing at ANSYS 2020R1 <padt_licensing_>`_ 。
如果您负责维护 Ansys 许可或个人安装了 Ansys，请参阅在线 `Ansys 安装和许可文档 <ansys_installation_and_licensing_>`_ 。

有关更全面的信息，请下载 :download:`ANSYS Licensing Guide <lic_guide.pdf>` 。

Incorrect licensing environment variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

也可以使用环境变量 :envvar:`ANSYSLMD_LICENSE_FILE` 指定许可证服务器。以下代码示例展示了如何在 Windows 或 Linux 环境中查看该环境变量的值。

.. tab-set:: 

    .. tab-item:: Windows

        .. code:: pwsh-session

            $env:ANSYSLMD_LICENSE_FILE
            1055@1.1.1.1

    .. tab-item:: Linux

        .. code:: console

            printenv | grep ANSYSLMD_LICENSE_FILE

.. _vpn_issues_troubleshooting:

Virtual private network (VPN) issues
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

从 ANSYS 2022 R2 到 ANSYS 2021 R1，当运行 VPN 软件时，MAPDL 会出现启动问题。其中一个问题源于 MPI 通信，解决方法是通过 ``-smp`` 选项将执行模式设置为 "共享内存并行"，从而禁用默认的 "分布式内存并行"。
或者使用不同的 MPI 编译，例如，如果使用 Windows，可以通过 ``-mpi msmpi`` 使用 Microsoft MPI 库，而不是默认的 Intel MPI 库。此问题不影响 Linux 版本的 MAPDL。

.. note:: 
    如果您在 ANSYS 2022 R2 至 ANSYS 2021 R1 的任何版本中使用 Windows，则在 PyMAPDL 启动 MAPDL 实例时，默认编译器为 Microsoft MPI。

.. code:: python

    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl(additional_switches="-smp")

虽然这种方法的缺点是使用可能较慢的共享内存并行模式，但至少可以运行 MAPDL。
有关共享内存与分布式内存的更多信息，请参阅 `High-Performance Computing for Mechanical Simulations using ANSYS (基于 ANSYS 的高性能力学仿真计算) <ansys_parallel_computing_guide_>`_。

此外，如果您的设备在 VPN 内，MAPDL 可能无法正确解析许可证服务器的 IP。请确认许可证服务器的主机名或 IP 地址是否正确。

在 Windows 系统中，您可以在以下位置找到指向许可证服务器的许可证配置文件：

.. code:: text

    C:\Program Files\ANSYS Inc\Shared Files\Licensing\ansyslmd.ini


.. _missing_dependencies_on_linux:

Missing dependencies on Linux
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

某些 Linux 安装可能缺少所需的依赖项。如果出现类似 ``libXp.so.6: cannot open shared object file: No such file or directory`` 等错误，则很可能缺少某些必要的依赖项。

**CentOS 7**

在 CentOS 7 上，您可以使用以下方法安装缺失的依赖项：

.. code:: console

    yum install openssl openssh-clients mesa-libGL mesa-libGLU motif libgfortran


**Ubuntu**

在 Ubuntu 22.04 上，使用此代码安装所需的依赖项：

.. code:: console

    apt-get update

    # Install dependencies
    apt-get install -y \
    openssh-client \
    libgl1 \
    libglu1 \
    libxm4 \
    libxi6

前面的代码会处理除 ``libxp6`` 以外的所有内容，您必须使用此代码安装它：

.. code:: console

    # This is a workaround
    # Source: https://bugs.launchpad.net/ubuntu/+source/libxp/+bug/1517884
    apt install -y software-properties-common
    add-apt-repository -y ppa:zeehio/libxp
    apt-get update
    apt-get install -y libxp6


**Ubuntu 20.04 and older**

如果您使用的是 Ubuntu 16.04，您可以使用此代码安装 ``libxp16``：

.. code:: console

   sudo apt install libxp6. 
   
不过，如果您使用的是 Ubuntu 18.04 至 20.04，则必须手动下载并安装该软件包。

由于 ``libxpl6`` 预先依赖于 ``multiarch-support``，而后者也已过时，因此必须删除。 
否则，你的软件包配置就会被破坏。下面的代码下载并修改 ``libxp6`` 软件包，
移除 ``multiarch-support`` 依赖关系，然后通过 ``dpkg`` 软件包安装。

.. code:: console

    cd /tmp
    wget http://ftp.br.debian.org/debian/pool/main/libx/libxp/libxp6_1.0.2-2_amd64.deb
    ar x libxp6_1.0.2-2_amd64.deb
    sudo tar xzf control.tar.gz
    sudo sed '/Pre-Depends/d' control -i
    sudo bash -c "tar c postinst postrm md5sums control | gzip -c > control.tar.gz"
    sudo ar rcs libxp6_1.0.2-2_amd64_mod.deb debian-binary control.tar.gz data.tar.xz
    sudo dpkg -i ./libxp6_1.0.2-2_amd64_mod.deb


.. _conflicts_student_version:

Conflicts with student version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

虽然可以在 Windows 上将 Ansys 与其他 Ansys 产品或版本一起安装，但不应将 Ansys 产品的学生版与其非学生版一起安装。
例如，同时安装 Ansys MAPDL 2022 R2 学生版和 Ansys MAPDL 2022 R2 可能会因覆盖环境变量而导致许可证冲突。
安装不同的版本（例如 Ansys MAPDL 2022 R2 学生版和 Ansys MAPDL 2021 R1）是没有问题的。

如果遇到问题，应编辑这些环境变量，删除对学生版本的任何引用： ``ANSYSXXX_DIR`` 、 ``AWP_ROOTXXX`` 和 ``CADOE_LIBDIRXXX`` 。
有关如何将这些环境变量设置到正确位置的信息，请访问 `Incorrect environment variables`_ 。


.. note:: Launching MAPDL Student Version
   默认情况下，如果检测到学生版本，PyMAPDL 会以 ``SMP`` 模式启动 MAPDL 实例，除非指定了其他 MPI 选项。

Incorrect environment variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

如果使用非标准安装，可能需要手动将环境变量 ``ANSYSXXX_DIR``, ``AWP_ROOTXXX`` 和 ``CADOE_LIBDIRXXX`` 设置到正确的位置。
三位数的 MAPDL 版本出现在显示 ``XXX`` 的位置。对于 Ansys MAPDL 2022 R2，在显示 ``XXX`` 的地方显示 ``222``。


.. vale off

.. code:: pwsh-session

    PS echo $env:AWP_ROOT222
    C:\Program Files\ANSYS Inc\ANSYS Student\v222
    PS $env:AWP_ROOT222 = "C:\Program Files\ANSYS Inc\v222"  # This overwrites the env var for the terminal session only.
    PS [System.Environment]::SetEnvironmentVariable('AWP_ROOT222','C:\Program Files\ANSYS Inc\v222',[System.EnvironmentVariableTarget]::User)  # This changes the env var permanently.
    PS echo $env:AWP_ROOT222
    C:\Program Files\ANSYS Inc\v222

    PS echo $env:ANSYS222_DIR
    C:\Program Files\ANSYS Inc\ANSYS Student\v222\ANSYS
    PS [System.Environment]::SetEnvironmentVariable('ANSYS222_DIR','C:\Program Files\ANSYS Inc\v222\ANSYS',[System.EnvironmentVariableTarget]::User)
    PS echo $env:ANSYS222_DIR
    C:\Program Files\ANSYS Inc\v222\ANSYS

    PS echo $env:CADOE_LIBDIR222
    C:\Program Files\ANSYS Inc\ANSYS Student\v222\CommonFiles\Language\en-us
    PS [System.Environment]::SetEnvironmentVariable('CADOE_LIBDIR222','C:\Program Files\ANSYS Inc\v222\CommonFiles\Language\en-us',[System.EnvironmentVariableTarget]::User)
    PS echo $env:CADOE_LIBDIR222
    C:\Program Files\ANSYS Inc\v222\CommonFiles\Language\en-us

.. vale on

Using a proxy server
~~~~~~~~~~~~~~~~~~~~

在极少数情况下，如果使用代理，在连接 MAPDL 实例时可能会遇到一些问题。
在代理环境中使用 `gRPC <grpc_>`_ 时，如果指定了本地地址（即 ``127.0.0.1``）作为连接目标，gRPC 实现会自动引用代理地址。
在这种情况下，本地地址无法被引用，从而导致连接错误。
作为一种变通方法，您可以将环境变量 ``NO_PROXY`` 设置为本地地址 ``127.0.0.1``，然后运行 :func:`launch_mapdl() <ansys.mapdl.core.launcher.launch_mapdl>` 连接到 MAPDL 实例。


Firewall settings
~~~~~~~~~~~~~~~~~

MAPDL 和 Python 应有正确的防火墙设置，以允许两者之间的通信。
如果使用防火墙，则应允许 MAPDL 接收以下端口的入站连接：

* 50052 (TCP) for gRPC connection.
* 50053+ (TCP) for extra gRPC connection.
* 50055 (TCP) for gRPC connection to the MAPDL database.

必须允许 Python 进程连接到上述端口（出站连接）。

通常情况下，大多数防火墙规则都侧重于入站连接，因此不需要配置出站连接。但是，如果遇到问题，应确保防火墙没有阻止以下端口的出站连接：

* 5005X (TCP) for gRPC connections.
* 50055 (TCP) for gRPC connection to the MAPDL database.
* 1055 (TCP) for licensing connections.
* 2325 (TCP) for licensing connections.

有关如何在 Windows 上 **配置防火墙的详细信息** ，请参阅 `Ansys forum-Licensing 2022 R2 Linux Ubuntu (and also Windows) <af_licensing_windows_ubuntu_>`_ 中的以下链接。

有关如何在 Ubuntu Linux 上 **配置防火墙的详细信息** ，请参阅以下链接 `Security-Firewall | Ubuntu <ubuntu_firewall_>`_ 。


Location of the executable file
-------------------------------

手动设置可执行文件的位置
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

如果您安装的是非标准安装，PyMAPDL 可能无法找到您的 MAPDL 安装。如果是这种情况，请将 MAPDL 的位置作为 :func:`launch_mapdl() <ansys.mapdl.core.launcher.launch_mapdl>` 方法的第一个参数。


.. tab-set::

    .. tab-item:: Windows

        .. code:: python

            >>> from ansys.mapdl.core import launch_mapdl
            >>> exec_loc = "C:/Program Files/ANSYS Inc/v211/ansys/bin/winx64/ANSYS211.exe"
            >>> mapdl = launch_mapdl(exec_loc)


    .. tab-item:: Linux

        .. code:: python

            >>> from ansys.mapdl.core import launch_mapdl
            >>> exec_loc = "/usr/ansys_inc/v211/ansys/bin/ansys211"
            >>> mapdl = launch_mapdl(exec_loc)



可执行文件的默认位置
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

首次运行 PyMAPDL 时，它会检测可用的 Ansys 安装。

**On Windows**

Ansys 的安装通常在

.. code:: text

    C:/Program Files/ANSYS Inc/vXXX


**On Linux**

Ansys 的安装通常在

.. code:: text

    /usr/ansys_inc/vXXX
    
或在：

.. code:: text

   /ansys_inc/vXXX

默认情况下，Ansys 安装程序使用前者 (``/usr/ansys_inc``)，但也会为后者创建一个符号 (``/ansys_inc``)。

如果 PyMAPDL 找到一个有效的 Ansys 安装，它会将其路径缓存到配置文件 ``config.txt`` 中。该文件的路径如代码所示：

.. code:: python

    >>> from ansys.mapdl.core.launcher import CONFIG_FILE
    >>> print(CONFIG_FILE)
    'C:\\Users\\user\\AppData\\Local\\ansys_mapdl_core\\ansys_mapdl_core\\config.txt'


在某些情况下，此配置文件可能会过时。例如，安装了新的 Ansys 版本并删除了之前的安装。

要使用最新路径更新配置文件，请使用

.. code:: python

    >>> from ansys.mapdl.core import save_ansys_path
    >>> save_ansys_path(r"C:\Program Files\ANSYS Inc\v222\ansys\bin\winx64\ansys222.exe")
    'C:\\Program Files\\ANSYS Inc\\v222\\ansys\\bin\\winx64\\ansys222.exe'

如果要查看 PyMAPDL 检测到了哪些 Ansys 安装，请使用

.. code:: python

    >>> from ansys.mapdl.core import get_available_ansys_installations
    >>> get_available_ansys_installations()
    {222: 'C:\\Program Files\\ANSYS Inc\\v222',
    212: 'C:\\Program Files\\ANSYS Inc\\v212',
    -222: 'C:\\Program Files\\ANSYS Inc\\ANSYS Student\\v222'}


由于 Python 字典不接受两个相等的键，因此学生版本以 **negative** 的形式提供。
:func:`get_available_ansys_installations() <ansys.mapdl.core.get_available_ansys_installations>` 方法的结果首先列出高版本，最后列出学生版本。


.. warning::
    不应安装相同的 Ansys 产品版本和学生版本。有关详细信息，请参阅 :ref:`conflicts_student_version`。


PyMAPDL usage issues
--------------------

.. _ref_issues_np_mapdl:

在 MAPDL 中导入和导出 NumPy 数组时出现的问题
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

由于 MAPDL 的设计方式，无法存储一个或多个维数为零的数组。
这种情况可能发生在 NumPy 数组中，因为数组的第一个维度可以设置为零。例如

.. code:: python

   >>> import numpy
   >>> from ansys.mapdl.core import launch_mapdl
   >>> mapdl = launch_mapdl()
   >>> my_array = np.reshape([1, 2, 3, 4], (4,))
   >>> my_array
   array([1, 2, 3, 4])


这些类型的数组维数总是转换为 ``1``。

For example:

.. code:: python

   >>> mapdl.parameters["mapdlarray"] = my_array
   >>> mapdl.parameters["mapdlarray"]
   array([[1.],
      [2.],
      [3.],
      [4.]])
   >>> mapdl.parameters["mapdlarray"].shape
   (4, 1)

这意味着，当您传递两个数组时，一个数组的第二个轴等于零（例如， ``my_array`` ），另一个数组的第二个轴等于一，如果稍后检索，这两个数组将具有相同的形状。

.. code:: python

   >>> my_other_array = np.reshape([1, 2, 3, 4], (4, 1))
   >>> my_other_array
   array([[1],
      [2],
      [3],
      [4]])
   >>> mapdl.parameters["mapdlarray_b"] = my_other_array
   >>> mapdl.parameters["mapdlarray_b"]
   array([[1.],
      [2.],
      [3.],
      [4.]])
   >>> np.allclose(mapdl.parameters["mapdlarray"], mapdl.parameters["mapdlarray_b"])
   True


.. _ref_pymapdl_stability:

PyMAPDL stability
-----------------

Recommendations
~~~~~~~~~~~~~~~

使用 gRPC（默认）连接到 MAPDL 实例时，在某些情况下 MAPDL 服务器可能会意外退出。有几种方法可以提高 MADPL 的性能和稳定性：

Use ``mute`` to improve stability
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

在可能的情况下，将 ``mute=True`` 传递给单个 MAPDL 命令，或使用 :func:`Mapdl.mute <ansys.mapdl.core.mapdl_grpc.MapdlGrpc>` 方法进行全局设置。
这样就可以禁止从 MAPDL 回传每条命令的响应流，从而略微提高性能和稳定性。考虑在程序或脚本中加入调试标记，以便根据需要打开或关闭日志记录和冗余度。


Known Issues
~~~~~~~~~~~~

MAPDL 2021 R1 存在以下稳定性问题：

* :func:`Mapdl.input() <ansys.mapdl.core.Mapdl.input>` 方法。尽可能避免使用输入文件。
  尝试使用 :func:`Mapdl.upload() <ansys.mapdl.core.Mapdl.upload>` 方法上传节点和单元，并通过 :func:`Mapdl.nread() <ansys.mapdl.core.Mapdl.nread>` 和 :func:`Mapdl.eread() <ansys.mapdl.core.Mapdl.eread>` 方法读取它们。


More help needed?
-----------------

.. vale off

.. epigraph::

   *“如果问题未在此处列出，我该怎么办？”*

.. vale on

要查看您的问题是否已经发布，请搜索 `PyMAPDL Issues <pymapdl_issues_>`_ 页面。如果没有，请执行以下操作之一：

* 如果您不确定原因，或者希望得到有关函数用法或其文档的解释，请在 `PyMAPDL 讨论页面 <pymapdl_discussions_>`_ 上创建讨论。

* 如果你认为发现了一个错误或想创建一个功能请求，请在 `PyMAPDL Issues <pymapdl_issues_>`_ 页面上创建一个问题。

有关更复杂的问题或查询，请联系 `PyAnsys 核心团队 <pyansys_core_>`_ 。

