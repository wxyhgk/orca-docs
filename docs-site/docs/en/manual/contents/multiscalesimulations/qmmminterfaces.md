
<a id="sec:multiscalesimulations.qmmminterfaces.interfaces"></a>
# QM/MM via Interfaces to ORCA

ORCA is easy to interface as a QM engine in pretty much any QM/MM
environment, as it will accept a set of point charges from an external
file (see section
[coordinates.pointcharges](../essentialelements/coordinates.md#sec:essentialelements.coordinates.pointcharges)) and it will return, in a
transparent format, all the required information for computing energies
and gradients to the driving program. In our research group we have
experience with four different QM/MM environments: ChemShell, Gromacs,
pDynamo and NAMD. Each of the interfaces is described in the following section.
It is beyond the scope of the manual to be exhaustive, and only minimal
working examples are going to be presented. These will cover mainly the
technical aspects with respect to the QM part of the QM/MM calculation.
For the initial preparation of the system the user is referred to the
documentation of the driving program.

## ORCA and Gromacs

In cooperation with the developers of Gromacs software package we
developed an interface to ORCA. The interface is available starting with
Gromacs version 4.0.4 up to version 4.5.5.

As mentioned above, the initial setup has to be done with the Gromacs.
In the QM/MM calculation Gromacs will call ORCA to get the energy and
the gradients of the QM atoms. The interface can be used to perform all
job types allowed by the Gromacs software package, e.g. optimizations,
molecular dynamics, free energy. In addition, for geometry optimizations
we have implemented a microiterative scheme that can be requested by
setting the keyword `bOpt = yes` in the Gromacs `.mdp` file. This will
cause ORCA to perform a QM geometry optimization every time it is called
by Gromacs. During this optimization ORCA will also compute the
Lennard-Jones interaction between the QM and MM atoms, and freeze the
boundary atoms. This microiterative scheme can also be used to perform a
transition state optimization. If you are looking for a transition state
and have a good initial guess for the structure, you can carry out an
optimization of the MM system and at the same time perform a transition
state optimization of the QM system with ORCA via the microiterative
scheme. Since it is expensive to calculate the Hessian for each
microiterative step, the user can tell ORCA to use the
(updated) Hessian matrix of the previous step via `read_temp_Hess` in
the ORCA input.

In order to allow full flexibility to the user, the information for the
QM run are provided in a separate plain text file, called
`GromacsBasename.ORCAINFO`. When Gromacs writes the input for the
ORCA calculation, it will merge this file with the information on the
coordinates, point charges, Lennard-Jones coefficients and type of
calculation (`EnGrad`, `Opt`, `TSOpt`).

Below is a typical example of an input file created by Gromacs, where
for each Gromacs optimization step, a full optimization of the QM-part
will be performed by ORCA, instead of just doing the energy and gradient
calculation.

```orca
# Optimization step in the Lennard-Jones and point charges field of the MM atoms
! QMMMOpt

# file containing the Lennard Jones coefficients for the Lennard-Jones interaction
%LJCoefficients "temp.LJ"
# file containing the point charges for the electrostatic interaction
%pointcharges "temp.pc"

%geom
    # calculate the exact Hessian before the first optimization step
    Calc_Hess true
    # in case of a TS optimization the updated Hessian of the previous
    # TS optimization run is read instead of calculating a new one
    read_temp_Hess true
 end
```

!!! note

    -   If you are using `bOpt` or `bTS` you have to take care of additional
        terms over the boundary. Either you can zero out the dihedral terms
        of the Q2-Q1-M1-M2 configurations, or you can fix the respective Q2
        atoms.

    -   If you want to use the ORCA constraints, you have to also put them
        in the Gromacs part of the calculation.

    -   If there are no bonds between the QM and MM systems, the `bOpt`
        optimization of the QM system might have convergence problems. This
        is the case if the step size is too large and thus QM atoms come too
        close to MM atoms. The convergence problems can be circumvented by
        adding extra coordinates and Hessian diagonal values for Cartesian
        coordinates of selected QM atoms to the set of internal coordinates.
        This should be done for only few atoms that are in the boundary
        region.

    ```orca
    %geom
        # add the Cartesian position of atoms 2 and 4 to the
        # set of internal coordinates with a diagonal Hessian value of 0.1
        Hess_Internal
        {C 2 D 0.1}
        {C 4 D 0.1}
        end
    end
    ```

 
## ORCA and pDynamo

The interface with the pDynamo library is briefly documented
[here](https://sites.google.com/site/pdynamomodeling/). It
uses the same plain text files to exchange information between the
pDynamo library and ORCA. In order to have simiar functionality as
presented above, we have extended the interface to generate more complex
ORCA input files by accepting verbatim blocks of text. We have also
implemented in pDynamo the capability of writing files containing
Lennard-Jones parameters.

A simple example which calculates the QM/MM energy for a small designed
peptide in which the side chain of one amino acid is treated QM is
ilustrated below. For this example, a complete geometry optimization is
going to be performed during the ORCA call.

```python
import os
import pCore
import pBabel
import pMolecule
import pMoleculeScripts

# Read the initial coordinates from the .pdb file.
system = pMoleculeScripts.PDBFile_ToSystem(
        "1UAO.pdb", modelNumber=1, useComponentLibrary=True)

# Instantiate the required models.
mmmodel = pMolecule.MMModelOPLS("protein")
nbmodel = pMolecule.NBModelORCA()
qcmodel = pMolecule.QCModelORCA(
        command=os.getenv("ORCA_COMMAND"),
        deleteJobFiles=False, header="bp86 def2-svp qmmmopt/pdynamo",
        job="chignolin", run=True)

# Assign the models to the system.
system.DefineMMModel(mmmodel)
system.DefineQCModel(
        qcmodel, qcSelection=pCore.Selection([35, 36, 37, 34, 40, 41]))
system.DefineNBModel(nbmodel)
system.electronicState = pMolecule.ElectronicState(
        charge=-1, multiplicity=1)

# Print a summary and calculate the energy.
system.Summary()
system.Energy()
```

After the execution of the above Python program, a series of files are
going to be created `chignolin.inp`, `chignolin.pc`, `chignolin.lj` and
ORCA is going to be called. The generated ORCA input file is listed
below.

```orca
%geom
    # add the Cartesian position of atoms 2 and 4 to the
    # set of internal coordinates with a diagonal Hessian value of 0.1
    Hess_Internal
    {C 2 D 0.1}
    {C 4 D 0.1}
    end
end
```

There are few points that have to be raised here. Because the keyword
`qmmm/pdynamo` was specified in the `header` variable, the pDynamo
library will automatically add the `constraint` block in the ORCA input,
which will freeze the link atoms and the QM atoms to which they are
bound. It will also generate the `chignolin.lj` file containing all the
Lennard-Jones parameters. The important parts of this file, which is
somewhat different than the one generated by Gromacs, are listed next.

```orca
# number of atoms  combination rule
138 0
#      x            y             z          sigma       epsilon   id
   -6.778000    -1.424000     4.200000     3.250000     0.711280   -1
   -6.878000    -0.708000     2.896000     3.500000     0.276144   -1
   -5.557000    -0.840000     2.138000     3.750000     0.439320   -1
...
    0.433000     0.826000     0.502000     2.960000     0.878640   -1
   -0.523000     0.687000     3.249000     3.500000     0.276144    1
    0.418000     1.724000     3.866000     3.750000     0.439320    2
   -0.069000     2.762000     4.283000     2.960000     0.878640    3
    1.609000     1.463000     3.911000     2.960000     0.878640    4
   -2.259000    -0.588000     1.846000     0.000000     0.000000   -1
   -1.795000     2.207000     2.427000     2.500000     0.125520   -1
   -1.224000     0.346000     3.997000     2.500000     0.125520    5
    0.055000    -0.151000     2.889000     2.500000     0.125520    6
   -0.311000     2.922000     0.557000     3.250000     0.711280   -1
...
   -1.387000    -2.946000     5.106000     2.500000     0.125520   -1
# number of special pairs
22
#        atom1        atom2    factor
          34           32     0.000000
          35           39     0.500000
          40           31     0.000000
          41           30     0.500000
          41           32     0.500000
          36           31     0.500000
          40           32     0.500000
          40           39     0.500000
          34           31     0.000000
          35           30     0.500000
          34           11     0.500000
          34           38     0.500000
          41           31     0.000000
          37           31     0.500000
          34           33     0.500000
          34           39     0.000000
          40           30     0.500000
          41           39     0.500000
          34           30     0.000000
          35           31     0.000000
          34           42     0.500000
          35           32     0.500000
```

The second number on the first line refers to the type of combination
rule used to calculate the Lennard-Jones interaction. It is 0 if a
geometric average is used (OPLS force field), or 1 for the
Lorentz-Berthelot rules (AMBER force field). The `id` on the last column
is -1 for MM atoms and is equal to the atom number for the QM atoms. In
this case the hydrogen link atom is atom 0. The last block of the file
is composed of atom pairs and a special factor by which their
Lennard-Jones interaction is scaled. In general this factor is equal to
1, but for atoms one or two bonds apart is zero, while for atoms three
bonds apart depends on the type of force field, and in this case is 0.5.

After successful completion of the ORCA optimization run, the
information will be relayed back the pDynamo library, which will report
the total QM/MM energy of the system. At this point the type QM/MM of
calculation is limited only by the capabilities of the pDynamo library,
which are quite extensive.

## ORCA and NAMD

Since version 2.12, NAMD is able to perform hybrid QM/MM calculations. A
more detailed explanation of all available key words, setting up the
calculation and information on tutorials and on the upcoming graphic
interface to VMD are available on the NAMD
[website](http://www.ks.uiuc.edu/~rcbernardi/QMMM/).

Similar to other calculations with NAMD, the QM/MM is using a pdb file
to control the active regions. An example is shown below, where the
sidechain of a histidine protonated at N$\epsilon$ is chosen to be the
QM region. Either the occupancy column or the b-factor column of the
file are used to indicate which atom are included in a QM area and which
are treated by the forcefield. In the other column, atoms which are
connecting the QM area and the MM part are indicated similarly. To
clarify which column is used for which purpose, the keywords `qmColumn`
and `qmBondColumn` have to be defined in the NAMD input.

    ...
    ATOM   1737  CA  HSE P 117      14.762  47.946  31.597  1.00  0.00      PROT C
    ATOM   1738  HA  HSE P 117      14.751  47.579  32.616  0.00  0.00      PROT H
    ATOM   1739  CB  HSE P 117      14.129  49.300  31.501  1.00  1.00      PROT C
    ATOM   1740  HB1 HSE P 117      14.407  49.738  30.518  0.00  1.00      PROT H
    ATOM   1741  HB2 HSE P 117      13.024  49.194  31.509  0.00  1.00      PROT H
    ATOM   1742  ND1 HSE P 117      13.899  51.381  32.779  0.00  1.00      PROT N
    ATOM   1743  CG  HSE P 117      14.572  50.261  32.582  0.00  1.00      PROT C
    ATOM   1744  CE1 HSE P 117      14.615  52.043  33.669  0.00  1.00      PROT C
    ATOM   1745  HE1 HSE P 117      14.356  53.029  34.064  0.00  1.00      PROT H
    ATOM   1746  NE2 HSE P 117      15.678  51.318  33.982  0.00  1.00      PROT N
    ATOM   1747  HE2 HSE P 117      16.369  51.641  34.627  0.00  1.00      PROT H
    ATOM   1748  CD2 HSE P 117      15.706  50.183  33.335  0.00  1.00      PROT C
    ATOM   1749  HD2 HSE P 117      16.451  49.401  33.388  0.00  1.00      PROT H
    ATOM   1750  C   HSE P 117      13.916  47.000  30.775  0.00  0.00      PROT C
    ATOM   1751  O   HSE P 117      12.965  46.452  31.334  0.00  0.00      PROT O
    ...

NOTES:

-   If one wants to include more than one QM region, integers bigger
    than 1 can be used to define the different regions.

-   Charge groups cannot be split when selecting QM and MM region. The
    reason is that non-integer partial charges may occur if a charge
    group is split. Since the QM partial charges are updated in every QM
    iteration, this may lead to a change in the total charge of the
    system over the course of the MD simulation.

-   The occupancy and b-factor columns are used for several declarations
    in NAMD. If two of these come together in one simulation, the
    keyword `qmParamPDB` is used to define which pdb file contains the
    information about QM atoms and bonds.

-   To simplify the selection of QM atoms and writing the pdb file a set
    of scripts is planned to be included in future releases of NAMD.

To run the calculation, the keyword `qmForces on` must be set. To select
ORCA  `qmSoftware "orca"` must be specified and the path to the
executables must be given to `qmExecPath`, as well as a directory where
the calculation is carried out (`qmBaseDir`). To pass the method and
specifications from NAMD to ORCA  `qmConfigLine` is used. These lines
will be copied to the beginning of the input file and can contain both
simple input as well as block input. To ensure the calculation of the
gradient, the `engrad` keyword should be used.

The geometry of the QM region including the selected links as well as
the MM point charges are copied to the ORCA inputfile automatically.
Multiplicity and charge can be defined using `qmMult` and `qmCharge`,
although the latter can be determined automatically by NAMD using the MM
parameters. It should be noted at this point that NAMD is capable to
handle more than one QM region per QM/MM calculation. Therefore for each
region, charge and multiplicity are expected. In the case of only one QM
region, the input looks like the following:

    qmMult          "1 1"
    qmCharge        "1 0"

Currently, two charge modes are available: Mulliken and CHELPG. They
have to be specified in the NAMD input using `QMChargeMode` and in the
`qmConfigLine`, respectively. Different embedding schemes, point charge
schemes and switching functions are available, which will be not further
discussed here. Another useful tool worth mentioning is the possibility
to call secondary executables before the first or after each QM software
execution using `QMPrepProc` or `QMSecProc`, respectively. Both are
called with the complete path and name to the QM input file, allowing
e.g. storage of values during an QM/MM-MD.

It is strongly emphasized that at this points both programs are
constantly developed further. For the latest information, either the
ORCA forum or the NAMD website should be consulted.
