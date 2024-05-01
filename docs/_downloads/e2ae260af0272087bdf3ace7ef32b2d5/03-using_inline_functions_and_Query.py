# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
.. _ref_how_to_use_query:

使用内联函数（Query）
------------------------------

本例向您展示如何使用 PyMAPDL 中的内联函数（Inline Functions）。

像 ``UX`` 这样的内联函数已经作为 ``mapdl.inline_functions.Query`` 对象的方法在 PyMAPDL 中实现。在本例中，我们将建立一个简单的模拟，并使用 ``Query`` 演示其部分功能。

首先，使用 ``mapdl`` 属性 ``queries`` 获取下面 :class:`ansys.mapdl.core.inline_functions.Query` 的实例。

"""

from ansys.mapdl.core import launch_mapdl

mapdl = launch_mapdl()

# clear at the start and enter the preprocessing routine
mapdl.clear()
mapdl.prep7()
q = mapdl.queries

###############################################################################
# Setup Mesh
# ~~~~~~~~~~
# - 将单元类型 ``SOLID5`` 分配给单元类型 1
# - 创建一个长方体 ``mapdl.block`` 尺寸为 10 x 20 x 30
# - 将单元大小设置为 2
# - 对长方体进行网格划分
# - 绘制创建的单元图

mapdl.et(1, "SOLID5")
mapdl.block(0, 10, 0, 20, 0, 30)
mapdl.esize(2)
mapdl.vmesh("ALL")
mapdl.eplot()

###############################################################################
# Setup Boundary Conditions
# ~~~~~~~~~~~~~~~~~~~~~~~~~
# - 为材料 1 指定弹性模量为 21e9
# - 泊松比为 0.3
# - 选择长方体 ``z = 30`` 端的所有节点
# - 约束选区中所有节点的全部自由度
# - 选择 ``z = 0`` 端的所有节点
# - 对这些节点施加 10000 的 X 方向力
# - 完成前处理

mapdl.mp("EX", 1, 21e9)
mapdl.mp("PRXY", 1, 0.3)
mapdl.nsel("S", "LOC", "Z", 30)
mapdl.d("ALL", "UX")
mapdl.d("ALL", "UY")
mapdl.d("ALL", "UZ")
mapdl.nsel("S", "LOC", "Z", 0)
mapdl.f("ALL", "FX", 10000)
mapdl.finish()

###############################################################################
# Setup Boundary Conditions
# ~~~~~~~~~~~~~~~~~~~~~~~~~
# - 进入求解层（ ``mapdl.slashsolu`` 命令也适用）
# - 将分析类型设置为 ``STATIC``
# - 选择所有节点
# - 求解模型
# - 完成求解

mapdl.run("/SOLU")
mapdl.antype("STATIC")
mapdl.allsel()
mapdl.solve()
mapdl.finish(mute=True)

###############################################################################
# Post-Processing
# ~~~~~~~~~~~~~~~
# - 从 ``mapdl`` 实例获取结果
# - 绘制等效应力结果图
# - 显示边缘，以便我们可以看到单元的边界
# - 使用 “plasma” 颜色贴图，因为它在感知上是一致的

result = mapdl.result
result.plot_principal_nodal_stress(0, "SEQV", show_edges=True, cmap="plasma")

###############################################################################
# Using ``Query``
# ~~~~~~~~~~~~~~~
# - 使用 ``Query`` 获取距离 (5, 0, 0) 和 (5, 10, 0) 最近的节点
# - 使用 ``Query`` 实例检查 x、y 和 z 位移。
# - 以格式化字符串打印结果。

node1 = q.node(5.0, 0.0, 0.0)
node2 = q.node(5.0, 10.0, 0.0)

for node in [node1, node2]:
    x_displacement = q.ux(node)
    y_displacement = q.uy(node)
    z_displacement = q.uz(node)

    message = f"""
    ************************
    Displacement at Node {node}:
    ************************
    X | {x_displacement}
    Y | {y_displacement}
    Z | {z_displacement}

    """
    print(message)


###############################################################################
# Stop mapdl
# ~~~~~~~~~~
#
mapdl.exit()
