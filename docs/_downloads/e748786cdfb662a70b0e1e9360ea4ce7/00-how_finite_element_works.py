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
.. _build_element_example:

建立有限元模型
----------------------------

使用等参数公式为四边形单元建立了有限元模型，并用 PyMAPDL 进行了验证。

为了用一个具体的例子来说明，我们以一个二维单元为例，该单元由以下 (x, y) 节点位置、各向同性材料（杨氏模量为 30e6 psi，波依斯特比为 0.25）和单位厚度描述，
提供了 Daryl Logan 的《有限元法第一课》（第 2 版，PWS 出版社，1993 年）中讨论内容的实际应用。
"""
# sphinx_gallery_thumbnail_number = 2
import itertools

import matplotlib.pyplot as plt
import numpy as np

np.set_printoptions(linewidth=120) # 这些选项决定了浮点数、数组和其他 NumPy 对象的显示方式。


###############################################################################
# 二维线性矩形单元刚度矩阵的推导
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 用以下坐标建立一个基本的二维单元
#
# .. math::
#
#    \begin{matrix}
#    (1, 2) \\ (8, 0) \\ (9, 4) \\ (4, 5)
#    \end{matrix}
#

node_xy = [(1, 2), (8, 0), (9, 4), (4, 5)]
node_ids = list(range(1, 1 + 4))
nodes = np.array(node_xy, dtype=float)


def plot_my_mesh(nodes, points=None):
    fig = plt.figure(figsize=(6, 6))
    ax = plt.gca()
    plt.scatter(nodes[:, 0], nodes[:, 1])
    if points is not None:
        plot_pts = points if points.ndim > 1 else points[None, :]
        plt.scatter(plot_pts[:, 0], plot_pts[:, 1])
    nodes_around = np.reshape(np.take(nodes, range(10), mode="wrap"), (-1, 2))
    plt.plot(nodes_around[:, 0], nodes_around[:, 1])
    for i, n in enumerate(nodes):
        ax.annotate(i + 1, n + np.array([0.1, 0.1]))
    plt.xlim(0, 10)
    plt.ylim(0, 6)
    plt.box(False)
    ax.set_aspect(1)
    plt.show()


plot_my_mesh(nodes)

###############################################################################
# 我们将创建一个单元类 ``MyElementDemo`` 来承载本演示所需的所有数据和方法。
# 虽然我们可以一次性对整个类进行编程（如本练习底部所做的），但我们将逐个添加数据和方法，以便对其含义进行注释。
# 我们将创建该类的一个实例，并将其称为 ``my_elem`` 以表示我们的特定单元示例


class MyElementDemo:
    def __init__(self, nodes):
        self.nodes = nodes


my_elem = MyElementDemo(nodes)

###############################################################################
# 形函数
# ~~~~~~~~~~~~~~~
# 通过单元形状函数，我们可以将某些量（例如位移分量）从角节点插值到整个单元的任意点。
# 这样，当结构发生变形时，我们不仅可以知道节点处的位移，还可以知道内部任意点的位移。
#
# 等参公式的特别之处在于为我们的二维单元选择一个典型形状。我们假设任何二维四边形都可以映射为正方形，例如 :math:`{\rm I\!R}^2` 中的一个域，如 :math:`s\in [-1,1]` 和 :math:`t\in [-1,1]`。
# 我们在该正方形上推导出所有物理量，并利用映射将它们的值转换为单元的实际形状。
# 这种变换将有助于简化计算所需的积分，以测量离散节点移动和形状变形时，应变能是如何在整个单元的连续体中累积的。
#
# 对于等参二维单元，我们定义了以下 4 个形状函数：
#
# .. math::
#
#    \begin{matrix}
#    N_1 = \frac{(1-s)\cdot(1-t)}{4} \\
#    N_2 = \frac{(1+s)\cdot(1-t)}{4} \\
#    N_3 = \frac{(1+s)\cdot(1+t)}{4} \\
#    N_4 = \frac{(1-s)\cdot(1+t)}{4}
#    \end{matrix}
#
# 这些函数的构建方式是，节点 :math:`i` 上的函数在所有其他节点上消失，并且它们的和在域中的所有点上都为 1。
#
# 为了好玩，让我们绘制一下它们，看看它们各自对单元的插值有什么贡献

###############################################################################


s = np.linspace(-1, 1, 11)
t = np.linspace(-1, 1, 11)
S, T = np.meshgrid(s, t)

fig = plt.figure(figsize=(10, 10))

ax1 = fig.add_subplot(2, 2, 1, projection="3d")
ax1.plot_surface(S, T, 0.25 * (1 - S) * (1 - T))
ax1.title.set_text(r"N1")

ax2 = fig.add_subplot(2, 2, 2, projection="3d")
ax2.plot_surface(S, T, 0.25 * (1 + S) * (1 - T))
ax2.title.set_text(r"N2")

ax3 = fig.add_subplot(2, 2, 3, projection="3d")
ax3.plot_surface(S, T, 0.25 * (1 + S) * (1 + T))
ax3.title.set_text(r"N3")

ax4 = fig.add_subplot(2, 2, 4, projection="3d")
ax4.plot_surface(S, T, 0.25 * (1 - S) * (1 + T))
ax4.title.set_text(r"N4")

fig.tight_layout()
plt.show()


###############################################################################
# 让我们将形状函数方法添加到我们的类中


def shape_functions(self, s, t):
    return 0.25 * np.array(
        [
            (1 - s) * (1 - t),
            (1 + s) * (1 - t),
            (1 + s) * (1 + t),
            (1 - s) * (1 + t),
        ],
        dtype=float,
    )


MyElementDemo.shape_functions = shape_functions

###############################################################################
# 要将一个量（如位置）从节点插值到整个单元中的任意点，我们可以使用以下操作。
#
# .. math::
#
#    \begin{bmatrix}
#    x \\ y \end{bmatrix} =
#    \begin{bmatrix}
#    N_{1}(s, t) & 0 & N_{2}(s, t) & 0 & N_{3}(s, t) & 0 & N_{4}(s, t) & 0 \\
#    0 & N_{1}(s, t) & 0 & N_{2}(s, t) & 0 & N_{3}(s, t) & 0 & N_{4}(s, t)
#    \end{bmatrix} \cdot
#    \begin{bmatrix}
#    {}^1x \\ {}^1y \\ {}^2x \\ {}^2y \\ {}^3x \\ {}^3y \\ {}^4x \\ {}^4y
#    \end{bmatrix}
#
# .. math::
#
#    \mathbf{X}_{\text{throughout}} = \mathbf{N} \cdot \mathbf{X}_{\text{nodal}}


def N(self, s, t):
    n_vec = self.shape_functions(s, t)
    return np.array(
        [
            [n_vec[0], 0, n_vec[1], 0, n_vec[2], 0, n_vec[3], 0],
            [0, n_vec[0], 0, n_vec[1], 0, n_vec[2], 0, n_vec[3]],
        ]
    )


MyElementDemo.N = N


###############################################################################
# 为了了解这一点的用处，让我们来插值一些常见的点。
# 我们的等参单元的中心点为 :math:`(s,t) = (0, 0)` 。让我们看看插值是如何得到实单元中的等价点的：


def interpolate_nodal_values(self, s, t, nodal_values):
    return self.N(s, t).dot(nodal_values.flatten())


MyElementDemo.interpolate_nodal_values = interpolate_nodal_values

my_points = my_elem.interpolate_nodal_values(0, 0, nodes)
my_points

###############################################################################
# 绘制网格

plot_my_mesh(nodes, my_elem.interpolate_nodal_values(0, 0, nodes))

###############################################################################
# 高斯积分
# ~~~~~~~~~~~~~~~~
#
# 高斯积分是一种用有限和 :math:`\sum w_i f(x_i)` 近似函数 :math:`\int f(x) dx` 的积分的方法。
# 通过在域中的有限位置对函数 :math:`f(x)` 进行采样，并适当缩放其值，就可以得到积分的估计值。
# 事实证明，取样点 :math:`x_i` 及其权重值 :math:`w_i` 存在最佳位置。
# 对于我们的等参数单元域中的二维函数，即 :math:`(s,t) \in {\rm I\!R}^2` 且 :math:`s \in [-1,1]` 和 :math:`t\in [-1,1]`, 4 个点积分的最佳位置是：

gauss_pts = (
    np.array([[-1, -1], [1, -1], [1, 1], [-1, 1]], dtype=float) * 0.57735026918962
)

MyElementDemo.gauss_pts = gauss_pts
MyElementDemo.gauss_pts

###############################################################################
# Their locations in the element of interest

gauss_pt_locs = np.stack(
    [
        my_elem.interpolate_nodal_values(*gauss_pt, nodes)
        for gauss_pt in MyElementDemo.gauss_pts
    ]
)

plot_my_mesh(nodes, gauss_pt_locs)

###############################################################################
# Strain calculation
# ~~~~~~~~~~~~~~~~~~
# 应变通过线性微分算子与位移相关。对于二维结构，我们只考虑其平面内分量：
#
# .. math::
#
#    \mathbf{\varepsilon} =
#    \begin{bmatrix}
#    \varepsilon_x \\ \varepsilon_y \\ \gamma_{xy}
#    \end{bmatrix}
#    =
#    \begin{bmatrix}
#    \frac{\partial u_x}{\partial x} \\ \frac{\partial u_y}{\partial y} \\
#    \frac{\partial u_x}{\partial y} + \frac{\partial u_y}{\partial x}
#    \end{bmatrix}
#
# 并推断出微分算子如下
#
# .. math::
#
#    \begin{bmatrix}
#    \varepsilon_x \\ \varepsilon_y \\ \gamma_{xy}
#    \end{bmatrix}
#    =
#    \begin{bmatrix}
#    \frac{\partial \left( ... \right)}{\partial x} & 0 \\
#    0 & \frac{\partial \left( ... \right)}{\partial y} \\
#    \frac{\partial \left( ... \right)}{\partial y} & \frac{\partial \left( ... \right)}{\partial x}
#    \end{bmatrix} \cdot
#    \begin{bmatrix}
#    u_x \\ u_y
#    \end{bmatrix}
#

###############################################################################
# 我们回顾一下，由于形函数，整个单元的位移 :math:`begin{bmatrix}u_x & u_y\end{bmatrix}^T` 是已知的。 因此
#
# .. math::
#
#    \begin{bmatrix}
#    u_x \\ u_y \end{bmatrix} =
#    \begin{bmatrix}
#    N_{1}(s, t) & 0 & N_{2}(s, t) & 0 & N_{3}(s, t) & 0 & N_{4}(s, t) & 0 \\
#    0 & N_{1}(s, t) & 0 & N_{2}(s, t) & 0 & N_{3}(s, t) & 0 & N_{4}(s, t)
#    \end{bmatrix} \cdot
#    \begin{bmatrix}
#    {}^1u_x \\ {}^1u_y \\ {}^2u_x \\ {}^2u_y \\ {}^3u_x \\ {}^3u_y \\ {}^4u_x \\ {}^4u_y
#    \end{bmatrix}
#
# .. math::
#
#    \mathbf{u}_{\text{throughout}} = \mathbf{N} \cdot \mathbf{u}_{\text{nodal}}

###############################################################################
# 为了将形函数纳入上述应变表达式，我们需要将相对于 :math:`x` 和 :math:`y` 的微分算子替换为以 :math:`s` 和 :math:`t` 表示的等价算子。
# 这就需要使用链式法则，而在多元微积分中，Jacobian 矩阵（及其行列式）为链式法则提供了便利：
#
# .. math::
#
#    \begin{bmatrix}
#    \varepsilon_x \\ \varepsilon_y \\ \gamma_{xy}
#    \end{bmatrix}
#    =
#    \frac{1}{\det{\mathbf{J}}} \begin{bmatrix}
#    \frac{\partial y}{\partial t} \frac{\partial \left( ... \right)}{\partial s} - \frac{\partial y}{\partial s} \frac{\partial \left( ... \right)}{\partial t} & 0 \\
#    0 & \frac{\partial x}{\partial s} \frac{\partial \left( ... \right)}{\partial t} - \frac{\partial x}{\partial t} \frac{\partial \left( ... \right)}{\partial s} \\
#    \frac{\partial x}{\partial s} \frac{\partial \left( ... \right)}{\partial t} - \frac{\partial x}{\partial t} \frac{\partial \left( ... \right)}{\partial s} & \frac{\partial y}{\partial t} \frac{\partial \left( ... \right)}{\partial s} - \frac{\partial y}{\partial s} \frac{\partial \left( ... \right)}{\partial t}
#    \end{bmatrix} \cdot
#    \begin{bmatrix}
#    u_x \\ u_y
#    \end{bmatrix}
#
#
# .. math::
#
#    \mathbf{\varepsilon} =
#    \mathbf{D} \cdot \mathbf{u_{\text{throughout}}}
#
# 因此：
#
# .. math::
#
#    \begin{bmatrix}
#    \varepsilon_x \\ \varepsilon_y \\ \gamma_{xy}
#    \end{bmatrix}
#    =
#    \mathbf{D} \cdot \mathbf{N} \cdot \mathbf{u_{\text{nodal}}}
#    =
#    \mathbf{B} \cdot  \mathbf{u_{\text{nodal}}}
#
# 其中
#
# .. math::
#
#    \mathbf{D}=
#    \frac{1}{\det{\mathbf{J}}} \begin{bmatrix}
#    \frac{\partial y}{\partial t} \frac{\partial \left( ... \right)}{\partial s} - \frac{\partial y}{\partial s} \frac{\partial \left( ... \right)}{\partial t} & 0 \\
#    0 & \frac{\partial x}{\partial s} \frac{\partial \left( ... \right)}{\partial t} - \frac{\partial x}{\partial t} \frac{\partial \left( ... \right)}{\partial s} \\
#    \frac{\partial x}{\partial s} \frac{\partial \left( ... \right)}{\partial t} - \frac{\partial x}{\partial t} \frac{\partial \left( ... \right)}{\partial s} & \frac{\partial y}{\partial t} \frac{\partial \left( ... \right)}{\partial s} - \frac{\partial y}{\partial s} \frac{\partial \left( ... \right)}{\partial t}
#    \end{bmatrix}
#
# and
#
# .. math::
#
#    \mathbf{J}=
#    \begin{bmatrix}
#    \frac{\partial x}{\partial s} & \frac{\partial y}{\partial s} \\
#    \frac{\partial x}{\partial t} & \frac{\partial y}{\partial t}
#    \end{bmatrix}

###############################################################################
# Implementation: Jacobians
# ~~~~~~~~~~~~~~~~~~~~~~~~~
#
# 在形函数的帮助下，将位置 :math:`x` 和 :math:`y` 的表达式替换为节点位置的函数，就可以得到雅各比。结果相当于下面的双线性形式：
#
# .. math::
#
#    \begin{aligned}
#    \det{\mathbf{J}} &=
#    \frac{1}{8}
#    \begin{bmatrix}{}^1x & {}^2x & {}^3x & {}^4x \end{bmatrix} \cdot
#    \begin{bmatrix}
#    0 & 1 - t & t-s & s-1 \\
#    t-1 & 0 & s+1 & -s-t \\
#    s-t & -s-1 & 0 & t+1 \\
#    1-s & s+t & -t-1 & 0 \\
#    \end{bmatrix} \cdot
#    \begin{bmatrix}{}^1y \\ {}^2y \\ {}^3y \\ {}^4y \end{bmatrix}
#    \\&=
#    \mathbf{X_{\text{locs}}}^T \cdot
#    \begin{bmatrix}
#    0 & 1 - t & t-s & s-1 \\
#    t-1 & 0 & s+1 & -s-t \\
#    s-t & -s-1 & 0 & t+1 \\
#    1-s & s+t & -t-1 & 0 \\
#    \end{bmatrix} \cdot
#    \mathbf{Y_{\text{locs}}}
#    \end{aligned}

###############################################################################
# 我们现在已经准备好在我们的单元中实施它了


def J(self, s, t):
    upper = np.array(
        [
            [0, -t + 1, +t - s, +s - 1],
            [0, 0, +s + 1, -s - t],
            [0, 0, 0, +t + 1],
            [0, 0, 0, 0],
        ],
        dtype=float,
    )
    temp = upper - upper.T
    return 1.0 / 8 * self.nodes[:, 0].dot(temp).dot(self.nodes[:, 1])


MyElementDemo.J = J


###############################################################################
# 接下来，我们将研究雅各布因子在单元内部是如何变化的。
# First for our subject element:

my_elem.J(-1, -1), my_elem.J(0, 0), my_elem.J(1, 1)


###############################################################################
# Implementation: B Matrix
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Similarly, we can implement our expression for the B matrix, which converts
# nodal displacements :math:`\mathbf{u_{\text{nodal}}}` to strains
# :math:`\mathbf{\varepsilon}`, by substituting the D operator, the shape
# functions and nodal locations:
#
# .. math::
#
#    \begin{bmatrix}
#    \varepsilon_x \\ \varepsilon_y \\ \gamma_{xy}
#    \end{bmatrix}
#    =
#    \mathbf{B} \cdot  \mathbf{u_{\text{nodal}}}
#
# .. math::
#
#    \mathbf{B} = \frac{1}{\det{\mathbf{J}}}
#    \begin{bmatrix}
#    \mathbf{B_1} & \mathbf{B_2} & \mathbf{B_3} & \mathbf{B_4}
#    \end{bmatrix}
#
# where
#
# .. math::
#
#    \mathbf{B_i} =
#    \begin{bmatrix}
#    a \frac{\partial N_i}{\partial s} - b \frac{\partial N_i}{\partial t} & 0 \\
#    0 & c \frac{\partial N_i}{\partial t} - d \frac{\partial N_i}{\partial s} \\
#    c \frac{\partial N_i}{\partial t} - d \frac{\partial N_i}{\partial s} & a \frac{\partial N_i}{\partial s} - b \frac{\partial N_i}{\partial t}
#    \end{bmatrix}
#
# and
#
# .. math::
#
#    \begin{bmatrix}
#    d & c\\
#    a & b
#    \end{bmatrix}=
#    \frac{1}{4}
#    \begin{bmatrix} \mathbf{X_{\text{locs}}}^T \\ \mathbf{Y_{\text{locs}}}^T \end{bmatrix}  \cdot
#    \begin{bmatrix} \mathbf{S} & \mathbf{T} \end{bmatrix}
#
# for
#
# .. math::
#
#    \mathbf{S} = \begin{bmatrix} s - 1 \\ -(s+1) \\ s+1 \\ -(s-1) \end{bmatrix}
#
# .. math::
#
#    \mathbf{T} = \begin{bmatrix} t - 1 \\ -(t-1) \\ t+1 \\ -(s+1) \end{bmatrix}


def grad_N(self, s, t):
    return 0.25 * np.array(
        [
            [-(1 - t), +(1 - t), +(1 + t), -(1 + t)],
            [-(1 - s), -(1 + s), +(1 + s), +(1 - s)],
        ],
        dtype=float,
    )


def B(self, s, t):
    j = self.J(s, t)
    S = np.array([-1 + s, -1 - s, +1 + s, +1 - s], dtype=float)
    T = np.array([-1 + t, +1 - t, +1 + t, -1 - t], dtype=float)
    [d, c], [a, b] = (
        0.25 * np.c_[self.nodes[:, 0], self.nodes[:, 1]].T.dot(np.c_[S, T])
    ).tolist()
    n = self.grad_N(s, t)

    def _bi_(i):
        return np.array(
            [
                [a * n[0, i] - b * n[1, i], 0],
                [0, c * n[1, i] - d * n[0, i]],
                [c * n[1, i] - d * n[0, i], a * n[0, i] - b * n[1, i]],
            ],
            dtype=float,
        )

    return 1.0 / j * np.c_[_bi_(0), _bi_(1), _bi_(2), _bi_(3)]


MyElementDemo.grad_N = grad_N
MyElementDemo.B = B

my_elem.B(0, 0)

###############################################################################
# Stress Calculation
# ~~~~~~~~~~~~~~~~~~
# The leap from strains to stresses involves the constitutive model,
# i.e., the material properties.  This demo assumes a very simple
# case, i.e., a linear isotropic material which converts strains to
# stresses according to the following matrix:
#
# .. math::
#
#    \mathbf{\sigma}
#    =
#    \mathbf{C} \cdot \mathbf{\varepsilon}
#
# .. math::
#
#    \begin{bmatrix}
#    \sigma_x \\ \sigma_y \\ \tau_{xy}
#    \end{bmatrix}
#    =
#    \begin{bmatrix}
#    1 & \nu & 0 \\
#    \nu & 1 & 0 \\
#    0 & 0 & 1
#    \end{bmatrix}
#    \begin{bmatrix}
#    \varepsilon_x \\ \varepsilon_y \\ \gamma_{xy}
#    \end{bmatrix}


class Isotropic:
    def __init__(self, ex, nu):
        self.nu = nu
        self.ex = ex

    def evaluate(self):
        d = np.array(
            [[1, self.nu, 0], [self.nu, 1, 0], [0, 0, (1 - self.nu) / 2.0]],
            dtype=float,
        )

        return d * (self.ex / (1 - self.nu**2))


isotropic = Isotropic(30e6, 0.25)

###############################################################################
# Stiffness Calculation
#
# The total energy of a system :math:`E`, comprising an element on which nodal
# forces :math:`\mathbf{F}_{\text{nodal}}` are applied and undergoes nodal
# deformation :math:`\mathbf{u}_{\text{nodal}}` is:
#
# .. math::
#
#    E = - \mathbf{F}_{\text{nodal}} \cdot \mathbf{u}_{\text{nodal}} + \frac{1}{2} \iiint_V{} \mathbf{\varepsilon}^T \cdot \mathbf{\sigma} \,dV
#
#
# The first term stems from the work by the force at the nodes while the second
# measures the strain energy density accumulated throughout the element volume
# as it deforms.
#
# As we saw, both stress and strain relate back to the nodal displacements
# through the B (courtesy of the shape functions), i.e.,
# :math:`\mathbf{\varepsilon} = \mathbf{B} \cdot \mathbf{u}_{\text{nodal}}` and
# :math:`\mathbf{\sigma} = \mathbf{C} \cdot \mathbf{B} \cdot
# \mathbf{u}_{\text{nodal}}`
# thus:
#
# .. math::
#
#    E = -\mathbf{F}_{\text{nodal}} \cdot \mathbf{u}_{\text{nodal}} + \frac{1}{2} \iiint_V{} \mathbf{u}_{\text{nodal}}^T \cdot \mathbf{B}^T \cdot \mathbf{C} \cdot \mathbf{B} \cdot \mathbf{u}_{\text{nodal}} \,dV

###############################################################################
# Our assumed linear shape functions are not as rich as the true functions
# governing the actual deformation of the structure in real life.  Imagine a
# Taylor expansion: our linear shape function captures up to the first
# polynomial term, whereas the true shape function could have arbitrarily many
# beyond that. One way this shows up is in the total energy of our system.
# When constrained to use our limited fidelity shape functions the system will
# accumulate a higher total energy than that of the true solution it is meant
# to approximate.  To seek the best approximation, it makes sense to find a
# minimum of this total energy relative to the possible solutions, i.e., nodal
# displacements :math:`\mathbf{u}_{\text{nodal}}`.  Loyal to our calculus
# roots, we look for the minimum by taking the corresponding partial
# derivative:
#
# .. math::
#
#    \frac{\partial E}{\partial \mathbf{u}_{\text{nodal}}} = -\mathbf{F}_{\text{nodal}} + \frac{1}{2} \iiint_V{} \mathbf{B}^T \cdot \mathbf{C} \cdot \mathbf{B} \cdot \mathbf{u}_{\text{nodal}} \,dV =0
#
# .. math::
#
#    \mathbf{F}_{\text{nodal}}  = \frac{1}{2} \iiint_V{} \mathbf{B}^T \cdot \mathbf{C} \cdot \mathbf{B} \cdot \mathbf{u}_{\text{nodal}} \,dV = \mathbf{K} \cdot \mathbf{u}_{\text{nodal}}
#
# Thus, we've unlocked the Hooke's law stiffness hidden in the integral:
#
# .. math::
#
#    \mathbf{K} = \iiint_V{} \mathbf{B}^T \cdot \mathbf{C} \cdot \mathbf{B} \,dV

###############################################################################
#
# For our planar element, assumed to have constant thickness :math:`h` and area
# :math:`A`:
#
# .. math::
#
#    \mathbf{K} = h \iint_A{} \mathbf{B}^T \cdot \mathbf{C} \cdot \mathbf{B} \,dA=h \iint_A{} \mathbf{B}^T \cdot \mathbf{C} \cdot \mathbf{B}   \,dx \,dy = h \iint_A{} \mathbf{B}^T \cdot \mathbf{C} \cdot \mathbf{B} \cdot \det(\mathbf{J})  \,ds \,dt
#
# And the integral can be approximated by Gaussian quadrature through a weighted sum with the optimal sampling points for :math:`\mathbf{B}`:
#
# .. math::
#
#    \mathbf{K}\approx
#    h \sum_{(s,t) \in \text{Gauss}} w(s,t) \cdot \mathbf{B}^T(s,t) \cdot \mathbf{C} \cdot \mathbf{B}(s,t) \cdot \det(\mathbf{J}(s,t))
#
# Thus the use of an isoparametric formulation allowed us to make this
# integration easy, since the domain of integration is constant, regardless of
# the shape of the 2D quadrilateral at hand.


def K(self, C):
    tot = np.zeros((self.ndof, self.ndof), dtype=float)
    for st in self.gauss_pts:
        B = self.B(*(st.tolist()))
        J = self.J(*(st.tolist()))
        tot += B.T.dot(C).dot(B) * J

    return tot


MyElementDemo.K = K
MyElementDemo.ndof = 8


###############################################################################

stiffness = my_elem.K(isotropic.evaluate())
print(stiffness)


###############################################################################

stiffness_scaled = np.round(stiffness / 1e4)
print(stiffness_scaled)


###############################################################################
# Putting it all together
# ~~~~~~~~~~~~~~~~~~~~~~~
# Creating `Elem2D` class.
#


class Elem2D:
    gauss_pts = (
        np.array([[-1, -1], [1, -1], [1, 1], [-1, 1]], dtype=float) * 0.57735026918962
    )
    nnodes = 4
    ndof = 8

    def __init__(self, nodes):
        self.nodes = nodes

    def B(self, s, t):
        j = self.J(s, t)
        S = np.array([-1 + s, -1 - s, +1 + s, +1 - s], dtype=float)
        T = np.array([-1 + t, +1 - t, +1 + t, -1 - t], dtype=float)
        [d, c], [a, b] = (
            0.25 * np.c_[self.nodes[:, 0], self.nodes[:, 1]].T.dot(np.c_[S, T])
        ).tolist()
        n = self.__grad_Ni(s, t)

        def _bi_(i):
            return np.array(
                [
                    [a * n[0, i] - b * n[1, i], 0],
                    [0, c * n[1, i] - d * n[0, i]],
                    [c * n[1, i] - d * n[0, i], a * n[0, i] - b * n[1, i]],
                ],
                dtype=float,
            )

        return 1.0 / j * np.c_[_bi_(0), _bi_(1), _bi_(2), _bi_(3)]

    def __Ni(self, s, t):
        return 0.25 * np.array(
            [
                (1 - s) * (1 - t),
                (1 + s) * (1 - t),
                (1 + s) * (1 + t),
                (1 - s) * (1 + t),
            ],
            dtype=float,
        )

    def __grad_Ni(self, s, t):
        return 0.25 * np.array(
            [
                [-(1 - t), +(1 - t), +(1 + t), -(1 + t)],
                [-(1 - s), -(1 + s), +(1 + s), +(1 - s)],
            ],
            dtype=float,
        )

    def J(self, s, t):
        upper = np.array(
            [
                [0, -t + 1, +t - s, +s - 1],
                [0, 0, +s + 1, -s - t],
                [0, 0, 0, +t + 1],
                [0, 0, 0, 0],
            ],
            dtype=float,
        )
        temp = upper - upper.T
        return 1.0 / 8 * self.nodes[:, 0].dot(temp).dot(self.nodes[:, 1])

    def k(self, C):
        tot = np.zeros((self.ndof, self.ndof), dtype=float)
        for st in self.gauss_pts:
            B = self.B(*(st.tolist()))
            J = self.J(*(st.tolist()))
            tot += B.T.dot(C).dot(B) * J

        return tot

    def N(self, s, t):
        n_vec = self.___Ni(s, t)
        return np.array(
            [
                [n_vec[0], 0, n_vec[1], 0, n_vec[2], 0, n_vec[3], 0],
                [0, n_vec[0], 0, n_vec[1], 0, n_vec[2], 0, n_vec[3]],
            ]
        )

    def M(self, rho):
        tot = np.zeros((8, 8), dtype=float)
        for st in self.gauss_pts:
            n_array = self.N(*(st.tolist()))
            tot += n_array.T.dot(n_array)

        return tot


###############################################################################
# Isotropic class definition


class Isotropic:
    def __init__(self, ex, nu):
        self.nu = nu
        self.ex = ex

    def evaluate(self):
        d = np.array(
            [[1, self.nu, 0], [self.nu, 1, 0], [0, 0, (1 - self.nu) / 2.0]],
            dtype=float,
        )

        return d * (self.ex / (1 - self.nu**2))


###############################################################################
# Applying the created classes.

isotropic = Isotropic(30e6, 0.25)
elem = Elem2D(nodes)

stiffness = elem.k(isotropic.evaluate())

stiffness_scaled = np.round(stiffness / 1e4)
print(stiffness_scaled)


###############################################################################
# Element in PyMAPDL
# ~~~~~~~~~~~~~~~~~~
# Now let's obtain the same stiffness matrix from MAPDL
#
# launch PyMAPDL

from ansys.mapdl.core import launch_mapdl

mapdl = launch_mapdl()
mapdl.clear()


###############################################################################
# Create a use a 2-D 4-Node Structural Solid element with matching material
# properties.

mapdl.prep7()
mapdl.et(1, 182)
mapdl.mp("ex", 1, 30e6)  # Young's modulus
mapdl.mp("nuxy", 1, 0.25)  # Poisson's ratio
mapdl.mp("dens", 1, 1)
# unit density


###############################################################################
# Create the nodes at the same locations as above.

for i, n in zip(node_ids, nodes):
    mapdl.n(i, *n)


###############################################################################
# Setup our element with the corresponding material properties.

_ = mapdl.e(*node_ids)  # Using '_ =' to hide output.


###############################################################################
# Setup the static analysis.

mapdl.slashsolu()
mapdl.antype("static", "new")


###############################################################################
# Solve and permit one degree of freedom of each mode to be free per solution.

dof_list = list(itertools.product(node_ids, ["ux", "uy"]))

for node_id, dof in dof_list:
    mapdl.d("all", "all")
    mapdl.d(node_id, dof, 1)
    mapdl.solve()

mapdl.finish()

###############################################################################
# The columns of the stiffness matrix appear as nodal force reactions

results = []

for i, _ in enumerate(dof_list):
    mapdl.post1()
    mapdl.set(i + 1)
    prrsol_f = mapdl.prrsol("f").to_array()[:, 1:]  # Omitting node column (0)
    results.append(prrsol_f)

for txt in results:
    print(txt)
    print("=" * 80)


###############################################################################
# Now, apply this to the whole matrix and output it.

stiffness_mapdl = np.array(results)
stiffness_mapdl = stiffness_mapdl.reshape(8, 8)
stiffnes_mapdl_scaled = np.round(stiffness_mapdl / 1e4)
print(stiffnes_mapdl_scaled)


###############################################################################
# Which is identical to the stiffness matrix obtained from our
# academic formulation.

print(stiffness_scaled)


###############################################################################
# Show that the stiffness matrix in MAPDL matches what we derived.

if np.allclose(stiffnes_mapdl_scaled, stiffness_scaled):
    print("Both matrices are the equal within tolerance.")


###############################################################################
# Stop mapdl
# ~~~~~~~~~~
#
mapdl.exit()
