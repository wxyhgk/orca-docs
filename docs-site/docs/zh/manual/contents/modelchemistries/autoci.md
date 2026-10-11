

<a id="sec:modelchemistries.autoci"></a>
# 基于自动代码生成的相关方法（AUTOCI）

AUTOCI 模块汇集了多种方法，其中若用手工实现将十分繁琐甚至实际上不可能。
该模块可与 ORCA 中所有类型的参考波函数（reference wave function）协同工作，
即 RHF、ROHF、UHF 和 [CASSCF](CASSCF.md#sec:modelchemistries.casscf)，并提供 CI 及相关方法。

所有方法均在正则轨道基（canonical orbital basis）中实现，并将所有积分存储在磁盘上。

<a id="sec:modelchemistries.autoci.introduction"></a>
## 简介（Introduction）

所有理论均通过 ORCA-AGE（Automated Generator Environment for ORCA，ORCA 自动
生成器环境）中的自动化编程手段获得[krupicka2017ORCA_AGE,lechner2024code](../../bibliography.md)。
CI 模块读入 SCF 波函数并优化 CI 展开的系数。从概念上讲，该模块与 `orca_mdci`
类似，因此输入与输出有许多共同之处。

<a id="sec:modelchemistries.autoci.available"></a>
## 基本用法/功能列表（Basis Usage / List of Features）

目前 AUTOCI 中实现了以下单参考（single-reference）方法。

| 参考波函数    | 相关方法          | 能量          | 梯度          | 
| ------------- | ----------------- | ------------- | ------------- |
| RHF           | CID               | &check;       | &check;       |
| RHF           | CISD              | &check;       | &check;       |
| RHF           | CISDT             | &check;       |               |
| RHF           | CCD               | &check;       | &check;       |
| RHF           | CCSD              | &check;       | &check;       |
| RHF           | CCSD[T]           | &check;       | &check;       |
| RHF           | CCSD(T)           | &check;       | &check;       |
| RHF           | CCSDT             | &check;       |               |
| RHF           | CEPA(0)           | &check;       | &check;       |
| RHF           | CC2               | &check;       |               |
| RHF           | QCISD             | &check;       |               |
| RHF           | MP2               | &check;       | &check;       |
| RHF           | MP3               | &check;       | &check;       |
| RHF           | MP4               | &check;       | &check;       |
| RHF           | MP4(SDQ)          | &check;       | &check;       |
| UHF           | CID               | &check;       | &check;       |
| UHF           | CISD              | &check;       | &check;       |
| UHF           | CISDT             | &check;       | &check;       |
| UHF           | CCD               | &check;       | &check;       |
| UHF           | CCSD              | &check;       | &check;       |
| UHF           | CCSD[T]           | &check;       | &check;       |
| UHF           | CCSD(T)           | &check;       | &check;       |
| UHF           | CCSDT             | &check;       | &check;       |
| UHF           | CCSDTQ            | &check;       |               |
| UHF           | CCSDT-1           | &check;       |               |
| UHF           | CCSDT-2           | &check;       |               |
| UHF           | CCSDT-3           | &check;       |               |
| UHF           | CCSDT-4           | &check;       |               |
| UHF           | CEPA(0)           | &check;       | &check;       |
| UHF           | CC2               | &check;       |               |
| UHF           | CC3               | &check;       |               |
| UHF           | QCISD             | &check;       |               |
| UHF           | MP2               | &check;       | &check;       |
| UHF           | MP3               | &check;       | &check;       |
| UHF           | MP4               | &check;       | &check;       |
| UHF           | MP4(SDQ)          | &check;       | &check;       |
| UHF           | MP5               | &check;       | &check;       |
| ROHF          | CISD              | &check;       |               |

任何 AUTOCI 单参考方法都可以通过在相关方法前加上 `AUTOCI-` 前缀
由简单关键词调用，例如

```orca
! AUTOCI-CCSD
```
加上 'AUTOCI' 前缀是为了与 `orca_mdci` 和 `orca_mp2` 中的手工实现相区分。

!!! warning
    CCSDT 和 CCSDTQ 等高阶 CC 计算在 CC 迭代中对内存有极高要求。尤其是 UHF CCSDTQ
    （计算代价按$N^{10}$ 标度！），视你的体系结构而定，只有电子数和基函数很少的体系才是可行的。

对于 CASSCF 参考波函数则省略前缀。以下多参考（multi-reference）方法及其
非弛豫密度（unrelaxed density）可用。

| 参考波函数    | 相关方法          | 能量          | 非弛豫密度    |
| ------------- | ----------------- | ------------- | ------------- | 
| CASSCF        | FIC-MRCI          | &check;       |  &check;          |
| CASSCF        | FIC-CEPA(0)     | &check;       |  &check;          |
| CASSCF        | FIC-ACPF        | &check;       |  &check;          |
| CASSCF        | FIC-AQCC        | &check;       |  &check;          |
| CASSCF        | FIC-MRCC          | &check;       |  Linearized       |
| CASSCF        | FIC-DDCI3         | &check;       |  &check;          |
| CASSCF        | FIC-NEVPT2        | &check;       |  &check;          |
| CASSCF        | FIC-NEVPT3        | &check;       |  &check;          |
| CASSCF        | FIC-NEVPT4(SD)    | &check;       |  &check;          |

!!! note
    如果以简单关键词指定多参考方法，则关于参考空间、根的数目等所有信息都取自
    假定已预先运行的 CASSCF 模块。更精细的设置需要在输入中使用 `%autoci` 块。

<a id="sec:modelchemistries.autoci.gradients"></a>
## 用 AUTOCI 计算解析核梯度（Analytic Nuclear Gradients with AUTOCI）

获得精确的几何结构对准确计算分子性质至关重要。为了进行几何优化，核梯度是必需的，
虽然用数值有限差分方法可以容易地得到它，但代价也相当高。也许更重要的是，
数值导数往往变得不稳定。因此，能够计算解析梯度（analytic gradient）至关重要。
借助 AGE，我们构建了一个支持任意阶 CI、CC 和 MPn 核梯度（及其他导数）的通用框架
[lechner2024code](../../bibliography.md)。

下面给出一个在 CCSD 理论级别上使用 AUTOCI 梯度优化几何的示例

```orca
! RHF cc-pVTZ AUTOCI-CCSD VerytightSCF Opt

%maxcore 10000

*xyz 0 1
...
*
```

解析梯度甚至可用于进行半数值频率（semi-numerical frequency）计算

```orca
! AUTOCI-CCSD NumFreq
```

除核梯度外，ORCA 中所有其他可用的一阶性质对相应方法也都可用，
例如偶极/四极矩、超精细耦合或四极分裂。如上所述，(非)弛豫密度可通过下式请求

```orca
%autoci
  density relaxed
end
```

对于几何优化，非弛豫密度与弛豫密度都会自动计算，无需显式请求。

<a id="sec:modelchemistries.autoci.autociresp"></a>
## 通过解析导数计算 AUTOCI 响应性质（AUTOCI Response Properties via Analytic Derivatives）

对于单参考方法（`CCSD` 与 `CCSD(T)`），某些响应性质（response property）
可以通过解析导数方案计算。

| 响应性质                | 参考波函数 | 相关方法    | 轨道响应              |
| ------------------------- | --------- | ----------- | --------------------- |
| 静态极化率*               | RHF       | CCSD        | 非弛豫 / 弛豫         |
|                           | RHF       | CCSD(T)     | 非弛豫 / 弛豫         |
|                           | UHF       | CCSD        | 非弛豫 / 弛豫         |
|                           | UHF       | CCSD(T)     | 非弛豫 / 弛豫         |
| NMR 屏蔽（GIAO）          | RHF       | CCSD        | 非弛豫 / 弛豫         |
|                           | RHF       | CCSD(T)     | 非弛豫 / 弛豫         |
|                           | UHF       | CCSD        | 非弛豫 / 弛豫         |
|                           | UHF       | CCSD(T)     | 非弛豫 / 弛豫         |
| g 张量（GIAO）            | UHF       | CCSD        | 非弛豫 / 弛豫         |
|                           | UHF       | CCSD(T)     | 非弛豫 / 弛豫         |

（* 偶极-偶极、偶极-四极、四极-四极）
注意，对于 NMR 屏蔽与 EPR g 张量，默认采用完全解析的 GIAO 方法
（见 [spectroscopyproperties.nmr](../spectroscopyproperties/nmr.md#sec:spectroscopyproperties.nmr) 与 [epr.gaugeorigin](../spectroscopyproperties/epr.md#sec:spectroscopyproperties.epr.gaugeorigin)），
而精度较低的公共规范（common gauge）方法则不可用。

要计算这些性质，需要计算以下各量：
 - 未微扰的 CC 振幅
 - 未微扰的 CC$\Lambda$（拉格朗日乘子，Lagrange Multiplier）
 - 未微扰的 1-RDM
 - 未微扰的 2-RDM（$\dagger$）
 - 未微扰的 Z 向量（Z-Vector）（$\dagger$）
 - 微扰的 CC 振幅
 - 微扰的 CC$\Lambda$（拉格朗日乘子）
 - 微扰的 1-RDM
 - 微扰的 2-RDM（$\dagger$）
 - 微扰的 Z 向量（$\dagger$）

标注为（$\dagger$）的任务是可选的——它们只在计算响应性质的"弛豫"（relaxed）方案中
才是必需的。在"弛豫"方案中，轨道允许弛豫以响应外微扰。
（参见：[轨道弛豫](#sec:modelchemistries.autoci.autociresp.relaxation)

<a id="sec:modelchemistries.autoci.autociresp.unperturbed"></a>
### 未微扰参数（Unperturbed Parameters）

由 CC 梯度理论，并如前文 [`MDCI` 一节](mdci.md#sec:modelchemistries.mdci.densities)所述，
CC 能量拉格朗日量（Lagrangian）可写为（将相似变换哈密顿量（similarity-transformed
Hamiltonian）记作$\bar{H}=e^{-T}H e^{T}$）：

$$
L _{\text{CC}} = \langle \Phi_{0}|\bar{H}|\Phi_{0}\rangle
                 + \sum_{\eta}\lambda_{\eta}\langle \Phi_{\eta}|\bar{H}|\Phi_{0}\rangle 
                 + \sum_{ai}f _{ai}z _{ai}
$$

等价地，我们也可以用密度矩阵来表达该拉格朗日量：

$$
L _{\text{CC}} = \sum_{pq}h _{pq} \frac{\partial L_{\text{CC}}}{\partial h_{pq}} \\
                 + \sum_{pqrs}(pq|rs)\frac{\partial L_{\text{CC}}}{\partial (pq|rs)} \\ 
               = \sum_{pq}h _{pq}D_{pq} + \sum_{pqrs}(pq|rs)d_{pqrs}
$$

其中单体与双体约化密度矩阵（reduced density matrix，RDM）可分解为振幅贡献与轨道贡献：

$$
D_{pq} = \gamma_{pq} + z _{pq}\delta_{pa}\delta_{qi} \\
d_{pqrs} = \Gamma^{pr}_{qs} + z_{pq}\sum_{k}\left(\delta_{pa}\delta_{qi}\delta_{rk}\delta_{sk}
                                                  -\delta_{pa}\delta_{qk}\delta_{rk}\delta_{si}\right)
$$

上述称为弛豫 1- 与 2-RDM，因为涉及$z_{pq}$ 的项源自[轨道弛豫](#sec:modelchemistries.autoci.autociresp.relaxation)。
CC 振幅贡献（亦称非弛豫 1- 与 2-RDM）定义为：

$$
\gamma_{pq} = \langle \Phi_{0}|(1+\Lambda)e^{-T}E^{p}_{q}e^{T}|\Phi_{0} \rangle \\
\Gamma^{pr}_{qs} = \langle \Phi_{0}|(1+\Lambda)e^{-T}\left(E^{p}_{q}E^{r}_{s}-E^{p}_{s}\delta_{rq}\right)e^{T}|\Phi_{0} \rangle
$$

这些量依赖于 CC 振幅$t_{\eta}$ 与拉格朗日乘子$\lambda_{\eta}$，为此需要求解振幅方程与$\Lambda$ 方程：

$$
\langle \Phi_{\eta}|\bar{H}| \Phi_{0}\rangle = 0 \\
\langle \Phi_{0}|(1+\Lambda)(\bar{H}-E_{\text{CC}})|\Phi_{\eta}\rangle = 0
$$

<a id="sec:modelchemistries.autoci.autociresp.perturbed"></a>
### 微扰参数（Perturbed Parameters）
著名的 Wigner$2n+1$ 微扰理论规则指出：$2n+1$ 阶能量需要至$n$ 阶的波函数参数。
对于 CC 这类非变分方法，采用拉格朗日方法，得到一个变分能量泛函
（尽管非 Rayleigh-Ritz 型，因而不保证上界），从而可对导数作解析求值。
该拉格朗日泛函中拉格朗日乘子的$2n+2$ 规则指出：$2n+2$ 阶能量需要至$n$ 阶的拉格朗日乘子。在实践中，也即在 `ORCA-AUTOCI` 的实现中，这两条规则（尤其是$2n+2$ 规则）
并未被完全利用。这是出于对某些分子性质计算效率的考虑。例如，CC 能量在两个外微扰
$x$ 与$y$ 下的二阶导数一般表达式可写为：

$$
\frac{\mathrm{d} ^{2}E}{\mathrm{d} x \mathrm{d} y}
= \langle \Phi_{0}|(1+\Lambda)e^{-T}\frac{\partial ^{2}H}{\partial x \partial y}e^{T}|\Phi_{0}\rangle \\
+ \langle \Phi_{0}|(1+\Lambda)\left[e^{-T}\frac{\partial H}{\partial x}e^{T},\frac{\mathrm{d} T}{\mathrm{d} y}\right]|\Phi_{0}\rangle \\
+ \langle \Phi_{0}|(1+\Lambda)\left[e^{-T}\frac{\partial H}{\partial y}e^{T},\frac{\mathrm{d} T}{\mathrm{d} x}\right]|\Phi_{0}\rangle \\
+ \langle \Phi_{0}|(1+\Lambda)\left[\left[e^{-T}H e^{T}, \frac{\mathrm{d} T}{\mathrm{d} x}\right],\frac{\mathrm{d} T}{\mathrm{d} y}\right]|\Phi_{0}\rangle
$$

这被称为"对称"表达式，同时满足$2n+1$ 与$2n+2$ 规则。
然而，对于混合导数，下述"非对称"表达式可能更为可取：

$$
\frac{\mathrm{d} ^{2}E}{\mathrm{d} x \mathrm{d} y} \\
= \langle \Phi_{0}|(1+\Lambda)e^{-T}\frac{\partial ^{2}H}{\partial x \partial y}e^{T}|\Phi_{0}\rangle \\
+ \langle \Phi_{0}|(1+\Lambda)\left[e^{-T}\frac{\partial H}{\partial x}e^{T},\frac{\mathrm{d} T}{\mathrm{d} y}\right]|\Phi_{0}\rangle \\
+ \langle \Phi_{0}|\frac{\mathrm{d} \Lambda}{\mathrm{d}y}e ^{-T}\frac{\partial H}{\partial x}e ^{T}|\Phi_{0}\rangle
$$

这样，我们只需针对单个微扰求解微扰的$T$ 与$\Lambda$ 方程。
对于 NMR 屏蔽，这意味着只需针对磁场微扰求解这些方程，
即$\mathrm{d} T/\mathrm{d} B_{i}$ 有$3$ 个方程，$\mathrm{d} \Lambda/\mathrm{d} B_{i}$ 有$3$ 个方程。
若采用第一种"对称"表达式，虽然可以省去求解任何微扰$\Lambda$ 的功夫，但仍需针对磁场微扰（$3$ 个方程）与核磁矩微扰（$3N_{\text{atoms}}$ 个方程）两者求解微扰的$T$。为得到微扰$T$ 与$\Lambda$ 的方程，我们将未微扰方程对外微扰$\chi$ 求导

$$
\frac{\partial}{\partial\chi} \langle \Phi_{\eta}|\bar{H}|\Phi_{0}\rangle = 0 \\ 
  \frac{\partial}{\partial\chi} \langle
\Phi_{0}|(1+\Lambda)(\bar{H}-E_{\text{CC}})|\Phi_{\eta}\rangle = 0
$$

然后通过对未微扰表达式求导来构造微扰的 1- 与 2-RDM：

$$
\frac{\partial\gamma_{pq}}{\partial\chi}      = \frac{\partial}{\partial\chi}\langle \Phi_{0}|(1+\Lambda)e^{-T}E^{p}_{q}e^{T}|\Phi_{0} \rangle \\
 \frac{\partial\Gamma^{pr}_{qs}}{\partial\chi} = \frac{\partial}{\partial\chi}\langle \Phi_{0}|(1+\Lambda)e^{-T}\left(E^{p}_{q}E^{r}_{s}-E^{p}_{s}\delta_{rq}\right)e^{T}|\Phi_{0} \rangle
$$

表达式与相关模块由代码生成器产生。注意，对于目前可用的响应性质——极化率、NMR 屏蔽、
EPR g 张量——它们在技术上是单粒子性质，2-RDM 不会显式出现在能量导数表达式中，
因此未微扰 2-RDM 与微扰 2-RDM 都只在需要计算[轨道弛豫](#sec:modelchemistries.autoci.autociresp.relaxation)时才是必需的。
<a id="sec:modelchemistries.autoci.autociresp.relaxation"></a>
### 轨道弛豫（Orbital Relaxation）
将轨道弛豫效应纳入性质计算，本质上就是允许 MO 响应外微扰。这导致 MO 系数
有如下的参数化：

$$
C(\chi) = C(0) U(\chi)
$$

于是 MO 导数可写为：

$$
C^{\chi}\equiv \frac{\partial C(\chi)}{\partial \chi}
= C(0) \frac{\partial U(\chi)}{\partial \chi} \equiv C
U^{\chi}
$$

其中$U^{\chi}$ 是 [CPSCF](../essentialelements/cpscf.md#sec:essentialelements.cpscf) 方程的解。对于非弛豫计算，MO 系数始终为$C(0)$。在弛豫计算中，MO 响应通过两种方式
进入相关的 CC 方程。
第一，如[上文](#sec:modelchemistries.autoci.autociresp.perturbed)所述，
对于二阶响应性质（如极化率、NMR 屏蔽等）我们需要求解一阶$T$ 与$\Lambda$ 方程。
在弛豫方案下，进入 CC 方程的任何导数积分（Fock、ERI 等）都包含 CPSCF 贡献。
例如：

$$
\frac{\partial (pq|rs)}{\partial \chi} = \\
\sum_{\mu\nu\kappa\tau}C_{\mu p}C_{\nu q} \frac{\partial (\mu\nu|\kappa\tau)}{\partial \chi}C_{\kappa r}C_{\tau s} \\
+ \sum_{\mu\nu\kappa\tau}C_{\mu p}^{\chi}C_{\nu q}(\mu\nu|\kappa\tau)C_{\kappa r}C_{\tau s} \\
+ \sum_{\mu\nu\kappa\tau}C_{\mu p}C_{\nu q}^{\chi}(\mu\nu|\kappa\tau)C_{\kappa r}C_{\tau s} \\
+ \sum_{\mu\nu\kappa\tau}C_{\mu p}C_{\nu q}(\mu\nu|\kappa\tau)C_{\kappa r}^{\chi}C_{\tau s} \\
+ \sum_{\mu\nu\kappa\tau}C_{\mu p}C_{\nu q}(\mu\nu|\kappa\tau)C_{\kappa r}C_{\tau s}^{\chi}
$$

对于非弛豫计算，后 4 项为零。
第二，为计算弛豫 1- 与 2-RDM 及其导数，需要包括$z$ 向量贡献。
这是要求在存在外微扰时 CC 能量对轨道旋转不变的必然结果。
Schaefer 与 Handy 的这一巧妙技巧使得无需为轨道求解$3N_{atoms}$ 个方程即可计算梯度，取而代之只需求解所谓的 "$z$ 向量"方程。由此打开了高效解析响应性质计算的大门。
$z$ 向量方程与 [CPSCF](../essentialelements/cpscf.md#sec:essentialelements.cpscf) 方程形式相同：

$$
Az = X
$$

其中$A$ 矩阵与 CPSCF 的左端完全相同，右端矩阵$X$ 是
CC 能量泛函的轨道梯度。对于二阶响应性质，还需要求解该方程（对所请求的每个微扰）
的导数。
关于弛豫性质与非弛豫性质的讨论相当常见。一般而言，我们认为对于极化率这类依赖电场的性质，
纳入轨道弛豫相比实验值并不必然给出更精确的结果。然而对于 NMR 与 EPR 参数这类
依赖磁场的性质，通常认为纳入轨道弛豫是必要的。
最后还值得注意的是，该轨道弛豫方案并不能恢复在 CC 波函数框架中使用 HF 轨道的 MO 响应，
后者依赖于轨道优化耦合簇（orbital-optimized coupled-cluster，OOCC）方法，
如[上一节](mdci.md#sec:modelchemistries.mdci.densities)所述。
<a id="sec:modelchemistries.autoci.autociresp.inputs"></a>
### 输入选项（Input Options）
波函数的输入参数由 [`%autoci`](#sec:modelchemistries.autoci.keywords) 块控制，
而与性质相关的参数由各自的性质块控制，例如
[`elprop`](../spectroscopyproperties/electric.md#sec:spectroscopyproperties.properties.elprop.keywords) 与
[`eprnmr`](../spectroscopyproperties/nmr.md#sec:spectroscopyproperties.properties.eprnmr)。
下面汇总了一些有用选项。
```orca
%autoci
    citype
        CCSD(T)
        CCSD
    STol      1e-06 # residue convergence tolerance
    MaxIter   50    # maximum number of iterations
    MaxDIIS   5     # depth of the DIIS memory
    density         # need at least unrelaxed density (see details below)
        unrelaxed
        relaxed
end
%method 
  Z_Tol       1e-8  # Convergence tolerance for the CP-SCF equations
                    # default if 3e-6 for ExtremeSCF
                    # however, we recommend at least one level tighter than %autoci STol
end
%elprop
    polar         true    # dipole-dipole polarizability
    polardipquad  true    # dipole-quadrupole polarizability
    polarquadquad true    # quadrupole-quadrupole polarizability
    Tol           1e-8    # Alia, see: %method Z_Tol
end
%eprnmr
    gtensor       true    # calculate the g-tensor
    NMRShielding  1       # for chosen nuclei - specified with the Nuclei keyword
                  2       # for all nuclei, equivalent to the 'NMR' simple input
    Tol           1e-8    # Alia, see: %method Z_Tol
end
```
输出文件：
AutoCI-Response 模块生成的计算输出被重定向到单独的输出文件中，
文件名为 `basename.autociresp_efield`、`basename.autociresp_bfield` 等。
<a id="sec:modelchemistries.autoci.autociresp.examples"></a>
### 输入示例（Input Examples）
HF 的高精度 NMR 屏蔽：
```mol
title: structure 1
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
2
structure
H    0.00000000   0.00000000   1.64411926
F    0.00000000   0.00000000  -0.08721704
```
NH 自由基的 g 张量，其中 SOC 算符取有效核电荷（见 [`SOCoptions`](../spectroscopyproperties/spinorbit.md#sec:spectroscopyproperties.soc)）：
```mol
title: structure 2
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
2
structure (0 3)
N           0.0          0.0          0.0
H           0.0          0.0     1.957794
--- input ---
! UHF cc-pVTZ G-Tensor ExtremeSCF AUTOCI-CCSD(T)
! NoFrozenCore Bohrs
%rel 
  SOCType 1
  Zeff[1] = 1.0   # H
  Zeff[7] = 4.55  # N
end
%eprnmr
  Tol 1e-10
end
%autoci
  STol 1e-9
  Density relaxed
end
# NH radical
* xyz 0 3
N 0.0  0.0  0.0
H 0.0  0.0  1.957794
*
```
将 `%rel` 块改为如下内容，即可用更精确的 SOC 描述（SOMF）进行同样的计算：
```
%rel 
  # these two are defaults
  SOCType 3
  SOCFlags 1,4,3,0
end
```
<a id="sec:modelchemistries.autoci.ficmrci"></a>
## 全内收缩 MRCI（FIC-MRCI）
任何多参考方法的出发点都是一个由多个行列式或组态状态函数（CSF）构成的参考波函数。
在许多情形下这就是完全活性空间 SCF（CASSCF）波函数。在 `orca_mrci` 模块所实现的
非收缩 MRCI 方法中，波函数通过考虑相对于所有参考 CSF 的激发所产生的激发 CSF
来展开。该方法的标度依赖于参考 CSF 的数目，因而仅限于小参考空间。
此外，`orca_mrci` 中所用的组态驱动算法将所有积分保留在内存中，这进一步限制了
分子的总体规模。
Meyer 与 Siegbahn 所提出的内收缩（internal contraction）避免了这些瓶颈
[siegbahn_direct_1980,meyer_configuration_1977](../../bibliography.md)。在此，激发 CSF 通过将
激发算符作用于整个参考波函数来生成。全内收缩 MRCI（fully internally contracted
MRCI，FIC-MRCI）采用与 FIC-NEVPT2（又称 PC-NEVPT2）相同的内收缩方案。
整套方法及其与常规非收缩 MRCI 的比较已在我们的文章中报道[sivalingam_comparison_2016](../../bibliography.md)。
CEPA0、ACPF 与 AQCC 变体是直接的移植[saitowfic](../../bibliography.md)。FIC-MRCI 拟设的残差

<a id="eq:residualfic"></a>

$$
R_K=\braket{\Phi^{pr}_{qs}| \hat H - E^\text{CAS}-\lambda E_{c}|\Psi^\text{FIC} },\qquad \text{(residualfic)}
$$

被如下因子所修正

$$
\lambda = \left\{\begin{array}{cc}
1  & \text{MRCI} \\
0  & \text{CEPA0} \\
\frac{2}{N_{e} }  & \text{ACPF}\\
\frac{1-(N_e-3)(N_e-2) }{N_e\cdot(N_e-1) } & \text{AQCC}
\end{array}
\right.
$$

这里$E_{c}$ 是相关能，$\Phi^{pr}_{qs}$ 表示由自旋求迹激发算符（spin-traced
excitation operator）作用于 CAS-CI 参考波函数而产生的内收缩 CSF

$$
\Phi^{pr}_{qs}=E^p_qE^r_s \ket{\Psi^\text{CAS} }.
$$

对于 ACPF 与 AQCC，$\lambda$ 因子显式依赖于相关电子数（$N_{e}$）。
一般的输入结构与 CASSCF 模块相同，例如下面的示例输入读入一组任意轨道
并启动 FIC-MRCI 计算。内收缩形式体系要求至四阶的 CAS-CI 约化密度，
构造它们可能代价高昂。默认情况下，密度构造使用
[modelchemistries.nevpt2](NEVPT2.md#sec:modelchemistries.nevpt2) 一节所述的预筛选（prescreening，PS）近似
来加速[guo_nevpt2_approx1_2021](../../bibliography.md)。
```orca
!def2-tzvp moread allowrhf noiter nofrozencore
%moinp "start.gbw"  # could be from CASSCF
%autoci
citype   FIC-MRCI      # Fully internally contracted MRCI (singles, doubles)
         FIC-CEPA(0)   # CEPA0 version of FIC-MRCI
         FIC-ACPF      # ACPF  version of FIC-MRCI
         FIC-AQCC      # AQCC  version of FIC-MRCI
         FIC-DDCI3     # FIC-MRCI without the IJAB excitation
# CAS-CI reference wavefunction
nel 2
norb 2
mult 1,3
nroots 3,1
nthresh 1e-6  # removal of linear dependencies in the IC-CSFs
D3TPre        1e-14 # default density truncation of the 3-RDM
D4TPre        1e-14 # default density truncation of the 4-RDM
# Davidson correction for the FIC-MRCI
DavidsonOpt 0  # none (default)
            1  # Davidson correction
end
```
目前该程序能够计算总能量与垂直激发能（vertical excitation energy）。
未来版本将提供更多功能。
### 输入示例（Input Example）
```mol
title: structure 3
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
2
structure (0 3)
O             0            0            0
O             0            0         1.28
--- input ---
# potentially "!FIC-CEPA(0)" omitting the %autoci block.
!def2-SVP  
# get CASSCF orbitals and define states
%casscf
  nel 8
  norb 6
  mult 3
  nroots 1
end
# run FIC-CEPA(0)
%autoci
  # CAS settings are automatically copied from the %casscf block, if 
  # not defined in %autoci
  citype FIC-CEPA(0)
end
# O2 molecule
*xyz 0 3
O 0 0 0 
O 0 0 1.28
*
```
<a id="sec:modelchemistries.autoci.ficmrcc2"></a>
## 全内收缩 MRCC（FIC-MRCC）
已有若干途径被尝试用于将 CC 理论扩展到真正多组态参考波函数的情形[Lyakh2012](../../bibliography.md)，
然而这些途径都未获广泛采用。自 2011 年起，内收缩 MRCC 理论迎来复兴：
对若干近似进行了严格的理论研究，并证明了其轨道不变性[Evangelista2011](../../bibliography.md)；
同时首次报道了通过自动生成方程得到的多项式标度代码[Hanauer2011](../../bibliography.md)。
我们在 ORCA 中的实现与文献 [Evangelista2011,Hanauer2011](../../bibliography.md) 中早先发表的表述相仿，
不过一切都是用无自旋激发算符
$\hat E_q^p = \hat a^{p\alpha }\hat a_{q\alpha } + \hat a^{p\beta }\hat a_{q\beta }$
严格表述的，并使用了改进版的 ORCA-AGE 代码生成器[lechner2024code](../../bibliography.md)。
首先，波函数的*拟设*（*ansatz*）为

<a id="eq:MRCC-ansatz"></a>

$$
\begin{aligned}
|\Psi \rangle  = \text{e}^{\hat T}|0\rangle \;, \end{aligned}\qquad \text{(eq:MRCC-ansatz)}
$$

其中$|0\rangle$ 表示零阶 CASSCF 参考波函数，簇算符（cluster operator）
可写为（采用 Einstein 求和约定）

$$
\hat T = \frac{1}{2}t_{ab}^{ij}\hat E_i^a\hat E_j^b + t_{ab}^{it}\hat E_i^a\hat E_t^b + \frac{1}{2}t_{ab}^{tu}\hat E_t^a\hat E_u^b + t_{at}^{ij}\hat E_i^a\hat E_j^t + t_{au}^{it}\hat E_i^a\hat E_t^u \\
    + t_{ua}^{it}\hat E_i^u\hat E_t^a + t_{av}^{tu}\hat E_t^a\hat E_u^v + \frac{1}{2} t_{tu}^{ij}\hat E_i^t\hat E_j^u + t_{uv}^{it}\hat E_i^u\hat E_t^v\;.
$$

注意我们在簇算符中不使用正规乘积（normal order）。

将式 [Eq](#eq:MRCC-ansatz) 中的*拟设*代入 Schrödinger 方程并左乘逆指数，
我们得到相似变换哈密顿量与能量表达式

$$
\begin{aligned}
    \bar H|0\rangle  = \text{e}^{ - \hat T}\hat H\text{e}^{\hat T}|0\rangle  = E|0\rangle \;.\end{aligned}
$$

在我们的代码中，相似变换哈密顿量在二次项后截断，
因为已发现该近似对方法精度只有轻微影响[Evangelista2011](../../bibliography.md)，

$$
\begin{aligned}
    \bar H \approx \hat H + [\hat H,\hat T] + \frac{1}{2}[[\hat H,\hat T],\hat T]\;.\end{aligned}
$$

随后通过以逆变激发函数（contravariant excited function）$\langle \tilde \Phi _P|$
投影到 Schrödinger 方程上来得到残差条件

$$
\begin{aligned}
{ r_P} = \langle \tilde \Phi _P|\bar H|0\rangle \;.\end{aligned}
$$

关于逆变投影函数的定义，我们请读者参阅文献 [sivalingam_comparison_2016](../../bibliography.md)，
因为该 FIC-MRCC 实现使用与已发表的 FIC-MRCI 实现相同的逆变函数。
尽管使用了逆变投影函数，这仍不足以从投影函数集合$\{ \tilde\Phi_P \}$ 中
消除所有线性相关，即度规矩阵（metric matrix）

$$
\begin{aligned}
    S_{PQ} &= \braket{\tilde\Phi_P | \tilde\Phi_Q} \ne \delta_{PQ}\end{aligned}
$$

在激发类*内部*以及具有相同非活性与虚拟指标数目的类之间（ITAU 与 ITUA）
存在非对角元。因此需要对投影函数集合作正交归一化，
这在 AUTOCI 模块中通过 Löwdin 正则正交化实现。[^1]

<a id="sec:autoci.ficmrcc.example.detailed"></a>
### 输入示例（Input Example）

可以通过在 `%autoci` 块中指定 `CIType` 关键词，或在 ORCA 输入文件的简单输入行中
加入 `FIC-MRCC` 来启动 FIC-MRCC 模块。下面的例子计算边长为$2 a_0$ 的正方形排列的
四个氢原子（通常称为 H4 模型[Jankowski1980](../../bibliography.md)）的单重态基态能量。

```orcainput
! cc-pVTZ Bohrs  # it is possible to add the `FIC-MRCC' keyword here
                 # and omit the %autoci block below

%maxcore 10000

# get CASSCF orbitals and define states.
%casscf
  nel 2
  norb 2
  mult 1
  nroots 1
end

# run FIC-MRCC
%autoci  
  # CAS settings are automatically copied from the %casscf block, if 
  # not defined in %autoci
  citype fic-mrcc
  
  # optional parameters
  nthresh 1e-6        # default removal of linear dependencies in the IC-CSFs
  D3TPre        1e-14 # default density truncation of the 3-RDM
  D4TPre        1e-14 # default density truncation of the 4-RDM
  D5TPre        1e-14 # default density truncation of the 5-RDM
  Density  linearized  # compute the linearized density (not default).
end

* int 0 1
  H 0 0 0 0.0  0.0 0.0
  H 1 0 0 2.0  0.0 0.0
  H 2 1 0 2.0 90.0 0.0
  H 1 2 3 2.0 90.0 0.0
*
```

在此示例中，ORCA 首先运行一个态特定的 CASSCF 计算，然后立即在第一步 CASSCF 解的
基础上继续进行 fic-MRCC 计算。不过并非总是必须在 `autoci` 模块之前运行 CASSCF 计算。
任何 ORCA `gbw/mp2nat/…` 文件都可以通过 `%moinp` 接受，只是该途径要求用户在
`autoci` 块中指定活性空间。`autoci` 随后用所提供的输入轨道计算 CASCI 解，
并用该信息驱动相关计算。

请注意，FIC-MRCC 是一种非常庞大的理论，会导致很长的运行时间。
计算代价主要取决于轨道数、总电子数以及活性空间的大小。
在较为现代的硬件上，CAS(2,2) 下约$\sim 300$ 个轨道的计算应可轻易完成。对于更大的活性空间（如 CAS(6,6)），总计约$\sim 200$ 个轨道的计算也能在一天内完成。

<a id="sec:modelchemistries.autoci.ficnevpt"></a>
## 全内收缩 NEVPT（FIC-NEVPT4(SD)/FIC-NEVPT3/FIC-NEVPT2）

微扰理论是前述 FIC-MRCI 与 FIC-MRCC 方法的一种高性价比替代。
通常在展开的二阶就已经能得到对电子相关的合理描述。
CASSCF 模块提供了二阶方法的高效实现，能够处理大分子与大活性空间。
关于二阶变体的更多细节与文献，请参阅专门章节 [modelchemistries.nevpt2](NEVPT2.md#sec:modelchemistries.nevpt2)。\
本节着重于 AUTOCI 框架内可用的高阶 n 电子价态微扰理论（n-electron valence state
perturbation theory，NEVPT）。这里所有积分都被计算并保存在磁盘上，
这将应用范围限制在大约 700 个原子轨道（atomic orbital，AO）。
高阶约化密度矩阵的出现是内收缩方法的共同特征。
与 FIC-NEVPT2 一样，FIC-NEVPT3 与 FIC-NEVPT4(SD) 至多需要四阶约化密度矩阵。
其计算可用 [modelchemistries.nevpt2](NEVPT2.md#sec:modelchemistries.nevpt2) 一节讨论的预筛选方法加速
[guo_nevpt2_approx1_2021,guo_nevpt2_approx2_2021](../../bibliography.md)。
就计算时间而言，FIC-NEVPT4(SD) 与 FIC-NEVPT3 或 FIC-MRCI 方法的一次迭代相当。

<a id="sec:modelchemistries.autoci.ficnevpt.nevpt3"></a>
### FIC-NEVPT3
FIC-NEVPT3 方法由 Angeli 等人详细描述[angeli_nevpt3](../../bibliography.md)。利用一阶波函数$\Psi^{(1)}$，三阶能量由下式给出

$$
E^{(3)}=\langle \Psi^{(1)}|V|\Psi^{(1)} \rangle.
$$

<a id="sec:modelchemistries.autoci.ficnevpt.nevpt4"></a>
### FIC-NEVPT4(SD)
四阶微扰理论需要二阶波函数，而它原则上涉及定义二阶相互作用空间的三重与四重激发。
纳入后者在计算上要求很高。下面我们报道一种近似解，称为 FIC-NEVPT4(SD)，
它局限于一阶相互作用空间——即相对于参考波函数的单双激发。
Kempfer 等人对该方法有更详细的报道与分析[kempfer_nevpt4sd](../../bibliography.md)。
以$\Psi^{(2)}$ 表示二阶波函数，四阶能量可方便地表示为

$$
E^{(4)} = \langle\Psi^{(1)}|V|\Psi^{(2)}\rangle - E^{(2)}\langle\Psi^{(1)}|\Psi^{(1)}\rangle.
$$

上式中的第二项$E^{(2)}\langle\Psi^{(1)}|\Psi^{(1)}\rangle$ 是重整化项。
正如该论文所讨论的[kempfer_nevpt4sd](../../bibliography.md)，在缺少精确四重激发时重整化项会破坏
尺寸一致性（size consistency），因此将其略去（默认）。

<a id="sec:modelchemistries.autoci.ficnevpt.input"></a>
### 输入示例（Input Example）

```mol
title: structure 4
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
2
structure (0 3)
O             0            0            0
O             0            0         1.28
--- input ---
# potentially "!FIC-NEVPT4(SD)"/"!FIC-NEVPT3" instead of the %autoci block.
!def2-tzvp 

# get CASSCF orbitals and define the states
%casscf
    nel 8
    norb 6
    mult 3
    nroots 1
end

# run NEVPT4(SD)
%autoci
# CAS settings are automatically copied from the %casscf block, if 
# not defined in %autoci

 citype fic-nevpt4(sd)

# optional parameters
nthresh 1e-6        # default removal of linear dependencies in the IC-CSFs
D3TPre        1e-14 # default density truncation of the 3-RDM
D4TPre        1e-14 # default density truncation of the 4-RDM

Density  Unrelaxed  # compute the unrelaxed density (not default).
end

# O2 molecule
* xyz 0 3
O 0 0 0
O 0 0 1.28
*
```

## FIC 拟设：非弛豫密度与自然轨道（FIC Ansatz: Unrelaxed Densities and Natural Orbitals）
FIC-NEVPT4(SD)、FIC-MRCC 与 FIC-MRCI 各变体在其波函数中共用一组激发参数。
对这些方法，可得到（线性化的）非弛豫密度（`density unrelaxed`）。
使用 `!KeepDens` 可将密度存储到密度容器中（磁盘上的 **.densities** 文件），
并可由 [`orca_plot` 程序](../utilitiesvisualization/utilities.md#sec:utilities.plot)读取。
密度的名称反映了其多重度、根计数与实际方法。下面是调用
"orca_plot jobname.densities" 的示例片段：
```
---------------------
List of density names
---------------------

Index:                                                   Name of Density
------------------------------------------------------------------------
    0:                                                      jobname.scfp
    1:                                                      jobname.scfr
    2:                                         Tdens-CAS.mult.3.root.0.p
    3:                                         Tdens-CAS.mult.3.root.1.p
    4:                                         Tdens-CAS.mult.3.root.2.p
    5:                                         Tdens-CAS.mult.3.root.0.r
    6:                                         Tdens-CAS.mult.3.root.1.r
    7:                                         Tdens-CAS.mult.3.root.2.r
    8:                     jobname.mult.3.root.0.FIC-NEVPT4(SD).autoci.p
    9:                     jobname.mult.3.root.1.FIC-NEVPT4(SD).autoci.p
   10:                     jobname.mult.3.root.2.FIC-NEVPT4(SD).autoci.p
```
这里密度 8-10 是 FIC-NEVPT4(SD) 方法对前三重三重态根的非弛豫密度。
利用非弛豫密度可以生成自然轨道（natural orbital，`natorbs true`）。
所得以 (.nat) 结尾的 .gbw 文件可用于进一步分析，例如使用
[MultiWFN 程序](https://pubs.aip.org/aip/jcp/article/161/8/082503/3309709/A-comprehensive-electron-wavefunction-analysis)。

```orca
!FIC-NEVPT4(sd)
...
%autoci
  Density  Unrelaxed  # compute the unrelaxed density
  natorbs true        # generate natural orbitals
end
```
<a id="sec:modelchemistries.autoci.keywords"></a>
## 关键词（Keywords）

<a id="tab:modelchemistries.autoci.keywords.simple"></a>
!!! note "AUTOCI 方法的简单输入关键词。"
    | 关键词                | 说明                                                                                   |
    |:--------------------|:----------------------------------------------------------------------------------------------|
    | `AUTOCI-<method>`   | 启用 AUTOCI 的单参考相关模块。禁用 MDCI。                                                      |
    | `FIC-MRCI`          |
    | `FIC-CEPA(0)`     |
    | `FIC-ACPF`        |
    | `FIC-AQCC`        |
    | `FIC-DDCI3`         |
    | `FIC-MRCC`          |
    | `FIC-NEVPT2`        |
    | `FIC-NEVPT3`        |
    | `FIC-NEVPT4(SD)`    |

<a id="tab:modelchemistries.autoci.keywords.block"></a>
!!! note "AUTOCI 方法的 `%autoci` 块输入关键词。"


| ****关键词**** | 选项 | 说明 |
| --- | --- | --- |
| ** `CIType`** | `CID` | 相关方法 |
| **`CISD`** |  |  |

| **`CISDT`** | 无 |
| **`CCD`** | 无 |
| **`CCSD`** | 无 |
| **`CCSDT`** | 无 |
| **`CEPA(0)`** | 无 |
| **`QCISD`** | 无 |
| **`CC2`** | 无 |
| **`CC3`** | 无 |
| **`CCSD[T]`** | 无 |
| **`CCSD(T)`** | 无 |
| **`CCSDT-1`** | 无 |
| **`CCSDT-2`** | 无 |
| **`CCSDT-3`** | 无 |
| **`CCSDT-4`** | 无 |
| **`FIC-MRCI`** | 无 |
| **`FIC-CEPA(0)`** | 无 |
| **`FIC-ACPF`** | 无 |
| **`FIC-AQCC`** | 无 |
| **`FIC-DDCI3`** | 无 |
| **`FIC-MRCC`** | 无 |
| **`FIC-NEVPT2`** | 无 |
| **`FIC-NEVPT3`** | 无 |
| **`FIC-NEVPT4(SD)`** | 无 |
| **`MP2`** | 无 |
| **`MP3`** | 无 |
| **`MP4(SDQ)`** | 无 |
| **`MP4`** | 无 |
| **`MP5`** | 无 |
| **`STol`** | 无 |

      - 1e-6
      - 残差收敛容差


| | **0.2** | DIIS 更新/分母中的能级移位 |
| --- | --- | --- |
| **`LevelShift`** | 0.2 | DIIS 更新/分母中的能级移位 |
| **`MaxIter`** | 50 | 最大迭代次数 |
| **`MaxDiis`** | 5 | DIIS 记忆深度 |
| **`DIISStartIter`** | 2 | 从第 1 次迭代起应用 DIIS（计数从 0 开始）。 |
| **`ExcludeHigherExcDIIS`** | `false` | 将三重及更高激发排除出 DIIS 过程 |
| **`NEl`** | 6 | 活性电子数（仅限 CAS） |
| **`NOrb`** | 7 | 活性轨道数（仅限 CAS） |
| **`Mult`** | 1 | 所请求的多重度块（仅限 CAS） |
| **`NRoots`** | 1 | 多重度块的根数（仅限 CAS） |
| **`Irrep`** | 0 | 多重度块所请求的不可约表示（仅限 CAS） |
| **`NThresh`** | 1e-6 | IC-CSF 基中线性相关的阈值（仅限 CAS） |
| **`D3TPre`** | 1e-14 | D3 中的密度截断（仅限 CAS） |
| **`D4TPre`** | 1e-14 | D4 中的密度截断（仅限 CAS） |
| **`PrintLevel`** | 3 | 打印量（1-7） |
| ** `TrafoType`** | `NoRI` | 积分变换的类型 |
| **`RITrafo`** |  |  |

| **`KeepInts`** | 无 |

      - `false`
      - 将变换后的积分保存在磁盘上


| | **`false`** | 使用磁盘上已有的变换后积分 |
| --- | --- | --- |
| **`UseOldInts`** | `false` | 使用磁盘上已有的变换后积分 |
| **`RunROHFasUHF`** | `false` | 用 ROHF 计算所得的轨道调用 AUTOCI UHF 模块 |
| ** `Density`** | `none` | 所请求的单体密度类型 |
| **`linearized`** |  |  |

| **`unrelaxed`** | 无 |
| **`relaxed`** | 无 |
| ** `Density2`** | 无 |

      - `none`
      -  所请求的双体密度类型


| | **值** |
| --- | --- |
| **`linearized`** |  |

| **`unrelaxed`** | 无 |
| **`relaxed`** | 无 |
| **`NatOrbs`** | 无 |

      - `false`
      - 生成自然轨道（并非所有方法都可用）

注意：对于 ROHF 参考，当前版本只能进行 CISD 计算。不过可以通过将
`RunROHFasUHF` 标志设为 true，用 ROHF 参考运行 UHF 计算。注意这只有在参考
确实是 ROHF 时才有意义，例如（在 CCSD 级别计算 HFC 的各向同性部分，
运行 AutoCI UHF CCSD 模块，轨道来自 ROHF SCF 计算）：

```mol
title: structure 5
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
1
structure (0 2)
Cu          0.0          0.0          0.0
--- input ---
! ROHF def2-svp tightscf pmodel AUTOCI-CCSD

%autoci
    RunROHFasUHF true
end

* xyz 0 2
Cu  0.0  0.0  0.0
*

%eprnmr nuclei = all Cu {aiso} end
```

如果希望对模块本身进行试验，而参考波函数保持不变，则可以将变换后的 MO 积分
存储在磁盘上（`keepints`）并重复使用（`useoldints`）。程序只检查磁盘上积分的
维度是否与实际求解的问题相匹配，也就是说，用户需自行对数据的有效性负责。

[^1]: 这与文献 [Hanauer2011](../../bibliography.md) 中的方案 A 类似。
