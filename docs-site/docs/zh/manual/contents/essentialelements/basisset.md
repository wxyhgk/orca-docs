

<a id="sec:essentialelements.basisset"></a>
# 基组（Basis Sets）

ORCA 提供大量原生实现的[轨道基组](#sec:essentialelements.basisset.builtin)和[辅助基组](#sec:essentialelements.basisset.aux)，以及可与之组合的各种[有效核势（effective core potentials, ECP）](#sec:essentialelements.basisset.ecps)。对于[标量相对论方法（如 ZORA、DKH 或 X2C）](relativistic.md#sec:essentialelements.relativistic)，也有专门的[相对论基组](#sec:essentialelements.basisset.builtin.rel)可供使用。此外，还可以[从外部文件读入](#sec:essentialelements.basisset.file)其他基组。大多数内置基组和 ECP 取自 Basis Set Exchange[bse2019](../../bibliography.md) 或其前身 EMSL 库，ORCA 中的输入格式与 "GAMESS-US" 格式密切相关。

<a id="sec:essentialelements.basisset.basicusage"></a>
## 基本用法（Basic Usage）

在 ORCA 中使用轨道基组和辅助基组最简单的方式是通过简单输入关键字。所有可用的轨道基组关键字见 [basisset.builtin](#sec:essentialelements.basisset.builtin)，所有辅助基组选项见 [basisset.aux](#sec:essentialelements.basisset.aux)。例如，Karlsruhe def2-TZVP 基组可以通过 `def2-TZVP` 关键字调用。

```orca
! def2-TZVP
```

!!! note "注意"
    有些基组（如 [Karlsruhe def2](#sec:essentialelements.basisset.builtin.def2)）对重元素默认采用 [ECP](#sec:essentialelements.basisset.ecps)，此处为 `def2-ECP`。ECP 的显式控制见 [basisset.ecps](#sec:essentialelements.basisset.ecps)。

[分辨率恒等式（resolution-of-the-identity, RI）](RI.md#sec:essentialelements.ri)所需的[辅助基组](#sec:essentialelements.basisset.aux)可以用同样的方式定义。本例中使用的是 Weigend 通用 `def2/J` 辅助基。

```orca
! def2-TZVP def2/J
```

!!! note "注意"
    注意，许多计算中 RI 默认是开启的（例如[杂化 DFT](../modelchemistries/DensityFunctionalTheory.md#sec:modelchemistries.dft.hybriddft) 默认使用 [RIJCOSX](RI.md#sec:essentialelements.ri.rijcosx)）。相应地，若未另行指定，`def2/J` 辅助基也会自动调用。在标量相对论计算中，默认改为 `SARC/J`。

<a id="par:essentialelements.basisset.basicusage.aux"></a>
注意，RI 的辅助基组有三个独立的槽位：
- `AuxJ` 是 [RI-J](RI.md#sec:essentialelements.ri.rij)、[RIJDX/RIJONX](RI.md#sec:essentialelements.ri.rijonx) 和 [RIJCOSX](RI.md#sec:essentialelements.ri.rijcosx) 近似所用的库仑拟合基。
- `AuxJK` 是 [RI-JK](RI.md#sec:essentialelements.ri.rijk) 所用的库仑与交换拟合基。
- `AuxC` 用于后 SCF 动态电子相关方法中基于 RI 的积分生成步骤，例如 [RI-MP2](../modelchemistries/MP2.md#sec:modelchemistries.mp2.ri)、[DLPNO-MP2](../modelchemistries/MP2.md#sec:modelchemistries.mp2.dlpno) 和 [DLPNO-CC](../modelchemistries/mdci.md#sec:modelchemistries.mdci.localcorrelation)。

最后，[F12 方法](../modelchemistries/mdci.md#sec:modelchemistries.mdci.expcorrelation)除了[专用轨道基](#sec:essentialelements.basisset.builtin.f12)（以及可能的 `AuxC`）外，还需要互补辅助基组（complementary auxiliary basis set, `CABS`），例如：

```orca
! F12-RI-MP2 cc-pVDZ-F12 cc-pVDZ-F12-CABS cc-pVTZ-F12-MP2Fit
```

用简单输入关键字指定辅助基组时，会将其分配到相应槽位。但每个基组槽位以及 ECP 都可以在 `%basis` 模块块中显式分配。例如，可以按这种方式把某个 "/JK" 基分配给 `AuxJ`。

```orca
%basis
  Basis "def2-TZVP"         # The orbital expansion basis set
  ECP   "def2-ECP"          # Effective core potential
  AuxJ  "def2/J"            # RI-J auxiliary basis set
  AuxJK "def2/JK"           # RI-JK auxiliary basis set
  AuxC  "def2-TZVP/C"       # Auxiliary basis set for correlated 
                            # calculations, e.g. RI-MP2
  CABS  "cc-pVDZ-F12-OptRI" # complementary auxiliary basis set 
                            # for F12 calculations
end
```

<a id="par:essentialelements.basisset.basicusage.decontract"></a>
如有需要，所有基组都可以通过简单输入（例如 `! DECONTRACT`）或带相应关键字的 `%basis` 模块块去收缩（decontract）。注意，如果你的基组来自一般收缩（general contraction），它会在多个收缩中包含重复的原始高斯函数。这些会被移除，只保留唯一的原始函数，因此不会有冗余问题。

```orca
%basis
  DecontractBas   false  # if chosen "true" the program will
                         # decontract the orbital basis set
  DecontractAuxJ  false  # if "true" - decontract the AuxJ basis set
  DecontractAuxJK false  # if "true" - decontract the AuxJK basis set
  DecontractAuxC  false  # if "true" - decontract the AuxC basis set
  DecontractCABS  true   # if "false" - do not decontract the CABS
  Decontract      false  # if "true" - decontract all basis sets
end
```

!!! tip "提示"
    - 一般而言，基组可以[分配给特定元素](#sec:essentialelements.basisset.element)、分配给单个[原子](#sec:essentialelements.basisset.atom)，甚至分配给[结构片段](#sec:essentialelements.basisset.fragments)。
    - 任何内置基组都可以通过 [`orca_exportbasis` 工具](../utilitiesvisualization/utilities.md#sec:utilities.exportbasis)导出。
    - 内置基组的参考文献通常打印在 ORCA 输出的开头，`orca_exportbasis` 也会给出。

!!! warning "警告"
    ORCA 对所有基组都使用纯 d 和 f 函数（5D 和 7F，而不是笛卡尔 6D 和 10F）。在与其他程序的结果作比较时需要考虑这一点，尤其是对于用笛卡尔 (6D) 函数优化的 Pople 型基组。

<a id="sec:essentialelements.basisset.builtin"></a>
## 轨道基组（Orbital Basis Sets）

下面我们将概述来自不同家族的原生实现基组，如 [Karlsruhe def2](#sec:essentialelements.basisset.builtin.def2) 和[相关一致（correlation consistent）](#sec:essentialelements.basisset.builtin.cc)基组，并列出各自的元素覆盖范围。如果重元素需要 [ECP](#sec:essentialelements.basisset.ecps)，会在相应表格条目中注明，并在通过简单输入或 `%basis` 模块块中的 `basis` 关键字选择该基组时默认调用。

<a id="sec:essentialelements.basisset.builtin.pople"></a>
### Pople 基组（Pople Basis Sets）

ORCA 中提供 Pople 基组家族的多种基组。所有可用的 Pople 型基组列于 [tab:essentialelements.basisset.builtin.pople](#tab:essentialelements.basisset.builtin.pople)。

!!! note "Pople 基组的命名约定（Naming Convention of Pople Basis Sets）"
    * \* 或 (d) 在除 H 以外的所有原子上添加一组第一极化函数
    * \*\* 或 (d,p) 在所有原子上添加一组第一极化函数
    * 更多组合：(2d)、(2df)、(2d,p)、(2d,2p)、(2df,2p)、(2df,2pd)
    * "G" 前的 $+$ 表示在除 H 以外的所有原子上包含弥散函数（例如 6-31$+$G）
    * "G" 前的 $++$ 表示在所有原子上包含弥散函数。仅当已包含 H 极化时才有效，例如 6-31$++$G(d,p)

<a id="tab:essentialelements.basisset.builtin.pople"></a>
!!! note "可用的 Pople 型基组。"
    | Basis Set | Elem. | ECP | Comment |
    | --- | --- | --- | --- |
    | `STO-3G` | H--I | \-- | 极小基组 |
    | `3-21G` | H--Cs | \-- |  |
    | `3-21GSP` | H--Ar | \-- |  |
    | `4-22GSP` | H--Ar | \-- |  |
    | `6-31G` | H--Zn | \-- |  |
    | `6-31G*` | H--Kr | \-- |  |
    | `m6-31G` | Sc--Cu | \-- | 用于 3d 过渡金属（Sc--Cu）的修改版 6-31G |
    | `m6-31G*` | Sc--Cu | \-- |  |
    | `6-31G**` | H--Zn | \-- |  |
    | `6-31G(d)` | H--Zn | \-- |  |
    | `6-31G(d,p)` | H--Zn | \-- |  |
    | `6-31G(2d)` | H--Zn | \-- |  |
    | `6-31G(2d,p)` | H--Zn | \-- |  |
    | `6-31G(2d,2p)` | H--Zn | \-- |  |
    | `6-31G(2df)` | H--Zn | \-- |  |
    | `6-31G(2df,2p)` | H--Zn | \-- |  |
    | `6-31G(2df,2pd)` | H--Zn | \-- |  |
    | `6-31+G*` | H--Kr | \-- |  |
    | `6-31+G**` | H--Zn | \-- |  |
    | `6-31+G(d)` | H--Zn | \-- |  |
    | `6-31+G(d,p)` | H--Zn | \-- |  |
    | `6-31+G(2d)` | H--Zn | \-- |  |
    | `6-31+G(2d,p)` | H--Zn | \-- |  |
    | `6-31+G(2d,2p)` | H--Zn | \-- |  |
    | `6-31+G(2df)` | H--Zn | \-- |  |
    | `6-31+G(2df,2p)` | H--Zn | \-- |  |
    | `6-31+G(2df,2pd)` | H--Zn | \-- |  |
    | `6-31++G**` | H--Zn | \-- |  |
    | `6-31++G(d,p)` | H--Zn | \-- |  |
    | `6-31++G(2d,p)` | H--Zn | \-- |  |
    | `6-31++G(2d,2p)` | H--Zn | \-- |  |
    | `6-31++G(2df,2p)` | H--Zn | \-- |  |
    | `6-31++G(2df,2pd)` | H--Zn | \-- |  |
    | `6-311G` | H--Br | \-- |  |
    | `6-311G*` | H--Br | \-- |  |
    | `6-311G**` | H--Br | \-- |  |
    | `6-311G(d)` | H--Br | \-- |  |
    | `6-311G(d,p)` | H--Br | \-- |  |
    | `6-311G(2d)` | H--Br | \-- |  |
    | `6-311G(2d,p)` | H--Br | \-- |  |
    | `6-311G(2d,2p)` | H--Br | \-- |  |
    | `6-311G(2df)` | H--Br | \-- |  |
    | `6-311G(2df,2p)` | H--Br | \-- |  |
    | `6-311G(2df,2pd)` | H--Br | \-- |  |
    | `6-311G(3df)` | H--Br | \-- |  |
    | `6-311G(3df,3pd)` | H--Br | \-- |  |
    | `6-311+G*` | H--Br | \-- |  |
    | `6-311+G**` | H--Br | \-- |  |
    | `6-311+G(d)` | H--Br | \-- |  |
    | `6-311+G(d,p)` | H--Br | \-- |  |
    | `6-311+G(2d)` | H--Br | \-- |  |
    | `6-311+G(2d,p)` | H--Br | \-- |  |
    | `6-311+G(2d,2p)` | H--Br | \-- |  |
    | `6-311+G(2df)` | H--Br | \-- |  |
    | `6-311+G(2df,2p)` | H--Br | \-- |  |
    | `6-311+G(2df,2pd)` | H--Br | \-- |  |
    | `6-311+G(3df)` | H--Br | \-- |  |
    | `6-311+G(3df,2p)` | H--Br | \-- |  |
    | `6-311+G(3df,3pd)` | H--Br | \-- |  |
    | `6-311++G**` | H--Br | \-- |  |
    | `6-311++G(d,p)` | H--Br | \-- |  |
    | `6-311++G(2d,p)` | H--Br | \-- |  |
    | `6-311++G(2d,2p)` | H--Br | \-- |  |
    | `6-311++G(2df,2p)` | H--Br | \-- |  |
    | `6-311++G(2df,2pd)` | H--Br | \-- |  |
    | `6-311++G(3df,3pd)` | H--Br | \-- |  |

<a id="sec:essentialelements.basisset.builtin.ahlrichs"></a>
### Ahlrichs 基组（Ahlrichs Basis Sets）

ORCA 中实现的较早的 Ahlrichs 基组包括全电子基组，以及对 Rb 以后所有元素自动采用 def-ECP 的基组。可用的 Ahlrichs 基组列于 [tab:essentialelements.basisset.builtin.ahlrichs](#tab:essentialelements.basisset.builtin.ahlrichs)。相对论重收缩变体见 [rel.ahlrichs](#sec:essentialelements.basisset.builtin.rel.ahlrichs)。

!!! note "注意"
    ORCA 的旧版本（ORCA <4.0）曾对 Rb-I 元素也使用下面这些双-$\zeta$ 和三-$\zeta$ 关键字加载全电子基组。Rb-I 基组源自 Turbomole 库的非相对论全电子基组（如 "TZVPAlls"）。**这种自动替换现已弃用**。不过我们暂时仍可通过在下面关键字前加前缀 "old-" 来复现该行为，例如 `old-TZVP`。

<a id="tab:essentialelements.basisset.builtin.ahlrichs"></a>
!!! note "可用的全电子 Ahlrichs 基组。"
    | Basis Set | Elem. | ECP | Comment |
    | --- | --- | --- | --- |
    | `SV` | H--Kr | \-- | 价层双-$\zeta$ 基组。 |
    | `SV(P)` | H--Kr | \-- | 仅在重元素上带极化的价层双-$\zeta$ 基组。 |
    | `SVP` | H--Kr | \-- | 带极化的价层双-$\zeta$ 基组。 |
    | `TZV` | H--Kr | \-- | 价层三-$\zeta$ 基组。 |
    | `TZV(P)` | H--Kr | \-- | 在重元素上带极化的价层三-$\zeta$ 基组。 |
    | `TZVP` | H--Kr | \-- | 带极化的价层三-$\zeta$ 基组。 |
    | `TZVPP` | H--Kr | \-- | 双重极化的三-$\zeta$ 基组。 |
    | `QZVP` | H--Kr | \-- | 带极化的价层四-$\zeta$ 基组。 |
    | `QZVPP` | H--Kr | \-- | 双重极化的四-$\zeta$ 基组。 |
    | `def-SV(P)` | H--Lr | `def-ECP` (Rb--Lr) | 仅在重元素上带极化的价层双-$\zeta$ 基组。 |
    | `def-SVP` | H--Lr | `def-ECP` (Rb--Lr) | 带极化的价层双-$\zeta$ 基组。 |
    | `def-TZVP` | H--Lr | `def-ECP` (Rb--Lr) | 带极化函数的价层三-$\zeta$ 基组。 |
    | `def-TZVPP` | H--Lr | `def-ECP` (Rb--Lr) | 双重极化的三-$\zeta$ 基组。 |
    | *极小增强*（Truhlar 等人的方案[Zheng:2010iz](../../bibliography.md)） |  |  |  |
    | `ma-def-TZVP` | Fr--Lr | `def-ECP` (Fr--Lr) | 极小增强的 def-TZVP 基组。 |
    | *遗留定义（不推荐！）* |  |  |  |
    | `old-SV` | H--I | \-- |  |
    | `old-SV(P)` | H--I | \-- |  |
    | `old-SVP` | H--I | \-- |  |
    | `old-TZV` | H--I | \-- |  |
    | `old-TZV(P)` | H--I | \-- |  |
    | `old-TZVP` | H--I | \-- |  |
    | `old-TZVPP` | H--I | \-- |  |

<a id="sec:essentialelements.basisset.builtin.def2"></a>
### Karlsruhe def2 基组（Karlsruhe def2 Basis Sets）

Karlsruhe def2 家族的价层极化基组对元素 **H-Kr** 是全电子的，并对元素 **Rb-Rn** 自动加载 Stuttgart-Dresden [有效核势](#sec:essentialelements.basisset.ecps)。可用的 Karlsruhe def2 基组列于 [tab:essentialelements.basisset.builtin.def2](#tab:essentialelements.basisset.builtin.def2)。相对论重收缩变体见 [rel.def2](#sec:essentialelements.basisset.builtin.rel.def2) 的讨论。

<a id="tab:essentialelements.basisset.builtin.def2"></a>
!!! note "可用的 Karlsruhe def2 基组。"
    | Basis Set | Elem. | ECP | Comment |
    | --- | --- | --- | --- |
    | `def2-SVP` | H--Rn | `def2-ECP` (Rb--Rn) | 带极化的价层双-$\zeta$。 |
    | `def2-SV(P)` | H--Rn | `def2-ECP` (Rb--Rn) | 极化略微减弱的 `def2-SVP`。 |
    | `def2-TZVP` | H--Rn | `def2-ECP` (Rb--Rn) | 带极化的价层三-$\zeta$。与较早的 def-TZVPP（主族元素）和 TZVP（H）十分相似。 |
    | `def2-TZVP(-f)` | H--Rn | `def2-ECP` (Rb--Rn) | 去掉主族元素 f 极化的 `def2-TZVP`。 |
    | `def2-TZVPP` | H--Rn | `def2-ECP` (Rb--Rn) | 双重极化的价层三-$\zeta$。 |
    | `def2-QZVP` | H--Rn | `def2-ECP` (Rb--Rn) | 带极化的价层四-$\zeta$。 |
    | `def2-QZVPP` | H--Rn | `def2-ECP` (Rb--Rn) | 双重极化的价层四-$\zeta$。 |
    | *弥散*（Rappoport 等人[Rappoport:2010kr,Rappoport:2021ln](../../bibliography.md)） |  |  |  |
    | `def2-SVPD` | H--Rn | `def2-ECP` (Rb--Rn) | 用于性质计算的弥散 def2-SVP 基组 |
    | `def2-TZVPD` | H--Rn | `def2-ECP` (Rb--Rn) | 用于性质计算的弥散 def2-TZVP 基组 |
    | `def2-TZVPPD` | H--Rn | `def2-ECP` (Rb--Rn) | 用于性质计算的弥散 def2-TZVPP 基组 |
    | `def2-QZVPD` | H--Rn | `def2-ECP` (Rb--Rn) | 用于性质计算的弥散 def2-QZVP 基组 |
    | `def2-QZVPPD` | H--Rn | `def2-ECP` (Rb--Rn) | 用于性质计算的弥散 def2-QZVPP 基组 |
    | *极小增强*（Truhlar 等人的方案[Zheng:2010iz](../../bibliography.md)） |  |  |  |
    | `ma-def2-SVP` | H--Rn | `def2-ECP` (Rb--Rn) | 极小增强的 def2-SVP 基组。 |
    | `ma-def2-SV(P)` | H--Rn | `def2-ECP` (Rb--Rn) | 极小增强的 def2-SV(P) 基组。 |
    | `ma-def2-mSVP` | H--Rn | `def2-ECP` (Rb--Rn) | 极小增强的 def2-mSVP 基组。 |
    | `ma-def2-TZVP` | H--Rn | `def2-ECP` (Rb--Rn) | 极小增强的 def2-TZVP 基组。 |
    | `ma-def2-TZVP(-f)` | H--Rn | `def2-ECP` (Rb--Rn) | 极小增强的 def2-TZVP(-f) 基组。 |
    | `ma-def2-TZVPP` | H--Rn | `def2-ECP` (Rb--Rn) | 极小增强的 def2-TZVPP 基组。 |
    | `ma-def2-QZVPP` | H--Rn | `def2-ECP` (Rb--Rn) | 极小增强的 def2-QZVPP 基组。 |

<a id="sec:essentialelements.basisset.builtin.dhf"></a>
### Karlsruhe dhf 基组（Karlsruhe dhf Basis Sets）
这些基组由 def2-XVP 基组衍生而来，对 5s、6s、4d、5d 元素和碘做了小幅修改。[Weigend2010-dhf-XVP](../../bibliography.md) 它们是针对修正的 Dirac-Fock ECP（`dhf-ECP`）优化的，而非针对 Wood--Boring 型 ECP（`def2-ECP`）。对元素 H--Kr，这些基组等同于相应的 [def2-XVP](#sec:essentialelements.basisset.builtin.def2) 基组。也有面向二分量方法的版本，例如 `dhf-TZVP-2c`，**但这类方法目前尚未在 ORCA 中实现**。可用的 Karlsruhe dhf 基组列于 [tab:essentialelements.basisset.builtin.dhf](#tab:essentialelements.basisset.builtin.dhf)。

<a id="tab:essentialelements.basisset.builtin.dhf"></a>
!!! note "可用的 dhf 基组。"
    | Basis Set | Elem. | ECP | Comment |
    | --- | --- | --- | --- |
    | `dhf-SV(P)` | H--Rn | `dhf-ECP` (Rb--Rn) | 基于 def2-SV(P) |
    | `dhf-SVP` | H--Rn | `dhf-ECP` (Rb--Rn) | 基于 def2-SVP |
    | `dhf-TZVP` | H--Rn | `dhf-ECP` (Rb--Rn) | 基于 def2-TZVP |
    | `dhf-TZVPP` | H--Rn | `dhf-ECP` (Rb--Rn) | 基于 def2-TZVPP |
    | `dhf-QZVP` | H--Rn | `dhf-ECP` (Rb--Rn) | 基于 def2-QZVP |
    | `dhf-QZVPP` | H--Rn | `dhf-ECP` (Rb--Rn) | 基于 def2-QZVPP |
    | *二分量变体：* |  |  |  |
    | `dhf-SVP-2c` | H--Rn | `dhf-ECP-2c` (Rb--Rn) | 基于 def2-SVP |
    | `dhf-TZVP-2c` | H--Rn | `dhf-ECP-2c` (Rb--Rn) | 基于 def2-TZVP |
    | `dhf-TZVPP-2c` | H--Rn | `dhf-ECP-2c` (Rb--Rn) | 基于 def2-TZVPP |
    | `dhf-QZVP-2c` | H--Rn | `dhf-ECP-2c` (Rb--Rn) | 基于 def2-QZVP |
    | `dhf-QZVPP-2c` | H--Rn | `dhf-ECP-2c` (Rb--Rn) | 基于 def2-QZVPP |

<a id="sec:essentialelements.basisset.builtin.jensen"></a>
### Jensen 基组（Jensen Basis Sets）

Jensen 的极化一致一般收缩基组包含多种通用和专用变体。可用的 Jensen 基组列于
[tab:essentialelements.basisset.builtin.jensen](#tab:essentialelements.basisset.builtin.jensen)。[jensen2001a, jensen2002a, jensen2004a, jensen2007a, jensen2012a, jensen2014a, jensen2015a](../../bibliography.md)

<a id="tab:essentialelements.basisset.builtin.jensen"></a>
!!! note "可用的 Jensen 基组。"
    | Basis Set | Elem. | ECP | Comment |
    | --- | --- | --- | --- |
    | `pc-0` | H--Ca, Ga--Kr | \-- |  |
    | `pc-1` | H--Kr | \-- |  |
    | `pc-2` | H--Kr | \-- |  |
    | `pc-3` | H--Kr | \-- |  |
    | `pc-4` | H--Kr | \-- |  |
    | `aug-pc-0` | H--Ca, Ga--Kr | \-- | `pc-0` 用弥散函数增强 |
    | `aug-pc-1` | H--Kr | \-- | `pc-1` 用弥散函数增强 |
    | `aug-pc-2` | H--Kr | \-- | `pc-2` 用弥散函数增强 |
    | `aug-pc-3` | H--Kr | \-- | `pc-3` 用弥散函数增强 |
    | `aug-pc-4` | H--Kr | \-- | `pc-4` 用弥散函数增强 |
    | *分段收缩变体：* |  |  |  |
    | `pcseg-0` | H--Kr | \-- |  |
    | `pcseg-1` | H--Kr | \-- |  |
    | `pcseg-2` | H--Kr | \-- |  |
    | `pcseg-3` | H--Kr | \-- |  |
    | `pcseg-4` | H--Kr | \-- |  |
    | `aug-pcseg-0` | H--Kr | \-- | `pcseg-0` 用弥散函数增强 |
    | `aug-pcseg-1` | H--Kr | \-- | `pcseg-1` 用弥散函数增强 |
    | `aug-pcseg-2` | H--Kr | \-- | `pcseg-2` 用弥散函数增强 |
    | `aug-pcseg-3` | H--Kr | \-- | `pcseg-3` 用弥散函数增强 |
    | `aug-pcseg-4` | H--Kr | \-- | `pcseg-4` 用弥散函数增强 |
    | *针对核磁屏蔽优化：* |  |  |  |
    | `pcSseg-0` | H--Kr | \-- |  |
    | `pcSseg-1` | H--Kr | \-- |  |
    | `pcSseg-2` | H--Kr | \-- |  |
    | `pcSseg-3` | H--Kr | \-- |  |
    | `pcSseg-4` | H--Kr | \-- |  |
    | `aug-pcSseg-0` | H--Kr | \-- | `pcSseg-0` 用弥散函数增强 |
    | `aug-pcSseg-1` | H--Kr | \-- | `pcSseg-1` 用弥散函数增强 |
    | `aug-pcSseg-2` | H--Kr | \-- | `pcSseg-2` 用弥散函数增强 |
    | `aug-pcSseg-3` | H--Kr | \-- | `pcSseg-3` 用弥散函数增强 |
    | `aug-pcSseg-4` | H--Kr | \-- | `pcSseg-4` 用弥散函数增强 |
    | *Optimized for spin-spin coupling constants:* |  |  |  |
    | `pcJ-0` | H--He, B--Ne, Al--Ar | \-- |  |
    | `pcJ-1` | H--He, B--Ne, Al--Ar | \-- |  |
    | `pcJ-2` | H--He, B--Ne, Al--Ar | \-- |  |
    | `pcJ-3` | H--He, B--Ne, Al--Ar | \-- |  |
    | `pcJ-4` | H--He, B--Ne, Al--Ar | \-- |  |
    | `aug-pcJ-0` | H--He, B--Ne, Al--Ar | \-- | `pcJ-0` 用弥散函数增强 |
    | `aug-pcJ-1` | H--He, B--Ne, Al--Ar | \-- | `pcJ-1` 用弥散函数增强 |
    | `aug-pcJ-2` | H--He, B--Ne, Al--Ar | \-- | `pcJ-2` 用弥散函数增强 |
    | `aug-pcJ-3` | H--He, B--Ne, Al--Ar | \-- | `pcJ-3` 用弥散函数增强 |
    | `aug-pcJ-4` | H--He, B--Ne, Al--Ar | \-- | `pcJ-4` 用弥散函数增强 |
    | *针对超精细耦合常数优化：* |  |  |  |
    | `pcH-1` | H, He, B--Ne, Al--Ar | \-- |  |
    | `pcH-2` | H, He, B--Ne, Al--Ar | \-- |  |
    | `pcH-3` | H, He, B--Ne, Al--Ar | \-- |  |
    | `pcH-4` | H, He, B--Ne, Al--Ar | \-- |  |
    | `aug-pcH-1` | H, He, B--Ne, Al--Ar | \-- | `pcH-1` 用弥散函数增强 |
    | `aug-pcH-2` | H, He, B--Ne, Al--Ar | \-- | `pcH-2` 用弥散函数增强 |
    | `aug-pcH-3` | H, He, B--Ne, Al--Ar | \-- | `pcH-3` 用弥散函数增强 |
    | `aug-pcH-4` | H, He, B--Ne, Al--Ar | \-- | `pcH-4` 用弥散函数增强 |
    | *Optimized for core-spectroscopy:* |  |  |  |
    | `pcX-1` | Li--Ar | \-- |  |
    | `pcX-2` | Li--Ar | \-- |  |
    | `pcX-3` | Li--Ar | \-- |  |
    | `pcX-4` | Li--Ar | \-- |  |
    | `aug-pcX-1` | Li--Ar | \-- | `pcX-1` 用弥散函数增强 |
    | `aug-pcX-2` | Li--Ar | \-- | `pcX-2` 用弥散函数增强 |
    | `aug-pcX-3` | Li--Ar | \-- | `pcX-3` 用弥散函数增强 |
    | `aug-pcX-4` | Li--Ar | \-- | `pcX-4` 用弥散函数增强 |

<a id="sec:essentialelements.basisset.builtin.hgbs"></a>
### 类氢高斯基组（Hydrogenic Gaussian Basis Sets）

Lehtola 的类氢高斯基组（HGBS）是基于模拟真实原子和分子的单电子模型体系构建的、可广泛移植且精确的基组。
[lehtola2020hgbs](../../bibliography.md) 可用的 HGBS 基组列于 [tab:essentialelements.basisset.builtin.hgbs](#tab:essentialelements.basisset.builtin.hgbs)。

!!! note "HGBS 基组的命名约定（Naming convention of HGBS basis sets）"
    * $m$：表示能量优化阈值 $10^{-m}$
    * P$n$：表示极化壳层数目
    * $A$：表示显式地用弥散函数增强

<a id="tab:essentialelements.basisset.builtin.hgbs"></a>
!!! note "Karlsruhe HGBS、HGBSP、AHGBS 和 AHGBSP 基组。"
    | Basis Set | Elem. | ECP | Comment |
    | --- | --- | --- | --- |
    | `HGBS-5` | H--Og | \-- |  |
    | `HGBS-7` | H--Og | \-- |  |
    | `HGBS-9` | H--Og | \-- |  |
    | `HGBSP1-5` | H--Og | \-- | 极化变体 |
    | `HGBSP1-7` | H--Og | \-- |  |
    | `HGBSP1-9` | H--Og | \-- |  |
    | `HGBSP2-5` | H--Og | \-- |  |
    | `HGBSP2-7` | H--Og | \-- |  |
    | `HGBSP2-9` | H--Og | \-- |  |
    | `HGBSP3-5` | H--Og | \-- |  |
    | `HGBSP3-7` | H--Og | \-- |  |
    | `HGBSP3-9` | H--Og | \-- |  |
    | `AHGBS-5` | H--Og | \-- | 用弥散函数增强 |
    | `AHGBS-7` | H--Og | \-- |  |
    | `AHGBS-9` | H--Og | \-- |  |
    | `AHGBSP1-5` | H--Og | \-- | 用弥散函数增强的极化变体 |
    | `AHGBSP1-7` | H--Og | \-- |  |
    | `AHGBSP1-9` | H--Og | \-- |  |
    | `AHGBSP2-5` | H--Og | \-- |  |
    | `AHGBSP2-7` | H--Og | \-- |  |
    | `AHGBSP2-9` | H--Og | \-- |  |
    | `AHGBSP3-5` | H--Og | \-- |  |
    | `AHGBSP3-7` | H--Og | \-- |  |
    | `AHGBSP3-9` | H--Og | \-- |  |

<a id="sec:essentialelements.basisset.builtin.sapporo"></a>
### Sapporo 基组（Sapporo Basis Sets）

Sapporo 基组家族以日本札幌市命名，包含直至四-$\zeta$ 质量的分段收缩全电子高斯基组。[yamamoto1992sapporo,  noro2003sapporo, noro2012sapporo](../../bibliography.md) 它们是为相关波函数方法计算而开发的紧凑而精确的基组。也有针对标量相对论 DKH3 哈密顿量优化的变体。可用的 Sapporo 基组列于 [tab:essentialelements.basisset.builtin.sapporo](#tab:essentialelements.basisset.builtin.sapporo)。相对论变体见 [rel.sapporo](#sec:essentialelements.basisset.builtin.rel.sapporo) 的讨论。

<a id="tab:essentialelements.basisset.builtin.sapporo"></a>
!!! note "可用的 Sapporo 基组列表。"
    | Basis Set | Elem. | ECP | Comment |
    | --- | --- | --- | --- |
    | `Sapporo-DZP-2012` | H--Xe | \-- |  |
    | `Sapporo-TZP-2012` | H--Xe | \-- |  |
    | `Sapporo-QZP-2012` | H--Xe | \-- |  |

<a id="sec:essentialelements.basisset.builtin.partridge"></a>
### Partridge 基组（Partridge Basis Sets）

Partridge 家族的基组是未经收缩的 RHF 基态能量优化基组。[partridge1987chem, partridge1989chem](../../bibliography.md) 可用的 Partridge 基组列于 [tab:essentialelements.basisset.builtin.partridge](#tab:essentialelements.basisset.builtin.partridge)。

<a id="tab:essentialelements.basisset.builtin.partridge"></a>
!!! note "可用的 Partridge 基组。"
    | Basis Set | Elem. | ECP | Comment |
    | --- | --- | --- | --- |
    | `Partridge-1` | H, Li--Sr | \-- |  |
    | `Partridge-2` | H, Li--Kr | \-- |  |
    | `Partridge-3` | H, Li--Zn | \-- |  |
    | `Partridge-4` | Sc--Zn | \-- |  |

<a id="sec:essentialelements.basisset.builtin.crenb"></a>
### CRENB 基组（CRENB Basis Sets）

Christiansen-Ross-Ermler-Nash-Bursten（CRENB）基组和[有效核势](#sec:essentialelements.basisset.ecps)适用于大多数元素。[pacios1985crenbla, hurley1986crenblb, lajohn1987crenblc, ross1990crenbld, ross1994crenble, ermler1991crenblf, nash1997crenblg](../../bibliography.md) 注意，虽然这些 ECP 最初是为自旋-轨道耦合（SOC）相互作用设计的，**目前 ORCA 尚未实现带 ECP 的 SOC 计算**。可用的 CRENB 基组列于 [tab:essentialelements.basisset.builtin.crenb](#tab:essentialelements.basisset.builtin.crenb)。

<a id="tab:essentialelements.basisset.builtin.crenb"></a>
!!! note "可用的 CRENB 基组列表。"
    | Basis Set | Elem. | ECP | Comment |
    | --- | --- | --- | --- |
    | `CRENBL` | H, Li--Og | `CRENBL-ECP` (Li--Og) | 与*小*核 ECP 配合使用的*大*基组版本 |

<a id="sec:essentialelements.basisset.builtin.lanl"></a>
### LANL 基组（LANL Basis Sets）

Los Alamos 国家实验室（LANL）基组和[有效核势](#sec:essentialelements.basisset.ecps)最初由 Hay 和 Wadt 于 1985 年提出。[hay1985chem, wadt1985ecp, hay1985ecpb](../../bibliography.md) 后来又提出了极化变体[ehlers1993lanlf, check2001lanldp](../../bibliography.md)，Roy 等人进一步扩展了这些基组[roy2008chem](../../bibliography.md)。
可用的 LANL 基组列于 [tab:essentialelements.basisset.builtin.lanl](#tab:essentialelements.basisset.builtin.lanl)。

<a id="tab:essentialelements.basisset.builtin.lanl"></a>
!!! note "可用的 LANL 基组列表。"
    | Basis Set | Elem. | ECP | Comment |
    | --- | --- | --- | --- |
    | `LANL08` | Na--La, Hf--Bi | `HayWadt` (Na--La, Hf--Bi) | 未收缩 |
    | `LANL08(f)` | Sc--Cu, Y--Ag, La, Hf--Au | `HayWadt` (Sc--Cu, Y--Ag, La, Hf--Au) | 未收缩 + 极化 |
    | `LANL2DZ` | H, Li--La, Hf--Bi, U--Pu | `HayWadt` (Na--La, Hf--Bi, U--Pu) | 双-$\zeta$，H--Ne 用 D95V |
    | `LANL2TZ` | Sc--Zn, Y--Cd, La, Hf--Hg | `HayWadt` (Sc--Zn, Y--Cd, La, Hf--Hg) | 三-$\zeta$ |
    | `LANL2TZ(f)` | Sc--Cu, Y--Ag, La, Hf--Au | `HayWadt` (Sc--Cu, Y--Ag, La, Hf--Au) | 三-$\zeta$ + 极化 |

<a id="sec:essentialelements.basisset.builtin.cc"></a>
### 相关一致基组（Correlation-consistent Basis Sets）

相关一致基组由 Dunning 及其合作者开创，此后发展出众多变体。它们是相关波函数方法中应用最广泛的基组之一，尤其适合[基组外推](../modelchemistries/mdci.md#sec:modelchemistries.mdci.basissetextrapolation)。可用的相关一致基组列于 [tab:essentialelements.basisset.builtin.cc](#tab:essentialelements.basisset.builtin.cc)。相对论变体见 [rel.cc](#sec:essentialelements.basisset.builtin.rel.cc) 的讨论。

<a id="tab:essentialelements.basisset.builtin.cc"></a>
!!! note "可用的相关一致基组列表。"
    | Basis Set | Elem. | ECP | Comment |
    | --- | --- | --- | --- |
    | `cc-pVDZ` | H--Ar, Ca--Kr | \-- | Dunning 相关一致极化双-$\zeta$ |
    | `cc-pVTZ` | H--Ar, Ca--Kr, Y, Ag, Au | \-- | Dunning 相关一致极化三-$\zeta$ |
    | `cc-pVQZ` | H--Ar, Ca--Kr | \-- | Dunning 相关一致极化四-$\zeta$ |
    | `cc-pV5Z` | H--Ar, Ca--Kr | \-- | Dunning 相关一致极化五-$\zeta$ |
    | `cc-pV6Z` | H--He, Be--Ne, Al--Ar | \-- | Dunning 相关一致极化六-$\zeta$ |
    | `aug-cc-pVDZ` | H--Ar, Sc--Kr | \-- | `cc-pVDZ` 用弥散函数增强 |
    | `aug-cc-pVTZ` | H--Ar, Sc--Kr, Ag, Au | \-- | `cc-pVTZ` 用弥散函数增强 |
    | `aug-cc-pVQZ` | H--Ar, Sc--Kr | \-- | `cc-pVQZ` 用弥散函数增强 |
    | `aug-cc-pV5Z` | H--Ar, Sc--Kr | \-- | `cc-pV5Z` 用弥散函数增强 |
    | `aug-cc-pV6Z` | H--He, B--Ne, Al--Ar | \-- | `cc-pV6Z` 用弥散函数增强 |
    | *With tight d functions:* |  |  |  |
    | `cc-pVD(+d)Z` | Na--Ar | \-- |  |
    | `cc-pVT(+d)Z` | Na--Ar | \-- |  |
    | `cc-pVQ(+d)Z` | Na--Ar | \-- |  |
    | `cc-pV5(+d)Z` | Na--Ar | \-- |  |
    | `aug-cc-pVD(+d)Z` | Al--Ar | \-- | `cc-pVD(+d)Z` 用弥散函数增强 |
    | `aug-cc-pVT(+d)Z` | Al--Ar | \-- | `cc-pVT(+d)Z` 用弥散函数增强 |
    | `aug-cc-pVQ(+d)Z` | Al--Ar | \-- | `cc-pVQ(+d)Z` 用弥散函数增强 |
    | `aug-cc-pV5(+d)Z` | Al--Ar | \-- | `cc-pV5(+d)Z` 用弥散函数增强 |
    | `aug-cc-pV6(+d)Z` | Al--Ar | \-- | `cc-pV6(+d)Z` 用弥散函数增强 |
    | *按 Truhlar 等人[papajak2011](../../bibliography.md) 部分增强：* |  |  |  |
    | `apr-cc-pV(Q+d)Z` | H--Ar | \-- | 在 Li--Ca 上用 sp 弥散函数增强 |
    | `may-cc-pV(T+d)Z` | H--Ar | \-- | 在 Li--Ca 上用 sp 弥散函数增强 |
    | `may-cc-pV(Q+d)Z` | H--Ar | \-- | 在 Li--Ca 上用 spd 弥散函数增强 |
    | `jun-cc-pV(D+d)Z` | H--Ar | \-- | 在 Li--Ca 上用 sp 弥散函数增强 |
    | `jun-cc-pV(T+d)Z` | H--Ar | \-- | 在 Li--Ca 上用 spd 弥散函数增强 |
    | `jun-cc-pV(Q+d)Z` | H--Ar | \-- | 在 Li--Ca 上用 spdf 弥散函数增强 |
    | `jul-cc-pV(D+d)Z` | H--Ar | \-- | 在 Li--Ca 上用 spd 弥散函数增强 |
    | `jul-cc-pV(T+d)Z` | H--Ar | \-- | 在 Li--Ca 上用 spdf 弥散函数增强 |
    | `jul-cc-pV(Q+d)Z` | H--Ar | \-- | 在 Li--Ca 上用 spdfg 弥散函数增强 |
    | `maug-cc-pV(D+d)Z` | H--Ar | \-- | 等同于 `jun-cc-pV(D+d)Z` |
    | `maug-cc-pV(T+d)Z` | H--Ar | \-- | 等同于 `may-cc-pV(T+d)Z` |
    | `maug-cc-pV(Q+d)Z` | H--Ar | \-- | 等同于 `apr-cc-pV(Q+d)Z` |
    | *为核-价电子相关做核极化：* |  |  |  |
    | `cc-pCVDZ` | H--Ar, Ca, Ga--Kr | \-- | 对 H 和 He 等同于 `cc-pVDZ` |
    | `cc-pCVTZ` | H--Ar, Ca, Ga--Kr | \-- | 对 H 和 He 等同于 `cc-pVTZ` |
    | `cc-pCVQZ` | H--Ar, Ca, Ga--Kr | \-- | 对 H 和 He 等同于 `cc-pVQZ` |
    | `cc-pCV5Z` | H--Ar, Ca, Ga--Kr | \-- | 对 H 和 He 等同于 `cc-pV5Z` |
    | `cc-pCV6Z` | H--He, B--Ne, Al--Ar | \-- | 对 H 和 He 等同于 `cc-pV6Z` |
    | `aug-cc-pCVDZ` | H--Ar, Ga--Kr | \-- | `cc-pCVDZ` 用弥散函数增强，对 H 和 He 等同于 `aug-cc-pVDZ` |
    | `aug-cc-pCVTZ` | H--Ar, Ga--Kr | \-- | `cc-pCVTZ` 用弥散函数增强，对 H 和 He 等同于 `aug-cc-pVTZ` |
    | `aug-cc-pCVQZ` | H--Ar, Ga--Kr | \-- | `cc-pCVQZ` 用弥散函数增强，对 H 和 He 等同于 `aug-cc-pVQZ` |
    | `aug-cc-pCV5Z` | H--Ar, Ga--Kr | \-- | `cc-pCV5Z` 用弥散函数增强，对 H 和 He 等同于 `aug-cc-pV5Z` |
    | `aug-cc-pCV6Z` | H--He, B--Ne, Al--Ar | \-- | `cc-pCV6Z` 用弥散函数增强，对 H 和 He 等同于 `aug-cc-pV6Z` |
    | *用加权核函数做核极化*： |  |  |  |
    | `cc-pwCVDZ` | H--Ar, Ca, Ga--Kr | \-- | 对 H 和 He 等同于 `cc-pVDZ` |
    | `cc-pwCVTZ` | H--Ar, Ca--Kr, Ag, Au | \-- | 对 H 和 He 等同于 `cc-pVTZ` |
    | `cc-pwCVQZ` | H--Ar, Ca--Kr | \-- | 对 H 和 He 等同于 `cc-pVQZ` |
    | `cc-pwCV5Z` | H--Ar, Ca--Kr | \-- | 对 H 和 He 等同于 `cc-pV5Z` |
    | `aug-cc-pwCVDZ` | H--Ar, Ga--Kr | \-- | `cc-pwCVDZ` 用弥散函数增强，对 H 和 He 等同于 `aug-cc-pVDZ` |
    | `aug-cc-pwCVTZ` | H--Ar, Sc--Kr, Ag, Au | \-- | `cc-pwCVTZ` 用弥散函数增强，对 H 和 He 等同于 `aug-cc-pVTZ` |
    | `aug-cc-pwCVQZ` | H--Ar, Sc--Kr | \-- | `cc-pwCVQZ` 用弥散函数增强，对 H 和 He 等同于 `aug-cc-pVQZ` |
    | `aug-cc-pwCV5Z` | H--Ar, Sc--Kr | \-- | `cc-pwCV5Z` 用弥散函数增强，对 H 和 He 等同于 `aug-cc-pV5Z` |
    | *Pseudo-potential (ECP) variants:* |  |  |  |
    | `cc-pVDZ-PP` | Ca, Cu--Kr, Sr--Xe, Ba, Hf--Rn, Ra, U | `SK-MCDHF-RSC` (Ca, Cu--Kr, Sr--Xe, Ba, Hf--Ra, U) |  |
    | `cc-pVTZ-PP` | Ca, Cu--Kr, Sr--Xe, Ba, Hf--Rn, Ra, U | `SK-MCDHF-RSC` (Ca, Cu--Kr, Sr--Xe, Ba, Hf--Ra, U) |  |
    | `cc-pVQZ-PP` | Ca, Cu--Kr, Sr--Xe, Ba, Hf--Rn, Ra, U | `SK-MCDHF-RSC` (Ca, Cu--Kr, Sr--Xe, Ba, Hf--Ra, U) |  |
    | `cc-pV5Z-PP` | Ca, Cu--Kr, Sr--Xe, Ba, Hf--Rn, Ra | `SK-MCDHF-RSC` (Ca, Cu--Kr, Sr--Xe, Ba, Hf--Ra, U) |  |
    | `aug-cc-pVDZ-PP` | Ca, Cu--Kr, Sr--Xe, Ba, Hf--Rn, Ra | `SK-MCDHF-RSC` (Ca, Cu--Kr, Sr--Xe, Ba, Hf--Ra, U) | `cc-pVDZ-PP` 用弥散函数增强 |
    | `aug-cc-pVTZ-PP` | Ca, Cu--Kr, Sr--Xe, Ba, Hf--Rn, Ra | `SK-MCDHF-RSC` (Ca, Cu--Kr, Sr--Xe, Ba, Hf--Ra, U) | `cc-pVTZ-PP` 用弥散函数增强 |
    | `aug-cc-pVQZ-PP` | Ca, Cu--Kr, Sr--Xe, Ba, Hf--Rn, Ra | `SK-MCDHF-RSC` (Ca, Cu--Kr, Sr--Xe, Ba, Hf--Ra, U) | `cc-pVQZ-PP` 用弥散函数增强 |
    | `aug-cc-pV5Z-PP` | Ca, Cu--Kr, Sr--Xe, Ba, Hf--Rn, Ra | `SK-MCDHF-RSC` (Ca, Cu--Kr, Sr--Xe, Ba, Hf--Ra, U) | `cc-pV5Z-PP` 用弥散函数增强 |
    | `cc-pCVDZ-PP` | Ca, Sr, Ba, Ra | `SK-MCDHF-RSC` (Ca, Sr, Ba, Ra) |  |
    | `cc-pCVTZ-PP` | Ca, Sr, Ba, Ra | `SK-MCDHF-RSC` (Ca, Sr, Ba, Ra) |  |
    | `cc-pCVQZ-PP` | Ca, Sr, Ba, Ra | `SK-MCDHF-RSC` (Ca, Sr, Ba, Ra) |  |
    | `cc-pCV5Z-PP` | Ca, Sr, Ba, Ra | `SK-MCDHF-RSC` (Ca, Sr, Ba, Ra) |  |
    | `aug-cc-pCVDZ-PP` | Ca, Sr, Ba, Ra | `SK-MCDHF-RSC` (Ca, Sr, Ba, Ra) | `cc-pCVDZ-PP` 用弥散函数增强 |
    | `aug-cc-pCVTZ-PP` | Ca, Sr, Ba, Ra | `SK-MCDHF-RSC` (Ca, Sr, Ba, Ra) | `cc-pCVTZ-PP` 用弥散函数增强 |
    | `aug-cc-pCVQZ-PP` | Ca, Sr, Ba, Ra | `SK-MCDHF-RSC` (Ca, Sr, Ba, Ra) | `cc-pCVQZ-PP` 用弥散函数增强 |
    | `aug-cc-pCV5Z-PP` | Ca, Sr, Ba, Ra | `SK-MCDHF-RSC` (Ca, Sr, Ba, Ra) | `cc-pCV5Z-PP` 用弥散函数增强 |
    | `cc-pwCVDZ-PP` | Ca, Cu--Kr, Sr--Xe, Ba, Hf--Rn, Ra, U | `SK-MCDHF-RSC` (Ca, Cu--Kr, Sr--Xe, Ba, Hf--Ra, U) |  |
    | `cc-pwCVTZ-PP` | Ca, Cu--Kr, Sr--Xe, Ba, Hf--Rn, Ra, U | `SK-MCDHF-RSC` (Ca, Cu--Kr, Sr--Xe, Ba, Hf--Ra, U) |  |
    | `cc-pwCVQZ-PP` | Ca, Cu--Kr, Sr--Xe, Ba, Hf--Rn, Ra, U | `SK-MCDHF-RSC` (Ca, Cu--Kr, Sr--Xe, Ba, Hf--Ra, U) |  |
    | `cc-pwCV5Z-PP` | Ca, Cu--Kr, Sr--Xe, Ba, Hf--Rn, Ra | `SK-MCDHF-RSC` (Ca, Cu--Kr, Sr--Xe, Ba, Hf--Ra, U) |  |
    | `aug-cc-pwCVDZ-PP` | Ca, Cu--Kr, Sr--Xe, Ba, Hf--Rn, Ra | `SK-MCDHF-RSC` (Ca, Cu--Kr, Sr--Xe, Ba, Hf--Ra, U) | `cc-pwCVDZ-PP` 用弥散函数增强 |
    | `aug-cc-pwCVTZ-PP` | Ca, Cu--Kr, Sr--Xe, Ba, Hf--Rn, Ra | `SK-MCDHF-RSC` (Ca, Cu--Kr, Sr--Xe, Ba, Hf--Ra, U) | `cc-pwCVTZ-PP` 用弥散函数增强 |
    | `aug-cc-pwCVQZ-PP` | Ca, Cu--Kr, Sr--Xe, Ba, Hf--Rn, Ra | `SK-MCDHF-RSC` (Ca, Cu--Kr, Sr--Xe, Ba, Hf--Ra, U) | `cc-pwCVQZ-PP` 用弥散函数增强 |
    | `aug-cc-pwCV5Z-PP` | Ca, Cu--Kr, Sr--Xe, Ba, Hf--Rn, Ra | `SK-MCDHF-RSC` (Ca, Cu--Kr, Sr--Xe, Ba, Hf--Ra, U) | `cc-pwCV5Z-PP` 用弥散函数增强 |
    | *针对超精细耦合常数优化：* |  |  |  |
    | `aug-cc-pVTZ-J` | H, B--F, Al--Cl, Sc--Zn, Se | \-- | Sauer 的精确超精细耦合基组 |
    | *W4 theory:* |  |  |  |
    | `haV(T+d)Z` | H--Ar | \-- | `cc-pVTZ` (H--Be, Na, Mg), `aug-cc-pVTZ` (B--Ne), `aug-cc-pVT(+d)Z` (Al--Ar) |
    | `haV(Q+d)Z` | H--Ar | \-- | `cc-pVQZ` (H--Be, Na, Mg), `aug-cc-pVQZ` (B--Ne), `aug-cc-pVQ(+d)Z` (Al--Ar) |
    | `haV(5+d)Z` | H--Ar | \-- | `cc-pV5Z` (H--Be, Na, Mg), `aug-cc-pV5Z` (B--Ne), `aug-cc-pV5(+d)Z` (Al--Ar) |

<a id="sec:essentialelements.basisset.builtin.f12"></a>
### F12 基组（F12 Basis Sets）

[F12 计算](../modelchemistries/mdci.md#sec:modelchemistries.mdci.expcorrelation)专用的轨道基组（比常规的 D、T、Q-$\zeta$ 基组更大！）。
可用的 F12 基组列于 [tab:essentialelements.basisset.builtin.f12](#tab:essentialelements.basisset.builtin.f12)。
所需的互补辅助基组（CABS）见 [tab:essentialelements.basisset.aux.cabs](#tab:essentialelements.basisset.aux.cabs)。

<a id="tab:essentialelements.basisset.builtin.f12"></a>
!!! note "F12 基组。"
    | Basis Set | Elem. | ECP | Comment |
    | --- | --- | --- | --- |
    | `cc-pVDZ-F12` | H--Ar | \-- |  |
    | `cc-pVTZ-F12` | H--Ar | \-- |  |
    | `cc-pVQZ-F12` | H--Ar | \-- |  |
    | *Core-polarized:* |  |  |  |
    | `cc-pCVDZ-F12` | Li--Ar | \-- |  |
    | `cc-pCVTZ-F12` | Li--Ar | \-- |  |
    | `cc-pCVQZ-F12` | Li--Ar | \-- |  |
    | *Pseudo-potential (ECP) variants:* |  |  |  |
    | `cc-pVDZ-PP-F12` | Ga--Kr, In--Xe, Tl--Rn | `SK-MCDHF-RSC` (Ga--Kr, In--Xe, Tl--Rn) |  |
    | `cc-pVTZ-PP-F12` | Ga--Kr, In--Xe, Tl--Rn | `SK-MCDHF-RSC` (Ga--Kr, In--Xe, Tl--Rn) |  |
    | `cc-pVQZ-PP-F12` | Ga--Kr, In--Xe, Tl--Rn | `SK-MCDHF-RSC` (Ga--Kr, In--Xe, Tl--Rn) |  |

<a id="sec:essentialelements.basisset.builtin.ano"></a>
### 原子自然轨道基组（Atomic Natural Orbital Basis Sets）

原子自然轨道是一类特殊的基组。它们由能对角化球对称相关原子密度的正交归一轨道集表示。其思想是把尽可能多的信息放入每个基函数中，从而在给定基函数数目下获得尽可能好的结果。这对相关计算尤为重要，因为此时原始函数的数目远不如基函数的数目关键。ORCA 基于 cc-pV6Z（缺失时用 pc-4）原始函数提供了一些 ANO 基组。[neese2011jctc](../../bibliography.md) 这些基组非常精确，在相同基函数数目下明显优于 cc-pV$n$Z 对应基组（但原始函数数目多得多）。可用的 ANO 基组列于 [tab:essentialelements.basisset.builtin.ano](#tab:essentialelements.basisset.builtin.ano)。

!!! note "注意"
    * **aug-ANO-pV$n$Z：** 用 spd、spdf、spdfg 极化函数集完全增强。其代价几乎与高一级基组相同。实际上 aug-ANO-pV$n$Z $=$ ANO-pV($n+1$)Z 去掉最高角动量极化函数。
    * **saug-ANO-pV$n$Z：** 用单组 sp 函数增强。大幅提高 SCF 能量的精度，但对相关能无效。

<a id="tab:essentialelements.basisset.builtin.ano"></a>
!!! note "可用的原子自然轨道（ANO）基组。"
    | Basis Set | Elem. | ECP | Comment |
    | --- | --- | --- | --- |
    | `ANO-SZ` | H--Ar, Sc--Zn | \-- |  |
    | `ANO-pVDZ` | H--Ar, Sc--Zn | \-- |  |
    | `ANO-pVTZ` | H--Ar, Sc--Zn | \-- |  |
    | `ANO-pVQZ` | H--Ar, Sc--Zn | \-- |  |
    | `ANO-pV5Z` | H--Ar, Sc--Zn | \-- |  |
    | `ANO-pV6Z` | H--Ar, Sc--Zn | \-- |  |
    | `aug-ANO-pVDZ` | H--Ar, Sc--Zn | \-- | `ANO-pVDZ` 用弥散函数增强 |
    | `aug-ANO-pVTZ` | H--Ar, Sc--Zn | \-- | `ANO-pVTZ` 用弥散函数增强 |
    | `aug-ANO-pVQZ` | H--Ar, Sc--Zn | \-- | `ANO-pVQZ` 用弥散函数增强 |
    | `aug-ANO-pV5Z` | H--Ar, Sc--Zn | \-- | `ANO-pV5Z` 用弥散函数增强 |
    | `saug-ANO-pVDZ` | H--Ar, Sc--Zn | \-- | `ANO-pVDZ` 用一组弥散 sp 函数增强 |
    | `saug-ANO-pVTZ` | H--Ar, Sc--Zn | \-- | `ANO-pVTZ` 用一组弥散 sp 函数增强 |
    | `saug-ANO-pVQZ` | H--Ar, Sc--Zn | \-- | `ANO-pVQZ` 用一组弥散 sp 函数增强 |
    | `saug-ANO-pV5Z` | H--Ar, Sc--Zn | \-- | `ANO-pV5Z` 用一组弥散 sp 函数增强 |

<a id="sec:essentialelements.basisset.builtin.ano.efficient"></a>
#### 使用 ANO 基组的高效计算（Efficient Calculations with ANO Basis Sets）

通常 ANO 基组是"一般收缩"的，这意味着对
任何给定的角动量，所有原始函数都对所有基函数有贡献。
由于 ANO 的概念只有在底层原始函数集足够大时才有意义，
计算很容易变得非常昂贵，除非在积分求值
算法中采取特殊措施。ORCA 为 ANO 基组提供了特殊算法，
并为非相对论计算提供了精确的 ANO 基组。然而，
即便如此，积分求值仍然十分昂贵，只有把所有积分
存储在磁盘上并按需重复使用，
才能实现高效率。

目前 ANO 的使用仅限于[内置 ANO 基组](tab:essentialelements.basisset.builtin.ano)。它们建立在 cc-pV6Z 原始函数之上，因此
计算需要相当长的时间。

!!! tip "提示"
    不建议用 ANO 进行几何优化；它们会*非常*低效。

推荐按以下方式使用 ANO：

```orcainput
! ano-pVTZ Conv TightSCF CCSD(T)
%maxcore 2000 
* int 0 1
C  0 0 0    0   0   0
O  1 0 0  1.2   0   0
H  1 2 0  1.1 120   0
H  1 2 3  1.1 120 180
*
```

这给出：

```orca
ano-pVTZ:
E(SCF) = -113.920388785
E(corr)=   -0.427730189
```

与 cc-pVTZ 的数值比较：

```orca
cc-pVTZ:
E(SCF) = -113.911870901
E(corr)=   -0.421354947
```

因此，基于 ANO 的 SCF 能量比同规模的 cc 基组低约 8--9 mEh，相关能
几乎低 2 mEh。
通常 ANO 的结果比 cc 结果更接近基组极限。
此外，ANO 数值的外推表现非常好（见章节
[mdci.basissetextrapolation](../modelchemistries/mdci.md#sec:modelchemistries.mdci.basissetextrapolation)）

重要的是，本任务中所有积分都被存储下来。取决于你的
体系和耐心，这在 300--500 个基函数以内是可行的。
ORCA 的相关模块已重写，能够高效处理这些
存储的积分。因此，我们本来也可以使用
本来也可以使用 `! MO-CCSD(T) ` 或 `! AO-CCSD(T) `，两者都会表现良好。

然而，生成和存储所有四指标积分的负担
很快会变得相当沉重。因此，ANO 基组与 RI-JK 技术
的组合特别强大和高效。例如：

```orca
! ano-pVTZ cc-pVTZ/JK RI-JK Conv TightSCF RI-CCSD(T)
```

对 SCF 而言这非常有效，可以高效地进行大得多的基于 ANO 的
计算。RI-MP2 也可以用这种方式高效完成。
然而对于 CCSD(T) 这类更高阶的相关方法，
合乎逻辑的选择是 RI-CCSD(T)，但它明显比基于 AO 或 MO 的
CCSD(T) 效率低（大约慢两倍）。
因此 ORCA 实现了一种混合方法，用 RI 近似
来生成所有四指标积分。这通过
"RI-AO" 关键字完成：

```orca
! ano-pVTZ cc-pVTZ/JK RI-AO Conv TightSCF AO-CCSD(T)
```

在这种情况下 AO-CCSD(T) 或 MO-CCSD(T) 都会工作良好。当然这
并不能解决四指标积分的存储瓶颈。
如果这成为真正的问题，就必须使用 RI-CCSD(T)。
在本例中总能量的误差小于 0.1 mEh。

!!! warning "警告"
    在常规 RI 计算中无法使用第二个拟合基组，否则会得到不一致的结果。因此请只使用一个辅助基组！

<a id="sec:essentialelements.basisset.builtin.misc"></a>
### 其他与专用基组（Miscellaneous and Specialized Basis Sets）

更多可用的专用与其他基组列于 [tab:essentialelements.basisset.builtin.misc](#tab:essentialelements.basisset.builtin.misc)。

<a id="tab:essentialelements.basisset.builtin.misc"></a>
!!! note "可用的其他与专用基组汇总。"
    | Basis Set | Elem. | ECP | Comment |
    | --- | --- | --- | --- |
    | `D95` | H, Li, B--Ne, Al--Cl | \-- | Dunning's double-$\zeta$ basis set |
    | `D95p` | H, Li, B--Ne, Al--Cl | \-- | `D95` 的极化版本 |
    | `EPR-II` | H, B--F | \-- | Barone 的 EPR 计算用双-$\zeta$ 基组 |
    | `EPR-III` | H, B--F | \-- | Barone 的 EPR 计算用三-$\zeta$ 基组 |
    | `IGLO-II` | H, B--F, Al--Cl | \-- | Kutzelnigg 的 NMR 与 EPR 计算基组。 |
    | `IGLO-III` | H, B--F, Al--Cl | \-- | Kutzelnigg 的更大 NMR 与 EPR 计算基组。 |
    | `UGBS` | H--Th, Pu--Am, Cf--Lr | \-- | 通用高斯基组。 |
    | `CP` | Sc--Zn | \-- |  |
    | `CP(PPP)` | Sc--Zn | \-- |  |
    | `Wachters+f` | Sc--Cu | \-- |  |
    | `W1-mtsmall` | H--Ar | \-- | W1 理论基组 |
    | `W1-DZ` | H--Ar | \-- | W1 理论基组 |
    | `W1-TZ` | H--Ar | \-- | W1 理论基组 |
    | `W1-QZ` | H--Ar | \-- | W1 理论基组 |
    | `W1-Opt` | H--Ar | \-- | W1 理论基组 |
    | `MINI` | H--Ca | \-- | Huzinaga 的极小基组。 |
    | `MINIS` | H--Ca | \-- | MINI 的标度版本 |
    | `MIDI` | H--Na, Al--K | \-- | Huzinaga 的价层双-$\zeta$ 基组 |
    | `MINIX` | H--Lr | `def-ECP` (Rb--Lr) | Grimme 的小基组组合（见 [tab:modelchemistries.3cmethods.minix](#tab:modelchemistries.3cmethods.minix)）。用于 [HF-3c](../modelchemistries/3cmethods.md#sec:modelchemistries.3cmethods.hf3c). |
    | `def2-mSVP` | H--Lr | `def2-ECP` (Rb--Rn), `def-ECP` (Fr--Lr) | Used in [PBEh-3c](../modelchemistries/3cmethods.md#sec:modelchemistries.3cmethods.pbeh3c) and [B3LYP-3c](../modelchemistries/3cmethods.md#sec:modelchemistries.3cmethods.b3lyp3c) |
    | `def2-mTZVP` | H--Lr | `def2-ECP` (Rb--Rn), `def-ECP` (Fr--Lr) | Used in [B97-3c](../modelchemistries/3cmethods.md#sec:modelchemistries.3cmethods.b973c) |
    | `def2-mTZVPP` | H--Lr | `def2-ECP` (Rb--Rn), `def-ECP` (Fr--Lr) | Used in [r²SCAN-3c](../modelchemistries/3cmethods.md#sec:modelchemistries.3cmethods.r2scan3c) |
    | `vDZP` | H--Rn | `vDZP-ECP` (B--Rn) | Grimme 等人针对分子优化的极化价层双-$\zeta$ 基组。用于 [$\omega$B97X-3c](../modelchemistries/3cmethods.md#sec:modelchemistries.3cmethods.wb97x3c).[grimme2022wb97x3c](../../bibliography.md) |

<a id="sec:essentialelements.basisset.builtin.rel"></a>
## 相对论基组（Relativistic Basis Sets）

采用 [DKH](relativistic.md#sec:essentialelements.relativistic.dkh)、[ZORA](relativistic.md#sec:essentialelements.relativistic.zora) 或 [X2C](relativistic.md#sec:essentialelements.relativistic.x2c) 方法的标量相对论计算通常需要专门优化或重收缩的基组——详见 [relativistic.basissets](relativistic.md#sec:essentialelements.relativistic.basissets)。ORCA 为这类计算提供了多种合适的基组，如重收缩的 [Karlsruhe](#sec:essentialelements.basisset.builtin.rel.def2)、[SARC](#sec:essentialelements.basisset.builtin.rel.sarc) 和 [SARC2](#sec:essentialelements.basisset.builtin.rel.sarc2) 基组，以及多种优化的全电子[相关一致](#sec:essentialelements.basisset.builtin.rel.cc)基组。合适的辅助基组选项（如 `SARC/J` 或 `AutoAux`）见 [basisset.aux](#sec:essentialelements.basisset.aux)。

<a id="sec:essentialelements.basisset.builtin.rel.ahlrichs"></a>
### 重收缩 Ahlrichs 基组（Recontracted Ahlrichs Basis Sets）

原始 Ahlrichs 基组的可用相对论重收缩变体列于 [tab:essentialelements.basisset.builtin.rel.ahlrichs](#tab:essentialelements.basisset.builtin.rel.ahlrichs)。
关于带 "old-" 前缀的遗留定义的由来，参见章节 [builtin.ahlrichs](#sec:essentialelements.basisset.builtin.ahlrichs)。

<a id="tab:essentialelements.basisset.builtin.rel.ahlrichs"></a>
!!! note "相对论重收缩的 Ahlrichs 基组。RH = 相对论哈密顿量。"
    | Basis Set | Elem. | RH | Comment |
    | --- | --- | --- | --- |
    | `DKH-SV(P)` | H–Kr | DKH2 |  |
    | `DKH-SVP` | H–Kr | DKH2 |  |
    | `DKH-TZV(P)` | H–Kr | DKH2 |  |
    | `DKH-TZVP` | H–Kr | DKH2 |  |
    | `DKH-TZVPP` | H–Kr | DKH2 |  |
    | `DKH-QZVP` | H–Kr | DKH2 |  |
    | `DKH-QZVPP` | H–Kr | DKH2 |  |
    | `ZORA-SV(P)` | H–Kr | ZORA |  |
    | `ZORA-SVP` | H–Kr | ZORA |  |
    | `ZORA-TZV(P)` | H–Kr | ZORA |  |
    | `ZORA-TZVP` | H–Kr | ZORA |  |
    | `ZORA-TZVPP` | H–Kr | ZORA |  |
    | `ZORA-QZVP` | H–Kr | ZORA |  |
    | `ZORA-QZVPP` | H–Kr | ZORA |  |
    | *遗留定义（不推荐！）* |  |  |  |
    | `old-DKH-SV(P)` | H--I | DKH2 |  |
    | `old-DKH-SVP` | H--I | DKH2 |  |
    | `old-DKH-TZV(P)` | H--I | DKH2 |  |
    | `old-DKH-TZVP` | H--I | DKH2 |  |
    | `old-DKH-TZVPP` | H--I | DKH2 |  |
    | `old-ZORA-SV(P)` | H--I | ZORA |  |
    | `old-ZORA-SVP` | H--I | ZORA |  |
    | `old-ZORA-TZV(P)` | H--I | ZORA |  |
    | `old-ZORA-TZVP` | H--I | ZORA |  |
    | `old-ZORA-TZVPP` | H--I | ZORA |  |

<a id="sec:essentialelements.basisset.builtin.rel.def2"></a>
### 重收缩 Karlsruhe def2 基组（Recontracted Karlsruhe def2 Basis Sets）

def2 基组可用的改编 [DKH](relativistic.md#sec:essentialelements.relativistic.dkh) 和 [ZORA](relativistic.md#sec:essentialelements.relativistic.zora) 版本（即用于全电子 def2 基组的版本）列于 [tab:essentialelements.basisset.builtin.rel.def2](#tab:essentialelements.basisset.builtin.rel.def2)。这些基组保留原始的 def2 指数，但每个角动量只有一个收缩函数（因此略大），其收缩系数适用于相应的标量相对论哈密顿量。对于更重的元素，这些基组可以与 [SARC](#sec:essentialelements.basisset.builtin.rel.sarc) 和 [SARC2](#sec:essentialelements.basisset.builtin.rel.sarc2) 基组合用。

<a id="tab:essentialelements.basisset.builtin.rel.def2"></a>
!!! note "相对论重收缩的 Karlsruhe 基组。RH = 相对论哈密顿量。"
    | Basis Set | Elem. | RH | Comment |
    | --- | --- | --- | --- |
    | `DKH-def2-SVP` | H--Kr | DKH2 |  |
    | `DKH-def2-SV(P)` | H--Kr | DKH2 |  |
    | `DKH-def2-TZVP` | H--Kr | DKH2 |  |
    | `DKH-def2-TZVP(-f)` | H--Kr | DKH2 |  |
    | `DKH-def2-TZVPP` | H--Kr | DKH2 |  |
    | `DKH-def2-QZVPP` | H--Kr | DKH2 |  |
    | `ZORA-def2-SVP` | H--Kr | ZORA |  |
    | `ZORA-def2-SV(P)` | H--Kr | ZORA |  |
    | `ZORA-def2-TZVP` | H--Kr | ZORA |  |
    | `ZORA-def2-TZVP(-f)` | H--Kr | ZORA |  |
    | `ZORA-def2-TZVPP` | H--Kr | ZORA |  |
    | `ZORA-def2-QZVPP` | H--Kr | ZORA |  |
    | *极小增强*（Truhlar 等人的方案[Zheng:2010iz](../../bibliography.md)） |  |  |  |
    | `ma-DKH-def2-SVP` | H--Kr | DKH2 |  |
    | `ma-DKH-def2-SV(P)` | H--Kr | DKH2 |  |
    | `ma-DKH-def2-TZVP` | H--Kr | DKH2 |  |
    | `ma-DKH-def2-TZVP(-f)` | H--Kr | DKH2 |  |
    | `ma-DKH-def2-TZVPP` | H--Kr | DKH2 |  |
    | `ma-DKH-def2-QZVPP` | H--Kr | DKH2 |  |
    | `ma-ZORA-def2-SVP` | H--Kr | ZORA |  |
    | `ma-ZORA-def2-SV(P)` | H--Kr | ZORA |  |
    | `ma-ZORA-def2-TZVP` | H--Kr | ZORA |  |
    | `ma-ZORA-def2-TZVP(-f)` | H--Kr | ZORA |  |
    | `ma-ZORA-def2-TZVPP` | H--Kr | ZORA |  |
    | `ma-ZORA-def2-QZVPP` | H--Kr | ZORA |  |

<a id="sec:essentialelements.basisset.builtin.rel.sarc"></a>
### SARC 基组（SARC Basis Sets）

用于 DKH2 和 ZORA 哈密顿量的分段全电子相对论收缩（SARC）基组。[Pantazis2008,Buehl2008,Pantazis2009,Pantazis2011,Pantazis2012,Rolfes2020](../../bibliography.md) 可用的 SARC 基组列于 [tab:essentialelements.basisset.builtin.rel.sarc](#tab:essentialelements.basisset.builtin.rel.sarc)。

!!! tip "提示"
    特别对于镧系体系的波函数计算，我们推荐极化更强的 [SARC2 基组](#sec:essentialelements.basisset.builtin.rel.sarc) [aravenaSARC2](../../bibliography.md)。

<a id="tab:essentialelements.basisset.builtin.rel.sarc"></a>
!!! note "相对论 SARC 基组。RH = 相对论哈密顿量。"
    | Basis Set | Elem. | RH | Comment |
    | --- | --- | --- | --- |
    | `SARC-DKH-SVP` | Hf--Hg | DKH2 |  |
    | `SARC-DKH-TZVP` | Rb--Rn, Ac--Lr | DKH2 |  |
    | `SARC-DKH-TZVPP` | Rb--Rn, Ac--Lr | DKH2 |  |
    | `SARC-ZORA-SVP` | Hf--Hg | ZORA |  |
    | `SARC-ZORA-TZVP` | Rb--Rn, Ac--Lr | ZORA |  |
    | `SARC-ZORA-TZVPP` | Rb--Rn, Ac--Lr | ZORA |  |

!!! note "注意"
    *SARC/J 是所有 SARC 轨道基组的通用库仑拟合辅助基。*

<a id="sec:essentialelements.basisset.builtin.rel.sarc2"></a>
### SARC2 基组（SARC2 Basis Sets）

面向镧系元素的价层四-ζ 质量 SARC 基组，带 NEVPT2 优化的 (3g2h) 极化函数（SARC2）。[aravenaSARC2](../../bibliography.md) 适合用相关波函数方法进行精确计算。可用的 SARC2 基组列于 [tab:essentialelements.basisset.builtin.rel.sarc2](#tab:essentialelements.basisset.builtin.rel.sarc2)。

<a id="tab:essentialelements.basisset.builtin.rel.sarc2"></a>
!!! note "相对论 SARC2 基组。RH = 相对论哈密顿量。"
    | Basis Set | Elem. | ECP | Comment |
    | --- | --- | --- | --- |
    | `SARC2-DKH-QZV` | La--Lu | DKH2 |  |
    | `SARC2-DKH-QZVP` | La--Lu | DKH2 |  |
    | `SARC2-ZORA-QZV` | La--Lu | ZORA |  |
    | `SARC2-ZORA-QZVP` | La--Lu | ZORA |  |

!!! note "注意"
    每个基组都有一个专用的大型 /JK 辅助基组，用于同时进行库仑与交换拟合（参见 [tab:essentialelements.basisset.aux.auxjk](#tab:essentialelements.basisset.aux.auxjk)）。

<a id="sec:essentialelements.basisset.builtin.rel.karlsruhex2c"></a>
### Karlsruhe x2c 基组（Karlsruhe x2c Basis Sets）

对于 X2C 哈密顿量的计算，有直至 Rn 的全电子基组可供使用。[Weigend2017-x2c-XVP](../../bibliography.md) "-s" 变体（例如 `x2c-TZVPall-s`）用额外的紧缩函数增强，用于 NMR 屏蔽常数计算。[Weigend2019-x2c-XVP-s](../../bibliography.md) "-2c" 变体（例如 `x2c-TZVPall-2c`）用于包含自旋-轨道耦合的二分量计算（**注意二分量计算尚未在 *ORCA* 中实现**）。该家族可用基组列于 [tab:essentialelements.basisset.builtin.rel.karlsruhex2c](#tab:essentialelements.basisset.builtin.rel.karlsruhex2c)。

!!! tip "提示"
    `x2c/J` 和 `AutoAux` 辅助基组选项可用于这些基组。

<a id="tab:essentialelements.basisset.builtin.rel.karlsruhex2c"></a>
!!! note "针对 x2c 哈密顿量优化的 Karlsruhe 基组。[Weigend2017-x2c-XVP](../../bibliography.md) RH = 相对论哈密顿量。"
    | Basis Set | Elem. | RH | Comment |
    | --- | --- | --- | --- |
    | `x2c-SV(P)all` | H--Rn | X2C |  |
    | `x2c-SVPall` | H--Rn | X2C |  |
    | `x2c-TZVPall` | H--Rn | X2C |  |
    | `x2c-TZVPPall` | H--Rn | X2C |  |
    | `x2c-QZVPall` | H--Rn | X2C |  |
    | `x2c-QZVPPall` | H--Rn | X2C |  |
    | *NMR 屏蔽优化*[Weigend2019-x2c-XVP-s](../../bibliography.md) |  |  |  |
    | `x2c-SV(P)all-s` | H--Rn | X2C |  |
    | `x2c-SVPall-s` | H--Rn | X2C |  |
    | `x2c-TZVPall-s` | H--Rn | X2C |  |
    | `x2c-TZVPPall-s` | H--Rn | X2C |  |
    | `x2c-QZVPall-s` | H--Rn | X2C |  |
    | `x2c-QZVPPall-s` | H--Rn | X2C |  |
    | *二分量变体*（尚无匹配的哈密顿量！） |  |  |  |
    | `x2c-SV(P)all-2c` | H--Rn | SO-X2C |  |
    | `x2c-SVPall-2c` | H--Rn | SO-X2C |  |
    | `x2c-TZVPall-2c` | H--Rn | SO-X2C |  |
    | `x2c-TZVPPall-2c` | H--Rn | SO-X2C |  |
    | `x2c-QZVPall-2c` | H--Rn | SO-X2C |  |
    | `x2c-QZVPPall-2c` | H--Rn | SO-X2C |  |
    | `x2c-QZVPall-2c-s` | H--Rn | SO-X2C |  |
    | `x2c-QZVPPall-2c-s` | H--Rn | SO-X2C |  |

<a id="sec:essentialelements.basisset.builtin.rel.sapporo"></a>
### 相对论 Sapporo 基组（Relativistic Sapporo Basis Sets）

针对 DKH3 哈密顿量和有限核优化的 [Sapporo 基组](#sec:essentialelements.basisset.builtin.sapporo)的相对论变体列于 [tab:essentialelements.basisset.builtin.rel.sapporo](#tab:essentialelements.basisset.builtin.rel.sapporo)。

<a id="tab:essentialelements.basisset.builtin.rel.sapporo"></a>
!!! note "相对论 Sapporo 基组。RH = 相对论哈密顿量。"
    | Basis Set | Elem. | RH | Comment |
    | --- | --- | --- | --- |
    | `Sapporo-DKH3-DZP-2012` | K--Rn | DKH3 | 针对 DKH3 和有限核优化 |
    | `Sapporo-DKH3-TZP-2012` | K--Rn | DKH3 |  |
    | `Sapporo-DKH3-QZP-2012` | K--Rn | DKH3 |  |

<a id="sec:essentialelements.basisset.builtin.rel.cc"></a>
### 相对论相关一致基组（Relativistic Correlation-Consistent Basis Sets）

[相关一致基组](#sec:essentialelements.basisset.builtin.cc)的相对论变体列于 [tab:essentialelements.basisset.builtin.rel.cc](#tab:essentialelements.basisset.builtin.rel.cc)。

<a id="tab:essentialelements.basisset.builtin.rel.cc"></a>
!!! note "相对论相关一致基组。RH = 相对论哈密顿量。"
    | Basis Set | Elem. | RH | Comment |
    | --- | --- | --- | --- |
    | `cc-pVDZ-DK` | H--Ar, Sc--Kr | DKH2 |  |
    | `cc-pVTZ-DK` | H--Ar, Sc--Kr, Y--Xe, Hf--Rn | DKH2 |  |
    | `cc-pVQZ-DK` | H--Ar, Sc--Kr, In--Xe, Tl--Rn | DKH2 |  |
    | `cc-pV5Z-DK` | H--Ar, Sc--Kr | DKH2 |  |
    | `cc-pVDZ-DK3` | U | DKH3 | 用于三阶 DKH |
    | `cc-pVTZ-DK3` | U | DKH3 |  |
    | `cc-pVQZ-DK3` | U | DKH3 |  |
    | `aug-cc-pVDZ-DK` | H--Ar, Sc--Kr | DKH2 | `cc-pVDZ-DK` 用弥散函数增强 |
    | `aug-cc-pVTZ-DK` | H--Ar, Sc--Kr, Y--Xe, Hf--Rn | DKH2 | `cc-pVTZ-DK` 用弥散函数增强 |
    | `aug-cc-pVQZ-DK` | H--Ar, Sc--Kr, In--Xe, Tl--Rn | DKH2 | `cc-pVQZ-DK` 用弥散函数增强 |
    | `aug-cc-pV5Z-DK` | H--Ar, Sc--Kr | DKH2 | `cc-pV5Z-DK` 用弥散函数增强 |
    | `cc-pwCVDZ-DK` | H--Be, Na--Mg, Ca--Zn | DKH2 | 对 H 和 He 等同于 `cc-pVDZ-DK` |
    | `cc-pwCVTZ-DK` | H--Be, Na--Mg, Ca--Zn, Y--Xe, Hf--Rn | DKH2 | 对 H 和 He 等同于 `cc-pVTZ-DK` |
    | `cc-pwCVQZ-DK` | H--Be, Na--Mg, Ca--Zn, In--Xe, Tl--Rn | DKH2 | 对 H 和 He 等同于 `cc-pVQZ-DK` |
    | `cc-pwCV5Z-DK` | H--Be, Na--Mg, Ca--Zn | DKH2 | 对 H 和 He 等同于 `cc-pV5Z-DK` |
    | `cc-pwCVDZ-DK3` | U | DKH3 |  |
    | `cc-pwCVTZ-DK3` | U | DKH3 |  |
    | `cc-pwCVQZ-DK3` | U | DKH3 |  |
    | `aug-cc-pwCVDZ-DK` | H--Be, Na--Mg, Sc--Zn | DKH2 | `cc-pwCVDZ-DK` 用弥散函数增强，对 H 和 He 等同于 `aug-cc-pVDZ-DK` |
    | `aug-cc-pwCVTZ-DK` | H--Be, Na--Mg, Sc--Zn, Y--Xe, Hf--Rn | DKH2 | `cc-pwCVTZ-DK` 用弥散函数增强，对 H 和 He 等同于 `aug-cc-pVTZ-DK` |
    | `aug-cc-pwCVQZ-DK` | H--Be, Na--Mg, Sc--Zn, In--Xe, Tl--Rn | DKH2 | `cc-pwCVQZ-DK` 用弥散函数增强，对 H 和 He 等同于 `aug-cc-pVQZ-DK` |
    | `aug-cc-pwCV5Z-DK` | H--Be, Na--Mg, Sc--Zn | DKH2 | `cc-pwCV5Z-DK` 用弥散函数增强，对 H 和 He 等同于 `aug-cc-pV5Z-DK` |

### 相对论收缩 ANO 基组（Relativistically Contracted ANO Basis Sets）

Roos 及其合作者的相对论收缩 ANO 基组是为 DKH2 哈密顿量开发的。完整列表见 [tab:essentialelements.basisset.builtin.rel.ano](#tab:essentialelements.basisset.builtin.rel.ano)。

<a id="tab:essentialelements.basisset.builtin.rel.ano"></a>
!!! note "相对论收缩 ANO 基组。RH = 相对论哈密顿量。"
    | Basis Set | Elem. | RH | Comment |
    | --- | --- | --- | --- |
    | `ANO-RCC-Full` | H--Cm | DKH2 | 完整的 ANO-RCC 基组。 |
    | `ANO-RCC-DZP` | H--Cm | DKH2 | `ANO-RCC-Full` 的双-$\zeta$ 收缩。 |
    | `ANO-RCC-TZP` | H--Cm | DKH2 | `ANO-RCC-Full` 的三-$\zeta$ 收缩。 |
    | `ANO-RCC-QZP` | H--Cm | DKH2 | `ANO-RCC-Full` 的四-$\zeta$ 收缩。 |

<a id="sec:essentialelements.basisset.aux"></a>
## 辅助基组（Auxiliary Basis Sets）

[分辨率恒等式（RI）](RI.md#sec:essentialelements.ri)技术可用于加速各类计算。任何 RI 方法除了所选的[轨道基组](#sec:essentialelements.basisset.builtin)外，还需要定义合理的辅助基组。ORCA 为 [`AuxJ`](tab:essentialelements.basisset.aux.auxj)、[`AuxJK`](tab:essentialelements.basisset.aux.auxjk)、[`AuxC`](tab:essentialelements.basisset.aux.auxc) 和 [`CABS`](tab:essentialelements.basisset.aux.cabs) 提供多种内置辅助基组选项，以及名为 [AutoAux](#sec:essentialelements.basisset.aux.autoaux) 的辅助基组自动生成方式。辅助基组也可以如 [basisset.file](#sec:essentialelements.basisset.file) 所述从外部文件读取。

!!! note "注意"
    `AuxJ`、`AuxJK`、`AuxC` 和 `CABS` 之间的区别以及如何正确分配它们，已在[上文说明](par:essentialelements.basisset.basicusage.aux)。

<a id="sec:essentialelements.basisset.aux.auxj"></a>
### 库仑拟合辅助基组（`AuxJ`）
[tab:essentialelements.basisset.aux.auxj](#tab:essentialelements.basisset.aux.auxj) 中列出的辅助基组适用于 [RI-J](RI.md#sec:essentialelements.ri.rij)、
[RIJDX/RIJONX](RI.md#sec:essentialelements.ri.rijonx)、
and [RIJCOSX](RI.md#sec:essentialelements.ri.rijcosx) approximations.

<a id="tab:essentialelements.basisset.aux.auxj"></a>
!!! note "可用的库仑拟合辅助基组。"
    | Keyword | Elements | Comment |
    | --- | --- | --- |
    | `def2/J` | H--Lr | Weigend 的"通用"库仑拟合基，适用于所有 [def2](#sec:essentialelements.basisset.builtin.def2) 和 [def](#sec:essentialelements.basisset.builtin.ahlrichs) 型基组。 假定 Kr 以外使用 ECP（不要与 DKH/ZORA/X2C 一起使用）。 |
    | `def2-mTZVP/J` | H--Lr |  |
    | `def2-mTZVPP/J` | H--Lr |  |
    | `x2c/J` | H--Rn | Weigend 面向全电子 [x2c-XVPall](#sec:essentialelements.basisset.builtin.rel.karlsruhex2c) basis sets |
    | `SARC/J` | H--Rn, Ac--Lr | 用于全电子计算的通用库仑拟合基组。 由直至 Kr 的去收缩 def2/J 和我们自己的辅助 基组（覆盖周期表其余部分）组成。 适用于与下述基组配合的 DKH 或 ZORA 计算： [全电子 def2 的重收缩版本](#sec:essentialelements.basisset.builtin.rel.def2)（直至 Kr）和 [SARC](#sec:essentialelements.basisset.builtin.rel.sarc) 较重元素的基组。 |

<a id="sec:essentialelements.basisset.aux.auxjk"></a>
### 库仑与交换拟合辅助基组（`AuxJK`）

[tab:essentialelements.basisset.aux.auxjk](#tab:essentialelements.basisset.aux.auxjk) 中列出的辅助基组
是针对 [RI-JK](RI.md#sec:essentialelements.ri.rijk) 近似优化的。
它们可以安全地用于 [RI-J](RI.md#sec:essentialelements.ri.rij)、
[RIJDX/RIJONX](RI.md#sec:essentialelements.ri.rijonx)、
或 [RIJCOSX](RI.md#sec:essentialelements.ri.rijcosx)，
但在这种情况下必须通过 `%basis` 模块块把它们分配给 `AuxJ`。

<a id="tab:essentialelements.basisset.aux.auxjk"></a>
!!! note "可用的库仑与交换拟合辅助基组。"
    | Keyword | Elements | Comment |
    | --- | --- | --- |
    | `def2/JK` | H--Rn | 适用于所有 [def2](#sec:essentialelements.basisset.builtin.def2) basis sets |
    | `def2/JKsmall` | H--Ra, Th--Lr | `def2/JK` 的缩减版 |
    | `cc-pVTZ/JK` | H, B--F, Al--Cl, Ga--Br | 与相应的 cc-pV$n$Z 轨道基配合使用 |
    | `cc-pVQZ/JK` | H, B--F, Al--Cl, Ga--Br |  |
    | `cc-pV5Z/JK` | H, B--F, Al--Cl, Ga--Br |  |
    | `aug-cc-pVTZ/JK` | H, B--F, Al--Cl, Ga--Br | 与相应的 aug-cc-pV$n$Z 轨道基配合使用 |
    | `aug-cc-pVQZ/JK` | H, B--F, Al--Cl, Ga--Br |  |
    | `aug-cc-pV5Z/JK` | H, B--F, Al--Cl, Ga--Br |  |
    | `SARC2-DKH-QZV/JK` | La--Lu |  |
    | `SARC2-DKH-QZVP/JK` | La--Lu |  |
    | `SARC2-ZORA-QZV/JK` | La--Lu |  |
    | `SARC2-ZORA-QZVP/JK` | La--Lu |  |

<a id="sec:essentialelements.basisset.aux.auxc"></a>
### 相关方法的辅助基组（`AuxC`）
适用于后（CAS）SCF 动态电子相关方法的可用辅助基组
列于 [tab:essentialelements.basisset.aux.auxc](#tab:essentialelements.basisset.aux.auxc)。

<a id="tab:essentialelements.basisset.aux.auxc"></a>
!!! note "可用的相关方法辅助基组。"
    | Keyword | Elements | Comment |
    | --- | --- | --- |
    | `def2-SVP/C` | H--Rn | 与相应的 def2 轨道基配合使用 |
    | `def2-TZVP/C` | H--Rn |  |
    | `def2-TZVPP/C` | H--Rn |  |
    | `def2-QZVPP/C` | H--Rn |  |
    | `def2-SVPD/C` | H--La, Hf--Rn |  |
    | `def2-TZVPD/C` | H--La, Hf--Rn |  |
    | `def2-TZVPPD/C` | H--La, Hf--Rn |  |
    | `def2-QZVPPD/C` | H--La, Hf--Rn |  |
    | `cc-pVDZ/C` | H--Ar, Ga--Kr | 与相应的 cc-pV$n$Z 轨道基配合使用 |
    | `cc-pVTZ/C` | H--Ar, Sc--Kr |  |
    | `cc-pVQZ/C` | H--Ar, Sc--Kr |  |
    | `cc-pV5Z/C` | H--Ar, Ga--Kr |  |
    | `cc-pV6Z/C` | H--He, B--Ne, Al--Ar |  |
    | `aug-cc-pVDZ/C` | H--He, Be--Ne, Mg--Ar, Ga--Kr | 与相应的 aug-cc-pV$n$Z 轨道基配合使用 |
    | `aug-cc-pVTZ/C` | H--He, Be--Ne, Mg--Ar, Sc--Kr |  |
    | `aug-cc-pVQZ/C` | H--He, Be--Ne, Mg--Ar, Sc--Kr |  |
    | `aug-cc-pV5Z/C` | H--Ne, Al--Ar, Ga--Kr |  |
    | `aug-cc-pV6Z/C` | H--He, B--Ne, Al--Ar |  |
    | `cc-pwCVDZ/C` | H--He, B--Ne, Al--Ar, Ga--Kr | 与相应的 cc-pwCV$n$Z 轨道基配合使用，对 H 和 He 等同于 `cc-pV$n$Z/C` |
    | `cc-pwCVTZ/C` | H--He, B--Ne, Al--Ar, Sc--Kr |  |
    | `cc-pwCVQZ/C` | H--He, B--Ne, Al--Ar, Ga--Kr |  |
    | `cc-pwCV5Z/C` | H--Ne, Al--Ar |  |
    | `aug-cc-pwCVDZ/C` | H--He, B--Ne, Al--Ar, Ga--Kr | For use with the respective aug-cc-pwCV$n$Z orbital basis, equals `aug-cc-pV$n$Z/C` for H and He |
    | `aug-cc-pwCVTZ/C` | H--He, B--Ne, Al--Ar, Sc--Kr |  |
    | `aug-cc-pwCVQZ/C` | H--He, B--Ne, Al--Ar, Ga--Kr |  |
    | `aug-cc-pwCV5Z/C` | H--Ne, Al--Ar |  |
    | `cc-pVDZ-PP/C` | Cu--Kr, Y--Xe, Hf--Rn | 与相应的 cc-pV$n$Z-PP 轨道基配合使用 |
    | `cc-pVTZ-PP/C` | Cu--Kr, Y--Xe, Hf--Rn |  |
    | `cc-pVQZ-PP/C` | Cu--Kr, Y--Xe, Hf--Rn |  |
    | `aug-cc-pVDZ-PP/C` | Cu--Kr, Y--Xe, Hf--Rn | 与相应的 aug-cc-pV$n$Z-PP 轨道基配合使用 |
    | `aug-cc-pVTZ-PP/C` | Cu--Kr, Y--Xe, Hf--Rn |  |
    | `aug-cc-pVQZ-PP/C` | Cu--Kr, Y--Xe, Hf--Rn |  |
    | `cc-pwCVDZ-PP/C` | Cu--Kr, Y--Xe, Hf--Rn | 与相应的 cc-pwCV$n$Z-PP 轨道基配合使用 |
    | `cc-pwCVTZ-PP/C` | Cu--Kr, Y--Xe, Hf--Rn |  |
    | `cc-pwCVQZ-PP/C` | Cu--Kr, Y--Xe, Hf--Rn |  |
    | `aug-cc-pwCVDZ-PP/C` | Cu--Kr, Y--Xe, Hf--Rn | 与相应的 aug-cc-pwCV$n$Z-PP 轨道基配合使用 |
    | `aug-cc-pwCVTZ-PP/C` | Cu--Kr, Y--Xe, Hf--Rn |  |
    | `aug-cc-pwCVQZ-PP/C` | Cu--Kr, Y--Xe, Hf--Rn |  |
    | `cc-pVDZ-F12-MP2Fit` | H--Ar | 与相应的 cc-pV$n$Z-F12 轨道基配合使用 |
    | `cc-pVTZ-F12-MP2Fit` | H--Ar |  |
    | `cc-pVQZ-F12-MP2Fit` | H--Ar |  |
    | `cc-pVDZ-PP-F12-MP2Fit` | Ga--Kr, In--Xe, Tl--Rn | 与相应的 cc-pV$n$Z-PP-F12 轨道基配合使用 |
    | `cc-pVTZ-PP-F12-MP2Fit` | Ga--Kr, In--Xe, Tl--Rn |  |
    | `cc-pVQZ-PP-F12-MP2Fit` | Ga--Kr, In--Xe, Tl--Rn |  |
    | `cc-pCVDZ-F12-MP2Fit` | Li--Ar | 与相应的 cc-pCV$n$Z-F12 轨道基配合使用 |
    | `cc-pCVTZ-F12-MP2Fit` | Li--Ar |  |
    | `cc-pCVQZ-F12-MP2Fit` | Li--Ar |  |

<a id="sec:essentialelements.basisset.aux.cabs"></a>
### F12 的互补辅助基组（`CABS`）
[F12 方法](../modelchemistries/mdci.md#sec:modelchemistries.mdci.expcorrelation)的可用 CABS 选项
列于 [tab:essentialelements.basisset.aux.cabs](#tab:essentialelements.basisset.aux.cabs)。

<a id="tab:essentialelements.basisset.aux.cabs"></a>
!!! note "可用的 F12 方法互补辅助基组。"
    | Keyword | Elements | Comment |
    | --- | --- | --- |
    | `cc-pVDZ-F12-CABS` | H, B--Ne, Al--Ar | 与相应的 cc-pV$n$Z-F12 轨道基配合使用 |
    | `cc-pVTZ-F12-CABS` | H, B--Ne, Al--Ar |  |
    | `cc-pVQZ-F12-CABS` | H, B--Ne, Al--Ar |  |
    | `cc-pVDZ-F12-OptRI` | H--Ar | 与上面的 cc-pV$n$Z-F12-CABS 基组相同 |
    | `cc-pVTZ-F12-OptRI` | H--Ar |  |
    | `cc-pVQZ-F12-OptRI` | H--Ar |  |
    | `cc-pVDZ-PP-F12-OptRI` | Ga--Kr, In--Xe, Tl--Rn | 与相应的 cc-pV$n$Z-PP-F12 轨道基配合使用 |
    | `cc-pVTZ-PP-F12-OptRI` | Ga--Kr, In--Xe, Tl--Rn |  |
    | `cc-pVQZ-PP-F12-OptRI` | Ga--Kr, In--Xe, Tl--Rn |  |
    | `aug-cc-pVDZ-PP-OptRI` | Cu--Zn, Ag--Cd, Au--Hg | 与相应的 aug-cc-pV$n$Z-PP-F12 轨道基配合使用 |
    | `aug-cc-pVTZ-PP-OptRI` | Cu--Zn, Ag--Cd, Au--Hg |  |
    | `aug-cc-pVQZ-PP-OptRI` | Cu--Zn, Ag--Cd, Au--Hg |  |
    | `aug-cc-pV5Z-PP-OptRI` | Cu--Zn, Ag--Cd, Au--Hg |  |
    | `cc-pCVDZ-F12-OptRI` | Li--Ar | 与相应的 cc-pCV$n$Z-PP-F12 轨道基配合使用 |
    | `cc-pCVTZ-F12-OptRI` | Li--Ar |  |
    | `cc-pCVQZ-F12-OptRI` | Li--Ar |  |
    | `aug-cc-pwCVDZ-PP-OptRI` | Cu--Zn, Ag--Cd, Au--Hg | 与相应的 aug-cc-pwCV$n$Z-PP-F12 轨道基配合使用 |
    | `aug-cc-pwCVTZ-PP-OptRI` | Cu--Zn, Ag--Cd, Au--Hg |  |
    | `aug-cc-pwCVQZ-PP-OptRI` | Cu--Zn, Ag--Cd, Au--Hg |  |
    | `aug-cc-pwCV5Z-PP-OptRI` | Cu--Zn, Ag--Cd, Au--Hg |  |

<a id="sec:essentialelements.basisset.aux.autoaux"></a>
### 辅助基组的自动生成（AutoAux）

如果所选轨道基组没有可用的辅助基组，ORCA 可以用关键字 `AutoAux` 自动生成一个。它的指定方式与其他拟合基组相同：作为 `%basis` 模块块中 `AuxJ/AuxJK/AuxC` 变量的取值，或作为简单输入行中的单独关键字（此时三个 Aux 槽位都填入相同的拟合基组）。`AutoAux` 也可以分配给单个元素或原子——见章节 [basisset.element](#sec:essentialelements.basisset.element) 和 [basisset.atom](#sec:essentialelements.basisset.atom)。生成的基组可用于库仑、交换和相关拟合，精度与优化的辅助基组相当，代价是体积最多大一倍。[autoaux](../../bibliography.md)
`AutoAux` 的可用设置及其默认值见 [tab:essentialelements.basisset.keywords.block](#tab:essentialelements.basisset.keywords.block)。

!!! note "注意"
    ORCA 3.1 的生成流程有很大不同，不会产生相同的结果！为兼容起见，仍可通过在 `%basis` 模块块中设置 `OldAutoAux true` 访问旧版本。

注意，如果轨道基组包含弥散函数（如 aug-cc-pVXZ 系列），AutoAux 拟合基可能包含（近）线性相关。此时库仑度量的 Cholesky 分解会失败，程序很可能崩溃。可以用 `!PrintBasis` 打印有问题的辅助基组，并手动移除最弥散的 s 和/或 p 函数，这通常能解决问题。也实现了另一种自动解决方案——见章节 [basisset.lindep-pcd](#sec:essentialelements.basisset.lindep-pcd)。

<a id="sec:essentialelements.basisset.ecps"></a>
## 有效核势（Effective Core Potentials）

从 2.8.0 版本起，ORCA 支持有效核势
（ECP）。若涉及重元素，它们是标量相对论全电子
计算的良好替代方案。这适用于几何
优化和能量计算，但对性质计算可能并非如此。
calculations.

为了减少计算量，通常高度收缩且
化学惰性的核基函数可以通过采用 ECP 来消除。
ECP 计算只包含"仅价层"基组，因此
服从冻结核近似。核轨道的贡献由一个
有效单电子算符 $U^{\text{core} }$ 来描述，它替代了核
与价电子之间的相互作用，并考虑了
电子的不可分辨性。其径向部分 $U_l(r)$
一般表示为高斯函数的线性组合，
而角向依赖通过角动量投影算符
$|S^l_m\rangle$ 引入。

$$
U^{\text{core} } = U_L(r) + \sum\limits_{l=0}^{L-1} \sum\limits_{m=-l}^{l}\left|S^l_m \rangle \left[U_l(r) - U_L(r)\right]\langle S^l_m\right|
$$

$$
U_l = \sum\limits_k d_{kl}r^{n_{kl} } \exp (-\alpha_{kl}r^2)
$$

最大角动量 $L$ 一般定义为
$l_{\text{max} }^{\text{atom} } + 1$。计算 ECP 积分
所需的参数 $n_{kl}$、$\alpha_{kl}$ 和 $d_{kl}$
已由多位作者发表，其中包括著名的
Los Alamos（LANL）[hay1985chem](../../bibliography.md) 和 Stuttgart--Dresden（SD）
[fuentealba1982chem,szentpaly1982chem,fuentealba1983phys,stoll1984chem,fuentealba1985phys,dolg1987chem,igel1988mol,dolg1989chem,schwerdtfeger1989chem,dolg1989theor,andrae1990theor,kaupp1991chem,kuechle1991mol,dolg1991chem,dolg1992chem,bergner1993mol,dolg1993phys,dolg1993theor,haeussermann1993mol,kuechle1994chem,nicklass1995chem,leininger1996chem,leininger1996chemlett,leininger1997chem,schautz1998theor,wang1998theor,metz2000chem,metz2000theor,martin2001chem,cao2001chem,stoll2002comput,cao2002molec,peterson2003chem,petersonEtAl2003chem,figgen2005chem,lim2005chem,peterson2005theor,yang2005theor,lim2006chem,peterson2006phys,peterson2007chem,moritz2007theor,moritz2008theor,huelsen2009theor,figgen2009chem,weigand2009theor](../../bibliography.md)
参数集。取决于 ECP 的具体参数化方式，
相对论效应可以以半经验方式包含到
原本非相对论的计算中。把 $U^{\text{core} }$ 引入
电子哈密顿量会产生两类 ECP 积分：由最大
角动量势 $U_L$ 产生的局域（或 type-1）积分，
以及由投影势项产生的半局域（或 type-2）积分。
ORCA 中这些积分的求值按照
Flores-Moreno 等人发表的方案进行
[flores2006comput](../../bibliography.md)。

一系列 ECP 参数及关联基组可直接
通过 ORCA 的内部 ECP 库获取（关键字列表见 [table:ECP_keywords](#table:ECP_keywords)）。

<a id="table:ECP_keywords"></a>
!!! note "ORCA 中可用的 ECP 及其关联基组的库关键字概览。"
    | ECP keyword | 核大小[^coresize] | Elements | 价层基组 |
    | --- | --- | --- | --- |
    | *Recommended* |  |  |  |
    | `def-ECP` | 78 | Fr--Ra | Karlsruhe def2 基组：\ def-SV(P), def-SVP, def-TZVP, def-TZVPP, ma-def-TZVP\ MINIX |
    |  | 60 | Ac--Lr |  |
    | `def2-ECP` | 28 | Rb--Xe | Karlsruhe 基组：\ def2-SVP, def2-TZVP, etc.\ def2-SVPD, def2-TZVPD, etc.\ ma-def2-SVP, ma-def2-TZVP, etc. |
    |  | 46 | Cs--La |  |
    |  | 28 | Ce--Lu |  |
    |  | 60 | Hf--Rn |  |
    | `SK-MCDHF-RSC` | 10 | Ca, Cu--Kr | 相关一致基组：\ cc-pV$n$Z-PP, aug-cc-pV$n$Z-PP, cc-pCV$n$Z-PP, aug-cc-pCV$n$Z-PP, cc-pwCV$n$Z-PP, aug-cc-pwCV$n$Z-PP ($n=$ D, T, Q, 5) cc-pV$n$Z-PP ($n=$ D, T, Q) |
    |  | 28 | Sr--Xe |  |
    |  | 46 | Ba |  |
    |  | 60 | Hf--Rn |  |
    |  | 78 | Ra |  |
    |  | 60 | U |  |
    | `HayWadt`[^lanl] | 10 | Na--Cu | LANL 基组：\ LANL2DZ, LANL2TZ, LANL2TZ(f), LANL08, LANL08(f) |
    |  | 18 | Zn |  |
    |  | 28 | Ga--Ag |  |
    |  | 36 | Cd |  |
    |  | 46 | In--La |  |
    |  | 60 | Hf--Au |  |
    |  | 68 | Hg--Tl |  |
    |  | 78 | Pb--Bi, U--Pu |  |
    | `dhf-ECP` | 28 | Rb--Xe | Karlsruhe dhf 基组： dhf-SVP, dhf-TZVP, etc. |
    |  | 46 | Cs--Ba |  |
    |  | 60 | Hf--Rn, U |  |
    | `vDZP-ECP` | 2 | B--Mg | vDZP\ *专为与 vDZP 配合使用而编制* |
    |  | 10 | Al--Zn |  |
    |  | 28 | Ga--Cd |  |
    |  | 46 | In--Lu |  |
    |  | 60 | Hf--Hg |  |
    |  | 78 | Tl--Rn |  |
    | `CRENBL-ECP` | 2 | Li--Mg | CRENBL |
    |  | 10 | Al--Zn |  |
    |  | 28 | Rb--Cd |  |
    |  | 36 | In--Xe |  |
    |  | 46 | Cs--La |  |
    |  | 54 | Ce--Lu |  |
    |  | 60 | Hf-Hg |  |
    |  | 68 | Tl-Rn |  |
    |  | 78 | Fr-Ts |  |
    |  | 92 | Og |  |
    | *Legacy definitions* |  |  |  |
    | `def2-SD` | 28,MWB | Rb--Cd |  |
    |  | 28,MDF[^legacy1] | In--Xe |  |
    |  | 46,MWB | Cs--La |  |
    |  | 60,MWB | Hf--Pt |  |
    |  | 60,MDF[^legacy2] | Au--Rn |  |
    | `def-SD` | 28,MWB | Rb--Cd |  |
    |  | 46,MWB | In--La |  |
    |  | 28,MWB | Ce--Lu |  |
    |  | 60,MWB | Hf--Pt |  |
    |  | 60,MDF[^legacy2] | Au, Hg, Rn |  |
    |  | 78,MWB | Tl--At |  |
    |  | 78,MDF | Fr, Ra |  |
    |  | 60,MWB | Ac--Lr |  |
    | `SDD` | 2,SDF | Li, Be |  |
    |  | 2,MWB | B--Ne |  |
    |  | 10,SDF | Na, Mg |  |
    |  | 10,MWB | Al--Ca |  |
    |  | 10,MDF | Sc--Ni |  |
    |  | 10,MWB | Cu-Zn |  |
    |  | 28,MWB | Ga--Sr |  |
    |  | 28,MHF | Y--Cd |  |
    |  | 28,MDF | Ge--Br, Rb--Xe |  |
    |  | 46,MWB | In--Ba |  |
    |  | 28,MWB | La--Lu |  |
    |  | 60,MWB | Hf--Hg |  |
    |  | 78,MWB | Tl--Rn |  |
    |  | 60,MWB | Ac--Lr |  |
    | `LANL1` | 10 | Na--Ar |  |
    |  | 18 | K--Zn |  |
    |  | 28 | Ga--Kr |  |
    |  | 36 | Rb--Cd |  |
    |  | 46 | In--Xe |  |
    |  | 54 | Cs--La |  |
    |  | 68 | Hf--Tl |  |
    |  | 78 | Pb, Bi |  |
    | `LANL2` | 10 | K--Cu |  |
    |  | 28 | Rb--Ag |  |
    |  | 46 | Cs--La |  |
    |  | 60 | Hf--Au |  |

[^coresize]: 在适用处给出参考方法和数据（S：单价电子离子；M：中性原子；HF：Hartree–Fock；WB：准相对论；DF：相对论）。
[^lanl]: 对应 LANL2，在 LANL2 不可用时对应 LANL1。
[^legacy1]: I：为与 TURBOMOLE 兼容，使用 OLD-SD(28,MDF)。
[^legacy2]: Au、Hg：为与 TURBOMOLE 兼容，使用 OLD-SD(60,MDF)。

!!! note "注意"
    请求某些基组会自动分配匹配的 ECP
    （使用 `NewGTO` 关键字时除外）：
    例如 "def2" 基组使用 `def2-ECP`。
    其他的请参见相应的[基组表格条目](#sec:essentialelements.basisset.builtin)。

分配 ECP 最简单的方式是在简单输入行中使用 ECP 关键字。
ECP 关键字本身*只*分配有效核势，不分配价层基组！
作为显式指定 ECP 名称的例子，你可以使用

```orca
! def2-TZVP def2-SD
```

这将按照上表中的定义分配 def2-SD ECP。
如果没有 def2-SD 关键字，ORCA 默认使用 def2-ECP。

ECP 的分配可以在 `%basis` 模块块中用 `ECP` 和 `NewECP` 关键字完成，
as in the following

```orca
%basis
  ECP       "def2-ECP"     # All elements (for which the ECP is defined)
  NewECP Pt "def2-SD" end  # Different ECP for Pt
end
```

`NewECP` 关键字的一个变体可用于几何定义中的
单个原子：

```orca
* xyz ...
  ...
  S   0.0  0.0  0.0  NewECP "SDD" end
  ...
*
```

注意这些关键字同样只影响 ECP，不影响价层基组！

如果已用 `NewGTO` 关键字（见上文
章节 [basisset.element](#sec:essentialelements.basisset.element) 和
[basisset.atom](#sec:essentialelements.basisset.atom)）改变了某元素/原子的
基组，则可能需要从该元素/原子上
移除 ECP。这可以分别用
`%basis` 模块块或坐标输入中的 `DelECP` 关键字完成：

```mol
title: structure 1
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
1
structure
Cu          0.0          0.0          0.0
```

要移除所有默认加载的 ECP（例如未选择全局基组时），
可以使用简单关键字 `!NoECP`。

<a id="sec:essentialelements.basisset.ecps.manual"></a>
### ECP 参数的手动输入（Manual Input of ECP Parameters）

要手动指定 ECP 参数，`NewECP` 关键字后跟
要输入 ECP 的元素、被替换的核
电子数（N_core）和最大角动量
（lmax）。ECP 规范通过给出构成角向相关
势 U$_l$ 的各个壳层定义来完成。

```orca
%basis 
    NewECP <element>
      N_core <number of core electrons>
      lmax <max. angular momentum>
      [shells]
    end
end
```

对每个 ECP 壳层，首先要给出角动量 $l$，
然后是原始函数的数目。原始函数本身通过
给出序号以及指数 $a_{kl}$、展开系数 $d_{kl}$
和径向幂次 $n_{kl}$ 的相应元组来指定。

```orca
# ECP shell 
      l <number of primitives>
      1    a1l    d1l    n1l
      2    a2l    d2l    n3l
      ...
```

以钒的 SD(10,MDF) 为例。该名称表示
一种 Stuttgart--Dresden 型 ECP，替换 10 个核电子，
源自对中性原子的相对论计算。它
由角动量为 s、p、d、f 的 4 个壳层组成。注意
f 壳层的展开系数为 0.0，因此对这个
有效核势完全没有贡献。这是所有 SD 势的典型特征
（但对于像 TURBOMOLE 这样不支持 ECP 任意角动量、
因而对原始参数集进行重收缩的程序包，
情况可能不同）。

```orca
%basis 
  # ECP SD(10,MDF) for V 
  # M. Dolg, U. Wedig, H. Stoll, H. Preuss,
  # J. Chem. Phys. 86, 866 (1987).  
  NewECP V 
    N_core 10 
    lmax f 
    s 2 
      1      14.4900000000    178.4479710000  2 
      2       6.5240000000     19.8313750000  2 
    p 2 
      1      14.3000000000    109.5297630000  2 
      2       6.0210000000     12.5703100000  2 
    d 2 
      1      17.4800000000    -19.2196570000  2 
      2       5.7090000000     -0.6427750000  2 
    f 1 
      1       1.0000000000      0.0000000000  2 
  end
end
```

### ECP 与幽灵原子（ECPs and Ghost Atoms）

当输入中定义了幽灵原子时（见章节 [coordinates.special](coordinates.md#sec:essentialelements.coordinates.special)），默认**不会**为这些原子添加 ECP。如果确实需要，请在 `%basis` 模块块下添加 `GhostECP true`。

```orca
%basis 
 GhostECP true
 AllowGhostECP true # synonym
end
```

<a id="sec:essentialelements.basisset.embeddingpotentials"></a>
### ECP 嵌入（ECP Embedding）

簇模型的计算有时需要嵌入势，以考虑边界处 otherwise 被忽略的排斥项 [giordano2001surf](../../bibliography.md)。为简化 ORCA 中的这类计算，ECP 嵌入可以很容易地完成：

```orca
*xyz ...
# atom>  charge x    y    z    optional ECP declaration
Zr>      4.0    0.0  0.0  0.0  NewECP "SDD" end
...
*
```

这种无核 ECP 中心在坐标部分声明，方法是在元素符号后附加尖括号 "\>"。注意嵌入 ECP 在 ORCA 中按点电荷处理，因此接下来必须给出电荷。无核 ECP 中心的坐标照常指定，后面可以跟可选的 ECP 分配。一般而言，采用 ECP 嵌入流程的计算应为单点计算。但如果确需进行几何优化，请务必为无核 ECP 中心设置显式的笛卡尔约束。

<a id="sec:essentialelements.basisset.element"></a>
## 为元素分配或添加基函数

要为给定元素分配新的基组，请使用：

```orca
%basis
  NewGTO 8    # New basis for oxygen.
# NewGTO O    # This works as well.
   S   3      # s-shell
    1  910.10034975         0.03280967
    2  137.19711335         0.23422391
    3   30.85279077         0.81490980
   0   2      # also an s-shell
    1     1.72885887         0.27389659
    2     0.39954770         0.79112437
   P   1
    1     8.35065975         1.00000000
  end
end
```

为简单和一致起见，输入格式与[基组文件](#sec:essentialelements.basisset.file)中使用的格式相同。在此格式中，第一行给出要添加壳层的角动量（整数或标签 s、p、d、f、g、h、i、k）以及原始函数的数目。然后每个原始函数一行，包含 (a) 原始函数序号（1、2、3、...）、(b) 原始函数的指数和 (c) 收缩系数（未归一化）。还可以在第一行原始函数数目之后加入 `SCALE X` 语句，表示基函数指数应被标度。

!!! warning "警告"
    - ORCA 始终使用球谐高斯函数。
    - 角动量 7 标记为 "k"——在公认的光谱学惯例中没有 j 壳层。
    - s 和 p 的组合壳层在其他程序中有时标记为 "L 壳层"。`NewGTO` 格式不支持这种记法；为避免混淆，角动量为 8 的壳层只能用数字指定，不能用标签 "l"。

要向给定元素的基组添加基函数（例如因为你不喜欢标准极化函数），请用 `AddGTO` 代替 `NewGTO`。在 `NewGTO` 或 `AddGTO` 中也可以使用内部存储基组的昵称。例如：

```orca
%basis
  NewGTO 8    # new basis for oxygen
   "6-31G"
    D  1 
    1  0.4  1.0
  end
end
```

本例中把 6-31G 基组分配给氧，并另外向氧的基组添加一个指数为 0.4 的极化函数。

注意 `NewGTO` 关键字不会更改给定元素的 ECP——必须使用 `NewECP` 或 `DelECP`（见章节
[basisset.ecps](#sec:essentialelements.basisset.ecps)).

RI 中的辅助基组也有类似的机制
calculations:

```orca
%basis
  NewAuxJGTO 8    # new auxiliary basis for oxygen
    s  1 
    1  350  1.0
    ... etc
  end
  AddAuxJGTO 8   # add a shell to the auxiliary basis for 
                # oxygen
    D  1 
    1  0.8  1.0
  end
end
```

新的基函数可以专门分配给任何辅助基组
sets. The keywords `NewAuxCGTO`, `AddAuxCGTO`, `NewAuxJKGTO`,
`AddAuxJKGTO`、`NewCABSGTO`、`AddCABSGTO` 的用法相同。关键字 `NewAuxGTO` 和 `AddAuxGTO` 与 `NewAuxJGTO` 和 `AddAuxJGTO` 相同，即它们只影响库仑辅助基组
(`AuxJ`)!

<a id="sec:essentialelements.basisset.atom"></a>
## 为单个原子分配或添加基函数

有时你可能不希望同一元素的所有原子都用相同的基组，而是想把特定基组分配给分子中的特定原子。这在 ORCA 中也可以做到，通过
坐标部分（`%coords`、`*xyz` 等）。格式与
如上所述。看一个例子会更清楚：

```orca
*int 0 1
  C  0 0 0 0.00   0.0   0.00
   AddGTO
     D  1 
      1  1.0  1.0
   end
  O  1 0 0 1.13   0.0   0.00
   NewGTO
     "6-311G"
     D  1 
      1  1.2  1.0
   end
*
```

本例中向第一个碳原子添加了一个指数为 1.0 的额外 d 壳层，并把氧原子的基组改为 `6-311G`
with an extra d-function of exponent 1.2 added.

类似地，可以用关键字 `NewAuxJGTO`、`AddAuxJGTO` 把 `AUX` 基函数分配或添加给单个原子，
`NewAuxCGTO`, `AddAuxCGTO`, `NewAuxJKGTO`, `AddAuxJKGTO`, `NewCABSGTO`,
`AddCABSGTO`.

关于 `AutoAux` 用法的说明：如果你更改了某个原子的基组并希望生成拟合基，必须在坐标部分再次指定它，即使 `AutoAux` 已出现在简单输入行或 `%basis` 模块块中。对于

```mol
title: structure 2
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
3
structure (0 1)
O          0.00         0.00         0.00
H         -0.25         0.93         0.00
H          0.96         0.00         0.00
--- input ---
! def2-SVP def2/JK
%basis
  NewAuxJKGTO H
    "AutoAux"
  end
end
*xyz 0 1
  O  0.00 0.00 0.00
  H -0.25 0.93 0.00
  H  0.96 0.00 0.00
   AddGTO
     P 1
      1 1.6 1.0
     D 1
      1 1.0 1.0
   end
   NewAuxJKGTO
     "AutoAux"
   end
*
```

这里氧原子被分配 def2-SVP 基组和 def2/JK 拟合基，第一个氢原子被分配 def2-SVP 基组和自动生成的拟合基，第二个氢原子被分配 def2-SVP 基组外加两个极化函数，以及一个计入这些函数的更大的自动生成拟合基。

!!! tip "提示"
    分配自定义基组时，最好打印基组信息（`%output print[p_basis] 2 end` 或直接 `!PrintBasis`）并检查一切是否正确。

<a id="sec:essentialelements.basisset.fragments"></a>
## 为片段分配基组和 ECP

在多层级或 QM/QM 计算中，把不同基组分配给不同的[片段](fragmentation.md#sec:essentialelements.fragmentation)可能更方便。这可以在 `%basis` 模块块中用关键字 `FragBasis`、`FragAuxJ`、`FragAuxJK`、`FragAuxC`、`FragCABS` 和 `FragECP` 完成，后跟片段编号（从 1 开始！）以及 ORCA 库中的标准基组或 ECP（见 [basisset.builtin](#sec:essentialelements.basisset.builtin) 和 [table:ECP_keywords](#table:ECP_keywords)）。注意与 `NewGTO` 关键字不同，`FragBasis` 在适用时也会更改 ECP。片段基组会覆盖全局或按元素的选择（[basisset.element](#sec:essentialelements.basisset.element)），但可以被针对单个原子的设置（[basisset.atom](#sec:essentialelements.basisset.atom)）覆盖。如果为片段请求了 AutoAux，它会针对每个原子实际选定的轨道基组生成，即使该基组在坐标部分被更改。但如果为某元素或在简单输入中请求了 AutoAux，辅助基组会在片段基组分配之前生成（这不是我们想要的），因此必须为片段再次请求 AutoAux。下面给出一个例子：

```mol
title: structure 3
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
5
structure (0 1)
H             0            0            0
I             0            0          1.6
I             0            5          1.6
H             5            0            0
I             5            0          1.6
--- input ---
! PrintBasis BP86 NoIter
! def2-SVP def2/J
%basis
  FragBasis 1 "def2-TZVP"
  FragBasis 2 "cc-pVTZ-PP"
  FragAuxJ  2 "AutoAux"
  FragECP   3 "SK-MCDHF-RSC"
  FragAuxJ  3 "def2/JK"
end
*xyz 0 1
  H(1) 0 0 0
  I(1) 0 0 1.6
  H(2) 0 5 0   NewGTO "cc-pVTZ" end
  I(2) 0 5 1.6
  H(3) 5 0 0
  I(3) 5 0 1.6
*
# Final basis sets:
# Atom Basis      ECP          AuxJ
# 0H   def2-TZVP  def2-ECP     def2/J
# 1I   def2-TZVP  def2-ECP     def2/J
# 2H   cc-pVTZ    -            AutoAux(cc-pVTZ)
# 3I   cc-pVTZ-PP SK-MCDHF-RSC AutoAux(cc-pVTZ-PP)
# 4H   def2-SVP   -            def2/JK
# 5I   def2-SVP   SK-MCDHF-RSC def2/JK
```

也可以从文件读取片段专用基组。语法类似，使用关键字 `ReadFragBasis`、`ReadFragAuxJ`、`ReadFragAuxJK`、`ReadFragAuxC`、`ReadFragCABS` 和 `ReadFragECP`。此时输入字符串应是 GAMESS-US 格式的现有基组文件（见章节 [basisset.file](#sec:essentialelements.basisset.file)）。上文的其他细节（例如关于 ECP 和 AutoAux）同样适用。

!!! note "注意"
    -  关于片段分配的细节见[片段指定](fragmentation.md#sec:essentialelements.fragmentation)一节。

<a id="sec:essentialelements.basisset.file"></a>
## 从文件读取基组

通过使用变量 `GTOName`、`GTOAuxJName`、`GTOAuxJKName`、`GTOAuxCName` 和 `GTOCABSName`（`GTOAuxName` 是 `GTOAuxJName` 的同义词），可以从 ASCII 文件读取基组。这样你就可以构造或修改你喜欢的标准基组，并方便地加载到程序中。

```orca
%basis
  GTOName      = "MyBasis.bas"      # read orbital basis
  GTOAuxJName  = "MyAuxJBasis.bas"  # read Coulomb-fitting basis
  GTOAuxJKName = "MyAuxJKBasis.bas" # read Coulomb- and exchange-fitting basis
  GTOAuxCName  = "MyAuxCBasis.bas"  # read correlation-fitting basis
  GTOCABSName  = "MyCABSBasis.bas"  # read complementary auxiliary basis set
end
```

注意事项：在 Windows 下，反斜杠目录路径
必须给出两次才能被正确理解！所用格式为
即 EMSL 库中的 "GAMESS-US" 格式 [basissets](../../bibliography.md)。为展示该格式的样子，下面是 Buenker 及其合作者 `3-21GSP` 基组的一部分 [mitin1996chem,mitin1997comp](../../bibliography.md)：

```orca
!                         lines in the beginning with '!' or '#' are comments
! BASIS="3-21GSP"
!Elements                             References                                
!--------                             ----------                                
! H - Ne: A.V. Mitin, G. Hirsch, R. J. Buenker, Chem. Phys. Lett. 259, 151 (1996)
! Na - Ar: A.V. Mitin, G. Hirsch, R. J. Buenker, J. Comp. Chem. 18, 1200 (1997). 
!
$DATA        ! Optional
HYDROGEN     ! (3s) -> [2s]      Element symbols are also recognized
 S   2
  1           4.50036231         0.15631167
  2           0.68128924         0.90466909
 S   1
  1           0.15137639         1.00000000
CARBON       ! (6s,3p) -> [3s,2p]                                
 S   3
  1         499.24042249         0.03330322
  2          75.25419194         0.23617745
  3          16.86538669         0.81336259
 L   2       ! L shells are a s and a p shell with identical exponents
  1           0.89739483         0.24008573         0.46214684
  2           0.21746772         0.81603757         0.66529098
 L   1
  1           4.52660451         1.00000000         1.00000000
$END         ! Optional
```

辅助基组的文件格式完全相同。基组
基组也可以用 `orca_exportbasis` 工具（章节 [utilities.exportbasis](../utilitiesvisualization/utilities.md#sec:utilities.exportbasis)）导出为 GAMESS-US 格式。注意为了
读取 ORCA 打印的基组（使用 `!PrintBasis`）、`NewGTO` 和
`end` 关键字必须被移除。

!!! warning "警告"
    - 角动量 7 标记为 "k"——在公认的光谱学惯例中没有 j 壳层。
    - 为避免与 s 和 p 的组合壳层混淆，角动量为 8 的壳层只能用数字指定，不能用标签 "l"。

<a id="sec:essentialelements.lindep"></a>
## 线性相关（Linear Dependence）

前面几节描述了如何从分子内不同位置（通常以原子为中心）
经过适当参数化的函数来构造所需的分子
基组。这些函数的参数化使得
出现冗余的可能性极小。然而，由于
我们只能在有限的数值精度下工作，而且
这些参数还依赖于分子几何结构，
冗余无法事先完全消除。冗余
是指在给定参数值（包括几何）下由给定基函数
张成的子空间，可以由更少数目的
*线性无关*基函数同样地张成。线性
相关（冗余）的函数集可能导致数值不稳定。
线性相关通常通过寻找重叠矩阵的
零本征值来识别。注意重叠矩阵
（或相关矩阵）的逆用于正交化，
因此如果接近零的本征值处理不当，
逆矩阵将失去良好定义，SCF 过程在数值上
变得不稳定。

由前面的讨论可知，治疗线性相关的关键参数
是判定重叠本征值为零的阈值。
该参数可以用下面的关键字更改

```orca
%scf
  sthresh 1e-6 # default 1e-7
end
```

虽然上述参数的取值没有严格限制，
但合理的范围是 1e-5 到 1e-8 之间（默认为 1e-7）。取 1e-9 甚至更低也许能不出现
收敛问题，但结果有被接近零的向量
引起的噪声污染的风险。在困难情形下，1e-6 的阈值
往往工作顺畅，高于此值则有可能
丢弃越来越多的函数，这也会影响
与其他计算结果的可比性。要监视
小本征值的行为，应在输出中查找下面的
块

```orca
Diagonalization of the overlap matrix:
Smallest eigenvalue                        ... -1.340e-17
Time for diagonalization                   ...    0.313 sec
Threshold for overlap eigenvalues          ... 1.000e-07
Number of eigenvalues below threshold      ... 1
Smallest eigenvalue above threshold        ... 6.013e-07
Time for construction of square roots      ...    0.073 sec
Total time needed                          ...    0.387 sec
```

这里打印最小本征值、当前使用的
重叠阈值以及低于该阈值的函数数目（将被丢弃）。
建议做一致性检查：SCF 收敛后在轨道能量中
查找相同数目的零值。
注意对属于零本征值的函数*不施加
任何能级移动*！

如果从基组中移除了冗余向量，
`! MORead NoIter` 只应与原计算中相同的
`SThresh` 一起使用，否则结果将
不一致。
`! MORead` 仍可与更改 `SThresh` 一起使用，
但需要若干次 SCF 迭代。

<a id="sec:essentialelements.basisset.lindep-diffsthresh"></a>
### 近线性相关情形的自动调整

从 ORCA6 起有一个名为 DiffSThresh 的关键字，它控制
在发现重叠矩阵小本征值时自动收紧积分
截断参数 Thresh 和 TCut。我们发现这对
某些使用弥散基组的计算很重要，当上面显示的
"Smallest eigenvalue" 低于该值时，这些参数被设为最小值
`Thresh=1e-12` 和 `TCut=1e-13`。如果截断已经比这更严格，
例如使用 `!VeryTightSCF` 时，则不会发生任何变化。

我们凭经验发现这些是抑制噪声、
增强 SCF 过程稳健性的安全数值，因此默认强制执行。
默认值为 1e-6，如果不希望这种自动调整发生，可在输入中设置
`%SCF DiffSThresh -1 END` 将其关闭。

<a id="sec:essentialelements.basisset.lindep-pcd"></a>
### 冗余基函数的移除

虽然上述方法通常能成功消除
轨道基组中的线性相关，但 RI 中使用的辅助基组
并非以同样的方式正交化。RI 线性方程组
是用辅助基组库仑度量的 Cholesky 分解（CD）求解的。
如果辅助基组冗余，CD 会失败，
程序通常会中止。ORCA 中实现的一个简单解
是对度量进行带主元的 Cholesky 分解（PCD），
在给定阈值处终止。然后在计算开始时
把对零空间有贡献的壳层从基组中移除。
这可以对任何基组按重叠度量或库仑度量
来请求。它最适合用库仑度量的
AuxJ/AuxJK/AuxC 基组。截断后的基组可以用
`!PrintBasis` 关键字检查。经常会出现某元素的
部分原子被移除函数、而其他原子保留的情况。只要
阈值足够低，即只移除真正冗余的函数，
这就不应影响结果的分子对称性。

```orca
%basis
  PCDTrimBas   Overlap # Trim the orbital basis in the overlap metric
  PCDTrimAuxJ  Coulomb # Trim the AuxJ basis in the Coulomb metric
  PCDTrimAuxJK Coulomb # Trim the AuxJK basis in the Coulomb metric
  PCDTrimAuxC  Coulomb # Trim the AuxC basis in the Coulomb metric
  PCDThresh    -1      # Threshold for the PCD: chosen automatically if <0
end
```

<a id="sec:essentialelements.basisset.methods"></a>
## 哪些方法需要哪些基组？

ORCA 提供多种方法以及大量可与之搭配的
[orbital](#sec:essentialelements.basisset.builtin)
and [auxiliary](#sec:essentialelements.basisset.aux)
基组。
纯（GGA 或 meta-GGA）[DFT](../modelchemistries/DensityFunctionalTheory.md#sec:modelchemistries.dft) 泛函
只需计算库仑积分，
而[杂化 DFT](../modelchemistries/DensityFunctionalTheory.md#sec:modelchemistries.dft.hybriddft)、
HF（以及推而广之的所有后 HF 电子相关方法，
如 [MP2](../modelchemistries/MP2.md#sec:modelchemistries.mp2) 和[耦合簇](../modelchemistries/mdci.md#sec:modelchemistries.mdci)）、
以及 [CASSCF](../modelchemistries/CASSCF.md#sec:modelchemistries.casscf)（和 [NEVPT2](../modelchemistries/NEVPT2.md#sec:modelchemistries.nevpt2)），
都需要计算库仑积分和交换积分。
- 这些方法始终需要一个轨道基组（`<basis>`）。
- 若对库仑积分使用 RI（[RI-J](RI.md#sec:essentialelements.ri.rij)、
  [RIJDX/RIJONX](RI.md#sec:essentialelements.ri.rijonx)、
  [RIJCOSX](RI.md#sec:essentialelements.ri.rijcosx)），
  则需要 `AuxJ`（通常为 `<basis>/J` 或 `def2/J`）。
- 若对交换积分也使用 RI（[RI-JK](RI.md#sec:essentialelements.ri.rijk)），
  则改为需要 `AuxJK`（通常为 `<basis>/JK` 或 `def2/JK`）。
- 若在后 SCF 相关方法的积分生成中使用 RI，
  如 [RI-MP2](../modelchemistries/MP2.md#sec:modelchemistries.mp2.ri)
  （包括[双杂交 DFT](../modelchemistries/DensityFunctionalTheory.md#sec:modelchemistries.dft.doublehybriddft)）、
  [DLPNO-MP2](../modelchemistries/MP2.md#sec:modelchemistries.mp2.dlpno)、
  以及 [DLPNO-CC](../modelchemistries/mdci.md#sec:modelchemistries.mdci.localcorrelation)，
  还需要 `AuxC`（通常为 `<basis/C>`）。
- 在 [F12 方法](../modelchemistries/mdci.md#sec:modelchemistries.mdci.expcorrelation)中，
  使用专用的轨道基组（`<basis>-F12`），
  另外还需要 `CABS`（通常为 `<basis>-F12-CABS` 或 `<basis>-F12-OptRI`）。

下面给出一份并非穷尽的方法与近似列表的
辅助基组需求概览，见 [tab:essentialelements.basisset.methods](#tab:essentialelements.basisset.methods)。

<a id="tab:essentialelements.basisset.methods"></a>
!!! note "基组和 ECP 的简单输入关键字。"
    | 方法              | 近似               | 基组                                                               |
    |:----------------|:------------------|:-----------------------------------------------------------------|
    | HF              | NoRI (default)    | `<basis>`                                                        |
    | HF              | RIJONX or RIJCOSX | `<basis>` + `<basis>/J`                                          |
    | HF              | RI-JK             | `<basis>` + `<basis>/JK`                                         |
    | pure DFT        | RI (default)      | `<basis>` + `<basis>/J`                                          |
    | hybrid DFT      | NoRI              | `<basis>`                                                        |
    | hybrid DFT      | RIJCOSX (default) | `<basis>` + `<basis>/J`                                          |
    | hybrid DFT      | RI-JK             | `<basis>` + `<basis>/JK`                                         |
    | CASSCF/NEVPT2   |                   | `<basis>`                                                        |
    | CASSCF/NEVPT2   | RI-JK             | `<basis>` + `<basis>/JK`                                         |
    | CASSCF/NEVPT2   | RIJCOSX           | `<basis>` + `<basis>/J` + `<basis>/C`                            |
    | CASSCF/NEVPT2   | TrafoStep RI      | `<basis>` + `<basis>/JK` or `<basis>/C`                          |
    | NEVPT2-F12      | TrafoStep RI      | `<basis>-F12` + `<basis>-F12-CABS` + `<basis>/JK` or `<basis>/C` |
    | TDDFT           |                   | `<basis>`                                                        |
    | MP2             |                   | `<basis>`                                                        |
    | RI-MP2          |                   | `<basis>` + `<basis>/C`                                          |
    | RI-MP2          | RI-JK             | `<basis>` + `<basis>/C` + `<basis>/JK`                           |
    | F12-MP2         |                   | `<basis>-F12` + `<basis>-F12-CABS`                               |
    | F12-RI-MP2      |                   | `<basis>-F12` + `<basis>-F12-CABS` + `<basis>/C`                 |
    | DLPNO-MP2       |                   | `<basis>` + `<basis>/C`                                          |
    | DLPNO-MP2       | RIJCOSX           | `<basis>` + `<basis>/C` + `<basis>/J`                            |
    | F12-DLPNO-MP2   |                   | `<basis>-F12` + `<basis>-F12-CABS` + `<basis>/C`                 |
    | CCSD            |                   | `<basis>`                                                        |
    | RI-CCSD         |                   | `<basis>` + `<basis>/C`                                          |
    | DLPNO-CCSD      |                   | `<basis>` + `<basis>/C`                                          |
    | DLPNO-CCSD      | RIJCOSX           | `<basis>` + `<basis>/C` + `<basis>/J`                            |
    | F12-CCSD        |                   | `<basis>-F12` + `<basis>-F12-CABS`                               |
    | F12-RI-CCSD     |                   | `<basis>-F12` + `<basis>-F12-CABS` + `<basis>/C`                 |
    | F12-RI-CCSD     | RI-JK             | `<basis>-F12` + `<basis>-F12-CABS` + `<basis>/C` + `<basis>/JK`  |

<a id="sec:essentialelements.basisset.keywords"></a>
## 关键字（Keywords）

<a id="tab:essentialelements.basisset.keywords.simple"></a>
!!! note "基组和 ECP 的简单输入关键字。"
    | Keyword             | Description                                                                                                                 |
    |:--------------------|:----------------------------------------------------------------------------------------------------------------------------|
    | `<BasisName>`       | 为所有元素分配相应的[轨道基组](#sec:essentialelements.basisset.builtin)                            |
    | `<AUXJName>`        | 为所有元素分配相应的 [`AuxJ` 基组](#sec:essentialelements.basisset.aux.auxj)                           |
    | `<AUXJKName>`       | 为所有元素分配相应的 [`AuxJK` 基组](#sec:essentialelements.basisset.aux.auxjk)                         |
    | `<AUXCName>`        | 为所有元素分配相应的 [`AuxJC` 基组](#sec:essentialelements.basisset.aux.auxc)                          |
    | `<CABSName>`        | 为所有元素分配相应的 [`CABS`](#sec:essentialelements.basisset.aux.cabs)                                     |
    | `AutoAux`           | 自动生成 AuxJ、AuxJK 和 AuxC 辅助基组（见 [aux.autoaux](#sec:essentialelements.basisset.aux.autoaux))|
    | `<ECPName>`         | 为所有定义了该 ECP 的元素分配相应的 ECP                                                           |
    | `NoECP`             | 移除默认 ECP                                                                                                      |
    | `Decontract`        | 对所有（轨道和辅助）基组去收缩                                                                           |
    | `DecontractBas`     | 对轨道基组去收缩                                                                                           |
    | `NoDecontractBas`   | 不对基组去收缩                                                                                             |
    | `DecontractAuxJ`    | 对 AuxJ 基组去收缩                                                                                               |
    | `NoDecontractAuxJ`  | 不对 AuxJ 基组去收缩                                                                                            |
    | `DecontractAuxJK`   | 对 AuxJK 基组去收缩                                                                                              |
    | `NoDecontractAuxJK` | 不对 AuxJK 基组去收缩                                                                                           |
    | `DecontractAuxC`    | 对 AuxC 基组去收缩                                                                                               |
    | `NoDecontractAuxC`  | 不对 AuxC 基组去收缩                                                                                            |

<a id="tab:essentialelements.basisset.keywords.block"></a>
!!! note "基组和 ECP 的 `%basis` 模块块输入关键字。"
    | Keyword | Options | Description |
    | --- | --- | --- |
    | `Basis` | `"<BasisName>"` | 定义[轨道基组](#sec:essentialelements.basisset.builtin) |
    | `AuxJ` | `"<AuxName>"` | 定义 [J 辅助基组](#sec:essentialelements.basisset.aux.auxj) |
    | `AuxJK` | `"<AuxName>"` | 定义 [JK 辅助基组](#sec:essentialelements.basisset.aux.auxjk) |
    | `AuxC` | `"<AuxName>"` | 定义[相关辅助基组](#sec:essentialelements.basisset.aux.auxc) |
    | `CABS` | `"<CABSName>"` | 定义 F12 计算用的[互补辅助基组](#sec:essentialelements.basisset.aux.cabs) |
    | `ECP` | `"<ECPName>"` | 为所有可用元素分配相应的 [ECP](#sec:essentialelements.basisset.ecps) |
    | `GhostECP` | `false` | 在幽灵原子上启用 ECP |
    | `AllowGhostECP` | `false` | 等同于 `GhostECP` |
    | 去收缩选项 |  |  |
    | `Decontract` | `false` | 若为 `true`，对所有基组去收缩 |
    | `DecontractBas` | `false` | 若为 `true`，对轨道基组去收缩 |
    | `DecontractAuxJ` | `false` | 若为 `true`，对 AuxJ 基组去收缩 |
    | `DecontractAuxJK` | `false` | 若为 `true`，对 AuxJK 基组去收缩 |
    | `DecontractAuxC` | `false` | 若为 `true`，对 AuxC 基组去收缩 |
    | `DecontractCABS` | `true` | 若为 `false`，不对 CABS 去收缩 |
    | 为元素设置基组（见 [basisset.element](#sec:essentialelements.basisset.element)） |  |  |
    | `NewGTO` | `<Element> "<BasisName>" <shells> End` | 通过内置名称和/或自定义壳层为元素定义新的 `Basis` |
    | `AddGTO` | `<Element> <shells> End` | 为元素的基组添加 GTO 壳层 |
    | `NewAuxJGTO` | `<Element> "<AuxName>" <shells> End` | 通过内置名称和/或自定义壳层为元素定义新的 `AuxJ` 集 |
    | `AddAuxJGTO` | `<Element> <shells> End` | 为元素的 `AuxJ` 添加 GTO 壳层 |
    | `NewAuxJKGTO` | `<Element> "<AuxName>" <shells> End` | 通过内置名称和/或自定义壳层为元素定义新的 `AuxJK` 集 |
    | `AddAuxJKGTO` | `<Element> <shells> End` | 为元素的 `AuxJK` 添加 GTO 壳层 |
    | `NewAuxCGTO` | `<Element> "<AuxName>" <shells> End` | 通过内置名称和/或自定义壳层为元素定义新的 `AuxC` 集 |
    | `AddAuxCGTO` | `<Element> <shells> End` | 为元素的 `AuxC` 添加 GTO 壳层 |
    | `NewCABSGTO` | `<Element> "<CABSName>" <shells> End` | 通过内置名称和/或自定义壳层为元素定义新的 `CABS` 集 |
    | `AddCABSGTO` | `<Element> <shells> End` | 为元素的 `CABS` 添加 GTO 壳层 |
    | `NewECP` | `<Element> "<ECPName>" End` | 为元素定义新的内置 ECP |
    |  | `<Element> <shells> End` | 为元素手动定义新的 ECP（见 [ecps.manual](#sec:essentialelements.basisset.ecps.manual)） |
    | `DelECP` | `<Element>` | 移除该元素的 ECP |
    | 为片段设置基组（见 [basisset.fragments](#sec:essentialelements.basisset.fragments)） |  |  |
    | `FragBasis` | `<FragID> "<BasisName>"` | 为片段定义 `Basis` |
    | `FragAuxJ` | `<FragID> "<AuxName>"` | 为片段定义 `AuxJ` |
    | `FragAuxJK` | `<FragID> "<AuxName>"` | 为片段定义 `AuxJK` |
    | `FragAuxC` | `<FragID> "<AuxName>"` | 为片段定义 `AuxC` |
    | `FragCABS` | `<FragID> "<CABSName>"` | 为片段定义 `CABS` |
    | `FragECP` | `<FragID> "<ECPName>"` | 为片段定义 `ECP` |
    | `ReadFragBasis` | `<FragID> "<filename.bas>"` | 从文件为片段读取 `Basis` |
    | `ReadFragAuxJ` | `<FragID> "<filename.bas>"` | 从文件为片段读取 `AuxJ` |
    | `ReadFragAuxJK` | `<FragID> "<filename.bas>"` | 从文件为片段读取 `AuxJK` |
    | `ReadFragAuxC` | `<FragID> "<filename.bas>"` | 从文件为片段读取 `AuxC` |
    | `ReadFragCABS` | `<FragID> "<filename.bas>"` | 从文件为片段读取 `CABS` |
    | `ReadFragECP` | `<FragID> "<filename.bas>"` | 从文件为片段读取 `ECP` |
    | 从文件读取基组（见 [basisset.file](#sec:essentialelements.basisset.file)） |  |  |
    | `GTOName` | `<filename.bas>` | 从文件读取轨道基组 |
    | `GTOAuxJName` | `<filename.bas>` | 从文件读取 `AuxJ` |
    | `GTOAuxName` | `<filename.bas>` | 等同于 `GTOAuxJName` |
    | `GTOAuxJKName` | `<filename.bas>` | 从文件读取 `AuxJK` |
    | `GTOAuxCName` | `<filename.bas>` | 从文件读取 `AuxC` |
    | `GTOCABSName` | `<filename.bas>` | 从文件读取 `CABS` |
    | 线性相关的移除（见 [basisset.lindep-pcd](#sec:essentialelements.basisset.lindep-pcd)） |  |  |
    | `PCDTrimBas` | `Overlap` | 在重叠度量下修剪轨道基组 |
    | `PCDTrimAuxJ` | `Coulomb` | 在库仑度量下修剪 AuxJ 基组 |
    | `PCDTrimAuxJK` | `Coulomb` | 在库仑度量下修剪 AuxJK 基组 |
    | `PCDTrimAuxC` | `Coulomb` | 在库仑度量下修剪 AuxC 基组 |
    | `PCDThresh` | `-1` | PCD 的阈值（1e-16 到 1e-10 较为合理）：若 `<0` 则自动选择 |
    | AutoAux-related keywords (see [aux.autoaux](#sec:essentialelements.basisset.aux.autoaux)) |  |  |
    | `AutoAuxSize` | 0 | 使用最小有效指数而非最小原始指数（适用于 ANO 基组） |
    |  | 1 | （默认）增大小角动量壳层的最大指数。 |
    |  | 2 | 增大所有壳层的最大指数 |
    |  | 3 | 直接使用原始函数并产生最大的拟合基 |
    | `AutoAuxLmax` | `false` | 若为 `true`，把拟合基组的最大角动量提高到 ORCA 和轨道基组所允许的最高值。 |
    | `AutoAuxLLimit` | -1 | 若 >0，不超过给定的角动量。 |
    | `AutoAuxF[0]` | 20.0 | 增大最大 s 指数的因子 |
    | `AutoAuxF[1]` | 7.0 | p 壳层同理 |
    | `AutoAuxF[2]` | 4.0 | d 壳层同理 |
    | `AutoAuxF[3]` | 4.0 | f 壳层同理 |
    | `AutoAuxF[4]` | 3.5 | g 壳层同理 |
    | `AutoAuxF[5]` | 2.5 | h 壳层同理 |
    | `AutoAuxF[6]` | 2.0 | i 壳层同理 |
    | `AutoAuxF[7]` | 2.0 | j 壳层同理 |
    | `AutoAuxB[0]` | 1.8 | s 壳层的等比展开因子 |
    | `AutoAuxB[1]` | 2.0 | p 壳层同理 |
    | `AutoAuxB[2]` | 2.2 | d 壳层同理 |
    | `AutoAuxB[3]` | 2.2 | f 壳层同理 |
    | `AutoAuxB[4]` | 2.2 | g 壳层同理 |
    | `AutoAuxB[5]` | 2.3 | h 壳层同理 |
    | `AutoAuxB[6]` | 3.0 | i 壳层同理 |
    | `AutoAuxB[7]` | 3.0 | j 壳层同理 |
    | `AutoAuxTightB` | `true` | 仅对高 `l` 壳层使用 `AutoAuxB[l]`，其余使用 `AutoAuxB[0]` |
    | `OldAutoAux` | `false` | 若为 `true`，选择 ORCA 3.1 的生成流程（已弃用） |
