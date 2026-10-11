(sec:essentialelements.relativistic)=
# 相对论计算（Relativistic Calculations）

ORCA 提供三种不同的近似来涵盖相对论效应（relativistic effects）：

1. "精确二分量"（[X2C](sec:essentialelements.relativistic.x2c)）哈密顿量（Hamiltonian）
2. 二阶 Douglas-Kroll-Hess（[DKH](sec:essentialelements.relativistic.dkh)）哈密顿量
3. 带模型势（model potential）的零阶正则近似（[ZORA](sec:essentialelements.relativistic.regularapprox)）

早期版本的 ORCA 还提供若干其他近似，现已不再支持。

后续开发中将持续推进的主相对论哈密顿量是 X2C 哈密顿量。在这三种选择中，
我们认为 X2C 具有最好的特性组合，建议所有用户优先使用该方法。

这三种相对论模型哈密顿量都为标量相对论（scalar relativistic）能量计算
实现，并在整个程序中一致地贯彻。标量相对论表现为加到单电子矩阵上的
一个附加有效势。ORCA 中不提供双电子相互作用的标量相对论校正。
此外，包含自旋-轨道耦合（spin-orbit coupling, SOC）的自洽场计算
（HF、DFT、CASSCF）在 ORCA 中也不可用，但我们不排除在未来版本中
加入这一功能的可能性。

(sec:essentialelements.relativistic.basic)=
## 基本用法（Basic Usage）

ORCA 中的相对论方法以相当直接的方式实现，但用户确实需要一些谨慎。
基本选项可通过简单输入关键词获得，更精细的控制可通过 `%rel` 块实现——
完整关键词列表见 {numref}`sec:essentialelements.relativistic.keywords`。
每种哈密顿量还各有特定的设置——这些在下文相应小节中说明。

以下三行（互斥的）输入分别请求：
- 用 ZORA 哈密顿量进行 TPSS 优化，
  配以[相对论性重构的 `ZORA-def2-TZVP`](sec:essentialelements.basisset.builtin.rel.def2) 基组
  和 `SARC/J` [辅助基组](sec:essentialelements.basisset.aux.auxj)；
- 用二阶 DKH 哈密顿量进行 DLPNO-CCSD(T) 能量计算，
  配以匹配的[相关一致基组](sec:essentialelements.basisset.builtin.rel.cc)
  和合适的 [`AuxC`](sec:essentialelements.basisset.aux.auxc)；
- 用 X2C 哈密顿量进行双杂化 DFT NMR 计算，
  配以[合适的基组](sec:essentialelements.basisset.builtin.rel.karlsruhex2c)。

```orca
! TPSS Opt ZORA ZORA-def2-TZVP SARC/J
# or
! DLPNO-CCSD(T) DKH cc-pVTZ-DK cc-pVTZ/C
# or
! DSD-PBEP86/2013 NMR X2C x2c-TZVPall-s x2c/J
```

相对论计算中基组要求的说明见
{numref}`sec:essentialelements.relativistic.basissets`，
可用基组列表见 {numref}`sec:essentialelements.basisset.builtin.rel`。

:::{warning} 警告
- 较早版本的 ORCA 在检测到使用 DKH 或 ZORA 哈密顿量时，
  会大量使用自动基组替换和别名。现在已不再如此！
  基组的相对论版本现在必须用相应的前缀显式请求。
  对于 Kr 之后的元素，SARC 基组也必须显式请求。
- 用 DKH 和 ZORA（但不含 X2C）进行的几何优化会自动使用
  [单中心近似](sec:essentialelements.relativistic.hamiltonian.1c)。
  计算相对能量时，不要把不带单中心近似的单点计算能量
  与使用了该特性的几何优化能量混用。
:::

(sec:essentialelements.relativistic.basic.props)=
### 标量相对论梯度与性质

在这三种模型哈密顿量中，只有 X2C 具有解析梯度。因此对于几何优化，
这也是首选方法。对于 DKH 和 ZORA，程序会自动切换到
[单中心近似](sec:essentialelements.relativistic.hamiltonian.1c)。
这需要用户多加注意，因为用单中心近似得到的最终单点能量
与不用该近似得到的能量不一致。单中心近似通常精度足够，
但我们在实际应用中观察到过它导致明显错误几何结构的情形。
因此，我们强烈建议在这一领域使用 X2C 哈密顿量（甚至使用基于 ECP 的计算）。

如果把相对论计算用于分子性质，非相对论计算的性质积分与相对论哈密顿量
之间存在潜在的不匹配。消除这些不一致性的流程称为"图像变换"
（picture change）。它由 `%rel` 中的关键词 `PictureChange` 控制，
在大多数计算中默认激活。

```orca
%rel 
  FiniteNuc     true   # Invokes the Gaussian finite nucleus model.
  PictureChange 1 or 2 # First or second order picture change effects.
                       # Second order is potentially more accurate and more expensive.
end
```

图像变换效应对 DKH 和 X2C 已实现，对 ZORA 也在一定程度上实现。
不过，它们并非对 ORCA 能计算的所有性质都已实现。请注意性质积分程序
和性质程序的输出。这两个程序都会明确说明分子积分中包含了哪些图像变换效应。
更多细节见 {numref}`sec:essentialelements.relativistic.picturechange`。
上面的例子还调用了有限核模型——见
{numref}`sec:essentialelements.relativistic.finnuc`。

(sec:essentialelements.relativistic.hamiltonian)=
## 近似相对论哈密顿量

在相对论领域，计算基于原子单位下（减去静止质量）的单电子定态
Dirac 方程

$$h_{D} \Psi =\left({ \left({ \beta -1} \right)c^{2}+c \boldsymbol\alpha \cdot \boldsymbol p +V} \right)\Psi =E\Psi .
$$ (eqn:rel-h-dirac)

旋量（spinor）$\Psi$ 可以分解为其所谓的大分量（large component）
和小分量（small component）

$$\Psi =
\begin{pmatrix}
\Psi_L \\
\Psi_S
\end{pmatrix}
$$ (eqn:rel-spinorLS)

它们显然通过 Dirac 方程耦合。更准确地说，求解 $\Psi_{S}$ 后可得：

$$\Psi_{S} =\frac{1}{2c}\left(1+\frac{E-V}{2c^{2} } \right)^{-1}\boldsymbol\sigma\cdot\boldsymbol p \Psi_{L} =R\Psi_{L}
$$ (eqn:exact-relativistic)

通过幺正变换（unitary transformation）

$$U=
\begin{pmatrix}
\Omega_+ & - R^+\Omega \\
R\Omega_+ & \Omega_-
\end{pmatrix}
$$ 

其中

$$
\Omega_{+} =\frac{1}{\sqrt{1+R^{+}R} },\Omega_{-} =\frac{1}{\sqrt{ 1+RR^{+} } }
$$

可把哈密顿量化为块对角（block-diagonal）形式

$$U^{+}h_{D} U=
\begin{pmatrix}
\tilde h_{++} & 0 \\
0 & \tilde h_{--}
\end{pmatrix}
$$ (eqn:rel-unitary-decoupling)

（电子的）大分量因而必须满足如下关系

$$h_{++} \Psi_{L} =\Omega_{+} \left({ h_{++} +h_{\pm } R+R^{+}\left({ h_{\mp
} +h_{--} R} \right)} \right)\Omega_{+} \Psi_{L} =E_{+} \Psi_{L} .
$$ (eqn:exact-relativistic-2c)

ORCA 中实现的近似相对论方案（DKH 和 ZORA）用不同的方法把精确关系
{eq}`eqn:exact-relativistic-2c` 替换为近似关系，
而 X2C 形式体系则精确求解该模型单电子问题。

(sec:essentialelements.relativistic.hamiltonian.1c)=
### 单中心近似（One-Center Approximation）

在单中心近似中——它可应用于 DKH、ZORA 或 X2C 中的任何方法——
{eq}`eqn:rel-h-dirac` 中的模型势 $V$ 只含单中心项，
即忽略与其他原子的相互作用。这有几个好处：
- 幺正解耦变换 {eq}`eqn:rel-unitary-decoupling` 只需在原子基内
  对每种原子类型求解，而不必对整个体系求解。
- ZORA 或 IORA 中没有规范非不变性误差。
- 最重要的是，对于几何微扰（即梯度/Hessian）
  没有[图像变换效应](sec:essentialelements.relativistic.picturechange)，
  因为相对论校正与分子几何结构无关。因此，所有相对论方法都可以用于
  几何优化和频率计算，而相对于非相对论计算，其计算代价可以忽略。

文献中多篇论文表明，该近似对结构参数和振动频率的计算相当精确。
因此，对于需要解析梯度或 Hessian 的 DKH 和 ZORA 计算，默认启用它，
而且实际上不启用时这类计算并未实现（尽管全数值梯度/Hessian 是可用的）。
对于 X2C，几何微扰的图像变换校正已经实现，因此默认不启用单中心近似。
该近似可通过简单关键词 `!Rel1C`（开）和 `!RelFull`（关），
或 `%rel` 块中的 `OneCenter` 关键词显式控制。

:::{warning} 警告
使用与不使用单中心近似得到的能量不可比较！
:::

```{index} ZORA
```
(sec:essentialelements.relativistic.regularapprox)=
## 正则近似（Regular Approximation）

在正则近似中，{eq}`eqn:exact-relativistic-2c` 被近似为

$$R=\frac{c}{2c^{2}-V} \boldsymbol\sigma \cdot \boldsymbol p.
$$ (eqn:166)

在零阶（ZORA）下，$\Omega_{\pm } =1$，因此 ZORA 变换简单地是

$$U_{\mathrm{ZORA} } =
\begin{pmatrix}
1 & -R^+ \\
R & 1
\end{pmatrix}
$$ (eqn:167)

而相应的哈密顿量为

$$\tilde{{h} }_{++}^{\mathrm{ZORA} } =V+c \boldsymbol\sigma \cdot \boldsymbol p \frac{1}{2c^{2}-V}c\boldsymbol\sigma \cdot \boldsymbol p.
$$ (eqn:168)

在无限阶（IORA）下，$\Omega_{\pm }$ 被考虑在内，于是

$$U_{\mathrm{IORA} } =U_{\mathrm{ZORA} }
\begin{pmatrix}
\Omega_+ & 0 \\
0 & \Omega_-
\end{pmatrix}
$$ (eqn:169)

且

$$\tilde{{h} }_{++}^{\mathrm{IORA} } =\Omega_{+} \left({ V+c \boldsymbol\sigma \cdot \boldsymbol p \frac{1}{2c^{2}-V}c \boldsymbol\sigma \cdot \boldsymbol p} \right)\Omega_{+}
$$ (eqn:170)

是相应的哈密顿量。请注意，尽管名为*无限阶*正则近似，它仍然*不是*精确的。

在 ORCA 中，实现了 ZORA 和 IORA 的无自旋（标量相对论）变体。
它们由上式通过如下替换得到

$$\boldsymbol\sigma \cdot \boldsymbol p \frac{1}{2c^{2}-V} \boldsymbol\sigma \cdot \boldsymbol p \to \boldsymbol p \frac{1}{2c^{2}-V} \boldsymbol p.
$$ (eqn:171)

正则哈密顿量只含 Darwin 项的一部分，不含质量-速度项。
关系 {eq}`eqn:170` 和 {eq}`eqn:168` 的一个问题在于：
由于所得正则哈密顿量对 $V$ 的非线性依赖，$V$ 的常数改变——
这在 Dirac 和 Schrödinger 方程中会导致能量的相应改变

$$E\to E+\text{const}$$

——在正则近似中却不会如此。人们已多次尝试绕过这一问题。
标度 ZORA 变体（scaled ZORA variant）就是这样一种方案。
另一种方案是引入替代 $V$ 的模型势。这两种方法在 ORCA 中都可用。

### 标度 ZORA 变体

这一变体源于 van Lenthe 等人 {cite}`vanlenthe1994jcp`。核心观察是哈密顿量

$$h_{\mathrm{scaledZORA} } =\frac{h_{\mathrm{ZORA} } }{1+\left\langle { \Psi_{L} \left|{c \boldsymbol\sigma \cdot \boldsymbol p \frac{1}{\left({ 2c^{2}-V}
\right)^{2} }c \boldsymbol\sigma \cdot \boldsymbol p} \right|\Psi_{L} } \right\rangle}
$$ (eqn:172)

当势 $V$ 改变一个常数时，产生常数能量平移 $E\to E+\text{const}$
——*对于类氢离子*。对于多电子体系，标度 ZORA 哈密顿量在
$V\to V+\text{const}$ 时仍不给出简单的常数能量平移。
但它对类氢原子给出精确的 Dirac 能量，且对原子电离能的表现
优于一阶正则近似。

(sec:essentialelements.relativistic.zora)=
### 带模型势的正则近似

这一方法的思想源于 Van Wüllen {cite}`vanwuellen1998jcp`，
他为 DFT 提出了该方案。不过我们也把它用于其他方法。
标量相对论 ZORA 自洽场方程在我们的实现中（原子单位）为：

$$\left[{ \mathrm{\mathbf{p} }\frac{c^{2} }{2c^{2}-V }\mathrm{\mathbf{p} }+V_{\mathrm{eff} } } \right]\psi_{i} =\varepsilon_{i} \psi_{i}
$$ (eqn:173)

其中 $c$ 是光速。它看起来就像普通的非相对论 Kohn--Sham 方程，
具有 KS 势 $V_{\mathrm{eff} }$：

$$V_{\mathrm{eff} } \left({ \mathrm{\mathbf{r} }} \right)=-\sum\limits_A { \frac{Z_{A} }{\left|{\mathrm{\mathbf{r} }-\mathrm{\mathbf{R} }_{A} } \right|} } +\int \frac{\rho \left( \mathrm{\mathbf{r}'} \right)}{\left| \mathrm{\mathbf{r} } - \mathrm{\mathbf{r}'} \right|}
d\mathrm{\mathbf{r}'} + V_{\text{xc} } \left[ \rho \right](\mathbf r)
$$ (eqn:174)

（$Z_{A}$ 是核 $A$ 的电荷，$R_{A}$ 是其位置；$\rho (r)$ 是总电子密度，
$V_{xc} \left[ \rho \right]$ 是交换-关联势——交换-关联能量对密度的
泛函导数。）非相对论处理中的动能算符 $T=-\frac{1}{2}\nabla^{2}$
被简单地替换为 ZORA 动能算符：

$$T^{\mathrm{ZORA} }=\mathrm{\mathbf{p} }\frac{c^{2} }{2c^{2}-V }\mathrm{\mathbf{p} }
$$ (eqn:175)

显然，在势 $V$ 相对于 $c^{2}$ 很小的区域，该算符约化为非相对论动能。
$V$ 可以是实际的 KS 势。然而，这会要求以特殊方式求解 ZORA 方程，
需要在每个 SCF 循环中重新计算动能。这会变得昂贵，也不可取，
因为 ZORA 方法不是规范不变的，除非采取特殊的预防措施，
否则这样的流程会带来相当大的误差。因此 Van Wüllen
{cite}`vanwuellen1998jcp` 主张把势 $V$ 替换为模型势
$\tilde{{V} }_{\mathrm{model} }$ 是一个合理的近似，该模型势构造如下：

$$
\tilde{{V} }_{\mathrm{model} } =-\sum\limits_A { \frac{Z_{A} }{\left|{ \mathrm{\mathbf{r} }
-\mathrm{\mathbf{R} }_{A} } \right|} } +\int \frac{\rho_{\mathrm{model} } \left( \mathrm{\mathbf{r}'} \right)}{\left| \mathrm{\mathbf{r} }
-\mathrm{\mathbf{r}'} \right|}
d\mathrm{\mathbf{r}'} +V_{\text{xc} }^{\text{LDA} } \left[{ \rho^{\mathrm{model} }} \right](\mathbf r)
$$ (eqn:176)

模型密度构造为球对称（中性）原子密度之和：

$$\rho_{\mathrm{model} } \left({ \mathrm{\mathbf{r} }} \right)=\sum\limits_A { \rho
^{A}\left({ \mathrm{\mathbf{r} }} \right)}
$$ (eqn:177)

因此，这个密度既没有正确的电子数（对于带电物种），
也没有任何自旋极化。然而在靠近原子核、相对论效应起作用的区域，
它是一个合理的近似。原子密度按 s 型 Gaussian 函数之和展开：

$$\rho^{A}\left({ \mathrm{\mathbf{r} }} \right)=\sum\limits_i { d_{i} \exp \left({-\alpha_{i} \left|{ \mathrm{\mathbf{r} }-\mathrm{\mathbf{R} }_{A} } \right|^{2} } \right)}
$$ (eqn:178)

拟合系数通过近基组极限的标量相对论原子 HF 计算以三种不同方式确定，
并作为库存储在程序中。拟合密度可用于直到 Rn 的元素以及锕系元素。
通过变量 `ModelDens`，用户可以在这些拟合之间选择，
并考察结果对该选择的依赖性（除了可能在较重元素以及不推荐的 HF 密度下，
这种依赖应当相当小）。模型势的各个分量（式 {eq}`eqn:176`）
可通过变量 `ModelPot` 打开或关闭。这些关键词的可用选项列于
{numref}`sec:essentialelements.relativistic.keywords`。例如：

```orca
! ZORA ZORA-def2-TZVP SARC/J
# for more detail use
%rel
     ModelPot 1,1,1,1
     ModelDens rhoZORA
end
```

:::{Attention} 注意
ZORA 方法高度依赖于数值积分，因此务必关注径向积分精度
（radial integration accuracy）这一问题！自 ORCA 5.0 起，
默认情况下我们在格点构建中已加以考虑，默认值应当工作得很好。
只有在非常棘手的情况下，才考虑使用更高的
[`IntAcc` 参数](sec:essentialelements.numericalintegration.radgrid)，
或至少用 `SpecialGridAtoms` 和 `SpecialGridIntAcc` 提高重原子附近的
径向积分精度（见
{numref}`sec:essentialelements.numericalintegration.detailsandoptions`）。
:::


```{index} Douglas-Kroll-Hess (DKH)
```
(sec:essentialelements.relativistic.dkh)=
## Douglas-Kroll-Hess 方法

Douglas-Kroll-Hess（DKH）方法把精确关系
{eq}`eqn:exact-relativistic-2c` 按外势 V 展开。在 ORCA 中实现了
一阶和二阶 DKH 方法。一阶 DKH 哈密顿量为

$$\tilde{h}_{++}^{(1) } =E_{p} +A_{p} VA_{p} +B_{p} V^{(p) }B_{p} ,
$$ (eqn:179)

其中

$$E_{P} =\sqrt{ c^{4}+c^{2}p^{2} }, \, A_{p} =\sqrt{\frac{E_{p} +c^{2} }{2E_{p} }}, \, B_{p} =\frac{c}{\sqrt{ 2E_{p} (E_{p} +c^{2}) } }
$$ (eqn:180)

在二阶下，它写作

$$\tilde{{h} }_{++}^{(2) } =\tilde{{h} }_{++}^{(1) } +\frac{1}{2}\left[{ W_{p} ,O} \right]$$ (eqn:181)

其中

$$\left\{{ W_{p} ,E_{p} } \right\}=\beta O, \, O=A_{p} \left[{ R_{p} ,V}
\right]A_{p}, \, R_{p} =\frac{c\sigma p}{E_{p} +c^{2} }
$$ (eqn:182)

定义了二阶贡献。在 ORCA 中实现了 $\tilde{{h} }_{++}^{(2) }$ 的无自旋部分。

相对论动能 $E_{P}$ 在位置空间中没有良好定义，它的出现使得变换到
$p^{2}$ 本征空间成为必要。因此任何 DKH 计算都以基组的去收缩
（decontraction）开始，以确保恒等算符的良好分解。然后对角化非相对论
动能，并在该空间中计算依赖 $E_{P}$ 的算符。势 $V$ 和 $V^{(p) }$
被变换到 $p^{2}$ 本征空间。在所有贡献相乘得到（一阶或二阶）哈密顿量后，
再变换回 AO 空间并把基组重新收缩。

（无自旋的）DKH 哈密顿量包含所有无自旋的相对论校正项，
例如质量-速度项和 Darwin 项。由于势线性地进入，无需标度或模型势
即可引入能量在如下改变下的正确行为

$$V\to V+\text{const}.$$

在所有这些方面，DKH 哈密顿量都比正则近似哈密顿量干净得多。

一阶或二阶 DKH 方法可分别通过简单输入关键词 `DKH1` 或 `DKH2` 请求
（`DKH` 是后者的别名），并配以合适的基组：

```orca
! DKH DKH-def2-TZVP SARC/J
```

对大多数计算而言，不需要其他设置。可用关键词的完整列表见
{numref}`sec:essentialelements.relativistic.keywords`。

(sec:essentialelements.relativistic.dkh.magnetic)=
### DKH 下的磁性质

对于磁性质，DKH 变换以及由此而来的 DKH 哈密顿量和相应的性质算符
并不唯一。取决于磁场是否包含在 DKH 流程第一步所执行的自由粒子
Foldy--Wouthuysen（fpFW）变换中，会得到两种不同的哈密顿量。
如果磁场包含在 fpFW 变换中，所得哈密顿量是规范不变动量
（gauge invariant momentum）

$$\boldsymbol{\pi}=\textbf{p}+\textbf{A}.$$

的函数。因此它在磁矢势 $\mathbf A$ 的规范变换下是规范不变的，
由它导出的性质算符也是如此。这称为 f$\pi$FW DKH 哈密顿量。
如果磁场不包含在 FW 变换中，所得哈密顿量只是动能动量 $\textbf{p}$
的函数，因而不是规范不变的。后一种哈密顿量称为 fpFW DKH 哈密顿量。
两种哈密顿量的比较见表 {numref}`table:compdkhham`。

(table:compdkhham)=
:::{table} fpFW 与 fπFW DKH 哈密顿量性质的比较。细节见参考文献 {cite}`sandhoefer2012jcp`。

| 判据                              | fpFW 哈密顿量 | fπFW 哈密顿量     |
|:----------------------------------|:-------------:|:-----------------:|
| 本征值向 Dirac 本征值的收敛性     | ?             | 是                |
| 一阶有界                          | 否            | 是                |
| 重现 Pauli 哈密顿量               | 否            | 是                |
| 规范不变性                        | 否            | 是                |
| Lorentz 不变性                    | 否            | 否                |
:::

从该表可以清楚看出，f$\pi$FW DKH 哈密顿量明显优于 fpFW 哈密顿量。
然而，要获得性质算符，必须对这些哈密顿量求导。结果发现，
对于超精细耦合张量（hyperfine-coupling tensor），
f$\pi$FW DKH 哈密顿量情形下所需的导数会产生发散的性质算符。
这可能源于把核磁矩的磁场源视为点偶极子这一非物理的假设。
由于缺乏实验数据，无法给出核磁化分布的物理描述，
因此假定磁化分布与核电荷分布相同，见
{ref}`sec:essentialelements.relativistic.finnuc` 一节。这是非物理的，
因为磁化是由核内那个未配对的核子引起的，而电荷分布则由核内的质子产生。
因此从物理上说，磁化在空间中占据的体积应大于电荷。这也可能是所得
有限核模型不足以消除 f$\pi$FW 超精细耦合张量中发散的原因。
因此，超精细耦合张量只在由 fpFW DKH 哈密顿量导出的版本中实现。
对于 g 张量，两种版本都已实现，可通过关键词访问

```orca
%rel fpFWtrafo true/false end
```

默认情况下该关键词设为 `true`。用于 g 张量和超精细张量的性质算符的
详细形式见参考文献 {cite}`sandhoefer2012jcp`。

```{index} X2C
```
(sec:essentialelements.relativistic.x2c)=
## 精确二分量理论（X2C）

ORCA 中的 X2C 实现紧密遵循 Franzke、Weigend 及其合作者的工作，
见参考文献：{cite}`Peng2013`（能量）、{cite}`Franzke2018`（梯度）、
{cite}`Franzke2022`（EPR 超精细耦合）、{cite}`Franzke2021a`（NMR
自旋-自旋耦合）、{cite}`Franzke2019`（NMR 屏蔽）。它们也与 Gauss
及其合作者的工作一致，见参考文献：{cite}`Cheng2011`（梯度、电性质）、
{cite}`Cheng2011a`（Hessian）、{cite}`Cheng2013`（NMR 屏蔽）。
不过，尽管名为"精确"，目前只有标量相对论（无自旋）版本可用，
实际上是一个一分量方法（更恰当地称为 "SF-X2C-1e"），
与上文所述的 DKH 和 ZORA 方法非常相似。与后两者的主要区别在于
单电子 Dirac 哈密顿量的解耦是精确的而非近似的。SF-X2C-1e 在 ORCA 中
为能量、梯度和各种性质（见下文）实现，支持点核和有限核两种模型。

我们在此简要描述工作方程，使用上述参考文献的记号，
它与前几节的记号略有不同。直接求解单电子 Dirac 方程：

$$\mathbb{D C} = \mathbb{M C E},
\quad
  \mathbb{C} =
  \begin{pmatrix}
  \mathbf C^{\mathrm L}_{+} & \mathbf C^{\mathrm L}_{-} \\
  \mathbf C^{\mathrm S}_{+} & \mathbf C^{\mathrm S}_{-} \\
  \end{pmatrix} 
$$ (eq:x2c-DCSCE)

以获得幺正变换矩阵：

$$\begin{aligned}
  \mathbb{U} &= 
  \begin{pmatrix}
  \mathbf U_{++} & \mathbf U_{+-} \\
  \mathbf U_{-+} & \mathbf U_{--} \\
  \end{pmatrix}
  = 
  \begin{pmatrix}
  \mathbf 1 & -\mathbf X^\dagger \\
  \mathbf X & \mathbf 1 \\
  \end{pmatrix}
  \begin{pmatrix}
  \mathbf R & \mathbf 0 \\
  \mathbf 0 & \mathbf R' \\
  \end{pmatrix}
\\
  \mathbf X &= \mathbf C^{\mathrm S}_{+} \left( \mathbf C^{\mathrm L}_{+} \right)^{-1}\\
  \mathbf R &= \mathbf S^{-\frac{1}{2} } \left(\mathbf S^{-\frac{1}{2} }\tilde{\mathbf S} \mathbf S^{-\frac{1}{2} }\right)^{-\frac{1}{2} } \mathbf S^{\frac{1}{2} }\\
  \tilde{\mathbf S} &= \mathbf S + \frac{1}{2c^2}\mathbf X^\dagger \mathbf T \mathbf X
\end{aligned}$$

它精确地把哈密顿量块对角化：

$$\mathbb{U^\dagger D U} =
  \begin{pmatrix}
  \mathbf h^{+} & \mathbf 0 \\
  \mathbf 0 & \mathbf h^{-} \\
  \end{pmatrix}
$$ (eq:x2c-UDU)

$$\mathbf h^{+} = 
  \mathbf R^\dagger \mathbf L \mathbf R
$$ (eq:x2c-h)

$$ \mathbf L = \mathbf V + \mathbf T \mathbf X + \mathbf X^\dagger \mathbf T 
 +\mathbf X^\dagger \left(\frac{1}{4c^2} \mathbf W - \mathbf T\right) \mathbf X
$$ (eq:x2c-L)

其中 $\mathbf V$、$\mathbf T$、$\mathbf S$ 和 $\mathbf W$ 分别是
势、动能、重叠和相对论势（$\hat p\,\hat V\hat p$）积分矩阵。
因此 $\mathbf h^{+}$ 就是用于后续计算的相对论校正单电子哈密顿量的矩阵形式。

请注意，上述方程中使用的势算符 $\hat V$ 只包含电子-核 Coulomb 相互作用。
外部点电荷可通过 `%rel ModelPot[4]=1` 选择性地包含（默认 0）。
该选项影响能量和 NMR 屏蔽计算，但目前对梯度或 Hessian 不可用。

在最简单的情况下，只需在输入中添加 `X2C` 简单关键词并选择合适的基组：

```orca
! X2C X2C-TZVPall X2C/J
```

(sec:essentialelements.relativistic.x2c.dlu)=
### DLU 近似

幺正变换矩阵的对角局域近似（diagonal local approximation to the
unitary transformation matrix, DLU）由 Peng 和 Reiher
{cite}`Peng2012` 引入，它通过把 $\mathbb U$（即 $\mathbf R$ 和
$\mathbf X$）近似为原子块对角矩阵，降低了 X2C 变换的计算代价。
它导致的精度损失非常小，特别适合梯度/Hessian 计算。

$$\begin{aligned}
  \mathbf R &\approx \bigoplus_A \mathbf R_A
&
  \mathbf X &\approx \bigoplus_A \mathbf X_A\end{aligned}$$

其中 $\bigoplus_A$ 表示原子对角块的直和。
方程 {eq}`eq:x2c-DCSCE`--{eq}`eq:x2c-L` 随后可对对角原子块
$\mathbf h^+_{AA}$ 独立求解。非对角块 $\mathbf h^+_{AB}$ 由下式得到：

$$\begin{aligned}
    \mathbf h^+_{AB}  &= \mathbf R^\dagger_A \mathbf L_{AB} \mathbf R_B
\\
    \mathbf L_{AB} &= \mathbf V_{AB} + \mathbf T_{AB} \mathbf X_B + \mathbf X^\dagger_A \mathbf T_{AB} + \mathbf X^\dagger_A \left(\frac{1}{4c^2}\mathbf W_{AB} - \mathbf T_{AB}\right) \mathbf X_B\end{aligned}$$

也可以把轻原子 $a,b$（低于某一原子序数）近似为非相对论的：

$$\begin{aligned}
  \mathbf X_a &= \mathbf R_a = \mathbf I
\\
  \mathbf W_{ab} &= \mathbf W_{aB} = \mathbf 0
\\
  \mathbf h^+_{ab} &= \mathbf V_{ab} + \mathbf T_{ab}
\\
  \mathbf h^+_{aB} &= \left(\mathbf V_{aB} + \mathbf T_{aB} \mathbf X_B\right) \mathbf R_B\end{aligned}$$

与单中心近似（X2C 也可用）不同，所有原子核都包含在势算符 $\hat V$ 中。

DLU 近似可通过简单输入关键词 `!DLU-X2C` 请求。`%rel` 块中还有
附加选项（另见 {numref}`sec:essentialelements.relativistic.keywords`）：

```orca
%rel
  DLU         false # default - not used
               true # turn DLU on
  LightAtomThresh 0 # (default) highest atomic number treated as non-relativistic
end
```

(sec:essentialelements.relativistic.x2c.props)=
### X2C 导数与性质

如 {numref}`sec:essentialelements.relativistic.picturechange` 中所讨论的，
用相对论方法计算性质时，需要对正确的哈密顿量求导，
即 X2C 情形下的 $\mathbf h^+$（式 {eq}`eq:x2c-h`）。其中包含来自
$\mathbf R$ 和 $\mathbf X$ 导数的贡献，这些贡献通常很小。
因此可以通过以下选项忽略它们，以节省一些计算时间：

```orca
%rel
  PictureChange 2 # compute the full relativistic Hamiltonian derivative
                1 # neglect derivatives of R and X
                0 # (default) use the non-relativistic operator
end
```

同一设置适用于所有实现了 X2C 校正的性质。目前这些性质是：
几何梯度、电偶极矩、四极矩和极化率、电场梯度、EPR 超精细耦合，
以及 NMR 屏蔽和自旋-自旋耦合。对于 Hessian，X2C 校正以半数值方式实现。
如果请求，DLU 近似全程应用，并大幅降低计算代价。请注意，
对于磁性质，只要请求了 GIAO（例如 NMR 屏蔽），小分量基函数就使用
限制性磁平衡（restricted magnetic balance, RMB）；
否则使用限制性动能平衡（restricted kinetic balance, RKB）
（例如 NMR 耦合）。用于各种性质的自旋-轨道耦合积分只包含单电子项的
相对论校正，与 DKH 的情况相同。

对于数目与原子数成正比的二阶导数性质——例如 NMR 耦合的 DSO 项——
完全 X2C 二阶导数所需的各种中间量的一阶导数会被存储到磁盘上。
存储需求可通过 `StorageLevel` 关键词降低，缺失的中间量将即时重算，
这当然会增加计算时间。

```orca
%rel
  StorageLevel 0 # do not store anything - not always available
               1 # store integral derivatives
               2 # 1 + derivatives of R and X (default, minimum for DLU)
               3 # 2 + derivatives of L
               4 # 3 + derivatives of S-tilde
               5 # 4 + derivatives of D and M
end
```

(sec:essentialelements.relativistic.basissets)=
## 相对论计算中的基组

不同的标量相对论势在核心区域具有不同的形状。因此，
每一种都需要针对相应哈密顿量优化的专用全电子基组。这样的基组
已经设计出来：既有针对直到 Kr 的元素（其原始非相对论版本是全电子的）
[Ahlrichs](sec:essentialelements.basisset.builtin.rel.ahlrichs) 和
[Karlsruhe](sec:essentialelements.basisset.builtin.rel.def2) 基组的
DKH 和 ZORA 重构版本，也有针对 Kr 之后元素专门构建的分段全电子
相对论收缩（segmented all-electron relativistically contracted, SARC）
基组。{cite}`Pantazis2008,Buehl2008,Pantazis2009,Pantazis2011,Pantazis2012,Rolfes2020`
对于 X2C 计算，可使用 ["x2c-XVPall" 基组](sec:essentialelements.basisset.builtin.rel.karlsruhex2c)
及其变体。{cite}`Weigend2017-x2c-XVP,Weigend2019-x2c-XVP-s`
所有可用的内置选择列于 {ref}`sec:essentialelements.basisset.builtin.rel` 一节。

一个足够大的未收缩全电子基组总是可行的。同样，各种 RI 计算中的
未收缩拟合基组也总是合适的。使用
[`!Decontract` 关键词](par:essentialelements.basisset.basicusage.decontract)
把所选基组去收缩，使其适合任何相对论哈密顿量，也便于它们之间的比较。

如果在标量相对论计算中使用大的未收缩基组，存在明显的变分坍缩
（variational collapse）风险。这一行为与相对论轨道在点核情况下会发散
这一事实有关。ORCA 对 DKH 和 X2C 提供了 Dyall 和 Visscher 的
Gaussian 有限核模型。我们建议在相对论计算中始终使用该功能
（`FiniteNuc`）（见 {numref}`sec:essentialelements.relativistic.finnuc`）。

鉴于重元素化合物的相对论全电子计算具有非常陡峭的核心基函数，
数值积分（如 DFT 和 COSX 中的）可能颇具挑战。ORCA 提供自动流程，
使积分格点适应陡峭基函数的存在。不过，如果你遇到奇怪的结果，
数值积分是一个潜在的问题来源。解决办法是改用更大的积分格点，
并特别提高[径向积分精度](sec:essentialelements.numericalintegration.radgrid)
（`IntAcc`）。

```{index} PictureChange
```
(sec:essentialelements.relativistic.picturechange)=
## 图像变换效应（Picture-Change Effects）

无论在确定波函数时使用了哪种哈密顿量，性质的计算都需要一些特别的关照。
这可以从两方面理解：首先，我们从普通的 Schrödinger 哈密顿量
换成了一个更复杂的哈密顿量。由于性质定义为能量的导数，
显然新的哈密顿量会给出能量的新表达式，因而给出所讨论性质的新表达式。
另一种看法是：通过变换 $U$，我们不仅改变了哈密顿量，也改变了波函数。
要获得所求性质作为性质算符对波函数的期望值，
我们必须确保性质算符和波函数实际上处在同一个空间中。
这通过对性质算符或波函数之一做变换来完成。

无论如何，非相对论与（准）相对论性质算符在（准）相对论波函数上
求值的差，称为_图像变换效应_（picture-change effect）。
由上所述，这显然不是一个物理效应。它描述的是准相对论计算被贯彻得
有多一致。一个完全一致的计算要求波函数也在（准）相对论层面上确定，
并且使用（准）相对论性质算符。这可通过启用 `%rel` 块中的
`PictureChange` 选项获得：

```orca
%rel PictureChange 1 end  # or 2 - see below
```

有可能（准）相对论与非相对论性质算符给出相似的结果。
这种情况下，关闭图像变换（`PictureChange=0`）的计算可能是一个好的近似。
对于价壳层主导的性质——如电偶极矩和极化率——情况往往如此。
另一方面，涉及含电子-核距离负幂次算符的性质计算，
如果忽略图像变换效应，可能极不准确。因此强烈建议在所有（准）相对论
性质计算中打开图像变换！

对于 DKH2，完全一致的图像变换效应通过对性质算符使用与单电子哈密顿量
相同的变换阶数获得，即设置 `PictureChange=2`；而 `PictureChange=1`
只考虑性质算符的一阶变化，这会降低计算代价。然而，由于这无论如何
都算不上显著的降低，不推荐这一选择。

类似的论证适用于 X2C，其中 `PictureChange=2` 是形式上正确的做法，
`PictureChange=1` 是近似处理（见
{ref}`sec:essentialelements.relativistic.x2c.props`）。

默认情况下，ORCA 会根据所请求的性质尝试选择 `PictureChange` 变量
最合适的取值，如下所述（并在输出开始时发出警告），
但用户的显式输入始终被尊重。
- 对于 DKH 或 ZORA 的几何微扰，激活
  [单中心近似](sec:essentialelements.relativistic.hamiltonian.1c)，
  不需要图像变换校正。对于 X2C，选择 `PictureChange=1`，
  因为它显著降低计算代价。
- 对于其他性质，尤其是核心敏感的性质（即 EPR/NMR 中），
  应用完全的图像变换校正。
- 某些相对论哈密顿量与性质算符的组合并未实现，
  这种情况下 ORCA 会打印警告，或在图像变换效应预计很显著时
  干脆中止计算。

(sec:essentialelements.relativistic.finnuc)=
## 有限核模型（Finite Nucleus Model）

像原子核这样的复合粒子与基本粒子不同，具有一定的空间范围。
虽然原子核的点电荷近似在非相对论计算中通常非常好，
但在相对论计算中可能导致不可忽略的误差。ORCA 中实现了一个有限核模型
——参考文献 {cite}`visscher1997atom` 的 Gaussian 核模型——
在 ORCA 程序包中可用于 DKH 和 X2C（但不含 ZORA）计算。
它可通过 `%rel` 块访问

```orca
%rel FiniteNuc true end
```

默认情况下该关键词设为 `false`。若设为 `true`，
则在以下积分中考虑有限核效应：

- 核势 $V$ 及其核导数；
- DKH 和 X2C 中的相对论势积分 $V^{(p) }$；
- 自旋-轨道（SOC）积分的单电子部分；
- 电场梯度（EFG）；
- 接触密度积分；
- EPR 超精细耦合的 Fermi 接触（Fermi-contact）项和自旋-偶极
  （spin-dipole）项，以及 NMR 间接自旋-自旋耦合张量；
- 核-轨道耦合积分；
- 角动量积分；
- GIAO 上的 NMR 屏蔽积分。

(sec:essentialelements.relativistic.keywords)=
## 关键词

:::{raw} latex
\begingroup
\footnotesize
:::
(tab:essentialelements.relativistic.keywords.simple)=
:::{table} 相对论方法的简单输入关键词。
:class: footnotesize
| 关键词              | 说明                                                                                          |
|:--------------------|:----------------------------------------------------------------------------------------------|
| `DKH1`              | 激活一阶 DKH 哈密顿量                                                                         |
| `DKH2`, `DKH`       | 激活二阶 DKH 哈密顿量                                                                         |
| `ZORA`              | 激活 ZORA 哈密顿量                                                                            |
| `IORA`              | 激活 IORA 哈密顿量                                                                            |
| `X2C`               | 激活 X2C 哈密顿量                                                                             |
| `DLU-X2C`           | 在 DLU 近似下激活 X2C 哈密顿量                                                                |
| `RelDLU`            | 启用 [DLU 近似](sec:essentialelements.relativistic.x2c.dlu)（仅 X2C）                         |
| `Rel1C`             | 启用[单中心近似](sec:essentialelements.relativistic.hamiltonian.1c)                           |
| `RelFull`           | 关闭单中心和 DLU 近似                                                                         |
:::
:::{raw} latex
\endgroup
:::


:::{raw} latex
\begingroup
\footnotesize
:::
:::{tabularcolumns} \Y{0.2}\Y{0.3}\Y{0.5}
:::
(tab:essentialelements.relativistic.keywords.block)=
:::{flat-table} `%rel` 块相对论方法输入关键词。
:header-rows: 1
:class: longtable
:class: footnotesize
* - 关键词
  - 选项
  - 说明
* - {rspan}`3` `Method`
  - `DKH`
  - {rspan}`3`标量相对论哈密顿量
* - `ZORA`
* - `IORA`
* - `X2C`
* - `ModelPot`
  - `<VeN>, <VC>, <VXa>, <VLDA>, <VPC>`
  - 模型势的标志（1：包含，0：不包含）。
    `<VeN>`：核吸引；
    `<VC>`：Coulomb（仅 ZORA/IORA）；
    `<VXa>`：Xalpha（仅 ZORA/IORA）；
    `<VLDA>`：VWN-5 关联（仅 ZORA/IORA）；
    `<VPC>`：点电荷（仅 X2C）
* - {rspan}`2` `ModelDens`
  - `rhoDKH`
  - {rspan}`2` 用于 Coulomb 模型势和 PModel 初始猜测的拟合原子密度
* - `rhoZORA`
* - `rhoHF`
* - `OneCenter`
  - `false`
  - 若为 true，使用[单中心近似](sec:essentialelements.relativistic.hamiltonian.1c)
* - `C`
  - 137.0359895
  - 所用光速（原子单位）。同义词：`VELIT`、`VELOCITY`
* - `PictureChange`
  - 0, 1, 2
  - 性质的[图像变换](sec:essentialelements.relativistic.picturechange)。
    0：无；1：启用；2：完全（DKH/X2C）。默认：自动确定
* - `FiniteNuc`
  - `false`
  - 是否使用[有限核模型](sec:essentialelements.relativistic.finnuc)（DKH 或 X2C）
* - `PrintLevel`
  - 1
  - 打印多少与相对论相关的输出（0-4）。为 `%output Print[P_Rel]` 的别名
* - {cspan}`2` DKH 专用
* - `Order`
  - 2
  - DKH 哈密顿量的阶数（1 或 2）
* - `fpFWtrafo`
  - `true`
  - DKH 下 EPR 所用的 Foldy-Wouthuysen 变换类型
    （见 {numref}`sec:essentialelements.relativistic.dkh.magnetic`）。
    `true`：fpFW；`false`：fπFW
* - {cspan}`2` ZORA 专用
* - `Xalpha`
  - 0.7
  - Xalpha 势的默认值。仅当包含 VXa 时起作用
* - `ScaleZORA`
  - `false`
  - 是否标度轨道能量（仅单点）
* - {cspan}`2` X2C 专用
* - `DLU`
  - `false`
  - 若为 true，对 X2C 使用 [DLU 近似](sec:essentialelements.relativistic.x2c.dlu)
    （与 `OneCenter` 互斥）
* - `LightAtomThresh`
  - 0
  - 在 [DLU 近似](sec:essentialelements.relativistic.x2c.dlu)中
    被视为非相对论的最高原子序数
* - `StorageLevel`
  - 2
  - X2C 中间量存储级别（0–5）——
    见 {numref}`sec:essentialelements.relativistic.x2c.props`
:::
:::{raw} latex
\endgroup
:::
