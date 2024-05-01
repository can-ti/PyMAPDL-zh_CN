
.. _ref_cli:

==============================
PyMAPDL command line interface
==============================

为方便起见，PyMAPDL 软件包包含一个命令行界面，允许您启动、停止和列出本地 MAPDL 实例。

.. note::
   使用该 cmd 命令需要 PyMAPDL ≥ v0.68。


Launch MAPDL instances
======================

要启动 MAPDL，只需在已激活的虚拟环境中键入即可：


.. tab-set::

    .. tab-item:: Windows

        .. code:: pwsh-session

            (.venv) PS C:\Users\user\pymapdl> launch_mapdl
            Success: Launched an MAPDL instance (PID=23644) at 127.0.0.1:50052

    .. tab-item:: Linux

                
        .. code:: console

            (.venv) user@machine:~$ launch_mapdl
            Success: Launched an MAPDL instance (PID=23644) at 127.0.0.1:50052

如果要指定参数，例如端口，则需要调用 `launch_mapdl start` ：


.. tab-set::

    .. tab-item:: Windows

        .. code:: pwsh-session

            (.venv) PS C:\Users\user\pymapdl> launch_mapdl start --port 50054
            Success: Launched an MAPDL instance (PID=18238) at 127.0.0.1:50054

    .. tab-item:: Linux

                
        .. code:: console

            (.venv) user@machine:~$ launch_mapdl start --port 50054
            Success: Launched an MAPDL instance (PID=18238) at 127.0.0.1:50054


这个命令 `launch_mapdl start` 的目的是复制函数 :func:`ansys.mapdl.core.launchcher.launch_mapdl`，因此你可以使用这个函数允许的一些参数。例如，可以指定工作目录：

.. tab-set::

    .. tab-item:: Windows


        .. code:: pwsh-session

            (.venv) PS C:\Users\user\pymapdl> launch_mapdl start --run_location C:\Users\user\temp\    
            Success: Launched an MAPDL instance (PID=32612) at 127.0.0.1:50052

    .. tab-item:: Linux

                
        .. code:: console

            (.venv) user@machine:~$ launch_mapdl start --run_location /home/user/tmp    
            Success: Launched an MAPDL instance (PID=32612) at 127.0.0.1:50052


有关更多信息，请参阅 :func:`ansys.mapdl.core.launcher.launch_mapdl` 和 :func:`ansys.mapdl.core.cli.launch_mapdl` 。


Stop MAPDL instances
====================

可以通过使用 `launch_mapdl stop` 命令以下列方式停止 MAPDL 实例：


.. tab-set::

    .. tab-item:: Windows


        .. code:: pwsh-session

            (.venv) PS C:\Users\user\pymapdl> launch_mapdl stop
            Success: Ansys instances running on port 50052 have been stopped.

    .. tab-item:: Linux

                
        .. code:: console

            (.venv) user@machine:~$ launch_mapdl stop
            Success: Ansys instances running on port 50052 have been stopped.


默认情况下，在端口 `50052` 上运行的实例会被停止。

您可以使用 `--port` 参数指定在不同端口上运行的实例：


.. tab-set::

    .. tab-item:: Windows


        .. code:: pwsh-session

            (.venv) PS C:\Users\user\pymapdl> launch_mapdl stop --port 50053
            Success: Ansys instances running on port 50053 have been stopped.

    .. tab-item:: Linux

                
        .. code:: console

            (.venv) user@machine:~$ launch_mapdl stop --port 50053
            Success: Ansys instances running on port 50053 have been stopped.


或具有给定进程 ID (PID) 的实例：


.. tab-set::

    .. tab-item:: Windows


        .. code:: pwsh-session

            (.venv) PS C:\Users\user\pymapdl> launch_mapdl stop --pid 40952
            Success: The process with PID 40952 and its children have been stopped.

    .. tab-item:: Linux

                
        .. code:: console

            (.venv) user@machine:~$ launch_mapdl stop --pid 40952
            Success: The process with PID 40952 and its children have been stopped.


或者，可以使用以下命令停止所有正在运行的实例：


.. tab-set::

    .. tab-item:: Windows


        .. code:: pwsh-session

            (.venv) PS C:\Users\user\pymapdl> launch_mapdl stop --all      
            Success: Ansys instances have been stopped.

    .. tab-item:: Linux

                
        .. code:: console

            (.venv) user@machine:~$ launch_mapdl stop --all      
            Success: Ansys instances have been stopped.


List MAPDL instances and processes
==================================

您还可以列出 MAPDL 实例和进程。如果要列出 MAPDL 进程，只需使用以下命令：

.. tab-set::

    .. tab-item:: Windows


        .. code:: pwsh-session

            (.venv) PS C:\Users\user\pymapdl> launch_mapdl list
            Name          Is Instance    Status      gRPC port    PID
            ------------  -------------  --------  -----------  -----
            ANSYS.exe     False          running         50052  35360
            ANSYS.exe     False          running         50052  37116
            ANSYS222.exe  True           running         50052  41644

    .. tab-item:: Linux

                
        .. code:: console

            (.venv) user@machine:~$ launch_mapdl list
            Name          Is Instance    Status      gRPC port    PID
            ------------  -------------  --------  -----------  -----
            ANSYS.exe     False          running         50052  35360
            ANSYS.exe     False          running         50052  37116
            ANSYS222.exe  True           running         50052  41644


如果只想列出实例（避免列出子 MAPDL 进程），只需键入

.. tab-set::

    .. tab-item:: Windows


        .. code:: pwsh-session

            (.venv) PS C:\Users\user\pymapdl> launch_mapdl list -i
            Name          Status      gRPC port    PID
            ------------  --------  -----------  -----
            ANSYS222.exe  running         50052  41644

    .. tab-item:: Linux

                
        .. code:: console

            (.venv) user@machine:~$ launch_mapdl list -i
            Name          Status      gRPC port    PID
            ------------  --------  -----------  -----
            ANSYS222.exe  running         50052  41644


还可以打印其他字段，如工作目录（使用 `-cwd` ）或命令行（使用 `-c` ）。
此外，还可以使用参数 `--long` 或 `-l` 打印所有可用信息：

.. tab-set::

    .. tab-item:: Windows


        .. code:: pwsh-session

            (.venv) PS C:\Users\user\pymapdl> launch_mapdl list -l
            Name          Is Instance    Status      gRPC port    PID  Command line                                                                                                                      Working directory
            ------------  -------------  --------  -----------  -----  --------------------------------------------------------------------------------------------------------------------------------  ---------------------------------------------------
            ANSYS.exe     False          running         50052  35360  C:\Program Files\ANSYS Inc\v222\ANSYS\bin\winx64\ANSYS.EXE -j file -b -i .__tmp__.inp -o .__tmp__.out -port 50052 -grpc           C:\Users\User\AppData\Local\Temp\ansys_ahmfaliakp
            ANSYS.exe     False          running         50052  37116  C:\Program Files\ANSYS Inc\v222\ANSYS\bin\winx64\ANSYS.EXE -j file -b -i .__tmp__.inp -o .__tmp__.out -port 50052 -grpc           C:\Users\User\AppData\Local\Temp\ansys_ahmfaliakp
            ANSYS222.exe  True           running         50052  41644  C:\Program Files\ANSYS Inc\v222\ansys\bin\winx64\ansys222.exe -j file -np 2 -b -i .__tmp__.inp -o .__tmp__.out -port 50052 -grpc  C:\Users\User\AppData\Local\Temp\ansys_ahmfaliakp

    .. tab-item:: Linux

                
        .. code:: console

            (.venv) user@machine:~$ launch_mapdl list -l
            Name          Is Instance    Status      gRPC port    PID  Command line                                                               Working directory
            ------------  -------------  --------  -----------  -----  -------------------------------------------------------------------------  --------------------------------
            ANSYS         False          running         50052  35360  /ansys_inc/v222/ansys/bin/linx64/ansys -j file -port 50052 -grpc           /home/user/temp/ansys_ahmfaliakp
            ANSYS         False          running         50052  37116  /ansys_inc/v222/ansys/bin/linx64/ansys -j file -port 50052 -grpc           /home/user/temp/ansys_ahmfaliakp
            ANSYS222      True           running         50052  41644  /ansys_inc/v222/ansys/bin/linx64/ansys222 -j file -np 2 -port 50052 -grpc  /home/user/temp/ansys_ahmfaliakp


转换器模块有自己的命令行界面，用于将 MAPDL 文件转换为 PyMAPDL。更多信息，请参见 :ref:`ref_cli_converter`。