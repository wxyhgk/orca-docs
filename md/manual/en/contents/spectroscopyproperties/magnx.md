```{index} Broken-Symmetry Wavefunctions and Exchange Couplings
```

(sec:spectroscopyproperties.magnx)=
# Broken-Symmetry Wavefunctions and Exchange Couplings

A popular way to estimate the phenomenological parameter
$J_{\mathrm{AB} }$ that enters the Heisenberg--Dirac--van Vleck
Hamiltonian which parameterizes the interaction between two spin systems
is the "broken-symmetry" formalism. The phenomenological Hamiltonian is:

$$H_{\mathrm{HDvV} } = -2J_{\mathrm{AB} } \vec{{S} }_{\mathrm{A} } \vec{{S} }_{\mathrm{B} }
$$ (eqn:HDvV)

It is easy to show that such a Hamiltonian leads to a "ladder" of spin
states from $S=S_{\mathrm{A} } + S_{\mathrm{B} }$ down to
$S=\left|{ S_{\mathrm{A} } - S_{\mathrm{B} }} \right|$. If the parameter
$J_{\mathrm{AB} }$ is positive the systems "A" and "B" are said to be
*ferromagnetically* coupled because the highest spin-state is lowest in
energy while in the case that $J_{\mathrm{AB} }$ is negative the
coupling is *antiferromagnetic* and the lowest spin state is lowest in
energy.

In the broken symmetry formalism one tries to obtain a wavefunction that
breaks spatial (and spin) symmetry. It may be thought of as a "poor
man's MC-SCF" that simulates a multideterminantal character within a
single determinant framework. Much could be said about the theoretical
advantages, disadvantages, problems and assumptions that underly this
approach. Here, we only want to show how this formalism is applied
within ORCA.

For $N_{\mathrm{A} }$ unpaired electrons localized on "site A" and
$N_{\mathrm{B} }$ unpaired electrons localized on a "site B" one can
calculate the parameter $J_{\mathrm{AB} }$ from two separate
spin-unrestricted SCF calculations: (a) the calculation for the
high-spin state with
$S=\frac{\left({ N_{\mathrm{A} } + N_{\mathrm{B} }} \right)}{2}$ and (b)
the "broken symmetry" calculation with
$M_{S} = \frac{\left({ N_{\mathrm{A} } -N_{\mathrm{B} } }
\right)}{2}$ that features $N_{\mathrm{A} }$ spin-up electrons that are
quasi-localized on "site A" and $N_{\mathrm{B} }$ spin-down electrons
that are quasi-localized on "site B". Several formalisms exist to
extract $J_{\mathrm{AB} }$:
{cite}`GinsbergJACS1980,NoodlemanJCP1981,NoodlemanCP1986,BenciniJACS1980,Yamaguchi1986,SodaCPL2000`.

$$J_{\mathrm{AB} } = - \frac{\left({ E_{\mathrm{HS} } -E_{\mathrm{BS} } } \right)}{\left({ S_{\mathrm{A} } +S_{\mathrm{B} } } \right)^{2} }
$$ (eqn:J_weak)

$$J_{\mathrm{AB} } = -\frac{\left({ E_{\mathrm{HS} } -E_{\mathrm{BS} } } \right)}{\left({ S_{\mathrm{A} } +S_{\mathrm{B} } } \right)\left({ S_{\mathrm{A} } +S_{\mathrm{B} } +1} \right)}
$$ (eqn:J_strong)

$$J_{\mathrm{AB} } =-\frac{\left({ E_{\mathrm{HS} } -E_{\mathrm{BS} } } \right)}{\left\langle { S^{2} } \right\rangle_{\mathrm{HS} } -\left\langle { S^{2} } \right\rangle_{\mathrm{BS} } }
$$ (eqn:J_Yamaguchi)

We prefer the last definition (Eq.
{eq}`eqn:J_Yamaguchi`) because it is approximately valid over the
whole coupling strength regime while the first equation implies the weak
coupling limit and the second the strong coupling limit.

In order to apply the broken symmetry formalism use:

```orca
%scf BrokenSym NA,NB
     end
```

The program will then go through a number of steps. Essentially it
computes an energy and wavefunction for the high-spin state, localizes
the orbitals and reconverges to the broken symmetry state.

:::{Caution}
Make sure that in your input coordinates "site A" is the site
that contains the larger number of unpaired electrons!
:::

Most often the formalism is applied to spin coupling in transition metal
complexes or metal-radical coupling or to the calculation of the
potential energy surfaces in the case of homolytic bond cleavage. In
general, hybrid DFT methods appear to give reasonable semiquantitative
results for the experimentally observed splittings.

As an example consider the following simple calculation of the
singlet--triplet splitting in a stretched Li$_{2}$ molecule:

```{literalinclude} ../../orca_working_input/C05S13_233.inp
:language: orca
```

There is a second mechanism for generating broken-symmetry solutions in
ORCA. This mechanism uses the individual spin densities and is invoked
with the keywords `FlipSpin` and `FinalMs`. The strategy is to exchange
the $\alpha$ and $\beta$ spin blocks of the density on certain
user-defined centers after converging the high-spin wavefunction. With
this method arbitrary spin topologies should be accessible. The use is
simple:

```{literalinclude} ../../orca_working_input/C05S13_234.inp
:language: orca
```

Finally, you may attempt to break the symmetry by using the SCF
stability analysis feature (see Section
{ref}`sec:essentialelements.stabilityanalysis`). The ground spin state
can be obtained by diagonalizing the above spin Hamiltonian through
**ORCA-ECA** utility (see
{ref}`sec:utilities.eca`).

## Approximate Spin Projection Method

The approximate spin projection (AP) method, proposed by Yamaguchi and
co-workers, is a technique to remove the spin contamination from
exchange coupling constants.{cite}`Yamaguchi1986,Yamaguchi1988,Saito2010`
In this scheme, the energy of a system is given by

$$
E_{\mathrm{AP} }=\alpha E_{\mathrm{BS} }-\left(\alpha - 1\right)E_{\mathrm{HS} }
$$ (eq_eap)

The parameter $\alpha$ is calculated as

$$
\alpha=\frac{S^{\mathrm{HS} }\left(S^{\mathrm{HS} }+1\right) - S_Z^{\mathrm{BS} }\left(S_Z^{\mathrm{BS} }+1\right)}{\langle\hat{\mathbf{S} }^2\rangle^{\mathrm{HS} }-\langle\hat{\mathbf{S} }^2\rangle^{\mathrm{BS} }}
$$ (alpha_yam)

Here, $S_Z^{\mathrm{BS} }$ is the $z$-component of the total spin for
the BS state ($S_Z^{\mathrm{BS} }=(N_{\alpha}-N_{\beta})/2$).
Alternatively, one can adopt Noodleman's scheme,{cite}`NoodlemanCP1986` where
$\alpha$ is calculated as follows

$$
\alpha=\frac{S^{\mathrm{HS} }\left(S^{\mathrm{HS} }+1\right) - S_Z^{\mathrm{BS} }\left(S_Z^{\mathrm{BS} }+1\right)}{\left(S^{\mathrm{HS} }\right)^2}
$$ (alpha_nood)

or Ruiz's scheme,{cite}`Ruiz_BS_1999` with $\alpha$ equal to

$$
\alpha=\frac{S^{\mathrm{HS} }\left(S^{\mathrm{HS} }+1\right) - S_Z^{\mathrm{BS} }\left(S_Z^{\mathrm{BS} }+1\right)}{S^{\mathrm{HS} }\left(S^{\mathrm{HS} }+1\right)}
$$ (alpha_ruiz)

The AP method is requested via the tag `APMethod` in the `%scf` block:

```orca
%scf BrokenSym NA,NB
     APMethod 3  # 1 = Noodleman
                 # 2 = Ruiz
                 # 3 = Yamaguchi
end
```

The default is `APMethod 0`, which corresponds to a normal BS
calculation. Yamaguchi's AP method is available for single point energy
calculations and geometry optimizations. If we run a geometry
optimization in the context of Yamaguchi's AP method, then, the gradient
of equation {eq}`eq_eap` w.r.t a nuclear displacement $X$ reads as

$$
\frac{\partial E_{\mathrm{AP} }}{\partial X}=\alpha\frac{\partial E_{\mathrm{BS} }}{\partial X}-\left(\alpha-1\right)\frac{\partial E_{\mathrm{HS} }}{\partial X}+\frac{\partial\alpha}{\partial X}\left(E_{\mathrm{BS} } - E_{\mathrm{HS} }\right)
$$ (der_alpha_yam)

The last term contains the derivative
$\frac{\partial\alpha}{\partial X}$. ORCA uses the formalism proposed by
Saito and Thiel, which involves solving the CP-SCF equations in each
geometry optimization cycle.{cite}`Saito2012` The cost of such a calculation
is higher than using Noodleman's or Ruiz's schemes, where
$\frac{\partial\alpha}{\partial X}=0$.

(sec:spectroscopyproperties.magnx.decompositionpath)=
# Decomposition of the Magnetic Exchange Coupling
```{index} Magnetic Exchange Coupling Decomposition
```

The Decomposition method ({cite}`DecompositionPath_2013,DecompositionPath_2015,DecompositionPath_2020,DecompositionPath_2023a`) aims to
extract the main physical contributions to the magnetic exchange coupling
$J_{ab}$ between two magnetic sites $A$ and $B$ based on successive relaxation of high-spin (HS) and broken symmetry determinants. The present implementation in ORCA refers to systems involving two magnetic centres and is based on the use of the Yamaguchi formula. For systems involving more centres, the Yamaguchi formula is invalid, and the decomposition implies a different strategy for which an input file generator to perform the decomposition with ORCA is available [here](https://gitlab.com/gdavid123/input-files-generator).({cite}`DecompositionPath_2023b,DecompositionPath_2024`) 

Based on the Heisenberg-Dirac-van Vleck Hamiltonian,

$$H_\text {HDvV} = -2J_{AB}\vec{S}_A\vec{S}_B$$

magnetic exchange coupling may be decomposed into three main physical contributions: i) the ferromagnetic direct exchange $J_0$  between the magnetic centres, ii) the antiferromagnetic kinetic exchange contribution $\Delta J_\text {KE}$ reflecting the relaxation 
of the magnetic centres in the low-spin state, and iii) the spin polarisation effects $\Delta J_\text {SP}$ which corresponds to the differential response of the core (non-magnetic) orbitals in the HS and BS determinants and which may be ferro- or antiferromagnetic, depending on the system. 

To extract these contributions from DFT or HF calculations, a set of starting orbital is obtained from an HS state calculation, either in the restricted open-shell formalism (HS.RO) or the quasi-restricted open-shell formalism (HS.qRO). This defines a set of doubly occupied molecular orbitals and a set of singly-occupied orbitals (SOMOs) according to the number of unpaired electrons. The SOMOs are then localised using by default the Pipek-Mezey method resulting in a set of localised magnetic orbitals. By flipping the spin of the electrons associated with one centre, a first BS determinant is obtained for which the energy is computed without optimising any orbital (BS.NOpt). Using the HS.RO and BS.NOpt determinants, the first direct exchange contribution may be calculated as,

$$J_0 = -\frac{E_\text{HS.RO}-E_\text{BS.NOpt} }{\left < S^{2} \right >_\text{HS.RO} - \left < S^{2} \right >_\text{BS.NOpt } }$$

Or with the HS.qRO,

$$J_0 = -\frac{E_\text{HS.qRO}-E_\text{BS.NOpt} }{\left < S^{2} \right >_\text{HS.qRO} - \left < S^{2} \right >_\text{BS.NOpt} }$$

To compute the second kinetic exchange contribution, from the BS.NOpt determinant, magnetic orbitals are relaxed in the field of the frozen core (non-magnetic) orbitals, resulting in a new BS frozen core determinant (BS.FC).  Using the BS.FC and HS.RO or HS.qRO determinants and retrieving the direct exchange contribution, the kinetic exchange may be computed,

$$\Delta J_\text{KE} = -\frac{E_\text{HS.(q)RO}-E_\text{BS.FC} }{\left < S^{2} \right >_\text{HS.(q)RO} - \left < S^{2} \right >_\text{BS.FC} } - J_0$$
The contribution from the spin polarisation effects is computed by allowing the relaxation of the core orbitals while keeping the magnetic orbitals frozen (FM) from the HS.RO/HS.qRO and the BS.NOpt determinants, resulting in the HS.FM and BS.FM determinants, respectively. Using these two new determinants and retrieving the direct exchange contribution, the spin polarisation effects may be evaluated as,

$$\Delta J_\text{SP} = -\frac{E_\text{HS.FM }-E_\text{BS.FM} }{\left < S^{2} \right >_\text{HS.(q)RO} - \left < S^{2} \right >_\text{BS.Nopt} } - J_0$$

In addition to the usual use of the Yamaguchi formula with fully relaxed HS and BS determinants, the magnetic exchange coupling may be evaluated by summing these three contributions up, the so-called Recomposition method,

$$ J_\Sigma = J_0 + \Delta J_\text{KE} + \Delta J_\text{SP}$$

In order to use the decomposition:

```orca
%scf DecompositionPath NA,NB
     end
```
with `NA` and `NB` the number of unpaired eletrons in the sites $A$ and $B$, respectively.
The program will then go through several steps to perform the decomposition as described above. To use the HS.RO as reference definition of the orbitals, HFTyp=ROHF must be used whilst, for HS.qRO, it must be HFTyp=UHF.

:::{Caution}
Make sure that in your input coordinates "site A" is the site
that contains the larger number of unpaired electrons!
:::
