
<a id="sec:modelchemistries.dft"></a>
# 密度泛函理论（Density Functional Theory, DFT）

由于其良好的成本-精度比（cost-accuracy ratio），Kohn-Sham 密度泛函理论（DFT）已成为量子化学的主力方法（workhorse）。
在过去几十年间，已经发展出了一整个"泛函动物园"（zoo of density functionals），它们在构造方式和设计理念上各不相同。
Perdew 提出的所谓雅各布天梯（Jacob's Ladder）图景（[fig:modelchemistries.dft.jacobsladder](#fig:modelchemistries.dft.jacobsladder)）[perdew2001jacobsladder](../../bibliography.md) 根据密度泛函的基本物理成分将其划分为不同的层级（rungs）。
层级越高，相应泛函的成本越高，但从概念上预期精度也更高。
然而，密度泛函的精度差异很大，通常建议仔细研究基准测试（benchmark studies）的结果。

<a id="fig:modelchemistries.dft.jacobsladder"></a>
*:width: 400px

密度泛函的雅各布天梯图景（Jacob's ladder picture）。*

ORCA 在每个层级都提供了多种密度泛函，有的是原生实现，有的则通过 [dft.libxc](#sec:modelchemistries.dft.libxc) 提供。
这些泛函可以与各种[基组](../essentialelements/basisset.md)和[相对论方法](../essentialelements/relativistic.md)结合使用。
此外，ORCA 还提供了一套实用的[分辨率恒等式（resolution-of-identity, RI）](../essentialelements/RI.md)方法工具包，用于加速 DFT 计算。

关于可与 DFT 一起使用的色散校正（dispersion corrections）及相应的泛函专属参数，请参阅[色散校正章节](../modelchemistries/dispersioncorrections.md)。

另请注意，某些泛函（如 SCAN 和 Minnesota 系列）可能需要增强的[数值积分网格设置](../essentialelements/numericalintegration.md)。

<a id="sec:modelchemistries.dft.basicusage"></a>
## 基本用法（Basic Usage）

所有已实现的 DFT 方法都可以通过各自的关键词调用，例如使用简单输入行的 `!PBE`：

```orca
! PBE
```
!!! warning "警告"
    如果只定义了泛函，将使用各种默认设置，包括较小的 def2-SVP 基组、适当的 [RI](../essentialelements/RI.md) 处理以及默认的[数值积分网格](../essentialelements/numericalintegration.md)！为获得更高的精度，尤其应该调整[基组](../essentialelements/basisset.md)！

许多泛函也可以通过 `%method` 块调用，不过由于技术原因双杂化泛函（double-hybrid functionals）不可用：

```orca
%method
   Method DFT        # equivalent to method DFGTO
   Functional PBE
end
```

ORCA 还通过 `%method` 块提供更多实用功能，用于构造和修改泛函。这些专家选项在各泛函层级的相应章节中描述。各种其他泛函也可以通过 [dft.libxc](#sec:modelchemistries.dft.libxc) 调用。

!!! warning "警告"
    只有在简单输入中选择了 DFT 泛函时，[RI](../essentialelements/RI.md#sec:essentialelements.ri)/[RIJCOSX](../essentialelements/RI.md#sec:essentialelements.ri.rijcosx) 才会默认激活！
    如果改用 `%method` 块，则应通过 `!RI` 或 `!RIJCOSX` 显式指定这些近似。

<a id="sec:modelchemistries.dft.local"></a>
## 局域泛函（Local Functionals）

局域交换-关联泛函（local exchange-correlation functionals）是按照公式 [Eq](#eqn:modelchemistries.dft.gga.exlocal) 构造的最基本的一类泛函：

<a id="eqn:modelchemistries.dft.gga.exlocal"></a>

$$
E_{\text{XC} } = E_{\text{LSD} }^{\text{X} } + E_{\text{LSD} }^{\text{C} }\qquad \text{(eqn:modelchemistries.dft.gga.exlocal)}
$$

它们通常将原始的斯莱特交换泛函（Slater exchange functional）与不同的局域关联泛函（如 VWN-V[vosko1980can](../../bibliography.md) 或 PW-LDA[perdew1992physb](../../bibliography.md)）组合使用。
ORCA 中所有可用的局域泛函见 [tab:modelchemistries.dft.local](#tab:modelchemistries.dft.local)。

<a id="tab:modelchemistries.dft.local"></a>
!!! note "可用局域泛函列表（List of available local functionals）。"
    | 泛函（Functional）                       | 关键词（Keywords） | 描述（Description）                                                |
    |:-------------------------------------|:-------------|:------------------------------------------------------------|
    | HFS                                  | `HFS`        | 仅含 Hartree--Fock--Slater 交换的泛函                               |
    | LDA or LSD                           | `LDA`, `LSD` | 局域密度近似（local density approximation，默认为 VWN5）               |
    | VWN-V [vosko1980can](../../bibliography.md)           | `VWN`,`VWN5` | Vosko-Wilk-Nusair 局域密度近似参数集 "V"                               |
    | VWN-III [vosko1980can](../../bibliography.md)         | `VWN3`       | Vosko-Wilk-Nusair 局域密度近似参数集 "III"                              |
    | PW-LDA [perdew1992physb](../../bibliography.md)       | `PWLDA`      | LDA 的 Perdew-Wang 参数化                                         |

<a id="sec:modelchemistries.dft.gga"></a>
## 梯度校正泛函（Gradient Corrected Functionals）：(meta-)GGA

下一个层级对应于广义梯度近似（generalized gradient approximation, GGA）和 meta-广义梯度近似（meta-GGA）类型的梯度校正泛函。
这些类型泛函的简化交换-关联能量表达式见 [Eq](#eqn:modelchemistries.dft.gga.excgga)。(meta-)GGA 由于计算成本相对较低，特别适用于[几何优化](../structurereactivity/optimizations.md)和筛选（screening）用途。

<a id="eqn:modelchemistries.dft.gga.excgga"></a>

$$
E_{\text{XC} } = E_{\text{LSD} }^{\text{X} } + E_{\text{GGA} }^{\text{X} } + E_{\text{LSD} }^{\text{C} } + E_{\text{GGA} }^{\text{C} }\qquad \text{(eqn:modelchemistries.dft.gga.excgga)}
$$

<a id="tab:modelchemistries.dft.gga"></a>
!!! note "可用 (meta-)GGA 泛函列表（List of available (meta-)GGA functionals）。"
    | 泛函（Functional）    | 关键词（Keyword） | 描述（Description） |
    |:----------------|:--------|:------------|
    | **GGAs** | | |
    | BP86 [becke1988phys, perdew1986phys](../../bibliography.md) | `BP86`       | Becke '88 交换与 Perdew '86 关联  |
    | BLYP [BLYP](../../bibliography.md) | `BLYP`       | Becke '88 交换与 Lee-Yang-Parr 关联  |
    | OLYP [handy2001molphys](../../bibliography.md) | `OLYP`       | Handy 的"最优"交换与 Lee-Yang-Parr 关联  |
    | GLYP [gill1996mol](../../bibliography.md) | `GLYP`       | Gill 的 '96 交换与 Lee-Yang-Parr 关联  |
    | XLYP [goddard2004pnas](../../bibliography.md) | `XLYP`       | Xu 与 Goddard 交换与 Lee-Yang-Parr 关联  |
    | PW91 [perdew1991pw91](../../bibliography.md) | `PW91`       | Perdew-Wang '91 GGA 泛函  |
    | mPWPW [barone1997jcp](../../bibliography.md) | `MPWPW`      | 修正的 PW 交换与 PW 关联  |
    | mPWLYP [barone1997jcp](../../bibliography.md) | `MPWLYP`     | 修正的 PW 交换与 LYP 关联  |
    | PBE [perdew1996phys](../../bibliography.md) | `PBE`        | Perdew-Burke-Erzerhoff GGA 泛函  |
    | RPBE [hammer1999phys](../../bibliography.md) | `RPBE`      | "修正的" PBE  |
    | revPBE [zhang1998phys](../../bibliography.md) | `REVPBE`     | "修订的" PBE  |
    | RPW86PBE [rPW86PBE](../../bibliography.md) | `RPW86PBE`   | PBE 关联配以重新拟合的 Perdew '86 交换  |
    | PWP [perdew1991pw91](../../bibliography.md) | `PWP` | Perdew-Wang '91 交换与 Perdew '86 关联  |
    | **composite** | | |
    | B97-3c [grimme2018b973c](../../bibliography.md) | `B97-3C` | Grimme 等人的复合 DFT 方法 |
    | **meta-GGAs** | | |
    | B97M-V [headgordon2015B97MV](../../bibliography.md)    | `B97M-V` | Head-Gordon 的 DF B97M-V，含 VV10 非局域关联  |
    | B97M-D3(BJ) [goerigk2018](../../bibliography.md) | `B97M-D3BJ` | Najibi 和 Goerigk 提出的 B97M-V 修正版，含 D3BJ 校正  |
    | B97M-D4 [najibi2020](../../bibliography.md)   | `B97M-D4` | Najibi 和 Goerigk 提出的 B97M-V 修正版，含 DFT-D4 校正  |
    | SCAN [perdew2015scan](../../bibliography.md)  | `SCANFUNC` | Perdew 的 SCAN 泛函  |
    | rSCAN [bartok2019rscan](../../bibliography.md)     | `RSCAN` | 正则化 SCAN 泛函（Regularized SCAN）
    | r²SCAN [furness2020r2scan](../../bibliography.md)      | `R2SCAN` | Furness、Sun 等人的正则化并恢复的 SCAN 泛函  |
    | M06-L [m06l](../../bibliography.md)      | `M06L` | Minnesota M06-L meta-GGA 泛函  |
    | TPSS [TPSS2003](../../bibliography.md)       | `TPSS` | TPSS meta-GGA 泛函  |
    | revTPSS [revtpss, revtpsserratum](../../bibliography.md)       | `REVTPSS` | 修订的 TPSS meta-GGA 泛函  |
    | **composite** | | |
    | r²SCAN-3c [grimme2020r2scan3c](../../bibliography.md) | `R2SCAN-3C` | Grimme 等人的复合 DFT 方法 |

<a id="sec:modelchemistries.dft.gga.customizexc"></a>
### 基本泛函的定制（Customization of Basic Functionals）

基本交换-关联泛函也可以通过 `%method` 块中的 `Exchange`、`Correlation` 和 `LDAOpt` 关键词从其组成部分构造。
这些分别控制泛函的交换部分、关联部分以及关联泛函的局域部分。
例如 BP86（`!BP86`）由 Becke 的 '88 交换（通过 `X_BECKE`）和 Perdew 的 '86 关联泛函（通过 `C_P86`）构造而成。在 ORCA 中，它还通过 `C_PWLDA` 对关联泛函的局域部分采用 Perdew 和 Wang 的 LDA 重新参数化[perdew1992physb](../../bibliography.md) `PWLDA`：

```orca
%method
   Method DFT
   Exchange     X_BECKE
   Correlation  C_P86
   LDAOpt       C_PWLDA
end
```

可用组成部分的完整列表见 [tab:modelchemistries.dft.gga.customizexc.keywords.block](#tab:modelchemistries.dft.gga.customizexc.keywords.block)。

正确选择关联泛函的局域部分对于确保结果的可重复性（reproducibility）至关重要。在 ORCA 中，几乎所有泛函都选择 `PWLDA`[perdew1992physb](../../bibliography.md) 作为底层 LDA 泛函，因为它比 VWN 更好地拟合了均匀电子气（uniform electron gas）。对于 VWN（Vosko、Wilk 和 Nusair[vosko1980can](../../bibliography.md)），存在若干参数化方式。他们在经典论文中给出了两组参数——一组在正文中（RPA 结果的参数化，称为 VWN-III），另一组在他们的关联能表 5 中（Ceperley/Alder 蒙特卡洛（Monte Carlo）结果的参数化，称为 VWN-V）。PW-LDA 的结果与 VWN-V 非常相似，而 VWN-III 给出的值则大不相同。
多年来，不同量子化学程序对同一泛函名称使用不同参数化的做法造成了一些混淆和结果的偏差。一个突出的例子是 ORCA 和 Gaussian 中 B3LYP [杂化泛函](#sec:modelchemistries.dft.globalhybrids)的不同实现。ORCA 使用与 TURBOMOLE 程序[ahlrichs2000turbo,ahlrichs2000ency,ahlrichs1989chem](../../bibliography.md) 一致的 VNW-V，而 Gaussian 程序[frisch1998gauss](../../bibliography.md) 则采用 VWN-III。使用 `LDAOpt` 关键词可以构造这两种变体：

```orca
# consistent with TURBOMOLE
%method
   Method DFT
   Functional B3LYP
   LDAOpt C_VWN5
end
```

```orca
# consistent with Gaussian
%method
   Method DFT
   Functional B3LYP
   LDAOpt C_VWN3
end
```

为方便起见，这两种泛函可以分别通过简单输入关键词 `!B3LYP`（ORCA/TURBOMOLE 变体）和 `!B3LYP/G`（Gaussian 变体）调用。

!!! note "注意"
    如果 LYP 是关联泛函[lee1988phys](../../bibliography.md)，则会出现一种特殊情况，因为 LYP *不是*对关联的校正，而是包含了完整的关联。
    因此它在 B3LYP 泛函中的用法为：

<a id="eqn:modelchemistries.dft.gga.customizexc.ecb3lyp"></a>

$$
E_{\text{B3LYP} }^{\text{C} } =E_{\text{LSD} }^{\text{C} } +c\left({ E_{\text{LYP} }^{\text{C} } -E_{\text{LSD} }^{\text{C} } } \right)\qquad \text{(eqn:modelchemistries.dft.gga.customizexc.ecb3lyp)}
$$

一些泛函还包含经验参数（empirical parameters），可以通过更改这些参数来改善与实验的符合程度。目前有少数几个参数可以更改（[杂化泛函](#sec:modelchemistries.dft.hybriddft)中使用的参数除外，后者将在后文描述）。
这些参数中的第一个是斯莱特 X$_{\alpha }$ 方法中的 $\alpha$。理论上它的值为 2/3，HFS 和 LSD 泛函中就使用该值。然而，这一近似使交换贡献被低估了约 10%（相当显著！），对于分子建议使用 0.70-0.75 左右的值。第二个参数是 Becke 梯度校正交换泛函中的 $\beta$。
Becke 通过拟合稀有气体原子的交换能确定了值 0.0042。有证据表明，使用较小的基组时，略小一些的值（如 0.0039）对分子能给出改善的结果。
下一个参数是 PBE 交换泛函中出现的值 $\kappa$。Perdew 等人为了满足 Lieb-Oxford 界（Lieb-Oxford bound）将其定为 0.804。此后，其他研究者认为该参数取更大的值（约 1.2）会给出更好的能量学结果，revPBE 泛函就采用了这一思路。不过请注意，虽然 revPBE 给出略好的能量学结果，但几何结构也略差。
最后两个参数也与 PBE 有关。在 PBE 关联泛函中，存在 $\beta_C$（不要与 Becke 交换泛函中的交换参数 $\beta$ 混淆），其原始值为 $\beta_C=0.066725$。存在具有不同 $\beta_C$ 值的修正变体，例如 PBEsol 泛函和 [PBEh-3c 复合方法](3cmethods.md#sec:modelchemistries.3cmethods.pbeh3c)。此外，PBE 交换泛函中的 $\mu$ 参数也可以修改。在原始表述中，它通过 $\mu = \beta_C \frac{\pi^{2} }{3}$ 与 $\beta_C$ 相关联，但在后续变体中也已被修改。
<a id="tab:modelchemistries.dft.gga.customizexc.keywords.block"></a>
!!! note "用于修改基本交换-关联泛函的 `%method` 块输入关键词（`%method` block input keywords to modify basic exchange-correlation functionals）。"
    | 关键词（Keyword）                  | 选项（Options）        | 描述（Description）                                                        |
    |:--------------------------------|:------------------|:--------------------------------------------------------------------|
    | `Exchange`                      | `X_NOX`           | 无交换                                                                 |
    |                                 | `X_SLATER`        | Slater 的局域交换                                                        |
    |                                 | `X_BECKE`         | Becke 的 '88 交换                                                       |
    |                                 | `X_wB88`          | 用于范围分离泛函的短程 Becke '88 交换                                          |
    |                                 | `X_G96`           | Gill '96 梯度交换                                                       |
    |                                 | `X_PW91`          | Perdew-Wang (PW) '91 梯度交换                                            |
    |                                 | `X_mPW`           | Adamo-Barone 对 PW 交换的修正                                             |
    |                                 | `X_PBE`           | Perdew-Burke-Ernzerhof (PBE) 交换                                       |
    |                                 | `X_RPBE`          | 修订的 PBE 交换                                                          |
    |                                 | `X_OPTX`          | Hoe/Cohen/Handy 的优化交换                                                 |
    |                                 | `X_X`             | Xu/Goddard 交换                                                        |
    |                                 | `X_TPSS`          | TPSS meta-GGA 交换                                                     |
    |                                 | `X_B97D`          | Grimme 为 B97-D GGA 所做的修正交换                                          |
    |                                 | `X_B97BECKE`      | Becke 为 B97 杂化泛函所做的原始交换                                             |
    |                                 | `X_SCAN`          | Perdew 为 SCAN meta-GGA 所做的约束交换（constrained exchange）                 |
    |                                 | `X_RSCAN`         | Perdew 为 rSCAN meta-GGA 所做的约束交换                                     |
    |                                 | `X_R2SCAN`        | Perdew 为 r²SCAN meta-GGA 所做的约束交换                                    |
    | `Correlation`                   | `C_NOC`           | 无关联                                                                 |
    |                                 | `C_VWN5`          | 局域 Vosko-Wilk-Nusair 关联（参数集 "V"）                                    |
    |                                 | `C_VWN3`          | 局域 Vosko-Wilk-Nusair 关联（参数集 "III"）                                  |
    |                                 | `C_PWLDA`         | 局域 PW 关联                                                            |
    |                                 | `C_P86`           | Perdew '86 关联                                                        |
    |                                 | `C_PW91`          | PW '91 关联                                                            |
    |                                 | `C_PBE`           | PBE 关联                                                               |
    |                                 | `C_LYP`           | LYP 关联                                                               |
    |                                 | `C_TPSS`          | TPSS meta-GGA 关联                                                     |
    |                                 | `C_B97D`          | Grimme 为 B97-D GGA 所做的修正关联                                          |
    |                                 | `C_B97BECKE`      | Becke 为 B97 杂化泛函所做的原始关联                                             |
    |                                 | `C_SCAN`          | Perdew 为 SCAN meta-GGA 所做的约束关联                                      |
    |                                 | `C_RSCAN`         | Perdew 为 rSCAN meta-GGA 所做的约束关联                                     |
    |                                 | `C_R2SCAN`        | Perdew 为 r²SCAN meta-GGA 所做的约束关联                                    |
    | `LDAOpt`                        | `C_NOC`           | 将任意关联泛函的局域部分设为无关联                                                 |
    |                                 | `C_PWLDA`         | 将任意关联泛函的局域部分设为 PWLDA                                              |
    |                                 | `C_VWN5`          | 将任意关联泛函的局域部分设为 VWN5                                               |
    |                                 | `C_VWN3`          | 将任意关联泛函的局域部分设为 VWN3                                               |
    | **特定参数（Specific Parameters）** |                   |                                                                     |
    | `XAlpha`                        | `<real>`          | 修改 Slater 的 $\alpha$ 参数（默认 2/3）                                    || `XBeta`                         | `<real>`          | 修改 Becke 的 $\beta$ 参数（默认 0.0042）                                   |
    | `XKappa`                        | `<real>`          | 修改 PBE(交换) 的 $\kappa$ 参数（默认 0.804）                                || `XMuePBE`                       | `<real>`          | 修改 PBE(交换) 的 $\kappa$ 参数（默认 0.21952）                              |
    | `CBetaPBE`                      | `<real>`          | 修改 PBE(关联) 的 beta 参数（默认 0.066725）                                 |
<a id="sec:modelchemistries.dft.hybriddft"></a>
## 杂化 DFT（Hybrid DFT）
用哈特里-福克理论的精确交换（exact exchange, HFX）替换部分 DFT 交换的想法是 Becke 于 1993 年提出的[becke1993chem1,becke1993chem2](../../bibliography.md)。
这一方案通常称为杂化 DFT，单参数杂化泛函（one-parameter hybrid functional）最简单的表述见公式 [Eq](#eqn:modelchemistries.dft.hybriddft.exchybrid)
<a id="eqn:modelchemistries.dft.hybriddft.exchybrid"></a>

$$
E_{\text{hyb}}^{\text{XC}} =aE_{\text{HF}}^{\text{X}} + (1-a){ E_{\text{GGA}}^{\text{X}}} + E_{\text{GGA}}^{\text{C}}\qquad \text{(eqn:modelchemistries.dft.hybriddft.exchybrid)}
$$

更一般的描述由绝热连接模型（adiabatic connection model, ACM）给出。在 ACM 中，杂化泛函按照公式 [Eq](#eqn:modelchemistries.dft.hybriddft.acm) 用三个参数构造：
<a id="eqn:modelchemistries.dft.hybriddft.acm"></a>

$$
E_{\text{XC} } = a E_{\text{HF} }^{\text{X} } +\left( 1 - a \right)E_{\text{LSD} }^{\text{X} } +bE_{\text{GGA} }^{\text{X} } +E_{\text{LSD} }^{\text{C} } +cE_{\text{GGA} }^{\text{C} }\qquad \text{(eqn:modelchemistries.dft.hybriddft.acm)}
$$

其中，$E_{\text{XC} }$ 是总交换/关联能，$E_{\text{HF} }^{\text{X} }$ 是哈特里-福克交换，$E_{\text{LSD} }^{\text{X} }$ 是局域（Slater）交换，$E_{\text{GGA} }^{\text{X} }$ 是对交换的梯度校正，$E_{\text{LSD} }^{\text{C} }$ 是关联能中基于自旋密度的局域部分，$E_{\text{GGA} }^{\text{C} }$ 是对关联能的梯度校正。
多年来，人们发展出了构造杂化泛函的各种策略。这些策略从依赖尽可能少参数的物理驱动方法（如总体上平衡良好的 PBE0 泛函[adamo1999chem](../../bibliography.md)）到更经验化的变体（如著名的三参数杂化泛函 B3LYP[b3lyp](../../bibliography.md)）不一而足。
此外，还发展出了对 HF 交换混合比例的各种处理方式。使用固定比例 HFX 的基本杂化泛函通常称为[全局杂化泛函（global hybrids）](#sec:modelchemistries.dft.globalhybrids)，而具有可变 HFX 比例的泛函包括[范围分离杂化泛函（range-separated hybrids）](#sec:modelchemistries.dft.hybriddft.rangeseparatedhybrids)和局域杂化泛函（local hybrids）。ORCA 中提供了各种[全局](#sec:modelchemistries.dft.globalhybrids)和[范围分离杂化泛函](#sec:modelchemistries.dft.hybriddft.rangeseparatedhybrids)。局域杂化泛函可能会在未来版本中实现。
ORCA 还提供了复杂的基础设施，用于创建和[定制全局](#sec:modelchemistries.dft.globalhybrids.customization)及[范围分离杂化泛函](#sec:modelchemistries.dft.rangeseparatedhybrids.customization)。
!!! note "注意"
    由于理论上杂化泛函比 (meta-)GGA 昂贵得多，ORCA 默认使用复杂的 [RIJCOSX](../essentialelements/RI.md) 算法来加速杂化 DFT 计算。
<a id="sec:modelchemistries.dft.globalhybrids"></a>
### 全局杂化泛函（Global Hybrid Functionals）
全局杂化泛函采用固定比例的哈特里-福克精确交换。ORCA 提供了多种具有不同组成和 HFX 比例的代表泛函。最优的 HFX 比例在文献中存在争议，许多经验泛函是通过将其拟合到某个实验性质来构造的。
然而，从理论观点出发，有人认为 HF 交换的最优混合比例为 25%[ernzerhof1998density](../../bibliography.md)，而且已知大比例的 HFX 对过渡金属配合物不利。
原生实现的全局杂化泛函列表见 [tab:modelchemistries.dft.hybriddft.globlhybrids](#tab:modelchemistries.dft.hybriddft.globlhybrids)。
<a id="tab:modelchemistries.dft.hybriddft.globlhybrids"></a>
!!! note "可用全局杂化泛函列表（List of available global hybrid functionals）。"
    | 泛函（Functional）                                    | 关键词（Keyword）   | %HFX  | 描述（Description）                                                                                                 |
    |:----------------------------------------------|:--------------|:-----:|:-------------------------------------------------------------------------------------------------------------|
    | **hybrid GGAs**                               |               |       |                                                                                                              |
    | B1LYP [adamo1997b1lyp](../../bibliography.md)                  | `B1LYP`       | 25    | 单参数杂化泛函，含 Becke '88 交换和 Lee-Yang-Parr 关联（25% HF 交换）                                                       |
    | B3LYP [b3lyp](../../bibliography.md)                           | `B3LYP`       | 20    | 广受欢迎的 B3LYP 泛函（20% HF 交换），定义与 TurboMole 程序体系一致（`LDAOPT C_VWN5`）                                        |
    | B3LYP/G [b3lyp](../../bibliography.md)                         | `B3LYP/G`     | 20    | 广受欢迎的 B3LYP 泛函（20% HF 交换），定义与 Gaussian 程序体系一致（`LDAOPT C_VWN3`）                                         |
    | O3LYP [cohen2001o3lyp](../../bibliography.md)                  | `O3LYP`       | 11.61 | Handy 杂化泛函                                                                                                  |
    | X3LYP [goddard2004pnas](../../bibliography.md)                 | `X3LYP`       | 21.8  | Xu 与 Goddard 杂化泛函                                                                                           |
    | B1P86 [perdew1986phys](../../bibliography.md)                  | `B1P86`       | 25    | BP86 的单参数杂化版本                                                                                              |
    | B3P86 [becke1993chem1](../../bibliography.md)                  | `B3P86`       | 20    | BP86 的三参数杂化版本                                                                                              |
    | B3PW91 [becke1993chem1](../../bibliography.md)                 | `B3PW91`      | 20    | PW91 的三参数杂化版本                                                                                              |
    | PW1PW [adamo1999chem](../../bibliography.md)                   | `PW1PW`       | 25    | PW91 的单参数杂化版本                                                                                              |
    | mPW1PW [barone1997jcp](../../bibliography.md)                  | `MPW1PW`      | 25    | mPWPW 的单参数杂化版本                                                                                             |
    | mPW1LYP [barone1997jcp](../../bibliography.md)                 | `MPW1LYP`     | 25    | mPWLYP 的单参数杂化版本                                                                                            |
    | PBE0 [adamo1999chem](../../bibliography.md)                    | `PBE0`        | 25    | PBE 的单参数杂化版本                                                                                               |
    | revPBE0 [grimme2011gmtkn30](../../bibliography.md)             | `REVPBE0`     | 25    | "修订的" PBE0                                                                                                 |
    | revPBE38 [grimme2011gmtkn30](../../bibliography.md)            | `REVPBE38`    | 37.5  | 带 37.5% HF 交换的"修订的" PBE0                                                                                    |
    | BHandHLYP [becke1993chem1](../../bibliography.md)              | `BHANDHLYP`   | 50    | Becke 的"对半"杂化泛函（half-and-half hybrid）                                                                        |
    | **hybrid meta-GGAs**                          |               |       |                                                                                                              |
    | M06 [m06](../../bibliography.md)                               | `M06`         | 27    | |
    | M06-2X [m06](../../bibliography.md)                            | `M062X`       | 54    | |
    | PW6B95 [zhao2005phys](../../bibliography.md)                   | `PW6B95`      | 28    | |
    | TPSSh [TPSS2003](../../bibliography.md)                        | `TPSSH`       | 10    | TPSS 的杂化版本（10% HF 交换）                                                                                     |
    | TPSS0  [grimme2005tpss0](../../bibliography.md)                | `TPSS0`       | 25    | TPSSh 的 25% 交换版本，给出改善的能量学结果                                                                               |
    | r²SCANh [bursch_r2scanhybrids_2022](../../bibliography.md)     | `R2SCANH`     | 10    | 含 10% HF 交换的 r²SCAN 全局杂化变体                                                                                |
    | r²SCAN0 [bursch_r2scanhybrids_2022](../../bibliography.md)     | `R2SCAN0`     | 25    | 含 25% HF 交换的 r²SCAN 全局杂化变体                                                                                |
    | r²SCAN50 [bursch_r2scanhybrids_2022](../../bibliography.md)    | `R2SCAN50`    | 50    | 含 50% HF 交换的 r²SCAN 全局杂化变体                                                                                |
    | **composite**                                 |               |       |                                                                                                              |
    | PBEh-3c [grimme_pbeh3c](../../bibliography.md)                 | `PBEH-3C`     | 42    | Grimme 等人的复合 DFT 方法                                                                                        |
    | B3LYP-3c [grimme2020b3lyp3c](../../bibliography.md)            | `B3LYP-3C`    | 20    | Grimme 等人的复合 DFT 方法                                                                                        |
<a id="sec:modelchemistries.dft.globalhybrids.customization"></a>
#### 全局杂化泛函的定制（Customization of Global Hybrids）
全局杂化泛函参数可以通过 `%method` 块定制。关于基本交换和关联组成部分的定制，请参阅[基本泛函的定制](#sec:modelchemistries.dft.gga.customizexc)章节。杂化泛函的重要参数是 ACM 模型中使用的那些参数（参见公式 [Eq](#eqn:modelchemistries.dft.hybriddft.acm)）。在此，我们将使用 ACM 语法重建 PBE0 泛函（25% HFX）：
```orca
! RIJCOSX
# PBE0
%method
   Method DFT
   Functional PBE
   ACM_A        0.25      # fraction of Hartree-Fock exchange
   ACM_B        0.75      # fraction of the GGA exchange
   ACM_C        1.00      # fraction of the GGA correlation
   ScalLDAC     1.00      # fraction of LDA correlation, must be
                          # equal to ACM_C 
end
```
为简便起见，ACM 参数也可以作为一个字符串给出。
```orca
! RIJCOSX
# PBE0
%method
   Method DFT
   Functional PBE
   ACM       0.25, 1.00, 1.00   # as ACM   ACM-A, ACM-B, ACM-C
   ScalLDAC  1.00               # fraction of LDA correlation,
                                # must be equal to ACM_C 
end
```
由于 ACM 形式可能不太直观，ORCA 提供了等效的语法来控制相应参数。
```orca
! RIJCOSX
# PBE0
%method
   Method DFT
   Functional PBE
   ScalHFX        0.25      # fraction of Hartree-Fock exchange
   ScalDFX        0.75      # fraction of GGA exchange
   ScalGGAC       1.00      # fraction of GGA correlation
   ScalLDAC       1.00      # fraction of LDA correlation,
                            # must be equal to ScalGGAC 
end
```
!!! warning "警告"
    注意，`Functional` 会为下文描述的变量 `Exchange`、`Correlation`、`LDAOpt` 和 `ACM` 选择特定的预定义值。
    如果作为简单输入关键词给出，在某些情况下它还会激活色散校正。您可以显式给出这些变量来替代或补充 `Functional`。但请确保在给 `Functional` 赋值*之后*再指定这些变量，否则它们会被重置为 `Functional` 所选的值。
<a id="tab:modelchemistries.dft.globalhybrids.customization.keywords.block"></a>
!!! note "用于修改全局杂化泛函的 `%method` 块输入关键词（`%method` block input keywords to modify global hybrid functionals）。"

| ****关键词（Keyword）**** | 选项（Options） | 描述（Description） |
| --- | --- | --- |
| **`ACM`** | `<real, real, real>` | 定义 ACM-A、ACM-B 和 ACM-C 参数 |
| **`ACM_A`** | `<real>` | 定义 ACM-A 参数（哈特里-福克交换的比例） |
| **`ACM_B`** | `<real>` | 定义 ACM-B 参数（GGA 交换的比例） |
| **`ACM_C`** | `<real>` | 定义 ACM-C 参数（GGA 关联的比例） |
| **`ScalHFX`** | `<real>` | 控制哈特里-福克交换的比例，等同于 `ACM_A` |
| **`ScalDFX`** | `<real>` | 控制 GGA 交换的比例，等同于 `ACM_B` |
| **`ScalGGAC`** | `<real>` | 控制 GGA 关联的比例，等同于 `ACM_C` |

<a id="sec:modelchemistries.dft.hybriddft.rangeseparatedhybrids"></a>
### 范围分离杂化泛函（Range-Separated Hybrid Functionals）
与[全局杂化泛函](#sec:modelchemistries.dft.globalhybrids)不同，范围分离杂化（range-separated hybrid, RSH）泛函将用于交换的双电子算符划分为短程（SR）和长程（LR）两个区域，其中短程部分通常由 DFT 交换描述，长程部分由哈特里-福克交换描述。在 ORCA 中，所有范围分离杂化泛函都使用 Hirao 及其同事的误差函数（error function）划分方法来区分这两个区域（参见公式 [Eq](#eqn:modelchemistries.dft.hybriddft.rangeseparatedhybrids.erf)）。[hirao2001rangeseparation](../../bibliography.md) 这允许定义这样的 DFT 泛函：其短程部分由 [LDA](#sec:modelchemistries.dft.local)、[GGA 或 meta-GGA](#sec:modelchemistries.dft.gga) 层级的适当交换泛函主导，长程部分则由哈特里-福克交换主导。
<a id="eqn:modelchemistries.dft.hybriddft.rangeseparatedhybrids.erf"></a>

$$
r_{12}^{-1} = \underbrace{\text{erfc}(\mu \cdot r_{12}) \cdot r_{12}^{-1} }_{\text{SR} } + \underbrace{\text{erf}(\mu \cdot r_{12}) \cdot r_{12}^{-1} }_{\text{LR} }\qquad \text{(eqn:modelchemistries.dft.hybriddft.rangeseparatedhybrids.erf)}
$$

其中
$\text{erf}(x) = \frac{2}{\sqrt{\pi} } \in t_{0}^{x} \exp(-t^{2}) dt$，$\text{erfc}(x) = 1 - \text{erf}(x)$。注意该划分仅应用于交换贡献；所有其他贡献（哈密顿量的单电子部分、电子-电子库仑相互作用以及 DFT 关联的近似）都不受影响。后来，Handy 及其同事[handy2004CAMB3LYPLC](../../bibliography.md) 将这一拟设（ansatz）推广为：
<a id="eqn:modelchemistries.dft.hybriddft.rangeseparatedhybrids.erfgeneralized"></a>

$$
r_{12}^{-1} = \underbrace{\frac{1 - [ \alpha + \beta \cdot \text{erf}(\mu \cdot r_{12})]}{ r_{12} }}_{\text{SR} } + \underbrace{\frac{\alpha + \beta \cdot \text{erf}(\mu \cdot r_{12}) }{r_{12} }}_{\text{LR} }\qquad \text{(eqn:modelchemistries.dft.hybriddft.rangeseparatedhybrids.erfgeneralized)}
$$

ORCA 中使用的这种划分形式（按照 Handy 及其同事的术语）如 [fig:modelchemistries.dft.hybriddft.rangeseparatedhybrids.ansatz](#fig:modelchemistries.dft.hybriddft.rangeseparatedhybrids.ansatz) 所示。
<a id="fig:modelchemistries.dft.hybriddft.rangeseparatedhybrids.ansatz"></a>
*范围分离拟设（range-separation ansatz）的图形描述。灰色区域对应哈特里-福克交换。$\alpha$ 和 $\beta$ 遵循 Handy 的术语[handy2004CAMB3LYPLC](../../bibliography.md)。*
!!! warning "重要"
    目前，RSH 泛函可用于积分直接（integral-direct）单点能计算、涉及一阶核梯度的计算（即几何优化）、频率计算、TDDFT、TDDFT 核梯度以及 EPR/NMR 计算。
    与[全局杂化泛函](#sec:modelchemistries.dft.globalhybrids)一样，默认使用 [RIJCOSX](../essentialelements/RI.md) 来大幅加速计算。也可以只使用 RIJONX。
可用范围分离杂化泛函的列表见 [tab:modelchemistries.dft.rangeseparatedhybrids](#tab:modelchemistries.dft.rangeseparatedhybrids)
<a id="tab:modelchemistries.dft.rangeseparatedhybrids"></a>
!!! note "可用范围分离杂化泛函列表（List of available range-separated hybrid functionals）。$\mu$ 是范围分离参数（range-separation parameter）。"| 泛函（Functional）                                        | 关键词（Keyword）   | %HFX             | $\mu$ / $\text{bohr}^{-1}$ | % 固定 DFX |
    |:--------------------------------------------------|:---------------|:----------------:|:--------------------------:|:-----------:|
    | **hybrid GGAs**                                   |                |                  |                            |             |
    | $\omega$B97 [headgordon2008wB97wB97X](../../bibliography.md)       | `WB97`         | 0 -- 100         | 0.40                       | ---         |
    | $\omega$B97X [headgordon2008wB97wB97X](../../bibliography.md)      | `WB97X`        | 15.7706 -- 100   | 0.30                       | ---         |
    | $\omega$B97X-V [headgordon2014wB97XV](../../bibliography.md)       | `WB97X-V`      | 16.7 -- 100      | 0.30                       | ---         |
    | $\omega$B97X-D3 [chai2013wB97XD3](../../bibliography.md)           | `WB97X-D3`     | 19.5728 -- 100   | 0.25                       | ---         |
    | $\omega$B97X-D3(BJ) [goerigk2018](../../bibliography.md)           | `WB97X-D3BJ`   | 16.7 -- 100      | 0.30                       | ---         |
    | $\omega$B97X-D4 [najibi2020](../../bibliography.md)                | `WB97X-D4`     | 16.7 -- 100      | 0.30                       | ---         |
    | $\omega$B97X-D4rev[grimme2022wb97x3c](../../bibliography.md)       | `WB97X-D4REV`  | 16.7 -- 100      | 0.30                       | ---         |
    | CAM-B3LYP [handy2004CAMB3LYPLC](../../bibliography.md)             | `CAM-B3LYP`    | 19 -- 65         | 0.33                       | 35%         |
    | LC-BLYP [hirao2004LC_TDDFT](../../bibliography.md)                 | `LC-BLYP`      | 0 -- 100         | 0.33                       | ---         |
    | LC-PBE [hirao2001rangeseparation](../../bibliography.md)           | `LC-PBE`       | 0 -- 100         | 0.47                       | ---         |
    | **hybrid meta-GGAs**                              |                |                  |                            |             |
    | $\omega$B97M-V [headgordon2016wB97MV](../../bibliography.md)       | `WB97M-V`      | 15 -- 100        | 0.30                       | ---         |
    | $\omega$B97M-D3(BJ) [goerigk2018](../../bibliography.md)           | `WB97M-D3BJ`   | 15 -- 100        | 0.30                       | ---         |
    | $\omega$B97M-D4 [najibi2020](../../bibliography.md)                | `WB97M-D4`     | 15 -- 100        | 0.30                       | ---         |
    | $\omega$B97M-D4rev [grimme2022wb97x3c](../../bibliography.md)      | `WB97M-D4REV`  | 15 -- 100        | 0.30                       | ---         |
    | $\omega$r²SCAN [Wittmann2023](../../bibliography.md)               | `WR2SCAN`      | 0 -- 100         | 0.30                       | ---         |
    | **composite**                                     |                |                  |                            |             |
    | $\omega$B97X-3c [grimme2022wb97x3c](../../bibliography.md)         | `WB97X-3C`     | 16.7 -- 100      | 0.30                       | ---         |
<a id="sec:modelchemistries.dft.rangeseparatedhybrids.customization"></a>
#### 范围分离杂化泛函的定制（Customizing Range-Separated Hybrids）
范围分离杂化泛函参数也可以通过 `%method` 块定制。关于基本交换和关联组成部分的定制，请参阅[基本泛函的定制](#sec:modelchemistries.dft.gga.customizexc)章节。基本的杂化相关关键词和相应的 ACM 模型在[杂化 DFT](#sec:modelchemistries.dft.hybriddft) 和[全局杂化泛函的定制](#sec:modelchemistries.dft.globalhybrids.customization)章节中描述。
在此示例中，我们将重建 LC-PBE 泛函：
```orca
! RIJCOSX
# LC-PBE
%method
   Method DFT
   Exchange X_LRCPBE
   Correlation C_PBE
   LDAOpt C_PWLDA
   ACM_A        0.00   # fraction of static Hartree-Fock exchange
   ACM_B        0.00   # fraction of static GGA exchange
   ACM_C        1.00   # fraction of GGA correlation
   ScalLDAC     1.00   # fraction of LDA correlation, must be equal to ScalGGAC 
   RangeSepEXX  true   # activates range-separated exchange
   RangeSepMu   0.47   # range-separation parameter, should be >0
   RangeSepScal 1.00   # fraction of variable HFX, should sum to 1
                       # with ACM-A and ACM-B
end
```
这与前面描述的 `ScalX` 语法等价。
```orca
! RIJCOSX
# LC-PBE
%method
   Method DFT
   Exchange X_LRCPBE
   Correlation C_PBE
   LDAOpt C_PWLDA
   ScalHFX      0.00   # fraction of static Hartree-Fock exchange
   ScalDFX      0.00   # fraction of static GGA exchange
   ScalGGAC     1.00   # fraction of GGA correlation
   ScalLDAC     1.00   # fraction of LDA correlation, must be equal to ScalGGAC 
   RangeSepEXX  true   # activates range-separated exchange
   RangeSepMu   0.47   # range-separation parameter, should be >0
   RangeSepScal 1.00   # fraction of variable HFX, should sum to 1
                       # with ScalHFX and ScalDFX
end
```
!!! warning "警告"
    固定 DFT 交换的比例（`ACM_B` 或 `ScalDFX`）只能对 CAM-B3LYP 和 LC-BLYP 进行更改。相应地，ACM-B 会被 $\omega$B97 系列方法忽略，因为尚未定义相应的与 $\mu$ 无关的交换泛函。虽然从技术上可以选择一个不依赖 $\mu$ 的交换泛函，但这在概念上没有意义。
<a id="tab:modelchemistries.dft.rangeseparatedhybrids.customization.keywords.block"></a>
!!! note "用于修改范围分离杂化泛函的 `%method` 块输入关键词（`%method` block input keywords to modify range-separated hybrid functionals）。"
    | 关键词（Keyword）                  | 选项（Options）           | 描述（Description）                                                    |
    |:--------------------------------|:---------------------|:----------------------------------------------------------------|
    | `RangeSepEXX`                   | `true`               | 激活范围分离交换                                                          |
    | `RangeSepMu`                    | `<real>`             | 控制范围分离参数，应大于 0                                                   |
    | `RangeSepScal`                  | `<real>`             | 控制可变哈特里-福克交换的比例                                                  |
<a id="sec:modelchemistries.dft.doublehybriddft"></a>
## 双杂化 DFT（Double-Hybrid DFT）
除了将 HF 交换混合到给定的密度泛函中之外，Grimme 还提出混入一部分用杂化 DFT 轨道计算的[MP2 关联能](../modelchemistries/MP2.md)[Grimme2006jcp](../../bibliography.md)。这类泛函可称为"双"杂化（"double-"hybrid）泛函。Grimme 的原始表达式为：
<a id="eqn:modelchemistries.dft.doublehybriddft.exc"></a>

$$
E_{\text{XC}} = aE_{\text{X}}^{\text{HF}} +\left({1-a} \right)E_{\text{X}}^{\text{DFT}} +\left({1-c}
\right)E_{\text{C}}^{\text{DFT}} +cE_{\text{C}}^{\text{MP2}}\qquad \text{(eqn:modelchemistries.dft.doublehybriddft.exc)}
$$

Grimme 提出的第一个双杂化泛函是 B2PLYP。[Grimme2006jcp](../../bibliography.md) 该双杂化泛函使用 B88 交换泛函和 LYP 关联泛函。它引入 53% 的哈特里-福克交换（$a = 0.53$），并用 MP2 关联能替换 27% 的 DFT 关联能（$c = 0.27$）。
此后，人们发展出了许多偏离原始思路的 DH-DFT 方法。例如 Grimme 提出了像 PWPB95[goerigk2011chem](../../bibliography.md) 这样使用自旋分量缩放 MP2（spin-component-scaled MP2）的 DH 泛函。
此外，还开发并改进了其组成完全根据数据库经验拟合、不受任何物理约束或限制（如公式 [Eq](#eqn:modelchemistries.dft.doublehybriddft.exc) 中所提出的那样）的泛函，例如 Martin 的 DSD（dispersion corrected, spin-component scaled double-hybrid，色散校正、自旋分量缩放双杂化）泛函[martin2010dsd,martin2011dsd,martin2013dsd](../../bibliography.md)，其中 revDSD-PBEP86-D4[martin2021revdsd](../../bibliography.md) 是最知名的代表之一。XYG$n$ 系列泛函[goddard2009xyg](../../bibliography.md) 或 Head-Gordon 的 $\omega$B97M(2)[Mardirossian2018](../../bibliography.md) 则为 DFT 部分和微扰理论部分采用不同构造的密度，后者还基于[范围分离杂化泛函](#sec:modelchemistries.dft.hybriddft.rangeseparatedhybrids)。
原则上，其他关联方法（如 dRPA 或更高阶 MP 理论）也可以在双杂化框架内使用。不过最常见的方法是采用经典的 [MP2](../modelchemistries/MP2.md) 或其自旋分量缩放变体。[MP2 的 DLPNO 近似](MP2.md#sec:modelchemistries.mp2.dlpno)在 ORCA 中也可用，可用于大幅加速大体系的能量和梯度计算。DLPNO-DH 的精度和效率已由 Bursch、Neese 及其同事进行了广泛研究[bursch2023dlpnodhs](../../bibliography.md)。
几乎所有双杂化泛函的共同点是其哈特里-福克交换比例相对较高，达 50% 甚至更多。
遵循 Grimme 方案的大多数经典双杂化泛函可用于单点能计算、解析梯度（因而也包括几何优化[Neese2007doublehybrid](../../bibliography.md)、弛豫扫描和过渡态搜索）、偶极矩及其他一阶性质、磁学二阶性质（化学位移和 g 张量，MP2 部分不使用冻结芯近似），以及数值极化率和频率计算。
一些双杂化泛函还针对激发态应用进行了优化，它们会使用[双激发校正（Doubles Corrections）](../spectroscopyproperties/tddft.md#sec:spectroscopyproperties.tddft.doubles)来校正[含时 DFT（TD-DFT）](../../../../en/manual/contents/spectroscopyproperties/excitedstates.md#sec:spectroscopyproperties.excitedstates.tddft)框架内的单激发态。其中一些（如 SCS-PBE-QIDH）仅对计算的 CIS(D) 部分使用自旋分量缩放。不过，其中许多最近也已针对基态性质进行了测试。[GS_RSDHDFs](../../bibliography.md)
!!! note "注意"
    ORCA 默认采用 [RIJCOSX](../essentialelements/RI.md) 和 [RI-MP2](../essentialelements/RI.md)。如果不希望这样，可以使用 `!NORI` 关键词全局关闭 RI，或者如果只想关闭 MP2 部分的 RI 近似，可通过 `%mp2` 块：
    ```orca
    %mp2
       RI false
    end
    ```
    事实上，几乎没有任何理由使用常规（conventional）MP2。
!!! note "注意"
    注意，默认情况下不计算 MP2 响应密度（response density），因为其构造会带来显著的额外开销。在这种情况下，只有双杂化能量是正确的。
    与解析一阶导数所得一阶性质相一致的 MP2 响应密度的计算，可以通过 `%mp2` 块中的 `%mp2 density relaxed end` 语句来请求。成本低得多的非弛豫（unrelaxed，期望值形式的）密度可以通过 `%mp2 density unrelaxed end` 来请求。不过，我们不推荐这样做，因为根据我们的经验，弛豫密度的变化相当可观，而非弛豫密度的理论地位远弱于其弛豫对应形式。
<a id="sec:modelchemistries.dft.doublehybriddft.globaldoublehybrids"></a>
### 全局双杂化泛函（Global Double-Hybrid Functionals）
全局双杂化泛函基于相应的[全局杂化泛函](#sec:modelchemistries.dft.globalhybrids)，并采用[哈特里-福克](hartreefock.md#sec:essentialelements.hartreefock)交换和[MP2 关联能](../modelchemistries/MP2.md)的固定混合比例。
当前已实现的全局双杂化泛函列表见 [tab:modelchemistries.dft.doublehybriddft.globaldoublehybrids](#tab:modelchemistries.dft.doublehybriddft.globaldoublehybrids)。
Martin 及其同事的 revDSD-PBEP86-D4[martin2021revdsd](../../bibliography.md) 在大多数热化学应用中已被证明是准确的。
!!! warning "警告"
    对于 DSD/DOD 系列的某些泛函，原作者对同一泛函名称提供了不同的参数。所采用的参数化由泛函和相应关键词的 `(年份)` 后缀标明。另请注意，对于其中一些泛函，在存在不同[色散校正](../modelchemistries/dispersioncorrections.md)时基本参数会发生变化。请仔细检查所用参数是否符合您的预期！
!!! tip "提示"
    对于大多数原生实现的双杂化泛函，您只需在相应的泛函简单输入关键词前添加 `DLPNO-` 前缀即可，例如 `DLPNO-B2PLYP`。
    对于所有其他泛函，可以通过 `%mp2` 块中的 `DLPNO true` 关键词激活 DLPNO 处理。
<a id="tab:modelchemistries.dft.doublehybriddft.globaldoublehybrids"></a>
!!! note "可用全局双杂化泛函列表（List of available global double-hybrid functionals）。`PS` 是反自旋（opposite-spin）缩放参数，`PT` 是同自旋（same-spin）缩放参数。针对激发态优化的泛函仅对 TD-DFT 框架内的 [CIS(D) 双激发校正](../spectroscopyproperties/tddft.md#sec:spectroscopyproperties.tddft.doubles)使用自旋分量缩放。同自旋间接项（CTss）、反自旋间接项（CTos）、同自旋直接项（CUss）和反自旋直接项（CUos）参数见脚注。"

| | **关键词（Keywords）** | `%HFX` | `%DFX` | `%GGAC` | `%MP2C` | `PS` | `PT` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **泛函（Functional）** | 关键词（Keywords） | `%HFX` | `%DFX` | `%GGAC` | `%MP2C` | `PS` | `PT` |
| **DSD-BLYP [martin2010dsd](../../bibliography.md)** | `DSD-BLYP D3BJ` | 69 | 31 | 54 | 100 | 0.46 | 0.37 |
| **DSD-BLYP-NoDisp(2013) [martin2013dsd](../../bibliography.md)** | `DSD-BLYP/2013` | 75 | 25 | 53 | 100 | 0.46 | 0.60 |
| **DSD-BLYP-D3(BJ)(2013) [martin2013dsd](../../bibliography.md)** | `DSD-BLYP/2013 D3BJ` | 71 | 29 | 54 | 100 | 0.47 | 0.40 |
| **DSD-PBEP86 [martin2011dsd](../../bibliography.md)** | `DSD-PBEP86 D3BJ` | 70 | 30 | 43 | 100 | 0.53 | 0.25 |
| **DSD-PBEP86-NoDisp(2013) [martin2013dsd](../../bibliography.md)** | `DSD-PBEP86/2013` | 72 | 28 | 44 | 100 | 0.51 | 0.36 |
| **DSD-PBEP86-D3(BJ)(2013) [martin2013dsd](../../bibliography.md)** | `DSD-PBEP86/2013 D3BJ` | 69 | 31 | 44 | 100 | 0.52 | 0.22 |
| **DSD-PBEB95-NoDisp [martin2013dsd](../../bibliography.md)** | `DSD-PBEB95` | 70 | 30 | 52 | 100 | 0.48 | 0.22 |
| **DSD-PBEB95-D3(BJ) [martin2013dsd](../../bibliography.md)** | `DSD-PBEB95 D3BJ` | 66 | 34 | 55 | 100 | 0.46 | 0.09 |
| **B2PLYP [Grimme2006jcp](../../bibliography.md)** | `B2PLYP` | 53 | 47 | 73 | 27 |  |  |
| **mPW2PLYP [Schwabe2006pccp](../../bibliography.md)** | `mPW2PLYP` | 55 | 45 | 75 | 25 |  |  |
| **B2GP-PLYP [b2gpplyp](../../bibliography.md)** | `B2GP-PLYP` | 65 | 35 | 64 | 36 |  |  |
| **B2K-PLYP [b2kplyp](../../bibliography.md)** | `B2K-PLYP` | 72 | 28 | 58 | 42 |  |  |
| **B2T-PLYP [b2kplyp](../../bibliography.md)** | `B2T-PLYP` | 60 | 40 | 69 | 31 |  |  |
| **B2NC-PLYP [b2ncplyp](../../bibliography.md)** | `B2NC-PLYP` | 81 | 19 | 45 | 55 |  |  |
| **PWPB95 [goerigk2011chem](../../bibliography.md)** | `PWPB95` | 50 | 50 | 73.1 | 26.9 | 1.0 | 0.0 |
| **PBE-QIDH [PBEQIDH](../../bibliography.md)** | `PBE-QIDH` | 69 | 31 | 67 | 33 |  |  |
| **PBE0-DH [PBE0DH](../../bibliography.md)** | `PBE0-DH` | 50 | 50 | 87.5 | 12.5 |  |  |
| **revDSD-PBEP86(2021) [martin2021revdsd](../../bibliography.md)** | `REVDSD-PBEP86/2021` | 69 | 31 | 42.24 | 100 | 0.5935 | 0.0566 |
| **revDSD-PBEP86-D4(2021) [martin2021revdsd](../../bibliography.md)** | `REVDSD-PBEP86-D4/2021` | 69 | 31 | 42.24 | 100 | 0.5935 | 0.0566 |
| **revDOD-PBEP86(2021) [martin2021revdsd](../../bibliography.md)** | `REVDOD-PBEP86/2021` | 69 | 31 | 43.01 | 100 | 0.6131 | 0.0 |
| **revDOD-PBEP86-D4(2021) [martin2021revdsd](../../bibliography.md)** | `REVDOD-PBEP86-D4/2021` | 69 | 31 | 43.01 | 100 | 0.6131 | 0.0 |
| **SOS1-r²SCAN-CIDH [Wittmann2023](../../bibliography.md)** | `R2SCAN-CIDH` | 55 | 45 | 83.33 | 16.67 | 1.333 | 0.0 |
| **SOS1-r²SCAN-QIDH [Wittmann2023](../../bibliography.md)** | `R2SCAN-QIDH` | 69.34 | 30.76 | 66.67 | 33.33 | 1.333 | 0.0 |
| **SOS1-r²SCAN0-2 [Wittmann2023](../../bibliography.md)** | `R2SCAN0-2` | 79.37 | 20.63 | 50 | 50 | 1.333 | 0.0 |
| **SOS1-r²SCAN0-DH [Wittmann2023](../../bibliography.md)** | `R2SCAN0-DH` | 50 | 50 | 87.50 | 12.50 | 1.333 | 0.0 |
| **Pr²SCAN50 [Wittmann2023](../../bibliography.md)** | `PR2SCAN50` | 50 | 50 | 75 | 25 | 1.333 | 0.0 |
| **Pr²SCAN69 [Wittmann2023](../../bibliography.md)** | `PR2SCAN69` | 69.34 | 30.76 | 55.56 | 44.44 | 1.333 | 0.0 |
| **$\kappa$Pr²SCAN50 [Wittmann2023](../../bibliography.md)** | `KPR2SCAN50` | 50 | 50 | 70 | 30 | 1.333 | 0.0 |
| ****excited state opt.**** |  |  |  |  |  |  |  |

| **SCS/SOS-B2PLYP21 [SCSTDDHDFs](../../bibliography.md)** | 无 |
      - `SCS/SOS-B2PLYP21`
      - 53
      - 47
      - 73
      - 27
      - [^a]
      - [^a]

| | **`SCS-PBE-QIDH`** | 69 | 31 | 67 | 33 | [^b] | [^b] |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **SCS-PBE-QIDH [SCSTDDHDFs](../../bibliography.md)** | `SCS-PBE-QIDH` | 69 | 31 | 67 | 33 | [^b] | [^b] |
| **SOS-PBE-QIDH [SCSTDDHDFs](../../bibliography.md)** | `SOS-PBE-QIDH` | 69 | 31 | 67 | 33 | [^c] | [^c] |
| **SCS-B2GP-PLYP21 [SCSTDDHDFs](../../bibliography.md)** | `SCS-B2GP-PLYP21` | 65 | 35 | 64 | 36 | [^d] | [^d] |
| **SOS-B2GP-PLYP21 [SCSTDDHDFs](../../bibliography.md)** | `SOS-B2GP-PLYP21` | 65 | 35 | 64 | 36 | [^e] | [^e] |

[^a]: SCS/SOS-B2PLYP21: CTss: 0.000; CTos: 0.334; CUss: 0.000; CUos: 0.283.
[^b]: SCS-PBE-QIDH: CTss: 0.070; CTos: 0.515; CUss: 0.096; CUos: 0.524.
[^c]: SOS-PBE-QIDH: CTss: 0.000; CTos: 0.547; CUss: 0.000; CUos: 0.573.
[^d]: SCS-B2GP-PLYP21: CTss: 0.018; CTos: 0.475; CUss: 0.000; CUos: 0.468.
[^e]: SOS-B2GP-PLYP21: CTss: 0.000; CTos: 0.489; CUss: 0.000; CUos: 0.484.
<a id="sec:modelchemistries.dft.doublehybriddft.rangeseparateddoublehybrids"></a>
### 范围分离双杂化泛函（Range-Separated Double-Hybrid Functionals）
范围分离双杂化泛函采用可变比例的哈特里-福克交换（与[范围分离杂化泛函](#sec:modelchemistries.dft.hybriddft.rangeseparatedhybrids)非常相似）以及固定比例的 [MP2 关联](../modelchemistries/MP2.md)。可用范围分离双杂化泛函的列表见 [tab:modelchemistries.dft.doublehybriddft.rangeseparateddoublehybrids](#tab:modelchemistries.dft.doublehybriddft.rangeseparateddoublehybrids)。
!!! tip "提示"
    对于大多数原生实现的双杂化泛函，您只需在相应的泛函简单输入关键词前添加 `DLPNO-` 前缀即可，例如 `DLPNO-WPR2SCAN50`。
    对于所有其他泛函，可以通过 `%mp2` 块中的 `DLPNO true` 关键词激活 DLPNO 处理。
<a id="tab:modelchemistries.dft.doublehybriddft.rangeseparateddoublehybrids"></a>
!!! note "可用范围分离双杂化泛函列表（List of available range-separated double-hybrid functionals）。`PS` 是反自旋缩放参数，`PT` 是同自旋缩放参数。$\mu$ 是范围分离参数。针对激发态优化（ES-Opt.）的泛函仅对 TD-DFT 框架内的 [CIS(D) 双激发校正](../spectroscopyproperties/tddft.md#sec:spectroscopyproperties.tddft.doubles)使用自旋分量缩放。同自旋间接项（CTss）、反自旋间接项（CTos）、同自旋直接项（CUss）和反自旋直接项（CUos）参数见脚注。"

| | **关键词（Keywords）** | `%HFX` | $\mu$ / $\text{bohr}^{-1}$ | `%GGAC` | `%MP2C` | `PS` | `PT` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **泛函（Functional）** | 关键词（Keywords） | `%HFX` | $\mu$ / $\text{bohr}^{-1}$ | `%GGAC` | `%MP2C` | `PS` | `PT` |
| **$\omega$B97M(2)[^f] [Mardirossian2018](../../bibliography.md)** | `WB97M(2)` | 62.194 `-` 100 | 0.30 | 100 | 34.096 | `-` | `-` |
| **$\omega$B97X-2(TQZ) [Chai2009](../../bibliography.md)** | `WB97X-2` | 63.6158 `-` 95.1661 | 0.30 | 100 | 100 | 0.447105 | 0.529319 |
| **$\omega$Pr2SCAN50 [Wittmann2023](../../bibliography.md)** | `WPR2SCAN50` | 50 `-` 100 | 0.214013 | 65 | 35 | 1.333 | 0.000 |
| **RSX-QIDH [RSXQIDH](../../bibliography.md)** | `RSX-QIDH` | 69 `-` 100 | 0.27 | 67 | 33 | `-` | `-` |
| **RSX-0DH [RSX0DH](../../bibliography.md)** | `RSX-0DH` | 50 `-` 100 | 0.33 | 87.5 | 12.5 | `-` | `-` |
| **$\omega$B2PLYP [goerigk2019RSDHTDDFT](../../bibliography.md)** | `WB2PLYP` | 53 `-` 100 | 0.30 | 73 | 27 | `-` | `-` |
| **$\omega$B2GP-PLYP [goerigk2019RSDHTDDFT](../../bibliography.md)** | `WB2GP-PLYP` | 65 `-` 100 | 0.27 | 64 | 36 | `-` | `-` |
| **$\omega$B88PP86 [goerigk2019RSDHTDDFT](../../bibliography.md)** | `WB88PP86` | 65 `-` 100 | 0.20 | 58 | 42 | `-` | `-` |
| **$\omega$PBEPP86 [goerigk2019RSDHTDDFT](../../bibliography.md)** | `WPBEPP86` | 70 `-` 100 | 0.18 | 68 | 48 | `-` | `-` |
| ****excited state opt.**** |  |  |  |  |  |  |  |

| **SCS/SOS-$\omega$B2PLYP [SCSTDDHDFs](../../bibliography.md)** | 无 |
      - `SCS/SOS-WB2PLYP`
      - 53 `-` 100
      - 0.30
      - 73
      - 27
      - [^g]
      - [^g]

| | **`SCS-WB2GP-PLYP`** | 65 `-` 100 | 0.27 | 64 | 36 | [^h] | [^h] |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **SCS-$\omega$B2GP-PLYP [SCSTDDHDFs](../../bibliography.md)** | `SCS-WB2GP-PLYP` | 65 `-` 100 | 0.27 | 64 | 36 | [^h] | [^h] |
| **SOS-$\omega$B2GP-PLYP [SCSTDDHDFs](../../bibliography.md)** | `SOS-WB2GP-PLYP` | 65 `-` 100 | 0.27 | 64 | 36 | [^i] | [^i] |
| **SCS-RSX-QIDH [SCSTDDHDFs](../../bibliography.md)** | `SCS-RSX-QIDH` | 69 `-` 100 | 0.27 | 67 | 33 | [^j] | [^j] |
| **SOS-RSX-QIDH [SCSTDDHDFs](../../bibliography.md)** | `SOS-RSX-QIDH` | 69 `-` 100 | 0.27 | 67 | 33 | [^k] | [^k] |
| **SCS-$\omega$B88PP86 [SCSTDDHDFs](../../bibliography.md)** | `SCS-WB88PP86` | 65 `-` 100 | 0.20 | 58 | 42 | [^l] | [^l] |
| **SOS-$\omega$B88PP86 [SCSTDDHDFs](../../bibliography.md)** | `SOS-WB88PP86` | 65 `-` 100 | 0.20 | 58 | 42 | [^m] | [^m] |
| **SCS-$\omega$PBEPP86 [SCSTDDHDFs](../../bibliography.md)** | `SCS-WPBEPP86` | 70 `-` 100 | 0.18 | 68 | 48 | [^n] | [^n] |
| **SOS-$\omega$PBEPP86 [SCSTDDHDFs](../../bibliography.md)** | `SOS-WPBEPP86` | 70 `-` 100 | 0.18 | 68 | 48 | [^o] | [^o] |

[^f]: Must be used with ωB97M-V orbitals (cf. [rangeseparateddoublehybrids.wb97m2](#sec:modelchemistries.dft.doublehybriddft.rangeseparateddoublehybrids.wb97m2)).
[^g]: SCS/SOS-$\omega$B2PLYP: CTss: 0.000; CTos: 0.433; CUss: 0.000; CUos: 0.460.
[^h]: SCS-$\omega$B2GP-PLYP: CTss: 0.000; CTos: 0.571; CUss: 0.135; CUos: 0.558.
[^i]: SOS-$\omega$B2GP-PLYP: CTss: 0.000; CTos: 0.570; CUss: 0.000; CUos: 0.610.
[^j]: SCS-RSX-QIDH: CTss: 0.174; CTos: 0.541; CUss: 0.586; CUos: 0.424.
[^k]: SOS-RSX-QIDH: CTss: 0.000; CTos: 0.632; CUss: 0.000; CUos: 0.714.
[^l]: SCS-$\omega$B88PP86: CTss: 0.000; CTos: 0.557; CUss: 0.092; CUos: 0.545.
[^m]: SOS-$\omega$B88PP86: CTss: 0.000; CTos: 0.559; CUss: 0.000; CUos: 0.599.
[^n]: SCS-$\omega$PBEPP86: CTss: 0.000; CTos: 0.610; CUss: 0.297; CUos: 0.540.
[^o]: SOS-$\omega$PBEPP86: CTss: 0.000; CTos: 0.613; CUss: 0.000; CUos: 0.669.
<a id="sec:modelchemistries.dft.doublehybriddft.rangeseparateddoublehybrids.wb97m2"></a>
#### $\omega$B97M(2)
某些双杂化泛函（如 $\omega$B97M(2)[Mardirossian2018](../../bibliography.md)）必须应用于用另一种泛函收敛的轨道。这可以通过使用 `MORead` 和 `MaxIter=1` 的两步计算来完成。注意，由于轨道不是自洽获得的，用这种方式只能计算单点能——即不能得到密度、梯度或性质！
这类泛函的使用可以通过[Compound 脚本语言](../workflowsautomatization/compound.md)自动化。
一个用于 $\omega$B97M(2) 单点能计算的示例 compound 脚本如下所示：
```mol
title: structure 1
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
2
structure (0 1)
H           0.0          0.0          0.0
F           0.0          0.0          0.9
--- input ---
*xyz 0 1
  H 0.0 0.0 0.0
  F 0.0 0.0 0.9
*
# ------------------------------------------------------------------------------------
# Energy calculation with the wB97M(2) double-hybrid functional, as defined in
# N. Mardirossian, M. Head-Gordon, J. Chem. Phys. 2018, 148, 241736.
# The final energy is calculated non-variatonally using wB97M-V orbitals.
# Note that FrozenCore is on default - one can turn it off using kw2 = "NoFrozenCore".
# Author: Georgi L. Stoychev
# ------------------------------------------------------------------------------------
# Optional variables:
Variable molecule = "water.xyz";
Variable charge   = 0;
Variable mult     = 1;
Variable NLOpt = "SCNL";        # Consistent with Q-Chem. "NL" likely very similar. Only matters for Step 1.
Variable Basis = "def2-TZVP";   # Should be TZ or higher for reliable results
Variable AuxC  = "def2-TZVP/C"; # RI-MP2 is used by default. Must be compatible with the Basis
Variable AuxJ  = "def2/J";      # RIJCOSX is used by default
Variable RIMP2 = True;          # Set to false to turn off RI-MP2
Variable Grid  = "defGrid2";    # Should be OK.
Variable kw1   = "";            # Additional simple input keywords for step 1
Variable kw2   = "";            # Additional simple input keywords for step 2
# Output variables
Variable EwB97MV, EwB97M2;      # Will hold the final energies
# Step 1: wB97M-V calculation to obtain the orbitals
NewStep
  ! wB97M-V &{NLOpt} &{Grid} &{kw1}
  *xyzfile &{charge} &{mult} &{molecule}
  %basis
    Basis "&{Basis}"
    AuxJ  "&{AuxJ}"
  end
StepEnd
EwB97MV.ReadProperty(propertyName="DFT_Total_En");
# Step 2: single iteration with the wB97M(2) functional + MP2 correlation to get the final energy
ReadMOs(1);
NewStep
  ! wB97M(2) &{NLOpt} &{Grid} &{kw2} NoIter CalcGuessEnergy
  %basis
    Basis "&{Basis}"
    AuxC  "&{AuxC}"
    AuxJ  "&{AuxJ}"
  end
  %scf
    IgnoreConv 1
  end
  %mp2 RI &{RIMP2} end
Step_End
EwB97M2.ReadProperty(propertyName="MP2_Total_Energy");
Print("");
Print("================================================================================\n");
Print(" wB97M-V Energy:  %20.10lf\n",EwB97MV);
Print(" wB97M(2) Energy: %20.10lf\n",EwB97M2);
End
```
<a id="sec:modelchemistries.dft.doublehybrids.customization"></a>
### 双杂化泛函的定制（Customization of Double-Hybrids）
由于双杂化泛函使用[全局杂化泛函](#sec:modelchemistries.dft.rangeseparatedhybrids.customization)或[范围分离杂化泛函](#sec:modelchemistries.dft.rangeseparatedhybrids.customization)的可定制组成部分，它们也可以用类似的方式构造和定制。
双杂化的 MP2 关联处理可以通过 `%method` 块中的 `DoMP2 true` 和 `ScalMP2C` 关键词控制。
此外，MP2 处理还可以通过 `%mp2` 块进一步定制。例如，自旋分量缩放的范围分离双杂化泛函 $\omega$Pr²SCAN50 可以按如下方式构造：
```orca
! RIJCOSX def2-TZVP/C NOTRAH
# wPr2SCAN50
%method
   Method       DFT
   DoMP2        true       # activates MP2 correlation part
   Exchange     X_WR2SCAN
   Correlation  C_R2SCAN
   LDAOpt       C_PWLDA
   ScalHFX      0.50       # fraction of static Hartree-Fock exchange
   ScalDFX      0.00       # fraction of static GGA exchange
   ScalGGAC     0.65       # fraction of GGA correlation
   ScalLDAC     0.65       # fraction of LDA correlation, must be equal to ScalGGAC 
   ScalMP2C     0.35       # fraction of MP2 correlation
   RangeSepEXX  true       # activates range-separated exchange
   RangeSepMu   0.214013   # range-separation parameter, should be >0
   RangeSepScal 0.50       # fraction of variable HFX, should sum to 1 with ScalHFX and ScalDFX
end
%mp2
   DoSCS        true       # activates spin-component-scaling
   RI           true       # activate RI-MP2
   PS           1.333      # opposite-spin-scaling parameter
   PT           0.000      # same-spin-scaling parameter
end
```
许多其他与 MP2 相关的选项（如 DLPNO 处理和正则化（regularization））可在手册的 [MP2](../modelchemistries/MP2.md) 章节中找到。
<a id="tab:modelchemistries.dft.doublehybriddft.customization.keywords.block.method"></a>
!!! note "用于定制双杂化泛函的最重要 `%method` 块输入关键词（Most important `%method` block input keywords to customize double-hybrid functionals）。"
    | 关键词（Keyword）                  | 选项（Options）           | 描述（Description）                                                    |
    |:--------------------------------|:---------------------|:----------------------------------------------------------------|
    | `DoMP2`                         | `true`               | 激活 MP2 关联部分                                                        |
    | `ScalMP2C`                      | `<real>`             | 控制 GGA 交换的比例                                                       |
<a id="tab:modelchemistries.dft.doublehybriddft.customization.keywords.block.mp2"></a>
!!! note "用于定制双杂化泛函的最重要 `%mp2` 块输入关键词（Most important `%mp2` block input keywords to customize double-hybrid functionals）。更多细节参见 [MP2 章节](../modelchemistries/MP2.md)。"
    | 关键词（Keyword）                  | 选项（Options）           | 描述（Description）                                                    |
    |:--------------------------------|:---------------------|:----------------------------------------------------------------|
    | `DoSCS`                         | `true`               | 激活 MP2 部分的自旋分量缩放（spin-component-scaling）                           |
    | `PS`                            | `<real>`             | 控制反自旋缩放参数                                                        |
    | `PT`                            | `<real>`             | 控制同自旋缩放参数                                                        |
    | `RI`                            | `true`               | 激活 RI-MP2                                                         |
    | `DLPNO`                         | `true`               | 激活 DLPNO-MP2                                                      |
<a id="sec:modelchemistries.dft.libxc"></a>
## LibXC 泛函库（LibXC Functional Library）
可以在 ORCA 框架内使用 LibXC 提供的泛函 [^libxc]。ORCA 所使用的 LibXC 版本会在输出开头打印出来。当 LibXC 用作您计算的一部分时，应引用 LibXC 的参考文献。参考文献见 [libxc](../../bibliography.md)。
通过 LibXC 接口可用的泛函完整列表始终可以通过在命令行输入以下命令来查看：
```orca
orca -libxcfunctionals
```
泛函列表的形式如下：
```orca
Functionals available via LibXC:
  No.:     ID / Keyword                    - Name
    0:     18 / lda_c_1d_csc               - Casula, Sorella & Senatore
    1:     26 / lda_c_1d_loos              - P-F Loos correlation LDA
    2:     15 / lda_c_2d_amgb              - AMGB (for 2D systems)
    3:     16 / lda_c_2d_prm               - PRM (for 2D systems)
    4:    552 / lda_c_br78                 - Brual & Rothstein 78
   ...
```
列表按泛函的"层级"（LDA、GGA、meta-GGA 等）分组，然后按其建模的能量部分（关联、交换、交换-关联）分组。
关联泛函的名称中带有 `'_c_'`，交换泛函带有 `'_x_'`，合并的交换-关联泛函带有 `'_xc_'`。特定泛函的附加信息可以通过以下命令获取：
```orca
orca -libxcinfo [functional name]
```
其中泛函名称是上述列表中的关键词。
在 ORCA 输入中指定 LibXC 泛函遵循标准格式：
```orca
%method 
  Method     DFT
  Functional hyb_gga_xc_b3lyp
end
```
或者在分别指定交换和关联的情况下：
```orca
%method 
  Method      DFT
  Exchange    mgga_x_m06_l
  Correlation mgga_c_m06_l
end
```
自 ORCA 5.0 起，CAM 型范围分离泛函通过 LibXC 接口得到支持。包含非局域（VV10）关联的泛函（参见 [nl.theory](dispersioncorrections.md#sec:modelchemistries.dispersioncorrections.nl.theory)）同样如此。VV10 部分由 ORCA 内部计算。其他非局域泛函（如 BEEF-vdW）不受支持。依赖动能密度（kinetic energy density）$\tau$ 的 meta-GGA 泛函受支持，但依赖密度拉普拉斯（Laplacian of the density）$\nabla^2\rho$ 的则不受支持。
双杂化泛函可以用 LibXC 组成部分按照前述定制章节构造，但只能使用分开的交换和关联组成部分。因此可以使用 `exchange=gga_x_pbe` 和 `correlation=gga_c_pbe`，但 `functional=hyb_gga_xc_pbeh` **不能**用于双杂化表述。请注意，LibXC 计算的交换和关联贡献只是简单地分别被 `ScalDFX` 和 `ScalGGAC` 缩放，并不会单独缩放 LDA 组分或更改其他内部参数！
<a id="sec:modelchemistries.dft.libxc.screeningthresholds"></a>
### 筛选阈值（Screening Thresholds）
当密度小于某个阈值时，LibXC 会跳过泛函的求值，转而将所有输出量设为零，以避免下溢和/或上溢（under- and/or overflows）。不同泛函的默认阈值由 LibXC 开发者设定，但有时可能过低。我们没有进行大量测试，但允许用户设置该阈值。类似地，为避免除零，对 $\zeta$ 和 $\tau$ 的最小值也存在阈值。默认值与泛函无关，可以使用以下关键词更改。
```orca
%method 
  LibXCDensityThreshold 1e-12    # seems to be reasonable
  LibXCZetaThreshold    2e-16    # default value in LibXC
  LibXCTauThreshold     1e-20    # default value in LibXC
end
```
<a id="sec:modelchemistries.dft.libxc.modifyingparameters"></a>
### 修改 LibXC 泛函参数（Modifying LibXC Functional Parameters）
从 ORCA 5.1 起，可以修改 LibXC 接口所提供的泛函"外部参数"（external parameters）。
可用参数及其默认值可以在输出中查看，也可以用上述 `orca -libxcinfo` 命令查看。使用此接口时请谨慎，如果使用的是已发表的泛函重新参数化，请确保能够重现原始文献的结果。该语法要求使用 `ExtParamX`、`ExtParamC` 或 `ExtParamXC` 关键词之一（取决于修改的是哪个泛函），后跟引号中的参数名称，最后是新的值。例如，以下是 PWPB95 双杂化泛函的一个输入，其中用简单输入关键词设置大多数参数（如 MP2 缩放因子），只修改 mPW91 和 B95 LibXC 泛函的交换和关联参数：
```mol
title: structure 2
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
2
structure (0 1)
H             0            0            0
F             0            0          0.9
--- input ---
! Opt PWPB95 def2-SVP def2-SVP/C
%method
  Exchange    gga_x_mpw91
  Correlation mgga_c_bc95
  ExtParamX   "_bt"     0.00444
  ExtParamX   "_alpha" 19.823391
  ExtParamX   "_expo"   3.7868
  ExtParamC   "_css"    0.03241
  ExtParamC   "_copp"   0.00250
end
*xyz 0 1
  H 0 0 0
  F 0 0 0.9
*
```
请注意，LibXC 中的变量定义可能与 ORCA 内部或原始文献中使用的定义不同，原因可能是各种常数因子等。如有疑问，请查阅 LibXC 文档或源代码仓库——我们只是提供该接口的访问途径。
<a id="sec:modelchemistries.dft.libxc.simpleinput"></a>
### LibXC 泛函的简单输入（Simple Input of LibXC Functionals）
某些 LibXC 泛函可以通过简单输入关键词 `!LibXC(Keyword)` 访问，例如 `!LibXC(TPSS)`。这些关键词与 ORCA 中原生实现的关键词一致。使用这种语法时，[DFT-D 色散校正](../modelchemistries/dispersioncorrections.md)的参数也会自动设置（如果已实现）。表 [tab:modelchemistries.dft.libxc.simpleinput](#tab:modelchemistries.dft.libxc.simpleinput) 列出了可用的泛函及其 LibXC 名称。
<a id="tab:modelchemistries.dft.libxc.simpleinput"></a>
!!! note "可通过简单输入 `!LibXC(Keyword)` 访问的 LibXC 泛函（LibXC functionals available via the simple input `!LibXC(Keyword)`）"
    | 关键词（Keyword）               | LibXC 组成部分（LibXC components）        | 备注（Notes）                       |
    |:----------------------------|:------------------------------------|:-------------------------------|
    | **LDA functionals**         |                                     |                                |
    | `PWLDA`                     | lda_x + gga_c\_pw                   |                                |
    | `VWN5`                      | lda_x + gga_c\_vwn                  |                                |
    | **GGAs**                    |                                     |                                |
    | `B97-D`                     | gga_xc_b97_d                        | 使用 D2                          |
    | `B97-D3`                    | gga_xc_b97_d                        | 使用 D3(0)                       |
    | `B97-D4`                    | gga_xc_b97_d                        | 使用 D4                          |
    | `BLYP`                      | gga_x\_b88 + gga_c\_lyp             |                                |
    | `BPBE`                      | gga_x\_b88 + gga_c\_pbe             |                                |
    | `BPW91`                     | gga_x\_b88 + gga_c\_pw91            |                                |
    | `BVWN`                      | gga_x\_b88 + lda_c\_vwn             |                                |
    | `GLYP`                      | gga_x\_g96 + gga_c\_lyp             |                                |
    | `KT2`                       | gga_xc_kt2                          |                                |
    | `KT3`                       | gga_xc_kt3                          |                                |
    | `MPWLYP`                    | gga_x\_mpw91 + gga_c\_lyp           |                                |
    | `MPWPW`                     | gga_x\_mpw91 + gga_c\_pw91          |                                |
    | `OPBE`                      | gga_x\_optx + gga_c\_pbe            |                                |
    | `OLYP`                      | gga_x\_optx + gga_c\_lyp            |                                |
    | `RPW86PBE`                  | gga_x\_rpw86 + gga_c\_pbe           |                                |
    | `PW86PBE`                   | gga_x\_pw86 + gga_c\_pbe            |                                |
    | `PW91`                      | gga_x\_pw91 + gga_c\_pw91           |                                |
    | `PBE`                       | gga_x\_pbe + gga_c\_pbe             |                                |
    | `RPBE`                      | gga_x\_rpbe + gga_c\_pbe            |                                |
    | `REVPBE`                    | gga_x\_pbe + gga_c\_pbe             | $\kappa$=1.245                 |
    | `XLYP`                      | gga\_xc\_xlyp                       |                                |
    **meta-GGAs**                 |                                     |                                |
    | `B97M-V`                    | mgga_xc_b97m_v                      | 使用 VV10                        |
    | `B97M-D3BJ`                 | mgga_xc_b97m_v                      | 使用 D3(BJ)                      |
    | `B97M-D4`                   | mgga_xc_b97m_v                      | 使用 D4                          |
    | `M06L`                      | mgga_x\_m06_l + mgga_c\_m06_l       |                                |
    | `MN15L`                     | mgga_x\_mn15_l + mgga_c\_mn15_l     |                                |
    | `MTASK-LDA`                 | mgga_x\_mtask + lda_c\_pw_mod       |                                |
    | `MTASK-SCAN`                | mgga_x\_mtask + mgga_c\_scan        |                                |
    | `REVTM`                     | mgga_x\_revtm + mgga_c\_revtm       |                                |
    | `R2SCAN`                    | mgga_x\_r2scan + mgga_c\_r2scan     |                                |
    | `RSCAN`                     | mgga_x\_rscan + mgga_c\_rscan       |                                |
    | `SCAN`                      | mgga_x\_scan + mgga_c\_scan         |                                |
    | `TASK-CCALDA`               | mgga_x\_task + mgga_c\_ccalda       |                                |
    | `TASK-CC`                   | mgga_x\_task + mgga_c\_cc           |                                |
    | `TASK-LDA`                  | mgga_x\_task + lda_c\_pw_mod        |                                |
    | `TASK-SCAN`                 | mgga_x\_task + mgga_c\_scan         |                                |
    | `TM`                        | mgga_x\_tm + mgga_c\_tm             |                                |
    | `TPSS`                      | mgga_x\_tpss + mgga_c\_tpss         |                                |
    | **Hybrid LDA functionals**  |                                     |                                |
    | `HFLDA`                     | lda_x + lda_c\_pw                   |                                |
    | **Hybrid GGAs**             |                                     |                                |
    | `BHANDHLYP`                 | hyb_gga_xc_bhandhlyp                |                                |
    | `B1LYP`                     | hyb_gga_xc_b1lyp                    |                                |
    | `B1PW91`                    | hyb_gga_xc_b1pw91                   |                                |
    | `B1PW`                      | gga_x\_b88,gga_c\_pw91              | 自定义混合（Custom mixing）             |
    | `B1PBE`                     | gga\_x\_b88 + gga\_c\_pbe           | 自定义混合                          |
    | `B3PW91`                    | hyb\_gga\_xc\_b3pw91                | 自定义混合                          |
    | `B3LYP`                     | hyb_gga_xc_b3lyp5                   |                                |
    | `B3LYP/G`                   | hyb_gga_xc_b3lyp                    |                                |
    | `B3LYPS`                    | hyb_gga_xc_b3lyps                   | B3LYP*, 15% HFX                |
    | `BLYP35`                    | hyb_gga_xc_blyp35                   |                                |
    | `B97`                       | hyb_gga_xc_b97                      |                                |
    | `CAM-B3LYP`                 | hyb\_gga\_xc\_cam\_b3lyp            | 自定义混合                          |
    | `CASE21`                    | hyb_gga_xc_case21                   |                                |
    | `G1LYP`                     | gga\_x\_g96 + gga\_c\_lyp           | 自定义混合                          |
    | `HSE03`                     | hyb_gga_xc_hse03                    |                                |
    | `HSE12`                     | hyb_gga_xc_hse12                    |                                |
    | `HSE12S`                    | hyb_gga_xc_hse12s                   |                                |
    | `HSESOL`                    | hyb_gga_xc_hse_sol                  |                                |
    | `KMLYP`                     | hyb_gga_xc_kmlyp                    |                                |
    | `LB07`                      | hyb_gga_xc_lb07                     |                                |
    | `LC-BLYP`                   | hyb\_gga\_xc\_lc\_blyp              | 自定义混合                          |
    | `MPW1LYP`                   | hyb\_gga\_xc\_mpw1lyp               | 自定义混合                          |
    | `MPW1PW`                    | hyb\_gga\_xc\_mpw1pw                | 自定义混合                          |
    | `PBE0`                      | hyb_gga_xc_pbeh                     |                                |
    | `PBE38`                     | hyb_gga_xc_pbe38                    |                                |
    | `PBE50`                     | hyb_gga_xc_pbe50                    |                                |
    | `PW91_0`                    | gga\_x\_pw91 + gga\_c\_pw91         | 自定义混合                          |
    | `PW1PW`                     | gga\_x\_pw91 + gga\_c\_pw91         | 自定义混合                          |
    | `REVPBE0`                   | gga_x\_pbe,gga_c\_pbe               | $\kappa$=1.245                 |
    | `REVPBE38`                  | gga_x\_pbe,gga_c\_pbe               | 37.5% HFX, $\kappa$=1.245      |
    | `WHPBE0`                    | hyb_gga_xc_whpbe0                   |                                |
    | `WB97`                      | hyb_gga_xc_wb97                     |                                |
    | `WB97X`                     | hyb_gga_xc_wb97x                    |                                |
    | `WB97X-D3`                  | hyb_gga_xc_wb97x_d3                 | 使用 D3(0)                       |
    | `WB97X-V`                   | hyb_gga_xc_wb97x_v                  | 使用 VV10                        |
    | `WB97X-D3BJ`                | hyb_gga_xc_wb97x_v                  | 使用 D3(BJ)                      |
    | `WB97X-D4`                  | hyb_gga_xc_wb97x_v                  | 使用 D4                          |
    | `WB97X-D4REV`               | hyb_gga_xc_wb97x_v                  | 使用 D4 及修订参数                       |
    | **Hybrid meta-GGAs**        |                                     |                                |
    | `GAS22`                     | hyb_mgga_xc_gas22                   |                                |
    | `M05`                       | hyb_mgga_x\_m05 + mgga_c\_m05       |                                |
    | `M052X`                     | hyb_mgga_x\_m05_2x + mgga_c\_m05_2x |                                |
    | `M06`                       | hyb_mgga_x\_m06 + mgga_c\_m06       |                                |
    | `M062X`                     | hyb_mgga_x\_m06_2x + mgga_c\_m06_2x |                                |
    | `M06SX`                     | hyb_mgga_x\_m06_sx + mgga_c\_m06_sx |                                |
    | `MN15`                      | hyb_mgga_x\_mn15 + mgga_c\_mn15     |                                |
    | `LC-TMLYP`                  | hyb_mgga_xc_lc_tmlyp                |                                |
    | `PW6B95`                    | hyb_mgga_xc_pw6b95                  |                                |
    | `R2SCANH`                   | hyb_mgga_xc_r2scanh                 |                                |
    | `R2SCAN0`                   | hyb_mgga_xc_r2scan0                 |                                |
    | `R2SCAN38`                  | hyb_mgga_xc_r2scanh                 | 37.5% HFX                      |
    | `R2SCAN50`                  | hyb_mgga_xc_r2scan50                |                                |
    | `SCAN0`                     | hyb_mgga_x\_scan0 + mgga_c\_scan    |                                |
    | `TPSS0`                     | hyb_mgga_xc_tpss0                   |                                |
    | `TPSSH`                     | hyb_mgga_xc_tpssh                   |                                |
    | `WB97M-V`                   | hyb_mgga_xc_wb97m_v                 | 使用 VV10                        |
    | `WB97M-D3BJ`                | hyb_mgga_xc_wb97m_v                 | 使用 D3(BJ)                      |
    | `WB97M-D4`                  | hyb_mgga_xc_wb97m_v                 | 使用 D4                          |
    | `WB97M-D4REV`               | hyb_mgga_xc_wb97m_v                 | 使用 D4 及修订参数                       |
    | **Double-hybrids**          |                                     |                                |
    | `B2PLYP`                    | gga\_x\_b88 + gga\_c\_lyp           | 自定义混合                          |
    | `B2GP-PLYP`                 | gga\_x\_b88 + gga\_c\_lyp           | 自定义混合                          |
    | `B2T-PLYP`                  | gga\_x\_b88 + gga\_c\_lyp           | 自定义混合                          |
    | `B2K-PLYP`                  | gga\_x\_b88 + gga\_c\_lyp           | 自定义混合                          |
    | `B2NC-PLYP`                 | gga\_x\_b88 + gga\_c\_lyp           | 自定义混合                          |
    | `DSD-PBEB95-D3`             | gga_x\_pbe + mgga_c\_bc95           | 自定义混合，使用 D3(BJ)                   |
    | `DSD-PBEB95-D4`             | gga_x\_pbe + mgga_c\_bc95           | 自定义混合，使用 D4                      |
    | `MPW2-PLYP`                 | gga\_x\_mpw91 + gga\_c\_lyp         | 自定义混合                          |
    | `PWPB95`                    | gga_x\_mpw91 + mgga_c\_bc95         | 自定义混合及 `ExtParam` 参数              |
    | `PBE0-DH`                   | gga\_x\_pbe + gga\_c\_pbe           | 自定义混合                          |
    | `PBE0-2`                    | gga\_x\_pbe + gga\_c\_pbe           | 自定义混合                          |
    | `PBE-QIDH`                  | gga\_x\_pbe + gga\_c\_pbe           | 自定义混合                          |
    | `PR2SCAN50`                 | mgga\_x\_r2scan + mgga_c\_r2scan   | 自定义混合                          |
    | `PR2SCAN69`                 | mgga\_x\_r2scan + mgga_c\_r2scan   | 自定义混合                          |
    | `SOS1-R2SCAN0-DH`           | mgga\_x\_r2scan + mgga_c\_r2scan   | 自定义混合                          |
    | `SOS1-R2SCAN-CIDH`          | mgga\_x\_r2scan + mgga_c\_r2scan   | 自定义混合                          |
    | `SOS1-R2SCAN-QIDH`          | mgga\_x\_r2scan + mgga_c\_r2scan   | 自定义混合                          |
    | `SOS1-R2SCAN0-2`            | mgga\_x\_r2scan + mgga_c\_r2scan   | 自定义混合                          |
[^libxc]: https://libxc.gitlab.io
