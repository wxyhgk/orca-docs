```{index} DCD-CAS
```

(sec:modelchemistries.dcdcas2)=
# Dynamic Correlation Dressed CAS

Non-degenerate multireference perturbation theory (MRPT) methods, such
as NEVPT2 or CASPT2, have the 0th order part of the wave function fixed
by a preceding CASSCF calculation. The latter can be a problem if the
CASSCF states are biased towards a wrong state composition in terms of
electron configurations. In these instances, a quasi-degenerate or
multi-state formulation is necessary, for example the QD-NEVPT2
described in Section {ref}`sec:modelchemistries.nevpt2.qdnev`. A drawback of these approaches is that the
results depend on the number of included states. The 2nd order Dynamic Correlation Dressed Complete Active Space method (DCD-CAS(2)) is a post-CASSCF MRPT method of the perturb-then-diagonalize
kind, i.e. it can modify the CAS wavefunction compared to the previous
CASSCF.{cite}`PathakLang2017DCDCAS` DCD-CAS(2) offers
an alternative uncontracted approach, where a dressed CASCI matrix is
constructed. Its diagonalization yields correlated energies and 0th
order states that are remixed in the CASCI space under the effect of
dynamic correlation.{cite}`PathakLang2017DCDCAS` In cases where CASSCF already provides a
good 0th order wavefunction, DCD-CAS(2) energies are comparable to
NEVPT2.

## Theory of Nonrelativistic DCD-CAS(2) 

The DCD-CAS(2) method is based on solving the eigenvalue problem of an
effective Hamiltonian of the form

$$H_{IJ}^{\text{DCD}, S} = \langle \Phi_I^{SS} | H | \Phi_J^{SS} \rangle - \sum_{K \in \text{FOIS} } \frac{\langle \Phi_I^{SS} | H | \tilde{\Phi}_K^{SS} \rangle \langle \tilde{\Phi}_K^{SS} | H | \Phi_J^{SS} \rangle }{E_K^S - E_0^S}$$

for each total spin $S$ separately. The 0th order energies $E_K^S$ of
the perturbers $|\tilde{\Phi}_K^{SS}\rangle$ are obtained by
diagonalizing the Dyall Hamiltonian in the first-order interacting
space (FOIS, the space consisting of all single and double excitations with respect to the CASCI space). The effective Hamiltonian has the form of a CASCI
Hamiltonian that is dressed with the effect of dynamic correlation
(dynamic correlation dressed, DCD), hence the name for the method.
$E_0^S$ is chosen to be the ground state CASSCF energy for the
respective total spin $S$. Since this choice is worse for excited states
than for the ground state, excitation energies suffer from a \"ground
state bias\".

For the contribution coming from perturbers in which electrons are
excited from two inactive ($ij$) to two virtual ($ab$) orbitals, we use
(when writing the DCD Hamiltonian in a basis of CASCI states) the
alternative expression

$$\langle \Psi_I^{SS} | H^\text{DCD}(ij \rightarrow ab) | \Psi_J^{SS} \rangle = - \delta_{IJ} E_\text{MP2}$$

$$E_\text{MP2} = \sum_{ijab} \frac{(ib|ja)^2 - (ib|ja)(ia|jb) + (ia|jb)^2}{\epsilon_a + \epsilon_b - \epsilon_i - \epsilon_j}$$

Since in this version the $ij\rightarrow ab$ perturber class does not
contribute at all to excitation energies (like it is assumed in the
difference-dedicated configuration interaction method), we call this the
difference-dedicated DCD-CAS(2) method. Since the $ij\rightarrow ab$
class contributes the largest part of the dynamic correlation energy,
this also removes the largest part of the ground state bias. This option
is used as default in DCD-CAS(2) calculations. In order to also remove
the ground state bias from the other perturber classes, we furthermore
apply a perturbative correction to the final energies. At first order
(which is chosen as default), it takes the form

$$\Delta E_I = - \Delta_I \sum_{K \in \text{FOIS} } \frac{\langle \tilde{\Psi}_I | H | \tilde{\Phi}_K\rangle \langle \tilde{\Phi}_K | H | \tilde{\Psi}_I \rangle }{(E_K - E_0)^2}$$

$$\Delta_I = \langle \tilde{\Psi}_I | H | \tilde{\Psi}_I \rangle - E_0$$

for the correction $\Delta E_I$ to the total energy of the $I$th
DCD-CAS(2) root $|\tilde{\Psi}_I\rangle$.

## Treatment of spin-dependent effects

The theory so far is valid for a nonrelativistic or scalar-relativistic
Hamiltonian $H$. If we modify it to a Hamiltonian $H+V$, where $V$
contains effects that are possibly spin-dependent such as spin-orbit coupling (SOC) and spin-spin coupling
(SSC), this leads us to a
theory {cite}`Lang2019` which has a similar form as QDPT with all CAS roots
included. The form of the spin-dependent DCD-CAS(2) effective
Hamiltonian is

$$\langle \Phi_I^{SM} | H^\text{DCD} | \Phi_J^{S'M'}\rangle = \delta_{SS'} \delta_{MM'} H_{IJ}^{\text{DCD},S,\text{corr} } + \langle \Phi_I^{SM} | V | \Phi_J^{S'M'} \rangle.$$

$$\mathbf{H}^{\text{DCD}, S, \text{corr} } = \mathbf{C}^\text{DCD} \mathbf{E} (\mathbf{C}^\text{DCD})^T.$$

In order to construct it, we first need to solve the scalar-relativistic
DCD-CAS(2) problem to construct the matrix
$\mathbf{H}^{\text{DCD},S,\text{corr} }$ from the bias corrected
energies $\mathbf{E}$ and DCD-CAS(2) CI coefficients $\mathbf{C}^\text{DCD}$ and
then calculate the matrix elements of the operators contributing to V in
the basis of CSFs $|\Phi_I^{SM}\rangle$.

Zero field splitting D tensors are extracted using the effective
Hamiltonian technique, i.e. fitting the model Hamiltonian to a
des Cloizeaux effective Hamiltonian that is constructed from the
relativistic states and energies by projection onto the nonrelativistic
multiplet (see section
{ref}`sec:modelchemistries.mrci.soc.zfs` and the reference
{cite}`maurice2009`). There are limitations to this approach if spin orbit
coupling becomes so strong that the relativistic states cannot uniquely
be assigned to a single nonrelativistic spin multiplet.

Hyperfine A-matrices and Zeeman g-matrices for individual Kramers
doublets consisting of states $|\Phi\rangle, |\bar{\Phi}\rangle$
are extracted by comparing the spin Hamiltonians

$$H_\text{Zeeman} = \mu_B \vec B \cdot g \cdot \vec S$$

$$H_\text{HFC} = \sum_A \vec I^A \cdot A^A \cdot \vec S$$

to the matrix representation of the many-electron Zeeman and HFC
operators in the basis of the Kramers doublet. This yields {cite}`Lang2019`

$$\begin{aligned}
  g_{k1} &= 2\Re \langle \bar{\Phi} | L_k + g_e S_k | \Phi \rangle \\
  g_{k2} &= 2\Im \langle \bar{\Phi} | L_k + g_e S_k | \Phi \rangle \\
  g_{k3} &= 2\langle \Phi | L_k + g_e S_k | \Phi \rangle\end{aligned}$$

$$\begin{aligned}
  A_{k1} &= -2\gamma_A \Re \langle \bar{\Phi} | B_k^\text{HFC}(\vec R_A) | \Phi \rangle \\
  A_{k2} &= -2\gamma_A \Im \langle \bar{\Phi} | B_k^\text{HFC}(\vec R_A) | \Phi \rangle \\
  A_{k3} &= -2\gamma_A \langle \Phi | B_k^\text{HFC}(\vec R_A) | \Phi \rangle\end{aligned}$$

where $B_k^\text{HFC}(\vec R_A)$ is the $k$th component of the magnetic
hyperfine field vector at the position of nucleus $A$ and $\gamma_A$ is
the gyromagnetic ratio.

## Simple example

The basic usage is very simple: One just needs a `%casscf` block and the
simple input keyword `!DCD-CAS(2) `. The following example is a
calculation on the LiF molecule. It possesses two singlet states that
can be qualitatively described as ionic (Li$^+$ and F$^-$) and covalent
(neutral Li with electron in 2s orbital and neutral F with hole in $2p_z$
orbital). At distances close to the equilibrium geometry, the ground
state is ionic, while in the dissociation limit the ground state is
neutral. Somewhere in between, there is an avoided crossing of the
adiabatic potential energy curves where the character of the two states
quickly changes (see figure
{numref}`fig:lifavoided` for potential energy curves for this system
at the (QD)NEVPT2 level). At the CASSCF level, the neutral state is
described better than the ionic state, with the result that the latter
is too high in energy and the avoided crossing occurs at a too small
interatomic distance. In the region where the avoided crossing actually
takes place, the CASSCF states are then purely neutral or purely ionic.
DCD-CAS(2) allows for a remixing of the states in the CASCI space under
the effect of dynamic correlation, which will lower the ionic state more
in energy than the neutral one. The input file is as follows:

```{literalinclude} ../../orca_working_input/sample_dcdcas2.inp
:language: orca
```

Since none of the standard guesses (`!PAtom`, `!PModel`, etc.) produces
the correct active orbitals (Li 2s and F $2p_z$), we read them from the
file casorbs.gbw. We also use the `actorbs locorbs` option to preserve
the atomic character of the active orbitals and interpret the states in
terms of neutral and ionic components easier. The following is the state
composition of LiF at an interatomic distance of 5.5 angstrom at the
CASSCF and DCD-CAS(2) levels.

```orca
---------------------------------------------
CAS-SCF STATES FOR BLOCK  1 MULT= 1 NROOTS= 2
---------------------------------------------

ROOT   0:  E=    -106.8043590118 Eh
      0.99395 [     1]: 11
      0.00604 [     2]: 02
ROOT   1:  E=    -106.7485794535 Eh  1.518 eV  12242.2 cm**-1
      0.99396 [     2]: 02
      0.00604 [     1]: 11
```

```orca
---------------------------------------
      DCD-CAS(2) STATES
---------------------------------------

ROOT   0:  E=    -107.0917611937 Eh
      0.60590 [     2]: 02
      0.39410 [     1]: 11
ROOT   1:  E=    -107.0837717163 Eh  0.217 eV   1753.5 cm**-1
      0.60590 [     1]: 11
      0.39410 [     2]: 02
```

One can clearly see that while the CASSCF states are purely neutral
(dominated by CFG `11`) or purely ionic (dominated by CFG `02`), the
DCD-CAS(2) states are mixtures of neutral and ionic contributions. The
calculation indicates that the interatomic distance of 5.5 is in
the avoided crossing region. Note that the energies that are printed
together with the DCD-CAS(2) state composition are the ones that are
obtained from diagonalization of the DCD-CAS(2) dressed Hamiltonian. For
excited states, these energies suffer from what we call *ground state
bias* (see the original paper for a discussion {cite}`PathakLang2017DCDCAS`).
A perturbative correction has been devised to overcome this problem. Our
standard choice is first-order bias correction. The corrected energies
are also printed in the output file and those energies should be used in
production use of the DCD-CAS(2) method:

```orca
---------------------------------------------------------
 BIAS-CORRECTED (ORDER 1) STATE AND TRANSITION ENERGIES
=========================================================
 ROOT     Energy/a.u.    DE/a.u.     DE/eV     DE/cm**-1
=========================================================
   0:  -107.093214435   0.000000     0.000       0.0
   1:  -107.084988306   0.008226     0.224    1805.4
```

:::{Warning}
Note that the computational cost of a DCD-CAS(2) calculation
scales as roughly the 3rd power of the size of the CASCI space. This
makes calculations with active spaces containing more than a few hundred
CSFs very expensive!
:::


## List of keywords

The following keywords can be used in conjunction with the DCD-CAS(2)
method:

```orca
%casscf
  dcdcas true                # Do a DCD-CAS(2) calculation
  diffded true               # Use difference-dedicated DCD-CAS(2) for the 
                             # ij->ab class
  corrorder 1                # Maximum order for the perturbative bias correction
                             # (lower orders come for free)
  dcd_ritrafo false          # Use RI approximation for electron repulsion
                             # integrals

  dcd_soc false              # Relativistic DCD-CAS(2) with spin orbit coupling
  dcd_ssc false              # Relativistic DCD-CAS(2) with direct electronic
                             # spin-spin coupling
  dcd_domagfield 0           # Number of user-specified finite magnetic fields
  dcd_dtensor false          # Calculate an effective Hamiltonian D-tensor
  dcd_nmultd 1               # The number of nonrelativistic multiplets for which 
                             # the D-tensor is calculated
  dcd_gmatrix false          # Calculate an effective Kramers pair Zeeman g-matrix
  dcd_amatrix false          # Calculate an effective Kramers pair Hyperfine
                             # A-matrix
  dcd_kramerspairs 1         # The number of Kramers pairs for which g and/or A
                             # is calculated
  dcd_magnetization false    # Calculate the magnetization of the molecule in an
                             # external magnetic field

  dcd_cascimode false        # Run relativistic calculation in CASCI mode, i.e.
                             # without the dynamic correlation dressing
  dcd_natorbs false          # Calculate natural orbitals for each state and write
                             # them to disk
  dcd_populations false      # Perform population analysis on the DCD-CAS(2) states
end
```

Note that the calculation of SSC requires the definition of an auxiliary
basis set, since it is only implemented in conjunction with RI
integrals. If `dcd_magnetization` is requested, the values for magnetic
flux density and temperature to be used can be specified via the
keywords `MAGTemperatureMIN`, `MAGTemperatureMAX`,
`MAGTemperatureNPoints`, `MAGFieldMIN`, `MAGFieldMAX`, `MAGNpoints` of
the `rel` subblock of the `%casscf` block (see section
{ref}`sec:modelchemistries.mrci.soc.magnet`). If the keyword
`dcd_domagfield` is set to a number different than 0, the magnetic
fields can be entered as a matrix of xyz coordinates (in Gauss), e.g.

```orca
%casscf
  dcdcas true
  ...
  dcd_domagfield 2
  dcd_magneticfields[0] = 10000, 0, 0
  dcd_magneticfields[1] = 0, 10000, 0
end
```

Furthermore, there is the keyword `DCD_EDIAG` that when running the
DCD-CAS(2) code in CASCI mode works analogously to the keyword `EDiag`
in the `soc` subblock of the `%mrci` block (see section
{ref}`sec:modelchemistries.mrci.soc.zfs`). The energies should be entered in atomic units, e.g.

```orca
%casscf
  ...
  dcdcas true
  dcd_cascimode true
  dcd_soc true
  DCD_EDIAG[0] -2220.920028
  DCD_EDIAG[1] -2220.834377
  DCD_EDIAG[2] -2220.835871
  DCD_EDIAG[3] -2220.810290
  DCD_EDIAG[4] -2220.812293
  DCD_EDIAG[5] -2220.756732
end
```
