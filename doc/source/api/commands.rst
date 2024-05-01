.. _ref_commands_api:

Commands output
===============

有助于数据后处理的各种 PyMAPDL 类和命令。

所有这些类都是 :py:class:`str` 类的子类，因此它们继承了 :class:`string` 的所有方法和属性。

.. currentmodule:: ansys.mapdl.core.commands

.. 我们应该在以下类 autosummary 中添加 `:toctree：_autosummary` 一行，以消除构建过程中的警告，
   但是，侧边栏中只显示方法链接（toctree），而不显示类，而且由于两个类的方法名称相同，因此会造成混淆。


.. autoclass:: ansys.mapdl.core.commands.CommandListingOutput

.. autosummary::

   CommandListingOutput.to_list
   CommandListingOutput.to_array
   CommandListingOutput.to_dataframe


.. autoclass:: ansys.mapdl.core.commands.BoundaryConditionsListingOutput

.. autosummary::

   BoundaryConditionsListingOutput.to_list
   BoundaryConditionsListingOutput.to_dataframe