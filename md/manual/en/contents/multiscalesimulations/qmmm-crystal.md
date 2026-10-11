```{index} Crystal-QMMM
```
(sec:multiscalesimulations.cryst-qmmm)=
# CRYSTAL-QMMM

For the simulation of extended systems ORCA provides the CRYSTAL-QMMM
features:

-   [MOL-CRYSTAL-QMMM](sec:multiscalesimulations.mol-cryst-qmmm) for molecular crystals.

-   [IONIC-CRYSTAL-QMMM](sec:multiscalesimulations.ionic-cryst-qmmm) for semiconductors and insulators.

In this section we present the concepts and keywords that are common to
both methods. ORCA is a molecular code and cannot carry out periodic
calculations, but ORCA has been used for modeling selected properties
for ionic solids using embedded cluster models already in the past (see
e.g reference {cite}`Dittmer2019`). With ORCA 5 we provide the CRYSTAL-QMMM
method, which simplifies setting up and running these types of embedded
cluster calculations. The user needs to provide the structure with a
(large enough) supercell representative for the crystal, and provide a
list of QM atoms. The QM region should be located in the central part of
the supercell. The QM atoms are embedded in the remainder of the
supercell, the surrounding MM atoms, which are represented by
atom-centered point charges and influence the QM calculations. How these
charges are obtained, is outlined in the next paragraph.

(sec:multiscalesimulations.cryst-qmmm-charge-conv)=
## Charge Convergence between QM and MM region

The core idea of the CRYSTAL-QMMM method is to reach charge convergence
between the QM and the MM atoms. For this purpose, the MM charges are
updated self-consistently with the atomic (CHELPG) charges of the QM
atoms. This idea follows the work of reference {cite}`Dittmer2019` for the
`IONIC-CRYSTAL-QMMM` and of reference {cite}`Bjornsson2012` for the
`MOL-CRYSTAL-QMMM`.

:::{raw} latex
\begingroup
\footnotesize
:::

:::{tabularcolumns} \Y{0.3}\Y{0.2}\Y{0.4}
:::

(tab:multiscalesimulations.cryst-qmmm-charge-conv)=
:::{flat-table} Keywords for charge convergence settings for `!IONIC-CRYSTAL-QMMM` or `MOL-CRYSTAL-QMMM`
:class: footnotesize
:header-rows: 1
* - Keyword
  - Options
  - Description
* - `Conv_Charges`
  - `true`/`false`
  - Use charge convergence scheme. Default `true`.
* - `Conv_Charges_MaxNCycles`
  - `<int>`
  - Maximum number of cycles for charge convergence scheme. Default `30` for MOL-CRYSTAL-QMMM. Default `50` for IONIC-CRYSTAL-QMMM.
* - `Conv_Charges_ConvThresh`
  - `<real>`
  - Convergence threshold for maximum charge change (default `0.01`) for atom type between two subsequent charge convergence cycles.
* - `Scale_FormalCharge_MMAtom`
  - `<real>`
  - MM atomic charges used in QM part of the CRYSTAL-QMMM calculation are scaled by this factor. Default `1.`.
:::
:::{raw} latex
\endgroup
:::




During optimizations, the charge convergence scheme can be used (i) only
at the very beginning, (ii) every N geometry steps, or (iii) for each
geometry step, using the following keyword:

```orca
%geom
  ReConvCharge 1 # default is 1. Redo charge convergence scheme every N steps.
end
```

After charge convergence, the converged charges are stored in the file
`basename.convCharges.ORCAFF.prms`. It can be used for a later calculation
(with the same or different electronic structure settings) with the
following keyword combination:

```orca
!IONIC-CRYSTAL-QMMM    or    !MOL-CRYSTAL-QMMM
%qmmm
  Conv_Charges false
  ORCAFFFilename "firstjob.convCharges.ORCAFF.prms"
end
```

## MM-MM Interaction

Unlike with the other multiscale methods (QMMM, QM/QM2, QM/QM2/MM) the
MM region is only treated as a perturbation to the QM region. The
(bonded and nonbonded) MM-MM interaction is not computed - since it
would not affect the QM-MM interaction - and thus the active region
(optimizations, frequencies, \...) in CRYSTAL-QMMM calculations should
be restricted to atoms of the QM region.

## Preparing CRYSTAL-QMMM Calculations

The input structures and input files for the CRYSTAL-QMMM calculations
can be prepared with the {ref}`sec:utilities.crystalprep` module.

(sec:multiscalesimulations.mol-cryst-qmmm)=
## MOL-CRYSTAL-QMMM

Conceptually we use an additive QM/MM calculation, in which the QM
region interacts with the MM region only via nonbonded interactions.
Lennard-Jones interaction between QM and MM region is computed using van
der Waals parameters from the UFF force field. The charge convergence
treatment between QM and MM region starts with zero charges on the MM
atoms, and is iterated until convergence of the QM atomic (CHELPG) and
MM point charges is achieved.

The `MOL-CRYSTAL-QMMM` method expects as structural input a supercell that
consists of repeating, identical molecular subunits, i.e. the atom
ordering of the molecules should always be the same, and one molecular
subunit should follow the next one. The minimum input necessary for a
`MOL-CRYSTAL-QMMM` run looks as follows.

```orca
%qmmm
  NUnitCellAtoms 16      # provide the number of atoms per molecular subunit
  QMAtoms {160:175} end  # QM atoms, should be in central part of the supercell. 
                         # Must be at least one complete molecular subunit.
end
```

:::{Note}
For molecular crystals it is assumed that the entire supercell
consists of repeating units which each have zero charge. QM regions
should consist of one or multiple of such charge-neutral units.
:::

### Extending the QM Region

ORCA can extend the QM region (which we call QM core region, defined by
the original `QMAtoms` input) by one or multiple layers of molecular
subunits using the `HFLayers` keyword. If the `HFLayers` keyword is
used, the molecular subunits of the defined number of layers around the
QM core region is added to the QM region. The layers of molecular
subunits around the QM core region are detected via distance criteria.

```orca
%qmmm
  HFLayers 0                       # default 0
  HFLayerGTO "LANL2DZ"             # default. Use this basis set for the 
                                   # HFLayer atoms
  HFLayerECP "HayWadt"             # default. Use these ECPs for the HFLayer atoms
  Conv_Charge_UseQMCoreOnly true   # only use the QM core region for the charge 
                                   # convergence scheme
end
```

The HFLayer can be seen as a buffer region between the molecular subunit
of interest (original QM atoms) and the surrounding subunits. The
different possible reasons for `HFLayers` are as follows:

-   For DLPNO calculations with `HFLayers`, the DLPNO multilevel feature
    is automatically switched on. The molecules of the `HFlayer` form an
    own fragment which is treated on HF level only, i.e. these molecules
    are not included in the Post-HF treatment.

-   The `HFLayers` can also be used for non-DLPNO calculations. In such
    cases, the HFLayer molecules are in the same way included in the QM
    calculation as the other QM molecules. But their definition is a
    convenient way to choose a different basis set (and ECPs) for those
    molecules.

-   It can be assumed that the QM charges computed for the QM core
    region are more realistic than the charges of the HFLayer atoms near
    the MM atomic charges. Thus, using only the QM atomic charges of the
    QM core region represent more realistic charges for the charge
    convergence scheme.

-   If necessary, the atoms of the HFLayer can be defined by the user.
    Make sure that complete molecular subunits are used here.

```orca
%qmmm
  HFLayerAtoms {0:15} end
end
```

:::{Note}

The term `HFLayers` might be misleading. Strictly speaking, only for
`MOL-CRYSTAL-QMMM` calculations with `DLPNO` methods (e.g.
`DLPNO-CCSD(T)`, `DLPNO-MP2`, `DLPNO-B2PLYP`) the HF layer atoms are
treated on HF level. For other methods (e.g. DFT) the HF layer atoms
are treated with the same electronic structure method as the QM core
region atoms.
:::

### Basic Usage

An example for a `MOL-CRYSTAL-QMMM` calculation looks as follows:

```orcainput
! MOL-CRYSTAL-QMMM
! PBE def2-SVP Opt NumFreq
%qmmm
 NUnitCellAtoms 13
 QMAtoms {221:233} end                   
 ActiveAtoms {221:233} end  
end
*xyzfile 0 1 Ala_SC.xyz
```

(sec:multiscalesimulations.ionic-cryst-qmmm)=
## IONIC-CRYSTAL-QMMM

Conceptually we use an embedded cluster calculation, in which the QM
region interacts only with the MM atomic point charges of the
surrounding. Unlike with `MOL-CRYSTAL-QMMM`, the Lennard-Jones interaction
between QM and MM region is not computed. The charge convergence
treatment between QM and MM region starts with the initial MM charges
(the charges initially read from the ORCAFF.prms file) and is iterated
until convergence of the QM atomic (CHELPG) and MM point charges is
achieved.

### Boundary Region

For ionic crystals a boundary region needs to be introduced between the
QM region and the atomic point charges of the MM atoms in order to avoid
spurious electron leakage from the clusters and to treat dangling bonds
on the surface of the QM region. This boundary region consists of capped
effective core potentials (cECPs). These cECPs are placed on the
position of the MM atoms that are directly adjacent to the QM region.
ORCA analyzes the connectivity of the atoms of the supercell and can
thus detect the layers of atoms around the QM region, where the first
layer consists of the atoms directly bonded to the QM atoms, the second
layer consists of the atoms directly bonded to the atoms of the first
layer and so on. The charges of these cECPs are determined in the same
way as the MM atomic charges during the charge convergence scheme.

```orca
%qmmm
  ECPLayerECP "SDD"              # cECPs used for the boundary region
  ECPLayers 3                    # Number of cECP layers around the QM region. 
                                 # Default is 3.
  Scale_FormalCharge_ECPAtom 1.  # default is 1. Charges on cECPs are scaled by 
                                 # this factor
end
```

### Extending the QM Region

ORCA can extend the QM region (which we call QM core region, defined by
the original QMAtoms input) by one or multiple layers of atoms using the
`HFLayers` keyword. If the `HFLayers` keyword is used, the atoms of the
defined number of layers around the QM core region is added to the QM
region. The layers of atoms around the QM core region are detected in
the same way as defined above for the ECPLayers.

```orca
%qmmm
  HFLayers 0                       # default 0
  HFLayerGTO "LANL2DZ"             # default. Use this basis set for the
                                   # HFLayer atoms
  HFLayerECP "HayWadt"             # default. Use these ECPs for the HFLayer atoms
  Conv_Charge_UseQMCoreOnly true   # only use the QM core region for the charge 
                                   # convergence scheme
end
```

The HFLayer can be seen as a buffer region between the actual atoms of
interest (original QM atoms) and the surrounding cECP and MM point
charge environment.The different possible reasons for `HFLayers` are as
follows:

-   For DLPNO calculations with `HFLayers`, the DLPNO multilevel feature
    is automatically switched on. The atoms of the HFLayer form an own
    fragment which is treated at HF level only, i.e. these atoms are not
    included in the Post-HF treatment.

-   It can be assumed that the QM charges computed for the QM core
    region are more realistic than the charges of the HFLayer atoms near
    the cECPs and MM atomic charges, in particular for highly charged
    systems. Thus, using only the QM atomic charges of the QM core
    region represent more realistic charges for the charge convergence
    scheme.

-   If necessary, the atoms of the HFLayer can be defined by the user:

```orca
%qmmm
  HFLayerAtoms {29:35} end
end
```

-   The charge of the HFLayer is automatically computed based on the
    formal charges of its atoms. If necessary, the HFLayer charge can be
    provided by the user.

```orca
%qmmm
  Charge_HFLayer 10 # by default it is computed automatically based on the 
                    # formal charges from the ORCAFF.prms file
end
```

:::{Note}

The term `HFLayers` might be misleading. Strictly speaking, only for
`IONIC-CRYSTAL-QMMM` calculations with DLPNO methods (e.g.
`DLPNO-CCSD(T)`, `DLPNO-MP2`, `DLPNO-B2PLYP`) the HF layer atoms are
treated on HF level. For other methods (e.g. DFT) the HF layer atoms
are treated with the same electronic structure method as the QM core
region atoms.
:::

### Net Charge of the Entire Supercell

For ionic crystals, the QM region (as well as the entire supercell) can
consist of an unequal number of atoms of each atom type. As a result of
that, the QM region may have non-zero net charge. Consequently, when
assigning the atomic point charges to the MM atoms during the charge
convergence scheme, the sum of the charge of the QM region, of the ECP
layer, and of the atomic charges of the MM atoms, can deviate from the
ideal charge of the supercell. In order to enforce the ideal charge of
the supercell, the total charge of the entire system is enforced by
equally shifting the charges of all MM (including boundary) atoms.

```orca
%qmmm
  Charge_Total  0         # default 0. Total charge of the supercell
  EnforceTotalCharge true # enforce the total charge by shifting MM charges
end
```

The charge shifting procedure can be restricted to the MM atoms on the
outer parts of the supercell by defining the number of `OuterPCLayers`. If
`OuterPCLayers` is set to 1, only the atoms of the most outer layer of
the supercell (recognized based on the connectivity of the atoms) are
included in the charge shifting procedure. If `OuterPCLayers` is larger
than 2, the atoms connected to the most outer layer are additionally
included in the charge shifting procedure, etc.

```orca
%qmmm
  OuterPCLayers 0         # default 0, i.e. charge shifting for all MM atoms
end
```

:::{Note}

The charge of the QM core region can be chosen to be assigned
automatically. This overwrites the charge provided in the xyz or pdb
section.

```orca
%qmmm
  AutoDetectQCCharge false # default is false
end
```
:::

### Example Input

A minimal example for an `IONIC-CRYSTAL-QMMM` calculation looks as
follows:

```orcainput
! IONIC-CRYSTAL-QMMM 
! NMR
! PBE pcSseg-2 def2/JK def2-svp/C
%qmmm
  QMAtoms {0:6} end
  ORCAFFFilename "nacl6.ORCAFF.prms"
  CHARGE_TOTAL    0
end
*xyzfile -5 1 nacl6.xyz
```

(sec:multiscalesimulations.ionic-cryst-pdb)=
### Different QM and MM regions Stored in the PDB file

The stored PDB file contains the following entries in its occupancy
column.

(tab:multiscalesimulations.ionic-cryst-pdb-occ)=
:::{table} Definition of entries stored in the pdb file for Ionic-Crystal-QMMM calculations.
:class: normalsize
| Value         | Description       |
|:----------------|:----------------|
| `0` | MM atoms mimicked by surrounding point charges |
| `1` | QM core region atoms |
| `2` | HFLayer atoms |
| `3` | cECPs           |
| `4` | OuterPCLayer atoms (subset of MM atoms) if defined, are the only atoms that are used in the charge shift procedure for enforcing the total charge |
:::