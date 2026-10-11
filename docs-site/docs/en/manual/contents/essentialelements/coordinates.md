<a id="sec:essentialelements.coordinates"></a>
# Input of Coordinates

Coordinates can be either specified directly in the input file or read
from an external file, and they can be in either Cartesian ("xyz") or
internal coordinate format ("Z-matrix").

## Reading coordinates from the input file

The easiest way to specify coordinates in the input file is by including
a block like the following, enclosed by star symbols:

```orca
* CType Charge Multiplicity
...
coordinate specifications
...
*
```

Here `CType` can be one of `xyz`, `int` (or `internal`), or `gzmt`,
which correspond to Cartesian coordinates, internal coordinates, and
internal coordinates in Gaussian Z-matrix format.

The input of Cartesian coordinates in the "`xyz`" option is
straightforward. Each line consists of the label for a given atom type
and three numbers that specify the coordinates of the atom. The units
can be either Ångström (default) or Bohr.
This can be specified via the simple keywords `!Angs` or `!Bohrs`, respectively,
or via the variable `Units` in the `%coords` block described below.

```orca
* xyz Charge Multiplicity
Atom1   x1  y1  z1
Atom2   x2  y2  z2
 ...
*
```

For example for CO$^+$ in a $S=1/2$ state (multiplicity =
$2\times1/2+1=2$)

```mol
title: structure 1
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
2
structure (1 2)
C           0.0          0.0          0.0
O           0.0          0.0       1.1105
--- input ---
* xyz 1 2
C  0.0  0.0  0.0
O  0.0  0.0  1.1105
*
```

Internal coordinates are specified in the form of the familiar
"Z-matrix". A Z-matrix basically contains information about molecular
connectivity, bond lengths, bond angles and dihedral angles. The program
then constructs Cartesian coordinates from this information. Both sets
of coordinates are printed in the output such that conversion between
formats is facilitated. The input in that case looks like:

```orca
* int Charge Multiplicity
Atom1  0  0  0    0.0   0.0   0.0
Atom2  1  0  0    R1    0.0   0.0
Atom3  1  2  0    R2    A1    0.0
Atom4  1  2  3    R3    A2    D1
. . .
AtomN  NA NB NC   RN    AN    DN
*
```

The rules for connectivity in the "`internal`" mode are as follows:

-   `NA`: The atom that the actual atom has a distance (`RN`) with.

-   `NB`: The actual atom has an angle (`AN`) with atoms `NA` and `NB`.

-   `NC`: The actual atom has a dihedral angle (`DN`) with atoms `NA`,
    `NB` and `NC`. This is the angle between the actual atom and atom
    `NC` when looking down the `NA-NB` axis.

-   Note that - contrary to other parts in ORCA - atoms are counted
    starting from 1.

Angles are always given in degrees! The rules are compatible with those
used in the well known MOPAC and ADF programs.

Finally, `gzmt` specifies internal coordinates in the format used by the
Gaussian program. This resembles the following:

```orca
* gzmt 0 1
    C
    O   1   4.454280
    Si  2   1.612138    1   56.446186
    O   3   1.652560    2   114.631525  1   -73.696925
    C   4   1.367361    3   123.895399  2   -110.635060
    ...
*
```

An alternative way to specify coordinates in the input file is through
the use of the `%coords` block, which is organized as follows:

```orca
%coords
 CTyp   xyz     # the type of coordinates = xyz or internal
 Charge 0       # the total charge of the molecule
 Mult   2       # the multiplicity = 2S+1
 Units  Angs    # the unit of length = angs or bohrs

 # the subblock coords is for the actual coordinates
 # for CTyp=xyz
  coords
     Atom1   x1  y1  z1
     Atom2   x2  y2  z2
  end
 # for CTyp=internal
  coords
     Atom1  0  0  0    0.0   0.0   0.0
     Atom2  1  0  0    R1    0.0   0.0
     Atom3  1  2  0    R2    A1    0.0
     Atom4  1  2  3    R3    A2    D1
      . . .
     AtomN  NA NB NC   RN    AN    DN
  end
end
```

!!! warning
    Since ORCA is a C++ based program its internal counting starts from zero.
    Therefore all electrons, atoms, frequencies, orbitals, excitation energies etc. are counted
    from zero. User-based counting such as the numeration of fragments is counted from one.

## Reading coordinates from external files

It is also possible to read the coordinates from external files. The
most common format is a `.xyz` file, which can in principle contain more
than one structure (see section
[optimization.multiplexyz](../structurereactivity/optimizations_scans.md#sec:structurereactivity.optimization.multiplexyz) for this multiple XYZ
feature):

```orca
* xyzfile Charge Multiplicity Filename
```

For example:

```orca
* xyzfile 1 2 mycoords.xyz
```

A lot of graphical tools like Gabedit, molden or Jmol can write Gaussian
Z-Matrices (`.gzmt`). ORCA can also read them from an external file with
the following

```orca
* gzmtfile 1 2 mycoords.gzmt
```

Note that if multiple jobs are specified in the same input file then new
jobs can read the coordinates from previous jobs. If no filename is
given as fourth argument then the name of the actual job is
automatically used.

```orca
... specification for the first job

$new_job
! keywords
* xyzfile 1 2
```

In this way, optimization and single point jobs can be very conveniently
combined in a single, simple input file. Examples are provided in the
following sections.

!!! note
    The keyword lines in this section must end with an OS-appropriate line-terminating character sequence after the file name
    (i.e. `\n` on Linux/MacOS or `\r\n` on Windows) to avoid parsing errors.

<a id="sec:essentialelements.coordinates.special"></a>
## Special definitions

-   **Dummy atoms** are defined in exactly the same way as any other
    atom, by using "DA", "X", or "Xx" as the atomic symbol.

-   **Ghost atoms** are specified by adding ":" right after the symbol
    of the element (see
    [essentialelements.counterpoise](counterpoise.md#sec:essentialelements.counterpoise)).

-   **Point charges** are specified with the symbol "Q", followed by the
    charge (see
    [coordinates.pointcharges](#sec:essentialelements.coordinates.pointcharges)).

-   **Embedding potentials** are specified by adding a "\>" right after
    the symbol of the element (see
    [basisset.embeddingpotentials](basisset.md#sec:essentialelements.basisset.embeddingpotentials)).

-   **Non-standard** isotopes or nuclear charges are specified with the
    statements "`M = `..." and "`Z = `...", respectively, after the
    atomic coordinate definition.

    1. The nuclear charge can adopt non-integer values
    2. When the nuclear charge is modified throughca "`Z = `..." statement, the total charge of the system should still be calculated based on the unmodified charge. For example, for a
    calculation of a single hydrogen atom whose `Z` is set to 1.5, a
    charge of 0 and a spin multiplicity of 2 should be entered into the
    charge and multiplicity sections of the input file, despite that the
    actual total charge is 0.5.

-   **Fragments** can be conveniently defined by declaring the fragment
    number a given atom belongs to in parentheses "`(n)`" following the
    element symbol (see
    [essentialelements.fragmentation](fragmentation.md#sec:essentialelements.fragmentation)).

<a id="sec:essentialelements.coordinates.parascan"></a>
## Defining Geometry Parameters and Scanning Potential Energy Surfaces

ORCA lets you define the coordinates of all atoms as functions of user
defined geometry parameters. By giving not only a value but a range of
values (or a list of values) to this parameters potential energy
surfaces can be scanned. In this case the variable `RunTyp` is
automatically changed to `Scan`. The format for the parameter
specification is straightforward:

```orca
%coords
 CTyp   internal
 Charge 0
 Mult   1
 pardef
  rCH  = 1.09;    # a C-H distance
  ACOH = 120.0;   # a C-O-H angle
  rCO  = 1.35, 1.10, 26; # a C-O distance that will be scanned
 end
 coords
    C  0  0  0   0     0         0
    O  1  0  0  {rCO}  0         0
    H  1  2  0  {rCH}  {ACOH}    0
    H  1  2  3  {rCH}  {ACOH}  180
 end
end
```

In the example above the geometry of formaldehyde is defined in internal
coordinates (the geometry functions work exactly the same way with
Cartesian coordinates). Each geometric parameter can be assigned as a
function of by enclosing an expression within function braces, "`{} `".
For example, a function may look like `*cos(Theta)*rML+R`. Note that all
trigonometric functions expect their arguments to be in degrees and not
radians. The geometry parameters are expected to be defined such that
the lengths come out in Ångströms and the angles in degrees. *After*
evaluating the functions, the coordinates will be converted to atomic
units. In the example above, the variable `rCO` was defined as a "Scan
parameter". Its value will be changed in 26 steps from 1.3 Å down to 1.1
Å and at each point a single point calculation will be done. At the end
of the run the program will summarize the total energy at each point.
This information can then be copied into the spreadsheet of a graphics
program and the potential energy surface can be plotted. Up to three
parameters can be scan parameters. In this way grids or cubes of energy
(or property) values as a function of geometry can be constructed.

If you want to define a parameter at a series of values rather than
evenly spaced intervals, the following syntax is to be used:

```orca
%coords
 CTyp   internal
 Charge 0
 Mult   1
 pardef
  rCH = 1.09;   # a C-H distance
  ACOH= 120.0;  # a C-O-H angle
  rCO [1.3 1.25 1.22 1.20 1.18 1.15 1.10];  # a C-O distance that will be scanned
 end
 coords
    C  0  0  0   0     0         0
    O  1  0  0  {rCO}  0         0
    H  1  2  0  {rCH}  {ACOH}    0
    H  1  2  3  {rCH}  {ACOH}  180
 end
end
```

In this example the C-O distance is changed in seven non-equidistant
steps. This can be used in order to provide more points close to a
minimum or maximum and fewer points at less interesting parts of the
surface.

A special feature has also been implemented into ORCA - the parameters
themselves can be made functions of the other parameters as in the
following (nonsense) example:

```orca
%coords
 CTyp   internal
 Charge 0
 Mult   1
 pardef
  rCOHalf= 0.6;
  rCO    = { 2.0*rCOHalf };
 end
 coords
    C  0  0  0   0     0         0
    O  1  0  0  {rCO}  0         0
    O  1  0  0  {rCO}  180       0
 end
end
```

In this example the parameter `rCO` is computed from the parameter
`rCOHalf`. In general the geometry is computed (assuming a `Scan`
calculation) by:
(a) incrementing the value of the parameter to be
scanned
(b) evaluating the functions that assign values to parameters,
and
(c) evaluating functions that assign values to geometrical
variables.

Although it is not mandatory, it is good practice to *first*
define the static or scan-parameters and then define the parameters that
are functions of these parameters.

Finally, ORCA has some special features that may help to reduce the
computational effort for surface scans:

```orca
%method
 SwitchToSOSCF true      # switches the converger to SOSCF
                         # after the first point. SOSCF may
                         # converge better than DIIS if the
                         # starting orbitals are good.
                         # default = false
 ReducePrint true        # reduce printout after the first point
                         # default=true

 # The initial guess can be changed after the first point.
 # The default is MORead. The MOs of the previous point will,
 # in many cases, be a very good guess for the next point.
 # However, in some cases you may want to be more conservative
 # and use a general guess.

 ScanGuess   OneElec    # the one-electron matrix
             Hueckel    # the extended Hueckel guess
             PAtom      # the PAtom guess
             PModel     # the PModel guess
             MORead     # MOs of the previous point
 end
```

!!! note
    -   You can scan along normal modes of a Hessian using the `NMScan`
        feature as described in section
        [scan.normalModeScan](../spectroscopyproperties/tddft.md#sec:spectroscopyproperties.tddft.scan.normalModeScan).

    -   The surface scan options are also supported in conjunction with
        TD-DFT/CIS or MR-CI calculations (see section
        [tddft.scan](../spectroscopyproperties/tddft.md#sec:spectroscopyproperties.tddft.scan)).

<a id="sec:essentialelements.coordinates.mixed"></a>
## Mixing internal and Cartesian coordinates

In some cases it may be practical to define some atomic positions in
Cartesian and some in internal coordinates. This can be achieved by
specifying all coordinates in the `*int` block: using "0 0 0" as
reference atoms indicates Cartesian coordinates. Note that for the first
atom the flags are "1 1 1", as "0 0 0" would be the normal values for
internal coordinates. Consider, for example, the relaxed surface scan
from section
[optimization.relaxedsurface](../structurereactivity/optimizations_scans.md#sec:structurereactivity.optimization.relaxedsurface), where the methyl
group is given first in an arbitrary Cartesian reference frame and then
the water molecule is specified in internal coordinates:

```orca
* CType Charge Multiplicity
...
coordinate specifications
...
*
```

Internal and Cartesian coordinates can thus be mixed in any order but it
is recommended that the first 3 atoms are specified in Cartesian
coordinates in order to define a unique reference frame.

<a id="sec:essentialelements.coordinates.pointcharges"></a>
## Inclusion of Point Charges

In some situations it is desirable to add point charges to the system.
In ORCA there are two mechanisms to add point-charges. If you only want
to add a few point charges you can "mask" them as atoms as in the
following (nonsense) input:

```orca
* xyz Charge Multiplicity
Atom1   x1  y1  z1
Atom2   x2  y2  z2
 ...
*
```

Here the "Q"'s define the atoms as point charges. The next four numbers
are the magnitude of the point charge and its position. The program will
then treat the point charges as atoms with no basis functions and
nuclear charges equal to the "Q" values.

If you have thousands of point charges to treat, as in a QM/MM
calculation, it is more convenient, and actually necessary, to read the
point charges from an external file as in the following example:

```mol
title: structure 2
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
2
structure (1 2)
C           0.0          0.0          0.0
O           0.0          0.0       1.1105
--- input ---
* xyz 1 2
C  0.0  0.0  0.0
O  0.0  0.0  1.1105
*
```

The program will now read the file "`pointcharges.pc`" that contains the
point-charge information and then call the module `orca_pc` which adds
the point charge contribution to the one-electron matrix and the nuclear
repulsion. The file "`pointcharges.pc`" is a simple ASCII file in the
following format:

```orca
3
 -0.834  -1.3130    0.0000   -0.0310
  0.417  -1.8700    0.7570    0.1651
  0.417  -1.8700   -0.7570    0.1651
```

The first line gives the number of point charges. Each consecutive line
gives the magnitude of the point charge (in atomic units) and its
position (in Ångström units!). However, it should be noted that ORCA
treats point charges from an external file differently than "Q" atoms.
When using an external point charge file, the interaction between the
point charges is not included in the nuclear energy. This behavior
originates from QM/MM, where the interactions among the point charges is
done by the MM program. These programs typically use an external point
charge file when generating the ORCA input. To add the interaction of
the point charges to the nuclear energy, the `DoEQ` keyword is used
either in the simple input or the `%method` block as shown below.

```orca
# A non QM/MM pointcharge calculation
! DoEQ

%pointcharges "pointcharges.pc"

%method
   DoEQ true
end
```

!!! warning
    The `DoEQ` keyword has no effect for semi-empirical calculations (e.g., AM1)!

