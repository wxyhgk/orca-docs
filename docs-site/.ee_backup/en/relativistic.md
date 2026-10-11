<a id="sec:essentialelements.relativistic"></a>
# Relativistic Calculations

ORCA features three different approximations to cover relativistic effects:

1. The „Exact 2 component“ ([X2C](sec:essentialelements.relativistic.x2c)) Hamiltonian
2. The Douglas-Kroll-Hess ([DKH](sec:essentialelements.relativistic.dkh)) Hamiltonian to second order 
3. The 0th order regular approximation ([ZORA](sec:essentialelements.relativistic.regularapprox)) with a model potential

Earlier versions of ORCA offered a number of additional approximations, which are no longer supported.

The main relativistic Hamiltonian that will be pursued in further development is the X2C Hamiltonian. 
Of the three alternatives, we believe that X2C has the best feature set and we recommend to all of our users to preferentially use this method. 

All three relativistic model Hamiltonians are implemented for scalar relativistic energy calculations 
and these are carried through consistently through the entire program. 
Scalar relativity shows up as an additional effective potential that is added to the one-electron matrix. 
Scalar relativistic corrections to the two-electron interaction are not available in ORCA. 
Furthermore, self-consistent field calculations (HF, DFT, CASSCF) with inclusion of spin-orbit-coupling (SOC) 
are also not available in ORCA but we will not exclude the possibility to add this feature in a future version of the program. 

<a id="sec:essentialelements.relativistic.basic"></a>
## Basic Usage

The relativistic methods in ORCA are implemented in a fairly
straightforward way but do require some caution from the user. 
The basic options are available via simple input keywords 
and finer control is possible through the `%rel` block --
see [sec:essentialelements.relativistic.keywords](#sec:essentialelements.relativistic.keywords) for a full list of keywords.
There are also settings specific to each Hamiltonian -- 
these are explained in the respective section below.

The following three (mutually exclusive) input lines request, respectively:
- a TPSS optimization with the ZORA Hamiltonian, 
  together with the [relativistically recontracted `ZORA-def2-TZVP`](sec:essentialelements.basisset.builtin.rel.def2) basis set 
  and the `SARC/J` [auxiliary basis set](sec:essentialelements.basisset.aux.auxj);
- a DLPNO-CCSD(T) energy calculation with the second order DKH Hamiltonian with,
  together with a matching [correlation-consistent basis set](sec:essentialelements.basisset.builtin.rel.cc)
  and suitable [`AuxC`](sec:essentialelements.basisset.aux.auxc);
- a double-hybrid DFT NMR calculation with the X2C Hamiltonian 
  and [appropriate basis sets](sec:essentialelements.basisset.builtin.rel.karlsruhex2c).

```orca
! TPSS Opt ZORA ZORA-def2-TZVP SARC/J
# or
! DLPNO-CCSD(T) DKH cc-pVTZ-DK cc-pVTZ/C
# or
! DSD-PBEP86/2013 NMR X2C x2c-TZVPall-s x2c/J
```

See [sec:essentialelements.relativistic.basissets](#sec:essentialelements.relativistic.basissets) for an explanation 
of the basis set requirements in relativistic calculations 
and [sec:essentialelements.basisset.builtin.rel](#sec:essentialelements.basisset.builtin.rel) for a list of available basis sets.

!!! warning
    - Older versions of ORCA made extensive use of automatic basis set substitution and aliasing 
      when the use of the DKH or ZORA Hamiltonians was detected. 
      This is no longer the case! 
      Relativistic versions of basis sets now have to be requested explicitly with the appropriate prefix. 
      SARC basis sets also have to be requested explicitly for elements beyond Kr.
    - Geometry optimizations with DKH and ZORA (but not X2C) automatically use the
      [one-center approximation](sec:essentialelements.relativistic.hamiltonian.1c).
      When computing relative energies, do not mix energies from single-point calculations 
      without the one-center approximation
      with those from geometry optimizations that do make use of this feature.

<a id="sec:essentialelements.relativistic.basic.props"></a>
### Scalar-Relativistic Gradients and Properties

Of the three model Hamiltonians, only X2C features analytic gradients. 
Hence, for geometry optimizations this is also the preferred method. 
For DKH and ZORA, the program automatically switches to the 
[one-center approximation](sec:essentialelements.relativistic.hamiltonian.1c).
This requires some attention by the users since final single point energies obtained 
with the one-center approximation are inconsistent with energies obtained without it. 
The one-center approximation is usually of sufficient accuracy but we have observed cases 
in actual applications where it leads to clearly wrong geometries. 
Hence, we strongly recommend to use the X2C Hamiltonian 
(or even an ECP-based calculation) in this realm.

If relativistic calculations are used for molecular properties there is a potential mismatch 
between non-relativistically calculated property integrals and the relativistic Hamiltonian. 
The procedure to remove these inconsistencies is referred to as "picture change". 
It is controlled by the keyword `PictureChange` in `%rel` and is activated by default in most calculations.

```orca
%rel 
  FiniteNuc     true   # Invokes the Gaussian finite nucleus model.
  PictureChange 1 or 2 # First or second order picture change effects.
                       # Second order is potentially more accurate and more expensive.
end
```

Picture change effects are implemented for DKH and X2C and to some extent also for ZORA.
However, they are not implemented for all properties that ORCA can calculate. 
Please pay attention to the output of the property integral and property programs. 
Both programs will explicitly state which picture change effects are included in the molecular integrals. 
For more details, see [sec:essentialelements.relativistic.picturechange](#sec:essentialelements.relativistic.picturechange).
The example above also invokes the finite nucleus model -- 
see [sec:essentialelements.relativistic.finnuc](#sec:essentialelements.relativistic.finnuc).

<a id="sec:essentialelements.relativistic.hamiltonian"></a>
## Approximate Relativistic Hamiltonians

In the relativistic domain, calculations are based on the one-electron,
stationary Dirac equation in atomic units (rest mass subtracted)

$$

h_{D} \Psi =\left({ \left({ \beta -1} \right)c^{2}+c \boldsymbol\alpha \cdot \boldsymbol p +V} \right)\Psi =E\Psi .\qquad \text{(eqn:rel-h-dirac)}

$$

The spinor $\Psi$ can be decomposed in its so-called large and small
components

$$

\Psi =
\begin{pmatrix}
\Psi_L \\
\Psi_S
\end{pmatrix}\qquad \text{(eqn:rel-spinorLS)}

$$

These are obviously coupled through the Dirac equation. More precisely,
upon solving for $\Psi_{S}$, the following relation is obtained:

$$

\Psi_{S} =\frac{1}{2c}\left(1+\frac{E-V}{2c^{2} } \right)^{-1}\boldsymbol\sigma\cdot\boldsymbol p \Psi_{L} =R\Psi_{L}\qquad \text{(eqn:exact-relativistic)}

$$

Through the unitary transformation

$$

U=
\begin{pmatrix}
\Omega_+ & - R^+\Omega \\
R\Omega_+ & \Omega_-
\end{pmatrix}

$$ 
with

$$

\Omega_{+} =\frac{1}{\sqrt{1+R^{+}R} },\Omega_{-} =\frac{1}{\sqrt{ 1+RR^{+} } }

$$

the Hamiltonian can be brought into block-diagonal form

$$

U^{+}h_{D} U=
\begin{pmatrix}
\tilde h_{++} & 0 \\
0 & \tilde h_{--}
\end{pmatrix}\qquad \text{(eqn:rel-unitary-decoupling)}

$$

The (electronic) large component thus has to satisfy the following
relation

$$

h_{++} \Psi_{L} =\Omega_{+} \left({ h_{++} +h_{\pm } R+R^{+}\left({ h_{\mp
} +h_{--} R} \right)} \right)\Omega_{+} \Psi_{L} =E_{+} \Psi_{L} .\qquad \text{(eqn:exact-relativistic-2c)}

$$

The approximate relativistic schemes implemented in ORCA (DKH and ZORA)
use different methods to substitute the exact relation
[Eq](#eqn:exact-relativistic-2c) with approximate ones,
while the X2C formalism solves the model one-electron problem exactly.

<a id="sec:essentialelements.relativistic.hamiltonian.1c"></a>
### One-Center Approximation

In the one-center approximation, which can be applied to any of the 
DKH, ZORA, or X2C methods, the model potential $V$ in [Eq](#eqn:rel-h-dirac)
only contains one-center terms, i.e. interactions with other atoms are ignored.
This has several benefits:
- The unitary decoupling transformation [Eq](#eqn:rel-unitary-decoupling)
  only needs to be solved for each atom type, within the atomic basis, 
  not for the whole system.
- There are no gauge noninvariance errors in ZORA or IORA.
- Most importantly, there are no 
  [picture-change effects](sec:essentialelements.relativistic.picturechange)
  for geometric perturbations (i.e. gradients/Hessians),
  because the relativistic correction is independent of the molecular geometry.
  Thus, all relativistic methods can be used for geometry optimizations
  and frequency calculations at negligible computational effort,
  relative to the non-relativistic calculation.

Several papers in the literature show that this approximation 
is fairly accurate for the calculation of structural parameters and vibrational frequencies.
Thus, it is enabled by default for DKH and ZORA calculations
that require analytic gradients or Hessians,
and indeed such calculations are not implemented without it
(although fully numerical gradients/Hessians are available).
For X2C, picture-change corrections for geometric perturbations are implemented,
so the one-center approximation is not enabled by default.
The approximation can be controlled explicitly via the simple keywords
`!Rel1C` (on) and `!RelFull` (off), or the `OneCenter` keyword in the `%rel` block.

!!! warning
    Energies obtained with and without the one-center approximation not comparable!

<a id="sec:essentialelements.relativistic.regularapprox"></a>
## The Regular Approximation

In the regular approximation,
[Eq](#eqn:exact-relativistic-2c) is approximated by

$$

R=\frac{c}{2c^{2}-V} \boldsymbol\sigma \cdot \boldsymbol p.\qquad \text{(eqn:166)}

$$

At the zeroth-order level (ZORA), $\Omega_{\pm } =1$, so that the ZORA
transformation is simply

$$

U_{\mathrm{ZORA} } =
\begin{pmatrix}
1 & -R^+ \\
R & 1
\end{pmatrix}\qquad \text{(eqn:167)}

$$

and the corresponding Hamiltonian given by

$$

\tilde{{h} }_{++}^{\mathrm{ZORA} } =V+c \boldsymbol\sigma \cdot \boldsymbol p \frac{1}{2c^{2}-V}c\boldsymbol\sigma \cdot \boldsymbol p.\qquad \text{(eqn:168)}

$$

At the infinite-order level (IORA), $\Omega_{\pm }$is taken into
account, so that

$$

U_{\mathrm{IORA} } =U_{\mathrm{ZORA} }
\begin{pmatrix}
\Omega_+ & 0 \\
0 & \Omega_-
\end{pmatrix}\qquad \text{(eqn:169)}

$$

and

$$

\tilde{{h} }_{++}^{\mathrm{IORA} } =\Omega_{+} \left({ V+c \boldsymbol\sigma \cdot \boldsymbol p \frac{1}{2c^{2}-V}c \boldsymbol\sigma \cdot \boldsymbol p} \right)\Omega_{+}\qquad \text{(eqn:170)}

$$

is the corresponding Hamiltonian. Note that despite the name --
*infinite-order* regular approximation -- this is still *not* exact.

In ORCA, the spin-free (scalar-relativistic) variant of ZORA and IORA
are implemented. These are obtained from those above through the
replacement

$$

\boldsymbol\sigma \cdot \boldsymbol p \frac{1}{2c^{2}-V} \boldsymbol\sigma \cdot \boldsymbol p \to \boldsymbol p \frac{1}{2c^{2}-V} \boldsymbol p.\qquad \text{(eqn:171)}

$$

The regular Hamiltonians contain only part of the Darwin term and no
mass-velocity term. A problem with relations
[Eq](#eqn:170) and
[Eq](#eqn:168) is
that due to the non-linear dependence of the resulting regular
Hamiltonians on $V$, a constant change of $V$, which in the Dirac and
Schrödinger equations will result in a corresponding change of energy

$$

E\to E+\text{const}

$$

does not so in the regular approximation. Several attempts have been
made to circumvent this problem. The scaled ZORA variant is one such
procedure. Another one is given through the introduction of model
potentials replacing $V$. Both approaches are available in ORCA.
### The Scaled ZORA Variant
This variant goes back to van Lenthe et al. [vanlenthe1994jcp](../../bibliography.md). 
The central observation is that the Hamiltonian

$$

h_{\mathrm{scaledZORA} } =\frac{h_{\mathrm{ZORA} } }{1+\left\langle { \Psi_{L} \left|{c \boldsymbol\sigma \cdot \boldsymbol p \frac{1}{\left({ 2c^{2}-V}
\right)^{2} }c \boldsymbol\sigma \cdot \boldsymbol p} \right|\Psi_{L} } \right\rangle}\qquad \text{(eqn:172)}

$$

produces constant energy-shifts $E\to E+\text{const}$ when the potential
$V$ is changed by a constant -- *for hydrogenic ions*. For many-electron
systems, the scaled-ZORA Hamiltonian still does not yield simple,
constant energy shift for $V\to
V+\text{const}$. But it produces the exact Dirac energy for
hydrogen-like atoms and performs better than the first-order regular
approximation for atomic ionization energies.

<a id="sec:essentialelements.relativistic.zora"></a>
### The Regular Approximation with Model Potential

The idea of this approach goes back to Van Wüllen [vanwuellen1998jcp](../../bibliography.md),
who suggested the procedure for DFT. However we also use it for other
methods. The scalar relativistic ZORA self-consistent field equation is
in our implementation (in atomic units):

$$

\left[{ \mathrm{\mathbf{p} }\frac{c^{2} }{2c^{2}-V }\mathrm{\mathbf{p} }+V_{\mathrm{eff} } } \right]\psi_{i} =\varepsilon_{i} \psi_{i}\qquad \text{(eqn:173)}

$$

where $c$ is the speed of light. It looks like the normal
nonrelativistic Kohn--Sham equation with the KS potential
$V_{\mathrm{eff} }$:

$$

V_{\mathrm{eff} } \left({ \mathrm{\mathbf{r} }} \right)=-\sum\limits_A { \frac{Z_{A} }{\left|{\mathrm{\mathbf{r} }-\mathrm{\mathbf{R} }_{A} } \right|} } +\int \frac{\rho \left( \mathrm{\mathbf{r}'} \right)}{\left| \mathrm{\mathbf{r} } - \mathrm{\mathbf{r}'} \right|}
d\mathrm{\mathbf{r}'} + V_{\text{xc} } \left[ \rho \right](\mathbf r)\qquad \text{(eqn:174)}

$$

($Z_{A}$ is the charge of nucleus $A$ and $R_{A}$ is its position;
$\rho (r)$ is the total electron density and
$V_{xc} \left[ \rho \right]$ the exchange-correlation potential -- the
functional derivative of the exchange-correlation energy with respect to
the density). The kinetic energy operator $T=-\frac{1}{2}\nabla^{2}$ of
the nonrelativistic treatment is simply replaced by the ZORA kinetic
energy operator:

$$

T^{\mathrm{ZORA} }=\mathrm{\mathbf{p} }\frac{c^{2} }{2c^{2}-V }\mathrm{\mathbf{p} }\qquad \text{(eqn:175)}

$$

Clearly, in the regions where the potential $V$ is small compared to
$c^{2}$, this operator reduces to the nonrelativistic kinetic energy.
$V$ could be the actual KS potential. However, this would require to
solve the ZORA equations in a special way which demands recalculation of
the kinetic energy in every SCF cycle. This becomes expensive and is
also undesirable since the ZORA method is not gauge invariant and one
obtains fairly large errors from such a procedure unless special
precaution is taken. Van Wüllen [vanwuellen1998jcp](../../bibliography.md) has therefore
argued that it is a reasonable approximation to replace the potential
$V$ with a model potential $\tilde{{V} }_{\mathrm{model} }$ which is
constructed as follows:

$$

\tilde{{V} }_{\mathrm{model} } =-\sum\limits_A { \frac{Z_{A} }{\left|{ \mathrm{\mathbf{r} }
-\mathrm{\mathbf{R} }_{A} } \right|} } +\int \frac{\rho_{\mathrm{model} } \left( \mathrm{\mathbf{r}'} \right)}{\left| \mathrm{\mathbf{r} }
-\mathrm{\mathbf{r}'} \right|}
d\mathrm{\mathbf{r}'} +V_{\text{xc} }^{\text{LDA} } \left[{ \rho^{\mathrm{model} }} \right](\mathbf r)\qquad \text{(eqn:176)}

$$

The model density is constructed as a sum over spherically symmetric
(neutral) atomic densities:

$$

\rho_{\mathrm{model} } \left({ \mathrm{\mathbf{r} }} \right)=\sum\limits_A { \rho
^{A}\left({ \mathrm{\mathbf{r} }} \right)}\qquad \text{(eqn:177)}

$$

Thus, this density neither has the correct number of electrons (for
charged species) nor any spin polarization. Yet, in the regions close to
the nucleus, where the relativistic effects matter, it is a reasonable
approximation. The atomic density is expanded in a sum of s-type
Gaussian functions like:

$$

\rho^{A}\left({ \mathrm{\mathbf{r} }} \right)=\sum\limits_i { d_{i} \exp \left({-\alpha_{i} \left|{ \mathrm{\mathbf{r} }-\mathrm{\mathbf{R} }_{A} } \right|^{2} } \right)}\qquad \text{(eqn:178)}

$$

The fit coefficients were determined in three different ways by near
basis set limit scalar relativistic atomic HF calculations and are
stored as a library in the program. 
The fitting densities are available for elements up to Rn, as well as the actinoids.
Through the variable `ModelDens` the user can choose between these fits and study the
dependence of the results in this choice (it should be fairly small
except, perhaps, with the heavier elements and the HF densities which
are not recommended). The individual components of the model potential
(eq. [Eq](#eqn:176))
can be turned on or off through the use of the variable `ModelPot`.
The available options for these keywords are listed in 
[sec:essentialelements.relativistic.keywords](#sec:essentialelements.relativistic.keywords).
For example:

```orca
! ZORA ZORA-def2-TZVP SARC/J
# for more detail use
%rel
     ModelPot 1,1,1,1
     ModelDens rhoZORA
end
```

!!! note
    The ZORA method is highly dependent on
    numerical integration and it is very important to pay attention to the
    subject of radial integration accuracy! 
    By default, from ORCA 5.0 we consider that during the grid construction 
    and the defaults should work very well.
    Only for very problematic cases, consider using a higher 
    [`IntAcc` parameter](sec:essentialelements.numericalintegration.radgrid) 
    or at least to increase the radial integration accuracy
    around the heavy atoms using `SpecialGridAtoms` and `SpecialGridIntAcc`
    (see [sec:essentialelements.numericalintegration.detailsandoptions](#sec:essentialelements.numericalintegration.detailsandoptions)).

<a id="sec:essentialelements.relativistic.dkh"></a>
## The Douglas-Kroll-Hess Method

The Douglas-Kroll-Hess (DKH) method expands the exact relation
[Eq](#eqn:exact-relativistic-2c) in the external potential V. In
ORCA the first- and second-order DKH methods are implemented. The
first-order DKH Hamiltonian is given by

$$

\tilde{h}_{++}^{(1) } =E_{p} +A_{p} VA_{p} +B_{p} V^{(p) }B_{p} ,\qquad \text{(eqn:179)}

$$

with

$$

E_{P} =\sqrt{ c^{4}+c^{2}p^{2} }, \, A_{p} =\sqrt{\frac{E_{p} +c^{2} }{2E_{p} }}, \, B_{p} =\frac{c}{\sqrt{ 2E_{p} (E_{p} +c^{2}) } }\qquad \text{(eqn:180)}

$$

At second order, it reads

$$

\tilde{{h} }_{++}^{(2) } =\tilde{{h} }_{++}^{(1) } +\frac{1}{2}\left[{ W_{p} ,O} \right]\qquad \text{(eqn:181)}

$$

where

$$

\left\{{ W_{p} ,E_{p} } \right\}=\beta O, \, O=A_{p} \left[{ R_{p} ,V}
\right]A_{p}, \, R_{p} =\frac{c\sigma p}{E_{p} +c^{2} }\qquad \text{(eqn:182)}

$$

define the second-order contribution. In ORCA, the spin-free part of
$\tilde{{h} }_{++}^{(2) }$ is implemented.

The occurrence of the relativistic kinetic energy, $E_{P}$, which is not
well-defined in position space, makes a transformation to the
$p^{2}$-eigenspace necessary. Thus any DKH calculation will start with a
decontraction of the basis set, to ensure a good resolution of the
identity. Then the non-relativistic kinetic energy is diagonalized and
the $E_{P}$-dependent operators calculated in that space. The potential
$V$ and $V^{(p) }$ are transformed to $p^{2}$-eigenspace. After all
contributions are multiplied to yield the (first- or second-order)
Hamiltonian, the transformation back to AO space is carried out and the
basis is recontracted.

The (spin-free) DKH-Hamiltonians contain all spin-free, relativistic
correction terms, e.g. the mass-velocity and Darwin terms. As the
potential enters linearly, no scaling or model potential is necessary to
introduce the correct behaviour of the energy under a change

$$

V\to V+\text{const}.

$$

In all these respects the DKH Hamiltonians are much cleaner than the
regular approximation Hamiltonians.
The first- or second-order DKH method be requested via the simple input keywords 
`DKH1` or `DKH2`, respectively (`DKH` is an alias for the latter), 
together with appropriate basis sets:
```orca
! DKH DKH-def2-TZVP SARC/J
```
For most calculations, no other settings are needed.
A full list of available keywords is given in 
[sec:essentialelements.relativistic.keywords](#sec:essentialelements.relativistic.keywords).
<a id="sec:essentialelements.relativistic.dkh.magnetic"></a>
### Magnetic Properties with DKH
For magnetic properties, the DKH transformation and consequently the DKH
Hamiltonian and the corresponding property operators are not unique.
Depending on whether the magnetic field is included in the free-particle
Foldy--Wouthuysen (fpFW) transformation carried out in the first step of
the DKH protocol or not, two different Hamiltonians result. If the
magnetic field is included in the fpFW transformation, the resulting
Hamiltonian is a function of the gauge invariant momentum

$$

\boldsymbol{\pi}=\textbf{p}+\textbf{A}.

$$

It is therefore gauge invariant under gauge transformations of the
magnetic vector potential $\mathbf A$ and thus are the property
operators derived from it. This is referred to as f$\pi$FW DKH
Hamiltonian. If the magnetic field is not included in the FW
transformation, the resulting Hamiltonian is a function of the kinetic
momentum $\textbf{p}$ only and thus is not gauge invariant. The latter
Hamiltonian is referred to as fpFW DKH Hamiltonian. A comparison of both
Hamiltonians is given in Table [table:compdkhham](#table:compdkhham).
<a id="table:compdkhham"></a>
!!! note "Comparison of the properties of the fpFW and fπFW DKH Hamiltonians. For details see Ref. [sandhoefer2012jcp](../../bibliography.md)."
    | Criterion                    | fpFW Hamiltonian | fπFW Hamiltonian     |
    |:-----------------------------|:----------------:|:--------------------:|
    | Convergence of Eigenvalues to Dirac Eigenvalues  | ? |    yes          |
    | 1st order is bounded         |        no        |         yes          |
    | Reproduces Pauli Hamiltonian |        no        |         yes          |
    | Gauge invariance             |        no        |         yes          |
    | Lorentz invariance           |        no        |          no          |
From this Table, it becomes clear that the f$\pi$FW DKH Hamiltonian is
clearly preferred over the fpFW Hamiltonian. To obtain the property
operators, it is however necessary to take the derivatives of these
Hamiltonians. It turns out that in the case of the hyperfine-coupling
tensor, the necessary derivatives produce divergent property operators
in the case of the f$\pi$FW DKH Hamiltonian. This may be due to the
unphysical assumption of a point-dipole as a source of the magnetic
field of the nucleus. As a physical description of the magnetization
distribution of the nucleus is not available due to a lack of
experimental data, the magnetization distribution is assumed to be the
same as the charge distribution of the nucleus, see
Section [sec:essentialelements.relativistic.finnuc](#sec:essentialelements.relativistic.finnuc).
This is unphysical as the magnetization is caused by the one unpaired nucleon in the nucleus
whereas the charge distribution is generated by the protons in the
nucleus. So, physically, the magnetization should occupy a larger volume
in space than the charge. This might also be the reason why the
resulting finite-nucleus model is insufficient to remedy the
divergences in the f$\pi$FW hyperfine-coupling tensor. Consequently,
the hyperfine-coupling tensor is only implemented in the version
resulting from the fpFW DKH Hamiltonian. In the case of the g-tensor
both versions are implemented and accessible via the keyword
```orca
%rel fpFWtrafo true/false end
```
By default, this keyword is set to `true`. A detailed form of the
property operators used for the g-tensor and hyperfine-tensors can be
found in Ref. [sandhoefer2012jcp](../../bibliography.md).
<a id="sec:essentialelements.relativistic.x2c"></a>
## Exact Two-Component Theory (X2C) 
The X2C implementation in ORCA closely follows that of Franzke, Weigend,
and their coworkers, described in the references: [Peng2013](../../bibliography.md) (energy),
[Franzke2018](../../bibliography.md) (gradient), [Franzke2022](../../bibliography.md) (EPR hyperfine coupling),
[Franzke2021a](../../bibliography.md) (NMR spin--spin coupling), [Franzke2019](../../bibliography.md) (NMR
shielding). These are also consistent with the work of Gauss and
coworkers in refs: [Cheng2011](../../bibliography.md) (gradient, electric properties),
[Cheng2011a](../../bibliography.md) (Hessian), [Cheng2013](../../bibliography.md) (NMR shielding). However, despite
the name, only a scalar relativistic (spin-free) version is available at
present, resulting effectively in a one-component method (more aptly
called "SF-X2C-1e"), very similar to the DKH and ZORA approaches
described above. The main difference to the latter two is that the
decoupling of the one-electron Dirac Hamiltonian is exact, rather than
approximate. SF-X2C-1e is implemented in ORCA for energies, gradients,
and various properties (see below) with both a point- and finite nucleus
model.
We briefly describe the working equations here, using the notation of
the aforementioned references, which differs somewhat from that in the
previous sections. The one-electron Dirac equation is solved directly:

$$

\mathbb{D C} = \mathbb{M C E},
\quad
  \mathbb{C} =
  \begin{pmatrix}
  \mathbf C^{\mathrm L}_{+} & \mathbf C^{\mathrm L}_{-} \\
  \mathbf C^{\mathrm S}_{+} & \mathbf C^{\mathrm S}_{-} \\
  \end{pmatrix}\qquad \text{(eq:x2c-DCSCE)}

$$

to obtain the unitary transformation matrix:

$$

\begin{aligned}
  \mathbb{U} &= 
  \begin{pmatrix}
  \mathbf U_{++} & \mathbf U_{+-} \\
  \mathbf U_{-+} & \mathbf U_{--} \\
  \end{pmatrix}
  = 
  \begin{pmatrix}
  \mathbf 1 & -\mathbf X^\dagger \\
  \mathbf X & \mathbf 1 \\
  \end{pmatrix}
  \begin{pmatrix}
  \mathbf R & \mathbf 0 \\
  \mathbf 0 & \mathbf R' \\
  \end{pmatrix}
\\
  \mathbf X &= \mathbf C^{\mathrm S}_{+} \left( \mathbf C^{\mathrm L}_{+} \right)^{-1}\\
  \mathbf R &= \mathbf S^{-\frac{1}{2} } \left(\mathbf S^{-\frac{1}{2} }\tilde{\mathbf S} \mathbf S^{-\frac{1}{2} }\right)^{-\frac{1}{2} } \mathbf S^{\frac{1}{2} }\\
  \tilde{\mathbf S} &= \mathbf S + \frac{1}{2c^2}\mathbf X^\dagger \mathbf T \mathbf X
\end{aligned}

$$

which exactly block-diagonalizes the Hamiltonian:

$$

\mathbb{U^\dagger D U} =
  \begin{pmatrix}
  \mathbf h^{+} & \mathbf 0 \\
  \mathbf 0 & \mathbf h^{-} \\
  \end{pmatrix}\qquad \text{(eq:x2c-UDU)}

$$

$$

\mathbf h^{+} = 
  \mathbf R^\dagger \mathbf L \mathbf R\qquad \text{(eq:x2c-h)}

$$

$$

\mathbf L = \mathbf V + \mathbf T \mathbf X + \mathbf X^\dagger \mathbf T 
 +\mathbf X^\dagger \left(\frac{1}{4c^2} \mathbf W - \mathbf T\right) \mathbf X\qquad \text{(eq:x2c-L)}

$$

where $\mathbf V$, $\mathbf T$, $\mathbf S$, and $\mathbf W$ are the
potential, kinetic, overlap, and relativistic potential
($\hat p\,\hat V\hat p$) integral matrices. $\mathbf h^{+}$ is thus the
matrix form of the relativistically-corrected one-electron Hamiltonian
used for the rest of the calculation.

Note that the potential operator $\hat V$ used in the above equations
only includes the electron--nuclear Coulomb interaction. External point
charges may optionally be included via `%rel ModelPot[4]=1` (default 0).
This option affects energy and NMR shielding calculations but it is
presently not available for gradients or Hessians.

In the simplest case, it is sufficient to add the `X2C` simple keyword to the input
and choose an appropriate basis set:

```orca
! X2C X2C-TZVPall X2C/J
```

<a id="sec:essentialelements.relativistic.x2c.dlu"></a>
### DLU Approximation

The diagonal local approximation to the unitary transformation matrix
(DLU), as introduced by Peng and Reiher,[Peng2012](../../bibliography.md) reduces the
computational cost of the X2C transformation by approximating
$\mathbb U$ (i.e., $\mathbf R$ and $\mathbf X$) as an
atomic-block-diagonal matrix.
It leads to very minor loss of accuracy and is particularly suited
for gradient/Hessian calculations.

$$

\begin{aligned}
  \mathbf R &\approx \bigoplus_A \mathbf R_A
&
  \mathbf X &\approx \bigoplus_A \mathbf X_A\end{aligned}

$$

where $\bigoplus_A$ denotes a direct sum of atomic diagonal blocks.
Eqs [Eq](#eq:x2c-DCSCE)--[Eq](#eq:x2c-L) can then be solved independently for diagonal
atomic blocks $\mathbf h^+_{AA}$. Off-diagonal blocks $\mathbf h^+_{AB}$
are obtained as:

$$

\begin{aligned}
    \mathbf h^+_{AB}  &= \mathbf R^\dagger_A \mathbf L_{AB} \mathbf R_B
\\
    \mathbf L_{AB} &= \mathbf V_{AB} + \mathbf T_{AB} \mathbf X_B + \mathbf X^\dagger_A \mathbf T_{AB} + \mathbf X^\dagger_A \left(\frac{1}{4c^2}\mathbf W_{AB} - \mathbf T_{AB}\right) \mathbf X_B\end{aligned}

$$

It is also possible to approximate light atoms $a,b$ (below a certain
atomic number) as non-relativistic:

$$

\begin{aligned}
  \mathbf X_a &= \mathbf R_a = \mathbf I
\\
  \mathbf W_{ab} &= \mathbf W_{aB} = \mathbf 0
\\
  \mathbf h^+_{ab} &= \mathbf V_{ab} + \mathbf T_{ab}
\\
  \mathbf h^+_{aB} &= \left(\mathbf V_{aB} + \mathbf T_{aB} \mathbf X_B\right) \mathbf R_B\end{aligned}

$$

Unlike the one center approximation (which is also available for X2C),
all nuclei are included in the potential operator $\hat V$. 

The DLU approximation can be requested via the simple input keyword `!DLU-X2C`.
Additional options are available in the `%rel` block 
(see also [sec:essentialelements.relativistic.keywords](#sec:essentialelements.relativistic.keywords)):

```orca
%rel
  DLU         false # default - not used
               true # turn DLU on
  LightAtomThresh 0 # (default) highest atomic number treated as non-relativistic
end
```

<a id="sec:essentialelements.relativistic.x2c.props"></a>
### X2C Derivatives and Properties

As discussed in [sec:essentialelements.relativistic.picturechange](#sec:essentialelements.relativistic.picturechange), 
when computing properties with relativistic methods, 
derivatives need to be taken of the correct Hamiltonian, 
namely $\mathbf h^+$ (eq [Eq](#eq:x2c-h)) in the X2C case. 
These include contributions due to the derivatives of $\mathbf R$ and $\mathbf X$, 
which are often small. 
Therefore, it is possible to neglect them and save some computational time 
via the following option:

```orca
%rel
  PictureChange 2 # compute the full relativistic Hamiltonian derivative
                1 # neglect derivatives of R and X
                0 # (default) use the non-relativistic operator
end
```

The same setting is applied to all properties for which the X2C
correction is implemented. Currently, these are: geometric gradients,
electric dipoles, quadrupoles, and polarizabilities, electric field
gradients, EPR hyperfine couplings, and NMR shieldings and spin--spin couplings.
For the Hessian, the X2C correction is implemented in a semi-numeric fashion.
The DLU approximation is applied throughout, if requested,
and reduces the computational effort dramatically. Note that for
magnetic properties, the restricted magnetic balance (RMB) for the small
component basis functions is used whenever GIAOs are requested (e.g. NMR
shielding), while the restricted kinetic balance (RKB) is used otherwise
(e.g. NMR coupling). The spin--orbit coupling integrals used for various
properties only include a relativistic correction to the one-electron
term, as is the case for DKH.

For second derivative properties whose number is proportional to the
number of atoms, e.g. the DSO term of NMR couplings, first derivatives
of various intermediate quantities required for the full X2C second
derivative are stored on disk. The storage requirements can be reduced
via the `StorageLevel` keyword and the missing intermediates will be
recomputed on-the-fly, which of course increases the computation time.

```orca
%rel
  StorageLevel 0 # do not store anything - not always available
               1 # store integral derivatives
               2 # 1 + derivatives of R and X (default, minimum for DLU)
               3 # 2 + derivatives of L
               4 # 3 + derivatives of S-tilde
               5 # 4 + derivatives of D and M
end
```

<a id="sec:essentialelements.relativistic.basissets"></a>
## Basis Sets in Relativistic Calculations

The different scalar relativistic potentials have different shapes in the core region. 
Consequently, each one of them requires specialized all electron basis sets that are optimized for the Hamiltonian at hand. 
Such basis sets have been designed,
both as DKH and ZORA recontractions of the [Ahlrichs](sec:essentialelements.basisset.builtin.rel.ahlrichs) 
and [Karlsruhe](sec:essentialelements.basisset.builtin.rel.def2) basis sets
for elements up to Kr (for which the original non-relativistic versions are all-electron), 
and as purpose-built segmented all-electron relativistically contracted (SARC) 
basis sets for elements beyond Kr
.[Pantazis2008,Buehl2008,Pantazis2009,Pantazis2011,Pantazis2012,Rolfes2020](../../bibliography.md)
For X2C calculations, the ["x2c-XVPall" basis sets](sec:essentialelements.basisset.builtin.rel.karlsruhex2c)
and their variants are available.[Weigend2017-x2c-XVP,Weigend2019-x2c-XVP-s](../../bibliography.md)
All available built-in choices are listed in the section [sec:essentialelements.basisset.builtin.rel](#sec:essentialelements.basisset.builtin.rel).

An uncontracted all-electron basis set of sufficient size will always work.
Likewise, uncontracted fitting basis sets in all forms of RI calculations are always appropriate. 
Use the [`!Decontract` keyword](par:essentialelements.basisset.basicusage.decontract)
to decontract the chosen basis set and make it suitable for any relativistic Hamiltonian, as well as comparisons between them.

If large, uncontracted basis sets are used in scalar relativistic calculations, there is a distinct danger of variational collapse. 
This behavior is related to the fact that the relativistic orbitals will diverge for a point nucleus. 
ORCA features the Gaussian finite nucleus model of Dyall and Visscher for DKH and X2C. 
We recommend to always use this feature (`FiniteNuc`) in relativistic calculations 
(see [sec:essentialelements.relativistic.finnuc](#sec:essentialelements.relativistic.finnuc)). 

Given the fact relativistic all-electron calculations on heavy element compounds feature very steep core basis functions, 
numeric integration, such as in DFT and COSX, may be challenging. 
ORCA features automatic procedures that adapt the integration grids for the presence of steep basis functions. 
However, in case you experience strange results, the numeric integration is one potential source of problem. 
The cure is to go to larger integration grids and, in particular, 
increase the [radial integration accuracy](sec:essentialelements.numericalintegration.radgrid) (`IntAcc`). 

<a id="sec:essentialelements.relativistic.picturechange"></a>
## Picture-Change Effects

Irrespective of which Hamiltonian has been used 
in the determination of the wave function, 
the calculation of properties requires some special care. 
This can be understood in two ways: 
First of all, we changed from the ordinary Schrödinger Hamiltonian 
to a more complicated Hamiltonian.
As properties are defined as derivatives of the energy, 
it is clear that a new Hamiltonian will yield a new expression for the energy 
and thus a new and different expression for the property in question. 
Another way of seeing this is that through the transformation $U$, 
we changed not only the Hamiltonian but also the wave function. 
To obtain the property at hand as the expectation value 
of the property operator with the wave function, 
we have to make sure that property operator and wave function
are actually given in the same space. 
This is done through a transformation of either the property operator or the wave function.

In any case, the difference between the non-relativistic 
and (quasi) relativistic property operator,
evaluated over the (quasi) relativistic wave function, 
is called the _picture-change effect_. 
From what was said above, this is clearly not a physical effect. 
It describes how consistently the quasi relativistic calculation is carried out. 
A fully consistent calculation requires the determination of the wave function
on the (quasi) relativistic level as well,
as the use of the (quasi) relativistic property operator. 
This is obtained by enabling the `PictureChange` option in the `%rel` block:

```orca
%rel PictureChange 1 end  # or 2 - see below
```

It may be that the (quasi) relativistic and non-relativistic
property operator do produce similar results. 
In this case, a calculation with picture-change turned off
(`PictureChange=0`) may be a good approximation. 
This is often the case for valence shell-dominated properties, 
such as the eletric dipole and polarizability.
On the other hand, property calculations involving operators 
that carry inverse powers of the electron-nucleus distance
can be wildly inaccurate if picture change effects are ignored.
It is therefore highly recommended to turn on picture-change
in all (quasi) relativistic property calculations!

For DKH2, the fully consistent picture-change effects are obtained
using the same transformation order for the property operator
as for the one-electron Hamiltonian, i.e. setting `PictureChange=2`,
while with `PictureChange=1` only first-order changes on the property operators 
are taken into account, which reduces the computational cost. 
However, since this is in no way a significant reduction, this choice is not recommended.

A similar argument applies to X2C, 
where `PictureChange=2` is the formally correct approach
and `PictureChange=1` is an approximate treatment 
(see [sec:essentialelements.relativistic.x2c.props](#sec:essentialelements.relativistic.x2c.props)).

By default, ORCA tries to choose the most appropriate value 
of the `PictureChange` variable depending on the requested properties,
as described below (and issues a warning at the start of the output), 
but explicit user input is always respected.
- For geometric perturbations with DKH or ZORA the 
  [one-center approximation](sec:essentialelements.relativistic.hamiltonian.1c)
  is activated and picture-change corrections are not needed.
  With X2C, `PictureChange=1` is chosen, because it significantly
  reduces the computational cost.
- For other properties, in particular core-sensitive ones (i.e. in EPR/NMR), 
  the full picture-change correction is applied.
- Certain combinations of relativistic Hamiltonian and property operator are not implemented,
  in which case ORCA prints a warning, or aborts entirely 
  if picture change effects are expected to be significant.

<a id="sec:essentialelements.relativistic.finnuc"></a>
## Finite Nucleus Model

Composite particles like nuclei have, as opposed to elementary particles, a certain spatial extent.
While the point-charge approximation for nuclei is 
in general very good in nonrelativistic calculations, 
in relativistic calculations it might lead to non-negligible errors. 
A finite-nucleus model is implemented in ORCA -- 
the Gaussian nucleus model of Ref. [visscher1997atom](../../bibliography.md) --
and is available for DKH and X2C (but not ZORA) calculations in the ORCA program package.
It is accessible from the `%rel` block via

```orca
%rel FiniteNuc true end
```

By default, this keyword is set to `false`. If the keyword is set to
`true`, finite-nucleus effects are considered in the following
integrals:

- nucleus potential $V$ and its nuclear derivatives;
- relativistic potential integral $V^{(p) }$ in DKH and X2C;
- one-electron part of the spin-orbit (SOC) integrals;
- electric-field gradient (EFG);
- contact density integral;
- Fermi-contact and spin-dipole terms of the EPR hyperfine coupling;
  and NMR indirect spin-spin coupling tensors;
- nucleus-orbit coupling integral;
- angular-momentum integral;
- NMR shielding integrals over GIAOs.

<a id="sec:essentialelements.relativistic.keywords"></a>
## Keywords

<a id="tab:essentialelements.relativistic.keywords.simple"></a>
!!! note "Simple input keywords for relativistic methods."
    :class: footnotesize
    | Keyword             | Description                                                                                   |
    |:--------------------|:----------------------------------------------------------------------------------------------|
    | `DKH1`              | Activate the first-order DKH Hamiltonian                                                      |
    | `DKH2`, `DKH`       | Activate the second-order DKH Hamiltonian                                                     |
    | `ZORA`              | Activate the ZORA Hamiltonian                                                                 |
    | `IORA`              | Activate the IORA Hamiltonian                                                                 |
    | `X2C`               | Activate the X2C Hamiltonian                                                                  |
    | `DLU-X2C`           | Activate the X2C Hamiltonian in the DLU approximation                                         |
    | `RelDLU`            | Enable the [DLU approximation](sec:essentialelements.relativistic.x2c.dlu) (X2C only)         |
    | `Rel1C`             | Enable the [one-center approximation](sec:essentialelements.relativistic.hamiltonian.1c)      |
    | `RelFull`           | Disable the one-center and DLU approximations                                                 |

<a id="tab:essentialelements.relativistic.keywords.block"></a>
!!! note "`%rel` block input keywords relativistic methods."
    :header-rows: 1
    :class: longtable
    :class: footnotesize

| Item | Value |
| --- | --- |
| **Keyword** | — |

      - Options
      - Description

| Item | Value |
| --- | --- |
| **{rspan}`3` `Method`** | — |

      - `DKH`
      - {rspan}`3`Scalar relativistic Hamiltonian

| Item | Value |
| --- | --- |
| **`ZORA`** | — |
| **`IORA`** | — |
| **`X2C`** | — |
| **`ModelPot`** | — |

      - `<VeN>, <VC>, <VXa>, <VLDA>, <VPC>`
      - Flags for model potential (1: included, 0: not included). 
        `<VeN>`: nuclear attraction; 
        `<VC>`: Coulomb (ZORA/IORA only); 
        `<VXa>`: Xalpha (ZORA/IORA only); 
        `<VLDA>`: VWN-5 correlation (ZORA/IORA only); 
        `<VPC>`: point charges (X2C only)

| Item | Value |
| --- | --- |
| **{rspan}`2` `ModelDens`** | — |

      - `rhoDKH`
      - {rspan}`2` Fitted atomic density used for Coulomb model potential and for PModel guess

| Item | Value |
| --- | --- |
| **`rhoZORA`** | — |
| **`rhoHF`** | — |
| **`OneCenter`** | — |

      - `false`
      - If true, use the [one-center approximation](sec:essentialelements.relativistic.hamiltonian.1c)

| Item | Value |
| --- | --- |
| **`C`** | — |

      - 137.0359895
      - Speed of light used (in a.u.). Synonyms: `VELIT`, `VELOCITY`

| Item | Value |
| --- | --- |
| **`PictureChange`** | — |

      - 0, 1, 2
      - [Picture change](sec:essentialelements.relativistic.picturechange) for properties. 
        0: none; 1: enable; 2: full (DKH/X2C). Default: determine automatically

| Item | Value |
| --- | --- |
| **`FiniteNuc`** | — |

      - `false`
      - Whether to use the [finite nucleus model](sec:essentialelements.relativistic.finnuc) (DKH or X2C)

| Item | Value |
| --- | --- |
| **`PrintLevel`** | — |

      - 1
      - How much relativistics-related output to print (0-4). Alias for `%output Print[P_Rel]`

| Item | Value |
| --- | --- |
| **{cspan}`2` DKH-specific** | — |
| **`Order`** | — |

      - 2
      - Order of DKH Hamiltonian (1 or 2)

| Item | Value |
| --- | --- |
| **`fpFWtrafo`** | — |

      - `true`
      - Kind of Foldy-Wouthuysen transformation used for EPR with DKH 
        (see [sec:essentialelements.relativistic.dkh.magnetic](#sec:essentialelements.relativistic.dkh.magnetic)). 
        `true`: fpFW; `false`: fπFW

| Item | Value |
| --- | --- |
| **{cspan}`2` ZORA-specific** | — |
| **`Xalpha`** | — |

      - 0.7
      - Default value for Xalpha potential. Has effect only if VXa is included

| Item | Value |
| --- | --- |
| **`ScaleZORA`** | — |

      - `false`
      - Whether to scale the orbital energies (single points only)

| Item | Value |
| --- | --- |
| **{cspan}`2` X2C-specific** | — |
| **`DLU`** | — |

      - `false`
      - If true, use the [DLU approximation](sec:essentialelements.relativistic.x2c.dlu) 
        for X2C (mutually exclusive with `OneCenter`)

| Item | Value |
| --- | --- |
| **`LightAtomThresh`** | — |

      - 0
      - Highest atomic number treated as non-relativistic in the 
        [DLU approximation](sec:essentialelements.relativistic.x2c.dlu) 

| Item | Value |
| --- | --- |
| **`StorageLevel`** | — |

      - 2
      - X2C intermediate storage level (0–5) -- 
        see [sec:essentialelements.relativistic.x2c.props](#sec:essentialelements.relativistic.x2c.props)

