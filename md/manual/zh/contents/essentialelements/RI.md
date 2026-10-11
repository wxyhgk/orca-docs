```{index} Resolution-of-the-Identity (RI)
```

(sec:essentialelements.ri)=
# 分辨率恒等式（Resolution-of-the-Identity, RI）

加速 DFT 计算的一种非常高效且成熟的方法是分辨率恒等式（resolution-of-the-identity，RI）技术，也称为密度拟合（density fitting）{cite}`whitten1973chem,baerends1973chem,dunlap1979chem,vanalsenoy1988comp,kendall1997theor,eichkorn1995chem,eichkorn1997theor`。针对库仑（Coulomb）部分和 Hartree-Fock 交换部分（参见 [Hartree-Fock](sec:essentialelements.hartreefock) 和[杂化 DFT](sec:modelchemistries.dft.hybriddft)）有各种变体。ORCA 中可用的选项包括 [RI-J](sec:essentialelements.ri.rij)、[Split-RI-J](sec:essentialelements.ri.splitrij)、[RIJONX](sec:essentialelements.ri.rijonx)、[RI-JK](sec:essentialelements.ri.rijk) 和 [RIJCOSX](sec:essentialelements.ri.rijcosx)。

:::{admonition} 关于 ORCA 中 RI 的若干说明（Some Notes on RI in ORCA）
:class: note
* 任何 RI 近似都需要选择足够大的[辅助基组（auxiliary basis set）](sec:essentialelements.basisset.aux)。
* 使用 `def2/J` 辅助基的 [Split-RI-J](sec:essentialelements.ri.splitrij) 是[非杂化 DFT](sec:modelchemistries.dft.gga) 的默认选项。
* 使用 `def2/J` 辅助基的 [RIJCOSX](sec:essentialelements.ri.rijcosx) 是[杂化 DFT](sec:modelchemistries.dft.hybriddft) 的默认选项。
* 当[标量相对论哈密顿量](../essentialelements/relativistic.md)与全电子基组一起使用时，可以选择 `SARC/J` 作为通用[辅助基组](../essentialelements/basisset.md)。其他选择记录在[基组章节](sec:essentialelements.basisset)中。
* 一般推荐使用 RI，因为其引入的误差非常小。由此带来的加速还使得对大体系使用更大的[基组](../essentialelements/basisset.md)成为可能，这将显著改善结果。
* RI 近似的默认使用可通过 `!NORI` 关键字关闭（不推荐！）。
* 如果你不想依赖 RI 近似，一个合理但不够方便的做法是先收敛一个 RI-J 计算，再把得到的轨道作为精确库仑项计算的初始猜测。这通常几个循环内即可收敛，且总执行时间仍低于直接用精确库仑处理收敛计算。
:::

(sec:essentialelements.ri.rij)=
## RI-J
```{index} RI-J
```

:::{admonition} 注意
:class: note
这是非杂化 DFT 的默认选项！可用 `!NORI` 关闭。
:::

一种非常有用、能大幅加速 DFT 计算（除非分子非常大）的近似就是所谓的"RI 近似"

RI 是"Resolution of the identity"（分辨率恒等式）的缩写。简言之，由*基函数乘积*产生的电荷分布用*辅助基函数*的线性组合来近似。

$$\phi_{i} \left({ \vec{{r} }} \right)\phi_{j} \left({ \vec{{r} }}
\right)\approx \sum\limits_k { c_{k}^{ij} \eta_{k} (\mathrm{\mathbf{r} }) }
$$ (eqn:15)

确定展开系数 $c_{k}^{ij}$ 有多种不同的方法。早些时候，Almlöf 及其合作者 {cite}`vahtras1993chem` 证明，对于电子排斥积分的近似，最佳选择是最小化*剩余排斥（residual repulsion）*。

:::{admonition} 注意
:class: note
RI 方法背后的基本理论早已为人所知，至少从 20 世纪 60 年代末起，与 RI 近似类似的方法就已被使用——主要在"近似从头算方法"的背景下，如 LEDO、PDDO 和 MADO，也在 70 年代中后期由 Baerends、Dunlap 等人用于密度泛函理论 {cite}`baerends1973chem, dunlap1979chem, vanalsenoy1988comp, whitten1973chem`
:::

定义：

$$R_{ij} \equiv \phi_{i} \left({ \vec{{r} }} \right)\phi_{j} \left({\vec{{r} }} \right)-\sum\limits_k { c_{k}^{ij} \eta_{k} \left({ \vec{{r} }}
\right)}
$$ (eqn:16)

以及

$$T_{ij} =\int{ \int{ R_{ij} \left({ \vec{{r} }} \right)\frac{1}{\left|{\vec{{r} }-{\vec{{r} }}'} \right|}R_{ij} \left({ \vec{{r} }}
\right)d^{3}rd^{3}{r}'} }
$$ (eqn:17)

确定使 $T_{ij}$ 最小化的系数得到

$$\mathrm{\mathbf{c} }^{ij} =\mathrm{\mathbf{V} }^{-1}\mathrm{\mathbf{t} }^{ij}
$$ (eqn:18)

其中：

$$t_{k}^{ij} =\left\langle { \phi_{i} \phi_{j} \left|{ r_{12}^{-1} }
\right|\eta_{k} } \right\rangle$$ (eqn:19)

$$V_{ij} =\left\langle { \eta_{i} \left|{ r_{12}^{-1} } \right|\eta_{j} }\right\rangle$$ (eqn:20)

于是，普通的双电子积分变为

$$\begin{aligned}
  \left\langle { \phi_{i} \phi_{j} \left|{ r_{12}^{-1} } \right|\phi_{k}
    \phi_{l} } \right\rangle &\approx \sum\limits_{p,q} { c_{p}^{ij} c_{q}^{kl} V_{pq} } \\
  &=\sum\limits_{p,q} {V_{pq} \sum\limits_r { \left({ \mathrm{\mathbf{V} }^{-1} } \right)_{pr} t_{r}^{ij} }
    \sum\limits_s { \left({ \mathrm{\mathbf{V} }^{-1} } \right)_{qs} t_{s}^{kl} } } \\
  &=\sum\limits_{r,s}
    {\left({ \mathrm{\mathbf{V} }^{-1} } \right)_{rs} t_{r}^{ij} t_{s}^{kl} }
\end{aligned}
$$ (eqn:21)

总库仑能变为

$$\begin{aligned}
  E_{J} &=\sum\limits_{i,j} { \sum\limits_{k,l} { P_{ij} P_{kl} \left\langle {\phi_{i} \phi_{j} \left|{ r_{12}^{-1} } \right|\phi_{k}
    \phi_{l} }\right\rangle} } \\
  &\approx \sum\limits_{i,j} { \sum\limits_{k,l} { P_{ij} P_{kl} \sum\limits_{r,s} { 
    \left({ \mathrm{\mathbf{V} }^{-1} } \right)_{rs} t_{r}^{ij} t_{s}^{kl} } } } \\
  &=\sum\limits_{r,s} { \left({ \mathrm{\mathbf{V} }^{-1} } \right)_{rs} }
    \underbrace{ \sum\limits_{i,j} { P_{ij} t_{r}^{ij} } }_{\mathrm{\mathbf{X} }_{r}}
    \underbrace{ \sum\limits_{k,l} { P_{kl} t_{s}^{kl} } }_{\mathrm{\mathbf{X} }_{s}}
\end{aligned}
$$ (eqn:23) 

其中 $\mathrm{\mathbf{P} }$ 是总密度矩阵。

以类似方式可以计算 Kohn-Sham 矩阵的库仑贡献。这种近似有显著优点：需要存储的量只有矩阵 $\mathrm{\mathbf{V} }^{-1}$（只依赖两个指标）和三指标辅助积分 $t_{r}^{ij}$。与四指标排斥积分列表相比，这大大降低了存储需求。此外，双指标和三指标电子排斥积分比四指标积分更容易计算，从而进一步缩短了处理时间。而且，库仑能和 Kohn-Sham 矩阵贡献可以通过简单的向量/矩阵运算快速组装，带来很大的时间节省。这是因为每个辅助基函数 $\eta_{k} \left({ \vec{{r} }} \right)$ 都出现在许多电荷分布 $\phi_{i} \left({\vec{{r} }} \right)\phi_{j} \left({ \vec{{r} }} \right)$ 的展开中。遗憾的是，类似的策略较难（或者说收益较小）应用于 Hartree-Fock 交换项。

如果辅助基组 $\left\{\eta \right\}$ 足够大，该近似的精度也很高。由于任何 DFT 过程本身在 XC 部分数值积分中就有一定（有时相当可观）的噪声误差，因此可以说库仑部分有同样大小的误差完全可以接受，而不会过多影响计算的总体精度。此外，RI 方法引入的误差通常远小于基组不完全性带来的误差。因此，对于纯密度泛函（DF）推荐使用 RI 过程。不过，可能不应直接混用 RI 与非 RI 计算得到的绝对总能量，因为总能量中的误差会累积并随分子尺寸增大而增大，而相对能量中的误差则倾向于相互抵消。

辅助基组有若干选择，将在下一节中描述，它们取决于展开分子轨道所用主 GTO 基组的选择 [^cholesky]。RI 过程需要对辅助基组度量矩阵 $\mathbf{V}$ 求逆，由于 O(N$^{3}$) 标度和辅助基组规模较大，这通常是计算中最耗时的矩阵运算。不过在 ORCA 中这是通过高效的 Cholesky 分解完成的，且在单点计算的启动阶段只执行一次。因此，这一步在实践中通常无关紧要。

在 ORCA 中，RI 近似由如下输入开关控制

```orca
%method
  RI  on   # do use the RI-J approximation
      off  # do not use the RI-J approximation
end
```

:::{admonition} 注意
:class: note
如果使用 RI，你*必须*指定辅助基组（在 `%basis` 部分中或使用相应简单关键字），或使用简单关键字 `!AutoAux`。
:::

[^cholesky]: 可能需要指出的是，该过程中略显笨拙的一步是对辅助积分矩阵 V 求逆，该矩阵很容易变得非常大。矩阵求逆是 $O(N^3)$ 的过程，因此对大分子来说这一步会耗费可观的时间。然而在 ORCA 中这只在计算过程中做一次，而其他限制拟合也精确重现电子数的程序则在每次迭代中都执行类似过程。从 ORCA 2.2.09 起，改用 Cholesky 分解代替矩阵求逆，消除了求解线性方程组方面的任何瓶颈。

(sec:essentialelements.ri.splitrij)=
## Split-RI-J

自 ORCA 2.2.09 起实现了一种改进版的 RI 算法。这种 Split-RI-J 算法给出与标准 RI 算法相同的库仑能，但当基组包含许多高角动量函数（d、f、g 函数）时明显更快。对于小基组，两种算法几乎没有差别，只是 Split-RI-J 比标准 RI 占用更多内存。不过，约 2000 个基函数的计算中 Split-RI-J 只需额外约 13 MB，这对当今硬件来说是微不足道的要求。

Split-RI-J 算法由简单关键字 `!Split-RI-J` 调用。目前 Split-RI-J 仅可用于 SCF 和梯度计算。

:::{admonition} 注意
:class: note
-   如果通过 `!RI` 开启 RI，则 Split-RI-J 算法是默认算法。如果不想使用 Split-RI-J，请同时使用关键字 `!NoSplit-RI-J`
:::

(sec:essentialelements.ri.rijonx)=
## RIJONX 

另一种选择是库仑项用 RI 方法、交换项用标准处理。该方法称为 RIJONX，因为对大分子而言交换项应趋于线性标度。对于 Hartree-Fock 和杂化 DFT 计算，可通过 `!RIJONX` 关键字调用 RIJONX。

```orca
! HF RIJONX
```

对辅助基组的要求与普通 RI-J 方法相同。

```{index} RIJCOSX
```

(sec:essentialelements.ri.rijcosx)=
## RIJCOSX 

由于对纯泛函与杂化泛函之间执行时间的巨大差异感到沮丧，我们开始研究 Hartree-Fock 交换项的近似方法。我们最终提出的方法称为"球链"（chain of spheres）COSX 近似，可以将其视为赝谱（pseudo-spectral）思想的一个变体。其本质是在计算双电子积分时，第一个积分在网格上数值完成，第二个积分（涉及库仑奇点）则解析完成。算法与理论细节见文献 {cite}`neese2009chemphys` 和 {cite}`Helmich-Paris2021a`。将这一处理与库仑项的 [Split-RI-J](sec:essentialelements.ri.splitrij) 方法结合（因此需要库仑拟合基组！），我们设计了 RIJCOSX 近似，可用于加速 Hartree-Fock 和杂化 DFT 计算。注意，这会在 DFT 积分网格之上引入另一个通常明显更小的网格。

:::{admonition} 注意
:class: note
自 ORCA 5 起，RIJCOSX 是杂化 DFT 的默认选项（可用 `!NOCOSX` 关闭）。但对于 HF，默认并不开启。
:::

尤其对于大而精确的基组，这种方式获得的加速非常大——我们观察到高达六十倍！该过程本质上是线性标度的，因此大而精确的计算可以高效进行。RIJCOSX 近似在整个程序中基本都可用。默认情况下，总能量以及能量差的误差在 0.05 $\pm$ 0.1 kcal mol$^{-1}$ 或更小的量级，用大于默认的网格或在没有该近似的情况下运行最后一个 SCF 循环可以使其更小。对键长的影响不到 pm 的几分之一，键角优于零点几度，柔性二面角好到约 1 度左右。就有限的测试而言，在默认设置下振动频率大致精确到 0.1 个波数。

该近似的目标是高效计算交换型矩阵的矩阵元，如文献 {cite}`Helmich-Paris2021a, neese2009chemphys` 所述：

$$K_{\mu \nu } =\sum\limits_{\kappa \tau } { P_{\kappa \tau } } (\mu \kappa
\vert \nu \tau )
$$ (eqn:25)

其中 $\mathrm{\mathbf{P} }$ 是某种密度型矩阵（不一定对称），双电子积分在基组 $\{\varphi \}$ 上定义为：

$$(\mu \kappa \vert \nu \tau )=\int{ \mu (\mathrm{\mathbf{r} }_{1} )\kappa (\mathrm{\mathbf{r} }_{1} )\nu (\mathrm{\mathbf{r} }_{2} )\tau (\mathrm{\mathbf{r} }_{2} )r_{12}^{-1} }
d\mathrm{\mathbf{r} }_{1} d\mathrm{\mathbf{r} }_{2}
$$ (eqn:26)

这里采用的近似可以写成：

$$K_{\mu \nu } \approx \sum\limits_g { X_{\mu g} } \sum\limits_\tau{A_{\upsilon \tau } (\mathrm{\mathbf{r} }_{g} ) } \sum\limits_\kappa{ P_{\kappa \tau
} X_{\kappa g} }
$$ (eqn:27)

这里指标 $g$ 指网格点 $\mathrm{\mathbf{r} }_{g}$，且：

$$X_{\kappa g} =w_{g}^{1/2} \kappa (\mathrm{\mathbf{r} }_{g} )
$$ (eqn:28)

$$A_{\upsilon \tau } (\mathrm{\mathbf{r} }_{g} )=\int{ \frac{\nu (\mathrm{\mathbf{r} })\tau
(\mathrm{\mathbf{r} }) }{\vert \mathrm{\mathbf{r} }-\mathrm{\mathbf{r} }_{g} \vert }d\mathrm{\mathbf{r} }}
$$ (eqn:29)

其中 $w_{g}$ 表示网格权重。因此，第一个积分数值完成，第二个解析完成。注意这破坏了双电子积分的厄米（Hermitian）性质。

公式 {eq}`eqn:27`
也许最好分三步求值：

$$F_{\tau g} =(\mathrm{\mathbf{PX} })_{\tau g}
$$ (eqn:30)

$$G_{\nu g} =\sum\limits_\tau{ A_{\nu \tau } (\mathrm{\mathbf{r} }_{g} )F_{\tau g} }
$$ (eqn:31)

$$K_{\mu \nu } =(\mathrm{\mathbf{XG} }^{+})_{\mu \nu }
$$ (eqn:32)

就这样来看，这些方程与 Friesner 及其合作者自 20 世纪 80 年代中期以来广泛发展和讨论、并在 Jaguar 量子化学软件包中商业化的赝谱方法非常相似。此时的主要区别是，在 Friesner 的公式中出现的是最小二乘拟合算符 $Q_{\kappa g}$，而不是 $X_{\kappa g}$。注意，ORCA 中也实现了拟合过程的类似版本——与 Friesner 的赝谱方法不同——它不需要专门优化的网格。其基本思想是通过把数值重叠"拟合"到解析重叠来消除基组内的网格误差。由其性质所决定，重叠拟合（overlap fitting）在较大基组下应当工作得更好。


(sec:essentialelements.ri.rijcosx.basicusage)=
### 基本用法（Basic Usage）

RIJCOSX 近似可通过 `!RIJCOSX` 关键字调用：

```orca
! HF RIJCOSX 
```

默认情况下，RIJCOSX 将使用 `def2/J` [辅助基组](../essentialelements/basisset.md)。注意，由于 SCF 拟合基与相关拟合基的要求差别很大，还需要另外定义[相关辅助基组](../essentialelements/basisset.md)。例如 [RI-MP2](../modelchemistries/MP2.md) 或[双杂交 DFT](sec:modelchemistries.dft.doublehybriddft) 就属于这种情况。

```orca
! RI-MP2 def2-TZVPP def2/J def2-TZVPP/C RIJCOSX
```

:::{admonition} 注意
:class: note
这是杂化 DFT 的默认选项！COSX 部分可用关键字 `!NOCOSX` 关闭。
:::

(sec:essentialelements.ri.rijcosx.gradient)=
### RIJCOSX 梯度

给定交换矩阵，交换能为（为简洁起见，这里略去了对自旋情形的求和）：

$$E_{\text{X} } =\frac{1}{2}\sum\limits_{\mu \nu } { P_{\mu \nu } K_{\mu \nu } (\mathrm{\mathbf{P} }) }
$$ (eqn:33)

在 ORCA6 之前，COSX 能量贡献的梯度取的是近似形式：

$$\frac{\partial E_{X} }{\partial \lambda }\approx 2\sum\limits_g
{\sum\limits_{\mu \nu } { \frac{\partial F_{\mu g} }{\partial \lambda } } }
 G_{\nu g}
$$ (eqn:34)

其中

$$\frac{\partial F_{\mu g} }{\partial \lambda }=w_{g}^{1/2} \sum\limits_\kappa{P_{\kappa \mu } \frac{\partial X_{\mu g} }{\partial \lambda } }
$$ (eqn:35)

如原始实现论文 {cite}`neese2009chemphys` 所发表。

从 ORCA6 起，这被更新为能量分量的完整导数，包括所有项的导数：网格权重导数、SFitting 矩阵的导数以及 $F$ 和 $G$ 的所有导数 [^a]。因此梯度现在更精确、噪声也更小。如果想改回先前的近似版本（不推荐），只需设置：

[^a]: 理论尚未发表，但很快会发表。

```orca
%method
  cosxgradtype grad_n
  useqgradfit false
end
```

(sec:essentialelements.ri.rijcosx.grids)=
### COSX 数值网格

对于专家用户，交换网格的网格参数可以更精细地控制：

```orca
%method
  IntAccX  Acc1, Acc2, Acc3
  GridX    Ang1, Ang2, Ang3
end
```

这里涉及三个网格：用于最初 SCF 迭代的最小网格（Acc1, Ang1）、一直用到 SCF 结束的中等网格（Acc2, Ang2），以及用于最终能量和梯度求值的最大网格（Acc3, Ang3）。`UseFinalGridX` 可用于开关最后这个网格，但一般不建议更改。关于网格构造的更多细节见 {ref}`sec:essentialelements.numericalintegration`。

(sec:essentialelements.ri.rijcosx.sfitting)=
### SFitting 参数

要修改重叠拟合参数，可以指定如下输入：

```orca
%method
  UseSFitting false   # Same as NoSFitting in the simple input
                      # (Default is true)
  UseQGradFit false   # Uses the SCF fitting matrix for gradient calculations
                      # (Default is true)
end
```

注意，重叠拟合对 HF 和 MP2 梯度同样有效，无需指定任何额外关键字。`UseQGradFit` 参数对梯度使用与能量计算相同的拟合矩阵，自 ORCA6 起这是默认行为。

(sec:essentialelements.ri.rijcosx.partialcontraction)=
### 部分收缩方案（Partial Contraction Scheme）

自 ORCA 5.0 起，通过在交换矩阵计算中使用中间部分收缩（pc）原子轨道基组，可以高效处理一般收缩基组，且不影响结果 {cite}`Helmich-Paris2021a`。取决于基组和元素类型，计算速度可能提升多个数量级。出于测试或基准目的，可以用如下标志在原始基组中进行 K 矩阵计算

```orca
%method
  COSX_PartialContraction false   # No intermediate basis for generally contracted shells
                                  # (Default is true)
end
```
(sec:essentialelements.ri.rijcosx.fullsymmetry)=
### 恢复完全对称性

默认 COSX 算法中的半数值积分方案破坏了双电子积分的置换对称性。我们观察到，这一缺陷常常是迭代算法收敛问题的原因，尤其是对多参考理论 {cite}`Helmich-Paris2022`。自 ORCA 6.0 起提供了一个输入选项，用于保持双电子积分完整的八重置换对称性：

```orca
%method
  COSX_IntSymmetry Full      # Fully symmetrized integrals
                   Standard  # Original COSX algorithm
end
```

完全对称化算法通常能提高数值稳定性，在 TRAH-CASSCF 和 CASSCF 线性响应计算中默认启用。不过，完全对称化算法可能带来额外开销，这取决于 $\mathbf{F}$ 中间量的数目。$\mathbf{F}$ 中间量的数目取决于密度矩阵的对称性（对称 (S)、反对称 (A) 和非对称 (N)）以及是否采用重叠拟合，汇总于下表。

(tab:cosx-full-sym)=
:::{table} 每个密度矩阵对应的 COSX $\mathbf{F}$ 中间量数目

| S fitting                   | P symmetry (S, A, N)                | Number of $\mathbf{F}$ intermediates      |
|:----------------------------|:------------------------------------|:-------------------------------|
| No                          | S / A                               | 1                              |
| No                          | N                                   | 2                              |
| Yes                         | S / A                               | 2                              |
| Yes                         | N                                   | 4                              |
:::

注意，对于对称 (S) 和反对称 (A) 密度，我们分别在最后对交换矩阵进行对称化和反对称化，这使 $\mathbf{F}$ 中间量的数目减少一半。实际计算开销通常并不随 $\mathbf{F}$ 中间量数目线性增长，因为我们只计算一次昂贵的解析积分（$A_{\nu\tau}(\mathbf{r}_g)$），然后再将其与额外的 $\mathbf{F}$ 中间量缩并。根据我们的经验，完全对称化算法的开销大约是原算法的 1.2 到 1.5 倍。

(sec:essentialelements.ri.rijcosx.convergence)=
### COSX 网格与收敛问题

**收敛问题的症状：**不稳定的收敛行为，往往从第一个 SCF 步就开始，也可能在较晚阶段才出现，产生带有"兆哈特里"（megahartree）跳变的荒唐能量值。如果开启了重叠拟合，还可能遇到如下错误信息："Error in Cholesky inversion of numerical overlap"。

当选定的网格难以表示基组时，可能出现收敛问题。这就是线性相关问题的"网格等价物"，如 {ref}`sec:essentialelements.lindep` 中所讨论。还应提到，这里讨论的网格相关问题往往与基组线性相关相伴出现，尽管并非必然。最直接的处理方法是增大积分网格。但这并不总是可取或可行的。

避免 Cholesky 求逆问题的一种方法是关闭重叠拟合（`!NoSFitting`）。然而这意味着数值问题依然存在，只是被忽略了。由于重叠拟合使用数值重叠及其逆矩阵，它对线性相关问题更敏感，因此关闭拟合过程可能带来收敛。这可能是一个务实的——但绝不干净的——解决方案，因为它依赖于数值误差很小这一假设。

另一方面，重叠拟合也提供了一个与基组中所讨论的类似工具来处理线性相关问题。数值重叠的本征值同样可以检查，小值可以筛除。遗憾的是，没有普适的方法来确定这一筛选参数，但典型取值可参考 {ref}`sec:essentialelements.lindep`。

影响求逆方法和拟合矩阵获取的参数有：

```orca
%method
  SFitInvertType Cholesky    # Cholesky inversion (default)
                 Cholesky_Q  # Cholesky + full Q matrix
                 Diag        # Inversion via diagonalization
                 Diag_Q      # Diag + full Q matrix
  SInvThresh     1e-8        # Inversion threshold for Diag and Diag_Q (default 1e-8)
end
```

默认情况下，求逆过程通过 Cholesky 分解进行，因为它是最快的选项。理想情况下，如果基组不是线性相关的，重叠矩阵就是非奇异的。对于奇异矩阵，Cholesky 过程会失败。这里应当指出，即使基函数的重叠不是线性相关的，数值重叠也可能变得线性相关，因此需要一个单独的参数来处理网格相关问题。为此，可以使用对角化过程（`Diag`）代替 Cholesky，并用相应参数筛除属于低于阈值（`SInvThresh`）本征值的本征向量。对于 Cholesky 和对角化过程，也提供"full Q"方法（`Cholesky_Q` 和 `Diag_Q`），对应于使用更精确（未截断）的拟合矩阵。

(sec:essentialelements.ri.rijk)=
## RI-JK
```{index} RI-JK
```

加速杂化 DFT 或 HF 计算中 HF 交换的另一种算法是 Kendall 和 Früchtl 开发的 RI-JK {cite}`kendall1997theor`。它对库仑和交换都使用 RI 近似，并给出对 Hartree-Fock 交换矩阵相当好的近似。要使该近似达到很高精度可能比较困难。但如果分子足够"致密"，与直接 SCF 相比它的速度相当可观。为此有专门的辅助基组（见章节 {ref}`sec:essentialelements.basisset`）。RI-JK 在 ORCA 中实现了 SCF 单点能量，但未实现梯度。对小分子其加速优于 [RIJCOSX](sec:essentialelements.ri.rijcosx)，对中等大小分子（例如 $(\text{gly})_{4}$）两者相当，而对更大的分子 RI-JK 效率低于 RIJCOSX。详细比较见 {numref}`sec:essentialelements.ri.speedcomparison`。RI-JK 的误差通常低于 1 mEh，且误差非常平滑（比 [RIJCOSX](sec:essentialelements.ri.rijcosx) 更平滑）。因此，对于使用大基组的小体系计算，RI-JK 是个好选择；对于大分子的大体系计算，[RIJCOSX](sec:essentialelements.ri.rijcosx) 更好。

:::{admonition} 注意
:class: note
*   RI-JK 需要更大的辅助基组。对于[Karlsruhe 基组](../essentialelements/basisset.md)，有通用的 `def2/JK` 和 `def2/JKsmall` 基组可用。它们大而精确。

*   对于 UHF，RI-JK 的开销大约是 RHF 的两倍。RIJCOSX 则不是这样。

*   RI-JK 可用于常规（conventional）和直接（direct）运行，也可用于 ANO 基组。对于 ANO 基组推荐使用常规模式。
:::

(sec:essentialelements.ri.rijk.basicusage)=
### 基本用法（Basic Usage）

RI-JK 近似可通过 `!RI-JK` 关键字调用：

```orca
! RHF def2/JK RI-JK
```

(sec:essentialelements.ri.speedcomparison)=
## RIJCOSX 与 RI-JK 的速度比较

[RIJCOSX](sec:essentialelements.ri.rijcosx) 与 [RI-JK](sec:essentialelements.ri.rijk) 方法的比较见 {numref}`tab:essentialelements.ri.speedcomparison`。

(tab:essentialelements.ri.speedcomparison)=
:::{table} $\text{(gly)}_{2}$、$\text{(gly)}_{4}$ 和 $\text{(gly)}_{8}$ 完整 SCF 的墙钟时间（秒）比较。数据取自文献 {cite}`Kossmann2009`
|                            |           | **def2-SVP**| **def2-TZVP(-df)**| **def2-TZVPP** | **def2-QZVPP** |
|:--------------------------:|:---------:|:-----------:|:-----------------:|:--------------:|:--------------:|
| **$\text{(gly)}_{2}$**     | *Default* | 105         | 319               | 2574           | 27856          |
|                            |  *RI-JK*  | 44          | 71                | 326            | 3072           |
|                            | *RIJCOSX* | 70          | 122               | 527            | 3659           |
| **$\text{(gly)}_{4}$**     | *Default* | 609         | 1917              | 13965          | 161047         |
|                            |  *RI-JK*  | 333         | 678               | 2746           | 30398          |
|                            | *RIJCOSX* | 281         | 569               | 2414           | 15383          |
| **$\text{(gly)}_{8}$**     | *Default* | 3317        | 12505             | 82774          |                |
|                            |  *RI-JK*  | 3431        | 5452              | 16586          | 117795         |
|                            | *RIJCOSX* | 1156        | 2219              | 8558           | 56505          |
:::

从数据可以明显看出，对小分子 [RI-JK](sec:essentialelements.ri.rijk) 近似是效率最高的选择。对 $\text{(gly)}_{4}$ 这已不再明显。直到 def2-TZVPP 基组，[RI-JK](sec:essentialelements.ri.rijk) 和 [RIJCOSX](sec:essentialelements.ri.rijcosx) 几乎相同，而对 def2-QZVPP，[RIJCOSX](sec:essentialelements.ri.rijcosx) 已经比 [RI-JK](sec:essentialelements.ri.rijk) 快两倍。对于像 $\text{(gly)}_{8}$ 这样的大分子配小基组，[RI-JK](sec:essentialelements.ri.rijk) 改善不大，但对大基组它仍胜过普通的 4 指标计算。另一方面 [RIJCOSX](sec:essentialelements.ri.rijcosx) 则始终更快。它在 def2-TZVPP 上带来约 10 倍加速，在 def2-QZVPP 上可达 50–60 倍。在这里它再次以两倍的优势胜过 [RI-JK](sec:essentialelements.ri.rijk)。

(sec:essentialelements.ri.keywords)=
## 关键字（Keywords）
```{index} Resolution-of-the-Identity Keywords
```

(tab:essentialelements.ri.keywords.simple)=
:::{table} RI 近似的简单输入关键字。
| Keyword                         | Description                                                                                                           |
|:--------------------------------|:----------------------------------------------------------------------------------------------------------------------|
| `RI`                            | 激活 [RI-J](sec:essentialelements.ri.rij)（默认使用 [Split-RI-J](sec:essentialelements.ri.splitrij)）                        |
| `NORI`                          | 关闭 RI 处理                                                                                                             |
| `SplitRIJ`, `Split-RI-J`        | 激活 [Split-RI-J](sec:essentialelements.ri.splitrij)                                                                   |
| `NoSplitRIJK`, `NoSplit-RI-J`   | 激活 [Split-RI-J](sec:essentialelements.ri.splitrij)                                                                   |
| `RIJONX`, `RIJDX`               | 激活 [RIJONX](sec:essentialelements.ri.rijonx)                                                                         |
| `RIJCOSX`, `RIJDX`              | 激活 [RIJCOSX](sec:essentialelements.ri.rijcosx)                                                                       |
| `NORIJCOSX`, `NOCOSX`           | 关闭 RIJCOSX，改为激活 RIJONX                                                                                              |
| `RIJK`, `RI-JK`                 | 激活 [RI-JK](sec:essentialelements.ri.rijk)                                                                            |
| `NoSFitting`                    | 关闭 [SFitting](sec:essentialelements.ri.rijcosx.sfitting)                                                             |
:::

(tab:essentialelements.ri.keywords.block)=
:::{table} RI 近似的 `%method` 模块块输入关键字。
| Keyword                         | Options              | Description                                                                      |
|:--------------------------------|:---------------------|:---------------------------------------------------------------------------------|
| `RI`                            | `on`/`off`           | 开启/关闭 RI（默认：Split-RI-J）                                                         |
| `IntAccX`                       | `<Acc1, Acc2, Acc3>` | 控制交换网格精度参数（参见[数值积分](sec:essentialelements.numericalintegration.SCFkeys)）        |
| `GridX`                         | `<Ang1, Ang2, Ang3>` | 控制交换网格参数（参见[数值积分](sec:essentialelements.numericalintegration.SCFkeys)）          |
| `UseSFitting`                   | `true`/`false`       | 开启 [SFitting](sec:essentialelements.ri.rijcosx.sfitting)（默认：true）              |
| `SFitInvertType`                | `Cholesky`           | 使用 Cholesky 求逆（默认）                                                               |
|                                 | `Cholesky_Q`         | 使用 Cholesky + 完整 Q 矩阵                                                            |
|                                 | `Diag`               | 通过对角化进行求逆                                                                        |
|                                 | `Diag_Q`             | 激活对角化 + 完整 Q 矩阵                                                                  |
| `SInvThresh`                    | `<real>`             | Diag 与 Diag_Q 的求逆阈值（默认：1e-8）                                                     |
| `UseQGradFit`                   | `true`/`false`       | 梯度计算使用 SCF 拟合矩阵（默认：true）                                                        |
| `COSX_PartialContraction`       | `true`/`false`       | 为一般收缩壳层开启中间基组（默认：true）                                                          |
| `COSX_IntSymmetry`              | `full`               | 使用完全对称化的积分                                                                       |
|                                 | `standard`           | 使用原始 COSX 算法                                                                     |
:::
