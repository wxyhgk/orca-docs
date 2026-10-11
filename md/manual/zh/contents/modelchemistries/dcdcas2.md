```{index} DCD-CAS
```

(sec:modelchemistries.dcdcas2)=
# 动态相关缀饰 CAS（Dynamic Correlation Dressed CAS）

非简并多参考微扰理论（non-degenerate multireference perturbation theory，MRPT）方法
（如 NEVPT2 或 CASPT2）的波函数零阶部分由先前的 CASSCF 计算固定。
如果 CASSCF 的各态在电子组态构成上偏向于错误的态成分，这就会带来问题。
在这种情形下，就需要准简并（quasi-degenerate）或多态（multi-state）表述，
例如 {ref}`sec:modelchemistries.nevpt2.qdnev` 一节所述的 QD-NEVPT2。
这类方法的一个缺点是结果依赖于所纳入的态的数目。
二阶动态相关缀饰完全活性空间方法（2nd order Dynamic Correlation Dressed Complete
Active Space method，DCD-CAS(2)）是一种 CASSCF 后的 MRPT 方法，属于
"先微扰后对角化"（perturb-then-diagonalize）类型，即它能够改变先前 CASSCF
得到的 CAS 波函数{cite}`PathakLang2017DCDCAS`。DCD-CAS(2) 提供了一种替代的非收缩
（uncontracted）途径，它构造一个缀饰（dressed）的 CASCI 矩阵。将其对角化即可给出相关能量
以及在动态相关作用下于 CASCI 空间中重新混合的零阶态{cite}`PathakLang2017DCDCAS`。
当 CASSCF 已经给出良好的零阶波函数时，DCD-CAS(2) 能量与 NEVPT2 相当。

## 非相对论 DCD-CAS(2) 理论（Theory of Nonrelativistic DCD-CAS(2)）

DCD-CAS(2) 方法基于求解如下形式有效哈密顿量（effective Hamiltonian）的本征值问题

$$H_{IJ}^{\text{DCD}, S} = \langle \Phi_I^{SS} | H | \Phi_J^{SS} \rangle - \sum_{K \in \text{FOIS} } \frac{\langle \Phi_I^{SS} | H | \tilde{\Phi}_K^{SS} \rangle \langle \tilde{\Phi}_K^{SS} | H | \Phi_J^{SS} \rangle }{E_K^S - E_0^S}$$

并对每个总自旋 $S$ 分别处理。微扰体（perturber）$|\tilde{\Phi}_K^{SS}\rangle$
的零阶能量 $E_K^S$ 通过在一阶相互作用空间（first-order interacting
space，FOIS，即由相对于 CASCI 空间的所有单双激发构成的空间）中
对角化 Dyall 哈密顿量（Dyall Hamiltonian）得到。该有效哈密顿量呈 CASCI
哈密顿量的形式，但缀饰了动态相关的效应（dynamic correlation dressed，
DCD），方法因此得名。$E_0^S$ 取为相应总自旋 $S$ 的基态 CASSCF 能量。
由于该选择对激发态不如对基态理想，激发能会受到"基态偏置"（ground state
bias）的影响。

对于电子从两个非活性轨道（$ij$）激发到两个虚拟轨道（$ab$）的微扰体所贡献的部分
（在以 CASCI 态为基书写 DCD 哈密顿量时）我们采用替代表达式

$$\langle \Psi_I^{SS} | H^\text{DCD}(ij \rightarrow ab) | \Psi_J^{SS} \rangle = - \delta_{IJ} E_\text{MP2}$$

$$E_\text{MP2} = \sum_{ijab} \frac{(ib|ja)^2 - (ib|ja)(ia|jb) + (ia|jb)^2}{\epsilon_a + \epsilon_b - \epsilon_i - \epsilon_j}$$

由于在这一版本中 $ij\rightarrow ab$ 微扰体类对激发能完全没有贡献
（正如差值专用组态相互作用（difference-dedicated configuration interaction）方法所假设的那样），
我们称之为差值专用 DCD-CAS(2)（difference-dedicated DCD-CAS(2)）方法。
由于 $ij\rightarrow ab$ 类贡献了动态相关能的最大部分，这也同时消除了基态偏置的最主要部分。
DCD-CAS(2) 计算默认采用该选项。为进一步消除其他微扰体类中的基态偏置，
我们还对最终能量施加微扰校正。在一阶（默认选择）下，其形式为

$$\Delta E_I = - \Delta_I \sum_{K \in \text{FOIS} } \frac{\langle \tilde{\Psi}_I | H | \tilde{\Phi}_K\rangle \langle \tilde{\Phi}_K | H | \tilde{\Psi}_I \rangle }{(E_K - E_0)^2}$$

$$\Delta_I = \langle \tilde{\Psi}_I | H | \tilde{\Psi}_I \rangle - E_0$$

其中 $\Delta E_I$ 是对第 $I$ 个 DCD-CAS(2) 根 $|\tilde{\Psi}_I\rangle$ 总能量的校正。

## 自旋相关效应的处理（Treatment of spin-dependent effects）

上述理论对非相对论或标量相对论（scalar-relativistic）哈密顿量 $H$ 成立。
若将其改为哈密顿量 $H+V$，其中 $V$ 包含可能与自旋相关的效应
（如自旋轨道耦合（spin-orbit coupling，SOC）与自旋自旋耦合（spin-spin
coupling，SSC）），我们便得到一种理论{cite}`Lang2019`，其形式类似于包含所有
CAS 根的 QDPT。自旋相关 DCD-CAS(2) 有效哈密顿量的形式为

$$\langle \Phi_I^{SM} | H^\text{DCD} | \Phi_J^{S'M'}\rangle = \delta_{SS'} \delta_{MM'} H_{IJ}^{\text{DCD},S,\text{corr} } + \langle \Phi_I^{SM} | V | \Phi_J^{S'M'} \rangle.$$

$$\mathbf{H}^{\text{DCD}, S, \text{corr} } = \mathbf{C}^\text{DCD} \mathbf{E} (\mathbf{C}^\text{DCD})^T.$$

为构造它，我们首先需要求解标量相对论的 DCD-CAS(2) 问题，
由偏置校正后的能量 $\mathbf{E}$ 与 DCD-CAS(2) CI 系数 $\mathbf{C}^\text{DCD}$
构造矩阵 $\mathbf{H}^{\text{DCD},S,\text{corr} }$，
然后在 CSF 基 $|\Phi_I^{SM}\rangle$ 下计算对 $V$ 有贡献的各算符的矩阵元。

零场分裂（zero field splitting）D 张量通过有效哈密顿量技术提取，
即将模型哈密顿量拟合到由相对论态与能量通过投影到非相对论多重态上
所构造的 des Cloizeaux 有效哈密顿量（见
{ref}`sec:modelchemistries.mrci.soc.zfs` 一节及文献
{cite}`maurice2009`）。当自旋轨道耦合强到相对论态无法唯一归属于
某一个非相对论自旋多重态时，该方法存在局限。

对于由态 $|\Phi\rangle, |\bar{\Phi}\rangle$ 构成的各个 Kramers 双重态
（Kramers doublet），超精细 A 矩阵（hyperfine A-matrix）与 Zeeman g 矩阵
通过比较自旋哈密顿量

$$H_\text{Zeeman} = \mu_B \vec B \cdot g \cdot \vec S$$

$$H_\text{HFC} = \sum_A \vec I^A \cdot A^A \cdot \vec S$$

与多电子 Zeeman 及 HFC 算符在 Kramers 双重态基下的矩阵表示来提取。
由此可得{cite}`Lang2019`

$$\begin{aligned}
  g_{k1} &= 2\Re \langle \bar{\Phi} | L_k + g_e S_k | \Phi \rangle \\
  g_{k2} &= 2\Im \langle \bar{\Phi} | L_k + g_e S_k | \Phi \rangle \\
  g_{k3} &= 2\langle \Phi | L_k + g_e S_k | \Phi \rangle\end{aligned}$$

$$\begin{aligned}
  A_{k1} &= -2\gamma_A \Re \langle \bar{\Phi} | B_k^\text{HFC}(\vec R_A) | \Phi \rangle \\
  A_{k2} &= -2\gamma_A \Im \langle \bar{\Phi} | B_k^\text{HFC}(\vec R_A) | \Phi \rangle \\
  A_{k3} &= -2\gamma_A \langle \Phi | B_k^\text{HFC}(\vec R_A) | \Phi \rangle\end{aligned}$$

其中 $B_k^\text{HFC}(\vec R_A)$ 是核 $A$ 位置处磁场超精细场矢量的第 $k$ 个分量，
$\gamma_A$ 为旋磁比（gyromagnetic ratio）。

## 简单示例（Simple example）

基本用法非常简单：只需一个 `%casscf` 块和简单输入关键词 `!DCD-CAS(2) `。
下面的例子是对 LiF 分子的计算。它有两个单重态，可定性地描述为离子型
（Li$^+$ 与 F$^-$）和共价型（中性 Li 的电子在 2s 轨道上，中性 F 的空穴在
$2p_z$ 轨道上）。在接近平衡几何的距离处，基态为离子型；而在解离极限处，
基态为中性。两者之间的某处存在绝热势能曲线（adiabatic potential energy
curve）的避免交叉（avoided crossing），两个态的性质在此迅速改变
（关于该体系在 (QD)NEVPT2 级别下的势能曲线，见图
{numref}`fig:lifavoided`）。在 CASSCF 级别上，中性态比离子态描述得更好，
结果是后者能量过高，避免交叉发生在过小的原子间距离处。而在避免交叉实际
发生的区域，CASSCF 的态是纯中性或纯离子性的。DCD-CAS(2) 允许在动态相关
作用下于 CASCI 空间中重新混合各态，这将使离子态的能量比中性态降得更多。
输入文件如下：

```{literalinclude} ../../orca_working_input/sample_dcdcas2.inp
:language: orca
```

由于标准初始猜测（`!PAtom`、`!PModel` 等）都无法给出正确的活性轨道
（Li 2s 与 F $2p_z$），我们从文件 casorbs.gbw 中读入它们。我们还使用
`actorbs locorbs` 选项来保持活性轨道的原子特性，从而更容易用中性与离子
成分来解释各态。下面是 LiF 在原子间距离为 5.5 Å 处 CASSCF 与 DCD-CAS(2)
级别下的态组成。

```orca
---------------------------------------------
CAS-SCF STATES FOR BLOCK  1 MULT= 1 NROOTS= 2
---------------------------------------------

ROOT   0:  E=    -106.8043590118 Eh
      0.99395 [     1]: 11
      0.00604 [     2]: 02
ROOT   1:  E=    -106.7485794535 Eh  1.518 eV  12242.2 cm**-1
      0.99396 [     2]: 02
      0.00604 [     1]: 11
```

```orca
---------------------------------------
      DCD-CAS(2) STATES
---------------------------------------

ROOT   0:  E=    -107.0917611937 Eh
      0.60590 [     2]: 02
      0.39410 [     1]: 11
ROOT   1:  E=    -107.0837717163 Eh  0.217 eV   1753.5 cm**-1
      0.60590 [     1]: 11
      0.39410 [     2]: 02
```

可以清楚地看到，CASSCF 的态是纯中性（以组态 `11` 为主）或纯离子性
（以组态 `02` 为主），而 DCD-CAS(2) 的态则是中性与离子性贡献的混合。
该计算表明 5.5 的原子间距离处于避免交叉区域。注意，与 DCD-CAS(2) 态组成
一同打印的能量，是对 DCD-CAS(2) 缀饰哈密顿量对角化所得的能量。
对激发态而言，这些能量会受到我们称之为*基态偏置*的影响
（讨论见原始论文{cite}`PathakLang2017DCDCAS`）。已设计出一种微扰校正来克服
该问题。我们的标准选择是一阶偏置校正。校正后的能量也会打印在输出文件中，
在实际使用 DCD-CAS(2) 方法时应当采用这些能量：

```orca
---------------------------------------------------------
 BIAS-CORRECTED (ORDER 1) STATE AND TRANSITION ENERGIES
=========================================================
 ROOT     Energy/a.u.    DE/a.u.     DE/eV     DE/cm**-1
=========================================================
   0:  -107.093214435   0.000000     0.000       0.0
   1:  -107.084988306   0.008226     0.224    1805.4
```

:::{Warning}
注意，DCD-CAS(2) 计算的计算代价大致随 CASCI 空间大小的三次方增长。
这使得活性空间包含数百个以上 CSF 的计算变得非常昂贵！
:::


## 关键词列表（List of keywords）

以下关键词可与 DCD-CAS(2) 方法配合使用：

```orca
%casscf
  dcdcas true                # Do a DCD-CAS(2) calculation
  diffded true               # Use difference-dedicated DCD-CAS(2) for the 
                             # ij->ab class
  corrorder 1                # Maximum order for the perturbative bias correction
                             # (lower orders come for free)
  dcd_ritrafo false          # Use RI approximation for electron repulsion
                             # integrals

  dcd_soc false              # Relativistic DCD-CAS(2) with spin orbit coupling
  dcd_ssc false              # Relativistic DCD-CAS(2) with direct electronic
                             # spin-spin coupling
  dcd_domagfield 0           # Number of user-specified finite magnetic fields
  dcd_dtensor false          # Calculate an effective Hamiltonian D-tensor
  dcd_nmultd 1               # The number of nonrelativistic multiplets for which 
                             # the D-tensor is calculated
  dcd_gmatrix false          # Calculate an effective Kramers pair Zeeman g-matrix
  dcd_amatrix false          # Calculate an effective Kramers pair Hyperfine
                             # A-matrix
  dcd_kramerspairs 1         # The number of Kramers pairs for which g and/or A
                             # is calculated
  dcd_magnetization false    # Calculate the magnetization of the molecule in an
                             # external magnetic field

  dcd_cascimode false        # Run relativistic calculation in CASCI mode, i.e.
                             # without the dynamic correlation dressing
  dcd_natorbs false          # Calculate natural orbitals for each state and write
                             # them to disk
  dcd_populations false      # Perform population analysis on the DCD-CAS(2) states
end
```

注意，SSC 的计算需要定义辅助基组（auxiliary basis set），因为它只在与 RI
积分联用时实现。如果请求 `dcd_magnetization`，所用的磁通量密度与温度值
可通过 `%casscf` 块中 `rel` 子块的关键词 `MAGTemperatureMIN`、
`MAGTemperatureMAX`、`MAGTemperatureNPoints`、`MAGFieldMIN`、
`MAGFieldMAX`、`MAGNpoints` 来指定（见
{ref}`sec:modelchemistries.mrci.soc.magnet` 一节）。若关键词
`dcd_domagfield` 设为非 0 的数，则磁场可以以 xyz 坐标矩阵的形式输入
（单位为高斯），例如

```orca
%casscf
  dcdcas true
  ...
  dcd_domagfield 2
  dcd_magneticfields[0] = 10000, 0, 0
  dcd_magneticfields[1] = 0, 10000, 0
end
```

此外还有关键词 `DCD_EDIAG`，在以 CASCI 模式运行 DCD-CAS(2) 代码时，
它的作用类似于 `%mrci` 块中 `soc` 子块的关键词 `EDiag`（见
{ref}`sec:modelchemistries.mrci.soc.zfs` 一节）。能量应以原子单位输入，例如

```orca
%casscf
  ...
  dcdcas true
  dcd_cascimode true
  dcd_soc true
  DCD_EDIAG[0] -2220.920028
  DCD_EDIAG[1] -2220.834377
  DCD_EDIAG[2] -2220.835871
  DCD_EDIAG[3] -2220.810290
  DCD_EDIAG[4] -2220.812293
  DCD_EDIAG[5] -2220.756732
end
```
