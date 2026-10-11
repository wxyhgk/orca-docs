(sec:.quickstartguide.recommendations)=
# 一般性建议

:::{warning}
科学家们对于何时使用何种方法以及原因无疑存在不同看法。不过，基于开发者的经验，我们想在 ORCA 的语境下给出一些主观建议。
:::

ORCA 为量子化学计算提供了一套全面而强大的工具。然而，为手头的化学问题选择合适的方法往往很困难，但这对于获得合理结果又至关重要。尽管如此，我们仍可以给出一些一般性的主观建议，帮助您在海量可用的方法组合和计算方案中找到方向。我们还建议查阅涵盖计算化学应用基础的教学性综述文章。

```{index} 计算化学文献
```

:::{admonition} 计算化学教学综述
:class: hint

```{bibliography} ../../bibliography.bib
:list: enumerated
:filter: false

bursch20222bestpracticedft
```
:::

(sec:.quickstartguide.recommendations.knowyourmethods)=
## 了解你所用的方法

尽管某些方法的理论背景可能相当复杂，但使用者应当了解所选方法的优势与局限。因此，建议在使用任何方法之前，先对其理论基础有一个基本认识。一些突出的例子如下：

*   典型的 DFT 泛函（density functional）在理论上无法恢复伦敦色散（London dispersion）效应。因此必须采用合适的[色散校正（dispersion correction）](sec:modelchemistries.dispersioncorrections)，对大体系尤其如此。

*   二阶 Møller-Plesset 微扰理论（second order Møller-Plesset perturbation theory, MP2）的能量表达式分母依赖于占据轨道与非占据轨道的能级差。因此，对于轨道能隙很小或电子态近简并的体系（例如许多 3d 过渡金属配合物），该方法可能会失效。

*   单参考（single-reference）方法如常规 DFT 和[单参考耦合簇对多参考情形可能不适用](sec:modelchemistries.CCsDiagnostic)。何时转向多参考方法是更复杂的问题。通常，在需要多重态（multiplet）、含多个未配对电子体系的纯自旋函数、断键情形或某些激发态时（通俗地说：只要体系中存在弱相互作用电子），就需要多参考方法。然而，无论何时决定这样做，请务必意识到这需要对所研究问题的物理和化学有深刻的理解。未经训练地使用 [CASSCF](sec:modelchemistries.casscf) 或 MRCI/MRPT 方法，很可能以巨大的计算代价得到毫无意义的数字。在这方面，经验（和耐心）无可替代。

:::{tip}
**了解你所选方法的优势与不足**。归根结底，任何近似方法的精度都是有限的，它是否完全适合计算所需的性质，只能通过实验以及与实验结果或高级别 *ab initio* 计算的比较来回答。在这方面，我们建议利用各种非常有用的基准研究（benchmark study），它们针对不同性质提供了有价值的数据和方法推荐！
:::

(sec:.quickstartguide.recommendations.costvsaccuracy)=
## 成本与精度

时间和计算资源并非无限。因此，重要的是要了解所选方法能否在给定时间范围内达到足够的精度。此外，能把某个数字算得稍微更准一点，并不意味着这有助于更好地理解目标体系的物理和化学。陷入技术细节而错失所需洞察的危险是真实存在的！决定成本-精度比的最相关因素是：(a) 所用方法，(b) 所用基组（basis set），以及 (c) 所用的截断值（cutoff）和容差（tolerance）。一些示例如下：

*   即使是高级别电子结构方法，若与 STO-3G 或 3-21G 这类极小或小的分裂价基组（split-valence basis set）联用，也会给出很差、至少是不可靠的结果。
    不过，如果只需要定性结果，它们对于非常大的分子或在筛选和探索性方案中可能有用。要获得可靠结果，推荐使用三-$\zeta$（triple-zeta）及更高精度的基组。例如卡尔斯鲁厄（Karlsruhe）的 def2-TZVPP 和 Dunning 的 cc-pVTZ [基组](../essentialelements/basisset.md)。

*   使用非常宽松的优化阈值（optimization threshold）可能会加快优化速度，但会阻碍体系到达给定势能面（potential energy surface）上的真正极小点。
    对于势能面相对平坦的柔性分子，情况尤其如此。

*   不够精确的[数值积分（numerical integration）](../essentialelements/numericalintegration.md)格点可以加快计算，但也会限制原本高精度的方法/基组组合的准确度。尽管 ORCA 中的默认设置被选定为在大多数情况下给出合理结果，但如果您追求高精度，仍应增大数值积分格点。

*   有些近似比其他近似危害更大。例如，[RI 近似](../essentialelements/RI.md)配合足够大的辅助基组（auxiliary basis set）可以大幅缩短计算时间，而几乎不损失精度。因此，我们一般推荐按照 ORCA 的默认设置使用 RI 技术。

:::{tip}
**明确你想达到的精度水平。**如果定性结果就足够了，那么减小基组规模或放宽阈值也许是合理的。不过，任何结果都存在一个限度，超出该限度就应被视为可疑。
:::

(sec:.quickstartguide.recommendations.model)=
## 建立正确的模型

在实验条件（例如高温或溶液中）下重现体系的性质，是量子化学的圣杯之一。然而，即使最好的电子结构方法也无济于事，如果你的体系模型不完整或不正确。一些示例如下：

*   如果分子是柔性的且势能面平坦，那么实验条件下它的分子性质可能无法仅用一个构象（conformer）来描述。
    在这种情况下，应使用多结构方法，通过玻尔兹曼加权的构象系综来描述性质，这些构象可由 [GOAT](../structurereactivity/goat.md) 生成。

*   如果你的实验在溶液中进行，气相模拟可能无法给出足够准确的结果。可能需要通过
    [隐式溶剂化（implicit solvation）](../essentialelements/solvationmodels.md)或用 [SOLVATOR](../structurereactivity/solvator.md) 工具添加的显式溶剂分子来包含溶剂化效应。

*   创建较小的模型体系可以缩短计算时间，但有遗漏细微效应的风险，而这些效应可能导致与实验的显著差异。

:::{tip}
**明智地建立你的模型。**始终考虑在计算中包含环境效应，并确保你的结构模型能够重现所需的性质。
:::

(sec:.quickstartguide.recommendations.match)=
## 方法与性质的匹配

对一种性质表现良好的方法，未必对另一种性质也是如此。这对 [DFT](../modelchemistries/DensityFunctionalTheory.md) 这类更为近似的方法尤其适用。因此，我们建议查阅基准研究，以找到针对给定性质准确且稳健的密度泛函近似和方法组合。一些突出的情形如下：

*   [（meta-）GGA 泛函](sec:modelchemistries.dft.gga)如 PBE 或 r²SCAN 即使与相对较小的基组联用也能给出良好的几何结构。
    但对于能量，至少需要[杂化（hybrid）](sec:modelchemistries.dft.hybriddft)甚至[双杂化泛函（double-hybrid functional）](sec:modelchemistries.dft.doublehybriddft)才能达到足够高的精度。

    :::{warning}
    有些研究者喜欢根据自己的需要、或根据自己认为比标准"更好"的判断，来调整 Hartree-Fock
    交换（HF exchange）的比例。这会增加计算的半经验性质，而且可能只是针对某一类化合物和/或性质有效的补救措施，同时使其他情形的结果变差。在记住这一告诫的前提下，如果你喜欢，这属于你可以自由尝试的事情之一。然而，我们并不推荐这样做，因为它会损害你的结果与其他研究者结果的可比性——绝大多数研究者使用的是标准泛函。改变 HF 交换比例的一种替代方案是：对若干已知情形简单地构造一个线性回归，然后使用该线性回归。
    :::

*   像 TPSS 或 TPSSh 这类能量表现中等的泛函，在计算光谱性质（如 NMR 屏蔽常数（shielding constant）或
    EPR g 张量（g-tensor）与超精细耦合（hyperfine coupling））时可能非常有用。

*   双杂化泛函对大多数有机体系能给出很高的精度，但对 HOMO-LUMO 能隙很小的体系（例如 3d 过渡金属配合物）应避免使用。

:::{tip}
**检验你所选的方法。**我们一般建议查阅关于不同性质的详细基准研究。如果没有现成的基准研究，花些时间针对你的体系类别和要计算的性质对有前景的方法做基准测试或许是值得的。如果这也不可行，那么选择经验成分更少的高级 *ab-initio* 方法可能是提高结果可靠性更好的选择。
:::

(sec:.quickstartguide.recommendations.specific)=
## 一些针对特定方法的建议

-   双杂化泛函（DH）：经过微扰校正的泛函
    （B2PLYP）对许多问题也可能是非常好的选择（成本与 MP2 相当；
    注意，即使对于超过 1000 个基函数的大分子，只要调用了 RI 近似，
    MP2 校正部分也只需前面 SCF 计算约 10-20% 的时间。对于更大的分子，
    还可以通过 DLPNO 近似进一步加速 MP2 部分）。

-   DLPNO-CCSD(T)
    超越 DFT 和 (SCS-)MP2 之上还有耦合簇（coupled cluster）方法，
    ORCA 中的实现效率很高。借助局域对自然轨道（local pair natural orbital）
    方法，您甚至可以研究规模可观的分子，并获得诱人的周转时间。

-   **def2-TZVP** 与旧的 TZVP 不同。人们已经认识到，
    如果在价层的精确 triple-zeta 描述上投入计算资源，那么只使用一个极化函数（polarization function）
    意义有限。此时精度受极化函数集的限制，并不比从
    SV(P) 得到的结果好多少。因此 def2-TZVP 对氢包含一组 p 函数，
    但其他方面与旧的 TZVPP 基组非常相似，例如它对主族元素包含
    2d1f 极化函数，对过渡金属则包含大得多的极化函数集。最高阶的极化函数
    （主族的 f）确实会显著增加计算量。因此我们经常使用不含 f
    极化函数的 def2-TZVP。为此可以使用关键词
    def2-TZVP(-f)。与 RI 或 RIJCOSX 配合，这对大多数研究而言
    在计算上仍然足够经济。

-   **def2-TZVPP** 是一个完全自洽的 triple-zeta 基组，为 SCF 计算
    （HF 和 DFT）提供出色的精度，对相关计算（correlated calculation）也仍然
    相当不错。它是提供最终单点能（single point energy）的一个良好基组。

-   **def2-QZVPP** 是适用于各类计算的高精度基组。它提供接近基组极限的
    SCF 能量，相关能（correlation energy）同样出色。它在计算上
    昂贵，但配合 RI 和 RIJCOSX 以及并行化，通常仍可用于最终单点能
    计算。与这样大的基组配合时，还应提高 DFT
    和 RIJCOSX 中积分格点（integration grid）的精度——如果因为
    格点的数值噪声而限制了原本非常精确的计算的精度，那就太可惜了。

-   **一致性相关基组（correlation consistent basis sets）**能提供良好的相关能，
    但 SCF 能量很差甚至非常差。在相同规模下，ano-pVDZ
    基组准确得多，但计算上也更昂贵。除系统性的基组外推（basis set extrapolation）之外，我们看不出
    有多少理由使用 cc 基组。

-   **Pople 基组**有些过时，而且在整个周期表上的一致性也远不如
    卡尔斯鲁厄（Karlsruhe）小组的基组。因此我们一般倾向于后者。

-   对于**标量相对论（scalar relativistic）计算**（X2C、ZORA 和 DKH），我们强烈
    推荐使用[针对相应相对论校正重新收缩的基组](sec:essentialelements.basisset.builtin.rel)。

-   **有效核势（effective core potential, ECP）**相比全电子相对论
    计算能带来一些节省（但不一定是惊人的节省）。为获得准确结果，应使用小核
    [ECP](sec:essentialelements.basisset.ecps)。
    对于氪以后的元素，通常有与 def2 卡尔斯鲁厄型基组
    配套的 ECP 可用。一般而言，我们偏好 Stuttgart--Dresden
    ECP 而非 LANL 的。对于第一过渡系，选择
    较为有限。这里不存在与 ECP 配套的卡尔斯鲁厄基组，您只能
    在 SDD 或 LANL 之间选择，我们推荐前者。由
    ECP 得到的几何结构和能量通常不错，但对于性质计算，我们强烈建议改用
    全电子标量相对论计算，磁性质用 ZORA，
    电性质用 DKH。

-   您可以利用内置基组（用
    `!PrintBasis` 或 `orca_exportbasis` 打印），然后通过
    展开收缩的原函数、添加更陡的函数等对其进行修改（完全
    非收缩的基组可通过 `%basis` 中的 `uncontract` 生成）。
    另外，也存在一些在核心区域至少具有 double-zeta 品质的基组，包括 DZP 和 Dunning
    基组。若要获得更高精度，您不妨考虑 `aug-`
    系列基组。关于基组输入的更多内容，请参见
    {ref}`sec:essentialelements.basisset` 一节。

-   同样，如果对气相中的阴离子（anion）进行计算，
    建议在基组中包含弥散函数（diffuse function）。
    然而，有了这些弥散函数，事情会变得困难得多，因为基组的定域性显著降低。
    如果包含这些函数，建议为 `Thresh` 选择较小的值
    （10$^{-12}$ 或更低）。如果重叠矩阵（overlap matrix）的最小本征值低于 DiffSThresh
    （默认为 1e-6），则会自动如此处理。此外，弥散函数
    往往会引入基组线性相关（linear dependence）问题，这可以通过将 `Sthresh` 设为
    大于默认值 10$^{-7}$ 的值来解决（参见
    {ref}`sec:essentialelements.lindep` 一节）。任何超过 1e-6 的 `Sthresh` 值
    都必须谨慎使用，特别是在进行几何优化时，不同几何步骤中
    可能会切断不同的基组；或在比较不同构象时，
    因为最终基组可能出现某些不连续性。

-   DFT 中使用的**积分格点（integration grid）**应与基组一起考虑。如果大基组计算收敛到很高
    精度，那么也建议使用大的 DFT 积分格点
    （如 `! DEFGRID3`）。对于"无限"精度（即基准
    计算），最好使用乘积格点（`Grid=0`）
    并为 `IntAcc` 取较大的值（也许在 6.0 左右）。默认
    格点的选取原则是以最低的计算成本提供足够的精度，但对于重元素的全电子
    计算，配合标量相对论哈密顿量（Hamiltonian）时，您应非常仔细地考察
    格点依赖性，并相应调整这些参数以使误差最小。您应意识到，对大分子而言，
    交换相关积分通常*不是*主导因素（即使与 RI-J 组合时也不是）。

-   同样重要的是 `Thresh` 的值，它在很大程度上
    决定直接 SCF 计算的周转时间。将值取到
    10$^{-6}$--10$^{-8}$ 也许可行，这会带来大幅度加速。然而，
    最终能量的误差可能比截断值大 3 个数量级，或者有时
    由于积分精度有限，计算会无法收敛。一般而言，直接
    SCF 计算不可能收敛到优于 `Thresh` 的程度（程序也不
    允许这样）。若要获得更高精度，可使用约
    10$^{-10}$--10$^{-12}$ 的值，较大的分子需要较小的截断值。在 SCF 几乎收敛、但随后
    无法最终收敛的情形（这非常令人恼火）下，建议减小
    `Thresh` 并切换到 `TRAH` SCF。一般而言，为稳妥起见，`TCut`
    应大约取 `0.01` $\times$`Thresh`。

-   DFT 计算有许多优点，在许多情形下能给出可靠结果。不过，如果您研究有机
    分子，用 MP2 检验 DFT 结果仍是个好主意。RI-MP2 形式的 MP2 通常负担得起，
    并且能给出可靠结果（对于 DFT 精度较差的弱相互作用尤其如此）。如果
    MP2 与 DFT 结果之间存在较大差异，警钟就敲响了——在许多这类情形中 MP2
    是更好的选择，但在另一些情形（例如氧化还原过程或
    过渡金属体系）中则不然。请记住 SCS-MP2
    （RI-SCS-MP2）和双杂化泛函通常会给出比 MP2 本身更
    准确的结果。

-   耦合簇计算正变得越来越可行，
    应尽可能加以使用。DLPNO-CCSD 和
    DLPNO-CCSD(T) 计算可用于单点计算，并给出准确的结果。不过，
    耦合簇研究确实需要仔细考察基组效应，因为收敛到基组极限非常慢。成熟的
    基组外推方案在这里可能非常有帮助。对于开壳层（open-shell）分子，尤其对于过渡
    金属，在参考态上再怎么小心也不为过。您必须
    仔细检查 Hartree-Fock 计算是否收敛到所需的状态，才能得到
    有意义的耦合簇结果。轨道优化的 MP2（orbital optimized MP2）、CASSCF 或 DFT 轨道可能有所帮助，
    但我们经常遇到以这类选择求解耦合簇方程时的收敛困难。

-   一般而言，CEPA 往往优于 CCSD，并接近
    CCSD(T) 的质量。不过，由于对单
    激发与电子弛豫（electronic relaxation）之间关系的处理不够严格，
    它也比 CC 方法略欠稳健。
