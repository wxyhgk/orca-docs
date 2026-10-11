<a id="sec:spectroscopyproperties.asa"></a>
# 用 orca_asa 程序模拟和拟合电子谱中的振动结构、共振拉曼激发轮廓与谱图（Simulation and Fit of Vibronic Structure in Electronic Spectra, Resonance Raman Excitation Profiles and Spectra with the orca_asa Program） 

!!! note "自 ORCA 6.0.0 起已弃用"
    :class: warning
    - `orca_asa` 程序不再受支持。
      它仍包含在 6.0.0 发行版中，文档保存如下。
      但它可能无法正常工作，并将在未来的 ORCA 版本中被移除！
    - `!NMScan` 和 `!NMGrad` 关键词仍可用，但这些计算可能
      失败或无法为 `orca_asa` 生成有效输入。
      若适用，请改用 [ESD 模块](#sec:spectroscopyproperties.esd)。

本节讨论光谱（包括吸收、荧光和共振拉曼）模拟与拟合的各个方面。
ORCA 的这一部分相当独立，也可用于数据分析语境，
而不仅限于"量子化学"模式。该程序名为 `orca_asa`，
其中 ASA 代表
"[A]{.underline}dvanced [ S]{.underline}pectral [
A]{.underline}nalysis"（高级光谱分析）。该程序完全由 Taras
Petrenko 博士设计。

总体思路如下：一次 ORCA 运行产生喂入 `orca_asa` 程序所需的必要数据，
并写出一个初始输入文件。该输入文件可用于直接运行 `orca_asa`
以预测吸收、荧光或共振拉曼谱。也可以编辑该输入文件
以更改模拟中使用的参数。最后——但绝非最不重要——
`orca_asa` 程序可用于对模型参数进行相对实验数据的拟合。

<a id="fig:714"></a>
*:height: 400px*

下面所有例子均取自 [petrenko2007analysis](../../bibliography.md)，
若您使用 `orca_asa` 程序进行任何工作，必须引用该文献！

<a id="sec:spectroscopyproperties.asa.general"></a>
## 程序的一般描述（General Description of the Program）

程序输入包含以下信息：(1) 模型以及刻画分子电子结构的模型参数
和线型因子的说明；(2) 模拟的光谱范围和分辨率；
(3) 用于 rR 激发轮廓和谱图生成的振动跃迁说明；
(4) 依模型而定的若干算法选择选项；(5) 拟合选项。

所有可选参数 (1)–(3) 都在 `%sim` 块中给出，
拟合选项在 `%fit` 块中。模型参数在下文描述的各个块中指定。
程序 `orca_asa` 与 ORCA 相接口，并沿用其输入风格。
`orca_asa` 运行的输入也可在 ORCA 运行时生成。

当前实现提供所谓的"简单"（simple）、"独立模位移简谐振子"
（independent mode, displaced harmonic oscillator, IMDHO）
以及"含频率改变的独立模位移简谐振子"
（independent mode, displaced harmonic oscillator with frequency alteration, IMDHOFA）模型。

<a id="sec:spectroscopyproperties.asa.input"></a>
## 光谱模拟流程：输入结构与模型参数（Spectral Simulation Procedures: Input Structure and Model Parameters）

<a id="sec:spectroscopyproperties.asa.input.simple"></a>
### 示例：简单模式（Example: Simple Mode）

该模型代表最简单的方法，通常用于吸收谱分析。
它忽略电子跃迁的振动结构，并用标准线型——通常是高斯、
洛伦兹或混合（Voigt）函数——近似每一条电子谱带。
只有当电子谱中振动精细结构未被分辨时，该模型才有意义。
在此近似下，吸收谱强度取决于入射光子能量（$E_{L} )$、
电子跃迁能（$E_{T} )$、跃迁电偶极矩
（$\mathrm{\mathbf{M} }$，在基态平衡几何处计算）。
线型因子由均匀线宽 $\Gamma$ 和对应于跃迁能高斯分布的
标准差参数 $\sigma$ 指定。下例说明了使用不同强度和线型参数
模拟吸收带形的一个简单输入。

```orca
# example001.inp
#
# Input file to generate absorption spectrum consisting
# of 3 bands   with different lineshape factors:
#
# 1. Lorentzian centered at 18000cm**-1 (damping factor Gamma= 100 cm**-1)
# 2. Gaussian   centered at 20000cm**-1
#    (standard deviation Sigma= 100 cm**-1)
# 3. Mixed Gaussian-Lorentzian band representing Voigt profile
#    centered at 21000 cm**-1

%sim
         Model Simple

         # Spectral range for absorption simulation:
         AbsRange     17000.0,   23000.0

         # Number of points to simulate absorption spectrum:
         NAbsPoints  2000

end

#---------------------------------------------------------------------------
#  Transition        Gamma    Sigma  Transition Dipole Moment (atomic unit)
#  Energy (cm**-1)  (cm**-1) (cm**-1)      Mx          My        Mz
#---------------------------------------------------------------------------

$el_states
3     # number of electronic states
   1  18000.0        100.00      0.0        1.0         0.0       0.0
   2  20000.0          0.00    100.0        1.0         0.0       0.0
   3  22000.0         50.00     50.0        1.0         0.0       0.0
```

由各跃迁到达的末态电子态参数在 `$el_states` 块中指定。
计算中使用的光谱范围和分辨率由 `%sim` 块中的
`AbsRange` 和 `NAbsPoints` 关键词定义。
若 `NAbsPoints>1`，将自动调用吸收谱计算。
`orca_asa` 运行结束后，您会在目录中找到文件
`example001.abs.dat`，它以简单的两列 ASCII 格式包含吸收谱，
适合用任何电子表格程序绘图。与各个电子跃迁对应的吸收谱
存储在文件 `example001.abs.as.dat` 中（后缀 "`as`"
代表 "All States"，即所有态）。

<a id="fig:715"></a>
*对文件 `example001.inp.` 运行 orca_asa 后生成的吸收谱。
三条谱带具有不同的线型参数。
请注意，尽管所有跃迁都具有相同的跃迁电偶极矩，
它们的强度却按跃迁能成比例缩放。*

程序运行的输出还包含每个电子谱带对应的振子强度
和半高全宽（FWHM）参数：

```orca
----------------------------------------------
   State       EV        fosc    Stokes shift
            (cm**-1)               (cm**-1)
----------------------------------------------
    1:      18000.00   0.054676      0.00
    2:      20000.00   0.060751      0.00
    3:      22000.00   0.066826      0.00

----------------------------------------
   BROADENING PARAMETETRS (cm**-1)
----------------------------------------
   State     Gamma     Sigma      FWHM
----------------------------------------
    1:        100.00      0.00    200.00
    2:          0.00    100.00    235.48
    3:         50.00     50.00    180.07
```

请注意，尽管三种线型函数都是对称的，
单条吸收带的整体形状却并非如此，
因为消光系数（吸收截面）也与入射光子能量成正比。
因此，若线宽大于峰位能量的 10%，电子谱带的不对称性可能相当明显。

<a id="sec:spectroscopyproperties.asa.input.imdho"></a>
### 示例：IMDHO 模型中吸收与荧光谱的建模（Example: Modelling of Absorption and Fluorescence Spectra within the IMDHO Model）

IMDHO 模型是最简单的方法，能成功预测大量真实体系
电子谱中的振动结构以及 rR 强度。该模型假设：

1.  基态和激发态势能面为简谐的；

2.  激发态势能面相对基态势能面发生原点位移；

3.  激发态中不发生振动频率改变或简正模旋转；

4.  电子跃迁偶极矩不依赖于坐标。

除了上文"简单模型"中引入的参数外，它还需要关于振动自由度的信息。
所需信息包括基态振动频率 $\left\{{ \omega_{gm} } 
ight\}$ 和
（无量纲）原点位移 $\left\{{ \Delta_{mi} } 
ight\}$，
其中 $i$ 和 $m$ 分别指电子态和简正模。
$\Delta$ 以无量纲简正坐标表示。
因此，对 IMDHO 模型需要指定以下各块

-   `$el_states` 块包含每个电子态的参数
    $E_{T}, \Gamma, \sigma, \mathrm{\mathbf{M} }$。
    默认假定 $E_{T}$ 为绝热极小分离能。
    也可以将其重定义为垂直跃迁能。这通过在 `%sim` 块中
    指定关键词 `EnInput=EV` 实现。

-   `$vib_freq_gs` 块指定基态振动频率。

-   `$sdnc` 块以矩阵形式包含参数
    $\left\{{ \Delta_{mi} } 
ight\}$，使得第 $i$ 列表示
    第 $i$ 个激发态势能面沿所有简正模的无量纲位移。

文件 `example002.inp` 提供了对一个沿 5 个简正坐标具有显著
激发态原点位移的体系模拟吸收和荧光谱的输入。

```orca
# example002.inp
#
# Input file for simulation  of vibrational structure
# in absorption and fluorescence spectra assuming
# origin shift of excited PES along 5 normal coordinates.
# The simulated spectra closely reproduce the experimental
# optical bandshapes for the tetracene molecule.
#
%sim
     Model IMDHO

     # spectral range for absorption simulation (cm**-1)
     AbsRange    20000.0, 27000.0
     NAbsPoints  2000             # number of points in absorption spectrum

     # spectral range for simulation of fluorescence (cm**-1)
     FlRange     22000.0, 16000.0
     NFlPoints   2000      # number of points in fluorescence spectrum

     # the following options require the spectra to be normalized
     # so that their maxima are equal to 1.0
     AbsScaleMode Rel
     FlScaleMode  Rel   # default  for fluorescence

     # for absorption spectrum the default option is AbsScaleMode= Ext
     # which stands for extinction coefficient

end

#---------------------------------------------------------------------------
#   Transition        Gamma    Sigma  Transition Dipole Moment (atomic unit)
#   Energy (cm**-1)  (cm**-1) (cm**-1)      Mx          My          Mz
#---------------------------------------------------------------------------

$el_states
1
   1  21140.0         50.00    100.0        1.0         0.0         0.0

# Block specifying Stokes Shift parameter for each electronic state
# This information is optional
$ss
1   # number of excited states
  1   300.0      # the Stokes shift for the 1st electronic transition

# Block providing the values of VIBrational FREQuencies
# for 5 Ground-State normal modes.
# Obligatory for IMDHO and IMDHOFA models.
$vib_freq_gs
5
    1      310.0
    2     1193.0
    3     1386.0
    4     1500.0
    5     1530.0

# Block specifying origin Shift of the excite-state PES
# along each normal mode in terms of the ground-state
# Dimensionless Normal Coordinates
# Obligatory for IMDHO and IMDHOFA models.
$sdnc
5 1
               1
     1       0.698
     2      -0.574
     3       0.932
     4      -0.692
     5       0.561
```

若参数 `NAbsPoints>1` 和 `NFlPoints> 1`，将自动调用吸收和荧光谱的计算。
输入文件还包含可选块 `$ss `，它为每个电子跃迁指定 Stokes 位移
$\lambda$。该参数等于吸收谱和荧光谱中 0-0 振动峰之间的能量差，
如 [fig:716](#fig:716) 所示。一般而言，$\lambda$ 包含溶剂诱导效应
以及输入中未指定的低频模对应的未分辨振动结构。
请注意，我们在 `%sim` 块中指定了参数
`AbsScaleMode=Rel` 和 `FlScaleMode=Rel`，
以确保模拟谱归一化为 1。计算得到的吸收谱和荧光谱
分别存储在 `example002.abs.dat` 和 `example002.fl.dat` 文件中。

<a id="fig:716"></a>
*对文件 `example002.inp.` 运行 `orca_asa` 后生成的吸收谱和荧光谱。
若均匀展宽设为 $\Gamma = 10 \, \text{cm}^{-1}$，
可以分辨出隐含的振动精细结构。*

<a id="sec:spectroscopyproperties.asa.input.imdhofa"></a>
### 示例：IMDHOFA 模型中吸收与荧光谱的建模（Example: Modelling of Absorption and Fluorescence Spectra within the IMDHOFA Model）

IMDHOFA（含频率改变的独立模位移简谐振子，
Independent Mode Displaced Harmonic Oscillators with Frequency
Alteration）基于与 IMDHO 模型相同的假设，
只是激发态中可以发生振动频率改变。
文件 `example003.inp` 的输入参数与 `example002.inp` 几乎相同。
IMDHOFA 模型通过 `%sim` 块中的关键词 `Model=IMDHOFA` 调用。
此外，必须提供必需块 `$vib_freq_es`。
它以矩阵形式包含激发态振动频率 $\left\{{ \omega_{emi} } 
ight\}$，
使得第 $i$ 列表示第 $i$ 个激发态势能面所有简正模的振动频率。

```orca
# Block providing the values of VIBrational FREQuencies
# for 5 Excited-State normal modes.
# Obligatory for IMDHOFA model.

$vib_freq_es
5  1         # number of modes and number of excited states
             1
    1      410.0
    2     1293.0
    3     1400.0
    4     1600.0
    5     1730.0
```

<a id="fig:717"></a>
*对文件 `example003.inp` 运行 `orca_asa` 后生成的吸收谱和荧光谱。
图中还给出了对应于均匀展宽 $\Gamma = 10 \, \text{cm}^{-1}$ 的高分辨谱。*

<a id="sec:spectroscopyproperties.asa.input.paraimdho"></a>
### 示例：IMDHO 模型中有效展宽、有效 Stokes 位移和温度效应的建模（Example: Modelling of Effective Broadening, Effective Stokes Shift and Temperature Effects in Absorption and Fluorescence Spectra within the IMDHO Model）

对于 IMDHO 模型，`orca_asa` 能够在有限温度近似下对吸收和发射谱建模。
关键词 `Model=IMDHO ` 假设零温近似，
而 `Model=IMDHOT` 的值则调用有限温度下的谱计算，
温度由 `%sim` 块中的参数 `TK` 指定：

```orca
# example004.inp
#
#
%sim
     Model IMDHOT
     TK 300 # temperature (in Kelvin)

     # spectral range for absorption simulation (cm**-1)
     AbsRange    18000.0, 35000.0
     NAbsPoints  5000             # number of points in absorption spectrum

     # spectral range for simulation of fluorescence (cm**-1)
     FlRange     22000.0, 10000.0
     NFlPoints   5000      # number of points in fluorescence spectrum

     # the following options require the spectra to be normalized
     # so that their maxima are equal to 1.0
     AbsScaleMode Rel
     FlScaleMode  Rel   # default  for fluorescence
end

#---------------------------------------------------------------------------
#   Transition        Gamma    Sigma  Transition Dipole Moment (atomic unit)
#   Energy (cm**-1)  (cm**-1) (cm**-1)      Mx          My          Mz
#---------------------------------------------------------------------------

$el_states
1
   1  21140.0         50.00    100.0        1.0         0.0         0.0

# Block specifying Stokes Shift parameter for each electronic state
$ss
1   # number of excited states
  1   300.0      # the Stokes shift for the 1st electronic transition

# Block providing the values of VIBrational FREQuencies
# for 10 Ground-State normal modes.
$vib_freq_gs
10
    1       30.0
    2       80.0
    3       100.0
    4       120.0
    5       130.0
    6      140.0
    7      160.0
    8      200.0
    9      310.0
   10     1300.0

# Block specifying origin Shift of the excite-state PES
# along each normal mode in terms of the ground-state
# Dimensionless Normal Coordinates
$sdnc
 10  1
              1
     1       2.5
     2       2.0
     3       1.8
     4       1.9
     5       1.5
     6       1.9
     7       2.4
     8       1.9
     9       2.5
    10       0.9
```

该例说明了大分子中的典型情形：存在若干低频模，
对给定激发态势能面具有显著的无量纲位移值。
当振动态密度很高、频率低于或接近 FWHM 的本征值
（由 $\Gamma$ 和 $\sigma$ 决定）时，振动精细结构无法分辨，
谱变得非常弥散，吸收谱与发射谱极大值之间出现很大分离
（[fig:717](#fig:717)）。此外，在条件 $h\nu_{i} \leqslant kT$ 下，
谱中有效带宽和极大值位置会强烈受温度效应影响。

<a id="fig:718"></a>
*对文件 `example004.inp` 运行 `orca_asa` 后生成的 T$=$0 K（蓝）
和 T$=$300 K（红）的吸收谱和荧光谱。
黑线表示所有低频模的无量纲位移均设为零时的谱。*

在简单自洽过程中评估得到有效 Stokes 位移和线宽参数，
它们给出在 `orca_asa` 运行的输出中：

```orca
------------------------------------------------------------------------------
State      E0           EV       fosc    Stokes shift  Effective Stokes shift
          (cm**-1)     (cm**-1)              (cm**-1)           (cm**-1)
------------------------------------------------------------------------------
    1:     21140.00   24535.85   0.074529    300.00             7091.70

-------------------------------------------------------------------------------------------
                                BROADENING PARAMETETRS (cm**-1)
-------------------------------------------------------------------------------------------
               Intrinsic                                    Effective
State  --------------------------  --------------------------------------------------------
                                                  Sigma                         FWHM
      Gamma    Sigma    FWHM      ---------------------------   ---------------------------
                                    0K     298.15K   300.00K      0K     298.15K   300.00K
-------------------------------------------------------------------------------------------
 1:  50.00   100.00   293.50     1125.34   1411.13   1413.57   2703.84   3376.75   3382.48
```

请注意，有效参数的评估是相当近似的，
这些值可能与直接从计算谱推得的值有明显偏离。
不过，这类信息通常给出有效振动展宽和 Stokes 位移的正确数量级。
如上面程序输出所示，有效带形以高斯特征为主，
并随温度变化：$\sigma = 1125 \, \text{cm}^{-1}$（$T = 0$ K）和
$\sigma =1414 \, \text{cm}^{-1}$（$T=300$ K）。
的确，如 [fig:719](#fig:719) 所示，在 $T=300$ K 时的吸收谱
可以用 $\sigma = 1388 \, \text{cm}^{-1}$
（FWHM$= 3270 \, \text{cm}^{-1}$）的高斯线型很好地拟合。
可以看到，在更高温度下谱与其高斯拟合之间的偏差变得更小。

在分子中，系综中电子跃迁能的正态分布会使吸收带呈高斯带形。
然而，相应的标准差预计在 100 cm$^{-1}$ 数量级，
因此典型的约 1000 cm$^{-1}$ 的高斯带宽看来源自未分辨的振动精细结构。
一般而言，这一论断得到模型参数量子化学计算的支持。
原则上，有效带宽参数也可用于表征和归属各条电子谱带。

<a id="fig:719"></a>
*对文件 `example004.inp` 运行 `orca_asa` 后生成的 $T=300$ K 吸收谱（蓝）。
红线表示计算谱的高斯拟合。*

<a id="sec:spectroscopyproperties.asa.input.raman1"></a>
### 示例：*反式*-1,3,5-己三烯中 1-$^1$A$_g$ $\rightarrow$ 1-$^1$B$_u$ 跃迁的吸收与共振拉曼谱建模（Example: Modelling of Absorption and Resonance Raman Spectra for the 1-$^1$A$_g$ $\rightarrow$ 1-$^1$B$_u$ Transition in *trans*-1,3,5-Hexatriene）

己三烯分子具有 9 个全对称简正模，它们主导吸收谱中的振动结构，
并在约 40000 cm$^{-1}$ 处强偶极允许的
$1-^{1}A_{g} \rightarrow 1-^{1}B_{u}$ 跃迁对应的 rR 谱中具有活性。
除了忽略激发态中简正模旋转所带来的一些特殊性之外，
IMDHO 模型对光谱的描述相当令人满意。

下例演示了对任意预定数目激发能模拟吸收谱和 rR 谱。

```orca
#
# example005.inp
#
# input for simulation of absorption and resonance Raman spectra
# using experimental values of transition energy and displacement
# parameters corresponding to the strongly allowed 1-1Ag 1-1Bu transition
# in trans-1,3,5-hexatriene
#
%sim
   Model IMDHO

   AbsRange     38000.0,   48000.0
   NAbsPoints   2000
   AbsScaleMode Rel

   # resonance Raman intensities will be calculated
   # for all vibrational states with excitation number
   # up to RamanOrder:
   RamanOrder  4

   # excitation energies (cm**-1) for which rR spectra will be calculated:
   RRSE 39500, 39800, 41400

   # full width half maximum of Raman bands in rR spectra (cm**-1):
   RRS_FWHM  10

   RSRange   0, 5000  # spectral range for simulation of rR spectra (cm**-1)
   NRRSPoints  5000   # number of points to simulate rR spectra (cm**-1)

end

$el_states
1
   1  39800.0      150.00    0.0     1.0   0.0   0.0

$vib_freq_gs
9
    1      354.0
    2      444.0
    3      934.0
    4     1192.0
    5     1290.0
    6     1305.0
    7     1403.0
    8     1581.0
    9     1635.0

$sdnc
9 1
               1
      1       0.55
      2       0.23
      3       0.23
      4       0.82
      5       0.485
      6       0.00
      7       0.085
      8       0.38
      9       1.32
```

`orca_asa` 运行后将创建以下文件：

-   `example005abs.dat` 包含模拟的吸收谱。如 [fig:720](#fig:720) 所示。

-   `example005.o4.rrs.39500.dat`、`example005.o4.rrs.39800.dat` 和
    `example005.o4.rrs.41400.dat` 分别包含激发能为 39500、39800 和
    41400 cm$^{-1}$ 时模拟的 rR 谱。后缀 "`o4`" 表示输入中
    由关键词 `RamanOrder=4` 指定的拉曼散射阶数。rR 谱如 [fig:721](#fig:721) 所示。

-   `example005.o4.rrs.39500.stk`、`example005.o4.rrs.39800.stk` 和
    `example005.o4.rrs.41400.stk` 给出每个振动跃迁的拉曼位移和强度。
    相应的振动态由被激发模的量子数指定。

<a id="fig:720"></a>
*对文件 `example005.inp` 运行 `orca_asa` 后生成的、
*反式*-1,3,5-己三烯中 $1-^{1}A_{g} \rightarrow 1-^{1}B_{u}$ 跃迁对应的吸收谱。*

<a id="fig:721"></a>
*三个不同激发能下的共振拉曼谱，它们与 *反式*-1,3,5-己三烯中的
$1-^{1}A_{g} \rightarrow 1-^{1}B_{u}$ 跃迁共振。*

!!! note

    -   默认情况下，程序以任意标度给出 rR 谱，
        因为在大多数实际情形中，只有单条 rR 谱内的相对 rR 强度才是主要关心的。
        不过，可以在 `%sim` 块中提供关键词 `RSISM=ASR`
        将不同激发能对应的 rR 谱放在同一强度标度上
        （RSISM —— Raman Spectra Intensity Scaling Mode，拉曼谱强度缩放模式；
        ASR —— All Spectra Relative，所有谱相对）。默认为 `RSISM=SSR`
        （SSR —— Single Spectrum Relative，单谱相对），
        此时每条 rR 谱被归一化，使其最强谱带的强度为 1.0。
        若相对参考信号（例如溶剂的拉曼带）的强度进行适当归一化，
        则不同激发能下测得的 rR 谱中各谱带的相对强度可以相互比较。
        我们也考虑到扩展本方法以给出 rR 强度绝对度量
        （以全截面或微分截面表示）的可能性。

    -   在简谐模型内，对单个电子态，在 `AbsScaleMode=Rel` 情况下，
        无论相对 rR 强度还是吸收带形都不依赖于电子跃迁偶极矩的数值
        （除非它恰好为零）。

在上例中，对总激发量子数不超过参数 `RamanOrder` 所定值的
所有振动跃迁生成了共振拉曼谱。也可以通过 `$rr_vib_states` 块
显式指定对应于各基频、倍频和组合频带的振动态。
在这种情形下，将单独生成仅含这些振动跃迁的 rR 谱。

每个振动跃迁由具有以下结构的子块指定：

```orca
$rr_vib_states 5 # total number of vibrational transitions
 1
   modes 1
   quanta 1; # final vibrational state for the fundamental
             # band corresponding to mode 1
 2
   modes 9
   quanta 1; # final vibrational state for the fundamental
             # band corresponding to mode 9
 3
   modes 3, 4
   quanta 1, 1; # final vibrational state for the combination band involving 
                # single excitations in modes 3 and 4
 4
   modes 5
   quanta 3; # final vibrational state for the second overtone band 
             # corresponding to mode 5
 5
   modes 1, 5,9
   quanta 1,2, 1; # final vibrational state for the combination band
                  # involving single excitations in modes 1 and 2, and
		  # double excitation in mode 5
```

这意味着第 $k$ 个跃迁由模 $m_{i}$ 的激发数 $q_{i}$ 表征，
相应的拉曼位移等于 $\nu =\sum\nolimits{ q_{i} \nu_{i} }$，
其中 $\nu_{i}$ 是模 $m_{i}$ 的振动频率。

`orca_asa` 运行后还将创建以下文件：

-   `example005.us.rrs.39500.dat`、`example005.us.rrs.39800.dat` 和
    `example005.us.rrs.41400.dat` 分别包含激发能为 39500、39800 和
    41400 cm$^{-1}$ 时、仅含 `$rr_vib_states` 块中指定振动跃迁的模拟 rR 谱。
    后缀 "us" 代表 "User specified vibrational States"（用户指定的振动态）。

-   `example005.us.rrs.39500.stk`、`example005.us.rrs.39800.stk` 和
    `example005.us.rrs.41400.stk` 给出 `$rr_vib_states` 块中
    指定的每个振动跃迁的拉曼位移和强度。

<a id="sec:spectroscopyproperties.asa.input.raman2"></a>
### 示例：*反式*-1,3,5-己三烯中 1-$^1$A$_g$ $\rightarrow$ 1-$^1$B$_u$ 跃迁的吸收谱与共振拉曼轮廓建模（Example: Modelling of Absorption Spectrum and Resonance Raman Profiles for the 1-$^1$A$_g$ $\rightarrow$ 1-$^1$B$_u$ Transition in *trans*-1,3,5-Hexatriene）

下例说明了模拟吸收带形和共振拉曼轮廓（RRP）的输入：

```orca
#
# example006.inp
#
# input for simulation of absorption and resonance Raman profiles
# using experimental values of transition energy and displacement
# parameters corresponding to the strongly allowed 1-1Ag 1-1Bu transition
# in trans-1,3,5-hexatriene
#

%sim
     Model IMDHO

     AbsRange     38000.0,   48000.0
     NAbsPoints   2000
     AbsScaleMode Rel

     RRPRange   38000.0, 48000.0 # spectral range for simulation of
                                 # rR profiles (cm**-1)

     NRRPPoints   2000 # number of points for simulation of rR profiles
     CAR 0.8

     RamanOrder 2
end

$el_states
1
   1  39800.0      150.00    0.0     1.0   0.0   0.0

$vib_freq_gs
9
    1      354.000000
    2      444.000000
    3      934.000000
    4     1192.000000
    5     1290.000000
    6     1305.000000
    7     1403.000000
    8     1581.000000
    9     1635.000000

$sdnc
9 1
               1
      1       0.55
      2       0.23
      3       0.23
      4       0.82
      5       0.485
      6       0.00
      7       0.085
      8       0.38
      9       1.32

$rr_vib_states 5 # total number of vibrational transitions
 1
    modes 1
    quanta 1;
 2
    modes 9
    quanta 1;
 3
    modes 3, 4
    quanta 1, 1;
 4
    modes 5
    quanta 3;
5
     modes 1, 5,9
     quanta 1,2, 1;
```

关键词 `RamanOrder=2` 将在关键词 `RRPRange` 和 `NRRPPoints`
指定的激发能范围内，为总激发量子数不超过 2 的所有振动跃迁生成 rR 轮廓。
同样，`$rr_vib_states` 块中给出的振动态的 rR 轮廓将单独生成。
由于在大多数情形中只有相对 rR 强度才重要，
而且人们往往希望比较吸收带形与各条 rR 轮廓的形状，
因此使用关键词 `CAR = 0.8` 对所有振动跃迁的 rR 轮廓
按一个公共因子缩放，使得所有 rR 强度的极大值与吸收带极大值之比等于 0.8。

`orca_asa` 运行后将创建以下文件：

-   `example006.abs.dat` 包含模拟的吸收谱（[fig:722](#fig:722)）。

-   `example006.o1.rrp.dat` 和 `example006.o2.rrp.dat` 分别包含
    总激发量子数为 1 和 2 的振动跃迁的 rR 轮廓。
    所有基频带的 RR 轮廓（来自文件 `example006.o1.rrp.dat`）
    如 [fig:722](#fig:722) 所示。

-   `example006.o1.info` 和 `example006.o1.info `分别包含
    总激发量子数为 1 和 2 的振动跃迁的说明以及相应的拉曼位移。

-   `example006.us.rrp.1.dat–example006.us.rrp.5.da`t 包含
    `$rr_vib_states` 块中指定的振动跃迁 1--5 的 rR 轮廓。

<a id="fig:722"></a>
**反式*-1,3,5-己三烯中 $1-^1A_g \rightarrow 1-^1B_u$ 跃迁对应的
吸收谱和基频带的共振拉曼轮廓。*

<a id="sec:spectroscopyproperties.asa.fit"></a>
## 实验谱的拟合（Fitting of Experimental Spectra）

<a id="sec:spectroscopyproperties.asa.fit.gauss"></a>
### 示例：吸收谱的高斯拟合（Example: Gauss-Fit of Absorption Spectrum）

吸收谱基本上由若干吸收带组成。每条吸收带对应于
基电子态到激发电子态的一个跃迁。在分子中这类跃迁通常相当宽。
许多情形下谱带会相互重叠，需要将宽的吸收包络解卷积为
各个跃迁的贡献。在"简单模型"内，`orca_asa` 程序能用
标准线型函数（高斯、洛伦兹）或更一般的 Voigt 函数之和
对吸收谱进行拟合。在大多数情形下，只需进行"高斯拟合"，
即假定每条谱带的形状为高斯函数。
然后使用必要数量（可多可少）的高斯函数以精确表示吸收包络。
为说明"简单模型"内的拟合流程，让我们考察
[fig:723](#fig:723) 中的实验吸收谱：

<a id="fig:723"></a>
*实验吸收谱。竖线标出在谱拟合输入中用作初始猜测的跃迁能。*

如 [fig:723](#fig:723) 所示，可以大致辨认出 7 条电子谱带。
对应于吸收谱中极大值和肩峰的跃迁能初始估计
（在 [fig:723](#fig:723) 中以竖线标出），
以及非均匀展宽和跃迁偶极矩分量的相当近似的值，
在谱拟合输入文件的 `$el_states` 块中指定：

```orca
# example007.inp 
#
# Input file for fitting of experimental absorption spectrum
#

%sim
        model Simple
end

%fit
       Fit true               # Global flag to turn on the fit
       AbsFit true            # Flag to include absorption into the fit
       method Simplex
       WeightsAdjust true

       AbsRange 0.0, 100000.0 # absorption spectral range to be included in the fit;
                              # in the present case all experimental points 
                              # will be included

       AbsName "absexp.dat"   # name of the file containing experimental
                              # absorption spectrum in a simple two-column 
                              # ASCII format

       ExpAbsScaleMode Ext    # This keyword indicates that the experimental 
                              # absorption intensity is given in terms of
                              # the extinction coefficient. This is important
                              # for the proper fitting of transition dipole  
                              # moments and oscillator strengths

       NMaxFunc 10000   # maximum number of function evaluations in simplex
                        # algorithm 

       MWADRelTol 1e-5  # Relative Tolerance of the Mean Weighted Absolute 
                        # Difference  (MWAD) function which specifies the        
                        # convergence criterion

       E0Step 500.00    # initial step for the transition energies
                        # in the simplex fitting

       TMStep 0.5       # initial step for the transition dipole moments
                        # in the simplex fitting

       E0SDStep 500.0   # initial step for the inhomogeneous linewidth (Sigma)
                        # in the simplex fitting

end

# ! Parameters specified in the $el_states block 
#   are used as initial guess in the fit

#---------------------------------------------------------------------------
#  Transition        Gamma    Sigma  Transition Dipole Moment (atomic unit)
#  Energy (cm**-1)  (cm**-1) (cm**-1)      Mx          My        Mz
#---------------------------------------------------------------------------

$el_states
7
    1 11270           0.0     1000.00    1.0000     0.0000     0.0000
    2 15100           0.0     1000.00    1.0000     0.0000     0.0000
    3 20230           0.0     1000.00    1.0000     0.0000     0.0000
    4 27500           0.0     1000.00    1.0000     0.0000     0.0000
    5 31550           0.0     1000.00    1.0000     0.0000     0.0000
    6 37070           0.0     1000.00    1.0000     0.0000     0.0000
    7 39800           0.0     1000.00    1.0000     0.0000     0.0000

# the integer values specified in $el_states_c block indicate parameters
# in the $el_states block to be varied
$el_states_c
7
    1    1             0          1          1         0         0
    2    2             0          2          2         0         0
    3    3             0          3          3         0         0
    4    4             0          4          4         0         0
    5    5             0          5          5         0         0
    6    6             0          6          6         0         0
    7    7             0          7          7         0         0
```

约束块 `$el_states_c` 的功能应按如下方式理解：
1) 0 标志表示 `$el_state` 块中相应的参数在拟合中不变；
2) 若某个参数对应的数字与相应电子态的编号一致，
则该参数将独立变化。因此，输入中的 `$el_states_c` 块表明
所有跃迁能、非均匀线宽和跃迁电偶极矩的 x 分量将独立变化，
而均匀线宽、跃迁偶极矩的 y 和 z 分量将固定为其初始值。

以下几点很重要：

-   由于常规吸收光谱处理的是取向平均的吸收截面，
    信号强度与跃迁电偶极矩的平方 $\left|{ \mathrm{\mathbf{M} }} \right|^{2}$ 成正比。
    因此，只要 $\left|{ \mathrm{\mathbf{M} }} \right|^{2}= \text{const}$，
    强度就不依赖于 $\mathrm{\mathbf{M} }$ 各分量的数值。
    因此，我们只允许 $M_{x}$ 分量变化。
    否则拟合算法的收敛可能出现问题。

-   进入最小化所用的平均绝对差函数的实验点权重之和
    始终保持等于实验点数目。若实验光子能量是等间距的，
    所有权重均设为相等。然而，在实验电子谱中，
    从高能到低能光谱区域谱点密度可能显著增加，
    这是因为实验吸收谱最初是在波长标度上采集的。
    在这种情形下，拟合质量会明显偏向低能光谱区域。
    因此，建议按实验点的密度调整其相对权重，
    这由 `%fit` 块中的关键词 `WeightsAdjust` 控制。
    尽管该参数对本例并不关键，但一般而言它会给出更均衡的拟合。

-   `%fit` 块中的参数 `E0Step`、`TMStep`、`E0SDStep`
    指定 $E_{T} ,\mathrm{\mathbf{M} }, \sigma$ 空间中单纯形的初始尺度，
    应大致对应于 `$el_states` 块中这些参数的初始猜测
    相对其实际值的预期不确定度。
    若指定初始步长的参数过低或过高，拟合质量可能明显变差。

对文件 `example007.inp` 运行 `orca_asa` 拟合，
将在约 3600 次函数求值后收敛（对 `MWADRelTol=1e-5`）。
拟合结果将存储在文件 `example007.001.inp` 中，
其结构与输入文件 `example007.inp` 相同。
因此，若拟合不令人满意和/或未完全收敛，
可以在随后的 `orca_asa` 运行中加以改进，
该运行将创建文件 `example007.002.inp`，依此类推。
中间文件中的一些模型参数可以额外修改，
也可以根据需要解除或施加某些约束。
输出文件 `example007.001.inp` 将包含存储在 `$el_states` 块中的
拟合模型参数：

```orca
$el_states
7
   1 11368.24     0.00  732.50     1.6290   0.0000   0.0000
   2 15262.33     0.00  495.17    -0.2815   0.0000   0.0000
   3 19500.08     0.00  1023.39     0.2300   0.0000   0.0000
   4 26969.01     0.00  1832.30     1.4089   0.0000   0.0000
   5 31580.41     0.00  1440.87     1.8610   0.0000   0.0000
   6 35769.07     0.00  1804.02     1.5525   0.0000   0.0000
   7 39975.11     0.00  1909.38     2.4745   0.0000   0.0000
```

拟合的总体质量由参数 MWAD 决定，
收敛时其值达到 $\approx$0.009
（MWAD 代表 Mean Weighted Absolute Difference，平均加权绝对差）。

`orca_asa` 运行后将创建文件 `absexp.fit.dat` 和 `absexp.fit.as.dat`。
两个文件都包含实验谱和拟合谱，如 [fig:724](#fig:724) 所示。
此外，文件 `absexp.fit.as.dat` 还将包含对应于不同激发态的
各条吸收谱贡献。

<a id="fig:724"></a>
*对文件 `example007.inp` 运行 `orca_asa` 拟合时实验（黑曲线）与拟合（红）
吸收谱的比较。蓝曲线表示各条电子谱带的贡献。*

由于拟合谱与实验谱在约 13000 cm$^{-1}$ 处存在明显差异
（[fig:724](#fig:724)），值得在文件 `example007.001.inp` 中
添加一个新态的参数后改进拟合：

```orca
$el_states
8
   1 11368.24     0.00  732.50     1.6290   0.0000   0.0000
... ... ...
   8 13280.00     0.00  1000.00     1.000   0.0000   0.0000

$el_states_c
8
   1     1         0        1          1        0        0
... ... ...
   8     8         0        8          8        0        0
```

实际上，本例中差异的性质与 [fig:721](#fig:721) 中非常相似
（[sec:spectroscopyproperties.asa.input.paraimdho](#sec:spectroscopyproperties.asa.input.paraimdho) 一节），
那里用高斯线型拟合了振动展宽的吸收谱。
因此，约 1300 cm$^{-1}$ 区域的拟合不佳，
很可能是由于振动展宽本质上不对称，而非存在另一条电子谱带。

如 [fig:725](#fig:725) 所示，改进后的拟合使实验与拟合吸收谱之间
的一致性好得多（MWAD$=$0.0045）。

<a id="fig:725"></a>
*对文件 `example007.001.inp` 运行 `orca_asa` 拟合时实验（黑）与拟合（红）
吸收谱的比较。蓝曲线表示各条电子谱带的贡献。*

由于函数极小化单纯形算法的一些特殊性，
您仍可通过在文件 `example007.002.inp` 上重新运行 `orca_asa` 来改进拟合！
这会得到更低的参数值 MWAD$=$ 0.0038，
从而使实验谱与拟合谱符合得更好（尽管上一次运行已被宣布收敛）。

也可以对所有电子态使用相同的非均匀线宽值进行拟合。
为此需要在 `$el_states ` 块中选取相同的线宽参数作为猜测：

```orca
$el_states
8
   1 11118.58     0.00  1000.0      1.0687   0.0000   0.0000
   2 13673.38     0.00  1000.0     -0.5530   0.0000   0.0000
   3 21267.40     0.00  1000.0      0.3675   0.0000   0.0000
   4 27024.71     0.00  1000.0      1.4041   0.0000   0.0000
   5 31414.74     0.00  1000.0      1.7279   0.0000   0.0000
   6 35180.77     0.00  1000.0      1.6246   0.0000   0.0000
   7 39985.52     0.00  1000.0      2.5708   0.0000   0.0000
   8 11665.01     0.00  1000.0      1.2332   0.0000   0.0000
```

此外，约束块应修改如下：

```orca
$el_states_c
8
   1     1         0        1          1        0        0
   2     2         0        1          2        0        0
   3     3         0        1          3        0        0
   4     4         0        1          4        0        0
   5     5         0        1          5        0        0
   6     6         0        1          6        0        0
   7     7         0        1          7        0        0
   8     8         0        1          8        0        0
```

非均匀展宽的约束参数选为 1，这意味着形式上对应于第一态的
$\sigma_{1}$ 独立变化，而其他谱带的线宽
$\left\{{ \sigma_{i} } 
\right\}$ 的变化方式是保持比值
$\sigma 
_{i} /\sigma_{1}$ 固定为其初始值，
从而对所有态使用相同的线宽参数。

<a id="fig:726"></a>
*对文件 `example007.002.inp` 运行 `orca_asa` 拟合时实验（黑）与拟合（红）
吸收谱的比较，其中假设所有电子谱带的展宽相等。*

可以看到（[fig:726](#fig:726)），假设所有电子谱带线宽相等
会导致低能光谱范围内拟合质量明显变差（MWAD$=$0.017）。
显然，假设在更高能量处存在更多电子态可以消除这一差异。

注意

-   均匀线宽参数也可以用类似方式纳入拟合。
    不过可以看到，在大多数情形下它们远小于相应的高斯线宽参数。

-   吸收谱的高斯拟合通常假定所有谱带具有相同的线宽参数。
    然而，由于高斯展宽的很大部分主要来自谱中未分辨的振动结构，
    而后者可随跃迁性质显著变化，假设不相等的高斯带宽似乎是合理的。

<a id="sec:spectroscopyproperties.asa.fit.raman"></a>
### 示例：*反式*-1,3,5-己三烯中 1-$^1$A$_g$ $\rightarrow$ 1-$^1$B$_u$ 跃迁的吸收与共振拉曼谱拟合（Example: Fit of Absorption and Resonance Raman Spectra for the 1-$^1$A$_g$ $\rightarrow$ 1-$^1$B$_u$ Transition in *trans*-1,3,5-Hexatriene）

下面我们给出一个拟合己三烯中强偶极允许的 1-$^{1}$A$_{g}$
$\rightarrow$1-$^{1}$B$_{u}$ 跃迁的线型参数和
$\left\{{\Delta_{m} } \right\}$ 的例子。
已知 rR 谱中最强的谱带对应于吸收谱中振动活性最强的模。
对于 IMDHO 模型，这一关联由 $\left\{{ \Delta_{m} } 
\right\}$ 的数值决定。因此，$\Delta$ 越大，
给定模的 rR 强度越大，吸收谱中对应于该模的精细结构也越明显。
原则上，若吸收中所有振动跃迁都很好分辨，
可以仅通过拟合吸收谱确定 $\left\{{ \Delta 
_{m} } \right\}$。实际上，由于实验吸收谱分辨率有限，
该任务是不确定的。观测 rR 谱可以鉴定出对吸收谱精细结构
负责的振动态，并以 $\left\{{ \Delta_{m} } \right\}$ 进行定量分析。
文件 `example006.inp `提供了一个用尽可能少的实验信息进行拟合的
直接例子：1) 一张吸收谱；2) 给定激发能下基频带的相对 rR 强度。
在与 39809 cm$^{-1}$ 处 0-0 振动带共振的激发下的 rR 谱
如 [fig:715](#fig:715) 所示。

<a id="fig:727"></a>
**反式*-1,3,5-己三烯中 1-$^1$A$_g$ $\rightarrow$ 1-$^1$B$_u$ 跃迁对应的实验共振拉曼谱。*

实验 rR 谱鉴定出七个产生最强共振拉曼谱带的振动态。
因此，预计它们具有最大的激发态位移，
对吸收谱振动结构的影响也最明显。
它们的振动频率作为拟合输入输入如下：

```orca
#
# example008.inp
#
# Input for fit of absorption and resonance Raman spectra
# corresponding to the strongly allowed 1-1Ag 1-1Bu transition
# in 1,3,5 trans-hexatriene.
# 
# Parameters to be varied:
# 1) adiabatic minima transiton energy
# 2) homogeneous linewidth (Gamma)
# 3) dimensionless normal coordinate displacements of the 
#    excited-state origin 
#

%sim
      Model IMDHO
end

%fit 
    
    Fit true     # boolean parameter to switch on the fit

    # boolean parameter to include experimental absorption 
    # spectrum in the fit:
    AbsFit true  

    # boolean parameter to include experimental rR spectra
    # specified in $rrs_exp block in the fit:
    RRSFit true

    AbsExpName "hex-abs.dat" # name of the file with experimental absorption
                             # spectrum

    # the following value of keyword ExpAbsScaleMode
    # indicates that only the shape of absorption band 
    # but not its total intensity will be accounted in the fit:
    ExpAbsScaleMode Rel

    # the weight of absorption relative to the total weight of
    #  rR intensities in the difference function to be minimized:
    CWAR  5.0

    NMaxFunc  1000   # maximum number of function evaluations in simplex
                     # algorithm 

    MWADRelTol 1e-4  # Relative Tolerance of the Mean Weighted Absolute 
                     # Difference  (MWAD) function which specifies the        
                     # convergence criterion
    SDNCStep  1.0
                    
end  

# The values specified in $el_states block serve as initial guess in the fit
$el_states
1
   1  40000.0      200.00    0.0     1.0   0.0   0.0

# the integer values specified in $el_states_c block indicate parameters
# in $el_states block to be varied
$el_states_c
1
   1     1            1       0       0     0     0 

# 7 totally symmetric vibrations which give rise to the most
# intense bands in the rR spectra are included into analysis.
# Experimental values of vibration frequencies are given: 
$vib_freq_gs
7
    1      354.0
    2      444.0 
    3      934.0
    4     1192.0
    5     1290.0
    6     1403.0
    7     1635.0

# Initial guess for the values of dimensionless normal
# coordinate displacements of the excited-state origin 
$sdnc
7 1
               1
      1       0.0    
      2       0.0     
      3       0.0      
      4       0.0      
      5       0.0   
      6       0.0    
      7       0.0     

# the integer values specified in $sdnc_c block indicate parameters
# in $sdnc block to be varied
$sdnc_c
7 1
             1
      1        1
      2        2
      3        3
      4        4
      5        5
      6        6
      7        7

# specification  of vibrational transitions and their intensities 
# in experimental rR spectra:
$rrs_exp 
1         # number of rR spectra
1 1       # start of the block specifying the 1st rR spectrum
    Ex 39809.0 # excitation energy for the first rR spectrum
    NTr  7     # number of vibrational transitions for which intensities are 
               # provided 
    1     
       int   10.0  1.0
       modes  1
       quanta 1;
    2     
       int   5.0  1.0
       modes  2
       quanta 1;
    3     
       int   1.5  1.0
       modes  3
       quanta 1;
    4     
       int   21.0  1.0
       modes  4
       quanta 1;
    5     
       int   7.5  1.0
       modes  5
       quanta 1;
    6     
       int   2.0  1.0
       modes  6
       quanta 1;
    7     
       int   46.0  1.0
       modes  7
       quanta 1;
```

任意数目激发能的 rR 强度输入跟在关键词 `$rrs_exp` 块之后：

```orca
$rrs_exp 
1         # number of rR spectra
1 1
```

最后一行中的第一个 "1" 表示下面开始说明的 rR 谱的编号。
若第二个数字与谱的编号相同，则意味着在拟合中
只有第一条 rR 谱的相对强度是有意义的。
若输入中给出多条谱，第二个数字可以有不同的值，例如：

```orca
$rrs_exp 
3         # number of rR spectra
1 2 
...
```

该输入应解释为：提供了 3 条 rR 谱，
第一条谱的相对强度与第二条谱在同一标度上给出，
后者将在拟合中加以考虑。在指定每条 rR 谱强度的块中，
激发能的数值和指定的振动跃迁数目是必不可少的。

在关键词 `NTr` 给出的振动跃迁数目之后，
必须指定每个振动跃迁及其强度。
因此，在本例中有七个具有以下结构的子块：

```orca
k    int   I  W
          modes m1,m2,...mn  
          quanta q1,q2,...qn;
```

这意味着第 $k$ 个跃迁具有强度 $I$ 和权重 $W$，
后者进入用于最小化的平均绝对差函数（$W$ 是可选参数）。
随后两行通过给出模 $m_{i}$ 的激发数 $q_{i}$ 指定振动跃迁，
相应的拉曼位移等于 $\nu =\sum\limits_ { q_{i} \nu 
_{i} }$，其中 $\nu_{i}$ 是模 $m_{i}$ 的振动频率。

需要变化的参数在约束块 `$el_states_c` 和 `$sdnc_c` 中指定。
两个块的结构和参数数目分别与 `$el_states` 和 `$sdnc` 相同。
若 `$el_states_c` 块中的对应参数等于电子态的编号，
则假定 `$el_states` 块中的该参数独立变化。
同样，若 `$sdnc_c` 块中的对应参数等于简正模的编号，
则假定 `$sdnc` 块中的该参数独立变化。
在相应约束块中设为 0 的模型参数在拟合中不变。
以下参数的数值对拟合质量可能很重要：

-   `%fit` 块中的 `CWAR` 指定在待最小化的差函数中
    吸收相对于 rR 强度的权重。若未指定该参数，
    拟合将几乎不敏感于输入中的 rR 强度，
    因为通常实验吸收点的数目远大于输入中 rR 跃迁的数目。
    在大多数情形下，`CWAR` 取 1.0--5.0 范围内的值是不错的选择，
    因为吸收测量强度的误差预计远小于共振拉曼的。

-   `%fit` 块中的 `SDNCStep` 指定 $\left\{{ \Delta_{m} } \right\}$ 空间中
    单纯形的初始尺度，应大致对应于 `$sdnc `块中
    $\left\{{ \Delta_{m} } \right\}$ 的初始猜测相对其实际值的预期不确定度。
    您可以在本例中注意到，若该参数过大（>2.0）或过小（<0.4），
    拟合质量可能显著变差

-   尽管对不同类型的参数单纯形的默认初始尺度取值合理，
    但在某些情形下修改默认值可能有所帮助：

```orca
  FREQGStep 10.0  # ground-state vibrational frequencies
  FREQEStep 10.0  # excited-state vibrational frequencies
  E0Step    300.0 # transition energies
  SSStep     20.0 # Stokes shift
  TMStep      0.5 # electronic transition dipole moment
  GammaStep  50.0 # homogeneous linewidth
  E0SDStep   50.0 # inhomogeneous linewidth
  SDNCStep    1.0 # origin shift along dimensionless normal coordinate
```

对文件 `example008.inp` 运行 `orca_asa` 拟合，
将在约 700 次函数求值后收敛（对 `MWADRelTol=1e-4`）。
拟合结果将存储在文件 `example008.001.inp` 中，
其结构与输入文件 `example008.inp` 相同。
因此，若拟合不令人满意和/或未完全收敛，
可以在随后的 `orca_asa` 运行中加以改进，
该运行将创建文件 `example008.002.inp`，依此类推。
中间文件中的一些模型参数可以额外修改，
也可以根据需要解除某些约束。输出文件 `example008.001.inp`
将包含存储在 `$sdnc` 块中的拟合位移参数
$\left\{{ \Delta_{m} } \right\}$：

```orca
$sdnc                  
7 1                    
                   1   
      1       0.675000 
      2      -0.194484 
      3      -0.217527 
      4       0.811573 
      5       0.529420 
      6      -0.149991 
      7       1.314915
```

在本例中，这些参数实际上与己三烯分子已发表的值非常接近！

拟合的总体质量由参数 MWAD 决定，收敛时其值达到 $\approx$0.027。
拟合的 rR 强度以注释行的形式列在文件 `example008.001.inp` 中
实验 rR 强度的旁边：

```orca
$rrs_exp
1
   1   1 3.495285e+001
   Ex    39809.00
   NT   7
      1
        Int 10.0 1.0  # simulated intensity: 1.000982e+001
        modes  1
        quanta 1;
      2
        Int 5.0 1.0   # simulated intensity: 8.976285e-001
        modes  2
        quanta 1;
      3
        Int 1.5 1.0   # simulated intensity: 1.255880e+000
        modes  3
        quanta 1;
      4
        Int 21.0 1.0  # simulated intensity: 1.761809e+001
        modes  4
        quanta 1;
      5
        Int 7.5 1.0   # simulated intensity: 7.499749e+000
        modes  5
        quanta 1;
      6
        Int 2.0 1.0   # simulated intensity: 6.014466e-001
        modes  6
        quanta 1;
      7
        Int 46.0 1.0  # simulated intensity: 4.600071e+001
        modes  7
        quanta 1;
```

文件 hex-abs.fit.dat 将以 ASCII 格式包含实验和拟合吸收谱，
可绘图以直观显示吸收拟合的质量（[fig:728](#fig:728)）。

<a id="fig:728"></a>
*1,3,5 *反式*-己三烯中 1-$^1$A$_g$ $\rightarrow$ 1-$^1$B$_u$ 跃迁对应的
实验（黑）与拟合（红）吸收谱。*

!!! note

    -   分析中包含的实验 rR 强度越多，拟合越可靠。
        原则上，即使只提供有限数目的振动跃迁，
        也可能得到完全一致的结果。不过，在这种情形下，
        最好在分析中至少包含一条涉及待确定 $\Delta$ 之模的拉曼跃迁。

    -   若调用 IMDHOFA 模型并允许激发态振动频率变化，
        拟合质量可以提高。

    -   由于初始猜测和单纯形的尺度，以及函数极小化单纯形算法的一些特殊性，
        您仍可通过在文件 `example008.001.inp` 上重新运行 `orca_asa` 来改进拟合，
        这可能得到更低的参数值 `MWAD = 0.021`，
        从而使实验谱与拟合谱符合得更好（尽管上一次运行已被宣布收敛）。

    -   在这方面，分三步进行拟合似乎是明智的：

        1.  用单个洛伦兹带拟合 0-0 振动带以下的预共振区域，
            由此得到绝热跃迁能 $E_{0}$ 和均匀线宽 $\Gamma$。
            吸收谱的拟合范围可由 `%fit` 块中的 `AbsRange` 关键词指定。

        2.  固定 $E_{0}$ 和 $\Gamma$，优化
            $\left\{{ \Delta_{m} } \right\}$，拟合整个光谱范围和 rR 强度。

        3.  解除对 $E_{0}$ 和 $\Gamma$ 的约束，同时重新优化所有参数。

<a id="sec:spectroscopyproperties.asa.fit.singleMode"></a>
### 示例：并四苯中 1-$^1$A$_g$ $\rightarrow$ 1-$^1$B$_{2u}$ 跃迁的吸收与荧光谱单模拟合（Example: Single-Mode Fit of Absorption and Fluorescence Spectra for 1-$^1$A$_g$ $\rightarrow$ 1-$^1$B$_{2u}$ Transition in Tetracene）

本节我们给出一个例子，并讨论荧光谱和吸收谱联合拟合的最重要方面。
[fig:729](#fig:729) 显示了并四苯中
1-$^1$A$_g$ $\rightarrow$ 1-$^1$B$_{2u}$ 跃迁对应的
实验发射谱和吸收谱。

<a id="fig:729"></a>
*在单一振动活性模假设下环己烷中并四苯的解卷积吸收（红）和荧光（蓝）谱。
黑色实线表示实验谱，点线表示拟合谱。*

两张谱都显示出明显的有效振动精细结构，分别以 3 个和 5 个峰为主。
正如量子化学计算可以证明的，该精细结构本质上是多模的。
然而，在假设单一振动活性模的情况下，实验谱可以很好地拟合。
输入具有以下结构：

```orca
#
# example009.inp
# 
# Parameters to be varied:
# 1) adiabatic minima transition energy
# 2) homogeneous and inhomogeneous linewidths
# 3) normal mode frequency and corresponding dimensionless displacement of the 
#    excited-state origin 
#

%sim
      Model IMDHO
      EnInput E0 # we assume adiabatic minima separation energies 
end

%fit
    Fit true       # global flag to turn on the fit
    AbsFit true    # flag to include absorption spectrum into the fit
    FlFit true     # flag to include fluorescence spectrum into the fit

    WeightsAdjust true

    AbsRange 19000.0, 28000.0 # spectral range for absorption
                              # which will be included into the fit

    FlRange  17800.0, 22300.0 # spectral range for absorption
                              # which will be considered in the fit

    AbsName "absexp.dat" # name of the file containing experimental
                         # absorption spectrum in a simple two-column 
                         # ASCII format
    FlName  "flexp.dat"  # name of the file with experimental fluorescence spectrum 

    ExpAbsScaleMode Rel  # flags indicating that only relative shapes of the 
    ExpFlScaleMode Rel   # absorption and fluorescence bands will be fitted.
    

    CWAF   1.000 # important parameter to have a balanced relative quality of fit
                 # of fluorescence and absorption

    NMaxFunc 10000  # maximum number of function evaluations in simplex
                    # algorithm 

    MWADRelTol= 0.0001  # Relative Tolerance of the Mean Weighted Absolute 
                        # Difference  (MWAD) function which specifies the        
                        # convergence criterion

    TMStep 0.5       # initial step for the transition dipole moments
                     # in the simplex fitting

    E0SDStep 500.0   # initial step for the inhomogeneous linewidth (Sigma)

    FREQGStep 100.00 # initial step for the vibrational frequencies

    E0Step 1000.0    # initial step for the transition energies

    SSStep 10.0      # initial step for the Stokes shift

    GammaStep 100    # initial step for the homogeneous linewidth

    SDNCStep 0.5    # initial step for the displacement parameter

end

$el_states
2
   1 21100.00    100.00   100.00     1.0000   0.0000   0.0000
   2 24000.00    100.00   1000.00    1.0000   0.0000   0.0000

$el_states_c
2
   1     1         1        1          0        0        0
   2     2         2        2          2        0        0

$abs_bool
2
  1  1
  2  1

$fl_bool
2
  1  1
  2  0

$ss
2
    1      100.000000
    2        0.000000

$ss_c
2
    1            1
    2            0

$vib_freq_gs
1
    1      1500.0

$vib_freq_gs_c
1
    1            1

$sdnc
1 2
                   1          2    
      1       2.0000000   0.000000
 
$sdnc_c
1 2
                   1          2    
      1         1          0
```

`%fit` 块中的参数 `CWAF=1.0` 指定在待最小化的差函数中
吸收相对于荧光的权重。若未指定该参数，拟合质量会偏向
实验点数目较多的那张谱。在某些典型情形下，
吸收测量强度的误差预计小于发射的，
这时最好将 `CWAF` 的值选为大于 1.0。

为考虑 24000 cm$^{-1}$ 以上吸收谱中宽而无结构的背景信号，
第二条谱带被纳入分析，并用 Voigt 线型近似，
这意味着 `$vib_freq_gs` 块中相应的频率和 `$sdnc ` 块中的位移参数
在拟合中固定为零。因此，`$el_states ` 块包含对 2 个态的
跃迁能、跃迁电偶极矩和线宽参数的初始猜测：

```orca
$el_states
2
   1 21100.00    100.00   100.00     1.0000   0.0000   0.0000
   2 24000.00    100.00   1000.00    1.0000   0.0000   0.0000
```

第一态绝热极小分离能的初始值由吸收谱中第一个振动峰
（21100 cm$^{-1})$ 对应的能量近似。
跃迁能和线宽参数如 `$el_states_c` 块所示独立变化。
由于我们只拟合带形而不拟合谱的总体强度，
只有两条谱带跃迁电偶极矩的相对绝对值才是重要的。
因此合理的是固定第一态跃迁矩的所有分量，
只让第二态的 $M_{x}$ 分量变化：

```orca
$el_states_c
2
   1     1         1        1          0        0        0
   2     2         2        2          2        0        0
```

由于我们假设两个态都吸收而只有第一态发射，
有必要包含布尔数组 \$abs_bool 和 \$fl_bool，
它们分别指定在吸收谱和荧光谱处理中将包含哪些态：

```orca
$abs_bool
2
  1  1 # 1 indicates that the corresponding state will be included 
  2  1 # in the calculation of absorption
  

$fl_bool
2
  1  1
  2  0 # 0 indicates that the corresponding state will be excluded 
       # from the calculation of emission spectrum
```

我们还需要变化决定谱中振动峰间距的模的振动频率值。
这通过约束块 `$vib_freq_gs_c` 完成：

```orca
$vib_freq_gs_c
1
    1            1
```

请注意，将第二态的 Stokes 位移纳入处理是没有意义的，
因为该态产生吸收谱中的背景信号，而相应的发射并不存在。
因此，第二态的 $\lambda$ 如 `$ss ` 块及其约束对应块 `$ss_c` 所示
固定为零：

```orca
$ss
2
    1    100.000000 # initialization of the Stokes shift for 
    2      0.000000 # the 1st electronic state

$ss_c
2
    1    1 # the Stokes shift for the 1st electronic state will be varied in the fit
    2    0 # the Stokes shift for the 2nd electronic state will be fixed in the fit
```

对文件 `example009.inp` 运行 `orca_asa` 拟合，
将在约 700 次函数求值后收敛（对 `MWADRelTol=1e-4`）。
文件 `example009.001.inp` 将包含拟合得到的振动频率和无量纲位移的有效值：
$\omega = 1404 \, \text{cm}^{-1}$，$\Delta = 1.35$。
可以注意到，在吸收谱和荧光谱的低能和高能边缘处拟合相当差
（[fig:729](#fig:729)）。
这一差异的来源是这里采用的单模近似。
假设若干具有非零位移参数的模可以显著提高拟合质量。
请注意，在这种情形下，关于活性模数目和相应无量纲位移的合理猜测
可以从量子化学计算中推得。

<a id="sec:spectroscopyproperties.asa.fitvalues"></a>
## 量子化学辅助的光谱带形与共振拉曼强度模拟和拟合（Quantum-Chemically Assisted Simulations and Fits of Optical Bandshapes and Resonance Raman Intensities）

本节我们最终将谱模拟算法与实际量子化学计算联系起来，
并概述在 IMDHO 模型内分析吸收、荧光和共振拉曼谱的详细方法。
若可得到激发态对核位移的解析导数，
我们的流程将高度高效且几乎自动。
不过，这并非必需，因此，对于尚未实现解析梯度的高水平电子结构方法，
也可以通过简正模扫描计算来实现谱预测。

<a id="sec:spectroscopyproperties.asa.fitvalues.raman"></a>
### 示例：*反式*-1,3,5-己三烯中 1-$^1$A$_g$ $\rightarrow$ 1-$^1$B$_u$ 跃迁的吸收与共振拉曼谱的量子化学辅助分析和拟合（Example: Quantum-Chemically Assisted Analysis and Fit of the Absorption and Resonance Raman Spectra for the 1-$^1$A$_g$ $\rightarrow$ 1-$^1$B$_u$ Transition in *trans*-1,3,5-Hexatriene）

下面的 ORCA 运行输入文件通过在基态平衡几何处进行能量和激发态梯度计算，
调用沿所有简正模的激发态原点位移计算。
该方法对 IMDHO 模型有效，其中沿给定简正模的激发态能量梯度
与相应原点位移之间存在非常简单的关系。

```orca
#
# example010.inp
#
# TDDFT BHLYP Normal Mode Gradient Calculation
#
#   The keyword NMGrad invokes the normal mode gradient calculation
#
! RKS BHandHLYP TightSCF SV(P) NMGrad

%cis    NRoots 1
        triplets false
end

%rr
    # the nuclear Hessian must have been calculated before - for example by a 
    # DFT calculation.
    HessName= "hexatriene.hess"

    states 1    # Perform energy-gradient calculations for the 1st 
                # excited state.
    Tdnc 0.005  # Threshold for dimensionless displacements to be 
                # included in the input file for spectral simulations 
                # generated at the end of the program run.
                # By default Tdnc= 0.005

    ASAInput true # Generate the input file for spectra simulations   
 end    

* xyz   0 1
  C    -0.003374    0.678229   0.00000
  H    -0.969173    1.203538   0.00000
  C     1.190547    1.505313   0.00000
  H     2.151896    0.972469   0.00000
  C     1.189404    2.852603   0.00000
  H     0.251463    3.423183   0.00000
  H     2.122793    3.426578   0.00000
  C     0.003374   -0.678229   0.00000
  H     0.969172   -1.203538   0.00000
  C    -1.190547   -1.505313   0.00000
  H    -2.151897   -0.972469   0.00000
  C    -1.189404   -2.852603   0.00000
  H    -0.251463   -3.423183    0.00000
  H    -2.122793   -3.426578    0.00000
*
```

在 ORCA 运行中，TDDFT 激发态梯度计算在 TDDFT 计算之上进行。
请注意，必须纳入分析的激发态编号以及谱模拟的输入文件
必须在 `%rr` 块的 `States` 关键词之后指定。
它们还应与 `%tddft` 块中要求的根数一致。
1-$^{1}$B$_{u}$ 激发态是 TDDFT 计算中的第一根。
因此，`%tddft` 块中为 `NRoots=1`，`%rr` 块中为 `States=1`。
还应通过 `%rr` 块中的 `HessName` 关键词提供包含核 Hessian 矩阵的文件名。
这里我们使用了在 BHLYP/SV(P) 理论水平频率计算中得到的 `.hess` 文件。

ORCA 计算结束后，您会在目录中找到名为
`example010.asa.inp` 的文件，它适合与前几节所定义的
`orca_asa 程序` 一起使用。

```orca
#
# example010.asa.inp
#
# ASA input
#
%sim
         model IMDHO
         method Heller
         AbsRange     5000.0,  100000.0
         NAbsPoints    0

         FlRange      5000.0,  100000.0
         NFlPoints     0

         RRPRange     5000.0,  100000.0
         NRRPPoints    0

         RRSRange        0.0,    4000.0
         NRRSPoints 4000

         RRS_FWHM 10.0

         AbsScaleMode Ext
         FlScaleMode Rel
         RamanOrder  0

         EnInput E0

         CAR   0.800

end

%fit
         Fit false
         AbsFit false
         FlFit false
         RRPFit fsalse
         RRSFit false
         method Simplex
         WeightsAdjust true

         AbsRange        0.0,  10000000.0
         FlRange         0.0,  10000000.0
         RRPRange        0.0,  10000000.0
         RRSRange        0.0,  10000000.0
         AbsName ""
         FlName  ""

         ExpFlScaleMode  Rel
         ExpAbsScaleMode Rel

         CWAR  -1.000
         CWAF  -1.000

         NMaxFunc 100
         MWADRelTol= 1.000000e-004

         SFRRPSimStep= 1.000000e+002
         SFRRSSimStep 1.000000e+002
         FREQGStep 1.000000e+001
         FREQEStep 1.000000e+001
         E0Step 3.000000e+002
         SSStep 2.000000e+001
         TMStep 5.000000e-001
         GammaStep 5.000000e+001
         E0SDStep 5.000000e+001
         SDNCStep 4.000000e-001
end

$el_states
1
   1 42671.71   100.00    0.00     1.0725   3.3770  -0.0000

$vib_freq_gs
12
    1      359.709864
    2      456.925612
    3      974.521651
    4     1259.779018
    5     1356.134238
    6     1370.721341
    7     1476.878592
    8     1724.259894
    9     1804.572974
   10     3236.588264
   11     3244.034359
   12     3323.831066

$sdnc
12 1
                   1    
      1      -0.594359
      2       0.369227
      3      -0.132430
      4      -0.727616
      5       0.406841
      6      -0.105324
      7       0.177617
      8      -0.090105
      9      -1.412258
     10       0.048788
     11       0.021438
     12       0.008887
```

该输入文件可用于构造理论吸收谱和 rR 谱。
**为比较实验与理论 rR 谱，必须在两种情形下使用大约与吸收谱中
同一振动跃迁共振的激发能。因此，对于具有已分辨或部分分辨
振动结构的吸收谱，必须修改 `%el_states ` 中的跃迁能，
使之与实验观测到的 0-0 振动峰一致。**
也建议大致调整均匀线宽以及可能的非均匀线宽参数，
使实验和计算吸收谱在预共振区域（0-0 跃迁以下）显示出相似的斜率。
然后，实验 rR 谱的归属可以通过与相应实验激发能下
计算的理论 rR 谱比较来完成。
为了一致和简单，最好使用落在预共振区域
和/或与 0-0 跃迁共振的那些激发能。
**对于弥散的吸收谱（即不显示已分辨振动结构的谱），
也必须调整理论跃迁能和线宽参数，使实验与计算的吸收极大值位置大致重合，
且极大值以下相应斜率的行为相似。**
根据上述考虑，需要修改文件 `example010.asa.inp` 中的 `%el_states` 块：

```orca
$el_states
1
   1 39808.0   150.00    0.00  1.0725   3.3770  -0.0000
```

通过提供 `AbsScaleMode= Rel`、`AbsRange= 39000`、`49000`
和 `NAbsPoints= 2000` 得到的计算吸收谱如 [fig:730](#fig:730) 所示。
与实验谱比较可以注意到，BHLYP 泛函给出的差异相对较小，
低频边缘强度略低，谱的高能侧强度较大。
此外，各振动峰间距有明显不符，这是由于 BHLYP 泛函
高估了振动频率（通常约 $\approx$ 10%）。

您可以在 `%sdnc` 块中任意改变各简正坐标位移，
幅度在其值的 10--30% 以内，以观察计算谱的变化。
这将告诉您这些参数如何影响谱，
并且很可能得到更好的拟合初始猜测。在本例中您会发现，
将第九个模对应的位移参数绝对值减小约 $\approx$ 10%，
并把振动频率减小约 $\approx$ 10%，可以明显改善谱包络。
这样快速的分析表明，吸收谱中实验观测到的峰代表
对应于单一电子激发态的不同振动跃迁，而非不同的电子激发。
这一结论将在确认吸收谱和 rR 谱可以基于单一电子跃迁假设
成功拟合之后得到证实。

<a id="fig:730"></a>
**反式*-1,3,5-己三烯中 1-$^1$A$_g$ $\rightarrow$ 1-$^1$B$_u$ 跃迁对应的
BHLYP/SV(P) 和 B3LYP/SV(P) 理论水平的计算与实验吸收谱（左图）和 rR 谱（右图）。*

要计算实验激发能下的 rR 谱，您需要通过 `%sim` 块中的 `RRSE` 关键词
指定其数值，并可能修改适合与实验 rR 谱比较的
光谱范围和 rR 谱带线宽相关参数：

```orca
# excitation energies (cm**-1) for which rR spectra will be calculated:
   RRSE 39808

   # full width half maximum of Raman bands in rR spectra (cm**-1):
   RRS_FWHM  20  

   RSRange   0, 4000  # spectral range for simulation of rR spectra (cm**-1)
   NRRSPoints  4000   # number of points to simulate rR spectra (cm**-1)

   # resonance Raman intensities will be calculated
   # for all vibrational states with excitation number
   # up to RamanOrder:
   RamanOrder 3
```

计算得到的 rR 谱如 [fig:730](#fig:730) 所示。
在输入中我们调用了最终振动态中最多含 3 个振动量子的跃迁的
rR 强度计算（`RamanOrder = 3`）。
请确认在给定光谱范围内，进一步增大该参数时 rR 强度模式没有明显变化。
通常，简正坐标位移越大，计算中需要的拉曼散射阶数就越高，
以考虑 rR 谱中所有最强的跃迁。
包含基频以外的振动跃迁是 `orca_asa` 程序的一个特色。

计算与实验 rR 谱的比较（[fig:730](#fig:730)）主要显示拉曼位移数值上的差异，
这主要与 BHLYP 水平得到的振动频率精度较低有关
（通常高估约 $\approx$ 10%）。然而，计算与实验 rR 谱的强度模式
与实验符合得非常好，这已足以将实验峰归属到各个振动跃迁。
这可以通过检查文件 `example010.asa.o3.rrs.39808.stk` 来完成，
该文件给出每个振动跃迁的强度、拉曼位移和说明。
这实际上是能鉴定实验观测 rR 谱中不同基频、倍频和组合频带的
最一致的流程之一。这样的归属是拟合的必要前提。
本例相对直接，因为 1--1700 cm$^{-1}$ 光谱区域实际上以基频带为主，
而最强的倍频和组合跃迁出现在更高频率。
然而，在许多情形下即使低频光谱范围也以显著的
倍频和组合频带贡献为特征，它们有时甚至比基频跃迁更强！
因此，量子化学计算可以大大促进实验 rR 谱带的归属。

完成归属之后，建议从分析中剔除那些不参与任何
有明显强度的实验观测基频、倍频或组合 rR 谱带的模。
在本例中，这些是上述输入文件中的模 6、8、10--12。
对这些模，拟合的位移参数隐含为零。
您会发现计算得到的位移值确实相当小。
也建议将 `$vib_freq_gs` 块中的基态振动频率改为其实验值。

下面是用于拟合运行的修改后输入文件：

```orca
#
# example010-01.asa.inp
#
# ASA input
#
%sim
         model IMDHO
         method Heller
end

%fit 
    
    Fit true  
    AbsFit true  
    RRSFit true
    AbsExpName "hex-abs.dat"  
    ExpAbsScaleMode Rel
    CWAR  5.0

    NMaxFunc  1000 

    SDNCStep  0.5
                    
end  

$el_states
1
   1 39808.0   150.00    0.00    -0.8533  -3.3690  -0.0000

$el_states_c
1
   1     1        1       0           0        0       0 

$vib_freq_gs
7
    1      354.0
    2      444.0 
    3      934.0
    4     1192.0
    5     1290.0
    6     1403.0
    7     1635.0

$sdnc
7 1
                   1    
      1      -0.594359
      2       0.369227
      3      -0.132430
      4      -0.727616
      5       0.406841
      6       0.177617
      7      -1.412258

$sdnc_c
7 1
             1
      1        1
      2        2
      3        3
      4        4
      5        5
      6        6
      7        7

$rrs_exp 
1         
1 1 
    Ex 39809.0 
    NTr  11
    1     
       int   10.0  1.0
       modes  1
       quanta 1;
    2     
       int   5.0  1.0
       modes  2
       quanta 1;
    3     
       int   1.5  1.0
       modes  3
       quanta 1;
    4     
       int   21.0  1.0
       modes  4
       quanta 1;
    5     
       int   7.5  1.0
       modes  5
       quanta 1;
    6     
       int   2.0  1.0
       modes  6
       quanta 1;
    7     
       int   46.0  1.0
       modes  7
       quanta 1;

    8  
       int  6.8 1.0
       modes  1, 7
       quanta 1, 1;

    9  
       int  4.0 1.0
       modes  2, 7
       quanta 1, 1;

   10  
       int  2.0 1.0
       modes  3, 7
       quanta 1, 1;
   
   11  
       int 17.0 1.0
       modes  7   
       quanta 2;
```

除了基频带的实验强度外，输入文件还包含一些倍频和组合跃迁的信息。
请注意，没有必要把它们全部纳入拟合，
特别是当某些 rR 谱带彼此严重重叠时。

拟合得到的激发态原点简正坐标位移与已发表的值符合得很好：

```orca
$sdnc
7 1
                   1    
      1      -0.638244
      2       0.455355
      3      -0.229126
      4      -0.854357
      5       0.501219
      6       0.197679
      7      -1.292997
```

!!! note

    -   为得到 `.hess` 文件，在频率计算中采用 BHLYP/SV(P) 方法并不重要
        （这样做只是为了与激发态模型参数计算的 TDDFT/BHLYP/SV(P) 方法保持一致）。
        频率计算例如可以在 BP86/TZVP 或 RI-SCS-MP2/TZVP 理论水平进行。
        这将给出与 BHLYP/SV(P) 方法非常相似的位移模式，
        但振动频率准确得多，从而进一步促进 rR 谱的归属
        （[fig:730](#fig:730)）。
        不过，若两种方法给出明显不同的简正模组成和/或振动频率，
        这样的流程可能不一致。根据我们的经验，
        它可能导致某些低频模的激发态位移被显著高估。

    -   已知预测的无量纲简正坐标位移强烈依赖于杂化泛函中
        所包含的"精确" Hartree-Fock 交换（EEX）份额。
        一般而言，不存在对所有体系和态都能给出一致良好描述的通用 EEX 份额。
        通常，对给定分子，BHLYP/TZVP（50% EEX）或 B3LYP/TZVP（20% EEX）
        方法之一在适当标度振动频率后，
        能给出与实验非常吻合的模拟谱。

<a id="sec:spectroscopyproperties.asa.notes"></a>
### 关于正确比较实验与量子化学计算的共振拉曼谱的重要说明（Important Notes about Proper Comparison of Experimental and Quantum Chemically Calculated Resonance Raman Spectra）

为比较实验与理论 rR 谱，**必须在两种情形下使用大约与吸收谱中
同一振动跃迁共振的激发能**。因此，对于弥散的吸收谱
（即不显示已分辨振动结构的谱），需要调整 `%el_states` 块中的
跃迁能和线宽参数，使实验与理论谱的包络大致重合，
然后使用实验激发能数值构造理论 rR 谱。
通常在弥散吸收谱情形下 rR 轮廓相当平滑。
因此，即使激发能不与吸收谱中同一振动跃迁共振，
在这样的不匹配情形下 rR 谱预计也不会显著变化。

对于具有已分辨或部分分辨振动结构的吸收谱，
必须修改 `%el_states` 块中的跃迁能，
使计算与实验观测的 0-0 振动峰重合，
并修改线宽参数，使计算与实验谱中低能斜率的行为相似。

考虑一个单模模型体系，其"实验"与计算吸收谱如 [fig:731](#fig:731) 所示。

<a id="fig:731"></a>
*单模模型体系的实验与理论吸收谱。计算谱经过调整，
使 0-0 峰位置与实验一致。*

计算与实验谱的比较表明，在构造理论 rR 谱之前需要对线宽参数作一些调整。
可以直接比较 16200 cm$^{-1}$ 激发（与 0-0 振动带共振）下的
计算与实验 rR 谱。然而，在计算与另一条振动带共振的 rR 谱时
使用实验激发能数值是不一致的，
因为实验与计算谱中振动峰间距不同，两张谱中峰的位置并不重合。
相反，**应当使用在计算吸收谱中与实验谱中同一振动峰对应的激发能**。
或者，可以调整振动频率的理论值，
使谱中相应振动峰的位置重合，然后使用实验激发能数值计算 rR 谱。

<a id="sec:spectroscopyproperties.asa.fitvalues.scan"></a>
### 示例：*反式*-1,3,5-己三烯中 1-$^1$A$_g$ $\rightarrow$ 1-$^1$B$_u$ 跃迁模型参数的简正模扫描计算（Example: Normal Mode Scan Calculations of Model Parameters for the 1-$^1$A$_g$ $\rightarrow$ 1-$^1$B$_u$ Transition in *trans*-1,3,5-Hexatriene）

若激发态梯度不可用（ORCA 支持的许多电子结构方法都是如此），
您不得不采用更繁琐的流程——在沿体系各简正模位移的几何处进行单点计算。
这大致相当于取数值导数——不过，一旦投入这项额外工作，
就能从计算中得到比解析导数计算可能得到的更多信息。

本例说明了应用简正模扫描计算求取 IMDHO 模型内模拟光谱所需的
激发态简谐参数。该方法可与 CIS、CASSCF、MRCI 或 TD-DFT 等任何方法一起使用。

下面报告的多参考计算的参考波函数是态平均 CASSCF（SA-CASSCF）类型。
完整活性空间 CAS(6,6) 包含全部 6 个价层 $\pi$-轨道。
平均取自前四个态，发现这是包含基态和强允许的
1-$^{1}$B$_{u}$ 态所必需的。

```orca
#
# example011.inp
#
# CASSCF normal mode scan calculations
#

# first do single point RHF calculation
! RHF TZVP TightSCF  

* xyz 0 1
 C       -0.002759    0.680006    0.000000
 H       -0.966741    1.204366    0.000000
 C        1.187413    1.500920    0.000000
 H        2.146702    0.969304    0.000000
 C        1.187413    2.850514    0.000000
 H        0.254386    3.420500    0.000000
 H        2.116263    3.422544    0.000000
 C        0.002759   -0.680006    0.000000
 H        0.966741   -1.204366    0.000000
 C       -1.187413   -1.500920    0.000000
 H       -2.146702   -0.969304    0.000000
 C       -1.187413   -2.850514    0.000000
 H       -0.254386   -3.420500    0.000000
 H       -2.116263   -3.422544    0.000000
*

# perform SA-CASSCF calculation upon appropriate rotation of MOs
$new_job
! TZVP TightSCF  

%scf
    rotate {23,27} end
end 

%casscf
        nel 6
        norb  6
        mult  1
        nroots  4
end

* xyz 0 1
 C       -0.002759    0.680006    0.000000
 H       -0.966741    1.204366    0.000000
 C        1.187413    1.500920    0.000000
 H        2.146702    0.969304    0.000000
 C        1.187413    2.850514    0.000000
 H        0.254386    3.420500    0.000000
 H        2.116263    3.422544    0.000000
 C        0.002759   -0.680006    0.000000
 H        0.966741   -1.204366    0.000000
 C       -1.187413   -1.500920    0.000000
 H       -2.146702   -0.969304    0.000000
 C       -1.187413   -2.850514    0.000000
 H       -0.254386   -3.420500    0.000000
 H       -2.116263   -3.422544    0.000000
*

# do normal mode scan calculations
# to map CASSCF ground and excited-state PESs
$new_job
! TZVP TightSCF  NMScan 

%casscf
        nel 6
        norb  6
        mult  1
        nroots  4
end

%rr
    HessName "hexatriene_bp86.hess"
    NMList 10,11,18,24,26,28,29,31,32
    NSteps 6
    FreqAlter true
    EnStep 0.0001
    State 3
end

* xyz 0 1
 C       -0.002759    0.680006    0.000000
 H       -0.966741    1.204366    0.000000
 C        1.187413    1.500920    0.000000
 H        2.146702    0.969304    0.000000
 C        1.187413    2.850514    0.000000
 H        0.254386    3.420500    0.000000
 H        2.116263    3.422544    0.000000
 C        0.002759   -0.680006    0.000000
 H        0.966741   -1.204366    0.000000
 C       -1.187413   -1.500920    0.000000
 H       -2.146702   -0.969304    0.000000
 C       -1.187413   -2.850514    0.000000
 H       -0.254386   -3.420500    0.000000
 H       -2.116263   -3.422544    0.000000
*
```

包含 Hessian 矩阵的文件（`"hexatriene_bp86.hess"`）
来自 BP86/TZVP 频率计算。关键词 `NMList` 提供待扫描的简正模列表。
这些应当只是全对称振动，因为在 IMDHO 模型的约束下
只有它们对吸收谱和共振拉曼谱可能是重要的。
`FreqAlter` 标志指示扫描后势能面拟合中是否假定频率改变。
参数 `EnStep` 用于在扫描计算中选取合适的步长。
该值的选取使得两个方向上的平均能量变化（以 Eh 为单位）不小于该参数。
