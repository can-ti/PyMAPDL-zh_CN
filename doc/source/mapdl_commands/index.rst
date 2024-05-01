.. _ref_mapdl_commands:

==============
MAPDL commands
==============
本节概述了通过 PyMAPDL 以 Python 封装的经典 MAPDL 命令。大多数命令已被封装，但有一些命令在 PyMAPDL 中不被本地支持或仅被部分支持。详情请参见 :ref:`ref_unsupported_commands` 。

*******
Session
*******
这些命令为会话提供一般控制。这些命令按功能分组。

.. toctree::
   :maxdepth: 1

   session/run_controls
   session/processor_entry
   session/files
   session/list_controls


********
Database
********
这些命令用于对数据库进行全局操作。

.. toctree::
   :maxdepth: 1

   database/setup
   database/selecting
   database/components
   database/working_plane
   database/coord_sys
   database/picking

********
Graphics
********
这些命令用于控制程序的图形。

.. toctree::
   :maxdepth: 1

   graphics/setup
   graphics/views
   graphics/scaling
   graphics/style
   graphics/labeling
   graphics/graphs
   graphics/annotation


****
APDL
****
这些命令构成了 ANSYS 参数化设计语言（APDL）。

.. toctree::
   :maxdepth: 1

   apdl/parameter_definition
   apdl/macro_files
   apdl/abbreviations
   apdl/array_parm
   apdl/matrix_op
   apdl/process_controls

.. _ref_prep_commands:

*************
Preprocessing
*************

这些命令用于创建和设置模型。


.. toctree::
   :maxdepth: 1

   prep7/database
   prep7/element_type
   prep7/real_constants
   prep7/materials
   prep7/material_data_tables
   prep7/primitives
   prep7/keypoints
   prep7/hard_points
   prep7/lines
   prep7/areas
   prep7/volumes
   prep7/booleans
   prep7/meshing
   prep7/nodes
   prep7/elements
   prep7/superelements
   prep7/digitizing
   prep7/coupled_dof
   prep7/constraint_equations
   prep7/status
   prep7/explicit_dynamics
   prep7/sections
   prep7/morphing
   prep7/artificially_matched_layers
   prep7/special_purpose


********
Solution
********
这些命令用于加载和求解模型。

.. toctree::
   :maxdepth: 1

   solution/analysis_options
   solution/nonlinear_options
   solution/dynamic_options
   solution/spectrum_options
   solution/load_step_options
   solution/solid_constraints
   solution/solid_forces
   solution/solid_surface_loads
   solution/solid_body_loads
   solution/inertia
   solution/miscellaneous_loads
   solution/load_step_operations
   solution/master_dof
   solution/gap_conditions
   solution/rezoning
   solution/2d_to_3d_analysis
   solution/birth_and_death
   solution/fe_constraints
   solution/fe_forces
   solution/fe_surface_loads
   solution/fe_body_loads
   solution/ocean
   solution/solution_status
   solution/radiosity
   solution/multi_field_solver_definition_commands
   solution/multi_field_solver_global_controls
   solution/multi_field_solver_time_controls
   solution/multi_field_solver_load_transfer
   solution/multi_field_solver_convergence_controls
   solution/multi_field_solver_interface_mapping
   
*****
POST1
*****
这些命令用于使用数据库处理器对结果进行后处理。

.. toctree::
   :maxdepth: 1

   post1/setup
   post1/controls
   post1/results
   post1/element_table
   post1/listing
   post1/animation
   post1/path_operations
   post1/surface_operations
   post1/load_case
   post1/magnetics_calc
   post1/trace_points
   post1/special
   post1/status
   post1/failure_criteria

******
POST26
******
这些命令用于使用时间历程处理器对结果进行后处理。

.. toctree::
   :maxdepth: 1

   post26/setup
   post26/controls
   post26/operations
   post26/display
   post26/listing
   post26/special
   post26/status


****
AUX2
****
这些命令用于检查或处理程序生成的二进制文件的内容。


.. toctree::
   :maxdepth: 1

   aux2/bin_dump
   aux2/bin_manip


****
AUX3
****
通过辅助处理器 ``/AUX3`` 可以对结果文件进行操作，删除数据集或更改数值。

.. toctree::
   :maxdepth: 1

   aux3


*****
AUX12
*****
这些命令用于定义热分析中使用的辐射选项。

.. toctree::
   :maxdepth: 1

   aux12/general_radiation
   aux12/radiation_mat
   aux12/radiosity_solver


*****
AUX15
*****
这些命令用于读取 IGES 文件，以便在 ANSYS 中进行分析。

.. toctree::
   :maxdepth: 1

   aux15


*****************
Mapping processor
*****************
``MAP`` 处理器允许您将外部文件中的数据映射到现有几何体上。

.. toctree::
   :maxdepth: 1

   map


***************
DISPLAY program
***************
这些命令用于 DISPLAY 程序。DISPLAY 程序是 ANSYS 的配套程序，用于恢复 ANSYS 中生成的图形显示。

.. note::
   这些命令中有许多在使用 PyMAPDL 时并不适用。

.. toctree::
   :maxdepth: 1

   display/setup


**********************
REDUCED order modeling
**********************

.. toctree::
   :maxdepth: 1

   reduced/setup
   reduced/preparation
   reduced/generation
   reduced/use_pass

*******************
Connection commands
*******************

这些命令可将外部 CAD 文件读入 MAPDL。

.. toctree::
   :maxdepth: 1

   conn


**********************
Miscellaneous commands
**********************

未记录的其他命令。

.. toctree::
   :maxdepth: 1

   misc



*****************************
Undocumented inquire commands
*****************************

未记录的查询命令。

.. warning:: 
   **声明** : 《ANSYS 命令参考指南》官方文档中没有该功能的说明。因此，对它的支持有限，也不鼓励使用。 **Please use it with caution.**


.. toctree::
   :maxdepth: 1

   inqfun


