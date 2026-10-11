```{index} Molecular Dynamics (MD), AIMD
```

(sec:moldyn)=
# *从头算*分子动力学（*Ab initio* Molecular Dynamics）

几年前，我们在 ORCA 中加入了一个*从头算*分子动力学（*ab initio* molecular dynamics，AIMD）模块。[^1] 由于已经实现了大量具有解析梯度的不同电子结构方法，所有这些方法现在也都可用于 MD 模拟，提供了范围广泛的精度/性能权衡。

尽管在 ORCA 包内的历史相对较短，MD 模块在过去几年中已有相当大的发展。其他 MD 代码中的一些特性仍有所缺失。在未来版本中，程序的这一部分（希望）会加入更多新特性和方法。我们将始终尽最大努力保持严格的向后兼容性，使本节中的示例输入在未来所有版本中仍然有效。

关于 ORCA MD 模块的更多信息以及输入示例，请访问

[https://brehm-research.de/orcamd](https://brehm-research.de/orcamd)

(moldyn:changes)=
## ORCA 5.0 中的变更（Changes in ORCA 5.0）

-   添加了具有许多特性和选项的 [`Metadynamics`](#moldyn:sec_metadynamics)（元动力学）模块：

    -   可进行一维和二维元动力学模拟 {cite}`laio2002`，以探索沿反应坐标（称为集合变量（collective variables，"Colvars"））的自由能剖面。

    -   [`Colvars`](#moldyn:cmd_manage_colvar) 可以是距离*（包括投影到矢量和平面上）*、键角、二面角和配位数 {cite}`ianuzzi2003`。后者允许，*例如*，准确计算弱酸的 p$K_{\mathrm{A}}$ 值 {cite}`tummanapelli2014,tummanapelli2015`。

    -   对所有 Colvars，都可以使用原子组*（例如质心）*代替单个原子。

    -   元动力学模拟可以轻松重启并拆分到多次运行中。

    -   能够运行良温（well-tempered）元动力学 {cite}`barducci2008`，得到平滑收敛的自由能剖面。

    -   能够运行扩展拉格朗日元动力学（extended Langrangian Metadynamics）{cite}`ianuzzi2003`，其中偏置剖面上的一个虚拟粒子通过弹簧与真实体系耦合。虚拟粒子可以被恒温。

-   添加了两个现代而强大的[`恒温器`](#moldyn:cmd_thermostat)*（均可作为全局和 massive 使用）*：
 
    -   广泛使用的 Nosé–Hoover 链恒温器（NHC），带高阶 Yoshida 积分器 {cite}`martyna1992,martyna1996`；可对正则系综进行非常准确的采样。

    -   随机的"通过速度缩放的正则采样"（Canonical Sampling through Velocity Rescaling，CSVR）恒温器 {cite}`bussi2007`，最近相当流行。

-   可为所有 Colvars*（距离、键角、二面角、配位数）*定义谐和高斯[`约束（restraints）`](#moldyn:cmd_restraint)。这允许伞形采样（umbrella sampling）{cite}`kumar1992,kaestner2006` 等方法。也可以定义单侧约束，作为下壁或上壁。

-   现在可以打印[`约束（constraints）`](#moldyn:cmd_constraint)和[`约束（restraints）`](#moldyn:cmd_restraint)上的瞬时和平均力；这允许热力学积分 {cite}`kaestner2006`。

-   [`约束（constraints）`](#moldyn:cmd_constraint)和[`约束（restraints）`](#moldyn:cmd_restraint)的目标值现在可以是一个斜坡（ramp），使其能在模拟期间线性变化。

-   现在可以在 MD 运行期间保持体系质心固定。

-   现在可以在每个 MD 步按请求打印布居分析、轨道能量和 .engrad 文件。

## ORCA 4.2 中的变更（Changes in ORCA 4.2，2019 年 8 月）

-   向 MD 模块添加了基于 L-BFGS 和模拟退火的笛卡尔极小化命令。适用于大体系（$>10\,000$ 个原子）以及带约束的情况。提供一个标志以只优化氢原子位置*（用于晶体结构精修）*。见 [`Minimize`](#moldyn:cmd_minimize) 命令。

-   MD 模块现在可以以 DCD 文件格式写轨迹*（除已实现的 XYZ 和 PDB 格式之外）*，见 [`Dump`](#moldyn:cmd_dump) 命令。

-   [`恒温器`](#moldyn:cmd_thermostat)现在能够在模拟运行期间施加温度斜坡。

-   对区域定义增加了更多灵活性*（现在可以向现有区域添加/删除原子）*。将 `Define_Region` 命令重命名为 [`Manage_Region`](#moldyn:cmd_manage_region)。

-   添加了两种新的约束类型，保持质心固定或将完整原子组保持为刚性，见 [`Constraint`](#moldyn:cmd_constraint) 命令。

-   能够在 MD 运行期间每 $n$ 步存储 GBW 文件*（例如用于沿轨迹绘制轨道）*，见 [`Dump`](#moldyn:cmd_dump) 命令。

-   现在可以设置 MD 步中任何原子最大位移的限制，这可以用较差的初始结构稳定动力学。运行可以通过"`touch EXIT`"干净地中止。见 [`Run`](#moldyn:cmd_run) 命令。

-   在 MD 运行期间更好地处理/报告未收敛的 SCF。

-   修复了一个在许多步后使分子动力学变慢的问题。

-   Stefan Grimme 的 xTB 方法现在可用于 MD 模块，允许对大体系进行快速模拟。

## ORCA 4.1 中的变更（Changes in ORCA 4.1，2018 年 12 月）

-   分子动力学模拟现在可以使用笛卡尔、距离、键角和二面角约束。这些通过 [`Constraint`](#moldyn:cmd_constraint) 命令管理。

-   MD 模块现在具备多种几何形状的盒子（立方、正交、平行六面体、球、椭球），可帮助将体系保持在明确定义的体积内。盒子具有排斥谐势壁。

-   盒子可以定义为弹性的，使其尺寸适应体系。这使得可以在恒压下运行模拟。

-   轨迹现在可以以 XYZ 和 PDB 文件格式写入。

-   每个模拟步都会写一个重启文件。用该文件，可以重启模拟以无缝继续（对批处理运行或作业崩溃时有用）。重启通过 [`Restart`](#moldyn:cmd_restart) 命令处理；见下文。

-   引入了区域（*即*原子子集），可以单独定义。区域可用于将体系的不同部分恒温到不同温度（*例如*热溶剂中的冷溶质），或写选定原子的子集轨迹。

-   模拟的能量漂移现在在每一步显示（单位为开尔文每原子）。大的能量漂移可能由 SCF 收敛差或时间步长选择过大引起。

-   MD 输入中的物理单位现在通过下划线与其数值连接，如 `350_pm`。数值和单位之间的空格不再可接受。这略微破坏了向后兼容性——抱歉。

-   修复了运动方程时间积分中的一个 bug，该 bug 损害了能量守恒。

-   修复了使用半经验和 ECP 时的崩溃。现在可以用 PM3 等方法和 ECP 运行 MD 模拟。

(moldyn:input)=
## 输入格式（Input Format）

分子动力学模块通过在简单输入行中指定"`MD`"激活。描述模拟的实际 MD 输入在输入文件中稍后位置的"`%md`"节中。该节的内容随后被称为"MD 输入"。

```orcainput
! MD BLYP D3 def2-SVP
%md
  Timestep 0.5_fs # This is a comment
  Initvel 350_K
  Thermostat NHC 350_K Timecon 10.0_fs
  Dump Position Stride 1 Filename "trajectory.xyz"
  Run 200
end
* xyz 0 1
O         -4.54021        0.78439        0.09307
H         -3.64059        0.38224       -0.01432
H         -4.63463        1.39665       -0.67880
*
```

请注意，MD 输入不是由 ORCA 的主解析器处理，而是由 MD 模块中专门的解析器处理。因此，MD 输入不需要遵守一般的 ORCA 语法规则。其语法将在下文描述。

与一般 ORCA 输入不同，MD 输入不是基于关键词，而是基于*命令*，从顶部开始逐行连续执行（例如就像 shell 脚本中那样）。这意味着可以给出带有不同参数的相同命令，在解释器到达相应行时生效。这使得可以在单个输入文件中执行多次模拟（*例如*预平衡和生产运行）：

```orca
%md
  Timestep 1.0_fs
  Run 200
  Timestep 2.0_fs
  Run 500
end
```

向 MD 输入添加变量定义、循环和条件分支的工作已在进行中。[^2] 这将带来更大的灵活性（*例如*运行模拟直到某个量收敛）。MD 输入用 SANscript 语言（"Scientific Algorithm Notation Script"，科学算法记号脚本）编写，正在开发中。初步了解可在以下地址找到

[https://brehm-research.de/sanscript](https://brehm-research.de/sanscript)

与标准 ORCA 输入一样，MD 输入中的**注释**由"`#`"号开始，延续到当前行末。命令可以在行首和一个命令之后开始。"`#`"**不**被视为注释开始的唯一位置是在字符串字面量内部（*例如*在文件名中）。

```orca
%md
  # Comment
  Timestep 0.5_fs # Comment
  Dump Position Filename "trajectory#1.xyz"
end
```


::: samepage
更多 MD 输入语法规则：

-   MD 输入一般**不**区分大小写。唯一例外是大小写敏感文件系统（如 GNU Linux）上的文件名。

-   允许空行。

-   命令和选项由空格或制表符分隔。这些字符的任意组合都可用作分隔符。

-   DOS 和 UNIX 换行风格都可接受。
:::

### 命令（Commands）

如上所述，MD 输入的核心项是命令。每个输入行包含（最多）一个命令，这些命令按给定顺序执行。命令通常带有一个或多个参数，给出在命令名之后，由空白、制表符或逗号（可选）分隔。命令参数的顺序是固定的（见 {ref}`moldyn:commands` 一节中的命令列表）。命令可以有可选参数，它们总是指定在参数列表的末尾，在最后一个非可选参数之后。如果一个命令有多个可选参数，不必全部指定；但它们需要按正确顺序指定且无间隙：

```orca
%md
  Command Arg1 Arg2 Arg3                  # fine
  Command Arg1, Arg2, Arg3                # fine
  Command Arg1 Arg2 Arg3 Optarg1          # fine
  Command Arg1 Arg2 Arg3 Optarg1 Optarg2  # fine
  Command Arg1 Arg2 Arg3 Optarg2          # will not work
end
```

除参数和可选参数外，命令还可以有*修饰符（modifiers）*。它们可被视为"子命令"，修改给定命令，并可能拥有自己的参数列表。修饰符一般跟在所有非可选和可选参数之后，它们本身**不**得拥有可选参数。如果一个命令有多个修饰符，它们给出的顺序并不重要。

在下面的输入示例中，"`Mod1`"和"`Mod2`"是"`Command`"的修饰符。"`Mod1`"带一个参数，"`Mod2`"不带参数：

```orca
%md
  Command Arg1                            # fine
  Command Arg1 Optarg1                    # fine
  Command Arg1 Mod1 Modarg1 Mod2          # fine
  Command Arg1 Mod2                       # fine
  Command Arg1 Mod2 Mod1 Modarg1          # fine
  Command Arg1 Optarg1 Mod1 Modarg1 Mod2  # fine
end
```

为使这个抽象定义更具体些，请再看本节开头输入示例中的一行：

```orca
%md
  Dump Position Stride 1 Filename "trajectory.xyz"
end
```

这里 "`Dump`" 是命令，带一个非可选参数指定要转储哪个量——本例中是 "`Position`"。"`Dump`" 命令有两个修饰符，即 "`Stride`" 和 "`Filename`"。前者带一个整数参数，后者带一个字符串参数。交换这两个修饰符（当然连同它们各自的参数）不会改变行为。

(moldyn:sec_separating)=
### 分隔参数（Separating Arguments）

如上所示，传递给命令的参数不需要用逗号分隔。不过，使用逗号是允许的（也是推荐的）。首先，它能增加输入文件的可读性。其次，存在一些有歧义的情况，应用逗号（或括号）来澄清意图。其中之一是算术减号运算符。它既可用作二元运算符（从一个数减去另一个数），也可用作一元运算符（返回一个数的负值）。默认情况下，减号运算符被视为二元运算符（若可能）。

考虑你想给命令传递两个整数参数 "`10`" 和 "`-10`" 的情况。没有逗号（或括号）时，减号被误当作二元运算符，只有一个参数会被传递给命令：

```orca
Command 10 -10    #  Pitfall: treated as "Command (10 - 10)", i.e., "Command 0"
Command 10, -10   #  Two arguments, as intended
Command 10 (-10)  #  Also works
```

### 物理单位（Physical Units）

在许多情况下，需要在输入文件中指定带物理单位的量（*例如*温度、时间步长等）。对许多量，有不同广泛使用的单位，这总导致一些混乱（想想"kcal 与 kJ"的情形）。ORCA 通过为每个量定义默认单位并要求所有量以默认单位给出，来处理这个问题。ORCA 的默认单位是原子单位，在量子化学界大量使用，但在分子动力学界用得不多。由于*从头算*分子动力学模块存在于两个界的小重叠区域，可能会出现一些"单位冲突"。为从一开始就防止这些，在 ORCA 的 MD 输入中允许指定个人偏好的单位。

幸运的是，这像听起来一样简单方便。MD 模块的解析器检查数值常量后是否给出单位，并自动将该常量转换为内部默认单位。若未给出显式单位，则假定为默认单位。请注意，MD 模块内的默认单位不一定是原子单位（见下表）。单位通过下划线与前面的数值连接：


```orca
%md
  Timestep  1.0_fs
  Timestep 41.3_au # identical
  Timestep  1.0    # identical, as default time unit in MD module is fs
end
```

下文列出 MD 模块解析器当前已知的所有单位，按物理量排序。每个量的默认单位以 **`粗体`** 印出。加性常数和因子用于将一个单位转换为默认单位。加性常数在因子之前施加。"$-$"表示不施加常数/因子。未来可能会添加更多单位。

| **单位符号**           | **加性常数** | **因子** |
|:--------------------------|:---------------------:|:----------:|
| --- 长度单位 ---      |                       |            |
| **`Angstrom`**            |          $-$          |    $-$     |
| `A`                       |          $-$          |    $-$     |
| `Bohr`                    |          $-$          |   0.5291   |
| `pm`                      |          $-$          |    0.01    |
| `nm`                      |          $-$          |    10.0    |
| --- 时间单位 ---        |                       |            |
| **`fs`**                  |          $-$          |    $-$     |
| `ps`                      |          $-$          |    1000    |
| `au`                      |          $-$          |  0.02419   |
| --- 温度单位 --- |                       |            |
| **`Kelvin`**              |          $-$          |    $-$     |
| `K`                       |          $-$          |    $-$     |
| `Celsius`                 |        273.15         |    $-$     |
| `C`                       |        273.15         |    $-$     |
| --- 角度单位 ---       |                       |            |
| **`Deg`**                 |          $-$          |    $-$     |
| `Rad`                     |          $-$          | $180/\pi$  |


(moldyn:sec.functions)=
## 特性讨论（Discussion of Features）

(moldyn:sec_restart)=
### 重启模拟（Restarting Simulations）

*从头算*分子动力学模拟计算量昂贵，即使对中等大小的体系通常也会运行很长时间。通常希望将此类模拟作为多次短运行的组合来执行（*例如*若集群的排队系统施加最大作业时间）。ORCA MD 模块在每个模拟步写一个重启文件，允许模拟的无缝继续。该重启文件名为 "`basename.mdrestart`"，其中 `basename` 是项目的基本名。要加载现有的重启文件，使用 [`Restart`](#moldyn:cmd_restart) 命令*（见下面的命令列表）*。

在计划运行序列的第一次运行中，还没有重启文件。对这种情况，[`Restart`](#moldyn:cmd_restart) 命令提供了 `IfExists` 修饰符。重启文件仅在存在时才加载。若不存在，则简单跳过重启，不抛出错误。使用此修饰符，你可以在序列的第一次运行中（开始时不存在重启文件）就已放好 [`Restart`](#moldyn:cmd_restart) 命令，且不需要在第一次运行完成后修改输入。

关于 [`Dump`](#moldyn:cmd_dump) 命令，值得知道轨迹文件默认是追加（*不是*覆盖）的。如果你想用 [`Dump`](#moldyn:cmd_dump) 命令覆盖现有的轨迹文件，使用 `Replace` 修饰符。

请注意，执行 [`Restart`](#moldyn:cmd_restart) 命令时**只**重启位置、速度、恒温器内部状态*（仅对 NHC）*、元动力学山丘和时间步计数器。所有其他性质（恒温器、区域、轨迹转储、约束、盒子等）**不**会被重启。它们都应保留在输入文件中，作为序列第一次运行中执行的那样。只需在所有其他相关命令执行之后、[`Run`](#moldyn:cmd_run) 命令之前，添加 [`Restart`](#moldyn:cmd_restart) 命令。

作为本讨论的结束，给出一个简短示例。如果 MD 输入文件

```orca
%md
  Timestep 0.5_fs
  Initvel 300_K
  Thermostat NHC 300_K Timecon 10.0_fs
  Dump Position Stride 1 Filename "trajectory.xyz"
  Restart IfExists
  Run 100
end
```

随后被执行十次（不作任何修改），所得轨迹文件将与执行一次以下输入所得的*（除数值噪声外）*完全相同：

```orca
%md
  Timestep 0.5_fs
  Initvel 300_K
  Thermostat NHC 300_K Timecon 10.0_fs
  Dump Position Stride 1 Filename "trajectory.xyz"
  Run 1000
end
```

(moldyn:sec_regions)=
### 区域（Regions）

在 ORCA MD 模块中，可以定义**区域（regions）**。这一概念*不*指空间中的区域，而是体系中原子的子集。区域不过是一个原子列表。区域可以重叠，*即*原子可以同时属于多于一个区域。属于某区域的原子保持不变，直到区域被手动重新定义，*即*区域是固定的，不适应体系的任何变化。存在一些有名字的预定义区域。与之相对，用户定义的区域只带一个整数标识符。以下区域在任何情况下都是预定义的：

-   `all`：包含体系的所有原子。如果某些命令中未指定区域，这就是默认值，所以默认情况下这些命令总是作用于整个体系。

-   `active`：该区域包含所有可移动的（"非冻结"）原子。默认情况下，它与 `all` 区域相同。该区域内的原子在分子动力学运行中由时间积分更新，在极小化中被位移，并被计入动能的计算。

-   `inactive`：该区域包含所有*不*属于 `active` 区域的原子。这些原子是"冻结的"；它们被时间积分/极小化忽略，也不计入动能的计算。它们只是保持在初始位置。这在原则上等同于对这些原子施加笛卡尔约束；但要快得多。由于约束必须迭代求解*（见下文）*，若施加到数千个原子上，笛卡尔约束在计算上会相当昂贵。

从这三个预定义区域中，只有 `active` 区域可以手动修改。`active` 区域组成的改变会自动修改 `inactive` 区域。`all` 区域显然不能更改。

在 QM/MM 模拟的情况下，可以使用以下四个附加区域：

-   `qm`：这是"量子力学"区域——它包含所有由电子结构方法处理的原子。

-   `mm`：这是"分子力学"区域——它包含所有由力场方法处理的原子。它恰好包含那些不属于 `qm` 区域的原子。

-   `active_qm`：恰好包含那些同时属于 `qm` 和 `active` 区域的原子。

-   `active_mm`：恰好包含那些同时属于 `mm` 和 `active` 区域的原子。

这些区域**不能**在 MD 输入中修改。MD 模块只从 QM/MM 模块读取区域定义，但不能在此做任何更改。

区域对许多目的都很有用。例如，通过定义 `active` 区域使其只包含非壁原子，可以在体系周围构建"真实的"原子壁。壁原子随后将被冻结。除此之外，区域的轨迹可以写入磁盘，只含模拟中"有趣"的部分。此外，速度初始化可以施加到区域上，使模拟可以以不同原子组具有不同初始温度开始。恒温器可以附加到区域上，在整个模拟期间将不同原子组保持在不同温度。这允许复杂的模拟设置（热溶剂中的冷溶质、贯穿体系的温度梯度等）。

区域通过 [`Manage_Region`](#moldyn:cmd_manage_region) 命令定义或修改。许多其他命令把区域作为可选参数。请见下面的命令列表。

(moldyn:sec_metadynamics)=
### 元动力学（Metadynamics）

元动力学是基于分子动力学模拟分析反应及其他过程*（溶剂化、聚集、构象变化、解离）*自由能剖面的强大工具。它由 Laio 和 Parrinello 于 2002 年开发 {cite}`laio2002`。原则上，在 MD 模拟中观察到某过程的频率与该过程的自由能垒直接相关。然而，许多有趣的过程*（如化学反应）*具有如此高的自由能垒，以至于它们在 AIMD 模拟典型的时间尺度（100 ps）上永远不会发生。为提高此类过程发生的频率，可以采用所谓的稀有事件采样方法。元动力学是其中之一。它通过将偏置势构建为高斯山丘之和来工作，使自由能极小值被慢慢填满，体系逐渐被推离其静止点。

请注意，还有一种同名的方法用于探索构象空间，由 Grimme 于 2019 年发表 {cite}`grimme2019`。它原则上基于原始的"Parrinello"元动力学，但有若干修改和扩展。ORCA MD 模块包含原始 Parrinello 变体的元动力学 {cite}`laio2002`，以及若干扩展如良温元动力学 {cite}`barducci2008` 和扩展拉格朗日元动力学 {cite}`ianuzzi2003`。Grimme 的构象搜索方法将来可能会实现。

在元动力学中，必须定义一个或多个"集合变量"（Colvars），沿其采样体系的自由能剖面。Colvar 原则上不过是所有原子位置的连续函数，返回一个实数。Colvar 的一个简单例子是两个原子之间的距离，可用于探索成键或断键的自由能剖面。在 ORCA MD 模块中，Colvars 可通过 [`Manage_Colvar`](#moldyn:cmd_manage_colvar) 命令定义。可用的 Colvar 类型有距离*（包括投影到线或平面上）*、键角、二面角和配位数 {cite}`ianuzzi2003`。后者允许，*例如*，通过元动力学准确计算溶剂中弱酸的 p$K_{\mathrm{A}}$ 值 {cite}`tummanapelli2014,tummanapelli2015`。对于距离、键角和二面角，可以指定原子组代替单个原子，以便，*例如*，定义两个分子质心之间的距离作为 Colvar。

基于一或两个 Colvars（ORCA 支持一维和二维元动力学），可以设置元动力学模拟。有许多参数可选，描述见 [`Metadynamics`](#moldyn:cmd_metadynamics) 命令一节。设置完所有参数后，实际模拟简单地通过 [`Run`](#moldyn:cmd_run) 命令启动。也可以重启元动力学模拟，使其可以拆分为多次连续运行；见 [`Restart`](#moldyn:cmd_restart) 命令。二维良温扩展拉格朗日元动力学模拟的完整示例可在[下文](#moldyn:sec.metadyn.example)找到。

注意元动力学模拟通常需要非常多的计算时间*（粗略收敛的结果至少需要数万 MD 步，取决于 Colvar 的选择）*。所以这绝不是"稍微试试"的方法。然而，对于预测自由能剖面没有更便宜的方法*（除谐振子等非常简单的近似外）*，计算自由能剖面的预测能力是有代价的。

(moldyn:commands)=
## 命令列表（Command List）

在 {numref}`tab:moldyn:commands.overview` 中，
给出 MD 模块当前已知所有命令的字母顺序列表。每个命令的描述以一个小框开始，包含命令的名称以及参数和修饰符的表格。表格的倒数第二列指定每个参数的类型。可能的类型是"Integer"、"Real"、"String"和"Keyword"。对后者，最后一列包含 { `braces` } 中允许的关键词值列表。若类型为"Real"且是带单位的物理量，该量在最后一列以 \[方括号\] 给出。每个这样的框后跟相应命令的文字描述。

(tab:moldyn:commands.overview)=
:::{table} `%md` 块中命令的概览
| 命令                                       | 说明                                  |
|:----------------------------------------------|:---------------------------------------------|
| [`Cell`](#moldyn:cmd_cell)                    | 定义和修改盒子                   |
| [`Constraint`](#moldyn:cmd_constraint)        | 管理约束                          |
| [`Dump`](#moldyn:cmd_dump)                    | 控制轨迹输出                   |
| [`Initvel`](#moldyn:cmd_initvel)              | 随机初始化原子速度         |
| [`Manage_Colvar`](#moldyn:cmd_manage_colvar)  | 管理集合变量（"Colvars"）     |
| [`Manage_Region`](#moldyn:cmd_manage_region)  | 管理区域                              |
| [`Metadynamics`](#moldyn:cmd_metadynamics)    | 设置元动力学运行的参数        |
| [`Minimize`](#moldyn:cmd_minimize)            | 执行笛卡尔能量极小化     |
| [`PrintLevel`](#moldyn:cmd_printlevel)        | 控制输出详细程度                |
| [`Randomize`](#moldyn:cmd_randomize)          | 设置随机种子                         |
| [`Restart`](#moldyn:cmd_restart)              | 重启模拟以无缝继续 |
| [`Restraint`](#moldyn:cmd_restraint)          | 管理对 Colvars 的约束                |
| [`Run`](#moldyn:cmd_run)                      | 执行分子动力学运行            |
| [`SCFLog`](#moldyn:cmd_scflog)                | 控制 ORCA 日志文件输出            |
| [`Screendump`](#moldyn:cmd_screendump)        | 将当前 MD 状态打印到屏幕            |
| [`Thermostat`](#moldyn:cmd_thermostat)        | 管理恒温器                          |
| [`Timestep`](#moldyn:cmd_timestep)            | 设置积分器时间步 $\Delta t$     |
:::

(moldyn:cmd_cell)=
### `Cell`

:::{flat-table}

* - {cspan}`1` 必选参数:
  - {cspan}`1` -
* - {cspan}`1` 可选参数:
  - {cspan}`1` -
* - {rspan}`12` 修饰符:
  - `Cube`
  - ...
  - ...
  - *见正文*
* - `Rect`
  - ...
  - ...
  - *见正文*
* - `Rhomb`
  - ...
  - ...
  - *见正文*
* - `Sphere`
  - ...
  - ...
  - *见正文*
* - `Ellipsoid`
  - ...
  - ...
  - *见正文*
* - `None`
  - —
  - —
  - —
* - `Spring`
  - $k$
  - Real
  - *见正文*
* - {rspan}`1` `Elastic`
  - $t_{\text{avg}}$
  - Real
  - \[时间\]
* - $c_{\text{response}}$
  - Real
  - *见正文*
* - `Anisotropic`
  - —
  - —
  - —
* - `Pressure`
  - ...
  - ...
  - *见正文*
* - `Fixed`
  - —
  - —
  - —
:::

在体系周围定义谐排斥势壁*（该势壁是"软"的，带弹簧常数，原子可以轻微穿透；不支持"硬"排斥壁）*。这有助于将分子保持在明确定义的体积内，或在体系中保持恒压。在后一种情况下，盒子可以定义为弹性的，使其施加明确定义的压力*（见下文）*。请注意，ORCA 不具备周期性边界条件，因此所有盒子都是非周期的（只是排斥壁）。有几种盒子几何形状可用*（一次只能激活一种盒子类型）*：

-   **`Cube`**：定义一个立方盒子。若指定两个实数值 $p_1$ 和 $p_2$ 作为坐标，盒子范围从 $\bigl(p_1,p_1,p_1\bigr)$ 到 $\bigl(p_2,p_2,p_2\bigr)$。若只给一个实数值 $p$，盒子范围从 $\bigl(-\frac{p}{2},-\frac{p}{2},-\frac{p}{2}\bigr)$ 到 $\bigl(\frac{p}{2},\frac{p}{2},\frac{p}{2}\bigr)$，*即*它以原点为中心、棱长为 $p$。

-   **`Rect`**：定义一个正交盒子。必须指定六个实数值 $x_1$、$y_1$、$z_1$、$x_2$、$y_2$ 和 $z_2$ 作为坐标*（按此顺序）*。盒子范围从 $\bigl(x_1,y_1,z_1\bigr)$ 到 $\bigl(x_2,y_2,z_2\bigr)$。

-   **`Rhomb`**：定义一个平行六面体形状的盒子（有时也称为菱形体）。总共必须指定十二个实数值。前三个定义盒子的一个角点 $p$，其余九个定义三个盒子矢量 $v_1$、$v_2$ 和 $v_3$，每个都以笛卡尔矢量分量给出。盒子随后定义为点集 $\bigl\{p+c_1v_1+c_2v_2+c_3v_3\ \rvert\ 0\leq{}c_1,c_2,c_3\leq{}1\bigr\}$。矢量 $v_1$、$v_2$ 和 $v_3$ 不需要彼此正交，但它们不能都位于同一平面内（那样盒子体积为零）。

-   **`Sphere`**：定义一个球形盒子。需要指定四个实数值 $c_x$、$c_y$、$c_z$ 和 $r$。盒子随后定义为围绕中心点 $\bigl(c_x,c_y,c_z\bigr)$、半径为 $r$ 的球。

-   **`Ellipsoid`**：定义一个椭球形状的盒子。作为前三个参数，必须指定三个实数值 $c_x$、$c_y$、$c_z$，定义椭球的中心为 $\bigl(c_x,c_y,c_z\bigr)$。作为第四个参数，必须跟一个关键词，可以是 "`XYZ`" 或 "`Vectors`"。在 "`XYZ`" 情况下，必须再指定三个实数值 $r_x$、$r_y$ 和 $r_z$，定义椭球沿 X、Y 和 Z 坐标轴的部分半径。若改为给出 "`Vectors`"，关键词后必须跟九个实数值 $v_x^1$、$v_y^1$、$v_z^1$、$v_x^2$、$v_y^2$、$v_z^2$、$v_x^3$、$v_y^3$、$v_z^3$。这些值定义三个矢量 $v^1:=\bigl(v_x^1,v_y^1,v_z^1\bigr)$、$v^2:=\bigl(v_x^2,v_y^2,v_z^2\bigr)$ 和 $v^3:=\bigl(v_x^3,v_y^3,v_z^3\bigr)$，它们是椭球的主轴。这些矢量必须严格相互正交。每个矢量的长度定义椭球沿相应主轴的部分半径。

所有盒子类型定义一个谐势 $E_{\text{cell}}\left(r\right):=k\cdot{}r^2$，作用于体系中**在盒子外**的所有原子，其中 $r$ 是原子中心到所定义盒子表面的最近距离。中心在盒子内或直接在盒子表面上的原子不感受任何排斥力。由定义，作用于盒子外原子的力总是平行于盒子表面在最接近原子中心点处的法矢量。这对立方、长方、菱形和球形盒子是平凡的，但对椭球形状的盒子则不那么平凡。

上述方程中的弹簧常数 $k$（*即*势壁的"陡度"）可由 "`Spring`" 修饰符指定，它期望一个实数值作为参数。弹簧常数必须以 kJ mol$^{-1}$ Å$^{-2}$ 为单位指定，这里不能指定其他单位。默认值是 10 kJ mol$^{-1}$ Å$^{-2}$。更大的弹簧常数减小原子穿入势壁的深度，但可能需要更短的积分时间步来确保能量守恒。若出现总能量的跳跃，尝试使用较小的弹簧常数（*例如*默认值）。

命令 "`Cell None`" 禁用任何先前定义的盒子。

如果你想在恒压下运行模拟，可以定义一个弹性盒子。然后，ORCA 在每个时间步积累盒子对原子施加的力，并将该总力除以盒子表面积得到压力。由于该瞬时压力波动很大，使用运行平均来平滑该量。若平均压力大于指定的外压，盒子将略微增大；若较小，盒子将略微收缩。在模拟开始时，在至少运行平均历史深度的步数完成之前，盒子大小不会变化。

弹性盒子通过在盒子几何定义后使用 "`Elastic`" 修饰符启用。随后需要两个实数值 $t_{\text{avg}}$ 和 $c_{\text{response}}$。$t_{\text{avg}}$ 定义平滑压力的运行平均长度*（以物理时间为单位，**不是**时间步）*，而 $c_{\text{response}}$ 常数控制盒子大小最多变化多快。更具体地，$c_{\text{response}}$ 是若平均与外压之比为无穷大时每时间步盒子体积增长的比例，同时若该比值为零时每步盒子体积减少的比例。用数学形式表示，每时间步的盒子体积变化为

 $$
V_{\text{new}}:=\begin{cases}
V_{\text{old}}\cdot\frac{c_{\text{response}}\cdot\frac{\left<p\right>}{p_{\text{ext}}}+1}{c_{\text{response}}+1} & \text{if }\frac{\left<p\right>}{p_{\text{ext}}}\leq{}1,\\
V_{\text{old}}\cdot\frac{\left(c_{\text{response}}+1\right)\cdot\frac{\left<p\right>}{p_{\text{ext}}}}{\frac{\left<p\right>}{p_{\text{ext}}}+c_{\text{response}}} & \text{if }\frac{\left<p\right>}{p_{\text{ext}}}>1,
\end{cases}
$$ (moldyn:eq1) 

其中 $\left<p\right>$ 表示体系对势壁施加的平均压力，$p_{\text{ext}}$ 是指定的外压。好的起始值是 $t_{\text{avg}}=100\,$fs 和 $c_{\text{response}}=0.001$。请注意，较大的 $c_{\text{response}}$ 或较小的 $t_{\text{avg}}$ 值可能导致盒子大小的失控波动。已定义的固定盒子可通过命令 "`Cell Elastic ...`" 切换为弹性（省略号代表两个实参数）。


默认情况下，弹性盒子因压力的大小变化是*各向同性*进行的，*即*盒子作为一个整体缩放，并精确保持其长宽比。通过在开启弹性盒子后指定 "`Anisotropic`" 修饰符，盒子压力被分解为各个分量，允许盒子大小在各个方向独立变化。当然，这只对盒子几何形状 `Rect`、`Rhomb` 和 `Ellipsoid` 有意义。已定义的各向同性盒子可通过简单执行 "`Cell Anisotropic`" 切换为各向异性。

在弹性盒子的情况下，外压由修饰符 "`Pressure`" 定义，它期望一个或三个实数值作为参数。若给出一个参数，这就是各向同性外压。若提供三个参数，这些是 X、Y 和 Z 方向上的压力分量*（对正交盒子）*或沿三个指定矢量方向的压力分量*（对平行六面体形状和椭球形状的盒子）*。这允许各向异性外压（可能只对固态计算有用）。压力和压力分量都必须以 bar（$=10^5$ N m$^{-2}$）为单位指定，不能使用其他单位。若未使用该修饰符，若使用弹性盒子，默认压力将设为 1.0 bar（各向同性）。已定义盒子的外压可通过命令 "`Cell Pressure ...`" 修改（省略号代表实参数）。

由于所有盒子默认都是非弹性的，在盒子定义时没有明确请求非弹性的关键词。不过，可能的应用要求在平衡期间使用弹性盒子，然后在生产运行中将该盒子"冻结"在最终几何上。这可通过使用 "`Cell Fixed`" 命令（不带任何附加参数）实现。

若盒子是弹性的，有一个体积功项贡献于体系的总能量。ORCA 在每一步计算该项并加到势能上。没有该贡献，在弹性盒子运行中守恒量会过度漂移。

要完全关闭先前定义的盒子，简单使用 "`Cell None`"。

请注意，盒子**不会**通过使用 [`Restart`](#moldyn:cmd_restart) 命令自动重启。


**示例（Examples）：**

以原点为中心、棱长 10 Å 的立方盒子：\
`Cell Cube 10`

以原点为中心、半径 5 Å、势壁陡度 20 kJ mol$^{-1}$ Å$^{-2}$ 的球形盒子：

`Cell Sphere 0, 0, 0, 5 Spring 20`

从 $\bigl(-2,-2,0\bigr)$ 到 $\bigl(12,12,10\bigr)$ 的弹性正交盒子，$t_{\text{avg}}=100\,$fs，$c_{\text{response}}=0.001$：

`Cell Rect -2, -2, 0, 12, 12, 10 Elastic 100, 0.001`

以原点为中心、沿 X、Y、Z 轴部分半径为 5、10、15 Å 的椭球形状盒子：

`Cell Ellipsoid 0, 0, 0 XYZ 5, 10, 15`

逗号是可选的，但对负数务必使用它们。默认情况下，减号运算符若可能将充当二元运算符*（见[**上文讨论**](#moldyn:sec_separating)）*。


(moldyn:cmd_constraint)=
### `Constraint`

:::{flat-table}

* - {cspan}`1` {rspan}`2` 必选参数: 
  - *operation* 
  - Keyword 
  - { `Add`, `Remove`, `List` }
* - *type* 
  - Keyword 
  - { `Cartesian`, `Distance`, `Angle`, `Dihedral`, `Center`, `Rigid` }
* - *atom(s)* 
  - Integer 
  - —
* - {cspan}`1` 可选参数: 
  - {cspan}`2` —
* - {rspan}`4` 修饰符: 
  - `Target` 
  - *value(s)* 
  - Real 
  - —
* - `Ramp` 
  - *value(s)* 
  - Real 
  - —
* - `Weights` 
  - ... 
  - ... 
  - *见正文*
* - `All` 
  - {cspan}`2` —
* - `Noprint` 
  - {cspan}`2` —
:::


管理分子动力学模拟中的约束（constraints）。与 [`Restraints`](#moldyn:cmd_restraint) 不同，约束是在每个时刻都严格强制执行的几何关系（*即*它们不会围绕目标值涨落）。约束中涉及的所有原子都必须包含在 active 区域中。原则上，约束在用 [`Minimize`](#moldyn:cmd_minimize) 命令的笛卡尔几何优化中也能工作，但与 L-BFGS 一起的性能可能较差（笛卡尔约束除外，它在 L-BFGS 中工作得很好）。在这些情况下，尝试改用模拟退火方法。

最简单的可能是将一个原子的笛卡尔位置约束到某个值。需要一个从零开始的原子索引。命令 `Constraint Add Cartesian 3` 会将模拟中的第四个原子固定在其当前空间位置。若需显式给出期望位置，可通过 `Target` 修饰符指定，*例如* `Constraint Add Cartesian 3 Target 5.0 1.0 1.0`。为确定固定哪些维度，可添加 `XYZ`、`XY`、`XZ`、`YZ`、`X`、`Y` 或 `Z` 修饰符之一。例如 `Constraint Add Cartesian 3 X Target 1.0` 会将原子 3 的 X 坐标约束到绝对值 1.0，但完全不影响沿 Y 和 Z 坐标的运动。

通过使用 `Distance` 关键词，可以固定原子之间的距离。命令 `Constraint Add Distance 3 5` 会将原子 3 和 5 之间的距离固定到其当前值。需要恰好指定两个原子索引；多个距离约束通过多个 `Constraint` 命令输入。这里也可以通过 `Target` 修饰符给出期望距离值，如 `Constraint Add Distance 3 5 Target 350_pm`。

类似地，原子之间的键角和二面角可用 `Angle` 和 `Dihedral` 关键词固定。键角由三个原子索引定义，二面角由四个原子索引定义。这里也可以指定目标值。笛卡尔、距离、键角和二面角约束的任意组合可以同时使用，甚至可以施加到同一组原子上。一个分子可以通过约束其所有键、键角和扭转变得完全刚性。请确保你的约束不过度确定，也不相互矛盾。否则它们无法被强制执行，模拟将打印警告或崩溃。

一类不同而强大的约束可以用 `Center` 参数定义。紧跟关键词之后，期望一个整数原子编号列表。该列表可以是数字和范围的组合，*例如* "`1, 3, 5..11, 14`"。该原子子集的加权平均位置随后被约束到笛卡尔空间中的固定位置。默认情况下，权重取为原子质量，使所选原子的质心保持固定。这允许，*例如*，运行两个分子的 MD 模拟并固定质心，使其质心距离保持恒定。中心定义的自定义权重可通过在原子列表后使用 `Weights` 修饰符输入。它期望与所指定原子列表长度完全相同数量的实参数。一组原子的几何中心可通过将所有权重设为 $1.0$ 来保持固定，例如 "`Constraint Add Center 2, 5..7 Weights 1.0 1.0 1.0 1.0`"。若需要，可为中心位置给出 `Target`，它期望关键词后三个实数作为 X、Y 和 Z 坐标。若未指定目标，则保持当前中心位置固定。

用 `Rigid` 类型的约束，可以保持完整的原子组为刚性，*即*保持它们彼此之间的所有距离和键角，但作为一个整体移动。`Rigid` 关键词之后，期望一个原子编号列表。可以同时保持多于一组原子为刚性——只需用不同原子列表多次调用 `Constraint Add Rigid` 命令。在内部，刚性约束通过定义正确数量的距离约束来实现。如此大量的距离约束难以收敛；因此，如果刚性约束处于活动状态，RATTLE 未收敛的警告消息将**不**会显示。几乎平面（甚至线性）的原子组很难只用距离约束保持刚性。在平面外添加一个虚原子并将其纳入约束可能有帮助。

ORCA 支持目标值在模拟期间线性变化的约束。要定义这样的约束，在 "`Target`" 修饰符后直接写 "`Ramp`"。"`Ramp`" 之后，跟 "`Target`" 所需数量两倍的实数（距离、键角和二面角为二个而非一个；"`Cartesian XYZ`" 为六个而非三个，依此类推）。这些参数的前一半是起始值，后一半是最终目标值。例如 "`Constraint Add Distance 3 5 Target Ramp 300_pm 400_pm`" 将定义一个目标值从 300 pm 线性上升到 400 pm 的距离约束。斜坡将在约束定义后接下来的 [`Run`](#moldyn:cmd_run) 命令期间执行一次。因此，该 [`Run`](#moldyn:cmd_run) 命令中指定的步数也指定约束目标修改的速率。斜坡完成一次后，最终（恒定）目标值将用于所有后续的 [`Run`](#moldyn:cmd_run) 命令。

如果再次定义已定义的约束，它会被覆盖，*即*先自动删除旧版本的约束。

约束用 `Remove` 关键词删除。你可以删除单个约束，*例如* `Constraint Remove Distance 3 5`，或删除类似的约束组。要删除所有键角约束，使用 `Constraint Remove Angle All`。要删除所有约束，输入 `Constraint Remove All`。

`List` 参数将所有当前活动的约束打印到屏幕和日志文件。不能指定额外的参数。


默认情况下，作用于每个约束的外力在每个 MD 步计算并写入名为 "`basename-constraints.csv`" 的文件*（每约束一列）*。这可能有用——作用于约束的平均力可以，*例如*，用于热力学积分 {cite}`kaestner2006`。若定义了大量约束，若不需要这可能浪费计算机时间。在这些情况下，约束可以用 `Noprint` 修饰符定义。对这样的约束，作用力不计算也不写入文件。注意，预定义的约束*（例如由刚性分子如 TIP3P 水的力场定义）*自动具有该修饰符。

请注意，每个约束使体系的自由度（DoF）减少一个。这一效应被包含在，*例如*温度计算中，其中 DoF 计数进入。从这一考虑也可以理解，约束的行为与弹簧常数非常大的约束（restraint）显著不同：在前一种情况下，DoF 从体系中移除；在后一种情况下，DoF 仍然存在，但只能在一个很小的区间内运动。

若只是要固定一个原子子集，定义大量笛卡尔约束在计算上是低效的。更高效的方法是定义只包含可动原子的 active 区域（见 [`Manage_Region`](#moldyn:cmd_manage_region) 命令）。active 区域外的所有原子不参与时间积分，因此保持其位置。不过，请注意这些原子不能参与任何其他（距离、键角、二面角）约束。


(moldyn:cmd_dump)=
### `Dump`

:::{flat-table}

* - {cspan}`2` 必选参数: 
  - *quantity* 
  - Keyword 
  - { `Position`, `Velocity`, `Force`, `GBW`, `EnGrad` }
* - {cspan}`1` 可选参数: 
  - {cspan}`2` —
* - {rspan}`5` 修饰符: 
  - `Format` 
  - *fmt* 
  - Keyword 
  - { `XYZ`, `PDB`, `DCD` }
* - `Stride` 
  - *n* 
  - Integer 
  - —
* - `Filename` 
  - *fname* 
  - String 
  - —
* - `Region` 
  - *region* 
  - ... 
  - ...
* - `Replace` 
  - {cspan}`2` — 
* - `None` 
  - {cspan}`2` — 
:::


指定如何写模拟的输出轨迹。*quantity* 参数可以是关键词 `Position`、`Velocity`、`Force`、`GBW` 和 `EnGrad` 之一。速度以 Å/fs 写入，力的单位是 Hartree/Å。以下段落只适用于前三个量。转储 GBW 和 EnGrad 文件的工作方式不同，描述见本节最末。

`Stride` 修饰符指定只将每 $n$ 个时间步写入输出文件（默认是 $n=1$，*即*每一步）。步长值为零只在调用 `Dump` 命令时写一帧到轨迹——运行期间不会写更多帧。这可能有帮助，*例如*为 DCD 轨迹写初始 PDB 快照，或在某处保留单个 GBW 文件。

`Format` 修饰符设置输出文件的格式。目前只实现了 `XYZ`、`PDB` 和 `DCD` 格式。请注意 `DCD` 格式定义不完善，不同程序对该扩展名使用不同格式。此外，`DCD` 文件不存储原子类型信息，只与体系的 PDB 快照一起有效（单个 PDB 快照可通过 "`Dump Position Format PDB Stride 0`" 写入）。若未指定，ORCA 尝试从指定文件名的扩展名推断格式。若也未给出文件名，轨迹将默认以 XYZ 格式写入。

`Filename` 修饰符设置输出文件名。若未指定，默认文件名形式为 "`proj-qty-rgn.ext`"，其中 `proj` 是 ORCA 项目的基本名，`qty` 是 `postrj`、`veltrj` 或 `frctrj` 之一，`rgn` 指定转储激活的区域的名称或编号，`ext` 是 `Format` 修饰符选择的文件扩展名。

若在 [`Run`](#moldyn:cmd_run) 命令开始时轨迹文件已存在，新帧默认追加到其末尾。若想改为覆盖现有文件，使用 `Replace` 修饰符。旧的现有文件只在指定带此修饰符的转储后擦除一次。若在转储定义后跟多个 [`Run`](#moldyn:cmd_run) 命令，轨迹在这些运行的每次之前**不会**被替换，只在它们中的第一个之前。要再次覆盖文件，简单用 `Replace` 修饰符重新定义转储。若在运行开始时文件尚不存在，该修饰符无效。向 DCD 轨迹追加帧是不可能的*（因为它们在头部存储总帧数）*。因此，若格式为 DCD，`Replace` 自动开启。

用 `Region` 修饰符，轨迹输出可限制到特定区域（*即*原子子集）。该修饰符期望一个参数，是预定义区域的名称或用户定义区域的编号*（见上文）*。若未指定，将写整个体系的轨迹。多个区域的多个转储命令可以同时活动，但每个区域和量*（位置/速度/力）*对一次只能附带一个转储命令（重新定义将覆盖转储设置）。

用 `None` 修饰符禁用将该量写入输出文件。命令 "`Dump Position None`" 将禁用所有区域的所有位置轨迹的写入。要只禁用特定区域的转储，使用 "`Dump Position Region r None`"，其中 `r` 是区域的名称或编号。

默认是将步长为 `Stride 1`、格式为 `Format XYZ` 的位置轨迹写入名为 "`proj-postrj-all.xyz`" 的文件，其中 "proj" 是 ORCA 项目的基本名。若完全不想创建输出轨迹，使用如上所述的 "`Dump Position None`"。

`Dump GBW` 命令每 $n$ 步保留一份 GBW 文件的副本，可用于计算沿 MD 轨迹的性质，*例如*绘制轨道。这不产生轨迹，因为所有 GBW 文件都单独存储。$n$ 的值由 `Stride` 修饰符控制。文件名通过在 `Filename` 参数后附加步号*（六位带前导零）*再加 ".gbw" 构成。因此，该参数本身不应包含 ".gbw" 扩展名。若未指定 `Filename` 修饰符，默认为 "proj-step"，其中 "proj" 是 ORCA 项目的基本名。这将产生如 "`proj-step000001.gbw`" 等文件。`Format` 和 `Region` 修饰符不能用于 `Dump GBW`。

以非常相似的方式，`Dump EnGrad` 每 $n$ 步存储一个 ORCA `.engrad` 文件*（能量和梯度）*。所有 `.engrad` 文件都单独存储*（不是作为连续轨迹）*。$n$ 的值由 `Stride` 修饰符控制。默认使用如 "`proj-step000001.engrad`" 的文件名。


(moldyn:cmd_initvel)=
### `Initvel`

:::{flat-table}
* - {cspan}`1` 必选参数: 
  - *temp* 
  - Real 
  - \[温度\]
* - {cspan}`1` 可选参数: 
  - {cspan}`2` — 
* - {rspan}`1` 修饰符: 
  - `Region` 
  - *region* 
  - ... 
  - ...
* - `No_Overwrite` 
  - {cspan}`2` — 
:::


基于 Maxwell–Boltzmann 分布用随机数初始化原子的速度，使初始温度与 $temp$ 匹配（另见 [1.5.2](#moldyn:science.initvel){reference-type="ref" reference="moldyn:science.initvel"} 一节）。请注意这会覆盖所有速度，所以当你的体系已平衡时不要调用此命令（*例如*要改温度——改用恒温器）。

初始构型的总线性动量被自动移除，使模拟开始时体系不会漂移。这只涉及初始构型。总线性动量在模拟期间可能因数值效应积累。

用 `Region` 修饰符，速度初始化可对特定区域（*即*原子子集）执行。该修饰符期望一个参数，是预定义区域的名称或用户定义区域的编号*（见上文）*。若未指定，命令作用于整个体系。

`No_Overwrite` 修饰符只在之前未定义/读取任何原子速度时初始化速度。这与 `Restart` 命令结合很有用：读取现有重启文件后，速度已知，若使用该修饰符将跳过初始化。MD 输入中以下命令组合将只在首次执行时初始化速度，在同一输入的所有后续执行中重启位置和速度：

```orca
Restart IfExists
Initvel 350_K No_Overwrite
```

若在 [`Run`](#moldyn:cmd_run) 调用前既未调用 `Initvel` 命令也未调用 [`Restart`](#moldyn:cmd_restart) 命令，原子速度将在开始运行前初始化为零。


(moldyn:cmd_manage_colvar)=
### `Manage_Colvar`

:::{flat-table}
* - {cspan}`1` {rspan}`2` 必选参数:
  - *operation* 
  - Keyword 
  - { `Define` }
* - *id* 
  - Integer 
  - —
* - *type* 
  - Keyword 
  - { `Distance`, `Angle`, `Dihedral`, `CoordNumber` }
* - {cspan}`1` 可选参数: 
  - {cspan}`2` — 
* - {rspan}`4` 修饰符: 
  - `Atom` 
  - *atom* 
  - Integer 
  - —
* - `Group` 
  - *atomlist* 
  - Integers 
  - —
* - `Weights` 
  - *weights* 
  - Reals 
  - —
* - `Cutoff` 
  - *cutoff* 
  - Real 
  - \[长度\]
* - `Noprint` 
  - {cspan}`2` — 
:::


定义用于 [`Metadynamics`](#moldyn:cmd_metadynamics) 或对体系施加 [`Restraints`](#moldyn:cmd_restraint) 的集合变量（"Colvars"）。一般意义上，Colvar 只是所有原子位置的连续函数，返回一个实数。由于 Colvars 本身对模拟没有任何影响，它们目前只能定义或重新定义；没有删除它们的需求。`Manage_Colvar` 命令的第二个参数是 Colvar 的编号。该编号稍后用于寻址该 Colvar。允许的编号在 $1\dots{}10000$ 范围内。若先前定义的 Colvar 编号再次定义，它被简单覆盖*（且所有基于旧 Colvar 的约束被删除！）*。第三个必选参数是 Colvar 的类型，可以是 `Distance`、`Angle`、`Dihedral` 和 `CoordNumber`。未来可能会添加更多 Colvar 类型*（欢迎在论坛提出建议！）*。

距离 Colvar 定义在空间中的两个点之间。每个点可以是单个原子（用 "`Atom`" 表示）或一组原子位置的加权平均（中心）（用 "`Group`" 表示）。例如命令 "`Manage_Colvar Define 1 Distance Atom 0 Atom 7`" 将 Colvar 1 定义为原子 0 和原子 7 之间的距离*（一如既往，原子计数从零开始）*。另一方面，命令 "`Manage_Colvar Define 2 Distance Group 0 1 2 Group 3 4 5`" 将 Colvar 2 设为原子 0、1、2 和原子 3、4、5 的中心之间的距离。若要选许多原子，可使用范围语法 "`Group 0..2`"，如需要可包含多个这样的范围，如 "`Group 0..2, 5, 7..11`"*（另见 [`Manage_Region`](#moldyn:cmd_manage_region) 命令的讨论）*。默认情况下，组使用质心。不过，如有需要，可通过在中心的原子列表结束后直接使用 "`Weights`" 修饰符手动指定权重。"`Weights`" 期望与组中原子数一样多的实数，例如 "`Manage_Colvar Define 2 Distance Atom 0 Group 1 2 3 Weights 1.0 1.0 1.0`"。"`Atom`" 和 "`Group`" 语法可以混用，*例如*定义单个原子与质心之间的距离。定义距离 Colvar 时，修饰符 `X`、`Y`、`Z`、`XY`、`XZ`、`YZ` 和 `XYZ` 之一可在 "`Distance`" 之后直接指定。其中前三个表示在计算距离之前将位置投影到相应的笛卡尔矢量上。随后的三个修饰符要求在计算距离之前将两个位置投影到相应的笛卡尔平面内。最后一个是默认的*（只测量 3D 空间中的标准距离）*，不需要显式指定。

以非常相似的方式，可以定义键角 Colvar。与空间中两个点不同，键角 Colvar 通过空间中三个点定义，每个点可以是 "`Atom`" 或 "`Group`"*（见上文）*。例如命令 "`Manage_Colvar Define 3 Angle Group 0 1 2 Atom 3 Atom 4`" 将 Colvar 3 定义为分别由原子 0、1、2 的质心、原子 3 和原子 4 张成的键角。

二面角 Colvar 通过空间中四个点定义，每个点可以是 "`Atom`" 或 "`Group`"*（见上文）*。例如命令 "`Manage_Colvar Define 4 Dihedral Atom 0 Group 1..5 Atom 6 Atom 7`" 将 Colvar 4 定义为分别由原子 0、原子 1、2、3、4、5 的质心、原子 6 和原子 7 张成的二面角。

Colvar 类型 "`CoordNumber`" 在文献中被建议 {cite}`ianuzzi2003` 用于测量某原子周围某种原子的配位数。该类型 Colvar 成功应用的一个例子是通过元动力学计算溶剂中弱酸的 p$K_{\mathrm{A}}$ 值 {cite}`tummanapelli2014,tummanapelli2015`。该 Colvar 由以下方程定义

$$C:=\frac{1}{N_A}\sum\limits_i^{N_A}\sum\limits_j^{N_B}\frac{1-\left(\frac{r_{ij}}{r_{\mathrm{cut}}}\right)^6}{1-\left(\frac{r_{ij}}{r_{\mathrm{cut}}}\right)^{12}},$$

其中 $N_A$ 是被配位的原子集*（通常只有一个原子）*，$N_B$ 是配位原子集，$r_{ij}$ 是原子 $i$ 和 $j$ 之间的距离，$r_{\mathrm{cut}}$ 是指定配位阈值的常数截断距离。"`CoordNumber`" 之后必须跟两个原子或原子组，分别对应 $N_A$ 和 $N_B$。距离截断在 "`Cutoff`" 修饰符后指定，应跟在两个组定义之后。例如命令 "`Manage_Colvar Define 5 CoordNumber Atom 0 Group 1..10 Cutoff 200_pm`" 将 Colvar 5 定义为原子 1 到 10 的组围绕原子 0 的配位数，距离截断为 $r_{\mathrm{cut}}=200$ pm。

对每个定义的 Colvar，位置的时间发展和作用于 Colvar 的外力默认在每个 MD 步写入名为 "`basename-colvars.csv`" 的文本文件。若定义了大量 Colvars，这可能浪费时间和磁盘空间。在这些情况下，定义 Colvar 时可指定 "`Noprint`" 修饰符。用该修饰符定义的 Colvars 不会出现在文本文件中，作用于 Colvar 的力也不计算*（除非另有需要，例如用于约束）*。


(moldyn:cmd_manage_region)=
### `Manage_Region`

:::{flat-table}
* - {cspan}`1` {rspan}`2` 必选参数: 
  - *identifier* 
  - Keyword/Integer 
  - ...
* - *operation* 
  - Keyword 
  - { `Define`, `AddAtoms`, `RemoveAtoms` }
* - *atomlist* 
  - Integer(s) 
  - —
* - {cspan}`1` 可选参数: 
  - {cspan}`2` — 
* - 修饰符: 
  - `Element` 
  - *elem* 
  - String 
  - —
:::


定义或修改区域。区域只是体系中原子的子集——见上文[**[1.3] 节(#moldyn:sec.functions){reference-type="ref" reference="moldyn:sec.functions"}**](#moldyn:sec_regions)。

如上所述，存在几个以名称标识的预定义区域。唯一可由用户重新定义的预定义区域是 `active` 区域。该区域中的所有原子在分子动力学中受时间积分支配，在极小化运行中被位移。所有其他原子被简单忽略并保持在初始位置。请注意 `active` 区域可能永远不能为空。

要重新定义 `active` 区域，使用命令 "`Manage_Region active Define 1 5 7 ...`"。`active` 之后的整数参数是要包含在区域中的原子编号，按 ORCA 输入文件中给出的顺序。ORCA 中原子编号一般从零开始，*即*计数从 0 开始。

除此之外，支持用户定义的区域。它们用整数编号而非名称标识。整数编号不需要连续，*即*定义区域 2 而不定义区域 1 是可以的。举例来说，命令 "`Manage_Region 1 Define 17 18 19`" 定义区域 1，并向这个新定义的区域添加原子 17、18 和 19。使用不带原子列表的 `Define`，如 "`Manage_Region 1 Define`"，会删除用户定义的区域，因为它随后将为空。可以用 `AddAtoms` 和 `RemoveAtoms` 操作向先前定义的区域（包括 `active` 区域）添加或移除原子。操作名后指定的原子编号被添加到或从区域中移除。例如 "`Manage_Region active RemoveAtoms 15 16 17`" 将从 `active` 区域移除原子 15 到 17（并把它们改加到 `inactive` 区域）。

若想指定原子范围，可使用语法 "`a..b`" 包含从 `a` 到 `b` 的所有原子编号。若只想，*例如*，范围内每第三个原子，可使用 "`a..b..i`" 以增量 `i` 添加从 `a` 到 `b` 的范围。例如 "`2..10..3`" 将展开为列表 `2, 5, 8`。可以混合原子编号和范围，如下面两个示例所示*（一如既往，逗号是可选的）*：

```orca
Manage_Region active Define 1, 4, 5..11, 14, 17..30..2
Manage_Region active RemoveAtoms 4, 15..17
```

代替原子列表，可使用 `Element` 修饰符，后跟一个表示元素标签的字符串。这与指定包含该元素类型所有原子的原子列表效果相同。别忘了元素标签字符串周围的双引号。例如 `Manage_Region active RemoveAtoms Element "H"` 从 active 区域移除所有氢原子。


(moldyn:cmd_metadynamics)=
### `Metadynamics`

:::{flat-table}
* - {cspan}`1` 必选参数: 
  - {cspan}`2` — 
* - {cspan}`1` 可选参数: 
  - {cspan}`2` — 
* - {rspan}`19` 修饰符: 
  - `Off` 
  - {cspan}`2` — 
* - `Reset` 
  - {cspan}`2` — 
* - `Colvar` 
  - *colvar* 
  - Integer 
  - —
* - `Scale` 
  - *scale* 
  - Real 
  - ...
* - {rspan}`2` `Wall` 
  - *side* 
  - Keyword 
  - { `Lower`, `Upper` }
* - *target* 
  - Real 
  - 物理单位
* - *k* 
  - Real 
  - kJ mol$^{-1}$ 物理单位$^{-2}$
* - {rspan}`2` `HillSpawn` 
  - *frequency* 
  - Integer 
  - —
* - *height* 
  - Real 
  - kJ mol$^{-1}$
* - *sigma* 
  - Real 
  - 物理单位
* - {rspan}`2` `Range` 
  - *from* 
  - Real 
  - 物理单位
* - *to* 
  - Real 
  - 物理单位
* - *resolution* 
  - Integer 
  - —
* - `Store` 
  - *store* 
  - Integer 
  - —
* - `Temperature` 
  - *temp* 
  - Real 
  - \[温度\]
* - `WellTempered` 
  - *biastemp* 
  - Real 
  - \[温度\]
* - {rspan}`3` `Lagrange` 
  - *mass* 
  - Real 
  - a.m.u.
* - *k* 
  - Real 
  - kJ mol$^{-1}$ 标度单位$^{-2}$
* - *target_temp* 
  - Real 
  - \[温度\]
* - *tau* 
  - Real 
  - \[时间\]
:::


设置 [`Metadynamics`](#moldyn:sec_metadynamics) 模拟 {cite}`laio2002` 的参数。设置完所有参数后，实际模拟可通过 [`Run`](#moldyn:cmd_run) 命令启动。参数既可以在对 `Metadynamics` 命令的单次调用中全部设置，也可以分布在多次这样的调用中以避免过长的行。两种情况下，参数设置都有一些顺序规则。元动力学的所有 Colvars 需要在设置任何其他参数之前指定。与 Colvars 相关的修饰符（如 `Scale`、`Wall` 或 `Range`）只适用于它们之前最后指定的那个 Colvar。

`Colvar` 修饰符指定要在元动力学模拟中使用的 Colvar。它期望一个整数参数，是之前通过 [`Manage_Colvar`](#moldyn:cmd_manage_colvar) 命令定义的 Colvar 编号。ORCA MD 模块支持一维和二维元动力学，所以可给出一个或两个 `Colvar` 修饰符。指定的 `Colvar` 修饰符数量定义元动力学模拟的维数。请注意与 Colvars 相关的修饰符（如 `Scale`、`Wall` 或 `Range`）只适用于它们之前最后指定的那个 Colvar，所以在指定第一个 Colvar 之后、指定第二个 Colvar 之前应设置它们。

Colvars 可以有不同的物理单位，如距离用 Å、键角用度。在多维元动力学运行中，相应数值的不同量级可能是个问题：键角跨越 180 度的范围，而距离往往只在 10 Å 的区间内。为将所有 Colvars 归到相近的标度，元动力学模块在内部将每个 Colvar 除以用户提供的常数。这些内部值是无量纲的，将被称为"标度单位（scale units）"。对先前指定的 Colvar，标度常数可通过 `Scale` 修饰符设置。它期望一个实参数，必须以 Colvar 的物理单位指定（距离 Colvar 用长度单位，键角和二面角 Colvar 用角度单位）。配位数 Colvar 本来就是无量纲的。若未指定，使用合理的标度默认值，距离 Colvar 为 1.0 Å，键角和二面角 Colvar 为 20.0 度，配位数 Colvar 为 0.2。注意 `Scale` 修饰符只适用于 `Metadynamics` 命令中其之前最后给出的那个 Colvar。

作为示例，考虑以下命令设置二维元动力学模拟：

```orca
Manage_Colvar Define 1 Distance Atom 0 Atom 1
Manage_Colvar Define 2 Angle Atom 0 Atom 1 Atom 2
Metadynamics Colvar 1 Scale 1.0_A Colvar 2 Scale 10.0_Deg
```

为在元动力学模拟期间将 Colvars 保持在感兴趣区域内，可对 Colvars 施加谐势壁。这通过 `Wall` 修饰符实现。作为第一个参数，它期望势壁的方向，可以是 `Lower` 或 `Upper`。第二个参数是该势壁的位置——以 Colvar 的物理单位给出（*例如*距离 Colvar 用 Å），**不是**标度单位。作为可选的第三个实参数，谐势壁的弹簧常数可以 kJ mol$^{-1}$ 单位$^{-2}$ 为单位指定，其中单位是 Colvar 的默认物理单位（距离用 Å，键角用度）。若省略，距离用 50 kJ mol$^{-1}$ Å$^{-2}$、键角用 0.5 kJ mol$^{-1}$ 度$^{-2}$、配位数用 250.0 kJ mol$^{-1}$ 的弹簧常数*（合理的选择）*。下壁和上壁都可在同一个 `Wall` 修饰符后定义，如 "`Metadynamics Colvar 1 Wall Lower 3.0_A 50.0 Upper 10.0_A 50.0`"。注意单侧谐势壁也可通过 [`Restraint`](#moldyn:cmd_restraint) 命令施加到 Colvars 上。对标准元动力学，这是冗余的。但对扩展拉格朗日元动力学*（见下文）*，这有区别：约束作用于 Colvar 从而作用于真实原子体系，而 `Metadynamics` 命令中定义的势壁直接作用于虚拟粒子。再次注意 `Wall` 修饰符只适用于 `Metadynamics` 命令中其之前最后给出的那个 Colvar。

最后一个适用于 Colvars 的修饰符是 `Range` 修饰符。它对元动力学运行本身没有影响，只控制自由能剖面的输出。`Range` 修饰符期望三个参数。前两个必须是实数，定义相对该 Colvar 的自由能剖面要输出的区间上下边界。第三个参数是整数类型，控制为该区间生成多少网格点。在二维元动力学中，两个 Colvars 都可以有关联的 `Range` 修饰符，它们随后控制自由能剖面二维网格的区间和分辨率。在这种情况下，网格不应比 $100\times{}100$ 细得多；否则网格点的求值会相当慢。若未给出 `Range` 修饰符，使用默认值（距离 Colvar 范围 $0\dots{}20$ Å，键角 Colvar 范围 $0\dots{}180$ 度，二面角 Colvar 范围 $-180\dots{}180$ 度，配位数 Colvar 范围 $0\dots{}3$）。如上，注意 `Range` 修饰符只适用于 `Metadynamics` 命令中其之前最后给出的那个 Colvar。

向偏置势添加新高斯山丘通过 `HillSpawn` 修饰符控制。它期望三个参数。第一个参数必须是整数类型，定义山丘生成频率，*即*每多少 MD 步添加一个新山丘*（通常每 10–50 fs）*。第二个参数是实数，以 kJ mol$^{-1}$ 为单位指定每个新山丘的高度*（通常 0.1–1.0 kJ mol$^{-1}$）*。第三个参数以"标度单位"设置高斯山丘的宽度 $\sigma$（这是标准差，**不是**方差 $\sigma^2$）——见上文 `Scale` 修饰符。在二维元动力学模拟中，宽度同时适用于两个维度，两个 Colvars 的标度需要调整以获得山丘宽度正确的"长宽比"。$\sigma$ 的标准选择是 0.1–1.0 标度单位。山丘生成参数可在元动力学模拟期间随时更改，不修改已存在的山丘。若要在元动力学模拟期间暂时暂停生成新山丘，可指定 "`Metadynamics HillSpawn Off`"。若要删除所有山丘，考虑下述 `Reset` 修饰符。

`Store` 修饰符控制当前中间自由能剖面保存到磁盘的频率。它期望一个整数参数，指定两次此类存储之间的 MD 模拟时间步数。在一维元动力学中，这些自由能剖面的文件名是 "`basename-metadynamics_profile_###.csv`"，其中 "`###`" 表示剖面写入后的步号。除此之外，还写一个文件 "`basename-metadynamics_profile_history.csv`"，包含所有先前计算的自由能剖面作为列，以便它们可以轻松打印在同一张图上。对二维元动力学，写文件名为 "`basename-metadynamics_2d_profile_###.gp`" 的 Gnuplot 源文件，可用免费工具 Gnuplot*（在 Windows 和 GNU Linux 上都运行）*转换为等高线图。这些等高线图的原始数据可在相应的名为 "`basename-metadynamics_2d_profile_###.gp.csv`" 的文件中找到。注意在两种情况下，自由能标度原点都设为最深的自由能阱，使所有数都为正。若未指定 `Store` 修饰符，默认每 1000 MD 步存储一次自由能剖面。

`WellTempered` 修饰符开启良温元动力学（well-tempered Metadynamics）{cite}`barducci2008`。与标准元动力学不同，该方法中自由能剖面对长运行收敛到一个极限。简而言之，该方法在已生成许多山丘的位置缩小山丘大小，使偏置势的变化随时间变小*（收敛）*。`WellTempered` 修饰符期望一个实参数，即所谓的偏置温度，以温度单位指定。偏置温度的选择应使 $\frac{1}{2}\cdot{}k_{\mathrm{B}}\cdot{}T_{\mathrm{Bias}}$ 与模拟要克服的最大能垒大致相当。例如 12 000 K 的偏置温度很适合克服约 100 kJ mol$^{-1}$ 的能垒。注意元动力学模块需要知道模拟温度才能在良温元动力学运行中重建自由能剖面。通常在元动力学运行期间应有恒温器活动，保持模拟温度恒定。在这种情况下，温度简单地从恒温器获得。但若未为 `all` 区域指定恒温器，良温元动力学的模拟温度必须手动指定。这可通过 `temperature` 修饰符实现，它期望一个实参数——以温度单位的模拟温度。

`Lagrange` 修饰符开启扩展拉格朗日元动力学（extended Lagrangian Metadynamics）{cite}`ianuzzi2003`。在该变体中，一个虚拟粒子*（带质量和速度）*在 Colvars 张成的空间中运动，该粒子与真实原子体系之间唯一的连接是一个谐弹簧。偏置势*（高斯山丘）*只作用于虚拟粒子。第一个参数是虚拟粒子的质量（a.m.u.）。第二个参数是谐弹簧常数（kJ mol$^{-1}$），以标度单位求值——见上文 `Scale` 修饰符。典型值取决于体系和 Colvars，但可能是 100 a.m.u. 和 10 kJ mol$^{-1}$。可选地，可给第三和第四个参数以开启虚拟粒子的恒温。这里施加一个简单的 Berendsen 恒温器。第三个参数是虚拟粒子的目标温度，第四个参数是恒温器时间常数 $\tau$。好的选择是目标温度 100 K、$\tau=10$ fs。注意与普通 Berendsen 恒温器不同，虚拟粒子只被冷却，从不被加热。换句话说，只有当虚拟粒子的瞬时温度大于目标温度时恒温器才变得活跃。这是为确保虚拟粒子可以改变方向——否则它可能在非常长的时间区间内被驱动向同一方向。

`Reset` 修饰符重置偏置剖面，*即*它删除所有已生成的山丘，使偏置剖面再次变平。元动力学模拟的所有其他参数不被修改。例如若山丘生成仍开启，则新的山丘将在下一个模拟运行中生成。

`Off` 修饰符完全关闭元动力学。它删除所有山丘并关闭元动力学模块。它还重置元动力学的 Colvar 选择，所以若你想在同一输入脚本中设置第二个不同的元动力学运行，需要先使用它。该修饰符只能作为 `Metadynamics` 命令的第一个参数给出，其后不能跟任何参数。

元动力学模块的重启文件（文件名 "`basename.metarestart`"）在每次生成新山丘时写入。[`Restart`](#moldyn:cmd_restart) 命令检测该文件并自动重启元动力学运行*（即若活动，加载所有山丘和扩展拉格朗日虚拟粒子的位置和速度）*。但这只在调用 [`Restart`](#moldyn:cmd_restart) 命令时元动力学处于活动并已设置的情况下发生。元动力学模拟的参数**不**会被重启。因此，在你的输入文件中保留所有通过对 `Metadynamics` 命令调用的参数设置，并在它们之后、[`Run`](#moldyn:cmd_run) 命令之前，简单调用 [`Restart`](#moldyn:cmd_restart) 命令即可。

另请参阅[**[1.3] 节(#moldyn:sec.functions){reference-type="ref" reference="moldyn:sec.functions"}**](#moldyn:sec_metadynamics)中关于元动力学的讨论。

(moldyn:sec.metadyn.example)=

本节以一个二维良温扩展拉格朗日元动力学运行的完整示例结束，带重启能力*（只需再次运行同一输入即可从中断处继续模拟）*。两个 Colvar 定义为原子之间的距离。你需要将[蓝色]{style="color: blue"}中的所有参数调整到你的问题和体系：

```orca
Timestep 0.5_fs
Initvel 350_K
Thermostat NHC 350_K Timecon 100.0_fs
Dump Position Stride 1 Filename "trajectory.xyz"
Manage_Colvar Define 1 Distance Atom 0 Atom 1
Manage_Colvar Define 2 Distance Atom 2 Atom 3
Metadynamics Colvar 1 Scale 1.0_A Wall Lower 3.0 50.0 Upper 10.0 50.0 Range 0.0 15.0 100
Metadynamics Colvar 2 Scale 1.0_A Wall Lower 1.0 50.0 Upper 8.0 50.0 Range 0.0 13.0 100
Metadynamics HillSpawn 40 0.5 0.5 Store 2000
Metadynamics WellTempered 6000_K
Metadynamics Lagrange 100.0 10.0 200.0_K 10.0_fs
Restart IfExists
Run 100000
```

(moldyn:cmd_minimize)=
### `Minimize`

:::{flat-table}
* - {cspan}`1` 必选参数: 
  - {cspan}`2` — 
* - {cspan}`1` 可选参数: 
  - *method* 
  - Keyword 
  - { `Combined`, `LBFGS`, `Anneal` }
* - {rspan}`10` 修饰符: 
  - `Steps` 
  - *n* 
  - Integer 
  - —
* - `MaxGrad` 
  - *thres* 
  - Real 
  - \[kJ mol$^{-1}$ Å$^{-1}$\]
* - `RMSGrad` 
  - *thres* 
  - Real 
  - \[kJ mol$^{-1}$ Å$^{-1}$\]
* - `TempConv` 
  - *thres* 
  - Real 
  - \[温度\]
* - `Accel` 
  - *value* 
  - Real 
  - —
* - `Damp` 
  - *value* 
  - Real 
  - —
* - `StepLimit` 
  - *value* 
  - Real 
  - \[长度\]
* - `History` 
  - *n* 
  - Integer 
  - —
* - `Noise` 
  - *value* 
  - Real 
  - \[长度\]
* - `OnlyH` 
  - {cspan}`2` — 
:::

对体系执行笛卡尔能量极小化。对分子而言，这不如 ORCA 内建的内坐标几何优化高效*（即需要更多步才能收敛）*。不过，这里采用的算法也适用于大原子数*（例如 50 000）*的情况（如 QM/MM 模拟中有时遇到的），这完全超出 ORCA 主优化模块的范围。此外，该极小化也在所有类型的约束下工作（L-BFGS 情况下有一些限制），这些约束用 [`Constraint`](#moldyn:cmd_constraint) 命令设置，若激活还包括排斥模拟盒子的效应。只有包含在 active 区域中的原子被位移，所有其他原子保持在其位置。

执行极小化最简单的方式是不带参数调用 `Minimize` 命令。这默认使用 L-BFGS 方法，相当稳健高效。若极小化似乎不稳定，尝试减小 `History` 或 `StepLimit` 参数。L-BFGS 对笛卡尔类型以外的约束有时表现不佳。除此之外，还有一个模拟退火方法已实现，可通过指定 `Anneal` 作为第一个参数选择。与 L-BFGS 不同，模拟退火方法对所有类型的约束都同样工作。还有一个 `Combined` 方法，是若干 L-BFGS 步在开头、随后是模拟退火运行直到温度降到阈值以下、再一个最终 L-BFGS 运行直到达到收敛判据的组合。

用 `Steps` 修饰符，可指定极小化步的最大数目。若已执行了这么多步，无论是否满足收敛判据，极小化都会完成。默认值是 500。

`MaxGrad` 和 `RMSGrad` 修饰符控制某个原子上最大梯度和梯度均方根平均值的收敛阈值。默认值目前设为 5.0 和 1.0 kJ mol$^{-1}$ Å$^{-1}$，这与主 ORCA 几何优化中的默认设置大致相同的判据。

若给出 `TempConv` 修饰符，模拟退火运行在温度于 5 个连续步内单调下降并降到指定值以下后完成。注意模拟退火运行在达到该条件或观察到梯度阈值时都会完成。不需要同时满足两个判据。

`Accel` 修饰符指定模拟退火运行的加速度因子*（对 L-BFGS 无影响）*。只要某个原子的速度矢量与梯度矢量之间的夹角低于 90 度，梯度乘以该因子、速度乘以该因子的一个分数。这有助于强制沿梯度方向更快运动。默认值是 4.0。若不希望该特性，用 `Accel 1.0` 关闭它（1.0 表示"无人为加速度"）。

`Damp` 修饰符是模拟退火运行的阻尼因子*（对 L-BFGS 无影响）*。原子速度在每个积分步乘以该因子。默认值是 0.98。较小的值将使算法更稳定、更不易振荡和过冲，但也需要显著更多步才能收敛。不要使用 $\geq{}1$ 的值，否则那就不再是"退火"了 :-)

`StepLimit` 修饰符指定极小化运行一步中任何原子*（以长度为单位）*可发生的最大位移。这有助于避免大的、不可靠的步，它们可能导致几何突变和非常高的势能。该修饰符涉及 L-BFGS 和模拟退火运行。负值禁用步长限制。默认禁用步长限制。若需开启，试用约 0.1 Å 量级的值。

`History` 修饰符控制 L-BFGS 方法中用于近似逆 Hessian 的梯度和位置矢量历史的深度。默认值是 20。较小的值有助于稳定算法。

用 `Noise` 修饰符，可在极小化开始前向原子位置添加小的随机数。这有助于在极小化中逃离局域极大值和鞍点。例如，初始为线性水分子的极小化将无法离开该极大值——但有一些随机"噪声"，就有可能。该修饰符期望一个实参数，以长度单位指定最大原子位移（约 0.01 Å 是合理的）。该特性默认关闭。

若给出 `OnlyH` 修饰符，所有非氢原子在极小化开始前从 active 区域移除。极小化完成后，恢复原始 active 区域。若只优化氢原子位置，*例如*精修实验晶体结构，这很有帮助。


(moldyn:cmd_printlevel)=
### `PrintLevel`

:::{flat-table}
* - {cspan}`1` 必选参数: 
  - *value* 
  - Keyword 
  - { `Low`, `Medium`, `High`, `Debug` }
* - {cspan}`1` 可选参数: 
  - {cspan}`2` — 
* - 修饰符: 
  - {cspan}`3` — 
:::


控制模拟期间打印到屏幕的信息量。`Debug` 只应在少数情况下使用，因为它可能严重减慢模拟速度。

默认值是 `Medium`。


(moldyn:cmd_randomize)=
### `Randomize`

:::{flat-table}
* - {cspan}`1` 必选参数: 
  - {cspan}`2` — 
* - {cspan}`1` 可选参数: 
  - *seed* 
  - Integer 
  - —
* - 修饰符: 
  - {cspan}`3` — 
:::


ORCA MD 模块中有一些依赖随机数的算法，*例如*用 [`Initvel`](#moldyn:cmd_initvel) 命令初始化原子速度。这些随机数是所谓的"伪随机数"，由确定性生成器产生。该生成器有一个*状态*，只是一个整数。若初始化到相同状态，生成器将总是创建相同的"随机"数序列。乍一看这像是缺陷，但对科学可重复性和调试目的是非常重要的特性。若你用"随机"速度初始化启动同一 MD 输入文件多次，所有运行的轨迹将完全相同。


然而，有些情况不希望这种行为，*例如*若你想对同一体系的多条轨迹平均某个性质。在这些情况下，在输入开头调用 `Randomize` 命令。若不给参数，随机数生成器以当前系统时间作为种子初始化。在不同时间启动的 MD 运行开始时将有不同的随机速度。若想对该过程有更多控制，也可以指定一个正整数作为参数，用作初始随机种子。以相同种子参数启动的模拟将具有相同的初始随机速度（若所有其他系统参数如原子数、原子类型等保持相同）。

不调用 `Randomize`，总是使用种子 1。


(moldyn:cmd_restart)=
### `Restart`

:::{flat-table}
* - {cspan}`1` 必选参数: 
  - {cspan}`2` — 
* - {cspan}`1` 可选参数: 
  - *fname* 
  - String 
  - —
* - 修饰符: 
  - `IfExists` 
  - {cspan}`2` — 
:::

读取重启文件以继续先前的分子动力学运行。每个模拟步后都会写这样的重启文件，使崩溃的模拟可以轻松恢复。重启文件的文件名可通过 *fname* 给出；否则从项目基本名推断为 `<basename>.mdrestart`。

若指定 `IfExists` 修饰符，只在重启文件存在时才执行重启。该标志抑制了通常在重启文件不存在时会发生的错误和中止。这在一系列批处理运行中的第一次很有用，那时开始时重启文件尚不存在。

请注意，以下量被存储到/从重启文件加载：

-   原子位置

-   原子速度

-   恒温器内部状态*（仅对 NHC）*

-   元动力学山丘和扩展拉格朗日内部状态

-   模拟步号和已用物理时间

所有其他量（时间步、区域、恒温器、约束、盒子等）**不**会被重启，需要在输入文件中设置，通常**在** `Restart` 命令之前。在 [`Run`](#moldyn:cmd_run) 命令之前立即调用 `Restart` 命令是安全的。

另请参阅[**[1.3] 节(#moldyn:sec.functions){reference-type="ref" reference="moldyn:sec.functions"}**](#moldyn:sec_restart)中关于重启模拟的讨论。


(moldyn:cmd_restraint)=
### `Restraint`

:::{flat-table}
* - {cspan}`1` {rspan}`2` 必选参数: 
  - *operation* 
  - Keyword 
  - { `Add`, `Reset` }
* - 
  - Keyword 
  - `Colvar`
* - *colvar* 
  - Integer 
  - —
* - {cspan}`1` 可选参数: 
  - {cspan}`2` — 
* - {rspan}`10` 修饰符: 
  - `Harmonic` 
  - {cspan}`2` — 
* - `Gaussian` 
  - {cspan}`2` — 
* - `Spring` 
  - {cspan}`2` — 
* - `Sigma` 
  - *Gaussian Sigma* 
  - Real 
  - ...
* - `Height` 
  - *Gaussian Height* 
  - Real 
  - kJ mol$^{-1}$
* - `Target` 
  - *target* 
  - Real 
  - ...
* - `Lower` 
  - *lower wall* 
  - Real 
  - ...
* - `Upper` 
  - *upper wall* 
  - Real 
  - ...
* - {rspan}`1` `Ramp` 
  - *initial target* 
  - Real 
  - ...
* - *final target* 
  - Real 
  - ...
* - `Noprint` 
  - {cspan}`2` — 
:::

该命令对先前通过 [`Manage_Colvars`](#moldyn:cmd_manage_colvar) 命令定义的集合变量（"Colvars"）施加约束（restraints）。作为第一个参数，它期望要执行的操作类型，可以是 `Add` 和 `Reset`。第二个参数需要是关键词 "`Colvar`"，第三个参数是指定对其执行该操作的 Colvar 的整数。

若第一个参数是 "`Add`"，则向指定的 Colvar 添加一个新约束。注意任意数量的不同类型约束可同时在一个 Colvar 上活动。Colvar 编号之后的下一个参数需要是约束的类型。目前允许 `Harmonic` 和 `Gaussian`。添加谐约束时，可给出 `Spring` 修饰符，以 kJ mol$^{-1}$ 单位$^{-2}$ 指定约束的谐弹簧常数，其中单位是 Colvar 的默认物理单位（距离用 Å，键角用度）。若未指定，使用 50 kJ mol$^{-1}$ 单位$^{-1}$ 的值。添加高斯约束时，允许 `Height` 和 `Sigma` 修饰符。前者以 kJ mol$^{-1}$ 设置高斯山丘的高度，后者以 Colvar 的物理单位设置高斯函数的宽度*（$\sigma$ 是标准差，**不是**方差 $\sigma^2$）*。高度可正可负，允许高斯山丘和高斯阱。若未指定，使用高度 $-10$ kJ mol$^{-1}$*（即高斯阱）*和 sigma 10 个 Colvar 单位*（例如 Å 或度）*的默认值。

新约束的位置通过 `Target` 修饰符控制，它期望一个以 Colvar 为单位的实参数。若约束应是单侧势壁，可用 `Lower` 和 `Upper` 修饰符代替 `Target`。也可以同时指定 `Lower` 和 `Upper`，以在一条命令中定义不同位置的下壁和上壁。若 `Ramp` 直接跟在 `Target`、`Lower` 或 `Upper` 之后，定义一个目标位置随时间线性移动的约束。`Ramp` 期望两个参数，即初始约束位置和下一个后续 [`Run`](#moldyn:cmd_run) 命令之后的最终约束位置。

以下示例展示如何将具有不同下壁和上壁参数的谐双侧约束分配给先前通过 [`Manage_Colvars`](#moldyn:cmd_manage_colvar) 命令定义的编号为 7 的距离 Colvar：

`Restraint Add Colvar 7 Harmonic Lower 400_pm Spring 50.0`\
`Restraint Add Colvar 7 Harmonic Upper 800_pm Spring 80.0`

默认情况下，每个约束的一些附加数据*（当前位置、势能、外力、内力）*在每个 MD 步打印到名为 "`basename-restraints.csv`" 的文件。这些数据可用于，*例如*，热力学积分。若定义了大量约束，这可能浪费时间和磁盘空间。要为约束关闭此项，定义时指定 `Noprint` 修饰符。

若第一个参数是 "`Reset`"，则删除施加在指定 Colvar 上的所有约束。不能给出其他参数或修饰符*（除上述三个必选参数外）*。


(moldyn:cmd_run)=
### `Run`

:::{flat-table}
* - {cspan}`1` 必选参数: 
  - *n* 
  - Integer 
  - —
* - {cspan}`1` 可选参数: 
  - {cspan}`2` — 
* - {rspan}`1` 修饰符: 
  - `StepLimit` 
  - *value* 
  - Real 
  - \[长度\]
* - `CenterCOM` 
  - {cspan}`2` — 
:::

用当前设置执行 $n$ 个时间步的分子动力学运行，应用速度 Verlet 算法求解运动方程（见 [1.5.1](#moldyn:science.integration){reference-type="ref" reference="moldyn:science.integration"} 一节）。你可能想先调用 [`Timestep`](#moldyn:cmd_timestep)、[`Initvel`](#moldyn:cmd_initvel)、[`Thermostat`](#moldyn:cmd_thermostat) 和 [`Dump`](#moldyn:cmd_dump) 等命令。请注意只有 `active` 区域内的原子受时间积分支配。所有其他原子将被跳过，因此保留其初始位置。

`StepLimit` 修饰符可用于限制 MD 时间积分步中任何原子的最大位移。除位移外，速度也将限制在最大 *value*$\cdot\Delta{}t$。若初始几何较差且作用力很大（原子靠得很近等），这有助于稳定动力学。该关键词期望一个以距离为单位的实参数。合理的选择是 0.1 Å。

若给出 `CenterCOM` 修饰符，整个体系的质心（CoM）保持固定。通常 CoM 反正不应漂移，因为速度初始化以给 CoM 零初始速度的方式执行，动量守恒应保持这样。但数值误差和 massive [`Thermostats`](#moldyn:cmd_thermostat)*（除其他因素外）*会破坏该动量守恒，导致 CoM 随时间漂移。若要避免这种情况，指定该修饰符。

若在该命令之前未调用 [`Initvel`](#moldyn:cmd_initvel)，原子速度初始化为零。若在该命令之前未调用 [`Timestep`](#moldyn:cmd_timestep)，设默认时间步 $0.5\,\mathrm{fs}$。

你可以通过创建名为 "`EXIT`" 的空文件干净地结束 MD 运行*（注意在大小写敏感文件系统上全大写字母）*。在 GNU Linux 等 Unix 操作系统上，这可通过命令 "`touch EXIT`" 轻松实现。将检测该文件、中止 MD 运行并删除该文件。你仍将得到剩余输出*（如计时统计）*，且不必删除所有剩余的 "`.tmp`" 文件，而若你杀死进程则两者都不会如此。

(moldyn:cmd_scflog)=
### `SCFLog`

:::{flat-table}
* - {cspan}`1` 必选参数: 
  - *value* 
  - Keyword 
  - { `Discard`, `Last`, `Append`, `Each` }
* - {cspan}`1` 可选参数: 
  - {cspan}`2` — 
* - 修饰符: 
  - {cspan}`3` — 
:::


控制电子结构计算的详细输出（*即*积分、scf、梯度等）是否/如何写入日志文件。`Discard` 完全丢弃输出。`Last` 只为每次程序调用保留最后一次输出（若模拟中止，便于读取错误消息）。`Append` 将所有输出重定向到单个日志文件（"basename.scf.log"、"basename.int.log"、"basename.grad.log" 等），每一步追加到文件末尾。`Each` 将每一步每个程序的输出写入不同的日志文件，这些文件的文件名中有步号。

打印到 SCF 日志文件的信息量可由标准 ORCA 打印标志控制，如 "`%output PrintLevel Maxi end`"。注意默认情况下 ORCA 在第一次 SCF 后降低打印级别。因此，轨道能量和布居分析等性质默认只打印一次。若你想对后续 SCF 运行保持打印级别不变，通过 ORCA 输入中的 "`%method ReducePrint false end`" 禁用该特性。

默认值是 `Append`。注意这在长运行中可能导致很大的日志文件。


(moldyn:cmd_screendump)=
### `Screendump`

:::{flat-table}
* - {cspan}`1` 必选参数: 
  - {cspan}`2` — 
* - {cspan}`1` 可选参数: 
  - {cspan}`2` — 
* - 修饰符: 
  - {cspan}`3` — 
:::

将 MD 模块的当前状态（原子位置、速度、势能和动能、盒子性质等）以明确定义且"可 grep"的格式打印到屏幕和日志文件。这主要用于单元测试，*例如*验证 MD 运行后的体系状态是否等于从其他 ORCA 二进制发行版获得的状态。


(moldyn:cmd_thermostat)=
### `Thermostat`

:::{flat-table}
* - {cspan}`1` 必选参数: 
  - *type* 
  - Keyword 
  - { `Berendsen`, `CSVR`, `NHC`, `None` }
* - {cspan}`1` 可选参数: 
  - *temperature* 
  - Real 
  - \[温度\]
* - {rspan}`6` 修饰符: 
  - `Timecon` 
  - *tau* 
  - Real 
  - \[时间\]
* - `Ramp` 
  - *target_temp* 
  - Real 
  - \[温度\]
* - `Chain` 
  - *chain_length* 
  - Integer 
  - —
* - `MTS` 
  - *mts* 
  - Integer 
  - —
* - `Yoshida` 
  - *yoshida* 
  - Integer 
  - —
* - `Region` 
  - *region* 
  - ... 
  - ...
* - `Massive` 
  - — 
:::

更改后续模拟运行的原子恒温器设置。"*Type*" 设置恒温器类型。目前实现了三种恒温器类型：Berendsen {cite}`berendsen1984`、Nosé–Hoover 链（NHC）{cite}`martyna1992,martyna1996` 和"通过速度缩放的正则采样"（CSVR）{cite}`bussi2007`。非常基本而稳健的 Berendsen 恒温器只应用于早期预平衡运行，因为它**不**采样正则系综并会导致飞冰块效应等问题。NHC 和 CSVR 恒温器都非常精密，正确采样正则系综。所有标准 NVT 模拟都应使用这两种之一。用 `None` 作为类型禁用恒温器。

可选的 *temperature* 参数设置体系恒温到的目标温度。若省略该参数，使用上次调用 [`Initvel`](#moldyn:cmd_initvel) 命令的温度（若之前未调用过，则中止模拟）。

`Timecon` 修饰符设置恒温器的耦合强度（大时间常数对应弱耦合）。默认值是 $10\,\mathrm{fs}$，这是相对强的耦合。对生产运行，$100\,\mathrm{fs}$ 是合适的。$10\dots 100\,\mathrm{fs}$ 范围内的值是合理的（另见 [1.5.3](#moldyn:science.thermostats){reference-type="ref" reference="moldyn:science.thermostats"} 一节）。

若使用 `Ramp` 修饰符，可在 MD 运行期间施加温度斜坡。斜坡结束时的最终温度必须在修饰符后直接指定。斜坡开始时的初始温度取自 *temperature* 参数*（若缺少该参数，取自上次 [`Initvel`](#moldyn:cmd_initvel) 命令）*。温度斜坡只施加到首先跟随斜坡定义的 [`Run`](#moldyn:cmd_run) 命令。斜坡的斜率选取使得在运行结束时达到最终温度。任何后续 [`Run`](#moldyn:cmd_run) 命令将简单地使用最终温度进行恒温。要施加另一个温度斜坡，需要显式地再次定义它。

`Chain`、`MTS` 和 `Yoshida` 修饰符只适用于 NHC 恒温器。它们分别指定 Nosé–Hoover 链的链长（默认：3）、恒温器积分执行的多重时间步数（默认：2）和所用 Yoshida 积分器的阶数（默认：3，允许：1、3、5、7）。通常很少需要修改这些参数之一。更多信息参阅原始出版物 {cite}`martyna1992,martyna1996`。

`Massive` 修饰符激活 *massive thermostating*，意味着每个自由度分配一个独立的恒温器。这对预平衡运行有用（有助于达到能量均分），在生产运行中不应使用，因为它可能严重扭曲动力学。注意 massive 恒温器也破坏动量守恒（线性和角动量都是），所以若这是个问题，最好为 [`run`](#moldyn:cmd_run) 命令指定 `CenterCOM` 修饰符。另请注意大体系的 massive NHC 恒温器可能相当慢，因为每个 NHC 恒温器本身就是一个需要时间积分的动力系统。

用 `Region` 修饰符，恒温器可附加到特定区域（*即*原子子集）。该修饰符期望一个参数，是预定义区域的名称或用户定义区域的编号*（见上文）*。若未指定，恒温器作用于整个体系。多个区域的多个恒温器可以同时活动，但每个区域一次只能附带一个恒温器（重新定义将覆盖恒温器设置）。

命令 "`Thermostat None`" 将从所有区域移除所有恒温器。若只想为特定区域禁用恒温器，使用 "`Thermostat None Region r`"，其中 `r` 是区域的名称或编号。

请注意，若体系温度接近 0 K，所有三种已实现的恒温器类型都将无效果（或产生意外效果），因为它们都通过将速度乘以一个*（或多或少复杂的）*因子来工作。

(moldyn:cmd_timestep)=
### `Timestep`

:::{flat-table}
* - {cspan}`1` 必选参数: 
  - *dt* 
  - Real 
  - \[时间\]
* - {cspan}`1` 可选参数: 
  - — 
* - 修饰符: 
  - — 
:::

将所有后续运行用于积分运动方程的模拟时间步 $\Delta{}t$ 设为 $dt$。若你的体系含氢原子，建议时间步不超过 $0.5\,\mathrm{fs}$。若只有较重的原子，可选择较大的时间步。仍允许准确模拟的时间步的好估计是 $\Delta{}t=\sqrt{m}\cdot{}0.5\mathrm{fs}$，其中 $m$ 是体系中最轻原子的质量（a.m.u.）。这是一些科学家用全氘代化合物进行模拟的一个原因：它允许将时间步增加约 1.4 倍 :-)

若在 [`Run`](#moldyn:cmd_run) 调用前未调用该命令，将在开始运行前设默认时间步 $0.5\,\mathrm{fs}$。


(moldyn:science)=
## 科学背景（Scientific Background）

本节更深入地描述 ORCA MD 模块中使用的一些方法和算法，重点是科学背景。

(moldyn:science.integration)=
### 时间积分与运动方程（Time Integration and Equations of Motion）

分子动力学模拟的核心概念是求解牛顿运动方程（至少在原子核被经典处理的范围内）。它们写为

$$\ddot x_i\left(t\right)=\frac{F_i\Bigl(\vec{x}\left(t\right)\Bigr)}{m_i},\quad i=1\dots N,$$

其中 $x_i\left(t\right)$ 表示第 $i$ 个自由度在时间 $t$ 的位置，$m$ 是相应的质量，$F_i$ 是作用于该自由度的力。由于力可能依赖于所有位置，这是一个 $N$ 个常微分方程（ODEs）的耦合系统。一般情况下，不可能得到该系统的解析解，因此应用数值求解方法。这些几乎总是基于将时间变量离散化并通过采取有限时间步近似求解系统。

在数值求解耦合 ODE 系统的所有不同方法中，哈密顿系统的*辛积分格式（symplectic integration schemes）*在分子动力学领域获得了特别关注。它们具有非常好的能量守恒。与许多其他方法不同，它们在研究混沌哈密顿系统（如 MD 模拟）的长期演化时表现出合理的行为。三种流行的辛积分格式是 *Leapfrog* 算法、*Verlet* 方法和 *Velocity Verlet* 积分器。尽管名称不同，它们非常相似。容易看出 Verlet 和 Velocity Verlet 方法在代数上等价（从 Velocity Verlet 算法中消去速度），并且可以证明最终所有三种方法都是相同的。[^3] 三种方法都是全局误差为 2 阶的显式积分方法，因此比半隐式欧拉方法高一阶，后者也是辛积分格式。由于 Velocity Verlet 算法是这三种方法中唯一在同一时间点给出速度和位置的方法，许多流行的分子动力学软件包（CP2k、CPMD、LAMMPS）使用该格式。出于同样的原因，ORCA MD 模块使用 Velocity Verlet 算法作为时间积分方法。

Velocity Verlet 格式的一般方程写为

$$\begin{aligned}
\vec{x}\left(t+\Delta t\right) &= \vec{x}\left(t\right)+\vec{v}\left(t\right)\Delta t+\frac{1}{2}\vec{a}\left(t\right)\Delta t^2,\\
\vec{v}\left(t+\Delta t\right) &= \vec{v}\left(r\right)+\frac{\vec{a}\left(t\right)+\vec{a}\left(t+\Delta t\right)}{2}\Delta t.\end{aligned}$$

代入

$$\vec{a}_i\left(t\right)=\frac{\vec{F}_i\left(t\right)}{m_i},\quad i=1\dots N,$$

得到两步方法

$$\begin{aligned}
\vec{x}_i\left(t+\Delta t\right) &= \vec{x}_i\left(t\right)+\vec{v}_i\left(t\right)\Delta t+\frac{\vec{F}_i\left(t\right)}{2m_i}\Delta t^2,\quad &i=1\dots N,\\
\vec{v}_i\left(t+\Delta t\right) &= \vec{v}_i\left(r\right)+\frac{\vec{F}_i\left(t\right)+\vec{F}_i\left(t+\Delta t\right)}{2m_i}\Delta t,\quad &i=1\dots N,\end{aligned}$$

这在 ORCA 的 MD 模块中实现。


(moldyn:science.initvel)=
### 速度初始化（Velocity Initialization）

在 MD 模拟开始时，往往只知道原子的初始位置，不知道速度。由于 MD 模拟在某个有限温度下进行，以使期望的模拟温度一开始就存在的方式初始化速度是个好主意。在统计力学中，常假定原子的速度分布由 Maxwell–Boltzmann 分布给出（严格来说这只在理想气体中成立）。因此，在 MD 模拟开始时按 Maxwell–Boltzmann 方程初始化原子的速度是合理的选择。目标是找到一个初始速度分布，使每个自由度具有相近的能量，从而近似满足能量均分定理。

温度 $T$ 下的标量 Maxwell–Boltzmann 速度分布（略去归一化因子）为

$$f\left(v\right)=v^2\exp\Bigl(-\frac{mv^2}{2k_BT}\Bigr).$$

为初始化粒子的速度使满足该分布函数，从一系列均值为 $0$、方差为 $1$ 的正态分布随机数 $\mathcal{N}\left(0,1\right)$ 开始。每个原子的笛卡尔速度分量随后由下式计算

$$v_{i,\alpha}:=\sqrt{\frac{k_BT}{m_i}}\,\mathcal{N}\left(0,1\right),\quad\alpha\in\{x,y,z\},\ \ i=1\dots N.$$

由于 C++98 标准不提供平台无关的方式获得正态分布随机数，这些在内部通过对均匀分布随机数施加 *Box–Muller 变换* {cite}`box1958` 计算：假设 $u_1$ 和 $u_2$ 是区间 $[0,1]$ 上两个均匀分布随机数，方程

$$\begin{aligned}
z_1 &:= \sqrt{-2\log\left(u_1\right)}\cos\left(2\pi u_2\right),\\
z_2 &:= \sqrt{-2\log\left(u_1\right)}\sin\left(2\pi u_2\right)\end{aligned}$$

产生两个服从均值 $0$、方差 $1$ 正态分布的新随机数 $z_1$ 和 $z_2$。

速度初始化后，体系的总线性动量可能有某个非零的有限值。由于线性动量在分子动力学模拟中（近似）守恒，这将导致体系在模拟过程中向一个方向漂移，这大概不是所期望的。因此，在 Maxwell–Boltzmann 初始化后显式将总动量设为零：

$$\begin{aligned}
\vec{P}_\mathrm{tot} &:= \sum\limits_{i=1}^Nm_i\vec{v}_{i,\mathrm{old}},\\
\vec{v}_{i,\mathrm{new}} &:= \vec{v}_{i,\mathrm{old}}-\frac{\vec{P}_\mathrm{tot}}{m_iN},\quad i=1\dots N.\end{aligned}$$

这当然可能改变初始温度。因此，执行最后一步，将所有速度矢量乘以一个确定的因子，使初始温度精确匹配目标值。

(moldyn:science.thermostats)=
### 恒温器（Thermostats）

初始速度初始化到某个有限温度后，可能以为只需开始动力系统的时间积分（等同于 *NVE 系综*），起始温度就会大致保持。然而在真实体系中，（至少）有两个原因使温度在几步之后就会强烈偏离初始值。首先，初始速度分布只考虑粒子的动能，但一定量的能量将立即与势能贡献（*例如*键伸缩）交换，改变温度。其次，由有限时间步引入的数值误差（在*从头算* MD 情况下还有近似力）将导致能量从而温度的漂移。为抵消这些效应，通常希望在模拟过程中有温度控制（模拟随后在 *NVT 系综*下运行），这称为恒温器。

存在许多不同种类的恒温器，从简单的表达式到自身就是高度复杂动力系统的都有。但它们都有一个共同的问题：若恒温器只与体系弱耦合，温度仍会变化。但若恒温器与体系耦合更强（*即*干预更强），则模拟的动力学将改变，不再类似人们想研究的未受扰动的原始动力学。因此，决定恒温器应与体系耦合多强，总是在温度稳定性与受扰动动力学之间的权衡。

在 ORCA 中，目前实现了三种恒温器：Berendsen 恒温器 {cite}`berendsen1984`、Nosé–Hoover 链恒温器（NHC）{cite}`martyna1992,martyna1996` 和"通过速度缩放的正则采样"恒温器（CSVR）{cite}`bussi2007`。

### Berendsen 恒温器（Berendsen Thermostat）

Berendsen 恒温器 {cite}`berendsen1984` 类似于简单的速度缩放方案，但增加了时间常数 $\tau$ 来控制耦合强度。设 $T_0$ 为期望的目标温度，$T$ 为体系当前温度。则恒温器引起的温度梯度可表示为

$$\frac{dT}{dt}=\frac{T_0-T}{\tau}.$$

考虑到使用离散时间步 $\Delta t$，每个时间步速度的校正因子由下式确定

$$f:=\sqrt{1+\frac{\Delta t\left(T_0-T\right)}{T\tau}}$$

新速度随后容易得到为

$$\vec{v}_{i,\mathrm{new}}:=f\cdot\vec{v}_{i,\mathrm{old}},\quad i=1\dots N.$$

考虑一些特殊情况。若 $\tau=\Delta t$，整个温度偏离 $T_0$ 的量立即被校正，温度总是精确保持在目标值。这等同于简单速度缩放（无任何时间常数），已知这对大多数系统效果很差（例如单个谐振子会简单地爆炸）。用较大的时间常数 $\tau>\Delta T$，耦合强度降低，得到合理的结果。通常应用 $\tau$ 在 $20\dots 200\cdot\Delta T$ 范围内的值。对 $\tau\to\infty$，耦合强度趋于零，恒温器不再活跃。不允许 $\tau<\Delta T$ 的值。

从公式可知，若体系温度为 0 K（或在 "massive" 情况下：所考虑的自由度为 0 K），Berendsen 恒温器将无效，因为它基于将速度乘以一个因子来修改温度。因此，这种恒温器不能用于从 0 K 开始加热体系。

(moldyn:science.constraints)=
### 约束（Constraints）

与约束（restraints）不同，约束（constraints）是在每个时刻都严格强制执行的几何关系（*即*它们不会围绕目标值涨落）。许多分子动力学技术使用几何约束（*例如*保持水分子刚性，或固定某个反应坐标）。标准 BOMD 将核描述为空间中的点电荷，使原子的运动由经典力学定律支配。经典力学中的体系可用拉格朗日形式体系描述，它包含一个成熟的关于完整约束（holonomic constraints）的子形式体系，即拉格朗日乘子法。

然而，分子动力学将时间离散化以用有限时间步求解运动方程，常使用 Verlet 积分器。在时间离散化下，强制执行和保持精确约束稍微复杂些。近几十年来，已开发出这样做的一种著名算法是 SHAKE 算法。但它有一个缺点，即只在位置上强制执行约束，不在速度上。这可能导致问题，如沿约束方向的"隐藏"速度造成人为的高温值。SHAKE 的一个扩展也对速度强制执行约束，是 RATTLE 算法，它在 ORCA 的 AIMD 模块中实现。

RATTLE 格式是 Velocity Verlet 积分器允许约束的推广。这意味着 RATTLE 不是在 Velocity Verlet 积分器之外应用，而是取代它。在无活动约束的情况下，两种方法相同。耦合约束的系统不能一步精确求解，RATTLE 使用迭代方法同时强制执行所有约束。这在性能方面常是关注的问题。然而在 AIMD 中，能量和梯度计算通常每步要花数秒甚至数分钟，因此迭代求解约束的额外计算时间完全可以忽略。

作为迭代过程，RATTLE 不能给出精确解，只能收敛到给定容差。在 ORCA MD 模块中，容差目前设为距离 $10^{-2}$ pm、键角和二面角 $10^{-4}$ 度。该容差通常在几十次迭代内达到。某些情况下，RATTLE 迭代可能不收敛到所需容差。这通常是约束集合过度确定或矛盾时的情况。

RATTLE 的数学和技术细节这里不描述，可在文献中找到。RATTLE 的一般概念由 Andersen 提出 {cite}`andersen1983`。原始文章只涵盖距离约束。后续工作描述如何处理任何完整约束，特别是如何约束键角和二面角 {cite}`kutteh1998`。Wilson 矢量（*即*键角和二面角相对笛卡尔原子位置的导数）取自 Wilson 的原始工作 {cite}`wilson1955`。


[^1]: 严格来说，这些模拟是 Born–Oppenheimer 分子动力学模拟（BOMD），因为它们近似求解不含时薛定谔方程来计算梯度，然后按这些梯度移动原子。

[^2]: 技术上说，ORCA 随后将是一个图灵完备的脚本解释器，从而使*任何*计算问题都能用 ORCA 解决 :-)

[^3]: Hairer, Lubich, Wanner, "Geometric Numerical Integration", Springer 2006.
