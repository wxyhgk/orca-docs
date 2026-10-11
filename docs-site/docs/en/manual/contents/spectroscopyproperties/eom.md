

<a id="sec:spectroscopyproperties.eom"></a>
# Excited States via EOM-CCSD

Many of the previously described methods are based on the
single excitation framework. For a more accurate treatment, double
excitations should also be considered. The equation of motion (EOM) CCSD
method (and the closely related family of linear response CC methods)
provides an accurate way of describing excited, ionized, and electron-attached
states based on singles and doubles excitations within the
coupled-cluster framework.

<a id="sec:spectroscopyproperties.eom.theory"></a>
## Theory

The EOM wave function is parametrized in the following manner

$$
\mathcal{R}|\Psi_{CC}\rangle,
$$

i.e. via the action of a linear excitation operator $\mathcal{R}$ on the
coupled-cluster ground state wave function $\Psi_{CC}$. Here,
$\mathcal{R}$ is a particle conserving operator, in the case of the
excitation energy problem. However, this is not true for the ionization
or electron attachment problems, where $\mathcal{R}$ is a net
annihilation or net creation operator, respectively. The ground state
coupled-cluster T-amplitudes are obtained from a CCSD calculation, and
our task is to obtain $\mathcal{R}$. Note that since the CC Hamiltonian
is nonsymmetric, a left hand solution ($\mathcal{L}$) would also be
needed to evaluate properties. For the calculation of excitation,
ionization or electron attachment energies, however, it is enough to
obtain the right hand solutions ($\mathcal{R}$). In principle, this is
done by building the Hamiltonian and diagonalizing it in order to obtain
energy expectation values.

In practice, the size of the CCSD Hamiltonian matrix is prohibitively
large and thus, various methods have been devised to obtain its lowest
few eigenvalues and eigenstates. One of the most popular of these
approaches is the Davidson method, which can be summarized as follows:

-   Construct an initial guess of orthogonal trial vectors, $C$.

-   Evaluate the sigma vectors $\sigma=HC$.

-   Build model Hamiltonian $\mathcal{H}=C^T\sigma$.

-   Diagonalize $\mathcal{H}$: $\mathcal{E=U}^T\mathcal{HU}$.

-   Compute Ritz vectors $X=C\mathcal{U}$.

-   Compute residuals $R=X\mathcal{E}-\sigma\mathcal{U}$, check
    convergence: if yes, pass $X,\mathcal{E}$ as solutions.

-   Preconditioning: $T=MR$ (many possible choices for the
    preconditioner $M$).

-   Check if adding new trial vectors would exceed the maximum number of
    trial vectors:

    -   if no, add $T$ to $C$, and orthonormalize the united set

    -   if yes, then set $X$ as $C$ (orthonormalize if $H$ is
        nonsymmetric); then add $T$ and orthonormalize

The advantage of the above method is that, instead of the full
Hamiltonian, only the sigma vectors have to be explicitly evaluated and
stored.

It is also possible to use a lower scaling version of the EOM-CCSD
methods, which relies on the perturbative truncation of the
coupled-cluster similarity transformed Hamiltonian. Presently, only the
second order truncated version (CCSD(2) approximation) is available for
closed-shell molecules (RHF). However, it is better to use the PNO based
implementation, as it has the cost of EOM-CCSD(2), but its accuracy is
comparable to canonical EOM-CCSD.

<a id="sec:spectroscopyproperties.eom.theory.initguess"></a>
### Initial Guess

The present initial guess in the RHF EOM implementation consists of
constructing a CIS Hamiltonian of a certain dimension, and diagonalizing
it. The roots are preselected based on the energetic ordering of the
diagonal elements of the Hamiltonian. In the UHF case, the guess is
constructed from the solutions of a UHF CIS calculation. The number of
roots in the initial guess is determined as 20 times the number of roots
desired in EOM (`NRoots`) if `NDav` is 20 or smaller, otherwise it is
set to `NDav` times the number of EOM roots. If the parameter `NInits`
is larger than zero, then the number of initial guess roots will be set
to this parameter times `NRoots`. The maximum possible number of roots
is the full CIS dimension, ($N_ON_V$ (RHF) or
$N_{O_{\alpha} }N_{V_{\alpha} } + N_{O_{\beta} }N_{V_{\beta} }$ (UHF)) .
One should keep in mind, while increasing the number of initial guess
vectors, that this corresponds to diagonalizing a matrix of increasing
dimension. If, for example `NRoots` is 10, then by default 200 roots are
considered in the initial guess (unless it exceeds the size of the CIS
space), or if `NInits` is set to 100, then there will be 1000 roots in
the guess. In some cases, the roots calculated using EOM may not be the
lowest ones, but a few of these may be replaced by some higher roots
which are "easier" to find. In such cases, it may help to increase
`NRoots` or `NInits` to converge to the proper roots. The program can be
made to follow the initial CIS guess by setting `FollowCIS` to true and is
necessary if we wish to ionize or excite from inner-valence or core
orbitals. In the RHF implementation, the core orbital, from which the
ionization or excitation originates, can be specified using the keyword
`CoreHole`, in addition to setting `DoCore` and `FollowCIS` to true. The
`CoreHole` keyword is quite general and in principle, ionization or
excitation processes from any occupied orbital can be specified using
this keyword.

<a id="sec:spectroscopyproperties.eom.theory.hamiltonian"></a>
### Hamiltonian Construction

The Hamiltonian construction begins by calling the sigma routines. In
the case of the closed-shell code, the logical variables `UseEOMOptS`
and `UseEOMOptD` choose the routines to be used in the evaluation of the
singles and doubles sigma vectors, respectively. If true, the optimized
sigma routine, using dressed integrals, will be used. This should not be
changed, the option is there mainly for debugging purposes. If set to
false, an automatically generated, and much slower serial code will be
used instead. In the case of the open-shell UHF implementation,
optimized sigma routines have been generated using the ORCA Automated
Generator Environment (AGE) [krupicka2017ORCA_AGE](../../bibliography.md). In each early
iteration, $N_R$ sigma vectors will be determined, except in the case of
a restart, where the number of sigma vectors is $2N_R$. For further
details on convergence, see
[theory.conv](#sec:spectroscopyproperties.eom.theory.conv) below.

The most time consuming part of the sigma vector construction is the
formation of the external exchange contribution, which can be influenced
via the CC keyword `KCOpt`. Currently, there are three options that are
compatible with the RHF EOM implementation: `KC_MO`,`KC_AOX` and
`KC_AOBLAS` and `KC_AOX` is the only option
available in the UHF EOM code. The external exchange term can be treated
most efficiently using COSX, which in the closed-shell case, leads to
average speed ups of 10x for the external exchange term and an overall
speedup of 3x for the EOM calculation. This is accompanied by a drastic
reduction of the storage cost[Dutta2016COSX](../../bibliography.md). The error introduced is
below 1 meV, which is 200-fold less than the error bar of the
method[Dutta2016COSX](../../bibliography.md) itself. It is the default for `KCOpt` `KC_AOX`
and `KC_AOBLAS` and can be controlled by the keyword `DOCOSXEOM`. The
default grid settings for EOM are `GridX 1` and `IntAccX 2.68`.

Once the sigma vectors are available, they are multiplied with the trial
vectors to yield the reduced space Hamiltonian. The Hamiltonian is built
in a way that, in each iteration, only the new vector products are added
to the "edge" of the old Hamiltonian, so that a full build is avoided.
It should be clear that the parameter `NDav` plays an important role
here, since it determines the maximum size of the Hamiltonian
($N_DN_R$), and also controls how much memory is needed for the trial
and sigma vectors, as seen above. Since the choice of this parameter
influences convergence properties, it will be discussed further in
[theory.conv](#sec:spectroscopyproperties.eom.theory.conv).

<a id="sec:spectroscopyproperties.eom.theory.nonsymmetric"></a>
### Solution of the (Nonsymmetric) Eigenproblem

Following the construction of the Hamiltonian, a nonsymmetric
eigensolver is called. In this case, it is possible to have complex
eigenvalues. In practice, this is rarely the case, and indicates a
problem of some kind. A warning will be given if this happens, however,
one may get away with this if it only happens in an isolated iteration
step.

Once the eigenvectors are available, they are compared with those of the
previous iteration, if root homing is turned on, i.e. if the
`RootHoming` keyword is set to true. This means evaluating the overlap
of the old and new eigenvectors, in order to keep track of the possible
movement of the eigenvectors if root flipping occurs. If converged roots
are removed from further iterations (see next section), it is important
to keep track of changes in ordering, especially if a converged and a
non-converged root is swapped. After diagonalization, the Ritz vectors
and residuals can be evaluated.

<a id="sec:spectroscopyproperties.eom.theory.conv"></a>
### Convergence, Restart, Preconditioning and Subspace Expansion

Convergence is signaled once a residual square norm based criteria is
fulfilled. This criteria is determined by the `CheckEachRoot` keyword.
If it is true (default), the convergence of the residual square norm of
each root is checked separately. This is due to the fact that different
roots converge at a different rate. Once a root is converged, no new
trial vectors will be generated, belonging to that vector. This means
that the EOM iterations will progressively become faster (until
restart). Turning off the rootwise convergence check is possible, but
not recommended. In this case, the maximum of all residual square norms
is checked for convergence, and all iterations will take roughly the
same amount of time since no vectors are removed in any iteration.
However, this procedure can be numerically unstable, since the residuals
of some roots might become very close to zero, and trying to generate
new vectors, which are orthogonal to these, may lead to numerical
disaster. In short, the recommended default is having both
`CheckEachRoot` and `RootHoming` set to true. If `CheckEachRoot` is
false, then `RootHoming` should also be set to false, as it may cause
problems if `NDav` is too small. The convergence threshold of the
residual in Davidson's method can be larger than that for the ground
state CC residual threshold in order to obtain converged results.
Namely, a value of `DTol` of 1e-5 is almost always enough to get well
converged energies.

At this point it is worth discussing the role of the keyword `NDav`.
This keyword determines at what point the Davidson algorithm should be
restarted. If it is chosen too small, it may cause slow convergence. If
this value is too large, this may result in overwhelming demands on
memory/disk space requirements. The default value (20) is chosen with
the hope that no, or maybe one restart will be required. It should only
be changed if computational resources demand it. However, the treatment
of core ionization or core excitation processes often requires a large
value of `NDav`. At restart, the Ritz vectors are copied as new trial vectors
for all roots, which will then be orthonormalized, while new vectors
will only be generated for the non-converged roots. This means that the
step after the rebuilding of the expansion space will be 1-2 times as
expensive as one of the initial steps.

New directions (trial vectors) are generated from the preconditioned
residual vectors. If no preconditioning is applied (the preconditioner
is taken to be a unit matrix), one falls back to the Lanczos algorithm,
which is inferior to the Davidson algorithm. This happens if the keyword
`DoLanczos` is true. This is not recommended, as the Lanczos algorithm
converges several times slower than Davidson's, and is there for
debugging mainly. The original Davidson preconditioner is the inverse of
a diagonal matrix which contains the difference of the diagonal elements
of the Hamiltonian and the current approximation to the eigenvalue
belonging to the given root. Let us consider the closed-shell RHF
implementation for simplicity. If $R_{ia}$ and $R_{ijab}$ are elements
of the singles and doubles amplitudes, respectively, then the updated
vectors ($T_{ia}$, $T_{ijab}$) have the form

$$
T_{ia}=\frac{R_{ia} }{D_{ia}+\mathcal{E}_R}
$$

for singles, and

$$
T_{ijab}=\frac{R_{ia} }{D_{ijab}+\mathcal{E}_R}
$$

for doubles. Here, $D_{ia}$ and $D_{ijab}$ are related to, and possibly
approximations of, the respective diagonal Hamiltonian elements. The
simplest approximation is just to construct these from diagonal Fock
matrix elements (i.e. orbital energies) as
$D_{ia}=\varepsilon_a-\varepsilon_i$ and
$D_{ijab}=\varepsilon_a+\varepsilon_b-\varepsilon_i-\varepsilon_j$. A
slightly better preconditioning can be obtained as follows. For singles,
take the exact CIS diagonal elements,
$D_{ia}=\varepsilon_a-\varepsilon_i+\overline{g}_{iiaa}$, where the last
term is the respective antisymmetrized integral; and construct the
doubles as $D_{ijab}=D_{ia}+D_{jb}$. This is the default, and can be
changed back to the simple Fock matrix guess by setting `UseCISUpdate`
to false.

Following the preconditioning step, the resulting vectors are
orthogonalized to the previous set of trial vectors, and orthonormalized
among themselves. Since, the trial vectors do not change once they are
generated (unless a restart occurs), only the new elements of the
overlap matrix need to be generated for the orthonormalization. The
numerical threshold for the inversion (and other division steps) is
controlled by the parameter `OTol`. Finally, the amount of printed
information can be controlled via the `PrintLevel` keyword. If not given
or equal to 2, only basic iteration information will be printed. If set
to 3, detailed iteration information will be printed (recommended if
timing results for individual steps are required), while 4 or higher
triggers additional (and very verbose) information from other
subroutines as well.

The default solver is a multi-root Davidson procedure. The single-root
solver can be initiated by setting `DoRootwise` and `FollowCIS` to true.
The latter is more stable when a large number of roots are requested.

<a id="sec:spectroscopyproperties.eom.theory.properties"></a>
### Properties in the RHF EOM implementation

The only property that can be calculated with the current RHF EOM
implementation is the transition moment. It is calculated as a CI-like
expectation value, as proposed by Stanton and Bartlett. The right and
left transition density are defined as

$$
\rho_{pq}^{Gr\rightarrow Ex} =\langle\phi_{0}|(1+\Lambda)[e^{-T}\{p^{+}q^{-}\}e^{T},R]|\phi_{0}\rangle
$$

$$
\rho_{pq}^{Ex\rightarrow Gr} =\langle\phi_{0}|Le^{-T}\{p^{+}q^{-}\}e^{T}|\phi_{0}\rangle
$$

In the above equation, $\Lambda$ corresponds to the ground state left
vector, which needs to be solved once and $L$ is the left vector, which
needs to be solved separately for each root. Once the right and left
vectors have been obtained, the left and right transition densities are
constructed and the oscillator strength is calculated using the following
formula

$$
f=\frac{2}{3}\varepsilon|\mu_{pq}\rho_{pq}^{Ex\rightarrow Gr}||\mu_{pq}\rho_{pq}^{Gr\rightarrow Ex}|
$$

The oscillator strength, calculated by default, employs a linear
approximation for $\Lambda$. The $L$ vectors are, on the other hand,
calculated as a general inverse of the corresponding $R$ vectors. This
approximation requires no additional effort over the energy calculation
and gives similar accuracy as that of the exact oscillator strength
calculation, which is at least twice the cost of the energy calculation.
Exact EOM-CC transition moments can, however, be calculated by setting
`DoLeft` and `DoTDM` to true. Please note that transition moments have not
yet been implemented for the UHF EOM-CCSD approach.

<a id="sec:spectroscopyproperties.eom.use"></a>
## General Use

The EOM-CCSD routine is part of the `orca_mdci` module of the ORCA
program package. It is called after a successful coupled-cluster
calculation, if the appropriate flags and the number of roots have been
set. In the following chapter, the general program flow and the input
parameters of the EOM routine will be described. For an RHF or UHF reference, the EE-, IP-
and EA-EOM-CCSD approaches are available for the computation of
excitation energies, ionization potentials and electron affinities,
respectively. Currently, the following simple input keywords are available:

```orca
!EOM-CCSD      # same as !EE-EOM-CCSD
!EE-EOM-CCSD   # EOM for electronically excited states
!IP-EOM-CCSD   # IP version
!EA-EOM-CCSD   # EA version
```

The simplest way to perform an EOM calculation is via the usage of the
`EOM-CCSD` keyword, together with the specification of the desired
number of roots:

```orca
!EOM-CCSD      # same as !EE-EOM-CCSD
!EE-EOM-CCSD   # EOM for electronically excited states
!IP-EOM-CCSD   # IP version
!EA-EOM-CCSD   # EA version
```

The above input will call the EOM routine with default settings. The
main output is a list of excitation energies, augmented with some
further state-specific data. For the above input, the following output
is obtained:

```orca
----------------------
EOM-CCSD RESULTS (RHS)
----------------------

IROOT=  1:  0.147823 au     4.022 eV   32443.5 cm**-1
  Amplitude    Excitation
   0.107945     4 ->   8
   0.665496     7 ->   8
   0.104633     7 ->   8     6 ->   8
  Ground state amplitude:  0.000000
Percentage singles character=     92.32

IROOT=  2:  0.314133 au     8.548 eV   68944.3 cm**-1
  Amplitude    Excitation
   0.671246     7 ->   9
  Ground state amplitude: -0.000000
Percentage singles character=     90.42

IROOT=  3:  0.343833 au     9.356 eV   75462.6 cm**-1
  Amplitude    Excitation
  -0.670633     5 ->   8
  -0.112538     6 ->   8     5 ->   8
  Ground state amplitude:  0.000000
Percentage singles character=     92.00

IROOT=  4:  0.364199 au     9.910 eV   79932.5 cm**-1
  Amplitude    Excitation
   0.102777     4 ->  10
  -0.484661     6 ->   8
   0.438311     7 ->  10
  -0.167512     6 ->   8     6 ->   8
  Ground state amplitude: -0.021060
Percentage singles character=     87.22

IROOT=  5:  0.389398 au    10.596 eV   85463.0 cm**-1
  Amplitude    Excitation
   0.646812     4 ->   8
  -0.122387     7 ->   8
   0.171366     7 ->   8     6 ->   8
  Ground state amplitude:  0.000000
Percentage singles character=     87.47

IROOT=  6:  0.414587 au    11.281 eV   90991.4 cm**-1
  Amplitude    Excitation
  -0.378418     6 ->   8
  -0.537292     7 ->  10
  -0.124246     6 ->   8     6 ->   8
  Ground state amplitude: -0.061047
Percentage singles character=     89.13

IROOT=  7:  0.423861 au    11.534 eV   93026.7 cm**-1
  Amplitude    Excitation
   0.673806     7 ->  11
  Ground state amplitude:  0.000000
Percentage singles character=     93.14

IROOT=  8:  0.444201 au    12.087 eV   97490.8 cm**-1
  Amplitude    Excitation
   0.664877     6 ->   9
   0.130475     6 ->   9     6 ->   8
  Ground state amplitude: -0.000000
Percentage singles character=     87.17

IROOT=  9:  0.510514 au    13.892 eV  112044.8 cm**-1
  Amplitude    Excitation
  -0.665791     6 ->  10
   0.114259     6 ->  15
  -0.124374     6 ->  10     6 ->   8
  Ground state amplitude: -0.000000
```

The IP and EA versions can be called using the keywords `IP-EOM-CCSD`
and `EA-EOM-CCSD`, respectively. For open-shell systems (UHF reference
wavefunction), IP/EA-EOM-CCSD calculations require an additional
keyword. Namely, an IP/EA calculation involving the removal/attachment
of an $\alpha$ electron is requested by setting the `DoAlpha` keyword to
true in the %mdci block, while setting the `DoBeta` keyword to true
selects an IP/EA calculation for the removal/attachment of a $\beta$
electron. Note that `DoAlpha` and `DoBeta` cannot simultaneously be true
and that the calculation defaults to one in which `DoAlpha` is true if
no keyword is specified on input. A simple example of the input for a
UHF IP-EOM-CCSD calculation for the removal of an $\alpha$ electron is
given below.

```mol
title: structure 1
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
2
structure (0 3)
O           0.0          0.0          0.0
O           0.0          0.0        1.207
--- input ---
! IP-EOM-CCSD cc-pVDZ 
%mdci
  DoAlpha true
  NRoots 7
end

*xyz 0 3
  O      0.0 0.0 0.0
  O      0.0 0.0 1.207
*
```

<a id="sec:spectroscopyproperties.excitedstates.eom.capabilities"></a>
### Capabilities

At present, the EOM routine is able to perform excited, ionized and
electron attached state calculations, for both closed- or open-shell
systems, using RHF or UHF reference wave functions, respectively. It can
be used for serial and parallel calculations. The method is available in
the back-transformed PNO and DLPNO framework enabling the calculation of
large molecules - see Section
[spectroscopyproperties.dleom](#sec:spectroscopyproperties.dleom) and Section
[excitedstates.dlpnoeom](#sec:spectroscopyproperties.excitedstates.dlpnoeom). In the closed-shell case (RHF), a
lower-scaling version can be invoked by setting the `CCSD2` keyword to
true in the %mdci section. The latter is a second-order approximation to
the conventional EOM-CCSD. For the time being, the most useful
information provided is the list of the excitation energies, the
ionization potentials or the electron affinities. The ground to excited
state transition moments are also available for the closed-shell
implementation of EE-EOM-CCSD.

<a id="sec:spectroscopyproperties.eom.memory"></a>
## Memory Management

The most important data coming from the coupled-cluster routine are the
ground state energy and wave function, and the molecular integrals. The
integrals are then used to create "dressed" integral containers, which
allows for an efficient factorization of the EOM equations, since these
dressed quantities do not change during the calculation. Most of these
are written on disk, with the possible exception of the integral
container which has three external labels. This, and the solver files
may remain in core if enough memory is available. The program
sequentially tries to allocate memory for the files in the order of
their importance, and what cannot be kept in core, goes on disk. The
order of allocation is as follows: 1. residual vectors, 2. Ritz vectors,
3. three external integrals, 4. sigma vectors and 5. state (trial)
vectors, as seen in the example below:

```orca
--------------------------------
AUTOMATIC CHOICE OF INCORE LEVEL
--------------------------------

Memory available                           ...   6512.00 MB
Memory needed for Residual-vectors         ...     71.27 MB
Memory needed for Ritz-vectors             ...     71.27 MB
Memory needed for 3-ext integrals          ...     92.05 MB
Memory needed for Sigma-vectors            ...   1425.31 MB
Memory needed for State-vectors            ...   1425.31 MB
 -> Final InCoreLevel    ... 5
```

Half of the memory specified with the keyword `MaxCore` is distributed
among the five candidates. In the above case, everything fits in memory.
Note that these are only the largest contributors to memory consumption,
and there should ideally be a safety margin when allocating memory.

In order to estimate the amount of necessary memory, it should be kept
in mind that, in the closed shell case, the memory requirements of the
residual and Ritz vectors are proportional to $N_RN_PN_V^2$, the three
external integrals to $N_RN_ON_V^3$ and the sigma and trial vectors to
$N_DN_RN_PN_V^2$, where $N_O$ and $N_V$ are the number of occupied and
virtual orbitals, $N_P=\frac{N_O(N_O+1) }{2}$ is the number of occupied
pairs, $N_R$ is the number of roots, and $N_D$ is the maximum size of
the reduced space. The keyword `NRoots` sets $N_R$, while `NDav`
determines $N_D$. Luckily, the contributions that, in our experience,
are the most important to keep in memory, are also the ones that require
the smallest amount of it. It is advisable to use `KCOpt AOBLAS`, as it
has the lowest memory requirements.

Note that in the UHF EE-EOM-CCSD implementation, the memory requirements
of the residual and Ritz vectors are proportional to
$N_R(N_{P_{\alpha} }N_{V_{\alpha} }^2 + N_{P_{\beta} }N_{V_{\beta} }^2 + N_{O_{\alpha} }N_{O_{\beta} }N_{V_{\alpha} }N_{V_{\beta} })$,
the three external integrals to
$N_R(N_{O_{\alpha} }N_{V_{\alpha} }^2 + N_{O_{\beta} }N_{V_{\beta} }^2 + N_{O_{\alpha} }N_{V_{\alpha} }N_{V_{\beta} }^2 + N_{O_{\beta} }N_{V_{\beta} }N_{V_{\alpha} }^2)$
and the sigma and trial vectors memory requirements are proportional to
$N_DN_R(N_{P_{\alpha} }N_{V_{\alpha} }^2 + N_{P_{\beta} }N_{V_{\beta} }^2 + N_{O_{\alpha} }N_{O_{\beta} }N_{V_{\alpha} }N_{V_{\beta} })$,
where $N_{O_{\alpha} }$, $N_{O_{\beta} }$, $N_{V_{\alpha} }$ and
$N_{V_{\beta} }$ are respectively, the number of occupied alpha,
occupied beta, virtual alpha and virtual beta orbitals and
$N_{P_{\alpha} }=\frac{N_{O_{\alpha} }(N_{O_{\alpha} }-1) }{2}$ and
$N_{P_{\beta} }=\frac{N_{O_{\beta} }(N_{O_{\beta} }-1) }{2}$ are the
number of alpha and beta occupied pairs, respectively.

<a id="sec:spectroscopyproperties.eom.tips"></a>
## Some tips and tricks for EOM-CC calculation

-   The COSX approximation gives significant savings in terms of memory
    use, disk space use and computational timings with almost no loss
    of accuracy[Dutta2016COSX](../../bibliography.md). Therefore, the preferred setting for
    large-scale calculations should include `DoCOSXEOM true`, `DoAOX3e true`
    and `KCOpt KC_AOBLAS` (Note that `KC_AOX` is the only option available for
    `KCOpt` in the UHF implementation).

-   The EOM-CC code in ORCA has three versions of the Davidson solver.
    The default one is the multi-root solver which does optimization of all
    the roots together. It gives the fastest convergence and is more
    suitable when one is interested only in a few roots of a big
    molecule. However, the multi-root solver can run into numerical
    issues, if more than 10 roots are desired. In that case, one can
    invoke the root-wise solver by setting `DoRootwise true`. The single
    root solver is very stable and should be used when a large number of
    roots are desired. However, the convergence of the single root
    solver is slower than the multi-root one. In the RHF implementation,
    there is also a batchwise solver, where a subset of the total number
    of roots is optimized together. This can be invoked by setting
    `NRootsPerBatch true` and is intermediate between the multi-root
    and single-root solvers in terms of stability and convergence.

-   If the EOM iterations do not converge within 50 cycles, one can try
    to increase the number of iterations by setting `MaxIter` in the `%mdci` 
    block to a larger value. One can also try to increase the dimension of the Krylov
    space in the Davidson solver by increasing the `NDav` value and this generally helps to
    accelerate convergence. However, setting `NDav` to a value larger
    than 200 can make the calculation prohibitively costly especially in terms of memory.

-   Convergence thresholds of `DTol 1e-5` (Davidson convergence) and `STol`
    `1e-7` (ground state CCSD convergence) generally yield sufficiently
    converged energies, and are suitable for most purposes.

-   The normal Davidson solver generally leads to the lowest-energy
    solutions. This procedure can also yield roots dominated by double
    excitations (the so-called satellite states) for the IP and EA
    variants of EOM-CC, when one asks for a large number of roots. If one is
    interested in the low-lying Koopman's type of IP and EA states, they
    can be obtained by setting `FollowCIS` to true. This will follow the
    initial guess provided by the Fock operators.

<a id="sec:spectroscopyproperties.eom.options"></a>
## Full keyword list

The simple input keywords related to EOM-CC are collected in [tab:spectroscopyproperties.eom.options.simple](#tab:spectroscopyproperties.eom.options.simple). 
The input keywords of the `%mdci` block related to UHF EOM-CC are collected in [tab:spectroscopyproperties.eom.options.uhfmdciblock](#tab:spectroscopyproperties.eom.options.uhfmdciblock). 
The input keywords of the `%mdci` block related to RHF EOM-CC are collected in [tab:spectroscopyproperties.eom.options.rhfmdciblock](#tab:spectroscopyproperties.eom.options.rhfmdciblock).

<a id="tab:spectroscopyproperties.eom.options.simple"></a>
!!! note "Simple input keywords for EOM-CC."
    | Keyword       | Description                              |
    |:--------------|:-----------------------------------------|
    | `EOM-CCSD`    | Same as `EE-EOM-CCSD`                    |
    | `EE-EOM-CCSD` | EOM-CC for electronically excited states |
    | `IP-EOM-CCSD` | IP version                               |
    | `EA-EOM-CCSD` | EA version                               |

<a id="tab:spectroscopyproperties.eom.options.rhfmdciblock"></a>
!!! note "`%mdci` block input keywords for RHF EOM-CC with defaults in parentheses."

    | Keyword | Options | Description |
    | --- | --- | --- |
    | `DoEOM` (false) | `true/false` | Perform EOM? |
    | `UseEOMOptS` (true) | `true/false` | Use optimized sigma routines for singles? |
    | `UseEOMOptD` (true) | `true/false` | Use optimized sigma routines for doubles? |
    | `NDav` (20) | `<int>` | Max. size of reduced space (i.e. 20×NRoots) |
    | `CCSD2` (false) | `true/false` | Use the lower scaling CCSD(2) approximation? |
    | `CheckEachRoot` (true) | `true/false` | Check convergence for each root separately? |
    | `RootHoming` (true) | `true/false` | Apply root homing? |
    | `DoLanczos` (false) | `true/false` | Use the Lanczos procedure rather than Davidson? |
    | `UseCISUpdate` (true) | `true/false` | Use diagonal CIS for updating? |
    | `NInits` (0) | `<int>` | Number of roots in the initial guess; if 0, use preset value |
    | `DRESS3ES` (true) | `true/false` | Construct the external dressing to singles or calculate on the fly? |
    | `DRESS3ED` (false) | `true/false` | Construct the external dressing to doubles or calculate on the fly? |
    | `DOCOSXEOM` (false) | `true/false` | Use COSX approximation for external exchange term in EOM? |
    | `DOAOX3E` (false) | `true/false` | Use COSX approximation for 4 external terms contribution to 3-external intermediate? |
    | `DoRootwise` (false) | `true/false` | Solve for each root separately? More stable for large number of roots. |
    | `DoTDM` (false) | `true/false` | Option for calculation of default transition moment? |
    | `Doleft` (false) | `true/false` | Calculation of exact left vector? |
    | `NRootsPerBatch` (1) | `<int>` | Number of roots calculated together |
    | `FOLLOWCIS` (false) | `true/false` | Follows the initial singles guess? |
    | `DoCore` (true) | `true/false` | Initiates ionization or excitation from core orbital? |
    | `CoreHole` (0) | `<int>` | Core orbital from which ionization or excitation is needed |
    | `CVSEP` (false) | `true/false` | Separate core orbitals from valence? |
    | `DTol` (1e-5) | `<real>` | Default for EOM residual threshold |
    | `NRoots` (9) | `<int>` | Number of roots |
    | `OTol` (1e-14) | `<real>` | Orthogonalization threshold |
    | `KCOpt` |  | Method for external exchange formation |
    |  | `KC_MO` |  |
    |  | `KC_AOX` | When asked for exact TDM calculation |
    |  | `KC_AOBLAS` | Most efficient |
    | `PrintLevel` (3) | `<int>` | The amount of information to be printed |
    | `MaxCore` (500) | `<int>` | Total amount of memory |

<a id="tab:spectroscopyproperties.eom.options.uhfmdciblock"></a>
!!! note "`%mdci` block input keywords for UHF EOM-CC with defaults in parentheses."

    | Keyword | Options | Description |
    | --- | --- | --- |
    | `DoEOM` (false) | `true/false` | Perform EOM? |
    | `DoAlpha` (false) | `true/false` | Removal/attachment of an alpha electron (IP/EA calculations)? |
    | `DoBeta` (false) | `true/false` | Removal/attachment of a beta electron (IP/EA calculations)? |
    | `NDav` (20) | `<int>` | Max. size of reduced space (i.e. 20×NRoots) |
    | `UseQROs` (false) | `true/false` | Use QROs? |
    | `CheckEachRoot` (true) | `true/false` | Check convergence for each root separately? |
    | `RootHoming` (true) | `true/false` | Apply root homing? |
    | `DoLanczos` (false) | `true/false` | Use the Lanczos procedure rather than Davidson? |
    | `DoOlsen` (false) | `true/false` | Use the Olsen procedure rather than Davidson? |
    | `UseCISUpdate` (true) | `true/false` | Use diagonal CIS for updating? |
    | `NInits` (0) | `<int>` | Number of roots in the initial guess; if 0, use preset value |
    | `DOCOSXEOM` (false) | `true/false` | Use COSX approximation for external exchange term in EOM? |
    | `DOAOX3E` (false) | `true/false` | Use COSX approximation for 4 external terms contribution to 3-external intermediate? |
    | `DoRootwise` (false) | `true/false` | Solve for each root separately? More stable for large number of roots |
    | `NRootsPerBatch` (1) | `<int>` | Number of roots calculated together |
    | `FOLLOWCIS` (true) | `true/false` | Follow the initial singles guess? |
    | `DTol` (1e-5) | `<real>` | Default for EOM residual threshold |
    | `NRoots` (9) | `<int>` | Number of roots |
    | `OTol` (1e-14) | `<real>` | Orthogonalization threshold |
    | `KCOpt` | `KC_AOX` | AO exchange for the four external contributions |
    | `PrintLevel` (3) | `<int>` | The amount of information to be printed |
    | `MaxCore` (500) | `<int>` | Total amount of memory |

