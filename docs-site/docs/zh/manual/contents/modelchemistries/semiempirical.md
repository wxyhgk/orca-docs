

<a id="sec:modelchemistries.semiempirical"></a>
# 半经验方法（Semiempirical Methods）

半经验量子力学方法（Semi-empirical quantum mechanical methods, SQM）对于处理许多非常大的体系非常有用。它们采用定制的近似（tailored approximations）来大幅降低计算成本，同时在化学空间（chemical space）的很大部分上保持合理的精度水平。它们对于用 [NEB-TS](../structurereactivity/neb.md#sec:structurereactivity.neb.nebts) 模拟反应路径（reaction paths），或在 [ONIOM 等多尺度方法](mm.md#sec:modelchemistries.mm.orca)中定义 SQM 区域特别有用。

<a id="sec:modelchemistries.semiempirical.ndo"></a>
## 微分重叠忽略（Neglect of Differential Overlap）：CNDO、INDO、NDDO

目前已实现若干基于"微分重叠忽略"（neglect of differential overlap）[pople1970approx,sedlej1985semi](../../bibliography.md) 的方法，可用于能量和解析梯度计算，包括 AM1[dewar1985am](../../bibliography.md)、PM3[stewart1989comp](../../bibliography.md)、MNDO[dewar1977theor,thiel1992theor,dewar1977am](../../bibliography.md) 以及 CNDO、INDO 和 NDDO 的其他变体。MNDO、AM1 和 PM3 方法仅适用于主族元素（main group elements），源自 Dewar 课题组的工作。它们经过优化以重现分子结构和能量学性质。较早的 CNDO/1,2 和 INDO/1,2 由 Pople 课题组开发[pople1965chem,pople1966chem,santry1968am,santry1967chem,pople1967chem,clack1972chem,clack1974mol,clack1974theor,boehm1981theor](../../bibliography.md)，其设计目标是大致模拟最小基组*从头算*（*ab initio*）计算。Zerner 课题组的方法（ZINDO/1,2 和 ZINDO/S）与这些较早的方法密切相关，但针对过渡金属也进行了良好的参数化[ridley1973theor,bacon1979theor,zerner1980am,anderson1986inorg,anderson1990inorg,anderson1991int,zerner1990reviews,zerner1992metal,zerner1996metal,cory1991chem,kotzian1992theor](../../bibliography.md)。
ZINDO/1（以及较少程度上的 ZINDO/2）适合几何优化。ZINDO/S 在中等组态相互作用（configuration interaction）水平上对电子激发态（electronically excited states）给出良好的结果，在计算大型过渡金属配合物中的电子和自旋分布方面也很成功[anderson1991int,zerner1990reviews,zerner1992metal,zerner1996metal,cory1991chem,kotzian1992theor](../../bibliography.md)。
ZNDDO/1,2 方法已作为对应 INDO 方法的直接扩展实现到 ORCA 中，未改变任何参数。不过，这些方法受益于 NDDO 近似中对库仑相互作用略为更精确的表述[nieke1984theor,koehler1972zchem](../../bibliography.md)。对这些方法的初步经验是，它们在过渡金属配合物结构计算方面优于相应的 INDO 方法，但总体上也有类似的缺陷。所有这些方法都提供解析梯度，可用于以较低的计算成本产生合理的分子结构，或对所研究体系的行为获得初步认识。但请勿尝试用 ZINDO/S（或 CNDO/S）做结构优化——这样做没有意义，而且会导致灾难性的结果，因为这些方法中没有对核排斥（nuclear repulsion）的精确表述。

!!! tip "提示"
    尽管 ORCA 没有实现较新的 MNDO 方法（如 PM6 或 RM1），但可以通过 ORCA 的[外部优化器功能（External Optimizer feature）](../structurereactivity/optimizations.md#sec:structurereactivity.optimization.externaloptimizer)配合 [MOPAC](https://github.com/openmopac/mopac) 来使用它们。这样，[MOPAC](https://github.com/openmopac/mopac) 可以通过相应的封装脚本（wrapper script）与 ORCA 对接，为 ORCA 提供能量和梯度；该脚本可从 [ORCA 外部工具 GitHub 仓库](https://github.com/ORCAQuantumChemistry/orca-external-tools)下载。

<a id="sec:modelchemistries.semiempirical.ndo.basicusage"></a>
### 基本用法（Basic Usage）

基于 NDDO 的 MNDO、AM1 和 PM3 方法可通过简单输入关键词 `!MNDO`、`!AM1` 和 `!PM3` 调用。

```orca
!MNDO
```
```orca
!AM1
```
```orca
!PM3
```

这些及其他方法可通过 `%method` 块进一步定义，例如使用 INDO/1 参数集的 INDO：

```orca
%method
   METHOD   INDO
   VERSION  INDO_1
end
```

或通过直接将相应参数化指定为 `METHOD`：

```orca
%method
   METHOD   INDO_1
end
```

!!! note "注意"
    如果需要，也可以将半经验方法与 MP2 结合使用（仅限能量）。例如使用 `Method AM1` 和 `DoMP2 true`。这是否能使半经验计算的结果变得更好尚存疑问，但至少在 ORCA 中是可行的。

<a id="sec:modelchemistries.semiempirical.ndo.customparams"></a>
### 自定义参数（Custom Parameters）

您可以通过 `%ndoparas` 块以直接的方式更改内置的半经验参数。为此，任何元素专属的参数都可以通过数组 "P" 来定义：

```orca
%ndoparas  
   P[<atomic number>,<parameter number>] <real>
end
```

例如，我们可以将碳（Z = 6）的共振积分参数（resonance integral parameter）BS（s 壳层 beta，编号 25）设置为 20 eV：

```orca
%ndoparas  
   P[6,25] 20
end
```

可修改参数的完整列表见下文。其中大多数只对专家用户有意义。最常修改的参数是 Beta（编号 25 至 28）。注意，大多数程序在此处要求负数。在 ORCA 中，共振积分的定义方式使 Beta 为正值。

<a id="tab:modelchemistries.semiempirical.ndo.paras"></a>
!!! note "可在 `%ndoparas` 块中设置的参数列表（List of parameters that can be set in the `%ndoparas` block）。"


| ****参数（Parameter）**** | 编号（Number） | 描述（Description） |
| --- | --- | --- |
| ** *芯积分（Core Integrals，单位为 eV）：*** |  |  |

| **`US`** | 无 |

         - `0`
         - 


| | **`1`** |  |
| --- | --- | --- |
| **`UP`** | `1` |  |
| **`UD`** | `2` |  |
| **`UF`** | `3` |  |
| ** *基组参数（Basis Set Parameters，双 zeta）：*** |  |  |

| **`NSH`** | 无 |

         - `4`
         - 该元素的壳层数


| | **`5`** | s 壳层的斯莱特型轨道（Slater type orbitals）数目 |
| --- | --- | --- |
| **`NZS`** | `5` | s 壳层的斯莱特型轨道（Slater type orbitals）数目 |
| **`ZS1`** | `6` | 第一个指数 |
| **`ZS2`** | `7` | 第二个指数 |
| **`CS1`** | `8` | 第一个收缩系数 |
| **`CS2`** | `9` | 第二个收缩系数 |
| **`NZP`** | `10` | p 壳层的斯莱特型轨道数目 |
| **`ZP1`** | `11` |  |
| **`ZP2`** | `12` |  |
| **`CP1`** | `13` |  |
| **`CP2`** | `14` |  |
| **`NZD`** | `15` | d 壳层的斯莱特型轨道数目 |
| **`ZD1`** | `16` |  |
| **`ZD2`** | `17` |  |
| **`CD1`** | `18` |  |
| **`CD2`** | `19` |  |
| **`NZF`** | `20` | f 壳层的斯莱特型轨道数目 |
| **`ZF1`** | `21` |  |
| **`ZF2`** | `22` |  |
| **`CF1`** | `23` |  |
| **`CF2`** | `24` |  |
| ** *共振积分参数（Resonance integral parameters，单位为 eV）：*** |  |  |

| **`BS`** | 无 |

         - `25`
         - s 壳层 beta


| | **`26`** | p 壳层 beta |
| --- | --- | --- |
| **`BP`** | `26` | p 壳层 beta |
| **`BD`** | `27` | d 壳层 beta |
| **`BF`** | `28` | f 壳层 beta |
| ** *基态电子数（Number of electrons in the ground state）：*** |  |  |

| **`NEL`** | 无 |

         - `29`
         - 电子总数（整数）


| | **`30`** | s 壳层的分数占据数（fractional occupation number） |
| --- | --- | --- |
| **`NS`** | `30` | s 壳层的分数占据数（fractional occupation number） |
| **`NP`** | `31` | p 壳层的分数占据数 |
| **`ND`** | `32` | d 壳层的分数占据数 |
| **`NF`** | `33` | f 壳层的分数占据数 |
| ** *单中心排斥（gamma）积分（One center repulsion (gamma) integrals，单位为 eV）：*** |  |  |

| **`GSS`** | 无 |

         - `34`
         - 


| | **`35`** |  |
| --- | --- | --- |
| **`GSP`** | `35` |  |
| **`GSD`** | `36` |  |
| **`GSF`** | `37` |  |
| **`GPP`** | `38` |  |
| **`GPD`** | `39` |  |
| **`GPF`** | `40` |  |
| **`GDD`** | `41` |  |
| **`GDF`** | `42` |  |
| **`GFF`** | `43` |  |
| ** *Slater-Condon 参数（单位为 eV）：*** |  |  |

| **`F2PP`** | 无 |

         - `44`
         - 


| | **`45`** |  |
| --- | --- | --- |
| **`F2PD`** | `45` |  |
| **`F2DD`** | `46` |  |
| **`F4DD`** | `47` |  |
| **`G1SP`** | `48` |  |
| **`G1PD`** | `49` |  |
| **`G2SD`** | `50` |  |
| **`G3PD`** | `51` |  |
| **`R1SPPD`** | `52` |  |
| **`R2SDPP`** | `53` |  |
| **`R2SDDD`** | `54` |  |
| ** *Dewar 型模型的核排斥参数（The nuclear repulsion parameters for Dewar type models）：*** |  |  |

| **`NR1`** | 无 |

         - `55`
         - 


| | **`56`** |  |
| --- | --- | --- |
| **`NR2`** | `56` |  |
| **`NR3`** | `57` |  |
| **`NR4`** | `58` |  |
| **`NR5`** | `59` |  |
| **`NR6`** | `60` |  |
| **`NR7`** | `61` |  |
| **`NR8`** | `62` |  |
| **`NR9`** | `63` |  |
| **`NR10`** | `64` |  |
| **`NR11`** | `65` |  |
| **`NR12`** | `66` |  |
| **`NR13`** | `67` |  |
| ** *MNDO/d 的核吸引/排斥参数（Nuclear attraction/repulsion parameter for MNDO/d）：*** |  |  |

| **`RHO`** | 无 |

         - `68`
         - 


| | **值** |
| --- | --- |
| ** *自旋轨道耦合参数（Spin orbit coupling parameters）：*** |  |

| **`SOCP`** | 无 |

         - `69`
         - p 壳层的 SOC


| | **`70`** | d 壳层的 SOC |
| --- | --- | --- |
| **`SOCD`** | `70` | d 壳层的 SOC |
| **`SOCF`** | `71` | f 壳层的 SOC |

"分子"参数同样在 `%ndoparas` 块中使用 "`INTFA`"（"相互作用因子"，interaction factors）设置：

```orca
%ndoparas  
   INTFA[PP_PI] 0.585
  # The interaction factors exist for
  #  ss_sigma
  #  sp_sigma
  #  sd_sigma
  #  pp_sigma
  #  pd_sigma
  #  dd_sigma
  #  pp_pi
  #  pd_pi
  #  dd_pi
  #  dd_delta
  # the parameter entering the Coulomb integrals
  # in INDO/S
   FGAMMA 1.2
end
```
<a id="sec:modelchemistries.semiempirical.ndo.keywords"></a>
### 关键词（Keywords）

<a id="tab:modelchemistries.semiempirical.ndo.keywords.simple"></a>
!!! note "基于 NDO 的方法的简单输入关键词（Simple input keywords for the NDO-based methods）。"


| ****关键词（Keyword）**** | 描述（Description） |
| --- | --- |
| **`AM1`** | 激活 AM1 |
| **`PM3`** | 激活 PM3 |
| **`MNDO`** | 激活 MNDO |
| **`ZINDO/1`** | 激活 ZINDO/1 |
| **`ZINDO/2`** | 激活 ZINDO/2 |
| **`ZINDO/S`** | 激活 ZINDO/S |
| **`ZNDDO/1`** | 激活 ZNDDO/1 |
| **`ZNDDO/2`** | 激活 ZNDDO/2 |

<a id="tab:modelchemistries.semiempirical.ndo.keywords.block"></a>
!!! note "基于 NDO 的方法的 `%method` 块输入关键词（`%method` block input keywords for the NDO-based methods）。"

    | 关键词（Keyword） | 选项（Options） | 描述（Description） |
    |---|---|---|
    | `METHOD` | `AM1` | 激活 AM1 |
    |  | `PM3` | 激活 PM3 |
    |  | `MNDO` | 激活 MNDO |
    |  | `CNDO_1` | 激活 CNDO/1 |
    |  | `CNDO_2` | 激活 CNDO/2 |
    |  | `CNDO_S` | 激活 CNDO/S |
    |  | `INDO_1` | 激活 INDO/1 |
    |  | `INDO_2` | 激活 INDO/2 |
    |  | `INDO_S` | 激活 INDO/S |
    |  | `ZINDO_1` | 激活 ZINDO/1 |
    |  | `ZINDO_2` | 激活 ZINDO/2 |
    |  | `ZINDO_S` | 激活 ZINDO/S |
    |  | `ZNDDO_1` | 激活 ZNDDO/1 |
    |  | `ZNDDO_2` | 激活 ZNDDO/2 |
    |  | `CNDO` | 激活 CNDO，需要设置 `VERSION` |
    |  | `INDO` | 激活 INDO，需要设置 `VERSION` |
    |  | `NDDO` | 激活 NDDO，需要设置 `VERSION` |
    | `VERSION` | `CNDO_1` | 将 CNDO 的参数集设为 `CNDO_1` |
    |  | `CNDO_2` | 将 CNDO 的参数集设为 `CNDO_2` |
    |  | `CNDO_S` | 将 CNDO 的参数集设为 `CNDO_S` |
    |  | `INDO_1` | 将 INDO 的参数集设为 `INDO_1` |
    |  | `INDO_2` | 将 INDO 的参数集设为 `INDO_2` |
    |  | `INDO_S` | 将 INDO 的参数集设为 `INDO_S` |
    |  | `ZINDO_1` | 将 INDO 的参数集设为 `ZINDO_1` |
    |  | `ZINDO_2` | 将 INDO 的参数集设为 `ZINDO_2` |
    |  | `ZINDO_S` | 将 INDO 的参数集设为 `ZINDO_S` |
    |  | `ZNDDO_1` | 将 NDDO 的参数集设为 `ZNDDO_1` |
    |  | `ZNDDO_2` | 将 NDDO 的参数集设为 `ZNDDO_2` |
    |  | `MNDO` | 将 NDDO 的参数集设为 `MNDO` |
    |  | `AM1` | 将 NDDO 的参数集设为 `AM1` |
    |  | `PM3` | 将 NDDO 的参数集设为 `PM3` |

<a id="sec:modelchemistries.semiempirical.xtb"></a>
## 扩展紧束缚方法（Extended Tight-Binding）：GFN0-xTB、GFN-xTB、GFN2-xTB

ORCA 与 Grimme 及其同事的 xtb 程序进行了对接，允许用户使用流行的 GFN0-xTB、GFN-xTB 和 GFN2-xTB 哈密顿量（Hamiltonians）进行各类计算。[grimme2017xtb,grimme2019xtb,pracht2019xtb](../../bibliography.md) 在技术层面，用户需要提供 Grimme 课题组发布的可执行文件。xtb 程序包可以从 <https://github.com/grimme-lab/xtb/releases> 免费获取，关于 `xtb` 独立程序及其工具的详细使用信息可在 <https://xtb-docs.readthedocs.io/en/latest/contents.html> 找到。ORCA 仅使用其中的 `bin/xtb` 文件。用户应将该文件复制到其他 ORCA 可执行文件所在的目录，并将其重命名为 `otool_xtb`。

!!! warning "警告"
    - 请使用 6.7.1 版本（或任何更新版本）的 `xtb`；较旧的版本与 ORCA 不再完全兼容，或者缺少功能，例如可能无法调用溶剂化模型（solvation model）！此外，Windows 用户应将 `libiomp5md.dll` 从 XTB 目录复制到 ORCA 目录。
    - 在 Linux 上，只有当默认 shell（即 `/bin/sh`）符合 POSIX 标准时 `xtb` 接口才能工作，例如 `bash` 或 `dash`，而 `csh` 或 `tcsh` 不行。

xTB 方法可通过 `GFN0-xTB`、`GFN-xTB` 和 `GFN2-xTB` 关键词调用。GFN-FF 通用力场（generic force-field）可通过 `GFN-FF` 调用：

```orca
! GFN0-xTB  # Synonym: XTB0
```
```orca
! GFN-xTB  # Synonym: XTB1
```
```orca
! GFN2-xTB  # Synonym: XTB2
```
```orca
! GFN-FF # Synonym: XTBFF
```

以下方法可与 XTB 结合使用：

-   单点能计算（Single Point Energy）

-   能量与梯度（Energy and Gradient）

-   优化，支持各类约束（constraints）、弛豫势能面扫描（relaxed surface scans）等

-   微动弹性带（Nudged-Elastic Band）计算

-   数值频率计算（Numerical Frequency Calculations）

-   内禀反应坐标（Intrinsic Reaction Coordinate）

-   分子动力学计算（Molecular Dynamics Calculations）

-   QM/MM 计算

!!! note "注意"

    -   XTB0 是一种非自洽（non-self-consistent）紧束缚方法，因此其精度通常不如 XTB1 和 XTB2（有时甚至不如 XTBFF），尽管它比 XTB1 和 XTB2 快几倍。根据我们的经验，只有当 XTB1 和 XTB2 对感兴趣的体系都出现定性失败时，才推荐使用 XTB0。

    -   请注意，XTB0、XTB1 和 XTB2 也可用于初始路径的生成，或用于在 XTB 水平上计算初始过渡态（TS）结构，二者均可作为后续更高理论水平 NEB 计算的输入。更多细节请参阅章节 [structurereactivity.neb](../structurereactivity/neb.md#sec:structurereactivity.neb)。

<a id="sec:modelchemistries.semiempirical.xtb.solvation"></a>
### xTB 中的溶剂化（Solvation in xTB）

xTB 计算中可以请求三种隐式溶剂化模型（implicit solvation models）：
1. 解析线性化泊松-玻尔兹曼（analytical linearized Poisson-Boltzmann, ALPB）[grimme2021alpb](../../bibliography.md) 溶剂化模型
2. 区域分解 COSMO（domain decomposition COSMO, ddCOSMO）[ddcosmo2013](../../bibliography.md)
3. 扩展类导体极化连续模型（extended conductor-like polarizable continuum model, CPCM-X）。[cpcmx2023](../../bibliography.md)

这些模型可通过简单关键词输入来请求：

```orca
! ALPB(solvent) # use ALPB
```
```orca
! DDCOSMO(solvent) # use ddCOSMO
```
```orca
! CPCMX(solvent) # use CPCMX
```

其中 `solvent` 可为 [tab:modelchemistries.semiempirical.xtb.solvation.solvents](#tab:modelchemistries.semiempirical.xtb.solvation.solvents) 中的任何溶剂。

它们也可以通过 `%xtb` 块调用，这里以 ALPB 为例：

```orca
%xtb
  DOALPB true
  ALPBSOLVENT "water"
end
```

<a id="tab:modelchemistries.semiempirical.xtb.solvation.solvents"></a>
!!! note "可与 `xtb` 一起使用的不同隐式溶剂化方法的可用溶剂列表（List of available solvents for the different implicit solvation methods that can be used with `xtb`）。"
    |  溶剂（Solvent）             |  ALPB     |   ddCOSMO  |   CPCM-X  |
    |:---------------------|:---------:|:----------:|:---------:|
    |	1,2,4-trimethylbenzene	|		|		|	X	|
    |	1,2-dichloroethane	|		|		|	X	|
    |	1,4-dioxane / dioxane	|	X	|	X	|		|
    |	1-butanol / butanol	|		|		|	X	|
    |	1-chlorohexane / chlorohexane	|		|		|	X	|
    |	1-decanol / decanol	|		|		|	X	|
    |	1-fluorooctane	|		|		|	X	|
    |	1-heptanol / heptanol	|		|		|	X	|
    |	1-hexanol / hexanol	|		|		|	X	|
    |	1-iodohexadecane / hexadecyliodide	|		|		|	X	|
    |	1-nonanol / nonanol	|		|		|	X	|
    |	1-octanol / octanol	|	X	|	X	|	X	|
    |	1-pentanol / pentanol	|		|		|	X	|
    |	1-propanol / propanol	|		|		|	X	|
    |	2,2,4-trimethylpentane / isooctane	|		|		|	X	|
    |	2,6-dimethylpyridine	|		|		|	X	|
    |	2-butanol / secbutanol	|		|		|	X	|
    |	2-methoxyethanol / methoxyethanol	|		|		|	X	|
    |	2-methyl-1-propanol / isobutanol	|		|		|	X	|
    |	2-methylpyridine / 2methylpyridine	|		|		|	X	|
    |	2-propanol / isopropanol	|		|		|	X	|
    |	4-methyl-2-pentanone / 4methyl2pentanone	|		|		|	X	|
    |	acetic acid / aceticacid	|		|		|	X	|
    |	acetone	|	X	|	X	|		|
    |	acetonitrile / mecn / ch3cn	|	X	|	X	|	X	|
    |	acetophenone	|		|		|	X	|
    |	aniline	|	X	|	X	|	X	|
    |	anisole	|		|		|	X	|
    |	benzaldehyde	|	X	|	X	|		|
    |	benzene	|	X	|	X	|	X	|
    |	benzonitrile	|		|		|	X	|
    |	benzyl alcohol / benzylalcohol	|		|		|	X	|
    |	bromobenzene	|		|		|	X	|
    |	bromoethane	|		|		|	X	|
    |	bromoform	|		|		|	X	|
    |	butanone	|		|		|	X	|
    |	butyl ethanoate / butyl acetate / butylacetate	|		|		|	X	|
    |	n-butylbenzene / butylbenzene	|		|		|	X	|
    |	sec-butylbenzene / secbutylbenzene	|		|		|	X	|
    |	tert-butylbenzene / tbutylbenzene	|		|		|	X	|
    |	carbon disulfide / carbondisulfide / cs2	|	X	|	X	|	X	|
    |	carbon tetrachloride / ccl4	|		|		|	X	|
    |	chlorobenzene	|		|		|	X	|
    |	chloroform / chcl3	|	X	|	X	|	X	|
    |	conductor	|		|	X	|		|
    |	m-cresol / mcresol	|		|		|	X	|
    |	cyclohexane	|		|		|	X	|
    |	cyclohexanone	|		|		|	X	|
    |	decalin	|		|		|	X	|
    |	n-decane / decane	|		|		|	X	|
    |	dibromomethane	|		|		|	X	|
    |	dibutylether	|		|		|	X	|
    |	o-dichlorobenzene / odichlorobenzene	|		|		|	X	|
    |	dichloromethane / ch2cl2 / dcm	|	X	|	X	|	X	|
    |	diethyl ether / diethylether	|	X	|	X	|	X	|
    |	diisopropyl ether / diisopropylether	|		|		|	X	|
    |	n,n-dimethylacetamide / dimethylacetamide	|		|		|	X	|
    |	n,n-dimethylformamide / dimethylformamide / dmf	|	X	|	X	|	X	|
    |	dimethylsulfoxide / dmso	|	X	|	X	|	X	|
    |	diphenylether	|		|		|	X	|
    |	n-dodecane / dodecane	|		|		|	X	|
    |	ethanol	|	X	|	X	|	X	|
    |	ethyl acetate / ethylacetate / ethanoate	|	X	|	X	|	X	|
    |	ethyl phenyl ether / ethoxybenzene	|		|		|	X	|
    |	ethylbenzene	|		|		|	X	|
    |	fluorobenzene	|		|		|	X	|
    |	furan / furane	|	X	|	X	|		|
    |	n-heptane / heptane	|		|		|	X	|
    |	n-hexadecane / hexadecane	|	X	|	X	|	X	|
    |	n-hexane / hexane	|	X	|	X	|	X	|
    |	iodobenzene	|		|		|	X	|
    |	isopropylbenzene	|		|		|	X	|
    |	p-isopropyltoluene / isopropyltoluene	|		|		|	X	|
    |	mesitylene	|		|		|	X	|
    |	methanol	|	X	|	X	|	X	|
    |	n-methylformamide / methylformamide	|		|		|	X	|
    |	nitrobenzene / phno2	|		|		|	X	|
    |	nitroethane	|		|		|	X	|
    |	nitromethane / meno2	|	X	|	X	|	X	|
    |	o-nitrotoluene / onitrotoluene	|		|		|	X	|
    |	n-nonane / nonane	|		|		|	X	|
    |	n-octane / octane	|		|		|	X	|
    |	n-pentadecane / pentadecane	|		|		|	X	|
    |	octanol(wet) / wetoctanol / woctanol	|	X	|	X	|		|
    |	n-pentane / pentane	|		|		|	X	|
    |	perfluorobenzene / hexafluorobenzene	|		|		|	X	|
    |	phenol	|	X	|	X	|		|
    |	pyridine	|		|		|	X	|
    |	tetrachloroethene / c2cl4	|		|		|	X	|
    |	tetrahydrofuran / thf	|	X	|	X	|	X	|
    |	tetrahydrothiophene-s,s-dioxide / tetrahydrothiophenedioxide / sulfolane	|		|		|	X	|
    |	tetralin	|		|		|	X	|
    |	toluene	|	X	|	X	|	X	|
    |	tributylphosphate	|		|		|	X	|
    |	triethylamine	|		|		|	X	|
    |	n-undecane / undecane	|		|		|	X	|
    |	water / h2o	|	X	|	X	|	X	|
    |	xylene	|		|		|	X	|

!!! note "注意"
    -   如果作业跨多个节点运行，XTB 工具实际使用的核心数可能低于通过 pal 关键词所请求的数量。

### 关键词（Keywords）

<a id="tab:modelchemistries.semiempirical.xtb.keywords.simple"></a>
!!! note "扩展紧束缚方法的简单输入关键词（Simple input keywords for the extended tight-binding methods）。"


| ****关键词（Keyword）**** | 描述（Description） |
| --- | --- |
| **`XTB`** | 激活 GFN2-xTB |
| **`XTB0`** | 激活 GFN0-xTB |
| **`GFN0-XTB`** | 激活 GFN0-xTB |
| **`XTB1`** | 激活 GFN1-xTB |
| **`GFN1-XTB`** | 激活 GFN1-xTB |
| **`XTB2`** | 激活 GFN2-xTB |
| **`GFN2-XTB`** | 激活 GFN2-xTB |
| **`XTBFF`** | 激活 GFN-FF |
| **`GFN-FF`** | 激活 GFN-FF |
| **`ALPB(<solvent>)`** | 为 `<solvent>` 激活 ALPB 溶剂化，例如 ALPB(Water) |
| **`DDCOSMO(<solvent>)`** | 为 `<solvent>` 激活 DDCOSMO 溶剂化，例如 DDCOSMO(Water) |
| **`CPCMX(<solvent>)`** | 为 `<solvent>` 激活 CPCMX 溶剂化，例如 CPCMX(Water) |

<a id="tab:modelchemistries.semiempirical.xtb.keywords.block"></a>
!!! note "扩展紧束缚方法的 `%xtb` 块输入关键词（`%xtb` block input keywords for the extended tight-binding methods）。"


| ****关键词（Keyword）**** | 选项（Options） | 描述（Description） |
| --- | --- | --- |
| **`XTBINPUTSTRING`** | `"<string>"` | 将字符串传递给 `otool_xtb` 调用 |
| **`XTBINPUTSTRING2`** | `"<string>"` | 将字符串传递给 `otool_xtb` 调用 |
| **`NPROCS`** | `<integer>` | 控制 `otool_xtb` 运行的处理器数量，默认为 ORCA 的 `PAL` 设置 |
| **`MAXCORE`** | `<integer>` | 为 `xtb` 运行预留的内存（MB），默认为 ORCA 的 `maxcore` 设置 |
| **`ACCURACY`** | `<real>` | `otool_xtb` 中 `--acc` 的精度设置，默认为 ORCA 的精度乘以 1.e6 |
| **`DOALPB`** | `true`/`false` | 在 `xtb` 运行中激活 ALPB 溶剂化 |
| **`ALPBSOLVENT`** | `"<solvent>"` | 控制 ALPB 所用的 `<solvent>` |
| **`DODDCOSMO`** | `true`/`false` | 在 `xtb` 运行中激活 DDCOSMO 溶剂化 |
| **`DDCOSMOSOLVENT`** | `"<solvent>"` | 控制 DDCOSMO 所用的 `<solvent>` |
| **`EPSILON`** | `<real>` | 控制介电常数，仅用于 ddCOSMO |
| **`DOCPCMX`** | `true`/`false` | 在 `xtb` 运行中激活 CPCMX 溶剂化 |
| **`CPCMXSOLVENT`** | `"<solvent>"` | 控制 CPCMX 中所用的 `<solvent>` |
| **`ETEMP`** | `<real>` | 控制 `otool_xtb` 中的电子温度 `--etemp` |

<a id="sec:modelchemistries.semiempirical.nativextb"></a>
## 原生 GFN-xTB 与 GFN2-xTB（Native GFN-xTB and GFN2-xTB）
!!! note "6.1.0"
    GFN1-xTB 和 GFN2-xTB 的原生实现

ORCA 拥有自己的 GFN-xTB 和 GFN2-xTB 原生实现。与 `xtb` 程序的接口不同，原生 xTB 实现可以使用 [SCF](../essentialelements/scf.md#sec:essentialelements.scfconvergence) 和 [绘图](../utilitiesvisualization/plots.md#sec:utilities.plots) 基础设施。

原生 xTB 方法可通过 `!Native-GFN-xTB`、`!Native-GFN2-xTB` 简单关键词调用：

```orca
! Native-GFN-xTB  # Synonym: Native-GFN1-xTB, Native-XTB1
```
```orca
! Native-GFN2-xTB # Synonym: Native-XTB2
```

!!! warning "警告"
    为了基于原子电荷和多极矩（multipole moments）实现更快的 SCF 重启（restart），原生 xTB 方法会写入一个 `basename.xtbw` 文件。如果存在这样的 `.xtbw` 文件，它将替代 `.gbw` 文件用于重启。

<a id="sec:modelchemistries.semiempirical.nativecustomparam"></a>
### 自定义参数化（Custom parameterization）

原生实现支持使用自定义半经验参数，方法是读取名为 `basename.xtb.json` 的 JSON 参数文件。该文件与 dxtb 程序中的 JSON 文件格式相同（[dxtb 文档](https://dxtb.readthedocs.io/en/latest/)），可通过写出内部参数来生成。半经验参数的读写可通过 `%method` 块开启和关闭：

```orca
%method
  XTBParamFile "orca.xtb.json" # set parameter filename to orca.xtb.json
  WriteXTBParam true      # if true: write parameters to orca.xtb.json file
  WriteXTBParamDry false  # if true: write parameters to orca.xtb.json file
                          # and exit
  ReadXTBParam false      # if true: read parameters from orca.xtb.json file
end
```

默认情况下，参数文件将根据您计算的 basename 命名（`basename.xtb.json`），但可以通过 method 块中的 `XTBParamFile` 选项选择其他名称。若要进行一次仅从默认参数生成参数文件的空运行（dry run），请设置 `WriteXTBParamDry true`。

!!! warning "警告"
    请注意，原生 xTB 实现不允许更改基组。

<a id="sec:modelchemistries.semiempirical.nativextb.spinpol"></a>
### 自旋极化的原生 xTB（Spin-polarized native xTB）
原始 GFNn-xTB 方法的能量表达式是自旋无关的（spin-independent）。因此，即使对于开壳层体系，计算通常也使用 RHF/RKS 型波函数进行。由于自旋不进入能量表达式，具有较高自旋多重度的电子态其能量总是高于相应的低自旋态。
自旋极化 xTB 方法解决了这一缺陷。自旋极化变体[grimme2023spxtb](../../bibliography.md)，称为 spGFN1-xTB 和 spGFN2-xTB，采用了一个简单的在位（on-site）自旋依赖项，可以稳定高自旋态，并允许用 xTB 方法筛选潜在的高自旋组态（high-spin configurations）。

原生自旋极化 xTB 方法可通过 `!Native-spGFN1-xTB`、`!Native-spGFN2-xTB` 简单关键词调用：

```orca
! Native-spGFN1-xTB  # Synonym: Native-spGFN-xTB, Native-spXTB1
```
```orca
! Native-spGFN2-xTB # Synonym: Native-spXTB2
```

注意，自旋极化项只影响高自旋态。与 RHF/RKS 型计算相比计算成本会增加，因为底层的 UHF/UKS 型波函数需要两次 Fock 矩阵对角化而不是一次——成本大约翻倍。

<a id="sec:modelchemistries.semiempirical.nativextb.scf"></a>
### 使用原生 xTB 的 SCF（SCF with native xTB）
原生 xTB 方法默认采用特殊的 SCF 设置，以模拟 `xtb` 程序的 SCF 流程，并覆盖所有其他 ORCA SCF 设置。这些特殊设置利用了 xTB 特有的功能，最显著的是 Fock 矩阵可以仅由原子电荷和多极矩构造。
由于这些捷径，这些特殊 SCF 设置对 xTB 方法通常比 ORCA 默认 SCF 更快。不过，默认 SCF 更稳健（robust），可能在 `xtb` SCF 失败的问题情形下成功收敛。

若要改用标准的 ORCA SCF 基础设施，请在 `%scf` 块中将 `UseXTBMixer` 设为 false：

```orca
%scf
  UseXTBMixer false    # if true (default): special xTB SCF is used
end
```

使用 ORCA 默认 SCF 基础设施时，往往可以收敛具有挑战性的电子结构，但结果应谨慎使用。在必须强制 SCF 收敛的情况下，GFNn-xTB 哈密顿量往往不足以描述所处理的体系。此时应检查 Mulliken 电荷是否合理，并且可能需要通过上述参数文件略微调整逐元素的对参数（pair parameters）。

!!! warning "警告"
    注意，对于 xTB 方法，所有 SCF 迭代都是直接（direct）的。

<a id="sec:modelchemistries.semiempirical.nativextb.fod"></a>
### 使用原生 xTB 的 FOD（FOD with native xTB）
为了更好地考虑静态关联（static correlation），xTB 方法默认使用[有限温度 SCF](../essentialelements/scf.md#sec:essentialelements.scf.finitetemp)，电子温度为 300 K。相应的[分数占据数加权密度（fractional occupation number weighted density, FOD）](../spectroscopyproperties/fod.md#sec:spectroscopyproperties.fod)默认不打印，因为 300 K 这一温度太低，不适合作为诊断工具使用。通过在 `%scf` 输入块中将 `XTBFOD` 设为 true，可以启用 FOD 打印。电子温度可以像其他方法一样通过 `SmearTemp` 关键词控制：

```orca
%scf
  XTBFOD true    # if true: Enable FOD printout and add FOD to density container
  SmearTemp 5000 # 5000 K is typically used for FOD plots with xTB methods
end
```

<a id="sec:modelchemistries.semiempirical.nativextb.solvation"></a>
### 原生 xTB 中的溶剂化（Solvation in native xTB）
xTB 的原生实现包含 ALPB 溶剂化模型，可用溶剂与 `xtb` 程序中相同（[见上文](#tab:modelchemistries.semiempirical.xtb.solvation.solvents)）。它通过与外部 ALPB 相同的关键词、经由简单关键词输入来控制：

```orca
! ALPB(solvent) # use ALPB
```

 此外，原生实现可以与 ORCA 中提供的其他[溶剂化模型](../essentialelements/solvationmodels.md#sec:essentialelements.solvationmodels) 一起使用，但需要注意的是，与 xTB 计算相比 CPCM 和 SMD 模型相当昂贵，因此推荐使用更快的 ALPB 溶剂化模型。

<a id="sec:modelchemistries.semiempirical.nativextb.keywords"></a>
### 关键词（Keywords）

<a id="tab:modelchemistries.semiempirical.nativextb.keywords.simple"></a>
!!! note "原生扩展紧束缚方法的简单输入关键词（Simple input keywords for the native extended tight-binding methods）。"


| ****关键词（Keyword）**** | 描述（Description） |
| --- | --- |
| **`NATIVE-XTB`** | 激活原生 GFN2-xTB |
| **`NATIVE-spXTB`** | 激活原生 spGFN2-xTB |
| **`NATIVE-XTB1`** | 激活原生 GFN1-xTB |
| **`NATIVE-spXTB1`** | 激活原生 spGFN1-xTB |
| **`NATIVE-GFN-XTB`** | 激活原生 GFN1-xTB |
| **`NATIVE-spGFN-XTB`** | 激活原生 spGFN1-xTB |
| **`NATIVE-GFN1-XTB`** | 激活原生 GFN1-xTB |
| **`NATIVE-spGFN1-XTB`** | 激活原生 spGFN1-xTB |
| **`NATIVE-XTB2`** | 激活原生 GFN2-xTB |
| **`NATIVE-spXTB2`** | 激活原生 spGFN2-xTB |
| **`NATIVE-GFN2-XTB`** | 激活原生 GFN2-xTB |
| **`NATIVE-spGFN2-XTB`** | 激活原生 spGFN2-xTB |
| **`ALPB(<solvent>)`** | 为 `<solvent>` 激活 ALPB 溶剂化，例如 ALPB(Water) |

<a id="tab:modelchemistries.semiempirical.nativextb.keywords.methodblock"></a>
!!! note "原生扩展紧束缚方法的 `%method` 块输入关键词（`%method` block input keywords for the native extended tight-binding methods）。"


| ****关键词（Keyword）**** | 选项（Options） | 描述（Description） |
| --- | --- | --- |
| **`WRITEXTBPARAM`** | `true/false` | 将半经验参数写入 xtb.json 文件 |
| **`WRITEXTBPARAMDRY`** | `true/false` | 将半经验参数写入 xtb.json 文件并中止 |
| **`READXTBPARAM`** | `true/false` | 从 xtb.json 文件读取半经验参数 |
| **`XTBPARAMFILE`** | `"filename.xtb.json"` | 将 xtb.json 文件名指定为 "filename.xtb.json" |

<a id="tab:modelchemistries.semiempirical.nativextb.keywords.scfblock"></a>
!!! note "原生扩展紧束缚方法的 `%scf` 块输入关键词（`%scf` block input keywords for the native extended tight-binding methods）。"


| ****关键词（Keyword）**** | 选项（Options） | 描述（Description） |
| --- | --- | --- |
| **`XTBFOD`** | `true/false` | 启用 FOD 打印 |
| **`UseXTBMixer`** | `true/false` | 使用与 `xtb` 中类似的特殊 SCF 设置 |

