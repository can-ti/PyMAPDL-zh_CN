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
.. _ref_3d_bracket_example:

绘图和网格访问
------------------------

PyMAPDL 可以加载基本的 IGES 几何图形进行分析。

本示例演示了如何将基本几何图形加载到 MAPDL 中进行分析，并演示了如何使用内置的 Python 特定绘图功能。

该示例还演示了 PyMAPDL 的一些更高级功能，包括通过 VTK 直接访问网格。

"""
# sphinx_gallery_thumbnail_number = 3

import numpy as np

from ansys.mapdl import core as pymapdl
from ansys.mapdl.core import examples

mapdl = pymapdl.launch_mapdl()


###############################################################################
# Load Geometry
# ~~~~~~~~~~~~~
# 在这里，我们下载一个简单的支架 IGES 文件并将其加载到 MAPDL 中。注意 ``igesin`` 必须在 AUX15 进程中。

# 注意，该方法只返回文件路径
bracket_file = examples.download_bracket()

# 加载支架，然后打印几何图形
mapdl.aux15()
mapdl.igesin(bracket_file)
print(mapdl.geometry)


###############################################################################
# Plotting
# ~~~~~~~~
# PyMAPDL 使用 VTK 和 pyvista 作为绘图后端，以实现远程（使用 2021R1 及更新版本）交互式绘图。
# 常见的绘图方法 (``kplot`` , ``lplot`` , ``aplot`` , ``eplot`` 等) 都有相应 :func:`ansys.mapdl.core.plotting.general_plotter` 函数
# 的兼容命令。您可以使用各种关键字参数配置此方法。例如：
mapdl.lplot(
    show_line_numbering=False,
    background="k",
    line_width=3,
    color="w",
    show_axes=False,
    show_bounds=True,
    title="",
    cpos="xz",
)


###############################################################################
# 您还可以配置一个主题，以便在多个绘图中实现一致的绘图。这些主题参数会覆盖所有未设置的关键字参数。例如

my_theme = pymapdl.MapdlTheme()
my_theme.background = "white"
my_theme.cmap = "jet"  # colormap
my_theme.axes.show = False
my_theme.show_scalar_bar = False

mapdl.aplot(theme=my_theme, quality=8)


###############################################################################
# Accessesing Element and Nodes Pythonically
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PyMAPDL 还支持使用 `eplot` 和 `nplot` 绘制单元和节点图。首先，使用 SOLID187 单元对支架进行网格划分。这些单元非常适合这种几何形状和静态结构分析。

# 设置前处理器、单元类型和大小，并对几何体进行网格划分
mapdl.prep7()
mapdl.et(1, "SOLID187")
mapdl.esize(0.075)
mapdl.vmesh("all")

# 打印网格特征
print(mapdl.mesh)


###############################################################################
# 您可以通过 ``mesh.grid`` 属性以 VTK 网格的形式访问底层有限元网格。

grid = mapdl.mesh.grid
grid


###############################################################################
# 这个 UnstructuredGrid 包含一个功能强大的 API，包括访问节点、单元和原始节点编号的功能，所有这些功能都可以绘制网格，并为网格添加新的属性和数据。

grid.points  # same as mapdl.mesh.nodes


###############################################################################
# 以 VTK 格式表示的单元格

grid.cells


###############################################################################
# 获取网格的节点编号

grid.point_data["ansys_node_num"]


###############################################################################
# 将任意数据保存到网格中

# 必须根据点数调整大小
grid.point_data["my_data"] = np.arange(grid.n_points)
grid.point_data


###############################################################################
# 用您选择的标量绘制该网格。绘制时可以使用相同的 MapdlTheme，因为它与网格绘制器兼容。

# make interesting scalars
scalars = grid.points[:, 2]  # z coordinates

sbar_kwargs = {"color": "black", "title": "Z Coord"}
grid.plot(
    scalars=scalars,
    show_scalar_bar=True,
    scalar_bar_args=sbar_kwargs,
    show_edges=True,
    theme=my_theme,
)


###############################################################################
# 该网格还能以紧凑的跨平台 VTK 格式保存到磁盘中，并再次用 ``pyvista`` 或 ParaView 加载。
#

grid.save('my_mesh.vtk')
import pyvista
imported_mesh = pyvista.read('my_mesh.vtk')

###############################################################################
# Stop mapdl
# ~~~~~~~~~~
#
mapdl.exit()
