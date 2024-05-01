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
.. _ref_element_size_transition:

MAPDL 单元尺寸转换示例
-------------------------------------

本例向您展示如何使用 PyMAPDL 控制网格密度。

在很多情况下，您需要控制局部高应力区域附近的网格密度（如模拟裂缝、滤波支架等）。
这通常会在网格中引入单元尺寸的急剧变化。本例使用简单几何体演示了减少这种影响的一种方法。

首先，将 MAPDL 作为服务启动。
"""
# sphinx_gallery_thumbnail_number = 3

from ansys.mapdl.core import launch_mapdl

mapdl = launch_mapdl()
print(mapdl)

###############################################################################
# The Geometry (a box)
# ~~~~~~~~~~~~~~~~~~~~
# 本例使用非常简单的几何图形。在本例中，是一个有 4 个边的 3D box。
# 剩下的两个边是开放的，我们就得到了一个矩形管，其尺寸为 5 x 5 x 1。我们使用 8 个关键点创建，然后构建 4 个 area。
#

mapdl.prep7()

k0 = mapdl.k(1, 0, 0, 0)
k1 = mapdl.k(2, 0, 5, 0)
k2 = mapdl.k(3, 5, 5, 0)
k3 = mapdl.k(4, 5, 0, 0)

k4 = mapdl.k(5, 0, 0, 1)
k5 = mapdl.k(6, 0, 5, 1)
k6 = mapdl.k(7, 5, 5, 1)
k7 = mapdl.k(8, 5, 0, 1)

a0 = mapdl.a(1, 2, 3, 4)
a1 = mapdl.a(5, 6, 7, 8)
a2 = mapdl.a(3, 4, 8, 7)
a3 = mapdl.a(1, 2, 6, 5)


###############################################################################
# Mesh size
# ~~~~~~~~~
# 我们将全局网格大小设置为 0.7，但我们对面 ``a2`` 特别感兴趣，因此将该面的单元大小设置为 0.1。然后，我们只需指定单元类型（此处使用 ``SHELL181`` ），并对几何体进行网格划分。
#
# 此外，我们使用 ``mshape`` 指定我们需要的三角形单元。这纯粹是为了演示效果。这对四边形网格同样有效。
#

mapdl.esize(0.7)
mapdl.aesize(a2, 0.1)
mapdl.mshape(1, "2D")

mapdl.et(1, "SHELL181")
mapdl.amesh("ALL")
mapdl.eplot(show_edges=True, show_axes=False, line_width=2, background="w")

###############################################################################
# Smoothing the transition 
# ~~~~~~~~~~~~~~~~~~~~~~~~
#
# 平滑过渡
#
# 大部分网格看起来都很好，但在焦点区域的边缘，单元尺寸的变化非常明显。这很可能是不可取的，因为这些是边角区域，通常需要更高的精度。不过这一点很容易解决。
#
# 为此，我们需要将绑定 a2 的关键点的单元大小也设置为 0.1。这将把这些关键点附近的所有单元都设置为 0.1，包括不在 ``a2`` 上的单元。这样就可以将过渡从边缘分散开来。
#
# 为了演示这一点，我们首先使用 aclear 清除现有网格。然后使用 kesize 设置关键点单元大小，最后重新网格。结果不言而喻。
#

mapdl.aclear("ALL")
for k in [k2, k3, k6, k7]:
    mapdl.kesize(k, 0.1)
mapdl.amesh("ALL")
mapdl.eplot(show_edges=True, show_axes=False, line_width=2, background="w")

###############################################################################
# Smoothing the transition into a2
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 同样，如果我们希望减小 ``a2`` 边缘的网格尺寸，我们可以将关键点单元尺寸设置为一个中间值，这样就可以将尺寸转换的主要位置转移到 ``a2`` 面内。
#

mapdl.aclear("ALL")
for k in [k2, k3, k6, k7]:
    mapdl.kesize(k, 0.2)
mapdl.amesh("ALL")
mapdl.eplot(vtk=True, show_edges=True, show_axes=False, line_width=2, background="w")


###############################################################################
# Stop mapdl
# ~~~~~~~~~~
#
mapdl.exit()
