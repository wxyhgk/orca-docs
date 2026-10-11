```{index} AUTOCI
```

(sec:modelchemistries.autoci)=
# Correlated Methods using Automatic Code Generation (AUTOCI)

The AUTOCI module hosts a number of methods, where their
manual implementation would be tedious or practically
impossible. The module works with all types of reference wave function
available in ORCA, i.e., RHF, ROHF, UHF and [CASSCF](sec:modelchemistries.casscf) and offers CI and
related methods.

All the methods are implemented in
canonical orbital basis and storing all integrals on disk.

(sec:modelchemistries.autoci.introduction)=
## Introduction

All the theories are obtained by the means of automated programming
within the ORCA-AGE (Automated Generator Environment for ORCA).{cite}`krupicka2017ORCA_AGE,lechner2024code` The CI
module reads in the SCF wavefunction and optimizes the coefficient of
the CI expansion. Conceptually, the module is similar to `orca_mdci`,
therefore the input and output do have a lot in common.


(sec:modelchemistries.autoci.available)=
## Basis Usage / List of Features
```{index} CCSDT-n, CC2, CC3, CCSDT, MP3, MP4, MP5
```

The following single-reference methods are currently implemented in the AUTOCI.

| Reference     | Correlation       | Energy        | Gradient      | 
| ------------- | ----------------- | ------------- | ------------- |
| RHF           | CID               | &check;       | &check;       |
| RHF           | CISD              | &check;       | &check;       |
| RHF           | CISDT             | &check;       |               |
| RHF           | CCD               | &check;       | &check;       |
| RHF           | CCSD              | &check;       | &check;       |
| RHF           | CCSD[T]           | &check;       | &check;       |
| RHF           | CCSD(T)           | &check;       | &check;       |
| RHF           | CCSDT             | &check;       |               |
| RHF           | CEPA(0)           | &check;       | &check;       |
| RHF           | CC2               | &check;       |               |
| RHF           | QCISD             | &check;       |               |
| RHF           | MP2               | &check;       | &check;       |
| RHF           | MP3               | &check;       | &check;       |
| RHF           | MP4               | &check;       | &check;       |
| RHF           | MP4(SDQ)          | &check;       | &check;       |
| UHF           | CID               | &check;       | &check;       |
| UHF           | CISD              | &check;       | &check;       |
| UHF           | CISDT             | &check;       | &check;       |
| UHF           | CCD               | &check;       | &check;       |
| UHF           | CCSD              | &check;       | &check;       |
| UHF           | CCSD[T]           | &check;       | &check;       |
| UHF           | CCSD(T)           | &check;       | &check;       |
| UHF           | CCSDT             | &check;       | &check;       |
| UHF           | CCSDTQ            | &check;       |               |
| UHF           | CCSDT-1           | &check;       |               |
| UHF           | CCSDT-2           | &check;       |               |
| UHF           | CCSDT-3           | &check;       |               |
| UHF           | CCSDT-4           | &check;       |               |
| UHF           | CEPA(0)           | &check;       | &check;       |
| UHF           | CC2               | &check;       |               |
| UHF           | CC3               | &check;       |               |
| UHF           | QCISD             | &check;       |               |
| UHF           | MP2               | &check;       | &check;       |
| UHF           | MP3               | &check;       | &check;       |
| UHF           | MP4               | &check;       | &check;       |
| UHF           | MP4(SDQ)          | &check;       | &check;       |
| UHF           | MP5               | &check;       | &check;       |
| ROHF          | CISD              | &check;       |               |

Any AUTOCI single-reference methods can be called from the simple keyword by prepending `AUTOCI-`
to the correlation method, for instance

```orca
! AUTOCI-CCSD
```
The prefix 'AUTOCI' is added to dinstinguish from the handwritten implementations in `orca_mdci`and `orca_mp2`.

:::{warning}
Higher order CC calculations like CCSDT and CCSDTQ have extreme memory requirements in the CC Iterations. For UHF CCSDTQ particularly (computational efford scales as $N^{10}$ !) only systems with few electrons and basis functions are feasible depending on your achitecture.
:::

For a CASSCF reference wavefunction, the prefix is omitted. The following multi-reference methods and their unrelaxed densities are available.

| Reference     | Correlation       | Energy        | Unrelaxed Density |
| ------------- | ----------------- | ------------- | ------------- | 
| CASSCF        | FIC-MRCI          | &check;       |  &check;          |
| CASSCF        | FIC-CEPA(0)     | &check;       |  &check;          |
| CASSCF        | FIC-ACPF        | &check;       |  &check;          |
| CASSCF        | FIC-AQCC        | &check;       |  &check;          |
| CASSCF        | FIC-MRCC          | &check;       |  Linearized       |
| CASSCF        | FIC-DDCI3         | &check;       |  &check;          |
| CASSCF        | FIC-NEVPT2        | &check;       |  &check;          |
| CASSCF        | FIC-NEVPT3        | &check;       |  &check;          |
| CASSCF        | FIC-NEVPT4(SD)    | &check;       |  &check;          |

:::{note}
If a multi-reference method is specified as a simple keyword,
all information about reference spaces, number of roots etc. 
is taken from the CASSCF module that is assumed to be run in advance. 
More refined settings require the `%autoci` block in the input.
:::

(sec:modelchemistries.autoci.gradients)=
## Analytic Nuclear Gradients with AUTOCI

Obtaining accurate geometries is crucial to computing molecular properties
accurately. In order to perform geometry optimisations, the nuclear gradient
is necessary and while this can easily be obtained using numerical finite
difference methods, it is also quite costly. More importantly,
perhaps, is the fact that numeric derivatives tend to become unstable.
Therefore, being able to evaluate analytic gradients is of vital importance.
Using the AGE, a general framework has been built
that supports arbitrary-order CI, CC and MPn nuclear gradients
(and other derivatives).{cite}`lechner2024code`

An example is shown below how to optimise a geometry using AUTOCI's gradients
at the CCSD level of theory

```orca
! RHF cc-pVTZ AUTOCI-CCSD VerytightSCF Opt

%maxcore 10000

*xyz 0 1
...
*
```

The analytic gradients can even be used to perform semi-numerical frequency calculations

```orca
! AUTOCI-CCSD NumFreq
```

Besides nuclear gradients, all other first-order properties available in ORCA are available
for the respective methods, such as dipole/quadrupole moments, hyperfine couplings or quadrupole splittings.
As discussed above, (un)relaxed densities can be requested via

```orca
%autoci
  density relaxed
end
```

For geometry optimisations, both the unrelaxed and relaxed densities are computed automatically and do not need to be requested explicitly.

(sec:modelchemistries.autoci.autociresp)=
## AUTOCI Response Properties via Analytic Derivatives

For single-reference methods (`CCSD` and `CCSD(T)`), some response properties could be calculated via the analytic derivative scheme.

| Response Property         | Reference | Correlation | Orbital Response      |
| ------------------------- | --------- | ----------- | --------------------- |
| Static Polarizabilities*  | RHF       | CCSD        | Unrelaxed / Relaxed   |
|                           | RHF       | CCSD(T)     | Unrelaxed / Relaxed   |
|                           | UHF       | CCSD        | Unrelaxed / Relaxed   |
|                           | UHF       | CCSD(T)     | Unrelaxed / Relaxed   |
| NMR Shielding (GIAO)      | RHF       | CCSD        | Unrelaxed / Relaxed   |
|                           | RHF       | CCSD(T)     | Unrelaxed / Relaxed   |
|                           | UHF       | CCSD        | Unrelaxed / Relaxed   |
|                           | UHF       | CCSD(T)     | Unrelaxed / Relaxed   |
| G-Tensor (GIAO)           | UHF       | CCSD        | Unrelaxed / Relaxed   |
|                           | UHF       | CCSD(T)     | Unrelaxed / Relaxed   |

(* dipole-dipole, dipole-quadrupole, quadrupole-quadrupole)
Note that for NMR shielding and EPR g-Tensor the fully analytic GIAO approach
(see {ref}`sec:spectroscopyproperties.nmr` and {ref}`sec:spectroscopyproperties.epr.gaugeorigin`)
is the default and the common gauge approach (less accurate) is not available.

To calculate these properties, the following quantities need to be computed:
 - Unperturbed CC amplitudes
 - Unperturbed CC $\Lambda$ (Lagrange Multiplier)
 - Unperturbed 1-RDM
 - Unperturbed 2-RDM ($\dagger$)
 - Unperturbed Z-Vector ($\dagger$)
 - Perturbed CC amplitudes 
 - Perturbed CC $\Lambda$ (Lagrange Multiplier)
 - Perturbed 1-RDM
 - Perturbed 2-RDM ($\dagger$)
 - Perturbed Z-Vector ($\dagger$)

Tasks labelled with ($\dagger$) are optional - they are only required for the "relaxed" scheme of
computing response properties. With the "relaxed" scheme, the orbitals are allowed to relax to
external perturbations. (See: [orbital relaxation](sec:modelchemistries.autoci.autociresp.relaxation)

(sec:modelchemistries.autoci.autociresp.unperturbed)=
### Unperturbed Parameters

From CC gradient theory and as stated in the previous [`MDCI` section](sec:modelchemistries.mdci.densities), the CC energy Lagrangian could be written as (denoting the similarity-transformed Hamiltonian as $\bar{H}=e^{-T}H e^{T}$):

$$
L _{\text{CC}} = \langle \Phi_{0}|\bar{H}|\Phi_{0}\rangle
                 + \sum_{\eta}\lambda_{\eta}\langle \Phi_{\eta}|\bar{H}|\Phi_{0}\rangle 
                 + \sum_{ai}f _{ai}z _{ai}
$$

Equivalently, we could also express this Lagrangian in terms of density matrices:

$$
L _{\text{CC}} = \sum_{pq}h _{pq} \frac{\partial L_{\text{CC}}}{\partial h_{pq}} \\
                 + \sum_{pqrs}(pq|rs)\frac{\partial L_{\text{CC}}}{\partial (pq|rs)} \\ 
               = \sum_{pq}h _{pq}D_{pq} + \sum_{pqrs}(pq|rs)d_{pqrs}
$$

in which the one- and two-body reduced density matrices (RDMs) could be decomposed into the amplitude and orbital contributions:

$$
D_{pq} = \gamma_{pq} + z _{pq}\delta_{pa}\delta_{qi} \\
d_{pqrs} = \Gamma^{pr}_{qs} + z_{pq}\sum_{k}\left(\delta_{pa}\delta_{qi}\delta_{rk}\delta_{sk}
                                                  -\delta_{pa}\delta_{qk}\delta_{rk}\delta_{si}\right)
$$

The above are known as the relaxed 1- and 2-RDMs, since the terms involving the $z_{pq}$ arise due to [orbital relaxation](sec:modelchemistries.autoci.autociresp.relaxation).
The CC amplitude contributions (a.k.a. the unrelaxed 1- and 2-RDMs) are defined as:

$$
\gamma_{pq} = \langle \Phi_{0}|(1+\Lambda)e^{-T}E^{p}_{q}e^{T}|\Phi_{0} \rangle \\
\Gamma^{pr}_{qs} = \langle \Phi_{0}|(1+\Lambda)e^{-T}\left(E^{p}_{q}E^{r}_{s}-E^{p}_{s}\delta_{rq}\right)e^{T}|\Phi_{0} \rangle
$$

These quantities depend on the CC amplitudes $t_{\eta}$ and Lagrange multipliers $\lambda_{\eta}$, for which we need to solve the amplitude- and $\Lambda$-equations:

$$
\langle \Phi_{\eta}|\bar{H}| \Phi_{0}\rangle = 0 \\
\langle \Phi_{0}|(1+\Lambda)(\bar{H}-E_{\text{CC}})|\Phi_{\eta}\rangle = 0
$$

(sec:modelchemistries.autoci.autociresp.perturbed)=
### Perturbed Parameters

The well-known Wigner's $2n+1$ rule of perturbation theory states: wavefunction parameters up to 
the $n$-th order are required for the energies at the order of $2n+1$. For non-variational methods
like CC, the Lagrangian approach is employed, resulting in a variational energy functional
(albeit non-Rayleigh-Ritz, thus no guaranteed upper bound), which 
enables the analytic evaluation of derivatives. The $2n+2$ rule of the Lagrange multiplier in such 
Lagrangian functional states: Lagrange multipliers up to the $n$-th order are required for the
energies at the order of $2n+2$.

In practice, and here in `ORCA-AUTOCI` implementation, these two rules (especially the $2n+2$ rule) are not fully exploited. This is due to the consideration of computational efficiency for certain molecular propeties. For example, the general expression for the second derivative of the CC energy,
subject to two external perturbations $x$ and $y$, could be written as:

$$
\frac{\mathrm{d} ^{2}E}{\mathrm{d} x \mathrm{d} y}
= \langle \Phi_{0}|(1+\Lambda)e^{-T}\frac{\partial ^{2}H}{\partial x \partial y}e^{T}|\Phi_{0}\rangle \\
+ \langle \Phi_{0}|(1+\Lambda)\left[e^{-T}\frac{\partial H}{\partial x}e^{T},\frac{\mathrm{d} T}{\mathrm{d} y}\right]|\Phi_{0}\rangle \\
+ \langle \Phi_{0}|(1+\Lambda)\left[e^{-T}\frac{\partial H}{\partial y}e^{T},\frac{\mathrm{d} T}{\mathrm{d} x}\right]|\Phi_{0}\rangle \\
+ \langle \Phi_{0}|(1+\Lambda)\left[\left[e^{-T}H e^{T}, \frac{\mathrm{d} T}{\mathrm{d} x}\right],\frac{\mathrm{d} T}{\mathrm{d} y}\right]|\Phi_{0}\rangle
$$

which is known as the "symmetric" expression, satisfying both the $2n+1$ and $2n+2$ rules.
However, the following "asymmetric" expression might be preferred for mixed derivatives:

$$
\frac{\mathrm{d} ^{2}E}{\mathrm{d} x \mathrm{d} y} \\
= \langle \Phi_{0}|(1+\Lambda)e^{-T}\frac{\partial ^{2}H}{\partial x \partial y}e^{T}|\Phi_{0}\rangle \\
+ \langle \Phi_{0}|(1+\Lambda)\left[e^{-T}\frac{\partial H}{\partial x}e^{T},\frac{\mathrm{d} T}{\mathrm{d} y}\right]|\Phi_{0}\rangle \\
+ \langle \Phi_{0}|\frac{\mathrm{d} \Lambda}{\mathrm{d}y}e ^{-T}\frac{\partial H}{\partial x}e ^{T}|\Phi_{0}\rangle
$$

In this way, we solve the perturbed $T$ and $\Lambda$ equations subject to only a single perturbation. 
For NMR shielding this means we can solve these equations only for the magnetic-field perturbation and
there are $3$ equations for $\mathrm{d} T/\mathrm{d} B_{i}$ and $3$ for $\mathrm{d} \Lambda/\mathrm{d} B_{i}$. If we were to use the first "symmetric" expression, 
although we could save some effort by not having to solve for any perturbed $\Lambda$,
we still need to solve for perturbed $T$, subject to both the magnetic-field perturbation
($3$ equations) and the nuclear magnetic moment perturbation ($3N_{\text{atoms}}$ equations).

To obtain the equations for perturbed $T$ and $\Lambda$, we differentiate the unperturbed
equations, w.r.t. external perturbation $\chi$

$$
  \frac{\partial}{\partial\chi} \langle \Phi_{\eta}|\bar{H}|\Phi_{0}\rangle = 0 \\ 
  \frac{\partial}{\partial\chi} \langle
\Phi_{0}|(1+\Lambda)(\bar{H}-E_{\text{CC}})|\Phi_{\eta}\rangle = 0
$$

Then we build the perturbed 1- and 2-RDMs, by taking derivative of the unperturbed expressions:

$$
 \frac{\partial\gamma_{pq}}{\partial\chi}      = \frac{\partial}{\partial\chi}\langle \Phi_{0}|(1+\Lambda)e^{-T}E^{p}_{q}e^{T}|\Phi_{0} \rangle \\
 \frac{\partial\Gamma^{pr}_{qs}}{\partial\chi} = \frac{\partial}{\partial\chi}\langle \Phi_{0}|(1+\Lambda)e^{-T}\left(E^{p}_{q}E^{r}_{s}-E^{p}_{s}\delta_{rq}\right)e^{T}|\Phi_{0} \rangle
$$

The expressions and relevant modules are produced by the code generator. Note that for the
currently available response properties - polarizabilities, NMR shielding, EPR g-tensors - which
are technically one-particle properties, for which the 2-RDMs do not appear explicitly in the
energy derivative expression, both the unperturbed 2-RDMs and the perturbed 2-RDMs are only needed when [orbital relaxation](sec:modelchemistries.autoci.autociresp.relaxation) needs to be computed.

(sec:modelchemistries.autoci.autociresp.relaxation)=
### Orbital Relaxation
By including the orbital relaxation effect into property calculations, we essentially allow the MO
to respond to external perturbations. This leads to the following parameterization of MO
coeffcients:

$$
\mathbf{C}(\chi) = \mathbf{C}(0) \mathbf{U}(\chi)
$$

then MO derivatives could be written as:

$$
\mathbf{C}^{\chi}\equiv \frac{\partial \mathbf{C}(\chi)}{\partial \chi}
= \mathbf{C}(0) \frac{\partial \mathbf{U}(\chi)}{\partial \chi} \equiv \mathbf{C}
\mathbf{U}^{\chi}
$$

where $\mathbf{U}^{\chi}$ are solutions to the [CPSCF](sec:essentialelements.cpscf) equations.
For unrelaxed calculations the MO coefficients are always $\mathbf{C}(0)$. In relaxed
calculations, the MO response enters relevant CC equations in two ways.

First, as described [above](sec:modelchemistries.autoci.autociresp.perturbed),
for second-order response properties (like polarizabilities, NMR shielding, etc.)
we need to solve the first-order $T$ and $\Lambda$ equations. Within a relaxed scheme,
any derivative integrals (Fock, ERI, etc.) entering the CC equations contain CPSCF contributions.
For example:

$$
\frac{\partial (pq|rs)}{\partial \chi} = \\
\sum_{\mu\nu\kappa\tau}C_{\mu p}C_{\nu q} \frac{\partial (\mu\nu|\kappa\tau)}{\partial \chi}C_{\kappa r}C_{\tau s} \\
+ \sum_{\mu\nu\kappa\tau}C_{\mu p}^{\chi}C_{\nu q}(\mu\nu|\kappa\tau)C_{\kappa r}C_{\tau s} \\
+ \sum_{\mu\nu\kappa\tau}C_{\mu p}C_{\nu q}^{\chi}(\mu\nu|\kappa\tau)C_{\kappa r}C_{\tau s} \\
+ \sum_{\mu\nu\kappa\tau}C_{\mu p}C_{\nu q}(\mu\nu|\kappa\tau)C_{\kappa r}^{\chi}C_{\tau s} \\
+ \sum_{\mu\nu\kappa\tau}C_{\mu p}C_{\nu q}(\mu\nu|\kappa\tau)C_{\kappa r}C_{\tau s}^{\chi}
$$

For unrelaxed calculations the last 4 terms are zero.

Second, to compute the relaxed 1- and 2-RDMs and their derivatives, the $z$-vector contribution
needs to be included. This is a consequence of requiring the CC energy to be invariant to orbital 
rotation, in the presence of external perturbations. This nice trick by Schaefer and Handy allows
gradient to be evaluated without having to solve $3N_{atoms}$ equations for the orbitals. Instead,
only the so-called "$z$-vector" equation needs to be solved. It thus opens a door towards
efficient analytic response property evaluations. The $z$-vector equations are of the same form as
the [CPSCF](sec:essentialelements.cpscf) equations:

$$
\mathbf{A}\mathbf{z} = \mathbf{X}
$$

where the $\mathbf{A}$ matrix is exactly the same as the CPSCF LHS, and the RHS matrix $\mathbf{X}$ is
the orbital gradient of the CC energy functional. For second-order response properties, the
derivatives (subject to each perturbation requested) of this equation also need to be solved.

The discussion of relaxed properties vs unrelaxed ones are quite common. Generally, we believe
that for electric-field dependent properties like polarizabilities, inclusion of orbital relaxation
does not necessarily lead to more accurate values compared with experiments. However it is generally 
regarded essential to include orbital relaxation for magnetic-field dependent properties like NMR and 
EPR parameters.

Finally, it is also worth noting that this orbital relaxtion scheme does not recover the MO response
of using HF orbitals in a CC wavefunction setup, which relies on the orbital-optimized coupled-cluster
(OOCC) methods, as described in the [previous section](sec:modelchemistries.mdci.densities).

(sec:modelchemistries.autoci.autociresp.inputs)=
### Input Options
The input parameters for the wavefunctions are controlled by the [`%autoci`](sec:modelchemistries.autoci.keywords)
block, while the property-related parameters are controlled by respective property blocks, 
like [`elprop`](sec:spectroscopyproperties.properties.elprop.keywords) and 
[`eprnmr`](sec:spectroscopyproperties.properties.eprnmr).
Some useful options are gathered below.

```orca
%autoci
    citype
        CCSD(T)
        CCSD
    STol      1e-06 # residue convergence tolerance
    MaxIter   50    # maximum number of iterations
    MaxDIIS   5     # depth of the DIIS memory
    density         # need at least unrelaxed density (see details below)
        unrelaxed
        relaxed
end

%method 
  Z_Tol       1e-8  # Convergence tolerance for the CP-SCF equations
                    # default if 3e-6 for ExtremeSCF
                    # however, we recommend at least one level tighter than %autoci STol
end

%elprop
    polar         true    # dipole-dipole polarizability
    polardipquad  true    # dipole-quadrupole polarizability
    polarquadquad true    # quadrupole-quadrupole polarizability
    Tol           1e-8    # Alia, see: %method Z_Tol
end

%eprnmr
    gtensor       true    # calculate the g-tensor
    NMRShielding  1       # for chosen nuclei - specified with the Nuclei keyword
                  2       # for all nuclei, equivalent to the 'NMR' simple input
    Tol           1e-8    # Alia, see: %method Z_Tol
end
```

Output files:
Calculation outputs generated from AutoCI-Response modules are re-directed into 
separate outputfiles, with the names `basename.autociresp_efield`, `basename.autociresp_bfield`, etc.

(sec:modelchemistries.autoci.autociresp.examples)=
### Input Examples

Highly accurate NMR shielding for HF:
```
! AUTOCI-CCSD(T) NMR pcsseg-4 cc-pwcv5z/c ExtremeSCF

%autoci
  STol 1e-10
  density relaxed
end

%eprnmr
  Tol 1e-12
end

%coords
  CTyp xyz
  Charge 0
  Mult 1
  Units bohrs
  coords
    H  0.00000000  0.00000000  1.64411926
    F  0.00000000  0.00000000 -0.08721704
  end
end
```

G-Tensor for NH radical, with the SOC operator being the effective nuclear charge (see [`SOCoptions`](sec:spectroscopyproperties.soc)):
```
! UHF cc-pVTZ G-Tensor ExtremeSCF AUTOCI-CCSD(T)
! NoFrozenCore Bohrs

%rel 
  SOCType 1
  Zeff[1] = 1.0   # H
  Zeff[7] = 4.55  # N
end

%eprnmr
  Tol 1e-10
end

%autoci
  STol 1e-9
  Density relaxed
end

# NH radical
* xyz 0 3
N 0.0  0.0  0.0
H 0.0  0.0  1.957794
*  
```

By changing the `%rel` block to the following we can do the same calculation, using a more accurate
SOC description (SOMF):
```
%rel 
  # these two are defaults
  SOCType 3
  SOCFlags 1,4,3,0
end
```

(sec:modelchemistries.autoci.ficmrci)=
## Fully Internally Contracted MRCI (FIC-MRCI)
```{index} FIC-MRCI
```

Starting point for any multireference approach is a reference
wavefunction that consists of multiple determinants or configurations
state functions (CSFs). In many instances this is the complete active
space SCF (CASSCF) wavefunction. In the uncontracted MRCI approach, as
implemented in the `orca_mrci` module, the wavefunction is expanded in
terms of excited CSFs that are generated by considering excitations with
respect to all reference CSFs. The methodology scales with the number of
reference CSFs and hence is restricted to small reference spaces.
Moreover, the configuration driven algorithm used in `orca_mrci` keeps
all integrals in memory, which further limits the overall size of the
molecule.

Internal contraction as proposed by Meyer and Siegbahn avoids these
bottlenecks {cite}`siegbahn_direct_1980,meyer_configuration_1977`. Here,
excited CSFs are generated by applying the excitation operator to the
reference wavefunction as whole. The fully internally contracted MRCI
(FIC-MRCI) uses the same internal contraction scheme as
the FIC-NEVPT2 (aka PC-NEVPT2). The entire methodology as well as a
comparison with the conventional uncontracted MRCI is reported in our
article {cite}`sivalingam_comparison_2016`. The CEPA0, ACPF and AQCC variants
are straight forward adoptions {cite}`saitowfic`. The residue of the FIC-MRCI
ansatz

$$
R_K=\braket{\Phi^{pr}_{qs}| \hat H - E^\text{CAS}-\lambda E_{c}|\Psi^\text{FIC} },
$$ (residualfic)

is modified by the factor

$$\lambda = \left\{\begin{array}{cc}
1  & \text{MRCI} \\
0  & \text{CEPA0} \\
\frac{2}{N_{e} }  & \text{ACPF}\\
\frac{1-(N_e-3)(N_e-2) }{N_e\cdot(N_e-1) } & \text{AQCC}
\end{array}
\right.$$

Here, $E_{c}$ is the correlation energy and $\Phi^{pr}_{qs}$ denote the
internally contracted CSF that arise from the action of the spin-traced
excitation operators on the CAS-CI reference wave function

$$\Phi^{pr}_{qs}=E^p_qE^r_s \ket{\Psi^\text{CAS} }.$$

In case of ACPF and AQCC, the $\lambda$ factor explicitly depends on the
number of correlated electrons ($N_{e}$).

The general input structure is like that of the CASSCF module, e.g., the
following example input reads an arbitrary set of orbitals and starts
the FIC-MRCI calculation. The internal contracted formalism requires
CAS-CI reduced densities up to fourth-order, which can be expensive to
construct. By default, the density construction is sped up using the
prescreening (PS) approximation reported in Section
{ref}`sec:modelchemistries.nevpt2`.{cite}`guo_nevpt2_approx1_2021`

```orca
!def2-tzvp moread allowrhf noiter nofrozencore
%moinp "start.gbw"  # could be from CASSCF

%autoci
citype   FIC-MRCI      # Fully internally contracted MRCI (singles, doubles)
         FIC-CEPA(0)   # CEPA0 version of FIC-MRCI
         FIC-ACPF      # ACPF  version of FIC-MRCI
         FIC-AQCC      # AQCC  version of FIC-MRCI
         FIC-DDCI3     # FIC-MRCI without the IJAB excitation

# CAS-CI reference wavefunction
nel 2
norb 2
mult 1,3
nroots 3,1

nthresh 1e-6  # removal of linear dependencies in the IC-CSFs
D3TPre        1e-14 # default density truncation of the 3-RDM
D4TPre        1e-14 # default density truncation of the 4-RDM

# Davidson correction for the FIC-MRCI
DavidsonOpt 0  # none (default)
            1  # Davidson correction
end
```

Currently, the program is capable of computing total energies and
vertical excitation energies. More features will be available with
future releases.

### Input Example

```orca
# potentially "!FIC-CEPA(0)" omitting the %autoci block.
!def2-SVP  

# get CASSCF orbitals and define states
%casscf
  nel 8
  norb 6
  mult 3
  nroots 1
end

# run FIC-CEPA(0)
%autoci
  # CAS settings are automatically copied from the %casscf block, if 
  # not defined in %autoci
 
  citype FIC-CEPA(0)
end

# O2 molecule
*xyz 0 3
O 0 0 0 
O 0 0 1.28
*
```


(sec:modelchemistries.autoci.ficmrcc2)=
## Fully Internally Contracted MRCC (FIC-MRCC)
```{index} FIC-MRCC
```

Several approaches have been taken towards extending CC theory to work with
genuinely multiconfigurational reference wave functions {cite}`Lyakh2012`,
yet none of these approaches has found widespread adoption. As of 2011,
the internally contracted MRCC theory has had a revival, with a rigorous
theoretical investigation of several approximations that also proved its
orbital invariance {cite}`Evangelista2011` and a first report of a
polynomial-scaling code obtained through automatic equation
generation {cite}`Hanauer2011`.

Our implementation in ORCA is akin to the previously published
formulations in Refs. {cite}`Evangelista2011,Hanauer2011`, although
everything is formulated rigorously in terms of the spin-free excitation
operators
$\hat E_q^p = \hat a^{p\alpha }\hat a_{q\alpha } + \hat a^{p\beta }\hat a_{q\beta }$,
using an improved version of the ORCA-AGE code generator.{cite}`lechner2024code` To begin
with, the *ansatz* for the wave function is

$$\begin{aligned}
|\Psi \rangle  = \text{e}^{\hat T}|0\rangle \;, \end{aligned}$$ (eq:MRCC-ansatz)

where $|0\rangle$ denotes a zeroth order CASSCF reference wave function
and the cluster operator can be written as (Einstein's summation
convention implied)

$$
  \hat T = \frac{1}{2}t_{ab}^{ij}\hat E_i^a\hat E_j^b + t_{ab}^{it}\hat E_i^a\hat E_t^b + \frac{1}{2}t_{ab}^{tu}\hat E_t^a\hat E_u^b + t_{at}^{ij}\hat E_i^a\hat E_j^t + t_{au}^{it}\hat E_i^a\hat E_t^u \\
    + t_{ua}^{it}\hat E_i^u\hat E_t^a + t_{av}^{tu}\hat E_t^a\hat E_u^v + \frac{1}{2} t_{tu}^{ij}\hat E_i^t\hat E_j^u + t_{uv}^{it}\hat E_i^u\hat E_t^v\;.
$$

Note that we do not use normal order in the cluster operator.

Inserting the *ansatz* from Eq. {eq}`eq:MRCC-ansatz` into the Schrödinger equation and
pre-multiplying with the inverse exponential, we obtain the similarity
transformed Hamiltonian and the energy expression,

$$\begin{aligned}
    \bar H|0\rangle  = \text{e}^{ - \hat T}\hat H\text{e}^{\hat T}|0\rangle  = E|0\rangle \;.\end{aligned}$$

In our code, the similarity-transformed Hamiltonian is truncated after
the quadratic terms since that approximation has been found to only have
minor impact on the accuracy of the method {cite}`Evangelista2011`,

$$\begin{aligned}
    \bar H \approx \hat H + [\hat H,\hat T] + \frac{1}{2}[[\hat H,\hat T],\hat T]\;.\end{aligned}$$

The residual conditions are subsequently obtained by projecting with
contravariant excited functions $\langle \tilde \Phi _P|$ onto the
Schrödinger equation,

$$\begin{aligned}
{ r_P} = \langle \tilde \Phi _P|\bar H|0\rangle \;.\end{aligned}$$

For a definition of the contravariant projection functions, we refer to
Ref. {cite}`sivalingam_comparison_2016` since this FIC-MRCC implementation
uses the same contravariant functions as the published FIC-MRCI
implementation. Despite using contravariant projection functions, this
is not sufficient to remove all linear dependencies from the set of
projection functions $\{ \tilde\Phi_P \}$, i.e. the metric matrix

$$\begin{aligned}
    S_{PQ} &= \braket{\tilde\Phi_P | \tilde\Phi_Q} \ne \delta_{PQ}\end{aligned}$$

has off-diagonal elements *within* excitation classes and between
classes with the same number of inactive and virtual indices (ITAU and
ITUA). Hence, the set of projection functions needs to be
orthonormalized, which is achieved with Löwdin's canonic
orthogonalization in the AUTOCI module.[^1]

(sec:autoci.ficmrcc.example.detailed)=
### Input Example

The FIC-MRCC module can be started by specifying the `CIType` keyword in
the `%autoci` block or by adding `FIC-MRCC` to the simple input line of
an ORCA input file. The following example computes the singlet ground
state energy of four hydrogen atoms arranged as a square with a side
length of $2 a_0$, which is commonly known as the H4
model {cite}`Jankowski1980`.

```orcainput
! cc-pVTZ Bohrs  # it is possible to add the `FIC-MRCC' keyword here
                 # and omit the %autoci block below

%maxcore 10000

# get CASSCF orbitals and define states.
%casscf
  nel 2
  norb 2
  mult 1
  nroots 1
end

# run FIC-MRCC
%autoci  
  # CAS settings are automatically copied from the %casscf block, if 
  # not defined in %autoci
  citype fic-mrcc
  
  # optional parameters
  nthresh 1e-6        # default removal of linear dependencies in the IC-CSFs
  D3TPre        1e-14 # default density truncation of the 3-RDM
  D4TPre        1e-14 # default density truncation of the 4-RDM
  D5TPre        1e-14 # default density truncation of the 5-RDM
  Density  linearized  # compute the linearized density (not default).
end

* int 0 1
  H 0 0 0 0.0  0.0 0.0
  H 1 0 0 2.0  0.0 0.0
  H 2 1 0 2.0 90.0 0.0
  H 1 2 3 2.0 90.0 0.0
*
```

In this example, ORCA will first run a state-specific CASSCF
calculation, and then immediately continue with the fic-MRCC calculation
on top of the CASSCF solution from the first step. It is, however, not
required to always run a CASSCF calculation before the `autoci` module.
Any ORCA `gbw/mp2nat/…` file is accepted through `%moinp`, although that
route requires the user to specify the active space in the `autoci`
block. `autoci` will then compute a CASCI solution with the provided
input orbitals and use that information to drive the correlated
calculations.

Please be aware that FIC-MRCC is a very extensive theory, which leads to
long run times. The computational effort depends mainly on the number of
orbitals, the number of total electrons and the size of the active
space. On modestly modern hardware, calculations of $\sim 300$ orbitals
with a CAS(2,2) should be readily achievable. For larger active spaces,
such as a CAS(6,6), calculations with a total of $\sim 200$ orbitals
will also complete within a day.

(sec:modelchemistries.autoci.ficnevpt)=
## Fully Internally Contracted NEVPT (FIC-NEVPT4(SD)/FIC-NEVPT3/FIC-NEVPT2)
```{index} FIC-NEVPT
```

Perturbation theory is a cost-effective alternative to the previously mentioned FIC-MRCI and FIC-MRCC methods. 
Most often, a reasonable description of electron correlation is already achieved at the second order of the expansion. 
The CASSCF module features an efficient implementation of the second-order methods, that are able to tackle large molecules 
and active spaces. For more details and references on the second-order variants, we refer to the dedicated 
section {ref}`sec:modelchemistries.nevpt2`.\
In the following section, the focus is on higher orders of the n-electron valence state perturbation theory (NEVPT), 
that are available within the AUTOCI framework. Here, all integrals are computed and kept on disk, which limits the application
to approximately 700 atomic orbitals (AOs). The appearance of higher-order reduced density matrices is a common feature of 
internally contracted methods. 
Like FIC-NEVPT2, the FIC-NEVPT3 and FIC-NEVPT4(SD) require at most the fourth-order reduced density matrix. Its computation 
can be accelerated with the prescreening method discussed in section
 {ref}`sec:modelchemistries.nevpt2`.{cite}`guo_nevpt2_approx1_2021,guo_nevpt2_approx2_2021`
In terms of computation time, the FIC-NEVPT4(SD) is as expensive as FIC-NEVPT3 or a single iteration of the FIC-MRCI method.

(sec:modelchemistries.autoci.ficnevpt.nevpt3)=
### FIC-NEVPT3
The FIC-NEVPT3 methodlogy is desribed in detail by Angeli et al.{cite}`angeli_nevpt3` With the first order wave function $\Psi^{(1)}$, the third order energy is given by the expression

$$E^{(3)}=\langle \Psi^{(1)}|V|\Psi^{(1)} \rangle.$$

(sec:modelchemistries.autoci.ficnevpt.nevpt4)=
### FIC-NEVPT4(SD)
The fourth-order perturbation theory requires the second wave function, which, in principle, involves triple and quadruple
 excitation defining the second-order interacting space. The inclusion of the latter is computationally demanding. 
In the following we report an approximate solution, coined FIC-NEVPT4(SD), which is restricted to the first-order 
interacting space - the single and double excitations with respect to the reference wave function. This method is reported and analyzed in more detail by Kempfer et al.{cite}`kempfer_nevpt4sd` 
Denoting the second order wave function with $\Psi^{(2)}$, the fourth order energy is readily expressed as 

$$E^{(4)} = \langle\Psi^{(1)}|V|\Psi^{(2)}\rangle - E^{(2)}\langle\Psi^{(1)}|\Psi^{(1)}\rangle.$$

The second contribution in the expression above, $E^{(2)}\langle\Psi^{(1)}|\Psi^{(1)}\rangle$, is a renormalization term. As discussed in the paper,{cite}`kempfer_nevpt4sd` the renormalization term is dropped (default) as it destroys the size consistancy in the absence of the exact quadruple excitations.


(sec:modelchemistries.autoci.ficnevpt.input)=
### Input Example

```orcainput
# potentially "!FIC-NEVPT4(SD)"/"!FIC-NEVPT3" instead of the %autoci block.
!def2-tzvp 

# get CASSCF orbitals and define the states
%casscf
    nel 8
    norb 6
    mult 3
    nroots 1
end


# run NEVPT4(SD)
%autoci
# CAS settings are automatically copied from the %casscf block, if 
# not defined in %autoci

 citype fic-nevpt4(sd)

# optional parameters
nthresh 1e-6        # default removal of linear dependencies in the IC-CSFs
D3TPre        1e-14 # default density truncation of the 3-RDM
D4TPre        1e-14 # default density truncation of the 4-RDM

Density  Unrelaxed  # compute the unrelaxed density (not default).
end

# O2 molecule
* xyz 0 3
O 0 0 0
O 0 0 1.28
*
```
## FIC Ansatz: Unrelaxed Densities and Natural Orbitals
The FIC-NEVPT4(SD), the FIC-MRCC and the FIC-MRCI variants have a common set excitation parameters in their wavefunction. For these methods, 
(linearized) unrelaxed densities are available (`density unrelaxed`). With `!KeepDens` the densities are stored in the density 
container (**.densities** file on disk), which can be read with the [`orca_plot` program](sec:utilities.plot). 
The name of the densities reflect its multiplicity, root count and the actual method. Below is an example snippet of
the "orca_plot jobname.densities" call:
```
---------------------
List of density names
---------------------

Index:                                                   Name of Density
------------------------------------------------------------------------
    0:                                                      jobname.scfp
    1:                                                      jobname.scfr
    2:                                         Tdens-CAS.mult.3.root.0.p
    3:                                         Tdens-CAS.mult.3.root.1.p
    4:                                         Tdens-CAS.mult.3.root.2.p
    5:                                         Tdens-CAS.mult.3.root.0.r
    6:                                         Tdens-CAS.mult.3.root.1.r
    7:                                         Tdens-CAS.mult.3.root.2.r
    8:                     jobname.mult.3.root.0.FIC-NEVPT4(SD).autoci.p
    9:                     jobname.mult.3.root.1.FIC-NEVPT4(SD).autoci.p
   10:                     jobname.mult.3.root.2.FIC-NEVPT4(SD).autoci.p
```
Here, the densities 8-10 are unrelaxed densities of the FIC-NEVPT4(SD) method for the first three triplet roots.
With the unrelaxed densities, natural orbitals (`natorbs true`) can be generated. The resulting .gbw files ending with (.nat) 
can be used to carry out further analysis, e.g. using the [MultiWFN program](https://pubs.aip.org/aip/jcp/article/161/8/082503/3309709/A-comprehensive-electron-wavefunction-analysis).


```orca
!FIC-NEVPT4(sd)
...
%autoci
  Density  Unrelaxed  # compute the unrelaxed density
  natorbs true        # generate natural orbitals
end
```
(sec:modelchemistries.autoci.keywords)=
## Keywords
```{index} AUTOCI Keywords
```

:::{raw} latex
\begingroup
\footnotesize
:::
(tab:modelchemistries.autoci.keywords.simple)=
:::{table} Simple input keywords for AUTOCI methods.
:class: footnotesize
| Keyword             | Description                                                                                   |
|:--------------------|:----------------------------------------------------------------------------------------------|
| `AUTOCI-<method>`   | Activate single-reference correlation module from AUTOCI. Disables MDCI.                      |
| `FIC-MRCI`          |
| `FIC-CEPA(0)`     |
| `FIC-ACPF`        |
| `FIC-AQCC`        |
| `FIC-DDCI3`         |
| `FIC-MRCC`          |
| `FIC-NEVPT2`        |
| `FIC-NEVPT3`        |
| `FIC-NEVPT4(SD)`    |
:::
:::{raw} latex
\endgroup
:::

:::{raw} latex
\begingroup
\footnotesize
:::
:::{tabularcolumns} \Y{0.2}\Y{0.3}\Y{0.5}
:::
(tab:modelchemistries.autoci.keywords.block)=
:::{flat-table} `%autoci` block input keywords AUTOCI methods.
:header-rows: 1
:class: longtable
:class: footnotesize
* - Keyword
  - Options
  - Description
* - {rspan}`29` `CIType`
  - `CID`
  - {rspan}`29` Correlation method
* - `CISD`
* - `CISDT`
* - `CCD`
* - `CCSD`
* - `CCSDT`
* - `CEPA(0)`
* - `QCISD`
* - `CC2`
* - `CC3`
* - `CCSD[T]`
* - `CCSD(T)`
* - `CCSDT-1`
* - `CCSDT-2`
* - `CCSDT-3`
* - `CCSDT-4`
* - `FIC-MRCI`
* - `FIC-CEPA(0)`
* - `FIC-ACPF`
* - `FIC-AQCC`
* - `FIC-DDCI3`
* - `FIC-MRCC`
* - `FIC-NEVPT2`
* - `FIC-NEVPT3`
* - `FIC-NEVPT4(SD)`
* - `MP2`
* - `MP3`
* - `MP4(SDQ)`
* - `MP4`
* - `MP5`
* - `STol`
  - 1e-6
  - Residue convergence tolerance
* - `LevelShift`
  - 0.2
  - LevelShift in the DIIS update / denominators
* - `MaxIter`
  - 50
  - Maximum number of iterations
* - `MaxDiis`
  - 5
  - Depth of the DIIS memory
* - `DIISStartIter`
  - 2
  - Apply DIIS starting at iteration 1 (counting starts with 0).
* - `ExcludeHigherExcDIIS`
  - `false`
  - Exclude triples and higher excitations from DIIS procedure
* - `NEl`
  - 6
  - Number of active electrons (CAS only)
* - `NOrb`
  - 7
  - Number of active orbitals (CAS only)
* - `Mult`
  - 1
  - Requested multiplicity block (CAS only)
* - `NRoots`
  - 1
  - Number of roots for mult block (CAS only)
* - `Irrep`
  - 0
  - Requested irrep for mult block (CAS only)
* - `NThresh`
  - 1e-6
  - Threshold for lin. dependencies in the IC-CSFs basis (CAS only)
* - `D3TPre`
  - 1e-14
  - Density truncation in D3 (CAS only)
* - `D4TPre`
  - 1e-14
  - Density truncation in D4 (CAS only)
* - `PrintLevel`
  - 3
  - Amount of printing (1-7)
* - {rspan}`1` `TrafoType`
  - `NoRI`
  - {rspan}`1` Type of integral transformation
* - `RITrafo`
* - `KeepInts`
  - `false`
  - Keep the transformed integrals on disk
* - `UseOldInts`
  - `false`
  - Use the transformed integrals found on disk
* - `RunROHFasUHF`
  - `false`
  - Invokes AUTOCI UHF modules with orbitals from ROHF calculation
* - {rspan}`3` `Density`
  - `none`
  - {rspan}`3` Type of 1-body density requested
* - `linearized`
* - `unrelaxed`
* - `relaxed`
* - {rspan}`3` `Density2`
  - `none`
  - {rspan}`3` Type of 2-body density requested
* - `linearized`
* - `unrelaxed`
* - `relaxed`
* - `NatOrbs`
  - `false`
  - Generate natural orbitals (not available for all methods)
:::
:::{raw} latex
\endgroup
:::

N.B. For a ROHF reference, only CISD calculations can be performed in
the current version. However, it is possible to run UHF calculations with an ROHF
reference by setting the `RunROHFasUHF` flag to true. Note that this only makes
sense when the reference is indeed ROHF, e.g. (calculating the isotropic part of the
HFC at CCSD level, running AutoCI UHF CCSD module, with orbitals obtained from the
ROHF SCF calculation):

```orcainput
! ROHF def2-svp tightscf pmodel AUTOCI-CCSD

%autoci
    RunROHFasUHF true
end

* xyz 0 2
Cu  0.0  0.0  0.0
*

%eprnmr nuclei = all Cu {aiso} end
```

If one wishes to experiment with the module itself and the reference
wavefunction stays constant, it is possible to store the transformed MO
integrals on disk (`keepints`) and reuse them (`useoldints`). The
program checks only whether the dimension of the integrals on disk match
the problem actually solved, i.e. the user is responsible for valid
data.


[^1]: This is similar to scheme A from Ref. {cite}`Hanauer2011`.
