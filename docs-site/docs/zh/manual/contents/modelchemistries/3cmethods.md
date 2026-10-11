

<a id="sec:modelchemistries.3cmethods"></a>
# 复合方法（Composite Methods，3c 方法）

复合（composite）[HF](hartreefock.md#sec:essentialelements.hartreefock) 和 [DFT](../modelchemistries/DensityFunctionalTheory.md) 方法利用相对较小的定制[基组](../essentialelements/basisset.md)和特殊的校正项，以远低于逼近基组极限（basis set limit）计算的代价实现高精度。最著名的复合方法是 Grimme 及其同事提出的所谓 "3c" 方法。

<a id="sec:modelchemistries.3cmethods.hf3c"></a>
## HF-3c

HF-3c 是一种快速的基于[哈特里-福克](hartreefock.md#sec:essentialelements.hartreefock)的方法，专为计算巨大分子体系的结构、振动频率（vibrational frequencies）和非共价相互作用能（non-covalent interaction energies）而开发[sure_hf3c](../../bibliography.md)。评估电子能量的起点是一个采用小型高斯型原子轨道（Gaussian AO）基组的标准 HF 计算。所用的所谓 MINIX 基组针对不同的原子组使用不同的基函数集合，如表 [tab:modelchemistries.3cmethods.minix](#tab:modelchemistries.3cmethods.minix) 所示。在 ORCA 中，HF-3c 适用于直至 Pu（Z = 94）的所有元素。

<a id="tab:modelchemistries.3cmethods.minix"></a>
!!! note "MINIX 基组的构成（Composition of the MINIX basis set）。"
    | 元素（element） | 基组（basis）                            |
    |:-----------|:-------------------------------------|
    | H-He, B-Ne | MINIS                                |
    | Li-Be      | MINIS+1(p)                           |
    | Na-Mg      | MINIS+1(p)                           |
    | Al-Ar      | MINIS+1(d)                           |
    | K-Zn       | SV                                   |
    | Ga-Kr      | SVP                                  |
    | Rb-Rn      | def2-SVP with def-ECPs               |
    | Fr-Lr      | def-SVP with def-ECPs                |

在 HF 能量$E_{\text{tot} }^{\text{HF/MINIX} }$ 上添加三项校正，以包含伦敦色散相互作用（London dispersion interactions）、处理 BSSE（基组重叠误差，basis set superposition error）并校正基组缺陷（即被高估的键长）。因此，校正后的总能量计算为

<a id="eq:hf3c"></a>

$$
E_{\text{tot} }^{\text{HF-3c} } = E_{\text{tot} }^{\text{HF/MINIX} } + E_{\text{disp} }^{\text{D3(BJ) }} + E_{\text{BSSE} }^{\text{gCP} } + E_{\text{SRB} }.\qquad \text{(eq:hf3c)}
$$

第一项校正$E_{\text{disp} }^{\text{D3(BJ) }}$ 来自 [D3 色散校正](dispersioncorrections.md#sec:modelchemistries.dispersioncorrections.dftd.theory)方案[grimme2010chem](../../bibliography.md)中逐原子对的伦敦色散能，并采用 Becke-Johnson（BJ）阻尼（damping）[becke2005chem,johnson2005chem,johnson2006chem](../../bibliography.md)（参见章节 [dftd.theory](dispersioncorrections.md#sec:modelchemistries.dispersioncorrections.dftd.theory)）。第二项$E_{\text{BSSE} }^{\text{gCP} }$ 表示用于处理 BSSE 的[几何反位校正（geometrical counterpoise, gCP）](../essentialelements/counterpoise.md#sec:essentialelements.counterpoise.gcp)[KrusegCP](../../bibliography.md)（参见章节 [counterpoise.gcp](../essentialelements/counterpoise.md#sec:essentialelements.counterpoise.gcp)）。对于 HF-3c 方法，三个常规 D3 参数$s_8$、$a_1$ 和$a_2$ 已使用 S66 测试集[resac2011chem](../../bibliography.md)中配合物的参考相互作用能重新拟合。结果为$s_8=0.8777$、$a_1=0.4171$ 和$a_2=2.9149$。与往常一样，参数$s_6$ 设为 1 以强制满足正确的渐近极限（asymptotic limit），并且 gCP 校正已在该拟合步骤中应用。

最后一项$E_{\text{SRB} }$ 是一项短程校正，用于处理使用小型或最小基组时出现的基组缺陷。它校正电负性元素共价键长被系统性高估的问题，计算为对所有原子对求和：

$$
E_{\text{SRB} } = -s \sum_{A}^{\text{Atoms} } \sum_{B \neq A}^{\text{Atoms} }(Z_A Z_B)^{3/2}\exp(-\gamma (R_{AB}^{0,\text{D3} })^{3/4}
                 R_{AB})
$$

其中，$R_{AB}^{0,\text{D3} }$ 是为 D3 方案[grimme2010chem](../../bibliography.md)从头算确定的默认截断半径，$Z_A$、$Z_B$ 是核电荷数。该校正适用于直至氩（Ar）的所有元素。经验拟合参数$s=0.03$ 和$\gamma= 0.7$ 的确定基于这样一个要求：对于 107 个小有机分子的 B3LYP-D3(BJ)/def2-TZVPP 平衡结构，HF-3c 的总原子受力应接近于零。更多细节可参见原始文献[sure_hf3c](../../bibliography.md)。

HF-3c 方法只能通过一个简单关键词调用：

```orca
! HF-3c
```

`! HF-3c` 是一个复合关键词（compound keyword），等同于 `! HF MINIX D3BJ GCP(HF/MINIX) PATOM`，因此无需指定基组等。之所以选择 `PATOM` 初始猜测，是因为默认猜测的网格构建可能比一个实际 SCF 步骤耗时更长。该初始猜测只能在 %method 部分手动覆盖。

积分处理的默认模式设为 `Conventional`。将双电子积分存储到磁盘上，或尽可能存储到内存中，可以大幅节省计算开销。如果想使用 `Direct` 模式，则必须在 %scf 输入部分中指定：

```orca
%scf
  SCFmode Direct
end
```

输出中会分别给出 D3 和 gCP 所使用的参数及校正本身。由于 SRB 校正也由 otool_gcp 计算，其结果给出在 gCP 输出部分中。`Total correction to HF/MINIX` 是全部三项校正（D3、gCP 和 SRB）之和，`FINAL SINGLE POINT ENERGY` 是公式 [Eq](#eq:hf3c) 中给出的 HF-3c 总能量。

```orca
-------------------------------------------------------------------------------
                          DFT DISPERSION CORRECTION

                                DFTD3 V2.1  Rev 6
                          USING Becke-Johnson damping
-------------------------------------------------------------------------------
The default Hartree-Fock  is recognized
Active option DFTDOPT                   ...         4

molecular C6(AA) [au] = 1689.256597

            DFT-D V3
 parameters
 using HF/MINIX parameters
 s6 scaling factor         :     1.0000
 a1 scaling factor         :     0.4171
 s8 scaling factor         :     0.8777
 a2 scaling factor         :     2.9149
 ad hoc parameters k1-k3   :    16.0000     1.3333    -4.0000

 Edisp/kcal,au: -32.163184627631  -0.051255291794
 E6   /kcal   : -18.007221978
 E8   /kcal   : -14.155962649
 % E8         :  44.012938437

-------------------------   ----------------
Dispersion correction            -0.051255292
-------------------------   ----------------

------------------------------------------------------------------------------

                  g C P  - geometrical counterpoise correction

------------------------------------------------------------------------------
Method:  hf/minix

Parameters:   sigma        eta         alpha        beta
              0.1290      1.1526      1.1549       1.1763
Egcp:       0.0723150636 a.u.
Ebas:      -0.0636976872 a.u.
------------------   -----------------
gCP+bas correction         0.008617376
------------------   -----------------
----------------------------   ----------------
Total correction to HF/MINIX       -0.042637915
----------------------------   ----------------

-------------------------   --------------------
FINAL SINGLE POINT ENERGY      -163.002895262171
-------------------------   --------------------
```

对于直至 Xe 的元素，默认初始猜测为休克尔（Hückel）猜测。对于 Xe 之后的元素，猜测模式改为 `HCORE`，因为对应的 ECP 基组没有可用的休克尔参数，且目前尚未实现其他模型。对于只含较轻元素、因而不含 ECP 的计算，输出文件中的 ECP 打印信息可以忽略。

<a id="sec:modelchemistries.3cmethods.b973c"></a>
## B97-3c

B97-3c[grimme_b973c](../../bibliography.md)是另一种复合 DFT 方法，专为热化学（thermochemistry）、结构和非共价相互作用（noncovalent interactions）设计，尤其适用于过渡金属化学及其他强关联（strongly correlated）体系。它基于 B97 GGA 泛函，包含带三体贡献（three-body contribution）的 [D3(BJ) 色散校正](dispersioncorrections.md#sec:modelchemistries.dispersioncorrections.dftd.theory)、一项短程键长校正，以及一个经过修改、精简的三 zeta（triple-$\zeta$）基组 def2-mTZVP。该方法的计算成本介于 HF-3c 与 [PBEh-3c](#sec:modelchemistries.3cmethods.pbeh3c) 之间（对大体系而言大约是 [HF-3c](#sec:modelchemistries.3cmethods.hf3c) 的两倍）。在 ORCA 中，B97-3c 适用于直至 Pu（Z = 94）的所有元素。

B97-3c 可通过简单输入关键词调用：

```orca
! B97-3c
```

<a id="sec:modelchemistries.3cmethods.r2scan3c"></a>
##$r^2$SCAN-3c

$r^2$SCAN-3c 复合方法[grimme2020r2scan3c](../../bibliography.md)是一种稳健的"瑞士军刀式"电子结构方法，适用于热化学、几何结构和非共价相互作用，初步测试表明它对开壳层和闭壳层的过渡金属配合物均表现一致。它基于$r^2$SCAN[furness2020r2scan](../../bibliography.md) meta-GGA 泛函，结合 [D4 色散校正](dispersioncorrections.md#sec:modelchemistries.dispersioncorrections.dftd.theory)[ehlert2020r2scand4](../../bibliography.md)和[几何反位校正（geometrical counter poise-correction）](../essentialelements/counterpoise.md#sec:essentialelements.counterpoise.gcp)[KrusegCP](../../bibliography.md)。修改后的三 zeta 基组 def2-mTZVPP 对轻主族元素而言更大、更一致，且计算效率几乎与 [B97-3c](#sec:modelchemistries.3cmethods.b973c) 的 def2-mTZVP 基组相当。$r^2$SCAN-3c 的计算成本略高于 [B97-3c](#sec:modelchemistries.3cmethods.b973c)。在 ORCA 中，$r^2$SCAN-3c 适用于直至 Lr（Z = 103）的所有元素。可通过简单关键词调用：

```orca
! r2SCAN-3c
```

<a id="sec:modelchemistries.3cmethods.pbeh3c"></a>
## PBEh-3c

PBEh-3c 是一种高效的电子结构方法，在几何结构优化和非共价配合物相互作用能方面表现尤为出色。[grimme_pbeh3c](../../bibliography.md)此处采用 Perdew-Burke-Ernzerhof（PBE）泛函的一个全局杂化（global hybrid）变体，其非局域 Fock 交换（non-local Fock-exchange）比例较高（42%），并配以价层双 zeta（valence-double-zeta）高斯型原子轨道基组（def2-mSVP）。基组重叠误差（BSSE）和伦敦色散效应分别通过 [gCP](../essentialelements/counterpoise.md#sec:essentialelements.counterpoise.gcp) 和 [D3](dispersioncorrections.md#sec:modelchemistries.dispersioncorrections.dftd.theory) 方案加以考虑（见上文）。基组的构成如下：

<a id="tab:modelchemistries.3cmethods.def2msvp"></a>
!!! note "def2-mSVP 基组的构成（Composition of the def2-mSVP basis set）。"
    | 元素（element） | 基组（basis）                                     |
    |:------------|:------------------------------------------|
    | H           | def2-SV(P) ($\alpha$ scaled by 1.2)       |
    | He          | def2-SVP(-p)                              |
    | Li-Be,Na-Kr | def2-SV(P)                                |
    | B,Ne        | Ahlrichs' DZ + Polarization from def2-SVP |
    | C-F         | Ahlrichs' DZ + Polarization from 6-31G\*  |
    | Rb-Rn       | def2-SVP with def2 ECPs                   |
    | Fr-Lr       | def-SVP with def-ECPs                     |

对于分子间和分子内 BSSE，使用公式 [Eq](#eqn:gcp) 中的 [gCP](../essentialelements/counterpoise.md#sec:essentialelements.counterpoise.gcp) 表达式，但额外加入一个阻尼函数（damping function，类似于公式 [Eq](#eqn:modelchemistries.dispersioncorrections.dftd.theory.zero) 中的零阻尼（zero-damping））。与未加阻尼的版本相比，该阻尼显著改善了方法的热化学精度。伦敦色散效应通过包含三体项的 [DFT-D3](dispersioncorrections.md#sec:modelchemistries.dispersioncorrections.dftd.theory)（BJ 阻尼）方案加以考虑。与相关的 HF-3c 方法相比，PBEh-3c 的成本稍高，但给出的几何结构好得多。这些几何结构大致达到 MP2 的精度水平（对于非共价结构甚至更好），但计算成本却低得多。由于非局域 Fock 交换比例适中，该方法较不易受自相互作用误差（self-interaction errors，如 GGA 中那样）影响，同时在哈特里-福克方法失效的情形（强关联体系）下仍然适用。在 ORCA 中，PBEh-3c 适用于直至 Pu（Z = 94）的所有元素。

PBEh-3c 方法可通过简单关键词调用：

```orca
! PBEh-3c
```

与 HF-3c 相同，直至 Xe 的所有元素的默认初始猜测为休克尔猜测。对于 Xe 之后的元素，猜测模式改为 `HCORE`。对于只含较轻元素、因而不含 ECP 的计算，输出文件中的 ECP 打印信息可以忽略。

<a id="sec:modelchemistries.3cmethods.b3lyp3c"></a>
## B3LYP-3c

B3LYP-3c 是 Grimme 及其同事提出的一种方法组合，用于高效计算气相红外光谱（gas-phase infrared spectra）。[grimme2020b3lyp3c](../../bibliography.md)
它将标准 B3LYP 泛函与 [D3(BJ)-ATM 色散校正](dispersioncorrections.md#sec:modelchemistries.dispersioncorrections.dftd.theory)、def2-mSVP 基组以及[几何反位校正](../essentialelements/counterpoise.md#sec:essentialelements.counterpoise.gcp)相结合。
在 ORCA 中，B3LYP-3c 适用于直至 Pu（Z = 94）的所有元素。B3LYP-3c 可通过简单输入关键词调用：

```orca
! B3LYP-3c
```
也可以通过以下方式从其各组成部分手动构建：

```orca
!B3LYP D3BJ GCP(DFT/SV(P)) def2-mSVP ABC
```

<a id="sec:modelchemistries.3cmethods.wb97x3c"></a>
##$\omega$B97X-3c

$\omega$B97X-3c 复合方法[grimme2022wb97x3c](../../bibliography.md)基于$\omega$B97X-V 泛函，结合了定制且经分子优化的极化价层双 zeta（polarized valence double-$\zeta$, vDZP）基组和专门调整的 D4 色散校正。vDZP 基组采用大核 ECP（large-core ECP），与常规双 zeta 基组相比，仅表现出极小的基组重叠误差和基组不完备误差（basis set incompleteness errors）。在对标准基准测试集进行的全面测试中，$\omega$B97X-3c 方法的表现与四 zeta（quadruple-$\zeta$）基组下表现良好的杂化 DFT 方法相当，而计算成本仅为其一小部分。$\omega$B97X-3c 对直至 Rn（Z = 1--86）的所有元素均可用。

可通过简单关键词调用：

```orca
! wB97X-3c
```

单独使用 vDZP 基组的方式如下（注意相应的大核 ECP 会被自动调用）：

```orca
! vDZP
```

<a id="sec:modelchemistries.3cmethods.keywords"></a>
## 关键词（Keywords）

<a id="tab:modelchemistries.3cmethods.keywords.simple"></a>
!!! note "3c 复合方法的简单输入关键词（Simple input keywords for the 3c composite methods）。"
    | 关键词（Keyword）                  | 描述（Description）                                                                          |
    |:--------------------------------|:-----------------------------------------------------------------------------------------|
    | `HF-3C`                         | 调用 [HF-3c](#sec:modelchemistries.3cmethods.hf3c) 方法                                    |
    | `B97-3C`                        | 调用 [B97-3c](#sec:modelchemistries.3cmethods.b973c) 方法                                  |
    | `R2SCAN-3C`                     | 调用 [$r^2$SCAN-3c](#sec:modelchemistries.3cmethods.r2scan3c) 方法                         |
    | `PBEH-3C`                       | 调用 [PBEh-3c](#sec:modelchemistries.3cmethods.pbeh3c) 方法                                |
    | `B3LYP-3C`                      | 调用 [B3LYP-3c](#sec:modelchemistries.3cmethods.b3lyp3c) 方法                              |
    | `WB97X-3C`                      | 调用 [$\omega$B97X-3c](#sec:modelchemistries.3cmethods.wb97x3c) 方法                       |

