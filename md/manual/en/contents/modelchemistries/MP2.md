```{index} Møller-Plesset Perturbation Theory (MP2)
```

(sec:modelchemistries.mp2)=
# Perturbation Theory - MP2
In this section, we discuss the second order Møller-Plesset Perturbation Theory (MP2) and its implementation 
in the `orca_mp2` module. Higher order correlated methods, such as MP3 and MP4 theories, are available 
through computer generated code in the [AUTOCI module](sec:modelchemistries.autoci). 
(sec:modelchemistries.mp2.standard)=
## Standard (non-RI) MP2

The standard (or full accuracy) MP2 module has two different branches.
One branch is used for energy calculations, the other for gradient
calculations.

For standard MP2 energies, the program performs two half-transformations
and the half-transformed integrals are stored on disk in compressed
form. This appears to be the most efficient approach that can also be
used for medium sized molecules.The module should parallelize acceptably
well as long as I/O is not limiting.

For standard MP2 gradients, the program performs four quarter
transformations that are ordered by occupied orbitals. Here, the program
massively benefits from large core memory (`%maxcore`) since this
minimizes the number of batches that are to be done. I/O demands are
minimal in this approach.

In "memory mode" (Q1Opt\>0) basically the program treats batches of
occupied orbitals at the same time. Thus, there must be at least enough
memory to treat a single occupied MO at each pass. Otherwise the MP2
module will fail. Thus, potentially, MP2 calculations on large molecules
take significant memory and may be most efficiently done through the RI
approximation.

Alternatively, in the "disk based mode" (Q1Opt$=$-1) the program
performs a half transformation of the exchange integrals and stores the
transformed integrals on disk. A bin-sort then leads to the AO operator
$K^{ij} \left(\mu ,\nu\right)=\left(i\mu|j\nu \right)$ in (11|22) 
integral notation. These
integrals are then used to make the final K$^{ij}$(a,b) (a,b$=$virtual
MOs) and the EMP2 pair energy contributions. In many cases, and in
particular for larger molecules, this algorithm is much more efficient
than the memory based algorithm. It depends, however, much more heavily
on the I/O system of the computer that you use. It is important, that
the program uses the flags `CFLOAT, UCFLOAT, CDOUBLE` or `UCDOUBLE` in
order to store the unsorted and sorted AO exchange integrals. Which flag
is used will influence the performance of the program and to some extent
the accuracy of the result (float based single precision results are
usually very slightly less accurate; $\mu$Eh-range deviations from the
double precision result[^1]). Finally, gradients are presently only
available for the memory based algorithm since in this case a much
larger set of integrals is required.

The `! MP2` command does the following: (a) it changes the `Method` to
`HFGTO` and (b) it sets the flag `DoMP2` to `true`. The program will
then first carry out a Hartree-Fock SCF calculation and then estimate
the correlation energy by MP2 theory. RHF, UHF and high-spin ROHF
reference wavefunctions are permissible and the type of MP2 calculation
to be carried out (for high-spin ROHF the gradients are not available)
is automatically chosen based on the value of `HFTyp`. If the SCF is
carried out conventionally, the MP2 calculation will also be done in a
conventional scheme unless the user forces the calculation to be direct.
For `SCFMode` $=$`Direct` the MP2 energy evaluation will be fully in the
integral direct mode.

The following variables can be adjusted in the block for conventional
MP2 calculations:

```orca
%mp2
  EMin       -1.5       # orbital energy cutoff that defines the 
                        # frozen core in Eh
  EMax        1.0e3     # orbital energy cutoff that defines the
                        # neglected virtual orbitals in Eh
  EWin        EMin,EMax # the same, but accessed as array 
                        # (respects settings in %method block!)
  MaxCore     256       # maximum amount of memory (in MB) to be 
                        # used for integral buffering
  ForceDirect false     # Force the calculation to be integral 
                        # direct
  RI          false     # use the RI approximation
  F12         false     # apply F12 correction
  Q1Opt                 # For non-RI calculations a flag how to perform
                        # the first quarter transformation
                        #  1 - use double precision buffers
                        #      (default for gradient runs)
                        #  2 - use single precision buffers. This reduces
                        #      the memory usage in the bottleneck step by
                        #      a factor of two. If several passes are re-
                        #      quired, the number of passes is reduced by
                        #      a factor of two.
                        # -1 - Use a disk based algorithm. This respects
                        #      the flags UCFLOAT,CFLOAT,UCDOUBLE and 
                        #      CDOUBLE. (but BE CAREFUL with FLOAT)
                        #      (default for energy runs)
  PrintLevel  2         # How much output to produce. PrintLevel 3 produces
                        # also pair correlation energies and other info.
  DoSCS       false     # use spin-component scaling
  Ps          1.2       # scaling factor for ab pairs
  Pt          0.333     # scaling factor for aa and bb pairs
  Density     none      # no density construction
              unrelaxed # only "unrelaxed densities"
              relaxed   # full relaxed densities
  NatOrbs     false     # calculate natural orbitals
  
  # Generate guess natural orbitals for CASSCF:
  # "TNat" is an alias for natural orbitals with unrelaxed density 
  # omitting amplitudes < TNat. (Default = no truncation).
  TNat        0.0       # good results are obtained with 1e-6 
```

```{note}
Throughout this section, indices $i,j,k,\dots$ refer to occupied
orbitals in the reference determinant, $a,b,c,
\dots$ to virtual orbitals and $p,q,r,\dots$ to general orbitals from
either set while $\mu ,\nu ,\kappa ,\tau ,
\dots$ refer to basis functions.
```

(sec:modelchemistries.mp2.ri)=
## RI-MP2
```{index} RI-MP2
```

The RI-MP2 module is of a straightforward nature. The program first
transforms the three-index integrals $(ia|
\tilde{P})$, where "$i$" is a occupied, "$a$" is a virtual MO and
"$\tilde{P}$" is an auxiliary basis function that is orthogonalized
against the Coulomb metric. These integrals are stored on disk, which is
not critical, even if the basis has several thousand functions. The
integral transformation is parallelized and has no specifically large
core memory requirements.

In the next step, the integrals are read ordered with respect to the
occupied labels and the exchange operators
$K^{ij}(a,b) = (ia| jb) = \sum_{\tilde{P} }^{\text{NAux} } (ia | \tilde{P})(\tilde{P} | jb)$
are formed in the rate limiting O(N$^{5})$ step. This step is done with
high efficiency by a large matrix multiplication and parallelizes well.
From the exchange operators, the MP2 amplitudes and the MP2 energy is
formed. The program mildly benefits from large core memory (%maxcore) as
this minimizes the number of batches and hence reads through the
integral list.

The RI-MP2 gradient is also available. Here, all necessary intermediates
are made on the fly.

In the RI approximation, one introduces an auxiliary fitting basis
$\eta_{P} \left({ \mathrm{\mathbf{r} }} \right)$ and then approximates
the two-electron integrals in the Coulomb metric as:

$$\left({ pq\vert rs} \right)\approx \sum\limits_{PQ} { \left({ pq\vert P} 
\right)V_{PQ}^{-1} \left({ Q\vert rs} \right)} 
$$ (eqn:55)

where $V_{PQ} =\left({ P\vert Q} \right)$ is a two-index
electron-electron repulsion integral. As first discussed by Weigend and
Häser, the closed-shell case RI-MP2 gradient takes the form:

$$E_{\text{RI-MP2} }^{x} =2\sum\limits_{\mu \nu P} { \left({ \mu \nu \vert P} 
\right)^{\left( x \right)}\sum\limits_i { c_{\mu i} \Gamma_{i\nu }^{P} } } 
+\sum\limits_{RS} { V_{RS}^{x} \left({ \mathrm{\mathbf{V} }^{-1/2}\gamma \mathrm{\mathbf{V} }^{-1/2} } \right)_{RS} } +
\left\langle { \mathrm{\mathbf{DF} }^{x} } \right\rangle
$$ (eqn:56)

The **F**-matrix derivative terms are precisely handled as in the non-RI
case and need not be discussed any further. $\Gamma_{ia}^{P}$ is a
three-index two-particle "density":

$$\Gamma_{ia}^{P} =\sum\limits_{jbQ} { \left({ 1+\delta_{ij} } 
\right)\tilde{{t} }_{ab}^{ij} V_{PQ}^{-1/2} \left({ Q\vert jb} \right)} 
$$ (eqn:57)

Which is partially transformed to the AO basis by:

$$\Gamma_{i\nu }^{P} =\sum\limits_a { c_{\nu a} \Gamma_{ia}^{P} } 
$$ (eqn:58)

The two-index analogue is given by:

$$\gamma_{PQ} =\sum\limits_{iaR} { \Gamma_{ia}^{Q} \left({ ia\vert R} 
\right)V_{RP}^{-1/2} } 
$$ (eqn:59)

The RI contribution to the Lagrangian is particularly convenient to
calculate:

$$L_{ai}^{RI} =\sum\limits_\mu{ c_{\mu a} } \left[{ 2\sum\limits_{PQ\nu } 
{\Gamma_{i\nu }^{P} \left({ \mu \nu \vert Q} \right)V_{PQ}^{-1/2} } } 
\right]$$ (eqn:60)

In a similar way, the remaining contributions to the energy weighted
density matrix can be obtained efficiently. Note, however, that the
response operator and solution of the CP-SCF equations still proceed via
traditional four- index integrals since the SCF operator was built in
this way. Thus, while the derivatives of the three-index integrals are
readily and efficiently calculated, one still has the separable
contribution to the gradient, which requires the derivatives of the
four-index integrals.

The RI-MP2 energy and gradient calculations can be drastically
accelerated by employing the RIJCOSX or the RIJDX approximation.

(sec:modelchemistries.mp2.energies)=
## Calculating MP2 and RI-MP2 Energies

You can do conventional or integral direct MP2 calculations for RHF, UHF
or high-spin ROHF reference wavefunctions. MP3 functionality is not
implemented as part of the MP2 module, but can be accessed through the
MDCI module. Analytic gradients are available for RHF and
UHF. The analytic MP2-Hessians have been deprecated with ORCA-6.0. 
The frozen core approximation is used by default. For RI-MP2 the
$\langle\hat{S}^2\rangle$ expectation value is computed in the
unrestricted case according to {cite}`Lochan2007`. An extensive coverage of
MP2 exists in the
literature.{cite}`szabo1989modern,mcweeny1992methods,cremer1998ency,saebo1989chem,head1988chem,lauderdale1991chem,knowles1991chem,pople1976int,krishnan1980chem,handy1985theor,weigend1998chem,weigend1997theor,feyereisen1993chem,bernholdt1996chem`

```orcainput
! MP2 def2-TZVP TightSCF
%paras  rCO = 1.20
        ACOH = 120
        rCH  = 1.08
        end
* int 0 1
C 0 0 0 0.00 0.0 0.00
O 1 0 0 {rCO} 0.0 0.00
H 1 2 0 {rCH} {ACOH} 0.00
H 1 2 3 {rCH} {ACOH} 180.00
*
```

```{note}
There are two algorithms for MP2 calculations without the RI
  approximation. The first one uses main memory as much as possible.
  The second one uses more disk space and is usually faster (in
  particular, if you run the calculations in single precision using
  `! FLOAT, UCFLOAT or CFLOAT`). The memory algorithm is used by
  specifying `Q1Opt >0` in the `%mp2` block whereas the disk based
  algorithm is the default or specified by `Q1Opt = -1`. Gradients are
  presently only available for the memory based algorithm.
```

The RI approximation to
MP2{cite}`weigend1998chem,weigend1997theor,feyereisen1993chem,bernholdt1996chem`
is fairly easy to use, too. It results in a tremendous speedup of the
calculation, while errors in energy differences are very small. For
example, consider the same calculation as before:

```{literalinclude} ../../orca_working_input/C05S01_033.inp
:language: orca
```

Generally, the RI approximation can be switched on by setting `RI true`
in the `%mp2` block. Specification of an appropriate auxiliary basis set
("/C") for correlated calculations is required. Note that if the RIJCOSX
method (section
{ref}`sec:essentialelements.ri.rijcosx`) or the RI-JK
method (section
{ref}`sec:essentialelements.ri.rijk`) is used to accelerate
the SCF calculation, then two basis sets should be specified: firstly
the appropriate Coulomb ("/J") or exchange fitting set ("/JK"), and
secondly the correlation fitting set ("/C"), as shown in the example
below.

```orca
# Simple input line for RIJCOSX:
! RHF RI-MP2 RIJCOSX def2-TZVP def2/J def2-TZVP/C TightSCF

# Simple input line for RI-JK:
! RHF RI-MP2 RI-JK def2-TZVP def2/JK def2-TZVP/C TightSCF
```

The MP2 module can also do Grimme's spin-component scaled MP2
{cite}`Grimme2003jcp`. It is a semi-empirical modification of MP2 which
applies different scaling factors to same-spin and opposite-spin
components of the MP2 energy. Typically it gives fairly bit better
results than MP2 itself.

```{literalinclude} ../../orca_working_input/C05S01_034.inp
:language: orca
```

Energy differences with SCS-MP2 appear to be much better than with MP2
itself according to Grimme's detailed evaluation study. For the sake of
efficiency, it is beneficial to make use of the RI approximation using
the `RI-SCS-MP2` keyword. The opposite-spin and same-spin scaling
factors can be modified using `PS` and `PT` in the `%mp2` block,
respectively. By default, $\texttt{PS}=6/5$ and $\texttt{PT}=1/3$.

:::{note}
In very large RI-MP2 runs you can cut down the amount of main memory
used by a factor of two if you use the keyword `! FLOAT`. This is
more important in gradient runs than in single point runs.
Deviations from double precision values for energies and gradients
should be in the $\mu$Eh and sub-$\mu$Eh range. However, we have met
cases where this option introduced a large and unacceptable error,
in particular in transition metal calculations. You are therefore
advised to be careful and check things out beforehand.
:::

A word of caution is due regarding MP2 calculations with a linearly
dependent basis. This can happen, for example, with very diffuse basis
sets (see {ref}`sec:essentialelements.lindep` for more information). If some
vectors were removed from the basis in the SCF procedure, those
redundant vectors are still present as \"virtual\" functions with a zero
orbital energy in the MP2 calculation. When the number of redundant
vectors is small, this is often not critical (and when their number is
large, one should probably use a different basis). However, it is better
to avoid linearly dependent basis sets in MP2 calculations whenever
possible. Moreover, in such a situation the orbitals should not be read
with the `MORead` and `NoIter` keywords, as that is going to produce
wrong results!

(sec:modelchemistries.mp2.frozencore)=
## Frozen Core Options

In MP2 energy and gradient runs the Frozen Core (FC) approximation is
applied by default. This implies that the core electrons are not
included in the perturbation treatment, since the inclusion of dynamic
correlation in the core electrons usually effects relative energies or
geometry parameters insignificantly.

The frozen core option can be switched on or off with `FrozenCore` or
`NoFrozenCore` in the simple input line. Furthermore, frozen orbitals
can be selected by means of an energy window:

```orca
%method FrozenCore FC_EWIN end
%mp2 ewin -1.5, 1.0e3 end
```

More information and the different options can be found in section
{ref}`sec:essentialelements.frozencore`


(sec:modelchemistries.mp2.gradients)=
## MP2 and RI-MP2 Gradients 

Geometry optimization with MP2, RI-MP2, SCS-MP2 and RI-SCS-MP2 proceeds
just as with any SCF method. With frozen core orbitals, second
derivatives of any kind are currently only available numerically. The
RIJCOSX approximation (section
{ref}`sec:essentialelements.ri.rijcosx`) is supported in
RI-MP2 and hence also in double-hybrid DFT gradient runs (it is in fact
the default for double-hybrid DFT since ORCA 5.0). This leads to large
speedups in larger calculations, particularly if the basis sets are
accurate.

```{literalinclude} ../../orca_working_input/C05S01_036.inp
:language: orca
```

This job results in:

```orca
---------------------------------------------------------------------------
Redundant Internal Coordinates

--- Optimized Parameters ---  
(Angstroem and degrees)

Definition                    OldVal   dE/dq     Step     FinalVal
----------------------------------------------------------------------------
1. B(O   1,C   0)                1.2081  0.000488 -0.0003    1.2078   
2. B(H   2,C   0)                1.1027  0.000009 -0.0000    1.1027   
3. B(H   3,C   0)                1.1027  0.000009 -0.0000    1.1027   
4. A(O   1,C   0,H   3)          121.85  0.000026   -0.00    121.85   
5. A(H   2,C   0,H   3)          116.29 -0.000053    0.01    116.30   
6. A(O   1,C   0,H   2)          121.85  0.000026   -0.00    121.85   
7. I(O   1,H   3,H   2,C   0)     -0.00 -0.000000    0.00      0.00   
----------------------------------------------------------------------------
```

Just to demonstrate the accuracy of RI-MP2, here is the result with
RI-SCS-MP2 instead of SCS-MP2, with the addition of def2-TZVP/C:

```orca
---------------------------------------------------------------------------
Redundant Internal Coordinates

--- Optimized Parameters ---  
(Angstroem and degrees)

Definition                    OldVal   dE/dq     Step     FinalVal
----------------------------------------------------------------------------
1. B(O   1,C   0)                1.2081  0.000487 -0.0003    1.2078   
2. B(H   2,C   0)                1.1027  0.000009 -0.0000    1.1027   
3. B(H   3,C   0)                1.1027  0.000009 -0.0000    1.1027   
4. A(O   1,C   0,H   3)          121.85  0.000026   -0.00    121.85   
5. A(H   2,C   0,H   3)          116.29 -0.000053    0.01    116.30   
6. A(O   1,C   0,H   2)          121.85  0.000026   -0.00    121.85   
7. I(O   1,H   3,H   2,C   0)     -0.00  0.000000   -0.00     -0.00   
----------------------------------------------------------------------------
```

You see that *nothing* is lost in the optimized geometry through the RI
approximation thanks to the efficient and accurate RI-auxiliary basis
sets of the Karlsruhe group (in general the deviations in the geometries
between standard MP2 and RI-MP2 are very small). Thus, RI-MP2 really is
a substantial improvement in efficiency over standard MP2.

Geometric gradients can be calculated with RI-MP2 in
conjunction with the RIJCOSX method. They are called the same way as
with a conventional SCF wave function, for example to perform a geometry
optimization with tight convergence parameters:
(Please note that you have to switch on NumFreq for the MP2-Hessian,
as the analytical (RI-)MP2-Hessians are no longer available).

```orca
! RI-MP2 def2-TZVPP def2/J def2-TZVPP/C TightSCF RIJCOSX 
! TightOpt
...
```

(sec:modelchemistries.mp2.rijcosxrigrad)=
## RIJCOSX-RI-MP2 Gradients

Additional grids are introduced for the RIJCOSX-MP2 gradient. They have
sensible default settings and therefore do not usually require any
intervention from the user. However, a number of expert options are
available, as described below.

The COSX terms in the Z-vector equations are calculated on a grid,
controlled by the keywords `Z_GridX` and `Z_IntAccX`, as discussed in
sections {ref}`sec:essentialelements.numericalintegration.gridothers` and
{ref}`sec:essentialelements.cpscf`. For example, the `DefGrid3` CP-SCF COSX
grid can be requested as:

```orca
%method
  Z_GridX   2     # Lebedev 110-point grid
  Z_IntAccX 3.067 # radial integration accuracy
end
```

The grid used for evaluation of the response operator on the right-hand
side of the Z-vector equations (see for example
eqs {eq}`eqn:82` and
{eq}`eqn:RD-DHDFT`) can be independently selected using the
keyword `Z_GridX_RHS`. Note that starting with ORCA 5, the usage is
different to `Z_GridX` - the choice is between one of the three grids
used during the RIJCOSX SCF procedure: a small grid for the initial
iterations, a medium grid for the final iterations (default in ORCA 5),
and a large grid to evaluate the energy more accurately after the
iterations have converged.

```orca
%method
  Z_GridX_RHS 1  # small SCF grid
              2  # medium SCF grid (default)
              3  # large SCF grid
end
```

Yet another grid is used to evaluate basis functions derivatives.
Appropriate parameters are chosen through `! DefGridn` (in addition to
the three SCF grids), but one can override this by setting the angular
(`GridX`) and radial (`IntAccX`) grids explicitly through:

```orca
%mp2 GridX    4       # default 4: angular Lebedev grid 302
     IntAccX  4.871   # radial grid 
end
```


(sec:modelchemistries.mp2.2ndder)=
## MP2 and RI-MP2 Second Derivatives
```{index} MP2 Derivatives
```

Analytical second-order properties with the MP2, RI-MP2 and
double-hybrid DFT methods are available in ORCA for calculations without
frozen core orbitals. The most expensive term in the second derivative calculations is the four-external contribution which can be evaluated either via an AO direct (default) or a semi-numerical Chain-of-Spheres approach. In case
that the latter approach is chosen, appropriate grid parameters are
defined through the `! DefGridn` settings. However, a more fine-grained
specification is available to expert users as follows:

```orca
%mp2 KCOpt _AOBLAS          # (default) AO direct with BLAS routines
           _COSX            # semi-numerical evaluation using the COSX method
     KC_GridX    2          # default 2: angular Lebedev grid 110
     KC_IntAccX  4.020      # radial grid 
end
```

Alternatively, all the grid settings can be defined in the `%method`
block, as discussed in
section {ref}`sec:essentialelements.numericalintegration.SCFkeys`. The first three entries
define the three SCF grids, the fourth entry the MP2 grid for basis
function derivatives (refer to
section {ref}`sec:modelchemistries.mp2.rijcosxrigrad`) and the fifth entry the
grid for the four-external contribution.

```orca
%method
   IntAccX     Acc1,  Acc2,  Acc3,  Acc4,   Acc5
   GridX       Ang1,  Ang2,  Ang3,  Ang4,   Ang5
end
```

(sec:modelchemistries.mp2.properties)=
## MP2 Properties, Densities and Natural Orbitals

The MP2 method can be used to calculate electric and magnetic properties
such as dipole moments, polarizabilities, hyperfine couplings, g-tensors
or NMR chemical shielding tensors. For this purpose, the appropriate MP2
density needs to be requested - otherwise the properties are calculated
using the SCF density!

Two types of densities can be constructed - an \"unrelaxed\" density
(which basically corresponds to the MP2 expectation value density) and a
\"relaxed\" density which incorporates orbital relaxation. For both sets
of densities a population analysis is printed if the SCF calculation
also requested this population analysis. These two densities are stored
as `JobName.pmp2ur.tmp` and `JobName.pmp2re.tmp`, respectively. For the
open shell case case the corresponding spin densities are also
constructed and stored as `JobName.rmp2ur.tmp` and `JobName.rmp2re.tmp`.

In addition to the density options, the user has the ability to
construct MP2 natural orbitals. If relaxed densities are available, the
program uses the relaxed densities and otherwise the unrelaxed ones. The
natural orbitals are stored as `JobName.mp2nat` which is a GBW type file
that can be read as input for other jobs (for example, it is sensible to
start CASSCF calculations from MP2 natural orbitals). The density
construction can be controlled separately in the input file (even
without running a gradient or optimization) by:

```orca
#
# MP2 densities and natural orbitals
#
%mp2  Density none         # no density
              unrelaxed    # unrelaxed density
              relaxed      # relaxed density
      NatOrbs true         # Natural orbital construction on or off
      end
```

Below is a calculation of the dipole and quadrupole moments of a water
molecule:

```{literalinclude} ../../orca_working_input/C05S01_037.inp
:language: orca
```

Another example is a simple g-tensor calculation with MP2:

```{literalinclude} ../../orca_working_input/C05S01_038.inp
:language: orca
```

NMR chemical shielding as well as g-tensor calculations with GIAOs are
only available for RI-MP2. The input for NMR chemical shielding looks as
follows:

```{literalinclude} ../../orca_working_input/C05S01_039.inp
:language: orca
```

Note that by default core electrons are not correlated unless the
`NoFrozenCore` keyword is present.

For details, see
sections {ref}`sec:modelchemistries.mp2` and
{ref}`sec:spectroscopyproperties.properties.eprnmr.MP2magnetic`.


(sec:modelchemistries.mp2.rimp2.response)=
## RI-MP2 and Double-Hybrid DFT Response Properties

Starting from ORCA 5, both the electric (for the dipole polarizability)
and the magnetic (for NMR shielding and the EPR g-tensor) field response
as well as the nucleus-orbit response (hyperfine couplings
$A_\text{orb}$ term) for RI-MP2 (and double-hybrid functionals) is
handled by a different implementation of the RI-MP2 second derivatives
than that used for geometric Hessian calculations
({ref}`sec:modelchemistries.mp2.2ndder`). This code is more efficient, uses
the RI approximation throughout (including the four-external
contribution) and supports frozen core orbitals. The implementation is
described in detail in refs {cite}`Stoychev2018RIMP2NMR,Tran2020RIMP2GIAO`.
Consider the following input for a GIAO-RI-MP2 NMR shielding
calculation:

```{literalinclude} ../../orca_working_input/ri-mp2_giao_nmr_details.inp
:language: orca
```

By default perturbed canonical orbitals are used for the occupied block,
i.e., the internal orbital rotation coefficients are chosen as

$$U^{\mathbf B}_{ij} = \frac{F^{(\mathbf B) }_{ij} - S^{(\mathbf B) }_{ij}\varepsilon_{j} }{\varepsilon_{j}-\varepsilon_{i} }$$

which results in $F^{\mathbf B}_{ij}=0$, thereby eliminating its
contribution to the perturbed amplitudes:

$$
T^{ij,\mathbf B}_{ab} \gets
- \sum_k \left[ T^{ik}_{ab} F_{kj}^\mathbf B + T^{kj}_{ab} F_{ki}^\mathbf B \right]
$$ (eq:MP2-TijB)

If $| \epsilon_j - \epsilon_i |<$ `PertCan_EThresh` or $|U_{ij}^B| > $ `PertCan_UThresh`, then
$U^{\mathbf B}_{ij}$ is chosen using the standard formula

$$U^{\mathbf B}_{ij} = - \frac{1}{2} S^{(\mathbf B) }_{ij}$$

And the relevant contributions to
eq {eq}`eq:MP2-TijB` are added, unless
$\left|F^{\mathbf B}_{ij}\right|< $ `FCut`. The required amplitudes
$\mathbf T^{ik}$ and $\mathbf T^{kj}$ (all amplitudes, in case
`UsePertCanOrbs = false`) are stored on disk if
`RespStoreT = true` or recalculated as needed otherwise.
The latter option is significantly slower and not recommended unless
disk space is an issue. Similarly, in the case of insufficient RAM, the
option `RespDijConv = true` tells ORCA to store all
amplitudes in the batch (required to calculate $D_{ij}^\mathbf B$) on
disk, rather than keep them in memory. The 3-index 2-particle densities,
needed for the right-hand side of the Z-vector equations, are always stored on disk.

Note also that in this implementation the RIJCOSX Fock-response terms
are calculated with one of the SCF grids, chosen with `Z_GridX_RHS` (see
section {ref}`sec:essentialelements.cpscf`).

```{index} DLPNO-MP2
```
(sec:modelchemistries.mp2.dlpno)=
## Local MP2 calculations (DLPNO-MP2)

Purely domain-based local MP2 methodology dates back to Pulay and has
been developed further by Werner, Schütz and co-workers. ORCA features a
local MP2 method (DLPNO-MP2) that combines the ideas of domains and
local pair natural orbitals, so that RI-MP2 energies are reproduced
efficiently to within chemical accuracy.
Its default thresholds are chosen to reproduce about 99.9% of the
total RI-MP2 correlation energy, resulting in an accuracy of a fraction of $1\,\text{kcal/mol}$ for
energy differences.
Due to the intricate connections with other DLPNO methods, reading of the section
{ref}`sec:modelchemistries.mdci.localcorrelation` is recommended. A full
description of the method for RHF reference wave functions has been
published.{cite}`pinski2015lmp2`

The local MP2 method becomes truly beneficial for very large molecules and can be used to compute
energies of systems containing several hundred atoms. {numref}`fig:DLPNO-MP2-scaling` shows the scaling behavior for linear
alkane chains. Note that this represents an idealized situation. For
three-dimensional molecules the crossover with canonical RI-MP2 is going
to occur at a later point.

(fig:DLPNO-MP2-scaling)=
```{figure} ../../images/DLPNO_MP2_Scaling.*
Scaling of the DLPNO-MP2 method with default thresholds for linear
alkane chains in def2-TZVP basis. Shown are also the times for the
corresponding Hartree-Fock calculations with RIJCOSX and for
RI-MP2.
```

Since DLPNO-MP2 employs an auxiliary basis set to evaluate integrals,
its energies converge systematically to RI-MP2 as thresholds are
tightened. The computational effort of DLPNO-MP2 with default settings
is usually comparable with or less than that of a Hartree-Fock
calculation. However, for small and medium-sized molecules, RI-MP2 is
even faster than DLPNO-MP2.

Calculations on open-shell systems are supported through a UHF
treatment. While most approximations are consistent between the RHF and
UHF versions, this is not true for the PNO spaces. **DLPNO-MP2 gives
different energies for closed-shell molecules in the RHF and UHF
formalisms. When calculating reaction energies or other energy
differences involving open-shell species, energies of closed-shell
species must also be calculated with UHF-DLPNO-MP2, and not with
RHF-DLPNO-MP2.** As for canonical MP2, ROHF reference wave functions are
subject to an ROMP2 treatment through the UHF machinery. It is not
consistent with the RHF version of DLPNO-MP2, unlike in the case of
RHF-/ROHF-DLPNO-CCSD.

In the following, the most important design principles of the
RHF-DLPNO-MP2 are pointed out:

Both DLPNO-CCSD(T) and DLPNO-MP2 are linear-scaling methods (albeit
the former has a larger prefactor). This means that if a DLPNO-MP2
calculation can be performed, DLPNO-CCSD(T) is often going to be
within reach, too. However, CCSD(T) is generally much more accurate
than MP2 and thus should be given preference.

A correlation fitting set must be provided, as the method makes use
of the RI approximation.

Canonical RI-MP2 energy differences are typically reproduced to
within a fraction of $1\,\text{kcal/mol}$. The default thresholds
have been chosen so as to reproduce about $99.9\,\%$ of the total
RI-MP2 correlation energy.

The preferred way to control the accuracy of the method is by means
of specifying "LoosePNO", "NormalPNO" and "TightPNO" keywords.
"NormalPNO" corresponds to default settings and does not need to be
given explicitly. More details and an exhaustive list of input
parameters are provided in section
{ref}`sec:modelchemistries.mp2.dlpno`. Note that the thresholds differ
from DLPNO coupled cluster.

Results obtained from RI-MP2 and DLPNO-MP2, or from DLPNO-MP2 with
different accuracy settings, must never be mixed, such as when
computing energy differences. In calculations involving open-shell
species, even the closed-shell molecules need to be subject to a UHF
treatment.

Spin-component scaled DLPNO-MP2 calculations are invoked by using
the `! DLPNO-SCS-MP2` keyword instead of `! DLPNO-MP2` in the simple
input line. Weights for same-spin and opposite-spin contributions
can be adjusted as described for the canonical SCS-MP2 method.
Likewise, there is a `DLPNO-SOS-MP2` keyword to set the parameters
defined by the SOS-MP2 method (but there is no Laplace
transformation involved).

The frozen core approximation is used by default. If core orbitals
are involved in the calculation, they are subject to the treatment
described in section
{ref}`sec:modelchemistries.mp2.dlpno`.

Calculations can be performed in parallel.

It may be beneficial to accelerate the Hartree-Fock calculation by
means of the RIJCOSX method (requiring specification of a second
auxiliary set).

Unlike in the 2013 version of the DLPNO methodology, domains are
selected by means of the differential overlap
$\sqrt{\int i^2(\mathbf{r}) \tilde\mu'^2 (\mathbf{r}) d\mathbf{r} }$
between localized MOs $i$ and projected atomic orbitals (PAOs)
$\tilde\mu'$ which are normalized to unity. The default value for
the corresponding cutoff is $T_\text{CutDO}=10^{-2}$.

MP2 amplitudes for each pair of localized orbitals $ij$ are
expressed in a basis of pair natural orbitals (PNOs)
$\tilde a_{ij}$. PNOs are obtained from diagonalization of an
approximate, "semicanonical" MP2 pair density $\mathbf{D}^{ij}$.
Only PNOs with an occupation number $>T_\text{CutPNO}$ are retained,
with a default value of $T_\text{CutPNO} = 10^{-8}$ for DLPNO-MP2. The
pair density is given by:

$$\mathbf{D}^{ij} = \mathbf{T}^{ij\dagger} \tilde{\mathbf{T} }^{ij} + \mathbf{T}^{ij} \tilde{\mathbf{T} }^{ij\dagger}
\quad\text{where}\quad
\begin{matrix}T^{ij}_{\tilde\mu\tilde\nu} = -\dfrac{\left(i\tilde\mu \middle| j \tilde\nu\right)}{\varepsilon_{\tilde\mu} + \varepsilon_{\tilde\nu} - F_{ii} - F_{jj} } \\
\tilde{\mathbf{T} }^{ij} = \left(1+\delta_{ij}\right)^{-1} \left( 4\mathbf{T}^{ij} - 2\mathbf{T}^{ij\dagger}\right)\end{matrix}$$

Since the occupied block of the Fock matrix is not diagonal in the
basis of localized orbitals, the MP2 amplitudes $\mathbf{T}^{ij}$
are obtained by solving the following set of residual equations
iteratively (where subscripts of PNOs have been dropped):

$$R^{ij}_{\tilde a\tilde b} = \left(i \tilde a \middle| j \tilde b\right) + \left( \varepsilon_{\tilde a} + 
\varepsilon_{\tilde b} - F_{ii} - F_{jj} \right) T^{ij}_{\tilde a\tilde b} - \sum_{k\neq i} \sum_{\tilde c\tilde d} 
F_{ik} S^{ij, kj}_{\tilde a\tilde c} T^{kj}_{\tilde c \tilde d}  S^{kj, ij}_{\tilde d\tilde b} - \sum_{k\neq j} 
\sum_{\tilde c\tilde d} F_{kj} S^{ij, ik}_{\tilde a\tilde c} T^{ik}_{\tilde c \tilde d}  S^{ik, ij}_{\tilde d\tilde 
b} = 0$$

The largest part of the error relative to canonical RI-MP2 is
controlled by the domain (`TCutDO`) and PNO (`TCutPNO`) thresholds,
which should be adequate for most applications. If increased
accuracy is needed (e.g. for studying weak interactions), tighter
truncation criteria can be invoked by means of the `! TightPNO`
keyword. Conversely, a less accurate but faster calculation can be
performed with the `! LoosePNO` keyword. For more details refer to
table {numref}`tab:Settings-LMP2`.

Fitting domains are determined by means of orbital Mulliken
populations with a threshold $T_\text{CutMKN}
=10^{-3}$. This threshold results in an error contribution that is
typically about an order of magnitude smaller than the overall total
energy deviation from RI-MP2.

Prior to performing the local MP2 calculation, pairs of localized
molecular orbitals $ij$ are prescreened using an MP2 energy estimate
with a dipole approximation, and the differential overlap integral
between orbitals $i$ and $j$. This procedure has been chosen
conservatively and leads to minimal errors.

Residual evaluation can be accelerated significantly by neglecting
terms with associated Fock matrix elements $F_{ik}$ and $F_{kj}$
below $F_\text{Cut}=10^{-5}$. Errors resulting from this
approximation are typically below $1\,\mu\text{E}_\text{h}$ and thus
negligible.

Sparsity of the MO and PAO coefficient matrices in atomic orbital
basis is exploited to accelerate integral transformations for large
systems. Truncation of the coefficients is controlled by a parameter
$T_\text{CutC}$. Neglect of these coefficients has to be performed
very carefully in order to avoid uncontrollable errors. The
threshold has been chosen so as to make the errors essentially
vanish.

By default, core orbitals are frozen in the MP2 module. However, if
core orbitals are subject to an MP2 treatment, it is necessary to
use a tighter PNO cutoff for pairs involving at least one core
orbital. For this purpose core orbitals and valence orbitals are
localized separately. The cutoff for pairs involving core orbitals
is given by $T_\text{CutPNO} \times T_\text{ScalePNO\_Core}$, where
$T_\text{ScalePNO\_Core}=10^{-2}$ by default. For more details refer to
section {ref}`sec:modelchemistries.mdci.dlpnocorepno`.

The UHF-DLPNO-MP2 implementation differs somewhat from the RHF case,
particularly regarding construction of PNOs, as described below.

A separate set of PAOs $\tilde\mu'_\alpha$ and $\tilde\mu'_\beta$ is
obtained for each spin case.

For $\alpha\beta$ pairs, separate pair domains of PAOs need to be
determined for each spin case. For example, the $\alpha$ pair domain
$\left[i_\alpha j_\beta\right]_\alpha$ is the union of the domains
$\left[i_\alpha\right]_\alpha$ and $\left[j_\beta\right]_\alpha$.
The latter domain $\left[j_\beta\right]_\alpha$ is determined by
evaluating the spatial differential overlap between $j_\beta$ and
$\alpha$-spin PAOs $\tilde\mu'_\alpha$.

One set of PNOs is needed for each same-spin pair. Opposite-spin
pairs require a set of $\alpha$-PNOs and a set of $\beta$-PNOs. In
total this results in four types of PNO sets.

Semicanonical amplitudes are obtained as follows, where $i,j$ are
spin orbitals and $\tilde\mu\tilde\nu$ are nonredundant spin PAOs.

$$T^{ij}_{\tilde\mu\tilde\nu} = -\frac{\left\langle ij \middle|\middle| \tilde\mu\tilde\nu \right\rangle}{\varepsilon_{\tilde\mu} + \varepsilon_{\tilde\nu} - F_{ii} - F_{jj} }$$

In the same-spin case
$\left\langle i_\alpha j_\alpha \middle|\middle| \tilde\mu_\alpha\tilde\nu_\alpha 
\right\rangle= \left\langle i j \middle| \tilde\mu \tilde\nu \right\rangle- \left\langle i j \middle| \tilde\nu 
\tilde\mu \right\rangle$, while in the opposite-spin case
$\left\langle i_\alpha j_\beta \middle|\middle| 
\tilde\mu_\alpha\tilde\nu_\beta \right\rangle= \left\langle i j \middle| \tilde\mu \tilde\nu \right\rangle$.

For opposite-spin pairs, $\alpha$-PNOs and $\beta$-PNOs are obtained
from diagonalisation of $\mathbf{T}^{ij} 
\mathbf{T}^{ij\dagger}$ and
$\mathbf{T}^{ij\dagger} \mathbf{T}^{ij}$, respectively. For
same-spin pairs the pair density is symmetric and only one set of
PNOs is needed. PNOs are discarded whenever the absolute value of
their natural occupation number is below the threshold
$T_\text{CutPNO}$.

The following residual equations need to be solved for the cases
$R^{i_\alpha j_\alpha}_{\tilde a_\alpha 
\tilde b_\alpha}$,
$R^{i_\beta j_\beta}_{\tilde a_\beta \tilde b_\beta}$ and
$R^{i_\alpha j_\beta}_{\tilde a_\alpha 
\tilde b_\beta}$:

$$\begin{split}
R^{i_\sigma j_\tau}_{\tilde a_\sigma\tilde b_\tau} =& \left\langle i j \middle|\middle| \tilde a \tilde b 
\right\rangle+ \left( \varepsilon_{\tilde a} + \varepsilon_{\tilde b} - F_{ii} - F_{jj} \right) T^{ij}_{\tilde 
a\tilde b} \\
&- \sum_{k_\sigma \neq i_\sigma} \sum_{\tilde c_\sigma \tilde d_\tau} F_{ik} S^{ij, kj}_{\tilde a\tilde c} T^{kj}
_{\tilde c \tilde d}  S^{kj, ij}_{\tilde d\tilde b} - \sum_{k_\tau \neq j_\tau} \sum_{\tilde c_\sigma \tilde d_\tau} 
F_{kj} S^{ij, ik}_{\tilde a\tilde c} T^{ik}_{\tilde c \tilde d}  S^{ik, ij}_{\tilde d\tilde b} = 0
\end{split}$$

Most approximations are consistent between the RHF and UHF schemes,
with the exception of the PNO truncation. This means that results
would match for closed-shell molecules with $T_\text{CutPNO}=0$
(provided both Hartree-Fock solutions are identical), but this is
not true whenever the PNO space is truncated. Therefore,
UHF-DLPNO-MP2 energies should only be compared to other
UHF-DLPNO-MP2 energies, even for closed-shell species.

We found that it is necessary to use tighter PNO thresholds for
UHF-DLPNO-MP2. With NormalPNO settings the default value is
$T_\text{CutPNO} = 10^{-9}$. For an overview of accuracy settings
refer to table {numref}`tab:Settings-LMP2`. As in the RHF implementation, the
PNO cutoff for pairs involving core orbitals is scaled with
$T_\text{ScalePNO\_Core}$.


Input for DLPNO-MP2 requires little specification from the user:

```orca
# DLPNO-MP2 calculation with standard settings
# sufficient for most purposes
! def2-TZVP def2-TZVP/C DLPNO-MP2 TightSCF

# OR: DLPNO-MP2 with tighter thresholds
# May be interesting for weak interactions, calculations with diffuse basis sets etc.
! def2-TZVP def2-TZVP/C DLPNO-MP2 TightPNO TightSCF

%maxcore 2000

*xyz 0 1
... (coordinates)
*
```

Explicit correlation has been implemented in the DLPNO-MP2-F12
methodology for RHF reference wave functions.{cite}`pavosevic2016lmp2f12` The
available approaches are C (keyword `! DLPNO-MP2-F12`) and the somewhat
more approximate D (keyword `! DLPNO-MP2-F12/D`). Approach D is
generally recommended as it results in a significant speedup while
leading only to small errors relative to approach C. In addition to the
MO and correlation fitting sets, a CABS basis set is also required for
both F12 approaches as shown below.

```orca
# DLPNO-MP2-F12 calculation using approach C
! cc-pVDZ-F12 aug-cc-pVDZ/C cc-pVDZ-F12-CABS DLPNO-MP2-F12 TightSCF

# OR: DLPNO-MP2-F12 calculation using approach D (recommended)
! cc-pVDZ-F12 aug-cc-pVDZ/C cc-pVDZ-F12-CABS DLPNO-MP2-F12/D TightSCF
```

(tab:Settings-LMP2)=
:::{table} Accuracy settings for DLPNO-MP2.
| Setting   |  $T_\text{CutDO}$  | $T_\text{CutPNO}$ (RHF) | $T_\text{CutPNO}$ (UHF) |
|:----------|:------------------:|:-----------------------:|:-----------------------:|
| LoosePNO  | $2 \times 10^{-2}$ |        $10^{-7}$        |        $10^{-8}$        |
| NormalPNO | $1 \times 10^{-2}$ |        $10^{-8}$        |        $10^{-9}$        |
| TightPNO  | $5 \times 10^{-3}$ |        $10^{-9}$        |       $10^{-10}$        |

:::

Options specific to DLPNO-MP2 are listed below.

```orca
%mp2 DLPNO            false  # Do DLPNO-MP2 (also requires RI true)
     TolE             1e-6   # Energy convergence threshold. Default: TolE of SCF
     TolR             5e-6   # Residual convergence threshold. Default: 5 * TolE
     MaxPNOIter       100    # Maximum number of residual iterations
     MaxLocIter       128    # Maximum number of iterations for orbital
                             # localization
     LocMet           AHFB   # Localization method
                             # options: FB, PM, IAOIBO, IAOBOYS, NEWBOYS, AHFB
     LocTol           1e-6   # Localization convergence tolerance
                             # Default: 0.1 * TolG from SCF
     DIISStart_PNO    0      # First iteration to invoke DIIS extrapolation
     MaxDIIS_PNO      7      # length of DIIS vector
     Damp1_PNO        0.5    # Damping before DIIS is started
     Damp2_PNO        0.0    # Damping with DIIS
     MP2Shift_PNO     0.2    # level shift in amplitude update (Eh)
# Truncation parameters:
     TCutPNO          1e-8   # PNO occupation number cutoff (RHF)
                      1e-9   # PNO occupation number cutoff (UHF)
     TScalePNO_Core   1e-2   # Core PNO scaling factor
     TCutDO           1e-2   # Differential overlap cutoff for domain selection
     TCutMKN          1e-3   # Mulliken population cutoff for fitting
                             # domain selection
     FCut             1e-5   # Occupied Fock matrix element cutoff
     TCutPre          1e-6   # Energy threshold for dipole prescreening
     TCutDOij         1e-5   # Maximum differential overlap between screened MOs
     TCutDOPre        3e-2   # Cutoff to select PAOs for domains in prescreening
     TCutC            1e-3   # Cutoff for PAO coefficient truncation
     ScaleTCutC_MO    1.0    # Cutoff for MO truncation: TCutC * ScaleTCutC_MO
     PAOOverlapThresh 1e-8   # Threshold for constructing non-redundant PAOs
end
```

(sec:modelchemistries.mp2.dlpnograd)=
## Local MP2 gradients

The analytical gradient has been implemented for the RHF variant of the
DLPNO-MP2 method.{cite}`Pinski2018GradientCommunication,Pinski2019` It is a
complete derivative of all components in the DLPNO-MP2 energy, and the
results are therefore expected to coincide with numerical derivatives of
DLPNO-MP2 (minus the noise).

General remarks:

No gradient is presently implemented for the UHF-DLPNO-MP2 variant.

Spin-component scaled MP2 is supported by the gradient.

Double-hybrid density functionals are supported by the gradient.

Only Foster-Boys localization is presently supported. The default
converger is `AHFB` with a convergence tolerance that is
automatically bound by a constant factor to the SCF orbital gradient
tolerance. Using a different converger is possible, but discouraged,
as the orbital localization needs to be sufficiently tightly
converged.

When calculating properties without the full nuclear gradient, the
relaxed MP2 density should be requested.

A number of points regarding geometry optimizations (not all of them
specific to DLPNO-MP2) are worth keeping in mind:

As of 2018, we expect that the DLPNO-MP2 gradient can most
beneficially be used for geometry optimizations of systems
containing around 70-150 atoms. It may be faster than RI-MP2 even
for systems containing 50-60 atoms or less, but the timing
difference is probably not going to be very large. Of course,
structures containing 200 atoms and above can (and have been)
optimized, but this may take long if many geometry steps are
required. On the other hand, single point gradient or density
calculations can be performed for systems containing many hundred
atoms.

DLPNO-MP2 is a substantially more expensive method for geometry
optimizations than GGA or hybrid DFT functionals. Therefore, it is
generally a good idea to start a geometry optimization with a
structure that is already optimized at dispersion-corrected DFT
level.

RIJCOSX can be used to accelerate exchange evaluation substantially.
However, great care needs to be exercised with the grid settings.
Insufficiently large grids may lead, for example, to non-planar
distortions of planar molecules. The updated default grids in ORCA 5
(`DefGrid2-3`) should be sufficiently accurate to optimize neutral
main group compounds. We therefore recommend these grids for general
use with some careful checking in more complicated cases. Even with
these grids, the calculation is a lot faster than \"regular\"
Hartree-Fock with basis sets of triple zeta quality (or larger).

Using RIJONX is also possible.

Sufficiently large grids should be used for the exchange-correlation
functional of double hybrids. The SCF calculation takes only a
fraction of the time that is needed for DLPNO-MP2, and sacrificing
quality because of an insufficiently accurate grid is a waste of
computer time.

Optimization of large structures is often a challenge for the
geometry optimizer. It may help to change the trust radius settings,
to modify the settings of the `AddExtraBonds` feature, or to change
other settings of the geometry optimizer. Sometimes it may be
beneficial to check the geometry optimizer settings with a less
demanding electronic structure method.

Finally, problems with a geometry optimization may in some cases
indeed be caused by the DLPNO approximations. Using `LoosePNO` for
accurate calculations is not recommended anyway, and difficulties
with `NormalPNO` settings are possibly rectified by switching to
`TightPNO`.

During the development process, a number of difficulties were
encountered related to the orbital localization Z-vector equations.
Great care was taken to work around these problems and to make the
procedures as robust as possible, but a number of settings can be
changed. For more information on these aspects, we recommend consulting
the full paper on the DLPNO-MP2 gradient {cite}`Pinski2019`.

Several different solvers are implemented for the orbital
localization Z-vector equations. The default is an iterative
conjugate gradient solver. As an alternative, the DIIS-accelerated
Jacobi solver can be used, but it tends to be inferior to the
conjugate gradient solver. Moreover, a direct solver is available as
a fail-safe alternative for smaller systems. As the dimension of the
linear equation system is $n(n-1)/2$ for $n$ occupied orbitals, the
memory requirement and FLOP count increase as $O(n^4)$ and $O(n^6)$,
respectively, and using the direct solver becomes unfeasible for
large systems.

Settings for the CPSCF solver are specified the same way as for
canonical MP2.

Under specific circumstances, the orbital Hessian of the orbital
localization function may have zero or near-zero eigenvalues, which
can lead to singular localization Z-vector equations. In particular,
it is typically a consequence of continuously degenerate localized
orbitals, which may (but do not need to) appear in some molecular
symmetries.{cite}`Scheurer2000` A typical symptom are natural occupation
number above 2 and below 0 for systems that would be expected to
have MP2 density eigenvalues between 2 and 0 without the DLPNO
approximations.

In order to work around the aforementioned problem, a procedure has
been implemented to eliminate singular or near-singular eigenvectors
of the localization function orbital Hessian. Vectors with an
eigenvalue smaller than `ZLoc_EThresh` (or `ZLoc_EThresh_core` for
the core orbitals) are subject to the modified procedure. If the
program eliminates any eigenvectors, it might sometimes be a good
idea to check if calculated properties are reasonable (or at least
to check the natural occupation numbers). Eigenvectors of the
Hessian are calculated by Davidson diagonalization by default, but
direct diagonalization can be chosen for smaller systems, instead.

Diagonalization of the localization orbital Hessian can be switched
off altogether by setting `ZLoc_EThresh` to 0.

If the \"Asymmetric localization equation residual norm\" exceeds
the localization Z-vector equation tolerance (`ZLoc_Tol`), there are
typically two plausible reasons: (1) the localized orbitals are not
sufficiently tightly converged (too large `LocTol`) or unconverged,
or (2) the orbital localization Hessian has got small eigenvalues
that were not eliminated.

Usage is as simple as that of RI-MP2. For example, the following input calculates
the gradient and the natural orbitals:

```{literalinclude} ../../orca_working_input/dlpno-mp2-gradient.inp
:language: orca
```

The implementation supports spin-component scaling and can be used
together with double-hybrid density functionals. The latter are invoked
with the name of the functional preceded by \"`DLPNO-`\". A simple
geometry optimization with a double-hybrid density functional is
illustrated in the example below:

```{literalinclude} ../../orca_working_input/dlpno-b2plyp-gradient.inp
:language: orca
```

For smaller systems, the performance difference between DLPNO-MP2 and
RI-MP2 is not particularly large, but very substantial savings in
computational time over RI-MP2 can be achieved for systems containing
more than approximately 70-80 atoms.

Since MP2 is an expensive method for geometry optimizations, it is
generally a good idea to use well-optimized starting structures
(calculated, for example, with a dispersion-corrected DFT functional).
Moreover, it is highly advisable to employ accurate Grids for RIJCOSX or
the exchange-correlation functional (if applicable), as the SCF
iterations account only for a fraction of the overall computational
cost. If calculating calculating properties without requesting the
gradient, `Density Relaxed` needs to be specified in the `%MP2-block`.

Only the Foster-Boys localization scheme is presently supported by the
derivatives implementation. The default localizer in DLPNO-MP2 is
`AHFB`, and changing this setting is strongly discouraged, since tightly
converged localized orbitals are necessary to calculate the gradient.

This is an overview over the options related to the gradient:

```orca
# Settings specific to the localization equation z-solver
%mp2 ZLoc_Solver        CG      # Use conjugate gradient solver (default)
                        DIR     # Use direct solver
                        JAC     # Use DIIS-accelerated Jacobi solver
     ZLoc_Tol           1.0e-3  # Residual convergence tolerance for the
                                # localization Z-solver
                                # Default: same value as Z_Tol for CPSCF
     ZLoc_MaxIter       1024    # Maximum localization Z-solver iterations
     ZLoc_MaxDIIS       10      # Number of DIIS vectors for the Jacobi solver
     ZLoc_Shift         0.2     # Shift for the Jacobi solver
# Options for eliminating (near-)singular eigenvectors of the
# orbital Hessian of the localization function.
     ZLoc_EThresh       3.0e-4  # Eigenvectors with an eigenvalue below
                                # this threshold are eliminated.
     ZLoc_EThresh_core  3.0e-4  # Same as ZLoc_EThresh, but for the core orbitals.
                                # Default: identical value as ZLoc_EThresh.
# Options for determining eigenvectors of the localization orbital Hessian.
     ZLoc_UseDavidson   True    # Use Davidson diagonalization.
                                # If false, use direct diagonalization.
     ZLoc_DVDRoots      32      # Number of Davidson roots to be determined.
     ZLoc_DVDNIter      256     # Number of Davidson iterations.
     ZLoc_DVDTolE       3.0e-10 # Eigenvalue tolerance for the Davidson solver.
                                # Default: 1e-6 * ZLoc_EThresh
     ZLoc_DVDTolR       1.0e-7  # Residual tolerance for the Davidson solver.
                                # Default: 0.1 * (ZLoc_Tol)^2
     ZLoc_DVDMaxDim     10      # During Davidson diagonalization, the space of
                                # trial vectors is expanded up to
				# MaxDim * DVDRoots.
# Choice of the PNO processing algorithm.
     DLPNOGrad_Opt      AUTO      # Chooses automatically between RAM and DISK
                                  # (default and recommended)
                        RAM       # Enforce memory-based one-pass algorithm
                        DISK      # Enforce disk-based two-pass algorithm
                        BUFFERED  # Buffered algorithm. Usage is discouraged.
                                  # Experimental, unpredictable I/O performance.
end
```

(sec:modelchemistries.mp2.dlpnoresp)=
## Local MP2 Second Derivatives and Response Properties

Analytical second derivatives with respect to electric and magnetic
fields are implemented for closed-shell DLPNO-MP2 (as well as
double-hybrid DFT).{cite}`StoychevDLPNO-MP2Response` Thus, analytic dipole
polarizability and NMR shielding tensors (with our without GIAOs) are
available. The implementation supports spin-component scaling and double-hybrid functionals. Errors in the
calculated properties are well below 0.5% when `NormalPNO` thresholds
are used.
Refer to section {ref}`sec:modelchemistries.mp2.dlpnoresp` for more information about the
DLPNO-MP2 second derivatives implementation, as well as to the sections
on electric ({ref}`sec:spectroscopyproperties.elprop`) and magnetic
({ref}`sec:spectroscopyproperties.properties.eprnmr`) properties and CP-SCF
settings ({ref}`sec:essentialelements.cpscf`).
All considerations and options discussed in sections {ref}`sec:modelchemistries.mp2.dlpno` and
{ref}`sec:modelchemistries.mp2.dlpnograd` apply here as well, while
additional remarks specific to second derivatives are given below.

DLPNO-MP2 response property calculations are expected to be faster
than the RI-MP2 equivalents for systems larger than about 70 atoms
or 300 correlated electrons.

Using the `NormalPNO` default thresholds, relative errors in the
calculated properties, due to the local approximations, are smaller
than 0.5%, or 5--10 times smaller than the inherent inaccuracy of
MP2 vs a more accurate method like CCSD(T).

DLPNO-MP2 second derivatives are much more sensitive to near-linear
dependencies and other numerical issues than the energy or
first-order properties. We have made efforts to choose reasonable
and robust defaults, however we encourage the user to be critical of
the results and to proceed with caution, especially if diffuse basis
sets or numerical integration (DFT, COSX) are used. In the latter
case, `DefGrid3` is recommended.

In particular, the near-redundancy of PAO domains introduces
numerical instabilities in the algorithm. Hence, these should be
truncated at `PAOOverlapThresh=1e-5`, which is higher than the
default for the energy and gradient. Therefore, the energy and
gradient in jobs, which include response property calculations, may
deviate from jobs, which do not. The difference is much smaller than
the accuracy of the method (vs RI-MP2) but it is still advisable to
use the same value of `PAOOverlapThresh` in all calculations, when
calculating, e.g., relative energies.

For the same reason, if diffuse basis sets are used, it is advised
to set `SThresh=1e-6` in the `%scf` block.

Another instability arises due to small differences between the
occupation number of kept and discarded PNOs and may result in very
large errors. The smallest difference is printed during the
DLPNO-MP2 relaxed density calculation:

::: ORCAoutput 0
Smallest occupation number difference between PNOs and complementary
PNOs. Absolute: 3.10e-10 Relative: 3.28e-02
:::

We found that a relative difference under $10^{-3}$, which is not
uncommon, may be cause for concern. To regularize the unstable
equations, a level shift is applied, which is equal to
$T_\text{CutPNO}$ multiplied by $T_\text{ScalePNO\_LShift}$. A
reasonable value of `TScalePNO_LShift=0.1` is set by default for
response property calculations but not for gradient (or energy)
calculations, as these were not found to suffer from this issue, so
the same considerations as above apply.

The option `DLPNOGrad_Opt=BUFFERED` is not implemented for response
properties.

Below is an example for a simple
DLPNO-MP2 NMR shielding calculation:

```{literalinclude} ../../orca_working_input/dlpno-mp2-nmr-simple.inp
:language: orca
```

A summary of the additional options used for DLPNO-MP2 response
properties is given below:

```orca
%mp2
     PAOOverlapThresh 1e-5   # Threshold for constructing non-redundant PAOs
                             # Default is 1e-8 for energy/gradient calculations!
     TScalePNO_LShift 0.1    # Level shift for PNO constraint equations:
                             # TScalePNO_LShift * TCutPNO
                             # Default is 0 for energy/gradient calculations!
end
```

An example input for a DSD-PBEP86 calculation of the NMR shielding and
dipole polarizability tensors employing DLPNO-MP2 is given below. Note
that the def2-TZVP basis set is not necessarily ideal for either
shielding or polarizability.

```orcainput
! DLPNO-DSD-PBEP86/2013 D3BJ def2-TZVP def2-TZVP/C TightSCF NoFrozenCore
! RIJCOSX def2/J DefGrid3      # Use RIJCOSX with tighter grid settings
! NMR                          # Request NMR shielding
%elprop Polar 1 end            # Request polarizability
%mp2                           # These settings are default for response properties
   Density Relaxed
   PAOOverlapThresh 1e-5
   TScalePNO_LShift 0.1
end
%eprnmr 
  GIAO_2el GIAO_2el_RIJCOSX    # Also use RIJCOSX for GIAO integrals
end                            # (This is the default for !RIJCOSX)
*xyzfile 0 1 geometry.xyz
```

(sec:modelchemistries.mp2.dlpno-numeric)=
## Numerical DLPNO-MP2 derivatives

The various truncations in local correlation methods introduce small
discontinuities in the potential energy surface. For example, a small
displacement may change the sizes of correlation domains, leading to a
slightly larger or smaller error from the domain approximation. The
default DLPNO-MP2 truncation thresholds are conservative enough, so that
these discontinuities should not cause problems in geometry
optimizations using analytic gradients.{cite}`Pinski2019` However, if one
wishes to calculate (semi-)numerical derivatives of the DLPNO-MP2
energy, gradient, or properties using finite differences, large errors
can occur. Therefore, in these cases it is advisable to keep the pair
lists and correlation domains fixed upon displacement. Currently, this
can be achieved using the following procedure: first, the calculation at
the reference geometry is carried out with the additional setting
`StoreDLPNOData=true`:

```orcainput
! DLPNO-MP2 def2-SVP def2-SVP/C VeryTightSCF
%base "calc0"
%mp2
  StoreDLPNOData true
end
*xyzfile 0 1 geom0.xyz
```

This will produce the additional files *calc0.MapDLPNO00.tmp*,
*calc0.MapDLPNOPre0.tmp*, *calc0.IJLIST.0.tmp*, *calc0.IJLISTSCR.0.tmp*,
and *calc0.IJNPNO.0.tmp*, which are needed in the working directory for
the next step together with the localized orbitals in *calc0.loc*. The
calculation at the displaced geometry is then requested as:

```orcainput
! DLPNO-MP2 def2-SVP def2-SVP/C VeryTightSCF
%mp2
  RefBaseName "calc0"
end
*xyzfile 0 1 geom1.xyz
```

The program will use the orbitals from *calc0.loc* as a starting guess
for the localization and map the reference orbitals to the new ones
based on maximal overlap. The lists of correlated and screened out pairs
are read from the files *calc0.IJLIST.0.tmp* and
*calc0.IJLISTSCR.0.tmp*, while the domain information (MO-PAO, MO-Aux,
etc.) is read from *calc0.MapDLPNO00.tmp* and *calc0.MapDLPNOPre0.tmp*.
The number of PNOs for a each pair (stored in *calc0.IJNPNO.0.tmp*) is
also kept consistent with the reference calculation: the ones with the
higest occupation numbers are kept, disregarding $T_\text{CutPNO}$.

This procedure should improve the accuracy and numerical stability for
manually calculated geometric derivatives of various DLPNO-MP2
properties (including those that require analytic first or second
derivatives at the displaced geometries). For semi-numerical Hessian
calculations (`NumFreq`), it is sufficient to add `StoreDLPNOData=true`
as shown below and ORCA will handle the rest. For the sake of numerical
stability, it is also recommended to increase `PAOOverlapThresh` and add
a PNO level shift for the reasons described in
section {ref}`sec:modelchemistries.mp2.dlpnoresp`.

```orca
! DLPNO-MP2 def2-SVP def2-SVP/C VeryTightSCF NumFreq
%mp2
  StoreDLPNOData true
  PAOOverlapThresh 1e-5
  TScalePNO_LShift 0.1
end
# geometry definition
```

Note that in case the orbital localization Hessian is (near-)singular,
the mapping of orbitals from reference to displaced geometries will
likely fail. No solution is presently implemented for this problem.

(sec:modelchemistries.mp2.multilevel)=
## Multi-Level DLPNO-MP2 calculations

With the DLPNO-MP2 method it is possible to treat the interactions among
different fragments of a system with varying accuracy, or exclude some
interactions from the electron correlation treatment entirely. A more
detailed discussion in the DLPNO-CCSD(T) context is given in
section {ref}`sec:modelchemistries.mdci.multilevel` and in ref. {cite}`Sparta2017`.
Here we just present the technical capabilities of the MP2 module and
the required input. Currently, multilayer calculations are only
available for closed-shell DLPNO-MP2. Multilayer gradients and response
properties are also possible. Fragments must be defined -- see
{ref}`sec:essentialelements.fragmentation`.

```orca
! DLPNO-MP2 NoFrozenCore TightPNO
%mp2
  LoosePNOFragInter  {1 *} # * can be used as a wildcard for either or both indices
  NormalPNOFragInter {1 1} {1 2} # multiple fragment pairs can be listed like this
  TightPNOFragInter  {2 3}
  HFFragInter        {3 1} {4 2}
  CustomFragInter
    FragPairs        {4 4} {3 4} # pair definition is required
    HFOnly           false # flag to skip MP2 for these pairs - same as HFFragInter
    FrozenCore       false # flag to skip core correlation - requires !NoFrozenCore
    TCutPNO          1e-8  # custom value for these pairs
    TCutDO           1e-2  # custom value for these pairs
    TCutDOij         1e-5  # custom value for these pairs
    TCutPre          1e-6  # custom value for these pairs
  end
end
# geometry and fragment definition
```

Note that a given pair or fragments can only belong to a single layer
and definitions later in the input overwrite previous ones. This means
that if the above input is used in a 4-fragment calculation, the 1-4
interfragment interactions will be treated with `LoosePNO` thresholds,
the interactions within fragment 1 and with fragment 2 -- with
`NormalPNO` thresholds, 2-3 pairs -- with `TightPNO`, 1-3 and 2-4 pairs
will be left at the HF level, 3-4 and 4-4 pairs will be treated with
$T_\text{CutPNO}=10^{-8}$ and $T_\text{CutDO}=10^{-2}$ (i.e. the
`NormalPNO` defaults), and 2-2 and 3-3 pairs will be left at the global
(`TightPNO`) settings.

[^1]: However, sometimes, and in particular when transition metals and
    core orbitals are involved we have met unpleasantly large errors. So
    -- be careful and double check when using floats!


(sec:modelchemistries.mp2.expcorrelation)=
## Explicitly correlated MP2 calculations

ORCA features an efficient explicit correlation module that is available
for MP2 and coupled-cluster calculations (section
{ref}`sec:modelchemistries.mdci.expcorrelation`). It is
described below in the context of coupled-cluster calculations.


(sec:modelchemistries.mp2.dft)=
## MP2 in "Double-Hybrid" Density Functional Theory
```{index} Double-Hybrid DFT and MP2
```

A slightly more general form is met in the double-hybrid DFT gradient.
The theory is briefly described below.

The energy expression for perturbatively and gradient corrected hybrid
functionals as proposed by Grimme is:

$$\begin{gathered}
E=V_{NN} +\left\langle { \mathrm{\mathbf{Ph} }^{+} } \right\rangle+ \frac{1}{2}\int{\int{ \frac{\rho \left({ \mathrm{\mathbf{r} }_{1} } \right)\rho \left({ \mathrm{\mathbf{r} }_{2} } \right)}{\left|{\mathrm{\mathbf{r} }_{1} -\mathrm{\mathbf{r} }_{2} } 
\right|}d\mathrm{\mathbf{r} }_{1} d\mathrm{\mathbf{r} }_{2} } } -\frac{1}{2}a_{x} 
\sum\limits_{\mu \nu \kappa \tau \sigma } { P_{\mu \kappa }^{\sigma } P_{\nu 
\tau }^{\sigma } \left({ \mu \nu \vert \kappa \tau } \right)} +c_{\text{DF} } E_{\text{XC} } 
\left[{ \rho_{\alpha } ,\rho_{\beta } } \right]+c_{\text{PT} } E_{\text{PT} } \end{gathered}$$

$$\begin{gathered}
E = E_{\text{SCF}} + c_{\text{PT}}E_{\text{PT}}
\end{gathered}$$ (eqn:61)

<!--$$\hspace{-12.75cm}= E_{\text{SC}F} +c_{\text{PT} } E_{\text{PT} } 
$$ (eqn:61)-->

Here $V_{NN}$ is the nuclear repulsion energy and $h_{\mu \nu }$ is a
matrix element of the usual one-electron operator which contains the
kinetic energy and electron-nuclear attraction terms
($\left\langle {\mathrm{\mathbf{ab} }} \right\rangle$ denotes the trace
of the matrix product $\mathrm{\mathbf{ab} })$. As usual, the molecular
spin-orbitals are expanded in atom centered basis functions
($\sigma =\alpha ,\beta )$:

$$\psi_{p}^{\sigma } \left({ \mathrm{\mathbf{r} }} \right)=\sum_\mu{ c_{\mu 
p}^{\sigma } \varphi_{\mu } \left({ \mathrm{\mathbf{r} }} \right)} 
$$ (eqn:62)

with MO coefficients $c_{\mu p}^{\sigma }$. The total density is given
by (real orbitals are assumed throughout):

$$\rho \left({ \mathrm{\mathbf{r} }} \right)=\sum_{i\sigma } { \left|{ \psi 
_{i}^{\sigma } \left({ \mathrm{\mathbf{r} }} \right)} \right|^{2} } 
=\sum_{\mu \nu \sigma } { P_{\mu \nu }^{\sigma } \varphi_{\mu } 
\left({ \mathrm{\mathbf{r} }} \right)\varphi_{\nu } \left({ \mathrm{\mathbf{r} }} 
\right)} =\rho^{\alpha }\left({ \mathrm{\mathbf{r} }} \right)+\rho^{\beta }\left({\mathrm{\mathbf{r} }} \right)$$ (eqn:63)

Where
$\mathrm{\mathbf{P} }=\mathrm{\mathbf{P} }^{\alpha }+\mathrm{\mathbf{P} }^{\beta }$
and $P_{\mu \nu }^{\sigma } 
=\sum_{i_{\sigma } } { c_{\mu i}^{\sigma } c_{\nu i}^{\sigma } }$.

The second term of {eq}`eqn:61` represents the Coulombic self-repulsion. The third
term represents the contribution of the Hartree-Fock exchange with the
two-electron integrals being defined as:

$$\left({ \mu \nu \vert \kappa \tau } \right)=\int{ \int{ \phi_{\mu } \left({\mathrm{\mathbf{r} }_{1} } \right)\phi_{\nu } \left({ \mathrm{\mathbf{r} }_{1} } 
\right)r_{12}^{-1} \phi_{\kappa } \left({ \mathrm{\mathbf{r} }_{2} } \right)\phi 
_{\tau } \left({ \mathrm{\mathbf{r} }_{2} } \right)d\mathrm{\mathbf{r} }_{1} d\mathrm{\mathbf{r} }_{2} } } 
$$ (eqn:64)

The mixing parameter $a_{x}$ controls the fraction of Hartree-Fock
exchange and is of a semi-empirical nature. The exchange correlation
contribution may be written as:

$$E_{\text{XC} } \left[{ \rho_{\alpha } ,\rho_{\beta } } \right] = 
\left({ 1-a_{x} } \right) E_{\text{X} }^{\text{GGA} } \left[{ \rho_{\alpha } ,\rho_{\beta } } \right] 
+ b E_{\text{C} }^{\text{GGA} } \left[{ \rho_{\alpha } ,\rho_{\beta } } \right]$$ (eqn:65)

Here,
$E_{\text{X} }^{\text{GGA} } \left[{ \rho_{\alpha } ,\rho_{\beta } } \right]$
is the exchange part of the XC- functional in question and
$E_{\text{C} }^{\text{GGA} } \left[{ \rho_{\alpha } ,\rho_{\beta } } \right]$
is the correlation part. The parameter $b$ controls the mixing of DFT
correlation into the total energy and the parameter $c_{\text{DF} }$ is
a global scaling factor that allows one to proceed from Hartree-Fock
theory ($a_{\text{X} } =1$, $c_{\text{DF} } =0$, $c_{\text{PT} } =0)$ to
MP2 theory ($a_{\text{X} } =1$, $c_{\text{DF} } =0$,
$c_{\text{PT} } =1$) to pure DFT ($a_{\text{X} } =1$,
$c_{\text{DF} } =0$, $c_{\text{PT} } =1$) to hybrid DFT
($0 < a_{\text{X} } <1$, $c_{\text{DF} } =1$, $c_{\text{PT} } =0)$ and
finally to the general perturbatively corrected methods discussed in
this work ($0<a_{\text{X} } <1$, $c_{\text{DF} } =1$,
$0<c_{\text{PT} } <1$). As discussed in detail by Grimme, the B2- PLYP
functional uses the Lee-Yang-Parr (LYP) functional as correlation part,
the Becke 1988 (B88) functional as GGA exchange part and the optimum
choice of the semi-empirical parameters was determined to be
$a_{\text{X} } =0.53$, $c_{\text{PT} } =0.27$, $c_{\text{DF} } =1$,
$b=1-c_{\text{PT} }$. For convenience, we will suppress the explicit
reference to the parameters $a_{\text{X} }$ and $b$ in the XC part and
rewrite the gradient corrected XC energy as:

$$E_{\text{XC} } \left[{ \rho^{\alpha },\rho^{\beta } } \right]=\int{ f\left({ \rho 
^{\alpha },\rho^{\beta },\gamma^{\alpha \alpha },\gamma^{\beta \beta 
},\gamma^{\alpha \beta } } \right)d\mathrm{\mathbf{r} }}
$$ (eqn:66)

with the gradient invariants
$\gamma^{\sigma{ \sigma }'}=\vec{{\nabla } }\rho^{\sigma }\vec{{\nabla } }
\rho^{{\sigma }'}$. The final term in eq (48) represents the scaled
second order perturbation energy:

$$E^{\text{PT2} }=\frac{1}{2}\sum_{i_{\alpha } <j_{\alpha } } { \left\langle {\mathrm{\mathbf{t} }^{i_{\alpha } j_{\alpha } } { \mathrm{\mathbf{\overline{K} }} }^{i_{\alpha } j_{\alpha } +} } 
\right\rangle} 
+\frac{1}{2}\sum_{i_{\beta } <j_{\beta } } { \left\langle { \mathrm{\mathbf{t} }^{i_{\beta } j_{\beta } } 
\mathrm{\mathbf{\overline{{K} }} }^{i_{\beta } 
j_{\beta } +} } \right\rangle} +\sum_{i_{\alpha } ,j_{\beta } } 
{\left\langle { \mathrm{\mathbf{t} }^{i_{\alpha } j_{\beta } } { \mathrm{\mathbf{\overline{K} }} }^{i_{\alpha } j_{\beta } 
+} } \right\rangle}
$$ (eqn:67)

The PT2 amplitudes have been collected in matrices
$\mathrm{\mathbf{t} }^{i_{\sigma } j_{{\sigma }'} }$ with elements:

$$t_{a_{\sigma } b_{{\sigma }'} }^{i_{\sigma } j_{{\sigma }'} } 
=\bar{{K} }_{a_{\sigma } b_{{\sigma }'} }^{i_{\sigma } j_{{\sigma }'} } 
\left({ \varepsilon_{i}^{\sigma } +\varepsilon_{j}^{{\sigma }'} 
-\varepsilon_{a}^{\sigma } -\varepsilon_{b}^{{\sigma }'} } \right)^{-1}
$$ (eqn:68)

Where the orbitals were assumed to be canonical with orbital energies
$\varepsilon_{p}^{\sigma }$. The exchange operator matrices are
$K_{a_{\sigma } b_{{\sigma }'} }^{i_{\sigma } j_{{\sigma }'} } =\left({ i_{\sigma } 
a_{\sigma } \vert j_{{\sigma }'} b_{{\sigma }'} } \right)$ and the
anti-symmetrized exchange integrals are defined as
$\bar{{K} }_{a_{\sigma } b_{{\sigma }'} }^{i_{\sigma } j_{{\sigma }'} } =\left({ i_{\sigma } a_{\sigma } \vert 
j_{{\sigma }'} b_{{\sigma }'} } \right)-\delta_{\sigma{ \sigma }'} \left({ i_{\sigma } b_{\sigma } \vert _{\sigma } 
a_{\sigma } } \right)$.

The orbitals satisfy the SCF equations with the matrix element of the
SCF operator given by:

$$F_{\mu \nu }^{\sigma } =h_{\mu \nu } +\sum_{\kappa \tau } { P_{\kappa 
\tau } \left({ \mu \nu \vert \kappa \tau } \right)-a_{\text{X} } P_{\kappa \tau 
}^{\sigma } \left({ \mu \kappa \vert \nu \tau } \right)} +c_{\text{DF} } \left({ \mu 
\vert V_{\text{XC} }^{\sigma } \vert \nu } \right)$$ (eqn:69)

The matrix elements of the XC--potential for a gradient corrected
functional are: {cite}`szabo1989modern`

$$\left({ \mu \vert V_{\text{XC} }^{\alpha } \vert \nu } \right)=\int{ \left\{{\frac{\delta f}{\delta \rho_{\alpha } \left({ \mathrm{\mathbf{r} }} 
\right)}\left({ \varphi_{\mu } \varphi_{\nu } } \right)+2\frac{\delta 
f}{\delta \gamma_{\alpha \alpha } }\vec{{\nabla } }\rho_{\alpha } 
\vec{{\nabla } }\left({ \varphi_{\mu } \varphi_{\nu } } 
\right)+\frac{\delta f}{\delta \gamma_{\alpha \beta } }\vec{{\nabla } }\rho 
_{\beta } \vec{{\nabla } }\left({ \varphi_{\mu } \varphi_{\nu } } \right)} 
\right\}d\mathrm{\mathbf{r} }} 
$$ (eqn:70)

The energy in equation {eq}`eqn:61` depends on the MO-coefficients, the PT2-amplitudes
and through $V_{NN}$, $V_{eN}$ (in $h)$ and the basis functions also
explicitly on the molecular geometry. Unfortunately, the energy is only
stationary with respect to the PT2 amplitudes since they can be
considered as having been optimized through the minimization of the
Hylleraas functional:

$$E_{\text{PT2} } =\min_{\mathrm{\mathbf{t}}} \left\{{\frac{1}{2}\sum_{i_{\alpha} <j_{\alpha}} { \left\langle { \mathrm{\mathbf{t} }^{i_{\alpha } j_{\alpha } }
{\mathbf{\overline{{K}}}}^{i_{\alpha } 
j_{\alpha } +} } \right\rangle} +\frac{1}{2}\sum_{i_{\beta } 
<j_{\beta } } { \left\langle {{\mathbf{t} }^{i_{\beta } j_{\beta } } {{\mathbf{\overline{K} }} }^{i_{\beta } 
j_{\beta } +} } \right\rangle} 
+\sum_{i_{\alpha } j_{\beta } } { \left\langle {{\mathbf{t} }^{i_{\alpha } j_{\beta } } 
{\mathbf{\overline{{K} }} }^{i_{\alpha } 
j_{\beta } +} } \right\rangle+\left\langle {{\mathbf{D}'}^{\alpha }{\mathbf{F} }^{\alpha +} } 
\right\rangle+\left\langle {{\mathbf{D}'}^{\beta }{\mathbf{F} }^{\beta +} } \right\rangle} } 
\right\}
$$(eqn;71)

The unrelaxed PT2 difference density is defined as:

$${D}_{ij}^{'\alpha } =-\frac{1}{2}\sum_{k_{\alpha } } { \left\langle { \mathrm{\mathbf{t} }^{i_{\alpha } k_{\alpha } } 
\mathrm{\mathbf{t} }^{k_{\alpha } j_{\alpha } 
} } \right\rangle} -\sum_{k_{\beta } } { \left\langle { \mathrm{\mathbf{t} }^{i_{\alpha } k_{\beta } } 
\mathrm{\mathbf{t} }^{k_{\beta } j_{\alpha } } 
} \right\rangle}
$$ (eqn:72)

$${D}_{ab}^{'\alpha } =\sum_{i_{\alpha } <j_{\alpha } } { \mathrm{\mathbf{t} }^{i_{\alpha } j_{\alpha } } 
\mathrm{\mathbf{t} }^{i_{\alpha } j_{\alpha } 
+} } +\sum_{i_{\beta } j_{\alpha } } { \mathrm{\mathbf{t} }^{i_{\beta } 
j_{\alpha } +} \mathrm{\mathbf{t} }^{i_{\beta } j_{\alpha } } }
$$ (eqn:73)

With analogous expressions for the spin-down unrelaxed difference
densities. Minimization of this functional with respect to the
amplitudes yields the second order perturbation energy. The derivative
of the SCF part of equation {eq}`eqn:61` with respect to a parameter "$x$" is straightforward
and well known. It yields:

$$\begin{array}{l}
 E_{\text{SCF} }^{x} =V_{NN}^{x} +\left\langle { \mathrm{\mathbf{Ph} }^{x} } \right\rangle
+\left\langle { \mathrm{\mathbf{W} }^{SCF}\mathrm{\mathbf{S} }^{\left( x \right)} } 
\right\rangle+\sum_{\mu \nu \kappa \tau } { \Gamma_{\mu \nu \kappa 
\tau } \left({ \mu \nu \vert \kappa \tau } \right)^{\left( x \right)} } \\ 
\hspace{1cm}
+\underbrace{\sum_\sigma}_{\left({ {\sigma }'\ne \sigma } \right)}
{\int{ \left\{{ \frac{\delta f}{\delta \rho_{\sigma } \left({\mathrm{\mathbf{r} }} \right)}\rho_{\sigma }^{\left( x \right)} +2\frac{\delta 
f}{\delta \gamma_{\sigma \sigma } }\vec{{\nabla } }\rho_{\sigma } 
\vec{{\nabla } }\rho_{\sigma }^{\left( x \right)} +\frac{\delta f}{\delta 
\gamma_{\sigma{ \sigma }'} }\vec{{\nabla } }\rho_{{\sigma }'} \vec{{\nabla 
} }\rho_{\sigma }^{\left( x \right)} } \right\}d\mathrm{\mathbf{r} }} } \\ 
 \end{array}
$$ (eqn:74)

Superscript "$x$" refers to the derivative with respect to some
perturbation "$x$" while a superscript in parentheses indicates that
only the derivative of the basis functions with respect to "$x$" is to
be taken. For example:

$$\begin{array}{l}
 \rho_{\sigma }^{\left( x \right)} =\sum_{\mu \nu } P_{\mu \nu 
}^{\sigma } \left\{\frac{\partial \varphi_{\mu } }{\partial x}\varphi 
_{\nu } +\varphi_{\mu } \frac{\partial \varphi_{\nu } }{\partial x} 
\right\}\\ 
 h_{\mu \nu }^{x} =\left( \frac{\partial \varphi_{\mu } }{\partial x}\vert 
\hat{{h} }\vert \varphi_\nu  \right)+\left( \varphi_{\mu } \vert 
\hat{{h} }\vert \frac{\partial \varphi_{\nu } }{\partial x} \right)+\left( 
\varphi_{\mu } \vert \frac{\partial \hat{{h} }}{\partial x}\vert \varphi 
_{\nu }  \right) \\ 
 \end{array}
$$ (eqn:75)

In equation {eq}`eqn:74`, **S** is the overlap matrix and **W**
$^{\text{SCF} }$ the energy weighted density:

$$W_{\mu \nu }^{\text{SCF} } =W_{\mu \nu }^{\alpha ;\text{SCF} } +W_{\mu \nu }^{\beta ;\text{SCF} } 
=-\sum_{i\sigma } { c_{\mu i}^{\sigma } c_{\nu i}^{\sigma } 
\varepsilon_{i}^{\sigma } } 
$$ (eqn:76)

At this point, the effective two-particle density matrix is fully
separable and reads:

$$\Gamma_{\mu \nu \kappa \tau } =\frac{1}{2}P_{\mu \nu } P_{\kappa \tau 
} -\frac{1}{2}a_{x} P_{\mu \kappa }^{\alpha } P_{\nu \tau }^{\alpha } 
-\frac{1}{2}a_{x} P_{\mu \kappa }^{\beta } P_{\nu \tau }^{\beta }
$$ (eqn:77)

The derivative of the PT2 part is considerably more complex, since
$E_{\text{PT2} }$ is not stationary with respect to changes in the
molecular orbitals. This necessitates the solution of the
coupled-perturbed SCF (CP-SCF) equations. We follow the standard
practice and expand the perturbed orbitals in terms of the unperturbed
ones as:

$$\psi_{p}^{\sigma ;x} \left({ \mathrm{\mathbf{r} }} \right)=\sum_q 
{U_{qp}^{\sigma ;x} \psi_{q}^{\sigma } \left({ \mathrm{\mathbf{r} }} \right)} 
$$ (eqn:78)

The occupied-occupied and virtual-virtual blocks of **U** are fixed, as
usual, through the derivative of the orthonormality constraints:

$$U_{ij}^{\sigma ;x} =-\frac{1}{2}S_{ij}^{\sigma \left( x \right)}
$$ (eqn:79)

$$U_{ab}^{\sigma ;x} =-\frac{1}{2}S_{ab}^{\sigma \left( x \right)} 
$$ (eqn:80)

$$U_{ia}^{\sigma ;x} =-S_{ia}^{\sigma \left( x \right)} -U_{ai}^{\sigma ;x} 
$$ (eqn:81)

Where
$S_{pq}^{\sigma \left( x \right)} =\sum\nolimits_{\mu \nu } { c_{\mu p}^{\sigma } c_{\nu q}^{\sigma } S_{\mu 
\nu }^{\left( x \right)} }$. The remaining virtual-occupied block of
**U** $^{x}$ must be determined through the solution of the CP-SCF
equations. However, as shown by Handy and Schaefer, this step is
unnecessary and only a single set of CP-SCF equations (Z-vector
equations) needs to be solved. To this end, one defines the Lagrangian:

$$\begin{array}{l}
 L_{ai}^{\alpha } =R^{\sigma }\left( \mathrm{\mathbf{D}'} \right)_{ai} 
+2\sum_{j_{\alpha } b_{\alpha } c_{\alpha } } { \left({ a_{\alpha } 
c_{\alpha } \vert j_{\alpha } b_{\alpha } } \right)t_{c_{\alpha } b_{\alpha 
} }^{i_{\alpha } j_{\alpha } } } -2\sum_{j_{\alpha } k_{\alpha } 
b_{\alpha } } { \left({ k_{\alpha } i_{\alpha } \vert j_{\alpha } b_{\alpha } 
} \right)t_{a_{\alpha } b_{\alpha } }^{k_{\alpha } j_{\alpha } } } \\ 
\hspace{2.6cm}
+2\sum_{j_{\beta 
} b_{\beta } c_{\alpha } } { \left({ a_{\alpha } c_{\alpha } \vert j_{\beta } 
b_{\beta } } \right)t_{b_{\beta } c_{\alpha } }^{j_{\beta } i_{\alpha } } } 
-2\sum_{j_{\beta } k_{\alpha } b_{\beta } } { \left({ k_{\alpha } 
i_{\alpha } \vert j_{\beta } b_{\beta } } \right)t_{b_{\beta } a_{\alpha } 
}^{j_{\beta } k_{\alpha } } } \\ 
 \end{array}
$$ (eqn:82)

An analogous equation holds for $L_{ai}^{\beta }$. The matrix elements
of the response operator $R^{\alpha }
\left({ \mathrm{\mathbf{D}'} } \right)$ are best evaluated in the AO
basis and then transformed into the MO basis. The AO basis matrix
elements are given by:

$$%\begin{array}{l}
\begin{aligned}
 R^{\alpha }\left({ \mathrm{\mathbf{D}'} } \right)_{\mu \nu } 
=&\sum_{\kappa \tau } { 2{D}'_{\kappa \tau } \left({ \mu \nu \vert 
\kappa \tau } \right)-{D}_{\kappa \tau }^{'\alpha } \left[{ \left({ \mu 
\kappa \vert \nu \tau } \right)+\left({ \nu k\vert \mu \tau } \right)} 
\right]} \\ 
&+\sum_\zeta{ \int{ \left[{\frac{\delta^{2}f}{\delta \rho_{\alpha } \delta \zeta } } \right.\zeta 
\left({ \mathrm{\mathbf{D}'} } \right)\left({ \phi_{\mu } \phi_{\nu } } 
\right)+\left({ 2\frac{\delta^{2}f}{\delta \gamma_{\alpha \alpha } \delta 
\zeta }\vec{{\nabla } }\rho_{\mathrm{\mathbf{P} }}^{\alpha } +\frac{\delta 
^{2}f}{\delta \gamma_{\alpha \beta } \delta \zeta }\vec{{\nabla } }\rho 
_{\mathrm{\mathbf{P} }}^{\beta } } \right)\zeta \left({ \mathrm{\mathbf{D}'} } 
\right)\vec{{\nabla } }\left({ \phi_{\mu } \phi_{\nu } } \right)} } \\ 
&\left.{+\left({ 2\frac{\delta f}{\delta \gamma_{\alpha \alpha } }\vec{{\nabla 
} }\rho_{\mathrm{\mathbf{D}'} }^{\alpha } +\frac{\delta f}{\delta \gamma_{\alpha 
\beta } }\vec{{\nabla } }\rho_{\mathrm{\mathbf{D}'} }^{\beta } } 
\right)\vec{{\nabla } }\left({ \phi_{\mu } \phi_{\nu } } \right)} 
\right]d\mathrm{\mathbf{r} } \\ 
% \end{array}
\end{aligned}$$ (eqn:RD-DHDFT)

where

$$\zeta \left({ \mathrm{\mathbf{D}'} } \right)=\rho_{\mathrm{\mathbf{D}'} }^{\alpha } 
,\rho_{\mathrm{\mathbf{D}'} }^{\beta } ,\gamma_{\alpha \alpha } \left({ \mathrm{\mathbf{D}'} } \right),\gamma_{\beta 
\beta } \left({ \mathrm{\mathbf{D}'} } 
\right),\gamma_{\alpha \beta } \left({ \mathrm{\mathbf{D}'} } \right)$$ (eqn:83)

The $\zeta$-gradient-parameters are evaluated as a mixture of PT2
difference densities and SCF densities. For example:

$$\gamma_{\alpha \alpha } (\mbox{D}')=2\vec{{\nabla } }\rho 
_{\mbox{D}'}^{\alpha } \vec{{\nabla } }\rho_{\mbox{P}'}^{\alpha } 
$$ (eqn:84)

With

$$\rho_{\mathrm{\mathbf{D}'} }^{\alpha } \left({ \mathrm{\mathbf{r} }} 
\right)=\sum_{\mu \nu } { {D}_{\mu \nu }^{'\alpha } \phi_{\mu } 
\left({ \mathrm{\mathbf{r} }} \right)\phi_{\nu } \left({ \mathrm{\mathbf{r} }} \right)}
$$ (eqn:85)

$$\rho_{\mathrm{\mathbf{P} }}^{\alpha } \left({ \mathrm{\mathbf{r} }} 
\right)=\sum_{\mu \nu } { P_{\mu \nu }^{\alpha } \phi_{\mu } \left({\mathrm{\mathbf{r} }} \right)\phi_{\nu } \left({ \mathrm{\mathbf{r} }} \right)} 
$$ (eqn:86)

Having defined the Lagrangian, the following CP-SCF equations need to be
solved for the elements of the "Z- vector":

$$\left({ \varepsilon_{a}^{\sigma } -\varepsilon_{i}^{\sigma } } 
\right)Z_{ai}^{\sigma } +R^{\sigma }\left({ \mathrm{\mathbf{Z} }} \right)_{ai} 
=-L_{ai}^{\sigma } 
$$ (eqn:87)

The solution defines the occupied-virtual block of the relaxed
difference density, which is given by:

$$\mathrm{\mathbf{D} }^{\sigma }=\mathrm{\mathbf{D}'}^{\sigma }+\mathrm{\mathbf{Z} }^{\sigma }
$$ (eqn:88)

For convenience, $\mathrm{\mathbf{D} }^{\sigma }$ is symmetrized since
it will only be contracted with symmetric matrices afterwards. After
having solved the Z-vector equations, all parts of the energy weighted
difference density matrix can be readily calculated:

$$W_{ij}^{\alpha ;\text{PT2} } =-\frac{1}{2}D_{ij}^{\alpha } \left({ \varepsilon 
_{i}^{\alpha } +\varepsilon_{j}^{\alpha } } \right)-\frac{1}{2}R\left({\mathrm{\mathbf{D} }} \right)_{ij} -\sum_{k_{\alpha } a_{\alpha } b_{\alpha 
} } { \left({ i_{\alpha } a_{\alpha } \vert k_{\alpha } b_{\alpha } } 
\right)t_{a_{\alpha } b_{\alpha } }^{j_{\alpha } k_{\alpha } } } 
-\sum_{k_{\beta } a_{\alpha } b_{\beta } } { \left({ i_{\alpha } 
a_{\alpha } \vert k_{\beta } b_{\beta } } \right)t_{b_{\beta } a_{\alpha } 
}^{k_{\beta } j_{\alpha } } } 
$$ (eqn:89)

$$W_{ab}^{\alpha ;\text{PT2} } =-\frac{1}{2}D_{ab}^{\alpha } \left({ \varepsilon 
_{a}^{\alpha } +\varepsilon_{b}^{\alpha } } \right)-\sum_{i_{\alpha 
} j_{\alpha } c_{\alpha } } { \left({ i_{\alpha } a_{\alpha } \vert j_{\alpha 
} c_{\alpha } } \right)t_{b_{\alpha } c_{\alpha } }^{i_{\alpha } j_{\alpha } 
} } -\sum_{i_{\alpha } j_{\beta } c_{\beta } } { \left({ i_{\alpha } 
a_{\alpha } \vert j_{\beta } c_{\beta } } \right)t_{c_{\beta } b_{\alpha } 
}^{j_{\beta } i_{\alpha } } } 
$$ (eqn:90)

$$W_{ai}^{\alpha ;\text{PT2} } =-2\sum_{j_{\alpha } k_{\alpha } b_{\alpha } } 
{\left({ k_{\alpha } i_{\alpha } \vert j_{\alpha } b_{\alpha } } 
\right)t_{a_{\alpha } b_{\alpha } }^{k_{\alpha } j_{\alpha } } } 
-2\sum_{j_{\beta } k_{\alpha } b_{\beta } } { \left({ k_{\alpha } 
i_{\alpha } \vert j_{\beta } b_{\beta } } \right)t_{b_{\beta } a_{\alpha } 
}^{j_{\beta } k_{\alpha } } } 
$$ (eqn:91)

$$W_{ia}^{\alpha ;\text{PT2} } =-\varepsilon_{i}^{\alpha } Z_{ai}^{\alpha } 
$$ (eqn:92)

Once more, analogous equations hold for the spin-down case. With the
relaxed difference density and energy weighted density matrices in hand,
one can finally proceed to evaluate the gradient of the PT2 part as
$(\mathrm{\mathbf{W} }
^{\text{PT2} }=\mathrm{\mathbf{W} }^{\alpha ;\text{PT2} }+\mathrm{\mathbf{W} }^{\beta ;\text{PT2} })$:

$$\begin{array}{l}
E_{\text{PT2} }^{x} =\left\langle { \mathrm{\mathbf{Dh} }^{x} } \right\rangle+\left\langle {\mathrm{\mathbf{W} }^{\text{PT2} } \mathrm{\mathbf{S} }^{\left( x \right)} } \right\rangle
+\sum_{\mu \nu \kappa \tau } { \Gamma_{\mu \nu \kappa \tau }^{\text{PT2} } 
\left({ \mu \nu \vert \kappa \tau } \right)^{(x) }} \\
+ \sum_{\underset{(\sigma \ne{ \sigma }') }{\sigma} }
{\displaystyle\int} \left\{\frac{\delta f}{\delta \rho_\sigma (\mathbf{r}) } \rho_{\sigma }^{(x) } 
+2\frac{\delta f}{\delta \gamma_{\sigma \sigma } }
\overset{r}{\nabla}\rho_{\sigma } \overset{r}{\nabla}\rho^{(x) }_{\sigma } 
+{\frac{\delta f}{\delta \gamma _{\sigma \sigma } }
\overset{r}{\nabla}\rho_{{\sigma }'} \overset{r}{\nabla}\rho_{\sigma }^{(x) }} \right\}\,d\mathbf{r}
\end{array}
$$ (eqn:93)

The final derivative of eq. {eq}`eqn:61` is of course the sum
$E_{SCF}^{x} +c_{PT} E_{\text{PT2} }^{x}$. Both derivatives should be
evaluated simultaneously in the interest of computational efficiency.

Note that the exchange-correlation contributions to the gradient take a
somewhat more involved form than might have been anticipated. In fact,
from looking at the SCF XC-gradient (eq.
{eq}`eqn:74`) it could
have been speculated that the PT2 part of the gradient is of the same
form but with $\rho_{\mathrm{\mathbf{P} }}^{\sigma \left( x \right)}$
being replaced by $\hat{{H} }$, the relaxed PT2 difference density. This
is, however, not the case. The underlying reason for the added
complexity apparent in equation
{eq}`eqn:93` is that
the XC contributions to the PT2 gradient arise from the contraction of
the relaxed PT2 difference density with the derivative of the SCF
operator. Since the SCF operator already contains the first derivative
of the XC potential and the PT2 energy is not stationary with respect to
changes in the SCF density, a response type term arises which requires
the evaluation of the second functional derivative of the XC-functional.
Finally, as is well known from MP2 gradient theory, the effective two-
particle density matrix contains a separable and a non-separable part:

$$\Gamma_{\mu \nu \kappa \tau }^{\text{PT2} } =D_{\mu \nu } P_{\kappa \tau } -D_{\mu 
\kappa }^{\alpha } P_{\nu \tau }^{\alpha } -D_{\mu \kappa }^{\beta } P_{\nu 
\tau }^{\beta } +\Gamma_{\mu \nu \kappa \tau }^{\text{NS} } 
$$ (eqn:94)

$$\Gamma_{\mu \nu \kappa \tau }^{\text{NS} } =\sum_{i_{\alpha } j_{\alpha } 
a_{\alpha } b_{\alpha } } { c_{\mu i}^{\alpha } c_{\nu a}^{\alpha } c_{\kappa 
j}^{\alpha } c_{\tau b}^{\alpha } t_{a_{\alpha } b_{\alpha } }^{i_{\alpha } 
j_{\alpha } } } +\sum_{i_{\beta } j_{\beta } a_{\beta } b_{\beta } } 
{c_{\mu i}^{\beta } c_{\nu a}^{\beta } c_{\kappa j}^{\beta } c_{\tau 
b}^{\beta } t_{a_{\beta } b_{\beta } }^{i_{\beta } j_{\beta } } } 
+2\sum_{i_{\alpha } j_{\beta } a_{\alpha } b_{\beta } } { c_{\mu 
i}^{\alpha } c_{\nu a}^{\alpha } c_{\kappa j}^{\beta } c_{\tau b}^{\beta } 
t_{a_{\alpha } b_{\beta } }^{i_{\alpha } j_{\beta } } } 
$$ (eqn:95)

Thus, the non-separable part is merely the back-transformation of the
amplitudes from the MO to the AO basis. It is, however, important to
symmetrize the two-particle density matrix in order to be able to
exploit the full permutational symmetry of the AO derivative integrals.



(sec:modelchemistries.mp2.optmethod)=
## Orbital Optimized MP2 Methods


### OO-MP2 Theory
```{index} OO-MP2
```

The MP2 energy can be regarded as being stationary with respect to the
MP2 amplitudes, since they can be considered as having been optimized
through the minimization of the Hylleraas functional:

$$E_{\text{MP2} } =\min\limits_{\mathrm{\mathbf{t} }} \left\{{ 2\left\langle { \Psi 
_{1} \vert \hat{{H} }\vert \Psi_{0} } \right\rangle+\left\langle {\Psi_{1} \vert \hat{{H} }_{0} -E_{0} \vert \Psi_{1} } 
\right\rangle} \right\}$$ (eqn:96)

$\hat{{H} }$ is the 0$^{th}$ order Hamiltonian as proposed by Møller and
Plesset, $\Psi_{0}$ is the reference determinant, $\Psi_{1}$ is the
first-order wave function and
$E_{0} =E_{\text{HF} } =\left\langle\Psi_{\text{HF} }
\right|\hat{{H} }\left| \Psi_{\text{HF} }\right\rangle$ is the reference
energy. The quantities $\mathbf{t}$ collectively denote the MP2
amplitudes.

The fundamental idea of the OO-MP2 method is to not only minimize the
MP2 energy with respect to the MP2 amplitudes, but to minimize the total
energy additionally with respect to changes in the orbitals. Since the
MP2 energy is not variational with respect to the MO coefficients, no
orbital relaxation due to the correlation field is taken into account.
If the reference determinant is poor, the low-order perturbative
correction then becomes unreliable. This may be alleviated to a large
extent by choosing better orbitals in the reference determinant.
Numerical evidence for the correctness of this assumption will be
presented below.

In order to allow for orbital relaxation, the Hylleraas functional can
be regarded as a functional of the wavefunction amplitudes $\mathbf{t}$
and the orbital rotation parameters $\mathbf{R}$ that will be defined
below. Through a suitable parameterization it becomes unnecessary to
ensure orbital orthonormality through Lagrange multipliers. The
functional that we minimize reads:

$$L\left\{\mathbf{t,\, R}\right\}= E_{0} \left[{ \mathbf{R} } 
\right]+2\left\langle\Psi_{1} \right|\hat{{H} }\left| \Psi_{0} \right\rangle
+\left\langle\Psi_{1} \right|\hat{H}_0 - E_0 \left| \Psi_{1} \right\rangle
$$ (eqn:97)

$\Psi_{0}$ is the reference determinant. However, it does no longer
correspond to the Hartree-Fock (HF) determinant. Hence, the reference
energy
$E_{0} \left[{ \mathbf{R} } \right]=\left\langle { \Psi_{0} \left[{ \mathbf{R} } 
\right]} \right|\hat{{H} }\left|\Psi_{0} \left[{ \mathbf{R} } 
\right] \right\rangle$ also changes during the variational process and
is no longer stationary with respect to the HF MO coefficients.
Obviously, $E_{0} \left[{ \mathbf{R} } \right]\geqslant E_{\text{HF} }$
since the HF determinant is, by construction, the single determinant
with the lowest expectation value of the full Hamiltonian.

The reference energy is given as:

$$E_{0} \left[{ \mathbf{R} } \right]=\sum_i { \left\langle i \right|h\left|i
\right\rangle+\frac{1}{2}\sum_{ij} { \left\langle { ij} || ij
\right\rangle} } 
$$ (eqn:98)

The first-order wave function excluding single excitations is:

$$\left| \Psi_1 \right\rangle= \frac{1}{4} \sum_{ijab} t_{ab}^{ij} | \left. \Psi_{ij}^{ab} \right\rangle
$$ (eqn:99)

A conceptually important point is that Brillouin's theorem
{cite}`jensen1999intro` is no longer obeyed since the Fock matrix will
contain off-diagonal blocks. Under these circumstances the first-order
wavefunction would contain contributions from single excitations. Since
the orbital optimization brings in all important effects of the singles
we prefer to leave them out of the treatment. Any attempt to the
contrary will destroy the convergence properties. We have nevertheless
contemplated to include the single excitations perturbatively:

$$E_{\text{Singles} }^{(2) } =-\sum_{ia} { \frac{\left|{ F_{ia} } 
\right|^{2} }{\varepsilon_{a} -\varepsilon_{i} } } 
$$ (eqn:100)

The perturbative nature of this correction would destroy the stationary
nature of the total energy and is hence not desirable. Furthermore,
results with inclusion of single excitation contributions represent no
improvement to the results reported below. They will therefore not be
documented below and henceforth be omitted from the OO-MP2 method by
default.

The explicit form of the orbital-optimized MP2 Hylleraas functional
employing the RI approximation (OO-RI-MP2) becomes:

$$L_{\infty} \left[{ \mathbf{t,\, R} } \right]=\sum_i { \left\langle i \right|} 
\hat{{h} }\left|i \right\rangle+\frac{1}{2}\sum_{ij} { \left\langle {ij} || ij \right\rangle+\sum_{iaP} { (ia\vert P)\Gamma 
_{ia}^{'P} } } +\sum_{ij} { D_{ij} F_{ij} } +\sum_{ab} { D_{ab} 
F_{ab} } 
$$ (eqn:101)

with:

$$\Gamma_{ia}^{'P} =\sum_Q { V_{PQ}^{-1} \sum_{jb} { (Q\vert 
jb)t_{ab}^{ij} } } 
$$ (eqn:102)

$$(ia\vert P)=\int{ \int{ \psi_{i} (\mathbf{r}_{1} ) } } \psi_{a} (\mathbf{r}_{1} 
)\frac{1}{\left|{ \mathbf{r}_{1} \mathbf{\, }-\mathbf{\, r}_{2} } \right|}\eta 
_{P} (\mathbf{r}_{2} )d\mathbf{r}_{1} d\mathbf{r}_{2} 
$$ (eqn:103)

$$(P\vert Q)=\int{ \int{ \eta_{p} } } (\mathbf{r}_{1} )\frac{1}{\left|{\mathbf{r}_{1} \mathbf{\, }-\mathbf{\, r}_{2} } \right|}\eta_{Q} (\mathbf{r}_{2} 
)d\mathbf{r}_{1} d\mathbf{r}_{2} 
$$ (eqn:104)

Here, $\left\{\psi \right\}$ is the set of orthonormal molecular
orbitals and $\left\{\eta \right\}$ denotes the auxiliary basis set.
$F_{pq}$ denotes a Fock matrix element:

$$F_{pq} =\left\langle p \right|\hat{{h} }\left| q \right\rangle+\sum_k 
{\left\langle { pk} || qk \right\rangle} 
$$ (eqn:105)

and it is insisted that the orbitals diagonalize the occupied and
virtual subspaces, respectively:

$$\begin{array}{l}
 F_{ij} =\delta_{ij} F_{ii} =\delta_{ij} \varepsilon_{i} \\ 
 F_{ab} =\delta_{ab} F_{aa} =\delta_{ab} \varepsilon_{a} \\ 
 \end{array}
$$ (eqn:106)

The MP2 like density blocks are,

$$\begin{array}{l}
 D_{ij} =-\frac{1}{2}\sum_{kab} { t_{ab}^{ik} t_{ab}^{jk} } \\ 
 D_{ab} =\frac{1}{2}\sum_{ijc} { t_{ac}^{ij} t_{bc}^{ij} } \\ 
 \end{array}
$$ (eqn:107)

where the MP2 amplitudes in the case of a block diagonal Fock matrix are
obtained through the
condition$\frac{\partial L_{\infty} }{\partial t_{ab}^{ij} 
}=0$:

$$t_{ab}^{ij} =-\frac{\left\langle { ij} || ab \right\rangle
}{\varepsilon_{a} +\varepsilon_{b} -\varepsilon_{i} -\varepsilon_{j} }
$$ (eqn:108)

The orbital changes are parameterized by an anti-Hermitian matrix
$\mathbf{R}$ and an exponential Ansatz,

$$\begin{array}{c}
 \mathbf{c}^{\text{new} }=\mathbf{c}^{\text{old} }\exp (\mathbf{R}) \\ 
 \mathbf{R}=\left({ {\begin{array}{*{20}c}
 0 \hfill & { \mathbf{R}_{ia} } \hfill \\
 { -\mathbf{R}_{ia} } \hfill & 0 \hfill \\
\end{array} } } \right) \\ 
 \end{array}
$$ (eqn:109)

The orbitals changes to second order are,

$$\begin{array}{l}
 \exp (\mathbf{R})\left|i \right\rangle=\left|i \right\rangle+\sum_a 
{\mathbf{R}_{ai} \left| a \right\rangle} -\frac{1}{2}\sum_{jb} { \mathbf{R}_{bi} \mathbf{R}_{bj} 
\left| j \right\rangle+ \dots} \\ 
 \exp (\mathbf{R})\left| a \right\rangle=\left| a \right\rangle-\sum_i 
{\mathbf{R}_{ai} \left| i \right\rangle} -\frac{1}{2}\sum_{jb} { \mathbf{R}_{aj} \mathbf{R}_{bj} 
\left| b \right\rangle+ \dots} \\ 
 \end{array}
$$ (eqn:110)

Through this Ansatz it is ensured that the orbitals remain orthonormal
and no Lagrangian multipliers need to be introduced. The first-order
expansion of the Fock operator due to the orbital rotations are:

$$F_{pq} \left[ R \right]=F_{pq} \left[ 0 \right]+R_{pq}^{(1) } +\sum_r 
{R_{rp} F_{rq} \left[ 0 \right]+R_{rq} F_{pr} \left[ 0 \right]} 
$$ (eqn:111)

$$R_{pq}^{(1) } =\sum_{kc} { R_{ck} \left\{{ \left\langle { pc}|| qk \right\rangle+ \left\langle { pk} || qc 
\right\rangle} \right\}}
$$ (eqn:112)

The first-order energy change becomes
$\left({ h_{pq} \equiv \left\langle p 
\right|\hat{{h} }\left| q \right\rangle,g_{pqrs} \equiv \left\langle { pq} 
|| rs \right\rangle} \right)$:

$$\begin{array}{c}
 L_{\infty} \left[{ \mathbf{t,R} } \right]=\sum_{ic} { R_{ci} \left({ h_{ci} 
+h_{ic} } \right)+\frac{1}{2}\sum_{ijc} { R_{ci} \left({ g_{cjij} 
+g_{ijcj} } \right)} } +R_{cj} \left({ g_{icij} +g_{ijic} } \right) \\ 
 +2\sum_{iacP} { R_{ci} (ac\vert P)\Gamma_{ia}^{'P} } 
-2\sum_{ikaP} { R_{ak} (ik\vert P) } \Gamma_{ia}^{'P} \\ 
 -\sum_{ij} { D_{ij} \left({ R_{ij}^{(1) } +\sum_c { \left({R_{ci} F_{cj} +R_{cj} F_{ic} } \right)} } \right)} \\ 
 +\sum_{ab} { D_{ab} \left({ R_{ab}^{(1) } -\sum_k { \left({R_{ak} F_{kb} +R_{bk} F_{ak} } \right)} } \right)} \\ 
 \end{array}
$$ (eqn:113)

The condition for the energy functional to be stationary with respect to
the orbital rotations
$\left({ \frac{\partial L_{\infty} \left[{ \mathbf{t,R} } 
\right]}{\partial R_{ai} }=0} \right)$, yields the expression for the
orbital gradient and hence the expression for the OO-RI-MP2 Lagrangian.

$$\frac{\partial L_{\infty} [ \mathbf{t},\mathbf{ R}]}{\partial R_{ai} }\equiv 
g_{ai} = 2F_{ai} +2\sum_j { D_{ij} F_{aj} -2\sum_b { D_{ab} 
F_{ib} +R^{(1) }(\mathrm{\mathbf{D} })_{ai} } } 
$$ (eqn:114)

$$+2\sum_{cP} { (ac\vert P)\Gamma_{ia}^{\prime P} -2\sum_{kP} 
{(ik\vert P)\Gamma_{ia}^{\prime P} } }$$

The goal of the orbital optimization process is to bring this gradient
to zero. There are obviously many ways to achieve this. In our
experience, the following simple procedure is essentially satisfactory.
We first build a matrix $\mathbf{B}$ in the current MO basis with the
following structure:

$$\begin{array}{c}
 \mathbf{B}_{ij} =\delta_{ij} \mathbf{F}_{ii} \\ 
 \mathbf{B}_{ab} =\delta_{ab} (\mathbf{F}_{aa} + \boldsymbol{\Delta} ) \\ 
 \mathbf{B}_{ai} =\mathbf{B}_{ia} = \mathbf{g}_{ai} \\ 
 \end{array}
$$ (eqn:115)

where $\Delta$ is a level shift parameter. The occupied/occupied and
virtual/virtual blocks of this matrix are arbitrary but their definition
has a bearing on the convergence properties of the method. The orbital
energies of the block diagonalized Fock matrix appear to be a logical
choice. If the gradient is zero, the **B**-matrix is diagonal. Hence one
obtains an improved set of orbitals by diagonalizing **B**.

In order to accelerate convergence a standard DIIS scheme is used.
{cite}`koch2000achemist,mcweeny1992methods` However, in order to carry out
the DIIS extrapolation of the **B**-matrix it is essential that a common
basis is used that does not change from iteration to iteration. Since
the **B**-matrix itself is defined in the molecular orbitals of the
current iteration we choose as a common set of orthonormal orbitals the
MOs of the HF calculation. The extrapolation is carried out in this
basis and the extrapolated **B**-matrix is transformed back to the
current set of MOs prior to diagonalization. Obviously, the same
strategy can be used for orbital optimization in any method for which an
orbital gradient is available.

For well behaved cases this simple scheme converges in 5-10 iterations.
Transition metals and more complicated molecules may require up to 20
iterations and level shifting in order to achieve convergence.

Upon convergence the sum of the matrix $\mathbf{D}$ and the density of
the reference determinant $P_{\mu \nu } =\sum_i { c_{\mu i} c_{\nu i} }$
form the true one-particle density matrix of the OO-MP2 approach that
can be used for property or gradient calculations.

(sec:modelchemistries.mp2.optmethod.usage)=
### OO-MP2 - Tips, Usage and Examples

By making the Hylleraas functional stationary with respect to the
orbital rotations one obtains the orbital-optimized MP2 method that is
implemented in ORCA in combination with the RI approximation
(OO-RI-MP2). One obtains from these calculations orbitals that are
adjusted to the dynamic correlation field at the level of second order
many-body perturbation theory. Also, the total energy of the OO-RI-MP2
method is lower than that of the RI-MP2 method itself. One might think
of this method as a special form of multiconfigurational SCF theory
except for the fact that the Hamiltonian is divided into a
0$^{\text{th} }$ order term and a perturbation.

The main benefit of the OO-RI-MP2 method is that it "repairs" the poor
Hartree--Fock orbitals to some extent which should be particularly
beneficial for systems which suffer from the imbalance in the
Hartree-Fock treatment of the Coulomb and the Exchange hole. Based on
the experience gained so far, the OO-RI-MP2 method is no better than
RI-MP2 itself for the thermochemistry of organic molecules. However, for
reactions barriers and radicals the benefits of OO-MP2 over MP2 are
substantial. This is particularly true with respect to the
spin-component scaled variant of OO-RI-MP2 that is OO-RI-SCS-MP2.
Furthermore, the OO-RI-MP2 method substantially reduces the spin
contamination in UHF calculations on radicals.

Since every iteration of the OO-MP2 method is as expensive as a RI-MP2
relaxed density calculation, the computational cost is much higher than
for RI-MP2 itself. One should estimate about a factor of 10 increase in
computational time with respect to the RI-MP2 time of a normal
calculation. This may still be feasible for calculations in the range of
1000--2000 basis functions (the upper limit, however, implies very
significant computational costs). A full assessment of the orbital
optimized MP2 method has been published.{cite}`Neese2009ooscsmp2`

OO-RI-MP2 is triggered either with `! OO-RI-MP2` or `! OO-RI-SCS-MP2 `
(with spin component scaling) in the simple input line or by
`OrbOpt true` in the `%mp2` block. The method comes with the following
new variables:

```orca
%mp2 OrbOpt  true   # turns on the orbital optimization
     CalcS2  false  # calculate the S**2 expectation value
                    # in spin-unrestricted calculations
     MaxOrbIter 64  # Max. number of iterations
     MP2Shift  0.1  # Level shift for the procedure
     end
```

The solver is a simple DIIS type scheme with additional level shifting.
We have found that it is not really beneficial to first converge the
Hartree-Fock equations. Thus it is sensible to additionally use the
keyword `! noiter` in order to turn off the standard Hartree-Fock SCF
process before entering the orbital optimizations.

The OO-RI-MP2 method is implemented for RHF and UHF reference
wavefunctions. Analytic gradients are available.

The density does not need to be requested separately in OO-RI-MP2
calculations because it is automatically calculated. Also, there is no
distinction between relaxed and unrelaxed densities because the
OO-RI-MP2 energy is fully stationary with respect to all wavefunction
parameters and hence the unrelaxed and relaxed densities coincide.

(sec:modelchemistries.mp2.regularized)=
## Regularized MP2 and RI-MP2

Regularized MP2 is a variant of second-order Moller-Plesset theory (MP2) introduced
by J. Shee, M. Loipersberger, A. Rettig, J. Lee, and M. Head-Gordon {cite}`Shee2021`
that aims to improve its accuracy for systems with $\pi$-driven dispersion
interactions and dative bonds in transition metal complexes. The approach 
achieves this by introducing a single-parameter, energy-gap dependent
regularization that dampens overestimated pairwise additive contributions,
thus renormalizing first-order amplitudes to empirically mimic higher-order correlations.

For this, the standard MP2 energy and thus the standard algorithms are modified. For the $\sigma$ $\text{(}p=1\text{)}$ and  $\sigma^2$ $\text{(}p=2\text{)}$ regularization, the energy is modified according to

$$
E_{\sigma^p\text{-MP2}} = -\dfrac{1}{4} \sum_{ijab} \dfrac{|\left\langle ij||ab \right\rangle |^2}{\Delta_{ij}^{ab}} (1-e^{-\sigma(\Delta_{ij}^{ab})^p})
$$

which corresponds to regularizing the first-order amplitudes.
For the $\kappa$ regularization, the MP2 energy is modified according to

$$
E_{\kappa\text{-MP2}} = -\dfrac{1}{4} \sum_{ijab} \dfrac{|\left\langle ij||ab \right\rangle |^2}{\Delta_{ij}^{ab}} \left(1-e^{-\kappa(\Delta_{ij}^{ab})}\right)^2
$$

which corresponds to regularizing the first-order amplitudes and the exchange integrals.

Regularized MP2 is available for standard MP2 in "memory mode" (Q1Opt$>$0) and RI-MP2 (RIJDX, RIJCOSX, RIJK).

The usage of regularized MP2 is controlled by the `DoRegMP2` keyword, the type of regularization can be specified by setting the `RegMP2Type` parameter to 0 for $\kappa$, 1 for $\sigma$, or 2 for $\sigma^2$. The value of the regularizers can be specified by `RegMP2Kappa` and `RegMP2Sigma` respectively.

```orca
%mp2
    DoRegMP2     true   # required
    RegMP2Type   0      # kappa regularizer
                 1      # sigma regularizer
                 2      # sigma-squared regularizer
    RegMP2Kappa  1.1    # kappa value
    RegMP2Sigma  0.5    # sigma value
end
```

It is important to note that only single point energies are available and tested for regularized MP2. Density, Gradient, and Hessian calculations are not yet supported.

(sec:modelchemistries.mp2.keywords)=
## Keywords

:::{raw} latex
\begingroup
\footnotesize
:::
(tab:modelchemistries.mp2.keywords.simple)=
:::{flat-table} Simple input keywords selecting MP2 variants.
:header-rows: 1
:class: footnotesize
* - Keyword
  - Description
* - `MP2`
  - Canonical MP2
* - `RI-MP2`
  - RI-MP2 (Aliases: `RIMP2`, `MP2RI`)
* - `DLPNO-MP2`
  - DLPNO-MP2
* - `SCS-MP2`
  - Spin-component-scaled canonical MP2
* - `SCS-MP2`
  - Spin-opposite-scaled canonical MP2
* - `RI-SCS-MP2`
  - Spin-component-scaled RI-MP2 (Aliases: `SCS-RI-MP2`, `SCS-RIMP2`)
* - `RI-SOS-MP2`
  - Spin-opposite-scaled RI-MP2 (Aliases: `SOS-RI-MP2`, `SOS-RIMP2`)
* - `DLPNO-SCS-MP2`
  - Spin-component-scaled DLPNO-MP2 (Alias: `SCS-DLPNO-MP2`)
* - `DLPNO-SOS-MP2`
  - Spin-opposite-scaled DLPNO-MP2 (Alias: `SOS-DLPNO-MP2`)
* - `RI-SCS-MP2`
  - Spin-opposite-scaled RI-MP2 (Aliases: `SOS-RI-MP2`, `SOS-RIMP2`)
* - `OO-RI-MP2`
  - Orbital-optimized RI-MP2 (Aliases: `OO-RIMP2`, `OO-MP2RI`)
* - `OO-RI-SCS-MP2`
  - Orbital-optimized spin-component-scaled RI-MP2 (Aliases: `OO-SCS-RI-MP2`, `OO-SCS-RIMP2`)
* - `OO-RI-SOS-MP2`
  - Orbital-optimized spin-opposite-scaled RI-MP2 (Aliases: `OO-SOS-RI-MP2`, `OO-SOS-RIMP2`)
* - `F12-MP2`
  - MP2 with F12 correction (Alias: `MP2-F12`)
* - `F12-RI-MP2`
  - RI-MP2 with F12 correction (Aliases: `MP2-F12-RI`, `RI-MP2-F12`)
* - `F12/D-RI-MP2`
  - RI-MP2 with F12 correction employing the lower-cost D approximation 
    (Aliases: `MP2-F12/D-RI`, `RI-MP2-F12/D`, `F12D-RI-MP2`, `MP2-F12D-RI`, `RI-MP2-F12D` )
* - `F12-DLPNO-MP2`
  - DLPNO-MP2 with F12 correction (Alias: `DLPNO-MP2-F12`)
* - `F12/D-DLPNO-MP2`
  - DLPNO-MP2 with F12 correction employing the lower-cost D approximation 
    (Aliases: `DLPNO-MP2-F12/D`, `F12D-DLPNO-MP2`, `DLPNO-MP2-F12D` )
* - `LoosePNO`
  - Selects loose thresholds for DLPNO-MP2
* - `NormalPNO`
  - (Default) Selects default thresholds for DLPNO-MP2
* - `TightPNO`
  - Selects tight thresholds for DLPNO-MP2
:::
:::{raw} latex
\endgroup
:::
