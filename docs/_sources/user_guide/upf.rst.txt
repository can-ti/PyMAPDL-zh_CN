.. _python_upf:


Using Python to code UPF subroutines
------------------------------------

作为 C 和 Fortran 等编译语言的替代，您可以使用 Python 语言来编写用户可编程子程序。已记录的 UPF 子程序子集支持 Python UPF 功能。更多信息，请参阅 `Supported UPF subroutines`_ 。

使用此功能前，您必须安装 Python 发行版。支持 Python 3.8 至 Python 3.12。

Python UPF 仅支持 Linux。


强烈建议您根据 `Python UPF examples`_ 中的一个示例开始编写代码。在 Python 代码中，您可以使用标准 Python 库，如 NumPy。

这些主题可供选择：

* `Supported UPF subroutines`_
* `Python UPF methodology`_
* `Accessing the database from the Python code`_
* `Python UPF limitations`_
* `Python UPF examples`_


Supported UPF subroutines
^^^^^^^^^^^^^^^^^^^^^^^^^

在所有可用的 UPF 子程序中，有一部分支持 Python 编码。下表列出了支持的子程序。


**Table 1: Python support for subroutines** 


+---------------------------------------+-----------------------------------------------------------------------------+
| **Subroutine**                        | **Fortran description**                                                     |
+=======================================+=============================================================================+
|                              **Material behavior**                                                                  |
+---------------------------------------+-----------------------------------------------------------------------------+
| ``UserMat``                           | Subroutine ``UserMat`` (Creating Your Own Material Model)                   |
+---------------------------------------+-----------------------------------------------------------------------------+
| ``UserMatTh``                         | Subroutine ``UserMatTh`` (Creating Your Own Thermal Material Model)         |
+---------------------------------------+-----------------------------------------------------------------------------+
| ``UserHyper``                         | Subroutine ``UserHyper`` (Writing Your Own Isotropic Hyperelasticity Laws)  |
+---------------------------------------+-----------------------------------------------------------------------------+
| ``UserCreep``                         | Subroutine ``UserCreep`` (Defining Creep Material Behavior)                 |
+---------------------------------------+-----------------------------------------------------------------------------+
|                              **Modifying and Monitoring Elements**                                                  |
+---------------------------------------+-----------------------------------------------------------------------------+
| ``UsrShift``                          | Subroutine ``UsrShift`` (Calculating Pseudotime Time Increment)             |
+---------------------------------------+-----------------------------------------------------------------------------+
| ``UTimeInc``                          | Subroutine ``UTimeInc`` (Overriding the Program-Determined Time Step)       |
+---------------------------------------+-----------------------------------------------------------------------------+
| ``UCnvrg``                            | Subroutine ``UCnvrg`` (Overriding the Program-Determined Convergence)       |
+---------------------------------------+-----------------------------------------------------------------------------+
|                              **Customizing loads**                                                                  |
+---------------------------------------+-----------------------------------------------------------------------------+
| ``usrefl``                            | Subroutine ``usrefl`` (Changing Scalar Fields to User-Defined Values)       |
+---------------------------------------+-----------------------------------------------------------------------------+
| ``userpr``                            | Subroutine ``userpr`` (Changing Element Pressure Information)               |
+---------------------------------------+-----------------------------------------------------------------------------+
| ``usercv``                            | Subroutine ``usercv`` (Changing Element Face Convection Surface Information)|
+---------------------------------------+-----------------------------------------------------------------------------+
| ``userfx``                            | Subroutine ``userfx`` (Changing Element Face Heat Flux Surface Information) |
+---------------------------------------+-----------------------------------------------------------------------------+
|                              **Accessing subroutines**                                                              |
+---------------------------------------+-----------------------------------------------------------------------------+
| ``UanBeg`` / ``UanFin``               | Access at the beginning and end of various operations                       |
|                                       |                                                                             |
| ``USolBeg`` / ``USolFin``             |                                                                             |
|                                       |                                                                             |
| ``ULdBeg`` / ``ULdFin``               |                                                                             |
|                                       |                                                                             |
| ``UItBeg`` / ``UItFin``               |                                                                             |
|                                       |                                                                             |
| ``USsBeg`` / ``USsFin``               |                                                                             |
+---------------------------------------+-----------------------------------------------------------------------------+


Python UPF methodology
^^^^^^^^^^^^^^^^^^^^^^

编码 Python UPF 与使用 C/C++ 或 Fortran 等编译语言不同，主要体现在 API 方面。
由于 `gRPC 技术 <grpc_>`_ 用于处理 Python 进程和 Mechanical APDL 进程之间的通信和数据交换，因此您需要了解该功能处理数据序列化和反序列化的方式。

The main difference is in the subroutine arguments. Instead of having a full list of
arguments as described for each of the subroutines, there are only two: the request
object (for inputs), and the response object (for outputs). If an argument is both input
and output of the subroutine, it is part of both objects. | 
主要区别在于子程序参数。每个子程序都有一个完整的参数列表，而现在只有两个：请求对象（用于输入）和响应对象（用于输出）。
如果一个参数既是子程序的输入，又是子程序的输出，那么它就是这两个对象的一部分。

The description of the request object and the response object can be found in the
``MapdlUser.proto`` file stored in this installation directory: | 关于请求对象和响应对象的说明，可在本安装目录下的 ``MapdlUser.proto`` 文件中找到：


.. code:: output

    Ansys Inc\vXXX\ansys\syslib\ansGRPC\User

其中 ``XXX`` 是您使用的 Mechanical APDL 版本。例如， ``222`` 表示 Mechanical APDL 2022R2。

首先，从这个模板开始创建一个 Python 文件：


**my\_upf.py** 

.. code:: python

    import grpc
    import sys
    from mapdl import *


    class MapdlUserService(MapdlUser_pb2_grpc.MapdlUserServiceServicer):
        #   #################################################################
        def UAnBeg(self, request, context):
            print(" ======================================= ")
            print(" >> Inside the PYTHON UAnBeg routine  << ")
            print(" ======================================= \n")

            response = google_dot_protobuf_dot_empty__pb2._EMPTY()
            return response


    if __name__ == "__main__":
        upf.launch(sys.argv[0])


请注意，Mechanical APDL 会自动安装 Mechanical APDL Python 包（一组 Python 函数），以处理 Mechanical APDL 和 Python 环境之间的连接。必须导入每个 Python UPF：


.. code:: python

    from mapdl import *


The preceding example redefines the `UAnBeg` routine and prints a
customized banner. This file must be in the same directory as the input file. | 
上例重新定义了 `UAnBeg` 例程，并打印了一个定制的横幅。该文件必须与输入文件位于同一目录。

To use this Python UPF, you must add the Mechanical APDL ``/UPF`` command to your
input file (``my\_inp.dat``). | 
要使用 Python UPF，必须在输入文件（ ``my\_inp.dat`` ）中添加 Mechanical APDL ``/UPF`` 命令。

.. code:: apdl

    /UPF,'my_upf.py'

    ! The UAnBeg UPF must be activated by using the USRCAL APDL command

    USRCAL,UANBEG


该命令会被 Mechanical APDL 启动器捕获，这样当 Mechanical APDL 进程启动时，Python gRPC 服务器就会启动并运行。

使用此输入文件启动 Mechanical APDL 时，会看到以下打印输出，表明 Mechanical APDL 检测到 Python UPF 指令并启动了 Python 服务器：


.. code:: output

    Processing "/upf" found in input file "my_inp.dat"

    Python UPF Detected

    PYTHON VERSION : 3.10
    >>
    >> START PYTHON GRPC SERVER
    >>
    >> User Functions Python File :  my_upf.py
    >>
    >> Server started on port [50054]


在 Mechanical APDL 进程中， 您会看到以下 Python 打印输出：


.. code:: output

    RUN SETUP PROCEDURE FROM FILE= /ansys_inc/v212/ansys/apdl/start.ans
    =======================================
    >> Inside the PYTHON UAnBeg routine  <<
    =======================================


在进程的最后，Python 服务器会自动关闭：


.. code:: output
    
    |-----------------------------------------------------------------|
    |                                                                 |
    |   CP Time      (sec) =          0.326       Time  =  10:40:24   |
    |   Elapsed Time (sec) =          2.000       Date  =  03/11/2021 |
    |                                                                 |
    *-----------------------------------------------------------------*

    >> We shutdown Python Server(s)



Accessing the database from the Python code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

在 UPF 例程中，您可能需要以 只读/写 模式访问 Mechanical APDL 数据库。

在 Python 代码中，您可以创建与 DB 服务器的连接。该命令必须只调用一次，这样就可以保护基于静态变量值的调用：


.. code:: python

    import grpc
    import sys
    from mapdl import *

    firstcall = 1


    class MapdlUserService(MapdlUser_pb2_grpc.MapdlUserServiceServicer):
        #   ###############################################################
        def UserMat(self, request, context):
            global firstcall

            if firstcall == 1:
                print(">> Connection to the MAPDL DB Server\n")
                db.start()
                firstcall = 0

            # continuation of the python function
            # ...


一旦初始化了 DB 连接，就可以以 只读/写 模式访问 Mechanical APDL 实例的数据库。

在访问 Mechanical APDL 数据库中记录的函数中，有一部分已经公开，以便从 Python 代码中调用。下表描述了已公开的函数。

**Table 2. Supported database access functions**

+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **Supported database access functions**                                                                                                                                                                                                              |
+==========================================================+===========================================================================================================================================================================================+
| ``db.start()``                                           | Initializes the connection with a running Mechanical APDL instance. The DB Server is automatically started in Mechanical APDL if a **/UPF** command with a Python file has been detected. |
+----------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``db.stop()``                                            | Closes the connection with the DB Server.                                                                                                                                                 |
+----------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``db.ndnext(next)``                                      | Equivalent to the function described in function ``ndnext`` (Getting the Next Node Number)                                                                                                |
+----------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``db.ndinqr(ind, key)``                                  | Equivalent to the function described in function ``ndinqr`` (Getting Information About a Node)                                                                                            |
+----------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``db.getnod(inod)``                                      | Equivalent to the function described in function ``getnod`` (Getting a Nodal Point)                                                                                                       |
+----------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``db.putnod(inod, x, y, z)``                             | Equivalent to the function described in function ``putnod`` (Storing a Node)                                                                                                              |
+----------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``db.elnext(ielm)``                                      | Equivalent to the function described in function ``elnext`` (Getting the Number of the Next Element)                                                                                      |
+----------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``db.getelem(ielm)``                                     | Equivalent to the function described in function ``elmget`` (Getting an Element's Attributes and Nodes)                                                                                   |
+----------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``db.get_ElmInfo(inquire)``                              | Equivalent to the function ``get\_ElmInfo`` described in accessing Solution and Material Data                                                                                             |
+----------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``db.get_ElmData(kchar, elemId, kMatRecPt, ncomp, vect)``| Equivalent to the function ``get\_ElmData`` described in accessing Solution and Material Data                                                                                             |
+----------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``db.putElmData(inquire, elemId, kIntg, nvect, vect)``   | Equivalent to the function ``put\_ElmData`` described in accessing Solution and Material Data                                                                                             |
+----------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+


Python UPF limitations
^^^^^^^^^^^^^^^^^^^^^^

Python UPF 功能有这些限制：

* 目前不支持分布式 Ansys。必须在命令行中指定 ``-smp`` 选项，以确保 Mechanical APDL 在共享内存处理模式下运行。
* Python UPF 仅适用于 Linux 平台。



Python UPF examples
^^^^^^^^^^^^^^^^^^^

以下 Python UPF 示例位于 :ref:`python_upf_examples` 中：

* Python `UserMat` subroutine
* Python `UsrShift` subroutine
* Python `UserHyper` subroutine

