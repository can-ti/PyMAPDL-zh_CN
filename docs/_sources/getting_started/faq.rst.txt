.. _faq:

**************************
Frequently asked questions
**************************

如何报告问题？
=========================

如果发现问题，首先要访问 :ref:`疑难解答部分 <ref_troubleshooting>` ，了解可能的解决方案。

如果在那里找不到解决方案，您可以在 `GitHub 代码库 <pymapdl_repo_>`_ 中搜索您的问题。你可以使用 `搜索框 <pymapdl_search_issues_pr_>`_ 查找相关问题或拉动请求。

要提出更多开放式问题或向社区寻求建议，请使用 GitHub 代码库中的 `PyMAPDL 讨论 <pymapdl_discussions_>`_ 页面。

要报告 bug 和文档错误以及提出功能请求，请使用 GitHub 代码库中的 `PyMAPDL issues <pymapdl_issues_>`_ 页面。


PyMAPDL 与 Ansys ACT 相比有哪些优缺点？
=======================================================

利弊取决于您的 pipeline（工作流程） 和软件方法。Ansys ACT 是一种依赖于 Ansys Workbench 的方法，在 ACT 应用程序生成器中构建扩展，然后在 Ansys Mechanical 中运行。如果您打算更改参数，则必须使用 Ansys optiSLang 来更改参数并批处理解决方案。

与 Ansys ACT 相比，PyMAPDL 的主要优势在于

* PyMAPDL 与 Python 工具和开源模块紧密集成，可与 Ansys 软件一起运行。
* 脚本使用 Python 编写。ACT 使用 .NET，这意味着您只能调用 IronPython 以及 Ansys Mechanical 中的潜在其他工具。
* 由于 PyMAPDL 在 Ansys Mechanical 之外，因此您可以调用应用程序工作流，而无需为用户交互打开图形用户界面。如果需要图形用户界面，可以使用 `PyQt <https://pythonpyqt.com/>`_ 创建自己的图形用户界面。或者，您可以使用 `Matplotlib <https://matplotlib.org/>`_ 或 `VTK <https://vtk.org/>`_ 输出绘图。
* PyMAPDL 与现代 Python3兼容，而 ACT 只与 IronPython（Python2）兼容。

最佳方法取决于您的工作流程需求和开发软件的方式。


APDL 是否已被 Ansys "弃用"？如果是，这对 PyMAPDL 意味着什么？
============================================================================

APDL 不会消失。事实上，每当您调用 Mechanical Workbench 时，它都会生成一个输入文件 (``ds.dat``)，并将其输入 MAPDL。
不过，在过去几年中发生变化的是几何、网格划分和后处理的位置。几何图形的生成可以在 SpaceClaim 或 Design Modeler 中进行，
网格划分则使用 Workbench 中各种功能强大的新型网格划分工具完成。虽然这些工具远远优于 MAPDL 中的工具，但它们最大的局限是难以
编写脚本（尤其是外部脚本）。因此，仍有用户选择在 MAPDL 中生成几何体和网格。


与 Workbench 等其他 Ansys 产品相比，使用 PyMAPDL 的主要原因是什么？
==================================================================================

在某些任务中，使用其中一种总是比使用另一种更好。 Workbench 是快速制作原型、网格、设置边界条件和求解的绝佳工具。
因为它是大量开发工作的起点，所以有很多功能可以让分析运行变得更容易。不过，它受到 IronPython 脚本的限制。
此外，你无法在细粒度或高层次上调用多个产品，也无法使用诸如 `NumPy <https://numpy.org/>`_, 
`SciPy <https://scipy.org/>`_, `PyTorch <https://pytorch.org/>`_ 和 `TensorFlow <https://www.tensorflow.org/>`_ 之类的软件包。
PyMAPDL 将其与 MAPDL 相结合，使您能够拥有一个完全参数化的工作流，充分利用这些机器学习工具。它还允许您使用 `PyVista <pyvista_docs_>`_ 或 `Matplotlib <matplotlib_main_>`_ 生成高级绘图。


How do you end a simulation and restart a script?
=================================================
**如何结束一个模拟并重新启动脚本？**

关闭并重新打开 Python 会清除 Python 中的求解结果。要清除网格等所有先前的数据，可以使用以下代码：

.. code:: python

    import sys

    sys.modules[__name__].__dict__.clear()


不过，更有效的方法是使用 :meth:`clear() <ansys.mapdl.core.Mapdl.clear>` 方法清除 MAPDL。您也可以退出并重新启动 MAPDL。


为什么 PyMAPDL 的结果与 MAPDL GUI 中显示的结果不同？
=======================================================================

Listing results
---------------

MAPDL 图形用户界面中显示的结果与使用 PyMAPDL 得出的结果不同，可能有多种原因。最常见的原因是 MAPDL GUI 使用的图形配置与 PyMAPDL 使用的图形配置不同。

在 MAPDL 图形用户界面中，图形配置可以改变结果的显示方式。每种图形配置都以不同方式实现实体选择和平均。默认情况下，图形配置被设置为 ``Power Graphics`` 。然而，PyMAPDL 会连接到以批处理模式运行的 MAPDL 实例，该实例默认使用 ``Full Graphics`` 配置。图形配置的这种差异也会影响平均值。

您可以使用该命令更改 PyMAPDL 中的图形配置：

.. code:: python

    mapdl.graphics("POWER")

您也可以使用 ``POWRGRPH`` 按钮或此命令在 MAPDL GUI 中更改图形配置：

.. code:: text

    /GRAPHICS,FULL

如何对节点上的结果进行平均也会影响结果。默认情况下，MAPDL 会对节点上的结果取平均值，除非存在材料类型不连续的情况。更多信息，请参阅 :meth:`avres() <ansys.mapdl.core.Mapdl.avres>`。此外，命令 :meth:`efacet() <ansys.mapdl.core.Mapdl.efacet>` 可以影响结果的显示方式。

应确保在 MAPDL GUI 和 PyMAPDL 中，命令 :meth:`avres() <ansys.mapdl.core.Mapdl.avres>` 和 :meth:`efacet() <ansys.mapdl.core.Mapdl.efacet>` 的值相同。

最后，根据您试图获得的结果，您可能会使用不同的 MAPDL 命令。例如，命令 :meth:`post.element_displacement() <ansys.mapdl.core.post.PostProcessing.element_displacement>` 使用 ``PRETAB`` 和 ``ETAB`` 命令的组合来获取结果。这个 MAPDL 命令可能会显示与 PyMAPDL :meth:`presol() <ansys.mapdl.core.Mapdl.presol>` 方法不同的结果。为确保使用正确的命令，应比较使用 MAPDL 和 PyMAPDL 命令得到的结果。

.. note:: Further reading on `this discussion <pymapdl_discussion_differences_mapdl_pymapdl_>`_

Plotting results
----------------

即使 PyMAPDL 和 MAPDL 在结果值上达成一致，仍可能存在显示差异。例如，将四边形面节点上的标量值插值到整个面上并不是确定的。
