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
.. _ref_xpl_example:

二进制 MAPDL 文件资源管理器
-------------------------------

本教程将演示如何探索 MAPDL 会话生成的二进制文件内容并提取相关记录。

这些文件包括 APDL 生成的大多数二进制文件（如 ``.RST`` 、``.FULL`` 等）。

"""

from ansys.mapdl.core import launch_mapdl

# 将 MAPDL 作为服务启动，并禁用除错误信息之外的所有功能。
from ansys.mapdl.core.examples import vmfiles

mapdl = launch_mapdl()

# mapdl 类下的一个特定属性专门用于 XPL。它基于 APDLMath `*XPL` 命令。
xpl = mapdl.xpl

# 许多命令可通过 xpl 类直接访问：
help(xpl)


###############################################################################
# Open and explore a file
# ~~~~~~~~~~~~~~~~~~~~~~~
# 首先，您需要打开一个现有文件。我们可以通过运行一个验证手动输入文件来创建一个示例结果文件，然后打开它创建的结果文件。
#
# **NOTE:** 目前一次只能打开一个文件

# 运行 Verification Manual 1 并打开其创建的结果文件
mapdl.input(vmfiles["vm1"])
print(xpl.open("file.rst"))

###############################################################################
# 使用 `list` 函数，可以列出当前层级的可用记录。
#
print(xpl.list())


###############################################################################
# 使用 ``step`` 和 ``up`` 函数，您可以向下进入树的某个分支，或向上进入树的顶层
xpl.step("GEO")
print(xpl.list())


###############################################################################
# 显示您在树或记录中的位置：
#
print(xpl.where())


###############################################################################
# 上一级回到顶部，然后列出当前点的记录。
xpl.up()
print(xpl.list())


###############################################################################
# Read a record into an APDLMath Vector
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ``info`` 方法将提供记录的相关信息（如长度、数据类型等）。
#
# 使用 ``read`` 方法，可以读取特定记录并填充 APDLMath 对象。
#
print(xpl.info("DOF"))
v = xpl.read("DOF")
print(v)


###############################################################################
# 要将该向量转换为 NumPy 数组，需要明确使用 ``asarray``：
#
nod = v.asarray()
print(nod)


###############################################################################
# 读取第一个节点解

# 首先，我们进入第一个 set
#
print(xpl.goto("DSI::SET1"))
print(xpl.list())


###############################################################################
# Then we read the Nodal solution vector `"NSL"` into a numpy array
#
u = xpl.read("NSL")
un = u.asarray()
print(un)


###############################################################################
# 关闭已打开的文件
print(xpl.close())


###############################################################################
# Stop mapdl
# ~~~~~~~~~~
#
mapdl.exit()
