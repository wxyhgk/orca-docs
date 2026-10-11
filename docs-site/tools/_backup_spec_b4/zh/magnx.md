

<a id="sec:spectroscopyproperties.magnx"></a>
# 破缺对称波函数与交换耦合（Broken-Symmetry Wavefunctions and Exchange Couplings）

用于估算唯象参数 $J_{\mathrm{AB} }$ 的一种流行方法是
"破缺对称"（broken-symmetry）形式。
该参数出现在 Heisenberg--Dirac--van Vleck 哈密顿量中，
用于参数化两个自旋体系之间的相互作用。
该唯象哈密顿量为：

$$

H_{\mathrm{HDvV} } = -2J_{\mathrm{AB} } \vec{{S} }_{\mathrm{A} } \vec{{S} }_{\mathrm{B} }\qquad \text{(eqn:HDvV)}

$$

不难证明，这样的哈密顿量会产生从 $S=S_{\mathrm{A} } + S_{\mathrm{B} }$
到 $S=\left|{ S_{\mathrm{A} } - S_{\mathrm{B} }} \right|$ 的自旋态"阶梯"。
若参数 $J_{\mathrm{AB} }$ 为正，则称体系 "A" 与 "B" 为
*铁磁*（ferromagnetically）耦合，因为最高自旋态能量最低；
而若 $J_{\mathrm{AB} }$ 为负，则耦合为
*反铁磁*（antiferromagnetic），最低自旋态能量最低。

在破缺对称形式中，人们试图获得一个破坏空间（和自旋）对称性的波函数。
它可以被看作一种"穷人版 MC-SCF"，
在单行列式框架内模拟多行列式特征。
关于该方法背后的理论优势、劣势、问题和假设，可以谈很多。
这里我们只想说明这一形式如何在 ORCA 中应用。

对于定域在"位点 A"上的 $N_{\mathrm{A} }$ 个未配对电子
和定域在"位点 B"上的 $N_{\mathrm{B} }$ 个未配对电子，
可通过两次独立的自旋非限制 SCF 计算来计算参数 $J_{\mathrm{AB} }$：
(a) 高自旋态计算，$S=\frac{\left({ N_{\mathrm{A} } + N_{\mathrm{B} }} \right)}{2}$；
(b) "破缺对称"计算，$M_{S} = \frac{\left({ N_{\mathrm{A} } -N_{\mathrm{B} } }
\right)}{2}$，其中 $N_{\mathrm{A} }$ 个自旋向上电子准定域在"位点 A"上，
$N_{\mathrm{B} }$ 个自旋向下电子准定域在"位点 B"上。
提取 $J_{\mathrm{AB} }$ 有若干种形式：
[GinsbergJACS1980,NoodlemanJCP1981,NoodlemanCP1986,BenciniJACS1980,Yamaguchi1986,SodaCPL2000](../../bibliography.md)。

$$

J_{\mathrm{AB} } = - \frac{\left({ E_{\mathrm{HS} } -E_{\mathrm{BS} } } \right)}{\left({ S_{\mathrm{A} } +S_{\mathrm{B} } } \right)^{2} }\qquad \text{(eqn:J_weak)}

$$

$$

J_{\mathrm{AB} } = -\frac{\left({ E_{\mathrm{HS} } -E_{\mathrm{BS} } } \right)}{\left({ S_{\mathrm{A} } +S_{\mathrm{B} } } \right)\left({ S_{\mathrm{A} } +S_{\mathrm{B} } +1} \right)}\qquad \text{(eqn:J_strong)}

$$

$$

J_{\mathrm{AB} } =-\frac{\left({ E_{\mathrm{HS} } -E_{\mathrm{BS} } } \right)}{\left\langle { S^{2} } \right\rangle_{\mathrm{HS} } -\left\langle { S^{2} } \right\rangle_{\mathrm{BS} } }\qquad \text{(eqn:J_Yamaguchi)}

$$

我们倾向于采用最后一种定义（式
[Eq](#eqn:J_Yamaguchi)），因为它在整个耦合强度范围内都近似成立，
而第一个公式对应弱耦合极限，第二个对应强耦合极限。

要应用破缺对称形式，请使用：

```orca
%scf BrokenSym NA,NB
     end
```

程序随后会执行若干步骤。
本质上，它先计算高自旋态的能量和波函数，
然后定域轨道，再重新收敛到破缺对称态。

!!! note
    请确保在你的输入坐标中，"位点 A" 是包含较多未配对电子的位点！

该形式最常用于过渡金属配合物中的自旋耦合、金属-自由基耦合，
或均裂键断裂情形下势能面的计算。
总体而言，杂化 DFT 方法对实验观测到的劈裂
似乎能给出合理的半定量结果。

作为一个例子，考虑下面这个拉伸 Li$_{2}$ 分子中
单重态-三重态劈裂的简单计算：

```orca
%scf BrokenSym NA,NB
     end
```

在 ORCA 中还有第二种生成破缺对称解的机制。
该机制利用各个自旋密度，通过关键词 `FlipSpin` 和 `FinalMs` 调用。
其策略是：在收敛高自旋波函数之后，
在用户指定的中心上交换密度矩阵的 $\alpha$ 和 $\beta$ 自旋块。
用这一方法应当可以实现任意的自旋拓扑。用法很简单：

```orca
#
# Example of a broken symmetry calculation
#
! B3LYP DEF2-SVP TightSCF
%scf BrokenSym 1,1
     end
* xyz 0 3
  Li  0  0  0
  Li  0  0  4
*
```

最后，你也可以尝试用 SCF 稳定性分析功能来破坏对称性
（参见 [sec:essentialelements.stabilityanalysis](#sec:essentialelements.stabilityanalysis) 一节）。
基态自旋态可通过 **ORCA-ECA** 工具对上述自旋哈密顿量作对角化得到
（参见 [sec:utilities.eca](#sec:utilities.eca)）。

## 近似自旋投影方法（Approximate Spin Projection Method）

近似自旋投影（approximate spin projection，AP）方法由 Yamaguchi 及其同事提出，
是一种从交换耦合常数中去除自旋污染的技术。[Yamaguchi1986,Yamaguchi1988,Saito2010](../../bibliography.md)
在该方案中，体系的能量由下式给出

$$

E_{\mathrm{AP} }=\alpha E_{\mathrm{BS} }-\left(\alpha - 1\right)E_{\mathrm{HS} }\qquad \text{(eq_eap)}

$$

参数 $\alpha$ 计算为

$$

\alpha=\frac{S^{\mathrm{HS} }\left(S^{\mathrm{HS} }+1\right) - S_Z^{\mathrm{BS} }\left(S_Z^{\mathrm{BS} }+1\right)}{\langle\hat{\mathbf{S} }^2\rangle^{\mathrm{HS} }-\langle\hat{\mathbf{S} }^2\rangle^{\mathrm{BS} }}\qquad \text{(alpha_yam)}

$$

其中，$S_Z^{\mathrm{BS} }$ 是 BS 态总自旋的 $z$ 分量
（$S_Z^{\mathrm{BS} }=(N_{\alpha}-N_{\beta})/2$）。
另外，也可采用 Noodleman 方案，[NoodlemanCP1986](../../bibliography.md) 其中
$\alpha$ 计算为

$$

\alpha=\frac{S^{\mathrm{HS} }\left(S^{\mathrm{HS} }+1\right) - S_Z^{\mathrm{BS} }\left(S_Z^{\mathrm{BS} }+1\right)}{\left(S^{\mathrm{HS} }\right)^2}\qquad \text{(alpha_nood)}

$$

或 Ruiz 方案，[Ruiz_BS_1999](../../bibliography.md) 其中 $\alpha$ 等于

$$

\alpha=\frac{S^{\mathrm{HS} }\left(S^{\mathrm{HS} }+1\right) - S_Z^{\mathrm{BS} }\left(S_Z^{\mathrm{BS} }+1\right)}{S^{\mathrm{HS} }\left(S^{\mathrm{HS} }+1\right)}\qquad \text{(alpha_ruiz)}

$$

通过 `%scf` 块中的 `APMethod` 标签请求 AP 方法：

```orca
%scf BrokenSym NA,NB
     APMethod 3  # 1 = Noodleman
                 # 2 = Ruiz
                 # 3 = Yamaguchi
end
```

默认为 `APMethod 0`，对应普通的 BS 计算。
Yamaguchi 的 AP 方法可用于单点能计算和几何优化。
若在 Yamaguchi AP 方法的框架下进行几何优化，
则式 [Eq](#eq_eap) 对核位移 $X$ 的梯度为

$$

\frac{\partial E_{\mathrm{AP} }}{\partial X}=\alpha\frac{\partial E_{\mathrm{BS} }}{\partial X}-\left(\alpha-1\right)\frac{\partial E_{\mathrm{HS} }}{\partial X}+\frac{\partial\alpha}{\partial X}\left(E_{\mathrm{BS} } - E_{\mathrm{HS} }\right)\qquad \text{(der_alpha_yam)}

$$

最后一项包含导数 $\frac{\partial\alpha}{\partial X}$。
ORCA 采用 Saito 和 Thiel 提出的形式，
即在每个几何优化循环中求解 CP-SCF 方程。[Saito2012](../../bibliography.md)
这种计算的代价高于采用 Noodleman 或 Ruiz 方案
（此时 $\frac{\partial\alpha}{\partial X}=0$）。

<a id="sec:spectroscopyproperties.magnx.decompositionpath"></a>
# 磁交换耦合的分解（Decomposition of the Magnetic Exchange Coupling）

分解方法（[DecompositionPath_2013,DecompositionPath_2015,DecompositionPath_2020,DecompositionPath_2023a](../../bibliography.md)）旨在
基于高自旋（HS）与破缺对称行列式的逐步弛豫，
提取两个磁位点 $A$ 和 $B$ 之间磁交换耦合 $J_{ab}$ 的主要物理贡献。
ORCA 中目前的实现针对含两个磁中心的体系，基于 Yamaguchi 公式。
对于包含更多中心的体系，Yamaguchi 公式不再适用，
分解需要不同的策略；为此提供了一个用于生成 ORCA 分解输入文件的工具，
见[此处](https://gitlab.com/gdavid123/input-files-generator)。([DecompositionPath_2023b,DecompositionPath_2024](../../bibliography.md)) 

基于 Heisenberg-Dirac-van Vleck 哈密顿量，

$$

H_\text {HDvV} = -2J_{AB}\vec{S}_A\vec{S}_B

$$

磁交换耦合可分解为三个主要物理贡献：
i) 磁中心之间的铁磁直接交换 $J_0$；
ii) 反铁磁动力学交换贡献 $\Delta J_\text {KE}$，反映低自旋态中磁中心的弛豫；
iii) 自旋极化效应 $\Delta J_\text {SP}$，
对应于 HS 与 BS 行列式中芯层（非磁性）轨道的差别响应，
视体系而定，它可以是铁磁或反铁磁的。

为从 DFT 或 HF 计算中提取这些贡献，
先从 HS 态计算得到一组起始轨道，
可采用开壳层限制形式（HS.RO）或准限制开壳层形式（HS.qRO）。
这定义了一组双占据分子轨道和一组单占据轨道（SOMO），数量与未配对电子数一致。
随后（默认）用 Pipek-Mezey 方法对 SOMO 进行定域化，
得到一组定域磁轨道。
通过翻转与其中一个中心相关联的电子的自旋，
得到第一个 BS 行列式，其能量在不优化任何轨道的情况下计算（BS.NOpt）。
利用 HS.RO 和 BS.NOpt 行列式，第一个直接交换贡献可计算为

$$

J_0 = -\frac{E_\text{HS.RO}-E_\text{BS.NOpt} }{\left < S^{2} \right >_\text{HS.RO} - \left < S^{2} \right >_\text{BS.NOpt } }

$$

或用 HS.qRO 表示为

$$

J_0 = -\frac{E_\text{HS.qRO}-E_\text{BS.NOpt} }{\left < S^{2} \right >_\text{HS.qRO} - \left < S^{2} \right >_\text{BS.NOpt} }

$$

为计算第二个动力学交换贡献，
从 BS.NOpt 行列式出发，在冻结芯层（非磁性）轨道的场中弛豫磁轨道，
得到新的 BS 冻结芯行列式（BS.FC）。
利用 BS.FC 与 HS.RO 或 HS.qRO 行列式，并扣除直接交换贡献，
即可计算动力学交换：

$$

\Delta J_\text{KE} = -\frac{E_\text{HS.(q)RO}-E_\text{BS.FC} }{\left < S^{2} \right >_\text{HS.(q)RO} - \left < S^{2} \right >_\text{BS.FC} } - J_0

$$

自旋极化效应的贡献则通过允许芯层轨道弛豫、
同时冻结磁轨道（FM）来计算：
分别从 HS.RO/HS.qRO 和 BS.NOpt 行列式出发，
得到 HS.FM 和 BS.FM 行列式。
利用这两个新行列式并扣除直接交换贡献，
自旋极化效应可评估为

$$

\Delta J_\text{SP} = -\frac{E_\text{HS.FM }-E_\text{BS.FM} }{\left < S^{2} \right >_\text{HS.(q)RO} - \left < S^{2} \right >_\text{BS.Nopt} } - J_0

$$

除了通常对完全弛豫的 HS 与 BS 行列式使用 Yamaguchi 公式外，
磁交换耦合也可通过将这三个贡献求和得到，
即所谓的再组合（Recomposition）方法：

$$

J_\Sigma = J_0 + \Delta J_\text{KE} + \Delta J_\text{SP}

$$

要使用分解方法：

```orca
%scf DecompositionPath NA,NB
     end
```
其中 `NA` 和 `NB` 分别是位点 $A$ 和 $B$ 中的未配对电子数。
程序随后会执行上述若干步骤来完成分解。
要以 HS.RO 作为轨道的参考定义，必须使用 HFTyp=ROHF；
而对于 HS.qRO，则必须使用 HFTyp=UHF。

!!! note
    请确保在你的输入坐标中，"位点 A" 是包含较多未配对电子的位点！

