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
.. _ref_path_operation:

PyMAPDL 和 MAPDL 中的路径插值操作
----------------------------------------

本教程展示了如何使用 pyansys 和 MAPDL 沿路径进行应力插值。它展示了 `pyvista` 模块执行插值的一些高级功能。

首先，将 MAPDL 作为服务启动，并禁用除错误信息之外的所有功能。
"""
# sphinx_gallery_thumbnail_number = 3

import matplotlib.pyplot as plt
import numpy as np
import pyvista as pv

from ansys.mapdl.core import launch_mapdl

mapdl = launch_mapdl(loglevel="ERROR")

###############################################################################
# MAPDL: 非均匀载荷作用下的梁
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 创建梁，施加载荷，并求解静态问题。
# beam dimensions
width_ = 0.5
height_ = 2
length_ = 10

# simple 3D beam
mapdl.clear()
mapdl.prep7()
mapdl.mp("EX", 1, 70000)
mapdl.mp("NUXY", 1, 0.3)
mapdl.csys(0)
mapdl.blc4(0, 0, 0.5, 2, length_)
mapdl.et(1, "SOLID186")
mapdl.type(1)
mapdl.keyopt(1, 2, 1)
mapdl.desize("", 100)

mapdl.vmesh("ALL")
# mapdl.eplot()

# fixed constraint
mapdl.nsel("s", "loc", "z", 0)
mapdl.d("all", "ux", 0)
mapdl.d("all", "uy", 0)
mapdl.d("all", "uz", 0)

# arbitrary non-uniform load
mapdl.nsel("s", "loc", "z", length_)
mapdl.f("all", "fz", 1)
mapdl.f("all", "fy", 10)
mapdl.nsel("r", "loc", "y", 0)
mapdl.f("all", "fx", 10)
mapdl.allsel()
mapdl.run("/solu")
sol_output = mapdl.solve()

# plot the normalized global displacement
mapdl.post_processing.plot_nodal_displacement(lighting=False, show_edges=True)


###############################################################################
# Post-Processing - MAPDL Path Operation
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 在 MAPDL 中计算路径上的应力，并将结果转换为 numpy 数组

mapdl.post1()
mapdl.set(1, 1)
# mapdl.plesol("s", "int")

# path definition
pl_end = (0.5 * width_, height_, 0.5 * length_)
pl_start = (0.5 * width_, 0, 0.5 * length_)

mapdl.run("width_ = %f" % width_)
mapdl.run("height_ = %f" % height_)
mapdl.run("length_ = %f" % length_)
# 这些命令将 Python 变量 width_、height_ 和 length_ 的值赋给 MAPDL 中的同名变量。
# %f 是一个格式化字符串，用于将浮点数插入到字符串中。

mapdl.run("pl_end = node(0.5*width_, height_, 0.5*length_)")
mapdl.run("pl_start = node(0.5*width_, 0, 0.5*length_)")
mapdl.path("my_path", 2, ndiv=100)
mapdl.ppath(1, "pl_start")
mapdl.ppath(2, "pl_end")

# 将感兴趣的组件映射到路径上。
mapdl.pdef("Sx_my_path", "s", "x")
mapdl.pdef("Sy_my_path", "s", "y")
mapdl.pdef("Sz_my_path", "s", "z")
mapdl.pdef("Sxy_my_path", "s", "xy")
mapdl.pdef("Syz_my_path", "s", "yz")
mapdl.pdef("Szx_my_path", "s", "xz")

# 从 MAPDL 提取路径结果并发送至 numpy 数组
nsigfig = 10

# 调用 mapdl 对象的 header 方法，关闭所有的头部信息。在 ANSYS MAPDL 中，头部信息通常包括日期、时间、标题等，这里全部关闭了。
mapdl.header("OFF", "OFF", "OFF", "OFF", "OFF", "OFF") 

# 调用 mapdl 对象的 format 方法，设置输出格式。这里设置的是科学计数法（"E"），总宽度为 nsigfig + 9，小数部分的位数为 nsigfig。
mapdl.format("", "E", nsigfig + 9, nsigfig)

# 调用 mapdl 对象的 page 方法，设置输出页面的大小。这里设置的是每页 1e9 行，每行 240 字符。
mapdl.page(1e9, "", -1, 240)

path_out = mapdl.prpath(
    "Sx_my_path",
    "Sy_my_path",
    "Sz_my_path",
    "Sxy_my_path",
    "Syz_my_path",
    "Szx_my_path",
)
table = np.genfromtxt(path_out.splitlines()[1:])
print("Numpy Array from MAPDL Shape:", table.shape)
print(table)

###############################################################################
# Comparing with Path Operation Within `pyvista`
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 同样的路径操作也可以在 `pyvista` 中执行，方法是保存生成的应力并存储在底层的 `UnstructuredGrid` 中。
#
# 请注意，MAPDL 和 VTK 的插值方法（两者的插值结果几乎相同）都有轻微的分段行为。VTK 的基本算法是：
#
# .. note::
#
#    一旦找到包含查询点的单元格， `vtkProbeFilter` 就会使用单元格的插值函数来执行插值/计算点的属性。

# same thing in pyvista
rst = mapdl.result
nnum, stress = rst.nodal_stress(0)

# get SYZ stress
stress_yz = stress[:, 5]  # 第 5 列

# 将 YZ 应力分配给结果实例中的底层网格。
# 在本例中，NAN 值必须替换为 0，插值才能成功
stress_yz[np.isnan(stress_yz)] = 0
rst.grid["Stress YZ"] = stress_yz

# 创建一条线并在其上取样
line = pv.Line(pl_start, pl_end, resolution=100)
out = line.sample(rst.grid)  # bug where the interpolation must be run twice
out = line.sample(rst.grid)
# 注：我们本可以使用样条曲线（或任何数据集），并在其上进行插值，而不是简单的直线。

# 绘制 VTK 和 MAPDL 的内插应力图
plt.plot(out.points[:, 1], out["Stress YZ"], "x", label="Stress vtk")
plt.plot(table[:, 0], table[:, 6], label="Stress MAPDL")
plt.legend()
plt.xlabel("Y Position (in.)")
plt.ylabel("Stress YZ (psi)")
plt.show()


###############################################################################
# 2D Slice Interpolation
# ~~~~~~~~~~~~~~~~~~~~~~
# 沿梁绘制二维切片，并将其与该线上的应力一并绘制。
#
# 请注意，该切片发生在该梁的边缘节点之间，由于应力/应变（通常）会外推到 ANSYS 有限元的边缘节点，因此有必要进行插值。

stress_slice = rst.grid.slice("z", pl_start)

# 可以单独绘制
# stress_slice.plot(scalars=stress_slice['Stress YZ'],
#                   scalar_bar_args={'title': 'Stress YZ'})

# 良好的摄像机位置（使用 pl.camera_position 手动确定）
cpos = [(3.2, 4, 8), (0.25, 1.0, 5.0), (0.0, 0.0, 1.0)]
max_ = np.max((out["Stress YZ"].max(), stress_slice["Stress YZ"].max()))
min_ = np.min((out["Stress YZ"].min(), stress_slice["Stress YZ"].min()))
clim = [min_, max_]

pl = pv.Plotter()
pl.add_mesh(
    out,
    scalars=out["Stress YZ"],
    line_width=10,
    clim=clim,
    scalar_bar_args={"title": "Stress YZ"},
)
pl.add_mesh(
    stress_slice,
    scalars="Stress YZ",
    opacity=0.25,
    clim=clim,
    show_scalar_bar=False,
)
pl.add_mesh(rst.grid, color="w", style="wireframe", show_scalar_bar=False)
pl.camera_position = cpos
_ = pl.show()

###############################################################################
# Stop mapdl
# ~~~~~~~~~~
#
mapdl.exit()
