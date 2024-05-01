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
.. _ref_lathe_cutter_example:

=====================================
车床刀具结构分析
=====================================

介绍 PyMAPDL 的基本功能。

Objective
=========

本示例的目的是通过车刀有限元模型来突出 PyMAPDL 的一些常用功能。
车床铣刀有多种磨损和失效途径，支持其设计的分析通常是瞬态热结构分析。
不过，为了简单起见，本仿真示例使用了非均匀载荷。

.. figure:: ../../../_static/lathe_cutter_model.png
    :align: center
    :width: 600
    :alt:  Lathe cutter geometry and load description.
    :figclass: align-center

    **Figure 1: 车床铣刀几何形状和负载描述**



Contents
========

1. **变量和启动：** 
   定义必要的变量并启动 MAPDL。

2. **几何、网格和 MAPDL 参数：** 
   导入几何体并检查 MAPDL 参数。使用 Python 变量定义线性弹性材料模型。绘制网格并应用对称边界条件。

3. **坐标系和载荷：** 
   为外加载荷创建局部坐标系，并通过绘图进行验证。

4. **压力负荷：** 
   使用 numpy 数组将压力负荷定义为应用区域长度的正弦函数。将压力数组作为表数组导入 MAPDL。验证应用载荷并求解。

5. **绘图：**
   显示结果绘图、选择绘图以及使用绘图图例。

6. **后处理：**
   列出结果的两种方法：使用 PyMAPDL 和 Pythonic 版本的 APDL。演示扩展方法和将列表写入文件。

7. **高级绘图：**
   使用 :class:`pyvista.UnstructuredGrid` 进行额外的后处理。


Step 1: Variables and launch
============================

定义变量并启动 MAPDL。
"""

import os

import numpy as np

from ansys.mapdl.core import launch_mapdl
from ansys.mapdl.core.examples.downloads import download_example_data

# cwd = current working directory 当前工作目录
path = os.getcwd()
print(path)
PI = np.pi
EXX = 1.0e7
NU = 0.27

###############################################################################
# 常用的 MAPDL 命令行选项在 :func:`ansys.mapdl.core.launcher.launch_mapdl` 中以 Pythonic 参数名公开。
# 例如， ``-dir`` 变成了 ``run_location`` 。您可以使用 ``run_location`` 指定 MAPDL 的运行位置。例如
#
# .. code:: python
#
#    mapdl = launch_mapdl(run_location=path)
#
# 否则，MAPDL 的工作目录将存储在 ``mapdl.directory`` 中。在这个目录中，MAPDL 将创建我们稍后要展示的一些图像。
#
# 没有 Pythonic 版本的选项可以通过 ``additional_switches`` 参数访问。
# 这里使用 ``-smp`` 只是为了尽量减少求解器文件的数量。

mapdl = launch_mapdl(additional_switches="-smp")

###############################################################################
# Step 2: Geometry, mesh, and MAPDL parameters
# ============================================
#
# - 导入几何体并检查 MAPDL 参数。
# - 定义材料和网格，然后创建边界条件。
#

# 首先，重置 MAPDL 数据库。
mapdl.clear()

###############################################################################
# 导入几何体文件并列出所有 MAPDL 参数。
lathe_cutter_geo = download_example_data("LatheCutter.anf", "geometry")
mapdl.input(lathe_cutter_geo)
mapdl.finish()
print(mapdl.parameters)

###############################################################################
# 在载荷定义中使用单位长度的压力面积。
pressure_length = mapdl.parameters["PRESS_LENGTH"]

print(mapdl.parameters)

###############################################################################
# 更改单位和标题。
mapdl.units("Bin")
mapdl.title("Lathe Cutter")

###############################################################################
# 设置材料属性
mapdl.prep7()
mapdl.mp("EX", 1, EXX)
mapdl.mp("NUXY", 1, NU)

###############################################################################
# MAPDL 单元类型 ``SOLID285`` 用于演示目的。请考虑在实际应用中使用适当的单元类型或网格密度。

mapdl.et(1, 285)
mapdl.smrtsize(4)
mapdl.aesize(14, 0.0025)
mapdl.vmesh(1)

mapdl.da(11, "symm")
mapdl.da(16, "symm")
mapdl.da(9, "symm")
mapdl.da(10, "symm")

###############################################################################
# Step 3: Coordinate system and load
# ==============================================
#
# 创建一个局部坐标系（CS），将施加的压力作为局部坐标轴 X 的函数。
#
# 局部坐标系 ID = 11

mapdl.cskp(11, 0, 2, 1, 13)
mapdl.csys(1)
mapdl.view(1, -1, 1, 1)
mapdl.psymb("CS", 1)
mapdl.vplot(
    color_areas=True,
    show_lines=True,
    cpos=[-1, 1, 1],
    smooth_shading=True,
)

###############################################################################
#
# VTK 图形不显示 MAPDL 图形符号。
# 不过，要使用 MAPDL 绘图功能，可以将关键字选项 ``vtk`` 设为 ``False`` 。

mapdl.lplot(vtk=False)

###############################################################################
# Step 4: Pressure load
# =================================
#
# 创建压力载荷，将其作为表数组载入 MAPDL，验证载荷并求解。

# pressure_length = 0.055 inch

pts = 10
pts_1 = pts - 1

length_x = np.arange(0, pts, 1)
length_x = length_x * pressure_length / pts_1

press = 10000 * (np.sin(PI * length_x / pressure_length))

###############################################################################
# ``length_x`` 和 ``press`` 是一个向量。要将它们组合成定义 MAPDL 表数组所需的正确形式，可以使用 `numpy.stack <https://numpy.org/doc/stable/reference/generated/numpy.stack.html>`_ 。

press = np.stack((length_x, press), axis=-1)
mapdl.load_table("MY_PRESS", press, "X", csysid=11)

mapdl.asel("S", "Area", "", 14)
mapdl.nsla("S", 1)
mapdl.sf("All", "Press", "%MY_PRESS%")
mapdl.allsel()

###############################################################################
# 您可以打开 MAPDL GUI 检查模型。
#
# .. code:: python
#
#     mapdl.open_gui()
#
#

###############################################################################
# 设置求解。
mapdl.finish()
mapdl.slashsolu()
mapdl.nlgeom("On")
mapdl.psf("PRES", "NORM", 3, 0, 1)
mapdl.view(1, -1, 1, 1)
mapdl.eplot(vtk=False)

###############################################################################
# 求解模型。
mapdl.solve()
mapdl.finish()
if mapdl.solution.converged:
    print("The solution has converged.")

###############################################################################
# Step 5: Plotting
# ================
#

mapdl.post1()
mapdl.set("last")
mapdl.allsel()

mapdl.post_processing.plot_nodal_principal_stress("1", smooth_shading=False)

###############################################################################
# Plotting - Part of Model
# ------------------------
#

mapdl.csys(1)
mapdl.nsel("S", "LOC", "Z", -0.5, -0.141)
mapdl.esln()
mapdl.nsle()
mapdl.post_processing.plot_nodal_principal_stress(
    "1", edge_color="white", show_edges=True
)

###############################################################################
# Plotting - Legend Options
# -------------------------
#

mapdl.allsel()
sbar_kwargs = {
    "color": "black",
    "title": "1st Principal Stress (psi)",
    "vertical": False,
    "n_labels": 6,
}
mapdl.post_processing.plot_nodal_principal_stress(
    "1",
    cpos="xy",
    background="white",
    edge_color="black",
    show_edges=True,
    scalar_bar_args=sbar_kwargs,
    n_colors=9,
)

###############################################################################
# 让我们从 `PyVista 文档 <pyvista_docs_>`_ 中试用一些标量条选项。
# 例如，在米色背景上设置黑色文字。
#
# 定义为 Python 字典的标量条关键字是使用 {key:value} 的另一种方法。
# 您也可以使用 “单击并拖动” 方法重新定位标量栏。
# 试着按住鼠标左键，同时移动鼠标。

sbar_kwargs = dict(
    title_font_size=20,
    label_font_size=16,
    shadow=True,
    n_labels=9,
    italic=True,
    bold=True,
    fmt="%.1f",
    font_family="arial",
    title="1st Principal Stress (psi)",
    color="black",
)

mapdl.post_processing.plot_nodal_principal_stress(
    "1",
    cpos="xy",
    edge_color="black",
    background="beige",
    show_edges=True,
    scalar_bar_args=sbar_kwargs,
    n_colors=256,
    cmap="jet",
)

# cmap 名称 *_r 通常会反转值。试试 cmap='jet_r'


###############################################################################
# Step 6: Postprocessing
# =======================
#
# Results List
# ------------
#
# 得到所有的节点主应力。
mapdl.post_processing.nodal_principal_stress("1")

###############################################################################
# 获取节点子集的主节点应力。
mapdl.nsel("S", vmin=1200, vmax=1210)
mapdl.esln()
mapdl.nsle()

print("The node numbers are:")
print(mapdl.mesh.nnum)  # get node numbers

print("The principal nodal stresses are:")
mapdl.post_processing.nodal_principal_stress("1")

###############################################################################
# Results as lists, arrays, and DataFrames
# -----------------------------------------
# 使用 :meth:`mapdl.prnsol` 检查
print(mapdl.prnsol("S", "PRIN"))

###############################################################################
# 使用此命令可以将其转换为 list 类型。
mapdl_s_1_list = mapdl.prnsol("S", "PRIN").to_list()
print(mapdl_s_1_list)

###############################################################################
# 使用此命令可以将其转换为 array 类型：
mapdl_s_1_array = mapdl.prnsol("S", "PRIN").to_array()
print(mapdl_s_1_array)

###############################################################################
# 或转换为为 DataFrame：
mapdl_s_1_df = mapdl.prnsol("S", "PRIN").to_dataframe()
mapdl_s_1_df.head()

###############################################################################
# 使用该命令可以以 DataFrame 的形式获取数据，DataFrame 是一种 `Pandas 数据类型 <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html>`_ 。由于已导入 Pandas 模块，因此可以使用其函数。例如，可以将主应力写入文件。

# mapdl_s_1_df.to_csv(path + '\prin-stresses.csv')
# mapdl_s_1_df.to_json(path + '\prin-stresses.json')
mapdl_s_1_df.to_html(path + "\prin-stresses.html")

###############################################################################
# Step 7: Advanced plotting
# =========================
#

mapdl.allsel()
principal_1 = mapdl.post_processing.nodal_principal_stress("1")

###############################################################################
# 将结果加载到 VTK grid 中。
grid = mapdl.mesh.grid
grid["p1"] = principal_1

sbar_kwargs = {
    "color": "black",
    "title": "1st Principal Stress (psi)",
    "vertical": False,
    "n_labels": 6,
}

###############################################################################
# 沿 XY 平面生成单个水平切片。
#
# .. note::
#    PyVista 的 ``eye_dome_lighting`` 方法用于增强切片的绘图效果。更多信息，请参阅 `Eye Dome Lighting <pyvista_eye_dome_lighting_>`_ 。

single_slice = grid.slice(normal=[0, 0, 1], origin=[0, 0, 0])
single_slice.plot(
    scalars="p1",
    background="white",
    lighting=False,
    eye_dome_lighting=True,
    show_edges=False,
    cmap="jet",
    n_colors=9,
    scalar_bar_args=sbar_kwargs,
)

###############################################################################
# 生成带有三个切平面的绘图。
slices = grid.slice_orthogonal()
slices.plot(
    scalars="p1",
    background="white",
    lighting=False,
    eye_dome_lighting=True,
    show_edges=False,
    cmap="jet",
    n_colors=9,
    scalar_bar_args=sbar_kwargs,
)

###############################################################################
# 在同一平面内生成具有多个切面的网格。
#
slices = grid.slice_along_axis(12, "x")
slices.plot(
    scalars="p1",
    background="white",
    show_edges=False,
    lighting=False,
    eye_dome_lighting=True,
    cmap="jet",
    n_colors=9,
    scalar_bar_args=sbar_kwargs,
)

###############################################################################
# Finally, exit MAPDL.
mapdl.exit()
