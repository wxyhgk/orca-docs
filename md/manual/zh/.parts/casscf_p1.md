(sec:modelchemistries.casscf)=
# 完全与不完全活性空间自洽场（CASSCF 与 RAS/ORMAS）
```{index} CASSCF
```

(sec:modelchemistries.casscf.intro)=
## 引言

完全活性空间自洽场（complete active space self-consistent field, CASSCF）方法是多组态 SCF 方法的一种特殊形式，
可以看作 Hartree-Fock 方法的扩展。它是研究静态相关效应的非常强大的方法，
也是 MR-CI 和 MR-PT 处理的坚实基础。它可以应用于基态和激发态或它们的平均。
ORCA 中的实现相当通用，也允许省略活性-活性旋转的不完全活性空间。
此类[不完全模型空间](casscf.modelspace)的例子包括任意参考组态、限制活性空间（RAS）和占据限制多重活性空间（ORMAS）。
在接下来的章节中，主要重点是完全活性空间。

该主题相当复杂，最终需要用户大量的洞察才能成功。
因此，除手册中的材料外，我们还创建了 [CASSCF 教程](https://orcaforum.kofo.mpg.de/app.php/dlext/?cat=4&sid=9d58efcf2208abe23b1af87a601b42f6)，
涵盖了计算设计和程序使用的许多实用技巧。

有几种情况下 CASSCF 处理是个好主意：

-   来自多个近简并组态（静态相关）的具有显著多参考特征的波函数

-   需要多行列式处理的波函数（例如原子、离子、过渡金属配合物的多重态）

-   键断裂或部分断裂的情况。

-   生成在多个态的要求之间折中的轨道。

-   作为涵盖动态相关的多参考方法（NEVPT2、MRCI、MREOM 等）的起点。

-   为多行列式/多参考波函数生成真正的自旋本征函数。
    
在所有这些情况下，单行列式 Hartree-Fock/DFT 方法严重失效，而 CASSCF 仍是好的选择。
在后者中，轨道被分为三个子空间：(a) 在所有组态状态函数（CSF）中双占据的内部（非活性）轨道；(b) 部分占据的（活性）轨道；(c) 在所有 CSF 中为空的虚（外部）轨道。

固定数量的电子被分配到内部子空间和活性
子空间。如果 $N$ 个电子在 $M$ 个轨道中是"活性的"，就称其为
CASSCF($N$,$M$) 波函数。$N$ 个电子在 $M$ 个
轨道中的所有自旋本征函数都包含在组态相互作用步骤（CAS-CI）中，并且
能量关于 MO 和 CI 系数的变化取驻定值。可以计算任意数量不同多重度的任意数量的根，CASSCF 能量可以针对用户定义的这些态的平均进行优化。

CASSCF 方法有一个很好的优点，即它是完全变分的，这使得解析梯度的计算相对容易。
因此，CASSCF 方法可用于几何优化和数值频率计算。应当注意，态平均
CASSCF 计算一般不是完全变分的。
轨道必须针对感兴趣的态进行优化。

ORCA 中提供了许多性质（g-张量、ZFS 分裂、CD、MCD、磁化率、偶极矩等）。大多数 CASSCF
性质（如 EPR 参数）在[拟简并微扰理论](sec:spectroscopyproperties.qdpt_magnetic_properties)框架中计算。
此外，一些性质（如 ZFS 分裂）也可以通过微扰理论计算或从有效哈密顿量严格提取。
关于可用性质和选项的详细描述，参见第
{numref}`sec:modelchemistries.casscf.properties` 节。上述所有性质都在 CASSCF 模块内计算。
例外是 [Mössbauer 参数](sec:spectroscopyproperties.moessbauer)，当密度（在密度容器中）可用时，它们使用 `%EPRNMR` 块中的常用关键词计算。一般而言，`%EPRNMR` 块中的性质使用线性响应理论导出。后者对 CASSCF 波函数的扩展在第 {numref}`sec:spectroscopyproperties.casscfresp` 节中针对几个选定的性质报告。

:::{note} 注意
CASSCF 模块承载了 [CASPT2](sec:modelchemistries.caspt2) 和 [NEVPT2](sec:modelchemistries.nevpt2) 方法及其变体。更高阶的多参考理论（例如 [FIC-NEVPT4(sd)](sec:modelchemistries.autoci.ficnevpt.nevpt4)）可以在 [AutoCI 模块](sec:modelchemistries.autoci)和 [MRCI 模块](sec:modelchemistries.mrci)中找到。
:::

## 理论
```{index} CASSCF Theory
```

将态记为 $I$，其自旋记为 $S$，CASSCF 波函数写为

$$\left| \Psi_I^S \right\rangle= \sum_{k} { C_{kI} \left| \Phi_k^S \right\rangle}.
$$ 

这里波函数在一组组态状态函数（CSFs）中展开，
它们是适应总自旋 $S$ 的行列式的线性组合。

为了定义实际的 CSF 集（$\Phi_{I}^{S}$），分子轨道空间被划分为三个用户定义的子空间：

 * "非活性轨道"是在所有 CSF 中双占据的轨道。
 * "活性轨道"是在 CSF 中占据数可变的轨道。
 * "外部轨道"在所有 CSF 中为空。
 
完全模型空间 CAS($N$,$M$) 包括所有 CSF，它们产生于完全组态相互作用（FCI），
其中 $N$ 个活性电子分布在 $M$ 个活性轨道中，而系统的其余电子位于双占据的非活性轨道中。**活性轨道是拟设的核心，必须由用户谨慎选择。** CSF 的数量随活性电子和轨道的数量极快增长（基本上是阶乘级的）。取决于实际体系，可行性的极限大约在 $\sim$14 个活性轨道或活性空间中约一百万个 CSF。更大的活性空间可以用近似 FCI 求解器（如[迭代组态展开 CI（ICE-CI）](sec:modelchemistries.iceci)）或[密度矩阵重整化群（DMRG）方法](sec:modelchemistries.dmrg)来处理。[^approxfci] 在某些情况下，[不完全模型空间（如 RAS 或 ORMAS）](casscf.modelspace)是可行的替代方案。

展开系数 $C_{kI}$ 代表第一组变分参数。每个 CSF 由一组公共的正交归一分子轨道
$\psi_{i} \left({ \mathrm{\mathbf{r} }} \right)$ 构建，后者又在基函数中展开：
$\psi_{i} \left({ \mathrm{\mathbf{r} }} \right)=\sum\nolimits_\mu{c_{\mu i} \phi_{\mu } \left({ \mathrm{\mathbf{r} }} \right)}$。
MO 系数 $c_{\mu i}$ 构成第二组变分参数。

CASSCF 波函数的能量由 Rayleigh 商给出

$$E\left({ \mathrm{\mathbf{c} },\mathrm{\mathbf{C} }} \right)=\frac{\left\langle { \Psi
_{I}^{S} \left|{ \hat{{H} }_{\text{BO} } } \right|\Psi_{I}^{S} } \right\rangle}{\left\langle { \Psi_{I}^{S} \left|{ \Psi_{I}^{S} } \right.} \right\rangle},
$$ 

它是真实总能量的上界。然而，CASSCF 计算*不是*为提供接近精确能量的总能量值而设计的。CASSCF 计算的目的是提供定性正确的波函数，为动态电子相关的处理形成良好的起点。

CASSCF 方法是完全变分的，即能量关于 MO 和 CI 两组系数的变化取驻定值。收敛时，能量关于 MO 和 CI 系数的梯度消失

$$\frac{\partial E\left({ \mathrm{\mathbf{c} },\mathrm{\mathbf{C} }} \right)}{\partial
c_{\mu i} }=0,
$$

$$\frac{\partial E\left({ \mathrm{\mathbf{c} },\mathrm{\mathbf{C} }} \right)}{\partial
C_{kI} }=0.
$$ 

对于完全模型空间，波函数和能量关于三个子空间内的幺正变换是不变的。因此，子空间内的轨道仅定义到相差一个幺正变换，程序需要做出某种正则化选择。在 ORCA 中，[最终轨道](sec:modelchemistries.casscf.actorbs)默认是：

 *  活性空间中的自然轨道，

 *  在内部空间中对角化 CASSCF Fock 矩阵的轨道和

 *  在外部空间中对角化 CASSCF Fock 矩阵的轨道。

### CASSCF 波函数的优化

一般而言，除 trivial 情况外，CASSCF 波函数比 RHF（或 UHF）波函数难优化得多。根本原因是 **c** 和 **C** 的变化可能强烈耦合，能量泛函在（**c**，**C**）空间中可能有许多局部极小值。因此，起始轨道的选择确实非常重要，选择哪些轨道和电子包含在活性空间中对 CASSCF 研究的成功有决定性影响。

一般而言，变换到自然轨道后，可以根据占据数对活性空间轨道进行分类，占据数在 0.0 到 2.0 之间变化。一般而言，如果将占据数接近零或接近 2.0 的轨道包含在活性空间中，几乎肯定会出现收敛问题。占据数在 0.02 到 1.98 之间通常非常合理，不应导致大的收敛问题。出现收敛问题的原因是，如果活性轨道几乎双占据，能量对内部和活性轨道之间旋转的依赖性非常弱，对于外部和弱占据活性轨道之间的旋转也是如此。然而，在某些情况下（例如在研究势能面时），可能无法避免将弱占据或几乎非活性的轨道包含在活性空间中，在这些情况下需要使用最强大的收敛辅助手段（*见下文*）。

除 [TRAH-CASSCF](sec:modelchemistries.casscf.trah) 求解器{cite}`Helmich-Paris2022`外，
ORCA 的实现遵循[两步过程](sec:modelchemistries.casscf.2step)，其中在每个循环（宏迭代）中，在当前分子轨道集下求解 CAS-CI 问题。然后用幺正矩阵 U 更新轨道系数

$$\mathrm{\mathbf{c} }^{\text{new} }=\mathrm{\mathbf{c} }^{\text{old} }\mathrm{\mathbf{U} }$$

然后开始新的循环。重复该过程直到收敛，即能量不再变化（默认 `ETol 1e-8`）或轨道梯度接近零（默认 `GTol 1e-3`）。相比之下，[一步拟设](sec:modelchemistries.casscf.trah)同时更新轨道系数和 CI 系数。

在两种情况下，幺正变换都用反对称矩阵参数化（$X_{pq} =-X_{qp}$）

$$\mathrm{\mathbf{U} }=\exp \left({\mathrm{\mathbf{X} }} \right),$$ 

其中 $X_{pq}$ 由非冗余轨道旋转（子空间间）组成。

与单行列式波函数（RHF、UHF、RKS、UKS）的情况一样，存在一阶收敛方法，
例如当前默认的微扰 SuperCI（`SuperCI_PT`）{cite}`kollmarSXPT2019`，它们只需要轨道梯度

$$\frac{\partial E\left({ \mathrm{\mathbf{X} },\mathrm{\mathbf{C} }} \right)}{\partial
X_{pq} }.$$ 

所需的变换积分 $(tu|vx)$（$tuv$ 为活性轨道，$x$ 属于任何子空间）非常少，即使对于较大的计算也很容易保存在中央存储中。
