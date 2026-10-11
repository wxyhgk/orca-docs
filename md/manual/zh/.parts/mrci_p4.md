
对于当前的 Mn(II)Mn(III) 二聚体，共有 9 个电子分布在 10 个 d 轨道中。

2\. 接下来，使用实现的定域化方案之一对分子轨道进行定域化。下面是本例中使用的 `orca_loc` 输入：

```orca
sahf.gbw
sahf.loc
0
200 # first of the 10 d-orbitals
209 # last of the 10 d-orbitals
128
0.000001
0.75
0.65
2
```

3\. 随后，使用 `orca_blockf` 工具对 Fock 矩阵进行块对角化，使定域轨道成为局域正则的。

```orca
orca_blockf sahf.gbw sahf.loc 200 204 205 209
```

前两个数字定义定域在一个中心上的分子轨道范围；后两个用于第二个中心。

4\. 存储在 `sahf.loc` 文件中的重新正则化轨道随后可用于以下 MRCI 输入来计算 Mn(III) 中心局域 ZFS 的 SOC 贡献：

```orca
! ZORA-def2-TZVP def2-TZVP/C ZORA
! nomulliken noloewdin
! moread noiter allowrhf
! moread

% mrci
    citype mrci
    tsel 0
    tpre 0
    intmode ritrafo
    solver diis
    soc
        intmode ritrafo
        dosoc true
        end
    newblock 10 *
        nroots 5
        excitations none
        refs
            #  Mn(II)    Mn(III)
            {1 1 1 1 1  1 1 1 1 0}
            {1 1 1 1 1  1 1 1 0 1}
            {1 1 1 1 1  1 1 0 1 1}
            {1 1 1 1 1  1 0 1 1 1}
            {1 1 1 1 1  0 1 1 1 1}
            end
        end
    newblock 8 *
        nroots 45
        excitations none
        refs
            #  Mn(II)    Mn(III)
            {1 1 1 1 1  2 1 1 0 0}
            {1 1 1 1 1  2 1 0 1 0}
            {1 1 1 1 1  2 1 0 0 1}
            {1 1 1 1 1  2 0 1 1 0}
            {1 1 1 1 1  2 0 1 0 1}
            {1 1 1 1 1  2 0 0 1 1}
            {1 1 1 1 1  1 2 1 0 0}
            {1 1 1 1 1  1 2 0 1 0}
            {1 1 1 1 1  1 2 0 0 1}
            {1 1 1 1 1  1 1 2 0 0}
            {1 1 1 1 1  1 1 1 1 0}
            {1 1 1 1 1  1 1 1 0 1}
            {1 1 1 1 1  1 1 0 2 0}
            {1 1 1 1 1  1 1 0 1 1}
            {1 1 1 1 1  1 1 0 0 2}
            {1 1 1 1 1  1 0 2 1 0}
            {1 1 1 1 1  1 0 2 0 1}
            {1 1 1 1 1  1 0 1 2 0}
            {1 1 1 1 1  1 0 1 1 1}
            {1 1 1 1 1  1 0 1 0 2}
            {1 1 1 1 1  1 0 0 2 1}
            {1 1 1 1 1  1 0 0 1 2}
            {1 1 1 1 1  0 2 1 1 0}
            {1 1 1 1 1  0 2 1 0 1}
            {1 1 1 1 1  0 2 0 1 1}
            {1 1 1 1 1  0 1 2 1 0}
            {1 1 1 1 1  0 1 2 0 1}
            {1 1 1 1 1  0 1 1 2 0}
            {1 1 1 1 1  0 1 1 1 1}
            {1 1 1 1 1  0 1 1 0 2}
            {1 1 1 1 1  0 1 0 2 1}
            {1 1 1 1 1  0 1 0 1 2}
            {1 1 1 1 1  0 0 2 1 1}
            {1 1 1 1 1  0 0 1 2 1}
            {1 1 1 1 1  0 0 1 1 2}
            end
        end
    end
```

5\. 计算结束时打印的三个二阶 ZFS 分量（`Second order D-tensor: component 0` 等）使用该配合物的 *S* 值（本例中为 4.5（9 个电子 $\times$ 0.5））进行缩放。为了获得正确的 ZFS 局域值，三个矩阵必须用 Mn(III) 的 *S* 值（即 2）重新缩放。注意三个矩阵有不同的缩放前置因子，对 *S* 的依赖性不同：

$\mathbf{D}^{SOC-(0) } \propto \frac{1}{S^2}$

$\mathbf{D}^{SOC-(-1) } \propto \frac{1}{S(2S-1) }$

$\mathbf{D}^{SOC-(+1) } \propto \frac{1}{(S+1)(2S+1) }$

这些方程可用于计算所需的前置因子。例如对于 *SOC*-(0)，前置因子等于：

$\mathbf{D}_{\mathrm{Mn(III) }}^{SOC-(0) } = \frac{4.5^2}{2^2}\cdot\mathbf{D}_{\mathrm{dimer} }^{SOC-(0) } = 5.0625 \cdot \mathbf{D}_{\mathrm{dimer} }^{SOC-(0) }$

最后一步是用适当的前置因子缩放其余两个矩阵，将三个矩阵相加，对所得矩阵对角化，并用其本征值计算 *D* 和 *E* 参数。这些代表 Mn(III) 中心的局域 ZFS 参数。

(sec:modelchemistries.mrci.soc.excited_state_zfs)=
### 来自激发多重态的零场分裂

对于激发态多重态，可以通过以下方式请求 ZFS 计算

```orca
Lowest eigenvalue of the SOC matrix:    -149.86223277 Eh
Energy stabilization:    -2.54512 cm-1
Eigenvalues:     cm-1         eV      Boltzmann populations at T =  300.000 K
   0:            0.00        0.0000       3.36e-01
   1:            2.37        0.0003       3.32e-01
   2:            2.37        0.0003       3.32e-01
   3:         7757.65        0.9618       2.33e-17
   4:         7757.66        0.9618       2.33e-17
   5:        11913.81        1.4771       5.15e-26
```

```orca
soc
 DTensor true
 IStates 3,4,5
end
```

```orca
*****************************************
 EXCITED STATE ZERO-FIELD SPLITTING:
*****************************************

--------------------------------------------
Computing Excited State D Tensors of
Excited State Multiplet Consisting of States :  3  4  5
--------------------------------------------
          0         4     
          1         5     
          2         0     
          3         1     
          4         0     
          5         2     


--------------------------------------------
           ZERO-FIELD SPLITTING
(2ND ORDER SPIN-ORBIT COUPLING CONTRIBUTION)
--------------------------------------------

D   =   -2.668445  cm-1
E/D =    0.000103


...

--------------------------------------------------------
                  ZERO-FIELD SPLITTING
EFFECTIVE HAMILTONIAN SOC CONTRIBUTION
--------------------------------------------------------

D   =   -2.674495  cm-1
E/D =    0.009610

...
```

(sec:modelchemistries.mrci.soc.gTensor)=
### g-张量
```{index} g-Tensor with MRCI
```

`orca_mrci` 程序包含使用 MRCI 波函数计算 g-张量的选项。对于奇数电子体系，从 QDPT 过程获得的二重简并本征值代表 Kramers 对，用于从 Zeeman 哈密顿量构建总自旋算符和总角动量算符的矩阵元。将 $\Psi$ 记为一个解，$\bar{\Psi}$ 记为其 Kramers 伙伴，并使用矩阵元记号

$$\Phi_{11}^{k} =\left\langle\Psi \right|\hat{{L} }_{k} +g_{e} \hat{{S} }_{k}
\left| \Psi \right\rangle,\, \Phi_{12}^{k} =\left\langle\Psi
\right|\hat{{L} }_{k} +g_{e} \hat{{S} }_{k} \left| \bar{\Psi} \right\rangle,\, k=x,y,z
$$ (eqn:229)

g-矩阵的元素由下式获得：

$$g_{kz} =2\Phi_{11}^{k} ,\, g_{ky} =-2\Im\left({ \Phi_{12}^{k} }
\right) ,\, g_{kx} =2\Re\left({ \Phi_{12}^{k} } \right)$$ (eqn:230)

然后，真实张量 G 由 g-矩阵构建：

$$G=gg^{T}
$$ (eqn:231)

G 进一步对角化得到正本征值，其平方根给出 g-矩阵的主值。

$$g_{xx} =\sqrt{ G_{xx} } ,\, g_{yy} =\sqrt{ G_{yy} } ,\, g_{zz} =\sqrt{ G_{zz} }
$$ (eqn:232)

g-张量计算的输入文件的典型 mrci 块（例如 S=3/2 问题）应如下所示：

```orca
%mrci   ewin -4,1000
        citype mrci
        cimode direct2
        intmode fulltrafo
        solver diis
        etol 1e-8
        rtol 1e-8
        tsel 1e-6
        tpre 1e-5
        soc
          PrintLevel 2
          GTensor true      # make g-tensor calculations
          NDoubGTensor 2    # number of Kramers doublets to account
                            # for every pair a separate
                            # calculation is performed
        end
        newblock 4 *
          excitations cisd
          nroots 10
          refs  cas(7,5) end
        end
end
```

第一对 Kramers 对的结果打印如下：

```orca
--------------
KRAMERS PAIR 1
--------------

Matrix elements Re<1|S|1>   -0.072128   0.024511  -2.998843 
Matrix elements Re<1|S|2>   -0.001088   0.000366  -0.002010 
Matrix elements Im<1|S|2>   -0.000354  -0.001037  -0.000173 
Matrix elements Re<1|L|1>   -0.027067   0.009209  -1.123531 
Matrix elements Re<1|L|2>   -0.000031   0.000010  -0.000763 
Matrix elements Im<1|L|2>   -0.000006  -0.000011  -0.000065 

-------------------
ELECTRONIC G-MATRIX
-------------------

g-matrix:
-0.002240     0.000754    -0.005551 
0.000720     0.002100     0.000477 
-0.198556     0.067498    -8.251703 

g-factors:
0.002220     0.002222     8.254370 iso =     2.752937

g-shifts:
-2.000100    -2.000098     6.252051 iso =     0.750618

Eigenvectors:
0.057426     0.998060     0.024055 
0.998327    -0.057244    -0.008177 
0.006784    -0.024484     0.999677
```

这里对于 $L$ 和 $S$ 矩阵元，指标 1 和 2 被假设表示 Kramers 伙伴，第一行的三个数字代表 $x, y, z$ 贡献。

此外，g-张量也在有效哈密顿量形式体系中计算。

```orca
----------------------------------------------
  ELECTRONIC G-MATRIX FROM EFFECTIVE HAMILTONIAN
  ----------------------------------------------

  g-matrix:
  1.978874    -0.000345     0.018908 
  -0.000345     1.977899    -0.006433 
  0.018879    -0.006418     2.763402 

  g-factors:
  1.977789     1.978477     2.763909 iso =     2.240058

  g-shifts:
  -0.024530    -0.023843     0.761590 iso =     0.237739

  Eigenvectors:
  0.288884     0.957062     0.024060 
  0.957364    -0.288770    -0.008181 
  0.000882    -0.025397     0.999677 

  # The g-factors are square roots of the eigenvalues of gT*g
  # Orientations are the eigenvectors of gT*g
```

最后且仅在 MRCI 模块中，g-张量使用态求和（Sum Over States）形式体系{cite}`neese2003sos-gtensors`求值：

```orca
---------------------------------------------------------------------------
  SUM OVER STATES CALCULATION OF THE SPIN HAMILTONIAN (for g and HFC tensors)
  ---------------------------------------------------------------------------


  Ground state index        =     0
  Ground state multiplicity =     4
  Ground state spin density = P[  1]
  State =   1  <0|P|I>=   2  <0|Q|I>=  19
  State =   2  <0|P|I>=   3  <0|Q|I>=  27
  State =   3  <0|P|I>=   4  <0|Q|I>=  34
  State =   4  <0|P|I>=   5  <0|Q|I>=  40
  State =   5  <0|P|I>=   6  <0|Q|I>=  45
  State =   6  <0|P|I>=   7  <0|Q|I>=  49
  State =   7  <0|P|I>=   8  <0|Q|I>=  52
  State =   8  <0|P|I>=   9  <0|Q|I>=  54
  State =   9  <0|P|I>=  10  <0|Q|I>=  55

  Origin for angular momentum        ... ( -0.0006, -0.0010,  0.0021)
  Kinetic Energy                     ... done
  Relativistic mass correction       ... done
  Gauge correction                   ... done
  Angular momentum integrals         ... done
  Reading Spin-Orbit Integrals       ... done
  -----------------------
  MATRIX ELEMENT PRINTING
  -----------------------

  Energy differences (DE=EI-E0) and spin-orbit matrix elements (SO=<I|HSO|0>) are 
  printed in cm**-1. Orbital Zeeman matrix elements (L=<I|L|0>) are printed in au.

  State   DE        LX        LY        LZ          SOX         SOY         SOZ
  1    1349.3     0.0464   -0.0158    1.9264     -23.432       7.965    -974.312
  2   13026.2    -0.6596    0.6888    0.0214     337.028    -351.116     -10.966
  3   13615.1    -0.6961   -0.6514    0.0113     354.225     332.219      -5.736
  4   56686.3    -0.0053    0.0077    0.0971       1.794      -1.696     -36.786
  5   56954.2    -0.0516   -0.0048   -0.0042      28.211       5.821       1.459
  6   56994.0    -0.0418    0.0233   -0.0025      15.185      -2.144       1.145
  7   63371.5    -0.0211    0.0226    0.0078       3.833      -2.948      -2.724
  8   64176.0    -0.0652    0.0032   -0.0002      32.779       6.146       0.063
  9   74309.9    -0.0007    0.0032    0.0380       0.183      -1.058     -13.517

  -------------------
  ELECTRONIC G-MATRIX
  -------------------

  raw-matrix : 
  2.025533    -0.000738     0.021755  
  -0.000738     2.024537    -0.007389  
  0.021755    -0.007389     2.928943  

  g-factors: 
  2.024122     2.025363     2.929527 iso =     2.326338

  g-shifts:
  0.021803     0.023044     0.927208 iso =     0.324018

  Eigenvectors: 
  0.533896    -0.845208     0.024064  
  0.845530     0.533866    -0.008182  
  -0.005932     0.024715     0.999677  


  Euler angles w.r.t. molecular frame (degrees):
  -76.5038       1.4564    -161.2223

  -----------------------------
  CONTRIBUTIONS TO THE G-MATRIX
  -----------------------------

  Term                                g1           g2           g3
  --------------------------------------------------------------------
  Relativistic mass correction:   -0.0008220   -0.0008220   -0.0008220
  Gauge correction            :    0.0000000    0.0000000    0.0000000
  g(OZ/SOC)                   :    0.0226250    0.0238662    0.9280297

  State   1                   :    0.0000000   -0.0000000    0.9279829
  State   2                   :    0.0013767    0.0223913    0.0000000
  State   3                   :    0.0212332    0.0014408    0.0000000
  State   4                   :    0.0000000    0.0000004    0.0000418
  State   5                   :    0.0000074    0.0000099    0.0000001
  State   6                   :    0.0000002    0.0000078    0.0000001
  State   7                   :    0.0000000    0.0000015    0.0000002
  State   8                   :    0.0000076    0.0000144    0.0000000
  State   9                   :    0.0000000    0.0000000    0.0000046
  -----------------------------------------
  Total g-shifts              :    0.0218030    0.0230442    0.9272077


  # The g-factors are square roots of the eigenvalues of gT*g
  # Orientations are the eigenvectors of gT*g
```

注意在 SOS 形式体系中，除了二阶（SOC）贡献外，对场的双线性项：相对论质量校正和抗磁自旋-轨道项（Gauge）也被求值。可以看到，与二阶 SOC 贡献相比，这些校正相当可忽略，大多数时候可以安全地省略。此外，通过打印每个激发态对 g-张量的单独贡献可以获得进一步的洞察。在上面的例子中，第一激发态对 $g_z$ 分量有贡献，而接下来的两个分别对 $g_x$ 和 $g_y$ 分量有贡献。

总结一下，在 MRCI 和/或 CASSCF 等基于波函数的方法框架中，g-张量计算可以通过以下方式求值：

-   通过 QDPT 方法在单个 Kramers 双重态内。这种分析仅对非整数自旋情况有效。特别是对于具有良好隔离的 Kramers 双重态的体系，其中 EPR 谱仅来自在赝自旋 1/2 形式体系中定义的一个 Kramers 双重态。该分析已被证明对确定 ZFS 的符号和所研究体系的电子结构有用。{cite}`maganas2011zfs`

-   在有效哈密顿量方法内。这对所有自旋情况都是有效的分析，因为它提供在分子轴坐标系中求值的所研究体系的主 g 值。这些 g 值可以直接与实验确定的值比较。{cite}`maganas2015zfs`

-   在态求和（SOS）形式体系内。如上所述，该分析对所有自旋情况有效，且仅通过 MRCI 模块提供。

(sec:modelchemistries.mrci.soc.magnet)=
### 磁化与磁化率
```{index} Magnetic Properties with MRCI
```

ORCA 的 MRCI 和 CASSCF 模块允许通过对 QDPT 哈密顿量关于磁场的微分，在不同磁场和温度下计算磁化和磁化率曲线。对于磁化率，当定义了非零静磁场时，计算以两种方式进行：(i) 作为能量对磁场的二阶导数；(ii) 作为磁化除以磁场。虽然第一种方法对应于磁化率的定义，但第二种方法在实验确定 $\chi*T$ 曲线中被广泛使用。如果静磁场较低，两种公式倾向于提供相似的值。

完整关键词列表如下。

```orca
%mrci
   citype mrci
   newblock 3 *
   excitations none
   refs cas(2,7) end
   end
   soc
     dosoc true
     domagnetization true      # Calculate magnetization (def: false)
     dosusceptibility true     # Calculate susceptiblity (def: false)
     LebedevPrec            5  # Precision of the grid for different field
                               # directions (meaningful values range from 1
                               # (smallest) to 10 (largest))
     nPointsFStep           5  # number of steps for numerical differentiation
                               # (def: 5, meaningful values are 3, 5 7 and 9)
     MAGFieldStep       100.0  # Size of field step for numerical 
                               # differentiation (def: 100 Gauss)
     MAGTemperatureMIN    4.0  # minimum temperature (K) for magnetization
     MAGTemperatureMAX    4.0  # maximum temperature (K) for magnetization
     MAGTemperatureNPoints  1  # number of temperature points for magnetization
     MAGFieldMIN          0.0  # minimum field (Gauss) for magnetization
     MAGFieldMAX      70000.0  # maximum field (Gauss) for magnetization
     MAGNpoints            15  # number of field points for magnetization
     SUSTempMIN           1.0  # minimum temperature (K) for susceptibility
     SUSTempMAX         300.0  # maximum temperature (K) for susceptibility
     SUSNPoints           300  # number of temperature points for susceptibility
     SUSStatFieldMIN      0.0  # minimum static field (Gauss) for susceptibility
     SUSStatFieldMAX      0.0  # maximum static field (Gauss) for susceptibility
     SUSStatFieldNPoints    1  # number of static fields for susceptibility
   end
end
```

相同的关键词适用于 CASSCF 计算中的 rel 块（代替 MRCI 中的 soc）。虽然可以通过关键词修改积分和网格精度的不同方面，但默认值应能提供对两种性质的精确描述。计算的磁化和磁化率分别打印在 .sus 和 .mag 文件中，也在输出文件中。

```orca
-------------------------------------------------------------------------------
FIELD DEPENDENT MAGNETIZATION AND MEAN SUSCEPTIBILITY (chi=M/B)
-------------------------------------------------------------------------------
TEMPERATURE (K)   M. FIELD (Gauss)   MAGNETIZATION (B.M.)   chi*T (cm3*K/mol)
-------------------------------------------------------------------------------

4.00               0.00               0.000000                  inf
4.00            5000.00               0.350759             1.567189
4.00           10000.00               0.688804             1.538788
4.00           15000.00               1.003466             1.494496
4.00           20000.00               1.287480             1.438115
4.00           25000.00               1.537346             1.373773
4.00           30000.00               1.752841             1.305282
4.00           35000.00               1.936067             1.235764
4.00           40000.00               2.090450             1.167516
4.00           45000.00               2.219920             1.102067
4.00           50000.00               2.328368             1.040315
4.00           55000.00               2.419335             0.982690
4.00           60000.00               2.495883             0.929301
4.00           65000.00               2.560582             0.880052
4.00           70000.00               2.615538             0.834730
-----------------------------------------------------------
```

```orca
-----------------------------------------------------------
  TEMPERATURE DEPENDENT MAGNETIC SUSCEPTIBILITY
  -----------------------------------------------------------
  STATIC  FIELD    TEMPERATURE       chi*T (cm3*K/mol)
  (Gauss)           (K)          M/B          d2E/dB2
  -----------------------------------------------------------

  0.00       1.00           ----       1.576836
  0.00       2.00           ----       1.576910
  0.00       3.00           ----       1.576951
  0.00       4.00           ----       1.576988
  0.00       5.00           ----       1.577023
  0.00       6.00           ----       1.577057
  0.00       7.00           ----       1.577091
  0.00       8.00           ----       1.577125
  0.00       9.00           ----       1.577159
  0.00      10.00           ----       1.577193
  0.00      11.00           ----       1.577227
  .....
  0.00     300.00           ----       1.586942
 1000.00     1.00       1.570517       1.558042
 1000.00     2.00       1.575324       1.572178
 1000.00     3.00       1.576246       1.574845
 1000.00     4.00       1.576590       1.575802
 1000.00     5.00       1.576768       1.576264
 1000.00     6.00       1.576880       1.576530
 1000.00     7.00       1.576961       1.576704
 1000.00     8.00       1.577026       1.576829
  .....
```

注意 CASSCF 模块也支持在非零用户定义磁场下计算磁化率张量。MRCI 模块目前尚不支持。

(sec:modelchemistries.mrci.soc.mcd)=
### MCD 与吸收光谱
```{index} MCD with MRCI
```

ORCA 程序的 MRCI 模块允许计算 MCD 光谱和 SOC 对吸收光谱的影响。该形式体系由 Ganyushin 和 Neese 详细描述{cite}`ganyushin2008`。该方法基于直接计算磁能级之间的跃迁能和跃迁概率。即从初始态流形 $A$ 到终态流形 $J$ 的跃迁中 LCP- 和 RCP 光子的微分吸收。使用 Fermi 黄金规则、Franck-Condon 近似，假设纯电子偶极机制并考虑能级的 Boltzmann 布居，MCD 光谱的基本方程可以写为（全文使用原子单位）：

$$\frac{\Delta \varepsilon }{E}=\gamma \sum\limits_{a,j} { \left({N_{a} -N_{j} } \right)\left({ \left|{ \left\langle { \Psi_{a} \left|{m_{\text{LCP} } } \right|\Psi_{j} } \right\rangle} \right|^{2}-\left|{\left\langle { \Psi_{a} \left|{ m_{\text{RCP} } } \right|\Psi_{j} } \right\rangle} \right|^{2} } \right)f\left( E \right)}
$$ (eqn:233)

这里 $a$ 和 $j$ 标记实验中探测的初始和终态流形的成员。

$$N_{a} \left({ B,T} \right)=\frac{\exp \left({ -E_{a} /kT}
\right)}{\sum\limits_i { \exp \left({ -E_{i} /kT} \right)} }
$$ (eqn:234)

表示 Boltzmann 布居，其中 $a$-th 基态子能级在能量 $E_{a}$，$f\left( E \right)$ 表示线形函数，$\gamma$ 表示常数集合。电偶极算符由下式给出：

$$m_{\text{LCP} } \equiv m_{x} -im_{y}
$$ (eqn:235)

$$m_{\text{RCP} } \equiv m_{x} +im_{y}
$$ (eqn:236)

它们表示偶极矩算符的线性组合：

$$\vec{{m} }=\sum\limits_N { Z_{N} \vec{{R} }_{N} } -\sum\limits_i { \vec{{r} }_{i} }
$$ (eqn:237)

其中 $N$ 和 $i$ 分别表示核（在位置 $\vec{{R} }_{N}$，电荷 $Z_{N})$ 和电子（在位置 $\vec{{r} }_{i} )$ 的求和。计算的跃迁偶极矩需要在 Euler 角上进行空间平均，通过在三个角度网格上简单求和完成。

$$\left({ \frac{\Delta \varepsilon }{E} } \right)_{ev} =\frac{1}{8\pi
^{2} }\int\limits_{\psi =0}^{2\pi } { \int\limits_{\phi =0}^{2\pi }
{\int\limits_{\theta =0}^\pi{ \left({ \frac{\Delta \varepsilon }{E} }
\right)\sin \theta d\theta d\phi d\psi } } } \approx \sum\limits_{\mu \eta
\tau } { \left({ \frac{\Delta \varepsilon }{E} } \right)_{\mu \eta \tau } }
\sin \theta_{\tau }
$$ (eqn:238)

最后，每次跃迁用具有确定 Gaussian 形状宽度参数的 Gaussian 曲线近似。因此，最终计算的 MCD 光谱来自这些曲线的叠加。

作为示例，考虑计算 \[Fe(CN) $_{6}$\]$^{3-}$ 的 MCD 光谱经典例子。输入文件的 mrci 块如下所示。

```orca
%mrci   ewin -4,10000
        citype mrddci2
        intmode ritrafo
        Tsel  1e-6
        Tpre  1e-5
        etol 1e-8
        rtol 1e-8
        cimode direct2
        maxmemint 300
        solver diis
        davidsonopt 0
        nguessmat 150
        MaxIter 50
        LevelShift 0.5
        PrintLevel 3
        soc
        printlevel 3
        Domcd true        # perform the MCD calculation
        NInitStates 24    # number of SOC and SSC state to account
                          # Starts from the lowest state
        NPointsTheta 10   # number of integration point for
        NPointsPhi 10     # Euler angles
        NPointsPsi 10     #
        B 43500           # experimental magnetic field strength
                          # in Gauss
        Temperature 299.0 # experimental temperature (in K)
        end
        newblock 2 *
         nroots 12
         excitations cisd
         refs cas(23,12) end
         end
        end
```

参数 B 和 Temperature 可以成对指定，即 B $=$ 1000, 2000, 3000...，Temperature $=$ 4, 10, 300.... 程序为每对计算 MCD 和吸收光谱。现在对积分网格的每个点，程序打印出 Euler 角、磁场在分子坐标系中的取向和能级。

```orca
Psi = 36.000 Phi = 72.000 Theta = 20.000

Bx = 8745.0 By = 12036.5 Bz = 40876.6

Energy levels (cm-1,eV):Boltzmann populations for T = 299.000   K
   0 :         0.000     0.0000         4.53e-01
   1 :         3.943     0.0005         4.45e-01
   2 :       454.228     0.0563         5.09e-02
   3 :       454.745     0.0564         5.08e-02
   4 :      1592.142     0.1974         2.13e-04
   5 :      1595.272     0.1978         2.10e-04
   6 :     25956.363     3.2182         2.59e-55
   7 :     25958.427     3.2184         2.56e-55
   8 :     25985.656     3.2218         2.25e-55
   9 :     25987.277     3.2220         2.23e-55
  10 :     26070.268     3.2323         1.49e-55
  11 :     26071.484     3.2325         1.49e-55
  12 :     31976.645     3.9646         6.78e-68
  13 :     31979.948     3.9650         6.67e-68
  14 :     32018.008     3.9697         5.56e-68
  15 :     32021.074     3.9701         5.48e-68
  16 :     32153.427     3.9865         2.90e-68
  17 :     32157.233     3.9870         2.84e-68
  18 :     42299.325     5.2444         1.81e-89
  19 :     42303.461     5.2450         1.78e-89
  20 :     42346.521     5.2503         1.45e-89
  21 :     42348.023     5.2505         1.44e-89
  22 :     42456.119     5.2639         8.53e-90
  23 :     42456.642     5.2640         8.51e-90
```

在接下来的行中，ORCA 计算 LCP 和 RCP 跃迁的强度并打印跃迁能、LCP 和 RCP 跃迁之差（记为 C）、LCP 和 RCP 跃迁之和（记为 D）以及 C 与 D 的比值。

```orca
                dE      Na         C          D        C/D
  0 -> 1        3.943 4.53e-01  1.14e-13  8.13e-13   0.00e+00
  0 -> 2      454.228 4.53e-01  5.01e-09  9.90e-09   5.06e-01
  0 -> 3      454.745 4.53e-01 -4.65e-09  7.00e-09  -6.65e-01
  0 -> 4     1592.142 4.53e-01 -8.80e-08  1.02e-07  -8.67e-01
  0 -> 5     1595.272 4.53e-01 -2.29e-08  2.97e-08  -7.71e-01
  0 -> 6    25956.363 4.53e-01  1.22e+01  9.60e+01   1.27e-01
  0 -> 7    25958.427 4.53e-01  3.44e+01  3.52e+01   9.77e-01
  0 -> 8    25985.656 4.53e-01  3.83e+01  1.70e+02   2.25e-01
  0 -> 9    25987.277 4.53e-01 -7.73e+00  6.03e+01  -1.28e-01
  0 ->10    26070.268 4.53e-01 -6.11e+00  2.85e+01  -2.14e-01
  0 ->11    26071.484 4.53e-01  6.17e+00  9.21e+00   6.70e-01
  0 ->12    31976.645 4.53e-01  2.45e+01  6.21e+01   3.95e-01
  0 ->13    31979.948 4.53e-01 -6.58e+01  6.93e+01  -9.50e-01
  0 ->14    32018.008 4.53e-01  3.42e-01  1.07e+02   3.21e-03
  0 ->15    32021.074 4.53e-01 -6.16e+00  3.24e+01  -1.90e-01
  0 ->16    32153.427 4.53e-01 -4.73e+01  1.37e+02  -3.46e-01
  0 ->17    32157.233 4.53e-01 -1.02e+00  5.97e+01  -1.71e-02
  0 ->18    42299.325 4.53e-01  6.47e+00  2.11e+01   3.07e-01
  0 ->19    42303.461 4.53e-01 -2.59e+00  7.61e+00  -3.40e-01
  0 ->20    42346.521 4.53e-01  1.90e+01  8.99e+01   2.11e-01
  0 ->21    42348.023 4.53e-01  3.36e+00  3.55e+00   9.48e-01
  0 ->22    42456.119 4.53e-01  2.52e-01  4.86e-01   5.20e-01
  0 ->23    42456.642 4.53e-01 -2.01e+00  2.91e+00  -6.91e-01
  1 -> 2      450.285 4.45e-01  4.59e-09  6.87e-09   6.69e-01
  1 -> 3      450.802 4.45e-01 -4.96e-09  9.73e-09  -5.09e-01
```

所有 C 和 D 值额外复制到文本文件 input.1.mcd、input.2.mcd... 中，用于每对 Temperature 和 B 参数。这些文件包含每个计算跃迁的能量和 C、D 值。这些文件被程序 `orca_mapspc` 用来计算谱线。`orca_mapspc` 程序从原始跃迁数据生成谱线。`orca_mapspc` 程序的主要参数在第 7.18.1 节描述。当前示例中 `orca_mapspc` 程序用于 MCD 光谱计算的典型用法如下：

```orca
orca_mapspc input.1.mcd MCD -x020000 -x150000 -w2000
```

这里光谱生成的区间设置为从 20000 cm$^{-1}$ 到 50000 cm$^{-1}$，线形参数设置为 2000 cm$^{-1}$。

通常，希望为光谱的不同峰指定不同的线宽参数以获得与实验的更好拟合。`orca_mapspc` 可以从名为 input.1.mcd.inp 的简单文本文件读取线形参数。该文件应包含能量区间（以 cm$^{-1}$ 为单位）和该能量区间的线形参数，形式为：

```orca
20000 35000 1000
35000 40000 2000
40000 50000 1000
```

该文件不应在执行命令中指定；`orca_mapspc` 会自动检查其存在：

```orca
orca_mapspc input.1.mcd MCD -x020000 -x150000
Mode is MCD
Number of peaks            ... 276001
Start wavenumber [cm-1]    ...  20000.0
Stop wavenumber [cm-1]     ...  50000.0
Line width parameters are taken from the file:input.1.mcd.inp
Number of points           ... 1024
```

最后，`orca_mapspc` 程序生成输出文本文件 input.1.mcd.dat，包含七列数字：跃迁能、MCD 跃迁强度（MCD 光谱）、吸收跃迁强度（吸收光谱）、MCD 与吸收强度之比，最后三列代表相应跃迁的"棒图"。

```orca
Energy      C         D         C/D       C        D       E/D
24310.8   0.6673    980.2678   0.0006   0.0000   0.0000   0.0000
24340.1   0.8471   1174.3637   0.0007  -0.0001   0.0129  -0.0112
24369.5   1.0664   1408.5788   0.0007   0.0001   0.0281   0.0033
24398.8   1.3325   1690.5275   0.0007   0.0000   0.0000   0.0000
24428.1   1.6542   2029.0152   0.0008   0.0000   0.0000   0.0000
24457.4   2.0416   2434.1699   0.0008   0.0000   0.0332   0.0003
```

现在可以用合适的图形程序绘制 MCD 和吸收光谱，例如 Origin 程序。

(fig:713)=
```{figure} ../../images/713.*

计算的 \[Fe(CN) $_6$\]$^{3-}$ MCD 和吸收光谱（虚线）与实验光谱（实线）的比较。
```

(sec:modelchemistries.mrci.soc.magField)=
### 加磁场

将 Zeeman 贡献包含到 QDPT 过程中可以获得外磁场中磁能级的分裂。该计算的开关和磁场强度在 mrci 块的 soc 子块中定义。可选地，对于 `MagneticField_PrintLevel` 大于 0 可以打印波函数分解。后者使用阈值 `TPrint` 来省略打印中的小贡献：

```orca
%mrci
  soc
    DoSOC true          #
    DoSSC true          #
    MagneticField true  # default false
    B 1,10,100,1000     # Strengh of the magnetic field in Gauss.
                        # 4000 is the default value
    
    # Optional printing of the wave function for each
    # magnetic field settings
    MagneticField_PrintLevel 0 # default (disabled)
    TPrint                    1e-3 
  end
end
```

然后，输出包含磁场沿 x、y 和 z 方向平行施加时磁能级分裂的三组数据：

```orca
End B (Gauss)  Energy levels (cm-1) and populations for B || x

     1.0   -0.030   0.333   0.012   0.333   0.018   0.333
    10.0   -0.030   0.333   0.012   0.333   0.018   0.333
   100.0   -0.031   0.333   0.012   0.333   0.020   0.333
  1000.0   -0.102   0.333   0.012   0.333   0.091   0.333

B (Gauss)  Energy levels (cm-1) and populations for B || y

     1.0   -0.030   0.333   0.012   0.333   0.018   0.333
    10.0   -0.030   0.333   0.012   0.333   0.018   0.333
   100.0   -0.032   0.333   0.014   0.333   0.018   0.333
  1000.0   -0.105   0.334   0.018   0.333   0.087   0.333

B (Gauss)  Energy levels (cm-1) and populations for B || z

     1.0   -0.030   0.333   0.012   0.333   0.018   0.333
    10.0   -0.030   0.333   0.011   0.333   0.018   0.333
   100.0   -0.030   0.333   0.005   0.333   0.025   0.333
  1000.0   -0.079   0.333  -0.030   0.333   0.108   0.333
```

这里一行中的数字代表磁场强度（以 Gauss 为单位），随后的数字对表示磁能级的能量（以 cm$^{-1}$ 为单位）及其占据数。该表可以用任何合适的图形程序轻松绘制。

(sec:modelchemistries.mrci.soc.picturechange)=
### Douglas-Kroll-Hess SOC 和 Zeeman 算符中的相对论绘景变换
```{index} Picture Change Effects with MRCI
```

SOC 算符的 DKH 校正在 ORCA 中作为 SOMF 算符单电子部分的校正实现。DKH 变换执行到二阶，我们的实现中双电子部分保持不变换。然而，用于求值 SOMF 矩阵元的电子密度来自标量相对论计算。DKH 校正的包含由 rel 块中的 picturechange 键控制：

```orca
%rel method DKH              # relativistic method
     picturechange 2         # include the DKH correction to SOC
     end
```

"picturechange" 键可以设为 0、1 和 2，分别对应无绘景变换、SOC 算符的一阶和二阶 DKH 变换。

当 "picturechange" 设为 1 或 2 时，DKH 校正以一阶应用于 Zeeman 算符。该校正对含第三周期及更重原子的分子的计算 g-张量有明显影响。

(sec:modelchemistries.mrci.soc.x-ray.spectroscopy)=
### X 射线光谱
```{index} X-Ray Spectroscopy with MRCI
```

与第 {ref}`sec:casscf.CoreExitedStates.detailed` 节介绍的 CASCI/NEVPT2 计算方案类似，从 ORCA 4.2 起 MRCI 模块可用于计算芯层激发光谱，即 X 射线吸收（XAS）和共振非弹性散射（RIXS）光谱。

如 CASCI/NEVPT2 方案 {ref}`sec:casscf.CoreExitedStates.detailed` 中所讨论的，在 MRCI 模块内计算 XAS/RIXS 光谱遵循类似的策略。原则上 XAS/RIXS 光谱计算需要两个步骤：

-   第一步需要在 SA-CASSCF 计算框架中优化价层活性空间轨道，例如包含 6 到 15 eV 范围内的价层激发态。

-   第二步将相关芯层轨道旋转到活性空间中，并用单芯层激发电子组态饱和激发空间，使用先前优化的轨道集求解 MRCI 问题。

-   芯层轨道也包含在 XASMOs 定义中。该关键词的使用有两个目的。首先，它有效地将生成的组态状态函数（CSFs）减少到仅包含来自定义的芯层轨道的贡献的那些。在 RIXS 和 XES（见下文）的情况下，指定的 XASMOs 用于定义中间态或芯层电离态。

Fe(Cl) $_4$ 的代表性输入如下：

-   第一步对 5 个五重态和 15 个三重态执行 SA-CASSCF 计算（FeIICl4.casscf.inp）。

```orcainput
!cc-PWCVTZ-DK cc-pVTZ/C RIJCOSX SARC/J TightSCF DKH2

%rel
  FiniteNuc true
end

%basis
  newgto Cl "cc-pVTZ-DK" end
  newauxgto Cl "cc-pVTZ/C" end
end

%method FrozenCore FC_NONE
end

%casscf nel   6
  norb   5
  mult   5,3
  nroots 5,15
  switchstep nr
end

* xyz -2 5
Fe  -17.84299991694815     -0.53096694321123      6.09104775508499
Cl  -19.84288422845700      0.31089495619796      7.04101319789001
Cl  -17.84298666758073      0.11868125024595      3.81067954087770
Cl  -17.84301352218429     -2.87052442818457      6.45826391412877
Cl  -15.84311566482982      0.31091516495189      7.04099559201853
*
```

-   第二步将芯层轨道旋转到活性空间中，并用涉及芯层轨道单激发的所有五重态和三重态饱和激发空间来求解 MRCI 问题（FeIICl4-mrci.inp）

```orca
!MORead CC-PWCVTZ-DK cc-pVTZ/C  RIJCOSX SARC/J TightSCF DKH2 

%moinp "FeIICl4-casscf.gbw"

%rel
  FiniteNuc true
end

%method FrozenCore FC_NONE
end

%scf
  rotate { 6,42,90} { 7,43,90} { 8,44,90}  end
end

%basis
  newgto Cl "cc-pVTZ-DK" end
  newauxgto Cl "cc-pVTZ/C" end
end


%casscf
  nel    12
  norb   8
  mult   5,3
  nroots 34,195
  maxiter 1
  switchstep nr
end


%mrci
  CIType MRCI
  intmode fulltrafo
  XASMOs 42, 43, 44
  newblock 5 *
  nroots 34
  excitations cisd
  refs CAS(12,8)
  end
  end
  newblock 3 *
  nroots 195
  excitations cisd
  refs CAS(12,8)
  end
  end
  maxiter 100
  soc
  printlevel 3
  dosoc true
  end
end


* xyz -2 5
Fe  -17.84299991694815     -0.53096694321123      6.09104775508499
Cl  -19.84288422845700      0.31089495619796      7.04101319789001
Cl  -17.84298666758073      0.11868125024595      3.81067954087770
Cl  -17.84301352218429     -2.87052442818457      6.45826391412877
Cl  -15.84311566482982      0.31091516495189      7.04099559201853
*
```

类似地，多参考运动方程耦合簇 MR-EOM-CC（见下一节）也可用于计算 X 射线光谱。更多信息见参考文献{cite}`2019xasmrcimreom`

正如相关 ROCIS 节明确描述的，RIXS 光谱可以通过以下关键词请求：

```orca
RIXS    true    # Request RIXS calculation (NoSOC)   
RIXSSOC true    # Request RIXS calculation (with SOC)   
Elastic true    # Request RIXS calculation (Elastic)
```

请查阅第 {ref}`sec:spectroscopyproperties.rocis.rixs` 节以处理和分析生成的光谱

与 TDDFT（{ref}`sec:spectroscopyproperties.tddft`）、ROCIS（{ref}`sec:spectroscopyproperties.excitedstates.rocis`）和 CASSCF（{ref}`sec:casscf.CoreExitedStates.detailed`）类似，计算的跃迁密度（包括 SOC 存在时）可以使用 [OPS 工具](#sec:spectroscopyproperties.ops)超越偶极近似，详见细节。

1.  通过执行多极展开

2.  通过计算完整的半经典跃迁矩

整个光谱表集合可以通过以下命令请求：

```orca
%mrci
 DoDipoleLength        true
 DoDipoleVelocity      true
 DecomposeFosc         true
 DoFullSemiclassical   true
end
```

更多细节见 TDDFT（{ref}`sec:spectroscopyproperties.tddft`）、ROCIS（{ref}`sec:spectroscopyproperties.excitedstates.rocis`）和 CASSCF（{ref}`sec:casscf.CoreExitedStates.detailed`）节。

从 ORCA 4.2 起，先前报道的 RASCI-XES 方案参考文献{cite}`2014xesrasci`（可计算 K$_\beta$ 主线 XES 光谱）可以完全在 ORCA 模块内处理。在 ORCA 5.0 中，CASSCF 模块中存在类似的方案（CASCI-XES）（{ref}`sec:casscf.CoreExitedStates.detailed`）

-   如上或在 CASCI/NEVPT2 情况下，第一步需要在 SA-CASSCF 计算框架中优化价层活性空间轨道，例如为 N 电子体系包含 6 到 15 eV 范围内的价层激发态。

-   第二步将金属 1s 和 3p 轨道旋转到活性空间中，并在 XASMOs 列表中定义 1s MO

-   在 SOC 存在下为 N-1 电子体系在 RASCI 框架中计算 XES 光谱，使用 XESSOC 关键词针对所有由 3p-1s 电子衰变主导的态。

Fe(Cl) $_6$ 的代表性输入序列如下：

如参考文献{cite}`2014xesrasci`所述，首先对 CAS(5,5) 用六重态以及 24 个四重态和 75 个双重态饱和激发空间，这些态以 SA-CASSCF 方式优化。

```orcainput
X2c x2c-TZVPall x2c/J  def2-TZVP/C


%scf
  MaxDisk 40000
end

%casscf
  nel 5
  norb 5
  mult 6,4,2
  nroots 1,24,75
  shiftup 0.5
  shiftdn 0.5
  trafostep RI
  maxiter 150
end

*xyz -3  6 
Fe      0.0000       0.0000     0.000000
Cl      2.478        0.0000     0.000
Cl     -2.478        0.0000     0.000
Cl      0.000005     2.478      0.00000
Cl      0.000005    -2.478     -0.0000
Cl     -0.000       -0.000      2.478
Cl      0.000       -0.0000    -2.478
*
```

接着将 1s 和 3p Fe 基 MO 旋转到活性空间中，并为 \[Fe(Cl) $_6$\]$^+$ 体系的 4 个七重态和 81 个五重态计算 XES 光谱。

```orca
! X2c x2c-TZVPall x2c/J  def2-TZVP/C MORead AllowRHF
! NormalPrint
! NoLoewdin NoMulliken


%moinp "fecl6_casscf.gbw"


%scf
  MaxDisk 40000
end


%scf
  #Rotate the 1s and 3p orbitals below the SOMOs by using the rotate option
  rotate {0,59,90} {36,60,90} {37,61,90} {38,62,90} end
end

%casscf
  nel 5
  norb 5
  mult 6,4
  nroots 1,24
  shiftup 0.5
  shiftdn 0.5
  trafostep exact
  maxiter 1
end


%mrci citype mrci
 UseIVOs false
 Etol 1e-8
 IntMode fulltrafo
 PrintLevel 3
 newblock 7 *
  excitations none
  nroots 4
  refs ras(12:4 1/5/0 0) end
 end
 newblock 5 *
  excitations none
  nroots 81
  refs ras(12:4 1/5/0 0) end
 end
 XASMOS 59
 soc
  dosoc true
  xessoc true
 end
end


*xyz -2  7 
Fe      0.0000       0.0000     0.000000
Cl      2.478        0.0000     0.000
Cl     -2.478        0.0000     0.000
Cl      0.000005     2.478      0.00000
Cl      0.000005    -2.478     -0.0000
Cl     -0.000       -0.000     2.478
Cl      0.000       -0.0000    -2.478
*
```

结果计算出 X 射线发射光谱，强度基于跃迁电偶极矩计算

```orca
--------------------------------------------------------------------------------------------------------
      SOC CORRECTED   EMISSION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS    
--------------------------------------------------------------------------------------------------------
      Transition         Energy     Energy  Wavelength fosc(D2)      D2       |DX|      |DY|      |DZ|  
                          (eV)      (cm-1)    (nm)                 (au**2)    (au)      (au)      (au)  
--------------------------------------------------------------------------------------------------------
 426-7.0A  -> 420-5.0A   7083.210737 57129953.4     0.2   0.000000203   0.00000   0.00002   0.00002   0.00002
 427-7.0A  -> 420-5.0A   7083.210737 57129953.4     0.2   0.000003409   0.00000   0.00003   0.00014   0.00000
 426-7.0A  -> 419-5.0A   7083.210739 57129953.4     0.2   0.000000626   0.00000   0.00004   0.00004   0.00002
 427-7.0A  -> 419-5.0A   7083.210739 57129953.4     0.2   0.000000169   0.00000   0.00000   0.00001   0.00003
 426-7.0A  -> 418-5.0A   7083.210756 57129953.5     0.2   0.000000867   0.00000   0.00003   0.00006   0.00002
 427-7.0A  -> 418-5.0A   7083.210756 57129953.5     0.2   0.000000228   0.00000   0.00000   0.00000   0.00004
 426-7.0A  -> 417-5.0A   7083.210911 57129954.8     0.2   0.000000824   0.00000   0.00001   0.00003   0.00006
 427-7.0A  -> 417-5.0A   7083.210911 57129954.8     0.2   0.000001296   0.00000   0.00008   0.00004   0.00000
 426-7.0A  -> 416-5.0A   7083.211098 57129956.3     0.2   0.000000159   0.00000   0.00000   0.00002   0.00002
  ...
 428-5.0A  ->  0-5.0A   7159.092436 57741980.6     0.2   0.000000000   0.00000   0.00000   0.00000   0.00000
 430-5.0A  ->  0-5.0A   7159.092436 57741980.6     0.2   0.000000000   0.00000   0.00000   0.00000   0.00000
 429-5.0A  ->  0-5.0A   7159.092436 57741980.6     0.2   0.000000000   0.00000   0.00000   0.00000   0.00000
 431-5.0A  ->  0-5.0A   7159.092436 57741980.6     0.2   0.000000000   0.00000   0.00000   0.00000   0.00000
 432-5.0A  ->  0-5.0A   7159.092436 57741980.6     0.2   0.000000000   0.00000   0.00000   0.00000   0.00000
--------------------------------------------------------------------------------------------------------
```

所得 XES 光谱可以通过用 `orca_mapspc` 处理上述输出文件来可视化

```orca
orca_mapspc fecl6_xes.out XESSOC -x07000 -x17200 -w4.0 -eV -n10000
```
:::{note} 注意
一般不推荐在 mrci 模块基础上计算 rasci XES 光谱。

- 事实上 $K_{\alpha}$: $\mathrm{Fe}\ 2p \rightarrow \mathrm{Fe}\ 1s$ 和 
$K_{\alpha}$: $\mathrm{Fe}\ 2p \rightarrow \mathrm{Fe}\ 1s$（主线 XES）光谱对态的需求极大，
需要生成大量相对论跃迁密度，这给 mrci 模块带来很大压力。

- 更直接和计算高效的替代方案是通过 %casscf 模块的 rasci xes 方案，如 {ref}`sec:modelchemistries.casscf.XES` 所述。
这原则上提供了计算所有 X 射线发射的合适方案
- $K_{\alpha}$: $\mathrm{Fe}\ 2p \rightarrow \mathrm{Fe}\ 1s$
- $K_{\beta_{1,3}}$: $\mathrm{Fe}\ 3p \rightarrow \mathrm{Fe}\ 1s$（主线 XES）  
- $K_{\beta_{2,5}}$ / $K_{\beta'}$: $(\mathrm{Cl}\ 2p + \mathrm{Fe}\ 3d) \rightarrow \mathrm{Fe}\ 1s$（VtC-XES）

以及相应的共振 XES（RIXS）光谱。

- 我们也提醒，在适用范围内 XES 和 RIXS 光谱也可以基于静态基态 DFT（SGS-DFT）计算，讨论见 {ref}`sec:spectroscopyproperties.xes`；以及 ROCIS 系列方法，讨论见 {ref}`sec:spectroscopyproperties.rocis.rixs`。
- 关于 X 射线光谱实验以及如何基于现代计算光谱学方法处理它们的一般讨论见参考文献 {cite}`MatheNatRevChem2025`
:::

因此通过处理上述光谱，可以得到与 {numref}`fig:FeCl6_RASCI_K_beta_XES` 中所示完全相似的光谱


(sec:modelchemistries.mrci.keywords)=
## 关键词
```{index} MRCI Keywords
```

:::{caution} 小心
MRCI 程序被视为遗留（legacy）程序。
:::

MRCI 模块的简单输入关键词在 {numref}`tab:modelchemistries.mrci.keywords.simple` 中给出。
注意如果使用这些，关于参考空间、根数等的所有信息都取自假设已预先运行的 CASSCF 模块。
一般来说，这些计算属于个别选择类型且非常耗时。
这些方法可以设置和修改非常多的标志，一般使用这些方法需要专家用户！
参见定义个别选择过程的变量 `Tsel`、`Tpre` 和 `Tnat`。
所有这些方法都可以通过使用 `RI-<Method>` 等与 RI 积分一起使用。
然而，由于积分是逐个即时生成的，计算会更加耗时。
非 RI 计算基本上局限于 CI 中包含约 200-300 个轨道。
下面是 `%mrci` 块关键词及其含义的相当完整的列表。

:::{raw} latex
\begingroup
\footnotesize
:::
(tab:modelchemistries.mrci.keywords.simple)=
:::{flat-table} MRCI 模块的简单输入关键词。
:header-rows: 1
:class: footnotesize
* - 关键词
  - 描述
* - `MRCI`
  - 启动含单激发和双激发的多参考组态相互作用计算
* - `MRCI+Q`
  - 同上加针对非连通四重激发的多参考 Davidson 校正
* - `MRACPF`
  - 平均耦合对泛函
* - `MRAQCC`
  - 平均二次耦合簇
* - `MRDDCI1`
  - 一个自由度的差值专用 CI
* - `MRDDCI2`
  - 同上两个自由度
* - `MRDDCI3`
  - 同上三个自由度
* - `MRDDCI<n>+Q`
  - 带 Davidson 校正的 MRDDCI（`n` = 1--3）
* - `SORCI`
  - 光谱导向 CI
:::
:::{raw} latex
\endgroup
:::


```orca
%mrci
       # -----------------------------------------------------------
       # Orbital selection
       # NOTE: The orbitals are used as supplied. Thus, the ORDER of
       # orbitals is critical. Say you have
       #   nact    electrons in the active space
       #   nint    electrons in the internal space
       #   nfrozen electrons
       # * The first nfrozen/2 orbitals will not be included in the CI
       # * The next nint/2 orbitals will be doubly occupied in all
       #   references
       # * the nact electrons are distributed over the,say, mact
       #   orbitals according to the active space definitions.
       # The remaining orbitals are external.
       # IT IS YOUR RESPONSIBILITY THAT THE ORBITAL ORDERING MAKES
       # SENSE!
       # A sensible two-step procedure is:
       #  * generate some orbitals and LOOK AT THEM. Decide which ones
       #    to include in the CI.
       #  * re-read these orbitals with ! MORead NoIter. Perhaps use
       #    the "rotate" feature to reorder the MOs
       #    Then jump right into the CI which is defined in this se-
       #    cond job
       #
       # NOTE: the MRCI module respects the %method FrozenCore settings
       # -----------------------------------------------------------
       Loc  0,0,0
           # Localize orbitals in the internal (first flag), active
           # (second flag) and external space (third flag).
       UseIVOs  false
           # Use improved virtual orbitals in the CI
       # orbital energy window for the frozencore option FC_EWIN
       EWIN -40,1000 
       # alternative MO definition 
       MORanges  First_internal, Last_Internal, First_active, Last_Active, First-Virtual,Last_virtual
       XASMOs  x1,x2,x3,...   # List of XAS donor MOs (see above)
      
       # ---------------------------------
       # Method selection
       # ---------------------------------
       CIType   MRCI      # Multireference CI (default)
                MRDDCI1   # Difference dedicated CI 1-degree of freedom
                MRDDCI2   # Difference dedicated CI 2-degrees of freedom
                MRDDCI3   # Difference dedicated CI 3-degrees of freedom
                MRACPF    # Average coupled-pair functional
                MRACPF2   # Modified version of ACPF
                MRACPF2a  # A slightly modified version of ACPF-2a
                MRAQCC    # Average quadratic coupled-cluster
                MRCEPA_R  # Multireference CEPA due to Ruttink
                MRCEPA_0  # CEPA-0 approximation
                SORCI     # Spectroscopy oriented CI
                SORCP     # Spectroscopy oriented couplet pair approx.
                MRMP2     # Multireference Moeller-Plesset at second order
                MRMP3     # Multireference Moeller-Plesset at third order
                MRMP4     # Multireference Moeller-Plesset at fourth order
                          # but keeping only singles and doubles relative to
                          # the reference configurations.

       # ---------------------------------
       # Selection thresholds
       # ---------------------------------
       Tsel    1e-6   # Selection threshold for inclusion in the CI based
                      # 2nd order MP perturbation theory <0|H|I>/DE(MP)
       Tpre    1e-4   # Selection of configurations in the reference space
                      # after the initial diagonalization of the reference
                      # space only configurations with a weight large>Tpre
                      # to any root are included
       AllSingles   false
                      # include ALL SINGLES in the CI. Default is now TRUE!!!

       # perturbative estimate of the effect of the rejected configurations
       EunselOpt  0   # no correction
                  1   # based on the overlap with the 0th order wavefunction
                  2   # calculation with the relaxed reference space
                      # coefficients. This is the most accurate and only
                      # slightly more expensive

       # For CIType=MRCI,MRDDCI and SORCI the approximate correction for
       # higher excitations
       DavidsonOpt  Davidson1  # default
                    Davidson2  # modified version
                    Siegbahn   # Siegbahn's approximation
                    Pople      # Pople's approximation

       # For MRACPF,MRACPF2,MRAQCC and SORCP
       NelCorr      0
          # Number of electrons used for computing the average coupled-
          # pair correction.
          # =0 : set equal to ALL electrons in the CI
          # =-1: set equal to all ACTIVE SPACE electrons
          # =-2: set equal to ACTIVE SPACE electrons IF inactive doubles
          #      are excluded (as in MRDDCI)
          # >0 : set equal to user defined input value
       LinearResponse false
          # Use ground state correlation energy to compute the shift for
          # higher roots (not recommended)

       # ---------------------------------
       # Natural Orbital Iterations
       # ---------------------------------
       NatOrbIters    0 # default
          # number of average natural orbital iterations
       Tnat        1e-4
          # cutoff of natural orbitals. NOs with an occupation number less
          # then Tnat will not be included in the next iteration
          # Also, orbitals with occupation number closer than Tnat to 2.0
          # will be frozen in the next iteration
       Tnat2       -1
          # if chosen >0 then Tnat2 is the threshold for freezing the
          # almost doubly occupied orbitals. Otherwise it is set equal
          # to Tnat

       # ----------------------------------
       # Additional flags and algorithmic
       # details
       # ----------------------------------
       PrintLevel   2  # default. Values between 1 and 4 are possible

       DoDDCIMP2  false
          # for DDCI calculations: if set to true the program computes
          # a MP2 like correction for the effect of inactive double
          # excitations which are not explicitly included in the CI. This
          # is necessary if you compare molecules at different geometries
          # or compute potential energy surfaces.
       # ----------------------------------
       # The SORCP model
       # ----------------------------------
       CIType_in  # First step CIType
       CIType_fi  # Second step CIType
       Exc_in     # First step excitation scheme
       Exc_fi     # Second step excitation scheme
       Tsel_in    # First step Tsel
       Tsel_fi    # Second step Tsel
       Tpre_in    # First step Tsel
       Tpre_fi    # Second step Tpre

         # Thus, the SORCI model corresponds to CIType=SORCP with
         # CIType_in MRCI  CIType_fi MRCI
         # Exc_in    DDCI2 Cexc_fi   DDCI3
         # Tsel_in   1e-5  Tsel_fi   1e-5
         # Tpre_in   1e-2  Tpre_fi   1e-2

       # ----------------------------------
       # Multirerence perturbation theory
       # ----------------------------------
       MRPT_b  0.02   # Intruder state avoidance PT after Hirao (default 0.0)
                      # with this flag individual intruders are shifted away to
                      # to some extent from the reference space
       MRPT_shift 0.3 # Level shift introduced by Roos which shifts the entire
                      # excited manifold away in order to avoid intruder states.
                      # A correction is applied afterwards but results do depend
                      # on this (arbitrary) value to some extent.
       H0Opt  projected  # use an off-diagonal definition of H0
              Diagonal   # use a diagonal definition of H0 (much faster but maybe
                         # a little less reliable
       Partitioning MP   # Moeller plesset partitioning
                    EN   # Epstein-Nesbet partitioning (not recommended)
                    RE   # Fink's partitioning 
       Fopt  Standard    # Standard definition of MR Fock operators
             G3          # uses Anderson's g3 correction also used in CASPT2
       UsePartialTrafo   true/false    # speedups MRMP2

       #---------------------------------------
       # restrict reference configurations
       #---------------------------------------
       RejectInvalidRefs true # by default reference CSFs are restricted
                              # to target spin and spatial symmetry

       # ======================================
       # Definitions of blocks of the CI Matrix
       # ======================================
       NewBlock 2 *    # generate a Block with doublet(=2) multiplicity
         Nroots  1     # number of roots to be generated
         Excitations cis   # CI with single excitations
                     cid   # CI with double excitations
                     cisd  # CI with single and double excitations
                     ddci1 # DDCI list with one degree of freedom
                     ddci2 # DDCI list with two degrees of freedom
                     ddci3 # DDCI list with three degrees of freedom
         Flags[_class_] 0 or 1
                  # Turn excitation classes on or off individually
                  # ``s'' stands for any SOMO, ``i'',``j'' for internal orbitals
                  #  and ``a'',``b'' for external orbitals
                  #  Singles _class_ = ss, sa, is, ia
                  #  Doubles _class_ = ijss, ijsa, ijab,
                  #                    isss, issa, isab,
                  #                    ssss, sssa, ssab
                  # ``Flags'' takes priority over ``Excitations''. In fact 
                  # ``Excitations'' does nothing but to set ``Flags''. So, 
                  # you can use ``Excitations'' to provide initial values 
                  # for ``Flags'' and then modify them with subsequent
		  # ``Flags'' assignments
         refs
               #
               # First choice - complete active space
               #
               CAS(nel,norb)  # CAS-CI reference with nel electrons in
                              # Norb orbitals
               #
               # Second choice - restricted active space
               #
               RAS(nel: m1 h/ m2 / m3 p)
                              # RAS-reference with nel electrons
                     # m1= number orbitals in RAS-1
                     # h = max. number of holes in RAS-1
                     # m2= number of orbitals in RAS-2 (any number of
                     #     electrons or holes)
                     # m3= number of orbitals in RAS-3
                     # p = max. number of particles in RAS-3
               #
               # Third choice - individually defined configurations
               #
                \{ 2 0 1 0\}
                \{ 1 1 1 0\}
                  etc.
              # define as many configurations as you want. Doubly occupied MOs
              # singly occupied MOs and empty MOs. Important notes:
              #  a) the number of electrons must be the same in all references
              #  b) the number of orbitals is determined from the number of
              #     definitions. Thus, in the example above we have three active
              #     electrons and four active orbitals despite the fact that the
              #     highest orbital is not occupied in any reference.
              #  The program determines the internal, active and external spaces
              #  automatically from the number of active electrons and orbitals
               end
         end
         # there can be as many blocks as you want!!!

       # ----------------------------------
       # Density matrix generation flags
       #  First Key= State densities <I|D|I>
       #     =0: none
       #     =1: Ground state only (lowest root of all blocks; Electron only)
       #     =2: Ground state only (Electron and spin density)
       #     =3: Lowest root from each block (Electron density)
       #     =4: Lowest root from each block (Electron and spin density)
       #     =5: All states (Electron density)
       #     =6: All states (Electron and spin density)
       #  Second Key= Transition densities <I|D|J>
       #     needed for all transition intensities, g-tensor etc
       #     =0: none
       #     =1: from the ground state into all excited states (el)
       #     =2: from the ground state into all excited states (el+spin)
       #     =3: from all lowest states into all excited states (el)
       #     =4: from all lowest states into all excited states (el+spin)
       #     =5: all state pairs (el)
       #     =6: all state pairs (el+spin)
       # Note that for perturbation theory the density is computed as
       # an expectation value over the first (second) order wavefunction.
       # which is renormalized for this purpose
       # ----------------------------------
       Densities 1,1
       
       # ----------------------------------
       # Complete printing of the wavefunction 
       # ----------------------------------
       PrintWF    1      # CFG based printing (default)
                  det    # Determinant based wavefunction printing
       TPrintWF   3e-3   # Threshold for the printing of the CFGs/Dets

       # ----------------------------------
       # Algorithm for the solver
       # ----------------------------------
       Solver   Diag   # Davidson like solver
                DIIS   # DIIS like solver
         # both solvers have their pros and cons. The DIIS may converge
         # better or use less time since it only recomputes the vectors that
         # have not yet converged; The DIIS may be less sensitive to root
	 # flipping effects but occasionally it converges poorly and states
	 # of the same symmetry are occasionally a little problematic
         # For perturbation theory DIIS is always used.
       # For both solvers
       MaxIter   100  # the maximum number of iterations
       Etol      1e-6 # convergence tolerance for energies in Eh
       Rtol      1e-6 # convergence tolerance for residual

       # For Solver=Diag (Davidson solver)
       Otol      1e-16 # Orthogonality threshold for Schmidt process
       NGuessMat 512   # Dimension of the guess matrix 512x512
                       # be used to compute the initial guess of the actual
		       # MRCI calculation
       NGuessMatRefCI 512 # Dimension of the guess matrix 
                          # for the reference CI
        
       MaxDim       3  # Davidson expansion space = MaxDim * NRoots
       # For the Solver=DIIS. Particularly recommended for anything else but
       # straightforward CI and also for calculations in direct2 mode!
       MaxDIIS       5 # Maximum number of old vectors to be used in DIIS
       RelaxRefs  true # Relax reference space coefficients in the CI or
                       # freeze them to their zeroth order values
       LevelShift  0.4 # Level Shift for stabilizing the DIIS procedure
       
       # ----------------------------------
       # RI Approximation
       # ----------------------------------
       IntMode RITrafo #Use RI integrals
               FullTrafo #No RI (default)
       
       # ----------------------------------
       # Integral storage, memory and files
       # ----------------------------------
       FourIndexInts false (default)
                     True
          # Store ALL four index integrals over Mos in main memory
          # only possible for relatively small systems, perhaps up
          # to 150-200 MOs included in the CI
       MaxMemInt     256
          # Maximum amount of core memory devoted to the storage of
          # integrals. If NOT all three index integrals fit into main
          # memory the program fails
       MaxMemVec      16
          # Maximum amount of memory used for section of the trial and
          # sigma vectors. This is not a particularly critical variable
       KeepFiles    false
          # Keep integrals and CI program input file (.mrciinp). Then
          # you can manually edit the .mrciinp file which is a standard
          # ASCII file and run the MRCI program directly. The only thing
          # you cannot change is the orbital window.
       end
```



[^1]: 无论你是持悲观还是乐观的观点，你可以说这个结果展示了 dedicated to a single determinant reference 的代码能实现什么。或者你（也许应该）抱怨为 MRCI 方法的通用性付出的高代价。无论如何，关键在于发展与单参考方法同样高效的多参考方法。更多信息见 FIC-MRCI 章节。

[^2]: 注意在打印时，我们总是对给定空间组态的所有线性无关自旋耦合求和，只打印组态的总权重，而不是组态的每个单独 CSF。

[^3]: 在这种情况下计算 $0^{th}$ 阶态与最终 CI 向量的最大重叠，并将微扰能加到"最相似的根"上。这当然是相当粗糙的近似，更好的选择是严格重算未选中组态的二阶能量，如 `EUnselOpt = FullMP2` 所做的那样。

[^4]: 这些结果大多来自稍早的版本，MR 能量与当前版本略有不同。能量差不受影响。

[^5]: 这些数字大多来自稍旧的版本，但在当前版本中不会有太大变化。
