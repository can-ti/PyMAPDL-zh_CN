.. _extended_example01:


Gmsh example
============

Objective
---------
该示例演示了 PyAnsys 与 Gmsh 的互操作性， Gmsh 是一个非常著名的开源 Python 网格库。更多信息，请访问 Gmsh 网站：`Gmsh <gmsh_>`_。

Description
-----------
Gmsh 用于导入 STL 格式的外部几何体文件。 然后使用 `PyMAPDL Reader <legacy_reader_docs_>`_ 库将几何图形导入 PyMAPDL。 

本示例使用以下这些文件：

* ``gmsh_converter.py``: 加载 STEP 文件，绘制网格并保存为 Gmsh 文件。
* ``mesh_converter``: 将 MSH 文件转换为 Ansys CDB 数据库格式文件（归档文件）。
* ``modal_analysis.py``: 导入 CDB 数据库、设置模态分析并运行。它还会显示一阶模态的动画，并将其保存到名为 ``animation.gif`` 的 GIF 文件中。


Requirements
------------
您必须安装 Gmsh。可以使用 ``pip`` 安装：

.. code-block:: console

    pip install gmsh


Source code
-----------

``gmsh_generator.py`` file
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: gmsh_generator.py
    :linenos:
    :language: python


``mesh_converter.py`` file
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: mesh_converter.py
    :linenos:
    :language: python


``modal_analysis.py`` file
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: modal_analysis.py
    :linenos:
    :language: python



Notes
-----

您应将所有文件复制到一个单独的目录中，以便于运行示例。
