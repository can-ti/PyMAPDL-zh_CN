.. _develop_on_codespaces:


Develop on Codespaces
=====================

`Codespaces <codespaces_features_>`_ 是 GitHub 提供的一个虚拟开发环境。您可以启动一个包含所有所需工具的容器，并在几分钟内开始工作。这是开始 PyMAPDL 开发的简便方法，无需经历设置环境的过程。


.. warning::
   `Codespaces <codespaces_features_>`_ 不是免费的，但每月有丰厚的免费额度。之后，您必须按照 `GitHub 定价 <github_pricing_>`_ 支付费用。你可以在 *GitHub 帐户设置* 中的 *计费和计划* 和 *计划和使用量* 下查看计费详情。


How to start
------------

要启动代码空间环境，请访问 `PyMAPDL 代码库 <pymapdl_repo_>`_ ，点击绿色的 **Code** 按钮，并选择 **Codespaces** 选项卡。然后，点击 **+** 按钮，打开默认的代码空间环境。

或者，您也可以点击菜单按钮，然后选择 **New with options** 。

下一个窗口将显示配置表单。您可以设置这些选项： **Branch（分支）** 、 **Dev container configuration（开发容器配置）** 、 **Region** 和 **Machine type** 。

**Branch** 选项设置要从中加载配置的 PyMAPDL GitHub 分支。 **Dev container configuration** 选项设置代码空间配置。


目前，主要有三种配置：

* :ref:`PyMAPDL-Codespaces-Developer <ref_codespaces_dev_welcome>` 。这是默认配置。它包含开发和测试 PyMAPDL 所需的操作系统和 Python 依赖项。例如，它安装了用于测试的 ``xvfb`` 和 ``pytest`` 软件包。

  |Open a GitHub Codespaces for developers-light|
  |Open a GitHub Codespaces for developers-dark|
  

* :ref:`PyMAPDL-Codespaces-Documentation <ref_codespaces_docs_welcome>` 。该配置是专门为处理文档或示例的人员设置的。因此，它包含了适当的操作系统和 Python 依赖项。例如，它包括 `sphinx`` 和 `latex`` 软件包，用于将文档构建为 HTML 和 PDF 输出。

  |Open a GitHub Codespaces for documentation-light|
  |Open a GitHub Codespaces for documentation-dark|

* `PyMAPDL-DevContainer (Local) <pymapdl_codespaces_welcome_local_>`_ **[不推荐]** 。
  这是用于在本地启动开发容器的配置。该容器与前面的配置类似，但它是与 Visual Studio Code 一起在本地使用的。
  因此，在创建 Codespaces 环境时， **一定不要** 选择它。有关如何在本地启动开发容器的详细信息，请参阅 :ref:`develop_on_remote_containers` 。

最后， **Machine type** 选项允许您选择托管代码空间的机器规格。消耗的代码空间限额（免费或付费）与机器的功率成正比。


.. warning::

   如果选择 **New with options** ，则与选择默认配置相比，构建代码空间环境可能需要更长的时间（最多五分钟）。


How to use
==========

如果你熟悉 Visual Studio Code，浏览器内代码空间的使用就非常简单。例如，您可以创建、编辑和删除文件，也可以安装扩展。
您可以做许多在本地安装的 Visual Studio Code 实例中可以做的事情。不过，也有一些限制，详见 :ref:`Limitations <codespaces_limitations>` 。

.. figure:: ../images/codespaces.png
   :width: 300pt

   PyMAPDL GitHub Codespaces environment


如何连接到已存在的实例
==============================================

你可以访问 PyMAPDL 代码库，点击 **Code** 按钮和 **Codespaces** 标签，然后选择要连接的机器。

您可以在您的 `个人代码空间页面 <codespaces_personal_page_>`_ 中访问您的代码空间（无论是否使用 PyMAPDL）的完整列表。在那里，你可以启动、停止、删除或配置每个代码空间，与创建该代码空间的版本库无关。


您也可以通过打开代码空间 **Command palette** (:kbd:`Ctr/⌘` + :kbd:`Shift` + :kbd:`P`) 并选择 *Open in* 打开您的集成开发环境名称，从本地集成开发环境连接到您的代码空间。

如何停止或删除实例
=================================


当您不使用 Codespace 虚拟机时，应停止该虚拟机，这样您就不会被计费。您可以通过 **Command palette** （:kbd:`Ctr/⌘` + :kbd:`Shift`+:kbd:`P`）停止代码空间，然后搜索 ``Stop current Codespace`` 。

.. warning:: 
   如果您关闭了浏览器窗口（无论是否误关）， **您的代码空间仍在运行** 。
   您可以通过点击绿色的 **Code** 按钮，然后点击 **Codespaces** 标签，从 PyMAPDL 代码库中再次访问它。你会看到当前（激活和停止的）PyMAPDL 代码空间机器的列表，你可以选择要连接、停止或删除的机器。

当你完成了代码空间虚拟机的工作并想删除它时，你可以从你的 `个人代码空间页面 <codespaces_personal_page_>`_ ，
击你想处理的虚拟机的更多按钮(**. . .**) ，然后点击 **Delete** 。或者，您也可以从 PyMAPDL 代码库中 **Code** 按钮下的 **Codespace** 选项卡中删除它们。在那里，你可以看到正在运行的虚拟机，并停止或删除你喜欢的虚拟机。


.. _codespaces_limitations:

Limitations
===========

* Codespaces 不允许打开窗口进行绘图。不过，您可以绘制到文件中，然后从 **文件资源管理器** 选项卡打开文件。

* 在 Codespaces 中渲染 HTML 页面可能有点困难。因此，:ref:`PyMAPDL-Codespaces-Documentation <ref_codespaces_docs_welcome>` 包含了一些脚本助手，用于启动和停止 Web 服务器以生成文档。更多信息请访问 :ref:`PyMAPDL-Codespaces-Documentation <ref_codespaces_docs_welcome>`。

* 从本地集成开发环境打开代码空间时，可能会丢失一些配置。例如，你可能会发现自己处于不同的工作目录中，或者你可能会发现 Python 虚拟环境没有被正确激活。



.. Images

.. |Open a GitHub Codespaces for developers-light| image:: https://img.shields.io/badge/-Open%20GitHub%20Codespace-333?style=flat-square&logo=github
   :target: https://codespaces.new/ansys/pymapdl?quickstart=1&devcontainer_path=.devcontainer%2Fdevcontainer.json
   :class: only-light

.. |Open a GitHub Codespaces for developers-dark| image:: https://img.shields.io/badge/-Open%20GitHub%20Codespace-ffffff?style=flat-square&logo=github&logoColor=000000
   :target: https://codespaces.new/ansys/pymapdl?quickstart=1&devcontainer_path=.devcontainer%2Fdevcontainer.json
   :class: only-dark

.. |Open a GitHub Codespaces for documentation-light| image:: https://img.shields.io/badge/-Open%20GitHub%20Codespace-333?style=flat-square&logo=github
   :target: https://codespaces.new/ansys/pymapdl?quickstart=1&devcontainer_path=.devcontainer%2Fcodespaces-docs%2Fdevcontainer.json
   :class: only-light

.. |Open a GitHub Codespaces for documentation-dark| image:: https://img.shields.io/badge/-Open%20GitHub%20Codespace-ffffff?style=flat-square&logo=github&logoColor=000000
   :target: https://codespaces.new/ansys/pymapdl?quickstart=1&devcontainer_path=.devcontainer%2Fcodespaces-docs%2Fdevcontainer.json
   :class: only-dark
