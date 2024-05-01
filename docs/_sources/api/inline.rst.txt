.. _inline_functions_api:

Inline functions
================

.. currentmodule:: ansys.mapdl.core.inline_functions

这些是内联 APDL 函数的封装版本，用于执行给定节点编号（ ``Query.nx`` ）后查找节点 x 坐标等操作。

.. autoclass:: ansys.mapdl.core.inline_functions.Query

.. autosummary::
   :toctree: _autosummary/

   Query.node
   Query.kp

   Query.centrx
   Query.centry
   Query.centrz

   Query.kx
   Query.ky
   Query.kz

   Query.nx
   Query.ny
   Query.nz

   Query.ux
   Query.uy
   Query.uz

   Query.rotx
   Query.roty
   Query.rotz

   Query.lx
   Query.ly
   Query.lz

   Query.lsx
   Query.lsy
   Query.lsz

   Query.nsel
   Query.ksel
   Query.lsel
   Query.asel
   Query.esel
   Query.vsel
