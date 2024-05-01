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
.. _ref_contact_example:

接触单元示例
~~~~~~~~~~~~~~~~~~~~~~~

本例演示如何为一般接触问题创建接触单元。

首先启动 MAPDL。

"""
from ansys.mapdl import core as pymapdl

mapdl = pymapdl.launch_mapdl()

###############################################################################
# 进入前处理器，创建一个程序块，并用四面体单元对其进行网格划分。
#
mapdl.prep7()

vnum0 = mapdl.block(0, 1, 0, 1, 0, 0.5)

mapdl.et(1, 187)
mapdl.esize(0.1)

mapdl.vmesh(vnum0)
mapdl.eplot()

###############################################################################
# 在现有图块上方再添加一个体块，并用二次六面体单元对其进行网格划分。确保这些体块不会相碰，方法是将其起始位置略高于现有体块。
#
# 请注意，这两个图块并不接触，网格也不规则。

mapdl.esize(0.09)
mapdl.et(2, 186)
mapdl.type(2)
vnum1 = mapdl.block(0, 1, 0, 1, 0.50001, 1)
mapdl.vmesh(vnum1)
mapdl.eplot()


###############################################################################
# 选择两个图块交叉处的所有单元并生成接触单元。

mapdl.nsel("s", "loc", "z", 0.5, 0.50001)
mapdl.esln("s")
output = mapdl.gcgen("NEW", splitkey="SPLIT", selopt="SELECT")
print(output)

###############################################################################
# 绘制接触单元对。从上面的命令输出中可以看出，断面 ID 分别为 5 和 6。
#
# 在这里，我们将单元网格绘制成线框，以显示接触对的重叠。

mapdl.esel("S", "SEC", vmin=5, vmax=6)
mapdl.eplot(style="wireframe", line_width=3)

###############################################################################
# Stop mapdl
# ~~~~~~~~~~
#
mapdl.exit()
