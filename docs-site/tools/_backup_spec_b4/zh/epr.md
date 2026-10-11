

<a id="sec:spectroscopyproperties.epr"></a>
# 电子顺磁共振（EPR）参数（Electron Paramagnetic Resonance Parameters）

电子顺磁共振（electron paramagnetic resonance，EPR）探测电子基态的磁子能级。
在 `%eprnmr` 输入块中，可请求计算如下形式自旋哈密顿量的参数

$$

H_S = \beta_e \mathbf{B}\mathbf{g}\mathbf{S} + \sum_N\mathbf{S}\mathbf{A}_N\mathbf{I}_N
      + \mathbf{S}\mathbf{D}\mathbf{S}\qquad \text{(eq:epr_SH)}

$$

这些性质通过解析导数/响应理论方法评估。
关于基于 CC 的解析响应途径，请参阅
[sec:modelchemistries.autoci.autociresp](#sec:modelchemistries.autoci.autociresp)。
若想用准简并微扰理论评估自旋哈密顿量参数，
你可能会对 [sec:spectroscopyproperties.qdpt_magnetic_properties](#sec:spectroscopyproperties.qdpt_magnetic_properties) 感兴趣。
eprnmr 模块的完整关键词列表见
[sec:spectroscopyproperties.properties.eprnmr](#sec:spectroscopyproperties.properties.eprnmr)。
EPR 的笛卡尔指标约定见 [sec:spectroscopyproperties.properties.eprnmrConv](#sec:spectroscopyproperties.properties.eprnmrConv)。

<a id="sec:spectroscopyproperties.epr.g"></a>
## g 张量（The g-Tensor）

g 张量决定信号在 EPR 谱中的位置。
它可以作为能量的二阶导数计算，
ORCA 中对 SCF 方法（HF 和 DFT）、CASSCF、
全电子 MP2（或 RI-MP2）和双杂化 DFT
以及耦合簇（CCSD 和 CCSD(T)）均如此实现。

### 理论（Theory）

g 张量有四个贡献，可在 ORCA 中评估：

$$

\mathbf{g} = g_e\mathbf{1} + \mathbf{g}^{\text{RMC} }
              +\mathbf{g}^{\text{DSO} } + \mathbf{g}^{\text{PSO}}.\qquad \text{(eq:g_contrib)}

$$

这些贡献是：

- **自旋塞曼**（spin Zeeman）贡献，它是各向同性的，
  由一个简单常数——自由电子 g 值 $g_{e} = 2.002319\dots$ 表征

  $$

g_{\mu \nu }^{{ \text{SZ} } } =\delta_{\mu \nu } g_{e}\qquad \text{(eqn:249)}

$$

  这意味着它不需要任何计算。其余各项贡献于对自由电子值的偏离，
  有时称为 g 位移（g-shift）。

- 一阶**相对论质量修正**（relativistic mass correction），
  通常是一个相当小的标量相对论修正，
  可作为自旋密度上的期望值评估

  $$

\mathbf{g}^{ \text{RMC} } =-\frac{\alpha^{2} g_e}{2S}\sum\limits_{k,l}
  {P_{kl}^{\alpha -\beta } \left\langle { \phi_{k} \left|{ \hat{{T} }}
  \right|\phi_{l} } \right\rangle}.\qquad \text{(eqn:250)}

$$

- **抗磁自旋-轨道**（diamagnetic spin-orbit，也称规范校正）项，
  另一个一阶修正，通常也较小

  $$

g_{\mu \nu }^{ \text{DSO} } =\frac{\alpha^2 g_e}{4S}\sum\limits_{k,l}
  {P_{kl}^{\alpha -\beta } \left\langle { \phi_{k} \left|{ \sum\limits_A { \xi
  \left({ r_{A} } \right)\left[{ \mathrm{\mathbf{r} }_{A} \mathrm{\mathbf{r} }_{O} -\mathrm{\mathbf{r} }_{A,\mu } \mathrm{\mathbf{r} }_{O,\nu } } \right]} } \right|\phi_{l} }
  \right\rangle}.\qquad \text{(eqn:251)}

$$

- 二阶**轨道塞曼/SOC**贡献，通常是分子中偏离自由电子 g 值的主要来源，

  $$

g_{\mu \nu }^{ \text{PSO} } = - \frac{g_e}{2S}\sum\limits_{k,l} { \frac{\partial
  P_{kl}^{\alpha -\beta } }{\partial B_{\mu } }\left\langle { \phi_{k} \left|{h_{\nu }^{\text{SOC} } } \right|\phi_{l} } \right\rangle}.\qquad \text{(eqn:252)}

$$

  
  其计算需要求解响应方程以获得受微扰的自旋密度，
  ORCA 中对磁场微扰这样做。精确细节取决于理论水平。
  在 SCF 水平，通过求解耦合微扰 SCF 方程实现
  （参见 [sec:essentialelements.cpscf](#sec:essentialelements.cpscf)）。
  在 CASSCF 水平，则求解 CP-CASSCF 方程
  （[sec:spectroscopyproperties.casscfresp](#sec:spectroscopyproperties.casscfresp)）。

在这些方程中，$S$ 是总自旋，$\alpha$ 是精细结构常数，
$P^{\alpha -\beta }$ 是自旋密度矩阵，$\phi$ 是基组，
$\hat{T}$ 是动能算符，$\xi \left({ r_{A} } \right)$ 是近似径向算符，
$h^{\text{SOC} }$ 是有效单电子自旋-轨道算符的空间部分，
$B_{\mu }$ 是磁场的一个分量。

### 基本用法（Basic usage）

作为一个例子，考虑如下简单的 g 张量作业：

```orca
! BP86 Def2-SVP TightSCF g-tensor SOMF(1X)
* int 1 2
   O  0  0  0  0      0  0
   H  1  0  0  1.1056 0  0
   H  1  2  0  1.1056 109.62 0
*
```

最简单的方式如上所示在简单输入行中调用 g 张量性质。
也可在 `%eprnmr` 块中用 `gtensor true` 指定。
`SOMF(1X) ` 定义所选的自旋-轨道耦合（SOC）算符。

输出如下所示。它包含 g 张量各贡献
（相对论质量修正、抗磁自旋-轨道项（= 规范校正）、
顺磁自旋-轨道项（= OZ/SOC））、各向同性 g 值以及总张量取向的信息。

```orca
-------------------
ELECTRONIC G-MATRIX
-------------------

The g-matrix:
              2.0104321   -0.0031354   -0.0000000
             -0.0031354    2.0081968   -0.0000000
             -0.0000000   -0.0000000    2.0021275

Breakdown of the contributions
 gel          2.0023193    2.0023193    2.0023193
 gRMC        -0.0003174   -0.0003174   -0.0003174
 gDSO(tot)    0.0000808    0.0001539    0.0001515
 gPSO(tot)    0.0000449    0.0038301    0.0104898
             ----------   ----------   ----------
 g(tot)       2.0021275    2.0059858    2.0126431 iso=  2.0069188
 Delta-g     -0.0001917    0.0036665    0.0103238 iso=  0.0045995

 Orientation:
  X           0.0000000    0.5762906   -0.8172448
  Y           0.0000000    0.8172448    0.5762906
  Z           1.0000000   -0.0000000    0.0000000
```

SCF 水平的 g 张量计算对基组大小要求不高。
能给出可靠 SCF 结果的基组（至少价层双-zeta 加极化）
通常也能给出可靠的 g 张量结果。
对许多分子，Hartree-Fock 近似会给出合理的预测。
然而在若干情形下它会完全失效。
DFT 更稳健，失效的分子数目少得多。
在密度泛函中，杂化泛函似乎最准确。

!!! note
    程序中自旋-轨道耦合算符的处理有不同的可选方案。
    默认设置应当相当可靠。
    更多信息参见 [sec:spectroscopyproperties.soc](#sec:spectroscopyproperties.soc)。

<a id="sec:spectroscopyproperties.epr.gaugeorigin"></a>
### 规范原点处理（Gauge origin treatment）

g 张量不是规范无关的。
若不采取特殊预防措施，结果将非物理地依赖于规范原点相对于分子的放置位置。
除非使用完全不变的程序（如 GIAO），
否则计算中总会存在这一不理想的方面。

从 ORCA 5.0 开始，g 张量计算的默认规范处理是 **GIAO** 途径
（GIAO 代表"gauge including atomic orbitals"，规范包含原子轨道）。
GIAO 在 SCF 水平、RI-MP2 以及直到 CCSD(T) 水平的耦合簇中可用。
GIAO 目前***不***可用于 CASSCF 线性响应，
且必须在 `%eprnmr` 块中提供一个公共规范原点。

| EPR g 张量所用方法                                          |GIAO   |CGO    |
|--------------------------------------------------------|-------|-------|
| [SCF](sec:essentialelements.cpscf)                     |&check;|&check;|
| [RI-MP2](sec:modelchemistries.mp2.2ndder)              |&check;|&check;|
| [CASSCF](sec:spectroscopyproperties.casscfresp)        |       |&check;|
| [CCSD, CCSD(T)](sec:modelchemistries.autoci.autociresp)|&check;|       |

GIAO 单电子积分默认解析计算，
而 GIAO 双电子积分的处理选择与 SCF 相同。
可在 `%eprnmr` 块中用 `giao_1el / giao_2el` 设置的可选方案见
[sec:spectroscopyproperties.properties.eprnmr](#sec:spectroscopyproperties.properties.eprnmr) 一节。
关于计算时间，对于小体系（如苯基自由基，41 个电子），
`rijk` 近似对 SCF 过程和 GIAO 双电子积分都适用。
对于更大的体系（如叶绿素自由基，473 个电子），
`rijcosx` 近似能极大地缩短计算时间。
虽然 ORCA 5.0 中新的默认网格设置（`defgrid2`）在多数情况下足够，
但某些情形可能需要使用 `defgrid3`。
请注意，对于 CC-NMR/EPR 的当前实现，
`giao_1el` 和 `giao_2el` 都需要完全解析评估，
当请求 CC-NMR/EPR 时这也是默认。

若规范原点的选择不是极其糟糕，**公共规范原点**
通常能给出合理的 g 张量结果（比 NMR 中合理得多——NMR 中不应使用）。
在使用大基组时尤其如此。
原点可用 `%eprnmr` 输入块内的关键词 `ori` 修改。
若你使用公共规范原点，
明智的做法是检查结果对原点位置的敏感性，
特别是在只计算几百 ppm 量级的小 g 位移时。

### 关键词（Keywords）

<a id="tab:spectroscopyproperties.epr.g.keywords.block"></a>
!!! note "与 g 张量计算相关的 `%eprnmr` 块输入关键词。更多 GIAO 相关选项见 [sec:spectroscopyproperties.properties.eprnmr](#sec:spectroscopyproperties.properties.eprnmr)"
    :header-rows: 1
    :class: longtable
    :class: footnotesize

| 项目 | 内容 |
| --- | --- |
| **关键词** | 无 |

      - 选项
      - 说明

| 项目 | 内容 |
| --- | --- |
| **`gtensor`** | 无 |

      - `true/false`
      - 计算 g 张量

| 项目 | 内容 |
| --- | --- |
| **`gtensor_1el2el`** | 无 |

      - `true/false`
      - 打印 g 张量的单电子和双电子贡献

| 项目 | 内容 |
| --- | --- |
| **`ori`** | 无 |

      - `GIAO`
      - 使用 GIAO 形式（默认）

| 项目 | 内容 |
| --- | --- |
| **—** | 无 |

      - `CenterOfElCharge`
      - 公共规范原点在电子电荷中心

| 项目 | 内容 |
| --- | --- |
| **—** | 无 |

      - `CenterOfNucCharge`
      - 公共规范原点在核电荷中心

| 项目 | 内容 |
| --- | --- |
| **—** | 无 |

      - `CenterOfSpinDens`
      - 公共规范原点在自旋密度中心

| 项目 | 内容 |
| --- | --- |
| **—** | 无 |

      - `CenterOfMass`
      - 公共规范原点在质心

| 项目 | 内容 |
| --- | --- |
| **—** | 无 |

      - `N`
      - 公共规范原点在原子 `N`

| 项目 | 内容 |
| --- | --- |
| **—** | 无 |

      - `x, y, z`
      - 公共规范原点在位置 `x, y, z`（坐标输入单位，默认埃）

| 项目 | 内容 |
| --- | --- |
| **`do_giao_soc2el`** | 无 |

      - `true/false`
      - 是否包含 SOMF 算符对 GIAO 项的双电子贡献（通常很小但昂贵，默认关闭）

<a id="sec:spectroscopyproperties.epr.hyperfine"></a>
## 超精细耦合（Hyperfine Coupling）

超精细耦合表征分子中电子自旋与核自旋之间的相互作用。
在典型 EPR 谱中，它们导致信号的劈裂。

<a id="sec:spectroscopyproperties.epr.hyperfine.contrib"></a>
### 理论（Theory）
超精细耦合有四个贡献，可在 ORCA 中评估：

$$

\mathbf{A}_N = a_{iso}\mathbf{1} + \mathbf{A}^{\text{dip} }
              +\mathbf{A}^{\text{orb} } + \mathbf{A}^{\text{GC}}.\qquad \text{(eq:A_contrib)}

$$

这些贡献是：

- 各向同性**费米接触**（Fermi contact）项，
  源于所考察核上的有限自旋密度。
  对核 $N$ 它由下式计算：

  $$

a_{\text{iso} } \left( N \right)=\left( \frac{4}{3}\pi
  \left\langle { S_{z} } \right\rangle^{-1} \right)g_{e} g_{N} \beta_{e}
  \beta_{N} \rho \left({ \vec{{R} }_{N} } \right)\qquad \text{(eqn:244)}

$$

  其中 $\left\langle { S_{z} } \right\rangle$ 是总自旋 z 分量的期望值，
  $g_{e}$ 和 $g_{N}$ 是电子和核 g 因子，
  $\beta_{e}$ 和 $\beta_{N}$ 分别是电子和核磁子。
  $\rho \left({ \vec{{R} }_{N} } \right)$ 是核处的自旋密度。
  比例因子 $P_{N} = \alpha^2 g_{e} g_{N} \beta_{e} \beta_{N}$ 常被使用，
  在 ORCA 中其量纲为 MHz bohr$^{3}$。

- **自旋偶极**（spin dipole）项，
  源于磁核与电子磁矩之间的空间偶极-偶极相互作用。
  它也作为自旋密度上的期望值计算：

  $$

A_{\mu \nu}^{\text{dip} } \left( N \right) =
  P_N \sum\limits_{kl} \rho_{kl}
  \left\langle\phi_k \left| r_N^{-5} \left(3\vec{r}_{N \mu}\vec{r}_{N \nu}
  -\delta_{\mu \nu}r_N^2 \right)\right|\phi_l \right\rangle\qquad \text{(eqn:245)}

$$

  其中 $\mathrm{\mathbf{\rho } }$ 是自旋密度矩阵，
  $\vec{{r} }_{N}$ 是大小为 $r_{N}$、
  从所考察核指向电子的矢量（$\left\{\phi \right\}$ 是基函数集合）。

- 二阶**自旋-轨道**贡献，
  作为自旋-轨道与核-轨道耦合算符之间的交叉项出现。
  它需要求解耦合微扰 SCF 方程，因而计算量更大。
  该贡献可写为：

  $$

A_{\mu \nu }^{\text{orb} } \left( N \right)=-\frac{1}{2S}P_{N} \sum\limits_{kl}
  {\frac{\partial \rho_{kl} }{\partial I_{\nu } }\left\langle { \phi_{k}
  \left|{ h_{\mu }^{\text{SOC} } } \right|\phi_{l} } \right\rangle}\qquad \text{(eqn:246)}

$$

  自旋密度的导数通过求解
  相对于核-轨道耦合微扰的耦合微扰 SCF 方程计算，
  该微扰由算符表示

  $$

h_{\nu }^{\text{NOC} } \left( N \right)=\sum\limits_i { r_{iA}^{-3} l_{i,\nu
  }^{\left( N \right)} }\qquad \text{(eqn:247)}

$$

  其中求和遍历电子，$N$ 是所考察的核。

- **规范校正**（gauge-correction）贡献（有时也称抗磁项）。
  该项通常很小。然而，为获得完全规范不变的结果它是必需的。
  我们最近证明，在核自旋与电子自旋的长程极限下，
  规范校正可能变得至关重要。
  这与赝接触 NMR 化学位移（PCS）相关。[LangPCS](../../bibliography.md)

!!! note
    对较重的核，二阶 HFC 可能相当显著，
    对过渡金属配合物当然值得包含。
    自旋-轨道耦合算符的可用处理见 [sec:spectroscopyproperties.soc](#sec:spectroscopyproperties.soc)。

### 基本用法（Basic usage）
超精细耦合和四极耦合可在 `%eprnmr` 输入块中请求。
由于你可能关注多个核，输入相对复杂。

下面是计算 CN 自由基的超精细张量和场梯度张量的示例：

```orca
-------------------
ELECTRONIC G-MATRIX
-------------------

The g-matrix:
              2.0104321   -0.0031354   -0.0000000
             -0.0031354    2.0081968   -0.0000000
             -0.0000000   -0.0000000    2.0021275

Breakdown of the contributions
 gel          2.0023193    2.0023193    2.0023193
 gRMC        -0.0003174   -0.0003174   -0.0003174
 gDSO(tot)    0.0000808    0.0001539    0.0001515
 gPSO(tot)    0.0000449    0.0038301    0.0104898
             ----------   ----------   ----------
 g(tot)       2.0021275    2.0059858    2.0126431 iso=  2.0069188
 Delta-g     -0.0001917    0.0036665    0.0103238 iso=  0.0045995

 Orientation:
  X           0.0000000    0.5762906   -0.8172448
  Y           0.0000000    0.8172448    0.5762906
  Z           1.0000000   -0.0000000    0.0000000
```

在本例中，对所有碳原子和原子 2（此处为氮）计算超精细张量。
（此外，对氮计算电场梯度。）

!!! note
    -   原子编号从 1 开始计数。

    -   注意——写在同一行上的所有核都将被赋予相同的同位素质量！
        若需要几个不同的核（如 C 和 H），
        必须为每一个各写一行。

    -   你必须在原子坐标定义*之后*指定 `Nuclei` 语句，
        否则程序无法确定 "`all`" 指的是什么。

输出如下所示。它包含超精细耦合各贡献的详细信息、
其取向、本征值、各向同性部分，
以及（若请求了）四极耦合张量。

```orca
-----------------------------------------
ELECTRIC AND MAGNETIC HYPERFINE STRUCTURE
-----------------------------------------

 -----------------------------------------------------------
 Nucleus   0C : A:ISTP=   13 I=  0.5 P=134.1903 MHz.au**3
                Q:ISTP=   13 I=  0.5 Q=  0.0000 barn
 -----------------------------------------------------------
 Raw HFC matrix (all values in MHz):
 -----------------------------------
               695.8952           0.0000          -0.0000
                 0.0000         543.0617          -0.0000
                -0.0000          -0.0000         543.0617

 A(FC)         594.0062         594.0062         594.0062
 A(SD)         -50.9445         -50.9445         101.8890
             ----------       ----------       ----------
 A(Tot)        543.0617         543.0617         695.8952  A(iso)=594.0062
 Orientation:
  X           0.0000000        0.0000000       -1.0000000
  Y          -0.8111216       -0.5848776       -0.0000000
  Z          -0.5848776        0.8111216        0.0000000

Notes:  (1) The A matrix conforms to the "SAI" spin Hamiltonian convention.
        (2) Tensor is right-handed.

 -----------------------------------------------------------
 Nucleus   1N : A:ISTP=   14 I=  1.0 P= 38.5677 MHz.au**3
                Q:ISTP=   14 I=  1.0 Q=  0.0204 barn
 -----------------------------------------------------------
 Raw HFC matrix (all values in MHz):
 -----------------------------------
                13.2095         -0.0000          0.0000
                -0.0000        -45.6036         -0.0000
                 0.0000         -0.0000        -45.6036

 A(FC)         -25.9993        -25.9993        -25.9993
 A(SD)          39.2088        -19.6044        -19.6044
             ----------      ----------      ----------
 A(Tot)         13.2095        -45.6036        -45.6036  A(iso)=-25.9993
 Orientation:
  X           1.0000000       0.0000000      -0.0000000
  Y          -0.0000000       0.9996462       0.0265986
  Z           0.0000000      -0.0265986       0.9996462

Notes:  (1) The A matrix conforms to the "SAI" spin Hamiltonian convention.
        (2) Tensor is right-handed.

 Raw EFG matrix (all values in a.u.**-3):
 -----------------------------------
            -0.1832      -0.0000       0.0000
            -0.0000       0.0916       0.0000
             0.0000       0.0000       0.0916

 V(El)       0.6468       0.6468      -1.2935
 V(Nuc)     -0.5551      -0.5551       1.1103
         ----------   ----------   ----------
 V(Tot)      0.0916       0.0916      -0.1832
 Orientation:
  X      -0.0000003    0.0000002    1.0000000
  Y       0.9878165    0.1556229    0.0000003
  Z      -0.1556229    0.9878165   -0.0000002

Note: Tensor is right-handed

 Quadrupole tensor eigenvalues (in MHz;Q= 0.0204 I=  1.0)
  e**2qQ            =    -0.880 MHz
  e**2qQ/(4I*(2I-1))=    -0.220 MHz
  eta               =     0.000
  NOTE: the diagonal representation of the SH term
  I*Q*I = e**2qQ/(4I(2I-1))*[-(1-eta),-(1+eta),2]
```

若在同一作业中也进行了 EPR g 张量或 D 张量计算（见下一节），
ORCA 会自动打印超精细/四极耦合与分子 g 或 D 张量之间的取向关系。
更多信息参见 [sec:utilities.euler](#sec:utilities.euler) 一节。

!!! note
    对于重核，你可能需要考虑相对论效应的可能性。
    标量相对论效应可用 ORCA 中的若干准相对论哈密顿量处理。
    各种可能性的概述和一些推荐见
    [sec:essentialelements.relativistic](#sec:essentialelements.relativistic)。
    请注意，相对论计算可能对基组有特殊要求。
    在相对论性质计算中，你应当注意绘景变换（picture change）校正的重要性
    （参见 [sec:essentialelements.relativistic.picturechange](#sec:essentialelements.relativistic.picturechange)）。
    在用 DFT 的准相对论计算中，对数值积分的精度也应非常谨慎，
    尤其是对较重的（过渡金属）核。

!!! note
    用 DLPNO-CCSD 计算 HFCC 时，建议在简单关键词行使用
    定制的截断设置 `!DLPNO-HFC1` 或 `!DLPNO-HFC2`，
    它们对应于文献 [saitow2018dlpnohfc](../../bibliography.md) 中的
    "Default1" 和 "Default2" 设置。

若你希望提取多核过渡金属配合物的 *A* 张量，
输出中的 `A(iso)` 值可按文献 [Pantazis2009ChemEurJ](../../bibliography.md)
所述的方法处理。

### 关于基组的说明（A note on basis sets）

对于超精细（和四极）耦合，
为能量和几何优化设计的标准基组往往不令人满意
（尤其是对比 Ne 重的原子）。
你应当寻找能描述核附近电子结构的基组。
一种选择是使用针对"芯层性质"计算定制的基组。
以下是不错的选择：

-   Barone 及其同事的 `EPR-II` 基组：它只对少数轻原子
    （H、B、C、N、O、F）可用，
    本质上是双-zeta 加极化质量，在芯区增加了灵活性，
    应能给出合理的结果。

-   Kutzelnigg 及其同事的 `IGLO-II` 和 `IGLO-III` 基组：
    它们相当准确，但也只对部分第一、二周期元素可用。

-   CP 基组：它们对第一过渡系金属也准确。

-   未收缩的 Partridge 基组：它们是通用的 HF 极限基组，
    用于常规计算可能过于昂贵，但对校准目的非常有用。

-   Jensen 为超精细耦合计算定制的 `pcH` 基组，同样可用范围有限
    （参见 [sec:essentialelements.basisset.builtin.jensen](#sec:essentialelements.basisset.builtin.jensen)）。

若 ORCA 尚无你所用元素的专用基组，
你很可能需要按需定制基组。
你可以通过手动添加大指数的 s 型原函数，
或通过去收缩基组的芯层部分来实现
（去收缩功能的说明见 [sec:essentialelements.basisset](#sec:essentialelements.basisset)）。
你可以先检查已有的基组——
若在 `%output` 块中加入语句 `Print[p_basis] 2`
（或在简单输入行中用 `PrintBasis`），
程序会以输入格式打印基组（用于 basis 块）。
然后你可以添加或删除原函数、去收缩芯层函数等。
例如，下面是碳基组 DZP 以输入格式的打印：

```orca
# Basis set for element : C
  NewGTO 6
  s 5
   1  3623.8613000000      0.0022633312
   2   544.0462100000      0.0173452633
   3   123.7433800000      0.0860412011
   4    34.7632090000      0.3022227208
   5    10.9333330000      0.6898436475
  s 1
   1     3.5744765000      1.0000000000
  s 1
    1    0.5748324500      1.0000000000
  s 1
    1    0.1730364000      1.0000000000
  p 3
    1    9.4432819000      0.0570590790
    2    2.0017986000      0.3134587330
    3    0.5462971800      0.7599881644
  p 1
    1    0.1520268400      1.0000000000
  d 1
    1    0.8000000000      1.0000000000
  end;
```

阅读这些信息相对直接。
例如："`s 5`" 表示第一个基函数的角动量和原函数数目。
随后五行则包含该函数中原函数的编号、指数和（未归一化的）收缩系数。

**请记住，若你添加非常陡的函数，
当计算使用 DFT 时，你*必须*增大积分网格！
否则结果将不准确。**
在一定程度上，程序现在检测到陡函数时会自动调整网格。
若你还需要提高积分精度，
可以在 `Method` 块中增大 `IntAcc` 来全局提高径向网格大小，
或只对个别原子提高积分精度，后者代价更低。
更多细节见 [sec:essentialelements.numericalintegration.detailsandoptions](#sec:essentialelements.numericalintegration.detailsandoptions) 一节。
在当前例子中，芯区更大基组和更精确积分所引起的变化相对温和——约 3%。
不过，若你有点完美主义，这仍然显著。

### 超精细耦合关键词（Hyperfine Coupling Keywords）

!!! note
    写在同一行上的所有核都将被赋予相同的同位素质量（以及其他参数）！

<a id="tab:spectroscopyproperties.epr.hyperfine.keywords.block"></a>
!!! note "与 HFC 计算相关的 `%eprnmr` 块输入关键词"
    :class: footnotesize
    | 关键词          | 选择              | 执行动作          | 说明                                       |
    |:----------------|:------------------|:------------------|:-------------------------------------------------|
    | `nuclei`        | `all <type>`      |                   | 选择元素 `<type>` 的所有核            |
    |                 | `i1,i2,i3...`     |                   | 选择原子 `i1`、`i2`、`i3`……（从 1 开始！） |
    |                 |                   | `{ aiso  }`       | 计算各向同性费米接触贡献 |                   
    |                 |                   | `{ adip  }`       | 计算自旋偶极贡献          |                   
    |                 |                   | `{ aorb  }`       | 计算自旋-轨道贡献           |                   
    |                 |                   | `{ ist=<N> }`       | 为所选对象选择同位素 `<N>`                |
    |                 |                   | `{ PPP=<N> }`       | 将所选对象的 HFC 比例因子 $\alpha^2 g_e g_N \beta_E \beta_N$ 设为 `<N>`    |
    |                 |                   | `{ III=<N> }`       | 将所选对象的核自旋设为 `<N>`         |
    |                 |                   | `{ aiso, adip, aorb }`  | 为所选对象请求多个动作的示例                 |

<a id="tab:spectroscopyproperties.epr.tweaks"></a>
!!! note "`%eprnmr` 块中抗磁规范校正的可能微调选项。除非你有特殊理由，否则不太可能需要使用这些设置。"
    :header-rows: 1
    :class: longtable
    :class: footnotesize

| 项目 | 内容 |
| --- | --- |
| **关键词** | 无 |

      - 选项
      - 说明

| 项目 | 内容 |
| --- | --- |
| **`hfcgaugecorrection_zeff`** | 无 |

      - `true/false`
      - 规范校正使用有效核电荷

| 项目 | 内容 |
| --- | --- |
| **`hfcgaugecorrection_numeric`** | 无 |

      - `true/false`
      - 数值计算 DSO 积分（更快）

| 项目 | 内容 |
| --- | --- |
| **`hfcgaugecorrection_angulargrid`** | 无 |

      - `-1`
      - < 0 表示使用 DFT 网格设置

| 项目 | 内容 |
| --- | --- |
| **`hfcgaugecorrection_intacc`** | 无 |

      - `-1`
      - < 0 表示使用 DFT 网格设置

| 项目 | 内容 |
| --- | --- |
| **`hfcgaugecorrection_prunegrid`** | 无 |

      - `-1`
      - < 0 表示使用 DFT 网格设置

| 项目 | 内容 |
| --- | --- |
| **`hfcgaugecorrection_bfcutoff`** | 无 |

      - `-1`
      - < 0 表示使用 DFT 网格设置

| 项目 | 内容 |
| --- | --- |
| **`hfcgaugecorrection_wcutoff`** | 无 |

      - `-1`
      - < 0 表示使用 DFT 网格设置

<a id="sec:spectroscopyproperties.epr.D"></a>
## 零场分裂（Zero-Field Splitting）

零场分裂（zero-field splitting，ZFS）通常是总基态自旋 $S$>1/2 的
过渡金属配合物自旋哈密顿量（SH）中的主导项
（综述和参考文献见 [sec:appendix.publications](#sec:appendix.publications) 一章）。
它的作用是引入 $2S+1$ 个 $M_{S}$ 子能级的劈裂，
这些子能级在 Born-Oppenheimer 哈密顿量水平上是严格简并的，
即使在没有外磁场时也是如此。

### 理论（Theory）

零场分裂有两个重要贡献 [harriman1978ESR](../../bibliography.md)：

- 来自直接**自旋-自旋**相互作用的一阶项

  $$

D_{KL}^{ \text{SS} } =\frac{1}{2}\frac{\alpha^{2} }{S\left({ 2S-1}
  \right)}\left\langle { 0SS\left|{ \sum\limits_i { \sum\limits_{j\ne i}
  {\frac{r_{ij}^{2} \delta_{KL} -3\left({ \mathrm{\mathbf{r} }_{ij} } \right)_{K}
  \left({ \mathrm{\mathbf{r} }_{ij} } \right)_{L} }{r_{ij}^{5} }\left\{{2\hat{{s} }_{zi} \hat{{s} }_{zj} -\hat{{s} }_{xi} \hat{{s} }_{xj}
  -\hat{{s} }_{yi} \hat{{s} }_{yj} } \right\}} } } \right|0SS} \right\rangle\qquad \text{(eqn:253)}

$$

  其中 $K$,$L=$x,y,z，$\alpha$ 是精细结构常数
  （原子单位下 $\approx$ 1/137），
  $\mathrm{\mathbf{r} }_{ij}$ 是大小为 $r_{ij}$ 的电子间距离矢量，
  $\hat{{s} }_{i}$ 是第 $i$ 个电子的自旋矢量算符。
  $\left|0SS \right\rangle$ 是总自旋 $S$、
  投影量子数 $M_{S} = S$ 的 Born-Oppenheimer
  哈密顿量的精确基态本征函数。
  由于自旋-自旋相互作用是一阶的，其评估没有特别的困难。

- 二阶**自旋-轨道**贡献，它复杂得多。
  在自旋-轨道耦合（SOC）算符可较好地近似为有效单电子算符
  （$\hat{{H} }_{\text{SOC} } =\sum\nolimits_i { \mathrm{\mathbf{\hat{{h} }} }_{i}^{\text{SOC} } { \mathrm{\mathbf{\hat{s} }} }_{i} } )$ 的假设下，
  文献 [neese1998inorgchem](../../bibliography.md) 推导了 SOC 对 ZFS 张量贡献的
  如下态求和（sum-over-states，SOS）方程：

  $$

D_{KL}^{\text{SOC}-\left( 0 \right)} =-\frac{1}{S^{2} }\sum\limits_{b\left({ S_{b}
  =S} \right)} { \Delta_{b}^{-1} \left\langle { 0^{SS}\left|{ \sum\limits_i
  {\hat{{h} }_{i}^{K;\text{SOC} } \hat{{s} }_{i,0} } } \right|b^{SS} } \right\rangle\left\langle { b^{SS}\left|{ \sum\limits_i { \hat{{h} }_{i}^{L;\text{SOC} }
  \hat{{s} }_{i,0} } } \right|0^{SS} } \right\rangle}\qquad \text{(eqn:254)}

$$

  $$

D_{KL}^{\text{SOC}-\left({ -1} \right)} =-\frac{1}{S\left({ 2S-1}
  \right)}\sum\limits_{b\left({ S_{b} =S-1} \right)} { \Delta_{b}^{-1}
  \left\langle { 0^{SS}\left|{ \sum\limits_i { \hat{{h} }_{i}^{K;\text{SOC} }
  \hat{{s} }_{i,+1} } } \right|b^{S-1S-1} } \right\rangle\left\langle {b^{S-1S-1}\left|{ \sum\limits_i { \hat{{h} }_{i}^{L;\text{SOC} } \hat{{s} }_{i,-1} } }
  \right|0^{SS} } \right\rangle}\qquad \text{(eqn:255)}

$$

  $$

\begin{array}{l}
  D_{KL}^{\text{SOC}-\left({ +1} \right)} =-\frac{1}{\left({ S+1} \right)\left({2S+1} \right)} \cdot \\
  \hspace{2cm}
  \sum\limits_{b\left({ S_{b} =S+1} \right)} { \Delta_{b}^{-1}
  \left\langle { 0^{SS}\left|{ \sum\limits_i { \hat{{h} }_{i}^{K;\text{SOC} }
  \hat{{s} }_{i,-1} } } \right|b^{S+1S+1} } \right\rangle\left\langle {b^{S+1S+1}\left|{ \sum\limits_i { \hat{{h} }_{i}^{L;\text{SOC} } \hat{{s} }_{i,+1} } }
  \right|0^{SS} } \right\rangle}
  \end{array}\qquad \text{(eqn:256)}

$$

  这里电子 $i$ 的单电子自旋算符已用球矢量算符分量
  $s_{i,m}$（$m=0,\pm 1$）写出，
  $\Delta_{b} =E_{b} -E_{0}$ 是到激发多重态
  $\left| b^{SS} \right\rangle$ 的激发能
  （在 BO 哈密顿量水平上所有 $M_{S}$ 分量都是简并的）。

!!! note
    二阶自旋-轨道项可在波函数理论方法的框架内用上述态求和公式评估。
    下一节聚焦于基于 SCF 解析导数/响应理论的表述。
    你也可能对 QDPT 感兴趣，它在零场分裂很大的体系中尤其可靠。

!!! note
    自旋-轨道耦合算符的可用处理见 [sec:spectroscopyproperties.soc](#sec:spectroscopyproperties.soc)。

### 基本用法（Basic usage）

例如，考虑如下假想 Mn(III) 配合物的作业。

```orca
! PBE0 def2-MSVP TightSCF
* int 0 2
   C  0  0  0  0     0  0
   N  1  0  0  1.170 0  0
*
%eprnmr  Nuclei = all C { aiso, adip }
         Nuclei = 2 { aiso, adip, fgrad }
         end
```

输出记录了 D 张量的各个贡献，
其中也包含（与 g 张量不同）自旋翻转项的贡献。

!!! note
    SOC 贡献有四种不同的变体，这本身就说明这是一个困难的性质。可选项有：

    -   QRO 方法有完整文献记载 [neese2006am](../../bibliography.md)，
        基于更早发展的理论。[neese1998inorgchem](../../bibliography.md)
        QRO 方法合理但略显简单，已被下文描述的 CP 方法取代。

    -   Pederson-Khanna 模型于 1999 年基于定性论证提出。[pedersonkhanna1999gtensor-zfs](../../bibliography.md)
        它的自旋翻转项也含有不正确的前置因子。
        不过我们仍实现了该方法以便比较。
        在原始形式中它只对局域泛函有效。
        在 ORCA 中它被扩展到杂化泛函和 HF。

    -   默认的耦合微扰方法是 ZFS 的 DFT 方法的推广；
        它对自旋翻转项使用修正的前置因子，
        并为 SOC 微扰求解一组耦合微扰方程。
        因此它对杂化泛函有效。已有详细描述。[Neese2007zfs](../../bibliography.md)

ORCA 中的当前实现适用于 HF、DFT 和杂化 DFT。

DSS 部分是一个涉及体系自旋密度的期望值。
在详细的校准工作 [sinnecker2006](../../bibliography.md) 中发现，
自旋非限制 DFT 方法表现得有些不稳定，
而开壳层自旋限制 DFT 能得到准确得多的数值。
因此 "UNO" 选项允许用从单占据非限制自然轨道
获得的限制性自旋密度计算 SS 项。

对于 UKS/UHF 波函数和正则轨道，DSS 部分含有一项不稳定自相互作用项。
因此，对这类计算推荐使用 `UNO`。[riplinger2009epr](../../bibliography.md)
若仍使用 `DIRECT` 选项，ORCA 会在输出的相应部分打印警告。

!!! note
    若用关联波函数方法（如 (DLPNO-/LPNO-)CCSD）计算 D 张量，
    不应使用 `DSS=UNO` 选项。

<a id="sec:spectroscopyproperties.epr.D.detail"></a>
### 耦合微扰表述的详细理论（Detailed theory of the coupled-perturbed formulation）

2007 年，我们发展了一种使 ZFS 计算与解析导数语言相容的程序。[Neese2007zfs](../../bibliography.md)
也许最清晰的途径是从 Born-Oppenheimer 哈密顿量的精确解出发。
为此，我们考察基态能量
（$E=\left\langle { 0^{SS}\left|{\hat{{H} }} \right|0^{SS} } \right\rangle)$
对如下一般形式的自旋相关单电子算符的二阶导数：

$$

\hat{{h} }^{K;\left( m \right)}=x_{K}^{\left( m \right)} \sum\limits_{pq}
{h_{pq}^{K} \hat{{S} }_{pq}^{\left( m \right)} }\qquad \text{(eqn:260)}

$$

其中 $h_{pq}^{K}$ 是算符空间部分第 $K$ 个分量的矩阵
（假定为虚厄米，如 SOC 算符的空间分量那样），
$\hat{{S} }_{pq}^{\left( m \right)}$ 是自旋矢量算符的二次量子化形式
（$m=0,\pm 1$）。
量 $x_{K}^{\left( m \right)}$ 是一个形式上的微扰参数。
利用 BO 算符的精确本征函数，一阶导数为：

$$

\left.{ \frac{\partial E}{\partial x_{K}^{\left( m \right)} } }
\right|_{x_{K}^{\left( m \right)} =0} =\sum\limits_{pq} { h_{pq}^{K}
P_{pq}^{\left( m \right)} }\qquad \text{(eqn:261)}

$$

其中自旋密度的分量为：

$$

P_{pq}^{\left( m \right)} =\left\langle { 0^{SS}\vert \hat{{S} }_{pq}^{\left(m \right)} \vert 0^{SS} } \right\rangle\qquad \text{(eqn:262)}

$$

对第二个分量（$m'=-m$）的二阶导数为：

$$

\left.{ \frac{\partial^{2}E}{\partial x_{K}^{\left( m \right)} \partial
x_{L}^{\left({ -m} \right)} } } \right|_{x_{K}^{\left( m \right)}
=x_{L}^{\left({ -m} \right)} =0} =\sum\limits_{pq} { h_{pq}^{K}
\frac{\partial P_{pq}^{\left( m \right)} }{x_{L}^{\left({ -m} \right)} } }\qquad \text{(eqn:263)}

$$

自旋密度的导数可写为：

$$

\frac{\partial P_{pq}^{\left( m \right)} }{x_{L}^{\left({ -m} \right)}
}=\left\langle { 0_{L}^{SS\left({ -m} \right)} \vert \hat{{S} }_{pq}^{\left( m
\right)} \vert 0^{SS} } \right\rangle+\left\langle { 0^{SS}\vert
\hat{{S} }_{pq}^{\left( m \right)} \vert 0_{L}^{SS\left({ -m} \right)} }
\right\rangle\qquad \text{(eqn:264)}

$$

将受微扰波函数按未微扰态展开，一阶为：

$$

\left| 0_L^{SS\left(-m\right)}\right\rangle=
-\sum\limits{n \ne 0} \Delta_n^{-1} \left| n \right \rangle \left\langle n \left| \hat{h}^
{L;\left(-m\right)} \right| 0^{SS} \right \rangle\qquad \text{(eqn:265)}

$$

其中 $\left| n \right\rangle$ 是任一 $\left| b^{S'M'} \right\rangle$。
于是得到：

$$

\frac{\partial^{2}E}{\partial x_{K}^{\left( m \right)} \partial
x_{L}^{\left({ -m} \right)} }=\sum\limits_{pq} { h_{pq}^{K} \frac{\partial
P_{pq}^{\left( m \right)} }{x_{L}^{\left({ -m} \right)} } }\qquad \text{(eqn:266)}

$$

$$

\hspace{2cm}
=-\sum\limits_{n\ne 0} { \Delta
_{n}^{-1} \left[{ \left\langle { 0^{SS}\vert \hat{{h} }^{L;\left({ -m}
\right)}\vert n} \right\rangle\left\langle { n\vert \hat{{h} }^{K;\left( m
\right)}\vert 0^{SS} } \right\rangle+\left\langle { 0^{SS}\vert
\hat{{h} }^{K;\left( m \right)}\vert n} \right\rangle\left\langle { n\vert
\hat{{h} }^{L;\left({ -m} \right)}\vert 0^{SS} } \right\rangle} \right]}\qquad \text{(eqn:267)}

$$

该等式对精确态成立。
对于近似的电子结构处理，解析导数途径更有吸引力，
因为无穷态求和在实践中永远无法完成，
而且解析导数的计算比计算激发多电子态的计算量小。

利用式 [Eq](#eqn:266)，SOC 对 **D**-张量贡献的分量被重新表述为

$$

D_{KL}^{\text{SOC}-\left( 0 \right)} =\frac{1}{2S^{2} }\sum\limits_{pq}
{h_{pq}^{K;\text{SOC} } \frac{\partial P_{pq}^{\left( 0 \right)} }{\partial
x_{L}^{\left( 0 \right)} } }\qquad \text{(eqn:268)}

$$

$$

D_{KL}^{\text{SOC}-\left({ -1} \right)} =\frac{1}{S\left({ 2S-1}
\right)}\sum\limits_{pq} { h_{pq}^{K;\text{SOC} } \frac{\partial P_{pq}^{\left({ +1}
\right)} }{\partial x_{L}^{\left({ -1} \right)} } }\qquad \text{(eqn:269)}

$$

$$

D_{KL}^{\text{SOC}-\left({ +1} \right)} =\frac{1}{\left({ S+1} \right)\left({ 2S+1}
\right)}\sum\limits_{pq} { h_{pq}^{K;\text{SOC} } \frac{\partial P_{pq}^{\left({ -1}
\right)} }{\partial x_{L}^{\left({ +1} \right)} } }\qquad \text{(eqn:270)}

$$

这些是通用方程，可与任何能写成二次量子化形式的
非相对论或标量相对论电子结构方法一起使用。
下面，该形式被应用于自洽场（HF、DFT）参考态的情形。

对于 DFT 或 HF 基态，方程进一步发展如下：

SCF 能量为：

$$

E_{\text{SCF} } =V_{\text{NN} } +\left\langle { \mathrm{\mathbf{Ph} }^{+} } \right\rangle+\frac{1}{2}\int{ \int{ \frac{\rho \left({ \mathrm{\mathbf{r} }_{1} } \right)\rho
\left({ \mathrm{\mathbf{r} }_{2} } \right)}{\left|{ \mathrm{\mathbf{r} }_{1} -\mathrm{\mathbf{r} }_{2} } \right|}d\mathrm{\mathbf{r} }_{1} d\mathrm{\mathbf{r} }_{2} } }
-\frac{1}{2}a_{\text{X} } \sum\limits_{\mu \nu \kappa \tau \sigma } { P_{\mu \kappa
}^{\sigma } P_{\nu \tau }^{\sigma } \left({ \mu \nu \vert \kappa \tau }
\right)} +c_{\text{DF} } E_{\text{XC} } \left[{ \rho_{\alpha } ,\rho_{\beta } } \right]\qquad \text{(eqn:271)}

$$

其中 $V_{\text{NN} }$ 是核排斥能，
$h_{\mu \nu }$ 是含动能和电子-核吸引项的单电子算符矩阵元
（$\left\langle { \mathrm{\mathbf{ab} }}
\right\rangle$ 表示矩阵乘积 $\mathrm{\mathbf{ab} }$ 的迹）。
如通常那样，分子自旋轨道 $\psi_{p}^{\sigma }$
在以原子为中心的基函数上展开（$\sigma =\alpha ,\beta )$：

$$

\psi_{p}^{\sigma } \left({ \mathrm{\mathbf{r} }} \right)=\sum\limits_\mu{ c_{\mu
p}^{\sigma } \phi_{\mu } \left({ \mathrm{\mathbf{r} }} \right)}\qquad \text{(eqn:272)}

$$

MO 系数为 $c_{\mu p}^{\sigma }$。
双电子积分定义为：

$$

\left({ \mu \nu \vert \kappa \tau } \right)=\int{ \int{ \phi_{\mu } \left({\mathrm{\mathbf{r} }_{1} } \right)\phi_{\nu } \left({ \mathrm{\mathbf{r} }_{1} }
\right)r_{12}^{-1} \phi_{\kappa } \left({ \mathrm{\mathbf{r} }_{2} } \right)\phi
_{\tau } \left({ \mathrm{\mathbf{r} }_{2} } \right)d\mathrm{\mathbf{r} }_{1} d\mathrm{\mathbf{r} }_{2} } }\qquad \text{(eqn:273)}

$$

混合参数 $a_{\text{X} }$ 控制 Hartree-Fock 交换的份额，具有半经验性质。
$E_{\text{XC} } \left[{ \rho_{\alpha } ,\rho
_{\beta } } \right]$ 表示交换-相关能。
参数 $c_{\text{DF} }$ 是一个总的缩放因子，
使人们可以从 Hartree-Fock 理论
（$a_{\text{X} } =1, c_{\text{DF} } =0)$
到纯 DFT（$a_{\text{X} } =0, c_{\text{DF} } =1)$
再到杂化 DFT（$0<a_{\text{X} } <1, c_{\text{DF} } =1$）。
轨道满足自旋非限制 SCF 方程：

$$

F_{\mu \nu }^{\sigma } =h_{\mu \nu } +\sum\limits_{\kappa \tau } { P_{\kappa
\tau } \left({ \mu \nu \vert \kappa \tau } \right)-a_{\text{X} } P_{\kappa \tau
}^{\sigma } \left({ \mu \kappa \vert \nu \tau } \right)} +c_{\text{DF} } \left({ \mu
\vert V_{XC}^{\alpha } \vert \nu } \right)\qquad \text{(eqn:274)}

$$

其中
$V_{XC}^{\sigma } =\frac{\delta E_{XC} }{\delta \rho_{\sigma } \left({\mathrm{\mathbf{r} }} \right)}$，
$P_{\mu \nu } =P_{\mu \nu }^{\alpha } +P_{\mu
\nu }^{\beta }$ 是总电子密度。
对于 SOC 微扰，习惯上将基组视为与微扰无关。
在自旋非限制处理中，一阶导数为：

$$

\frac{\partial E_{\text{SCF} } }{\partial x_{K}^{\left( m \right)}
}=\sum\limits_{i_{\alpha } } { \left({ i_{\alpha } \vert h^{K}s_{m} \vert
i_{\alpha } } \right)} +\sum\limits_{i_{\beta } } { \left({ i_{\beta } \vert
h^{K}s_{m} \vert i_{\beta } } \right)} =0\qquad \text{(eqn:275)}

$$

对于二阶导数，需要受微扰的轨道。
然而，在自旋相关微扰存在时，
它们不能再取为纯自旋向上或自旋向下轨道。
相对于自旋分量 $m$ 的微扰第 $L$ 个分量，
轨道展开为：

$$

\psi_{i}^{\alpha ;\left( m \right)L} \left({ \mathrm{\mathbf{r} }}
\right)=\sum\limits_{a_{\alpha } } { U_{a_{\alpha } i_{\alpha } }^{\left( m
\right);L} \psi_{a}^{\alpha } \left({ \mathrm{\mathbf{r} }} \right)}
+\sum\limits_{a_{\beta } } { U_{a_{\beta } i_{\alpha } }^{\left( m \right);L}
\psi_{a}^{\beta } \left({ \mathrm{\mathbf{r} }} \right)}\qquad \text{(eqn:276)}

$$

$$

\psi_{i}^{\beta ;\left( m \right)L} \left({ \mathrm{\mathbf{r} }}
\right)=\sum\limits_{a_{\alpha } } { U_{a_{\alpha } i_{\beta } }^{\left( m
\right);L} \psi_{a}^{\alpha } \left({ \mathrm{\mathbf{r} }} \right)}
+\sum\limits_{a_{\beta } } { U_{a_{\beta } i_{\beta } }^{\left( m \right);L}
\psi_{a}^{\beta } \left({ \mathrm{\mathbf{r} }} \right)}\qquad \text{(eqn:277)}

$$

由于自旋矢量算符分量的矩阵元是纯实的，
而 SOC 算符的空间部分矩阵元是纯虚的，
可知一阶系数是纯虚的。
总 SCF 能量的二阶导数变为：

$$

\begin{split}
 \frac{\partial^{2}E_{\text{SCF} } }{\partial x_{K}^{\left( m \right)} \partial x_{L}^{\left({ -m} \right)} }=\sum\limits_{i_{\alpha } a_{\alpha } }
{\left\{{ U_{a_{\alpha } i_{\alpha } }^{\left({ -m} \right);L\ast } \left({a_{\alpha } \vert h^{K}s_{m} \vert i_{\alpha } } \right)+U_{a_{\alpha }
i_{\alpha } }^{\left({ -m} \right);L} \left({ i_{\alpha } \vert h^{K}s_{m}
\vert a_{\alpha } } \right)} \right\}} \\
 +\sum\limits_{i_{\alpha } a_{\beta } } { \left\{{ U_{a_{\beta } i_{\alpha }
}^{\left({ -m} \right);L\ast } \left({ a_{\beta } \vert h^{K}s_{m} \vert
i_{\alpha } } \right)+U_{a_{\beta } i_{\alpha } }^{\left({ -m} \right);L}
\left({ i_{\alpha } \vert h^{K}s_{m} \vert a_{\beta } } \right)} \right\}}
\\
 +\sum\limits_{i_{\beta } a_{\alpha } } { \left\{{ U_{a_{\alpha } i_{\beta }
}^{\left({ -m} \right);L\ast } \left({ a_{\alpha } \vert h^{K}s_{m} \vert
i_{\beta } } \right)+U_{a_{\alpha } i_{\beta } }^{\left({ -m} \right);L}
\left({ i_{\beta } \vert h^{K}s_{m} \vert a_{\alpha } } \right)} \right\}}
\\
 +\sum\limits_{i_{\beta } a_{\beta } } { \left\{{ U_{a_{\beta } i_{\beta }
}^{\left({ -m} \right);L\ast } \left({ a_{\beta } \vert h^{K}s_{m} \vert
i_{\beta } } \right)+U_{a_{\beta } i_{\beta } }^{\left({ -m} \right);L}
\left({ i_{\beta } \vert h^{K}s_{m} \vert a_{\beta } } \right)} \right\}}
\end{split}\qquad \text{(eqn:278)}

$$

考察三种情形 $m=0, \pm 1$ 可得 **D**-张量分量的如下方程：

$$

D_{KL}^{\left( 0 \right)} =-\frac{1}{4S^{2} }\sum\limits_{\mu \nu }
{\frac{\partial P_{\mu \nu }^{\left( 0 \right)} }{\partial x_{L}^{\left( 0
\right)} }\left({ \mu \vert h^{K;\text{SOC} }\vert \nu } \right)}\qquad \text{(eqn:279)}

$$

$$

D_{KL}^{\left({ +1} \right)} =\frac{1}{2\left({ S+1} \right)\left({ 2S+1}
\right)}\sum\limits_{\mu \nu } { \left({ \mu \vert h^{K;\text{SOC} }\vert \nu }
\right)\frac{\partial P_{\mu \nu }^{\left({ -1} \right)} }{\partial
x_{L}^{\left({ +1} \right)} } }\qquad \text{(eqn:280)}

$$

$$

D_{KL}^{\left({ -1} \right)} =\frac{1}{2S\left({ 2S-1}
\right)}\sum\limits_{\mu \nu } { \left({ \mu \vert h^{K;\text{SOC} }\vert \nu }
\right)} \frac{\partial P_{\mu \nu }^{\left({ +1} \right)} }{\partial
x_{L}^{\left({ -1} \right)} }\qquad \text{(eqn:281)}

$$

其中选取了受微扰密度的特殊形式。
它们在原子轨道基下给出为：

$$

\frac{\partial P_{\mu \nu }^{\left( 0 \right)} }{\partial x_{L}^{\left( 0
\right)} }=\sum\limits_{i_{\alpha } a_{\alpha } } { U_{a_{\alpha } i_{\alpha
} }^{\left( 0 \right);L} c_{\mu i}^{\alpha } c_{\nu a}^{\alpha } }
+\sum\limits_{i_{\beta } a_{\beta } } { U_{a_{\beta } i_{\beta } }^{\left( 0
\right);L} c_{\mu i}^{\beta } c_{\nu a}^{\beta } }\qquad \text{(eqn:282)}

$$

$$

\frac{\partial P_{\mu \nu }^{\left({ +1} \right)} }{\partial x_{L}^{\left({-1} \right)} }=\sum\limits_{i_{\alpha } a_{\beta } } { U_{a_{\beta }
i_{\alpha } }^{\left({ -1} \right);L} c_{\mu i}^{\alpha } c_{\nu a}^{\beta }
} -\sum\limits_{i_{\beta } a_{\alpha } } { U_{a_{\alpha } i_{\beta }
}^{\left({ -1} \right);L} c_{\mu a}^{\alpha } c_{\nu i}^{\beta } }\qquad \text{(eqn:283)}

$$

$$

\frac{\partial P_{\mu \nu }^{\left({ -1} \right)} }{\partial x_{L}^{\left({+1} \right)} }=-\sum\limits_{i_{\alpha } a_{\beta } } { U_{a_{\beta }
i_{\alpha } }^{\left({ +1} \right);L} c_{\mu a}^{\beta } c_{\nu i}^{\alpha }
} +\sum\limits_{i_{\beta } a_{\alpha } } { U_{a_{\alpha } i_{\beta }
}^{\left({ +1} \right);L} c_{\mu i}^{\beta } c_{\nu a}^{\alpha } }\qquad \text{(eqn:284)}

$$

耦合微扰方程的特殊形式在 ORCArun 中实现如下：
微扰具有一般形式 $h^{K}\hat{{s} }_{m}$。
方程 [Eq](#eqn:279)-[Eq](#eqn:284) 以及下文 [Eq](#eqn:285)-[Eq](#eqn:290) 的写法
已执行了自旋积分，但将自旋相关因子从右端去掉，
并纳入式 [Eq](#eqn:279)-[Eq](#eqn:281) 的前置因子中。
待求解线性方程的显式形式为：

$m=0$：

$$

\left({ \varepsilon_{a_{\alpha } }^{\left( 0 \right)} -\varepsilon
_{i_{\alpha } }^{\left( 0 \right)} } \right)U_{a_{\alpha } i_{\alpha }
}^{K\left( 0 \right)} +a_{\text{X} } \sum\limits_{j_{\alpha } b_{\alpha } }
{U_{b_{\alpha } j_{\alpha } }^{K\left( m \right)} \left\{{ \left({ b_{\alpha
} i_{\alpha } \vert a_{\alpha } j_{\alpha } } \right)-\left({ j_{\alpha }
i_{\alpha } \vert a_{\alpha } b_{\alpha } } \right)} \right\}} =-\left({a_{\alpha } \vert h^{K}\vert i_{\alpha } } \right)\qquad \text{(eqn:285)}

$$

$$

\left({ \varepsilon_{a_{\beta } }^{\left( 0 \right)} -\varepsilon
_{i_{\beta } }^{\left( 0 \right)} } \right)U_{a_{\beta } i_{\beta }
}^{K\left( 0 \right)} +a_{\text{X} } \sum\limits_{j_{\beta } b_{\beta } }
{U_{b_{\beta } j_{\beta } }^{K\left( m \right)} \left\{{ \left({ b_{\beta }
i_{\beta } \vert a_{\beta } j_{\beta } } \right)-\left({ j_{\beta } i_{\beta
} \vert a_{\beta } b_{\beta } } \right)} \right\}} =-\left({ a_{\beta }
\vert h^{K}\vert i_{\beta } } \right)\qquad \text{(eqn:286)}

$$

$m=+1$：

$$

\left({ \varepsilon_{a_{\alpha } }^{\left( 0 \right)} -\varepsilon
_{i_{\beta } }^{\left( 0 \right)} } \right)U_{a_{\alpha } i_{\beta }
}^{K\left({ +1} \right)} +a_{\text{X} } \sum\limits_{j_{\alpha } b_{\alpha } }
{U_{b_{\beta } j_{\alpha } }^{K\left({ +1} \right)} \left({ b_{\beta }
i_{\beta } \vert a_{\alpha } j_{\alpha } } \right)} -a_{\text{X} }
\sum\limits_{b_{\alpha } j_{\beta } } { U_{b_{\beta } j_{\alpha } }^{K\left({+1} \right)} \left({ j_{\beta } i_{\beta } \vert a_{\alpha } b_{\alpha } }
\right)} =-\left({ a_{\alpha } \vert h^{K}\vert i_{\beta } } \right)\qquad \text{(eqn:287)}

$$

$$

\left({ \varepsilon_{a_{\beta } }^{\left( 0 \right)} -\varepsilon
_{i_{\alpha } }^{\left( 0 \right)} } \right)U_{a_{\beta } i_{\alpha }
}^{K\left({ +1} \right)} +a_{\text{X} } \sum\limits_{j_{\beta } b_{\alpha } }
{U_{b_{\alpha } j_{\beta } }^{K\left({ +1} \right)} \left({ b_{\alpha }
i_{\alpha } \vert a_{b} j_{\beta } } \right)} -a_{\text{X} } \sum\limits_{b_{\beta }
j_{\alpha } } { U_{b_{\beta } j_{\alpha } }^{K\left({ +1} \right)} \left({j_{\alpha } i_{\alpha } \vert a_{\beta } b_{\beta } } \right)} =0\qquad \text{(eqn:288)}

$$

$m=-1$：

$$

\left({ \varepsilon_{a_{\beta } }^{\left( 0 \right)} -\varepsilon
_{i_{\alpha } }^{\left( 0 \right)} } \right)U_{a_{\beta } i_{\alpha }
}^{K\left({ -1} \right)} +a_{\text{X} } \sum\limits_{j_{\beta } b_{\alpha } }
{U_{b_{\alpha } j_{\beta } }^{K\left({ -1} \right)} \left({ b_{\alpha }
i_{\alpha } \vert a_{b} j_{\beta } } \right)} -a_{\text{X} } \sum\limits_{b_{\beta }
j_{\alpha } } { U_{b_{\beta } j_{\alpha } }^{K\left({ -1} \right)} \left({j_{\alpha } i_{\alpha } \vert a_{\beta } b_{\beta } } \right)} =-\left({a_{\beta } \vert h^{K}\vert i_{\alpha } } \right)\qquad \text{(eqn:289)}

$$

$$

\left({ \varepsilon_{a_{\alpha } }^{\left( 0 \right)} -\varepsilon
_{i_{\beta } }^{\left( 0 \right)} } \right)U_{a_{\alpha } i_{\beta }
}^{K\left({ -1} \right)} +a_{\text{X} } \sum\limits_{j_{\alpha } b_{\alpha } }
{U_{b_{\beta } j_{\alpha } }^{K\left({ -1} \right)} \left({ b_{\beta }
i_{\beta } \vert a_{\alpha } j_{\alpha } } \right)} -a_{\text{X} }
\sum\limits_{b_{\alpha } j_{\beta } } { U_{b_{\beta } j_{\alpha } }^{K\left({-1} \right)} \left({ j_{\beta } i_{\beta } \vert a_{\alpha } b_{\alpha } }
\right)} =0\qquad \text{(eqn:290)}

$$

请注意，这些耦合微扰（CP）方程不含库仑势或
任何其他局域势（如 DFT 中的交换-相关势）的贡献。
因此，在没有 HF 交换时，方程可平凡求解：

$$

U_{a_{\alpha } i_{\alpha } }^{K\left( 0 \right)} =-\frac{\left({ a_{\alpha }
\vert h^{K}\vert i_{\alpha } } \right)}{\varepsilon_{a_{\alpha } }^{\left(0 \right)} -\varepsilon_{i_{\alpha } }^{\left( 0 \right)} }\qquad \text{(eqn:291)}

$$

$$

U_{a_{\beta } i_{\beta } }^{K\left( 0 \right)} =-\frac{\left({ a_{\beta }
\vert h^{K}\vert i_{\beta } } \right)}{\varepsilon_{a_{\beta } }^{\left( 0
\right)} -\varepsilon_{i_{\beta } }^{\left( 0 \right)} }\qquad \text{(eqn:292)}

$$

$$

U_{a_{\alpha } i_{\beta } }^{K\left({ +1} \right)} =-\frac{\left({ a_{\alpha
} \vert h^{K}\vert i_{\beta } } \right)}{\varepsilon_{a_{\alpha } }^{\left(0 \right)} -\varepsilon_{i_{\beta } }^{\left( 0 \right)} }\qquad \text{(eqn:293)}

$$

$$

U_{a_{\beta } i_{\alpha } }^{K\left({ +1} \right)} =0\qquad \text{(eqn:294)}

$$

$$

U_{a_{\beta } i_{\alpha } }^{K\left({ -1} \right)} =-\frac{\left({ a_{\beta
} \vert h^{K}\vert i_{\alpha } } \right)}{\varepsilon_{a_{\beta } }^{\left(0 \right)} -\varepsilon_{i_{\alpha } }^{\left( 0 \right)} }\qquad \text{(eqn:295)}

$$

$$

U_{a_{\alpha } i_{\beta } }^{K\left({ -1} \right)} =0\qquad \text{(eqn:296)}

$$

有趣的是，"反向自旋翻转系数"
$U_{a_{\beta } i_{\alpha } }^{K\left({ +1} \right)}$ 和
$U_{a_{\alpha } i_{\beta } }^{K\left({ -1} \right)}$
只有在存在 HF 交换时才非零。
在 CP 方程的微扰展开中，它们出现在二阶
（V$^{2}$/$\Delta \varepsilon^{2})$，
而其他系数是一阶的
（V/$\Delta \varepsilon$；V 表示微扰的矩阵元）。
因此这些贡献是 $\alpha^{4}$ 量级的，
为了始终一致地保持在 $\alpha^{2}$ 水平，可以考虑将它们从处理中略去。
不过在当前处理中仍保留了这些项。

方程 [Eq](#eqn:285)-[Eq](#eqn:290) 称为
CP-SOC（耦合微扰自旋-轨道耦合）方程。
它们可用标准技术求解，
是为确定 g 张量而求解的 CP-SCF 磁响应方程的所需类比，
此前已详细讨论 [perdew1992physa](../../bibliography.md)。
不难证实，在没有 HF 交换时，
将式 [Eq](#eqn:291)-[Eq](#eqn:296) 代入式 [Eq](#eqn:279)-[Eq](#eqn:284)
会回到 SOC 对 **D**-张量贡献的修正 Pederson-Khanna 型处理
[perdew1996phys](../../bibliography.md)。
在上面发展的形式框架内，
Pederson-Khanna 公式可改写为：

$$

\begin{split}
 D_{KL}^{\left({ \text{SOC};\text{PK} } \right)} =\frac{1}{4S^{2} }\sum\limits_{i_{\beta }
,a_{\beta } } { \left({ \psi_{i}^{\beta } \left|{ h^{K;\text{SOC} } } \right|\psi
_{a}^{\beta } } \right)U_{a_{\beta } i_{\beta } }^{L;\left( 0 \right)} }
+\frac{1}{4S^{2} }\sum\limits_{i_{\alpha } ,a_{\alpha } } { \left({ \psi
_{i}^{\alpha } \left|{ h^{K;\text{SOC} } } \right|\psi_{a}^{\alpha } }
\right)U_{a_{\alpha } i_{\alpha } }^{L;\left( 0 \right)} } \\
\hspace{3cm}
-\frac{1}{4S^{2} }\sum\limits_{i_{\alpha
} ,a_{\beta } } { \left({ \psi_{i}^{\alpha } \left|{ h^{K;\text{SOC} } }
\right|\psi_{a}^{\beta } } \right)U_{a_{\beta } i_{\alpha } }^{L;\left({-1} \right)} } -\frac{1}{4S^{2} }\sum\limits_{i_{\beta } ,a_{\alpha } }
{\left({ \psi_{i}^{\alpha } \left|{ h^{K;\text{SOC} } } \right|\psi_{a}^{\alpha
} } \right)U_{a_{\alpha } i_{\beta } }^{L;\left({ +1} \right)} }
\end{split}\qquad \text{(eqn:297)}

$$

该方程由二阶非自洽微扰理论导出，未借助自旋耦合。
对于没有 Hartree-Fock 交换的特殊情形，
与这里给出的处理的主要区别在于，
式 [Eq](#eqn:268)-[Eq](#eqn:270) 中的正确前置因子
出现在自旋翻转贡献前，
而不是式 [Eq](#eqn:297) 中的 $\pm$ 1/(4$S^{2})$。
在存在 HF 交换时，建议 PK 方法的一致推广
是式 [Eq](#eqn:279)-[Eq](#eqn:281) 带 $\pm$ 1/(4$S^{2})$ 前置因子，
该方法已作为一个选项在 ORCA 程序中这样实现。

为完整起见，SCF 情形下自旋-自旋项的评估可方便地通过下式进行：

$$

D_{KL}^{\left( \text{SS} \right)} =\frac{g_{e}^{2} }{4}\frac{\alpha^{2} }{S\left({2S-1} \right)}\sum\limits_{\mu \nu } { \sum\limits_{\kappa \tau } { \left\{{P_{\mu \nu }^{\alpha -\beta } P_{\kappa \tau }^{\alpha -\beta } -P_{\mu
\kappa }^{\alpha -\beta } P_{\nu \tau }^{\alpha -\beta } } \right\}} }
\left\langle { \mu \nu \left|{ r_{12}^{-5} \left\{{ 3r_{12,K} r_{12,L}
-\delta_{KL} r_{12}^{2} } \right\}} \right|\kappa \tau } \right\rangle\qquad \text{(eqn:298)}

$$

由 McWeeny 和 Mizuno 导出，
并由 Sinnecker 和 Neese 作了较详细的讨论。[sinnecker2006](../../bibliography.md)
在该文献中发现，若计算基于自旋非限制 SCF 处理，
DFT 方法倾向于高估自旋-自旋贡献。
对开壳层自旋限制计算发现了与实验好得多的关联。
这一效应的来源证明难以理解，
但文献 [hammer1999phys](../../bibliography.md) 表明，在自旋污染很小的情形下，
ROKS 计算的结果与基于自旋非限制自然轨道（UNO）行列式
所得的结果实际上无法区分。
因此在 ORCA 程序中可选择在 UNO 行列式基础上计算自旋-自旋项。

### ZFS 关键词（ZFS Keywords）

<a id="tab:spectroscopyproperties.epr.D.keywords.block"></a>
!!! note "与 ZFS 计算相关的 `%eprnmr` 块输入关键词"
    | 关键词          | 选项           | 说明                                       |
    |:----------------|:-----------------|:-------------------------------------------------|
    | `dtensor`       | `ss`             | 计算自旋-自旋部分                         |
    |                 | `so`             | 计算自旋-轨道部分                        |
    |                 | `ssandso`        | 计算两部分                             |
    | `DSOC`          | `qro`            | SOC 的准限制方法，必须与 `!UNO` 组合|
    |                 | `pk`             | SOC 的 Pederson-Khanna 方法                   |
    |                 | `cp`             | SOC 的耦合微扰方法（默认）       |
    |                 | `cvw`            | SOC 的 van Wüllen 方法                        |
    | `DSS`           | `direct`         | 直接用正则轨道计算自旋密度|
    |                 | `uno`            | 用 UNO 的自旋密度                       |
    | `printEuler`    | `true/false`     | 是否通过 `orca_euler` 计算欧拉角 |

