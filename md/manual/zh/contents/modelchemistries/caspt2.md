(sec:modelchemistries.caspt2)=
# 完全活性空间微扰理论（CASPT2 与 CASPT2-K）
```{index} CASPT2
```

全内收缩（fully internally contracted）的 CASPT2（FIC-CASPT2）方法可使用实数、虚数以及 IPEA
移位（shift）{cite}`caspt2,caspt2Shift,caspt2IShift`。ORCA 的实现采用了 CASPT2 的一种重新表述，
完全避免了在正则实现中会出现的四阶约化密度矩阵（reduced density
matrix）{cite}`kollmar_d4efficient_2021`。其中一些概念与 Sokolov 及其合作者报道的
一项新进展相通{cite}`sokolov_mradc_2020`。这一修改使得在大活性空间（active space）下
无需用累积量展开（cumulant expansion）等手段近似结果即可进行计算。

值得注意的是，OpenMOLCAS 中的 IPEA 移位与 ORCA 略有不同{cite}`openmolcas2019`。在本文中，
IPEA 移位 $\lambda$ 被加到内收缩 CSF
$\Phi^{pr}_{qs}=E^p_qE^r_s|\Psi^0>$ 的矩阵元上，并以广义 Fock 算符（generalized Fock operator）表示为

$$<\Phi^{p'r'}_{q's'}|\hat{F}|\Phi^{pr}_{qs}>+=<\Phi^{p'r'}_{q's'}|\Phi^{pr}_{qs}> \cdot \frac{\lambda}{2}\cdot (4+\gamma^p_p-\gamma^q_q+\gamma^r_r-\gamma^s_s),$$

其中 $\gamma^p_q=<\Psi^0|E^p_q|\Psi^0>$ 是自旋求迹激发算符（spin-traced excitation
operator）的期望值{cite}`caspt2ipea2`。标记 p、q、r、s 对应于一般分子轨道
（molecular orbital，即非活性、活性和虚拟轨道）。无论 ORCA 的实现如何，
IPEA 移位在普遍意义上的有效性仍存疑问，因此默认处于禁用
状态{cite}`zobel_ipea_2016`。ORCA 提供了一种称为 **CASPT2-K** 的替代表述，
它修订了零阶哈密顿量（zeroth order Hamiltonian）本身{cite}`caspt2k`。此处为向活性空间
加入或移除电子的激发类引入了两个额外的 Fock 矩阵。新的 Fock 矩阵由对应于
电子电离（ionization）与附着（attachment）过程的广义 Koopmans 矩阵导出。
所得方法更不易受入侵态（intruder state）影响，同时相比正则 CASPT2 方法更为精确。
更详细的讨论请参阅 Kollmar 等人的论文{cite}`caspt2k`。

CASPT2 与 CASPT2-K 与 [NEVPT2](sec:modelchemistries.nevpt2) 属于同一类方法家族。
两者的调用方式与 FIC-NEVPT2 方法完全类似。
注意，该方法可与 [RI 近似](sec:modelchemistries.nevpt2.ri)相结合。
然而与 NEVPT2 不同，CASPT2 表述需要存储整个波函数。因此，
与 ORCA 中的 NEVPT2 实现相比，可处理体系的范围要有限得多。下面是[可用选项的简要列表](sec:modelchemistries.caspt2.keywords)。

```orca
%casscf
  ...

  # mandatory
  PTMethod  FIC_CASPT2  # canonical CASPT2 approach
            FIC_CASPT2K # CASPT2-K with revised H0

  # optional
  TrafoStep RI      # optional for RI approximation for CASSCF and CASPT2
  PTSettings
    CASPT2_ishift 0.0    # imaginary level-shift
    CASPT2_rshift 0.0    # real      level-shift
    CASPT2_IPEAshift 0.0 # IPEA shift.
  end
end
```

CASPT2 也可以在任何有效的 CASSCF 输入之上通过简单关键词来设置。

```orca
!CASPT2       # FIC-CASPT2
!CASPT2K      # FIC-CASPT2-K
!RI-CASPT2    # FIC-CASPT2 with RI approximation
!RI-CASPT2K   # FIC-CASPT2-K with RI approximation
%casscf ...
```

## 示例：氮分子

在本短节中，我们将 CASPT2 结果加入到此前计算的 N$_{2}$ 分子的
[NEVPT2 势能面](sec:modelchemistries.nevpt2.n2)中。

```{literalinclude} ../../orca_working_input/n2_caspt2_scan.inp
:language: orca
```

CASPT2 输出会在计算之前列出各项设置。应检查所打印的参考权重（reference weight）。
较小的**参考权重**表明存在入侵态。同时，程序还会打印微扰表达式中的
**最小分母**（smallest denominator，在下面的片段中高亮显示）。较小的分母可能导致入侵态。


```orca
---------------------------------------------------------------
ORCA-CASSCF
---------------------------------------------------------------

...
PT2-SETTINGS:
A PT2 calculation will be performed on top of the CASSCF wave function (PT2=CASPT2)   
CASPT2 Real Levelshift            ...  0.00e+00
CASPT2 Im.  Levelshift            ...  0.00e+00
CASPT2 IPEA Levelshift            ...  0.00e+00
...
---------------------------------------------------------------
                           < CASPT2  >
---------------------------------------------------------------
...
-----------------------------------
CASPT2-D Energy =     -0.171839049
-----------------------------------

Class V0_ijab: dE=     -0.013891923
Class Vm1_iab: dE=     -0.034571085
Class Vm2_ab : dE=     -0.040985427
Class V1_ija : dE=     -0.003511548
Class V2_ij  : dE=     -0.000579508
Class V0_ia  : dE=     -0.075176596
Class Vm1_a  : dE=     -0.002917335
Class V1_i   : dE=     -0.000205627

smallest energy denominator IJAB =      3.237539973
smallest energy denominator ITAB =      2.500295823
smallest energy denominator IJTA =      2.339868413
smallest energy denominator TUAB =      1.664398302
smallest energy denominator IJTU =      1.342421639
smallest energy denominator ITAU =      1.496042538
smallest energy denominator TUVA =      0.706288250
smallest energy denominator ITUV =      0.545304334

...
 Iter           EPT2     EHylleraas  residual norm    Time
    1    -0.17183905    -0.17057203     0.03246225     0.0
    2    -0.17057203    -0.17119523     0.00616509     0.0
    3    -0.17117095    -0.17121211     0.00086389     0.0
    4    -0.17120782    -0.17121281     0.00013292     0.0
    5    -0.17121273    -0.17121282     0.00000990     0.0
    6    -0.17121283    -0.17121282     0.00000159     0.0
    7    -0.17121282    -0.17121282     0.00000020     0.0
 
 CASPT2 calculation converged in 7 iterations

...
 ===============================================================
 CASPT2 Results  
 ===============================================================
   *********************
   MULT 1, ROOT 0 
   *********************
   
  Class V0_ijab :        dE = -0.013831560889
  Class Vm1_iab :        dE = -0.034124733943
  Class Vm2_ab  :        dE = -0.041334010085
  Class V1_ija  :        dE = -0.003446396316
  Class V2_ij   :        dE = -0.000584401134
  Class V0_ia   :        dE = -0.074688029120
  Class Vm1_a   :        dE = -0.002962355569
  Class V1_i    :        dE = -0.000241331405

 ---------------------------------------------------------------
         Total Energy Correction : dE = -0.17121281846205
 ---------------------------------------------------------------
         Reference  Energy       : E0 = -108.66619981448225
         Reference Weight        : W0 = 0.94765190644139
 ---------------------------------------------------------------
         Total Energy (E0+dE)    : E  = -108.83741263294431
 ---------------------------------------------------------------
```

注意，程序会在进入 CASPT2 迭代之前打印 CASPT2-D 结果{cite}`caspt2`。若存在入侵态，
残差方程可能无法收敛。程序不会中止。因此，检查每次 CASPT2 运行的收敛性非常重要。
在这个使用小基组的特定示例中并不存在入侵态。

(fig:caspt2scan)=
```{figure} ../../images/n2_caspt2_scan.*

CASSCF(6,6) 与 CASPT2 计算（def2-SVP）得到的 N$_2$ 分子势能面（Potential Energy Surface）。
```

{numref}`fig:caspt2scan` 中的势能面
确实与 FIC-NEVPT2 方法非常相似，而后者更高效（无需迭代）也更稳健（不存在入侵态）。
图中还给出了 CASPT2-K 的结果，它通常是两种方法之间的折衷。正如预期的那样，
与 CASPT2 的最大偏差出现在解离极限（dissociation limit）处，此时开壳层特性
在参考波函数中占主导地位。在此示例中，三种方法之间的差异相当细微。
然而，在某些具有挑战性的体系上（例如 CASPT2-K 论文中研究的铬二聚体（Chromium dimer）），
结果可能会有实质性差异。{cite}`caspt2k`。尽管存在缺陷，CASPT2 方法仍具有
历史重要性，并且依然是一种流行的理论方法。未来我们可能会考虑进一步扩展，
例如 (X)MS-CASPT2{cite}`xmscaspt2`。

(sec:modelchemistries.caspt2.keywords)=
## 关键词（Keywords）

```orca
%casscf
  ...

  MULT   1,3 # multiplicity block
  NRoots 3,2 # number of roots for the MULT blocks

  TrafoStep RI      # optional for RI approximation for CASSCF and CASPT2
  PTMethod  FIC_CASPT2  # canonical CASPT2 approach
            FIC_CASPT2K # CASPT2-K with revised H0

  # detailed settings (this is optional)
  PTSettings
    CASPT2_ishift 0.0    # imaginary level-shift
    CASPT2_rshift 0.0    # real      level-shift
    CASPT2_IPEAshift 0.0 # IPEA shift.
    MaxIter       20     # maximum for the CASPT2 iterations
    MaxDIIS       7      # maximum dimension of the DIIS expansion
    
    # intruder state warnings
    TSmallDenom   1e-2   # printing thresh for small denominators

    # general settings
    NThresh 1e-6  # FIC-CASPT2 cut off for linear dependencies
    D4Tpre  1e-12 # truncation of the 4-pdm
    D3Tpre  1e-14 # truncation of the 3-pdm
    EWIN  -3,1000 # Energy window for the frozencore setting fc_ewin

    # option to skip the PT2 correction for all states except for the ones
    # specified for a selected multiplicity block and root 
    # selectedRoots[block]  = root number counting from 0.
    selectedRoots[0]=0,1 # compute MULT=1 root=0,1 and skip all others.

    #CASPT2-K specific options
    TReg 1e-2 # default for the Tikhonov reguralization
  end

end
```
