.. _ref_array_parameters_commands_api:

****************
Array parameters
****************

.. currentmodule:: ansys.mapdl.core

这些 APDL 命令用于对参数数组（向量和矩阵）进行操作。

.. note::
   保留这些命令中的许多命令是为了与传统命令兼容。

   要以更 Pythonic 的方式与数组交互，请参见参数类 :ref:`ref_parameters_api` 。

   如果要在 MAPDL 之外处理数组，可以考虑使用 `NumPy <https://numpy.org/>`_ 。


.. autosummary::
   :toctree: _autosummary/

   Mapdl.mfouri
   Mapdl.mfun
   Mapdl.moper
   Mapdl.mwrite
   Mapdl.sread
   Mapdl.toper
   Mapdl.vabs
   Mapdl.vcol
   Mapdl.vcum
   Mapdl.vfact
   Mapdl.vfun
   Mapdl.vitrp
   Mapdl.vlen
   Mapdl.vmask
   Mapdl.voper
   Mapdl.starvput
   Mapdl.vscfun
   Mapdl.vstat
   Mapdl.vwrite
