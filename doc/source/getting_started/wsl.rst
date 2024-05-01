.. _ref_guide_wsl:

###########################
Windows Subsystem for Linux
###########################

本页介绍如何在 Windows Subsystem for Linux (WSL) 中使用 PyAnsys 库，更具体地说是 PyMAPDL。WSL 是在 Windows 10、Windows 11 和 Windows Server 2019 上原生运行 Linux 二进制可执行文件的兼容性层。更多信息，请参阅：

- `Wikipedia WSL <WikipediaWSL_>`_
- Microsoft's `What is the Windows Subsystem for Linux <What_is_the_Windows_Subsystem_for_Linux_>`_.

本页将指导您在 Windows 上安装 WSL，然后展示如何将其与 MAPDL、PyMAPDL 和 `Docker <https://www.docker.com/>`_ 结合使用。

.. note::
   由于 WSL 仍在不断开发中，因此很难随时更新本指南。如果您发现任何问题或有与 WSL 相关的疑问，请随时在 `GitHub 存储库 <pymapdl_issues_>`_ 中提交问题。


Install WSL
###########

WSL 有两个版本： WSL1 和 WSL2。由于 WSL2 比 WSL1 有了许多改进，因此您应该升级到并使用 WSL2。

按照 Microsoft 的说明安装 WSL ，请访问 `Microsoft: Install WSL <install_wsl_microsoft_>`_ 。


Install the CentOS7 WSL distribution
====================================

使用 PyAnsys 库时，应使用 CentOS7 WSL 发行版。

您可以使用 `CentOS-WSL <gh_centos_wsl_1_>`_ 包或 `CentOS WSL <gh_centos_wsl_2_>`_ 包中的非官方 WSL 发行版安装该发行版。


.. vale off

Using the Ubuntu WSL distribution
=================================

.. vale on

Ubuntu 是 Ansys 产品支持的操作系统。但尚未在 WSL 环境中对其进行测试。请谨慎使用。


Install Ansys products in WSL
#############################

Prerequisites
=============
如果使用的是 CentOS 7 ，在安装 MAPDL 之前，必须先安装一些必需的库：

.. code:: console
   
   sudo yum install openssl openssh-clients mesa-libGL mesa-libGLU motif libgfortran


如果使用的是 Ubuntu ，请按照 `Run MAPDL: Ubuntu <pymapdl_run_ubuntu_>`_ 中的说明操作。

.. _installing_ansys_in_wsl:

Install Ansys products
======================

要在 WSL Linux 中安装 Ansys 产品，请执行以下步骤：

1. 从客户门户下载 **Ansys Structures** 映像（ `Current Release <ansys_current_release_>`_ ）。
   
   如果在 Windows 机器上下载镜像，则应随后将镜像从下载文件夹复制到 WSL。

2. 使用此命令解压缩源代码文件（ ``tar.gz`` ）：

   .. code:: console
   
       tar xvzf STRUCTURES_2021R2_LINX64.tgz


3. 要安装 MAPDL，请进入解压文件所在的文件夹并运行此命令：

   .. code:: console
   
      sudo ./INSTALL -silent -install_dir /usr/ansys_inc/ -mechapdl

   where: 

   - ``-silent`` : 启动静默安装，即不显示图形用户界面。
   - ``-install_dir /path/`` : 指定产品或许可证管理器的安装目录。如果要安装到默认位置，可以省略 ``-install_dir`` 参数。如果设置了符号链接，默认位置为 ``/ansys_inc``。否则，默认位置为 ``/usr/ansys_inc``。
   - ``-<product_flag>`` : 指定要安装的一个或多个产品。
     如果省略该参数，则会安装所有产品。The *Ansys, Inc.
     Installation Guides* in the Ansys Help provides a list of valid
     values for the ``product_flags`` argument in `Chapter 6
     <https://ansyshelp.ansys.com/account/secured?returnurl=/Views/Secured/corp/v231/en/installation/unix_silent.html>`_
     of the *Linux Installation Guide* and `Chapter 7
     <https://ansyshelp.ansys.com/account/secured?returnurl=/Views/Secured/corp/v231/en/installation/win_silent.html>`_
     of the *Windows Installation Guide*.
     
     在前面的 MAPDL 示例中，只需指定 ``-mechapdl`` 标记。


直接在 ``/ansys_inc`` 或 ``/usr/ansys_inc`` 中安装 MAPDL 后，使用此命令创建一个符号链接：

.. code:: console

   sudo ln -s /usr/ansys_inc /ansys_inc

默认情况下，PyMAPDL 希望 MAPDL 可执行文件位于 ``/usr/ansys_inc`` 中。无论安装与否，都应该使用符号链接将该目录与 Ansys 安装目录 (`/*/ansys_inc``)关联起来。


安装后的设置
#######################

开放许可证服务器通信端口
===========================================

**理论上：** 您应在 **Windows 控制面板** 中为许可证服务器通信打开端口 ``1055`` 和 ``2325`` 。有关设置高级 Windows 防火墙选项的步骤，请参阅 Microsoft 的 `如何在 Windows 10 防火墙中打开端口 <open_port_windows_10_>`_ 。


**事实上：** 如果您想使用 WSL Linux 映像来运行 Docker 映像，并托管该 Docker 映像，则此方法可行。如果在打开这些端口的情况下运行 Docker 镜像时使用了 ``'-p'`` 标志， Docker 镜像就会使用这些端口与 Windows 许可服务器成功通信。

如果要在 CentOS 7 映像中运行 MAPDL 并使用 Windows 许可服务器，打开端口可能无法正常工作，因为 Windows 防火墙似乎会阻止来自 WSL 的所有流量。
出于安全考虑，您仍应尝试在防火墙中打开端口 ``1055`` 和 ``2325`` 并验证 MAPDL 安装是否可以与 Windows 主机通信。如果设置防火墙规则后仍有问题，
可能需要关闭 WSL 以太网虚拟接口的 Windows 防火墙。这可能会带来一些未知的副作用和安全风险，请谨慎使用。
有关详细信息，请参阅 :ref:`Disable firewall on WSL ethernet <disable_firewall_on_wsl_ethernet_section>`。


在 WSL 中设置指向 Windows 主机许可证服务器的环境变量
==================================================================================

Windows 主机的 IP 地址会在 WSL ``/etc/hosts`` 文件中的 ``host.docker.internal`` 名称之前给出。

.. note::
   如果未安装 Docker，可能无法使用此 ``host.docker.internal`` 定义。

下面是 WSL ``/etc/hosts`` 文件的示例：

.. vale off

.. code-block:: bash
   :emphasize-lines: 8

   # 该文件由 WSL 自动生成。
   # 要停止自动生成该文件，请在 /etc/wsl.conf 中添加以下条目：
   # [network]
   # generateHosts = false
   127.0.0.1       localhost
   127.0.1.1       AAPDDqVK5WqNLve.win.ansys.com   AAPDDqVK5WqNLve

   192.168.0.12    host.docker.internal
   192.168.0.12    gateway.docker.internal
   127.0.0.1       kubernetes.docker.internal

   # 以下行适用于支持IPv6的主机
   ::1     ip6-localhost ip6-loopback
   fe00::0 ip6-localnet
   ff00::0 ip6-mcastprefix
   ff02::1 ip6-allnodes
   ff02::2 ip6-allrouters


.. vale on

您可以在 WSL ``=/.bashrc`` 文件中添加下几行，以创建包含此 IP 地址的环境变量：

.. vale off

.. _ref_bash_win_ip:

.. vale on

.. code:: console

    winhostIP=$(grep -m 1 host.docker.internal /etc/hosts | awk '{print $1}')
    export ANSYSLMD_LICENSE_FILE=1055@$winhostIP


Launch MAPDL in WSL
###################

要在 WSL 中启动 MAPDL，必须启动 MAPDL 进程。下面是一个示例。

.. code:: console

    /ansys_inc/v222/ansys/bin/ansys222 -grpc

这将启动一个工作目录为当前目录的 MAPDL 实例。如果要更改工作目录，可以使用 ``-dir`` 标志。

.. code:: console

    /ansys_inc/v222/ansys/bin/ansys222 -grpc -dir /tmp/ansys_jobs/myjob


在 Windows 主机操作系统中启动 MAPDL
###################################

您可以使用 Windows 主机操作系统中的 MAPDL 安装程序启动 MAPDL 实例。为此，请运行以下代码：

.. code:: python

   from ansys.mapdl.core import launch_mapdl

   mapdl = launch_mapdl(
       exec_file="/mnt/c/Program Files/ANSYS Inc/v231/ANSYS/bin/winx64/ANSYS231.exe",
   )



如 **许可服务器通信的开放端口** 所述，Windows 主机操作系统和 WSL 通过一个虚拟网络连接，两者拥有不同的 IP 地址。
PyMAPDL 会尽力检测 Windows 主机的 IP 地址。为此，它会解析 WSL 中 ``ip route`` 命令给出的输出。但是，如果发现该 IP 地址不正确，可以像这样指定要连接的 IP 地址：

.. code:: python

   from ansys.mapdl.core import launch_mapdl

   mapdl = launch_mapdl(
       exec_file="/mnt/c/Program Files/ANSYS Inc/v231/ANSYS/bin/winx64/ANSYS231.exe",
       ip="172.23.112.1",
   )

您可能需要完全关闭 Microsoft 防火墙，或至少关闭 WSL 网络连接的防火墙。为此，请遵循 :ref:`Disable firewall on WSL ethernet <disable_firewall_on_wsl_ethernet_section>`。


有关更多信息，请参阅问题 `从 WSL 启动 MAPDL <wsl_launching_mapdl_>`_ 或在 `GitHub 存储库问题 <pymapdl_issues_>`_ 中打开一个新问题。


连接到在 WSL 中运行的 MAPDL 实例
###########################################

要连接到运行 MAPDL 实例的 WSL 实例，需要指定 WSL 实例的 IP 地址：

.. code:: pycon

    >>> from ansys.mapdl.core import Mapdl
    >>> mapdl = Mapdl(ip="127.0.0.1", port=50053)



其他信息
######################

WSL 中的 IP 地址和 Windows 主机
========================================

**理论上：** 您应该能够使用 WSL ``/etc/hosts`` 文件中指定的 IP 地址访问 Windows 主机。该 IP 地址通常为 ``127.0.1.1``。这意味着本地 WSL 的 IP 地址是 ``127.0.0.1``。

**事实上：** 使用 IP 地址 ``127.0.1.1`` 连接 Windows 主机几乎是不可能的。不过，可以在同一个 WSL ``/etc/hosts`` 文件中使用 ``host.docker.internal`` 主机名。这是一个随机分配的 IP 地址，在定义许可证服务器时会出现问题。不过，按照这里提到的方法更新 ``.bashrc`` 文件就可以解决这个问题。

从 WSL 角度看，IP 地址 ``127.0.0.1`` 是 WSL CentOS 的 IP 地址，而 Windows 主机的 IP 地址通常是 ``127.0.1.1``。

Docker 以 WSL 发行版为基础构建 PyMAPDL 镜像。因此，PyMAPDL 运行在 Linux WSL 发行版上，而 WSL 发行版运行在 Windows 主机上。由于 Docker 镜像与 WSL 共享资源，因此它也与 WSL 发行版共享内部 IP 地址。


Ansys installation flags
========================

获得帮助
~~~~~~~~~~~

要获取许可证服务器信息，请使用以下方法之一访问 ``INSTALL`` 文件，然后检查最后几行。

Method 1
--------

.. code:: console

    ./INSTALL --help

Method 2
--------

.. code:: console

    cat ./INSTALL


客户端的许可证服务器信息
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``-licserverinfo`` 参数指定许可证服务器的客户端使用的信息。此参数仅在静默安装（INSTALL）时有效。


单一许可证服务器
---------------------

单个许可证服务器的格式为

.. code:: console

   -licserverinfo LI_port_number:FLEXlm_port_number:hostname

下面是一个示例：

.. code:: console

   ./INSTALL -silent -install_dir /ansys_inc/ -mechapdl -licserverinfo 2325:1055:winhostIP

三台许可证服务器
---------------------

三个许可证服务器的格式为

.. code:: console

   -licserverinfo LI_port_number:FLEXlm_port_number:hostname1,hostname2,hostname3

下面是一个示例：

.. code:: console

   ./INSTALL -silent -install_dir /ansys_inc/ -mechapdl -licserverinfo 2325:1055:abc,def,xyz


安装语言
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

参数 ``-lang`` 指定安装使用的语言。


指定要安装的产品的文件
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

您可以指定一个 ``options`` 文件，列出要安装的产品。这样做时，必须使用 ``-productfile`` 参数指定 ``options`` 文件的完整路径。


.. _disable_firewall_on_wsl_ethernet_section:

禁用 WSL 以太网的防火墙
================================
在 WSL 以太网上禁用防火墙有两种方法。

Method 1
~~~~~~~~

此方法会显示一个通知：

.. code:: pwsh-session

    Set-NetFirewallProfile -DisabledInterfaceAliases "vEthernet (WSL)"

Method 2
~~~~~~~~

此方法不显示通知：

.. code:: pwsh-session

    powershell.exe -Command "Set-NetFirewallProfile -DisabledInterfaceAliases \"vEthernet (WSL)\""


**Reference:** 
The information has been obtained from `WSL Windows Toolbar Launcher repository <WSL_Windows_Toolbar_Launcher_>`_.
More specifically from the *Troubleshooting* section `Firewall rules <disabling_firewall_on_wsl_>`_

Windows 10 上的端口转发
=============================

您可以使用 Windows PowerShell 命令在 Windows 10 上进行端口转发。


WSL 和 Windows 之间的链接端口
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

该命令用于连接 WSL 和 Windows 之间的端口：

.. code:: pwsh-session

    netsh interface portproxy add v4tov4 listenport=1055 listenaddress=0.0.0.0 connectport=1055 connectaddress=XXX.XX.XX.XX


View all forwards
~~~~~~~~~~~~~~~~~

该命令允许您查看所有转发：

.. code:: pwsh-session

    netsh interface portproxy show v4tov4


Delete port forwarding
~~~~~~~~~~~~~~~~~~~~~~

使用此命令可以删除端口转发：

.. code:: pwsh-session

    netsh interface portproxy delete v4tov4 listenport=1055 listenaddres=0.0.0.0 protocol=tcp

Reset Windows network adapters
==============================

您可以使用此代码重置 Windows 网络适配器：

.. code:: pwsh-session

    netsh int ip reset all
    netsh winhttp reset proxy
    ipconfig /flushdns
    netsh winsock reset


Restart the WSL service
=======================

您可以使用此命令重新启动 WSL 服务：

.. code:: pwsh-session

    Get-Service LxssManager | Restart-Service


Stop all processes with a given name
====================================

使用该命令可以停止所有指定名称的进程。

.. code:: pwsh-session

   Get-Process "ANSYS212" | Stop-Process


Install ``xvfb`` in CentOS 7
============================

如果要复制 CI/CD 行为，必须安装 ``xvfb`` 软件包，如以下命令所示。有关详细信息，请参阅 ``.ci`` 文件夹。

.. code:: console

   yum install xorg-x11-server-Xvfb


.. note::
   如果您想复制 CI/CD 行为或在 Docker 容器内进行开发，则应使用 Ubuntu 作为基础操作系统。你可以在 :ref:`ref_make_container` 中找到创建自己的 MAPDL Ubuntu 容器的说明，并在 :ref:`ref_devcontainer` 中找到如何使用它在容器上进行开发的说明。

Notes
=====

- 在 WSL 上运行时，PyMAPDL 只适用于共享内存并行 (SMP)。这就是为什么要加入 ``-smp`` 标志的原因。

- 由于 VPN 和 INTEL MPI 之间存在一些不兼容问题，因此在调用 MAPDL 时应使用标记 ``-mpi msmpi``。本 WSL 指南未针对 VPN 编写，也未在 VPN 上进行测试。如果在连接 Windows 主机、许可证服务器或 MAPDL 实例时遇到问题，请断开 VPN 并重试。
