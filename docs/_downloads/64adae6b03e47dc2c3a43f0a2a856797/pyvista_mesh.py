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
.. _ref_pyvista_mesh:

PyVista 网格集成
------------------------

在 MAPDL 中对 pyvista 生成的网格进行模态分析。

"""
# sphinx_gallery_thumbnail_number = 2

import os
import tempfile

from ansys.mapdl.reader import save_as_archive
import pyvista as pv

from ansys.mapdl.core import launch_mapdl

# launch MAPDL as a service
mapdl = launch_mapdl(loglevel="ERROR")

# 在 XY 平面上创建一个以 (0, 0, 0) 为中心的简单平面网格
mesh = pv.Plane(i_resolution=100, j_resolution=100)
mesh.plot(color="w", show_edges=True)

###############################################################################
# 将网格写入临时文件
archive_filename = os.path.join(tempfile.gettempdir(), "tmp.cdb")
save_as_archive(archive_filename, mesh)

# 读取存档文件
response = mapdl.cdread("db", archive_filename)
mapdl.prep7()
print(mapdl.shpp("SUMM"))

###############################################################################
#指定壳单元厚度
mapdl.sectype(1, "shell")
mapdl.secdata(0.01)
mapdl.emodif("ALL", "SECNUM", 1)

###############################################################################
# 规定材料属性
# 使用 `AISI 5000 <http://www.matweb.com/search/datasheet.aspx?matguid=89d4b891eece40fbbe6b71f028b64e9e>`_ 系列钢材的近似值
# 
mapdl.units("SI")  # not necessary, but helpful for book keeping
mapdl.mp("EX", 1, 200e9)  # Elastic moduli in Pa (kg/(m*s**2))
mapdl.mp("DENS", 1, 7800)  # Density in kg/m3
mapdl.mp("NUXY", 1, 0.3)  # Poissons Ratio
mapdl.emodif("ALL", "MAT", 1)

###############################################################################
# 运行无约束模态分析
# for the first 20 modes above 1 Hz
mapdl.modal_analysis(nmode=20, freqb=1)

# 您还可以这样运行：
# mapdl.run('/SOLU')
# mapdl.antype('MODAL')  # default NEW
# mapdl.modopt('LANB', 20, 1)
# mapdl.solve()

###############################################################################
# 在 ``pyansys`` 中加载结果文件并绘制第 8 阶模态。
result = mapdl.result
print(result)

result.plot_nodal_displacement(7, show_displacement=True, displacement_factor=0.4)

###############################################################################
# 使用等高线绘制一阶模态
result.plot_nodal_displacement(
    0, show_displacement=True, displacement_factor=0.4, n_colors=10
)

###############################################################################
# 对模态分析结果进行动画处理
#
# 禁用 ``movie_filename`` ，并增加 ``n_frames`` 以获得更平滑的绘图。使用 ``loop=True`` 启用连续循环绘图。

result.animate_nodal_displacement(
    18,
    loop=False,
    add_text=False,
    n_frames=30,
    displacement_factor=0.4,
    show_axes=False,
    background="w",
    movie_filename="plane_vib.gif",
)

###############################################################################
# Stop mapdl
# ~~~~~~~~~~
#
mapdl.exit()
