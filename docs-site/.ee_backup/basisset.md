

<a id="sec:essentialelements.basisset"></a>
# Basis Sets

ORCA provides a large number of natively implemented [orbital](sec:essentialelements.basisset.builtin) and 
[auxiliary basis sets](sec:essentialelements.basisset.aux) alongside various [effective core potentials (ECPs)](sec:essentialelements.basisset.ecps) that
can be combined with them. For use with [scalar-relativistic methods like ZORA, DKH, or X2C](sec:essentialelements.relativistic), 
specialized [relativistic basis sets](sec:essentialelements.basisset.builtin.rel) are available as well. 
Furthermore, other basis sets can be [read from external files](sec:essentialelements.basisset.file). Most built-in basis
sets and ECPs were obtained from the Basis Set Exchange[bse2019](../../bibliography.md) or its predecessor, 
the EMSL library, and the input format in ORCA is closely related to the "GAMESS-US" format.

<a id="sec:essentialelements.basisset.basicusage"></a>
## Basic Usage

The easiest way to use orbital and auxiliary basis sets in ORCA is via the simple input keywords. All available orbital
basis set keywords can be found in [sec:essentialelements.basisset.builtin](#sec:essentialelements.basisset.builtin) and all auxiliary basis set options in
[sec:essentialelements.basisset.aux](#sec:essentialelements.basisset.aux). For example, the Karlsruhe def2-TZVP basis set can be invoked via
the `def2-TZVP` keyword.

```orca
! def2-TZVP
```

!!! note
    Some basis sets like the [Karlsruhe def2](sec:essentialelements.basisset.builtin.def2) employ 
    [ECPs](sec:essentialelements.basisset.ecps) by default for heavy elements, 
    in this case the `def2-ECP`. 
    The explicit control of the ECPs is described in [sec:essentialelements.basisset.ecps](#sec:essentialelements.basisset.ecps).

[Auxiliary basis sets](sec:essentialelements.basisset.aux) needed for 
[resolution-of-the-identity (RI)](sec:essentialelements.ri) can be defined in the same way. 
In this example, Weigend's universal `def2/J` auxiliary basis is used.

```orca
! def2-TZVP def2/J
```

!!! note
    Note that for many calculations, RI is activated by default (e.g. [RIJCOSX](sec:essentialelements.ri.rijcosx) for [hybrid DFT](sec:modelchemistries.dft.hybriddft)). 
    Accordingly, the `def2/J` auxiliary basis is automatically invoked by default as well if not otherwise specified.
    In scalar relativistic calculations, the default is `SARC/J` instead.

<a id="par:essentialelements.basisset.basicusage.aux"></a>
Note that there are three separate slots for auxiliary basis sets for RI: 
- `AuxJ` is the Coulomb-fitting basis for the [RI-J](sec:essentialelements.ri.rij), 
  [RIJDX/RIJONX](sec:essentialelements.ri.rijonx),
  and [RIJCOSX](sec:essentialelements.ri.rijcosx) approximations.
- `AuxJK` is the Coulomb- and exchange-fitting basis used for 
  [RI-JK](sec:essentialelements.ri.rijk).
- `AuxC` is used for RI-based integral generation steps in post-SCF 
  dynamical electron correlation methods,
  such as [RI-MP2](sec:modelchemistries.mp2.ri), 
  [DLPNO-MP2](sec:modelchemistries.mp2.dlpno), 
  and [DLPNO-CC](sec:modelchemistries.mdci.localcorrelation).

Finally, [F12 methods](sec:modelchemistries.mdci.expcorrelation) 
require a complementary auxiliary basis set (`CABS`),
in addition to the [specialized orbital basis](sec:essentialelements.basisset.builtin.f12)
(and possibly `AuxC`), for example:

```orca
! F12-RI-MP2 cc-pVDZ-F12 cc-pVDZ-F12-CABS cc-pVTZ-F12-MP2Fit
```

Specifying an auxiliary basis with the simple input keyword, assigns it to the corresponding slot.
However, each basis slot, as well as the ECP, can be assigned explicitly in the `%basis` block.
For example, a "/JK" basis may be assigned to `AuxJ` in this way.

```orca
%basis
  Basis "def2-TZVP"         # The orbital expansion basis set
  ECP   "def2-ECP"          # Effective core potential
  AuxJ  "def2/J"            # RI-J auxiliary basis set
  AuxJK "def2/JK"           # RI-JK auxiliary basis set
  AuxC  "def2-TZVP/C"       # Auxiliary basis set for correlated 
                            # calculations, e.g. RI-MP2
  CABS  "cc-pVDZ-F12-OptRI" # complementary auxiliary basis set 
                            # for F12 calculations
end
```

<a id="par:essentialelements.basisset.basicusage.decontract"></a>
If required, all basis sets can be decontracted via simple input (e.g. `! DECONTRACT`)
or the `%basis` block with the respective keywords below.
Note that if your basis set arises from general contraction,
it will contain duplicate primitives in several contractions.
These will be removed such that only unique primitives remain 
and there is no problem with redundancy.

```orca
%basis
  DecontractBas   false  # if chosen "true" the program will
                         # decontract the orbital basis set
  DecontractAuxJ  false  # if "true" - decontract the AuxJ basis set
  DecontractAuxJK false  # if "true" - decontract the AuxJK basis set
  DecontractAuxC  false  # if "true" - decontract the AuxC basis set
  DecontractCABS  true   # if "false" - do not decontract the CABS
  Decontract      false  # if "true" - decontract all basis sets
end
```

!!! tip
    - Generally, basis sets can be 
      [assigned to specific elements](sec:essentialelements.basisset.element), 
      to individual [atoms](sec:essentialelements.basisset.atom), 
      or even to [structural fragments](sec:essentialelements.basisset.fragments).
    - Any built-in basis can be exported via the [`orca_exportbasis` utility](sec:utilities.exportbasis).
    - References for the built-in basis sets are usually printed at the start of the ORCA output,
      as well as by `orca_exportbasis`.

!!! warning
    ORCA uses pure d and f functions (5D and 7F instead of Cartesian 6D and 10F) for all basis sets. 
    This needs to be taken into account when results are compared with other programs, 
    especially for Pople-style basis sets that were optimized with Cartesian (6D) functions.

<a id="sec:essentialelements.basisset.builtin"></a>
## Orbital Basis Sets

In the following, we will give an outline of natively implemented basis sets from various families,
like the [Karlsruhe def2](sec:essentialelements.basisset.builtin.def2) 
and [correlation consistent](sec:essentialelements.basisset.builtin.cc) basis sets,
and list which elements are covered by each.
If an [ECP](sec:essentialelements.basisset.ecps) is necessary for heavy elements, 
it is documented in the respective table entries and invoked by default 
if the basis is selected in the simple input or via the `basis` keyword in the `%basis` block.

<a id="sec:essentialelements.basisset.builtin.pople"></a>
### Pople Basis Sets

Various basis sets of the Pople basis set family are available in ORCA. A list of all available Pople-style basis sets is given in
[tab:essentialelements.basisset.builtin.pople](#tab:essentialelements.basisset.builtin.pople).

!!! note "Naming Convention of Pople Basis Sets"
    :class: note
    * \* or (d) adds one set of first polarization functions on all atoms except H
    * \*\* or (d,p) adds one set of first polarization functions on all atoms
    * Further combinations: (2d), (2df), (2d,p), (2d,2p), (2df,2p), (2df,2pd)
    * $+$ before "G" includes diffuse functions on all atoms except H (e.g. 6-31$+$G)
    * $++$ before "G" includes diffuse functions on all atoms. Works only when H polarization is already included, e.g. 6-31$++$G(d,p)

<a id="tab:essentialelements.basisset.builtin.pople"></a>
!!! note "Available Pople-style basis sets."
    :header-rows: 1
    :class: longtable
    :class: footnotesize

| Item | Value |
| --- | --- |
| **Basis Set** | — |

      - Elem.
      - ECP
      - Comment

| Item | Value |
| --- | --- |
| **`STO-3G`** | — |

      - H--I
      - \--
      - Minimal basis set

| Item | Value |
| --- | --- |
| **`3-21G`** | — |

      - H--Cs
      - \--
      - 

| Item | Value |
| --- | --- |
| **`3-21GSP`** | — |

      - H--Ar
      - \--
      - 

| Item | Value |
| --- | --- |
| **`4-22GSP`** | — |

      - H--Ar
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-31G`** | — |

      - H--Zn
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-31G*`** | — |

      - H--Kr
      - \--
      - 

| Item | Value |
| --- | --- |
| **`m6-31G`** | — |

      - Sc--Cu
      - \--
      - Modified 6-31G for 3d transition metals (Sc--Cu)

| Item | Value |
| --- | --- |
| **`m6-31G*`** | — |

      - Sc--Cu
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-31G**`** | — |

      - H--Zn
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-31G(d)`** | — |

      - H--Zn
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-31G(d,p)`** | — |

      - H--Zn
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-31G(2d)`** | — |

      - H--Zn
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-31G(2d,p)`** | — |

      - H--Zn
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-31G(2d,2p)`** | — |

      - H--Zn
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-31G(2df)`** | — |

      - H--Zn
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-31G(2df,2p)`** | — |

      - H--Zn
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-31G(2df,2pd)`** | — |

      - H--Zn
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-31+G*`** | — |

      - H--Kr
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-31+G**`** | — |

      - H--Zn
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-31+G(d)`** | — |

      - H--Zn
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-31+G(d,p)`** | — |

      - H--Zn
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-31+G(2d)`** | — |

      - H--Zn
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-31+G(2d,p)`** | — |

      - H--Zn
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-31+G(2d,2p)`** | — |

      - H--Zn
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-31+G(2df)`** | — |

      - H--Zn
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-31+G(2df,2p)`** | — |

      - H--Zn
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-31+G(2df,2pd)`** | — |

      - H--Zn
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-31++G**`** | — |

      - H--Zn
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-31++G(d,p)`** | — |

      - H--Zn
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-31++G(2d,p)`** | — |

      - H--Zn
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-31++G(2d,2p)`** | — |

      - H--Zn
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-31++G(2df,2p)`** | — |

      - H--Zn
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-31++G(2df,2pd)`** | — |

      - H--Zn
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-311G`** | — |

      - H--Br
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-311G*`** | — |

      - H--Br
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-311G**`** | — |

      - H--Br
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-311G(d)`** | — |

      - H--Br
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-311G(d,p)`** | — |

      - H--Br
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-311G(2d)`** | — |

      - H--Br
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-311G(2d,p)`** | — |

      - H--Br
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-311G(2d,2p)`** | — |

      - H--Br
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-311G(2df)`** | — |

      - H--Br
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-311G(2df,2p)`** | — |

      - H--Br
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-311G(2df,2pd)`** | — |

      - H--Br
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-311G(3df)`** | — |

      - H--Br
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-311G(3df,3pd)`** | — |

      - H--Br
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-311+G*`** | — |

      - H--Br
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-311+G**`** | — |

      - H--Br
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-311+G(d)`** | — |

      - H--Br
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-311+G(d,p)`** | — |

      - H--Br
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-311+G(2d)`** | — |

      - H--Br
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-311+G(2d,p)`** | — |

      - H--Br
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-311+G(2d,2p)`** | — |

      - H--Br
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-311+G(2df)`** | — |

      - H--Br
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-311+G(2df,2p)`** | — |

      - H--Br
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-311+G(2df,2pd)`** | — |

      - H--Br
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-311+G(3df)`** | — |

      - H--Br
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-311+G(3df,2p)`** | — |

      - H--Br
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-311+G(3df,3pd)`** | — |

      - H--Br
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-311++G**`** | — |

      - H--Br
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-311++G(d,p)`** | — |

      - H--Br
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-311++G(2d,p)`** | — |

      - H--Br
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-311++G(2d,2p)`** | — |

      - H--Br
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-311++G(2df,2p)`** | — |

      - H--Br
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-311++G(2df,2pd)`** | — |

      - H--Br
      - \--
      - 

| Item | Value |
| --- | --- |
| **`6-311++G(3df,3pd)`** | — |

      - H--Br
      - \--
      - 

<a id="sec:essentialelements.basisset.builtin.ahlrichs"></a>
### Ahlrichs Basis Sets

The older Ahlrichs basis sets implemented in ORCA cover all-electron basis sets and the basis sets automatically employing the def-ECP for all elements beyond Rb.
A list of available Ahlrichs basis sets is given in [tab:essentialelements.basisset.builtin.ahlrichs](#tab:essentialelements.basisset.builtin.ahlrichs). Relativistically recontracted variants are shown in
[sec:essentialelements.basisset.builtin.rel.ahlrichs](#sec:essentialelements.basisset.builtin.rel.ahlrichs).

!!! note
    Past versions of ORCA (ORCA <4.0) used to load all-electron basis sets also for elements Rb-I with the below keywords for double- and triple-$\zeta$ basis sets. The Rb-I basis sets originated from non-relativistic all-electron basis sets of the Turbomole library (such as "TZVPAlls"). **This automatic substitution is now deprecated**. However, we offer temporarily the ability to reproduce that behavior by adding the prefix "old-" to the below keywords, e.g. `old-TZVP`.

<a id="tab:essentialelements.basisset.builtin.ahlrichs"></a>
!!! note "Available all-electron Ahrlichs basis sets."
    :header-rows: 1
    :class: longtable
    :class: footnotesize

| Item | Value |
| --- | --- |
| **Basis Set** | — |

      - Elem.
      - ECP
      - Comment

| Item | Value |
| --- | --- |
| **`SV`** | — |

      - H--Kr
      - \--
      - Valence double-zeta basis set.

| Item | Value |
| --- | --- |
| **`SV(P)`** | — |

      - H--Kr
      - \--
      - Valence double-zeta with polarization only on heavy elements.

| Item | Value |
| --- | --- |
| **`SVP`** | — |

      - H--Kr
      - \--
      - Polarized valence double-zeta basis set.

| Item | Value |
| --- | --- |
| **`TZV`** | — |

      - H--Kr
      - \--
      - Valence triple-zeta basis set.

| Item | Value |
| --- | --- |
| **`TZV(P)`** | — |

      - H--Kr
      - \--
      - Valence triple-zeta with polarization on heavy elements.

| Item | Value |
| --- | --- |
| **`TZVP`** | — |

      - H--Kr
      - \--
      - Polarized valence triple-zeta basis set.

| Item | Value |
| --- | --- |
| **`TZVPP`** | — |

      - H--Kr
      - \--
      - Doubly polarized triple-zeta basis set.

| Item | Value |
| --- | --- |
| **`QZVP`** | — |

      - H--Kr
      - \--
      - Polarized valence quadruple-zeta basis set.

| Item | Value |
| --- | --- |
| **`QZVPP`** | — |

      - H--Kr
      - \--
      - Doubly polarized quadruple-zeta basis set.

| Item | Value |
| --- | --- |
| **`def-SV(P)`** | — |

      - H--Lr
      - `def-ECP` (Rb--Lr)
      - Valence double-zeta with polarization only on heavy elements.

| Item | Value |
| --- | --- |
| **`def-SVP`** | — |

      - H--Lr
      - `def-ECP` (Rb--Lr)
      - Polarized valence double-zeta basis set.

| Item | Value |
| --- | --- |
| **`def-TZVP`** | — |

      - H--Lr
      - `def-ECP` (Rb--Lr)
      - Valence triple-zeta basis set with polarization functions.

| Item | Value |
| --- | --- |
| **`def-TZVPP`** | — |

      - H--Lr
      - `def-ECP` (Rb--Lr)
      - Doubly polarized triple-zeta basis set.

| Item | Value |
| --- | --- |
| ***Minimally augmented* (scheme by Truhlar et al.[Zheng:2010iz](../../bibliography.md))** | — |
| **`ma-def-TZVP`** | — |

      - Fr--Lr
      - `def-ECP` (Fr--Lr)
      - Minimally augmented def-TZVP basis set.

| Item | Value |
| --- | --- |
| ***Legacy definitions (not recommended!)*** | — |
| **`old-SV`** | — |

      - H--I
      - \--
      - 

| Item | Value |
| --- | --- |
| **`old-SV(P)`** | — |

      - H--I
      - \--
      - 

| Item | Value |
| --- | --- |
| **`old-SVP`** | — |

      - H--I
      - \--
      - 

| Item | Value |
| --- | --- |
| **`old-TZV`** | — |

      - H--I
      - \--
      - 

| Item | Value |
| --- | --- |
| **`old-TZV(P)`** | — |

      - H--I
      - \--
      - 

| Item | Value |
| --- | --- |
| **`old-TZVP`** | — |

      - H--I
      - \--
      - 

| Item | Value |
| --- | --- |
| **`old-TZVPP`** | — |

      - H--I
      - \--
      - 

<a id="sec:essentialelements.basisset.builtin.def2"></a>
### Karlsruhe def2 Basis Sets

The valence polarized basis sets of the Karlsruhe def2 family are all-electron for elements **H-Kr**, and automatically load Stuttgart-Dresden 
[effective core potentials](sec:essentialelements.basisset.ecps) for elements **Rb-Rn**. A list of available Karlsruhe def2 basis sets is given in
[tab:essentialelements.basisset.builtin.def2](#tab:essentialelements.basisset.builtin.def2). Relativistically recontracted variants are discussed in [sec:essentialelements.basisset.builtin.rel.def2](#sec:essentialelements.basisset.builtin.rel.def2).

<a id="tab:essentialelements.basisset.builtin.def2"></a>
!!! note "Available Karlsruhe def2 basis sets."
    :header-rows: 1
    :class: longtable
    :class: footnotesize

| Item | Value |
| --- | --- |
| **Basis Set** | — |

      - Elem.
      - ECP
      - Comment

| Item | Value |
| --- | --- |
| **`def2-SVP`** | — |

      - H--Rn
      - `def2-ECP` (Rb--Rn)
      - Polarized valence double-$\zeta$.

| Item | Value |
| --- | --- |
| **`def2-SV(P)`** | — |

      - H--Rn
      - `def2-ECP` (Rb--Rn)
      - `def2-SVP` with slightly reduced polarization.

| Item | Value |
| --- | --- |
| **`def2-TZVP`** | — |

      - H--Rn
      - `def2-ECP` (Rb--Rn)
      - Polarized valence triple-$\zeta$. Quite similar to the older def-TZVPP for main group elements and TZVP for H.

| Item | Value |
| --- | --- |
| **`def2-TZVP(-f)`** | — |

      - H--Rn
      - `def2-ECP` (Rb--Rn)
      - `def2-TZVP` with f polarization removed from main group elements.

| Item | Value |
| --- | --- |
| **`def2-TZVPP`** | — |

      - H--Rn
      - `def2-ECP` (Rb--Rn)
      - Doubly polarized valence triple-$\zeta$.

| Item | Value |
| --- | --- |
| **`def2-QZVP`** | — |

      - H--Rn
      - `def2-ECP` (Rb--Rn)
      - Polarized valence quadruple-$\zeta$.

| Item | Value |
| --- | --- |
| **`def2-QZVPP`** | — |

      - H--Rn
      - `def2-ECP` (Rb--Rn)
      - Doubly polarized valence quadruple-$\zeta$.

| Item | Value |
| --- | --- |
| ***Diffuse* (Rappoport et al.[Rappoport:2010kr,Rappoport:2021ln](../../bibliography.md))** | — |
| **`def2-SVPD`** | — |

      - H--Rn
      - `def2-ECP` (Rb--Rn)
      - Diffuse def2-SVP basis set for property calculations

| Item | Value |
| --- | --- |
| **`def2-TZVPD`** | — |

      - H--Rn
      - `def2-ECP` (Rb--Rn)
      - Diffuse def2-TZVP basis set for property calculations

| Item | Value |
| --- | --- |
| **`def2-TZVPPD`** | — |

      - H--Rn
      - `def2-ECP` (Rb--Rn)
      - Diffuse def2-TZVPP basis set for property calculations

| Item | Value |
| --- | --- |
| **`def2-QZVPD`** | — |

      - H--Rn
      - `def2-ECP` (Rb--Rn)
      - Diffuse def2-QZVP basis set for property calculations

| Item | Value |
| --- | --- |
| **`def2-QZVPPD`** | — |

      - H--Rn
      - `def2-ECP` (Rb--Rn)
      - Diffuse def2-QZVPP basis set for property calculations

| Item | Value |
| --- | --- |
| ***Minimally augmented* (scheme by Truhlar et al.[Zheng:2010iz](../../bibliography.md))** | — |
| **`ma-def2-SVP`** | — |

      - H--Rn
      - `def2-ECP` (Rb--Rn)
      - Minimally augmented def2-SVP basis set.

| Item | Value |
| --- | --- |
| **`ma-def2-SV(P)`** | — |

      - H--Rn
      - `def2-ECP` (Rb--Rn)
      - Minimally augmented def2-SV(P) basis set.

| Item | Value |
| --- | --- |
| **`ma-def2-mSVP`** | — |

      - H--Rn
      - `def2-ECP` (Rb--Rn)
      - Minimally augmented def2-mSVP basis set.

| Item | Value |
| --- | --- |
| **`ma-def2-TZVP`** | — |

      - H--Rn
      - `def2-ECP` (Rb--Rn)
      - Minimally augmented def2-TZVP basis set.

| Item | Value |
| --- | --- |
| **`ma-def2-TZVP(-f)`** | — |

      - H--Rn
      - `def2-ECP` (Rb--Rn)
      - Minimally augmented def2-TZVP(-f) basis set.

| Item | Value |
| --- | --- |
| **`ma-def2-TZVPP`** | — |

      - H--Rn
      - `def2-ECP` (Rb--Rn)
      - Minimally augmented def2-TZVPP basis set.

| Item | Value |
| --- | --- |
| **`ma-def2-QZVPP`** | — |

      - H--Rn
      - `def2-ECP` (Rb--Rn)
      - Minimally augmented def2-QZVPP basis set.

<a id="sec:essentialelements.basisset.builtin.dhf"></a>
### Karlsruhe dhf Basis Sets
These basis sets are derived from the def2-XVP ones with small modifications for 5s, 6s, 4d, and 5d elements and iodine.[Weigend2010-dhf-XVP](../../bibliography.md)
They are optimized for the revised Dirac-Fock ECPs (`dhf-ECP`) as opposed to the Wood--Boring ones (`def2-ECP`).
For elements H--Kr these basis sets are equivalent to the respective [def2-XVP](sec:essentialelements.basisset.builtin.def2) basis set.
Versions for two-component methods are also available, e.g. `dhf-TZVP-2c`, **however, such methods are currently not implemented in ORCA**. 
A list of available Karlsruhe dhf basis sets is given in [tab:essentialelements.basisset.builtin.dhf](#tab:essentialelements.basisset.builtin.dhf).

<a id="tab:essentialelements.basisset.builtin.dhf"></a>
!!! note "Available dhf basis sets."
    :header-rows: 1
    :class: longtable
    :class: footnotesize

| Item | Value |
| --- | --- |
| **Basis Set** | — |

      - Elem.
      - ECP
      - Comment

| Item | Value |
| --- | --- |
| **`dhf-SV(P)`** | — |

      - H--Rn
      - `dhf-ECP` (Rb--Rn)
      - based on def2-SV(P)

| Item | Value |
| --- | --- |
| **`dhf-SVP`** | — |

      - H--Rn
      - `dhf-ECP` (Rb--Rn)
      - based on def2-SVP

| Item | Value |
| --- | --- |
| **`dhf-TZVP`** | — |

      - H--Rn
      - `dhf-ECP` (Rb--Rn)
      - based on def2-TZVP

| Item | Value |
| --- | --- |
| **`dhf-TZVPP`** | — |

      - H--Rn
      - `dhf-ECP` (Rb--Rn)
      - based on def2-TZVPP

| Item | Value |
| --- | --- |
| **`dhf-QZVP`** | — |

      - H--Rn
      - `dhf-ECP` (Rb--Rn)
      - based on def2-QZVP

| Item | Value |
| --- | --- |
| **`dhf-QZVPP`** | — |

      - H--Rn
      - `dhf-ECP` (Rb--Rn)
      - based on def2-QZVPP

| Item | Value |
| --- | --- |
| ***Two-component variants:*** | — |
| **`dhf-SVP-2c`** | — |

      - H--Rn
      - `dhf-ECP-2c` (Rb--Rn)
      - based on def2-SVP

| Item | Value |
| --- | --- |
| **`dhf-TZVP-2c`** | — |

      - H--Rn
      - `dhf-ECP-2c` (Rb--Rn)
      - based on def2-TZVP

| Item | Value |
| --- | --- |
| **`dhf-TZVPP-2c`** | — |

      - H--Rn
      - `dhf-ECP-2c` (Rb--Rn)
      - based on def2-TZVPP

| Item | Value |
| --- | --- |
| **`dhf-QZVP-2c`** | — |

      - H--Rn
      - `dhf-ECP-2c` (Rb--Rn)
      - based on def2-QZVP

| Item | Value |
| --- | --- |
| **`dhf-QZVPP-2c`** | — |

      - H--Rn
      - `dhf-ECP-2c` (Rb--Rn)
      - based on def2-QZVPP

<a id="sec:essentialelements.basisset.builtin.jensen"></a>
### Jensen Basis Sets

Jensen's polarization-consistent generally contracted basis sets include various general purpose and sepcialized variants. A list of available Jensen
basis sets is given in [tab:essentialelements.basisset.builtin.jensen](#tab:essentialelements.basisset.builtin.jensen).[jensen2001a, jensen2002a, jensen2004a, jensen2007a, jensen2012a, jensen2014a, jensen2015a](../../bibliography.md)

<a id="tab:essentialelements.basisset.builtin.jensen"></a>
!!! note "Available Jensen basis sets."
    :header-rows: 1
    :class: longtable
    :class: footnotesize

| Item | Value |
| --- | --- |
| **Basis Set** | — |

      - Elem.
      - ECP
      - Comment

| Item | Value |
| --- | --- |
| **`pc-0`** | — |

      - H--Ca, Ga--Kr
      - \--
      -

| Item | Value |
| --- | --- |
| **`pc-1`** | — |

      - H--Kr
      - \--
      - 

| Item | Value |
| --- | --- |
| **`pc-2`** | — |

      - H--Kr
      - \--
      - 

| Item | Value |
| --- | --- |
| **`pc-3`** | — |

      - H--Kr
      - \--
      - 

| Item | Value |
| --- | --- |
| **`pc-4`** | — |

      - H--Kr
      - \--
      - 

| Item | Value |
| --- | --- |
| **`aug-pc-0`** | — |

      - H--Ca, Ga--Kr
      - \--
      - `pc-0` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`aug-pc-1`** | — |

      - H--Kr
      - \--
      - `pc-1` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`aug-pc-2`** | — |

      - H--Kr
      - \--
      - `pc-2` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`aug-pc-3`** | — |

      - H--Kr
      - \--
      - `pc-3` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`aug-pc-4`** | — |

      - H--Kr
      - \--
      - `pc-4` augmented by diffuse functions

| Item | Value |
| --- | --- |
| ***Segmented contraction variants:*** | — |
| **`pcseg-0`** | — |

      - H--Kr
      - \--
      - 

| Item | Value |
| --- | --- |
| **`pcseg-1`** | — |

      - H--Kr
      - \--
      - 

| Item | Value |
| --- | --- |
| **`pcseg-2`** | — |

      - H--Kr
      - \--
      - 

| Item | Value |
| --- | --- |
| **`pcseg-3`** | — |

      - H--Kr
      - \--
      - 

| Item | Value |
| --- | --- |
| **`pcseg-4`** | — |

      - H--Kr
      - \--
      - 

| Item | Value |
| --- | --- |
| **`aug-pcseg-0`** | — |

      - H--Kr
      - \--
      - `pcseg-0` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`aug-pcseg-1`** | — |

      - H--Kr
      - \--
      - `pcseg-1` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`aug-pcseg-2`** | — |

      - H--Kr
      - \--
      - `pcseg-2` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`aug-pcseg-3`** | — |

      - H--Kr
      - \--
      - `pcseg-3` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`aug-pcseg-4`** | — |

      - H--Kr
      - \--
      - `pcseg-4` augmented by diffuse functions

| Item | Value |
| --- | --- |
| ***Optimized for nuclear magnetic shieldings:*** | — |
| **`pcSseg-0`** | — |

      - H--Kr
      - \--
      - 

| Item | Value |
| --- | --- |
| **`pcSseg-1`** | — |

      - H--Kr
      - \--
      - 

| Item | Value |
| --- | --- |
| **`pcSseg-2`** | — |

      - H--Kr
      - \--
      - 

| Item | Value |
| --- | --- |
| **`pcSseg-3`** | — |

      - H--Kr
      - \--
      - 

| Item | Value |
| --- | --- |
| **`pcSseg-4`** | — |

      - H--Kr
      - \--
      - 

| Item | Value |
| --- | --- |
| **`aug-pcSseg-0`** | — |

      - H--Kr
      - \--
      - `pcSseg-0` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`aug-pcSseg-1`** | — |

      - H--Kr
      - \--
      - `pcSseg-1` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`aug-pcSseg-2`** | — |

      - H--Kr
      - \--
      - `pcSseg-2` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`aug-pcSseg-3`** | — |

      - H--Kr
      - \--
      - `pcSseg-3` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`aug-pcSseg-4`** | — |

      - H--Kr
      - \--
      - `pcSseg-4` augmented by diffuse functions

| Item | Value |
| --- | --- |
| ***Optimized for spin-spin coupling constants:*** | — |
| **`pcJ-0`** | — |

      - H--He, B--Ne, Al--Ar
      - \--
      - 

| Item | Value |
| --- | --- |
| **`pcJ-1`** | — |

      - H--He, B--Ne, Al--Ar
      - \--
      - 

| Item | Value |
| --- | --- |
| **`pcJ-2`** | — |

      - H--He, B--Ne, Al--Ar
      - \--
      - 

| Item | Value |
| --- | --- |
| **`pcJ-3`** | — |

      - H--He, B--Ne, Al--Ar
      - \--
      - 

| Item | Value |
| --- | --- |
| **`pcJ-4`** | — |

      - H--He, B--Ne, Al--Ar
      - \--
      - 

| Item | Value |
| --- | --- |
| **`aug-pcJ-0`** | — |

      - H--He, B--Ne, Al--Ar
      - \--
      - `pcJ-0` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`aug-pcJ-1`** | — |

      - H--He, B--Ne, Al--Ar
      - \--
      - `pcJ-1` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`aug-pcJ-2`** | — |

      - H--He, B--Ne, Al--Ar
      - \--
      - `pcJ-2` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`aug-pcJ-3`** | — |

      - H--He, B--Ne, Al--Ar
      - \--
      - `pcJ-3` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`aug-pcJ-4`** | — |

      - H--He, B--Ne, Al--Ar
      - \--
      - `pcJ-4` augmented by diffuse functions

| Item | Value |
| --- | --- |
| ***Optimized for hyperfine coupling constants:*** | — |
| **`pcH-1`** | — |

      - H, He, B--Ne, Al--Ar
      - \--
      - 

| Item | Value |
| --- | --- |
| **`pcH-2`** | — |

      - H, He, B--Ne, Al--Ar
      - \--
      - 

| Item | Value |
| --- | --- |
| **`pcH-3`** | — |

      - H, He, B--Ne, Al--Ar
      - \--
      - 

| Item | Value |
| --- | --- |
| **`pcH-4`** | — |

      - H, He, B--Ne, Al--Ar
      - \--
      - 

| Item | Value |
| --- | --- |
| **`aug-pcH-1`** | — |

      - H, He, B--Ne, Al--Ar
      - \--
      - `pcH-1` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`aug-pcH-2`** | — |

      - H, He, B--Ne, Al--Ar
      - \--
      - `pcH-2` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`aug-pcH-3`** | — |

      - H, He, B--Ne, Al--Ar
      - \--
      - `pcH-3` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`aug-pcH-4`** | — |

      - H, He, B--Ne, Al--Ar
      - \--
      - `pcH-4` augmented by diffuse functions

| Item | Value |
| --- | --- |
| ***Optimized for core-spectroscopy:*** | — |
| **`pcX-1`** | — |

      - Li--Ar
      - \--
      - 

| Item | Value |
| --- | --- |
| **`pcX-2`** | — |

      - Li--Ar
      - \--
      - 

| Item | Value |
| --- | --- |
| **`pcX-3`** | — |

      - Li--Ar
      - \--
      - 

| Item | Value |
| --- | --- |
| **`pcX-4`** | — |

      - Li--Ar
      - \--
      - 

| Item | Value |
| --- | --- |
| **`aug-pcX-1`** | — |

      - Li--Ar
      - \--
      - `pcX-1` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`aug-pcX-2`** | — |

      - Li--Ar
      - \--
      - `pcX-2` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`aug-pcX-3`** | — |

      - Li--Ar
      - \--
      - `pcX-3` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`aug-pcX-4`** | — |

      - Li--Ar
      - \--
      - `pcX-4` augmented by diffuse functions

<a id="sec:essentialelements.basisset.builtin.hgbs"></a>
### Hydrogenic Gaussian Basis Sets

Lehtolas hydrogenic Gaussian basis sets (HGBS) were constructed as widely transferable and accurate basis sets based on one-electron model 
systems imitating real atoms and molecules.[lehtola2020hgbs](../../bibliography.md) A list of available HGBS basis sets is given in [tab:essentialelements.basisset.builtin.hgbs](#tab:essentialelements.basisset.builtin.hgbs).

!!! note "Naming convention of HGBS basis sets"
    :class: note
    * $m$: represents the energy optimization threshold $10^{-m}$
    * P$n$: represents the number of polarization shells
    * $A$: indicates explicit augmentation by diffuse functions

<a id="tab:essentialelements.basisset.builtin.hgbs"></a>
!!! note "Karlsruhe HGBS, HGBSP, AHGBS, and AHGBSP basis sets."
    :header-rows: 1
    :class: longtable
    :class: footnotesize

| Item | Value |
| --- | --- |
| **Basis Set** | — |

      - Elem.
      - ECP
      - Comment

| Item | Value |
| --- | --- |
| **`HGBS-5`** | — |

      - H--Og
      - \--
      - 

| Item | Value |
| --- | --- |
| **`HGBS-7`** | — |

      - H--Og
      - \--
      - 

| Item | Value |
| --- | --- |
| **`HGBS-9`** | — |

      - H--Og
      - \--
      - 

| Item | Value |
| --- | --- |
| **`HGBSP1-5`** | — |

      - H--Og
      - \--
      - {rspan}`8` Polarized variant

| Item | Value |
| --- | --- |
| **`HGBSP1-7`** | — |

      - H--Og
      - \--

| Item | Value |
| --- | --- |
| **`HGBSP1-9`** | — |

      - H--Og
      - \--

| Item | Value |
| --- | --- |
| **`HGBSP2-5`** | — |

      - H--Og
      - \--

| Item | Value |
| --- | --- |
| **`HGBSP2-7`** | — |

      - H--Og
      - \--

| Item | Value |
| --- | --- |
| **`HGBSP2-9`** | — |

      - H--Og
      - \--

| Item | Value |
| --- | --- |
| **`HGBSP3-5`** | — |

      - H--Og
      - \--

| Item | Value |
| --- | --- |
| **`HGBSP3-7`** | — |

      - H--Og
      - \--

| Item | Value |
| --- | --- |
| **`HGBSP3-9`** | — |

      - H--Og
      - \--

| Item | Value |
| --- | --- |
| **`AHGBS-5`** | — |

      - H--Og
      - \--
      - {rspan}`2` Augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`AHGBS-7`** | — |

      - H--Og
      - \--

| Item | Value |
| --- | --- |
| **`AHGBS-9`** | — |

      - H--Og
      - \--

| Item | Value |
| --- | --- |
| **`AHGBSP1-5`** | — |

      - H--Og
      - \--
      - {rspan}`8` Polarized variant augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`AHGBSP1-7`** | — |

      - H--Og
      - \--

| Item | Value |
| --- | --- |
| **`AHGBSP1-9`** | — |

      - H--Og
      - \--

| Item | Value |
| --- | --- |
| **`AHGBSP2-5`** | — |

      - H--Og
      - \--

| Item | Value |
| --- | --- |
| **`AHGBSP2-7`** | — |

      - H--Og
      - \--

| Item | Value |
| --- | --- |
| **`AHGBSP2-9`** | — |

      - H--Og
      - \--

| Item | Value |
| --- | --- |
| **`AHGBSP3-5`** | — |

      - H--Og
      - \--

| Item | Value |
| --- | --- |
| **`AHGBSP3-7`** | — |

      - H--Og
      - \--

| Item | Value |
| --- | --- |
| **`AHGBSP3-9`** | — |

      - H--Og
      - \--

<a id="sec:essentialelements.basisset.builtin.sapporo"></a>
### Sapporo Basis Sets

The Sapporo basis set family, named after the city of Sapporo, Japan, comprises segmented contracted all-electron Gaussian basis sets up to quadruple-$\zeta$ quality.[yamamoto1992sapporo,  noro2003sapporo, noro2012sapporo](../../bibliography.md)
They were developed as compact yet accurate basis sets focusing on calculations with correlated wavefunction methods. Variants optimized for the scalar-relativistic DKH3 Hamiltonian
are also available. A list of available Sapporo basis sets is given in [tab:essentialelements.basisset.builtin.sapporo](#tab:essentialelements.basisset.builtin.sapporo). Relativistic variants are discussed in [sec:essentialelements.basisset.builtin.rel.sapporo](#sec:essentialelements.basisset.builtin.rel.sapporo).

<a id="tab:essentialelements.basisset.builtin.sapporo"></a>
!!! note "List of available Sapporo basis sets."
    :header-rows: 1
    :class: longtable
    :class: footnotesize

| Item | Value |
| --- | --- |
| **Basis Set** | — |

      - Elem.
      - ECP
      - Comment

| Item | Value |
| --- | --- |
| **`Sapporo-DZP-2012`** | — |

      - H--Xe
      - \--
      - 

| Item | Value |
| --- | --- |
| **`Sapporo-TZP-2012`** | — |

      - H--Xe
      - \--
      -

| Item | Value |
| --- | --- |
| **`Sapporo-QZP-2012`** | — |

      - H--Xe
      - \--
      - 

<a id="sec:essentialelements.basisset.builtin.partridge"></a>
### Partridge Basis Sets

The basis sets of the Partridge family are uncontracted RHF groundstate energy-optimized.[partridge1987chem, partridge1989chem](../../bibliography.md) A list of available Partridge basis sets is given in
[tab:essentialelements.basisset.builtin.partridge](#tab:essentialelements.basisset.builtin.partridge).

<a id="tab:essentialelements.basisset.builtin.partridge"></a>
!!! note "AvailablePartridge basis sets."
    :header-rows: 1
    :class: longtable
    :class: footnotesize

| Item | Value |
| --- | --- |
| **Basis Set** | — |

      - Elem.
      - ECP
      - Comment

| Item | Value |
| --- | --- |
| **`Partridge-1`** | — |

      - H, Li--Sr
      - \--
      - 

| Item | Value |
| --- | --- |
| **`Partridge-2`** | — |

      - H, Li--Kr
      - \--
      - 

| Item | Value |
| --- | --- |
| **`Partridge-3`** | — |

      - H, Li--Zn
      - \--
      - 

| Item | Value |
| --- | --- |
| **`Partridge-4`** | — |

      - Sc--Zn
      - \--
      - 

<a id="sec:essentialelements.basisset.builtin.crenb"></a>
### CRENB Basis Sets

The Christiansen-Ross-Ermler-Nash-Bursten (CRENB) basis sets and [effective core potentials](sec:essentialelements.basisset.ecps) are available for
most elements.[pacios1985crenbla, hurley1986crenblb, lajohn1987crenblc, ross1990crenbld, ross1994crenble, ermler1991crenblf, nash1997crenblg](../../bibliography.md)
Note that while the ECPs were originally designed for spin-orbit coupling (SOC) interactions, 
**SOC calculations with ECPs are currently not implemented in ORCA**.
A list of availble CRENB basis sets is given in [tab:essentialelements.basisset.builtin.crenb](#tab:essentialelements.basisset.builtin.crenb).

<a id="tab:essentialelements.basisset.builtin.crenb"></a>
!!! note "List of available CRENB basis sets."
    :header-rows: 1
    :class: longtable
    :class: footnotesize

| Item | Value |
| --- | --- |
| **Basis Set** | — |

      - Elem.
      - ECP
      - Comment

| Item | Value |
| --- | --- |
| **`CRENBL`** | — |

      - H, Li--Og
      - `CRENBL-ECP` (Li--Og)
      - *Large* basis version for use with *small*-core ECP

<a id="sec:essentialelements.basisset.builtin.lanl"></a>
### LANL Basis Sets

The Los Alamos National Laboratory (LANL) basis sets and [effective core potentials](sec:essentialelements.basisset.ecps) were originally introduced in 1985 by Hay and Wadt.[hay1985chem, wadt1985ecp, hay1985ecpb](../../bibliography.md) Later polarized variants were proposed[ehlers1993lanlf, check2001lanldp](../../bibliography.md) and the basis sets were extended by Roy et al.[roy2008chem](../../bibliography.md).
A list of available LANL basis sets is given in [tab:essentialelements.basisset.builtin.lanl](#tab:essentialelements.basisset.builtin.lanl).

<a id="tab:essentialelements.basisset.builtin.lanl"></a>
!!! note "List of available LANL basis sets."
    :header-rows: 1
    :class: longtable
    :class: footnotesize

| Item | Value |
| --- | --- |
| **Basis Set** | — |

      - Elem.
      - ECP
      - Comment

| Item | Value |
| --- | --- |
| **`LANL08`** | — |

      - Na--La, Hf--Bi
      - `HayWadt` (Na--La, Hf--Bi)
      - uncontracted

| Item | Value |
| --- | --- |
| **`LANL08(f)`** | — |

      - Sc--Cu, Y--Ag, La, Hf--Au
      - `HayWadt` (Sc--Cu, Y--Ag, La, Hf--Au)
      - uncontracted + polarization

| Item | Value |
| --- | --- |
| **`LANL2DZ`** | — |

      - H, Li--La, Hf--Bi, U--Pu
      - `HayWadt` (Na--La, Hf--Bi, U--Pu)
      - double-$\zeta$, D95V for H--Ne

| Item | Value |
| --- | --- |
| **`LANL2TZ`** | — |

      - Sc--Zn, Y--Cd, La, Hf--Hg
      - `HayWadt` (Sc--Zn, Y--Cd, La, Hf--Hg)
      - triple-$\zeta$

| Item | Value |
| --- | --- |
| **`LANL2TZ(f)`** | — |

      - Sc--Cu, Y--Ag, La, Hf--Au
      - `HayWadt` (Sc--Cu, Y--Ag, La, Hf--Au)
      - triple-$\zeta$ + polarization

<a id="sec:essentialelements.basisset.builtin.cc"></a>
### Correlation-consistent Basis Sets

The correlation-consistent basis sets were pioneered by Dunning and co-workers
and manifold variants have been developed since. 
They are among the most widely used for application with correlated wave-function methods 
and are particularly suited for [basis set extrapolation](sec:modelchemistries.mdci.basissetextrapolation).
A list of available correlation-consisten basis sets is 
given in [tab:essentialelements.basisset.builtin.cc](#tab:essentialelements.basisset.builtin.cc). 
Relativistic variants are discussed in [sec:essentialelements.basisset.builtin.rel.cc](#sec:essentialelements.basisset.builtin.rel.cc).

<a id="tab:essentialelements.basisset.builtin.cc"></a>
!!! note "List of available correlation-consistent basis sets."
    :header-rows: 1
    :class: longtable
    :class: footnotesize

| Item | Value |
| --- | --- |
| **Basis Set** | — |

      - Elem.
      - ECP
      - Comment

| Item | Value |
| --- | --- |
| **`cc-pVDZ`** | — |

      - H--Ar, Ca--Kr
      - \--
      - Dunning correlation-consistent polarized double-$\zeta$

| Item | Value |
| --- | --- |
| **`cc-pVTZ`** | — |

      - H--Ar, Ca--Kr, Y, Ag, Au
      - \--
      - Dunning correlation-consistent polarized triple-$\zeta$

| Item | Value |
| --- | --- |
| **`cc-pVQZ`** | — |

      - H--Ar, Ca--Kr
      - \--
      - Dunning correlation-consistent polarized quadruple-$\zeta$

| Item | Value |
| --- | --- |
| **`cc-pV5Z`** | — |

      - H--Ar, Ca--Kr
      - \--
      - Dunning correlation-consistent polarized quintuple-$\zeta$

| Item | Value |
| --- | --- |
| **`cc-pV6Z`** | — |

      - H--He, Be--Ne, Al--Ar
      - \--
      - Dunning correlation-consistent polarized sextuple-$\zeta$

| Item | Value |
| --- | --- |
| **`aug-cc-pVDZ`** | — |

      - H--Ar, Sc--Kr
      - \--
      - `cc-pVDZ` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`aug-cc-pVTZ`** | — |

      - H--Ar, Sc--Kr, Ag, Au
      - \--
      - `cc-pVTZ` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`aug-cc-pVQZ`** | — |

      - H--Ar, Sc--Kr
      - \--
      - `cc-pVQZ` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`aug-cc-pV5Z`** | — |

      - H--Ar, Sc--Kr
      - \--
      - `cc-pV5Z` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`aug-cc-pV6Z`** | — |

      - H--He, B--Ne, Al--Ar
      - \--
      - `cc-pV6Z` augmented by diffuse functions

| Item | Value |
| --- | --- |
| ***With tight d functions:*** | — |
| **`cc-pVD(+d)Z`** | — |

      - Na--Ar
      - \--
      - 

| Item | Value |
| --- | --- |
| **`cc-pVT(+d)Z`** | — |

      - Na--Ar
      - \--
      - 

| Item | Value |
| --- | --- |
| **`cc-pVQ(+d)Z`** | — |

      - Na--Ar
      - \--
      - 

| Item | Value |
| --- | --- |
| **`cc-pV5(+d)Z`** | — |

      - Na--Ar
      - \--
      - 

| Item | Value |
| --- | --- |
| **`aug-cc-pVD(+d)Z`** | — |

      - Al--Ar
      - \--
      - `cc-pVD(+d)Z` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`aug-cc-pVT(+d)Z`** | — |

      - Al--Ar
      - \--
      - `cc-pVT(+d)Z` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`aug-cc-pVQ(+d)Z`** | — |

      - Al--Ar
      - \--
      - `cc-pVQ(+d)Z` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`aug-cc-pV5(+d)Z`** | — |

      - Al--Ar
      - \--
      - `cc-pV5(+d)Z` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`aug-cc-pV6(+d)Z`** | — |

      - Al--Ar
      - \--
      - `cc-pV6(+d)Z` augmented by diffuse functions

| Item | Value |
| --- | --- |
| ***Partially augmented according to Truhlar et al.[papajak2011](../../bibliography.md):*** | — |
| **`apr-cc-pV(Q+d)Z`** | — |

      - H--Ar
      - \--
      - Augmented with sp diffuse functions on Li--Ca

| Item | Value |
| --- | --- |
| **`may-cc-pV(T+d)Z`** | — |

      - H--Ar
      - \--
      - Augmented with sp diffuse functions on Li--Ca

| Item | Value |
| --- | --- |
| **`may-cc-pV(Q+d)Z`** | — |

      - H--Ar
      - \--
      - Augmented with spd diffuse functions on Li--Ca

| Item | Value |
| --- | --- |
| **`jun-cc-pV(D+d)Z`** | — |

      - H--Ar
      - \--
      - Augmented with sp diffuse functions on Li--Ca

| Item | Value |
| --- | --- |
| **`jun-cc-pV(T+d)Z`** | — |

      - H--Ar
      - \--
      - Augmented with spd diffuse functions on Li--Ca

| Item | Value |
| --- | --- |
| **`jun-cc-pV(Q+d)Z`** | — |

      - H--Ar
      - \--
      - Augmented with spdf diffuse functions on Li--Ca

| Item | Value |
| --- | --- |
| **`jul-cc-pV(D+d)Z`** | — |

      - H--Ar
      - \--
      - Augmented with spd diffuse functions on Li--Ca

| Item | Value |
| --- | --- |
| **`jul-cc-pV(T+d)Z`** | — |

      - H--Ar
      - \--
      - Augmented with spdf diffuse functions on Li--Ca

| Item | Value |
| --- | --- |
| **`jul-cc-pV(Q+d)Z`** | — |

      - H--Ar
      - \--
      - Augmented with spdfg diffuse functions on Li--Ca

| Item | Value |
| --- | --- |
| **`maug-cc-pV(D+d)Z`** | — |

      - H--Ar
      - \--
      - Equals `jun-cc-pV(D+d)Z`

| Item | Value |
| --- | --- |
| **`maug-cc-pV(T+d)Z`** | — |

      - H--Ar
      - \--
      - Equals `may-cc-pV(T+d)Z`

| Item | Value |
| --- | --- |
| **`maug-cc-pV(Q+d)Z`** | — |

      - H--Ar
      - \--
      - Equals `apr-cc-pV(Q+d)Z`

| Item | Value |
| --- | --- |
| ***Core-polarized for core-valence electron correlation:*** | — |
| **`cc-pCVDZ`** | — |

      - H--Ar, Ca, Ga--Kr
      - \--
      - Equals `cc-pVDZ` for H and He

| Item | Value |
| --- | --- |
| **`cc-pCVTZ`** | — |

      - H--Ar, Ca, Ga--Kr
      - \--
      - Equals `cc-pVTZ` for H and He

| Item | Value |
| --- | --- |
| **`cc-pCVQZ`** | — |

      - H--Ar, Ca, Ga--Kr
      - \--
      - Equals `cc-pVQZ` for H and He

| Item | Value |
| --- | --- |
| **`cc-pCV5Z`** | — |

      - H--Ar, Ca, Ga--Kr
      - \--
      - Equals `cc-pV5Z` for H and He

| Item | Value |
| --- | --- |
| **`cc-pCV6Z`** | — |

      - H--He, B--Ne, Al--Ar
      - \--
      - Equals `cc-pV6Z` for H and He

| Item | Value |
| --- | --- |
| **`aug-cc-pCVDZ`** | — |

      - H--Ar, Ga--Kr
      - \--
      - `cc-pCVDZ` augmented by diffuse functions, equals `aug-cc-pVDZ` for H and He

| Item | Value |
| --- | --- |
| **`aug-cc-pCVTZ`** | — |

      - H--Ar, Ga--Kr
      - \--
      - `cc-pCVTZ` augmented by diffuse functions, equals `aug-cc-pVTZ` for H and He

| Item | Value |
| --- | --- |
| **`aug-cc-pCVQZ`** | — |

      - H--Ar, Ga--Kr
      - \--
      - `cc-pCVQZ` augmented by diffuse functions, equals `aug-cc-pVQZ` for H and He

| Item | Value |
| --- | --- |
| **`aug-cc-pCV5Z`** | — |

      - H--Ar, Ga--Kr
      - \--
      - `cc-pCV5Z` augmented by diffuse functions, equals `aug-cc-pV5Z` for H and He

| Item | Value |
| --- | --- |
| **`aug-cc-pCV6Z`** | — |

      - H--He, B--Ne, Al--Ar
      - \--
      - `cc-pCV6Z` augmented by diffuse functions, equals `aug-cc-pV6Z` for H and He

| Item | Value |
| --- | --- |
| ***Core-polarized with weighted core functions*** | — |
| **`cc-pwCVDZ`** | — |

      - H--Ar, Ca, Ga--Kr
      - \--
      - Equals `cc-pVDZ` for H and He

| Item | Value |
| --- | --- |
| **`cc-pwCVTZ`** | — |

      - H--Ar, Ca--Kr, Ag, Au
      - \--
      - Equals `cc-pVTZ` for H and He

| Item | Value |
| --- | --- |
| **`cc-pwCVQZ`** | — |

      - H--Ar, Ca--Kr
      - \--
      - Equals `cc-pVQZ` for H and He

| Item | Value |
| --- | --- |
| **`cc-pwCV5Z`** | — |

      - H--Ar, Ca--Kr
      - \--
      - Equals `cc-pV5Z` for H and He

| Item | Value |
| --- | --- |
| **`aug-cc-pwCVDZ`** | — |

      - H--Ar, Ga--Kr
      - \--
      - `cc-pwCVDZ` augmented by diffuse functions, equals `aug-cc-pVDZ` for H and He

| Item | Value |
| --- | --- |
| **`aug-cc-pwCVTZ`** | — |

      - H--Ar, Sc--Kr, Ag, Au
      - \--
      - `cc-pwCVTZ` augmented by diffuse functions, equals `aug-cc-pVTZ` for H and He

| Item | Value |
| --- | --- |
| **`aug-cc-pwCVQZ`** | — |

      - H--Ar, Sc--Kr
      - \--
      - `cc-pwCVQZ` augmented by diffuse functions, equals `aug-cc-pVQZ` for H and He

| Item | Value |
| --- | --- |
| **`aug-cc-pwCV5Z`** | — |

      - H--Ar, Sc--Kr
      - \--
      - `cc-pwCV5Z` augmented by diffuse functions, equals `aug-cc-pV5Z` for H and He

| Item | Value |
| --- | --- |
| ***Pseudo-potential (ECP) variants:*** | — |
| **`cc-pVDZ-PP`** | — |

      - Ca, Cu--Kr, Sr--Xe, Ba, Hf--Rn, Ra, U
      - `SK-MCDHF-RSC` (Ca, Cu--Kr, Sr--Xe, Ba, Hf--Ra, U)
      - 

| Item | Value |
| --- | --- |
| **`cc-pVTZ-PP`** | — |

      - Ca, Cu--Kr, Sr--Xe, Ba, Hf--Rn, Ra, U
      - `SK-MCDHF-RSC` (Ca, Cu--Kr, Sr--Xe, Ba, Hf--Ra, U)
      - 

| Item | Value |
| --- | --- |
| **`cc-pVQZ-PP`** | — |

      - Ca, Cu--Kr, Sr--Xe, Ba, Hf--Rn, Ra, U
      - `SK-MCDHF-RSC` (Ca, Cu--Kr, Sr--Xe, Ba, Hf--Ra, U)
      - 

| Item | Value |
| --- | --- |
| **`cc-pV5Z-PP`** | — |

      - Ca, Cu--Kr, Sr--Xe, Ba, Hf--Rn, Ra
      - `SK-MCDHF-RSC` (Ca, Cu--Kr, Sr--Xe, Ba, Hf--Ra, U)
      - 

| Item | Value |
| --- | --- |
| **`aug-cc-pVDZ-PP`** | — |

      - Ca, Cu--Kr, Sr--Xe, Ba, Hf--Rn, Ra
      - `SK-MCDHF-RSC` (Ca, Cu--Kr, Sr--Xe, Ba, Hf--Ra, U)
      - `cc-pVDZ-PP` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`aug-cc-pVTZ-PP`** | — |

      - Ca, Cu--Kr, Sr--Xe, Ba, Hf--Rn, Ra
      - `SK-MCDHF-RSC` (Ca, Cu--Kr, Sr--Xe, Ba, Hf--Ra, U)
      - `cc-pVTZ-PP` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`aug-cc-pVQZ-PP`** | — |

      - Ca, Cu--Kr, Sr--Xe, Ba, Hf--Rn, Ra
      - `SK-MCDHF-RSC` (Ca, Cu--Kr, Sr--Xe, Ba, Hf--Ra, U)
      - `cc-pVQZ-PP` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`aug-cc-pV5Z-PP`** | — |

      - Ca, Cu--Kr, Sr--Xe, Ba, Hf--Rn, Ra
      - `SK-MCDHF-RSC` (Ca, Cu--Kr, Sr--Xe, Ba, Hf--Ra, U)
      - `cc-pV5Z-PP` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`cc-pCVDZ-PP`** | — |

      - Ca, Sr, Ba, Ra
      - `SK-MCDHF-RSC` (Ca, Sr, Ba, Ra)
      - 

| Item | Value |
| --- | --- |
| **`cc-pCVTZ-PP`** | — |

      - Ca, Sr, Ba, Ra
      - `SK-MCDHF-RSC` (Ca, Sr, Ba, Ra)
      - 

| Item | Value |
| --- | --- |
| **`cc-pCVQZ-PP`** | — |

      - Ca, Sr, Ba, Ra
      - `SK-MCDHF-RSC` (Ca, Sr, Ba, Ra)
      - 

| Item | Value |
| --- | --- |
| **`cc-pCV5Z-PP`** | — |

      - Ca, Sr, Ba, Ra
      - `SK-MCDHF-RSC` (Ca, Sr, Ba, Ra)
      - 

| Item | Value |
| --- | --- |
| **`aug-cc-pCVDZ-PP`** | — |

      - Ca, Sr, Ba, Ra
      - `SK-MCDHF-RSC` (Ca, Sr, Ba, Ra)
      - `cc-pCVDZ-PP` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`aug-cc-pCVTZ-PP`** | — |

      - Ca, Sr, Ba, Ra
      - `SK-MCDHF-RSC` (Ca, Sr, Ba, Ra)
      - `cc-pCVTZ-PP` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`aug-cc-pCVQZ-PP`** | — |

      - Ca, Sr, Ba, Ra
      - `SK-MCDHF-RSC` (Ca, Sr, Ba, Ra)
      - `cc-pCVQZ-PP` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`aug-cc-pCV5Z-PP`** | — |

      - Ca, Sr, Ba, Ra
      - `SK-MCDHF-RSC` (Ca, Sr, Ba, Ra)
      - `cc-pCV5Z-PP` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`cc-pwCVDZ-PP`** | — |

      - Ca, Cu--Kr, Sr--Xe, Ba, Hf--Rn, Ra, U
      - `SK-MCDHF-RSC` (Ca, Cu--Kr, Sr--Xe, Ba, Hf--Ra, U)
      - 

| Item | Value |
| --- | --- |
| **`cc-pwCVTZ-PP`** | — |

      - Ca, Cu--Kr, Sr--Xe, Ba, Hf--Rn, Ra, U
      - `SK-MCDHF-RSC` (Ca, Cu--Kr, Sr--Xe, Ba, Hf--Ra, U)
      - 

| Item | Value |
| --- | --- |
| **`cc-pwCVQZ-PP`** | — |

      - Ca, Cu--Kr, Sr--Xe, Ba, Hf--Rn, Ra, U
      - `SK-MCDHF-RSC` (Ca, Cu--Kr, Sr--Xe, Ba, Hf--Ra, U)
      - 

| Item | Value |
| --- | --- |
| **`cc-pwCV5Z-PP`** | — |

      - Ca, Cu--Kr, Sr--Xe, Ba, Hf--Rn, Ra
      - `SK-MCDHF-RSC` (Ca, Cu--Kr, Sr--Xe, Ba, Hf--Ra, U)
      - 

| Item | Value |
| --- | --- |
| **`aug-cc-pwCVDZ-PP`** | — |

      - Ca, Cu--Kr, Sr--Xe, Ba, Hf--Rn, Ra
      - `SK-MCDHF-RSC` (Ca, Cu--Kr, Sr--Xe, Ba, Hf--Ra, U)
      - `cc-pwCVDZ-PP` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`aug-cc-pwCVTZ-PP`** | — |

      - Ca, Cu--Kr, Sr--Xe, Ba, Hf--Rn, Ra
      - `SK-MCDHF-RSC` (Ca, Cu--Kr, Sr--Xe, Ba, Hf--Ra, U)
      - `cc-pwCVTZ-PP` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`aug-cc-pwCVQZ-PP`** | — |

      - Ca, Cu--Kr, Sr--Xe, Ba, Hf--Rn, Ra
      - `SK-MCDHF-RSC` (Ca, Cu--Kr, Sr--Xe, Ba, Hf--Ra, U)
      - `cc-pwCVQZ-PP` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`aug-cc-pwCV5Z-PP`** | — |

      - Ca, Cu--Kr, Sr--Xe, Ba, Hf--Rn, Ra
      - `SK-MCDHF-RSC` (Ca, Cu--Kr, Sr--Xe, Ba, Hf--Ra, U)
      - `cc-pwCV5Z-PP` augmented by diffuse functions

| Item | Value |
| --- | --- |
| ***Optimized for hyperfine coupling constants:*** | — |
| **`aug-cc-pVTZ-J`** | — |

      - H, B--F, Al--Cl, Sc--Zn, Se
      - \--
      - Sauer's basis set for accurate hyperfine coupling

| Item | Value |
| --- | --- |
| ***W4 theory:*** | — |
| **`haV(T+d)Z`** | — |

      - H--Ar
      - \--
      - `cc-pVTZ` (H--Be, Na, Mg), `aug-cc-pVTZ` (B--Ne), `aug-cc-pVT(+d)Z` (Al--Ar)

| Item | Value |
| --- | --- |
| **`haV(Q+d)Z`** | — |

      - H--Ar
      - \--
      - `cc-pVQZ` (H--Be, Na, Mg), `aug-cc-pVQZ` (B--Ne), `aug-cc-pVQ(+d)Z` (Al--Ar)

| Item | Value |
| --- | --- |
| **`haV(5+d)Z`** | — |

      - H--Ar
      - \--
      - `cc-pV5Z` (H--Be, Na, Mg), `aug-cc-pV5Z` (B--Ne), `aug-cc-pV5(+d)Z` (Al--Ar)

<a id="sec:essentialelements.basisset.builtin.f12"></a>
### F12 Basis Sets

Special orbital basis sets for [F12 calculations](sec:modelchemistries.mdci.expcorrelation) (larger than the regular D, T, Q-zeta basis sets!). 
A list of available F12 basis sets is given in [tab:essentialelements.basisset.builtin.f12](#tab:essentialelements.basisset.builtin.f12).
See [tab:essentialelements.basisset.aux.cabs](#tab:essentialelements.basisset.aux.cabs) for the necessary complementary auxiliary basis sets (CABS).

<a id="tab:essentialelements.basisset.builtin.f12"></a>
!!! note "F12 basis sets."
    :header-rows: 1
    :class: longtable
    :class: footnotesize

| Item | Value |
| --- | --- |
| **Basis Set** | — |

      - Elem.
      - ECP
      - Comment

| Item | Value |
| --- | --- |
| **`cc-pVDZ-F12`** | — |

      - H--Ar
      - \--
      - 

| Item | Value |
| --- | --- |
| **`cc-pVTZ-F12`** | — |

      - H--Ar
      - \--
      - 

| Item | Value |
| --- | --- |
| **`cc-pVQZ-F12`** | — |

      - H--Ar
      - \--
      - 

| Item | Value |
| --- | --- |
| ***Core-polarized:*** | — |
| **`cc-pCVDZ-F12`** | — |

      - Li--Ar
      - \--
      - 

| Item | Value |
| --- | --- |
| **`cc-pCVTZ-F12`** | — |

      - Li--Ar
      - \--
      - 

| Item | Value |
| --- | --- |
| **`cc-pCVQZ-F12`** | — |

      - Li--Ar
      - \--
      - 

| Item | Value |
| --- | --- |
| ***Pseudo-potential (ECP) variants:*** | — |
| **`cc-pVDZ-PP-F12`** | — |

      - Ga--Kr, In--Xe, Tl--Rn
      - `SK-MCDHF-RSC` (Ga--Kr, In--Xe, Tl--Rn)
      - 

| Item | Value |
| --- | --- |
| **`cc-pVTZ-PP-F12`** | — |

      - Ga--Kr, In--Xe, Tl--Rn
      - `SK-MCDHF-RSC` (Ga--Kr, In--Xe, Tl--Rn)
      - 

| Item | Value |
| --- | --- |
| **`cc-pVQZ-PP-F12`** | — |

      - Ga--Kr, In--Xe, Tl--Rn
      - `SK-MCDHF-RSC` (Ga--Kr, In--Xe, Tl--Rn)
      - 

<a id="sec:essentialelements.basisset.builtin.ano"></a>
### Atomic Natural Orbital Basis Sets

Atomic natural orbitals are a special class of basis sets. They are represented by the orthonormal set of orbitals that diagonalizes a spherically symmetric, correlated atomic density. The idea is to put as much information as possible into each basis functions such that one obtains the best possible result with the given number of basis functions. This is particularly important for correlated calculations where the number of primitives is less an issue than the number of basis functions. ORCA features some ANO basis sets on the basis of the cc-pV6Z (or pc-4 where missing) basis set primitives.[neese2011jctc](../../bibliography.md) These are very accurate and significantly better than the cc-pV$n$Z counterparts for the same number of basis functions (but much larger number of primitives). A list of available ANO basis sets is given in [tab:essentialelements.basisset.builtin.ano](#tab:essentialelements.basisset.builtin.ano).

!!! note
    * **aug-ANO-pV$n$Z:** full augmentation with spd, spdf,
    spdfg set of polarization functions. Almost as expensive as the next
    higher basis set. In fact, aug-ANO-pV$n$Z $=$ ANO-pV($n+1$)Z with the
    highest angular momentum polarization function deleted.
    * **saug-ANO-pV$n$Z:** augmentation with a single set of sp
    functions. Greatly enhances the accuracy of the SCF energies but not for
    correlation energies.

<a id="tab:essentialelements.basisset.builtin.ano"></a>
!!! note "Available atomic natural orbital (ANO) basis sets."
    :header-rows: 1
    :class: longtable
    :class: footnotesize

| Item | Value |
| --- | --- |
| **Basis Set** | — |

      - Elem.
      - ECP
      - Comment

| Item | Value |
| --- | --- |
| **`ANO-SZ`** | — |

      - H--Ar, Sc--Zn
      - \--
      - 

| Item | Value |
| --- | --- |
| **`ANO-pVDZ`** | — |

      - H--Ar, Sc--Zn
      - \--
      - 

| Item | Value |
| --- | --- |
| **`ANO-pVTZ`** | — |

      - H--Ar, Sc--Zn
      - \--
      - 

| Item | Value |
| --- | --- |
| **`ANO-pVQZ`** | — |

      - H--Ar, Sc--Zn
      - \--
      - 

| Item | Value |
| --- | --- |
| **`ANO-pV5Z`** | — |

      - H--Ar, Sc--Zn
      - \--
      - 

| Item | Value |
| --- | --- |
| **`ANO-pV6Z`** | — |

      - H--Ar, Sc--Zn
      - \--
      - 

| Item | Value |
| --- | --- |
| **`aug-ANO-pVDZ`** | — |

      - H--Ar, Sc--Zn
      - \--
      - `ANO-pVDZ` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`aug-ANO-pVTZ`** | — |

      - H--Ar, Sc--Zn
      - \--
      - `ANO-pVTZ` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`aug-ANO-pVQZ`** | — |

      - H--Ar, Sc--Zn
      - \--
      - `ANO-pVQZ` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`aug-ANO-pV5Z`** | — |

      - H--Ar, Sc--Zn
      - \--
      - `ANO-pV5Z` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`saug-ANO-pVDZ`** | — |

      - H--Ar, Sc--Zn
      - \--
      - `ANO-pVDZ` augmented by by a single set of diffuse sp functions

| Item | Value |
| --- | --- |
| **`saug-ANO-pVTZ`** | — |

      - H--Ar, Sc--Zn
      - \--
      - `ANO-pVTZ` augmented by by a single set of diffuse sp functions

| Item | Value |
| --- | --- |
| **`saug-ANO-pVQZ`** | — |

      - H--Ar, Sc--Zn
      - \--
      - `ANO-pVQZ` augmented by by a single set of diffuse sp functions

| Item | Value |
| --- | --- |
| **`saug-ANO-pV5Z`** | — |

      - H--Ar, Sc--Zn
      - \--
      - `ANO-pV5Z` augmented by by a single set of diffuse sp functions

<a id="sec:essentialelements.basisset.builtin.ano.efficient"></a>
#### Efficient Calculations with ANO Basis Sets

Usually, ANO basis sets are "generally contracted" which means that for
any given angular momentum all primitives contribute to all basis
functions. Since the concept of ANOs only makes sense if the underlying
set of primitives is large, the calculations readily become very
expensive unless special precaution is taken in the integral evaluation
algorithms. ORCA features special algorithms for ANO basis sets together
with accurate ANO basis sets for non-relativistic calculations. However,
even then the integral evaluation is so expensive that efficiency can
only be realized if all integrals are stored on disk and are re-used as
needed.

Currently, the use of ANOs is restricted to the [built-in ANO basis sets](tab:essentialelements.basisset.builtin.ano). These are built upon the cc-pV6Z primitives and hence,
the calculations take significant time.

!!! tip
    Geometry optimizations with ANOs are discouraged; they will be *very* inefficient.

The use of ANOs is recommended in the following way:

```orcainput
! ano-pVTZ Conv TightSCF CCSD(T)
%maxcore 2000 
* int 0 1
C  0 0 0    0   0   0
O  1 0 0  1.2   0   0
H  1 2 0  1.1 120   0
H  1 2 3  1.1 120 180
*
```

This yields:

```orca
ano-pVTZ:
E(SCF) = -113.920388785
E(corr)=   -0.427730189
```

Compare to the cc-pVTZ value of:

```orca
cc-pVTZ:
E(SCF) = -113.911870901
E(corr)=   -0.421354947
```

Thus, the ANO-based SCF energy is ca. 8--9 mEh lower and the correlation
energy almost 2 mEh lower than with the cc-basis set of the same size.
Usually, the ANO results are much closer to the basis set limit than the
cc-results. Also, ANO values extrapolate very well (see section
[sec:modelchemistries.mdci.basissetextrapolation](#sec:modelchemistries.mdci.basissetextrapolation))

Importantly, the integrals are all stored in this job. Depending on your
system and your patience, this may be possible up to 300--500 basis
functions. The ORCA correlation modules have been rewritten such that
they deal efficiently with these stored integrals. Thus, we might as
well have used `! MO-CCSD(T) ` or `! AO-CCSD(T) `, both of which would
perform well.

Yet, the burden of generating and storing all four-index integrals
quickly becomes rather heavy. Hence, the combination of ANO basis sets
with the RI-JK technique is particularly powerful and efficient. For
example:

```orca
! ano-pVTZ cc-pVTZ/JK RI-JK Conv TightSCF RI-CCSD(T)
```

For the SCF, this works very well and allows for much larger ANO based
calculations to be done efficiently. Also, RI-MP2 can be done very
efficiently in this way. However, for higher order correlation methods
such as CCSD(T) the logical choice would be RI-CCSD(T) which is
distinctly less efficient than the AO or MO based CCSD(T) (roughly a
factor of two slower). Hence, ORCA implements a hybrid method where the
RI approximation is used to generate all four index integrals. This is
done via the "RI-AO" keyword:

```orca
! ano-pVTZ cc-pVTZ/JK RI-AO Conv TightSCF AO-CCSD(T)
```

In this case either AO-CCSD(T) or MO-CCSD(T) would both work well. This
does not solve the storage bottleneck with respect to the four index
integrals of course. If this becomes a real issue, then RI-CCSD(T) is
mandatory. The error in the total energy is less than 0.1 mEh in the
present example.

!!! warning
    With conventional RI calculations the use of a second fit basis set is not possible and inconsistent results will be obtained. Hence, stick to one auxiliary basis!

<a id="sec:essentialelements.basisset.builtin.misc"></a>
### Miscellaneous and Specialized Basis Sets

A list of further available specialized and miscellaneous basis sets is given in [tab:essentialelements.basisset.builtin.misc](#tab:essentialelements.basisset.builtin.misc).

<a id="tab:essentialelements.basisset.builtin.misc"></a>
!!! note "Collection of available miscellaneous and specialized basis sets."
    :header-rows: 1
    :class: longtable
    :class: footnotesize

| Item | Value |
| --- | --- |
| **Basis Set** | — |

      - Elem.
      - ECP
      - Comment

| Item | Value |
| --- | --- |
| **`D95`** | — |

      - H, Li, B--Ne, Al--Cl
      - \--
      - Dunning's double-$\zeta$ basis set 

| Item | Value |
| --- | --- |
| **`D95p`** | — |

      - H, Li, B--Ne, Al--Cl
      - \--
      - Polarized version of `D95`

| Item | Value |
| --- | --- |
| **`EPR-II`** | — |

      - H, B--F
      - \--
      - Barone's double-$\zeta$ basis set for EPR calculations

| Item | Value |
| --- | --- |
| **`EPR-III`** | — |

      - H, B--F
      - \--
      - Barone's triple-$\zeta$ basis set for EPR calculations

| Item | Value |
| --- | --- |
| **`IGLO-II`** | — |

      - H, B--F, Al--Cl
      - \--
      - Kutzelnigg's basis set for NMR and EPR calculations.

| Item | Value |
| --- | --- |
| **`IGLO-III`** | — |

      - H, B--F, Al--Cl
      - \--
      - Kutzelnigg's larger basis set for NMR and EPR calculations.

| Item | Value |
| --- | --- |
| **`UGBS`** | — |

      - H--Th, Pu--Am, Cf--Lr
      - \--
      - Universal Gaussian basis set.

| Item | Value |
| --- | --- |
| **`CP`** | — |

      - Sc--Zn
      - \--
      - 

| Item | Value |
| --- | --- |
| **`CP(PPP)`** | — |

      - Sc--Zn
      - \--
      - 

| Item | Value |
| --- | --- |
| **`Wachters+f`** | — |

      - Sc--Cu
      - \--
      - 

| Item | Value |
| --- | --- |
| **`W1-mtsmall`** | — |

      - H--Ar
      - \--
      - W1 theory basis set

| Item | Value |
| --- | --- |
| **`W1-DZ`** | — |

      - H--Ar
      - \--
      - W1 theory basis set

| Item | Value |
| --- | --- |
| **`W1-TZ`** | — |

      - H--Ar
      - \--
      - W1 theory basis set

| Item | Value |
| --- | --- |
| **`W1-QZ`** | — |

      - H--Ar
      - \--
      - W1 theory basis set

| Item | Value |
| --- | --- |
| **`W1-Opt`** | — |

      - H--Ar
      - \--
      - W1 theory basis set

| Item | Value |
| --- | --- |
| **`MINI`** | — |

      - H--Ca
      - \--
      - Huzinaga’s minimal basis set.

| Item | Value |
| --- | --- |
| **`MINIS`** | — |

      - H--Ca
      - \--
      - Scaled version of the MINI

| Item | Value |
| --- | --- |
| **`MIDI`** | — |

      - H--Na, Al--K
      - \--
      - Huzinaga's valence double-$\zeta$ basis set

| Item | Value |
| --- | --- |
| **`MINIX`** | — |

      - H--Lr
      - `def-ECP` (Rb--Lr)
      - Combination of small basis sets by Grimme (see [tab:modelchemistries.3cmethods.minix](#tab:modelchemistries.3cmethods.minix)). Used in [HF-3c](sec:modelchemistries.3cmethods.hf3c).

| Item | Value |
| --- | --- |
| **`def2-mSVP`** | — |

      - H--Lr
      - `def2-ECP` (Rb--Rn), `def-ECP` (Fr--Lr)
      - Used in [PBEh-3c](sec:modelchemistries.3cmethods.pbeh3c) and [B3LYP-3c](sec:modelchemistries.3cmethods.b3lyp3c)

| Item | Value |
| --- | --- |
| **`def2-mTZVP`** | — |

      - H--Lr
      - `def2-ECP` (Rb--Rn), `def-ECP` (Fr--Lr)
      - Used in [B97-3c](sec:modelchemistries.3cmethods.b973c)

| Item | Value |
| --- | --- |
| **`def2-mTZVPP`** | — |

      - H--Lr
      - `def2-ECP` (Rb--Rn), `def-ECP` (Fr--Lr)
      - Used in [r²SCAN-3c](sec:modelchemistries.3cmethods.r2scan3c)

| Item | Value |
| --- | --- |
| **`vDZP`** | — |

      - H--Rn
      - `vDZP-ECP` (B--Rn)
      - Molecule-optimized polarized valence double-$\zeta$ basis set by Grimme et al. Used in [$\omega$B97X-3c](sec:modelchemistries.3cmethods.wb97x3c).[grimme2022wb97x3c](../../bibliography.md)

<a id="sec:essentialelements.basisset.builtin.rel"></a>
## Relativistic Basis Sets

Scalar-relativistic calculations with the [DKH](sec:essentialelements.relativistic.dkh), 
[ZORA](sec:essentialelements.relativistic.zora) or [X2C](sec:essentialelements.relativistic.x2c) 
approaches typically require specifically optimized or recontracted basis sets -- 
see [sec:essentialelements.relativistic.basissets](#sec:essentialelements.relativistic.basissets) for details. 
ORCA provides various suitable basis sets for such calculations like the recontracted 
[Karlsruhe](sec:essentialelements.basisset.builtin.rel.def2), 
the [SARC](sec:essentialelements.basisset.builtin.rel.sarc), 
and [SARC2](sec:essentialelements.basisset.builtin.rel.sarc2), 
and various optimized all-electron [correlation-consistent](sec:essentialelements.basisset.builtin.rel.cc) basis sets. 
Suitable auxiliary basis options like `SARC/J` or `AutoAux`
can be found in [sec:essentialelements.basisset.aux](#sec:essentialelements.basisset.aux).

<a id="sec:essentialelements.basisset.builtin.rel.ahlrichs"></a>
### Recontracted Ahlrichs Basis Sets

A list of available relativistically recontracted variants of the original Ahlrichs basis sets is given in [tab:essentialelements.basisset.builtin.rel.ahlrichs](#tab:essentialelements.basisset.builtin.rel.ahlrichs).
Refer to the section [sec:essentialelements.basisset.builtin.ahlrichs](#sec:essentialelements.basisset.builtin.ahlrichs) for the origin of the legacy definitions with the prefix "old-".

<a id="tab:essentialelements.basisset.builtin.rel.ahlrichs"></a>
!!! note "Relativistically recontracted Ahlrichs basis sets. RH = relativistic Hamiltonian."
    :header-rows: 1
    :class: longtable
    :class: footnotesize

| Item | Value |
| --- | --- |
| **Basis Set** | — |

      - Elem.
      - RH
      - Comment

| Item | Value |
| --- | --- |
| **`DKH-SV(P)`** | — |

      - H–Kr
      - DKH2
      - 

| Item | Value |
| --- | --- |
| **`DKH-SVP`** | — |

      - H–Kr
      - DKH2
      - 

| Item | Value |
| --- | --- |
| **`DKH-TZV(P)`** | — |

      - H–Kr
      - DKH2
      - 

| Item | Value |
| --- | --- |
| **`DKH-TZVP`** | — |

      - H–Kr
      - DKH2
      - 

| Item | Value |
| --- | --- |
| **`DKH-TZVPP`** | — |

      - H–Kr
      - DKH2
      - 

| Item | Value |
| --- | --- |
| **`DKH-QZVP`** | — |

      - H–Kr
      - DKH2
      - 

| Item | Value |
| --- | --- |
| **`DKH-QZVPP`** | — |

      - H–Kr
      - DKH2
      -

| Item | Value |
| --- | --- |
| **`ZORA-SV(P)`** | — |

      - H–Kr
      - ZORA
      - 

| Item | Value |
| --- | --- |
| **`ZORA-SVP`** | — |

      - H–Kr
      - ZORA
      - 

| Item | Value |
| --- | --- |
| **`ZORA-TZV(P)`** | — |

      - H–Kr
      - ZORA
      - 

| Item | Value |
| --- | --- |
| **`ZORA-TZVP`** | — |

      - H–Kr
      - ZORA
      - 

| Item | Value |
| --- | --- |
| **`ZORA-TZVPP`** | — |

      - H–Kr
      - ZORA
      - 

| Item | Value |
| --- | --- |
| **`ZORA-QZVP`** | — |

      - H–Kr
      - ZORA
      - 

| Item | Value |
| --- | --- |
| **`ZORA-QZVPP`** | — |

      - H–Kr
      - ZORA
      - 

| Item | Value |
| --- | --- |
| ***Legacy definitions (not recommended!)*** | — |
| **`old-DKH-SV(P)`** | — |

      - H--I
      - DKH2
      - 

| Item | Value |
| --- | --- |
| **`old-DKH-SVP`** | — |

      - H--I
      - DKH2
      - 

| Item | Value |
| --- | --- |
| **`old-DKH-TZV(P)`** | — |

      - H--I
      - DKH2
      - 

| Item | Value |
| --- | --- |
| **`old-DKH-TZVP`** | — |

      - H--I
      - DKH2
      - 

| Item | Value |
| --- | --- |
| **`old-DKH-TZVPP`** | — |

      - H--I
      - DKH2
      - 

| Item | Value |
| --- | --- |
| **`old-ZORA-SV(P)`** | — |

      - H--I
      - ZORA
      - 

| Item | Value |
| --- | --- |
| **`old-ZORA-SVP`** | — |

      - H--I
      - ZORA
      - 

| Item | Value |
| --- | --- |
| **`old-ZORA-TZV(P)`** | — |

      - H--I
      - ZORA
      - 

| Item | Value |
| --- | --- |
| **`old-ZORA-TZVP`** | — |

      - H--I
      - ZORA
      - 

| Item | Value |
| --- | --- |
| **`old-ZORA-TZVPP`** | — |

      - H--I
      - ZORA
      - 

<a id="sec:essentialelements.basisset.builtin.rel.def2"></a>
### Recontracted Karlsruhe def2 Basis Sets

A list of available adapted [DKH](sec:essentialelements.relativistic.dkh) and [ZORA](sec:essentialelements.relativistic.zora) versions of the def2 basis sets (i.e., for the all-electron def2 basis sets) is given in [tab:essentialelements.basisset.builtin.rel.def2](#tab:essentialelements.basisset.builtin.rel.def2). These basis sets retain the original def2 exponents but have only one contracted function per angular momentum (and hence are somewhat larger), with contraction coefficients suitable for the respective scalar relativistic Hamiltonian. These basis sets can be combined with the [SARC](sec:essentialelements.basisset.builtin.rel.sarc) and [SARC2](sec:essentialelements.basisset.builtin.rel.sarc2) basis sets for the heavier elements.

<a id="tab:essentialelements.basisset.builtin.rel.def2"></a>
!!! note "Relativistically recontracted Karlsruhe basis sets. RH = relativistic Hamiltonian."
    :header-rows: 1
    :class: longtable
    :class: footnotesize

| Item | Value |
| --- | --- |
| **Basis Set** | — |

      - Elem.
      - RH
      - Comment

| Item | Value |
| --- | --- |
| **`DKH-def2-SVP`** | — |

      - H--Kr
      - DKH2
      - 

| Item | Value |
| --- | --- |
| **`DKH-def2-SV(P)`** | — |

      - H--Kr
      - DKH2
      - 

| Item | Value |
| --- | --- |
| **`DKH-def2-TZVP`** | — |

      - H--Kr
      - DKH2
      - 

| Item | Value |
| --- | --- |
| **`DKH-def2-TZVP(-f)`** | — |

      - H--Kr
      - DKH2
      - 

| Item | Value |
| --- | --- |
| **`DKH-def2-TZVPP`** | — |

      - H--Kr
      - DKH2
      - 

| Item | Value |
| --- | --- |
| **`DKH-def2-QZVPP`** | — |

      - H--Kr
      - DKH2
      -

| Item | Value |
| --- | --- |
| **`ZORA-def2-SVP`** | — |

      - H--Kr
      - ZORA
      - 

| Item | Value |
| --- | --- |
| **`ZORA-def2-SV(P)`** | — |

      - H--Kr
      - ZORA
      - 

| Item | Value |
| --- | --- |
| **`ZORA-def2-TZVP`** | — |

      - H--Kr
      - ZORA
      - 

| Item | Value |
| --- | --- |
| **`ZORA-def2-TZVP(-f)`** | — |

      - H--Kr
      - ZORA
      - 

| Item | Value |
| --- | --- |
| **`ZORA-def2-TZVPP`** | — |

      - H--Kr
      - ZORA
      - 

| Item | Value |
| --- | --- |
| **`ZORA-def2-QZVPP`** | — |

      - H--Kr
      - ZORA
      - 

| Item | Value |
| --- | --- |
| ***Minimally augmented* (scheme by Truhlar et al.[Zheng:2010iz](../../bibliography.md))** | — |
| **`ma-DKH-def2-SVP`** | — |

      - H--Kr
      - DKH2
      -

| Item | Value |
| --- | --- |
| **`ma-DKH-def2-SV(P)`** | — |

      - H--Kr
      - DKH2
      -

| Item | Value |
| --- | --- |
| **`ma-DKH-def2-TZVP`** | — |

      - H--Kr
      - DKH2
      -

| Item | Value |
| --- | --- |
| **`ma-DKH-def2-TZVP(-f)`** | — |

      - H--Kr
      - DKH2
      -

| Item | Value |
| --- | --- |
| **`ma-DKH-def2-TZVPP`** | — |

      - H--Kr
      - DKH2
      -

| Item | Value |
| --- | --- |
| **`ma-DKH-def2-QZVPP`** | — |

      - H--Kr
      - DKH2
      -

| Item | Value |
| --- | --- |
| **`ma-ZORA-def2-SVP`** | — |

      - H--Kr
      - ZORA
      -

| Item | Value |
| --- | --- |
| **`ma-ZORA-def2-SV(P)`** | — |

      - H--Kr
      - ZORA
      -

| Item | Value |
| --- | --- |
| **`ma-ZORA-def2-TZVP`** | — |

      - H--Kr
      - ZORA
      -

| Item | Value |
| --- | --- |
| **`ma-ZORA-def2-TZVP(-f)`** | — |

      - H--Kr
      - ZORA
      -

| Item | Value |
| --- | --- |
| **`ma-ZORA-def2-TZVPP`** | — |

      - H--Kr
      - ZORA
      -

| Item | Value |
| --- | --- |
| **`ma-ZORA-def2-QZVPP`** | — |

      - H--Kr
      - ZORA
      -

<a id="sec:essentialelements.basisset.builtin.rel.sarc"></a>
### SARC Basis Sets

Segmented all-electron relativistically contracted (SARC) basis sets for use with the DKH2 and ZORA Hamiltonians.[Pantazis2008,Buehl2008,Pantazis2009,Pantazis2011,Pantazis2012,Rolfes2020](../../bibliography.md) A list of available SARC basis sets is given in [tab:essentialelements.basisset.builtin.rel.sarc](#tab:essentialelements.basisset.builtin.rel.sarc).

!!! tip
    Specifically for wavefunction-based calculations of lanthanide systems
    we recommend the more heavily polarized [SARC2 basis sets](sec:essentialelements.basisset.builtin.rel.sarc)
    [aravenaSARC2](../../bibliography.md).

<a id="tab:essentialelements.basisset.builtin.rel.sarc"></a>
!!! note "Relativistic SARC basis sets. RH = relativistic Hamiltonian."
    :header-rows: 1
    :class: longtable
    :class: footnotesize

| Item | Value |
| --- | --- |
| **Basis Set** | — |

      - Elem.
      - RH
      - Comment

| Item | Value |
| --- | --- |
| **`SARC-DKH-SVP`** | — |

      - Hf--Hg
      - DKH2
      - 

| Item | Value |
| --- | --- |
| **`SARC-DKH-TZVP`** | — |

      - Rb--Rn, Ac--Lr
      - DKH2
      - 

| Item | Value |
| --- | --- |
| **`SARC-DKH-TZVPP`** | — |

      - Rb--Rn, Ac--Lr
      - DKH2
      - 

| Item | Value |
| --- | --- |
| **`SARC-ZORA-SVP`** | — |

      - Hf--Hg
      - ZORA
      - 

| Item | Value |
| --- | --- |
| **`SARC-ZORA-TZVP`** | — |

      - Rb--Rn, Ac--Lr
      - ZORA
      - 

| Item | Value |
| --- | --- |
| **`SARC-ZORA-TZVPP`** | — |

      - Rb--Rn, Ac--Lr
      - ZORA
      - 

!!! note
    *SARC/J is the general-purpose Coulomb-fitting auxiliary for all SARC orbital basis sets.*

<a id="sec:essentialelements.basisset.builtin.rel.sarc2"></a>
### SARC2 Basis Sets

SARC basis sets of valence quadruple-zeta quality for lanthanides, with NEVPT2-optimized (3g2h) polarization functions (SARC2).[aravenaSARC2](../../bibliography.md) Suitable for accurate calculations using correlated wavefunction methods. A list of available SARC2 basis sets is given in [tab:essentialelements.basisset.builtin.rel.sarc2](#tab:essentialelements.basisset.builtin.rel.sarc2).

<a id="tab:essentialelements.basisset.builtin.rel.sarc2"></a>
!!! note "Relativistic SARC2 basis sets. RH = relativistic Hamiltonian."
    :header-rows: 1
    :class: longtable
    :class: footnotesize

| Item | Value |
| --- | --- |
| **Basis Set** | — |

      - Elem.
      - ECP
      - Comment

| Item | Value |
| --- | --- |
| **`SARC2-DKH-QZV`** | — |

      - La--Lu
      - DKH2
      - 

| Item | Value |
| --- | --- |
| **`SARC2-DKH-QZVP`** | — |

      - La--Lu
      - DKH2
      - 

| Item | Value |
| --- | --- |
| **`SARC2-ZORA-QZV`** | — |

      - La--Lu
      - ZORA
      - 

| Item | Value |
| --- | --- |
| **`SARC2-ZORA-QZVP`** | — |

      - La--Lu
      - ZORA
      - 

!!! note
    Each basis set has a large dedicated /JK auxiliary basis set for simultaneous Coulomb and exchange fitting (cf. [tab:essentialelements.basisset.aux.auxjk](#tab:essentialelements.basisset.aux.auxjk)).

<a id="sec:essentialelements.basisset.builtin.rel.karlsruhex2c"></a>
### Karlsruhe x2c Basis Sets

For calculations with the X2C Hamiltonian, all-electron basis sets up to Rn are available.[Weigend2017-x2c-XVP](../../bibliography.md)
The "-s" variants, e.g. `x2c-TZVPall-s`, are augmented with additional tight functions for NMR shielding calculations.[Weigend2019-x2c-XVP-s](../../bibliography.md)
The "-2c" variants, e.g. `x2c-TZVPall-2c`, are intended for two-component calculations including spin-orbit coupling (**Note that two-component calculations are not implemented in *ORCA***). 
A list of available basis sets of this family is given in [tab:essentialelements.basisset.builtin.rel.karlsruhex2c](#tab:essentialelements.basisset.builtin.rel.karlsruhex2c).

!!! tip
    The `x2c/J` and `AutoAux` auxiliary basis set options can be used for these basis sets.

<a id="tab:essentialelements.basisset.builtin.rel.karlsruhex2c"></a>
!!! note "Karlsruhe basis sets optimized for the x2c Hamiltonian.[Weigend2017-x2c-XVP](../../bibliography.md) RH = relativistic Hamiltonian."
    :header-rows: 1
    :class: longtable
    :class: footnotesize

| Item | Value |
| --- | --- |
| **Basis Set** | — |

      - Elem.
      - RH
      - Comment

| Item | Value |
| --- | --- |
| **`x2c-SV(P)all`** | — |

      - H--Rn
      - X2C
      - 

| Item | Value |
| --- | --- |
| **`x2c-SVPall`** | — |

      - H--Rn
      - X2C
      - 

| Item | Value |
| --- | --- |
| **`x2c-TZVPall`** | — |

      - H--Rn
      - X2C
      - 

| Item | Value |
| --- | --- |
| **`x2c-TZVPPall`** | — |

      - H--Rn
      - X2C
      - 

| Item | Value |
| --- | --- |
| **`x2c-QZVPall`** | — |

      - H--Rn
      - X2C
      - 

| Item | Value |
| --- | --- |
| **`x2c-QZVPPall`** | — |

      - H--Rn
      - X2C
      -

| Item | Value |
| --- | --- |
| ***NMR shielding optimized*[Weigend2019-x2c-XVP-s](../../bibliography.md)** | — |
| **`x2c-SV(P)all-s`** | — |

      - H--Rn
      - X2C
      - 

| Item | Value |
| --- | --- |
| **`x2c-SVPall-s`** | — |

      - H--Rn
      - X2C
      - 

| Item | Value |
| --- | --- |
| **`x2c-TZVPall-s`** | — |

      - H--Rn
      - X2C
      - 

| Item | Value |
| --- | --- |
| **`x2c-TZVPPall-s`** | — |

      - H--Rn
      - X2C
      - 

| Item | Value |
| --- | --- |
| **`x2c-QZVPall-s`** | — |

      - H--Rn
      - X2C
      - 

| Item | Value |
| --- | --- |
| **`x2c-QZVPPall-s`** | — |

      - H--Rn
      - X2C
      - 

| Item | Value |
| --- | --- |
| ***Two-component variants* (no matching Hamiltonian yet!)** | — |
| **`x2c-SV(P)all-2c`** | — |

      - H--Rn
      - SO-X2C
      - 

| Item | Value |
| --- | --- |
| **`x2c-SVPall-2c`** | — |

      - H--Rn
      - SO-X2C
      - 

| Item | Value |
| --- | --- |
| **`x2c-TZVPall-2c`** | — |

      - H--Rn
      - SO-X2C
      - 

| Item | Value |
| --- | --- |
| **`x2c-TZVPPall-2c`** | — |

      - H--Rn
      - SO-X2C
      - 

| Item | Value |
| --- | --- |
| **`x2c-QZVPall-2c`** | — |

      - H--Rn
      - SO-X2C
      - 

| Item | Value |
| --- | --- |
| **`x2c-QZVPPall-2c`** | — |

      - H--Rn
      - SO-X2C
      - 

| Item | Value |
| --- | --- |
| **`x2c-QZVPall-2c-s`** | — |

      - H--Rn
      - SO-X2C
      - 

| Item | Value |
| --- | --- |
| **`x2c-QZVPPall-2c-s`** | — |

      - H--Rn
      - SO-X2C
      - 

<a id="sec:essentialelements.basisset.builtin.rel.sapporo"></a>
### Relativistic Sapporo Basis Sets

A list of relativistic variants of the 
[Sapporo basis sets](sec:essentialelements.basisset.builtin.sapporo)
that were optimized for the DKH3 Hamiltonian and finite nucleus are given in 
[tab:essentialelements.basisset.builtin.rel.sapporo](#tab:essentialelements.basisset.builtin.rel.sapporo).

<a id="tab:essentialelements.basisset.builtin.rel.sapporo"></a>
!!! note "Relativistic Sapporo basis sets. RH = relativistic Hamiltonian."
    :header-rows: 1
    :class: longtable
    :class: footnotesize

| Item | Value |
| --- | --- |
| **Basis Set** | — |

      - Elem.
      - RH
      - Comment

| Item | Value |
| --- | --- |
| **`Sapporo-DKH3-DZP-2012`** | — |

      - K--Rn
      - DKH3
      - Optimized for DKH3 and finite nucleus

| Item | Value |
| --- | --- |
| **`Sapporo-DKH3-TZP-2012`** | — |

      - K--Rn
      - DKH3
      - 

| Item | Value |
| --- | --- |
| **`Sapporo-DKH3-QZP-2012`** | — |

      - K--Rn
      - DKH3
      - 

<a id="sec:essentialelements.basisset.builtin.rel.cc"></a>
### Relativistic Correlation-Consistent Basis Sets

A list of relativistic variants of the [correlation-consistent basis sets](sec:essentialelements.basisset.builtin.cc)
is given in [tab:essentialelements.basisset.builtin.rel.cc](#tab:essentialelements.basisset.builtin.rel.cc).

<a id="tab:essentialelements.basisset.builtin.rel.cc"></a>
!!! note "Relativistic correlation-consistent basis sets. RH = relativistic Hamiltonian."
    :header-rows: 1
    :class: longtable
    :class: footnotesize

| Item | Value |
| --- | --- |
| **Basis Set** | — |

      - Elem.
      - RH
      - Comment

| Item | Value |
| --- | --- |
| **`cc-pVDZ-DK`** | — |

      - H--Ar, Sc--Kr
      - DKH2
      - 

| Item | Value |
| --- | --- |
| **`cc-pVTZ-DK`** | — |

      - H--Ar, Sc--Kr, Y--Xe, Hf--Rn
      - DKH2
      - 

| Item | Value |
| --- | --- |
| **`cc-pVQZ-DK`** | — |

      - H--Ar, Sc--Kr, In--Xe, Tl--Rn
      - DKH2
      - 

| Item | Value |
| --- | --- |
| **`cc-pV5Z-DK`** | — |

      - H--Ar, Sc--Kr
      - DKH2
      - 

| Item | Value |
| --- | --- |
| **`cc-pVDZ-DK3`** | — |

      - U
      - DKH3
      - For use with 3rd-order DKH

| Item | Value |
| --- | --- |
| **`cc-pVTZ-DK3`** | — |

      - U
      - DKH3
      - 

| Item | Value |
| --- | --- |
| **`cc-pVQZ-DK3`** | — |

      - U
      - DKH3
      - 

| Item | Value |
| --- | --- |
| **`aug-cc-pVDZ-DK`** | — |

      - H--Ar, Sc--Kr
      - DKH2
      - `cc-pVDZ-DK` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`aug-cc-pVTZ-DK`** | — |

      - H--Ar, Sc--Kr, Y--Xe, Hf--Rn
      - DKH2
      - `cc-pVTZ-DK` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`aug-cc-pVQZ-DK`** | — |

      - H--Ar, Sc--Kr, In--Xe, Tl--Rn
      - DKH2
      - `cc-pVQZ-DK` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`aug-cc-pV5Z-DK`** | — |

      - H--Ar, Sc--Kr
      - DKH2
      - `cc-pV5Z-DK` augmented by diffuse functions

| Item | Value |
| --- | --- |
| **`cc-pwCVDZ-DK`** | — |

      - H--Be, Na--Mg, Ca--Zn
      - DKH2
      - Equals `cc-pVDZ-DK` for H and He

| Item | Value |
| --- | --- |
| **`cc-pwCVTZ-DK`** | — |

      - H--Be, Na--Mg, Ca--Zn, Y--Xe, Hf--Rn
      - DKH2
      - Equals `cc-pVTZ-DK` for H and He

| Item | Value |
| --- | --- |
| **`cc-pwCVQZ-DK`** | — |

      - H--Be, Na--Mg, Ca--Zn, In--Xe, Tl--Rn
      - DKH2
      - Equals `cc-pVQZ-DK` for H and He

| Item | Value |
| --- | --- |
| **`cc-pwCV5Z-DK`** | — |

      - H--Be, Na--Mg, Ca--Zn
      - DKH2
      - Equals `cc-pV5Z-DK` for H and He

| Item | Value |
| --- | --- |
| **`cc-pwCVDZ-DK3`** | — |

      - U
      - DKH3
      - 

| Item | Value |
| --- | --- |
| **`cc-pwCVTZ-DK3`** | — |

      - U
      - DKH3
      - 

| Item | Value |
| --- | --- |
| **`cc-pwCVQZ-DK3`** | — |

      - U
      - DKH3
      - 

| Item | Value |
| --- | --- |
| **`aug-cc-pwCVDZ-DK`** | — |

      - H--Be, Na--Mg, Sc--Zn
      - DKH2
      - `cc-pwCVDZ-DK` augmented by diffuse functions, equals `aug-cc-pVDZ-DK` for H and He

| Item | Value |
| --- | --- |
| **`aug-cc-pwCVTZ-DK`** | — |

      - H--Be, Na--Mg, Sc--Zn, Y--Xe, Hf--Rn
      - DKH2
      - `cc-pwCVTZ-DK` augmented by diffuse functions, equals `aug-cc-pVTZ-DK` for H and He

| Item | Value |
| --- | --- |
| **`aug-cc-pwCVQZ-DK`** | — |

      - H--Be, Na--Mg, Sc--Zn, In--Xe, Tl--Rn
      - DKH2
      - `cc-pwCVQZ-DK` augmented by diffuse functions, equals `aug-cc-pVQZ-DK` for H and He

| Item | Value |
| --- | --- |
| **`aug-cc-pwCV5Z-DK`** | — |

      - H--Be, Na--Mg, Sc--Zn
      - DKH2
      - `cc-pwCV5Z-DK` augmented by diffuse functions, equals `aug-cc-pV5Z-DK` for H and He

### Relativistically Contracted ANO Basis Sets

The relativistic contracted ANO basis sets of Roos and coworkers
were developed for the DKH2 Hamiltonian.
The full list is given in [tab:essentialelements.basisset.builtin.rel.ano](#tab:essentialelements.basisset.builtin.rel.ano).

<a id="tab:essentialelements.basisset.builtin.rel.ano"></a>
!!! note "Relativistic contracted ANO basis sets. RH = relativistic Hamiltonian."
    :header-rows: 1
    :class: longtable
    :class: footnotesize

| Item | Value |
| --- | --- |
| **Basis Set** | — |

      - Elem.
      - RH
      - Comment

| Item | Value |
| --- | --- |
| **`ANO-RCC-Full`** | — |

      - H--Cm
      - DKH2
      - Complete ANO-RCC basis sets.

| Item | Value |
| --- | --- |
| **`ANO-RCC-DZP`** | — |

      - H--Cm
      - DKH2
      - Double-$\zeta$ contraction of `ANO-RCC-Full`.

| Item | Value |
| --- | --- |
| **`ANO-RCC-TZP`** | — |

      - H--Cm
      - DKH2
      - Triple-$\zeta$ contraction of `ANO-RCC-Full`.

| Item | Value |
| --- | --- |
| **`ANO-RCC-QZP`** | — |

      - H--Cm
      - DKH2
      - Quadruple-$\zeta$ contraction of `ANO-RCC-Full`.

<a id="sec:essentialelements.basisset.aux"></a>
## Auxiliary Basis Sets

[Resolution-of-the-idendity (RI)](sec:essentialelements.ri) techniques can be used to speed up various types of calculations. 
Any RI method requires the definition of a reasonable auxiliary basis set in addition to the chosen 
[orbital basis set](sec:essentialelements.basisset.builtin). 
ORCA provides various built-in auxiliary basis set options
for [`AuxJ`](tab:essentialelements.basisset.aux.auxj), 
[`AuxJK`](tab:essentialelements.basisset.aux.auxjk), 
[`AuxC`](tab:essentialelements.basisset.aux.auxc), 
and [`CABS`](tab:essentialelements.basisset.aux.cabs)
and an automatic auxiliary basis set generation called [AutoAux](sec:essentialelements.basisset.aux.autoaux). 
Auxiliary basis sets can further be read from external files as described in [sec:essentialelements.basisset.file](#sec:essentialelements.basisset.file).

!!! note
    The distinction beweeen `AuxJ`, `AuxJK`, `AuxC`, and `CABS`,
    as well as how to correctly assign them, 
    is [explained above](par:essentialelements.basisset.basicusage.aux).

<a id="sec:essentialelements.basisset.aux.auxj"></a>
### Coulomb-fitting auxiliary basis sets (`AuxJ`)
The auxiliary basis sets listed in [tab:essentialelements.basisset.aux.auxj](#tab:essentialelements.basisset.aux.auxj)
are suitable for the [RI-J](sec:essentialelements.ri.rij), 
[RIJDX/RIJONX](sec:essentialelements.ri.rijonx),
and [RIJCOSX](sec:essentialelements.ri.rijcosx) approximations.

<a id="tab:essentialelements.basisset.aux.auxj"></a>
!!! note "Available Coulomb-fitting auxiliary basis sets."
    :header-rows: 1
    :class: longtable
    :class: footnotesize

| Item | Value |
| --- | --- |
| **Keyword** | — |

      - Elements
      - Comment

| Item | Value |
| --- | --- |
| **`def2/J`** | — |

      - H--Lr
      - Weigend's "universal" Coulomb-fitting basis suitable for all 
        [def2](sec:essentialelements.basisset.builtin.def2) 
        and [def](sec:essentialelements.basisset.builtin.ahlrichs) type basis sets. 
        Assumes the use of ECPs beyond Kr (do not use with DKH/ZORA/X2C).

| Item | Value |
| --- | --- |
| **`def2-mTZVP/J`** | — |

      - H--Lr
      -  

| Item | Value |
| --- | --- |
| **`def2-mTZVPP/J`** | — |

      - H--Lr
      -

| Item | Value |
| --- | --- |
| **`x2c/J`** | — |

      - H--Rn
      - Weigend's Coulomb-fitting basis for the all-electron 
        [x2c-XVPall](sec:essentialelements.basisset.builtin.rel.karlsruhex2c) basis sets

| Item | Value |
| --- | --- |
| **`SARC/J`** | — |

      - H--Rn, Ac--Lr
      - General-purpose Coulomb-fitting basis set for all-electron calculations. 
        Consists of the decontracted def2/J up to Kr and of our own auxiliary 
        basis sets for the rest of the periodic table. 
        Appropriate for use in DKH or ZORA calculations with the 
        [recontracted versions of the all-electron def2](sec:essentialelements.basisset.builtin.rel.def2)
        basis sets (up to Kr) and the [SARC](sec:essentialelements.basisset.builtin.rel.sarc) 
        basis sets for the heavier elements.

<a id="sec:essentialelements.basisset.aux.auxjk"></a>
### Coulomb- and exchange-fitting auxiliary basis sets (`AuxJK`)

The auxiliary basis sets listed in [tab:essentialelements.basisset.aux.auxjk](#tab:essentialelements.basisset.aux.auxjk)
are optimized for the [RI-JK](sec:essentialelements.ri.rijk) approximation.
They can safely be used for [RI-J](sec:essentialelements.ri.rij), 
[RIJDX/RIJONX](sec:essentialelements.ri.rijonx),
or [RIJCOSX](sec:essentialelements.ri.rijcosx),
but in that case they must be assigned to `AuxJ` via the `%basis` block.

<a id="tab:essentialelements.basisset.aux.auxjk"></a>
!!! note "Available Coulomb- and exchange-fitting auxiliary basis sets."
    :header-rows: 1
    :class: longtable
    :class: footnotesize

| Item | Value |
| --- | --- |
| **Keyword** | — |

      - Elements
      - Comment

| Item | Value |
| --- | --- |
| **`def2/JK`** | — |

      - H--Rn
      - Coulomb+Exchange fitting for all 
        [def2](sec:essentialelements.basisset.builtin.def2) basis sets

| Item | Value |
| --- | --- |
| **`def2/JKsmall`** | — |

      - H--Ra, Th--Lr
      - reduced version of `def2/JK`

| Item | Value |
| --- | --- |
| **`cc-pVTZ/JK`** | — |

      - H, B--F, Al--Cl, Ga--Br
      - {rspan}`2` For use with the respective cc-pV$n$Z orbital basis

| Item | Value |
| --- | --- |
| **`cc-pVQZ/JK`** | — |

      - H, B--F, Al--Cl, Ga--Br

| Item | Value |
| --- | --- |
| **`cc-pV5Z/JK`** | — |

      - H, B--F, Al--Cl, Ga--Br

| Item | Value |
| --- | --- |
| **`aug-cc-pVTZ/JK`** | — |

      - H, B--F, Al--Cl, Ga--Br
      - {rspan}`2` For use with the respective aug-cc-pV$n$Z orbital basis

| Item | Value |
| --- | --- |
| **`aug-cc-pVQZ/JK`** | — |

      - H, B--F, Al--Cl, Ga--Br

| Item | Value |
| --- | --- |
| **`aug-cc-pV5Z/JK`** | — |

      - H, B--F, Al--Cl, Ga--Br

| Item | Value |
| --- | --- |
| **`SARC2-DKH-QZV/JK`** | — |

      - La--Lu
      -

| Item | Value |
| --- | --- |
| **`SARC2-DKH-QZVP/JK`** | — |

      - La--Lu
      -

| Item | Value |
| --- | --- |
| **`SARC2-ZORA-QZV/JK`** | — |

      - La--Lu
      -

| Item | Value |
| --- | --- |
| **`SARC2-ZORA-QZVP/JK`** | — |

      - La--Lu
      -

<a id="sec:essentialelements.basisset.aux.auxc"></a>
### Auxiliary basis sets for correlated methods (`AuxC`)
The available auxiliary basis sets suitable for post-(CAS)SCF dynamical electron correlation methods
are listed in [tab:essentialelements.basisset.aux.auxc](#tab:essentialelements.basisset.aux.auxc).

<a id="tab:essentialelements.basisset.aux.auxc"></a>
!!! note "Available auxiliary basis sets for correlated methods."
    :header-rows: 1
    :class: longtable
    :class: footnotesize

| Item | Value |
| --- | --- |
| **Keyword** | — |

      - Elements
      - Comment

| Item | Value |
| --- | --- |
| **`def2-SVP/C`** | — |

      - H--Rn
      - {rspan}`7` For use with the respective def2 orbital basis

| Item | Value |
| --- | --- |
| **`def2-TZVP/C`** | — |

      - H--Rn

| Item | Value |
| --- | --- |
| **`def2-TZVPP/C`** | — |

      - H--Rn

| Item | Value |
| --- | --- |
| **`def2-QZVPP/C`** | — |

      - H--Rn

| Item | Value |
| --- | --- |
| **`def2-SVPD/C`** | — |

      - H--La, Hf--Rn

| Item | Value |
| --- | --- |
| **`def2-TZVPD/C`** | — |

      - H--La, Hf--Rn

| Item | Value |
| --- | --- |
| **`def2-TZVPPD/C`** | — |

      - H--La, Hf--Rn

| Item | Value |
| --- | --- |
| **`def2-QZVPPD/C`** | — |

      - H--La, Hf--Rn

| Item | Value |
| --- | --- |
| **`cc-pVDZ/C`** | — |

      - H--Ar, Ga--Kr
      - {rspan}`4` For use with the respective cc-pV$n$Z orbital basis

| Item | Value |
| --- | --- |
| **`cc-pVTZ/C`** | — |

      - H--Ar, Sc--Kr

| Item | Value |
| --- | --- |
| **`cc-pVQZ/C`** | — |

      - H--Ar, Sc--Kr

| Item | Value |
| --- | --- |
| **`cc-pV5Z/C`** | — |

      - H--Ar, Ga--Kr

| Item | Value |
| --- | --- |
| **`cc-pV6Z/C`** | — |

      - H--He, B--Ne, Al--Ar

| Item | Value |
| --- | --- |
| **`aug-cc-pVDZ/C`** | — |

      - H--He, Be--Ne, Mg--Ar, Ga--Kr
      - {rspan}`4` For use with the respective aug-cc-pV$n$Z orbital basis

| Item | Value |
| --- | --- |
| **`aug-cc-pVTZ/C`** | — |

      - H--He, Be--Ne, Mg--Ar, Sc--Kr

| Item | Value |
| --- | --- |
| **`aug-cc-pVQZ/C`** | — |

      - H--He, Be--Ne, Mg--Ar, Sc--Kr

| Item | Value |
| --- | --- |
| **`aug-cc-pV5Z/C`** | — |

      - H--Ne, Al--Ar, Ga--Kr

| Item | Value |
| --- | --- |
| **`aug-cc-pV6Z/C`** | — |

      - H--He, B--Ne, Al--Ar

| Item | Value |
| --- | --- |
| **`cc-pwCVDZ/C`** | — |

      - H--He, B--Ne, Al--Ar, Ga--Kr
      - {rspan}`3` For use with the respective cc-pwCV$n$Z orbital basis, equals `cc-pV$n$Z/C` for H and He

| Item | Value |
| --- | --- |
| **`cc-pwCVTZ/C`** | — |

      - H--He, B--Ne, Al--Ar, Sc--Kr

| Item | Value |
| --- | --- |
| **`cc-pwCVQZ/C`** | — |

      - H--He, B--Ne, Al--Ar, Ga--Kr

| Item | Value |
| --- | --- |
| **`cc-pwCV5Z/C`** | — |

      - H--Ne, Al--Ar

| Item | Value |
| --- | --- |
| **`aug-cc-pwCVDZ/C`** | — |

      - H--He, B--Ne, Al--Ar, Ga--Kr
      - {rspan}`3` For use with the respective aug-cc-pwCV$n$Z orbital basis, equals `aug-cc-pV$n$Z/C` for H and He 

| Item | Value |
| --- | --- |
| **`aug-cc-pwCVTZ/C`** | — |

      - H--He, B--Ne, Al--Ar, Sc--Kr

| Item | Value |
| --- | --- |
| **`aug-cc-pwCVQZ/C`** | — |

      - H--He, B--Ne, Al--Ar, Ga--Kr

| Item | Value |
| --- | --- |
| **`aug-cc-pwCV5Z/C`** | — |

      - H--Ne, Al--Ar

| Item | Value |
| --- | --- |
| **`cc-pVDZ-PP/C`** | — |

      - Cu--Kr, Y--Xe, Hf--Rn
      - {rspan}`2` For use with the respective cc-pV$n$Z-PP orbital basis

| Item | Value |
| --- | --- |
| **`cc-pVTZ-PP/C`** | — |

      - Cu--Kr, Y--Xe, Hf--Rn

| Item | Value |
| --- | --- |
| **`cc-pVQZ-PP/C`** | — |

      - Cu--Kr, Y--Xe, Hf--Rn

| Item | Value |
| --- | --- |
| **`aug-cc-pVDZ-PP/C`** | — |

      - Cu--Kr, Y--Xe, Hf--Rn
      - {rspan}`2` For use with the respective aug-cc-pV$n$Z-PP orbital basis

| Item | Value |
| --- | --- |
| **`aug-cc-pVTZ-PP/C`** | — |

      - Cu--Kr, Y--Xe, Hf--Rn

| Item | Value |
| --- | --- |
| **`aug-cc-pVQZ-PP/C`** | — |

      - Cu--Kr, Y--Xe, Hf--Rn

| Item | Value |
| --- | --- |
| **`cc-pwCVDZ-PP/C`** | — |

      - Cu--Kr, Y--Xe, Hf--Rn
      - {rspan}`2` For use with the respective cc-pwCV$n$Z-PP orbital basis

| Item | Value |
| --- | --- |
| **`cc-pwCVTZ-PP/C`** | — |

      - Cu--Kr, Y--Xe, Hf--Rn

| Item | Value |
| --- | --- |
| **`cc-pwCVQZ-PP/C`** | — |

      - Cu--Kr, Y--Xe, Hf--Rn

| Item | Value |
| --- | --- |
| **`aug-cc-pwCVDZ-PP/C`** | — |

      - Cu--Kr, Y--Xe, Hf--Rn
      - {rspan}`2` For use with the respective aug-cc-pwCV$n$Z-PP orbital basis

| Item | Value |
| --- | --- |
| **`aug-cc-pwCVTZ-PP/C`** | — |

      - Cu--Kr, Y--Xe, Hf--Rn

| Item | Value |
| --- | --- |
| **`aug-cc-pwCVQZ-PP/C`** | — |

      - Cu--Kr, Y--Xe, Hf--Rn

| Item | Value |
| --- | --- |
| **`cc-pVDZ-F12-MP2Fit`** | — |

      - H--Ar
      - {rspan}`2` For use with the respective cc-pV$n$Z-F12 orbital basis

| Item | Value |
| --- | --- |
| **`cc-pVTZ-F12-MP2Fit`** | — |

      - H--Ar

| Item | Value |
| --- | --- |
| **`cc-pVQZ-F12-MP2Fit`** | — |

      - H--Ar

| Item | Value |
| --- | --- |
| **`cc-pVDZ-PP-F12-MP2Fit`** | — |

      - Ga--Kr, In--Xe, Tl--Rn
      - {rspan}`2` For use with the respective cc-pV$n$Z-PP-F12 orbital basis

| Item | Value |
| --- | --- |
| **`cc-pVTZ-PP-F12-MP2Fit`** | — |

      - Ga--Kr, In--Xe, Tl--Rn

| Item | Value |
| --- | --- |
| **`cc-pVQZ-PP-F12-MP2Fit`** | — |

      - Ga--Kr, In--Xe, Tl--Rn

| Item | Value |
| --- | --- |
| **`cc-pCVDZ-F12-MP2Fit`** | — |

      - Li--Ar
      - {rspan}`2` For use with the respective cc-pCV$n$Z-F12 orbital basis

| Item | Value |
| --- | --- |
| **`cc-pCVTZ-F12-MP2Fit`** | — |

      - Li--Ar

| Item | Value |
| --- | --- |
| **`cc-pCVQZ-F12-MP2Fit`** | — |

      - Li--Ar

<a id="sec:essentialelements.basisset.aux.cabs"></a>
### Complementary auxiliary basis sets for F12 (`CABS`)
The available CABS options for [F12 methods](sec:modelchemistries.mdci.expcorrelation)
are listed in [tab:essentialelements.basisset.aux.cabs](#tab:essentialelements.basisset.aux.cabs).

<a id="tab:essentialelements.basisset.aux.cabs"></a>
!!! note "Available complementary auxiliary basis sets for F12 methods."
    :header-rows: 1
    :class: longtable
    :class: footnotesize

| Item | Value |
| --- | --- |
| **Keyword** | — |

      - Elements
      - Comment

| Item | Value |
| --- | --- |
| **`cc-pVDZ-F12-CABS`** | — |

      - H, B--Ne, Al--Ar
      - {rspan}`2` For use with the respective cc-pV$n$Z-F12 orbital basis

| Item | Value |
| --- | --- |
| **`cc-pVTZ-F12-CABS`** | — |

      - H, B--Ne, Al--Ar

| Item | Value |
| --- | --- |
| **`cc-pVQZ-F12-CABS`** | — |

      - H, B--Ne, Al--Ar

| Item | Value |
| --- | --- |
| **`cc-pVDZ-F12-OptRI`** | — |

      - H--Ar
      - {rspan}`2` Identical to the cc-pV$n$Z-F12-CABS basis above

| Item | Value |
| --- | --- |
| **`cc-pVTZ-F12-OptRI`** | — |

      - H--Ar

| Item | Value |
| --- | --- |
| **`cc-pVQZ-F12-OptRI`** | — |

      - H--Ar

| Item | Value |
| --- | --- |
| **`cc-pVDZ-PP-F12-OptRI`** | — |

      - Ga--Kr, In--Xe, Tl--Rn
      - {rspan}`2` For use with the respective cc-pV$n$Z-PP-F12 orbital basis

| Item | Value |
| --- | --- |
| **`cc-pVTZ-PP-F12-OptRI`** | — |

      - Ga--Kr, In--Xe, Tl--Rn

| Item | Value |
| --- | --- |
| **`cc-pVQZ-PP-F12-OptRI`** | — |

      - Ga--Kr, In--Xe, Tl--Rn

| Item | Value |
| --- | --- |
| **`aug-cc-pVDZ-PP-OptRI`** | — |

      - Cu--Zn, Ag--Cd, Au--Hg
      - {rspan}`3` For use with the respective aug-cc-pV$n$Z-PP-F12 orbital basis

| Item | Value |
| --- | --- |
| **`aug-cc-pVTZ-PP-OptRI`** | — |

      - Cu--Zn, Ag--Cd, Au--Hg

| Item | Value |
| --- | --- |
| **`aug-cc-pVQZ-PP-OptRI`** | — |

      - Cu--Zn, Ag--Cd, Au--Hg

| Item | Value |
| --- | --- |
| **`aug-cc-pV5Z-PP-OptRI`** | — |

      - Cu--Zn, Ag--Cd, Au--Hg

| Item | Value |
| --- | --- |
| **`cc-pCVDZ-F12-OptRI`** | — |

      - Li--Ar
      - {rspan}`2` For use with the respective cc-pCV$n$Z-PP-F12 orbital basis

| Item | Value |
| --- | --- |
| **`cc-pCVTZ-F12-OptRI`** | — |

      - Li--Ar

| Item | Value |
| --- | --- |
| **`cc-pCVQZ-F12-OptRI`** | — |

      - Li--Ar

| Item | Value |
| --- | --- |
| **`aug-cc-pwCVDZ-PP-OptRI`** | — |

      - Cu--Zn, Ag--Cd, Au--Hg
      - {rspan}`3` For use with the respective aug-cc-pwCV$n$Z-PP-F12 orbital basis

| Item | Value |
| --- | --- |
| **`aug-cc-pwCVTZ-PP-OptRI`** | — |

      - Cu--Zn, Ag--Cd, Au--Hg

| Item | Value |
| --- | --- |
| **`aug-cc-pwCVQZ-PP-OptRI`** | — |

      - Cu--Zn, Ag--Cd, Au--Hg

| Item | Value |
| --- | --- |
| **`aug-cc-pwCV5Z-PP-OptRI`** | — |

      - Cu--Zn, Ag--Cd, Au--Hg

<a id="sec:essentialelements.basisset.aux.autoaux"></a>
### Automatic Generation of Auxiliary Basis Sets (AutoAux)

If no auxiliary basis set is available for your chosen orbital basis
set, one can be generated automatically by ORCA using the keyword
`AutoAux`. This is specified as any other fitting basis set: as a value
to the `AuxJ/AuxJK/AuxC` variables in the `%basis` block or as a
separate keyword in the simple input line (in which case all three Aux
slots are populated with identical fitting basis sets). `AutoAux` can
also be assigned to individual elements or atoms -- see sections
[sec:essentialelements.basisset.element](#sec:essentialelements.basisset.element) and
[sec:essentialelements.basisset.atom](#sec:essentialelements.basisset.atom). The generated basis sets can be
used for Coulomb, exchange and correlation fitting and are as accurate
as the optimized auxiliary basis sets at the cost of being up to twice
as large.[autoaux](../../bibliography.md)
The available settings for `AutoAux` are given in 
[tab:essentialelements.basisset.keywords.block](#tab:essentialelements.basisset.keywords.block) with their default values.

!!! note
    The generation procedure in ORCA 3.1 was significantly different
    and does not produce the same results!
    For compatibility, the old version is still accessible via 
    the setting `OldAutoAux true` in the `%basis` block. 

Note that if the orbital basis set contains diffuse functions, as is the
case for the aug-cc-pVXZ sets, the AutoAux fitting basis may contain
(near-)linear dependencies. In this case, the Cholesky decomposition of
the Coulomb metric will fail and the program will likely crash. One may
print the offending auxiliary basis using `!PrintBasis` and manually
remove the most diffuse s- and/or p-functions, which will usually
resolve the problem. 
An alternative, automatic solution is also implemented --
see section [sec:essentialelements.basisset.lindep-pcd](#sec:essentialelements.basisset.lindep-pcd).

<a id="sec:essentialelements.basisset.ecps"></a>
## Effective Core Potentials

Starting from version 2.8.0, ORCA features effective core potentials
(ECPs). They are a good alternative to scalar relativistic all-electron
calculations if heavy elements are involved. This pertains to geometry
optimizations and energy calculations but may not be true for property
calculations.

In order to reduce the computational effort, the usually highly
contracted and chemically inert core basis functions can be eliminated
by employing ECPs. ECP calculations comprise a "valence-only" basis and
thus are subject to the frozen core approximation. Contributions due to
the core orbitals are accounted for by an effective one-electron
operator $U^{\text{core} }$ which replaces the interactions between core
and valence electrons and accounts for the indistinguishability of the
electrons. Its radial parts $U_l(r)$ are generally expressed as a linear
combination of Gaussian functions, while the angular dependence is
included through angular momentum projectors $|S^l_m\rangle$.

$$

U^{\text{core} } = U_L(r) + \sum\limits_{l=0}^{L-1} \sum\limits_{m=-l}^{l}\left|S^l_m \rangle \left[U_l(r) - U_L(r)\right]\langle S^l_m\right|

$$

$$

U_l = \sum\limits_k d_{kl}r^{n_{kl} } \exp (-\alpha_{kl}r^2)

$$ 

The maximum angular momentum $L$ is generally defined as
$l_{\text{max} }^{\text{atom} } + 1$. The parameters $n_{kl}$,
$\alpha_{kl}$ and $d_{kl}$ that are necessary to evaluate the ECP
integrals have been published by various authors, among them the
well-known Los Alamos (LANL) [hay1985chem](../../bibliography.md) and Stuttgart--Dresden (SD)
[fuentealba1982chem,szentpaly1982chem,fuentealba1983phys,stoll1984chem,fuentealba1985phys,dolg1987chem,igel1988mol,dolg1989chem,schwerdtfeger1989chem,dolg1989theor,andrae1990theor,kaupp1991chem,kuechle1991mol,dolg1991chem,dolg1992chem,bergner1993mol,dolg1993phys,dolg1993theor,haeussermann1993mol,kuechle1994chem,nicklass1995chem,leininger1996chem,leininger1996chemlett,leininger1997chem,schautz1998theor,wang1998theor,metz2000chem,metz2000theor,martin2001chem,cao2001chem,stoll2002comput,cao2002molec,peterson2003chem,petersonEtAl2003chem,figgen2005chem,lim2005chem,peterson2005theor,yang2005theor,lim2006chem,peterson2006phys,peterson2007chem,moritz2007theor,moritz2008theor,huelsen2009theor,figgen2009chem,weigand2009theor](../../bibliography.md)
parameter sets. Depending on the specific parametrization of the ECP,
relativistic effects can be included in a semiempirical fashion in an
otherwise nonrelativistic calculation. Introducing $U^{\text{core} }$
into the electronic Hamiltonian yields two types of ECP integrals, the
local (or type-1) integrals that arise because of the maximum angular
momentum potential $U_L$ and the semi-local (or type-2) integrals that
result from the projected potential terms. The evaluation of these
integrals in ORCA proceeds according to the scheme published by
Flores-Moreno et al.[flores2006comput](../../bibliography.md).

A selection of ECP parameters and associated basis sets is directly
accessible in ORCA through the internal ECP library (see  [table:ECP_keywords](#table:ECP_keywords) for a listing of keywords).

<a id="table:ECP_keywords"></a>
!!! note "Overview of library keywords for ECPs and associated basis sets available in ORCA."
    :header-rows: 1
    :class: footnotesize

| Item | Value |
| --- | --- |
| **ECP keyword** | — |

      - Core size[^coresize]
      - Elements
      - Valence basis sets

| Item | Value |
| --- | --- |
| **{cspan}`3` *Recommended*** | — |
| **{rspan}`1` `def-ECP`** | — |

      - 78
      - Fr--Ra
      - {rspan}`1` Karlsruhe def2 basis sets:\
        def-SV(P), def-SVP, def-TZVP, def-TZVPP, ma-def-TZVP\
        MINIX

| Item | Value |
| --- | --- |
| **60** | — |

      - Ac--Lr

| Item | Value |
| --- | --- |
| **{rspan}`3` `def2-ECP`** | — |

      - 28
      - Rb--Xe
      - {rspan}`3` Karlsruhe basis sets:\
        def2-SVP, def2-TZVP, etc.\
        def2-SVPD, def2-TZVPD, etc.\
        ma-def2-SVP, ma-def2-TZVP, etc.

| Item | Value |
| --- | --- |
| **46** | — |

      - Cs--La

| Item | Value |
| --- | --- |
| **28** | — |

      - Ce--Lu

| Item | Value |
| --- | --- |
| **60** | — |

      - Hf--Rn

| Item | Value |
| --- | --- |
| **{rspan}`5` `SK-MCDHF-RSC`** | — |

      - 10
      - Ca, Cu--Kr
      - {rspan}`5` Correlation-consistent basis sets:\
        cc-pV$n$Z-PP, aug-cc-pV$n$Z-PP,
        cc-pCV$n$Z-PP, aug-cc-pCV$n$Z-PP,
        cc-pwCV$n$Z-PP, aug-cc-pwCV$n$Z-PP
        ($n=$ D, T, Q, 5)
        cc-pV$n$Z-PP ($n=$ D, T, Q)

| Item | Value |
| --- | --- |
| **28** | — |

      - Sr--Xe

| Item | Value |
| --- | --- |
| **46** | — |

      - Ba

| Item | Value |
| --- | --- |
| **60** | — |

      - Hf--Rn

| Item | Value |
| --- | --- |
| **78** | — |

      - Ra

| Item | Value |
| --- | --- |
| **60** | — |

      - U

| Item | Value |
| --- | --- |
| **{rspan}`7` `HayWadt`[^lanl]** | — |

      - 10
      - Na--Cu
      - {rspan}`7` LANL basis sets:\
        LANL2DZ, LANL2TZ, LANL2TZ(f),
        LANL08, LANL08(f)

| Item | Value |
| --- | --- |
| **18** | — |

      - Zn

| Item | Value |
| --- | --- |
| **28** | — |

      - Ga--Ag

| Item | Value |
| --- | --- |
| **36** | — |

      - Cd

| Item | Value |
| --- | --- |
| **46** | — |

      - In--La

| Item | Value |
| --- | --- |
| **60** | — |

      - Hf--Au

| Item | Value |
| --- | --- |
| **68** | — |

      - Hg--Tl

| Item | Value |
| --- | --- |
| **78** | — |

      - Pb--Bi, U--Pu

| Item | Value |
| --- | --- |
| **{rspan}`2` `dhf-ECP`** | — |

      - 28
      - Rb--Xe
      - {rspan}`2` Karlsruhe dhf basis sets:
        dhf-SVP, dhf-TZVP, etc.

| Item | Value |
| --- | --- |
| **46** | — |

      - Cs--Ba

| Item | Value |
| --- | --- |
| **60** | — |

      - Hf--Rn, U

| Item | Value |
| --- | --- |
| **{rspan}`5` `vDZP-ECP`** | — |

      - 2
      - B--Mg
      - {rspan}`5` vDZP\
        *uniquely compiled for the use with vDZP*

| Item | Value |
| --- | --- |
| **10** | — |

      - Al--Zn

| Item | Value |
| --- | --- |
| **28** | — |

      - Ga--Cd

| Item | Value |
| --- | --- |
| **46** | — |

      - In--Lu

| Item | Value |
| --- | --- |
| **60** | — |

      - Hf--Hg

| Item | Value |
| --- | --- |
| **78** | — |

      - Tl--Rn

| Item | Value |
| --- | --- |
| **{rspan}`9` `CRENBL-ECP`** | — |

      - 2
      - Li--Mg
      - {rspan}`9` CRENBL

| Item | Value |
| --- | --- |
| **10** | — |

      - Al--Zn

| Item | Value |
| --- | --- |
| **28** | — |

      - Rb--Cd

| Item | Value |
| --- | --- |
| **36** | — |

      - In--Xe

| Item | Value |
| --- | --- |
| **46** | — |

      - Cs--La

| Item | Value |
| --- | --- |
| **54** | — |

      - Ce--Lu

| Item | Value |
| --- | --- |
| **60** | — |

      - Hf-Hg

| Item | Value |
| --- | --- |
| **68** | — |

      - Tl-Rn

| Item | Value |
| --- | --- |
| **78** | — |

      - Fr-Ts

| Item | Value |
| --- | --- |
| **92** | — |

      - Og

| Item | Value |
| --- | --- |
| **{cspan}`3` *Legacy definitions*** | — |
| **{rspan}`4` `def2-SD`** | — |

      - 28,MWB
      - Rb--Cd
      - {rspan}`4`

| Item | Value |
| --- | --- |
| **28,MDF[^legacy1]** | — |

      - In--Xe

| Item | Value |
| --- | --- |
| **46,MWB** | — |

      - Cs--La

| Item | Value |
| --- | --- |
| **60,MWB** | — |

      - Hf--Pt

| Item | Value |
| --- | --- |
| **60,MDF[^legacy2]** | — |

      - Au--Rn

| Item | Value |
| --- | --- |
| **{rspan}`7` `def-SD`** | — |

      - 28,MWB
      - Rb--Cd
      - {rspan}`7`

| Item | Value |
| --- | --- |
| **46,MWB** | — |

      - In--La

| Item | Value |
| --- | --- |
| **28,MWB** | — |

      - Ce--Lu

| Item | Value |
| --- | --- |
| **60,MWB** | — |

      - Hf--Pt

| Item | Value |
| --- | --- |
| **60,MDF[^legacy2]** | — |

      - Au, Hg, Rn

| Item | Value |
| --- | --- |
| **78,MWB** | — |

      - Tl--At

| Item | Value |
| --- | --- |
| **78,MDF** | — |

      - Fr, Ra

| Item | Value |
| --- | --- |
| **60,MWB** | — |

      - Ac--Lr

| Item | Value |
| --- | --- |
| **{rspan}`13` `SDD`** | — |

      - 2,SDF
      - Li, Be
      - {rspan}`13`

| Item | Value |
| --- | --- |
| **2,MWB** | — |

      - B--Ne

| Item | Value |
| --- | --- |
| **10,SDF** | — |

      - Na, Mg

| Item | Value |
| --- | --- |
| **10,MWB** | — |

      - Al--Ca

| Item | Value |
| --- | --- |
| **10,MDF** | — |

      - Sc--Ni

| Item | Value |
| --- | --- |
| **10,MWB** | — |

      - Cu-Zn

| Item | Value |
| --- | --- |
| **28,MWB** | — |

      - Ga--Sr

| Item | Value |
| --- | --- |
| **28,MHF** | — |

      - Y--Cd

| Item | Value |
| --- | --- |
| **28,MDF** | — |

      - Ge--Br, Rb--Xe

| Item | Value |
| --- | --- |
| **46,MWB** | — |

      - In--Ba

| Item | Value |
| --- | --- |
| **28,MWB** | — |

      - La--Lu

| Item | Value |
| --- | --- |
| **60,MWB** | — |

      - Hf--Hg

| Item | Value |
| --- | --- |
| **78,MWB** | — |

      - Tl--Rn

| Item | Value |
| --- | --- |
| **60,MWB** | — |

      - Ac--Lr

| Item | Value |
| --- | --- |
| **{rspan}`7` `LANL1`** | — |

      - 10
      - Na--Ar
      - {rspan}`7`

| Item | Value |
| --- | --- |
| **18** | — |

      - K--Zn

| Item | Value |
| --- | --- |
| **28** | — |

      - Ga--Kr

| Item | Value |
| --- | --- |
| **36** | — |

      - Rb--Cd

| Item | Value |
| --- | --- |
| **46** | — |

      - In--Xe

| Item | Value |
| --- | --- |
| **54** | — |

      - Cs--La

| Item | Value |
| --- | --- |
| **68** | — |

      - Hf--Tl

| Item | Value |
| --- | --- |
| **78** | — |

      - Pb, Bi

| Item | Value |
| --- | --- |
| **{rspan}`3` `LANL2`** | — |

      - 10
      - K--Cu
      - {rspan}`3`

| Item | Value |
| --- | --- |
| **28** | — |

      - Rb--Ag

| Item | Value |
| --- | --- |
| **46** | — |

      - Cs--La

| Item | Value |
| --- | --- |
| **60** | — |

      - Hf--Au

[^coresize]: Where applicable, reference method and data are given (S: single-valence-electron ion; M: neutral atom; HF: Hartree–Fock; WB: quasi-relativistic; DF: relativistic).
[^lanl]: Corresponds to LANL2 and to LANL1 where LANL2 is unavailable.
[^legacy1]: I: OLD-SD(28,MDF) for compatibility with TURBOMOLE.
[^legacy2]: Au, Hg: OLD-SD(60,MDF) for compatibility with TURBOMOLE.

!!! note
    Requesting some basis sets automatically assigns the matching ECP
    (except when using the `NewGTO` keyword): 
    for example, "def2" basis sets use the `def2-ECP`.
    For others, see the respective [basis set table entries](sec:essentialelements.basisset.builtin).

The simplest way to assign ECPs is by using the ECP keyword within the simple input line. 
The ECP keyword itself assigns *only* the effective core potential, not a valence basis set! 
As an example for an explicitly named ECP you could use

```orca
! def2-TZVP def2-SD
```

This would assign the def2-SD ECP according to the definition given in the table above. 
Without the def2-SD keyword ORCA would default to def2-ECP.

Assignment of ECPs can be done within the `%basis` block using the `ECP` and `NewECP` keywords,
as in the following example:

```orca
%basis
  ECP       "def2-ECP"     # All elements (for which the ECP is defined)
  NewECP Pt "def2-SD" end  # Different ECP for Pt
end
```

A variant of the `NewECP` keyword can be used for individual atoms
inside the geometry definition:

```orca
* xyz ...
  ...
  S   0.0  0.0  0.0  NewECP "SDD" end
  ...
*
```

Note that these keywords also only affect the ECP and not the valence basis set!

In case the basis set for an element/atom has been changed using the
`NewGTO` keyword (see sections
[sec:essentialelements.basisset.element](#sec:essentialelements.basisset.element) and
[sec:essentialelements.basisset.atom](#sec:essentialelements.basisset.atom) above) it may be necessary to
remove the ECP from that element/atom. This can be done with the
`DelECP` keyword in the `%basis` block or coordinates input,
respectively:

```orca
! LANL2DZ                   # Uses HayWadt ECPs by default, starting from Na
%basis
  NewGTO S "def2-TZVP" end  # All-electron up to Kr
  DelECP S                  # Remove HayWadt ECP
end
* xyz ...
...
Cu   0.0  0.0  0.0  
  DelECP                    # Remove HayWadt ECP
  NewGTO "def2-QZVPP" end   # All-electron up to Kr
...
*
```

To remove all ECPs loaded by default (e.g. in case no global basis set
is chosen) you can use the `!NoECP` simple keyword.

<a id="sec:essentialelements.basisset.ecps.manual"></a>
### Manual Input of ECP Parameters

To manually specify ECP parameters, the `NewECP` keyword is followed by
the element for which an ECP is to be entered, the number of core
electrons to be replaced (N_core) and the maximum angular momentum
(lmax). The ECP specification is finished by giving the definitions of
the individual shells that constitute the angular dependent potentials
U$_l$.

```orca
%basis 
    NewECP <element>
      N_core <number of core electrons>
      lmax <max. angular momentum>
      [shells]
    end
end
```

For each ECP shell, first the angular momentum $l$ has to be given,
followed by the number of primitives. The primitives themselves are then
specified by giving a running index and the respective tuple of exponent
$a_{kl}$, expansion coefficient $d_{kl}$ and radial power $n_{kl}$.

```orca
# ECP shell 
      l <number of primitives>
      1    a1l    d1l    n1l
      2    a2l    d2l    n3l
      ...
```

As an example, consider the SD(10,MDF) for Vanadium. The name indicates
a Stuttgart--Dresden type ECP that replaces 10 core electrons and is
derived from a relativistic calculation for the neutral atom. It
consists of 4 shells with angular momentum s, p, d, and f. Note
that the f shell has an expansion coefficient of 0.0 and thus will not
contribute at all to this effective core potential. This is typical for
all SD potentials (but may be different for program packages like
TURBOMOLE that do not support arbitrary angular momentum with respect to
the ECP and therefore use recontractions of the original parameter
sets).

```orca
%basis 
  # ECP SD(10,MDF) for V 
  # M. Dolg, U. Wedig, H. Stoll, H. Preuss,
  # J. Chem. Phys. 86, 866 (1987).  
  NewECP V 
    N_core 10 
    lmax f 
    s 2 
      1      14.4900000000    178.4479710000  2 
      2       6.5240000000     19.8313750000  2 
    p 2 
      1      14.3000000000    109.5297630000  2 
      2       6.0210000000     12.5703100000  2 
    d 2 
      1      17.4800000000    -19.2196570000  2 
      2       5.7090000000     -0.6427750000  2 
    f 1 
      1       1.0000000000      0.0000000000  2 
  end
end
```

### ECPs and Ghost Atoms

When ghost atoms are defined in the input 
(see section [sec:essentialelements.coordinates.special](#sec:essentialelements.coordinates.special)), 
ECPs are **not** added to these atoms by default. 
If that is somehow needed, please add `GhostECP true` under the `%basis` block.

```orca
%basis 
 GhostECP true
 AllowGhostECP true # synonym
end
```

<a id="sec:essentialelements.basisset.embeddingpotentials"></a>
### ECP Embedding

Computations on cluster models sometimes require the presence of
embedding potentials in order to account for otherwise neglected
repulsive terms at the border [giordano2001surf](../../bibliography.md). In order to simplify
these kind of calculations with ORCA the ECP embedding can be
accomplished quite easily:

```orca
*xyz ...
# atom>  charge x    y    z    optional ECP declaration
Zr>      4.0    0.0  0.0  0.0  NewECP "SDD" end
...
*
```

The declaration of such a coreless ECP center takes place in the
coordinates section by appending a bracket "\>" to the element symbol.
Note that embedding ECPs are treated as point charges in ORCA, so the
charge has to be given next. The coordinates of the coreless ECP center
have to be specified as usual and may be followed by an optional ECP
assignment. In general, calculations that employ an ECP embedding
procedure should be single point calculations. However if the need
arises to perform a geometry optimization, make sure to set up explicit
Cartesian constraints for the coreless ECP centers.

<a id="sec:essentialelements.basisset.element"></a>
## Assigning or Adding Basis Functions to an Element

In order to assign a new basis set to a given element, use:

```orca
%basis
  NewGTO 8    # New basis for oxygen.
# NewGTO O    # This works as well.
   S   3      # s-shell
    1  910.10034975         0.03280967
    2  137.19711335         0.23422391
    3   30.85279077         0.81490980
   0   2      # also an s-shell
    1     1.72885887         0.27389659
    2     0.39954770         0.79112437
   P   1
    1     8.35065975         1.00000000
  end
end
```

For simplicity and consistency the input format is the same as
that used in the [basis set files](sec:essentialelements.basisset.file). 
In this format, the first line carries the angular momentum of the shell to be added -- 
either as an integer, or as a label (s, p, d, f, g, h, i, k) -- and the number of primitives. 
Then for each primitive one line follows which has 
(a) the index of the primitive (1, 2, 3, ...) 
(b) the exponent of the primitive and 
(c) the contraction coefficient (unnormalized). 
There also is the possibility to include a `SCALE X` statement 
after the number of primitives in the first line 
to indicate that the basis function exponents should be scaled.

!!! warning
    - ORCA always uses spherical harmonic Gaussian functions. 
    - Angular momentum 7 is labeled as "k" -- 
      there are no j-shells in accepted spectroscopic conventions.
    - Combined s- and p-shells are sometimes labelled as "L-shells" in other programs.
      This is not supported in the `NewGTO` format and to avoid confusion, 
      shells with angular momentum 8 can only be specified with a number,
      and not with the label "l".

In order to add basis functions to the basis of a given element (for
example because you do not like the standard polarization functions) use
`AddGTO` instead of `NewGTO`. In `NewGTO` or `AddGTO` you can also use
the nicknames of internally stored basis sets. An example is:

```orca
%basis
  NewGTO 8    # new basis for oxygen
   "6-31G"
    D  1 
    1  0.4  1.0
  end
end
```

In this example the 6-31G basis is assigned to oxygen and in addition a
polarization function with exponent 0.4 is added to the oxygen basis.

Note that the `NewGTO` keyword does not change the ECP for the given
element -- you must use `NewECP` or `DelECP` (see section
[sec:essentialelements.basisset.ecps](#sec:essentialelements.basisset.ecps)).

A similar mechanism was established for the auxiliary basis sets in RI
calculations:

```orca
%basis
  NewAuxJGTO 8    # new auxiliary basis for oxygen
    s  1 
    1  350  1.0
    ... etc
  end
  AddAuxJGTO 8   # add a shell to the auxiliary basis for 
                # oxygen
    D  1 
    1  0.8  1.0
  end
end
```

New basis functions can be specifically assigned to any auxiliary basis
sets. The keywords `NewAuxCGTO`, `AddAuxCGTO`, `NewAuxJKGTO`,
`AddAuxJKGTO`, `NewCABSGTO`, `AddCABSGTO` are used in the same way. The
keywords `NewAuxGTO` and `AddAuxGTO` are the same as `NewAuxJGTO` and
`AddAuxJGTO`, that is, they only influence the Coulomb auxiliary basis
(`AuxJ`)!

<a id="sec:essentialelements.basisset.atom"></a>
## Assigning or Adding Basis Functions to Individual Atoms

Sometimes you may want to not treat all atoms of the same element with the same basis
set but to assign a specific basis set to a specific atom in the
molecules. This is also possible in ORCA and takes place in the
coordinate section (`%coords`, `*xyz`, etc.). The format is the same as
described above. An example may help to make things clear:

```orca
*int 0 1
  C  0 0 0 0.00   0.0   0.00
   AddGTO
     D  1 
      1  1.0  1.0
   end
  O  1 0 0 1.13   0.0   0.00
   NewGTO
     "6-311G"
     D  1 
      1  1.2  1.0
   end
*
```

In this example an extra d-shell with exponent 1.0 is added to the first
carbon atom and the basis for the oxygen atom is changed to `6-311G`
with an extra d-function of exponent 1.2 added.

Analogously, `AUX` basis functions can be assigned or added to
individual atoms using the keywords `NewAuxJGTO`, `AddAuxJGTO`,
`NewAuxCGTO`, `AddAuxCGTO`, `NewAuxJKGTO`, `AddAuxJKGTO`, `NewCABSGTO`,
`AddCABSGTO`.

A note on the use of `AutoAux`: if you change the basis set on a given
atom and want to generate a fitting basis, you have to specify it again
in the coordinates section, even if `AutoAux` is already present in the
simple input line or in the `%basis` block. For example:

```orcainput
! def2-SVP def2/JK
%basis
  NewAuxJKGTO H
    "AutoAux"
  end
end
*xyz 0 1
  O  0.00 0.00 0.00
  H -0.25 0.93 0.00
  H  0.96 0.00 0.00
   AddGTO
     P 1
      1 1.6 1.0
     D 1
      1 1.0 1.0
   end
   NewAuxJKGTO
     "AutoAux"
   end
*
```

Here the oxygen atom is assigned the def2-SVP basis and the def2/JK
fitting basis, the first hydrogen atom is assigned the def2-SVP basis
and an automatically generated fitting basis and the second hydrogen
atom is assigned the def2-SVP basis with two additional polarization
functions and a larger automatically generated fitting basis that
accounts for these functions.

!!! note
    When assigning custom basis sets it is always a good idea to
    print the basis set information (`%output print[p_basis] 2 end` or
    simply `!PrintBasis`) and check that everything is correct.

<a id="sec:essentialelements.basisset.fragments"></a>
## Assigning Basis Sets and ECPs to Fragments

In multi-level or QM/QM calculations it may be convenient to assign
different basis sets to different [fragments](sec:essentialelements.fragmentation). 
This can be done with the keywords `FragBasis`, `FragAuxJ`, `FragAuxJK`, `FragAuxC`, 
`FragCABS`, and `FragECP` in the `%basis` block, followed by the number of the
fragment (numbering starts at 1!) and a standard basis set or ECP from
the ORCA library (see
[sec:essentialelements.basisset.builtin](#sec:essentialelements.basisset.builtin) and
[table:ECP_keywords](#table:ECP_keywords)). Note that unlike the `NewGTO` keyword,
`FragBasis` also changes the ECP, if applicable. Fragment basis sets
will overload the global or element-specific
([sec:essentialelements.basisset.element](#sec:essentialelements.basisset.element)) choice but can be overloaded
for individual atoms
([sec:essentialelements.basisset.atom](#sec:essentialelements.basisset.atom)). If AutoAux is requested for a
fragment, it will be generated for the actual orbital basis set chosen
for each atom, even if it is changed in the coordinates section.
However, if AutoAux was requested for an element or in the simple input,
the auxiliary basis will be generated before the fragment basis is
assigned (which is not desired), therefore AutoAux must be requested
again for the fragment. An example is given below:

```orca
! PrintBasis BP86 NoIter
! def2-SVP def2/J
%basis
  FragBasis 1 "def2-TZVP"
  FragBasis 2 "cc-pVTZ-PP"
  FragAuxJ  2 "AutoAux"
  FragECP   3 "SK-MCDHF-RSC"
  FragAuxJ  3 "def2/JK"
end
*xyz 0 1
  H(1) 0 0 0
  I(1) 0 0 1.6
  H(2) 0 5 0   NewGTO "cc-pVTZ" end
  I(2) 0 5 1.6
  H(3) 5 0 0
  I(3) 5 0 1.6
*
# Final basis sets:
# Atom Basis      ECP          AuxJ
# 0H   def2-TZVP  def2-ECP     def2/J
# 1I   def2-TZVP  def2-ECP     def2/J
# 2H   cc-pVTZ    -            AutoAux(cc-pVTZ)
# 3I   cc-pVTZ-PP SK-MCDHF-RSC AutoAux(cc-pVTZ-PP)
# 4H   def2-SVP   -            def2/JK
# 5I   def2-SVP   SK-MCDHF-RSC def2/JK
```

It is also possible to read fragment-specific basis sets from a file.
The syntax is analogous, using the keywords `ReadFragBasis`,
`ReadFragAuxJ`, `ReadFragAuxJK`, `ReadFragAuxC`, `ReadFragCABS`, and
`ReadFragECP`. In this case, the input string is expected to be an
existing basis set file in GAMESS-US format (see
section [sec:essentialelements.basisset.file](#sec:essentialelements.basisset.file)). All other details above
(e.g., regarding ECPs and AutoAux) also apply here.

!!! note
    -  Details regarding the assignment of fragments can be found in [Fragment Specification](#sec:essentialelements.fragmentation) section.

<a id="sec:essentialelements.basisset.file"></a>
## Reading Basis Sets from a File

By using the variables `GTOName`, `GTOAuxJName`, `GTOAuxJKName`,
`GTOAuxCName`, and `GTOCABSName` (`GTOAuxName` is a synonym for
`GTOAuxJName`) a basis set can be read from an ASCII file. In this way
you can construct or modify your favorite standard basis set and load it
easily into the program.

```orca
%basis
  GTOName      = "MyBasis.bas"      # read orbital basis
  GTOAuxJName  = "MyAuxJBasis.bas"  # read Coulomb-fitting basis
  GTOAuxJKName = "MyAuxJKBasis.bas" # read Coulomb- and exchange-fitting basis
  GTOAuxCName  = "MyAuxCBasis.bas"  # read correlation-fitting basis
  GTOCABSName  = "MyCABSBasis.bas"  # read complementary auxiliary basis set
end
```

A word of caution: under Windows, backslashes directory assignments
must be given twice to be correctly understood! The format is that used
for "GAMESS-US" in the EMSL library [basissets](../../bibliography.md). To give an example of
what this format looks like here is a part of the `3-21GSP` basis of
Buenker and coworkers [mitin1996chem,mitin1997comp](../../bibliography.md):

```orca
!                         lines in the beginning with '!' or '#' are comments
! BASIS="3-21GSP"
!Elements                             References                                
!--------                             ----------                                
! H - Ne: A.V. Mitin, G. Hirsch, R. J. Buenker, Chem. Phys. Lett. 259, 151 (1996)
! Na - Ar: A.V. Mitin, G. Hirsch, R. J. Buenker, J. Comp. Chem. 18, 1200 (1997). 
!
$DATA        ! Optional
HYDROGEN     ! (3s) -> [2s]      Element symbols are also recognized
 S   2
  1           4.50036231         0.15631167
  2           0.68128924         0.90466909
 S   1
  1           0.15137639         1.00000000
CARBON       ! (6s,3p) -> [3s,2p]                                
 S   3
  1         499.24042249         0.03330322
  2          75.25419194         0.23617745
  3          16.86538669         0.81336259
 L   2       ! L shells are a s and a p shell with identical exponents
  1           0.89739483         0.24008573         0.46214684
  2           0.21746772         0.81603757         0.66529098
 L   1
  1           4.52660451         1.00000000         1.00000000
$END         ! Optional
```

The file format for the auxiliary basis sets is exactly the same. Basis
sets can be also exported in GAMESS-US format by the `orca_exportbasis`
utility (section
[sec:utilities.exportbasis](#sec:utilities.exportbasis)). Note that in order to
read basis sets printed by ORCA (using `!PrintBasis`), the `NewGTO` and
`end` keywords must be removed.

!!! warning
    - Angular momentum 7 is labeled as "k" -- 
      there are no j-shells in accepted spectroscopic conventions.
    - To avoid confusion with combined s- and p-shells,
      shells with angular momentum 8 can only be specified with a number,
      and not with the label "l".

<a id="sec:essentialelements.lindep"></a>
## Linear Dependence

The previous sections describe the assessment of a desired molecular
basis set from appropriately parametrized functions at various locations
within the molecule (normally centered on atoms). The parametrization of
these functions is such that the chance for redundancy is minimal. Since
however, one is limited to work with finite numerical precision, and
furthermore these parameters also depend on the molecular geometry,
redundancies cannot be completely eliminated in advance. Redundancy
means that the subspace spanned by the given basis functions at given
values of parameters (including geometry), can be identically spanned by
a smaller number of *linear independent* basis functions. Linear
dependent (redundant) function sets however may cause numerical
instabilities. Linear dependence is normally identified by searching for
zero eigenvalues of the overlap matrix. Note that the inverse of the
overlap (or related matrices) are used for orthogonalization purposes,
and it follows that if near zero eigenvalues are not treated properly,
the inverse becomes ill-defined, and the SCF procedure numerically
unstable.

From the previous discussion, it is evident that the crucial parameter
for curing linear dependence is the threshold below which an overlap
eigenvalue is considered zero. This parameter may be changed using the
following keyword

```orca
%scf
  sthresh 1e-6 # default 1e-7
end
```

Although there is no strict limit for the value of the above parameter,
it should reasonably be somewhere between 1e-5 and 1e-8 (the default is 1e-7). One may get away with 1e-9 or perhaps even lower without
convergence problem, but there is a risk that the result is contaminated
with noise caused by the near zero vectors. In difficult cases, an 1e-6
threshold was often found to work smoothly, and above that one risks
throwing away more and more functions, which also influence
comparability of results with other calculations. To monitor the
behavior of the small eigenvalues, one should look for the following
block in the output

```orca
Diagonalization of the overlap matrix:
Smallest eigenvalue                        ... -1.340e-17
Time for diagonalization                   ...    0.313 sec
Threshold for overlap eigenvalues          ... 1.000e-07
Number of eigenvalues below threshold      ... 1
Smallest eigenvalue above threshold        ... 6.013e-07
Time for construction of square roots      ...    0.073 sec
Total time needed                          ...    0.387 sec
```

Here, the smallest eigenvalue is printed, along with the currently used
overlap threshold, and the number of functions below this (which will be
dropped). It is a recommended consistency check to look for an equal
number of zero entries among orbital energies once the SCF procedure
converged. Note that for functions belonging to zero eigenvalues *no
level shifts* are applied!

In case that redundant vectors were removed from the basis,
`! MORead NoIter` should only be used in conjunction with the same 
`SThresh` as in the original calculation, otherwise the results will
be inconsistent. 
`! MORead` may still be used together with a change in `SThresh`, 
but a few SCF iterations will be required.

<a id="sec:essentialelements.basisset.lindep-diffsthresh"></a>
### Automatic Adjustments for Near Linear-Dependent Cases

Starting from ORCA6, there is now a keyword called DiffSThresh, which controls
an automatic tightening of the integral cutoff parameters Thresh and TCut
in case small eigenvalues of the overlap matrix are found. We found this
to be important in some calculations using diffuse basis, and these parameters are
set to a minimum value of `Thresh=1e-12` and `TCut=1e-13` in case the "Smallest eigenvalue"
shown above gets below that number. If the cutoffs are already tighter than
that, for instance when using `!VeryTightSCF`, than nothing will happen.

We found empirically that these are safe numbers to mitigate noise and 
increase the robustness of the SCF procedure, thus they are enforced by default. 
The default is 1e-6 and this can be turned off by setting `%SCF DiffSThresh -1 END`
 on the input in case you don't want this automatic adjustment to happen.

<a id="sec:essentialelements.basisset.lindep-pcd"></a>
### Removal of Redundant Basis Functions

While the approach described above is usually successful in removing
linear dependencies from the orbital basis set, the auxiliary basis used
in RI is not orthogonalized the same way. Instead, the RI linear
equation system is solved using a Cholesky decomposition (CD) of the
auxiliary basis Coulomb metric. If the auxiliary basis is redundant, the
CD fails and the program usually aborts. One simple solution implemented
in ORCA is to perform a pivoted Cholesky decomposition (PCD) of the
metric, terminating at a given threshold. Then, the shells contributing
to the nullspace are removed from the basis at the beginning of the
calculation. This can be requested for any of the basis sets using
either the overlap or the Coulomb metric. It is most appropriate for the
AuxJ/AuxJK/AuxC basis using the Coulomb metric. The truncated basis can
be examined using the `!PrintBasis` keyword. Often, functions may be
removed for some atoms of a given element, but kept for others. As long
as the threshold is low enough, i.e. only truly redundant functions are
removed, this should not affect the molecular symmetry of the results.

```orca
%basis
  PCDTrimBas   Overlap # Trim the orbital basis in the overlap metric
  PCDTrimAuxJ  Coulomb # Trim the AuxJ basis in the Coulomb metric
  PCDTrimAuxJK Coulomb # Trim the AuxJK basis in the Coulomb metric
  PCDTrimAuxC  Coulomb # Trim the AuxC basis in the Coulomb metric
  PCDThresh    -1      # Threshold for the PCD: chosen automatically if <0
end
```

<a id="sec:essentialelements.basisset.methods"></a>
## Which Methods Need Which Basis Sets?

ORCA offers a variety of methods and a large choice of 
[orbital](sec:essentialelements.basisset.builtin) 
and [auxiliary](sec:essentialelements.basisset.aux) 
basis sets to go with them. 
Pure (GGA or meta-GGA) [DFT](sec:modelchemistries.dft) functionals 
only require the calculation of Coulomb integrals,
while [hybrid DFT](sec:modelchemistries.dft.hybriddft), 
HF (and by extension, all post-HF electron correlation methods, 
such as [MP2](sec:modelchemistries.mp2) and [coupled cluster](sec:modelchemistries.mdci)), 
as well as [CASSCF](sec:modelchemistries.casscf) (and [NEVPT2](sec:modelchemistries.nevpt2)), 
require the calculation of Coulomb and exchange integrals.
- An orbital basis set (`<basis>`) is always needed for these methods.
- If RI is used for Coulomb integrals ([RI-J](sec:essentialelements.ri.rij), 
  [RIJDX/RIJONX](sec:essentialelements.ri.rijonx), 
  [RIJCOSX](sec:essentialelements.ri.rijcosx)), 
  `AuxJ` is needed (usually `<basis>/J` or `def2/J`).
- If RI is also used for exchange integrals ([RI-JK](sec:essentialelements.ri.rijk)), 
  `AuxJK` is needed instead (usually `<basis>/JK` or `def2/JK`).
- If RI is used for integral generation in post-SCF correlation methods, 
  as in [RI-MP2](sec:modelchemistries.mp2.ri) 
  (including [double-hybrid DFT](sec:modelchemistries.dft.doublehybriddft)), 
  [DLPNO-MP2](sec:modelchemistries.mp2.dlpno), 
  and [DLPNO-CC](sec:modelchemistries.mdci.localcorrelation), 
  `AuxC` is also needed (usually `<basis/C>`).
- In [F12 methods](sec:modelchemistries.mdci.expcorrelation), 
  a specialized orbital basis is used (`<basis>-F12`) 
  and `CABS` is needed in addition (usually `<basis>-F12-CABS` or `<basis>-F12-OptRI`).

An overview of auxiliary basis requirements for an inexhaustive list of 
methods and approximations is given in [tab:essentialelements.basisset.methods](#tab:essentialelements.basisset.methods).

<a id="tab:essentialelements.basisset.methods"></a>
!!! note "Simple input keywords for basis sets and ECPs."
    :class: footnotesize
    | Method          | Approximation     | Basis sets                                                       |
    |:----------------|:------------------|:-----------------------------------------------------------------|
    | HF              | NoRI (default)    | `<basis>`                                                        |
    | HF              | RIJONX or RIJCOSX | `<basis>` + `<basis>/J`                                          |
    | HF              | RI-JK             | `<basis>` + `<basis>/JK`                                         |
    | pure DFT        | RI (default)      | `<basis>` + `<basis>/J`                                          |
    | hybrid DFT      | NoRI              | `<basis>`                                                        |
    | hybrid DFT      | RIJCOSX (default) | `<basis>` + `<basis>/J`                                          |
    | hybrid DFT      | RI-JK             | `<basis>` + `<basis>/JK`                                         |
    | CASSCF/NEVPT2   |                   | `<basis>`                                                        |
    | CASSCF/NEVPT2   | RI-JK             | `<basis>` + `<basis>/JK`                                         |
    | CASSCF/NEVPT2   | RIJCOSX           | `<basis>` + `<basis>/J` + `<basis>/C`                            |
    | CASSCF/NEVPT2   | TrafoStep RI      | `<basis>` + `<basis>/JK` or `<basis>/C`                          |
    | NEVPT2-F12      | TrafoStep RI      | `<basis>-F12` + `<basis>-F12-CABS` + `<basis>/JK` or `<basis>/C` |
    | TDDFT           |                   | `<basis>`                                                        |
    | MP2             |                   | `<basis>`                                                        |
    | RI-MP2          |                   | `<basis>` + `<basis>/C`                                          |
    | RI-MP2          | RI-JK             | `<basis>` + `<basis>/C` + `<basis>/JK`                           |
    | F12-MP2         |                   | `<basis>-F12` + `<basis>-F12-CABS`                               |
    | F12-RI-MP2      |                   | `<basis>-F12` + `<basis>-F12-CABS` + `<basis>/C`                 |
    | DLPNO-MP2       |                   | `<basis>` + `<basis>/C`                                          |
    | DLPNO-MP2       | RIJCOSX           | `<basis>` + `<basis>/C` + `<basis>/J`                            |
    | F12-DLPNO-MP2   |                   | `<basis>-F12` + `<basis>-F12-CABS` + `<basis>/C`                 |
    | CCSD            |                   | `<basis>`                                                        |
    | RI-CCSD         |                   | `<basis>` + `<basis>/C`                                          |
    | DLPNO-CCSD      |                   | `<basis>` + `<basis>/C`                                          |
    | DLPNO-CCSD      | RIJCOSX           | `<basis>` + `<basis>/C` + `<basis>/J`                            |
    | F12-CCSD        |                   | `<basis>-F12` + `<basis>-F12-CABS`                               |
    | F12-RI-CCSD     |                   | `<basis>-F12` + `<basis>-F12-CABS` + `<basis>/C`                 |
    | F12-RI-CCSD     | RI-JK             | `<basis>-F12` + `<basis>-F12-CABS` + `<basis>/C` + `<basis>/JK`  |

<a id="sec:essentialelements.basisset.keywords"></a>
## Keywords

<a id="tab:essentialelements.basisset.keywords.simple"></a>
!!! note "Simple input keywords for basis sets and ECPs."
    :class: footnotesize
    | Keyword             | Description                                                                                                                 |
    |:--------------------|:----------------------------------------------------------------------------------------------------------------------------|
    | `<BasisName>`       | Assign the respective [orbial basis set](sec:essentialelements.basisset.builtin) to all elements                            |
    | `<AUXJName>`        | Assign the respective [`AuxJ` basis set](sec:essentialelements.basisset.aux.auxj) to all elements                           |
    | `<AUXJKName>`       | Assign the respective [`AuxJK` basis set](sec:essentialelements.basisset.aux.auxjk) to all elements                         |
    | `<AUXCName>`        | Assign the respective [`AuxJC` basis set](sec:essentialelements.basisset.aux.auxc) to all elements                          |
    | `<CABSName>`        | Assign the respective [`CABS`](sec:essentialelements.basisset.aux.cabs) to all elements                                     |
    | `AutoAux`           | Automatically generate AuxJ, AuxJK, and AuxC auxiliary basis sets (see [sec:essentialelements.basisset.aux.autoaux](#sec:essentialelements.basisset.aux.autoaux))|
    | `<ECPName>`         | Assign the respective ECP to all elements for which it is defined                                                           |
    | `NoECP`             | Remove the default ECP                                                                                                      |
    | `Decontract`        | Decontract all (orbital and auxiliary) basis sets                                                                           |
    | `DecontractBas`     | Decontract the orbital basis sets                                                                                           |
    | `NoDecontractBas`   | Do not decontract the basis set                                                                                             |
    | `DecontractAuxJ`    | Decontract the AuxJ basis set                                                                                               |
    | `NoDecontractAuxJ`  | Do not decontract the AuxJ basis                                                                                            |
    | `DecontractAuxJK`   | Decontract the AuxJK basis set                                                                                              |
    | `NoDecontractAuxJK` | Do not decontract the AuxJK basis                                                                                           |
    | `DecontractAuxC`    | Decontract the AuxC basis set                                                                                               |
    | `NoDecontractAuxC`  | Do not decontract the AuxC basis                                                                                            |

<a id="tab:essentialelements.basisset.keywords.block"></a>
!!! note "`%basis` block input keywords for basis sets and ECPs."
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
| **`Basis`** | — |

      - `"<BasisName>"`
      - Define the [orbital basis set](sec:essentialelements.basisset.builtin)

| Item | Value |
| --- | --- |
| **`AuxJ`** | — |

      - `"<AuxName>"`
      - Define the [J auxiliary basis set](sec:essentialelements.basisset.aux.auxj)

| Item | Value |
| --- | --- |
| **`AuxJK`** | — |

      - `"<AuxName>"`
      - Define the [JK auxiliary basis set](sec:essentialelements.basisset.aux.auxjk)

| Item | Value |
| --- | --- |
| **`AuxC`** | — |

      - `"<AuxName>"`
      - Define the [correlation auxiliary basis set](sec:essentialelements.basisset.aux.auxc)

| Item | Value |
| --- | --- |
| **`CABS`** | — |

      - `"<CABSName>"`
      - Define the [complementary auxiliary basis set](sec:essentialelements.basisset.aux.cabs) for F12 calculations

| Item | Value |
| --- | --- |
| **`ECP`** | — |

      - `"<ECPName>"`
      - Assign the respective [ECP](sec:essentialelements.basisset.ecps) to all elements for which it is available

| Item | Value |
| --- | --- |
| **`GhostECP`** | — |

      - `false`
      - Activate ECPs on ghost atoms

| Item | Value |
| --- | --- |
| **`AllowGhostECP`** | — |

      - `false`
      - Equivalent to `GhostECP`

| Item | Value |
| --- | --- |
| **{cspan}`2` Decontraction options** | — |
| **`Decontract`** | — |

      - `false`
      - If `true`, decontract all basis sets

| Item | Value |
| --- | --- |
| **`DecontractBas`** | — |

      - `false`
      - If `true`, decontract the orbital basis set

| Item | Value |
| --- | --- |
| **`DecontractAuxJ`** | — |

      - `false`
      - If `true`, decontract the AuxJ basis set

| Item | Value |
| --- | --- |
| **`DecontractAuxJK`** | — |

      - `false`
      - If `true`, decontract the AuxJK basis set

| Item | Value |
| --- | --- |
| **`DecontractAuxC`** | — |

      - `false`
      - If `true`, decontract the AuxC basis set

| Item | Value |
| --- | --- |
| **`DecontractCABS`** | — |

      - `true`
      - If `false`, do not decontract the CABS

| Item | Value |
| --- | --- |
| **{cspan}`2` Setting basis sets for elements (see [sec:essentialelements.basisset.element](#sec:essentialelements.basisset.element))** | — |
| **`NewGTO`** | — |

      - `<Element> "<BasisName>" <shells> End`  
      - Define new `Basis` for element via built-in name and/or custom shells 

| Item | Value |
| --- | --- |
| **`AddGTO`** | — |

      - `<Element> <shells> End`
      - Add GTO shells to basis for element

| Item | Value |
| --- | --- |
| **`NewAuxJGTO`** | — |

      - `<Element> "<AuxName>" <shells> End`
      - Define new `AuxJ` set for element via built-in name and/or custom shells

| Item | Value |
| --- | --- |
| **`AddAuxJGTO`** | — |

      - `<Element> <shells> End`
      - Add GTO shells to `AuxJ` for element

| Item | Value |
| --- | --- |
| **`NewAuxJKGTO`** | — |

      - `<Element> "<AuxName>" <shells> End`
      - Define new `AuxJK` set for element via built-in name and/or custom shells

| Item | Value |
| --- | --- |
| **`AddAuxJKGTO`** | — |

      - `<Element> <shells> End`
      - Add GTO shells to `AuxJK` for element

| Item | Value |
| --- | --- |
| **`NewAuxCGTO`** | — |

      - `<Element> "<AuxName>" <shells> End`
      - Define new `AuxC` set for element via built-in name and/or custom shells

| Item | Value |
| --- | --- |
| **`AddAuxCGTO`** | — |

      - `<Element> <shells> End`
      - Add GTO shells to `AuxC` for element

| Item | Value |
| --- | --- |
| **`NewCABSGTO`** | — |

      - `<Element> "<CABSName>" <shells> End`
      - Define new `CABS` set for element via built-in name and/or custom shells

| Item | Value |
| --- | --- |
| **`AddCABSGTO`** | — |

      - `<Element> <shells> End`
      - Add GTO shells to `CABS` for element

| Item | Value |
| --- | --- |
| **{rspan}`1` `NewECP`** | — |

      - `<Element> "<ECPName>" End`
      - Define new built-in ECP for element

| Item | Value |
| --- | --- |
| **`<Element> <shells> End`** | — |

      - Manually define new ECP for element (see [sec:essentialelements.basisset.ecps.manual](#sec:essentialelements.basisset.ecps.manual))

| Item | Value |
| --- | --- |
| **`DelECP`** | — |

      - `<Element>`
      - Remove the ECP for the element

| Item | Value |
| --- | --- |
| **{cspan}`2` Setting basis sets for fragments (see [sec:essentialelements.basisset.fragments](#sec:essentialelements.basisset.fragments))** | — |
| **`FragBasis`** | — |

      - `<FragID> "<BasisName>"`
      - Define `Basis` for fragment

| Item | Value |
| --- | --- |
| **`FragAuxJ`** | — |

      - `<FragID> "<AuxName>"`
      - Define `AuxJ` for fragment

| Item | Value |
| --- | --- |
| **`FragAuxJK`** | — |

      - `<FragID> "<AuxName>"`
      - Define `AuxJK` for fragment

| Item | Value |
| --- | --- |
| **`FragAuxC`** | — |

      - `<FragID> "<AuxName>"`
      - Define `AuxC` for fragment

| Item | Value |
| --- | --- |
| **`FragCABS`** | — |

      - `<FragID> "<CABSName>"`
      - Define `CABS` for fragment

| Item | Value |
| --- | --- |
| **`FragECP`** | — |

      - `<FragID> "<ECPName>"`
      - Define `ECP` for fragment

| Item | Value |
| --- | --- |
| **`ReadFragBasis`** | — |

      - `<FragID> "<filename.bas>"`
      - Read `Basis` for fragment from file

| Item | Value |
| --- | --- |
| **`ReadFragAuxJ`** | — |

      - `<FragID> "<filename.bas>"`
      - Read `AuxJ` for fragment from file

| Item | Value |
| --- | --- |
| **`ReadFragAuxJK`** | — |

      - `<FragID> "<filename.bas>"`
      - Read `AuxJK` for fragment from file

| Item | Value |
| --- | --- |
| **`ReadFragAuxC`** | — |

      - `<FragID> "<filename.bas>"`
      - Read `AuxC` for fragment from file

| Item | Value |
| --- | --- |
| **`ReadFragCABS`** | — |

      - `<FragID> "<filename.bas>"`
      - Read `CABS` for fragment from file

| Item | Value |
| --- | --- |
| **`ReadFragECP`** | — |

      - `<FragID> "<filename.bas>"`
      - Read `ECP` for fragment from file

| Item | Value |
| --- | --- |
| **{cspan}`2` Reading basis sets from a file (see [sec:essentialelements.basisset.file](#sec:essentialelements.basisset.file))** | — |
| **`GTOName`** | — |

      - `<filename.bas>`
      - Read orbital basis from file

| Item | Value |
| --- | --- |
| **`GTOAuxJName`** | — |

      - `<filename.bas>`
      - Read `AuxJ` from file

| Item | Value |
| --- | --- |
| **`GTOAuxName`** | — |

      - `<filename.bas>`
      - Equivalent to `GTOAuxJName`

| Item | Value |
| --- | --- |
| **`GTOAuxJKName`** | — |

      - `<filename.bas>`
      - Read `AuxJK` from file

| Item | Value |
| --- | --- |
| **`GTOAuxCName`** | — |

      - `<filename.bas>`
      - Read `AuxC` from file

| Item | Value |
| --- | --- |
| **`GTOCABSName`** | — |

      - `<filename.bas>`
      - Read `CABS` from file

| Item | Value |
| --- | --- |
| **{cspan}`2` Removal of linear dependence (see [sec:essentialelements.basisset.lindep-pcd](#sec:essentialelements.basisset.lindep-pcd))** | — |
| **`PCDTrimBas`** | — |

      - `Overlap`
      - Trim the orbital basis in the overlap metric

| Item | Value |
| --- | --- |
| **`PCDTrimAuxJ`** | — |

      - `Coulomb`
      - Trim the AuxJ basis in the Coulomb metric

| Item | Value |
| --- | --- |
| **`PCDTrimAuxJK`** | — |

      - `Coulomb`
      - Trim the AuxJK basis in the Coulomb metric

| Item | Value |
| --- | --- |
| **`PCDTrimAuxC`** | — |

      - `Coulomb`
      - Trim the AuxC basis in the Coulomb metric

| Item | Value |
| --- | --- |
| **`PCDThresh`** | — |

      - `-1`
      - Threshold for the PCD (1e-16 to 1e-10 makes sense): chosen automatically if `<0`

| Item | Value |
| --- | --- |
| **{cspan}`2` AutoAux-related keywords (see [sec:essentialelements.basisset.aux.autoaux](#sec:essentialelements.basisset.aux.autoaux))** | — |
| **{rspan}`3` `AutoAuxSize`** | — |

      - 0 
      - Use minimal effective rather than minimal primitive exponent (suitable for ANO basis sets)

| Item | Value |
| --- | --- |
| **1** | — |

      - (default) Increases the maximal exponent for the shells with low angular momenta. 

| Item | Value |
| --- | --- |
| **2** | — |

      - Increases the maximal exponent for all shells

| Item | Value |
| --- | --- |
| **3** | — |

      - Directly uses the primitives and produces the largest fitting basis

| Item | Value |
| --- | --- |
| **`AutoAuxLmax`** | — |

      - `false` 
      - If `true`, increase the maximal angular momentum of the fitting basis set 
        to the highest value permitted by ORCA and by the orbital basis set.

| Item | Value |
| --- | --- |
| **`AutoAuxLLimit`** | — |

      - -1
      - If >0, do not exceed the given angular momentum.

| Item | Value |
| --- | --- |
| **`AutoAuxF[0]`** | — |

      - 20.0
      - The factor to increase the maximal s-exponent

| Item | Value |
| --- | --- |
| **`AutoAuxF[1]`** | — |

      -  7.0
      - Same for the p-shell

| Item | Value |
| --- | --- |
| **`AutoAuxF[2]`** | — |

      -  4.0
      - Same for the d-shell

| Item | Value |
| --- | --- |
| **`AutoAuxF[3]`** | — |

      -  4.0
      - Same for the f-shell

| Item | Value |
| --- | --- |
| **`AutoAuxF[4]`** | — |

      -  3.5
      - Same for the g-shell

| Item | Value |
| --- | --- |
| **`AutoAuxF[5]`** | — |

      -  2.5
      - Same for the h-shell

| Item | Value |
| --- | --- |
| **`AutoAuxF[6]`** | — |

      -  2.0
      - Same for the i-shell

| Item | Value |
| --- | --- |
| **`AutoAuxF[7]`** | — |

      -  2.0
      - Same for the j-shell

| Item | Value |
| --- | --- |
| **`AutoAuxB[0]`** | — |

      -  1.8
      - Even-tempered expansion factor for the s-shell

| Item | Value |
| --- | --- |
| **`AutoAuxB[1]`** | — |

      -  2.0
      - Same for the p-shell

| Item | Value |
| --- | --- |
| **`AutoAuxB[2]`** | — |

      -  2.2
      - Same for the d-shell

| Item | Value |
| --- | --- |
| **`AutoAuxB[3]`** | — |

      -  2.2
      - Same for the f-shell

| Item | Value |
| --- | --- |
| **`AutoAuxB[4]`** | — |

      -  2.2
      - Same for the g-shell

| Item | Value |
| --- | --- |
| **`AutoAuxB[5]`** | — |

      -  2.3
      - Same for the h-shell

| Item | Value |
| --- | --- |
| **`AutoAuxB[6]`** | — |

      -  3.0
      - Same for the i-shell

| Item | Value |
| --- | --- |
| **`AutoAuxB[7]`** | — |

      -  3.0
      - Same for the j-shell

| Item | Value |
| --- | --- |
| **`AutoAuxTightB`** | — |

      - `true`
      - Only use `AutoAuxB[l]` for shells with high `l` and `AutoAuxB[0]` for the rest

| Item | Value |
| --- | --- |
| **`OldAutoAux`** | — |

      - `false`
      - If `true`, selects the ORCA 3.1 generation procedure (deprecated)

