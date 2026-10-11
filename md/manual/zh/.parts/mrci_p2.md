                       ****Iteration    4****
   Size of expansion space: 4
   Lowest Energy          :  -114.086074300143
   Maximum Energy change  :     0.000031026018 (vector 0)
   Maximum residual norm  :     0.000004959126
   Rebuilding the expansion space

                       ****Iteration    5****
   Size of expansion space: 2
   Lowest Energy          :  -114.086076038587
   Maximum Energy change  :     0.000001738444 (vector 0)
   Maximum residual norm  :     0.000000572348

      *** CONVERGENCE OF RESIDUAL NORM REACHED ***

Storing the converged CI vectors               ... test1.mrci.vec

                 *** DAVIDSON DONE ***
Returned from DIAG section
```

该过程同时收敛所有根，在六次迭代后完成，这是合理的。现在程序计算
Davidson 校正（`DavidsonOpt`），为每个根打印。

```orca
Davidson type correction:
Root= 0 W=   0.912 E0=  -113.778810014 ECI=  -114.086076039 DE=-0.026913
```

即使在这个小例子中，校正也相当大，基态约 27 mEh
（激发态约 $\approx 36$ mEh，稍后在输出中）。因此，对跃迁能得到 $\approx 9$ mEh = 0.25 eV 的贡献，这无疑是显著的。
不幸的是，当参考空间权重下降或关联电子数变大时，校正变得不可靠。这里
0.912 和 0.888 仍然可以，体系足够小，可以期望
Davidson 校正给出好结果。

下一步是估计未选中组态的校正：

```orca
Unselected CSF estimate:
Full relaxed MR-MP2 calculation           ...

Selection will be done from 1 spatial configurations
Selection will make use of spatial symmetry
Selection will make use of spatial symmetry
Selection will make use of spatial symmetry
done
Selected MR-MP2 energies                  ...

 Root=  0  E(unsel)=     -0.000106931
```

在当前情况下这低于 1 mEh，对所有三个态也非常相似，因此对跃迁能不重要。

```orca
----------
CI-RESULTS
----------

The threshold for printing is  0.30 percent
The weights of configurations will be printed. The weights are summed over
all CSFs that belong to a given configuration before printing

STATE   0:  Energy=   -114.113096211 Eh RefWeight=  0.9124  0.00 eV      0.0 cm**-1
      0.9124  : h---h---[20]
      0.0114  : h  6h  6[22]
```

最终基态能量是 `-114.113096211`，这是该基组下完全 CI 能量的估计。
领头组态仍然是权重约 91% 的闭壳层组态。
然而，参考空间*之外*的双激发贡献了约 1%。这是激发 MO6,MO6 $\to$LUMO,LUMO。这表明一旦 MO6 也被包含在参考空间中（这是 HOMO-1），预计会有更精确的结果。激发态由
HOMO-LUMO 跃迁主导（如所期望的），但最终 CI 向量中也出现了其他一些单激发和双激发。

现在所有 CI 向量已知，我们可以按能量递增排序并打印（垂直）跃迁能：

```orca
-------------------
TRANSITION ENERGIES
-------------------

The lowest energy is   -114.113096211 Eh

State Mult Irrep Root Block    mEh          eV      1/cm
  0    1    A1    0    0      0.000      0.000       0.0
  1    3    A2    0    2    134.086      3.649   29428.4
  2    1    A2    0    1    148.499      4.041   32591.8
```

这个结果已经相当不错，跃迁能
在其气相实验值（$\approx 3.50$ 和 $\approx 4.00$ eV）的 $\approx 0.1$ eV 以内，可以与 CIS
值 3.8 和 4.6 eV 相比，后者误差相当大。

下一步求值密度和跃迁密度并计算吸收和 CD 光谱（在偶极长度
形式中）以及自旋允许跃迁的态偶极
矩：

```orca
----------------------------------------------------------------------------------------------------
                     ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS
----------------------------------------------------------------------------------------------------
     Transition      Energy     Energy  Wavelength fosc(D2)      D2        DX        DY        DZ
                      (eV)      (cm-1)    (nm)                 (au**2)    (au)      (au)      (au)
----------------------------------------------------------------------------------------------------
  0-1A1 ->  0-1A2   4.040866   32591.8   306.8   0.000000000   0.00000  -0.00000   0.00000   0.00000

------------------------------------------------------------------------------------------
                     CD SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS
------------------------------------------------------------------------------------------
     Transition      Energy     Energy  Wavelength    R        MX        MY        MZ
                      (eV)      (cm-1)    (nm)   (1e40*cgs)   (au)      (au)      (au)
------------------------------------------------------------------------------------------
  0-1A1 ->  0-1A2   4.040866   32591.8   306.8   -0.00000  -0.00000  -0.00000   0.59348


------------------------------------------------------------------------------
                             STATE DIPOLE MOMENTS
------------------------------------------------------------------------------
  Root  Block           TX        TY        TZ           |T|
                      (Debye)   (Debye)   (Debye)      (Debye)
------------------------------------------------------------------------------
    0    0            0.00000  -0.00000   2.33244      2.33244
    0    2            0.00000  -0.00000   1.45831      1.45831
    0    1            0.00000  -0.00000   1.58658      1.58658
```

这里跃迁是对称禁阻的，因此没有
振子强度。基态的态偶极矩是
2.33 Debye，比 SCF 计算的 2.87 Debye 略低。因此，相关效应降低了极性，与如下解释一致：键的离子性（HF 理论总是高估它）被相关所降低。
最后，您还会得到每个生成态密度的详细布居分析，可以与输出前面部分相应的 SCF 分析比较。

关于 MR-CI 模块使用的初始示例到此结束。该模块在磁盘上留下若干文件，大部分目前还不需要，但将来将允许更多分析和重启等。`.ivo` 文件是标准 `.gbw` 类型文件，其中的轨道可用于可视化。这对于弄清
生成的 IVO 的身份很重要。也许它们不是您想要的，那么您需要用 IVO 作为输入、`NoIter`
并在新运行中关闭 IVO 功能重新运行 MR-CI！我们可以用 IVO 作为
态平均 CASSCF 计算的输入：

```orca
! moread UseSym KDIIS
%moinp "Test-SYM-MRCI-H2CO.ivo"

%casscf nel    2
        norb   2
        irrep  0,1,1
        mult   1,1,3
        nroots 1,1,1
        end
```

如果我们基于这个参考空间进行 MR-ACPF 计算，会发现
计算的跃迁能略差于 MRCI+Q 计算。这是近似簇型方法的典型情况，通常需要稍大的参考空间才能获得精确结果。SORCI 得到类似结果。

```orca
%mrci  CIType          SORCI
        tsel             1e-6
        tpre             1e-4
        tnat             1e-5
        AllSingles       true
        doNatOrbs        true
        IntMode     FullTrafo
        # ground state 1A1
        NewBlock 1 0
          NRoots 1
          Excitations cisd
          Refs CAS(2,2) end
          End
        # HOMO LUMO transition 1A2
        NewBlock 1 1
          NRoots 1
          Excitations cisd
          Refs CAS(2,2) end
          End
        # HOMO LUMO triplet transition 3A2
        NewBlock 3 1
          NRoots 1
          Excitations cisd
          Refs CAS(2,2) end
          End
end
```

结果是：

```orca
State Mult Irrep Root Block    mEh          eV      1/cm
  0    1    A1    0    0      0.000      0.000       0.0
  1    3    A2    0    2    144.563      3.934   31728.0
  2    1    A2    0    1    161.179      4.386   35374.7
```

这系统性地偏高 0.4 eV。但让我们看看
近似平均自然轨道（AANOs）占据数：

```orca
------------------------
AVERAGE NATURAL ORBITALS
------------------------

Trace of the density to be diagonalized = 12.000000
Sum of eigenvalues = 12.000000
Natural Orbital Occupation Numbers:
N[  2] ( A1)=   1.99831062
N[  3] ( A1)=   1.99761604
N[  4] ( A1)=   1.99479313
N[  5] ( B1)=   1.99016881
N[  6] ( B2)=   1.95818285
N[  7] ( B1)=   1.33014178
N[  8] ( B2)=   0.70688423
N[  9] ( B1)=   0.00988561
N[ 10] ( A1)=   0.00436843
```

这表明有一个低占据轨道（MO6）不在参考空间中。因此，我们再试同样的计算，但现在多一个活性轨道和两个活性电子：

```orca
! moread
%moinp "Test-SYM-MRCI-H2CO.gbw"

%casscf nel 4
        norb 3
        irrep  0,1,1
        mult   1,1,3
        nroots 1,1,1
        end

%mrci CIType          SORCI
      tsel             1e-6
      tpre             1e-4
      tnat             1e-5
      AllSingles       true
      doNatOrbs        true
      IntMode     FullTrafo
      # ground state 1A1
      NewBlock 1 0
        NRoots 1
        Excitations cisd
        Refs CAS(4,3) end
        End
      # HOMO LUMO transition 1A2
      NewBlock 1 1
        NRoots 1
        Excitations cisd
        Refs CAS(4,3) end
        End
      # HOMO LUMO triplet transition 3A2
      NewBlock 3 1
        NRoots 1
        Excitations cisd
        Refs CAS(4,3) end
        End
end
```

结果是：

```orca
State Mult Irrep Root Block    mEh          eV      1/cm
  0    1    A1    0    0      0.000      0.000       0.0
  1    3    A2    0    2    145.494      3.959   31932.3
  2    1    A2    0    1    162.222      4.414   35603.6
```

现在结果很好了，因为所有 essential physics 都在参考空间中。检查占据数表明不再有可疑的轨道。请注意，这仍然比 MRCI+Q 紧凑得多。

同样，用扩展的参考空间我们从 MRACPF 得到精确结果。

```orca
State Mult Irrep Root Block    mEh          eV      1/cm
  0    1    A1    0    0      0.000      0.000       0.0
  1    3    A2    0    2    134.985      3.673   29625.8
  2    1    A2    0    1    148.330      4.036   32554.6
```

然而，SORCI 计算*更*紧凑。对于较大的分子，差异变得越来越明显，SORCI 或甚至 MRDDCI2（带或不带 +Q）可能是唯一可行的方法——如果还有可能的话。

(sec:modelchemistries.mrci.exitationenergy)=
## 不同多重度之间的激发能

作为一个相对精确的 MRCI+Q 计算的例子，考虑以下任务，计算 O$_{2}$ 的三重态基态和第一激发单重态。

```{literalinclude} ../../orca_working_input/C05S10_174.inp
:language: orca
```

注意线性分子在 D$_{2h}$ 下运行。这产生一个小问题，因为 CASSCF 过程必然破坏 $^{1}\Delta$ 态的对称性。

```orca
LOWEST ROOT (ROOT 0, MULT 3, IRREP B1g) =   -149.765383866 Eh -4075.323 eV

STATE   ROOT MULT IRREP DE/a.u.    DE/eV    DE/cm**-1
   1:    0    1  B1g   0.033334     0.907   7316.0
   2:    0    1   Ag   0.033650     0.916   7385.3
   3:    1    1   Ag   0.062381     1.697  13691.1
```

MRCI+Q 的结果是：

```orca
-------------------
TRANSITION ENERGIES
-------------------

The lowest energy is   -150.176905551 Eh

State Mult Irrep Root Block    mEh          eV      1/cm
  0    3   B1g    0    0      0.000      0.000       0.0
  1    1   B1g    0    2     36.971      1.006    8114.2
  2    1    Ag    0    1     38.021      1.035    8344.7
  3    1    Ag    1    1     62.765      1.708   13775.2
```

这些激发能精确到几百个波数以内。注意简并 $^{1}\Delta$ 态中约 $\approx 200$ 波数的分裂是由于 CAS 的对称性破缺和个别选择造成的。用 MP2 自然轨道重复计算给出几乎无法区分的结果，基态能量甚至比用 CASSCF 轨道得到的还低。因此，这样的自然轨道（通常更容易获得）是 CASSCF 轨道的良好替代品，同时由于使用对称性造成的对称性破缺似乎难以避免。

```orca
-------------------
TRANSITION ENERGIES
-------------------

The lowest energy is   -150.177743426 Eh

State Mult Irrep Root Block    mEh          eV      1/cm
  0    3   B1g    0    0      0.000      0.000       0.0
  1    1   B1g    0    2     37.369      1.017    8201.5
  2    1    Ag    0    1     38.237      1.040    8392.1
  3    1    Ag    1    1     62.731      1.707   13767.9
```

(sec:modelchemistries.mrci.correlationenergy)=
## 相关能

我们遵循的逻辑如下：CID 减 SCF 给出双激发的效应；到 CISD 给出单激发的效应；QCISD(=CCD) 减 CID 给出非连通四重激发的效应。QCISD 减 QCID 同时给出单激发和非连通三重激发的效应。它们有点难以分离，但如果只看单激发并与单激发 + 非连通三重激发比较，可能得到不错的估计。
最后，QCISD(T) 减 QCISD 给出连通三重激发的效应。
当然也可以用 CCSD 代替 QCISD，但我觉得 T$_{1}$ 的高次幂使图景稍微模糊了——当然这可以讨论。

首先是 H$_2$O/TZVPP 在其 MP2/TZVPP 平衡几何下
（$T_{\text{pre}} \hspace{0.5mm} = \hspace{0.5mm} 10^{-6}$ 和
$T_{\text{sel} } \hspace{0.5mm} = \hspace{0.5mm} 10^{-9}$ Eh 用于 MRCI 和 MRACPF 计算）：

| [**激发类**]{style="color: white"} | [**能量（Eh）**]{style="color: white"} | [**能量差（mEh）**]{style="color: white"} |
|:----------------------------------------------|:----------------------------------------:|:-----------------------------------------------:|
| 无 (RHF)                                      |                 -76.0624                 |                                                 |
| 双激发 (CID)                                  |                 -76.3174                 |                       255                       |
| +单激发 (CISD)                                |                 -76.3186                 |                        1                        |
| +非连通四重激发 (QCID)                        |                 -76.3282                 |                       11                        |
| +非连通三重激发 (QCISD)                       |                 -76.3298                 |                        2                        |
| +连通三重激发 (QCISD(T))                      |               **-76.3372**               |                        7                        |
| CASSCF(8,6)                                   |                 -76.1160                 |                                                 |
| CASSCF(8,6) + MRCI                            |                 -76.3264                 |                       210                       |
| CASSCF(8,6) + MRCI+Q                          |               **-76.3359**               |                       10                        |
| CASSCF(8,6) + MRACPF                          |               **-76.3341**               |                       218                       |

可以观察到单参考和多参考方法之间相当好的一致。特别是非连通三重激发和单激发的贡献非常小。非连通四重激发的估计从多参考 Davidson 校正或 ACPF 都相当好，CCSD(T) 与这些 MR 方法之间的一致在总能量上是 2-3 mEh，大致在化学精度以内。

为了也有一个开壳层分子，让我们看 N-H 距离为 1.0 Å 用 TZVPP 基组的 NH。

| [**激发类**]{style="color: white"} | [**能量（Eh）**]{style="color: white"} | [**能量差（mEh）**]{style="color: white"} |
|:----------------------------------------------|:----------------------------------------:|:-----------------------------------------------:|
| 无 (UHF)                                      |                 -54.9835                 |                                                 |
| 双激发 (CID)                                  |                 -55.1333                 |                       150                       |
| +单激发 (CISD)                                |                 -55.1344                 |                        1                        |
| +非连通四重激发 (QCID)                        |                 -55.1366                 |                        3                        |
| +非连通三重激发 (QCISD)                       |                 -55.1378                 |                        1                        |
| +连通三重激发 (QCISD(T))                      |               **-55.1414**               |                        4                        |
| CASSCF(6,5)                                   |                 -55.0004                 |                                                 |
| CASSCF(6,5) + MRCI                            |                 -55.1373                 |                       137                       |
| CASSCF(6,5) + MRCI+Q                          |               **-55.1429**               |                        6                        |
| CASSCF(6,5) + MRACPF                          |               **-55.1413**               |                       141                       |

同样，一致性相当好，表明单参考和多参考方法都收敛到相同的极限。

(sec:modelchemistries.mrci.thresholds)=
## 阈值

现在我们选择 CO 分子（1.128 Å）用 SVP 基组，研究结果对选择阈值的收敛性。与高水平单参考方法的比较是可行的（SCF 能量是 `-112.645 946 Eh`）。

(sec:modelchemistries.mrci.thresholds.reference)=
### 总能量的参考值

单参考值是：

```orca
BD: -112.938 48002
              CCSD: -112.939 79145
             QCISD: -112.941 95700
             BD(T): -112.950 17278
           CCSD(T): -112.950 63889
          QCISD(T): -112.951 37425
         MP4(SDTQ): -112.954 80113
```

不含连通三重激发的计算（BD、CCSD、QCISD）大约是不显式考虑三重激发所能达到的最好结果。CCSD 在这类中可能是最好的。一旦包含连通三重激发，CCSD(T)、QCISD(T) 和 BD(T) 值就接近了，根据经验它们也接近完全 CI 值，后者预计在 --112.950 到 --112.952 Eh 之间。

(sec:modelchemistries.mrci.thresholds.convsingle)=
### 单参考方法对 T$_{\text{sel} }$ 的收敛性

接下来研究这些单参考方法如何随 T$_{\text{sel} }$ 收敛：

```orca
Closed-Shell ACPF:
   Tsel        Energy      (NCSF)    Energy       (NCSF)
   (Eh)       AllSingles=true      AllSingles=false
  TSel=0      -112.943 387 (5671)
  TSel=1e-14  -112.943 387 (2543)  -112.943 387 (2478)
  TSel=1e-10  -112.943 387 (2543)  -112.941 023 (2453)
  TSel=1e-08  -112.943 387 (2451)  -112.937 087 (2346)
  TSel=1e-06  -112.943 350 (2283)  -112.937 046 (2178)
  TSel=1e-05  -112.943 176 (1660)  -112.936 821 (1555)
  TSel=1e-04  -112.944 039 ( 782)  -112.938 381 ( 677)
```

很明显，如果不自动包含单激发，收敛是不稳定的。这就是从 2.6.35 版本开始将其作为默认的原因。在当前情况下，单激发只会由于舍入误差被选中，因为根据 Brillouin 定理，单激发与基态行列式的相互作用为零。因此，对于个别选择的单参考方法，自动包含所有单激发以获得收敛结果是个好主意。替代方案是不同的单激发选择过程，但尚未开发。双激发的选择似乎能相当好地收敛总能量。可以看到选择在 10$^{-5}$ 到 10$^{-7}$ Eh 之间选择了大部分 CSF。10$^{-6}$ Eh 的阈值已经给出小于 0.1 mEh 的误差，相对于反应能等可以忽略。即使 10$^{-5}$ Eh 也给出小于 0.1 kcal/mol 的误差。

(sec:modelchemistries.mrci.thresholds.convmulti)=
### 多参考方法对 T$_{\text{pre} }$ 的收敛性

我们接下来转向多参考处理。这里我们想关联所有价轨道中的所有价电子，因此 CAS(10,8) 是合适的选择。我们首先通过使用 T$_{\text{sel} }=$10$^{-14}$ 要求 T$_{\text{pre} }$ 的收敛值，对 MRCI$+$Q 得到：

```orca
TPre = 1e-1: -112.943 964
         1e-2: -112.952 963
         1e-3: -112.953 786
         1e-4: -112.954 019
         1e-5: -112.954 336
         1e-6: -112.954 416
         1e-7: -112.954 440
```

因此，T$_{\text{pre} }=10^{-4}-10^{-6}$ 可获得相当好的收敛。因此 $10^{-4}$ 是默认值。

为了展示方便的输入，考虑以下：

```orcainput
#
# Here we calculate the CO ground state correlation energy with several methods
#
! Def2-SVP Def2-SV/C RI-MP2 CCSD(T)
%base "1"

%mp2  density relaxed
      donatorbs  true
      end

* int 0 1
 C     0   0   0   0.000000     0.000     0.000
 O     1   0   0   1.128        0.000     0.000
*

$new_job

! aug-SVP MRACPF
! moread
%moinp "1.mp2nat"
# the CASSCF is done with MP2 natural orbitals which is a good idea and
# secondly we use a large level shift in order to help convergence
%casscf nel     10
        norb     8
        mult     1
        nroots   1
        shiftup  2
        shiftdn  2
        end

%mrci   tsel 1e-8
        tpre 1e-6
        end

* int 0 1
 C     0   0   0   0.000  0.000  0.000
 O     1   0   0   1.128  0.000  0.000
*
```

这个任务同时计算下面所有内容，再次展示了相继的单参考和多参考相关方法之间的一致性

```orca
SCF          =  -112.6459
RI-MP2       =  -112.9330
CCSD         =  -112.9398
CCSD(T)      =  -112.9506
CASSCF(10,8) =  -112.7769
MRACPF       =  -112.9514
```

(sec:modelchemistries.mrci.bondbreaking)=
## 能量差——键断裂

对于能量差的计算，我们再次从参考 CCSD(T) 计算开始；这种方法是少数能在实际应用中声称化学精度的方法之一：

```orca
Reference Total Energies for N2 at 1.0977 Angstr\"{o}m with
  The SVP basis
    E(CCSD)   = -109.163 497
    E(CCSD(T))= -109.175 625
  Nitrogen Atom (4S), SVP basis, unrestricted
    E(CCSD)   =  -54.421 004
    E(CCSD(T))=  -54.421 7183
  Energy Difference:
  Delta-E(CCSD)   = -0.321 489 = 8.75 eV
  Delta-E(CCSD(T))= -0.332 188 = 9.04 eV
```

基组当然不适合与实验值的定量比较。然而，这些计算的重点不在于此，它们本质上是说明性的。SVP 基组刚好足够好，允许进行方法评估而不导致过于昂贵的计算。
