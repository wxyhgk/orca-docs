

<a id="sec:spectroscopyproperties.elprop"></a>
# 电性质 - 电矩与极化率（Electrical Properties - Electric Moments and Polarizabilities）

ORCA 中可以计算一些基本电性质，尽管这从来不是开发的重点。
这些性质可以通过 `%elprop` 块直接访问：

```orca
! B3LYP DEF2-SVP TightSCF

%elprop Dipole       true # dipole moment
        Quadrupole   true # quadrupole moment

        Polar        true # dipole-dipole polarizability
                        1 # equivalent to true (for backward compatibility)
                          # Note: the flags "polar 2" and "polar 3" for
		          # seminumeric and fully numeric polarizabilities are 
                          # not supported anymore! For numerical polarizability 
                          # calculations please use the respective compound scripts
        
        Hyperpol     true # the dip/dip/dip hyperpolarizability

        PolarVelocity true # polarizability w.r.t. velocity perturbations
        PolarDipQuad  true # dipole-quadrupole polarizability
        PolarQuadQuad true # quadrupole-quadrupole polarizability
        end
* int 0 1
   C  0  0  0  0       0         0
   H  1  0  0  1.09  109.4712    0
   H  1  2  0  1.09  109.4712    0
   H  1  2  3  1.09  109.4712  120
   H  1  2  3  1.09  109.4712  240
*
```

极化率（偶极-偶极、偶极-四极、四极-四极）在 HF 和 DFT 计算中
通过求解耦合微扰（CP-）SCF 方程解析计算（见 [sec:essentialelements.cpscf](#sec:essentialelements.cpscf)），
在 CASSCF 计算中则通过 CP-CASSCF 方程计算（见 [sec:spectroscopyproperties.casscfresp](#sec:spectroscopyproperties.casscfresp)）。
解析极化率也可用于 CCSD/CCSD(T)（见 [sec:modelchemistries.autoci.autociresp](#sec:modelchemistries.autoci.autociresp)）、RI-MP2 和 DLPNO-MP2，
以及双杂化 DFT 方法。对于正则 MP2，可以使用 AUTOCI 进行解析计算
（见 [sec:modelchemistries.autoci.autociresp](#sec:modelchemistries.autoci.autociresp)），或者对使用弛豫密度
计算的解析偶极矩进行微分。对于其他相关方法，只能采用完全数值方法。

```orca
---------------------------------------------------
STATIC POLARIZABILITY TENSOR (Dipole/Dipole)
---------------------------------------------------

Method             : SCF
Type of density    : Electron Density
Type of derivative : Electric Field (Direction=X)
Multiplicity       :   1
Irrep              :   0
Relativity type    :
Basis              : AO

The raw cartesian tensor (atomic units):
    12.852429555       -0.002199911        0.000000170
    -0.002199911       12.860507003       -0.000000346
     0.000000170       -0.000000346       12.868107945
diagonalized tensor:
    12.851869269       12.861067290       12.868107945

Orientation:
     0.969064588       -0.246807263        0.000017958
     0.246807263        0.969064586       -0.000050696
    -0.000004890        0.000053560        0.999999999

Isotropic polarizability :  12.86035
```

正如预期的那样，极化率张量是各向同性的。

偶极-四极极化率张量以 18 个不同分量的列表形式打印，
第一个指标遍历 x,y,z，第二个指标遍历 xx,yy,zz,xy,xz,yz。
这被称为张量的"纯笛卡尔"（"pure Cartesian"）版本，
尽管文献中可能存在其他约定，与 ORCA 数值相差一个常数因子。

```orca
---------------------------------------------------
STATIC POLARIZABILITY TENSOR (Dipole/Quadrupole)
---------------------------------------------------

Method             : SCF
Type of density    : Electron Density
Type of derivative : Electric Field (Direction=X)
Multiplicity       :   1
Irrep              :   0
Relativity type    :
Basis              : AO

The raw cartesian tensor (atomic units):
  X- X X :     11.577165985
  X- Y Y :     -5.795339382
  X- Z Z :     -5.797320742
  X- X Y :      0.001285565
  X- X Z :      0.000000155
  X- Y Z :     -0.000000077
  Y- X X :      0.001386387
  Y- Y Y :      8.200445841
  Y- Z Z :     -8.198375727
  Y- X Y :     -5.794687548
  Y- X Z :      0.000000228
  Y- Y Z :     -0.000000121
  Z- X X :     -0.000000151
  Z- Y Y :      0.000000627
  Z- Z Z :     -0.000000812
  Z- X Y :     -0.000000312
  Z- X Z :     -5.798359323
  Z- Y Z :     -8.205110537
```

之后打印张量的"无迹"（"traceless"）版本，在文献中通常记为
$A_{x,xx}, A_{x,xy}$ 等[McLean1967JCP,Pedersen2011JCC,Yan2020CTP](../../bibliography.md)。
这是报告偶极-四极极化率张量的首选格式。
某些参考文献使用的符号约定与这里报告的相反，但总体而言，
无迹极化率张量的约定比纯笛卡尔极化率张量的约定更为统一。

```orca
-------------------------------------------------------------
STATIC TRACELESS POLARIZABILITY TENSOR (Dipole/Quadrupole)
-------------------------------------------------------------

Method             : SCF
Type of density    : Electron Density
Type of derivative : Electric Field (Direction=X)
Multiplicity       :   1
Irrep              :   0
Relativity type    :
Basis              : AO

The raw cartesian tensor (atomic units):
  X- X X :     17.373496046
  X- Y Y :     -8.685262003
  X- Z Z :     -8.688234043
  X- X Y :      0.001928347
  X- X Z :      0.000000232
  X- Y Z :     -0.000000116
  Y- X X :      0.000351329
  Y- Y Y :     12.298940512
  Y- Z Z :    -12.299291841
  Y- X Y :     -8.692031322
  Y- X Z :      0.000000342
  Y- Y Z :     -0.000000181
  Z- X X :     -0.000000058
  Z- Y Y :      0.000001109
  Z- Z Z :     -0.000001050
  Z- X Y :     -0.000000468
  Z- X Z :     -8.697538984
  Z- Y Z :    -12.307665806
```

四极-四极极化率张量同样以纯笛卡尔形式和无迹形式打印。
同样，无迹形式（通常记为 $C_{xx,xx}, C_{xx,xy}$ 等[McLean1967JCP,Pedersen2011JCC,Yan2020CTP](../../bibliography.md)）
是报告的首选格式。

```orca
---------------------------------------------------
STATIC POLARIZABILITY TENSOR (Quadrupole/Quadrupole)
---------------------------------------------------

The order in each direction is XX, YY, ZZ, XY, XZ, YZ

Method             : SCF
Type of density    : Electron Density
Type of derivative : Quadrupolar Field (Direction=X)
Multiplicity       :   1
Irrep              :   0
Relativity type    :
Basis              : AO

The raw cartesian tensor (atomic units):
      60.656194448         8.024072323         8.017351959        -0.002591466         0.000000801        -0.000000184
       8.024072323        55.906127614        12.837825709        -6.821368242        -0.000000954        -0.000000529
       8.017351959        12.837825709        55.938851507         6.815300773         0.000000232         0.000000422
      -0.002591466        -6.821368242         6.815300773        16.716647772         0.000000169        -0.000000030
       0.000000801        -0.000000954         0.000000232         0.000000169        16.715850196         6.818791255
      -0.000000184        -0.000000529         0.000000422        -0.000000030         6.818791255        21.534628724
diagonalized tensor:
      11.893291534        13.566719080        26.357187387        46.234564137        52.663246003        76.753292120

Orientation:
      -0.000000018        -0.000019986        -0.000000013        -0.001433194         0.817436692         0.576016666
       0.000000006         0.219691224         0.000000038         0.673107563        -0.405967809         0.577799371
       0.000000008        -0.219450737        -0.000000021        -0.671194117        -0.408640606         0.578232381
      -0.000000035         0.950566746        -0.000000034        -0.310519906        -0.000497156        -0.000034103
       0.816443231         0.000000038         0.577425709        -0.000000037         0.000000027         0.000000000
      -0.577425709        -0.000000003         0.816443231        -0.000000036         0.000000002        -0.000000003

Isotropic polarizability :  37.91138

-------------------------------------------------------------
STATIC TRACELESS POLARIZABILITY TENSOR (Quadrupole/Quadrupole)
-------------------------------------------------------------

The order in each direction is XX, YY, ZZ, XY, XZ, YZ

Method             : SCF
Type of density    : Electron Density
Type of derivative : Quadrupolar Field (Direction=X)
Multiplicity       :   1
Irrep              :   0
Relativity type    :
Basis              : AO

The raw cartesian tensor (atomic units):
      26.331642600       -13.160050722       -13.171591878         0.000221134         0.000000581        -0.000000065
     -13.160050722        22.733889017        -9.573838294        -5.113861448        -0.000000735        -0.000000324
     -13.171591878        -9.573838294        22.745430172         5.113640314         0.000000154         0.000000389
       0.000221134        -5.113861448         5.113640314        12.537485829         0.000000127        -0.000000022
       0.000000581        -0.000000735         0.000000154         0.000000127        12.536887647         5.114093442
      -0.000000065        -0.000000324         0.000000389        -0.000000022         5.114093442        16.150971543
```

!!! note
    -   **与四极矩本身类似，偶极-四极和四极-四极极化率依赖于
        `%elprop` 模块的规范原点。后者可以使用 `%elprop` 中的
        `Origin` 关键词更改；见章节 [sec:spectroscopyproperties.elprop](#sec:spectroscopyproperties.elprop)。**

对于不支持解析极化率的方法，可以计算数值的偶极-偶极和
四极-四极极化率，方法是对偶极/四极矩相对于有限偶极/四极电场
进行有限差分，或者对总能量相对于有限偶极/四极电场进行二重有限差分。
后者可以使用复合脚本完成（见 [sec:workflowsautomatization.compound](#sec:workflowsautomatization.compound)、
[sec:workflowsautomatization.compound_examples](#sec:workflowsautomatization.compound_examples)）。

在 MP2 水平上，目前可以使用 RI
（[sec:modelchemistries.mp2.rimp2.response](#sec:modelchemistries.mp2.rimp2.response)）或 DLPNO
（[sec:modelchemistries.mp2.dlpnoresp](#sec:modelchemistries.mp2.dlpnoresp)）近似或者在
全电子正则计算中解析计算极化率，但对于冻结芯轨道的正则 MP2，
必须对偶极矩进行数值微分才能得到极化率张量。一般来说，在这种情况下，
您应该记住，紧密的 SCF 收敛是必要的，以免二阶导数中出现过多数值噪声。
另外，您应该尝试数值微分过程中的有限场增量。

例如，以下复合任务可用于在 MP2 水平上计算半数值极化率
（替代现已弃用的 `Polar 2` 用法）：

```orca
! B3LYP DEF2-SVP TightSCF

%elprop Dipole       true # dipole moment
        Quadrupole   true # quadrupole moment

        Polar        true # dipole-dipole polarizability
                        1 # equivalent to true (for backward compatibility)
                          # Note: the flags "polar 2" and "polar 3" for
		          # seminumeric and fully numeric polarizabilities are 
                          # not supported anymore! For numerical polarizability 
                          # calculations please use the respective compound scripts
        
        Hyperpol     true # the dip/dip/dip hyperpolarizability

        PolarVelocity true # polarizability w.r.t. velocity perturbations
        PolarDipQuad  true # dipole-quadrupole polarizability
        PolarQuadQuad true # quadrupole-quadrupole polarizability
        end
* int 0 1
   C  0  0  0  0       0         0
   H  1  0  0  1.09  109.4712    0
   H  1  2  0  1.09  109.4712    0
   H  1  2  3  1.09  109.4712  120
   H  1  2  3  1.09  109.4712  240
*
```

其中文件 `semiNumericalPolarizability.cmp` 包含：

```orca
# ---------------------------------------------------------------------
# Authors: Dimitrios G. Liakos and Frank Neese
# Date   : March-May of 2024
#
# This is a compound script that calculates the 
#  raw porarizability tensor semi-numerically 
#  using the dipole moments.
#
# The idea is the following:
#
# 1. Calculate dipole moment  in the field free case 
# 
# 2. Loop over directions I=X,Y,Z
#    - put a small E-field in direction I+Delta
#    - Solve equations to get the dipole moment D+
#    - put s small E-field in direction I-Delta
#    - Solve equations to get the dipole moment D-
#    - Polarizability alpha(I,J). (D+(I)-D-(I))/(2Delta)	
#    - Diagonalize to get eigenValues, eigenVectors, a_iso
#
# 3. Print polarisability
#
# NOTE: We use the last dipole_moment found in the file. If a specific
#       one is needed the 'myProperty' option should be accordingly
#       adjusted and remove the 'property_Base = true' option.
#
# NOTE: This is not the most general version. It is adjusted for testsuite
#       with 'method' and 'mp2' blocks.
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------    Variables    ------------------------------
#
# --- Variables to be adjusted (e.g. using 'with' ---------------------
Variable molecule    = "h2o.xyz";        # xyz file with coordinates
Variable charge      = 0;
Variable mult        = 1;
Variable method      = "HF";
Variable basis       = " " ;
Variable restOfInput = "NoFrozenCore VeryTightSCF";
Variable E_Field     = 0.0001;           # Size of Electric field
Variable myProperty  = "Dipole_Moment_Total";
Variable removeFiles = true;             # Remove files in the end of the calculation
# ---------------------------------------------------------------------
# -------------- Rest of the variables --------------------------------
Variable D_Free, D_Minus, D_Plus, a[3][3];    #dipole moment and polarizability
Variable aEigenValues[3], aEigenVectors[3][3], a_iso;
Variable FFieldStringPlus, FFieldStringMinus;
Variable res = -1;

# ----------------------------------------------------------------------
# Field Free 
# ----------------------------------------------------------------------
New_Step
  !&{method} &{basis} &{restOfInput}
  %Method
    z_tol 1e-8
  End
  %MP2
    Density Relaxed
  End
  #*xyzFile &{charge} &{mult} &{molecule}
Step_End
res = D_Free.readProperty(propertyName=myProperty, property_Base=true);

# ------------------------------------------------------------------
# Loop over the x, y, z directions and create the appropriate string
# ------------------------------------------------------------------
for direction from 0 to 2 Do
  #Create the appropriate direction oriented field string
  if (direction = 0) then          #( X direction)
    write2String(FFieldStringPlus,  " %lf, 0.0, 0.0", E_Field);
    write2String(FFieldStringMinus, "-%lf, 0.0, 0.0", E_Field);
  else if (direction = 1) then     #( Y direction)
    write2String(FFieldStringPlus,  " 0.0,  %lf, 0.0", E_Field); 
    write2String(FFieldStringMinus, " 0.0, -%lf, 0.0", E_Field);
  else                             #( Z direction)
    write2String(FFieldStringPlus,  " 0.0,  0.0,  %lf", E_Field);
    write2String(FFieldStringMinus, " 0.0,  0.0, -%lf", E_Field);
  EndIf
  # ----------------------------------------
  # Perform the calculations. 
  # First the plus (+) one  
  # ----------------------------------------
  ReadMOs(1);
  New_Step
    !&{method} &{basis} &{restOfInput}
    %SCF
      EField = &{FFieldStringPlus}
    End
    %Method
      z_tol 1e-8
    End
    %MP2
      Density Relaxed
    End
  Step_End
  res = D_Plus.readProperty(propertyName=myProperty, property_Base=true);
  
  # ----------------------------------------
  # And the minus (-) one
  # ----------------------------------------
  ReadMOs(1);
  New_Step
    !&{method} &{basis} &{restOfInput}
    %SCF
      EField = &{FFieldStringMinus}
    End
    %Method
      z_tol 1e-8
    End
    %MP2
      Density Relaxed
    End
  Step_End
  res = D_Minus.readProperty(propertyName=myProperty, property_Base=true);

  # ------------------------------------------
  # Construct and store SCF polarizability
  # ------------------------------------------
  a[direction][0] = (D_Plus[0]-D_Minus[0])/(2*E_Field);
  a[direction][1] = (D_Plus[1]-D_Minus[1])/(2*E_Field);
  a[direction][2] = (D_Plus[2]-D_Minus[2])/(2*E_Field);

EndFor
# -----------------------------------------
# Diagonalize
# -----------------------------------------
a.Diagonalize(aEigenValues, aEigenVectors);

# -----------------------------------------
# Do some printing
# -----------------------------------------
print( "\n\n");
print( " -------------------------------------------------------\n");
print( "                   COMPOUND                             \n");
print( " Semi analytical calculation of polarizability\n");
print( " -------------------------------------------------------\n");
print( " Method:  %s\n", method);
print( " Basis :  %s\n", basis);
print( " The electric field perturbation used was:    %.5lf a.u.\n", E_Field);
print( " \n\n");

print( " -------------------------------------------------------\n");
print( " Raw electric semi-analytical polarizability tensor\n");
print( " -------------------------------------------------------\n");
For i from 0 to 2 Do
  print("%13.8lf  %13.8lf  %13.8lf\n", a[i][0], a[i][1], a[i][2]);
EndFor
print( " -------------------------------------------------------\n");
print("\n");

print( " -------------------------------------------------------\n");
print( " Raw electric semi-analytical polarizability Eigenvalues\n");
print( " -------------------------------------------------------\n");
print("%13.8lf  %13.8lf  %13.8lf\n", aEigenValues[0], aEigenValues[1], aEigenValues[2]);
print( " -------------------------------------------------------\n");
print("\n");

print( " -------------------------------------------------------\n");
print( " Raw electric semi-analytical polarizability Eigenvectors\n");
print( " -------------------------------------------------------\n");
For i from 0 to 2 Do
  print("%13.8lf  %13.8lf  %13.8lf\n", aEigenVectors[i][0], aEigenVectors[i][1], aEigenVectors[i][2]);
EndFor

print( "\n a isotropic value : %.5lf\n", (aEigenValues[0]+aEigenValues[1]+aEigenValues[2])/3.0);
# 
#
# ---------------------------------------------------
#  Maybe remove unneccesary files
# ---------------------------------------------------
if (removeFiles) then
  sys_cmd("rm *_Compound_* *.bas* ");
EndIf

End
```
关于复合任务的更多细节，见 [sec:workflowsautomatization.compound](#sec:workflowsautomatization.compound)。

对于其他相关方法（连弛豫密度都没有的），只能采用完全数值方法
（使用复合脚本），并且需要极其严格的收敛。

请注意，极化率计算对基组有更高的要求。
对这一性质来说相当不错的基组是 Sadlej 基组（见
[sec:essentialelements.basisset.builtin](#sec:essentialelements.basisset.builtin)）。与电性质相关，或许值得一提的是，
ORCA 中可以进行有限电场计算。关于这类计算的更多信息见
[sec:essentialelements.finEfield](#sec:essentialelements.finEfield)。

静态超极化率张量作为能量对三个偶极微扰的解析三阶导数计算。
目前可用于 SCF 方法（HF、DFT）。例如，考虑以下输入：

```orcainput
! RHF def2-SVP TightSCF

%elprop
  hyperpol 1
end

*xyz 0 1
  C       0.000000     -0.000000     -0.528012
  O      -0.000000      0.000000      0.650528
  H      -0.000000      0.931690     -1.116318
  H      -0.000000     -0.931690     -1.116318
*
```

超极化率可以在输出中找到，打印为
```orca
---------------------------------------------------
         STATIC HYPERPOLARIZABILITY TENSOR
---------------------------------------------------

Method             : SCF
Type of density    : Electron Density
Type of derivative : Electric Field (Direction=X)
Multiplicity       :   1
Irrep              :   0
Basis              : AO

  The raw Cartesian tensor (atomic units):

     ( x x x ):          -0.000000
     ( x x y ):          -0.000000
     ( x x z ):           7.076938
     ( x y x ):          -0.000000
     ( x y y ):          -0.000000
     ( x y z ):          -0.000000
     ( x z x ):           7.076938
     ( x z y ):          -0.000000
     ( x z z ):          -0.000000
     ( y x x ):          -0.000000
     ( y x y ):          -0.000000
     ( y x z ):          -0.000000
     ( y y x ):          -0.000000
     ( y y y ):           0.000000
     ( y y z ):          49.371503
     ( y z x ):          -0.000000
     ( y z y ):          49.371503
     ( y z z ):           0.000000
     ( z x x ):           7.076938
     ( z x y ):          -0.000000
     ( z x z ):          -0.000000
     ( z y x ):          -0.000000
     ( z y y ):          49.371503
     ( z y z ):           0.000000
     ( z z x ):          -0.000000
     ( z z y ):           0.000000
     ( z z z ):          44.368713
```

<a id="sec:spectroscopyproperties.atomicelectric"></a>
## 原子偶极矩与极化率（Atomic Dipole Moment and Polarizabilities）

ORCA 包含一种机制，可将电性质分解为原子贡献。
简而言之，该方法依赖于将实空间划分为原子区域。
这些区域由原子 A 的平滑权重函数定义

$$

f_{A}\left( \mathbf{r} \right) = \frac{\varrho_{A}^{(0)}(\mathbf{r})}{\sum_{B}^{}{\varrho_{B}^{(0)}(\mathbf{r})}}

$$

量 $\varrho_{A}^{(0)}(r)$ 是中性原子的球对称原子密度
（在足够大的 Gaussian s 函数集合中展开），
这些密度在代码中以预表形式存在。

利用这些分割函数，原子多极矩定义为：

$$

Q_{l}^{m}(A) = \sum_{\mu\nu}P_{\mu\nu}\int{\mu(\mathbf{r}){\widehat{q}}_{l}^{m}\nu(\mathbf{r})f_{A}\left( \mathbf{r} \right)d\mathbf{r}}

$$

这里 **P** 是密度矩阵，${\hat{q}}_{l}^{m}$ 是 l 阶、m 分量
多极矩的算符。例如，对于偶极矩 l=1，m=0,+1,-1。
类似地，对于四极矩 l=2，m=2,1,0,-1,-2，以此类推。
空间上的分割积分通过数值积分执行。在精确数值积分的极限下，
该构造保证原子矩之和等于总的多极矩。由于数值积分会引入小误差，
累积矩

$$

Q_{l}^{m} = \sum_{A}^{}{Q_{l}^{m}(A)}

$$

会与程序同时计算并打印的解析积分矩有小的偏差。

显然，同样的策略也可用于响应性质。
例如，对于极化率，可以将其分解为原子分量：

$$

\alpha_{KL}(A) = - \sum_{\mu\nu}\frac{\partial P_{\mu\nu}}{\partial F_{K}}\int{\mu(\mathbf{r})\mathbf{r}_{L}\nu(\mathbf{r})f_{A}\left( \mathbf{r} \right)d\mathbf{r}}

$$

这里 **F** 是外电场，密度矩阵的导数是相对于该场的响应密度。

要触发此计算，请使用：

```orca
%elprop
Polar true
PolarAtom true
Dipole true
DipoleAtom true
Quadrupole true
QuadrupoleAtom true
end
```

!!! note
    -   原子电性质目前在 SCF 水平上可用于偶极矩、四极矩和极化率
    -   众所周知，带电分子的偶极矩依赖于规范原点。因此，按照这里
        分解偶极矩的方式，原子偶极矩指的是全局原点，带电原子存在
        规范依赖性。因此，在解释这些局域偶极矩时需要谨慎。

论文：
-   Grigorash, D.; Müller, S.; Heid, E.; Neese, F.; Liakos, D.;
    Riplinger, C.; Garcia-Rates, M.; Paricaud, P. Erling H.S.; Smirnova,
    I.; Yan, W. A comprehensive approach to incorporating intermolecular
    dispersion into the openCOSMO-RS model. Part 2: Atomic
    polarizabilities, 2025, submitted 

<a id="sec:spectroscopyproperties.properties.elprop.dynamic"></a>
## 动态电性质（Dynamic Electrical Properties）

在 SCF 水平上，可以使用纯实数或纯虚数频率计算动态（频率相关的）
偶极极化率。
```orca
%elprop
 polar 1
 freq_r 0.08  # purely real frequencies
 #freq_i 0.08 # purely imaginary frequencies 
end
```
在上面的例子中，计算了单个实数频率 0.08 a.u. 的动态偶极极化率张量。
对每个频率，必须对微扰算符的所有分量（电偶极的 3 个笛卡尔分量）
求解线性响应方程。
请注意，虚数频率极化率的计算成本与实数频率极化率相同。
通过简单的围道积分，它们可以用来计算色散系数。

!!! warning
    基于解析微分的动态（频率相关的）偶极第一超极化率
    在 ORCA 中尚不可用。

!!! note
    对于动态（频率相关的）极化率和超极化率，
    数值微分更为复杂[Goncharov2012JCP](../../bibliography.md)。
    目前尚无基于复合脚本的工作流。

<a id="sec:spectroscopyproperties.properties.elprop.keywords"></a>
## Elprop 关键词（Elprop Keywords）

可以在 `%elprop` 输入块中请求一阶（电偶极矩和四极矩）
和二阶（极化率）电性质的计算。二阶性质可以通过求解
CP-SCF（见 [sec:essentialelements.cpscf](#sec:essentialelements.cpscf)）
或 CP-CASSCF（见 [sec:spectroscopyproperties.casscfresp](#sec:spectroscopyproperties.casscfresp)）方程计算。
细节如下：

```orca
%elprop
  Dipole     true
  Quadrupole true
  Polar      true
  PolarVelocity true # polarizability w.r.t. velocity perturbations
  PolarDipQuad  true # dipole-quadrupole polarizability
  PolarQuadQuad true # quadrupole-quadrupole polarizability
  Hyperpol      true # the dip/dip/dip hyperpolarizability
  freq_r 0.00   # purely real frequency (default: static calculation)
  freq_i 0.00   # purely imaginary frequency (default: static calculation)
  Solver  CG    # CG(conjugate gradient)
                # other options: DIIS or POPLE(default)
  MaxDIIS  5    # max. dimension of DIIS method
  Shift   0.2   # level shift used in DIIS solver
  Tol     1e-3  # Convergence of the CP-SCF equations
                # (norm of the residual)
  MaxIter 64    # max. number of iterations in CPSCF
  PrintLevel 2
  Origin  CenterOfElCharge  # center of electronic charge
          CenterOfNucCharge # center of nuclear charge
          CenterOfSpinDens	# center of spin density
          CenterOfMass      # center of mass (default)
          N                 # position of atom N (starting at 0)
          X,Y,Z             # explicit position of the origin
                            # in coordinate input units (Angstrom by default)
  end
```

解析计算极化率最高效、最准确的方法是使用耦合微扰 SCF 方法。
最耗时且最不准确的方法是总能量的数值二阶导数。
请注意，数值微分需要：(a) 紧密甚至非常紧密收敛的 SCF 计算，
以及 (b) 仔细选择的场增量。如果场增量太大，
截断误差会很大，数值将不可靠。另一方面，如果场增量太小，
与有限差分微分相关的数值误差会变得大到不可接受，
以至于整个计算变得无用。
