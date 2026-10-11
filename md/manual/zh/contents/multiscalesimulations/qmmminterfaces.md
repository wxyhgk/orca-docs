```{index} QMMM, Interfaces
```
(sec:multiscalesimulations.qmmminterfaces.interfaces)=
# 通过接口实现 QM/MM（QM/MM via Interfaces to ORCA）

ORCA 很容易作为 QM 引擎接入几乎任何 QM/MM 环境，因为它可以从外部文件接受一组点电荷（参见章节 {ref}`sec:essentialelements.coordinates.pointcharges`），并以透明的格式向驱动程序返回计算能量和梯度所需的所有信息。在我们的研究组中，我们有使用四种不同 QM/MM 环境的经验：ChemShell、Gromacs、pDynamo 和 NAMD。每个接口都在下一节中描述。本手册不可能面面俱到，这里只给出最小可运行示例。这些示例主要涵盖 QM/MM 计算中 QM 部分的技术方面。关于体系的初始准备，请用户参阅驱动程序的文档。

## ORCA 与 Gromacs（ORCA and Gromacs）

通过与 Gromacs 软件包开发者的合作，我们开发了到 ORCA 的接口。该接口从 Gromacs 4.0.4 版本起可用，直至 4.5.5 版本。

如上所述，初始设置必须用 Gromacs 完成。
在 QM/MM 计算中，Gromacs 将调用 ORCA 以获得 QM 原子的能量和梯度。该接口可用于执行 Gromacs 软件包允许的所有作业类型，例如优化、分子动力学、自由能。此外，对于几何优化，我们实现了一个微迭代方案，可以通过在 Gromacs 的 `.mdp` 文件中设置关键词 `bOpt = yes` 来请求。这将使 ORCA 每次被 Gromacs 调用时都执行一次 QM 几何优化。在此优化过程中，ORCA 还将计算 QM 和 MM 原子之间的 Lennard-Jones 相互作用，并冻结边界原子。这一微迭代方案也可用于执行过渡态优化。如果您正在寻找过渡态并对结构有良好的初始猜测，则可以通过微迭代方案同时进行 MM 体系的优化和用 ORCA 对 QM 体系进行过渡态优化。由于为每个微迭代步骤计算 Hessian 代价高昂，用户可以通过 ORCA 输入中的 `read_temp_Hess` 告诉 ORCA 使用上一步的（更新后的）Hessian 矩阵。

为了给用户充分的灵活性，QM 运行所需的信息放在一个单独的纯文本文件中，名为 `GromacsBasename.ORCAINFO`。当 Gromacs 为 ORCA 计算写入输入时，它会将该文件与坐标、点电荷、Lennard-Jones 系数和计算类型（`EnGrad`、`Opt`、`TSOpt`）的信息合并。

下面是由 Gromacs 创建的输入文件的典型示例，其中对每个 Gromacs 优化步骤，ORCA 将执行 QM 部分的完全优化，而不仅仅是能量和梯度计算。

```{literalinclude} ../../orca_working_input/C05S14_238.inp
:language: orca
```

:::{admonition} 注意
:class: note

-   如果您使用 `bOpt` 或 `bTS`，必须处理边界上的额外项。您可以将 Q2-Q1-M1-M2 构型的二面角项置零，或者固定相应的 Q2 原子。

-   如果您想使用 ORCA 的约束，也必须将它们放在计算的 Gromacs 部分中。

-   如果 QM 和 MM 体系之间没有键，QM 体系的 `bOpt` 优化可能会有收敛问题。当步长过大导致 QM 原子离 MM 原子过近时就会出现这种情况。可以通过向内坐标集合中添加选定 QM 原子的笛卡尔坐标的额外坐标和 Hessian 对角值来规避这些收敛问题。这应当只对边界区域的少数几个原子进行。

```orca
%geom
    # add the Cartesian position of atoms 2 and 4 to the
    # set of internal coordinates with a diagonal Hessian value of 0.1
    Hess_Internal
    {C 2 D 0.1}
    {C 4 D 0.1}
    end
end
```
:::
 
## ORCA 与 pDynamo（ORCA and pDynamo）

与 pDynamo 库的接口在[此处](https://sites.google.com/site/pdynamomodeling/)有简要文档。它使用相同的纯文本文件在 pDynamo 库和 ORCA 之间交换信息。为了具备与上文所述类似的功能，我们扩展了该接口，通过接受逐字文本块来生成更复杂的 ORCA 输入文件。我们还在 pDynamo 中实现了写出包含 Lennard-Jones 参数的文件的能力。

下面展示了一个简单示例，计算一个小的定制肽的 QM/MM 能量，其中一个氨基酸的侧链按 QM 处理。在本例中，将在 ORCA 调用期间执行完全几何优化。

```python
import os
import pCore
import pBabel
import pMolecule
import pMoleculeScripts

# Read the initial coordinates from the .pdb file.
system = pMoleculeScripts.PDBFile_ToSystem(
        "1UAO.pdb", modelNumber=1, useComponentLibrary=True)

# Instantiate the required models.
mmmodel = pMolecule.MMModelOPLS("protein")
nbmodel = pMolecule.NBModelORCA()
qcmodel = pMolecule.QCModelORCA(
        command=os.getenv("ORCA_COMMAND"),
        deleteJobFiles=False, header="bp86 def2-svp qmmmopt/pdynamo",
        job="chignolin", run=True)

# Assign the models to the system.
system.DefineMMModel(mmmodel)
system.DefineQCModel(
        qcmodel, qcSelection=pCore.Selection([35, 36, 37, 34, 40, 41]))
system.DefineNBModel(nbmodel)
system.electronicState = pMolecule.ElectronicState(
        charge=-1, multiplicity=1)

# Print a summary and calculate the energy.
system.Summary()
system.Energy()
```

执行上述 Python 程序后，将创建一系列文件 `chignolin.inp`、`chignolin.pc`、`chignolin.lj`，并调用 ORCA。所生成的 ORCA 输入文件列在下面。

```{literalinclude} ../../orca_working_input/C05S15_241.inp
:language: orca
```

这里需要指出几点。由于在 `header` 变量中指定了关键词 `qmmm/pdynamo`，pDynamo 库将自动在 ORCA 输入中添加 `constraint` 块，以冻结链接原子（link atoms）以及与它们成键的 QM 原子。它还将生成包含所有 Lennard-Jones 参数的 `chignolin.lj` 文件。该文件与 Gromacs 所生成的有所不同，其重要部分列在下面。

```orca
# number of atoms  combination rule
138 0
#      x            y             z          sigma       epsilon   id
   -6.778000    -1.424000     4.200000     3.250000     0.711280   -1
   -6.878000    -0.708000     2.896000     3.500000     0.276144   -1
   -5.557000    -0.840000     2.138000     3.750000     0.439320   -1
...
    0.433000     0.826000     0.502000     2.960000     0.878640   -1
   -0.523000     0.687000     3.249000     3.500000     0.276144    1
    0.418000     1.724000     3.866000     3.750000     0.439320    2
   -0.069000     2.762000     4.283000     2.960000     0.878640    3
    1.609000     1.463000     3.911000     2.960000     0.878640    4
   -2.259000    -0.588000     1.846000     0.000000     0.000000   -1
   -1.795000     2.207000     2.427000     2.500000     0.125520   -1
   -1.224000     0.346000     3.997000     2.500000     0.125520    5
    0.055000    -0.151000     2.889000     2.500000     0.125520    6
   -0.311000     2.922000     0.557000     3.250000     0.711280   -1
...
   -1.387000    -2.946000     5.106000     2.500000     0.125520   -1
# number of special pairs
22
#        atom1        atom2    factor
          34           32     0.000000
          35           39     0.500000
          40           31     0.000000
          41           30     0.500000
          41           32     0.500000
          36           31     0.500000
          40           32     0.500000
          40           39     0.500000
          34           31     0.000000
          35           30     0.500000
          34           11     0.500000
          34           38     0.500000
          41           31     0.000000
          37           31     0.500000
          34           33     0.500000
          34           39     0.000000
          40           30     0.500000
          41           39     0.500000
          34           30     0.000000
          35           31     0.000000
          34           42     0.500000
          35           32     0.500000
```

第一行上的第二个数字指的是用于计算 Lennard-Jones 相互作用的组合规则类型。若使用几何平均（OPLS 力场）则为 0，若使用 Lorentz-Berthelot 规则（AMBER 力场）则为 1。最后一列的 `id` 对 MM 原子为 -1，对 QM 原子等于其原子序号。在本例中氢链接原子是原子 0。文件的最后一块由原子对和一个特殊因子组成，它们的 Lennard-Jones 相互作用按该因子缩放。一般该因子等于 1，但对相隔一个或两个键的原子为零，而对相隔三个键的原子则取决于力场类型，在本例中为 0.5。

ORCA 优化运行成功完成后，信息将传回 pDynamo 库，由它报告体系的总 QM/MM 能量。此时 QM/MM 计算的类型仅受 pDynamo 库能力的限制，而该库的功能相当广泛。

## ORCA 与 NAMD（ORCA and NAMD）

自 2.12 版本起，NAMD 能够执行混合 QM/MM 计算。有关所有可用关键词、计算设置以及教程和即将推出的 VMD 图形界面的更详细说明，可在 NAMD [网站](http://www.ks.uiuc.edu/~rcbernardi/QMMM/)上找到。

与 NAMD 的其他计算类似，QM/MM 使用 pdb 文件来控制活性区域。下面给出一个示例，其中选择在 N$\epsilon$ 上质子化的组氨酸侧链作为 QM 区域。文件的 occupancy 列或 b-factor 列用于指示哪些原子包含在 QM 区域中、哪些由力场处理。在另一列中，连接 QM 区域和 MM 部分的原子以类似方式标出。为明确哪一列用于何种目的，必须在 NAMD 输入中定义关键词 `qmColumn` 和 `qmBondColumn`。

    ...
    ATOM   1737  CA  HSE P 117      14.762  47.946  31.597  1.00  0.00      PROT C
    ATOM   1738  HA  HSE P 117      14.751  47.579  32.616  0.00  0.00      PROT H
    ATOM   1739  CB  HSE P 117      14.129  49.300  31.501  1.00  1.00      PROT C
    ATOM   1740  HB1 HSE P 117      14.407  49.738  30.518  0.00  1.00      PROT H
    ATOM   1741  HB2 HSE P 117      13.024  49.194  31.509  0.00  1.00      PROT H
    ATOM   1742  ND1 HSE P 117      13.899  51.381  32.779  0.00  1.00      PROT N
    ATOM   1743  CG  HSE P 117      14.572  50.261  32.582  0.00  1.00      PROT C
    ATOM   1744  CE1 HSE P 117      14.615  52.043  33.669  0.00  1.00      PROT C
    ATOM   1745  HE1 HSE P 117      14.356  53.029  34.064  0.00  1.00      PROT H
    ATOM   1746  NE2 HSE P 117      15.678  51.318  33.982  0.00  1.00      PROT N
    ATOM   1747  HE2 HSE P 117      16.369  51.641  34.627  0.00  1.00      PROT H
    ATOM   1748  CD2 HSE P 117      15.706  50.183  33.335  0.00  1.00      PROT C
    ATOM   1749  HD2 HSE P 117      16.451  49.401  33.388  0.00  1.00      PROT H
    ATOM   1750  C   HSE P 117      13.916  47.000  30.775  0.00  0.00      PROT C
    ATOM   1751  O   HSE P 117      12.965  46.452  31.334  0.00  0.00      PROT O
    ...

注意：

-   若要包含多个 QM 区域，可以使用大于 1 的整数来定义不同区域。

-   选择 QM 和 MM 区域时不能拆分电荷基团（charge groups）。原因是如果电荷基团被拆分，可能出现非整数的部分电荷。由于 QM 部分电荷在每次 QM 迭代中都会更新，这可能导致体系总电荷在 MD 模拟过程中发生变化。

-   occupancy 和 b-factor 列在 NAMD 中用于多种声明。如果其中两种在一次模拟中同时出现，则使用关键词 `qmParamPDB` 来定义哪个 pdb 文件包含 QM 原子和键的信息。

-   为简化 QM 原子的选择和 pdb 文件的编写，计划在 NAMD 的未来版本中包含一组脚本。

要运行计算，必须设置关键词 `qmForces on`。要选择 ORCA，必须指定 `qmSoftware "orca"`，并把可执行文件的路径给 `qmExecPath`，同时给出执行计算的目录（`qmBaseDir`）。要将方法和设定从 NAMD 传给 ORCA，使用 `qmConfigLine`。这些行将被复制到输入文件的开头，可以包含简单输入和块输入。为确保计算梯度，应使用 `engrad` 关键词。

QM 区域的几何结构（包括所选链接）以及 MM 点电荷会自动复制到 ORCA 输入文件中。多重度和电荷可以用 `qmMult` 和 `qmCharge` 定义，尽管后者可以由 NAMD 使用 MM 参数自动确定。这里应当注意，NAMD 能够在一次 QM/MM 计算中处理多个 QM 区域。因此对每个区域，都需要电荷和多重度。在只有一个 QM 区域的情况下，输入如下所示：

    qmMult          "1 1"
    qmCharge        "1 0"

目前有两种电荷模式可用：Mulliken 和 CHELPG。它们必须分别在 NAMD 输入中使用 `QMChargeMode` 以及在 `qmConfigLine` 中指定。还有不同的嵌入方案、点电荷方案和开关函数可用，这里不再进一步讨论。另一个值得一提的有用工具是可以在第一次或每次 QM 软件执行之前/之后分别使用 `QMPrepProc` 或 `QMSecProc` 调用辅助可执行文件。两者都以 QM 输入文件的完整路径和名称被调用，例如可用于在 QM/MM-MD 过程中存储数值。

这里特别强调，目前这两个程序都在不断开发中。有关最新信息，应查阅 ORCA 论坛或 NAMD 网站。
