---
title: 定域能分解（LED）
source: https://www.faccts.de/docs/orca/6.1/tutorials/prop/led.html
---

# 定域能分解（LED）

将相互作用能分解为具有物理意义的组分，对于理解和控制不同分子之间的相互作用模式非常有用。
基于 DLPNO-CCSD(T) 相互作用能的定域能分解（Local Energy Decomposition, LED）方法是 ORCA 中提供的、现有最完善的方法之一。

$$
\Delta E_{int.} = \Delta E_{el-prep}^{ref.} + E_{elstat}^{ref.} + E_{exch}^{ref.}
           + \Delta E^{C-CCSD}_{non-dispersion} + E^{C-CCSD}_{dispersion}
           + \Delta E^{C-(T) }_{int}
$$

通常，配位过程中的几何弛豫还会额外计入 $\Delta E_{geo-prep}$。这一贡献也称为*应变*（strain）。有关 LED 各项贡献的解释和物理意义的更多信息，请参阅
[ORCA 手册](https://www.faccts.de/docs/orca/6.0/manual)和文献
[[Bistoni2020c]](../bib.md#bistoni2020c)[[Bistoni2021]](../bib.md#bistoni2021)。

## 示例：CpRe(CO)_2(*n*-pentane) 中的烷烃配位

作为示例，我们将分解 *n*-pentane 在 CpRe(CO)_2(*n*-pentane) 中的相互作用能。

[![re-complex](../images/re-complex.png)](../images/re-complex.png)

*图：CpRe(CO)_2(*n*-pentane) 的分子结构。*

```mol
title: CpRe(CO)₂(n-戊烷)
theme: chem311
height: 360px
representation: ball-stick
--- xyz ---
28
structure
C -4.04623 -0.94060 -0.87986
C -3.23056 -2.00842 -0.35445
C -3.13403 -1.81280 1.05377
C -3.91155 -0.67695 1.43080
H -4.06405 -0.30844 2.43482
H -2.55793 -2.42869 1.73308
H -2.78231 -2.81070 -0.92293
H -4.33874 -0.81051 -1.91193
H -5.12295 0.73363 0.15767
Re -2.25459 0.06030 -0.00431
C -2.28573 1.94921 0.30847
O -2.41945 3.09516 0.50242
C -1.42081 0.35728 -1.70388
C 1.36998 0.37687 0.48298
C 2.65689 -0.45514 0.51279
C 3.88944 0.33865 0.06397
C 5.17382 -0.49523 0.09209
H 6.03818 0.09339 -0.23266
H -0.71033 0.32056 1.08127
H -0.03361 -1.27625 0.26666
H 0.26149 -0.82286 1.95167
H 1.48316 1.25742 1.12785
H 1.19312 0.75113 -0.53133
H 2.53534 -1.33457 -0.13562
H 2.82276 -0.83988 1.52947
H 4.00603 1.21834 0.71103
H 3.71924 0.72157 -0.95085
H 5.09141 -1.36476 -0.57032
```

LED 分析可以通过简单的输入关键词 `LED` 调用。此外，片段 CpRe(CO)_2 (1) 和 *n*-pentane (2) 可以在
输入文件中定义：

```text
!DLPNO-CCSD(T) DEF2-SVP DEF2-SVP/C DEF2/J RIJCOSX VERYTIGHTSCF TIGHTPNO LED

*XYZ 0 1
C(1) -4.46463 -0.12110 0.22162
[...]
O(1) -0.99391 0.49487 -2.78478
C(2) 0.15487 -0.43421 0.93360
[...]
H(2) 5.37983 -0.86517 1.10337
*
```

> **重要**
> 请注意，在实际计算中，建议使用三重 zeta 或更大规模的基组。

该计算将给出 LED 分析的摘要，所有能量均以原子单位表示：

```text
-------------------------------------------------
FINAL SUMMARY DLPNO-CCSD ENERGY DECOMPOSITION (Eh)
------------------------------------------------- 

Intrafragment REF. energy:    
Intra fragment   1 (REF.)              -494.831830000
Intra fragment   2 (REF.)              -196.014013871     

Interaction of fragments  2 and  1:
Electrostatics (REF.)                  -0.191884228
Exchange (REF.)                        -0.064166273
Dispersion (strong pairs)              -0.015681646 
Dispersion (weak pairs)                -0.001188732

Sum of non dispersive correlation terms:
Non dispersion (strong pairs)          -2.466925458  
Non dispersion (weak pairs)            -0.001535283
```

从该输出中，我们可以直接提取出其中三项贡献：

$$
E_{elstat}^{ref.} = \text{Electrostatics (REF.)} = -0.191884228
$$

$$
E_{exch}^{ref.} = \text{Exchange (REF.)} = -0.064166273
$$

$$
E^{C-CCSD}_{dispersion} = \text{Dispersion (strong pairs)} + \text{Dispersion (weak pairs)} =  −0.016870378
$$

对于其余三项，我们需要在相同水平下对配合物几何结构中的孤立片段进行额外计算。

对于 CpRe(CO)_2 (1)：

```text
!DLPNO-CCSD(T) DEF2-SVP DEF2-SVP/C DEF2/J RIJCOSX VERYTIGHTSCF TIGHTPNO

*XYZ 0 1
C(1) -4.46463 -0.12110 0.22162
[...]
O(1) -0.99391 0.49487 -2.78478
```

对于 *n*-pentane (2)：

```text
!DLPNO-CCSD(T) DEF2-SVP DEF2-SVP/C DEF2/J RIJCOSX VERYTIGHTSCF TIGHTPNO

*XYZ 0 1
C(2) 0.15487 -0.43421 0.93360
[...]
H(2) 5.37983 -0.86517 1.10337
*
```

这些计算将给出计算其余贡献所需的关键部分：`E(0)`、`E(CORR)(corrected)` 和 `Triples Correction (T)`：

CpRe(CO)_2 (1) 输出中的相应部分类似于：

```text
E(0)                                       ...   -494.901127802
E(CORR)(strong-pairs)                      ...     -1.652880182
E(CORR)(weak-pairs)                        ...     -0.001184997
E(CORR)(corrected)                         ...     -1.654065179
E(TOT)                                     ...   -496.555192980
```

```text
Triples Correction (T)                     ...     -0.071314179
Final correlation energy                   ...     -1.725379358
E(CCSD)                                    ...   -496.555192980
E(CCSD(T))                                 ...   -496.626507159
```

对于 *n*-pentane (2) 则类似于：

```text
E(0)                                       ...   -196.190109425
E(CORR)(strong-pairs)                      ...     -0.806037106
E(CORR)(weak-pairs)                        ...     -0.000302982
E(CORR)(corrected)                         ...     -0.806340087
E(TOT)                                     ...   -196.996449513
```

```text
Triples Correction (T)                     ...     -0.022482469
Final correlation energy                   ...     -0.828822556
E(CCSD)                                    ...   -196.996449513
E(CCSD(T))                                 ...   -197.018931981
```

有了这些数据，我们现在就可以计算缺失的 LED 贡献项：

$$
\begin{split} 
\begin{split} 
\Delta E_{el-prep}^{ref.} & =  [\text{Intra fragment   1 (REF.)} - \text{E(0)}_{frag 1}] + [\text{Intra fragment   2 (REF.)} - \text{E(0)}_{frag 2}] \\
 & = 0.245393356
\end{split}
\end{split}
$$

$$
\begin{split} 
\begin{split}
\Delta E^{C-CCSD}_{non-dispersion} & = (\text{non-dispersion (strong pairs)} + \text{non-dispersion (weak pairs)}) \\
& - (\text{E(CORR)(corrected)}_{frag 1} + \text{E(CORR)(corrected)}_{frag 2}) \\
& = -0.008055475 
\end{split}
\end{split}
$$

$$
\begin{split} 
\begin{split}
\Delta E^{C-(T) }_{int} & = \text{Triples Correction (T)}_{complex} \\ 
& - (\text{Triples Correction (T)}_{frag 1} + \text{Triples Correction (T)}_{frag 2}) \\
& = -0.002667349 
\end{split}
\end{split}
$$

现在，我们得到了片段相互作用能 LED 分析的所有组分：

| $\Delta E_{int.}$ | $\Delta E_{el-prep}^{ref.}$ | $E_{elstat}^{ref.}$ | $E_{exch}^{ref.}$ | $\Delta E^{C-CCSD}_{non-disp.}$ | $E^{C-CCSD}_{disp.}$ | $\Delta E^{C-(T)}_{int}$ | 总和 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| a.u. | 0.24539 | -0.19188 | -0.06417 | -0.00806 | -0.01687 | -0.00267 | -0.03825 |
| kcal/mol | 153.99 | -120.41 | -40.26 | -5.05 | -10.59 | -1.67 | -24.00 |

这六项贡献之和即为总相互作用能，它也可以通过用配合物的总能量减去各片段的总能量得到。下图
总结了计算各组分所需执行的步骤以及需要哪些计算数据。

[![led-summary](../images/led-summary.png)](../images/led-summary.png)

*图：LED 分析的步骤示意图。*

## 色散相互作用密度（DID）

由于伦敦色散相互作用是相互作用能的关键组分，理解并控制它们已成为现代化合物设计不可或缺的一部分。例如，
色散能量给体（dispersion-energy-donors, DED）的概念[[Grimme2006]](../bib.md#grimme2006)[[Grimme2011c]](../bib.md#grimme2011c)[[Schreiner2015]](../bib.md#schreiner2015)在这一背景下变得特别有用。
可视化 LED 分析中伦敦色散组分的一种方法是绘制色散相互作用密度（Dispersion Interaction Density, DID）图。[[Mata2016]](../bib.md#mata2016)[[Bistoni2019]](../bib.md#bistoni2019)

要获得 DID，只需在 LED 输入中加入 `%mdci DoDIDplot true end` 并按前述方式运行计算即可。

计算成功后，DID 将以 `basename.ded21` 的形式存储在 `basename.densities` 容器中。

现在我们可以使用 `orca_plot` 从 DID 创建可绘制的数据文件。要打开交互界面，请调用

```text
orca_plot basename.gbw -i
```

这里我们选择 `1 - Enter type of plot` 来决定绘制什么

```text
PlotType       ... MO-PLOT
MO/Operator    ... 0 0
Output file    ... (null)
Format         ... Grid3d/Cube
Resolution     ... 40 40 40
Boundaries     ...   -16.680972    18.410507 (x direction)
                     -12.311453    12.849005 (y direction)
                     -12.262472    11.601143 (z direction)

       1 - Enter type of plot
       2 - Enter no of orbital to plot
       3 - Enter operator of orbital (0=alpha,1=beta)
       4 - Enter number of grid intervals
       5 - Select output file format
       6 - Plot CIS/TD-DFT difference densities
       7 - Plot CIS/TD-DFT transition densities
       8 - Set AO(=1) vs MO(=0) to plot
       9 - List all available densities
      10 - Perform Density Algebraic Operations

      11 - Generate the plot
      12 - exit this program
Enter a number: 
```

从给出的列表中，我们现在选择 `15 - LED dispersion interaction density (ded21)`，它也被标记为 `available`

```text
     1 -   molecular orbitals                          
     2 -   (scf) electron density                              ......  (scfp                     )  => AVAILABLE
     3 -   (scf) spin density                                  ......  (scfr                     )  - NOT AVAILABLE
     4 -   natural orbitals                               
     5 -   corresponding orbitals                         
     6 -   atomic orbitals                                
     7 -   mdci electron density                               ......  (mdcip                    )  - NOT AVAILABLE
     8 -   mdci spin density                                   ......  (mdcir                    )  - NOT AVAILABLE
     9 -   OO-RI-MP2 density                                   ......  (pmp2re                   )  - NOT AVAILABLE
    10 -   OO-RI-MP2 spin density                              ......  (pmp2ur                   )  - NOT AVAILABLE
    11 -   MP2 relaxed density                                 ......  (pmp2re                   )  - NOT AVAILABLE
    12 -   MP2 unrelaxed density                               ......  (pmp2ur                   )  - NOT AVAILABLE
    13 -   MP2 relaxed spin density                            ......  (rmp2re                   )  - NOT AVAILABLE
    14 -   MP2 unrelaxed spin density                          ......  (rmp2ur                   )  - NOT AVAILABLE
    15 -   LED dispersion interaction density                  ......  (ded21                    )  => AVAILABLE
[...]
    42 -   LFT QDPT unrelaxed transition AO density            ......  (Tdens-LFTQDSOC           )  - NOT AVAILABLE
Enter Type: 
```

现在，程序会询问你默认建议的 `basename.ded21` 密度文件是否正确，我们予以确认

```text
The default name of the density would be: led.ded21
Is this the one you want (y/n)? y
```

通过选项 `5 - Select output file format` 我们还可以进一步选择输出文件的格式，本例中为 `Gaussian cube`，
并通过 `4 - Enter number of grid intervals` 设置所包含的网格点数。然后 `11 - Generate the plot` 将
创建 `basename.eldens.cube` 文件。该文件现在包含 DID 的数据，最终可以将其渲染到普通的
电子密度上。相应的电子密度也可以用同样的方式创建，只需改为选择 `2 - (scf) electron density` 即可。

这些文件现在可以用来渲染 DID 图，例如用 ChimeraX。左侧是 DID（等值面 = 0.12 kJ/mol/bohr^3），
右侧是映射到电子密度上的 DID。

[![re-complex-led](../images/re-complex-led.png)](../images/re-complex-led.png)

*图：左：直接的 DID 图（等值面 = 0.12 kJ/mol/bohr^3）；右：映射到电子密度上的 DID。*

从 DID 图中，我们可以很容易地看出片段的哪些部分对相互作用能的色散组分贡献最大。
