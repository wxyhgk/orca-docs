```{index} PNO-EOM-CC, Excited States via PNO-CC
```

(sec:spectroscopyproperties.dleom)=
# Excited States via PNO-based coupled cluster

Despite the successes of the DLPNO-CC approximation for ground states, 
the use of PNOs for excited states has been less fruitful. Defining a 
PNO-based scheme for excited states that maintains the balance between 
speed and accuracy observed for ground states is not straightforward. 
As an intermediate solution, the basis for ground-state DLPNO quantities 
is transformed back to the canonical basis and used within the canonical 
EOM routine. This procedure is justified, as the main bottleneck of the 
EOM-CCSD or STEOM-CCSD methods lies in the ground-state calculation. 
Approximating the ground-state CCSD amplitudes with MP2 amplitudes is also 
possible, as done in the EOM-CCSD(2) approach. However, it is not reliable 
and can lead to large errors when the reference HF wave function does not 
provide a reasonable zeroth-order approximation to the ground-state wave 
function. Note that the back-transformed PNO scheme (bt-PNO) described here 
is available for both open-shell (UHF (QROs) or ROHF reference) and 
closed-shell (RHF reference) systems.

(sec:spectroscopyproperties.dleom.general)=
## General Description

The back-transformation of the ground-state DLPNO-CCSD amplitudes to the 
virtual space involves three steps. The amplitudes in the PNO basis are first 
converted to the PAO basis, then to the atomic orbital (AO) basis, and finally 
to the canonical MO basis[640]. For example, in the closed-shell case, we have

$$d_{\tilde{\mu}\tilde{a}_{ij} }^{ij}T^{ij}_{\tilde{a}_{ij}\tilde{b}_{ij} }d_{\tilde{b}_{ij}\tilde{\mu} }^{ij} \Rightarrow
L_{\mu\tilde{\mu} }^{ij}T^{ij}_{\tilde{\mu}\tilde{\nu} }L_{\tilde{\nu}\nu}^{ij} \Rightarrow
C_{a\mu }^{ij}T^{ij}_{\mu\nu}C_{\nu b}^{ij} \Rightarrow
T^{ij}_{ab},$$

$$d_{\tilde{\mu}\tilde{a}_{ii} }^{i}T^{i}_{\tilde{a}_{ii} } \Rightarrow
L_{\mu\tilde{\mu} }^{i}T^{i}_{\tilde{\mu} } \Rightarrow
C_{a\mu }^{i}T^{i}_{\mu} \Rightarrow
T^{i}_{a},$$

The AO basis functions are denoted as $\mu,\nu,\ldots$, while
$\tilde{\mu},\tilde{\nu},\ldots$ refers to PAOs. The missing pairs are
treated using MP2 amplitudes. If all the thresholds are set to zero, the
back-transformed amplitudes match exactly with the canonical RI-EOM-CCSD
ones. On the other hand, when all the thresholds are made infinitely
tight, one obtains the EOM-CCSD(2) results. This PNO-based excited state
approach is available for all the flavors of EOM-CCSD and for STEOM-CCSD
in both open- and closed-shell systems.

Below, we list all the parameters that influence the DLPNO-CCSD-based
excited state calculations

```orca
%mdci
#bt-PNO-EOM and STEOM parameters - defaults displayed
DoEOMMP2 true        # MP2 correction for missing pairs
DoRECAN  true        # recanonicalization of the occupied
                     # orbitals before the excited state calculation
                     #(only relevant for the RHF implementation)
end
```

(sec:spectroscopyproperties.dleom.energy)=
## Reference State Energy

It should be noted that the reference energy for PNO-based EOM-CCSD or 
STEOM-CCSD differs slightly from the energy printed for a converged ground-state 
DLPNO-CCSD calculation, as it includes perturbative corrections for various 
truncated quantities.

```
----------------------
COUPLED CLUSTER ENERGY
----------------------

E(0)                                       ...   -113.913498239
E(CORR)(strong-pairs)                      ...     -0.401457078
E(CORR)(weak-pairs)                        ...     -0.000339627
E(CORR)(corrected)                         ...     -0.401796705
E(TOT)                                     ...   -114.315294944
```

In the bt-PNO-EOM-CCSD scheme, the CI-like excited state treatment of
the reference state is defined by back-transformed DLPNO amplitudes (or
MP2 amplitudes for the weak pairs). The energy corresponding to this set
of amplitude is printed at the beginning of the EOM calculations.

```
Dressing integrals for EOM-CCSD            ... 
Reference state energy for EOM-DLPNO-CCSD     ...   -114.314954945

done (    0.4)
```

Therefore, to calculate the total energy of an excited (ionized or
electron attached) state, one needs to add the excitation energy to the
reference state energy in bt-PNO-EOM-CCSD.

(sec:spectroscopyproperties.dleom.localorbitals)=
## Use of Local Orbitals

The use of local orbitals makes it difficult to follow a particular guess 
vector during the Davidson diagonalization process in EOM-CC and STEOM-CC. 
Therefore, it is advisable to recanonicalize the occupied orbitals after 
the ground-state DLPNO-CCSD calculation by setting DoRECAN to true (this 
is only relevant for the closed-shell RHF implementation). It is important 
to note that recanonicalization does not affect the EOM-CCSD energies. 
However, STEOM-CC energies are not invariant to orbital rotations and may 
differ slightly between local and canonical orbitals. In the open-shell 
bt-PNO implementation, a different procedure is followed: all quantities 
are transformed to the delocalized basis before proceeding with the 
back-transformation and the excited-state calculation.

(sec:spectroscopyproperties.dleom.tips)=
## Some tips and tricks for bt-PNO calculations

-   The bt-PNO scheme with tightPNO settings gives results, which are
    within 0.01 eV of the canonical EOM-CCSD numbers, at a fraction of
    the computational cost{cite}`Dutta2016PNO`. So, use of bt-PNO scheme is
    always preferable over canonical calculations.

-   In the case of an RHF reference, one should set 'DLPNOLINEAR true'
    and 'NEWDOMAINS true' in the mdci block input to use the 2015 fully
    linear scaling implementation, which is more robust than the 2013
    implementation used as default in bt-PNO scheme.

-   The transition moment in bt-PNO-EOM (RHF only) and bt-PNO-STEOM
    (RHF, UHF (QROs) or ROHF) is only available using the linear
    approximation.
