<a id="sec:workflowsautomatization.compound_examples"></a>
# Compound 示例（Compound Examples）

<a id="sec:workflowsautomatization.compound_examples.introduction"></a>
## 简介（Introduction）

在页面 https://github.com/ORCAQuantumChemistry/CompoundScripts 上有一个 compound 脚本库。

<a id="sec:workflowsautomatization.compound_examples.HelloWorld"></a>
## Hello World

**简介（Introduction）**

这是最简单的脚本，但它指向了 *Compound* 的一个重要特性。即 *Compound* 不必运行真正的“常规”ORCA 计算，也可以用作各种任务的驱动程序，在本例中只是打印一条消息。

**文件名（Filename）**

helloWorld.inp

**SCRIPT**
```orca
%Compound
  print("Hellow World!\n");
EndRun
```

## New Job

**简介（Introduction）**

ORCA 中将来会被弃用、且不应再使用的特性之一是 *'New_Job'* 特性。本脚本是一个简单示例，展示如何用 *Compound* 仅运行一系列计算。

**文件名（Filename）**

replaceNewJob.inp

**SCRIPT**
```mol
title: structure 1
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
4
structure (0 1)
H           0.0          0.0          0.0
H           0.0          0.0          0.8
H           0.0          0.0          0.0
H           0.0          0.0          0.8
--- input ---
# This is a small script thas shows how
# 'Compound' can replace the previous
# ORCA '$New_Job' feature
%Compound
  # ------------------------------------
  # First job
  # ------------------------------------
  New_Step
    !BP86 
    *xyz 0 1
      H 0.0 0.0 0.0
      H 0.0 0.0 0.8
    *
  Step_End
  # ------------------------------------
  # Second job with same goemetry
  # but different functional
  # ------------------------------------
  New_Step
    !B3LYP
    *xyz 0 1
      H 0.0 0.0 0.0
      H 0.0 0.0 0.8
    *
  Step_End
EndRun
```

**注释（Comments）**

从 *Compound* 的角度来看，本脚本中的语法并非最高效的写法。它可以改写成更紧凑、更清晰、更通用的形式。不过，这只是一个示例，说明 *Compound* 如何取代使用了即将弃用的 *'New_Job'* 特性的较旧 ORCA 计算。

## 高精度（High Accuracy）

**简介（Introduction）**

这是一个利用 N. J. DeYonker、T. R. Cundari 和 A. K. Wilson 所提出方案的脚本，发表于：J. Chem. Phys. 124, 114104 (2006)。该脚本计算分子的精确总能量。

**文件名（Filename）**

ccCA_CBS_2.cmp

**SCRIPT**
```mol
title: structure 2
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
4
structure (0 1)
H           0.0          0.0          0.0
H           0.0          0.0          0.8
H           0.0          0.0          0.0
H           0.0          0.0          0.8
--- input ---
# This is a small script thas shows how
# 'Compound' can replace the previous
# ORCA '$New_Job' feature
%Compound
  # ------------------------------------
  # First job
  # ------------------------------------
  New_Step
    !BP86 
    *xyz 0 1
      H 0.0 0.0 0.0
      H 0.0 0.0 0.8
    *
  Step_End
  # ------------------------------------
  # Second job with same goemetry
  # but different functional
  # ------------------------------------
  New_Step
    !B3LYP
    *xyz 0 1
      H 0.0 0.0 0.0
      H 0.0 0.0 0.8
    *
  Step_End
EndRun
```

**注释（Comments）**

有意思的是，在该方案中处理的是总能量，外推时不区分 HF 能量和相关能。

## 扫描（Scan）
**简介（Introduction）**

这是一维几何扫描的示例脚本。它针对 Ne-Ne 键长设置，但可以修改以适应用户的具体需求。

**文件名（Filename）**

scan_1D_1M_1P.cmp

**SCRIPT**
```mol
title: structure 3
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
1
structure
Ne          0.0          0.0          0.0
```

**注释（Comments）**

本脚本有一些有趣的特性。它包含两个变量 *removeFiles* 和 *DoPython*。如果第一个设为 *true*，脚本将使用系统命令删除计算结束后不再需要的文件。后者 *DoPython* 若设为 *true*，则会读取所创建的 *.csv* 文件并写出一个 *python* 文件来绘制结果图。随后它将运行该 python 脚本实际绘图。

## 数值极化率（Numerical polarizabilities）

**简介（Introduction）**

该脚本使用带电场的单点计算来数值计算分子的极化率。

**文件名（Filename）**

numericalPolarizability.cmp

**SCRIPT**
```orca
# Authors: Dimitrios G. Liakos / Frank Neese / Zikuan Wang
# Date   : May of 2024
#
# This is a compound script that calculates the
#  dipole-dipole polarizability tensor numerically
#  using the double derivative of energy.
#
# The idea is the following:
#
# 1 Perform a field free calculation
#
# 2 Loop over directions I=X,Y,Z
#
# 3 Loop over directions J=X,Y,Z
#
#    - put a small Q-field in directions I and J
#    - Solve equations to get the energy for each combination
#    - Polarizability alpha(I,J) =- ( E(+I,+J) - E(+I,-J)-E(-I,+J)+ E(-i,-j)/(4*Field^2)
# 4 Print polarisability
#
# ----------------------------------------------------------------------
# ----------------------    Variables    -------------------------------
# --- Variables to be adjusted (e.g. using 'with' ----------------------
Variable molecule    = "h2o.xyz";
Variable charge      = 0;
Variable mult        = 1;
Variable method      = "HF";
Variable basis       = " ";
Variable restOfInput = "VeryTightSCF";
Variable blocksInput = " ";
Variable E_Field     = 0.0001;
Variable enPropName  = "JOB_Info_Total_En";
Variable removeFiles = true;
# -------------- Rest of the variables --------------------------------
Variable FField[3];
Variable EFree, EPlusPlus, EPlusMinus, EMinusPlus, EMinusMinus, a[3][3];
Variable FFieldStringPlusPlus, FFieldStringPlusMinus;
Variable FFieldStringMinusPlus, FFieldStringMinusMinus;
Variable aEigenValues, aEigenVectors;

# -----------------------------------------
# Calculation without field
# -----------------------------------------
New_Step
  !&{method} &{basis} &{restOfInput}
  &{blocksInput}
  *xyzfile &{charge} &{mult} &{molecule}
Step_End
EFree.ReadProperty(propertyName=enPropName);

# ------------------------------------------------------------
# Loop over the x, y, z directions
# ------------------------------------------------------------
for i from 0 to 2 Do
  for j from 0 to 2 Do
    # ----------------------------------------------------------
    # Create the appropriate direction oriented field string 
    # ----------------------------------------------------------
    # ---------------------- (++) ------------------------------
    for k from 0 to 2 Do
      FField[k] = 0.0;
    EndFor
    FField[i] = FField[i] + E_Field;
    FField[j] = FField[j] + E_Field;
    write2String(FFieldStringPlusPlus,   " %lf,  %lf,  %lf",
    FField[0], FField[1], FField[2]);
    #
    # --------------------- (+-) ------------------------------
    for k from 0 to 2 Do
      FField[k] = 0.0;
    EndFor
    FField[i] = FField[i] + E_Field;
    FField[j] = FField[j] - E_Field;
    write2String(FFieldStringPlusMinus,   " %lf,  %lf,  %lf",
    FField[0], FField[1], FField[2]);
    #
    # --------------------- (-+) ------------------------------
    for k from 0 to 2 Do
      FField[k] = 0.0;
    EndFor
    FField[i] = FField[i] - E_Field;
    FField[j] = FField[j] + E_Field;
    write2String(FFieldStringMinusPlus,   " %lf,  %lf,  %lf",
    FField[0], FField[1], FField[2]);
    #
    # --------------------- (--) ------------------------------
    for k from 0 to 2 Do
      FField[k] = 0.0;
    EndFor
    FField[i] = FField[i] - E_Field;
    FField[j] = FField[j] - E_Field;
    write2String(FFieldStringMinusMinus,   " %lf,  %lf,  %lf",
    FField[0], FField[1], FField[2]);

    # ----------------------------------------
    # Perform the calculations. 
    # The plus_plus (++) one  
    # ----------------------------------------
    ReadMOs(1);
    New_Step
      !&{method} &{basis} &{restOfInput}
      %SCF
        EField = &{FFieldStringPlusPlus}
      End
      &{blocksInput}
    Step_End
    EPlusPlus.readProperty(propertyName=enPropName);
    # ----------------------------------------
    # The plus_minus (+-) one
    # ----------------------------------------
    ReadMOs(1);
    New_Step
      !&{method} &{basis} &{restOfInput}
       %SCF
        EField = &{FFieldStringPlusMinus}
      End
      &{blocksInput}
    Step_End
    EPlusMinus.readProperty(propertyName=enPropName);
    # ----------------------------------------
    # The minus_plus (-+) one  
    # ----------------------------------------
    ReadMOs(1);
    New_Step
      !&{method} &{basis} &{restOfInput}
      %SCF
        EField = &{FFieldStringMinusPlus}
      End
      &{blocksInput}
    Step_End
    EMinusPlus.readProperty(propertyName=enPropName);
    # ----------------------------------------
    # And the minus_minus (--) one
    # ----------------------------------------
    ReadMOs(1);
    New_Step
      !&{method} &{basis} &{restOfInput}
       %SCF
        EField = &{FFieldStringMinusMinus}
      End      
      &{blocksInput}
    Step_End
    EMinusMinus.readProperty(propertyName=enPropName); 
 
    a[i][j] = -(EPlusPlus-EPlusMinus-EMinusPlus+EMinusMinus)/(4*E_Field*E_Field);
  EndFor
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
print( " Numerical calculation of dipole polarizability\n");
print( " -------------------------------------------------------\n");
print( " Molecule    : %s\n", molecule);
print( " charge      : %d\n", charge);
print( " Mult        : %d\n", mult);
print( " Method      : %s\n", method);
print( " Basis       : %s\n", basis);
print( " RestOfInput : %s\n", restOfInput);
print( " BlocksInput : %s\n", blocksInput); 
print( " The electric field perturbation used was:    %.5lf a.u.\n", E_Field);
print( " \n\n");

print( " -------------------------------------------------------\n");
print( " Raw electric dipole  polarizability tensor is:\n");
print( " -------------------------------------------------------\n");
For i from 0 to 2 Do
  print("%13.8lf  %13.8lf  %13.8lf\n", a[i][0], a[i][1], a[i][2]);
EndFor
print( " -------------------------------------------------------\n");
print("\n");

print( " -------------------------------------------------------\n");
print( " Raw electric dipole polarizability Eigenvalues\n");
print( " -------------------------------------------------------\n");
print("%13.8lf  %13.8lf  %13.8lf\n", aEigenValues[0], aEigenValues[1], aEigenValues[2]);
print( " -------------------------------------------------------\n");
print("\n");

print( " -------------------------------------------------------\n");
print( " Raw electric dipole polarizability Eigenvectors\n");
print( " -------------------------------------------------------\n");
For i from 0 to 2 Do
  print("%13.8lf  %13.8lf  %13.8lf\n", aEigenVectors[i][0], aEigenVectors[i][1], aEigenVectors[i][2]);
EndFor

print( "\n a isotropic value : %.5lf\n", (aEigenValues[0]+aEigenValues[1]+aEigenValues[2])/3.0);
print( " -------------------------------------------------------\n");
print("\n\n");
# 
#
# ---------------------------------------------------
#  Maybe remove unneccesary files
# ---------------------------------------------------
if (removeFiles) then
  sys_cmd("rm *_Compound_* *.bas* ");
EndIf
#
End
```

**注释（Comments）**

在本脚本中我们还使用了 *Compound* 中提供的线性代数 *diagonalize* 函数。

<a id="sec:workflowsautomatization.compound_examples.iterativeopt"></a>
## 迭代优化（Iterative optimization）
**简介（Introduction）**

该脚本执行几何优化，然后运行频率计算；如果存在虚频，它会基于 Hessian 调整几何结构并再次优化。

**文件名（Filename）**

iterativeOptimization.cmp

**SCRIPT**
```orca
# Author: Dimitrios G. Liakos and Franke Neese
# Date  : May/June of 2024
#
# *************************************** DESCRIPTION ***********************************************
# iterative Optimization protocol to find structure with no negative
# frequencies (e.g. real minima)
#
# Step 1. Run a single point calculation (we need it for the first property file)
#
# Step 1. Loop and perform calculations with (optimization and frequencies)
#
# Step 2. Check the frequencies. If there are negative ones use the hessian 
#         of the appropriate normal mode to adjust the geometry
#
# ------ Variables to adjust (e.g. using 'with') -------------------
Variable method          = "HF"; #"HF-3c";
Variable MaxNTries       =  25;   # Number of maximum tries
Variable CutOff          = -10.0; # CutOff for a negative frequency
Variable scaling         = 0.6;   # Scaling factor for normal mode
Variable NNegativeTarget = 0;     # Number of negative frequencies we allow
Variable myFilename      = "xyzInput.xyz";
Variable charge          = 0;
Variable multiplicity    = 2;
# ------------------------------------------------------------------
# ------            Rest of variables            -------------------  
Geometry myGeom;
Variable freqs, modes;
Variable res = -1;
Variable NNegative =   0;
Variable OptDone;

# -----------------------------------------------------------
# Perform a single point calculation. We need it for 
# the initial geometry from the property file
# -----------------------------------------------------------
New_Step
  !&{method}
Step_End
myGeom.Read();
myGeom.WriteXYZFile(filename=myFilename);

# -----------------------------------------------------------
# Start a for loop over number of tries
# ----------------------------------------------------------
For itry From 1 To maxNTries Do
  # --------------------------------------------
  # Perform a geometry optimization/Frequency calculation
  # --------------------------------------------
  New_Step
    ! &{method} freq Opt
    *xyzfile &{charge} &{multiplicity} &{myFilename}
  Step_End
  res = freqs.readProperty(propertyName = "THERMO_FREQS");
  res = modes.readProperty(propertyName = "HESSIAN_MODES");
  myGeom.Read();

  # ---------------------------------------------
  #  check for sufficiently negative frequencies
  # ---------------------------------------------
  NNegative = 0;
  For ifreq From 0 to freqs.GetSize()-1 Do
    if ( freqs[ifreq] < CutOff )  then
       myGeom.FollowNormalMode(vibrationSN=ifreq, scalingFactor=scaling);
       NNegative = NNegative + 1;
    endif
  endfor
  myGeom.WriteXYZFile(filename=myFilename);
  If ( NNegative <= NNegativeTarget ) then
    goto OptDone;
  endif
endfor

# -----------------------------------------------------------------
# Either found correct geometry or reached maximum number of tries.
# -----------------------------------------------------------------
OptDone :
if (NNegative > NNegativeTarget) then
  print("ERROR The program did not find a structure with the desired\n number of imaginary frequencies.\n There are %9.3lf negative frequencies after %3d steps", NNegative,itry);
else
  print("\nSUCCESS optimized structure with (%d) negative\n frequencies found after %3d steps", NNegative, itry);
endif

End
```

## 梯度外推（Gradient extrapolation）

**简介（Introduction）**

该脚本对分子的梯度进行外推。它使用两点外推，其中梯度的 Hartree-Fock 部分和相关部分分别外推。这为使用外推梯度进行几何优化开辟了道路。

**文件名（Filename）**

gradientExtrapolation.cmp

**SCRIPT**
```orca
#   Author: Dimitrios G. Liakos and Frank Neese
#   Date  : May of 2024
#
#   This is a compound file that extrapolates the
#   energy gradients to Complete Basis Set Limit (CBS).
#
#   STEPS:
#   Step1 : Run HF calculation with small basis set
#          Read scfGradX and scfEnX
#   Step2 : Run Correlation calculation with small basis set
#          Read totalGradX and totalEnX
#   Step3 : Calculate the gradient differene to get
#          the corrGradX (only the correlation part)
#   Step4 : Run HF calculation with big basis set
#          Read scfGradY and scfEnY
#   Step5 : Run correlation calculation with big basis set
#          Read totalGradY and totalEnY
#   Step6 : Calculate the gradient difference with the
#          big basis set to get corrGradY
#   Step7 : Evaluate scfGradCBS and scfEnCBS
#          using scfGradX and scfGradY
#   Step8 : Evaluate corrGradCBS using 
#          corrGradX and corrGradY
#   Step9 : Add scfGradCBS and corrGradCBS to get
#          totalGradCBS
#   Step10: If needed, create an ORCA engrad file
#
#
#   NOTE: It works with an xyz file the name of which we should provide.
#         using the variable initialXYZFilename.
#
#   We extrapolate the SCF part using the scheme 
#     proposed in: J. Phys. Chem. 129, 184116, 2008
#       E_SCF(X) = E_SCF(CBS)+Aexp(-a*SQRT(X))
#
#   We extrapolate the correlation part using the schem 
#     proposed in: J. Chem. Phys. 1997, 106, 9639
#   E_CBS(CORR)=(X^b*E_X(CORR)-Y^b*E_Y(CORR))/(X^b-Y^b)

#   We use alpha and beta exponents proposed in:
#     J. Chem. Theory Comput., 7, 33-43 (2011)
# ----------------------    Variables    -------------------------------
# --- Variables to be adjusted (e.g. using 'with' ----------------------
Variable Molecule           = "initial.xyz";   # xyz file of the initial structure
Variable charge             = 0;               # Charge
Variable multiplicity       = 1;               # Spin multiplicity
Variable method             = "MP2";           # The method we use for the calculation
Variable LowerBasis         = "cc-pVDZ";       # Small basis set
Variable UpperBasis         = "cc-pVTZ";       # Big basis set
Variable restOfInput        = "EnGrad ";       # The rest of the simple input
Variable addCorrelation     = true;            # If we have a correlation part
Variable scfEnPropName      = "MP2_Ref_Energy";  # The name of the property for the SCFenergy
Variable corrEnPropName     = "MP2_Corr_Energy"; # The name of the property for the correlation energy
Variable LowerCardinal      = 2;               # Cardinal number of small basis set
Variable UpperCardinal      = 3;               # Cardinal number of big basis set
Variable alpha              = 4.420;           # Exponent for SCF extrapolation
Variable beta               = 2.460;           # Exponent for corrleation extrapolation
Variable enGradFilename     = "result.engrad"; # Filename of the ORCA engrad file
Variable produceEnGradFile  = true;            # Produce an ORCA engrad file   
# ---------------------------------------------------------------------
# -------------- Rest of the variables --------------------------------
Geometry myGeom;
Variable scfGradX, scfGradY;                   # SCF Gradients
Variable scfEnX, scfEnY, scfEnCBS;             # SCF energies
Variable corrEnX, corrEnY, corrEnCBS;          # Correlation enegies
Variable totalGradX, totalGradY;               # Total Gradients
Variable eX = 0.0;
Variable eY = 0.0;
Variable res = -1;

Variable denominator = 0.0;
Variable gradX = 0.0, gradY = 0.0, gradCBS=0.0;
Variable nAtoms = 0;
Variable EnGradFile;
Variable Cartesians, AtomicNumbers;

# -------------------------------------------------------------------
# Step 1. SCF Calculation with small basis set (X)
# -------------------------------------------------------------------
New_Step
  ! HF &{LowerBasis} &{restOfInput}
  *xyzfile &{charge} &{multiplicity} &{Molecule}
Step_end
res = scfEnX.readProperty(propertyName="SCF_Energy");
res = scfGradX.readProperty(propertyName="Nuclear_Gradient", Property_Base=true);
myGeom.Read();
nAtoms = myGeom.GetNumOfAtoms();

# ------------------------------------------------------------------
# Step 2. Initialize rest of the variables
# ------------------------------------------------------------------
Variable corrGradX[3*nAtoms];   # Correlation part of gradient with basis X
Variable corrGradY[3*nAtoms];   # Correlation part of gradient with basis Y
Variable corrGradCBS[3*nAtoms]; # CBS estimation of correlation part of the gradient                            
Variable scfGradCBS[3*nAtoms];  # CBS estimation of SCF part of the gradient 
Variable totalGradCBS[3*nAtoms];# CBS estimation of total gradient

# -------------------------------------------------
# Step3. Correlation Calculation with small basis set (X)
# -------------------------------------------------
if (addCorrelation) then
  New_Step
    ! &{method} &{LowerBasis} &{restOfInput}
  Step_end
  res = scfEnX.readProperty(propertyName=scfEnPropName);
  res = corrEnX.readProperty(propertyName=corrEnPropName);
  res = totalGradX.readProperty(propertyName="Nuclear_Gradient", Property_Base=true);

  # -------------------------------------------------
  # Evaluate correlation gradient with small basis set (X)
  # -------------------------------------------------
  corrGradX =mat_p_mat(1, totalGradX, -1, scfGradX);
EndIf

# -------------------------------------------------
# Step4. SCF Calculation with large basis set (Y)
# -------------------------------------------------
New_Step
  !HF &{UpperBasis} &{restOfInput}
Step_End
res = scfEnY.readProperty(propertyName="SCF_Energy");
res = scfGradY.readProperty(propertyName="Nuclear_Gradient", Property_Base=true);

# -------------------------------------------------
# Step5. Correlation calculation with large basis set (Y)
# -------------------------------------------------
if (addCorrelation) then
  New_Step
    ! &{method} &{UpperBasis} &{restOfInput}
  Step_end
  res = scfEnY.readProperty(propertyName=scfEnPropName);
  res = corrEnY.readProperty(propertyName=corrEnPropName);
  res = totalGradY.readProperty(propertyName="Nuclear_Gradient", Property_Base=true);

  # -------------------------------------------------
  # Evaluate correlation gradient with big basis set Y
  # -------------------------------------------------
  corrGradY = mat_p_mat(1, totalGradY, -1, scfGradY);
EndIf

# -------------------------------------------------
# Step6. Extrapolate the SCF part of the gradient and energy
# -------------------------------------------------
eX               = exp(-alpha * sqrt(LowerCardinal));
eY               = exp(-alpha * sqrt(UpperCardinal));
denominator      = eY-eX;

scfEnCBS    = (scfEnX*eY - scfEnY*eX)/(eY-eX);
for i from 0 to scfGradX.GetSize()-1 Do
  gradX = scfGradX[i];
  gradY = scfGradY[i];

  scfGradCBS[i]  = (gradX * eY - gradY * eX)/denominator;
endFor

if (addCorrelation) then
  # -------------------------------------------------
  # Step7. Extrapolate the correlation part of the gradient and energy
  # -------------------------------------------------
  denominator = LowerCardinal^(beta)-(UpperCardinal)^(beta);

  corrEnCBS =  (LowerCardinal^(beta)*corrEnX-(UpperCardinal)^(beta)*corrEnY)/denominator;
  for i from 0 to scfGradX.GetSize()-1 Do
    gradX = corrGradX[i];
    gradY = corrGradY[i];

    corrGradCBS[i] = (LowerCardinal^(beta)*gradX-(UpperCardinal)^(beta)*gradY)/denominator;
  endFor

  # -------------------------------------------------
  # Add SCF and correlation part to get total CBS extrapolated values
  # -------------------------------------------------
  totalGradCBS = mat_p_mat( 1, scfGradCBS, 1, corrGradCBS);
EndIf

# -------------------------------------------------
# Step8. Present the results
# -------------------------------------------------
print( "\n\n\n");
print( "--------------------------------------------------------\n");
print( "             Compound Extrapolation of Gradient         \n");
print( "--------------------------------------------------------\n");
print( "Number of atoms       : %d\n", nAtoms);
print( "Lower basis set       : %s\n", LowerBasis);
print( "Upper basis set       : %s\n", UpperBasis);
print( "Alpha                 : %.2lf\n", alpha);
print( "Beta                  : %.2lf\n", beta);
print( "Lower Cardinal number : %d\n", LowerCardinal);
print( "Upper Cardinal number : %d\n", UpperCardinal);
print( "Method                : %s\n", method); 
print( "AddCorrelation        : %s\n", AddCorrelation.GetString());
print( "Produce EnGrad File   : %s\n", produceEnGradFile.GetString());
print( "\n\n");
print( "SCF Energy with small basis set         : %.12e\n", scfEnX);
print( "SCF Energy with big basis set           : %.12e\n", scfEnY);
print( "Extrapolated SCF energy                 : %.12e\n", scfEnCBS);
print("\n\n");
if (addCorrelation) then
  print( "Correlation Energy with small basis set : %.12e\n", corrEnX);
  print( "Correlation Energy with big basis set   : %.12e\n", corrEnY);
  print( "Extrapolated correlation  energy        : %.12e\n", corrEnCBS);
  print("\n\n");
  print( "Total Energy with small basis set : %.12e\n", scfEnX   + corrEnX);
  print( "Total Energy with big basis set   : %.12e\n", scfEnY   + corrEnY);
  print( "Extrapolated Total energy         : %.12e\n", scfEnCBS + corrEnCBS);
  print("\n\n");
else
  print( "Total Energy with small basis set : %.12e\n", scfEnX);
  print( "Total Energy with big basis set   : %.12e\n", scfEnY);
  print( "Extrapolated Total energy         : %.12e\n", scfEnCBS);
  print("\n\n");
EndIf

print( "----------------------------------------------------------------\n");
print( "SCF Gradient with basis set: %s\n", LowerBasis );
print( "----------------------------------------------------------------\n");
print( "Atom     %20s     %20s     %20s\n", "X", "Y", "Z"); 
for i from 0 to nAtoms-1 Do
  print("%4d     %20lf     %20lf     %20lf\n", i, scfGradX[3*i], scfGradX[3*i+1], scfGradX[3*i+2]);
EndFor
if (addCorrelation) then
  print( "----------------------------------------------------------------\n");
  print( "Correlation Gradient with basis set: %s\n", LowerBasis );
  print( "----------------------------------------------------------------\n");
  print( "Atom     %20s     %20s     %20s\n", "X", "Y", "Z");
  for i from 0 to nAtoms-1 Do
    print("%4d     %20lf     %20lf     %20lf\n", i, corrGradX[3*i], corrGradX[3*i+1], corrGradX[3*i+2]);
  EndFor

  print( "----------------------------------------------------------------\n");
  print( "Total Gradient with basis set: %s\n", LowerBasis );
  print( "----------------------------------------------------------------\n");
  print( "Atom     %20s     %20s     %20s\n", "X", "Y", "Z");
  for i from 0 to nAtoms-1 Do
    print("%4d     %20lf     %20lf     %20lf\n", i, totalGradX[3*i], totalGradX[3*i+1], totalGradX[3*i+2]);
  EndFor
EndIf

print( "----------------------------------------------------------------\n");
print( "SCF Gradient with basis set: %s\n", UpperBasis );
print( "----------------------------------------------------------------\n");
print( "Atom     %20s     %20s     %20s\n", "X", "Y", "Z");
for i from 0 to nAtoms-1 Do
  print("%4d     %20lf     %20lf     %20lf\n", i, scfGradY[3*i], scfGradY[3*i+1], scfGradY[3*i+2]);
EndFor

if (addCorrelation) then
  print( "----------------------------------------------------------------\n");
  print( "Correlation gradient with basis set: %s\n", UpperBasis );
  print( "----------------------------------------------------------------\n");
  print( "Atom     %20s     %20s     %20s\n", "X", "Y", "Z");
  for i from 0 to nAtoms-1 Do
    print("%4d     %20lf     %20lf     %20lf\n", i, corrGradY[3*i], corrGradY[3*i+1], corrGradY[3*i+2]);
  EndFor
  print( "----------------------------------------------------------------\n");
  print( "Total Gradient with basis set: %s\n", UpperBasis );
  print( "----------------------------------------------------------------\n");
  print( "Atom     %20s     %20s     %20s\n", "X", "Y", "Z");
  for i from 0 to nAtoms-1 Do
    print("%4d     %20lf     %20lf     %20lf\n", i, totalGradY[3*i], totalGradY[3*i+1], totalGradY[3*i+2]);
  EndFor 
EndIf

print( "----------------------------------------------------------------\n");
print( "Extrapolated SCF part of the Gradient:\n" );
print( "----------------------------------------------------------------\n");
print( "Atom     %20s     %20s     %20s\n", "X", "Y", "Z");
for i from 0 to nAtoms-1 Do
  print("%4d     %20lf     %20lf     %20lf\n", i, scfGradCBS[3*i], scfGradCBS[3*i+1], scfGradCBS[3*i+2]);
EndFor

if (addCorrelation) then
  print( "----------------------------------------------------------------\n");
  print( "Correlation Gradient with basis set:\n" );
  print( "----------------------------------------------------------------\n");
  print( "Atom     %20s     %20s     %20s\n", "X", "Y", "Z");
  for i from 0 to nAtoms-1 Do
    print("%4d     %20lf     %20lf     %20lf\n", i, corrGradCBS[3*i], corrGradCBS[3*i+1], corrGradCBS[3*i+2]);
  EndFor
  print( "----------------------------------------------------------------\n");
  print( "Total Gradient with basis set:\n" );
  print( "----------------------------------------------------------------\n");
  print( "Atom     %20s     %20s     %20s\n", "X", "Y", "Z");
  for i from 0 to nAtoms-1 Do
    print("%4d     %20lf     %20lf     %20lf\n", i, totalGradCBS[3*i], totalGradCBS[3*i+1], totalGradCBS[3*i+2]);
  EndFor
EndIf
print( "----------------------------------------------------------------\n");

if (produceEnGradFile) then
  # ------------------------------------------
  # Read the geometry of the last calculation
  # ------------------------------------------
  myGeom.Read();
  Cartesians = myGeom.GetCartesians();
  atomicNumbers = myGeom.GetAtomicNumbers();
  EnGradFile = openFile(enGradFilename, "w");
  Write2File(EnGradFile, "\n\n\n");
  Write2File(EnGradFile, " %d\n", nAtoms);
  Write2File(EnGradFile, "\n\n\n");
  if (addCorrelation) then
    Write2File(EnGradFile, " %.12lf\n", scfEnCBS + corrEnCBS);
  else
    Write2File(EnGradFile, " %.12lf\n", scfEnCBS);
  EndIf
  Write2File(EnGradFile, "\n\n\n");
  for i from 0 to 3*nAtoms-1 Do
    if (addCorrelation) then
      Write2File(EnGradFile, "     %20.12lf\n", totalGradCBS[i]);
    else
      Write2File(EnGradFile, "     %20.12lf\n", scfGradCBS[i]);
    EndIf
  EndFor
  Write2File(EnGradFile, "\n\n\n");
  for i from 0 to nAtoms-1 Do
    Write2File(EnGradFile, "%5d  %12.8lf  %12.8lf   %12.8lf\n", atomicNumbers[i], cartesians[i][0], cartesians[i][1], cartesians[i][2]);
  EndFor
  closeFile(EnGradFile);

EndIf

End
```

**注释（Comments）**

## BSSE 优化（BSSE Optimization）

**简介（Introduction）**

该脚本使用经过基组重叠误差（Basis Set Superposition Error，BSSE）校正的梯度来优化分子几何结构。基本步骤是使用第二个脚本来计算经 BSSE 校正的梯度。

**文件名（Filename）**

BSSEOptimization.cmp

**SCRIPT**
```orca
# Author:  Frank Neese and Dimitrios G. Liakos
# Date  :  May of 2024 
# ---------------------------------------------------
#
# This is a script that will use a compound script to 
#   calculate BSSE corrected gradients and use them
#   in combination with ORCA External Optimizer to
#   perform a geometry optimization. 
#
# We perform the following steps.
# 1. Choose a compound script that calculates the BSSE
#    corrected gradient.
#    We achieve this with the compoundFilename
#
# 2. Create a script to run an ORCA calculalation with
#    the external optimizer and the BSSE cprrected 
#    gradient. We do that by running a script that runs
#    an ORCA calculation that calculates the gradient
#    and then copy this gradient file back to the expected
#    name
#
# 3. Make a normal ORCA New_Step that calls the external
#    optimizer
#
# NOTE: Depending on the chosen method the property names of 
#       myPropName has to be adjusted. For the gradient we do 
#       not have this problem because we read the last 
#       available in the corresponding property file.
#
# NOTE: Variable baseFilename should have the name of the calling
#       orca input file!
#
# ----------------------    Variables    -------------------------------
# --- Variables to be adjusted (e.g. using 'with' ----------------------
Variable molecule           = "01.xyz";         # xyz file of the initial structure
Variable method             = "BP86";            # The method we use for the calculation
Variable basis              = " ";               # The basis set
Variable restOfInput        = "";                # The rest of the simple input
Variable charge             = 0;                 # Charge
Variable mult               = 1;                 # Spin multiplicity
Variable myPropName         = "SCF_Energy";      # The name of the property for the energy
variable myFilename         = "compoundBSSE";    # Name for the created xyz files
Variable baseFilename       = "run";
Variable gradCreateFile     = "BSSEGradient.cmp";# The compound script that extrapolates the gradient  
Variable DoOptimization     = false;             # Optimize the monomers or not
Variable produceEnGradFile  = true;              # Produce an ORCA engrad file   
Variable enGradFilename     = "result.engrad";   # Filename of the ORCA engrad file
# -------------------------------------------------------
#
#           Variables for the driver script
Variable createDriverScript = true;            # The shell script driver
Variable driverScript;                         # A script to create the extrapolated energy gradient
Variable driverScriptName   = "runningScript";
Variable submitCommand      = "orca";
# --------------------------------------------------------

# --------------------------------------------------------
#
#           Variables for the ORCA input
Variable createORCAInput = true;
Variable orcaInput;                           # The ORCA input for the gradient extrapolation
Variable orcaInputName  = "runGradient.inp";
# --------------------------------------------------------

# ------------------------------------------------
# 1. Maybe Create the necessary driver script  
#    for the external optimizer and make it executable
#    NOTE: This will depenend on the operating system
# -------------------------------------------------
if (createDriverScript) then
  driverScript = openFile(driverScriptName, "w");
  write2File(driverScript, "source ~/.bashrc\n");
  write2File(driverScript, "%s %s\n", submitCommand, orcaInputName );
  write2File(driverScript, "cp %s  %s_Compound_1_EXT.engrad\n", engradFilename, baseFilename);
  closeFile(driverScript);
  sys_cmd("chmod +x %s",driverScriptName);
EndIf

# ------------------------------------------------
# 2. Maybe Create the ORCA input that will run the 
#    compound script for the gradient extrapolation  
# -------------------------------------------------
if (createORCAInput) then
  orcaInput = openFile(orcaInputName, "w");
  Write2File(orcaInput, "%%Compound \"%s\"\n", gradCreateFile);
  Write2File(orcaInput, "  with\n");
  Write2File(orcaInput, "    molecule          =\"%s_Compound_1_EXT.xyz\"\;\n", baseFilename);
  Write2File(orcaInput, "    charge            = %d\;\n",     charge);
  Write2File(orcaInput, "    mutliplicity      = %d\;\n",     mult);
  Write2File(orcaInput, "    method            = \"%s\"\;\n", method);
  Write2File(orcaInput, "    basis             = \"%s\"\;\n", basis);
  Write2File(orcaInput, "    restOfInput       = \"%s\"\;\n", restOfInput);
  Write2File(orcaInput, "    myPropName        = \"%s\"\;\n", myPropName);
  Write2File(orcaInput, "    myFilename        = \"%s\"\;\n", myFilename);
  Write2File(orcaInput, "    removeFiles       = false\;\n");
  Write2File(orcaInput, "    DoOptimization    = %s\;\n",     DoOptimization.GetString());
  Write2File(orcaInput, "    produceEnGradFile = %s\;\n",     produceEnGradFile.GetString());
  Write2File(orcaInput, "    enGradFilename    = \"%s\"\;\n", enGradFilename); 
  Write2File(orcaInput, "End\n");
  closeFile(orcaInput);
EndIf

# ------------------------------------------------
# 3. Copy the initial XYZ file to the one needed
#    for the external optimizer 
# -------------------------------------------------
sys_cmd("cp %s %s_Compound_1_EXT.xyz", molecule, baseFilename);

# --------------------------------------------------
# 1. Run the driver ORCA input file that calls the
#    External optimizer
# --------------------------------------------------
New_Step
  !ExtOpt Opt 
  *xyzfile &{charge} &{mult} &{baseFilename}_Compound_1_EXT.xyz
  %method
    ProgExt "./&{driverScriptName}"
  End
Step_End

End
```

**注释（Comments）**

初始结构应包含一些 ghost 原子。

## 伞形翻转脚本（Umbrella script）
**简介（Introduction）**

该脚本计算 NH_3 中“伞效应（umbrella effect）”的势能。此外，它还定位势能面上的极小点和极大点。

**文件名（Filename）**

Umbrella.cmp

**SCRIPT**
```orca
# ----------------------------------------------
# Umbrella coordinate mapping for NH3
# Author: Frank Neese
# ----------------------------------------------
variable JobName = "NH3-umbrella";
variable amin    = 50.0;
variable amax    = 130.0;
variable nsteps  = 21;
Variable energies[21];

Variable angle;
Variable JobStep;
Variable JobStep_m;
variable step;

Variable method = "BP86";
Variable basis  = "def2-SVP def2/J";

step  = 1.0*(amax-amin)/(nsteps-1);

# Loop over the number of steps
# ----------------------------
for iang from 0 to nsteps-1 do
  angle    = amin + iang*step;
  JobStep  = iang+1;
  JobStep_m= JobStep-1;
  if (iang>0) then
    Read_Geom(JobStep_m);
    New_step
      ! &{method} &{basis} TightSCF Opt
      %base "&{JobName}.step&{JobStep}"
      %geom constraints
        {A 1 0 2 &{angle} C}
        {A 1 0 3 &{angle} C}
        {A 1 0 4 &{angle} C}
        end
      end

    Step_End
  else
    New_step
      ! &{method} &{basis} TightSCF Opt
      %base "&{JobName}.step&{JobStep}"
      %geom constraints
        {A 1 0 2 &{angle} C}
        {A 1 0 3 &{angle} C}
        {A 1 0 4 &{angle} C}
        end
      end

      * int 0 1
      N 0 0 0 0.0 0.0 0.0
      DA 1 0 0 2.0 0.0 0.0
      H 1 2 0 1.06 &{angle} 0.0
      H 1 2 3 1.06 &{angle} 120.0
      H 1 2 3 1.06 &{angle} 240.0
      *
    Step_End
  endif
   energies[iang].readProperty(propertyName="SCF_ENERGY");
   print(" index: %3d Angle %6.2lf Energy: %16.12lf Eh\n", iang, angle, energies[iang]);
EndFor

# Print a summary at the end of the calculation
# ---------------------------------------------
print("////////////////////////////////////////////////////////\n");
print("// POTENTIAL ENERGY RESULT\n");
print("////////////////////////////////////////////////////////\n");
variable minimum,maximum;
variable Em,E0,Ep;
variable i0,im,ip;
for iang from 0 to nsteps-1 do
  angle   = amin + 1.0*iang*step;
  JobStep = iang+1;
  minimum = 0;
  maximum = 0;
  i0      = iang;
  im      = iang-1;
  ip      = iang+1;
  E0      = energies[i0];
  Em      = E0;
  Ep      = E0;
  if (iang>0 and iang<nsteps-1) then
    Em = energies[im];
    Ep = energies[ip];
  endif
  if (E0<Em and E0<Ep) then minimum=1; endif
  if (E0>Em and E0>Ep) then maximum=1; endif
  if (minimum = 1 ) then
    print(" %3d  %6.2lf %16.12lf (-)\n",JobStep,angle, E0 );
  endif
  if (maximum = 1 ) then
    print(" %3d  %6.2lf %16.12lf (+)\n",JobStep,angle, E0 );
  endif
  if (minimum=0 and maximum=0) then
    print(" %3d  %6.2lf %16.12lf    \n",JobStep,angle, E0 );
  endif
endfor
print("////////////////////////////////////////////////////////\n");

End # end of compound block
```

## 多参考（Multi reference）
**简介（Introduction）**

这是一个计算自由原子中原子电子密度并建立其库的脚本。

**文件名（Filename）**

atomDensities.inp

**SCRIPT**
```orca
# FN 07/2024
#
# A compound script to run calculation on free atoms
# in order to generate a library of electron densities 
#
%compound
   Variable Element = {" ",
                         "H",                               "He",
			 "Li","Be","B" ,"C" ,"N" ,"O" ,"F" ,"Ne"
			 };
   Variable Nact    = {" ",
                         "1" ,                              "0",
			 "1" ,"0" ,"3" ,"4" ,"5" ,"6" ,"7" ,"0"
			 };

   Variable Norb    = {" ",
                         "1" ,                              "0",
			 "1" ,"0" ,"4" ,"4" ,"4" ,"4" ,"4" ,"0"
			 };

   Variable Nroots  = {" ",
                         "1" ,                              "0",
			 "1" ,"0" ,"3" ,"3" ,"1" ,"3" ,"3" ,"0"
			 };
			 
   Variable Charge  = {" ",
                       "0" ,                              "0",
		       "0" ,"0" ,"0" ,"0" ,"0" ,"0" ,"0" ,"0"
		       };

   Variable Mult    =  {" ",
                         "2" ,                              "1",
			 "2" ,"1" ,"2" ,"3" ,"4" ,"3" ,"2" ,"1"
			 };

   Variable HFTyp   = {" ",
                         "UHF",                                                           "RHF",
			 "CASSCF","RHF","CASSCF" ,"CASSCF" ,"CASSCF" ,"CASSCF" ,"CASSCF" ,"RHF"
			 };

   Variable el;
   for el from 1 to Element.GetSize()-1 do
      if (HFTyp[el]="CASSCF") then
        New_Step
	  ! cc-pVDZ VeryTightSCF Conv
	  %base "atom_&{Element[el]}_&{Charge[el]}_&{Mult[el]}"
	  %casscf  nel    = &{Nact[el]};
	           norb   = &{Norb[el]};
		   nroots = &{Nroots[el]};
		   mult   = &{Mult[el]};
		   end
         * xyz &{Charge[el]} &{Mult[el]}
	  &{Element[el]} 0.0  0.0   0.0 
	 *
	Step_end
      else
        New_Step
         ! &{HFTyp[el]} cc-pVDZ VeryTightSCF Conv
	  %base "atom_&{Element[el]}_&{Charge[el]}_&{Mult[el]}" 
         * xyz &{Charge[el]} &{Mult[el]}
	  &{Element[el]} 0.0  0.0   0.0 
	 *
	Step_end
      endif
   endfor

endrun; 
```

**注释（Comments）**

这里值得注意的是，根据所选原子的不同，脚本要么进行 CASSCF 计算（提供诸如电子数和根数等细节参数），要么进行简单的 Hartree-Fock 计算。

## GoTo
**简介（Introduction）**

这是一个简短示例，演示如何在 *Compound* 中使用 *GoTo* 命令。

**文件名（Filename）**

goTo_Example.inp

**SCRIPT**
```orca
# Compound Example on GoTo usage
# Efficient ON/OFF switch

%Compound
  Variable switch="OFF";
  Variable turnOff, turnOn, loopEnd;
  Variable maxIter = 10;
  for i from 0 to maxIter do
    if (switch="ON") then
      GoTo turnOff;
    else
      GoTo turnOn;
    endIf
    turnOff:
      print("Switch: %s\n", switch);
      switch="OFF";
      GoTo loopEnd;
    turnON:
      print("Switch: %s\n", switch);
      switch="ON";
      GoTo loopEnd;
    loopEnd:
  EndFor
End
```
