```{index} EOM-CCSD, Excited States via EOM-CCSD
```

(sec:spectroscopyproperties.eom)=
# 通过 EOM-CCSD 计算激发态（Excited States via EOM-CCSD）

前面描述的许多方法都基于单激发框架。为了更精确的处理，
还应考虑双激发。运动方程（equation of motion，EOM）CCSD 方法
（以及密切相关的线性响应 CC 方法系列）在耦合簇框架内
基于单激发和双激发，为描述激发态、电离态和电子附着态
提供了精确的途径。

(sec:spectroscopyproperties.eom.theory)=
## 理论（Theory）
```{index} EOM-CCSD Theory
```

EOM 波函数按如下方式参数化

$$\mathcal{R}|\Psi_{CC}\rangle,$$

即通过线性激发算符 $\mathcal{R}$ 作用于耦合簇基态波函数
$\Psi_{CC}$。这里，对于激发能问题，$\mathcal{R}$ 是粒子数守恒算符。
然而，对于电离或电子附着问题则不然，此时 $\mathcal{R}$
分别是净湮灭或净产生算符。基态耦合簇 T 振幅从 CCSD 计算获得，
我们的任务是获得 $\mathcal{R}$。请注意，由于 CC 哈密顿量是非对称的，
计算性质还需要左手解（$\mathcal{L}$）。然而，对于激发、
电离或电子附着能的计算，获得右手解（$\mathcal{R}$）就足够了。
原则上，这通过构造哈密顿量并对其进行对角化来获得能量期望值。

实际上，CCSD 哈密顿量矩阵的规模大得难以处理，因此
人们设计了多种方法来获得其最低的几个本征值和本征态。
其中最流行的方法之一是 Davidson 方法，可概括如下：

-   构造正交试探向量 $C$ 的初始猜测。

-   计算 sigma 向量 $\sigma=HC$。

-   构造模型哈密顿量 $\mathcal{H}=C^T\sigma$。

-   对角化 $\mathcal{H}$：$\mathcal{E=U}^T\mathcal{HU}$。

-   计算 Ritz 向量 $X=C\mathcal{U}$。

-   计算残差 $R=X\mathcal{E}-\sigma\mathcal{U}$，检查
    收敛：若是，则将 $X,\mathcal{E}$ 作为解。

-   预条件：$T=MR$（预条件子 $M$ 有多种可能的选择）。

-   检查添加新的试探向量是否会超过试探向量的最大数目：

    -   若否，将 $T$ 加到 $C$ 中，并对联合集合进行正交归一化

    -   若是，则将 $X$ 设为 $C$（若 $H$ 非对称则进行正交归一化）；
        然后添加 $T$ 并正交归一化

上述方法的优点在于，只需显式计算并存储 sigma 向量，
而无需完整哈密顿量。

也可以使用 EOM-CCSD 方法的低标度版本，它依赖于耦合簇
相似变换哈密顿量的微扰截断。目前，仅对闭壳层分子（RHF）
提供二阶截断版本（CCSD(2) 近似）。不过，最好使用基于 PNO 的实现，
因为它具有 EOM-CCSD(2) 的成本，但精度与正则 EOM-CCSD 相当。

(sec:spectroscopyproperties.eom.theory.initguess)=
### 初始猜测（Initial Guess）

目前 RHF EOM 实现中的初始猜测是构造一定维度的 CIS 哈密顿量
并对其进行对角化。根根据哈密顿量对角元素的能量顺序预选。
在 UHF 情形下，猜测由 UHF CIS 计算的解构造。
初始猜测中根的数目确定为 EOM 所需根数（`NRoots`）的 20 倍
（若 `NDav` 为 20 或更小），否则设为 `NDav` 乘以 EOM 根数。
如果参数 `NInits` 大于零，则初始猜测根的数目将设为该参数
乘以 `NRoots`。根的最大可能数目是完整的 CIS 维度
（$N_ON_V$（RHF）或
$N_{O_{\alpha} }N_{V_{\alpha} } + N_{O_{\beta} }N_{V_{\beta} }$（UHF））。
在增加初始猜测向量数目的同时，应记住这对应于对角化一个
维度递增的矩阵。例如，如果 `NRoots` 为 10，则默认在初始猜测中
考虑 200 个根（除非超过 CIS 空间的大小），或者如果 `NInits`
设为 100，则猜测中将有 1000 个根。在某些情况下，EOM 计算的根
可能不是最低的，而是其中一些可能被某些"更容易"找到的更高根所取代。
在这种情况下，增加 `NRoots` 或 `NInits` 以收敛到正确的根可能会有帮助。
通过将 `FollowCIS` 设为 true，可以让程序追踪初始 CIS 猜测，
如果我们希望从内价或芯轨道电离或激发，这是必要的。
在 RHF 实现中，除了将 `DoCore` 和 `FollowCIS` 设为 true 外，
还可以使用关键词 `CoreHole` 指定电离或激发所源自的芯轨道。
`CoreHole` 关键词相当通用，原则上可以使用该关键词指定
从任何占据轨道出发的电离或激发过程。

(sec:spectroscopyproperties.eom.theory.hamiltonian)=
### 哈密顿量构造（Hamiltonian Construction）

哈密顿量构造从调用 sigma 例程开始。在闭壳层代码的情形下，
逻辑变量 `UseEOMOptS` 和 `UseEOMOptD` 分别选择用于计算
单激发和双激发 sigma 向量的例程。若为 true，将使用经过优化的、
采用 dressed 积分的 sigma 例程。这不应更改，该选项主要
用于调试目的。若设为 false，则改用自动生成的、慢得多的
串行代码。在开壳层 UHF 实现的情形下，已使用 ORCA 自动
生成环境（AGE）{cite}`krupicka2017ORCA_AGE` 生成了优化的 sigma 例程。
在每次早期迭代中，将确定 $N_R$ 个 sigma 向量，但在重启的情形下
例外，此时 sigma 向量的数目为 $2N_R$。关于收敛的更多细节，
见下文 {ref}`sec:spectroscopyproperties.eom.theory.conv`。

sigma 向量构造中最耗时的部分是外交换贡献的形成，这可以通过
CC 关键词 `KCOpt` 来影响。目前有三个选项与 RHF EOM 实现兼容：
`KC_MO`、`KC_AOX` 和 `KC_AOBLAS`，而 `KC_AOX` 是 UHF EOM 代码中
唯一可用的选项。外交换项可以使用 COSX 高效处理，在闭壳层情形下，
这使外交换项平均加速 10 倍，EOM 计算总体加速 3 倍。
同时存储成本也大幅降低{cite}`Dutta2016COSX`。引入的误差
低于 1 meV，比该方法本身的误差棒小 200 倍{cite}`Dutta2016COSX`。
它是 `KCOpt` 选项 `KC_AOX` 和 `KC_AOBLAS` 的默认设置，
可通过关键词 `DOCOSXEOM` 控制。EOM 的默认网格设置为
`GridX 1` 和 `IntAccX 2.68`。

一旦获得 sigma 向量，就将其与试探向量相乘以得到约化空间哈密顿量。
哈密顿量的构造方式是，在每次迭代中只将新的向量积添加到旧哈密顿量的
"边缘"，从而避免完全重建。应当清楚，参数 `NDav` 在这里起着重要作用，
因为它决定了哈密顿量的最大尺寸（$N_DN_R$），并且如上所述
还控制着试探向量和 sigma 向量所需的内存量。由于该参数的选择
会影响收敛性质，将在
{ref}`sec:spectroscopyproperties.eom.theory.conv` 中进一步讨论。

(sec:spectroscopyproperties.eom.theory.nonsymmetric)=
### （非对称）本征问题的求解（Solution of the (Nonsymmetric) Eigenproblem）

哈密顿量构造完成后，调用非对称本征求解器。在这种情况下，
可能出现复本征值。实际上，这种情况很少见，并且表明存在某种问题。
如果发生这种情况会给出警告，不过，如果它只发生在孤立的迭代步骤中，
可能问题不大。

一旦获得本征向量，如果开启了根追踪（root homing），即
`RootHoming` 关键词设为 true，就会将其与上一次迭代的本征向量进行比较。
这意味着计算新旧本征向量的重叠，以便在发生根翻转（root flipping）时
跟踪本征向量可能的移动。如果收敛的根从后续迭代中移除（见下一节），
跟踪顺序的变化就很重要，尤其是当一个收敛的根和一个未收敛的根
发生交换时。对角化后，可以计算 Ritz 向量和残差。

(sec:spectroscopyproperties.eom.theory.conv)=
### 收敛、重启、预条件与子空间扩展（Convergence, Restart, Preconditioning and Subspace Expansion）

当满足基于残差平方范数的判据时，即标志着收敛。
该判据由 `CheckEachRoot` 关键词决定。
若为 true（默认），则分别检查每个根的残差平方范数的收敛性。
这是因为不同的根以不同的速率收敛。一旦某个根收敛，
就不会再为属于该向量的根生成新的试探向量。
这意味着 EOM 迭代将逐步变快（直到重启）。
可以关闭逐根收敛检查，但不推荐。在这种情况下，
检查所有残差平方范数的最大值是否收敛，并且所有迭代
将花费大致相同的时间，因为在任何迭代中都不会移除向量。
然而，这一过程在数值上可能不稳定，因为某些根的残差
可能变得非常接近于零，而尝试生成与这些残差正交的新向量
可能导致数值灾难。简而言之，推荐的默认设置是
`CheckEachRoot` 和 `RootHoming` 都设为 true。
如果 `CheckEachRoot` 为 false，则 `RootHoming` 也应设为 false，
因为如果 `NDav` 太小，它可能会引起问题。
Davidson 方法中残差的收敛阈值可以大于基态 CC 残差阈值，
以便获得收敛的结果。也就是说，`DTol` 取 1e-5 几乎总是
足以得到良好收敛的能量。

这里值得讨论一下关键词 `NDav` 的作用。
该关键词决定 Davidson 算法应在何时重启。
如果选得太小，可能导致收敛缓慢。如果该值太大，
可能导致对内存/磁盘空间的过高要求。默认值（20）的选取
是希望不需要重启，或者最多需要一次重启。
只有在计算资源要求时才应更改。然而，处理芯电离或芯激发过程
往往需要较大的 `NDav` 值。在重启时，Ritz 向量被复制为
所有根的新试探向量，然后进行正交归一化，而只为未收敛的根
生成新向量。这意味着重建扩展空间之后的步骤将比初始步骤之一
贵 1-2 倍。

新方向（试探向量）由预条件后的残差向量生成。
如果不应用预条件（预条件子取为单位矩阵），则退回到
Lanczos 算法，它不如 Davidson 算法。当关键词 `DoLanczos`
为 true 时就会发生这种情况。不推荐这样做，因为 Lanczos 算法
的收敛速度比 Davidson 慢好几倍，主要用于调试。
原始的 Davidson 预条件子是一个对角矩阵的逆，该对角矩阵
包含哈密顿量对角元素与给定根所属本征值当前近似值之差。
为简单起见，让我们考虑闭壳层 RHF 实现。
如果 $R_{ia}$ 和 $R_{ijab}$ 分别是单激发和双激发振幅的元素，
则更新向量（$T_{ia}$、$T_{ijab}$）具有如下形式

$$T_{ia}=\frac{R_{ia} }{D_{ia}+\mathcal{E}_R}$$

（单激发），以及

$$T_{ijab}=\frac{R_{ia} }{D_{ijab}+\mathcal{E}_R}$$

（双激发）。这里，$D_{ia}$ 和 $D_{ijab}$ 与相应的哈密顿量
对角元素有关，也可能是其近似。最简单的近似就是用对角 Fock
矩阵元素（即轨道能）构造：$D_{ia}=\varepsilon_a-\varepsilon_i$ 和
$D_{ijab}=\varepsilon_a+\varepsilon_b-\varepsilon_i-\varepsilon_j$。
可以得到略好的预条件，如下所示。对于单激发，取精确的 CIS
对角元素，$D_{ia}=\varepsilon_a-\varepsilon_i+\overline{g}_{iiaa}$，
其中最后一项是相应的反对称化积分；双激发则构造为
$D_{ijab}=D_{ia}+D_{jb}$。这是默认设置，可以通过将
`UseCISUpdate` 设为 false 改回简单的 Fock 矩阵猜测。

预条件步骤之后，所得向量与先前的试探向量集合正交，
并彼此正交归一化。由于试探向量一旦生成就不会改变
（除非发生重启），正交归一化只需生成重叠矩阵的新元素。
求逆（及其他除法步骤）的数值阈值由参数 `OTol` 控制。
最后，打印信息的量可以通过 `PrintLevel` 关键词控制。
如果不给定或等于 2，只打印基本的迭代信息。
如果设为 3，将打印详细的迭代信息（如果需要各步骤的计时结果
则推荐），而 4 或更高还会触发来自其他子例程的额外
（且非常冗长的）信息。

默认求解器是多根 Davidson 过程。可以通过将 `DoRootwise`
和 `FollowCIS` 设为 true 来启动单根求解器。
当请求大量根时，后者更稳定。

(sec:spectroscopyproperties.eom.theory.properties)=
### RHF EOM 实现中的性质（Properties in the RHF EOM implementation）

当前 RHF EOM 实现中唯一可以计算的性质是跃迁矩。
它按照 Stanton 和 Bartlett 提出的方法，作为类 CI 期望值计算。
右跃迁密度和左跃迁密度定义为

$$\rho_{pq}^{Gr\rightarrow Ex} =\langle\phi_{0}|(1+\Lambda)[e^{-T}\{p^{+}q^{-}\}e^{T},R]|\phi_{0}\rangle$$

$$\rho_{pq}^{Ex\rightarrow Gr} =\langle\phi_{0}|Le^{-T}\{p^{+}q^{-}\}e^{T}|\phi_{0}\rangle$$

在上述方程中，$\Lambda$ 对应于基态左矢量，需要求解一次，
$L$ 是左矢量，需要为每个根分别求解。一旦获得右矢量和左矢量，
就构造左跃迁密度和右跃迁密度，并使用以下公式计算振子强度

$$f=\frac{2}{3}\varepsilon|\mu_{pq}\rho_{pq}^{Ex\rightarrow Gr}||\mu_{pq}\rho_{pq}^{Gr\rightarrow Ex}|$$

默认计算的振子强度对 $\Lambda$ 采用线性近似。
另一方面，$L$ 向量作为相应 $R$ 向量的一般逆来计算。
这种近似在能量计算之外不需要额外的工作量，其精度
与精确振子强度计算相当，而后者的成本至少是能量计算的两倍。
不过，通过将 `DoLeft` 和 `DoTDM` 设为 true，
可以计算精确的 EOM-CC 跃迁矩。请注意，跃迁矩尚未在
UHF EOM-CCSD 方法中实现。

(sec:spectroscopyproperties.eom.use)=
## 一般用法（General Use）

EOM-CCSD 例程是 ORCA 程序包 `orca_mdci` 模块的一部分。
在成功的耦合簇计算之后，如果设置了相应的标志和根数，
它就会被调用。在下一章中，将描述 EOM 例程的一般程序流程和
输入参数。对于 RHF 或 UHF 参考，EE-、IP- 和 EA-EOM-CCSD 方法
分别可用于计算激发能、电离势和电子亲和能。
目前，可用的简单输入关键词如下：

```orca
!EOM-CCSD      # same as !EE-EOM-CCSD
!EE-EOM-CCSD   # EOM for electronically excited states
!IP-EOM-CCSD   # IP version
!EA-EOM-CCSD   # EA version
```

进行 EOM 计算最简单的方式是使用 `EOM-CCSD` 关键词，
并指定所需的根数：

```{literalinclude} ../../orca_working_input/C05S07_162.inp
:language: orca
```

上述输入将以默认设置调用 EOM 例程。主要输出是激发能列表，
并附有一些进一步的态相关数据。对于上述输入，得到如下输出：

```orca
----------------------
EOM-CCSD RESULTS (RHS)
----------------------

IROOT=  1:  0.147823 au     4.022 eV   32443.5 cm**-1
  Amplitude    Excitation
   0.107945     4 ->   8
   0.665496     7 ->   8
   0.104633     7 ->   8     6 ->   8
  Ground state amplitude:  0.000000
Percentage singles character=     92.32

IROOT=  2:  0.314133 au     8.548 eV   68944.3 cm**-1
  Amplitude    Excitation
   0.671246     7 ->   9
  Ground state amplitude: -0.000000
Percentage singles character=     90.42

IROOT=  3:  0.343833 au     9.356 eV   75462.6 cm**-1
  Amplitude    Excitation
  -0.670633     5 ->   8
  -0.112538     6 ->   8     5 ->   8
  Ground state amplitude:  0.000000
Percentage singles character=     92.00

IROOT=  4:  0.364199 au     9.910 eV   79932.5 cm**-1
  Amplitude    Excitation
   0.102777     4 ->  10
  -0.484661     6 ->   8
   0.438311     7 ->  10
  -0.167512     6 ->   8     6 ->   8
  Ground state amplitude: -0.021060
Percentage singles character=     87.22

IROOT=  5:  0.389398 au    10.596 eV   85463.0 cm**-1
  Amplitude    Excitation
   0.646812     4 ->   8
  -0.122387     7 ->   8
   0.171366     7 ->   8     6 ->   8
  Ground state amplitude:  0.000000
Percentage singles character=     87.47

IROOT=  6:  0.414587 au    11.281 eV   90991.4 cm**-1
  Amplitude    Excitation
  -0.378418     6 ->   8
  -0.537292     7 ->  10
  -0.124246     6 ->   8     6 ->   8
  Ground state amplitude: -0.061047
Percentage singles character=     89.13

IROOT=  7:  0.423861 au    11.534 eV   93026.7 cm**-1
  Amplitude    Excitation
   0.673806     7 ->  11
  Ground state amplitude:  0.000000
Percentage singles character=     93.14

IROOT=  8:  0.444201 au    12.087 eV   97490.8 cm**-1
  Amplitude    Excitation
   0.664877     6 ->   9
   0.130475     6 ->   9     6 ->   8
  Ground state amplitude: -0.000000
Percentage singles character=     87.17

IROOT=  9:  0.510514 au    13.892 eV  112044.8 cm**-1
  Amplitude    Excitation
  -0.665791     6 ->  10
   0.114259     6 ->  15
  -0.124374     6 ->  10     6 ->   8
  Ground state amplitude: -0.000000
```

IP 和 EA 版本可以分别使用关键词 `IP-EOM-CCSD` 和 `EA-EOM-CCSD`
调用。对于开壳层体系（UHF 参考波函数），IP/EA-EOM-CCSD 计算
需要一个额外的关键词。也就是说，通过在 %mdci 块中将
`DoAlpha` 关键词设为 true 来请求涉及移除/附着 $\alpha$ 电子的
IP/EA 计算，而将 `DoBeta` 关键词设为 true 则选择移除/附着
$\beta$ 电子的 IP/EA 计算。请注意，`DoAlpha` 和 `DoBeta` 不能
同时为 true，且如果输入中未指定关键词，计算默认为 `DoAlpha` 为 true。
下面给出 UHF IP-EOM-CCSD 计算（移除 $\alpha$ 电子）输入的一个简单示例。

```orcainput
! IP-EOM-CCSD cc-pVDZ 
%mdci
  DoAlpha true
  NRoots 7
end

*xyz 0 3
  O      0.0 0.0 0.0
  O      0.0 0.0 1.207
*
```

(sec:spectroscopyproperties.excitedstates.eom.capabilities)=
### 功能（Capabilities）

目前，EOM 例程能够对闭壳层或开壳层体系分别使用 RHF 或 UHF
参考波函数，进行激发态、电离态和电子附着态计算。
它可用于串行和并行计算。该方法在反变换 PNO 和 DLPNO 框架中可用，
从而能够计算大分子——见
{ref}`sec:spectroscopyproperties.dleom` 章节和
{ref}`sec:spectroscopyproperties.excitedstates.dlpnoeom` 章节。
在闭壳层情形下（RHF），可以通过在 %mdci 部分将 `CCSD2` 关键词
设为 true 来调用低标度版本。后者是对常规 EOM-CCSD 的二阶近似。
目前，提供的最有用的信息是激发能、电离势或电子亲和能的列表。
基态到激发态的跃迁矩也可用于 EE-EOM-CCSD 的闭壳层实现。

(sec:spectroscopyproperties.eom.memory)=
## 内存管理（Memory Management）

来自耦合簇例程的最重要数据是基态能量和波函数，以及分子积分。
这些积分随后用于创建 "dressed" 积分容器，这使得 EOM 方程的
高效因子分解成为可能，因为这些 dressed 量在计算过程中不会改变。
其中大部分写在磁盘上，但具有三个外部指标的积分容器可能例外。
如果有足够的内存，这些以及求解器文件可以保留在内存中。
程序按照重要性顺序依次尝试为这些文件分配内存，
无法保留在内存中的则写入磁盘。分配顺序如下：
1. 残差向量，2. Ritz 向量，3. 三外部积分，4. sigma 向量，
5. 态（试探）向量，如下例所示：

```orca
--------------------------------
AUTOMATIC CHOICE OF INCORE LEVEL
--------------------------------

Memory available                           ...   6512.00 MB
Memory needed for Residual-vectors         ...     71.27 MB
Memory needed for Ritz-vectors             ...     71.27 MB
Memory needed for 3-ext integrals          ...     92.05 MB
Memory needed for Sigma-vectors            ...   1425.31 MB
Memory needed for State-vectors            ...   1425.31 MB
 -> Final InCoreLevel    ... 5
```

用关键词 `MaxCore` 指定的内存的一半分配给这五个候选者。
在上述情形下，所有内容都放得进内存。
请注意，这些只是内存消耗的最大贡献者，分配内存时理想情况下
应留有安全余量。

为估计所需内存量，应记住，在闭壳层情形下，
残差向量和 Ritz 向量的内存需求正比于 $N_RN_PN_V^2$，
三外部积分正比于 $N_RN_ON_V^3$，sigma 向量和试探向量
正比于 $N_DN_RN_PN_V^2$，其中 $N_O$ 和 $N_V$ 是占据轨道数和
虚拟轨道数，$N_P=\frac{N_O(N_O+1) }{2}$ 是占据对数，
$N_R$ 是根数，$N_D$ 是约化空间的最大尺寸。
关键词 `NRoots` 设定 $N_R$，而 `NDav` 决定 $N_D$。
幸运的是，根据我们的经验，保留在内存中最重要的贡献
也是需要内存量最小的那些。建议使用 `KCOpt AOBLAS`，
因为它的内存需求最低。

请注意，在 UHF EE-EOM-CCSD 实现中，残差向量和 Ritz 向量的
内存需求正比于
$N_R(N_{P_{\alpha} }N_{V_{\alpha} }^2 + N_{P_{\beta} }N_{V_{\beta} }^2 + N_{O_{\alpha} }N_{O_{\beta} }N_{V_{\alpha} }N_{V_{\beta} })$，
三外部积分正比于
$N_R(N_{O_{\alpha} }N_{V_{\alpha} }^2 + N_{O_{\beta} }N_{V_{\beta} }^2 + N_{O_{\alpha} }N_{V_{\alpha} }N_{V_{\beta} }^2 + N_{O_{\beta} }N_{V_{\beta} }N_{V_{\alpha} }^2)$，
sigma 向量和试探向量的内存需求正比于
$N_DN_R(N_{P_{\alpha} }N_{V_{\alpha} }^2 + N_{P_{\beta} }N_{V_{\beta} }^2 + N_{O_{\alpha} }N_{O_{\beta} }N_{V_{\alpha} }N_{V_{\beta} })$，
其中 $N_{O_{\alpha} }$、$N_{O_{\beta} }$、$N_{V_{\alpha} }$ 和
$N_{V_{\beta} }$ 分别是占据 alpha、占据 beta、虚拟 alpha 和
虚拟 beta 轨道数，$N_{P_{\alpha} }=\frac{N_{O_{\alpha} }(N_{O_{\alpha} }-1) }{2}$ 和
$N_{P_{\beta} }=\frac{N_{O_{\beta} }(N_{O_{\beta} }-1) }{2}$
分别是 alpha 和 beta 占据对数。

(sec:spectroscopyproperties.eom.tips)=
## EOM-CC 计算的一些提示与技巧（Some tips and tricks for EOM-CC calculation）

-   COSX 近似在内存使用、磁盘空间使用和计算时间方面带来显著节省，
    而几乎不损失精度{cite}`Dutta2016COSX`。因此，大规模计算的
    首选设置应包括 `DoCOSXEOM true`、`DoAOX3e true`
    和 `KCOpt KC_AOBLAS`（请注意，在 UHF 实现中 `KC_AOX` 是
    `KCOpt` 唯一可用的选项）。

-   ORCA 中的 EOM-CC 代码有三个版本的 Davidson 求解器。
    默认是多根求解器，它对所有根一起进行优化。
    它收敛最快，当只对大分子的少数几个根感兴趣时更合适。
    然而，如果需要超过 10 个根，多根求解器可能遇到数值问题。
    在这种情况下，可以通过设置 `DoRootwise true` 来调用逐根求解器。
    单根求解器非常稳定，当需要大量根时应使用它。
    不过，单根求解器的收敛比多根求解器慢。在 RHF 实现中，
    还有一个分批求解器，其中总根数的一个子集一起优化。
    这可以通过设置 `NRootsPerBatch true` 来调用，
    在稳定性和收敛性方面介于多根求解器和单根求解器之间。

-   如果 EOM 迭代在 50 个周期内不收敛，可以尝试通过将
    `%mdci` 块中的 `MaxIter` 设为更大的值来增加迭代次数。
    也可以尝试通过增加 `NDav` 值来增大 Davidson 求解器中
    Krylov 空间的维度，这通常有助于加速收敛。
    然而，将 `NDav` 设为大于 200 的值会使计算成本高得难以承受，
    尤其在内存方面。

-   收敛阈值 `DTol 1e-5`（Davidson 收敛）和 `STol`
    `1e-7`（基态 CCSD 收敛）通常能得到足够收敛的能量，
    适用于大多数目的。

-   常规 Davidson 求解器通常得到最低能量的解。
    当请求大量根时，对于 EOM-CC 的 IP 和 EA 变体，
    该过程也可能得到以双激发为主的根（即所谓的卫星态）。
    如果对低能的 Koopman 型 IP 和 EA 态感兴趣，
    可以通过将 `FollowCIS` 设为 true 来获得。
    这将追踪 Fock 算符提供的初始猜测。

(sec:spectroscopyproperties.eom.options)=
## 完整关键词列表（Full keyword list）
```{index} EOM-CCSD Keywords
```

与 EOM-CC 相关的简单输入关键词汇总于 {numref}`tab:spectroscopyproperties.eom.options.simple`。
与 UHF EOM-CC 相关的 `%mdci` 块输入关键词汇总于 {numref}`tab:spectroscopyproperties.eom.options.uhfmdciblock`。
与 RHF EOM-CC 相关的 `%mdci` 块输入关键词汇总于 {numref}`tab:spectroscopyproperties.eom.options.rhfmdciblock`。

(tab:spectroscopyproperties.eom.options.simple)=
:::{table} EOM-CC 的简单输入关键词。
:class: footnotesize
| 关键词        | 说明                                       |
|:--------------|:-----------------------------------------|
| `EOM-CCSD`    | 与 `EE-EOM-CCSD` 相同                      |
| `EE-EOM-CCSD` | 用于电子激发态的 EOM-CC                    |
| `IP-EOM-CCSD` | IP 版本                                    |
| `EA-EOM-CCSD` | EA 版本                                    |
:::

:::{raw} latex
\begingroup
\footnotesize
:::

:::{tabularcolumns} \Y{0.2}\Y{0.2}\Y{0.6}
:::

(tab:spectroscopyproperties.eom.options.rhfmdciblock)=
:::{flat-table} RHF EOM-CC 的 `%mdci` 块输入关键词，括号内为默认值。
:class: footnotesize
:header-rows: 1
* - 关键词
  - 选项
  - 说明
* - `DoEOM` (false)
  - `true/false`
  - 是否执行 EOM？
* - `UseEOMOptS` (true)
  - `true/false`
  - 对单激发使用优化的 sigma 例程？
* - `UseEOMOptD` (true)
  - `true/false`
  - 对双激发使用优化的 sigma 例程？
* - `NDav` (20)
  - `<int>`
  - 约化空间的最大尺寸（即 20×NRoots）
* - `CCSD2` (false)
  - `true/false`
  - 使用低标度的 CCSD(2) 近似？
* - `CheckEachRoot` (true)
  - `true/false`
  - 分别检查每个根的收敛？
* - `RootHoming` (true)
  - `true/false`
  - 应用根追踪（root homing）？
* - `DoLanczos` (false)
  - `true/false`
  - 使用 Lanczos 过程而非 Davidson？
* - `UseCISUpdate` (true)
  - `true/false`
  - 使用对角 CIS 进行更新？
* - `NInits` (0)
  - `<int>`
  - 初始猜测中的根数；若为 0，使用预设值
* - `DRESS3ES` (true)
  - `true/false`
  - 构造单激发的外 dressing 还是即时计算？
* - `DRESS3ED` (false)
  - `true/false`
  - 构造双激发的外 dressing 还是即时计算？
* - `DOCOSXEOM` (false)
  - `true/false`
  - 在 EOM 中对外交换项使用 COSX 近似？
* - `DOAOX3E` (false)
  - `true/false`
  - 对 4 外部项对 3 外部中间量的贡献使用 COSX 近似？
* - `DoRootwise` (false)
  - `true/false`
  - 分别求解每个根？对大量根更稳定。
* - `DoTDM` (false)
  - `true/false`
  - 计算默认跃迁矩的选项？
* - `Doleft` (false)
  - `true/false`
  - 计算精确左矢量？
* - `NRootsPerBatch` (1)
  - `<int>`
  - 一起计算的根数
* - `FOLLOWCIS` (false)
  - `true/false`
  - 追踪初始单激发猜测？
* - `DoCore` (true)
  - `true/false`
  - 从芯轨道开始电离或激发？
* - `CoreHole` (0)
  - `<int>`
  - 需要从中电离或激发的芯轨道
* - `CVSEP` (false)
  - `true/false`
  - 将芯轨道与价轨道分开？
* - `DTol` (1e-5)
  - `<real>`
  - EOM 残差阈值的默认值
* - `NRoots` (9)
  - `<int>`
  - 根数
* - `OTol` (1e-14)
  - `<real>`
  - 正交归一化阈值
* - `KCOpt`
  - 
  - 外交换形成的方法
* -
  - `KC_MO`
  - 
* -
  - `KC_AOX`
  - 当请求精确 TDM 计算时
* -
  - `KC_AOBLAS`
  - 最高效
* - `PrintLevel` (3)
  - `<int>`
  - 要打印的信息量
* - `MaxCore` (500)
  - `<int>`
  - 总内存量
:::

:::{raw} latex
\endgroup
:::

:::{raw} latex
\begingroup
\footnotesize
:::

:::{tabularcolumns} \Y{0.2}\Y{0.2}\Y{0.6}
:::

(tab:spectroscopyproperties.eom.options.uhfmdciblock)=
:::{flat-table} UHF EOM-CC 的 `%mdci` 块输入关键词，括号内为默认值。
:class: footnotesize
:header-rows: 1

* - 关键词
  - 选项
  - 说明
* - `DoEOM` (false)
  - `true/false`
  - 是否执行 EOM？
* - `DoAlpha` (false)
  - `true/false`
  - 移除/附着一个 alpha 电子（IP/EA 计算）？
* - `DoBeta` (false)
  - `true/false`
  - 移除/附着一个 beta 电子（IP/EA 计算）？
* - `NDav` (20)
  - `<int>`
  - 约化空间的最大尺寸（即 20×NRoots）
* - `UseQROs` (false)
  - `true/false`
  - 使用 QROs？
* - `CheckEachRoot` (true)
  - `true/false`
  - 分别检查每个根的收敛？
* - `RootHoming` (true)
  - `true/false`
  - 应用根追踪（root homing）？
* - `DoLanczos` (false)
  - `true/false`
  - 使用 Lanczos 过程而非 Davidson？
* - `DoOlsen` (false)
  - `true/false`
  - 使用 Olsen 过程而非 Davidson？
* - `UseCISUpdate` (true)
  - `true/false`
  - 使用对角 CIS 进行更新？
* - `NInits` (0)
  - `<int>`
  - 初始猜测中的根数；若为 0，使用预设值
* - `DOCOSXEOM` (false)
  - `true/false`
  - 在 EOM 中对外交换项使用 COSX 近似？
* - `DOAOX3E` (false)
  - `true/false`
  - 对 4 外部项对 3 外部中间量的贡献使用 COSX 近似？
* - `DoRootwise` (false)
  - `true/false`
  - 分别求解每个根？对大量根更稳定
* - `NRootsPerBatch` (1)
  - `<int>`
  - 一起计算的根数
* - `FOLLOWCIS` (true)
  - `true/false`
  - 追踪初始单激发猜测？
* - `DTol` (1e-5)
  - `<real>`
  - EOM 残差阈值的默认值
* - `NRoots` (9)
  - `<int>`
  - 根数
* - `OTol` (1e-14)
  - `<real>`
  - 正交归一化阈值
* - `KCOpt`
  - `KC_AOX`
  - 四外部贡献的 AO 交换
* - `PrintLevel` (3)
  - `<int>`
  - 要打印的信息量
* - `MaxCore` (500)
  - `<int>`
  - 总内存量
:::
:::{raw} latex
\endgroup
:::
