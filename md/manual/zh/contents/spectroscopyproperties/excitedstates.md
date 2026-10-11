```{index} Excited States Calculations
```

(sec:spectroscopyproperties.excitedstates)=
# 激发态计算（Excited States Calculations）

ORCA 中存在大量计算激发态的方法。
这里我们简要概述主要方法，重点介绍每种方法的基本用法
和当前功能。每种方法的详细文档在各小节中指出。

多参考方法（如 NEVPT2 或 MRCI）在手册的其他地方描述
（{ref}`sec:modelchemistries.nevpt2`、{ref}`sec:modelchemistries.mrci`）。

```{index} TD-DFT
```
(sec:spectrochemistryproperties.excitedstates.tddft)=
## 用 RPA、CIS、TD-DFT 和 SF-TDA 计算激发态（Excited States with RPA, CIS, TD-DFT and SF-TDA）

ORCA 提供一个模块来执行 TD-DFT、单激发组态相互作用（CIS）和 RPA。
该模块适用于闭壳层（RHF 或 RKS）或非限制性（UHF 或 UKS）参考波函数。
对于 DFT 模型，模块自动选择 TD-DFT；对于 HF 波函数，则选择 CIS 模型。
如果 SCF 部分使用了 RI 近似，在激发态计算中也会使用它。
详细文档见章节 {ref}`sec:spectroscopyproperties.tddft`

(sec:spectroscopyproperties.excitedstates.tddft.general)=
### 一般用法（General Use）

最简单的形式只需提供所求的根数：

```orca
! BP86 def2-SVP TightSCF

%tddft
  Nroots   10
  triplets true
end

*xyz 0 1
  C     0.016227   -0.000000    0.000000
  O     1.236847    0.000000   -0.000000
  H    -0.576537    0.951580   -0.000000
  H    -0.576537   -0.951580   -0.000000
end
```

得到如下输出：

```orca
------------------------------------
TD-DFT/TDA EXCITED STATES (SINGLETS)
------------------------------------

the weight of the individual excitations are printed if larger than 1.0e-02

STATE  1:  E=   0.142238 au      3.870 eV    31217.5 cm**-1 <S**2> =   0.000000 Mult 1
     7a ->   8a  :     0.999852 (c=  0.99992610)

STATE  2:  E=   0.279148 au      7.596 eV    61265.8 cm**-1 <S**2> =   0.000000 Mult 1
     7a ->   9a  :     0.991058 (c=  0.99551880)

STATE  3:  E=   0.326547 au      8.886 eV    71668.9 cm**-1 <S**2> =   0.000000 Mult 1
     5a ->   8a  :     0.992394 (c= -0.99618994)

STATE  4:  E=   0.339416 au      9.236 eV    74493.3 cm**-1 <S**2> =   0.000000 Mult 1
     6a ->   8a  :     0.214928 (c=  0.46360308)
     7a ->  10a  :     0.760130 (c= -0.87185424)

STATE  5:  E=   0.357323 au      9.723 eV    78423.4 cm**-1 <S**2> =   0.000000 Mult 1
     4a ->   8a  :     0.998607 (c=  0.99930350)

STATE  6:  E=   0.396031 au     10.777 eV    86918.7 cm**-1 <S**2> =   0.000000 Mult 1
     7a ->  11a  :     0.995757 (c= -0.99787607)

STATE  7:  E=   0.412518 au     11.225 eV    90537.2 cm**-1 <S**2> =   0.000000 Mult 1
     3a ->   8a  :     0.015703 (c=  0.12531336)
     6a ->   9a  :     0.982525 (c=  0.99122380)

STATE  8:  E=   0.420413 au     11.440 eV    92270.0 cm**-1 <S**2> =   0.000000 Mult 1
     4a ->  10a  :     0.023644 (c= -0.15376603)
     5a ->   9a  :     0.184687 (c= -0.42975192)
     5a ->  11a  :     0.029413 (c= -0.17150093)
     6a ->   8a  :     0.535798 (c= -0.73198239)
     7a ->  10a  :     0.161330 (c= -0.40165919)
     7a ->  14a  :     0.031134 (c=  0.17644805)

STATE  9:  E=   0.454354 au     12.364 eV    99719.1 cm**-1 <S**2> =   0.000000 Mult 1
     5a ->   9a  :     0.801630 (c=  0.89533782)
     5a ->  11a  :     0.012558 (c= -0.11206253)
     6a ->   8a  :     0.103311 (c= -0.32142015)
     7a ->  10a  :     0.051303 (c= -0.22650208)
     7a ->  14a  :     0.016544 (c=  0.12862428)

STATE 10:  E=   0.474384 au     12.909 eV   104115.2 cm**-1 <S**2> =   0.000000 Mult 1
     6a ->  10a  :     0.998860 (c= -0.99942977)
```

以及三重态：

```orca
------------------------------------
TD-DFT/TDA EXCITED STATES (TRIPLETS)
------------------------------------

the weight of the individual excitations are printed if larger than 1.0e-02

STATE 11:  E=   0.114291 au      3.110 eV    25084.1 cm**-1 <S**2> =   2.000000 Mult 3
     7a ->   8a  :     0.999453 (c=  0.99972624)

STATE 12:  E=   0.213324 au      5.805 eV    46819.1 cm**-1 <S**2> =   2.000000 Mult 3
     6a ->   8a  :     0.996522 (c=  0.99825941)

STATE 13:  E=   0.255583 au      6.955 eV    56094.1 cm**-1 <S**2> =   2.000000 Mult 3
     7a ->   9a  :     0.992767 (c=  0.99637714)

STATE 14:  E=   0.276345 au      7.520 eV    60650.8 cm**-1 <S**2> =   2.000000 Mult 3
     5a ->   8a  :     0.998251 (c= -0.99912505)

STATE 15:  E=   0.316749 au      8.619 eV    69518.3 cm**-1 <S**2> =   2.000000 Mult 3
     7a ->  10a  :     0.991502 (c= -0.99574190)

STATE 16:  E=   0.327793 au      8.920 eV    71942.2 cm**-1 <S**2> =   2.000000 Mult 3
     4a ->   8a  :     0.994029 (c=  0.99701018)

STATE 17:  E=   0.377551 au     10.274 eV    82862.9 cm**-1 <S**2> =   2.000000 Mult 3
     7a ->  11a  :     0.998586 (c= -0.99929259)

STATE 18:  E=   0.400159 au     10.889 eV    87824.7 cm**-1 <S**2> =   2.000000 Mult 3
     3a ->   8a  :     0.062364 (c=  0.24972706)
     6a ->   9a  :     0.934672 (c= -0.96678411)

STATE 19:  E=   0.433339 au     11.792 eV    95107.0 cm**-1 <S**2> =   2.000000 Mult 3
     5a ->   9a  :     0.988277 (c=  0.99412115)

STATE 20:  E=   0.445213 au     12.115 eV    97713.0 cm**-1 <S**2> =   2.000000 Mult 3
     3a ->   8a  :     0.934403 (c=  0.96664514)
     6a ->   9a  :     0.063400 (c=  0.25179341)
```

默认情况下，它还会打印偶极吸收谱和圆二色谱：

```orca
----------------------------------------------------------------------------------------------------
                     ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS
----------------------------------------------------------------------------------------------------
     Transition      Energy     Energy  Wavelength fosc(D2)      D2        DX        DY        DZ
                      (eV)      (cm-1)    (nm)                 (au**2)    (au)      (au)      (au)
----------------------------------------------------------------------------------------------------
  0-1A  ->  1-3A    3.110029   25084.1   398.7   0.000000000   0.00000   0.00000   0.00000   0.00000
  0-1A  ->  1-1A    3.870479   31217.5   320.3   0.000000000   0.00000  -0.00000   0.00000   0.00000
  0-1A  ->  2-3A    5.804830   46819.1   213.6   0.000000000   0.00000   0.00000   0.00000   0.00000
  0-1A  ->  3-3A    6.954778   56094.1   178.3   0.000000000   0.00000   0.00000   0.00000   0.00000
  0-1A  ->  4-3A    7.519743   60650.8   164.9   0.000000000   0.00000   0.00000   0.00000   0.00000
  0-1A  ->  2-1A    7.595990   61265.8   163.2   0.139374365   0.74893  -0.00000   0.86541  -0.00000
  0-1A  ->  5-3A    8.619170   69518.3   143.8   0.000000000   0.00000   0.00000   0.00000   0.00000
  0-1A  ->  3-1A    8.885804   71668.9   139.5   0.002010847   0.00924   0.00000  -0.00000  -0.09611
  0-1A  ->  6-3A    8.919695   71942.2   139.0   0.000000000   0.00000   0.00000   0.00000   0.00000
  0-1A  ->  4-1A    9.235990   74493.3   134.2   0.021695302   0.09588  -0.30964  -0.00000  -0.00000
  0-1A  ->  5-1A    9.723256   78423.4   127.5   0.000000000   0.00000  -0.00000   0.00000  -0.00000
  0-1A  ->  7-3A   10.273692   82862.9   120.7   0.000000000   0.00000   0.00000   0.00000   0.00000
  0-1A  ->  6-1A   10.776542   86918.7   115.1   0.009793664   0.03709   0.00000  -0.19260  -0.00000
  0-1A  ->  8-3A   10.888868   87824.7   113.9   0.000000000   0.00000   0.00000   0.00000   0.00000
  0-1A  ->  7-1A   11.225180   90537.2   110.5   0.002033718   0.00740   0.00000  -0.00000   0.08599
  0-1A  ->  8-1A   11.440020   92270.0   108.4   0.371220034   1.32448  -1.15086  -0.00000   0.00000
  0-1A  ->  9-3A   11.791761   95107.0   105.1   0.000000000   0.00000   0.00000   0.00000   0.00000
  0-1A  -> 10-3A   12.114872   97713.0   102.3   0.000000000   0.00000   0.00000   0.00000   0.00000
  0-1A  ->  9-1A   12.363588   99719.1   100.3   0.259360077   0.85625  -0.92534   0.00000   0.00000
  0-1A  -> 10-1A   12.908634  104115.2    96.0   0.000000000   0.00000  -0.00000  -0.00000  -0.00000
```

```orca
------------------------------------------------------------------------------------------
                     CD SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS
------------------------------------------------------------------------------------------
     Transition      Energy     Energy  Wavelength    R        MX        MY        MZ
                      (eV)      (cm-1)    (nm)   (1e40*cgs)   (au)      (au)      (au)
------------------------------------------------------------------------------------------
  0-1A  ->  1-3A    3.110029   25084.1   398.7   -0.00000   0.00000   0.00000   0.00000
  0-1A  ->  1-1A    3.870479   31217.5   320.3    0.00000   0.58235   0.00000   0.00000
  0-1A  ->  2-3A    5.804830   46819.1   213.6   -0.00000   0.00000   0.00000   0.00000
  0-1A  ->  3-3A    6.954778   56094.1   178.3   -0.00000   0.00000   0.00000   0.00000
  0-1A  ->  4-3A    7.519743   60650.8   164.9   -0.00000   0.00000   0.00000   0.00000
  0-1A  ->  2-1A    7.595990   61265.8   163.2   -0.00000  -0.00000   0.00000   0.32961
  0-1A  ->  5-3A    8.619170   69518.3   143.8   -0.00000   0.00000   0.00000   0.00000
  0-1A  ->  3-1A    8.885804   71668.9   139.5   -0.00000  -0.00000  -0.73058   0.00000
  0-1A  ->  6-3A    8.919695   71942.2   139.0   -0.00000   0.00000   0.00000   0.00000
  0-1A  ->  4-1A    9.235990   74493.3   134.2   -0.00000  -0.00000  -0.00000  -0.00000
  0-1A  ->  5-1A    9.723256   78423.4   127.5    0.00000   0.31342  -0.00000   0.00000
  0-1A  ->  7-3A   10.273692   82862.9   120.7   -0.00000   0.00000   0.00000   0.00000
  0-1A  ->  6-1A   10.776542   86918.7   115.1    0.00000   0.00000   0.00000   0.58743
  0-1A  ->  8-3A   10.888868   87824.7   113.9   -0.00000   0.00000   0.00000   0.00000
  0-1A  ->  7-1A   11.225180   90537.2   110.5   -0.00000   0.00000  -0.06966   0.00000
  0-1A  ->  8-1A   11.440020   92270.0   108.4   -0.00000  -0.00000  -0.00000   0.00000
  0-1A  ->  9-3A   11.791761   95107.0   105.1   -0.00000   0.00000   0.00000   0.00000
  0-1A  -> 10-3A   12.114872   97713.0   102.3   -0.00000   0.00000   0.00000   0.00000
  0-1A  ->  9-1A   12.363588   99719.1   100.3   -0.00000  -0.00000  -0.00000  -0.00000
  0-1A  -> 10-1A   12.908634  104115.2    96.0    0.00000   0.00260   0.00000   0.00000
```

(sec:spectroscopyproperties.excitedstates.tddft.ccapabilities)=
### 功能（Capabilities）

目前，TD-DFT/CIS 模块能够计算激发能、吸收谱和圆二色谱。
在 TD-DFT 方法内，还可以计算磁圆二色（见 {ref}`sec:spectroscopyproperties.mcd`）
和瞬态光谱。

TD-DFT 在限制性和非限制性形式以及共线自旋翻转变体中
都有解析梯度，从而可以进行激发态的几何优化，
如 {ref}`sec:spectroscopyproperties.tddft.geometry` 中所述。


```{index} ROCIS
```

(sec:spectroscopyproperties.excitedstates.rocis)=
## 用限制性开壳层 CIS - ROCIS 计算激发态（Excited States with Restricted Open-shell CIS - ROCIS）

除了 CIS/TD-DFT 对激发态的描述外，ORCA
还提供 ROCIS 方法{cite}`roemelt2013`、{cite}`roemelt2013b`，它使用
限制性开壳层 Hartree-Fock（ROHF）参考进行单激发
组态相互作用计算。

从 ORCA 6.0 开始，提供了一般自旋 ROCIS（`GS-ROCIS`）{cite}`gouveia2025JPCA` 实现。
这一新实现可以处理通过 `CSF-ROHF` 方法获得的、具有任意自旋耦合的
CSF 作为参考。

ROCIS 的主要用途是计算 L 边和 M 边 X 射线吸收谱（XAS）以及 X 射线
磁圆二色（XMCD）和共振非弹性 X 射线散射（RIXS）。计算成本
通常高于 TD-DFT，但显著低于基于耦合簇的方法。
结合对自然轨道方法（`PNO-ROCIS`），中等到大分子尺寸的光谱
也是可行的。

详细文档见 {ref}`sec:spectroscopyproperties.rocis`。

(sec:spectrochemistryproperties.excitedstates.rocis.general)=
### 一般用法（General Use）

通过在输入文件的 `%rocis` 块中提供所求根数来调用该方法：

<!-- >```{literalinclude} ../../orca_working_input/C05S05_160.inp
:language: orca
``` -->

```orca
!def2-SVP TightSCF

%scf
 HFTyp ROHF
 ROHF_CASE HIGHSPIN
 ROHF_NEL[1] 2
end

%rocis
 NRoots 10
end

* xyz 0 3 
 C 0  0       0.1058
 H 0  0.9910 -0.3174
 H 0 -0.9910 -0.3174
end
```

(sec:spectroscopyproperties.excitedstates.rocis.capabilities)=
### 功能（Capabilities）

ROCIS 模块可以计算激发能、振子强度、跃迁偶极矩以及
X 射线吸收谱。它还支持计算 X 射线磁圆二色（XMCD）谱
和共振非弹性 X 射线散射（RIXS）截面。
ROCIS 方法适用于开壳层体系，特别适合过渡金属配合物的
L 边和 M 边光谱。

(sec:spectroscopyproperties.excitedstates.mcrpa)=
## 用 CASSCF 线性响应（MC-RPA）计算开壳层分子的激发态（Excited States for Open-Shell Molecules with CASSCF Linear Response (MC-RPA)）

MCRPA 是 CASSCF 线性响应理论的同义表述，主要用于
开壳层和强相关体系。在完成基态 CASSCF 计算后，
可以计算激发能、振子强度和旋光强度。
详细文档见 {ref}`sec:spectroscopyproperties.mcrpa`。

(sec:spectroscopyproperties.excitedstates.mcrpa.general)=
### 一般用法（General Use）

在收敛的 CASSCF 计算之后，通过在 `%mcrpa` 块中指定根数
来启动 MCRPA 计算：

```orca
#casscf + mcrpa input example
```

(sec:spectroscopyproperties.excitedstates.mcrpa.ccapabilities)=
### 功能（Capabilities）

MCRPA 可以计算激发能、振子强度和旋光强度。
它特别适合开壳层和强相关体系。还可以使用 CVS 近似
计算 X 射线吸收谱（XAS）。

(sec:spectroscopyproperties.excitedstates.ADC2)=
## 用 ADC2 计算激发态（Excited States with ADC2）

ADC2（代数图解构造二阶）方法是 CC2 的一种近似，
提供了一种比 EOM-CCSD 更经济的计算激发能的途径。
ADC2 方法在 ORCA 中实现，用于计算激发能和跃迁矩。

(sec:spectroscopyproperties.excitedstates.ADC2.general)=
### 一般用法（General Use）

通过在简单输入中使用 `!ADC2` 关键词并指定基组
来调用 ADC2 计算。需要在 `%mdci` 块中指定根数：

```orca
!ADC2 def2-TZVP TightSCF

%mdci
NRoots 10
end
```

(sec:spectroscopyproperties.excitedstates.ADC2.capabilities)=
### 功能（Capabilities）

ADC2 模块可以计算激发能和跃迁矩。它提供比 EOM-CCSD
更经济的计算，但精度略低。ADC2 的计算标度为 O($N^{5}$)。

(sec:spectroscopyproperties.excitedstates.steom)=
## 用 STEOM-CCSD 计算激发态（Excited States with STEOM-CCSD）

STEOM-CCSD 方法是对 EOM-CCSD 的改进，通过第二次相似变换
将最终的矩阵对角化步骤压缩到 CIS 空间。
详细文档见 {ref}`sec:spectroscopyproperties.steom`。

(sec:spectroscopyproperties.excitedstates.steom.general)=
### 一般用法（General Use）

STEOM-CCSD 通过在简单输入中使用 `!STEOM-CCSD` 关键词来调用。
主要步骤包括基态 CCSD 计算、IP-EOM 和 EA-EOM 计算，
以及最终的 CIS 空间对角化。

(sec:spectroscopyproperties.excitedstates.steom.capabilities)=
### 功能（Capabilities）

STEOM-CCSD 可以计算激发能和跃迁矩。它提供比 EOM-CCSD
更高效的计算，适用于中等到大分子。还可以计算
芯激发能（见 {ref}`sec:spectroscopyproperties.eomcore.core-excitation`）。

(sec:spectroscopyproperties.excitedstates.ihfsmr)=
## 用 IH-FSMR-CCSD 计算激发态（Excited States with IH-FSMR-CCSD）

IH-FSMR-CCSD 是另一种解耦单激发空间与更高激发空间的方法。
详细文档见 {ref}`sec:spectroscopyproperties.ihfsmr`。

(sec:spectroscopyproperties.excitedstates.ihfsmr.general)=
### 一般用法（General Use）

IH-FSMR-CCSD 计算涉及基态 CCSD、IP-EOM、EA-EOM 和
最终的 CIS 空间对角化步骤。

(sec:spectroscopyproperties.excitedstates.ihfsmr.capabilities)=
### 功能（Capabilities）

IH-FSMR-CCSD 可以计算激发能和跃迁矩。它特别适合
需要考虑多重参考效应的体系。

(sec:spectroscopyproperties.excitedstates.dleom)=
## 用基于 PNO 的耦合簇方法计算激发态（Excited States with PNO based coupled cluster methods）

基于 PNO 的方法（bt-PNO）通过将基态 DLPNO 量反变换回
正则基，在保持精度的同时大幅降低计算成本。
详细文档见 {ref}`sec:spectroscopyproperties.dleom`。

(sec:spectroscopyproperties.excitedstates.dleom.general)=
### 一般用法（General Use）

bt-PNO 方法通过在简单输入中使用 `!bt-PNO-EOM-CCSD` 关键词来调用。
它适用于闭壳层和开壳层体系。

(sec:spectroscopyproperties.excitedstates.dleom.capabilities)=
### 功能（Capabilities）

bt-PNO 方法可以计算激发能、电离势和电子亲和能。
它提供与正则 EOM-CCSD 相当的精度，但计算成本显著降低。

(sec:spectrochemistryproperties.excitedstates.dlpnoeom)=
## 用基于 DLPNO 的耦合簇方法计算激发态（Excited States with DLPNO based coupled cluster methods）

DLPNO 方法是 PNO 方法的进一步加速版本，适用于
更大的分子体系。详细文档见
{ref}`sec:spectroscopyproperties.excitedstates.dlpnoeom`。

(sec:spectroscopyproperties.excitedstates.dlpnoeom.general)=
### 一般用法（General Use）

DLPNO-EOM 方法通过在简单输入中使用 `!IP-EOM-DLPNO-CCSD`
或类似关键词来调用。它适用于大分子体系。

(sec:spectroscopyproperties.excitedstates.dlpnoeom.capabilities)=
### 功能（Capabilities）

DLPNO 方法可以计算激发能，适用于大分子体系。
它的精度略低于正则方法，但计算成本大幅降低。
