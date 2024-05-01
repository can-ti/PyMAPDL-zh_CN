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
.. _ref_dpf_basic_example:

使用 PyMAPDL 的 DPF-Core 基本用法
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

本例改编自 `DPF-Core 基本用法示例 <https://dpf.docs.pyansys.com/version/stable/examples/00-basic/00-basic_example.html>`_ ，
展示了如何在 `DPF <https://dpf.docs.pyansys.com/>`_ 中打开结果文件，并进行一些基本的后处理。

如果安装了 Ansys 2021 R1，启动 DPF 就非常简单了，因为 DPF-Core 会负责启动后处理 Ansys 文件所需的所有服务。

首先，以 ``dpf_core`` 的形式导入 DPF-Core 模块，并导入随附的示例文件。


"""
import tempfile

from ansys.dpf import core as dpf

from ansys.mapdl.core import launch_mapdl
from ansys.mapdl.core.examples import vmfiles

###############################################################################
# Create model
# ~~~~~~~~~~~~~~
#
# 运行 MAPDL 验证手册中的示例

mapdl = launch_mapdl()

vm5 = vmfiles["vm5"]
output = mapdl.input(vm5)

print(output)

# 如果在本地工作，则无需执行以下步骤
temp_directory = tempfile.gettempdir()
print(f'默认临时文件地址： {temp_directory}')

# 将 RST 文件下载到当前文件夹
rst_path = mapdl.download_result(temp_directory)

###############################################################################
# 接下来，打开生成的 RST 文件并打印出 :class:`Model <ansys.dpf.core.model.Model>` 对象。
# :class:`Model <ansys.dpf.core.model.Model>` 类通过跟踪结果文件使用的运算符和数据源，有助于组织结果的访问方法。
#
# 打印模型显示：
#
# - Analysis type 分析类型
# - Available results 可用结果
# - Size of the mesh 网格尺寸
# - Number of results 结果数量

###############################################################################
# 如果要使用远程服务器，可能需要先上传 ``RST`` 文件，然后再使用它。
# 然后你就可以创建 :class:`DPF Model <ansys.dpf.core.model.Model>` 。

dpf.core.make_tmp_dir_server(dpf.SERVER)

if dpf.SERVER.local_server:
    model = dpf.Model(rst_path)
else:
    server_file_path = dpf.upload_file_in_tmp_folder(rst_path)
    model = dpf.Model(server_file_path)

print(model)

###############################################################################
# Model Metadata
# ~~~~~~~~~~~~~~
# 可以通过引用模型的 :attr:`metadata <ansys.dpf.core.model.Model.metadata>` 属性从模型中提取特定元数据。
# 例如，只打印 :attr:`result_info <ansys.dpf.core.model.Metadata.result_info>` 属性：

metadata = model.metadata
print(metadata.result_info)

###############################################################################
# 打印 :class:`mesh region（网格区域） <ansys.dpf.core.meshed_region.MeshedRegion>` ：

print(metadata.meshed_region)

###############################################################################
# 要打印结果的时间或频率，请使用 :class:`time_freq_support <ansys.dpf.core.time_freq_support.TimeFreqSupport>`：

print(metadata.time_freq_support)

###############################################################################
# Extracting Displacement Results
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 可以通过 :class:`Results <ansys.dpf.core.results.Results>` 属性访问模型的所有结果，
# 该属性返回 :class:`ansys.dpf.core.results.Results` 类。该类包含特定结果文件可用的 DPF 结果运算符，使用 ``print(results)`` 打印对象时会列出这些运算符。
#
# 这里，:class:`displacement <ansys.dpf.core.operators.result.displacement.displacement>` 运算符与 :class:`DataSources（数据源） <ansys.dpf.core.data_sources.DataSources>` 相联，
# 这会在运行 :class:`results.displacement() <ansys.dpf.core.operators.result.displacement.displacement>` 时自动进行。
# 默认情况下，:class:`displacement <ansys.dpf.core.operators.result.displacement.displacement>` 运算符连接到第一个结果集，对于此静态结果而言，它是唯一的结果。

results = model.results
displacements = results.displacement()
fields = displacements.outputs.fields_container()

# 最后，提取位移场数据：
disp = fields[0].data
disp

###############################################################################
# Plot displacements
# ~~~~~~~~~~~~~~~~~~
#
# 您可以使用以下方法打印上面的位移场：

model.metadata.meshed_region.plot(fields, cpos="xy")

###############################################################################
# 或使用
#

fields[0].plot(cpos="xy")

###############################################################################
# 如果您在网格或结果上使用了 :class:`ansys.dpf.core.scoping.Scoping` 方法，这种方法会特别有用。


###############################################################################
# Close session
# ~~~~~~~~~~~~~~
#
# Stop MAPDL session.
#
mapdl.exit()
