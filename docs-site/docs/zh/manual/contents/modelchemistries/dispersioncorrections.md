

<a id="sec:modelchemistries.dispersioncorrections"></a>
# 色散校正（Dispersion Corrections）

常规密度泛函理论（以及哈特里-福克理论）的一个主要缺陷是缺乏对包括伦敦色散（London dispersion）在内的长程关联效应（long-range correlation effects）的描述。伦敦色散代表范德华相互作用（van-der-Waals interaction）中的吸引分量，尽管它是一种相当弱的相互作用，但对许多情形而言其正确描述可能至关重要。对于非共价相互作用（non-covalent interactions）和延展分子（extended molecules）尤其如此。不过，已有若干成熟的色散校正方法可在很大程度上弥补这一缺陷。在 ORCA 中提供了多种选项，包括 Grimme 的 D3 [grimme2010chem, grimme2011comp](../../bibliography.md) 和 D4 [caldeweyher2017, caldeweyher2019](../../bibliography.md) 校正，以及 VV10 的非局域变体（NL，[vydrov2010chem, hujo2011chem](../../bibliography.md)）。

!!! note "关于色散校正的一些说明（Some notes on dispersion corrections）"

    -   色散校正不仅影响非共价配合物（non-covalent complexes），也影响构象能量（conformational energies）和结构——它们在很大程度上受分子内色散（intramolecular dispersion）影响。因此，几乎总是推荐、甚至必须包含色散校正（除少数不能、不应或无需使用的情形外，见下文）。

    -   使用小基组（如双 zeta 基组）的 DFT 计算，即便不加色散校正，也常常给出吸引性的势能面（potential energy surfaces）。然而，这是由基组重叠误差（basis set superposition error, BSSE）造成的，而 BSSE 带来的相互作用能往往与色散导致的真实相互作用能并不吻合（因为二者来源完全不同）。因此，尽管不加色散校正的 DFT 双 zeta 计算看起来可能给出定性正确的结果，偶尔甚至比加色散校正的双 zeta 计算结果更好（因为后者往往会高估总吸引作用），仍强烈建议通过降低 BSSE 并开启色散校正来"因正确的理由得到正确的答案"（get the right answer for the right reason）。BSSE 可以通过多种手段校正，例如：(1) 使用更大的基组；(2) 使用 counterpoise 校正（[essentialelements.counterpoise](../essentialelements/counterpoise.md#sec:essentialelements.counterpoise)）；或 (3) 使用几何反位校正（geometrical counterpoise correction，章节 [counterpoise.gcp](../essentialelements/counterpoise.md#sec:essentialelements.counterpoise.gcp)）。其中，(3) 几乎不增加额外开销（包括解析梯度贡献），特别适合大分子的几何优化。否则，(1)（或其与 (2) 的组合）由于精度更高，可能更为合适。

    -   含有 VV10 型非局域色散的泛函（一般是以 "-V" 结尾的泛函）不需要（也不能与）色散校正一起使用。同样的情况也适用于后 HF（post-HF）方法和多参考方法，如 MP2、CCSD(T)、CASSCF 和 NEVPT2。不过，可以在 HF 之上添加色散校正。

    -   某些泛函，尤其是 Minnesota 系列泛函（例如 M06-2X），能描述中程色散（medium-range dispersion）但缺失长程色散。它们对中小体系给出合理的色散能，但对大体系可能略微低估色散能。在这种情况下，未经校正的泛函本身已涵盖了色散的主体部分，色散校正远不如 B3LYP 那类情形重要，总体上应视为有益但并非强制。

<a id="sec:modelchemistries.dispersioncorrections.dftd.theory"></a>
## Grimme 的 DFT-D3 与 DFT-D4

DFT-D3 和 DFT-D4 是逐原子对（atom-pairwise，逐原子三元组（atom-triplewise））的色散校正，可以添加到 KS-DFT 能量和梯度中[grimme2010chem](../../bibliography.md)。在 ORCA 中，D3 适用于直至 Pu（Z = 94）的所有元素，D4 适用于直至 Lr（Z = 103）的所有元素。

<a id="eqn:modelchemistries.dispersioncorrections.dftd.theory.edftd"></a>

$$
E_{\text{DFT-D}} = E_{\text{KS-DFT}} + E_{\text{disp}}\qquad \text{(eqn:modelchemistries.dispersioncorrections.dftd.theory.edftd)}
$$

$E_{\text{disp}}$ 是色散能的两体（two-body）和三体（three-body）贡献之和，$E_{\text{disp} } =E^{(2) }+E^{(3) }$。其中最重要的是两体项，其长程形式为：

<a id="eqn:modelchemistries.dispersioncorrections.dftd.theory.twobody"></a>

$$
E_{\text{disp} } = - \sum_{A < B} \sum_{n=6,8} s_{n} \frac{C_{n}^{AB} }{r_{AB}^{n} }\qquad \text{(eqn:modelchemistries.dispersioncorrections.dftd.theory.twobody)}
$$

其中$C_{n}^{AB}$ 表示原子对 *AB* 的平均（各向同性）$n$ 阶色散系数，$r_{AB}$ 是其核间距。$s_{n}$ 是与泛函相关的缩放因子（见下文）。在一般情形下，必须使用适当的阻尼函数（damping function）。较新的 D4 模型基本采用类似的理论，但进一步引入了原子参考极化率（atomic reference polarizabilities）对原子分电荷的依赖关系。

<a id="sec:modelchemistries.dispersioncorrections.dftd.theory.damping"></a>
### 阻尼函数（Damping Functions）

为避免小$r_{AB}$ 时的近奇异性（near-singularities），需要在短距离处对色散贡献进行阻尼处理。一种可行的方式是使用 Becke 和 Johnson 提出的有理阻尼（rational damping）[becke2005chem,johnson2005chem,johnson2006chem](../../bibliography.md)：

<a id="eqn:modelchemistries.dispersioncorrections.dftd.theory.bj"></a>

$$
E^{(2) }= - \sum_{A < B} \sum_{n=6,8} s_{n} \frac{C_{n}^{AB} }{r_{AB}^{n} +f(R_{0}^{AB} )^{n} }\qquad \text{(eqn:modelchemistries.dispersioncorrections.dftd.theory.bj)}
$$

其中[johnson2006chem](../../bibliography.md)

<a id="eqn:modelchemistries.dispersioncorrections.dftd.theory.r0ab"></a>

$$
R_{0}^{AB} =\sqrt{ \frac{C_{8}^{AB} }{C_{6}^{AB} } }\qquad \text{(eqn:modelchemistries.dispersioncorrections.dftd.theory.r0ab)}
$$

且

<a id="eqn:modelchemistries.dispersioncorrections.dftd.theory.fbj"></a>

$$
f(R_{0}^{AB} )=a_{1} R_{0}^{AB} +a_{2} .\qquad \text{(eqn:modelchemistries.dispersioncorrections.dftd.theory.fbj)}
$$

将短程区的色散贡献阻尼至零（如参考文献 [grimme2010chem](../../bibliography.md) 中那样）也是可行的：

<a id="eqn:modelchemistries.dispersioncorrections.dftd.theory.zero"></a>

$$
E^{(2) }= - \sum_{A < B}  \sum_{n=6,8} s_{n} \frac{C_{n}^{AB} }{r_{AB}^{n} }f_{d,n} (r_{AB} )\qquad \text{(eqn:modelchemistries.dispersioncorrections.dftd.theory.zero)}
$$

其中

<a id="eqn:modelchemistries.dispersioncorrections.dftd.theory.fzero"></a>

$$
f_{d,n} =\frac{1}{1+6(\frac{r_{AB} }{s_{r,n} R_{0}^{AB} })^{-\alpha_{n} } }\qquad \text{(eqn:modelchemistries.dispersioncorrections.dftd.theory.fzero)}
$$

注意，与该阻尼一起使用的$R_{0}^{AB}$ 来自参考文献 [grimme2010chem](../../bibliography.md)。关于所支持的阻尼函数的更多信息，参见参考文献 [grimme2011comp](../../bibliography.md)。

<a id="sec:modelchemistries.dispersioncorrections.dftd.theory.atm"></a>
### 三体项（Three-body term）

可以按下式计算三体色散贡献：

<a id="eqn:modelchemistries.dispersioncorrections.dftd.theory.abc"></a>

$$
E^{(3) }= - \sum_{A < B < C} \frac{C_{9}^{ABC} (3\cos{\theta_{a} } \cos{\theta_{b} } \cos{\theta_{c} } +1) }{(r_{AB} r_{BC} r_{CA} )^{3} } f_{d,(3) }(\overline{r}_{ABC})\qquad \text{(eqn:modelchemistries.dispersioncorrections.dftd.theory.abc)}
$$

其中$\theta_{a}$、$\theta_{b}$ 和$\theta_{c}$ 是由$r_{AB}$、$r_{BC}$ 和$r_{CA}$ 构成的三角形的内角。$C_{9}$ 系数近似为

<a id="eqn:modelchemistries.dispersioncorrections.dftd.theory.c9abc"></a>

$$
C_{9}^{ABC} \approx -\sqrt{ C_{6}^{AB} C_{6}^{AC} C_{6}^{BC} }\qquad \text{(eqn:modelchemistries.dispersioncorrections.dftd.theory.c9abc)}
$$

三体贡献对中等大小分子的影响很小，并按公式 [Eq](#eqn:modelchemistries.dispersioncorrections.dftd.theory.abc) 进行阻尼。阻尼函数$f_{d,(3) }(\overline{r}_{ABC})$ 与公式 [Eq](#eqn:modelchemistries.dispersioncorrections.dftd.theory.fzero) 中所示的类似，其中$\overline{r}_{ABC}$ 是$r_{AB}$、$r_{BC}$ 和$r_{CA}$ 的几何平均值。它可以与$E^{(2) }$ 项的两种变体一起使用，不过三体项本身始终使用零阻尼（zero damping）方案计算。事实证明，加入三体校正对超分子体系（supramolecular systems）的热化学给出了相当准确的结果[grimme2012chemeurj](../../bibliography.md)。注意，D4 中默认包含三体项。

<a id="sec:modelchemistries.dispersioncorrections.dftd.basicusage"></a>
### 基本用法（Basic Usage）

D3 校正可通过 `!D3` 关键词调用，它将自动使用默认的 Becke-Johnson 阻尼，因而等同于 `!D3BJ`。零阻尼方案可用 `!D3ZERO`。注意，一般推荐使用 Becke-Johnson 方案。

```orca
!PBE D3
```

三体项可通过关键词 `!ABC` 调用。

```orca
!PBE D3 ABC
```

!!! note "注意"
    注意，并非所有方法都针对所有阻尼选项进行了参数化。例如，哈特里-福克（HF）只针对 BJ 阻尼进行了参数化，而 M06 只针对零阻尼进行了参数化。

较新且普遍推荐的 D4 校正可用 `!D4` 关键词。注意，D4 默认使用 Becke-Johnson 阻尼和三体项。

```orca
!PBE D4
```

D4 校正也可以在输入的 `%method` 块中定义：

```orca
! PBE def2-TZVP

%method
  DFTDOpt     5     # 5 = D4; 4 = D3(BJ)
end
```

<a id="sec:modelchemistries.dispersioncorrections.dftd.customparams"></a>
### 自定义参数（Custom parameters）

如果某个泛函的参数已知但尚未在 ORCA 中实现，可以通过 `%method` 块手动指定。

!!! warning "警告"
    使用自定义参数风险自负，一般不推荐。D3 的部分可用参数列表可以在 [Grimme 小组的网站](https://www.chemie.uni-bonn.de/grimme/de/software/dft-d3)上找到。

!!! warning "GGA 和杂化泛函（hybrid functionals）应仅与"
$s_{6}=1.0$ 一起使用，以确保渐近行为正确。双杂化泛函（double-hybrid functionals）已经包含了部分色散相互作用，因此应与$s_{6} < 1.0$ 一起使用。

对于采用 Becke-Johnson 阻尼的 D3，可以调整$s_6$、$a_1$、$s_8$ 和$a_2$ 参数：

```orca
!B2PLYP D3

%method
  D3S6 0.6400
  D3S8 0.9147
  D3A1 0.3065
  D3A2 5.0570
end
```

对于 D4，三体项的$s_9$ 参数也可以调整。

```orca
!B2PLYP D4

%method
  D4S6 0.6400
  D4S8 1.1689
  D4A1 0.4415
  D4A2 4.7311
  D4S9 1.0000
end
```

对于零阻尼的 D3 变体，可以调整$s_6$、$rs_6$、$s_8$ 和$\alpha_{6}$ 参数。

```orca
!BLYP D3ZERO

%method
  D3S6     1.000
  D3RS6    1.094
  D3S8     1.682
  D3alpha6 14
end
```

对于某些泛函，还有专门针对 def2-TZVPP 三 zeta 基组优化的特殊参数。该选项仅在零阻尼下可用，可通过关键词 `!D3ZERO D3TZ` 调用。参考文献 [grimme2010chem](../../bibliography.md) 补充材料中的初步结果表明，其结果仅比使用默认参数的四 zeta 基组略差。在未来的大规模计算中使用该选项前应谨慎测试。

<a id="sec:modelchemistries.dispersioncorrections.dftd.example1"></a>
### 示例（Example）

在第一个示例中，使用 DFT-D4 色散校正。

```mol
title: structure 1
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
3
structure (0 1)
C      0.000000     0.000000     0.000000
O      0.000000     0.000000     1.400000
O      0.000000     0.000000    -1.400000
--- input ---
!PBE def2-TZVP D4

* xyz 0 1
  C     0.000000     0.000000     0.000000
  O     0.000000     0.000000     1.400000
  O     0.000000     0.000000    -1.400000
*
```

ORCA 输出中 D4 色散校正的部分如下所示：

```orca
-------------------------------------------------------------------------------
                          DFT DISPERSION CORRECTION                            
                                                                                
                                DFTD4 V3.4.0                                   
-------------------------------------------------------------------------------
The PBE functional is recognized
Active option DFTDOPT                   ...         5   

-------------------------   ----------------
Dispersion correction           -0.000936618
-------------------------   ----------------

-------------------------   --------------------
FINAL SINGLE POINT ENERGY      -188.360452990031
-------------------------   --------------------

```

总色散能$E_{\text{disp} }$ 以 `Dispersion correction` 给出，并自动包含在最终单点能中。如上所述，各参数可以手动调整。

```mol
title: structure 2
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
3
structure (0 1)
C      0.000000     0.000000     0.000000
O      0.000000     0.000000     1.400000
O      0.000000     0.000000    -1.400000
--- input ---
!PBE def2-TZVP D4

%method
  D4S6 1.0
  D4A1 0.4289
  D4S8 0.7875
  D4A2 4.4407
  D4S9 0.9000
end

* xyz 0 1
  C     0.000000     0.000000     0.000000
  O     0.000000     0.000000     1.400000
  O     0.000000     0.000000    -1.400000
*
```

这会产生与上面相同的输出，但额外带有提示已找到用户输入参数的消息：

```orca
A user input s6-coefficient scaling factor has been recognized
A user input a1-coefficient scaling factor has been recognized
A user input s8-coefficient scaling factor has been recognized
A user input a2-coefficient scaling factor has been recognized
A user input s9-coefficient scaling factor has been recognized
```

<a id="sec:modelchemistries.dispersioncorrections.dftd.keywords"></a>
### 关键词（Keywords）

<a id="tab:modelchemistries.dispersioncorrections.dftd.keywords.simple"></a>
!!! note "DFT-D 校正的简单输入关键词（Simple input keywords for the DFT-D corrections）。"
    | 关键词（Keyword）                  | 描述（Description）                                 |
    |:--------------------------------|:-------------------------------------------------|
    | `D2`                            | 激活 D2 校正                                       |
    | `D3`                            | 激活带 BJ 阻尼的 D3 校正（D3(BJ)）                     |
    | `D3BJ`                          | 激活带 BJ 阻尼的 D3 校正（D3(BJ)）                     |
    | `D3ZERO`                        | 激活带零阻尼的 D3 校正（D3(0)）                         |
    | `D30`                           | 激活带零阻尼的 D3 校正（D3(0)），等同于 `D3ZERO`            |
    | `D3TZ`                          | 激活特殊的三 zeta D3 参数化（仅与 `D3ZERO` 一起使用）        |
    | `D4`                            | 激活 D4 校正（含 BJ 和 ATM）                         |
    | `ABC`                           | 激活三体项                                          |
    | `ATM`                           | 激活三体项，等同于 `ABC`                               |
    | `NOVDW`                         | 关闭 DFT-D 色散校正                                  |

<a id="tab:modelchemistries.dispersioncorrections.dftd.keywords.block"></a>
!!! note "DFT-D 校正的 `%method` 块输入关键词（`%method` block input keywords for the DFT-D corrections）。"
    | 关键词（Keyword）                  | 选项（Options）        | 描述（Description）                                |
    |:--------------------------------|:------------------|:-------------------------------------------------|
    | `DFTDOPT`                       | `1`               | 激活原始 D 校正[GrimmeVDW04](../../bibliography.md)（已弃用）            |
    |                                 | `2`               | 激活 D2 校正（已弃用）                                 |
    |                                 | `3`               | 激活 D3ZERO 校正                                   |
    |                                 | `4`               | 激活 D3BJ 校正                                     |
    |                                 | `5`               | 激活 D4 校正                                       |
    | `D3S6`                          | `<real>`          | 控制 D3 的$s_6$ 参数                              || `D3S8`                          | `<real>`          | 控制 D3 的$s_8$ 参数                              |
    | `D3A1`                          | `<real>`          | 控制 D3 的$a_1$ 参数                              || `D3A2`                          | `<real>`          | 控制 D3 的$a_2$ 参数                              |
    | `D3RS6`                         | `<real>`          | 控制零阻尼的$rs_6$ 参数                              || `D3alpha6`                      | `<real>`          | 控制零阻尼的$\alpha_{6}$ 参数                        |
    | `D4S6`                          | `<real>`          | 控制 D4 的$s_6$ 参数                              || `D4S8`                          | `<real>`          | 控制 D4 的$s_8$ 参数                              |
    | `D4A1`                          | `<real>`          | 控制 D4 的$a_1$ 参数                              || `D4A2`                          | `<real>`          | 控制 D4 的$a_2$ 参数                              |
    | `D4S9`                          | `<real>`          | 控制 D4 中 ABC 项的$s_9$ 参数                       |
    | `DFTDScaleC6`                   | `<real>`          | 定义 C6 缩放系数                                    |

<a id="sec:modelchemistries.dispersioncorrections.dftd.params"></a>
### 可用参数（Available Parameters）

<a id="tab:modelchemistries.dispersioncorrections.dftd.params.d4"></a>
!!! note "各种泛函所用的 DFT-D4（`!D4`）参数（DFT-D4 (`!D4`) parameters used for various functionals）。"
    | 泛函（Functional）    |$s_{6}$         |$s_{8}$         |$a_{1}$         |$a_{2}$         |$s_{9}$         |
    |:------------------|:---------------:|:---------------:|:---------------:|:---------------:|:---------------:|
    |	HF	|	1.0000	|	1.61679827	|	0.44959224	|	3.35743605	|	1.0000	|
    |	BLYP	|	1.0000	|	2.34076671	|	0.44488865	|	4.09330090	|	1.0000	|
    |	BPBE	|	1.0000	|	3.64405246	|	0.52905620	|	4.11311891	|	1.0000	|
    |	BP86	|	1.0000	|	3.35497927	|	0.43645861	|	4.92406854	|	1.0000	|
    |	BPW91	|	1.0000	|	3.24571506	|	0.50050454	|	4.12346483	|	1.0000	|
    |	GLYP	|	1.0000	|	4.23798924	|	0.38426465	|	4.38412863	|	1.0000	|
    |	LB94	|	1.0000	|	2.59538499	|	0.42088944	|	3.28193223	|	1.0000	|
    |	mPWLYP	|	1.0000	|	1.25842942	|	0.25773894	|	5.02319542	|	1.0000	|
    |	mPWPW	|	1.0000	|	1.82596836	|	0.34526745	|	4.84620734	|	1.0000	|
    |	OLYP	|	1.0000	|	2.74836820	|	0.60184498	|	2.53292167	|	1.0000	|
    |	OPBE	|	1.0000	|	3.06917417	|	0.68267534	|	2.22849018	|	1.0000	|
    |	PBE	|	1.0000	|	0.95948085	|	0.38574991	|	4.80688534	|	1.0000	|
    |	RPBE	|	1.0000	|	1.31183787	|	0.46169493	|	3.15711757	|	1.0000	|
    |	REVPBE	|	1.0000	|	1.74676530	|	0.53634900	|	3.07261485	|	1.0000	|
    |	PW86PBE	|	1.0000	|	1.21362856	|	0.40510366	|	4.66737724	|	1.0000	|
    |	RPW86PBE	|	1.0000	|	1.12624034	|	0.38151218	|	4.75480472	|	1.0000	|
    |	PW91	|	1.0000	|	0.77283111	|	0.39581542	|	4.93405761	|	1.0000	|
    |	PW91P86	|	1.0000	|	0.32801227	|	0.35874687	|	6.05861168	|	1.0000	|
    |	XLYP	|	1.0000	|	1.62972054	|	0.11268673	|	5.40786417	|	1.0000	|
    |	B97BECKE	|	1.0000	|	0.87854260	|	0.29319126	|	4.51647719	|	1.0000	|
    |	TPSS	|	1.0000	|	1.76596355	|	0.42822303	|	4.54257102	|	1.0000	|
    |	revTPSS	|	1.0000	|	1.53089454	|	0.44880597	|	4.64042317	|	1.0000	|
    |	SCAN	|	1.0000	|	1.46126056	|	0.62930855	|	6.31284039	|	1.0000	|
    |	B1LYP	|	1.0000	|	1.98553711	|	0.39309040	|	4.55465145	|	1.0000	|
    |	B3LYP	|	1.0000	|	2.02929367	|	0.40868035	|	4.53807137	|	1.0000	|
    |	BHANDHLYP	|	1.0000	|	1.65281646	|	0.27263660	|	5.48634586	|	1.0000	|
    |	B1P	|	1.0000	|	3.36115015	|	0.48665293	|	5.05219572	|	1.0000	|
    |	B3P86	|	1.0000	|	3.08822155	|	0.47324238	|	4.98682134	|	1.0000	|
    |	B1PW91	|	1.0000	|	3.02227550	|	0.47396846	|	4.49845309	|	1.0000	|
    |	B3PW91	|	1.0000	|	2.88364295	|	0.46990860	|	4.51641422	|	1.0000	|
    |	O3LYP	|	1.0000	|	1.75762508	|	0.10348980	|	6.16233282	|	1.0000	|
    |	REVPBE0	|	1.0000	|	1.57185414	|	0.38705966	|	4.11028876	|	1.0000	|
    |	REVPBE38	|	1.0000	|	1.66597472	|	0.39476833	|	4.39026628	|	1.0000	|
    |	PBE0	|	1.0000	|	1.20065498	|	0.40085597	|	5.02928789	|	1.0000	|
    |	PWP1	|	1.0000	|	0.60492565	|	0.46855837	|	5.76921413	|	1.0000	|
    |	PW1PW	|	1.0000	|	0.96850170	|	0.42427511	|	5.02060636	|	1.0000	|
    |	mPW1PW	|	1.0000	|	1.80841716	|	0.42961819	|	4.68892341	|	1.0000	|
    |	mPW1LYP	|	1.0000	|	1.15591153	|	0.25603493	|	5.32083895	|	1.0000	|
    |	PW6B95	|	1.0000	|	-0.31926054	|	0.04142919	|	5.84655608	|	1.0000	|
    |	TPSSh	|	1.0000	|	1.85897750	|	0.44286966	|	4.60230534	|	1.0000	|
    |	TPSS0	|	1.0000	|	1.62438102	|	0.40329022	|	4.80537871	|	1.0000	|
    |	X3LYP	|	1.0000	|	1.54701429	|	0.20318443	|	5.61852648	|	1.0000	|
    |	M06L	|	1.0000	|	0.59493760	|	0.71422359	|	6.35314182	|	1.0000	|
    |	M06	|	1.0000	|	0.16366729	|	0.53456413	|	6.06192174	|	1.0000	|
    |	wB97	|	1.0000	|	6.55792598	|	0.76666802	|	8.36027334	|	1.0000	|
    |	wB97X	|	1.0000	|	-0.07519516	|	0.45094893	|	6.78425255	|	1.0000	|
    |	B97M-D4	|	1.0000	|	0.66330000	|	0.42880000	|	3.99350000	|	1.0000	|
    |	CAM-B3LYP	|	1.0000	|	1.66041301	|	0.40267156	|	5.17432195	|	1.0000	|
    |	LC-BLYP	|	1.0000	|	1.60344180	|	0.45769839	|	7.86924893	|	1.0000	|
    |	B2PLYP	|	0.6400	|	1.16888646	|	0.44154604	|	4.73114642	|	1.0000	|
    |	B2GP-PLYP	|	0.5600	|	0.94633372	|	0.42907301	|	5.18802602	|	1.0000	|
    |	mPW2PLYP	|	0.7500	|	0.45788846	|	0.42997704	|	5.07650682	|	1.0000	|
    |	PWPB95	|	0.8200	|	-0.34639127	|	0.41080636	|	3.83878274	|	1.0000	|
    |	B97-D	|	1.0000	|	1.69460052	|	0.28904684	|	4.13407323	|	1.0000	|
    |	RSCAN	|	1.0000	|	0.87728975	|	0.49116966	|	5.75859346	|	1.0000	|
    |	r2SCAN	|	1.0000	|	0.60187490	|	0.51559235	|	5.77342911	|	1.0000	|
    |	r2SCANh	|	1.0000	|	0.83240000	|	0.49440000	|	5.90190000	|	1.0000	|
    |	r2SCAN0	|	1.0000	|	0.89920000	|	0.47780000	|	5.87790000	|	1.0000	|
    |	r2SCAN50	|	1.0000	|	1.04710000	|	0.45740000	|	5.89690000	|	1.0000	|
    |	wB97X-D4rev	|	1.0000	|	0.44850000	|	0.33060000	|	4.27900000	|	1.0000	|
    |	wB97M-D4rev	|	1.0000	|	0.84200000	|	0.35900000	|	4.66800000	|	1.0000	|
    |	wR2SCAN	|	1.0000	|	1.00000000	|	0.38340000	|	5.78890000	|	1.0000	|
    |	r2SCAN0-DH	|	0.9424	|	0.38560000	|	0.42710000	|	5.85650000	|	1.0000	|
    |	r2SCAN-CIDH	|	0.8666	|	0.53360000	|	0.41710000	|	5.91250000	|	1.0000	|
    |	r2SCAN-QIDH	|	0.7867	|	0.29550000	|	0.40010000	|	5.83000000	|	1.0000	|
    |	r2SCAN0-2	|	0.7386	|	0.00000000	|	0.40300000	|	5.51420000	|	1.0000	|
    |	Pr2SCAN50	|	0.7964	|	0.34210000	|	0.46630000	|	5.79160000	|	1.0000	|
    |	kPr2SCAN50	|	0.8402	|	0.12120000	|	0.43820000	|	5.82320000	|	1.0000	|
    |	wPr2SCAN50	|	0.8143	|	0.38420000	|	0.41350000	|	5.87730000	|	1.0000	|
    |	Pr2SCAN69	|	0.7167	|	0.00000000	|	0.46440000	|	5.25630000	|	1.0000	|
    |	revDSD-PBEP86/2021	|	0.5917	|	0.00000000	|	0.37100000	|	4.20140000	|	1.0000	|
    |	revDOD-PBEP86/2021	|	0.6158	|	0.00000000	|	0.34400000	|	4.24270000	|	1.0000	|
    |	LRC-PBE	|	1.0000	|	1.17000000	|	0.37800000	|	4.81600000	|	1.0000	|

<a id="tab:modelchemistries.dispersioncorrections.dftd.params.d3bj"></a>
!!! note "各种泛函所用的 DFT-D3(BJ)（`!D3BJ`）参数（DFT-D3(BJ) (`!D3BJ`) parameters used for various functionals）。"
    | 泛函（Functional）    |$s_{6}$         |$s_{8}$         |$a_{1}$         |$a_{2}$         |$s_{9}$         |
    |:------------------|:---------------:|:---------------:|:---------------:|:---------------:|:---------------:|
    |	HF	|	1.0000	|	0.91710000	|	0.33850000	|	2.88300000	|	1.0000	|
    |	BP86	|	1.0000	|	3.28220000	|	0.39460000	|	4.85160000	|	1.0000	|
    |	BLYP	|	1.0000	|	2.69960000	|	0.42980000	|	4.23590000	|	1.0000	|
    |	REVPBE	|	1.0000	|	2.35500000	|	0.52380000	|	3.50160000	|	1.0000	|
    |	B97-D	|	1.0000	|	2.26090000	|	0.55450000	|	3.22970000	|	1.0000	|
    |	PBE	|	1.0000	|	0.78750000	|	0.42890000	|	4.44070000	|	1.0000	|
    |	RPBE	|	1.0000	|	0.83180000	|	0.18200000	|	4.00940000	|	1.0000	|
    |	RPW86PBE	|	1.0000	|	1.38450000	|	0.46130000	|	4.50620000	|	1.0000	|
    |	B3LYP	|	1.0000	|	1.98890000	|	0.39810000	|	4.42110000	|	1.0000	|
    |	BHANDHLYP	|	1.0000	|	1.03540000	|	0.27930000	|	4.96150000	|	1.0000	|
    |	TPSS	|	1.0000	|	1.94350000	|	0.45350000	|	4.47520000	|	1.0000	|
    |	TPSS0	|	1.0000	|	1.25760000	|	0.37680000	|	4.58650000	|	1.0000	|
    |	PBE0	|	1.0000	|	1.21770000	|	0.41450000	|	4.85930000	|	1.0000	|
    |	REVPBE38	|	1.0000	|	1.47600000	|	0.43090000	|	3.94460000	|	1.0000	|
    |	PW6B95	|	1.0000	|	0.72570000	|	0.20760000	|	6.37500000	|	1.0000	|
    |	B2PLYP	|	0.6400	|	0.91470000	|	0.30650000	|	5.05700000	|	1.0000	|
    |	mPWLYP	|	1.0000	|	2.00770000	|	0.48310000	|	4.53230000	|	1.0000	|
    |	OLYP	|	1.0000	|	2.62050000	|	0.52990000	|	2.80650000	|	1.0000	|
    |	BPBE	|	1.0000	|	4.07280000	|	0.45670000	|	4.39080000	|	1.0000	|
    |	OPBE	|	1.0000	|	3.38160000	|	0.55120000	|	2.94440000	|	1.0000	|
    |	B3PW91	|	1.0000	|	2.85240000	|	0.43120000	|	4.46930000	|	1.0000	|
    |	REVPBE0	|	1.0000	|	1.75880000	|	0.46790000	|	3.76190000	|	1.0000	|
    |	TPSSh	|	1.0000	|	2.23820000	|	0.45290000	|	4.65500000	|	1.0000	|
    |	CAM-B3LYP	|	1.0000	|	2.06740000	|	0.37080000	|	5.47430000	|	1.0000	|
    |	B2GP-PLYP	|	0.5600	|	0.25970000	|	0.00000000	|	6.33320000	|	1.0000	|
    |	PWPB95	|	0.8200	|	0.29040000	|	0.00000000	|	7.31410000	|	1.0000	|
    |	SCAN	|	1.0000	|	0.00000000	|	0.53800000	|	5.42000000	|	1.0000	|
    |	RSCAN	|	1.0000	|	1.08860000	|	0.47020000	|	5.73410000	|	1.0000	|
    |	R2SCAN	|	1.0000	|	0.78980000	|	0.49480000	|	5.73080000	|	1.0000	|
    |	R2SCANh	|	1.0000	|	1.12360000	|	0.47090000	|	5.91570000	|	1.0000	|
    |	R2SCAN0	|	1.0000	|	1.18460000	|	0.45340000	|	5.89720000	|	1.0000	|
    |	R2SCAN50	|	1.0000	|	1.32940000	|	0.43110000	|	5.92400000	|	1.0000	|
    |	WR2SCAN	|	1.0000	|	1.00000000	|	0.38340000	|	5.78890000	|	1.0000	|
    |	r2SCAN0-DH	|	0.9424	|	0.38560000	|	0.42710000	|	5.85650000	|	1.0000	|
    |	r2SCAN-CIDH	|	0.8666	|	0.53360000	|	0.41710000	|	5.91250000	|	1.0000	|
    |	r2SCAN-QIDH	|	0.7867	|	0.29550000	|	0.40010000	|	5.83000000	|	1.0000	|
    |	r2SCAN0-2	|	0.7386	|	0.00000000	|	0.40300000	|	5.51420000	|	1.0000	|
    |	Pr2SCAN50	|	0.7964	|	0.34210000	|	0.46630000	|	5.79160000	|	1.0000	|
    |	kPr2SCAN50	|	0.8402	|	0.12120000	|	0.43820000	|	5.82320000	|	1.0000	|
    |	wPr2SCAN50	|	0.8143	|	0.38420000	|	0.41350000	|	5.87730000	|	1.0000	|
    |	Pr2SCAN69	|	0.7167	|	0.00000000	|	0.46440000	|	5.25630000	|	1.0000	|
    |	revDSD-PBEP86/2021	|	0.5917	|	0.00000000	|	0.37100000	|	4.20140000	|	1.0000	|
    |	revDOD-PBEP86/2021	|	0.6158	|	0.00000000	|	0.34400000	|	4.24270000	|	1.0000	|
    |	DSD-BLYP	|	0.5000	|	0.21300000	|	0.00000000	|	6.05200000	|	1.0000	|
    |	DSD-BLYP/2013	|	0.5700	|	0.00000000	|	0.00000000	|	5.40000000	|	1.0000	|
    |	DSD-PBEB95	|	0.6100	|	0.00000000	|	0.00000000	|	6.20000000	|	1.0000	|
    |	DSD-PBEP86	|	0.4180	|	0.00000000	|	0.00000000	|	5.65000000	|	1.0000	|
    |	DSD-PBEP86/2013	|	0.4800	|	0.00000000	|	0.00000000	|	5.60000000	|	1.0000	|
    |	B97M-D3BJ	|	1.0000	|	0.13840000	|	-0.07800000	|	5.59460000	|	1.0000	|
    |	wB97X-D3BJ	|	1.0000	|	0.26410000	|	0.00000000	|	5.49590000	|	1.0000	|
    |	wB97M-D3BJ	|	1.0000	|	0.39080000	|	0.56600000	|	3.12800000	|	1.0000	|
    |	wB97X-2	|	0.5470	|	0.00000000	|	3.52000000	|	7.79500000	|	1.0000	|
    |	PBE0DH	|	0.8800	|	1.08900000	|	0.00000000	|	6.38500000	|	1.0000	|
    |	PBE02	|	0.5400	|	0.51500000	|	0.00000000	|	8.34500000	|	1.0000	|
    |	PBE-QIDH	|	0.6100	|	0.56600000	|	0.11400000	|	7.53800000	|	1.0000	|

<a id="tab:modelchemistries.dispersioncorrections.dftd.params.d3zero"></a>
!!! note "各种泛函所用的 DFT-D3(0)（`!D3ZERO`）参数（DFT-D3(0) (`!D3ZERO`) parameters used for various functionals）。"
    | 泛函（Functional）    |$s_{6}$         |$rs_{6}$         |$s_{8}$         |$\alpha_{6}$         |
    |:------------------|:---------------:|:---------------:|:---------------:|:---------------:|
    |	HF	|	1.0000	|	1.1580	|	1.7460	|	14	|
    |	BLYP	|	1.0000	|	1.0940	|	1.6820	|	14	|
    |	BP86	|	1.0000	|	1.1390	|	1.6830	|	14	|
    |	B97-D	|	1.0000	|	0.8920	|	0.9090	|	14	|
    |	REVPBE	|	1.0000	|	0.9230	|	1.0100	|	14	|
    |	PBE	|	1.0000	|	1.2170	|	0.7220	|	14	|
    |	RPBE	|	1.0000	|	0.8720	|	0.5140	|	14	|
    |	TPSS	|	1.0000	|	1.1660	|	1.1050	|	14	|
    |	B3LYP	|	1.0000	|	1.2610	|	1.7030	|	14	|
    |	PBE0	|	1.0000	|	1.2870	|	0.9280	|	14	|
    |	PW6B95	|	1.0000	|	1.5230	|	0.8620	|	14	|
    |	TPSS0	|	1.0000	|	1.2520	|	1.2420	|	14	|
    |	B2PLYP	|	0.6400	|	1.4270	|	1.0220	|	14	|
    |	B2GP-PLYP	|	0.5600	|	1.5860	|	0.7600	|	14	|
    |	PWPB95	|	0.8200	|	1.5570	|	0.7050	|	14	|
    |	mPWLYP	|	1.0000	|	1.2390	|	1.0980	|	14	|
    |	BPBE	|	1.0000	|	1.0870	|	2.0330	|	14	|
    |	BHANDHLYP	|	1.0000	|	1.3700	|	1.4420	|	14	|
    |	TPSSh	|	1.0000	|	1.2230	|	1.2190	|	14	|
    |	REVPBE0	|	1.0000	|	0.9490	|	0.7920	|	14	|
    |	REVPBE38	|	1.0000	|	1.0210	|	0.8620	|	14	|
    |	RPW86PBE	|	1.0000	|	1.2240	|	0.9010	|	14	|
    |	B3PW91	|	1.0000	|	1.1760	|	1.7750	|	14	|
    |	M06L	|	1.0000	|	1.5810	|	0.0000	|	14	|
    |	M06	|	1.0000	|	1.3250	|	0.0000	|	14	|
    |	M062X	|	1.0000	|	1.6190	|	0.0000	|	14	|
    |	wB97X-D3	|	1.0000	|	1.2810	|	1.0000	|	14	|
    |	CAM-B3LYP	|	1.0000	|	1.3780	|	1.2170	|	14	|
    |	SCAN	|	1.0000	|	1.3240	|	0.0000	|	14	|
    |	wB97X-2	|	0.5470	|	4.7330	|	-0.1090	|	14	|
    |	PBE0DH	|	0.8800	|	1.1280	|	0.0000	|	14	|
    |	PBE02	|	0.5400	|	1.2430	|	-0.2280	|	14	|
    |	PBE-QIDH	|	0.4000	|	1.1140	|	0.0540	|	14	|

<a id="sec:modelchemistries.dispersioncorrections.nl.theory"></a>
## 非局域色散校正（Non-Local Dispersion Correction, VV10）：DFT-NL

校正伦敦色散的另一条途径是范德华密度泛函（van der Waals Density Functional, vdW-DF），由 Langreth 和 Lundquist 开创[lee2010phys](../../bibliography.md)。这类方法仅使用电子密度来包含此类色散/关联效应，并可自洽地使用，从而不仅校正能量，也校正分子轨道。Vydrov 和 Van Voorhis 的 vdW 关联泛函 VV10[vydrov2010chem](../../bibliography.md) 目前看来是通用于精确电子结构方法最有希望的候选者。

我们用 DFT-NL 这一术语指代任意密度泛函与 VV10 泛函的非局域部分（其优化参数$b$ 见下文定义）的组合。这些方法的表现已在参考文献 [hujo2011chem](../../bibliography.md) 中使用 GMTKN30[goerigk2010chem,goerigk2011chem,goerigk2011phys](../../bibliography.md) 数据库和 S66 集[resac2011chem](../../bibliography.md) 进行了评估。弱氢键（weak hydrogen bonds）的表现则在参考文献 [hujo2011phys](../../bibliography.md) 中进行了评估。

DFT-NL 与 DFT-D3/D4 的表现非常相似，但对于金属体系或当基本电子结构发生显著变化时（例如氧化或电离），NL 更可取。作为一个较近的例子，Janes 和 Iron 表明，对于 wB97X-V 这类泛函，当涉及金属时，包含 VV10 关联可得到非常高质量的反应能垒（reaction barriers）[iron_evaluating_2019](../../bibliography.md)。

VV10 型泛函的总交换-关联（exchange-correlation, XC）能量定义于公式 [Eq](#eqn:modelchemistries.dispersioncorrections.dftnl.theory.exc-dftnl)。它由标准交换（X）部分和关联（C）部分，以及非局域（NL）项组成——后者涵盖（主要是）长程色散能：

<a id="eqn:modelchemistries.dispersioncorrections.dftnl.theory.exc-dftnl"></a>

$$
E_{\text{XC} }^{\text{DFT-NL} } = E_{\text{X} }^{\text{(hybrid)GGA} } +E_{\text{C} }^{\text{GGA} }
+E_{\text{C-NL} }^{\text{VV10} }\qquad \text{(eqn:modelchemistries.dispersioncorrections.dftnl.theory.exc-dftnl)}
$$

NL 项由以下双重积分给出：

<a id="eqn:modelchemistries.dispersioncorrections.dftnl.theory.ec-vv10"></a>

$$
E_{\text{C-NL} }^{\text{VV10} }  = \in t dr\rho (r)\left[{ \beta
+\frac{1}{2}\mathop \in t\nolimits dr'\rho ( { r'}
) \varphi (r,r') } \right]\qquad \text{(eqn:modelchemistries.dispersioncorrections.dftnl.theory.ec-vv10)}
$$

其中$\rho$ 是总电子密度，核函数$\varphi (r,r')$ 和$\beta$ 的定义如下（原子单位制）：

<a id="eqn:modelchemistries.dispersioncorrections.dftnl.theory.vv10-phi"></a>

$$
\varphi \left({ r,r'} \right) = -\frac{3}{2gg'\left({ g+g'} \right)}\qquad \text{(eqn:modelchemistries.dispersioncorrections.dftnl.theory.vv10-phi)}
$$

  

<a id="eqn:modelchemistries.dispersioncorrections.dftnl.theory.vv10-beta"></a>

$$
\beta = \frac{1}{32}\left[{ \frac{3}{b^{2} }} \right]^{3/4}\qquad \text{(eqn:modelchemistries.dispersioncorrections.dftnl.theory.vv10-beta)}
$$

其中

<a id="eqc:modelchemistries.dispersioncorrections.dftnl.theory.grw0k"></a>

$$
\begin{aligned}
  g\left( r \right) &= \omega_{0} \left( r \right)R^{2}+\kappa (r) \\ 
  R &= \left|{ r-r'} \right| \\ 
  \omega_{0} \left( r \right) &= \sqrt{ C\left|{ \frac{\nabla \rho (r) }{\rho (r) }} \right|^{4}+\frac{4\pi }{3}\rho (r) } \\ 
  \kappa \left( r \right) &= b\frac{3\pi }{2}\left[{ \frac{\rho (r) }{9\pi } } \right]^{1/6}
\end{aligned}\qquad \text{(eqc:modelchemistries.dispersioncorrections.dftnl.theory.grw0k)}
$$

在原始定义中，出现在$\kappa$ 和$\beta$ 中的短程衰减参数$b$ 是对 S22 非共价相互作用集[jurecka2006phys](../../bibliography.md) 拟合的（对于 rPW86PBE GGA，$b = 5.9$）。出现在$\omega_{0}$ 中的另一个参数$C = 0.0093$ 决定长程行为，被设为其原始值。其他 DFT-NL 泛函按类似方式构造。关于公式推导及其物理意义和基础的详细讨论，参见上述参考文献。

所定义的非局域 DFT-NL 交换-关联泛函的能量可以用两种方式计算：作为基于收敛 SCF 密度的 SCF 后（post-SCF）附加项，或采用自洽（self-consistent）处理。在我们对非自洽 DFT-NL 泛函的实现中，第一步先执行自洽 DFT 计算；第二步，将 DFT 计算得到的优化电子密度作为非局域部分能量计算的输入。在自洽处理中，轨道和密度在完整的 DFT + VV10 交换-关联势存在下进行优化。
根据大量测试计算，对于常规能量评估，很少需要自洽处理。
公式 [Eq](#eqn:modelchemistries.dispersioncorrections.dftnl.theory.ec-vv10) 中双重积分的计算需要使用积分网格（integration grid），就像常规交换-关联泛函一样。该网格的构建方式与 ORCA 中可用的常规网格类似，参见章节 [essentialelements.numericalintegration](../essentialelements/numericalintegration.md#sec:essentialelements.numericalintegration)。

<a id="sec:modelchemistries.dispersioncorrections.nl.basicusage"></a>
### 基本用法（Basic usage）

非自洽的 NL 变体可通过 `!NL` 关键词调用。

```orca
!B3LYP NL
```
自洽变体通过 `!SCNL` 调用。

```orca
!B3LYP SCNL
```

在当前版本的 ORCA 中，已为多种泛函和 HF 实现了 NL 参数：

<a id="tab:modelchemistries.dispersioncorrections.nl.params"></a>
!!! note "已有可用 NL 参数的方法（Methods with available NL parameters）。若未给出数值，则使用默认参数。"
    | 方法（Method）                                                    |$b$         |$C$        |$NLScal$                                |
    |:----------------------------------------------------------|:-----------:|:----------:|:---------------------------------------:|
    | **Hartree-Fock**                                          |             |            |                                         |
    | `HF`                                                      | 3.9         |            |                                         |
    | **(meta-)GGA**                                            |             |            |                                         |
    | `BLYP`                                                    | 4.0         |            |                                         |
    | `BP86`                                                    | 4.4         |            |                                         |
    | `PBE`                                                     | 6.4         |            |                                         |
    | `REVPBE`                                                  | 3.7         |            |                                         |
    | `RPBE`                                                    | 4.0         |            |                                         |
    | `RPW86PBE`                                                | 5.9         |            |                                         |
    | `SCANfunc`                                                | 6.4         |            |                                         |
    | `RSCAN`                                                   | 10.8        |            |                                         |
    | `R2SCAN`                                                  | 12.3        |            |                                         |
    | `TPSS`                                                    | 5.0         |            |                                         |
    | `B97M-V`                                                  | 6.0         | 0.01       |                                         |
    | **Hybrid**                                                |             |            |                                         |
    | `B3LYP`                                                   | 4.8         |            |                                         |
    | `B3LYP/G`                                                 | 4.8         |            |                                         |
    | `B3P86`                                                   | 5.3         |            |                                         |
    | `B3PW91`                                                  | 4.5         |            |                                         |
    | `mPW1PW`                                                  | 5.3         |            |                                         |
    | `PBE0`                                                    | 6.9         |            |                                         |
    | `PW1PW`                                                   | 7.7         |            |                                         |
    | `PW6B95`                                                  | 9.0         |            |                                         |
    | `REVPBE0`                                                 | 4.3         |            |                                         |
    | `REVPBE38`                                                | 4.7         |            |                                         |
    | `TPSSh`                                                   | 5.2         |            |                                         |
    | `TPSS0`                                                   | 5.5         |            |                                         |
    | `R2SCANh` (see [bursch_r2scanhybrids_2022](../../bibliography.md))         | 11.9        |            |                                         |
    | `R2SCAN0` (see [bursch_r2scanhybrids_2022](../../bibliography.md))         | 11.4        |            |                                         |
    | `R2SCAN50` (see [bursch_r2scanhybrids_2022](../../bibliography.md))        | 10.8        |            |                                         |
    | **Range-separated hybrid**                                |             |            |                                         |
    | `LRC-PBE`                                                 | 6.4         |            |                                         |
    | `WR2SCAN` (see [Wittmann2023](../../bibliography.md))                      | 9.2612      |            |                                         |
    | `WB97X-V`                                                 | 6.0         | 0.01       |                                         |
    | `WB97M-V`                                                 | 6.0         | 0.01       |                                         |
    | **Double-hybrid**                                         |             |            |                                         |
    | `B2PLYP` (see [arago_nonlocal_2013](../../bibliography.md))                | 7.8         |            |                                         |
    | `DSD-BLYP` (see [yu_spin-component-scaled_2014](../../bibliography.md))    | 12.0        |            |                                         |
    | `DSD-PBEP86` (see [yu_spin-component-scaled_2014](../../bibliography.md))  | 14.2        |            |                                         |
    | `DSD-BLYP/2013`                                           | 12.0        |            |                                         |
    | `DSD-PBEP86/2013`                                         | 14.2        |            |                                         |
    | `PWPB95` (see [yu_spin-component-scaled_2014](../../bibliography.md))      | 11.1        |            |                                         |
    | `PR2SCAN50` (see [Wittmann2023](../../bibliography.md))                    | 10.9207     |            | 0.75                                    |
    | `KPR2SCAN50` (see [Wittmann2023](../../bibliography.md))                   | 10.6723     |            | 0.70                                    |
    | `PR2SCAN69` (see [Wittmann2023](../../bibliography.md))                    | 9.0691      |            | 0.5556                                  |
    | **Range-separated double-hybrid**                         |             |            |                                         |
    | `WPR2SCAN50` (see [Wittmann2023](../../bibliography.md))                   | 9.4149      |            | 0.65                                    |
    | `WB97M(2)`                                                | 10.0        | 0.01       | 0.65904                                 |

!!! warning "重要"
    Head-Gordon 的$\omega$B97X-V[headgordon2014wB97XV](../../bibliography.md)、B97M-V [headgordon2015B97MV](../../bibliography.md) 和$\omega$B97M-V[headgordon2016wB97MV](../../bibliography.md) 泛函是专门拟合的变体，它们使用非局域 VV10 核来捕捉伦敦色散效应。
    它们默认采用非自洽 NL 校正，无需使用任何额外的 NL 关键词！自洽处理可通过 `!SCNL` 关键词调用。

!!! note "关于 ORCA 中 NL 校正的一些说明（Some notes on the NL corrections in ORCA）"

    * 哈特里-福克方法无法进行自洽计算。

    * 解析梯度（analytic gradients）可用，因此可以计算带有数值频率的几何优化。

    * TD-DFT 计算尚不可用。

    * 任何需要 NL 泛函二阶导数的计算目前尚不可行。CP-SCF 解中实型微扰（real type perturbations）需要这些二阶导数，例如解析 Hessian、偶极极化率（dipole polarizabilities）和双杂化梯度。

    * 严格的虚型微扰（strictly imaginary perturbations），如 NMR 屏蔽（shielding）和 EPR g 张量（两者也支持 GIAO），以及超精细耦合（hyperfine couplings）是可用的。

<a id="sec:modelchemistries.dispersioncorrections.nl.customparams"></a>
### 自定义参数（Custom parameters）

对于 NL，可以通过 `%method` 块调整参数$b$、$C$ 以及 NL 关联能项的全局缩放参数。全局缩放参数 `NLScal` 应用于对 NL 校正进行缩放，适用于那些已经部分涵盖长程关联的方法（如双杂化）。

```orca
!B3LYP NL

%method
  NLb    5.0
  NLC    0.0083
  NLScal 1.0
end
```

!!! note "注意"
    为了改善对较大体系的标度行为，还引入了一个距离截断（distance cutoff），由 `%method` 块中的 `vdWdistTCUT` 标志控制。默认值为 10 Å，即相距超过 10 Å 的两个格点不会通过 VV10 势发生关联。这一取值已经非常保守，对最终能量的实际影响为零，但如有需要可以更改。

<a id="sec:modelchemistries.dispersioncorrections.nl.example"></a>
### 示例（Example）

下面以 def2-TZVP 基组和 B3LYP 杂化泛函为例，计算距离为 3.76 Å 的氩二聚体（argon dimer）的能量。这里我们选择 DFT-NL 色散校正的非自洽变体。

```mol
title: structure 3
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
2
structure (0 1)
Ar          0.0          0.0          0.0
Ar          0.0          0.0         3.76
--- input ---
!B3LYP NL def2-TZVP

*xyz 0 1
  Ar  0.0 0.0 0.0
  Ar  0.0 0.0 3.76
*
```

该示例的 DFT-NL 输出如下所示：

```orca
-------------------------------------------------------------------------------
                    post-SCF DFT-NL dispersion correction                      
-------------------------------------------------------------------------------

SCF Energy:    -1054.960511496 
NL    Energy:      0.209449910 
SC+NL Energy:  -1054.751061586 
NL done in  :              0.7 sec
-------------------------------------------------------------------------------

[...]

----------------
TOTAL SCF ENERGY
----------------

[...]

DFT components:
N(Alpha)           :       17.999996328440 electrons
N(Beta)            :       17.999996328440 electrons
N(Total)           :       35.999992656880 electrons
E(X)               :      -47.880920358714 Eh       
E(C)               :       -1.761923687962 Eh       
NL Energy, E(C,NL) :        0.209449910227 Eh       
E(XC)              :      -49.433394136450 Eh
```

这里我们可以找到 B3LYP 总能量（`SCF Energy`）、非局域贡献（`NL Energy`）以及二者之和（`SC+NL Energy`），后者即为最终总能量。在 `DFT components` 部分中，非局域贡献被单独列出（`NL Energy, E(C,NL)`），以便与 `!SCNL` 的输出保持一致。

<a id="sec:modelchemistries.dispersioncorrections.nl.keywords"></a>
### 关键词（Keywords）

<a id="tab:modelchemistries.dispersioncorrections.nl.keywords.simple"></a>
!!! note "NL 校正的简单输入关键词（Simple input keywords for the NL correction）。"
    | 关键词（Keyword）                  | 描述（Description）                                |
    |:--------------------------------|:-------------------------------------------------|
    | `NL`                            | 激活非自洽 NL 校正                                  |
    | `SCNL`                          | 激活自洽 NL 校正                                   |

<a id="tab:modelchemistries.dispersioncorrections.nl.keywords.block"></a>
!!! note "NL 校正的 `%method` 块输入关键词（`%method` block input keywords for the NL correction）。"
    | 关键词（Keyword）                  | 选项（Options）        | 描述（Description）                                |
    |:--------------------------------|:------------------|:-------------------------------------------------|
    | `NLb`                           | `<real>`          | 控制 NL 的$b$ 参数                               || `NLC`                           | `<real>`          | 控制 NL 的$C$ 参数                               |
    | `NLScal`                        | `<real>`          | 控制 NL 的全局缩放参数                               |
    | `vdWdistTCUT`                   | `<real>`          | 控制 NL 的关联距离截断                               |

