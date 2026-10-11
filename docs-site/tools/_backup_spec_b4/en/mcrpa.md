

<a id="sec:spectroscopyproperties.mcrpa"></a>
# Excited States via MCRPA

The MCRPA method is a synonym for [CASSCF](sec:modelchemistries.casscf) linear response theory.
Having converged [CASSCF](sec:modelchemistries.casscf) calculations for the electronic ground state,
you can employ ORCA's MCRPA implementation to compute
- excitation energies
- oscillator strengths (intensities of the UV/Vis spectrum)
- rotatory strengths (intensities of the ECD spectrum)
- core excitation energies to simulate XAS spectra
primarily for open-shell and strongly correlated systems.

Before running these calculations make sure you are familiar with
[CASSCF](sec:modelchemistries.casscf) calculations in general.

## General Description

MCRPA excitation energies and transition moments are computed from the
poles and residues of the linear response function of CASSCF a wave
function.[Yeager1979,Joergensen1988,Helmich-Paris2019a](../../bibliography.md)
Those are determined from the generalized eigenvalue equations

$$

\begin{aligned}
\mathbf{E}^{(2) } \, \boldsymbol{\lambda} =   \mathbf{S}^{(2) } \, \boldsymbol{\lambda}\, \omega \text{,}\end{aligned}

$$

that involve the second-derivative matrices $\mathbf{E}^{(2) }$ and $\mathbf{S}^{(2) }$. 
The eigenvalues $\omega$ correspond to the
electronic excitation energies. The second-derivative matrices
$\mathbf{E}^{(2) }$ and $\mathbf{S}^{(2) }$ have a paired structure as
both kind of operators that express electronic excitation and de-excitations are involved:

$$

\left[ \left( \begin{array}{cc}
          \mathbf{A}   & \mathbf{B} \\
          \mathbf{B}^* & {\mathbf{A}}^*
        \end{array} \right)
        - \omega
        \left(
        \begin{array}{cc}
          \boldsymbol{\Sigma}   &  \boldsymbol{\Delta}  \\
          -\boldsymbol{\Delta}^* & -\boldsymbol{\Sigma}^*
        \end{array}
        \right)\right]
    \left(
    \begin{array}{c}
      \mathbf{X} \\
      \mathbf{Y}^*
    \end{array} \right)
= \left(
    \begin{array}{c}
      \mathbf{0} \\
      \mathbf{0}
    \end{array}
    \right)

$$

The eigenvalue equations above are valid for all variational wave
functions methods, e.g. [DFT](sec:modelchemistries.dft), [HF](sec:essentialelements.hartreefock), [CASSCF](sec:modelchemistries.casscf) etc. The only difference is the

operator manifold and the time-independent Hamiltonian $\hat{H}$ that is
used. For the CASSCF linear response and eigen value equations, the
super matrices $\mathbf{A}$, $\mathbf{B}$, $\boldsymbol{\Sigma}$, and
$\boldsymbol{\Delta}$ have the following structure:

$$

\begin{aligned}
&
\begin{array}{cc}
\mathbf{A} = \left(\begin{array}{cc}
\bra{0} [ q_i, [\hat{H}, q_j^{\dagger} ] ]    \ket{0} & \bra{0} [ [ q_i, \hat{H} ], R_j^{\dagger} ]  \ket{0} \\
\bra{0} [  R_i , [ \hat{H}, q_j^{\dagger} ] ] \ket{0} & \bra{0} [ R_i, [ \hat{H}, R_j^{\dagger} ] ]  \ket{0}
\end{array}
\right)%
&
\boldsymbol\Sigma = \left(\begin{array}{cc}
\bra{0} [ q_i, q_j^{\dagger} ] \ket{0} & \bra{0} [ q_i, R_j^{\dagger} ] \ket{0} \\
\bra{0} [ R_i, q_j^{\dagger} ] \ket{0} & \bra{0} [ R_i, R_j^{\dagger} ] \ket{0}
\end{array}
\right) \\[2.0em]
\mathbf{B} = \left(\begin{array}{cc}
\bra{0} [ q_i, [\hat{H}, q_j ] ]    \ket{0} & \bra{0} [ [ q_i, \hat{H} ], R_j ] \ket{0} \\
\bra{0} [  R_i , [ \hat{H}, q_j ] ] \ket{0} & \bra{0} [ R_i, [ \hat{H}, R_j ] ] \ket{0}
\end{array}
\right)%
&
\boldsymbol\Delta = \left(\begin{array}{cc}
\bra{0}  [ q_i, q_j ] \ket{0}  & \bra{0} [ q_i, R_j ] \ket{0} \\
\bra{0}  [ R_i, q_j ] \ket{0}  & \bra{0} [ R_i, R_j ] \ket{0}
\end{array}
\right)
\end{array}
\end{aligned}

$$

There are two types of operators for describing electronic excitations,
i.e. orbital excitation $q_i^{\dagger}$ and de-excitation operators $q_i$,

$$

\begin{aligned}
 &
 \begin{array}{lcr}
 q_i^{\dagger} = E_{pq} = a^{\dagger}_{p\alpha} a_{q\alpha} + a^{\dagger}_{p\beta} a_{q\beta} \text{,}
&
 q_i        = E_{qp}  \text{,}
&
\text{ with }  \quad p > q
 \end{array}\end{aligned}

$$

as well as so called state-transfer operators

$$

\begin{aligned}
&
\begin{array}{lcr}
 R_i^{\dagger} = \ket{i}\bra{0} \text{,}
&
 R_i        = \ket{0}\bra{i} \text{,}
&
 \text{ with }  i \ne 0
\end{array}\end{aligned}

$$

Intensities of the (UV/Vis) absorption and electronic circular
 dichroism (ECD) spectra are obtained from the transition moments.
Transition moments are easily computed as dot product

$$

\begin{aligned}
\bra{0} \hat{V} \ket{f} = 
\left(\begin{array}{c}
\mathbf{X}^f \\
(\mathbf{Y}^f)^*
\end{array}\right)^{\dagger}
\left(\begin{array}{c}
\mathbf{C} \\
\mathbf{D}^*
\end{array}\right)
\end{aligned}

$$

from the eigenvectors $\mathbf{X}$ and $\mathbf{Y}$ of root $f$
and the electronic gradients $\mathbf{C}$ and $\mathbf{D}$ of the dipole operators $\hat{V}$.

$$

\begin{aligned}
\begin{array}{lr}
\mathbf{C} = \left(\begin{array}{c}
\bra{0} [ q_i, \hat{V} ] \ket{0} \\
\bra{0} [ R_i, \hat{V} ] \ket{0}
\end{array}\right)
&
\mathbf{D} = \left(\begin{array}{c}
\bra{0} [ q^{\dagger}_i, \hat{V} ] \ket{0} \\
\bra{0} [ R^{\dagger}_i, \hat{V} ] \ket{0}
\end{array}\right)
\end{array}
\end{aligned}

$$

The eigenvalue equations are solved iteratively by a
customized version of the Davidson algorithm that simultaneously
determines the N lowest lying roots. 
The most time of the calculation is spent on the
transformation of trial vectors that contain an orbital and CI
coefficient part with the electronic Hessian matrix $\mathbf{E}^{(2) }$.
The working equations are very similar to those of the CASSCF electronic
gradient that is computed when minimizing the CASSCF ground state
energy. Further technical aspects are described in
subsection [sec:spectroscopyproperties.mcrpa.computational](#sec:spectroscopyproperties.mcrpa.computational).

<a id="fig:MCRPA-ni-II-h2o-6"></a>
*Structure and frontier orbitals of Ni(II) hexaquo complex.*
As a show case example, the lowest valence excitation energies
of the octahedrally coordinated Ni(II) hexaquo complex are computed with MCRPA
(for structure and frontier orbitals see Fig. [fig:MCRPA-ni-II-h2o-6](#fig:MCRPA-ni-II-h2o-6)).
We include the 3d and 4d Ni orbitals in the active space and converge the
CASSCF triplet ground state, first. Then, the MCRPA calculation is launched.
It is only necessary to specify the number of desired roots `NRoots`.
```orca
%casscf
 nel    10  # number of active electrons
 norb   10  # number of active orbitals
 nroots  1  # only the ground state
 mult    3  # triplet multiplicity
end

%mcrpa
 NRoots 15  # number of roots / excited states
end
```
Note that in contrast to state-averaged CASSCF, the MCRPA excitation energies
do not dependent on `NRoots` as for [TDDFT](sec:spectroscopyproperties.tddft) or [EOM-CC](sec:spectroscopyproperties.eom) calculations.

It is also possible to omit the orbital part of MCTDA or MCRPA calculations
by toggling the `DoOrbResp false` flag. For such calculation, the [CASCI](sec:modelchemistries.casscf.excitedstates)
excitation energies are obtained. Note that for such MCRPA calculations the orbitals were optimized
for the CASSCF ground state.

<a id="sec:spectroscopyproperties.mcrpa.results"></a>
## Analyzing Transitions

After convergence, the most significant contributions of the excitation / eigen vector
is given for each state. 
When comparing with the ground state CI coefficients
```orca
---------------------------------------------
CAS-SCF STATES FOR BLOCK  0 MULT= 3 NROOTS= 1
---------------------------------------------

ROOT   0:  E=   -1962.8698444660 Eh
      0.98088 [     0]: 2221100000
```
we see that the lowest excited state is dominated by a transition from
active orbital 3 (d<sub>yz</sub>) to active orbitals 4 and 5 (mixture of d<sub>z<sup>2</sup></sub> and d<sub>x<sup>2</sup>-y<sup>2</sup></sub>).

```orca
STATE    1 3A  :  E=   0.033027 au      0.899 eV     7248.5 cm**-1

   (+) CI                                  0.72808 [    21]: 2212100000
   (+) CI                                  0.25245 [    27]: 2211200000
```
The `(+)` denotes the upper component of the eigenvectors.

By default the largest elements of the CI eigenvector are printed 
in the configuration basis. By changing `PrintWF` to `DET` or `CSF`
you can also print that in the determinant or configuration state function (CSF) basis,
respectively.

Note that the analysis of CI coefficient depends also on the choice
of active orbitals which are chosen to be natural orbitals (default option).

There are also transitions dominated by single-electron excitations represented by
the orbital part of the eigenvector. In case of the Ni(II) hexaquo complex
those are primarily Rydberg states.
Below find the most significant orbital pairs (upper `(+)` and lower `(-)` component)
for the 24th excited state.
```orca
STATE   24 3A  :  E=   0.469596 au     12.778 eV   103064.3 cm**-1

   (+) I  24 (  35) -> V   0 (  49) :      0.01744 (c=  0.13206324)
   (+) I  26 (  37) -> V   2 (  51) :      0.02398 (c= -0.15485895)
   (+) I  24 (  35) -> V   4 (  53) :      0.02513 (c=  0.15853501)
   (+) A   0 (  39) -> V   0 (  49) :      0.26647 (c= -0.51620412)
   (+) A   7 (  46) -> V   0 (  49) :      1.55291 (c=  1.24615978)
   (+) A   0 (  39) -> V  16 (  65) :      0.11782 (c= -0.34324922)
   (+) A   7 (  46) -> V  16 (  65) :      0.73241 (c=  0.85580859)

   (-) I   0 (  11) -> A   0 (  39) :      0.05738 (c=  0.23954155)
```

<a id="sec:spectroscopyproperties.mcrpa.ntos"></a>
## Natural Transition Orbitals

Rather than analyzing the sections of the excitation vectors directly,
visualizing natural transition orbitals[Martin2003,Helmich-Paris2019a](../../bibliography.md) (NTO)
can be very insightful.
Since NTOs are obtained from a singular value decomposition of the MCRPA
ground-to-excited state (f) transition density matrices
$\rho_{pq}^{0\to f}$, they are independent of any unitary transformation
of the molecular orbital (inactive, active, and virtual) sections and, thus,
independent of type of orbitals (canonical, localized, natural, etc.).

As for [TDDFT](sec:spectroscopyproperties.tddft.natTransOrb) and [ROCIS](sec:spectroscopyproperties.rocis.natTransOrb)
one obtains two sets of orbitals for each state that describe the donation (occupied and active)
and acceptance (active and virtual) of an electron in the electronic
transition. The orbital structure of $\rho_{pq}^{0\to f}$ for CASSCF
wave functions is illustrated in [fig:MCRPA-nto-tdm](#fig:MCRPA-nto-tdm).

<a id="fig:MCRPA-nto-tdm"></a>
*Structure of MCRPA transition density matrix
$\rho_{pq}^{0\to f}$*

Note that the configuration part of the excitation vector contributes
to the active-active block of $\rho_{pq}^{0\to f}$ and is thus respected.

To compute NTOs, only the `DoNTO` flag in the input has to switched
on (`DoNTO true`):

```orca
%mcrpa
 nroots    20    # number of roots
 DoNTO     true  # generate NTOs for converged roots
 NTOThresh 5e-5  # NTO selection threshold
end
```

This will compute all NTOs with a singular value larger then the
`NTOThresh` threshold for ALL roots.

```orca
------------------------------------------------
NATURAL TRANSITION ORBITALS FOR STATE     1 3A  
------------------------------------------------

STATE    1 3A  :  E=   0.033027 au      0.899 eV     7248.5 cm**-1

Threshold for printing occupation numbers 1.0000e-03

     0  : n=  0.99567919
     1  : n=  0.02731085
     2  : n=  0.02231787
     ...

=> Natural Transition Orbitals (donor   ) were saved in ni-II-h2o-6-cas-8-10-mcrpa.mcrpa.1-3A_nto-donor.gbw
=> Natural Transition Orbitals (acceptor) were saved in ni-II-h2o-6-cas-8-10-mcrpa.mcrpa.1-3A_nto-acceptor.gbw
```

For the above example, the most important (controlled by `NTOThresh`)
donating and accepting NTOs of state 1 are written to the `gbw`-type
files.
The NTOs can be visualized with the `orca_plot` program (see Sec. [sec:utilities.plot](#sec:utilities.plot)),
for the donating NTOs
```orca
orca_plot ni-II-h2o-6-cas-8-10-mcrpa.mcrpa.1-3A_nto-donor.gbw -i
```
and for the accepting NTOs
```orca
orca_plot ni-II-h2o-6-cas-8-10-mcrpa.mcrpa.1-3A_nto-acceptor.gbw -i
```
The NTOs are ordered according to their singular value in descending order
as given in the output, starting with index 0 for the most significant NTO pair.

The most dominant NTO pairs (index 0) for the three lowest valence <sup>3</sup>T<sub>g</sub> transitions of
Ni(H<sub>2</sub>O)<sub>6</sub><sup>2+</sup> are given in Fig. [fig:MCRPA_ni-II-h2o-6-ntos](#fig:MCRPA_ni-II-h2o-6-ntos).

<a id="fig:MCRPA_ni-II-h2o-6-ntos"></a>
*Lowest transitions in Ni(H<sub>2</sub>O)<sub>6</sub><sup>2+</sup>.*

<a id="sec:spectroscopyproperties.mcrpa.xas"></a>
## X-Ray Absorption Spectroscopy

It is also possible to compute X-ray absorption spectra (XAS) with the MCRPA module
by making use of the core-valence separation (CVS) approximation.[Helmich-Paris2021c](../../bibliography.md)
For such calculations, the same active space as for ground state CASSCF
 or valence excitation energy  MCRPA calculations should be chosen.
To access MCRPA core excitations, two restrictions are introduced by the CVS approximation:
- The configuration part of the eigenvectors is omitted
  as it is responsible for valence excitations within the valence active orbitals.
- The orbital part of the eigenvectors is restricted to core-active and core-virtual 
  pairs with a user given list of core orbitals

For computing the lowest MCRPA oxygen K-edge transitions of ozone,
 one can employ the following input for an CVS-MCRPA calculation:
```orca
%casscf
 nel    12 # number of active electrons
 norb    9 # number of active orbitals
 nroots  1 # only the ground state
 mult    1 # singlet multiplicity
end

%mcrpa
 NRoots 15            # number of roots / excited states
 DoCVS  true          # turn on core valence separation
 OrbWin 0, 2, -1, -1  # select on the lowest 3 core orbitals
 DoNTO  true          # generate NTOs for converged roots
end
```
Here the first 3 inactive MOs are selected by `OrbWin` that are primarily expanded in the
3 1s atomic orbitals of the three O atoms.
There is no restriction on the virtual orbitals
( `-1` is chosen for first and last virtual MO index).

Note that in constrast to other [multi-reference protocols](sec:casscf.CoreExitedStates.detailed), the core orbitals
must not get added to the active space for CVS-MCRPA calculations.

The most dominant NTO pairs for the four lowest core excitations are given below:
<a id="fig:MCRPA-cvs-ozone"></a>
*Lowest CVS-MCRPA oxygen K-edge transitions in ozone.*

<a id="sec:spectroscopyproperties.mcrpa.computational"></a>
## Computational Aspects

### Large Molecules

The code is intended to be used for medium-sized and larger open-shell
molecules. It has the same scaling as ORCA's first-order CASSCF energy
implementation though a larger pre-factor as the computational cost grow
"in principle" linearly with the number of roots.

The implementation is AO-driven meaning that the computational
bottleneck is the Fock matrix construction for the several
state-specific pseudo AO densities. Note that there are up to 6 pseudo
AO densities for each state. The computational costs can be reduced
significantly if the [RIJCOSX](sec:essentialelements.ri.rijcosx) approximation is employed, which is
highly recommended.

The second most expensive part of the MCRPA computation are the
two-electron integrals with 3 active indices $g_{ptuv}$. As we aim for
running calculations on larger systems, there is only an implementation
of the integral transformation that uses the resolution-of-the-identity
(RI) approximation.

The restrictions on the auxiliary basis sets are the same as for the
CASSCF code (Sec.
[sec:spectroscopyproperties.casscfresp](#sec:spectroscopyproperties.casscfresp)). That is

-   If the Fock matrices are constructed in `Direct` or `Conventional`
    mode, the /C bases are used for the RI approximation of the
    $g_{ptuv}$ integrals.

-   If the [RIJCOSX](sec:essentialelements.ri.rijcosx) approximation for the Fock matrices is employed,
    the /JK bases are used for both the Fock matrices and the $g_{ptuv}$
    integrals.

Note that the [RIJK](sec:essentialelements.ri.rijk) approximation is not yet available.

### Convergence

Before starting running MCRPA, it is recommended to converge the state-specific
 CASSCF energy calculation very tightly.
The [TRAH-CASSCF](sec:modelchemistries.casscf.trah) is ideally suited for that purpose.
Note that property calculations in general assume vanishing
electronic gradients otherwise numerical issues in the eigenvalue /
response equations may occur.

Eigenvalues and eigenvectors are determined by a dedicated variant of the Davidson algorithm
 for solving large-scale TDA or RPA eigenvalue equations.[Olsen1988,Helmich-Paris2019a](../../bibliography.md)
The accuracy of the eigenvalues and eigenvectors is solely determined by `TolR` (default 1.e-5)
 that is compared to the Frobenius of the residual vector for each root.

Similar to converging CASSCF equations, the MCTDA and MCRPA convergence rates are also affected by
the choice of molecules orbitals.
This has to be setup in the `%casscf` input block. The MCRPA program will not
change the converged orbitals and CI coefficients.
For most calculations, the default settings are most appropriate which are
*canonical orbitals* for inactive and virtual orbitals and *natural orbitals* for active orbitals.
as explained in subsection [sec:modelchemistries.casscf.actorbs](#sec:modelchemistries.casscf.actorbs).
For multi-center systems as bimetallic transition metal complexes, *localized orbitals* are a better choice.
Purified d or f orbitals (`ActOrbs dorbs` or `ddorbs` and `forbs`)
for single-metal complexes are often helpful for analyzing excitations, though, their choice
usually result in slower convergence of the eigenvalue equations.

To facilitate quick convergence of the eigenvalue equations, we start the iterations
 from eigenvectors that were obtained from direct diagonalization of full Hessian and metric matrices that
 were compute for a subset of elements. 
This is referred to as P-space or `full` method which is the default for obtaining initial eigenvectors
 but also the preconditioner of the TDA/RPA Davidson algorithm (`PreCond full`).
The P-space method contains the orbital-orbital and configuration-configuration blocks that are
 diagonalized individually. Orbital-configuration coupling is omitted here.
The size of the P space is controlled by the keyword `PreConMaxRed` which is set to 400 by default.
Faster convergence can be expected with larger P-space dimensions, though the cost of the full diagonalization
 increase cubically.
Alternatively, the approximate diagonal Hessian[chaban1997theor](../../bibliography.md) and metric can be used for preconditioning
 (`PreCond diag`), but not for the initial eigenvectors.
It is recommended to employ `Precond full`.

<a id="sec:spectroscopyproperties.mcrpa.keywords"></a>
## Keyword List

```orca
%mcrpa

  NRoots       0         # The number of desired roots

  TolR         1e-5      # Convergence threshold for residual norm
  PrintWF      CFG       # print CI part in (CFG (default), CSF, or DET basis)
  TolPrint     1e-2      # Threshold for printing elements of excitation vector

  MaxRed       200       # maximum size of reduces space for ALL VECTORS IN TOTAL
  MaxIter      100       # maximum number of (Davidson) iterations
                         
  TDA          false     # Switch off full TD-CASSCF (Tamm-Dancoff approximation)
  
  DoNTO        false     # Generate Natural Transition Orbitals
  NTOThresh    1e-3      # Threshold for printing occupation numbers

  DoCVS        false     # toggle core valence separation (CVS) for XAS
  OrbWin       i0, i1, a0, a1 # first and last inactive and virtual MO, respectively

  PreCond      full      # (default) P-space preconditioner uses parts of exact
                         # Hessian matrix
               diag      # diagonal preconditioner approximate diagonal
	                 # Hessian elements

  PreConMaxRed 400       # dimension of exact Hessian for preconditioning

  DoOrbResp    true      # turn orbital response off -> CAS-CI method

  DoCD                  true  # circular dichroism calculation
  DoDipoleLength        true  # electric moments in a length formulation
  DoDipoleVelocity      true  # electric moments in a velocity formulation
  DoFullSemiclassical   false # request the calculation of complete semiclassical multipolar moments
  DecomposeFosc         false # request the decomposition of the oscillator strengths in a multipolar expansion.

```
