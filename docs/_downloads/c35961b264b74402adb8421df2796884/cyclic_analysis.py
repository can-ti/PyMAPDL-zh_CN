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
.. _ref_cyclic_analysis_example:

循环对称分析
---------------

本示例使用循环扇形的参数几何创建了一个叶盘，然后对该循环扇形进行模态分析。
然后，我们使用传统的 `MAPDL reader <https://readerdocs.pyansys.com/>`_ 对结果进行后处理，最后使用参数建模器生成另一个循环模型。

我们的第一项任务是创建一个包含 7 个扇区的简单循环模型。

.. image:: ../../../images/cyclic_disc.png

首先，将 MAPDL 作为服务启动。

"""
# sphinx_gallery_thumbnail_number = 3

import numpy as np
import pyvista as pv

from ansys.mapdl.core import launch_mapdl

mapdl = launch_mapdl()


###############################################################################
# Create the Cyclic Sector
# ~~~~~~~~~~~~~~~~~~~~~~~~
# 为我们的循环模型创建一个 "扇形"。
#


def gen_sector(mapdl, sectors): # 这里 `mapdl` 竟然可以当作一个函数里的参数？ ————ff
    """在 MAPDL 中生成一个扇形。"""

    # 厚度
    thickness = 0.003  # 单位：m
    arc_end = 2 * np.pi / sectors
    arc_cent = arc_end / 2

    # 半径
    rad = 0.01  # m
    arc = pv.CircularArc(
        [rad, 0, 0],
        [np.cos(arc_end) * rad, np.sin(arc_end) * rad, 0],
        [0, 0, 0],
    )

    # 内圆
    kp_begin = [rad, 0, 0]
    kp_end = [np.cos(arc_end) * rad, np.sin(arc_end) * rad, 0]
    kp_center = [0, 0, 0]

    # 外圆
    out_rad = 5.2e-2

    # 求出角度，以获得末端相同的弧长
    cent_ang = arc.length / out_rad / 2

    # 内圈
    kp_beg_outer = [
        np.cos(arc_cent - cent_ang) * out_rad,
        np.sin(arc_cent - cent_ang) * out_rad,
        0,
    ]
    kp_end_outer = [
        np.cos(arc_cent + cent_ang) * out_rad,
        np.sin(arc_cent + cent_ang) * out_rad,
        0,
    ]

    mapdl.prep7()
    mapdl.k(0, *kp_center) # 这里*kp_center 将 kp_center 列表中的元素拆分为单独的参数传递给 mapdl.k 函数。
    mapdl.k(0, *kp_begin)
    mapdl.k(0, *kp_end)
    mapdl.k(0, *kp_beg_outer)
    mapdl.k(0, *kp_end_outer)

    # inner arc
    mapdl.l(1, 2)  # left line
    mapdl.l(1, 3)  # right line
    lnum_inter = mapdl.l(2, 3)  # internal line
    mapdl.al("all")

    # outer "blade"
    lnum = [lnum_inter, mapdl.l(4, 5), mapdl.l(2, 4), mapdl.l(3, 5)]
    mapdl.al(*lnum)

    # 按 ``厚度`` 在 Z 方向挤出模型
    mapdl.vext("all", dz=thickness)

# 生成 7 扇形模型中的一个扇形
sectors = 7
gen_sector(mapdl, sectors)

# Volume plot
mapdl.vplot()


###############################################################################
# Make the Model Cyclic
# ~~~~~~~~~~~~~~~~~~~~~
# 运行 :func:`Mapdl.cyclic` 使模型循环运行
#
# 请注意扇形的数量是如何匹配的

output = mapdl.cyclic()
print(f"Expected Sectors: {sectors}")
print(output)


###############################################################################
# Generate the mesh
# ~~~~~~~~~~~~~~~~~
# 使用四面体 SOLID186 生成有限元网格。

# 单元大小为 0.001
esize = 0.001

mapdl.et(1, 186)
mapdl.esize(esize)
mapdl.vsweep("all")

# 绘制有限元网格
mapdl.eplot()


###############################################################################
# Apply Material Properties
# ~~~~~~~~~~~~~~~~~~~~~~~~~

# 定义一种材料（公称钢，单位为 SI，国际单位制）
mapdl.mp("EX", 1, 210e9)  # Elastic moduli in Pa (kg/(m*s**2))
mapdl.mp("DENS", 1, 7800)  # Density in kg/m3
mapdl.mp("NUXY", 1, 0.3)  # Poisson's Ratio

# 将其应用于所有元素
mapdl.emodif("ALL", "MAT", 1)


###############################################################################
# Run the Modal Analysis
# ~~~~~~~~~~~~~~~~~~~~~~
# 让我们获取前 10 阶模态。请注意，这实际上是根据循环边界条件计算 ``(扇区/2)*nmode`` 。

output = mapdl.modal_analysis(nmode=10, freqb=1)
print(output)


###############################################################################
# Get the Results of the Cyclic Modal Analysis
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 将模态分析中的谐波可视化。
#
# 更多详情，请参阅 `Validation of a Modal Work Approach for Forced Response Analysis of Bladed Disks <https://www.mdpi.com/2076-3417/11/12/5437/pdf>`_ 或 `Cyclic Symmetry Analysis Guide <https://ansyshelp.ansys.com/Views/Secured/corp/v222/en/pdf/Ansys_Mechanical_APDL_Cyclic_Symmetry_Analysis_Guide.pdf>`_ 。
#
# .. note::
#    它使用传统的结果读取器(mapdl reader)，该读取器将在某个时候弃用，转而使用 DPF，但我们现在可以用它来制作一些精彩的动画。
#
# 有关循环结果后处理的更多详情，请参阅：
# * `Understanding Nodal Diameters from a Cyclic Model Analysis <https://reader.docs.pyansys.com/version/stable/examples/01-cyclic_results/academic_sector_nd.html>`_
# * `Cyclic symmetry examples <https://dpf.docs.pyansys.com/version/stable/examples/11-cyclic-symmetry/index.html>`_

# 从 MAPDL 中抓取结果对象
result = mapdl.result
print(result)


###############################################################################
# List the Table of Harmonic Indices
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 这是谐波指数表。该表为每个累积模态提供了相应的谐波指数。
print("C. Index   Harmonic Index")
for i, hindex in zip(range(result.n_results), result.harmonic_indices):
    print(f"{i:3d}      {hindex:3d}")


###############################################################################
# Generate an Animation of a Traveling Wave
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 这是循环分析中第一个弯曲的节点直径 1。
#
# 在节点直径为 1 的情况下，我们可以用以下方法得到第一阶摩天（通常是叶片转子的第一种弯曲模式）：
#
# ``mode_num = np.nonzero(result.harmonic_indices == 1)[0][0]``
#

pv.global_theme.background = "w"

_ = result.animate_nodal_displacement(
    11,
    displacement_factor=5e-4,
    movie_filename="traveling_wave11.gif",
    n_frames=30,
    off_screen=True,
    loop=False,
    add_text=False,
    show_scalar_bar=False,
    cmap="jet",
)

###############################################################################
# 这是节点直径 3 的一阶扭转模态。

_ = result.animate_nodal_displacement(
    36,
    displacement_factor=2e-4,
    movie_filename="traveling_wave36.gif",
    n_frames=30,
    off_screen=True,
    loop=False,
    add_text=False,
    show_scalar_bar=False,
    cmap="jet",
)


###############################################################################
# Parametric Geometry
# ~~~~~~~~~~~~~~~~~~~
# 由于我们的几何体创建是脚本化的，因此可以创建任意数量的 "扇形" 结构。让我们用 20 个扇形创建一个更有趣的结构。
#
# 首先，确保清除 MAPDL，以便我们从头开始。

mapdl.clear()
mapdl.prep7()

# 生成 20 个扇形模型中的一个扇形
gen_sector(mapdl, 20)

# make it cyclic
mapdl.cyclic()

# Mesh it
esize = 0.001
mapdl.et(1, 186)
mapdl.esize(esize)
mapdl.vsweep("all")

# apply materials
mapdl.mp("EX", 1, 210e9)  # Elastic moduli in Pa (kg/(m*s**2))
mapdl.mp("DENS", 1, 7800)  # Density in kg/m3
mapdl.mp("NUXY", 1, 0.3)  # Poisson's Ratio
mapdl.emodif("ALL", "MAT", 1)

# Run the modal analysis
output = mapdl.modal_analysis(nmode=6, freqb=1)

# 从 MAPDL 中抓取结果对象
result = mapdl.result
print(result)


###############################################################################
# List the Table of Harmonic Indices
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 请注意，这些模式的谐波指数最高可达 10，即 N/2，其中 N 是扇形数。

print("C. Index   Harmonic Index")
for i, hindex in zip(range(result.n_results), result.harmonic_indices):
    print(f"{i:3d}    {hindex:3d}")


###############################################################################
# Plot First Bend for Nodal Diameter 2
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 请注意，由于该模态形状的节点直径为 2，因此可以清楚地看到两条节点线。

result.plot_nodal_displacement(
    12, cpos="xy", cmap="jet", show_scalar_bar=False, add_text=False
)


###############################################################################
# Animate First Bend for Nodal Diameter 2
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 最后，让我们以模态 12 的动画效果结束本示例，它对应于本示例模型第二个节点直径的一阶弯曲。

_ = result.animate_nodal_displacement(
    12,
    displacement_factor=2e-4,
    movie_filename="traveling_wave12.gif",
    n_frames=30,
    off_screen=True,
    loop=False,
    add_text=False,
    show_scalar_bar=False,
    cmap="jet",
)
