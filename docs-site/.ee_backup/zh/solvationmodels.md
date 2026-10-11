

<a id="sec:essentialelements.solvationmodels"></a>
# 隐式溶剂化（Implicit Solvation）

隐式溶剂化模型（implicit solvation models）在量子化学中扮演着重要角色。
无需放置多层溶剂分子的溶剂化壳层，隐式溶剂模型就能模拟特定溶剂对溶质的影响。

ORCA 中可用的隐式溶剂模型有

1.   C-PCM[barone1998,garcia_neese_gcs](../../bibliography.md)：类导体连续极化模型（Conductor-like Continuum Polarization Model）

2.   SMD[marenich2009](../../bibliography.md)：基于密度的溶剂化模型（Solvation Model based on Density）

3.   OpenCOSMO-RS[gerlachcosmors2022](../../bibliography.md)：COSMO-RS 模型开源实现的接口

4.   ALPB/ddCOSMO/CPCM-X：XTB 中可用的溶剂化模型

关于 C-PCM 和 SMD，它们是 ORCA 的原生实现。借助这些模型，可以使用
带有真实 van der Waals 空腔的可极化连续介质进行各种类型的计算，概述如下：

-   在 HF 和 DFT 层面以及后 HF 方法下，计算介电常数（dielectric constant）
    $\varepsilon$ 有限的溶液中分子的能量。

-   使用 HF 或任何带解析梯度的 DFT 方法优化溶液中的分子结构。

-   对 HF 或任何 DFT 方法，使用解析 Hessian 计算振动频率，
    前提是相同的计算在真空中也可用。

-   通过耦合微扰 SCF 理论（coupled-perturbed SCF theory）计算溶剂对
    极化率等响应性质的影响。对于磁响应性质（如 g 张量），C-PCM 响应为零。

-   使用含时 DFT 或 CIS 方法计算溶剂对跃迁能量的位移。
    除介电常数外，还需要提供溶剂的折射率（refractive index）。

-   在多参考微扰和组态相互作用计算中，
    对状态能量和跃迁能量的溶剂效应做一阶微扰估计。

关于可用隐式溶剂化方法及其用法的详细概述，见
[sec:essentialelements.solvationmodels.cpcm.detailed](#sec:essentialelements.solvationmodels.cpcm.detailed)、
[sec:essentialelements.solvationmodels.smd.detailed](#sec:essentialelements.solvationmodels.smd.detailed)、
[sec:essentialelements.solvationmodels.opencosmors](#sec:essentialelements.solvationmodels.opencosmors)、
[sec:modelchemistries.semiempirical.xtb](#sec:modelchemistries.semiempirical.xtb) 和 [sec:oniom](#sec:oniom) 各节。

<a id="sec:essentialelements.solvationmodels.cpcm.detailed"></a>
## 类导体可极化连续介质模型（C-PCM）

类导体可极化连续介质模型（conductor-like polarizable continuum model,
C-PCM）是类导体表观表面电荷方法（conductor-like apparent surface charge
methods）的一种实现。在这些模型中，溶质被置于一个大致呈分子形状的空腔
（cavity）中。溶剂反应场（solvent reaction field）由空腔表面的表观极化电荷
（apparent polarization charges）描述，而这些电荷又由溶质决定。
这些电荷可以作为点电荷（point charges）处理，也可以建模为球形 Gaussian
电荷 [york_gauss](../../bibliography.md)。ORCA 中空腔的构建方式取决于电荷的处理方式。
在使用点电荷的情况下，空腔通过 GEPOL[gepol1,gepol2,gepol3](../../bibliography.md) 算法生成，
可以是溶剂排除表面（solvent-excluding surface, SES）或溶剂可及表面
（solvent-accessible surface, SAS）。当考虑 Gaussian 电荷时，
用户可以在缩放 vdW 表面和 GEPOL SES 之间选择，而电荷位置则按
Lebedev 求积（Lebedev quadrature）方法确定。这一方案称为 Gaussian
电荷方案（Gaussian Charge Scheme）[garcia_neese_gcs](../../bibliography.md)，
关于如何使用它的更多细节见
[sec:essentialelements.solvationmodels.gaussian_charge](#sec:essentialelements.solvationmodels.gaussian_charge) 一节。

在 C-PCM 中，孤立体系的分子哈密顿量受溶剂微扰：

$$

\hat{H} = \hat{H}^0 + \hat{V}

$$

其中 $\hat{H}^0$ 是孤立分子的哈密顿量，而 $\hat{V}$ 描述溶质-溶剂相互作用。
SCF 流程导致溶质自由能 $G$ 的变分极小化：

$$

G = \left\langle\Psi \left| \hat{H}^0 \right| \Psi \right\rangle+
\frac{1}{2} \left\langle\Psi \left| \hat{V} \right| \Psi \right\rangle

$$

利用类导体边界条件，静电势可由下式确定

$$

V(\vec{r}) + \sum_i^{N_q} V_{q_i} (\vec{r}) = 0

$$

其中 $V$ 和 $V_{q_i}$ 分别是溶质和极化电荷产生的静电势，
$\vec{r}$ 是空腔表面上的一点，$N_q$ 是溶剂化电荷的总数。
极化电荷向量随后可由下式确定

$$

\mathbf{AQ = -V}\qquad \text{(eqn:feps)}

$$

其中向量 $\mathbf{V}$ 含有溶质在电荷位置处的静电势。
矩阵 $\mathbf{A}$ 的元素具有不同的函数形式，取决于电荷的处理方式。
若使用点电荷：

$$

A_{ii} = 1.07 \sqrt{ \frac{4\pi}{S_i} }

$$
$$

A_{ij} = \frac{1}{r_{ij} }\qquad \text{(eq:Aijp)}

$$

其中 $S_i$ 是面元 $i$ 的面积，$r_{ij}=\left| \vec{r}_i - \vec{r}_j \right|$。
当考虑 Gaussian 电荷时：

$$

A_{ii} = \frac{\zeta_i\sqrt{2/\pi} }{F_i}

$$
$$

A_{ij} = \frac{\mathrm{erf}\left(\zeta_{ij}r_{ij}\right)}{r_{ij} }

$$

这里 $\zeta_i$ 是 Gaussian 电荷 $i$ 的指数（$i$ 属于球 $I$）。该量计算为
$\zeta_i=\zeta/(R_I\sqrt{w_i})$，其中 $R_I$ 是球 $I$ 的半径，
$w_i$ 是 Lebedev 点 $i$ 的权重，$\zeta$ 是为每种特定 Lebedev 格点
优化的宽度参数 [york_gauss](../../bibliography.md)。另一方面，
$\zeta_{ij}=\zeta_i\zeta_j/\sqrt{\zeta_i^2+\zeta_j^2}$。函数 $F_i$
称为开关函数（switching function），它度量 Gaussian 电荷 $i$
对溶剂化能的贡献。该函数计算为

$$

F_i=\prod^{\mathrm{atoms} }_{J,i\notin J}g(\vec{r}_i,\vec{R}_J)

$$

其中 $g(\vec{r}_i,\vec{R}_J)$ 是基本开关函数。在 ORCA 中，
我们对 $g(\vec{r}_i,\vec{R}_J)$ 使用参考文献 [lange2010](../../bibliography.md)
提出的改进 Switching/Gaussian（ISWIG）函数：

$$

g(\vec{r}_i,\vec{R}_J)=1-\frac{1}{2}\left\{\mathrm{erf}\left[\zeta_i\left(R_J-r_{iJ}\right)\right]+\mathrm{erf}\left[\zeta_i\left(R_J+r_{iJ}\right)\right]\right\}

$$

若 $g(\vec{r}_i,\vec{R}_J)<10^{-7}$，则 $g$ 的值设为 0。
如果我们考虑介电常数为 $\varepsilon$ 的溶剂，公式 [Eq](#eqn:feps) 写作

$$

\mathbf{AQ} = -f(\varepsilon)\mathbf{V}\qquad \text{(eq_cpcm)}

$$

其中 $f(\varepsilon)=(\varepsilon - 1)/(\varepsilon + x)$ 是标度函数，
$x$ 在 0–2 范围内。在 C-PCM 中 $x$ 等于 0。

C-PCM 模型可通过

```orca
! CPCM(solvent)
```

使用，其中 `solvent` 是 [table:list-solvents](#table:list-solvents) 中可用的溶剂之一

<a id="table:list-solvents"></a>
!!! note "ORCA 中 C-PCM、SMD、openCOSMO-RS 和 ALPB 可用的溶剂列表。C-PCM 中所用介电常数的数据是 293.15 K 下的值，[crcchemistry2014](../../bibliography.md) 氨除外（其沸点为 239.81 K）。其余溶剂化模型见相应来源。[marenich2009](../../bibliography.md)[cpcmx2023](../../bibliography.md) 注意 ALPB 仅在 XTB 计算中可用。另一方面，ddCOSMO 和 CPCM-X 的溶剂列表见 [tab:modelchemistries.semiempirical.xtb.solvation.solvents](#tab:modelchemistries.semiempirical.xtb.solvation.solvents)。"
    |  溶剂               |   C-PCM     |   SMD      |   COSMO-RS  |  ALPB     |
    |:--------------------:|:-----------:|:----------:|:---------:|:---------:|
    | 1,1,1-trichloroethane            | X | X |  |  |
    | 1,1,2-trichloroethane            | X | X |  |  |
    | 1,2,4-trimethylbenzene           | X | X |  |  |
    | 1,2-dibromoethane                | X | X | X |  |
    | 1,2-dichloroethane               | X | X | X |  |
    | 1,2-ethanediol                   | X | X |  |  |
    | 1,4-dioxane / dioxane            | X | X | X | X |
    | 1-bromo-2-methylpropane          | X | X |  |  |
    | 1-bromooctane / bromooctane      | X | X | X |  |
    | 1-bromopentane                   | X | X |  |  |
    | 1-bromopropane                   | X | X |  |  |
    | 1-butanol / butanol              | X | X | X |  |
    | 1-chlorohexane / chlorohexane    | X | X | X |  |
    | 1-chloropentane                  | X | X |  |  |
    | 1-chloropropane                  | X | X |  |  |
    | 1-decanol / decanol              | X | X | X |  |
    | 1-fluorooctane                   | X | X | X |  |
    | 1-heptanol / heptanol            | X | X | X |  |
    | 1-hexanol / hexanol              | X | X | X |  |
    | 1-hexene                         | X | X |  |  |
    | 1-hexyne                         | X | X |  |  |
    | 1-iodobutane                     | X | X |  |  |
    | 1-iodohexadecane / hexadecyliodide| X | X | X |  |
    | 1-iodopentane                    | X | X |  |  |
    | 1-iodopropane                    | X | X |  |  |
    | 1-nitropropane                   | X | X |  |  |
    | 1-nonanol / nonanol              | X | X | X |  |
    | 1-octanol / octanol              | X | X | X | X |
    | 1-pentanol / pentanol            | X | X | X |  |
    | 1-pentene                        | X | X |  |  |
    | 1-propanol / propanol            | X | X | X |  |
    | 2,2,2-trifluoroethanol           | X | X |  |  |
    | 2,2,4-trimethylpentane / isooctane | X | X | X |  |
    | 2,4-dimethylpentane              | X | X |  |  |
    | 2,4-dimethylpyridine             | X | X |  |  |
    | 2,6-dimethylpyridine             | X | X | X |  |
    | 2-bromopropane                   | X | X |  |  |
    | 2-butanol / secbutanol           | X | X | X |  |
    | 2-chlorobutane                   | X | X |  |  |
    | 2-heptanone                      | X | X |  |  |
    | 2-hexanone                       | X | X |  |  |
    | 2-methoxyethanol / methoxyethanol| X | X | X |  |
    | 2-methyl-1-propanol / isobutanol | X | X | X |  |
    | 2-methyl-2-propanol              | X | X |  |  |
    | 2-methylpentane                  | X | X |  |  |
    | 2-methylpyridine / 2methylpyridine| X | X | X |  |
    | 2-nitropropane                   | X | X |  |  |
    | 2-octanone                       | X | X |  |  |
    | 2-pentanone                      | X | X |  |  |
    | 2-propanol / isopropanol         | X | X | X |  |
    | 2-propen-1-ol                    | X | X |  |  |
    | e-2-pentene                      | X | X |  |  |
    | 3-methylpyridine                 | X | X |  |  |
    | 3-pentanone                      | X | X |  |  |
    | 4-heptanone                      | X | X |  |  |
    | 4-methyl-2-pentanone / 4methyl2pentanone| X | X | X |  |
    | 4-methylpyridine                 | X | X |  |  |
    | 5-nonanone                       | X | X |  |  |
    | acetic acid / aceticacid         | X | X | X |  |
    | acetone                          | X | X | X | X |
    | acetonitrile / mecn / ch3cn      | X | X | X | X |
    | acetophenone                     | X | X | X |  |
    | ammonia                          | X |  | X |  |
    | aniline                          | X | X | X | X |
    | anisole                          | X | X | X |  |
    | benzaldehyde                     | X | X | X | X |
    | benzene                          | X | X | X | X |
    | benzonitrile                     | X | X | X |  |
    | benzyl alcohol / benzylalcohol   | X | X | X |  |
    | bromobenzene                     | X | X | X |  |
    | bromoethane                      | X | X | X |  |
    | bromoform                        | X | X | X |  |
    | butanal                          | X | X |  |  |
    | butanoic acid                    | X | X |  |  |
    | butanone                         | X | X | X |  |
    | butanonitrile                    | X | X |  |  |
    | butyl ethanoate / butyl acetate / butylacetate| X | X | X |  |
    | butylamine                       | X | X |  |  |
    | n-butylbenzene / butylbenzene    | X | X | X |  |
    | sec-butylbenzene / secbutylbenzene| X | X | X |  |
    | tert-butylbenzene / tbutylbenzene| X | X | X |  |
    | carbon disulfide / carbondisulfide / cs2| X | X | X | X |
    | carbon tetrachloride / ccl4      | X | X | X |  |
    | chlorobenzene                    | X | X | X |  |
    | chloroform / chcl3               | X | X | X | X |
    | a-chlorotoluene                  | X | X |  |  |
    | o-chlorotoluene                  | X | X |  |  |
    | conductor                        | X |  |  |  |
    | m-cresol / mcresol               | X | X | X |  |
    | o-cresol                         | X | X |  |  |
    | cyclohexane                      | X | X | X |  |
    | cyclohexanone                    | X | X | X |  |
    | cyclopentane                     | X | X |  |  |
    | cyclopentanol                    | X | X |  |  |
    | cyclopentanone                   | X | X |  |  |
    | decalin                          | X | X | X |  |
    | cis-decalin                      | X | X |  |  |
    | n-decane / decane                | X | X | X |  |
    | dibromomethane                   | X | X |  |  |
    | dibutylether                     | X | X | X |  |
    | o-dichlorobenzene / odichlorobenzene| X | X | X |
    | e-1,2-dichloroethene             | X | X |  |  |
    | z-1,2-dichloroethene             | X | X |  |  |
    | dichloromethane / ch2cl2 / dcm   | X | X | X | X |
    | diethyl ether / diethylether     | X | X | X | X |
    | diethyl sulfide                  | X | X |  |  |
    | diethylamine                     | X | X |  |  |
    | diiodomethane                    | X | X |  |  |
    | diisopropyl ether / diisopropylether| X | X | X |  |
    | cis-1,2-dimethylcyclohexane      | X | X |  |  |
    | dimethyl disulfide               | X | X |  |  |
    | n,n-dimethylacetamide / dimethylacetamide| X | X | X |  |
    | n,n-dimethylformamide / dimethylformamide / dmf| X | X | X | X |
    | dimethylsulfoxide / dmso         | X | X | X | X |
    | diphenylether                    | X | X | X |  |
    | dipropylamine                    | X | X |  |  |
    | n-dodecane / dodecane            | X | X | X |  |
    | ethanethiol                      | X | X |  |  |
    | ethanol                          | X | X | X | X |
    | ethyl acetate / ethylacetate / ethanoate| X | X | X | X |
    | ethyl methanoate                 | X | X |  |  |
    | ethyl phenyl ether / ethoxybenzene| X | X | X |  |
    | ethylbenzene                     | X | X | X |  |
    | fluorobenzene                    | X | X | X |  |
    | formamide                        | X | X |  |  |
    | formic acid                      | X | X |  |  |
    | furan / furane                   |  |  | X | X |
    | n-heptane / heptane              | X | X | X |  |
    | n-hexadecane / hexadecane        | X | X | X | X |
    | n-hexane / hexane                | X | X | X | X |
    | hexanoic acid                    | X | X |  |  |
    | iodobenzene                      | X | X | X |  |
    | iodoethane                       | X | X |  |  |
    | iodomethane                      | X | X |  |  |
    | isopropylbenzene                 | X | X | X |  |
    | p-isopropyltoluene / isopropyltoluene| X | X |  |  |
    | mesitylene                       | X | X | X |  |
    | methanol                         | X | X | X | X |
    | methyl benzoate                  | X | X |  |  |
    | methyl butanoate                 | X | X |  |  |
    | methyl ethanoate                 | X | X |  |  |
    | methyl methanoate                | X | X |  |  |
    | methyl propanoate                | X | X |  |  |
    | n-methylaniline                  | X | X |  |  |
    | methylcyclohexane                | X | X |  |  |
    | n-methylformamide / methylformamide | X | X | X |  |
    | nitrobenzene / phno2             | X | X | X |  |
    | nitroethane                      | X | X | X |  |
    | nitromethane / meno2             | X | X | X | X |
    | o-nitrotoluene / onitrotoluene   | X | X |  |  |
    | n-nonane / nonane                | X | X | X |  |
    | n-octane / octane                | X | X | X |  |
    | n-pentadecane / pentadecane      | X | X | X |  |
    | octanol(wet) / wetoctanol / woctanol|  |  |  | X |
    | pentanal                         | X | X |  |  |
    | n-pentane / pentane              | X | X | X |  |
    | pentanoic acid                   | X | X |  |  |
    | pentyl ethanoate                 | X | X |  |  |
    | pentylamine                      | X | X |  |  |
    | perfluorobenzene / hexafluorobenzene | X | X | X |  |
    | phenol                           | X |   | X | X |
    | propanal                         | X | X |  |  |
    | propanoic acid                   | X | X |  |  |
    | propanonitrile                   | X | X |  |  |
    | propyl ethanoate                 | X | X |  |  |
    | propylamine                      | X | X |  |  |
    | pyridine                         | X | X | X |  |
    | tetrachloroethene / c2cl4        | X | X | X |  |
    | tetrahydrofuran / thf            | X | X | X | X |
    | tetrahydrothiophene-s,s-dioxide /| X | X |  |  |
    | / tetrahydrothiophenedioxide / sulfolane| X | X |  |  |
    | tetralin                         | X | X | X |  |
    | thiophene                        | X | X |  |  |
    | thiophenol                       | X | X |  |  |
    | toluene                          | X | X | X | X |
    | trans-decalin                    | X | X |  |  |
    | tributylphosphate                | X | X | X |  |
    | trichloroethene                  | X | X |  |  |
    | triethylamine                    | X | X | X |  |
    | n-undecane / undecane            | X | X | X |  |
    | water / h2o                      | X | X | X | X |
    | xylene                           | X | X |  |  |
    | m-xylene                         | X | X |  |  |
    | o-xylene                         | X | X |  |  |
    | p-xylene                         | X | X |  |  |

与每种隐式溶剂化方法以及溶剂相关的参数，可以用 `%cpcm` 块输入更精确地定义。
可用选项的完整列表见
[sec:essentialelements.solvationmodels.keyword-list.detailed](#sec:essentialelements.solvationmodels.keyword-list.detailed)。

围绕溶质的空腔类型以及 ORCA 中溶剂化电荷的处理方式，在
[sec:essentialelements.solvationmodels.gaussian_charge](#sec:essentialelements.solvationmodels.gaussian_charge) 和
[sec:essentialelements.solvationmodels.point_charge](#sec:essentialelements.solvationmodels.point_charge) 小节中说明。
ORCA 支持两种溶剂化电荷方案：(i) 点电荷方案，(ii) Gaussian 电荷方案。
从 ORCA 5.0 起，默认的溶剂化方案是带 vdW 型空腔的 Gaussian 电荷方案
（`surfacetype vdw_gaussian`）。较早的 ORCA 版本以
`surfacetype gepol_ses` 和点电荷方案为默认。因此，如果想重现 ORCA 5.0
之前版本得到的结果，请在 `%cpcm` 块中使用标签 `surfacetype gepol_ses`。

不同的电荷方案在
[sec:essentialelements.solvationmodels.gaussian_charge](#sec:essentialelements.solvationmodels.gaussian_charge) 和
[sec:essentialelements.solvationmodels.point_charge](#sec:essentialelements.solvationmodels.point_charge) 小节中描述。
电荷方案与表面不同组合下解析梯度和 Hessian 的可用性见表
[table:CPCM-features](#table:CPCM-features)。

<a id="table:CPCM-features"></a>
!!! note "ORCA 中 C-PCM 内可用的梯度与 Hessian 类型。标签 "YES" 表示该功能已实现，"NO" 表示未实现。为清楚起见，我们用 "\*" 标记 ORCA 中的默认方案（`surfacetype vdw_gaussian`）。"
    |                      |             |            |           |            |           |
    |:--------------------:|:-----------:|:----------:|:---------:|:----------:|:---------:|
    |    `surfacetype`     | 电荷类型    |  梯度      |           |  Hessian   |           |
    |                      |             | 解析       | 数值      | 解析       | 数值      |
    |     `gepol_ses`      |    Point    |    Yes     |    Yes    |    Yes     |    Yes    |
    |     `gepol_sas`      |    Point    |    Yes     |    Yes    |    Yes     |    Yes    |
    |   `vdw_gaussian^*`   |  Gaussian   |    Yes     |    Yes    |    Yes     |    Yes    |
    | `gepol_ses_gaussian` |  Gaussian   |     No     |    Yes    |     No     |    Yes    |

**注 1：** 如果用户想关闭 C-PCM，必须在简单输入中写如下标签：

```orca
! NOCPCM
```

例如，在使用 `$new_job` 特性的串接计算中就需要这样做：
先前的计算涉及溶剂化，但下一个计算要把它关掉。

**注 2：** 如上所述，ORCA 中 C-PCM 的默认是带 vdW 型空腔的 Gaussian
电荷方案。实现遵循参考文献 [garcia_neese_gcs](../../bibliography.md)。因此，
如果在 ORCA 计算中使用 C-PCM，必须把该文献与参考文献 [barone1998](../../bibliography.md)
一同引用。如果请求了 SMD 或 openCOSMO-RS，也必须引用参考文献
[garcia_neese_gcs](../../bibliography.md)，因为这类计算依赖于 C-PCM。

<a id="sec:essentialelements.solvationmodels.gaussian_charge"></a>
### Gaussian 电荷方案的使用

Gaussian 电荷方案避免了传统点电荷面元模型中的 Coulomb 奇异性。
这一方法与开关函数结合使用时，会给出平滑的溶剂化势，
更重要的是给出该量对外部微扰的平滑导数。因此，强烈建议在 C-PCM 中
采用这一方法。Gaussian 电荷方案可与两类溶质空腔表面配合使用：
(1) 缩放 vdW 表面，(2) 溶剂排除表面（SES）。为给不同原子指派半径，
我们遵循参考文献 [lange2010](../../bibliography.md) 提出的方案。即除氢采用 1.1 Å 外，
对所有元素使用 Bondi 半径 [radii_1](../../bibliography.md)。对于元素周期表中 Bondi 半径
未定义的 16 个主族元素，我们采用参考文献 [radii_2](../../bibliography.md) 中 Mantina 等人
提出的半径。这些元素是：Be、B、Al、Ca、Ge、Rb、Sr、Sb、Cs、Ba、Bi、Po、
At、Rn、Fr、Ra。对于 Bondi 和 Mantina 都未涵盖的元素，我们取 2 Å 的半径。

-   **缩放 vdW 空腔**

带缩放 vdW 型空腔的 Gaussian 电荷方案现在是 ORCA 的默认，
因此只需在输入文件的 `%cpcm` 块中添加 C-PCM 标签即可。这对应于
（尽管用户无需写出，因为 ORCA 会在内部处理）：

```orca
%cpcm
  surfacetype vdw_gaussian
end
```

在这种情况下，缩放 vdW 空腔中原子 $I$ 的半径 $R_I$ 计算为

$$

R_I=f_{scal}R_I^{\mathrm{vdW} }

$$

其中 $R_I^{\mathrm{vdW} }$ 是原子 $I$ 的 vdW 半径，$f_{scal}$ 是缩放因子。
按照参考文献 [lange2010](../../bibliography.md) 的建议，该参数默认等于 1.2。
不过，用户可以通过输入文件 `%cpcm` 块中的 `scale_gauss` 标签修改其值。
每个原子的 C-PCM 电荷数使得空腔表面具有约 5.0 个电荷/Å$^2$ 的密度。
这个数大致相当于氢原子上有 110 个点
（110/$(4\pi\times 1.32^2)\approx 5.0$Å$^{-2}$）。ORCA 随后会根据原子半径
选择不同的离散化级别（Lebedev 格点）。该方案称为等密度方案
（isodensity scheme）。氢原子和非氢原子上单位面积电荷数的阈值
可由用户分别通过 `thresh_h` 和 `thresh_noth` 指定。或者，
用户可以请求空腔中每个球固定数目的 Lebedev 点（与球的半径无关）。
这可通过 `num_leb` 标签完成。该参数可取如下值：50、110、194、302、
434、590、770、974 和 1202。ORCA 6.0 之前的版本使用这后一种方案。
该溶剂化方法可用解析梯度以及解析 Hessian。
-   **溶剂排除表面**
GEPOL 生成的 SES 可与 Gaussian 电荷方案配合使用。在这种情况下，
Gaussian 电荷不仅放置在原子球的表面上，也放置在 GEPOL 算法生成的新球的
表面上。要使用这一方法，应如下修改 ORCA 输入文件
```orca
%cpcm
  surfacetype gepol_ses_gaussian
end
```
当溶质被少数几层溶剂显式溶剂化时，一般推荐使用 SES。在这种情况下，
附加的 GEPOL 球可防止溶剂填充显式溶剂分子之间或这些分子与溶质之间的空间。
在溶质 vdW 型表面上滚动以生成 SES 的溶剂球半径由关键词 `rsolv` 控制。
该半径的默认值为 1.30 Å，但用户可通过在 `%cpcm` 块中为 `rsolv`
指定另一个值来更改。所添加 GEPOL 球的最小半径由 `rmin` 控制。
该策略既没有解析梯度也没有解析 Hessian。它们需要数值计算。
由于 GEPOL 球与体系中原子之间的相互依赖性，用 SES 计算的解析梯度
不如用 vdW 型空腔的收敛得平滑（见参考文献 [garcia_neese_gcs](../../bibliography.md)），
并可能导致错误的极小值。Hessian 也受到同样的影响。因此，
ORCA 6.0 不再支持该表面的解析梯度/Hessian，以防止不准确的结果。
<a id="sec:essentialelements.solvationmodels.point_charge"></a>
### 点电荷方案的使用
在该方案中，溶剂化电荷被当作点来处理，并且不使用开关函数来接受/丢弃
构成溶质空腔的球体交界处的电荷。这两个事实导致不连续的势能面
（SCF 能量及其导数的数值不稳定）。因此，在 C-PCM 中不推荐使用点电荷方案。
如果用户仍想使用该电荷方案，它可以与两类不同的溶质空腔表面配合使用：
(1) SES，(2) SAS。
-   **溶剂排除表面**
与 Gaussian 电荷方案配合 SES 一样，该表面通过 GEPOL 算法为点电荷方案
生成。不过，对于 `surfacetype gepol_ses_gaussian`，
表面使用 Lebedev 型格点离散化；而在点电荷方案中，表面被划分为称为
"tesserae" 的球面三角形。细分（tesselation）级别由标签 `ndiv` 控制。
为构建 GEPOL 空腔而对溶质原子使用的半径，是为 COSMO-RS 模型
[cosmors_radii](../../bibliography.md) 优化的 H、C、N、O、F、S、Cl、Br 和 I 的半径，
其余元素则使用缩放的 Bondi 半径。
要把点电荷方案与 SES 配合使用，应在 `%cpcm` 块中添加如下标签：
```orca
%cpcm
  surfacetype gepol_ses
end
```
-   **溶剂可及表面**
这里，溶质空腔的表面是通过跟踪一个半径为 `rsolv`（代表溶剂分子）的球
在溶质 vdW 表面上滚动的中心生成的。所得表面的离散化通过 tesserae 完成，
与 SES 的做法相同。要把点电荷方案与 SAS 配合使用，应在 `%cpcm` 块中
添加如下标签：
```orca
%cpcm
  surfacetype gepol_sas
end
```
-   **如何规避点电荷方案中的数值不稳定**
由于电荷的"点"性质，以及在构成溶质空腔的球体交界处不考虑开关函数，
数值不稳定在点电荷方案中是隐含的。同时，无法事先预测 SCF 能量和/或
其导数中是否会出现不连续。不过，如果用户仍想使用该电荷方案——
无论哪种表面（SES 或 SAS）——有两件事可以尝试以尽量减少上述问题：
-   [**改变 `ndiv`**]{.underline}：参数 `ndiv` 控制溶质空腔中每个球的
    三角形数目。改变三角形数目也改变了球体交界处的三角形数目，
    从而可以解决两个点电荷靠得太近、使公式 [Eq](#eq:Aijp) 中的
    $A_{ij}$ 元发散（以及溶剂化电荷突然变得非常大）的那些情形。
    不过，这一策略可能对某个特定情形有效，但永远不能保证对于同一
    体系的另一几何结构不会出现 SCF 能量的不连续
    （因为它并不防止点电荷彼此过于接近）。
-   [**增大 `pmin`**]{.underline}：该参数移除彼此距离小于 `pmin` 的电荷。
    `pmin` 的默认值为 0.1 原子单位（$\approx 0.0529$ Å）。
    通过增大 `pmin`，可以移除球体交界处彼此靠得太近的所有电荷对。
    **注意：** 增大 `pmin` 时要小心。虽然它可以防止 SCF 能量的突跳，
    但也可能导致"有偏地"处理溶质-溶剂相互作用，
    因为你正在移除相当数量的代表溶剂效应的电荷。
### C-PCM 中溶剂化自由能的计算
溶剂化自由能（solvation free energy）$\Delta G_{solv}$ 定义为溶质从气相
转移到凝聚相的自由能。该量可以写成（见参考文献 [garcia_neese_gcs](../../bibliography.md)
中的公式 27）

$$

\Delta G_{solv}=E_{solv}(\vec{R}_l,\vec{R}_v)+\Delta G_{el}+\Delta G_{cav}+\Delta G_{disp}\qquad \text{(eq_g_solv)}

$$

第一项 $E_{solv}(\vec{R}_v,\vec{R}_l)$ 对应于气相哈密顿量在液相的期望值
$E(\vec{R}_l)$ 与气相势能面 $E(\vec{R}_v)$ 之差

$$

E_{solv}(\vec{R}_v,\vec{R}_l)=E(\vec{R}_l)-E(\vec{R}_v)

$$

公式 [Eq](#eq_g_solv) 中的第二项计入对 $\Delta G_{solv}$ 的电子极化贡献，
由分布在溶质空腔（vdW 型或 SES）表面上的电荷计算。
最后，$\Delta G_{cav}$ 是空腔化能（cavitation energy），即为容纳溶质而在
溶剂体相内创建空腔所需的可逆功；而 $\Delta G_{disp}$ 计入溶剂化溶质时
色散能发生的变化。这后两项之和对应于对 $\Delta G_{solv}$ 的非静电贡献
$\Delta G_{nel}$

$$

\Delta G_{nel}=\Delta G_{cav}+\Delta G_{disp}

$$

在 ORCA 中，如果体系在 C-PCM 中被溶剂化（在输入文件中定义
`!CPCM(solvent name)`，无论点电荷方案还是 Gaussian 电荷方案），
则 SCF 能量及其导数都没有"非静电溶剂化贡献"。为粗略了解
$\Delta G_{nel}$ 的取值，可以通过文献中由实验数据得到的经验公式来估计。
例如，$\Delta G_{nel}$ 可由直链烷烃的水合自由能来估计 [truong1995](../../bibliography.md)

$$

\Delta G_{\text{nel} } = 1.321 + 0.0067639\times\mathrm{SASA}\qquad \text{(eq:delta_truong)}

$$

其中 SASA 是溶剂可及表面积（solvent-accessible surface area）。
不过，尽管公式 [Eq](#eq:delta_truong) 对水中的有机分子可能给出
$\Delta G_{nel}$ 的良好估计，但在考虑水以外的溶剂（以及水中的许多溶质）时，
它对非静电溶剂化效应是一个糟糕的近似。要在 ORCA 计算中包含非静电
溶剂化效应，可以采用该近似的两种替代方案：

1.  把 SMD 模型与 C-PCM 结合使用（见
    [sec:essentialelements.solvationmodels.smd.detailed](#sec:essentialelements.solvationmodels.smd.detailed) 一节）。
    这是量子化学界最常采用的策略。

2.  用 Gaussian 电荷计算对 $\Delta G_{solv}$ 的静电贡献，
    再配以一个由溶质原子对 SASA 的贡献计算的
    $\Delta G_{\text{nel} }$ 公式。[garcia_neese_gcs](../../bibliography.md)

着眼于第二种策略，空腔化能 $\Delta G_{cav}$ 通过 Pierotti 和 Claverie
提出的公式计算。[pierotti1976,claverie1978](../../bibliography.md) 在这种情况下，
$\Delta G_{cav}$ 按溶质球半径 $R_I$ 与溶剂球半径 $R_S$ 之比
$\overline{\mathbf{R} }$ 的幂次展开。于是，以原子 $I$ 为中心的溶质球的
空腔化能写作

$$

\Delta G_{cav,I}=-\mathrm{ln}(1-y)+\left(\frac{3y}{1-y}\right)\overline{\mathbf{R} }+\left[\frac{3y}{1-y}+\frac{9}{2}\left(\frac{y}{1-y}\right)^2\right]\overline{\mathbf{R} }^2+\frac{yP}{\rho_Sk_BT}\overline{\mathbf{R} }^3

$$

其中 $y=8\pi\rho_SR_S^3/6$，$\rho_S$ 是溶剂密度，
$\overline{\mathbf{R} }=R_I/R_S$，$T$ 是温度，$P$ 是压力。
如果我们考虑溶剂可及表面（SAS），则总的 $\Delta G_{cav}$ 是各
$\Delta G_{cav,I}$ 按依赖于球 $I$ 暴露的 $\mathrm{SASA}_I$ 的因子加权之和

$$

\Delta G_{cav}=\sum_{i=1}^{N_{\mathrm{sph} }}\frac{\mathrm{SASA}_I}{4\pi R_I^2}\Delta G_{cav,I}=\sum_{i=1}^{N_{el} }\frac{\mathrm{SASA}_i}{4\pi R_I^2}\Delta G_{cav,i}\qquad \text{(eq_g_cav)}

$$

这里，对构成 SAS 的球总数（$N_{\mathrm{sph} }$）的求和，
被替换为对 SAS 所划分的面元总数（$N_{\mathrm{el} }$）的求和。

关于 $\Delta G_{disp}$，该量假定与每个面元对 SASA 的贡献呈线性关系

$$

\Delta G_{disp}=\sum_{i=1}^{N_{\mathrm{el} }}\sigma_I\mathrm{SASA}_i\qquad \text{(eq_g_disp)}

$$

这里，因子 $\sigma_I$ 是面元 $i$ 所属球 $I$ 的原子表面张力。

这一考虑公式 [Eq](#eq_g_cav) 和 [Eq](#eq_g_disp) 来计算
$\Delta G_{nel}$ 的策略，假定用 Gaussian 电荷计算公式 [Eq](#eq_g_solv)
中的 $\Delta G_{el}$。当用 vdW 型空腔来计入静电溶剂化效应时，
该溶剂化方法称为 GVDW_nel；而当使用 SES 型空腔时，我们称该溶剂化方法为
GSES_nel（"G" 代表 Gaussian 电荷，"nel" 因为包含了非静电溶剂化效应）。
GVDW_nel 和 GSES_nel 模型的细节见参考文献 [garcia_neese_gcs](../../bibliography.md)。

GVDW_nel 和 GSES_nel 模型已针对含 H、C、N 和 O 原子的溶质，
在如下溶剂中参数化：苯、氯仿、环己烷、辛醇、甲苯和水。
公式 [Eq](#eq_g_disp) 中 $\sigma_I$ 原子表面张力的参数，
以及生成 SAS 所用溶剂分子的半径 $R_S$，见参考文献 [garcia_neese_gcs](../../bibliography.md)。
GVDW_nel 和 GSES_nel 的使用由在 `%cpcm` 块中添加的字符串 `cds_cpcm`
控制。在这两个模型中该标志应等于 2（默认情况下，
当使用 C-PCM 与 Gaussian 电荷方案而不含非静电溶剂化效应时，
`cds_cpcm` 等于 0）。要为 GVDW_nel 方案计算 $\Delta G_{solv}$，
必须执行如下步骤：

1.  在真空中优化溶质（本例中为苯甲醚）的几何结构。
    对于 B3LYP/def2-TZVP 理论水平的 DFT 计算（带 RIJCOSX），
    我们的输入文件如下：

    ```orcainput
    ! B3LYP def2-TZVP D3BJ tightopt

    %maxcore 4000

    * xyz 0 1
    C   0.66588156410505    1.19833878437922    -0.02647672759883
    C   1.95470174000504    0.69483871574862    -0.01927812843331
    C   2.17893173780041   -0.68097630146538     0.00933914777704
    C   1.09270919891774   -1.54252176637089     0.03141990372830
    C  -0.21073409652496   -1.05179390481975     0.02471602253843
    C  -0.42517201252444    0.32533458015547    -0.00499572635290
    H   0.47565631823749    2.26336213776820    -0.05012843684387
    H   2.79210971512409    1.38085300778245    -0.03749594945361
    H   3.18771596563920   -1.07149825338966     0.01433233618265
    H   1.25061585302875   -2.61357041387417     0.05495238973649
    H  -1.03877793934640   -1.74453554370491     0.04346162651229
    O  -1.65366310927299    0.90979347913477    -0.01693978807213
    C  -2.79791686738707    0.07370821312998     0.01117694976431
    H  -2.83142307710305   -0.58944196707467    -0.85867919998175
    H  -3.65619850989594    0.74176224021803    -0.00958531946332
    H  -2.82883648080292   -0.53125300761732     0.92288089996024
    *
    ```

2.  把所得结构（`anisole.xyz`）用作后续溶液中几何优化的输入结构。
    本例中我们考虑水作为溶剂。输入文件如下：

    ```orcainput
    ! B3LYP def2-TZVP D3BJ tightopt CPCM(Water)

    %cpcm
      cds_cpcm 2
    end

    %maxcore 4000

    * xyzfile 0 1 anisole.xyz

    ```

3.  在溶剂化体系的输出文件中查找 `FINAL SINGLE POINT ENERGY`
    （我们记作 $E_s$）：

    ```orca
    -------------------------   --------------------
    FINAL SINGLE POINT ENERGY      -346.723542928703
    -------------------------   --------------------
    ```

4.  在真空体系的输出文件中查找 `FINAL SINGLE POINT ENERGY`
    （我们记作 $E_0$）：

    ```orca
    -------------------------   --------------------
    FINAL SINGLE POINT ENERGY      -346.719657761697
    -------------------------   --------------------

    ```

5.  计算 $\Delta G_{solv}=E_s-E_0=-0.003885$ 原子单位。若换算为 kcal/mol
    并四舍五入到两位小数，得 $\Delta G_{solv}=-2.44$ kcal/mol。
    该量与实验值（-2.45 kcal/mol[marenich2009](../../bibliography.md)）非常吻合。

6.  如果用户对 $\Delta G_{nel}$ 的取值感兴趣，该量打印在
    `CPCM Solvation Model Properties` 块中：

    ```orca
    CPCM Solvation Model Properties:
    Surface-charge          :  -0.02580688416088
    Corrected charge        :   0.00000000000000
    Outlying charge corr.   :   0.00005046206545 Eh    0.00137 eV
    Free-energy (cav+disp)  :   0.00272597402638 Eh    0.07418 eV
    ```

这里 $\Delta G_{nel}$ 对应于 `Free-energy (cav+disp)`，
通过公式 [Eq](#eq_g_cav) 和 [Eq](#eq_g_disp) 计算。
称为 `Surface-charge` 的项对应于位于 C-PCM 空腔之外的溶质净电荷。
它基本上是 C-PCM 电荷之和（不含 $f(\varepsilon)$ 的标度）。
这些过剩电荷对能量和 C-PCM 电荷本身的影响可通过所谓的外部电荷校正
（outlying charge correction）来修正。在 ORCA 中，该校正通过一个基于
Lagrange 的算法计算 [pye1999](../../bibliography.md)，但仅作信息打印。即外部电荷效应
既不加到 SCF 能量上，也不加到其导数上。无论如何，校正后的总电荷打印在
`Corrected charge` 中，而能量的校正项打印在 `Outlying charge corr.` 中。
为进一步帮助用户，ORCA 还会打印一个扩展名为 `.cpcm_corr` 的文件，
其中给出校正后的 C-PCM 电荷。

如果想改用 GSES_nel 模型，只需在 `%cpcm` 块中添加
`surfacetype` `gepol_ses_gaussian`。

**[注意：]{.underline}** GVDW_nel 和 GSES_nel 模型没有解析 Hessian，
因为 $\Delta G_{nel}$ 对核位移的二阶导数尚未实现。

### 计算 CPCM 各项的选项

在 CPCM 计算中有三个主要步骤。第一步是计算量子对象在表面格点上产生的
静电势。这一步的特征是：

$$

V\left( \mathbf{r}_{g} \right) = \sum_{A}^{}\frac{Z_{A}}{\left| \mathbf{R}_{A} - \mathbf{r}_{g} \right|} - \sum_{\mu\nu}^{}P_{\mu\nu}\int_{}^{}{\frac{\mu(\mathbf{r})\nu(\mathbf{r})}{\left| \mathbf{r} - \mathbf{r}_{g} \right|}d\mathbf{r}}

$$
$$

= \sum_{A}^{}\frac{Z_{A}}{\left| \mathbf{R}_{A} - \mathbf{r}_{g} \right|} - \sum_{\mu\nu}^{}P_{\mu\nu}\left( \mu\nu|g \right)

$$

第一个求和遍历原子核，第二个遍历基函数。计算的第二步是把表面势转换为
表面屏蔽电荷 **q**。我们在此不写出它，因为这一步对 CPCM 的每个变体
略有不同。简言之，它涉及求解一个维数为表面分段数的线性方程组，
通常通过 Cholesky 分解完成。
第三步是把表面电荷与量子电子的相互作用求和到 Fock 矩阵中。这一步为：

$$

F_{\mu\nu}^{(CPCM)} = - \sum_{g}^{}q_{q}\int_{}^{}{\frac{\mu\left( \mathbf{r} \right)\nu\left( \mathbf{r} \right)}{\left| \mathbf{r} - \mathbf{r}_{g} \right|}d\mathbf{r}}

$$
$$

= - \sum_{g}^{}q_{q}\left( \mu\nu|g \right)

$$

这里的求和遍历带表面屏蔽电荷 $q_g$ 的表面分段。
这些计算中耗时的步骤是三中心静电积分 $(\mu\nu | g)$ 的计算。
默认情况下，这些积分使用 SHARK 提供的高效解析积分计算。不过还有如下
替代方案：
1)  积分可通过数值积分求值
2)  势和 Fock 矩阵贡献可分别使用 RI 密度和 RI 近似求值
3)  势和 Fock 矩阵元可使用积分的多极近似求值
这些选项由以下方式触发：
```orca
%cpcm UseAnalyticOnRebuild true # if true, full Fock matrix builds
                                # are done with analytic integrals
                                # (strongly recommended)
Vopt v_analytic
 # = v_multipole
 # = v_RI
 # = v_numeric
Fopt f_analytic
 # = f_multipole
 # = f_RI
 # = f_numeric
```
!!! note "注意"
    -   我们的经验表明，解析积分仍然是最安全、最准确的选项。
    -   解析积分将胜过数值积分或多极近似
    -   RI 近似可以实现一些节省，但也可能引入不可忽略的误差。
<a id="sec:essentialelements.solvationmodels.cosmo.detailed"></a>
## 类导体屏蔽溶剂化模型（COSMO）
!!! note "注意"
    COSMO 溶剂化模型已从 ORCA v4.0.0 中移除！！！
    *如有需要，请把 C-PCM 溶剂化模型与 COSMO epsilon 函数配合使用！*
    作为使用带 COSMO epsilon 函数的 C-PCM 模型的简写，
    你可以通过 `!CPCMC(solvent)` 指定溶剂。
<a id="sec:essentialelements.solvationmodels.smd.detailed"></a>
## SMD 溶剂化模型
SMD 溶剂化模型由 Cramer 和 Truhlar 小组提出 [marenich2009](../../bibliography.md)，
它基于溶质分子的量子力学电荷密度与溶剂的连续介质描述之间的相互作用。
在该模型中使用完整的溶质电子密度而不定义分原子电荷，溶剂也不显式表示，
而是作为在溶质-溶剂边界处具有表面张力的介电介质。SMD 是一个普适的
溶剂化模型，即它适用于任何带电或不带电的溶质、任何溶剂或液体介质，
只要已知几个关键描述符。特别是这些描述符为介电常数、折射率、
体相表面张力以及酸性和碱性参数。忽略浓度贡献，该模型把可观测的溶剂化
自由能分为两个主要分量，

$$

\Delta G_{\mathrm{S} } = \Delta G_{\mathrm{ENP} } + \Delta G_{\mathrm{CDS} }.\qquad \text{(eq_smdg)}

$$

在 ORCA 中，第一项是来自自洽反应场处理的体相静电贡献，
涉及使用类导体可极化连续介质模型（C-PCM）的静电相互作用。
不过半径被设为"本征原子 Coulomb 半径"。第二项称为空腔-色散-溶剂结构
（cavity-dispersion solvent-structure, CDS）项，是溶质与第一溶剂化壳层中
溶剂分子之间短程相互作用产生的贡献。该贡献是若干项之和，
这些项（其比例常数称为原子表面张力，与几何结构有关）与溶质各原子的
溶剂可及表面积成正比。CDS 对溶剂化自由能的贡献为

$$

\Delta G_{\mathrm{CDS} }=\sum_{k}^{\text{atoms} }\sigma_{k}A_{k}(\textbf{R},{R_{Z_{k} }+r_{s} }) + \sigma^{\mathrm{[M]} }\sum_{k}^{\text{atoms} }A_{k}(\textbf{R},{R_{Z_{k} }+r_{s} }),

$$

其中 $\sigma_{k}$ 和 $\sigma^{\mathrm{[M]} }$ 分别是原子 $k$ 的原子表面张力
和分子表面张力，$A_{k}$ 是溶剂可及表面积（SASA）。SASA 依赖于几何结构
**R**、所有原子 van der Waals 半径的集合 ${R_{Z_{k} }}$，以及加到每个
原子 van der Waals 半径上的溶剂半径 $r_{s}$。程序中对 CDS 贡献使用
Bondi 半径。
更多细节见 Marenich 等人的原始论文 [marenich2009](../../bibliography.md)，
在使用 SMD 计算结果的出版物中应当引用该文
（连同参考文献 [garcia_neese_gcs](../../bibliography.md)，它描述了 SMD 所用的
ORCA 中 C-PCM 的实现）。
SMD 可用于单点计算和几何优化，使用单行列式 SCF（HF 和 DFT）以及 CASSCF
方法。在后 SCF 方法中，结果在参考波函数处校正。SMD 溶剂化模型通过
输入文件中的如下方式调用
```orca
! SMD(solvent)
```
其中 `solvent` 是 SMD 库中 179 种溶剂之一（见表
[table:list-solvents](#table:list-solvents)）。或者，可以通过 `%cpcm` 块请求 SMD 模型，
写法为：
```orca
%cpcm
  smd true             # turn on SMD
  SMDsolvent "solvent" # specify the name of solvent from the list
end
```
无论用户以何种方式调用 SMD 模型，ORCA 都会自动为所选溶剂设置若干默认的
SMD 参数。如有需要，用户也可以在 `%cpcm` 块中手动指定 SMD 计算中所用的
溶剂描述符。
```orca
%cpcm
  soln      # index of refraction at optical frequencies at 293 K
  soln25    # index of refraction at optical frequencies at 298 K
  sola      # Abraham's hydrogen bond acidity
  solb      # Abraham's hydrogen bond basicity
  solg      # relative macroscopic surface tension
  solc      # aromaticity, fraction of non-hydrogenic solvent atoms
            # that are aromatic carbon atoms
  solh      # electronegative halogenicity, fraction of non-hydrogenic
            # solvent atoms that are F, Cl, or Br
 end
```
考虑如下被水溶剂化的水分子输入，
```orcainput
! B3LYP def2-SVP tightscf SMD(water)
* xyz 0 1
O  -0.00000018976103    0.00606010894837    0.00000000004527
H   0.76098169249695   -0.58891312953082   -0.00000000000022
H  -0.76098151333900   -0.58891299029372   -0.00000000000022
*
```
在 SCF 部分开始之前，程序打印 SMD 信息。该部分如下：
```orca
--------------------
CPCM SOLVATION MODEL
--------------------
CPCM parameters:
  Epsilon                                         ...      78.3550
  Refrac                                          ...       1.3328
  Rsolv                                           ...       1.3000
  Surface type                                    ... GAUSSIAN VDW
  Discretization scheme                           ... Constant charge density
    Threshold for H atoms                         ...       5.0000 (charges/Ang^2)
    Threshold for non-H atoms                     ...       5.0000 (charges/Ang^2)
  Epsilon function type                           ...         CPCM
Solvent:                                          ... WATER
SMD-CDS solvent descriptors:
  Soln                                            ...       1.3328
  Soln25                                          ...       1.3323
  Sola                                            ...       0.0000
  Solb                                            ...       0.0000
  Solg                                            ...       0.0000
  Solc                                            ...       0.0000
  Solh                                            ...       0.0000
Radii:
  Scheme                                          ... Element-dependent radii
  Radius for O  used is    2.8724 Bohr (=   1.5200 Ang.)
  Radius for H  used is    2.2677 Bohr (=   1.2000 Ang.)
Calculating surface                               ...        done! (  0.0s)
Cavity surface points                             ...          244
Cavity Volume                                     ...     130.0616
Cavity Surface-area                               ...     129.3354
Calculating surface distance matrix               ...        done! (  0.0s)
Performing Cholesky decomposition & store         ...        done! (  0.0s)
Overall time for CPCM initialization              ...                 0.0s
```
SCF 收敛后，打印 SMD 对总能量的贡献（该项标记为 "SMD CDS" 项）。
```orca
               *****************************************************
               *                     SUCCESS                       *
               *           SCF CONVERGED AFTER  10 CYCLES          *
               *****************************************************
Recomputing exchange energy using gridx3       ... done (    0.056 sec)
Old exchange energy                            :     -1.791736873 Eh
New exchange energy                            :     -1.791694663 Eh
Exchange energy change after final integration :      0.000042211 Eh
Total energy after final integration           :    -76.335230273 Eh
SMD CDS free energy correction energy :                 1.44927     Kcal/mol
Total Energy after SMD CDS correction =               -76.332920707 Eh
             **** ENERGY FILE WAS UPDATED (water.en.tmp) ****
----------------
TOTAL SCF ENERGY
----------------
Total Energy       :        -76.33292070695327 Eh           -2077.12437 eV
Components:
Nuclear Repulsion  :          9.11286213981824 Eh             247.97359 eV
Electronic Energy  :        -85.43200537714571 Eh           -2324.72305 eV
One Electron Energy:       -123.06209110061025 Eh           -3348.68974 eV
Two Electron Energy:         37.63008572346453 Eh            1023.96669 eV
CPCM Dielectric    :         -0.01612924659271 Eh              -0.43890 eV
SMD CDS (Gcds)     :          0.00230956608299 Eh               0.06285 eV
```
在 ORCA 中，用户也可以请求 SMD18 模型 [engelageSMD18](../../bibliography.md)，
它涉及对溴和碘的改进半径（用于构建 C-PCM 部分所用空腔的半径）。
SMD18 模型被证明能准确描述溶液中的卤键（Halogen-bonding）相互作用。
它通过简单输入中的 `SMD18` 标签请求：
```orca
! SMD(solvent) SMD18
```
或通过 `%cpcm` 块：
```orca
%cpcm
  SMD18 true  # default = false
end
```
**[注：]{.underline}**
-   如果对使用 SMD 模型计算溶剂化自由能感兴趣，只需按公式
    [Eq](#eq_smdg) 计算 $\Delta G_{\mathrm{S}}$ 即可。不过这里应当注意，
    SMD 模型在气相和溶液相中考虑相同的浓度（1 mol/L）。
    因此，如果考虑 1 atm 的气相标准态，而我们想把计算的
    $\Delta G_{\mathrm{S} }$ 与实验值比较，就必须给计算的
    $\Delta G_{\mathrm{S} }$ 加上一个等于 1.89 kcal/mol 的浓度项。
<a id="sec:essentialelements.solvationmodels.draco"></a>
## 连续溶剂化的动态半径调整（DRACO）
DRACO 方案是一种改进隐式溶剂化模型性能的方法，
特别是提高计算的溶剂化自由能的精度。[Plettdraco2024](../../bibliography.md)
它基于对描述溶质空腔的原子/球的原始静态半径进行动态标度。
在该方法中，原子 $i$ 的原始半径 $r_i$ 按下式标度

$$

r_{i\text{scale}} = f_{i\text{scale}}r_i\qquad \text{(eq_dracosc)}

$$

其中标度因子 $f_{i\text{scale}}$ 由下式确定

$$

f_{i\text{scale}} = \text{erf}(a_Z(q_{\text{eff},i}-b_Z)) + 1\qquad \text{(eq_dracof)}

$$

这里 $q_{\text{eff},i}$ 对应于有效分电荷，定义为

$$

q_{\text{eff},i} = q_i + k_Zq_i\text{CN}_i\qquad \text{(eq_dracoq)}

$$

其中 $q_i$ 是原子分电荷。参数 $a_Z$、$b_Z$ 和 $k_Z$ 是元素特定的参数，
$\text{CN}_i$ 是分数配位数（fractional coordination number）。

对于氧原子，$f_{i\text{scale}}$ 通过一个依赖于 Abraham 氢键酸度（$\alpha$）
的项来校正：

$$

f_{i\text{scale}}^{\text{O}} = f_{i\text{scale}} +c_{\text{O}}(0.43-\alpha)\qquad \text{(eq_dracoo)}

$$

其中 $c_{\text{O}}$ 是对纯 C-PCM 或 SMD 不同的参数。公式
[Eq](#eq_dracoo) 中的校正仅对 $\alpha<0.43$ 的溶剂应用。

DRACO 已针对 C-PCM 和 SMD，在如下溶剂中参数化：乙腈、DMSO、甲醇和水。
公式 [Eq](#eq_dracof)、[Eq](#eq_dracoq) 和 [Eq](#eq_dracoo) 中的元素特定参数
可在 <https://github.com/grimme-lab/DRACO> 获取。

DRACO 与 C-PCM 或 SMD 的配合使用通过简单输入中的如下标签触发：

```orca
! CPCM(solvent) DRACO
```

或

```orca
! SMD(solvent) DRACO
```

也可以在 `%cpcm` 块中请求：

```orca
%cpcm
  DRACO true
end
```

在 ORCA 中，计算公式 [Eq](#eq_dracoq) 中分电荷的默认方案是电负性均衡
（electronegativity-equilibration, EEQ）电荷模型（D4 情形）
[caldeweyher2019](../../bibliography.md)。不过也可以请求 Charge Extended Hückel（CEH）
模型。[grimme2023AOmin](../../bibliography.md) DRACO 内的电荷方案由 `%cpcm` 块中的
如下标签控制：

```orca
%cpcm
  draco_charges ceh  # default = eeq
end
```

如果请求 CEH 电荷，ORCA 需要运行一次 XTB 计算来生成它们。
这里应当至少有 XTB 6.7.1 版（较早版本不会生成 CEH 电荷，
见 [sec:programs.general](#sec:programs.general) 一节）。关于公式 [Eq](#eq_dracoq) 中的
分数配位数，它按 GFN2-XTB 计算中所述的方式计算。[grimme2019xtb](../../bibliography.md)

DRACO 可用于单点能量计算（CEH 和 EEQ 电荷均可）和几何优化（用 EEQ 电荷）
[wittmann2025draco](../../bibliography.md)。DRACO 对解析 Hessian 的贡献尚未实现。
在这种情况下，用户应请求 `numfreq`。

请注意，请求 DRACO 的计算涉及一种基于每球固定电荷数的空腔表面离散化方案。
默认是 194 个 Lebedev 点。这与不带 DRACO 的 C-PCM/SMD 计算所用的方案
不同，后者的默认是等密度方案，如
[sec:essentialelements.solvationmodels.gaussian_charge](#sec:essentialelements.solvationmodels.gaussian_charge) 一节所讨论。
这一选择是必要的，特别是对于几何优化。对于 DRACO，空腔中球的半径在
每个优化步都会变化。因此，如果 ORCA 默认为 DRACO 使用等密度方案，
每个原子相关的 Lebedev 格点可能在两个连续步骤之间改变，
导致总能量及其梯度的不连续。不过，对于涉及 DRACO 的计算，
仍可通过 `%cpcm` 块中的标签 `DRACOisodens` 请求等密度方案：

```orca
%cpcm
  dracoisodens true  # default = false
end
```

<a id="sec:essentialelements.solvationmodels.opencosmors"></a>
## OpenCOSMO-RS

ORCA 与 openCOSMO-RS 相接口 [gerlachcosmors2022,Muellercosmors2025](../../bibliography.md)，
它是 COSMO-RS 模型 [cosmors_1995,cosmors_1998](../../bibliography.md) 的一个开源实现。
该模型在学术界和工业界被广泛用于预测流体相热力学。

COSMO-RS 背后的主要思想是：液相中分子之间的相互作用可以描绘为一组相互
作用的表面分段（surface segments）的系综。表面分段上的性质通过溶质和
溶剂在完美导体（$\epsilon = \infty$）中的 QM 计算得到，
而分段之间的相互作用自由能是一组描述符的函数。其中最相关的是
屏蔽电荷密度（screening charge density, $\sigma$）。

ORCA 中所用 COSMO-RS 模型的完整说明见参考文献
[gerlachcosmors2022,Muellercosmors2025](../../bibliography.md)，代码可在
<https://github.com/TUHH-TVT> 获取。特别是，ORCA 6.0 的参数化称为
openCOSMO-RS 24a。相应的可执行文件随 ORCA 6.0 二进制文件一同发布，
名为 `openCOSMORS`。ORCA 会在需要时在内部调用该可执行文件。

ORCA 中的 COSMO-RS 计算是一种特殊类型的计算。通过请求 COSMO-RS，
ORCA 为溶质和溶剂各运行一组单点能量计算，然后调用 openCOSMO-RS
可执行文件，后者接收溶质和溶剂的输入几何结构，并计算溶质在溶剂中的
溶剂化自由能。在 ORCA 中请求 COSMO-RS 的计算工作流程如下：

1. 溶质在气相中的单点能量计算
2. 溶质在导体中（$\epsilon = \infty$）的单点能量计算
3. 溶剂在导体中（$\epsilon = \infty$）的单点能量计算
4. 通过 openCOSMO-RS 可执行文件做 COSMO-RS 并计算溶剂化性质

第 1 至 3 点对应于 BP86/def2-TZVPD 水平的 DFT 计算。这是为 ORCA 6.0
参数化 COSMO-RS 所用的理论水平。如下文所示，用户可以更换泛函和基组，
但不推荐！

关于计算 2 和 3，为产生平滑的 $\sigma$ 轮廓，ORCA 丢弃面积 < 0.01 Å$^2$
的表面分段。对于这两项计算，用于构建溶质和溶剂空腔的若干元素的半径
与非 COSMO-RS 计算（使用 C-PCM）中采用的默认值不同。这是因为所提供的
openCOSMO-RS 二进制文件涉及为 ORCA 6.0 做的 COSMO-RS 特殊参数化，
这不仅影响 COSMO-RS 参数，也影响 C-PCM 部分中若干元素的半径。

第 4 点完成后，溶质在溶剂中的溶剂化自由能（$\Delta G_{\mathrm{S}}$）
打印在 ORCA 输出文件中。在 ORCA 6.0 中，openCOSMO-RS 的使用仅限于
$\Delta G_{\mathrm{S}}$ 的计算。

<a id="sec:essentialelements.solvationmodels.usecosmors"></a>
### 如何运行 ORCA/COSMO-RS 计算
ORCA/COSMO-RS 计算通过 `%cosmors` 块控制。这类计算需要两个输入结构，
一个用于溶质，一个用于溶剂。溶质坐标在输入文件中提供，与任何其他类型的
计算相同。不过关于溶剂的结构，有两个选项：

1. 从数据库检索溶剂结构
2. 在单独的文件中提供结构

要用策略 1，我们需要通过如下方式请求溶剂：

```orca
COSMORS(Solvent)
```

在简单输入中，或使用 `%cosmors` 块：

```orca
%cosmors
  solvent "Solvent"
end
```

ORCA 中可用的内置溶剂列表见 [table:list-solvents](#table:list-solvents)。例如，
对于被乙腈溶剂化的水分子，输入文件如下：

```orcainput
!COSMORS(Acetonitrile)
* xyz 0 1
O    0.00000006589375       0.00157184228646       0.00000000004493
H    0.77316868532439      -0.58666889665624      -0.00000000000005
H   -0.77316876182122      -0.58666895650640      -0.00000000000005
*
```

如果用户想为溶剂提供结构（策略 2），则应有一个扩展名为
**.cosmorsxyz** 的单独文件。该文件的名称（不含扩展名）由 `%cosmors`
块中的标签 `solventfilename` 控制。例如，如果想计算丙酮在水中的溶剂化
自由能，ORCA 输入文件如下：

```orcainput
%cosmors
  solventfilename "water"
end

* xyz 0 1
H    1.99757808828569      0.25022586507917      0.72957579847856
C    1.44666788654273      0.06088176074125     -0.18975506731892
H    1.67115809398389      0.82690156694531     -0.93346420198265
H    1.76410010378270     -0.89580894800398     -0.61702931492419
C   -0.03218812888253     -0.00668250402989      0.08117960952503
O   -0.47126229461002     -0.06383203315654      1.21590571064657
C   -0.93671505604705     -0.00759565576779     -1.12174123739234
H   -0.88761294036774      0.97611724740670     -1.59852429171257
H   -0.58940208311204     -0.73299176093053     -1.85998395179737
H   -1.96332366957567     -0.22151553828368     -0.83026305352213
*
```

溶剂（水）的结构是 `water.cosmorsxyz` 文件中的那个：

```orca
3
0 1
O    0.00000006589375       0.00157184228646       0.00000000004493
H    0.77316868532439      -0.58666889665624      -0.00000000000005
H   -0.77316876182122      -0.58666895650640      -0.00000000000005
```

其中第一行对应于原子数，第二行给出电荷和多重度。

COSMO-RS 的输出打印在 ORCA 输出文件中 `OPENCOSMO-RS CALCULATION` 行之后。
首先打印关于理论水平、溶质和溶剂的信息。对于上面的例子（水中的丙酮），如下：

```orca
------------------------------------------------------------------------------
                          OPENCOSMO-RS CALCULATION
------------------------------------------------------------------------------

----------------------
GENERAL INFORMATION
----------------------
Calculation method                          ... DFT
Functional                                  ... BP86
Basis set                                   ... DEF2-TZVPD

----------------------
SOLUTE INFORMATION
----------------------
Number of atoms                             ...     10
Total charge                                ...      0
Multiplicity                                ...      1

CARTESIAN COORDINATES (ANGSTROEM)
  H      1.997578    0.250226    0.729576
  C      1.446668    0.060882   -0.189755
  H      1.671158    0.826902   -0.933464
  H      1.764100   -0.895809   -0.617029
  C     -0.032188   -0.006683    0.081180
  O     -0.471262   -0.063832    1.215906
  C     -0.936715   -0.007596   -1.121741
  H     -0.887613    0.976117   -1.598524
  H     -0.589402   -0.732992   -1.859984
  H     -1.963324   -0.221516   -0.830263

----------------------
SOLVENT INFORMATION
----------------------
Solvent name                                ... water
Number of atoms                             ...      3
Total charge                                ...      0
Multiplicity                                ...      1

CARTESIAN COORDINATES (ANGSTROEM)
  O      0.000000    0.001572    0.000000
  H      0.773169   -0.586669   -0.000000
  H     -0.773169   -0.586669   -0.000000
```

这些行之后，ORCA 打印每个 QM 计算的最终单点能量，
以及 ORCA 输出被重定向到的输出文件：

```orca
----------------------------------------------
Single Point Calculation (solute / gas-phase)
----------------------------------------------
Output single point calculation redirected to >test.solute_vac.lastout

FINAL SINGLE POINT ENERGY (Solute-gas-phase)     -193.233975714789

----------------------------------------------
Single Point Calculation (solute / CPCM)
----------------------------------------------
Output single point calculation redirected to >test.solute_cpcm.lastout

FINAL SINGLE POINT ENERGY (Solute-CPCM)     -193.243987123912

----------------------------------------------
Single Point Calculation (solvent / CPCM)
----------------------------------------------
Output single point calculation redirected to >test.solvent_cpcm.lastout

FINAL SINGLE POINT ENERGY (Solvent-CPCM)      -76.479155022866
```

该信息打印后，ORCA 调用 openCOSMO-RS 可执行文件，
$\Delta G_{\mathrm{S}}$ 打印在如下块中：

```orca
----------------------
SOLVATION DATA
----------------------
Reference temperature             :          298.15 K
Free energy of solvation (dGsolv) : -0.006626234385 Eh   -4.158026 kcal/mol

Note: In order to calculate the free energy of the solvated solute (Gsolv),
      one should add the computed dGsolv to the "Final Gibbs free energy"
      (Gvac = H-T*S) of the solute in gas-phase. That is: Gsolv = Gvac +
      dGsolv. Here, the Gvac has been calculated previously after a frequency
      calculation of the solute at a certain level of theory and printed
      in the "THERMOCHEMISTRY" block.
```

如 COSMO-RS 输出最后一段所指出的，要计算被给定溶剂溶剂化的溶质的
Gibbs 自由能，应当把计算的 $\Delta G_{\mathrm{S}}$ 加到气相溶质的
`Final Gibbs free energy` 上。

**[注意：]{.underline}** 上文解释的 ORCA/openCOSMO-RS 计算工作流程
对气相和溶液中的溶质使用相同的结构。不过，这些结构可能因溶质和溶剂的
类型而有实质差异。在 ORCA 中，可以为 ORCA/openCOSMO-RS 工作流程中
所需的三项计算分别优化结构。即 (1) 气相中的溶质，(2) 导体中的溶质，
(3) 导体中的溶剂。为此，需要通过 `dftfunc` 标签添加优化级别，
该标签专用于 DFT 泛函，但作为例外，可以用优化标签扩展：

```orca
%cosmors
  dftfunc  "BP86 tightopt"
end
```

<a id="sec:essentialelements.solvationmodels.opencosmors.keywords"></a>
### OpenCOSMO-RS 关键词

可在 ORCA 输入文件 `%cosmors` 块中定义的参数如下：

```orca
%cosmors
  aeff              5.925  # Effective contact area between surface segments (Å^2)
  lnalpha           0.202  # Logarithm of the misfit prefactor
  lnchb             0.166  # Hydrogen bond (HB) strength parameter
  chbt              1.50   # Parameter for the temperature dependence of the HB
  sigmahb           9.61e-3 # HB threshold parameter (e/Å^2)
  rav               0.50   # Radius to average ideal screening charges in Å
  fcorr             2.40   # Parameter adjusted from dielectric screening energies
  ravcorr           1.00   # Additional radius to calculate the misfit energy in Å
  astd              41.624 # Standard surface area (normalization factor) in Å^2
  zcoord            10.0   # Coordination number
  dgsolv_eta       -4.4480 # Offset for the solv. energy calculation
  dgsolv_omegaring  0.2630 # Correction for solv. energy of molecules with rings
  temp              298.15 # Reference temperature in Kelvin
  dftfunc           "BP86" # String for the DFT functional
  dftbas            "def2-TZVPD"  # String for the basis set
  solvent           "THF"  # Solvent from the internal database
  solventfilename   "water" # Name of the .cosmorsxyz solvent file
  orbs_vac          false  # Reuse the gas-phase orbitals for the calculation
                           # involving the solute in a conductor
end
```
不建议更改 COSMO-RS 参数的默认值。

<a id="sec:essentialelements.solvationmodels.cc"></a>
## 耦合簇方法中的隐式溶剂化

隐式溶剂化体系的耦合簇拉格朗日量（coupled-cluster Lagrangian）
$\mathcal{L}$ 如下 [cammi2009,caricato2011,garcia_neese_cc_cpcm](../../bibliography.md)

$$

\mathcal{L}(\Lambda,T)=\langle\psi_0|(1+\Lambda)\mathrm{e}^{-T} H_0 \mathrm{e}^T|\psi_0\rangle+\frac{1}{2}\mathbf{\overline{Q}}(\Lambda,T)\cdot\mathbf{\overline{V} }(\Lambda,T)\qquad \text{(eq_lag)}

$$

其中 $\psi_0$ 是参考波函数，$H_0$ 是孤立分子的哈密顿量。CCSD 的算符 $T$
按单激发和双激发定义（$T=T_1+T_2$），$\Lambda$ 是去激发算符
（de-excitation operator），按 Lagrange 乘子定义：

$$

T=T_1+T_2=\sum_{ia}t_a^ia_a^+a_i+\sum_{ijab}t_{ab}^{ij}a_a^+a_b^+a_ja_i\qquad \text{(eq_t)}

$$

$$

\Lambda=\sum_{ia}\lambda_i^aa_i^+a_a+\frac{1}{2}\sum_{ijab}\lambda_{ij}^{ab}a_i^+a_aa_j^+a_b\qquad \text{(eq_mult)}

$$

这里 $t_a^i$ 和 $t_{ab}^{ij}$ 是单激发和双激发波函数振幅
（amplitudes），$a_i$ 和 $a_a^+$ 分别是标准的费米子湮灭和产生算符。
正则占据轨道用符号 $i,j,k,\dots$ 表示，虚轨道用符号 $a,b,c,\dots$ 表示，
一般轨道指标用符号 $p,q,r\dots$ 表示。

量 $\mathbf{\overline{Q} }$ 和 $\mathbf{\overline{V} }$ 是 C-PCM 算符
$\mathbf{Q}$ 和 $\mathbf{V}$ 的 CC 期望值，它们分别是定义在电荷位置处的
溶剂化电荷向量和溶质势向量。

$$

\mathbf{\overline{Q}}(\Lambda,T)=\langle\psi_0|(1+\Lambda)\mathrm{e}^{-T}\mathbf{Q}\mathrm{e}^T|\psi_0\rangle\qquad \text{(eq_qbar1)}

$$

$$

\mathbf{\overline{V}}(\Lambda,T)=\langle\psi_0|(1+\Lambda)\mathrm{e}^{-T}\mathbf{V}\mathrm{e}^T|\psi_0\rangle\qquad \text{(eq_vqbar1)}

$$

公式 [Eq](#eq_lag) 可以通过引入算符的正规乘积形式改写为：

$$

X_N=X-\langle\psi_0|X|\psi_0\rangle=X-X_0\qquad \text{(eq_normalf)}

$$

如果在公式 [Eq](#eq_lag) 中使用这一结果，并结合 $\mathbf{Q}$ 和
$\mathbf{V}$ 通过公式 [Eq](#eq_cpcm) 相关联的事实，则公式
[Eq](#eq_lag) 写作

$$

\begin{split}
\mathcal{L}(\Lambda,T)=&\langle\psi_0|H_0|\psi_0\rangle+\langle\psi_0|(1+\Lambda)\mathrm{e}^{-T}H_{0N}\mathrm{e}^T|\psi_0\rangle+\frac{1}{2}\mathbf{Q}_0\cdot\mathbf{V}_0+\mathbf{Q}_0\cdot\mathbf{\overline{V} }_N(\Lambda,T)+\frac{1}{2}\mathbf{\overline{Q} }_N(\Lambda,T)\cdot\mathbf{\overline{V} }_N(\Lambda,T)=\\
&=E_0+\langle\psi_0|(1+\Lambda)\mathrm{e}^{-T}H_{0N}\mathrm{e}^T|\psi_0\rangle+\mathbf{Q}_0\cdot\mathbf{\overline{V} }_N(\Lambda,T)+\frac{1}{2}\mathbf{\overline{Q} }_N(\Lambda,T)\cdot\mathbf{\overline{V} }_N(\Lambda,T)
\end{split}\qquad \text{(eq_lag2)}

$$

这里 $\mathbf{Q}_0$ 和 $\mathbf{V}_0$ 是用 $\psi_0$ 波函数计算的
$\mathbf{Q}$ 和 $\mathbf{V}$ 向量，$E_0$ 是参考能量
（$E_0=\langle\psi_0|H_0|\psi_0\rangle+\frac{1}{2}\mathbf{Q}_0\cdot\mathbf{V}_0$）。
在公式 [Eq](#eq_lag2) 中可以采用不同的近似，
取决于如何计算其最后一项
$\frac{1}{2}\mathbf{\overline{Q} }_N(\Lambda,T)\cdot\mathbf{\overline{V} }_N(\Lambda,T)$。

在 ORCA 中有三种不同的 CCSD/CPCM 方法：(i) PTE 方案，(ii) PTE(S) 方案，
(iii) PTES 方案，最后一种是默认。这里缩写 PTE 代表"微扰理论与能量"
（perturbation theory and energy），"S" 代表单激发（singles）。
这些方法的选择通过标签 `CPCMccm` 控制。关于 ORCA 在计算中使用了哪种
CCSD/C-PCM 的信息，打印在输出文件 `ORCA-MATRIX DRIVEN CI` 块中
以 `CPCM scheme` 开头的行：

```orca
--------------------------------------------------------------------------------
                             ORCA-MATRIX DRIVEN CI
--------------------------------------------------------------------------------

--------------------------------
AUTOMATIC CHOICE OF INCORE LEVEL
--------------------------------

Memory available                           ...   2000.00 MB
Memory needed for S+T                      ...      9.26 MB
Memory needed for J+K                      ...     18.57 MB
Memory needed for DIIS                     ...    129.61 MB
Memory needed for 3-ext                    ...     72.69 MB
Memory needed for 4-ext                    ...    486.14 MB
Memory needed for triples                  ...      0.00 MB
 -> Final InCoreLevel    ... 5

Wavefunction type
-----------------
Correlation treatment                      ...      CCSD
Single excitations                         ... ON
Orbital optimization                       ... OFF
Calculation of Lambda equations            ... ON
Calculation of Brueckner orbitals          ... OFF
Perturbative triple excitations            ... OFF
CPCM scheme                                ... PTE(S)
Calculation of F12 correction              ... OFF
```

在下面的小节中，我们描述 ORCA 中可用的不同 CCSD/C-PCM 方法及其用法。

<a id="sec:essentialelements.solvationmodels.sec_pte"></a>
### PTE 方案

在"微扰理论能量"（PTE）方案中，公式 [Eq](#eq_lag2) 的最后一项等于零
（该项不依赖于 $\Lambda$ 和 $T$），

$$

\mathcal{L}(\Lambda,T)=E_0+\langle\psi_0|(1+\Lambda)\mathrm{e}^{-T}H_{0N}\mathrm{e}^T|\psi_0\rangle+\mathbf{Q}_0\cdot\mathbf{\overline{V} }_N(\Lambda,T)\qquad \text{(eq_pte_lag)}

$$

势 $\mathbf{\overline{V} }_N$ 可以写成：

$$

\mathbf{\overline{V} }_N(\Lambda,T)=\langle\psi_0|(1+\Lambda)\mathrm{e}^{-T}\sum_{pq}\mathbf{v}_{pq}\{p^+q\}\mathrm{e}^T|\psi_0\rangle=\sum_{pq}\mathbf{v}_{pq}\langle\psi_0|(1+\Lambda)\mathrm{e}^{-T}\{p^+q\}\mathrm{e}^T|\psi_0\rangle=\sum_{pq}\mathbf{v}_{pq}\Gamma_{pq}\qquad \text{(eq_vnlt)}

$$

这里我们使用了 $\mathbf{V}_N=\sum_{pq}\mathbf{v}_{pq}\{p^+q\}$
（正规序算符的二次量子化形式），其中 $\mathbf{v}_{pq}$ 是溶质势在
MO 基中的分量。矩阵 $\Gamma$ 是 CCSD 弛豫单电子密度矩阵。
于是，对 $T$ 振幅方程的贡献来自 $\mathbf{\overline{V} }_N(\Lambda,T)$
对 $\Lambda$ 振幅的导数（$\mathbf{Q}_0$ 不依赖于 Lagrange 乘子）。
在这一语境下，哈密顿量 $H_{0N}$ 含有一项依赖于 Fock 矩阵元
（$\sum_{pq}f_{pq}\{p^+q\}$）的项，它与 $\mathbf{V}_N$ 具有相同的函数形式。
由于 Fock 矩阵在参考计算中用一项 C-PCM 项更新（AO 基下）
$F_{\mu\nu}^{\mathrm{CPCM} }=\mathbf{Q}_0\cdot\mathbf{V}_{\mu\nu}$，
则项 $\mathbf{Q}_0\cdot\mathbf{\overline{V} }_N(\Lambda,T)$ 被隐含地
加到公式 [Eq](#eq_pte_lag) 中。

一旦得到 $T$ 振幅，总能量 $E$ 计算为

$$

E=E_0+\langle\psi_0|\mathrm{e}^{-T}(H_{0N}+\mathbf{Q}_0\cdot\mathbf{V}_N)\mathrm{e}^T|\psi_0\rangle=E_0+\sum_{ia}F_{ia}t_a^i+\frac{1}{4}\sum_{ijab}\langle ij||ab\rangle\left(t_{ab}^{ij}+2t_a^it_b^j\right)\qquad \text{(eq_ecc_pte)}

$$

于是，PTE 方案中 C-PCM 对 CC 能量的贡献通过 $E_0$ 中的项
$\frac{1}{2}\mathbf{Q}_0\cdot\mathbf{V}_0$，以及隐含地通过 Fock 矩阵元
$F_{ia}$（$F_{ia}=F_{ia}^0+\mathbf{Q}_0\cdot\mathbf{v}_{ia}$）出现。

PTE 方案对应于 `CPCMccm 0`，对正则 CCSD（RHF 和 UHF）和 DLPNO-CCSD
（RHF 和 UHF）实现。例如，对用水溶剂化的体系用 PTE 方案做
DLPNO-CCSD 计算（闭壳层参考），输入文件如下：

```orca

! DLPNO-CCSD cc-pVTZ cc-PVTZ/C TightSCF CPCM(Water)

%cpcm
  CPCMccm 0
end

* xyzfile 0 1 water.xyz
```

<a id="sec:essentialelements.solvationmodels.sec_pte_s"></a>
### PTE(S) 方案

在该方案中（"S" 代表单激发），公式 [Eq](#eq_lag2) 的最后一项依赖于
$T$ 振幅，但不依赖于 $\Lambda$ 振幅，

$$

\mathcal{L}(\Lambda,T)=E_0+\langle\psi_0|(1+\Lambda)\mathrm{e}^{-T}H_{0N}\mathrm{e}^T|\psi_0\rangle+\mathbf{Q}_0\cdot\mathbf{\overline{V} }_N(\Lambda,T)+\frac{1}{2}\mathbf{\overline{Q} }_N(T)\cdot\mathbf{\overline{V} }_N(T)\qquad \text{(eq_pte_s_lag)}

$$

同样，与 PTE 方案相同，C-PCM 对 $T$ 振幅方程的贡献来自公式
[Eq](#eq_pte_s_lag) 中的项 $\mathbf{Q}_0\cdot\mathbf{\overline{V} }_N(\Lambda,T)$，
它被隐含地加到 MO 基中的 Fock 矩阵元上。公式
[Eq](#eq_pte_s_lag) 的最后一项不依赖于 $\Lambda$ 振幅，
因而对 $T$ 振幅方程没有贡献。不过，该项通过密度矩阵 $\Gamma$ 的
$\gamma_{ai}$ 元依赖于 $T$ 振幅，

$$

\gamma_{ai}=t_a^i+\sum_{me}\left(t_{ae}^{im}-t_e^it_a^m\right)\lambda_m^e-\frac{1}{2}\sum_{mnef}\lambda_{mn}^{ef}\left(t_{ef}^{in}t_a^m+t_{af}^{mn}t_e^i\right)\qquad \text{(eq_gai)}

$$

于是它以如下方式对最终能量 $E$ 作出贡献：

$$

\frac{1}{2}\mathbf{\overline{Q} }_N(T)\cdot\mathbf{\overline{V} }_N(T)=\frac{1}{2}\left(\sum_{ai}t_a^i\mathbf{q}_{ai}\right)\cdot\left(\sum_{ai}t_a^i\mathbf{v}_{ai}\right)\qquad \text{(eq_pte_s_ec)}

$$

这就给出了体系总能量的最终方程，

$$

\begin{split}
E&=E_0+\langle\psi_0|\mathrm{e}^{-T}(H_{0N}+\mathbf{Q}_0\cdot\mathbf{V}_N)\mathrm{e}^T|\psi_0\rangle+\frac{1}{2}\left(\sum_{ai}t_a^i\mathbf{q}_{ai}\right)\cdot\left(\sum_{ai}t_a^i\mathbf{v}_{ai}\right)=\\
&=E_0+\sum_{ia}F_{ia}t_a^i+\frac{1}{4}\sum_{ijab}\langle ij||ab\rangle\left(t_{ab}^{ij}+2t_a^it_b^j\right)+\frac{1}{2}\left(\sum_{ai}t_a^i\mathbf{q}_{ai}\right)\cdot\left(\sum_{ai}t_a^i\mathbf{v}_{ai}\right)\end{split}\qquad \text{(eq_ecc_pte_s)}

$$

因此，PTE(S) 方案中溶剂化体系的 CC 能量涉及三项 C-PCM 贡献：
(1) 包含在 $E_0$ 中的项 $\frac{1}{2}\mathbf{Q}_0\cdot\mathbf{V}_0$，
(2) 通过 $\sum_{ia}F_{ia}t_a^i$ 隐含出现的项
$\sum_{ia}\mathbf{Q}_0\cdot\mathbf{v}_{ia}t_a^i$，
(3) 项 $\frac{1}{2}\left(\sum_{ai}t_a^i\mathbf{q}_{ai}\right)\cdot\left(\sum_{ai}t_a^i\mathbf{v}_{ai}\right)$。

该方案在 ORCA 中对正则 CCSD（RHF 和 UHF）和 DLPNO-CCSD（RHF 和 UHF）
可用。要使用它，用户需要在 `%cpcm` 块中添加标签 `CPCMccm 1`。

```orca

! DLPNO-CCSD cc-pVTZ cc-PVTZ/C TightSCF CPCM(Water)

%cpcm
  CPCMccm 1
end

* xyzfile 0 1 water.xyz
```

<a id="sec:essentialelements.solvationmodels.sec_ptes"></a>
### PTES 方案

在该方案中，公式 [Eq](#eq_lag2) 最后一项中的
$\mathbf{\overline{Q} }_N$ 和 $\mathbf{\overline{V} }_N$ 都依赖于 $T$ 振幅，
但只有一个依赖于 $\Lambda$ 振幅，

$$

\mathcal{L}(\Lambda,T)=E_0+\langle\psi_0|(1+\Lambda)\mathrm{e}^TH_{0N}\mathrm{e}^T|\psi_0\rangle+\mathbf{Q}_0\cdot\mathbf{\overline{V} }_N(\Lambda,T)+\frac{1}{2}\mathbf{\overline{Q} }_N(T)\cdot\mathbf{\overline{V} }_N(\Lambda,T)\qquad \text{(eq_lptes)}

$$

C-PCM 项一方面通过 Fock 矩阵元隐含地进入这些方程
（与 PTE 和 PTE(S) 方案一样），另一方面通过
$\frac{1}{2}\mathbf{\overline{Q} }_N(T)\cdot\mathbf{\overline{V} }_N(\Lambda,T)$
对 $\Lambda$ 的导数显式地进入。如果我们把公式 [Eq](#eq_lptes) 中
最后一个 C-PCM 项记作 $\mathcal{L}_{\mathrm{CPCM} }$，
则该项对 $T$ 振幅方程的贡献为：

$$

\frac{\partial\mathcal{L}_{\mathrm{CPCM} }}{\partial \lambda_i^a}=\frac{1}{2}\left(\sum_{ai}t_a^i\mathbf{q}_{ai}\right)\cdot\left[-\sum_jt_a^j\mathbf{v}_{ji}+\sum_bt_b^i\mathbf{v}_{ab}+\mathbf{v}_{ia}+\sum_{bj}\left(t_{ba}^{ji}-t_a^jt_b^i\right)\mathbf{v}_{bj}\right]\qquad \text{(eq_ltesd1)}

$$

$$

\frac{\partial\mathcal{L}_{\mathrm{CPCM} }}{\partial \lambda_{ij}^{ab} }=\frac{1}{2}\left(\sum_{ai}t_a^i\mathbf{q}_{ai}\right)\cdot\left[-\frac{1}{2}\sum_kt_{ab}^{kj}\mathbf{v}_{ki}+\frac{1}{2}\sum_ct_{ac}^{ij}\mathbf{v}_{bc}-\frac{1}{2}\sum_{ck}\left(t_{ab}^{kj}t_c^i+t_{cb}^{ij}t_a^k\right)\mathbf{v}_{ck}\right]\qquad \text{(eq_ltedd)}

$$

对能量的贡献与 PTE(S) 方案相同，但 $T$ 振幅的取值不同
（因为计算它们的方程与 PTE(S) 方案略有不同）。

$$

\begin{split}
E&=E_0+\langle\psi_0|\mathrm{e}^{-T}(H_{0N}+\mathbf{Q}_0\cdot\mathbf{V}_N)\mathrm{e}^T|\psi_0\rangle+\frac{1}{2}\left(\sum_{ai}t_a^i\mathbf{q}_{ai}\right)\cdot\left(\sum_{ai}t_a^i\mathbf{v}_{ai}\right)=\\
&=E_0+\sum_{ia}F_{ia}t_a^i+\frac{1}{4}\sum_{ijab}\langle ij||ab\rangle\left(t_{ab}^{ij}+2t_a^it_b^j\right)+\frac{1}{2}\left(\sum_{ai}t_a^i\mathbf{q}_{ai}\right)\cdot\left(\sum_{ai}t_a^i\mathbf{v}_{ai}\right)\end{split}\qquad \text{(eq_ecc_ptes)}

$$

该方案是 ORCA 中默认的 CCSD/C-PCM 方法，在 ORCA 中对正则 CCSD
（RHF 和 UHF）和 DLPNO-CCSD（RHF 和 UHF）可用。在这种情况下，
`%cpcm` 块中的标签 `CPCMccm` 等于 2。不过，由于 PTES 方案是 ORCA 的
默认，用户只需在输入文件中添加关于溶剂的信息即可使用该方法。

```orca

! DLPNO-CCSD cc-pVTZ cc-PVTZ/C TightSCF CPCM(Water)

* xyz 0 1
O  -0.00000018976103    0.00606010894837    0.00000000004527
H   0.76098169249695   -0.58891312953082   -0.00000000000022
H  -0.76098151333900   -0.58891299029372   -0.00000000000022
*
```

**关于使用 CCSD/C-PCM 方案的注**：

-   对于 PTE(S) 和 PTES 方案中的计算，对总能量的显式 C-PCM 贡献
    （见公式 [Eq](#eq_ecc_pte_s) 和 [Eq](#eq_ecc_ptes)）
    在 "T" 振幅方程收敛后打印在 `COUPLED CLUSTER ENERGY` 块中。
    在这种情况下，该能量标记为 `C-PCM corr. term`，
    并已包含在相关能 `E(CORR)` 中。对于上面的输入例子，该信息如下：

    ```orca
    ----------------------
    COUPLED CLUSTER ENERGY
    ----------------------

    E(0)                                       ...    -76.066903687
    E(CORR)(strong-pairs)                      ...     -0.267203798
    E(CORR)(weak-pairs)                        ...     -0.000106106
    E(CORR)(corrected)                         ...     -0.267309904
    C-PCM corr. term (included in E(CORR))     ...     -0.000003158
    E(TOT)                                     ...    -76.334213591
    Singles Norm <S|S>**1/2                    ...      0.017784967
    T1 diagnostic                              ...      0.006287935
    ```

    该贡献并不代表 C-PCM 对相关能的全部贡献，
    因为后者还通过 "T" 振幅隐含地出现。

-   C-PCM 对 $\Lambda$ 方程的贡献在 ORCA 中对 PTE(S) 和 PTES 方案实现。
    因此用户可以请求非弛豫密度（unrelaxed densities）。

<a id="sec:essentialelements.solvationmodels.keyword-list.detailed"></a>
## `%cpcm` 块的完整关键词列表

用户可通过 `%cpcm` 块请求的可用参数/选项有：

```orca
%cpcm
  epsilon             80.0    # Dielectric constant
  refrac               1.0    # Refractive index
  rsolv                1.3    # Solvent probe radius in Angstroem
                              # (for SES-type cavities)
  rmin                 0.5    # Minimal GEPOL sphere radius in Angstroem
  pmin                 0.1    # Minimal distance between two surface points
                              # in Angstroem
  fepstype            cpcm    # Epsilon function type: cpcm, cosmo
  xfeps                0.0    # X parameter for the feps scaling function
  surfacetype vdw_gaussian    # Cavity surface: gepol_ses, gepol_sas
                                                vdw_gaussian, gepol_ses_gaussian
  ndiv                   5    # Maximum depth for recursive sphere generation
  num_leb              302    # Lebedev points for the Gaussian charge scheme
  radius[N]            1.3    # Atomic radius for atomic number N in Angstroem
  AtomRadii(N,1.4)            # Atomic radius for the Nth atom in Angstroem
  scale_gauss          1.2    # Scaling factor for the atomic radii in the
                                Gaussian charge scheme
  cut_area             0.0    # Cutoff for the area of a surface segment in a.u.
                                Only valid for the Gaussian charge scheme
  cut_swf             1e-7    # Cutoff for the switching function
                                Only valid for the Gaussian charge scheme
  thresh_h             5.0    # Threshold for the charge density on a hydrogen
                                atom in charges/Å^2 (isodensity scheme)
  thresh_noth          5.0    # Threshold for the charge density on non-hydrogen
                                atoms in charges/Å^2 (isodensity scheme)
  solvent          "water"    # Solvent name (for C-PCM)
  smd                 true    # Turn on SMD
  smdsolvent     "ethanol"    # Solvent name for SMD
  soln              1.3611    # Index of refraction at optical frequencies at 293 K
  soln25            1.3593    # Index of refraction at optical frequencies at 298 K
  sola                0.37    # Abraham's hydrogen bond acidity
  solb                0.48    # Abraham's hydrogen bond basicity
  solg               31.62    # Relative macroscopic surface tension
  solc                0.00    # Aromaticity, fraction of non-hydrogenic solvent
                              # atoms that are aromatic carbon atoms
  solh                0.00    # Electronegative halogenicity, fraction of
                              # non-hydrogenic solvent atoms that are F, Cl, or Br
  SMD18              false    # Turn on SMD18
  CPCMccm                0    # Coupled-cluster/C-PCM scheme (default = 2)
  cds_cpcm               0    # Use of the GVDW_nel or GSES_nel scheme
                              # (default = 0)
  draco               true    # Turn on DRACO (default = false)
  dracoisodens       false    # Use isodensity scheme for DRACO (default = false)
  draco_charges        ceh    # Charges used within DRACO (default = eeq)
  vopt          v_analytic    # Method to calculate the ESP at the position
                              # of the charges:
                              #   v_analytic (default): via analytic ESP integrals
                              #   v_numeric: via numerical integration
                              #   v_ri: via the RI-density
                              #   v_multipole: via BUPO
 fopt           f_analytic    # Method to calculate the C-PCM contribution to the
                              # Fock or Kohn-Sham matrix:
                              #   f_analytic (default): via the ESP integrals
                              #   f_numeric: via numerical integration
                              #   f_ri: via the RI-density
                              #   f_multipole: via BUPO
end
```
