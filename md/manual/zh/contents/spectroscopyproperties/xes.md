```{index} XES
```

(sec:spectroscopyproperties.xes)=
# 静态基态 DFT（SGS-DFT）（Static Ground State DFT）

## SGS-DFT 对 X 射线谱学的适用性

SGS-DFT 通过利用 Kohn-Sham 方程将多电子体系的复杂性约化到单电子框架，
聚焦于用于计算基态轨道的电子密度。
在这一框架中，激发态问题可以在轨道能量差的基础上构建，
这与激发态方法（如 TD-DFT、ROCIS、RASCI/CASCI/NEVPT2、MRCI/MREOM-CC）
有本质区别。
这种简洁性使其计算高效，
同时在多种 X 射线谱学实验中仍能给出可靠结果，
例如 X 射线吸收谱（X-ray Absorption Spectroscopy，XAS）、
X 射线发射谱（X-ray Emission Spectroscopy，XES）
和共振非弹性 X 射线散射（Resonant Inelastic X-ray Scattering，RIXS）。

SGS-DFT 在价-芯 X 射线发射谱（Valence-to-Core XES，VtC-XES）中
已获得重要应用，
它通过芯空穴跃迁探测价轨道，从而提供对配体-金属相互作用的洞见。
它与 TD-DFT（用于 XAS）等其他单电子方法、
基于波函数的方法（ROCIS、RASCI/CASCI/NEVPT2、MRCI/MREOM-CC）
以及基于配体场的 CI 方法互补，在精度和计算成本之间取得平衡。
关于所有这些方法及其在计算 X 射线谱学谱图中的优势与局限，
参考文献 {cite}`MatheNatRevChem2025` 提供了一篇综合性综述。

## 截面方程总结

本节总结 X 射线谱学（包括 XAS、XES 和 RIXS）中截面的
通用表达式、非相对论表达式和相对论表达式。

指标与符号


$\rho, \rho'$：偶极矩的笛卡尔分量，对 $x, y, z$ 求和，即 $\rho, \rho' \in {x, y, z}$。



$I$：初态（在通用表达式中为基态）。



$F$：通用截面和 XAS 表达式中的末态，对 $F$ 的求和包括所有可能的末态。



$V, V'$：RIXS 表达式中的中间态，能量为 $\epsilon_V, \epsilon_{V'}$。



$i_\sigma, j_\sigma$：非相对论处理中的占据单电子轨道，其中 $\sigma \in {\alpha, \beta}$ 表示自旋。



$a_\sigma$：非相对论处理中的未占据单电子轨道，$\sigma \in {\alpha, \beta}$。



$\nu_\sigma, \nu'_\sigma$：非相对论 RIXS 表达式中的中间态，$\sigma \in {\alpha, \beta}$。



$\omega_{ex}$：激发能（入射辐射频率）。



$\omega_{em}$：发射能（XES 中散射辐射的频率）。



$\omega_{sc}$：散射能（RIXS 中用于散射辐射的频率）。



$\Delta \omega$：RIXS 中的能量转移，通常 $\Delta \omega = \omega_{ex} - \omega_{sc}$。



$\omega_{FI}$：初态 $I$ 与末态 $F$ 之间的跃迁能。



$\omega_{VI}$：初态 $I$ 与中间态 $V$ 之间的跃迁能。



$\omega_{a_\sigma i_\sigma}$：未占据轨道 $a_\sigma$ 与占据轨道 $i_\sigma$ 之间的跃迁能，定义为 $\epsilon_{a_\sigma} - \epsilon_{i_\sigma}$。



$\omega_{j_\sigma i_\sigma}$：占据轨道 $j_\sigma$ 与 $i_\sigma$ 之间的跃迁能，定义为 $\epsilon_{j_\sigma} - \epsilon_{i_\sigma}$。



$\epsilon_{a_\sigma}, \epsilon_{i_\sigma}, \epsilon_{\nu_\sigma}, \epsilon_{\nu'\sigma}$：未占据轨道 $a\sigma$、占据轨道 $i_\sigma$ 以及中间态 $\nu_\sigma, \nu'_\sigma$ 的轨道能量。



$\Gamma, \Gamma_{\nu_\sigma}, \Gamma_{\nu'_\sigma}$：寿命展宽的线宽参数。



$\Gamma_F$：末态 $F$ 的线宽参数。



$c$：光速（原子单位下 $\sim 137$）。



$m$：电偶极跃迁算符，定义为 $m = \sum_i \mathbf{r}_i + \sum_A \mathbf{Z}_A \mathbf{R}_A$，其中 $\mathbf{r}_i$ 是电子坐标，$\mathbf{Z}_A \mathbf{R}_A$ 是核贡献。

通用表达式



- **XAS 截面**

XAS 截面描述从初态 $I$ 到末态 $F$ 的吸收：

$$
\sigma_{\text{XAS}}(\omega_{ex}) = \frac{4\pi}{3c} \omega_{ex} \sum_{F} \sum_{\rho \in \{x, y, z\}} \frac{|\langle F | m_{\rho} | I \rangle|^2}{(\omega_{FI} - \omega_{ex})^2 + \frac{1}{4} \Gamma^2}
$$

或等价地：

$$
\sigma_{\text{XAS}}(\omega_{ex}) = \frac{4\pi}{3c} \omega_{ex} \sum_{F} \sum_{\rho \in \{x, y, z\}} |\langle F | m_{\rho} | I \rangle|^2 f(\omega_{ex}, \omega_{ex}, \Gamma)
$$

- **XES 截面**

XES 截面描述从中间态到末态 $F$ 的发射：

$$
\sigma_{\text{XES}}(\omega_{em}) = \frac{4\pi}{3c} \omega_{em} \sum_{F} \sum_{\rho \in \{x, y, z\}} \frac{|\langle F | m_{\rho} | I \rangle|^2}{(\omega_{FI} - \omega_{em})^2 + \frac{1}{4} \Gamma^2}
$$

- **RIXS 截面**

RIXS 的非弹性散射截面为：

$$
\sigma(\omega_{ex}, \omega_{sc}) = \frac{8\pi}{9c^4} \omega_{ex}^3 \omega_{sc} \sum_{\rho, \rho' \in \{x, y, z\}} |\alpha_{\rho, \rho'}(\omega_{ex}, \omega_{sc})|^2
$$

- **极化率张量**

由 Kramers-Heisenberg-Dirac 表达式给出的极化率张量为：

$$
\alpha_{\rho, \rho'}(\omega_{ex}, \omega_{sc}) = \sum_{V} \sum_{F} \frac{\langle F | m_{\rho'} | V \rangle \langle V | m_{\rho} | I \rangle}{(\omega_{VI} - \omega_{ex} - \frac{i}{2} \Gamma)} + \frac{\langle F | m_{\rho} | V \rangle \langle V | m_{\rho'} | I \rangle}{(\omega_{VI} + \omega_{sc} - \frac{i}{2} \Gamma)}
$$

## 轨道、态与能量

当前的处理基于单一的单电子途径。
轨道来自密度泛函理论（DFT）计算，并满足 Kohn-Sham 方程

$$
F^{\text{KS}} |\rho_{\mathbf{k}} \rangle = \varepsilon_{\mathbf{k}} |\rho_{\mathbf{k}} \rangle
$$

其中 $F^{\text{KS}}$ 是 Kohn-Sham 算符，$| \rho_{\mathbf{k}} \rangle$ 是自旋为 $\sigma_{\mathbf{k}} = 0, \beta$ 的自旋轨道，$\varepsilon_{\mathbf{k}}$ 是轨道能量。Kohn-Sham 算符为：

$$
F^{\text{KS}} = h + \int \left( \frac{\rho(\mathbf{r}')}{|\mathbf{r} - \mathbf{r}'|} \right) d\mathbf{r}' + V^{\text{xc}} [\rho (\mathbf{r})]
$$

其中 $h$ 是单电子哈密顿量（动能加电子-核势，以及可能存在的其他外势），
第二项表示库仑排斥，其中

$$
\rho(\mathbf{r}) = \rho^{\alpha} (\mathbf{r}) + \rho^{\beta} (\mathbf{r}) = \sum_{\mathbf{k}} |\rho^{\alpha} (\mathbf{k})|^2 + \sum_{\mathbf{k}} |\rho^{\beta} (\mathbf{k})|^2
$$

是电子密度，而交换-相关势为：

$$
V^{\text{xc}} [\rho (\mathbf{r})] = \frac{\delta E_{\text{xc}} [\rho]}{\delta \rho (\mathbf{r})}
$$

量 $E_{\text{xc}} [\rho]$ 是交换-相关泛函。
与 Kohn-Sham 过程相关联的是 Kohn-Sham 行列式：

$$
| I \rangle = |i \ldots j \ldots n|
$$

一般而言，电子基态的占据轨道用 $i,j,k,\ldots$ 标记，
未占据轨道用 $a,b,c,\ldots$ 标记。
在单电子途径中，初态、中间态和末态构造为：

$$
| I \rangle &= |i \ldots j \ldots n| \\
| V \rangle &= |a \ldots j \ldots n| \\
| F \rangle &= |a \ldots i \ldots n|
$$

在眼前的具体应用中，轨道 $i$ 是芯层轨道，
例如给定吸收体原子的金属 1s 衍生轨道，
$a$ 是任意未占据轨道（但最重要的是空的金属 d 基轨道），
而 $j$ 是同一原子的另一个芯层轨道。

与其试图获得所有这些态的精确总能量，不如采用简单近似：

$$
\omega_{jk} \approx \varepsilon_{\mathbf{k}} - \varepsilon_{\mathbf{j}}
$$

这当然是相当简化的。就含时 DFT 而言，
可以证明，若 DFT 势中不含 Hartree-Fock 交换，
则轨道能量差是态能量差的一个良定义近似。
对于半定量讨论，这已经足够好，
因为目前所用 DFT 势的较大误差本来就使得计算无法预测精确的跃迁能。

## 单电子轨道基下的非相对论处理

在非相对论处理中，用单电子轨道表示各态。
初态是占据轨道 $i_\sigma$ 的 Slater 行列式，
末态涉及向未占据轨道 $a_\sigma$ 的激发，
其中 $\sigma \in {\alpha, \beta}$ 表示自旋。

- **非相对论 XAS**

非相对论 XAS 截面为：

$$
\sigma_{\text{XAS}}(\omega_{ex}) = \frac{4\pi}{3c} \omega_{ex} \sum_{i_\sigma, a_\sigma} \sum_{\rho \in \{x, y, z\}} \frac{|\langle a_\sigma | m_{\rho} | i_\sigma \rangle|^2}{(\epsilon_{a_\sigma} - \epsilon_{i_\sigma} - \omega_{ex})^2 + \frac{1}{4} \Gamma^2}
$$

或等价地：

$$
\sigma_{\text{XAS}}(\omega_{ex}) = \frac{4\pi}{3c} \omega_{ex} \sum_{i_\sigma, a_\sigma} \sum_{\rho \in \{x, y, z\}} |\langle a_\sigma | m_{\rho} | i_\sigma \rangle|^2 f(\omega_{a_\sigma i_\sigma}, \omega_{ex}, \Gamma)
$$

- **非相对论 XES**

非相对论 XES 截面为：

$$
\sigma_{\text{XES}}(\omega_{em}) = \frac{4\pi}{3c} \omega_{em} \sum_{i_\sigma, j_\sigma} \sum_{\rho \in \{x, y, z\}} |\langle j_\sigma | m_{\rho} | i_\sigma \rangle|^2 f(\omega_{j_\sigma i_\sigma}, \omega_{em}, \Gamma)
$$

- **非相对论极化率张量**

非相对论极化率张量为：


$$
\alpha_{\rho, \rho'}(\omega_{\text{ex}}, \omega_{\text{sc}}) = \sum_{i_\sigma} \sum_{j_\sigma} \sum_{a_\sigma} \langle a_\sigma | m_{\rho} | i_\sigma \rangle \langle i_\sigma | m_{\rho'} | j_\sigma \rangle \left[ \frac{1}{\epsilon_{a_\sigma} - \epsilon_{i_\sigma} - \omega_{\text{ex}} - \frac{i}{2}\Gamma} + \frac{1}{\epsilon_{a_\sigma} - \epsilon_{j_\sigma} + \omega_{\text{sc}} - \frac{i}{2}\Gamma} \right]
$$

或者，若 $\omega_{\text{ex}}$ 调谐到与某个中间态共振，则主导项为：

$$
\left| \alpha_{\rho \lambda}(\varepsilon_a^\sigma - \varepsilon_i^\sigma, \omega_{\text{sc}}) \right|^2 
= \sum_{i_\sigma} \sum_{j_\sigma} \left| 
\langle a_\sigma | m_\rho | i_\sigma \rangle 
\langle i_\sigma | m_\lambda | j_\sigma \rangle 
\right|^2 
\left[
\frac{\Gamma}{
\left( \varepsilon_a^\sigma - \varepsilon_j^\sigma + \omega_{\text{sc}} \right)^2 + \tfrac{1}{4} \Gamma^2
}
\right]
$$


沿 $\omega_{\text{sc}}$ 轴，这是一个中心位于 $\varepsilon_j^\sigma - \varepsilon_a^\sigma$ 的共振。
这表明应提供一组 $(i_\sigma, j_\sigma)$，其跃迁能为 $E_{\omega_{\text{ex}}} = \varepsilon_a^\sigma - \varepsilon_i^\sigma$、$E_{\omega_{\text{sc}}} = \varepsilon_a^\sigma - \varepsilon_j^\sigma$，
以及数值 $\left| \langle a_\sigma | m_\rho | i_\sigma \rangle \right|^2 \left| \langle i_\sigma | m_\lambda | j_\sigma \rangle \right|^2$。
orca_mapspc 之类的工具可以读取线宽，并用线型函数对峰进行卷积，例如：

$$
f(E_{VI}, E_{VF}, \omega_{ex}, \Delta \omega, \Gamma_{V}, \Gamma_{F}) = \left( \frac{\Gamma_V}{(E_{VI} - \omega_{ex})^2 + \frac{1}{4} \Gamma^2} \right)
\left( \frac{\Gamma_F}{(E_{VF} - \Delta \omega)^2 + \frac{1}{4} \Gamma_F^2} \right)
$$

这凸显出 RIXS 实际上是通过在例如 K 边处激发来测量 L 或 M 边。
其他线型（洛伦兹、高斯、Voigt）也是可能的，
详见（placeholder mapspc）一节。

- **非相对论 RIXS**

因此非相对论 RIXS 截面变为：

$$
\sigma_{\text{RIXS}}(\omega_{ex}, \omega_{sc})=
& \frac {8\pi}{9c^4} \omega_{ex}^3 \omega_{sc} \\ 
&\quad \times \sum_{i_\sigma} \sum_{j_\sigma} \sum_{a_\sigma} f(\Delta\omega_{a_\sigma i_\sigma},\Delta\omega_{j_\sigma i_\sigma}, \omega_{ex}, \Delta \omega, \Gamma_V, \Gamma_F)\\
&\quad \times \sum_{\rho, \rho' \in \{x, y, z\}}
|\langle a_\sigma | m_{\rho'} | i_\sigma \rangle \langle i_\sigma | m_{\rho} | j_\sigma \rangle|^2
$$

## 相对论效应的纳入

相对论效应主要有两种类型：
标量相对论（无自旋）效应和自旋-轨道耦合。


- **标量相对论效应**

标量相对论效应可通过 {ref}`sec:essentialelements.relativistic` 所述的各种方案纳入，
方法是修改哈密顿量的单电子部分。
标量相对论效应表现为核附近的吸引势。
因此 $s$ 轨道和 $p$ 轨道被稳定化，$d$ 轨道和 $f$ 轨道被去稳定化。
伴随这些效应，$s$ 和 $p$ 轨道的径向函数将收缩，而 $d$ 轨道的将膨胀。
因此，跃迁偶极矩也会被改变。

- **自旋-轨道耦合（SOC）**


自旋-轨道耦合要棘手得多，因为 SOC 是一个双电子算符，
它耦合不同的自旋流形和纯自旋多重态。
一个良好的近似是自旋-轨道平均场（SOMF）处理 {ref}`sec:spectroscopyproperties.soc`。
此时，SOC 表现为如下形式的有效单电子算符： 

$H_{\text{SOMF}} = \sum_{\mathbf{k}} h^{\text{SOC}} s_{\mathbf{k}}$

- **在单电子框架中纳入 SOC**

在 \textit{ab initio} 量子化学中，可以用 Wigner–Eckart 代数
来显式耦合总自旋 $S$ 的所有 $M_s$ 子态。
这大致对应于原子情形下的 LS 耦合。
对于我们这里使用的 SGS-DFT 途径，这不是一个选项，
因此我们只能采用 $jj$ 耦合类型的处理。
该途径更严格的版本是二分量 DFT 方法。
这里我们尝试这种更精细过程的一个简单版本。
它包括在收敛的非相对论或标量相对论自旋轨道的基下
对角化 Kohn–Sham 算符和 SOC 算符。
于是，本征值方程为：

$$
\left[
\begin{array}{cc}
\epsilon^{\alpha} & 0 \\
0 & \epsilon^{\beta}
\end{array}
\right]
+ \frac{1}{2}
\left[
\begin{array}{cc}
h_z^{\text{SOC}} & h_x^{\text{SOC}} - i h_y^{\text{SOC}} \\
h_x^{\text{SOC}} + i h_y^{\text{SOC}} & -h_z^{\text{SOC}}
\end{array}
\right]
\begin{bmatrix}
\mathbf{p}_{\alpha} \\
\mathbf{p}_{\beta}
\end{bmatrix}
=
\epsilon_n
\begin{bmatrix}
\mathbf{p}_{\alpha} \\
\mathbf{p}_{\beta}
\end{bmatrix}
$$

矩阵元的详细形式为：

$$
\langle p_{\alpha} | {F}^{\alpha} + {s_{z}h_{z}^{\text{SOC}}} | q_{\alpha} \rangle = \delta_{pq}\epsilon_{p}^{\alpha}+i\frac{1}{2} L_{p_{\alpha}q_{\alpha}}
$$

$$
\langle p_{\beta} | {F}^{\beta} + {s_{z}h_{z}^{\text{SOC}}} | q_{\beta} \rangle = \delta_{pq}\epsilon_{p}^{\beta}-i\frac{1}{2} L_{p_{\beta}q_{\beta}}
$$

$$
\langle p_{\alpha} | {F}^{\beta} + {s_{x}h_{x}^{\text{SOC}}} | q_{\beta} \rangle = i\frac{1}{2} L_{p_{\alpha}q_{\beta}}
$$

$$
\langle p_{\beta} | {F}^{\alpha} + {s_{x}h_{x}^{\text{SOC}}} | q_{\alpha} \rangle = i\frac{1}{2} L_{p_{\beta}q_{\alpha}}
$$

$$
\langle p_{\alpha} | {F}^{\beta} + {s_{y}h_{y}^{\text{SOC}}} | q_{\beta} \rangle = -i\frac{1}{2} L_{p_{\alpha}q_{\beta}}
$$

$$
\langle p_{\beta} | {F}^{\alpha} + {s_{y}h_{x}^{\text{SOC}}} | q_{\alpha} \rangle = i\frac{1}{2} L_{p_{\beta}q_{\alpha}}
$$

矩阵元 $L_{pq}$ 是 SOC 算符的空间部分，具有反对称性质 $L_{pq} = -L_{pq}$。

这个复厄米矩阵的对角化给出经 SOC 校正的轨道能量
以及"二分量"轨道，后者是无自旋自旋轨道的线性组合：

$$
| p \rangle = \sum_{r_{\alpha}} V_{r_{\alpha}p} | r_{\alpha} \rangle + \sum_{r_{\beta}} V_{r_{\beta}p} | r_{\beta} \rangle
$$

由这些轨道可以方便地计算跃迁矩：

$$
\langle p | \mathbf{m} | p \rangle = \sum_{r_{\alpha} r_{\alpha}} V_{r_{\alpha}p}^{*}V_{s_{\alpha}q} \langle r_{\alpha} | \mathbf{m} | s_{\alpha} \rangle + \sum_{r_{\beta} r_{\beta}} V_{r_{\beta}p}^{*}V_{s_{\beta}q} \langle r_{\beta} | \mathbf{m} | s_{\beta} \rangle
$$

其中 $V$ 是 $\mathbf{F} + \mathbf{h}^{\text{SOC}}$ 矩阵的本征函数。
有了这些跃迁矩和轨道能量，所有 XAS、XES 和 RIXS 都像之前一样计算；
只是现在具有自旋-轨道标记 $p$。


## X 射线谱学性质的计算

在下面的例子中，我们展示采用常规 BP86 结合 X2C 相对论哈密顿量
和相应三-zeta 基组的各种 X 射线谱学计算。
然而原则上可以改用任何相对论方案 {ref}`sec:essentialelements.relativistic.basissets`。

我们选择显式描述八面体 $\mathrm{Fe}^{\mathrm{III}}$ 配合物
$[\mathrm{Fe}^{\mathrm{III}}\mathrm{Cl}_6]^{3-}$ 的 X 射线计算谱图。

```{literalinclude} ../../orca_working_input/FeCl4_1el_xas_xes.inp
:language: orca
```

由于 SCF-XES 或 SGS-XES 方法的核心涉及在轨道和自旋轨道基中
推导计算 Fe K 边 XAS 以及相应主线 XES 和对应（价-芯）VtC-XES 谱
所需的所有重要量，
这里选择所需的芯层轨道列表，即 $\mathrm{Fe}_{1s}$，
以及相应的轨道（0 和 1）和 SOC 轨道算符（此处为 0 和 1）。
```orca

 CoreOrb 0,0
 OrbOp 0,1
 CoreOrbSOC 0,1

```

我们同时计算：

- $K_{\alpha}$：$\mathrm{Fe}\ 2p \rightarrow \mathrm{Fe}\ 1s$（主线 XES）
- $K_{\beta_{1,3}}$：$\mathrm{Fe}\ 3p \rightarrow \mathrm{Fe}\ 1s$（主线 XES）  
- $K_{\beta_{2,5}}$ / $K_{\beta'}$：$(\mathrm{Cl}\ 2p + \mathrm{Fe}\ 3d) \rightarrow \mathrm{Fe}\ 1s$（VtC-XES）

以及 Fe K 边 XAS 谱。

在非相对论部分，随后在 ORCA 的单光子谱学（One-Photon Spectroscopy）框架内
获得 XAS 和 XES 谱

```orca
--------------------------------------
CALCULATION OF X-RAY EMISSION SPECTRUM
--------------------------------------
Reading and Transforming integrals ... Generating transition densities between Orbitals ... done 
Reading integrals                                                ... 
Reading the Dipole integrals                                     ... done

Calculating the Full-semiclassical Transition moment on transition block:0  ... 
10% done
20% done
30% done
40% done
50% done
60% done
70% done
80% done
90% done
100% done
All done in  (       29.14 sec)
--------------------------------------------------------------------
Using One-Photon Spectroscopy Tool
--------------------------------------------------------------------

----------------------------------------------------------------------------------------------------
              X-RAY   EMISSION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS    
----------------------------------------------------------------------------------------------------
     Transition      Energy     Energy  Wavelength fosc(D2)      D2        DX        DY        DZ   
                      (eV)      (cm-1)    (nm)                 (au**2)    (au)      (au)      (au)  
----------------------------------------------------------------------------------------------------
  1a-a  ->  0a-a   4243.560625 34226628.2     0.3   0.000000000   0.00000   0.00000  -0.00000  -0.00000
  2a-a  ->  0a-a   4243.562891 34226646.5     0.3   0.000000000   0.00000   0.00000   0.00000   0.00000
  3a-a  ->  0a-a   4243.563723 34226653.2     0.3   0.000000000   0.00000  -0.00000   0.00000  -0.00000
  4a-a  ->  0a-a   4243.563845 34226654.2     0.3   0.000000000   0.00000   0.00000   0.00000  -0.00000
  1b-a  ->  0b-a   4243.609379 34227021.5     0.3   0.000000000   0.00000   0.00000  -0.00000  -0.00000
  2b-a  ->  0b-a   4243.611639 34227039.7     0.3   0.000000000   0.00000   0.00000   0.00000   0.00000
  3b-a  ->  0b-a   4243.612467 34227046.4     0.3   0.000000000   0.00000   0.00000  -0.00000   0.00000
  4b-a  ->  0b-a   4243.612590 34227047.4     0.3   0.000000000   0.00000   0.00000   0.00000  -0.00000
  5a-a  ->  0a-a   6174.919612 49804090.7     0.2   0.000000000   0.00000  -0.00000   0.00000   0.00000
  5b-a  ->  0b-a   6176.509051 49816910.3     0.2   0.000000000   0.00000  -0.00000   0.00000   0.00000
  6a-a  ->  0a-a   6296.393596 50783844.5     0.2   0.101316564   0.00066  -0.02354   0.00780  -0.00648
  7a-a  ->  0a-a   6296.393628 50783844.8     0.2   0.101316573   0.00066  -0.00668   0.00037   0.02474
  8a-a  ->  0a-a   6296.393675 50783845.1     0.2   0.101316586   0.00066  -0.00762  -0.02441  -0.00169
  6b-a  ->  0b-a   6297.611741 50793669.5     0.2   0.101563788   0.00066   0.02425  -0.00783   0.00303
  7b-a  ->  0b-a   6297.611770 50793669.7     0.2   0.101563797   0.00066  -0.00317   0.00003   0.02546
  8b-a  ->  0b-a   6297.611810 50793670.1     0.2   0.101563807   0.00066  -0.00777  -0.02443  -0.00094

...

-----------------------------------------------------------------------------
              X-RAY   EMISSION SPECTRUM VIA FULL SEMI-CLASSICAL FORMULATION    
-----------------------------------------------------------------------------
     Transition      Energy     Energy  Wavelength   fosc(FFMIO)
                      (eV)      (cm-1)    (nm)                
-----------------------------------------------------------------------------
  1a-a  ->  0a-a   4243.560625 34226628.2     0.3     0.00000000000264
  2a-a  ->  0a-a   4243.562891 34226646.5     0.3     0.00000000000270
  3a-a  ->  0a-a   4243.563723 34226653.2     0.3     0.00000000000328
  4a-a  ->  0a-a   4243.563845 34226654.2     0.3     0.00000000000163
  1b-a  ->  0b-a   4243.609379 34227021.5     0.3     0.00000000000264
  2b-a  ->  0b-a   4243.611639 34227039.7     0.3     0.00000000000270
  3b-a  ->  0b-a   4243.612467 34227046.4     0.3     0.00000000000327
  4b-a  ->  0b-a   4243.612590 34227047.4     0.3     0.00000000000163
  5a-a  ->  0a-a   6174.919612 49804090.7     0.2     0.00000000000007
  5b-a  ->  0b-a   6176.509051 49816910.3     0.2     0.00000000000006
  6a-a  ->  0a-a   6296.393596 50783844.5     0.2     0.10239197992333
  7a-a  ->  0a-a   6296.393628 50783844.8     0.2     0.10239199025533
  8a-a  ->  0a-a   6296.393675 50783845.1     0.2     0.10239200379726
  6b-a  ->  0b-a   6297.611741 50793669.5     0.2     0.10265622291301
  7b-a  ->  0b-a   6297.611770 50793669.7     0.2     0.10265623313526
  8b-a  ->  0b-a   6297.611810 50793670.1     0.2     0.10265624471656

----------------------------------------
CALCULATION OF X-RAY ABSORPTION SPECTRUM
----------------------------------------
Reading integrals                                                ... 
Reading the Dipole integrals                                     ... done

Calculating the Full-semiclassical Transition moment on transition block:0        ... 
10% done
20% done
30% done
40% done
50% done
60% done
70% done
80% done
90% done
100% done
All done in  (      105.64 sec)
--------------------------------------------------------------------
Using One-Photon Spectroscopy Tool
--------------------------------------------------------------------

----------------------------------------------------------------------------------------------------
              X-RAY ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS    
----------------------------------------------------------------------------------------------------
     Transition      Energy     Energy  Wavelength fosc(D2)      D2        DX        DY        DZ   
                      (eV)      (cm-1)    (nm)                 (au**2)    (au)      (au)      (au)  
----------------------------------------------------------------------------------------------------
  0b-a  -> 45b-a   6988.978848 56369921.9     0.2   0.000000000   0.00000   0.00000   0.00000  -0.00000
  0b-a  -> 46b-a   6988.978999 56369923.1     0.2   0.000000000   0.00000   0.00000  -0.00000  -0.00000
  0b-a  -> 47b-a   6990.167972 56379512.8     0.2   0.000111632   0.00000  -0.00045   0.00053   0.00040
  0b-a  -> 48b-a   6990.168059 56379513.5     0.2   0.000111638   0.00000  -0.00048  -0.00060   0.00026
  0b-a  -> 49b-a   6990.168100 56379513.8     0.2   0.000111637   0.00000  -0.00047   0.00010  -0.00065
  0a-a  -> 50a-a   6992.570956 56398894.2     0.2   0.000000000   0.00000   0.00000   0.00000   0.00000
  0b-a  -> 50b-a   6992.689756 56399852.4     0.2   0.000000000   0.00000  -0.00000   0.00000   0.00000
  0a-a  -> 51a-a   6995.905926 56425792.5     0.2   0.000037002   0.00000  -0.00036  -0.00006   0.00029
  0a-a  -> 52a-a   6995.906125 56425794.1     0.2   0.000036975   0.00000   0.00006  -0.00046  -0.00003
  0a-a  -> 53a-a   6995.906494 56425797.1     0.2   0.000037064   0.00000  -0.00029  -0.00002  -0.00036
  0a-a  -> 54a-a   6996.058845 56427025.9     0.2   0.000006536   0.00000   0.00010  -0.00009   0.00014
  0a-a  -> 55a-a   6996.059201 56427028.8     0.2   0.000006569   0.00000   0.00016   0.00010  -0.00005
  0a-a  -> 56a-a   6996.059311 56427029.7     0.2   0.000006619   0.00000  -0.00004   0.00014   0.00013
  0b-a  -> 51b-a   6996.206394 56428216.0     0.2   0.000014342   0.00000   0.00021  -0.00015  -0.00013

-----------------------------------------------------------------------------
              X-RAY ABSORPTION SPECTRUM VIA FULL SEMI-CLASSICAL FORMULATION    
-----------------------------------------------------------------------------
     Transition      Energy     Energy  Wavelength   fosc(FFMIO)
                      (eV)      (cm-1)    (nm)                
-----------------------------------------------------------------------------
  0b-a  -> 45b-a   6988.978848 56369921.9     0.2     0.00000231997701
  0b-a  -> 46b-a   6988.978999 56369923.1     0.2     0.00000232027335
  0b-a  -> 47b-a   6990.167972 56379512.8     0.2     0.00011661916478
  0b-a  -> 48b-a   6990.168059 56379513.5     0.2     0.00011662652902
  0b-a  -> 49b-a   6990.168100 56379513.8     0.2     0.00011662384321
  0a-a  -> 50a-a   6992.570956 56398894.2     0.2     0.00000000000014
  0b-a  -> 50b-a   6992.689756 56399852.4     0.2     0.00000000000008
  0a-a  -> 51a-a   6995.905926 56425792.5     0.2     0.00004544364720
  0a-a  -> 52a-a   6995.906125 56425794.1     0.2     0.00004540088165
  0a-a  -> 53a-a   6995.906494 56425797.1     0.2     0.00004552596978
  0a-a  -> 54a-a   6996.058845 56427025.9     0.2     0.00001087977536
  0a-a  -> 55a-a   6996.059201 56427028.8     0.2     0.00001092658019
  0a-a  -> 56a-a   6996.059311 56427029.7     0.2     0.00001099716202
  0b-a  -> 51b-a   6996.206394 56428216.0     0.2     0.00001669184884

```

随后程序继续生成经 SOC 校正的轨道

```orca
-----------------------------------------
XES/XAS SPECTRUM WITH SPIN ORBIT COUPLING
-----------------------------------------

Reading the SOC integrals             ... done
Forming the SOC Hamiltonian           ... done
Diagonalizing the SOC Hamiltonian     ... done
-------------------------------
SOC CORRECTED OCCUPIED ORBITALS
-------------------------------
 E[   0] = -6987.772 eV: ( -0.512 +  -0.859 *i)|   0a>
 E[   1] = -6987.756 eV: (  0.002 +  -1.000 *i)|   0b>
 E[   2] = -2744.212 eV: (  0.383 +  -0.924 *i)|   1a>
 E[   3] = -2744.209 eV: ( -0.772 +  -0.636 *i)|   2a>
 E[   4] = -2744.208 eV: ( -0.952 +   0.307 *i)|   3a>
 E[   5] = -2744.208 eV: ( -0.923 +   0.384 *i)|   4a>
 E[   6] = -2744.147 eV: ( -0.001 +  -1.000 *i)|   1b>
 E[   7] = -2744.144 eV: (  0.001 +  -1.000 *i)|   2b>
 E[   8] = -2744.144 eV: (  0.244 +   0.970 *i)|   3b>
 E[   9] = -2744.143 eV: (  0.025 +  -1.000 *i)|   4b>
 E[  10] =  -812.853 eV: (  0.512 +  -0.859 *i)|   5a>
 E[  11] =  -811.247 eV: (  0.163 +   0.987 *i)|   5b>
 E[  12] =  -698.833 eV: (  0.548 +  -0.181 *i)|   6a> (  0.155 +  -0.009 *i)|   7a> (  0.177 +   0.568 *i)|   8a> ( -0.534 +  -0.000 *i)|   7b>
 E[  13] =  -698.431 eV: (  0.072 +  -0.139 *i)|   6a> ( -0.275 +   0.529 *i)|   7a> (  0.393 +  -0.388 *i)|   6b> (  0.392 +   0.394 *i)|   8b>
 E[  14] =  -687.512 eV: ( -0.671 +   0.134 *i)|   6a> ( -0.165 +   0.082 *i)|   7a> (  0.150 +   0.689 *i)|   8a>
 E[  15] =  -687.067 eV: ( -0.092 +   0.176 *i)|   6a> (  0.350 +  -0.673 *i)|   7a> (  0.309 +  -0.305 *i)|   6b> (  0.308 +   0.310 *i)|   8b>
 E[  16] =  -686.654 eV: ( -0.349 +   0.116 *i)|   6a> ( -0.113 +  -0.362 *i)|   8a> ( -0.837 +  -0.000 *i)|   7b>
 E[  17] =  -686.266 eV: (  0.500 +   0.493 *i)|   6b> (  0.499 +  -0.501 *i)|   8b>

```

随后在 SOC 存在下于 OPS 框架中重新计算所有谱图


```orca
Generating transition densities between SOC_Corrected_Orbitals         ... done 
------------------------------------------------------
CALCULATION OF SOC CORRECTED X-RAY EMISSION SPECTRUM  
------------------------------------------------------
Reading integrals                                                ... 
Reading the Dipole integrals                                     ... done

Calculating the Full-semiclassical Transition moment on transition block:0        ... 
10% done
20% done
30% done
40% done
50% done
60% done
70% done
80% done
90% done
100% done
All done in  (       58.75 sec)
--------------------------------------------------------------------
Using One-Photon Spectroscopy Tool
--------------------------------------------------------------------

--------------------------------------------------------------------------------------------------------
   SPIN-ORBIT X-RAY   EMISSION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS    
--------------------------------------------------------------------------------------------------------
      Transition         Energy     Energy  Wavelength fosc(D2)      D2       |DX|      |DY|      |DZ|  
                          (eV)      (cm-1)    (nm)                 (au**2)    (au)      (au)      (au)  
--------------------------------------------------------------------------------------------------------
     2-a  ->  0-a      4243.560625 34226628.2     0.3   0.000000000   0.00000   0.00000   0.00000   0.00000
     2-a  ->  1-a      4243.544569 34226498.7     0.3   0.000000000   0.00000   0.00000   0.00000   0.00000
     3-a  ->  0-a      4243.562891 34226646.5     0.3   0.000000000   0.00000   0.00000   0.00000   0.00000
     3-a  ->  1-a      4243.546835 34226517.0     0.3   0.000000000   0.00000   0.00000   0.00000   0.00000
     4-a  ->  0-a      4243.563723 34226653.2     0.3   0.000000000   0.00000   0.00000   0.00000   0.00000
     4-a  ->  1-a      4243.547667 34226523.7     0.3   0.000000000   0.00000   0.00000   0.00000   0.00000
     5-a  ->  0-a      4243.563845 34226654.2     0.3   0.000000000   0.00000   0.00000   0.00000   0.00000
     5-a  ->  1-a      4243.547790 34226524.7     0.3   0.000000000   0.00000   0.00000   0.00000   0.00000
     6-a  ->  0-a      4243.625435 34227151.0     0.3   0.000000000   0.00000   0.00000   0.00000   0.00000
     6-a  ->  1-a      4243.609379 34227021.5     0.3   0.000000000   0.00000   0.00000   0.00000   0.00000
     7-a  ->  0-a      4243.627694 34227169.2     0.3   0.000000000   0.00000   0.00000   0.00000   0.00000
     7-a  ->  1-a      4243.611639 34227039.7     0.3   0.000000000   0.00000   0.00000   0.00000   0.00000
     8-a  ->  0-a      4243.628523 34227175.9     0.3   0.000000000   0.00000   0.00000   0.00000   0.00000
     8-a  ->  1-a      4243.612467 34227046.4     0.3   0.000000000   0.00000   0.00000   0.00000   0.00000
     9-a  ->  0-a      4243.628646 34227176.9     0.3   0.000000000   0.00000   0.00000   0.00000   0.00000
     9-a  ->  1-a      4243.612590 34227047.4     0.3   0.000000000   0.00000   0.00000   0.00000   0.00000
    10-a  ->  0-a      6174.919612 49804090.7     0.2   0.000000000   0.00000   0.00000   0.00000   0.00000
    10-a  ->  1-a      6174.903556 49803961.2     0.2   0.000000000   0.00000   0.00000   0.00000   0.00000
    11-a  ->  0-a      6176.525107 49817039.8     0.2   0.000000000   0.00000   0.00000   0.00000   0.00000
    11-a  ->  1-a      6176.509051 49816910.3     0.2   0.000000000   0.00000   0.00000   0.00000   0.00000
    12-a  ->  0-a      6288.939050 50723719.5     0.2   0.072768392   0.00047   0.01537   0.01537   0.00000
    12-a  ->  1-a      6288.922994 50723590.0     0.2   0.029738152   0.00019   0.00000   0.00000   0.01389
    13-a  ->  0-a      6289.340683 50726958.9     0.2   0.039112694   0.00025   0.00000   0.00000   0.01593
    13-a  ->  1-a      6289.324627 50726829.4     0.2   0.063473047   0.00041   0.01435   0.01435   0.00000
    14-a  ->  0-a      6300.260175 50815030.6     0.2   0.100751569   0.00065   0.01807   0.01807   0.00000

...

其余谱图表同理
```


所有谱图均用 orca_mapspc 生成，[Options] 用于 XAS、XES、XASFFMIO 和 XESSFFMIO，
包括电偶极（ED）、
完整场-物质相互作用算符（FFMIO），带与不带 SOC：


```orca
   orca_mapspc FileName.out [Options] -x06000 -x18000 -w2.0 -n10000 
```

在电偶极近似（EDA）下以及采用 FFMIO 半经典算符（带与不带 SOC）
计算得到的 XAS 谱如图 {numref}`fig:FeCl4_SGDFT_K_edge_XAS` 所示。

(fig:FeCl4_SGDFT_K_edge_XAS)=
```{figure} ../../images/FeCl4_SGDFT_K_edge_XAS.*

$[FeCl_4]^{1-}$ 计算的 SGS-DFT Fe K 边 XAS 谱比较：
EDA（蓝色）与 FFMIO（红色）近似。
```

随后，采用 FFMIO 半经典算符（带与不带 SOC）
计算得到的 $K_{\alpha}$ 主线 XES 谱如图 {numref}`fig:FeCl4_SGDFT_K_alpha_XES` 所示。
在含 SOC 的情形下，可以清楚地观察到
2p $\rightarrow \mathrm{Fe}\ 1s$（主线 XES）电子衰变过程中
由 2p 芯空穴引起的 SOC 劈裂。

(fig:FeCl4_SGDFT_K_alpha_XES)=
```{figure} ../../images/FeCl4_SGDFT_K_alpha_XES.*

$[FeCl_4]^{1-}$ 计算的 SGS-DFT $K_{\alpha}$ 主线 XES 谱比较：
采用 FFMIO 半经典算符，含 SOC（红色）与不含 SOC（蓝色）校正。
```
在这种态-轨道途径中（原则上在 SGS-DFT 框架内每个轨道激发构成一个态），
在同样的计算设置下，还能额外获得所有可及的电子衰变过程。
这意味着除了
$K_{\beta_{1,3}}$：$\mathrm{Fe}\ 3p \rightarrow \mathrm{Fe}\ 1s$（主线 XES）之外，
$K_{\beta_{2,5}}$ / $K_{\beta'}$：$(\mathrm{Cl}\ 2p + \mathrm{Fe}\ 3d) \rightarrow \mathrm{Fe}\ 1s$（VtC-XES）
也可以获得，如图 {numref}`fig:FeCl4_SGDFT_K_beta_XES` 所示。


(fig:FeCl4_SGDFT_K_beta_XES)=
```{figure} ../../images/FeCl4_SGDFT_K_beta_XES.*

$[FeCl_4]^{1-}$ 计算的 SGS-DFT $K_{\beta}$ 主线 XES（红色）和 VtC XES（蓝色）谱：
采用 FFMIO 半经典算符，含 SOC 校正。
```

在同一框架下，也可以按直接 RIXS 方式计算简单 RIXS 谱……
将在下一个次版本中提供。
关于 RIXS 谱的理论和生成，更多信息请参阅
{ref}`sec:spectroscopyproperties.rocis.rixs` 一节。

SCF-XES 或 SSS-DFT 方法 %xes 块中的完整关键词设置如下
```orca
%xes 
 #-------------------------------
 #    Core Orbital Definitions
 #-------------------------------
 CoreOrb 0,0 # list of core orbitals (alpha,-beta)
 OrbOp 0,1 # operators for core-orbitals (0=alpha,1=beta)
 CoreOrbSOC 0,1 # core orbitals for SOC calculations
 #-------------------------------
 #    RIXS Orbital Definitions
 #-------------------------------
 RIXSOrb    6,7,8,6,7,8       # RIXS final orbitals
 RIXSOrbOp  0,0,0,1,1,1       # operators for these orbitals
 RIXSOrbSOC 12,13,14,15,16,17 # same for SOC
 #-------------------------------
 #    Virtual Orbital Definitions
 #-------------------------------
 MaxNVirt 200 #max number of virtual Orbitals
 #-------------------------------
 #    Spectroscopic Properties
 #-------------------------------
 DoXAS true # Do calculate XAS spectra in addition to XES
 DoSOC true # Do calculate SOC corrected  spectra 
 DoRIXS true # Do calculate RIXS  spectra 
 #-------------------------------
 #    Spectra Intensities
 #-------------------------------
 DoDipoleLength true # Calculate Spectra in Electric Dipole EDA (Length/Velocity) 
 DoFullSemiclassical true # Calculate Spectra in Semiclassical FFMIO framework
end

```

:::{note}
一般不建议用 SGS-DFT 途径计算具有复杂多重态结构的 X 射线谱。
这涉及例如金属 L/M 边 XAS 谱、$K_{\alpha}$：$\mathrm{Fe}\ 2p \rightarrow \mathrm{Fe}\ 1s$ 和
$K_{\beta_{1,3}}$：$\mathrm{Fe}\ 3p \rightarrow \mathrm{Fe}\ 1s$（主线 XES）
以及 RIXS 谱。
此类谱学问题最好基于波函数方法来处理：

- ROCIS 和 CASCI/RASCI（与 NEVPT2 结合）或多参考方法（如 MREOM-CC）以及 MCRPA
能够处理各种此类复杂谱学问题，讨论见
{ref}`sec:spectroscopyproperties.rocis.transMetal`、{ref}`sec:spectroscopyproperties.rocis.rixs`、{ref}`sec:modelchemistries.casscf.XES`、{ref}`sec:spectroscopyproperties.mcrpa`
- 在类似框架下，TD-DFT 已被证明对计算金属和配体 K 边谱很有用，
讨论见 {ref}`sec:spectroscopyproperties.tddft`。
- 芯层谱学谱（目前为金属/配体 K 边 XAS）也可用耦合簇（EOM-CC、STEOM-CC）方法计算，
讨论见 {ref}`sec:spectroscopyproperties.eomcore` 
