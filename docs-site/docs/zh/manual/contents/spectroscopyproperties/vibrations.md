<a id="sec:spectroscopyproperties.vib"></a>
# 振动光谱（Vibrational Spectroscopy）

在 ORCA 中计算振动频率的基本用法和若干示例见：
[structurereactivity.frequencies](#sec:structurereactivity.frequencies)。以下章节更侧重于光谱学。

<a id="sec:spectroscopyproperties.vib.ir"></a>
## 红外光谱（IR Spectra）

**\*\*ORCA 4.2.1 之后 IR 打印格式有重大变化！\*\***

IR 光谱强度在频率计算中自动计算。
因此，用户无需进行任何控制。考虑以下任务：

```mol
title: structure 1
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
4
structure (0 1)
O      0.000000     0.000000     0.611880
C      0.000000     0.000000    -0.596849
H      0.952616     0.000000    -1.209311
H     -0.952616     0.000000    -1.209311
--- input ---
! OPT FREQ BP86 def2-SVP

*xyz 0 1
 O    0.000000    0.000000    0.611880
 C    0.000000    0.000000   -0.596849
 H    0.952616    0.000000   -1.209311
 H   -0.952616    0.000000   -1.209311
*
```

得到如下输出：

```orca
-----------
IR SPECTRUM
-----------

 Mode   freq       eps      Int      T**2         TX        TY        TZ
       cm**-1   L/(mol*cm) km/mol    a.u.
----------------------------------------------------------------------------
  6:   1146.68   0.000341    1.73  0.000093  (-0.000000 -0.009640  0.000000)
  7:   1224.67   0.002004   10.13  0.000511  ( 0.022596  0.000000  0.000000)
  8:   1485.77   0.001002    5.07  0.000211  ( 0.000000 -0.000000  0.014510)
  9:   1806.49   0.020286  102.51  0.003504  ( 0.000000 -0.000000  0.059197)
 10:   2769.13   0.014010   70.80  0.001579  ( 0.000000  0.000000  0.039734)
 11:   2812.52   0.039321  198.71  0.004363  ( 0.066052 -0.000000 -0.000000)
```

第一列（'Mode'）标记振动模式，频率从上到下递增。
下一列给出振动频率。
每个模式的摩尔吸收系数 $\varepsilon$ 列在 "eps" 列中。
该量与给定基频在 IR 谱中的强度成正比，因此被 `orca_mapspc`
实用程序用作 IR 强度。

"Int" 下的数值是积分吸收系数[^1]，
"T\*\*2" 列列出跃迁偶极导数的范数，
其中已包含振动部分。

要得到光谱图，可以运行 `orca_mapspc` 实用程序，调用输出文件：

```orca
orca_mapspc Test-Freq-H2CO.out ir -w25
```

或者调用 Hessian 文件：

```orca
orca_mapspc Test-Freq-H2CO.hess ir -w25
```

`orca_mapspc` 的基本选项如下：

```orca
-w  : a value for the linewidth (gaussian shape, fwhm)
-x0 : start value of the spectrum in cm**-1
-x1 : end value of the spectrum in cm**-1
-n  : number of points to use
```

要查看详细选项，可不带输入调用 `orca_mapspc`。
上述对 H$_2$CO 分子的 `orca_mapspc` 运行提供了
`Test-NumFreq-H2CO.out.ir.dat` 文件，其中包含强度和
波数两列。因此，该文件可作为任何绘图程序的输入。
由上述 ORCA 运行得到的 H$_2$CO 分子计算 IR 谱
如图 [fig:637](#fig:637) 所示。

<a id="fig:637"></a>
!!! note "../../images/637.*"
    使用 `orca_mapspc` 工具生成的文件绘制的 H$_2$CO 分子预测 IR 谱。

<a id="sec:spectroscopyproperties.vib.nearir"></a>
## 通过 NEARIR 计算倍频、组合频与近红外光谱（Overtones, Combination Bands and Near IR Spectra via NEARIR）

为完整起见，倍频和组合频也可以纳入计算的 IR 或近红外光谱中。
这些谱带的强度强烈依赖于非谐效应。ORCA 可以通过 VPT2 方法
[Bloino2014](../../bibliography.md) 包含这些效应。
完整的三次力场、倍频和组合频的非谐修正，以及多种方法都可在
`orca_vpt2` 模块中使用（见章节 [spectroscopyproperties.vpt2](#sec:spectroscopyproperties.vpt2)）。

特别是，`NEARIR` 关键词调用一种更简单的半对角方法，
仅包含两个模式（$i$ 和 $j$，在 [yagi_ab_2004,barnes_fast_2016](../../bibliography.md) 中也称为 2MR-QFF）
以及最高到三次阶的力常数（$k_{iij}$、$k_{iji}$ 和 $k_{iii}$）。
目前，只有强度对非谐效应进行了修正——**频率没有。**

### 倍频与组合频（Overtones and Combination Bands）

由于这些项的计算随 $N_{modes}^2$ 标度增长，很快就会变得过于昂贵，
因此我们默认使用半经验的 GFN2-xTB[grimme2017xtb](../../bibliography.md) 来计算
高阶导数所需的能量和偶极矩（之后可以更改）。
要请求此功能，只需在主输入中添加 `!NEARIR`。下面是一个示例输入，
使用 B2PLYP 双杂化泛函计算甲苯的基频，并使用 XTB 计算非谐项：

```orcainput
! TightOPT NumFREQ RI-B2PLYP def2-TZVP def2-TZVP/C RIJCOSX NEARIR
 
*xyzfile 0 1 toluene.xyz
```

!!! note
    这些非谐修正对几何结构非常敏感。因此，
    只要可能，请进行保守的几何优化（至少 `TightOPT`）。

在输出中，首先打印常规 IR 谱的特征。
然后，倍频和组合频的特征以与基频类似的方式给出，如下所示：

```orca
-------------------------------
OVERTONES AND COMBINATION BANDS
-------------------------------

Mode      freq       eps       Int      T**2        TX        TY        TZ
         cm**-1   L/(mol*cm)  km/mol    a.u.
------------------------------------------------------------------------------
6+6:      64.71    0.000994    5.02   0.004792  (-0.009428 -0.066232  0.017796)
6+7:      241.83   0.000022    0.11   0.000028  (-0.005268  0.000255  0.000638)
6+8:      375.36   0.000048    0.24   0.000040  (-0.000740  0.001917  0.006007)
6+9:      442.49   0.000000    0.00   0.000000  ( 0.000010  0.000001  0.000001)
6+10:     506.37   0.000003    0.01   0.000002  ( 0.001078 -0.000061  0.000799)
(...)
```

"Mode" 列显示倍频（如 6+6）和组合频（如 6+7 和 6+8）。
当用 `orca_mapspc` 实用程序调用输出文件时，这些新量会被
自动检测并纳入 IR 谱：

```orca
orca_mapspc toluene-nearir.out ir -w25
```

由 `orca_mapspc` 提供的文件，可以绘制 IR 谱，
如图 [fig:nearir_toluene](#fig:nearir_toluene) 所示。

<a id="fig:nearir_toluene"></a>
!!! note "../../images/nearir_toluene.*"
    气相甲苯的计算与实验红外光谱。
    红色曲线仅包含基频，蓝色曲线
    还包含倍频和组合频。灰色虚线是
    从 NIST 数据库获得的实验气相光谱。理论频率
    按照文献值 [keshfreq2015](../../bibliography.md) 进行了标度。

计算光谱中恢复了"苯指纹"（"Benzene fingers"），
即环的倍频和组合频。请注意，频率是按照文献值[keshfreq2015](../../bibliography.md) 标度的，
尚未使用 VPT2 进行修正。

### 近红外光谱（Near IR Spectra）

让我们模拟 CCl$_4$ 中甲醇的近红外光谱，如 Bec 和 Huck
[bec_breakthrough_2019](../../bibliography.md) 所发表的那样，使用 B3LYP 计算基频、
XTB 计算倍频、CPCM 处理溶剂化。输入如下：

```mol
title: structure 2
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
6
structure (0 1)
O       0.39517      4.38840     -0.00683
C      -0.50818      3.29837      0.00221
H      -0.11943      5.18771      0.19752
H       0.03977      2.38083     -0.22470
H      -1.27919      3.45664     -0.75583
H      -0.96616      3.21170      0.99058
--- input ---
! TightOPT FREQ B3LYP def2-TZVP RIJCOSX NEARIR CPCM(CCl4)

*xyz 0 1
 O      0.39517      4.38840     -0.00683
 C     -0.50818      3.29837      0.00221
 H     -0.11943      5.18771      0.19752
 H      0.03977      2.38083     -0.22470
 H     -1.27919      3.45664     -0.75583
 H     -0.96616      3.21170      0.99058
*
```

通过将终点设为约 8000 cm$^{-1}$ 用 `orca_mapspc` 调用输出，
以便将光谱扩展到近红外区域，即

```orca
orca_mapspc toluene-nearir.out ir -w25 -x18000
```

即可从生成的 "toluene-nearir.dat" 文件模拟光谱。
如图 [fig:nearir_methanol](#fig:nearir_methanol) 所示，使用按照 [keshfreq2015](../../bibliography.md)
标度的计算频率（尚未使用 VPT2 修正）绘制的计算光谱与实验光谱
符合得相当好。

<a id="fig:nearir_methanol"></a>
*CCl$_4$ 中甲醇的计算与实验近红外光谱。
蓝色曲线为倍频；红色曲线为组合频；
灰色虚线为实验光谱。理论频率按照文献值[keshfreq2015](../../bibliography.md) 进行了标度。*

### 使用其他方法进行 VPT2 修正（Using Other Methods for the VPT2 Correction）

要用计算基频所选的方法计算倍频，只需将 `%freq` 块中的 `XTBVPT2`
选项设为 false，即

```orca
%freq XTBVPT2 False end
```

要为倍频和组合频的计算设置与基频计算不同的方法，需要先进行频率计算，
然后在 `%geom` 块中调用所得的 Hessian 文件，并激活 `PRINTTHERMOCHEM` 标志
（详见章节 [structurereactivity.thermochemistry](#sec:structurereactivity.thermochemistry)），即

```orca
! BP86 def2-TZVP NEARIR CPCM(CCl4) PRINTTHERMOCHEM

%geom INHESSNAME "methanol.hess" end
%freq XTBVPT2 False end

*xyzfile 0 1 methanol_opt.xyz
```

在这个例子中，基频模式从 "methanol.hess" 文件读取，
但倍频和组合频的非谐项与强度则使用 BP86 计算。
任何方法组合都是允许的，例如 B3LYP/BP86 和 B2PLYP/AM1。
请注意，本描述是完整 VPT2 或 GVPT2 的近似。更完整的处理见
章节 [spectroscopyproperties.vpt2](#sec:spectroscopyproperties.vpt2) 中描述的 VPT2 模块。

默认情况下，数值计算中使用无量纲简正模式单位下 0.5 的步长。
这可以通过在 `%freq` 块中设置 `DELQ` 来更改：

```orca
%freq
    XTBVPT2 False
    DELQ    0.1
end
```

与 VPT2 及一般频率计算相关的完整选项列表见
Sec. [structurereactivity.frequencies](#sec:structurereactivity.frequencies)。

<a id="sec:spectroscopyproperties.vcd.typical"></a>
## 振动圆二色（VCD）光谱（Vibrational Circular Dichroism (VCD) Spectra）

振动圆二色光谱计算在 SCF（HF 或 DFT）水平上解析实现，
遵循 Weigend 及其合作者的推导[Reiter2017](../../bibliography.md)。
基本用法见以下示例：

```mol
title: structure 3
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
4
structure (0 1)
O      0.000000     0.000000     0.611880
C      0.000000     0.000000    -0.596849
H      0.952616     0.000000    -1.209311
H     -0.952616     0.000000    -1.209311
--- input ---
! OPT FREQ BP86 def2-SVP

*xyz 0 1
 O    0.000000    0.000000    0.611880
 C    0.000000    0.000000   -0.596849
 H    0.952616    0.000000   -1.209311
 H   -0.952616    0.000000   -1.209311
*
```

请注意，除 Hessian 外，VCD 计算还需要使用 GIAO 的磁场响应
以及场原点置于 (0,0,0) 的电场响应。
后者与 GIAO 情形下硬编码的磁场规范原点一致，
对于确保结果的规范不变性是必要的。
ORCA 会自动完成所有这些工作，但这意味着如果在同一任务中同时
请求 VCD 和电性质和/或磁性质，则无法更改场原点。

影响 VCD 计算的其他关键词包括
`%eprnmr` 中的 `GIAO_1el` 和 `GIAO_2el` 以及 `%freq` 中的 `CutOffFreq`。
另请注意，VCD 不能与 `NumFreq` 一起计算。

<a id="sec:spectroscopyproperties.vib.raman"></a>
## 拉曼光谱（Raman Spectra）

从 ORCA 6.1 开始，拉曼强度计算已通过极化率张量的解析几何导数
实现，现在与 SCF 方法（HF、DFT）的解析频率计算兼容。
如果频率计算（`!Freq`）与极化率计算相结合，拉曼光谱将被自动计算。

考虑以下示例：

```mol
title: structure 4
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
4
structure (0 1)
C      0.000000     0.000000    -0.533905
O      0.000000     0.000000     0.682807
H      0.000000     0.926563    -1.129511
H      0.000000    -0.926563    -1.129511
--- input ---
! OPT RHF STO-3G TightSCF SmallPrint Freq

%elprop Polar 1 end

*xyz 0 1
 C    0.000000    0.000000   -0.533905
 O    0.000000    0.000000    0.682807
 H    0.000000    0.926563   -1.129511
 H    0.000000   -0.926563   -1.129511
*
```

输出给出每个模式的拉曼散射活性（单位为 ${\text{Å}}^4$/AMU）[Neugebauer2002](../../bibliography.md)
和拉曼退偏比：

```orca
--------------
RAMAN SPECTRUM
--------------

 Mode    freq (cm**-1)   Activity   Depolarization
-------------------------------------------------------------------
   6:      1278.43      0.007371      0.750000
   7:      1397.30      3.043852      0.750000
   8:      1767.07     16.391442      0.707250
   9:      2099.28      6.704492      0.075590
  10:      3498.60     38.681286      0.186510
  11:      3645.53     24.527417      0.750000
```

ORCA 运行还会生成一个包含极化率导数和拉曼活性的 `.hess` 文件。
同位素取代对拉曼活性的影响可以使用该 `.hess` 文件计算。

与 IR 谱情形类似，`orca_mapspc` 提供一个 `.dat` 文件
用于绘制计算的拉曼光谱：

```orca
orca_mapspc Test-NumFreq-H2CO.out raman -w50
```

使用相应 `.dat` 文件绘制的 H$_2$CO 拉曼光谱
如图 [fig:638](#fig:638) 所示。

<a id="fig:638"></a>
!!! note "../../images/638.*"
    在 STO-3G 水平上计算的 H$_2$CO 拉曼光谱，使用
    `orca_mapspc` 工具从数值频率和拉曼活性生成的 `.dat` 文件绘制。

值得注意的是，每个模式 $i$ 的拉曼散射活性 $S_i$ 与相应模式的
拉曼强度 $I_i$ 有关但并不直接相等，后者依赖于拉曼测量中所用
激光的激发线 $\nu_0$（对于 Nd:YAG 激光器：$\nu_0$ = 1064 nm = 9398.5 cm$^{-1}$）。
为获得实验与模拟拉曼光谱之间显著更好的符合，
每个模式的 $I_i$ 需要用以下公式计算：

$$
I_i = \frac{f(\nu_0 - \nu_i)^4 S_i}{\nu_i [1 - \exp(-h c \nu_i / k T)]}
$$

其中 $f$ 是所有模式共有的归一化常数；$h$、$c$、$k$ 和 $T$ 分别是
普朗克常数、光速、玻尔兹曼常数和温度。

!!! note
    -   如果指定 `!NumFreq` 和 `%elprop polar 1 end` 的组合，
        仍然可以使用解析极化率的数值导数计算拉曼强度。
        这是目前动力学极化率导数的唯一选项。在静态极化率情形下，
        这种方式效率明显更低，并且需要比解析导数更严格的精度设置。

    -   解析拉曼强度计算也已针对隐式溶剂化实现，
        例如在简单输入中使用 `!CPCM(solvent)` 指定。

    -   解析拉曼强度在 SCF 中使用 RI-J 和/或 COSX 近似时会利用这些近似。
        需要提醒的是，我们观察到，如果使用带弥散函数的基组
        （例如 `def2-SVPD`），默认辅助基下 RI-J 近似的误差可能会变大。

<a id="sec:spectroscopyproperties.vib.resonanceraman"></a>
## 共振拉曼光谱（Resonance Raman Spectra）

共振拉曼光谱（NRVS）和激发剖面可以使用
[spectroscopyproperties.asa](#sec:spectroscopyproperties.asa) 中描述的程序进行预测或拟合。
获取必要 orca_asa 输入的示例见
章节 [asa.bandshapes](#sec:spectroscopyproperties.asa.bandshapes)。

<a id="sec:spectroscopyproperties.vib.nrvs"></a>
## NRVS 光谱（NRVS Spectra）

NRVS 光谱的理论和实现细节见参考文献
[petrenko2007hyperfine,debeer2007vibrational](../../bibliography.md)。
*含铁分子*的 NRVS 光谱可以简单地通过用 `orca_vib` 实用程序
调用先前频率计算的 `.hess` 文件来计算。该实用程序的输出文件
随后可以用 `orca_mapspc` 实用程序调用，生成用于绘图的 `.dat` 文件：

```orca
orca_vib MyJob.hess > MyJob.vib.out
orca_mapspc MyJob.vib.out NRVS
```

对于铁(III)-叠氮配合物[petrenko2007hyperfine](../../bibliography.md)，
计算和实验 NRVS 光谱见图 [fig:639](#fig:639)。

<a id="fig:639"></a>
!!! note "../../images/639.*"
    在 BP86/TZVP 水平（T $=$ 20 K）得到的 Fe(III)-叠氮配合物的
    实验（a，黑色曲线）、拟合（a，红色）和模拟（b）NRVS 光谱。
    柱状图表示各个振动跃迁的相应强度。
    蓝色曲线表示去除背景线后的拟合光谱。

与 [spectroscopyproperties.asa](#sec:spectroscopyproperties.asa) 中描述的共振拉曼光谱计算类似，
DFT 估计通常是进行最小二乘精修的优秀起点。

下面我们描述在 ${\text{Fe(SH)}}_{4}^{1-}$ 配合物上使用 BP86 泛函
计算此类 NRVS 光谱的过程，该泛函通常能提供良好的 NRVS 光谱。
首先需要优化配合物的几何结构并计算其振动结构：

```mol
title: structure 5
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
9
structure (-1 6)
Fe    -0.115452     0.019090    -0.059506
S     -0.115452     1.781846     1.465006
S     -0.115452    -1.743665     1.462801
S     -1.908178    -0.072782    -1.518702
S      1.560523     0.154286    -1.656664
H      0.410700     2.760449     0.687716
H     -0.674147    -2.708278     0.690223
H     -2.905212     0.345589    -0.699907
H      2.647892    -0.211681    -0.932926
--- input ---
! OPT FREQ BP86 def2-TZVP TightSCF SmallPrint
 
*xyz -1 6
 Fe     -0.115452      0.019090     -0.059506
 S      -0.115452      1.781846      1.465006
 S      -0.115452     -1.743665      1.462801
 S      -1.908178     -0.072782     -1.518702
 S       1.560523      0.154286     -1.656664
 H       0.410700      2.760449      0.687716
 H      -0.674147     -2.708278      0.690223
 H      -2.905212      0.345589     -0.699907
 H       2.647892     -0.211681     -0.932926
*
```

现在在该任务生成的 `.hess` 文件上运行 `orca_vib` 实用程序，
以获得可与 `orca_mapspc` 实用程序一起使用的输出文件：

```orca
orca_vib Test-FeIIISH4-NumFreq.hess > Test-FeIIISH4-NumFreq.out
orca_mapspc Test-FeIIISH4-NumFreq.out NRVS
```

该 `orca_mapspc` 运行生成 xy 格式的
`Test-FeIIISH4-NumFreq.nrvs.dat` 文件。
该文件包含声子能量（$x$，单位 cm$^{-1}$）
和 NRVS 强度（$y$，原子单位），因此可以直接用于
可视化光谱。

相应的 NRVS 光谱见图 [fig:639_1](#fig:639_1)，
并附有同一频率标度下的计算 IR 光谱。
NRVS 报告的是由于声子（振动）共振散射引起的 Mössbauer 信号多普勒展宽，
这些振动主要由 Fe 核运动主导。这是对 IR 光谱的宝贵补充，
因为在 IR 光谱中这些模式的强度非常小。

<a id="fig:639_1"></a>
!!! note "../../images/639_1.*"
    (a) ${\text{Fe(SH)}}_{4}^{1-}$ 的理论 IR 谱以及峰值附近
    最高强度模式的箭头图。(b) 相应的 NRVS 散射光谱。

<a id="sec:spectroscopyproperties.vib.animation"></a>
## 振动模式的动画（Animation of Vibrational Modes）

为说明如何制作振动模式的动画并生成其"箭头图"，
让我们对 H$_2$CO 进行频率计算：

```orca
-----------
IR SPECTRUM
-----------

 Mode   freq       eps      Int      T**2         TX        TY        TZ
       cm**-1   L/(mol*cm) km/mol    a.u.
----------------------------------------------------------------------------
  6:   1146.68   0.000341    1.73  0.000093  (-0.000000 -0.009640  0.000000)
  7:   1224.67   0.002004   10.13  0.000511  ( 0.022596  0.000000  0.000000)
  8:   1485.77   0.001002    5.07  0.000211  ( 0.000000 -0.000000  0.014510)
  9:   1806.49   0.020286  102.51  0.003504  ( 0.000000 -0.000000  0.059197)
 10:   2769.13   0.014010   70.80  0.001579  ( 0.000000  0.000000  0.039734)
 11:   2812.52   0.039321  198.71  0.004363  ( 0.066052 -0.000000 -0.000000)
```

该任务的输出给出振动特征：

```orca
Mode      freq       eps       Int    T**2         TX        TY        TZ
         cm**-1   L/(mol*cm) km/mol    a.u.
----------------------------------------------------------------------------
6:       1278.37   0.001222    6.18  0.000298  (-0.017272  0.000000  0.000000)
7:       1397.26   0.005844   29.53  0.001305  ( 0.000000  0.036128  0.000000)
8:       1767.02   0.000828    4.18  0.000146  (-0.000000  0.000000 -0.012089)
9:       2099.24   0.001668    8.43  0.000248  ( 0.000000 -0.000000  0.015749)
10:      3498.54   0.000356    1.80  0.000032  ( 0.000000 -0.000000 -0.005636)
11:      3645.47   0.003922   19.82  0.000336  (-0.000000  0.018322  0.000000)
```

该输出可以直接用 `ChemCraft` 打开，以可视化 H$_2$CO 的简正模式
并提取表示原子核运动方向的箭头图，如图 [fig:VibModes](#fig:VibModes) 所示。
例如，从该图可以推断 1397 cm$^{-1}$ 模式对应于摇摆振动。

<a id="fig:VibModes"></a>
!!! note "../../images/VibModes.*"
    H$_2$CO 的简正模式，箭头指示原子核运动的大小和方向，
    以及从 `ORCA` 输出文件通过 `ChemCraft` 得到的相应振动频率（cm$^{-1}$）。

为了使用 `gOpenMol` 等免费程序包制作振动模式的动画
并创建其"箭头图"，可以使用小程序 `orca_pltvib`。
该实用程序从频率运行的 ORCA 输出文件生成一系列文件，
可以用分子可视化程序打开。`orca_pltvib` 的用法如下：

```orca
orca_pltvib Test-FREQ-H2CO.out [list of vibrations or all]
```

例如，让我们为标记为 7 的 1397 cm$^{-1}$ 模式制作动画：

```orca
orca_pltvib Test-FREQ-H2CO.out 7
```

该调用将生成 `Test-FREQ-H2CO.out.v007.xyz` 文件。
打开 `gOpenMol` 并以 `Xmol` 格式读取该文件（`Import->coords`）。
然后，进入 `Trajectory->Main` 菜单，再次以 `Xmol` 格式导入该文件。
现在您就可以播放该模式的动画了。要生成可打印的图片，
按 `Dismiss`，然后在 gOpenMol 命令行窗口中键入
`lulVectorDemo {4 0.1 black}`。
生成的图片（见图 [fig:640](#fig:640)）表明
该模式对应于摇摆振动。

<a id="fig:640"></a>
!!! note "../../images/640.*"
    H$_2$CO 分子的 1397 cm$^{-1}$ 模式，由 `ORCA` 到 `gOpenMol`
    的接口和 `orca_pltvib` 工具创建的动画文件得到。

箭头的外观也可以按照 `gOpenMol` 的网络教程进行修改。

<a id="sec:spectroscopyproperties.vib.isotopeshifts"></a>
## 同位素位移（Isotope Shifts）

计算得到的同位素位移极大地有助于振动的归属、
实验的解释以及对计算所得振动简正模式可靠性的评估。
为研究同位素位移而重新计算 Hessian 是非常糟糕的做法，
因为 Hessian 计算通常很昂贵，而 Hessian 本身与质量无关。
下面我们描述如何在不重新计算 Hessian 的情况下考察同位素效应。

假设您已经按照上面讨论的示例计算了 Hessian，
并且想要预测 $^{18}$O 取代的影响。
在这种情况下，您可以使用小程序 `orca_vib`。
首先需要手动编辑 `.hess` 文件中给出的质量。
对于上面给出的示例，`.hess` 文件如下：

```orca
$orca_hessian_file
......................
$hessian
12
... the cartesian Hessian in Eh/bohr**"

$vibrational_frequencies
12

...the vibrational frequencies (in cm-1) as in the output

$normal_modes
12 12
... the vibrational normal modes in Cartesian displacements
#
# The atoms: label  mass x  y  z
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#   Here we have changed 15.999 for oxygen into
#   18.0  in order to see the oxygen 18 effects
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
$atoms
4
 C     12.0110      0.000000     0.000000    -1.149571
 O     18.0000     -0.000000    -0.000000     1.149695
 H      1.0080     -0.000000     1.750696    -2.275041
 H      1.0080     -0.000000    -1.750696    -2.275041

$actual_temperature
  0.000000

$dipole_derivatives
12

... the dipole derivatives (Cartesian displacements)
#
# The IR spectrum
#  wavenumber T**2 TX TY  TY
#
$ir_spectrum
12
... the IR intensities
```

按照上面所示将 O 的质量从 15.999 改为 18.0 后，让我们调用：

```orca
orca_vib Test-FREQ-H2CO.hess
```

这将重新计算存在 $^{18}$O 时的振动频率。
让我们将本次运行输出中的振动频率与
原始频率（单位 cm$^{-1}$）进行比较：

```orca
  Mode       H2C16O    H2CO18O    Shift
----------------------------------------- 
   6:        1284.36   1282.82    -1.54
   7:        1397.40   1391.74    -5.66
   8:        1766.60   1751.62   -14.98
   9:        2099.20   2061.49   -37.71
  10:        3499.11   3499.02    -0.09
  11:        3645.24   3645.24     0.00
```

分析同位素位移的另一种方法是绘制两个预测光谱，
然后将一个从另一个中相减。这将产生具有导数形状的峰，
其过零点位于对同位素敏感的模式处。

!!! note
    在存在点电荷和/或外电场的情况下，
    体系的平移和转动对称性可能会被破坏。
    在这种情况下，您可能不希望从 Hessian 中投影掉平移和
    转动自由度。这可以通过以下方式实现：

    ```orca
    orca_vib Test-FREQ-H2CO.hess -noproj
    ```

[^1]: Neugbauer [Neugebauer2002](../../bibliography.md) 有更详细的解释
