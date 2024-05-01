close_all_local_instances
=========================

.. py:function:: ff_ansys.mapdl.core.launcher.close_all_local_instances(port_range=None)

    关闭 ``port_range`` 内的所有 MAPDL 实例。

    该功能可用于清理失败的池或批运行。

    :Parameters:

    port_range : :class:`list` , :class:`optional`
        默认为 ``range(50000, 50200)``。如果在 gRPC 模式下有许多潜在的 MAPDL 实例，请扩大此范围。

    :Examples:

    Close all instances on in the range of 50000 and 50199.

    >>> import ansys.mapdl.core as pymapdl
    >>> pymapdl.close_all_local_instances()

    """