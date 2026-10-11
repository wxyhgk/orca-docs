```{index} NMR, Nuclear Magnetic Resonance
```

(sec:spectroscopyproperties.nmr)=
# 核磁共振（NMR）参数（Nuclear Magnetic Resonance Parameters）

(sec:spectroscopyproperties.nmr.shifts)=
## NMR 化学位移（NMR Chemical Shifts）

HF、DFT（标准 GGA 和杂化泛函）、CASSCF，
以及 RI- 和 DLPNO-MP2 与双杂化 DFT 水平
（参见 {ref}`sec:spectroscopyproperties.properties.eprnmr.MP2magnetic` 一节及其中的参考文献），
再加上耦合簇（GIAO-CCSD、GIAO-CCSD(T)，参见 {ref}`sec:modelchemistries.autoci.autociresp`）
的 NMR 化学位移，均可从 ORCA 的 EPR/NMR 模块获得。
为计算 NMR 屏蔽张量，程序采用规范包含原子轨道
（GIAO，Gauge Including Atomic Orbitals——有时也称为 London 轨道）。{cite}`londonPR37,ditchfieldJCP72,helgakerChemRev99`
在这一途径中引入依赖于磁场的基函数，
从而最小化规范原点依赖性，并保证结果随单电子基组迅速收敛。{cite}`GaussNIC2000`
请注意，GIAO 目前**不可**用于 CASSCF 线性响应，
且必须在 `%eprnmr` 块中提供规范原点
（参见 {ref}`sec:spectroscopyproperties.casscfresp`）。
CASSCF 响应的 GIAO 即将登陆 ORCA！
eprnmr 模块的完整关键词列表见
{ref}`sec:spectroscopyproperties.properties.eprnmr`。

| NMR 化学位移所用方法                                          |GIAO   |
|-------------------------------------------------------------|-------|
| [SCF](sec:essentialelements.cpscf)                          |&check;|
| [RI-MP2 与 DH-DFT](sec:modelchemistries.mp2.rimp2.response)|&check;|
| [DLPNO-MP2](sec:modelchemistries.mp2.dlpnoresp)             |&check;|
| [CASSCF](sec:spectroscopyproperties.casscfresp)             |       |
| [CCSD, CCSD(T)](sec:modelchemistries.autoci.autociresp)     |&check;|


化学位移模块的使用很简单：

```{literalinclude} ../../orca_working_input/C05S13_225.inp
:language: orca
```

屏蔽的输出包含关于顺磁和抗磁贡献、张量的取向、
本征值、其各向同性部分等的详细信息。
对每个原子，给出一个包含这些信息的输出块：

```orca
--------------
 Nucleus   0C :
 --------------

Diamagnetic contribution to the shielding tensor (ppm) :
           209.647        -10.519         0.000
           -26.601        215.858         0.000
            -0.000          0.000       200.382

Paramagnetic contribution to the shielding tensor (ppm):
            59.273         18.302        -0.000
            13.380          6.063        -0.000
             0.000         -0.000        -2.770

Total shielding tensor (ppm):
           268.920          7.783        -0.000
           -13.220        221.921        -0.000
             0.000          0.000       197.611


 Diagonalized sT*s matrix:

 sDSO           200.382          214.507          210.998  iso=     208.629
 sPSO            -2.770            7.279           58.057  iso=      20.855
        ---------------  ---------------  ---------------
 Total          197.611          221.786          269.055  iso=     229.484
```

请注意，所有单位均以 ppm 给出，且所给的化学位移屏蔽是
*绝对*屏蔽（见下文）。
在各原子块的末尾，给出一个总结，列出每个核的各向同性屏蔽
和各向异性 {cite}`masonNMR93`：

```orca
Nucleus  Element    Isotropic     Anisotropy
  -------  -------  ------------   ------------
      0       C          229.484         59.356
      1       C          227.642         62.878
      2       H           56.015         12.469
      3       H           55.460         15.284
      4       H           55.460         15.284
      5       O          334.125        110.616
      6       H           47.337         27.101
      7       H           47.337         27.101
      8       H           64.252         32.114
```

因此，预测 $^{13}$C 核的绝对各向同性屏蔽
为 229.5 和 227.6 ppm，而 $^{17}$O 为 334.1 ppm。
虽然使用 GIAO 时基组收敛迅速且平滑，
但仍建议使用含紧缩指数的基组进行 NMR 计算，
例如专用的 pcSseg-$n$。
不过在多数情况下 TZVPP 或 QZVP 就足够了。{cite}`auerJCP2003,ochsenfledJCTC2014`

需要注意的一点是，为与实验比较，必须为所关注的核类型选取标准分子。
在实验中，NMR 化学位移通常相对于某种标准确定，
例如质子位移用 CH$_{4}$ 或 TMS。
因此，需要分别计算感兴趣分子和给定标准分子的屏蔽，
再用计算值减去参考值得到相对屏蔽。
当然，重要的是参考计算和目标计算必须使用相同的基组和泛函。
若标准选得合适，这也有助于利用误差相消
（一种选择甚至是考虑"内标"——例如用感兴趣的化合物内部
甲基的 $^{13}$C 屏蔽作为参考）。

让我们看一个例子——丙酸（CH$_3$-CH$_2$COOH）。
在 AIST（<http://sdbs.db.aist.go.jp>）等数据库中
可以找到 CDCl$_3$ 中的 $^{13}$C 谱。
化学位移给出为 $\delta_1$ = 8.9 ppm、$\delta_2$ = 27.6 ppm、$\delta_3$ = 181.5 ppm。
虽然直觉已告诉我们羧基的碳屏蔽最小，
因而向低场位移（$\delta$ 值较大），
但让我们看看用 SVP 和 TZVPP 基组
在 HF、BP86 和 B3LYP 理论水平下计算得到什么：

|   method    | $\sigma_1$ | $\sigma_2$ | $\sigma_3$ |
|:-----------:|:----------:|:----------:|:----------:|
|   HF/SVP    |   191.7    |   176.6    |    23.7    |
|  HF/TZVPP   |   183.5    |   167.1    |    9.7     |
|   B86/SVP   |   181.9    |   165.8    |    26.5    |
|  B86/TZVPP  |   174.7    |   155.5    |    7.6     |
|  B3LYP/SVP  |   181.8    |   165.8    |    22.9    |
| B3LYP/TZVPP |   173.9    |   155.0    |    2.9     |

观察这些结果，我们可以发现几点——
首先，使用过小基组的显著影响，差异超过 10 ppm。
其次，通过 DFT 纳入电子相关后结果变化很大，且依赖于泛函。
最后但同样重要的是，这些数值与实验值毫无共同之处
（变化顺序是错的），
因为计算给出的是如上表那样的*绝对屏蔽*，
而实验值是*相对位移*，这里相对于 TMS。

为获得相对位移，我们计算标准分子（TMS）的屏蔽
$\sigma_{TMS}$（TMS HF/TZVPP: 194.1 ppm，
BP86/TZVPP: 184.8 ppm，B3LYP/TZVPP: 184.3 ppm），
再用 $\delta_{mol} = \sigma_{ref} - \sigma_{mol}$
即可计算化学位移（单位 ppm）并与实验直接比较：

|   method    | $\delta_1$ | $\delta_2$ | $\delta_3$ |
|:-----------:|:----------:|:----------:|:----------:|
|  HF/TZVPP   |    10.6    |    27.0    |   184.4    |
|  B86/TZVPP  |    10.1    |    29.3    |   177.2    |
| B3LYP/TZVPP |    10.4    |    29.3    |   181.4    |
|    Exp.     |    8.9     |    27.6    |   181.5    |

关于 ORCA 中 GIAO 的实现，有几点需要说明。
使用 GIAO 会导致一些相当复杂的分子单电子和双电子积分，
以及耦合微扰 SCF 方程右端的若干额外项。
其中双电子贡献尤其耗时。
因此实现了 RIJK、RIJDX 和 RIJCOSX 近似并作了测试。{cite}`stoychevNMRBench`
默认情况下，SCF 所用的近似也应用于 GIAO 积分，
但后者可通过 eprnmr 输入块中的 `GIAO_2el` 关键词更改
（参见 {ref}`sec:spectroscopyproperties.properties.eprnmr` 一节）。
请注意，虽然默认的 COSX 网格对化学位移通常足够精确，
但对特殊情形或 post-HF 计算建议使用 `defgrid3`。

用户可以精细控制对哪些核计算位移
（尽管这不会显著降低计算成本，后者由磁场的 CP-SCF 方程主导）。
其方式与下一节描述的超精细耦合和四极耦合完全相同。例如：

```{literalinclude} ../../orca_working_input/C05S13_225a.inp
:language: orca
```

NMR 化学位移也已与隐式溶剂模型结合实现，
因此 NMR 关键词可与 CPCM 输入块组合使用。
请注意，对于包含隐式溶剂的计算，
强烈建议也用同一模型优化几何结构。
无论如何，NMR 中可观测的显式溶剂-溶质相互作用（如氢键）
无法用这样的模型描述：溶剂分子必须显式包含在计算中。

(sec:spectroscopyproperties.nmr.coupling)=
## NMR 自旋-自旋耦合常数（NMR Spin-Spin Coupling Constants）
```{index} NMR Spin-Spin Coupling Constants, Spin-Spin Coupling Constants 
```

溶液中分子 NMR 谱观测到的间接自旋-自旋耦合常数
由四项贡献组成：抗磁自旋-轨道项：

$$\hat{H}_{DSO}=\frac{1}{2}  \sum_{ikl} \frac{ (\vec{M}_k \times \vec{r}_{ik})(\vec{M}_l \times \vec{r}_{il}) }{r_{ik}^3 ~ r_{il}^3} 
$$ (eqn:SSCC_DSO)

顺磁自旋-轨道项：

$$\hat{H}_{PSO}=\sum_{ik}\frac{\vec{M}_k ~ \vec{l}_{ik} }{r_{ik}^3}
$$ (eqn:SSCC_PSO)

费米接触项：

$$\hat{H}_{FC}=\frac{8 ~ \pi}{3}\sum_{ik}\delta(r_i-r_k) ~ \mathbf{m}_k 
$$ (eqn:SSCC_FC)

以及自旋偶极项：

$$\hat{H}_{SD}=\sum_{ik} \mathbf{m}_k^T ~ \frac{3 ~ \mathbf{r}_{ik} ~ \mathbf{r}_{ik}^{~T}-r_{ik}^2 }{ r_{ik}^5} ~ \mathbf{s}_{i}
$$ (eqn:SSCC_SD)

虽然费米接触项通常最重要，
但所有贡献都可在 ORCA 的 HF 和 DFT 理论水平下计算。
为此，需在 eprnmr 输入块中调用关键词 `ssall`，
而四个项可分别用 `ssdso`、`sspso`、`ssfc` 和 `sssd` 请求。例如：

```{literalinclude} ../../orca_working_input/C05S13_225c.inp
:language: orca
```

结果以 Hz 给出。请注意，默认使用的同位素
可能不是计算 NMR 性质所期望的，
因此建议用 `ist` 标志定义相应的同位素。
也可以用标志 `PrintReducedCoupling=True`
打印约化耦合常数 $K$（单位为 $10^{19}\cdot\mathrm T\cdot \mathrm J^{-2}$），
它与核同位素无关。

CP-SCF 方程必须对每一对中的一个核求解，是计算的瓶颈。
因此，自旋-自旋耦合常数只在彼此距离一定范围内
（默认 5 埃）的核之间计算。
后者可用关键词 `SpinSpinRThresh` 更改。

若请求了多个核素，也可用关键词 `SpinSpinElemPairs`
只选择某些元素对（例如只选 C--H 和 H--H，不含 C--C）。
类似地，关键词 `SpinSpinAtomPairs` 选择要考虑的实际核对。
后两选项的并集用于*缩减*用 `Nuclei` 输入所做的选择，
之后再应用 `SpinSpinRThresh`。

下面是另一个说明这些附加选项的例子：

```{literalinclude} ../../orca_working_input/C05S13_225d.inp
:language: orca
```

(sec:spectroscopyproperties.nmr.spectrum)=
## 模拟 NMR 谱（Simulating NMR Spectra）

由计算得到的 NMR 屏蔽和自旋-自旋耦合常数，
可以模拟耦合的 NMR 谱。
最典型的 NMR 实验是去耦的 $^{13}$C 谱和耦合的 $^1H$ 谱，
因此这里我们聚焦于这两种。
为模拟完整的 NMR 谱，我们以巴豆酸乙酯为例，
需要三个步骤：1) 计算自旋-自旋耦合常数，
2) 计算化学位移屏蔽，3) 用自旋哈密顿量形式模拟谱图。
请注意，这些步骤可以独立进行，
屏蔽和耦合可以使用不同的理论水平，
且步骤 1 和 2 的顺序无关紧要。

此外，若谱图要以 TMS 为参考进行模拟，
则需要 TMS 的屏蔽值（此处氢和碳的值分别为 31.77 和 188.10 ppm）。
下面是耦合常数计算的输入，命名为 `ethylcrotonate_sscc.inp`：

```{literalinclude} ../../orca_working_input/C05S13_225e.inp
:language: orca
```

自旋-自旋耦合常数将存储在文件 `ethylcrotonate_sscc.property.txt` 中，
NMR 谱模拟需要读取它。
NMR 屏蔽将在下一步计算，其输入 `ethylcrotonate_nmr.inp` 如下：

```{literalinclude} ../../orca_working_input/C05S13_225f.inp
:language: orca
```

最终的 NMR 谱模拟用 `orca_nmrspectrum` 进行，
它需要一个单独的输入文件 `ethylcrotonate.nmrspec`，如下所示
（注意必需的末尾 END 语句）：

```orca
NMRShieldingFile = "ethylcrotonate_nmr"   #property file for shieldings
NMRCouplingFile  = "ethylcrotonate_sscc"  #property file for couplings
NMRSpecFreq = 80.00                   #spectrometer freq [MHz] (default 400)
PrintLevel = 0                        #PrintLevel for debugging info
NMRCoal = 1.0                         #threshold for merged lines [Hz] (default 1)
NMRREF[1] 31.77                       #shielding for 1H reference [ppm]
NMRREF[6] 188.10                      #shielding for 13C reference [ppm]
NMREquiv                              #lists of NMR-equivalent nuclei
1 {13 14 15} end                      #H 13,14,15 are equivalent (methyl)
2 {16 17} end                         #H 16 and 17 equivalent (ethyl)
3 {8 10 11} end                       #H 8,10,11 again equivalent methyl
end                                   #end equiv nucl block
END                                   #essential end of input
```

其中包含以下关键词：\
`NMRShieldingFile` 和 `NMRCouplingFile` 表示 `.property.txt` 文件，
NMR 谱模块将从中读取屏蔽张量和耦合常数。
若未给出该行，程序将期望屏蔽或耦合在当前计算的 property 文件中。

`NMRSpecFreq` NMR 谱仪频率（单位 MHz）对谱图的外观至关重要，
因为屏蔽以 ppm 给出，而耦合以 Hz 给出。默认为 400 MHz。

`NMRCoal` 若两条谱线比该阈值（单位 Hz）更接近，
则模块会将它们合并为一条强度加倍的谱线。默认为 1 Hz。

`NMRREF[X]` 元素 X 的绝对屏蔽参考值，
用于模拟谱图中的相对位移。
通常这些是例如单独的 TMS 计算得到的绝对屏蔽值，
在模拟谱图中将位于零 ppm。

`NMREquiv` 用户必须指定 NMR 等价核的分组。
这些通常是在 NMR 时间尺度上互换的原子，如甲基质子。
屏蔽和耦合将对用户指定的每个分组取平均。

用这个输入，`orca_nmrspectrum` 以两个参数调用，
第一个是包含分子所有信息的 gbw 文件，
通常是 nmr 或 sscc 计算的 gbw 文件，
第二个是上面给出的输入文件名：

```orca
orca_nmrspectrum ethylcrotonate_nmr.gbw ethylcrotonate.nmrspec > output
```

若执行此计算，NMR 谱模块将读取文件
`ethylcrotonate_sscc.property.txt` 和 `ethylcrotonate_nmr.property.txt`，
提取屏蔽和耦合，对等价核取平均，并为每个核建立有效 NMR 自旋哈密顿量：

$${H}_{NMR}(p,q)= \sigma_{p} \delta_{pq} + J_{pq} I_p I_q.
$$ (eqn:effNMRspinH)

:::{Caution}
这包括该核自旋所耦合的所有核，
且不应包含太多自旋（见 `SpinSpinRThres`），
因为每个原子及其所耦合核的自旋哈密顿量是用暴力法对角化的。
之后，所有自旋激发被累积并合并为每种元素的最终谱图。
对于巴豆酸乙酯，NMR 谱输出如下：

```orca
----------------------------------------------------- 
 NMR Peaks for atom type 1, ref value  31.7700 ppm : 
----------------------------------------------------- 
Atom   shift[ppm]   rel.intensity  
   8        2.34    9.00 
   8        2.36    9.00 
   8        2.25    9.00 
   8        2.27    9.00 
   9        6.34    1.00 
   9        6.36    3.00 
   9        6.38    3.00 
   9        6.41    1.00 
   9        6.14    1.00 
   9        6.16    3.00 
   9        6.19    3.00 
   9        6.21    1.00 
  12        7.95    1.00 
  12        7.85    3.00 
  12        7.75    4.00 
  12        7.65    4.00 
  12        7.56    3.00 
  12        7.47    1.00
  13        1.71    9.00 
  13        1.61   18.00 
  13        1.52    9.00 
  16        4.56    4.00 
  16        4.46   12.00 
  16        4.37   12.00 
  16        4.27    4.00 

----------------------------------------------------- 
 NMR Peaks for atom type 6, ref value 188.1000 ppm : 
----------------------------------------------------- 
Atom   shift[ppm]   rel.intensity  
   2       25.70    1.00 
   3      155.15    1.00 
   4       19.96    1.00 
   5       68.91    1.00 
   6      174.39    1.00 
   7      130.29    1.00 

----------------------------------------------------- 
 NMR Peaks for atom type 8, ref value 104.8826 ppm : 
----------------------------------------------------- 
Atom   shift[ppm]   rel.intensity  
   0        0.00    5.00 
   1      149.74    5.00
```
:::

第一列是信号来源核的原子编号，
第二列是谱线位置（单位 ppm），第三列是信号的相对强度。
对氧未给出参考值，因此程序会自动将计算中得到的最低值设为参考值。

例如用 gnuplot 绘制谱图，
可得到 $^{13}$C 和 $^1H$ 的如下谱图 [^1]：

(fig:crotonate)=
```{figure} ../../images/ethyl_crotonate_sim.*

模拟的 $^13C$（上）和 1H（下）NMR 谱。请注意，由于只计算了 HH 耦合，
谱图不包含任何 CH 耦合，碳谱也是未耦合的。
```

这使得与实验比较和评估计算参数变得容易得多，
但它不像其他代码那样先进，
例如不考虑构象自由度等。
请注意，相应的 property 文件也可以修改，
以对计算得到的屏蔽和耦合作微调。

(sec:spectroscopyproperties.nmr.tensors)=
## 用 `orca_plot` 可视化屏蔽张量

为进行可视化，建议执行一次 ORCA NMR 计算，
使得 `orca_plot` 所需的相应 `gbw` 和 `density` 文件
通过 `!keepdens` 关键词与 `!NMR` 一起生成。
若以交互模式调用 `orca_plot`（指定 `orca_plot myjob.gbw -i`；
注意 `myjob.gbw`、`myjob.densities` 和 `myjob.property.txt`
必须在当前目录中），
然后选择 `1 - type of plot`，再选 `17 - shielding tensor`，
确认 property 文件名，最后选 `11 - Generate the plot`，
就会生成一个 `.cube` 文件，
其中屏蔽张量在相应核处以椭球表示。
这些可用例如 Avogadro 绘制，
建议等值面值取 1.0 左右，cube 文件的网格稍密一些（如 100x100x100）。
用 Avogadro 为 CF$_3$SCH$_3$ 生成的典型图如下 [^2]：

(fig:shielding_tensors_cf3)=
```{figure} ../../images/cf3sch3_st.*

CF$_{3}$SCH$_{3}$ 中每个原子的屏蔽张量已在相应核处
绘为椭球（a、b 和 c 轴分别对应屏蔽张量归一化主轴）。
```

(sec:spectroscopyproperties.nmr.NICS)=
## 与核无关的化学位移（Nucleus-independent chemical shielding）
```{index} Nucleus-independent chemical shielding, NICS
```

芳香性是化学中的一个基本概念，
其分析在量子化学中备受关注。
理解芳香性的一种可能是
在 $\pi$ 体系附近采样 NMR 中的环电流效应。
由于这不是通过检查任何原子的化学位移来完成的，
该量称为与核无关的化学位移（nucleus independent chemical shielding，NICS）。
通常，一个"哑"原子被放在环的中心和/或距环一定距离处。
在 ORCA 中，需要使用虚原子（ghost atom），例如 "`H:`"，
以确保程序在感兴趣的区域生成 DFT 或 COSX 网格点。
出于技术原因，该原子也必须至少有一个基函数，
可用 `NewGTO` 设置。
一个指数足够大的 s 函数不会与分子中任何其他基函数重叠，
因此不会影响结果，只是满足技术要求
（请注意，额外的网格点可能通过提高数值积分精度
改变部分计算结果）。
若使用 RI，还必须向 AuxJ、AuxJK 和/或 AuxC 基组添加哑拟合函数。
苯的典型输入如下：

```orca
! TightSCF NMR PBE def2-TZVP RI def2/J
* gzmt 0 1
 H:                            NewGTO S 1 1 1e6 1 end NewAuxJGTO S 1 1 2e6 1 end
 H:  1   1                     NewGTO S 1 1 1e6 1 end NewAuxJGTO S 1 1 2e6 1 end
 C   1   1.39    2   90
 C   1   1.39    2   90  3   60
 C   1   1.39    2   90  4   60
 C   1   1.39    2   90  5   60
 C   1   1.39    2   90  3  -60
 C   1   1.39    2   90  6   60
 H   3   1.09    4   120 1   180
 H   4   1.09    3   120 1   180
 H   5   1.09    4   120 1   180
 H   6   1.09    5   120 1   180
 H   7   1.09    3   120 1   180
 H   8   1.09    7   120 1   180
*
```

(sec:spectroscopyproperties.nmr.shielding-decomposition)=
## 屏蔽张量的轨道分解（Shielding tensor orbital decomposition）
```{index} NMR Shielding Tensor Orbital Decomposition
```

可以将 NMR 屏蔽张量分解为轨道或轨道对贡献。
一种选择是自然化学位移（Natural Chemical Shielding）分析
（参见 {ref}`sec:spectroscopyproperties.nbo.ncsanalysis` 一节），
这里介绍另一种。
核 $A$ 的屏蔽张量可精确分解如下：

$$\begin{aligned}
\boldsymbol{\sigma}^A &=
  \sum_{p}\left(  \boldsymbol{\sigma}^{A,\text{para} }_p + \boldsymbol{\sigma}^{A,\text{dia} }_p
  \right)\\
\boldsymbol{\sigma}^{A,\text{para/dia} }_i &=
  \boldsymbol{\sigma}^{A,\text{para/dia} }_{ii}
  +\frac{1}{2}\sum_{j\ne i}\left(  \boldsymbol{\sigma}^{A,\text{para/dia} }_{ij} + \boldsymbol{\sigma}^{A,\text{para/dia} }_{ji}
  \right)  +\sum_{a}\left(  \boldsymbol{\sigma}^{A,\text{para/dia} }_{ia} + \boldsymbol{\sigma}^{A,\text{para/dia} }_{ai}
  \right)\\
\boldsymbol{\sigma}^{A,\text{para/dia} }_a &=
  \boldsymbol{\sigma}^{A,\text{para/dia} }_{aa}
  +\frac{1}{2}\sum_{b\ne a}\left(  \boldsymbol{\sigma}^{A,\text{para/dia} }_{ab} + \boldsymbol{\sigma}^{A,\text{para/dia} }_{ba}
  \right) 
\\
\boldsymbol{\sigma}^{A,\text{para} }_{pq} &= D^\mathbf{B}_{pq} h^{\mathbf{M}_A}_{pq}
\\
\boldsymbol{\sigma}^{A,\text{dia} }_{pq} &= D_{pq} h^{\mathbf{B,M}_A}_{pq}
\\
D_{pq} &= \sum_{\mu\nu\kappa\lambda} c_{\mu p} S_{\mu\nu} D_{\nu\kappa} S_{\kappa\lambda} c_{\lambda q}
\\
D^\mathbf{B}_{pq} &= \sum_{\mu\nu\kappa\lambda} c_{\mu p} S_{\mu\nu} D^\mathbf{B}_{\nu\kappa} S_{\kappa\lambda} c_{\lambda q}
\\
h^{\mathbf{M}_A}_{pq} &= \sum_{\mu\nu} c_{\mu p} h^{\mathbf{M}_A}_{\mu\nu} c_{\nu q}
\\
h^{\mathbf{B,M}_A}_{pq} &= \sum_{\mu\nu} c_{\mu p} h^{\mathbf{B,M}_A}_{\mu\nu} c_{\nu q}\end{aligned}$$

请注意，对于 SCF 方法（HF 或 DFT），
$\boldsymbol{\sigma}^{A,\text{para/dia} }_a=0$。
要请求该分析，必须用关键词 `LocOrbGBW` 给出有效的 GBW 文件，
其中可含同一基下的任何正交归一 MO，
例如正则轨道或定域轨道，
不过上述分解假定布里渊条件成立，
若对例如 NBO 执行可能会有误导。
打印超过 0.01 ppm 的轨道贡献——目前用户不可配置。
分离的轨道对贡献也可用 `Printlevel=3` 打印。
下面的示例输入为甲醛计算 HF 和 RI-MP2 屏蔽，
并将其分解到 Pipek--Mezey 定域轨道上
（注意虚轨道可能定域得不好——`AHFB` 在那里更合适）。
第二个子计算只是打印 LMO，以便用 Avogadro 方便地可视化。

```{literalinclude} ../../orca_working_input/H2CO_NMR_local_analysis.inp
:language: orca
```

(sec:spectroscopyproperties.nmr.tau)=
## Meta-GGA 泛函中 Tau 的处理

对于基于 GIAO 的 meta-GGA 计算，
动能密度 $\tau$ 有不同的可选方案。
与流无关的 $\tau_0$ 不是规范不变的。
忽略产生规范依赖性的那些项，
会导出一种特设的规范不变处理（直到 ORCA 5 这一直是默认）。
Maximoff 和 Scuseria 提出了一种含外磁场显式依赖的
规范不变定义 $\tau_\text{MS}$。{cite}`Maximoff2004`
然而，该拟设会对屏蔽张量产生非物理的顺磁贡献。{cite}`Schattenberg2021`
最后一种方案由 Dobson 引入 {cite}`Dobson1993`，
它是规范不变的，但即使对纯密度泛函也需要求解 CP-SCF 方程。
关于这些方案的讨论和比较见参考文献 {cite}`Bates2012`（在 TDDFT 语境下）
和 {cite}`Reimann2015,Schattenberg2021`（在 NMR 屏蔽语境下）。
请注意，不同方案计算得到的屏蔽可能相差很大！
其他一些电子结构程序默认使用 MS 拟设，
因此在比较不同代码的结果时要小心。
在 ORCA 中，基于 GIAO 的计算中 $\tau$ 的处理选择如下

```orca
%eprnmr	
  Tau 0      # gauge-variant
      GI     # ad-hoc gauge-invariant
      MS     # field-dependent, gauge-invariant version of Maximoff and Scuseria
      Dobson # (default) current density-dependent, gauge-invariant version
             # of Dobson
  end
```

(sec:spectroscopyproperties.properties.eprnmrConv)=
## EPR 和 NMR 张量的笛卡尔指标约定（Cartesian Index Conventions）
```{index} Cartesian Index Conventions for EPR and NMR Tensors, NMR Tensors Index Conventions, EPR Tensors Index Conventions 
```

NMR 屏蔽张量 $\boldsymbol{\sigma}$ 以及 EPR $g$ 和 $A$ 张量
一般是非对称矩阵。因此了解其笛卡尔指标的约定很重要。
这些约定规定了各自自旋哈密顿量中矢量-矩阵-矢量乘法的顺序。
除非另有说明，ORCA 采用如下约定：

对于 NMR 屏蔽张量，核塞曼哈密顿量取如下形式：

$$H_{\!I} = -g_N\beta_N\mathbf{B}(\mathbf{1} - \boldsymbol{\sigma})\mathbf{I},$$

其中 $\mathbf{B}$ 是外加磁场矢量。

对于 EPR $g$ 和 $A$ 张量，EPR 自旋哈密顿量取如下形式：

$$
H_S = \beta_e \mathbf{B}\mathbf{g}\mathbf{S} + \mathbf{S}\mathbf{A}\mathbf{I}.
$$ (eq:g_A_convention)

```{index} Paramagnetic NMR Shielding Tensors, PNMR
```
(sec:spectroscopyproperties.pnmr)=
## 顺磁 NMR 屏蔽张量（Paramagnetic NMR Shielding Tensors）

对于自旋 $S>0$ 的体系，核屏蔽包含一项来自
未配对电子顺磁性的贡献。[^3]
该项依赖于温度，称为"顺磁屏蔽"（$\boldsymbol{\sigma}^\mathrm{p}$）。
它加到与温度无关的屏蔽贡献（也称为"轨道"贡献）上：

$$\boldsymbol{\sigma} = \boldsymbol{\sigma}^\mathrm{orb} + \boldsymbol{\sigma}^\mathrm{p}.$$

ORCA 目前支持对顺磁性可用有效 EPR 自旋哈密顿量描述的体系
计算 $\boldsymbol{\sigma}^\mathrm{p}$：

$$
H_S = \mathbf{S}\mathbf{D}\mathbf{S} + \beta_e \mathbf{B}\mathbf{g}\mathbf{S} + \mathbf{S}\mathbf{A}\mathbf{I}.
$$ (eq:pnmr_SHam)

理论背景见参考文献
{cite}`VandenHeuvel2013,Soncini2013`。这里我们复述主要方程。

对于由式 {eq}`eq:pnmr_SHam` 描述的自旋态，
顺磁屏蔽张量由下式给出

$$
 \boldsymbol{\sigma}^\mathrm{p} = -\frac{\beta_e S(S+1) }{g_N\beta_N 3kT}
 \mathbf{g}\mathbf{Z}\mathbf{A},
$$ (eq:pnmr_sigma)

其中 $\mathbf{Z}$ 是一个无量纲的 $3\times3$ 矩阵，
由 ZFS 和温度确定，如下：
对角化 ZFS 哈密顿量 $\mathbf{S}\mathbf{D}\mathbf{S}$
得到能级 $E_\lambda$ 和本征态 $|S\lambda a\rangle$，
其中若 $E_\lambda$ 简并，则 $a$ 标记简并态。
然后 $\mathbf{Z}$ 定义为（$i,j=x,y,z$）

$$\begin{gathered}
Z_{ij} = \frac{3}{S(S+1) }\frac{1}{Q_0} \sum_\lambda e^{-E_\lambda/kT}
  \Bigg[\sum_{a,a'}\langle S\lambda a|S_i|S\lambda a'\rangle\langle S\lambda a'|S_j|S\lambda
  a\rangle\\ +2kT\sum_{\lambda'\neq\lambda}\sum_{a,a'} \frac{\langle S\lambda a|S_i|S\lambda'
  a'\rangle\langle S\lambda' a'|S_j|S\lambda a\rangle }{E_{\lambda'}-E_\lambda} \Bigg],\end{gathered}$$
  
其中 $Q_0 = \sum_{\lambda',a} e^{-E_\lambda/kT}$ 表示配分函数。
按上式定义的 $\mathbf{Z}$ 矩阵的一个重要性质是：
当 $\mathbf{D}/kT$ 趋于零时，它趋于单位矩阵。

屏蔽的轨道部分 $\boldsymbol{\sigma}^\mathrm{orb}$
按与闭壳层分子相同的方式计算。
它在 ORCA 中适用于非限制 HF 和 DFT 方法以及 MP2
（关于后者，更多信息见
{ref}`sec:spectroscopyproperties.properties.eprnmr.MP2magnetic` 一节）。

`orca_pnmr` 工具使用式
[\[eq:pnmr_sigma\]](#eq:pnmr_sigma){reference-type="eqref"
reference="eq:pnmr_sigma"} 来计算
$\boldsymbol{\sigma}^\mathrm{p}$。
`orca_pnmr` 的用法见
{ref}`sec:utilities.pnmr` 一节。

[^1]: 使用 gnuplot 的基本绘图选项是
    `plot "mydata" using 2:3 w i, "mydata" using 2:3:1 with labels`

[^2]: 同样的方案可用于在分子框架中用 `orca_plot`
    可视化极化率张量。

[^3]: 关于顺磁 NMR 的综合综述，参见例如
    {cite}`Pell2018`。


```{index} Spin-Rotation Constants
```
(sec:spectroscopyproperties.properties.eprnmr.spinrot)=
## 自旋-转动常数（Spin-rotation Constants）

自旋-转动常数的计算按照 {cite}`Gauss1996_spinrot`
采用依赖于微扰的原子轨道实现。
如该文献式 34 所给，核 $K$ 的自旋-转动张量 $\mathbf{M}_K$，
与用 GIAO 计算的核屏蔽张量 $\boldsymbol{\sigma}_K^\text{GIAO}$、
以及规范原点设在该核处的屏蔽张量抗磁部分
$\boldsymbol{\sigma}_K^\text{dia}(\mathbf{R}_K)$ 相关联：

$$ 
\mathbf{M}_K = 
2 \gamma_K \left( \boldsymbol{\sigma}_K^\text{GIAO}  
- \boldsymbol{\sigma}_K^\text{dia}(\mathbf{R}_K) \right) \mathbf{I}^{-1}
- \mathbf{M}_K^\text{nuc}
$$

其中 $\mathbf{M}_K^\text{nuc}$ 是核分量（见该文献式 14），
$\mathbf{I}$ 是惯量张量，$\gamma_K$ 是核旋磁比。
因此，当请求自旋-转动常数时，ORCA 也会自动用 GIAO 计算 NMR 屏蔽。
请注意，eprnmr 模块的完整关键词列表见
{ref}`sec:spectroscopyproperties.properties.eprnmr`。

下面的输入展示了 H{sub}`2`{sup}`12`C{sup}`17`O 中
$\mathbf{M}(^{17}\text{O})$ 的示例计算：

```{literalinclude} ../../orca_working_input/h2co_spinrot.inp
:language: orca
```

:::{note}
- 所用旋磁比既可通过 `ist` 选择正确同位素更改，
  也可通过 `ssgn` 直接提供核 g 因子。
- 计算惯量张量所用的质量与所选同位素无关！
  上面的例子通过 `Mass2016` 关键词请求最丰度同位素的原子质量，
  并显式指定 {sup}`12`C（这是默认）和 {sup}`17`O 的质量。
:::


(sec:spectroscopyproperties.properties.eprnmr)=
## EPRNMR —— 磁性质关键词
```{index} NMR Keywords EPRNMR
```

可在 `%eprnmr` 输入块中请求 EPR 和 NMR 响应性质的计算。
各个标志如下所给。

```orca
%eprnmr
  # Calculate the g-tensor using CP-KS theory
  gtensor true
  # Calculate and print one- and two-electron contributions to the g-tensor
  gtensor_1el2el true

  # Calculate the D-tensor
  DTensor so      # spin orbit part
          ss      # spin-spin part
          ssandso # both parts
  DSOC    qro     # quasi-restricted method; must be done with the keyword !uno
          pk      # Pederson-Khanna method.
                  # NOTE: both approximations are only valid for
                  # pure functionals (no HF exchange)
          cp      # coupled-perturbed method (default)
          cvw     # van W\"ullen method
  DSS     direct  # directly use the canonical orbitals for the spin density
          uno     # use spin density from UNOs

  PrintLevel n    # Amount of output (default 2)

  # whether to calculate and print the Euler angles via `orca_euler` if the
  # calculation of the g-tensor or the D-tensor is requested
  PrintEuler false

  # For the solution of the CP-SCF equations:
  Solver   Pople  # Pople solver (default)
           CG     # conjugate gradient
           DIIS   # DIIS type solver
  MaxIter  64     # maximum number of iterations
  MaxDIIS  10     # max. number of DIIS vectors (only DIIS)
  Tol      1e-3   # convergence tolerance
  LevelShift 0.05 # level shift for DIIS (ignored otherwise)

  Ori     CenterOfElCharge  # center of electronic charge
          CenterOfNucCharge # center of nuclear charge
          CenterOfSpinDens	# center of spin density
          CenterOfMass      # center of mass
          GIAO              # use the GIAO formalism (default)
          N                 # number of the atom to put the origin
          X,Y,Z             # explicit position of the origin 
                            # in coordinate input units (Angstrom by default)

  # Calculate the NMR shielding tensor
  NMRShielding 1 # for chosen nuclei - specified with the Nuclei keyword
               2 # for all nuclei - equivalent to the 'NMR' simple input keyword

  # treatment of 1-electron integrals in the RHS of the CPSCF equations
  giao_1el = giao_1el_analytic   # analytical, default
             giao_1el_numeric    # numerical - for testing only

  # treatment of 2-electron integrals in the RHS of the CPSCF equations
  # various options for combination of approximations in Coulomb (J) and
  # exact (HF) exchange (K) part. The default is the same as used for the SCF.
  giao_2el = giao_2el_rijk        # RIJK approximation
             giao_2el_same_as_scf # use same scheme as in SCF
             giao_2el_analytic    # fully analytical
             giao_2el_rijonx      # RIJ approximation with analytical K
             giao_2el_cosjonx     # COSJ approximation with analytical K
             giao_2el_rijcosx     # RIJ approximation with COSX approximation
             giao_2el_cosjx       # COSJ approximation with COSX apprxomation
             giao_2el_exactjcosx  # exact J with COSX approximation
             giao_2el_exactjrik   # exact J with RIK approximation
             
  # for g-tensor calculations using the SOMF-operator for the SOC 
  # treatment, the 2-electron contribution to the GIAO terms can be 
  # computed as well, but they take much more time and usually do not
  # contribute significantly and therefore are disabled by default
  do_giao_soc2el false

  # treatment of tau in meta-GGA DFT - see above
  Tau = Dobson # (default) Other options: 0, MS, GI

  # use effective nuclear charges for the gauge correction to the A-tensor
  # (this makes sense if an effective 1-electron SOC operator is used)
  hfcgaugecorrection_zeff true

  # calculate diamagnetic spin-orbit (DSO) integrals needed for the gauge
  # correction to the A-tensor numerically (faster than the analytical way)
  hfcgaugecorrection_numeric true

  # Grid settings for the above: <0 means to use the DFT grid setting
  hfcgaugecorrection_angulargrid -1
  hfcgaugecorrection_intacc      -1
  hfcgaugecorrection_prunegrid   -1
  hfcgaugecorrection_bfcutoff    -1
  hfcgaugecorrection_wcutoff     -1

  Nuclei = all type { flags }
    # Calculate nuclear properties. Here the properties
    # for all nuclei of "type" are calculated ("type" is
    # an element name, for example Cu.)
    # Flags can be the following:
    #   aiso  - calculate the isotropic part of the HFC
    #   adip  - calculate the dipolar part of the HFC
    #   aorb  - 2nd order contribution to the HFC from SOC
    #   fgrad - calculate the electric field gradient
    #   rho   - calculate the electron density at the
    #           nucleus
    #   shift - NMR shielding tensor (orbital contribution)
    #   srot  - spin-rotation tensor
    #   ssdso - spin-spin coupling constants, diamagnetic spin orbit term 
    #   sspso - spin-spin coupling constants, paramagnetic spin orbit term
    #   ssfc  - spin-spin coupling constants, Fermi contact term
    #   sssd  - spin-spin coupling constants, spin dipole term 
    #   ssall - spin-spin coupling constants, calculate all above contributions 

  # In addition you can change several parameters
  # e.g. for a different isotope.
  Nuclei = all N { PPP=39.1, QQQ=0.5, III=1.0 };
      # PPP   - the HFC proportionality factor for this nucleus
      #         = ge*gN*betaE*betaN
      # QQQ   - the quadrupole moment for this nucleus
      # III   - the spin for this nucleus
      # ist   - isotope
      # ssgn  - nuclear g-factor for spin-spin coupling
      #         and spin-rotation constants (overrides ist)

  # For example:
  # calculates the hyperfine coupling for all nitrogen atoms
  Nuclei = all N { aiso, adip, fgrad, rho};

  # calculates the spin-spin coupling constants for all carbon atoms
  # assuming all carbon atoms are 13C
  Nuclei = all C { ssall, ist = 13};

  # You can also calculate properties for individual atoms
  # as in the following example:
  Nuclei = 1,5,8 { aiso, adip};

  # NOTE: Counting starts with atom 1!
  # WARNING: All the nuclei, mentioned in one line 
  # as above will be assigned the same parameters !

  # For spin-spin coupling constants, a distance threshold is 
  # applied in the eprnmr block to restrict the number of couplings
  # to be computed, given in Angstroms:
  SpinSpinRThresh 5.0 # default

  # Coupling can be restricted to certain element pairs
  # (if they are added to the "Nuclei" list and are within RThresh).
  # The syntax accepts multiple pairs of element symbols or
  # atomic numbers or "*" as a wildcard
  SpinSpinElemPairs {C C} {H *} {6 7} # default is {* *}, i.e. all

  # Similarly, coupling can be restricted to certain atom pairs
  # (if they are added to the "Nuclei" list and are within RThresh).
  # The syntax accepts multiple pairs of indices (starting at 0!)
  # or "*" as a wildcard
  SpinSpinAtomPairs {1 0} {5 *} # default is {* *}, i.e. all

  # whether to print reduced spin-spin coupling constants
  PrintReducedCoupling false

  end
```
