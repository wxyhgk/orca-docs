```{index} MR-EOM-CC
```

(sec:modelchemistries.mreom)=
# 多参考运动方程耦合簇（Multireference Equation of Motion Coupled-Cluster，MR-EOM-CC）

多参考运动方程耦合簇（Multireference Equation of Motion Coupled-Cluster，MR-EOM-CC）
方法{cite}`datta2011pICMRCC,datta2012mreom,demel2013mreom,nooijen2014mreom,huntington2015mreom_orb_select,huntington2015mreom_bench`
已在 ORCA 中实现。MR-EOM-CC 方法的优势在于能够从单一的态平均 CASSCF 解出发计算许多激发态：
只需解一组振幅（amplitude），最终变换后的哈密顿量只需在一个小的激发态集合上、
通过一个非收缩 MRCI 问题进行对角化。因此，一次给定的 MR-EOM-CC 计算包含三个步骤，
由 ORCA 中三个独立模块完成：

1.  态平均 CASSCF 计算（CASSCF 模块），

2.  求解振幅方程并计算相似变换哈密顿量的各矩阵元（MDCI 模块），

3.  对最终相似变换哈密顿量进行非收缩 MRCI 对角化（MRCI 模块）。

当前实现支持 MR-EOM-T|T$^{\dagger}$-h-v、MR-EOM-T|T$^{\dagger}$|SXD-h-v 与
MR-EOM-T|T$^{\dagger}$|SXD|U-h-v 计算。关于这些方法及可用输入参数的更详细描述见
{numref}`sec:modelchemistries.mreom.details` 一节。我们还指出，这些方法的理论细节
可参见文献 {cite}`huntington2015mreom_bench`。在 {numref}`sec:modelchemistries.mreom.calc.sacas`
一节，我们将更详细地讨论态平均 CAS 的选择策略以及设置 MR-EOM-CC 计算的其他步骤。
此外，我们还将讨论如何在 MR-EOM-CC 计算中纳入自旋轨道耦合效应、
一种帮助克服 $T$ 振幅迭代收敛困难的投影方案、
一种在计算激发能时缩减非活性核心与虚拟子空间规模的轨道选择方案，
以及一种在 MR-EOM-CC 中获得近似尺寸一致结果的策略。
本节的目的只是提供一个简单示例，说明 ORCA 中 MR-EOM-CC 实现的最基本用法。

(sec:modelchemistries.mreom.calc)=
## 一个简单的 MR-EOM-CC 计算（A Simple MR-EOM-CC Calculation）

让我们考虑甲醛（formaldehyde）的 MR-EOM-T|T$^{\dagger}$|SXD|U-h-v 计算。
MR-EOM-T|T$^{\dagger}$|SXD|U-h-v 计算通过 `MR-EOM` 关键词指定，
同时要指定态平均 CASSCF 计算（即 CASSCF(nel, norb) 计算，并给出参考态势平均中
所包含的各多重度的根数），以及最终 MRCI 对角化中每个多重度块所求的根数。
我们指出 CASSCF 模块在 {numref}`sec:modelchemistries.casscf` 一节描述，
MRCI 模块的说明见 {numref}`sec:modelchemistries.mrci` 一节。
这里我们进行态平均 CAS(6,4) 计算，由 3 个单重态和 3 个三重态组成，
并请求最终 MRCI 对角化中 6 个单重态根和 6 个三重态根
（即 MR-EOM-T|T$^{\dagger}$|SXD|U-h-v 计算中要计算的根）：

```{literalinclude} ../../orca_working_input/C05S10_195.inp
:language: orca
```

也可以通过将上述输入第一行中的 `MR-EOM` 关键词分别替换为 `MR-EOM-T|Td` 或
`MR-EOM-T|Td|SXD`，来进行 MR-EOM-T|T$^{\dagger}$-h-v 或
MR-EOM-T|T$^{\dagger}$|SXD-h-v 计算。也就是说，将上述输入第一行替换为

```orca
!MR-EOM-T|Td def2-TZVP VeryTightSCF
```

即运行 MR-EOM-T|T$^{\dagger}$-h-v 计算，而

```orca
!MR-EOM-T|Td|SXD def2-TZVP VeryTightSCF
```

运行 MR-EOM-T|T$^{\dagger}$|SXD-h-v 计算。

最终 MRCI 对角化集合在 MR-EOM-T|T$^{\dagger}$-h-v 计算中包括 2h1p、1h1p、2h、1h
与 1p 激发，在 MR-EOM-T|T$^{\dagger}$|SXD-h-v 计算中包括 2h、1p 与 1h 激发，
在 MR-EOM-T|T$^{\dagger}$|SXD|U-h-v 计算中包括 1h 与 1p 激发。
注意在 `%mdci` 块中，我们将振幅残差方程的收敛容差（`STol`）设为 $10^{-7}$，
因为使用 `TightSCF`、`VeryTightSCF` 等关键词会覆盖该默认值。
始终检查最大的 $T$、$S$（这里我们用 $S$ 表示 $S$、$X$ 与 $D$ 振幅的整个集合）
和 $U$ 振幅的取值非常重要。如果存在很大的振幅（绝对值 $> 0.15$），
对计算结果就应持怀疑态度。对于上述计算，我们得到：

```orca
--------------------
LARGEST T AMPLITUDES
--------------------
   8-> 13   8-> 13       0.060331
   4-> 17   4-> 17       0.029905
   8->  9   8->  9       0.028160
   8-> 16   8-> 16       0.027266
   6-> 20   6-> 20       0.025885
   8-> 21   8-> 21       0.025308
   4-> 16   4-> 16       0.024803
   8-> 12   8-> 12       0.023915
   5-> 18   5-> 18       0.023553
   8-> 23   8-> 23       0.023384
   3-> 16   3-> 16       0.023182
   7-> 19   7-> 19       0.023043
   8-> 13   4-> 11       0.022010
   3-> 19   3-> 19       0.021987
   8-> 16   8->  9       0.021230
   8->  9   8-> 16       0.021230
```

这是 $T$ 振幅，

```orca
--------------------
LARGEST S AMPLITUDES
--------------------
   4->  8   8-> 11       0.074048
   3->  8   8->  9       0.064886
   4->  5   5-> 11       0.045479
   3->  8   8-> 16       0.042657
   4->  7   7-> 11       0.042598
   4->  5   5-> 17       0.042076
   4->  5   8-> 11       0.039958
   4->  8   8-> 17       0.037532
   3->  5   8->  9       0.035907
   4->  7   7-> 17       0.035767
   2->  6   6-> 19       0.034148
   3->  5   5-> 10       0.033339
   2->  6   6-> 10       0.032691
   4->  6   6-> 11       0.032181
   8->  8   3-> 16       0.031775
   2->  7   7-> 22       0.031238
```

这是 $S$ 振幅，还有

```orca
--------------------
LARGEST U AMPLITUDES
--------------------
   3->  8   3->  8       0.026128
   3->  8   3->  5       0.007683
   2->  8   2->  8       0.006182
   3->  8   2->  5       0.006154
   2->  8   3->  5       0.004954
   3->  5   3->  5       0.004677
   4->  8   4->  8       0.003989
   3->  8   2->  8       0.002040
   2->  8   3->  8       0.002040
   2->  8   2->  5       0.001818
   4->  8   4->  5       0.001173
   2->  5   2->  5       0.001107
   4->  5   4->  5       0.000714
   3->  7   3->  7       0.000607
   3->  6   3->  6       0.000521
   2->  5   3->  5       0.000365
```

这是 $U$ 振幅。由此可见本次计算没有异常大的振幅。
**我们指出，$\boldsymbol{T}$ 振幅迭代可能出现收敛问题，在这种情况下应将如下标志：**

```orca
DoSingularPT true
```

**加入到 `%mdci` 块中。**收敛问题是由于存在近奇异（nearly singular）的 $T_2$ 振幅，
将 `DoSingularPT` 标志设为 `true` 会启用一个流程，在（每次迭代中）投影掉有问题的
振幅并以合适的微扰振幅替换它们。更多信息见
{numref}`sec:modelchemistries.mreom.singularpt` 一节的示例。

在 MDCI 模块中计算完振幅与相似变换哈密顿量的各矩阵元后，计算进入 MRCI 模块。
关于 MRCI 计算输出的完整逐步说明，我们请读者参阅
{numref}`sec:modelchemistries.mrci.example` 一节所述的示例。
让我们先关注单重态（`CI-BLOCK 1`）的结果。在 Davidson 对角化（默认）或 DIIS
过程收敛后，打印出如下单重态的 MRCI 计算结果：

```orca
----------
CI-RESULTS
----------

The threshold for printing is  0.30 percent
The weights of configurations will be printed. The weights are summed over
all CSFs that belong to a given configuration before printing

STATE   0:  Energy=   -114.321368425 Eh RefWeight=  0.9781  0.00 eV      0.0 cm**-1
      0.0137  : h---h---[0222]
      0.0756  : h---h---[1221]
      0.8879  : h---h---[2220]
STATE   1:  Energy=   -114.176866027 Eh RefWeight=  0.9765  3.93 eV  31714.6 cm**-1
      0.0039  : h---h---[1122]
      0.9726  : h---h---[2121]
      0.0071  : h---h  4[1222]
      0.0085  : h---h  4[2221]
STATE   2:  Energy=   -113.988050555 Eh RefWeight=  0.9774  9.07 eV  73154.8 cm**-1
      0.0044  : h---h---[1212]
      0.9730  : h---h---[2211]
      0.0063  : h---h  3[1222]
      0.0041  : h---h  3[2221]
STATE   3:  Energy=   -113.963862283 Eh RefWeight=  0.8810  9.73 eV  78463.5 cm**-1
      0.7459  : h---h---[1221]
      0.0807  : h---h---[2022]
      0.0533  : h---h---[2220]
      0.0228  : h---h  4[2122]
      0.0034  : h---h---[1220]p13
      0.0072  : h---h---[1220]p18
      0.0236  : h---h---[2120]p11
      0.0148  : h---h---[2120]p14
      0.0069  : h---h---[2120]p17
      0.0056  : h---h---[2120]p20
      0.0098  : h---h---[2210]p19
STATE   4:  Energy=   -113.931144468 Eh RefWeight=  0.0003 10.62 eV  85644.3 cm**-1
      0.0045  : h---h---[0122]p9
      0.0089  : h---h---[1121]p9
      0.9333  : h---h---[2120]p9
      0.0243  : h---h---[2120]p10
      0.0080  : h---h---[2120]p12
      0.0113  : h---h---[2120]p16
STATE   5:  Energy=   -113.929056780 Eh RefWeight=  0.6857 10.68 eV  86102.5 cm**-1
      0.0061  : h---h---[0222]
      0.0918  : h---h---[1221]
      0.5784  : h---h---[2022]
      0.0048  : h---h---[2202]
      0.0047  : h---h---[2220]
      0.2905  : h---h  4[2122]
      0.0045  : h---h---[2021]p13
```

对每个态，给出以 $E_\text{h}$ 为单位的总能量；给出该态中参考组态的权重
（`RefWeight`），并以 eV 和 cm$^{-1}$ 给出与最低态的能量差。
同时在每种情形下还给出对该态贡献最强的组态的权重与描述。
关于描述各组态所用记号的讨论见 {numref}`sec:modelchemistries.mrci.example` 一节。
为避免混淆，我们指出在有关 MR-EOM 方法的文献中
{cite}`datta2012mreom,demel2013mreom,nooijen2014mreom,huntington2015mreom_orb_select,huntington2015mreom_bench,liu2015mreom_bench,liu2015mreom_bench_SOC`，
"%active" 一词用来表示参考权重乘以 100%。一般而言，`RefWeight ` 应 $> 0.9$，
以使各态由参考空间组态主导。前三个态满足该判据，第四个态的参考权重也足够接近 $0.9$。
**然而，两个较高激发态（尤其是态 4）的参考权重太小，应舍弃这些态，
因为所得能量将是不准确的（即来自参考空间之外组态的显著贡献的态无法被准确处理）**。

对于三重态（`CI-BLOCK 2`），我们得到如下结果：

```orca
----------
CI-RESULTS
----------

The threshold for printing is  0.30 percent
The weights of configurations will be printed. The weights are summed over
all CSFs that belong to a given configuration before printing

STATE   0:  Energy=   -114.190840989 Eh RefWeight=  0.9693  0.00 eV      0.0 cm**-1
      0.9691  : h---h---[2121]
      0.0079  : h---h  4[1222]
      0.0115  : h---h  4[2221]
STATE   1:  Energy=   -114.106733017 Eh RefWeight=  0.9941  2.29 eV  18459.6 cm**-1
      0.9941  : h---h---[1221]
STATE   2:  Energy=   -114.015150051 Eh RefWeight=  0.9787  4.78 eV  38559.7 cm**-1
      0.9786  : h---h---[2211]
      0.0050  : h---h  3[1222]
STATE   3:  Energy=   -113.939299674 Eh RefWeight=  0.0006  6.84 eV  55206.9 cm**-1
      0.0044  : h---h---[0122]p9
      0.0084  : h---h---[1121]p9
      0.9419  : h---h---[2120]p9
      0.0131  : h---h---[2120]p10
      0.0043  : h---h---[2120]p12
      0.0173  : h---h---[2120]p16
STATE   4:  Energy=   -113.925571130 Eh RefWeight=  0.4017  7.22 eV  58220.0 cm**-1
      0.3863  : h---h---[1122]
      0.0154  : h---h---[2121]
      0.1722  : h---h  4[1222]
      0.4098  : h---h  4[2221]
      0.0045  : h---h---[2120]p13
STATE   5:  Energy=   -113.910479339 Eh RefWeight=  0.0009  7.63 eV  61532.3 cm**-1
      0.0088  : h---h---[0122]p10
      0.0030  : h---h---[1121]p10
      0.0120  : h---h---[2120]p9
      0.9408  : h---h---[2120]p10
      0.0106  : h---h---[2120]p16
      0.0112  : h---h---[2120]p19
```

这里我们看到前三个态的参考权重 $> 0.9$，而后三个态的参考权重远低于该阈值。
因此后三个态应从任何有意义的分析中舍弃。

在打印完最后一个 CI 块的 CI 结果后，各态按能量递增排序，并打印垂直跃迁能
（vertical transition energy）：

```orca
-------------------
TRANSITION ENERGIES
-------------------

The lowest energy is   -114.321368425 Eh

State Mult Irrep Root Block    mEh          eV      1/cm
  0    1    -1    0    0      0.000      0.000       0.0
  1    3    -1    0    1    130.527      3.552   28647.5
  2    1    -1    1    0    144.502      3.932   31714.6
  3    3    -1    1    1    214.635      5.841   47107.0
  4    3    -1    2    1    306.218      8.333   67207.2
  5    1    -1    2    0    333.318      9.070   73154.8
  6    1    -1    3    0    357.506      9.728   78463.5
  7    3    -1    3    1    382.069     10.397   83854.4
  8    1    -1    4    0    390.224     10.619   85644.3
  9    1    -1    5    0    392.312     10.675   86102.5
 10    3    -1    4    1    395.797     10.770   86867.5
 11    3    -1    5    1    410.889     11.181   90179.7
```

此外，在生成（近似）密度之后，打印吸收谱（absorption spectrum）与 CD 谱
（circular dichroism spectrum）：

```orca
==========================================
MR-EOM-CC  Non Relativistic Properties
==========================================

----------------------------------------------------------------------------------------------------
                     ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS    
----------------------------------------------------------------------------------------------------
     Transition      Energy     Energy  Wavelength fosc(D2)      D2        DX        DY        DZ   
                      (eV)      (cm-1)    (nm)                 (au**2)    (au)      (au)      (au)  
----------------------------------------------------------------------------------------------------
  0-1A  ->  1-1A    3.932110   31714.6   315.3   0.000000000   0.00000  -0.00000  -0.00000   0.00000
  0-1A  ->  2-1A    9.070040   73154.8   136.7   0.002137450   0.00962   0.09808  -0.00000  -0.00000
  0-1A  ->  3-1A    9.728237   78463.5   127.4   0.157495738   0.66081  -0.00000   0.00000  -0.81290
  0-1A  ->  4-1A   10.618534   85644.3   116.8   0.025353906   0.09746  -0.00000  -0.31218  -0.00000
  0-1A  ->  5-1A   10.675343   86102.5   116.1   0.024673667   0.09434  -0.00000  -0.00000   0.30715

------------------------------------------------------------------------------------------
                     CD SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS    
------------------------------------------------------------------------------------------
     Transition      Energy     Energy  Wavelength    R        MX        MY        MZ   
                      (eV)      (cm-1)    (nm)   (1e40*cgs)   (au)      (au)      (au)  
------------------------------------------------------------------------------------------
  0-1A  ->  1-1A    3.932110   31714.6   315.3   -0.00000   0.00000   0.00000   0.56273
  0-1A  ->  2-1A    9.070040   73154.8   136.7   -0.00000   0.00000  -0.74486   0.00000
  0-1A  ->  3-1A    9.728237   78463.5   127.4   -0.00000  -0.00000  -0.00000  -0.00000
  0-1A  ->  4-1A   10.618534   85644.3   116.8    0.00000   0.35898   0.00000  -0.00000
  0-1A  ->  5-1A   10.675343   86102.5   116.1    0.00000   0.00000  -0.00000  -0.00000
```

:::{Warning}

-   必须指出，跃迁矩（transition moment）与振子强度（oscillator strength）
    （以及态偶极矩）是由 MRCI 模块盲目计算的，目前尚未在这些量的求值中
    纳入各种相似变换的效应。因此这些量只是近似的，只能用作判断哪些态是
    偶极允许或禁阻的定性辅助。此外，由于所计算的密度是近似的，
    打印在吸收谱与 CD 谱之前的布居分析（population analysis）结果也是近似的。

-   尽管 CASSCF 与 MRCI 模块都能在一定程度上利用空间点群对称性，
    MR-EOM-CC 实现目前仅限于 $C_1$ 对称性下的计算。
:::

(sec:modelchemistries.mreom.capability)=
## 功能（Capabilities）

MR-EOM-CC 方法可用于从单一的态平均 CASSCF 解出发，为闭壳层与开壳层体系
计算所需数目的态。目前该方法仅限于串行计算以及较小活性空间中的较小体系。
应当意识到，在最具成本效益的 MR-EOM-T|T$^{\dagger}$|SXD|U-h-v 方法
（即最小的对角化集合）中，MRCI 对角化是在 CAS 之外所有 1h 与 1p 激发组态上进行的，
这必然限制了可用初始 CAS 的大小。我们还实现了一种轨道选择方案，
可用于在计算激发能时缩减非活性核心与虚拟子空间的规模，
从而将该方法的适用性扩展到更大的体系。当前实现还可与 MRCI 模块的
自旋轨道耦合子模块（{ref}`sec:modelchemistries.mrci.soc`）配合使用，
在 MR-EOM-CC 计算中以一阶近似计算自旋轨道耦合效应。
当前实现的这些及其他特性将在 {ref}`sec:modelchemistries.mreom.details` 中讨论。

(sec:modelchemistries.mreom.perturbative)=
## 微扰型 MR-EOM-CCPT（Perturbative MR-EOM-CCPT）

MR-EOM-CC 方法家族现在还具有一种几乎完全微扰的方法，称为 MR-EOM-T{cite}`Lechner2021`。
该方法保留了母体 MR-EOM-CC 方法的特性，同时对 $\hat T$ 与 $\hat S,\hat X,\hat D$
振幅采用非迭代的微扰估计。与迭代式 MR-EOM-CC 相比，这会略微降低精度，但缩短了运行时间。
此外，由于 $\hat T$ 与 $\hat S,\hat X,\hat D$ 振幅近奇异而引起的收敛问题不再出现。

该方法可通过在 `%mdci` 块中加入关键词 `DoMREOM_MRPT True` 来调用。

(sec:modelchemistries.mreom.details)=
## 多参考运动方程耦合簇（MR-EOM-CC）理论细节（Details on the Multireference Equation of Motion Coupled-Cluster (MR-EOM-CC ) Theory）

与单参考 EOM-CC 和 STEOM-CC 类似（见 {numref}`sec:spectroscopyproperties.eom` 与
{numref}`sec:spectroscopyproperties.steom` 两节），多参考运动方程耦合簇
（MR-EOM-CC）理论{cite}`datta2011pICMRCC,datta2012mreom,demel2013mreom,nooijen2014mreom,huntington2015mreom_orb_select,huntington2015mreom_bench`
可视为分子电子结构理论中的一种"变换并对角化"方法。
一次 MR-EOM-CC 计算包含一次态平均 CASSCF 计算（纳入若干低激发态），
以及求解一组簇振幅（cluster amplitude），后者定义了一系列相似变换哈密顿量。
这些多体变换的最终目标是将 CAS 组态与构成一阶相互作用空间的重要激发组态
（例如 2p2h、2p1h、1p1h 等）有效解耦。通过定义合适的簇算符，
在每次变换中大部分这类激发都可以以内收缩方式纳入。
因此所得的最终变换哈密顿量可以在原始一阶相互作用空间的一个小子空间上对角化，
从而获得许多电子态。如 {numref}`sec:modelchemistries.mreom` 一节所讨论的，
ORCA 中的 MR-EOM-CC 实现因此使用 CASSCF 模块（获得态平均 CASSCF 参考）、
MDCI 模块（求解振幅方程并计算各种相似变换哈密顿量的矩阵元）
以及 MRCI 模块（对最终变换哈密顿量对角化）。
该方法的一些可取特性是：

-   可通过对角化一个在紧凑对角化集合上的相似变换哈密顿量获得许多态
    （例如 MR-EOM-T|T$^\dagger$|SXD|U 中的最终对角化空间只包括 CAS 组态与
    1h、1p 组态）。

-   只需一次态平均 CASSCF 计算和求解一组振幅即可定义最终的相似变换哈密顿量，
    且结果通常对 CAS 的精确定义相当不敏感（态平均中只需纳入少数低激发多重态）。

-   MR-EOM-CC 方法对非活性、活性与虚拟子空间中的轨道旋转严格不变，
    并同时保持自旋对称性与空间对称性。

(table:mreom.trans)=
:::{flat-table} ORCA 的 MR-EOM-CC 实现中所考虑的各种 MR-EOM-CC 变换的细节。算符分量的方程以及确定相应振幅的残差方程也列于表中。注意我们采用通常的（Einstein）约定，重复指标求和。
:header-rows: 1
:class: footnotesize

* - 名称
  - 变换
  - 算符
  - 算符分量
  - 残差方程

* - {rspan}`1` T
  - $\widehat{\xbar{H}}=e^{-\widehat{T} }\widehat{H}e^{\widehat{T} }$
  - $\widehat{T}=\widehat{T}_1+\widehat{T}_2$
  - $\widehat{T}_1=t_i^a\widehat{E}_i^a$
  - $R^{a}_i=\sum_{\mathfrak{m} }w_{\mathfrak{m} }\left\langle\Phi_{\mathfrak{m} }\right\vert \widehat{E}^{i}_{a}\widehat{\xbar{H}}\left\vert\Phi_{\mathfrak{m} }\right\rangle$
* - $=\xbar{h}_0+\xbar{h}^p_q\big\{\widehat{E}^{p}_{q}\big\}+\xbar{h}^{pq}_{rs}\big\{\widehat{E}^{pq}_{rs}\big\}+\ldots$
  - 
  - $\widehat{T}_2=\frac{1}{2}t_{ij}^{ab}\widehat{E}_{ij}^{ab}$
  - $R_{ij}^{ab}=\xbar{h}^{ab}_{ij}$
* - {rspan}`1` T$^{\dagger}$
  - $\widehat{\xbar{H}}_2e^{-\widehat{T}^{\dagger} }$
  - $\widehat{T}^{\dagger}=\widehat{T}^{\dagger}_1+\widehat{T}^{\dagger}_2$
  - $\widehat{T}^{\dagger}_1=t_a^i\widehat{E}_a^i$
  - 无（*即*令 $t^{i}_{a}\approx t^a_i$）
* - $=\widetilde{h}_0+\widetilde{h}\,^{p}_{q}\big\{\widehat{E}^{p}_{q}\big\}+\widetilde{h}\,^{pq}_{rs}\big\{\widehat{E}^{pq}_{rs}\big\}+\ldots$
  -
  - $\widehat{T}^{\dagger}_2=\frac{1}{2}t_{ab}^{ij}\widehat{E}_{ab}^{ij}$
  - 无（*即*令 $t^{ij}_{ab}\approx t^{ab}_{ij}$）
* - SXD
  - $\widehat{\xbar{F}}=\big\{e^{\widehat{S}+\widehat{X}+\widehat{D} }\big\}^{-1}\widehat{\mathcal{H} }_2\big\{e^{\widehat{S}+\widehat{X}+\widehat{D} }\big\}$
  - $\widehat{S}=\widehat{S}_2$
  - $\widehat{S}_2=s_{i'j'}^{aw}\widehat{E}_{i'j'}^{aw}$
  - $R^{aw}_{i'j'}=\xbar{f}\,^{aw}_{i'j'}$
* - 
  - $=\xbar{f}_0+\xbar{f}\,^{p}_{q}\big\{\widehat{E}^{p}_{q}\big\}+\xbar{f}\,^{pq}_{rs}\big\{\widehat{E}^{pq}_{rs}\big\}+\ldots$
  - $\widehat{X}=\widehat{X}_2$
  - $\widehat{X}_2=x_{i'x}^{aw}\widehat{E}_{i'x}^{aw}$
  - $R^{aw}_{i'x}=\xbar{f},^{aw}_{i'x}$
* - 
  - 
  - $\widehat{D}=\widehat{D}_2$
  - $\widehat{D}_2=d_{xi'}^{aw}\widehat{E}_{xi'}^{aw}$
  - $R^{aw}_{xi'}=\xbar{f}\,^{aw}_{xi'}$
* - U
  - $\widehat{G}=e^{-\widehat{U} }\widehat{\xbar{F}}_2e^{\widehat{U} }$
  - $\widehat{U}=\widehat{U}_2$
  - $\widehat{U}_2=u_{i'j'}^{wx}\widehat{E}_{i'j'}^{wx}$
  - $R^{wx}_{i'j'}=g^{wx}_{i'j'}$
* - 
  - $=g_0+g^{p}_{q}\big\{\widehat{E}^{p}_{q}\big\}+g^{pq}_{rs}\big\{\widehat{E}^{pq}_{rs}\big\}+\ldots$
  -
  -
  -
:::

由于 MR-EOM-CC 方法的细节相当复杂，我们请感兴趣的读者参阅文献
{cite}`datta2011pICMRCC,datta2012mreom,demel2013mreom,nooijen2014mreom,huntington2015mreom_orb_select,huntington2015mreom_bench`
以获得更详细的讨论。注意关于 ORCA 中 MR-EOM-CC 实现的细节可参见文献
{cite}`huntington2015mreom_orb_select` 与 {cite}`huntington2015mreom_bench`。
在下面的讨论中，我们指出构成分子轨道基的一般空间轨道 $p,q,r,s$ 被划分为
（双占据的）非活性核心轨道 $i',j',k',l'$、占据轨道 $i,j,k,l$
（即非活性核心与活性轨道子空间的并集）、活性轨道 $w,x,y,z$ 与虚拟轨道 $a,b,c,d$。
一般而言，多体相似变换取如下一般形式

$$\begin{aligned}
\widehat{G}=\big\{e^{\widehat{Y} }\big\}^{-1}\widehat{\xbar{H}}_{2}\big\{e^{\widehat{Y} }\big\}=g_0+\sum_{p,q}g^{p}_{q}\big\{\widehat{E}^{p}_{q}\big\}+\sum_{p,q,r,s}g^{pq}_{rs}\big\{\widehat{E}^{pq}_{rs}\big\}+\ldots,\end{aligned}$$

其中 $\widehat{Y}$ 是簇算符，$\widehat{\xbar{H}}_2$ 是裸哈密顿量或截断到双体算符的
相似变换哈密顿量。花括号表示 Kutzelnigg-Mukherjee 正规排序
（normal ordering）{cite}`mukherjee1997normalorder,kutzelnigg1997normalorder`，
它在 MR-EOM-CC 形式体系的定义中被大量使用。
ORCA 的 MR-EOM-CC 实现中所需考虑的各种变换汇总于 {numref}`table:mreom.trans`。
该表还包括各种内收缩簇算符的算符分量表达式，以及必须为各种振幅求解的残差方程。
注意残差方程通常是多体型的（即通过令相似变换哈密顿量的相应矩阵元为零得到）。
唯一的例外是定义 $t_i^a$ 振幅的残差方程，它是一个投影方程，形式为

$$R_i^a=\sum_{\mathfrak{m} }w_{\mathfrak{m} }\big\langle\Phi_{\mathfrak{m} }\vert \widehat{E}^{i}_a\widehat{H}\vert\Phi_{\mathfrak{m} }\big\rangle.$$

这里 $\vert \Phi_{\mathfrak{m} }\big\rangle$ 是态平均 CAS 中所包含的
第 $\mathfrak{m}^{\text{th} }$ 个态，权重为 $w_{\mathfrak{m} }$。
单激发的方程之所以是投影形式，是因为它满足 Brillouin 定理
（即对所有 $i$ 与 $a$ 一阶单激发为零），而相应的多体方程（$\bar{h}_i^a=0)$ 则不然。

(table:mreom.details)=
:::{table} ORCA 中实现的三种 MR-EOM-CC 方法的细节
|          方法           |  输入关键词  |                                        算符                                        |  对角化集合   |
|:-------------------------:|:---------------:|:---------------------------------------------------------------------------------------:|:---------------------------:|
|   MR-EOM-T\|T$^\dagger$-h-v   |  `MR-EOM-T\|Td`   |                            $\widehat{T}$; $\widehat{T}^\dagger$                            | CAS, 2h1p, 1h1p, 2h, 1h, 1p |
| MR-EOM-T\|T$^\dagger$\|SXD-h-v  | `MR-EOM-T\|Td\|SXD` |        $\widehat{T}$; $\widehat{T}^\dagger$; $\widehat{S}+\widehat{X}+\widehat{D}$         |       CAS, 2h, 1h, 1p       |
| MR-EOM-T\|T$^\dagger$\|SXD\|U-h-v |    `MR-EOM`     | $\widehat{T}$; $\widehat{T}^\dagger$; $\widehat{S}+\widehat{X}+\widehat{D}$; $\widehat{U}$ |         CAS, 1h, 1p         |

:::

注意 ORCA 中实现了三种不同的 MR-EOM-CC 方法。也就是说，当前实现支持
MR-EOM-T|T$^\dagger$-h-v、MR-EOM-T|T$^\dagger$|SXD-h-v 与
MR-EOM-T|T$^\dagger$|SXD|U-h-v 计算。这里有必要讨论这些方法所用的命名约定。
我们用竖线分隔定义给定 MR-EOM-CC 方法的变换序列中所涉及的每一次变换。
例如 T|T$^\dagger$|SXD 表示先进行 T 变换，接着是 T$^\dagger$ 变换，
然后是 SXD 变换。h-v 表示变换后哈密顿量的矩阵元在进入 MRCI 对角化之前
已作厄米化（h）与顶点对称化（v）处理（更多信息见文献
{cite}`huntington2015mreom_bench`）。本质上，这意味着双电子积分的完整八重对称性
（以及单体矩阵元的厄米性）已被强加于变换后哈密顿量的矩阵元之上。
三种 MR-EOM-CC 方法的细节汇总于表 {numref}`table:mreom.details`。
该表包括在 ORCA 中启动计算所用的关键词（在输入第一行）、所涉及的各种算符，
以及最终对角化集合中所包含的组态。可以清楚看到
MR-EOM-T|T$^\dagger$|SXD|U-h-v 方法最具成本效益，因为它在最终对角化集合中
除 CAS 外只包括 1h 与 1p 组态。

对控制 MR-EOM-CC 计算较为重要的一些 `%mdci` 关键词如下（这里给出默认值）：

```orca
%mdci
  STol              1e-7        #Convergence Tolerance on Residual Equations
  MaxIter           100         #Maximum Number of Iterations
  DoSingularPT      false       #Activate the Singular PT/Projection Procedure
  SingularPTThresh  0.01        #Threshold for the Singular PT/Projection
                                #Procedure
  PrintOrbSelect    false       #Print the Eigenvalues of the Orbital Selection
                                #Densities (and R_core and R_virt values)
                                #and Terminate the Calculation
  CoreThresh        0.0         #Core Orbital Selection Threshold
  VirtualThresh     1.0         #Virtual Orbital Selection Threshold
end
```

如下文所述，轨道选择方案通过在简单输入行中加入 `!OrbitalSelection` 来启用。
CASSCF 与 MRCI 模块特有的关键词分别在 {numref}`sec:modelchemistries.casscf` 与
{numref}`sec:modelchemistries.mrci` 两节讨论。我们指出，在 MR-EOM-T|T$^\dagger$-h-v
与 MR-EOM-T|T$^\dagger$|SXD-h-v 计算中，可以覆盖最终 MRCI 对角化中的默认激发类。
做法是指定 `excitations none`，然后在给定多重度块内显式设置激发标志。
例如，如果我们希望在最终对角化集合中有 1h、1p、1h1p、2h 与 2h1p 激发，
则应指定（这里我们请求 6 个单重态并有 CAS(6,4) 参考）：

```orca
%mrci
    newblock 1 *
        excitations none
        Flags[is]   1
        Flags[sa]   1
        Flags[ia]   1
        Flags[ijss] 1
        Flags[ijsa] 1
        nroots      6
        refs
            cas(6,4)
        end
    end
end
```

(sec:modelchemistries.mreom.details.calc)=
### 运行 MR-EOM-CC 计算所需的步骤（The Steps Required to Run an MR-EOM-CC Calculation）

为说明典型 MR-EOM-CC 计算中所需的各种步骤，我们将考虑在 MR-EOM-T|T$^{\dagger}$|SXD|U-h-v
理论级别上计算中性 Fe 原子的激发能。

(sec:modelchemistries.mreom.calc.sacas)=
#### 态平均 CASSCF 计算（State-Averaged CASSCF Calculation）

显然，第一步是为后续 MR-EOM-CC 计算确定合适的态平均 CASSCF 参考。
在为 MR-EOM-CC 计算选择态平均 CAS 时，我们通常纳入若干与我们希望在最终 MR-EOM
计算中计算的（数目多得多的）态具有相同性质的低激发多重态。
对于中性 Fe 原子，我们通常有 4s$^2$3d$^6$ 性质或 4s$^1$3d$^7$ 性质的电子态。
从 NIST 原子光谱数据库{cite}`nist_atomic_spectra,nave1994Fe`我们发现最低的
$^5$D 多重态是 4s$^2$3d$^6$ 性质，而较高的 $^5$F 多重态是 4s$^1$3d$^7$ 性质。
因此我们可以设置一个态平均 CASSCF(8,6) 计算（即 6 个轨道（4s 与 3d）中 8 个电子），
纳入 $^5$D 与 $^5$F 态，并选择权重使 4s 轨道的平均占据数为 1.5。
如文献 {cite}`liu2015mreom_bench` 所讨论的，这样做是为了避免态平均偏向任一
4s 组态。我们将运行态平均 CASSCF 计算，采用二阶 DKH 方法（见
{ref}`sec:essentialelements.relativistic.dkh`）在 Def2-TZVPP 基组中纳入相对论效应
（即 {numref}`sec:essentialelements.basisset` 一节所列的 DKH-Def2-TZVPP
相对论收缩基组）。态平均 CASSCF(8,6) 计算的输入文件形式为：

```{literalinclude} ../../orca_working_input/C06S22_485.inp
:language: orca
```

这里我们请求了 12 个五重态（最低的 $^5$D 与 $^5$F 多重态），
并选择五个 $^5$D 态的权重为 0.7、七个 $^5$F 态的权重为 0.5，
使得 4s 轨道的总占据数为 1.5。计算收敛后，检查 CASSCF 计算最后一个宏迭代
（本例中为宏迭代 8）所打印的结果非常重要。本例中我们有：

```orca
MACRO-ITERATION   8:
   --- Inactive Energy E0 = -1249.82392764 Eh
   --- All densities will be recomputed
CI-ITERATION   0:
 -1271.258899450   0.000000000001 (    0.00)
 -1271.258899450   0.000000000001
 -1271.258899450   0.000000000001
 -1271.258899450   0.000000000001
 -1271.258899450   0.000000000001
 -1271.186288591   0.000000000001
 -1271.186288591   0.000000000001
 -1271.186288591   0.000000000002
 -1271.186288591   0.000000000001
 -1271.186288591   0.000000000001
 -1271.186288591   0.000000000001
 -1271.186288591   0.000000000001
   CI-PROBLEM SOLVED
   DENSITIES MADE
   E(CAS)= -1271.222594021 Eh DE=   -1.591616e-12
   --- Energy gap subspaces: Ext-Act = 0.276   Act-Int = 2.469
   N(occ)=  1.50000 1.30000 1.30000 1.30000 1.30000 1.30000
   ||g|| =     4.669702e-05 Max(G)=    1.104493e-05 Rot=68,1
```

在 `CI-ITERATION 0` 正下方打印了最终 CAS-CI 能量，可以看到它们遵循正确的简并模式
（即 5 个能量为 `-1271.258899450` 的态和 7 个能量为 `-1271.186288591` 的态）。
此外还打印了最终态平均 CASSCF 能量（`E(CAS)= -1271.222594021`）与占据数
（`N(occ)= 1.50000 1.30000 1.30000 1.30000 1.30000 1.30000`）。
正如预期，4s 轨道的占据数确实是 1.5，而各 3d 轨道的占据数为 1.3。

#### 选择要纳入 MR-EOM-CC 计算的态（Selection of the States to Include in the MR-EOM-CC Calculation）

获得令人满意的 CASSCF 参考后，下一步是确定要纳入 MR-EOM-CC 计算的态数。
从 NIST 原子光谱数据库可知，4s$^2$3d$^6$ 与 4s$^1$3d$^7$ 性质的较高激发态
是单重态、三重态或五重态。为弄清每个多重度块应纳入多少个态，可以进行一次
廉价的 CAS-CI 计算。做法是读入前一次 CASSCF 计算的轨道（这里存储在文件
`CAS.gbw` 中）并请求态平均 CASSCF 计算的单次迭代（即使用 `NoIter` 关键词）：

```{literalinclude} ../../orca_working_input/C06S22_486.inp
:language: orca
```

这里经过若干尝试后，我们选择了 15 个五重态、90 个三重态与 55 个单重态。
重要的是我们要计算到足够高能量的所有态（即所有感兴趣的态），
并且必须有完整的多重态。因此可能需要对该过程进行若干次迭代，
以选择每个多重态的恰当态数。应分析的输出文件相关部分是
`SA-CASSCF TRANSITION ENERGIES`。对上述计算，我们得到
（这里只显示前 33 个根的 CAS-CI 能量）：

```orca
-----------------------------
SA-CASSCF TRANSITION ENERGIES
------------------------------

LOWEST ROOT (ROOT 0 ,MULT 5) =  -1271.258899450 Eh -34592.713 eV

STATE   ROOT MULT  DE/a.u.    DE/eV    DE/cm**-1
   1:    1    5   0.000000     0.000      0.0
   2:    2    5   0.000000     0.000      0.0
   3:    3    5   0.000000     0.000      0.0
   4:    4    5   0.000000     0.000      0.0
   5:    5    5   0.072611     1.976  15936.2
   6:    6    5   0.072611     1.976  15936.2
   7:    7    5   0.072611     1.976  15936.2
   8:    8    5   0.072611     1.976  15936.2
   9:    9    5   0.072611     1.976  15936.2
  10:   10    5   0.072611     1.976  15936.2
  11:   11    5   0.072611     1.976  15936.2
  12:    0    3   0.092859     2.527  20380.2
  13:    1    3   0.092859     2.527  20380.2
  14:    2    3   0.092859     2.527  20380.2
  15:    3    3   0.092859     2.527  20380.2
  16:    4    3   0.092859     2.527  20380.2
  17:    5    3   0.092859     2.527  20380.2
  18:    6    3   0.092859     2.527  20380.2
  19:    7    3   0.092859     2.527  20380.2
  20:    8    3   0.092859     2.527  20380.2
  21:    9    3   0.092859     2.527  20380.2
  22:   10    3   0.092859     2.527  20380.2
  23:   11    3   0.101848     2.771  22353.1
  24:   12    3   0.101848     2.771  22353.1
  25:   13    3   0.101848     2.771  22353.1
  26:   14    3   0.101848     2.771  22353.1
  27:   15    3   0.101848     2.771  22353.1
  28:   16    3   0.101848     2.771  22353.1
  29:   17    3   0.101848     2.771  22353.1
  30:   18    3   0.102559     2.791  22509.1
  31:   19    3   0.102559     2.791  22509.1
  32:   20    3   0.102559     2.791  22509.1
```

#### 运行 MR-EOM-CC 计算（Running the MR-EOM-CC Calculation）

既然我们已选定合适的 CASSCF 参考以及希望计算的态，就可以进行 MR-EOM 计算了。
以下输入文件为中性 Fe 原子的 15 个五重态、90 个三重态与 55 个单重态运行
MR-EOM-T|T$^\dagger$|SXD|U-h-v 计算（即 CASSCF 轨道从 `CAS.gbw` 读入）：

```orcainput
!MR-EOM  DKH-Def2-TZVPP VeryTightSCF DKH

!MOREAD
%moinp "CAS.gbw"

%method frozencore fc_ewin end

%casscf
  nel 8
  norb 6
  mult 5
  nroots 12
  weights[0] = 0.7, 0.7, 0.7, 0.7, 0.7, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5
end

%mdci
  ewin -6, 10000
  STol 1e-7
end

%mrci
  ewin -6, 10000
  MaxIter 200
  newblock 5 *
    nroots 15
    refs cas(8,6) end
  end
  newblock 3 *
    nroots 90
    refs cas(8,6) end
  end
  newblock 1 *
    nroots 55
    refs cas(8,6) end
  end
end

* xyz 0 5
  Fe 0.000000 0.000000 0.000000
end
```

注意由于默认冻结核设置将 3p 轨道排除在相关处理之外，我们使用了能量窗口
（即 `%mdci` 与 `%mrci` 两个块中的 `ewin -6, 10000` 行），以便将它们纳入当前计算。
我们指出，MR-EOM-CC 计算输入与输出的详细讨论已在
{numref}`sec:modelchemistries.mreom` 一节给出，故此处不再重复。
需要重申的是，应始终检查最大（T、S 与 U）振幅的取值。理想情况下最大振幅应小于 0.1，
且不应超过 0.15。如果某些振幅大于 0.15，可能需要重新审视 CAS 的定义与所用权重。
对于 T 振幅，另一种解决方案是使用下文 {numref}`sec:modelchemistries.mreom.singularpt`
一节讨论的投影/奇异 PT 方案。

如 {numref}`sec:modelchemistries.mreom` 一节所讨论的，激发能打印在
`TRANSITION ENERGIES` 标题下。对当前计算我们得到如下结果（这里只显示 33 个态的结果）：

```orca
-------------------
TRANSITION ENERGIES
-------------------

The lowest energy is  -1271.833871822 Eh

State Mult Irrep Root Block    mEh          eV      1/cm
  0    5    -1    0    0      0.000      0.000       0.0
  1    5    -1    1    0      0.000      0.000       0.0
  2    5    -1    2    0      0.000      0.000       0.0
  3    5    -1    3    0      0.000      0.000       0.0
  4    5    -1    4    0      0.000      0.000       0.0
  5    5    -1    5    0     33.901      0.922    7440.4
  6    5    -1    6    0     33.901      0.922    7440.4
  7    5    -1    7    0     33.901      0.922    7440.4
  8    5    -1    8    0     33.901      0.922    7440.4
  9    5    -1    9    0     33.901      0.922    7440.4
 10    5    -1   10    0     33.901      0.922    7440.4
 11    5    -1   11    0     33.901      0.922    7440.4
 12    3    -1    0    1     54.743      1.490   12014.8
 13    3    -1    1    1     54.743      1.490   12014.8
 14    3    -1    2    1     54.743      1.490   12014.8
 15    3    -1    3    1     54.743      1.490   12014.8
 16    3    -1    4    1     54.743      1.490   12014.8
 17    3    -1    5    1     54.743      1.490   12014.8
 18    3    -1    6    1     54.743      1.490   12014.8
 19    5    -1   12    0     78.790      2.144   17292.5
 20    5    -1   13    0     78.790      2.144   17292.5
 21    5    -1   14    0     78.790      2.144   17292.5
 22    3    -1    7    1     95.413      2.596   20940.8
 23    3    -1    8    1     95.413      2.596   20940.8
 24    3    -1    9    1     95.413      2.596   20940.8
 25    3    -1   10    1     95.413      2.596   20940.8
 26    3    -1   11    1     95.413      2.596   20940.8
 27    3    -1   12    1     95.413      2.596   20940.8
 28    3    -1   13    1     95.413      2.596   20940.8
 29    3    -1   14    1     95.413      2.596   20940.8
 30    3    -1   15    1     95.413      2.596   20940.8
 31    3    -1   16    1     95.413      2.596   20940.8
 32    3    -1   17    1     95.413      2.596   20940.8
```

还要记住，应始终检查每个态的参考权重，因为只有由参考空间组态主导的态
才能在 MR-EOM 理论级别上被准确处理。一般而言，参考权重应大于（或接近）0.9。
在每个多重度块中，各态的能量与参考权重可在 MRCI 过程收敛后于 `CI-RESULTS`
标题下找到（更详细的讨论见 {numref}`sec:modelchemistries.mreom` 一节）。

### 在 MR-EOM-CC 计算中近似纳入自旋轨道耦合效应（Approximate Inclusion of Spin-Orbit Coupling Effects in MR-EOM-CC Calculations）

自旋轨道耦合的效应可以用 MRCI 模块的 SOC 子模块近似纳入 MR-EOM-CC 计算。
这可视为在 MR-EOM-CC 中纳入自旋轨道耦合效应的一阶近似。
在更严格的表述中，必须考虑自旋轨道耦合算符的各种相似变换。
MRCI 模块 SOC 子模块的细节已在 {numref}`sec:modelchemistries.mrci.soc` 一节详细讨论，
其在 MR-EOM 形式体系中的用法与其中所述完全相同。让我们考虑在上一节所讨论的
中性 Fe 原子激发谱中计算自旋轨道耦合效应。该计算的输入文件为：

```{literalinclude} ../../orca_working_input/C06S22_488.inp
:language: orca
```

与 {numref}`sec:modelchemistries.mreom.calc` 一节所进行的计算相比，
计算各方面的收敛阈值都已收紧（即使用 `ExtremeSCF` 关键词，
`etol` 与 `gtol`（CASSCF 能量与轨道梯度收敛容差）设为 $1 \times 10^{-12}$，
MR-EOM-CC 振幅迭代中残差的收敛容差设为 $1 \times 10^{-12}$）。
我们指出，使用 `ExtremeSCF` 关键词后，计算 MRCI 部分的能量（`Etol`）与
残差（`Rtol`）收敛容差也设为 $1 \times 10^{-12}$。尽管并非绝对必要，
我们使用了非常严格的收敛阈值，以尽可能保持各多重态的简并性。
自旋轨道校正的 MR-EOM-CC 谱输出出现在
`SOC CORRECTED ABSORPTION SPECTRUM VIA TRANSITION DIPOLE MOMENTS` 标题下：

```orca
--------------------------------------------------------------------------------------------------------
      SOC CORRECTED ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS    
--------------------------------------------------------------------------------------------------------
      Transition         Energy     Energy  Wavelength fosc(D2)      D2       |DX|      |DY|      |DZ|  
                          (eV)      (cm-1)    (nm)  (*population)  (au**2)    (au)      (au)      (au)  
--------------------------------------------------------------------------------------------------------
```

通过进行 MR-EOM-T|T$^\dagger$|SXD-h-v 计算并纳入 1h1p 激发，可以获得更精确的结果。
必须指出这些计算明显更加昂贵。如上所述，要运行 MR-EOM-T|T$^\dagger$|SXD-h-v 计算，
关键词 `MR-EOM-T|Td|SXD` 必须出现在输入第一行，并且为在 MRCI 计算的每个多重度块中
启用 1h1p 激发，`%mrci` 块应为如下形式：

```orca
%mrci
  ewin -6, 10000
  MaxIter 200
  newblock 5 *
    nroots 15
    excitations none
    Flags[is] 1
    Flags[sa] 1
    Flags[ia] 1
    Flags[ijss] 1
    refs cas(8,6) end
  end
  newblock 3 *
    nroots 90
    excitations none
    Flags[is] 1
    Flags[sa] 1
    Flags[ia] 1
    Flags[ijss] 1
    refs cas(8,6) end
  end
  newblock 1 *
    nroots 55
    excitations none
    Flags[is] 1
    Flags[sa] 1
    Flags[ia] 1
    Flags[ijss] 1
    refs cas(8,6) end
  end
  soc
    dosoc true
  end
end
```

我们用 `excitations none` 将默认激发标志设为 false，然后手动将 1h（`Flags[is]`）、
1p（`Flags[sa]`）、1h1p（`Flags[ia]`）与 2h（`Flags[ijss]`）激发标志设为 true。

:::{warning}
-   目前 MR-EOM-T|T$^\dagger$|SXD|U-h-v 计算只能以最终 MRCI 中的默认激发类
    （即 1h 与 1p）运行。激发标志的任何其他输入选项都将被自动覆盖并设为默认值。

-   对于 MR-EOM-CC 计算，只测试了自旋轨道耦合效应的纳入。
    MRCI 模块中可用的其他特性（例如自旋自旋耦合、磁性质计算等）
    尚未在 MR-EOM 计算中测试过。
:::

(sec:modelchemistries.mreom.singularpt)=
### 克服 T 振幅迭代收敛问题的投影/奇异 PT 方案（A Projection/Singular PT Scheme to Overcome Convergence Issues in the T Amplitude Iterations）

在某些情形下可能存在近奇异的 T$_2$ 振幅（其量值往往很大但并不总是如此），
这会在求解 T 振幅方程时引起收敛问题。因此有时必须舍弃某些振幅以消除这些收敛问题。
近奇异的 T$_2$ 振幅形如 $t^{ab}_{wx}$，其中 ($w,x$) 是一对活性轨道，
对应于双体约化密度矩阵（RDM）的一个小本征值（对占据数 $n_{wx}$）。
当存在近奇异振幅时，可以采用奇异 PT/投影方案（即文献 {cite}`datta2011pICMRCC`
所述的方案 I），以双体 RDM 作为度规矩阵，来舍弃这些近奇异振幅并以合适的
微扰估计替换它们。作为第一个例子，让我们考虑环戊二烯（cyclopentadiene）分子的
如下计算：

```{literalinclude} ../../orca_working_input/C06S22_490.inp
:language: orca
```

T 振幅迭代在 60 次迭代后不收敛，且毫无收敛迹象（即最终最大残差为 0.000458135，
且在相当一部分迭代中呈振荡行为）。如果我们检查最大的 T 振幅，

```orca
--------------------
LARGEST T AMPLITUDES
--------------------
  19-> 24  19-> 24       0.043103
  19-> 23  19-> 23       0.031162
  11-> 25  11-> 25       0.028458
  19-> 41  19-> 41       0.027950
  11-> 47  11-> 47       0.027026
  19-> 22  19-> 22       0.025163
  19-> 21  19-> 21       0.022167
  15-> 26  15-> 26       0.022084
  11-> 47  11-> 25       0.022033
  11-> 25  11-> 47       0.022033
  19-> 24  19-> 29       0.021769
  19-> 29  19-> 24       0.021769
  19-> 36  19-> 36       0.020986
  17-> 38  17-> 38       0.019743
  19-> 41  16-> 36       0.019107
  18-> 40  18-> 40       0.017949
```

可以看到没有异常大的振幅。如果通过在 `%mdci` 块中加入 `DoSingularPT true` 行
来开启奇异 PT/投影方案：

```orca
%mdci
  STol 1e-7
  MaxIter 60
  DoSingularPT true
end
```

并重新运行计算，我们会发现 T 振幅迭代现在在 22 次迭代内成功收敛。
如果查看最大的 T 振幅：

```orca
--------------------
LARGEST T AMPLITUDES
--------------------
  11-> 25  11-> 25       0.028440
  11-> 47  11-> 47       0.027027
  15-> 26  15-> 26       0.022069
  11-> 47  11-> 25       0.022031
  11-> 25  11-> 47       0.022031
  19-> 41  19-> 41       0.020463
  17-> 38  17-> 38       0.018288
  11-> 43  11-> 43       0.017250
  11-> 39  11-> 39       0.016838
  15-> 27  15-> 27       0.016001
  13-> 26  13-> 26       0.015985
  16-> 36  16-> 36       0.015759
  19-> 41  16-> 36       0.015697
  18-> 40  18-> 40       0.015376
  17-> 31  17-> 31       0.015074
  18-> 40  17-> 38       0.014470
```

对应于活性对 $(w,x)=(19,19)$ 的大多数振幅不再出现在列表中
（即它们是已被投影掉的近奇异振幅）。列表中唯一出现的那个对应于投影后的微扰估计
（例如 `19-> 41 19-> 41 0.020463`）。

默认情况下，当奇异 PT/投影方案激活时，对占据数满足 $n_{wx}<0.01$
（即 `SingularPTThresh = 0.01`）的振幅 $t^{ab}_{wx}$ 在该流程中被微扰振幅替换。
然而在某些情形下，可能需要将 `SingularPTThresh` 阈值提高到默认值以上才能收敛。
二茂铁（ferrocene）分子就是这样一个例子。考虑如下计算：

```{literalinclude} ../../orca_working_input/C06S23_492.inp
:language: orca
```

即使激活了奇异 PT/投影方案，T 振幅迭代在 50 次迭代后仍不收敛。
如果通过在 `%mdci` 块中加入 `SingularPTThresh 0.05` 将 `SingularPTThresh` 提高到 0.05：

```orca
%mdci
  DoSingularPT true
  SingularPTThresh 0.05
  MaxIter 50
end
```

T 振幅迭代在 25 次迭代内成功收敛。

总之，T 振幅迭代偶尔会不收敛。在这种情形下，可以激活奇异 PT/投影方案
（`DoSingularPT true`）来克服这些收敛困难。有时像二茂铁的情形那样，
需要调整奇异 PT/投影流程的阈值（`SingularPTThresh`）才能收敛。
如果在更大阈值下该流程仍失败，则可能需要重新审视态平均 CAS 的定义。

(sec:modelchemistries.mreom.orbitalselect)=
## 一种用于更高效计算 MR-EOM 激发谱的轨道选择方案（An Orbital Selection Scheme for More Efficient Calculations of Excitation Spectra with MR-EOM）

如文献 {cite}`huntington2015mreom_orb_select` 所述，ORCA 中的 MR-EOM 实现可利用
一套精密方案来舍弃对描述所关注激发态并不重要的非活性与虚拟轨道。
非活性核心轨道的选择基于核心轨道选择密度（core orbital selection density）的本征值

$$D_{i'j'}=D^{t}_{i'j'}+\frac{\text{Tr}\left( D^t \right)}{\text{Tr}\left( D^s \right)+\text{Tr}\left( D^u \right)}\left( D^s_{i'j'}+D^u_{i'j'} \right),$$ (os_eq1)

其中

$$\begin{aligned}
D^t_{i'j'}&=\sum_{w,a,b}t_{i'w}^{ab^{(1) }}\left( 2t_{j'w}^{ab^{(1) }}-t_{j'w}^{ba^{(1) }} \right), \\
D^s_{i'j'}&=\sum_{k,w,a}\Big[s_{i'k}^{aw^{(1) }}\left(2_{j'k}^{aw^{(1) }}-s_{kj'}^{aw^{(1) }}\right)+s_{ki'}^{aw^{(1) }}\left(2s_{kj'}^{aw^{(1) }}-s_{j'k}^{aw^{(1) }}\right) \Big], \\
D^u_{i'j'}&=\sum_{k',w,x}u_{i'k'}^{wx^{(1) }}\left( 2u_{j'k'}^{wx^{(1) }}-u_{k'j'}^{wx^{(1) }} \right),\end{aligned}$$

分别是一阶 $t_{i'w}^{ab^{(1) }}$、$s_{i'k}^{aw^{(1) }}$ 与 $u_{i'k'}^{wx^{(1) }}$
振幅的贡献（注意所有振幅至少有一个活性指标）。
类似地，虚拟轨道的选择基于虚拟轨道选择密度的本征值

$$\rho_{ab}=\rho^t_{ab}+\frac{\text{Tr}\left( \rho^t \right)}{\text{Tr}\left( \rho^s \right)} \rho^s_{ab},$$ (os_eq5)

其中来自一阶 $T_2$ 振幅的贡献 $\rho^t$ 由下式给出

$$\rho^t_{ab}=\sum_{k,w,c}t_{wk}^{ac^{(1) }}\left( 2t_{wk}^{bc^{(1) }}-t_{wk}^{cb^{(1) }}\right) +\sum_{i',w,c}t_{i'w}^{ac^{(1) }}\left( 2t_{i'w}^{bc^{(1) }}-t_{i'w}^{cb^{(1) }} \right),$$ (os_eq6)

来自一阶 $S_2$ 振幅的贡献 $\rho^s$ 由下式给出

$$\rho^s_{ab}=\sum_{i',k,w}s_{i'k}^{aw^{(1) }}\left( 2s_{i'k}^{bw^{(1) }}-s_{ki'}^{bw^{(1) }} \right)+\sum_{i',w,x}s_{xi'}^{aw^{(1) }}\left( 2s_{xi'}^{bw^{(1) }}-s_{i'x}^{bw^{(1) }} \right).$$ (os_eq7)

对核心轨道选择密度 $D_{i'j'}$ 与虚拟轨道选择密度 $\rho_{ab}$ 对角化，
分别得到两组本征值 $\{\lambda_{i'}\}$ 与 $\{\lambda_a\}$。我们发现计算如下比值

$$\mathcal{R}_{\text{core} }=\frac{\sum_{i'=0}^{n_{\text{core} }^{\text{excluded} }} \lambda_{i'} }{\sum_{i'=0}^{n_{\text{core} }}
\lambda_{i'} } \times 100\%, $$ (os_eq8)

$$\mathcal{R}_{\text{virt} }=\frac{\sum_{a=0}^{n_{\text{virt} }^{\text{excluded} }}
\lambda_{a} }{\sum_{a=0}^{n_{\text{virt} }}
\lambda_{a} } \times 100\%, $$ (os_eq9)

（被舍弃本征值之和与所有本征值之和的比值）是有用的。
核心与虚拟子空间中的轨道选择随后基于这些比值的取值，如下文所述。

轨道选择流程通过在输入第一行加入关键词 `OrbitalSelection` 来启用，例如

```orca
! MR-EOM-CC  def2-TZVPP VeryTightSCF OrbitalSelection
```

有两个阈值参数 `CoreThresh` 与 `VirtualThresh`，分别用于确定在轨道选择流程中
要舍弃哪些非活性核心轨道与虚拟轨道。也就是说，所有满足
$\mathcal{R_{\text{core} }}<$ `CoreThresh`（即式 {eq}`os_eq8` 所定义的
$\mathcal{R_{\text{core} }}$）的非活性核心轨道都被舍弃，
所有满足 $\mathcal{R_{\text{virt} }}<$ `VirtualThresh`（即式 {eq}`os_eq9`
所定义的 $\mathcal{R_{\text{virt} }}$）的虚拟轨道都被舍弃。
这些阈值的默认值为 `CoreThresh = 0.0`（不做核心轨道选择）与
`VirtualThresh = 1.0`。不过可以通过在 `%mdci` 块中重新定义来轻松改变这些参数的取值：

```orca
%mdci
  CoreThresh 1.0
  VirtualThresh 1.0
end
```

让我们考虑上一节（{ref}`sec:modelchemistries.mreom.singularpt`）中二茂铁的计算，
并启用轨道选择流程（使用默认阈值）：

```{literalinclude} ../../orca_working_input/C06S23_496.inp
:language: orca
```

轨道选择流程的细节打印在 `ORBITAL SELECTION` 标题下：

```orca
------------------------------------------------
ORBITAL SELECTION
------------------------------------------------

T1 is NOT used in the construction of the orbital selection densities
Factor (in percent) for inactive (core) orbital selection       ...      0.000000000
Factor (in percent) for virtual orbital selection               ...      1.000000000
Inactive orbitals before selection:    15 ...   44 ( 30 MO's/ 60 electrons)
Virtual orbitals before selection:     50 ...  220 (171 MO's              )
Inactive orbitals after selection:     15 ...   44 ( 30 MO's/ 60 electrons)
Virtual orbitals after selection:      50 ...  126 ( 77 MO's              )

-------------------------------------------
TIMINGS FOR THE ORBITAL SELECTION PROCEDURE
-------------------------------------------

Total Time for Orbital Selection            ...       61.470 sec

First Half Transformation                   ...       58.041 sec ( 94.4%)
Second Half Transformation                  ...        1.789 sec (  2.9%)
Formation of Orbital Selection Densities    ...        1.629 sec (  2.7%)
Core Orbital Selection                      ...        0.000 sec (  0.0%)
Virtual Orbital Selection                   ...        0.003 sec (  0.0%)
Finalization of Orbitals                    ...        0.006 sec (  0.0%)
```

比较轨道选择流程前的虚拟轨道数（171）与轨道选择后剩下的数目（77），
可见超过一半（94 个）被舍弃。正则计算（不做轨道选择）耗时 149373 秒，
给出如下激发能：

```orca
-------------------
TRANSITION ENERGIES
-------------------

The lowest energy is  -1648.190045042 Eh

State Mult Irrep Root Block    mEh          eV      1/cm
  0    1    -1    0    0      0.000      0.000       0.0
  1    3    -1    0    1     65.110      1.772   14289.9
  2    3    -1    1    1     65.110      1.772   14289.9
  3    3    -1    2    1     70.413      1.916   15454.0
  4    3    -1    3    1     70.413      1.916   15454.0
  5    3    -1    4    1     95.979      2.612   21065.0
  6    3    -1    5    1     95.979      2.612   21065.0
  7    1    -1    1    0    105.302      2.865   23111.1
  8    1    -1    2    0    105.302      2.865   23111.1
  9    1    -1    3    0    107.034      2.913   23491.4
 10    1    -1    4    0    107.034      2.913   23491.4
 11    1    -1    5    0    160.595      4.370   35246.6
 12    1    -1    6    0    160.596      4.370   35246.6
 13    3    -1    6    1    164.694      4.482   36146.1
 14    3    -1    7    1    165.379      4.500   36296.6
 15    3    -1    8    1    165.379      4.500   36296.6
 16    3    -1    9    1    171.464      4.666   37632.1
 17    1    -1    7    0    208.587      5.676   45779.6
 18    1    -1    8    0    208.587      5.676   45779.6
 19    1    -1    9    0    213.093      5.799   46768.6
 20    1    -1   10    0    213.093      5.799   46768.6
 21    1    -1   11    0    216.225      5.884   47456.0
 22    1    -1   12    0    220.230      5.993   48334.9
 23    1    -1   13    0    220.230      5.993   48334.9
 24    1    -1   14    0    224.583      6.111   49290.3
 25    1    -1   15    0    224.583      6.111   49290.3
 26    1    -1   16    0    237.914      6.474   52216.0
 27    1    -1   17    0    237.914      6.474   52216.0
```

相比之下，启用轨道选择流程的计算在 28977 秒内运行完毕（加速 5 倍），
给出如下激发能：

```orca
-------------------
TRANSITION ENERGIES
-------------------

The lowest energy is  -1647.788478559 Eh

State Mult Irrep Root Block    mEh          eV      1/cm
  0    1    -1    0    0      0.000      0.000       0.0
  1    3    -1    0    1     65.112      1.772   14290.4
  2    3    -1    1    1     65.134      1.772   14295.3
  3    3    -1    2    1     70.520      1.919   15477.3
  4    3    -1    3    1     70.520      1.919   15477.3
  5    3    -1    4    1     96.105      2.615   21092.7
  6    3    -1    5    1     96.134      2.616   21099.0
  7    1    -1    1    0    105.415      2.868   23136.0
  8    1    -1    2    0    105.450      2.869   23143.5
  9    1    -1    3    0    107.294      2.920   23548.3
 10    1    -1    4    0    107.294      2.920   23548.3
 11    1    -1    5    0    161.082      4.383   35353.4
 12    1    -1    6    0    161.094      4.384   35356.0
 13    3    -1    6    1    164.786      4.484   36166.4
 14    3    -1    7    1    165.465      4.503   36315.4
 15    3    -1    8    1    165.465      4.503   36315.5
 16    3    -1    9    1    171.542      4.668   37649.1
 17    1    -1    7    0    208.853      5.683   45838.0
 18    1    -1    8    0    208.853      5.683   45838.0
 19    1    -1    9    0    213.419      5.807   46840.1
 20    1    -1   10    0    213.419      5.807   46840.1
 21    1    -1   11    0    216.526      5.892   47521.9
 22    1    -1   12    0    220.611      6.003   48418.4
 23    1    -1   13    0    220.611      6.003   48418.5
 24    1    -1   14    0    225.135      6.126   49411.5
 25    1    -1   15    0    225.136      6.126   49411.5
 26    1    -1   16    0    238.388      6.487   52320.1
 27    1    -1   17    0    238.388      6.487   52320.1
```

我们指出轨道选择流程的激发能与正则计算符合得非常好。然而总能量有显著差异，
因为我们目前尚未实现校正它们的流程。因此下述警告尤为重要。

警告

-   轨道选择流程只能用于计算激发能。用轨道选择流程计算的总能量未经校正，
    可能与正则结果有很大差异。

在结束对轨道选择流程的讨论之前，我们指出还有一个关键词 `PrintOrbSelect`，
可加入 `%mdci` 块以打印非活性核心轨道选择密度与虚拟轨道选择密度的本征值，
以及式 {eq}`os_eq8` 与 {eq}`os_eq9` 中定义的相应
$\mathcal{R}_{\text{core} }$ 与 $\mathcal{R}_{\text{virt} }$ 值。
如果希望通过调整 `CoreThresh` 与 `VirtualThresh` 的取值来手动选择
轨道选择流程中要舍弃的轨道，这很有用。我们指出程序在打印后即终止。
在二茂铁的计算中，若将 `%mdci` 块修改为

```orca
%mdci
  DoSingularPT true
  SingularPTThresh 0.05
  MaxIter 50
  PrintOrbSelect True
end
```

则可在输出的 `ORBITAL SELECTION` 部分找到如下信息
（这里只显示虚拟轨道选择密度的前 50 个值）：

```orca
Eigenvalues and corresponding R_core values for the core orbital selection density

Orbital        Eigenvalue        R_core
   0           0.00026936        0.419318
   1           0.00027080        0.840883
   2           0.00038739        1.443947
   3           0.00038739        2.047011
   4           0.00040299        2.674355
   5           0.00040299        3.301700
   6           0.00077636        4.510285
   7           0.00086085        5.850394
   8           0.00086085        7.190503
   9           0.00091850        8.620358
  10           0.00091850       10.050213
  11           0.00112826       11.806598
  12           0.00115561       13.605563
  13           0.00137961       15.753236
  14           0.00137961       17.900908
  15           0.00139093       20.066210
  16           0.00139093       22.231512
  17           0.00143349       24.463072
  18           0.00143350       26.694633
  19           0.00148539       29.006985
  20           0.00148539       31.319338
  21           0.00173415       34.018940
  22           0.00224131       37.508054
  23           0.00224132       40.997171
  24           0.00533017       49.294785
  25           0.00533019       57.592429
  26           0.00658679       67.846267
  27           0.00662033       78.152314
  28           0.00701718       89.076149
  29           0.00701719      100.000000

 Eigenvalues and corresponding R_virt values for the virtual orbital selection density

Orbital        Eigenvalue        R_virt
   0           0.00000119        0.000450
   1           0.00000119        0.000899
   2           0.00000134        0.001404
   3           0.00000134        0.001909
   4           0.00000136        0.002423
   5           0.00000177        0.003091
   6           0.00000178        0.003764
   7           0.00000178        0.004437
   8           0.00000215        0.005248
   9           0.00000224        0.006096
  10           0.00000224        0.006944
  11           0.00000238        0.007844
  12           0.00000347        0.009154
  13           0.00000347        0.010465
  14           0.00000364        0.011841
  15           0.00000386        0.013299
  16           0.00000396        0.014793
  17           0.00000396        0.016287
  18           0.00000437        0.017937
  19           0.00000437        0.019587
  20           0.00000499        0.021472
  21           0.00000499        0.023357
  22           0.00000794        0.026354
  23           0.00000794        0.029352
  24           0.00000819        0.032447
  25           0.00000819        0.035543
  26           0.00000927        0.039044
  27           0.00000927        0.042546
  28           0.00001002        0.046332
  29           0.00001002        0.050119
  30           0.00001137        0.054415
  31           0.00001137        0.058711
  32           0.00001158        0.063086
  33           0.00001158        0.067461
  34           0.00001381        0.072678
  35           0.00001381        0.077894
  36           0.00001417        0.083249
  37           0.00001417        0.088604
  38           0.00001465        0.094137
  39           0.00001495        0.099785
  40           0.00001495        0.105432
  41           0.00001554        0.111302
  42           0.00001554        0.117172
  43           0.00001623        0.123303
  44           0.00001689        0.129685
  45           0.00001754        0.136310
  46           0.00001754        0.142934
  47           0.00001805        0.149752
  48           0.00001805        0.156570
  49           0.00002111        0.164546

.
.
.
```

总之，轨道选择方案为在 MR-EOM-CC 框架内计算精确激发谱提供了更高效的途径。
它可用于将该方法的适用性扩展到更大的体系，我们预计它在发色团定域于分子一小部分的
大体系中会有效得多。我们重申它目前仅限于激发能的计算，如果关注总能量则不应使用。

## 通过在最终对角化流程中采用 MR-CEPA(0) 移位获得 MR-EOM-CC 的近似尺寸一致结果（Nearly Size Consistent Results with MR-EOM-CC  by Employing an MR-CEPA(0) Shift in the Final Diagonalization Procedure）

MR-EOM-CC 方法的一个缺点是它不是尺度广延的（size-extensive）（或尺寸一致的）。
尺度广延性误差源自最终的非收缩 MR-CI 对角化步骤。也就是说，它们来自变换后哈密顿量
本征矢中位于 CASSCF 参考空间之外的分量（例如 1h、1p 等组态）。
随着通过哈密顿量的逐次相似变换纳入更多激发类，最终对角化集合的规模大大减小，
从而在从 MR-EOM-T|T$^\dagger$-h-v 转到 MR-EOM-T|T$^\dagger$|SXD|U-h-v 时
尺度广延性误差小得多。为说明这一点，让我们考虑 O$_2$---O$_2$ 二聚体，
其中两个 O$_2$ 分子相距很远。对于 O$_2$ 单体，我们采用由分布在两个 $\pi^*$
轨道上的 2 个电子构成的最小活性空间，且只考虑基态 $^3\Sigma^{-}_g$（不作态平均）。
在 MR-EOM-CC 计算中我们还计算较高的 $^1\Delta_g$ 与 $^1\Sigma_g^{+}$ 单重态。
例如 MR-EOM-T|T$^\dagger$|SXD|U-h-v 计算的输入文件为：

```{literalinclude} ../../orca_working_input/C06S23_498.inp
:language: orca
```

对于二聚体，我们取参考态为由单体态的乘积 $^3\Sigma_g^+\otimes\,^3\Sigma_g^+$
构成的耦合五重态。我们指出在大间距的非相互作用极限下，二聚体的态能量可分解为
单体态能量之和。考虑到各态的简并性，有各种可能性：

1.  能量为 $E(^3\Sigma_g^{-}+\,^3\Sigma_g^{-})$ 的一个单重态、一个三重态与一个五重态，

2.  能量为 $E(^3\Sigma_g^{-}+\,^1\Delta_g)$ 的四个三重态，

3.  能量为 $E(^3\Sigma_g^{-}+\,^1\Sigma_g^{+})$ 的两个三重态，

4.  能量为 $E(^1\Delta_g+\,^1\Delta_g)$ 的四个单重态，

5.  能量为 $E(^1\Delta_g+\,^1\Sigma_g^+)$ 的四个单重态，

6.  能量为 $E(^1\Sigma_g^{+}+\,^1\Sigma_g^{+})$ 的一个单重态。

因此在 MR-EOM-CC 计算的最终对角化步骤中，我们必须请求 10 个单重态、
7 个三重态与 1 个五重态。二聚体的 MR-EOM-T|T$^\dagger|$SXD|U-h-v 计算输入文件为：

```{literalinclude} ../../orca_working_input/C06S23_499.inp
:language: orca
```

在表 {numref}`sc_energies1` 中，我们汇总了尺寸一致性测试的结果，
取二聚体态能量（大间距下）与单体态能量之和的差（以 $\text{m}E_\text{h}$ 为单位）。
显然，随着更多激发类被纳入相似变换哈密顿量且最终对角化集合规模减小，
尺寸一致性误差减小。尤其值得注意的是 MR-EOM-T|T$^\dagger$|SXD|U-h-v 方法的结果
（最终对角化集合中只包括 1h 与 1p 组态），其最大偏差为
$1.25 \times 10^{-2}~\text{m}E_\text{h}$。MR-EOM-T|T$^\dagger|$SXD-h-v 方法大得多的偏差
清楚表明 2h 激发对尺寸一致性误差有很大影响。

(sc_energies1)=
:::{table} MR-EOM-CC 的尺寸一致性测试。O$_2$---O$_2$ 二聚体能量（大间距下）与基态及各激发态的单体能量之和的能量差（以 mE$_\text{h}$ 为单位）。结果在 aug-cc-pVTZ 基组中用最小活性空间获得。

|                                             | T\|T$^{\dagger}$-h-v | T\|T$^{\dagger}$\|SXD-h-v (with 1h1p) | T\|T$^{\dagger}$\|SXD-h-v |   T\|T$^{\dagger}$\|SXD\|U-h-v   |
|:--------------------------------------------|:---------------:|:------------------------------:|:------------------:|:-----------------------:|
| $\Delta E(^3\Sigma_g^{-}+\,^3\Sigma_g^{-})$ |      12.74      |              2.77              |        1.11        | 1.00 $\times$ $10^{-5}$ |
| $\Delta E(^3\Sigma_g^{-}+\,^1\Delta_g)$     |      14.20      |              3.84              |        1.85        | 1.54 $\times$ $10^{-4}$ |
| $\Delta E(^3\Sigma_g^{-}+\,^1\Sigma_g^{+})$ |      17.21      |              5.52              |        2.83        | 4.13 $\times$ $10^{-4}$ |
| $\Delta E(^1\Delta_g+\,^1\Delta_g)$         |      15.69      |              3.10              |        2.31        | 5.26 $\times$ $10^{-3}$ |
| $\Delta E(^1\Delta_g+\,^1\Sigma_g^{+})$     |      18.83      |              7.52              |        4.76        | 5.89 $\times$ $10^{-3}$ |
| $\Delta E(^1\Sigma_g^{+}+\,^1\Sigma_g^{+})$ |      22.34      |             10.75              |        7.31        | 1.25 $\times$ $10^{-2}$ |

:::

为减小尺寸一致性误差，可以在最终对角化步骤中使用 MR-CEPA(0) 移位
（shift）。该 MR-CEPA(0) 移位可通过在 `%mrci` 块开头加入如下行轻松启用

```orca
citype mrcepa_0
```

使用 MR-CEPA(0) 移位的尺寸一致性测试结果列于表 {numref}`sc_energies2`。
对每种方法我们都看到相对表 {ref}`sc_energies1`（不使用 MR-CEPA(0) 移位）的
显著改进。最大的改进出现在 MR-EOM-T|T$^\dagger$|SXD-h-v 与
MR-EOM-T|T$^\dagger$|SXD|U-h-v 结果中。也就是说，前者的误差在纳 Hartree 量级，
而 MR-EOM-T|T$^\dagger$|SXD|U-h-v 结果中的误差则不可检测（亚纳 Hartree），
因为能量只打印到小数点后九位。有趣的是，在 MR-EOM-T|T$^\dagger$|SXD-h-v 计算中
把 1h1p 组态加入对角化集合（即 with 1h1p）后，尺寸一致性误差大大增加。
因此，使用 MR-CEPA(0) 移位对减小最终对角化集合中存在 1h、1p 与 2h 组态
所导致的尺寸一致性误差似乎最为有效。无论如何，可以轻松利用该方法
在 MR-EOM-T|T$^\dagger$|SXD-h-v 与 MR-EOM-T|T$^\dagger$|SXD|U-h-v 两种方法中
获得近似尺寸一致的结果。


(sc_energies2)=
:::{table} 使用 MR-CEPA(0) 移位的 MR-EOM-CC 尺寸一致性测试：O$_2$---O$_2$ 二聚体能量（大间距下）与基态及各激发态的单体能量之和的能量差（以 mE$_\text{h}$ 为单位）。结果在 aug-cc-pVTZ 基组中用最小活性空间获得，且每种情形下都在最终对角化中应用了 MR-CEPA(0) 移位。

|                                             | T\|T$^{\dagger}$-h-v    | T\|T$^{\dagger}$\|SXD-h-v (with 1h1p) | T\|T$^{\dagger}$\|SXD-h-v | T\|T$^{\dagger}$\|SXD\|U-h-v |
|:--------------------------------------------|:-----------------------:|:------------------------------:|:-----------------------:|:--------------------:|
| $\Delta E(^3\Sigma_g^{-}+\,^3\Sigma_g^{-})$ | 2.75 $\times$ $10^{-3}$ |              0.01              | 2.00 $\times$ $10^{-6}$ |         0.00         |
| $\Delta E(^3\Sigma_g^{-}+\,^1\Delta_g)$     |          0.06           |              0.07              |          0.00           |         0.00         |
| $\Delta E(^3\Sigma_g^{-}+\,^1\Sigma_g^{+})$ |          0.14           |              0.15              | 4.00 $\times$ $10^{-6}$ |         0.00         |
| $\Delta E(^1\Delta_g+\,^1\Delta_g)$         |          0.21           |              0.22              | 1.00 $\times$ $10^{-6}$ |         0.00         |
| $\Delta E(^1\Delta_g+\,^1\Sigma_g^{+})$     |          0.42           |              0.44              | 5.00 $\times$ $10^{-6}$ |         0.00         |
| $\Delta E(^1\Sigma_g^{+}+\,^1\Sigma_g^{+})$ |          0.82           |              0.87              | 9.00 $\times$ $10^{-6}$ |         0.00         |

:::

## 微扰型 MR-EOM-CCPT（Perturbative MR-EOM-CCPT）

MR-EOM-T 方法是为不需要迭代式 MR-EOM-CC 方法全部精度的情形开发的。
它的表现与其他多参考微扰理论（如 fic-NEVPT2）相当，
并且不像其迭代母方法那样在 $\hat T$ 与 $\hat S,\hat X,\hat D$ 振幅上存在收敛困难，
因为这些振幅是以非迭代方式计算的。MR-EOM-T 方法中唯一的迭代部分是
$\hat U$ 振幅的计算，因为它们反正收敛很快{cite}`Lechner2021`。

MR-EOM-T 方法的设置流程与 MR-EOM-CC 方法相同，上述内容同样适用于该微扰变体。
请注意轨道选择方案尚未在该变体中测试过，而且反正应该没有必要，
因为计算比迭代式 MR-EOM-CC 方法快得多。

要调用该新变体，按 MR-EOM-CC 计算的方式设置计算，然后在 `%mdci` 块中
加入关键词 `DoMREOM_MRPT True`。

结果的解释与迭代式 MR-EOM-CC 方法的结果完全一样。用微扰估计的振幅对哈密顿量
作变换并完成最终 MRCIS 对角化步骤后，打印最终各态的能量及其参考权重。
为获得可靠结果，我们再次建议参考权重应 >90%。
