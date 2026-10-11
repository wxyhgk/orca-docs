```{index} 全组态相互作用 (Full-CI), FCI
```

(sec:modelchemistries.dcdcas.fci.fci)=
# 全组态相互作用（Full Configuration Interaction）

ORCA 提供了若干精确和近似方法来处理全组态相互作用（full configuration
interaction，FCI）问题。这些方法可通过 CASSCF 模块（见 {ref}`sec:modelchemistries.casscf` 一节）
或 ICE 模块（见 {ref}`sec:modelchemistries.iceci` 一节）来使用。

下面我们用 CASSCF 模块计算氢化锂（lithium hydride）分子的 FCI 能量，
典型的输入需要声明一个活性空间（active space）。活性空间定义了以 FCI
拟设（ansatz）处理的活性电子数与活性轨道数。在所有电子和轨道都以 FCI
拟设处理的特殊情况下，我们可以在 `%CASSCF` 块中使用关键词 `DoFCI`，
让程序相应地设定活性空间。在此示例中，我们关注单重态基态。
注意，任意多重度的激发态都可以通过关键词 `Mult` 和 `NRoots` 来计算。
FCI 方法对轨道旋转不变，因此 CASSCF 模块中会跳过轨道优化。
尽管如此，采用一组有意义的轨道（例如来自收敛的 Hartree-Fock 计算的轨道）
以减少 FCI 迭代次数仍然很重要。

```orcainput
# Hartree-Fock orbitals
!def2-tzvp RHF

*xyz 0 1
  Li 0 0 0
  H  0 0 1.597
*
```

Hartree-Fock 计算的输出还会报告体系中电子和轨道的总数（见下面的片段）。

```orca
Number of Electrons    NEL             ....    4
Basis Dimension        Dim             ....   20
```

在给定示例中，20 个轨道中有 4 个电子，即 "CAS(4,20)"。读入收敛的 RHF 轨道后，
即可启动 FCI 计算。

```orcainput
!def2-tzvp extremescf

!moread
%moinp "RHF.gbw"

%maxcore 2000

%casscf
  DoFCI true # sets NEL 4 and NORB 20 in this example.
end

*xyz  0 1
  Li 0 0 0
  H  0 0 1.597
*
```

输出会报告详细的 CI 设置、组态状态函数（configuration state function，CSF）
的数目以及 CI 收敛阈值。

```orca
CI-STEP:
  CI strategy                         ... General CI
  Number of multiplicity blocks       ...    1
  BLOCK  1 WEIGHT=   1.0000
  Multiplicity                      ...    1
  #(Configurations)                 ... 8455
  #(CSFs)                           ... 13300
  #(Roots)                          ...    1
  ROOT=0 WEIGHT=    1.000000
  
  PrintLevel                        ...    1
  N(GuessMat)                       ...       512
  MaxDim(CI)                        ...        10
  MaxIter(CI)                       ...        64
  Energy Tolerance CI               ...  1.00e-13
  Residual Tolerance CI             ...  1.00e-13
  Shift(CI)                         ...  1.00e-04
  ...
```

随后程序会打印实际的 CI 迭代过程、最终能量，以及用组态（configuration，CFG）
表示的波函数组成。

```orca
------------------
CAS-SCF ITERATIONS
------------------
  
  
  MACRO-ITERATION   1:
  --- Inactive Energy E0 = 0.99407115 Eh
  --- All densities will be recomputed
  CI-ITERATION   0:
  -8.012799617   0.526896429727 (    0.25)
  CI-ITERATION   1:
  -8.047996328   0.001601312242 (    0.25)
  CI-ITERATION   2:
  -8.048134967   0.000022625293 (    0.25)
  CI-ITERATION   3:
  -8.048137773   0.000000462227 (    0.25)
  CI-ITERATION   4:
  -8.048137841   0.000000035496 (    0.25)
  CI-ITERATION   5:
  -8.048137845   0.000000001357 (    0.25)
  CI-ITERATION   6:
  -8.048137845   0.000000000254 (    0.25)
  CI-ITERATION   7:
  -8.048137845   0.000000000006 (    0.25)
  CI-ITERATION   8:
  -8.048137845   0.000000000001 (    0.25)
  CI-ITERATION   9:
  -8.048137845   0.000000000000 (    0.25)
  CI-PROBLEM SOLVED
  DENSITIES MADE
  
  <<<<<<<<<<<<<<<<<<INITIAL CI STATE CHECK>>>>>>>>>>>>>>>>>>
  
  BLOCK  1 MULT= 1 NROOTS= 1
  ROOT   0:  E=      -8.0481378449 Eh
  0.97242 [     0]: 22000000000000000000
  0.00296 [    99]: 20000002000000000000
  0.00258 [    89]: 20000010001000000000
  0.00252 [    85]: 20000020000000000000
```

除能量外，CASSCF 模块还提供若干性质（g 张量、零场分裂（ZFS）等），
详见 {ref}`sec:modelchemistries.casscf.properties` 一节。

FCI 问题的精确解标度非常陡峭，因此仅限于较小的问题（最多 16 个电子
在 16 个轨道中的活性空间）。更大的体系可通过近似解来处理，
例如密度矩阵重整化群（density matrix renormalization group，DMRG）方法
（见 {ref}`sec:modelchemistries.dmrg` 一节），或迭代组态展开
（iterative configuration expansion，ICE）方法（见 {ref}`sec:modelchemistries.iceci` 一节）。
为了作一比较，我们再用 ICE-CI 拟设重复该计算，它提供了一种更传统的途径
来获得近似的全 CI 结果。

```orcainput
!def2-TZVP ExtremeSCF

!moread
%moinp "RHF.gbw"

%maxcore 2000

%ice
  Nel 4
  Norb 20
end

*xyz  0 1
  Li 0 0 0
  H  0 0 1.597
*
```

控制精度最重要的单一参数是 `TGen`。它与更精细的设置一并打印在输出中。
我们顺带指出，波函数展开及其截断可以在 CSF、组态或行列式（determinant）的
基组下进行。Chilkuri 等人{cite}`chilkuri_ice1,chilkuri_ice2` 详细讨论了这些不同的策略。

```orca
ICE-CI:
  General Strategy                 ... CONFIGURATIONS (all CSFs to a given CFG, spin adapted)
  Max. no of macroiterations       ...   12
  Variational selection threshold  ... -1.000e-07
  negative! => TVar will be set to 1.000e-07*Tgen=1.000e-11
  Generator selection threshold    ... 1.000e-04
  Excitation level                 ... 2
  Selection on initial CSF list    ... YES
  Selection on later CSFs lists    ... YES
  
  ...
  
******************************
*  ICECI MACROITERATION   3  *
******************************

# of active configurations =   2808
Initializing the CI            ...  (CI/Run=3,2 UseCC=0)done (  0.0 sec)
Building coupling coefficients ... (CI/Run=3,2)Calling BuildCouplings_RI UseCCLib=0 DoRISX=0
CI_BuildCouplings NCFG= 2808 NORB=20 NEL=4 UseCCLib=0 MaxCore=2000
PASS 1 completed. NCFG= 2808 NCFGK= 8416 MaxNSOMOI=4 MaxNSOMOK=4
PASS 2 completed.
PASS 3 completed.
Memory used for RI tree              =    2.99 MB (av. dim=    35)
Memory used for ONE tree             =    1.32 MB (av. dim=    46)
Memory used for coupling coefficients=    0.01 MB
done (    0 sec)
Now calling CI solver (4095 CSFs)

****Iteration    0****
Maximum residual norm  :     0.000293130557

****Iteration    1****
Maximum residual norm  :     0.000000565920

****Iteration    2****
Maximum residual norm  :     0.000001755176

****Iteration    3****
Maximum residual norm  :     0.000000435942
Rebuilding the expansion space

****Iteration    4****

*** CONVERGENCE OF ENERGIES REACHED ***
CI problem solved in   0.4 sec

CI SOLUTION :
STATE   0 MULT= 1: E=     -8.0481340246 Eh W=  1.0000 DE= 0.000 eV      0.0 cm**-1
0.97249  : 22000000000000000000
Selecting new configurations         ... (CI/Run=3,2)done (  0.0 sec)
# of selected configurations          ...   2747
# of generator configurations         ...     43 (NEW=1 (CREF=43))
Performing single and double excitations relative to generators ... done (0.0 sec)
# of configurations after S+D         ...   7038
Selecting from the generated configurations  ... done (  0.1 sec)
# of configurations after Selection  ...   2808
Root   0:     -8.048134025       -0.000000023      -8.048134048
==>>> CI space seems to have converged. No new configurations
maximum energy change                ... 1.727e-05 Eh

               ********* ICECI IS CONVERGED *********
  Initializing the CI            ...  (CI/Run=3,3 UseCC=0)done (  0.0 sec)
  Building coupling coefficients ... (CI/Run=3,3)Calling BuildCouplings_RI UseCCLib=0 DoRISX=
  CI_BuildCouplings NCFG= 2808 NORB=20 NEL=4 UseCCLib=0 MaxCore=2000
  PASS 1 completed. NCFG= 2808 NCFGK= 8416 MaxNSOMOI=4 MaxNSOMOK=4
  PASS 2 completed.
  PASS 3 completed.
  Memory used for RI tree              =    2.99 MB (av. dim=    35)
  Memory used for ONE tree             =    1.32 MB (av. dim=    46)
  Memory used for coupling coefficients=    0.01 MB
  done (    0 sec)
  Now calling CI solver (4095 CSFs)
  
  ****Iteration    0****
  Maximum residual norm  :     0.000000471011
  
  ****Iteration    1****
  
  *** CONVERGENCE OF ENERGIES REACHED ***
  CI problem solved in   0.1 sec
  
  CI SOLUTION :
  STATE   0 MULT= 1: E=     -8.0481340245 Eh W=  1.0000 DE= 0.000 eV      0.0 cm**-1
  0.97249  : 22000000000000000000
```

在使用 Hartree-Fock 轨道和默认设置时，ICE 在 3 次宏迭代（macro iteration）内
收敛到能量 $-8.048134047513~E_\text{h}$。在此示例中，与精确解的偏差仅为
$3.8 \times 10^{-6}~E_\text{h}$。

