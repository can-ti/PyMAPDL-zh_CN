<p align="center">
   <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://github.com/ansys/pymapdl/blob/main/doc/source/_static/logo_dark.png">
      <source media="(prefers-color-scheme: light)" srcset="https://github.com/ansys/pymapdl/blob/main/doc/source/_static/logo_light.png">
      <img alt="PyMAPDL Logo" src="https://github.com/ansys/pymapdl/blob/main/doc/source/_static/logo_light.png" width="70%">
   </picture>
</p>

[![pyansys](https://img.shields.io/badge/Py-Ansys-ffc107.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5mD8vE7q/3bpVyskbW0sMRUwofHD7Dh5OBkZGBgW7/3W2tZpa2tLQEOyOzeEsfumlK2tbVpaGj4N6jIs1lpsDAwMJ278sveMY2BgCA0NFRISwqkhyQ1q/Nyd3zg4OBgYGNjZ2ePi4rB5loGBhZnhxTLJ/9ulv26Q4uVk1NXV/f///////69du4Zdg78lx//t0v+3S88rFISInD59GqIH2esIJ8G9O2/XVwhjzpw5EAam1xkkBJn/bJX+v1365hxxuCAfH9+3b9/+////48cPuNehNsS7cDEzMTAwMMzb+Q2u4dOnT2vWrMHu9ZtzxP9vl/69RVpCkBlZ3N7enoDXBwEAAA+YYitOilMVAAAAAElFTkSuQmCC)](https://docs.pyansys.com/)
[![pypi](https://img.shields.io/pypi/v/ansys-mapdl-core.svg?logo=python&logoColor=white)](https://pypi.org/project/ansys-mapdl-core/)
[![PyPIact](https://img.shields.io/pypi/dm/ansys-mapdl-core.svg?label=PyPI%20downloads)](https://pypi.org/project/ansys-mapdl-core/)
[![codecov](https://codecov.io/gh/ansys/pymapdl/branch/main/graph/badge.svg)](https://codecov.io/gh/ansys/pymapdl)
[![GH-CI](https://github.com/ansys/pymapdl/actions/workflows/ci.yml/badge.svg)](https://github.com/ansys/pymapdl/actions/workflows/ci.yml)
[![zenodo](https://zenodo.org/badge/70696039.svg)](https://zenodo.org/badge/latestdoi/70696039)
[![MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat)](https://github.com/psf/black)
[![pre-commit](https://results.pre-commit.ci/badge/github/ansys/pymapdl/main.svg)](https://results.pre-commit.ci/latest/github/ansys/pymapdl/main)

## Overview

PyMAPDL 项目支持以 Pythonic 的方式访问 MAPDL，以便能够直接从 Python 与 MAPDL 进程通信。
最新的[ansys-mapdl-core](https://pypi.org/project/ansys-mapdl-core/)软件包提供了更全面的 MAPDL 接口并支持以下功能：

-  原始模块的所有功能（例如 Pythonic 命令和交互会话）。

-  通过 gRPC 从任何地方远程连接到 MAPDL。

-  以 Python 对象的形式直接访问 MAPDL 数组、网格和几何体。

-  在类似 SciPy 的界面中，通过 APDL Math 对 MAPDL 求解器进行底层访问。

下面是 PyMAPDL 在 Visual Studio Code 中的快速演示：

![landing_demo](https://github.com/ansys/pymapdl/raw/main/doc/source/_static/landing_page_demo.gif)

PyMAPDL 可在 Jupyter lab、标准 Python 控制台中运行，也可在 Windows、Linux 甚至 Mac OS 上以批处理模式运行。

## Try it!

您可以通过启动 PyMAPDL GitHub 代码空间来试用 PyMAPDL 库！
该环境已经为您提供了开始使用 PyMAPDL 的一切条件 :smile:

<p align="center">
   <a href="https://codespaces.new/ansys/pymapdl?quickstart=1&devcontainer_path=.devcontainer%2Fdevcontainer.json">
   <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/-Open%20GitHub%20Codespace-ffffff?style=flat-square&logo=github&logoColor=000000">
      <source media="(prefers-color-scheme: light)" srcset="https://img.shields.io/badge/-Open%20GitHub%20Codespace-333?style=flat-square&logo=github">
      <img alt="PyMAPDL Logo" src="https://github.com/ansys/pymapdl/blob/main/doc/source/_static/logo_light.png" tar>
   </picture>
   </a>
</p>

More information can be found in [develop on codespaces](https://mapdl.docs.pyansys.com/version/dev/getting_started/codespaces.html).

## Documentation and issues

PyMAPDL 最新稳定版的文档托管在 [PyMAPDL Documentation](https://mapdl.docs.pyansys.com) 上。

在文档标题栏的右上角有一个选项，可以从查看最新稳定版本的文档切换到查看开发版本或以前发布版本的文档。

您还可以 [查看](https://cheatsheets.docs.pyansys.com/pymapdl_cheat_sheet.png) 或 [下载](https://cheatsheets.docs.pyansys.com/pymapdl_cheat_sheet.pdf) PyMAPDL cheat sheet。这一页参考资料提供了使用 PyMAPDL 的语法规则和命令。


有关故障排除，请访问 [Troubleshooting PyMAPDL](https://mapdl.docs.pyansys.com/version/stable/user_guide/troubleshoot.html#troubleshooting-pymapdl)


在 [PyMAPDL Issues](https://github.com/ansys/pymapdl/issues) 页面，您可以创建问题来报告错误和请求新功能。在 [PyMAPDL Discussions](https://github.com/ansys/pymapdl/discussions) 页面或 [Ansys Developer portal](https://developer.ansys.com) 上的 [Discussions](https://discuss.ansys.com/) 页面，您可以发布问题、分享想法并获得社区反馈。

要联系项目支持团队，请发送电子邮件至 [PyAnsys 核心团队](pyansys.core@ansys.com)。遗憾的是，该团队无法回答具体的库问题。您必须使用 [PyMAPDL Issues](https://github.com/ansys/pymapdl/issues) 和 [PyMAPDL Discussions](https://github.com/ansys/pymapdl/discussions) 页面来提出问题、申请新功能和提问。

## Project transition -  legacy support

这个项目的前身是 ``pyansys`` ，我们要感谢所有早期采用者、贡献者和用户，感谢他们多年来提交问题、提供反馈和贡献代码。 ``pyansys `` 项目已由 Ansys 接管，并被用于为 Ansys 产品创建新的 Pythonic、跨平台和基于服务的多语言界面。您对 ``pyansys`` 的贡献使其成为更好的解决方案。


``pyansys`` 项目正在不断扩展，不仅仅局限于 MAPDL，在对原始 Python 模块进行了许多新功能和更改的同时，还采取了许多措施来确保与旧代码的兼容性，同时支持新功能。原始 Python 模块已被拆分为以下项目和模块：

-  [ansys.mapdl.core](https://github.com/ansys/pymapdl)
-  [ansys.mapdl.reader](https://github.com/ansys/pymapdl-reader)
-  [ansys.mapdl.corba](https://github.com/ansys/pymapdl-corba)

有关每个项目的更多信息，请访问它们的 GitHub 页面。

## Citing this module

如果您在研究中使用 [PyMAPDL](https://mapdl.docs.pyansys.com/version/stable/)，并希望引用模块和源代码，可以访问 [pyansys Zenodo](https://zenodo.org/badge/latestdoi/70696039) 并生成正确的引用。例如，BibTex 引用如下：

```bibtex
@software{alexander_kaszynski_2020_4009467,
  author       = {Alexander Kaszynski},
  title        = {{pyansys: Python Interface to MAPDL and Associated 
                    Binary and ASCII Files}},
  month        = aug,
  year         = 2020,
  publisher    = {Zenodo},
  version      = {0.43.2},
  doi          = {10.5281/zenodo.4009467},
  url          = {https://doi.org/10.5281/zenodo.4009467}
}
```

由于此处的引文可能不是最新的，请访问上面的链接获取最新的引文。

## License and acknowledgments

[PyMAPDL](https://mapdl.docs.pyansys.com/version/stable/) 采用 [MIT license](https://github.com/ansys/pymapdl/blob/main/LICENSE) 许可。

[ansys-mapdl-core](https://pypi.org/project/ansys-mapdl-core/)软件包对 Ansys 没有任何商业要求。该工具通过向 MAPDL 服务添加 Python 接口扩展了 ``MAPDL`` 的功能，但不改变原始软件的核心行为或许可证。使用 [PyMAPDL](https://mapdl.docs.pyansys.com/version/stable/) 的交互式 APDL 控件需要有合法授权的本地 Ansys 副本。

要获取 Ansys 的副本，请访问 [Ansys](https://www.ansys.com/)。
