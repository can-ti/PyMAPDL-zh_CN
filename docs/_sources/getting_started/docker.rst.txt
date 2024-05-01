.. _pymapdl_docker:

****************
MAPDL and Docker
****************

您可以在任何操作系统的 Docker 容器中运行 MAPDL，并通过 PyMAPDL 与之连接。

在 Docker（或 Singularity）等容器环境中运行 MAPDL 有几个优势：

- 无论主机操作系统如何，环境始终如一
- 便于携带和安装
- 使用 Kubernetes 进行大规模集群部署
- 通过容器化实现真正的应用程序隔离

在 Docker 容器中运行 MAPDL 时，需要使用本地 Python 安装来连接该实例。


Requirements
============

您必须能够访问包含 MAPDL 的 Docker 镜像。有关如何创建自己的 Docker 镜像的更多信息，请参阅 :ref:`ref_make_container`。

创建 Docker 镜像并将其上传到注册表后，就可以开始在其他设备上提取和使用该镜像了。

.. warning::

   MAPDL Docker 映像不允许在公共或免费访问的存储库或注册表中共享。这样做违反了 Ansys 政策。



配置 Docker 以访问 GitHub 私有注册表
----------------------------------------------------

如果您创建了 Docker 镜像并将其上传到 GitHub 私有仓库，则必须使用个人访问令牌授权您的 Docker 安装来访问该私有软件包。

有关创建具有 ``packages read`` 权限的 GitHub 个人访问令牌的信息，请参阅 GitHub 的 `创建个人访问令牌 <gh_creating_pat_>`_ 。

使用此命令将标记保存到文件中：

.. code::

   echo MY_GITHUB_TOKEN_WITH_PACKAGE_READ_PERMISSION > GH_TOKEN.txt


这样就可以将令牌发送给 Docker，而不会在历史记录中留下令牌值。接下来，用以下代码授权 Docker 访问该版本库：

.. code::

    GH_USERNAME=<my-github-username>
    cat GH_TOKEN.txt | docker login ghcr.io -u $GH_USERNAME --password-stdin


.. _run_an_mapdl_image:

Run an MAPDL Docker image
=========================

现在，你可以使用命令行 `docker compose file <run_an_mapdl_image_using_docker_compose_>`_ 或脚本从 Docker 启动 MAPDL。

您的 Docker 映像应具有有效的 MAPDL 许可证配置。最简单的方法是设置一个环境变量 :envvar:`ANSYSLMD_LICENSE_FILE`，指向一个有效的许可证服务器。
这个环境变量可以包含在 Docker 镜像中。不过，我们不建议这样做，因为如果 Docker 映像泄露，它可能会暴露许可证服务器。建议的做法是在运行容器时设置该环境变量。

要从托管在 ``ghcr.io/myuser/myrepo/mymapdldockerimage`` 的映像实例化 MAPDL Docker 容器，请使用以下示例中的代码。

**On Windows**

.. code:: pwsh-session

    $env:ANSYSLMD_LICENSE_FILE="1055@MY_LICENSE_SERVER_IP"
    $env:LOCAL_MAPDL_PORT=50053
    $env:MAPDL_DOCKER_REGISTRY_URL="ghcr.io/myuser/myrepo/mymapdldockerimage"

    docker run -e ANSYSLMD_LICENSE_FILE=$env:ANSYSLMD_LICENSE_FILE --restart always --name mapdl -p $env:LOCAL_MAPDL_PORT`:50052   $env:MAPDL_DOCKER_REGISTRY_URL -smp


**On Linux**

.. code:: bash

  ANSYSLMD_LICENSE_FILE=1055@MY_LICENSE_SERVER_IP
  LOCAL_MAPDL_PORT=50053
  MAPDL_DOCKER_REGISTRY_URL=ghcr.io/myuser/myrepo/mymapdldockerimage
  docker run -e ANSYSLMD_LICENSE_FILE=$ANSYSLMD_LICENSE_FILE --restart always --name mapdl -p $LOCAL_MAPDL_PORT:50052 $MAPDL_DOCKER_REGISTRY_URL -smp > log.txt


第一次实例化容器时，Docker 会登录注册表并提取所需的映像。这可能需要一些时间，具体取决于映像的大小。

要重新运行，应使用此命令重启容器：

.. code:: bash

   docker start mapdl

或者也可以删除容器，然后使用这些命令重新运行：

.. code:: bash

    docker rm -f mapdl

    docker run -e ANSYSLMD_LICENSE_FILE=$ANSYSLMD_LICENSE_FILE --restart always --name mapdl -p $LOCAL_MAPDL_PORT:50052   $MAPDL_DOCKER_REGISTRY_URL -smp > log.txt


您可以添加 Docker 标志 ``--rm`` 以在退出时自动清理容器。

上述命令会在当前目录下创建一个日志文件 (``log.txt``)。不过，如果不想创建该文件，可以删除 ``> log.txt``。
在这种情况下，命令输出会重定向到控制台，在 Docker 映像退出之前，控制台一直处于阻塞状态。您可以通过在 `docker run <docker_run_>`_ 
命令中添加 ``-d`` 将控制台从 Docker 容器输出中分离出来。（一定要在 Docker 镜像 URL 之前添加）。

如果不想阻塞控制台，最好的办法是将输出导入一个文件，如前所述，这样就可以检查该文件的输出。

请注意，MAPDL Docker 镜像的 gRPC 端口（ ``50052`` ）被映射到了不同的主机端口（ ``50053`` ），以避免与主机或其他 Docker 镜像上运行的本地 MAPDL 实例发生端口冲突。
如果要同时运行多个模拟，还可以在不同端口启动更多 Docker 容器。

当连接到远程 MAPDL Docker 镜像时，:ref:`ref_pymapdl_pool` 模块不起作用。当连接到 Docker 容器时，该模块也不起作用。如果决定启动多个 MAPDL 实例，则必须自行管理这些实例。

.. note:: 确保本地防火墙中的端口 ``50053`` 是开放的。

您可以向 MAPDL 提供额外的 MAPDL 命令行参数，只需将其附加到命令末尾即可。

例如，可以使用 ``-np`` 开关增加处理器数量（最多不超过主机上的可用数量）：

.. code:: bash

  docker run -e ANSYSLMD_LICENSE_FILE=$ANSYSLMD_LICENSE_FILE --restart always -d --name mapdl -p $LOCAL_MAPDL_PORT:50052 $MAPDL_DOCKER_REGISTRY_URL -smp -np 8 > log.txt


有关其他命令行参数，请参阅 :func:`launch_mapdl() <ansys.mapdl.core.launcher.launch_mapdl>` 函数说明中的 *Notes* 部分。

您可以使用脚本文件（batch ``".bat"`` 或 PowerShell ``".ps"`` ）一次性运行前面的命令。

启动 MAPDL 后，您应该会在控制台（或输出文件）中看到以下内容：

.. code::

    Start GRPC Server

    ##############################
    ### START GRPC SERVER      ###
    ##############################

    Server Executable   : MapdlGrpc Server
    Server listening on : 0.0.0.0:50052


.. note:: 
  
   请注意，控制台中指定的端口是 Docker 容器的内部端口。该端口已被映射到 :envvar:`LOCAL_MAPDL_PORT` 环境变量指定的值。


.. _run_an_mapdl_image_using_docker_compose:

Using ``docker-compose`` to launch MAPDL
----------------------------------------

你也可以使用 ``docker-compose`` 命令来启动配置在 ``docker-compose`` 文件中的 MAPDL。如果你想加载已经配置好的环境，或者想启动多个 MAPDL 或服务实例，这将非常有用。

为方便起见， `docker <pymapdl_docker_dir_>`_ 目录包含了配置好的 ``docker-compose`` 文件，你可以使用这些文件。

建议使用 `docker-compose.yml <pymapdl_docker_compose_base_>`_ 文件。这是用于启动可远程连接的 MAPDL 实例的 *base* 配置文件。


.. _pymapdl_connect_to_MAPDL_container:

Connect to the MAPDL container from Python
==========================================

您可以按照 :ref:`connect_grpc_madpl_session` 中的指示连接到 MAPDL 实例。您无需指定 IP 地址，因为 Docker 会将端口映射到本地主机。


其他注意事项
=========================

Use ``--restart`` policy with MAPDL products
--------------------------------------------

默认情况下，MAPDL 启动时会在工作目录中创建一个 ``LOCK`` 文件，正常退出时会删除该文件。在异常终止后启动 MAPDL 时，该文件用于避免覆盖数据库 (DB) 文件或结果 (RST) 文件等文件。

由于这种行为，当在 `docker run <docker_run_>`_ 命令中使用 Docker ``--restart`` 标志时，如果指定在异常终止后重新启动 Docker 映像，
可能会在崩溃后进入无限循环。当出现异常终止（MAPDL 崩溃）时，工作目录中会保留 :file:`LOCK` 文件。由于 MAPDL 已退出，因此容器也会退出。

这将触发 Docker ``restart`` 策略，该策略会尝试重新启动 MAPDL 容器和 MAPDL 进程。但由于存在 ``LOCK`` 文件，MAPDL 会退出，以避免覆盖上次崩溃的文件。这是一个无限循环的开始，Docker 会不断重启 MAPDL 容器，而 MAPDL 会不断退出以避免覆盖之前的文件。

在这种情况下，不应使用 ``--restart`` 选项。如果确实需要使用该选项，可以避免 MAPDL 检查，并通过将 ``ANSYS_LOCK`` 环境变量设置为 ``"OFF"`` 来启动进程，从而创建 ``LOCK`` 文件。

这段代码展示了如何在 `docker run <docker_run_>`_ 命令中实现这一点：

.. code:: bash

  docker run \
      --restart always \
      -e ANSYSLMD_LICENSE_FILE=1055@$LICENSE_SERVER \
      -e ANSYS_LOCK="OFF" \
      -p 50052:50052 \
      $IMAGE


异常终止后获取有用文件
-------------------------------------------

在某些情况下，MAPDL 容器可能会在 MAPDL 进程异常终止后崩溃。在这种情况下，您可以使用 Docker 提供的工具检索日志文件和输出文件。

首先，获取 Docker 容器名称：

.. code:: pwsh-session

  PS docker ps -a
  CONTAINER ID   IMAGE                                   COMMAND                  CREATED          STATUS          PORTS                      NAMES
  c14560bff70f   my.registry/myuser/mypackage/mapdl   "/ansys_inc/ansys/bi…"   9 seconds ago    Exited(137)    0.0.0.0:50053->50052/tcp   mapdl


然后使用该命令中的 ``name``：

.. code:: pwsh-session

  PS docker exec -it mapdl /bin/bash

该命令执行容器的命令 shell (``/bin/bash``)，并将您的当前终端连接到它（交互式 ``-it`` ）。

.. code:: pwsh-session

  PS C:\Users\user> docker exec -it mapdl /bin/bash
  [root@c14560bff70f /]#

现在，你可以在 Docker 容器中输入命令，并在其中导航。

.. code:: pwsh-session

  PS C:\Users\user> docker exec -it mapdl /bin/bash
  [root@c14560bff70f /]# ls
  anaconda-post.log  cleanup-ansys-c14560bff70f-709.sh  file0.err   file1.err  file1.page  file2.out   file3.log   home   media  proc  sbin  tmp
  ansys_inc          dev                                file0.log   file1.log  file2.err   file2.page  file3.out   lib    mnt    root  srv   usr
  bin                etc                                file0.page  file1.out  file2.log   file3.err   file3.page  lib64  opt    run   sys   var

然后，您可以记下要检索的文件。例如，您可能希望检索错误文件和输出文件（ ``file*.err`` 和 ``file*.out`` ）。

使用 ``exit`` 命令退出容器终端：

.. code:: pwsh-session

  [root@c14560bff70f /]# exit
  exit
  (base) PS C:\Users\user>

然后，你就可以使用 `docker cp <docker_cp_>`_ 命令复制注意到的文件：

.. code:: pwsh-session

  docker cp mapdl:/file0.err .

该命令复制当前目录下的文件。您可以使用第二个参数指定不同的目的。

如果要检索多个文件，最有效的方法是回到 Docker 容器内部：

.. code:: pwsh-session

  PS C:\Users\user> docker exec -it mapdl /bin/bash
  [root@c14560bff70f /]#

创建一个文件夹，在其中复制所有需要的文件：

.. code:: pwsh-session

  [root@c14560bff70f /]# mkdir -p /mapdl_logs
  [root@c14560bff70f /]# cp -f /file*.out /mapdl_logs
  [root@c14560bff70f /]# cp -f /file*.err /mapdl_logs
  [root@c14560bff70f /]# ls mapdl_logs/
  file0.err  file1.err  file1.out  file2.err  file2.out  file3.err  file3.out

然后一次性复制整个文件夹的内容：

.. code:: pwsh-session

  docker cp mapdl:/mapdl_logs/. .

