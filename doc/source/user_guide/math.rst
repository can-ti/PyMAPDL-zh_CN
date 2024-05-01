.. _mapdl_math_class_ref:

PyAnsys Math overview
=====================
`PyAnsys Math <pyansys_math_>`_ 提供了访问和处理大型稀疏矩阵的能力，并以类似于流行的 `numpy <numpy_docs_>`_ 和 `scipy <scipy_docs_>`_ 库的方式解决各种特征问题。

PyMAPDL and PyAnsys Math
~~~~~~~~~~~~~~~~~~~~~~~~

此示例演示了如何利用 PyMAPDL 来利用 `ansys-math-core` 软件包。

它说明了如何将 MAPDL 数学矩阵从 MAPDL 发送到 Python，然后再发送回去求解。
本例在 MAPDL 生成的质量和刚度矩阵上运行 :func:`mm.eigs() <ansys.math.core.math.AnsMath.eigs>` 方法，
您也可以使用外部有限元工具生成的质量和刚度矩阵，甚至在 Python 中修改质量和刚度矩阵。

首先，在 MAPDL 中求解 "1 x 1 x 1" 钢立方体的前 10 阶模态。

.. code:: python

    import re
    from ansys.mapdl.core import launch_mapdl

    mapdl = launch_mapdl()

    # setup the full file
    mapdl.prep7()
    mapdl.block(0, 1, 0, 1, 0, 1)
    mapdl.et(1, 186)
    mapdl.esize(0.5)
    mapdl.vmesh("all")

    # Define a material (nominal steel in SI)
    mapdl.mp("EX", 1, 210e9)  # Elastic moduli in Pa (kg/(m*s**2))
    mapdl.mp("DENS", 1, 7800)  # Density in kg/m3
    mapdl.mp("NUXY", 1, 0.3)  # Poisson's Ratio

    # solve first 10 non-trivial modes
    out = mapdl.modal_analysis(nmode=10, freqb=1)

    # store the first 10 natural frequencies
    mapdl.post1()
    resp = mapdl.set("LIST")
    w_n = np.array(re.findall(r"\s\d*\.\d\s", resp), np.float32)
    print(w_n)

现在，您已经解出了立方体的前 10 阶模态：

.. code:: output

    [1475.1 1475.1 2018.8 2018.8 2018.8 2024.8 2024.8 2024.8 2242.2 2274.8]

接下来，加载默认存储在 :file:`<jobname>.full` 文件中的质量和刚度矩阵。
首先，创建一个 :class:`MapdlMath <ansys.math.core.math.AnsMath>` 类的实例作为 ``mm`` ：

.. code:: python

    from ansys.math.core.math import AnsMath

    # 导入并连接 PyAnsys Math 到 PyMAPDL
    mm = AnsMath(mapdl)

    # 默认从 file.full 加载
    k = mm.stiff()
    m = mm.mass()

    # 转换为 numpy
    k_py = k.asarray()
    m_py = m.asarray()
    mapdl.clear()
    print(k_py)

运行 :func:`mapdl.clear() <ansys.mapdl.core.Mapdl.clear>` 方法后，这些矩阵将只存储在 Python 中。

.. code:: output

    (0, 0)	37019230769.223404
    (0, 1)	10283119658.117708
    (0, 2)	10283119658.117706
    :	:
    (240, 241)	11217948717.943113
    (241, 241)	50854700854.68495
    (242, 242)	95726495726.47179

要从 PyMAPDL 直接调用 PyAnsys Math，可以运行这条命令：

.. code:: python

    # 使用 PyMAPDL 直接启动 PyAnsys Math
    mm = mapdl.math


最后一步是将这些矩阵送回 MAPDL 进行求解。在清除 MAPDL 的同时，您可以关闭 MAPDL，甚至将矩阵转移到不同的 MAPDL 会话中进行求解：

.. code:: python

    my_stiff = mm.matrix(k_py, triu=True)
    my_mass = mm.matrix(m_py, triu=True)

    # solve for the first 10 modes above 1 Hz
    nmode = 10
    mapdl_vec = mm.eigs(nmode, my_stiff, my_mass, fmin=1)
    eigval = mapdl_vec.asarray()
    print(eigval)

不出所料，通过 :func:`mm.eigs() <ansys.math.core.math.AnsMath.eigs>` 方法得到的自然频率与 MAPDL 中 :func:`mapdl.solve() <ansys.mapdl.core.Mapdl.solve>` 方法得到的结果完全相同。

.. code:: output

    [1475.1333421  1475.1333426  2018.83737064 2018.83737109 2018.83737237
     2024.78684466 2024.78684561 2024.7868466  2242.21532585 2274.82997741]

如果您想获得特征向量和特征值，请初始化一个矩阵 ``eigvec`` 并将其发送到 :func:`mm.eigs() <ansys.math.core.math.AnsMath.eigs>` 方法：

.. code:: pycon

    >>> nmode = 10
    >>> eigvec = mm.zeros(my_stiff.nrow, nmode)  # for eigenvectors
    >>> val = mm.eigs(nmode, my_stiff, my_mass, fmin=1)

AnsMath 矩阵 ``eigvec`` 现在包含了解的特征向量。

PyAnsys Math reference
~~~~~~~~~~~~~~~~~~~~~~

更多信息，请参阅 `PyAnsys Math API 参考 <pyansys_math_api_>`_ 。
