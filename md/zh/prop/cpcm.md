---
title: 隐式溶剂化模型
source: https://www.faccts.de/docs/orca/6.1/tutorials/prop/cpcm.html
---

# 隐式溶剂化模型

在计算中引入溶剂效应的一种途径是所谓的"隐式溶剂模型"（implicit solvent model），这里我们将讨论 ORCA 中可用的两个主要选项。

## 概述

在这类模型中，溶质被放置在一个大致呈分子形状的空穴（cavity）中。溶剂被描述为连续介质（continuum），它与空穴表面的电荷相互作用，而这些电荷又由溶质决定，问题通过迭代方式求解（关于这一主题的一篇很好的综述见 [[Cammi2005]](../bib.md#cammi2005)）。

该方法的总体图像可以描绘如下：

[![surfaces_v2](../images/surfaces_v2.png)](../images/surfaces_v2.png)

其中"探针"（probe）是一个理想的溶剂分子，分子空穴由以下方式定义：

> - "范德华表面"（Van der Waals surface，vdW），由范德华半径构建（ORCA 中的默认设置）；
> - "溶剂可及表面"（Solvent-Accessible Surface，SAS），由探针的中心定义；
> - 或"溶剂排除表面"（Solvent-Excluded Surface，SES），即沿溶剂探针球在 vdW 表面上滚动时其内侧部分所形成的表面。

下图展示了一个环糊精分子 SES 的可视化示例：

[![cyclodex-ses-transparency40](../images/cyclodex-ses-transparency40.png)](../images/cyclodex-ses-transparency40.png)

*图：一个环糊精分子的 SES。*

溶剂化能（solvation energy）随后分解为两个主要项：静电项（$\Delta G_{ENP}$）和空穴-色散项（$\Delta G_{CDS}$）：

$$
\Delta G_{solv}^o = \Delta G_{ENP} + \Delta G_{CDS}
$$

各方法的区别就在于如何计算这两项。

## 从气相到液相的转变

取决于你所期望的分子参考态，溶剂化自由能中还需要包含一个额外项：

$$
\Delta G_{solv}^o = \Delta G_{ENP} + \Delta G_{CDS} + \Delta G^o_{conc}
$$

这一项出现在从 $1 atm$、$298 K$ 的气相（使用 `FREQ` 时默认 $G^o$ 就是按此条件计算的）转到 $1 molL^{-1}$ 的溶液相时。相应的校正 [[Cramer2004]](../bib.md#cramer2004) 为：

$$
\Delta G^o_{conc}= RTln(24.5) = 1.89 \ \mathrm{kcal/mol}.
$$

> **警告**
> 在预测溶液热力学时，不要忘记把这一项加到你的 $G^o$ 中。缺少该校正可能导致很大的误差！

## 类导体极化连续介质模型（Conductor-like Polarizable Continuum Model，CPCM）

在 CPCM 方法 [[Cossi1998]](../bib.md#cossi1998) 中，体相溶剂被处理为类导体的极化连续介质（polarizable continuum），定义该方法的主要参数是介质的**折射率**（refractive index）和**介电常数**（dielectric constant）。

由介质与分子表面电荷相互作用产生的静电贡献（$\Delta G_{ENP}$）被包含在 SCF 计算中——因此你甚至可以得到"溶剂化"的轨道——而空穴项（$\Delta G_{CDS}$）可以从更复杂的格式中得到。

ORCA 预置了一份溶剂列表，可以通过以下方式调用：

```text
!CPCM(solvent)
```

本教程末尾给出了[可用溶剂](#availablesolvents)的完整列表。

如果想包含任何其他溶剂，总可以用如下方式手动输入这些参数：

```text
%CPCM       EPSILON      80.4
            REFRAC       1.33
END
```

更多选项和细节可以在 [ORCA 手册](https://www.faccts.de/docs/orca/6.0/manual)中找到。水溶液中阿司匹林分子单点计算的一个例子是：

```text
!B97M-V DEF2-SVP CPCM(WATER)
* XYZFILE 0 1 aspirin.xyz
```

> **注意**
> CPCM 的解析梯度和黑塞矩阵均可用，因此也可以与 `OPT` 和 `FREQ` 关键词一起使用！

然后，在 SCF 之前，会打印一个包含所有 CPCM 相关信息的标题：

```text
--------------------                               
CPCM SOLVATION MODEL
--------------------
CPCM parameters:
  Epsilon                                         ...      80.1510
  Refrac                                          ...       1.3328
  Rsolv                                           ...       1.3000
  Surface type                                    ... GAUSSIAN VDW
  Discretization scheme                           ... Constant charge density
    Threshold for H atoms                         ...       5.0000 (charges/Ang^2)
    Threshold for non-H atoms                     ...       5.0000 (charges/Ang^2)
  Epsilon function type                           ...         CPCM
Solvent:                                          ... WATER
Radii:
  Scheme                                          ... Element-dependent radii
  Radius for C  used is    3.8550 Bohr (=   2.0400 Ang.)
  Radius for O  used is    3.4469 Bohr (=   1.8240 Ang.)
  Radius for H  used is    2.4944 Bohr (=   1.3200 Ang.)
Calculating surface                               ...        done! (  0.0s)
Cavity surface points                             ...         2001
Cavity Volume                                     ...    1411.7200
Cavity Surface-area                               ...     764.1268
Calculating surface distance matrix               ...        done! (  0.0s)
Performing Cholesky decomposition & store         ...        done! (  0.1s)
Overall time for CPCM initialization              ...                 0.1s
```

SCF 计算结束后，会给出 CPCM 相关信息的汇总：

```text
----------------
TOTAL SCF ENERGY
----------------

Total Energy       :       -648.14295834055463 Eh          -17636.86654 eV

Components:
Nuclear Repulsion  :        765.01084602209096 Eh           20817.00344 eV
Electronic Energy  :      -1413.49491093482038 Eh          -38463.15196 eV
One Electron Energy:      -2400.15868861270292 Eh          -65311.63830 eV
Two Electron Energy:        986.66377767788265 Eh           26848.48634 eV
CPCM Dielectric    :         -0.02002640002963 Eh              -0.54495 eV
[...]
CPCM Solvation Model Properties:
Surface-charge          :         -0.01495190657874
Corrected charge        :          0.00000000000000
Outlying charge corr.   :          0.00001461700770 Eh               0.00040 eV
Free-energy (cav+disp)  :  This term is not implemented in the current solvation scheme
```

可以看到，能量的**介电贡献**、溶质的**净电荷**、**电荷**和**空穴校正**分别打印出来（本例中后者没有计算）。`Charge-correction` 项不包含在 SCF 能量中，打印出来仅供参考。

现在*最终单点能*已经包含了所有计算得到的溶剂化项。用上面给出的方程来表述，$\Delta G_{ENP}$ 对应 `CPCM Dielectric`，$\Delta G_{CDS}$ 对应 `Free-energy (cav+disp)`。

> **重要**
> 与以前的 ORCA 版本相比有一个重要区别。现在对于常规 CPCM，默认**不**计算空穴项，也不将其加入。

> **注意**
> 有关空穴项和 CPCM 的更多信息，请查阅 [ORCA 手册](https://www.faccts.de/docs/orca/6.0/manual)。

## CPCM 与 COSMO

ORCA **没有**任何 COSMO 实现，但可以使用 `CPCMC(solvent)` 关键词（多一个 "C"）来调用 COSMO 介电函数：

```text
!B97M-V DEF2-SVP CPCMC(WATER)
```

### 将 DFT 与后 HF 方法结合

由于 HF 密度的质量低于 DFT 得到的密度，从 HF 计算得到的 CPCM 校正也是如此。

通常可以这样做：从 DFT 这类计算中取出 $\Delta G_{ENP}$（*CPCM Dielectric*）和 $\Delta G_{CDS}$（*Free-energy (cav+disp)*），再把它们加到该方法得到的总能量上，例如如果你想把 CPCM 与 DLPNO-CSSD 结合的话。

### 高斯点电荷

常规的点电荷格式可能导致能量不稳定，例如当两个点靠得太近时。在 ORCA 中，我们改用弥散的高斯电荷（smeared Gaussian charge），以获得更平滑的势能面 [[Karplus1999]](../bib.md#karplus1999) [[Neese2020]](../bib.md#neese2020)。从 ORCA 5 起，默认设置是：

```text
%CPCM SURFACETYPE VDW_GAUSSIAN END
```

但也可以用如下方式选择 SES 表面：

```text
%CPCM SURFACETYPE GEPOL_SES_GAUSSIAN END
```

更详细的信息请查阅 [ORCA 手册](https://www.faccts.de/docs/orca/6.0/manual)。

## 通用溶剂化模型（SMD）

SMD 方法 [[Truhlar2009]](../bib.md#truhlar2009) 可以看作对 CPCM 的改进，因为它使用完整的溶质电子密度来计算空穴-色散贡献，而不只是面积。

该方法需要更多参数，因此对于未知溶剂的灵活性较差（[可用溶剂列表](#availablesolvents)）！SMD 可以像 CPCM 一样通过简单输入 `SMD(Solvent)` 来请求：

```text
!B97M-V DEF2-SVP SMD(WATER)

* XYZFILE 0 1 aspirin.xyz
```

初始输出与 CPCM 类似，只是现在带有 SMD 描述符：

```text
--------------------
CPCM SOLVATION MODEL
--------------------
[...]
SMD-CDS solvent descriptors:
  Soln                                       ...    1.3328
  Soln25                                     ...    1.3323
  Sola                                       ...    0.0000
  Solb                                       ...    0.0000
  Solg                                       ...    0.0000
  Solc                                       ...    0.0000
  Solh                                       ...    0.0000
```

而在 *TOTAL SCF ENERGY* 标题之前的输出中有：

```text
----------------
TOTAL SCF ENERGY
----------------                                  
[...]
CPCM Dielectric    :         -0.03176518706751 Eh              -0.86437 eV
SMD CDS (Gcds)     :          0.01088483110166 Eh               0.29619 eV
```

可以使用这个 $\Delta G_{CDS}$（*Gcds*）项，连同 $\Delta G_{ENP}$（*CPCM Dielectric*），去校正后续计算得到的能量。

> **注意**
> 在 ORCA 6 中，SMD 也有了可用的解析梯度！

## 连续介质溶剂化的动态半径调整（Dynamic Radii Adjustment for Continuum Solvation，DRACO）

所有这些溶剂化模型都依赖于对溶剂可及表面积（solvent accessible surface area，SASA）的物理上合理的描述。然而，通常采用的方法是用一组预定义的、按元素区分的原子半径来构建它。这并没有考虑特定原子的分子环境，而有效半径可能随局部电子密度的不同而变化，例如比较中性氧原子和带负电的氧原子时。Grimme 等人最近提出的 DRACO 模型 [[Grimme2024]](../bib.md#grimme2024) 让这些半径可以随环境自适应。它采用一种类似分子中原子（atoms-in-molecules）的方法，基于原子部分电荷和分数配位数，对每个原子的默认半径独立进行缩放。这样一来，尤其是对带电体系的描述可以得到改善。

DRACO 目前在 ORCA 中可用于 CPCM 和 SMD，并且针对水、乙腈、DMSO 和甲醇这几种溶剂进行了参数化。在相应溶剂化方法之外，用一个简单输入关键词即可调用 DRACO：

```text
! CPCM(solvent) DRACO
```

或

```text
! SMD(solvent) DRACO
```

也可以在 `%cpcm` 块中请求：

```text
%cpcm
DRACO true
end
```

在 ORCA 中，DRACO 中使用的部分电荷默认采用电负性均衡（electronegativity-equilibration，EEQ）电荷模型，D4 色散校正中也使用该模型。不过，也可以请求最近的电荷扩展 Hückel（Charge Extended Hückel，CEH）模型。[[Grimme2023]](../bib.md#grimme2023) DRACO 中的电荷格式由 `%cpcm` 块中的如下标签控制：

```text
%cpcm
draco_charges ceh  # default = eeq
end
```

如果请求 CEH 电荷，ORCA 会通过其与 xtb 程序的接口生成它们。

> **注意**
> 目前 DRACO 只能用于单点能计算。DRACO 的梯度将在未来实现。

## 示例 1：辛醇/水分配系数

我们将使用 SMD 并尝试预测药物地西泮（Diazepam）的辛醇/水分配系数（octanol/water partition coefficient，$P_{o/w}$）：

$$
P_{o/w} = \frac {[solute]_{octanol}} {[solute]_{water}}
$$

它可以通过平衡常数与溶质在辛醇和水中的吉布斯自由能之差 $\Delta G^o_{o/w} = \Delta G^o_{o} - \Delta G^o_{w}$ 之间的关系得到 [[Truhlar2009]](../bib.md#truhlar2009)：

$$
logP_{o/w} = \frac {-\Delta G^o_{o/w}} {2.303RT}
$$

首先，我们在每种溶剂中分别优化几何，例如使用：

```text
!B3LYP DEF2-SVP OPT NUMFREQ D4
%CPCM SMD TRUE
      SMDSOLVENT "1-OCTANOL"
END
* XYZFILE 0 1 diazepam.xyz
```

或：

```text
!B3LYP DEF2-SVP OPT NUMFREQ D4
%CPCM SMD TRUE
      SMDSOLVENT "WATER"
END
* XYZFILE 0 1 diazepam.xyz
```

以获得每种溶剂化化合物的吉布斯自由能及其几何结构。

完成计算后，得到能量差为 $3.41 \ \mathrm{kcal/mol}$，对应 $logP_{o/w}=2.50$；考虑到该方法的简单性，这与实验值 $logP_{o/w}^{exp}=2.99$ 相差不大。

> **注意**
> 由于 SMD 模型目前还没有解析频率，我们使用 !NUMFREQ。如果你在这里不做并行化，计算可能耗时很长。

### 示例 1 的结构

### 阿司匹林

```text
21

C         -2.64076        2.23326        0.00014
C         -3.28499        1.00146       -0.00001
C         -2.53276       -0.17323       -0.00006
C         -1.24586        2.29692        0.00023
C         -0.48687        1.12113        0.00013
C         -1.12591       -0.13504        0.00002
C         -0.44272       -1.46662       -0.00003
O         -1.06358       -2.51853       -0.00017
O          0.90426       -1.44815        0.00010
O          0.94078        1.15087        0.00026
C          1.78023        2.27870       -0.00045
O          1.43411        3.44948       -0.00130
C          3.21351        1.83099        0.00005
H          3.28673        0.73990       -0.00017
H          3.70751        2.20906        0.89847
H          3.70821        2.20936       -0.89786
H          1.28154       -0.55226        0.00027
H         -3.22416        3.15173        0.00019
H         -4.37149        0.95196       -0.00007
H         -0.79315        3.28276        0.00040
H         -3.05624       -1.12937       -0.00015
```

### 地西泮

```text
33

C         -2.76533       -0.90855        1.85461
C         -4.10278       -0.72362        2.22052
C         -5.02528       -0.30117        1.27344
C         -4.62706       -0.08566       -0.04023
C         -3.28690       -0.29486       -0.41749
C         -2.32208       -0.67243        0.53842
Cl        -6.66626       -0.05897        1.72353
N         -0.93200       -0.82351        0.23569
C         -0.24076       -0.01864       -0.67861
C         -1.02949        1.08452       -1.37013
C         -2.96608       -0.16369       -1.86911
N         -1.95301        0.48903       -2.32972
H         -0.32054        1.71528       -1.91810
H         -1.52297        1.73752       -0.64155
O          0.97434       -0.13069       -0.86774
C         -0.12886       -1.74693        1.02668
H          0.21402       -1.23663        1.93228
H          0.75039       -2.08063        0.46656
H         -0.70989       -2.63829        1.28413
C         -3.87195       -0.81596       -2.86776
C         -4.45465       -2.06403       -2.61294
C         -4.11329       -0.17301       -4.08765
C         -5.29672       -2.64689       -3.56241
C         -5.55029       -1.99264       -4.76807
C         -4.95622       -0.75907       -5.03306
H         -3.64497        0.78461       -4.30431
H         -4.24920       -2.60250       -1.69208
H         -5.74819       -3.61652       -3.36692
H         -6.20254       -2.45023       -5.50807
H         -5.14291       -0.25572       -5.97837
H         -5.36297        0.23683       -0.77401
H         -4.40857       -0.89624        3.24980
H         -2.07050       -1.19831        2.63954
```

## openCOSMO-RS

ORCA 已与 openCOSMO-RS[[Gerlach2022]](../bib.md#gerlach2022) 对接，它是 COSMO-RS 模型[[Klamt1995]](../bib.md#klamt1995) 的一个开源实现。该模型在学术界和工业界被广泛用于预测流体相热力学。

openCOSMO-RS 计算需要在 ORCA 内进行若干次单点能（SPE）评估：

1. **溶质**在**气相**中的 SPE 计算
2. **溶质**在**导体**（$\epsilon = \infty$）中的 SPE 计算
3. **溶剂**在**导体**（$\epsilon = \infty$）中的 SPE 计算
4. 通过 openCOSMO-RS 可执行程序进行 COSMO-RS 计算并求得溶剂化性质

第 1 至 3 步采用 BP86/def2-TZVPD 级别，该级别也曾用于为 ORCA 6.0 参数化 COSMO-RS。

> **警告**
> 可以更改 DFT 级别，但强烈不建议这样做。有关可用设置的细节
> 请参阅 [ORCA 手册](https://www.faccts.de/docs/orca/6.0/manual)。

ORCA 中的 COSMO-RS 计算可以通过简单关键词 `COSMORS(Solvent)` 或 `%cosmors` 块来控制。用简单关键词调用时，溶剂结构从 ORCA 内置的数据库中读取。一般推荐这种方式。不过，也可以通过 `%cosmors` 块定义个别溶剂。此时必须提供相应的结构文件 `Solvent.cosmorsxyz`。否则，只需要溶质结构。相应的输入如下：

```text
!COSMORS(Solvent)
```

这是使用简单关键词和数据库中溶剂的写法。而当单独定义溶剂时，写法如下：

```text
%cosmors
solvent "Solvent"
end
```

## 示例 2：乙酰胺从环己烷到水的转移

下面以计算乙酰胺（acetamide）从环己烷转移到水中的自由能变化为例。

[![acetamide-ctow](../images/acetamide-ctow.png)](../images/acetamide-ctow.png)

尽管在本例中电子能量和热统计贡献最终会相互抵消，我们仍将执行在两种溶剂中获得乙酰胺完整溶液自由能所需的全部计算。一般而言，任何化合物在溶液中的完整自由能都计算为气相电子能量（$E_{el.}$）、通常由刚性转子-谐振子（rigid-rotor-harmonic-oscillator，RRHO）近似得到的热统计自由能校正（$G_{RRHO}$），以及可用 openCOSMO-RS 计算的溶剂化自由能（$\delta G_{solv.}$）之和：

$$
G_{solv.} = E_{el.} + G_{RRHO} + \delta G_{solv.}
$$

> **注意**
> 请注意，对于 DFT 计算，电子能量上应加上[伦敦色散校正](../prop/disp.md)！

为获得相应贡献，我们首先优化乙酰胺在气相中的几何结构，并进行振动频率计算以得到热统计贡献：

```text
!r2SCAN-3c TIGHTOPT FREQ

*XYZFILE 0 1 acetamide_unpotimized.xyz
```

优化后的几何保存在 `basename.xyz` 中，频率计算和热统计校正可以在 `basename.out` 输出文件中找到：

```text
-------------------
GIBBS FREE ENERGY
-------------------

The Gibbs free energy is G = H - T*S
  
Total enthalpy                    ...   -209.09952655 Eh 
Total entropy correction          ...     -0.03087478 Eh    -19.37 kcal/mol
-----------------------------------------------------------------------
Final Gibbs free energy         ...   -209.13040133 Eh
     
For completeness - the Gibbs free energy minus the electronic energy
G-E(el)                           ...      0.04630314 Eh     29.06 kcal/mol
```

`Final Gibbs free energy` 的数值包含了电子能量以及自由能的全部贡献和校正（$E_{el.}$ 与 $G_{RRHO}$）。现在需要用 openCOSMO-RS 计算溶剂化自由能校正。为此，我们对乙酰胺做两次计算，一次在环己烷中，一次在水中。

本例中，我们使用数据库中的溶剂，相应输入为

```text
!COSMORS(Cyclohexane)

*XYZFILE 0 1 acetamide.xyz
```

以及

```text
!COSMORS(Water)

*XYZFILE 0 1 acetamide.xyz
```

从这些计算中，我们将得到 openCOSMO-RS 输出，其中显示最终的溶剂化自由能校正，以及溶质在气相中的能量、溶质在溶液中的能量和溶剂在溶液中的能量：

```text
----------------------------------------------
Single Point Calculation (solute / gas-phase)
----------------------------------------------
Output single point calculation redirected to >cosmors.solute_vac.lastout

FINAL SINGLE POINT ENERGY (Solute-gas-phase)     -209.312701693624

----------------------------------------------
Single Point Calculation (solute / CPCM)
----------------------------------------------
Output single point calculation redirected to >cosmors.solute_cpcm.lastout

FINAL SINGLE POINT ENERGY (Solute-CPCM)     -209.328833397120

----------------------------------------------
Single Point Calculation (solvent / CPCM)
----------------------------------------------
Output single point calculation redirected to >cosmors.solvent_cpcm.lastout

FINAL SINGLE POINT ENERGY (Solvent-CPCM)     -235.952716268645

----------------------
SOLVATION DATA
----------------------
Reference temperature              :                 298.15 K
Free energy of solvation (dGsolv)  :       -0.005754344722 Eh             -3.610907 kcal/mol
```

乙酰胺在水中的相应输出如下：

```text
----------------------------------------------
Single Point Calculation (solute / gas-phase)
----------------------------------------------
Output single point calculation redirected to >cosmors.solute_vac.lastout

FINAL SINGLE POINT ENERGY (Solute-gas-phase)     -209.312701693624

----------------------------------------------
Single Point Calculation (solute / CPCM)
----------------------------------------------
Output single point calculation redirected to >cosmors.solute_cpcm.lastout

FINAL SINGLE POINT ENERGY (Solute-CPCM)     -209.328833397120

----------------------------------------------
Single Point Calculation (solvent / CPCM)
----------------------------------------------
Output single point calculation redirected to >cosmors.solvent_cpcm.lastout

FINAL SINGLE POINT ENERGY (Solvent-CPCM)      -76.479236610833

----------------------
SOLVATION DATA
----------------------
Reference temperature              :                 298.15 K
Free energy of solvation (dGsolv)  :       -0.015783182256 Eh             -9.904099 kcal/mol
```

由这些计算，我们现在可以计算乙酰胺从环己烷到水转移的自由能（$\Delta G_{c\rightarrow w}$）。由于本例中所有其他贡献都相互抵消，可以把计算简化为两个溶剂化自由能校正之差：

$$
\Delta G_{c\rightarrow w} = \delta G_{solv., water} - \delta G_{solv., cyclohexane} = -6.29 \ \mathrm{kcal/mol}
$$

该结果与实验值 $-6.64 \ \mathrm{kcal/mol}$ 吻合得非常好。

### 示例 2 的结构

### 乙酰胺

```text
9

  C       0.03376875735606      0.11863667646978      0.00007971525188
  C      -1.38895738873537     -0.40815378292582      0.00073395653376
  O       0.30448472971793      1.30795933448501     -0.00094554067961
  N       1.00134723494097     -0.84772818347762      0.00045966276690
  H      -2.07609613647844      0.43734414878230      0.00311440104423
  H      -1.57575950037091     -1.02364915793043     -0.88606618799168
  H      -1.57403464730113     -1.02748224372305      0.88521351042739
  H       0.77976379331123     -1.82795867908554      0.00113804977546
  H       1.96698315755967     -0.56336811259461     -0.00042756712832
```

## 可用溶剂

| 溶剂 | CPCM | + DRACO | SMD | + DRACO | COSMO-RS |
| --- | --- | --- | --- | --- | --- |
| 1,1,1-trichloroethane | ✓ |  | ✓ |  |  |
| 1,1,2-trichloroethane | ✓ |  | ✓ |  |  |
| 1,2,4-trimethylbenzene | ✓ |  | ✓ |  |  |
| 1,2-dibromoethane | ✓ |  | ✓ |  | ✓ |
| 1,2-dichloroethane | ✓ |  | ✓ |  | ✓ |
| 1,2-ethanediol | ✓ |  | ✓ |  |  |
| 1,4-dioxane / dioxane | ✓ |  | ✓ |  | ✓ |
| 1-bromo-2-methylpropane | ✓ |  | ✓ |  |  |
| 1-bromooctane / bromooctane | ✓ |  | ✓ |  | ✓ |
| 1-bromopentane | ✓ |  | ✓ |  |  |
| 1-bromopropane | ✓ |  | ✓ |  |  |
| 1-butanol / butanol | ✓ |  | ✓ |  | ✓ |
| 1-chlorohexane / chlorohexane | ✓ |  | ✓ |  | ✓ |
| 1-chloropentane | ✓ |  | ✓ |  |  |
| 1-chloropropane | ✓ |  | ✓ |  |  |
| 1-decanol / decanol | ✓ |  | ✓ |  | ✓ |
| 1-fluorooctane | ✓ |  | ✓ |  | ✓ |
| 1-heptanol / heptanol | ✓ |  | ✓ |  | ✓ |
| 1-hexanol / hexanol | ✓ |  | ✓ |  | ✓ |
| 1-hexene | ✓ |  | ✓ |  |  |
| 1-hexyne | ✓ |  | ✓ |  |  |
| 1-iodobutane | ✓ |  | ✓ |  |  |
| 1-iodohexadecane / hexadecyliodide | ✓ |  | ✓ |  | ✓ |
| 1-iodopentane | ✓ |  | ✓ |  |  |
| 1-iodopropane | ✓ |  | ✓ |  |  |
| 1-nitropropane | ✓ |  | ✓ |  |  |
| 1-nonanol / nonanol | ✓ |  | ✓ |  | ✓ |
| 1-octanol / octanol | ✓ |  | ✓ |  | ✓ |
| 1-pentanol / pentanol | ✓ |  | ✓ |  | ✓ |
| 1-pentene | ✓ |  | ✓ |  |  |
| 1-propanol / propanol | ✓ |  | ✓ |  | ✓ |
| 2,2,2-trifluoroethanol | ✓ |  | ✓ |  |  |
| 2,2,4-trimethylpentane / isooctane | ✓ |  | ✓ |  | ✓ |
| 2,4-dimethylpentane | ✓ |  | ✓ |  |  |
| 2,4-dimethylpyridine | ✓ |  | ✓ |  |  |
| 2,6-dimethylpyridine | ✓ |  | ✓ |  | ✓ |
| 2-bromopropane | ✓ |  | ✓ |  |  |
| 2-butanol / secbutanol | ✓ |  | ✓ |  | ✓ |
| 2-chlorobutane | ✓ |  | ✓ |  |  |
| 2-heptanone | ✓ |  | ✓ |  |  |
| 2-hexanone | ✓ |  | ✓ |  |  |
| 2-methoxyethanol / methoxyethanol | ✓ |  | ✓ |  | ✓ |
| 2-methyl-1-propanol / isobutanol | ✓ |  | ✓ |  | ✓ |
| 2-methyl-2-propanol | ✓ |  | ✓ |  |  |
| 2-methylpentane | ✓ |  | ✓ |  |  |
| 2-methylpyridine / 2methylpyridine | ✓ |  | ✓ |  | ✓ |
| 2-nitropropane | ✓ |  | ✓ |  |  |
| 2-octanone | ✓ |  | ✓ |  |  |
| 2-pentanone | ✓ |  | ✓ |  |  |
| 2-propanol / isopropanol | ✓ |  | ✓ |  | ✓ |
| 2-propen-1-ol | ✓ |  | ✓ |  |  |
| e-2-pentene | ✓ |  | ✓ |  |  |
| 3-methylpyridine | ✓ |  | ✓ |  |  |
| 3-pentanone | ✓ |  | ✓ |  |  |
| 4-heptanone | ✓ |  | ✓ |  |  |
| 4-methyl-2-pentanone / 4methyl2pentanone | ✓ |  | ✓ |  | ✓ |
| 4-methylpyridine | ✓ |  | ✓ |  |  |
| 5-nonanone | ✓ |  | ✓ |  |  |
| acetic acid / aceticacid | ✓ |  | ✓ |  | ✓ |
| acetone | ✓ |  | ✓ |  | ✓ |
| acetonitrile / mecn / ch3cn | ✓ | ✓ | ✓ | ✓ | ✓ |
| acetophenone | ✓ |  | ✓ |  | ✓ |
| ammonia | ✓ |  |  |  | ✓ |
| aniline | ✓ |  | ✓ |  | ✓ |
| anisole | ✓ |  | ✓ |  | ✓ |
| benzaldehyde | ✓ |  | ✓ |  | ✓ |
| benzene | ✓ |  | ✓ |  | ✓ |
| benzonitrile | ✓ |  | ✓ |  | ✓ |
| benzyl alcohol / benzylalcohol | ✓ |  | ✓ |  | ✓ |
| bromobenzene | ✓ |  | ✓ |  | ✓ |
| bromoethane | ✓ |  | ✓ |  | ✓ |
| bromoform | ✓ |  | ✓ |  | ✓ |
| butanal | ✓ |  | ✓ |  |  |
| butanoic acid | ✓ |  | ✓ |  |  |
| butanone | ✓ |  | ✓ |  | ✓ |
| butanonitrile | ✓ |  | ✓ |  |  |
| butyl ethanoate / butyl acetate / butylacetate | ✓ |  | ✓ |  | ✓ |
| butylamine | ✓ |  | ✓ |  |  |
| n-butylbenzene / butylbenzene | ✓ |  | ✓ |  | ✓ |
| sec-butylbenzene / secbutylbenzene | ✓ |  | ✓ |  | ✓ |
| tert-butylbenzene / tbutylbenzene | ✓ |  | ✓ |  | ✓ |
| carbon disulfide / carbondisulfide / cs2 | ✓ |  | ✓ |  | ✓ |
| carbon tetrachloride / ccl4 | ✓ |  | ✓ |  | ✓ |
| chlorobenzene | ✓ |  | ✓ |  | ✓ |
| chloroform / chcl3 | ✓ |  | ✓ |  | ✓ |
| a-chlorotoluene | ✓ |  | ✓ |  |  |
| o-chlorotoluene | ✓ |  | ✓ |  |  |
| conductor | ✓ |  |  |  |  |
| m-cresol / mcresol | ✓ |  | ✓ |  | ✓ |
| o-cresol | ✓ |  | ✓ |  |  |
| cyclohexane | ✓ |  | ✓ |  | ✓ |
| cyclohexanone | ✓ |  | ✓ |  | ✓ |
| cyclopentane | ✓ |  | ✓ |  |  |
| cyclopentanol | ✓ |  | ✓ |  |  |
| cyclopentanone | ✓ |  | ✓ |  |  |
| decalin | ✓ |  | ✓ |  | ✓ |
| cis-decalin | ✓ |  | ✓ |  |  |
| n-decane / decane | ✓ |  | ✓ |  | ✓ |
| dibromomethane | ✓ |  | ✓ |  |  |
| dibutylether | ✓ |  | ✓ |  | ✓ |
| o-dichlorobenzene / odichlorobenzene | ✓ |  | ✓ |  | ✓ |
| e-1,2-dichloroethene | ✓ |  | ✓ |  |  |
| z-1,2-dichloroethene | ✓ |  | ✓ |  |  |
| dichloromethane / ch2cl2 / dcm | ✓ |  | ✓ |  | ✓ |
| diethyl ether / diethylether | ✓ |  | ✓ |  | ✓ |
| diethyl sulfide | ✓ |  | ✓ |  |  |
| diethylamine | ✓ |  | ✓ |  |  |
| diiodomethane | ✓ |  | ✓ |  |  |
| diisopropyl ether / diisopropylether | ✓ |  | ✓ |  | ✓ |
| cis-1,2-dimethylcyclohexane | ✓ |  | ✓ |  |  |
| dimethyl disulfide | ✓ |  | ✓ |  |  |
| n,n-dimethylacetamide / dimethylacetamide | ✓ |  | ✓ |  | ✓ |
| n,n-dimethylformamide / dimethylformamide / dmf | ✓ |  | ✓ |  | ✓ |
| dimethylsulfoxide / dmso | ✓ | ✓ | ✓ | ✓ | ✓ |
| diphenylether | ✓ |  | ✓ |  | ✓ |
| dipropylamine | ✓ |  | ✓ |  |  |
| n-dodecane / dodecane | ✓ |  | ✓ |  | ✓ |
| ethanethiol | ✓ |  | ✓ |  |  |
| ethanol | ✓ |  | ✓ |  | ✓ |
| ethyl acetate / ethylacetate / ethanoate | ✓ |  | ✓ |  | ✓ |
| ethyl methanoate | ✓ |  | ✓ |  |  |
| ethyl phenyl ether / ethoxybenzene | ✓ |  | ✓ |  | ✓ |
| ethylbenzene | ✓ |  | ✓ |  | ✓ |
| fluorobenzene | ✓ |  | ✓ |  | ✓ |
| formamide | ✓ |  | ✓ |  |  |
| formic acid | ✓ |  | ✓ |  |  |
| furan / furane |  |  |  |  | ✓ |
| n-heptane / heptane | ✓ |  | ✓ |  | ✓ |
| n-hexadecane / hexadecane | ✓ |  | ✓ |  | ✓ |
| n-hexane / hexane | ✓ |  | ✓ |  | ✓ |
| hexanoic acid | ✓ |  | ✓ |  |  |
| iodobenzene | ✓ |  | ✓ |  | ✓ |
| iodoethane | ✓ |  | ✓ |  |  |
| iodomethane | ✓ |  | ✓ |  |  |
| isopropylbenzene | ✓ |  | ✓ |  | ✓ |
| p-isopropyltoluene / isopropyltoluene | ✓ |  | ✓ |  |  |
| mesitylene | ✓ |  | ✓ |  | ✓ |
| methanol | ✓ | ✓ | ✓ | ✓ | ✓ |
| methyl benzoate | ✓ |  | ✓ |  |  |
| methyl butanoate | ✓ |  | ✓ |  |  |
| methyl ethanoate | ✓ |  | ✓ |  |  |
| methyl methanoate | ✓ |  | ✓ |  |  |
| methyl propanoate | ✓ |  | ✓ |  |  |
| n-methylaniline | ✓ |  | ✓ |  |  |
| methylcyclohexane | ✓ |  | ✓ |  |  |
| n-methylformamide / methylformamide | ✓ |  | ✓ |  | ✓ |
| nitrobenzene / phno2 | ✓ |  | ✓ |  | ✓ |
| nitroethane | ✓ |  | ✓ |  | ✓ |
| nitromethane / meno2 | ✓ |  | ✓ |  | ✓ |
| o-nitrotoluene / onitrotoluene | ✓ |  | ✓ |  |  |
| n-nonane / nonane | ✓ |  | ✓ |  | ✓ |
| n-octane / octane | ✓ |  | ✓ |  | ✓ |
| n-pentadecane / pentadecane | ✓ |  | ✓ |  | ✓ |
| octanol(wet) / wetoctanol / woctanol |  |  |  |  |  |
| pentanal | ✓ |  | ✓ |  |  |
| n-pentane / pentane | ✓ |  | ✓ |  | ✓ |
| pentanoic acid | ✓ |  | ✓ |  |  |
| pentyl ethanoate | ✓ |  | ✓ |  |  |
| pentylamine | ✓ |  | ✓ |  |  |
| perfluorobenzene / hexafluorobenzene | ✓ |  | ✓ |  | ✓ |
| phenol | ✓ |  |  |  | ✓ |
| propanal | ✓ |  | ✓ |  |  |
| propanoic acid | ✓ |  | ✓ |  |  |
| propanonitrile | ✓ |  | ✓ |  |  |
| propyl ethanoate | ✓ |  | ✓ |  |  |
| propylamine | ✓ |  | ✓ |  |  |
| pyridine | ✓ |  | ✓ |  | ✓ |
| tetrachloroethene / c2cl4 | ✓ |  | ✓ |  | ✓ |
| tetrahydrofuran / thf | ✓ |  | ✓ |  | ✓ |
| tetrahydrothiophene-s,s-dioxide / | ✓ |  | ✓ |  |  |
| / tetrahydrothiophenedioxide / sulfolane | ✓ |  | ✓ |  |  |
| tetralin | ✓ |  | ✓ |  | ✓ |
| thiophene | ✓ |  | ✓ |  |  |
| thiophenol | ✓ |  | ✓ |  |  |
| toluene | ✓ |  | ✓ |  | ✓ |
| trans-decalin | ✓ |  | ✓ |  |  |
| tributylphosphate | ✓ |  | ✓ |  | ✓ |
| trichloroethene | ✓ |  | ✓ |  |  |
| triethylamine | ✓ |  | ✓ |  | ✓ |
| n-undecane / undecane | ✓ |  | ✓ |  | ✓ |
| water / h2o | ✓ | ✓ | ✓ | ✓ | ✓ |
| xylene | ✓ |  | ✓ |  |  |
| m-xylene | ✓ |  | ✓ |  |  |
| o-xylene | ✓ |  | ✓ |  |  |
| p-xylene | ✓ |  | ✓ |  |  |

## 选定的介电常数

| 溶剂 | 介电常数 | 折射率 |
| --- | --- | --- |
| 水 | 80.4 | 1.33 |
| 丙酮 | 20.7 | 1.359 |
| 乙腈 | 36.6 | 1.344 |
| 氨 | 22.4 | 1.33 |
| 苯 | 2.28 | 1.501 |
| CCl4 | 2.24 | 1.466 |
| CH2Cl2 | 9.08 | 1.424 |
| 氯仿 | 4.9 | 1.45 |
| 环己烷 | 2.02 | 1.425 |
| DMF | 38.3 | 1.430 |
| DMSO | 47.2 | 1.479 |
| 乙醇 | 24.3 | 1.361 |
| 己烷 | 1.89 | 1.375 |
| 甲醇 | 32.63 | 1.329 |
| 辛醇 | 10.3 | 1.421 |
| 吡啶 | 12.5 | 1.510 |
| THF | 7.25 | 1.407 |
| 甲苯 | 2.4 | 1.497 |
