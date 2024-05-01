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
.. _ref_basic-geometry-keypoints:

Keypoints
---------

本例演示了如何使用关键点命令创建基本几何体。

本节的重点是创建“关键点”。

"""

import numpy as np

from ansys.mapdl.core import launch_mapdl

# 启动 MAPDL 并进入前处理
mapdl = launch_mapdl()
mapdl.clear()
mapdl.prep7()
print(mapdl)


###############################################################################
# APDL Command: K
# ~~~~~~~~~~~~~~~
# 在 ``[0, 0, 0]`` 创建一个关键点。请注意，第一个值是空字符串，以便 MAPDL 自动选择关键点编号。
k0 = mapdl.k("", 0, 0, 0)
print(k0)


###############################################################################
# 在 (10, 11, 12) 处创建关键点，同时指定关键点编号。
k1 = mapdl.k(2, 1, 0, 0)
print(k1)


###############################################################################
# APDL Command: KBETW
# ~~~~~~~~~~~~~~~~~~~
# 在两个关键点之间创建关键点
k2 = mapdl.kbetw(kp1=k0, kp2=k1)
print(k2)


###############################################################################
# APDL Command: KCENTER
# ~~~~~~~~~~~~~~~~~~~~~
# 在由三个位置定义的圆弧中心创建关键点。
# 请注意，在生成这个几何体之前，我们首先要 clear mapdl
mapdl.clear()
mapdl.prep7()
k0 = mapdl.k("", 0, 1, 0)
k1 = mapdl.k("", 1, 0, 0)
k2 = mapdl.k("", 0, -1, 0)
k3 = mapdl.kcenter("KP", k0, k1, k2)
print([k0, k1, k2, k3])


###############################################################################
# Keypoint IDs
# ~~~~~~~~~~~~
# 返回关键点 ID 的数组
# 请注意，这与数组``[k0, k1, k2, k3]``相匹配（由于排序）
knum = mapdl.geometry.knum
knum

###############################################################################
# Keypoints geometry
# ~~~~~~~~~~~~~~~~~~
# 获取包含关键点的 VTK ``MultiBlock`` 。该 VTK 网格可以保存或绘制。更多信息，请访问 `Pyvista 文档 <pyvista_docs_>`_ 。
keypoints = mapdl.geometry.keypoints
keypoints


###############################################################################
# Keypoint Coordinates
# ~~~~~~~~~~~~~~~~~~~~
# 返回关键点位置数组
kloc = mapdl.geometry.get_keypoints()
kloc


###############################################################################
# APDL Command: KDIST
# ~~~~~~~~~~~~~~~~~~~
# 计算两个关键点之间的距离。请注意，您可以根据 ``kloc`` 自行计算。
dist = mapdl.kdist(k0, k1)
dist


###############################################################################
# Keypoint Selection
# ~~~~~~~~~~~~~~~~~~
# 有两种选择关键点的方法，一种是旧的 "传统" 风格，另一种是新的风格。对于那些熟悉现有 MAPDL 命令的人来说，旧式方法很有价值，而新式方法则适用于以 pythonic 方式选择关键点。
#
# 本例生成一系列随机关键点，并选择它们
mapdl.clear()
mapdl.prep7()

# 创建 20 个随机关键点
for _ in range(20):
    mapdl.k("", *np.random.random(3))

# 打印关键点编号
print(mapdl.geometry.knum)


###############################################################################
# 使用“旧方法”命令选择每隔一个关键点。
mapdl.ksel("S", "KP", "", 1, 20, 2)
print(mapdl.geometry.knum)


###############################################################################
# 使用“新样式”命令选择每隔一个关键点。
#
# **Note that the item IDs are 1 based in MAPDL, while Python ranges are 0 based.**
mapdl.geometry.keypoint_select(range(1, 21, 2))
print(mapdl.geometry.knum)


###############################################################################
# 从列表中选择关键点
#
# 请注意，如果您想查看所选内容，可以 ``return_selected`` 。这在从现有区域重新选择时非常有用。
#
# 注意，这里也可以使用 numpy 数组。
items = mapdl.geometry.keypoint_select([1, 5, 10, 20], return_selected=True)
print(items)


###############################################################################
# APDL Command: KPLOT
# ~~~~~~~~~~~~~~~~~~~
# 绘制关键点，同时显示关键点编号
#
# 所有常见的绘图方法都有多种绘图选项。
mapdl.kplot(
    show_keypoint_numbering=True,
    background="white",
    show_bounds=True,
    font_size=26,
)

###############################################################################
# Stop mapdl
# ~~~~~~~~~~
#
mapdl.exit()
