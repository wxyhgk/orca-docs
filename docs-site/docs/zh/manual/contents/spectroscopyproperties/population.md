

<a id="sec:spectroscopyproperties.pop"></a>
# 布居分析（Population Analysis）

原子布居相关的量不是真实的分子性质，因为它们不是可观测量。
尽管如此，它们对解释实验和计算结果非常有用。
ORCA 中提供了多种分析计算所得 SCF 波函数的方式。
默认情况下，ORCA 通过
[Mulliken](#sec:spectroscopyproperties.pop.mulliken)、
[Löwdin](#sec:spectroscopyproperties.pop.loewdin) 和
[Mayer](#sec:spectroscopyproperties.pop.mayer)
布居分析，提供关于计算所得分子轨道和化学键的非常详细的信息。

!!! info
    由于这些方法通常会产生大量的特定输出，我们一般建议阅读
    [输出控制](#sec:essentialelements.output) 一节。

    `!ReducedPOP` 关键词特别有用，因为它减少布居分析部分的打印信息，
    给出每个原子的轨道布居以及各基函数类型的百分比贡献。
    这对于弄清 MO 的特征非常有用。

<a id="sec:spectroscopyproperties.pop.mulliken"></a>
## Mulliken 布居分析（Mulliken Population Analysis）

Mulliken 布居分析 [mulliken1955pop](../../bibliography.md) 尽管有诸多众所周知的缺点，
仍是大多数量子化学程序中的标准方法。
它利用基函数向分子中给定原子的归属以及基函数重叠来划分总密度。
若将总电荷密度写为 $\rho \left({ \vec{r} } \right)$，
电子总数为 $N$，则有：

$$
\in t{ \rho \left({ \vec{r} } \right)d\vec{r} } =N\qquad \text{(eqn:299)}
$$

由密度矩阵 $\mathrm{P }$ 和基函数 $\phi$：

$$
\rho \left({ \vec{r} } \right)=\sum\limits_{\mu \nu } { P_{\mu \nu } \phi
_{\mu } \left({ \vec{r} } \right)\phi_{\nu } \left({ \vec{r} } \right)}\qquad \text{(eqn:300)}
$$

因此：

$$
\in t{ \rho \left({ \vec{{r} }} \right)d\vec{{r} }} =\sum\limits_{\mu \nu }
{P_{\mu \nu } \underbrace{ \in t{ \phi_{\mu } \left({ \vec{{r} }} \right)\phi
_{\nu } \left({ \vec{{r} }} \right)d\vec{{r} }} }_{S_{\mu \nu } } }\qquad \text{(eqn:301)}
$$

$$
%\hspace{1cm}
=\sum\limits_{\mu \nu } { P_{\mu
\nu } S_{\mu \nu } }\qquad \text{(eqn:302)}
$$

将每个基函数指派给给定中心后，上式可改写为：

$$
\hspace{2.5cm}
=\sum\limits_A { \sum\limits_B
{\sum\limits_\mu{ ^{A}\sum\limits_\nu{ ^{B}P_{\mu \nu }^{AB} S_{\mu \nu
}^{AB} } } } }\qquad \text{(eqn:303)}
$$

$$
\hspace{4cm}
=\sum\limits_A { \sum\limits_\mu{^{A}\sum\limits_\nu{ ^{A}P_{\mu \nu }^{AA} S_{\mu \nu }^{AA} } } }
+2\sum\limits_A { \sum\limits_{B<A} { \sum\limits_\mu{ ^{A}\sum\limits_\nu{^{B}P_{\mu \nu }^{AB} S_{\mu \nu }^{AB} } } } }\qquad \text{(eqn:304)}
$$

Mulliken 提议将第二项在涉及的每对原子之间均分，
并定义中心 $A$ 上的电子数 $N_{A}$ 为：

$$
N_{A} =\sum\limits_\mu{ ^{A}\sum\limits_\nu{ ^{A}P_{\mu \nu }^{AA} S_{\mu
\nu }^{AA} } } +\sum\limits_{B\ne A} { \sum\limits_\mu{ ^{A}\sum\limits_\nu{^{B}P_{\mu \nu }^{AB} S_{\mu \nu }^{AB} } } }\qquad \text{(eqn:305)}
$$

使得 $\sum\limits_A { N_{A} } =N$。
分子中原子的电荷为：

$$
Q_{A} =Z_{A} -N_{A}\qquad \text{(eqn:306)}
$$

其中 $Z_{A}$ 是原子 $A$ 的芯电荷。
位于不同原子上的一对基函数之间的交叉项是重叠电荷，
ORCA 用它定义 Mulliken 键级：

$$
B_{AB} =2\sum\limits_\mu{ ^{A}\sum\limits_\nu{ ^{B}P_{\mu \nu }^{AB} S_{\mu
\nu }^{AB} } }\qquad \text{(eqn:307)}
$$

<a id="sec:spectroscopyproperties.pop.mulliken.basicusage"></a>
### 基本用法（Basic Usage）

Mulliken 布居分析可通过 `!MULLIKEN` 输入关键词调用：

```orca
! MULLIKEN
```

也可通过 `%output` 块中的 `Print[ P_Mulliken ] 1` 关键词请求

```orca
%output
  Print[ P_Mulliken ] 1  # default = on
end
```

可在 `%output` 块中指定若干附加选项，以控制 Mulliken 布居分析的细节。
默认情况下 Mulliken 布居分析是开启的。

```orca
%output
  Print[ P_AtCharges_M  ] 1     # Print atomic charges
  Print[ P_OrbCharges_M ] 1     # Print orbital charges
  Print[ P_FragCharges_M] 1     # Print fragment charges
  Print[ P_BondOrder_M  ] 1     # Print bond orders
  Print[ P_FragBondOrder_M ] 1  # Print fragment b.o.
  Print[ P_ReducedOrbPop_M ] 1  # Print reduced orb. Charges
  Print[ P_AtPopMO_M    ] 1     # Print atomic charges in each MO
  Print[ P_OrbPopMO_M   ] 1     # Print orbital populaiton for each MO
  Print[ P_ReducedOrbPopMO_M] 1 # Print reduced orbital pop for each MO
  Print[ P_FragPopMO_M  ] 1     # Print the fragment population for for each MO
end
```

这些选项允许获得关于计算所得波函数的非常详细的信息，
比直接查看 MO 方便得多。
"约化轨道布居"（reduced orbital population）是按角动量类型的布居。
例如，给定原子上每个 p$_{z}$ 轨道布居之和
就是 p$_{z}$ 函数的约化轨道布居。

请注意，对于[有限温度 HF 或 KS-DFT](#sec:essentialelements.scf.finitetemp) 计算
（`SmearTemp` $>$ 0 K，分数占据数或 [FOD 分析](#sec:spectroscopyproperties.fod)），
只打印基于 $\rho^{FOD}$ 的 Mulliken 约化轨道电荷。

<a id="sec:spectroscopyproperties.pop.loewdin"></a>
## Löwdin 布居分析（Löwdin Population Analysis）

Löwdin 分析 [szabo1989modern](../../bibliography.md) 比 Mulliken 分析更直接一些。
在 Löwdin 方法中，变换到一个所有重叠积分都消失的基。
这通过 Löwdin 对称正交归一化矩阵 $\mathrm{S }^{-1/2}$ 实现。
利用该变换矩阵，新的基函数是多中心的，
但在最小二乘意义上尽可能接近原始的严格定域原子基函数。
布居分析利用了变换后函数与原始函数之间的相似性。
密度矩阵按下式变换：

$$
\mathrm{P }^{L}=\mathrm{S }^{1/2}\mathrm{PS }^{1/2}\qquad \text{(eqn:308)}
$$

则原子布居为：

$$
N_{A} =\sum\limits_\mu{ ^{A}P_{\mu \mu }^{L} }\qquad \text{(eqn:309)}
$$

键级由 Wiberg 指数 [wiberg1968tetrahedron](../../bibliography.md) 定义，
该指数最初用于半经验方法（它们从一开始就表述在 Löwdin 基中）：

$$
B_{AB} =\sum\limits_\mu{ ^{A}\sum\limits_\nu{ ^{B}\left({ P_{\mu \nu }^{L} }
\right)^{2} } }\qquad \text{(eqn:310)}
$$

<a id="sec:spectroscopyproperties.pop.loewdin.basicusage"></a>
### 基本用法（Basic Usage）

Löwdin 布居分析可通过 `!LOEWDIN` 输入关键词调用。
默认情况下 Löwdin 布居分析是开启的，
并提供比 Mulliken 分析稍多的细节。

```orca
! MULLIKEN
```

也可通过 `%output` 块中的 `Print[ P_Loewdin ] 1` 关键词请求：

```orca
%output
  Print[ P_Loewdin ] 1  # default = on
end
```

Löwdin 布居分析输出的细节可通过 `%output` 块控制：

```orca
%output
  Print[ P_AtCharges_L  ] 1     # Print atomic charges
  Print[ P_OrbCharges_L ] 1     # Print orbital charges
  Print[ P_FragCharges_L] 1     # Print fragment charges
  Print[ P_BondOrder_L  ] 1     # Print bond orders
  Print[ P_FragBondOrder_L ] 1  # Print fragment b.o.
  Print[ P_ReducedOrbPop_L ] 1  # Print reduced orb. Charges
  Print[ P_AtPopMO_L    ] 1     # Print atomic charges in each MO
  Print[ P_OrbPopMO_L   ] 1     # Print orbital population for each MO
  Print[ P_ReducedOrbPopMO_L] 1 # Print reduced orbital pop for each MO
  Print[ P_FragPopMO_L  ] 1     # Print the fragment population for each MO
end
```

此外，可在 `%method` 块中设置键级打印的阈值。

```orca
%method
  LOEWDIN_BONDORDERTHRESH 0.05
end
```

<a id="sec:spectroscopyproperties.pop.fmopop"></a>
## 前线分子轨道布居（Frontier Molecular Orbital Populations）

由于前线轨道通常特别受关注，可通过 "`FMOPop`" 关键词请求 HOMO 和 LUMO 的
[Mulliken](#sec:spectroscopyproperties.pop.mulliken) 和
[Löwdin](#sec:spectroscopyproperties.pop.loewdin) 布居：

```orca
! FMOPop
```

HOMO 和 LUMO 前线轨道相应的 Mulliken 和 Loewdin 布居
将打印在输出中：

```orca
----------------------------------------------
FRONTIER MOLECULAR ORBITAL POPULATION ANALYSIS
----------------------------------------------

ANALYZING ORBITALS: HOMO=   6 LUMO=   7

-------------------------------------------------------------------------
   Atom        Q(Mulliken)     Q(Loewdin)     Q(Mulliken)     Q(Loewdin) 
              <<<<<<<<<<<<HOMO>>>>>>>>>>>>   <<<<<<<<<<<<LUMO>>>>>>>>>>>>
-------------------------------------------------------------------------
   0-C         0.937186        0.906827       0.804044        0.755610
   1-O         0.062814        0.093173       0.195956        0.244390
-------------------------------------------------------------------------
```

<a id="sec:spectroscopyproperties.pop.mayer"></a>
## Mayer 布居分析（Mayer Population Analysis）

Mayer 的成键分析
[mayer1983chem,mayer1984int,mayer1985theor,mayer1987modelling](../../bibliography.md)
是另一种定义化学上有用指标的创造性尝试。
Mayer 原子电荷与 Mulliken 电荷相同。
Mayer 键级定义为：

$$
B_{AB} =\sum\limits_\mu{ ^{A}\sum\limits_\nu{ ^{B}\left({ \mathrm{PS }}
\right)_{\mu \nu } \left({ \mathrm{PS }} \right)_{\nu \mu } +\left({ \mathrm{RS }} \right)_{\mu \nu }
\left({ \mathrm{RS }} \right)_{\nu \mu } } }\qquad \text{(eqn:311)}
$$

其中 $\mathrm{P }$ 是总电子密度矩阵，
$\mathrm{R }$ 是自旋密度矩阵。
这些 Mayer 键级非常有用。
原子 $A$ 的 Mayer 总价定义为：

$$
V_{A} =2N_{A} -\sum\limits_\mu{ ^{A}\sum\limits_\nu{ ^{A}\left({ \mathrm{PS }} \right)_{\mu \nu } \left({ \mathrm{PS }} \right)_{\nu \mu } } }\qquad \text{(eqn:312)}
$$

在正常成键情形和正常基组下，$V_{A}$ 应当
与化学意义上原子 $A$ 的化合价相当接近（即碳原子接近四）。
成键价（bonded valence）由下式给出：

$$
X_{A} =V_{A} -\sum\limits_{B\ne A} { B_{AB} }\qquad \text{(eqn:313)}
$$

最后，自由价（free valence，衡量形成更多化学键的能力）由下式给出：

$$
F_{A} =V_{A} -X_{A}\qquad \text{(eqn:314)}
$$

<a id="sec:spectroscopyproperties.pop.mayer.basicusage"></a>
### 基本用法（Basic Usage）

Mayer 布居分析可通过 `!MAYER` 关键词调用：

```orca
! MAYER
```

也可通过 `%output` 块中的 `Print[ P_Mayer ] 1` 关键词请求：

```orca
%output
  Print[ P_Mayer ] 1  # default = on
end
```

输出相当简短，无法进一步控制。
默认情况下 Mayer 布居分析是开启的。
此外，可在 `%method` 块中设置键级打印的阈值。

```orca
%method
  MAYER_BONDORDERTHRESH 0.1
end
```

<a id="sec:spectroscopyproperties.pop.natural"></a>
## 自然布居分析（Natural Population Analysis）

如果你能获得 Weinhold 研究组的 `gennbo` 程序版本 [^a]，
可通过 [NBO 接口](#sec:spectroscopyproperties.nbo)请求自然布居分析（NPA）。

[^a]: 关于 NBO 程序的信息见 <http://nbo7.chem.wisc.edu>

!!! warning
    只有正确提供了 NBO 程序才会执行 NPA。
    否则 ORCA 将跳过 NPA 分析。

<a id="sec:spectroscopyproperties.pop.natural.basicusage"></a>
### 基本用法（Basic Usage）

自然布居分析可通过 `!NPA` 关键词调用：

```orca
! NPA
```

也可通过 `%output` 块中的 `Print[ P_NPA ] 1` 关键词请求：

```orca
%output
  Print[ P_NPA ] 1  # default = off
end
```

<a id="sec:spectroscopyproperties.pop.hirshfeld"></a>
## Hirshfeld 布居分析（Hirshfeld Population Analysis）

Hirshfeld 的分割方法是所谓分子中的原子
（atoms in molecules，AIM）方法中最常用的途径之一。[hirshfeld1977](../../bibliography.md)
此时，原子 A 的 AIM 密度 $\rho_A(\vec{r})$ 写为：

<a id="eq_aim_charge"></a>

$$
\rho_A(\vec{r}) = \rho(\vec{r})w_A(\vec{r})\qquad \text{(eq_aim_charge)}
$$

其中 $\rho(\vec{r})$ 是位置 $\vec{r}$ 处的总电荷密度，
$w_A(\vec{r})$ 是权重函数，在 Hirshfeld 方法中等于：

<a id="eq_w_hirshfeld"></a>

$$
w_A(\vec{r}) = \frac{\rho_A^0(\vec{r})}{\rho^0(\vec{r})}\qquad \text{(eq_w_hirshfeld)}
$$

其中 $\rho_A^0(\vec{r})$ 是原子 $A$ 的前原子密度（pro-atomic density），
$\rho^0(\vec{r})=\sum_A\rho_A^0(\vec{r})$ 是前分子密度（pro-molecular density）。
式 [Eq](#eq_aim_charge) 中的比值称为 _stockholder_。
由式 [Eq](#eq_aim_charge) 和 [Eq](#eq_w_hirshfeld) 可计算 Hirshfeld 电荷：

$$
Q_A^{\mathrm{Hirsh.}} = Z_A -\in t\rho_A(\vec{r})d\vec{r}\qquad \text{(eq_q_hirshfeld)}
$$

在 ORCA 中，Hirshfeld 方法中的前原子密度
通过每个元素一组高斯 s 函数的密度拟合计算。

<a id="sec:spectroscopyproperties.pop.hirshfeld.basicusage"></a>
### 基本用法（Basic Usage）

Hirshfeld 布居分析可通过 `!HIRSHFELD` 输入关键词调用。

```orca
! HIRSHFELD
```

也可通过 `%output` 块中的 `Print[ P_Hirshfeld ] 1` 关键词请求：

```orca
%output
  Print[ P_Hirshfeld ] 1  # default = off
end
```

<a id="sec:spectroscopyproperties.pop.hirshfeld.example"></a>
### 示例（Example）

作为一个例子，我们请求水分子的 Hirshfeld 电荷：

```mol
title: structure 1
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
3
structure (0 1)
O  0.00000006589375 0.00157184228646 0.00000000004493
H  0.77316868532439 -0.58666889665624 -0.00000000000005
H  -0.77316876182122 -0.58666895650640 -0.00000000000005
--- input ---
!HF cc-pVDZ TightSCF HIRSHFELD

* xyz 0 1
  O    0.00000006589375       0.00157184228646       0.00000000004493
  H    0.77316868532439      -0.58666889665624      -0.00000000000005
  H   -0.77316876182122      -0.58666895650640      -0.00000000000005
*
```

ORCA 在输出文件中打印如下信息：

```orca
------------------
HIRSHFELD ANALYSIS
------------------

Total integrated alpha density =      4.999998580
Total integrated beta density  =      4.999998580

  ATOM     CHARGE      SPIN
   0 O   -0.333756    0.000000
   1 H    0.166879    0.000000
   2 H    0.166879    0.000000

  TOTAL   0.000003    0.000000
```

<a id="sec:spectroscopyproperties.pop.mbis"></a>
## MBIS 电荷（MBIS Charges）

最小基迭代持股者（Minimal Basis Iterative Stockholder，MBIS）方法
是 Hirshfeld 方法的一个变体。[mbis2016](../../bibliography.md)
该方法的核心思想是将前原子密度 $\rho_A^0(\vec{r})$
在一组最小的、以原子为中心的 s 型 Slater 函数 $\rho_{Ai}^0(\vec{r})$ 上展开：

<a id="eq_sum_mbis"></a>

$$
\rho_A^0(\vec{r}) = \sum_{i=1}^{m_A}\rho_{Ai}^0(\vec{r})\qquad \text{(eq_sum_mbis)}
$$

其中 $\rho_{Ai}^0(\vec{r})$ 等于：

<a id="eq_rai_mbis"></a>

$$
\rho_{Ai}^0(\vec{r}) = \frac{N_{Ai}}{\sigma_{Ai}^38\pi}\mathrm{exp}\left(-\frac{\left|\vec{r}-\vec{R_A}\right|}{\sigma_{Ai}}\right)\qquad \text{(eq_rai_mbis)}
$$

这里 $m_A$ 是原子 $A$ 的壳层数。
布居 $N_{Ai}$ 和宽度 $\sigma_{Ai}$ 可写为：

<a id="eq_nai_mbis"></a>

$$
N_{Ai} = \in t\rho(\vec{r})\frac{\rho_{Ai}^0(\vec{r})}{\rho^0(\vec{r})}d\vec{r}\qquad \text{(eq_nai_mbis)}
$$

<a id="eq_sai_mbis"></a>

$$
\sigma_{Ai}=\frac{1}{3N_{Ai}}\in t\rho(\vec{r})\frac{\rho_{Ai}^0(\vec{r})}{\rho^0(\vec{r})}\left|\vec{r}-\vec{R_A}\right| d\vec{r}\qquad \text{(eq_sai_mbis)}
$$

为计算 AIM 密度 $\rho_A(\vec{r})$，MBIS 方法使用如下迭代算法：
(1) 为 $N_{Ai}$ 和 $\sigma_{Ai}$ 生成初始猜测，
并通过式 [Eq](#eq_sum_mbis) 和 [Eq](#eq_rai_mbis) 计算前原子密度；
(2) 通过式 [Eq](#eq_nai_mbis) 和 [Eq](#eq_sai_mbis) 得到新的 $N_{Ai}$ 和 $\sigma_{Ai}$ 组合；
(3) 若 $\rho_A(\vec{r})$ 达到收敛，迭代过程停止；
否则回到 (1)，但此时使用 $N_{Ai}$ 和 $\sigma_{Ai}$ 的最新估计值。

一旦 MBIS 迭代过程停止，MBIS 电荷计算为：

$$
Q_A^{\mathrm{MBIS.}} = Z_A -\in t\rho_A(\vec{r})d\vec{r}\qquad \text{(eq_q_mbis)}
$$

<a id="sec:spectroscopyproperties.pop.mbis.basicusage"></a>
### 基本用法（Basic Usage）

MBIS 布居分析可通过 `!MBIS` 输入关键词调用。

```orca
! MBIS
```

也可通过 `%output` 块中的 `Print[ P_MBIS ] 1` 关键词请求：

```orca
%output
  Print[ P_MBIS ] 1  # default = off
end
```

MBIS 电荷的收敛阈值设为 $10^{-6}$。
不过，可通过 `%method` 块中的标签 `MBIS_CHARGETHRESH` 更改：

```orca
%method
  MBIS_CHARGETHRESH 0.0001
end
```

<a id="sec:spectroscopyproperties.pop.mbis.quantities"></a>
### MBIS 相关量（MBIS Quantities）
ORCA 还可打印以下与 MBIS 相关的量： 

1. 原子偶极矩，
2. 原子四极矩，
3. 原子八极矩，以及
4. MBIS 密度的第三径向矩 $\left(\langle r^3\rangle_A = \in t \left|\vec{r}-\vec{R_A}\right|^3\rho_A(\vec{r})d\vec{r}\right)$。 

这些性质的打印由 `%method` 块中的 `MBIS_LARGEPRINT` 控制：

```orca
%method
  MBIS_LARGEPRINT true  # default = false
end
```

若激活该选项，在电荷达到收敛阈值后会额外执行一次迭代。

计算原子偶极矩、四极矩和八极矩的原点是每个原子的中心（默认）。
用户也可通过 `%method` 块中的 `MBIS_ORIGIN_MULT` 关键词定义全局原点（与原子无关）：

```orca
%method
  MBIS_ORIGIN_MULT  CenterOfCoords     # origin of coordinate system (0,0,0)
                    CenterOfMass       # center of mass
                    CenterOfNucCharge  # center of nuclear charge
                    CenterXYZ          # arbitrary position, set coordinates
		                       # with MBIS_ORIMULT_XYZ
                    CenterOfEachAtom   # center of each atom (default)
  MBIS_ORIMULT_XYZ  x,y,z # set the coordinates, otherwise 0,0,0 (unit: Angstrom)
end
```

<a id="sec:spectroscopyproperties.pop.mbis.example"></a>
### 示例（Example）

若我们请求氯仿分子在 cc-pVDZ 水平 HF 计算的 MBIS 电荷：

```mol
title: structure 2
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
5
structure (0 1)
C  -0.00000997794639 -0.00091664148112 0.45499807439812
H  0.00000069467312 0.00031189002174 1.53703126401237
Cl 0.00003188789531 1.69433732001280 -0.08420513240263
Cl 1.46635420502892 -0.84684178730039 -0.08421103795485
Cl -1.46637680965097 -0.84689178125304 -0.08420916805301
--- input ---
!HF cc-pVDZ TightSCF MBIS

* xyz 0 1
  C   -0.00000997794639     -0.00091664148112      0.45499807439812
  H    0.00000069467312      0.00031189002174      1.53703126401237
  Cl   0.00003188789531      1.69433732001280     -0.08420513240263
  Cl   1.46635420502892     -0.84684178730039     -0.08421103795485
  Cl  -1.46637680965097     -0.84689178125304     -0.08420916805301
*
```

ORCA 在输出文件末尾打印如下信息：

```orca
------------------
MBIS ANALYSIS
------------------

Convergence threshold (charges)      ...        1.000e-06
Number of iterations                 ...        46

Total integrated alpha density       ...     29.000001385
Total integrated beta density        ...     29.000001385

  ATOM     CHARGE    POPULATION     SPIN
   0 C    0.208633    5.791367    0.000000
   1 H    0.169417    0.830583    0.000000
   2 Cl  -0.126877   17.126877    0.000000
   3 Cl  -0.125586   17.125586    0.000000
   4 Cl  -0.125590   17.125590    0.000000

  TOTAL  -0.000003   58.000003    0.000000

 MBIS VALENCE-SHELL DATA:
  ATOM   POPULATION   WIDTH(A.U.)
   0 C    4.122213    0.508675
   1 H    0.830583    0.358785
   2 Cl   8.532439    0.524031
   3 Cl   8.531380    0.523959
   4 Cl   8.531381    0.523959
```

第二个块对应价层 Slater 函数，它由其布居 $N_{A,v}$ 和宽度 $\sigma_{A,v}$ 表征。

<a id="sec:spectroscopyproperties.pop.chelpg"></a>
## CHELPG 电荷（CHELPG Charges）

原子电荷也可用 Breneman 和 Wiberg 的
基于网格的静电势电荷（CHarges from ELectrostatic Potentials using a Grid-based，CHELPG）方法计算。[breneman1990](../../bibliography.md)
在该途径中，拟合原子电荷以再现分子周围规则网格上的静电势，
同时约束所有原子电荷之和等于分子的总电荷。
还可添加一个附加约束，使 CHELPG 电荷也再现分子的总偶极矩。

<a id="sec:spectroscopyproperties.pop.chelpg.basicusage"></a>
### 基本用法（Basic Usage）

在 ORCA 中，CHELPG 电荷可以 (i) 在计算中请求，
或 (ii) 通过独立工具 [`orca_chelpg`](#sec:utilities.chelpg) 计算。
走路径 (i) 需要在输入文件中加入 `!CHELPG` 简单输入关键词。

```orca
! CHELPG
```

更多设置可通过 `%chelpg` 块控制。

```orca
%chelpg
  GRID 0.3       # Spacing of the regular grid in Angstroems
  RMAX 2.8       # Maximum distance of all atoms to any gridpoint in Angstroems
  VDWRADII COSMO # VDW Radii of Atoms, COSMO default
           BW    # Breneman, Wiberg radii
  DIPOLE FALSE   # If true, then the charges also reproduce the total dipole moment
end
```

默认情况下，程序使用 COSMO VDW 半径来排除核附近的网格点，
因为这些半径对所有原子都有定义。
BW 半径与之类似，但只对很少的原子类型有定义。

电荷可能对分子在空间中的取向有一定依赖，
或在对称分子中出现一些人为的变异。
这些效应可通过增大 CHELPG 网格来最小化，
方法是设置 `%chelpg` 块中的 `GRID` 参数，
或使用 `!CHELPG(LARGE)` 简单输入关键词。

```orca
! CHELPG(LARGE)
```

若希望计算得到的 CHELPG 电荷不仅再现静电势、
还再现分子的总偶极矩，则需在 `%chelpg` 块中加入如下标签：

```orca
%chelpg
  DIPOLE TRUE  # The default is set to FALSE
end
```

特别地，该约束作用于总偶极矩的 $x$、$y$、$z$ 分量，
使它们再现通过单电子积分计算的总偶极矩的精确三个分量。

<a id="sec:spectroscopyproperties.pop.resp"></a>
## RESP 电荷（RESP Charges）

ORCA 还提供了计算所谓 RESP 电荷的功能 [baylyRESP_1993](../../bibliography.md)，
本质上是带有某种约束以避免过拟合的 CHELPG 电荷。
只需在主输入中使用 `!RESP` 即可以默认方式调用。

这些 RESP 电荷可有两种惩罚函数：二次型或双曲型（默认），如原始论文所述。
它们需要至多两个惩罚值，默认给为 $a=0.0005$ 和 $b=0.1$。

这些值可在 `%CHELPG` 块中更改：

```orca
%chelpg
  RESPWA 0.01   # for the a value
  RESPWB 0.002  # for the b value
end
```

惩罚函数可用如下方式选择：

```orca
%chelpg
  RESPPENALTY QUADRATIC # default is HYPREBOLIC
end
```

另外，如有需要，$a$ 参数和参考电荷 $q_0$ 的各个值
可通过一个特殊文件给出：

```orca
%chelpg
  RESPWFILE     "wfilename" # these will define the weights (or a parameters)
                            # for each atom
  RESPQREFFILE  "qfilename" # these might define reference charges different
                            # from zero
end
```

这两个文件的格式类似于 `.xyz` 文件，
第一行是原子数，第二行只是注释，
随后每行包含一个数字，即每个原子的权重或参考电荷。
它们不能放在同一个文件中，必须是两个不同的文件。

!!! note
      此处 RESP 文件得到的结果**不一定**与其他软件得到的相同。
      两个主要原因是：网格不同，
      且某些其他软件采用多层级方法，
      先用某个权重值起步，然后切换到不同的值，而这里不是这样。

<a id="sec:spectroscopyproperties.pop.lsa"></a>
## 局域自旋分析（Local Spin Analysis）

在化学中，习惯于用局域自旋态来思考开壳层体系的相互作用。
例如，在二聚或寡聚过渡金属簇中，
对局域上处于高自旋态的开壳层离子之间的"交换耦合"有广泛研究。
双自由基是有机化学中呈现这一现象的典型体系。
然而在量子力学中，总自旋不是一个局域性质，
而是整个体系的性质。
总自旋的平方 $S^2$ 及其在 z 轴上的投影 $S_z$
与非相对论哈密顿量对易，
因此非相对论哈密顿量的本征函数
可按好量子数 $S$ 和 $M$ 分类：

$$
{S }_{}^2\left|{ \Psi _{}^{SM} } \right\rangle = S(S + 1)\left|{ \Psi _{}^{SM} } \right\rangle
$$

$$
S_z^{}\left|{ \Psi _{}^{SM} } \right\rangle = M\left|{ \Psi _{}^{SM} } \right\rangle
$$

其中 $\left|{ \Psi _{}^{SM} } \right\rangle$ 是非相对论哈密顿量的精确本征函数，
或其保持总自旋为好量子数的近似。
总自旋本身由各个电子自旋之和给出：

$$
{S } = \sum\limits_i { {s }(i) }
$$

因此，

$$
{S }_{}^2 = \sum\nolimits_{i,j} { {s }(i){s }(j) }
$$

是体系的双电子性质。
将化学上非常有意义的局域自旋概念与严格的量子力学处理联系起来显然并非易事。
虽然有各种处理该问题的提议，
我们这里遵循 Clark 和 Davidson 的提议 [clark2001localspin](../../bibliography.md)。
下列方程已在 Orca 的 SCF 和 CASSCF 模块中实现。

Clark 和 Davidson 定义了具有如下性质的片段投影算符：

$$
P_A^{}P_B^{} = \delta _{AB}^{}P_A^{}
$$

以及：

$$
\sum\limits_A { P_A^{} }  = 1
$$

然后利用这一恒等式：

$$
{S } = \sum\limits_i { \sum\limits_A { {s }(i)P_{A(i) }^{} } }
$$

$$
{S } = \sum\limits_A { \sum\limits_i { {s }(i)P_A^{}(i) } }
$$

$$
\,\,\,\, = \sum\limits_A { {S }_A^{}(i) }
$$

他们证明局域自旋算符满足自旋算符的标准关系：

$$
{S }_A^{} = { S }_A^\dagger
$$

$$
{S }_A^{} \times{ S }_A^{} = i\hbar{ S }_A^{}
$$

于是

$$
{S }_{}^2 = \sum\limits_A { \sum\limits_B { {S }_A^{}{S }_B^{} } }
$$

但重要的是：

$$
{S }_A^{}{S }_B^{} = \sum\limits_i { \sum\limits_j { {s }(i){s }(j) } P_A^{}(i)P_B^{}(j) }
$$

$$
\,\,\,\,\,\,\,\,\,\,\,\, = { \textstyle{3 \over 4} }\delta _{AB}^{}\sum\limits_A { P_A^{}(i) }  + \sum\limits_i { \sum\limits_{j > i} { {s }(i){s }(j)\{ P_A^{}(i)P_B^{}(j) + P_A^{}(j)P_B^{}(i)\} } }
$$

用一阶和二阶密度矩阵：

$$
\gamma ({x },{x' }) = N\in t{ \Psi ({x },{x }_2^{},...,{x }_N^{})\Psi _{}^*({x' },{x }_2^{},...,{x }_N^{}) } d{x }_2^{}...d{x }_N^{}
$$

$$
\Gamma ({x }_1^{},{x' }_1^{};{x }_2^{},{x' }_2^{}) = \left({
\begin{matrix}
   N  \cr 
   2  \cr 
\end{matrix}
} \right)\in t{ \Psi ({x }_1^{},{x }_2^{},...,{x }_N^{})\Psi _{}^*({x' }_1^{},{x' }_2^{},...,{x }_N^{}) } d{x }_3^{}...d{x }_N^{}
$$

（其中 ${\textstyle{N \choose 2} }= { \textstyle{1 \over 2} }N(N - 1)$）。
则：

$$
\left\langle { {S }_A^{}{S }_B^{} } \right\rangle = { \textstyle{3 \over 4} }\delta _{AB}^{}tr(\gamma P_A^{}) + 2tr(P_A^{}(1)P_B^{}(2){s }(1){s }(2)\Gamma (1,1;2,2))
$$

用位点 'A' 上的电子数和 $S_z^A$ 的期望值表示：

$$
\left\langle { S_z^A} \right\rangle = { \textstyle{1 \over 2} }tr(\gamma _{}^{\alpha  - \beta }P_A^{})
$$

$$
\left\langle { N_{}^A} \right\rangle = tr(\gamma _{}^{\alpha  + \beta }P_A^{})
$$

用分子轨道表示：

$$
\left\langle { S_z^A} \right\rangle = { \textstyle{1 \over 2} }\sum\limits_{p,q} { \gamma _{pq}^{\alpha  - \beta }\left\langle { p|P_A^{}|q} \right\rangle}
$$

$$
\left\langle { N_{}^A} \right\rangle = \sum\limits_{p,q} { \gamma _{pq}^{\alpha  + \beta }\left\langle { p|P_A^{}|q} \right\rangle}
$$

McWeeny 和 Kutzelnigg [mcweeny1968independentparticle](../../bibliography.md) 证明，
对于 s(1)s(2) 的期望值，双体密度的相关不可约部分
可用二阶无自旋密度矩阵表示：

$$
R_0^{(0) }(1,1';2,2') =  - { \textstyle{1 \over 3} }\Gamma (1,1';2,2') - { \textstyle{2 \over 3} }\Gamma (2,1';1,2')
$$

$$
\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\, =  - { \textstyle{1 \over 3} }\sum\limits_{pqrs} { \Gamma _{rs}^{pq}p(1)q(1')r(2)s(2') }  + 2\Gamma _{rs}^{pq}p(2)q(1')r(1)s(2')
$$

$$
\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\, =  - { \textstyle{1 \over 3} }\sum\limits_{pqrs} { (\Gamma _{rs}^{pq} + 2\Gamma _{ps}^{rq})p(1)q(1')r(2)s(2') }
$$

自旋积分后归一化因子为 $3 \over 4$。
因此利用这一点：

$$
\left\langle { {S }_A^{}{S }_B^{} } \right\rangle = { \textstyle{3 \over 4} }\delta _{AB}^{}tr(\gamma P_A^{}) + { \textstyle{6 \over 4} }tr(P_A^{}(1)P_B^{}(2)R_0^{(0) }(1,1;2,2))
$$

然后执行积分：

$$
\left\langle { {S }_A^{}{S }_B^{} } \right\rangle = { \textstyle{3 \over 4} }\delta _{AB}^{}tr(\gamma P_A^{}) - \underbrace{ {\textstyle{6 \over 4} }{\textstyle{1 \over 3} }}_{{\textstyle{1 \over 2} }}\sum\limits_{pqrs} { (\Gamma _{rs}^{pq} + 2\Gamma _{ps}^{rq})P_{pq}^AP_{rs}^B}
$$

这是最终也可能是最紧凑的方程。
投影算符可以用许多不同方式定义。
最简单的是对基组作 Löwdin 正交归一化：

$$
\left|{ \mu_L^A} \right\rangle = \sum\limits_{\nu _{}^A} { \left|{ \nu _{}^A} \right\rangle S_{\mu \nu }^{ - 1/2} }
$$

其中 $L$ 表示 Löwdin 基。
这意味着分子轨道在正交基中表示为：

$$
{c }_L^{} = { S }_{}^{ + 1/2}{c }
$$

密度表示为：

$$
{P }_L^{} = { S }_{}^{ + 1/2}{PS }_{}^{ + 1/2}
$$

片段投影算符定义为：

$$
P_A^{} = \sum\limits_{\mu _L^{} \in A} { \left|{ \mu _L^{} } \right\rangle\left\langle { \mu _L^{} } \right|}
$$

Clark 和 Davidson 提出一种略为精细的投影算符，
其中首先消除片段内重叠。
这由矩阵 U 完成，对两个片段其形式为：

$$
{U } = \left( 
    \begin{matrix}{ {S }_A^{ - 1/2} } & { 0 }  \cr{ 0 } & { {S }_B^{ - 1/2} }  \cr 
 \end{matrix}
 \right)
$$

其中是属于片段 A 的基函数块。类似地：

$$
{U }_{}^{ - 1} = \left( 
    \begin{matrix}{ {S }_A^{ + 1/2} } & { 0 }  \cr{ 0 } & { {S }_B^{ + 1/2} }  \cr 
 \end{matrix}
 \right)
$$

则"前重叠"（pre-overlap）为：

$$
{\overline S } = { U }_{}^\dagger{ SU }
$$

它在片段内块中包含单位矩阵，其他地方为非零元素。
该重叠矩阵最后被正交归一化，以获得全局正交的 Löwdin 基。
我们最终用如下变换变换 MO 系数：

$$
{c }_L^{} = { S }_{}^{ + 1/2}{U }_{}^{ - 1}{c }
$$

对于投影算符，作用在两个 MO i 和 j 上给出：

$$
\left\langle { i|P_A^{}|j} \right\rangle = \sum\limits_{\mu _L^{} \in A} { \sum\limits_{\kappa _L^B\tau _L^C} { \left\langle { \kappa _L^B|\mu _L^A} \right\rangle\left\langle { \mu _L^A|\tau _L^C} \right\rangle c_{\kappa i}^Lc_{\tau j}^L} }
$$

$$
\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\, = \sum\limits_{\mu _L^{} \in A} { \sum\limits_{\kappa _L^B\tau _L^C} { \delta _{AB}^{}\delta _{AC}^{}\delta _{\kappa \mu }^{}\delta _{\tau \mu }^{}c_{\kappa i}^Lc_{\tau j}^L} }
$$

$$
\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\, = \sum\limits_{\mu _L^{} \in A} { c_{\mu i}^Lc_{\mu j}^L}
$$

Herrmann 等人 [herrmann2005localspin](../../bibliography.md) 给出单个自旋非限制行列式
期望值的正确表达式

$$
\begin{aligned}
  & \left\langle { {S }_A^{}{S }_B^{} } \right\rangle = { \textstyle{3 \over 4} }\delta _{AB}^{}\left\{{ \sum\limits_i { P_{ii}^A}  + \sum\limits_{\bar i} { P_{\bar i\bar i}^A} } \right\} \cr 
  & \,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\, + { \textstyle{1 \over 4} }\left\{{ \sum\limits_{ij} { P_{ii}^AP_{jj}^B}  + \sum\limits_{\bar i\bar j} { P_{\bar i\bar i}^AP_{\bar j\bar j}^B}  - \sum\limits_{ij} { P_{ij}^AP_{ij}^B}  - \sum\limits_{\bar i\bar j} { P_{\bar i\bar j}^AP_{\bar i\bar j}^B}  - \sum\limits_{\bar ij} { P_{\bar i\bar i}^AP_{jj}^B}  - \sum\limits_{i\bar j} { P_{ii}^AP_{\bar j\bar j}^B} } \right\} \cr 
  & \,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\, - \sum\limits_{i\bar j} { P_{i\bar j}^AP_{i\bar j}^B}  \cr\end{aligned}
$$

Orca 的实现采用该式。

局域自旋实现的使用非常简单。
只需将分子划分为[片段](#sec:essentialelements.fragmentation)。
其余自动完成。例如，考虑解离极限处的两个氮原子。
虽然总自旋态是 S=0，但两个氮原子局域上处于高自旋态（S=3/2）。
考虑如下测试作业：

```mol
title: structure 3
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
2
structure (0 1)
N             0            0            0
N             0            0         1094
--- input ---
! HF def2-SVP UHF TightSCF PModel 

%scf brokensym 3,3 end 

* xyz 0 1
N(1) 0 0 0
N(2) 0 0 1094
*
```

输出：

```orca
-------------------
LOCAL SPIN ANALYSIS (Loewdin* projector)
-------------------

(1) A.E. Clark; E.R. Davison J. Chem. Phys. (2001), 115(16), pp 7382-7392 
(2)  C. Herrmann, M. Reiher, B.A. Hess J. Chem. Phys. (2005) 122, art 034102-1

Number of fragments       = 2
Number of basis functions = 28
Number of atoms           = 2

   ... Fragment AO indices were mapped
   ... intra-fragment orthogonalization completed
   ... Global Loewdin orthogonalizer constructed
   ... Loewdin orthogonalized occupied orbitals constructed

 <SA*SB>        1            2     
----------------------------------
   1    :     3.7568  
   2    :    -2.2500       3.7568  

               <SzA>      Seff(A)
        --------------------------
   1    :     1.5000      1.5017
   2    :    -1.5000      1.5017
```

与预期完全一致。
同样的工作可在 CASSCF 水平完成：

```mol
title: structure 4
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
2
structure (0 1)
N             0            0            0
N             0            0         1094
--- input ---
! HF def2-SVP UHF TightSCF PModel

%casscf nel 6 norb 6 nroots 1 end 

* xyz 0 1
N(1) 0 0 0
N(2) 0 0 1094
*
```

结果为：

```orca
<SA*SB>        1            2     
----------------------------------
   1    :     3.7500  
   2    :    -3.7500       3.7500  

               <SzA>*      Seff(A)
        --------------------------
   1    :       n.a.      1.5000
   2    :       n.a.      1.5000

* = for a singlet state all <SzA> values are zero by definition
```

干净地证实了预期。
此外，若 nroots > 1，打印内容将包含所有根的态特定分析。

作为一个不那么平凡的例子，考虑一个典型的 Fe(III) 反铁磁耦合过渡金属二聚体。
合适的输入可以是：

```mol
title: structure 5
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
12
structure (-2 1)
Fe     -1.93818      0.53739     -0.00010
Fe      1.06735      0.47031      0.00029
S      -0.38935      2.59862     -0.00983
S      -0.48170     -1.59050      0.01091
S       2.68798      0.43924      1.99710
S       2.68692      0.42704     -1.99712
S      -3.55594      0.56407     -1.99889
S      -3.55850      0.58107      1.99646
H       3.91984      0.39462      1.47608
H       3.91940      0.39536     -1.47662
H      -4.78410      0.69179     -1.48280
H      -4.78991      0.49249      1.47983
--- input ---
! PBE def2-SV(P) TightSCF KDIIS SOSCF PModel

%scf
  brokensym 5,5
end

* xyz -2 1
Fe(1)	-1.93818	 0.53739	-0.00010
Fe(2)	 1.06735	 0.47031	 0.00029
S(3)	-0.38935	 2.59862	-0.00983
S(3)	-0.48170	-1.59050	 0.01091
S(1)	 2.68798	 0.43924	 1.99710
S(1)	 2.68692	 0.42704	-1.99712
S(2)	-3.55594	 0.56407	-1.99889
S(2)	-3.55850	 0.58107	 1.99646
H(1)	 3.91984	 0.39462	 1.47608
H(1)	 3.91940	 0.39536	-1.47662
H(2)	-4.78410	 0.69179	-1.48280
H(2)	-4.78991	 0.49249	 1.47983
*
```

其中两个桥硫分别指派给每个位点。

```orca
 <SA*SB>        1            2            3
-----------------------------------------------
   1    :     7.3346
   2    :    -4.5300       7.3349
   3    :    -0.7229      -0.7230       1.9403

               <SzA>      Seff(A)
        --------------------------
   1    :     1.7561      2.2540
   2    :    -1.7562      2.2541
   3    :     0.0001      0.9800
```

该计算的输出显示了预期结果，局域位点自旋接近其理想值 2.5，
即高自旋 Fe(III) 离子应有的值。

<a id="sec:spectroscopyproperties.pop.UNO"></a>
## UNO 的布居分析（Population Analysis of UNOs）

[UHF 自然轨道](#sec:modelchemistries.hftype.uhfno)的布居分析
可通过 `%output` 块中相应的打印选项请求：

```orca
%output
  Print[ P_UNO_OccNum     ] = 1;        # Occupation numbers
  Print[ P_UNO_AtPopMO_M  ] = 0;        # Mulliken atom pop. per UNO
  Print[ P_UNO_OrbPopMO_M] = 0;         # Mulliken orbital pop. per UNO
  Print[ P_UNO_ReducedOrbPopMO_M] = 0;  # Mulliken reduced orbital pop. per UNO
  Print[ P_UNO_AtPopMO_L  ] = 0;        # Loewdin atom pop. per UNO
  Print[ P_UNO_OrbPopMO_L] = 0;         # Loewdin orbital pop. per UNO
  Print[ P_UNO_ReducedOrbPopMO_L] = 0;  # Loewdin reduced orbital pop. per UNO
end
```

## 关键词（Keywords）

布居分析语境下有用的关键词汇编见 [tab:spectroscopyproperties.pop.keywords.simple](#tab:spectroscopyproperties.pop.keywords.simple)、
[tab:spectroscopyproperties.pop.keywords.block.output](#tab:spectroscopyproperties.pop.keywords.block.output)、[tab:spectroscopyproperties.pop.keywords.block.method](#tab:spectroscopyproperties.pop.keywords.block.method) 和 [tab:spectroscopyproperties.pop.keywords.block.chelpg](#tab:spectroscopyproperties.pop.keywords.block.chelpg)。

<a id="tab:spectroscopyproperties.pop.keywords.simple"></a>
!!! note "布居分析的简单输入关键词。"
    | 关键词                          | 说明                                                                                                                       |
    |:--------------------------------|:----------------------------------------------------------------------------------                                                |
    | `AllPop`                        | 启用所有布居分析                                                                                                 |
    | `NoPop`                         | 关闭所有布居分析                                                                                               |
    | `ReducedPop`                    | 打印每个 MO 的约化轨道布居                                                                                         |
    | `NoReducedPop`                  | 关闭约化轨道布居的打印                                                                               |
    | `Mulliken`                      | 启用 [Mulliken](#sec:spectroscopyproperties.pop.mulliken) 布居分析                                                 |
    | `NoMulliken`                    | 关闭 Mulliken 布居分析                                                                                          |
    | `Loewdin`                       | 启用 [Löwdin](#sec:spectroscopyproperties.pop.loewdin) 布居分析                                                    |
    | `NoLoewdin`                     | 关闭 Löwdin 布居分析                                                                                            |
    | `Mayer`                         | 启用 [Mayer](#sec:spectroscopyproperties.pop.mayer) 布居分析                                                       |
    | `NoMayer`                       | 关闭 Mayer 布居分析                                                                                             |
    | `NPA`                           | 启用 [NPA](#sec:spectroscopyproperties.pop.natural)。需要 NBO 程序                                                     |
    | `NBO`                           | 启用 [NPA](#sec:spectroscopyproperties.pop.natural) 和 [NBO](#sec:spectroscopyproperties.nbo) 分析。需要 NBO 程序  |
    | `NoNBO`                         | 关闭 NBO                                                                                                                   |
    | `NoNPA`                         | 关闭 NPA 和 NBO                                                                                                           |
    | `MBIS`                          | 启用 [MBIS](#sec:spectroscopyproperties.pop.mbis) 布居分析                                                         |
    | `CHELPG`                        | 请求计算 [CHELPG](#sec:spectroscopyproperties.pop.chelpg) 电荷                                                   |
    | `CHELPG(LARGE)`                 | 请求用大网格计算 [CHELPG](#sec:spectroscopyproperties.pop.chelpg) 电荷                                   |

<a id="tab:spectroscopyproperties.pop.keywords.block.output"></a>
!!! note "布居分析的 `%output` 块输入关键词和选项。"
    | 关键词                          | 选项                      | 说明                                            |
    |:--------------------------------|:--------------------------|:-------------------------------------------------------|
    | `Print[ <option> ]`             | `P_Mayer`                 | 打印 Mayer 布居分析（默认 = 开）         |
    |                                 | `P_NatPop`                | 打印自然布居分析（默认 = 关）      |
    |                                 | `P_NPA`                   | 打印自然布居分析（默认 = 关）      |
    |                                 | `P_Hirshfeld`             | 打印 Hirshfeld 布居分析（默认 = 关）    |
    |                                 | `P_MBIS`                  | 打印 MBIS 布居分析（默认 = 关）         |
    |                                 | `P_Mulliken`              | 打印 Mulliken 布居分析（默认 = 开）      |
    |                                 | `P_AtCharges_M`           | 打印 Mulliken 原子电荷                          |
    |                                 | `P_OrbCharges_M`          | 打印 Mulliken 轨道电荷                         |
    |                                 | `P_FragCharges_M`         | 打印 Mulliken 片段电荷                        |
    |                                 | `P_FragBondOrder_M`       | 打印 Mulliken 片段键级                    |
    |                                 | `P_BondOrder_M`           | 打印 Mulliken 键级                             |
    |                                 | `P_ReducedOrbPop_M`       | 打印 Mulliken 约化轨道电荷                 |
    |                                 | `P_FragPopMO_M`           | 打印每个 MO 的 Mulliken 片段布居         |
    |                                 | `P_FragOvlMO_M`           | 打印每对片段的 Mulliken 重叠布居   |
    |                                 | `P_AtPopMO_M`             | 打印每个 MO 中的 Mulliken 原子电荷               |
    |                                 | `P_OrbPopMO_M`            | 打印每个 MO 的 Mulliken 轨道布居          |
    |                                 | `P_ReducedOrbPopMO_M`     | 打印每个 MO 的 Mulliken 约化轨道布居  |
    |                                 | `P_Loewdin`               | 打印 Loewdin 布居分析（默认 = 开）       |
    |                                 | `P_AtCharges_L`           | 打印 Loewdin 原子电荷                           |
    |                                 | `P_OrbCharges_L`          | 打印 Loewdin 轨道电荷                          |
    |                                 | `P_FragCharges_L`         | 打印 Loewdin 片段电荷                         |
    |                                 | `P_FragBondOrder_L`       | 打印 Loewdin 片段键级                     |
    |                                 | `P_BondOrder_L`           | 打印 Loewdin 键级                              |
    |                                 | `P_ReducedOrbPop_L`       | 打印 Loewdin 约化轨道电荷                  |
    |                                 | `P_FragPopMO_L`           | 打印每个 MO 的 Loewdin 片段布居          |
    |                                 | `P_FragOvlMO_L`           | 打印每对片段的 Loewdin 重叠布居    |
    |                                 | `P_AtPopMO_L`             | 打印每个 MO 中的 Loewdin 原子电荷                |
    |                                 | `P_OrbPopMO_L`            | 打印每个 MO 的 Loewdin 轨道布居           |
    |                                 | `P_ReducedOrbPopMO_L`     | 打印每个 MO 的 Loewdin 约化轨道布居   |
    |                                 | `P_Fragments`             | 打印片段信息                             |
    |                                 | `P_GUESSPOP`              | 打印初始猜测布居                        |
    |                                 | `P_UNO_FragPopMO_M`       | 打印每个 UNO 的 Mulliken 片段布居             |
    |                                 | `P_UNO_OrbPopMO_M`        | 打印每个 UNO 的 Mulliken 轨道布居                    |
    |                                 | `P_UNO_AtPopMO_M`         | 打印每个 UNO 的 Mulliken 原子电荷                  |
    |                                 | `P_UNO_ReducedOrbPopMO_M` | 打印每个 UNO 的 Mulliken 约化轨道布居            |
    |                                 | `P_UNO_FragPopMO_L`       | 打印每个 UNO 的 Loewdin 片段布居              |
    |                                 | `P_UNO_OrbPopMO_L`        | 打印每个 UNO 的 Loewdin 轨道布居                     |
    |                                 | `P_UNO_AtPopMO_L`         | 打印每个 UNO 的 Loewdin 原子电荷                   |
    |                                 | `P_UNO_ReducedOrbPopMO_L` | 打印每个 UNO 的 Loewdin 约化轨道布居             |
    |                                 | `P_UNO_OccNum`            | 打印每个 UNO 的占据数                       |

<a id="tab:spectroscopyproperties.pop.keywords.block.method"></a>
!!! note "布居分析的 `%method` 块输入关键词和选项。"

    | 关键词 | 选项 | 说明 |
    | --- | --- | --- |
    | `LOEWDIN_BONDORDERTHRESH` | `<real>` | 设置 Löwdin 键级的打印阈值（默认 = 0.05） |
    | `MAYER_BONDORDERTHRESH` | `<real>` | 设置 Mayer 键级的打印阈值（默认 = 0.1） |
    | `MBIS_CHARGETHRESH` | `<real>` | 设置 MBIS 电荷的收敛阈值（默认 = $10^{-6}$） |
    | `MBIS_LARGEPRINT` | `true`/`false` | 启用 [MBIS 相关量](#sec:spectroscopyproperties.pop.mbis.quantities) 的打印（默认 = false） |
    | `MBIS_ORIGIN_MULT` | `CenterOfCoords` | 将 MBIS 性质的原点设为坐标系中心 (0,0,0) |
    | — | `CenterOfMass` | 将 MBIS 性质的原点设为质心 |
    | — | `CenterOfNucCharge` | 将 MBIS 性质的原点设为核电荷中心 |
    | — | `CenterXYZ` | 将 MBIS 性质的原点设为任意位置，用 `MBIS_ORIMULT_XYZ` 设置坐标 |
    | — | `CenterOfEachAtom` | 将 MBIS 性质的原点设为每个原子的中心（默认） |
    | `MBIS_ORIMULT_XYZ` | `<x,y,z>` | 设置坐标，否则为 0,0,0（单位：埃） |

<a id="tab:spectroscopyproperties.pop.keywords.block.chelpg"></a>
!!! note "CHELPG 电荷的 `%chelpg` 块输入关键词和选项。"
    | 关键词                          | 选项                    | 说明                                                                     |
    |:--------------------------------|:--------------------------|:--------------------------------------------------------------------------------|
    | `GRID`                          | `<real>`                  | 规则网格的间距，单位 Å（默认 = 0.3）                                |
    | `RMAX`                          | `<real>`                  | 所有原子到任意网格点的最大距离，单位 Å（默认 = 2.8）             |
    | `VDWRADII`                      | `COSMO`                   | 启用 COSMO 原子 VdW 半径（默认）                           |
    |                                 | `BW`                      | 启用 Breneman、Wiberg 半径                                       |
    | `DIPOLE`                        | `false`/`true`            | 若为 true，电荷也再现总偶极矩（默认 = `false`) |

