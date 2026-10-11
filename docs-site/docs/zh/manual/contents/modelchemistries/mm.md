

<a id="sec:modelchemistries.mm.orca"></a>
# 分子力学（Molecular Mechanics, MM）

自 4.2 版本起，ORCA 拥有自己独立的分子力学（Molecular Mechanics, MM）实现。

进行 MM 处理所需的最小输入如下所示。

```orca
!MM
%mm
 ORCAFFFilename "UBQ.ORCAFF.prms"
end
```

在本节中，我们将讨论 MM 的用法以及基本关键词和选项，即：

-   MM 计算可以与哪些其他功能结合使用

-   ORCA 力场文件（ORCA Force Field File）的基本结构

-   支持哪些力场（force fields）

-   如何生成 ORCA 力场文件

-   如何操作 ORCA 力场文件

-   如何加速 MM 计算

-   其他 MM 选项和关键词。

对 QM/MM 计算重要的其他选项将在章节 [qmmm.orca](../multiscalesimulations/qmmm-general.md#sec:multiscalesimulations.qmmm.orca) 中讨论。

## 将 MM 模块与其他 ORCA 功能结合使用

分子力学是作为 ORCA 中多尺度模拟（multiscale simulations）的前置条件而引入的。但 MM 计算也可以独立使用，例如用于廉价的预优化（preoptimizations）。

可能的 ORCA 功能包括：

-   **单点能计算（Single Point Calculations）**：简单的 MM 计算以及 [QM/MM 计算](../multiscalesimulations/qmmm-general.md#sec:multiscalesimulations.qmmm.orca)

-   **优化（Optimization）**：使用各类[几何优化](../structurereactivity/optimizations.md#sec:structurereactivity.optimization)，支持各种约束（constraints）、过渡态（TS）优化、弛豫势能面扫描（relaxed surface scans）以及 ScanTS 功能。可使用 L-Opt 和 L-OptH 功能，包括各种片段优化的组合（固定片段、弛豫片段、仅弛豫片段中的特定元素、将片段视为刚体）。

-   **过渡态与最小能量路径（Transition States and Minimum Energy Paths）**：使用 MM 方法无法进行键的断裂与形成，但构象变化（conformational changes）或色散驱动的反应（dispersion driven reactions）可以在 MM 层面上研究。对于此类任务，可使用 ORCA 的[微动弹性带（Nudged-Elastic Band）方法](../structurereactivity/neb.md#sec:structurereactivity.optimization.neb)。

-   **构象搜索（Conformational Searches）**：构象搜索可使用 ORCA 的 [GOAT](../structurereactivity/goat.md#sec:structurereactivity.GOAT) 模块运行。

-   **频率计算（Frequency Calculations）**：使用常规[频率计算](../structurereactivity/frequencies.md#sec:structurereactivity.frequencies)。如有需要，ORCA 会自动开启 [geomopt.partialhess](../structurereactivity/optimizations_TS.md#sec:structurereactivity.geomopt.partialhess)（PHVA）[li2002theor](../../bibliography.md) 计算。（未对 `IONIC-CRYSTAL-QMMM` 进行测试）

-   **分子动力学（Molecular Dynamics）**：使用[分子动力学](../moleculardynamics/moldyn.md#sec:moldyn)（MD）模块进行基于 MM 的玻恩-奥本海默分子动力学（Born-Oppenheimer MD, BOMD）。

!!! note "重要"

    [活性区域（Active regions）](../multiscalesimulations/qmmm-general.md#sec:multiscalesimulations.qmmm-active)也可为 MM 计算而定义。它们必须通过 `%qmmm` 块[定义](../multiscalesimulations/qmmm-general.md#sec:multiscalesimulations.qmmm-regions)。

<a id="sec:modelchemistries.mm-orcaforcefield"></a>
## ORCA 中的分子力学力场

QM/MM 计算的 MM 部分需要力场参数（force-field parameters）。ORCA 有自己的参数文件格式（ORCA 力场文件 —— ORCAFF.prms），其中包含非键相互作用（nonbonded interactions）的原子专属参数：

-   分电荷（partial charge）

-   LJ 系数（LJ coefficients）

以及成键相互作用（bonded interactions）的参数：

-   键（bonds）

-   键角（angles）

-   Urey-Bradley 项

-   二面角（dihedrals）

-   非正常二面角（impropers）

-   CMAP 项（主链交叉项，目前未使用）

各个参数（例如原子电荷、平衡键长和力常数等）都可以直接在 ORCA 力场文件中方便地修改。

### 支持的力场类型（Supported Force Field Types）

QM/MM 计算的 MM 部分需要力场参数。ORCA 有自己的力场文件格式（存储在名为 `basename.ORCAFF.prms` 的文件中），在内部使用。
ORCA 提供了将其他常用力场转换为 ORCA 力场文件格式的工具。
目前，支持将以下格式转换为 ORCA 力场文件格式：

-   **CHARMM psf 文件**：来自 CHARMM 力场的蛋白质结构文件（protein structure file）。psf 文件可以很容易地用流行的分子可视化工具 [VMD](https://www.ks.uiuc.edu/Research/vmd/) 及其扩展（[psfgen](https://www.ks.uiuc.edu/Research/vmd/plugins/psfgen/)、[QwikMD](http://www.ks.uiuc.edu/Research/qwikmd/)、[fftk](http://www.ks.uiuc.edu/Research/vmd/plugins/fftk/)（可与 ORCA 协同工作））来准备。psf 文件包含所有原子的原子类型和成键相互作用信息，但不包含这些相互作用所对应的参数。这些参数存储在特定文件中，通常以 prm 结尾，也有 par 或 str 的。CHARMM 参数文件随 VMD 安装一起提供，也可以直接[下载](http://mackerell.umaryland.edu/charmm_ff.shtml)。

-   **AMBER prmtop 文件**：来自 AMBER 力场的拓扑文件（topology files）。关于如何生成 AMBER prmtop 文件（针对标准和非标准分子）的教程可以在[这里](https://ambermd.org/tutorials/)找到。

-   **Open Force Field**：来自 [openforcefield 计划](http://openforcefield.org/)的 xml 文件。使用 openff-toolkit，可以轻松地为中小型非标准分子生成 xml 拓扑文件（与 AMBER 力场兼容）。教程参见[这里](https://github.com/openforcefield/openff-toolkit/blob/master/examples/using_smirnoff_with_amber_protein_forcefield/BRD4_inhibitor_benchmark.ipynb)。

-   **简单力场（Simple force field）**，适用于中小分子：另外，orca_mm 模块可以生成简单的近似 ORCAFF.prms 文件。更多选项参见 [modelchemistries.mm-orcaforcefield-makeff](#sec:modelchemistries.mm-orcaforcefield-makeff)。

这一概念具有以下优点：

-   力场参数的修改：原子和键的专属参数可以在 ORCA 力场文件中轻松修改，为用户修改力场提供了最大的灵活性，这对于过渡金属配合物等化学体系可能尤为有用。

-   标准与非标准配体（Standard and Non-Standard Ligands）：配体可以轻松、灵活地替换或添加到体系中，参见 [mm-orcaforcefield.prms](#sec:modelchemistries.mm-orcaforcefield.prms)。

<a id="sec:modelchemistries.mm-orcaforcefield.prms"></a>
### 如何生成和操作 ORCA 力场文件

一旦有了 ORCAFF.prms 文件，就可以对它进行操作，例如拆分为多个部分以对应各个分子、为非标准分子生成新的 ORCAFF.prms 文件，以及合并各个 ORCAFF.prms 文件，具体如下所述：

<a id="sec:modelchemistries.mm-orcaforcefield.prms-convff"></a>
#### 从其他格式转换为 ORCAFF.prms：convff

orca_mm 模块可以通过 -convff 标志将 psf 和 prm 文件（CHARMM）、prmtop 文件（AMBER）或 xml 文件（来自 openff toolkit 的 open force field，与 AMBER 兼容）转换为 ORCAFF 文件。输入选项为：

```orca
orca_mm -convff <optional:-verbose> <FFInput> <PSFFILE> <PRMFILE(S)>

Keywords:
          <FFInput> = -CHARMM
          <FFInput> = -AMBER
          <FFInput> = -OPENMM
```

对于 CHARMM 拓扑，当一个由例如 QwikMD、psfgen 或其他 vmd 工具准备的、含标准残基的体系已有 psf 文件时，转换需要 psf 加 prm 文件作为输入：

```orca
CHARMM example:
orca_mm -convff -CHARMM 1C1E.psf par_all36_prot.prm toppar_water_ions_namd.str
```

ORCA 也可以将 Amber 拓扑转换为 ORCAFF 文件。这里只需要 prmtop 文件：

```orca
AMBER example:
orca_mm -convff -AMBER complex.prmtop
```

ORCA 也可以将来自 openff toolkit 的 xml 文件（与 AMBER 兼容）转换为 ORCAFF 文件。这里只需要 xml 文件：

```orca
OPENFF example:
orca_mm -convff -OPENMM complex.xml
```

#### 拆分力场文件：splitff

如果需要将一个 ORCAFF.prms 文件细分为多个文件，例如当 psf 文件来自 QWikMD 且包含非标准分子（如某个配体）时。在这种情况下，首先将配体的参数从其余体系中拆分出来，接着对配体进行质子化（protonated），然后通过 orca_mm 的 makeff 选项生成一个简单的 ORCAFF.prms 文件，最后通过上述 mergeff 选项将配体的新 ORCAFF.prms 文件添加到主体系文件中。注意，文件只能拆分为对应非键片段（nonbonded fragments）的文件。

输入选项：

```orca
orca_mm -splitff <optional:-verbose> <ORCAFFFILE> <A1> <optional:A2> ... 

Keywords:

          <ORCAFFFILE>  = ORCA forcefield file.
          <A1>          = Atom number of first atom of fragment that should belong 
                           to a new ORCA forcefield file
          <A2>          = Atom number of first atom of fragment that should belong 
                           to a new ORCA forcefield file
          ...           = More split atoms possible
          Note that atoms start counting at 1.
          
Example:
orca_mm -splitff 1C1E_substrate_noH.ORCAFF.prms 7208
```

#### 合并力场文件：mergeff

如果有多个 ORCAFF.prms 文件并需要为一次 ORCA 计算合并它们，例如一个标准分子加一个非标准分子的情况。

输入选项：

```orca
orca_mm -mergeff <optional:-verbose> <ORCAFFFILE1> <ORCAFFFILE2> ... 

Keywords:

          <ORCAFFFILE1>   = First ORCA forcefield file
          <ORCAFFFILE2>   = Second ORCA forcefield file
          ...             = More ORCA forcefield files possible
          
Example:
orca_mm -mergeff 1C1E.ORCAFF.prms substrate_withH.ORCAFF.prms
```

#### 重复力场文件：repeatff

如果同一个 ORCAFF.prms 文件需要重复多次，可以使用 repeatff 功能。

输入选项：

```orca
orca_mm -repeatff <optional:-verbose> <ORCAFFFILE> <A>
          <ORCAFFFILE>      = ORCA forcefield file.
          <A>               = Factor (integer) defining how often this forcefield file should be repeated.
          
Example:
orca_mm -mergeff methanol.ORCAFF.prms 580
```

这一功能在例如给分子溶剂化（solvating a molecule）时很有用，即向溶质（solute）添加多个溶剂（solvent）副本。可以先将溶剂重复 N 次，随后将溶质的 prms 文件与溶剂 prms 文件合并。

#### 拆分 PDB 文件：splitpdb

拆分 ORCAFF.prms 文件时，也需要拆分 pdb 文件。该文件可以拆分为任意数量的单独文件。

这可以与 splitff 命令配合使用。

输入选项：

```orca
orca_mm -splitpdb <optional:-verbose> <PDBFILE> <A1> <optional:A2> ... 

Keywords:

          <PDBFILE> = PDB file.
          <A1>      = Atom number of first atom of fragment that should belong 
                       to a new ORCA forcefield file
          <A2>      = Atom number of first atom of fragment that should belong 
                       to a new ORCA forcefield file
          ...       = More split atoms possible
          Note that atoms start counting at 1.
          
Example:
orca_mm -splitpdb 1C1E_substrate_noH.pdb 7208
```

#### 合并 PDB 文件：mergepdb

如果有多个 PDB 文件需要为一次 ORCA 计算合并，例如一个蛋白质和一个配体或多个配体，或者一个先从配合物中移除、经修改后又要放回配合物 PDB 文件中的配体。

这可以与 mergeff 命令配合使用。

输入选项：

```orca
orca_mm -mergepdb <optional:-verbose> <1PDBFILE> <2PDBFILE> ... 

Keywords:

          <1PDBFILE>   = First PDB file
          <2PDBFILE>   = Second PDB file
          ...          = More PDB files possible
          
Example:
orca_mm -mergepdb 1C1E.pdb substrate_withH.pdb
```

<a id="sec:modelchemistries.mm-orcaforcefield-makeff"></a>
#### 创建简单力场：makeff

orca_mm 工具可以为一个分子生成近似力场，并以 ORCAFF.prms 格式存储。其中，LJ 系数基于 UFF 参数，分电荷基于简单的 PBE 或 XTB 计算。所得拓扑当然不如原始 CHARMM 拓扑精确，但仍可用于对分子进行近似处理。由此，该分子可以是 QM 区域的一部分（至少具有必要的 LJ 系数），也可以作为非活性旁观者（non-active spectator）属于 MM 区域——但不能离感兴趣的区域太近。在后一种情况下，重要的是该分子必须是非活性的，因为成键参数不可用。不过，它仍可以作为刚体（rigid body）进行优化，参见章节 [optimization.lbfgs](../structurereactivity/optimizations.md#sec:structurereactivity.optimization.lbfgs)，以及章节 [multiscalesimulations.qmmm-lopt](../multiscalesimulations/qmmm-general.md#sec:multiscalesimulations.qmmm-lopt) 中在 QM/MM 计算中的用法——在 MM 层面上优化其相对于特定环境的位置和取向。

输入选项：

```orca
orca_mm -makeff <optional:-verbose> <XYZ/PDBFILE> <optional:-C CHARGE> 
                <optional:-M MULT> <optional:-nproc N> <optional:-CHARGE_OPTIONS>

Keywords:

          <CHARGE>              = charge of system
          <MULT>                = multiplicity of system
          <-nproc N>            = number of processors (Default 1) 
          <-CHARGE_OPTIONS>     =   Structure            Charge calculation
               <-PBE>                input                     PBE
               <-PBEOpt>             PBE opt.                  PBE
               <-PBEOptH>            PBE H-opt.                PBE
               <-XTB>                input                     XTB
               <-XTBOpt>             XTB opt.                  XTB
               <-XTBOptH>            XTB H-opt.                XTB
               <-XTBOptPBE>          XTB opt.                  PBE
               <-noChargeCalc>       distribute net charge evenly

               PBE Opt and SP level: RI-PBE/def2-SVP CPCM(Water), CHELPG charges
               XTB Opt and SP level: GFN2-XTB GBSA(Water), Mulliken partial charges
          
Example:
orca_mm -makeff substrate_withH.xyz -M 2 -XTBOptPBE
```

注意，ORCA 基于简单的距离规则来生成键，这使 ORCA 能够检测应在 QM 和 MM 原子之间的何处添加连接原子（link atoms），另见章节 [multiscalesimulations.qmmm-boundary](../multiscalesimulations/qmmm-general.md#sec:multiscalesimulations.qmmm-boundary)。但建议用户对于用 makeff 选项生成 ORCAFF.prms 文件的分子，要么完全放在 QM 区域，要么完全放在 MM 区域，除非电荷分布已经得到妥善处理（因为 QM 和 MM 体系中需要整数电荷）。

<a id="sec:modelchemistries.mm-orcaforcefield-getHDist"></a>
#### 获取标准氢键键长：getHDist

对于连接原子的定义，C、N、O 与氢之间的标准键长由 ORCA 直接设定，但用户可以修改，参见章节 [multiscalesimulations.qmmm-boundary](../multiscalesimulations/qmmm-general.md#sec:multiscalesimulations.qmmm-boundary)。如果 QM-MM 边界的 QM 一侧有其他原子类型，则必须定义它们到连接原子的距离。在这种情况下，可以向 ORCA 提供一个文件，定义所有可能原子与氢之间的标准键长。该文件可以通过以下命令生成：

输入选项：

```orca
orca_mm -getHDist <optional:-verbose> <XYZ/PDBFILE>
          
Example:
orca_mm -getHDist 1C1E.xyz
```

随后可以修改该文件、添加所需数值，并将所得文件定义为 QMMM 计算的输入。

<a id="sec:modelchemistries.mm-orcaforcefield-ioniccrystal"></a>
#### 为 IONIC-CRYSTAL-QMMM 创建 ORCAFF.prms 文件

对于 IONIC-CRYSTAL-QMMM 计算（章节 [multiscalesimulations.ionic-cryst-qmmm](../multiscalesimulations/qmmm-crystal.md#sec:multiscalesimulations.ionic-cryst-qmmm)），需要一个包含初始电荷和连接关系（connectivities）的 ORCAFF.prms 文件。如果您没有使用 `orca_crystalprep` 工具来设置此类计算（参见章节 [utilities.crystalprep](../utilitiesvisualization/utilities.md#sec:utilities.crystalprep)），可以用以下命令直接准备 ORCAFF.prms 文件：

```orca
orca_mm -makeff <XYZ/PDBFILE> -CEL <ELEMENT1> <OXIDATION_STATE1> 
                              -CEL <ELEMENT2> <OXIDATION_STATE2>

Keywords:

          <ELEMENT1>             = element name
          <OXIDATION_STATE1>     = formal oxidation state of element 1
          ...                    = More elements possible
          
Example:
orca_mm -makeff na4cl4.xyz -CEL Na 1.0 -CEL Cl -1.0
```

这里，na4cl4.xyz 是超胞（supercell）结构文件（它可以包含数万个原子）。

!!! note "注意"

    对于氧化态更复杂的超胞（例如 Co$_3$O$_4$），可以通过 [utilities.crystalprep](../utilitiesvisualization/utilities.md#sec:utilities.crystalprep) 工具方便地生成 ORCAFF.prms 文件。

## 加速非键相互作用计算

对于含数十万原子的超大体系的 MM 计算，以及使用快速 QM 方法（例如 XTB、AM1）和/或极小 QM 体系的 QMMM 计算，非键相互作用的计算可能成为瓶颈（bottleneck）。ORCA 的 MM 实现中提供了多种加速非键相互作用计算的方案。其中两种方案对长程相互作用进行截断，另一种方案可用于带活性区域的计算，即只有体系的一部分是活性的或被优化的计算。关于活性区域的更多信息参见章节 [multiscalesimulations.qmmm-active](../multiscalesimulations/qmmm-general.md#sec:multiscalesimulations.qmmm-active)。

### LJ 相互作用的力开关（Force Switching）

通过对 LJ 相互作用采用力开关方案（见参考文献 [steinbach1996](../../bibliography.md)），使用一个平滑的开关函数（switching function）在外部截断距离 `LJCutOffOuter` 处平滑地截断 LJ 势能。如果 switching 设为 false，则 LJ 相互作用不会在 `LJCutOffOuter` 处被截断。参数 `LJCutOffInner` 指定开关函数开始生效的距离，以使范德华势（van der Waals potential）在 `LJCutOffOuter` 距离处平滑地降至 0，确保力在 `LJCutOffOuter` 处降至零而不引入不连续性。注意 `LJCutOffInner` 必须始终小于 `LJCutOffOuter`。

```orca
%mm
 SwitchForceLJ true       # Use the switch force scheme for the LJ interaction.
                          # Default: true. 
 LJCutOffInner 10.        # Distance (in Ang). Default: 10 Ang.
 LJCutOffOuter 12.        # Distance (in Ang). Default: 12 Ang.
end
```

### 静电相互作用的力平移（Force Shifting）

通过对静电相互作用采用力平移方案（见参考文献 [steinbach1996](../../bibliography.md)），静电势在截断距离 `CoulombCutOff` 处平移至零。如果 shifting 设为 false，则静电相互作用不会在 `CoulombCutOff` 处被截断。

```orca
%mm
 ShiftForceCoulomb true   # Use the shift force scheme for the Coulomb interaction.
                          # Default: true. 
 CoulombCutOff 12.        # Distance (in Ang). Default: 12 Ang.
end
```

### 忽略非活性区域内的非键相互作用

在优化和 MD 运行中使用活性区域时（参见章节 [multiscalesimulations.qmmm-active](../multiscalesimulations/qmmm-general.md#sec:multiscalesimulations.qmmm-active)），对于两个都是非活性的原子对，可以在 MM 层面上忽略其非键相互作用，而不会损失结果的准确性。只要非活性原子的坐标相同，甚至两个结构之间的相对能量也是正确的。对于所有其他情况，即如果非活性区域中原子的位置不同，则应在最终的单点能计算中计算完整的非键相互作用。默认情况下该选项是关闭的。

```orca
%mm
 Do_NB_For_Fixed_Fixed true # Compute MM-MM nonbonded interaction also for 
                            # non-active atom pairs. Default true.
end
```

<a id="sec:modelchemistries.mm-rigid-TIP3P"></a>
## 刚性水分子（Rigid Waters）

由于 TIP3P 水的参数化，可能必须将其作为刚体处理——请查看所用力场参数化的具体说明——我们提供了一个关键词，用于对所有活性 MM 水分子进行自动的刚性处理。以下关键词在优化和 MD 运行中对活性 MM 水分子施加键和键角约束：

```orca
%mm
 Rigid_MM_Water false       # Default: false. 
end
```

<a id="sec:modelchemistries.mm-keywords"></a>
## MM 模块的可用关键词

这里我们列出所有可从 mm 块中访问的、与 MM 计算相关的关键词。

<a id="tab:modelchemistries.mm-keywords-table"></a>
!!! note "`%mm` 块输入关键词"


| ****关键词（Keyword）**** | 选项（Options） | 描述（Description） |
| --- | --- | --- |
| **`ShiftForceCoulomb`** | `true`/`false` | 长程静电作用：使用 Shift Force 方案。默认为 true。Coulomb 相互作用的 Shift Force 方案将 Coulomb 势平移，使其在截断距离处变为零。 |
| **`CoulombCutOff`** | `<real>` | 距离（单位为 Ang）。默认：12 Ang。 |
| **`SwitchForceLJ`** | `true`/`false` | 使用 Switch Force 方案。默认为 true。对于 LJ 相互作用，在 `LJCutOffInner` 之前 Switch Force 方案保持 LJ 相互作用不变。在 `LJCutOffInner` 和 `LJCutOffOuter` 之间，对 LJ 势施加一个平滑的开关函数，使力在 `LJCutOffOuter` 处降至零而不引入不连续性。 |
| **`LJCutOffInner`** | `<real>` | 距离（单位为 Ang）。默认：10 Ang。 |
| **`LJCutOffOuter`** | `<real>` | 距离（单位为 Ang）。默认：12 Ang。 |
| **`DielecConst`** | `<real>` | 计算静电相互作用时使用的介电常数（dielectric constant）。默认：1。 |
| **`Coulomb14Scaling`** | `<real>` | 1,4-成键原子之间静电相互作用的缩放因子。默认：1。 |
| **`PrintLevel`** | `<int>` | 打印选项：可为 0 到 4，0=不打印，1=正常，…… |

部分 MM 关键词也可以通过 qmmm 块访问，参见章节 [multiscalesimulations.qmmm-keywords](../multiscalesimulations/qmmm-general.md#sec:multiscalesimulations.qmmm-keywords)。

<a id="tab:modelchemistries.mm-keywords-and-qmmm-keywords-table"></a>
!!! note "也可从 `%qmmm` 块访问的 `%mm` 块输入关键词"


| ****关键词（Keyword）**** | 选项（Options） | 描述（Description） |
| --- | --- | --- |
| **`ORCAFFFilename`** | `"<filename>"` | ORCA 力场 prms 文件的文件名。 |
| **`Do_NB_For_Fixed_Fixed`** | `true`/`false` | 同时计算非活性区域内的 MM-MM 非键相互作用，即对非活性原子对进行计算。默认为 `true`。对于 `GOAT` 和 `Crystal-QMMM`，默认为 `false`。 |
| **`RIGID_MM_WATER`** | `true`/`false` | 活性 MM 水分子的优化和 MD。默认为 `false`。 |
| **`ExtendActiveRegion`** | `distance` | 将活性区域扩展至 activeRegionExt 的方案。另见[这里](../multiscalesimulations/qmmm-general.md#sec:multiscalesimulations.qmmm-active)。`distance`：使用距离判据（VDW 距离加上 `Dist_AtomsAroundOpt`）。 |
| **—** | `cov_bonds` | 仅添加与活性原子共价键合的原子。 |
| **—** | `no` | 不向 activeRegionExt 添加任何原子。 |
| **`Dist_AtomsAroundOpt`** | `<real>` | `ExtendActiveRegion` 中加到 VDW 距离上的距离。单位为埃（Angstrom）。默认 `0.`。 |
| **`OptRegion_FixedAtoms`** | `{ints}` | 用于定义扩展活性区域的原子列表。默认：空列表。 |
| **`PrintOptRegion`** | `true`/`false` | 额外打印优化区域的 xyz 和 trj 文件。默认 `true`。 |
| **`PrintOptRegionExt`** | `true`/`false` | 额外打印扩展优化区域的 xyz 和 trj 文件。默认 `false`。 |
| **`PrintPDB`** | `true`/`false` | 额外打印整个体系的 pdb 文件，在优化中每次迭代都会更新。默认 `false`。 |

