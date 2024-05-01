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
.. _ref_cyclic_static_analysis:

静态循环分析
----------------------

在 1000 RPM 转速下，使用英制单位系统对转子扇形示例进行静态循环分析。


"""
from ansys.mapdl.reader import examples

from ansys.mapdl.core import launch_mapdl

# launch mapdl
mapdl = launch_mapdl()


###############################################################################
# Load in the mesh
# ~~~~~~~~~~~~~~~~
# 加载示例扇形并绘制。
mapdl.cdread("db", examples.sector_archive_file)
mapdl.eplot()


###############################################################################
# Make the rotor cyclic
# ~~~~~~~~~~~~~~~~~~~~~
# 进入前处理程序，使网格循环。
mapdl.prep7()
mapdl.shpp("off")
mapdl.nummrg(label="NODE", toler=1e-3)

mapdl.cyclic()


###############################################################################
# Set material properties
# ~~~~~~~~~~~~~~~~~~~~~~~
# 单位为英制单位，材料为（近似）结构钢。
mapdl.mp("NUXY", 1, 0.31)
mapdl.mp("DENS", 1, 4.1408e-04)
mapdl.mp("EX", 1, 16900000)


###############################################################################
# Apply boundary conditions
# ~~~~~~~~~~~~~~~~~~~~~~~~~
# 以 1000 RPM 的转速循环旋转，并将转子限制在中心位置。
mapdl.omega(0, 0, 1000)  # 1000 RPM

mapdl.csys(1)  # enter the cyclic coordinate system

mapdl.nsel("S", "loc", "x", 0, 0.71)  # radial between 0.69 - 0.71
mapdl.d("ALL", "ALL")  # all DOF for those 8 nodes

mapdl.allsel()
mapdl.csys(0)  # return to cartesian coordinate system

###############################################################################
# Run a static analysis
# ~~~~~~~~~~~~~~~~~~~~~
# 运行 MAPDL 求解器并打印求解结果。
mapdl.run("/SOLU")
mapdl.antype("STATIC")
output = mapdl.solve()
mapdl.finish()
print(output)


###############################################################################
# Plot the cyclic result
# ~~~~~~~~~~~~~~~~~~~~~~
# 使用传统方式（mapdl reader）打印结果
mapdl.result.plot_nodal_displacement(0)


###############################################################################
# Exit MAPDL
# ~~~~~~~~~~
# Finally, exit MAPDL.
mapdl.exit()
