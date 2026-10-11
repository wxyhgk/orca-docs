```{index} MRCI, MRPT
```

(sec:modelchemistries.mrci)=
# 多参考组态相互作用与微扰理论（Multireference Configuration Interaction and Perturbation Theory，非收缩）

多参考相关模块（`orca_mrci`）是为传统（非收缩）方法（组态相互作用 MR-CI
和微扰理论 MR-PT）设计的，这是本节的主要重点。
需要说明的是，这些方法的共同点是它们考虑从参考波函数的每一个
组态状态函数（CSF）出发的激发。因此，
此类方法的计算成本随参考空间（例如 CAS-CI）的大小
迅速增长。此外，为提高效率所有积分必须保存在内存中，这进一步
限制了应用领域。

内收缩（internally contracted）多参考方法，如 [N 电子价态微扰理论（NEVPT2）](sec:modelchemistries.nevpt2)，没有
这些瓶颈。这里激发是相对于整个参考
波函数定义的。若干内收缩方法（[NEVPT2](sec:modelchemistries.nevpt2)、[NEVPT4(SD)](sec:modelchemistries.autoci.ficnevpt.nevpt4)、[FIC-MRCC](sec:modelchemistries.autoci.ficmrcc2)
和 [FIC-MRCI](#sec:modelchemistries.autoci.ficmrci)）可用并在手册的其他地方描述。

:::{Note} 注意
NEVPT2 通常是首选方法，因为它快速且易于使用。如果对该领域不熟悉，强烈建议查看相关章节。以下章节侧重于作为 `orca_mrci`
模块一部分的传统多参考方法。
:::
(sec:modelchemistries.mrci.intro)=
## 引言
`orca_mrci` 中的所有方法都是非收缩的，并从
由多个组态（轨道占据模式）构成的参考波函数开始。虽然分子轨道通常来自 CASSCF 计算，但参考波函数不限于完全活性空间（CAS）。
限制活性空间（RAS）或任意组态列表可以在 `refs` 子块中定义。

总波函数通过考虑从参考组态出发的单激发和双激发来构建。这些激发
组态随后用于生成具有正确自旋和空间对称性的组态状态函数（CSF）。波函数参数的数量随参考
函数的数量迅速增长。orca_mrci 模块具有一组截断判据
（`TSel, TPre, TNat`），有助于减少波函数参数的数量。此外，默认情况下，程序只考虑
已经具有目标自旋和空间对称性的参考组态。在某些情况下这是不希望的，可以通过关键词 `rejectinvalidrefs false` 取消这些限制。
关于理论、程序模块及其用法的更多信息，我们推荐 Neese 等人的综述文章。{cite}`neese_advanced_2007` 该主题的教程式介绍
在手册第 {ref}`sec:modelchemistries.mrci` 章中给出，更多示例见
CASSCF 教程。


尽管已经有相当多的经验，程序的这一部分
使用起来仍有些困难，在接受结果之前需要耐心和
仔细测试。虽然我们尽量
让您的工作轻松，但您必须意识到最终
任何有意义的多参考*从头算*计算都比标准 SCF 或 DFT
计算或 MP2 这类单参考相关方法需要用户更多的
洞察和规划——所以
不要气馁！您还应该意识到，使用多参考
方法很容易让大型计算机长时间运行却仍然不能产生有意义的结果——您的洞察是成功应用的关键
要素！下面几个示例说明了
`orca_mrci` 模块的一些基本用法。

## RI 近似

首先，重要的是要理解当前实现中 MR-CI 模块的默认模式执行从 AO 到 MO 基组的完整积分
变换。当 CI 中包含的 MO 超过约 200 个时，这变得非常费力
且极其占用内存。或者，可以从恒等分解
（resolution of the identity, RI）近似构造分子
电子-电子排斥积分。*因此，如果选择此选项，必须提供有意义的辅助基组*。我们推荐 TurboMole 开发者为 MP2 计算开发的拟合基组。这些给出
精确的跃迁能；然而，总能量中的误差
略高，可能在 1 mEh 左右。检查
`IntMode` 以更改积分变换的默认模式。
请注意，无论哪种方式，个别选择的 MRCI 模块都需要
将所有积分保存在内存中，这限制了可研究分子的大小。

## 个别选择

其次，重要的是要理解 MR-CI 模块是
*个别选择*（individually selecting）类型的。因此，只有那些与目标态的
0$^{\text{th} }$ 阶近似相互作用强于给定阈值（**T** $_{\mathbf{sel} })$ 的激发组态
状态函数（CSF）才会包含在变分
过程中。被拒绝的 CSF 的效应使用二阶微扰理论估计。目标态的 0$^{\text{th} }$ 阶近似
通过对参考空间组态的对角化得到。进一步的近似是通过另一次选择来减小
参考空间的大小——所有对 0$^{\text{th} }$ 阶态贡献小于第二个阈值（**T** $_{\mathbf{pre} })$
的初始参考都从参考空间中被拒绝。

### 单激发

一个重要方面涉及单激发。如果参考
轨道来自 CASSCF 计算，参考态与单激发之间的矩阵元消失，单激发将
不被选中。然而，它们在微扰理论的四阶及更高阶中有贡献，对于获得光滑的势能
能面和精确的分子性质可能很重要。因此，MRCI 模块的默认模式要求通过标志 `AllSingles =true` 包含所有单
激发。如果参考空间变大，这可能导致冗长的计算！

### 参考空间

第三，MR-CI 模块中的参考空间可以是完全
活性空间（**CAS(n-electrons,m-orbitals)**）或限制活性
空间（**RAS**，后面解释）类型。重要的是要理解
程序使用用户提供的 HOMO-LUMO 间隙附近的轨道来构建参考空间！因此，如果您想放入活性空间的轨道不是从您的 SCF 计算中"自然地"出现在正确位置，您必须使用
"`moread`" 和 "`rotate`" 功能以及 `NoIter` 指令重新排列它们。
选择最有意义和经济的参考空间是多参考计算中最重要的步骤。它*总是*需要
用户的洞察，也需要谨慎，也许还需要一点试错。

### 尺寸一致性

第四，重要的是要理解 CI 型方法*不*是
尺寸一致的。实际上，具有无相互作用 A 和 B 片段的超分子
A-B 的能量不等于孤立 A 和孤立 B 的能量之和。有近似方法可以考虑这一点（**ACPF、AQCC** 和 **CEPA** 方法），但效应
会出现在能量中，包含的电子越多效应越明显。基于微扰理论的方法则*不*是这样，只要参考波函数是尺寸一致的，它们就是尺寸一致的。

### 性能

有许多标志控制 MR-CI 程序的性能。
请参阅第 0 章了解可能的标志、
阈值和截断的描述。最重要的阈值是
T$_{\text{sel} }$ 和 T$_{\text{pre} }$，对于 SORCI 还有
T$_{\text{nat} }$。

(fig22)=
```{figure} ../../images/serine.*
:width: 200px
:align: center

丝氨酸的两性离子形式。
```

对于某些方法（如 ACPF），可以比较
MRCI 模块与 MDCI 模块的性能。MDCI
模块的设计目的是在不引入近似时提供最佳性能。MRCI 模块的编写更多地是
灵活性而非性能。让我们
在一个稍微不平凡的计算中比较两个程序的性能——丝氨酸的两性离子形式。我们比较
选择性 MRCI 方法与无近似的 MDCI 模块。分子大小使得所有四指标积分仍然可以存储
在内存中。

(tab:6)=
:::{table} MRCI 和 MDCI 模块在丝氨酸两性离子形式（14 个原子，133 个基函数）上用 bn-ANO-DZP 基组进行单参考计算的性能比较。
| [**模块**]{style="color: white"} | [**方法**]{style="color: white"} | [**T** $_{\mathbf{sel} }$**(Eh)**]{style="color: white"} | [**时间（秒）**]{style="color: white"} | [**能量（Eh）**]{style="color: white"} |
|:------------------------------------|:------------------------------------|:---------------------------------------------------------:|:---------------------------------------:|:----------------------------------------:|
| **MRCI**                            | ACPF                                |                         10$^{-6}$                         |                  3277                   |               -397.943250                |
| **MDCI**                            | ACPF                                |                             0                             |                  1530                   |               -397.946429                |
| **MDCI**                            | CCSD                                |                             0                             |                  2995                   |               -397.934824                |
| **MDCI**                            | CCSD(T)                             |                             0                             |                  5146                   |               -397.974239                |

:::

选择性 ACPF 计算选择了约 15% 的可能双激发并求解规模为 $\approx$ 360,000 CSF 的久期问题。
MDCI 模块的 ACPF 计算优化了约 250 万个
波函数振幅——而这不是大分子或大
基组！尽管 MDCI 模块不做近似，
它比*选择性* MRCI 模块快两倍，估计比*非选择性* MRCI 模块快 50
倍！对于这类计算中本应使用的更大更精确的基组，这将变得更加明显。选择的误差
在总能量上约为 3 mEh 或 2 kcal/mol。可以期望
至少部分误差在取能量
差时相消。[^1] 更严格的 CCSD 计算比 ACPF 计算大约慢两倍，这似乎是合理的。在这个例子中三激发又增加了大约 2 倍，但对于更大的计算这将增加，因为它对体系大小的标度
更陡。ACPF 能量介于 CCSD 和 CCSD(T) 之间，
这是典型的——ACPF 高估了非连通四重激发的效应，部分补偿了对三重激发的忽略。

这些时间将强烈依赖于您运行计算的体系。尽管如此，您从这个例子中应该得到的信息是：
如果可以使用 MDCI 模块，就用它。

MDCI 模块可以避免对较大体系进行完整积分变换，而 MRCI 模块可以对较大体系使用选择和 RI 近似。
两类计算都将很快变得非常昂贵！近似的 MDCI 计算正在开发中。

### 对称性

MRCI 程序真正利用对称性适应轨道。在这种情况下，MRCI 矩阵可以按照不可约
表示分块并逐个不可约表示对角化。这是一个巨大的
计算优势，允许比不考虑对称性时更容易地收敛到特定的激发
态。

语法 relatively easy。如果您指定：

```orca
newblock 1 *
        nroots 8
        refs cas(4,4) end
        end
```

那么 "\*" 表示这要在点群的每个不可约表示中重复。因此，在 C$_{2v}$ 中，程序会在 C$_{2v}$ 点群的四个不可约表示中各计算 8 个单重态
根，总共得到 32 个态。

或者，您可以在所需的不可约表示中只计算几个根：

```orca
newblock 1 0
        nroots 3
        refs cas(4,4) end
        end
      newblock 1 2
        nroots 5
        refs cas(4,4) end
        end
      newblock 3 1
        nroots 1
        refs cas(4,4) end
        end
```

在这个例子中，我们会在不可约表示 "0"（即 A$_{1})$ 中计算 3 个单重态根，在不可约表示 "2"（即 B$_{1})$ 中计算 5 个根，
然后在不可约表示 1（即 B$_{2})$ 中计算 1 个三重态根。

显然，有对称性和无对称性的结果会略有不同。
这是因为没有对称性时参考空间将
包含属于"错误"对称性的参考，但会带着
属于"正确"对称性的激发组态。因此，不使用对称性的计算会有更多被选中的 CSF，从而能量略低。这似乎是不可避免的。然而，对于设计良好的参考空间，
效应应该不会很大，因为额外的 CSF 不属于一阶相互作用
空间。

(sec:modelchemistries.mrci.example)=
## MR 计算的教程式示例
```{index} MR-CI Tutorial
```

也许 MR-CI 模块最重要的用途是
计算跃迁能和光谱。让我们首先
用 MR-CI 方法加上 Davidson 校正来近似考虑非连通四重
替换的效应，计算甲醛分子的第一个激发单重态和三重态。我们故意为
此计算选择一个 somewhat small 基组，这是合理的，因为我们只看一个
价激发态并想演示原理。

假设我们已经从基态计算知道 H$_{2}$CO 的 HOMO 是氧孤对轨道，LUMO 是
$\pi^{\ast
}$ MO。因此，我们想计算单重态和三重态 n$\to \pi
^{\ast }$ 跃迁，别无其他。因此，我们只需在两个轨道中关联两个电子，这意味着 CAS(2,2) 参考
空间。

```{literalinclude} ../../orca_working_input/C05S10_167.inp
:language: orca
```

这个输入——远超实际所需——需要
一些解释：首先，我们选择带 SVP 基组的标准 RHF 计算，
虽然在 SCF 过程中完全不用 SV/C 拟合基组，我们还是指定了它。在 `%mrci` 块中指定了 MR-CI 过程的所有细节。首先，`EWin`
（`%method frozencore fc_ewin`）选择给定轨道能量范围内要包含在相关处理中的 MO。`CIType`
变量选择多参考处理的类型。有多种选择，
MRCI 只是为此应用选择的一种。

:::{Note} 注意
<i>CIType 语句为其他变量选择若干默认值。因此将此语句放在 MR-CI 块的开头并<u>稍后</u>覆盖程序选择的默认值是一个非常好的主意</i>。如果您将 `CIType` 语句放在它默认选择的某个值之后，您的输入将 simply 被覆盖！
:::

变量 `EUnselOpt` 和 `DavidsonOpt` 控制对 MR-CI 能量的校正。`EUnselOpt` 指定将 MR-CI
能量外推到零阈值 T$_{\text{Sel} }$ 的方式。这里我们
选择在变分步骤*之后*对缺失贡献进行完整的 MR-MP2 计算，即使用参考波函数的弛豫部分作为 MR-PT 的 0$^{\text{th} }$ 阶态。`DavidsonOpt` 控制对更高阶替换效应的估计类型。同样有多种选择，但最常用的（尽管有一些真正的缺点）无疑是
`Davidson1` 选择。标志 `UseIVOs` 指示程序使用
"改进虚轨道"（improved virtual orbitals）。这些是从 Fock 算符的对角化得到的虚轨道，其中一个电子已从价轨道以平均方式移除。因此，这些轨道"看到"的是 $N-1$ 电子势（如所需），并且不像 Hartree-Fock
计算中的标准虚轨道那样弥散。如果您在 MR-CI 模块中输入 DFT 轨道（这完全允许，在某些情况下也推荐，例如对于过渡金属配合物），那么建议关闭该标志，因为 DFT 轨道在这方面已经没问题了。两个
阈值 `Tsel` 和 `Tpre` 上面已经解释过，分别代表一阶相互作用空间和参考空间的选择判据。`Tsel` 以 Eh 为单位，指给定激发 CSF 的二阶 MR-MP2 能量贡献。
10$^{-6}$ Eh 是一个相当好的值。可靠的跃迁能结果从 $\approx 10^{-5}$ 开始；然而，总能量
随该参数收敛相当慢，这是个别选择 CI 过程的最大缺点之一！（见下文）。
`Tpre` 是无量纲的，指给定初始参考空间对角化后给定初始参考的*权重*
（10$^{-4\, }$ 是相当好的值，很少需要更低。激进的值如 10$^{-2}$ 只选择给定目标态的真正领头
组态，可以节省时间。
不推荐中间值）。参数
`MaxMemInt` 和 `MaxMemVec` 告诉程序允许为积分和试验向量及 sigma 向量分别分配多少内存（MB）。

标志 `IntMode` 告诉程序执行完整的积分变换。对于少于约
100--200 个 MO 的小体系这是可能的。在这种情况下它能显著加快计算。对于较大的分子您*必须*将此标志设为 `RITrafo`，这意味着积分使用 RI 近似即时重算，这更昂贵但也是进行计算的唯一方式。要在可能的模式之间切换，请使用：

```orca
%mrci  IntMode FullTrafo # exact 4 index transformation
               RITrafo   # use auxiliary basis sets
```

对于小分子或如果需要高精度的总能量，使用精确的四指标变换要好得多。
限制是超过约 200--300 个 MO 时磁盘空间或主内存会耗尽。

变量 `Solver` 可以是 `diag`（用于 Davidson 型对角化）
或 `DIIS`（用于多根 DIIS 型处理）。

```orca
%mrci  Solver Diag   # Davidson solver
              DIIS   # Multiroot DIIS
```

对于 CI 方法，diag 求解器通常更可取。对于像 ACPF 这样包含非线性项的方法，DIIS 是必需的。

输入中接下来是定义要构建和对角化的 CI 矩阵。每个多重度定义 CI 矩阵的一个*块*，分别指定。这里我们要求两个块——单重态和三重态。一般语法是：

```orca
NewBlock Multiplicity Irrep
         NRoots 1           # Number of roots to determine
         Excitations cisd   # Type of excitations
         Refs CAS(NEl,NOrb) end  # Reference space def.
         end                # Finalize the block
```

现在所有输入都已理解，让我们看看这个计算的结果：

SCF 计算之后发生的第一件事是
程序 `orca_ciprep` 准备冻核 Fock 矩阵和改进虚
轨道。从输出可以看到 IVO 的能量。在这种情况下 LUMO 降到 --8.2 eV，比 SCF 值 $+$3....
eV 合理得多。同时，该 MO 的形状将更加现实，这很重要，因为这个轨道在参考空间中！

```orca
------------------------------------------------------------------------------
                             ORCA CI-PREPARATION
------------------------------------------------------------------------------

Reading the GBW file               ... done
Symmetry usage                     ... ON

One-Electron Matrix                ... test1.H.tmp
GBW-File                           ... test1.gbw
Improved virtual orbitals          ... test1.ivo
First MO in the CI                 ... 2
Internal Fock matrix               ... test1.fi.tmp
LastInternal Orbital               ... 6
Integral package used              ... LIBINT
Reading the GBW file               ... done
Symmetry usage                     ... ON

Reading the one-electron matrix    ... done
Forming inactive density           ... done
Forming averaged valence density   ...
Scaling the occupied orbital occupation numbers
First MO                            ... 2
Last MO                             ... 7
Number of electrons in the range    ...    12
Scaling factor                      ... 0.917

done
Forming internal density           ... done
Forming Fock matrix/matrices       ...
Nuclear repulsion    ...    31.371502
Core repulsion       ...    31.371502
One-electron energy  ...  -114.942080
Fock-energy          ...   -94.993431
Final value          ...   -73.596254
done
Modifying virtual orbitals         ...
Last occupied MO               ...    7
Total number of MOs            ...   38
Number of virtual MOs          ...   30
Doing diagonalization with symmetry
The improved virtual eigenvalues:
    0: -0.2955 au   -8.041 eV    2- B2
    1: -0.0701 au   -1.907 eV    6- A1
    2: -0.0176 au   -0.479 eV    3- B1
    3:  0.0064 au    0.175 eV    7- A1
    4:  0.2922 au    7.951 eV    8- A1
    5:  0.2948 au    8.021 eV    3- B2
    6:  0.3836 au   10.439 eV    4- B1
    7:  0.4333 au   11.790 eV    9- A1
    8:  0.4825 au   13.128 eV    5- B1
    9:  0.5027 au   13.680 eV   10- A1
   10:  0.7218 au   19.642 eV   11- A1
   11:  0.8351 au   22.723 eV    4- B2
   12:  0.9371 au   25.501 eV    6- B1
   13:  1.0265 au   27.933 eV    1- A2
   14:  1.1141 au   30.317 eV   12- A1
   15:  1.2869 au   35.017 eV    5- B2
   16:  1.4605 au   39.743 eV    7- B1
...

done
Transforming integrals             ... done
Storing passive energy             ... done (    -73.59625384 Eh)
Transforming internal FI           ... done
             .... done with the Frozen Core Fock matrices
```

下一步是将电子-电子排斥积分变换到 MO 基组：

```orca
-------------------------
SHARK HALF TRANSFORMATION
-------------------------

Number of basis functions                ...     38
Number of operators                      ...      1
   Operator  0:    2-  37

Integral generator used                  ... SHARK
Contraction scheme used                  ... SEGMENTED CONTRACTION
MaxCore in resort                        ...    256 MB

Half transformed integrals for op=   0   ... test1.SHARK_MNPQ0.tmp
Resorted half transformed integrals      ... test1.JAO.tmp
Starting integral generation + half trafo...
Half trafo (segmented) done. Total time =0.1 sec integrals=0.0 sec trafo=0.0 sec
Starting integral resorting              ... done (  0.0 sec)

SHARK half integral transformation done. Total time =  0.1 sec.


-------------------
FULL TRANSFORMATION
-------------------

Processing MO  10
Processing MO  20
Processing MO  30
Full transformation done
Number of integrals made            ...       222111
Number of integrals stored          ...        59070
Timings:
Time for first half transformation  ...     0.068 sec
Time for second half transformation ...     0.014 sec
Total time                          ...     0.086 sec
```

这将产生 `orca_mrci` 所需的几个额外磁盘文件。
然后程序告诉您本次 MRCI 运行将处理哪些多重度：

```orca
------------------
CI-BLOCK STRUCTURE
------------------

Number of CI-blocks                ... 3

===========
CI BLOCK 1
===========
Multiplicity             ...   1
Irrep                    ...   0
Number of reference defs ...   1
  Reference   1: CAS(2,2)

Excitation type          ... CISD
Excitation flags for singles:
    1 1 1 1
Excitation flags for doubles:
    1 1 1 / 1 1 1 / 1 1 1

===========
CI BLOCK 2
===========
Multiplicity             ...   1
Irrep                    ...   1
Number of reference defs ...   1
  Reference   1: CAS(2,2)

Excitation type          ... CISD
Excitation flags for singles:
    1 1 1 1
Excitation flags for doubles:
    1 1 1 / 1 1 1 / 1 1 1

===========
CI BLOCK 3
===========
Multiplicity             ...   3
Irrep                    ...   1
Number of reference defs ...   1
  Reference   1: CAS(2,2)

Excitation type          ... CISD
Excitation flags for singles:
    1 1 1 1
Excitation flags for doubles:
    1 1 1 / 1 1 1 / 1 1 1

        --------------------------------------------------------------------
        -------------------- ALL SETUP TASKS ACCOMPLISHED ------------------
        --------------------      (     0.139 sec)        ------------------
        --------------------------------------------------------------------
```

现在所有设置任务都已完成，MRCI 计算本身开始了。

```orca
###################################################
#                                                 #
#                       M R C I                   #
#                                                 #
# TSel    =   1.000e-06 Eh                        #
# TPre    =   1.000e-02                           #
# TIntCut =   1.000e-10 Eh                        #
# Extrapolation to unselected MR-CI by full MP2   #
# DAVIDSON-1 Correction to full CI                #
#                                                 #
###################################################


---------------------
INTEGRAL ORGANIZATION
---------------------

Reading the one-Electron matrix   ... done
E0 read was -73.596253835266
Reading the internal Fock matrix
    ... assuming it to be equal to the one-electron matrix !!! done
Preparing the integral list       ... done
Loading the full integral         ... done
Making the simple integrals       ... done

                  ***************************************
                  *              CI-BLOCK  1            *
                  ***************************************

Configurations with insufficient # of SOMOs WILL be rejected
Building a CAS(2,2) for multiplicity 1 and irrep=A1
Reference Space:
 Initial Number of Configurations :      2
 Internal Orbitals :    2 -    6
 Active Orbitals   :    7 -    8
 External Orbitals :    9 -   37
The number of CSFs in the reference is 2
Calling MRPT_Selection with N(ref)=2
```

第一步是对角化参考空间。从这个 CI 中，
用 `Tpre` 选择最重要的组态：

```orca
------------------
REFERENCE SPACE CI
------------------

 Pre-diagonalization threshold                 : 1.000e-02
Warning: Setting NGuessMat to 512
N(ref-CFG)=2 N(ref-CSF)=2

                       ****Iteration    0****
   Lowest Energy          :  -113.779221580786
   Maximum Energy change  :   113.779221580786 (vector 0)
   Maximum residual norm  :     0.000000000000

      *** CONVERGENCE OF RESIDUAL NORM REACHED ***
Reference space selection using TPre= 1.00e-02

    ... found 1 reference configurations (1 CSFs)
        ... now redoing the reference space CI ...

Warning: Setting NGuessMat to 512
N(ref-CFG)=1 N(ref-CSF)=1

                       ****Iteration    0****
   Lowest Energy          :  -113.778810013503
   Maximum Energy change  :   113.778810013503 (vector 0)
   Maximum residual norm  :     0.000000000000

      *** CONVERGENCE OF RESIDUAL NORM REACHED ***
```

在这种情况下，CAS 空间只有 2 个正确对称性适应的 CSF，其中之一（闭壳层行列式）被选中。一般来说，
较大的 CAS 空间通常携带大量不必要的 CSF，这些 CSF 对任何事情都不需要，这时选择对于
减少计算量很重要。第二个参考空间 CI 的结果被打印出来：

```orca
----------
CI-RESULTS
----------

The threshold for printing is  0.30 percent
The weights of configurations will be printed. The weights are summed over
all CSFs that belong to a given configuration before printing

STATE   0:  Energy=   -113.778810014 Eh RefWeight=  1.0000  0.00 eV      0.0 cm**-1
      1.0000  : h---h---[20]
```

**`Energy`** 是以 Eh 为单位的总能量。在当前情况下我们可以与 SCF 能量 `-113.778810014 Eh` 比较，发现参考空间 CI 能量相同，这是必然的，因为最低态与参考空间重合。**`RefWeight`** 给出参考
组态在 CI 态中的权重。在当前情况下是 1.0，因为只有参考组态。数字 `1.000` 是 CI 向量中以下组态的权重。组态 **`h—h—[20]p—p— `** 的描述
如下理解：[^2] 活性轨道的占据
显式地在方括号中给出。由于 HOMO 轨道是 SCF 过程中的第 7 号，
在当前示例中这指 MO 7 和 8，因为我们有两个
活性轨道。`2` 表示双占据，`0` 表示空。任何出现在 `h` 之后的数字（代替 `—`）给出空穴所在的
内部轨道指标。类似地，`p` 之后的任何数字给出粒子所在的
虚（外部）MO 指标。因此 `h—h—[20] ` 是闭壳层组态，它
与 SCF 组态重合——这当然在预料之中。第二个根（在 CI-Block 2 中）`h—h—[11] ` 相比之下
指一个电子从 HOMO 提升到 LUMO 的组态，因此是我们想计算的
目标态。一切顺利，我们可以继续看
输出。

下一步是生成激发组态并基于 `Tsel` 进行选择：

```orca
------------------------------
MR-PT SELECTION TSel= 1.00e-06
------------------------------


Setting reference configurations WITH use of symmetry
Building active patterns WITH use of symmetry

Selection will be done from 1 spatial configurations
Selection will make use of spatial symmetry
 ( 0) Refs        : Sel:     1CFGs/       1CSFs Gen:           1CFGs/      1CSFs  (0.000 sec)
Building active space densities          ...        0.002 sec
Building active space Fock operators     ...        0.000 sec
 ( 1) (p,q)->(r,s): Sel:     1CFGs/       1CSFs Gen:           1CFGs/      1CSFs  (0.000 sec)
 ( 2) (i,-)->(p,-): Sel:     1CFGs/       1CSFs Gen:           1CFGs/      1CSFs  (0.000 sec)
 ( 3) (i,j)->(p,q): Sel:     8CFGs/       8CSFs Gen:           8CFGs/      8CSFs  (0.000 sec)
 ( 4) (i,p)->(q,r): Sel:     0CFGs/       0CSFs Gen:           1CFGs/      1CSFs  (0.000 sec)
 ( 5) (p,-)->(a,-): Sel:     8CFGs/       8CSFs Gen:           8CFGs/      8CSFs  (0.000 sec)
 ( 6) (i,-)->(a,-): Sel:    52CFGs/      52CSFs Gen:          52CFGs/     52CSFs  (0.000 sec)
 ( 7) (i,j)->(p,a): Sel:    95CFGs/     166CSFs Gen:          96CFGs/    167CSFs  (0.000 sec)
 ( 8) (i,p)->(q,a): Sel:    21CFGs/      42CSFs Gen:          22CFGs/     44CSFs  (0.000 sec)
 ( 9) (p,q)->(r,a): Sel:     3CFGs/       3CSFs Gen:           5CFGs/      5CSFs  (0.000 sec)
 (10) (i,p)->(a,b): Sel:   555CFGs/    1082CSFs Gen:         584CFGs/   1139CSFs  (0.001 sec)
 (11) (p,q)->(a,b): Sel:   124CFGs/     124CSFs Gen:         148CFGs/    148CSFs  (0.000 sec)
 (12) (i,j)->(a,b): Sel:  1688CFGs/    2685CSFs Gen:        1887CFGs/   2947CSFs  (0.001 sec)

Selection results:
Total number of generated configurations:       2814
Number of selected configurations       :       2557 ( 90.9%)
Total number of generated CSFs          :       4522
Number of selected CSFS                 :       4173 ( 92.3%)

The selected tree structure:
Number of selected Internal Portions       :     11
Number of selected Singly External Portions:     27
   average number of VMOs/Portion          :   6.39
   percentage of selected singly externals :  22.83
Number of selected Doubly External Portions:     21
   average number of VMOs/Portion          : 107.59
   percentage of selected doubly externals :  27.76
```

这里程序遍历各类激发。对于每个激发，它产生激发组态（CFGs）以及组态内可能的线性无关自旋函数（CSFs）。然后它计算与收缩
$0^{th}$ 阶根的相互作用，如果最大二阶微扰能大于或等于 `Tsel`，则将属于给定 CFG 的所有 CSF 包含在变分空间中。在当前情况下
产生了 $\approx$136,000 个 CSF，其中 25% 被
选中。对于较大的分子和基组，产生 $10^{9}$--$10^{10}$ 个组态并不罕见，那时别无选择只能选择远小于 20% 的比例。供您参考，程序还会在选择后打印每个态的总能量：

```orca
Diagonal second order perturbation results:
State      E(tot)           E(0)+E(1)     E2(sel)      E2(unsel)
             Eh                Eh           Eh           Eh
----------------------------------------------------------------
 0    -114.108350270   -113.778810014    -0.329433    -0.000107
```

如果需要，您可以忽略此输出。在微扰
过程发散的情况（并不罕见！）下，总能量看起来
奇怪——不用担心——随后的变分计算仍然
没问题。二阶微扰能在此分为选中部分 `E2(sel)` 和未选中组态提供的部分 `E2(unsel)`。根据 `EUnselOpt` 的模式，该值可能
稍后被用作未选中 CSF 能量贡献的估计。[^3]

现在我们在 CI 块 1 的变分空间中有 $\approx$ 4,200 个 CSF，继续使用 Davidson 或 DIIS 型过程对角化这些 CSF 上的哈密顿量：

```orca
------------------------
DAVIDSON-DIAGONALIZATION
------------------------

Dimension of the eigenvalue problem            ...   4173
Number of roots to be determined               ...      1
Maximum size of the expansion space            ...      4
Maximum number of iterations                   ...     35
Convergence tolerance for the residual         ...    1.000e-06
Convergence tolerance for the energies         ...    1.000e-06
Orthogonality tolerance                        ...    1.000e-14
Level Shift                                    ...    0.000e+00
Constructing the preconditioner                ... o.k.
Building the initial guess                     ... o.k.
Number of trial vectors determined             ...      4


                       ****Iteration    0****
   Size of expansion space: 3
   Lowest Energy          :  -113.937028067251
   Maximum Energy change  :   113.937028067251 (vector 0)
   Maximum residual norm  :     0.741727830968

                       ****Iteration    1****
   Size of expansion space: 4
   Lowest Energy          :  -114.082265676116
   Maximum Energy change  :     0.145237608865 (vector 0)
   Maximum residual norm  :     0.012707561344
   Rebuilding the expansion space

                       ****Iteration    2****
   Size of expansion space: 2
   Lowest Energy          :  -114.085350429118
   Maximum Energy change  :     0.003084753001 (vector 0)
   Maximum residual norm  :     0.002880697397

                       ****Iteration    3****
   Size of expansion space: 3
   Lowest Energy          :  -114.086043274125
   Maximum Energy change  :     0.000692845007 (vector 0)
   Maximum residual norm  :     0.000098595378

                       ****Iteration    4****
