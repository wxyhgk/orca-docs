```{index} QMMM, QM/QM2, QM/QM2/MM, additive, subtractive
```
(sec:multiscalesimulations.molecules)=
# 分子体系的多尺度模拟（Multiscale Simulations of molecular systems）

ORCA 提供三种适用于分子体系（如蛋白质、DNA、大分子、显式溶剂化）的方法，具体取决于体系大小以及力场参数的可用性。

-   [加和式 QM/MM](sec:multiscalesimulations.add_qmmm) 是纯加和式 QMMM 方法。

-   [QM1/QM2](sec:multiscalesimulations.oniom2) 是减除式（2 层）ONIOM 方法。

-   [QM1/QM2/MM](sec:multiscalesimulations.oniom3) 是 3 层方法，在 QM1 和 QM2 之间采用减除式方法，在 QM2/MM 之间采用加和式 QMMM 方法。

(sec:multiscalesimulations.add_qmmm)=
## 加和式 QMMM（Additive QMMM）

在加和式 QMMM 方案中，用力场参数描述 MM 区域内的相互作用，以及 QM 和 MM 原子之间的成键相互作用和 LJ 相互作用。因此，计算的 MM 部分需要力场参数。
ORCA 目前支持常用的 **CHARMM**、**AMBER** 和 **Open Force Field** 力场，如 {ref}`sec:modelchemistries.mm-orcaforcefield` 中所讨论，并提供工具将其[转换](sec:modelchemistries.mm-orcaforcefield.prms-convff)为 ORCA 力场文件格式。

(sec:multiscalesimulations.qmmm-orcaforcefield)=
### 基本用法（Basic Usage）

加和式 QM/MM 计算所需的最小输入如下面的示例所示。
力场文件名通过关键词 `ORCAFFFilename` 提供：

```orca
!QMMM
%qmmm
 QMAtoms {0 1 2 27 28} end
 ORCAFFFilename "UBQ.ORCAFF.prms"
end
```

:::{admonition} 注意
:class: note
QM/MM、QM/QM2/MM 和 IONIC-CRYSTAL-QMMM 计算需要提供 `ORCAFF.prms` 文件，而 QM/QM2 和 `MOL-CRYSTAL-QMMM` 则不需要。
:::

(sec:oniom)=
## ONIOM 方法：总体概述（ONIOM Methods: General Overview）

对于含多达 10000 个原子的大体系的模拟，或生物大分子中的大 QM 区域，ORCA 提供 QM/QM2 和 QM/QM2/MM 方法。这两种不同方法的具体内容将在下文讨论。这里我们介绍两种方法的共同概念和关键词。对于减除式方法，我们对体系的不同部分分别使用高水平（QM）和低水平（QM2）精度。与 QM-MM 方法相比，其优点如下：

-   QM2 方法是可极化的，与高水平区域的相互作用更准确。

-   在 QM2 水平描述的原子不需要 MM 参数。

(sec:multiscalesimulations.oniom-qm2methods)=
### 可用的 QM2 方法（Available QM2 Methods）

ORCA 内置了若干 QM2 方法：

-   半经验方法（`AM1`、`PM3`）

-   紧束缚 DFT（`XTB0`、`XTB1`、`XTB`（或 `XTB2`））

-   复合方法（`HF-3c`、`PBEh-3c`、`r2SCAN-3c`）

-   用户自定义 QM2 方法

这些方法对应的关键词为：

(tab:multiscalesimulations.oniom-qm2options)=
:::{table} 通过简单关键词为 QM/QM2 和 QM/QM2/MM 方法提供的 QM2 选项。
:class: normalsize
| QM/QM2      | QM/QM2/MM       |
|:------------|:----------------|
| `!QM/XTB`       | `!QM/XTB/MM`       |
| `!QM/XTB1`      | `!QM/XTB1/MM`      |
| `!QM/XTB0`      | `!QM/XTB0/MM`      |
| `!QM/GFN-FF`    | `!QM/GFN-FF/MM`    |
| `!QM/HF-3C`     | `!QM/HF-3C/MM`     |
| `!QM/PBEH-3C`   | `!QM/PBEH-3C/MM`   |
| `!QM/R2SCAN-3C` | `!QM/R2SCAN-3C/MM` |
| `!QM/PM3`       | `!QM/PM3/MM`       |
| `!QM/AM1`       | `!QM/AM1/MM`       |
:::

用户可以用如下方式定义自己的低水平方法

```orca
!QM/QM2          or   !QM/QM2/MM   
%qmmm
  QM2CUSTOMMETHOD "B3LYP"
  QM2CUSTOMBASIS "def2-SVP def2/J"
end
```

也可以提供自定义的 QM2 方法/基组文件：

```orca
!QM/QM2  or  !QM/QM2/MM   
%qmmm
  QM2CustomFile "myQM2Method.txt" # File should be available 
                                  # in working directory
end
```

自定义 QM2 方法文件可以包含任何所需的输入，例如文件 myQM2Method.txt：

```orca
!cc-pVDZ HF TightSCF NOSOSCF KDIIS
%basis
  NewAuxJKGTO Mg "AutoAux" end
end
```

:::{admonition} 注意
:class: note

QM2Custom 选项只添加方法（包括收敛设置）和基组。其他一切（并行化、内存、溶剂化等）由 ORCA 自行处理。
:::

### 高水平与低水平之间的静电相互作用（Electrostatic Interaction between high and low level）

默认情况下我们使用静电嵌入，即高水平体系“看到”低水平（QM2）体系的原子点电荷。
这些点电荷由整个体系的低水平（QM2）计算导出。可用于确定这些电荷的方法如下：

(tab:multiscalesimulations.oniom-qm2-chargemethod)=
:::{table} 确定 QM2 原子电荷的选项。
:class: normalsize
| 关键词         | 选项       |
|:----------------|:----------------|
| `Charge_Method` | `Hirshfeld`（默认） |
|                 | `MBIS`                |
|                 | `CHELPG`              |
|                 | `Mulliken`            |
|                 | `Loewdin`（若 QM2 为 AM1 或 PM3 则为默认） |
:::

QM2 点电荷可以用下列关键词进行缩放。

```orca
%qmmm
  Scale_QM2Charges_MMAtom 1. # default is 1.
end
```

### 边界区域（Boundary Region）

体系高低水平部分之间可以包含共价键。为了检测并合理处理这些共价键，在计算开始时使用下列关键词生成大 QM2 体系的拓扑。

(tab:multiscalesimulations.oniom-qm2-autoff)=
:::{table} 为完整（QM/QM2）或中等（QM/QM2/MM）体系创建初始拓扑的选项。
:class: normalsize
| 关键词         | 选项       |
|:----------------|:----------------|
| `AutoFF_QM2_Method` | `Simple_Eq`（默认） |
|                     | `XTB`             |
|                     | `XTB1`            |
|                     | `XTB0`            |
|                     | `GFNFF`           |
|                     | `HF3C`            |
|                     | `PBEH3C`          |
|                     | `R2SCAN3C`        |
|                     | `PM3`             |
|                     | `AM1`             |
|                     | `QM2`             |
:::

:::{admonition} 注意
:class: note

如果将任一 XTB 方法用作 AutoFF_QM2_Method，请确保 otool_xtb 可执行文件在您的 ORCA PATH 中，见
{ref}`sec:modelchemistries.semiempirical.xtb`。
:::

(sec:multiscalesimulations.oniom2)=
## 减除式 QM/QM2 方法（ONIOM2）（Subtractive QM/QM2 Method）

QM/QM2 方法是一种非常方便的多尺度计算方式，无需准备任何参数。该方法是减除式 QM-QM 方法，即对感兴趣的部分采用较高精度水平处理，体系的其余部分采用较低精度水平处理。该实现遵循了类似的工作，例如参考文献 {cite}`Mayhall2010` 中所述。

该方法的用法与常规 QM 计算类似。让我们看一下丙酸中的质子转移，可以按如下方式建模：

```{literalinclude} ../../orca_working_input/C06S28_535.inp
:language: orca
```

其中产物结构文件（propionicAcid_prod.xyz）为：

```{literalinclude} ../../orca_working_input/propionicAcid_prod.xyz
:language: orca
```

从输入可以看出，与常规计算的唯一区别是必须通过 `QMAtoms` 或 `QMCoreAtoms` 关键词定义高水平区域。

### 体系电荷与多重度（System charges and multiplicities）

两个子体系可以具有不同的（整数）电荷和多重度。正确设定电荷和多重度很重要。通过坐标部分定义的电荷和多重度对应于高水平区域（`QMAtoms`）的电荷和多重度。用户仍需定义整个体系的电荷和多重度（对应于高水平部分和低水平部分电荷之和，以及总多重度）。

```orca
%qmmm
  QMAtoms {0:3} end # high level region
  Charge_Total  0   # charge of the full system. Default 0.
  Mult_Total    1   # multiplicity of the full system. Default 1.
end
*xyz 0 1            # charge and mult. of the high level region, i.e. atoms 0 to 3
```

### 溶剂化（Solvation）

隐式溶剂化效应可以包含在 QM/QM2 计算中。一方面，对于 QM/XTB 计算，可以采用解析线性化 Poisson-Boltzmann（`ALPB`）溶剂化模型、域分解 COSMO（`ddCOSMO`）或扩展的类导体极化连续介质模型（`CPCM-X`）；另一方面，如果不请求 XTB，ORCA 使用 C-PCM。用户只需在 ORCA 输入文件中添加下列标记，
对 QM2 区域使用 XTB：

```orca
!QM/XTB ALPB(Water)

or

!QM/XTB DDCOSMO(Water)

or

!QM/XTB CPCMX(Water)
```

QM2 区域不使用 XTB：

```orca
!QM/HF-3c CPCM(Water)
```

如果请求 `ddCOSMO`（XTB）或 `C-PCM`（非 XTB），有两种可能的 ONIOM/隐式溶剂化方法 {cite}`oniom_pcm`。

-   **C-PCM/B：** 首先将溶剂效应包含在大 QM2 体系的计算中。该计算完成后，大体系空腔表面的溶剂化电荷被用作小体系后续低水平和高水平计算的点电荷。

-   **C-PCM/C：** 溶剂效应仅包含在大 QM2 体系的计算中。

用户可以在 "`qmmm`" 块中通过标记 "`solv_scheme`" 选择其中一种方案：

```orca
%qmmm
solv_scheme CPCM_B   # CPCM_B (default)
                     # CPCM_C
end
```

如果请求 ALPB 模型或 CPCM-X（在 QM/XTB 方法内），溶剂化效应仅包含在大 QM2 体系的计算中（与 C-PCM/C 方案相同）。

(sec:multiscalesimulations.oniom3)=
## QM/QM2/MM 方法（ONIOM3）（QM/QM2/MM Method）

QM/QM2/MM 方法对 QM-QM2 部分使用减除式方案，对（QM-QM2）-（MM）相互作用使用加和式方案。当生物大分子和显式溶剂化体系需要非常大的 QM 区域时，可以使用该方法。体系被划分为高水平（QM）、低水平（QM2）和 MM 区域（MM）。

(sec:multiscalesimulations.oniom-qm2atoms)=
### QM2 原子（QM2 Atoms）

QM/QM2/MM 计算需要定义 QM2 原子。它们可以直接定义

```orca
%qmmm                        
 QMAtoms {0:4} end           # list of QM atoms (counting starts from 0) or
 QM2Atoms {5:22} end         # list of QM2 atoms
end                          # an atom should not occur in both lists
*pdbfile 0 1 ubq.pdb
```

也可以通过 pdb 文件的 occupancy 列来定义（见
{ref}`sec:multiscalesimulations.qmmm-regions`）。

:::{admonition} 注意
:class: note
QM2 原子可以通过 occupancy 列中的 2 来定义。这种情况下必须将 `Use_QM2_InfoFromPDB` 设为 true。
:::

### 体系电荷与多重度（System charges and multiplicities）

高低水平子体系可以具有不同的（整数）电荷和多重度。正确设定电荷和多重度很重要。通过坐标部分定义的电荷和多重度对应于高水平区域（`QMAtoms`）的电荷和多重度。用户仍需定义中等体系的电荷和多重度（对应于高水平和低水平区域电荷之和，以及高低水平区域合并后的总多重度）。MM 区域的电荷根据力场提供的 MM 参数确定。

```orca
%qmmm
  QMAtoms {0:3} end # high level region
  Charge_Medium 0   # charge of the medium system. Default 0.
  Mult_Medium   1   # multiplicity of the medium system.  Default 0.
end
*xyz 0 1            # charge and mult. of the high level region, i.e. atoms 0 to 3
```

### 基本用法（Basic Usage）

QM/QM2/MM 计算的示例如下所示：

```orca
!QM/HF-3c/MM Opt B3LYP def2-TZVP def2/J NumFreq
%qmmm
 ORCAFFFilename "peptideChain.ORCAFF.prms"
 QMAtoms {16:33 68:82} end
 QM2Atoms {0:12 83:104} end
 ActiveAtoms { 0:38 65:120} end
 Charge_Medium 0
end
*pdbfile -1 1 peptideChain.pdb
```
