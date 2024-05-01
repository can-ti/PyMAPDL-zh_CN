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
.. _ref_basic-geometry-volumes:

Volumes
-------

本例演示了如何使用体积命令创建基本几何体。

"""

import numpy as np

from ansys.mapdl.core import launch_mapdl

# start MAPDL and enter the pre-processing routine
mapdl = launch_mapdl()
mapdl.clear()
mapdl.prep7()
print(mapdl)


###############################################################################
# APDL Command: V
# ~~~~~~~~~~~~~~~
# 通过关键点定义体积。

# 创建一个简单的立方体。

k0 = mapdl.k("", 0, 0, 0)
k1 = mapdl.k("", 1, 0, 0)
k2 = mapdl.k("", 1, 1, 0)
k3 = mapdl.k("", 0, 1, 0)
k4 = mapdl.k("", 0, 0, 1)
k5 = mapdl.k("", 1, 0, 1)
k6 = mapdl.k("", 1, 1, 1)
k7 = mapdl.k("", 0, 1, 1)
v0 = mapdl.v(k0, k1, k2, k3, k4, k5, k6, k7)
mapdl.vplot(show_lines=True)


###############################################################################
# 创建一个三棱柱体
mapdl.clear()
mapdl.prep7()

k0 = mapdl.k("", 0, 0, 0)
k1 = mapdl.k("", 1, 0, 0)
k2 = mapdl.k("", 1, 1, 0)
k3 = mapdl.k("", 0, 1, 0)
k4 = mapdl.k("", 0, 0, 1)
k5 = mapdl.k("", 1, 0, 1)
k6 = mapdl.k("", 1, 1, 1)
k7 = mapdl.k("", 0, 1, 1)
v1 = mapdl.v(k0, k1, k2, k2, k4, k5, k6, k6)
mapdl.vplot(show_lines=True)


###############################################################################
# Create a triangular prism
mapdl.clear()
mapdl.prep7()

k0 = mapdl.k("", 0, 0, 0)
k1 = mapdl.k("", 1, 0, 0)
k2 = mapdl.k("", 1, 1, 0)
k3 = mapdl.k("", 0, 0, 1)
v0 = mapdl.v(k0, k1, k2, k2, k3, k3, k3, k3)
mapdl.vplot(show_lines=True)


###############################################################################
# APDL Command: VA
# ~~~~~~~~~~~~~~~~
# 生成一个以现有 area 为边界的体积。
#
# 创建一个以 4 个 area 为边界的简单四面体
mapdl.clear()
mapdl.prep7()
k0 = mapdl.k("", -1, 0, 0)
k1 = mapdl.k("", 1, 0, 0)
k2 = mapdl.k("", 1, 1, 0)
k3 = mapdl.k("", 1, 0.5, 1)

# create faces
a0 = mapdl.a(k0, k1, k2)
a1 = mapdl.a(k0, k1, k3)
a2 = mapdl.a(k1, k2, k3)
a3 = mapdl.a(k0, k2, k3)

# 生成并绘制体积
vnum = mapdl.va(a0, a1, a2, a3)
mapdl.aplot(show_lines=True, show_bounds=True)


###############################################################################
# APDL Command: VDRAG
# ~~~~~~~~~~~~~~~~~~~
# 通过沿路径拖动 area 生成体积。
#
# 创建一个带孔的正方形，然后沿弧线拖动。
mapdl.clear()
mapdl.prep7()

# 创建一个带孔的正方形。
anum0 = mapdl.blc4(0, 0, 1, 1)
anum1 = mapdl.blc4(0.25, 0.25, 0.5, 0.5)
aout = mapdl.asba(anum0, anum1)

k0 = mapdl.k("", 0, 0, 0)
k1 = mapdl.k("", 1, 0, 1)
k2 = mapdl.k("", 1, 0, 0)
l0 = mapdl.larc(k0, k1, k2, 2)
mapdl.vdrag(aout, nlp1=l0)
mapdl.vplot(show_lines=True, quality=5)


###############################################################################
# APDL Command: VEXT
# ~~~~~~~~~~~~~~~~~~
# 通过拉伸 area 生成其他体积。
#
# 挤出一个圆，创建一个基本圆柱体。
mapdl.clear()
mapdl.prep7()

# first, create an area from a circle
k0 = mapdl.k("", 0, 0, 0)
k1 = mapdl.k("", 0, 0, 1)
k2 = mapdl.k("", 0, 0, 0.5)
carc0 = mapdl.circle(k0, 1, k1)
a0 = mapdl.al(*carc0)

# next, extrude it and plot it
mapdl.vext(a0, dz=4)
mapdl.vplot(show_lines=True, quality=5)


###############################################################################
# 使用 ``rx`` 和 ``ry`` 参数创建锥形圆柱体。
mapdl.vdele("all")
mapdl.vext(a0, dz=4, rx=0.3, ry=0.3, rz=1)
mapdl.vplot(show_lines=True, quality=5)


###############################################################################
# APDL Command: VROTAT
# ~~~~~~~~~~~~~~~~~~~~
# 通过绕轴旋转面积图案生成圆柱体积。
#
# 围绕 Z 轴旋转一个圆，创建一个环形图案
mapdl.clear()
mapdl.prep7()

# 首先，从圆创建一个 area 
hoop_radius = 10
hoop_thickness = 0.5
k0 = mapdl.k("", hoop_radius, 0, 0)
k1 = mapdl.k("", hoop_radius, 1, 0)
k2 = mapdl.k("", hoop_radius, 0, hoop_thickness)
carc0 = mapdl.circle(k0, 1, k1)
a0 = mapdl.al(*carc0)

# define a Z-axis
k_axis0 = mapdl.k("", 0, 0, 0)
k_axis1 = mapdl.k("", 0, 0, 1)

# 围绕 Z 轴旋转。默认情况下，它将旋转 360 度
mapdl.vrotat(a0, pax1=k_axis0, pax2=k_axis1)
mapdl.vplot(show_lines=True, quality=5)


###############################################################################
# APDL Command: VSYMM
# ~~~~~~~~~~~~~~~~~~~~
# 通过对称反射从体积生成体积。
#
# 通过在 YZ 平面和 XZ 平面上反射单个图块，创建四个图块。
mapdl.clear()
mapdl.prep7()

vnum = mapdl.blc4(1, 1, 1, 1, depth=1)
mapdl.vsymm("X", vnum)
mapdl.vsymm("Y", "ALL")

mapdl.vplot(show_lines=True, show_bounds=True)


###############################################################################
# Volume IDs
# ~~~~~~~~~~
# 返回一个 volume 编号数组。
vnum = mapdl.geometry.vnum
vnum


###############################################################################
# Volume Geometry
# ~~~~~~~~~~~~~~~
# 可通过 ``geometry.volumes`` 方法访问体积几何图形。
volume_mesh = mapdl.geometry.volumes
volume_mesh


###############################################################################
# Volume Selection
# ~~~~~~~~~~~~~~~~
# 选择 volume 有两种方法，一种是旧的 "传统" 风格，另一种是新的风格。旧式方法对于那些熟悉现有 MAPDL 命令的人来说很有价值，而新式方法则适用于以 pythonic 方式选择 volume 。
#
# 此示例生成一系列随机 volume ，并选择它们
mapdl.clear()
mapdl.prep7()


def generate_random_volume():
    start_x, start_y, height, width, depth = np.random.random(5)
    mapdl.blc4(start_x * 10, start_y * 10, height, width, depth)


# create 20 random volumes
for _ in range(20):
    generate_random_volume()

# Print the volume numbers
print(mapdl.geometry.vnum)


###############################################################################
# 使用旧式命令每隔一个选择 volume 。
mapdl.vsel("S", "VOLU", "", 1, 20, 2)
print(mapdl.geometry.vnum)


###############################################################################
# 使用新样式命令每隔一个选择 volume 。
#
# 请注意，在 MAPDL 中，Item ID 以 1 为基础，而 Python 范围以 0 为基础。
mapdl.geometry.volume_select(range(1, 21, 2))
print(mapdl.geometry.vnum)


###############################################################################
# 以列表方式选择 volume
#
# 请注意，如果您想查看所选内容，可以``return_selected``。这在从现有 volume 重新选择时非常有用。
#
# 注意，这里也可以使用 numpy 数组。
items = mapdl.geometry.volume_select([1, 5, 10, 20], return_selected=True)
print(items)


###############################################################################
# APDL Command: VPLOT
# ~~~~~~~~~~~~~~~~~~~
# 在显示关键点编号的同时绘制彩色 volume 图。
#
# 所有常见的绘图方法都有多种绘图选项。

mapdl.clear()
mapdl.prep7()

# 创建基本的几何演示
mapdl.cyl4(xcenter=0, ycenter=0, rad1=1, theta1=0, rad2=2, depth=1)
mapdl.vsymm("Y", "ALL")

# 在显示边界的同时进行绘图，并禁用额外的线条绘图。
mapdl.vplot(show_bounds=True, show_lines=False, quality=1)
mapdl.vplot(vtk=False)

###############################################################################
# Stop mapdl
# ~~~~~~~~~~
#
mapdl.exit()
