(sec:essentialelements.coordinates)=
# 坐标的输入（Input of Coordinates）

坐标既可以直接在输入文件中指定，也可以从
外部文件读取，而且可以是笛卡尔坐标（"xyz"）或
内坐标（"Z-matrix"）格式。

## 从输入文件读取坐标（Reading coordinates from the input file）

在输入文件中指定坐标的最简单方式是包含
如下所示、由星号包围的块：

```orca
* CType Charge Multiplicity
...
coordinate specifications
...
*
```

这里 `CType` 可以是 `xyz`、`int`（或 `internal`）或 `gzmt` 之一，
分别对应笛卡尔坐标、内坐标以及
Gaussian Z-matrix 格式的内坐标。

使用 "`xyz`" 选项输入笛卡尔坐标
很直观。每一行由一个给定原子类型的标签
和三个指定该原子坐标的数组成。单位
可以是 Ångström（默认）或 Bohr。
这可以通过简单关键词 `!Angs` 或 `!Bohrs` 分别指定，
也可以通过下文所述 `%coords` 块中的 `Units` 变量指定。

```orca
* xyz Charge Multiplicity
Atom1   x1  y1  z1
Atom2   x2  y2  z2
 ...
*
```

例如，对于处于 $S=1/2$ 态（多重度 =
$2\times1/2+1=2$）的 CO$^+$

```orca
* xyz 1 2
C  0.0  0.0  0.0
O  0.0  0.0  1.1105
*
```

内坐标以大家熟悉的
"Z-matrix" 形式指定。Z-matrix 基本上包含关于分子
连接性、键长、键角和二面角的信息。然后程序
根据这些信息构建笛卡尔坐标。两组
坐标都会在输出中打印，以便于
格式之间的转换。这种情况下输入形如：

```orca
* int Charge Multiplicity
Atom1  0  0  0    0.0   0.0   0.0
Atom2  1  0  0    R1    0.0   0.0
Atom3  1  2  0    R2    A1    0.0
Atom4  1  2  3    R3    A2    D1
. . .
AtomN  NA NB NC   RN    AN    DN
*
```

"`internal`" 模式下的连接性规则如下：

-   `NA`：当前原子与之有距离（`RN`）的原子。

-   `NB`：当前原子与原子 `NA` 和 `NB` 构成键角（`AN`）。

-   `NC`：当前原子与原子 `NA`、
    `NB` 和 `NC` 构成二面角（`DN`）。这是沿 `NA-NB` 轴
    俯视时当前原子与原子
    `NC` 之间的夹角。

-   请注意，与 ORCA 的其他部分不同，这里原子从
    1 开始计数。

角度始终以度为单位给出！这些规则与著名的 MOPAC 和 ADF 程序中
使用的规则兼容。

最后，`gzmt` 以 Gaussian 程序所用的格式
指定内坐标。其形式如下：

```orca
* gzmt 0 1
    C
    O   1   4.454280
    Si  2   1.612138    1   56.446186
    O   3   1.652560    2   114.631525  1   -73.696925
    C   4   1.367361    3   123.895399  2   -110.635060
    ...
*
```

在输入文件中指定坐标的另一种方式是使用
`%coords` 块，其组织如下：

```orca
%coords
 CTyp   xyz     # the type of coordinates = xyz or internal
 Charge 0       # the total charge of the molecule
 Mult   2       # the multiplicity = 2S+1
 Units  Angs    # the unit of length = angs or bohrs

 # the subblock coords is for the actual coordinates
 # for CTyp=xyz
  coords
     Atom1   x1  y1  z1
     Atom2   x2  y2  z2
  end
 # for CTyp=internal
  coords
     Atom1  0  0  0    0.0   0.0   0.0
     Atom2  1  0  0    R1    0.0   0.0
     Atom3  1  2  0    R2    A1    0.0
     Atom4  1  2  3    R3    A2    D1
      . . .
     AtomN  NA NB NC   RN    AN    DN
  end
end
```

:::{important}
由于 ORCA 是基于 C++ 的程序，其内部计数从零开始。
因此所有电子、原子、频率、轨道、激发能等都从零开始计数。
而用户层面的计数，例如片段的编号，则从一开始计数。
:::

## 从外部文件读取坐标（Reading coordinates from external files）

也可以从外部文件读取坐标。最
常见的格式是 `.xyz` 文件，它原则上可以包含
多个结构（关于这一多 XYZ
功能，参见
{ref}`sec:structurereactivity.optimization.multiplexyz` 一节）：

```orca
* xyzfile Charge Multiplicity Filename
```

例如：

```orca
* xyzfile 1 2 mycoords.xyz
```

许多图形工具，如 Gabedit、molden 或 Jmol，都可以写出 Gaussian
Z-Matrix（`.gzmt`）。ORCA 也可以用
以下方式从外部文件读取它们

```orca
* gzmtfile 1 2 mycoords.gzmt
```

请注意，如果在同一输入文件中指定了多个作业，那么新
作业可以读取先前作业的坐标。如果没有在第四个参数中
给出文件名，则会自动使用
当前作业的名称。

```orca
... specification for the first job

$new_job
! keywords
* xyzfile 1 2
```

这样，优化和单点作业就可以非常方便地
组合在一个简单的输入文件中。示例见
以下各节。

:::{note}
本节中的关键词行在文件名之后必须以适合操作系统的行终止符序列结束
（即 Linux/MacOS 上的 `\n` 或 Windows 上的 `\r\n`），以避免解析错误。
:::

(sec:essentialelements.coordinates.special)=
## 特殊定义（Special definitions）

-   **虚拟原子（Dummy atoms）** 的定义方式与任何其他
    原子完全相同，使用 "DA"、"X" 或 "Xx" 作为原子符号。

-   **赝原子（Ghost atoms）** 通过在元素符号
    之后加上 ":" 来指定（参见
    {ref}`sec:essentialelements.counterpoise`）。

-   **点电荷（Point charges）** 用符号 "Q" 后跟
    电荷值来指定（参见
    {ref}`sec:essentialelements.coordinates.pointcharges`）。

-   **嵌入势（Embedding potentials）** 通过在
    元素符号之后加上 "\>" 来指定（参见
    {ref}`sec:essentialelements.basisset.embeddingpotentials`）。

-   **非标准（Non-standard）** 同位素或核电荷分别在
    原子坐标定义之后用语句 "`M = `..." 和 "`Z = `..." 指定。

    :::{NOTE}
    1. 核电荷可以取非整数值
    2. 当核电荷通过 "`Z = `..." 语句修改时，体系的总电荷仍应按未修改的电荷来计算。例如，对于一个
    `Z` 设为 1.5 的单氢原子的计算，应在
    输入文件的电荷和多重度部分输入电荷 0 和自旋多重度 2，尽管
    实际总电荷是 0.5。
    :::

-   **片段（Fragments）** 可以方便地通过在元素符号后的圆括号 "`(n)`" 中
    声明给定原子所属的片段编号来定义（参见
    {ref}`sec:essentialelements.fragmentation`）。

(sec:essentialelements.coordinates.parascan)=
## 定义几何参数与扫描势能面（Defining Geometry Parameters and Scanning Potential Energy Surfaces）

ORCA 允许你将所有原子的坐标定义为用户
定义的几何参数的函数。通过给这些参数指定的不是一个值而是一个
值的范围（或一系列值），就可以扫描势能
面。在这种情况下变量 `RunTyp` 会
自动改为 `Scan`。参数
指定的格式很简单：

```orca
%coords
 CTyp   internal
 Charge 0
 Mult   1
 pardef
  rCH  = 1.09;    # a C-H distance
  ACOH = 120.0;   # a C-O-H angle
  rCO  = 1.35, 1.10, 26; # a C-O distance that will be scanned
 end
 coords
    C  0  0  0   0     0         0
    O  1  0  0  {rCO}  0         0
    H  1  2  0  {rCH}  {ACOH}    0
    H  1  2  3  {rCH}  {ACOH}  180
 end
end
```

在上面的例子中，甲醛的几何结构以内坐标
定义（几何函数对笛卡尔坐标的
用法完全相同）。每个几何参数都可以通过将
表达式括在花括号 "`{} `" 中来赋值为
某个函数。例如，一个函数可以形如 `*cos(Theta)*rML+R`。请注意，所有
三角函数都要求其参数以度为单位而非
弧度。几何参数应定义为
长度以 Ångström 为单位、角度以度为单位。在求值函数*之后*，
坐标将被转换为原子
单位。在上面的例子中，变量 `rCO` 被定义为"扫描
参数"。其值将分 26 步从 1.3 Å 递减到 1.1
Å，在每个点上都会做一次单点计算。在运行结束时，
程序将汇总各点的总能量。
这些信息随后可以复制到图形
程序的电子表格中，从而绘制势能面。最多三个
参数可以作为扫描参数。这样就可以构建能量
（或性质）值随几何变化的网格或立方体。

如果你想把一个参数定义在一系列离散值上而不是
等间距的间隔上，则应使用如下语法：

```orca
%coords
 CTyp   internal
 Charge 0
 Mult   1
 pardef
  rCH = 1.09;   # a C-H distance
  ACOH= 120.0;  # a C-O-H angle
  rCO [1.3 1.25 1.22 1.20 1.18 1.15 1.10];  # a C-O distance that will be scanned
 end
 coords
    C  0  0  0   0     0         0
    O  1  0  0  {rCO}  0         0
    H  1  2  0  {rCH}  {ACOH}    0
    H  1  2  3  {rCH}  {ACOH}  180
 end
end
```

在这个例子中，C-O 距离以七个不等距的
步长变化。这可以用来在极小值或极大值附近
提供更多的点，而在势能面上不太重要的部分
用较少的点。

ORCA 中还实现了一个特殊功能——参数
本身可以作为其他参数的函数，如下面这个
（无实际意义的）例子所示：

```orca
%coords
 CTyp   internal
 Charge 0
 Mult   1
 pardef
  rCOHalf= 0.6;
  rCO    = { 2.0*rCOHalf };
 end
 coords
    C  0  0  0   0     0         0
    O  1  0  0  {rCO}  0         0
    O  1  0  0  {rCO}  180       0
 end
end
```

在这个例子中，参数 `rCO` 由参数
`rCOHalf` 计算得到。一般而言，（在假定为 `Scan`
计算时）几何结构按以下方式计算：
(a) 增加待
扫描参数的值，
(b) 求值为参数赋值的函数，
以及
(c) 求值为几何
变量赋值的函数。

虽然并非强制，但良好的做法是*首先*
定义静态参数或扫描参数，然后定义作为这些参数之函数
的参数。

最后，ORCA 还有一些可能有助于减少
表面扫描计算量的特殊功能：

```orca
%method
 SwitchToSOSCF true      # switches the converger to SOSCF
                         # after the first point. SOSCF may
                         # converge better than DIIS if the
                         # starting orbitals are good.
                         # default = false
 ReducePrint true        # reduce printout after the first point
                         # default=true

 # The initial guess can be changed after the first point.
 # The default is MORead. The MOs of the previous point will,
 # in many cases, be a very good guess for the next point.
 # However, in some cases you may want to be more conservative
 # and use a general guess.

 ScanGuess   OneElec    # the one-electron matrix
             Hueckel    # the extended Hueckel guess
             PAtom      # the PAtom guess
             PModel     # the PModel guess
             MORead     # MOs of the previous point
 end
```

:::{Note}

-   你可以使用 `NMScan`
     功能沿 Hessian 的简正模式进行扫描，如
     {ref}`sec:spectroscopyproperties.tddft.scan.normalModeScan` 一节所述。

-   表面扫描选项也支持与
     TD-DFT/CIS 或 MR-CI 计算结合使用（参见
     {ref}`sec:spectroscopyproperties.tddft.scan` 一节）。
:::

(sec:essentialelements.coordinates.mixed)=
## 混合使用内坐标与笛卡尔坐标（Mixing internal and Cartesian coordinates）

在某些情况下，将某些原子位置定义为
笛卡尔坐标、另一些定义为内坐标可能比较实用。这可以通过
在 `*int` 块中指定所有坐标来实现：使用 "0 0 0" 作为
参考原子即表示笛卡尔坐标。请注意，对于第一个
原子，标志为 "1 1 1"，因为 "0 0 0" 对内坐标
来说是正常的取值。例如，考虑
{ref}`sec:structurereactivity.optimization.relaxedsurface` 一节中的弛豫表面扫描，
其中甲基
先在一个任意的笛卡尔参考系中给出，然后
水分子以内坐标指定：

```{literalinclude} ../../orca_working_input/mixed_coords.inp
:language: orca
```

因此内坐标和笛卡尔坐标可以按任意顺序混合使用，但
建议前 3 个原子以笛卡尔坐标
指定，以定义一个唯一的参考系。

(sec:essentialelements.coordinates.pointcharges)=
## 点电荷的引入（Inclusion of Point Charges）

在某些情况下，需要在体系中加入点电荷。
在 ORCA 中有两种加入点电荷的机制。如果你只想
添加少数几个点电荷，可以像下面这个
（无实际意义的）输入那样把它们"伪装"为原子：

```{literalinclude} ../../orca_working_input/C06S01_248.inp
:language: orca
```

这里 "Q" 将这些原子定义为点电荷。接下来的四个数字
是点电荷的大小及其位置。然后程序将
把这些点电荷当作没有基函数、
核电荷等于 "Q" 值的原子来处理。

如果你要处理成千上万个点电荷，例如在 QM/MM
计算中，那么从外部文件读取
点电荷更为方便，实际上也是必须的，如下面的例子所示：

```{literalinclude} ../../orca_working_input/C06S01_249.inp
:language: orca
```

程序现在将读取包含
点电荷信息的文件 "`pointcharges.pc`"，然后调用模块 `orca_pc`，该模块将
点电荷贡献加入单电子矩阵和核
排斥能。文件 "`pointcharges.pc`" 是一个简单的 ASCII 文件，格式
如下：

```orca
3
 -0.834  -1.3130    0.0000   -0.0310
  0.417  -1.8700    0.7570    0.1651
  0.417  -1.8700   -0.7570    0.1651
```

第一行给出点电荷的数目。随后每一行
给出点电荷的大小（以原子单位）及其
位置（以 Ångström 为单位！）。不过应当注意，ORCA
对外部文件中的点电荷的处理与 "Q" 原子不同。
当使用外部点电荷文件时，点电荷之间的
相互作用不计入核能量。这一行为
源于 QM/MM，其中点电荷之间的相互作用由
MM 程序完成。这些程序在生成 ORCA 输入时通常使用外部点
电荷文件。要把点电荷之间的相互作用加到核能量中，
可在简单输入或 `%method` 块中使用 `DoEQ` 关键词，如下所示。

```orca
# A non QM/MM pointcharge calculation
! DoEQ

%pointcharges "pointcharges.pc"

%method
   DoEQ true
end
```

:::{warning}
`DoEQ` 关键词对半经验计算（例如 AM1）没有作用！
:::
