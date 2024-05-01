Access MAPDL database
=====================

.. warning:: 
    此功能仍处于测试阶段。要报告任何错误或建议，请在 `GitHub <pymapdl_new_issue_>`_ 上提交问题。


在 PyMAPDL v0.61.2 及更高版本中，您可以使用 DB 模块访问 MAPDL 数据库中的单元和节点数据。


Usage
~~~~~

获取 ``lems`` 和 ``nodes`` 对象。

.. code:: python

   >>> from ansys.mapdl.core import launch_mapdl
   >>> from ansys.mapdl.core.examples import vmfiles
   >>> mapdl = launch_mapdl()
   >>> mapdl.input(vmfiles["vm271"])
   >>> elems = mapdl.db.elems
   >>> elems
   MAPDL Database Elements
      Number of elements:          3459
      Number of selected elements: 3459
      Maximum element number:      3459

   >>> nodes = mapdl.db.nodes
   MAPDL Database Nodes
      Number of nodes:          3652
      Number of selected nodes: 3652
      Maximum node number:      3652

获取第一个单元。

.. code:: python
    
    >>> elems = mapdl.db.elems
    >>> elems.first()
    1


检查单元是否被选中。

.. code:: python

    >>> from ansys.mapdl.core.database import DBDef
    >>> elems.info(1, DBDef.DB_SELECTED)

返回单元 1 的单元信息。

.. code:: python

    >>> elems = mapdl.db.elems
    >>> elem_info = elems.get(1)
    >>> elem_info
    ielem: 1
    elmdat: 1
    elmdat: 1
    elmdat: 1
    elmdat: 1
    elmdat: 0
    elmdat: 0
    elmdat: 12
    elmdat: 0
    elmdat: 0
    elmdat: 0
    nnod: 2
    nodes: 1
    nodes: 3

返回属于单元的节点。

.. code:: python

    >>> elem_info.nodes
    [1, 3]

返回单元数据。

.. code:: python

    >>> elem_info.elmdat
    [1, 1, 1, 1, 0, 0, 12, 0, 0, 0]

返回节点 22 的选择状态和坐标。

.. code:: python

    >>> nodes = mapdl.db.nodes
    >>> sel, coord = nodes.coord(22)
    >>> coord
    (-0.0014423144202849985, 0.010955465718673852, 0.0, 0.0, 0.0, 0.0)

.. note:: 由 ``coord`` 方法返回的坐标包含以下内容：X、Y、Z、THXY、THYZ 和 THZX。


Requirements
~~~~~~~~~~~~

要使用 ``DB`` 功能，您必须满足这些要求：

* ``ansys.api.mapdl`` 软件包版本应为 0.5.1 或更高。
* Ansys MAPDL 版本应为 2021 R1 或更高版本。

.. warning:: 
    该功能在 Ansys 2023 R1 中不起作用。



