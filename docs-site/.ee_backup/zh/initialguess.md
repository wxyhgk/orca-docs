

<a id="sec:essentialelements.initialguess"></a>
# 初始猜测的选择与 SCF 计算的重启（Choice of Initial Guess and Restart of SCF Calculations）

初始猜测是每个 SCF 计算中的一个重要问题。如果这一
猜测是合理的，计算过程的收敛性将会好得多。
ORCA 在提供良好的初始猜测方面做了不少努力，并给
用户足够的灵活性，以便根据其需要来定制初始猜测。

初始猜测同样通过 `%scf` 块以及
变量 `Guess`、`MOInp` 和 `GuessMode` 来控制。

```orca
%scf
  Guess     HCore       # One electron matrix
            Hueckel     # Extended H\"uckel guess
            PAtom       # Polarized atomic densities
            PModel      # Model potential 
            MORead      # Restart from an earlier calc.
  MOInp     "Name.gbw"  # orbitals used for MORead
  GuessMode FMatrix     # FMatrix projection
            CMatrix     # Corresponding orbital projection
  AutoStart true        # try to use the orbitals from the existing
                        # GBW file of the same name (if possible)
                        # (default)
            false       # don't use orbitals from existing GBW file
end
```

<a id="sec:essentialelements.initialguess.oneElectron"></a>
## 单电子矩阵猜测（One Electron Matrix Guess）

最简单的猜测是对单电子矩阵进行对角化以获得
起始轨道。这一猜测非常简单，但通常也是一场灾难，
因为它产生的轨道过于紧缩。

<a id="sec:essentialelements.initialguess.projection"></a>
## 基组投影（Basis Set Projection）

其余的猜测（可能）需要将初始猜测
轨道投影到实际基组上。在 ORCA 中有两种方式可以
做到这一点：`GuessMode FMatrix` 和 `GuessMode CMatrix`。这两种方法的
结果通常相当接近。在某些情况下
`GuessMode CMatrix` 可能更可取。`GuessMode FMatrix` 更简单
也更快。简而言之，`FMatrix` 投影定义了一个有效的单
电子算符：

$$

\hat{f}=\sum\limits_p { \varepsilon_{p} a_{p}^{\dagger} a_{p} }\qquad \text{(eqn:49)}

$$

其中求和遍及初始猜测轨道集合中的所有轨道，
$a_{p}^{\dagger}$ 是猜测 MO $p$ 中电子的产生算符，
$a_{p}$ 是相应的湮灭算符，
$\varepsilon_{i}$ 是轨道能量。这个有效的单电子
算符在实际基组中被对角化，其本征向量
就是目标基组中的初始猜测轨道。对大多数波函数
而言，这会产生相当合理的猜测。

`CMatrix` 更为复杂。它利用对应轨道理论
分别拟合每个 MO 子空间（占据、部分占据或自旋向上与
自旋向下占据）[amos1961proc,king1967chem](../../bibliography.md)。在
拟合占据轨道之后，虚轨道由
占据轨道的正交补中选取。在某些情况下，
尤其是在重启 ROHF 计算时，这可能是一个优势。
否则，对于大多数情况，预计 `CMatrix` 不会
明显优于 `FMatrix`。

<a id="sec:essentialelements.initialguess.PModel"></a>
## PModel 猜测（PModel Guess）

PModel 猜测（通过 `%scf` 块中的 `Guess PModel` 选择，或简单地
在关键词行中使用 `!PModel`）通常是相当
成功的一种。它构建并对角化一个 Kohn--Sham
矩阵，其电子密度由球形中性原子密度的叠加
组成，这些密度是为相对论与非相对论方法
预先确定的。这一猜测对 Hartree--Fock 和 DFT 方法均有效，
但不适用于半经验模型。
不过，由于该猜测较为复杂，它也会占用少量
计算机时间（通常少于一次 SCF 迭代）。模型密度
适用于元素周期表中的大多数原子，因此
PModel 猜测通常是首选方法（尤其对于含
重元素的分子），除非你有更精确的起始
轨道可用。

<a id="sec:essentialelements.initialguess.PAtom"></a>
## Hückel 与 PAtom 猜测（Hückel and PAtom Guesses）

扩展 Hückel 猜测的做法是执行一次最小基组的
扩展 Hückel 计算，并使用上述两种方法之一
将该计算得到的 MO 投影到实际基组上。
最小基组是 STO-3G 基组。Hückel 猜测可能不
是很好，因为 STO-3G 基组实在太差。也有
越来越多的证据表明，原子密度的叠加
能产生相当好的初始猜测。原子密度
方法的缺点在于它没有考虑分子的实际形状，
而且更难可靠地为 ROHF 计算定义单占据
轨道或为 UHF 计算定义合理的自旋密度。
因此 ORCA 在 `PAtom`
猜测（即默认猜测）中选择了不同的方式：Hückel 计算直接
在原子 SCF 轨道的最小基组中
*针对所有电子* 进行。这些轨道是一劳永逸确定的，
并存储在程序内部。这意味着原子周围的密度非常
接近原子本身，同一中心上的所有轨道都是精确
正交的，初始电子分布已经反映了
分子形状，并且存在定义良好的单占据轨道供
ROHF 计算使用。

<a id="sec:essentialelements.initialguess.restart"></a>
## 重启 SCF 计算（Restarting SCF Calculations）

要重启 SCF 计算，读入先前计算的轨道信息
会非常有帮助并节省时间。为此，
请指定：

```orca
! moread
%moinp "name.gbw"
```

对于单点计算，如果存在同名的 `.gbw` 文件，
则默认会自动执行此操作——
参见 [sec:essentialelements.initialguess.autostart](#sec:essentialelements.initialguess.autostart)。

程序在每个 SCF 循环中都会存储当前轨道。如果作业
崩溃，可以通过重新运行计算来使用现有的 `.gbw` 文件，
从而从当时存在的轨道重新开始。
此外，我们还努力使不同
版本的 `.gbw` 文件彼此兼容。如果你的输入 `.gbw` 文件来自
较旧的版本，请使用 `! rescue moread noiter` 配合 `% moinp "name.gbw"`
来生成最新的 `.gbw`。当调用 `rescue` 关键词时，
只会从 `.gbw` 文件中读取轨道系数，
其余一切都取自输入文件。因此，请确保
旧 `.gbw` 文件的几何结构和基组与新输入相匹配。

在同一个 ORCA 版本内，`name.gbw` 中存储的几何结构和基组
都不必与当前的几何结构或基组相匹配。
程序只会检查当前计算和 `name.gbw` 中的分子是否
彼此一致，然后
执行一种可能的轨道投影。如果两个基组
完全相同，程序默认只对输入轨道进行重新正交化和
重新归一化。不过，这可以通过在 `% scf` 块中
显式指定 `GuessMode` 为 `CMatrix` 或
`FMatrix` 来覆盖。

**如果基组中的冗余分量已被移除（参见
[sec:essentialelements.lindep](#sec:essentialelements.lindep)），则不得使用 `! moread noiter`
来读取先前计算的 SCF 轨道，因为这会
导致错误的结果。在这种情况下，如果无法
一次性完成整个计算，可以使用 `! moread`
（不带 `noiter`）。**

如果使用 `!moread` 和 `%moinp`，来自先前
计算的输入 `.gbw` 文件必须与新计算具有不同的名称，因为
在计算的一开始会写入一个新的 `.gbw` 文件。如果
名称相同，先前计算的 `.gbw` 文件会被
覆盖，所有信息都会丢失。因此，如果你想
使用与先前计算相同名称的输入文件来重启计算，
就必须先重命名 `.gbw` 文件。无论如何，这都是
良好的做法，可以避免意外，尤其是对于昂贵的计算。
或者，你可以使用
[AutoStart 功能](sec:essentialelements.initialguess.autostart)
来代替显式指定 `!moread` 和 `%moinp`。

重启 SCF 计算还有一个方面——如果你
选择了 `SCFMode = Conventional`，程序会将大量
积分存储到磁盘上，这些积分的计算可能非常耗时。
通常程序会在计算结束时
删除这些积分。但是，如果你想进行一个密切相关的计算，
且需要相同的积分（即*几何结构*、*基组*
和*阈值* `Thresh` 相同），那么使用先前
生成的积分会更快。这可以通过在第一次计算的
`% scf` 块中使用 `KeepInts = true`，然后在第二次计算的
`% scf` 块中使用 `ReadInts = true` 来实现。如果
第二次计算的名称与第一次计算不同，则
必须使用 `IntName = "FirstName"` 来告知程序积分
文件的名称。请注意，包含积分的文件没有
扩展名——它就是去掉 `.inp`
后缀的先前输入文件的名称。

```orca
%scf
  KeepInts true         # Keep integrals on disk
  ReadInts true         # Read integrals from disk
  IntName  "MyInts"     # Name of the integral files without extension
end
```

请注意，一般而言，使用旧积分文件重启计算
需要用户自行了解并承担责任。如果使用得当，
这一功能可以节省相当多的时间。

<a id="sec:essentialelements.initialguess.autostart"></a>
## AutoStart 功能（AutoStart feature）

较旧版本的 ORCA 总是在运行开始时创建一个新的 GBW 文件，无论
是否已存在同名文件或其中是否可能含有轨道。
现在，在单点计算的情况下，
程序会自动检查是否存在同名的 `.gbw` 文件。
如果存在，程序会检查其中是否包含轨道以及
重启所需的所有其他信息。如果包含，变量 `Guess` 就会被设置
为 `MORead`。已有的 `.gbw` 文件被重命名为 `BaseName.ges`，
`MOInp` 被设置为该文件名。如果不希望
使用 `AutoStart` 功能，请在 `%scf` 块中设置 `AutoStart false`，
或在简单输入行中给出关键词
`!NoAutoStart`。请注意，对于几何优化，`AutoStart` 会被
忽略：在这种情况下，使用先前收敛的轨道（包含在不同
名称的 `.gbw` 文件中）可以通过 `MORead` 和 `MOInp`
来实现。

<a id="sec:essentialelements.initialguess.changes"></a>
## 改变初始猜测 MO 的顺序与打破初始猜测的对称性（Changing the Order of Initial Guess MOs and Breaking the Initial Guess Symmetry）

有时你会想要改变初始猜测 MO 的顺序——
无论是因为初始猜测产生了错误的占据模式，
还是因为你想利用先前计算的轨道
收敛到不同的电子态。MO 的重排以及其他
任务（如打破电子波函数的对称性）都可以
方便地用 ORCA 中的 `Rotate` 功能来处理。`Rotate` 是
SCF 块的一个子块，允许你对 MO 对进行
线性变换。

```orca
%scf
  Rotate
   { MO1, MO2, Angle }
   { MO1, MO2, Angle, Operator1, Operator2 }
   { MO1, MO2} # Shortcut to swap MO1 and MO2. Angle=90 degrees.
  end
end
```

这里，`MO1` 和 `MO2` 是所关注的两个 MO 的索引。请记住，
ORCA 从索引 0 开始对 MO 计数，即索引为 1 的 MO 是
*第二个* MO。`Angle` 是以度为单位的旋转角度。90$^{\circ}$ 的旋转
角对应于交换两个 MO，45$^{\circ}$ 的角度
导致两个 MO 以 50:50 混合，而 180$^{\circ}$
旋转则导致相位改变。`Operator1` 和 `Operator2` 是
用于旋转的轨道集合。对于 UHF 计算，自旋向上轨道
属于算符 0，自旋向下轨道属于算符 1。RHF 和 ROHF
计算只有一组轨道。

除其他用途外，`Rotate` 功能可用于产生
破缺对称解，例如在过渡金属二聚体中。
为此，首先执行一次高自旋计算，然后找出
互为对称和反对称组合的
MO 对。以这些 MO 作为初始猜测，并对
每一对使用 45$^{\circ}$ 的旋转来定域化起始 MO。如果你
运气好且破缺对称解存在，你就有很大机会
通过这种方式找到它。关于破缺对称方法的更多细节，
参见 [sec:spectroscopyproperties.magnx](#sec:spectroscopyproperties.magnx)
一节。

<a id="sec:essentialelements.initialguess.guessmix"></a>
## 自动打破初始猜测的对称性（Automatically Breaking of the Initial Guess Symmetry）

对于更简单的情况，打破初始猜测对称性的另一个简单方法是直接使用关键词 `!GUESSMIX`。这会自动将 50% 的 alpha LUMO 混入 alpha HOMO。这等价于上述的 45 度旋转，且只针对这两个轨道。当人们想要开壳层单重态、并需要 alpha 与 beta 轨道以不同方式起始时，这可能会很有用。

具体的旋转角度可通过以下方式控制：

```orca
%scf
  guessmix 75 # angle in degrees, default is 45
end
```

<a id="sec:essentialelements.initialguess.scfguessenergy"></a>
## 仅计算输入密度的能量（Calculating only the energy of an input density）

如果你想给出先前 SCF 的结果并重新计算能量，
或者在不改变轨道的情况下用该密度计算
其他性质（例如 MP2 能量），
可以使用标志 `!CALCGUESSENERGY NOITER`。

SCF 程序会读取轨道，计算密度以及
获得能量所需的一个 Fock 矩阵，然后
不再进行轨道更新而继续。例如，这
可用于将 DFT 轨道与 DLPNO-CCSD(T) 结合使用。请谨慎
对待由此得到的结果，因为这些轨道不再是变分的！

<a id="sec:essentialelements.initialguess.keywords"></a>
## 关键词（Keywords）

<a id="tab:essentialelements.initialguess.keywords.simple"></a>
!!! note "与初始猜测相关的简单输入关键词。"
    :header-rows: 1
    :class: footnotesize

| 项目 | 内容 |
| --- | --- |
| **关键词** | 无 |

      - 说明

| 项目 | 内容 |
| --- | --- |
| **`PAtom`** | 无 |

      - 选择极化原子猜测

| 项目 | 内容 |
| --- | --- |
| **`PModel`** | 无 |

      - 选择模型势猜测

| 项目 | 内容 |
| --- | --- |
| **`Hueckel`** | 无 |

      - 选择扩展 Hückel 猜测

| 项目 | 内容 |
| --- | --- |
| **`HCore`** | 无 |

      - 选择单电子矩阵猜测

| 项目 | 内容 |
| --- | --- |
| **`MORead`** | 无 |

      - 从先前计算读取 MO
        （与 `%moinp "myorbitals.gbw"` 一起使用）

| 项目 | 内容 |
| --- | --- |
| **`AutoStart`** | 无 |

      - 尝试从与当前文件同名的现有 GBW 文件开始
        （默认；仅适用于单点计算）

| 项目 | 内容 |
| --- | --- |
| **`NoAutoStart`** | 无 |

      - 不执行上述操作

| 项目 | 内容 |
| --- | --- |
| **`NoIter`** | 无 |

      - 将 SCF 迭代次数设为 0。
        这与 MOREAD 配合使用，意味着
        程序将直接使用所提供的起始轨道。

| 项目 | 内容 |
| --- | --- |
| **`KeepInts`** | 无 |

      - 在常规模式（conventional mode）下计算后不从磁盘删除积分

| 项目 | 内容 |
| --- | --- |
| **`ReadInts`** | 无 |

      - 在常规模式下从先前计算读取现有积分
        （与 `%scf IntName "PreviousBaseName" end` 一起使用）

| 项目 | 内容 |
| --- | --- |
| **`CalcGuessEnergy`** | 无 |

      - 计算初始猜测轨道的能量
        （与 `NoIter` 一起使用）

