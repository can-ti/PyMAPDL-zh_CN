launch_mapdl
==============

.. py:function:: ff_ansys.mapdl.core.launcher.launch_mapdl(exec_file=None, run_location=None, jobname='file', nproc=2, ram=None, mode=None, override=False, loglevel='ERROR', additional_switches='', start_timeout=45, port=None, cleanup_on_exit=True, start_instance=None, ip=None, clear_on_connect=True, log_apdl=None, remove_temp_files=None, remove_temp_dir_on_exit=False, verbose_mapdl=None, license_server_check=True, license_type=None, pr:class:`int`_com=False, add_env_vars=None, replace_env_vars=None, version=None, **kwargs)

    在本地启动 MAPDL。

    :Parameters:

        exec_file : :class:`str`, :class:`optional`
            MAPDL 可执行文件的位置。当默认设置为 ``None`` 且未设置环境变量时，将使用缓存位置。

            .. note::
                也可通过环境变量 ``PYMAPDL_MAPDL_EXEC`` 设置可执行路径。例如:

                .. code:: console

                    export PYMAPDL_MAPDL_EXEC=/ansys_inc/v211/ansys/bin/mapdl

        run_location : :class:`str`, :class:`optional`
            MAPDL 工作目录。默认为临时工作目录。如果目录不存在，则会创建一个。

        jobname : :class:`str`, :class:`optional`
            MAPDL jobname. 默认为 ``'file'`` 。

        nproc : :class:`int`, :class:`optional`
            处理器数量。默认为 2。

        ram : :class:`float`, :class:`optional`
            为 MAPDL 申请的固定内存量。如果为 ``None`` ，则 MAPDL 将使用主机上的可用内存。

        mode : :class:`str`, :class:`optional`
            启动 MAPDL 的模式。必须是以下之一:

            - ``'grpc'``: ``'grpc'`` 模式在 ANSYS 2021R1 或更新版本上可用，具有最佳性能和稳定性。
            - ``'console'``: ``'console'`` 模式仅用于 v17.0 之前的旧版 Linux。该控制台模式将会被启用。更多信息，请访问 :ref:`versions_and_interfaces` 。

        override : :class:`bool`, :class:`optional`
            尝试删除 ``run_location`` 处的锁定文件。若当之前的 MAPDL 会话过早退出，而锁定文件尚未删除时，此功能非常有用。

        loglevel : :class:`str`, :class:`optional`
            设置打印到控制台的信息。 ``'INFO'`` 打印所有 ANSYS 信息， ``'WARNING'`` 只打印包含 ANSYS 警告的信息， ``'ERROR'`` 只记录错误信息。

        additional_switches : :class:`str`, :class:`optional`
            MAPDL 其他开关，例如 ``'aa_r'`` ，学术研究许可证：

            - ``additional_switches="-aa_r"``

            避免添加 ``-i`` 、 ``-o`` 或 ``-b`` 等开关，因为启动 MAPDL 服务器时已包含这些开关。更多详情，请参阅注释部分。

        start_timeout : :class:`float`, :class:`optional`
            连接 MAPDL 服务器的最长允许时间。

        port : :class:`int`
            启动 MAPDL gRPC 的端口。最终端口将是该端口之后（或包括该端口）的第一个可用端口。默认为 50052。您也可以使用环境变量 ``PYMAPDL_PORT=<VALID PORT>`` 来覆盖默认端口，该参数的优先级高于环境变量。

        cleanup_on_exit : :class:`bool`, :class:`optional`
            当 python 退出或 mapdl Python 实例被垃圾回收时，退出 MAPDL。

        start_instance : :class:`bool`, :class:`optional`
            当为 ``False`` 时，通过 ``ip`` 和 ``port`` 连接到现有的 MAPDL 实例，
            默认为 ip ``'127.0.0.1'`` 和端口 50052。否则，启动本地 MAPDL 实例。
            您也可以使用环境变量 ``PYMAPDL_START_INSTANCE=FALSE`` 来覆盖此关键字参数的默认行为。

        ip : :class:`bool`, :class:`optional`
            仅当 ``start_instance`` 为 ``False`` 时使用。如果提供，它将强制 ``start_instance`` 为 ``False`` 。指定要连接的 MAPDL 实例的 IP 地址。
            您也可以提供主机名来替代 IP 地址。默认值为 ``'127.0.0.1'`` 。您也可以使用环境变量 ``PYMAPDL_IP=<IP>`` 来覆盖此关键字参数的默认行为。
            该参数的优先级高于环境变量。

        clear_on_connect : :class:`bool`, :class:`optional`
            默认为 ``True`` ，这样在连接到 MAPDL 时会有一个全新的环境。如果指定了 ``start_instance`` ，则默认为 ``False`` 。

        log_apdl : :class:`str`, :class:`optional`
            若启用会将每一条 APDL 命令记录到本地磁盘。这可以用来 "record" 通过 PyMAPDL 发送到 MAPDL 的所有命令，这样就可以在 MAPDL 中运行脚本，而无需 PyMAPDL。
            该参数是输出文件的路径（例如 ``log_apdl='pymapdl_log.txt'`` ）。默认情况下禁用。

        remove_temp_files : :class:`bool`, :class:`optional`
            当 ``run_location`` 为 ``None`` 时，启动器会在用户临时目录中创建一个新的 MAPDL 工作目录，该目录可通过 ``tempfile.gettempdir()`` 获取。
            当此参数为 ``True`` 时，退出 MAPDL 时将删除此目录。默认为 ``False`` 。

            .. deprecated:: 0.64.0
               请改用参数 ``remove_temp_dir_on_exit`` 。

        remove_temp_dir_on_exit : :class:`bool`, :class:`optional`
            当 ``run_location`` 为 None 时，启动器会在用户临时目录中创建一个新的 MAPDL 工作目录，该目录可通过 ``tempfile.gettempdir()`` 获取。
            当此参数为 ``True`` 时，退出 MAPDL 时将删除此目录。默认为 ``False`` 。
            如果更改了工作目录，PyMAPDL 不会删除原来的工作目录，也不会删除新的工作目录。

        verbose_mapdl : :class:`bool`, :class:`optional`
            启动和运行 MAPDL 时，启用打印所有输出。这只能用于调试，因为输出可以在 pymapdl 中跟踪。默认为 ``False`` 。

            .. deprecated:: v0.65.0
                ``verbose_mapdl`` 参数已被弃用，将在今后的版本中删除。请使用日志记录器代替。详情参见 :ref:`api_logging_ff` 。

        license_server_check : :class:`bool`, :class:`optional`
            如果 MAPDL 启动失败，检查许可证服务器是否可用。仅适用于 ``mode='grpc'`` 。默认为 ``True`` 。

        license_type : :class:`str`, :class:`optional`
            启用许可证类型选择。可以输入一个字符串作为许可证名称（例如 ``meba`` 或 ``ansys`` ）或描述（分别为 "企业求解器" 或 "企业"）。
            您也可以使用旧版许可证（例如 ``'aa_t_a'`` ），但也会引发警告。
            如果未使用 (``None``)，则不会请求特定许可证，而是由许可证服务器提供特定许可证类型。默认为 ``None`` 。

        print_com : :class:`bool`, :class:`optional`
            将命令 ``/COM`` 参数打印到标准输出。默认为 ``False`` 。（这个 ``/COM`` 命令是 APDL 里用来注释的。--ff）

        add_env_vars : :class:`dict`, :class:`optional`
            所提供的字典将用于扩展 MAPDL 进程环境变量。
            如果要控制所有环境变量，请使用参数 ``replace_env_vars`` 。默认为 ``None`` 。

        replace_env_vars : :class:`dict`, :class:`optional`
            所提供的字典将用于替换所有 MAPDL 进程环境变量。
            它将替换系统环境变量，否则将在过程中使用这些变量。
            要在 MAPDL 进程中添加一些环境变量，请使用 ``add_env_vars`` 。默认为 ``None`` 。

        version : :class:`float`, :class:`optional`
            要启动的 MAPDL 版本。如果 ``None`` ，则使用最新版本。版本可以是整数（如 ``version=222`` ）或浮点数（如 ``version=22.2`` ）。
            要检索可用的已安装版本，请使用函数 ``ansys.tools.path.path.get_available_ansys_installations()`` 。

            .. note::
                默认版本也可通过环境变量 ``PYMAPDL_MAPDL_VERSION`` 设置。例如：

                .. code:: console

                    export PYMAPDL_MAPDL_VERSION=22.2

        \**kwargs : :class:`dict`, :class:`optional`
            这些关键字参数针对特定界面或用于开发目的。详情请参阅注释。

            set_no_abort : :class:`bool`

            *(Development use only)*
            （仅限开发使用）设置 MAPDL 在 /BATCH 模式下第一次出错时不会终止。默认为 ``True`` 。

            force_intel : :class:`bool`

            *(Development use only)*
            （仅限开发使用）在 Ansys 2021R0 和 2022R2 之间的版本中强制使用英特尔消息传递接口 (MPI)，由于 VPN 问题，默认情况下 MPI 已停用。
            更多信息，请参阅 :ref:`vpn_issues_troubleshooting` 。默认为 ``False`` 。

            log_broadcast : :class:`bool`

            *(Only for CORBA mode)*
            启用 logger 记录广播命令。默认为 ``False`` 。

    :Returns:

        ``Union`` [ ``MapdlGrpc`` , ``MapdlConsole`` , ``MapdlCorba`` ]
            Mapdl 的一个实例。类型取决于所选的 ``mode`` 。

    :Notes:

        **Ansys Student Version**
            如果检测到 Ansys Student 版本，除非指定其他选项，否则 PyMAPDL 将以共享内存并行（SMP）模式启动 MAPDL。

        **Additional switches**
            这些是 2020R2 中适用于通过 gRPC 将 MAPDL 作为服务运行的 MAPDL 开关选项。排除在外的开关，如 ``"-j"``，要么不适用，要么通过关键字参数设置。

        \-acc <device>
            启用 GPU 硬件。更多信息，请参阅《并行处理指南》中的 GPU 加速器功能。

        \-amfg
            启用快速成型制造功能。需要获得快速成型制造许可证。有关此功能的一般信息，请参阅 ANSYS Workbench 中的增材制造过程仿真。

        \-ansexe <executable>
            激活自定义 MAPDL 可执行文件。在 ANSYS 工作台环境中，激活自定义 MAPDL 可执行文件。

        \-custom <executable>
            调用定制的 Mechanical APDL 可执行文件 更多信息，请参阅《程序员参考手册》中的 "运行您的定制可执行文件"。

        \-db value
            初始内存分配

            定义用作数据库初始分配的工作区（内存）部分。默认值为 1024 MB。指定一个负数可在整个运行过程中强制使用固定大小；在小内存系统中非常有用。

        \-dis
            启用分布式 ANSYS

            更多信息，请参阅《并行处理指南》。

        \-dvt
            启用 ANSYS DesignXplorer 高级任务（附加组件）。
            需要 DesignXplorer。

        \-l <language>
            指定使用英语以外的语言文件

            只有在 ``/ansys_inc/v201/ansys/docu`` 或 ``Program Files\\ANSYS\Inc\V201\ANSYS\\docu`` 中适当命名的子目录下有翻译的信息文件时，该选项才有效。

        \-m <workspace>
            指定工作区的总大小

            用于初始分配的工作区（内存），单位为 MB。如果省略 ``-m`` 选项，默认值为 2 GB（2048 MB）。指定负数可强制在整个运行过程中使用固定大小。

        \-machines <IP>
            指定分布式计算机

            运行分布式 ANSYS 分析的机器。有关详细信息，请参阅并行处理指南中的启动分布式 ANSYS。

        \-mpi <value>
            指定要使用的 MPI 类型。

            更多信息，请参阅《并行处理指南》。

        \-mpifile <appfile>
            指定现有的 MPI 文件

            指定要在分布式 ANSYS 运行中使用的现有 MPI 文件（appfile）。有关详细信息，请参阅并行处理指南中的使用 MPI 文件。

        \-na <value>
            指定 GPU 加速设备的数量

            使用 GPU 加速器功能运行时，每台机器或计算节点的 GPU 设备数量。更多信息，请参阅《并行处理指南》中的 GPU 加速器功能。

        \-name <value>
            定义 MAPDL 参数

            在程序启动时设置 MAPDL 参数。参数名称长度至少为两个字符。有关参数的详细信息，请参阅《ANSYS 参数化设计语言指南》。

        \-p <productname>
            ANSYS 会话产品

            定义会话期间将运行的 ANSYS 会话产品。有关 ``-p`` 选项的详细信息，请参阅通过命令行选择 ANSYS 产品。

        \-ppf <license feature name>
            HPC（高性能计算） 许可证

            指定并行处理运行时使用的 HPC 许可。有关详细信息，请参阅《并行处理指南》中的 HPC 许可。

        \-smp
            启用共享内存并行。

            更多信息，请参阅《并行处理指南》。

        如果环境配置为使用 `PyPIM <https://pypim.docs.pyansys.com>`_ 且 ``start_instance`` 为 ``True``，那么启动实例将委托给 PyPIM。在这种情况下，大部分选项将被忽略，服务器端配置将被使用。



    :Examples:

        使用最佳协议启动 MAPDL。

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()

        使用共享内存并行运行 MAPDL，并指定 Ansys 二进制文件的位置。

        >>> exec_file = 'C:/Program Files/ANSYS Inc/v231/ansys/bin/winx64/ANSYS231.exe'
        >>> mapdl = launch_mapdl(exec_file, additional_switches='-smp')

        连接到 IP 地址为 192.168.1.30、端口为 50001 的现有 MAPDL 实例。这只能使用最新的 ``'grpc'`` 模式。

        >>> mapdl = launch_mapdl(start_instance=False, ip='192.168.1.30',
        ...                      port=50001)

        使用控制台模式运行 MAPDL（不建议使用，仅适用于 Linux）。

        >>> mapdl = launch_mapdl('/ansys_inc/v194/ansys/bin/ansys194',
        ...                       mode='console')

        使用附加环境变量运行 MAPDL。

        >>> my_env_vars = {"my_var":"true", "ANSYS_LOCK":"FALSE"}
        >>> mapdl = launch_mapdl(add_env_vars=my_env_vars)

        使用我们自己的环境变量集运行 MAPDL。它取代了系统环境变量，否则系统环境变量会在运行过程中使用。

        >>> my_env_vars = {"my_var":"true",
            "ANSYS_LOCK":"FALSE",
            "ANSYSLMD_LICENSE_FILE":"1055@MYSERVER"}
        >>> mapdl = launch_mapdl(replace_env_vars=my_env_vars)