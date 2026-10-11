

<a id="sec:spectroscopyproperties.dlpno-steom"></a>
# 通过 DLPNO-STEOM-CCSD 计算激发态（Excited States via DLPNO-STEOM-CCSD）

强大的耦合簇（coupled cluster）方法同样可用于激发态计算。
STEOM-CCSD 是对代价高昂的 EOM-CCSD 方法的改进，可在计算激发能时
获得更低的计算标度。在轨道空间中引入 DLPNO 近似后，通过进一步
优化计算成本，使理论更为紧凑。
一般性描述请参见 [sec:spectroscopyproperties.steom](#sec:spectroscopyproperties.steom)。

<a id="sec:spectroscopyproperties.dlpno-steom-dressing.general"></a>
## PNO dressing（实验性关键词，experimental keyword）

在 STEOM-DLPNO-CCSD 方法中，除最后一步——即 STEOM-CCSD 计算本身——以外，
大部分步骤均采用强大的 PNO 近似完成。在 dressing 的正则版本（canonical
version，ORCA 中的默认实现）中，先前在 PNO 水平上计算的所有振幅都会
被重新正则化（recanonicalized），从而增加了计算成本。PNO dressing 会
利用部分 PNO 中间量来缩短 dressing 时间，但对存储规模没有影响。

使用该 PNO dressing 可缩短计算时间，但激发能的精度会有所下降。
因此我们仅推荐将该选项用于特定的大型体系（>2500 个基函数）。

将关键词 $\textbf{DirectDressSTEOM}$ 设为 true 即可启用该选项。

<a id="sec:spectroscopyproperties.dlpno-steom-keyword.general"></a>
## 来自 STEOM-CCSD 的关键词（Keywords from STEOM-CCSD）

STEOM-CCSD 中的大多数关键词在 DLPNO 版本中同样可用。
更多信息见 [sec:spectroscopyproperties.steom](#sec:spectroscopyproperties.steom) 章节。

## 示例（Example）

对于标准有机分子，我们推荐使用如下输入。此处以甲醛为例，
采用 def2-TZVP 基组。

作为一般性指导，我们来讨论其中使用的部分关键词：

```orca
! STEOM-DLPNO-CCSD def2-TZVP def2-TZVP/C def2/J TightSCF

%mdci
  NRoots 6
  DoRootWise true
  OThresh 0.005
  VThresh 0.005
  TCutPNOSingles 1e-11
  NDAV 400
  DoStoreSTEOM true
  DoSimpleDens false
  AddL2Term True
  DTol 1e-5
end

* xyz 0 1
  C     0.016227   -0.000000    0.000000
  O     1.236847    0.000000   -0.000000
  H    -0.576537    0.951580   -0.000000
  H    -0.576537   -0.951580   -0.000000
*
```

## 提示与技巧（Tips and Tricks）

!!! warning
     对于 DLPNO 计算，至少需要一个辅助基组。因此本输入中使用了
     def2-TZVP/C def2/J。若不显式指定辅助基组，也可以使用通用关键词
     "AutoAux"。

在这种情况下，同一输入的第一行将变为
```orca
! STEOM-DLPNO-CCSD def2-TZVP AutoAux TightSCF
```

!!! note
    DLPNO-STEOM-CCSD 目前尚不适用于 UHF 波函数，因此目前无法进行
    开壳层（open shell）计算。

- 对任何 CCSD 计算而言，TIGHTSCF 都是必需的。

- 我们建议对所有分子都使用 TIGHTPNO，因为它带来的额外开销并不大，
且有助于获得更好的收敛性。

- OTHRESH、VTHRESH 和 TCutPNOSingles 关键词有助于计算收敛，并提高
每个根的活性百分比。与标准 STEOM-CCSD 不同，我们认为当活性特征百分比
至少达到 96% 时根已收敛。当然，您必须检查与激发相关的振幅和轨道是否
正确（且符合预期）。收紧上述 3 个关键词会提高活性特征百分比，其中最
重要的是 TCutPNOSingles。注意，当阈值收紧时，计算成本会急剧上升。
在多数情况下 $10^{-12}$ 或 $5\times 10^{-12}$ 即可。对于 OTHRESH 和
VTHRESH，不应低于 $10^{-3}$，因为收益并不明显。一个有助于更好收敛的
技巧是调整根的数目。如果您只关心前 3 个根，通常无需计算大量根。若某些
高能根的活性百分比偏低，删除它们有助于其他根的收敛。

- 如相关论文[Ghosh2020](../../bibliography.md) 所示，含 L2term 的 STEOM 密度现在已成为
计算激发态性质的默认方法。

- 基组的选择也能在不显著损失精度的前提下加速计算。对大多数有机分子而言，
def2-TZVP(-f) 已足够。在初步测试中尝试 def2-SVP 也是一个好主意。

- STEOM-CCSD 激发能对初始几何结构非常敏感。采用不同 DFT 泛函优化得到的
几何结构可能导致激发能存在显著差异（约 0.1 eV）。

- 有报告称，当关键词 $\textbf{Dorootwise}$ 设为 true 时会丢失某些根。
将其关闭即可解决该问题，但该关键词默认应为开启状态。
