```{index} QMMM, ONIOM
```
(sec:multiscalesimulations.qmmm.orca)=
# ORCA 多尺度实现概述（Overview on ORCA's Multiscale Implementation）

ORCA 提供五种主要方法，适用于蛋白质、DNA、大分子、显式溶剂化和晶体固体等多种应用：

-   [加和式 QM/MM](sec:multiscalesimulations.add_qmmm) 用于蛋白质和 DNA/RNA。

-   [QM1/QM2](sec:multiscalesimulations.oniom2)（2 层 ONIOM）用于小蛋白质、RNA、大分子和显式溶剂化。

-   [QM1/QM2/MM](sec:multiscalesimulations.oniom3)（3 层 ONIOM）用于蛋白质和 DNA/RNA。

-   [MOL-CRYSTAL-QMMM](sec:multiscalesimulations.mol-cryst-qmmm) 用于分子晶体。

-   [IONIC-CRYSTAL-QMMM](sec:multiscalesimulations.ionic-cryst-qmmm) 用于半导体和绝缘体。

所有方法都与其他 ORCA 模块无缝集成，简化了多尺度计算的准备和执行。

多尺度特性与 ORCA 6.1 中可用的所有其他模块和工具都实现了最优连接，使用户能够以 QM 为中心的视角，用简单高效的方式处理多尺度计算，重点简化准备、设置和运行多尺度计算的过程。自 6.1 版起，ORCA 提供了一个自动设置 QM 和活性区域的工具，描述见[此处](sec:multiscalesimulations.qmmm-regions-automated)。

从输入的角度看，所有方法共享一组共同的概念和关键词，本节将予以概述。
后续章节将描述不同方法并讨论更多输入选项。

## 将多尺度特性与其他 ORCA 特性结合（Combining Multiscale Features with other ORCA Features）

多尺度特性可以与所有其他可能的 ORCA 方法一起使用：

-   **单点计算（Single Point Calculations）**：使用各种可用的电子结构方法作为 QM 方法。

-   **优化（Optimization）**：使用各种[几何优化](sec:structurereactivity.optimization)，
    包括各种约束、TS 优化、弛豫势能面扫描以及 ScanTS 特性。使用 L-Opt 和 L-OptH 特性，包括与各种片段优化（固定片段、弛豫片段、仅弛豫片段中的特定元素、将片段作为刚体处理）的组合。

-   **过渡态与最小能量路径（Transition States and Minimum Energy Paths）**：使用各种[微动弹性带计算](sec:structurereactivity.optimization.neb)（Fast-NEB-TS、NEB、NEB-CI、NEB-TS，包括其 ZOOM 变体）以及内禀反应坐标计算。（`MOL-CRYSTAL-QMMM` 和 `IONIC-CRYSTAL-QMMM` 未实现）

-   **构象搜索（Conformational Searches）**：构象搜索可用 ORCA 的 [GOAT](sec:structurereactivity.GOAT) 模块运行。

-   **频率计算（Frequency Calculations）**：使用常规[频率计算](sec:structurereactivity.frequencies)。如有需要，ORCA 会自动开启 {ref}`sec:structurereactivity.geomopt.partialhess`
    （PHVA）{cite}`li2002theor` 计算。（`IONIC-CRYSTAL-QMMM` 未测试）

-   **分子动力学（Molecular Dynamics）**：使用[分子动力学](sec:moldyn)（MD）模块进行 QM/MM 的 Born-Oppenheimer MD
    （BOMD），可与各种电子结构方法结合。（`MOL-CRYSTAL-QMMM` 和
    `IONIC-CRYSTAL-QMMM` 未实现）

-   **性质计算（Property Calculation）**：各种常规性质计算均可使用。对于
    静电嵌入，电子密度会被周围的点电荷自动微扰。

-   **激发态计算（Excited State Calculations）**：使用各种[激发态计算](sec:spectroscopyproperties.tddft)（TD-DFT、EOM、单点计算、优化、频率）。

## 多尺度模拟所需的设置（Required Settings for a Multiscale Simulation）

下面介绍基本概念。

-   **QM 原子（QM atoms）**：用户可以直接定义 QM 区域，也可以通过 pdb 文件中的标记定义。见 {ref}`sec:multiscalesimulations.qmmm-regions`。关于以最少用户输入自动构建 QM 区域，见[此处](sec:multiscalesimulations.qmmm-regions-automated)。

-   **活性原子（Active Atoms）**：用户可以选择活性区域，例如对几何优化是被优化的原子，对频率计算是 PHVA 中允许振动的原子，对 MD 运行是被推进的原子。更多背景信息见[此处](sec:multiscalesimulations.qmmm-active)。
    关于如何以[自动](sec:multiscalesimulations.qmmm-regions-automated)方式或以[显式](sec:multiscalesimulations.qmmm-regions-explicit)方式定义活性区域的输入选项见下文。

ONIOM2 类型计算的最小用户输入如下所示。

```orca
!QM/XTB
%qmmm
  QMCoreAtoms {7 12} end
  ActiveCoreAtoms {7 12} end
end
*xyz 0 1
...
```

多尺度模拟中常常需要处理的其他方面会自动处理，并有合理的默认值——当然也可以由用户控制。
**边界处理**（即 QM 与 MM 区域之间必须切断的键）和过极化的处理在段落 {ref}`sec:multiscalesimulations.qmmm-boundary` 中介绍。
可用的**嵌入类型**在章节 {ref}`sec:multiscalesimulations.qmmm-embedding` 中讨论。
**QM2 原子**（在 3 层 ONIOM 计算中定义低水平区域）在章节 {ref}`sec:multiscalesimulations.oniom-qm2atoms` 中讨论。

关于不同可用输入和运行选项以及额外关键词（见
{ref}`sec:multiscalesimulations.qmmm-keywords`）的详细信息见下文。

:::{admonition} 注意
:class: note
为检查 ORCA 所做的多尺度设置而无需运行完整模拟，可以调用关键词 `! QMMMSetup`。
这会确保 ORCA 在多尺度准备后停止。关于 QMMM 设置的信息会打印在输出中，
并存储包含链接原子的 QM 区域文件（`basename_QM.xyz`）。
:::

(sec:multiscalesimulations.qmmm-regions)=
## QM 区域与活性区域的定义（QM and Active Region Definition）

QM 和活性区域的原子可以用三种不同方式定义：

-   显式定义所有原子索引。
-   定义最重要的原子（`core` 原子），由 ORCA 确定完整的 QM 和活性区域。
-   在 pdb 文件中定义。

(sec:multiscalesimulations.qmmm-regions-explicit)=
### QM 与活性区域的显式定义（Explicit Definition of QM and Active Region）
QM 和活性区域可以直接在输入中定义，如下例所示：

```orca
%qmmm                  
 QMAtoms {0 1 2 27 28} end      # lists of atoms (counting starts from 0) or
 ActiveAtoms {0:5 16 21:30} end # ranges of atoms (range defined via start:end)
end        
*pdbfile 0 1 ubq.pdb
```

(sec:multiscalesimulations.qmmm-regions-automated)=
### QM 与活性区域的自动定义（Automated Definition of QM and Active Region）

QMMM 科学文献中定义 QM 和活性区域的标准方法包括：

#### 识别重要原子或官能团（Identifying Important Atoms or Functional Groups）

示例包括：
- 直接参与成键或断键的原子。
- 对光谱至关重要的官能团。
- 催化活性核心的金属离子。
- 与蛋白质结合的整个分子或配体。
- *必要时的其他判据。*

#### 包含周围原子（Including Surrounding Atoms）

- 包含这些重要原子周围某一给定空间距离内的所有原子。

#### 应用规则以避免伪影（Applying Rules to Avoid Artifacts）

具体确保：
- QM 与 MM 区域之间的边界切断非极化的单键。
- 两个 QM-MM 切断点之间的拓扑距离（MM 间隙）足够大，
- 防止链接原子放置过近。

---

#### ORCA 6.1 中的自动流程（Automated procedure in ORCA 6.1）
在 ORCA 6.1 中，开发了一种自动方案来管理这一多步过程。
用户只需指定定义 QM 和活性区域核心部分的关键原子（**core** 原子）。

ORCA 需要：
- 体系**拓扑**的知识。
- 体系内**官能团**的信息。

利用新引入的[片段化流程](sec:essentialelements.fragmentation)，ORCA
在计算开始时自动确定这些信息。官能团根据用户选定的片段化流程存储为单独的片段。

#### 自动流程的步骤（以 QM 区域为例；活性区域的步骤类似）

1. 接受用户定义的输入 `QMCoreAtoms`。
2. 若 `QMCore_Type` 为 `Fragments`，将 `QMCoreAtoms` 扩展到完整片段，产生更新后的 `QMCoreAtoms` 集合。
3. 确定 `QMCoreAtoms` 周围 `QMCore_Extension` Å 内的所有原子，得到 `QMAtoms`。
4. 若 `QMCoreExtension_Type` 为 `Fragments`，将 `QMAtoms` 扩展到完整片段，再次更新该集合。
5. 将任何显式由用户定义的原子（`QMAtoms`）包含到自动生成的集合中。
6. 若 `CheckAutoFragForQMGaps` 为 `true`，验证拓扑上接近的 QM 原子之间没有少于 `QMGap_MinLength` 个 MM 原子的间隔。若有，则将必要的连接片段加入 `QMAtoms`。
7. 若 `CheckAutoFragBoundaries` 为 `true`，确保 QM-MM 边界不切断极化的或有问题的键。
8. 重复步骤 6 和 7，直到不再需要添加片段为止。

:::{admonition} 注意
:class: note
可以在输入中添加关键词 `QMMMSetup`。这样可以检查自动生成的 QM 区域（`basename_QM.xyz`）并验证实际多尺度计算所需的电荷和多重度。
:::

自动 QM 和活性区域设置可以在输入中定义，如下例所示：

```orca
! QM/XTB
! QMMMSetup # just do the preparation and stop
%qmmm
 QMCoreAtoms {2032} end
 ActiveCoreAtoms {2032} end
 frag
   FragProc NABackbone, NASideChains, FunctionalGroups, Extend, Connectivity
 end
end

*xyz 0 1
```
(fig:qmmm-autofrag_rna)=
```{figure} ../../images/qmmm-autofrag_rna.png
:width: 70%
QMCoreAtom 2032 的 QM 区域。左侧是以球棍模型表示的、作为卡通风格完整体系一部分的 QM 区域，右侧是包含链接原子的 QM 区域。
```
在上面的例子中（一个与 RNA 结合的配体），我们首先使用 [fragmentator](sec:essentialelements.fragmentation)（片段化工具）用 RNA 特有的基团和（配体的）官能团定义片段，然后围绕该配体构建 QM 和活性区域（原子 2032 是配体的一个原子）。

```orca
! QMMMSetup # just do the preparation and stop
! QMMM
%qmmm
  ORCAFFFilename "reactant.ORCAFF.prms"
  QMCoreAtoms {183 2745} end
  ActiveCoreAtoms {183 2745} end
  frag
    FragProc SEQBACKBONE, AASCFINEGRAINED, FUNCTIONALGROUPS, EXTEND, Connectivity
    UseTopology true
    TopolFile "reactant.ORCAFF.prms"
  end
end
*pdbfile 0 1 reactant.pdb
```

(fig:qmmm-autofrag_prot)=
```{figure} ../../images/qmmm-autofrag_prot.png
:width: 70%
QMCoreAtoms 183 和 2745 的 QM 区域。左侧是以球棍模型表示的、作为卡通风格完整体系一部分的 QM 区域，右侧是包含链接原子的 QM 区域。
```
在上面的例子中（涉及共价结合在蛋白质活性位点内的配体），我们首先使用 [fragmentator](sec:essentialelements.fragmentation)（片段化工具）定义片段，为配体和辅因子指定蛋白质特有基团和官能团。然后围绕直接参与共价结合过程的两个关键原子构建 QM 和活性区域：来自 Cys 残基的原子 `183`，以及来自共价结合配体的原子 `2745`。

:::{raw} latex
\begingroup
\footnotesize
:::

:::{tabularcolumns} \Y{0.4}\Y{0.2}\Y{0.4}
:::

(tab:multiscalesimulations.qmmm-autofrag_keywords)=
:::{flat-table} 自动定义 QM 和活性区域的选项。
:class: footnotesize
:header-rows: 1
* - 关键词
  - 选项
  - 说明
* - `QMCOREATOMS`
  - `{ints...}`
  - 定义 QM 区域的核心原子。单个索引可写作 `int int`。原子索引范围可写作 `int:int`。所有这些可以组合使用。
* - `ACTIVECOREATOMS`
  - `{ints}`
  - 定义活性区域的核心原子。
* - `Frag`
  - 如[此处](sec:essentialelements.fragmentation)所定义
  - 
* - `QMCore_Type`
  - `Fragments`
  - （默认）将用户定义的原子加上它们所属片段的全部原子作为 QM 核心。
* - 
  - `Atoms`
  - 仅将用户定义的原子作为 QM 核心。
* - `QMCoreExtension_Type`
  - `Fragments`
  - （默认）将属于这样片段的原子作为 `QMAtoms`：这些片段至少有一个原子到任一 `QMCoreAtoms` 的距离小于 `QMCore_Extension`。
* - 
  - `Atoms`
  - 将到任一 `QMCoreAtoms` 的距离小于 `QMCore_Extension` 的原子作为 `QMAtoms`。
* - `QMCore_Extension`
  - `real`
  - QM 核心扩展以得到 `QMAtoms` 的距离。默认 `3.`。
* - `CheckAutoFragForQMGaps`
  - `true`/`false`
  - 检查两个 QM 原子之间是否存在 QM 间隙，即它们在拓扑上通过超过 `QMGap_MinLength` 个 MM 原子连接；若是，则将连接片段加入 `QMAtoms`。
* - `QMGap_MinLength`
  - `0` 到 `6`
  - 两个 QM 原子之间的拓扑距离，决定连接的 MM 原子是否被视为 QM 间隙。默认 `3`。
* - `CheckAutoFragBoundaries`
  - `true`/`false`
  - 检查 QM-MM 键是否为非极性单键。若不是，则将该 MM 原子的片段加入 `QMAtoms`。
* - `ActiveCore_Type`
  - `Fragments`
  - （默认）将用户定义的原子加上它们所属片段的全部原子作为活性核心。
* - 
  - `Atoms`
  - 仅将用户定义的原子作为活性核心。
* - `ActiveCoreExtension_Type`
  - `Fragments`
  - （默认）将属于这样片段的原子作为 `ActiveAtoms`：这些片段至少有一个原子到任一 `ActiveCoreAtoms` 的距离小于 `ActiveCore_Extension`。
* - 
  - `Atoms`
  - 将到任一 `ActiveCoreAtoms` 的距离小于 `ActiveCore_Extension` 的原子作为 `ActiveAtoms`。
* - `ActiveCore_Extension`
  - `real`
  - 活性核心扩展以得到 `ActiveAtoms` 的距离。默认 `5.`。
* - `CheckAutoFragForQMGaps_Active`
  - `true`/`false`
  - 检查两个活性原子之间是否存在间隙，即它们在拓扑上通过超过 `QMGap_MinLength` 个非活性原子连接；若是，则将连接片段加入 `ActiveAtoms`。
* - `CheckAutoFragBoundaries_Active`
  - `true`/`false`
  - 检查活性-非活性键是否为非极性单键。若不是，则将该非活性原子的片段加入 `ActiveAtoms`。
:::
:::{raw} latex
\endgroup
:::


:::{admonition} 注意
:class: note
自动设置可以与通过 `QMAtoms` 和 `ActiveAtoms` 显式定义 QM 或活性原子相结合。
:::

(sec:multiscalesimulations.qmmm-regions-pdb)=
### 通过 pdb 文件定义 QM 与活性区域（Definition of QM and Active Region via pdb file）
QM 和活性区域可以在 pdb 文件中定义，如下例所示：

```orca
%qmmm
 Use_QM_InfoFromPDB true     # get the QMAtoms and ActiveAtoms definition from 
 Use_Active_InfoFromPDB true # the pdb file. The default for both is false.
                             # If InfoFromPDB is set to true, the QMAtoms or 
                             # ActiveAtoms input is ignored
end
*pdbfile 0 1 ubq.pdb
```

如果 `Use_QM_InfoFromPDB` 或 `Use_Active_InfoFromPDB` 设为 true，则应使用 pdb 文件作为结构输入。QM 原子通过 occupancy 列中的 1 定义，MM 原子通过 0 定义。活性原子通过 B-factor 列中的 1 定义，非活性原子通过 0 定义。

```orca
ubq.pdb:
...
ATOM    327  N   ASP A  21      29.599  18.599   9.828  0.00  0.00      P1   N
ATOM    328  HN  ASP A  21      29.168  19.310   9.279  0.00  0.00      P1   H
ATOM    329  CA  ASP A  21      30.796  19.083  10.566  0.00  1.00      P1   C
ATOM    330  HA  ASP A  21      31.577  18.340  10.448  0.00  1.00      P1   H
ATOM    331  CB  ASP A  21      31.155  20.515  10.048  2.00  1.00      P1   C
ATOM    332  HB1 ASP A  21      30.220  21.082   9.865  2.00  1.00      P1   H
ATOM    333  HB2 ASP A  21      31.754  21.064  10.801  2.00  1.00      P1   H
ATOM    334  CG  ASP A  21      31.923  20.436   8.755  1.00  1.00      P1   C
ATOM    335  OD1 ASP A  21      32.493  19.374   8.456  1.00  1.00      P1   O
ATOM    336  OD2 ASP A  21      31.838  21.402   7.968  1.00  1.00      P1   O
ATOM    337  C   ASP A  21      30.491  19.162  12.040  0.00  0.00      P1   C
ATOM    338  O   ASP A  21      29.367  19.523  12.441  0.00  0.00      P1   O
...
```

:::{admonition} 注意
:class: note
与 PDB 文件的 hybrid36 标准不同，ORCA 写出非标准 pdb 文件的方式为：

-   原子 1-99,999 用十进制数表示

-   原子 100,000 及以上用十六进制数表示，原子 100,000
    对应索引 186a0。

这确保了索引的唯一映射。如果要在十六进制空间中选择一个原子（索引大于 100,000），在 ORCA 输入文件中选择该索引时请将十六进制数转换为十进制。另请注意，在 pdb 文件中计数从 1 开始，而在 ORCA 中计数从零开始。
:::

(sec:multiscalesimulations.qmmm-active)=
## 活性原子与优化、频率计算、MD 的结合（Active Atoms in Combination with Optimization, Frequency Calculation, MD）

多尺度计算的体系可能相当大，含有数万乃至数十万个原子。在多尺度计算中，感兴趣的区域往往只是体系的特定部分，常见做法是将优化限制在体系的一小部分，我们称之为活性区域（active region）= 体系的活性部分。关于如何定义活性区域的信息见 {ref}`sec:multiscalesimulations.qmmm-regions`。
通常这部分活性区域由数百个原子组成，定义为 QM 区域加上 QM 区域周围的一层。对频率计算同样适用这一定义，尤其是因为优化后非活性原子不在驻点上，在这种情况下频率计算会导致伪影。对含数十万原子体系的 MD 计算没有问题，但在某些应用中区分活性和非活性部分可能很重要（例如溶剂液滴中的溶质，溶剂外壳被冻结）。

:::{admonition} 注意
:class: note
如果未定义活性原子，则整个体系按活性处理。
:::

:::{admonition} 注意
:class: note
活性区域定义也适用于 MM 计算，但必须通过 `%qmmm` 块提供。
:::

### 在冗余内坐标中的优化（Optimization in redundant internal coordinates）

在 ORCA 的 QM/MM 几何优化中，只优化活性原子的位置。不过，这些活性原子上的力仍受与周围非活性原子相互作用的影响。为了在内坐标的准牛顿优化算法中获得平滑的优化收敛，需要活性原子与直接周围非活性原子之间的 Hessian 值。为此，活性原子扩展了一层周围的非活性原子，它们也包含在几何优化中，但其位置受约束，见
{numref}`fig:QMMM_ActiveRegion`。这层原子可以由 ORCA 自动选择。有三个可用选项：

:::{raw} latex
\begingroup
\footnotesize
:::

:::{tabularcolumns} \Y{0.25}\Y{0.2}\Y{0.55}
:::

(tab:multiscalesimulations.qmmm-activeatoms_extend)=
:::{flat-table} 扩展活性区域的选项。
:class: footnotesize
:header-rows: 1
* - 关键词
  - 选项
  - 说明
* - `EXTENDACTIVEREGION`
  - `DISTANCE`
  - （默认）参数 `Dist_AtomsAroundOpt` 控制哪些非活性原子包含在扩展壳层中，即距离小于其 VDW 半径之和加 `Dist_AtomsAroundOpt` 的非活性原子被包含在内。
* - 
  - `COV_BONDS`
  - 与活性原子共价键合的全部（非活性）原子被包含在内。
* - 
  - `NO`
  - 不包含任何非活性原子。
:::
:::{raw} latex
\endgroup
:::

用户也可以手动提供扩展壳层的原子。这将在章节 {ref}`sec:multiscalesimulations.qmmm-active-freq` 中讨论。

(fig:QMMM_ActiveRegion)=
```{figure} ../../images/QMMM_ActiveRegion.*

活性和非活性原子。另外还显示了扩展壳层，
它由距离活性原子较近的非活性原子组成。
扩展壳层用于内坐标中的优化和 PHVA。
```

活性原子的集合称为 'activeRegion'，活性原子加上周围非活性原子的集合称为
'activeRegionExt'。在几何优化过程中存储下列轨迹（可以关闭）：

:::{raw} latex
\begingroup
\small
:::
(tab:multiscalesimulations.qmmm-opt-trjfiles)=
:::{flat-table} 优化过程中包含轨迹的文件。
:class: small
* - 文件名
  - 说明
* - `basename_trj.xyz`
  - 整个 QM/MM 体系
* - `basename.QMonly_trj.xyz`
  - 仅 QM 区域
* - `basename.activeRegion_trj.xyz`
  - 仅活性原子
* - `basename.activeRegionExt_trj.xyz`
  - 活性原子加上扩展
:::
:::{raw} latex 
\endgroup
:::

下列文件在请求时存储优化后的结构：

:::{raw} latex
\begingroup
\small
:::

(tab:multiscalesimulations.qmmm-opt-files)=
:::{flat-table} 包含优化后结构的文件。
:class: small
* - 文件名
  - 说明
* - `basename.pdb`
  - 优化后的 QM/MM 体系，pdb 文件格式
* - `basename.xyz`
  - 优化后的 QM/MM 体系
* - `basename.QMonly.xyz`
  - 仅 QM 区域
* - `basename.activeRegion.xyz`
  - 仅活性原子
* - `basename.activeRegionExt.xyz`
  - 活性原子加上扩展
:::
:::{raw} latex
\endgroup
:::

(sec:multiscalesimulations.qmmm-lopt)=
### 使用笛卡尔 L-BFGS 极小化器的优化（Optimization with the Cartesian L-BFGS Minimizer）

对于非常大的活性区域，内坐标中的准牛顿优化可能代价高昂。使用 `L-Opt` 或 `L-OptH` 特性可能更有利，见章节
{ref}`sec:structurereactivity.optimization.lbfgs`。
在多尺度模拟的背景下，将体系的部分或整个分子视为刚体也很有用。
例如，可以优化蛋白质和水分子的氢原子位置，同时将没有精确成键参数的非标准分子作为刚体弛豫。
该背景下的可用选项见 {ref}`sec:structurereactivity.optimization.rigidbody`。
示例如下：

```orca
!QMMM L-OptH
%qmmm
 QMAtoms {22397:22423} end
 ORCAFFFilename "DNA_hexamer.ORCAFF.prms"
end
*pdbfile 0 1 DNA_ligand.pdb

%frag 
 Definition
  1 {22307:22396} end # cofactor
  2 {22397:22423} end # ligand
 end
end

%geom 
 RigidFrags {1 2} end # treat cofactor and ligand as individual rigid bodies
end
```

(sec:multiscalesimulations.qmmm-active-freq)=
### 频率计算（Frequency Calculation）

如果所有原子都是活性的，请求 `!NumFreq` 时执行常规频率计算。如果 QM/MM 体系中还有非活性原子，则自动选择 {ref}`sec:structurereactivity.geomopt.partialhess`（PHVA）。此时，PHVA 对上述定义的 `activeRegionExt` 执行，其中扩展壳层原子自动用作“冻结”原子。请注意，由于 MM 计算缺少解析二阶导数，解析 Hessian 不可用。请注意，在优化之后的新计算中，新自动生成的扩展活性区域可能与优化前的区域不同。这意味着当使用先前计算的 Hessian（例如在优化或 NEB-TS 运行结束时）时，Hessian 与新的扩展活性区域不匹配。ORCA 尝试通过从 `.hess` 文件获取扩展区域的信息来解决这个问题。如果这不起作用（例如在 Hessian 计算之后使几何结构发生畸变），您应手动提供扩展活性区域的原子列表。这通过下列关键词完成：

```orca
%qmmm
 OptRegion_FixedAtoms {27 1288:1290 4400} end  # manually define the 
                                               # activeRegionExt atoms.
end
```

请注意，ORCA 在计算 Hessian 的那次计算输出中确实打印了必要信息：

```orca
Fixed atoms used in optimizer          ... 27 1288 1289 1290 4400
```

(sec:multiscalesimulations.qmmm-neb)=
### 微动弹性带计算（Nudged Elastic Band Calculations）

NEB 计算（章节 {ref}`sec:structurereactivity.neb`）可以与多尺度特性结合执行，例如用于研究酶催化。在多尺度 NEB 计算开始时自动构建扩展壳层时，不仅使用主输入结构（'reactant'）的坐标，还使用 'product' 以及（如果有的话）'transition state guess' 的原子坐标来确定活性区域扩展壳层的并集。对于大体系，建议对 NEB 计算使用活性区域特性。

:::{admonition} 注意
:class: note

反应物、产物以及（如果有的话）过渡态猜测的非活性原子位置应当相同。
:::

### 分子动力学（Molecular Dynamics）

如果多尺度体系中有活性和非活性原子，MD 运行中只有活性原子被推进。如果所有原子都是活性的，则推进所有原子。关于输出和轨迹选项的更多信息，见
章节 {ref}`moldyn:sec_regions`。

(sec:multiscalesimulations.qmmm-boundary)=
## 边界区域（Boundary Region）

本节对 QM/MM、QM/QM2 和 QM/QM2/MM 方法很重要。
对最后一种方法，存在两个边界区域（QM 与 QM2 之间以及 QM2 与 MM 区域之间），两者都可能穿过共价键。下面我们只讨论 QM 与 MM 之间边界的概念，但对另外两个边界同样适用。

### 链接原子（Link Atoms）

ORCA 根据 QM 区域的信息和体系的拓扑（基于 `ORCAFF.prms` 文件）自动生成链接原子。ORCA 将链接原子放置在 QM 与 MM 原子之间的键上。

:::{admonition} 重要
:class: important

定义 QM、QM2 和 MM 区域时，请确保只切断单键（而不是芳香键、双键、三键等）。
:::

QM 原子与链接原子之间的距离通过**键长缩放因子**（相对于 QM-MM 键长）确定，该因子计算为 QM 与氢原子之间平衡键长（$d_{QM-H}$）与 QM 与 MM 原子之间平衡键长（$d_{QM-MM}$）之比。

对于**与氢的平衡键长**，ORCA 对边界区域中最常见原子（C、N、O）使用表格化的标准值，可通过下文定义的关键词修改。ORCA 将这些值即时存储在一个简单文件中（`basename.H_DIST.prms`）。如有必要，用户可以按原子修改这些值，或在文件中添加其他值并将该文件作为输入提供给 ORCA（另见
段落 {ref}`sec:modelchemistries.mm-orcaforcefield-getHDist`）。对于 QM/QM2 和 QM/QM2/MM 方法，与氢的平衡键长是显式计算的。

```orca
%qmmm
# standard equilibrium bond lengths with hydrogen can be modified
 Dist_C_HLA 1.09        # d0_C-H
 Dist_O_HLA 0.98        # d0_O-H
 Dist_N_HLA 0.99        # d0_N-H 
# file can be provided which provides the used d0_X-H values specific to all atoms
 H_Dist_FileName "QM_H_dist.txt"
end
```

### QM-MM 边界处的成键相互作用（Bonded Interactions at the QM-MM Boundary）

在加和式耦合方案中，QM 区域内的 MM 成键相互作用被忽略。但在边界处，建议使用一些包含 QM 原子的特定成键相互作用。默认情况下，ORCA 只忽略边界处那些仅涉及一个 MM 原子的成键相互作用，即所有 QM1-MM1 类型的键、QM2-QM1-MM1 类型的弯曲以及 QM3-QM2-QM1-MM1 类型的扭转。其他 QM-MM 混合成键相互作用（涉及两个以上 MM 原子）则被包含。用户可以包含上述相互作用，这通过下列关键词控制：

```orca
%qmmm
 DeleteLADoubleCounting true     # Neglect bends (QM2-QM1-MM1) and torsions 
                                 # (QM3-QM2-QM1-MM1). Default true. 
 DeleteLABondDoubleCounting true # Neglect bonds (QM1-MM1)
end
```

### 电荷改性（Charge Alteration）

如果 QM 和 MM 原子通过键相连（在拓扑文件中定义），则必须修改邻近 MM 原子（及其相邻原子）的电荷，以防止链接原子和 QM 区域电子密度的过极化。这一电荷改性由 ORCA 在 `%qmmm` 块中自动处理。ORCA 提供了可用于防止过极化的最常用方案。

:::{raw} latex
\begingroup
\footnotesize
:::

:::{tabularcolumns} \Y{0.2}\Y{0.2}\Y{0.6}
:::

(tab:multiscalesimulations.qmmm-chargealteration)=
:::{flat-table} 修改 QM-MM 边界处电荷以防过极化的选项。
:class: footnotesize
:header-rows: 1
* - 关键词
  - 选项
  - 说明

* - `ChargeAlteration`
  - `CS`
  - （默认）电荷移动（Charge Shift）——将 MM 原子的电荷移到 MM2 原子上，使总电荷守恒。

* -
  - `RCD`
  - 重新分配电荷与偶极（Redistributed Charge and Dipole）——移动 MM 原子的电荷，使总电荷和偶极守恒。

* -
  - `Z0`
  - 保持电荷不变。该 MM 原子很可能导致过极化。

* -
  - `Z1`
  - 删除 MM1 原子上的电荷（不守恒总电荷）。

* -
  - `Z2`
  - 删除 MM1 原子及其第一层（MM2）近邻上的电荷（不守恒总电荷）。

* -
  - `Z3`
  - 删除 MM1 原子及其第一层（MM2）和第二层（MM3）近邻上的电荷（不守恒总电荷）。

* - `Scale_RCD`
  - `real`
  - 对 `RCD` 方案，定义移动后的电荷在 MM1 与 MM2 之间键上的位置。默认：`0.5`，即中点。

* - `Scale_CS`
  - `real`
  - 对 `CS` 方案，定义移动后的电荷在 MM2 与 MM1/MM3 之间键上的位置。默认：`0.06 × bond`。
:::
:::{raw} latex
\endgroup
:::


(sec:multiscalesimulations.qmmm-embedding)=
## 嵌入类型（Embedding Types）

有两种嵌入方案可用于处理高水平和低水平区域之间的静电相互作用。
在静电嵌入方案中，QM 与 MM 体系之间的静电相互作用在 QM 水平计算。
因此，MM 原子（或其他低水平方法）的电荷分布可以极化 QM 区域的电子密度。可用的嵌入方案如下：

:::{raw} latex
\begingroup
\footnotesize
:::

:::{tabularcolumns} \Y{0.2}\Y{0.2}\Y{0.6}
:::

(tab:multiscalesimulations.qmmm-embedding)=
:::{flat-table} 处理高低水平区域之间静电相互作用的嵌入方案选项。
:class: footnotesize
:header-rows: 1

* - 关键词
  - 选项
  - 说明

* - `Embedding`
  - `Electrostatic`
  - （默认）QM 与 MM 体系之间的静电相互作用在 QM 水平计算。

* -
  - `Mechanical`
  - QM 与 MM 体系之间的静电相互作用在 MM 水平计算。
:::
:::{raw} latex
\endgroup
:::



:::{admonition} 重要
:class: important
在 QMMM 中，QM 与 MM 体系之间的 LJ 相互作用始终在 MM 水平计算。

:::

在静电嵌入方案中，MM 部分产生的静电势的求值可以通过使用 FMM 算法加速（见参考文献 {cite}`Greengard1987`）。这将加快 Fock 矩阵的构建。默认推荐的设置可以直接在关键词行使用 FMM-QMMM 关键词调用。不过，关于算法参数和所有输入选项的更多细节可参见（另见段落 {ref}`sec:multiscalesimulations.fmm`）

```orca
! FMM-QMMM
```
建议只要 MM 部分由超过 10,000 个原子（或 ECM 方法的点电荷）组成，就使用该选项。

(sec:multiscalesimulations.qmmm-keywords)=
## 额外关键词（Additional Keywords）

这里列出可以从 `%qmmm` 块中访问、且与 QM/MM 计算相关的额外关键词和选项。
其中一些关键词也可以通过 `%mm` 块访问，见
章节 {ref}`sec:modelchemistries.mm-keywords`。

```orca
!QMMM
%qmmm

# The extended active region, activeRegionExt, contains the atoms surrounding the 
# active atoms.
 ExtendActiveRegion distance  # rule to choose the atoms belonging 
                              # to activeRegionExt.
                              # no - do not use activeRegionExt atoms
                              # cov_bonds - add only atoms bonded covalently to 
                              # active atoms
                              # distance (default) - use a distance criterion (VDW 
                              # distance plus Dist_AtomsAroundOpt)
 Dist_AtomsAroundOpt 0.0      # in Angstrom (Default 0). Meaning only freeze atoms
                              # which touch the active atoms by their VDW spheres.
                              # only needed for ExtendActiveRegion distance
 OptRegion_FixedAtoms {27 1288:1290 4400} end  # manually define the
                                               # activeRegionExt atoms.
                                               # Default: empty list. 
                                               
# Printing options. All are true by default.
 PrintLevel 1               # Can be 0 to 4, 0=nothing, 1=normal, ...
 PrintOptRegion true        # Additionally print xyz and trj for opt region
 PrintOptRegionExt false    # Additionally print xyz and trj for extended 
                            # opt region
 PrintQMRegion true         # Additionally print xyz and trj for QM region
 PrintFullTRJ true          # Print trajectory of full system. Default true.
 PrintPDB true              # Additionally print pdb file for entire system, is 
                            # updated every iteration for optimization
 
# Computing MM nonbonded interactions within non-active region.
 Do_NB_For_Fixed_Fixed true # Compute MM-MM nonbonded interaction also for 
                            # non-active atom pairs. Default true.
# Treats all active water molecules that are treated on MM level as rigid bodies 
#  in optimization and MD simulation, see section "Rigid Water".
 Rigid_MM_Water false       #  Default false.

end
                             
*pdbfile 0 1 ubq.pdb  # structure input via pdb file, but also possible via 
                      # xyz file
```

:::{raw} latex
\begingroup
\footnotesize
:::

:::{tabularcolumns} \Y{0.25}\Y{0.2}\Y{0.45}
:::

(tab:multiscalesimulations.qmmm-keywords)=
:::{flat-table} `%qmmm` 块中的额外关键词，也可从 `%mm` 块访问。
:class: footnotesize
:header-rows: 1
* - 关键词
  - 选项
  - 说明
* - `ORCAFFFilename`
  - `"<filename>"`
  - ORCA 力场 prms 文件的文件名。
* - `Do_NB_For_Fixed_Fixed`
  - `true`/`false`
  - 同时计算非活性区域内的 MM-MM 非键相互作用（即非活性原子对）。默认 `true`。对 `GOAT` 和 `Crystal-QMMM`，默认为 `false`。
* - `RIGID_MM_WATER`
  - `true`/`false`
  - 活性 MM 水分子的优化和 MD。默认 `false`。
* - `ExtendActiveRegion`
  - `distance`
  - 使用距离判据（VDW 距离加 `Dist_AtomsAroundOpt`）扩展活性区域。
* -
  - `cov_bonds`
  - 仅添加与活性原子共价键合的原子。
* -
  - `no`
  - 不向扩展活性区域添加任何原子。
* - `Dist_AtomsAroundOpt`
  - `<real>`
  - 为 `ExtendActiveRegion` 添加到 VDW 半径的距离（单位 Å）。默认：`0.`。
* - `OptRegion_FixedAtoms`
  - `{ints}`
  - 定义扩展活性区域的原子列表。默认：空列表。
* - `PrintOptRegion`
  - `true `/` false`
  - 额外打印优化区域的 `.xyz` 和 `.trj` 文件。默认 `true`。
* - `PrintOptRegionExt`
  - `true `/` false`
  - 额外打印扩展优化区域的 `.xyz` 和 `.trj` 文件。默认 `false`。
* - `PrintPDB`
  - `true `/` false`
  - 额外打印整个体系的 `.pdb` 文件，每次优化迭代更新。默认 `false`。
:::
:::{raw} latex
\endgroup
:::
