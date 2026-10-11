

<a id="sec:spectroscopyproperties.ihfsmrcc"></a>
# Excited States via IH-FSMR-CCSD

An alternative approach for decoupling the singles excitation space from
the space of double and higher excitations is to use the so called Fock
space multi-reference coupled cluster (FSMRCC) method. The method is
similar to STEOM-CCSD, but much more flexible in terms of formulation.

<a id="sec:spectroscopyproperties.ihfsmrcc.general"></a>
## General Description

FSMRCC is originally based on an effective Hamiltonian (EH). The basic
idea of EH theory is to obtain some selective eigenvalues of the
Hamiltonian operator from the total eigenvalue spectrum. For this
purpose, the entire configuration space is divided into a model and an
outer space with projection operators $P_{M}$ and $Q_{M}$, respectively
(see [fig:ihfsmrcc_ms](#fig:ihfsmrcc_ms)). The diagonalization of the EH takes care
of the non-dynamic correlation coming from the interactions between the
model space configurations. On the other hand, the dynamic correlation
arises due to the interactions of the model space configurations with
the outer space configurations. This interaction is introduced through a
universal wave operator $\Omega$, which is parametrized such that it
generates the exact wave function when acting on the model space. The
valence universal wave operator $\Omega$ has the form

$$

\begin{aligned}
\Omega=e^{\tilde{S}^{\left( p,h \right)} }\end{aligned}

$$

where the braces indicate normal ordering of the cluster operators and
$\tilde{S}^{\left( p,h \right)}$ is defined as

$$

\begin{aligned}
\tilde{S}^{\left( p,h \right)}=\sum_{k=0}^{p}\sum_{l=0}^{h}\tilde{S}^{\left( k,l \right)}\end{aligned}

$$

The cluster operator $\tilde{S}^{\left( k,l \right)}$ is capable of
destroying exactly k active particles and l active holes, in addition to
creation of holes and particles. The $\tilde{S}^{\left( p,h \right)}$
subsumes all lower sector Fock space $\tilde{S}^{\left( k,l \right)}$
operators. The $\tilde{S}^{\left( 0,0 \right)}$ is equivalent to
standard single-reference coupled cluster $\hat{T}$ operator. The EH for
(p,h) valence system can be defined as

$$

\begin{aligned}
\hat{H}_{eff}=P_{M}^{\left( p,h \right)}\Omega^{-1}\hat{H}\Omega P_{M}^{\left( p,h \right)}\end{aligned}

$$

However, $\Omega^{-1}$ may not be well defined in all the cases.
Therefore, the above definition for the EH is seldom used. Instead, the
Block-Lindgren approach is generally used for solving the equations,
which is defined by

$$

\begin{aligned}
P_{M}^{\left( p,h \right)}\left[  \hat{H}\Omega -\Omega\hat{H}_{eff}\right]P_{M}^{\left( p,h \right)}=0\end{aligned}

$$

$$

\begin{aligned}
Q_{M}^{\left( p,h \right)}\left[  \hat{H}\Omega -\Omega\hat{H}_{eff}\right]P_{M}^{\left( p,h \right)}=0\end{aligned}

$$

<a id="fig:ihfsmrcc_ms"></a>
*Division of the configuration space into model and outer space in
effective Hamiltonian (EH) theory and into model, intermediate, and
outer space in intermediate Hamiltonian (IH) theory. $P$ and $Q$ denote
the respective projection operators.*

When the model space is not energetically well separated from the outer
space, this method faces convergence problems. This is commonly termed
as the intruder state problem. In the intermediate Hamiltonian (IH)
formulation, configuration space is divided into three subspaces,
namely, the main(M), the intermediate(I), and the outer(O) space (see
[fig:ihfsmrcc_ms](#fig:ihfsmrcc_ms)) with projection operators $P_{M}$, $P_{I}$
and $Q_{O}$, respectively. The intermediate space acts as a buffer
between the model and the outer space. When diagonalization the IH, a
subset of the eigenvalues correspond to the main space obtained through
EH theory. The IH is for the singly excited state sector (1,1) is
defined as

$$

\begin{aligned}
H_{I}^{\left( 1,1 \right)}=P_{O}^{\left( 1,1 \right)}\bar{H}P_{O}^{\left( 1,1 \right)}+P_{O}^{\left( 1,1 \right)}\bar{H}Y^{\left( 1,1 \right)}P_{M}^{\left( 1,1 \right)}\end{aligned}

$$

where

$$

\begin{aligned}
Y^{\left( 1,1 \right)}=Q_{O}^{\left( 1,1 \right)}\left\{S_{2}^{\left( 0,1 \right)} +S_{2}^{\left( 1,0 \right)}+  S_{2}^{\left( 0,1 \right)}S_{1}^{\left( 1,0 \right)} +S_{2}^{\left( 1,0 \right)}S_{1}^{\left( 0,1 \right)}+S_{2}^{\left( 1,0 \right)}S_{2}^{\left( 0,1 \right)}\right\}P_{M}^{\left( 1,1 \right)}\end{aligned}

$$

The $S^{\left( 1,0 \right)}$ and $S^{\left( 0,1 \right)}$ are extracted
from converged EOMIP-CCSD and EOMEA-CCSD calculations, respectively, by
invoking intermediate normalization on the suitably chosen eigenvectors
corresponding to active holes and active particles. The total procedure
can be described as following

-   solve the ground state coupled cluster equations

-   construct $\hat{\bar{H} }=e^{-\hat{T} }\hat{H}e^{\hat{T} }$

-   solve the EOMIP and EOMEA equations

-   extract the $\hat{S}$ amplitudes

-   construct the second similarity transformed Hamiltonian as
    $H_{I}^{\left( 1,1 \right)}$

-   diagonalize the $H_{I}^{\left( 1,1 \right)}$ in CIS space

The automatic active space selection scheme and all the speed up options
which are available for STEOM-CCSD, including bt-PNO and COSX, are also
available for IH-FSMR-CCSD. All the keywords controlling the
IH-FSMR-CCSD are similar to STEOM-CCSD as described in
[sec:spectroscopyproperties.steom](#sec:spectroscopyproperties.steom).

No UHF variant of IH-FSMR-CCSD is currently available.

<a id="sec:spectroscopyproperties.ihfsmr.properties"></a>
## Properties

The transition properties can be calculated using a simple CIS-like
formulation, employing the converged IH-FSMR-CC eigenvectors. The
transition moments are computed by default in an IH-FSMR-CCSD
calculation.

<a id="sec:spectroscopyproperties.ihfsmr.Solvation"></a>
## Solvation Correction

Solvent effects can be approximated by a simple perturbative correction
to the IH-FSMR-CCSD via

$$

\begin{aligned}
\omega_{k}=\omega^{0}_{k}+\frac{1}{2} \bar{V}^{\Delta}\bar{Q}^{\Delta}\end{aligned}

$$

where

$$

\begin{aligned}
\omega^{0}_{k}=\hat{L_{K} }H_{I}^{\left( 1,1 \right)} \hat{R_{K} }\end{aligned}

$$

The CPCM correction directly enters the $H_{I}^{\left( 1,1 \right)}$,
the modified Hatree-Fock orbitals. In the non-equilibrium regime, one
can simply write the perturbative correction as

$$

\begin{aligned}
\omega_{k}^{neq}=\omega^{0,neq}_{k}+\frac{1}{2} \bar{V}\left( P_{\Delta}^{neq}\right) \bar{Q}\left( P_{\Delta}^{neq}\right)\end{aligned}

$$

where

$$

\begin{aligned}
P_{\Delta}^{neq}=L_{k}R_{k}\end{aligned}

$$

A typical input file looks like

```orca
! aug-cc-pVDZ IH-FSMR-CCSD
!CPCM(water)
%mdci
NROOTS 8
DoSOLV true
DTol 1e-10
end
*xyz 0 1
O       0.0000  0.0000  0.1173
H       0.0000  0.7572 -0.4692
H       0.0000 -0.7572 -0.4692
*
```

For the above input, the following output is obtained:

```orca
---------------------------------
     CALCULATED SOLVENT SHIFTS   
            CPCM  MODEL          
---------------------------------

Contributions of the 'fast' term to the solvent shift

 State Shift(Eh) Shift(eV) Shift(cm**-1) Shift(nm) E_FSMRCC(eV)  E_FSMRCC+SHIFT(eV)
-------------------------------------------------------------------------------
   0: -0.0058000 -0.158    -1273.0        3.3      7.814          7.656
   1: -0.0133523 -0.363    -2930.5        5.0      9.650          9.287
   2: -0.0053622 -0.146    -1176.9        1.8     10.144          9.998
   3: -0.0078092 -0.212    -1713.9        2.2     10.958         10.746
   4: -0.0040294 -0.110     -884.4        1.0     11.534         11.424
   5: -0.0137147 -0.373    -3010.0        3.3     12.003         11.630
   6: -0.0093172 -0.254    -2044.9        2.2     12.131         11.878
   7: -0.0077514 -0.211    -1701.2        1.7     12.562         12.352
```

Thee perturbative correction only changes the transition energies and
neither the wave function nor the transition moment.
