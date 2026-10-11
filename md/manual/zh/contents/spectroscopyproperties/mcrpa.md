```{index} MCRPA
```

(sec:spectroscopyproperties.mcrpa)=
# 通过 MCRPA 计算激发态（Excited States via MCRPA）

MCRPA 方法是 [CASSCF](sec:modelchemistries.casscf) 线性响应理论的同义表述。
在完成电子基态的收敛 [CASSCF](sec:modelchemistries.casscf) 计算后，
可以使用 ORCA 的 MCRPA 实现来计算
- 激发能
- 振子强度（UV/Vis 谱的强度）
- 旋光强度（ECD 谱的强度）
- 用于模拟 XAS 谱的芯激发能
主要针对开壳层和强相关体系。

在运行这些计算之前，请确保您熟悉
一般的 [CASSCF](sec:modelchemistries.casscf) 计算。

## 一般性描述（General Description）

MCRPA 激发能和跃迁矩由 CASSCF 波函数线性响应函数的极点和留数
计算得到。{cite}`Yeager1979,Joergensen1988,Helmich-Paris2019a`
这些量由广义本征值方程确定

$$\begin{aligned}
\mathbf{E}^{(2) } \, \boldsymbol{\lambda} =   \mathbf{S}^{(2) } \, \boldsymbol{\lambda}\, \omega \text{,}\end{aligned}$$

其中涉及二阶导数矩阵 $\mathbf{E}^{(2) }$ 和 $\mathbf{S}^{(2) }$。
本征值 $\omega$ 对应于电子激发能。二阶导数矩阵
$\mathbf{E}^{(2) }$ 和 $\mathbf{S}^{(2) }$ 具有配对结构，
因为表达电子激发和去激发的两类算符都包含在内：

$$ \left[ \left( \begin{array}{cc}
          \mathbf{A}   & \mathbf{B} \\
          \mathbf{B}^* & {\mathbf{A}}^*
        \end{array} \right)
        - \omega
        \left(
        \begin{array}{cc}
          \boldsymbol{\Sigma}   &  \boldsymbol{\Delta}  \\
          -\boldsymbol{\Delta}^* & -\boldsymbol{\Sigma}^*
        \end{array}
        \right)\right]
    \left(
    \begin{array}{c}
      \mathbf{X} \\
      \mathbf{Y}^*
    \end{array}
    \right)
= \left(
    \begin{array}{c}
      \mathbf{0} \\
      \mathbf{0}
    \end{array}
    \right)
$$

上述本征值方程对所有变分波函数方法都成立，
例如 [DFT](sec:modelchemistries.dft)、[HF](sec:essentialelements.hartreefock)、[CASSCF](sec:modelchemistries.casscf) 等。唯一的区别在于

所用的算符流形和不含时哈密顿量 $\hat{H}$。对于 CASSCF 线性响应和本征值方程，
超矩阵 $\mathbf{A}$、$\mathbf{B}$、$\boldsymbol{\Sigma}$ 和
$\boldsymbol{\Delta}$ 具有如下结构：

$$\begin{aligned}
&
\begin{array}{cc}
\mathbf{A} = \left(\begin{array}{cc}
\bra{0} [ q_i, [\hat{H}, q_j^{\dagger} ] ]    \ket{0} & \bra{0} [ [ q_i, \hat{H} ], R_j^{\dagger} ]  \ket{0} \\
\bra{0} [  R_i , [ \hat{H}, q_j^{\dagger} ] ] \ket{0} & \bra{0} [ R_i, [ \hat{H}, R_j^{\dagger} ] ]  \ket{0}
\end{array}
\right)%
&
\boldsymbol\Sigma = \left(\begin{array}{cc}
\bra{0} [ q_i, q_j^{\dagger} ] \ket{0} & \bra{0} [ q_i, R_j^{\dagger} ] \ket{0} \\
\bra{0} [ R_i, q_j^{\dagger} ] \ket{0} & \bra{0} [ R_i, R_j^{\dagger} ] \ket{0}
\end{array}
\right) \\[2.0em]
\mathbf{B} = \left(\begin{array}{cc}
\bra{0} [ q_i, [\hat{H}, q_j ] ]    \ket{0} & \bra{0} [ [ q_i, \hat{H} ], R_j ] \ket{0} \\
\bra{0} [  R_i , [ \hat{H}, q_j ] ] \ket{0} & \bra{0} [ R_i, [ \hat{H}, R_j ] ] \ket{0}
\end{array}
\right)%
&
\boldsymbol\Delta = \left(\begin{array}{cc}
\bra{0}  [ q_i, q_j ] \ket{0}  & \bra{0} [ q_i, R_j ] \ket{0} \\
\bra{0}  [ R_i, q_j ] \ket{0}  & \bra{0} [ R_i, R_j ] \ket{0}
\end{array}
\right)
\end{array}
\end{aligned}$$

有两类算符用于描述电子激发，
即轨道激发 $q_i^{\dagger}$ 和去激发算符 $q_i$，

$$\begin{aligned}
 &
 \begin{array}{lcr}
 q_i^{\dagger} = E_{pq} = a^{\dagger}_{p\alpha} a_{q\alpha} + a^{\dagger}_{p\beta} a_{q\beta} \text{,}
 &
 q_i        = E_{qp}  \text{,}
 &
\text{ with }  \quad p > q
 \end{array}\end{aligned}$$

以及所谓的态转移算符（state-transfer operators）

$$\begin{aligned}
 &
 \begin{array}{lcr}
 R_i^{\dagger} = \ket{i}\bra{0} \text{,}
 &
 R_i        = \ket{0}\bra{i} \text{,}
 &
 \text{ with }  i \ne 0
 \end{array}\end{aligned}$$

（UV/Vis）吸收谱和电子圆二色（ECD）谱的强度由跃迁矩得到。
跃迁矩很容易作为点积计算：

$$\begin{aligned}
\bra{0} \hat{V} \ket{f} = 
\left(\begin{array}{c}
\mathbf{X}^f \\
(\mathbf{Y}^f)^*
\end{array}\right)^{\dagger}
\left(\begin{array}{c}
\mathbf{C} \\
\mathbf{D}^*
\end{array}\right)
\end{aligned}$$

其中用到根 $f$ 的本征向量 $\mathbf{X}$ 和 $\mathbf{Y}$
以及偶极算符 $\hat{V}$ 的电子梯度 $\mathbf{C}$ 和 $\mathbf{D}$。

$$\begin{aligned}
\begin{array}{lr}
\mathbf{C} = \left(\begin{array}{c}
\bra{0} [ q_i, \hat{V} ] \ket{0} \\
\bra{0} [ R_i, \hat{V} ] \ket{0}
\end{array}\right)
&
\mathbf{D} = \left(\begin{array}{c}
\bra{0} [ q^{\dagger}_i, \hat{V} ] \ket{0} \\
\bra{0} [ R^{\dagger}_i, \hat{V} ] \ket{0}
\end{array}\right)
\end{array}
\end{aligned}$$

本征值方程通过定制版本的 Davidson 算法迭代求解，
该算法可同时确定 N 个最低根。
计算中最耗时的部分是将包含轨道部分和 CI 系数部分的试探向量
与电子 Hessian 矩阵 $\mathbf{E}^{(2) }$ 相乘变换。
工作方程与最小化 CASSCF 基态能量时计算的 CASSCF 电子梯度
非常相似。更多技术细节见
小节 {ref}`sec:spectroscopyproperties.mcrpa.computational`。

(fig:MCRPA-ni-II-h2o-6)=
```{figure} ../../images/MCRPA_ni-II-h2o-6.*

Ni(II) 六水合物的结构与前线轨道。
```
作为一个展示性算例，我们用 MCRPA 计算了八面体配位的
Ni(II) 六水合物的最低价激发能
（结构与前线轨道见图 {numref}`fig:MCRPA-ni-II-h2o-6`）。
我们将 Ni 的 3d 和 4d 轨道纳入活性空间，首先收敛
CASSCF 三重态基态。然后启动 MCRPA 计算。
只需指定所需根的数目 `NRoots` 即可。
```orca
%casscf
 nel    10  # number of active electrons
 norb   10  # number of active orbitals
 nroots  1  # only the ground state
 mult    3  # triplet multiplicity
end

%mcrpa
 NRoots 15  # number of roots / excited states
end
```
请注意，与态平均 CASSCF 不同，MCRPA 激发能
不依赖于 `NRoots`，这与 [TDDFT](sec:spectroscopyproperties.tddft) 或 [EOM-CC](sec:spectroscopyproperties.eom) 计算不同。

也可以通过切换 `DoOrbResp false` 标志来省略 MCTDA 或 MCRPA 计算
的轨道部分。对于这样的计算，得到的是 [CASCI](sec:modelchemistries.casscf.excitedstates)
激发能。请注意，对于这样的 MCRPA 计算，轨道是针对
CASSCF 基态优化的。

(sec:spectroscopyproperties.mcrpa.results)=
## 分析跃迁（Analyzing Transitions）

收敛后，对每个态给出激发/本征向量中最主要的贡献。
与基态 CI 系数比较
```orca
---------------------------------------------
CAS-SCF STATES FOR BLOCK  0 MULT= 3 NROOTS= 1
---------------------------------------------

ROOT   0:  E=   -1962.8698444660 Eh
      0.98088 [     0]: 2221100000
```
我们看到最低激发态主要由从活性轨道 3（d<sub>yz</sub>）到
活性轨道 4 和 5（d<sub>z<sup>2</sup></sub> 与 d<sub>x<sup>2</sup>-y<sup>2</sup></sub> 的混合）的跃迁组成。

```orca
STATE    1 3A  :  E=   0.033027 au      0.899 eV     7248.5 cm**-1


   (+) CI                                  0.72808 [    21]: 2212100000
   (+) CI                                  0.25245 [    27]: 2211200000
```
`(+)` 表示本征向量的上分量。

默认情况下，CI 本征向量中最大的元素以组态基（configuration basis）打印。
通过将 `PrintWF` 改为 `DET` 或 `CSF`，也可以分别以行列式基
或组态态函数（configuration state function，CSF）基打印。

请注意，CI 系数的分析还取决于活性轨道的选择，
这里选用的是自然轨道（natural orbitals）（默认选项）。

也有由单电子激发主导的跃迁，由本征向量的轨道部分表示。
对于 Ni(II) 六水合物，这些主要是 Rydberg 态。
下面给出第 24 个激发态最主要的轨道对（上 `(+)` 和下 `(-)` 分量）。
```orca
STATE   24 3A  :  E=   0.469596 au     12.778 eV   103064.3 cm**-1

   (+) I  24 (  35) -> V   0 (  49) :      0.01744 (c=  0.13206324)
   (+) I  26 (  37) -> V   2 (  51) :      0.02398 (c= -0.15485895)
   (+) I  24 (  35) -> V   4 (  53) :      0.02513 (c=  0.15853501)
   (+) A   0 (  39) -> V   0 (  49) :      0.26647 (c= -0.51620412)
   (+) A   7 (  46) -> V   0 (  49) :      1.55291 (c=  1.24615978)
   (+) A   0 (  39) -> V  16 (  65) :      0.11782 (c= -0.34324922)
   (+) A   7 (  46) -> V  16 (  65) :      0.73241 (c=  0.85580859)


   (-) I   0 (  11) -> A   0 (  39) :      0.05738 (c=  0.23954155)
```

(sec:spectroscopyproperties.mcrpa.ntos)=
## 自然跃迁轨道（Natural Transition Orbitals）
```{index} Natural Transition Orbitals (MCRPA)
```

与其直接分析激发向量的各部分，
可视化自然跃迁轨道（natural transition orbitals，NTO）{cite}`Martin2003,Helmich-Paris2019a`
往往更有启发性。
由于 NTO 是由 MCRPA 基态到激发态（f）跃迁密度矩阵
$\rho_{pq}^{0\to f}$ 的奇异值分解得到的，它们不依赖于
分子轨道（非活性、活性和虚拟）各部分的任何幺正变换，因此
与轨道类型（正则、局域、自然等）无关。

与 [TDDFT](sec:spectroscopyproperties.tddft.natTransOrb) 和 [ROCIS](sec:spectroscopyproperties.rocis.natTransOrb) 类似，
对每个态可以得到两组轨道，分别描述电子跃迁中
电子的给予（占据和活性）与接受（活性和虚拟）。
CASSCF 波函数的 $\rho_{pq}^{0\to f}$ 的轨道结构
如 {numref}`fig:MCRPA-nto-tdm` 所示。

(fig:MCRPA-nto-tdm)=
```{figure} ../../images/MCRPA_nto-tdm.*

MCRPA 跃迁密度矩阵 $\rho_{pq}^{0\to f}$ 的结构
```

请注意，激发向量的组态部分对 $\rho_{pq}^{0\to f}$ 的
活性-活性块有贡献，因此被考虑在内。

要计算 NTO，只需在输入中打开 `DoNTO` 标志
（`DoNTO true`）：

```orca
%mcrpa
 nroots    20    # number of roots
 DoNTO     true  # generate NTOs for converged roots
 NTOThresh 5e-5  # NTO selection threshold
end
```

这将为所有根计算奇异值大于
`NTOThresh` 阈值的所有 NTO。

```orca
------------------------------------------------
NATURAL TRANSITION ORBITALS FOR STATE     1 3A  
------------------------------------------------

STATE    1 3A  :  E=   0.033027 au      0.899 eV     7248.5 cm**-1

Threshold for printing occupation numbers 1.0000e-03

     0  : n=  0.99567919
     1  : n=  0.02731085
     2  : n=  0.02231787
     ...

=> Natural Transition Orbitals (donor   ) were saved in ni-II-h2o-6-cas-8-10-mcrpa.mcrpa.1-3A_nto-donor.gbw
=> Natural Transition Orbitals (acceptor) were saved in ni-II-h2o-6-cas-8-10-mcrpa.mcrpa.1-3A_nto-acceptor.gbw
```

对于上述例子，态 1 中最重要的（由 `NTOThresh` 控制）
给予 NTO 和接受 NTO 被写入 `gbw` 类型的文件。
NTO 可以用 `orca_plot` 程序可视化（见 Sec. {ref}`sec:utilities.plot`），
对于给予 NTO
```orca
orca_plot ni-II-h2o-6-cas-8-10-mcrpa.mcrpa.1-3A_nto-donor.gbw -i
```
对于接受 NTO
```orca
orca_plot ni-II-h2o-6-cas-8-10-mcrpa.mcrpa.1-3A_nto-acceptor.gbw -i
```
NTO 按其奇异值降序排列，如输出中所示，
从索引 0 开始为最重要的 NTO 对。

Ni(H<sub>2</sub>O)<sub>6</sub><sup>2+</sup> 三个最低价 <sup>3</sup>T<sub>g</sub> 跃迁的
最主要 NTO 对（索引 0）见图 {numref}`fig:MCRPA_ni-II-h2o-6-ntos`。

(fig:MCRPA_ni-II-h2o-6-ntos)=
```{figure} ../../images/MCRPA_ni-II-h2o-6-ntos.*

Ni(H<sub>2</sub>O)<sub>6</sub><sup>2+</sup> 中的最低跃迁。
```

(sec:spectroscopyproperties.mcrpa.xas)=
## X 射线吸收光谱（X-Ray Absorption Spectroscopy）
```{index} XAS via MCRPA
```

也可以利用芯-价分离（core-valence separation，CVS）近似，
用 MCRPA 模块计算 X 射线吸收谱（XAS）。{cite}`Helmich-Paris2021c`
对于这类计算，应选择与基态 CASSCF 或价激发能 MCRPA 计算
相同的活性空间。
为了访问 MCRPA 芯激发，CVS 近似引入了两个限制：
- 省略本征向量的组态部分，
  因为它对应于价活性轨道内部的价激发。
- 本征向量的轨道部分被限制为芯-活性和芯-虚拟
  轨道对，芯轨道列表由用户给出。

为计算臭氧最低的 MCRPA 氧 K 边跃迁，
可以使用如下输入进行 CVS-MCRPA 计算：
```orca
%casscf
 nel    12 # number of active electrons
 norb    9 # number of active orbitals
 nroots  1 # only the ground state
 mult    1 # singlet multiplicity
end

%mcrpa
 NRoots 15            # number of roots / excited states
 DoCVS  true          # turn on core valence separation
 OrbWin 0, 2, -1, -1  # select on the lowest 3 core orbitals
 DoNTO  true          # generate NTOs for converged roots
end
```
这里通过 `OrbWin` 选择了前 3 个非活性 MO，它们主要由
三个 O 原子的 3 个 1s 原子轨道展开。
对虚拟轨道没有限制
（第一个和最后一个虚拟 MO 索引均选 `-1`）。

请注意，与其他[多参考方法](sec:casscf.CoreExitedStates.detailed)不同，
对于 CVS-MCRPA 计算，芯轨道不必加入活性空间。

四个最低芯激发的最主要 NTO 对如下所示：
(fig:MCRPA-cvs-ozone)=
```{figure} ../../images/MCRPA_ozone-cvs-ntos.*

臭氧中最低的 CVS-MCRPA 氧 K 边跃迁。
```

(sec:spectroscopyproperties.mcrpa.computational)=
## 计算方面的考虑（Computational Aspects）

### 大分子（Large Molecules）

该代码旨在用于中等及更大规模的开壳层分子。它与 ORCA 的一阶
CASSCF 能量实现具有相同的标度，但前因子更大，因为计算成本
"原则上"随根的数目线性增长。

该实现是 AO 驱动的，意味着计算瓶颈是为多个态相关伪 AO 密度
构造 Fock 矩阵。请注意，每个态最多有 6 个伪 AO 密度。
如果采用 [RIJCOSX](sec:essentialelements.ri.rijcosx) 近似，
计算成本可以显著降低，强烈推荐使用。

MCRPA 计算中第二昂贵的部分是含 3 个活性指标的双电子积分
$g_{ptuv}$。由于我们的目标是在更大体系上进行计算，
积分变换只有一种使用分辨率恒等式
（resolution-of-the-identity，RI）近似的实现。

对辅助基组的限制与 CASSCF 代码相同
（Sec. {ref}`sec:spectroscopyproperties.casscfresp`）。即

-   如果 Fock 矩阵以 `Direct` 或 `Conventional` 模式构造，
    则使用 /C 基组进行 $g_{ptuv}$ 积分的 RI 近似。

-   如果对 Fock 矩阵采用 [RIJCOSX](sec:essentialelements.ri.rijcosx) 近似，
    则 Fock 矩阵和 $g_{ptuv}$ 积分都使用 /JK 基组。

请注意，[RIJK](sec:essentialelements.ri.rijk) 近似尚不可用。

### 收敛性（Convergence）

在开始运行 MCRPA 之前，建议将态相关 CASSCF 能量计算收敛得非常紧。
[TRAH-CASSCF](sec:modelchemistries.casscf.trah) 非常适合这一目的。
请注意，性质计算通常假设电子梯度为零，
否则本征值/响应方程中可能出现数值问题。

本征值和本征向量由 Davidson 算法的一个专用变体确定，
用于求解大规模 TDA 或 RPA 本征值方程。{cite}`Olsen1988,Helmich-Paris2019a`
本征值和本征向量的精度完全由 `TolR`（默认 1.e-5）决定，
它与每个根残差向量的 Frobenius 范数进行比较。

与收敛 CASSCF 方程类似，MCTDA 和 MCRPA 的收敛速率也受
分子轨道选择的影响。
这必须在 `%casscf` 输入块中设置。MCRPA 程序不会
改变收敛的轨道和 CI 系数。
对于大多数计算，默认设置最为合适，即
非活性和虚拟轨道用*正则轨道*，活性轨道用*自然轨道*，
如小节 {ref}`sec:modelchemistries.casscf.actorbs` 中所述。
对于双金属过渡金属配合物等多中心体系，*局域轨道*是更好的选择。
纯化的 d 或 f 轨道（`ActOrbs dorbs` 或 `ddorbs` 和 `forbs`）
对于单金属配合物的激发分析往往很有帮助，不过，
它们的选择通常会导致本征值方程收敛变慢。

为促进本征值方程快速收敛，我们从通过直接对角化完整 Hessian
和度规矩阵得到的本征向量开始迭代，这些矩阵是针对元素子集计算的。
这被称为 P 空间或 `full` 方法，它是获取初始本征向量的默认方法，
也是 TDA/RPA Davidson 算法的预条件子（`PreCond full`）。
P 空间方法包含轨道-轨道和组态-组态块，它们被单独对角化。
轨道-组态耦合在这里被忽略。
P 空间的大小由关键词 `PreConMaxRed` 控制，默认设为 400。
更大的 P 空间维度可以期望更快的收敛，但完全对角化的成本
呈立方增长。
另外，也可以使用近似对角 Hessian{cite}`chaban1997theor` 和度规进行预条件
（`PreCond diag`），但不能用于初始本征向量。
建议使用 `Precond full`。


(sec:spectroscopyproperties.mcrpa.keywords)=
## 关键词列表（Keyword List）
```{index} MCRPA Keywords
```


```orca
%mcrpa

  NRoots       0         # The number of desired roots

  TolR         1e-5      # Convergence threshold for residual norm
  PrintWF      CFG       # print CI part in (CFG (default), CSF, or DET basis)
  TolPrint     1e-2      # Threshold for printing elements of excitation vector

  MaxRed       200       # maximum size of reduces space for ALL VECTORS IN TOTAL
  MaxIter      100       # maximum number of (Davidson) iterations
                         
  TDA          false     # Switch off full TD-CASSCF (Tamm-Dancoff approximation)
  
  DoNTO        false     # Generate Natural Transition Orbitals
  NTOThresh    1e-3      # Threshold for printing occupation numbers

  DoCVS        false     # toggle core valence separation (CVS) for XAS
  OrbWin       i0, i1, a0, a1 # first and last inactive and virtual MO, respectively

  PreCond      full      # (default) P-space preconditioner uses parts of exact
                         # Hessian matrix
               diag      # diagonal preconditioner approximate diagonal
	                 # Hessian elements

  PreConMaxRed 400       # dimension of exact Hessian for preconditioning

  DoOrbResp    true      # turn orbital response off -> CAS-CI method

  DoCD                  true  # circular dichroism calculation
  DoDipoleLength        true  # electric moments in a length formulation
  DoDipoleVelocity      true  # electric moments in a velocity formulation
  DoFullSemiclassical   false # request the calculation of complete semiclassical multipolar moments
  DecomposeFosc         false # request the decomposition of the oscillator strengths in a multipolar expansion.

```
