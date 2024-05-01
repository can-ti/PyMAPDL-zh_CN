Translate scripts
===================

`ansys-mapdl-core <pymapdl_docs_>`_ 库包含一些将现有 MAPDL 脚本转换为 PyMAPDL 脚本的基本函数。理想情况下，所有数学运算和变量设置都在 Python 中进行，因为 APDL 命令的透明度较低，调试起来较为困难。


.. _ref_cli_converter:

命令行界面
----------------------

在 PyMAPDL v0.64.0 及更高版本中，您可以通过命令行使用转换器。按照 :ref:`install_mapdl` 中的说明激活并安装软件包后，就可以从终端使用转换器了。下面是使用 ``pymapdl_convert_script`` 命令的方法：

.. code:: console

    $ pymapdl_convert_script mapdl.dat -o python.py

    File mapdl.dat successfully converted to python.py.

要获取有关转换器用法、选项和示例的帮助，请键入此命令：

.. code:: console

    $ pymapdl_convert_script --help

    Usage: pymapdl_convert_script [OPTIONS] FILENAME_IN

    PyMAPDL CLI tool for converting MAPDL scripts to PyMAPDL scripts.

    USAGE:

    ...

``pymapdl_convert_script`` 命令使用 :func:`convert_script() <ansys.mapdl.core.convert_script>` 函数。因此，该命令接受该函数的大部分参数。

Usage
~~~~~

您可以使用不同的参数从终端调用该命令。下面是一个将 ``mapdl.dat`` 文件转换为名为 ``python.py`` 的 Python 文件的示例：

.. code:: console
    
    $ pymapdl_convert_script mapdl.dat -o python.py

    File mapdl.dat successfully converted to python.py.

输出参数完全是可选的。如果不指定，输出的文件将使用 ``py`` 扩展名：

.. code:: console

    $ pymapdl_convert_script mapdl.dat

    File mapdl.dat successfully converted to mapdl.py.

您可以使用 :func:`convert_script() <ansys.mapdl.core.convert_script>` 函数中的任何选项。

例如，要避免在运行脚本后退出 MAPDL 实例，可以使用 ``--auto-exit`` 参数：

.. code:: console

    $ pymapdl_convert_script mapdl.dat --auto-exit False

    File mapdl.dat successfully converted to mapdl.py.

通过将 ``--add_imports`` 选项设置为 ``False`` 可以跳过导入：

.. code:: console

    $ pymapdl_convert_script mapdl.dat --filename_out mapdl.out --add_imports
    False

    File mapdl.dat successfully converted to mapdl.out.

有关可能选项的更多信息，请使用 help 命令 (`pymapdl_convert_script --help``) 或 :func:`convert_script() <ansys.mapdl.core.convert_script>` 函数文档。

Caveats
~~~~~~~

这些示例仅显示了验证文件的自动转换，而非优化代码。如果需要从 Ansys 提取参数或数组，请使用 :func:`Mapdl.get_value() <ansys.mapdl.core.Mapdl.get_value>` 函数，
该函数与此处显示的 MAPDL :func:`Mapdl.get() <ansys.mapdl.core.Mapdl.get>` 命令非常相似：

.. code:: pycon

   >>> mapdl.get_value("NODE", 2, "U", "Y")
   4.532094298033

或者，如果已经定义了参数，可以使用 :attr:`Mapdl.parameters <ansys.mapdl.core.Mapdl.parameters>` 属性访问该参数：

.. code:: pycon

    >>> mapdl.parameters
    ARR                              : ARRAY DIM (3, 1, 1)
    PARM_FLOAT                       : 20.0
    PARM_INT                         : 10.0
    PARM_LONG_STR                    : "stringstringstringstringstringst"
    PARM_STR                         : "string"
    DEF_Y                            : 4.532094298033

    >>> mapdl.parameters["DEF_Y"]
    4.532094298033


Script translation
~~~~~~~~~~~~~~~~~~

可以使用 :func:`convert_script() <ansys.mapdl.core.convert_script>` 函数转换现有的 Ansys 脚本：

.. code:: pycon

    >>> import ansys.mapdl.core as pymapdl
    >>> inputfile = "ansys_inputfile.inp"
    >>> pyscript = "pyscript.py"
    >>> pymapdl.convert_script(inputfile, pyscript)

或者，您可以使用 :func:`convert_apdl_block() <ansys.mapdl.core.convert_apdl_block>` 函数将代码转换为字符串形式，以便稍后处理：


.. code:: python

    from ansys.mapdl.core.convert import convert_apdl_block

    apdl_string = """/com, This is a block of APDL commands.
    /PREP7
    N,,0,0,0
    N,,0,0,1
    FINISH"""
    pycode = convert_apdl_block(apdl_string)  # apdl_string 也可以是一个字符串列表。


脚本转换函数允许一些有趣的参数，您可以在各自的 :func:`convert_script() <ansys.mapdl.core.convert_script>` 和 :func:`convert_apdl_block() <ansys.mapdl.core.convert_apdl_block>` 函数文档中看到。
特别有趣的是 ``add_imports`` 、 ``comment_solve`` 和 ``print_com`` 关键字参数。

以下示例中特别值得注意的是，大多数命令都可以作为方法调用到 Ansys 对象，而不是作为命令发送字符串。
此外，请注意某些命令需要 :attr:`Mapdl.non_interactive <ansys.mapdl.core.Mapdl.non_interactive>` 上下文管理器，
因为某些命令需要并可能会破坏某些接口（如 CORBA）的服务器连接，或者是无效的（如 gRPC）。

还请注意，使用 ``*CREATE`` 的 APDL 宏已被 Python 函数取代。这样，如果需要在脚本中插入 ``breakpoint()`` 时，代码会更容易调试。


Example: VM1 - 超静定问题反作用力分析
---------------------------------------------------------------

Ansys MAPDL 包含 200 多个验证文件，用于 Ansys 验证和演示。这些验证文件用于演示 PyMAPDL 文件转换 :func:`convert_script() <ansys.mapdl.core.convert_script>` 函数的使用，可在以下文件中找到：

.. code:: pycon

    >>> from ansys.mapdl.core import examples
    >>> examples.vmfiles["vm1"]
    '.../ansys/mapdl/core/examples/verif/vm1.dat'

此示例转换验证示例 ``"vm1.dat"`` 。

首先是 MAPDL 代码：

.. code:: apdl

    /COM, 'ANSYS MEDIA REL. 150 (11/8/2013) REF. VERIF. MANUAL: REL. 150'
    /VERIFY, VM1
    /PREP7
    /TITLE,'  VM1, STATICALLY INDETERMINATE REACTION FORCE ANALYSIS'
    /COM,'      STR. OF MATL., TIMOSHENKO, PART 1, 3RD ED., PAGE 26, PROB.10'
    ANTYPE, STATIC                  ! STATIC ANALYSIS
    ET, 1, LINK180
    SECTYPE, 1, LINK
    SECDATA, 1  			       ! CROSS SECTIONAL AREA (ARBITRARY) = 1
    MP, EX, 1, 30E6
    N, 1
    N, 2, , 4
    N, 3, , 7
    N, 4, , 10
    E, 1, 2                          ! DEFINE ELEMENTS
    EGEN, 3, 1, 1
    D, 1, ALL, , , 4, 3                  ! BOUNDARY CONDITIONS AND LOADING
    F, 2, FY, -500
    F, 3, FY, -1000
    FINISH
    /SOLU
    OUTPR, BASIC, 1
    OUTPR, NLOAD, 1
    SOLVE
    FINISH
    /POST1
    NSEL, S, LOC, Y, 10
    FSUM
    *GET, REAC_1, FSUM, , ITEM, FY
    NSEL, S, LOC, Y, 0
    FSUM
    *GET, REAC_2, FSUM, , ITEM, FY

    *DIM, LABEL, CHAR, 2
    *DIM, VALUE, , 2, 3
    LABEL(1) = 'R1, lb', 'R2, lb '
    *VFILL, VALUE(1, 1), DATA, 900.0, 600.0
    *VFILL, VALUE(1, 2), DATA, ABS(REAC_1), ABS(REAC_2)
    *VFILL, VALUE(1, 3), DATA, ABS(REAC_1 / 900) , ABS( REAC_2 / 600)
    /OUT, vm1, vrt
    /COM
    /COM,' ------------------- VM1 RESULTS COMPARISON - --------------------'
    /COM,
    /COM,'         |   TARGET   |   Mechanical APDL   |   RATIO'
    /COM,
    *VWRITE, LABEL(1), VALUE(1, 1), VALUE(1, 2), VALUE(1, 3)
    (1X, A8, '   ', F10.1, '  ', F10.1, '   ', 1F5.3)
    /COM, ----------------------------------------------------------------
    /OUT
    FINISH
    *LIST, vm1, vrt

使用以下代码将文件转换为 Pymapdl ：

.. code:: pycon

    >>> from ansys.mapdl import core as pymapdl
    >>> from ansys.mapdl.core import examples
    >>> pymapdl.convert_script(examples.vmfiles["vm1"], "vm1.py")

以下是转换后的代码：

.. code:: python

    """ Script generated by ansys-mapdl-core version 0.57.0"""
    from ansys.mapdl.core import launch_mapdl

    mapdl = launch_mapdl()
    mapdl.run("/COM,ANSYS MEDIA REL. 150 (11/8/2013) REF. VERIF. MANUAL: REL. 150")
    mapdl.run("/VERIFY,VM1")
    mapdl.run("/PREP7")
    mapdl.run("/TITLE, VM1, STATICALLY INDETERMINATE REACTION FORCE ANALYSIS")
    mapdl.run("C***      STR. OF MATL., TIMOSHENKO, PART 1, 3RD ED., PAGE 26, PROB.10")
    mapdl.antype("STATIC")  # STATIC ANALYSIS
    mapdl.et(1, "LINK180")
    mapdl.sectype(1, "LINK")
    mapdl.secdata(1)  # CROSS SECTIONAL AREA (ARBITRARY) = 1
    mapdl.mp("EX", 1, 30e6)
    mapdl.n(1)
    mapdl.n(2, "", 4)
    mapdl.n(3, "", 7)
    mapdl.n(4, "", 10)
    mapdl.e(1, 2)  # DEFINE ELEMENTS
    mapdl.egen(3, 1, 1)
    mapdl.d(1, "ALL", "", "", 4, 3)  # BOUNDARY CONDITIONS AND LOADING
    mapdl.f(2, "FY", -500)
    mapdl.f(3, "FY", -1000)
    mapdl.finish()
    mapdl.run("/SOLU")
    mapdl.outpr("BASIC", 1)
    mapdl.outpr("NLOAD", 1)
    mapdl.solve()
    mapdl.finish()
    mapdl.run("/POST1")
    mapdl.nsel("S", "LOC", "Y", 10)
    mapdl.fsum()
    mapdl.run("*GET,REAC_1,FSUM,,ITEM,FY")
    mapdl.nsel("S", "LOC", "Y", 0)
    mapdl.fsum()
    mapdl.run("*GET,REAC_2,FSUM,,ITEM,FY")
    mapdl.run("*DIM,LABEL,CHAR,2")
    mapdl.run("*DIM,VALUE,,2,3")
    mapdl.run("LABEL(1) = 'R1, lb','R2, lb '")
    mapdl.run("*VFILL,VALUE(1,1),DATA,900.0,600.0")
    mapdl.run("*VFILL,VALUE(1,2),DATA,ABS(REAC_1),ABS(REAC_2)")
    mapdl.run("*VFILL,VALUE(1,3),DATA,ABS(REAC_1 / 900) ,ABS( REAC_2 / 600)")
    mapdl.run("/OUT,vm1,vrt")
    mapdl.run("/COM")
    mapdl.run("/COM,------------------- VM1 RESULTS COMPARISON ---------------------")
    mapdl.run("/COM,")
    mapdl.run("/COM,         |   TARGET   |   Mechanical APDL   |   RATIO")
    mapdl.run("/COM,")
    with mapdl.non_interactive:
        mapdl.run("*VWRITE,LABEL(1),VALUE(1,1),VALUE(1,2),VALUE(1,3)")
        mapdl.run("(1X,A8,'   ',F10.1,'  ',F10.1,'   ',1F5.3)")
    mapdl.run("/COM,----------------------------------------------------------------")
    mapdl.run("/OUT")
    mapdl.finish()
    mapdl.run("*LIST,vm1,vrt")
    mapdl.exit()


以下是运行转换后文件的结果：

.. code:: output

    ------------------- VM1 RESULTS COMPARISON ---------------------
    |   TARGET   |   Mechanical APDL   |   RATIO
    /INPUT FILE=    LINE=       0
    R1, lb          900.0       900.0   1.000
    R2, lb          600.0       600.0   1.000
    ----------------------------------------------------------------

您可以用以下方法验证反作用力：

.. code:: pycon

   >>> rst = mapdl.result
   >>> nnum, forces = rst.nodal_static_forces(0)
   >>> print(forces)
   [[   0. -600.    0.]
    [   0.  250.    0.]
    [   0.  500.    0.]
    [   0. -900.    0.]]

请注意，某些带 ``/`` 的命令不会直接转换为函数，而是作为 ``mapdl.run('/COM')`` 这样的 "经典" 命令运行。
此外，请注意 ``*VWRITE`` 命令需要紧跟其后的命令。这通常会锁定接口，因此在后台使用 :attr:`Mapdl.non_interactive <ansys.mapdl.core.Mapdl.non_interactive>` 属性将其作为输入文件执行。


VM7 - 管道组件的塑性压缩
--------------------------------------------
下面是 VM7 的输入文件：

.. code:: apdl

    /COM,'ANSYS MEDIA REL. 150 (11/8/2013) REF. VERIF. MANUAL: REL. 150'
    /VERIFY,VM7
    /PREP7
    /TITLE,' VM7, PLASTIC COMPRESSION OF A PIPE ASSEMBLY'
    /COM,'          MECHANICS OF SOLIDS, CRANDALL AND DAHL, 1959, PAGE 180, EX. 5.1'
    /COM,'          USING PIPE288, SOLID185 AND SHELL181 ELEMENTS'
    THETA=6                              ! SUBTENDED ANGLE
    ET,1,PIPE288,,,,2
    ET,2,SOLID185
    ET,3,SHELL181,,,2                    ! FULL INTEGRATION
    SECTYPE,1,SHELL
    SECDATA,0.5,1,0,5	                   ! THICKNESS (SHELL181)
    SECTYPE,2,SHELL
    SECDATA,0.5,2,0,5	                   ! THICKNESS (SHELL181)
    SECTYPE,3,PIPE
    SECDATA,4.9563384,0.5                ! OUTSIDE DIA. AND WALL THICKNESS FOR INSIDE TUBE (PIPE288)
    SECTYPE,4,PIPE
    SECDATA,8.139437,0.5                 ! OUTSIDE DIA. AND WALL THICKNESS FOR OUTSIDE TUBE (PIPE288)
    MP,EX  ,1,26.875E6                   ! STEEL
    MP,PRXY,1,0.3
    MP,EX  ,2,11E6                       ! ALUMINUM
    MP,PRXY,2,0.3
    TB,BKIN,1,1                          ! DEFINE NON-LINEAR MATERIAL PROPERTY FOR STEEL
    TBTEMP,0
    TBDATA,1,86000,0
    TB,BKIN,2,1                          ! DEFINE NON-LINEAR MATERIAL PROPERTY FOR ALUMINUM
    TBTEMP,0
    TBDATA,1,55000,0
    N,1                                  ! GENERATE NODES AND ELEMENTS FOR PIPE288
    N,2,,,10
    MAT,1  
    SECNUM,3                             ! STEEL (INSIDE) TUBE
    E,1,2
    MAT,2  
    SECNUM,4                             ! ALUMINUM (OUTSIDE) TUBE
    E,1,2
    CSYS,1
    N,101,1.9781692                      ! GENERATE NODES AND ELEMENTS FOR SOLID185
    N,102,2.4781692
    N,103,3.5697185
    N,104,4.0697185
    N,105,1.9781692,,10
    N,106,2.4781692,,10
    N,107,3.5697185,,10
    N,108,4.0697185,,10
    NGEN,2,10,101,108,,,THETA            ! GENERATE 2ND SET OF NODES TO FORM A THETA DEGREE SLICE
    NROTAT,101,118,1
    TYPE,2
    MAT,1                                ! INSIDE (STEEL) TUBE
    E,101,102,112,111,105,106,116,115
    MAT,2                                ! OUTSIDE (ALUMINUM) TUBE
    E,103,104,114,113,107,108,118,117
    N,201,2.2281692                      ! GENERATE NODES AND ELEMENTS FOR SHELL181
    N,203,2.2281692,,10
    N,202,3.8197185
    N,204,3.8197185,,10
    NGEN,2,4,201,204,,,THETA             ! GENERATE NODES TO FORM A THETA DEGREE SLICE
    TYPE,3
    SECNUM,1                             ! INSIDE (STEEL) TUBE
    E,203,201,205,207
    SECNUM,2                             ! OUTSIDE (ALUMINUM) TUBE
    E,204,202,206,208
    /COM,' APPLY CONSTRAINTS TO PIPE288 MODEL'
    D,1,ALL                              ! FIX ALL DOFS FOR BOTTOM END OF PIPE288
    D,2,UX,,,,,UY,ROTX,ROTY,ROTZ         ! ALLOW ONLY UZ DOF AT TOP END OF PIPE288 MODEL
    /COM,' APPLY CONSTRAINTS TO SOLID185 AND SHELL181 MODELS'
    CP,1,UX,101,111,105,115              ! COUPLE NODES AT BOUNDARY IN RADIAL DIR FOR SOLID185
    CPSGEN,4,,1
    CP,5,UX,201,205,203,20               ! COUPLE NODES AT BOUNDARY IN RADIAL DIR FOR SHELL181
    CPSGEN,2,,5
    CP,7,ROTY,201,205                    ! COUPLE NODES AT BOUNDARY IN ROTY DIR FOR SHELL181
    CPSGEN,4,,7
    NSEL,S,NODE,,101,212                 ! SELECT ONLY NODES IN SOLID185 AND SHELL181 MODELS
    NSEL,R,LOC,Y,0                       ! SELECT NODES AT THETA = 0 FROM THE SELECTED SET
    DSYM,SYMM,Y,1                        ! APPLY SYMMETRY BOUNDARY CONDITIONS
    NSEL,S,NODE,,101,212                 ! SELECT ONLY NODES IN SOLID185 AND SHELL181 MODELS
    NSEL,R,LOC,Y,THETA                   ! SELECT NODES AT THETA FROM THE SELECTED SET
    DSYM,SYMM,Y,1                        ! APPLY SYMMETRY BOUNDARY CONDITIONS
    NSEL,ALL
    NSEL,R,LOC,Z,0                       ! SELECT ONLY NODES AT Z = 0
    D,ALL,UZ,0                           ! CONSTRAIN BOTTOM NODES IN Z DIRECTION
    NSEL,ALL
    FINISH
    /SOLU    
    OUTPR,BASIC,LAST                     ! PRINT BASIC SOLUTION AT END OF LOAD STEP
    /COM,' APPLY DISPLACEMENT LOADS TO ALL MODELS'
    *CREATE,DISP
    NSEL,R,LOC,Z,10                      ! SELECT NODES AT Z = 10 TO APPLY DISPLACEMENT
    D,ALL,UZ,ARG1
    NSEL,ALL
    /OUT,SCRATCH
    SOLVE
    *END
    *USE,DISP,-.032
    *USE,DISP,-.05
    *USE,DISP,-.1
    FINISH
    /OUT,
    /POST1
    /COM,' CREATE MACRO TO GET RESULTS FOR EACH MODEL'
    *CREATE,GETLOAD
    NSEL,S,NODE,,1,2                    ! SELECT NODES IN PIPE288 MODEL
    NSEL,R,LOC,Z,0
    /OUT,SCRATCH
    FSUM                                ! FZ IS TOTAL LOAD FOR PIPE288 MODEL
    *GET,LOAD_288,FSUM,,ITEM,FZ
    NSEL,S,NODE,,101,118                ! SELECT NODES IN SOLID185 MODEL
    NSEL,R,LOC,Z,0
    FSUM
    *GET,ZFRC,FSUM,0,ITEM,FZ
    LOAD=ZFRC*360/THETA                 ! MULTIPLY BY 360/THETA FOR FULL 360 DEGREE RESULTS
    *STATUS,LOAD
    LOAD_185 = LOAD
    NSEL,S,NODE,,201,212                ! SELECT NODES IN SHELL181 MODEL
    NSEL,R,LOC,Z,0
    FSUM
    /OUT,
    *GET,ZFRC,FSUM,0,ITEM,FZ
    LOAD=ZFRC*360/THETA                 ! MULTIPLY BY 360/THETA FOR FULL 360 DEGREE RESULTS
    *STATUS,LOAD
    LOAD_181 = LOAD
    *VFILL,VALUE_288(1,1),DATA,1024400,1262000,1262000
    *VFILL,VALUE_288(I,2),DATA,ABS(LOAD_288)
    *VFILL,VALUE_288(I,3),DATA,ABS(LOAD_288)/(VALUE_288(I,1))
    *VFILL,VALUE_185(1,1),DATA,1024400,1262000,1262000
    *VFILL,VALUE_185(J,2),DATA,ABS(LOAD_185)
    *VFILL,VALUE_185(J,3),DATA,ABS(LOAD_185)/(VALUE_185(J,1))
    *VFILL,VALUE_181(1,1),DATA,1024400,1262000,1262000
    *VFILL,VALUE_181(K,2),DATA,ABS(LOAD_181)
    *VFILL,VALUE_181(K,3),DATA,ABS(LOAD_181)/(VALUE_181(K,1))
    *END
    /COM,' GET TOTAL LOAD FOR DISPLACEMENT = 0.032'
    /COM,' ---------------------------------------'
    SET,1,1
    I = 1
    J = 1
    K = 1
    *DIM,LABEL,CHAR,3,2
    *DIM,VALUE_288,,3,3
    *DIM,VALUE_185,,3,3
    *DIM,VALUE_181,,3,3
    *USE,GETLOAD
    /COM,' GET TOTAL LOAD FOR DISPLACEMENT = 0.05'
    /COM,' --------------------------------------'
    SET,2,1
    I = I + 1
    J = J + 1
    K = K + 1
    *USE,GETLOAD
    /COM,' GET TOTAL LOAD FOR DISPLACEMENT = 0.1'
    /COM,' -------------------------------------'
    SET,3,1
    I = I +1
    J = J + 1
    K = K + 1
    *USE,GETLOAD
    LABEL(1,1) = 'LOAD, lb','LOAD, lb','LOAD, lb'
    LABEL(1,2) = ' UX=.032',' UX=0.05',' UX=0.10'
    FINISH
    /OUT,vm7,vrt
    /COM,------------------- VM7 RESULTS COMPARISON ---------------------
    /COM,
    /COM,'                 |   TARGET   |   Mechanical APDL   |   RATIO'
    /COM,
    /COM,RESULTS FOR PIPE288:
    /COM,
    *VWRITE,LABEL(1,1),LABEL(1,2),VALUE_288(1,1),VALUE_288(1,2),VALUE_288(1,3)
    (1X,A8,A8,'   ',F10.0,'  ',F14.0,'   ',1F15.3)
    /COM,
    /COM,RESULTS FOR SOLID185:
    /COM,
    *VWRITE,LABEL(1,1),LABEL(1,2),VALUE_185(1,1),VALUE_185(1,2),VALUE_185(1,3)
    (1X,A8,A8,'   ',F10.0,'  ',F14.0,'   ',1F15.3)
    /COM,
    /COM,RESULTS FOR SHELL181:
    /COM,
    *VWRITE,LABEL(1,1),LABEL(1,2),VALUE_181(1,1),VALUE_181(1,2),VALUE_181(1,3)
    (1X,A8,A8,'   ',F10.0,'  ',F14.0,'   ',1F15.3)
    /COM,
    /COM,-----------------------------------------------------------------
    /OUT
    *LIST,vm7,vrt

将验证文件转换

.. code:: python

    >>> from ansys.mapdl import core as pymapdl
    >>> pymapdl.convert_script("vm7.dat", "vm7.py")

下面是转换好的 Python 脚本：

.. code:: python

    """ Script generated by ansys-mapdl-core version 0.57.0"""
    from ansys.mapdl.core import launch_mapdl

    mapdl = launch_mapdl()
    mapdl.run("/COM,ANSYS MEDIA REL. 150 (11/8/2013) REF. VERIF. MANUAL: REL. 150")
    mapdl.run("/VERIFY,VM7")
    mapdl.run("/PREP7")
    mapdl.run("/TITLE, VM7, PLASTIC COMPRESSION OF A PIPE ASSEMBLY")
    mapdl.run(
        "C***          MECHANICS OF SOLIDS, CRANDALL AND DAHL, 1959, PAGE 180, EX. 5.1"
    )
    mapdl.run("C***          USING PIPE288, SOLID185 AND SHELL181 ELEMENTS")
    mapdl.run("THETA=6                              ")  # SUBTENDED ANGLE
    mapdl.et(1, "PIPE288", "", "", "", 2)
    mapdl.et(2, "SOLID185")
    mapdl.et(3, "SHELL181", "", "", 2)  # FULL INTEGRATION
    mapdl.sectype(1, "SHELL")
    mapdl.secdata(0.5, 1, 0, 5)  # THICKNESS (SHELL181)
    mapdl.sectype(2, "SHELL")
    mapdl.secdata(0.5, 2, 0, 5)  # THICKNESS (SHELL181)
    mapdl.sectype(3, "PIPE")
    mapdl.secdata(
        4.9563384, 0.5
    )  # OUTSIDE DIA. AND WALL THICKNESS FOR INSIDE TUBE (PIPE288)
    mapdl.sectype(4, "PIPE")
    mapdl.secdata(
        8.139437, 0.5
    )  # OUTSIDE DIA. AND WALL THICKNESS FOR OUTSIDE TUBE (PIPE288)
    mapdl.mp("EX", 1, 26.875e6)  # STEEL
    mapdl.mp("PRXY", 1, 0.3)
    mapdl.mp("EX", 2, 11e6)  # ALUMINUM
    mapdl.mp("PRXY", 2, 0.3)
    mapdl.tb("BKIN", 1, 1)  # DEFINE NON-LINEAR MATERIAL PROPERTY FOR STEEL
    mapdl.tbtemp(0)
    mapdl.tbdata(1, 86000, 0)
    mapdl.tb("BKIN", 2, 1)  # DEFINE NON-LINEAR MATERIAL PROPERTY FOR ALUMINUM
    mapdl.tbtemp(0)
    mapdl.tbdata(1, 55000, 0)
    mapdl.n(1)  # GENERATE NODES AND ELEMENTS FOR PIPE288
    mapdl.n(2, "", "", 10)
    mapdl.mat(1)
    mapdl.secnum(3)  # STEEL (INSIDE) TUBE
    mapdl.e(1, 2)
    mapdl.mat(2)
    mapdl.secnum(4)  # ALUMINUM (OUTSIDE) TUBE
    mapdl.e(1, 2)
    mapdl.csys(1)
    mapdl.n(101, 1.9781692)  # GENERATE NODES AND ELEMENTS FOR SOLID185
    mapdl.n(102, 2.4781692)
    mapdl.n(103, 3.5697185)
    mapdl.n(104, 4.0697185)
    mapdl.n(105, 1.9781692, "", 10)
    mapdl.n(106, 2.4781692, "", 10)
    mapdl.n(107, 3.5697185, "", 10)
    mapdl.n(108, 4.0697185, "", 10)
    mapdl.ngen(
        2, 10, 101, 108, "", "", "THETA"
    )  # GENERATE 2ND SET OF NODES TO FORM A THETA DEGREE SLICE
    mapdl.nrotat(101, 118, 1)
    mapdl.type(2)
    mapdl.mat(1)  # INSIDE (STEEL) TUBE
    mapdl.e(101, 102, 112, 111, 105, 106, 116, 115)
    mapdl.mat(2)  # OUTSIDE (ALUMINUM) TUBE
    mapdl.e(103, 104, 114, 113, 107, 108, 118, 117)
    mapdl.n(201, 2.2281692)  # GENERATE NODES AND ELEMENTS FOR SHELL181
    mapdl.n(203, 2.2281692, "", 10)
    mapdl.n(202, 3.8197185)
    mapdl.n(204, 3.8197185, "", 10)
    mapdl.ngen(
        2, 4, 201, 204, "", "", "THETA"
    )  # GENERATE NODES TO FORM A THETA DEGREE SLICE
    mapdl.type(3)
    mapdl.secnum(1)  # INSIDE (STEEL) TUBE
    mapdl.e(203, 201, 205, 207)
    mapdl.secnum(2)  # OUTSIDE (ALUMINUM) TUBE
    mapdl.e(204, 202, 206, 208)
    mapdl.run("C*** APPLY CONSTRAINTS TO PIPE288 MODEL")
    mapdl.d(1, "ALL")  # FIX ALL DOFS FOR BOTTOM END OF PIPE288
    mapdl.d(
        2, "UX", "", "", "", "", "UY", "ROTX", "ROTY", "ROTZ"
    )  # ALLOW ONLY UZ DOF AT TOP END OF PIPE288 MODEL
    mapdl.run("C*** APPLY CONSTRAINTS TO SOLID185 AND SHELL181 MODELS")
    mapdl.cp(
        1, "UX", 101, 111, 105, 115
    )  # COUPLE NODES AT BOUNDARY IN RADIAL DIR FOR SOLID185
    mapdl.cpsgen(4, "", 1)
    mapdl.cp(
        5, "UX", 201, 205, 203, 20
    )  # COUPLE NODES AT BOUNDARY IN RADIAL DIR FOR SHELL181
    mapdl.cpsgen(2, "", 5)
    mapdl.cp(7, "ROTY", 201, 205)  # COUPLE NODES AT BOUNDARY IN ROTY DIR FOR SHELL181
    mapdl.cpsgen(4, "", 7)
    mapdl.nsel(
        "S", "NODE", "", 101, 212
    )  # SELECT ONLY NODES IN SOLID185 AND SHELL181 MODELS
    mapdl.nsel("R", "LOC", "Y", 0)  # SELECT NODES AT THETA = 0 FROM THE SELECTED SET
    mapdl.dsym("SYMM", "Y", 1)  # APPLY SYMMETRY BOUNDARY CONDITIONS
    mapdl.nsel(
        "S", "NODE", "", 101, 212
    )  # SELECT ONLY NODES IN SOLID185 AND SHELL181 MODELS
    mapdl.nsel("R", "LOC", "Y", "THETA")  # SELECT NODES AT THETA FROM THE SELECTED SET
    mapdl.dsym("SYMM", "Y", 1)  # APPLY SYMMETRY BOUNDARY CONDITIONS
    mapdl.nsel("ALL")
    mapdl.nsel("R", "LOC", "Z", 0)  # SELECT ONLY NODES AT Z = 0
    mapdl.d("ALL", "UZ", 0)  # CONSTRAIN BOTTOM NODES IN Z DIRECTION
    mapdl.nsel("ALL")
    mapdl.finish()
    mapdl.run("/SOLU")
    mapdl.outpr("BASIC", "LAST")  # PRINT BASIC SOLUTION AT END OF LOAD STEP
    mapdl.run("C*** APPLY DISPLACEMENT LOADS TO ALL MODELS")


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
    mapdl.finish()
    mapdl.run("/OUT,")
    mapdl.run("/POST1")
    mapdl.run("C*** CREATE MACRO TO GET RESULTS FOR EACH MODEL")


    def GETLOAD(
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
        mapdl.nsel("S", "NODE", "", 1, 2)  # SELECT NODES IN PIPE288 MODEL
        mapdl.nsel("R", "LOC", "Z", 0)
        mapdl.run("/OUT,SCRATCH")
        mapdl.fsum()  # FZ IS TOTAL LOAD FOR PIPE288 MODEL
        mapdl.run("*GET,LOAD_288,FSUM,,ITEM,FZ")
        mapdl.nsel("S", "NODE", "", 101, 118)  # SELECT NODES IN SOLID185 MODEL
        mapdl.nsel("R", "LOC", "Z", 0)
        mapdl.fsum()
        mapdl.run("*GET,ZFRC,FSUM,0,ITEM,FZ")
        mapdl.run(
            "LOAD=ZFRC*360/THETA                 "
        )  # MULTIPLY BY 360/THETA FOR FULL 360 DEGREE RESULTS
        mapdl.run("*STATUS,LOAD")
        mapdl.run("LOAD_185 = LOAD")
        mapdl.nsel("S", "NODE", "", 201, 212)  # SELECT NODES IN SHELL181 MODEL
        mapdl.nsel("R", "LOC", "Z", 0)
        mapdl.fsum()
        mapdl.run("/OUT,")
        mapdl.run("*GET,ZFRC,FSUM,0,ITEM,FZ")
        mapdl.run(
            "LOAD=ZFRC*360/THETA                 "
        )  # MULTIPLY BY 360/THETA FOR FULL 360 DEGREE RESULTS
        mapdl.run("*STATUS,LOAD")
        mapdl.run("LOAD_181 = LOAD")
        mapdl.run("*VFILL,VALUE_288(1,1),DATA,1024400,1262000,1262000")
        mapdl.run("*VFILL,VALUE_288(I,2),DATA,ABS(LOAD_288)")
        mapdl.run("*VFILL,VALUE_288(I,3),DATA,ABS(LOAD_288)/(VALUE_288(I,1))")
        mapdl.run("*VFILL,VALUE_185(1,1),DATA,1024400,1262000,1262000")
        mapdl.run("*VFILL,VALUE_185(J,2),DATA,ABS(LOAD_185)")
        mapdl.run("*VFILL,VALUE_185(J,3),DATA,ABS(LOAD_185)/(VALUE_185(J,1))")
        mapdl.run("*VFILL,VALUE_181(1,1),DATA,1024400,1262000,1262000")
        mapdl.run("*VFILL,VALUE_181(K,2),DATA,ABS(LOAD_181)")
        mapdl.run("*VFILL,VALUE_181(K,3),DATA,ABS(LOAD_181)/(VALUE_181(K,1))")


    mapdl.run("C*** GET TOTAL LOAD FOR DISPLACEMENT = 0.032")
    mapdl.run("C*** ---------------------------------------")
    mapdl.set(1, 1)
    mapdl.run("I = 1")
    mapdl.run("J = 1")
    mapdl.run("K = 1")
    mapdl.run("*DIM,LABEL,CHAR,3,2")
    mapdl.run("*DIM,VALUE_288,,3,3")
    mapdl.run("*DIM,VALUE_185,,3,3")
    mapdl.run("*DIM,VALUE_181,,3,3")
    GETLOAD()
    mapdl.run("C*** GET TOTAL LOAD FOR DISPLACEMENT = 0.05")
    mapdl.run("C*** --------------------------------------")
    mapdl.set(2, 1)
    mapdl.run("I = I + 1")
    mapdl.run("J = J + 1")
    mapdl.run("K = K + 1")
    GETLOAD()
    mapdl.run("C*** GET TOTAL LOAD FOR DISPLACEMENT = 0.1")
    mapdl.run("C*** -------------------------------------")
    mapdl.set(3, 1)
    mapdl.run("I = I +1")
    mapdl.run("J = J + 1")
    mapdl.run("K = K + 1")
    GETLOAD()
    mapdl.run("LABEL(1,1) = 'LOAD, lb','LOAD, lb','LOAD, lb'")
    mapdl.run("LABEL(1,2) = ' UX=.032',' UX=0.05',' UX=0.10'")
    mapdl.finish()
    mapdl.run("/OUT,vm7,vrt")
    mapdl.run("/COM,------------------- VM7 RESULTS COMPARISON ---------------------")
    mapdl.run("/COM,")
    mapdl.run("/COM,                 |   TARGET   |   Mechanical APDL   |   RATIO")
    mapdl.run("/COM,")
    mapdl.run("/COM,RESULTS FOR PIPE288:")
    mapdl.run("/COM,")
    with mapdl.non_interactive:
        mapdl.run(
            "*VWRITE,LABEL(1,1),LABEL(1,2),VALUE_288(1,1),VALUE_288(1,2),VALUE_288(1,3)"
        )
        mapdl.run("(1X,A8,A8,'   ',F10.0,'  ',F14.0,'   ',1F15.3)")
        mapdl.run("/COM,")
        mapdl.run("/COM,RESULTS FOR SOLID185:")
        mapdl.run("/COM,")
        mapdl.run(
            "*VWRITE,LABEL(1,1),LABEL(1,2),VALUE_185(1,1),VALUE_185(1,2),VALUE_185(1,3)"
        )
        mapdl.run("(1X,A8,A8,'   ',F10.0,'  ',F14.0,'   ',1F15.3)")
        mapdl.run("/COM,")
        mapdl.run("/COM,RESULTS FOR SHELL181:")
        mapdl.run("/COM,")
        mapdl.run(
            "*VWRITE,LABEL(1,1),LABEL(1,2),VALUE_181(1,1),VALUE_181(1,2),VALUE_181(1,3)"
        )
        mapdl.run("(1X,A8,A8,'   ',F10.0,'  ',F14.0,'   ',1F15.3)")
        mapdl.run("/COM,")
        mapdl.run("/COM,-----------------------------------------------------------------")
        mapdl.run("/OUT")
        mapdl.run("*LIST,vm7,vrt")
    mapdl.exit()
