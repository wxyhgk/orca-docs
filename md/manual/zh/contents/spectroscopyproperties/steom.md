```{index} STEOM
```

(sec:spectroscopyproperties.steom)=
# 通过 STEOM-CCSD 计算激发态（Excited States via STEOM-CCSD）

```{index} Excited States via STEOM
```

由于 O($N^{6}$) 的标度关系，EOM-CCSD 激发能方法对大体系而言
代价高得难以承受。因此，需要一种更紧凑的波函数拟设形式。
第二次相似变换可以将最终的矩阵对角化步骤压缩到仅 CIS 空间。
由此得到的 Marcel Nooijen 及其合作者的 STEOM-CCSD 方法{cite}`Rodney1997JCP`
是精确计算激发能的一种高效途径。

(sec:spectroscopyproperties.steom.general)=
## 一般性描述（General Description）

在标准 EOM-CC 方法中，变换后的哈密顿量在单激发和双激发空间中
对角化，以获得参考态的电离态、附着态或激发态。在 STEOM-CC 中，
再进行一次相似变换

$$\begin{aligned}
\hat{G}=\{e^{\hat{S} }\}^{-1}\hat{\bar{H} }\{e^{\hat{S} }\}\end{aligned}$$

变换算符 $\hat{S}$（包含单激发和双激发）定义为

$$\begin{aligned}
\hat{S}=\hat{S}^{IP}+\hat{S}^{EA},\end{aligned}$$

$$\begin{aligned}
\hat{S}^{IP}=S_{i^{\prime} }^{m}\hat{E}^{m}_{i^{\prime} }+\dfrac{1}{2}S^{mb}_{ij}\hat{E}^{mb}_{ij},\end{aligned}$$

$$\begin{aligned}
\hat{S}^{EA}=S^{a^{\prime} }_{e}\hat{E}_{e}^{a^{\prime} }+\dfrac{1}{2}S^{ab}_{ej}\hat{E}^{ab}_{ej}.\end{aligned}$$

在上述方程中，$m$ 和 $e$ 分别表示空穴型和粒子型的活性指标，
而撇号表示限制到非活性轨道。算符 $\hat{S}$ 的振幅定义为
使得变换后哈密顿量在二次量子化记号下的矩阵元等于零。

$$\begin{aligned}
g_{i^{\prime} }^{m}=g_{ij}^{mb}=g^{a^{\prime} }_{e}=g^{ab}_{ej}=0\end{aligned}$$

此外，求解 CCSD 方程后 $\bar{H}$ 中原有的零元仍保持不变。
上述方程对 $\hat{S}$ 是线性的，等价于单价问题的
Fock 空间多参考耦合簇方程。然而，为确保数值稳定性，
这些方程被改写为矩阵对角化问题，并作为 IP-EOM-CCSD 和
EA-EOM-CCSD 问题求解。然后，$\hat{S}^{IP}$ 和 $\hat{S}^{EA}$
分别从收敛的先前计算中提取，方法是对适当选取的、
对应于活性空穴和活性粒子的本征向量施加中间归一化
（intermediate normalization）。整个流程可描述如下：

-   求解基态耦合簇方程

-   构造第一个相似变换哈密顿量
    $\hat{\bar{H} }=e^{-\hat{T} }\hat{H}e^{\hat{T} }$

-   求解 IP-EOM 和 EA-EOM 方程

-   提取 $\hat{S}$ 振幅

-   构造第二个相似变换哈密顿量
    $\hat{\bar{G} }=e^{-\hat{S} }\hat{\bar{H} }e^{\hat{S} }$

-   在 CIS 空间中对 $\hat{\bar{G} }$ 进行对角化

上述方法的优点在于，它不需要一次迭代的 O($N^{6}$) 标度对角化步骤，
而是需要两次迭代的 O($N^{5}$) 标度步骤、一次非迭代的 O($N^{5}$) 标度步骤
和一次迭代的 O($N^{4}$) 标度矩阵对角化步骤。
所谓"隐式三重激发"项的存在确保了激发态的电荷转移可分离性，
而这在 EOM-CCSD 中是缺失的。此外，由于最终对角化步骤在
CIS 空间中进行，自旋适配是平凡的，并且无需经历基于自旋轨道
实现的复杂性即可获得三重态多重度的激发态。

STEOMCC 方法最近也已扩展到 UHF 形式下的开壳层体系应用{cite}`huntington2017UHFSTEOM`{cite}`casanova_neese_2024`。
在这种情况下，算符 $\hat{S}^{IP}$ 和 $\hat{S}^{EA}$ 的表达式为

$$\begin{aligned}
\hat{S}^{IP}&=\frac{1}{2}\sum_{i,e,a,b}s_{ie}^{ab}\big\{\hat{a}^{\dagger}\,\hat{b}^{\dagger}\,\hat{e}\,\hat{i}\big\}+\sum_{\bar{i},e,\bar{a},b}s_{\bar{i}e}^{\bar{a}b}\big\{\hat{\bar{a} }^{\dagger}\,\hat{b}^{\dagger}\,\hat{e}\,\hat{\bar{i} }\big\}\nonumber\\
&+\frac{1}{2}\sum_{\bar{i},\bar{e},\bar{a},\bar{b} }s_{\bar{i}\bar{e} }^{\bar{a}\bar{b} }\big\{\hat{\bar{a} }^{\dagger}\,\hat{\bar{b} }^{\dagger}\,\hat{\bar{e} }\,\hat{\bar{i} }\big\}+\sum_{i,\bar{e},a,\bar{b} }s_{i\bar{e} }^{a\bar{b} }\big\{\hat{a}^{\dagger}\,\hat{\bar{b} }^{\dagger}\,\hat{\bar{e} }\,\hat{i}\big\},\\
\widehat{S}_{-}&=\frac{1}{2}\sum_{i,j,a,m}s_{ij}^{am}\big\{\hat{a}^{\dagger}\,\hat{m}^{\dagger}\,\hat{j}\,\hat{i}\big\}+\sum_{\bar{i},j,\bar{a},m}s_{\bar{i}j}^{\bar{a}m}\big\{\hat{\bar{a} }^{\dagger}\,\hat{m}^{\dagger}\,\hat{j}\,\hat{\bar{i} }\big\}\nonumber\\
&+\frac{1}{2}\sum_{\bar{i},\bar{j},\bar{a},\bar{m} }s_{\bar{i}\bar{j} }^{\bar{a}\bar{m} }\big\{\hat{\bar{a} }^{\dagger}\,\hat{\bar{m} }^{\dagger}\,\hat{\bar{j} }\,\hat{\bar{i} }\big\}+\sum_{i,\bar{j},a,\bar{m} }s_{i\bar{j} }^{a\bar{m} }\big\{\hat{a}^{\dagger}\,\hat{\bar{m} }^{\dagger}\,\hat{\bar{j} }\,\hat{i}\big\}.\end{aligned}$$

其中我们用上划线区分 $\beta$ 轨道和 $\alpha$ 轨道。
振幅 $\big\{s_{ie}^{ab}, s_{\bar{i}e}^{\bar{a}b}\big\}$ 由求解
$\alpha$ 电子附着的 UHF EA-EOM-CCSD 方程确定，而
$\big\{s_{\bar{i}\bar{e} }^{\bar{a}\bar{b} }, s_{i\bar{e} }^{a\bar{b} }\big\}$
振幅则从 $\beta$ 电子附着的 UHF EA-EOM-CCSD 计算中提取。
类似地，振幅集合 $\big\{s_{ij}^{am}, s_{\bar{i}j}^{\bar{a}m}\}$ 和
$\big\{s_{\bar{i}\bar{j} }^{\bar{a}\bar{b} }, s_{i\bar{j} }^{a\bar{m} }\big\}$
分别由求解 $\alpha$ 电子电离和 $\beta$ 电子电离的解耦
UHF IP-EOM-CCSD 问题确定。因此，一次 UHF STEOMCC 计算涉及
两次独立的 IP 计算（O($N^{5}$) 标度）和两次独立的 EA 计算
（O($N^{5}$) 标度步骤）。

EOM-CCSD 中可用的所有加速选项（包括 CCSD(2)（仅在 RHF 实现中可用）
和 COSX）在 STEOMCC 中同样可用。STEOMCC 计算中最重要的步骤是
IP-EOM 和 EA-EOM 计算。这些步骤使用 EOM-CCSD 模块执行，
相关关键词与 {ref}`sec:spectroscopyproperties.eom` 中所述相同。
RHF STEOM 模块特有的关键词是：

```orca
%mdci
#
#RHF STEOM parameters - defaults displayed
DoCISNat true     # automatic selection of active space       
NActIP  3         # number of states defined as active in the IP calculation
NActEA  2         # number of states defined as active in the EA calculation
DoTriplet false   # target state of triplet multiplicity
DoDbFilter true   # filters out states with doubles excitation  character 
DoNewActSch true  # new active space selection scheme for STEOM-CCSD                             
DoSOLV            # perturbative correction for solvation effects (experimental) 
#
#Default values for automatic active space selection scheme
OThresh 0.001   # Cut off occupation of CIS natural orbitals in IP calculation 
VThresh 0.001   # Cut off occupation of CIS natural orbitals in EA calculation 
IPSThrs 80      #  The percentage singles threshold for the IP calculation
EASThrs 80      #  The percentage singles threshold for the EA calculation
end
```

UHF STEOM 模块相关的关键词是：

```orca
%mdci
#UHF STEOM parameters - defaults displayed
DoCISNat true        # automatic selection of active space       
NActIP_a  3          # number of states defined as active in the IP calculation 
                     # for the removal of an α electron
NActIP_b  3          # number of states defined as active in the IP calculation 
                     # for the removal of a β electron
NActEA_a  2          # number of states defined as active in the EA calculation 
                     # for the attachment of an α electron
NActEA_b 2           # number of states defined as active in the EA calculation 
                     # for the attachment of a β electron
DoDbFilter true      # filters out states with doubles excitation  character 
UseQROs  false       # use QROs or not
DoNewActSch true     # new active space selection scheme for STEOM-CCSD                             
#Default values for automatic active space selection scheme
OThresh 0.001        # Cut off occupation of CIS natural orbitals in tIP calculations
VThresh 0.001        # Cut off occupation of CIS natural orbitals in EA calculations 
IPSThrs 80           #  The percentage singles threshold for the IP calculations
EASThrs 80           #  The percentage singles threshold for the EA calculations
end
```

(sec:spectroscopyproperties.steom.active)=
## 活性空间的选择（Selection of Active space）

STEOM-CC 计算的结果取决于在 EOMIP 和 EOMEA 计算中被选为活性的
根的数目。在 ORCA 中，它们通过使用态平均 CIS 自然跃迁轨道
（NTO）自动选取。默认情况下，这一初始 CIS 计算中包含的根数
等于 STEOM 中请求的根数（`NRoots`）。不过，可以通过将
`NRootsCISNAT` 设为更高值来修改。然后选取占据数不超过预定义值的
轨道作为 EOMIP 和 EOMEA 计算中的活性轨道，这分别由关键词
`OThresh` 和 `VThresh` 控制。目前有两种选取活性空间的方式。
一种是使用参考文献 {cite}`Dutta2017STEOM` 中描述的 NTO 百分比占据判据。
然而，一种更新且更稳健的方法是使用绝对占据判据，这也是当前实现中的默认方式。
可以通过将 `DoNewActSch` 设为 false 来启用旧的基于百分比占据的
活性空间选择（不推荐）。

也可以通过将 `DoCISNat` 设为 false 并将 `NActIP` 和 `NActEA`
（RHF STEOM 计算）或 `NActIP_a`、`NActIP_b`、`NActEA_a` 和 `NActEA_b`
（UHF STEOM 计算）设为所需值来手动选择活性空间。不过，
对于一般用途并不推荐这样做。下面的片段展示了一个闭壳层分子上
活性轨道选择过程的输出：

```orca
------------------------------------------
STATE AVERAGED NATURAL ORBITALS FOR ACTIVE SPACE SELECTION
------------------------------------------

Solving eigenvalue problem for the occupied space  ... Occupied block occupation :  
     0   0.000478 
     1   0.002266 
     2   0.169928 
     3   0.171663 
     4   0.310125 
     5   0.345541 
Orbital taken as active for IP roots:  
     0   0.345541 
     1   0.310125 
     2   0.171663 
     3   0.169928 
done
Solving eigenvalue problem for the virtual space   ... Virtual block occupation :  
     6   0.640886 
     7   0.332262 
     8   0.017272 
     9   0.005326 
    10   0.001752 
    11   0.000667 
    12   0.000574 
    13   0.000540 
    14   0.000160 
    15   0.000150 
    16   0.000139 
    17   0.000086 
    18   0.000082 
    19   0.000037 
    20   0.000023 
    21   0.000016 
    22   0.000013 
    23   0.000008 
    24   0.000003 
    25   0.000002 
    26   0.000001 
    27   0.000000 
    28   0.000000 
    29   0.000000 
    30   0.000000 
    31   0.000000 
    32   0.000000 
    33   0.000000 
    34   0.000000 
    35  -0.000000 
Orbital taken as active for EA roots :  
     0   0.640886 
     1   0.332262 
     2   0.017272 
done
 No of roots active in IP calculation:    4  
 No of roots active in EA calculation:    3
```

(sec:spectroscopyproperties.steom.tddftguess)=
## 使用 TD-DFT 密度进行活性空间选择（Active space selection using TD-DFT densities）

除了使用 CIS 计算来选择活性空间的根之外，也可以考虑基于 TD-DFT 的方式。
请注意，使用 DFT Kohn-Sham 轨道计算 CCSD 基态能量可能会导致
某些不稳定并给出不正确的结果。

这种方法的主要好处是可以用 TD-DFT 电子密度启动 STEOM-CCSD 计算，
这些密度通常优于 CIS 密度，尤其对某些特定化合物（例如金属配合物）而言。
计算得到的 TD-DFT 密度也往往比 CIS 密度更稳定。不过，它会拖慢计算速度。

输入必须这样写：

```orca
!RHF/UHF BHANDHLYP STEOM-CCSD TZVP 

%mdci
nroots 10
tddftguess true
end

%tddft
nroots 10
end

*xyz 0 1
```

任何 DFT 泛函都可以使用，但我们推荐使用含有相当比例 HF 交换的泛函。
除此之外，必须在 mdci 块中将关键词 `TDDFTGuess` 设为 true，
并添加 tddft 及 `NRoots` 关键词。在两个输入块（`%mdci` 和 `%tddft`）中
必须给出相同数量的根。从 ORCA 6 开始，也可以在 UHF 参考下
使用 TD-DFT 初始猜测。

(sec:spectroscopyproperties.steom.reliability)=
## 计算激发能的可靠性（Reliability of the Calculated Excitation Energy）

STEOM-CC 中计算的任何态的激发能，只有当该态的主导激发被限制在
活性空间内时才是可靠的。这可以从计算态的活性特征百分比来验证，
这是一个*事后*诊断量，定义为

$$\begin{aligned}
A = \frac{\sum\limits_{m,e} C(m,e) \cdot C(m,e) }{\sum\limits_{i,a} C(i,a) \cdot C(i,a) }*100\end{aligned}$$

（闭壳层体系），在 UHF 形式下则为

$$\begin{aligned}
A =\frac{\sum\limits_{m,e}C(m,e) \cdot C(m,e)+\sum\limits_{\bar{m},\bar{e} }C(\bar{m},\bar{ e}) \cdot C(\bar{m},\bar{ e}) }{\sum\limits_{i,a}C(i,a) \cdot C(i,a)+\sum\limits_{\bar{i},\bar{a} }C(\bar{i},\bar{a}) \cdot C(\bar{i},\bar{a}) } \cdot 100.\end{aligned}$$

$A$ 高于 98.0 的根被认为相对于活性空间已经收敛。{cite}`Dutta2018eomvert`

```orca
------------------
STEOM-CCSD RESULTS
------------------

IROOT=  1:  0.145412 au     3.957 eV   31914.3 cm**-1
  Amplitude    Excitation
  -0.169361     4 ->   8
  -0.984822     7 ->   8

Percentage Active Character     99.86

  Amplitude    Excitation in Canonical Basis
  -0.166580     4 ->   8
  -0.975432     7 ->   8
  -0.124356     7 ->  13

IROOT=  2:  0.309409 au     8.419 eV   67907.5 cm**-1
  Amplitude    Excitation
   0.994141     7 ->   9

Percentage Active Character     99.78

  Amplitude    Excitation in Canonical Basis
  -0.990029     7 ->   9

IROOT=  3:  0.336993 au     9.170 eV   73961.4 cm**-1
  Amplitude    Excitation
  -0.994078     5 ->   8

Percentage Active Character     99.10

  Amplitude    Excitation in Canonical Basis
  -0.984116     5 ->   8
  -0.136769     5 ->  13

IROOT=  4:  0.357473 au     9.727 eV   78456.2 cm**-1
  Amplitude    Excitation
   0.181761     4 ->  10
   0.728209     6 ->   8
   0.611668     7 ->  10
  -0.191540     7 ->  12

Percentage Active Character     94.10

Warning:: the state may have not converged with respect to active space 
-------------------- Handle with Care -------------------- 

  Amplitude    Excitation in Canonical Basis
  -0.184144     4 ->  10
  -0.725183     6 ->   8
  -0.633718     7 ->  10

IROOT=  5:  0.386654 au    10.521 eV   84860.8 cm**-1
  Amplitude    Excitation
   0.980406     4 ->   8
  -0.178551     7 ->   8

Percentage Active Character     99.79

  Amplitude    Excitation in Canonical Basis
   0.971678     4 ->   8
   0.122877     4 ->  13
  -0.179242     7 ->   8

IROOT=  6:  0.444881 au    12.106 eV   97640.1 cm**-1
  Amplitude    Excitation
  -0.995150     6 ->   9

Percentage Active Character     99.69

  Amplitude    Excitation in Canonical Basis
  -0.989966     6 ->   9
```

如果任何计算态的 $\% active  character$ 小于 98，
该态可能相对于活性空间尚未收敛，该特定态的激发能不太可靠。
在这种情况下，用户应请求更多数量的根。

(sec:spectroscopyproperties.steom.remove)=
## 移除具有双激发特征的 IP 和 EA 态（Removal of IP and EA states with double excitation character）

为获得 STEOM-CCSD 的准确结果，只有对应于单激发主导态的 $\hat{S}$
振幅才应包含在第二次相似变换中。在 ORCA 中，这通过两种方式确保。
首先，默认激活根追踪（`FollowCIS`），使其收敛到由单激发试探向量
主导的态。这避免了计算所谓的"卫星态"（satellite states），
即相对于基态具有双激发特征的态。其次，在收敛的 IP 和 EA 根中，
单激发百分比低于某个预定义阈值（由关键词 `IPThresh` 和
`EAThresh` 控制）的态会自动从第二次相似变换中排除。

```orca
EOM-CCSD RESULTS
----------------

IROOT=  1:  0.105316 au     2.866 eV   23114.2 cm**-1
  Amplitude    Excitation
   0.697547     x ->   8
IROOT=  2:  0.217925 au     5.930 eV   47829.1 cm**-1
  Amplitude    Excitation
  -0.701454     x ->   9
IROOT=  3:  0.304098 au     8.275 eV   66741.8 cm**-1
  Amplitude    Excitation
  -0.700458     x ->  10
IROOT=  4:  0.350387 au     9.535 eV   76901.1 cm**-1
  Amplitude    Excitation
   0.702705     x ->  11
IROOT=  5:  0.651462 au    17.727 eV  142979.4 cm**-1
  Amplitude    Excitation
   0.637352     x ->  12
   0.121747     x ->   8     4 ->  10
   0.177039     x ->   8     5 ->   9
   0.109987     x ->   9     5 ->   8
  -0.206789     x ->   8     7 ->  10
  -0.109870     x ->  10     7 ->   8

EA STATE=  0:  percentage singles     95.282 
EA STATE=  1:  percentage singles     96.981 
EA STATE=  2:  percentage singles     96.540 
EA STATE=  3:  percentage singles     97.844 
EA STATE=  4:  percentage singles     68.884 

Warning: high double excitation character, excluding from the STEOM transformation
 Final no active EA roots:    4
```

请注意，使用 CIS 自然跃迁轨道可能导致以双激发特征为主的
IP 和 EA 态出现收敛问题。这可以通过将 `DoDbFilter` 设为 true 来解决。

(sec:spectroscopyproperties.store)=
## 跃迁密度与差分密度（Transition and difference densities）

在 STEOM 计算结束时，可以将最终本征向量存储到文件 "*job.cis*" 中，
这与 CIS 和 TD-DFT 计算中的做法类似。通过在输入中设置
`DoStoreSTEOM true` 即可获得该文件。然后可以用 `orca_plot` 处理
该文件，得到差分密度和/或跃迁密度。

也可以在 STEOM-CCSD 方案内进行自然跃迁轨道分析，详见
{ref}`sec:spectroscopyproperties.tddft.natTransOrb`。通过将关键词
`DoSTEOMNatTransOrb` 设为 true 即可执行。

(sec:spectroscopyproperties.steom.properties)=
## 性质（Properties）

偶极矩和跃迁矩（以及振子强度）可以在 STEOM 模块中使用不同类型的
近似计算。请引用我们关于这些修正的 STEOM 跃迁密度的论文{cite}`ghosh_new_2020`！
从 ORCA 5 开始，使用了新的默认设置（`DoSimpleDens false`），
它比之前的类 CIS 近似好得多，而完整选项则具有 CC3 级别的质量。

```orca
%mdci

DosimpleDens false  # Default, using STEOM-CCSD density + some doubles effect.
AddL2term true

DosimpleDens false  # using the STEOM-CCSD density + some doubles effect.
AddL2term true      # + neglected GS doubles
UpdateL1 true

DosimpleDens false  # using the STEOM-CCSD density + some doubles effect.
AddL2term true      # + neglected GS double + doubles from EOM-CCSD
UpdateL1 true       # (expensive, but of CC3 quality - see reference)
AddDDTerm true

end
```

默认情况下，如参考文献 {cite}`ghosh_new_2020` 中所讨论的，
所有计算都应使用带有 `AddL2term true` 的 STEOM-CCSD 密度。

(sec:spectroscopyproperties.steom.solvatation)=
## 溶剂化（实验性，Solvation (Experimental)）

在 STEOM-CCSD 中，激发能和密度可以使用 ORCA 中的 CPCM 溶剂化方案
进行修正。

要使用它，必须在 `%mdci` 块中将关键词 `DoSolv` 设为 true，
并给出简单关键词 `CPCM`（或 `SMD`）加溶剂名称。

```orca
!CPCM(ethanol) STEOM-CCSD TightSCF def2-TZVP def2-TZVP/C def2/J 

%mdci
Nroots 5
DoSolv true
end
```

(sec:spectroscopyproperties.steom.SOC)=
## 自旋-轨道耦合（实验性，Spin-Orbit Coupling (Experimental)）

可以使用关键词 `STEOMSOC true` 计算 STEOM-CCSD 中单重态和三重态
之间的自旋-轨道耦合。
请注意，目前所有 SOC 矩阵元和性质都**仅从右矢量**计算！

(sec:spectroscopyproperties.steom.core)=
## 芯激发（Core excitation）

STEOM-CCSD（以及 bt-PNO-STEOM-CCSD）方法也可用于计算分子的
K 边芯激发能。详见
{ref}`sec:spectroscopyproperties.eomcore.core-excitation`。

(sec:spectroscopyproperties.steom.trans)=
## 瞬态吸收（Transient absorption）

可以使用关键词 `DoTrans true` 计算瞬态吸收谱。
`IRoot` 关键词将选择目标激发态。
