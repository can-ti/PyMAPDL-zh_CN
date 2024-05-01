.. _user_guide_postprocessing:

Postprocessing
==============
在活动的 MAPDL 会话中，您可以使用 :class:`Mapdl.post_processing <ansys.mapdl.core.post.PostProcessing>` 类（:class:`Mapdl <ansys.mapdl.core.mapdl.MapdlBase>` 实例的属性）进行后处理。
这种方法的一个优点是能与现有的 MAPDL 脚本或自动化很好地集成。这种方法也可用于其他程序（包括 ANSYS Mechanical）生成的结果文件。

基于 gRPC 的后处理的最大优势之一是可以远程完成，无需交换任何文件。 数千兆字节的结果文件可以保持远程状态，只将必要的数据流传输回客户端进行审查或可视化。

.. note::

   我们鼓励您使用 `DPF-Core <dpf_core_gh_>`_ 和 `DPF-Post <dpf_post_gh_>`_ 中的数据处理框架 (DPF) 模块，因为它们提供了使用客户端-服务器界面访问 Ansys 结果文件的现代界面。它们使用与 Ansys Workbench 中相同的软件，但通过 Python 客户端。


您通常会使用 ``PRNSOL`` 命令从 MAPDL 请求节点结果：

.. code:: output

     POST1:
     PRNSOL, U, X
    
     PRINT U    NODAL SOLUTION PER NODE
    
      ***** POST1 NODAL DEGREE OF FREEDOM LISTING *****                            
     
      LOAD STEP=     1  SUBSTEP=     1                                             
       TIME=    1.0000      LOAD CASE=   0                                         
     
      THE FOLLOWING DEGREE OF FREEDOM RESULTS ARE IN THE GLOBAL COORDINATE SYSTEM  
     
        NODE       UX    
           1  0.10751E-003
           2  0.85914E-004
           3  0.57069E-004
           4  0.13913E-003
           5  0.35621E-004
           6  0.52186E-004
           7  0.30417E-004
           8  0.36139E-004
           9  0.15001E-003
     MORE (YES,NO OR CONTINUOUS)=


不过，使用 :class:`Mapdl <ansys.mapdl.core.mapdl.MapdlBase>` 类的实例，您可以请求节点位移：

.. code:: python

    >>> mapdl.set(1, 1)
    >>> disp_x = mapdl.post_processing.nodal_displacement("X")
    array([1.07512979e-04, 8.59137773e-05, 5.70690047e-05, ...,
           5.70333124e-05, 8.58600402e-05, 1.07445726e-04])

您还可以使用此代码绘制节点位移图：

.. code:: python

    >>> mapdl.post_processing.plot_nodal_displacement("X")


.. figure:: ../images/post_norm_disp.png
    :width: 300pt

    Normalized Displacement of a Cylinder from MAPDL


Selecting entities
------------------

如果节点或单元被选中，MAPDL 数据库会独立处理某些结果。如果您已经子选择了某个组件，
并希望同时限制某个输出结果（:func:`nodal_displacement() <ansys.mapdl.core.post.PostProcessing.nodal_displacement>` ），
请使用 :attr:`selected_nodes <ansys.mapdl.core.post.PostProcessing.selected_nodes>` 属性来获取当前选定节点的掩码：

.. code:: python

    >>> mapdl.nsel("S", "NODE", vmin=1, vmax=2000)
    >>> mapdl.esel("S", "ELEM", vmin=500, vmax=2000)
    >>> mask = mapdl.post_processing.selected_nodes


Postprocessing object methods
------------------------------

有关所有后处理方法的列表，请参阅 :ref:`post_processing_api`。


Enriched command output
~~~~~~~~~~~~~~~~~~~~~~~

所有 :class:`Mapdl <ansys.mapdl.core.mapdl.MapdlBase>` 类命令都会输出一个字符串对象，可以对其进行解析以获取特定数据。

在某些 :class:`Mapdl <ansys.mapdl.core.mapdl.MapdlBase>` 类命令中，返回的字符串包含一些处理输出的方法。 Table-1_ 列出了这些命令。

.. _Table-1:

**Table 1. Commands with extra processing methods in the output**

+----------------+---------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------+
| Category       | Extra methods available                                                                           | MAPDL commands                                                           |
+================+===================================================================================================+==========================================================================+
| **Listing**    | * :class:`cmd.to_list() <ansys.mapdl.core.commands.CommandListingOutput>`                         | **Results listing**                                                      |
|                | * :class:`cmd.to_array() <ansys.mapdl.core.commands.CommandListingOutput>`                        |                                                                          |
|                | * :class:`cmd.to_dataframe() <ansys.mapdl.core.commands.CommandListingOutput>`                    | * :func:`Mapdl.prcint() <ansys.mapdl.core.Mapdl.prcint>`                 |
|                |                                                                                                   | * :func:`Mapdl.prenergy() <ansys.mapdl.core.Mapdl.prenergy>`             |
|                |                                                                                                   | * :func:`Mapdl.prerr() <ansys.mapdl.core.Mapdl.prerr>`                   |
|                |                                                                                                   | * :func:`Mapdl.presol() <ansys.mapdl.core.Mapdl.presol>`                 |
|                |                                                                                                   | * :func:`Mapdl.pretab() <ansys.mapdl.core.Mapdl.pretab>`                 |
|                |                                                                                                   | * :func:`Mapdl.print() <ansys.mapdl.core.Mapdl.print>`                   |
|                |                                                                                                   | * :func:`Mapdl.priter() <ansys.mapdl.core.Mapdl.priter>`                 |
|                |                                                                                                   | * :func:`Mapdl.prjsol() <ansys.mapdl.core.Mapdl.prjsol>`                 |
|                |                                                                                                   | * :func:`Mapdl.prnld() <ansys.mapdl.core.Mapdl.prnld>`                   |
|                |                                                                                                   | * :func:`Mapdl.prnsol() <ansys.mapdl.core.Mapdl.prnsol>`                 |
|                |                                                                                                   | * :func:`Mapdl.prorb() <ansys.mapdl.core.Mapdl.prorb>`                   |
|                |                                                                                                   | * :func:`Mapdl.prpath() <ansys.mapdl.core.Mapdl.prpath>`                 |
|                |                                                                                                   | * :func:`Mapdl.prrfor() <ansys.mapdl.core.Mapdl.prrfor>`                 |
|                |                                                                                                   | * :func:`Mapdl.prrsol() <ansys.mapdl.core.Mapdl.prrsol>`                 |
|                |                                                                                                   | * :func:`Mapdl.prsect() <ansys.mapdl.core.Mapdl.prsect>`                 |
|                |                                                                                                   | * :func:`Mapdl.prvect() <ansys.mapdl.core.Mapdl.prvect>`                 |
|                |                                                                                                   | * :func:`Mapdl.swlist() <ansys.mapdl.core.Mapdl.swlist>`                 |
|                |                                                                                                   |                                                                          |
|                |                                                                                                   |  **Other Listing**                                                       |
|                |                                                                                                   |                                                                          |
|                |                                                                                                   | * :func:`Mapdl.set("LIST") <ansys.mapdl.core.Mapdl.set>`                 |
|                |                                                                                                   | * :func:`Mapdl.nlist() <ansys.mapdl.core.Mapdl.nlist>`                   |
|                |                                                                                                   |                                                                          |
+----------------+---------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------+  
| **Boundary**   | * :func:`cmd.to_list() <ansys.mapdl.core.commands.BoundaryConditionsListingOutput>`               | * :func:`Mapdl.dlist() <ansys.mapdl.core.Mapdl.dlist>`                   |
| **Conditions** | * :func:`cmd.to_dataframe() <ansys.mapdl.core.commands.BoundaryConditionsListingOutput>`          | * :func:`Mapdl.flist() <ansys.mapdl.core.Mapdl.flist>`                   |
| **Listing**    |                                                                                                   |                                                                          |
+----------------+---------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------+

.. warning:: 
   如果使用 :func:`Mapdl.nlist() <ansys.mapdl.core.Mapdl.nlist>` 这样的方法，您可能会获得比使用 :class:`Mesh <ansys.mapdl.core.mesh_grpc.MeshGrpc>` 方法更低的精度。

下面有一个简单的示例来演示使用方法：

.. code:: python

    
    >>> from ansys.mapdl.core import launch_mapdl
    >>> from ansys.mapdl.core import examples

    >>> mapdl = launch_mapdl()
    >>> example = examples.vmfiles["vm10"]
    >>> mapdl.input(example)

    >>> mapdl.slashsolu()
    >>> mapdl.solve()

    >>> mapdl.post1()
    >>> cmd = mapdl.prnsol("U", "X")

    # Output as a list.

    >>> cmd.to_list()
    [['1', '0.0000'], ['2', '0.0000']]

    # Output as array.

    >>> cmd.to_array()
    array([[1., 0.],
           [2., 0.]])

    # Output as dataframe.

    >>> cmd.to_dataframe()
    NODE   UX
    0      1.0
    1      2.0
