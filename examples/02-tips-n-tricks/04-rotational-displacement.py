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
.. _ref_rotational_displacement_example:

生成和提取旋转位移
-------------------------------------------------

在本例中，我们将展示如何处理壳体和旋转位移。

并非所有单元类型都有旋转自由度，但一般来说，"壳" 单元都有。在本例中，我们创建一个厚度为 0.1 的正方形外壳，然后将其弯曲，产生旋转位移。

随后，我们绘制累积主应力图，并使用 :class:`ansys.mapdl.core.inline_functions.Query` 提取正方形四个角的旋转位移精确值。

"""

# start MAPDL and enter the pre-processing routine
from ansys.mapdl.core import launch_mapdl

mapdl = launch_mapdl()
mapdl.prep7()

###############################################################################
# Mesh Setup
# ~~~~~~~~~~
# 在本例中，我们创建了一个简单的二维正方形，尺寸为 1 x 1，并赋予其 ``SHELL181`` 单元类型，因为该类型具有旋转自由度。接下来我们
#
# - 给出该材料的弹性模量为 2e5 (EX)
# - 将材料的主要泊松比定为 0.3 (PRXY)
# - 将截面类型设置为 “SHELL”
# - 将厚度设置为 0.1
# - 将单元大小设置为 0.2
# - 划分网格
# - 绘制模型

mapdl.et(1, "SHELL181")
mapdl.mp("EX", 1, 2e5)
mapdl.mp("PRXY", 1, 0.3)
mapdl.rectng(0, 1, 0, 1)
mapdl.sectype(1, "SHELL")
mapdl.secdata(0.1)
mapdl.esize(0.2)
mapdl.amesh("all")
mapdl.eplot()

###############################################################################
# Applying Boundary Conditions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# - 进入求解层
# - 将分析类型设为 ``STATIC`` 。
# - 约束 ``x = 0`` 节点的所有自由度
# - 在 ``x = 1`` 处施加 ``uz = -0.1`` 的位移
# - 选择所有节点
# - 求解模型

mapdl.run("/SOLU")
mapdl.antype("STATIC")
mapdl.nsel("s", "loc", "x", 0)
mapdl.d("all", "all")
mapdl.nsel("s", "loc", "x", 1)
mapdl.d("all", "uz", -0.1)
mapdl.allsel("all")
mapdl.solve()

###############################################################################
# Plotting Stresses
# ~~~~~~~~~~~~~~~~~
# - 提取结果
# - 绘制累积 (0) 等效应力 (SEQV) 图
# - 将 colormap 设置为 'plasma'，因为它在感知上是一致的
# - 显示位移，以便我们看到任何变形

result = mapdl.result
result.plot_principal_nodal_stress(
    0, "SEQV", show_edges=True, cmap="plasma", show_displacement=True
)


###############################################################################
# Extracting Rotational Displacements
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# - 从 ``queries`` 属性获取 :class:`ansys.mapdl.core.inline_functions.Query` 实例
# - 在正方形的四个角上定位节点
# - 分别提取所有 3 个旋转位移分量
# - 全部打印出来

q = mapdl.queries

node1 = q.node(0, 0, 0)
node2 = q.node(0, 1, 0)
node3 = q.node(1, 0, 0)
node4 = q.node(1, 1, 0)

nodes = [node1, node2, node3, node4]

rotations = [(q.rotx(n), q.roty(n), q.rotz(n)) for n in nodes]

message = f"""
(0,1) B _________ C (1,1)
       |         |
       |         |
       |         |
       |_________|
(0,0) A           D (1,0)

N | (x_rot_disp, y_rot_disp, z_rot_disp)
--|------------------------------------
A | {rotations[0][0]:11.6f},{rotations[0][1]:11.6f},{rotations[0][2]:11.6f}
B | {rotations[1][0]:11.6f},{rotations[1][1]:11.6f},{rotations[1][2]:11.6f}
C | {rotations[2][0]:11.6f},{rotations[2][1]:11.6f},{rotations[2][2]:11.6f}
D | {rotations[3][0]:11.6f},{rotations[3][1]:11.6f},{rotations[3][2]:11.6f}

"""

print(message)


###############################################################################
# Stop mapdl
# ~~~~~~~~~~
#
mapdl.exit()
