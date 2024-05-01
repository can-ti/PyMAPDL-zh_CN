.. _ref_process_controls_api:

****************
Process controls
****************

.. currentmodule:: ansys.mapdl.core

这些 APDL 命令可用于控制其他命令的处理顺序。

.. note::
   以下命令没有直接映射到 PyMAPDL。如果必须使用这些命令，请使用 `non-interactive` ，但最好用 Python 语句来代替。

   * ``*CYCLE``
   * ``*DO``
   * ``*DOWHILE``
   * ``*ELSE``
   * ``*ELSEIF``
   * ``*ENDDO``
   * ``*ENDIF``
   * ``*EXIT``
   * ``*GO``
   * ``*IF``
   * ``*REPEAT``
   * ``*RETURN``


.. autosummary::
   :toctree: _autosummary/

   Mapdl.wait
