.. _write_documentation:

===================
Write documentation
===================

编写文档是为项目做出贡献的绝佳方式，因为文档在使项目更易于访问和使用方面发挥着关键作用。清晰全面的文档可以帮助用户和开发人员有效地理解、
实施项目并排除故障。它最大限度地减少了准入门槛，使新人更容易参与进来，也使现有的贡献者更有成效。

好的文档还可以减轻维护者的负担，因为它可以解答常见问题并帮助预防问题的发生。通过创建或改进文档，您不仅能提高项目质量，还能促进知识共享和社区发展，从而为项目的长期成功做出宝贵贡献。

Set up your environment
=======================

要编写和构建文档，必须遵循 :ref:`developing_pymapdl` 中所述的相同步骤，但在这种情况下，必须使用此命令安装文档依赖项：

.. code:: console

    pip install -e '.[doc]'


Build the documentation
=======================

PyMAPDL 文档主要以 reStructuredText 格式编写，以 ``.rst`` 文件格式保存在 ``doc/source`` 目录中。用于从这些 reStructuredText 文件构建文档的工具是 `Sphinx <sphinx_>`_。

Sphinx 还能从源代码中构建 API 文档，并管理不同文件、类、方法等之间的交叉引用。此外，它还构建了一个 `示例库 <pymapdl_examples_gallery_>` ，在这里可以展示 PyMAPDL 的功能。

文档可制作成 HTML 文件或单一 PDF 文件。

要将文档制作成 HTML 文件，只需运行一条命令即可。

On Linux:

.. code:: console

   make -C doc html

On Windows: 

.. code:: pwsh-session

    doc\make.bat html

文档的 HTML 文件会写入 ``doc/_build/html`` 目录。

如果要制作 PDF 文档，必须先安装 LaTeX 发行版，如 `MikTeX <miktex_>`_ 。然后运行此命令：

.. code:: console

   make -C doc pdf

运行创建 HTML 文件或 PDF 文件的命令，会运行版本库根目录下 ``./examples`` 中的 Python 文件，以生成 `examples gallery <pymapdl_examples_gallery_>`_ 。运行这些示例的结果会被缓存，以便下次只重新运行已更改的文件。

Sphinx 配置位于 :file:`doc/source` 中的文件 `conf.py <https://github.com/ansys/pymapdl/blob/main/doc/source/conf.py>`_。


Write documentation
===================

为 GitHub 仓库编写良好的文档对于确保用户和贡献者能够理解、使用 PyMAPDL 并为其做出有效贡献至关重要。

以下是如何编写优秀文档的简短总结：

#. **使用一致的结构**：以清晰一致的结构组织文档。必要时使用标题、副标题和目录，帮助用户轻松浏览文档。

#. **解释配置更改**：如果需要更改配置，请提供清晰的说明，介绍如何使用新配置，并举例说明需要更改的原因。

#. **使用示例**：包括实际使用示例、代码片段和解释，以演示用户如何充分利用 PyMAPDL。

#. **记录 API 和代码**：彻底记录每个函数、类和方法。包括参数说明、返回值和使用示例。按照 `numpydoc <numpydoc_>`_ 惯例记录代码。

#. **教程和指南**：创建教程或指南，帮助用户使用 PyMAPDL 完成特定任务或工作流程。这些对于复杂的项目尤其有帮助。

#. **故障排除和常见问题**：在故障排除部分预测常见问题并提供解决方案。常见问题（FAQ）也有助于解决常见问题。

#. **维护和更新**：随着项目的发展，不断更新您的文档。新功能、变更和错误修复都应反映在文档中。

#. **征求反馈**：邀请用户和贡献者对文档提出反馈意见，并对他们的建议和问题做出回应。


Vale linting tool
=================

在 GitHub 代码库中，CI/CD 会运行 `Vale <vale_>`_ ，这是一个功能强大且可扩展的校验工具，用于检查每个拉取请求的编写情况。如果您也想在本地进行验证，则必须在本地安装 Vale：


Installation
------------

#. **Install Vale**: Follow the instructions in `Installation <vale_installation_>`_
#. **Verify installation**: To confirm that Vale is installed correctly, run this command:

   .. code:: console
    
      vale --version

   You should see the installed Vale version displayed in the terminal.

Usage
-----

Vale 是一款用于对文档进行着色和样式检查的多功能工具，支持各种文件格式并提供多种样式指南。下面是如何在 PyMAPDL 中使用 Vale 的基本示例：

#. **同步样式**：首次在版本库中运行 Vale 时，必须通过运行此命令同步在 :file:`.vale.ini` 文件中指定的样式：

   .. code:: console

      vale sync


#. **检查文件**：要验证文件，请在命令行中运行 Vale ，指定要检查的文件或目录。例如

   .. code:: console

       vale --config="./doc/.vale.ini" path/to/your_document.rst

   Vale 会分析你的文档，如果有任何违反样式指南的情况或 linting 问题，它会在终端提供反馈。

在打开您的拉取请求之前，请确保没有错误或警告。


.. _ref_building_example:

Create an example
=================
有三种类型的示例：动态、静态和半静态。

* `Dynamic examples`_
* `Static examples`_
* `Semi-dynamic examples`_


Dynamic examples
----------------

动态示例基于 Python 文件，必须能在三分钟内运行。

在 PyMAPDL 代码库中，它们位于 `examples <pymapdl_examples_>`_ 目录中。

.. vale off

Example: `2d_plate_with_a_hole.py <pymapdl_2d_plate_with_a_hole_>`_
.. vale on

下面是该动态示例的链接： `MAPDL 2D 平面应力集中分析 <pymapdl_doc_2d_plate_with_a_hole_>`_ 。

执行示例时， **脚本总运行时间** 会出现在文件末尾。

由于动态示例必须在每次构建文档时运行，因此要确保它们非常简短。要解决执行时间的问题，可以使用静态或半静态示例。

Static examples
---------------

静态示例基于 RST 文件，不会被执行。

在 PyMAPDL 代码库中，它们位于 `doc\source <pymapdl_doc_source_>`_ 目录中。
.. vale off

Example: `krylov_example.rst <pymapdl_doc_krylov_example_rst_>`_
.. vale on

下面是这个静态示例的链接： `使用频率扫描克雷洛夫方法进行谐波分析 <pymapdl_doc_krylov_example_>`_ 。

Semi-dynamic examples
---------------------

半动态示例是使用该 RST 指令执行 Python 代码的 RST 文件：

.. code:: rst

    .. jupyter-execute::
       :hide-code:


.. vale off

Example: `tecfricstir.rst <pymapdl_techdemo_28_rst_>`_
.. vale on

下面是这个半动态示例的链接： `搅拌摩擦焊接 (FSW) 仿真 <pymapdl_techdemo_28_>`_ 。


