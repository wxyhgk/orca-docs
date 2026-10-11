
现在将这与用一些单参考方法计算的相应能量差进行比较。一个典型输入是（这是一个 somewhat old-fashioned 的例子——在当前程序版本中您会做全价 CASSCF(10,8) 或 CASSCF(6,6) 并用单个关键词调用 MR 方法）：

```orcainput
! HF def2-SVP def2-TZVPP/C VeryTightSCF NoPop

%base "1"

* xyz 0 1
N 0 0 0
N 0 0 1.0977
*
%method 
     frozencore fc_ewin
end

%mrci 
     EWin          -3,1000
     CIType       MRACPF2a
     Solver           DIIS
     IntMode      FullTrafo 
     UseIVOs          true
     AllSingles       true
     TSel            1e-14
     TPre            1e-05
     TNat              0.0  
     ETol            1e-10
     RTol            1e-10 
     NewBlock 1 *
          NRoots 1
          Excitations CISD
          refs CAS(0,0) end
     end
end

$new_job

! ROHF def2-SVP def2-TZVPP/C VeryTightSCF NoPop PModel

%base "2"

* xyz 0 4
N 0 0 0
*
%method 
       frozencore fc_ewin
end

%mrci  
      EWin          -3,1000
      CIType       MRACPF2a
      IntMode      FullTrafo 
      UseIVOs          true
      AllSingles       true
      TSel            1e-14
      TPre            1e-05
      TNat              0.0
      ETol            1e-10
      RTol            1e-10
      NewBlock 4 *
          NRoots 1
          Excitations CISD
          refs CAS(3,3) end
      end
end
```

结果是：

```orca
Single reference approaches:
  Method   N2-Molecule         N-Atom        Delta-E
  CISD+Q : -109.167 904        -54.422 769    8.77 eV
  ACPF   : -109.166 926        -54.421 783    8.80 eV
  ACPF2  : -109.166 751        -54.421 333    8.82 eV
  ACPF2a : -109.166 730        -54.421 186    8.83 eV
  CEPA1  : -109.159 721        -54.422 564    8.56 eV
  CEPA2  : -109.172 888        -54.422 732    8.91 eV
  CEPA3  : -109.161 034        -54.422 589    8.59 eV
  AQCC   : -109.160 574        -54.420 948    8.67 eV
  CEPA-0 : -109.174 924        -54.422 951    8.95 eV
```

除 CEPA1 和 CEPA3 外，结果都是可以的。这些方法表现不佳的原因很简单：实现的形式体系只对闭壳层正确——开壳层需要不同的形式体系，MRCI 模块中没有（但单参考 MDCI 模块中有）。由于 CEPA2 中所做的简单近似，它也应该对开壳层有效，数值结果支持这一点。

接下来我们转向多参考方法，取与 CO 相同的 CAS(10,8) 参考以关联所有价电子。[^4]

```orca
Multi reference approaches:
  Method     N2-Molecule         N-Atom        Delta-E
  MRCISD+Q: -109.180 089        -54.422 667    9.11 eV
  MRACPF  : -109.178 708        -54.421 685    9.12 eV
  MRACPF2 : -109.177 140        -54.421 236    9.11 eV
  MRAQCC  : -109.175 947        -54.420 851    9.10 eV
  SORCI   : -109.179 101        -54.422 703    9.08 eV
```

这个测试计算令人满意地展示了多参考方法的高度一致性，它们都或多或少收敛到相同的结果，这一定是准确的。

(sec:modelchemistries.mrci.spinflip)=
## 能量差——自旋翻转

有许多有趣的情况涉及来自不同多重度但相同轨道组态的两个态之间的微小能量差。这就是双自由基或过渡金属配合物中磁耦合遇到的现象。作为这种情况的原始模型，可以考虑线性构型的假想分子 H-Ne-H，本节将用它作为模型。

参考值由所有价电子活性的 MR-ACPF 计算得到（同样，这个例子 somewhat old fashioned——在当前程序版本中您会做 CASSCF 计算然后用单个关键词调用 MR 方法）：

```{literalinclude} ../../orca_working_input/C05S10_183.inp
:language: orca
```

给出参考值 108 cm$^{-1}$。我们现在将其与只将两个"磁"轨道（氢上的 1s）放在活性空间中的几种其他方法比较：

```orca
... same as above
%mrci  EWin       -10,1000
       CIType      MRDDCI3
       ... same as previously
       NewBlock 1 *
          NRoots 1
          refs CAS(2,2) end
          end
       NewBlock 3 *
          NRoots 1
          refs CAS(2,2) end
          end
       end
```

结果是：

```orca
Method      S-T gap
MR-CI+Q  :  98 cm-1
MR-CI    :  93 cm-1
MR-ACPF  :  98 cm-1
MR-ACPF2 :  98 cm-1
MR-ACPF2a:  97 cm-1
MR-AQCC  :  95 cm-1
SORCI    : 131 cm-1
MR-DDCI2 :  85 cm-1
MR-DDCI3 : 130 cm-1
```

所有这些方法都给出好结果，SORCI 的误差比其他的略大。（差值专用 CI）DDCI2 方法略微低估了耦合，这是该方法的特征。DDCI3 给出与 SORCI 相同的结果在某种意义上是好的，因为 SORCI 应该近似 DDCI3（或更好的 IDDCI3）结果，它显然做到了。

这个分裂也可以用破缺对称 HF 和 DFT 方法研究，如本手册其他地方所述：

```orca
Method    S-T gap
 UHF     : 70 cm-1
 B3LYP/G : 240 cm-1
 BP86    : 354 cm-1
 PW91    : 234 cm-1
 PBE     : 234 cm-1
 PBE0    : 162 cm-1
 RPBE    : 242 cm-1
```

这证实了通常的观念；UHF 低估耦合，DFT 高估耦合，杂化泛函比 GGA 高估得少。BP86 比 PW91 或 PBE 差。PBE0 杂化可能是 DFT 方法中最好的。由于某种原因，如果将 BS 态简单地作为真正开壳层单重态的近似，大多数 DFT 方法给出最好的结果。我们认为这没有理论支持，但也被其他作者观察到。

现在让我们研究对 T$_{\text{sel} }$ 的依赖性，因为这应该是关键的（我们使用 DDCI3 方法）：

```orca
Tsel     S-T gap
    1e-04     121
    1e-05     128
    1e-06     132
    1e-07     131
    1e-08     131
    1e-10     131
    1e-12     131
    0         131
```

一旦包含 `AllSingles`，收敛就非常好。

(sec:modelchemistries.mrci.surface)=
## 势能面

需要多参考方法的另一种情况是研究键断裂并想计算完整的势能面。比如说我们想计算 CH 分子的势能面。首先我们需要弄清楚要包含哪些态。因此，让我们首先为全价 CASSCF 参考态确定相当数量的根（我们用小基组使任务快速）。

```{literalinclude} ../../orca_working_input/C05S10_188.inp
:language: orca
```

结果是：

```orca
-------------------
TRANSITION ENERGIES
-------------------

The lowest energy is    -38.308119994 Eh

State Mult Irrep Root Block    mEh          eV      1/cm
  0    2    -1    0    0      0.000      0.000       0.0
  1    2    -1    1    0      0.000      0.000       0.0
  2    4    -1    0    1     14.679      0.399    3221.6
  3    2    -1    2    0    126.464      3.441   27755.7
  4    2    -1    3    0    126.464      3.441   27755.7
  5    2    -1    4    0    132.689      3.611   29121.8
  6    2    -1    5    0    164.261      4.470   36051.2
  7    2    -1    6    0    305.087      8.302   66958.9
  8    2    -1    7    0    305.087      8.302   66958.9
  9    4    -1    1    1    328.911      8.950   72187.7
 10    4    -1    2    1    452.676     12.318   99350.8
 11    4    -1    3    1    452.676     12.318   99350.8
 12    2    -1    8    0    460.116     12.520  100983.9
 13    2    -1    9    0    463.438     12.611  101712.9
 14    2    -1   10    0    463.438     12.611  101712.9
 ...
```

因此，如果我们想关注低能态，应该包含五个双重态和一个四重态根。现在我们用这些根运行第二个任务并扫描核间距。

```{literalinclude} ../../orca_working_input/C05S10_189.inp
:language: orca
```

此运行得到的势能面如 {numref}`fig:16` 所示。您可以清楚地看到 $^{2}\Sigma$ 和 $^{2}\Delta$ 态在接近平衡距离处的交叉，以及 $^{4}\Sigma$ 态与 $^{2}\Pi$ 和 $^{2}\Sigma$ 向渐近线的合并，在那里 C-H 解离为 $^{3}$P 基态的中性 C 原子和 $^{2}$S 基态的中性氢原子。您可以观察到一旦 `AllSingles` 设为 true（默认值），MRCI 模块的默认设置就给出相当光滑的势能面。

(fig:16)=
```{figure} ../../images/616.*

用 MRCI+Q 方法计算的 CH 某些低能态势能面
```

在许多情况下，人们会关注极小值附近的区域，那里势能面几乎是二次的。在这种情况下仍然可以进行几个（2、3、5 点）多项式拟合，从中可以确定重要参数。在这些情况下必须研究数值精度和对 $T_\text{sel}$ 的行为，因为选择会在过程中产生一些噪声。我们用 HF 分子的计算来说明：

```{literalinclude} ../../orca_working_input/C05S10_190.inp
:language: orca
```

输出包含 Morse 拟合的结果：

```orca
Morse-Fit Results:
 Re               =   0.93014 Angstroem
 we               =   4111.2 cm**-1
 wexe             =     79.5 cm**-1
```

可以与用相同基组计算的 CCSD(T) 值比较：

```orca
Morse-Fit Results:
 Re               =   0.92246 Angstroem
 we               =   4209.8 cm**-1
 wexe             =     97.6 cm**-1
```

MRCI+Q 和 CCSD(T) 结果之间的一致性相当好。

(sec:modelchemistries.mrci.multiref)=
## 多参考体系——臭氧

臭氧分子由于其双自由基特征是一个相当经典的多参考体系。让我们看看三个最高占据和最低未占据 MO（下一个占据 MO 能量低约 6 eV，下一个虚 MO 能量高约 10 eV）：

(fig:FrontierMO_Ozone)=
:::{subfigure} ABCD
:subcaptions: below
:class-grid: outline

![(a) MO-9](../../images/617.*)
![(b) MO-10](../../images/618.*)
![(c) MO 11(HOMO)](../../images/619.*)
![(d) MO 12(LUMO)](../../images/620.*)

臭氧分子的前沿 MO。

:::

这些 MO 是两个能量较高的 $\sigma$ 孤对，然后是氧 $\pi$ 孤对的对称和反对称组合。特别是 LUMO 位置很低，将导致强相关效应，因为 (HOMO)$^{2} \to $ (LUMO)$^{2}$ 激发将以大系数出现。从物理上讲，这证明了该分子的双自由基特征很大，大致由结构 $\uparrow$O-O-O$\downarrow$ 表示。因此，正确处理该分子的最小活性空间是包含 HOMO 和 LUMO 的 CAS(2,2) 空间。我们通过查看沿 O--O 键长和 O-O-O 角的二维势能面的 RHF、MP2、MRACPF 计算来说明（实验值为 1.2717 Å 和 116.78${^\circ}$）。

```{literalinclude} ../../orca_working_input/C05S10_193.inp
:language: orca
```

由于需要 441 次能量求值，这是一个稍长的计算。RHF 在所检查的几何范围内没有找到任何有意义的极小值。MP2 好得多，接近所需的极小值，但将 O--O 距离低估了约 0.03 Å。CCSD(T) 给出非常好的角度但 O--O 距离太长。事实上，在这些计算中最大的双激发振幅是 $\approx$ 0.2（HOMO--LUMO 双激发），这表明是近简并计算，即使 CCSD(T) 也难以处理。CAS(2,2) 计算已经与实验定性一致，MRCI$+$Q 计算则给出几乎完美的吻合。

CCSD(T) 和 MRCI$+$Q 势能面的差异表明 CCSD(T) 比 MRCI$+$Q 略低，说明它处理了更多的相关。然而 CCSD(T) 的处理是不平衡的。MRCI 计算在 HOMO-LUMO 双激发之上采用单激发和双激发，这产生了显然在平衡 MR 计算中起重要作用的三重和四重激发。这些激发在 MRCI 计算中被显式地处理到所有阶，但在耦合簇方法中只是近似地处理（四重激发作为同时对激发，三重激发作为微扰）。因此，尽管理论在电子结构困难的情况下具有相当的鲁棒性，它不适用于真正的多参考问题。

尽管使用的基组太小，这是一个很好的结果，表明用具有物理合理活性空间（即使是 $2 \times 2$）的多参考处理对于获得定性和定量正确的结果是多么重要。

(fig:2Dpotenergysurface_ozone)=
:::{subfigure} ABCDEF
:subcaptions: below
:class-grid: outline

![(a) RHF](../../images/621.*)
![(b)  CASSCF(2,2)](../../images/622.*)
![(c) MP2](../../images/623.*)
![(d) CCSD(T)](../../images/624.*)
![(e) MRCI+Q](../../images/625.*)
![(f) Difference CCSD(T)/MRCI+Q](../../images/626.*)

用不同方法计算的 $ O_3 $ 分子的二维势能面

:::

(sec:modelchemistries.mrci.size)=
## 尺寸一致性

最后，我们想研究方法的尺寸一致性误差。为此我们在单参考水平研究两个无相互作用的 HF 分子并与单个 HF 分子的能量比较。这应该给出每种方法典型表现的合理认识（能量以 Eh 为单位）[^5]：

```orca
E(HF)         E(HF+HF)  |Difference|
  CISD+Q   -100.138 475  -200.273 599     0.00335
  ACPF     -100.137 050  -200.274 010     0.00000
  ACPF2    -100.136 913  -200.273 823     0.00000
  AQCC     -100.135 059  -200.269 792     0.00032
```

结果大致如预期——CISD+Q 有相对较大的误差，ACPF 和 ACPF/2 对这类例子是完美的；AQCC 不期望是尺寸一致的，在这方面（只）比 CISD+Q 好约 10 倍。CEPA-0 也是尺寸一致的。

(sec:modelchemistries.mrci.mrmp2)=
## 较大分子的高效 MR-MP2 计算

非收缩 MR-MP2 方法如今已过时。它们比内收缩方法（例如第 {ref}`sec:modelchemistries.nevpt2` 节描述的 NEVPT2 方法）昂贵得多。此外，MR-MP2 容易出现侵入态，这是实际应用的主要障碍。由于历史原因，本节介绍自 ORCA 2.7.0 版本起可用的传统 MR-MP2 方法。该实现避免了 MR-MP2 的完整积分变换，在时间和内存方面带来显著节省。因此，相对较大的 RI-MR-MP2 计算可以相当高效地完成。然而，程序仍使用非收缩的一阶波函数，这意味着对于非常大的参考空间，计算仍然变得不可行。

例如考虑二苯乙烯分子绕中心双键的旋转

(fig:stillbene_rotation)=
:::{subfigure} AB
:subcaptions: below
:class-grid: outline

![(a) ](../../images/627.*)
![(b)  ](../../images/628.*)

用 CASSCF(2,2) 参考和 MR-MP2 关联参考计算的二苯乙烯绕中心双键的旋转。

:::

该计算的输入如下所示。计算有超过 500 个基函数，每步（CASSCF-MR-MP2）仍在不到一小时内完成。程序处理相对于母体 MRCI 方法减少的双电子积分数，因此也可以应用于较大的分子。注意我们使用了 "JK" 拟合基组以足够精度同时拟合 Coulomb 和动态相关贡献。因此，这个例子表明对于不太大的参考空间，MR-MP2 计算可以用 ORCA 高效完成（一个小细节：计算从 90 度二面角开始，以确保正确的两个轨道在活性空间中，即在共面结构中构成 pi 键的中心碳 p 轨道）。

```orcainput
#
# Stilbene rotation using MRMP2
#
! def2-TZVP def2/JK RIJCOSX RI-MRMP2

%casscf nel            2
        norb           2
        end

%mrci   maxmemint 2000
        tsel 1e-8
        end


%paras  DIHED = 90,270, 19
        end

* int 0 1
 C     0   0   0   0.000000     0.000     0.000
 C     1   0   0   1.343827     0.000     0.000
 C     2   1   0   1.490606   125.126     0.000
 C     1   2   3   1.489535   125.829   \{DIHED\}
 C     4   1   2   1.400473   118.696   180.000
 C     4   1   2   1.400488   122.999     0.000
 C     6   4   1   1.395945   120.752   180.000
 C     5   4   1   1.394580   121.061   180.000
 C     8   5   4   1.392286   120.004     0.000
 C     3   2   1   1.400587   118.959   180.000
 C     3   2   1   1.401106   122.779     0.000
 C    11   3   2   1.395422   120.840   180.001
 C    12  11   3   1.392546   120.181     0.000
 C    13  12  11   1.392464   119.663     0.000
 H     1   2   3   1.099419   118.266     0.000
 H     2   1   3   1.100264   118.477   179.999
 H     5   4   1   1.102119   119.965     0.000
 H     6   4   1   1.100393   121.065     0.000
 H     7   6   4   1.102835   119.956   180.000
 H     8   5   4   1.102774   119.989   180.000
 H     9   8   5   1.102847   120.145   180.000
 H    10   3   2   1.102271   120.003     0.000
 H    11   3   2   1.100185   121.130     0.000
 H    12  11   3   1.103001   119.889   180.000
 H    13  12  11   1.102704   120.113   180.000
 H    14  13  12   1.102746   119.941   180.000
*
```


(sec:modelchemistries.mrci.soc)=
## 使用 SOC 子模块计算性质

(sec:modelchemistries.mrci.soc.zfs)=
### 零场分裂
```{index} Zero-Field Splitting with MRCI
```

自旋-轨道耦合（SOC）和自旋-自旋耦合（SSC）对零场分裂（ZFS）的贡献可以用来自多组态计算（如 CASSCF、MRCI 或 MRPT 等多参考类型）的波函数非常精确地计算，如 QDPT 磁性质节 {ref}`sec:spectroscopyproperties.qdpt_magnetic_properties` 所述。

```orca
# In case that you want to run QDPT-SOC calculation with manually adjusted
# diagonal energies you can copy the following part into the %mrci soc
# block and modify it as needed (energies are given in wavenumbers relative
# to the lowest state).                                  
#                                                                                                    
# NOTE: It is YOUR responsibility to make sure that the CAS-CI state that
#       you may want to dress with these energies correlates properly with
#       the energies printed here. The order of states or even the identity
#       of states may change with and without inclusion of dynamic
#       correlation. In the case that dynamic correlation strongly mixes,
#       different CAS-CI states there may not even be a proper correlation!       
#                                                                                                    
     EDiag[  0]    -149.526236244  # root   0 of block 0                                             
     EDiag[  1]    -149.359818263  # root   1 of block 0                                             
     EDiag[  2]    -149.359818263  # root   2 of block 0                                             
     EDiag[  3]    -149.496737695  # root   0 of block 1                                             
     EDiag[  4]    -149.496737695  # root   1 of block 1                                             
     EDiag[  5]    -149.474844108  # root   2 of block 1                                             
```

这些跃迁能可以用输入文件中提供的更精确的能量替代，如下：

```orca
%soc
dosoc true
dossc true
     EDiag[  0]    -149.526236244  # root   0 of block 0
     EDiag[  1]    -149.359818263  # root   1 of block 0
     EDiag[  2]    -149.359818263  # root   2 of block 0
     EDiag[  3]    -149.496737695  # root   0 of block 1
     EDiag[  4]    -149.496737695  # root   1 of block 1
     EDiag[  5]    -149.474844108  # root   2 of block 1
end
```

精确的对角能量通常能提高 SOC 和 SSC 分裂的精度。

(sec:modelchemistries.mrci.soc.lzfs)=
### 局域零场分裂

该子模块也可用于计算原子中心的局域 ZFS 分裂参数。该方法称为局域完全活性空间组态相互作用（L-CASCI），可用于将总 ZFS 张量的 SOC 部分分离为原子贡献。其原理和更多细节在原始出版物 {cite}`retegan_first-principles_2014` 中描述；下面仅列出重现其中二聚体配合物计算所需的步骤。

1\. 第一步是获得将在组态相互作用（CI）过程中使用的分子轨道。一组好的轨道可以从限制开壳层自旋平均 Hartree-Fock（SAHF）计算获得。输入的相关部分如下：

```orca
! def2-TZVP

% scf
    hftyp rohf
    rohf_case sahf
    rohf_numop 2
    rohf_nel[1] 9
    rohf_norb[1] 10
    end
```
