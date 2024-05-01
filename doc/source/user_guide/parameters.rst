
.. _ref_parameters:

*********************************
Setting and retrieving parameters
*********************************

可以使用 :attr:`Mapdl.parameters <ansys.mapdl.core.Mapdl.MapdlBase>` 从 :class:`Mapdl <ansys.mapdl.core.mapdl.MapdlBase>` 的实例中获取 MAPDL 参数。
例如，如果您想使用 MAPDL 的 :func:`Mapdl.get() <ansys.mapdl.core.Mapdl.get>` 方法来填充一个参数，那么您就可以用代码来访问该参数：

.. code:: python

   >>> from ansys.mapdl.core import launch_mapdl
   >>> mapdl = launch_mapdl()
   >>> mapdl.get("DEF_Y", "NODE", 2, "U", "Y")
   >>> mapdl.parameters["DEF_Y"]

您还可以使用 :attr:`Mapdl.parameters <ansys.mapdl.core.Mapdl.parameters>` 从 Python 对象设置标量和数组参数：

.. code:: python

   >>> mapdl.parameters["MY_ARRAY"] = np.arange(10000)
   >>> mapdl.parameters["MY_ARRAY"]
   array([0.00000e+00, 1.00000e+00, 2.00000e+00, ..., 9.99997e+05,
          9.99998e+05, 9.99999e+05])

   >>> mapdl.parameters["MY_STRING"] = "helloworld"
   >>> mapdl.parameters["MY_STRING"]
   "helloworld"

您还可以通过 :func:`Mapdl.get() <ansys.mapdl.core.Mapdl.get>` 方法访问的一些内置参数。例如，您可以用以下代码访问当前例程，而不是用 ``\*GET, ACTIVE, 0, ROUT`` 获取：

.. code:: python

  >>> mapdl.parameters.routine
  'Begin level'


有关 ``Parameters`` 类可用方法和属性的完整列表，请参阅 :ref:`ref_parameters_api`。

有关 PyMAPDL 数组限制的更多信息，请参阅 :ref:`Issues when importing and exporting numpy arrays in MAPDL <ref_issues_np_mapdl>`。

.. _ref_special_named_param:

特殊命名的参数
==========================

带前导下划线的参数
-----------------------------------

以下划线 (``'_'``) 开头的参数是 MAPDL 宏和例程的保留参数。不鼓励使用它们，在 PyMAPDL 中也不能直接设置它们。

如果需要设置其中一个参数，可以使用 :attr:`Mapdl._run <ansys.mapdl.core.Mapdl._run>` 属性来避免 PyMAPDL 参数名检查：


.. code:: python

   >>> mapdl._run("_parameter=123")
   'PARAMETER _PARAMETER =     123.00000000'

默认情况下，当发出 :attr:`Mapdl.parameters <ansys.mapdl.core.Mapdl.parameters>` 属性时，无法看到这种类型的参数。不过，您可以将 :attr:`Mapdl.parameters.show_leading_underscore_parameters <ansys.mapdl.core.Mapdl.parameters.show_leading_underscore_parameters>` 设置为 ``True`` ：

.. code:: python

   >>> mapdl.parameters.show_leading_underscore_parameters = True
   >>> mapdl.parameters
   MAPDL Parameters
   ----------------
   PORT                             : 50053.0
   _RETURN                          : 0.0
   _STATUS                          : 0.0
   _UIQR                            : 17.0


带尾随下划线的参数
------------------------------------

以下划线结尾的参数推荐用于用户例程和宏。您可以在 PyMAPDL 中设置这种类型的参数，但默认情况下，在 :attr:`Mapdl.parameters <ansys.mapdl.core.Mapdl.parameters>` 属性中看不到它们，
除非 :attr:`Mapdl.parameters.show_trailing_underscore_parameters <ansys.mapdl.core.Mapdl.parameters.show_trailing_underscore_parameters>` 属性设置为 ``True`` ：


.. code:: python

   >>> mapdl.parameters["param_"] = 1.0
   >>> mapdl.parameters
   MAPDL Parameters
   ----------------
   >>> mapdl.parameters.show_trailing_underscore_parameters = True
   >>> mapdl.parameters
   MAPDL Parameters
   ----------------
   PARAM_                           : 1.0


带前导下划线和尾随下划线的参数
------------------------------------------------

带前导和尾随下划线的参数是一种特殊类型。在任何情况下，都不能在 :attr:`Mapdl.parameters <ansys.mapdl.core.Mapdl.parameters>` 属性中看到这些参数。不建议使用它们。

您仍然可以使用检索参数的任何常规方法来检索这些特殊参数。不过，您必须知道参数名称：


.. code:: python

   >>> mapdl.parameters["_param_"] = 1.0
   >>> mapdl.parameters
   MAPDL Parameters
   ----------------
   >>> print(mapdl.parameters["_param_"])
   1.0

