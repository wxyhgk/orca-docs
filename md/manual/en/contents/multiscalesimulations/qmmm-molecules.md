```{index} QMMM, QM/QM2, QM/QM2/MM, additive, subtractive
```
(sec:multiscalesimulations.molecules)=
# Multiscale Simulations of molecular systems

ORCA features three methods suitable for molecular systems such as proteins, DNA, large molecules, explicit solvation, depending on their size and depending on the availability of force field parameters.

-   [Additive QM/MM](sec:multiscalesimulations.add_qmmm) is a pure additive QMMM method.

-   [QM1/QM2](sec:multiscalesimulations.oniom2) is a subtractive (2-layered) ONIOM method.

-   [QM1/QM2/MM](sec:multiscalesimulations.oniom3) is a 3-layered method, combining a subtractive method between QM1 and QM2, and an additive QMMM method for QM2/MM.

(sec:multiscalesimulations.add_qmmm)=
## Additive QMMM

In the additive QMMM scheme force field parameters are used to describe the interactions in the MM region, as well as
bonded interactions and LJ interactions between QM and MM atoms. Thus, force field parameters are required for the MM
part of the calculation.
ORCA currently supports the popular **CHARMM**, **AMBER**, and **Open Force Field** force fields, as discussed
in {ref}`sec:modelchemistries.mm-orcaforcefield`, and provides tools
to [convert](sec:modelchemistries.mm-orcaforcefield.prms-convff) their force field parameter files into the
ORCA force field file format.

(sec:multiscalesimulations.qmmm-orcaforcefield)=
### Basic Usage

The minimum input necessary for an additive QM/MM calculation is shown in the following example.
The force field filename is provided via the keyword `ORCAFFFilename`:

```orca
!QMMM
%qmmm
 QMAtoms {0 1 2 27 28} end
 ORCAFFFilename "UBQ.ORCAFF.prms"
end
```

:::{Note}
`ORCAFF.prms` files need to be provided for QM/MM, QM/QM2/MM and
IONIC-CRYSTAL-QMMM calculations, but not for QM/QM2 and `MOL-CRYSTAL-QMMM`.
:::

(sec:oniom)=
## ONIOM Methods: General Overview

For the simulation of large systems with up to 10000 atoms, or for large
QM regions in biomolecules, ORCA provides the QM/QM2 and QM/QM2/MM
methods. The specifics of the two different methods are discussed
further below. Here we are presenting the common concepts and keywords
of both methods. For subtractive methods, we use a high level (QM) and a
low level (QM2) of accuracy for different parts of the system. The
advantages of this - in contrary to QM-MM methods - are as follows:

-   QM2 methods are polarizable, the interaction with the high level
    region is more accurate.

-   No MM parameters are needed for the atoms that are described at the
    QM2 level.

(sec:multiscalesimulations.oniom-qm2methods)=
### Available QM2 Methods

ORCA has several built in QM2 methods:

-   Semiempirical methods (`AM1`, `PM3`)

-   Tight-binding DFT (`XTB0`, `XTB1`, `XTB` (or `XTB2`))

-   Composite methods (`HF-3c`, `PBEh-3c`, `r2SCAN-3c`)

-   User-defined QM2 methods

The individual keywords for these methods are:

(tab:multiscalesimulations.oniom-qm2options)=
:::{table} Options for QM2 for QM/QM2 and QM/QM2/MM methods available via simple keywords.
:class: normalsize
| QM/QM2      | QM/QM2/MM       |
|:------------|:----------------|
| `!QM/XTB`       | `!QM/XTB/MM`       |
| `!QM/XTB1`      | `!QM/XTB1/MM`      |
| `!QM/XTB0`      | `!QM/XTB0/MM`      |
| `!QM/GFN-FF`    | `!QM/GFN-FF/MM`    |
| `!QM/HF-3C`     | `!QM/HF-3C/MM`     |
| `!QM/PBEH-3C`   | `!QM/PBEH-3C/MM`   |
| `!QM/R2SCAN-3C` | `!QM/R2SCAN-3C/MM` |
| `!QM/PM3`       | `!QM/PM3/MM`       |
| `!QM/AM1`       | `!QM/AM1/MM`       |
:::

Users can define their own low-level methods in the following way

```orca
!QM/QM2          or   !QM/QM2/MM   
%qmmm
  QM2CUSTOMMETHOD "B3LYP"
  QM2CUSTOMBASIS "def2-SVP def2/J"
end
```

Alternatively, a custom QM2 method / basis set file can be provided:

```orca
!QM/QM2  or  !QM/QM2/MM   
%qmmm
  QM2CustomFile "myQM2Method.txt" # File should be available 
                                  # in working directory
end
```

The custom QM2 method file can contain any desired input, as e.g. the
file myQM2Method.txt:

```orca
!cc-pVDZ HF TightSCF NOSOSCF KDIIS
%basis
  NewAuxJKGTO Mg "AutoAux" end
end
```

:::{Note}

Only add methods (including convergence settings) and basis sets for
the QM2Custom options. Everything else (parallelization, memory,
solvation, etc.) is taken care of by ORCA itself.
:::

### Electrostatic Interaction between high and low level

By default we are using electrostatic embedding, i.e. the high level
system sees the atomic point charges of the low level (QM2) system.
These point charges are derived from the full system low level (QM2)
calculation. The following methods for determining these charges are
available:

(tab:multiscalesimulations.oniom-qm2-chargemethod)=
:::{table} Options for determining the atomic charges of the QM2 atoms.
:class: normalsize
| Keyword         | Option       |
|:----------------|:----------------|
| `Charge_Method` | `Hirshfeld` (default) |
|                 | `MBIS`                |
|                 | `CHELPG`              |
|                 | `Mulliken`            |
|                 | `Loewdin` (default if QM2 is AM1 or PM3) |
:::

The QM2 point charges can be scaled with the following keyword.

```orca
%qmmm
  Scale_QM2Charges_MMAtom 1. # default is 1.
end
```

### Boundary Region

The boundary between high and low level part of the system can contain
covalent bonds. For the detection and realistic treatment of these
covalent bonds, a topology of the large QM2 system is generated at calculation start using
the following keyword.

(tab:multiscalesimulations.oniom-qm2-autoff)=
:::{table} Options for creating an initial topology for the full (QM/QM2) or medium (QM/QM2/MM) system.
:class: normalsize
| Keyword         | Option       |
|:----------------|:----------------|
| `AutoFF_QM2_Method` | `Simple_Eq` (default) |
|                     | `XTB`             |
|                     | `XTB1`            |
|                     | `XTB0`            |
|                     | `GFNFF`           |
|                     | `HF3C`            |
|                     | `PBEH3C`          |
|                     | `R2SCAN3C`        |
|                     | `PM3`             |
|                     | `AM1`             |
|                     | `QM2`             |
:::

:::{Note}

If you use any of the XTB methods as AutoFF_QM2_Method make sure to have
the otool_xtb binary in your ORCA PATH, see
{ref}`sec:modelchemistries.semiempirical.xtb`.
:::

(sec:multiscalesimulations.oniom2)=
## Subtractive QM/QM2 Method (ONIOM2)

The QM/QM2 method is a very convenient way of running multiscale
calculations without the need to prepare any parameters. This method is
a subtractive QM-QM method, in which we treat a part of interest on a
higher level of accuracy, and the remainder of the system on lower level
of accuracy. The implementation follows similar works as e.g. described
in reference {cite}`Mayhall2010`.

The method can be used in a similar way as a regular QM calculation. Let
us have a look at the proton transfer in propionic acid, which can be
modeled as follows:

```{literalinclude} ../../orca_working_input/C06S28_535.inp
:language: orca
```

with the product structure file (propionicAcid_prod.xyz):

```{literalinclude} ../../orca_working_input/propionicAcid_prod.xyz
:language: orca
```

As can be seen from the input, the only difference to a regular
calculation is the necessity to define the high level region via the
`QMAtoms` or `QMCoreAtoms` keyword.

### System charges and multiplicities

The two subsystems can have different (integer) charges and
multiplicities. Defining the correct charges and multiplicities is
important. The charge and multiplicity defined via the coordinate
section defines the charge and multiplicity of the high level region
(`QMAtoms`). The user still needs to define the charge and multiplicity of
the total system (corresponding to the sum of the charge of the high
level and low level parts, and corresponding to the overall
multiplicity).

```orca
%qmmm
  QMAtoms {0:3} end # high level region
  Charge_Total  0   # charge of the full system. Default 0.
  Mult_Total    1   # multiplicity of the full system. Default 1.
end
*xyz 0 1            # charge and mult. of the high level region, i.e. atoms 0 to 3
```

### Solvation

Implicit Solvation effects can be included in QM/QM2 calculations. On
the one hand, for QM/XTB calculations, one can adopt the
analytical linearized Poisson-Boltzmann (`ALPB`) solvation model, the
domain decomposition COSMO (`ddCOSMO`), or the extended conductor-like
polarizable continuum model (`CPCM-X`), and on the other hand, if no XTB
is requested, ORCA uses the C-PCM. The user just needs to add the
following tags in the ORCA input file,
XTB for the QM2 region:

```orca
!QM/XTB ALPB(Water)

or

!QM/XTB DDCOSMO(Water)

or

!QM/XTB CPCMX(Water)
```

No XTB for the QM2 region:

```orca
!QM/HF-3c CPCM(Water)
```

If the `ddCOSMO` (XTB) or the `C-PCM` (non-XTB) are requested, there are two
possible ONIOM/implicit-solvation methods {cite}`oniom_pcm`.

-   **C-PCM/B:** The effect of the solvent is, in the first place,
    included in the calculation for the large QM2 system. Once this
    calculation finishes, the solvation charges located on the surface
    of the cavity for the large system are used as point charges for the
    subsequent low-level and high-level calculations for the small
    system.

-   **C-PCM/C:** The effect of the solvent is only included in the
    calculation for the large QM2 system.

The user can choose one scheme or the other via the tag "`solv_scheme`"
in the "`qmmm`" block:

```orca
%qmmm
solv_scheme CPCM_B   # CPCM_B (default)
                     # CPCM_C
end
```

If the ALPB model or the CPCM-X are requested (within QM/XTB methods), the solvation
effect is just included in the calculation for the large QM2 system (as
one does for the C-PCM/C scheme).

(sec:multiscalesimulations.oniom3)=
## QM/QM2/MM Method (ONIOM3)

The QM/QM2/MM method uses a combination of the subtractive scheme for
the QM-QM2 part, and the additive scheme for the (QM-QM2) - (MM)
interaction. It can be used if very large QM regions are required for
biomolecules and explicitly solvated systems. The system is divided into
a high level (QM), low level (QM2), and MM region (MM).

(sec:multiscalesimulations.oniom-qm2atoms)=
### QM2 Atoms

QM2 atoms need to be defined for QM/QM2/MM calculations. They can be
defined either directly

```orca
%qmmm                        
 QMAtoms {0:4} end           # list of QM atoms (counting starts from 0) or
 QM2Atoms {5:22} end         # list of QM2 atoms
end                          # an atom should not occur in both lists
*pdbfile 0 1 ubq.pdb
```

or via the occupancy column of a pdb file (see
{ref}`sec:multiscalesimulations.qmmm-regions`).

:::{Note}
QM2 atoms can be defined via 2 in the occupancy
column. In this case `Use_QM2_InfoFromPDB` must be set to true.
:::

### System charges and multiplicities

The high and low level subsystems can have different (integer) charges
and multiplicities. Defining the correct charges and multiplicities is
important. The charge and multiplicity defined via the coordinate
section defines the charge and multiplicity of the high level region
(`QMAtoms`). The user still needs to define the charge and multiplicity of
the medium system (corresponding to the sum of the charge of the high
level and low level regions, and corresponding to the overall
multiplicity of the combined high and low level region). The charge of
the MM region is determined based on the MM parameters provided by the
force field.

```orca
%qmmm
  QMAtoms {0:3} end # high level region
  Charge_Medium 0   # charge of the medium system. Default 0.
  Mult_Medium   1   # multiplicity of the medium system.  Default 0.
end
*xyz 0 1            # charge and mult. of the high level region, i.e. atoms 0 to 3
```

### Basic Usage

An example for a QM/QM2/MM calculation looks as follows:

```orca
!QM/HF-3c/MM Opt B3LYP def2-TZVP def2/J NumFreq
%qmmm
 ORCAFFFilename "peptideChain.ORCAFF.prms"
 QMAtoms {16:33 68:82} end
 QM2Atoms {0:12 83:104} end
 ActiveAtoms { 0:38 65:120} end
 Charge_Medium 0
end
*pdbfile -1 1 peptideChain.pdb
```