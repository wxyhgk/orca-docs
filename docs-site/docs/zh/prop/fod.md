---
title: 分数占据密度（FOD）
source: https://www.faccts.de/docs/orca/6.1/tutorials/prop/fod.html
---

# 分数占据密度（FOD）

大多数传统 DFT 方法和许多波函数理论（wave-function-theory, WFT）方法都是单参考（single-reference）方法，因此不涵盖静态电子相关（static electron correlation）效应。具有强静态电子相关的情形通常
无法用单个 Slater 行列式描述，因此常被称为"多参考"（multi-reference, MR）情形。例如，过渡金属配合物，特别是含 3*d* 金属的配合物，已知
容易出现静态电子相关，因此单参考方法可能不适合正确描述它们。文献中描述了许多多参考诊断方法，各有其优缺点。
尽管如此，分数占据密度（fractional occupation density, FOD）[[Grimme2015]](../bib.md#grimme2015) 是一种非常简单却强大的分析工具，甚至可以可视化潜在的多参考情形，ORCA 中提供了该工具。

ORCA 中默认的 FOD 分析采用 TPSS/def2-TZVP 方法，电子温度（electronic temperature）设为 5000K，以"抹平"易产生静态相关的电子。只需如下简单调用即可：

```text
!FOD

* XYZFILE 0 1 structure.xyz
```

> **注意**
> 原则上，FOD 分析可以用任何泛函进行。不过，电子温度必须调整到与所选泛函相匹配，
> 如果使用杂化泛函，尤其要匹配其中包含的 Fock 交换（Fock-exchange）比例。如何更改方法和电子温度的说明记录在
> [ORCA 手册](https://www.faccts.de/docs/orca/6.0/manual)中。

## 示例：Ni(bis-dithiolene)

让我们对潜在的电催化剂 NiBDT 进行 FOD 分析。

```mol
title: NiBDT
theme: chem311
height: 360px
representation: ball-stick
--- xyz ---
25
structure
Ni   -1.6002067    0.2502065   -0.0003481
S    -3.3823931    1.5039617   -0.0004815
S    -2.8019519   -1.5676128   -0.0007147
S    -0.3984619    2.0680264    0.0001148
S     0.1819779   -1.0035478    0.0002019
C    -4.7231842    0.3779025   -0.0008076
C    -4.4612846   -1.0082869   -0.0009494
C    -5.5353290   -1.9121780   -0.0003737
C    -6.8432986   -1.4529365    0.0003963
C    -7.1032240   -0.0766964    0.0004724
C    -6.0528479    0.8279006   -0.0002736
H    -8.1278403    0.2859146    0.0010614
H    -6.2454603    1.8978057   -0.0007489
H    -5.3245999   -2.9786641   -0.0003748
H    -7.6651706   -2.1641627    0.0009913
C     1.2608705    1.5087009    0.0005736
C     2.3349151    2.4125919    0.0003679
C     3.6428850    1.9533503   -0.0001444
C     3.9028088    0.5771099   -0.0001854
C     2.8524327   -0.3274871    0.0004449
C     1.5227693    0.1225114    0.0006544
H     2.1241862    3.4790779    0.0008070
H     4.4647574    2.6645759   -0.0005403
H     4.9274249    0.2144984   -0.0009591
H     3.0450448   -1.3973923    0.0008155
```

```text
!FOD

* XYZFILE 0 1 nibdt.xyz
```

计算成功后，ORCA 会将 N_FOD 值写入输出。该值是判断多参考情形的初步指标。在本例中，对于一个正常的闭壳层
配合物，N_FOD 非常高：

```text
N_FOD =  1.877046
```

> **注意**
> 请注意，N_FOD 值不具有大小一致性（size-consistent），在比较不同大小的配合物时，可以用电子数对其进行归一化。

此外，ORCA 将 FOD 密度存储在 `basename.densities` 容器中，可以用随 ORCA 一同提供的 `orca_plot` 工具进行可视化。可以通过命令行输入使用其交互界面：

```text
orca_plot basename.gbw -i
```

```text
PlotType       ... MO-PLOT
MO/Operator    ... 0 0
Output file    ... (null)
Format         ... Grid3D/Binary
Resolution     ... 40 40 40
Boundaries     ...   -22.359392    16.311484 (x direction)
                     -12.628859    13.574504 (y direction)
                      -7.001812     7.002006 (z direction)

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

现在我们输入 `1` 来选择所需的绘图类型：

```text
     1 -   molecular orbitals                          
     2 -   (scf) electron density                              ......  (scfp                     )  => AVAILABLE
     3 -   (scf) spin density                                  ......  (scfr                     )  - NOT AVAILABLE
     4 -   natural orbitals                               
     5 -   corresponding orbitals                         
     6 -   atomic orbitals                                
     7 -   mdci electron density                               ......  (mdcip                    )  - NOT AVAILABLE
     8 -   mdci spin density                                   ......  (mdcir                    )  - NOT AVAILABLE
[...]
    42 -   LFT QDPT unrelaxed transition AO density            ......  (Tdens-LFTQDSOC           )  - NOT AVAILABLE
Enter Type: 
```

这里我们选择 `2`，即 `(scf) electron density`。界面接下来会询问要绘制哪个密度。默认的电子密度文件是 `basename.scfp`，但由于我们要绘制 `basename.scfp_fod`，需要更改所选的密度文件。

`orca_plot` 会询问默认密度文件是否就是你要绘制的那个：

```text
The default name of the density would be: basename.scfp
Is this the one you want (y/n)?
```

输入 `n` 即可拒绝。现在你可以输入所需的 FOD 密度文件名 `basename.scfp_fod`：

```text
Enter the FileName: basename.scfp_fod
```

成功更改了用于绘图的密度文件后，我们可以通过 `5 - Select output file format` 选择所需的输出格式，例如 Gaussian cube，最后通过 `11 - Generate the plot` 生成文件 `basename.eldens.cube`，
再用所选的可视化程序进行处理。要可视化 FOD，推荐使用 0.005 a.u. 的等值面值。对我们的示例 NiBDT 而言，FOD 图如下所示：

[![fod](../images/fod.png)](../images/fod.png)

*图：NiBDT 在等值面值为 0.005 a.u. 时的 FOD 图。*

该图显示 FOD 显著离域于整个分子，表明存在很强的静态电子相关。

对于非常大的结构或高通量筛选，使用基于 xtb 的 FOD 分析（通过 ORCA）可能更为实用。
为此，你可以通过 ORCA 到 xtb 的接口调用 xtb 来进行 FOD 分析：

```text
!XTB2

%xtb
  XTBINPUTSTRING  "--fod" # string passed on to XTB call
  ETemp           5000
end

%output 
  print[p_xtb_prop] 1 
end

* XYZFILE 0 1 nibdt.xyz
```

对我们的 NiBDT 示例而言，这会将 N_FOD 值打印到 ORCA 输出中，并以 Gaussian cube 格式写出可绘图的 `fod.cub` 文件。

```text
NFOD :     2.4882
```

> **警告**
> 尽管 FOD 直观且易于使用，但它并不是判断多参考特征的 100% 可靠诊断工具，只应作为初步指标使用。我们建议始终将 FOD 分析与
> 更完善的多参考诊断方法结合使用。
