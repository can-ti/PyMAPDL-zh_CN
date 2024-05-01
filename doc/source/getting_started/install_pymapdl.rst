

.. _ref_pymapdl_installation:

***************
Install PyMAPDL
***************

Python module
~~~~~~~~~~~~~
目前， ``ansys.mapdl.core`` 软件包支持 Windows、Mac OS 和 Linux 上的 Python 3.8 至 Python 3.11。

从 `PyPi <pymapdl_pypi_>`_ 安装最新版本：

.. code:: console

   pip install ansys-mapdl-core

或者，使用此命令从 `PyMAPDL GitHub <pymapdl_issues_>`_ 安装最新版本：

.. code:: console

   pip install git+https://github.com/ansys/pymapdl.git


如需本地*开发*版本，请使用以下命令进行安装：

.. code:: console

   git clone https://github.com/ansys/pymapdl.git
   cd pymapdl
   pip install -e .

安装开发版本后，您可以在本地修改 ``ansys-mapdl-core`` 包，并在重启 Python 内核后将更改反映到设置中。


Offline installation
~~~~~~~~~~~~~~~~~~~~
如果您的安装机器上没有互联网连接，推荐的安装 PyMAPDL 的方法是从 `Releases <pymapdl_releases_>`_
页面下载相应机器架构的 wheelhouse 压缩包。

每个 wheelhouse 压缩包都包含在 Windows 和 Linux 上从头开始安装 PyMAPDL 所需的所有 Python 工具。
您可以将其安装在全新安装 Python 的独立系统上，也可以安装在虚拟环境中。

例如，在使用 Python 3.9 的 Linux 上，解压缩 wheelhouse 压缩包，然后使用以下命令安装：

.. code:: console

   unzip PyMAPDL-v0.68.dev1-wheelhouse-Linux-3.9.zip wheelhouse
   pip install ansys-mapdl-core -f wheelhouse --no-index --upgrade --ignore-installed

如果您使用的是 Python 3.9 版本的 Windows 操作系统，请解压到 ``wheelhouse`` 目录，然后使用前面的命令进行安装。

考虑使用 `虚拟环境 <using_venv_>`_ 进行安装。

Verify your installation
~~~~~~~~~~~~~~~~~~~~~~~~

.. note::
   要使用 PyMAPDL，您必须在本地安装 Ansys。安装的 Ansys 版本决定了您可以使用的界面和功能。

   有关获取 Ansys 授权副本的详细信息，请访问 `Ansys <ansys_>`_。

通过导入模块检查是否正确安装了软件包：

.. code:: python

    >>> from ansys.mapdl import core as pymapdl


有关启动 PyMAPDL 并将其连接到 MAPDL 实例的信息，请参阅 :ref:`ref_launch_pymapdl`。
