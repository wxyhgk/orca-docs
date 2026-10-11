

<a id="sec:spectroscopyproperties.properties.eprnmr.MP2magnetic"></a>
# MP2 水平的磁性质（MP2 Level Magnetic Properties）

目前，超精细耦合（hyperfine couplings，不含 $A_\text{orb}$ 项）、
g 张量（g-tensors）以及不含 GIAO 的屏蔽张量（shielding tensors），
均可在正则 MP2（canonical MP2）、RI-MP2 和双杂化 DFT（double-hybrid DFT）下计算，
且不采用冻结芯近似（frozen core approximation）。
超精细耦合中的 $A_\text{orb}$ 项仅适用于 RI-MP2 和双杂化 DFT（无论是否采用冻结芯近似）。
若使用 RIJCOSX 近似，
则关键词 `Z_GridX`、`Z_GridX_RHS`、`KCOpt`、`KC_GridX` 和 `KC_IntAccX`
是相关的——参见
[sec:modelchemistries.mp2.rijcosxrigrad](#sec:modelchemistries.mp2.rijcosxrigrad) 和
[sec:modelchemistries.mp2.2ndder](#sec:modelchemistries.mp2.2ndder) 两节。
使用 GIAO 的 NMR 屏蔽和 g 张量计算适用于 RI-MP2 和双杂化 DFT
（无论是否采用冻结芯）。
相关实现的详细说明见参考文献 [Stoychev2018RIMP2NMR,Tran2020RIMP2GIAO](../../bibliography.md)，
可用选项见
[sec:modelchemistries.mp2.rimp2.response](#sec:modelchemistries.mp2.rimp2.response) 一节。请注意，对于双杂化
DFT，正确的性质会打印在包含 "Method : MP2" 和 "Level : Relaxed density"
的密度标题之后。
DLPNO-MP2（以及双杂化）屏蔽张量同样可用——参见
[sec:modelchemistries.mp2.dlpnoresp](#sec:modelchemistries.mp2.dlpnoresp) 一节。

<a id="sec:spectroscopyproperties.properties.proponly"></a>
## 从已有密度计算性质（Calculating Properties from Existing Densities）

有时，人们可能用 CCSD 等昂贵的关联方法计算了密度矩阵，
事后才发现还需要某个性质（如四极矩或超精细耦合常数
（hyperfine coupling constant，HFCC））。
与其从头重跑整个计算，不如利用已有的密度矩阵来计算这些性质。
为此，我们实验性地引入了"仅计算性质"（properties only）计算模式：
从已有的 *BaseName.gbw* 文件读取分子轨道（MO），
从已有的 *BaseName.densities* 文件读取密度，
仅执行性质计算。
但请注意，这种做法出错的可能性很多，
因此**只应将其作为最后手段，并务必非常谨慎地对待结果**！

以这个 CCSD 计算为例：

```orcainput
! CCSD def2-SVP

%base "BO-CCSD"

%mdci density unrelaxed end

*xyz 0 2
B 0 0 0
O 0 0 1.2049
*
```

这会生成 *BO-CCSD.gbw* 和 *BO-CCSD.densities* 两个文件。
若要在不重复整个计算的情况下获得 CCSD 四极矩和 HFCC，
我们可以把这两个文件复制到一个新目录中（强烈建议这样做！），
并以 `!PropertiesOnly` 关键词启动第二个作业。
请注意，第二个作业的基名（basename）必须完全一致！

```orcainput
! CCSD def2-SVP

%base "BO-CCSD"

%mdci density unrelaxed end

*xyz 0 2
B 0 0 0
O 0 0 1.2049
*
# Everything above must be the same as in the first job!

# Request the property calculations
! PropertiesOnly 
%elprop
  quadrupole true
end
%eprnmr
  Nuclei = all B { Aiso, Adip }
  Nuclei = all O { Aiso, Adip }
end
```
