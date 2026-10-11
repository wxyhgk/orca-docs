<a id="sec:modelchemistries.hftype"></a>
# Wavefunction Types: RHF/RKS, UHF/UKS, ROKS and more

The basic variable that controls the type of wavefunction to be computed
is the variable `HFTyp` in the `%scf` block. If nothing is specified for
`HFTyp`, the program will check the multiplicity given in the input: for
closed-shell molecules with multiplicity 1, RHF/RKS is assumed; for open
shell molecules with multiplicity larger than 1, UHF/UKS is invoked.
`RHF` will lead to a spin restricted closed-shell type computation
[szabo1989modern](../../bibliography.md) whereas UHF does a spin unrestricted calculation. 

For DFT calculations, `RKS`, `UKS` and `ROKS` can be
used as synonyms for `RHF`, `UHF` and `ROHF`. The restricted open-shell
DFT method (`ROKS`) is only operative for high-spin states that have$n$
unpaired electrons and$S=n/2$. `UKS` wavefunctions will not be
spin-purified.

```orca
%scf
  HFTyp  RHF     # closed-shell (RKS for DFT)
         UHF     # unrestricted open-shell (UKS for DFT)
         ROHF    # restricted open-shell (ROKS for DFT)
         CASSCF  # complete active space SCF
end
```

In certain cases you may want to run open-shell systems with RHF/RKS
to get a "half-electron" type wavefunction [dewar1968am](../../bibliography.md). The total
energy is not corrected! Sometimes these half-electron computations lead
to acceptable convergence, and the resulting orbitals may be used as
input for ROHF, UHF or MRCI calculations. Special attention should be taken for transition
metal complexes where the RHF/RKS orbitals are quite different from ROHF or UHF
orbitals, so that it is not recommended to over-interpret the
wavefunctions from such calculations. The calculation is set up in the
following way:

```orca
%method AllowRHF true end
# or simply: ! AllowRHF
```

<a id="sec:modelchemistries.hftype.rohf"></a>
## ROHF Options

For ROHF
calculations[mcweeny1974mol,brobowicz1977methods,carbo1978general,binkley1974mol,edwards1987theor,muller1994chem,kollmar1996chem,kollmar1997int,bofill1998comp](../../bibliography.md)
the program will try to figure out what type of open-shell situation is
present on the basis of the initial guess orbitals and their energies.
Most "simple" cases are well recognized, but sometimes a little help from
the user is needed.

The simplest ROHF case is the `HIGHSPIN` case, where all unpaired electrons
in the open-shell are ferromagnetically coupled (parallel to each other), resulting in the highest
multiplicity possible. The user can request this case as follow:

```orca
%scf
  HFTyp       ROHF
  ROHF_case   HIGHSPIN
  ROHF_NEl[1] 4          # number of electrons in the open-shell
end
```

The ROHF code also has a very powerful feature that goes
back to insights of Mike Zerner [stavrev1997int,zerner1989int](../../bibliography.md). It
can average over either *all* states of a given configuration (`CAHF`)
or *all states of a given spin* for a given configuration (`SAHF`).
Especially, the `SAHF` feature gives you easy access to most degenerate
high symmetry situations and the orbitals resulting from such
calculations will be very convenient as input for CI calculations.

```orca
%scf
  HFTyp         ROHF
  ROHF_case     CAHF    # configuration averaged HF
                SAHF    # spin averaged HF
  ROHF_NumOp    3       # number of operators (3, 2 or 1)
  ROHF_NOrb[1]  2,1     # number of orbitals in each open-shell
  ROHF_NEl[1]   1,1     # number of electrons in each open-shell
end
```

The hypothetical example below could represent an excited state of an
octahedral d$^{3}$ transition metal complex. In this case there are five
open-shell orbitals. The first three open-shell orbitals contain two
electrons and the last two one electron. The input for a SAHF
calculation is identical, just replace CAHF with SAHF.

```orca
%scf
  HFTyp         ROHF
  ROHF_case     CAHF   # configuration averaged HF
  ROHF_NumOp    3      # 3 operators in this case: closed, open1, open2
  ROHF_NOrb[1]  3,2    # 3 orbitals in first open shell, 2 in the second
  ROHF_NEl[1]   2,1    # 2 electrons in first open shell, 1 in the second
end
```

Another feature of the ROHF code is the ability to converge the SCF to
a given Configuration State Function (`CSF-ROHF`) [gouveia2024JPCA](../../bibliography.md).
In this way one can approach results from MCSCF calculations. This can be
requested in two ways.

The user can give a specific coupling situation.
```orca
%scf
  HFTyp      ROHF
  ROHF_CASE  USER_CSF          # User defined CSF
  ROHF_REF   {1 1 -1 -1} end   # CSF to be converged to a 2 open shell antiferromagnetically coupled
end
```

Or the user can give how many orbitals per shell. Where each open-shell
will couple with antiparallel spin with the previous one.
```orca
%scf
  HFTyp       ROHF
  ROHF_CASE   AF_CSF          # User defined CSF
  ROHF_AFORBS 2,2             # Coupling Situation
end
```

As an example, one can think of a Fe(III) dimer, where each center is locally
high spin, but they couple antiferromagnetically to each other. In order to get
the ROHF solution for this system, first one needs a set of initial guess orbitals. The 
guess orbitals can be obtained either from the QROs of an UHF calculation, or a
high spin ROHF calculation, or even a SAHF or CAHF. Independently of the method used,
the orbitals need to be localized and ordered in a way that the set of 3d orbitals of each iron
are grouped together in sequence. From this, one can run a CSF-ROHF calculation for
the antiferromagnetic CSF as shown bellow:

```orca
%scf
  HFTyp      ROHF
  ROHF_CASE  USER_CSF                         # User defined CSF
  ROHF_REF   {1 1 1 1 1 -1 -1 -1 -1 -1} end   # 2 open shells coupling antiparallel
end

or

%scf
  HFTyp       ROHF
  ROHF_CASE   AF_CSF                          # User defined CSF
  ROHF_AFORBS 5,5                             # 2 open shells coupling antiparallel
end
```

The CSF-ROHF procedure can recognize doubly occupied and virtual orbitals in the definition of
the CSF when the `USER_CSF` case is invoked. When detected, these orbitals will be rotated out of 
the open-shell defined in the ROHF method and the calculation will run normally:

```orca
%scf
  HFTyp      ROHF
  ROHF_CASE  USER_CSF                   # User defined CSF
  ROHF_REF   {1 1 2 1  -1 -1 0 -1} end  # the DOMO will be rotated to
                                        # the closed-shell and the VMO
					# will be rotated to the virtual space. 
end
```

The user can also directly input the ROHF variables by means of the
`ROHFOPT Case User` keyword. For example,
for the high spin case with three electrons in three orbitals, it gives two
operators with vector coupling coefficients$a=1$ and$b=2$ (Zerner
convention).

```orca
%scf
  HFTyp      ROHF
  ROHFOP  Case    User  # manual input of ROHF variables
    Nop     2           # number of operators
    Norb[1] 3           # number of open-shell orbitals
    Nel[1]  3           # number of open-shell electrons
    A[1,1]  1           # Coulomb vector in the open shell
    B[1,1]  2           # Exchange vector in the open shell
  end
end
```

One awkward feature of the ROHF theory is that the Fock operator is
somewhat arbitrarily defined. Different choices lead to the same
wavefunction, but have different convergence properties that may vary
from system to system. ORCA thus lets the user choose the desired
variant. Playing around with these choices may turn a divergent or
slowly converging ROHF calculation into a successful calculation!

The `ROHF_Restrict` feature is another feature that may be useful. If
you suspect that the ROHF calculation does not converge because an
open-shell and a closed-shell orbital are flipping back and forth, you
can try to avoid this behavior by choosing `ROHF_Restrict true`. Of
course there is no guarantee that it will work, and no guarantee that
the system stays in the desired state. However, it decreases the chances
of large, uncontrolled steps.

```orca
%scf
  ROHF_Mode 0   # construct F according to Pulay (default)
            1   # construct F as in the Gamess program
            2   # construct F according to Kollmar

  ROHF_Restrict false # restrict orbital interchanges and off-diagonal elements
                      # (default=false)
                      
  # a complete list of ROHF variables
  ROHFOP 
    Case      User   # manual input of ROHF variables
    Nop       2      # number of operators
    Norb[1]   3      # number of open-shell orbitals
    Nel[1]    3      # number of open-shell electrons
    A[1,1]    1      # Coulomb vector in the open shell
    B[1,1]    2      # Exchange vector in the open shell
    Mode      2      # use the Kollmar operator
    Restrict  false  # do not restrict
  end
end
```

<a id="sec:modelchemistries.hftype.uhfno"></a>
## UHF Natural Orbitals

The program can produce the UHF natural orbitals (UNOs). With these, the
open-shell wavefunction can be pictured conveniently. The syntax is
simple:

```orca
%scf
  UHFNO true
end
# or simply: ! UNO
```

There are various printing options for UNOs described in the output
section [spectroscopyproperties.pop](../spectroscopyproperties/population.md#sec:spectroscopyproperties.pop). The UNOs can also be plotted as described
in the plots section
[utilities.plots](../utilitiesvisualization/plots.md#sec:utilities.plots). In general the program stores a file
`BaseName.uno`, where `BaseName` is by default the name of your input
file with `.inp` stripped off. Accordingly, the gbw file is named
`BaseName.gbw`. The `.uno` file is a normal gbw file that contains the
geometry, basis set and the UNO orbitals. It could be used, for example,
to start a ROHF calculation.

<a id="sec:modelchemistries.hftype.unoucoqro"></a>
## UNO, UCO and QROs input 

For calculations on open-shell systems we recommend to use the keywords
`!UNO` `!UCO` in the input line. This will generate quasi-restricted
molecular orbitals `QRO`, unrestricted natural spin-orbitals `UNSO`,
unrestricted natural orbitals `UNO` and unrestricted corresponding
orbitals `UCO`. Moreover, it will print the UCO overlaps in the output,
which can provide very clear information about the spin-coupling in the
system. Below an example of the input and section of the output is
provided.

```orca
!B3LYP def2-SVP UNO UCO TightSCF
```

The UCO overlap section in the output will look like:

```orca
***UHF Corresponding Orbitals were saved in MyJob.uco***

----------------------
Orbital    Overlap(*)
----------------------
.
.
.
96:       0.99968
97:       0.99955
98:       0.99947
99:       0.99910
100:      0.99873
101:      0.99563
102:      0.74329
103:      0.00000
```

The overlap that corresponds to a value usually less than 0.85 denotes a
spin-coupled pair. Whereas, values close to 1.00 and 0.00 refers to the
doubly occupied and singly occupied orbitals respectively.
