
.. _ref_components:

*******************
Managing components
*******************

可以使用 :attr:`Mapdl.components <ansys.mapdl.core.Mapdl.components>` 来检索和设置 MAPDL 组件。


在 MAPDL 中创建组件有几种方法。

您可以使用 :meth:`Mapdl.cm <ansys.mapdl.core.Mapdl.cm>` 方法：

.. code:: python

   >>> from ansys.mapdl.core import launch_mapdl
   >>> mapdl = launch_mapdl()
   >>> mapdl.prep7()
   >>> mapdl.block(0, 1, 0, 1, 0, 1)
   >>> mapdl.vsel("s", "", "", 1)
   >>> mapdl.cm("my_comp", "volu")

或者使用更高级别的语法。例如，设置一个组件，指定其类型和项目：

.. code:: python

    >>> mapdl.components["mycomp3"] = "KP", [1, 2, 3]

设置组件，但不指定类型，默认为 ``NODE``：

.. code:: python

   >>> mapdl.components["mycomp4"] = (1, 2, 3)
   /Users/german.ayuso/pymapdl/src/ansys/mapdl/core/component.py:347: UserWarning: Assuming   a KP selection.
   It is recommended you use the following notation to avoid this warning:
   > mapdl.components['mycomp4'] = 'KP' (1, 2, 3)
   Alternatively, you disable this warning using:
   > mapdl.components.default_entity_warning=False
   warnings.warn(

您可以通过更改 :attr:`Mapdl.components.default_entity <ansys.mapdl.core.Mapdl.components.default_entity>` 来更改默认类型。

.. code:: python

    >>> mapdl.components.default_entity = "KP"
    >>> mapdl.components["mycomp"] = [1, 2, 3]
    >>> mapdl.components["mycomp"].type
    'KP'

您也可以从已选定的实体中创建组件：

.. code:: python

    >>> mapdl.lsel("S", 1, 2)
    >>> mapdl.components["mylinecomp"] = "LINE"
    >>> mapdl.components["mylinecomp"]
    (1, 2)


选择并检索组件

.. code:: python

    >>> mapdl.cmsel("s", "mycomp3")
    >>> mapdl.components["mycomp3"]
    Component(type='KP', items=(1, 2, 3))


.. note:: Component selection
    要通过 :attr:`Mapdl.components <ansys.mapdl.core.Mapdl.components>` 访问组件，需要使用 :meth:`Mapdl.cmsel() <ansys.mapdl.core.Mapdl.cmsel>` 选择组件。


Component object
================

`组件对象 <ansys.mapdl.core.component.Component>`_ 是 :attr:`Mapdl.components <ansys.mapdl.core.Mapdl.components>` 用组件名称查询时由 :attr:`Mapdl.components <ansys.mapdl.core.Mapdl.components>` 返回的对象。
该对象有两个主要属性： `type <Component.type>`_ 和 `items <Component.items>`_ 。前者返回组件类型（ `"ELEM"` 、 `"NODE"` 、 `"KP"` 等），后者返回一个包含属于该组件的实体索引的元组。

.. code:: python

    >>> comp = mapdl.components["mycomp3"]
    >>> comp.type
    'KP'
    >>> comp.items
    (1, 2, 3)

应该注意的是，组件对象与 MAPDL 组件没有链接，因此对它的任何更改都不会反映在 MAPDL 对应组件中。

