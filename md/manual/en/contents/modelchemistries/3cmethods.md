```{index} DFT-3c
```

(sec:modelchemistries.3cmethods)=
# Composite Methods (3c methods)

Composite [HF](sec:essentialelements.hartreefock) and [DFT](../modelchemistries/DensityFunctionalTheory.md) 
methods utilize relatively small tailored [basis sets](../essentialelements/basisset.md) and special 
corrections to achieve high accuracies at a fraction of the computational cost of a
calculation approaching the basis set limit. The most prominent composite methods
are the so-called "3c" methods by Grimme and co-workers.

```{index} HF-3c
```

(sec:modelchemistries.3cmethods.hf3c)=
## HF-3c
HF-3c is a fast [Hartree-Fock](sec:essentialelements.hartreefock) based method developed for computation of
structures, vibrational frequencies and non-covalent interaction
energies in huge molecular systems {cite}`sure_hf3c`. The starting point for
evaluating the electronic energy is a standard HF calculation with a
small Gaussian AO basis set. The used so-called MINIX basis set consists
of different sets of basis functions for different groups of atoms as
shown in table {numref}`tab:modelchemistries.3cmethods.minix`. In ORCA, HF-3c is available for all elements up to Pu (Z = 94).

(tab:modelchemistries.3cmethods.minix)=
:::{table} Composition of the MINIX basis set.
| element    | basis                                |
|:-----------|:-------------------------------------|
| H-He, B-Ne | MINIS                                |
| Li-Be      | MINIS+1(p)                           |
| Na-Mg      | MINIS+1(p)                           |
| Al-Ar      | MINIS+1(d)                           |
| K-Zn       | SV                                   |
| Ga-Kr      | SVP                                  |
| Rb-Rn      | def2-SVP with def-ECPs               |
| Fr-Lr      | def-SVP with def-ECPs                |
:::

Three terms are added to correct the HF energy
$E_{\text{tot} }^{\text{HF/MINIX} }$ in order to include London
dispersion interactions, to account for the BSSE and to correct for
basis set deficiencies, i.e. overestimated bond lengths. The corrected
total energy is therefore calculated as

$$
  E_{\text{tot} }^{\text{HF-3c} } = E_{\text{tot} }^{\text{HF/MINIX} } + E_{\text{disp} }^{\text{D3(BJ) }} + E_{\text{BSSE} }^{\text{gCP} } + E_{\text{SRB} }.
$$ (eq:hf3c)

The first correction term $E_{\text{disp} }^{\text{D3(BJ) }}$ is the
atom-pair wise London dispersion energy from the [D3 dispersion correction](sec:modelchemistries.dispersioncorrections.dftd.theory) scheme{cite}`grimme2010chem` applying Becke-Johnson (BJ) damping
{cite}`becke2005chem,johnson2005chem,johnson2006chem` (see section
{ref}`sec:modelchemistries.dispersioncorrections.dftd.theory`). The second term
$E_{\text{BSSE} }^{\text{gCP} }$ denotes the [geometrical counterpoise (gCP) correction](sec:essentialelements.counterpoise.gcp) {cite}`KrusegCP` to treat the BSSE (see section
{ref}`sec:essentialelements.counterpoise.gcp`). For the HF-3c method, the
three usual D3 parameters $s_8$, $a_1$ and $a_2$ were re-fitted using
reference interaction energies of the complexes of the S66 test set
{cite}`resac2011chem`. This results in $s_8=0.8777$, $a_1=0.4171$ and
$a_2=2.9149$. The parameter $s_6$ was set to unity as usual to enforce
the correct asymptotic limit and the gCP correction was already applied
in this fitting step.

The last term $E_{\text{SRB} }$ is a short-ranged correction to deal
with basis set deficiencies which occur when using small or minimal
basis sets. It corrects for systematically overestimated covalent bond
lengths for electronegative elements and is calculated as a sum over all
atom pairs:

$$E_{\text{SRB} } = -s \sum_{A}^{\text{Atoms} } \sum_{B \neq A}^{\text{Atoms} }(Z_A Z_B)^{3/2}\exp(-\gamma (R_{AB}^{0,\text{D3} })^{3/4}
                 R_{AB})$$

Here, $R_{AB}^{0,\text{D3} }$ are the default cut-off radii as
determined *ab initio* for the D3 scheme {cite}`grimme2010chem` and $Z_A$,
$Z_B$ are the nuclear charges. This correction is applied for all
elements up to argon. The empirical fitting parameters $s=0.03$ and
$\gamma= 0.7$ were determined to produce vanishing HF-3c total atomic
forces for B3LYP-D3(BJ)/def2-TZVPP equilibrium structures of 107 small
organic molecules. More details can be found in the original publication
{cite}`sure_hf3c`.

The HF-3c method can only be invoked with a simple keyword:

```orca
! HF-3c
```

`! HF-3c` is a compound keyword and equals
`! HF MINIX D3BJ GCP(HF/MINIX) PATOM`, hence no basis set etc. has to be
specified. The `PATOM` guess is selected since the grid construction for
the default guess can take more time than an actual SCF step. The guess
can only be overwritten manually in the %method section.

The default mode for the integral handling is set to `Conventional`. The
storing of the two-electron integrals on disk or in memory if possible
leads to large computational savings. In case one want to use the
`Direct` mode, this has to be specified in the %scf input section:

```orca
%scf
  SCFmode Direct
end
```

The output gives the used parameters and the correction itself for D3
and gCP separately. As the SRB correction is also calculated with the
otool_gcp, the results are given in the gCP output section. The
`Total correction to HF/MINIX` is the sum of all three corrections (D3,
gCP and SRB) and `FINAL SINGLE POINT ENERGY` is the total HF-3c energy
as given in equation {eq}`eq:hf3c`.

```orca
-------------------------------------------------------------------------------
                          DFT DISPERSION CORRECTION

                                DFTD3 V2.1  Rev 6
                          USING Becke-Johnson damping
-------------------------------------------------------------------------------
The default Hartree-Fock  is recognized
Active option DFTDOPT                   ...         4

molecular C6(AA) [au] = 1689.256597


            DFT-D V3
 parameters
 using HF/MINIX parameters
 s6 scaling factor         :     1.0000
 a1 scaling factor         :     0.4171
 s8 scaling factor         :     0.8777
 a2 scaling factor         :     2.9149
 ad hoc parameters k1-k3   :    16.0000     1.3333    -4.0000

 Edisp/kcal,au: -32.163184627631  -0.051255291794
 E6   /kcal   : -18.007221978
 E8   /kcal   : -14.155962649
 % E8         :  44.012938437

-------------------------   ----------------
Dispersion correction            -0.051255292
-------------------------   ----------------


------------------------------------------------------------------------------

                  g C P  - geometrical counterpoise correction

------------------------------------------------------------------------------
Method:  hf/minix

Parameters:   sigma        eta         alpha        beta
              0.1290      1.1526      1.1549       1.1763
Egcp:       0.0723150636 a.u.
Ebas:      -0.0636976872 a.u.
------------------   -----------------
gCP+bas correction         0.008617376
------------------   -----------------
----------------------------   ----------------
Total correction to HF/MINIX       -0.042637915
----------------------------   ----------------


-------------------------   --------------------
FINAL SINGLE POINT ENERGY      -163.002895262171
-------------------------   --------------------
```

For the elements up to Xe, the default initial guess is a Hückel guess.
Beyond Xe, the guess mode is changed to `HCORE` since no Hückel
parameters for the respective ECP bases are available and other models
are not implemented at the moment. For calculations with only lighter
elements and therefore no ECPs, the ECP printouts in the output file can
be ignored.

```{index} B97-3c
```

(sec:modelchemistries.3cmethods.b973c)=
## B97-3c

B97-3c{cite}`grimme_b973c` is another composite DFT method designed for
thermochemistry, structures, and noncovalent interactions specifically
also for transition metal chemistry and other stronger correlated
systems. It is based on the B97 GGA including the [D3(BJ) dispersion correction](sec:modelchemistries.dispersioncorrections.dftd.theory) with
three-body contribution, a short range bond length correction, and a
modified, stripped-down triple-$\zeta$ basis termed def2-mTZVP, the
computational cost of this method is between that of HF-3c and 
[PBEh-3c](sec:modelchemistries.3cmethods.pbeh3c) (for large systems roughly two times more expensive
than [HF-3c](sec:modelchemistries.3cmethods.hf3c)). In ORCA, B97-3c is available for all elements up to Pu (Z = 94).

B97-3c can be invoked via simple input keyword:

```orca
! B97-3c
```

```{index} r²SCAN-3c
```

(sec:modelchemistries.3cmethods.r2scan3c)=
## $r^2$SCAN-3c

The $r^2$SCAN-3c composite method{cite}`grimme2020r2scan3c` is available as
robust "Swiss army knife" electronic structure method for
thermochemistry, geometries and non-covalent interactions and has shown
in preliminary tests consistent performance for both open and closed
shell transition metal complexes. It is based on the
$r^2$SCAN{cite}`furness2020r2scan` meta-GGA combined with the [D4 dispersion correction](sec:modelchemistries.dispersioncorrections.dftd.theory){cite}`ehlert2020r2scand4` and the 
[geometrical counter poise-correction](sec:essentialelements.counterpoise.gcp){cite}`KrusegCP`. The modified triple-$\zeta$ basis set,
def2-mTZVPP, is larger and more consistent for the light main-group
elements and almost as computationally efficient as the def2-mTZVP basis
set of [B97-3c](sec:modelchemistries.3cmethods.b973c). The computational cost of $r^2$SCAN-3c is slightly larger
than [B97-3c](sec:modelchemistries.3cmethods.b973c). In ORCA, $r^2$SCAN-3c is available for all elements up to Lr (Z = 103).
It is invoked with the simple keyword

```orca
! r2SCAN-3c
```

```{index} PBEh-3c
```

(sec:modelchemistries.3cmethods.pbeh3c)=
## PBEh-3c

PBEh-3c is a highly efficient electronic structure approach performing
particularly well in the optimization of geometries and for interaction
energies of non-covalent complexes.{cite}`grimme_pbeh3c` Here, a global
hybrid variant of the Perdew-Burke-Ernzerhof (PBE) functional with a
relatively large amount of non-local Fock-exchange (42%) is employed
with a valence-double-zeta Gaussian AO basis set (def2-mSVP). Basis set
superposition errors (BSSE) and London dispersion effects are accounted
for by the [gCP](sec:essentialelements.counterpoise.gcp) and [D3](sec:modelchemistries.dispersioncorrections.dftd.theory) schemes, respectively (see above). The basis set
is constructed such that:

(tab:modelchemistries.3cmethods.def2msvp)=
:::{table} Composition of the def2-mSVP basis set.
| element     | basis                                     |
|:------------|:------------------------------------------|
| H           | def2-SV(P) ($\alpha$ scaled by 1.2)       |
| He          | def2-SVP(-p)                              |
| Li-Be,Na-Kr | def2-SV(P)                                |
| B,Ne        | Ahlrichs' DZ + Polarization from def2-SVP |
| C-F         | Ahlrichs' DZ + Polarization from 6-31G\*  |
| Rb-Rn       | def2-SVP with def2 ECPs                   |
| Fr-Lr       | def-SVP with def-ECPs                     |
:::

For inter- and intramolecular BSSE the [gCP](sec:essentialelements.counterpoise.gcp) expression from
Eq. {eq}`eqn:gcp` is
used but with a damping function (similar to the zero-damping in
Eq. {eq}`eqn:modelchemistries.dispersioncorrections.dftd.theory.zero`).
This damping improves the thermochemistry of the method significantly
compared with the non-damped version. London dispersion effects are
accounted for by the [DFT-D3](sec:modelchemistries.dispersioncorrections.dftd.theory) (BJ-damping) scheme including the three-body
term. Compared to the related HF-3c approach, the PBEh-3c is somewhat
more costly, however, it yields much better geometries. These are
roughly of MP2-quality (or even better for non-covalent structures) but
may be computed at much lower cost. Due to the moderate amount of
non-local Fock exchange, the method is less prone to self-interaction
errors (as in GGAs) but still applicable in cases when Hartree-Fock
fails (strongly correlated systems). In ORCA, PBEh-3c is available for all elements up to Pu (Z = 94).

The PBEh-3c method may be invoked with the simple keyword:

```orca
! PBEh-3c
```

Identical to HF-3c, the default initial guess for all elements up to Xe
is a Hückel guess. Beyond Xe, the guess mode is changed to `HCORE`. For
calculations with only lighter elements and therefore no ECPs, the ECP
printouts in the output file can be ignored.

```{index} B3LYP-3c
```

(sec:modelchemistries.3cmethods.b3lyp3c)=
## B3LYP-3c

B3LYP-3c is a method combination introduced by Grimme and co-workers to efficiently calculate gas-phase infrared spectra.{cite}`grimme2020b3lyp3c`
It combines the standard B3LYP functional with the [D3(BJ)-ATM dispersion correction](sec:modelchemistries.dispersioncorrections.dftd.theory), a def2-mSVP basis set, and a [geometrical counterpoise correction](sec:essentialelements.counterpoise.gcp).
In ORCA, B3LYP-3c is available for all elements up to Pu (Z = 94). B3LYP-3c can be invoked via simple input keyword:

```orca
! B3LYP-3c
```
or it can be constructed manually from its components via:

```orca
!B3LYP D3BJ GCP(DFT/SV(P)) def2-mSVP ABC
```

```{index} ωB97X-3c
```

(sec:modelchemistries.3cmethods.wb97x3c)=
## $\omega$B97X-3c

The $\omega$B97X-3c composite method{cite}`grimme2022wb97x3c` is based on the
$\omega$B97X-V functional and combines a tailored and molecule-optimized
polarized valence double-$\zeta$ (vDZP) basis set and a specifically
adapted D4 dispersion correction. The vDZP basis set employs large-core
ECPs and shows only very small basis set superposition and
incompleteness errors compared to conventional double-$\zeta$ basis
sets. In thorough tests on standard benchmarks sets, the $\omega$B97X-3c
method was shown to be on par with well-performing hybrid DFT methods in
a quadruple-$\zeta$ basis set at a fraction of their computational cost.
$\omega$B97X-3c is consistently available for all elements up to Rn
(Z = 1--86).

It is invoked with the simple keyword:

```orca
! wB97X-3c
```

The vDZP basis set alone is utilized as follows (note that the
corresponding large-core ECPs are called automatically):

```orca
! vDZP
```

(sec:modelchemistries.3cmethods.keywords)=
## Keywords

(tab:modelchemistries.3cmethods.keywords.simple)=
:::{table} Simple input keywords for the 3c composite methods.
| Keyword                         | Description                                                                              |
|:--------------------------------|:-----------------------------------------------------------------------------------------|
| `HF-3C`                         | Invokes the [HF-3c](sec:modelchemistries.3cmethods.hf3c) method                          |
| `B97-3C`                        | Invokes the [B97-3c](sec:modelchemistries.3cmethods.b973c) method                        |
| `R2SCAN-3C`                     | Invokes the [$r^2$SCAN-3c](sec:modelchemistries.3cmethods.r2scan3c) method               |
| `PBEH-3C`                       | Invokes the [PBEh-3c](sec:modelchemistries.3cmethods.pbeh3c) method                      |
| `B3LYP-3C`                      | Invokes the [B3LYP-3c](sec:modelchemistries.3cmethods.b3lyp3c) method                    |
| `WB97X-3C`                      | Invokes the [$\omega$B97X-3c](sec:modelchemistries.3cmethods.wb97x3c) method             |
:::