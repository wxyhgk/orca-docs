(sec:essentialelements.numericalintegration)=
# 数值积分（Numerical Integration）

从 5.0 版本开始，ORCA 采用了一套新的数值积分求积（quadratures）方案。
它基于与旧格点方案相同的一般思路，只是我们使用了机器学习（machine
learning）方法，并结合一些最终的人工优化，为元素周期表前六行的所有原子
找到了最优参数，第七行则由此外推得到。更多细节见参考文献
{cite}`Helmich-Paris2021a`。我们还发现 COSX 格点和 DFT 格点的总体需求
并不相同，因此对它们分别进行了优化。

这一新方案的最大优点是：即使格点数相同，它也比旧方案显著更精确、更稳健。
我们测试了能量、几何结构、频率、激发能和性质，开发出三套新的格点方案，
分别命名为：DEFGRID1、DEFGRID2 和 DEFGRID3，它们会自动固定计算中
使用的所有格点。DEFGRID1 的表现基本与旧的默认方案相同，但更稳健。
第二套是新的默认方案，预计对各种应用都能给出足够小的误差。
最后一套是更重、更高精度的格点，如果以一个极其庞大的格点为参考，
它已接近该极限。

要从默认的 DEFGRID2 切换，只需在主输入中添加 `!DEFGRID1` 或 `!DEFGRID3`。

同样需要注意的是，只要需要 HF 交换（HF exchange），COSX 近似现在就是
DFT 的默认选项。这随时可以通过 `!NOCOSX` 关闭。

# 数值积分格点的细节

与所有其他常用的格点方案一样，我们的格点是按照 Becke 的方法，
把一组原子格点组装成分子格点而构建的。每个原子格点都基于该原子的优化参数
构建，并由分别定义的角向部分和径向部分组成。

整套方案从 ORCA 5.0 起进行了更新，但我们尽量使其与旧方案保持接近。
首先需要解释这些格点的总体构建方式。

(sec:essentialelements.numericalintegration.anggrid)=
## 角向格点方案（Angular Grid Scheme）

与在整个原子上使用单一角向格点不同，大多数方案都会进行所谓的格点剪枝
（grid pruning），以减少最重要区域之外的格点数，ORCA 也是如此。
在当前方案中，我们把原子格点划分为五个区域（region），每个区域使用
具有如下格点数的 Lebedev 格点：

(tab:anggridscheme)=
:::{table} ORCA 中使用的不同角向格点方案。数字表示所用的 Lebedev 格点。

| AngularGrid | 区域 1 | 区域 2 | 区域 3 | 区域 4 | 区域 5 |
|:------------|:-------:|:--------:|:--------:|:--------:|:--------:|
| **1**       |   14    |   26     |   50     |   50     |   26     |
| **2**       |   14    |   26     |   50     |   110    |   50     |
| **3**       |   26    |   50     |   110    |   194    |   110    |
| **4**       |   26    |   110    |   194    |   302    |   194    |
| **5**       |   26    |   194    |   302    |   434    |   302    |
| **6**       |   50    |   302    |   434    |   590    |   434    |
| **7**       |   110   |   434    |   590    |   770    |   590    |
:::

这些区域之间的理想截断值经过了优化，并为所有原子定义。每当在 ORCA 中
提到 AngularGrid 标志时，就会选择其中一种方案。

(sec:essentialelements.numericalintegration.radgrid)=
## 径向格点方案（Radial Grid Scheme）

给定原子的径向格点数（$n_r$）可以直接用 Krack 和 Köster 最先给出的
公式定义：

$$n_r = (15 \times \varepsilon - 40) + b \times ROW$$

其中 $\varepsilon$ 在 ORCA 中称为该格点的 IntAcc，$b$ 可以是任意数，
ROW 则指该原子在元素周期表中的行数。在最初的公式中，$b$ 被设为 $5$，
而这里它已被优化，并随上面所示的 AngularGrid 方案略有变化。

需要注意的一点是，IntAcc 每增加 $1$，就会为原子格点增加 $15$ 个径向格点，
这一点与旧的格点方案相同。针对每种角向格点，这些 IntAcc 值都经过了优化：

(tab:intaccs)=
:::{table} 交换-关联（XC）格点和 COSX 格点的优化 IntAcc 参数。

| AngularGrid | XC | COSX |
|:-----------------------------------------|:-------------------------------:|:---------------------------------:|
| **1**      |              4.004              |3.816|
| **2**      |              4.004              |4.020|
| **3**      |              4.159              |4.338|
| **4**      |              4.388              |4.871|
| **5**      |              4.629              |4.871|
| **6**      |              4.959              |4.871|
| **7**      |              4.959              |4.871|

:::

定义了径向格点数 $n_r$ 之后，实际的径向格点再由 Gauss-Chebyschev 求积
确定，使用 Treutler 和 Ahlrich 的所谓 M3 映射：

$$r = \frac{\xi}{ln 2} ln \frac{2}{1-x}$$

其中 $-1 \le x \le 1$，格点中心（$x=0$）与 $\xi$ 的值重合。
这些 $\xi$ 参数同样针对每种原子类型进行了优化。

(sec:essentialelements.numericalintegration.defgrid)=
## DEFGRID 系列

了解以上内容后，我们现在可以介绍 DEFGRID 是如何按其 AngularGrid 方案
和 IntAcc 构建的——这两者分别定义了原子格点的角向部分和径向部分。
更多细节见参考文献 {cite}`Helmich-Paris2021a`。

(tab:defgrids)=
:::{table} ORCA 不同部分所用的角向格点方案。XC 和 COSX 格点以斜杠分隔，多个 COSX 格点方案以逗号分隔。

| 格点名称     | SCF         | TD-DFT | CP-SCF | MP2 grad | MP2 2ndder |
|:-------------|:-----------:|:------:|:------:|:--------:|:----------:|
| **DEFGRID1** | 3 / 1, 1, 2 | 1 / 1  | 1 / 1  | 3        | 1          |
| **DEFGRID2** | 4 / 1, 2, 3 | 1 / 1  | 1 / 1  | 4        | 4          |
| **DEFGRID3** | 6 / 2, 3, 4 | 3 / 2  | 3 / 2  | 5        | 4          |
:::

注意：TD-DFT 和 CP-SCF 的 IntAcc 对 XC 为 3.467、对 COSX 为 3.067，
而不是默认值。这里的格点数可以更小，我们正是利用这一点来提高整体速度。

从 {numref}`tab:defgrids` 中可以看到，例如默认的 SCF XC 格点现在由
AngularGrid 4 定义（最后没有额外的积分步骤）。默认的 COSX 使用 1,2,3
格点方案，其中第三个 COSX 格点用于在 SCF 收敛后更新能量以及计算梯度。

(sec:essentialelements.numericalintegration.detailsandoptions)=
## 其他细节与选项

**新的自适应剪枝（adaptive pruning）。** 当前的剪枝方案在靠近原子核处
以及远离成键区域处使用较低的格点。然而，如果基组在原子核附近有极化函数
或有弥散 Gaussian 函数，这可能就不够了。

为改进这些情况下的格点，我们现在默认使用一种自适应剪枝方案，
它通过分析位置算符的期望值 $\langle \hat r  \rangle$ 来检测核心极化
（core-polarization）、弥散函数（diffuse functions）和陡峭的基组轨道，
并据此修正格点。在这些情况下，格点可能增大 10–20%，但结果明显更好。
要使用非自适应方案，只需设置 `%METHOD GRIDPRUNING OLDPRUNING END`。
若要完全不剪枝的格点，把 GRIDPRUNING 设为 UNPRUNED。

**更简单的 Gauss-Legendre 角向格点。** 把 AngularGrid 设为 $0$ 时，
将不再使用 Lebedev 格点，而是按照 Treutler 和 Ahlrich 的建议
{cite}`treutler1994chem` 构建 Gauss-Legendre 角向格点。
$\theta$ 点的数目默认定义为 $0.4 n_r$，而 $\phi$ 点的数目则选为
避免在极点附近过于拥挤。

这些格点总体上不如 Lebedev 格点高效，但如果需要为特定应用构建
极其庞大的格点，它们会很有用。

**SpecialGrid 选项。** 有时，你可能想提高某些需要特别关照的原子的积分精度，
而无需普遍增大格点。ORCA 提供了一种基本机制，可以在为其他所有原子保持
所选格点的同时，提高少数原子的径向积分精度。

```orca
%METHOD
   # a maximum of 64 assignments can be made
   #  in = 0 : no changes are made
   #  in > 0 : the grid will be changed for all atoms with
   #           atomic number=in to IntAcc=an
   #  in < 0 : only the specific n'th atom will have its
   #           IntAcc value changed to an
   SpecialGridAtoms  i1, i2, i3,...,in;
   SpecialGridIntAcc a1,a2,a3,...,an;
END
```

注意：从 ORCA 5.0 开始，除非有非常特殊的理由，否则已无必要再使用此选项。
构建格点时会考虑基组，并在需要时自动加以扩展。

(sec:essentialelements.numericalintegration.SCFkeys)=
## SCF 格点关键词列表

下面给出 SCF 格点选项的完整说明。有些关键词专用于 XC 积分，
有些专用于 COSX 积分，还有一部分是通用的，适用于所有情况：

```orca
%METHOD
# XC grids
AngularGrid    1    #Lebedev50
               2    #Lebedev110
               3    #Lebedev194
               4    #Lebedev302
               5    #Lebedev434 
               6    #Lebedev590 
               7    #Lebedev770 
               0    #SimpleGrid 
IntAcc         5.0  # determines no. of radial points

# COSX grids
AngularGridX   1,1,2,4,5    # the first three are used in the SCF
                            # the 4th in the MP2 gradient and
                            # the 5th for MP2 second derivatives
IntAccX        3.56,-1,4.5  # if a -1 is given, the default IntAcc is used.

# General
NThetaMax      0.4          # only for AngularGrid=0, multiplier for nr
GridPruning    Unpruned     # no Pruning
               OldPruning   # the old pruning
               Adaptive     # default (and recommended)
HGridReduced   true         # Reduce grids for H and He by one
                            # unit (default and recommended)
BFCut          1e-10        # basis fcn. cut. Is adjusted according to
                            # convergence tolerances
WeightCut      1e-14        # grid weight cut. default: 1e-14
END
```

(sec:essentialelements.numericalintegration.gridothers)=
## 修改 TD-DFT、CP-SCF 和 Hessian 格点

**TD-DFT。** CIS 或 TD-DFT 中使用的格点可以在各自的输入块中修改：

```orca
%TDDFT  # or %CIS, they are equivalent
  # XC grids
  IntAccXC 3.467
  GridXC   1

  #COSX grids
  IntAccX  3.076
  GridX    1
END
```

**CP-SCF。** CP-SCF 的格点在 %METHOD 块中修改：

```orca
%METHOD 
  # XC grids
  Z_IntAccXC  3.467
  Z_GridXC    1

  #COSX grids
  Z_IntAccX   3.076
  Z_GridX     1
  Z_GridX_RHS 2
END
```

注意：Z_Grid_RHS 仅在 MP2 中使用，这里的数值含义不同。它指的是从 SCF
中使用的多个 COSX 格点里选择哪一个，而不是指某种 AngularGrid 方案。
默认使用第二个 COSX 格点。

**Hessian。** 用于计算 Hessian 中 DFT 项的 XC 格点会自动设为比 SCF
格点高一个单位。由于二阶导数项的存在，我们发现此处使用略高的 XC 格点更好。
COSX 格点则可以自由修改：

```orca
%FREQ 
  HessGridX = 2,2,2,2
END
```

这四个数字对应 Hessian 中 COSX 的四种可能用法，详见
{ref}`sec:structurereactivity.frequencies` 一节

**非局域泛函（VV10 等）。** 默认的非局域格点由 AngularGrid 2 定义，
不建议修改。无论如何，都可以通过以下方式更改：

```orca
%METHOD
  # non-local grids
  VdwAngularGrid    2        # same scheme as the SCF ones
  VdWIntAcc         5.0      # determines no. of radial points
  VdwGridPruning    Adaptive # default
  VdwDistTCut       10       # cutoff distance between grid points, in angstroem
END
```

(sec:essentialelements.numericalintegration.whenchangedefault)=
## 何时应从默认格点切换？

一般而言，默认格点带来的误差相当小，对大多数应用都足够合理。
在使用默认的 `!DEFGRID2` 对 GMTNK55 测试集进行基准测试后，
我们发现 DFT 的误差约为 $0.01 \pm 0.03$ kcal/mol（相对于参考格点），
COSX 的误差约为 $0.05 \pm 0.10$ kcal/mol（相对于解析积分）。
我们还对几何结构、激发能和频率做了基准测试，所有误差都系统性地偏低。

不过，仍有可能需要更优格点的情形：

-   如果你需要确信能量误差低于 0.2 kcal/mol；

-   处理带有较大负电荷的阴离子时（$<-3$）；

-   对于非常微妙的分子间相互作用；

-   处理奇特的电子结构时；

-   对于大共轭体系——类石墨烯结构和大的多环芳烃。

需要时，`!DEFGRID3` 非常大且保守——它几乎覆盖了上述所有情形。
相比之下，`!DEFGRID1` 给出的格点规模接近旧版 ORCA 的默认值，
但精度仍有提高。
