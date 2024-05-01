.. _ref_user_guide:

==========
User guide
==========
本节概述了 PyMAPDL 及其使用方法。


..
   该索引必须是顶级索引，才能显示在 pydata_sphinx_theme 中

.. toctree::
   :maxdepth: 1
   :hidden:

   mapdl
   convert
   mesh_geometry
   plotting
   parameters
   components
   post
   cli
   mapdl_examples
   database
   math
   pool
   xpl
   upf
   krylov_method
   troubleshoot


PyMAPDL overview
================
``ansys-mapdl-core`` 库中的 :func:`launch_mapdl() <ansys.mapdl.core.launcher.launch_mapdl>` 函数
会在后台创建 :class:`Mapdl <ansys.mapdl.core.mapdl.MapdlBase>` 类的实例，并向该实例发送命令。
错误和警告通过 Python 处理，让您可以实时开发脚本，而不必担心在批处理模式下部署时脚本是否能正常运行。

可以使用 :func:`launch_mapdl() <ansys.mapdl.core.launcher.launch_mapdl>` 方法在 gRPC 模式下从 Python 启动 MAPDL。默认情况下，它会在临时目录中启动 MAPDL。您可以使用此代码将其更改为当前目录：
 
.. note::

   这里的”临时目录“，具体是在哪儿？  （——ff）

.. code:: python

    import os
    from ansys.mapdl.core import launch_mapdl

    path = os.getcwd()
    mapdl = launch_mapdl(run_location=path)

现在，MAPDL 已激活，您可以像真正的 Python 类一样向其发送命令。例如，如果您想使用关键点创建一个曲面，您可以运行

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

MAPDL 以交互方式返回每条命令的结果，并将其存储到日志模块中。错误会被立即捕获。例如，如果您输入了一条无效命令：

.. code:: pycon

   >>> mapdl.run("AL, 1, 2, 3")

   MapdlRuntimeError: 
   AL, 1, 2, 3

   DEFINE AREA BY LIST OF LINES
   LINE LIST =     1    2    3
   TRAVERSED IN SAME DIRECTION AS LINE     1)

   *** ERROR ***                           CP =       0.338   TIME= 09:45:36
   Keypoint 1 is referenced by only one line.  Improperly connected line   
   set for AL command.                                                     

这个 ``MapdlRuntimeError`` 立即被捕获。这意味着您可以用 Python 编写 MAPDL 脚本，以交互方式运行，然后以批处理方式运行，而不必担心如果将脚本输出到脚本文件，脚本是否能正确运行。

:class:`Mapdl <ansys.mapdl.core.mapdl.MapdlBase>` 类支持的功能远不止向 MAPDL 发送文本。它包括更高级别的封装，允许更好地编写脚本和与 MAPDL 交互。有关可视化、脚本和与 MAPDL 交互的各种高级方法的概述，请参阅 :ref:`ref_examples`。


Calling MAPDL Pythonically
~~~~~~~~~~~~~~~~~~~~~~~~~~

MAPDL 函数可以以 Pythonic 方式直接从 :class:`Mapdl <ansys.mapdl.core.mapdl.MapdlBase>` 的实例中调用。这是为了简化对 Ansys 的调用，尤其是当输入是 Python 中的变量时。例如，以下两条命令是等价的：

.. code:: python

    mapdl.k(1, 0, 0, 0)
    mapdl.run("K, 1, 0, 0, 0")

这种方法有一些明显的优势。首先，它更容易编写脚本，因为 ``ansys-mapdl-core`` 会为你处理字符串格式化。例如，你可以用以下方式从一个 numpy 数组中输入 points ：

.. code:: python

   # make 10 random keypoints in Ansys
   points = np.random.random((10, 3))
   for i, (x, y, z) in enumerate(points):
       mapdl.k(i + 1, x, y, z)

此外， Python 还会捕获和处理异常。

.. code:: pycon

   >>> mapdl.run("AL, 1, 2, 3")

   Exception: 
   AL, 1, 2, 3

   DEFINE AREA BY LIST OF LINES
   LINE LIST =     1    2    3
   (TRAVERSED IN SAME DIRECTION AS LINE     1)

   *** ERROR ***                           CP =       0.338   TIME= 09:45:36
   Keypoint 1 is referenced by only one line.  Improperly connected line   
   set for AL command.                                                     


对于较长的脚本，您可以运行 MAPDL ，而不是向 area 创建示例中的 MAPDL 发送命令：

.. code:: python

    # clear existing geometry
    mapdl.finish()
    mapdl.clear()

    # create a square area using keypoints
    mapdl.prep7()
    mapdl.k(1, 0, 0, 0)
    mapdl.k(2, 1, 0, 0)
    mapdl.k(3, 1, 1, 0)
    mapdl.k(4, 0, 1, 0)
    mapdl.l(1, 2)
    mapdl.l(2, 3)
    mapdl.l(3, 4)
    mapdl.l(4, 1)
    mapdl.al(1, 2, 3, 4)

这种方法有一些明显的优势，主要是编写脚本更容易，因为 :class:`Mapdl <ansys.mapdl.core.mapdl.MapdlBase>` 会为您处理字符串格式化。例如，从 numpy 数组中输入 points ：

.. code:: python

   import numpy as np

   # make 10 random keypoints in MAPDL
   points = np.random.random((10, 3))
   for i, (x, y, z) in enumerate(points):
       mapdl.k(i + 1, x, y, z)

此外，MAPDL 类的每个函数都有相关帮助。例如

.. code:: pycon

    >>> help(mapdl.k)

    Help on method K in module ansys.mapdl.core.mapdl_grpc.MapdlGrpc:

    k(npt='', x='', y='', z='') method of ansys.mapdl.core.mapdl_grpc.MapdlGrpc
    instance

        Defines a keypoint.

        APDL Command: K

        Parameters
        ----------
        npt
            Reference number for keypoint. If zero, the lowest
            available number is assigned [NUMSTR].

        x, y, z
            Keypoint location in the active coordinate system (may be
            R, θ, Z or R, θ, Φ). If X = P, graphical picking is
            enabled and all other fields (including NPT) are ignored
            (valid only in the GUI).

        Examples
        --------
        Create a keypoint at (1, 1, 2)

    >>> mapdl.k(1, 1, 1, 2)

        Notes
        -----
        Defines a keypoint in the active coordinate system [CSYS] for
        line, area, and volume descriptions. A previously defined
        keypoint of the same number is then redefined. A keypoint may
        be redefined only if it is not yet attached to a line or is
        not yet meshed. Solid modeling in a toroidal system is not
        recommended.


有关稳定性方面的考虑，请参阅 :ref:`PyMAPDL 稳定性 <ref_pymapdl_stability>`。
