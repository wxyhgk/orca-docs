

<a id="sec:modelchemistries.mm.orca"></a>
# Molecular Mechanics

Since version 4.2 ORCA features its own independent Molecular Mechanics (MM) implementation.

The minimum input necessary for an MM treatment looks as follows.

```orca
!MM
%mm
 ORCAFFFilename "UBQ.ORCAFF.prms"
end
```

In this section we discuss usage of MM as well as basic keywords and options, i.e.

-   with which other features MM calculations can be combined

-   the basic structure of the ORCA Force Field File,

-   which force fields are supported,

-   how to generate the ORCA Force Field File,

-   how to manipulate the ORCA Force Field File,

-   how to speed up MM calculations,

-   further MM options and keywords.

Further options important for QM/MM calculations will be discussed in
section [qmmm.orca](../multiscalesimulations/qmmm-general.md#sec:multiscalesimulations.qmmm.orca).

## Combining the MM module with other ORCA Features

Molecular mechanics was introduced as a prerequisite for multiscale simulations within ORCA. But MM calculations 
can also be used as a standalone, e.g. for cheap preoptomizations.

Possible ORCA features are:

-   **Single Point Calculations**: Simple MM calculations as well as [QM/MM calculations](../multiscalesimulations/qmmm-general.md#sec:multiscalesimulations.qmmm.orca)

-   **Optimization**: Use all kinds of [geometry optimizations](../structurereactivity/optimizations.md#sec:structurereactivity.optimization)
    with all kinds of
    constraints, TS optimization, relaxed surface scans, and the ScanTS
    feature. Use the L-Opt and L-OptH features including the combination
    of all kinds of fragment optimizations (fix fragments, relax
    fragments, relax only specific elements in fragments, treat a
    fragment as a rigid body).

-   **Transition States and Minimum Energy Paths**: Bond breaking and bond forming are not possible using MM methods, 
    but conformational changes or dispersion driven reactions can be studied on MM-level only. 
    For such tasks ORCA [Nudged-Elastic Band method](../structurereactivity/neb.md#sec:structurereactivity.optimization.neb) can be used.

-   **Conformational Searches**: Conformational Searches can be run with ORCA's [GOAT](../structurereactivity/goat.md#sec:structurereactivity.GOAT) module.

-   **Frequency Calculations**: Use regular [frequency calculations](../structurereactivity/frequencies.md#sec:structurereactivity.frequencies). If required, ORCA automatically
    switches on the [geomopt.partialhess](../structurereactivity/optimizations_TS.md#sec:structurereactivity.geomopt.partialhess)
    (PHVA) [li2002theor](../../bibliography.md) calculation. (not tested for `IONIC-CRYSTAL-QMMM`)

-   **Molecular Dynamics**: Use the [Molecular Dynamics](../moleculardynamics/moldyn.md#sec:moldyn) (MD) module for Born-Oppenheimer MD
    (BOMD) with MM.

!!! note

    [Active regions](../multiscalesimulations/qmmm-general.md#sec:multiscalesimulations.qmmm-active) can also be defined for MM calculations. They have to be [defined](../multiscalesimulations/qmmm-general.md#sec:multiscalesimulations.qmmm-regions) via the `%qmmm` block.

<a id="sec:modelchemistries.mm-orcaforcefield"></a>
## Molecular Mechanics Force Field in ORCA

For the MM part of the QM/MM calculation force-field parameters are
necessary. ORCA has its own parameter file format (ORCA force field
file - ORCAFF.prms), which includes the atom specific parameters for
nonbonded interactions:

-   partial charge

-   LJ coefficients

and parameters for bonded interactions:

-   bonds

-   angles

-   Urey-Bradley terms

-   dihedrals

-   impropers

-   CMAP terms (cross-terms for backbone, currently not used)

Individual parameters, like e.g. atomic charge, equilibrium bond length
and force constant, \..., can be conveniently modified directly within
the ORCA Force Field File.

### Supported Force Field Types

For the MM part of the QM/MM calculation force field parameters are
necessary. ORCA has its own force field file format (stored in files called
`basename.ORCAFF.prms`), which is used internally. 
ORCA provides tools to convert other popular force fields into the ORCA force field file format.
Currently, the following formats are supported to be converted to the ORCA
force field file format:

-   **CHARMM psf files**:   protein structure file from the CHARMM force field. The psf files
    can be easily prepared with the popular molecular visualizer
    [VMD](https://www.ks.uiuc.edu/Research/vmd/), together with its
    extensions
    ([psfgen](https://www.ks.uiuc.edu/Research/vmd/plugins/psfgen/),
    [QwikMD](http://www.ks.uiuc.edu/Research/qwikmd/),
    [fftk](http://www.ks.uiuc.edu/Research/vmd/plugins/fftk/), which
    works together with ORCA ). The psf file
    contains information on the atom types and on the bonded interactions of
    all atoms. It does, however, not contain the parameters that belong to
    these interactions. These parameteres are stored in specific files,
    often ending with prm, but also par or str. The CHARMM parameter files
    come with VMD installation, can be directly
    [downloaded](http://mackerell.umaryland.edu/charmm_ff.shtml).

-   **AMBER prmtop files**:   topology files from the AMBER force field. Tutorials on how to
    generate AMBER prmtop files (for standard and non-standard
    molecules) can be found [here](https://ambermd.org/tutorials/).

-   **Open Force Field**:   xml files from the [openforcefield
    initiative](http://openforcefield.org/). With the openff-toolkit
    xml topology files (compatible with the AMBER force field) can
    be easily generated for small and medium-sized non-standard
    molecules. For a tutorial see
    [here](https://github.com/openforcefield/openff-toolkit/blob/master/examples/using_smirnoff_with_amber_protein_forcefield/BRD4_inhibitor_benchmark.ipynb).

-   **Simple force field** for small to medium-sized molecules:   Alternatively, the orca_mm module can generate a simple
    approximate ORCAFF.prms file. For more options,
    see [modelchemistries.mm-orcaforcefield-makeff](#sec:modelchemistries.mm-orcaforcefield-makeff).

This concept has the following advantages:

-   Modification of force field parameters:   Atom and bond specific parameters can be easily modified within
    the ORCA force field file, allowing the user maximum flexibility
    in modifying the force field, which might be particularly useful
    for chemical systems like transition metal complexes.

-   Standard and Non-Standard Ligands:   Ligands can be easily and flexibly exchanged or added to the
    system, see [mm-orcaforcefield.prms](#sec:modelchemistries.mm-orcaforcefield.prms).

<a id="sec:modelchemistries.mm-orcaforcefield.prms"></a>
### How to generate and manipulate the ORCA Force Field File

Once a ORCAFF.prms file is available, it can be manipulated, i.e. split
up into several parts for individual molecules, new ORCAFF.prms files
can be generated for non-standard molecules, and individual ORCAFF.prms
files can be merged, as described in the following:

<a id="sec:modelchemistries.mm-orcaforcefield.prms-convff"></a>
#### Conversion from other formats to ORCAFF.prms: convff

The orca_mm module can convert psf and prm files (CHARMM), prmtop files
(AMBER) or xml files (open force field from the openff toolkit,
compatible to AMBER) to the ORCAFF file with the -convff flag. Input
options are:

```orca
orca_mm -convff <optional:-verbose> <FFInput> <PSFFILE> <PRMFILE(S)>

Keywords:
          <FFInput> = -CHARMM
          <FFInput> = -AMBER
          <FFInput> = -OPENMM
```

For CHARMM topologies, when a psf file is available for a system with
standard residues, prepared by e.g. QwikMD, psfgen or other vmd tools,
the conversion needs the psf plus the prm files as input:

```orca
CHARMM example:
orca_mm -convff -CHARMM 1C1E.psf par_all36_prot.prm toppar_water_ions_namd.str
```

ORCA can also convert Amber topologies to the ORCAFF file. Here, only
the prmtop file is required:

```orca
AMBER example:
orca_mm -convff -AMBER complex.prmtop
```

ORCA can also convert xml files from the openff toolkit (AMBER
compatible) to the ORCAFF file. Here, only the xml file is required:

```orca
OPENFF example:
orca_mm -convff -OPENMM complex.xml
```

#### Divide a force field file: splitff

If a ORCAFF.prms file should be subdivided into several files, e.g. if
the psf file stems from QWikMD with non-standard molecules included,
e.g. a ligand. In that case first the parameters of the ligand are split
from the remaining system, next the ligand needs to be protonated, then
a simple ORCAFF.prms file is generated via orca_mm's makeff option, and
finally the ligand's new ORCAFF.prms file is added to the main systems
file via the above described mergeff option. Note that the file can only
be split into files for nonbonded fragments.

Input options:

```orca
orca_mm -splitff <optional:-verbose> <ORCAFFFILE> <A1> <optional:A2> ... 

Keywords:

          <ORCAFFFILE>  = ORCA forcefield file.
          <A1>          = Atom number of first atom of fragment that should belong 
                           to a new ORCA forcefield file
          <A2>          = Atom number of first atom of fragment that should belong 
                           to a new ORCA forcefield file
          ...           = More split atoms possible
          Note that atoms start counting at 1.
          
Example:
orca_mm -splitff 1C1E_substrate_noH.ORCAFF.prms 7208
```

#### Merge force field files: mergeff

If several ORCAFF.prms files are available and should be merged for an
ORCA calculation, e.g. for a standard plus a non-standard molecule.

Input options:

```orca
orca_mm -mergeff <optional:-verbose> <ORCAFFFILE1> <ORCAFFFILE2> ... 

Keywords:

          <ORCAFFFILE1>   = First ORCA forcefield file
          <ORCAFFFILE2>   = Second ORCA forcefield file
          ...             = More ORCA forcefield files possible
          
Example:
orca_mm -mergeff 1C1E.ORCAFF.prms substrate_withH.ORCAFF.prms
```

#### Repeat force field files: repeatff

In case the same ORCAFF.prms file needs to be repeated multiple times,
the repeatff functionality is available.

Input options:

```orca
orca_mm -repeatff <optional:-verbose> <ORCAFFFILE> <A>
          <ORCAFFFILE>      = ORCA forcefield file.
          <A>               = Factor (integer) defining how often this forcefield file should be repeated.
          
Example:
orca_mm -mergeff methanol.ORCAFF.prms 580
```

This feature can be useful e.g. in the case of solvating a molecule,
i.e. adding multiple copies of a solvent to a solute. First the solvent
can be repeated N times, and subsequently the solute's prms file can be
merged together with the solvent prms file.

#### Divide a PDB file: splitpdb

When splitting a ORCAFF.prms file, also splitting of the pdb file is
required. The file can be split into an arbitrary number of individual
files.

This can be useful together with the splitff command.

Input options:

```orca
orca_mm -splitpdb <optional:-verbose> <PDBFILE> <A1> <optional:A2> ... 

Keywords:

          <PDBFILE> = PDB file.
          <A1>      = Atom number of first atom of fragment that should belong 
                       to a new ORCA forcefield file
          <A2>      = Atom number of first atom of fragment that should belong 
                       to a new ORCA forcefield file
          ...       = More split atoms possible
          Note that atoms start counting at 1.
          
Example:
orca_mm -splitpdb 1C1E_substrate_noH.pdb 7208
```

#### Merge PDB files: mergepdb

If several PDB files are available and need to be merged for an ORCA
calculation, e.g. a protein and a ligand or multiple ligands, or a
ligand that was first removed from a complex, then modified, and finally
should get back into the complex PDB file.

This can be useful together with the mergeff command.

Input options:

```orca
orca_mm -mergepdb <optional:-verbose> <1PDBFILE> <2PDBFILE> ... 

Keywords:

          <1PDBFILE>   = First PDB file
          <2PDBFILE>   = Second PDB file
          ...          = More PDB files possible
          
Example:
orca_mm -mergepdb 1C1E.pdb substrate_withH.pdb
```

<a id="sec:modelchemistries.mm-orcaforcefield-makeff"></a>
#### Create simple force field: makeff

The orca_mm tool can generate an approximate force field for a molecule,
storing it in ORCAFF.prms format. Here, the LJ coefficients are based on
UFF parameters and the partial charges are based on a simple PBE or XTB
calculation. The resulting topology is certainly not as accurate as an
original CHARMM topology, but can still be used for an approximate
handling of the molecule. Herewith, the molecule can be part of the QM
region (having at least the necessary LJ coefficients), or part of the
MM region as a non-active spectator - being not too close to the region
of interest. In the latter case it is important that the molecule is not
active, since bonded parameters are not available. However, it can still
be optimized as a rigid body, see
sections [optimization.lbfgs](../structurereactivity/optimizations.md#sec:structurereactivity.optimization.lbfgs) and the usage in
QM/MM calculations in
section [multiscalesimulations.qmmm-lopt](../multiscalesimulations/qmmm-general.md#sec:multiscalesimulations.qmmm-lopt), on MM level, optimizing its position and
orientation with respect to the specific environment.

Input options:

```orca
orca_mm -makeff <optional:-verbose> <XYZ/PDBFILE> <optional:-C CHARGE> 
                <optional:-M MULT> <optional:-nproc N> <optional:-CHARGE_OPTIONS>

Keywords:

          <CHARGE>              = charge of system
          <MULT>                = multiplicity of system
          <-nproc N>            = number of processors (Default 1) 
          <-CHARGE_OPTIONS>     =   Structure            Charge calculation
               <-PBE>                input                     PBE
               <-PBEOpt>             PBE opt.                  PBE
               <-PBEOptH>            PBE H-opt.                PBE
               <-XTB>                input                     XTB
               <-XTBOpt>             XTB opt.                  XTB
               <-XTBOptH>            XTB H-opt.                XTB
               <-XTBOptPBE>          XTB opt.                  PBE
               <-noChargeCalc>       distribute net charge evenly

               PBE Opt and SP level: RI-PBE/def2-SVP CPCM(Water), CHELPG charges
               XTB Opt and SP level: GFN2-XTB GBSA(Water), Mulliken partial charges
          
Example:
orca_mm -makeff substrate_withH.xyz -M 2 -XTBOptPBE
```

Note that ORCA generates bonds based on simple distance rules, which
enables ORCA to detect where to add link atoms between QM and MM atoms,
see also section [multiscalesimulations.qmmm-boundary](../multiscalesimulations/qmmm-general.md#sec:multiscalesimulations.qmmm-boundary). But the user is advised to treat a
molecule, for which the ORCAFF.prms file was generated with the makeff
option, either fully in the QM, or fully in the MM region, unless the
charge distribution has been properly taken care of (due to the need of
integer charges in QM and MM system).

<a id="sec:modelchemistries.mm-orcaforcefield-getHDist"></a>
#### Get standard hydrogen bond lengths: getHDist

For the definition of the link atoms standard bond lengths between C, N
and O and hydrogen are directly set by ORCA  but can be modified by the
user, see section [multiscalesimulations.qmmm-boundary](../multiscalesimulations/qmmm-general.md#sec:multiscalesimulations.qmmm-boundary). If other atom types are on the QM side
of the QM-MM boundary, their distance to the link atom has to be
defined. In this case a file can be provided to ORCA  which defines the
standard bond length to hydrogen for all possible atoms. Such a file can
be generated via the following command:

Input options:

```orca
orca_mm -getHDist <optional:-verbose> <XYZ/PDBFILE>
          
Example:
orca_mm -getHDist 1C1E.xyz
```

This file can then be modified, the required values can be added, and
the resulting file can be defined as input for the QMMM calculation.

<a id="sec:modelchemistries.mm-orcaforcefield-ioniccrystal"></a>
#### Create ORCAFF.prms file for IONIC-CRYSTAL-QMMM

For IONIC-CRYSTAL-QMMM calculations,
section [multiscalesimulations.ionic-cryst-qmmm](../multiscalesimulations/qmmm-crystal.md#sec:multiscalesimulations.ionic-cryst-qmmm), an ORCAFF.prms file with initial
charges and connectivities is required. If you are not using the
`orca_crystalprep` tool for setting up such calculations, see section
[utilities.crystalprep](../utilitiesvisualization/utilities.md#sec:utilities.crystalprep), you can directly
prepare the ORCAFF.prms file with the command:

```orca
orca_mm -makeff <XYZ/PDBFILE> -CEL <ELEMENT1> <OXIDATION_STATE1> 
                              -CEL <ELEMENT2> <OXIDATION_STATE2>

Keywords:

          <ELEMENT1>             = element name
          <OXIDATION_STATE1>     = formal oxidation state of element 1
          ...                    = More elements possible
          
Example:
orca_mm -makeff na4cl4.xyz -CEL Na 1.0 -CEL Cl -1.0
```

Here, na4cl4.xyz is the supercell structure file (it can contain tens of
thousands of atoms).

!!! note

    For supercells with more complex oxidation states', e.g.
    Co$_3$O$_4$, the ORCAFF.prms file can be generated conveniently via
    the [utilities.crystalprep](../utilitiesvisualization/utilities.md#sec:utilities.crystalprep) tool.

## Speeding Up Nonbonded Interaction Calculation

For MM calculations of very large systems with hundreds of thousands of
atoms, and for QMMM calculations with fast QM methods (e.g. XTB, AM1)
and / or very small QM systems, the computation of the nonbonded
interactions can become a bottleneck. Different schemes for speeding up
the calculation of nonbonded interactions are available within the ORCA
MM implementation. Two schemes truncate long-range interaction, another
scheme can be used for calculations with active regions, i.e.
calculations where only a part of the system is active or optimized. For
more information on active regions see
section [multiscalesimulations.qmmm-active](../multiscalesimulations/qmmm-general.md#sec:multiscalesimulations.qmmm-active).

### Force Switching for LJ Interaction

With force switching for the LJ interaction (described in
reference [steinbach1996](../../bibliography.md)) a smooth switching function is used to
truncate the LJ potential energy smoothly at the outer cutoff distance
`LJCutOffOuter`. If switching is set to false, the LJ interaction is not
truncated at `LJCutOffOuter`. The parameter `LJCutOffInner` specifies the
distance at which the switching function starts taking an effect to
bring the van der Waals potential to 0 smoothly at the `LJCutOffOuter`
distance, ensuring that the force goes down to zero at `LJCutOffOuter`,
without introducing discontinuities. Note that `LJCutOffInner` must always
be smaller than `LJCutOffOuter`.

```orca
%mm
 SwitchForceLJ true       # Use the switch force scheme for the LJ interaction.
                          # Default: true. 
 LJCutOffInner 10.        # Distance (in Ang). Default: 10 Ang.
 LJCutOffOuter 12.        # Distance (in Ang). Default: 12 Ang.
end
```

### Force Shifting for Electrostatic Interaction

With force shifting for the electrostatic interaction (described in
reference [steinbach1996](../../bibliography.md)) the electrostatic potential is shifted to
zero at the cutoff distance `CoulombCutOff`. If shifting is set to false,
the electrostatic interaction is not truncated at `CoulombCutOff`.

```orca
%mm
 ShiftForceCoulomb true   # Use the shift force scheme for the Coulomb interaction.
                          # Default: true. 
 CoulombCutOff 12.        # Distance (in Ang). Default: 12 Ang.
end
```

### Neglecting Nonbonded Interactions Within Non-Active Region

When using active regions (see
section [multiscalesimulations.qmmm-active](../multiscalesimulations/qmmm-general.md#sec:multiscalesimulations.qmmm-active)) for optimizations and MD runs, the
nonbonded interactions at the MM level can be neglected for those atom
pairs, which are both non-active, without loss of accuracy for the
results. Even relative energies between two structures are correct, if
the atom positions of the non-active atoms are identical. For all other
cases, i.e. if the positions of atoms in the non-active region differ,
the full nonbonded interaction should be computed in the final
single-point energy calculation. By default this option is switched off.

```orca
%mm
 Do_NB_For_Fixed_Fixed true # Compute MM-MM nonbonded interaction also for 
                            # non-active atom pairs. Default true.
end
```

<a id="sec:modelchemistries.mm-rigid-TIP3P"></a>
## Rigid Waters

As TIP3P water might have to be treated as rigid bodies due to its
parametrization - please check out the specifics of the applied force
field parametrization - we offer a keyword for the automated rigid
treatment of all active MM waters. The following keyword applies bond
and angle constraints to active MM waters in optimization as well as MD
runs:

```orca
%mm
 Rigid_MM_Water false       # Default: false. 
end
```

<a id="sec:modelchemistries.mm-keywords"></a>
## Available Keywords for the MM module

Here we list all keywords that are accessible from within the mm block
and that are relevant to MM calculations. 

<a id="tab:modelchemistries.mm-keywords-table"></a>
!!! note "`%mm` block input keywords"


| ****Keyword**** | Options | Description |
| --- | --- | --- |
| **`ShiftForceCoulomb`** | `true`/`false` | Long range electrostatics: Use the Shift Force scheme. Default true. The Shift Force scheme for the Coulomb interaction shifts the Coulomb potential such that it becomes zero at the cutoff distance. |
| **`CoulombCutOff`** | `<real>` | Distance (in Ang). Default: 12 Ang. |
| **`SwitchForceLJ`** | `true`/`false` | Use the Switch Force scheme. Default true. With the Switch Force scheme for the LJ interaction is unchanged up to `LJCutOffInner`. Between `LJCutOffInner` and `LJCutOffOuter` a smooth switching function is applied onto the LJ potential so that the force goes down to zero at `LJCutOffOuter`, without introducing discontinuities. |
| **`LJCutOffInner`** | `<real>` | Distance (in Ang). Default: 10 Ang. |
| **`LJCutOffOuter`** | `<real>` | Distance (in Ang). Default: 12 Ang. |
| **`DielecConst`** | `<real>` | Dielectric constant used in calc. of electrostatic interaction. Default: 1. |
| **`Coulomb14Scaling`** | `<real>` | Scaling factor for electrostatic interaction between 1,4-bonded atoms. Default: 1. |
| **`PrintLevel`** | `<int>` | Printing options: Can be 0 to 4, 0=nothing, 1=normal, ... |

Some of the MM
keywords can also be accessed via the qmmm block, see
section [multiscalesimulations.qmmm-keywords](../multiscalesimulations/qmmm-general.md#sec:multiscalesimulations.qmmm-keywords).

<a id="tab:modelchemistries.mm-keywords-and-qmmm-keywords-table"></a>
!!! note "`%mm` block input keywords which can also be accessed from the `%qmmm` block."


| ****Keyword**** | Options | Description |
| --- | --- | --- |
| **`ORCAFFFilename`** | `"<filename>"` | Filename of the ORCA Force Field prms file. |
| **`Do_NB_For_Fixed_Fixed`** | `true`/`false` | Compute MM-MM nonbonded interaction also within non-active region, i.e. for non-active atom pairs. Default `true`. For `GOAT` and `Crystal-QMMM` default is `false`. |
| **`RIGID_MM_WATER`** | `true`/`false` | Optimization and MD of active MM waters. Default `false`. |
| **`ExtendActiveRegion`** | `distance` | Scheme to extend the active region to activeRegionExt. See also [here](../multiscalesimulations/qmmm-general.md#sec:multiscalesimulations.qmmm-active). `distance`: Use a distance criterion (VDW distance plus `Dist_AtomsAroundOpt`). |
| **—** | `cov_bonds` | Add only atoms bonded covalently to active atoms. |
| **—** | `no` | Do not add any atoms to activeRegionExt. |
| **`Dist_AtomsAroundOpt`** | `<real>` | Distance to be added to VDW distance for `ExtendActiveRegion`. In Angstrom. Default `0.` |
| **`OptRegion_FixedAtoms`** | `{ints}` | List of atoms to define the extended active region. Default: empty list. |
| **`PrintOptRegion`** | `true`/`false` | Additionally print xyz and trj for opt region. Default `true`. |
| **`PrintOptRegionExt`** | `true`/`false` | Additionally print xyz and trj for extended opt region. Default `false`. |
| **`PrintPDB`** | `true`/`false` | Additionally print pdb file for entire system, is updated every iteration for optimization. Default `false`. |

