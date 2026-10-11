```{index} ROCIS
```

(sec:spectroscopyproperties.rocis)=
# 通过 ROCIS 和 ROCIS/DFT 计算激发态（Excited States via ROCIS and ROCIS/DFT）

ORCA 程序包可以使用限制性开壳层 Hartree-Fock（ROHF）参考函数
进行单激发组态相互作用（CIS）计算。
它产生激发能、吸收能和 CD 强度。
它的设计目标是重现——更重要的是——
可靠地预测 X 射线吸收光谱（XAS）中观测到的
过渡金属 L 边。

原始 ROCIS 实现{cite}`roemelt2013`、{cite}`roemelt2013b` 只能在
高自旋 ROHF 参考函数之上进行 CIS 计算。从 ORCA 6.0 开始，
新的通用自旋 ROCIS（GS-ROCIS）实现{cite}`gouveia2025JPCA`、{cite}`gouveia2025SOC`
也可应用户要求使用。
这一新实现可以在通过 CSF-ROHF 方法获得的任何自旋耦合情形之上
进行 CIS 计算。这包括原始实现所涵盖的高自旋情形。

(sec:spectroscopyproperties.rocis.general)=
## 一般性描述（General Description）

(sec:spectroscopyproperties.rocis.general.gsrocis)=
### 通用自旋 ROCIS（General Spin ROCIS）

GS-ROCIS 方法描述如下：

从在谱系耦合方案中构造的参考 CSF（通过 `CSF-ROHF` 计算获得）出发，
根据激发所涉及轨道的占据数定义四类激发 CSF。

这些激发类别是：
-  DOMO 到 SOMO 激发 - $\left| \Phi_i^t \right\rangle$
-  SOMO 到 VMO 激发 - $\left| \Phi_t^a \right\rangle$
-  DOMO 到 VMO 激发 - $\left| \Phi_i^a \right\rangle$
-  DOMO 到 VMO 激发与 SOMO 到 SOMO 激发的耦合 - $\left| \Phi_{ui}^{at} \right\rangle$

这样，GS-ROCIS 波函数定义为：

$$\begin{array}{l}
  \Psi_{GS-ROCIS} = c_0 \left| \Phi_0 \right\rangle + \sum_{i,t}{c_i^t\left| \Phi_i^t \right\rangle} + \sum_{t,a}{c_t^a\left| \Phi_t^a \right\rangle}
  + \sum_{i,a}{c_i^a\left| \Phi_i^a \right\rangle} + \sum_{i,t,a,u\neq t}{c_{ui}^{at}\left| \Phi_{ui}^{at} \right\rangle}
 \end{array}
$$

其中展开系数 $c_p^q$ 在 CI 过程中确定。

`GS-ROCIS` 可以通过以下方式请求：

```orca
%rocis
  DoGenROCIS true  # Turns the general-spin ROCIS procedure on 
  ReferenceMult 1  # The reference wavefunction multiplicity
                   # (it needs to agree with the ROHF solution)
end
```



`%rocis` 块中的若干基本变量控制用于求解 CI 问题的
Davidson 过程的设置：

```orca
%rocis
  NRoots    6     # Number of desired roots.
  MaxDim    5     # Davidson expansion space = MaxDim * NRoots.
  ETol      1e-6  # Energy convergence tolerance.
  RTol      1e-6  # Residual vector convergence tolerance.
  MaxIter   35    # Maxmimum number of iterations.
  NGuessMat 512   # Dimension of the guess matrix: 512x512.
end
```
计算过程中产生的输出量通过 `PrintLevel` 变量控制：

```orca
%rocis
  PrintLevel 3
end
```

请注意，这并不影响计算或打印哪些光谱。

`orca_rocis` 模块提供两种选择轨道激发空间的方式：
按轨道能或按轨道编号。在前一种情况下，需要指定一个能量窗口，
程序将考虑轨道能落在该窗口内的所有轨道。
请注意，实际上需要定义两个轨道窗口：一个用于供体轨道，
另一个用于受体轨道。窗口的输入以数组形式给出：
前两个数字定义供体空间，后两个数字定义受体空间。

```orca
%rocis
  NRoots 3
  EWin = -5,5,-5,5
end
```

默认情况下，芯轨道和很高能量的虚拟轨道被排除在各自的
轨道激发空间之外。由于这些轨道张成的空间通常是常规
UV/Vis 光谱无法到达的，这是一个合理的近似。
需要记住的是，只有当计算中使用的轨道具有明确定义的
轨道能时，轨道能窗口才有意义。因此，对于使用局域轨道的
计算不能使用轨道能窗口。指定激发空间的第二种方式是
按轨道编号。

```orca
%rocis
  NRoots 3
  OrbWin = 1,13,9,22
end
```

在限制性计算中，只创建一组空间轨道。
因此不需要分别为 $\alpha$ 和 $\beta$ 电子提供轨道窗口。
当然，只有双重或单重占据的轨道可以作为供体轨道，
只有单重和未占据的轨道可以作为受体轨道。
程序会识别供体空间中的未占据轨道和受体空间中的
双重占据轨道，并将两者都移除。

基于纯偶极近似计算的吸收谱总是被打印出来。

此外，与 TD-DFT（章节
{ref}`sec:spectroscopyproperties.tddft`）或 CASSCF 中一样，
可以通过计算二阶振子强度或完全半经典振子强度来获得强度。

-   精确振子强度的行为类似于速度表示中的多极展开。

-   根据定义它们与原点无关，不会像一阶以上的多极矩那样
    遭受人为负值的问题。

-   它们与最高到二阶的多极矩一起使用，以在长度表示或
    速度表示中重新生成电偶极、电四极和磁偶极贡献。

```orca
%rocis
  DoDipoleLength        true
  DoDipoleVelocity      true
  DecomposeFosc         true
  DoFullSemiclassical   true
  DoCD                  true
end
```

更多细节见章节 {ref}`sec:spectroscopyproperties.ops`。

用户可以控制将哪些轨道激发包含在 ROCIS 问题中：

```orca
%rocis
  Do_is true     # Include DOMO->SOMO excitations
  Do_sa true     # Include SOMO->Virtual excitations
  Do_ia true     # Include DOMO->Virtual excitations
  Do_ista true   # Include DOMO->SOMO coupled to
                 # SOMO->Virtual excitations with s not equal t

  # For GS-ROCIS, the following excitation is included in the DOMO->VMO class
  # Only on the original ROCIS implementation it is a separate class.
  Do_isa true    # Include DOMO->SOMO coupled to
                 # SOMO->Virtual excitations with s = t
end
```

默认情况下，包含所有激发。

当程序完成 ROCIS 计算时，它给出每个根的激发能、
组成以及相应的自旋耦合情形。
根据相应函数 $\left| \Phi \right\rangle$ 的标号数目，
属于不同激发类别的激发组态态函数的贡献
由两个、三个或四个数字给出。

```orca
STATE  16   Exc. Energy: 27294.664mEh  742.726eV     5990486.3cm**-1
       8->50                 :   0.0145   (-0.120499) : spin coupling: +1-1+1+1+1+1
       8->51                 :   0.0317   (0.178098)  : spin coupling: +1+1+1+1+1-1
       8->51                 :   0.2212   (-0.470333) : spin coupling: +1+1-1+1+1+1
       8->51                 :   0.4135   (-0.643076) : spin coupling: +1-1+1+1+1+1
       6->46   ;   48->51    :   0.0843   (-0.290338) : spin coupling: +1 2+1 0+1+1
       6->47   ;   49->51    :   0.1252   (-0.353805) : spin coupling: +1+1 2+1 0+1 
       7->46   ;   49->51    :   0.0452   (-0.212665) : spin coupling: +1 2+1+1 0+1 
       7->47   ;   48->51    :   0.0133   (0.115519)  : spin coupling: +1+1 2 0+1+1
       7->49   ;   46->51    :   0.0109   (0.104242)  : spin coupling: +1 0+1+1 2+1 
```

此外，ROCIS 能够计算自旋-轨道耦合（SOC）对计算的
基态和激发态的影响。它在准简并微扰理论（QDPT）框架中
引入 SOC。SOC 哈密顿量在计算的 ROCIS 态
$\left| \Psi_I^{SM} \right\rangle$ 的基下对角化，其中 $I$ 是
根标号，$S$ 和 $M$ 分别是自旋和磁自旋量子数{cite}`neese1998inorgchem`、{cite}`roemelt2013`。

```orca
%rocis
  rel
    DoSOC true        # invokes the calculation of SOC effects
    TEMPERATURE 10    # temperature for SOC corrected spectra in Kelvin
  end
end
```

SOC 计算之后，程序将为 SOC 修正结果产生额外的光谱。
光谱包含从 $2S+1$ 个最低态到所有激发态的跃迁，
其中 S 是电子基态的自旋量子数。这 $2S+1$ 个最低态
可能分裂 1-100 cm$^{-1}$ 的量级。由于分裂幅度很小，
即使在低温下所有 $2S+1$ 个态也可以显著布居。
在实验上，给定跃迁的强度依赖于相应初态的布居。
通过 `TEMPERATURE` 关键词，可以通过改变体系的虚拟温度
来调控理论计算态的布居。需要指出的是，自旋-轨道耦合态之间的
电四极跃迁没有良好定义，很可能给出不合理的结果。
因此建议仅在不包含 SOC 的计算中使用 `Decomposefosc` 关键词。

```orca
--------------------------------------------------------------------------------------------------------
      SOC CORRECTED ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS
--------------------------------------------------------------------------------------------------------
      Transition         Energy     Energy  Wavelength fosc(D2)      D2       |DX|      |DY|      |DZ|
                          (eV)      (cm-1)    (nm)  (*population)  (au**2)    (au)      (au)      (au)
--------------------------------------------------------------------------------------------------------
  0-5.0A  ->  1-5.0A    0.000000       0.0     0.0   0.000000000   0.00000   0.00000   0.00000   0.00000
  2-5.0A  ->  3-5.0A    0.000000       0.0  2927278012.6   0.000000000   0.00000   0.00000   0.00000   0.00000
  3-5.0A  ->  4-5.0A    0.000001       0.0  2013441147.3   0.000000000   0.00000   0.00000   0.00000   0.00000
  2-5.0A  ->  4-5.0A    0.000001       0.0  1192923906.3   0.000000000   0.00000   0.00000   0.00000   0.00000
  1-5.0A  ->  2-5.0A    0.000002       0.0  559585326.1   0.000000000   0.00000   0.00000   0.00000   0.00000
  0-5.0A  ->  2-5.0A    0.000002       0.0  554991701.4   0.000000000   0.00000   0.00000   0.00000   0.00000
  1-5.0A  ->  3-5.0A    0.000003       0.0  469780906.9   0.000000000   0.00000   0.00000   0.00000   0.00000
  0-5.0A  ->  3-5.0A    0.000003       0.0  466539107.5   0.000000000   0.00000   0.00000   0.00000   0.00000
  1-5.0A  ->  4-5.0A    0.000003       0.0  380906816.8   0.000000000   0.00000   0.00000   0.00000   0.00000
  0-5.0A  ->  4-5.0A    0.000003       0.0  378772788.3   0.000000000   0.00000   0.00000   0.00000   0.00000
  4-5.0A  ->  5-5.0A   715.072294 5767447.6     1.7   0.000853852   0.00024   0.00000   0.01494   0.00454
  3-5.0A  ->  5-5.0A   715.072294 5767447.6     1.7   0.000001143   0.00000   0.00021   0.00018   0.00050
  2-5.0A  ->  5-5.0A   715.072295 5767447.6     1.7   0.000001245   0.00000   0.00024   0.00053   0.00012
  1-5.0A  ->  5-5.0A   715.072297 5767447.6     1.7   0.000000330   0.00000   0.00000   0.00029   0.00010
  0-5.0A  ->  5-5.0A   715.072297 5767447.6     1.7   0.000024144   0.00001   0.00000   0.00251   0.00076
  4-5.0A  ->  6-5.0A   715.089740 5767588.3     1.7   0.000002661   0.00000   0.00067   0.00036   0.00042
  3-5.0A  ->  6-5.0A   715.089741 5767588.3     1.7   0.000008083   0.00000   0.00000   0.00145   0.00045
  2-5.0A  ->  6-5.0A   715.089742 5767588.3     1.7   0.000775076   0.00022   0.00001   0.01423   0.00432
  1-5.0A  ->  6-5.0A   715.089744 5767588.4     1.7   0.000000497   0.00000   0.00002   0.00015   0.00035
  0-5.0A  ->  6-5.0A   715.089744 5767588.4     1.7   0.000001537   0.00000   0.00056   0.00035   0.00007
  4-5.0A  ->  7-5.0A   715.115140 5767793.2     1.7   0.000001500   0.00000   0.00027   0.00020   0.00056
  3-5.0A  ->  7-5.0A   715.115141 5767793.2     1.7   0.000834113   0.00024   0.00001   0.01476   0.00449
  2-5.0A  ->  7-5.0A   715.115141 5767793.2     1.7   0.000008694   0.00000   0.00002   0.00150   0.00050
  1-5.0A  ->  7-5.0A   715.115143 5767793.2     1.7   0.000000562   0.00000   0.00026   0.00025   0.00018
  0-5.0A  ->  7-5.0A   715.115143 5767793.2     1.7   0.000003341   0.00000   0.00036   0.00031   0.00085
  4-5.0A  ->  8-5.0A   715.184940 5768356.2     1.7   0.000000146   0.00000   0.00004   0.00020   0.00001
  3-5.0A  ->  8-5.0A   715.184940 5768356.2     1.7   0.000019943   0.00001   0.00206   0.00012   0.00120
...
```

如果 `PrintLevel` 值设为 3 或更高，程序将在
$\left| \Psi_I^{SM} \right\rangle$ 态的基下打印
SOC 修正态的组成。

```orca
Eigenvectors of SOC calculation:
the threshold for printing is: 0.010000
          weight         real           image    :   Root   Block   Spin    Ms
State 0:           0.00 cm**-1         0.00000 eV
        0.135363      -0.028407       0.366819   :      0     0     2      2
        0.181749       0.224125       0.362653   :      0     0     2      1
        0.367330      -0.135925      -0.590639   :      0     0     2      0
        0.180828       0.039792      -0.423372   :      0     0     2     -1
        0.134728       0.185875       0.316510   :      0     0     2     -2
...
```

SOC 计算的更多细节（如 SOC 积分计算过程）可以通过
`%rel` 块控制（章节 {ref}`sec:essentialelements.relativistic`）。


(sec:spectroscopyproperties.rocis.general.hsrocis)=
### 原始 ROCIS 实现（Original ROCIS Implementation）

仍然可以使用 ROCIS 的原始实现{cite}`roemelt2013`、{cite}`roemelt2013b`，
它只能在高自旋 ROHF 参考函数之上进行 CIS 计算。
所有未配对电子的自旋必须铁磁耦合，
给出总自旋 $S = \frac{1}{2}N$，其中 $N$ 是未配对电子数。

原始 ROCIS 实现的使用可以通过以下方式请求：

```orca
%rocis
  DoGenROCIS false
end
```

根据我们的经验，ROHF 计算深受收敛问题困扰。
UHF 计算通常表现出更好的收敛性质。
在大多数情况下，UHF 计算的准限制性轨道（qro）类似于
ROHF 轨道。因此，原始 ROCIS 具有在 UHF 计算之上
开始计算的能力。它将自动创建 qro 并构造参考行列式
（见下文）。

(sec:spectroscopyproperties.rocis.general.dftrocis)=
### ROCIS/DFT

ROCIS/DFT 方法是 ROCIS 的一种变体，其中使用 DFT 计算的
轨道代替 ROHF 轨道。这可以改善对电子相关的描述。
ROCIS/DFT 可以通过在 `%rocis` 块中设置相应选项来启用。

(sec:spectroscopyproperties.rocis.general.ri)=
### 分辨率恒等式（Resolution of the Identity）

ROCIS 模块支持 RI 近似来加速积分计算。
这可以显著降低计算成本，特别是对于大分子。

(sec:spectrochemistryproperties.rocis.PNO)=
## 芯 PNO-ROCIS、PNO-ROCIS/DFT（Core PNO-ROCIS, PNO-ROCIS/DFT）

PNO-ROCIS 方法使用对自然轨道（PNO）近似来加速
ROCIS 计算，使得中等到大分子的计算成为可能。
PNO-ROCIS 适用于芯能级光谱计算。

(sec:spectroscopyproperties.rocis.transMetal)=
## 用 ROCIS 或 DFT/ROCIS 计算过渡金属 L 边（Transition Metal L-Edges with ROCIS or DFT/ROCIS）

ROCIS 方法特别适合计算过渡金属配合物的 L 边
X 射线吸收谱。它能够描述芯能级激发，
并提供与实验吻合良好的结果。

(sec:spectroscopyproperties.rocis.rixs)=
## 共振非弹性散射光谱（Resonant Inelastic Scattering Spectroscopy）

(sec:spectroscopyproperties.rocis.rixs.general)=
### 概述（General）

ROCIS 模块可以计算共振非弹性 X 射线散射（RIXS）截面。
这包括对入射和散射光子能量的双重依赖。

(sec:spectroscopyproperties.rocis.rixs.mapspc)=
### 用 `orca_mapspc` 处理光谱（Processing the spectra with `orca_mapspc`）

RIXS 光谱可以用 `orca_mapspc` 工具进行处理和可视化。

(sec:spectroscopyproperties.rocis.rixs.cut)=
### 生成切片（Generating Cuts）

可以从 RIXS 面生成各种切片，以与实验数据比较。

(sec:spectroscopyproperties.rocis.magProp)=
## ROCIS 磁性质（ROCIS Magnetic Properties）

ROCIS 方法还可以计算磁性质，如 g 张量和 A 张量。

(sec:spectroscopyproperties.rocis.natTransOrb)=
## 自然跃迁轨道/自然差分轨道（Natural Transition Orbitals/ Natural Difference Orbitals）

ROCIS 模块支持自然跃迁轨道（NTO）和自然差分轨道（NDO）
分析，以可视化电子跃迁。

(sec:spectroscopyproperties.rocis.keywords)=
## 关键词列表（Keyword List）

`%rocis` 块中可用的完整关键词列表如下所示。
详细说明见各关键词的注释。
