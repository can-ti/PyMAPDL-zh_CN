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
.. _ref_modal_beam:

=================================
MAPDL 梁模态分析示例
=================================

本例演示了如何执行简单的模态分析并将分析结果制作成动画。

Objective
~~~~~~~~~
本示例使用 BEAM188 单元建立了一个简单的三维弹性梁模型。这些梁单元由类似于钢的线弹性材料制成，具有矩形截面。


Procedure
~~~~~~~~~

* Launch MAPDL instance
* Material properties
* Geometry
* Finite element model
* Boundary conditions
* Solving the model
* Post-processing
* Stop MAPDL

"""

###############################################################################
# Launch MAPDL instance
# =====================
#
# 启动具有交互式绘图功能的 MAPDL
from ansys.mapdl.core import launch_mapdl

nmodes = 10
# start MAPDL
mapdl = launch_mapdl()
print(mapdl)


###############################################################################
# Define material
# ===============
#
# 定义材料
mapdl.prep7()
mapdl.mp("EX", 1, 2.1e11)
mapdl.mp("PRXY", 1, 0.3)
mapdl.mp("DENS", 1, 7800)

###############################################################################
# Create geometry
# ===============
#
# 创建关键点和线
mapdl.k(1)
mapdl.k(2, 10)
mapdl.l(1, 2)
mapdl.lplot()

###############################################################################
# Define finite element model
# ===========================
#
# 定义单元类型/截面类型 - 矩形梁截面。
mapdl.et(1, "BEAM188")
mapdl.sectype(1, "BEAM", "RECT")
mapdl.secoffset("CENT")
mapdl.secdata(2, 1)

# Mesh the line
mapdl.type(1)
mapdl.esize(1)
mapdl.lesize("ALL")
mapdl.lmesh("ALL")
mapdl.eplot()
mapdl.finish()

###############################################################################
# Specify boundary conditions
# ===========================
#
# 固定端
mapdl.solution()  # Entering the solution processor.
mapdl.nsel("S", "LOC", "X", "0")
mapdl.d("ALL", "ALL")
mapdl.allsel()
mapdl.nplot(plot_bc=True, nnum=True)

###############################################################################
# Solve the model
# ===============
#
# Setting modal analysis
mapdl.antype("MODAL")
mapdl.modopt("LANB", nmodes, 0, 200)
mapdl.solve()
mapdl.finish()

###############################################################################
# Postprocess
# ===========
#
# Enter the post processor (post1)
mapdl.post1()
output = mapdl.set("LIST")
print(output)

result = mapdl.result

###############################################################################
# 结果动画

mode2plot = 2
normalizeDisplacement = 1 / result.nodal_displacement(mode2plot - 1)[1].max()

result.plot_nodal_displacement(
    mode2plot,
    show_displacement=True,
    displacement_factor=normalizeDisplacement,
    n_colors=10,
)

result.animate_nodal_displacement(
    mode2plot,
    loop=False,
    add_text=False,
    n_frames=100,
    displacement_factor=normalizeDisplacement,
    show_axes=False,
    background="w",
    movie_filename="animation.gif",
    off_screen=True,
)

###############################################################################
# Stop MAPDL
# ==========
#
mapdl.finish()
mapdl.exit()
