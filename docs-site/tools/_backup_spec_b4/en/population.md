

<a id="sec:spectroscopyproperties.pop"></a>
# Population Analysis

Atomic population related quantities are not real molecular properties
since they are not observables. They are nevertheless highly useful
for interpreting experimental and computational findings. Various ways of analyzing a computed SCF wavefunction are available within ORCA. By default,
ORCA provides very detailed information about calculated molecular
orbitals and bonds through [Mulliken](sec:spectroscopyproperties.pop.mulliken), 
[Löwdin](sec:spectroscopyproperties.pop.loewdin), and [Mayer](sec:spectroscopyproperties.pop.mayer) 
population analyses.

!!! info
    As these methods typically create a very large amount of specific output, we generally recommend to read the 
    [Control of Output](sec:essentialelements.output) section.

    The `!ReducedPOP` keyword is of particular use as it reduces the printed information in the 
    population analysis section, providing orbital population of each 
    atom with percent contribution per basis function type. This is 
    highly useful in figuring out the character of the MOs.

<a id="sec:spectroscopyproperties.pop.mulliken"></a>
## Mulliken Population Analysis

The Mulliken population analysis [mulliken1955pop](../../bibliography.md) is, despite all its
known considerable weaknesses, the standard in most quantum chemical
programs. It partitions the total density using the assignment of basis
functions to given atoms in the molecules and the basis function
overlap. If the total charge density is written as
$\rho \left({ \vec{r} } \right)$ and the total number of electrons is
$N$ we have:

$$

\int{ \rho \left({ \vec{r} } \right)d\vec{r} } =N\qquad \text{(eqn:299)}

$$

and from the density matrix $\mathrm{\mathbf{P} }$ and the basis
functions $\phi$:

$$

\rho \left({ \vec{r} } \right)=\sum\limits_{\mu \nu } { P_{\mu \nu } \phi
_{\mu } \left({ \vec{r} } \right)\phi_{\nu } \left({ \vec{r} } \right)}\qquad \text{(eqn:300)}

$$

therefore:

$$

\int{ \rho \left({ \vec{{r} }} \right)d\vec{{r} }} =\sum\limits_{\mu \nu }
{P_{\mu \nu } \underbrace{ \int{ \phi_{\mu } \left({ \vec{{r} }} \right)\phi
_{\nu } \left({ \vec{{r} }} \right)d\vec{{r} }} }_{S_{\mu \nu } } }\qquad \text{(eqn:301)}

$$

$$

%\hspace{1cm}
=\sum\limits_{\mu \nu } { P_{\mu
\nu } S_{\mu \nu } }\qquad \text{(eqn:302)}

$$

After assigning each basis function to a given center this can be
rewritten:

$$

\hspace{2.5cm}
=\sum\limits_A { \sum\limits_B
{\sum\limits_\mu{ ^{A}\sum\limits_\nu{ ^{B}P_{\mu \nu }^{AB} S_{\mu \nu
}^{AB} } } } }\qquad \text{(eqn:303)}

$$

$$

\hspace{4cm}
=\sum\limits_A { \sum\limits_\mu{^{A}\sum\limits_\nu{ ^{A}P_{\mu \nu }^{AA} S_{\mu \nu }^{AA} } } }
+2\sum\limits_A { \sum\limits_{B<A} { \sum\limits_\mu{ ^{A}\sum\limits_\nu{^{B}P_{\mu \nu }^{AB} S_{\mu \nu }^{AB} } } } }\qquad \text{(eqn:304)}

$$

Mulliken proposed to divide the second term equally between each pair of
atoms involved and define the number of electrons on center $A$,
$N_{A}$, as:

$$

N_{A} =\sum\limits_\mu{ ^{A}\sum\limits_\nu{ ^{A}P_{\mu \nu }^{AA} S_{\mu
\nu }^{AA} } } +\sum\limits_{B\ne A} { \sum\limits_\mu{ ^{A}\sum\limits_\nu{^{B}P_{\mu \nu }^{AB} S_{\mu \nu }^{AB} } } }\qquad \text{(eqn:305)}

$$

such that $\sum\limits_A { N_{A} } =N$. The charge of an atom in the
molecule is then:

$$

Q_{A} =Z_{A} -N_{A}\qquad \text{(eqn:306)}

$$

where $Z_{A}$ is the core charge of atom $A$. The cross terms between
pairs of basis functions centered on different atoms is the overlap
charge and is used in ORCA to define the Mulliken bond order:

$$

B_{AB} =2\sum\limits_\mu{ ^{A}\sum\limits_\nu{ ^{B}P_{\mu \nu }^{AB} S_{\mu
\nu }^{AB} } }\qquad \text{(eqn:307)}

$$

<a id="sec:spectroscopyproperties.pop.mulliken.basicusage"></a>
### Basic Usage

The Mulliken population analysis can be invoked by the `!MULLIKEN` input keyword:

```orca
! MULLIKEN
```
It can further be requested via the `Print[ P_Mulliken ] 1` keyword in the `%output` block

```orca
%output
  Print[ P_Mulliken ] 1  # default = on
end
```

A number of additional options can be specified in the `%output` block to control the details
of the Mulliken population analysis. By default the Mulliken population analysis is turned on.

```orca
%output
  Print[ P_AtCharges_M  ] 1     # Print atomic charges
  Print[ P_OrbCharges_M ] 1     # Print orbital charges
  Print[ P_FragCharges_M] 1     # Print fragment charges
  Print[ P_BondOrder_M  ] 1     # Print bond orders
  Print[ P_FragBondOrder_M ] 1  # Print fragment b.o.
  Print[ P_ReducedOrbPop_M ] 1  # Print reduced orb. Charges
  Print[ P_AtPopMO_M    ] 1     # Print atomic charges in each MO
  Print[ P_OrbPopMO_M   ] 1     # Print orbital populaiton for each MO
  Print[ P_ReducedOrbPopMO_M] 1 # Print reduced orbital pop for each MO
  Print[ P_FragPopMO_M  ] 1     # Print the fragment population for for each MO
end
```

These options allow to get very detailed information about the computed
wavefunctions and is much more convenient than to look at the MOs
directly. A "reduced orbital population" is a population per angular
momentum type. For example the sum of populations of each p$_{z}$
orbital at a given atom is the reduced orbital population of the p$_{z}$
function.

Note that for [finite temperature HF or KS-DFT](sec:essentialelements.scf.finitetemp) calculations (`SmearTemp`
$>$ 0 K, fractional occupation numbers or [FOD analysis](sec:spectroscopyproperties.fod)), only the Mulliken reduced
orbital charges based on $\rho^{FOD}$ will be printed. 

<a id="sec:spectroscopyproperties.pop.loewdin"></a>
## Löwdin Population Analysis

The Löwdin analysis [szabo1989modern](../../bibliography.md) is somewhat more straightforward
than the Mulliken analysis. In the Löwdin method one changes to a basis
where all overlap integrals vanish. This is accomplished via Löwdins
symmetric orthogonalization matrix $\mathrm{\mathbf{S} }^{-1/2}$. Using
this transformation matrix the new basis functions are multicentered but
are in a least square sense as similar as possible to the original,
strictly localized, atomic basis functions. The similarity of the
transformed functions and original functions is explored in the
population analysis. The density matrix transforms as:

$$

\mathrm{\mathbf{P} }^{L}=\mathrm{\mathbf{S} }^{1/2}\mathrm{\mathbf{PS} }^{1/2}\qquad \text{(eqn:308)}

$$

Then the atomic populations are:

$$

N_{A} =\sum\limits_\mu{ ^{A}P_{\mu \mu }^{L} }\qquad \text{(eqn:309)}

$$

The bond order is defined from the Wiberg index [wiberg1968tetrahedron](../../bibliography.md)
that was first used in the context of semiempirical methods (that are
formulated in the Löwdin basis right from the start):

$$

B_{AB} =\sum\limits_\mu{ ^{A}\sum\limits_\nu{ ^{B}\left({ P_{\mu \nu }^{L} }
\right)^{2} } }\qquad \text{(eqn:310)}

$$

<a id="sec:spectroscopyproperties.pop.loewdin.basicusage"></a>
### Basic Usage

The Löwdin population analysis can be invoked by the `!LOEWDIN` input keyword. By default the Löwdin
population analysis is turned on and provides some more detail than the Mulliken analysis.

```orca
! MULLIKEN
```
It can further be requested via the `Print[ P_Loewdin ] 1` keyword in the `%output` block:

```orca
%output
  Print[ P_Loewdin ] 1  # default = on
end
```

The details of the Löwdin population analysis printout can be controlled via the `%output` block:

```orca
%output
  Print[ P_AtCharges_L  ] 1     # Print atomic charges
  Print[ P_OrbCharges_L ] 1     # Print orbital charges
  Print[ P_FragCharges_L] 1     # Print fragment charges
  Print[ P_BondOrder_L  ] 1     # Print bond orders
  Print[ P_FragBondOrder_L ] 1  # Print fragment b.o.
  Print[ P_ReducedOrbPop_L ] 1  # Print reduced orb. Charges
  Print[ P_AtPopMO_L    ] 1     # Print atomic charges in each MO
  Print[ P_OrbPopMO_L   ] 1     # Print orbital population for each MO
  Print[ P_ReducedOrbPopMO_L] 1 # Print reduced orbital pop for each MO
  Print[ P_FragPopMO_L  ] 1     # Print the fragment population for each MO
end
```

In addition one can set the threshold for the
printing of the bond order in the `%method` block.

```orca
%method
  LOEWDIN_BONDORDERTHRESH 0.05
end
```

<a id="sec:spectroscopyproperties.pop.fmopop"></a>
## Frontier Molecular Orbital Populations

As the frontier orbitals are typically of specific interest, [Mulliken](sec:spectroscopyproperties.pop.mulliken)
and [Löwdin](sec:spectroscopyproperties.pop.loewdin) populations of the HOMO and LUMO can be requested via the "`FMOPop`" keyword:

```orca
! FMOPop
```

The respective Mulliken and Loewdin population of the HOMO and LUMO frontier orbitals will
be printed in the output:

```orca
----------------------------------------------
FRONTIER MOLECULAR ORBITAL POPULATION ANALYSIS
----------------------------------------------

ANALYZING ORBITALS: HOMO=   6 LUMO=   7

-------------------------------------------------------------------------
   Atom        Q(Mulliken)     Q(Loewdin)     Q(Mulliken)     Q(Loewdin) 
              <<<<<<<<<<<<HOMO>>>>>>>>>>>>   <<<<<<<<<<<<LUMO>>>>>>>>>>>>
-------------------------------------------------------------------------
   0-C         0.937186        0.906827       0.804044        0.755610
   1-O         0.062814        0.093173       0.195956        0.244390
-------------------------------------------------------------------------
```

<a id="sec:spectroscopyproperties.pop.mayer"></a>
## Mayer Population Analysis

Mayers bonding analysis
[mayer1983chem,mayer1984int,mayer1985theor,mayer1987modelling](../../bibliography.md) is
another creative attempt to define chemically useful indices. The Mayer
atomic charge is identical to the Mulliken charge. The Mayer bond order
is defined as:

$$

B_{AB} =\sum\limits_\mu{ ^{A}\sum\limits_\nu{ ^{B}\left({ \mathrm{\mathbf{PS} }}
\right)_{\mu \nu } \left({ \mathrm{\mathbf{PS} }} \right)_{\nu \mu } +\left({ \mathrm{\mathbf{RS} }} \right)_{\mu \nu }
\left({ \mathrm{\mathbf{RS} }} \right)_{\nu \mu } } }\qquad \text{(eqn:311)}

$$

Here $\mathrm{\mathbf{P} }$ is the total electron density matrix and
$\mathrm{\mathbf{R} }$ is the spin-density matrix. These Mayer bond
orders are very useful. Mayer's total valence for atom $A$ is defined
as:

$$

V_{A} =2N_{A} -\sum\limits_\mu{ ^{A}\sum\limits_\nu{ ^{A}\left({ \mathrm{\mathbf{PS} }} \right)_{\mu \nu } \left({ \mathrm{\mathbf{PS} }} \right)_{\nu \mu } } }\qquad \text{(eqn:312)}

$$

In normal bonding situations and with normal basis sets $V_{A}$ should
be reasonably close to the valence of atom $A$ in a chemical sense (i.e.
close to four for a carbon atom). The bonded valence is given by:

$$

X_{A} =V_{A} -\sum\limits_{B\ne A} { B_{AB} }\qquad \text{(eqn:313)}

$$

and finally the free valence (a measure of the ability to form further
bonds) is given by:

$$

F_{A} =V_{A} -X_{A}\qquad \text{(eqn:314)}

$$

<a id="sec:spectroscopyproperties.pop.mayer.basicusage"></a>
### Basic Usage

The Mayer population analysis can be invoked via the `!MAYER` keyword:

```orca
! MAYER
```

It can further be requested via the `Print[ P_Mayer ] 1` keyword in the `%output` block:

```orca
%output
  Print[ P_Mayer ] 1  # default = on
end
```

The output is rather simple and short and can not be further controlled.
By default the Mayer population analysis is turned on. In addition one
can set the threshold for the printing of the bond order in the `%method` block.

```orca
%method
  MAYER_BONDORDERTHRESH 0.1
end
```

<a id="sec:spectroscopyproperties.pop.natural"></a>
## Natural Population Analysis

If you have access to a version of the `gennbo` program from
Weinhold's group[^a] you can request the Natural Population analysis via the [NBO interface](sec:spectroscopyproperties.nbo).

[^a]: Information about the NBO program can be found at <http://nbo7.chem.wisc.edu>

!!! warning
    The NPA is only performed if the NBO program is provided properly. If not, ORCA will skip the NPA analysis.

<a id="sec:spectroscopyproperties.pop.natural.basicusage"></a>
### Basic Usage

The Natural population analysis can be invoked via the `!NPA` keyword:

```orca
! NPA
```

It can further be requested via the `Print[ P_NPA ] 1` keyword in the `%output` block:

```orca
%output
  Print[ P_NPA ] 1  # default = off
end
```

<a id="sec:spectroscopyproperties.pop.hirshfeld"></a>
## Hirshfeld Population Analysis

The partitioning method by Hirshfeld is one of the most used approaches in
the so-called atoms in molecules (AIM) methods.[hirshfeld1977](../../bibliography.md) In this case, the AIM density
of atom A, $\rho_A(\vec{r})$ is written as:

$$

\rho_A(\vec{r}) = \rho(\vec{r})w_A(\vec{r})\qquad \text{(eq_aim_charge)}

$$

Here, $\rho(\vec{r})$ is the total charge density at position $\vec{r}$, and $w_A(\vec{r})$ a
weighting function, that within the Hirshfeld method is equal to:

$$

w_A(\vec{r}) = \frac{\rho_A^0(\vec{r})}{\rho^0(\vec{r})}\qquad \text{(eq_w_hirshfeld)}

$$

where $\rho_A^0(\vec{r})$ is the pro-atomic density of atom $A$ and $\rho^0(\vec{r})=\sum_A\rho_A^0(\vec{r})$ the 
pro-molecular density. The ratio in eq. [Eq](#eq_aim_charge) is known as _stockholder_. From eqs. [Eq](#eq_aim_charge)
and [Eq](#eq_w_hirshfeld) one can calculate the Hirshfeld charges as:

$$

Q_A^{\mathrm{Hirsh.}} = Z_A -\int\rho_A(\vec{r})d\vec{r}\qquad \text{(eq_q_hirshfeld)}

$$

In ORCA, the pro-atomic density within the Hirshfeld method is calculated via density fitting with
a set of Gaussian s-functions per element.

<a id="sec:spectroscopyproperties.pop.hirshfeld.basicusage"></a>
### Basic Usage

The Hirshfeld population analysis can be invoked by the `!HIRSHFELD` input keyword.

```orca
! HIRSHFELD
```
It can further be requested via the `Print[ P_Hirshfeld ] 1` keyword in the `%output` block:

```orca
%output
  Print[ P_Hirshfeld ] 1  # default = off
end
```

<a id="sec:spectroscopyproperties.pop.hirshfeld.example"></a>
### Example

As an example we request the Hirshfeld charges for a water molecule:

```orcainput
!HF cc-pVDZ TightSCF HIRSHFELD

* xyz 0 1
  O    0.00000006589375       0.00157184228646       0.00000000004493
  H    0.77316868532439      -0.58666889665624      -0.00000000000005
  H   -0.77316876182122      -0.58666895650640      -0.00000000000005
*
```

ORCA prints the following information in the output file:

```orca
------------------
HIRSHFELD ANALYSIS
------------------

Total integrated alpha density =      4.999998580
Total integrated beta density  =      4.999998580

  ATOM     CHARGE      SPIN
   0 O   -0.333756    0.000000
   1 H    0.166879    0.000000
   2 H    0.166879    0.000000

  TOTAL   0.000003    0.000000
```

<a id="sec:spectroscopyproperties.pop.mbis"></a>
## MBIS Charges

The Minimal Basis Iterative Stockholder (MBIS) method is a variant of the Hirshfeld method.[mbis2016](../../bibliography.md)
The idea behind this approach is that the pro-atomic density $\rho_A^0(\vec{r})$ is expanded
in a minimal set of atom-centered s-type Slater functions $\rho_{Ai}^0(\vec{r})$:

$$

\rho_A^0(\vec{r}) = \sum_{i=1}^{m_A}\rho_{Ai}^0(\vec{r})\qquad \text{(eq_sum_mbis)}

$$

with $\rho_{Ai}^0(\vec{r})$ equal to:

$$

\rho_{Ai}^0(\vec{r}) = \frac{N_{Ai}}{\sigma_{Ai}^38\pi}\mathrm{exp}\left(-\frac{\left|\vec{r}-\vec{R_A}\right|}{\sigma_{Ai}}\right)\qquad \text{(eq_rai_mbis)}

$$

Here, $m_A$ is the number of shells of atom $A$. The populations $N_{Ai}$, and the widths $\sigma_{Ai}$
can be written as:

$$

N_{Ai} = \int\rho(\vec{r})\frac{\rho_{Ai}^0(\vec{r})}{\rho^0(\vec{r})}d\vec{r}\qquad \text{(eq_nai_mbis)}

$$

$$

\sigma_{Ai}=\frac{1}{3N_{Ai}}\int\rho(\vec{r})\frac{\rho_{Ai}^0(\vec{r})}{\rho^0(\vec{r})}\left|\vec{r}-\vec{R_A}\right| d\vec{r}\qquad \text{(eq_sai_mbis)}

$$

In order to compute the AIM densities $\rho_A(\vec{r})$, the MBIS method uses an iterative algorithm where:
(1) an initial guess is generated for the set of $N_{Ai}$ and $\sigma_{Ai}$ and the pro-atomic densities are
calculated through eqs. [Eq](#eq_sum_mbis) and [Eq](#eq_rai_mbis), (2) the new set of $N_{Ai}$ and $\sigma_{Ai}$ are obtained
via eqs. [Eq](#eq_nai_mbis) and [Eq](#eq_sai_mbis), (3) if convergence is reached for $\rho_A(\vec{r})$, the
iterative process stops, otherwise we go back to (1) but now one uses the last estimates for $N_{Ai}$ and $\sigma_{Ai}$.

Once, the MBIS iterative process stops, the MBIS charges are calculated as:

$$

Q_A^{\mathrm{MBIS.}} = Z_A -\int\rho_A(\vec{r})d\vec{r}\qquad \text{(eq_q_mbis)}

$$

<a id="sec:spectroscopyproperties.pop.mbis.basicusage"></a>
### Basic Usage

The MBIS population analysis can be invoked by the `!MBIS` input keyword.

```orca
! MBIS
```
It can further be requested via the `Print[ P_MBIS ] 1` keyword in the `%output` block:

```orca
%output
  Print[ P_MBIS ] 1  # default = off
end
```

The convergence threshold for the MBIS charges is set to $10^{-6}$. However, it can be changed via
the tag `MBIS_CHARGETHRESH` in the `%method` block:

```orca
%method
  MBIS_CHARGETHRESH 0.0001
end
```

<a id="sec:spectroscopyproperties.pop.mbis.quantities"></a>
### MBIS Quantities
ORCA can also print the following MBIS-related quantities: 

1. atomic dipole moments, 
2. atomic quadrupole moments,
3. atomic octupole moments, and 
4. third radial moment of the MBIS density $\left(\langle r^3\rangle_A = \int \left|\vec{r}-\vec{R_A}\right|^3\rho_A(\vec{r})d\vec{r}\right)$. 

The printing of these properties is controlled by the `MBIS_LARGEPRINT` in the `%method` block:

```orca
%method
  MBIS_LARGEPRINT true  # default = false
end
```

If this option is activated, an extra iteration is performed after reaching the convergence threshold for
the charges.

The origin for the calculation of the atomic dipole, quadrupole and octupole moments is the center of each atom (default).
The user can also define a global origin (independent of the atom) through the `MBIS_ORIGIN_MULT` keyword in the `%method` block:

```orca
%method
  MBIS_ORIGIN_MULT  CenterOfCoords     # origin of coordinate system (0,0,0)
                    CenterOfMass       # center of mass
                    CenterOfNucCharge  # center of nuclear charge
                    CenterXYZ          # arbitrary position, set coordinates
		                       # with MBIS_ORIMULT_XYZ
                    CenterOfEachAtom   # center of each atom (default)
  MBIS_ORIMULT_XYZ  x,y,z # set the coordinates, otherwise 0,0,0 (unit: Angstrom)
end
```

<a id="sec:spectroscopyproperties.pop.mbis.example"></a>
### Example

If we request the MBIS charges for a HF calculation at the cc-pVDZ level of a chloroform molecule:

```orca
!HF cc-pVDZ TightSCF MBIS

* xyz 0 1
  C   -0.00000997794639     -0.00091664148112      0.45499807439812
  H    0.00000069467312      0.00031189002174      1.53703126401237
  Cl   0.00003188789531      1.69433732001280     -0.08420513240263
  Cl   1.46635420502892     -0.84684178730039     -0.08421103795485
  Cl  -1.46637680965097     -0.84689178125304     -0.08420916805301
*
```

ORCA prints the following information at the end of the output file:

```orca
------------------
MBIS ANALYSIS
------------------

Convergence threshold (charges)      ...        1.000e-06
Number of iterations                 ...        46

Total integrated alpha density       ...     29.000001385
Total integrated beta density        ...     29.000001385

  ATOM     CHARGE    POPULATION     SPIN
   0 C    0.208633    5.791367    0.000000
   1 H    0.169417    0.830583    0.000000
   2 Cl  -0.126877   17.126877    0.000000
   3 Cl  -0.125586   17.125586    0.000000
   4 Cl  -0.125590   17.125590    0.000000

  TOTAL  -0.000003   58.000003    0.000000

 MBIS VALENCE-SHELL DATA:
  ATOM   POPULATION   WIDTH(A.U.)
   0 C    4.122213    0.508675
   1 H    0.830583    0.358785
   2 Cl   8.532439    0.524031
   3 Cl   8.531380    0.523959
   4 Cl   8.531381    0.523959
```
The second block corresponds to the valence Slater function, which is caracterized by its
population $N_{A,v}$ and width $\sigma_{A,v}$.

<a id="sec:spectroscopyproperties.pop.chelpg"></a>
## CHELPG Charges

Atomic charges can also be calculated using the CHarges from ELectrostatic Potentials using 
a Grid-based (CHELPG) method according to Breneman and Wiberg.[breneman1990](../../bibliography.md) 
In this approach, the atomic charges are fitted to reproduce the
electrostatic potential on a regular grid around the molecule, while
constraining the sum of all atomic charges to the molecule's total
charge. An additional constraint can be added, so the CHELPG charges
also reproduce the total dipole moment of the molecule.

<a id="sec:spectroscopyproperties.pop.chelpg.basicusage"></a>
### Basic Usage

In ORCA the CHELPG charges can be (i) requested within a calculation, or (ii) calculated via the
standalone [`orca_chelpg`](sec:utilities.chelpg) utility. To follow path (i) one has to add the 
`!CHELPG` simple input keyword to the input file.

```orca
! CHELPG
```

Further settings can be controlled via the `%chelpg` block.

```orca
%chelpg
  GRID 0.3       # Spacing of the regular grid in Angstroems
  RMAX 2.8       # Maximum distance of all atoms to any gridpoint in Angstroems
  VDWRADII COSMO # VDW Radii of Atoms, COSMO default
           BW    # Breneman, Wiberg radii
  DIPOLE FALSE   # If true, then the charges also reproduce the total dipole moment
end
```

By default the program uses the COSMO VDW radii for the exclusion of 
gridpoints near the nuclei, as these are defined for all atoms. The 
BW radii are similar, but only defined for very few atom types.

The charges may exhibit some dependence on the molecule's orientation in
space, or some artificial variations in symmetric molecules. These
effects can be minimized by increasing the CHELPG grid size, either by
setting the `GRID` parameter in the `%chelpg` block, or by using the `!CHELPG(LARGE)`
simple input keyword.

```orca
! CHELPG(LARGE)
```

If one wants that the calculated CHELPG charges reproduce the total
dipole moment of the molecule, as well as the electrostatic potential, then the
following tag has to be added to the `%chelpg` block:

```orca
%chelpg
  DIPOLE TRUE  # The default is set to FALSE
end
```

In particular, the constraint affects the $x$,$y$,$z$ components of the
total dipole moment, so they reproduce the exact three components of the
total dipole moment calculated via one-electron integrals.

<a id="sec:spectroscopyproperties.pop.resp"></a>
## RESP Charges

ORCA also features the possibility of calculating the so-called RESP charges [baylyRESP_1993](../../bibliography.md), which are essentially CHELPG charges with some restraint to avoid over fitting. These can be invoked with the defaults by simply using `!RESP` on the main input.

These RESP charges can have two types of penalty function: quadratic or hyperbolic (default), as described on the original paper. These require up to two penalty values, which are by default given by $a=0.0005$ and $b=0.1$.

These values can be changed inside the `%CHELPG` block by using:

```orca
%chelpg
  RESPWA 0.01   # for the a value
  RESPWB 0.002  # for the b value
end
```

and the penalty function can be chosen with:

```orca
%chelpg
  RESPPENALTY QUADRATIC # default is HYPREBOLIC
end
```

Also, if needed, the individual values for the $a$ parameters and reference charges $q_0$ can be given via a special file with:

```orca
%chelpg
  RESPWFILE     "wfilename" # these will define the weights (or a parameters)
                            # for each atom
  RESPQREFFILE  "qfilename" # these might define reference charges different
                            # from zero
end
```

The format for both these files is similar to a `.xyz` file, where the first line has the number of atoms, the second line is just a comment, and every subsequent line contains a single number which is either the weights or the reference charges per atom. They can not be given on a single file, there must be two different ones.

!!! note
      The results from the RESP files obtained here are **not** necessarily the same one would get from other software. Two main reasons are: the grids are not the same and some other software use a multilevel approach, first starting with a certain value for the weights and then switching to a different value, which is not the case here.

<a id="sec:spectroscopyproperties.pop.lsa"></a>
## Local Spin Analysis

It is common practice in chemistry to think about the
interaction of open-shell systems in terms of local spin states. For
example, in dimeric or oligomeric transition metal clusters, the
'exchange coupling' between open shell ions that exist locally in
high-spin states is extensively studied. Diradicals would be
typical systems in organic chemistry that show this phenomenon. In
quantum mechanics, however, the total spin is not a local property, but
instead a property of the system as a whole. The total spin squared,
$S^2$, and its projection onto the z-axis, $S_z$, commute with the
non-relativistic Hamiltonian and hence, the eigenfunctions of the
non-relativistic Hamiltonian can be classified according to good quantum
numbers $S$ and $M$ according to:

$$

{\mathbf{S} }_{}^2\left|{ \Psi _{}^{SM} } \right\rangle = S(S + 1)\left|{ \Psi _{}^{SM} } \right\rangle

$$
$$

S_z^{}\left|{ \Psi _{}^{SM} } \right\rangle = M\left|{ \Psi _{}^{SM} } \right\rangle

$$

where $\left|{ \Psi _{}^{SM} } \right\rangle$ is an exact eigenfunction
of the non-relativistic Hamiltonian or an approximation to it that
conserves the total spin as a good quantum number. The total spin itself
is given by the sum over the individual electron spins as:

$$

{\mathbf{S} } = \sum\limits_i { {\mathbf{s} }(i) }

$$

And hence,

$$

{\mathbf{S} }_{}^2 = \sum\nolimits_{i,j} { {\mathbf{s} }(i){\mathbf{s} }(j) }

$$

is a two-electron property of the system. It is obviously not trivial to
relate the chemically very meaningful concept of local spin to a
rigorous quantum mechanical treatment. While there are various proposals
of how to deal with this problem, we follow here a proposal of Clark and
Davidson[clark2001localspin](../../bibliography.md). The following equations are implemented in the SCF and
CASSCF modules of Orca.
Clark and Davidson define fragment projection operators with the
property:

$$

P_A^{}P_B^{} = \delta _{AB}^{}P_A^{}

$$

and:

$$

\sum\limits_A { P_A^{} }  = 1

$$

Then using this identity:

$$

{\mathbf{S} } = \sum\limits_i { \sum\limits_A { {\mathbf{s} }(i)P_{A(i) }^{} } }

$$
$$

{\mathbf{S} } = \sum\limits_A { \sum\limits_i { {\mathbf{s} }(i)P_A^{}(i) } }

$$
$$

\,\,\,\, = \sum\limits_A { {\mathbf{S} }_A^{}(i) }

$$

they show that the local spin operators obey the standard relations for
spin operators:

$$

{\mathbf{S} }_A^{} = { \mathbf{S} }_A^\dagger

$$
$$

{\mathbf{S} }_A^{} \times{ \mathbf{S} }_A^{} = i\hbar{ \mathbf{S} }_A^{}

$$

Hence

$$

{\mathbf{S} }_{}^2 = \sum\limits_A { \sum\limits_B { {\mathbf{S} }_A^{}{\mathbf{S} }_B^{} } }

$$

But then importantly:

$$

{\mathbf{S} }_A^{}{\mathbf{S} }_B^{} = \sum\limits_i { \sum\limits_j { {\mathbf{s} }(i){\mathbf{s} }(j) } P_A^{}(i)P_B^{}(j) }

$$
$$

\,\,\,\,\,\,\,\,\,\,\,\, = { \textstyle{3 \over 4} }\delta _{AB}^{}\sum\limits_A { P_A^{}(i) }  + \sum\limits_i { \sum\limits_{j > i} { {\mathbf{s} }(i){\mathbf{s} }(j)\{ P_A^{}(i)P_B^{}(j) + P_A^{}(j)P_B^{}(i)\} } }

$$

With the first- and second-order density matrix:

$$

\gamma ({\mathbf{x} },{\mathbf{x'} }) = N\int{ \Psi ({\mathbf{x} },{\mathbf{x} }_2^{},...,{\mathbf{x} }_N^{})\Psi _{}^*({\mathbf{x'} },{\mathbf{x} }_2^{},...,{\mathbf{x} }_N^{}) } d{\mathbf{x} }_2^{}...d{\mathbf{x} }_N^{}

$$
$$

\Gamma ({\mathbf{x} }_1^{},{\mathbf{x'} }_1^{};{\mathbf{x} }_2^{},{\mathbf{x'} }_2^{}) = \left({
\begin{matrix}
   N  \cr 
   2  \cr 
\end{matrix}
} \right)\int{ \Psi ({\mathbf{x} }_1^{},{\mathbf{x} }_2^{},...,{\mathbf{x} }_N^{})\Psi _{}^*({\mathbf{x'} }_1^{},{\mathbf{x'} }_2^{},...,{\mathbf{x} }_N^{}) } d{\mathbf{x} }_3^{}...d{\mathbf{x} }_N^{}\qquad \text{(with ${\textstyle{N \choose 2} }= { \textstyle{1 \over 2} }N(N - 1)}

$$$).
Then:

$$

\left\langle { {\mathbf{S} }_A^{}{\mathbf{S} }_B^{} } \right\rangle = { \textstyle{3 \over 4} }\delta _{AB}^{}tr(\gamma P_A^{}) + 2tr(P_A^{}(1)P_B^{}(2){\mathbf{s} }(1){\mathbf{s} }(2)\Gamma (1,1;2,2))

$$

In terms of the number of electrons on site 'A'and the expectation value
of $S_z^A$

$$

\left\langle { S_z^A} \right\rangle = { \textstyle{1 \over 2} }tr(\gamma _{}^{\alpha  - \beta }P_A^{})

$$

$$

\left\langle { N_{}^A} \right\rangle = tr(\gamma _{}^{\alpha  + \beta }P_A^{})

$$

in terms of molecular orbitals:

$$

\left\langle { S_z^A} \right\rangle = { \textstyle{1 \over 2} }\sum\limits_{p,q} { \gamma _{pq}^{\alpha  - \beta }\left\langle { p|P_A^{}|q} \right\rangle}

$$

$$

\left\langle { N_{}^A} \right\rangle = \sum\limits_{p,q} { \gamma _{pq}^{\alpha  + \beta }\left\langle { p|P_A^{}|q} \right\rangle}

$$

McWeeny and Kutzelnigg[mcweeny1968independentparticle](../../bibliography.md) show that for the expectation value of s(1)s(2), the
relevant irreducible part of the two-body density can be expressed in
terms of the spinless density matrix of second order:

$$

R_0^{(0) }(1,1';2,2') =  - { \textstyle{1 \over 3} }\Gamma (1,1';2,2') - { \textstyle{2 \over 3} }\Gamma (2,1';1,2')

$$

$$

\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\, =  - { \textstyle{1 \over 3} }\sum\limits_{pqrs} { \Gamma _{rs}^{pq}p(1)q(1')r(2)s(2') }  + 2\Gamma _{rs}^{pq}p(2)q(1')r(1)s(2')

$$

$$

\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\, =  - { \textstyle{1 \over 3} }\sum\limits_{pqrs} { (\Gamma _{rs}^{pq} + 2\Gamma _{ps}^{rq})p(1)q(1')r(2)s(2') }

$$

with a normalization factor of $3 \over 4$ after spin integration. Hence
using this:

$$

\left\langle { {\mathbf{S} }_A^{}{\mathbf{S} }_B^{} } \right\rangle = { \textstyle{3 \over 4} }\delta _{AB}^{}tr(\gamma P_A^{}) + { \textstyle{6 \over 4} }tr(P_A^{}(1)P_B^{}(2)R_0^{(0) }(1,1;2,2))

$$

And then performing the integral:

$$

\left\langle { {\mathbf{S} }_A^{}{\mathbf{S} }_B^{} } \right\rangle = { \textstyle{3 \over 4} }\delta _{AB}^{}tr(\gamma P_A^{}) - \underbrace{ {\textstyle{6 \over 4} }{\textstyle{1 \over 3} }}_{{\textstyle{1 \over 2} }}\sum\limits_{pqrs} { (\Gamma _{rs}^{pq} + 2\Gamma _{ps}^{rq})P_{pq}^AP_{rs}^B}

$$

This is the final and perhaps most compact equation. The projection
operator can be defined in very many different ways. The easiest is to
Löwdin orthogonalize the basis set:

$$

\left|{ \mu_L^A} \right\rangle = \sum\limits_{\nu _{}^A} { \left|{ \nu _{}^A} \right\rangle S_{\mu \nu }^{ - 1/2} }

$$

where $L$ denotes the Löwdin basis. This means that molecular orbitals
are expressed in the orthogonal basis as:

$$

{\mathbf{c} }_L^{} = { \mathbf{S} }_{}^{ + 1/2}{\mathbf{c} }

$$

and the density as:

$$

{\mathbf{P} }_L^{} = { \mathbf{S} }_{}^{ + 1/2}{\mathbf{PS} }_{}^{ + 1/2}

$$

The fragment projector is defined as:

$$

P_A^{} = \sum\limits_{\mu _L^{} \in A} { \left|{ \mu _L^{} } \right\rangle\left\langle { \mu _L^{} } \right|}

$$

Clark and Davidson suggest a slightly more elaborate projector in which
first, the intra-fragment overlap is eliminated. This happens with a
matrix U that for two fragments takes form:

$$

{\mathbf{U} } = \left( 
    \begin{matrix}{ {\mathbf{S} }_A^{ - 1/2} } & { \mathbf{0} }  \cr{ \mathbf{0} } & { {\mathbf{S} }_B^{ - 1/2} }  \cr 
 \end{matrix}
 \right)

$$

where is the block of basis functions belonging to fragment A. Likewise:

$$

{\mathbf{U} }_{}^{ - 1} = \left( 
    \begin{matrix}{ {\mathbf{S} }_A^{ + 1/2} } & { \mathbf{0} }  \cr{ \mathbf{0} } & { {\mathbf{S} }_B^{ + 1/2} }  \cr 
 \end{matrix}
 \right)

$$

Then the 'pre-overlap'is:

$$

{\mathbf{\overline S} } = { \mathbf{U} }_{}^\dagger{ \mathbf{SU} }

$$

This contains the unit matrix in the intra-fragment blocks and non-zero
elements elsewhere. This overlap matrix is the finally orthogonalized to
obtain the globally orthogonal Löwdin basis. We finally transform the MO
coefficients by the following transformation:

$$

{\mathbf{c} }_L^{} = { \mathbf{S} }_{}^{ + 1/2}{\mathbf{U} }_{}^{ - 1}{\mathbf{c} }

$$

For the projectors, operating with the two MOs i and j gives:

$$

\left\langle { i|P_A^{}|j} \right\rangle = \sum\limits_{\mu _L^{} \in A} { \sum\limits_{\kappa _L^B\tau _L^C} { \left\langle { \kappa _L^B|\mu _L^A} \right\rangle\left\langle { \mu _L^A|\tau _L^C} \right\rangle c_{\kappa i}^Lc_{\tau j}^L} }

$$

$$

\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\, = \sum\limits_{\mu _L^{} \in A} { \sum\limits_{\kappa _L^B\tau _L^C} { \delta _{AB}^{}\delta _{AC}^{}\delta _{\kappa \mu }^{}\delta _{\tau \mu }^{}c_{\kappa i}^Lc_{\tau j}^L} }

$$

$$

\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\, = \sum\limits_{\mu _L^{} \in A} { c_{\mu i}^Lc_{\mu j}^L}

$$

Herrmann et al.[herrmann2005localspin](../../bibliography.md) give the correct expression of the expectation values
for a single spin-unrestricted determinant

$$

\begin{aligned}
  & \left\langle { {\mathbf{S} }_A^{}{\mathbf{S} }_B^{} } \right\rangle = { \textstyle{3 \over 4} }\delta _{AB}^{}\left\{{ \sum\limits_i { P_{ii}^A}  + \sum\limits_{\bar i} { P_{\bar i\bar i}^A} } \right\} \cr 
  & \,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\, + { \textstyle{1 \over 4} }\left\{{ \sum\limits_{ij} { P_{ii}^AP_{jj}^B}  + \sum\limits_{\bar i\bar j} { P_{\bar i\bar i}^AP_{\bar j\bar j}^B}  - \sum\limits_{ij} { P_{ij}^AP_{ij}^B}  - \sum\limits_{\bar i\bar j} { P_{\bar i\bar j}^AP_{\bar i\bar j}^B}  - \sum\limits_{\bar ij} { P_{\bar i\bar i}^AP_{jj}^B}  - \sum\limits_{i\bar j} { P_{ii}^AP_{\bar j\bar j}^B} } \right\} \cr 
  & \,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\, - \sum\limits_{i\bar j} { P_{i\bar j}^AP_{i\bar j}^B}  \cr\end{aligned}

$$

Which is used in the Orca implementation.

The use of the Local spin-implementation is very easy. All that is
required is to divide the molecule into 
[fragments](#sec:essentialelements.fragmentation). The rest happens
automatically. For example, let us consider two nitrogen atoms at the
dissociation limit. While the total spin state is S=0, the tow nitrogen
atoms local exist in high-spin states (S=3/2). Consider the following
test job:

```orcainput
! HF def2-SVP UHF TightSCF PModel 

%scf brokensym 3,3 end 

* xyz 0 1
N(1) 0 0 0
N(2) 0 0 1094
*
```

and the output:

```orca
-------------------
LOCAL SPIN ANALYSIS (Loewdin* projector)
-------------------

(1) A.E. Clark; E.R. Davison J. Chem. Phys. (2001), 115(16), pp 7382-7392 
(2)  C. Herrmann, M. Reiher, B.A. Hess J. Chem. Phys. (2005) 122, art 034102-1

Number of fragments       = 2
Number of basis functions = 28
Number of atoms           = 2

   ... Fragment AO indices were mapped
   ... intra-fragment orthogonalization completed
   ... Global Loewdin orthogonalizer constructed
   ... Loewdin orthogonalized occupied orbitals constructed

 <SA*SB>        1            2     
----------------------------------
   1    :     3.7568  
   2    :    -2.2500       3.7568  

               <SzA>      Seff(A)
        --------------------------
   1    :     1.5000      1.5017
   2    :    -1.5000      1.5017
```

thus perfectly corresponding to the expectations. The same can be done
at the CASSCF level:

```orcainput
! HF def2-SVP UHF TightSCF PModel

%casscf nel 6 norb 6 nroots 1 end 

* xyz 0 1
N(1) 0 0 0
N(2) 0 0 1094
*
```

With the result:

```orca
<SA*SB>        1            2     
----------------------------------
   1    :     3.7500  
   2    :    -3.7500       3.7500  

               <SzA>*      Seff(A)
        --------------------------
   1    :       n.a.      1.5000
   2    :       n.a.      1.5000

* = for a singlet state all <SzA> values are zero by definition
```

Thus, cleanly confirming the expectations. In addition, if nroots > 1, the printing
will contain the state-specific analysis of all roots.

As a less trivial example, consider a typical Fe(III) antiferromatically
coupled transition metal dimer. An appropriate input may be:

```orcainput
! PBE def2-SV(P) TightSCF KDIIS SOSCF PModel

%scf
  brokensym 5,5
end

* xyz -2 1
Fe(1)	-1.93818	 0.53739	-0.00010
Fe(2)	 1.06735	 0.47031	 0.00029
S(3)	-0.38935	 2.59862	-0.00983
S(3)	-0.48170	-1.59050	 0.01091
S(1)	 2.68798	 0.43924	 1.99710
S(1)	 2.68692	 0.42704	-1.99712
S(2)	-3.55594	 0.56407	-1.99889
S(2)	-3.55850	 0.58107	 1.99646
H(1)	 3.91984	 0.39462	 1.47608
H(1)	 3.91940	 0.39536	-1.47662
H(2)	-4.78410	 0.69179	-1.48280
H(2)	-4.78991	 0.49249	 1.47983
*
```

Where one of the bridging sulfurs was assigned to each site
respectively.

```orca
 <SA*SB>        1            2            3
-----------------------------------------------
   1    :     7.3346
   2    :    -4.5300       7.3349
   3    :    -0.7229      -0.7230       1.9403

               <SzA>      Seff(A)
        --------------------------
   1    :     1.7561      2.2540
   2    :    -1.7562      2.2541
   3    :     0.0001      0.9800
```

The output from this calculation shows the expected results, with the local site spins being close to
their ideal value 2.5 which would hold for a high-spin Fe(III) ion.

<a id="sec:spectroscopyproperties.pop.UNO"></a>
## Population Analysis of UNOs

Population analyses for [UHF natural Orbitals](sec:modelchemistries.hftype.uhfno) can be requested via
the respective print options in the `%output` block:

```orca
%output
  Print[ P_UNO_OccNum     ] = 1;        # Occupation numbers
  Print[ P_UNO_AtPopMO_M  ] = 0;        # Mulliken atom pop. per UNO
  Print[ P_UNO_OrbPopMO_M] = 0;         # Mulliken orbital pop. per UNO
  Print[ P_UNO_ReducedOrbPopMO_M] = 0;  # Mulliken reduced orbital pop. per UNO
  Print[ P_UNO_AtPopMO_L  ] = 0;        # Loewdin atom pop. per UNO
  Print[ P_UNO_OrbPopMO_L] = 0;         # Loewdin orbital pop. per UNO
  Print[ P_UNO_ReducedOrbPopMO_L] = 0;  # Loewdin reduced orbital pop. per UNO
end
```

## Keywords

A collection of useful keywords in the context of population analyses is given in [tab:spectroscopyproperties.pop.keywords.simple](#tab:spectroscopyproperties.pop.keywords.simple), 
[tab:spectroscopyproperties.pop.keywords.block.output](#tab:spectroscopyproperties.pop.keywords.block.output), [tab:spectroscopyproperties.pop.keywords.block.method](#tab:spectroscopyproperties.pop.keywords.block.method), and [tab:spectroscopyproperties.pop.keywords.block.chelpg](#tab:spectroscopyproperties.pop.keywords.block.chelpg).

<a id="tab:spectroscopyproperties.pop.keywords.simple"></a>
!!! note "Simple input keywords for population analyses."
    | Keyword                         | Description                                                                                                                       |
    |:--------------------------------|:----------------------------------------------------------------------------------                                                |
    | `AllPop`                        | Activates all population analyses                                                                                                 |
    | `NoPop`                         | Deactivates all population analyses                                                                                               |
    | `ReducedPop`                    | Prints reduced orbital populations per MO                                                                                         |
    | `NoReducedPop`                  | Deactivates printing of reduced orbital populations                                                                               |
    | `Mulliken`                      | Activates [Mulliken](sec:spectroscopyproperties.pop.mulliken) population analysis                                                 |
    | `NoMulliken`                    | Deactivates Mulliken population analysis                                                                                          |
    | `Loewdin`                       | Activates [Löwdin](sec:spectroscopyproperties.pop.loewdin) population analysis                                                    |
    | `NoLoewdin`                     | Deactivates Löwdin population analysis                                                                                            |
    | `Mayer`                         | Activates [Mayer](sec:spectroscopyproperties.pop.mayer) population analysis                                                       |
    | `NoMayer`                       | Deactivates Mayer population analysis                                                                                             |
    | `NPA`                           | Activates [NPA](sec:spectroscopyproperties.pop.natural). NBO program required                                                     |
    | `NBO`                           | Activates [NPA](sec:spectroscopyproperties.pop.natural) and [NBO](sec:spectroscopyproperties.nbo) analyses. NBO program required  |
    | `NoNBO`                         | Deactivates NBO                                                                                                                   |
    | `NoNPA`                         | Deactivates NPA and NBO                                                                                                           |
    | `MBIS`                          | Activates [MBIS](sec:spectroscopyproperties.pop.mbis) population analysis                                                         |
    | `CHELPG`                        | Requests calculation of [CHELPG](sec:spectroscopyproperties.pop.chelpg) charges                                                   |
    | `CHELPG(LARGE)`                 | Requests calculation of [CHELPG](sec:spectroscopyproperties.pop.chelpg) charges with large grid                                   |

<a id="tab:spectroscopyproperties.pop.keywords.block.output"></a>
!!! note "`%output` block input keywords and options for population analyses."
    | Keyword                         | Option                    | Description                                            |
    |:--------------------------------|:--------------------------|:-------------------------------------------------------|
    | `Print[ <option> ]`             | `P_Mayer`                 | Print Mayer population analysis (Default = on)         |
    |                                 | `P_NatPop`                | Print Natural population analysis (Default = off)      |
    |                                 | `P_NPA`                   | Print Natural population analysis (Default = off)      |
    |                                 | `P_Hirshfeld`             | Print Hirshfeld population analysis (Default = off)    |
    |                                 | `P_MBIS`                  | Print MBIS population analysis (Default = off)         |
    |                                 | `P_Mulliken`              | Print Mulliken population analysis (Default = on)      |
    |                                 | `P_AtCharges_M`           | Print Mulliken atomic charges                          |
    |                                 | `P_OrbCharges_M`          | Print Mulliken orbital charges                         |
    |                                 | `P_FragCharges_M`         | Print Mulliken fragment charges                        |
    |                                 | `P_FragBondOrder_M`       | Print Mulliken fragment bond orders                    |
    |                                 | `P_BondOrder_M`           | Print Mulliken bond orders                             |
    |                                 | `P_ReducedOrbPop_M`       | Print Mulliken reduced orbital charges                 |
    |                                 | `P_FragPopMO_M`           | Print Mulliken fragment population for each MO         |
    |                                 | `P_FragOvlMO_M`           | Print Mulliken overlap populations per fragment pair   |
    |                                 | `P_AtPopMO_M`             | Print Mulliken atomic charges in each MO               |
    |                                 | `P_OrbPopMO_M`            | Print Mulliken orbital population for each MO          |
    |                                 | `P_ReducedOrbPopMO_M`     | Print Mulliken reduced orbital population for each MO  |
    |                                 | `P_Loewdin`               | Print Loewdin population analysis (Default = on)       |
    |                                 | `P_AtCharges_L`           | Print Loewdin atomic charges                           |
    |                                 | `P_OrbCharges_L`          | Print Loewdin orbital charges                          |
    |                                 | `P_FragCharges_L`         | Print Loewdin fragment charges                         |
    |                                 | `P_FragBondOrder_L`       | Print Loewdin fragment bond orders                     |
    |                                 | `P_BondOrder_L`           | Print Loewdin bond orders                              |
    |                                 | `P_ReducedOrbPop_L`       | Print Loewdin reduced orbital charges                  |
    |                                 | `P_FragPopMO_L`           | Print Loewdin fragment population for each MO          |
    |                                 | `P_FragOvlMO_L`           | Print Loewdin overlap populations per fragment pair    |
    |                                 | `P_AtPopMO_L`             | Print Loewdin atomic charges in each MO                |
    |                                 | `P_OrbPopMO_L`            | Print Loewdin orbital population for each MO           |
    |                                 | `P_ReducedOrbPopMO_L`     | Print Loewdin reduced orbital population for each MO   |
    |                                 | `P_Fragments`             | Print fragment information                             |
    |                                 | `P_GUESSPOP`              | Print initial guess populations                        |
    |                                 | `P_UNO_FragPopMO_M`       | Print Mulliken fragment population per UNO             |
    |                                 | `P_UNO_OrbPopMO_M`        | Print Mulliken orbital pop. per UNO                    |
    |                                 | `P_UNO_AtPopMO_M`         | Print Mulliken atomic charges per UNO                  |
    |                                 | `P_UNO_ReducedOrbPopMO_M` | Print Mulliken reduced orbital pop. per UNO            |
    |                                 | `P_UNO_FragPopMO_L`       | Print Loewdin fragment population per UNO              |
    |                                 | `P_UNO_OrbPopMO_L`        | Print Loewdin orbital pop. per UNO                     |
    |                                 | `P_UNO_AtPopMO_L`         | Print Loewdin atomic charges per UNO                   |
    |                                 | `P_UNO_ReducedOrbPopMO_L` | Print Loewdin reduced orbital pop. per UNO             |
    |                                 | `P_UNO_OccNum`            | Print occupation numbers per UNO                       |

<a id="tab:spectroscopyproperties.pop.keywords.block.method"></a>
!!! note "`%method` block input keywords and options for population analyses."
    :header-rows: 1
    :class: longtable
    :class: footnotesize

| Item | Value |
| --- | --- |
| **Keyword** | — |

      - Option
      - Description

| Item | Value |
| --- | --- |
| **`LOEWDIN_BONDORDERTHRESH`** | — |

      - `<real>`
      - Sets printing threshold for Löwdin bond orders (default = 0.05)

| Item | Value |
| --- | --- |
| **`MAYER_BONDORDERTHRESH`** | — |

      - `<real>`
      - Sets printing threshold for Mayer bond orders (default = 0.1)

| Item | Value |
| --- | --- |
| **`MBIS_CHARGETHRESH`** | — |

      - `<real>`
      - Sets convergence threshold for MBIS charges (default = $10^{-6}$)

| Item | Value |
| --- | --- |
| **`MBIS_LARGEPRINT`** | — |

      - `true`/`false`
      - Activate printing of [MBIS Quantities](sec:spectroscopyproperties.pop.mbis.quantities) (default = false)

| Item | Value |
| --- | --- |
| **`MBIS_ORIGIN_MULT`** | — |

      - `CenterOfCoords`
      - Sets origin for MBIS properties to center of coordinate system (0,0,0)

| Item | Value |
| --- | --- |
| **—** | — |

      - `CenterOfMass`
      - Sets origin for MBIS properties to center of mass

| Item | Value |
| --- | --- |
| **—** | — |

      - `CenterOfNucCharge`
      - Sets origin for MBIS properties to center of nuclear charge

| Item | Value |
| --- | --- |
| **—** | — |

      - `CenterXYZ`
      - Sets origin for MBIS properties to arbitrary position, set coordinates with `MBIS_ORIMULT_XYZ`

| Item | Value |
| --- | --- |
| **—** | — |

      - `CenterOfEachAtom`
      - Sets origin for MBIS properties to center of each atom (default)

| Item | Value |
| --- | --- |
| **`MBIS_ORIMULT_XYZ`** | — |

      - `<x,y,z>`
      - Set the coordinates, otherwise 0,0,0 (unit: Angstrom)

<a id="tab:spectroscopyproperties.pop.keywords.block.chelpg"></a>
!!! note "`%chelpg` block input keywords and options for CHELPG charges."
    | Keyword                         | Option                    | Description                                                                     |
    |:--------------------------------|:--------------------------|:--------------------------------------------------------------------------------|
    | `GRID`                          | `<real>`                  | Spacing of the regular grid in Å (default = 0.3)                                |
    | `RMAX`                          | `<real>`                  | Maximum distance of all atoms to any gridpoint in Å (default = 2.8)             |
    | `VDWRADII`                      | `COSMO`                   | Activates usage of COSMO VdW radii of Atoms (default)                           |
    |                                 | `BW`                      | Activates usage of Breneman, Wiberg radii                                       |
    | `DIPOLE`                        | `false`/`true`            | If true, the charges also reproduce the total dipole moment (default = `false`) |

