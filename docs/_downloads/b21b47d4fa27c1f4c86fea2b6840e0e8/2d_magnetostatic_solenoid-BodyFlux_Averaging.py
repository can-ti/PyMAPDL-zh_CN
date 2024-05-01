# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# 特此允许任何获得本软件副本及相关文档文件（以下简称 "软件"）的人不受限制地使用本软件，
# 包括但不限于使用、复制、修改、合并、出版、分发、再许可和/或出售本软件副本的权利，
# 以及允许获得本软件的人在符合以下条件的情况下使用本软件：
#
# 上述版权声明和本许可声明应包含在本软件的所有副本或实质部分中。
#
# 本软件按 "原样" 提供，不作任何明示或暗示的保证，包括但不限于适销性、特定用途适用性和非侵权保证。
# 在任何情况下，作者或版权所有者均不对因本软件或本软件的使用或其他交易而产生、引起或与之相关的任何索赔、
# 损害赔偿或其他责任承担责任，无论是合同诉讼、侵权诉讼还是其他诉讼。

"""
.. _ref_solenoid_magnetostatic_2d:

=======================================
2D 静磁螺线管分析
=======================================


本示例展示了如何收集和绘制单元间材料不连续的结果（Power graphics style）与默认的全平均结果（Full graphics style）。


Description
===========

MAPDL 有两种显示结果的平均方法。尽管还存在其他差异，但以下描述说明了主要差异。

* **Full graphics**: 使用节点平均结果显示整个选定模型。
  如果两个或多个不同材料的单元共享一个节点，应力场在单元材料边界（共享节点）上是连续的。

* **Power graphics**: 显示所选模型的全部结果，包括同一材料单元内的平均结果和跨材料边界的不连续结果。

本示例的重点是材料边界。

原生 PyMAPDL 的后处理与 MAPDL 的 "Full graphics" 方法在材料边界方面类似。

螺线管的几何形状如图 1 所示。

.. figure:: ../../../_static/model_solenoid_2d.png
    :align: center
    :width: 600
    :alt:  电磁阀几何形状说明
    :figclass: align-center

    **Figure 1: 电磁阀几何形状说明**

载荷和边界条件
-----------------------------

线圈的电流密度为 650 匝，每匝 1 安培。
所有外部节点的 Z 磁矢量势均设为零，强制执行磁通平行条件。

导入模块
==============

除常规库外，还导入了 Matplotlib 和 PyVista。由于要使用 MAPDL 默认的等高线颜色样式，因此要导入 Matplotlib。然后通过 PyVista 设置 Power Graphics 风格曲线图。

"""
# sphinx_gallery_thumbnail_path = './_static/model_solenoid_2d.png'

import numpy as np
import pyvista as pv

from ansys.mapdl.core import launch_mapdl

###############################################################################
# Launch MAPDL service
# ====================
#
mapdl = launch_mapdl()

mapdl.clear()
mapdl.prep7()
mapdl.title("2-D Solenoid Actuator Static Analysis")

###############################################################################
# Set up the FE model
# ===================
#
# 定义几何体、载荷和网格大小的参数值。
# 模型以厘米为单位，然后按比例放大到米。
#
# “Plane233” 单元类型用于二维磁静力分析。

mapdl.et(1, "PLANE233")  # 将 PLANE233 定义为单元类型
mapdl.keyopt(1, 3, 1)  # 使用轴对称分析选项
mapdl.keyopt(1, 7, 1)  # Condense forces at the corner nodes

###############################################################################
# Set material properties
# -----------------------
#
# 单位采用国际单位制。
#
mapdl.mp("MURX", 1, 1)  # 定义材料特性（渗透性），空气
mapdl.mp("MURX", 2, 1000)  # Permeability of backiron
mapdl.mp("MURX", 3, 1)  # Permeability of coil
mapdl.mp("MURX", 4, 2000)  # Permeability of armature

###############################################################################
# Set parameters
# --------------
#
# 为几何设计设置参数。

n_turns = 650  # 线圈匝数
i_current = 1.0  # 每匝电流
ta = 0.75  # 模型尺寸（厘米）
tb = 0.75
tc = 0.50
td = 0.75
wc = 1
hc = 2
gap = 0.25
space = 0.25
ws = wc + 2 * space
hs = hc + 0.75
w = ta + ws + tc
hb = tb + hs
h = hb + gap + td
acoil = wc * hc  # 线圈横截面积（cm**2）
jdens = n_turns * i_current / acoil  # 电流密度（A/cm**2）

smart_size = 4  # 网格划分的智能尺寸等级

###############################################################################
# Create geometry
# ---------------
#
# 创建模型几何体

mapdl.rectng(0, w, 0, tb)  # 创建矩形区域
mapdl.rectng(0, w, tb, hb)
mapdl.rectng(ta, ta + ws, 0, h)
mapdl.rectng(ta + space, ta + space + wc, tb + space, tb + space + hc)
mapdl.aovlap("ALL")
mapdl.rectng(0, w, 0, hb + gap)
mapdl.rectng(0, w, 0, h)
mapdl.aovlap("ALL")
mapdl.numcmp("AREA")  # 压缩未使用的 area 编号


###############################################################################
# Mesh
# ----
#
# 设置模型网格。

mapdl.asel("S", "AREA", "", 2)  # Assign attributes to coil
mapdl.aatt(3, 1, 1, 0)

mapdl.asel("S", "AREA", "", 1)  # Assign attributes to armature
mapdl.asel("A", "AREA", "", 12, 13)
mapdl.aatt(4, 1, 1)

mapdl.asel("S", "AREA", "", 3, 5)  # Assign attributes to backiron
mapdl.asel("A", "AREA", "", 7, 8)
mapdl.aatt(2, 1, 1, 0)

mapdl.pnum("MAT", 1)  # Turn material numbers on
mapdl.allsel("ALL")

mapdl.aplot(vtk=False)

###############################################################################
# Mesh
#

mapdl.smrtsize(smart_size)  # Set smart size meshing
mapdl.amesh("ALL")  # Mesh all areas

###############################################################################
# Scale mesh to meters
# --------------------
#
# 将模型缩放至一米大小。

mapdl.esel("S", "MAT", "", 4)  # Select armature elements
mapdl.cm("ARM", "ELEM")  # Define armature as a component
mapdl.allsel("ALL")
mapdl.arscale(na1="all", rx=0.01, ry=0.01, rz=1, imove=1)  # 按比例调整模型至 MKS（米）
mapdl.finish()

###############################################################################
# Loads and boundary conditions
# ------------------------------
#
# 定义载荷和边界条件。

mapdl.slashsolu()

# Apply current density (A/m**2)
mapdl.esel("S", "MAT", "", 3)  # Select coil elements
mapdl.bfe("ALL", "JS", 1, "", "", jdens / 0.01**2)

mapdl.esel("ALL")
mapdl.nsel("EXT")  # Select exterior nodes
mapdl.d("ALL", "AZ", 0)  # Set potentials to zero (flux-parallel)

###############################################################################
# Solve the model
# ===============
#
# 求解静磁分析。

mapdl.allsel("ALL")
mapdl.solve()
mapdl.finish()

###############################################################################
# Postprocessing
# ==============
#
# 打开结果文件，读入最后一组结果

mapdl.post1()
mapdl.file("file", "rmg")
mapdl.set("last")

###############################################################################
#
# 打印节点值
#

print(mapdl.post_processing.nodal_values("b", "x"))

###############################################################################
# Create an MAPDL Power Graphics plot of the X-direction magnetic flux
# --------------------------------------------------------------------
#
# 通过 ``rgb`` 命令将 MAPDL 颜色反转，使背景为白色，文本和单元边缘为黑色。

mapdl.graphics("power")
mapdl.rgb("INDEX", 100, 100, 100, 0)
mapdl.rgb("INDEX", 80, 80, 80, 13)
mapdl.rgb("INDEX", 60, 60, 60, 14)
mapdl.rgb("INDEX", 0, 0, 0, 15)

mapdl.edge(1, 1)
mapdl.show("png")
mapdl.pngr("tmod", 0)

mapdl.plnsol("b", "x")
mapdl.show("")

###############################################################################
# Obtain grid and scalar data
# ---------------------------
#
# 首先，获取模型中唯一材料 ID 的集合

elem_mats = mapdl.mesh.material_type
np.unique(elem_mats)

###############################################################################
# 对于每个唯一的材质 ID ，将选择图元及其节点。“grids” 列表仅附加了这些单元的网格信息，“scalars” 列表附加了节点X方向的磁通量。

grids = []
scalars = []
for mat in np.unique(elem_mats):
    mapdl.esel("s", "mat", "", mat)
    mapdl.nsle()
    grids.append(mapdl.mesh.grid)
    scalars.append(mapdl.post_processing.nodal_values("b", "x"))
mapdl.allsel()

###############################################################################
# 如果有兴趣，可以打印网格列表，并与 mapdl.mesh.grid 的打印结果进行比较。

print(grids)
# print(mapdl.mesh.grid)


###############################################################################
# Color map and result plot
# -------------------------
#
# 由于某些 MAPDL 等高线颜色在标准 Matplotlib 颜色库中并不完全匹配，因此会尝试匹配颜色并使用十六进制 RGBA 数值。
#
# 对于网格列表中的每个项目，都会将网格添加到绘图中，并使用事先定义的颜色图和相同的等高线图例要求 9 种等高线颜色。
#
# 然后显示绘图，它可以很好地重新创建本地绘图。

from ansys.mapdl.core.theme import PyMAPDL_cmap

plotter = pv.Plotter()

for i, grid in enumerate(grids):
    plotter.add_mesh(
        grid,
        scalars=scalars[i],
        show_edges=True,
        cmap=PyMAPDL_cmap,
        n_colors=9,
        scalar_bar_args={
            "color": "black",
            "title": "B Flux X",
            "vertical": False,
            "n_labels": 10,
        },
    )

plotter.set_background(color="white")
_ = plotter.camera_position = "xy"
plotter.show()


###############################################################################
# Exiting MAPDL
# =============
mapdl.graphics("FULL")  # Returning to default mode.
mapdl.exit()
