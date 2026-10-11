

<a id="sec:structurereactivity.conicalintersections"></a>
# 锥形交叉（Conical Intersections）

两个态（这里记作 I 和 J）之间锥形交叉缝空间（conical intersection seam-space）中的极小值点可以通过常规几何优化算法找到，只是所优化的梯度为 [maeda_updated_2010](../../bibliography.md)：

$$
g = g'_{diff}  + Pg_{mean}
$$

其中
$g'_{diff} = 2(E_I-E_J)(\partial E_I / \partial q - \partial E_J / \partial q)$
与梯度差矢量平行；$g_{mean}$ 是梯度的平均值，$P$ 是一个投影矩阵，用于投影掉梯度差（$x$）和非绝热耦合（$y$）方向的分量：

$$
P = 1 - x x^T - y y^T
$$

现在 ORCA 中有三种求解该问题的途径，下面逐一说明。

<a id="sec:structurereactivity.conicalintersections.gradientprojection"></a>
## 梯度投影（Gradient Projection）

这正是上面所描述的方法，当 I 与 J 之间的 NACME 可用时，它会被选作默认方法。原则上它是最快、最准确的方法。可通过如下设置调用：

```orca
%CONICAL 
  METHOD GRADIENT_PROJECTION  #or simply GP
END
```

注意（OBS.）：开启 ETF（见 [nacmes.etf](../spectroscopyproperties/tddft.md#sec:spectroscopyproperties.tddft.nacmes.etf) 一节）可在使用完整梯度投影方法时改善优化效果。

<a id="sec:structurereactivity.conicalintersections.gradientprojectionnoacme"></a>
## 无 NACME 的梯度投影（Gradient Projection without NACME）

它是对上述方法的一种近似，即完全忽略 NACME。它本质上等价于寻找一个表面交叉点，不一定能找到 CI 缝空间内部的极小值点，尽管最终的 $\Delta E_{IJ}$ 应为零。

```orca
%CONICAL 
  METHOD GP_NONACME
END
```

<a id="sec:structurereactivity.conicalintersections.updatedbranchingplane"></a>
## 更新分支平面（Updated Branching Plane）

这里的想法是：从一个猜测的 NACME（即任何与 $x$ 垂直的单位矢量）出发，对其进行逐步更新，类似于对 Hessian 的 BFGS 更新 [maeda_updated_2010](../../bibliography.md)。由 $x$ 和 $y$ 定义的"分支平面（Branching Plane）"随后迭代地变得越来越精确，直到实现收敛。已证明它相当准确，并且当 NACME 不可用时为默认方法。可通过如下方式使用：

```orca
%CONICAL 
  METHOD UBP
END
```

最后，优化所用的 $\Delta E_{IJ}$ 能量阈值可通过如下方式修改：

```orca
%CONICAL 
  ETOL 1e-4 #default
END
```

作为此类分析的进一步示例，我们展示单重态乙烯基态与第一激发态的锥形交叉优化。

!!! note "目前这只适用于 TD-DFT，将在未来版本中扩展。关于具体选项的更多细节见"
    [spectroscopyproperties.tddft](../spectroscopyproperties/tddft.md#sec:spectroscopyproperties.tddft)。

!!! note
    尽管支持定位 TD-DFT 激发态与参考态之间的 CI，但这并不是寻找基态-激发态 CI 的推荐方式，因为 TD-DFT 不能正确描述这类 CI（特别是，TD-DFT 甚至会预言交叉空间的错误维度）。相反，建议为此目的使用 SF-TD-DFT，例如以 $T_1$ 态作为参考态，并将 $S_0$ 和 $S_1$ 两个态都作为激发态来计算。（*vide infra*）

```mol
title: structure 1
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
6
structure (0 1)
C   0.595560237 -0.010483480 -0.000284187
C  -0.831313750  0.167231832  0.001482505
H  -1.381857976  0.227877089  0.963419721
H   1.265119434  0.874806815  0.006897459
H  -1.382258208  0.243775568 -0.959090898
H   1.027489724 -1.032962768 -0.008829646
--- input ---
!B3LYP DEF2-SVP CI-OPT
%TDDFT IROOT 1 END
* xyz 0 1
C        0.595560237     -0.010483480     -0.000284187
C       -0.831313750      0.167231832      0.001482505
H       -1.381857976      0.227877089      0.963419721
H        1.265119434      0.874806815      0.006897459
H       -1.382258208      0.243775568     -0.959090898
H        1.027489724     -1.032962768     -0.008829646
*
```

!!! note
    你通常可以用两个态的优化结构之间的某一结构作为 CI 优化的初始猜测。如果这不起作用，可以尝试用扫描获得更好的初始猜测。

CI 优化的结果在以下输出中给出。基态与激发态之间的能量差打印为 E diff. (CI)，对于锥形交叉而言足够接近。关于在该几何结构处计算非绝热耦合的描述，见 [nacmes.numnacme](../spectroscopyproperties/tddft.md#sec:spectroscopyproperties.tddft.nacmes.numnacme) 一节。

```
                                    .--------------------.
              ----------------------|Geometry convergence|-------------------------
              Item                value                   Tolerance       Converged
              ---------------------------------------------------------------------
              Energy change       0.0000164283            0.0000050000      NO
              E diff. (CI)        0.0000025162            0.0001000000      YES
              RMS gradient        0.0000068173            0.0001000000      YES
              MAX gradient        0.0000136891            0.0003000000      YES
              RMS step            0.0000358228            0.0020000000      YES
              MAX step            0.0000821130            0.0040000000      YES
              ........................................................
              Max(Bonds)      0.0000      Max(Angles)    0.00
              Max(Dihed)        0.00      Max(Improp)    0.00
              ---------------------------------------------------------------------

              Everything but the energy has converged. However, the energy
              appears to be close enough to convergence to make sure that the
              final evaluation at the new geometry represents the equilibrium energy.
              Convergence will therefore be signaled now

                        ***********************HURRAY********************
                        ***        THE OPTIMIZATION HAS CONVERGED     ***
                        *************************************************

     --------------------------------------------------------------------------- 
                            Redundant Internal Coordinates

                             --- Optimized Parameters ---  
                               (Angstroem and degrees)

         Definition                    OldVal   dE/dq     Step     FinalVal
     ----------------------------------------------------------------------------
      1. B(C   1,C   0)                1.3254 -0.000005 -0.0000    1.3254
      2. B(H   2,C   1)                1.1270  0.000004 -0.0000    1.1270
      3. B(H   3,C   0)                1.1271 -0.000002  0.0000    1.1271
      4. B(H   4,C   1)                1.1271  0.000000 -0.0000    1.1271
      5. B(H   5,C   0)                1.1271 -0.000002  0.0000    1.1271
      6. A(H   3,C   0,H   5)          106.00  0.000001   -0.00    106.00
      7. A(C   1,C   0,H   5)          126.97 -0.000013    0.00    126.97
      8. A(C   1,C   0,H   3)          127.03  0.000011   -0.00    127.03
      9. A(C   0,C   1,H   4)          127.03  0.000013   -0.00    127.03
     10. A(H   2,C   1,H   4)          106.01 -0.000000    0.00    106.01
     11. A(C   0,C   1,H   2)          127.04  0.000009   -0.00    127.04
     12. D(H   2,C   1,C   0,H   5)    106.86 -0.000005    0.00    106.86
     13. D(H   4,C   1,C   0,H   3)    106.76 -0.000005    0.00    106.76
     14. D(H   4,C   1,C   0,H   5)    -73.62 -0.000004    0.00    -73.61
     15. D(H   2,C   1,C   0,H   3)    -72.76 -0.000005    0.01    -72.76

     ----------------------------------------------------------------------------
                  *******************************************************
                  *** FINAL ENERGY EVALUATION AT THE STATIONARY POINT ***
                  ***               (AFTER   12 CYCLES)               ***
                  *******************************************************
```

<a id="sec:structurereactivity.conicalintersections.ciexcitedstates"></a>
## 激发态之间的 CI 极小值点（CI Minima Between Excited States）

类似地，通过同时选择 IROOT 和 JROOT（如下所示），即可请求两个激发态之间的锥形交叉极小值点。

```mol
title: structure 2
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
6
structure (0 1)
C   0.595560237 -0.010483480 -0.000284187
C  -0.831313750  0.167231832  0.001482505
H  -1.381857976  0.227877089  0.963419721
H   1.265119434  0.874806815  0.006897459
H  -1.382258208  0.243775568 -0.959090898
H   1.027489724 -1.032962768 -0.008829646
--- input ---
!B3LYP DEF2-SVP CI-OPT
%TDDFT IROOT 2
       JROOT 1
       #IROOTMULT TRIPLET would search in the triplet PES
       #SF TRUE would search for the S0-S1 CI from a T1 reference, using SF-TD-DFT
       # (but remember to set the multiplicity as 3 instead of 1)
END
* xyz 0 1
C        0.595560237     -0.010483480     -0.000284187
C       -0.831313750      0.167231832      0.001482505
H       -1.381857976      0.227877089      0.963419721
H        1.265119434      0.874806815      0.006897459
H       -1.382258208      0.243775568     -0.959090898
H        1.027489724     -1.032962768     -0.008829646
*
```
