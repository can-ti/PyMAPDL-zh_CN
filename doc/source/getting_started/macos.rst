.. _ref_pymapdl_and_macos:

=================
PyMAPDL and MacOS
=================

Install PyMAPDL
===============

使用该命令，您可以在满足 PyMAPDL 要求的 MacOS 上正常安装 PyMAPDL：

.. code:: zsh

    pip install ansys-mapdl-core


PyMAPDL 需要连接到 MAPDL 实时实例才能运行，但 MAPDL 与 MacOS 不兼容。

有两种选择：

* **连接远程实例**：您可以按照 :ref:`connect_grpc_madpl_session` 中的说明，连接到运行在 Windows 或 Linux 机器上的远程实例。

* **使用 Docker 在本地启动 MAPDL**：您可以在 MacOS 机器上运行 MAPDL，如 :ref:`launch_mapdl_on_macos` 所示。


.. _launch_mapdl_on_macos:

Launch MAPDL on MacOS
=====================

如果没有 MAPDL Docker 镜像，可以按照 :ref:`ref_make_container` 中的说明在 Linux 机器上创建一个。


如果您已经有一个 MAPDL Docker 镜像，则可以按照 :ref:`run_an_mapdl_image` 中的指示启动 MAPDL。

Apple Silicon compatibility
---------------------------

如果您使用的是 Apple Silicon 设备（例如 M1 或 M2），您可能会看到以下警告：

.. code::  output

    WARNING: The requested image's platform (linux/amd64) does not match the detected host platform (linux/arm64/v8) and no specific platform was requested
    （请求的映像平台（linux/amd64）与检测到的主机平台（linux/arm64/v8）不匹配，且未请求特定平台）

这是因为 Docker 映像尚未构建为在 Apple Silicon 架构 (arm64) 上运行。你必须在 `docker run <docker_run_>`_ 命令中添加 ``--platform linux/amd64`` 参数，如代码示例所示：

.. code:: zsh

    ANSYSLMD_LICENSE_FILE=1055@MY_LICENSE_SERVER_IP
    LOCAL_MAPDL_PORT=50053
    MAPDL_DOCKER_REGISTRY_URL=ghcr.io/myuser/myrepo/mymapdldockerimage
    docker run -e ANSYSLMD_LICENSE_FILE=$ANSYSLMD_LICENSE_FILE --restart always --name mapdl -p $LOCAL_MAPDL_PORT:50052 --platform linux/amd64 $MAPDL_DOCKER_REGISTRY_URL -smp > log.txt


Connect to an MAPDL container
=============================

您可以按照 :ref:`connect_grpc_madpl_session` 中的指示连接到 MAPDL 实例。


