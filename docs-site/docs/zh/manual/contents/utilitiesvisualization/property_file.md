

<a id="sec:property_file.detailed"></a>
# 性质文件（Property File）

ORCA 在计算过程中生成的文件之一是*性质文件（property file）*。该文件名为 `basename.property.txt`，其中 `basename` 是输入文件的基名。

性质文件在 ORCA 中主要有两种用途。第一种用途是作为 *Compound* 脚本语言的基础。*Compound* 通过性质文件读取其所有与性质相关的信息，而不是通过解析 ORCA 输出。性质文件的第二种用途是让其他程序或潜在的 GUI 更容易与 ORCA 创建接口。

与常规 ORCA 输出相比，性质文件的优点是其语法定义良好，因此更容易解析。
它也可以转换为 JSON 格式，如下所示。

对于大多数计算，写入性质文件默认启用。
可以通过 `!NoPropFile` 禁用，或在 `%output` 块中切换开/关：

``` orca
%output
  PropFile false  # default: true
end
```

!!! note "小心"
    由于整个文件在每次单点计算中会被多次读取和重写，
    对含数千个原子的体系进行优化时，每个优化周期可能产生几毫秒的堆积 I/O 开销
    （即几百步之后每个周期约几秒）。
    因此，建议在此类计算中禁用性质文件，
    在简单输入中选择 `GOAT`、`MD-L-Opt`、`MM` 或 `GFN-FF` 时默认已禁用。

<a id="sec:property_file.txtFormat.detailed"></a>
## TXT 格式（TXT Format）

任何 ORCA 计算之后都会创建扩展名为 `.property.txt` 的性质文件。该文件是文本文件，可以用任何可用的文本编辑器读取和编辑。下面我们分析该文件的语法。

文件总是以下面三行开始：

```orca
*************************************************
******************* ORCA 6.1.x ******************
*************************************************
```

显然，其中 ORCA 的版本号会变化
（它也存储在 `Calculation_Status -> version` 中）。

然后，文件由一系列性质组成。每个性质以符号 `$` 加性质名开始，以符号 `$` 加 `End` 结束。

例如：
```orca
$SCF_Nuc_Gradient
   &GeometryIndex 1
   &NAtoms [&Type "Integer"] 2
   &gradNorm [&Type "Double"]       7.6940943132805237e-02
   &grad [&Type "ArrayOfDoubles", &Dim (6,1)]
                                                         0

0                                      6.7009699964043727e-10
1                                     -1.3755030800675890e-10
2                                      5.4405462640094826e-02
3                                     -6.7009699282161039e-10
4                                      1.3755031156980307e-10
5                                     -5.4405462640095381e-02
   &Method [&Type "String"] "SCF"
   &Level [&Type "String"] "Relaxed density"
   &Mult [&Type "Integer"] 1
   &State [&Type "Integer"] 0
   &Irrep [&Type "Integer"] 0
$End
```

每个性质由*分量（components）*组成。每个分量以符号 `&` 开始，没有结束符号。

例如：

```orca
   &gradNorm [&Type "Double"]       7.6940943132805237e-02
```

每个性质中的第一个分量是 `GeometryIndex`，
它表示当前性质所属的几何结构。
例如：

```orca
&GeometryIndex 1
```

请注意，几何索引从 1 开始。

其余分量具有以下语法：
- 首先是分量起始符号 `&`。
- 接着是分量名称。
- 然后是一个方括号，其中包含关于该分量的各种括号信息。有关括号信息语法的细节，请查看 [bracketInfo.detailed](#sec:property_file.txtFormat.bracketInfo.detailed)。

括号之后有不同的选项。

如果类型是 `String`，则期望一个以引号开始的字符串。
例如：

```orca
&Method [&Type "String"] "SCF"
```

如果类型是 `Double` 或 `Integer`，则期望相应类型的数值。
例如：

```orca
&NAtoms [&Type "Integer"] 2 "Number of atoms"
```

如上例所示，在与分量名同一行的数值之后可以可选地出现引号括起的分量描述或注释。
请注意，对于 `Array` 分量，注释实际上出现在数据*之前*。

最后，如果类型是某种 `Array`，则在可选注释之后，
数组从下一行开始写出。
数组按最多 8 个空白符分隔的列写成块。
每个块以一行列索引（从 0 开始）开始。
块中的第二行保留，但当前被忽略。
接下来的各行以行索引开始，后接相应行/列的数据。
例如：

```orca
   &dipoleTotal [&Type "ArrayOfDoubles", &Dim (3,1)] "Total"
                                                         0

0                                     -5.1716015643064861e-01
1                                      5.1774970936823518e-02
2                                      7.8324050140722279e-01
```

请注意，`Complex` 标量打印为两个连续的值，分别代表实部和虚部（位于可选注释之前），
而对于 `ArrayOfComplex`，则先打印整个数组的实部，
再打印虚部。

<a id="sec:property_file.txtFormat.bracketInfo.detailed"></a>
### 括号信息（Bracket Information）

括号信息是用 ',' 分隔的条目列表。
第一个也是最重要的括号条目是 `Type`，
它可以是以下之一：
- `Double`
- `Integer`
- `Boolean`
- `Complex`
- `String`
- `ArrayOfDoubles`
- `ArrayOfIntegers`
- `ArrayOfBooleans`
- `ArrayOfComplex`
- `Coordinates`
%-  "MixedMatrix"  % NOT IMPLEMENTED

例如：

```orca
&NAtoms [&Type "Integer"] 2
```

然后，在 `Type` 是某种数组的情况下，括号必须使用 `Dim` 条目包含数组的维度。请注意，所有数组都是二维的！
例如：

```orca
&ATNO [&Type "ArrayOfIntegers", &Dim (2,1)]
```

如果数值不是原子单位，也可以可选地给出 `Units`。例如：

```orca
&dipoleMagnitude [&Type "Double", &Units "Debye"]       9.4000050960598935e-01
```

<a id="sec:property_file.jsonFormat.detailed"></a>
## JSON 格式（JSON Format）

性质文件也可以以 JSON 格式生成。在内部，这是通过将 `txt` 格式转换为 JSON 格式来实现的。有两种创建 JSON 性质文件的方式。

第一种方式是通过常规 ORCA 输入使用 `JSONPropFile` 关键词。

```orca
%Output
  JSONPropFile True
End
```

这将创建 `basename.property.txt`，此外还会创建 `basename.property.json` 文件。

第二种方式是通过 [`orca_2json` 命令](orca_2json.md#sec:orca_2json.availableinformation.propertyFile)。
为此，首先需要运行常规 ORCA 输入，它会创建 `basename.property.txt` 文件，
然后使用以下命令将其转换为 `basename.property.json`：

```orca
orca_2json basename -property
```

该文件结构如下：
```orca
{
  "<GlobalPropertyName>": {
    "<ComponentName>": <value>,
    <More components>
  },
  <More global properties>
  "Geometries": [
    {
      "Geometry": {
        "Coordinates": {
            "Cartesians": [
                [
                    "<Symbol>",
                    <X>,
                    <Y>,
                    <Z>
                ],
                <More atoms>
            ],
            "Type": "Cartesians",
            "Units": "a.u."
        },
        "NAtoms": <value>,
        <More components>
      },
      "<PropertyName>": {
        "<ComponentName>": <value>,
        <More components>
      },
      <More properties for this geometry>
    },
    <More geometries>
  ]
}
```

“全局”性质（即与几何无关的性质）是：
`Calculation_Status`、`Calculation_Info` 和 `Calculation_Timings`。

大多数分量数据类型都直接转换为相应的 JSON 类型。
所有 `Array` 分量都使用嵌套列表以二维形式存储（即使某一维长度为 1）。`Complex` 和 `ArrayOfComplex` 值以分开的实部和虚部存储：
```orca
"ComplexComponentName": {
  "re": <real part>,
  "im": <imaginary part>
},
"ComplexArrayComponentName": {
  "re": [
      [<r11>, <r12>, <...>],
      [<r21>, <r22>, <...>],
      <...>
    ],
  "im": [
      [<i11>, <i12>, <...>],
      [<i21>, <i22>, <...>],
      <...>
    ]
}
```

<a id="sec:property_file.list"></a>
## 可用性质列表（List of Available Properties）

!!! note "List of available properties"
    | Property | M | Component | T | O | L | Description | Units |
    |---|---|---|---|---|---|---|---|
    | AutoCI_Energies [Energy] | Y | numOfEl | I | N | N |  |  |
    |  |  | numOfCorrEl | I | N | N |  |  |
    |  |  | numOfAlphaCorrEl | I | Y | N |  |  |
    |  |  | numOfBetaCorrEl | I | Y | N |  |  |
    |  |  | refEnergy | AD | N | N | Reference energy for each state |  |
    |  |  | corrEnergy | AD | N | N | Total correlation energy for each state |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | totalEnergy | AD | N | N | Total energy of each state |  |
    |  |  | Mult | AI | Y | N | Multiplicity of each state |  |
    |  |  | Irrep | AI | Y | N | Irreducible representation of each state |  |
    |  |  | RelCorr | S | Y | N | Relativistic correction (SOC and/or SSC) |  |
    |  |  | NBlocks | I | Y | N | Number of multiplicity blocks |  |
    |  |  | NRoots | AI | Y | N | Number of roots in each block |  |
    |  |  | NTotalRoots | I | Y | N | Total number of roots |  |
    |  |  | Block | AI | Y | N | Block index of each state |  |
    |  |  | Root | AI | Y | N | Root index within the block |  |
    |  |  | FollowIRoot | I | Y | N | Index of the followed root |  |
    |  |  | AvgMult | AD | Y | N | Average multiplicity of each SO-/SS-coupled state |  |
    | AutoCI_Dipole_Moment [Dipole_Moment] | Y | dipoleMagnitude | D | N | N |  | a.u. |
    |  |  | dipoleElecContrib | AD | N | N | Electronic contribution |  |
    |  |  | dipoleNucContrib | AD | N | N | Nuclear contribution |  |
    |  |  | dipoleTotal | AD | N | N | Total |  |
    |  |  | doAtomicDipole | B | N | N |  |  |
    |  |  | atomicDipole | AD | Y | N | Atomic dipoles (NAtoms * X,Y,Z) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | EFG_Tensor | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | QFAC | D | N | Y | Prefactor |  |
    |  |  | V | AD | N | Y | Raw tensor |  |
    |  |  | VEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | VIso | D | N | Y |  |  |
    | AutoCI_Polarizability [Polarizability] | Y | isotropicPolar | D | N | N |  |  |
    |  |  | rawCartesian | AD | N | N |  | a.u |
    |  |  | diagonalizedTensor | AD | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | doAtomicPolar | B | N | N |  |  |
    |  |  | atomicPolarIso | AD | Y | N | Atomic istotropic polarizabilities |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | AutoCI_Quadrupole_Moment [Quadrupole_Moment] | Y | isotropicQuadMoment | D | N | N |  | a.u. |
    |  |  | quadElecContrib | AD | N | N | Electronic contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadNucContrib | AD | N | N | Nuclear contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadTotal | AD | N | N | Total. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadDiagonalized | AD | N | N | The diagonalized tensor | a.u. |
    |  |  | doAtomicQuad | B | N | N |  |  |
    |  |  | atomicQuad | AD | Y | N | Atomic quadrupoles (NAtoms * XX, YY, ZZ, XY, XZ, YZ) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | AutoCI_A_Tensor [A_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elem | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | PFAC | D | N | Y | Prefactor PFAC=gegNbe*bN (in MHz) |  |
    |  |  | ARaw | AD | N | Y | Raw tensor |  |
    |  |  | AEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | AIso | D | N | Y |  |  |
    | AUTOCI_Chemical_Shift [Chemical_Shift] | Y | numOfNucs | I | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | SDSO | AD | N | Y | Diamagnetic contribution |  |
    |  |  | SPSO | AD | N | Y | Paramagnetic contribution |  |
    |  |  | STot | AD | N | Y | Total tensor |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | sTotEigen | AD | N | Y | Eigenvalues |  |
    |  |  | siso | D | N | Y |  |  |
    |  |  | saniso | D | N | Y |  |  |
    | AutoCI_D_Tensor [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | AutoCI_G_Tensor [G_Tensor] | Y | g_matrix | AD | N | N |  |  |
    |  |  | g_elec | D | N | N | The free electron g-value contribution |  |
    |  |  | g_RMC | D | N | N | The reduced mass correction |  |
    |  |  | g_DSO | AD | N | N |  |  |
    |  |  | g_PSO | AD | N | N |  |  |
    |  |  | g_Tot | AD | N | N |  |  |
    |  |  | g_iso | D | N | N |  |  |
    |  |  | Delta_g | AD | N | N |  |  |
    |  |  | Delta_g_iso | D | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | AutoCI_Spin_Spin_Coupling [Spin_Spin_Coupling] | Y | numOfNucPairs | I | N | N | Number of nuclei pairs to calculate |  |
    |  |  | numOfNucPairsDSO | I | N | N | number of nuclear pairs to calculate DSO |  |
    |  |  | numOfNucPairsPSO | I | N | N | number of nuclear pairs to calculate PSO |  |
    |  |  | numOfNucPairsFC | I | N | N | number of nuclear pairs to calculate FC |  |
    |  |  | numOfNucPairsSD | I | N | N | number of nuclear pairs to calculate SD |  |
    |  |  | numOfNucPairsSD_FC | I | N | N | number of nuclear pairs to calculate SD/FC |  |
    |  |  | pairsInfo | AI | N | N | Pairs Info: Col1->Index of A. Col2->Atom. Num. of A. Col3->Index of B. Col4->Atom. Num. of B. |  |
    |  |  | pairsDistances | AD | N | N | The distances of each pair |  |
    |  |  | pairsTotalSSCIso | AD | N | N | The Spin-Spin coupling constant for each pair |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | AutoCI_Absorption_Spectrum [Absorption_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | AutoCI_ECD_Spectrum [ECD_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | AutoCI_MRCI_Absorption_Spectrum [Absorption_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | AutoCI_MRCI_ECD_Spectrum [ECD_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | CAS_DCD_Energies [Energy] | Y | finalEnergy | D | N | N | Final GS or SA energy |  |
    |  |  | numOfElectrons | I | N | N |  |  |
    |  |  | numOfActiveEl | I | N | N | Number of active electrons |  |
    |  |  | numOfActiveOrbs | I | N | N | Number of active orbitals |  |
    |  |  | numOfFCElectrons | I | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | totalEnergy | AD | N | N | Total energy of each state |  |
    |  |  | Mult | AI | Y | N | Multiplicity of each state |  |
    |  |  | Irrep | AI | Y | N | Irreducible representation of each state |  |
    |  |  | RelCorr | S | Y | N | Relativistic correction (SOC and/or SSC) |  |
    |  |  | NBlocks | I | Y | N | Number of multiplicity blocks |  |
    |  |  | NRoots | AI | Y | N | Number of roots in each block |  |
    |  |  | NTotalRoots | I | Y | N | Total number of roots |  |
    |  |  | Block | AI | Y | N | Block index of each state |  |
    |  |  | Root | AI | Y | N | Root index within the block |  |
    |  |  | FollowIRoot | I | Y | N | Index of the followed root |  |
    |  |  | AvgMult | AD | Y | N | Average multiplicity of each SO-/SS-coupled state |  |
    | CAS_MSPT2_Energies [Energy] | Y | finalEnergy | D | N | N | Final GS or SA energy |  |
    |  |  | numOfElectrons | I | N | N |  |  |
    |  |  | numOfActiveEl | I | N | N | Number of active electrons |  |
    |  |  | numOfActiveOrbs | I | N | N | Number of active orbitals |  |
    |  |  | numOfFCElectrons | I | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | totalEnergy | AD | N | N | Total energy of each state |  |
    |  |  | Mult | AI | Y | N | Multiplicity of each state |  |
    |  |  | Irrep | AI | Y | N | Irreducible representation of each state |  |
    |  |  | RelCorr | S | Y | N | Relativistic correction (SOC and/or SSC) |  |
    |  |  | NBlocks | I | Y | N | Number of multiplicity blocks |  |
    |  |  | NRoots | AI | Y | N | Number of roots in each block |  |
    |  |  | NTotalRoots | I | Y | N | Total number of roots |  |
    |  |  | Block | AI | Y | N | Block index of each state |  |
    |  |  | Root | AI | Y | N | Root index within the block |  |
    |  |  | FollowIRoot | I | Y | N | Index of the followed root |  |
    |  |  | AvgMult | AD | Y | N | Average multiplicity of each SO-/SS-coupled state |  |
    | CAS_PT2_Energies [Energy] | Y | finalEnergy | D | N | N | Final GS or SA energy |  |
    |  |  | numOfElectrons | I | N | N |  |  |
    |  |  | numOfActiveEl | I | N | N | Number of active electrons |  |
    |  |  | numOfActiveOrbs | I | N | N | Number of active orbitals |  |
    |  |  | numOfFCElectrons | I | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | totalEnergy | AD | N | N | Total energy of each state |  |
    |  |  | Mult | AI | Y | N | Multiplicity of each state |  |
    |  |  | Irrep | AI | Y | N | Irreducible representation of each state |  |
    |  |  | RelCorr | S | Y | N | Relativistic correction (SOC and/or SSC) |  |
    |  |  | NBlocks | I | Y | N | Number of multiplicity blocks |  |
    |  |  | NRoots | AI | Y | N | Number of roots in each block |  |
    |  |  | NTotalRoots | I | Y | N | Total number of roots |  |
    |  |  | Block | AI | Y | N | Block index of each state |  |
    |  |  | Root | AI | Y | N | Root index within the block |  |
    |  |  | FollowIRoot | I | Y | N | Index of the followed root |  |
    |  |  | AvgMult | AD | Y | N | Average multiplicity of each SO-/SS-coupled state |  |
    | CAS_SCF_Energies [Energy] | Y | finalEnergy | D | N | N | Final GS or SA energy |  |
    |  |  | numOfElectrons | I | N | N |  |  |
    |  |  | numOfActiveEl | I | N | N | Number of active electrons |  |
    |  |  | numOfActiveOrbs | I | N | N | Number of active orbitals |  |
    |  |  | numOfFCElectrons | I | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | totalEnergy | AD | N | N | Total energy of each state |  |
    |  |  | Mult | AI | Y | N | Multiplicity of each state |  |
    |  |  | Irrep | AI | Y | N | Irreducible representation of each state |  |
    |  |  | RelCorr | S | Y | N | Relativistic correction (SOC and/or SSC) |  |
    |  |  | NBlocks | I | Y | N | Number of multiplicity blocks |  |
    |  |  | NRoots | AI | Y | N | Number of roots in each block |  |
    |  |  | NTotalRoots | I | Y | N | Total number of roots |  |
    |  |  | Block | AI | Y | N | Block index of each state |  |
    |  |  | Root | AI | Y | N | Root index within the block |  |
    |  |  | FollowIRoot | I | Y | N | Index of the followed root |  |
    |  |  | AvgMult | AD | Y | N | Average multiplicity of each SO-/SS-coupled state |  |
    | CASSCF_Dipole_Moment [Dipole_Moment] | Y | dipoleMagnitude | D | N | N |  | a.u. |
    |  |  | dipoleElecContrib | AD | N | N | Electronic contribution |  |
    |  |  | dipoleNucContrib | AD | N | N | Nuclear contribution |  |
    |  |  | dipoleTotal | AD | N | N | Total |  |
    |  |  | doAtomicDipole | B | N | N |  |  |
    |  |  | atomicDipole | AD | Y | N | Atomic dipoles (NAtoms * X,Y,Z) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | CASSCF_EFG_Tensor [EFG_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | QFAC | D | N | Y | Prefactor |  |
    |  |  | V | AD | N | Y | Raw tensor |  |
    |  |  | VEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | VIso | D | N | Y |  |  |
    | CASSCF_Polarizability [Polarizability] | Y | isotropicPolar | D | N | N |  |  |
    |  |  | rawCartesian | AD | N | N |  | a.u |
    |  |  | diagonalizedTensor | AD | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | doAtomicPolar | B | N | N |  |  |
    |  |  | atomicPolarIso | AD | Y | N | Atomic istotropic polarizabilities |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | CASSCF_Quadrupole_Moment [Quadrupole_Moment] | Y | isotropicQuadMoment | D | N | N |  | a.u. |
    |  |  | quadElecContrib | AD | N | N | Electronic contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadNucContrib | AD | N | N | Nuclear contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadTotal | AD | N | N | Total. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadDiagonalized | AD | N | N | The diagonalized tensor | a.u. |
    |  |  | doAtomicQuad | B | N | N |  |  |
    |  |  | atomicQuad | AD | Y | N | Atomic quadrupoles (NAtoms * XX, YY, ZZ, XY, XZ, YZ) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | CASSCF_A_Tensor [A_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elem | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | PFAC | D | N | Y | Prefactor PFAC=gegNbe*bN (in MHz) |  |
    |  |  | ARaw | AD | N | Y | Raw tensor |  |
    |  |  | AEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | AIso | D | N | Y |  |  |
    | CASSCF_Chemical_Shift [Chemical_Shift] | Y | numOfNucs | I | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | SDSO | AD | N | Y | Diamagnetic contribution |  |
    |  |  | SPSO | AD | N | Y | Paramagnetic contribution |  |
    |  |  | STot | AD | N | Y | Total tensor |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | sTotEigen | AD | N | Y | Eigenvalues |  |
    |  |  | siso | D | N | Y |  |  |
    |  |  | saniso | D | N | Y |  |  |
    | CASSCF_D_Tensor [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | CASSCF_G_Tensor [G_Tensor] | Y | g_matrix | AD | N | N |  |  |
    |  |  | g_elec | D | N | N | The free electron g-value contribution |  |
    |  |  | g_RMC | D | N | N | The reduced mass correction |  |
    |  |  | g_DSO | AD | N | N |  |  |
    |  |  | g_PSO | AD | N | N |  |  |
    |  |  | g_Tot | AD | N | N |  |  |
    |  |  | g_iso | D | N | N |  |  |
    |  |  | Delta_g | AD | N | N |  |  |
    |  |  | Delta_g_iso | D | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | CASSCF_Spin_Spin_Coupling [Spin_Spin_Coupling] | Y | numOfNucPairs | I | N | N | Number of nuclei pairs to calculate |  |
    |  |  | numOfNucPairsDSO | I | N | N | number of nuclear pairs to calculate DSO |  |
    |  |  | numOfNucPairsPSO | I | N | N | number of nuclear pairs to calculate PSO |  |
    |  |  | numOfNucPairsFC | I | N | N | number of nuclear pairs to calculate FC |  |
    |  |  | numOfNucPairsSD | I | N | N | number of nuclear pairs to calculate SD |  |
    |  |  | numOfNucPairsSD_FC | I | N | N | number of nuclear pairs to calculate SD/FC |  |
    |  |  | pairsInfo | AI | N | N | Pairs Info: Col1->Index of A. Col2->Atom. Num. of A. Col3->Index of B. Col4->Atom. Num. of B. |  |
    |  |  | pairsDistances | AD | N | N | The distances of each pair |  |
    |  |  | pairsTotalSSCIso | AD | N | N | The Spin-Spin coupling constant for each pair |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | D_Tensor_CASSCF_2ndOrder [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | D_Tensor_CASSCF_2ndOrder_ES [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | D_Tensor_CASSCF_Heff [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | D_Tensor_CASSCF_Heff_ES [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | D_Tensor_NEVPT2_2ndOrder [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | D_Tensor_NEVPT2_2ndOrder_ES [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | D_Tensor_NEVPT2_Heff [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | D_Tensor_NEVPT2_Heff_ES [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | D_Tensor_CUSTOM_2ndOrder [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | D_Tensor_CUSTOM_2ndOrder_ES [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | D_Tensor_CUSTOM_Heff [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | D_Tensor_CUSTOM_Heff_ES [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | G_Tensor_CASSCF_2ndOrder [G_Tensor] | Y | g_matrix | AD | N | N |  |  |
    |  |  | g_elec | D | N | N | The free electron g-value contribution |  |
    |  |  | g_RMC | D | N | N | The reduced mass correction |  |
    |  |  | g_DSO | AD | N | N |  |  |
    |  |  | g_PSO | AD | N | N |  |  |
    |  |  | g_Tot | AD | N | N |  |  |
    |  |  | g_iso | D | N | N |  |  |
    |  |  | Delta_g | AD | N | N |  |  |
    |  |  | Delta_g_iso | D | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | G_Tensor_CASSCF_Heff [G_Tensor] | Y | g_matrix | AD | N | N |  |  |
    |  |  | g_elec | D | N | N | The free electron g-value contribution |  |
    |  |  | g_RMC | D | N | N | The reduced mass correction |  |
    |  |  | g_DSO | AD | N | N |  |  |
    |  |  | g_PSO | AD | N | N |  |  |
    |  |  | g_Tot | AD | N | N |  |  |
    |  |  | g_iso | D | N | N |  |  |
    |  |  | Delta_g | AD | N | N |  |  |
    |  |  | Delta_g_iso | D | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | G_Tensor_NEVPT2_2ndOrder [G_Tensor] | Y | g_matrix | AD | N | N |  |  |
    |  |  | g_elec | D | N | N | The free electron g-value contribution |  |
    |  |  | g_RMC | D | N | N | The reduced mass correction |  |
    |  |  | g_DSO | AD | N | N |  |  |
    |  |  | g_PSO | AD | N | N |  |  |
    |  |  | g_Tot | AD | N | N |  |  |
    |  |  | g_iso | D | N | N |  |  |
    |  |  | Delta_g | AD | N | N |  |  |
    |  |  | Delta_g_iso | D | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | G_Tensor_NEVPT2_Heff [G_Tensor] | Y | g_matrix | AD | N | N |  |  |
    |  |  | g_elec | D | N | N | The free electron g-value contribution |  |
    |  |  | g_RMC | D | N | N | The reduced mass correction |  |
    |  |  | g_DSO | AD | N | N |  |  |
    |  |  | g_PSO | AD | N | N |  |  |
    |  |  | g_Tot | AD | N | N |  |  |
    |  |  | g_iso | D | N | N |  |  |
    |  |  | Delta_g | AD | N | N |  |  |
    |  |  | Delta_g_iso | D | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | G_Tensor_CUSTOM_2ndOrder [G_Tensor] | Y | g_matrix | AD | N | N |  |  |
    |  |  | g_elec | D | N | N | The free electron g-value contribution |  |
    |  |  | g_RMC | D | N | N | The reduced mass correction |  |
    |  |  | g_DSO | AD | N | N |  |  |
    |  |  | g_PSO | AD | N | N |  |  |
    |  |  | g_Tot | AD | N | N |  |  |
    |  |  | g_iso | D | N | N |  |  |
    |  |  | Delta_g | AD | N | N |  |  |
    |  |  | Delta_g_iso | D | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | G_Tensor_CUSTOM_Heff [G_Tensor] | Y | g_matrix | AD | N | N |  |  |
    |  |  | g_elec | D | N | N | The free electron g-value contribution |  |
    |  |  | g_RMC | D | N | N | The reduced mass correction |  |
    |  |  | g_DSO | AD | N | N |  |  |
    |  |  | g_PSO | AD | N | N |  |  |
    |  |  | g_Tot | AD | N | N |  |  |
    |  |  | g_iso | D | N | N |  |  |
    |  |  | Delta_g | AD | N | N |  |  |
    |  |  | Delta_g_iso | D | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | CASSCF_Absorption_Spectrum [Absorption_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | CASSCF_PT_Absorption_Spectrum [Absorption_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | CASSCF_QDPT_Absorption_Spectrum [Absorption_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | CASSCF_DCD_Absorption_Spectrum [Absorption_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | CASSCF_PT_Energies_Absorption_Spectrum [Absorption_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | CASSCF_Custom_Absorption_Spectrum [Absorption_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | CASSCF_ECD_Spectrum [ECD_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | CASSCF_PT_ECD_Spectrum [ECD_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | CASSCF_QDPT_ECD_Spectrum [ECD_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | CASSCF_DCD_ECD_Spectrum [ECD_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | CASSCF_PT_ECD_Spectrum [ECD_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | CASSCF_Custom_ECD_Spectrum [ECD_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | CIPSI_Energies | N | finalEnergy | D | N | N |  |  |
    |  |  | numOfRoots | I | N | N |  |  |
    |  |  | multiplicity | I | N | N |  |  |
    |  |  | energies | AD | N | N |  |  |
    | CIS_Energies [Energy] | Y | e0 | D | N | N | Ground state energy |  |
    |  |  | multP1 | B | N | N | Do the higher multiplicity too? |  |
    |  |  | mode | S | N | N | CIS mode: CIS, RPA, TDA, TD-DFT, sTDA, sTD-DFT |  |
    |  |  | dCorr | I | N | N | (D) Correction algorithm |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | totalEnergy | AD | N | N | Total energy of each state |  |
    |  |  | Mult | AI | Y | N | Multiplicity of each state |  |
    |  |  | Irrep | AI | Y | N | Irreducible representation of each state |  |
    |  |  | RelCorr | S | Y | N | Relativistic correction (SOC and/or SSC) |  |
    |  |  | NBlocks | I | Y | N | Number of multiplicity blocks |  |
    |  |  | NRoots | AI | Y | N | Number of roots in each block |  |
    |  |  | NTotalRoots | I | Y | N | Total number of roots |  |
    |  |  | Block | AI | Y | N | Block index of each state |  |
    |  |  | Root | AI | Y | N | Root index within the block |  |
    |  |  | FollowIRoot | I | Y | N | Index of the followed root |  |
    |  |  | AvgMult | AD | Y | N | Average multiplicity of each SO-/SS-coupled state |  |
    | CIS_Nuc_Gradient [Nuclear_Gradient] | Y | NAtoms | I | N | N |  |  |
    |  |  | gradNorm | D | N | N |  |  |
    |  |  | grad | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | CIS_Dipole_Moment [Dipole_Moment] | Y | dipoleMagnitude | D | N | N |  | a.u. |
    |  |  | dipoleElecContrib | AD | N | N | Electronic contribution |  |
    |  |  | dipoleNucContrib | AD | N | N | Nuclear contribution |  |
    |  |  | dipoleTotal | AD | N | N | Total |  |
    |  |  | doAtomicDipole | B | N | N |  |  |
    |  |  | atomicDipole | AD | Y | N | Atomic dipoles (NAtoms * X,Y,Z) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | CIS_EFG_Tensor [EFG_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | QFAC | D | N | Y | Prefactor |  |
    |  |  | V | AD | N | Y | Raw tensor |  |
    |  |  | VEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | VIso | D | N | Y |  |  |
    | CIS_Polarizability [Polarizability] | Y | isotropicPolar | D | N | N |  |  |
    |  |  | rawCartesian | AD | N | N |  | a.u |
    |  |  | diagonalizedTensor | AD | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | doAtomicPolar | B | N | N |  |  |
    |  |  | atomicPolarIso | AD | Y | N | Atomic istotropic polarizabilities |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | CIS_Quadrupole_Moment [Quadrupole_Moment] | Y | isotropicQuadMoment | D | N | N |  | a.u. |
    |  |  | quadElecContrib | AD | N | N | Electronic contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadNucContrib | AD | N | N | Nuclear contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadTotal | AD | N | N | Total. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadDiagonalized | AD | N | N | The diagonalized tensor | a.u. |
    |  |  | doAtomicQuad | B | N | N |  |  |
    |  |  | atomicQuad | AD | Y | N | Atomic quadrupoles (NAtoms * XX, YY, ZZ, XY, XZ, YZ) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | CIS_A_Tensor [A_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elem | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | PFAC | D | N | Y | Prefactor PFAC=gegNbe*bN (in MHz) |  |
    |  |  | ARaw | AD | N | Y | Raw tensor |  |
    |  |  | AEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | AIso | D | N | Y |  |  |
    | CIS_Chemical_Shift [Chemical_Shift] | Y | numOfNucs | I | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | SDSO | AD | N | Y | Diamagnetic contribution |  |
    |  |  | SPSO | AD | N | Y | Paramagnetic contribution |  |
    |  |  | STot | AD | N | Y | Total tensor |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | sTotEigen | AD | N | Y | Eigenvalues |  |
    |  |  | siso | D | N | Y |  |  |
    |  |  | saniso | D | N | Y |  |  |
    | CIS_D_Tensor [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | CIS_G_Tensor [G_Tensor] | Y | g_matrix | AD | N | N |  |  |
    |  |  | g_elec | D | N | N | The free electron g-value contribution |  |
    |  |  | g_RMC | D | N | N | The reduced mass correction |  |
    |  |  | g_DSO | AD | N | N |  |  |
    |  |  | g_PSO | AD | N | N |  |  |
    |  |  | g_Tot | AD | N | N |  |  |
    |  |  | g_iso | D | N | N |  |  |
    |  |  | Delta_g | AD | N | N |  |  |
    |  |  | Delta_g_iso | D | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | CIS_Spin_Spin_Coupling [Spin_Spin_Coupling] | Y | numOfNucPairs | I | N | N | Number of nuclei pairs to calculate |  |
    |  |  | numOfNucPairsDSO | I | N | N | number of nuclear pairs to calculate DSO |  |
    |  |  | numOfNucPairsPSO | I | N | N | number of nuclear pairs to calculate PSO |  |
    |  |  | numOfNucPairsFC | I | N | N | number of nuclear pairs to calculate FC |  |
    |  |  | numOfNucPairsSD | I | N | N | number of nuclear pairs to calculate SD |  |
    |  |  | numOfNucPairsSD_FC | I | N | N | number of nuclear pairs to calculate SD/FC |  |
    |  |  | pairsInfo | AI | N | N | Pairs Info: Col1->Index of A. Col2->Atom. Num. of A. Col3->Index of B. Col4->Atom. Num. of B. |  |
    |  |  | pairsDistances | AD | N | N | The distances of each pair |  |
    |  |  | pairsTotalSSCIso | AD | N | N | The Spin-Spin coupling constant for each pair |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | CIS_Absorption_Spectrum [Absorption_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | CIS_ECD_Spectrum [ECD_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | DBOC_Energy | N | DBOC_Energy | D | N | N |  |  |
    | DFT_Energy | N | nAlphaEl | I | N | N |  |  |
    |  |  | nBetaEl | I | N | N |  |  |
    |  |  | nTotalEl | I | N | N |  |  |
    |  |  | finalEn | D | N | N | No Van der Waals correction |  |
    |  |  | eExchange | D | N | N |  |  |
    |  |  | eCorr | D | N | N |  |  |
    |  |  | eXC | D | N | N |  |  |
    |  |  | eCNL | D | N | N |  |  |
    |  |  | eEmbed | D | Y | N |  |  |
    | BROKEN_SYMMETRY | N | enHighSpin | D | N | N | The High Spin Energy |  |
    |  |  | enBrokenSym | D | N | N | The Broken Symmetry Energy |  |
    |  |  | SHighSpin | D | N | N | The High Spin Spin |  |
    |  |  | S2HighSpin | D | N | N | The Expectation value of S**2 for the High Spin case |  |
    |  |  | S2BrokenSym | D | N | N | The Expectation value of S**2 for the Broken symmetry case |  |
    | Dipole_Moment | Y | dipoleMagnitude | D | N | N |  | a.u. |
    |  |  | dipoleElecContrib | AD | N | N | Electronic contribution |  |
    |  |  | dipoleNucContrib | AD | N | N | Nuclear contribution |  |
    |  |  | dipoleTotal | AD | N | N | Total |  |
    |  |  | doAtomicDipole | B | N | N |  |  |
    |  |  | atomicDipole | AD | Y | N | Atomic dipoles (NAtoms * X,Y,Z) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | EFG_Tensor | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | QFAC | D | N | Y | Prefactor |  |
    |  |  | V | AD | N | Y | Raw tensor |  |
    |  |  | VEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | VIso | D | N | Y |  |  |
    | Quadrupole_Moment | Y | isotropicQuadMoment | D | N | N |  | a.u. |
    |  |  | quadElecContrib | AD | N | N | Electronic contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadNucContrib | AD | N | N | Nuclear contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadTotal | AD | N | N | Total. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadDiagonalized | AD | N | N | The diagonalized tensor | a.u. |
    |  |  | doAtomicQuad | B | N | N |  |  |
    |  |  | atomicQuad | AD | Y | N | Atomic quadrupoles (NAtoms * XX, YY, ZZ, XY, XZ, YZ) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | Polarizability | Y | isotropicPolar | D | N | N |  |  |
    |  |  | rawCartesian | AD | N | N |  | a.u |
    |  |  | diagonalizedTensor | AD | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | doAtomicPolar | B | N | N |  |  |
    |  |  | atomicPolarIso | AD | Y | N | Atomic istotropic polarizabilities |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | Hyperpolarizability | Y | rawCartesian | AD | N | N |  | a.u |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | Excited_States_Dynamics | N | fluorRateConstant | D | N | N |  |  |
    | Energy_Extrapolation | N | doEp1 | B | N | N | Extrapolation using only one method |  |
    |  |  | doEp2 | B | N | N | Extrapolation using two different methods (same small basis Set) |  |
    |  |  | doEp3 | B | N | N | Extrapolation using two different methods (use three basis Sets for the cheap method) |  |
    |  |  | doGradients | B | N | N | Extrapolate energy gradients |  |
    |  |  | scfEnergies | AD | N | N |  |  |
    |  |  | scfCBS | D | N | N |  |  |
    |  |  | scfGradients | AD | Y | N | The SCF Gradients |  |
    |  |  | corrEnergies | AD | N | N |  |  |
    |  |  | corrCBS | D | N | N |  |  |
    |  |  | ccsdtEnergyX | D | Y | N |  |  |
    |  |  | totalCBS | D | N | N |  |  |
    |  |  | cardinalNumbers | AI | N | N |  |  |
    |  |  | alphas | AD | N | N |  |  |
    |  |  | betas | AD | N | N |  |  |
    |  |  | numOfEnergies | I | N | N | How many energies we are going to use (e.g. two-point scheme). |  |
    |  |  | basisName | S | N | Y |  |  |
    | gCP_Energy | N | gCP_Energy | D | N | N |  |  |
    | Hessian | N | HESSIAN | AD | N | N | The Hessian |  |
    |  |  | MODES | AD | N | N | The modes of vibrations |  |
    | ICE_Dipole_Moment [Dipole_Moment] | Y | dipoleMagnitude | D | N | N |  | a.u. |
    |  |  | dipoleElecContrib | AD | N | N | Electronic contribution |  |
    |  |  | dipoleNucContrib | AD | N | N | Nuclear contribution |  |
    |  |  | dipoleTotal | AD | N | N | Total |  |
    |  |  | doAtomicDipole | B | N | N |  |  |
    |  |  | atomicDipole | AD | Y | N | Atomic dipoles (NAtoms * X,Y,Z) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | ICE_EFG_Tensor [EFG_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | QFAC | D | N | Y | Prefactor |  |
    |  |  | V | AD | N | Y | Raw tensor |  |
    |  |  | VEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | VIso | D | N | Y |  |  |
    | ICE_Polarizability [Polarizability] | Y | isotropicPolar | D | N | N |  |  |
    |  |  | rawCartesian | AD | N | N |  | a.u |
    |  |  | diagonalizedTensor | AD | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | doAtomicPolar | B | N | N |  |  |
    |  |  | atomicPolarIso | AD | Y | N | Atomic istotropic polarizabilities |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | ICE_Quadrupole_Moment [Quadrupole_Moment] | Y | isotropicQuadMoment | D | N | N |  | a.u. |
    |  |  | quadElecContrib | AD | N | N | Electronic contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadNucContrib | AD | N | N | Nuclear contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadTotal | AD | N | N | Total. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadDiagonalized | AD | N | N | The diagonalized tensor | a.u. |
    |  |  | doAtomicQuad | B | N | N |  |  |
    |  |  | atomicQuad | AD | Y | N | Atomic quadrupoles (NAtoms * XX, YY, ZZ, XY, XZ, YZ) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | ICE_A_Tensor [A_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elem | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | PFAC | D | N | Y | Prefactor PFAC=gegNbe*bN (in MHz) |  |
    |  |  | ARaw | AD | N | Y | Raw tensor |  |
    |  |  | AEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | AIso | D | N | Y |  |  |
    | ICE_Chemical_Shift [Chemical_Shift] | Y | numOfNucs | I | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | SDSO | AD | N | Y | Diamagnetic contribution |  |
    |  |  | SPSO | AD | N | Y | Paramagnetic contribution |  |
    |  |  | STot | AD | N | Y | Total tensor |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | sTotEigen | AD | N | Y | Eigenvalues |  |
    |  |  | siso | D | N | Y |  |  |
    |  |  | saniso | D | N | Y |  |  |
    | ICE_D_Tensor [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | ICE_G_Tensor [G_Tensor] | Y | g_matrix | AD | N | N |  |  |
    |  |  | g_elec | D | N | N | The free electron g-value contribution |  |
    |  |  | g_RMC | D | N | N | The reduced mass correction |  |
    |  |  | g_DSO | AD | N | N |  |  |
    |  |  | g_PSO | AD | N | N |  |  |
    |  |  | g_Tot | AD | N | N |  |  |
    |  |  | g_iso | D | N | N |  |  |
    |  |  | Delta_g | AD | N | N |  |  |
    |  |  | Delta_g_iso | D | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | ICE_Spin_Spin_Coupling [Spin_Spin_Coupling] | Y | numOfNucPairs | I | N | N | Number of nuclei pairs to calculate |  |
    |  |  | numOfNucPairsDSO | I | N | N | number of nuclear pairs to calculate DSO |  |
    |  |  | numOfNucPairsPSO | I | N | N | number of nuclear pairs to calculate PSO |  |
    |  |  | numOfNucPairsFC | I | N | N | number of nuclear pairs to calculate FC |  |
    |  |  | numOfNucPairsSD | I | N | N | number of nuclear pairs to calculate SD |  |
    |  |  | numOfNucPairsSD_FC | I | N | N | number of nuclear pairs to calculate SD/FC |  |
    |  |  | pairsInfo | AI | N | N | Pairs Info: Col1->Index of A. Col2->Atom. Num. of A. Col3->Index of B. Col4->Atom. Num. of B. |  |
    |  |  | pairsDistances | AD | N | N | The distances of each pair |  |
    |  |  | pairsTotalSSCIso | AD | N | N | The Spin-Spin coupling constant for each pair |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | ICE_Absorption_Spectrum [Absorption_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | ICE_ECD_Spectrum [ECD_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | Calculation_Info | N | Mult | I | N | N |  |  |
    |  |  | Charge | I | N | N |  |  |
    |  |  | NumOfAtoms | I | N | N |  |  |
    |  |  | NumOfElectrons | I | N | N |  |  |
    |  |  | NumOfBasisFuncts | I | N | N |  |  |
    |  |  | NumOfAuxCBasisFuncts | I | N | N |  |  |
    |  |  | NumOfAuxJBasisFuncts | I | N | N |  |  |
    |  |  | NumOfAuxJKBasisFuncts | I | N | N |  |  |
    |  |  | NumOfCABSBasisFuncts | I | N | N |  |  |
    | Single_Point_Data | N | FinalEnergy | D | N | N | Final single point energy |  |
    |  |  | Converged | B | N | N |  |  |
    | LFT_Absorption_Spectrum [Absorption_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | LFT_ECD_Spectrum [ECD_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | A_Tensor | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elem | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | PFAC | D | N | Y | Prefactor PFAC=gegNbe*bN (in MHz) |  |
    |  |  | ARaw | AD | N | Y | Raw tensor |  |
    |  |  | AEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | AIso | D | N | Y |  |  |
    | Chemical_Shift | Y | numOfNucs | I | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | SDSO | AD | N | Y | Diamagnetic contribution |  |
    |  |  | SPSO | AD | N | Y | Paramagnetic contribution |  |
    |  |  | STot | AD | N | Y | Total tensor |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | sTotEigen | AD | N | Y | Eigenvalues |  |
    |  |  | siso | D | N | Y |  |  |
    |  |  | saniso | D | N | Y |  |  |
    | D_Tensor | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | G_Tensor | Y | g_matrix | AD | N | N |  |  |
    |  |  | g_elec | D | N | N | The free electron g-value contribution |  |
    |  |  | g_RMC | D | N | N | The reduced mass correction |  |
    |  |  | g_DSO | AD | N | N |  |  |
    |  |  | g_PSO | AD | N | N |  |  |
    |  |  | g_Tot | AD | N | N |  |  |
    |  |  | g_iso | D | N | N |  |  |
    |  |  | Delta_g | AD | N | N |  |  |
    |  |  | Delta_g_iso | D | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | Spin_Spin_Coupling | Y | numOfNucPairs | I | N | N | Number of nuclei pairs to calculate |  |
    |  |  | numOfNucPairsDSO | I | N | N | number of nuclear pairs to calculate DSO |  |
    |  |  | numOfNucPairsPSO | I | N | N | number of nuclear pairs to calculate PSO |  |
    |  |  | numOfNucPairsFC | I | N | N | number of nuclear pairs to calculate FC |  |
    |  |  | numOfNucPairsSD | I | N | N | number of nuclear pairs to calculate SD |  |
    |  |  | numOfNucPairsSD_FC | I | N | N | number of nuclear pairs to calculate SD/FC |  |
    |  |  | pairsInfo | AI | N | N | Pairs Info: Col1->Index of A. Col2->Atom. Num. of A. Col3->Index of B. Col4->Atom. Num. of B. |  |
    |  |  | pairsDistances | AD | N | N | The distances of each pair |  |
    |  |  | pairsTotalSSCIso | AD | N | N | The Spin-Spin coupling constant for each pair |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MCRPA_Dipole_Moment [Dipole_Moment] | Y | dipoleMagnitude | D | N | N |  | a.u. |
    |  |  | dipoleElecContrib | AD | N | N | Electronic contribution |  |
    |  |  | dipoleNucContrib | AD | N | N | Nuclear contribution |  |
    |  |  | dipoleTotal | AD | N | N | Total |  |
    |  |  | doAtomicDipole | B | N | N |  |  |
    |  |  | atomicDipole | AD | Y | N | Atomic dipoles (NAtoms * X,Y,Z) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MCRPA_EFG_Tensor [EFG_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | QFAC | D | N | Y | Prefactor |  |
    |  |  | V | AD | N | Y | Raw tensor |  |
    |  |  | VEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | VIso | D | N | Y |  |  |
    | MCRPA_Polarizability [Polarizability] | Y | isotropicPolar | D | N | N |  |  |
    |  |  | rawCartesian | AD | N | N |  | a.u |
    |  |  | diagonalizedTensor | AD | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | doAtomicPolar | B | N | N |  |  |
    |  |  | atomicPolarIso | AD | Y | N | Atomic istotropic polarizabilities |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MCRPA_Quadrupole_Moment [Quadrupole_Moment] | Y | isotropicQuadMoment | D | N | N |  | a.u. |
    |  |  | quadElecContrib | AD | N | N | Electronic contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadNucContrib | AD | N | N | Nuclear contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadTotal | AD | N | N | Total. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadDiagonalized | AD | N | N | The diagonalized tensor | a.u. |
    |  |  | doAtomicQuad | B | N | N |  |  |
    |  |  | atomicQuad | AD | Y | N | Atomic quadrupoles (NAtoms * XX, YY, ZZ, XY, XZ, YZ) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MCRPA_A_Tensor [A_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elem | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | PFAC | D | N | Y | Prefactor PFAC=gegNbe*bN (in MHz) |  |
    |  |  | ARaw | AD | N | Y | Raw tensor |  |
    |  |  | AEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | AIso | D | N | Y |  |  |
    | MCRPA_Chemical_Shift [Chemical_Shift] | Y | numOfNucs | I | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | SDSO | AD | N | Y | Diamagnetic contribution |  |
    |  |  | SPSO | AD | N | Y | Paramagnetic contribution |  |
    |  |  | STot | AD | N | Y | Total tensor |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | sTotEigen | AD | N | Y | Eigenvalues |  |
    |  |  | siso | D | N | Y |  |  |
    |  |  | saniso | D | N | Y |  |  |
    | MCRPA_D_Tensor [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MCRPA_G_Tensor [G_Tensor] | Y | g_matrix | AD | N | N |  |  |
    |  |  | g_elec | D | N | N | The free electron g-value contribution |  |
    |  |  | g_RMC | D | N | N | The reduced mass correction |  |
    |  |  | g_DSO | AD | N | N |  |  |
    |  |  | g_PSO | AD | N | N |  |  |
    |  |  | g_Tot | AD | N | N |  |  |
    |  |  | g_iso | D | N | N |  |  |
    |  |  | Delta_g | AD | N | N |  |  |
    |  |  | Delta_g_iso | D | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MCRPA_Spin_Spin_Coupling [Spin_Spin_Coupling] | Y | numOfNucPairs | I | N | N | Number of nuclei pairs to calculate |  |
    |  |  | numOfNucPairsDSO | I | N | N | number of nuclear pairs to calculate DSO |  |
    |  |  | numOfNucPairsPSO | I | N | N | number of nuclear pairs to calculate PSO |  |
    |  |  | numOfNucPairsFC | I | N | N | number of nuclear pairs to calculate FC |  |
    |  |  | numOfNucPairsSD | I | N | N | number of nuclear pairs to calculate SD |  |
    |  |  | numOfNucPairsSD_FC | I | N | N | number of nuclear pairs to calculate SD/FC |  |
    |  |  | pairsInfo | AI | N | N | Pairs Info: Col1->Index of A. Col2->Atom. Num. of A. Col3->Index of B. Col4->Atom. Num. of B. |  |
    |  |  | pairsDistances | AD | N | N | The distances of each pair |  |
    |  |  | pairsTotalSSCIso | AD | N | N | The Spin-Spin coupling constant for each pair |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MCRPA_Absorption_Spectrum [Absorption_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | MCRPA_ECD_Spectrum [ECD_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | MDCI_Energies [Energy] | Y | numOfEl | I | N | N |  |  |
    |  |  | numOfCorrEl | I | N | N |  |  |
    |  |  | numOfAlphaCorrEl | I | N | N |  |  |
    |  |  | numOfBetaCorrEl | I | N | N |  |  |
    |  |  | refEnergy | AD | N | N | Reference Energy |  |
    |  |  | corrEnergy | AD | N | N | Total Correlation Energy |  |
    |  |  | aaCorrEn | AD | N | N | Alpha-Alpha Pairs Correlation Energy (No (T)) |  |
    |  |  | bbCorrEn | AD | N | N | Beta-Beta Pairs Correlation Energy (No (T)) |  |
    |  |  | abCorrEn | AD | N | N | Alpha-Beta Pairs Correlation Energy (No (T)) |  |
    |  |  | CorrDS | AD | Y | N | Singlet pairs energy of double amplitudes (No (T)) |  |
    |  |  | CorrDT | AD | Y | N | Triplet pairs energy of double amplitudes (No (T)) |  |
    |  |  | CorrSS | AD | Y | N | Singlet pairs energy of quadratic single amplitudes (No (T)) |  |
    |  |  | CorrST | AD | Y | N | Triplet pairs energy of quadratic single amplitudes (No (T)) |  |
    |  |  | triplesEnergy | AD | N | N | Triples Correction Energy |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | totalEnergy | AD | N | N | Total energy of each state |  |
    |  |  | Mult | AI | Y | N | Multiplicity of each state |  |
    |  |  | Irrep | AI | Y | N | Irreducible representation of each state |  |
    |  |  | RelCorr | S | Y | N | Relativistic correction (SOC and/or SSC) |  |
    |  |  | NBlocks | I | Y | N | Number of multiplicity blocks |  |
    |  |  | NRoots | AI | Y | N | Number of roots in each block |  |
    |  |  | NTotalRoots | I | Y | N | Total number of roots |  |
    |  |  | Block | AI | Y | N | Block index of each state |  |
    |  |  | Root | AI | Y | N | Root index within the block |  |
    |  |  | FollowIRoot | I | Y | N | Index of the followed root |  |
    |  |  | AvgMult | AD | Y | N | Average multiplicity of each SO-/SS-coupled state |  |
    | MDCI_Nuc_Gradient [Nuclear_Gradient] | Y | NAtoms | I | N | N |  |  |
    |  |  | gradNorm | D | N | N |  |  |
    |  |  | grad | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MDCI_Dipole_Moment [Dipole_Moment] | Y | dipoleMagnitude | D | N | N |  | a.u. |
    |  |  | dipoleElecContrib | AD | N | N | Electronic contribution |  |
    |  |  | dipoleNucContrib | AD | N | N | Nuclear contribution |  |
    |  |  | dipoleTotal | AD | N | N | Total |  |
    |  |  | doAtomicDipole | B | N | N |  |  |
    |  |  | atomicDipole | AD | Y | N | Atomic dipoles (NAtoms * X,Y,Z) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MDCI_EFG_Tensor [EFG_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | QFAC | D | N | Y | Prefactor |  |
    |  |  | V | AD | N | Y | Raw tensor |  |
    |  |  | VEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | VIso | D | N | Y |  |  |
    | MDCI_Polarizability [Polarizability] | Y | isotropicPolar | D | N | N |  |  |
    |  |  | rawCartesian | AD | N | N |  | a.u |
    |  |  | diagonalizedTensor | AD | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | doAtomicPolar | B | N | N |  |  |
    |  |  | atomicPolarIso | AD | Y | N | Atomic istotropic polarizabilities |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MDCI_Quadrupole_Moment [Quadrupole_Moment] | Y | isotropicQuadMoment | D | N | N |  | a.u. |
    |  |  | quadElecContrib | AD | N | N | Electronic contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadNucContrib | AD | N | N | Nuclear contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadTotal | AD | N | N | Total. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadDiagonalized | AD | N | N | The diagonalized tensor | a.u. |
    |  |  | doAtomicQuad | B | N | N |  |  |
    |  |  | atomicQuad | AD | Y | N | Atomic quadrupoles (NAtoms * XX, YY, ZZ, XY, XZ, YZ) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MDCI_A_Tensor [A_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elem | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | PFAC | D | N | Y | Prefactor PFAC=gegNbe*bN (in MHz) |  |
    |  |  | ARaw | AD | N | Y | Raw tensor |  |
    |  |  | AEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | AIso | D | N | Y |  |  |
    | MDCI_Chemical_Shift [Chemical_Shift] | Y | numOfNucs | I | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | SDSO | AD | N | Y | Diamagnetic contribution |  |
    |  |  | SPSO | AD | N | Y | Paramagnetic contribution |  |
    |  |  | STot | AD | N | Y | Total tensor |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | sTotEigen | AD | N | Y | Eigenvalues |  |
    |  |  | siso | D | N | Y |  |  |
    |  |  | saniso | D | N | Y |  |  |
    | MDCI_D_Tensor [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MDCI_G_Tensor [G_Tensor] | Y | g_matrix | AD | N | N |  |  |
    |  |  | g_elec | D | N | N | The free electron g-value contribution |  |
    |  |  | g_RMC | D | N | N | The reduced mass correction |  |
    |  |  | g_DSO | AD | N | N |  |  |
    |  |  | g_PSO | AD | N | N |  |  |
    |  |  | g_Tot | AD | N | N |  |  |
    |  |  | g_iso | D | N | N |  |  |
    |  |  | Delta_g | AD | N | N |  |  |
    |  |  | Delta_g_iso | D | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MDCI_Spin_Spin_Coupling [Spin_Spin_Coupling] | Y | numOfNucPairs | I | N | N | Number of nuclei pairs to calculate |  |
    |  |  | numOfNucPairsDSO | I | N | N | number of nuclear pairs to calculate DSO |  |
    |  |  | numOfNucPairsPSO | I | N | N | number of nuclear pairs to calculate PSO |  |
    |  |  | numOfNucPairsFC | I | N | N | number of nuclear pairs to calculate FC |  |
    |  |  | numOfNucPairsSD | I | N | N | number of nuclear pairs to calculate SD |  |
    |  |  | numOfNucPairsSD_FC | I | N | N | number of nuclear pairs to calculate SD/FC |  |
    |  |  | pairsInfo | AI | N | N | Pairs Info: Col1->Index of A. Col2->Atom. Num. of A. Col3->Index of B. Col4->Atom. Num. of B. |  |
    |  |  | pairsDistances | AD | N | N | The distances of each pair |  |
    |  |  | pairsTotalSSCIso | AD | N | N | The Spin-Spin coupling constant for each pair |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MDCI_Absorption_Spectrum [Absorption_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | MDCI_ECD_Spectrum [ECD_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | MP2_Energies [Energy] | Y | refEnergy | AD | N | N | Reference energy for each state |  |
    |  |  | corrEnergy | AD | N | N | MP2 correlation energy for each state |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | totalEnergy | AD | N | N | Total energy of each state |  |
    |  |  | Mult | AI | Y | N | Multiplicity of each state |  |
    |  |  | Irrep | AI | Y | N | Irreducible representation of each state |  |
    |  |  | RelCorr | S | Y | N | Relativistic correction (SOC and/or SSC) |  |
    |  |  | NBlocks | I | Y | N | Number of multiplicity blocks |  |
    |  |  | NRoots | AI | Y | N | Number of roots in each block |  |
    |  |  | NTotalRoots | I | Y | N | Total number of roots |  |
    |  |  | Block | AI | Y | N | Block index of each state |  |
    |  |  | Root | AI | Y | N | Root index within the block |  |
    |  |  | FollowIRoot | I | Y | N | Index of the followed root |  |
    |  |  | AvgMult | AD | Y | N | Average multiplicity of each SO-/SS-coupled state |  |
    | MP2_Nuc_Gradient [Nuclear_Gradient] | Y | NAtoms | I | N | N |  |  |
    |  |  | gradNorm | D | N | N |  |  |
    |  |  | grad | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MP2_Dipole_Moment [Dipole_Moment] | Y | dipoleMagnitude | D | N | N |  | a.u. |
    |  |  | dipoleElecContrib | AD | N | N | Electronic contribution |  |
    |  |  | dipoleNucContrib | AD | N | N | Nuclear contribution |  |
    |  |  | dipoleTotal | AD | N | N | Total |  |
    |  |  | doAtomicDipole | B | N | N |  |  |
    |  |  | atomicDipole | AD | Y | N | Atomic dipoles (NAtoms * X,Y,Z) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MP2_EFG_Tensor [EFG_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | QFAC | D | N | Y | Prefactor |  |
    |  |  | V | AD | N | Y | Raw tensor |  |
    |  |  | VEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | VIso | D | N | Y |  |  |
    | MP2_Polarizability [Polarizability] | Y | isotropicPolar | D | N | N |  |  |
    |  |  | rawCartesian | AD | N | N |  | a.u |
    |  |  | diagonalizedTensor | AD | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | doAtomicPolar | B | N | N |  |  |
    |  |  | atomicPolarIso | AD | Y | N | Atomic istotropic polarizabilities |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MP2_Quadrupole_Moment [Quadrupole_Moment] | Y | isotropicQuadMoment | D | N | N |  | a.u. |
    |  |  | quadElecContrib | AD | N | N | Electronic contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadNucContrib | AD | N | N | Nuclear contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadTotal | AD | N | N | Total. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadDiagonalized | AD | N | N | The diagonalized tensor | a.u. |
    |  |  | doAtomicQuad | B | N | N |  |  |
    |  |  | atomicQuad | AD | Y | N | Atomic quadrupoles (NAtoms * XX, YY, ZZ, XY, XZ, YZ) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MP2_A_Tensor [A_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elem | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | PFAC | D | N | Y | Prefactor PFAC=gegNbe*bN (in MHz) |  |
    |  |  | ARaw | AD | N | Y | Raw tensor |  |
    |  |  | AEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | AIso | D | N | Y |  |  |
    | MP2_Chemical_Shift [Chemical_Shift] | Y | numOfNucs | I | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | SDSO | AD | N | Y | Diamagnetic contribution |  |
    |  |  | SPSO | AD | N | Y | Paramagnetic contribution |  |
    |  |  | STot | AD | N | Y | Total tensor |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | sTotEigen | AD | N | Y | Eigenvalues |  |
    |  |  | siso | D | N | Y |  |  |
    |  |  | saniso | D | N | Y |  |  |
    | MP2_D_Tensor [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MP2_G_Tensor [G_Tensor] | Y | g_matrix | AD | N | N |  |  |
    |  |  | g_elec | D | N | N | The free electron g-value contribution |  |
    |  |  | g_RMC | D | N | N | The reduced mass correction |  |
    |  |  | g_DSO | AD | N | N |  |  |
    |  |  | g_PSO | AD | N | N |  |  |
    |  |  | g_Tot | AD | N | N |  |  |
    |  |  | g_iso | D | N | N |  |  |
    |  |  | Delta_g | AD | N | N |  |  |
    |  |  | Delta_g_iso | D | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MP2_Spin_Spin_Coupling [Spin_Spin_Coupling] | Y | numOfNucPairs | I | N | N | Number of nuclei pairs to calculate |  |
    |  |  | numOfNucPairsDSO | I | N | N | number of nuclear pairs to calculate DSO |  |
    |  |  | numOfNucPairsPSO | I | N | N | number of nuclear pairs to calculate PSO |  |
    |  |  | numOfNucPairsFC | I | N | N | number of nuclear pairs to calculate FC |  |
    |  |  | numOfNucPairsSD | I | N | N | number of nuclear pairs to calculate SD |  |
    |  |  | numOfNucPairsSD_FC | I | N | N | number of nuclear pairs to calculate SD/FC |  |
    |  |  | pairsInfo | AI | N | N | Pairs Info: Col1->Index of A. Col2->Atom. Num. of A. Col3->Index of B. Col4->Atom. Num. of B. |  |
    |  |  | pairsDistances | AD | N | N | The distances of each pair |  |
    |  |  | pairsTotalSSCIso | AD | N | N | The Spin-Spin coupling constant for each pair |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MP2_Absorption_Spectrum [Absorption_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | MP2_ECD_Spectrum [ECD_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | MRCI_Dipole_Moment [Dipole_Moment] | Y | dipoleMagnitude | D | N | N |  | a.u. |
    |  |  | dipoleElecContrib | AD | N | N | Electronic contribution |  |
    |  |  | dipoleNucContrib | AD | N | N | Nuclear contribution |  |
    |  |  | dipoleTotal | AD | N | N | Total |  |
    |  |  | doAtomicDipole | B | N | N |  |  |
    |  |  | atomicDipole | AD | Y | N | Atomic dipoles (NAtoms * X,Y,Z) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MRCI_EFG_Tensor [EFG_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | QFAC | D | N | Y | Prefactor |  |
    |  |  | V | AD | N | Y | Raw tensor |  |
    |  |  | VEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | VIso | D | N | Y |  |  |
    | MRCI_Polarizability [Polarizability] | Y | isotropicPolar | D | N | N |  |  |
    |  |  | rawCartesian | AD | N | N |  | a.u |
    |  |  | diagonalizedTensor | AD | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | doAtomicPolar | B | N | N |  |  |
    |  |  | atomicPolarIso | AD | Y | N | Atomic istotropic polarizabilities |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MRCI_Quadrupole_Moment [Quadrupole_Moment] | Y | isotropicQuadMoment | D | N | N |  | a.u. |
    |  |  | quadElecContrib | AD | N | N | Electronic contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadNucContrib | AD | N | N | Nuclear contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadTotal | AD | N | N | Total. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadDiagonalized | AD | N | N | The diagonalized tensor | a.u. |
    |  |  | doAtomicQuad | B | N | N |  |  |
    |  |  | atomicQuad | AD | Y | N | Atomic quadrupoles (NAtoms * XX, YY, ZZ, XY, XZ, YZ) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MRCI_A_Tensor [A_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elem | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | PFAC | D | N | Y | Prefactor PFAC=gegNbe*bN (in MHz) |  |
    |  |  | ARaw | AD | N | Y | Raw tensor |  |
    |  |  | AEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | AIso | D | N | Y |  |  |
    | MRCI_Chemical_Shift [Chemical_Shift] | Y | numOfNucs | I | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | SDSO | AD | N | Y | Diamagnetic contribution |  |
    |  |  | SPSO | AD | N | Y | Paramagnetic contribution |  |
    |  |  | STot | AD | N | Y | Total tensor |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | sTotEigen | AD | N | Y | Eigenvalues |  |
    |  |  | siso | D | N | Y |  |  |
    |  |  | saniso | D | N | Y |  |  |
    | MRCI_D_Tensor [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MRCI_G_Tensor [G_Tensor] | Y | g_matrix | AD | N | N |  |  |
    |  |  | g_elec | D | N | N | The free electron g-value contribution |  |
    |  |  | g_RMC | D | N | N | The reduced mass correction |  |
    |  |  | g_DSO | AD | N | N |  |  |
    |  |  | g_PSO | AD | N | N |  |  |
    |  |  | g_Tot | AD | N | N |  |  |
    |  |  | g_iso | D | N | N |  |  |
    |  |  | Delta_g | AD | N | N |  |  |
    |  |  | Delta_g_iso | D | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MRCI_Spin_Spin_Coupling [Spin_Spin_Coupling] | Y | numOfNucPairs | I | N | N | Number of nuclei pairs to calculate |  |
    |  |  | numOfNucPairsDSO | I | N | N | number of nuclear pairs to calculate DSO |  |
    |  |  | numOfNucPairsPSO | I | N | N | number of nuclear pairs to calculate PSO |  |
    |  |  | numOfNucPairsFC | I | N | N | number of nuclear pairs to calculate FC |  |
    |  |  | numOfNucPairsSD | I | N | N | number of nuclear pairs to calculate SD |  |
    |  |  | numOfNucPairsSD_FC | I | N | N | number of nuclear pairs to calculate SD/FC |  |
    |  |  | pairsInfo | AI | N | N | Pairs Info: Col1->Index of A. Col2->Atom. Num. of A. Col3->Index of B. Col4->Atom. Num. of B. |  |
    |  |  | pairsDistances | AD | N | N | The distances of each pair |  |
    |  |  | pairsTotalSSCIso | AD | N | N | The Spin-Spin coupling constant for each pair |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | D_Tensor_MRCI_2ndOrder [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | D_Tensor_MRCI_2ndOrder_ES [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | D_Tensor_MRCI_Heff [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | D_Tensor_MRCI_Heff_ES [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MRCI_Absorption_Spectrum [Absorption_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | MRCI_ECD_Spectrum [ECD_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | Nuclear_Gradient | Y | NAtoms | I | N | N |  |  |
    |  |  | gradNorm | D | N | N |  |  |
    |  |  | grad | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | CHELPG_Population_Analysis | Y | NAtoms | I | N | N |  |  |
    |  |  | ATNO | AI | N | N |  |  |
    |  |  | AtomicCharges | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | Hirshfeld_Population_Analysis | Y | NAtoms | I | N | N |  |  |
    |  |  | ATNO | AI | N | N |  |  |
    |  |  | DENSA | D | N | N | Total integrated alpha density |  |
    |  |  | DENSB | D | N | N | Total integrated beta density |  |
    |  |  | AtomicCharges | AD | N | N |  |  |
    |  |  | Spin | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | Loewdin_Population_Analysis | Y | NAtoms | I | N | N |  |  |
    |  |  | ATNO | AI | N | N |  |  |
    |  |  | AtomicCharges | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | Mayer_Population_Analysis | Y | NAtoms | I | N | N | Total number of atoms |  |
    |  |  | NBondOrdersPrint | I | N | N | The number of bond orders larger than threshold |  |
    |  |  | bondThresh | D | N | N | The threshold for printing |  |
    |  |  | components | AI | Y | N | The indices and atomic numbers of the bonding atoms |  |
    |  |  | BondOrders | AD | Y | N | The bond orders |  |
    |  |  | ATNO | AI | N | N | Atomic number of the elements |  |
    |  |  | NA | AD | N | N | Mulliken gross atomic population |  |
    |  |  | ZA | AD | N | N | Total nuclear charge |  |
    |  |  | QA | AD | N | N | Mulliken gross atomic charge |  |
    |  |  | VA | AD | N | N | Mayer’s total valence |  |
    |  |  | BVA | AD | N | N | Mayer’s bonded valence |  |
    |  |  | FA | AD | N | N | Mayer’s free valence |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MBIS_Population_Analysis | Y | NAtoms | I | N | N |  |  |
    |  |  | ATNO | AI | N | N |  |  |
    |  |  | Thresh | D | N | N |  |  |
    |  |  | Niter | I | N | N |  |  |
    |  |  | LargePrint | B | N | N |  |  |
    |  |  | DENSA | D | N | N | Total integrated alpha density |  |
    |  |  | DENSB | D | N | N | Total integrated beta density |  |
    |  |  | AtomicCharges | AD | N | N |  |  |
    |  |  | Spin | AD | N | N |  |  |
    |  |  | NPOPVAL | AD | N | N |  |  |
    |  |  | SIGMAVAL | AD | N | N |  |  |
    |  |  | AtomicDipole | AD | Y | N |  |  |
    |  |  | AtomicQuadrupole | AD | Y | N |  |  |
    |  |  | AtomicOctupole | AD | Y | N |  |  |
    |  |  | ThirdRadialMoment | AD | Y | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | Mulliken_Population_Analysis | Y | NAtoms | I | N | N |  |  |
    |  |  | ATNO | AI | N | N |  |  |
    |  |  | AtomicCharges | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | RASCI_Nuc_Gradient [Nuclear_Gradient] | Y | NAtoms | I | N | N |  |  |
    |  |  | gradNorm | D | N | N |  |  |
    |  |  | grad | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | RASCI_Dipole_Moment [Dipole_Moment] | Y | dipoleMagnitude | D | N | N |  | a.u. |
    |  |  | dipoleElecContrib | AD | N | N | Electronic contribution |  |
    |  |  | dipoleNucContrib | AD | N | N | Nuclear contribution |  |
    |  |  | dipoleTotal | AD | N | N | Total |  |
    |  |  | doAtomicDipole | B | N | N |  |  |
    |  |  | atomicDipole | AD | Y | N | Atomic dipoles (NAtoms * X,Y,Z) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | RASCI_EFG_Tensor [EFG_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | QFAC | D | N | Y | Prefactor |  |
    |  |  | V | AD | N | Y | Raw tensor |  |
    |  |  | VEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | VIso | D | N | Y |  |  |
    | RASCI_Polarizability [Polarizability] | Y | isotropicPolar | D | N | N |  |  |
    |  |  | rawCartesian | AD | N | N |  | a.u |
    |  |  | diagonalizedTensor | AD | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | doAtomicPolar | B | N | N |  |  |
    |  |  | atomicPolarIso | AD | Y | N | Atomic istotropic polarizabilities |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | RASCI_Quadrupole_Moment [Quadrupole_Moment] | Y | isotropicQuadMoment | D | N | N |  | a.u. |
    |  |  | quadElecContrib | AD | N | N | Electronic contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadNucContrib | AD | N | N | Nuclear contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadTotal | AD | N | N | Total. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadDiagonalized | AD | N | N | The diagonalized tensor | a.u. |
    |  |  | doAtomicQuad | B | N | N |  |  |
    |  |  | atomicQuad | AD | Y | N | Atomic quadrupoles (NAtoms * XX, YY, ZZ, XY, XZ, YZ) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | RASCI_A_Tensor [A_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elem | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | PFAC | D | N | Y | Prefactor PFAC=gegNbe*bN (in MHz) |  |
    |  |  | ARaw | AD | N | Y | Raw tensor |  |
    |  |  | AEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | AIso | D | N | Y |  |  |
    | RASCI_Chemical_Shift [Chemical_Shift] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | RASCI_D_Tensor [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | RASCI_G_Tensor [G_Tensor] | Y | g_matrix | AD | N | N |  |  |
    |  |  | g_elec | D | N | N | The free electron g-value contribution |  |
    |  |  | g_RMC | D | N | N | The reduced mass correction |  |
    |  |  | g_DSO | AD | N | N |  |  |
    |  |  | g_PSO | AD | N | N |  |  |
    |  |  | g_Tot | AD | N | N |  |  |
    |  |  | g_iso | D | N | N |  |  |
    |  |  | Delta_g | AD | N | N |  |  |
    |  |  | Delta_g_iso | D | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | RASCI_Spin_Spin_Coupling [Spin_Spin_Coupling] | Y | numOfNucPairs | I | N | N | Number of nuclei pairs to calculate |  |
    |  |  | numOfNucPairsDSO | I | N | N | number of nuclear pairs to calculate DSO |  |
    |  |  | numOfNucPairsPSO | I | N | N | number of nuclear pairs to calculate PSO |  |
    |  |  | numOfNucPairsFC | I | N | N | number of nuclear pairs to calculate FC |  |
    |  |  | numOfNucPairsSD | I | N | N | number of nuclear pairs to calculate SD |  |
    |  |  | numOfNucPairsSD_FC | I | N | N | number of nuclear pairs to calculate SD/FC |  |
    |  |  | pairsInfo | AI | N | N | Pairs Info: Col1->Index of A. Col2->Atom. Num. of A. Col3->Index of B. Col4->Atom. Num. of B. |  |
    |  |  | pairsDistances | AD | N | N | The distances of each pair |  |
    |  |  | pairsTotalSSCIso | AD | N | N | The Spin-Spin coupling constant for each pair |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | RASCI_Absorption_Spectrum [Absorption_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | RASCI_ECD_Spectrum [ECD_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | ROCIS_Energies | N | refEnergy | D | N | N |  |  |
    |  |  | corrEnergy | D | N | N |  |  |
    |  |  | totalEnergy | D | N | N |  |  |
    |  |  | numOfRoots | I | N | N |  |  |
    |  |  | Energies | AD | N | N | State energies in Hartree |  |
    |  |  | Multiplicities | AI | N | N |  |  |
    | ROCIS_Dipole_Moment [Dipole_Moment] | Y | dipoleMagnitude | D | N | N |  | a.u. |
    |  |  | dipoleElecContrib | AD | N | N | Electronic contribution |  |
    |  |  | dipoleNucContrib | AD | N | N | Nuclear contribution |  |
    |  |  | dipoleTotal | AD | N | N | Total |  |
    |  |  | doAtomicDipole | B | N | N |  |  |
    |  |  | atomicDipole | AD | Y | N | Atomic dipoles (NAtoms * X,Y,Z) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | ROCIS_EFG_Tensor [EFG_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | QFAC | D | N | Y | Prefactor |  |
    |  |  | V | AD | N | Y | Raw tensor |  |
    |  |  | VEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | VIso | D | N | Y |  |  |
    | ROCIS_Polarizability [Polarizability] | Y | isotropicPolar | D | N | N |  |  |
    |  |  | rawCartesian | AD | N | N |  | a.u |
    |  |  | diagonalizedTensor | AD | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | doAtomicPolar | B | N | N |  |  |
    |  |  | atomicPolarIso | AD | Y | N | Atomic istotropic polarizabilities |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | ROCIS_Quadrupole_Moment [Quadrupole_Moment] | Y | isotropicQuadMoment | D | N | N |  | a.u. |
    |  |  | quadElecContrib | AD | N | N | Electronic contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadNucContrib | AD | N | N | Nuclear contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadTotal | AD | N | N | Total. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadDiagonalized | AD | N | N | The diagonalized tensor | a.u. |
    |  |  | doAtomicQuad | B | N | N |  |  |
    |  |  | atomicQuad | AD | Y | N | Atomic quadrupoles (NAtoms * XX, YY, ZZ, XY, XZ, YZ) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | ROCIS_A_Tensor [A_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elem | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | PFAC | D | N | Y | Prefactor PFAC=gegNbe*bN (in MHz) |  |
    |  |  | ARaw | AD | N | Y | Raw tensor |  |
    |  |  | AEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | AIso | D | N | Y |  |  |
    | ROCIS_Chemical_Shift [Chemical_Shift] | Y | numOfNucs | I | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | SDSO | AD | N | Y | Diamagnetic contribution |  |
    |  |  | SPSO | AD | N | Y | Paramagnetic contribution |  |
    |  |  | STot | AD | N | Y | Total tensor |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | sTotEigen | AD | N | Y | Eigenvalues |  |
    |  |  | siso | D | N | Y |  |  |
    |  |  | saniso | D | N | Y |  |  |
    | ROCIS_D_Tensor [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | ROCIS_G_Tensor [G_Tensor] | Y | g_matrix | AD | N | N |  |  |
    |  |  | g_elec | D | N | N | The free electron g-value contribution |  |
    |  |  | g_RMC | D | N | N | The reduced mass correction |  |
    |  |  | g_DSO | AD | N | N |  |  |
    |  |  | g_PSO | AD | N | N |  |  |
    |  |  | g_Tot | AD | N | N |  |  |
    |  |  | g_iso | D | N | N |  |  |
    |  |  | Delta_g | AD | N | N |  |  |
    |  |  | Delta_g_iso | D | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | ROCIS_Spin_Spin_Coupling [Spin_Spin_Coupling] | Y | numOfNucPairs | I | N | N | Number of nuclei pairs to calculate |  |
    |  |  | numOfNucPairsDSO | I | N | N | number of nuclear pairs to calculate DSO |  |
    |  |  | numOfNucPairsPSO | I | N | N | number of nuclear pairs to calculate PSO |  |
    |  |  | numOfNucPairsFC | I | N | N | number of nuclear pairs to calculate FC |  |
    |  |  | numOfNucPairsSD | I | N | N | number of nuclear pairs to calculate SD |  |
    |  |  | numOfNucPairsSD_FC | I | N | N | number of nuclear pairs to calculate SD/FC |  |
    |  |  | pairsInfo | AI | N | N | Pairs Info: Col1->Index of A. Col2->Atom. Num. of A. Col3->Index of B. Col4->Atom. Num. of B. |  |
    |  |  | pairsDistances | AD | N | N | The distances of each pair |  |
    |  |  | pairsTotalSSCIso | AD | N | N | The Spin-Spin coupling constant for each pair |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | ROCIS_Absorption_Spectrum [Absorption_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | ROCIS_ECD_Spectrum [ECD_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | RPA_Dipole_Moment [Dipole_Moment] | Y | dipoleMagnitude | D | N | N |  | a.u. |
    |  |  | dipoleElecContrib | AD | N | N | Electronic contribution |  |
    |  |  | dipoleNucContrib | AD | N | N | Nuclear contribution |  |
    |  |  | dipoleTotal | AD | N | N | Total |  |
    |  |  | doAtomicDipole | B | N | N |  |  |
    |  |  | atomicDipole | AD | Y | N | Atomic dipoles (NAtoms * X,Y,Z) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | RPA_EFG_Tensor [EFG_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | QFAC | D | N | Y | Prefactor |  |
    |  |  | V | AD | N | Y | Raw tensor |  |
    |  |  | VEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | VIso | D | N | Y |  |  |
    | RPA_Polarizability [Polarizability] | Y | isotropicPolar | D | N | N |  |  |
    |  |  | rawCartesian | AD | N | N |  | a.u |
    |  |  | diagonalizedTensor | AD | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | doAtomicPolar | B | N | N |  |  |
    |  |  | atomicPolarIso | AD | Y | N | Atomic istotropic polarizabilities |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | RPA_Quadrupole_Moment [Quadrupole_Moment] | Y | isotropicQuadMoment | D | N | N |  | a.u. |
    |  |  | quadElecContrib | AD | N | N | Electronic contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadNucContrib | AD | N | N | Nuclear contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadTotal | AD | N | N | Total. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadDiagonalized | AD | N | N | The diagonalized tensor | a.u. |
    |  |  | doAtomicQuad | B | N | N |  |  |
    |  |  | atomicQuad | AD | Y | N | Atomic quadrupoles (NAtoms * XX, YY, ZZ, XY, XZ, YZ) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | RPA_A_Tensor [A_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elem | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | PFAC | D | N | Y | Prefactor PFAC=gegNbe*bN (in MHz) |  |
    |  |  | ARaw | AD | N | Y | Raw tensor |  |
    |  |  | AEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | AIso | D | N | Y |  |  |
    | RPA_Chemical_Shift [Chemical_Shift] | Y | numOfNucs | I | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | SDSO | AD | N | Y | Diamagnetic contribution |  |
    |  |  | SPSO | AD | N | Y | Paramagnetic contribution |  |
    |  |  | STot | AD | N | Y | Total tensor |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | sTotEigen | AD | N | Y | Eigenvalues |  |
    |  |  | siso | D | N | Y |  |  |
    |  |  | saniso | D | N | Y |  |  |
    | RPA_D_Tensor [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | RPA_G_Tensor [G_Tensor] | Y | g_matrix | AD | N | N |  |  |
    |  |  | g_elec | D | N | N | The free electron g-value contribution |  |
    |  |  | g_RMC | D | N | N | The reduced mass correction |  |
    |  |  | g_DSO | AD | N | N |  |  |
    |  |  | g_PSO | AD | N | N |  |  |
    |  |  | g_Tot | AD | N | N |  |  |
    |  |  | g_iso | D | N | N |  |  |
    |  |  | Delta_g | AD | N | N |  |  |
    |  |  | Delta_g_iso | D | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | RPA_Spin_Spin_Coupling [Spin_Spin_Coupling] | Y | numOfNucPairs | I | N | N | Number of nuclei pairs to calculate |  |
    |  |  | numOfNucPairsDSO | I | N | N | number of nuclear pairs to calculate DSO |  |
    |  |  | numOfNucPairsPSO | I | N | N | number of nuclear pairs to calculate PSO |  |
    |  |  | numOfNucPairsFC | I | N | N | number of nuclear pairs to calculate FC |  |
    |  |  | numOfNucPairsSD | I | N | N | number of nuclear pairs to calculate SD |  |
    |  |  | numOfNucPairsSD_FC | I | N | N | number of nuclear pairs to calculate SD/FC |  |
    |  |  | pairsInfo | AI | N | N | Pairs Info: Col1->Index of A. Col2->Atom. Num. of A. Col3->Index of B. Col4->Atom. Num. of B. |  |
    |  |  | pairsDistances | AD | N | N | The distances of each pair |  |
    |  |  | pairsTotalSSCIso | AD | N | N | The Spin-Spin coupling constant for each pair |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | RPA_Absorption_Spectrum [Absorption_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | RPA_ECD_Spectrum [ECD_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | Energy | Y | Method | S | N | N |  |  |
    |  |  | totalEnergy | AD | N | N | Total energy of each state |  |
    |  |  | Mult | AI | Y | N | Multiplicity of each state |  |
    |  |  | Irrep | AI | Y | N | Irreducible representation of each state |  |
    |  |  | RelCorr | S | Y | N | Relativistic correction (SOC and/or SSC) |  |
    |  |  | NBlocks | I | Y | N | Number of multiplicity blocks |  |
    |  |  | NRoots | AI | Y | N | Number of roots in each block |  |
    |  |  | NTotalRoots | I | Y | N | Total number of roots |  |
    |  |  | Block | AI | Y | N | Block index of each state |  |
    |  |  | Root | AI | Y | N | Root index within the block |  |
    |  |  | FollowIRoot | I | Y | N | Index of the followed root |  |
    |  |  | AvgMult | AD | Y | N | Average multiplicity of each SO-/SS-coupled state |  |
    | SCF_Energy [Energy] | Y | Method | S | N | N |  |  |
    |  |  | totalEnergy | AD | N | N | Total energy of each state |  |
    |  |  | Mult | AI | Y | N | Multiplicity of each state |  |
    |  |  | Irrep | AI | Y | N | Irreducible representation of each state |  |
    |  |  | RelCorr | S | Y | N | Relativistic correction (SOC and/or SSC) |  |
    |  |  | NBlocks | I | Y | N | Number of multiplicity blocks |  |
    |  |  | NRoots | AI | Y | N | Number of roots in each block |  |
    |  |  | NTotalRoots | I | Y | N | Total number of roots |  |
    |  |  | Block | AI | Y | N | Block index of each state |  |
    |  |  | Root | AI | Y | N | Root index within the block |  |
    |  |  | FollowIRoot | I | Y | N | Index of the followed root |  |
    |  |  | AvgMult | AD | Y | N | Average multiplicity of each SO-/SS-coupled state |  |
    | SCF_Nuc_Gradient [Nuclear_Gradient] | Y | NAtoms | I | N | N |  |  |
    |  |  | gradNorm | D | N | N |  |  |
    |  |  | grad | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | SCF_Dipole_Moment [Dipole_Moment] | Y | dipoleMagnitude | D | N | N |  | a.u. |
    |  |  | dipoleElecContrib | AD | N | N | Electronic contribution |  |
    |  |  | dipoleNucContrib | AD | N | N | Nuclear contribution |  |
    |  |  | dipoleTotal | AD | N | N | Total |  |
    |  |  | doAtomicDipole | B | N | N |  |  |
    |  |  | atomicDipole | AD | Y | N | Atomic dipoles (NAtoms * X,Y,Z) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | SCF_EFG_Tensor [EFG_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | QFAC | D | N | Y | Prefactor |  |
    |  |  | V | AD | N | Y | Raw tensor |  |
    |  |  | VEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | VIso | D | N | Y |  |  |
    | SCF_Polarizability [Polarizability] | Y | isotropicPolar | D | N | N |  |  |
    |  |  | rawCartesian | AD | N | N |  | a.u |
    |  |  | diagonalizedTensor | AD | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | doAtomicPolar | B | N | N |  |  |
    |  |  | atomicPolarIso | AD | Y | N | Atomic istotropic polarizabilities |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | SCF_Quadrupole_Moment [Quadrupole_Moment] | Y | isotropicQuadMoment | D | N | N |  | a.u. |
    |  |  | quadElecContrib | AD | N | N | Electronic contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadNucContrib | AD | N | N | Nuclear contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadTotal | AD | N | N | Total. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadDiagonalized | AD | N | N | The diagonalized tensor | a.u. |
    |  |  | doAtomicQuad | B | N | N |  |  |
    |  |  | atomicQuad | AD | Y | N | Atomic quadrupoles (NAtoms * XX, YY, ZZ, XY, XZ, YZ) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | SCF_A_Tensor [A_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elem | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | PFAC | D | N | Y | Prefactor PFAC=gegNbe*bN (in MHz) |  |
    |  |  | ARaw | AD | N | Y | Raw tensor |  |
    |  |  | AEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | AIso | D | N | Y |  |  |
    | SCF_Chemical_Shift [Chemical_Shift] | Y | numOfNucs | I | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | SDSO | AD | N | Y | Diamagnetic contribution |  |
    |  |  | SPSO | AD | N | Y | Paramagnetic contribution |  |
    |  |  | STot | AD | N | Y | Total tensor |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | sTotEigen | AD | N | Y | Eigenvalues |  |
    |  |  | siso | D | N | Y |  |  |
    |  |  | saniso | D | N | Y |  |  |
    | SCF_D_Tensor [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | SCF_G_Tensor [G_Tensor] | Y | g_matrix | AD | N | N |  |  |
    |  |  | g_elec | D | N | N | The free electron g-value contribution |  |
    |  |  | g_RMC | D | N | N | The reduced mass correction |  |
    |  |  | g_DSO | AD | N | N |  |  |
    |  |  | g_PSO | AD | N | N |  |  |
    |  |  | g_Tot | AD | N | N |  |  |
    |  |  | g_iso | D | N | N |  |  |
    |  |  | Delta_g | AD | N | N |  |  |
    |  |  | Delta_g_iso | D | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | SCF_Spin_Spin_Coupling [Spin_Spin_Coupling] | Y | numOfNucPairs | I | N | N | Number of nuclei pairs to calculate |  |
    |  |  | numOfNucPairsDSO | I | N | N | number of nuclear pairs to calculate DSO |  |
    |  |  | numOfNucPairsPSO | I | N | N | number of nuclear pairs to calculate PSO |  |
    |  |  | numOfNucPairsFC | I | N | N | number of nuclear pairs to calculate FC |  |
    |  |  | numOfNucPairsSD | I | N | N | number of nuclear pairs to calculate SD |  |
    |  |  | numOfNucPairsSD_FC | I | N | N | number of nuclear pairs to calculate SD/FC |  |
    |  |  | pairsInfo | AI | N | N | Pairs Info: Col1->Index of A. Col2->Atom. Num. of A. Col3->Index of B. Col4->Atom. Num. of B. |  |
    |  |  | pairsDistances | AD | N | N | The distances of each pair |  |
    |  |  | pairsTotalSSCIso | AD | N | N | The Spin-Spin coupling constant for each pair |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | SCF_Absorption_Spectrum [Absorption_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | SCF_ECD_Spectrum [ECD_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | SOC_Energy_Correction | N | total_SOC_energy | D | N | N |  |  |
    |  |  | total_non_SOC_energy | D | N | N |  |  |
    |  |  | nuclear_energy | D | N | N |  |  |
    |  |  | SOC_correction | D | N | N |  |  |
    | STEOM | N | S2 | AD | N | N | <S**2> |  |
    |  |  | PercentageActiveCharacter | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | excitationEnergies | AD | N | N | Total energy of each state |  |
    |  |  | Mult | AI | Y | N | Multiplicity of each state |  |
    |  |  | Irrep | AI | Y | N | Irreducible representation of each state |  |
    |  |  | RelCorr | S | Y | N | Relativistic correction (SOC and/or SSC) |  |
    |  |  | NBlocks | I | Y | N | Number of multiplicity blocks |  |
    |  |  | NRoots | AI | Y | N | Number of roots in each block |  |
    |  |  | NTotalRoots | I | Y | N | Total number of roots |  |
    |  |  | Block | AI | Y | N | Block index of each state |  |
    |  |  | Root | AI | Y | N | Root index within the block |  |
    |  |  | FollowIRoot | I | Y | N | Index of the followed root |  |
    |  |  | AvgMult | AD | Y | N | Average multiplicity of each SO-/SS-coupled state |  |
    | Absorption_Spectrum | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | ECD_Spectrum | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | THERMOCHEMISTRY_Energies | Y | temperature | D | N | N |  |  |
    |  |  | pressure | D | N | N |  |  |
    |  |  | totalMass | D | N | N |  |  |
    |  |  | spinDegeneracy | I | N | N |  |  |
    |  |  | elEnergy | D | N | N |  |  |
    |  |  | transEnergy | D | N | N |  |  |
    |  |  | rotEnergy | D | N | N |  |  |
    |  |  | vibEnergy | D | N | N |  |  |
    |  |  | numOfFreqs | I | N | N |  |  |
    |  |  | freqScalingFactor | D | N | N |  |  |
    |  |  | FREQ | AD | N | N |  | cm^-1 |
    |  |  | zpe | D | N | N |  |  |
    |  |  | innerEnergyU | D | N | N |  |  |
    |  |  | enthalpyH | D | N | N |  |  |
    |  |  | qEl | D | N | N |  |  |
    |  |  | qRot | D | N | N |  |  |
    |  |  | qVib | D | N | N |  |  |
    |  |  | qTrans | D | N | N |  |  |
    |  |  | entropyS | D | N | N |  |  |
    |  |  | freeEnergyG | D | N | N |  |  |
    |  |  | isLinear | B | N | N |  |  |
    | VdW_Correction | N | vdW | D | N | N |  |  |
    |  |  | vdW_atomic | AD | Y | N |  |  |
    | Calculation_Status | N | version | S | N | N |  |  |
    |  |  | progName | S | N | N |  |  |
    |  |  | Status | S | N | N |  |  |
    | MDCI_EOM_Energies | Y | groundRefEnergy | D | N | N | Ground State Reference Energy |  |
    |  |  | groundCorrEnergy | D | N | N | Ground State Correlation Energy |  |
    |  |  | groundTotalEnergy | D | N | N | Ground State Total MDCI Energy |  |
    | CASPT2_Dipole_Moment [Dipole_Moment] | Y | dipoleMagnitude | D | N | N |  | a.u. |
    |  |  | dipoleElecContrib | AD | N | N | Electronic contribution |  |
    |  |  | dipoleNucContrib | AD | N | N | Nuclear contribution |  |
    |  |  | dipoleTotal | AD | N | N | Total |  |
    |  |  | doAtomicDipole | B | N | N |  |  |
    |  |  | atomicDipole | AD | Y | N | Atomic dipoles (NAtoms * X,Y,Z) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | CAS_CUSTOM_Dipole_Moment [Dipole_Moment] | Y | dipoleMagnitude | D | N | N |  | a.u. |
    |  |  | dipoleElecContrib | AD | N | N | Electronic contribution |  |
    |  |  | dipoleNucContrib | AD | N | N | Nuclear contribution |  |
    |  |  | dipoleTotal | AD | N | N | Total |  |
    |  |  | doAtomicDipole | B | N | N |  |  |
    |  |  | atomicDipole | AD | Y | N | Atomic dipoles (NAtoms * X,Y,Z) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | CASPT2_G_Tensor [G_Tensor] | Y | g_matrix | AD | N | N |  |  |
    |  |  | g_elec | D | N | N | The free electron g-value contribution |  |
    |  |  | g_RMC | D | N | N | The reduced mass correction |  |
    |  |  | g_DSO | AD | N | N |  |  |
    |  |  | g_PSO | AD | N | N |  |  |
    |  |  | g_Tot | AD | N | N |  |  |
    |  |  | g_iso | D | N | N |  |  |
    |  |  | Delta_g | AD | N | N |  |  |
    |  |  | Delta_g_iso | D | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MDCI_LED | N | numOfFragments | I | N | N | The number of fragments |  |
    |  |  | sumNonDisStrong | D | N | N | Sum of non dispersive correlation strong pairs |  |
    |  |  | sumNonDisWeak | D | N | N | Sum of non dispersive correlation weak pairs |  |
    |  |  | electrostRef | AD | N | N | Electrostatics reference |  |
    |  |  | exchangeRef | AD | N | N | Exchange reference |  |
    |  |  | dispContr | AD | N | N | Strong pair dispersion contribution |  |
    |  |  | dispWeak | AD | N | N | Weak pair dispersion contribution |  |
    |  |  | refInt | AD | N | N | Interaction reference |  |
    |  |  | corrInt | AD | N | N | Interaction correlation |  |
    |  |  | totInt | AD | N | N | Interaction total |  |
    | Natural_Orbitals | N | NEL | I | N | N |  |  |
    |  |  | NSOMO | I | N | N |  |  |
    |  |  | NDOMO | I | N | N |  |  |
    |  |  | NVMO | I | N | N |  |  |
    |  |  | NNatoOrbs | I | N | N |  |  |
    |  |  | OccUno | AD | N | N | Occupation of natural orbitals |  |
    |  |  | OccUnso | AD | N | N | Occupation of spin natural orbitals |  |
    | Calculation_Timings | N | GTOINT | D | Y | N |  |  |
    |  |  | STOINT | D | Y | N |  |  |
    |  |  | SCF | D | Y | N |  |  |
    |  |  | SCFGRAD | D | Y | N |  |  |
    |  |  | GSTEP | D | Y | N |  |  |
    |  |  | PLOT | D | Y | N |  |  |
    |  |  | MOM | D | Y | N |  |  |
    |  |  | MP2 | D | Y | N |  |  |
    |  |  | CPSCF | D | Y | N |  |  |
    |  |  | LOC | D | Y | N |  |  |
    |  |  | CIS | D | Y | N |  |  |
    |  |  | MRCI | D | Y | N |  |  |
    |  |  | REL | D | Y | N |  |  |
    |  |  | SOC | D | Y | N |  |  |
    |  |  | EPRNMR | D | Y | N |  |  |
    |  |  | CASSCF | D | Y | N |  |  |
    |  |  | MDCI | D | Y | N |  |  |
    |  |  | CHELPG | D | Y | N |  |  |
    |  |  | ROCIS | D | Y | N |  |  |
    |  |  | MRCC | D | Y | N |  |  |
    |  |  | FCI | D | Y | N |  |  |
    |  |  | MD | D | Y | N |  |  |
    |  |  | FREQ | D | Y | N |  |  |
    |  |  | FREQ_NUM | D | Y | N |  |  |
    |  |  | COMPOUND | D | Y | N |  |  |
    |  |  | CIPSI | D | Y | N |  |  |
    |  |  | AUTOCI | D | Y | N |  |  |
    |  |  | ESD | D | Y | N |  |  |
    |  |  | DLPNOCC | D | Y | N |  |  |
    |  |  | MCRPA | D | Y | N |  |  |
    |  |  | NEB | D | Y | N |  |  |
    |  |  | CONFSC | D | Y | N |  |  |
    |  |  | ANMR | D | Y | N |  |  |
    |  |  | MM | D | Y | N |  |  |
    |  |  | MMGRAD | D | Y | N |  |  |
    |  |  | XTB | D | Y | N |  |  |
    |  |  | XTBGRAD | D | Y | N |  |  |
    |  |  | LFT | D | Y | N |  |  |
    |  |  | EXT | D | Y | N |  |  |
    |  |  | ONIOM_S | D | Y | N |  |  |
    |  |  | ONIOM_M | D | Y | N |  |  |
    |  |  | ONIOM_L | D | Y | N |  |  |
    |  |  | PROPINT | D | Y | N |  |  |
    |  |  | RESPONSE | D | Y | N |  |  |
    |  |  | PROP | D | Y | N |  |  |
    |  |  | CASRESP | D | Y | N |  |  |
    |  |  | MP2RESP | D | Y | N |  |  |
    |  |  | COSMORS | D | Y | N |  |  |
    |  |  | AUTOCIRESP | D | Y | N |  |  |
    |  |  | GOAT | D | Y | N |  |  |
    |  |  | CISRESP | D | Y | N |  |  |
    |  |  | EDA | D | Y | N |  |  |
    |  |  | SUM | D | Y | N |  |  |
    | SCF_Timings | N | TOTAL | D | Y | N |  |  |
    |  |  | PREP | D | Y | N |  |  |
    |  |  | GUESS | D | Y | N |  |  |
    |  |  | FOCK | D | Y | N |  |  |
    |  |  | DENS | D | Y | N |  |  |
    |  |  | DIAG | D | Y | N |  |  |
    |  |  | ETOT | D | Y | N |  |  |
    |  |  | POP | D | Y | N |  |  |
    |  |  | TRAFO | D | Y | N |  |  |
    |  |  | ORTHO | D | Y | N |  |  |
    |  |  | DIIS | D | Y | N |  |  |
    |  |  | SOSCF | D | Y | N |  |  |
    |  |  | NR | D | Y | N |  |  |
    |  |  | J | D | Y | N |  |  |
    |  |  | X | D | Y | N |  |  |
    |  |  | XC | D | Y | N |  |  |
    |  |  | GRID | D | Y | N |  |  |
    |  |  | FSYMMETR | D | Y | N |  |  |
    |  |  | PSYMMETR | D | Y | N |  |  |
    |  |  | FOCKSTART | D | Y | N |  |  |
    |  |  | SOLV | D | Y | N |  |  |
    |  |  | SOLV_INIT | D | Y | N |  |  |
    |  |  | SOLV_FINAL | D | Y | N |  |  |
    |  |  | INT_PREP | D | Y | N |  |  |
    |  |  | INT_PRESCREEN | D | Y | N |  |  |
    |  |  | INT_BF | D | Y | N |  |  |
    |  |  | INT_DENS | D | Y | N |  |  |
    |  |  | INT_DENSIO | D | Y | N |  |  |
    |  |  | INT_FUNC | D | Y | N |  |  |
    |  |  | INT_POT | D | Y | N |  |  |
    |  |  | INT_POTIO | D | Y | N |  |  |
    |  |  | INT_SUM | D | Y | N |  |  |
    |  |  | SPLITRIJ | D | Y | N |  |  |
    |  |  | COSX | D | Y | N |  |  |
    |  |  | COSX1C | D | Y | N |  |  |
    |  |  | RIJK | D | Y | N |  |  |
    |  |  | STABANA | D | Y | N |  |  |
    |  |  | DFET | D | Y | N |  |  |
    |  |  | ADFT_GUESS | D | Y | N |  |  |
    |  |  | ADFT_JDENS | D | Y | N |  |  |
    |  |  | ADFT_JMAT | D | Y | N |  |  |
    |  |  | ADFT_XDENS | D | Y | N |  |  |
    |  |  | ADFT_XMAT | D | Y | N |  |  |
    |  |  | ADFT_TMAT | D | Y | N |  |  |
    |  |  | ADFT_EQNSOLV | D | Y | N |  |  |
    |  |  | ECRISM | D | Y | N |  |  |
    |  |  | ECRISM_QESP | D | Y | N |  |  |
    |  |  | ECRISM_TOOL | D | Y | N |  |  |
    |  |  | ECRISM_FOCK | D | Y | N |  |  |
    |  |  | FROZCORE | D | Y | N |  |  |
    | Solvation_Details | N | Solvent | S | N | N |  |  |
    |  |  | Epsilon | D | N | N |  |  |
    |  |  | Refrac | D | N | N |  |  |
    |  |  | RSolv | D | N | N |  |  |
    |  |  | SurfaceType | S | N | N |  |  |
    |  |  | CPCMDielEnergy | D | N | N |  |  |
    |  |  | NPoints | I | N | N |  |  |
    |  |  | SurfaceArea | D | N | N |  |  |
    | Geometry | N | NAtoms | I | N | N |  |  |
    |  |  | NCorelessECP | I | N | N |  |  |
    |  |  | NGhostAtoms | I | N | N |  |  |
    |  |  | Coordinates | CC | N | N |  | Bohr |
    |  |  | ATNO | AI | N | N |  |  |
    |  |  | coreless_ECP | AI | Y | N | Non-zero for cECPs |  |
    |  |  | ghostAtoms | AI | Y | N | Non-zero for ghost atoms |  |
    |  |  | fragments | AI | Y | N | Fragment ID |  |
