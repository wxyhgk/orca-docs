---
title: 振动频率
source: https://www.faccts.de/docs/orca/6.1/tutorials/prop/freq.html
---

# 振动频率

完成[几何优化](../prop/geoopt.md#geoopt)之后，你可能想计算体系的振动频率（vibrational frequency）并绘制简正模式（normal mode）动画。下面以乙酸为例说明如何操作：

[![aceticacid](../images/aceticacid.png)](../images/aceticacid.png)

*图：乙酸的分子结构。*

## 频率

要首先计算频率，例如使用 DFT 的 B3LYP 泛函（functional）：

```text
!B3LYP D4 DEF2-SVP FREQ
* XYZ 0 1
C         -0.81589       -0.51571       -0.02512
C          0.30690        0.49327       -0.06114
H         -0.42809       -1.56713       -0.28060
H         -1.26914       -0.51520        1.06962
H         -1.64631       -0.14518       -0.75104
O          0.16587        1.68279       -0.21470
O          1.51380       -0.07303        0.21899
H          2.16801        0.64625        0.13143
*
```

也可以在优化计算结束后立即进行，只需使用：

```text
!B3LYP D4 DEF2-SVP OPT FREQ
* XYZFILE 0 1 aceticacid.xyz
```

这样就会先执行几何优化。若优化成功，随后进行频率计算。当黑塞矩阵（Hessian）的计算开始时，会打印如下标题：

```text
-------------------------------------------------------------------------------
                               ORCA SCF HESSIAN
-------------------------------------------------------------------------------

Hessian of the Kohn-Sham DFT energy:
Kohn-Sham wavefunction type                      ... RKS
Hartree-Fock exchange scaling                    ...    0.200
Number of operators                              ...    1
Number of atoms                                  ...    8
Basis set dimensions                             ...   76
Integral neglect threshold                       ... 2.5e-11
Integral primitive cutoff                        ... 2.5e-12
```

接着计算所有必需的项。完成后，就能直接看到以 $cm^{-1}$ 为单位的振动频率：

```text
-----------------------
VIBRATIONAL FREQUENCIES
-----------------------

Scaling factor for frequencies =  1.000000000  (already applied!)

0:         0.00 cm**-1
1:         0.00 cm**-1
2:         0.00 cm**-1
3:         0.00 cm**-1
4:         0.00 cm**-1
5:         0.00 cm**-1
6:        82.29 cm**-1
7:       424.53 cm**-1
8:       544.40 cm**-1
9:       593.63 cm**-1
[...]
```

最初的几个频率总是为零，因为它们对应转动和平动模式。线型分子应有五个，非线型分子应有六个，其余才对应真正的振动模式。

### 频率的标度

如果想在热力学函数计算完成之后将所有频率值乘以某个系数，可以使用：

```text
%FREQ SCALFREQ 1.035 END
```

这样所有频率都会乘以 1.035。

### 可视化简正模式

振动模式可以[使用合适的图形界面](../first_steps/GUI.md)进行动画显示。在 Avogadro 或 Avogadro 2 中，只需打开 `basename.out` 文件，右侧应出现类似如下的面板：

[![aceticacid-avogadro2](../images/aceticacid-avogadro2.png)](../images/aceticacid-avogadro2.png)

*图：用 Avogadro 2 可视化的 ORCA 输出。*

在 ChimeraX（需安装 SEQCROW 插件）中同样可以做到，进入 `Tools` → `Quantum Chemistry` → `Visualize Normal Modes`：

[![aceticacid-chimerax](../images/aceticacid-chimerax.png)](../images/aceticacid-chimerax.png)

*图：用 ChimeraX 可视化的 ORCA 输出。*

在那里可以选择某个频率，并使用给出的动画选项查看该频率所对应的模式究竟是什么样。如果点击约 $\sim 1800 cm^{-1}$ 处的模式——按照经典有机化学预期应为 C=O 伸缩振动——会看到：

[![aceticacid-1800](../images/aceticacid-1800.gif)](../images/aceticacid-1800.gif)

*动画：$1869.95 \ \mathrm{cm}^{-1}$ 处的简正模式。*

这与经典预期相符。其他模式也是如此，例如通常指认为 C-H 伸缩振动的 $\sim 3150 cm^{-1}$ 处模式：

[![aceticacid-3100](../images/aceticacid-3100.gif)](../images/aceticacid-3100.gif)

*动画：$3126.68 \ \mathrm{cm}^{-1}$ 处的简正模式。*

## 消除负频率

计算结束后，如果出现一个或多个负频率，说明你的结构并不是该势能面（potential energy surface）上的极小值。这些负频率也称为*虚频模式*（imaginary mode），在输出文件中会特别标出。沿该模式方向的任何移动都会**降低**分子的能量：

```text
-----------------------
VIBRATIONAL FREQUENCIES
-----------------------

Scaling factor for frequencies =  1.000000000  (already applied!)

     0:       0.00 cm**-1
     1:       0.00 cm**-1
     2:       0.00 cm**-1
     3:       0.00 cm**-1
     4:       0.00 cm**-1
     5:       0.00 cm**-1
     6:     -83.22 cm**-1 ***imaginary mode***
     7:     435.79 cm**-1
     8:     544.50 cm**-1
     9:     592.38 cm**-1
```

> **重要**
> 如果可能，一般建议即使在优化计算之后也检查结构是否存在虚频模式。在少数情况下，几何优化也可能收敛到非极小值结构，例如势能面上的鞍点（saddle point）。如果你的几何是极小值，就不应有负频率；如果是过渡态，则必须恰好有一个！

在本例中，该虚频模式对应甲基的旋转。

[![aceticacid-imag](../images/aceticacid-imag.gif)](../images/aceticacid-imag.gif)

*动画：$-83.22 \ \mathrm{cm}^{-1}$ 处的虚频模式。*

要消除这类虚频模式并收敛到极小值结构，可以尝试用 `TightOPT` 或 `VeryTightOPT` 关键词收紧优化的收敛阈值。有时将数值积分网格收紧到 `DEFGRID3` 也有助于消除虚频模式。如果这些措施都无效，可以手动沿相应模式做位移并重新开始优化：

```text
!B3LYP D4 DEF2-SVP TIGHTOPT DEFGRID3 FREQ
* XYZFILE 0 1 aceticacid.xyz
```

## 数值频率

ORCA 中并非所有方法都能计算黑塞矩阵，但总可以使用 `NUMFREQ` 关键词进行**数值黑塞矩阵**（numerical Hessian）计算，例如：

```text
!RI-B2PLYP DEF2-SVP DEF2-SVP/C NUMFREQ
```

黑塞矩阵将通过中心差分（central differences）方法计算，需要 $6N$ 次位移，其中 $N$ 是体系中的原子数。这可以完全并行化，而且取决于你的内存条件，有时实际上比解析 FREQ 计算更好。

### 重启 NUMFREQ 计算

如果体系很大或方法较重，这类计算可能耗时很长。万一中途出问题导致计算中止，可以用如下方式重启：

```text
!RI-B2PLYP DEF2-SVP DEF2-SVP/C NUMFREQ
%FREQ RESTART TRUE END
```

如果 `basename.hess` 文件与输入文件位于同一目录，计算将从中断处继续。

> **重要**
> `%FREQ` 还有许多额外选项，更多信息请查阅 [ORCA 手册](https://www.faccts.de/docs/orca/6.0/manual)。
