(sec:modelchemistries.caspt2)=
# Complete Active Space Peturbation Theory (CASPT2 and CASPT2-K)
```{index} CASPT2
```

The fully internally contracted CASPT2 (FIC-CASPT2) approach is
available with real, imaginary and IPEA
shifts.{cite}`caspt2,caspt2Shift,caspt2IShift`. The ORCA implementation
employs a reformulation of the CASPT2, that completely avoids the fourth
order reduced density matrix, that would appear in the canonical
implementation.{cite}`kollmar_d4efficient_2021` Some concepts are shared by a
recent development reported by Sokolov and
coworkers.{cite}`sokolov_mradc_2020` The modification allows calculations
with large active spaces without approximating the results e.g. with the
cumulant expansion.

It should be noted that the IPEA shift in OpenMOLCAS slightly deviates
from ORCA.{cite}`openmolcas2019`. Here, the IPEA shift, $\lambda$, is added
to the matrix elements of the internally contracted CSFs
$\Phi^{pr}_{qs}=E^p_qE^r_s|\Psi^0>$ with the generalized Fock operator

$$<\Phi^{p'r'}_{q's'}|\hat{F}|\Phi^{pr}_{qs}>+=<\Phi^{p'r'}_{q's'}|\Phi^{pr}_{qs}> \cdot \frac{\lambda}{2}\cdot (4+\gamma^p_p-\gamma^q_q+\gamma^r_r-\gamma^s_s),$$

where $\gamma^p_q=<\Psi^0|E^p_q|\Psi^0>$ is the expectation value of the
spin-traced excitation operator.{cite}`caspt2ipea2` The labels p,q,r,s refer
to general molecular orbitals (inactive, active and virtual).
Irrespective of the ORCA implementation, the validity of the IPEA shift
in general remains questionable and is thus by default
disabled.{cite}`zobel_ipea_2016` ORCA features an alternative formulation,
named **CASPT2-K**, that revises the zeroth order Hamiltonian
itself.{cite}`caspt2k` Here, two additional Fock matrices are introduced for
excitation classes that add or remove electrons from the active space.
The new Fock matrices are derived from the generalized Koopmans'
matrices corresponding to electron ionization and attachment processes.
The resulting method is less prone to intruder states and the same time
more accurate compared to the canonical CASPT2 approach. For more a
detailed discussion, we refer to the paper by Kollmar et al.{cite}`caspt2k`

CASPT2 and CASPT2-K belong to the same family of approaches as [NEVPT2](sec:modelchemistries.nevpt2). 
Both methods are called in complete analogy to the FIC-NEVPT2 approach. 
Note that the methodology can be combined with the [RI approximation](sec:modelchemistries.nevpt2.ri).
However, unlike NEVPT2, the CASPT2 formulations require the storage of the entire wave function. Hence, the scope 
of accessible systems is far more limited compared to the NEVPT2 implementation in ORCA. Below is concise [list with the accessible options](sec:modelchemistries.caspt2.keywords).

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

CASPT2 can also be set using the simple keywords on top of any valid
CASSCF input.

```orca
!CASPT2       # FIC-CASPT2
!CASPT2K      # FIC-CASPT2-K
!RI-CASPT2    # FIC-CASPT2 with RI approximation
!RI-CASPT2K   # FIC-CASPT2-K with RI approximation
%casscf ...
```

## Example Nitrogen molecule

In this short section, we add the CASPT2 results to the previously
computed [NEVPT2 potential energy surface](sec:modelchemistries.nevpt2.n2)
 of the N$_{2}$ molecule.

```{literalinclude} ../../orca_working_input/n2_caspt2_scan.inp
:language: orca
```

The CASPT2 output lists the settings prior to the computation. The
printed reference weights should be checked. Small **reference weights**
indicate intruder states. Along the lines, the program also prints the
**smallest denominators** in the perturbation expression (highlighted in
the snippet below). Small denominator may lead to intruder states.


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

Note that the program prints CASPT2-D results prior entering the CASPT2
iterations.{cite}`caspt2` In case of intruder states, the residual equation
may not converge. The program will not abort. Hence, it is important to
check convergence for every CASPT2 run. In this particular example with
the small basis sets, there are no intruder states.

(fig:caspt2scan)=
```{figure} ../../images/n2_caspt2_scan.*

Potential Energy Surface of the N$_2$ molecule from CASSCF(6,6) and
CASPT2 calculations (def2-SVP).
```

The potential energy surface in {numref}`fig:caspt2scan`
is indeed very similar to the FIC-NEVPT2 approach, which is more
efficient (no iterations) and robust (absence of intruder states). The
figure also shows the CASPT2-K results, which is typically a compromise
between the two methods. As expected, the largest deviation from CASPT2
is observed at the dissociation limit, where the open shell character
dominates the reference wave function. In this example, the discrepancy
between the three methods is rather subtle. However, the results may
differ substantially on some challenging systems, such as Chromium dimer
studied in the CASPT2-K publication. {cite}`caspt2k`. Despite its flaws, the
CASPT2 method is of historical importance and remains a popular
methodology. In the future we might consider further extension such as
the (X)MS-CASPT2.{cite}`xmscaspt2`

(sec:modelchemistries.caspt2.keywords)=
## Keywords

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
