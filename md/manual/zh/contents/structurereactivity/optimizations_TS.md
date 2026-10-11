```{index} Transition States
```

(sec:structurereactivity.optimization.transitionstate)=
# 过渡态搜索（Transition State Searches）

## 过渡态搜索理论（Transition State Search Theory）

作为过渡态查找算法，我们实现了成熟的本征矢量跟踪（eigenvector following）算法，采用 Baker 实现的 P-RFO 步 {cite}`baker1986comp`。该算法是一种拟 Newton 类算法。

能量的泰勒级数截断到二次项后为：

$$E=E_{0} +g_{q}\,^{+}\Delta q_{q} +\frac{1}{2}\Delta q\, ^{+}\mathrm{H}_{q} \Delta q
$$ (eqn:200)

从当前点到达驻点的 Newton–Raphson 步为：

$$\Delta q=- \mathrm{H}_{q}^{-1} g_{q} =\sum{ -\frac{V_{i}^{+} g_{q} V_{i} }{b_{i} }}
$$ (eqn:201)

其中 $V_{i}$ 和 $b_{i}$ 是 Hessian $\mathrm{H}_{q}$ 的本征矢量和本征值。该步导向 PES 上最近的驻点。根据当前点处 PES 的曲率，该驻点可以是极小值点，也可以是鞍点。

在此方程中简单地移动 Hessian 本征值 $b_{i}$，即可将步引导至具有所需特性（Hessian 恰好有一个负本征值）的驻点。过渡态搜索被分为两个不同的优化问题：能量沿一个 Hessian 本征模式最大化，而沿其余 $3N-7(6)$ 个本征模式最小化。我们引入两个不同的移动参数 $\lambda_{p}$ 和 $\lambda_{n}$，其中 $\lambda_{p}$ 是被最大化本征模式的移动参数，$\lambda_{n}$ 则移动被最小化模式的 Hessian 本征值。该方法允许我们沿任意模式最大化，而不只是沿本征值最小的那个。从对应于不同优化问题的两个不同 RFO 矩阵出发（见上述描述），我们得到 $\lambda_{p}$ 和 $\lambda_{n}$：

$$\lambda_{p} =\frac{1}{2}b_{k} +\frac{1}{2}\sqrt{ b_{k}^{2} +4F_{k}^{2} } \quad
\text{and} \quad \sum\limits_{i\ne k} { \frac{F_{i}^{2} }{\lambda_{n} -b_{i} } } = \lambda_{n}
$$ (eqn:202)

其中 $F_{i} =V_{i}^{+} g$ 是 $g$ 沿 Hessian 本征模式 $V_{i}$ 的分量，而 $\lambda_{n}$ 需要迭代求解。$\lambda_{n}$ 的解必须为负，且低于 $b_{2}$（若跟踪的不是最低模式，则低于 $b_{1}$）。如果 Hessian 有一个以上的负本征值，这些性质可能无法满足，此时 Hessian 就必须加以修正。在我们的实现中，这种情况下 Hessian 的对角元素会被移动或反号。

一旦移动参数已知，P-RFO 步 $h$ 按如下方式计算：

$$\Delta q_{k} = -\frac{\bar{{F} }_{k} V_{k} }{b_{k} -\lambda_{p} } \quad  \text{and} \quad \Delta q_{i} = -\frac{\bar{{F} }_{i} V_{i} }{b_{i} -\lambda_{n} } \quad \text{with} \quad i=1\dots n,\, \, \, i\ne k
$$ (eqn:203)

$$\Delta q=\sum\limits_{j=1}^n { \Delta q_{j} }
$$ (eqn:204)


(sec:structurereactivity.optimization.transitionstate.intro)=
## 过渡态搜索简介（Introduction to Transition State Searches）

如果你为过渡态（Transition State，TS）结构提供了一个好的估计值，那么可以用 OptTS 和 ScanTS 关键词找到相应的过渡态（此例中我们取上面弛豫势能面扫描中能量最高的结构）：

```orca
! B3LYP SV(P) TightSCF SlowConv OptTS       
# performs a TS optimization with the EF-algorithm
# Transition state: H-atom abstraction from CH4 to OH-radical

%geom 
   Calc_Hess true  # calculation of the exact Hessian
                   #  before the first optimization step
end

* int 0 2
    C  0 0 0 0.000000   0.000   0.000
    H  1 0 0 1.285714   0.000   0.000
    H  1 2 0 1.100174 107.375   0.000
    H  1 2 3 1.100975 103.353 119.612
    H  1 2 3 1.100756 105.481 238.889
    O  2 1 3 1.244156 169.257  17.024
    H  6 2 1 0.980342 100.836  10.515
*
```

:::{Note}

-   你需要对 TS 结构有一个好的猜测。弛豫势能面扫描在几乎所有情况下都有帮助（也见上面的例子）。

-   对于 TS 优化（与几何优化不同），需要精确的 Hessian、Hybrid Hessian 或对选定二阶导数的修改。

-   对 HF 和 SCF 方法（包括 RI 和 RIJCOSX 近似以及正则 MP2）可进行解析 Hessian 计算。

-   检查优化结构的本征模式中是否有一个虚频的本征模式。你也可以用 `orca_pltvib`（{ref}`sec:spectroscopyproperties.vib.animation` 一节）或任何其他能读取 ORCA 输出文件的可视化程序来可视化该本征模式。

-   如果 Hessian 是在 TS 优化过程中计算的，它会存储为 basename.001.hess；若被多次重新计算，则后续计算的 Hessian 分别存储为 basename.002.hess、basename.003.hess、……

-   如果你使用 Hybrid Hessian，则必须在 TS 优化开始时（最初三到五个循环之后）仔细检查算法是否在跟踪正确的模式（见下面的小贴士）。若不是，你可以通过 inhess read 关键词再次使用同一个 Hybrid Hessian，并尝试瞄准另一个模式（通过 `TS_Mode` 关键词，见下文）。
:::

在上面的例子中，TS 模式是局域性质的。这种情况下，你可以直接将弛豫势能面扫描与 TS 优化结合起来，使用

```orca
! ScanTS
```

命令，如下例所示：

```
! B3LYP SV(P) TightSCF SlowConv
! ScanTS 
# perform a relaxed surface scan and TS optimization
#  in one calculation
%geom 
     scan 
        B 1 0 = 2.0, 1.0, 15 
     end 
end
* int 0 2
 C     0   0   0   0.000000     0.000     0.000
 H     1   0   0   1.999962     0.000     0.000
 H     1   2   0   1.095870   100.445     0.000
 H     1   2   3   1.095971    90.180   119.467
 H     1   2   3   1.095530    95.161   238.880
 O     2   1   3   0.984205   164.404    27.073
 H     6   2   1   0.972562   103.807    10.843
*
```

:::{Note}

-   该算法执行弛豫势能面扫描，在越过极大值后中止扫描，选择能量最高的优化结构，计算所扫描坐标的二阶导数，最后执行 TS 优化。

-   如果你不希望在到达最高点后中止扫描，而是要一直执行到最后一个点，则需要输入：

```orca
%geom
  fullScan true # do not abort the scan with !ScanTS
end
```
:::

作为过渡态查找算法，我们实现了拟 Newton 类的 Hessian 模式跟踪
算法。{cite}`schlegel1987ab,schlegel1995modern,schlegel1998encyclopedia,eckert1997comp,horn1991comp,baker1986comp,hess2008chem,harvey1998theor,li2002theor`
该算法相对一个（通常是最低的）本征模式使能量最大化，而相对 Hessian 其余 $3N-7$(6) 个本征模式使能量最小化。

:::{Tip}

-   你可以在早期阶段就检查优化是否会导向"正确的"过渡态。第一步优化之后，你会在冗余内坐标部分找到如下输出：

```orca
---------------------------------------------------------------------------
                     Redundant Internal Coordinates
                        (Angstroem and degrees)
   Definition                Value    dE/dq     Step   New-Value comp.(TS mode)
----------------------------------------------------------------------------
 1. B(H  1,C  0)              1.2857  0.013136  0.0286    1.3143      0.58
 2. B(H  2,C  0)              1.1002  0.014201 -0.0220    1.0782
 3. B(H  3,C  0)              1.1010  0.014753 -0.0230    1.0779
 4. B(H  4,C  0)              1.1008  0.014842 -0.0229    1.0779
 5. B(O  5,H  1)              1.2442 -0.015421 -0.0488    1.1954      0.80
 6. B(H  6,O  5)              0.9803  0.025828 -0.0289    0.9514
 7. A(H  1,C  0,H   2)        107.38 -0.001418   -0.88    106.49
 8. A(H  1,C  0,H   4)        105.48 -0.002209   -0.46    105.02
 9. A(H  1,C  0,H   3)        103.35 -0.003406    0.08    103.43
10. A(H  2,C  0,H   4)        113.30  0.001833    0.35    113.65
11. A(H  3,C  0,H   4)        113.38  0.002116    0.26    113.64
12. A(H  2,C  0,H   3)        112.95  0.001923    0.45    113.40
13. A(C  0,H  1,O   5)        169.26 -0.002089    4.30    173.56
14. A(H  1,O  5,H   6)        100.84  0.003097   -1.41     99.43
15. D(O  5,H  1,C   0,H   2)   17.02  0.000135    0.24     17.26
16. D(O  5,H  1,C   0,H   4) -104.09 -0.000100    0.52   -103.57
17. D(O  5,H  1,C   0,H   3)  136.64  0.000004    0.39    137.03
18. D(H  6,O  5,H   1,C   0)   10.52  0.000078   -0.72      9.79
----------------------------------------------------------------------------
```
:::

每一个 Hessian 本征模式都可以用冗余内坐标的线性组合来表示。在此列表的最后一列，那些在所跟踪的上坡模式中占比很大的内坐标被标注出来。这些数字反映了它们在 TS 本征矢量中的大小（该内坐标在 TS 模式本征矢量线性组合中所占的比例）。因此在这时你就已经可以检查 TS 优化是否在跟踪正确的模式（在我们的例子中确实如此，因为我们关注的是 O5 从 C0 夺取 H1）。

-   如果你希望算法跟踪不同于最低本征值的那个模式，你可以用 `TS_Mode` 关键词选择模式编号，或者给出一个应在该模式中强烈参与的内坐标。

:::{Tip}
-   如果你寻找的是断键的 TS，相应的内坐标可能不会被包含在冗余内坐标列表中（因为键长略长），导致收敛缓慢甚至完全不收敛。为防止这种情况，可以定义一组在 TS 搜索中活跃的原子区域，例如由断键的两个原子组成。在自动生成内坐标期间，这些原子（及其相邻原子）的键半径会被增大，从而更可能把 TS 中断裂或形成的键识别为键。参见下面关键词列表中的 `TS_Active_Atoms` 和 `TS_Active_Atoms_Factor` 关键词。
:::

(sec:structurereactivity.optimization.transitionstate.hessian)=
### 过渡态计算的 Hessian（Hessians for Transition State Calculations）

对于过渡态（TS）优化，一个用于极小化的简单初始 Hessian 是不够的。在 TS 优化中我们寻找的是一阶鞍点，即 PES 上沿 TS 模式方向曲率为负的点（TS 模式也称为过渡态矢量，是 TS 几何结构处 Hessian 唯一具有负本征值的本征矢量）。从初始猜测结构出发，ORCA TS 优化中所用的算法必须相对 TS 模式向上爬坡，这意味着起始结构必须靠近 TS，且初始 Hessian 必须能反映 PES 在该点的负曲率。简单的力场 Hessian 无法反映这一点，因为它们只知道谐势，从而只有正曲率。

这种情况下最直接的选择是（在借助弛豫势能面扫描找到一个有希望的初始猜测结构之后）在开始 TS 优化之前计算精确的 Hessian。有了这个 Hessian（取决于初始猜测结构的质量），我们就知道了带负本征值的 TS 本征矢量，并且也计算了所有其他本征模式（它们应具有正力常数）的精确力常数。对于 HF、DFT 方法和 MP2，可进行解析 Hessian 计算，这也是最佳选择，详见 Frequencies 一节（{ref}`sec:structurereactivity.frequencies`）。

当只有梯度可用时（最典型的是 CASSCF），精确 Hessian 的数值计算非常耗时，人们可能会问：是否真的有必要计算完整的精确 Hessian，因为与简单力场 Hessian 相比，我们唯一需要的特殊东西就是具有负本征值的 TS 模式。

为此，ORCA 提供了两种不同的加速 Hessian 计算的可能性，取决于 TS 模式的性质：Hybrid Hessian，以及单个内坐标 Hessian 值的计算。对这两种可能，初始 Hessian 都基于力场 Hessian，只对其部分进行精确计算。如果 TS 模式是高度局域的（例如断裂或形成一个键时就是这样），那么 Hessian 中精确计算的部分可以只是一个内坐标（即构成 TS 模式的那个内坐标，也就是形成或断裂的键）的二阶导数。如果 TS 模式更复杂、更离域，例如在一个协同质子转移反应中，那么 Hybrid Hessian（即只对参与 TS 模式的那些原子计算数值二阶导数的 Hessian 矩阵，更多细节见 {ref}`sec:structurereactivity.optimization` 一节）应当就足够了。如果你处理的是更复杂的情形，而这两种途径都不成功，那么你仍然可以以完整的精确 Hessian 开始 TS 优化。

数值频率计算相当昂贵。你可以先在较低理论水平或较小基组下计算 Hessian，并将该 Hessian 用作后续 TS 优化的输入：

```orca
%geom
  inhess   Read                   # this command comes with:
  InHessName "yourHessian.hess"   # filename of Hessian input file
end
```

另一种节省计算时间的可能性是：只对那些对 TS 优化至关重要的原子计算精确 Hessian 值，而对其余部分使用近似 Hessian 值。这一选项对大体系非常有用，因为在过渡过程中只有分子的一小部分发生几何变化，因此完整精确 Hessian 的信息并非必需。用此选项时，所选原子之间的耦合被精确计算，而 Hessian 矩阵的其余部分用模型初始 Hessian 填充：

```orca
%geom
  Calc_Hess true
  Hybrid_Hess {0 1 5 6} end   # calculates a Hybrid Hessian with
                              # exact calculation for atoms 0, 1, 5 and 6
end
```

对某些分子，TS 附近的 PES 可能非常不适合 Newton–Raphson 步。这种情况下，ORCA 可以在若干步之后重新计算 Hessian：

```orca
%geom
  Recalc_Hess  5   # calculate the Hessian at the beginning
                   # and recalculate it after 5,10,15,... steps
end
```

该情形的另一个解决办法是开启信赖半径更新（trust radius update），当 Newton–Raphson 步表现异常时它会减小步长，而当 PES 看起来相当接近二次时确保更大的步长：

```orca
%geom
  Trust 0.3 # Trust <0 - use fixed trust radius (default: -0.3 au)
            # Trust >0 - use trust radius update, i.e. 0.3 means: 
            # start with trust radius 0.3 and use trust radius update 
end
```

(sec:structurereactivity.optimizatiom.transitionstate.coords)=
### 过渡态优化的特殊坐标（Special Coordinates for Transition State Optimizations）

-   如果你寻找的是断键的 TS，相应的内坐标可能不会被包含在冗余内坐标列表中（但包含它会加速收敛）。这种情况下（当然还有其他情况），你可以向自动生成的冗余内坐标集合中添加坐标或从中删除坐标（也可查看 TS_Active_Atoms 关键词）：

```orca
# add ( A ) or remove ( R ) internal coordinates
%geom
  modify_internal
      { B 10 0 A }      # add a bond between atoms 0 and 10
      { A 8 9 10 R }    # remove the angle defined
                        # by atoms 8, 9 and 10
      { D 7 8 9 10 R }  # remove the dihedral angle defined
  end                   # by atoms 7, 8, 9 and 10
end
```

## ScanTS 选项（ScanTS option）

对于相当局域的 TS 模式（只涉及一个键或一个键角；不涉及跨多个原子的协同运动），我们实现了 ScanTS 功能。使用它，用户可以在一次计算中完成弛豫势能面扫描和 TS 优化。弛豫势能面扫描之后，算法选择扫描中能量最高的优化结构作为初始猜测结构，并用其两个相邻结构来计算所扫描坐标的二阶导数（例如，若扫描第 4 步给出能量最高的结构，则结构 `basename.004.xyz` 是 TS 优化的初始猜测；结构 `basename.003.xyz` 和 `basename.005.xyz` 用于计算二阶导数）。在后续 TS 优化的第一步之前，会计算这三个结构的能量和梯度。然后将梯度变换到内坐标。所扫描坐标的 Hessian 对角值随后通过给定两个结构（我们例子中的 003 和 005）内梯度的有限差分计算得到。

为构造初始 Hessian，会构建一个模型力场 Hessian（该 Hessian 只有对角元素，非对角元素为零）。精确计算的 Hessian 对角值会取代相应内坐标的模型力场 Hessian 元素。

如果用户已经进行了常规的弛豫势能面扫描而未做后续 TS 优化，那么他仍然可以用这些结构执行同样的过程。弛豫势能面扫描总会给出每个扫描步优化结构的 xyz 文件和 gbw 文件。可以另行执行 TS 优化，以能量最高的结构作为起始结构。此外还必须提供两个相邻结构的文件（如上所述）（通过 Hess_Internal 关键词，见下文）。另外，必须给出需要计算 Hessian 对角值的内坐标（即先前扫描的坐标）。这种精确 Hessian 计算只对一个内坐标可行：

```orca
%geom
  Hess_Internal
     {B 1 0 C}               # previously scanned coordinate
     XYZ1 "scanName.003.xyz" # the xyz-files of the structures
     XYZ2 "ScanName.005.xyz" #  next to the highest energy point
     GBW1 "ScanName.003.gbw" # the gbw-files of the structures
     GBW2 "ScanName.005.xyz" #  next to the highest energy
                             # the gbw-files are optional
   end
end
```

此外，还可以对其他内坐标操纵内 Hessian 的对角值，但无需额外计算。这里用户只需定义一个值（单位为 Eh/Bohr$^2$）。

```orca
Hess_Internal
  {A 3 2 1 D 2.0} # define a diagonal Hessian value of
                  #  2 Eh/Bohr2 for the angle between
                  #  atoms 3 2 1
  {B 1 0 D -0.5}  # define a diagonal Hessian value of
                  #  -0.5 Eh/Bohr2 for the bond between
                  #  atoms 1 and 0
end
```

这样的 Hessian（对角）元素定义可对多个内坐标进行。它们只是取代力场模型 Hessian 的相应值。

(sec:structurereactivity.geomopt.hybridhess)=
## Hybrid Hessian

我们实现了"Hybrid Hessian"的计算，作为 TS 优化中完整 Hessian 计算的替代方案。这里只对 TS 优化重要的那部分 Hessian 进行精确计算。为此计算我们定义两类原子：其与其他原子的耦合被精确处理的原子（E），以及其耦合被近似处理的原子（A）。

第一步，在冗余内坐标中构建 Almloef 模型 Hessian，并变换到笛卡尔坐标。该 Hessian 给出原子对 A/A 的二阶导数元素。第二步，对 E/E 和 E/A 对之间的二阶导数元素进行数值计算，与数值频率计算相同：

$$\frac{\boldsymbol{\Delta E} }{\Delta i_{B} \Delta j_{C} }=\frac{\boldsymbol{\Delta E} }{\Delta j_{C} \Delta i_{B} }=\frac{g_{j,C}^{i,B} -g_{j,C}^{eq.}}{displ.}
$$ (eqn:205)

其中：

|                 |                                                                                    |
|:----------------|:-----------------------------------------------------------------------------------|
| $i,j$           | x、y 或 z 方向                                                              |
| $B,C$           | E/E、E/A、A/E 对                                                             |
| $displ.$        | 位移的大小                                                          |
| $g_{j,C}^{eq.}$ | 当前几何结构中 $j$ 方向上作用于原子 $C$ 的力                             |
| $g_{j,C}^{i,B}$ | 原子 $B$ 在 $i$ 方向位移后 $j$ 方向上作用于原子 $C$ 的力 |


(sec:structurereactivity.geomopt.partialhess)=
## 部分 Hessian 振动分析（Partial Hessian Vibrational Analysis）

我们实现了部分 Hessian 振动分析（Partial Hessian Vibrational Analysis，PHVA），如 Li、Jensen 在 {cite}`li2002theor` 中所发表，用于分析 QM/MM 优化所得结构驻点的性质。

```orca
# PHVA after a QM/MM optimization in the (dispersion-/PC-) field
# caused by the MM-atoms
! NumFreq
%LJCoefficients "temp.LJ" # file with the Lennard Jones
                          #  coefficients for dispersion interaction
                          # obtained from last QM/MM run
%pointcharges "temp.pc"   # file with the point charges for
                          #  electrostatic interaction
                          # obtained from last QM/MM run
 #
%freq
    PARTIAL_Hess {0 1 2}  # atoms which are "frozen" and which make
                          #  the boundary to the MM-system
     end
   end
```

:::{note}
-   该过程只应用于 QM/MM 优化的结构，用于验证驻点的性质并给出 ZPE 的估计。
:::

这里我们简要描述该过程：在 PHVA 中，我们将体系分为两部分 $B$（大小为 $n$ 个原子）和 $C$（大小为 $N-n$）。设原子集合 $B$ 属于化学变化定域的区域。部分 Hessian 矩阵构建如下：

$$\begin{pmatrix}
K_{BB} & 0  \\
 0  & K_{CC}^{\varepsilon }\\
\end{pmatrix}
$$ (eqn:206)

其中：

$$K_{BB} \quad : x,y,z \quad \text{direction}$$

$$K_{CC}^{\varepsilon } =
\begin{pmatrix}
\varepsilon & 0 & 0 \\
 0 & \ddots & 0  \\
 0  & 0 & \varepsilon \\
\end{pmatrix}, \, \varepsilon =10^{-8} \, \text{au},
$$ (eqn:207)

这对应于对 $C$ 中的原子使用近乎无穷大的质量。

由此过程我们得到如下的本征值结构：

-   六个零本征值，其模式对应于整个分子的平动和转动。

-   $3(N - n) - 6$ 个小于 1 cm$^{-1}$ 的小本征值，其模式主要对应于区域 $C$ 内部的运动。

-   三个本征值（通常小于 10 cm$^{-1}$），其模式主要对应于区域 $C$ 相对于区域 $B$ 的运动。

-   $(3n - 3)$ 个本征值，其模式主要对应于 $B$ 与 $C$ 的相对运动以及区域 $B$ 内部的运动。


(sec:structurereactivity.optimization_ts.keywords)=
## 过渡态理论关键词（Transition State Theory Keywords）

:::{raw} latex
\begingroup
\footnotesize
:::

:::{tabularcolumns} \Y{0.3}\Y{0.3}\Y{0.4}
:::

(tab:ts.options)=
:::{flat-table} `%geom` 块中用于过渡态几何优化的输入关键词和选项。
:header-rows: 1
:class: footnotesize

* - 关键词
  - 选项 / 取值
  - 说明
* - `OptTS`
  - 
  - 过渡结构优化。以 `!OptTS` 包含
* - `Scan`
  - 
  - 过渡态扫描必须包含 `!ScanTS`。
* - 
  - `B 1 2 = v1, v2, N`
  - 将原子 1 到原子 2 的键长从 v1 扫描到 v2，共 N 步。
* - 
  - `B 1 2 [v1 v2 ...]`
  - 用自定义步长值扫描原子 1 到原子 2 的键。
* - 
  - `A 1 2 3`
  - 用原子 1,2,3 扫描一个键角。
* - 
  - `D 1 2 3 4`
  - 扫描原子 1,2,3,4 的二面角。
* - `Simul_Scan`
  - `true`
  - 启用同时多维扫描（最多 3 个坐标）。
* - `FullScan`
  - `true`
  - 在过渡态优化（`!ScanTS`）之前强制进行完整的势能面扫描。
* - `TS_search`
  - `EF`
  - 启用本征矢量跟踪（Eigenvector Following）的 TS 搜索。
* - `TS_Mode`
  - `{M 0}`
  - 跟踪本征矢量 0（最低模式）。
* - 
  - `{B 0 1}`
  - 跟踪原子 0 和 1 之间的键。
* - 
  - `{A 2 1 0}`
  - 跟踪原子 2、1、0 之间的键角。
* - 
  - `{D 3 2 1 0}`
  - 跟踪原子 3、2、1、0 之间的二面角。
* - `TS_Active_Atoms`
  - `{ 1 2 3 }`
  - 参与 TS 的原子，例如对于质子转移，即质子、其受体和其供体
* - `TS_Active_Atoms_Factor`
  - `1.5`
  - 上述定义原子的键截断值所增加的倍数。默认 1.5，即增加 50%
* - `inhess`
  - `unit`
  - 以单位矩阵 Hessian 开始优化。
* - 
  - `Read`
  - 从外部文件读取 Hessian。需要 `InHessName`。
* - `InHessName`
  - `"filename.hess"`
  - 指定包含 Hessian 的文件（例如 `.hess`、`.opt`、`.carthess`）。
* - 
  - `Lindh`
  - 使用 Lindh 模型 Hessian（仅用于冗余坐标）。
* - 
  - `Almloef`
  - 使用 Almloef 模型 Hessian。
* - 
  - `Schlegel`
  - 使用 Schlegel 模型 Hessian。
* - 
  - `Swart`
  - 使用 Swart 和 Bickelhaupt 的模型 Hessian。
* - 
  - `XTB0`
  - 使用 GFN0-xTB Hessian。
* - 
  - `XTB1`
  - 使用 GFN1-xTB Hessian。
* - 
  - `XTB2`
  - 使用 GFN2-xTB Hessian。
* - 
  - `GFNFF`
  - 使用 GFN-FF Hessian。
* - `Calc_Hess`
  - `true`
  - 在优化开始时计算数值 Hessian。
* - `Recalc_Hess`
  - `5`
  - 每 5 个循环重新计算一次 Hessian。
* - `Hybrid_Hess`
  - `{0 1 5 6} end`
  - 对指定原子计算精确 Hessian，对其余使用模型。
* - `NumHess`
  - `true`
  - 请求数值 Hessian。
* - `Hess_Internal`
  - `{A 3 2 1 D 2.0}`
  - 手动设置原子 3-2-1 之间键角的 Hessian 值（Eh/Bohr²）。
* - 
  - `reset 5`
  - 5 个循环后重置被修改的 Hessian 值。
* - 
  - `{B 1 0 C}`
  - 弛豫势能面扫描后用于 Hessian 精修的坐标。
* - 
  - `XYZ1` `"scanName.003.xyz"`
  - 扫描中极大值之前的结构文件。
* - 
  - `XYZ2` `"ScanName.005.xyz"`
  - 扫描中极大值之后的结构文件。
* - 
  - `GBW1` `"ScanName.003.gbw"`
  - 可选，扫描中极大值之前的 GBW 文件。
* - 
  - `GBW2` `"ScanName.005.xyz"`
  - 可选，扫描中极大值之后的 GBW 文件。
* - `Update`
  - `Powell`
  - 对 Hessian 使用 Powell 更新。
* - 
  - `Bofill`
  - 使用 Bofill 更新（TS 优化的默认）。
* - 
  - `BFGS`
  - 使用 BFGS 更新（几何优化的默认）。
* - `HESS_Modification`
  - `Shift_Diag`
  - 移动 Hessian 的对角元素（默认）。
* - 
  - `EV_Reverse`
  - 反转对角元素的符号。
* - `HESS_MinEV`
  - `0.0001`
  - 允许的最小 Hessian 本征值。
* - `NResetHess`
  - `20`
  - 20 步后重建模型 Hessian（仅限 BFGS）。
* - `NStepsInResetHess`
  - `5`
  - 用于构建新模型 Hessian 的先前步数。
* - `Trust`
  - `-0.3`
  - 使用 0.3 au 的固定信赖半径（负号表示固定）。
* - `modify_internal`
  - `{B 10 0 A}`
  - 添加原子 0 和 10 之间的键。
* - 
  - `{A 8 9 10 R}`
  - 删除原子 8、9、10 之间的键角。
* - 
  - `{D 7 8 9 10 R}`
  - 删除原子 7、8、9、10 之间的二面角。
:::
:::{raw} latex
\endgroup
:::
