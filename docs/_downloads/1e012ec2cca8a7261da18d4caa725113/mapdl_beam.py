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
.. _ref_mapdl_beam:

MAPDL 2D Beam
---------------------


本例来自 Paletikrishna Chaitanya、Sambanarajesh Kumar 和 Datti Srinivas 合著的 *"Finite element analysis using ansys 11.0"* 一书。PHI Learning Pvt. Ltd., 1 Jan 2010.
"""

###############################################################################
# 启动具有交互式绘图功能的 MAPDL
from ansys.mapdl.core import launch_mapdl

mapdl = launch_mapdl()
mapdl.fcomp("rst", 0)  # 指定压缩级别
###############################################################################
# 定义工字钢
mapdl.prep7()
mapdl.et(1, "BEAM188")
mapdl.keyopt(1, 4, 1)  # 横向剪应力输出

# 材料特性
mapdl.mp("EX", 1, 2e7)  # N/cm2
mapdl.mp("PRXY", 1, 0.27)  #  Poisson's ratio

# 以厘米为单位的梁特性
sec_num = 1
mapdl.sectype(sec_num, "BEAM", "I", "ISection", 3)
mapdl.secoffset("CENT")
beam_info = mapdl.secdata(15, 15, 29, 2, 2, 1)  # 尺寸单位为厘米

###############################################################################
# 在 MAPDL 中创建节点
mapdl.n(1, 0, 0, 0)
mapdl.n(12, 110, 0, 0)
mapdl.n(23, 220, 0, 0)
mapdl.fill(1, 12, 10)
mapdl.fill(12, 23, 10)

# 列出节点坐标
print(f'节点坐标为： {mapdl.mesh.nodes}')

# 列出节点编号
print(f'节点编号为： {mapdl.mesh.nnum}')

# 使用 VTK 绘制节点图
mapdl.nplot(vtk=True, nnum=True, cpos="xy", show_bounds=True, point_size=10)

###############################################################################
# 在节点之间创建单元
# 我们可以手动创建单元，因为我们知道单元是连续的
for node in mapdl.mesh.nnum[:-1]:
    mapdl.e(node, node + 1)

# 打印来自 MAPDL 的单元
print(mapdl.elist())

###############################################################################
# 以数组的形式访问它们
# 请参阅有关 ``mapdl.mesh.elem`` 的文档，了解如何解释各个单元
for elem in mapdl.mesh.elem:
    print(elem)

###############################################################################
# 定义边界条件

# 只允许在 X 和 Z 方向移动
for const in ["UX", "UY", "ROTX", "ROTZ"]:
    mapdl.d("all", const)

# 只限制 Z 方向上的节点 1 和 23
mapdl.d(1, "UZ")
mapdl.d(23, "UZ")

# 在节点 12 上施加 -Z 方向的力
mapdl.f(12, "FZ", -22840)


###############################################################################
# 运行静态分析
mapdl.run("/solu")
mapdl.antype("static")
print(mapdl.solve())

###############################################################################
# Stop mapdl
# ~~~~~~~~~~
#
mapdl.exit()
