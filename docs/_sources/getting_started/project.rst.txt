.. _ref_project_page:

Pymapdl Project
================

简介和目的
------------------------
PyMAPDL 是更强大的 `PyAnsys <pyansys_>`_ 的一部分，旨在促进直接从 Python 使用 Ansys 技术。
其主要软件包 ``ansys-mapdl-core`` 提供以下功能：

- 通过 Python 和 Ansys 参数设计语言 (APDL) 编写 MAPDL 脚本。
- 在 Python 脚本或交互式 `Jupyter notebook <jupyter_>`_ 中使用 `PyVista <pyvista_docs_>`_ 绘制 MAPDL 几何图形和网格。
- 以 Python 对象（例如，节点、元素、求解矩阵和结果）的形式访问 MAPDL 数组。

借助 APDL 和 Python 用户都非常熟悉的 API，PyMAPDL 比以往任何时候都更容易将 Ansys MAPDL 
多物理场求解器的仿真功能直接集成到新型应用程序中。该软件包提供了一个 Python 友好界面，用于驱动管理低级 APDL 命令提交的软件，同时通过高性能 gRPC 接口交换数据。

使用 PyMAPDL 可以加速模拟的准备工作。将通用 Python 代码的表现力与驱动求解器的方法相结合，
以控制输入面板中的流程。使用交互式 Jupyter notebook 探索概念、验证研究或捕获知识。让 MAPDL 求解器作为下一个 AI 应用中的物理引擎。PyMAPDL现在是开源的，所以尽情享受吧。欢迎参与贡献。

背景
----------
PyMAPDL 基于 `gRPC <grpc_>`_，代表了对其基于 CORBA 的前身的改进。这些技术允许 MAPDL 求解器
充当服务器，随时准备响应连接的客户端。

Google 远程过程调用 （gRPC） 用于建立安全连接，以便客户端应用可以直接调用潜在远程 MAPDL 实例上的方法，
就好像它是本地对象一样。HTTP/2 的使用使其对现代互联网基础设施友好。这与二进制传输格式的使用一起，有利于
更高的性能。使用 gRPC，PyMAPDL 可以将 Python 语句转换为 APDL 命令，然后可以将其传输到在任何地方运行
的 MAPDL 实例，同时产生紧凑高效的网络占用空间。

下图显示了 PyMAPADDL 的简化架构。

.. figure:: ../images/architecture_diagram.png
    :width: 500pt

    PyMAPDL 架构图

Quick code
----------
下面是 PyMAPDL 工作原理的一个简短示例：

.. code:: python

    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl()
    >>> print(mapdl)
    Product:             Ansys Mechanical Enterprise
    MAPDL Version:       24.1
    ansys.mapdl Version: 0.68.0

现在 MAPDL 已激活，您可以像真正的 Python 类一样向其发送命令。
例如，如果您想使用关键点创建一个曲面，您可以运行

.. code:: python

    mapdl.run("/PREP7")
    mapdl.run("K, 1, 0, 0, 0")
    mapdl.run("K, 2, 1, 0, 0")
    mapdl.run("K, 3, 1, 1, 0")
    mapdl.run("K, 4, 0, 1, 0")
    mapdl.run("L, 1, 2")
    mapdl.run("L, 2, 3")
    mapdl.run("L, 3, 4")
    mapdl.run("L, 4, 1")
    mapdl.run("AL, 1, 2, 3, 4")

MAPDL 以交互方式返回每条命令的结果，并将其存储到日志模块中。
也可以使用 ``print(mapdl.run)`` 方法立即打印出结果。错误会被立即捕获并按 Pythonically 方法处理。

以 Python 方式调用 MAPDL
~~~~~~~~~~~~~~~~~~~~~~~~~~
MAPDL 函数可以以 Python 方式直接从 :class:`Mapdl <ansys.mapdl.core.mapdl.MapdlBase>` 实例
调用。这是为了简化对 MAPDL 的调用，尤其是当输入是 Python 中的变量时。例如，以下两个命令是等效的：

.. code:: python

    mapdl.k(1, 0, 0, 0)
    mapdl.run("K, 1, 0, 0, 0")

这种方法会为你处理字符串格式化。例如，从一个 numpy 数组中输入“关键点”：

.. code:: python

   # 用 MAPDL 创建 10 个随机关键点
   points = np.random.random((10, 3))
   for i, (x, y, z) in enumerate(points):
       mapdl.k(i + 1, x, y, z)


高级功能
~~~~~~~~~~~~~~~~~
命令行 MAPDL 可用的所有功能都可以在 PyMAPDL 中使用，而且通过 gRPC 还可以使用各种新功能。

例如，使用以下选项查看当前网格状态：

.. code:: python

   >>> mapdl.mesh
    ANSYS Mesh
      Number of Nodes:              7217
      Number of Elements:           2080
      Number of Element Types:      2
      Number of Node Components:    0
      Number of Element Components: 0

或者用以下命令将其保存为 VTK 文件：

.. code:: python

    >>> mapdl.mesh.save("mymesh.vtk")

甚至可以使用以下工具直接从 Python 环境中输出：

.. code:: python

    >>> mapdl.et(1, "SOLID186")
    >>> mapdl.vsweep("ALL")
    >>> mapdl.esize(0.1)
    >>> mapdl.eplot()

.. figure:: ../images/eplot_vtk.png
    :width: 500pt

    Element plot from MAPDL using ``PyMAPDL`` and ``vtk``

Documentation and issues
------------------------
PyMAPDL 最新稳定版本的文档托管在 `PyMAPDL documentation <https://mapdl.docs.pyansys.com/version/stable/>`_。
同样的文档也可以 `PDF 格式 <pymapdl_latest_pdf_doc_>`_ 在最新 GitHub 包发布的 `Assets <pymapdl_latest_github_release_>`_ 中
的部分中获得。

在文档标题栏的右上角有一个选项，可以从查看最新稳定版本的文档切换到查看开发版本或以前发布版本的文档。

您还可以 `查看 <https://cheatsheets.docs.pyansys.com/pymapdl_cheat_sheet.png>`_ 
或 `下载 <https://cheatsheets.docs.pyansys.com/pymapdl_cheat_sheet.pdf>`_ PyMAPDL cheat sheet。
这一页参考资料提供了使用 PyMAPDL 的语法规则和命令。

在 `PyMAPDL Issues <https://github.com/ansys/pymapdl/issues>`_ 页面上，您可以创建问题来报告错误和申请新功能。
在 `PyMAPDL Discussions <https://github.com/ansys/pymapdl/discussions>`_ 页面或 Ansys Developer 门户网站上
的 `Discussions <https://discuss.ansys.com/>`_ 页面，您可以发布问题、分享想法并获得社区反馈。

要联系 PyAnsys 项目支持团队，请发送电子邮件至 `PyAnsys 核心团队 <pyansys.core@ansys.com>`_。遗憾的是，这封邮件无法回答
具体的库问题。请参阅 `PyMAPDL Issues <pymapdl_issues_>`_ 或 `PyMAPDL Discussions <pymapdl_discussions_>`_ 以提出问题、请求新功能或提问。


Project index
-------------

* :ref:`genindex`