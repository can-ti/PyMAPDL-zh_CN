
创建自己的 MAPDL docker 容器
======================================

.. warning:: 您需要有效的 Ansys 许可证和 Ansys 帐户才能执行本节中的详细步骤。

你可以按照本页提供的步骤创建自己的 MAPDL docker 容器。
本指南将使用本地 Ubuntu 机器为 MAPDL 容器生成所需的文件，首先安装 Ansys 产品，然后将生成的文件复制到容器中。


Requirements
============

* A linux machine, preferable with Ubuntu 18.04 or later.
  CentOS Linux distribution is not supported anymore.
  This machine needs to have `Docker <https://www.docker.com>`_ installed.

* A valid Ansys account. Your Ansys reseller should have
  provide you with one.

* The following provided files:
  
  * `Dockerfile <https://github.com/ansys/pymapdl/tree/main/docker/Dockerfile>`_
  * `.dockerignore <https://github.com/ansys/pymapdl/tree/main/docker/.dockerignore>`_


Procedure
=========

Download Ansys MAPDL installation files
---------------------------------------

Download latest Ansys MAPDL version from the customer portal 
(`Current Release <ansys_current_release_>`_).
You need to have a valid Ansys account with access to
products downloads.

If you lack of an Ansys account, please contact your
IT manager.


Install Ansys MAPDL product
---------------------------

To install Ansys MAPDL product on an Ubuntu machine you can follow 
:ref:`install_mapdl` if you are using the graphical user interface
or :ref:`installing_ansys_in_wsl` for the command line interface.
The later approach can be reused with small changes in a
continuous integration workflow.

To reduce the size of the final image, you might want to
install the minimal files by using:

.. code:: console

    sh /path-to-mapdl-installer \
        -install_dir /path-to-install-mapdl/ \
        -nochecks -mechapdl -ansyscust -silent

This command install Mechanical MAPDL (``-mechapdl``) and the
custom routines (``-ansyscust``) such as UPF.

Please take note of where you are installing ANSYS because the
directory path is need in the following section.

Build Docker image
------------------

To build the Docker image, you need to create a directory and copy
all the files you need in the image.

The steps to copy those files and build the image are detailed in the following script,
which you should modify to adapt it to your needs.

.. code:: dockerfile

    # Creating working directory
    mkdir docker_image
    cd docker_image

    # Copying the docker files
    cp ./path-to-pymapdl/pymapdl/docker/Dockerfile
    cp ./path-to-pymapdl/pymapdl/docker/.dockerignore

    # Creating env vars for the Dockerfile
    export VERSION=222
    export TAG="V222"
    export MAPDL_PATH=/path_to_mapdl_installation/ansys_inc

    # Build Docker image
    sudo docker build  -t $TAG --build-arg VERSION=$VERSION --build-arg MAPDL_PATH=$MAPDL_PATH

Please notice that:

* ``path-to-pymapdl`` is the path where PyMAPDL repository is located.
* ``path_to_mapdl_installation`` is the path to where you have locally installed ANSYS MAPDL.

Not all the installation files are copied, in fact, the files ignored during the copying
are detailed in the file `.dockerignore <https://github.com/ansys/pymapdl/tree/main/docker/.dockerignore>`_.

The Docker container configuration needed to build the container is detailed in the
`Dockerfile <https://github.com/ansys/pymapdl/tree/main/docker/Dockerfile>`_.


Summary
=======


* **Step 1:** Download latest Ansys MAPDL version from the customer portal 
  (`Current Release <ansys_current_release_>`_).

* **Step 2:** Install Ansys MAPDL in a known folder. You can reuse your local
  installation if it is updated and the machine is running the same Ubuntu
  version as the targe Ubuntu docker version.

* **Step 3:** Build the docker image with the provided Docker configuration files
  and script.
