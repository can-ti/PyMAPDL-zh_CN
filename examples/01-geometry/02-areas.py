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
.. _ref_basic-geometry-areas:

Areas
-----

本例演示如何使用 area 命令创建基本几何体。

"""

import numpy as np

from ansys.mapdl.core import launch_mapdl

# start MAPDL and enter the pre-processing routine
mapdl = launch_mapdl()
mapdl.clear()
mapdl.prep7()
print(mapdl)


###############################################################################
# APDL Command: A
# ~~~~~~~~~~~~~~~
# 使用三个关键点在 XY 平面上创建一个简单的三角形。

k0 = mapdl.k("", 0, 0, 0)
k1 = mapdl.k("", 1, 0, 0)
k2 = mapdl.k("", 0, 1, 0)
a0 = mapdl.a(k0, k1, k2)
mapdl.aplot(vtk=False)
mapdl.aplot(show_lines=True, line_width=5, show_bounds=True, cpos="xy")


###############################################################################
# APDL Command: AL
# ~~~~~~~~~~~~~~~~
# 用四条线创建一个 area 。
mapdl.clear()
mapdl.prep7()

k0 = mapdl.k("", 0, 0, 0)
k1 = mapdl.k("", 1, 0, 0)
k2 = mapdl.k("", 1, 1, 0)
k3 = mapdl.k("", 0, 1, 0)
l0 = mapdl.l(k0, k1)
l1 = mapdl.l(k1, k2)
l2 = mapdl.l(k2, k3)
l3 = mapdl.l(k3, k0)
anum = mapdl.al(l0, l1, l2, l3)
mapdl.aplot(vtk=False)
mapdl.aplot(show_lines=True, line_width=5, show_bounds=True, cpos="xy")


###############################################################################
# APDL Command: ADRAG
# ~~~~~~~~~~~~~~~~~~~
# 通过沿路径拖动线来生成 area。
#
# 在两个关键点之间拖动一个圆，创建一个 area 
mapdl.clear()
mapdl.prep7()

k0 = mapdl.k("", 0, 0, 0)
k1 = mapdl.k("", 0, 0, 1)
carc = mapdl.circle(k0, 1, k1, arc=90)
l0 = mapdl.l(k0, k1)
mapdl.adrag(carc[0], nlp1=l0)
mapdl.aplot(vtk=False)
mapdl.aplot(show_lines=True, line_width=5, show_bounds=True, smooth_shading=True)


###############################################################################
# APDL Command: ASBA
# ~~~~~~~~~~~~~~~~~~
# 从一个 ``1 x 1`` 矩形中减去一个 ``0.5 x 0.5`` 矩形。
mapdl.clear()
mapdl.prep7()

anum0 = mapdl.blc4(0, 0, 1, 1)
anum1 = mapdl.blc4(0.25, 0.25, 0.5, 0.5)
aout = mapdl.asba(anum0, anum1)
mapdl.aplot(vtk=False)
mapdl.aplot(show_lines=True, line_width=5, show_bounds=True, cpos="xy")


###############################################################################
# Area IDs
# ~~~~~~~~
# 返回一个 area ID 数组
anum = mapdl.geometry.anum
anum


###############################################################################
# Area Geometry
# ~~~~~~~~~~~~~
# 获取包含 area 的 VTK ``Multiblock`` 网格。这个 VTK 网格可以保存或绘制。更多信息，请参阅 `Pyvista 文档 <pyvista_docs_>`_ 。
#
areas = mapdl.geometry.areas
areas


###############################################################################
# Merged Area Geometry
# ~~~~~~~~~~~~~~~~~~~~
# 您还可以以 ``pyvista.PolyData`` 对象的形式获取 area 。
#
# 请注意，这是一种方法。您可以选择 area 的质量（网格密度），以及想要合并输出还是单独网格。

area = mapdl.geometry.get_areas(quality=3)
area

# 可选择保存或绘制 area 
# area.save('mesh.vtk')
area.plot()


###############################################################################
# Area Selection
# ~~~~~~~~~~~~~~
# 有两种选择 area 的方法，一种是旧的 "传统" 风格，另一种是新的风格。对于那些熟悉现有 MAPDL 命令的人来说，旧式方法很有价值，而新式方法则适用于以 pythonic 方式选择 area 。
#
# 此示例生成一系列随机 area 并选择它们
mapdl.clear()
mapdl.prep7()


def generate_random_area():
    start_x, start_y, height, width = np.random.random(4)
    mapdl.blc4(start_x * 10, start_y * 10, height, width)


# create 20 random rectangles
for i in range(20):
    generate_random_area()

# Print the area numbers
print(mapdl.geometry.anum)


###############################################################################
# 使用旧式命令选择其他 area 。
mapdl.asel("S", "AREA", "", 1, 20, 2)
print(mapdl.geometry.anum)


###############################################################################
# 使用新式命令选择其他 area 。
#
# Note that the Area IDs are 1 based in MAPDL, while Python ranges are 0 based.
mapdl.geometry.area_select(range(1, 21, 2))
print(mapdl.geometry.anum)


###############################################################################
# Select areas from a list
#
# 请注意，如果您想查看所选内容，可以 ``return_selected`` 。这在从现有 area 重新选择时非常有用。
items = mapdl.geometry.area_select([1, 5, 10, 20], return_selected=True)
print(items)


###############################################################################
# APDL Command: APLOT
# ~~~~~~~~~~~~~~~~~~~
# 该方法使用 VTK 和 pyvista 生成动态 3D 图形。
#
# 所有常见的绘图方法都有多种绘图选项。在此，我们将启用边界并显示绘图线，同时使用 ``quality`` 参数提高绘图质量。
#
# 请注意， ``"cpos"``` 关键字参数可用于描述以下摄像机方向：
#
# - ``iso`` - Isometric view
# - ``xy`` - XY Plane view
# - ``xz`` - XZ Plane view
# - ``yx`` - YX Plane view
# - ``yz`` - YZ Plane view
# - ``zx`` - ZX Plane view
# - ``zy`` - ZY Plane view

mapdl.aplot(quality=1, show_bounds=True, cpos="iso", show_lines=True)

###############################################################################
# Stop mapdl
# ~~~~~~~~~~
#
mapdl.exit()
