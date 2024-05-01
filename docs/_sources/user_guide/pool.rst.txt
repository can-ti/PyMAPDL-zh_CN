.. _ref_pymapdl_pool:

Create a pool of MAPDL instances
================================

PyMAPDL 包含 :class:`LocalMapdlPool <ansys.mapdl.core.pool.LocalMapdlPool>` 类，用于简化为批处理创建 :class:`Mapdl <ansys.mapdl.core.mapdl._MapdlCore>` 类的多个本地实例。
这可用于批量处理一组输入文件、收敛分析或其他与批量处理相关的流程。

这段代码将创建一个池：

.. code:: python

    >>> from ansys.mapdl.core import LocalMapdlPool
    >>> pool = LocalMapdlPool(10)
    'MAPDL Pool with 10 active instances'
    >>> pool.exit(block=True)

创建池时，您可以提供额外的关键字参数。这段代码创建了多个实例，每个实例都有一个 CPU，运行在各自独立的当前目录下：

.. code:: python

    >>> import os
    >>> my_path = os.getcmd()
    >>> pool = LocalMapdlPool(10, nproc=1, run_location=my_path)
    Creating Pool: 100%|########| 10/10 [00:01<00:00,  1.43it/s]

您可以用这段代码访问每个单独的 MAPDL 实例：

.. code:: python

    >>> pool[0]
    <ansys.mapdl.core.mapdl.MapdlGrpc object at 0x7f66270cc8d0>

请注意，这是一个自启动池。如果 MAPDL 的某个实例在批处理过程中终止，该实例会自动重启。您可以在创建池时设置 ``restart_failed=False`` 关闭此行为。

Run a set of input files
------------------------

您可以使用 :func:`run_batch <ansys.mapdl.core.LocalMapdlPool.run_batch>` 方法，使用池运行一组预先生成的输入文件。例如，这段代码将运行第一组 20 个验证文件：

.. code:: python

    >>> from ansys.mapdl.core import examples
    >>> files = [examples.vmfiles["vm%d" % i] for i in range(1, 21)]
    >>> outputs = pool.run_batch(files)
    >>> len(outputs)
    20


Run a user function
-------------------

您可以使用池在每个 MAPDL 实例上通过一组输入运行自定义用户函数。与 :func:`run_batch <ansys.mapdl.core.LocalMapdlPool.run_batch>` 函数的示例一样，以下代码使用了一组验证文件。
不过，它将其作为一个函数来实现，并输出最终例程，而不是 MAPDL 输出的文本。

.. code:: python

    completed_indices = []


    def func(mapdl, input_file, index):
        # input_file, index = args
        mapdl.clear()
        output = mapdl.input(input_file)
        completed_indices.append(index)
        return mapdl.parameters.routine


    inputs = [(examples.vmfiles["vm%d" % i], i) for i in range(1, 10)]
    output = pool.map(func, inputs, progress_bar=True, wait=True)
    [
        "Begin level",
        "Begin level",
        "Begin level",
        "Begin level",
        "Begin level",
        "Begin level",
        "Begin level",
        "Begin level",
        "Begin level",
    ]

    # Close the PyMAPDL pool.
    pool.exit()


Close the PyMAPDL pool
----------------------

可以使用 :meth:`pool.exit() <ansys.mapdl.core.LocalMapdlPool.exit>` 命令关闭 PyMAPDL 池。

.. code:: python
    
    >>> pool.exit()


API description
---------------

有关全面的描述，请参阅 :ref:`ref_pool_api` 。
