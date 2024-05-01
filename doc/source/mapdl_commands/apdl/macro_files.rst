.. _ref_macro_files_commands_api:

***********
Macro files
***********

.. currentmodule:: ansys.mapdl.core

这些 APDL 命令用于构建和执行命令宏。

.. note::
   这里的大部分命令都可以用 Python 替代。例如，不使用宏，而使用 Python 函数。用 ``os.mkdir`` 代替 ``/MKDIR``。

.. warning::
   这里的许多命令必须在 ``mapdl.non_interactive`` 中运行

.. autosummary::
   :toctree: _autosummary/

   Mapdl.cfclos
   Mapdl.cfopen
   Mapdl.cfwrite
   Mapdl.create
   Mapdl.dflab
   Mapdl.end
   Mapdl.mkdir
   Mapdl.msg
   Mapdl.pmacro
   Mapdl.psearch
   Mapdl.rmdir
   Mapdl.tee
   Mapdl.ulib
   Mapdl.use
