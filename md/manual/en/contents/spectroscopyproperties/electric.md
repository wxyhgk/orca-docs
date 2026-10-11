```{index} Electrical Properties, Electric Moments, Polarizabilities
```

(sec:spectroscopyproperties.elprop)=
# Electrical Properties - Electric Moments and Polarizabilities

A few basic electric properties can be calculated in ORCA although this
has never been a focal point of development. The properties can be
accessed straightforwardly through the `%elprop` block:

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

The polarizability (dipole-dipole, dipole-quadrupole, quadrupole-quadrupole)
is calculated analytically through solution of the
coupled-perturbed (CP-)SCF equations for HF and DFT runs (see {ref}`sec:essentialelements.cpscf`) 
and through the CP-CASSCF equations for CASSCF runs (see {ref}`sec:spectroscopyproperties.casscfresp`). 
Analytic polarizabilities are also available for CCSD/CCSD(T) (see {ref}`sec:modelchemistries.autoci.autociresp`), RI-MP2 and DLPNO-MP2, as well as
double-hybrid DFT methods. For canonical MP2 one can use AUTOCI for analytic calculations (see
{ref}`sec:modelchemistries.autoci.autociresp`) or differentiate the
analytical dipole moment calculated with relaxed densities. For other
correlation methods only a fully numeric approach is possible.

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

As expected the polarizability tensor is isotropic.

Dipole-quadrupole polarizability tensors are printed as a list of 18 different
components, with the first index running over x,y,z and the second index running
over xx,yy,zz,xy,xz,yz. This is known as the "pure Cartesian" version of the
tensor, although other conventions may exist in the literature that differ from
the ORCA values by a constant factor.

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

After this, the "traceless" version of the tensor is printed, which is usually denoted
by $A_{x,xx}, A_{x,xy}$ etc. in the literature{cite}`McLean1967JCP,Pedersen2011JCC,Yan2020CTP`.
This is the preferred format for
reporting dipole-quadrupole polarizability tensors. Certain references
use the opposite sign convention than reported here, but generally the conventions
of traceless polarizability tensors are more unified than those of pure Cartesian
polarizability tensors.

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

The quadrupole-quadrupole polarizability tensor is similarly printed in both the
pure Cartesian and traceless forms. Again, the traceless form (usually denoted as
$C_{xx,xx}, C_{xx,xy}$ etc.{cite}`McLean1967JCP,Pedersen2011JCC,Yan2020CTP`)
is the preferred format for reporting.

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

:::{note}
-   **Like the quadrupole moments themselves, the dipole-quadrupole and quadrupole-quadrupole
    polarizabilities depend on the gauge origin of the `%elprop` module. The latter can be changed
    using the `Origin` keyword in `%elprop`; see section {ref}`sec:spectroscopyproperties.elprop`.**
:::

For methods that do not support analytic polarizabilities, one can calculate
numeric dipole-dipole and quadrupole-quadrupole polarizabilities, either by
finite differentiation of dipole/quadrupole moments with respect to a finite
dipole/quadrupole electric field, or by double finite differentiation of
the total energy with respect to a finite dipole/quadrupole electric field.
The latter can be done using compound scripts (see {ref}`sec:workflowsautomatization.compound`,
{ref}`sec:workflowsautomatization.compound_examples`).

At the MP2 level, polarizabilities can currently be calculated
analytically using the RI
({ref}`sec:modelchemistries.mp2.rimp2.response`) or DLPNO
({ref}`sec:modelchemistries.mp2.dlpnoresp`) approximations or in
all-electron canonical calculations, but for canonical MP2 with frozen
core orbitals the dipole moment has to be differentiated numerically
in order to obtain the polarizability tensor. In general in such cases, you should keep in mind that tight SCF convergence is necessary in order to not get too much numerical noise in the second derivative. Also, you should experiment with the finite field increment in the numerical differentiation process.

As an example, the following Compound job can be used to calculate the seminumeric polarizability at the MP2 level (replacing the now deprecated usage of `Polar 2`):

```{literalinclude} ../../orca_working_input/ORCA_Test_0798.inp
:language: orca
```

with the file `semiNumericalPolarizability.cmp` containing:

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
For more details on Compound jobs in general, see {ref}`sec:workflowsautomatization.compound`.

For other correlation methods, where not even relaxed densities are
available, only a fully numeric approach (using compounds scripts) is
possible and requires obnoxiously tight convergence.

Note that polarizability calculations have higher demands on basis sets.
A rather nice basis set for this property is the Sadlej one (see
{ref}`sec:essentialelements.basisset.builtin`). In relation to electric properties, it might be interesting to know that it is possible to carry out finite electric field calculations in ORCA. See section {ref}`sec:essentialelements.finEfield` for more information on such calculations.

The static hyperpolarizability tensor is calculated as an analytical third derivative
of the energy with respect to three dipole perturbations. It is currently available for SCF
methods (HF, DFT). For example, consider the input:

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

The hyperpolarizability can be found printed in the output as
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

(sec:spectroscopyproperties.atomicelectric)=
## Atomic Dipole Moment and Polarizabilities 
```{index} Atomic Dipole Moment and Polarizabilities 
```

ORCA includes a mechanism by which electric properties can be decomposed
into atomic contributions. In a nutshell, the method relies on the
partitioning of real space into atomic regions. These regions are
defined by a smooth weighting function for atom A

$$f_{A}\left( \mathbf{r} \right) = \frac{\varrho_{A}^{(0)}(\mathbf{r})}{\sum_{B}^{}{\varrho_{B}^{(0)}(\mathbf{r})}}$$

The quantities $\varrho_{A}^{(0)}(r)$ are spherically symmetric atomic
densities (expanded in a reasonably large set of Gaussian s-functions)
for the neutral atoms that exit pretabulated in the code.

Using these partitioning functions, an atomic multipole moment is
defined as:

$$Q_{l}^{m}(A) = \sum_{\mu\nu}P_{\mu\nu}\int{\mu(\mathbf{r}){\widehat{q}}_{l}^{m}\nu(\mathbf{r})f_{A}\left( \mathbf{r} \right)d\mathbf{r}}$$

Here **P** is the density matrix and ${\hat{q}}_{l}^{m}$ the operator
for a multipole moment of order l with component m. For example, for the
dipole moment l=1 and m=0,+1,-1. Likewise, for a quadrupole moment l=2,
m=2,1,0,-1,-2 and so on. The partitioned integration over space is
carried out by numerical integration. In the limit of exact numerical
integration, the construction guarantees that the atomic moments sum to
the overall multipole moment. Because numerical integration introduces a
small error, the accumulated moments

$$Q_{l}^{m} = \sum_{A}^{}{Q_{l}^{m}(A)}$$

Will show small deviation from the analytically integrated moments that
the program also calculates prints.

Clearly, the same strategy can be used for response properties. For
example, for polarizabilities, one decomposes it into the atomic
components as follows:

$$\alpha_{KL}(A) = - \sum_{\mu\nu}\frac{\partial P_{\mu\nu}}{\partial F_{K}}\int{\mu(\mathbf{r})\mathbf{r}_{L}\nu(\mathbf{r})f_{A}\left( \mathbf{r} \right)d\mathbf{r}}$$

Here **F** is an external electric field and the derivative of the
density matrix is the response density with respect to this field.

In order to trigger this calculation use:

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

:::{note}
-   Atomic electric properties are available presently at the SCF level
    for dipole moments, quadrupole moments and polarizabilities
-   The dipole moment is well-known to be gauge dependent for charged
    molecules. Hence, the way the dipole moment is decomposed here, the
    atomic dipole moments refer to the global origin and there is a
    gauge dependence for charged atoms. Consequently, one needs to
    proceed with some caution in the interpretation of these local
    dipole moments.
:::

PAPER:
-   Grigorash, D.; Müller, S.; Heid, E.; Neese, F.; Liakos, D.;
    Riplinger, C.; Garcia-Rates, M.; Paricaud, P. Erling H.S.; Smirnova,
    I.; Yan, W. A comprehensive approach to incorporating intermolecular
    dispersion into the openCOSMO-RS model. Part 2: Atomic
    polarizabilities, 2025, submitted 

(sec:spectroscopyproperties.properties.elprop.dynamic)=
## Dynamic Electrical Properties
```{index} Dynamic Electrical Properties
```

At the SCF level, dynamic (frequency-dependent) dipole polarizabilities can be computed
using either purely real or purely imaginary frequencies.
```orca
%elprop
 polar 1
 freq_r 0.08  # purely real frequencies
 #freq_i 0.08 # purely imaginary frequencies 
end
```
In the example above, the dynamic dipole polarizability tensor
 for a single real frequency of 0.08 a.u. is computed.
For every frequency, linear response equations must be solved for 
 all component of the perturbation operator 
(3 Cartesian components of the electric dipole).
Note that imaginary-frequency polarizabilities are computed
 with the same costs as real-frequency polarizabilities.
By a simple contour integration they can be used to compute
 dispersion coefficients.

:::{warning} 
Dynamic (frequency-dependent) dipole first hyper-polarizabilities
based on analytic differentiation are not yet available in ORCA.
:::

:::{note} 
For dynamic (frequency-dependent) polarizabilties and hyper-polarizabilities
 numerical differentiation is more elaborate{cite}`Goncharov2012JCP`.
A workflow based on compound scripts is not yet available at the moment.
:::

(sec:spectroscopyproperties.properties.elprop.keywords)=
## Elprop Keywords 
```{index} Electrical Properties Keywords
```

Calculation of first order (electric dipole and quadrupole
moments) and second order (polarizabilities) electric properties can be requested
in the `%elprop` input block. The second order properties can be
calculated through the solution of the CP-SCF (see {ref}`sec:essentialelements.cpscf`) 
or CP-CASSCF (see {ref}`sec:spectroscopyproperties.casscfresp`) equations. Details are
shown below:

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

The most efficient and accurate way to calculate the polarizability
analytically is to use the coupled-perturbed SCF method. The most time
consuming and least accurate way is the numerical second derivative of
the total energy. Note that the numerical differentiation requires: (a)
tightly or even very tightly converged SCF calculations and (b)
carefully chosen field increments. If the field increment is too large
then the truncation error will be large and the values will be
unreliable. On the other hand, if the field increment is too small the
numerical error associated with the finite difference differentiation
will get unacceptably large up to the point where the whole calculation
becomes useless.
