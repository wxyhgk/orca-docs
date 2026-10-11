### singles Fock 项

在大多数 MDCI 计算中，有一个中间量非常类似于 SCF Fock 矩阵，并且有类似的高效计算方法。下面简要讨论所谓的 singles Fock 项，在闭壳层情况下其形式为

$$G(\mathbf{t}_1)_{pq}=\sum_{jb}t_b^j(2(pq|jb)-(pj|qb))=\sum_{\mu\nu}c_\mu^pc_\nu^qG(\mathbf{t}_1)_{\mu\nu},$$

singles Fock 矩阵可以通过从原子轨道（AO）基组中
的对应量（$G(\mathbf{t}_1)_{\mu\nu}$）变换得到

$$G(\mathbf{t}_1)_{\mu\nu}=\sum_{jb}t_b^j(2(\mu\nu|jb)-(\mu j|\nu b))=\sum_{\kappa\tau}P(\mathbf{t}_1)_{\kappa\tau}(2(\mu\nu|\kappa\tau)-(\mu\kappa|\nu \tau)),
$$ (eq:sfock)

其中

$$P(\mathbf{t}_1)_{\kappa\tau}=\sum_{jb}t_b^jc_\kappa^jc_\tau^b$$

是 singles Fock 情况下 SCF 密度矩阵的类似物。对于
singles Coulomb（$J(\mathbf{t}_1)_{\mu\nu}$）情况，密度可以对称化
（$\tilde{P}(\mathbf{t}_1)_{\kappa\tau}=P(\mathbf{t}_1)_{\kappa\tau}+P(\mathbf{t}_1)_{\tau\kappa}$），
并且可以使用恒等分解（resolution of identity）近似

$$J(\mathbf{t}_1)_{\mu\nu}=\sum_{\kappa\tau}\tilde{P}(\mathbf{t}_1)_{\kappa\tau}(\mu\nu|\kappa\tau)\approx\sum_{AB}\sum_{\kappa\tau}\tilde{P}(\mathbf{t}_1)_{\kappa\tau}(\mu\nu|r_{12}^{-1}|A)V_{AB}^{-1}(B|r_{12}^{-1}|\kappa\tau),$$

其中 $A, B$ 是 RI/DF 辅助拟合基组的元素。注意
({eq}`eq:sfock`) 中的因子 2 由对称化来处理。由于我们使用对称密度，可以像 SCF 情况下那样使用相同的高效例程来
求值 singles Coulomb 项，
参见 {ref}`sec:essentialelements.ri.rij` 和
{ref}`sec:essentialelements.ri.splitrij`。

对于交换项（$K(\mathbf{t}_1)_{\mu\nu}$），一种可能是
使用 COSX 近似
（参见 {ref}`sec:essentialelements.ri.rijcosx`）

$$K(\mathbf{t}_1)_{\mu\nu}=\sum_{\kappa\tau}P(\mathbf{t}_1)_{\kappa\tau}(\mu\kappa|\nu\tau)\approx\sum_gQ_{\mu g}\sum_{\tau}A_{\nu\tau}(\mathbf{r}_g)\sum_{\kappa}P(\mathbf{t}_1)_{\kappa\tau}X_{\kappa g},$$

COSX 例程也能够处理非对称密度，因此这里可以像 SCF 情况下一样使用它。

另一种可能是对交换使用 RI（RIK），

$$K(\mathbf{t}_1)_{\mu\nu}=\sum_{j\kappa\tau}c_\kappa^jC(\mathbf{t}_1)_\tau^j(\mu\kappa|\nu\tau)\approx\sum_{jAB}(\mu j|r_{12}^{-1}|A)V_{AB}^{-1}(B|r_{12}^{-1}|\nu\tilde{j}),$$

其中

$$C(\mathbf{t}_1)^j_\tau=\sum_{b}t_b^jc_\tau^b,$$

$\tilde{j}$ 是使用 $C(\mathbf{t}_1)$ 变换后的"轨道"。

使用这些近似，总的 singles Fock 项有两种近似：由简单关键词 RCSinglesFock 调用的 RIJCOSX
和由 RIJKSinglesFock 调用的 RIJK，参见
{ref}`sec:modelchemistries.mdci.moduleuse`。对于正则和
LPNO 方法，默认程序选择 SCF 计算中使用的相同近似。DLPNO2013 默认使用 RIJCOSX，而在
DLPNO 中，singles Fock 项也通过 SinglesFockUsePNOs 使用 PNO 求值，
参见 {ref}`sec:modelchemistries.mdci.localcorrelation`。这种行为也可以通过 method 块中的关键词来更改。

```orca
%method RIJKSinglesFock 1   # 0 false, 1 true
        RCSinglesFock   0   # 0 false, 1 true
end
```



(sec:modelchemistries.mdci.densities)=
## 耦合簇密度
```{index} Coupled-Cluster Density
```

如果你主要习惯于 Hartree-Fock 或 DFT 计算，密度矩阵的计算或多或少是 trivial 的，并且与自洽场方程的求解一起自动完成。不幸的是，在耦合簇理论中情况并非如此（MP2 理论中也不是）。根本原因在于，在耦合簇理论中，期望值中指数 $e^{\hat T}$ 的展开

$$D_{pq}^{} = \frac{\langle\Psi |E_p^q|\Psi\rangle }{\langle\Psi |\Psi\rangle }
= \frac{\langle e^{\hat T}\Psi _0|E_p^q|e^{\hat T}\Psi _0\rangle }{\langle e^{\hat T}\Psi _0|e^{\hat T}\Psi_0\rangle }$$

只有在耗尽所有可能的激发能级时才终止，即
如果参考行列式 $\Psi _0$（通常是
HF 行列式）中的所有电子都从占据轨道空间激发到
虚轨道空间（这里 $D_{pq}^{}$ 表示一阶密度
矩阵，$E_p^q$ 是自旋迹二次量子化轨道替换
算符，$\hat T$ 是簇算符）。因此，直接应用这些方程代价太高。不过，
可以展开指数并只保留
线性项。这定义了一个线性化密度，它与从线性化耦合簇
理论（CEPA/0）计算的密度一致。与 CEPA/0 密度的差别在于求值时使用的是收敛的
耦合簇振幅。这个密度很容易计算，求值的计算量
很低。因此，这是在耦合簇运行中可以轻松产生的密度。然而，它并不是
耦合簇专家们认可的密度。

耦合簇理论中密度这一主题是从响应理论的观点来处理的。设想向哈密顿量添加如下形式的微扰

$$ H_{}^{(\lambda)} = \lambda \sum\nolimits_{pq} {h_{pq}^\lambda E_p^q} $$

那么总是可以将总能量的一阶导数写成如下形式：

$$ \frac{{dE}}{{d\lambda}} = \sum\limits_{pq} {D_{pq}^{\text{(response)}}h_{pq}^\lambda}$$

这是一个很好的结果。量 $D_{pq}^{\text{(response)}}$ 就是
所谓的响应密度（response density）。在 CC 理论中能量不是通过对能量泛函进行变分优化得到的，因此
能量必须替换为如下拉格朗日量（Lagrangian）：

$$ L_{CC}= \langle \Phi_0 | \bar H | \Phi_0 \rangle + \sum_\eta \lambda_\eta \langle \Phi_\eta | \bar H | \Phi_0 \rangle
 + \sum_{ai} f_{ai} z_{ai}$$

这里 $\langle \Phi_\eta |$ 表示任何激发行列式（单激发、
双激发、三激发、...）。有两组拉格朗日乘子：量 $z_{ai}$ 通过使 Fock
矩阵的非对角块为零来保证受微扰的波函数
满足 Hartree-Fock 条件，量 $\lambda_{\eta}$ 保证
耦合簇关于振幅的投影方程
得到满足。如果两组条件都满足，那么
耦合簇拉格朗日量就简单地求值为耦合簇
能量。耦合簇拉格朗日量可以关于拉格朗日乘子 $z_{ai}$ 和 $\lambda_{\eta}$ 取驻定。响应密度
通过下式定义：

$$ \frac{dL_{CC}}{d\lambda} = \sum_{pq}D_{pq}^{\text{(response) }}h_{pq}^\lambda $$

该方程中出现的密度 $D_{pq}$ 不具有从期望值产生的密度那样的性质。
例如，响应密度可以有低于 0 或大于 2 的本征值。然而在实践中，响应密度是耦合簇理论中最好的"密度"。

不幸的是，耦合簇响应密度的计算相当复杂，因为需要求解额外的方程组
来确定 $z_{ai}$ 和 $\lambda_{\eta}$。如果只求解
$\lambda_{\eta}$ 的方程，就称为"非弛豫"（unrelaxed）
耦合簇密度。如果两组方程都求解，就
称为"弛豫"（relaxed）耦合簇密度。对于大多数用途，
弛豫密度中包含的轨道弛豫效应对耦合簇密度来说很小。之所以如此，是因为
耦合簇方程包含单激发算符的指数 $e^{\hat T_1} = \exp (\sum_{ai} t_a^iE_i^a)$。这
带来了大部分轨道弛豫效应。事实上，用算符
$\hat\kappa  = \sum_{ai} \kappa_a^i(E_i^a - E_a^i)$ 替换 $\hat T_1$ 算符将提供全部的
轨道弛豫，从而导致"轨道优化
耦合簇理论"（OOCC）。

不出所料，确定系数 $\lambda_{\eta}$ 的方程（Lambda 方程）与耦合簇振幅方程本身一样复杂。因此，非弛豫耦合簇密度矩阵的计算大约是耦合簇能量计算的两倍贵（但
如果程序组织得当，项可以复用，而且 Lambda 方程是线性方程，比
非线性振幅方程收敛得稍好一些，因此并没有那么贵）。

ORCA 基于 Lambda 方程为闭壳层和开壳层体系提供非弛豫耦合簇密度
的计算。如果需要完全弛豫的耦合簇密度，ORCA 仍然
提供轨道优化耦合簇双激发方法（OOCCD）。这与完全弛豫的 CCSD 密度矩阵
并不完全等价，因为使用了算符 $\hat\kappa$ 而不是 $\hat T_1$。然而，
结果非常接近，当预计轨道弛豫效应很大时，轨道优化耦合簇双激发是
首选方法。

就 ORCA 关键词而言，耦合簇密度通过以下关键词获得：

```orca
#
# coupled-cluster density
#
%mdci  density   none
                 linearized
                 unrelaxed
                 orbopt
       end
```

它将与 CCSD 或 QCISD 一起工作（在 OOCCD 情况下 QCISD 和 CCSD 是
相同的，因为没有单激发）。请注意，CCSD(T) 的非弛豫密度**不可**用。

除了在 mdci 块中使用密度选项 "orbopt" 外，OOCCD
也可以通过使用关键词来调用：

```orca
! OOCCD
```

(sec:modelchemistries.mdci.staticdynamic)=
## 静态相关与动态相关
```{index} Static Correlation, Dynamic Correlation
```

让我们来看一个单参考相关方法的"滥用"，（非常表面地）研究一个单 HF 行列式无法很好描述的体系。这在 C$_2$H$_4$ 双键的扭转中就已经发生了。在 90$^{\circ}$ 扭转
角时，该体系表现得像双自由基，应当用多参考方法描述（参见第
{ref}`sec:modelchemistries.casscf` 节）

(fig:1)=
```{figure} ../../images/61.*

沿 C$_2$H$_4$ 扭转坐标的刚性扫描。插图
显示 CCSD 计算的 T$_1$ 诊断量。
```

如 {numref}`fig:1` 所见，当接近 90$^{\circ}$ 扭转角时能量急剧上升。HF 曲线实际上是不连续的，并且在 90$^{\circ}$ 有一个尖点。一个简单的
CASSCF(2,2) 计算立即修复了这一点，给出光滑的势能面。
动态相关在 CASSCF(2,2) 方法之上用 MRACPF 方法处理如下：

```{literalinclude} ../../orca_working_input/C05S01_049.inp
:language: orca
```

这是这个问题的参考计算。可以看到 RHF 曲线远偏离 MRACPF 参考，但 CASSCF 计算
非常接近。因此，动态相关对这个问题并不重要！它看起来重要只是因为 RHF 行列式是一个很差的
选择。MP2 相关能不足以修复 RHF 结果。CCSD 方法更好但仍然达不到
定量精度。最后，CCSD(T) 曲线非常接近 MRACPF。这对于总能量也成立（{numref}`fig:2` 的插图），它们彼此
相差不超过 2--3 mEh。因此，在这种情况下，人们用强大的 CCSD(T) 方法以不恰当的方式来
描述一个具有多参考特征的体系。尽管如此，CCSD(T) 的成功表明该方法即使在棘手的
情况下也多么稳定。CCSD 和 CCSD(T) 的"警报"是所谓的
"T$_1$-诊断量"[^6]，也显示在 {numref}`fig:2` 中。经验法则
是，当诊断量的值大于 0.02 时，结果
不可信。在这个计算中我们还没有完全达到
这个临界点，尽管 T$_1$ 诊断量在 90$^{\circ}$ 扭转附近
急剧上升。

(fig:2)=
```{figure} ../../images/62.*

沿扭转坐标 C$_2$H$_4$ 的 CCSD(T) 和 MRACPF 总能量的比较。插图显示差值
E(MRACPF)-E(CCSD(T))。
```

计算成本（不考虑三重激发）是这样的：CCSD
方法最贵，其次是 QCISD
（便宜约 10%）和所有其他方法（比 CCSD 便宜约 50% 到
两倍）。最精确的方法通常是 CCSD(T)。然而，如果省略三重激发，这就不那么清楚了，在这个范围内耦合对方法（特别是 CPF/1
和 NCPF/1[^7]）可以与 CCSD 竞争。

让我们从略微不同的视角来看同样的情况，解离 F$_2$ 的单键。众所周知，
RHF 近似对这个分子完全失效，预测它是
不成键的。同样我们使用了一个太小的基组来获得定量
结果，但足以说明原理。

我们首先用 MRACPF 方法生成一个"参考"势能面：

```{literalinclude} ../../orca_working_input/C05S01_050.inp
:language: orca
```

注意我们从外向内扫描。这有助于程序找到
正确的势能面，因为在大距离下
$\sigma$ 和 $\sigma^{\ast}$ 轨道能量接近，并落在
CASSCF 计算所需的 $2\times2$ 窗口内（参见
第 {ref}`sec:modelchemistries.casscf` 节）。比较 MRACPF
和 CASSCF 曲线，很明显 MRACPF 过程引入的动态相关
非常重要，它将渐近线（粗略地说就是结合能）改变了几乎两倍
（参见 {numref}`fig:3`）。
在极小值附近（大约到 2.0 Å），CCSD(T) 和 MRACPF 曲线
吻合得非常好，几乎无法区分。超过这个距离，
CCSD(T) 计算开始发散并表现出非物理
行为，而多参考方法能够描述整个
势能面直到解离极限。CCSD 曲线定性上还可以但
有明显的定量缺陷：它预测的极小值键长太短，解离能太高。因此，
即使对于这个相当"简单"的分子，连通
三重激发的效应也非常重要。鉴于这种（相当不愉快的）
情况，简单得多的 CEPA 方法的表现相当
令人满意，因为它预测的极小值和解离能比 CCSD 或 CASSCF 更接近参考 MRACPF 结果。看起来在这个特定情况下 CEPA/1 和 CEPA/2 预测了
正确的结果。

(fig:3)=
```{figure} ../../images/63.*

用一些单参考方法计算的 F$_2$ 分子势能面并与 MRACPF
参考的比较。
```

(sec:modelchemistries.mdci.anos)=
## 相关计算的基组：ANO 的情况

在 HF 和 DFT 计算中，双电子排斥积分的生成和处理通常是
整个计算中最昂贵的步骤。因此，最高效的方法是使用
收缩松散、原函数尽可能少的基组——
Ahlrichs 基组（SVP、TZVP、TZVPP、QZVP、def2-TZVPP、def2-QZVPP）在这一方面
可能是最好的。另一种选择是
极化一致基组 pc-1 到 pc-4，但
它们只对 H-Ar 可用。对于大分子，这样的基组
也能带来高效的预筛选，从而带来高效的
计算。

在高度相关的计算（如 CCSD 和 CCSD(T)）中情况不同，其计算量随基函数数量
急剧增长。此外，计算通常只对
有限数量的基函数可行，并且经常在
积分常规模式下运行，因为存在高角动量基函数，这些函数不断重新计算代价很高。因此，关于基组设计的不同策略似乎是合乎逻辑的。最好使用尽可能少的基函数但使它们尽可能精确。这与原子
自然轨道（atomic natural orbital, ANO）基组的理念相容。这样的基组从
相关的原子计算生成，并为每个基组函数复制给定
角动量的原函数。因此，这些基组
收缩很深、代价高昂，但自然原子轨道构成了
分子计算的优美基础。ORCA 中包含了一组精确且系统的
ANO（ano-pV$n$Z，$n=$ D、T、Q、5）。相关一致
基组（cc-pV$n$Z，$n=$ D、T、Q、5、6,...）的设计也基于相关的策略，它们除了"主"
轨道的最外层原函数和极化函数（这些保持非收缩）外也都是收缩的。

让我们用 H$_2$CO 分子在标准几何下详细研究这个主题，并用
各种基组计算 SCF 和相关能。在评判结果时，应当结合基函数数量和总
耗时来看待总能量。看下表中的数据，很明显，对于给定的基数（cardinal number）（双 zeta 为 2，三重 zeta 为 3，四重 zeta 为 4），
ANO 基组给出的 SCF 能量低得多。使用自 ORCA 2.7.0 起可用的特别优化的 ANO 积分，
计算甚至不比标准基组的贵多少。显然，ANO 基组提供的相关能也是所测试的
12 个基组中最好的。因此，ANO 基组是高度相关计算的很好选择。优势在
早期成员（DZ/TZ）中尤其大。

(tab:4)=
:::{list-table} 高度相关计算的各种基组比较
:header-rows: 1
:stub-columns: 1

* - 基组
  - 基函数数目
  - E(SCF)
  - E$_{\mathbf{C} }$(CCSD(T))
  - E$_{\mathbf{tot} }$(CCSD(T))
  - 总时间


* - cc-pVDZ
  - 38
  - -113.876184
  - -0.34117952
  - -114.217364
  - 2 
* - cc-pVTZ
  - 88
  - -113.911871
  - -0.42135475
  - -114.333226
  - 40 
* - cc-pVQZ
  - 170
  - -113.920926
  - -0.44760332
  - -114.368529
  - 695
* - def2-SVP
  - 38
  - -113.778427
  - -0.34056109
  - -114.118988
  - 2
* - def2-TZVPP
  - 90
  - -113.917271
  - -0.41990287
  - -114.337174
  - 46
* - def2-QZVPP
  - 174
  - -113.922738
  - -0.44643753
  - -114.369175
  - 730
* - pc-1
  - 38
  - -113.840092
  - -0.33918253
  - -114.179274
  - 2 
* - pc-2
  - 88
  - -113.914256
  - -0.41321906
  - -114.327475
  - 43 
* - pc-3
  - 196
  - -113.922543
  - -0.44911659
  - -114.371660
  - 1176 
* - ano-pVDZ
  - 38
  - -113.910571
  - -0.35822337
  - -114.268795
  - 12 
* - ano-pVTZ
  - 88
  - -113.920389
  - -0.42772994
  - -114.348119
  - 113 
* - ano-pVQZ
  - 170
  - -113.922788
  - -0.44995355
  - -114.372742
  - 960
:::

(fig:4)=
```{figure} ../../images/64.*

各种基组相对于 ano-pVQZ 基组的高度相关计算误差（Eh）。
```

让我们在 {numref}`tab:5` 中再看一个例子：用 MP2
方法计算的 N$_2$ 分子优化结构随基组的变化*（这些计算比较古老，来自
ano-pVnZ 基组尚不存在的时代。今天，ano-pVnZ 会是首选）*。

这里最高质量的基组是 QZVP，它也给出最低的
总能量。然而，该基组包含直到 g 函数并且非常昂贵。不使用 g 函数和一组 f 函数（如 TZVPP 中那样）对
计算结果有明显影响，导致键长被
高估 0.2 pm——变化很小，但对于
这类基准计算仍然显著。缺少第二组
d 函数的 TZVP 基组在键长、结合能和电离
势上造成的误差出奇地小，尽管删除第二组
d 集"花费"的总能量超过 20 mEh（与 TZV(2d,2p) 相比），与更大的 TZVPP 相比更是如此。

较小的 DZP 型基组会在计算的
键长上产生 1--2 pm 量级的显著误差，这再次强调了这样的基组对于相关分子计算确实太小——
ANO-DZP 基组过于偏向原子，而"常规的"面向分子的 DZP 基组
（如 SVP）的 d 集是为覆盖极化而不是
相关而设计的（相关 d 函数比极化
d 函数更陡）。非常经济的 SVP 基组的表现应当被认为是很好的，而且（有点令人惊讶地）比 cc-pVDZ
稍好，尽管它给出的绝对能量更高。

看 MP2 层面计算的（未做 ZPE 校正的）结合能得到的图景基本相同——
最大的基组 QZVP 给出最大的结合能，而较小的基组
低估了它。DZP 型基组的误差相当大
（$\approx$ 2 eV），因此使用这样的基组时应当谨慎。

(tab:5)=
:::{list-table} 相关计算的各种基组比较。
:header-rows: 1
