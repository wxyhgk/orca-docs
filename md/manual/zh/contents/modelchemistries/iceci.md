```{index} ICE-CI
```

(sec:modelchemistries.iceci)=
# 子空间中的近似全 CI 计算：ICE-CI

(sec:modelchemistries.iceci.introduction)=
## 简介（Introduction）

在许多情形下，人们希望生成一个尽可能接近全 CI（full-CI）结果的波函数，
但由于计算上的原因，全 CI 本身是不现实的。需要这样做的情形包括：
a) 希望为小分子生成高精度能量；或 b) 希望理清若干低激发态；或
c) 希望进行活性空间比长期以来作为技术水平的约十四条轨道更大的
[CASSCF 计算](sec:modelchemistries.casscf.iceci)。

ORCA 提供了一种被称为迭代组态展开组态相互作用（Iterative-Configuration
Expansion Configuration Interaction，ICE-CI）的方法{cite}`chilkuri_ice1,chilkuri_ice2`。
它基于 Jean-Paul Malrieu 及其合作者在 1970 年代初于 CIPSI
（一个名称相当冗长的方法的缩写：*Configuration Interaction by Perturbation with
multiconfigurational zeroth-order wave functions Selected by Iterative process*，
即"以迭代过程挑选多组态零阶波函数、通过微扰进行组态相互作用"）
框架中提出的更早期的思想。

ICE-CI 的目标是以很小一部分计算代价提供接近全 CI 极限的紧凑波函数
（例如一个或若干个态）。然而，ICE-CI 本身并非为处理数百个原子或数千个基函数而设计。
因此，与作为处理大体系高精度方法的 DLPNO-CCSD(T) 不同，ICE-CI 要么是处理极小体系的
极其稳健的高精度方法，要么是大体系的"构件"（building block）。它本身能处理几十个
电子和轨道——例如比全 CI 多*得多*——但并不能创造奇迹。其适用范围与密度矩阵重整化群
（DMRG）或量子蒙特卡洛全 CI（QMCFCI）过程相当。

ICE-CI 应当被看作一种多参考方法。它具有自适应性且稳健，即使存在近简并或完全简并也是如此。
它给出正交的态（当应用于若干态时）与自旋本征函数，还给出密度与自旋密度。

(sec:modelchemistries.iceci.algrorithms)=
## ICE-CI 与 CIPSI 算法（The ICE-CI and CIPSI Algorithms）

ICE-CI 的总体思路很直接：考虑一个至少含有给定组态
$\mathrm{\mathbf{n} }^{0}$（这是活性轨道占据数 $n_{p}^{0} =0,1\,\,or\,\,2$
（$p \quad =$ 任意活性轨道）的集合）可观贡献的多粒子态。
由非相对论哈密顿量的性质，只有与 $\mathrm{\mathbf{n} }^{0}$ 至多相差两个轨道占据的
组态才会与之相互作用。我们可以用微扰理论挑选出与 $\mathrm{\mathbf{n} }^{0}$
相互作用最强的单双激发子集，然后求解变分问题。接着我们可以分析 CI 向量，
找出对基态有主导贡献的组态。假设我们挑出满足 $C_{I}^{2} >T_{\text{gen} }$
的组态。这就定义了"生成元"（generator）组态集合。其余组态称为"变分"（variational）组态。
它们由变分原理处理到无穷阶，但重要性不足以引入其单双激发。在下一次迭代中，
我们相对于这些一般组态进行单双激发，并根据它们与前一次 CI 向量主导部分
（截断到生成元）的相互作用来挑选。重复该过程，直到找不到新的重要组态
且总能量收敛（见 {numref}`icecifig:flowchart`）。

(icecifig:flowchart)=
```{figure} ../../images/ICE1-alter.*

ICE-CI 流程图。
```

所述过程与 Malrieu 的三级 CIPSI 过程非常相似。一个主要的技术差别是，
ICE 以*组态*（configuration）和*组态状态函数*（configuration state function，CSF）
为中心，而非*行列式*（determinant）。组态是一组占据数 0、1 或 2，描述电子如何分布于
各空间轨道。*组态状态函数*（CSF）由将给定组态中的未配对自旋耦合到给定总自旋 $S$ 而构成。
一般而言，构造线性无关 CSF 集合有若干种（甚至许多种）方式。另一方面，CSF 可以用
Slater 行列式展开，但给定组态的 Slater 行列式比 CSF 更多。例如对 CAS(14,18) 计算，
约有 10$^{\mathrm{9} }$ 个行列式，但只有约 3x10$^{\mathrm{8} }$ 个 CSF 和
3x10$^{\mathrm{7} }$ 个组态。在基于组态的 ICE（CFG-ICE）中，所有逻辑都发生在组态层面。
也就是说，是两个组态之间的关系决定了两个给定组态的 CSF 或行列式是否相互作用，
若是，又通过哪些积分相互作用。由于组态空间比行列式空间紧凑得多，
围绕组态概念组织计算可获得可观的计算收益。一般而言，在 CFG-ICE 中，
属于给定组态的所有 CSF 都被包括在内，且所有挑选量在决定是否纳入该 CSF 之前
先对给定组态的所有 CSF 求和。在基于组态状态函数的 ICE（CSF-ICE）中，
生成与挑选的逻辑发生在单个 CSF 层面，因而不必为给定组态携带所有 CSF。
对于包含大量过渡金属原子且每个原子都含高自旋中心的分子，这能带来可观收益。
在这类情形下，只有主导组态的少数 CSF 起主导作用，其余对波函数的贡献可忽略不计。
最后，在某些情形下，原始的基于行列式的 CIPSI 过程可能更为可取。
这类情形可由称为 DET-ICE 的基于行列式的 ICE 处理。因此 ICE 的三种变体涵盖了
量子化学中遇到的所有可能的多参考体系类型。

应当指出，尽管该过程包含微扰成分，最终能量主要由变分能量主导，
因此就所有实际目的而言，ICE-CI 过程是变分的（但并非严格尺寸一致——
尺寸一致性误差与绝对能量误差处于同一量级）。

(sec:modelchemistries.iceci.example)=
## 一个简单的示例计算（A Simple Example Calculation）

让我们看一个水分子的简单计算：

```orcainput
#
# Check the ICECI implementation
#

! SV 

%ice  nel 10           # number of active electrons
      norb 13          # number of active orbitals
      nroots 1         # number of requested roots 
      integrals exact  # exact 4-index transformation 
                       # can be set to RI to avoid bottlenecks

      icetype   CFGs   # The configuration based ICE-CI
                CSFs   # The CSF based ICE-CI         
                DETs   # The determinnat based ICE-CI 
                       # please choose one of these three

      Tgen 1e-04       # value for Tgen. Default is 1e-4
      Tvar 1e-11       # value for Tvar. Default is 1e-11 (1e-7*Tgen)

      etol 1e-06       # energy convergence tolerance 
end

* int 0 1
O 0 0 0 0.0   0.000 0.000
H 1 0 0 1.0   0.000 0.000
H 1 2 0 1.0 104.060 0.000
*
```

让我们看输出：

```orca
------------------------------------------------------------------------------
                ORCA Iterative Configuration Expansion
             - a configuration driven CIPSI type approach -
------------------------------------------------------------------------------

(some startup information)

Making an initial 'Aufbau' configuration      ... done
Performing S+D excitations from     1   configs ... done (  0.0 sec) NCFG=581
Performing perturbative selection             ... done (  0.0 sec)
   # of configurations before selection       ... 581
   # of configurations after selection        ... 191
   'rest' energy (probably not very physical) ... -3.736391e-10

                    ******************************
                    *  ICECI MACROITERATION   1  *
                    ******************************

   # of active configurations =    191
   Now calling CI solver (269 CSFs)
(...)
CI SOLUTION :
STATE   0 MULT= 1: E=    -76.0463127108 Eh W=  1.0000 DE= 0.000 eV      0.0 cm**-1
      0.95752  : 2222200000000
   Selecting new configurations         ... done (  0.0 sec)
   # of selected configurations          ...    191
   # of generator configurations         ...     69
  Performing single and double excitations relative to generators .. done (0.0 sec)
   # of configurations after S+D         ...  13174
   Selecting from the generated configurations  ... done (  0.1 sec)
   # of configurations after Selection  ...   3827
    Root   0:    -76.046312711       -0.000000063     -76.046312773
(...)
                    ******************************
                    *  ICECI MACROITERATION   3  *
                    ******************************

   # of active configurations =   3866
   Now calling CI solver (9606 CSFs)

CI SOLUTION :
STATE   0 MULT= 1: E=    -76.0539542296 Eh W=  1.0000 DE= 0.000 eV      0.0 cm**-1
      0.95097  : 2222200000000
(...)

             ********* ICECI IS CONVERGED *********
(one final CI)

           ********************************************
           **   ICECI Problem solved in    2.6 sec   **
           ********************************************


FINAL CIPSI ENERGIES
  Final CIPSI Energy Root   0:    -76.053954291 EH
```

从输出中可以清楚看出计算中的各个步骤。程序在 CI 问题的变分求解、新组态的生成
与微扰挑选之间不断循环，直到能量收敛。通常这很快就能发生，很少需要超过五次迭代。
结果将接近全 CI 结果。

让我们更详细地看一个 H$_{\mathrm{2} }$O/cc-pVDZ 计算（见 {numref}`icecifig:example-water`）。
计算从单个 Hartree-Fock 组态开始。ICE-CI 的第一次迭代创建单双激发，
共挑选了 544 个组态。这些单双激发带来了大约一半的相关能。
仅第二次迭代（产生 73000 个被挑选的 CSF）就已经给出接近全 CI 的结果。
此时已包括了相对于 Hartree-Fock 参考最高至四重的激发。
众所周知，这类四重激发对 CI 过程的正确行为很重要（近尺寸一致性来自
作为双激发乘积的那部分四重激发）。然而，为达到所需精度只需要极小一部分四重激发。
在第一次迭代中过程已经收敛，用全 CI 空间中 0.5% 的 CSF 提供了 99.8% 的相关能，
计算时间不到求解全 CI 问题所需时间的 0.2%。因此显然可以在实现惊人节省的同时
获得近乎精确的结果。

(icecifig:example-water)=
```{figure} ../../images/ICE2.*

水分子在 cc-pVDZ 基组下的 ICE-CI 计算（冻结 1s）。
```

(sec:modelchemistries.iceci.accuracy)=
## 精度（Accuracy）

该过程的精度由两个参数 T$_{\mathrm{gen} }$ 与 T$_{\mathrm{var} }$ 控制。
由于我们发现 T$_{\mathrm{var} } \quad =$ 10$^{\mathrm{-7} }$ T$_{\mathrm{gen} }$
总能给出收敛结果，该选择即为默认。不过 T$_{\mathrm{var} }$ 可手动设置。
它可以显著减小，以牺牲一定精度为代价加快计算。
我们的默认值是 T$_{\mathrm{gen} } \quad =$ 10$^{\mathrm{-4} }$ 与
T$_{\mathrm{var} } \quad =$ 10$^{\mathrm{-11} }$。这给出与全 CI 结果相差约 1 mEh
以内的结果（粗略地说，对真正的闭壳层体系略优于 CCSDT）。

在 ICE-CI 开发过程中，我们用小分子上 21 个全 CI 能量的参考集进行了系统测试计算。
平均绝对误差的收敛模式见 {numref}`icecifig:convergence`。从图中可见 ICE-CI 向 FCI 结果的
收敛非常平滑，且可获得很高精度。事实上，默认设置导致与全 CI 结果偏差 <1 mEh 的精度。
进一步收紧可达到 $\mu$Eh 精度。相对于精确耦合簇结果所达到的精度表明，
即使是 CCSDTQ 的精度也可被 ICE-CI 超越。可达到的精度只受 T$_{\mathrm{gen} }$ 取值的限制，
受 T$_{\mathrm{var} }$ 取值的影响要小得多。因此建议采用一个已基本收敛的
T$_{\mathrm{var} }$ 值，并由 T$_{\mathrm{gen} }$ 控制过程的精度。

(icecifig:convergence)=
```{figure} ../../images/ICE3_new.*

ICE-CI 过程对 21 个全 CI 能量测试集向全 CI 结果的收敛情况。
所示为相对于全 CI 结果的 RMS 误差。各种耦合簇变体的相应误差以水平虚线表示。
```

(sec:modelchemistries.iceci.scaling)=
## 标度行为（Scaling behavior）

ICE-CI 会打破全 CI 问题的阶乘标度并呈多项式标度。多项式标度的实际阶数依赖于
体系和精度。为给出一些概念，考虑线性聚烯烃（polyene）链上的一些计算。

(icecifig:polyene-chain)=
```{figure} ../../images/ICE4.*

用于标度计算的聚烯烃链。
```

结果示于 {numref}`icecifig:polyene-scaling`。从 {numref}`icecifig:polyene-scaling` 明显可见
ICE-CI 打破了全 CI 问题的阶乘标度。事实上，对阈值 T$_{\mathrm{gen} }=$10$^{\mathrm{-4} }$、
10$^{\mathrm{-3} }$ 与 10$^{\mathrm{-2} }$，观察到的标度分别约为 $O$(N$^{\mathrm{8} })$、
$O$(N$^{\mathrm{7} })$ 与 $O$(N$^{\mathrm{6} })$。这些数字显然非常依赖于体系，
但应可作为粗略指引。若收紧 T$_{\mathrm{gen} }$，计算会很快变得昂贵得多。
经验法则是 T$_{\mathrm{gen} }$ 每收紧一个数量级，计算时间增加 10 倍。
上述计算是在一台普通台式计算机上进行的，用默认阈值已能在不到一天的耗时内
求解 CAS(30,30) 问题。大活性空间将需要放宽阈值或更大、更强的机器。

(icecifig:polyene-scaling)=
```{figure} ../../images/ICE5.*

ICE-CI 对线性聚烯烃链（完整 $\pi$ 电子活性空间）在不同生成元阈值下
随体系大小的标度行为。
```

(sec:modelchemistries.iceci.accuracywavefunction)=
## 波函数的精度（Accuracy of the Wavefunction）

多粒子波函数的精度并不容易直接检验。不过一个合理的量度是它对单电子期望值
向精确结果收敛的程度。由于每个期望值都可以用单粒子密度的自然轨道写成：

$$ \left\langle { \hat{{O} }} \right\rangle=\left\langle { \Psi \left|{\sum\nolimits_o { \hat{{o} }(\mathrm{\mathbf{x} }_{i} ) } } \right|\Psi } \right\rangle = \sum\limits_{pq} { D_{pq} \left\langle { \psi_{p} \vert \hat{{o} }\vert \psi_{q} } \right\rangle} =\sum\limits_p { n_{p} \left\langle { \tilde{{\psi } }_{p} \vert \hat{{o} }\vert \tilde{{\psi 
} }_{p} } \right\rangle} $$

其中 $\hat{o}(\mathrm{\mathbf{x}}_{i})$ 是任意单粒子算符，$D_{pq}$ 是 ICE-CI 波函数的
密度矩阵，$\tilde{{\psi}}_{p}$ 是 ICE-CI 波函数的自然轨道，$n_{p}$ 是它们的占据数。
将自然轨道占据数的偏差作为波函数收敛的量度是合理的。

例如，我们再次处理 H$_{\mathrm{2} }$O/cc-pVDZ 问题。从 {numref}`icecifig:occ-convergence`
的结果可见 ICE-CI 波函数相当精确。在默认阈值下占据数与全 CI 参考值符合到
10$^{\mathrm{-3} }$ 以内，这意味着期望值也将具有相似的精度。有趣的是，
最大误差出现在 HOMO-LUMO 能隙附近区域，显然所有近似波函数方法都倾向于
过度清空高能轨道而在低能空轨道中放入过多电子密度。通过比较可见，
该问题的 CCSD 自然占据数精度明显更低。因此这证明 ICE-CI 波函数确实在向正确结果收敛。

(icecifig:occ-convergence)=
```{figure} ../../images/ICE6.*

ICE-CI 自然轨道占据数的收敛情况。上图显示全 CI 占据数，下图为 ICE-CI 值
相对于这些精确值的偏差。作为对照，也给出了 CCSD 自然轨道占据数。
```

(sec:modelchemistries.iceci.pes)=
## 势能面（Potential Energy Surfaces）

可以用 ICE-CI 扫描整条势能面。一般而言，沿势能面的非平行性误差（non-parallelity
error）非常小。因此 ICE-CI 在整个面上给出一致的质量。

例如，让我们看 N$_{\mathrm{2} }$ 分子的势能面（{numref}`icecifig:n2-surface`）——
这是量子化学方法的常见测试案例。能正确解离 N$_{\mathrm{2} }$ 三键的方法并不多——
ICE-CI 就是其中之一。势能面完全平滑，在解离极限处行为也正确。
在极小值附近它非常接近高水平耦合簇方法，但那些方法在键被拉长时都严重失效。

(icecifig:n2-surface)=
```{figure} ../../images/ICE7.*

N$_2$ 分子在 SV 基组下的势能面。作为对照，也给出了更高水平的耦合簇结果。
```

观察 ICE-CI 波函数沿解离势能面的变化是有趣的。作为一个例子，我们看 H$_{\mathrm{2} }$O
的解离曲线，其中两个 O-H 键同时被拉长（{numref}`icecifig:h2o-error`）。
可见 ICE-CI 方法在所有距离上都与全 CI 曲线极其平行。因此即使当 Hartree-Fock
成为糟糕近似时，对键的描述仍保持一致。若在 ICE-CI 过程中使用 MP2 自然轨道，
符合得特别好。在 T$_{\mathrm{gen\thinspace } }=$ 10$^{\mathrm{-4} }$ 的默认值与
MP2 自然轨道下，误差始终低于 0.2 mEh。对更紧的阈值，误差低于 0.05 mEh。
相比之下，CCSD(T) 方法与全 CI 结果偏差相对较大，而且随 O-H 距离的非平行性也很严重。

(icecifig:h2o-error)=
```{figure} ../../images/ICE8.*

H$_2$O 分子在 SV 基组下 ICE-CI 的非平行性误差。所示为随 O-H 距离
（两个键同时拉长）相对于全 CI 值的偏差。作为对照，也给出 CCSD(T) 曲线。
```

分析沿解离路径的 ICE-CI 波函数很有启发（{numref}`icecifig:h2o-bond`）。
可以明显看出，波函数在整个面上都保持紧凑，即使在解离极限处——
那里 Hartree-Fock 波函数的权重降至不足 25%。即使在这个极端极限下，
ICE-CI 波函数也只由约 60000 个 CSF 构成，与平衡几何下波函数的规模非常相似。
随着波函数变得更偏多组态，生成元组态数从平衡时的 77 略微上升到最大 118，
最终在解离时为 112。同样值得注意的是，沿整个解离路径没有生成超过 8 个开壳层的组态，
这意味着 ICE-CI 波函数中包含的激发不超过四重。ICE-CI 过程所需的迭代次数
在整个面上也保持恒定的 4 次，这有力地表明成功的 ICE-CI 计算并不需要一个主导组态。

(icecifig:h2o-bond)=
```{figure} ../../images/ICE9.*

沿 O-H 解离路径对 ICE-CI 波函数的分析。
```

## 激发态（Excited States）

ICE-CI 可用于从一无所知出发获得对激发态的某些认识。当然，启动激发态计算的最佳方式
是了解哪些组态对体系的低激发态重要。如果情况并非如此，则使用自动化流程。
程序将首先用输入提供的轨道生成一个"Aufbau"（构造）组态。从该 Aufbau 组态出发，
在组态层面进行单激发，并对所需数目的根对角化哈密顿量。然后分析这些根的主导组态，
并从这些组态启动常规 ICE-CI 过程。例如，看一个 CN 自由基的计算。
在此情形下，我们知道最低四个根（一个双重态 $\Sigma$ 基态、一个双重态 $\Pi$
激发态和一个双重态 $\Sigma$ 激发态）的相关轨道与主导组态，因而可以如下所示
在输入文件中提供它们。

```orcainput
#
! cc-pVDZ VeryTightSCF 

%maxcore 4096

%casscf nel 7
        norb 4
        nroots 4
        mult 2
        end

%ice   nel 9
        norb 26
        nroots 4
        cimode 3
        tvar 1e-11
        tgen 1e-4
        refs { 2 2 2 2 1 }
             { 2 2 2 1 2 }
             { 2 2 1 2 2 }
             { 2 1 2 2 2 }
             end
        end

* xyz 0 2
C 0 0 0
N 0 0 1.07
*
```

结果如下所示。激发能是合理的，但由于基组的限制并非高精度（实验上双重态
$\Pi$ 态在 1.32 eV，双重态 $\Sigma$ 态在 3.22 eV）。在双重态 $\Pi$ 态中
存在非常轻微的对称性破缺，源自挑选过程。应当指出，态平均 CASSCF 激发能为
0.25 eV 与 3.18 eV。

```orca
STATE   0 MULT= 2: E=    -92.4542949092 Eh W=  0.2500 DE= 0.000 eV      0.0 cm**-1
      0.67408  : 22221000000000000000000000
STATE   1 MULT= 2: E=    -92.3777338429 Eh W=  0.2500 DE= 2.083 eV  16803.2 cm**-1
      0.65997  : 22212000000000000000000000
      0.12092  : 22122000000000000000000000
      0.11545  : 22221000000000000000000000
STATE   2 MULT= 2: E=    -92.3776916150 Eh W=  0.2500 DE= 2.084 eV  16812.5 cm**-1
      0.69860  : 21222000000000000000000000
      0.16565  : 22122000000000000000000000
STATE   3 MULT= 2: E=    -92.3412510872 Eh W=  0.2500 DE= 3.076 eV  24810.3 cm**-1
      0.51251  : 22122000000000000000000000
      0.16825  : 22212000000000000000000000
      0.11151  : 21222000000000000000000000
```

下面介绍在主导组态未知时如何对激发态进行 ICE-CI 计算。

(sec:modelchemistries.iceci.tips)=
## 技巧与要点（Tips and Tricks）

(sec:modelchemistries.iceci.tips.csf)=
### 使用基于 CSF 的算法（Using the CSF-Based Algorithm）

对于包含大量过渡金属原子且每个原子都含高自旋中心的分子，CSF-ICE-CI 能带来可观收益。
在这类情形下，只有主导组态的少数 CSF 起主导作用，其余对波函数的贡献可忽略不计。
不过 CSF-ICE-CI 有一个注意事项：需要一个内存缓冲区来存储每个 CSF 的所有重要单双激发。

```orca
%ice 
 # Scratch space dimension (number of singles/double excitations per CSF) 
 # If scratch is too small, the program may crash.
 CIBufferLength 10240 # ~82kB (factor 8/10³ to get the memory in kB): 
end
```

默认缓冲区大小 `CIBufferLength` 通常足以应对大多数常见计算。
若 `CIBufferLength` 对给定计算太小，ICE-CI 程序会崩溃。
用显著更大的缓冲区大小重新启动（例如 `%ice CIBufferLength 1000000 end`）通常能解决此问题。
在为大型多中心过渡金属簇合物与配合物运行 ICE-CI 计算时，请记住这一变通办法。


(sec:modelchemistries.iceci.tips.orbitals)=
### 轨道的选择（Choice of Orbitals）

ICE-CI 与 MP2 自然轨道等配合使用会非常有效。这通常给出更接近全 CI 的结果，
同时产生更紧凑的波函数（可称为 nICE）。在 %ice 块中选择 `UseMP2nat true`
即可请求使用 MP2 自然轨道。另一种选择是改进虚轨道（improved virtual orbital，
由 `UseIVOs true` 请求）。比较见图 {ref}`icecifig:startorbitals`。
显然，基于 MP2 自然轨道的计算相对于全 CI 的误差几乎比相应正则轨道结果小一半，
同时波函数紧凑 30% 以上。因此，在 ICE-CI 过程中使用 MP2 自然轨道似乎是个好主意。
即使 MP2 本身是糟糕近似时（例如上文所示 H2O 分子的解离极限）也是如此。
另一方面，IVO 的行为与正则轨道非常相似，因而似乎优势较少。

(icecifig:startorbitals)=
```{figure} ../../images/ICE10.*

ICE-CI 过程中 MP2 自然轨道与改进虚轨道的比较
（H2O 分子，cc-pVDZ 基组，平衡几何）。

```

如果 ICE-CI 与 MP2 自然轨道配合使用，还有可能让程序自动选择活性空间
（这称为 auto-ICE）。总体思路很简单——我们基于 MP2 自然轨道及其占据数确定活性空间。
占据数在比如 1.98 到 0.02 之间的所有轨道都将包括在活性空间中。
相关输入如下所示。

```orcainput
! cc-pVDZ aug-cc-pV6Z/C Auto-ICE
%ice nmin 1.99 nmax 0.01 end

%paras R= 1.0 end

* int 0 1
O 0 0 0 0 0 0
H 1 0 0 { R} 0 0
H 1 2 0 { R} 104 0
*
```

如果我们扫描 H$_{\mathrm{2} }$O 解离面，可以看到尽管活性空间在变化，
解离曲线仍平滑并与全 CI 解离曲线保持相当平行。视阈值的松紧，活性空间在解离时
可能从较小的 5 个轨道中 6 个电子变为较大的 7 或 8 个轨道中 8 个电子。
这是预期行为，因为 $\sigma$ 反键轨道沿键拉伸坐标变得更稳定。
因此这些结果令人鼓舞——在许多情形下，程序无需用户大量输入就能选出合理的活性空间。

(icecifig:auto-space)=
```{figure} ../../images/ICE11.*

沿 H$_2$O 解离面的自动活性空间选择。参考曲线（蓝色三角）是默认参数下
完整轨道空间的 ICE-CI 方法。

```

自动选择方便发挥作用的另一个场合是激发态的计算。如果没有用户提供组态，
程序将首先选择一个 Aufbau "参考"组态，然后相对于该组态进行所有单激发。
接着程序在该组态集合上对角化哈密顿量，为所关注的根数创建 0$^{\mathrm{th} }$
阶近似，然后从这些态的主导组态启动 ICE-CI 过程。下面是苯分子的例子：

```orcainput
! RHF def2-SVPD def2-SVP/C Auto-ICE
%cclib "/user/me/orca/cclib/orcacc"
%ice nroots 5
     nmin 1.98
     nmax 0.02
     integrals ri
     end

* int 0 1
C 0 0 0 0.000000 0.000 0.000
C 1 0 0 1.389437 0.000 0.000
C 2 1 0 1.389437 120.000 0.000
C 3 2 1 1.389437 120.000 0.000
C 4 3 2 1.389437 120.000 0.000
C 5 4 3 1.389437 120.000 0.000
H 1 2 3 1.082921 120.000 180.000
H 2 1 3 1.082921 120.000 180.000
H 3 2 1 1.082921 120.000 180.000
H 4 3 2 1.082921 120.000 180.000
H 5 4 3 1.082921 120.000 180.000
H 6 5 4 1.082921 120.000 180.000
*
```

（%cclib 语句在下文说明，在此处并非必需。）Auto-ICE 过程给出多达 19 个轨道中
24 个电子的活性空间，这已是相当繁重的计算。过程在五次迭代内收敛，
且确实给出了正确的态：基态、6.4 eV 处的 $^{\mathrm{1} }$B$_{\mathrm{2u} }$ 态、
8.9 eV 处的 $^{\mathrm{1} }$B$_{\mathrm{1u} }$ 态，以及 10.0 eV 处的一个简并
$^{\mathrm{1} }$E$_{\mathrm{1u} }$ 态。这些激发能相对实验仍偏差约 2 eV，
主要归因于缺失动态相关。然而正确的态及其顺序已被找到。

(sec:modelchemistries.iceci.tips.states)=
### 态的探测（State Detection）

如果实际基态未知，可以用 ICE-CI 找到基态。为此只需关闭挑选步骤。
这会使计算更昂贵，但会收敛到最低态。在下面的例子中（还是 H$_{\mathrm{2} }$O 分子），
我们从一个随机的五重激发组态开始——ICE-CI 仍在四次迭代后找到了基态：

```orca
%ice
  nel     8
  norb    23
  nroots   1
  tvar 1e-11
  tgen 1e-04
  etol 1e-06

  # selection
  SelStart false 
  SelIter  false 
  
  # algorithm details
  useivos   false
  integrals exact
  cimaxdim     5 #Davidson expansion space = MaxDim * NRoots
  cimode       3

  # spatial sym (only supported for ICEType = CFGs)
  irrep 0
  # startup (optional)
  refs { 2 1 0 1 0 2 1 0 1 } 
       end
end
```

然而，如果希望收敛到某个激发态，则应开启挑选。在下面的例子中（还是水分子），
可以通过审慎选择起始组态收敛到第二激发单重态：

```orca
%ice 
  nel 8
  norb 23
  nroots 1
  tvar 1e-11
  tgen 1e-04
  etol 1e-06
  
  # selection
  SelStart true 
  SelIter true 
  
  # algorithm details
  useivos false
  integrals exact
  cimaxdim 5 
  cimode 3
  
  # spatial sym (only supported for ICEType = CFGs)
  irrep 0
  { #} startup (optional)
  refs 
    { 2 2 1 2 0 1 } 
  end
end
```

(sec:modelchemistries.iceci.cistep)=
## 大规模近似 CASSCF：ICE-SCF

ICE-CI 可以在 [CASSCF](sec:modelchemistries.casscf) 框架中替代默认的 `CIStep`。
由此可以设想比以往可行的[大得多的 CASSCF 计算](sec:modelchemistries.casscf.iceci)。
以这种方式使用 ICE-CI 时，应选择自然轨道作为活性轨道，以确保正确的正则化。
一般而言，ICE-CI 结果对轨道的选择不是不变的。不过在实践中我们并未发现这会成为问题。
我们称之为 ICE-SCF。

用法很简单：在 `%casscf` 块中选择 `CIStep ICE`。可选地，可以在 `refs` 子块中
定义起始组态（CFG）或组态状态函数（CSF）。所有其他参数可通过 `%casscf` 中的
'CI' 子块访问。程序还支持[以 ICE 为参考波函数的 FIC-NEVPT2 计算]
(sec:modelchemistries.nevpt2.ice){cite}`guo_icenevpt2_2025`。

```orca
%casscf 
...
  # mandatory
  CIStep ICE
  
  # optional starting references for ICE 
  # using the refs sub-block
  # refs {2 2 ...} end
  
  # optional refined settings
  # with keywords as in the %ice block
  ci
     ICEType CFGs   # select ICE expansion type: 
                    # 'CFGs' (default), 'DETS' or 'CSFs'
     TGen 1e-4      # controls accuracy (default = 1e-4)
     TVar 1e-11     # default = 1e-7 * TGen
     MaxIter 100    # number of allowed cycles (default = 64)
     
     # Scratch space dimension (number of singles/double excitations per CSF) 
     # If scratch is too small, the program may crash.
     CIBufferLength 10240 # ~82kB (factor 8/10³ to get the memory in kB): 
  end
end
```

其余全部输入与标准 CASSCF 计算相同。这样即可在合理的周转时间内进行
活性空间非常大的 CASSCF 计算。我们未观察到比标准 CASSCF 过程更差的收敛问题。
{numref}`icecifig:casdevs-energies` 中的结果表明与常规 CASSCF 能量的偏差非常小。
C$_{\mathrm{2} }$H$_{\mathrm{4} }$ 观察到的最大偏差约为 0.2 mEh，似乎可以接受。
注意 [CASSCF 教程](https://orcaforum.kofo.mpg.de/app.php/dlext/?cat=4&sid=9d58efcf2208abe23b1af87a601b42f6)
还涵盖更大的例子以及用 ICE-CI 作为 CI 求解器计算的激发能。

(icecifig:casdevs-energies)=
```{figure} ../../images/ICE12.*

ICE-SCF 相对 CASSCF 能量对若干分子的偏差（标准截断参数 $T_{\text{gen} } = 10^{-4}$
与 $T_{\text{var} } = 10^{-11}$）。

```

由于 CASSCF 是完全变分的，可以用该过程优化几何。迄今我们的经验是，
ICE-SCF 几何与 CASSCF 几何几乎无法区分（示例见 {numref}`icecifig:casdevs-geometries`）。

(icecifig:casdevs-geometries)=
```{figure} ../../images/ICE13.*

亚甲基与臭氧的 CASSCF 与 ICE-SCF 优化几何
（cc-pVDZ 基组，默认参数）。

```

(sec:modelchemistries.iceci.keywords)=
## 关键词（Keywords）

为完整起见，下面汇总了可在输入块中指定的参数：

```orca
%ice 
        nel           8 # number of active electrons
        norb         23 # number of active orbitals
        nroots        1 # number of roots
        mult          1 # requested multiplicity
        irrep         0 # requested irrep (only supported for ICEType=CFGs)only s
        tgen      1e-04 # generator threshold
        tvar      -1e-7 # negative -> 1e-7*tgen
        etol      1e-06 # convergence tolerance 

        icetype     CFGs # The configuration based ICE-CI                     
                    CSFs # The CSF based ICE-CI                               
                    DETs # The determinant based ICE-CI 

        # algorithm details
   
        
        useMP2nat  false  # use MP2 natural orbitals
        useIVOs    false  # use improved virtual orbitals
        useQROs    false  # For UHF: use quasi-restricted MOs?
        integrals  exact  # exact or ri transformation
        CIMaxIter     64  # max. number of CI iterations in the Davidson procedure
        CINGuessMat   512 # size of the CI guess matrix in the Davidson procedure
        CIMaxDim      10  # max. size of expansion space in the Davidson procedure
        CIMode         3  # default=accelerated CI, other settings not recommended
        CSFCIwithRI    1  # 1=with RI, 0=without RI, use withour RI
	                  # when norb >> nel (e.g. (30e, 120o))
        CIPSIOrbSweepWindow 1 # Use in case of large size of the S+D list and
	                      # small available memory. MOs can be divided into
			      # chunks (e.g. MOblock = MO/CIPSIOrbSweepWindow)                                                     
                              
        # scratch space dimension (number of singles/double excitations per CSF) 
        # If scratch is too small, the program may crash.
        CIBufferLength 10240 # ~82kB (factor 8/10³ to get the memory in kB):

        # startup configurations(optional)
        refs { 2 2 2 2 0 }
             { 2 2 2 0 2 }
             end
        end
        
        # natural orbitals with the ICE ansatz
        NatOrbs 1          # generates the .cipsi.nat GWB file containing
	                   # the natural orbitals
```

(sec:modelchemistries.iceci.cclib)=
## 技术说明：`orcacclib`（A Technical Note: `orcacclib`）

最后我们应提及一个技术方面。ICE-CI 中的 CI 过程基于所谓单粒子耦合系数

$$A_{pq}^{IJ} = \left< I | E_p^q | J \right>$$

其中 $A_{pq}^{IJ}$ 是耦合系数，$I$ 与 $J$ 是组态状态函数（CSF），
$E_p^q$ 是将一个电子从轨道 $p$ 激发到轨道 $q$ 的无自旋激发算符。
这些耦合系数的取值只依赖于 CSF $I$ 与 $J$ 之间的逻辑关系，而不依赖于
$I$、$J$、$p$、$q$ 的绝对取值。事实上，它们只依赖于 $I$ 中未配对电子的数目
以及两个 CSF 所对应的总自旋 $S$。因此原型系数可以预先列表。
这通常在 CI 运行开始时完成。然而在 ICE-CI 中它可能必须重复几十次，
而且对大量开壳层（比如 14 个）而言，该过程既费时又费内存。

为减轻计算负担，我们提供了一个小程序，为给定总自旋 $S$（更确切地说是多重度
$M = 2S + 1$）和最大开壳层数列表耦合系数。该程序名为 `orcacclib`。调用方式为：

```orca
orca_cclib Mult MaxNOpen
```

或者——如果你想加快 cclib 的生成：

```orca
mpirun -np 4 /full_path/orca_cclib_mpi Mult MaxNOpen cclib  # using 4 processes
```

它将在当前目录产生一系列文件 orcacc.el.mult.nopen（电子密度耦合系数）与
orcacc.sp.mult.nopen（自旋密度耦合系数）。这些是二进制文件，可以复制到任意目录。
通过设置到该目录的路径来指示程序读取这些系数（而不是每次重新计算）：

```orca
# My Job
! def2-SVP Auto-ICE
%cclib "/user/me/orca/cclib/orcacc"
```

文件名的其余部分将由程序自动添加。该选项可节省巨量时间。
耦合系数库只需为所需的多重度制作一次。实际上限为 14-16 个开壳层。
如果你通过某种提交脚本在集群上运行计算，必须确保所提供的 `cclib` 路径
能从计算节点访问。
