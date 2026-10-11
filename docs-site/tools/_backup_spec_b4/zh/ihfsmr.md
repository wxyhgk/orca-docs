

<a id="sec:spectroscopyproperties.ihfsmrcc"></a>
# 通过 IH-FSMR-CCSD 计算激发态（Excited States via IH-FSMR-CCSD）

将单激发空间与双激发及更高激发空间解耦的另一种方法是使用
所谓的 Fock 空间多参考耦合簇（Fock space multi-reference coupled
cluster，FSMRCC）方法。该方法与 STEOM-CCSD 类似，但在公式形式上
灵活得多。

<a id="sec:spectroscopyproperties.ihfsmrcc.general"></a>
## 一般性描述（General Description）

FSMRCC 最初基于有效哈密顿量（effective Hamiltonian，EH）。
EH 理论的基本思想是从哈密顿算符的完整本征值谱中
获取某些选择性的本征值。为此，整个组态空间被划分为
模型空间和外部空间，分别用投影算符 $P_{M}$ 和 $Q_{M}$
表示（见 [fig:ihfsmrcc_ms](#fig:ihfsmrcc_ms)）。EH 的对角化处理
来自模型空间组态之间相互作用的非动态相关。
另一方面，动态相关则源于模型空间组态与
外部空间组态之间的相互作用。这种相互作用通过
一个普适波算符 $\Omega$ 引入，该算符被参数化为
作用于模型空间时生成精确波函数。价普适波算符
$\Omega$ 的形式为

$$

\begin{aligned}
\Omega=e^{\tilde{S}^{\left( p,h \right)} }\end{aligned}

$$

其中花括号表示簇算符的正规排序（normal ordering），
$\tilde{S}^{\left( p,h \right)}$ 定义为

$$

\begin{aligned}
\tilde{S}^{\left( p,h \right)}=\sum_{k=0}^{p}\sum_{l=0}^{h}\tilde{S}^{\left( k,l \right)}\end{aligned}

$$

簇算符 $\tilde{S}^{\left( k,l \right)}$ 能够准确消灭 k 个活性粒子
和 l 个活性空穴，同时还能产生空穴和粒子。
$\tilde{S}^{\left( p,h \right)}$
包含所有更低扇区 Fock 空间的 $\tilde{S}^{\left( k,l \right)}$
算符。$\tilde{S}^{\left( 0,0 \right)}$ 等价于
标准单参考耦合簇 $\hat{T}$ 算符。(p,h) 价体系的 EH
可定义为

$$

\begin{aligned}
\hat{H}_{eff}=P_{M}^{\left( p,h \right)}\Omega^{-1}\hat{H}\Omega P_{M}^{\left( p,h \right)}\end{aligned}

$$

然而，$\Omega^{-1}$ 在所有情形下可能都没有良好定义。
因此，上述 EH 定义很少使用。取而代之的是，通常采用
Block-Lindgren 方法求解方程，其定义为

$$

\begin{aligned}
P_{M}^{\left( p,h \right)}\left[  \hat{H}\Omega -\Omega\hat{H}_{eff}\right]P_{M}^{\left( p,h \right)}=0\end{aligned}

$$

$$

\begin{aligned}
Q_{M}^{\left( p,h \right)}\left[  \hat{H}\Omega -\Omega\hat{H}_{eff}\right]P_{M}^{\left( p,h \right)}=0\end{aligned}

$$

<a id="fig:ihfsmrcc_ms"></a>
*在有效哈密顿量（EH）理论中，组态空间被划分为模型空间和外部空间；
在中间哈密顿量（IH）理论中，组态空间被划分为模型空间、中间空间
和外部空间。$P$ 和 $Q$ 分别表示相应的投影算符。*

当模型空间与外部空间在能量上没有良好分离时，该方法会面临收敛问题。
这通常被称为入侵态问题（intruder state problem）。在中间哈密顿量
（intermediate Hamiltonian，IH）表述中，组态空间被划分为三个子空间，
即主空间（M）、中间空间（I）和外部空间（O）（见
[fig:ihfsmrcc_ms](#fig:ihfsmrcc_ms)），投影算符分别为 $P_{M}$、$P_{I}$
和 $Q_{O}$。中间空间充当模型空间与外部空间之间的缓冲区。
在对 IH 对角化时，一部分本征值对应于通过 EH 理论得到的主空间。
对于单激发态扇区 (1,1)，IH 定义为

$$

\begin{aligned}
H_{I}^{\left( 1,1 \right)}=P_{O}^{\left( 1,1 \right)}\bar{H}P_{O}^{\left( 1,1 \right)}+P_{O}^{\left( 1,1 \right)}\bar{H}Y^{\left( 1,1 \right)}P_{M}^{\left( 1,1 \right)}\end{aligned}

$$

其中

$$

\begin{aligned}
Y^{\left( 1,1 \right)}=Q_{O}^{\left( 1,1 \right)}\left\{S_{2}^{\left( 0,1 \right)} +S_{2}^{\left( 1,0 \right)}+  S_{2}^{\left( 0,1 \right)}S_{1}^{\left( 1,0 \right)} +S_{2}^{\left( 1,0 \right)}S_{1}^{\left( 0,1 \right)}+S_{2}^{\left( 1,0 \right)}S_{2}^{\left( 0,1 \right)}\right\}P_{M}^{\left( 1,1 \right)}\end{aligned}

$$

$S^{\left( 1,0 \right)}$ 和 $S^{\left( 0,1 \right)}$ 分别从收敛的
EOMIP-CCSD 和 EOMEA-CCSD 计算中提取，方法是对适当选取的、
对应于活性空穴和活性粒子的本征向量施加中间归一化
（intermediate normalization）。整个流程可描述如下：

-   求解基态耦合簇方程

-   构造 $\hat{\bar{H} }=e^{-\hat{T} }\hat{H}e^{\hat{T} }$

-   求解 EOMIP 和 EOMEA 方程

-   提取 $\hat{S}$ 振幅

-   构造第二个相似变换哈密顿量 $H_{I}^{\left( 1,1 \right)}$

-   在 CIS 空间中对 $H_{I}^{\left( 1,1 \right)}$ 进行对角化

STEOM-CCSD 中可用的自动活性空间选择方案以及所有加速选项
（包括 bt-PNO 和 COSX）同样可用于 IH-FSMR-CCSD。控制
IH-FSMR-CCSD 的所有关键词与 STEOM-CCSD 相似，详见
[sec:spectroscopyproperties.steom](#sec:spectroscopyproperties.steom)。

目前尚无 IH-FSMR-CCSD 的 UHF 变体。

<a id="sec:spectroscopyproperties.ihfsmr.properties"></a>
## 性质（Properties）

跃迁性质可以使用简单的类 CIS 公式计算，其中采用收敛的
IH-FSMR-CC 本征向量。在 IH-FSMR-CCSD 计算中，跃迁矩
默认即被计算。

<a id="sec:spectroscopyproperties.ihfsmr.Solvation"></a>
## 溶剂化修正（Solvation Correction）

溶剂效应可通过如下对 IH-FSMR-CCSD 的简单微扰修正来近似：

$$

\begin{aligned}
\omega_{k}=\omega^{0}_{k}+\frac{1}{2} \bar{V}^{\Delta}\bar{Q}^{\Delta}\end{aligned}

$$

其中

$$

\begin{aligned}
\omega^{0}_{k}=\hat{L_{K} }H_{I}^{\left( 1,1 \right)} \hat{R_{K} }\end{aligned}

$$

CPCM 修正直接进入 $H_{I}^{\left( 1,1 \right)}$，
即修改后的 Hatree-Fock 轨道。在非平衡（non-equilibrium）情形下，
可以简单地将微扰修正写为

$$

\begin{aligned}
\omega_{k}^{neq}=\omega^{0,neq}_{k}+\frac{1}{2} \bar{V}\left( P_{\Delta}^{neq}\right) \bar{Q}\left( P_{\Delta}^{neq}\right)\end{aligned}

$$

其中

$$

\begin{aligned}
P_{\Delta}^{neq}=L_{k}R_{k}\end{aligned}

$$

典型输入文件如下所示：

```orca
! aug-cc-pVDZ IH-FSMR-CCSD
!CPCM(water)
%mdci
NROOTS 8
DoSOLV true
DTol 1e-10
end
*xyz 0 1
O       0.0000  0.0000  0.1173
H       0.0000  0.7572 -0.4692
H       0.0000 -0.7572 -0.4692
*
```

对于上述输入，得到如下输出：

```orca
---------------------------------
     CALCULATED SOLVENT SHIFTS   
            CPCM  MODEL          
---------------------------------

Contributions of the 'fast' term to the solvent shift

 State Shift(Eh) Shift(eV) Shift(cm**-1) Shift(nm) E_FSMRCC(eV)  E_FSMRCC+SHIFT(eV)
-------------------------------------------------------------------------------
   0: -0.0058000 -0.158    -1273.0        3.3      7.814          7.656
   1: -0.0133523 -0.363    -2930.5        5.0      9.650          9.287
   2: -0.0053622 -0.146    -1176.9        1.8     10.144          9.998
   3: -0.0078092 -0.212    -1713.9        2.2     10.958         10.746
   4: -0.0040294 -0.110     -884.4        1.0     11.534         11.424
   5: -0.0137147 -0.373    -3010.0        3.3     12.003         11.630
   6: -0.0093172 -0.254    -2044.9        2.2     12.131         11.878
   7: -0.0077514 -0.211    -1701.2        1.7     12.562         12.352
```

该微扰修正只改变跃迁能量，既不改变波函数，也不改变跃迁矩。
