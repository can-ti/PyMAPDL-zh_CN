.. _dash_example:

使用 Dash 构建 PyMAPDL web 应用程序
===================================

本例展示了如何使用 Dash 为一个简单的有限元分析问题构建网络 web 应用程序。

Dash 是一个低代码框架，用于构建可在网络浏览器中呈现的数据应用程序。有关 Dash 文档，请参阅： https://dash.plotly.com/ 。


所需模块
----------------

在本例中，根据需要安装模块：

* `dash <dash_>`_
* `dash_bootstrap_components <dash_bootstrap_components_>`_
* `plotly.express <plotly_express_>`_
* `webbrowser <webbrowser_library_>`_
* `pandas <pandas_org_>`_


web 应用结构
-------------

* **说明页** 
  阅读问题陈述
* **模拟页面** 
  允许更改输入值、求解并绘制结果。
* **数据页** 
	允许在表格和图表中绘制数据


使用方法
--------

从下面的链接下载压缩文件并解压到一个文件夹。运行 Python 文件 ``BimetallicStrip.py`` ，在默认浏览器中启动应用程序。

:download:`dash extra files <dash-vm35.zip>`
