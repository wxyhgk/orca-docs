```{index} Crystal-QMMM
```
(sec:multiscalesimulations.cryst-qmmm)=
# CRYSTAL-QMMM

对于扩展体系的模拟，ORCA 提供 CRYSTAL-QMMM 功能：

-   [MOL-CRYSTAL-QMMM](sec:multiscalesimulations.mol-cryst-qmmm) 用于分子晶体。

-   [IONIC-CRYSTAL-QMMM](sec:multiscalesimulations.ionic-cryst-qmmm) 用于半导体和绝缘体。

本节我们介绍两种方法共有的概念和关键词。ORCA 是分子程序，不能进行周期性计算，但 ORCA 过去已经使用嵌入簇模型对离子固体的若干性质进行建模（例如见参考文献 {cite}`Dittmer2019`）。从 ORCA 5 起，我们提供 CRYSTAL-QMMM 方法，它简化了这类嵌入簇计算的设置和运行。用户需要提供一个（足够大的）具有晶体代表性的超胞结构，并提供 QM 原子列表。QM 区域应位于超胞的中心部分。QM 原子嵌入在超胞的其余部分——周围的 MM 原子中，后者由原子中心点电荷表示并影响 QM 计算。如何获得这些电荷将在下一段概述。

(sec:multiscalesimulations.cryst-qmmm-charge-conv)=
## QM 与 MM 区域之间的电荷收敛（Charge Convergence between QM and MM region）

CRYSTAL-QMMM 方法的核心思想是在 QM 和 MM 原子之间达到电荷收敛。为此，MM 电荷与 QM 原子的原子（CHELPG）电荷自洽地更新。这一思想遵循了 `IONIC-CRYSTAL-QMMM` 的参考文献 {cite}`Dittmer2019` 以及 `MOL-CRYSTAL-QMMM` 的参考文献 {cite}`Bjornsson2012` 的工作。

:::{raw} latex
\begingroup
\footnotesize
:::

:::{tabularcolumns} \Y{0.3}\Y{0.2}\Y{0.4}
:::

(tab:multiscalesimulations.cryst-qmmm-charge-conv)=
:::{flat-table} `!IONIC-CRYSTAL-QMMM` 或 `MOL-CRYSTAL-QMMM` 电荷收敛设置的关键词
:class: footnotesize
:header-rows: 1
* - 关键词
  - 选项
  - 说明
* - `Conv_Charges`
  - `true`/`false`
  - 使用电荷收敛方案。默认 `true`。
* - `Conv_Charges_MaxNCycles`
  - `<int>`
  - 电荷收敛方案的最大循环数。MOL-CRYSTAL-QMMM 默认 `30`，IONIC-CRYSTAL-QMMM 默认 `50`。
* - `Conv_Charges_ConvThresh`
  - `<real>`
  - 两个后续电荷收敛循环之间原子类型最大电荷变化量的收敛阈值（默认 `0.01`）。
* - `Scale_FormalCharge_MMAtom`
  - `<real>`
  - CRYSTAL-QMMM 计算 QM 部分所用的 MM 原子电荷按该因子缩放。默认 `1.`。
:::
:::{raw} latex
\endgroup
:::




在优化过程中，电荷收敛方案可以 (i) 仅在最开始使用，(ii) 每 N 个几何步使用一次，或 (iii) 对每个几何步使用，通过下列关键词：

```orca
%geom
  ReConvCharge 1 # default is 1. Redo charge convergence scheme every N steps.
end
```

电荷收敛后，收敛的电荷存储在文件 `basename.convCharges.ORCAFF.prms` 中。它可用于后续计算（使用相同或不同的电子结构设置），配合下列关键词组合：

```orca
!IONIC-CRYSTAL-QMMM    or    !MOL-CRYSTAL-QMMM
%qmmm
  Conv_Charges false
  ORCAFFFilename "firstjob.convCharges.ORCAFF.prms"
end
```

## MM-MM 相互作用（MM-MM Interaction）

与其他多尺度方法（QMMM、QM/QM2、QM/QM2/MM）不同，MM 区域仅作为对 QM 区域的微扰处理。（成键和非成键的）MM-MM 相互作用不予计算——因为它不会影响 QM-MM 相互作用——因此 CRYSTAL-QMMM 计算中的活性区域（优化、频率等）应限制为 QM 区域的原子。

## 准备 CRYSTAL-QMMM 计算（Preparing CRYSTAL-QMMM Calculations）

CRYSTAL-QMMM 计算的输入结构和输入文件可以用 {ref}`sec:utilities.crystalprep` 模块准备。

(sec:multiscalesimulations.mol-cryst-qmmm)=
## MOL-CRYSTAL-QMMM

从概念上讲，我们使用加和式 QM/MM 计算，其中 QM 区域仅通过非键相互作用与 MM 区域相互作用。QM 和 MM 区域之间的 Lennard-Jones 相互作用使用 UFF 力场的 van der Waals 参数计算。QM 与 MM 区域之间的电荷收敛处理从 MM 原子上的零电荷开始，迭代直至 QM 原子（CHELPG）电荷与 MM 点电荷达到收敛。

`MOL-CRYSTAL-QMMM` 方法的结构输入是一个由重复的、相同的分子子单元组成的超胞，即分子的原子顺序应始终相同，一个分子子单元应紧接下一个。`MOL-CRYSTAL-QMMM` 运行所需的最小输入如下所示。

```orca
%qmmm
  NUnitCellAtoms 16      # provide the number of atoms per molecular subunit
  QMAtoms {160:175} end  # QM atoms, should be in central part of the supercell. 
                         # Must be at least one complete molecular subunit.
end
```

:::{admonition} 注意
:class: note
对于分子晶体，假定整个超胞由各自净电荷为零的重复单元组成。QM 区域应由一个或多个这样的电中性单元构成。
:::

### 扩展 QM 区域（Extending the QM Region）

ORCA 可以使用 `HFLayers` 关键词将 QM 区域（我们称之为 QM 核心区域，由原始 `QMAtoms` 输入定义）扩展一层或多层分子子单元。如果使用 `HFLayers` 关键词，QM 核心区域周围指定层数的分子子单元将被加入 QM 区域。QM 核心区域周围的分子子单元层通过距离判据检测。

```orca
%qmmm
  HFLayers 0                       # default 0
  HFLayerGTO "LANL2DZ"             # default. Use this basis set for the 
                                   # HFLayer atoms
  HFLayerECP "HayWadt"             # default. Use these ECPs for the HFLayer atoms
  Conv_Charge_UseQMCoreOnly true   # only use the QM core region for the charge 
                                   # convergence scheme
end
```

HFLayer 可以看作感兴趣的分子子单元（原始 QM 原子）与周围子单元之间的缓冲区域。`HFLayers` 的不同可能用途如下：

-   对于带 `HFLayers` 的 DLPNO 计算，DLPNO 多层特性会自动开启。`HFlayer` 的分子形成一个独立片段，仅在 HF 水平处理，即这些分子不包含在 Post-HF 处理中。

-   `HFLayers` 也可用于非 DLPNO 计算。这种情况下，HFLayer 分子与其他 QM 分子一样包含在 QM 计算中。但这样定义是为那些分子选择不同基组（和 ECP）的便捷方式。

-   可以认为，为 QM 核心区域计算的 QM 电荷比靠近 MM 原子电荷的 HFLayer 原子的电荷更真实。因此，仅使用 QM 核心区域的 QM 原子电荷可为电荷收敛方案提供更真实的电荷。

-   如有必要，HFLayer 的原子可以由用户定义。请确保这里使用完整的分子子单元。

```orca
%qmmm
  HFLayerAtoms {0:15} end
end
```

:::{admonition} 注意
:class: note

术语 `HFLayers` 可能会引起误解。严格来说，只有对使用 `DLPNO` 方法（例如 `DLPNO-CCSD(T)`、`DLPNO-MP2`、`DLPNO-B2PLYP`）的 `MOL-CRYSTAL-QMMM` 计算，HF 层原子才在 HF 水平处理。对其他方法（例如 DFT），HF 层原子与 QM 核心区域原子使用相同的电子结构方法处理。
:::

### 基本用法（Basic Usage）

`MOL-CRYSTAL-QMMM` 计算的示例如下所示：

```orcainput
! MOL-CRYSTAL-QMMM
! PBE def2-SVP Opt NumFreq
%qmmm
 NUnitCellAtoms 13
 QMAtoms {221:233} end                   
 ActiveAtoms {221:233} end  
end
*xyzfile 0 1 Ala_SC.xyz
```

(sec:multiscalesimulations.ionic-cryst-qmmm)=
## IONIC-CRYSTAL-QMMM

从概念上讲，我们使用嵌入簇计算，其中 QM 区域仅与周围 MM 原子点电荷相互作用。与 `MOL-CRYSTAL-QMMM` 不同，QM 与 MM 区域之间的 Lennard-Jones 相互作用不予计算。QM 与 MM 区域之间的电荷收敛处理从初始 MM 电荷（最初从 ORCAFF.prms 文件读取的电荷）开始，迭代直至 QM 原子（CHELPG）电荷与 MM 点电荷达到收敛。

### 边界区域（Boundary Region）

对于离子晶体，需要在 QM 区域与 MM 原子的原子点电荷之间引入边界区域，以避免簇中出现虚假的电子泄漏，并处理 QM 区域表面的悬挂键。该边界区域由封端有效芯势（capped effective core potentials，cECP）构成。这些 cECP 放置在与 QM 区域直接相邻的 MM 原子位置上。ORCA 分析超胞中原子的连接关系，因而能够检测 QM 区域周围的原子层，其中第一层由直接与 QM 原子成键的原子组成，第二层由直接与第一层原子成键的原子组成，依此类推。这些 cECP 的电荷在电荷收敛方案中以与 MM 原子电荷相同的方式确定。

```orca
%qmmm
  ECPLayerECP "SDD"              # cECPs used for the boundary region
  ECPLayers 3                    # Number of cECP layers around the QM region. 
                                 # Default is 3.
  Scale_FormalCharge_ECPAtom 1.  # default is 1. Charges on cECPs are scaled by 
                                 # this factor
end
```

### 扩展 QM 区域（Extending the QM Region）

ORCA 可以使用 `HFLayers` 关键词将 QM 区域（我们称之为 QM 核心区域，由原始 QMAtoms 输入定义）扩展一层或多层原子。如果使用 `HFLayers` 关键词，QM 核心区域周围指定层数的原子将被加入 QM 区域。QM 核心区域周围的原子层以与上述 ECPLayers 相同的方式检测。

```orca
%qmmm
  HFLayers 0                       # default 0
  HFLayerGTO "LANL2DZ"             # default. Use this basis set for the
                                   # HFLayer atoms
  HFLayerECP "HayWadt"             # default. Use these ECPs for the HFLayer atoms
  Conv_Charge_UseQMCoreOnly true   # only use the QM core region for the charge 
                                   # convergence scheme
end
```

HFLayer 可以看作实际感兴趣原子（原始 QM 原子）与周围 cECP 和 MM 点电荷环境之间的缓冲区域。`HFLayers` 的不同可能用途如下：

-   对于带 `HFLayers` 的 DLPNO 计算，DLPNO 多层特性会自动开启。HFLayer 的原子形成一个独立片段，仅在 HF 水平处理，即这些原子不包含在 Post-HF 处理中。

-   可以认为，为 QM 核心区域计算的 QM 电荷比靠近 cECP 和 MM 原子电荷的 HFLayer 原子的电荷更真实，对高电荷体系尤其如此。因此，仅使用 QM 核心区域的 QM 原子电荷可为电荷收敛方案提供更真实的电荷。

-   如有必要，HFLayer 的原子可以由用户定义：

```orca
%qmmm
  HFLayerAtoms {29:35} end
end
```

-   HFLayer 的电荷根据其原子的形式电荷自动计算。如有必要，HFLayer 电荷可以由用户给出。

```orca
%qmmm
  Charge_HFLayer 10 # by default it is computed automatically based on the 
                    # formal charges from the ORCAFF.prms file
end
```

:::{admonition} 注意
:class: note

术语 `HFLayers` 可能会引起误解。严格来说，只有对使用 DLPNO 方法（例如 `DLPNO-CCSD(T)`、`DLPNO-MP2`、`DLPNO-B2PLYP`）的 `IONIC-CRYSTAL-QMMM` 计算，HF 层原子才在 HF 水平处理。对其他方法（例如 DFT），HF 层原子与 QM 核心区域原子使用相同的电子结构方法处理。
:::

### 整个超胞的净电荷（Net Charge of the Entire Supercell）

对于离子晶体，QM 区域（以及整个超胞）可以由每种原子类型数目不等的原子组成。因此，QM 区域可能具有非零净电荷。结果，在电荷收敛方案中为 MM 原子指派原子点电荷时，QM 区域电荷、ECP 层电荷与 MM 原子原子电荷之和可能偏离超胞的理想电荷。为强制超胞的理想电荷，整个体系的总电荷通过等量移动所有 MM（包括边界）原子的电荷来强制实现。

```orca
%qmmm
  Charge_Total  0         # default 0. Total charge of the supercell
  EnforceTotalCharge true # enforce the total charge by shifting MM charges
end
```

可以通过定义 `OuterPCLayers` 的数目，将电荷移动过程限制在超胞外部的 MM 原子上。如果 `OuterPCLayers` 设为 1，则只有超胞最外层的原子（根据原子的连接关系识别）包含在电荷移动过程中。如果 `OuterPCLayers` 大于 2，则与最外层相连的原子也额外包含在电荷移动过程中，依此类推。

```orca
%qmmm
  OuterPCLayers 0         # default 0, i.e. charge shifting for all MM atoms
end
```

:::{admonition} 注意
:class: note

QM 核心区域的电荷可以选择自动指派。这会覆盖 xyz 或 pdb 部分中给出的电荷。

```orca
%qmmm
  AutoDetectQCCharge false # default is false
end
```
:::

### 示例输入（Example Input）

`IONIC-CRYSTAL-QMMM` 计算的最小示例如下所示：

```orcainput
! IONIC-CRYSTAL-QMMM 
! NMR
! PBE pcSseg-2 def2/JK def2-svp/C
%qmmm
  QMAtoms {0:6} end
  ORCAFFFilename "nacl6.ORCAFF.prms"
  CHARGE_TOTAL    0
end
*xyzfile -5 1 nacl6.xyz
```

(sec:multiscalesimulations.ionic-cryst-pdb)=
### 存储在 PDB 文件中的不同 QM 和 MM 区域（Different QM and MM regions Stored in the PDB file）

存储的 PDB 文件在其 occupancy 列中包含下列条目。

(tab:multiscalesimulations.ionic-cryst-pdb-occ)=
:::{table} Ionic-Crystal-QMMM 计算中存储在 pdb 文件中的条目定义。
:class: normalsize
| 数值         | 说明       |
|:----------------|:----------------|
| `0` | 由周围点电荷模拟的 MM 原子 |
| `1` | QM 核心区域原子 |
| `2` | HFLayer 原子 |
| `3` | cECP |
| `4` | OuterPCLayer 原子（MM 原子的子集）（若已定义），是在强制总电荷的电荷移动过程中唯一使用的原子 |
:::
