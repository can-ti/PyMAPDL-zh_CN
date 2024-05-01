.. _ref_mapdl_user_guide:

==========================
PyMAPDL language and usage
==========================

本页概述了 :class:`Mapdl <ansys.mapdl.core.mapdl.MapdlBase>` 类的 PyMAPDL API。更多信息，请参阅 :ref:`ref_mapdl_api`。

Overview
========

在以函数形式调用 MAPDL 命令时，每个命令都已从其原始的 MAPDL 全大写格式转换为 PEP8 兼容格式。例如， ``ESEL`` 现在是 :func:`Mapdl.esel() <ansys.mapdl.core.Mapdl.esel>` 方法。

.. tab-set::

    .. tab-item:: APDL
        :sync: key1

        .. code:: apdl

            ! Selecting elements whose centroid x coordinate
            ! is between 1 and 2.
            ESEL, S, CENT, X, 1, 2

    .. tab-item:: Python
        :sync: key2

        .. code:: python

            # Selecting elements whose centroid x coordinate
            # is between 1 and 2.
            # returns an array of selected elements ids
            mapdl.esel("S", "CENT", "X", 1, 2)
    

此外，包含 ``/`` 或 ``*`` 的 MAPDL 命令已删除这些字符，除非这会导致与现有名称冲突。
最值得注意的是 ``/SOLU`` ，它会与 ``SOLU`` 冲突。因此， ``/SOLU`` 被重命名为 :func:`Mapdl.slashsolu() <ansys.mapdl.core.Mapdl.slashsolu>` 方法，
以区别于 ``solu``。
在 1500 条 MAPDL 命令中，约有 15 条以 ``斜线 (/)`` 开头， 8 条以 ``星号 (*)`` 开头。


.. tab-set::

    .. tab-item:: APDL
        :sync: key1

        .. code:: apdl

            *STATUS
            /SOLU

    .. tab-item:: Python
        :sync: key2

        .. code:: python

            mapdl.startstatus()
            mapdl.slashsolu()
    

可以接受空格作为参数的 MAPDL 命令，如 ``ESEL,S,TYPE,,1`` ，在被 Python 调用时应包含空字符串，或者，可以使用关键字参数来调用这些命令：

.. tab-set::

    .. tab-item:: APDL
        :sync: key1

        .. code:: apdl

            ESEL,S,TYPE,,1

    .. tab-item:: Python
        :sync: key2

        .. code:: python

            mapdl.esel("s", "type", "", 1)
            mapdl.esel("s", "type", vmin=1)
    

这些限制都不适用于使用 :func:`Mapdl.run() <ansys.mapdl.core.Mapdl.run>` 方法运行的命令。运行这些命令中的某些命令（如 ``"/SOLU"``）可能会更容易：

.. tab-set::

    .. tab-item:: APDL
        :sync: key1

        .. code:: apdl

            /SOLU

    .. tab-item:: Python
        :sync: key2

        .. code:: python

            # 接下来的三个功能是等价的。进入求解处理器。
            mapdl.run("/SOLU")
            mapdl.slashsolu()
            mapdl.solution()


Selecting entities
------------------

您可以使用这些方法选择节点或线条等实体：

* :func:`Mapdl.nsel() <ansys.mapdl.core.Mapdl.nsel>`
* :func:`Mapdl.esel() <ansys.mapdl.core.Mapdl.esel>`
* :func:`Mapdl.ksel() <ansys.mapdl.core.Mapdl.ksel>`
* :func:`Mapdl.lsel() <ansys.mapdl.core.Mapdl.lsel>`
* :func:`Mapdl.asel() <ansys.mapdl.core.Mapdl.asel>`
* :func:`Mapdl.vsel() <ansys.mapdl.core.Mapdl.vsel>`

上述方法会返回所选实体的 ID。例如

.. code:: python

    >>> selected_nodes = mapdl.nsel("S", "NODE", vmin=1, vmax=2000)
    >>> print(selected_nodes)
    array([   1    2    3 ... 1998 1999 2000])

.. code:: python

    >>> mapdl.ksel("all")
    array([1, 2, 3, ..., 1998, 1999, 2000])


Running in non-interactive mode
-------------------------------

有些命令只能在脚本中以非交互方式运行。PyMAPDL 通过将命令写入临时输入文件，然后读取输入文件来绕过这一限制。
要运行一组必须非交互式运行的命令，通过使用 :func:`Mapdl.non_interactive() <ansys.mapdl.core.mapdl.MapdlBase>` 方法，
将 :class:`Mapdl <ansys.mapdl.core.mapdl.MapdlBase>` 类设置为以输入文件的形式运行一系列命令。下面是一个示例：

.. code:: python

    with mapdl.non_interactive:
        mapdl.run("*VWRITE,LABEL(1),VALUE(1,1),VALUE(1,2),VALUE(1,3)")
        mapdl.run("(1X,A8,'   ',F10.1,'  ',F10.1,'   ',1F5.3)")


然后，您可以使用 :attr:`Mapdl.last_response <ansys.mapdl.core.Mapdl.last_response>` 属性查看非交互式上下文的最终响应。

使用 :meth:`Mapdl.non_interactive() <ansys.mapdl.core.Mapdl.non_interactive>` 方法也可以在服务器端运行命令，
而无需 Python 的交互。这可以大大加快速度，但您应该了解 APDL 是如何工作的。关于 PyMAPDL 和 APDL 速度比较的有趣讨论，
请参阅 `PyMAPDL 和 APDL <pymapdl_discussion_speed_pymapdl_mapdl_>`_ 。

应谨慎使用 :meth:`Mapdl.non_interactive() <ansys.mapdl.core.Mapdl.non_interactive>` 方法。

How the non-interactive context manager works
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

在Python中，上下文管理器（context manager）是一种用于管理资源的机制。它提供了一种可靠的方式来打开、使用和关闭资源，无论是否发生异常。上下文管理器通过使用with语句来实现，可以确保资源的正确分配和释放，避免资源泄漏和错误处理的繁琐。
:meth:`Mapdl.non_interactive()<ansys.mapdl.core.Mapdl.non_interactive>` 方法便是通过 `上下文管理器 <python_context_manager_>`_ 实现的，这意味着在进入和退出上下文时会发生一些操作。
进入上下文时，:class:`Mapdl <ansys.mapdl.core.mapdl._MapdlCore>` 实例将停止向 MAPDL 实例发送任何 APDL 命令。
相反，它会为这些 APDL 命令分配一个缓冲区。对于该上下文中的每一条 PyMAPDL 命令，PyMAPDL 都会在该缓冲区中存储相应的 MAPDL 命令。
在退出上下文之前，PyMAPDL 会创建一个包含所有这些 APDL 命令的文本文件，将其发送到 MAPDL 实例，并使用 :meth:`Mapdl.input() <ansys.mapdl.core.Mapdl.input>` 方法运行它。


例如，本示例代码使用 :meth:`non_interactive context <ansys.mapdl.core.Mapdl.non_interactive>` 方法为 MAPDL 生成输入：

.. code:: python

    with mapdl.non_interactive:
        mapdl.nsel("all")
        mapdl.nsel("R", "LOC", "Z", 10)

前面的代码为 MAPDL 生成了这一输入：

.. code:: apdl

    NSEL,ALL   
    NSEL,R,LOC,Z,10

该 MAPLD 输入通过 :meth:`Mapdl.input() <ansys.mapdl.core.Mapdl.input>` 方法调用执行。

由于非交互式上下文直到最后才运行所有命令，你可能会发现在其中与 Python 等进行交互时会出现问题。
例如，在上下文中运行 Python 命令，如 :meth:`Mapdl.get_array() <ansys.mapdl.core.Mapdl.get_array>` 方法，可能会得到不同步的响应。
下面的代码片段就是这类问题的演示：

.. code:: python

    # Create some keypoints
    mapdl.clear()
    mapdl.k(1, 0, 0, 0)
    mapdl.k(2, 1, 0, 0)

    with mapdl.non_interactive:
        mapdl.k(3, 2, 0, 0)
        klist_inside = mapdl.get_array("KP", item1="KLIST")
        # Here is where PyMAPDL sends the commands to the MAPDL instance and execute 'mapdl.k(3,2,0,0)'

    klist_outside = mapdl.get_array("KP", item1="KLIST")

    assert klist_inside != klist_outside  # Evaluates to true 计算结果为true

在前面的脚本中，通过 :meth:`Mapdl.get_array() <ansys.mapdl.core.Mapdl.get_array>` 方法获得的值是不同的：

.. code:: python

    >>> print(klist_inside)
    array([1., 2.])
    >>> print(klist_outside)
    array([1., 2., 3.])

这是因为第一个 :meth:`Mapdl.get_array() <ansys.mapdl.core.Mapdl.get_array>` 方法调用是在 :meth:`Mapdl.k() <ansys.mapdl.core.Mapdl.k>` 方法调用之前执行的。

在使用 :meth:`non_interactive context <ansys.mapdl.core.Mapdl.non_interactive>` 方法时，不应以 Pythonic 方式从 MAPDL 实例获取任何数据。
了解这种行为以及 :meth:`non_interactive context <ansys.mapdl.core.Mapdl.non_interactive>` 方法如何工作，对于 PyMAPDL 的高级使用至关重要。


MAPDL macros
------------

请注意，在 PyMAPDL 中创建的宏 (而不是从文件中加载的宏) 似乎不能正确运行。例如，下面是在 APDL 和 PyMAPDL 中使用 ``*CREATE`` 命令创建的 ``DISP`` 宏：


.. tab-set::

    .. tab-item:: APDL
        :sync: key1

        .. code:: apdl

            ! SELECT NODES AT Z = 10 TO APPLY DISPLACEMENT
            *CREATE,DISP
            NSEL,R,LOC,Z,10
            D,ALL,UZ,ARG1
            NSEL,ALL
            /OUT,SCRATCH
            SOLVE
            *END

            ! Call the function
            *USE,DISP,-.032
            *USE,DISP,-.05
            *USE,DISP,-.1

    .. tab-item:: Python
        :sync: key2

        .. code:: python

            def DISP(
                ARG1="",
                ARG2="",
                ARG3="",
                ARG4="",
                ARG5="",
                ARG6="",
                ARG7="",
                ARG8="",
                ARG9="",
                ARG10="",
                ARG11="",
                ARG12="",
                ARG13="",
                ARG14="",
                ARG15="",
                ARG16="",
                ARG17="",
                ARG18="",
            ):
                mapdl.nsel("R", "LOC", "Z", 10)  # SELECT NODES AT Z = 10 TO APPLY DISPLACEMENT
                mapdl.d("ALL", "UZ", ARG1)
                mapdl.nsel("ALL")
                mapdl.run("/OUT,SCRATCH")
                mapdl.solve()


            DISP(-0.032)
            DISP(-0.05)
            DISP(-0.1)

如果您有一个包含宏的现有输入文件，可以使用 :func:`convert_script() <ansys.mapdl.core.convert_script>` 方法进行转换，同时设置 ``macros_as_functions=True`` ：

.. code:: python

    >>> from ansys.mapdl import core as pymapdl
    >>> pymapdl.convert_script(apdl_inputfile, pyscript, macros_as_functions=True)



Additional options when running commands
----------------------------------------

命令可以在 ``mute`` 或 ``verbose`` 模式下运行，这允许您在运行任何 MAPDL 命令时抑制或打印输出。
这对于像 ``SOLVE`` 这样长时间运行的命令尤其有用。这适用于所有命令的 Pythonic 封装，以及使用 :func:`Mapdl.run() <ansys.mapdl.core.Mapdl.run>` 方法时。


运行命令并抑制其输出：

.. code:: python

    >>> mapdl.run("/PREP7", mute=True)
    >>> mapdl.prep7(mute=True)

运行命令并在其运行时对其输出进行流式处理：

.. code:: python

    >>> mapdl.run("SOLVE", mute=True)
    >>> mapdl.solve(verbose=True)

.. note::
    ``verbose`` 和 ``mute`` 功能仅在以 gRPC 模式运行 MAPDL 时可用。


Running several commands or an input file
-----------------------------------------

您可以使用 :func:`Mapdl.input_strings() <ansys.mapdl.core.Mapdl.input_strings>` 方法将多个 MAPDL 命令作为一个统一的块运行。这在将 PyMAPDL 与旧的 MAPDL 脚本一起使用时非常有用。例如：

.. code:: python

    cmd = """/prep7
    ! Mat
    MP,EX,1,200000
    MP,NUXY,1,0.3
    MP,DENS,1,7.85e-09
    ! Elements
    et,1,186
    ! Geometry
    BLC4,0,0,1000,100,10
    ! Mesh
    esize,5
    vmesh,all"""

.. code:: python

    >>> resp = mapdl.input_strings(cmd)
    >>> resp
    You have already entered the general preprocessor (PREP7).

    MATERIAL          1     EX   =   200000.0

    MATERIAL          1     NUXY =  0.3000000

    MATERIAL          1     DENS =  0.7850000E-08

    ELEMENT TYPE          1 IS SOLID186     3-D 20-NODE STRUCTURAL SOLID
    KEYOPT( 1- 6)=        0      0      0        0      0      0
    KEYOPT( 7-12)=        0      0      0        0      0      0
    KEYOPT(13-18)=        0      0      0        0      0      0

    CURRENT NODAL DOF SET IS  UX    UY    UZ
    THREE-DIMENSIONAL MODEL

    CREATE A HEXAHEDRAL VOLUME WITH
    X-DISTANCES FROM      0.000000000     TO      1000.000000
    Y-DISTANCES FROM      0.000000000     TO      100.0000000
    Z-DISTANCES FROM      0.000000000     TO      10.00000000

        OUTPUT VOLUME =     1

    DEFAULT ELEMENT DIVISIONS PER LINE BASED ON ELEMENT SIZE =   5.00

    GENERATE NODES AND ELEMENTS   IN  ALL  SELECTED VOLUMES

    NUMBER OF VOLUMES MESHED   =         1
    MAXIMUM NODE NUMBER        =     45765
    MAXIMUM ELEMENT NUMBER     =      8000

或者，您可以简单地将命令写入文件，然后使用 :func:`Mapdl.input() <ansys.mapdl.core.Mapdl.input>` 方法运行该文件。例如，如果您有一个从 Ansys Mechanical 生成的 ``"ds.dat"`` 文件，您可以使用以下方法运行该文件：

.. code:: python

    >>> resp = mapdl.input("ds.dat")


条件语句和循环
--------------------------------

APDL 条件语句，如 ``*IF`` 必须用 Python 实现，或使用 :attr:`Mapdl.non_interactive <ansys.mapdl.core.Mapdl.non_interactive>` 属性。例如

.. tab-set::

    .. tab-item:: APDL
        :sync: key1

        .. code:: apdl

            *IF,ARG1,EQ,0,THEN
            *GET,ARG4,NX,ARG2     ! RETRIEVE COORDINATE LOCATIONS OF BOTH NODES
            *GET,ARG5,NY,ARG2
            *GET,ARG6,NZ,ARG2
            *GET,ARG7,NX,ARG3
            *GET,ARG8,NY,ARG3
            *GET,ARG9,NZ,ARG3
            *ELSE
            *GET,ARG4,KX,ARG2     ! RETRIEVE COORDINATE LOCATIONS OF BOTH KEYPOINTS
            *GET,ARG5,KY,ARG2
            *GET,ARG6,KZ,ARG2
            *GET,ARG7,KX,ARG3
            *GET,ARG8,KY,ARG3
            *GET,ARG9,KZ,ARG3
            *ENDIF

    .. tab-item:: Python-Non interactive
        :sync: key3

        .. code:: python

            with mapdl.non_interactive:
                mapdl.run("*IF,ARG1,EQ,0,THEN")
                mapdl.run("*GET,ARG4,NX,ARG2     ")  # RETRIEVE COORDINATE LOCATIONS OF BOTH NODES
                mapdl.run("*GET,ARG5,NY,ARG2")
                mapdl.run("*GET,ARG6,NZ,ARG2")
                mapdl.run("*GET,ARG7,NX,ARG3")
                mapdl.run("*GET,ARG8,NY,ARG3")
                mapdl.run("*GET,ARG9,NZ,ARG3")
                mapdl.run("*ELSE")
                mapdl.run(
                    "*GET,ARG4,KX,ARG2     "
                )  # RETRIEVE COORDINATE LOCATIONS OF BOTH KEYPOINTS
                mapdl.run("*GET,ARG5,KY,ARG2")
                mapdl.run("*GET,ARG6,KZ,ARG2")
                mapdl.run("*GET,ARG7,KX,ARG3")
                mapdl.run("*GET,ARG8,KY,ARG3")
                mapdl.run("*GET,ARG9,KZ,ARG3")
                mapdl.run("*ENDIF")


    .. tab-item:: Python
        :sync: key2

        .. code:: python

            if ARG1 == 0:
                mapdl.get(ARG4, "NX", ARG2)  # RETRIEVE COORDINATE LOCATIONS OF BOTH NODES
                mapdl.get(ARG5, "NY", ARG2)
                mapdl.get(ARG6, "NZ", ARG2)
                mapdl.get(ARG7, "NX", ARG3)
                mapdl.get(ARG8, "NY", ARG3)
                mapdl.get(ARG9, "NZ", ARG3)
            else:
                mapdl.get(ARG4, "KX", ARG2)  # RETRIEVE COORDINATE LOCATIONS OF BOTH KEYPOINTS
                mapdl.get(ARG5, "KY", ARG2)
                mapdl.get(ARG6, "KZ", ARG2)
                mapdl.get(ARG7, "KX", ARG3)
                mapdl.get(ARG8, "KY", ARG3)
                mapdl.get(ARG9, "KZ", ARG3)

参数 ``ARGX`` 的值不会从 MAPDL 实例中获取。因此，除非使用以下命令，否则无法在 Python 代码中使用这些参数：

.. code:: python

   ARG4 = mapdl.parameters["ARG4"]
   ARG5 = mapdl.parameters["ARG5"]
   # ...
   # etc

使用 ``*DO`` 或 ``*DOWHILE`` 的 APDL 循环也应使用 :attr:`Mapdl.non_interactive <ansys.mapdl.core.Mapdl.non_interactive>` 属性或以 Python 方式实现。


Warnings and errors
-------------------
错误以 Pythonical 的方式处理。例如：

.. code:: python

    try:
        mapdl.solve()
    except:
        # do something else with MAPDL
        pass

在 MAPDL 中被忽略的命令会被标记为错误。这与 MAPDL 的默认行为不同，后者将被忽略的命令作为警告处理。例如，在 ``ansys-mapdl-core`` 中，在错误的会话中运行命令会引发错误：

.. code:: python

    >>> mapdl.finish()
    >>> mapdl.k()

    Exception: 
    K, , , , 

     *** WARNING ***                         CP =       0.307   TIME= 11:05:01
     K is not a recognized BEGIN command, abbreviation, or macro.  This      
     command will be ignored.

您可以使用 :func:`Mapdl.ignore_errors() <ansys.mapdl.core.Mapdl.ignore_errors>` 函数来更改此行为，以便将忽略的命令记录为警告而不是异常。例如

.. code:: python

   >>> mapdl.ignore_errors = True
   >>> mapdl.k()  # warning silently ignored


Prompts 提示
------------
来自 MAPDL 的提示会自动继续，就像 MAPDL 处于批处理模式一样。需要用户输入的命令，如 :meth:`Mapdl.vwrite() <ansys.mapdl.core.Mapdl.vwrite>` 方法会失败，必须以非交互方式输入。


APDL command logging
====================
虽然 ``ansys-mapdl-core`` 的设计目的是使通过使用 Python 调用 APDL 会话来控制 APDL 会话变得更容易，但可能有必要使用 PyMAPDL 脚本生成的输入文件再次调用 MAPDL。使用 ``log_apdl="apdl.log"`` 参数可以自动启用这一点。 
启用此参数后，:class:`Mapdl <ansys.mapdl.core.mapdl.MapdlBase>` 类将把运行的每个命令写入活动的 :attr:`Mapdl.directory <ansys.mapdl.core.Mapdl.directory>` 中名为 ``"apdl.log"`` 的日志文件。


例如：

.. code:: python

    >>> from ansys.mapdl.core import launch_mapdl

    >>> ansys = launch_mapdl(log_apdl="apdl.log")
    >>> ansys.prep7()
    >>> ansys.k(1, 0, 0, 0)
    >>> ansys.k(2, 1, 0, 0)
    >>> ansys.k(3, 1, 1, 0)
    >>> ansys.k(4, 0, 1, 0)

这段代码会将以下内容写入 ``"apdl.log"`` 文件：

.. code:: apdl

    /PREP7,
    K,1,0,0,0
    K,2,1,0,0
    K,3,1,1,0
    K,4,0,1,0

除条件语句、循环或函数外，这允许将 Python 脚本转换为 APDL 脚本。

Use the ``lgwrite`` method
--------------------------
另外，如果只需要数据库命令输出，可以使用 :func:`Mapdl.lgwrite <Mapdl.ansys.mapdl.core.Mapdl.lgwrite>` 方法将整个数据库命令日志写入文件。


Interactive breakpoint 交互式断点
====================================

在大多数情况下，有必要或最好打开 MAPDL GUI。:class:`Mapdl <ansys.mapdl.core.mapdl.MapdlBase>` 类有 :func:`Mapdl.open_gui() <ansys.mapdl.core.Mapdl.open_gui>` 方法，
它允许您无缝地打开图形用户界面，而不会丢失工作或重新启动会话。例如

.. code:: python

    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl()

使用关键点创建正方形区域

.. code:: python

    >>> mapdl.prep7()
    >>> mapdl.k(1, 0, 0, 0)
    >>> mapdl.k(2, 1, 0, 0)
    >>> mapdl.k(3, 1, 1, 0)
    >>> mapdl.k(4, 0, 1, 0)
    >>> mapdl.l(1, 2)
    >>> mapdl.l(2, 3)
    >>> mapdl.l(3, 4)
    >>> mapdl.l(4, 1)
    >>> mapdl.al(1, 2, 3, 4)

打开图形用户界面

.. code:: python

    >>> mapdl.open_gui()

从上次中断的地方继续

.. code:: python

    >>> mapdl.et(1, "MESH200", 6)
    >>> mapdl.amesh("all")
    >>> mapdl.eplot()

这种方法避免了在交互会话和脚本会话之间来回切换的麻烦。相反，你可以使用一个脚本会话，
然后从脚本会话中打开图形用户界面，而不会丢失工作或进度。此外，在图形用户界面中进行的任何更改都不会影响脚本。
您可以在图形用户界面中进行实验，而脚本则不受影响。


Run a batch job
===============
您可以定义一个运行 MAPDL 的函数，而不是通过调用输入文件来运行 MAPDL 批处理。此示例根据扭转载荷下圆柱体的最大应力运行网格收敛研究。

.. code:: python

    import numpy as np
    from ansys.mapdl.core import launch_mapdl


    def cylinder_batch(elemsize, plot=False):
        """报告悬臂支撑圆柱体的最大 von Mises 应力"""

        # clear
        mapdl.finish()
        mapdl.clear()

        # cylinder parameters
        radius = 2
        h_tip = 2
        height = 20
        force = 100 / radius
        pressure = force / (h_tip * 2 * np.pi * radius)

        mapdl.prep7()
        mapdl.et(1, 186)
        mapdl.et(2, 154)
        mapdl.r(1)
        mapdl.r(2)

        # Aluminum(铝) properties (or something)
        mapdl.mp("ex", 1, 10e6)
        mapdl.mp("nuxy", 1, 0.3)
        mapdl.mp("dens", 1, 0.1 / 386.1)
        mapdl.mp("dens", 2, 0)

        # Simple cylinder
        for i in range(4):
            mapdl.cylind(radius, "", "", height, 90 * (i - 1), 90 * i)

        mapdl.nummrg("kp")

        # mesh cylinder
        mapdl.lsel("s", "loc", "x", 0)
        mapdl.lsel("r", "loc", "y", 0)
        mapdl.lsel("r", "loc", "z", 0, height - h_tip)
        # mapdl.lesize('all', elemsize*2)
        mapdl.mshape(0)
        mapdl.mshkey(1)
        mapdl.esize(elemsize)
        mapdl.allsel("all")
        mapdl.vsweep("ALL")
        mapdl.csys(1)
        mapdl.asel("s", "loc", "z", "", height - h_tip + 0.0001)
        mapdl.asel("r", "loc", "x", radius)
        mapdl.local(11, 1)
        mapdl.csys(0)
        mapdl.aatt(2, 2, 2, 11)
        mapdl.amesh("all")
        mapdl.finish()

        if plot:
            mapdl.view(1, 1, 1, 1)
            mapdl.eplot()

        # new solution
        mapdl.slashsolu()
        mapdl.antype("static", "new")
        mapdl.eqslv("pcg", 1e-8)

        # Apply tangential pressure 施加切向压力
        mapdl.esel("s", "type", "", 2)
        mapdl.sfe("all", 2, "pres", "", pressure)

        # Constrain bottom of cylinder/rod
        mapdl.asel("s", "loc", "z", 0)
        mapdl.nsla("s", 1)

        mapdl.d("all", "all")
        mapdl.allsel()
        mapdl.psf("pres", "", 2)
        mapdl.pbc("u", 1)
        mapdl.solve()
        mapdl.finish()

        # access results using MAPDL object 使用 MAPDL 对象访问结果
        result = mapdl.result

        # 要访问您可以运行的结果，请执行以下操作：
        # from ansys.mapdl import reader as pymapdl_reader
        # resultfile = os.path.join(mapdl.path, '%s.rst' % mapdl.jobname)
        # result = pymapdl_reader.read_binary(result file)

        # 获取结果 1 处的最大 von Mises 应力
        # Index 0 as it's zero based indexing
        nodenum, stress = result.principal_nodal_stress(0)

        # von Mises 应力是最后一列
        # 必须为 nanmax，因为没有记录壳单元应力
        maxstress = np.nanmax(stress[:, -1])

        # 返回节点数和最大应力
        return nodenum.size, maxstress


    # 初始化 MAPDL
    mapdl = launch_mapdl(override=True, loglevel="ERROR")

    # 调用 MAPDL 反复求解
    result_summ = []
    for elemsize in np.linspace(0.6, 0.15, 15):
        # 运行批处理并报告结果
        nnode, maxstress = cylinder_batch(elemsize, plot=False)
        result_summ.append([nnode, maxstress])
        print(
            "Element size %f: %6d nodes and maximum vom Mises stress %f"
            % (elemsize, nnode, maxstress)
        )

    # Exit MAPDL
    mapdl.exit()

下面是脚本的输出结果：

.. code:: output

    Element size 0.600000:   9657 nodes and maximum vom Mises stress 142.623505
    Element size 0.567857:  10213 nodes and maximum vom Mises stress 142.697800
    Element size 0.535714:  10769 nodes and maximum vom Mises stress 142.766510
    Element size 0.503571:  14177 nodes and maximum vom Mises stress 142.585388
    Element size 0.471429:  18371 nodes and maximum vom Mises stress 142.825684
    Element size 0.439286:  19724 nodes and maximum vom Mises stress 142.841202
    Element size 0.407143:  21412 nodes and maximum vom Mises stress 142.945984
    Element size 0.375000:  33502 nodes and maximum vom Mises stress 142.913437
    Element size 0.342857:  37877 nodes and maximum vom Mises stress 143.033401
    Element size 0.310714:  59432 nodes and maximum vom Mises stress 143.328842
    Element size 0.278571:  69106 nodes and maximum vom Mises stress 143.176086
    Element size 0.246429: 110547 nodes and maximum vom Mises stress 143.499329
    Element size 0.214286: 142496 nodes and maximum vom Mises stress 143.559128
    Element size 0.182143: 211966 nodes and maximum vom Mises stress 143.953430
    Element size 0.150000: 412324 nodes and maximum vom Mises stress 144.275406


Chain commands in MAPDL
=======================

MAPDL 通过使用分隔符 ``"$"`` 允许在一行中执行多个命令。在 PyMAPDL 中，可以有效地将多个命令链在一起，然后发送给 MAPDL 执行，
而不是单独执行。当你需要在一个 Python 循环中执行数千条命令，而不需要每条命令的单独结果时，命令链会很有帮助。
例如，如果您想沿 X 轴创建 1000 个关键点，您可以运行：

.. code:: python

    xloc = np.linspace(0, 1, 1000)
    for x in xloc:
        mapdl.k(x=x)


但是，由于每条命令都是单独执行并返回响应的，因此将要由 MAPDL 执行的命令分组发送，
并让 :class:`Mapdl <ansys.mapdl.core.mapdl.MapdlBase>` 类通过使用 :attr:`Mapdl.chain_commands <ansys.mapdl.core.Mapdl.chain_commands>` 属性来处理命令分组会更快。

.. code:: python

    xloc = np.linspace(0, 1, 1000)
    with mapdl.chain_commands:
        for x in xloc:
            mapdl.k(x=x)

使用这种方法的执行时间通常比单独运行每条命令快 4 到 10 倍。然后，您可以使用 :attr:`Mapdl.last_response <ansys.mapdl.core.Mapdl.last_response>` 属性查看链式命令的最终响应。

.. note::
   分布式 MAPDL 不支持命令链。为提高性能，请使用 ``mute=True`` 或 :attr:`Mapdl.non_interactive <ansys.mapdl.core.Mapdl.non_interactive>` 上下文管理器。


Sending arrays to MAPDL
=======================

您可以使用 :attr:`Mapdl.Parameters <ansys.mapdl.core.Mapdl.parameters>` 属性直接向 MAPDL 发送 ``numpy`` 数组或 Python 列表。
这比使用 :func:`Mapdl.run() <ansys.mapdl.core.Mapdl.run>` 方法通过 Python 单独向 MAPDL 发送参数要有效得多，因为它在幕后使用了 :func:`Mapdl.vread() <ansys.mapdl.core._commands.ParameterDefinition>` 方法。

.. code:: python

    from ansys.mapdl.core import launch_mapdl
    import numpy as np

    mapdl = launch_mapdl()
    arr = np.random.random((5, 3))
    mapdl.parameters["MYARR"] = arr

通过索引 :attr:`Mapdl.Parameters <ansys.mapdl.core.Mapdl.parameters>` 属性（就像 Python 字典一样），验证数据是否已正确加载到 MAPDL：

.. code:: python

   >>> array_from_mapdl = mapdl.parameters["MYARR"]
   >>> array_from_mapdl
   array([[0.65516567, 0.96977939, 0.3224993 ],
          [0.58634927, 0.84392263, 0.18152529],
          [0.76719759, 0.45748876, 0.56432361],
          [0.78548338, 0.01042177, 0.57420062],
          [0.33189362, 0.9681039 , 0.47525875]])


Download a remote MAPDL file
----------------------------
在 gRPC 模式下运行 MAPDL 时，可以使用 :class:`Mapdl <ansys.mapdl.core.mapdl.MapdlBase>` 类
和 :func:`Mapdl.download() <ansys.mapdl.core.mapdl_grpc.MapdlGrpc.download>` 函数列出并下载远程 MAPDL 文件。例如，以下代码列出了远程文件并下载了其中一个：

.. code:: python

    remote_files = mapdl.list_files()

    # 确保结果文件是远程文件之一
    assert "file.rst" in remote_files # assert(声明)

    # 下载远程结果文件
    mapdl.download("file.rst")

.. note::

   该功能仅适用于 MAPDL 2021 R1 及更高版本。

或者，您可以使用 glob 模式或 :func:`Mapdl.download() <ansys.mapdl.core.mapdl_grpc.MapdlGrpc.download>` 方法中的文件名列表一次性下载多个文件：

.. code:: python

    # 使用文件名列表
    mapdl.download(["file0.log", "file1.out"])

    # 使用 glob 模式匹配文件列表
    mapdl.download("file*")

您还可以使用此函数下载 MAPDL 工作目录（:func:`Mapdl.directory <ansys.mapdl.core.Mapdl.directory>` ）中的所有文件：

.. code:: python

    mapdl.download_project()

或者按扩展名过滤，如本例所示：

.. code:: python

    mapdl.download_project(
        ["log", "out"], target_dir="myfiles"
    )  # Download the files to 'myfiles' directory


Upload a local MAPDL file
-------------------------
您可以使用 :func:`Mapdl.upload() <ansys.mapdl.core.mapdl_grpc.MapdlGrpc.upload>` 方法将本地 MAPDL 文件作为远程 MAPDL 实例上传：

.. code:: python

    # upload a local file
    mapdl.upload("sample.db")

    # ensure the uploaded file is one of the remote files
    remote_files = mapdl.list_files()
    assert "sample.db" in remote_files

.. note::

   该功能仅适用于 MAPDL 2021 R1 及更高版本。


不支持的 MAPDL 命令及其他注意事项
===================================================
大多数 MAPDL 命令都已通过 Python 映射到相应的方法中。但是，有些命令不支持，因为它们不适用于交互会话，或者它们需要额外的命令，而这些命令与 MAPDL 服务器处理输入的方式不兼容。


.. _ref_unsupported_commands:

不可用的命令
--------------------
由于各种原因，有些命令在 PyMAPDL 中不可用。

其中有些命令在 Python 环境中没有意义。下面是一些例子：

- 可以用 Python ``input`` 代替 ``*ASK`` 命令。
- 可以用 Python ``if`` 语句代替 ``*IF`` 命令。
- 可以调用另一个 Python 函数或模块来代替 ``*CREATE`` 和 ``*USE`` 命令。


其他命令在非图形用户界面会话中没有意义。例如，在非图形用户界面会话中不需要清除图形屏幕的 ``/ERASE`` 和 ``ERASE`` 命令。

其他命令会被 MAPDL 忽略，但您仍然可以使用它们。例如，可以使用 :func:`mapdl.run("/BATCH") <ansys.mapdl.core.Mapdl.run>` 方法运行 ``/BATCH`` 命令，该方法会返回以下警告：

.. code:: output

    *** WARNING ***                         CP =       0.519   TIME= 12:04:16
    The /BATCH command must be the first line of input.  The /BATCH command
    is ignored.



Table-1_ 关于无法使用的命令的全面信息

.. _Table-1:

**Table 1. Non-available commands.**

.. table:: 
  :class: longtable

  +---------------------------+-------------------+------------------------+-----------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
  |                           | MAPDL command     | Interactive            | Non-interactive                         | Direct run                                   | Notes                                                                                                                                                   |
  +===========================+===================+========================+=========================================+==============================================+=========================================================================================================================================================+
  | **GUI commands**          | * ``*ASK``        | |:x:| Not available    | |:x:| Not available                     | |:heavy_check_mark:| Works                   | When used in :func:`mapdl.run() <ansys.mapdl.core.Mapdl.run>` it automatically assumes the user input is 0. Use Python ``input`` instead.               |
  |                           +-------------------+------------------------+-----------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
  |                           | * ``*VEDIT``      | |:x:| Not available    | |:x:| Not available                     | |:heavy_minus_sign:| MAPDL shows a warning   | It requires a GUI session to work.                                                                                                                      |
  |                           +-------------------+------------------------+-----------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
  |                           | * ``/ERASE``      | |:x:| Not available    | |:x:| Not available                     | |:heavy_check_mark:| Works                   | It does not make sense in a non-GUI session.                                                                                                            |
  |                           +-------------------+------------------------+-----------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
  |                           | * ``ERASE``       | |:x:| Not available    | |:x:| Not available                     | |:heavy_minus_sign:| MAPDL shows a warning   | It does not make sense in a non-GUI session.                                                                                                            |
  |                           +-------------------+------------------------+-----------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
  |                           | * ``HELP``        | |:x:| Not available    | |:x:| Not available                     | |:heavy_minus_sign:| Ignored by MAPDL        | It requires a GUI session to work.                                                                                                                      |
  |                           +-------------------+------------------------+-----------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
  |                           | * ``HELPDISP``    | |:x:| Not available    | |:x:| Not available                     | |:heavy_minus_sign:| Ignored by MAPDL        | It requires a GUI session to work.                                                                                                                      |
  |                           +-------------------+------------------------+-----------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
  |                           | * ``NOERASE``     | |:x:| Not available    | |:x:| Not available                     | |:heavy_check_mark:| Works                   | It does not make sense in a non-GUI session.                                                                                                            |
  +---------------------------+-------------------+------------------------+-----------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
  | **Control flow commands** | * ``*CYCLE``      | |:x:| Not available    | |:x:| Not available                     | |:heavy_check_mark:| Works                   | It is recommended to use Python control flow keywords, in this case ``continue``.                                                                       |
  |                           +-------------------+------------------------+-----------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
  |                           | * ``*DO``         | |:x:| Not available    | |:x:| Not available                     | |:heavy_check_mark:| Works                   | It is recommended to use Python control flow keywords, in this case ``for``.                                                                            |
  |                           +-------------------+------------------------+-----------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
  |                           | * ``*DOWHILE``    | |:x:| Not available    | |:x:| Not available                     | |:heavy_check_mark:| Works                   | It is recommended to use Python control flow keywords, in this case ``while``.                                                                          |
  |                           +-------------------+------------------------+-----------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
  |                           | * ``*ELSE``       | |:x:| Not available    | |:x:| Not available                     | |:heavy_check_mark:| Works                   | It is recommended to use Python control flow keywords, in this case ``else``.                                                                           |
  |                           +-------------------+------------------------+-----------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
  |                           | * ``*ELSEIF``     | |:x:| Not available    | |:x:| Not available                     | |:heavy_check_mark:| Works                   | It is recommended to use Python control flow keywords, in this case ``elif``.                                                                           |
  |                           +-------------------+------------------------+-----------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
  |                           | * ``*ENDDO``      | |:x:| Not available    | |:x:| Not available                     | |:heavy_check_mark:| Works                   | It is recommended to use Python control flow keywords.                                                                                                  |
  |                           +-------------------+------------------------+-----------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
  |                           | * ``*GO``         | |:x:| Not available    | |:x:| Not available                     | |:heavy_check_mark:| Works                   | It is recommended to use Python control flow keywords, such as ``if`` or functions.                                                                     |
  |                           +-------------------+------------------------+-----------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
  |                           | * ``*IF``         | |:x:| Not available    | |:x:| Not available                     | |:heavy_check_mark:| Works                   | It is recommended to use Python control flow keywords, in this case ``continue``.                                                                       |
  |                           +-------------------+------------------------+-----------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
  |                           | * ``*REPEAT``     | |:x:| Not available    | |:x:| Not available                     | |:heavy_check_mark:| Works                   | It is recommended to use Python control flow keywords such as ``for`` or ``while``                                                                      |
  |                           +-------------------+------------------------+-----------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
  |                           | * ``*RETURN``     | |:x:| Not available    | |:x:| Not available                     | |:heavy_check_mark:| Works                   | It is recommended to use Python control flow keywords such as ``break``, ``continue`` or ``return``                                                     |
  +---------------------------+-------------------+------------------------+-----------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
  | **Others commands**       | * ``*DEL``        | |:x:| Not available    | |:x:| Not available                     | |:heavy_check_mark:| Works                   | It is recommended to use Python variables (use Python memory) instead of MAPDL variables.                                                               |
  |                           +-------------------+------------------------+-----------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
  |                           | * ``/BATCH``      | |:x:| Not available    | |:x:| Not available                     | |:heavy_minus_sign:| Ignored by MAPDL.       | It does not make sense in a PyMAPDL session.                                                                                                            |
  |                           +-------------------+------------------------+-----------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
  |                           | * ``/EOF``        | |:x:| Not available    | |:x:| Not available                     | |:x:| PyMAPDL shows an exception             | To stop the server, use :func:`mapdl.exit() <ansys.mapdl.core.Mapdl.exit>`                                                                              |
  |                           +-------------------+------------------------+-----------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
  |                           | * ``UNDO``        | |:x:| Not available    | |:x:| Not available                     | |:heavy_minus_sign:| MAPDL shows a warning   | It does not undo any command.                                                                                                                           |
  +---------------------------+-------------------+------------------------+-----------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+


.. note::
    * **Interactive（交互式）** 是指 MAPDL 中有一个方法，例如 :func:`Mapdl.prep7() <ansys.mapdl.core.Mapdl.prep7>` 方法。
    * **Non-interactive** 表示在 :attr:`Mapdl.non_interactive <ansys.mapdl.core.Mapdl.non_interactive>` 上下文块、 :func:`Mapdl.input() <ansys.mapdl.core.Mapdl.input>` 方法或 :func:`Mapdl.input_strings() <ansys.mapdl.core.Mapdl.input_strings>` 方法中运行。例如

      .. code:: python

          with mapdl.non_interactive:
              mapdl.prep7()

    * **Direct run** 是指使用 :func:`mapdl.run() <ansys.mapdl.core.Mapdl.run>` 方法来运行 MAPDL 命令。
      例如 :func:`mapdl.run("/PREP7") <ansys.mapdl.core.Mapdl.run>` 方法。


请注意，使用 :func:`mapdl.run() <ansys.mapdl.core.Mapdl.run>` 方法运行这些命令不会导致 MAPDL 退出。但是，它可能会引发异常。

这些 MAPDL 命令也可以使用 :func:`mapdl.input() <ansys.mapdl.core.Mapdl.input>` 方法或 :func:`mapdl.input_strings() <ansys.mapdl.core.Mapdl.input_strings>` 方法执行。结果应与在正常批处理 MAPDL 会话中运行相同。


.. _ref_unsupported_interactive_commands:

不支持的 "交互式" 命令
----------------------------------

以下命令只能在非交互模式下运行（在 :attr:`Mapdl.non_interactive <ansys.mapdl.core.Mapdl.non_interactive>` 块内或使用 :func:`mapdl.input() <ansys.mapdl.core.Mapdl.input>` 方法）。

Table-2_ 提供有关不受支持的“交互式”命令的全面信息。


.. _Table-2:

**Table 2. Non-interactive only commands.**

+---------------+---------------------------------------------------------------------------------------------------------------------------------+----------------------------------+----------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------+
|               | Interactive                                                                                                                     | Non-interactive                  | Direct Run                                                                                                           | Notes                                                                                               |
+===============+=================================================================================================================================+==================================+======================================================================================================================+=====================================================================================================+
| * ``*CREATE`` | |:x:| Not available                                                                                                             | |:heavy_check_mark:| Available   | |:heavy_minus_sign:| Only in :attr:`Mapdl.non_interactive <ansys.mapdl.core.Mapdl.non_interactive>`                  | It is recommended to create Python functions instead.                                               |
+---------------+---------------------------------------------------------------------------------------------------------------------------------+----------------------------------+----------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------+
| * ``CFOPEN``  | |:x:| Not available                                                                                                             | |:heavy_check_mark:| Available   | |:heavy_minus_sign:| Only in :attr:`Mapdl.non_interactive <ansys.mapdl.core.Mapdl.non_interactive>`                  | It is recommended to use Python functions such as ``open``.                                         |
+---------------+---------------------------------------------------------------------------------------------------------------------------------+----------------------------------+----------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------+
| * ``CFCLOSE`` | |:x:| Not available                                                                                                             | |:heavy_check_mark:| Available   | |:heavy_minus_sign:| Only in :attr:`Mapdl.non_interactive <ansys.mapdl.core.Mapdl.non_interactive>`                  | It is recommended to use Python functions such as ``open``.                                         |
+---------------+---------------------------------------------------------------------------------------------------------------------------------+----------------------------------+----------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------+
| * ``*VWRITE`` | |:x:| Not available                                                                                                             | |:heavy_check_mark:| Available   | |:heavy_minus_sign:| Only in :attr:`Mapdl.non_interactive <ansys.mapdl.core.Mapdl.non_interactive>`                  | If you are working in a local session, it is recommended you use Python function such as ``open``.  |
+---------------+---------------------------------------------------------------------------------------------------------------------------------+----------------------------------+----------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------+
| * ``LSWRITE`` | |:heavy_check_mark:| Available (Internally running in :attr:`Mapdl.non_interactive <ansys.mapdl.core.Mapdl.non_interactive>`)   | |:heavy_check_mark:| Available   | |:heavy_minus_sign:| Only in :attr:`Mapdl.non_interactive <ansys.mapdl.core.Mapdl.non_interactive>`                  |                                                                                                     |
+---------------+---------------------------------------------------------------------------------------------------------------------------------+----------------------------------+----------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------+


环境变量
=====================

有几个 PyMAPDL 特定的环境变量可以用来控制 PyMAPDL 和 MAPDL 的行为或启动。下表列出了这些变量：

+---------------------------------------+---------------------------------------------------------------------+
| :envvar:`PYMAPDL_START_INSTANCE`      | Override the behavior of the                                        |
|                                       | :func:`ansys.mapdl.core.launcher.launch_mapdl` function             |
|                                       | to only attempt to connect to existing                              |
|                                       | instances of PyMAPDL. Generally used                                |
|                                       | in combination with ``PYMAPDL_PORT``.                               |
|                                       |                                                                     |
|                                       | **Example:**                                                        |
|                                       |                                                                     |
|                                       | .. code:: console                                                   |
|                                       |                                                                     |
|                                       |    export PYMAPDL_START_INSTANCE=True                               |
|                                       |                                                                     |
+---------------------------------------+---------------------------------------------------------------------+
| :envvar:`PYMAPDL_PORT`                | Default port for PyMAPDL to connect to.                             |
|                                       |                                                                     |
|                                       | **Example:**                                                        |
|                                       |                                                                     |
|                                       | .. code:: console                                                   |
|                                       |                                                                     |
|                                       |    export PYMAPDL_PORT=50052                                        |
|                                       |                                                                     |
+---------------------------------------+---------------------------------------------------------------------+
| :envvar:`PYMAPDL_IP`                  | Default IP for PyMAPDL to connect to.                               |
|                                       |                                                                     |
|                                       | **Example:**                                                        |
|                                       |                                                                     |
|                                       | .. code:: console                                                   |
|                                       |                                                                     |
|                                       |    export PYMAPDL_IP=123.45.67.89                                   |
|                                       |                                                                     |
+---------------------------------------+---------------------------------------------------------------------+
| :envvar:`ANSYSLMD_LICENSE_FILE`       | License file or IP address with port in the format                  |
|                                       | ``PORT@IP``. Do not confuse with the ``IP`` and                     |
|                                       | ``PORT`` where the MAPDL instance is running, which                 |
|                                       | are specified using :envvar:`PYMAPDL_IP` and                        |
|                                       | :envvar:`PYMAPDL_PORT`.                                             |
|                                       | This is helpful for supplying licensing for                         |
|                                       | Docker.                                                             |
|                                       |                                                                     |
|                                       | **Example:**                                                        |
|                                       |                                                                     |
|                                       | .. code:: console                                                   |
|                                       |                                                                     |
|                                       |    export ANSYSLMD_LICENSE_FILE=1055@123.45.67.89                   |
|                                       |                                                                     |
+---------------------------------------+---------------------------------------------------------------------+
| :envvar:`PYMAPDL_MAPDL_EXEC`          | Executable path from where to launch MAPDL                          |
|                                       | instances.                                                          |
|                                       |                                                                     |
|                                       | **Example:**                                                        |
|                                       |                                                                     |
|                                       | .. code:: console                                                   |
|                                       |                                                                     |
|                                       |    export PYMAPDL_MAPDL_EXEC=/ansys_inc/v222/ansys/bin/mapdl        |
|                                       |                                                                     |
+---------------------------------------+---------------------------------------------------------------------+
| :envvar:`PYMAPDL_MAPDL_VERSION`       | Default MAPDL version to launch in case there                       |
|                                       | are several versions availables.                                    |
|                                       |                                                                     |
|                                       | **Example:**                                                        |
|                                       |                                                                     |
|                                       | .. code:: console                                                   |
|                                       |                                                                     |
|                                       |    export PYMAPDL_MAPDL_VERSION=22.2                                |
|                                       |                                                                     |
+---------------------------------------+---------------------------------------------------------------------+
| :envvar:`PYMAPDL_MAX_MESSAGE_LENGTH`  | Maximum gRPC message length. If your                                |
|                                       | connection terminates when running                                  |
|                                       | PRNSOL or NLIST, raise this. In bytes,                              |
|                                       | defaults to 256 MB.                                                 |
|                                       |                                                                     |
|                                       | Only for developing purposes.                                       |
+---------------------------------------+---------------------------------------------------------------------+