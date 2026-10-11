

<a id="sec:modelchemistries.dcdcas.fci.fci"></a>
# Full Configuration Interaction

ORCA provides several exact and approximate approaches to tackle the
full configuration interaction (FCI) problem. These methods are
accessible via the CASSCF module (see Section
[modelchemistries.casscf](CASSCF.md#sec:modelchemistries.casscf)) or the ICE module (described
in Section
[modelchemistries.iceci](iceci.md#sec:modelchemistries.iceci)).

In the following, we compute the FCI energy of the lithium hydride
molecule using the CASSCF module, where a typical input requires the
declaration of an active space. The latter defines the number of active
electron and orbitals, which are evaluated with the FCI ansatz. In the
special case that all electrons and orbitals are treated with the FCI
ansatz, we can use the keyword `DoFCI` in the `%CASSCF` block and let
the program set the active space accordingly. In this example, we focus
on the singlet ground state. Note that excited states for arbitrary
multiplicities can be computed with the keywords `Mult` and `NRoots`.
The FCI approach is invariant to orbital rotations and thus orbital
optimization is skipped in the CASSCF module. Nevertheless, it is
important to employ a set of meaningful orbitals, e.g. from a converged
Hartree-Fock calculation, to reduce the number of FCI iterations.

```mol
title: structure 1
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
2
structure (0 1)
Li            0            0            0
H             0            0        1.597
--- input ---
# Hartree-Fock orbitals
!def2-tzvp RHF

*xyz 0 1
  Li 0 0 0
  H  0 0 1.597
*
```

The output of the Hartree-Fock calculation also reports on the total
number of electrons and orbitals in your system (see snippet below).

```orca
Number of Electrons    NEL             ....    4
Basis Dimension        Dim             ....   20
```

In the given example, there are 4 electrons in 20 orbitals, which is a
"CAS(4,20)". Reading the converged RHF orbitals, we can start the FCI
calculation.

```mol
title: structure 2
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
2
structure (0 1)
Li            0            0            0
H             0            0        1.597
--- input ---
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

The output reports on the detailed CI settings, the number of
configuration state functions (CSFs) and the CI convergence thresholds.

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

The program then prints the actual CI iterations, the final energy, and
the composition of the wave function in terms of configurations (CFGs).

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

Aside from energies, the CASSCF module offers a number of properties
(g-tensors, ZFS, ...), which are described in Section
[casscf.properties](CASSCF.md#sec:modelchemistries.casscf.properties).

The exact solution of the FCI problem has very steep scaling and is thus
limited to smaller problems (at most active spaces of 16 electrons in 16
orbitals). Larger systems are accessible with approximate solutions,
e.g. with the density matrix renormalization group approach (DMRG),
described in Section
[modelchemistries.dmrg](dmrg.md#sec:modelchemistries.dmrg), or the iterative configuration expansion
(ICE) reported in Section
[modelchemistries.iceci](iceci.md#sec:modelchemistries.iceci). For fun, we repeat the calculation with
the ICE-CI ansatz, which offers a more traditional approach to get an
approximate full CI result.

```mol
title: structure 3
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
2
structure (0 1)
Li            0            0            0
H             0            0        1.597
--- input ---
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

The single most important parameter to control the accuracy is `TGen`.
It is printed with the more refined settings in the output. We note
passing that the wave function expansion and its truncation can be
carried out in the basis of CSFs, configurations, or determinants. The
different strategies are discussed in detail by Chilkuri *et
al.* [chilkuri_ice1,chilkuri_ice2](../../bibliography.md).

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

With Hartree-Fock orbitals and the default settings, the ICE converges
in 3 macro iterations to an energy of$-8.048134047513~E_\text{h}$. The
deviation from the exact solution is just
$3.8 \times 10^{-6}~E_\text{h}$ in this example.

