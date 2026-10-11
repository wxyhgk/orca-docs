<a id="sec:essentialelements.shark"></a>
# SHARK 积分库与任务驱动器（SHARK Integral Package and Task Driver）

## 前言（Preface）

从 ORCA 5.0 开始，程序处理积分以及与积分相关的任务（如构建 Fock 矩阵）
的方式发生了非常大的变化。SHARK 是一个强大而高效的基础设施，
极大地简化了这些任务的处理。这使得开发人员能够编写高度精简的代码，
兼具最优性能和很高的可靠性。与 ORCA 5.0 之前 ORCA 处理积分的方式相比，
有数万行代码——往往是程序中密切相关部分的重复或近乎重复——得以删除。
从用户的角度来看，与 ORCA 4.2.1 及更早版本相比，程序输入输出方面
可见的变化相对有限。然而在底层，变化是广泛而巨大的，
并将确保 ORCA 的基础设施保持现代化，非常适合科学计算的未来。

SHARK 为 ORCA 用户带来的好处有：

1.  提升了代码效率，且在所有程序任务中保持一致。特别是复杂的双电子积分
    （two-electron integrals），例如 GIAO 框架下、双电子自旋-轨道耦合
    （spin-orbit coupling）以及双电子自旋-自旋耦合（spin-spin coupling）
    积分，其处理效率都得到了极大的提升。此外，积分的"消化"
    （integral digestion）也大为改进，对那些需要同时构建多个 Fock 矩阵的
    计算——例如 CIS/TD-DFT、解析 Hessian 或响应性质计算——有非常大的益处。

2.  提升了代码可靠性，因为所有积分现在都通过一个经过良好调试的公共接口运行。

3.  缩短了开发时间。新的基础设施对程序员非常友好，
    编写使用 SHARK 的新代码比过去快得多。

4.  SHARK 对基组（basis sets）的处理远好于旧的基础设施。无论所用基组
    采用分段收缩（segmented contraction）、一般收缩（general contraction）
    还是部分一般收缩（partial general contraction）都无关紧要，
    因为针对每一类基组，算法都已自始至终做了精心优化。

## SHARK 积分算法

SHARK 的基石之一是一种新的积分算法，能够高效地求值分子积分。
该算法基于优美的 McMurchie-Davidson 算法，对于给定的双电子积分，
可导出如下方程：

$$

({\mu _A}{\nu _B}|{\kappa _C}{\tau _D}) = C\sum\limits_{tuv} { E_t^{\mu \nu ;x}E_u^{\mu \nu ;y}E_v^{\mu \nu ;z} } \sum\limits_{t'u'v'} { E_{t'}^{\kappa \tau ;x}E_{u'}^{\kappa \tau ;y}E_{v'}^{\kappa \tau ;z}{{( - 1) }^{t' + u' + v'} }{R_{t + t',u + u',v + v'} }}

$$

其中

$$

C = 8{\pi ^{{\raise0.5ex\hbox{$\scriptstyle 5$}
\kern-0.1em/\kern-0.15em
\lower0.25ex\hbox{$\scriptstyle 2$} }} } = { 139.947346620998902770103}

$$

以及本原 Cartesian Gaussian 基函数（primitive Cartesian Gaussian basis
functions）$\{\mu_A\}$，这里 $A$ 是原子中心，基函数 $\mu$ 位于位置
${{{\mathbf{R} }_A} }$。为了粗略了解 McMurchie-Davidson 算法的内容，
考虑两个分别以原子 $A$ 和 $B$ 为中心的未归一化本原 Gaussian：

$$

\begin{aligned}
{ G_A} &= x_A^iy_A^jz_A^k\exp ( - \alpha R_A^2) \\
  { G_B} &= x_B^{i'}y_B^{j'}z_B^{k'}\exp ( - \beta R_B^2)\end{aligned}

$$

借助 Gaussian 乘积定理（Gaussian product theorem），
两个指数项可以直接改写为：

$$

\exp ( - \alpha R_A^2)\exp ( - \beta R_B^2) = { K_{AB} }\exp\Bigl( - (\alpha  + \beta)r_P^2\Bigr)

$$

其中

$$

{K_{AB} } = \exp\left( - { \textstyle{{\alpha \beta } \over{ \alpha  + \beta } }}{\left|{ {{\mathbf{R} }_A} - { {\mathbf{R} }_B} } \right|^2}\right)

$$
$r_P^2 = { \left|{ {\mathbf{r} } - { {\mathbf{R} }_P} } \right|^2}$ 是
相对于该点的电子位置

$$

{{\mathbf{R} }_P} = { \textstyle{\alpha  \over{ \alpha  + \beta } }}{{\mathbf{R} }_A} + { \textstyle{\beta  \over{ \alpha  + \beta } }}{{\mathbf{R} }_B}

$$

新 Gaussian 即以该点为中心。McMurchie 和 Davidson 的巧妙发明在于认识到：
两个本原 Cartesian Gaussian 相乘所产生的复杂多项式，
可以用 Hermite 多项式（Hermite polynomials）$\left\{\Lambda  \right\}$
很好地写出。在一维情况下：

$$

x_A^ix_B^{i'} = \sum\limits_{t = 0}^{i + i'} { {E_t} }

$$

于是：

$$

{G_A}{G_B} = { K_{AB} }\sum\limits_{t = 0}^{i + i'} { E_t^{AB} } \sum\limits_{u = 0}^{j + j'} { E_u^{AB} } \sum\limits_{v = 0}^{k + k'} { E_v^{AB}\Lambda _{tuv}^{AB} }

$$

其中

$$

\Lambda _{tuv}^{AB} = { \left({ {\partial  \over{ \partial{ X_P} }} } \right)^{\!\!t} }{\left({ {\partial  \over{ \partial{ Y_P} }} } \right)^{\!\!u} }{\left({ {\partial  \over{ \partial{ Z_P} }} } \right)^{\!\!v} }\exp\Bigl( - (\alpha  + \beta )R_P^2\Bigr)

$$

这意味着原始的四中心积分被约化为 Hermite Gaussian 函数上双中心积分之和。
这些积分记作

$$

{R_{t + t',u + u',v + v'} } = \int{ \int{ \Lambda _{tuv}^{AB}({{\mathbf{r} }_1};{{\mathbf{R} }_P})\Lambda _{t'u'v'}^{CD}({{\mathbf{r} }_2};{{\mathbf{R} }_Q})r_{12}^{ - 1}d{{\mathbf{r} }_1}d{{\mathbf{r} }_2} } }

$$

有了这些定义，就可以把 McMurchie Davidson 算法理解为三个步骤：
1.  将 Bra 函数乘积变换到 Hermite Gaussian 基
2.  将 Ket 函数乘积变换到 Hermite Gaussian 基
3.  计算 Hermite Gaussian 电子排斥积分
SHARK 的核心认识是：这三个步骤可以通过一个三重矩阵乘积高效地执行：\qquad \text{({\mu _A}{\nu _B}|{\kappa _C}{\tau _D})}

$$

= { \left({ {{\mathbf{E} }^\text{bra} }{\mathbf{R} }{{\mathbf{E} }^\text{ket} }} \right)_{\mu \nu ,\kappa \tau } }

$$

这里 ${{{\mathbf{E} }^\text{bra} }}$ 和 ${{{\mathbf{E} }^\text{ket} }}$
分别收集 bra 侧和 ket 侧壳层乘积（shell product）所有成员的 $E$ 系数
（$E_{\mu \nu ,tuv}^\text{bra}$ 和 $E_{\kappa\tau,tuv}^\text{ket}$），
${\mathbf{R} }$ 则收集 Hermite Gaussian 函数上的积分
（${R_{tuv,t'u'v'} }$）。

这种表述有许多优点：

1.  积分被因子化，使得各步骤可以彼此独立地进行。例如，E 矩阵可以在
    计算开始时算出，并在需要时重复使用。它们的存储不成问题。

2.  矩阵乘法能够极其高效地形成目标积分，并把硬件驱动到峰值性能。

3.  本原积分的收缩以及从 Cartesian 基到球谐函数（spherical Harmonics）基
    的变换等步骤，都可以折叠进 E 矩阵的定义中，从而得到极其高效的代码，
    几乎没有短循环带来的额外开销。

4.  编写积分变得非常容易和高效。其他类型的积分以及导数积分也都可以
    用同样的方式轻松处理。另外，RI 近似所需的双指标和三指标排斥积分
    也可以很方便地用这种方式表述。

5.  单电子积分同样很容易用这种方法完成。

还有大量技术细节我们不会在本手册中描述，本手册只打算给出算法的要旨。

## SHARK 与 libint

直到 ORCA 4.2.1，ORCA 几乎完全依赖 libint2 积分库，该库以高效和强大著称。
从 ORCA 5.0 开始，SHARK 和 libint 都被用于积分求值，并且 libint 已完全
集成到 SHARK 编程环境中。只在其中一个包中可用的积分就用该包来完成
（例如 GIAO、SOC 和自旋-自旋积分用 SHARK；F12 或二阶导数积分用 libint）。
对于两个包都可用的积分，程序会审慎地选择最高效的路径。
采用这种混合方式的原因如下：

SHARK 积分算法在高角动量函数（$l>2$；$d$ 函数）上表现最佳，
此时矩阵乘法的高效率能带来非常大的计算收益。比如四个 $f$ 或 $g$
函数上的积分，其计算速度比传统积分算法快得多（最高可达五倍）。
然而对于低角动量，矩阵乘法会带来额外开销，
而且 McMurchie Davidson 算法已知并非浮点运算次数（FLOP count）最优的算法。
在某种程度上，这是通过为低角动量使用高度精简、表现极佳的例程来弥补的。
不过在中等角动量处仍存在性能损失——此时矩阵乘法的效率尚未体现，
而积分又复杂到难以手工编码。这些积分用 libint 表现最好，
因此程序默认会选择 libint 来执行这类积分批次。

## 基组类型

分子积分求值的一个重要方面是 Gaussian 基组中所含的收缩（contraction）类型。
最一般的基组类型见于"一般收缩"（general contraction）方案。
这里把给定角动量的所有本原 Gaussian 基函数收集在一个向量
$\left\{\phi  \right\}$ 中。一般而言，所有本原函数都对该角动量下
所有基函数 $\left\{\varphi  \right\}$ 有贡献。因此我们可以写出：

$$

\left(\begin{array}{l}
          \varphi_1 \\
          \varphi_2 \\
          ~\vdots \\
          \varphi_{{N_l} }
        \end{array}\right) =
  \left(\begin{array}{llll}{ {d_{11} }} & { {d_{11} }} &  \cdots  & { {d_{1{M_l} }} }  \\
   { {d_{21} }} & { {d_{21} }} &  \cdots  & { {d_{2{M_l} }} }  \\
    ~\vdots  &  ~\vdots  &  \ddots  &  ~\vdots   \\
   { {d_{{N_l}1} }} & { {d_{{N_l}2} }} &  \cdots  & { {d_{{N_l}{M_l} }} }
        \end{array}\right)        \left(\begin{array}{l}
          \phi_1 \\
          \phi_2 \\
          ~\vdots \\
          \phi_{{M_l} }
        \end{array}\right)

$$

其中 ${N_l}$ 和 ${M_l}$ 分别是实际基函数和本原函数的数目。
通常本原函数的数目远大于基函数的数目。矩阵 ${\mathbf{d} }$
收集各角动量的收缩系数。遵循这种收缩模式的典型基组是原子自然轨道
（atomic natural orbital, ANO）基组。它们通常基于很大的 Gaussian
本原集合。这类基组对积分包提出了很高的要求，因为需要生成大量
本原 Gaussian 基函数上的积分。如果积分包没有利用一般收缩，
那么这种积分求值就会高度冗余：相同的积分会被计算 ${N_l}$ 次
（因此，四个一般收缩壳层上的积分会被冗余地生成 ${N_l^4}$ 次）。
SHARK 对它能生成的所有单电子和双电子积分都充分利用了一般收缩。
在这里，积分因子化的独特优势得到了充分发挥：给定原子四元组/角动量
四元组的所有积分四元组，只需两次大矩阵乘法就能高效生成。

与一般收缩相反的是分段收缩（segmented contraction）。
这里每个基函数涉及若干本原函数：

$$

{\varphi _\mu } = \sum\limits_k { {d_{k\mu } }{\phi _k} }

$$

通常，出现在一个基函数收缩中的 ${{\phi _k} }$ 不会出现在任何其他基函数中。
这种形式的典型基组是 Karlsruhe 小组的 "def2" 基组。它们很容易被大多数
积分包处理，在这种情况下 SHARK 和 libint 都很高效。

第三类基组见于一般收缩与分段收缩相结合的情形。这类基组例如相关一致
（correlation consistent, cc）基组。我们称这类基组为"部分一般收缩"
（partially generally contracted）。在这类基组中，一部分基函数是一般
收缩的（例如主族元素的 s 和 p 函数），而其他基函数（如极化函数、
弥散函数、核心相关函数）则不是一般收缩的。鉴于其复杂的结构，
很难充分利用这类基组。在 ORCA 5 中，提供了专门的代码把基组变换为
一个不含任何冗余的中间基组，从而使 SHARK 或 libint 都能以峰值性能运行。

在评估不同积分算法的效率与精度时，显然，如果构造得当，
分段基组能带来最高的效率。对于这类基组，预筛选（pre-screening）
——它是任何积分直接算法中的关键步骤——表现最好。
每个基函数所能达到的最高精度则见于一般收缩基组。不过在这种情况下，
预筛选会变得相当低效，因为它只能在原子/角动量组合的层面上进行，
而不能在单个壳层四元组的层面上进行。因此，一旦某个原子/角动量组合
产生了任何不可忽略的积分，该组合的所有积分都需要计算。这造成了
相当可观的额外开销。因此，SCF 计算永远无法达到分段基组那样的效率。
如果这无关紧要——例如，因为后续的耦合簇（coupled cluster）或 MRCI
计算主导了计算时间——那么一般收缩非常值得尝试。
对于部分一般收缩，我们的算法在 SCF 计算中的效率与分段收缩非常接近。
不过，由于中间基组比原始轨道基更大，在某些任务类型中可能会带来
一定的性能损失。

## 任务驱动器（Task drivers）

在传统算法中，量子化学程序往往包含大量对基组壳层嵌套循环的实例，
调用积分包，并为给定任务"消化"积分。这些步骤虽然不可避免，
但反复编程既费力又容易出错。此外，例如在收缩或对称性处理方面的改进，
需要在许多不同的地方实现。在 SHARK 基础设施中，所有这些都是不必要的，
因为它以面向对象（object-oriented）的方式编程，程序员无需关心任何细节。
因此，开发人员只需编写简短的代码段，把生成的积分分发到他们所需的
任何数据结构中，而 SHARK 接口则处理所有技术细节，
并触发其底层那套精密高效的机制。

在这种情况下，ORCA 的未来将是：由 SHARK 负责几乎所有计算密集、
繁琐的任务，而 ORCA 负责组织和触发所有这些任务。ORCA 与 SHARK
通过一个精简且定义良好的接口通信，以交换必要的数据。通过这种方式，
就建立起了一个现代化、高效、易用且易于维护的开发环境。

<a id="sec:essentialelements.shark.keywords"></a>
## SHARK 用户界面

虽然 SHARK 是一套庞大而复杂的机制，但我们刻意把接口保持得尽可能
简明、简单。

在简单输入行（simple input line）中有开启（默认）或关闭 SHARK 的关键词：

```orca
! UseShark
! NoUseShark
```

!!! warning "6.0.0"
    旧版（非 SHARK 代码）已从程序中移除，因此在需要积分的计算中
    （例如，与 MM 计算不同），SHARK 已无法被禁用。

此外，还有一些标志可以在 `%shark` 块中设置：

```orca
%shark
 UseGeneralContraction false  # turns general contraction algorithm on or
                              # off. There normally is no need to set this
                              # flag since the program will find the
                              # contraction case automatically
 Printlevel 1                 # Amount of output generated. Choose 0 to
                              # suppress output and 2 for more output.
                              # Everything else is debug level printing and
                              # will fill your harddrive very quickly with
                              # unusable information
 PartialGCFlag -1             # Let the program decide whether to use PGC
                0             # do not use it
                1             # Enforce PGC (even for ANO bases)
 FockFlag SHARK_libint_hybrid # default: best of both worlds
          force_shark         # Force Shark where possible
          force_libint        # Force libint where possible
 RIJFlag  RIJ_Auto            # default: program decides the best way
          Split_rij           # new SHARK Split-RI-J algorithm
          Split_rij_2003      # Highly efficient re-implementation of the
                              # Original 2003 algorithm. Mostly used!
          rij_regular         # Use traditional 3 center integrals
                              # (not recommended)
end
```
