add_instance_logger
===================

.. py:method:: ff_Logger.add_instance_logger(name, mapdl_instance, level=None)

    为 MAPDL 实例创建日志记录器。

    MAPDL 实例日志记录器是一种带有适配器的日志记录器，可添加上下文信息（如 MAPDL 实例名称）。
    此日志记录器会返回，您可以像使用普通日志记录器一样使用它来记录事件。它也存储在 ``_instances`` 字段中。

    :Return type:
        :class:`Logger`

    :Parameters:

    name : str
        Name for the new logger
    mapdl_instance : ansys.mapdl.core.mapdl.MapdlBase
        Mapdl 实例对象。该对象应包含属性 ``name``。

    :Returns:

    ansys.mapdl.core.logging.PymapdlCustomAdapter
        日志记录器适配器是为在日志中添加 MAPDL 信息而定制的。您可以使用该类来记录事件，方法与使用 logger 类相同。
    
    :Raises:

    Exception
        此方法只能输入字符串作为 ``name`` 。
