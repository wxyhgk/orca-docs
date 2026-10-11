```{index} Møller-Plesset Perturbation Theory (MP2)
```

(sec:modelchemistries.mp2)=
# 微扰理论（Perturbation Theory）—— MP2
在本节中，我们讨论二阶 Møller-Plesset 微扰理论（second order Møller-Plesset Perturbation Theory, MP2）及其在 `orca_mp2` 模块中的实现。
更高阶的关联方法（如 MP3 和 MP4 理论）可通过 [AUTOCI 模块](sec:modelchemistries.autoci)中计算机生成的代码获得。
(sec:modelchemistries.mp2.standard)=
## 标准（非 RI）MP2

标准（或全精度）MP2 模块有两个不同的分支。
一个分支用于能量计算，另一个用于梯度计算。

对于标准 MP2 能量，程序执行两次半变换（half-transformations），半变换后的积分以压缩形式存储在磁盘上。这似乎是最高效的方法，也可用于中等大小的分子。只要 I/O 不构成限制，该模块应具有可接受的并行效率。

对于标准 MP2 梯度，程序执行按占据轨道排序的四次四分之一变换（quarter transformations）。在此，程序从大内存（`%maxcore`）中获益巨大，因为这能最大程度地减少需要处理的批次数（batches）。该方法对 I/O 的需求极小。

在"内存模式"（Q1Opt\>0）下，程序基本上同时处理成批的占据轨道。因此，必须有足够的内存在每一趟（pass）中至少处理一个占据 MO。否则 MP2 模块将会失败。因此，对大分子的 MP2 计算可能需要大量内存，通过 RI 近似来完成可能是最高效的。

另外，在"基于磁盘的模式"（Q1Opt$=$-1）下，程序对交换积分进行半变换，并将变换后的积分存储在磁盘上。随后通过箱排序（bin-sort）得到 (11|22) 积分记号下的 AO 算符 $K^{ij} \left(\mu ,\nu\right)=\left(i\mu|j\nu \right)$。
然后使用这些积分构建最终的 K$^{ij}$(a,b)（a,b$=$虚轨道 MO）以及 EMP2 对能贡献。在许多情况下，特别是对较大的分子，这种算法比基于内存的算法高效得多。然而，它对您所用计算机的 I/O 系统的依赖要大得多。重要的是，程序使用标志 `CFLOAT, UCFLOAT, CDOUBLE` 或 `UCDOUBLE` 来存储未排序和已排序的 AO 交换积分。使用哪个标志会影响程序的性能，并在一定程度上影响结果的精度（基于 float 的单精度结果通常精度略低；与双精度结果的偏差在 $\mu$Eh 量级[^1]）。最后，梯度目前仅在基于内存的算法下可用，因为在这种情况下需要的积分集合要大得多。

`! MP2` 命令执行以下操作：(a) 将 `Method` 改为 `HFGTO`，(b) 将标志 `DoMP2` 设为 `true`。程序随后将先执行哈特里-福克 SCF 计算，再用 MP2 理论估算关联能。允许使用 RHF、UHF 和高自旋 ROHF 参考波函数，所执行的 MP2 计算类型（对于高自旋 ROHF 不提供梯度）会根据 `HFTyp` 的值自动选择。如果 SCF 是常规方式进行的，MP2 计算也将按常规方案进行，除非用户强制计算为直接（direct）模式。对于 `SCFMode` $=$`Direct`，MP2 能量求值将完全在积分直接（integral direct）模式下进行。

以下变量可以在常规 MP2 计算的块中调整：

```orca
%mp2
  EMin       -1.5       # orbital energy cutoff that defines the 
                        # frozen core in Eh
  EMax        1.0e3     # orbital energy cutoff that defines the
                        # neglected virtual orbitals in Eh
  EWin        EMin,EMax # the same, but accessed as array 
                        # (respects settings in %method block!)
  MaxCore     256       # maximum amount of memory (in MB) to be 
                        # used for integral buffering
  ForceDirect false     # Force the calculation to be integral 
                        # direct
  RI          false     # use the RI approximation
  F12         false     # apply F12 correction
  Q1Opt                 # For non-RI calculations a flag how to perform
                        # the first quarter transformation
                        #  1 - use double precision buffers
                        #      (default for gradient runs)
                        #  2 - use single precision buffers. This reduces
                        #      the memory usage in the bottleneck step by
                        #      a factor of two. If several passes are re-
                        #      quired, the number of passes is reduced by
                        #      a factor of two.
                        # -1 - Use a disk based algorithm. This respects
                        #      the flags UCFLOAT,CFLOAT,UCDOUBLE and 
                        #      CDOUBLE. (but BE CAREFUL with FLOAT)
                        #      (default for energy runs)
  PrintLevel  2         # How much output to produce. PrintLevel 3 produces
                        # also pair correlation energies and other info.
  DoSCS       false     # use spin-component scaling
  Ps          1.2       # scaling factor for ab pairs
  Pt          0.333     # scaling factor for aa and bb pairs
  Density     none      # no density construction
              unrelaxed # only "unrelaxed densities"
              relaxed   # full relaxed densities
  NatOrbs     false     # calculate natural orbitals
  
  # Generate guess natural orbitals for CASSCF:
  # "TNat" is an alias for natural orbitals with unrelaxed density 
  # omitting amplitudes < TNat. (Default = no truncation).
  TNat        0.0       # good results are obtained with 1e-6 
```

```{note}
在本节中，下标 $i,j,k,\dots$ 指参考行列式中的占据轨道，$a,b,c,\dots$ 指虚轨道，$p,q,r,\dots$ 指来自任一集合的一般轨道，而 $\mu ,\nu ,\kappa ,\tau ,\dots$ 指基函数。
```

(sec:modelchemistries.mp2.ri)=
## RI-MP2
```{index} RI-MP2
```

RI-MP2 模块的性质很直接。程序首先变换三指标积分 $(ia|\tilde{P})$，其中 "$i$" 是占据 MO，"$a$" 是虚 MO，"$\tilde{P}$" 是针对库仑度量（Coulomb metric）正交化的辅助基函数。这些积分存储在磁盘上，即使基组有几千个函数，这也不是问题。积分变换是并行化的，没有特别大的核心内存需求。

在下一步中，按占据标签排序读取积分，并在速率决定的 O(N$^{5})$ 步骤中构建交换算符 $K^{ij}(a,b) = (ia| jb) = \sum_{\tilde{P} }^{\text{NAux} } (ia | \tilde{P})(\tilde{P} | jb)$。这一步通过大型矩阵乘法高效完成，并且并行化效果很好。由交换算符构建 MP2 振幅（amplitudes）和 MP2 能量。程序从大内存（%maxcore）中获得适度的收益，因为这能最大程度地减少批次数，从而减少对积分列表的读取次数。

RI-MP2 梯度也可用。这里，所有必要的中间量都是即时（on the fly）构建的。

在 RI 近似中，引入辅助拟合基（auxiliary fitting basis）$\eta_{P} \left({ \mathrm{\mathbf{r} }} \right)$，然后将库仑度量下的双电子积分近似为：

$$\left({ pq\vert rs} \right)\approx \sum\limits_{PQ} { \left({ pq\vert P} 
\right)V_{PQ}^{-1} \left({ Q\vert rs} \right)} 
$$ (eqn:55)

其中 $V_{PQ} =\left({ P\vert Q} \right)$ 是二指标电子-电子排斥积分。正如 Weigend 和 Häser 首先讨论的那样，闭壳层情形的 RI-MP2 梯度具有如下形式：

$$E_{\text{RI-MP2} }^{x} =2\sum\limits_{\mu \nu P} { \left({ \mu \nu \vert P} 
\right)^{\left( x \right)}\sum\limits_i { c_{\mu i} \Gamma_{i\nu }^{P} } } 
+\sum\limits_{RS} { V_{RS}^{x} \left({ \mathrm{\mathbf{V} }^{-1/2}\gamma \mathrm{\mathbf{V} }^{-1/2} } \right)_{RS} } +
\left\langle { \mathrm{\mathbf{DF} }^{x} } \right\rangle
$$ (eqn:56)

**F** 矩阵导数项的处理与非 RI 情形完全相同，无需进一步讨论。$\Gamma_{ia}^{P}$ 是一个三指标双粒子"密度"：

$$\Gamma_{ia}^{P} =\sum\limits_{jbQ} { \left({ 1+\delta_{ij} } 
\right)\tilde{{t} }_{ab}^{ij} V_{PQ}^{-1/2} \left({ Q\vert jb} \right)} 
$$ (eqn:57)

它通过下式部分变换到 AO 基：

$$\Gamma_{i\nu }^{P} =\sum\limits_a { c_{\nu a} \Gamma_{ia}^{P} } 
$$ (eqn:58)

二指标的类似形式为：

$$\gamma_{PQ} =\sum\limits_{iaR} { \Gamma_{ia}^{Q} \left({ ia\vert R} 
\right)V_{RP}^{-1/2} } 
$$ (eqn:59)

RI 对拉格朗日量（Lagrangian）的贡献计算起来特别方便：

$$L_{ai}^{RI} =\sum\limits_\mu{ c_{\mu a} } \left[{ 2\sum\limits_{PQ\nu } 
{\Gamma_{i\nu }^{P} \left({ \mu \nu \vert Q} \right)V_{PQ}^{-1/2} } } 
\right]$$ (eqn:60)

以类似方式，可以高效地得到对能量加权密度矩阵（energy weighted density matrix）的其余贡献。但请注意，响应算符和 CP-SCF 方程的求解仍然通过传统的四指标积分进行，因为 SCF 算符就是以此方式构建的。因此，虽然三指标积分的导数可以轻松高效地计算，梯度中仍有可分离（separable）贡献，这需要四指标积分的导数。

采用 RIJCOSX 或 RIJDX 近似可以大幅加速 RI-MP2 能量和梯度计算。

(sec:modelchemistries.mp2.energies)=
## 计算 MP2 与 RI-MP2 能量

您可以对 RHF、UHF 或高自旋 ROHF 参考波函数进行常规或积分直接的 MP2 计算。MP3 功能不是 MP2 模块的一部分，但可以通过 MDCI 模块访问。RHF 和 UHF 提供解析梯度。解析 MP2-Hessian 自 ORCA-6.0 起已弃用（deprecated）。默认使用冻结芯（frozen core）近似。对于 RI-MP2，在非限制情形下按照 {cite}`Lochan2007` 计算 $\langle\hat{S}^2\rangle$ 期望值。文献中对 MP2 有广泛的介绍。{cite}`szabo1989modern,mcweeny1992methods,cremer1998ency,saebo1989chem,head1988chem,lauderdale1991chem,knowles1991chem,pople1976int,krishnan1980chem,handy1985theor,weigend1998chem,weigend1997theor,feyereisen1993chem,bernholdt1996chem`

```orcainput
! MP2 def2-TZVP TightSCF
%paras  rCO = 1.20
        ACOH = 120
        rCH  = 1.08
        end
* int 0 1
C 0 0 0 0.00 0.0 0.00
O 1 0 0 {rCO} 0.0 0.00
H 1 2 0 {rCH} {ACOH} 0.00
H 1 2 3 {rCH} {ACOH} 180.00
*
```

```{note}
不使用 RI 近似的 MP2 计算有两种算法。第一种尽可能使用主内存。
第二种使用更多磁盘空间，通常更快（特别是如果您用 `! FLOAT, UCFLOAT 或 CFLOAT` 以单精度运行计算）。内存算法通过在 `%mp2` 块中指定 `Q1Opt >0` 来使用，而基于磁盘的算法是默认的，或通过 `Q1Opt = -1` 指定。梯度目前仅在基于内存的算法下可用。
```

MP2 的 RI 近似{cite}`weigend1998chem,weigend1997theor,feyereisen1993chem,bernholdt1996chem` 也相当容易使用。它能极大地加速计算，而能量差的误差非常小。例如，考虑与之前相同的计算：

```{literalinclude} ../../orca_working_input/C05S01_033.inp
:language: orca
```

一般而言，可以通过在 `%mp2` 块中设置 `RI true` 来开启 RI 近似。需要为关联计算指定适当的辅助基组（"/C"）。请注意，如果使用 RIJCOSX 方法（章节 {ref}`sec:essentialelements.ri.rijcosx`）或 RI-JK 方法（章节 {ref}`sec:essentialelements.ri.rijk`）来加速 SCF 计算，则应指定两个基组：首先是适当的库仑（"/J"）或交换拟合基组（"/JK"），其次是关联拟合基组（"/C"），如下例所示。

```orca
# Simple input line for RIJCOSX:
! RHF RI-MP2 RIJCOSX def2-TZVP def2/J def2-TZVP/C TightSCF

# Simple input line for RI-JK:
! RHF RI-MP2 RI-JK def2-TZVP def2/JK def2-TZVP/C TightSCF
```

MP2 模块还可以进行 Grimme 的自旋分量缩放 MP2（spin-component scaled MP2）{cite}`Grimme2003jcp`。它是 MP2 的一种半经验修正，对 MP2 能量的同自旋和反自旋分量应用不同的缩放因子。通常它给出比 MP2 本身好相当多的结果。

```{literalinclude} ../../orca_working_input/C05S01_034.inp
:language: orca
```

根据 Grimme 的详细评估研究，SCS-MP2 的能量差似乎比 MP2 本身好得多。出于效率考虑，使用 `RI-SCS-MP2` 关键词来利用 RI 近似是有益的。反自旋和同自旋缩放因子可以分别用 `%mp2` 块中的 `PS` 和 `PT` 修改。默认情况下，$\texttt{PS}=6/5$，$\texttt{PT}=1/3$。

:::{note} 注意
在非常大的 RI-MP2 运行中，如果您使用关键词 `! FLOAT`，可以将主内存使用量减少一半。这在梯度计算中比在单点计算中更重要。
能量和梯度与双精度值的偏差应在 $\mu$Eh 和亚 $\mu$Eh 量级。然而，我们遇到过该选项引入大且不可接受误差的情况，特别是在过渡金属计算中。因此建议您谨慎行事并事先检查。
:::

关于使用线性相关（linearly dependent）基组的 MP2 计算，需要提醒一句。例如，这可能发生在非常弥散（diffuse）的基组上（更多信息参见 {ref}`sec:essentialelements.lindep`）。如果在 SCF 过程中从基组中移除了某些向量，这些冗余向量在 MP2 计算中仍以轨道能量为零的"虚"函数形式存在。当冗余向量数量很少时，这通常不严重（而当其数量很大时，可能应该换一个基组）。不过，在 MP2 计算中尽可能避免线性相关的基组是更好的做法。此外，在这种情况下不应使用 `MORead` 和 `NoIter` 关键词读取轨道，因为那会产生错误的结果！

(sec:modelchemistries.mp2.frozencore)=
## 冻结芯选项（Frozen Core Options）

在 MP2 能量和梯度计算中，默认应用冻结芯（Frozen Core, FC）近似。这意味着芯电子不被包含在微扰处理中，因为包含芯电子的动态关联（dynamic correlation）通常对相对能量或几何参数的影响很小。

冻结芯选项可以通过简单输入行中的 `FrozenCore` 或 `NoFrozenCore` 开启或关闭。此外，还可以通过能量窗口来选择冻结轨道：

```orca
%method FrozenCore FC_EWIN end
%mp2 ewin -1.5, 1.0e3 end
```

更多信息和不同选项见章节 {ref}`sec:essentialelements.frozencore`


(sec:modelchemistries.mp2.gradients)=
## MP2 与 RI-MP2 梯度

使用 MP2、RI-MP2、SCS-MP2 和 RI-SCS-MP2 进行几何优化与任何 SCF 方法一样简单。对于冻结芯轨道，任何类型的二阶导数目前都只能用数值方法得到。RI-MP2 支持 RIJCOSX 近似（章节 {ref}`sec:essentialelements.ri.rijcosx`），因此双杂化 DFT 的梯度计算也支持（事实上自 ORCA 5.0 起它是双杂化 DFT 的默认选项）。这在较大的计算中带来大幅加速，特别是当基组较精确时。

```{literalinclude} ../../orca_working_input/C05S01_036.inp
:language: orca
```

该作业的结果为：

```orca
---------------------------------------------------------------------------
Redundant Internal Coordinates

--- Optimized Parameters ---  
(Angstroem and degrees)

Definition                    OldVal   dE/dq     Step     FinalVal
----------------------------------------------------------------------------
1. B(O   1,C   0)                1.2081  0.000488 -0.0003    1.2078   
2. B(H   2,C   0)                1.1027  0.000009 -0.0000    1.1027   
3. B(H   3,C   0)                1.1027  0.000009 -0.0000    1.1027   
4. A(O   1,C   0,H   3)          121.85  0.000026   -0.00    121.85   
5. A(H   2,C   0,H   3)          116.29 -0.000053    0.01    116.30   
6. A(O   1,C   0,H   2)          121.85  0.000026   -0.00    121.85   
7. I(O   1,H   3,H   2,C   0)     -0.00 -0.000000    0.00      0.00   
----------------------------------------------------------------------------
```

仅为展示 RI-MP2 的精度，下面是用 RI-SCS-MP2 代替 SCS-MP2 并添加 def2-TZVP/C 的结果：

```orca
---------------------------------------------------------------------------
Redundant Internal Coordinates

--- Optimized Parameters ---  
(Angstroem and degrees)

Definition                    OldVal   dE/dq     Step     FinalVal
----------------------------------------------------------------------------
1. B(O   1,C   0)                1.2081  0.000487 -0.0003    1.2078   
2. B(H   2,C   0)                1.1027  0.000009 -0.0000    1.1027   
3. B(H   3,C   0)                1.1027  0.000009 -0.0000    1.1027   
4. A(O   1,C   0,H   3)          121.85  0.000026   -0.00    121.85   
5. A(H   2,C   0,H   3)          116.29 -0.000053    0.01    116.30   
6. A(O   1,C   0,H   2)          121.85  0.000026   -0.00    121.85   
7. I(O   1,H   3,H   2,C   0)     -0.00  0.000000   -0.00     -0.00   
----------------------------------------------------------------------------
```

您可以看到，得益于卡尔斯鲁厄（Karlsruhe）小组高效精确的 RI 辅助基组，优化几何结构通过 RI 近似*没有*损失任何东西（一般而言标准 MP2 与 RI-MP2 之间的几何偏差非常小）。因此，RI-MP2 相对于标准 MP2 确实是效率上的实质性改进。

几何梯度可以将 RI-MP2 与 RIJCOSX 方法结合使用来计算。其调用方式与常规 SCF 波函数相同，例如进行具有严格收敛参数的几何优化：
（请注意，您必须为 MP2-Hessian 打开 NumFreq，因为解析的 (RI-)MP2-Hessian 已不再可用）。

```orca
! RI-MP2 def2-TZVPP def2/J def2-TZVPP/C TightSCF RIJCOSX 
! TightOpt
...
```

(sec:modelchemistries.mp2.rijcosxrigrad)=
## RIJCOSX-RI-MP2 梯度

RIJCOSX-MP2 梯度引入了额外的网格。它们有合理的默认设置，因此通常不需要用户干预。不过，也有一些专家选项可用，如下所述。

Z-矢量方程（Z-vector equations）中的 COSX 项在网格上计算，由关键词 `Z_GridX` 和 `Z_IntAccX` 控制，如章节 {ref}`sec:essentialelements.numericalintegration.gridothers` 和 {ref}`sec:essentialelements.cpscf` 中所讨论的。例如，`DefGrid3` CP-SCF COSX 网格可以按如下方式请求：

```orca
%method
  Z_GridX   2     # Lebedev 110-point grid
  Z_IntAccX 3.067 # radial integration accuracy
end
```

用于在 Z-矢量方程右边求值响应算符的网格（例如参见公式 {eq}`eqn:82` 和 {eq}`eqn:RD-DHDFT`）可以用关键词 `Z_GridX_RHS` 独立选择。注意，从 ORCA 5 开始，其用法与 `Z_GridX` 不同——选择是在 RIJCOSX SCF 过程中使用的三个网格之一中进行：初始迭代用的小网格、最终迭代用的中等网格（ORCA 5 中的默认值），以及迭代收敛后更精确求值能量用的大网格。

```orca
%method
  Z_GridX_RHS 1  # small SCF grid
              2  # medium SCF grid (default)
              3  # large SCF grid
end
```

还有一个网格用于求值基函数导数。通过 `! DefGridn` 选择适当的参数（在三个 SCF 网格之外），但用户可以通过显式设置角向（`GridX`）和径向（`IntAccX`）网格来覆盖：

```orca
%mp2 GridX    4       # default 4: angular Lebedev grid 302
     IntAccX  4.871   # radial grid 
end
```


(sec:modelchemistries.mp2.2ndder)=
## MP2 与 RI-MP2 二阶导数
```{index} MP2 Derivatives
```

在 ORCA 中，对于没有冻结芯轨道的计算，MP2、RI-MP2 和双杂化 DFT 方法可以进行解析二阶性质（analytical second-order properties）计算。二阶导数计算中最昂贵的项是四外部贡献（four-external contribution），它可以通过 AO 直接法（默认）或半数值的链球（Chain-of-Spheres）方法求值。如果选择后一种方法，适当的网格参数通过 `! DefGridn` 设置定义。不过，专家用户可以进行更细粒度的指定，如下所示：

```orca
%mp2 KCOpt _AOBLAS          # (default) AO direct with BLAS routines
           _COSX            # semi-numerical evaluation using the COSX method
     KC_GridX    2          # default 2: angular Lebedev grid 110
     KC_IntAccX  4.020      # radial grid 
end
```

或者，所有网格设置都可以在 `%method` 块中定义，如章节 {ref}`sec:essentialelements.numericalintegration.SCFkeys` 中所讨论的。前三个条目定义三个 SCF 网格，第四个条目定义用于基函数导数的 MP2 网格（参见章节 {ref}`sec:modelchemistries.mp2.rijcosxrigrad`），第五个条目定义用于四外部贡献的网格。

```orca
%method
   IntAccX     Acc1,  Acc2,  Acc3,  Acc4,   Acc5
   GridX       Ang1,  Ang2,  Ang3,  Ang4,   Ang5
end
```

(sec:modelchemistries.mp2.properties)=
## MP2 性质、密度与自然轨道

MP2 方法可用于计算电学和磁学性质，如偶极矩、极化率、超精细耦合、g 张量或 NMR 化学屏蔽张量。为此，需要请求适当的 MP2 密度——否则性质将使用 SCF 密度计算！

可以构造两种类型的密度——"非弛豫"（unrelaxed）密度（基本上对应于 MP2 期望值密度）和包含轨道弛豫（orbital relaxation）的"弛豫"（relaxed）密度。如果 SCF 计算也请求了布居分析（population analysis），则对这两组密度都会打印布居分析。这两种密度分别存储为 `JobName.pmp2ur.tmp` 和 `JobName.pmp2re.tmp`。对于开壳层情形，相应的自旋密度也会被构造并存储为 `JobName.rmp2ur.tmp` 和 `JobName.rmp2re.tmp`。

除了密度选项外，用户还可以构造 MP2 自然轨道（natural orbitals）。如果有弛豫密度，程序使用弛豫密度，否则使用非弛豫密度。自然轨道存储为 `JobName.mp2nat`，这是一个 GBW 类型的文件，可以作为其他作业的输入读取（例如，从 MP2 自然轨道启动 CASSCF 计算是合理的）。密度构造可以在输入文件中单独控制（即使不运行梯度或优化）：

```orca
#
# MP2 densities and natural orbitals
#
%mp2  Density none         # no density
              unrelaxed    # unrelaxed density
              relaxed      # relaxed density
      NatOrbs true         # Natural orbital construction on or off
      end
```

下面是对水分子偶极矩和四极矩的计算：

```{literalinclude} ../../orca_working_input/C05S01_037.inp
:language: orca
```

另一个例子是用 MP2 进行简单的 g 张量计算：

```{literalinclude} ../../orca_working_input/C05S01_038.inp
:language: orca
```

注意，NMR 化学屏蔽以及带 GIAO 的 g 张量计算仅在 RI-MP2 下可用。NMR 化学屏蔽的输入如下所示：

```{literalinclude} ../../orca_working_input/C05S01_039.inp
:language: orca
```

注意，默认情况下不关联芯电子，除非出现 `NoFrozenCore` 关键词。

详情参见章节 {ref}`sec:modelchemistries.mp2` 和 {ref}`sec:spectroscopyproperties.properties.eprnmr.MP2magnetic`。


(sec:modelchemistries.mp2.rimp2.response)=
## RI-MP2 与双杂化 DFT 响应性质

从 ORCA 5 开始，RI-MP2（以及双杂化泛函）的电场响应（用于偶极极化率）和磁场响应（用于 NMR 屏蔽和 EPR g 张量）以及核-轨道响应（超精细耦合 $A_\text{orb}$ 项）都由与几何 Hessian 计算所用不同的 RI-MP2 二阶导数实现来处理（{ref}`sec:modelchemistries.mp2.2ndder`）。该代码更高效，全程使用 RI 近似（包括四外部贡献），并支持冻结芯轨道。该实现的详细描述见参考文献 {cite}`Stoychev2018RIMP2NMR,Tran2020RIMP2GIAO`。
考虑以下 GIAO-RI-MP2 NMR 屏蔽计算的输入：

```{literalinclude} ../../orca_working_input/ri-mp2_giao_nmr_details.inp
:language: orca
```

默认情况下，占据块使用微扰正则轨道（perturbed canonical orbitals），即内部轨道旋转系数选为

$$U^{\mathbf B}_{ij} = \frac{F^{(\mathbf B) }_{ij} - S^{(\mathbf B) }_{ij}\varepsilon_{j} }{\varepsilon_{j}-\varepsilon_{i} }$$

这导致 $F^{\mathbf B}_{ij}=0$，从而消除了其对微扰振幅的贡献：

$$
T^{ij,\mathbf B}_{ab} \gets
- \sum_k \left[ T^{ik}_{ab} F_{kj}^\mathbf B + T^{kj}_{ab} F_{ki}^\mathbf B \right]
$$ (eq:MP2-TijB)

如果 $| \epsilon_j - \epsilon_i |<$ `PertCan_EThresh` 或 $|U_{ij}^B| > $ `PertCan_UThresh`，则 $U^{\mathbf B}_{ij}$ 用标准公式选为

$$U^{\mathbf B}_{ij} = - \frac{1}{2} S^{(\mathbf B) }_{ij}$$

并加入公式 {eq}`eq:MP2-TijB` 的相关贡献，除非 $\left|F^{\mathbf B}_{ij}\right|< $ `FCut`。所需的振幅 $\mathbf T^{ik}$ 和 $\mathbf T^{kj}$（若 `UsePertCanOrbs = false` 则为全部振幅）在 `RespStoreT = true` 时存储在磁盘上，否则根据需要重新计算。
后一种选项明显更慢，除非磁盘空间有压力，否则不推荐。类似地，在 RAM 不足的情况下，选项 `RespDijConv = true` 会让 ORCA 将批次中所有振幅（计算 $D_{ij}^\mathbf B$ 所需）存储到磁盘上，而不是保留在内存中。Z-矢量方程右边所需的三指标双粒子密度始终存储在磁盘上。

另请注意，在此实现中，RIJCOSX Fock 响应项用 SCF 网格之一计算，该网格由 `Z_GridX_RHS` 选择（参见章节 {ref}`sec:essentialelements.cpscf`）。

```{index} DLPNO-MP2
```
(sec:modelchemistries.mp2.dlpno)=
## 局域 MP2 计算（DLPNO-MP2）

纯粹基于域（domain）的局域 MP2 方法学可追溯到 Pulay，并由 Werner、Schütz 及其同事进一步发展。ORCA 提供了一种局域 MP2 方法（DLPNO-MP2），它结合了域和局域对自然轨道（local pair natural orbitals）的思想，从而高效地复现 RI-MP2 能量，达到化学精度（chemical accuracy）以内。
其默认阈值的选择使得大约复现 RI-MP2 总关联能的 99.9%，能量差精度达到 $1\,\text{kcal/mol}$ 的几分之一。
由于与其他 DLPNO 方法的复杂关联，推荐阅读章节 {ref}`sec:modelchemistries.mdci.localcorrelation`。RHF 参考波函数的方法完整描述已经发表。{cite}`pinski2015lmp2`

局域 MP2 方法对非常大的分子真正有益，可用于计算含数百个原子的体系的能量。{numref}`fig:DLPNO-MP2-scaling` 展示了线性烷烃链的标度（scaling）行为。请注意，这是一种理想化情形。对于三维分子，与正则 RI-MP2 的交叉点将会更晚出现。

(fig:DLPNO-MP2-scaling)=
```{figure} ../../images/DLPNO_MP2_Scaling.*
DLPNO-MP2 方法在 def2-TZVP 基组下对线性烷烃链使用默认阈值的标度行为。同时展示了相应使用 RIJCOSX 的哈特里-福克计算和 RI-MP2 的时间。
```

由于 DLPNO-MP2 使用辅助基组来求值积分，随着阈值收紧，其能量会系统性地收敛到 RI-MP2。默认设置下 DLPNO-MP2 的计算工作量通常与哈特里-福克计算相当或更低。不过，对于小和中等大小的分子，RI-MP2 甚至比 DLPNO-MP2 更快。

开壳层体系的计算通过 UHF 处理得到支持。虽然大多数近似在 RHF 和 UHF 版本之间是一致的，但 PNO 空间并非如此。**DLPNO-MP2 在 RHF 和 UHF 形式下对闭壳层分子给出不同的能量。在计算涉及开壳层物种的反应能或其他能量差时，闭壳层物种的能量也必须用 UHF-DLPNO-MP2 计算，而不能用 RHF-DLPNO-MP2。** 与正则 MP2 一样，ROHF 参考波函数通过 UHF 机制进行 ROMP2 处理。它与 RHF 版本的 DLPNO-MP2 不一致，这一点不同于 RHF-/ROHF-DLPNO-CCSD 的情形。

下面指出 RHF-DLPNO-MP2 最重要的设计原则：

DLPNO-CCSD(T) 和 DLPNO-MP2 都是线性标度方法（尽管前者的前因子更大）。这意味着如果能进行 DLPNO-MP2 计算，DLPNO-CCSD(T) 通常也触手可及。然而，CCSD(T) 通常比 MP2 准确得多，因此应优先考虑。

必须提供关联拟合基组（correlation fitting set），因为该方法使用 RI 近似。

正则 RI-MP2 能量差通常可复现到 $1\,\text{kcal/mol}$ 的几分之一以内。默认阈值的选择使得大约复现 RI-MP2 总关联能的 $99.9\,\%$。

控制方法精度的首选方式是指定 "LoosePNO"、"NormalPNO" 和 "TightPNO" 关键词。
"NormalPNO" 对应默认设置，无需显式给出。更多细节和详尽的输入参数列表见章节 {ref}`sec:modelchemistries.mp2.dlpno`。注意这些阈值与 DLPNO 耦合簇不同。

从 RI-MP2 和 DLPNO-MP2 得到的结果，或从不同精度设置的 DLPNO-MP2 得到的结果，绝不能混用，例如在计算能量差时。在涉及开壳层物种的计算中，即使是闭壳层分子也需要进行 UHF 处理。

自旋分量缩放的 DLPNO-MP2 计算通过在简单输入行中使用 `! DLPNO-SCS-MP2` 关键词（而非 `! DLPNO-MP2`）来调用。同自旋和反自旋贡献的权重可以按正则 SCS-MP2 方法中所述进行调整。
同样，有一个 `DLPNO-SOS-MP2` 关键词用于设置 SOS-MP2 方法定义的参数（但不涉及拉普拉斯变换（Laplace transformation））。

默认使用冻结芯近似。如果计算中涉及芯轨道，则按章节 {ref}`sec:modelchemistries.mp2.dlpno` 中描述的处理方式进行。

计算可以并行执行。

通过 RIJCOSX 方法加速哈特里-福克计算可能是有益的（需要指定第二个辅助基组）。

与 2013 版 DLPNO 方法学不同，域的选择通过定域 MO $i$ 与投影原子轨道（projected atomic orbitals, PAO）$\tilde\mu'$ 之间的微分重叠 $\sqrt{\int i^2(\mathbf{r}) \tilde\mu'^2 (\mathbf{r}) d\mathbf{r} }$（归一化到 1）进行。相应截断的默认值为 $T_\text{CutDO}=10^{-2}$。

每对定域轨道 $ij$ 的 MP2 振幅用对自然轨道（pair natural orbitals, PNO）$\tilde a_{ij}$ 的基组展开。PNO 通过近似的"半正则"（semicanonical）MP2 对密度 $\mathbf{D}^{ij}$ 的对角化获得。
只有占据数 $>T_\text{CutPNO}$ 的 PNO 被保留，DLPNO-MP2 的默认值为 $T_\text{CutPNO} = 10^{-8}$。对密度由下式给出：

$$\mathbf{D}^{ij} = \mathbf{T}^{ij\dagger} \tilde{\mathbf{T} }^{ij} + \mathbf{T}^{ij} \tilde{\mathbf{T} }^{ij\dagger}
\quad\text{where}\quad
\begin{matrix}T^{ij}_{\tilde\mu\tilde\nu} = -\dfrac{\left(i\tilde\mu \middle| j \tilde\nu\right)}{\varepsilon_{\tilde\mu} + \varepsilon_{\tilde\nu} - F_{ii} - F_{jj} } \\
\tilde{\mathbf{T} }^{ij} = \left(1+\delta_{ij}\right)^{-1} \left( 4\mathbf{T}^{ij} - 2\mathbf{T}^{ij\dagger}\right)\end{matrix}$$

由于 Fock 矩阵的占据块在定域轨道基组中不是对角的，MP2 振幅 $\mathbf{T}^{ij}$ 通过迭代求解以下残差方程（residual equations）组获得（其中 PNO 的下标已省略）：

$$R^{ij}_{\tilde a\tilde b} = \left(i \tilde a \middle| j \tilde b\right) + \left( \varepsilon_{\tilde a} + 
\varepsilon_{\tilde b} - F_{ii} - F_{jj} \right) T^{ij}_{\tilde a\tilde b} - \sum_{k\neq i} \sum_{\tilde c\tilde d} 
F_{ik} S^{ij, kj}_{\tilde a\tilde c} T^{kj}_{\tilde c \tilde d}  S^{kj, ij}_{\tilde d\tilde b} - \sum_{k\neq j} 
\sum_{\tilde c\tilde d} F_{kj} S^{ij, ik}_{\tilde a\tilde c} T^{ik}_{\tilde c \tilde d}  S^{ik, ij}_{\tilde d\tilde 
b} = 0$$

相对于正则 RI-MP2 的误差最大部分由域（`TCutDO`）和 PNO（`TCutPNO`）阈值控制，这些阈值对大多数应用应该是足够的。如果需要更高的精度（例如研究弱相互作用），可以通过 `! TightPNO` 关键词调用更紧的截断判据。相反，可以用 `! LoosePNO` 关键词进行精度较低但更快的计算。更多细节参见表 {numref}`tab:Settings-LMP2`。

拟合域（Fitting domains）通过轨道 Mulliken 布居确定，阈值为 $T_\text{CutMKN} =10^{-3}$。该阈值产生的误差贡献通常比相对 RI-MP2 的总能量偏差小约一个数量级。

在执行局域 MP2 计算之前，定域分子轨道对 $ij$ 会用带偶极近似的 MP2 能量估算以及轨道 $i$ 和 $j$ 之间的微分重叠积分进行预筛选（prescreened）。该过程的选择是保守的，导致的误差极小。

通过忽略关联 Fock 矩阵元 $F_{ik}$ 和 $F_{kj}$ 低于 $F_\text{Cut}=10^{-5}$ 的项，可以显著加速残差求值。由此近似产生的误差通常低于 $1\,\mu\text{E}_\text{h}$，因而可以忽略。

利用原子轨道基组中 MO 和 PAO 系数矩阵的稀疏性（sparsity）来加速大体系的积分变换。系数的截断由参数 $T_\text{CutC}$ 控制。忽略这些系数必须非常小心，以避免不可控的误差。阈值的选择使得误差基本消失。

默认情况下，MP2 模块中芯轨道是冻结的。然而，如果芯轨道参与 MP2 处理，则对涉及至少一个芯轨道的对需要使用更紧的 PNO 截断。为此，芯轨道和价轨道分别定域化。涉及芯轨道的对的截断为 $T_\text{CutPNO} \times T_\text{ScalePNO\_Core}$，其中默认 $T_\text{ScalePNO\_Core}=10^{-2}$。更多细节参见章节 {ref}`sec:modelchemistries.mdci.dlpnocorepno`。

UHF-DLPNO-MP2 实现与 RHF 情形有所不同，特别是在 PNO 的构造方面，如下所述。

每种自旋情形分别获得一组 PAO $\tilde\mu'_\alpha$ 和 $\tilde\mu'_\beta$。

对于 $\alpha\beta$ 对，每种自旋情形需要分别确定 PAO 的对域（pair domains）。例如，$\alpha$ 对域 $\left[i_\alpha j_\beta\right]_\alpha$ 是域 $\left[i_\alpha\right]_\alpha$ 和 $\left[j_\beta\right]_\alpha$ 的并集。后一个域 $\left[j_\beta\right]_\alpha$ 通过评估 $j_\beta$ 与 $\alpha$-自旋 PAO $\tilde\mu'_\alpha$ 之间的空间微分重叠确定。

每个同自旋对需要一组 PNO。反自旋对需要一组 $\alpha$-PNO 和一组 $\beta$-PNO。总计产生四种类型的 PNO 集合。

半正则振幅如下获得，其中 $i,j$ 是自旋轨道，$\tilde\mu\tilde\nu$ 是非冗余自旋 PAO。

$$T^{ij}_{\tilde\mu\tilde\nu} = -\frac{\left\langle ij \middle|\middle| \tilde\mu\tilde\nu \right\rangle}{\varepsilon_{\tilde\mu} + \varepsilon_{\tilde\nu} - F_{ii} - F_{jj} }$$

在同自旋情形下 $\left\langle i_\alpha j_\alpha \middle|\middle| \tilde\mu_\alpha\tilde\nu_\alpha \right\rangle= \left\langle i j \middle| \tilde\mu \tilde\nu \right\rangle- \left\langle i j \middle| \tilde\nu \tilde\mu \right\rangle$，而在反自旋情形下 $\left\langle i_\alpha j_\beta \middle|\middle| \tilde\mu_\alpha\tilde\nu_\beta \right\rangle= \left\langle i j \middle| \tilde\mu \tilde\nu \right\rangle$。

对于反自旋对，$\alpha$-PNO 和 $\beta$-PNO 分别由 $\mathbf{T}^{ij} \mathbf{T}^{ij\dagger}$ 和 $\mathbf{T}^{ij\dagger} \mathbf{T}^{ij}$ 的对角化获得。对于同自旋对，对密度是对称的，只需要一组 PNO。当 PNO 的自然占据数绝对值低于阈值 $T_\text{CutPNO}$ 时，PNO 被丢弃。

对于情形 $R^{i_\alpha j_\alpha}_{\tilde a_\alpha \tilde b_\alpha}$、$R^{i_\beta j_\beta}_{\tilde a_\beta \tilde b_\beta}$ 和 $R^{i_\alpha j_\beta}_{\tilde a_\alpha \tilde b_\beta}$，需要求解以下残差方程：

$$\begin{split}
R^{i_\sigma j_\tau}_{\tilde a_\sigma\tilde b_\tau} =& \left\langle i j \middle|\middle| \tilde a \tilde b 
\right\rangle+ \left( \varepsilon_{\tilde a} + \varepsilon_{\tilde b} - F_{ii} - F_{jj} \right) T^{ij}_{\tilde 
a\tilde b} \\
&- \sum_{k_\sigma \neq i_\sigma} \sum_{\tilde c_\sigma \tilde d_\tau} F_{ik} S^{ij, kj}_{\tilde a\tilde c} T^{kj}
_{\tilde c \tilde d}  S^{kj, ij}_{\tilde d\tilde b} - \sum_{k_\tau \neq j_\tau} \sum_{\tilde c_\sigma \tilde d_\tau} 
F_{kj} S^{ij, ik}_{\tilde a\tilde c} T^{ik}_{\tilde c \tilde d}  S^{ik, ij}_{\tilde d\tilde b} = 0
\end{split}$$

大多数近似在 RHF 和 UHF 方案之间是一致的，PNO 截断除外。这意味着对于 $T_\text{CutPNO}=0$ 的闭壳层分子，结果将会匹配（前提是两个哈特里-福克解相同），但只要 PNO 空间被截断，情况就不是这样。因此，UHF-DLPNO-MP2 能量只应与其他 UHF-DLPNO-MP2 能量比较，即使是闭壳层物种也是如此。

我们发现 UHF-DLPNO-MP2 需要使用更紧的 PNO 阈值。在 NormalPNO 设置下，默认值为 $T_\text{CutPNO} = 10^{-9}$。精度设置的概述参见表 {numref}`tab:Settings-LMP2`。与 RHF 实现一样，涉及芯轨道的对的 PNO 截断会用 $T_\text{ScalePNO\_Core$ 缩放。


DLPNO-MP2 的输入几乎不需要用户指定：

```orca
# DLPNO-MP2 calculation with standard settings
# sufficient for most purposes
! def2-TZVP def2-TZVP/C DLPNO-MP2 TightSCF

# OR: DLPNO-MP2 with tighter thresholds
# May be interesting for weak interactions, calculations with diffuse basis sets etc.
! def2-TZVP def2-TZVP/C DLPNO-MP2 TightPNO TightSCF

%maxcore 2000

*xyz 0 1
... (coordinates)
*
```

显式相关（Explicit correlation）已在 RHF 参考波函数的 DLPNO-MP2-F12 方法学中实现。{cite}`pavosevic2016lmp2f12` 可用的方法是 C（关键词 `! DLPNO-MP2-F12`）和近似程度略高的 D（关键词 `! DLPNO-MP2-F12/D`）。一般推荐方法 D，因为它在带来显著加速的同时相对方法 C 只有很小的误差。除了 MO 和关联拟合基组外，两种 F12 方法还需要 CABS 基组，如下所示。

```orca
# DLPNO-MP2-F12 calculation using approach C
! cc-pVDZ-F12 aug-cc-pVDZ/C cc-pVDZ-F12-CABS DLPNO-MP2-F12 TightSCF

# OR: DLPNO-MP2-F12 calculation using approach D (recommended)
! cc-pVDZ-F12 aug-cc-pVDZ/C cc-pVDZ-F12-CABS DLPNO-MP2-F12/D TightSCF
```

(tab:Settings-LMP2)=
:::{table} DLPNO-MP2 的精度设置（Accuracy settings for DLPNO-MP2）。
| 设置（Setting） |  $T_\text{CutDO}$  | $T_\text{CutPNO}$ (RHF) | $T_\text{CutPNO}$ (UHF) |
|:----------|:------------------:|:-----------------------:|:-----------------------:|
| LoosePNO  | $2 \times 10^{-2}$ |        $10^{-7}$        |        $10^{-8}$        |
| NormalPNO | $1 \times 10^{-2}$ |        $10^{-8}$        |        $10^{-9}$        |
| TightPNO  | $5 \times 10^{-3}$ |        $10^{-9}$        |       $10^{-10}$        |

:::

DLPNO-MP2 特有的选项如下所列。

```orca
%mp2 DLPNO            false  # Do DLPNO-MP2 (also requires RI true)
     TolE             1e-6   # Energy convergence threshold. Default: TolE of SCF
     TolR             5e-6   # Residual convergence threshold. Default: 5 * TolE
     MaxPNOIter       100    # Maximum number of residual iterations
     MaxLocIter       128    # Maximum number of iterations for orbital
                              # localization
     LocMet           AHFB   # Localization method
                              # options: FB, PM, IAOIBO, IAOBOYS, NEWBOYS, AHFB
     LocTol           1e-6   # Localization convergence tolerance
                              # Default: 0.1 * TolG from SCF
     DIISStart_PNO    0      # First iteration to invoke DIIS extrapolation
     MaxDIIS_PNO      7      # length of DIIS vector
     Damp1_PNO        0.5    # Damping before DIIS is started
     Damp2_PNO        0.0    # Damping with DIIS
     MP2Shift_PNO     0.2    # level shift in amplitude update (Eh)
# Truncation parameters:
     TCutPNO          1e-8   # PNO occupation number cutoff (RHF)
                      1e-9   # PNO occupation number cutoff (UHF)
     TScalePNO_Core   1e-2   # Core PNO scaling factor
     TCutDO           1e-2   # Differential overlap cutoff for domain selection
     TCutMKN          1e-3   # Mulliken population cutoff for fitting
                              # domain selection
     FCut             1e-5   # Occupied Fock matrix element cutoff
     TCutPre          1e-6   # Energy threshold for dipole prescreening
     TCutDOij         1e-5   # Maximum differential overlap between screened MOs
     TCutDOPre        3e-2   # Cutoff to select PAOs for domains in prescreening
     TCutC            1e-3   # Cutoff for PAO coefficient truncation
     ScaleTCutC_MO    1.0    # Cutoff for MO truncation: TCutC * ScaleTCutC_MO
     PAOOverlapThresh 1e-8   # Threshold for constructing non-redundant PAOs
end
```

(sec:modelchemistries.mp2.dlpnograd)=
## 局域 MP2 梯度

DLPNO-MP2 方法 RHF 变体的解析梯度已经实现。{cite}`Pinski2018GradientCommunication,Pinski2019` 它是 DLPNO-MP2 能量中所有组分的完整导数，因此预期结果与 DLPNO-MP2 的数值导数一致（扣除噪声）。

一般说明：

目前 UHF-DLPNO-MP2 变体尚未实现梯度。

梯度支持自旋分量缩放的 MP2。

梯度支持双杂化密度泛函。

目前仅支持 Foster-Boys 定域化（localization）。默认收敛器（converger）是 `AHFB`，其收敛容差通过一个常数因子自动受 SCF 轨道梯度容差约束。使用不同的收敛器是可能的，但不鼓励，因为轨道定域化需要足够紧地收敛。

在不计算完整核梯度而计算性质时，应请求弛豫 MP2 密度。

关于几何优化有若干值得记住的要点（并非都特属于 DLPNO-MP2）：

截至 2018 年，我们预计 DLPNO-MP2 梯度对含约 70-150 个原子的体系的几何优化最为有利。即使对含 50-60 个或更少原子的体系，它也可能比 RI-MP2 更快，但时间差异可能不会很大。当然，含 200 个及以上原子的结构可以（而且已经被）优化，但如果需要很多几何步，这可能耗时很长。另一方面，含数百个原子的体系可以进行单点梯度或密度计算。

对于几何优化，DLPNO-MP2 比 GGA 或杂化 DFT 泛函昂贵得多。因此，用一个已在色散校正 DFT 水平上优化过的结构开始几何优化通常是个好主意。

RIJCOSX 可用于大幅加速交换求值。但是，网格设置需要非常小心。网格不够大可能导致平面分子出现非平面畸变等问题。ORCA 5 中更新的默认网格（`DefGrid2-3`）应足够精确以优化中性主族化合物。因此我们推荐这些网格用于一般用途，但在更复杂的情形下仍需仔细检查。即使使用这些网格，计算也比三 zeta 质量（或更大）基组的"常规"哈特里-福克快得多。

也可以使用 RIJONX。

双杂化的交换-关联泛函应使用足够大的网格。SCF 计算只占 DLPNO-MP2 所需时间的一小部分，因为网格不够精确而牺牲质量是浪费计算机时间。

大结构的优化对几何优化器（geometry optimizer）往往是一个挑战。改变信赖半径（trust radius）设置、修改 `AddExtraBonds` 功能的设置或更改几何优化器的其他设置可能会有帮助。有时用一个要求较低的电子结构方法检查几何优化器设置可能是有益的。

最后，几何优化的问题在某些情况下确实可能由 DLPNO 近似引起。对精确计算使用 `LoosePNO` 无论如何都不推荐，而 `NormalPNO` 设置下的困难可能通过切换到 `TightPNO` 得到纠正。

在开发过程中，遇到了若干与轨道定域化 Z-矢量方程相关的困难。我们非常小心地绕开这些问题并使过程尽可能稳健，但有若干设置可以更改。关于这些方面的更多信息，我们建议查阅关于 DLPNO-MP2 梯度的完整论文 {cite}`Pinski2019`。

为轨道定域化 Z-矢量方程实现了几种不同的求解器（solvers）。默认是迭代共轭梯度（conjugate gradient）求解器。作为替代，可以使用 DIIS 加速的 Jacobi 求解器，但它往往不如共轭梯度求解器。此外，对于较小的体系，还有直接求解器（direct solver）作为故障保护（fail-safe）替代。由于线性方程组的维数对 $n$ 个占据轨道为 $n(n-1)/2$，内存需求和浮点运算量分别按 $O(n^4)$ 和 $O(n^6)$ 增长，对大体系使用直接求解器变得不可行。

CPSCF 求解器的设置与正则 MP2 的指定方式相同。

在特定情况下，轨道定域化函数的轨道 Hessian（orbital Hessian）可能有零或接近零的本征值，这会导致奇异的定域化 Z-矢量方程。特别是，这通常是连续简并（continuously degenerate）定域轨道的结果，这些轨道可能（但不一定）出现在某些分子对称性中。{cite}`Scheurer2000` 典型症状是对于没有 DLPNO 近似时期望 MP2 密度本征值在 2 和 0 之间的体系，自然占据数高于 2 或低于 0。

为了绕开上述问题，实现了一个过程来消除定域化函数轨道 Hessian 的奇异或近奇异本征向量。本征值小于 `ZLoc_EThresh`（芯轨道为 `ZLoc_EThresh_core`）的向量将接受修正后的过程。如果程序消除了任何本征向量，检查计算的性质是否合理（或至少检查自然占据数）有时是个好主意。默认情况下 Hessian 的本征向量通过 Davidson 对角化计算，但对较小的体系可以选择直接对角化。

定域化轨道 Hessian 的对角化可以通过将 `ZLoc_EThresh` 设为 0 来完全关闭。

如果"非对称定域化方程残差范数"（Asymmetric localization equation residual norm）超过定域化 Z-矢量方程容差（`ZLoc_Tol`），通常有两个合理的原因：(1) 定域轨道收敛不够紧（`LocTol` 太大）或未收敛，或 (2) 轨道定域化 Hessian 有未被消除的小本征值。

用法与 RI-MP2 一样简单。例如，以下输入计算梯度和自然轨道：

```{literalinclude} ../../orca_working_input/dlpno-mp2-gradient.inp
:language: orca
```

该实现支持自旋分量缩放，可与双杂化密度泛函一起使用。后者的调用方式是在泛函名称前加上 "`DLPNO-`"。用双杂化密度泛函进行简单几何优化的例子如下所示：

```{literalinclude} ../../orca_working_input/dlpno-b2plyp-gradient.inp
:language: orca
```

对于较小的体系，DLPNO-MP2 与 RI-MP2 的性能差异不是特别大，但对于含约 70-80 个以上原子的体系，相比 RI-MP2 可以实现非常可观的计算时间节省。

由于 MP2 对几何优化而言是昂贵的方法，使用优化良好的起始结构（例如用色散校正 DFT 泛函计算得到的）通常是个好主意。此外，强烈建议为 RIJCOSX 或交换-关联泛函（如适用）使用精确的网格，因为 SCF 迭代只占总体计算成本的一小部分。如果在不请求梯度的情况下计算性质，需要在 `%MP2-block` 中指定 `Density Relaxed`。

导数实现目前仅支持 Foster-Boys 定域化方案。DLPNO-MP2 中的默认定域器是 `AHFB`，强烈不建议更改此设置，因为计算梯度需要紧收敛的定域轨道。

以下是与梯度相关选项的概述：

```orca
# Settings specific to the localization equation z-solver
%mp2 ZLoc_Solver        CG      # Use conjugate gradient solver (default)
                        DIR     # Use direct solver
                        JAC     # Use DIIS-accelerated Jacobi solver
     ZLoc_Tol           1.0e-3  # Residual convergence tolerance for the
                                # localization Z-solver
                                # Default: same value as Z_Tol for CPSCF
     ZLoc_MaxIter       1024    # Maximum localization Z-solver iterations
     ZLoc_MaxDIIS       10      # Number of DIIS vectors for the Jacobi solver
     ZLoc_Shift         0.2     # Shift for the Jacobi solver
# Options for eliminating (near-)singular eigenvectors of the
# orbital Hessian of the localization function.
     ZLoc_EThresh       3.0e-4  # Eigenvectors with an eigenvalue below
                                # this threshold are eliminated.
     ZLoc_EThresh_core  3.0e-4  # Same as ZLoc_EThresh, but for the core orbitals.
                                # Default: identical value as ZLoc_EThresh.
# Options for determining eigenvectors of the localization orbital Hessian.
     ZLoc_UseDavidson   True    # Use Davidson diagonalization.
                                # If false, use direct diagonalization.
     ZLoc_DVDRoots      32      # Number of Davidson roots to be determined.
     ZLoc_DVDNIter      256     # Number of Davidson iterations.
     ZLoc_DVDTolE       3.0e-10 # Eigenvalue tolerance for the Davidson solver.
                                # Default: 1e-6 * ZLoc_EThresh
     ZLoc_DVDTolR       1.0e-7  # Residual tolerance for the Davidson solver.
                                # Default: 0.1 * (ZLoc_Tol)^2
     ZLoc_DVDMaxDim     10      # During Davidson diagonalization, the space of
                                # trial vectors is expanded up to
				# MaxDim * DVDRoots.
# Choice of the PNO processing algorithm.
     DLPNOGrad_Opt      AUTO      # Chooses automatically between RAM and DISK
                                  # (default and recommended)
                        RAM       # Enforce memory-based one-pass algorithm
                        DISK      # Enforce disk-based two-pass algorithm
                        BUFFERED  # Buffered algorithm. Usage is discouraged.
                                  # Experimental, unpredictable I/O performance.
end
```

(sec:modelchemistries.mp2.dlpnoresp)=
## 局域 MP2 二阶导数与响应性质

闭壳层 DLPNO-MP2（以及双杂化 DFT）实现了对电场和磁场的解析二阶导数。{cite}`StoychevDLPNO-MP2Response` 因此，可以得到解析的偶极极化率和 NMR 屏蔽张量（带或不带 GIAO）。该实现支持自旋分量缩放和双杂化泛函。当使用 `NormalPNO` 阈值时，计算性质的误差远低于 0.5%。
关于 DLPNO-MP2 二阶导数实现的更多信息参见章节 {ref}`sec:modelchemistries.mp2.dlpnoresp`，以及电学（{ref}`sec:spectroscopyproperties.elprop`）和磁学（{ref}`sec:spectroscopyproperties.properties.eprnmr`）性质和 CP-SCF 设置（{ref}`sec:essentialelements.cpscf`）的章节。
章节 {ref}`sec:modelchemistries.mp2.dlpno` 和 {ref}`sec:modelchemistries.mp2.dlpnograd` 中讨论的所有注意事项和选项同样适用于此，而二阶导数特有的补充说明如下。

对于约 70 个原子或 300 个关联电子以上的体系，DLPNO-MP2 响应性质计算预计比 RI-MP2 对应计算更快。

使用 `NormalPNO` 默认阈值时，由于局域近似引起的计算性质相对误差小于 0.5%，或者说比 MP2 相对于更精确方法（如 CCSD(T)）的固有误差小 5--10 倍。

DLPNO-MP2 二阶导数对近线性相关和其他数值问题比能量或一阶性质敏感得多。我们已努力选择合理且稳健的默认值，但我们鼓励用户对结果保持审慎并谨慎行事，尤其是在使用弥散基组或数值积分（DFT、COSX）时。在后一种情况下，推荐使用 `DefGrid3`。

特别是 PAO 域的近冗余性（near-redundancy）会在算法中引入数值不稳定性。因此，应在 `PAOOverlapThresh=1e-5` 处截断，这高于能量和梯度的默认值。因此，包含响应性质计算的作业中的能量和梯度可能与不含的作业有所不同。该差异远小于方法的精度（相对 RI-MP2），但在计算例如相对能量时，在所有计算中使用相同的 `PAOOverlapThresh` 值仍是明智的。

出于同样的原因，如果使用弥散基组，建议在 `%scf` 块中设置 `SThresh=1e-6`。

另一种不稳定性源于保留和丢弃的 PNO 之间占据数的微小差异，可能导致非常大的误差。最小差异会在 DLPNO-MP2 弛豫密度计算期间打印出来：

::: ORCAoutput 0
Smallest occupation number difference between PNOs and complementary
PNOs. Absolute: 3.10e-10 Relative: 3.28e-02
:::

我们发现相对差异低于 $10^{-3}$（这并不罕见）就可能值得关注。为了正则化（regularize）不稳定方程，施加一个能级移动（level shift），它等于 $T_\text{CutPNO}$ 乘以 $T_\text{ScalePNO\_LShift}$。对于响应性质计算，默认设置合理的 `TScalePNO_LShift=0.1` 值，但对于梯度（或能量）计算则不是，因为未发现后者受此问题困扰，因此适用与上述相同的考虑。

选项 `DLPNOGrad_Opt=BUFFERED` 未针对响应性质实现。

下面是一个简单的 DLPNO-MP2 NMR 屏蔽计算示例：

```{literalinclude} ../../orca_working_input/dlpno-mp2-nmr-simple.inp
:language: orca
```

DLPNO-MP2 响应性质所用附加选项的总结如下：

```orca
%mp2
     PAOOverlapThresh 1e-5   # Threshold for constructing non-redundant PAOs
                             # Default is 1e-8 for energy/gradient calculations!
     TScalePNO_LShift 0.1    # Level shift for PNO constraint equations:
                             # TScalePNO_LShift * TCutPNO
                             # Default is 0 for energy/gradient calculations!
end
```

下面是使用 DLPNO-MP2 进行 DSD-PBEP86 NMR 屏蔽和偶极极化率张量计算的示例输入。请注意，def2-TZVP 基组对于屏蔽或极化率都不一定理想。

```orcainput
! DLPNO-DSD-PBEP86/2013 D3BJ def2-TZVP def2-TZVP/C TightSCF NoFrozenCore
! RIJCOSX def2/J DefGrid3      # Use RIJCOSX with tighter grid settings
! NMR                          # Request NMR shielding
%elprop Polar 1 end            # Request polarizability
%mp2                           # These settings are default for response properties
   Density Relaxed
   PAOOverlapThresh 1e-5
   TScalePNO_LShift 0.1
end
%eprnmr 
  GIAO_2el GIAO_2el_RIJCOSX    # Also use RIJCOSX for GIAO integrals
end                            # (This is the default for !RIJCOSX)
*xyzfile 0 1 geometry.xyz
```

(sec:modelchemistries.mp2.dlpno-numeric)=
## 数值 DLPNO-MP2 导数

局域关联方法中的各种截断会在势能面上引入小的不连续性（discontinuities）。例如，一个小的位移可能改变关联域的大小，导致域近似的误差略大或略小。默认的 DLPNO-MP2 截断阈值足够保守，因此这些不连续性不应在使用解析梯度的几何优化中引起问题。{cite}`Pinski2019` 然而，如果希望用有限差分计算 DLPNO-MP2 能量、梯度或性质的（半）数值导数，则可能出现大误差。因此，在这些情况下，明智的做法是在位移时保持对列表（pair lists）和关联域固定。目前，这可以通过以下过程实现：首先，在参考几何结构处的计算附加设置 `StoreDLPNOData=true`：

```orcainput
! DLPNO-MP2 def2-SVP def2-SVP/C VeryTightSCF
%base "calc0"
%mp2
  StoreDLPNOData true
end
*xyzfile 0 1 geom0.xyz
```

这将产生附加文件 *calc0.MapDLPNO00.tmp*、*calc0.MapDLPNOPre0.tmp*、*calc0.IJLIST.0.tmp*、*calc0.IJLISTSCR.0.tmp* 和 *calc0.IJNPNO.0.tmp*，它们与 *calc0.loc* 中的定域轨道一起在下一步所需的工作目录中。然后位移几何结构处的计算按如下方式请求：

```orcainput
! DLPNO-MP2 def2-SVP def2-SVP/C VeryTightSCF
%mp2
  RefBaseName "calc0"
end
*xyzfile 0 1 geom1.xyz
```

程序将使用 *calc0.loc* 中的轨道作为定域化的初始猜测，并基于最大重叠将参考轨道映射到新轨道。关联和被筛选掉的对的列表从文件 *calc0.IJLIST.0.tmp* 和 *calc0.IJLISTSCR.0.tmp* 读取，而域信息（MO-PAO、MO-Aux 等）从 *calc0.MapDLPNO00.tmp* 和 *calc0.MapDLPNOPre0.tmp* 读取。每个对的 PNO 数量（存储在 *calc0.IJNPNO.0.tmp* 中）也与参考计算保持一致：保留占据数最高的那些，忽略 $T_\text{CutPNO}$。

该过程应能提高手动计算各种 DLPNO-MP2 性质几何导数的精度和数值稳定性（包括那些在位移几何结构处需要解析一阶或二阶导数的情况）。对于半数值 Hessian 计算（`NumFreq`），如下面所示添加 `StoreDLPNOData=true` 就足够了，ORCA 会处理其余部分。为了数值稳定性，也建议提高 `PAOOverlapThresh` 并添加 PNO 能级移动，原因见章节 {ref}`sec:modelchemistries.mp2.dlpnoresp` 的描述。

```orca
! DLPNO-MP2 def2-SVP def2-SVP/C VeryTightSCF NumFreq
%mp2
  StoreDLPNOData true
  PAOOverlapThresh 1e-5
  TScalePNO_LShift 0.1
end
# geometry definition
```

注意，如果轨道定域化 Hessian 是（近）奇异的，从参考几何结构到位移几何结构的轨道映射很可能会失败。目前尚未针对该问题实现解决方案。

(sec:modelchemistries.mp2.multilevel)=
## 多层 DLPNO-MP2 计算（Multi-Level DLPNO-MP2 calculations）

使用 DLPNO-MP2 方法可以以不同的精度处理体系不同片段之间的相互作用，或将某些相互作用完全排除在电子关联处理之外。DLPNO-CCSD(T) 语境下的更详细讨论见章节 {ref}`sec:modelchemistries.mdci.multilevel` 和参考文献 {cite}`Sparta2017`。这里我们只介绍 MP2 模块的技术能力和所需输入。目前，多层计算仅适用于闭壳层 DLPNO-MP2。多层梯度和响应性质也是可能的。必须定义片段——参见 {ref}`sec:essentialelements.fragmentation`。

```orca
! DLPNO-MP2 NoFrozenCore TightPNO
%mp2
  LoosePNOFragInter  {1 *} # * can be used as a wildcard for either or both indices
  NormalPNOFragInter {1 1} {1 2} # multiple fragment pairs can be listed like this
  TightPNOFragInter  {2 3}
  HFFragInter        {3 1} {4 2}
  CustomFragInter
    FragPairs        {4 4} {3 4} # pair definition is required
    HFOnly           false # flag to skip MP2 for these pairs - same as HFFragInter
    FrozenCore       false # flag to skip core correlation - requires !NoFrozenCore
    TCutPNO          1e-8  # custom value for these pairs
    TCutDO           1e-2  # custom value for these pairs
    TCutDOij         1e-5  # custom value for these pairs
    TCutPre          1e-6  # custom value for these pairs
  end
end
# geometry and fragment definition
```

注意，给定的对或片段只能属于一个层，输入中较后的定义会覆盖先前的定义。这意味着如果上述输入用于 4 片段计算，1-4 片段间相互作用将用 `LoosePNO` 阈值处理，片段 1 内部及其与片段 2 的相互作用用 `NormalPNO` 阈值，2-3 对用 `TightPNO`，1-3 和 2-4 对将停留在 HF 水平，3-4 和 4-4 对将用 $T_\text{CutPNO}=10^{-8}$ 和 $T_\text{CutDO}=10^{-2}$（即 `NormalPNO` 默认值）处理，而 2-2 和 3-3 对将停留在全局（`TightPNO`）设置上。

[^1]: 然而，有时——特别是涉及过渡金属和芯轨道时——我们遇到过令人不快的大误差。所以——使用 float 时要小心并仔细复核！


(sec:modelchemistries.mp2.expcorrelation)=
## 显式相关 MP2 计算（Explicitly correlated MP2 calculations）

ORCA 提供一个高效的显式相关模块，可用于 MP2 和耦合簇计算（章节 {ref}`sec:modelchemistries.mdci.expcorrelation`）。下面在耦合簇计算的语境中对其进行描述。


(sec:modelchemistries.mp2.dft)=
## "双杂化"密度泛函理论中的 MP2
```{index} Double-Hybrid DFT and MP2
```

在双杂化 DFT 梯度中会遇到一种略为更一般的形式。其理论简述如下。

Grimme 提出的微扰修正和梯度校正杂化泛函的能量表达式为：

$$\begin{gathered}
E=V_{NN} +\left\langle { \mathrm{\mathbf{Ph} }^{+} } \right\rangle+ \frac{1}{2}\int{\int{ \frac{\rho \left({ \mathrm{\mathbf{r} }_{1} } \right)\rho \left({ \mathrm{\mathbf{r} }_{2} } \right)}{\left|{\mathrm{\mathbf{r} }_{1} -\mathrm{\mathbf{r} }_{2} } 
\right|}d\mathrm{\mathbf{r} }_{1} d\mathrm{\mathbf{r} }_{2} } } -\frac{1}{2}a_{x} 
\sum\limits_{\mu \nu \kappa \tau \sigma } { P_{\mu \kappa }^{\sigma } P_{\nu 
\tau }^{\sigma } \left({ \mu \nu \vert \kappa \tau } \right)} +c_{\text{DF} } E_{\text{XC} } 
\left[{ \rho_{\alpha } ,\rho_{\beta } } \right]+c_{\text{PT} } E_{\text{PT} } \end{gathered}$$

$$\begin{gathered}
E = E_{\text{SCF}} + c_{\text{PT}}E_{\text{PT}}
\end{gathered}$$ (eqn:61)

<!--$$\hspace{-12.75cm}= E_{\text{SC}F} +c_{\text{PT} } E_{\text{PT} } 
$$ (eqn:61)-->

其中 $V_{NN}$ 是核排斥能，$h_{\mu \nu }$ 是通常单电子算符的矩阵元，包含动能和电子-核吸引项（$\left\langle {\mathrm{\mathbf{ab} }} \right\rangle$ 表示矩阵乘积 $\mathrm{\mathbf{ab} }$ 的迹）。与通常一样，分子自旋轨道在原子中心基函数中展开（$\sigma =\alpha ,\beta$）：

$$\psi_{p}^{\sigma } \left({ \mathrm{\mathbf{r} }} \right)=\sum_\mu{ c_{\mu 
p}^{\sigma } \varphi_{\mu } \left({ \mathrm{\mathbf{r} }} \right)} 
$$ (eqn:62)

其中 MO 系数为 $c_{\mu p}^{\sigma }$。总密度由下式给出（全文假定为实轨道）：

$$\rho \left({ \mathrm{\mathbf{r} }} \right)=\sum_{i\sigma } { \left|{ \psi 
_{i}^{\sigma } \left({ \mathrm{\mathbf{r} }} \right)} \right|^{2} } 
=\sum_{\mu \nu \sigma } { P_{\mu \nu }^{\sigma } \varphi_{\mu } 
\left({ \mathrm{\mathbf{r} }} \right)\varphi_{\nu } \left({ \mathrm{\mathbf{r} }} 
\right)} =\rho^{\alpha }\left({ \mathrm{\mathbf{r} }} \right)+\rho^{\beta }\left({\mathrm{\mathbf{r} }} \right)$$ (eqn:63)

其中 $\mathrm{\mathbf{P} }=\mathrm{\mathbf{P} }^{\alpha }+\mathrm{\mathbf{P} }^{\beta }$，$P_{\mu \nu }^{\sigma } =\sum_{i_{\sigma } } { c_{\mu i}^{\sigma } c_{\nu i}^{\sigma } }$。

公式 {eq}`eqn:61` 的第二项代表库仑自排斥（Coulombic self-repulsion）。第三项代表哈特里-福克交换的贡献，其中双电子积分定义为：

$$\left({ \mu \nu \vert \kappa \tau } \right)=\int{ \int{ \phi_{\mu } \left({\mathrm{\mathbf{r} }_{1} } \right)\phi_{\nu } \left({\mathrm{\mathbf{r} }_{1} } 
\right)r_{12}^{-1} \phi_{\kappa } \left({\mathrm{\mathbf{r} }_{2} } \right)\phi 
_{\tau } \left({\mathrm{\mathbf{r} }_{2} } \right)d\mathrm{\mathbf{r} }_{1} d\mathrm{\mathbf{r} }_{2} } } 
$$ (eqn:64)

混合参数 $a_{x}$ 控制哈特里-福克交换的比例，具有半经验性质。交换-关联贡献可以写为：

$$E_{\text{XC} } \left[{ \rho_{\alpha } ,\rho_{\beta } } \right] = 
\left({ 1-a_{x} } \right) E_{\text{X} }^{\text{GGA} } \left[{ \rho_{\alpha } ,\rho_{\beta } } \right] 
+ b E_{\text{C} }^{\text{GGA} } \left[{ \rho_{\alpha } ,\rho_{\beta } } \right]$$ (eqn:65)

其中，$E_{\text{X} }^{\text{GGA} } \left[{ \rho_{\alpha } ,\rho_{\beta } } \right]$ 是所讨论 XC 泛函的交换部分，$E_{\text{C} }^{\text{GGA} } \left[{ \rho_{\alpha } ,\rho_{\beta } } \right]$ 是关联部分。参数 $b$ 控制 DFT 关联混入总能量的比例，参数 $c_{\text{DF} }$ 是一个全局缩放因子，允许从哈特里-福克理论（$a_{\text{X} } =1$，$c_{\text{DF} } =0$，$c_{\text{PT} } =0$）到 MP2 理论（$a_{\text{X} } =1$，$c_{\text{DF} } =0$，$c_{\text{PT} } =1$）到纯 DFT（$a_{\text{X} } =1$，$c_{\text{DF} } =0$，$c_{\text{PT} } =1$）到杂化 DFT（$0 < a_{\text{X} } <1$，$c_{\text{DF} } =1$，$c_{\text{PT} } =0$）最后到本文讨论的一般微扰修正方法（$0<a_{\text{X} } <1$，$c_{\text{DF} } =1$，$0<c_{\text{PT} } <1$）。如 Grimme 详细讨论的，B2-PLYP 泛函使用 Lee-Yang-Parr（LYP）泛函作为关联部分，Becke 1988（B88）泛函作为 GGA 交换部分，半经验参数的最优选择确定为 $a_{\text{X} } =0.53$，$c_{\text{PT} } =0.27$，$c_{\text{DF} } =1$，$b=1-c_{\text{PT} }$。为方便起见，我们将省略 XC 部分中对参数 $a_{\text{X} }$ 和 $b$ 的显式引用，并将梯度校正 XC 能量改写为：

$$E_{\text{XC} } \left[{ \rho^{\alpha },\rho^{\beta } } \right]=\int{ f\left({ \rho 
^{\alpha },\rho^{\beta },\gamma^{\alpha \alpha },\gamma^{\beta \beta 
},\gamma^{\alpha \beta } } \right)d\mathrm{\mathbf{r} }}
$$ (eqn:66)

其中梯度不变量为 $\gamma^{\sigma{ \sigma }'}=\vec{{\nabla } }\rho^{\sigma }\vec{{\nabla } }\rho^{{\sigma }'}$。公式 (48) 中的最后一项代表缩放的二阶微扰能：

$$E^{\text{PT2} }=\frac{1}{2}\sum_{i_{\alpha } <j_{\alpha } } { \left\langle {\mathrm{\mathbf{t} }^{i_{\alpha } j_{\alpha } } { \mathrm{\mathbf{\overline{K} }} }^{i_{\alpha } j_{\alpha } +} } 
\right\rangle} 
+\frac{1}{2}\sum_{i_{\beta } <j_{\beta } } { \left\langle { \mathrm{\mathbf{t} }^{i_{\beta } j_{\beta } } 
\mathrm{\mathbf{\overline{{K} }} }^{i_{\beta } 
j_{\beta } +} } \right\rangle} +\sum_{i_{\alpha } ,j_{\beta } } 
{\left\langle { \mathrm{\mathbf{t} }^{i_{\alpha } j_{\beta } } { \mathrm{\mathbf{\overline{K} }} }^{i_{\alpha } j_{\beta } 
+} } \right\rangle}
$$ (eqn:67)

PT2 振幅已收集在矩阵 $\mathrm{\mathbf{t} }^{i_{\sigma } j_{{\sigma }'} }$ 中，其元素为：

$$t_{a_{\sigma } b_{{\sigma }'} }^{i_{\sigma } j_{{\sigma }'} } 
=\bar{{K} }_{a_{\sigma } b_{{\sigma }'} }^{i_{\sigma } j_{{\sigma }'} } 
\left({ \varepsilon_{i}^{\sigma } +\varepsilon_{j}^{{\sigma }'} 
-\varepsilon_{a}^{\sigma } -\varepsilon_{b}^{{\sigma }'} } \right)^{-1}
$$ (eqn:68)

其中假定轨道为正则的，轨道能量为 $\varepsilon_{p}^{\sigma }$。交换算符矩阵为 $K_{a_{\sigma } b_{{\sigma }'} }^{i_{\sigma } j_{{\sigma }'} } =\left({ i_{\sigma } a_{\sigma } \vert j_{{\sigma }'} b_{{\sigma }'} } \right)$，反对称化交换积分定义为 $\bar{{K} }_{a_{\sigma } b_{{\sigma }'} }^{i_{\sigma } j_{{\sigma }'} } =\left({ i_{\sigma } a_{\sigma } \vert j_{{\sigma }'} b_{{\sigma }'} } \right)-\delta_{\sigma{ \sigma }'} \left({ i_{\sigma } b_{\sigma } \vert _{\sigma } a_{\sigma } } \right)$。

轨道满足 SCF 方程，SCF 算符的矩阵元为：

$$F_{\mu \nu }^{\sigma } =h_{\mu \nu } +\sum_{\kappa \tau } { P_{\kappa 
\tau } \left({ \mu \nu \vert \kappa \tau } \right)-a_{\text{X} } P_{\kappa \tau 
}^{\sigma } \left({ \mu \kappa \vert \nu \tau } \right)} +c_{\text{DF} } \left({ \mu 
\vert V_{\text{XC} }^{\sigma } \vert \nu } \right)$$ (eqn:69)

梯度校正泛函的 XC 势矩阵元为：{cite}`szabo1989modern`

$$\left({ \mu \vert V_{\text{XC} }^{\alpha } \vert \nu } \right)=\int{ \left\{{\frac{\delta f}{\delta \rho_{\alpha } \left({ \mathrm{\mathbf{r} }} 
\right)}\left({ \varphi_{\mu } \varphi_{\nu } } \right)+2\frac{\delta 
f}{\delta \gamma_{\alpha \alpha } }\vec{{\nabla } }\rho_{\alpha } 
\vec{{\nabla } }\left({ \varphi_{\mu } \varphi_{\nu } } 
\right)+\frac{\delta f}{\delta \gamma_{\alpha \beta } }\vec{{\nabla } }\rho 
_{\beta } \vec{{\nabla } }\left({ \varphi_{\mu } \varphi_{\nu } } \right)} 
\right\}d\mathrm{\mathbf{r} }} 
$$ (eqn:70)

公式 {eq}`eqn:61` 中的能量依赖于 MO 系数、PT2 振幅，并通过 $V_{NN}$、$V_{eN}$（在 $h$ 中）和基函数也显式依赖于分子几何结构。遗憾的是，能量只对 PT2 振幅是驻定的（stationary），因为可以认为它们已通过对 Hylleraas 泛函的最小化进行了优化：

$$E_{\text{PT2} } =\min_{\mathrm{\mathbf{t}}} \left\{{\frac{1}{2}\sum_{i_{\alpha} <j_{\alpha}} { \left\langle { \mathrm{\mathbf{t} }^{i_{\alpha } j_{\alpha } }
{\mathbf{\overline{{K}}}}^{i_{\alpha } 
j_{\alpha } +} } \right\rangle} +\frac{1}{2}\sum_{i_{\beta } 
<j_{\beta } } { \left\langle {{\mathbf{t} }^{i_{\beta } j_{\beta } } {{\mathbf{\overline{K} }} }^{i_{\beta } 
j_{\beta } +} } \right\rangle} 
+\sum_{i_{\alpha } j_{\beta } } { \left\langle {{\mathbf{t} }^{i_{\alpha } j_{\beta } } 
{\mathbf{\overline{{K} }} }^{i_{\alpha } 
j_{\beta } +} } \right\rangle+\left\langle {{\mathbf{D}'}^{\alpha }{\mathbf{F} }^{\alpha +} } 
\right\rangle+\left\langle {{\mathbf{D}'}^{\beta }{\mathbf{F} }^{\beta +} } \right\rangle} } 
\right\}
$$(eqn;71)

非弛豫 PT2 差分密度（difference density）定义为：

$${D}_{ij}^{'\alpha } =-\frac{1}{2}\sum_{k_{\alpha } } { \left\langle { \mathrm{\mathbf{t} }^{i_{\alpha } k_{\alpha } } 
\mathrm{\mathbf{t} }^{k_{\alpha } j_{\alpha } 
} } \right\rangle} -\sum_{k_{\beta } } { \left\langle { \mathrm{\mathbf{t} }^{i_{\alpha } k_{\beta } } 
\mathrm{\mathbf{t} }^{k_{\beta } j_{\alpha } } 
} \right\rangle}
$$ (eqn:72)

$${D}_{ab}^{'\alpha } =\sum_{i_{\alpha } <j_{\alpha } } { \mathrm{\mathbf{t} }^{i_{\alpha } j_{\alpha } } 
\mathrm{\mathbf{t} }^{i_{\alpha } j_{\alpha } 
+} } +\sum_{i_{\beta } j_{\alpha } } { \mathrm{\mathbf{t} }^{i_{\beta } 
j_{\alpha } +} \mathrm{\mathbf{t} }^{i_{\beta } j_{\alpha } } }
$$ (eqn:73)

自旋向下的非弛豫差分密度有类似的表达式。对该泛函关于振幅的最小化给出二阶微扰能。公式 {eq}`eqn:61` 中 SCF 部分对参数 "$x$" 的导数是直接且众所周知的。它给出：

$$\begin{array}{l}
 E_{\text{SCF} }^{x} =V_{NN}^{x} +\left\langle { \mathrm{\mathbf{Ph} }^{x} } \right\rangle
+\left\langle { \mathrm{\mathbf{W} }^{SCF}\mathrm{\mathbf{S} }^{\left( x \right)} } 
\right\rangle+\sum_{\mu \nu \kappa \tau } { \Gamma_{\mu \nu \kappa 
\tau } \left({ \mu \nu \vert \kappa \tau } \right)^{\left( x \right)} } \\ 
\hspace{1cm}
+\underbrace{\sum_\sigma}_{\left({ {\sigma }'\ne \sigma } \right)}
{\int{ \left\{{ \frac{\delta f}{\delta \rho_{\sigma } \left({\mathrm{\mathbf{r} }} \right)}\rho_{\sigma }^{\left( x \right)} +2\frac{\delta 
f}{\delta \gamma_{\sigma \sigma } }\vec{{\nabla } }\rho_{\sigma } 
\vec{{\nabla } }\rho_{\sigma }^{\left( x \right)} +\frac{\delta f}{\delta 
\gamma_{\sigma{ \sigma }'} }\vec{{\nabla } }\rho_{{\sigma }'} \vec{{\nabla 
} }\rho_{\sigma }^{\left( x \right)} } \right\}d\mathrm{\mathbf{r} }} } \\ 
 \end{array}
$$ (eqn:74)

上标 "$x$" 指对某个微扰 "$x$" 的导数，而括号中的上标表示只对基函数关于 "$x$" 取导数。例如：

$$\begin{array}{l}
 \rho_{\sigma }^{\left( x \right)} =\sum_{\mu \nu } P_{\mu \nu 
}^{\sigma } \left\{\frac{\partial \varphi_{\mu } }{\partial x}\varphi 
_{\nu } +\varphi_{\mu } \frac{\partial \varphi_{\nu } }{\partial x} 
\right\}\\ 
 h_{\mu \nu }^{x} =\left( \frac{\partial \varphi_{\mu } }{\partial x}\vert 
\hat{{h} }\vert \varphi_\nu  \right)+\left( \varphi_{\mu } \vert 
\hat{{h} }\vert \frac{\partial \varphi_{\nu } }{\partial x} \right)+\left( 
\varphi_{\mu } \vert \frac{\partial \hat{{h} }}{\partial x}\vert \varphi 
_{\nu }  \right) \\ 
 \end{array}
$$ (eqn:75)

在公式 {eq}`eqn:74` 中，**S** 是重叠矩阵，**W**$^{\text{SCF} }$ 是能量加权密度：

$$W_{\mu \nu }^{\text{SCF} } =W_{\mu \nu }^{\alpha ;\text{SCF} } +W_{\mu \nu }^{\beta ;\text{SCF} } 
=-\sum_{i\sigma } { c_{\mu i}^{\sigma } c_{\nu i}^{\sigma } 
\varepsilon_{i}^{\sigma } } 
$$ (eqn:76)

此时，有效双粒子密度矩阵是完全可分离的，为：

$$\Gamma_{\mu \nu \kappa \tau } =\frac{1}{2}P_{\mu \nu } P_{\kappa \tau 
} -\frac{1}{2}a_{x} P_{\mu \kappa }^{\alpha } P_{\nu \tau }^{\alpha } 
-\frac{1}{2}a_{x} P_{\mu \kappa }^{\beta } P_{\nu \tau }^{\beta }
$$ (eqn:77)

PT2 部分的导数要复杂得多，因为 $E_{\text{PT2} }$ 对分子轨道的变化不是驻定的。这需要求解耦合微扰 SCF（coupled-perturbed SCF, CP-SCF）方程。我们遵循标准做法，将微扰轨道按未微扰轨道展开：

$$\psi_{p}^{\sigma ;x} \left({ \mathrm{\mathbf{r} }} \right)=\sum_q 
{U_{qp}^{\sigma ;x} \psi_{q}^{\sigma } \left({ \mathrm{\mathbf{r} }} \right)} 
$$ (eqn:78)

**U** 的占据-占据和虚-虚块与通常一样，通过正交归一性约束的导数固定：

$$U_{ij}^{\sigma ;x} =-\frac{1}{2}S_{ij}^{\sigma \left( x \right)}
$$ (eqn:79)

$$U_{ab}^{\sigma ;x} =-\frac{1}{2}S_{ab}^{\sigma \left( x \right)} 
$$ (eqn:80)

$$U_{ia}^{\sigma ;x} =-S_{ia}^{\sigma \left( x \right)} -U_{ai}^{\sigma ;x} 
$$ (eqn:81)

其中 $S_{pq}^{\sigma \left( x \right)} =\sum\nolimits_{\mu \nu } { c_{\mu p}^{\sigma } c_{\nu q}^{\sigma } S_{\mu \nu }^{\left( x \right)} }$。**U**$^{x}$ 剩余的虚-占据块必须通过求解 CP-SCF 方程确定。然而，正如 Handy 和 Schaefer 所证明的，这一步是不必要的，只需要求解一组 CP-SCF 方程（Z-矢量方程）。为此，定义拉格朗日量：

$$\begin{array}{l}
 L_{ai}^{\alpha } =R^{\sigma }\left( \mathrm{\mathbf{D}'} \right)_{ai} 
+2\sum_{j_{\alpha } b_{\alpha } c_{\alpha } } { \left({ a_{\alpha } 
c_{\alpha } \vert j_{\alpha } b_{\alpha } } \right)t_{c_{\alpha } b_{\alpha 
} }^{i_{\alpha } j_{\alpha } } } -2\sum_{j_{\alpha } k_{\alpha } 
b_{\alpha } } { \left({ k_{\alpha } i_{\alpha } \vert j_{\alpha } b_{\alpha } 
} \right)t_{a_{\alpha } b_{\alpha } }^{k_{\alpha } j_{\alpha } } } \\ 
\hspace{2.6cm}
+2\sum_{j_{\beta 
} b_{\beta } c_{\alpha } } { \left({ a_{\alpha } c_{\alpha } \vert j_{\beta } 
b_{\beta } } \right)t_{b_{\beta } c_{\alpha } }^{j_{\beta } i_{\alpha } } } 
-2\sum_{j_{\beta } k_{\alpha } b_{\beta } } { \left({ k_{\alpha } 
i_{\alpha } \vert j_{\beta } b_{\beta } } \right)t_{b_{\beta } a_{\alpha } 
}^{j_{\beta } k_{\alpha } } } \\ 
 \end{array}
$$ (eqn:82)

$L_{ai}^{\beta }$ 有类似的方程。响应算符 $R^{\alpha } \left({ \mathrm{\mathbf{D}'} } \right)$ 的矩阵元最好在 AO 基中求值，然后变换到 MO 基。AO 基矩阵元由下式给出：

$$%\begin{array}{l}
\begin{aligned}
 R^{\alpha }\left({ \mathrm{\mathbf{D}'} } \right)_{\mu \nu } 
=&\sum_{\kappa \tau } { 2{D}'_{\kappa \tau } \left({ \mu \nu \vert 
\kappa \tau } \right)-{D}_{\kappa \tau }^{'\alpha } \left[{ \left({ \mu 
\kappa \vert \nu \tau } \right)+\left({ \nu k\vert \mu \tau } \right)} 
\right]} \\
&+\sum_\zeta{ \int{ \left[{\frac{\delta^{2}f}{\delta \rho_{\alpha } \delta \zeta } } \right.\zeta 
\left({ \mathrm{\mathbf{D}'} } \right)\left({ \phi_{\mu } \phi_{\nu } } 
\right)+\left({ 2\frac{\delta^{2}f}{\delta \gamma_{\alpha \alpha } \delta 
\zeta }\vec{{\nabla } }\rho_{\mathrm{\mathbf{P} }}^{\alpha } +\frac{\delta 
^{2}f}{\delta \gamma_{\alpha \beta } \delta \zeta }\vec{{\nabla } }\rho 
_{\mathrm{\mathbf{P} }}^{\beta } } \right)\zeta \left({ \mathrm{\mathbf{D}'} } 
\right)\vec{{\nabla } }\left({ \phi_{\mu } \phi_{\nu } } \right)} } \\
&\left.{+\left({ 2\frac{\delta f}{\delta \gamma_{\alpha \alpha } }\vec{{\nabla 
} }\rho_{\mathrm{\mathbf{D}'} }^{\alpha } +\frac{\delta f}{\delta \gamma_{\alpha 
\beta } }\vec{{\nabla } }\rho_{\mathrm{\mathbf{D}'} }^{\beta } } 
\right)\vec{{\nabla } }\left({ \phi_{\mu } \phi_{\nu } } \right)} 
\right]d\mathrm{\mathbf{r} } \\
% \end{array}
\end{aligned}$$ (eqn:RD-DHDFT)

其中

$$\zeta \left({ \mathrm{\mathbf{D}'} } \right)=\rho_{\mathrm{\mathbf{D}'} }^{\alpha } 
,\rho_{\mathrm{\mathbf{D}'} }^{\beta } ,\gamma_{\alpha \alpha } \left({ \mathrm{\mathbf{D}'} } \right),\gamma_{\beta 
\beta } \left({ \mathrm{\mathbf{D}'} } 
\right),\gamma_{\alpha \beta } \left({ \mathrm{\mathbf{D}'} } \right)$$ (eqn:83)

$\zeta$-梯度参数作为 PT2 差分密度和 SCF 密度的混合来求值。例如：

$$\gamma_{\alpha \alpha } (\mbox{D}')=2\vec{{\nabla } }\rho 
_{\mbox{D}'}^{\alpha } \vec{{\nabla } }\rho_{\mbox{P}'}^{\alpha } 
$$ (eqn:84)

其中

$$\rho_{\mathrm{\mathbf{D}'} }^{\alpha } \left({ \mathrm{\mathbf{r} }} 
\right)=\sum_{\mu \nu } { {D}_{\mu \nu }^{'\alpha } \phi_{\mu } 
\left({ \mathrm{\mathbf{r} }} \right)\phi_{\nu } \left({ \mathrm{\mathbf{r} }} \right)}
$$ (eqn:85)

$$\rho_{\mathrm{\mathbf{P} }}^{\alpha } \left({ \mathrm{\mathbf{r} }} 
\right)=\sum_{\mu \nu } { P_{\mu \nu }^{\alpha } \phi_{\mu } \left({\mathrm{\mathbf{r} }} \right)\phi_{\nu } \left({ \mathrm{\mathbf{r} }} \right)} 
$$ (eqn:86)

定义了拉格朗日量之后，需要为 "Z-矢量" 的元素求解以下 CP-SCF 方程：

$$\left({ \varepsilon_{a}^{\sigma } -\varepsilon_{i}^{\sigma } } 
\right)Z_{ai}^{\sigma } +R^{\sigma }\left({ \mathrm{\mathbf{Z} }} \right)_{ai} 
=-L_{ai}^{\sigma } 
$$ (eqn:87)

该解定义了弛豫差分密度的占据-虚块，由下式给出：

$$\mathrm{\mathbf{D} }^{\sigma }=\mathrm{\mathbf{D}'}^{\sigma }+\mathrm{\mathbf{Z} }^{\sigma }
$$ (eqn:88)

为方便起见，$\mathrm{\mathbf{D} }^{\sigma }$ 被对称化，因为它之后只会与对称矩阵缩并。求解 Z-矢量方程后，能量加权差分密度矩阵的所有部分都可以方便地计算：

$$W_{ij}^{\alpha ;\text{PT2} } =-\frac{1}{2}D_{ij}^{\alpha } \left({ \varepsilon 
_{i}^{\alpha } +\varepsilon_{j}^{\alpha } } \right)-\frac{1}{2}R\left({\mathrm{\mathbf{D} }} \right)_{ij} -\sum_{k_{\alpha } a_{\alpha } b_{\alpha 
} } { \left({ i_{\alpha } a_{\alpha } \vert k_{\alpha } b_{\alpha } } 
\right)t_{a_{\alpha } b_{\alpha } }^{j_{\alpha } k_{\alpha } } } 
-\sum_{k_{\beta } a_{\alpha } b_{\beta } } { \left({ i_{\alpha } 
a_{\alpha } \vert k_{\beta } b_{\beta } } \right)t_{b_{\beta } a_{\alpha } 
}^{k_{\beta } j_{\alpha } } } 
$$ (eqn:89)

$$W_{ab}^{\alpha ;\text{PT2} } =-\frac{1}{2}D_{ab}^{\alpha } \left({ \varepsilon 
_{a}^{\alpha } +\varepsilon_{b}^{\alpha } } \right)-\sum_{i_{\alpha 
} j_{\alpha } c_{\alpha } } { \left({ i_{\alpha } a_{\alpha } \vert j_{\alpha 
} c_{\alpha } } \right)t_{b_{\alpha } c_{\alpha } }^{i_{\alpha } j_{\alpha } 
} } -\sum_{i_{\alpha } j_{\beta } c_{\beta } } { \left({ i_{\alpha } 
a_{\alpha } \vert j_{\beta } c_{\beta } } \right)t_{c_{\beta } b_{\alpha } 
}^{j_{\beta } i_{\alpha } } } 
$$ (eqn:90)

$$W_{ai}^{\alpha ;\text{PT2} } =-2\sum_{j_{\alpha } k_{\alpha } b_{\alpha } } 
{\left({ k_{\alpha } i_{\alpha } \vert j_{\alpha } b_{\alpha } } 
\right)t_{a_{\alpha } b_{\alpha } }^{k_{\alpha } j_{\alpha } } } 
-2\sum_{j_{\beta } k_{\alpha } b_{\beta } } { \left({ k_{\alpha } 
i_{\alpha } \vert j_{\beta } b_{\beta } } \right)t_{b_{\beta } a_{\alpha } 
}^{j_{\beta } k_{\alpha } } } 
$$ (eqn:91)

$$W_{ia}^{\alpha ;\text{PT2} } =-\varepsilon_{i}^{\alpha } Z_{ai}^{\alpha } 
$$ (eqn:92)

同样，自旋向下情形有类似的方程。有了弛豫差分密度和能量加权密度矩阵，最后就可以求 PT2 部分的梯度了（$(\mathrm{\mathbf{W} } ^{\text{PT2} }=\mathrm{\mathbf{W} }^{\alpha ;\text{PT2} }+\mathrm{\mathbf{W} }^{\beta ;\text{PT2} })$：

$$\begin{array}{l}
E_{\text{PT2} }^{x} =\left\langle { \mathrm{\mathbf{Dh} }^{x} } \right\rangle+\left\langle {\mathrm{\mathbf{W} }^{\text{PT2} } \mathrm{\mathbf{S} }^{\left( x \right)} } \right\rangle
+\sum_{\mu \nu \kappa \tau } { \Gamma_{\mu \nu \kappa \tau }^{\text{PT2} } 
\left({ \mu \nu \vert \kappa \tau } \right)^{(x) }} \\
+ \sum_{\underset{(\sigma \ne{ \sigma }') }{\sigma} }
{\displaystyle\int} \left\{\frac{\delta f}{\delta \rho_\sigma (\mathbf{r}) } \rho_{\sigma }^{(x) } 
+2\frac{\delta f}{\delta \gamma_{\sigma \sigma } }
\overset{r}{\nabla}\rho_{\sigma } \overset{r}{\nabla}\rho^{(x) }_{\sigma } 
+{\frac{\delta f}{\delta \gamma _{\sigma \sigma } }
\overset{r}{\nabla}\rho_{{\sigma }'} \overset{r}{\nabla}\rho_{\sigma }^{(x) }} \right\}\,d\mathbf{r}
\end{array}
$$ (eqn:93)

公式 {eq}`eqn:61` 的最终导数当然是 $E_{SCF}^{x} +c_{PT} E_{\text{PT2} }^{x}$ 之和。出于计算效率的考虑，两个导数应同时求值。

请注意，对梯度的交换-关联贡献采取的形式比预想的更复杂一些。事实上，从 SCF XC-梯度（公式 {eq}`eqn:74`）来看，可能会猜测梯度的 PT2 部分形式相同，只是 $\rho_{\mathrm{\mathbf{P} }}^{\sigma \left( x \right)}$ 被 $\hat{{H} }$（弛豫 PT2 差分密度）替换。然而，情况并非如此。公式 {eq}`eqn:93` 中显现的额外复杂性的根本原因在于，PT2 梯度的 XC 贡献来自弛豫 PT2 差分密度与 SCF 算符导数的缩并。由于 SCF 算符已包含 XC 势的一阶导数，且 PT2 能量对 SCF 密度的变化不是驻定的，因而产生一个响应类型的项，需要求 XC 泛函的二阶泛函导数。最后，正如 MP2 梯度理论中众所周知的，有效双粒子密度矩阵包含可分离和不可分离两部分：

$$\Gamma_{\mu \nu \kappa \tau }^{\text{PT2} } =D_{\mu \nu } P_{\kappa \tau } -D_{\mu 
\kappa }^{\alpha } P_{\nu \tau }^{\alpha } -D_{\mu \kappa }^{\beta } P_{\nu 
\tau }^{\beta } +\Gamma_{\mu \nu \kappa \tau }^{\text{NS} } 
$$ (eqn:94)

$$\Gamma_{\mu \nu \kappa \tau }^{\text{NS} } =\sum_{i_{\alpha } j_{\alpha } 
a_{\alpha } b_{\alpha } } { c_{\mu i}^{\alpha } c_{\nu a}^{\alpha } c_{\kappa 
j}^{\alpha } c_{\tau b}^{\alpha } t_{a_{\alpha } b_{\alpha } }^{i_{\alpha } 
j_{\alpha } } } +\sum_{i_{\beta } j_{\beta } a_{\beta } b_{\beta } } 
{c_{\mu i}^{\beta } c_{\nu a}^{\beta } c_{\kappa j}^{\beta } c_{\tau 
b}^{\beta } t_{a_{\beta } b_{\beta } }^{i_{\beta } j_{\beta } } } 
+2\sum_{i_{\alpha } j_{\beta } a_{\alpha } b_{\beta } } { c_{\mu 
i}^{\alpha } c_{\nu a}^{\alpha } c_{\kappa j}^{\beta } c_{\tau b}^{\beta } 
t_{a_{\alpha } b_{\beta } }^{i_{\alpha } j_{\beta } } } 
$$ (eqn:95)

因此，不可分离部分只是振幅从 MO 到 AO 基的反变换。但对双粒子密度矩阵进行对称化很重要，以便能够利用 AO 导数积分的完全置换对称性。



(sec:modelchemistries.mp2.optmethod)=
## 轨道优化 MP2 方法（Orbital Optimized MP2 Methods）


### OO-MP2 理论
```{index} OO-MP2
```

MP2 能量可以被视为对 MP2 振幅是驻定的，因为可以认为它们已通过对 Hylleraas 泛函的最小化进行了优化：

$$E_{\text{MP2} } =\min\limits_{\mathrm{\mathbf{t} }} \left\{{ 2\left\langle { \Psi 
_{1} \vert \hat{{H} }\vert \Psi_{0} } \right\rangle+\left\langle {\Psi_{1} \vert \hat{{H} }_{0} -E_{0} \vert \Psi_{1} } 
\right\rangle} \right\}$$ (eqn:96)

$\hat{{H} }$ 是 Møller 和 Plesset 提出的 0 阶哈密顿量，$\Psi_{0}$ 是参考行列式，$\Psi_{1}$ 是一阶波函数，$E_{0} =E_{\text{HF} } =\left\langle\Psi_{\text{HF} } \right|\hat{{H} }\left| \Psi_{\text{HF} }\right\rangle$ 是参考能量。量 $\mathbf{t}$ 统称 MP2 振幅。

OO-MP2 方法的基本思想是不仅对 MP2 振幅最小化 MP2 能量，还对轨道的变化额外最小化总能量。由于 MP2 能量对 MO 系数不是变分的（variational），不考虑关联场引起的轨道弛豫。如果参考行列式较差，低阶微扰校正就会变得不可靠。通过在参考行列式中选择更好的轨道，可以在很大程度上缓解这一点。该假设正确性的数值证据将在下面给出。

为了允许轨道弛豫，Hylleraas 泛函可以被视为波函数振幅 $\mathbf{t}$ 和下面将定义的轨道旋转参数 $\mathbf{R}$ 的泛函。通过适当的参数化，无需通过拉格朗日乘子确保轨道正交归一性。我们最小化的泛函为：

$$L\left\{\mathbf{t,\, R}\right\}= E_{0} \left[{ \mathbf{R} } 
\right]+2\left\langle\Psi_{1} \right|\hat{{H} }\left| \Psi_{0} \right\rangle
+\left\langle\Psi_{1} \right|\hat{H}_0 - E_0 \left| \Psi_{1} \right\rangle
$$ (eqn:97)

$\Psi_{0}$ 是参考行列式。然而，它不再对应于哈特里-福克（HF）行列式。因此，参考能量 $E_{0} \left[{ \mathbf{R} } \right]=\left\langle { \Psi_{0} \left[{ \mathbf{R} } \right]} \right|\hat{{H} }\left|\Psi_{0} \left[{ \mathbf{R} } \right] \right\rangle$ 在变分过程中也会变化，并且不再对 HF MO 系数驻定。显然，$E_{0} \left[{ \mathbf{R} } \right]\geqslant E_{\text{HF} }$，因为 HF 行列式按构造就是具有完整哈密顿量最低期望值的单行列式。

参考能量由下式给出：

$$E_{0} \left[{ \mathbf{R} } \right]=\sum_i { \left\langle i \right|h\left|i
\right\rangle+\frac{1}{2}\sum_{ij} { \left\langle { ij} || ij
\right\rangle} } 
$$ (eqn:98)

不包括单激发的一阶波函数为：

$$\left| \Psi_1 \right\rangle= \frac{1}{4} \sum_{ijab} t_{ab}^{ij} | \left. \Psi_{ij}^{ab} \right\rangle
$$ (eqn:99)

一个概念上重要的要点是 Brillouin 定理（Brillouin's theorem）{cite}`jensen1999intro` 不再被遵守，因为 Fock 矩阵将包含非对角块。在这种情况下，一阶波函数将包含来自单激发的贡献。由于轨道优化引入了单激发的所有重要效应，我们倾向于将它们排除在处理之外。任何相反的尝试都将破坏收敛性质。尽管如此，我们还是考虑过以微扰方式包含单激发：

$$E_{\text{Singles} }^{(2) } =-\sum_{ia} { \frac{\left|{ F_{ia} } 
\right|^{2} }{\varepsilon_{a} -\varepsilon_{i} } } 
$$ (eqn:100)

这一校正的微扰性质会破坏总能量的驻定性，因而是不可取的。此外，包含单激发贡献的结果相对下文报告的结果没有任何改进。因此它们不会在下文记录，并从此在 OO-MP2 方法中默认省略。

采用 RI 近似的轨道优化 MP2 Hylleraas 泛函（OO-RI-MP2）的显式形式为：

$$L_{\infty} \left[{ \mathbf{t,\, R} } \right]=\sum_i { \left\langle i \right|} 
\hat{{h} }\left|i \right\rangle+\frac{1}{2}\sum_{ij} { \left\langle {ij} || ij \right\rangle+\sum_{iaP} { (ia\vert P)\Gamma 
_{ia}^{'P} } } +\sum_{ij} { D_{ij} F_{ij} } +\sum_{ab} { D_{ab} 
F_{ab} } 
$$ (eqn:101)

其中：

$$\Gamma_{ia}^{'P} =\sum_Q { V_{PQ}^{-1} \sum_{jb} { (Q\vert 
jb)t_{ab}^{ij} } } 
$$ (eqn:102)

$$(ia\vert P)=\int{ \int{ \psi_{i} (\mathbf{r}_{1} ) } } \psi_{a} (\mathbf{r}_{1} 
)\frac{1}{\left|{ \mathbf{r}_{1} \mathbf{\, }-\mathbf{\, r}_{2} } \right|}\eta 
_{P} (\mathbf{r}_{2} )d\mathbf{r}_{1} d\mathbf{r}_{2} 
$$ (eqn:103)

$$(P\vert Q)=\int{ \int{ \eta_{p} } } (\mathbf{r}_{1} )\frac{1}{\left|{\mathbf{r}_{1} \mathbf{\, }-\mathbf{\, r}_{2} } \right|}\eta_{Q} (\mathbf{r}_{2} 
)d\mathbf{r}_{1} d\mathbf{r}_{2} 
$$ (eqn:104)

其中，$\left\{\psi \right\}$ 是正交归一分子轨道集合，$\left\{\eta \right\}$ 表示辅助基组。$F_{pq}$ 表示 Fock 矩阵元：

$$F_{pq} =\left\langle p \right|\hat{{h} }\left| q \right\rangle+\sum_k 
{\left\langle { pk} || qk \right\rangle} 
$$ (eqn:105)

并且要求轨道分别对角化占据和虚子空间：

$$\begin{array}{l}
 F_{ij} =\delta_{ij} F_{ii} =\delta_{ij} \varepsilon_{i} \\ 
 F_{ab} =\delta_{ab} F_{aa} =\delta_{ab} \varepsilon_{a} \\ 
 \end{array}
$$ (eqn:106)

类 MP2 密度块为：

$$\begin{array}{l}
 D_{ij} =-\frac{1}{2}\sum_{kab} { t_{ab}^{ik} t_{ab}^{jk} } \\ 
 D_{ab} =\frac{1}{2}\sum_{ijc} { t_{ac}^{ij} t_{bc}^{ij} } \\ 
 \end{array}
$$ (eqn:107)

其中在 Fock 矩阵为块对角的情况下，MP2 振幅通过条件 $\frac{\partial L_{\infty} }{\partial t_{ab}^{ij} }=0$ 获得：

$$t_{ab}^{ij} =-\frac{\left\langle { ij} || ab \right\rangle
}{\varepsilon_{a} +\varepsilon_{b} -\varepsilon_{i} -\varepsilon_{j} }
$$ (eqn:108)

轨道变化由反厄米矩阵（anti-Hermitian matrix）$\mathbf{R}$ 和指数拟设（exponential Ansatz）参数化：

$$\begin{array}{c}
 \mathbf{c}^{\text{new} }=\mathbf{c}^{\text{old} }\exp (\mathbf{R}) \\ 
 \mathbf{R}=\left({ {\begin{array}{*{20}c}
 0 \hfill & { \mathbf{R}_{ia} } \hfill \\
 { -\mathbf{R}_{ia} } \hfill & 0 \hfill \\
\end{array} } } \right) \\ 
 \end{array}
$$ (eqn:109)

轨道变化到二阶为：

$$\begin{array}{l}
 \exp (\mathbf{R})\left|i \right\rangle=\left|i \right\rangle+\sum_a 
{\mathbf{R}_{ai} \left| a \right\rangle} -\frac{1}{2}\sum_{jb} { \mathbf{R}_{bi} \mathbf{R}_{bj} 
\left| j \right\rangle+ \dots} \\ 
 \exp (\mathbf{R})\left| a \right\rangle=\left| a \right\rangle-\sum_i 
{\mathbf{R}_{ai} \left| i \right\rangle} -\frac{1}{2}\sum_{jb} { \mathbf{R}_{aj} \mathbf{R}_{bj} 
\left| b \right\rangle+ \dots} \\ 
 \end{array}
$$ (eqn:110)

通过这一拟设确保轨道保持正交归一，无需引入拉格朗日乘子。Fock 算符因轨道旋转产生的一阶展开为：

$$F_{pq} \left[ R \right]=F_{pq} \left[ 0 \right]+R_{pq}^{(1) } +\sum_r 
{R_{rp} F_{rq} \left[ 0 \right]+R_{rq} F_{pr} \left[ 0 \right]} 
$$ (eqn:111)

$$R_{pq}^{(1) } =\sum_{kc} { R_{ck} \left\{{ \left\langle { pc}|| qk \right\rangle+ \left\langle { pk} || qc 
\right\rangle} \right\}}
$$ (eqn:112)

一阶能量变化变为（$\left({ h_{pq} \equiv \left\langle p \right|\hat{{h} }\left| q \right\rangle,g_{pqrs} \equiv \left\langle { pq} || rs \right\rangle} \right)$）：

$$\begin{array}{c}
 L_{\infty } \left[{ \mathbf{t,R} } \right]=\sum_{ic} { R_{ci} \left({ h_{ci} 
+h_{ic} } \right)+\frac{1}{2}\sum_{ijc} { R_{ci} \left({ g_{cjij} 
+g_{ijcj} } \right)} } +R_{cj} \left({ g_{icij} +g_{ijic} } \right) \\ 
 +2\sum_{iacP} { R_{ci} (ac\vert P)\Gamma_{ia}^{'P} } 
-2\sum_{ikaP} { R_{ak} (ik\vert P) } \Gamma_{ia}^{'P} \\ 
 -\sum_{ij} { D_{ij} \left({ R_{ij}^{(1) } +\sum_c { \left({R_{ci} F_{cj} +R_{cj} F_{ic} } \right)} } \right)} \\ 
 +\sum_{ab} { D_{ab} \left({ R_{ab}^{(1) } -\sum_k { \left({R_{ak} F_{kb} +R_{bk} F_{ak} } \right)} } \right)} \\ 
 \end{array}
$$ (eqn:113)

能量泛函对轨道旋转驻定的条件（$\left({ \frac{\partial L_{\infty} \left[{ \mathbf{t,R} } \right]}{\partial R_{ai} }=0} \right)$）给出轨道梯度的表达式，从而给出 OO-RI-MP2 拉格朗日量的表达式。

$$\frac{\partial L_{\infty} [ \mathbf{t},\mathbf{ R}]}{\partial R_{ai} }\equiv 
g_{ai} = 2F_{ai} +2\sum_j { D_{ij} F_{aj} -2\sum_b { D_{ab} 
F_{ib} +R^{(1) }(\mathrm{\mathbf{D} })_{ai} } } 
$$ (eqn:114)

$$+2\sum_{cP} { (ac\vert P)\Gamma_{ia}^{\prime P} -2\sum_{kP} 
{(ik\vert P)\Gamma_{ia}^{\prime P} } }$$

轨道优化过程的目标是使该梯度变为零。显然有许多方法可以实现这一点。根据我们的经验，以下简单过程基本上是令人满意的。我们首先在当前 MO 基中构建一个具有以下结构的矩阵 $\mathbf{B}$：

$$\begin{array}{c}
 \mathbf{B}_{ij} =\delta_{ij} \mathbf{F}_{ii} \\ 
 \mathbf{B}_{ab} =\delta_{ab} (\mathbf{F}_{aa} + \boldsymbol{\Delta} ) \\ 
 \mathbf{B}_{ai} =\mathbf{B}_{ia} = \mathbf{g}_{ai} \\ 
 \end{array}
$$ (eqn:115)

其中 $\Delta$ 是能级移动参数。该矩阵的占据/占据和虚/虚块是任意的，但其定义对方法的收敛性质有影响。块对角化 Fock 矩阵的轨道能量似乎是一个合乎逻辑的选择。如果梯度为零，**B**-矩阵就是对角的。因此，通过对角化 **B** 可以得到一组改进的轨道。

为了加速收敛，使用标准 DIIS 方案。{cite}`koch2000achemist,mcweeny1992methods` 然而，为了对 **B**-矩阵进行 DIIS 外推（extrapolation），必须使用一个不随迭代变化的公共基组。由于 **B**-矩阵本身定义在当前迭代的分子轨道中，我们选择 HF 计算的 MO 作为公共正交归一轨道集。外推在此基组中进行，外推后的 **B**-矩阵在对角化之前变换回当前 MO 集。显然，同样的策略可以用于任何具有轨道梯度的方法中的轨道优化。

对于表现良好的情形，这一简单方案在 5-10 次迭代内收敛。过渡金属和更复杂的分子可能需要多达 20 次迭代和能级移动才能达到收敛。

收敛后，矩阵 $\mathbf{D}$ 与参考行列式密度 $P_{\mu \nu } =\sum_i { c_{\mu i} c_{\nu i} }$ 之和构成 OO-MP2 方法的真正单粒子密度矩阵，可用于性质或梯度计算。

(sec:modelchemistries.mp2.optmethod.usage)=
### OO-MP2 —— 提示、用法与示例

通过使 Hylleraas 泛函对轨道旋转驻定，得到轨道优化 MP2 方法，它在 ORCA 中与 RI 近似结合实现（OO-RI-MP2）。从这些计算中可以得到在二阶多体微扰理论水平上适应动态关联场的轨道。此外，OO-RI-MP2 方法的总能量低于 RI-MP2 方法本身。可以将该方法视为多组态 SCF 理论的一种特殊形式，只不过哈密顿量被分为 0 阶项和微扰。

OO-RI-MP2 方法的主要好处是它在一定程度上"修复"了较差的哈特里-福克轨道，这对受困于哈特里-福克处理中库仑洞和交换洞不平衡的体系应特别有益。根据迄今获得的经验，OO-RI-MP2 方法对有机分子的热化学并不比 RI-MP2 本身更好。然而，对于反应能垒和自由基，OO-MP2 相对 MP2 的好处是显著的。对于 OO-RI-MP2 的自旋分量缩放变体 OO-RI-SCS-MP2 来说尤其如此。此外，OO-RI-MP2 方法大幅降低了自由基 UHF 计算中的自旋污染（spin contamination）。

由于 OO-MP2 方法的每次迭代与 RI-MP2 弛豫密度计算一样昂贵，计算成本远高于 RI-MP2 本身。相对于正常计算的 RI-MP2 时间，预计计算时间增加约 10 倍。对于 1000--2000 个基函数范围内的计算这可能仍是可行的（不过上限意味着非常可观的计算成本）。轨道优化 MP2 方法的完整评估已经发表。{cite}`Neese2009ooscsmp2`

OO-RI-MP2 通过简单输入行中的 `! OO-RI-MP2` 或 `! OO-RI-SCS-MP2`（带自旋分量缩放）或 `%mp2` 块中的 `OrbOpt true` 触发。该方法带有以下新变量：

```orca
%mp2 OrbOpt  true   # turns on the orbital optimization
     CalcS2  false  # calculate the S**2 expectation value
                    # in spin-unrestricted calculations
     MaxOrbIter 64  # Max. number of iterations
     MP2Shift  0.1  # Level shift for the procedure
     end
```

求解器是一个带附加能级移动的简单 DIIS 型方案。我们发现先收敛哈特里-福克方程并没有真正的益处。因此，额外使用关键词 `! noiter` 以在进入轨道优化之前关闭标准哈特里-福克 SCF 过程是明智的。

OO-RI-MP2 方法为 RHF 和 UHF 参考波函数实现。提供解析梯度。

在 OO-RI-MP2 计算中不需要单独请求密度，因为它会自动计算。此外，弛豫和非弛豫密度没有区别，因为 OO-RI-MP2 能量对所有波函数参数是完全驻定的，因而非弛豫和弛豫密度重合。

(sec:modelchemistries.mp2.regularized)=
## 正则化 MP2 与 RI-MP2（Regularized MP2 and RI-MP2）

正则化 MP2 是二阶 Moller-Plesset 理论（MP2）的一种变体，由 J. Shee、M. Loipersberger、A. Rettig、J. Lee 和 M. Head-Gordon {cite}`Shee2021` 提出，旨在提高其对具有 $\pi$ 驱动色散相互作用的体系和过渡金属配合物中配位键（dative bonds）的精度。该方法通过引入单参数、能隙依赖的正则化（regularization）来实现这一点，该正则化阻尼被高估的成对可加（pairwise additive）贡献，从而重新归一化一阶振幅以经验地模拟更高阶关联。

为此，标准 MP2 能量（以及标准算法）被修改。对于 $\sigma$ $\text{(}p=1\text{)}$ 和 $\sigma^2$ $\text{(}p=2\text{)}$ 正则化，能量按下式修改

$$
E_{\sigma^p\text{-MP2}} = -\dfrac{1}{4} \sum_{ijab} \dfrac{|\left\langle ij||ab \right\rangle |^2}{\Delta_{ij}^{ab}} (1-e^{-\sigma(\Delta_{ij}^{ab})^p})
$$

这对应于对一阶振幅的正则化。
对于 $\kappa$ 正则化，MP2 能量按下式修改

$$
E_{\kappa\text{-MP2}} = -\dfrac{1}{4} \sum_{ijab} \dfrac{|\left\langle ij||ab \right\rangle |^2}{\Delta_{ij}^{ab}} \left(1-e^{-\kappa(\Delta_{ij}^{ab})}\right)^2
$$

这对应于对一阶振幅和交换积分的正则化。

正则化 MP2 可用于"内存模式"（Q1Opt$>$0）下的标准 MP2 和 RI-MP2（RIJDX、RIJCOSX、RIJK）。

正则化 MP2 的使用由 `DoRegMP2` 关键词控制，正则化类型可通过将 `RegMP2Type` 参数设为 0（$\kappa$）、1（$\sigma$）或 2（$\sigma^2$）来指定。正则化器（regularizers）的值可以分别用 `RegMP2Kappa` 和 `RegMP2Sigma` 指定。

```orca
%mp2
    DoRegMP2     true   # required
    RegMP2Type   0      # kappa regularizer
                 1      # sigma regularizer
                 2      # sigma-squared regularizer
    RegMP2Kappa  1.1    # kappa value
    RegMP2Sigma  0.5    # sigma value
end
```

需要注意的是，正则化 MP2 目前仅提供并测试了单点能。密度、梯度和 Hessian 计算尚不支持。

(sec:modelchemistries.mp2.keywords)=
## 关键词（Keywords）

:::{raw} latex
\begingroup
\footnotesize
:::
(tab:modelchemistries.mp2.keywords.simple)=
:::{flat-table} 选择 MP2 变体的简单输入关键词（Simple input keywords selecting MP2 variants）。
:header-rows: 1
:class: footnotesize
* - 关键词（Keyword）
  - 描述（Description）
* - `MP2`
  - 正则 MP2（Canonical MP2）
* - `RI-MP2`
  - RI-MP2（别名：`RIMP2`、`MP2RI`）
* - `DLPNO-MP2`
  - DLPNO-MP2
* - `SCS-MP2`
  - 自旋分量缩放的正则 MP2
* - `SCS-MP2`
  - 自旋反向缩放的正则 MP2
* - `RI-SCS-MP2`
  - 自旋分量缩放的 RI-MP2（别名：`SCS-RI-MP2`、`SCS-RIMP2`）
* - `RI-SOS-MP2`
  - 自旋反向缩放的 RI-MP2（别名：`SOS-RI-MP2`、`SOS-RIMP2`）
* - `DLPNO-SCS-MP2`
  - 自旋分量缩放的 DLPNO-MP2（别名：`SCS-DLPNO-MP2`）
* - `DLPNO-SOS-MP2`
  - 自旋反向缩放的 DLPNO-MP2（别名：`SOS-DLPNO-MP2`）
* - `RI-SCS-MP2`
  - 自旋反向缩放的 RI-MP2（别名：`SOS-RI-MP2`、`SOS-RIMP2`）
* - `OO-RI-MP2`
  - 轨道优化的 RI-MP2（别名：`OO-RIMP2`、`OO-MP2RI`）
* - `OO-RI-SCS-MP2`
  - 轨道优化的自旋分量缩放 RI-MP2（别名：`OO-SCS-RI-MP2`、`OO-SCS-RIMP2`）
* - `OO-RI-SOS-MP2`
  - 轨道优化的自旋反向缩放 RI-MP2（别名：`OO-SOS-RI-MP2`、`OO-SOS-RIMP2`）
* - `F12-MP2`
  - 带 F12 校正的 MP2（别名：`MP2-F12`）
* - `F12-RI-MP2`
  - 带 F12 校正的 RI-MP2（别名：`MP2-F12-RI`、`RI-MP2-F12`）
* - `F12/D-RI-MP2`
  - 带 F12 校正的 RI-MP2，采用低成本 D 近似
    （别名：`MP2-F12/D-RI`、`RI-MP2-F12/D`、`F12D-RI-MP2`、`MP2-F12D-RI`、`RI-MP2-F12D`）
* - `F12-DLPNO-MP2`
  - 带 F12 校正的 DLPNO-MP2（别名：`DLPNO-MP2-F12`）
* - `F12/D-DLPNO-MP2`
  - 带 F12 校正的 DLPNO-MP2，采用低成本 D 近似
    （别名：`DLPNO-MP2-F12/D`、`F12D-DLPNO-MP2`、`DLPNO-MP2-F12D`）
* - `LoosePNO`
  - 为 DLPNO-MP2 选择宽松阈值
* - `NormalPNO`
  - （默认）为 DLPNO-MP2 选择默认阈值
* - `TightPNO`
  - 为 DLPNO-MP2 选择严格阈值
:::
:::{raw} latex
\endgroup
:::
