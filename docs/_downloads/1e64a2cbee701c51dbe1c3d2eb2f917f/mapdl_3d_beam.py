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
.. _ref_3d_beam:

MAPDL 3D Beam
---------------------

这是一个简单的示例，加载包含梁的档案文件，然后使用简化的 ``modal_analysis`` 方法运行模态分析。

首先，将 MAPDL 作为一项服务启动。
"""

from ansys.mapdl.reader import examples

from ansys.mapdl.core import launch_mapdl

mapdl = launch_mapdl()

# 加载存储为示例档案文件的梁并对其进行网格划分
mapdl.cdread("db", examples.hexarchivefile)
mapdl.esel("s", "ELEM", vmin=5, vmax=20)
mapdl.cm("ELEM_COMP", "ELEM")
mapdl.nsel("s", "NODE", vmin=5, vmax=20)
mapdl.cm("NODE_COMP", "NODE")

# 边界条件
mapdl.allsel()

# 假设钢材性能
mapdl.prep7()
mapdl.mp("EX", 1, 200e9)  # Elastic moduli in Pa (kg/(m*s**2))
mapdl.mp("DENS", 1, 7800)  # Density in kg/m3
mapdl.mp("NUXY", 1, 0.3)  # Poissons Ratio
mapdl.emodif("ALL", "MAT", 1)

# 边界条件

# 固定梁的一端
mapdl.nsel("S", "LOC", "Z")
mapdl.d("all", "all")
mapdl.allsel()

# 绘制边界条件
mapdl.nplot(plot_bc=True)

###############################################################################

mapdl.mxpand(elcalc="YES")
mapdl.modal_analysis(nmode=6)


###############################################################################
# 使用 pyansys 结果对象查看结果
result = mapdl.result
print(result)


###############################################################################
# 获取节点位移值
nnum, disp = result.nodal_displacement(0)

# 打印节点数据 50 - 59
for i in range(49, 59):
    print(nnum[i], disp[i])


###############################################################################
# 绘制模态结果
result.plot_nodal_displacement(0, show_edges=True)


###############################################################################
# 为模态结果制作动画
result.animate_nodal_solution(0, show_edges=True, loop=False, displacement_factor=10, movie_filename='demo.gif')

###############################################################################
# Stop mapdl
# ~~~~~~~~~~
#
mapdl.exit()
