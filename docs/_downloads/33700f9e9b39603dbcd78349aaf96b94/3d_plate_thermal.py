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
.. _ref_3d_plate_thermal:

pyMAPDL 基本热力学分析
-----------------------------------

本例演示了如何使用 MAPDL 在 pyMAPDL 中创建板块、施加热边界条件、求解并绘制曲线。

首先，将 MAPDL 作为服务启动，并禁用除错误信息之外的所有功能。
"""

# sphinx_gallery_thumbnail_number = 2

from ansys.mapdl.core import launch_mapdl

mapdl = launch_mapdl()

###############################################################################
# Geometry and Material Properties
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 创建一个简单的横梁，指定材料属性并对其进行网格划分。
mapdl.prep7()
mapdl.mp("kxx", 1, 45)
mapdl.et(1, 90)
mapdl.block(-0.3, 0.3, -0.46, 1.34, -0.2, -0.2 + 0.02)
mapdl.vsweep(1)
mapdl.eplot()


###############################################################################
# Boundary Conditions
# ~~~~~~~~~~~~~~~~~~~
# 设置热边界条件
mapdl.asel("S", vmin=3)
mapdl.nsla()
mapdl.d("all", "temp", 5)
mapdl.asel("S", vmin=4)
mapdl.nsla()
mapdl.d("all", "temp", 100)
out = mapdl.allsel()


###############################################################################
# Solve
# ~~~~~
# 求解热力学静态分析并打印结果
mapdl.vsweep(1)
mapdl.run("/SOLU")
print(mapdl.solve())
out = mapdl.finish()


###############################################################################
# Post-Processing using MAPDL
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 通过 MAPDL 直接获取结果，查看梁的热力学结果。
mapdl.post1()
mapdl.set(1, 1)
mapdl.post_processing.plot_nodal_temperature()


###############################################################################
# 或者，也可以使用 pyansys 读取结果文件的结果对象

result = mapdl.result
nnum, temp = result.nodal_temperature(0)
# 这等同于 pyansys.read_binary(mapdl._result_file)
print(nnum, temp)

###############################################################################
# Stop mapdl
# ~~~~~~~~~~
#
mapdl.exit()
