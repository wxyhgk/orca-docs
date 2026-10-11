

<a id="sec:property_file.detailed"></a>
# Property File

One of the files that ORCA produces, during a calculation, is the *property file*. The name of the file is `basename.property.txt`, where `basename` is the basename of the input file.

The property file has mainly two usages in ORCA. The first usage is to work as basis for the *Compound* scripting language. *Compound* reads all its information concerning properties through the property file and not through parsing of the ORCA output. The second usage of the property file is to make it easier for other programs, or potential GUIs, to create interfaces with ORCA.

The advantage of the property file compared to the normal ORCA output is that it's syntax is well defined and so it is easier to parse it.
It can also be converted to JSON format as shown below.

Writing to the property file is enabled by default for most calculations.
It can be disabled via `!NoPropFile` or toggled on/off in the `%output` block:

``` orca
%output
  PropFile false  # default: true
end
```

!!! warning
    Since the whole file is read and re-written multiple times for each single point calculation,
    optimizations of systems with a few thousand atoms can incur a few milliseconds of stacking I/O overhead,
    per optimization cycle (i.e., a few seconds per cycle after several hundred steps).
    Thus, it is recommended to disable the property file for such calculations
    and this is done by default for `GOAT`, `MD-L-Opt`, `MM`, or `GFN-FF` chosen in the simple input.

<a id="sec:property_file.txtFormat.detailed"></a>
## TXT Format

After any ORCA calculation a property file is created with the extension `.property.txt`. The file is a text file and one can read it and edit it with any available text editor. Below we will analyze the syntax of the file.

The file always starts with the following three lines:

```orca
*************************************************
******************* ORCA 6.1.x ******************
*************************************************
```

where, obviously the version of ORCA changes
(it is also stored in `Calculation_Status -> version`).

Then, the file consists of a list of properties. Each property starts with the symbol `$` followed by the name of the property and ends with the symbol `$` followed by `End`.

For example:
```orca
$SCF_Nuc_Gradient
   &GeometryIndex 1
   &NAtoms [&Type "Integer"] 2
   &gradNorm [&Type "Double"]       7.6940943132805237e-02
   &grad [&Type "ArrayOfDoubles", &Dim (6,1)]
                                                         0

0                                      6.7009699964043727e-10
1                                     -1.3755030800675890e-10
2                                      5.4405462640094826e-02
3                                     -6.7009699282161039e-10
4                                      1.3755031156980307e-10
5                                     -5.4405462640095381e-02
   &Method [&Type "String"] "SCF"
   &Level [&Type "String"] "Relaxed density"
   &Mult [&Type "Integer"] 1
   &State [&Type "Integer"] 0
   &Irrep [&Type "Integer"] 0
$End
```

Each property consists of *components*. Each component starts with the symbol `&` and has no ending symbol.

For example:

```orca
   &gradNorm [&Type "Double"]       7.6940943132805237e-02
```

The first component in every property is `GeometryIndex`,
which shows the geometry to which the current property belongs.
For example:

```orca
&GeometryIndex 1
```

Note that geometry indices start from 1.

The remaining components have the following syntax:
- First the start of component symbol `&`.
- Then follows the name of the component.
- Then a bracket opens with various bracket information about the component. For details on the syntax of the bracket information please check [bracketInfo.detailed](#sec:property_file.txtFormat.bracketInfo.detailed).

After the bracket there are different options.

If the type is `String` then a string is expected starting with quotation marks.
For example:

```orca
&Method [&Type "String"] "SCF"
```

If the type is `Double` or `Integer` then a number of the appropriate type is expected.
For example:

```orca
&NAtoms [&Type "Integer"] 2 "Number of atoms"
```

As in the example above, a component description or comment in quotation marks may be optionally present after the value in the same line as the component name.
Note that for `Array` components, the comment actually comes *before* the data.

Finally, if the type is a kind of `Array` then, after the optional comment,
an array is written starting from the next line.
Arrays are written in blocks of up to 8 whitespace-sparated columns.
Each block starts with a line with column indices (starting from 0).
The second line in a block is reserved but currently ignored.
The next lines start with the row index and continue with the data for the respective row/columns.
For example:

```orca
   &dipoleTotal [&Type "ArrayOfDoubles", &Dim (3,1)] "Total"
                                                         0

0                                     -5.1716015643064861e-01
1                                      5.1774970936823518e-02
2                                      7.8324050140722279e-01
```

Note that `Complex` scalars are printed as two consecutive values for the real and imaginary part (before the optional comment),
whereas for `ArrayOfComplex` the real part of the whole array is printed first,
followed by the imaginary part.

<a id="sec:property_file.txtFormat.bracketInfo.detailed"></a>
### Bracket Information

Bracket information is a list of entries separated with ','.
The first and most important bracket entry is the `Type`,
which can be one of the following:
- `Double`
- `Integer`
- `Boolean`
- `Complex`
- `String`
- `ArrayOfDoubles`
- `ArrayOfIntegers`
- `ArrayOfBooleans`
- `ArrayOfComplex`
- `Coordinates`
%-  "MixedMatrix"  % NOT IMPLEMENTED

For example:

```orca
&NAtoms [&Type "Integer"] 2
```

Then, in case the `Type` is a kind of array, the bracket must contain the dimensions of the array, using the `Dim` entry. Note that all arrays are 2-dimensional!
For example:

```orca
&ATNO [&Type "ArrayOfIntegers", &Dim (2,1)]
```

Optionally, `Units` may also be given, if the value is not in a.u. For example:

```orca
&dipoleMagnitude [&Type "Double", &Units "Debye"]       9.4000050960598935e-01
```

<a id="sec:property_file.jsonFormat.detailed"></a>
## JSON Format

The property file can be also produced in a JSON format. Internally this happens through transformation of the `txt` format to JSON format. There are two ways to create a JSON property file.

The first way is through the normal ORCA input using the `JSONPropFile` keyword.

```orca
%Output
  JSONPropFile True
End
```

this will create a `basename.property.txt` and in addition a `basename.property.json` file.

The second way is through the [`orca_2json` command](orca_2json.md#sec:orca_2json.availableinformation.propertyFile).
For this, one first has to run a normal ORCA input, that will create a `basename.property.txt` file,
and then convert it to `basename.property.json` using the command:

```orca
orca_2json basename -property
```

The file is structured as follows:
```orca
{
  "<GlobalPropertyName>": {
    "<ComponentName>": <value>,
    <More components>
  },
  <More global properties>
  "Geometries": [
    {
      "Geometry": {
        "Coordinates": {
            "Cartesians": [
                [
                    "<Symbol>",
                    <X>,
                    <Y>,
                    <Z>
                ],
                <More atoms>
            ],
            "Type": "Cartesians",
            "Units": "a.u."
        },
        "NAtoms": <value>,
        <More components>
      },
      "<PropertyName>": {
        "<ComponentName>": <value>,
        <More components>
      },
      <More properties for this geometry>
    },
    <More geometries>
  ]
}
```

The "global", i.e. geometry-independent properties are:
`Calculation_Status`, `Calculation_Info`, and `Calculation_Timings`.

Most component data types are directly converted to the corresponding JSON types.
All `Array` components are stored as two-dimensional using nested lists (even if one dimension is of length 1). `Complex` and `ArrayOfComplex` values are stored as separate real and imaginary parts:
```orca
"ComplexComponentName": {
  "re": <real part>,
  "im": <imaginary part>
},
"ComplexArrayComponentName": {
  "re": [
      [<r11>, <r12>, <...>],
      [<r21>, <r22>, <...>],
      <...>
    ],
  "im": [
      [<i11>, <i12>, <...>],
      [<i21>, <i22>, <...>],
      <...>
    ]
}
```

<a id="sec:property_file.list"></a>
## List of Available Properties

!!! note "List of available properties"
    | Property | M | Component | T | O | L | Description | Units |
    |---|---|---|---|---|---|---|---|
    | AutoCI_Energies [Energy] | Y | numOfEl | I | N | N |  |  |
    |  |  | numOfCorrEl | I | N | N |  |  |
    |  |  | numOfAlphaCorrEl | I | Y | N |  |  |
    |  |  | numOfBetaCorrEl | I | Y | N |  |  |
    |  |  | refEnergy | AD | N | N | Reference energy for each state |  |
    |  |  | corrEnergy | AD | N | N | Total correlation energy for each state |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | totalEnergy | AD | N | N | Total energy of each state |  |
    |  |  | Mult | AI | Y | N | Multiplicity of each state |  |
    |  |  | Irrep | AI | Y | N | Irreducible representation of each state |  |
    |  |  | RelCorr | S | Y | N | Relativistic correction (SOC and/or SSC) |  |
    |  |  | NBlocks | I | Y | N | Number of multiplicity blocks |  |
    |  |  | NRoots | AI | Y | N | Number of roots in each block |  |
    |  |  | NTotalRoots | I | Y | N | Total number of roots |  |
    |  |  | Block | AI | Y | N | Block index of each state |  |
    |  |  | Root | AI | Y | N | Root index within the block |  |
    |  |  | FollowIRoot | I | Y | N | Index of the followed root |  |
    |  |  | AvgMult | AD | Y | N | Average multiplicity of each SO-/SS-coupled state |  |
    | AutoCI_Dipole_Moment [Dipole_Moment] | Y | dipoleMagnitude | D | N | N |  | a.u. |
    |  |  | dipoleElecContrib | AD | N | N | Electronic contribution |  |
    |  |  | dipoleNucContrib | AD | N | N | Nuclear contribution |  |
    |  |  | dipoleTotal | AD | N | N | Total |  |
    |  |  | doAtomicDipole | B | N | N |  |  |
    |  |  | atomicDipole | AD | Y | N | Atomic dipoles (NAtoms * X,Y,Z) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | EFG_Tensor | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | QFAC | D | N | Y | Prefactor |  |
    |  |  | V | AD | N | Y | Raw tensor |  |
    |  |  | VEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | VIso | D | N | Y |  |  |
    | AutoCI_Polarizability [Polarizability] | Y | isotropicPolar | D | N | N |  |  |
    |  |  | rawCartesian | AD | N | N |  | a.u |
    |  |  | diagonalizedTensor | AD | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | doAtomicPolar | B | N | N |  |  |
    |  |  | atomicPolarIso | AD | Y | N | Atomic istotropic polarizabilities |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | AutoCI_Quadrupole_Moment [Quadrupole_Moment] | Y | isotropicQuadMoment | D | N | N |  | a.u. |
    |  |  | quadElecContrib | AD | N | N | Electronic contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadNucContrib | AD | N | N | Nuclear contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadTotal | AD | N | N | Total. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadDiagonalized | AD | N | N | The diagonalized tensor | a.u. |
    |  |  | doAtomicQuad | B | N | N |  |  |
    |  |  | atomicQuad | AD | Y | N | Atomic quadrupoles (NAtoms * XX, YY, ZZ, XY, XZ, YZ) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | AutoCI_A_Tensor [A_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elem | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | PFAC | D | N | Y | Prefactor PFAC=gegNbe*bN (in MHz) |  |
    |  |  | ARaw | AD | N | Y | Raw tensor |  |
    |  |  | AEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | AIso | D | N | Y |  |  |
    | AUTOCI_Chemical_Shift [Chemical_Shift] | Y | numOfNucs | I | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | SDSO | AD | N | Y | Diamagnetic contribution |  |
    |  |  | SPSO | AD | N | Y | Paramagnetic contribution |  |
    |  |  | STot | AD | N | Y | Total tensor |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | sTotEigen | AD | N | Y | Eigenvalues |  |
    |  |  | siso | D | N | Y |  |  |
    |  |  | saniso | D | N | Y |  |  |
    | AutoCI_D_Tensor [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | AutoCI_G_Tensor [G_Tensor] | Y | g_matrix | AD | N | N |  |  |
    |  |  | g_elec | D | N | N | The free electron g-value contribution |  |
    |  |  | g_RMC | D | N | N | The reduced mass correction |  |
    |  |  | g_DSO | AD | N | N |  |  |
    |  |  | g_PSO | AD | N | N |  |  |
    |  |  | g_Tot | AD | N | N |  |  |
    |  |  | g_iso | D | N | N |  |  |
    |  |  | Delta_g | AD | N | N |  |  |
    |  |  | Delta_g_iso | D | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | AutoCI_Spin_Spin_Coupling [Spin_Spin_Coupling] | Y | numOfNucPairs | I | N | N | Number of nuclei pairs to calculate |  |
    |  |  | numOfNucPairsDSO | I | N | N | number of nuclear pairs to calculate DSO |  |
    |  |  | numOfNucPairsPSO | I | N | N | number of nuclear pairs to calculate PSO |  |
    |  |  | numOfNucPairsFC | I | N | N | number of nuclear pairs to calculate FC |  |
    |  |  | numOfNucPairsSD | I | N | N | number of nuclear pairs to calculate SD |  |
    |  |  | numOfNucPairsSD_FC | I | N | N | number of nuclear pairs to calculate SD/FC |  |
    |  |  | pairsInfo | AI | N | N | Pairs Info: Col1->Index of A. Col2->Atom. Num. of A. Col3->Index of B. Col4->Atom. Num. of B. |  |
    |  |  | pairsDistances | AD | N | N | The distances of each pair |  |
    |  |  | pairsTotalSSCIso | AD | N | N | The Spin-Spin coupling constant for each pair |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | AutoCI_Absorption_Spectrum [Absorption_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | AutoCI_ECD_Spectrum [ECD_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | AutoCI_MRCI_Absorption_Spectrum [Absorption_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | AutoCI_MRCI_ECD_Spectrum [ECD_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | CAS_DCD_Energies [Energy] | Y | finalEnergy | D | N | N | Final GS or SA energy |  |
    |  |  | numOfElectrons | I | N | N |  |  |
    |  |  | numOfActiveEl | I | N | N | Number of active electrons |  |
    |  |  | numOfActiveOrbs | I | N | N | Number of active orbitals |  |
    |  |  | numOfFCElectrons | I | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | totalEnergy | AD | N | N | Total energy of each state |  |
    |  |  | Mult | AI | Y | N | Multiplicity of each state |  |
    |  |  | Irrep | AI | Y | N | Irreducible representation of each state |  |
    |  |  | RelCorr | S | Y | N | Relativistic correction (SOC and/or SSC) |  |
    |  |  | NBlocks | I | Y | N | Number of multiplicity blocks |  |
    |  |  | NRoots | AI | Y | N | Number of roots in each block |  |
    |  |  | NTotalRoots | I | Y | N | Total number of roots |  |
    |  |  | Block | AI | Y | N | Block index of each state |  |
    |  |  | Root | AI | Y | N | Root index within the block |  |
    |  |  | FollowIRoot | I | Y | N | Index of the followed root |  |
    |  |  | AvgMult | AD | Y | N | Average multiplicity of each SO-/SS-coupled state |  |
    | CAS_MSPT2_Energies [Energy] | Y | finalEnergy | D | N | N | Final GS or SA energy |  |
    |  |  | numOfElectrons | I | N | N |  |  |
    |  |  | numOfActiveEl | I | N | N | Number of active electrons |  |
    |  |  | numOfActiveOrbs | I | N | N | Number of active orbitals |  |
    |  |  | numOfFCElectrons | I | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | totalEnergy | AD | N | N | Total energy of each state |  |
    |  |  | Mult | AI | Y | N | Multiplicity of each state |  |
    |  |  | Irrep | AI | Y | N | Irreducible representation of each state |  |
    |  |  | RelCorr | S | Y | N | Relativistic correction (SOC and/or SSC) |  |
    |  |  | NBlocks | I | Y | N | Number of multiplicity blocks |  |
    |  |  | NRoots | AI | Y | N | Number of roots in each block |  |
    |  |  | NTotalRoots | I | Y | N | Total number of roots |  |
    |  |  | Block | AI | Y | N | Block index of each state |  |
    |  |  | Root | AI | Y | N | Root index within the block |  |
    |  |  | FollowIRoot | I | Y | N | Index of the followed root |  |
    |  |  | AvgMult | AD | Y | N | Average multiplicity of each SO-/SS-coupled state |  |
    | CAS_PT2_Energies [Energy] | Y | finalEnergy | D | N | N | Final GS or SA energy |  |
    |  |  | numOfElectrons | I | N | N |  |  |
    |  |  | numOfActiveEl | I | N | N | Number of active electrons |  |
    |  |  | numOfActiveOrbs | I | N | N | Number of active orbitals |  |
    |  |  | numOfFCElectrons | I | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | totalEnergy | AD | N | N | Total energy of each state |  |
    |  |  | Mult | AI | Y | N | Multiplicity of each state |  |
    |  |  | Irrep | AI | Y | N | Irreducible representation of each state |  |
    |  |  | RelCorr | S | Y | N | Relativistic correction (SOC and/or SSC) |  |
    |  |  | NBlocks | I | Y | N | Number of multiplicity blocks |  |
    |  |  | NRoots | AI | Y | N | Number of roots in each block |  |
    |  |  | NTotalRoots | I | Y | N | Total number of roots |  |
    |  |  | Block | AI | Y | N | Block index of each state |  |
    |  |  | Root | AI | Y | N | Root index within the block |  |
    |  |  | FollowIRoot | I | Y | N | Index of the followed root |  |
    |  |  | AvgMult | AD | Y | N | Average multiplicity of each SO-/SS-coupled state |  |
    | CAS_SCF_Energies [Energy] | Y | finalEnergy | D | N | N | Final GS or SA energy |  |
    |  |  | numOfElectrons | I | N | N |  |  |
    |  |  | numOfActiveEl | I | N | N | Number of active electrons |  |
    |  |  | numOfActiveOrbs | I | N | N | Number of active orbitals |  |
    |  |  | numOfFCElectrons | I | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | totalEnergy | AD | N | N | Total energy of each state |  |
    |  |  | Mult | AI | Y | N | Multiplicity of each state |  |
    |  |  | Irrep | AI | Y | N | Irreducible representation of each state |  |
    |  |  | RelCorr | S | Y | N | Relativistic correction (SOC and/or SSC) |  |
    |  |  | NBlocks | I | Y | N | Number of multiplicity blocks |  |
    |  |  | NRoots | AI | Y | N | Number of roots in each block |  |
    |  |  | NTotalRoots | I | Y | N | Total number of roots |  |
    |  |  | Block | AI | Y | N | Block index of each state |  |
    |  |  | Root | AI | Y | N | Root index within the block |  |
    |  |  | FollowIRoot | I | Y | N | Index of the followed root |  |
    |  |  | AvgMult | AD | Y | N | Average multiplicity of each SO-/SS-coupled state |  |
    | CASSCF_Dipole_Moment [Dipole_Moment] | Y | dipoleMagnitude | D | N | N |  | a.u. |
    |  |  | dipoleElecContrib | AD | N | N | Electronic contribution |  |
    |  |  | dipoleNucContrib | AD | N | N | Nuclear contribution |  |
    |  |  | dipoleTotal | AD | N | N | Total |  |
    |  |  | doAtomicDipole | B | N | N |  |  |
    |  |  | atomicDipole | AD | Y | N | Atomic dipoles (NAtoms * X,Y,Z) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | CASSCF_EFG_Tensor [EFG_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | QFAC | D | N | Y | Prefactor |  |
    |  |  | V | AD | N | Y | Raw tensor |  |
    |  |  | VEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | VIso | D | N | Y |  |  |
    | CASSCF_Polarizability [Polarizability] | Y | isotropicPolar | D | N | N |  |  |
    |  |  | rawCartesian | AD | N | N |  | a.u |
    |  |  | diagonalizedTensor | AD | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | doAtomicPolar | B | N | N |  |  |
    |  |  | atomicPolarIso | AD | Y | N | Atomic istotropic polarizabilities |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | CASSCF_Quadrupole_Moment [Quadrupole_Moment] | Y | isotropicQuadMoment | D | N | N |  | a.u. |
    |  |  | quadElecContrib | AD | N | N | Electronic contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadNucContrib | AD | N | N | Nuclear contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadTotal | AD | N | N | Total. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadDiagonalized | AD | N | N | The diagonalized tensor | a.u. |
    |  |  | doAtomicQuad | B | N | N |  |  |
    |  |  | atomicQuad | AD | Y | N | Atomic quadrupoles (NAtoms * XX, YY, ZZ, XY, XZ, YZ) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | CASSCF_A_Tensor [A_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elem | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | PFAC | D | N | Y | Prefactor PFAC=gegNbe*bN (in MHz) |  |
    |  |  | ARaw | AD | N | Y | Raw tensor |  |
    |  |  | AEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | AIso | D | N | Y |  |  |
    | CASSCF_Chemical_Shift [Chemical_Shift] | Y | numOfNucs | I | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | SDSO | AD | N | Y | Diamagnetic contribution |  |
    |  |  | SPSO | AD | N | Y | Paramagnetic contribution |  |
    |  |  | STot | AD | N | Y | Total tensor |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | sTotEigen | AD | N | Y | Eigenvalues |  |
    |  |  | siso | D | N | Y |  |  |
    |  |  | saniso | D | N | Y |  |  |
    | CASSCF_D_Tensor [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | CASSCF_G_Tensor [G_Tensor] | Y | g_matrix | AD | N | N |  |  |
    |  |  | g_elec | D | N | N | The free electron g-value contribution |  |
    |  |  | g_RMC | D | N | N | The reduced mass correction |  |
    |  |  | g_DSO | AD | N | N |  |  |
    |  |  | g_PSO | AD | N | N |  |  |
    |  |  | g_Tot | AD | N | N |  |  |
    |  |  | g_iso | D | N | N |  |  |
    |  |  | Delta_g | AD | N | N |  |  |
    |  |  | Delta_g_iso | D | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | CASSCF_Spin_Spin_Coupling [Spin_Spin_Coupling] | Y | numOfNucPairs | I | N | N | Number of nuclei pairs to calculate |  |
    |  |  | numOfNucPairsDSO | I | N | N | number of nuclear pairs to calculate DSO |  |
    |  |  | numOfNucPairsPSO | I | N | N | number of nuclear pairs to calculate PSO |  |
    |  |  | numOfNucPairsFC | I | N | N | number of nuclear pairs to calculate FC |  |
    |  |  | numOfNucPairsSD | I | N | N | number of nuclear pairs to calculate SD |  |
    |  |  | numOfNucPairsSD_FC | I | N | N | number of nuclear pairs to calculate SD/FC |  |
    |  |  | pairsInfo | AI | N | N | Pairs Info: Col1->Index of A. Col2->Atom. Num. of A. Col3->Index of B. Col4->Atom. Num. of B. |  |
    |  |  | pairsDistances | AD | N | N | The distances of each pair |  |
    |  |  | pairsTotalSSCIso | AD | N | N | The Spin-Spin coupling constant for each pair |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | D_Tensor_CASSCF_2ndOrder [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | D_Tensor_CASSCF_2ndOrder_ES [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | D_Tensor_CASSCF_Heff [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | D_Tensor_CASSCF_Heff_ES [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | D_Tensor_NEVPT2_2ndOrder [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | D_Tensor_NEVPT2_2ndOrder_ES [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | D_Tensor_NEVPT2_Heff [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | D_Tensor_NEVPT2_Heff_ES [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | D_Tensor_CUSTOM_2ndOrder [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | D_Tensor_CUSTOM_2ndOrder_ES [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | D_Tensor_CUSTOM_Heff [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | D_Tensor_CUSTOM_Heff_ES [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | G_Tensor_CASSCF_2ndOrder [G_Tensor] | Y | g_matrix | AD | N | N |  |  |
    |  |  | g_elec | D | N | N | The free electron g-value contribution |  |
    |  |  | g_RMC | D | N | N | The reduced mass correction |  |
    |  |  | g_DSO | AD | N | N |  |  |
    |  |  | g_PSO | AD | N | N |  |  |
    |  |  | g_Tot | AD | N | N |  |  |
    |  |  | g_iso | D | N | N |  |  |
    |  |  | Delta_g | AD | N | N |  |  |
    |  |  | Delta_g_iso | D | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | G_Tensor_CASSCF_Heff [G_Tensor] | Y | g_matrix | AD | N | N |  |  |
    |  |  | g_elec | D | N | N | The free electron g-value contribution |  |
    |  |  | g_RMC | D | N | N | The reduced mass correction |  |
    |  |  | g_DSO | AD | N | N |  |  |
    |  |  | g_PSO | AD | N | N |  |  |
    |  |  | g_Tot | AD | N | N |  |  |
    |  |  | g_iso | D | N | N |  |  |
    |  |  | Delta_g | AD | N | N |  |  |
    |  |  | Delta_g_iso | D | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | G_Tensor_NEVPT2_2ndOrder [G_Tensor] | Y | g_matrix | AD | N | N |  |  |
    |  |  | g_elec | D | N | N | The free electron g-value contribution |  |
    |  |  | g_RMC | D | N | N | The reduced mass correction |  |
    |  |  | g_DSO | AD | N | N |  |  |
    |  |  | g_PSO | AD | N | N |  |  |
    |  |  | g_Tot | AD | N | N |  |  |
    |  |  | g_iso | D | N | N |  |  |
    |  |  | Delta_g | AD | N | N |  |  |
    |  |  | Delta_g_iso | D | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | G_Tensor_NEVPT2_Heff [G_Tensor] | Y | g_matrix | AD | N | N |  |  |
    |  |  | g_elec | D | N | N | The free electron g-value contribution |  |
    |  |  | g_RMC | D | N | N | The reduced mass correction |  |
    |  |  | g_DSO | AD | N | N |  |  |
    |  |  | g_PSO | AD | N | N |  |  |
    |  |  | g_Tot | AD | N | N |  |  |
    |  |  | g_iso | D | N | N |  |  |
    |  |  | Delta_g | AD | N | N |  |  |
    |  |  | Delta_g_iso | D | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | G_Tensor_CUSTOM_2ndOrder [G_Tensor] | Y | g_matrix | AD | N | N |  |  |
    |  |  | g_elec | D | N | N | The free electron g-value contribution |  |
    |  |  | g_RMC | D | N | N | The reduced mass correction |  |
    |  |  | g_DSO | AD | N | N |  |  |
    |  |  | g_PSO | AD | N | N |  |  |
    |  |  | g_Tot | AD | N | N |  |  |
    |  |  | g_iso | D | N | N |  |  |
    |  |  | Delta_g | AD | N | N |  |  |
    |  |  | Delta_g_iso | D | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | G_Tensor_CUSTOM_Heff [G_Tensor] | Y | g_matrix | AD | N | N |  |  |
    |  |  | g_elec | D | N | N | The free electron g-value contribution |  |
    |  |  | g_RMC | D | N | N | The reduced mass correction |  |
    |  |  | g_DSO | AD | N | N |  |  |
    |  |  | g_PSO | AD | N | N |  |  |
    |  |  | g_Tot | AD | N | N |  |  |
    |  |  | g_iso | D | N | N |  |  |
    |  |  | Delta_g | AD | N | N |  |  |
    |  |  | Delta_g_iso | D | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | CASSCF_Absorption_Spectrum [Absorption_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | CASSCF_PT_Absorption_Spectrum [Absorption_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | CASSCF_QDPT_Absorption_Spectrum [Absorption_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | CASSCF_DCD_Absorption_Spectrum [Absorption_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | CASSCF_PT_Energies_Absorption_Spectrum [Absorption_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | CASSCF_Custom_Absorption_Spectrum [Absorption_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | CASSCF_ECD_Spectrum [ECD_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | CASSCF_PT_ECD_Spectrum [ECD_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | CASSCF_QDPT_ECD_Spectrum [ECD_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | CASSCF_DCD_ECD_Spectrum [ECD_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | CASSCF_PT_ECD_Spectrum [ECD_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | CASSCF_Custom_ECD_Spectrum [ECD_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | CIPSI_Energies | N | finalEnergy | D | N | N |  |  |
    |  |  | numOfRoots | I | N | N |  |  |
    |  |  | multiplicity | I | N | N |  |  |
    |  |  | energies | AD | N | N |  |  |
    | CIS_Energies [Energy] | Y | e0 | D | N | N | Ground state energy |  |
    |  |  | multP1 | B | N | N | Do the higher multiplicity too? |  |
    |  |  | mode | S | N | N | CIS mode: CIS, RPA, TDA, TD-DFT, sTDA, sTD-DFT |  |
    |  |  | dCorr | I | N | N | (D) Correction algorithm |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | totalEnergy | AD | N | N | Total energy of each state |  |
    |  |  | Mult | AI | Y | N | Multiplicity of each state |  |
    |  |  | Irrep | AI | Y | N | Irreducible representation of each state |  |
    |  |  | RelCorr | S | Y | N | Relativistic correction (SOC and/or SSC) |  |
    |  |  | NBlocks | I | Y | N | Number of multiplicity blocks |  |
    |  |  | NRoots | AI | Y | N | Number of roots in each block |  |
    |  |  | NTotalRoots | I | Y | N | Total number of roots |  |
    |  |  | Block | AI | Y | N | Block index of each state |  |
    |  |  | Root | AI | Y | N | Root index within the block |  |
    |  |  | FollowIRoot | I | Y | N | Index of the followed root |  |
    |  |  | AvgMult | AD | Y | N | Average multiplicity of each SO-/SS-coupled state |  |
    | CIS_Nuc_Gradient [Nuclear_Gradient] | Y | NAtoms | I | N | N |  |  |
    |  |  | gradNorm | D | N | N |  |  |
    |  |  | grad | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | CIS_Dipole_Moment [Dipole_Moment] | Y | dipoleMagnitude | D | N | N |  | a.u. |
    |  |  | dipoleElecContrib | AD | N | N | Electronic contribution |  |
    |  |  | dipoleNucContrib | AD | N | N | Nuclear contribution |  |
    |  |  | dipoleTotal | AD | N | N | Total |  |
    |  |  | doAtomicDipole | B | N | N |  |  |
    |  |  | atomicDipole | AD | Y | N | Atomic dipoles (NAtoms * X,Y,Z) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | CIS_EFG_Tensor [EFG_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | QFAC | D | N | Y | Prefactor |  |
    |  |  | V | AD | N | Y | Raw tensor |  |
    |  |  | VEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | VIso | D | N | Y |  |  |
    | CIS_Polarizability [Polarizability] | Y | isotropicPolar | D | N | N |  |  |
    |  |  | rawCartesian | AD | N | N |  | a.u |
    |  |  | diagonalizedTensor | AD | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | doAtomicPolar | B | N | N |  |  |
    |  |  | atomicPolarIso | AD | Y | N | Atomic istotropic polarizabilities |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | CIS_Quadrupole_Moment [Quadrupole_Moment] | Y | isotropicQuadMoment | D | N | N |  | a.u. |
    |  |  | quadElecContrib | AD | N | N | Electronic contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadNucContrib | AD | N | N | Nuclear contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadTotal | AD | N | N | Total. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadDiagonalized | AD | N | N | The diagonalized tensor | a.u. |
    |  |  | doAtomicQuad | B | N | N |  |  |
    |  |  | atomicQuad | AD | Y | N | Atomic quadrupoles (NAtoms * XX, YY, ZZ, XY, XZ, YZ) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | CIS_A_Tensor [A_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elem | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | PFAC | D | N | Y | Prefactor PFAC=gegNbe*bN (in MHz) |  |
    |  |  | ARaw | AD | N | Y | Raw tensor |  |
    |  |  | AEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | AIso | D | N | Y |  |  |
    | CIS_Chemical_Shift [Chemical_Shift] | Y | numOfNucs | I | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | SDSO | AD | N | Y | Diamagnetic contribution |  |
    |  |  | SPSO | AD | N | Y | Paramagnetic contribution |  |
    |  |  | STot | AD | N | Y | Total tensor |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | sTotEigen | AD | N | Y | Eigenvalues |  |
    |  |  | siso | D | N | Y |  |  |
    |  |  | saniso | D | N | Y |  |  |
    | CIS_D_Tensor [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | CIS_G_Tensor [G_Tensor] | Y | g_matrix | AD | N | N |  |  |
    |  |  | g_elec | D | N | N | The free electron g-value contribution |  |
    |  |  | g_RMC | D | N | N | The reduced mass correction |  |
    |  |  | g_DSO | AD | N | N |  |  |
    |  |  | g_PSO | AD | N | N |  |  |
    |  |  | g_Tot | AD | N | N |  |  |
    |  |  | g_iso | D | N | N |  |  |
    |  |  | Delta_g | AD | N | N |  |  |
    |  |  | Delta_g_iso | D | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | CIS_Spin_Spin_Coupling [Spin_Spin_Coupling] | Y | numOfNucPairs | I | N | N | Number of nuclei pairs to calculate |  |
    |  |  | numOfNucPairsDSO | I | N | N | number of nuclear pairs to calculate DSO |  |
    |  |  | numOfNucPairsPSO | I | N | N | number of nuclear pairs to calculate PSO |  |
    |  |  | numOfNucPairsFC | I | N | N | number of nuclear pairs to calculate FC |  |
    |  |  | numOfNucPairsSD | I | N | N | number of nuclear pairs to calculate SD |  |
    |  |  | numOfNucPairsSD_FC | I | N | N | number of nuclear pairs to calculate SD/FC |  |
    |  |  | pairsInfo | AI | N | N | Pairs Info: Col1->Index of A. Col2->Atom. Num. of A. Col3->Index of B. Col4->Atom. Num. of B. |  |
    |  |  | pairsDistances | AD | N | N | The distances of each pair |  |
    |  |  | pairsTotalSSCIso | AD | N | N | The Spin-Spin coupling constant for each pair |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | CIS_Absorption_Spectrum [Absorption_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | CIS_ECD_Spectrum [ECD_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | DBOC_Energy | N | DBOC_Energy | D | N | N |  |  |
    | DFT_Energy | N | nAlphaEl | I | N | N |  |  |
    |  |  | nBetaEl | I | N | N |  |  |
    |  |  | nTotalEl | I | N | N |  |  |
    |  |  | finalEn | D | N | N | No Van der Waals correction |  |
    |  |  | eExchange | D | N | N |  |  |
    |  |  | eCorr | D | N | N |  |  |
    |  |  | eXC | D | N | N |  |  |
    |  |  | eCNL | D | N | N |  |  |
    |  |  | eEmbed | D | Y | N |  |  |
    | BROKEN_SYMMETRY | N | enHighSpin | D | N | N | The High Spin Energy |  |
    |  |  | enBrokenSym | D | N | N | The Broken Symmetry Energy |  |
    |  |  | SHighSpin | D | N | N | The High Spin Spin |  |
    |  |  | S2HighSpin | D | N | N | The Expectation value of S**2 for the High Spin case |  |
    |  |  | S2BrokenSym | D | N | N | The Expectation value of S**2 for the Broken symmetry case |  |
    | Dipole_Moment | Y | dipoleMagnitude | D | N | N |  | a.u. |
    |  |  | dipoleElecContrib | AD | N | N | Electronic contribution |  |
    |  |  | dipoleNucContrib | AD | N | N | Nuclear contribution |  |
    |  |  | dipoleTotal | AD | N | N | Total |  |
    |  |  | doAtomicDipole | B | N | N |  |  |
    |  |  | atomicDipole | AD | Y | N | Atomic dipoles (NAtoms * X,Y,Z) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | EFG_Tensor | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | QFAC | D | N | Y | Prefactor |  |
    |  |  | V | AD | N | Y | Raw tensor |  |
    |  |  | VEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | VIso | D | N | Y |  |  |
    | Quadrupole_Moment | Y | isotropicQuadMoment | D | N | N |  | a.u. |
    |  |  | quadElecContrib | AD | N | N | Electronic contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadNucContrib | AD | N | N | Nuclear contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadTotal | AD | N | N | Total. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadDiagonalized | AD | N | N | The diagonalized tensor | a.u. |
    |  |  | doAtomicQuad | B | N | N |  |  |
    |  |  | atomicQuad | AD | Y | N | Atomic quadrupoles (NAtoms * XX, YY, ZZ, XY, XZ, YZ) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | Polarizability | Y | isotropicPolar | D | N | N |  |  |
    |  |  | rawCartesian | AD | N | N |  | a.u |
    |  |  | diagonalizedTensor | AD | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | doAtomicPolar | B | N | N |  |  |
    |  |  | atomicPolarIso | AD | Y | N | Atomic istotropic polarizabilities |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | Hyperpolarizability | Y | rawCartesian | AD | N | N |  | a.u |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | Excited_States_Dynamics | N | fluorRateConstant | D | N | N |  |  |
    | Energy_Extrapolation | N | doEp1 | B | N | N | Extrapolation using only one method |  |
    |  |  | doEp2 | B | N | N | Extrapolation using two different methods (same small basis Set) |  |
    |  |  | doEp3 | B | N | N | Extrapolation using two different methods (use three basis Sets for the cheap method) |  |
    |  |  | doGradients | B | N | N | Extrapolate energy gradients |  |
    |  |  | scfEnergies | AD | N | N |  |  |
    |  |  | scfCBS | D | N | N |  |  |
    |  |  | scfGradients | AD | Y | N | The SCF Gradients |  |
    |  |  | corrEnergies | AD | N | N |  |  |
    |  |  | corrCBS | D | N | N |  |  |
    |  |  | ccsdtEnergyX | D | Y | N |  |  |
    |  |  | totalCBS | D | N | N |  |  |
    |  |  | cardinalNumbers | AI | N | N |  |  |
    |  |  | alphas | AD | N | N |  |  |
    |  |  | betas | AD | N | N |  |  |
    |  |  | numOfEnergies | I | N | N | How many energies we are going to use (e.g. two-point scheme). |  |
    |  |  | basisName | S | N | Y |  |  |
    | gCP_Energy | N | gCP_Energy | D | N | N |  |  |
    | Hessian | N | HESSIAN | AD | N | N | The Hessian |  |
    |  |  | MODES | AD | N | N | The modes of vibrations |  |
    | ICE_Dipole_Moment [Dipole_Moment] | Y | dipoleMagnitude | D | N | N |  | a.u. |
    |  |  | dipoleElecContrib | AD | N | N | Electronic contribution |  |
    |  |  | dipoleNucContrib | AD | N | N | Nuclear contribution |  |
    |  |  | dipoleTotal | AD | N | N | Total |  |
    |  |  | doAtomicDipole | B | N | N |  |  |
    |  |  | atomicDipole | AD | Y | N | Atomic dipoles (NAtoms * X,Y,Z) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | ICE_EFG_Tensor [EFG_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | QFAC | D | N | Y | Prefactor |  |
    |  |  | V | AD | N | Y | Raw tensor |  |
    |  |  | VEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | VIso | D | N | Y |  |  |
    | ICE_Polarizability [Polarizability] | Y | isotropicPolar | D | N | N |  |  |
    |  |  | rawCartesian | AD | N | N |  | a.u |
    |  |  | diagonalizedTensor | AD | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | doAtomicPolar | B | N | N |  |  |
    |  |  | atomicPolarIso | AD | Y | N | Atomic istotropic polarizabilities |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | ICE_Quadrupole_Moment [Quadrupole_Moment] | Y | isotropicQuadMoment | D | N | N |  | a.u. |
    |  |  | quadElecContrib | AD | N | N | Electronic contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadNucContrib | AD | N | N | Nuclear contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadTotal | AD | N | N | Total. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadDiagonalized | AD | N | N | The diagonalized tensor | a.u. |
    |  |  | doAtomicQuad | B | N | N |  |  |
    |  |  | atomicQuad | AD | Y | N | Atomic quadrupoles (NAtoms * XX, YY, ZZ, XY, XZ, YZ) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | ICE_A_Tensor [A_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elem | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | PFAC | D | N | Y | Prefactor PFAC=gegNbe*bN (in MHz) |  |
    |  |  | ARaw | AD | N | Y | Raw tensor |  |
    |  |  | AEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | AIso | D | N | Y |  |  |
    | ICE_Chemical_Shift [Chemical_Shift] | Y | numOfNucs | I | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | SDSO | AD | N | Y | Diamagnetic contribution |  |
    |  |  | SPSO | AD | N | Y | Paramagnetic contribution |  |
    |  |  | STot | AD | N | Y | Total tensor |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | sTotEigen | AD | N | Y | Eigenvalues |  |
    |  |  | siso | D | N | Y |  |  |
    |  |  | saniso | D | N | Y |  |  |
    | ICE_D_Tensor [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | ICE_G_Tensor [G_Tensor] | Y | g_matrix | AD | N | N |  |  |
    |  |  | g_elec | D | N | N | The free electron g-value contribution |  |
    |  |  | g_RMC | D | N | N | The reduced mass correction |  |
    |  |  | g_DSO | AD | N | N |  |  |
    |  |  | g_PSO | AD | N | N |  |  |
    |  |  | g_Tot | AD | N | N |  |  |
    |  |  | g_iso | D | N | N |  |  |
    |  |  | Delta_g | AD | N | N |  |  |
    |  |  | Delta_g_iso | D | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | ICE_Spin_Spin_Coupling [Spin_Spin_Coupling] | Y | numOfNucPairs | I | N | N | Number of nuclei pairs to calculate |  |
    |  |  | numOfNucPairsDSO | I | N | N | number of nuclear pairs to calculate DSO |  |
    |  |  | numOfNucPairsPSO | I | N | N | number of nuclear pairs to calculate PSO |  |
    |  |  | numOfNucPairsFC | I | N | N | number of nuclear pairs to calculate FC |  |
    |  |  | numOfNucPairsSD | I | N | N | number of nuclear pairs to calculate SD |  |
    |  |  | numOfNucPairsSD_FC | I | N | N | number of nuclear pairs to calculate SD/FC |  |
    |  |  | pairsInfo | AI | N | N | Pairs Info: Col1->Index of A. Col2->Atom. Num. of A. Col3->Index of B. Col4->Atom. Num. of B. |  |
    |  |  | pairsDistances | AD | N | N | The distances of each pair |  |
    |  |  | pairsTotalSSCIso | AD | N | N | The Spin-Spin coupling constant for each pair |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | ICE_Absorption_Spectrum [Absorption_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | ICE_ECD_Spectrum [ECD_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | Calculation_Info | N | Mult | I | N | N |  |  |
    |  |  | Charge | I | N | N |  |  |
    |  |  | NumOfAtoms | I | N | N |  |  |
    |  |  | NumOfElectrons | I | N | N |  |  |
    |  |  | NumOfBasisFuncts | I | N | N |  |  |
    |  |  | NumOfAuxCBasisFuncts | I | N | N |  |  |
    |  |  | NumOfAuxJBasisFuncts | I | N | N |  |  |
    |  |  | NumOfAuxJKBasisFuncts | I | N | N |  |  |
    |  |  | NumOfCABSBasisFuncts | I | N | N |  |  |
    | Single_Point_Data | N | FinalEnergy | D | N | N | Final single point energy |  |
    |  |  | Converged | B | N | N |  |  |
    | LFT_Absorption_Spectrum [Absorption_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | LFT_ECD_Spectrum [ECD_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | A_Tensor | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elem | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | PFAC | D | N | Y | Prefactor PFAC=gegNbe*bN (in MHz) |  |
    |  |  | ARaw | AD | N | Y | Raw tensor |  |
    |  |  | AEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | AIso | D | N | Y |  |  |
    | Chemical_Shift | Y | numOfNucs | I | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | SDSO | AD | N | Y | Diamagnetic contribution |  |
    |  |  | SPSO | AD | N | Y | Paramagnetic contribution |  |
    |  |  | STot | AD | N | Y | Total tensor |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | sTotEigen | AD | N | Y | Eigenvalues |  |
    |  |  | siso | D | N | Y |  |  |
    |  |  | saniso | D | N | Y |  |  |
    | D_Tensor | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | G_Tensor | Y | g_matrix | AD | N | N |  |  |
    |  |  | g_elec | D | N | N | The free electron g-value contribution |  |
    |  |  | g_RMC | D | N | N | The reduced mass correction |  |
    |  |  | g_DSO | AD | N | N |  |  |
    |  |  | g_PSO | AD | N | N |  |  |
    |  |  | g_Tot | AD | N | N |  |  |
    |  |  | g_iso | D | N | N |  |  |
    |  |  | Delta_g | AD | N | N |  |  |
    |  |  | Delta_g_iso | D | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | Spin_Spin_Coupling | Y | numOfNucPairs | I | N | N | Number of nuclei pairs to calculate |  |
    |  |  | numOfNucPairsDSO | I | N | N | number of nuclear pairs to calculate DSO |  |
    |  |  | numOfNucPairsPSO | I | N | N | number of nuclear pairs to calculate PSO |  |
    |  |  | numOfNucPairsFC | I | N | N | number of nuclear pairs to calculate FC |  |
    |  |  | numOfNucPairsSD | I | N | N | number of nuclear pairs to calculate SD |  |
    |  |  | numOfNucPairsSD_FC | I | N | N | number of nuclear pairs to calculate SD/FC |  |
    |  |  | pairsInfo | AI | N | N | Pairs Info: Col1->Index of A. Col2->Atom. Num. of A. Col3->Index of B. Col4->Atom. Num. of B. |  |
    |  |  | pairsDistances | AD | N | N | The distances of each pair |  |
    |  |  | pairsTotalSSCIso | AD | N | N | The Spin-Spin coupling constant for each pair |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MCRPA_Dipole_Moment [Dipole_Moment] | Y | dipoleMagnitude | D | N | N |  | a.u. |
    |  |  | dipoleElecContrib | AD | N | N | Electronic contribution |  |
    |  |  | dipoleNucContrib | AD | N | N | Nuclear contribution |  |
    |  |  | dipoleTotal | AD | N | N | Total |  |
    |  |  | doAtomicDipole | B | N | N |  |  |
    |  |  | atomicDipole | AD | Y | N | Atomic dipoles (NAtoms * X,Y,Z) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MCRPA_EFG_Tensor [EFG_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | QFAC | D | N | Y | Prefactor |  |
    |  |  | V | AD | N | Y | Raw tensor |  |
    |  |  | VEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | VIso | D | N | Y |  |  |
    | MCRPA_Polarizability [Polarizability] | Y | isotropicPolar | D | N | N |  |  |
    |  |  | rawCartesian | AD | N | N |  | a.u |
    |  |  | diagonalizedTensor | AD | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | doAtomicPolar | B | N | N |  |  |
    |  |  | atomicPolarIso | AD | Y | N | Atomic istotropic polarizabilities |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MCRPA_Quadrupole_Moment [Quadrupole_Moment] | Y | isotropicQuadMoment | D | N | N |  | a.u. |
    |  |  | quadElecContrib | AD | N | N | Electronic contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadNucContrib | AD | N | N | Nuclear contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadTotal | AD | N | N | Total. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadDiagonalized | AD | N | N | The diagonalized tensor | a.u. |
    |  |  | doAtomicQuad | B | N | N |  |  |
    |  |  | atomicQuad | AD | Y | N | Atomic quadrupoles (NAtoms * XX, YY, ZZ, XY, XZ, YZ) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MCRPA_A_Tensor [A_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elem | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | PFAC | D | N | Y | Prefactor PFAC=gegNbe*bN (in MHz) |  |
    |  |  | ARaw | AD | N | Y | Raw tensor |  |
    |  |  | AEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | AIso | D | N | Y |  |  |
    | MCRPA_Chemical_Shift [Chemical_Shift] | Y | numOfNucs | I | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | SDSO | AD | N | Y | Diamagnetic contribution |  |
    |  |  | SPSO | AD | N | Y | Paramagnetic contribution |  |
    |  |  | STot | AD | N | Y | Total tensor |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | sTotEigen | AD | N | Y | Eigenvalues |  |
    |  |  | siso | D | N | Y |  |  |
    |  |  | saniso | D | N | Y |  |  |
    | MCRPA_D_Tensor [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MCRPA_G_Tensor [G_Tensor] | Y | g_matrix | AD | N | N |  |  |
    |  |  | g_elec | D | N | N | The free electron g-value contribution |  |
    |  |  | g_RMC | D | N | N | The reduced mass correction |  |
    |  |  | g_DSO | AD | N | N |  |  |
    |  |  | g_PSO | AD | N | N |  |  |
    |  |  | g_Tot | AD | N | N |  |  |
    |  |  | g_iso | D | N | N |  |  |
    |  |  | Delta_g | AD | N | N |  |  |
    |  |  | Delta_g_iso | D | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MCRPA_Spin_Spin_Coupling [Spin_Spin_Coupling] | Y | numOfNucPairs | I | N | N | Number of nuclei pairs to calculate |  |
    |  |  | numOfNucPairsDSO | I | N | N | number of nuclear pairs to calculate DSO |  |
    |  |  | numOfNucPairsPSO | I | N | N | number of nuclear pairs to calculate PSO |  |
    |  |  | numOfNucPairsFC | I | N | N | number of nuclear pairs to calculate FC |  |
    |  |  | numOfNucPairsSD | I | N | N | number of nuclear pairs to calculate SD |  |
    |  |  | numOfNucPairsSD_FC | I | N | N | number of nuclear pairs to calculate SD/FC |  |
    |  |  | pairsInfo | AI | N | N | Pairs Info: Col1->Index of A. Col2->Atom. Num. of A. Col3->Index of B. Col4->Atom. Num. of B. |  |
    |  |  | pairsDistances | AD | N | N | The distances of each pair |  |
    |  |  | pairsTotalSSCIso | AD | N | N | The Spin-Spin coupling constant for each pair |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MCRPA_Absorption_Spectrum [Absorption_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | MCRPA_ECD_Spectrum [ECD_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | MDCI_Energies [Energy] | Y | numOfEl | I | N | N |  |  |
    |  |  | numOfCorrEl | I | N | N |  |  |
    |  |  | numOfAlphaCorrEl | I | N | N |  |  |
    |  |  | numOfBetaCorrEl | I | N | N |  |  |
    |  |  | refEnergy | AD | N | N | Reference Energy |  |
    |  |  | corrEnergy | AD | N | N | Total Correlation Energy |  |
    |  |  | aaCorrEn | AD | N | N | Alpha-Alpha Pairs Correlation Energy (No (T)) |  |
    |  |  | bbCorrEn | AD | N | N | Beta-Beta Pairs Correlation Energy (No (T)) |  |
    |  |  | abCorrEn | AD | N | N | Alpha-Beta Pairs Correlation Energy (No (T)) |  |
    |  |  | CorrDS | AD | Y | N | Singlet pairs energy of double amplitudes (No (T)) |  |
    |  |  | CorrDT | AD | Y | N | Triplet pairs energy of double amplitudes (No (T)) |  |
    |  |  | CorrSS | AD | Y | N | Singlet pairs energy of quadratic single amplitudes (No (T)) |  |
    |  |  | CorrST | AD | Y | N | Triplet pairs energy of quadratic single amplitudes (No (T)) |  |
    |  |  | triplesEnergy | AD | N | N | Triples Correction Energy |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | totalEnergy | AD | N | N | Total energy of each state |  |
    |  |  | Mult | AI | Y | N | Multiplicity of each state |  |
    |  |  | Irrep | AI | Y | N | Irreducible representation of each state |  |
    |  |  | RelCorr | S | Y | N | Relativistic correction (SOC and/or SSC) |  |
    |  |  | NBlocks | I | Y | N | Number of multiplicity blocks |  |
    |  |  | NRoots | AI | Y | N | Number of roots in each block |  |
    |  |  | NTotalRoots | I | Y | N | Total number of roots |  |
    |  |  | Block | AI | Y | N | Block index of each state |  |
    |  |  | Root | AI | Y | N | Root index within the block |  |
    |  |  | FollowIRoot | I | Y | N | Index of the followed root |  |
    |  |  | AvgMult | AD | Y | N | Average multiplicity of each SO-/SS-coupled state |  |
    | MDCI_Nuc_Gradient [Nuclear_Gradient] | Y | NAtoms | I | N | N |  |  |
    |  |  | gradNorm | D | N | N |  |  |
    |  |  | grad | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MDCI_Dipole_Moment [Dipole_Moment] | Y | dipoleMagnitude | D | N | N |  | a.u. |
    |  |  | dipoleElecContrib | AD | N | N | Electronic contribution |  |
    |  |  | dipoleNucContrib | AD | N | N | Nuclear contribution |  |
    |  |  | dipoleTotal | AD | N | N | Total |  |
    |  |  | doAtomicDipole | B | N | N |  |  |
    |  |  | atomicDipole | AD | Y | N | Atomic dipoles (NAtoms * X,Y,Z) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MDCI_EFG_Tensor [EFG_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | QFAC | D | N | Y | Prefactor |  |
    |  |  | V | AD | N | Y | Raw tensor |  |
    |  |  | VEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | VIso | D | N | Y |  |  |
    | MDCI_Polarizability [Polarizability] | Y | isotropicPolar | D | N | N |  |  |
    |  |  | rawCartesian | AD | N | N |  | a.u |
    |  |  | diagonalizedTensor | AD | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | doAtomicPolar | B | N | N |  |  |
    |  |  | atomicPolarIso | AD | Y | N | Atomic istotropic polarizabilities |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MDCI_Quadrupole_Moment [Quadrupole_Moment] | Y | isotropicQuadMoment | D | N | N |  | a.u. |
    |  |  | quadElecContrib | AD | N | N | Electronic contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadNucContrib | AD | N | N | Nuclear contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadTotal | AD | N | N | Total. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadDiagonalized | AD | N | N | The diagonalized tensor | a.u. |
    |  |  | doAtomicQuad | B | N | N |  |  |
    |  |  | atomicQuad | AD | Y | N | Atomic quadrupoles (NAtoms * XX, YY, ZZ, XY, XZ, YZ) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MDCI_A_Tensor [A_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elem | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | PFAC | D | N | Y | Prefactor PFAC=gegNbe*bN (in MHz) |  |
    |  |  | ARaw | AD | N | Y | Raw tensor |  |
    |  |  | AEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | AIso | D | N | Y |  |  |
    | MDCI_Chemical_Shift [Chemical_Shift] | Y | numOfNucs | I | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | SDSO | AD | N | Y | Diamagnetic contribution |  |
    |  |  | SPSO | AD | N | Y | Paramagnetic contribution |  |
    |  |  | STot | AD | N | Y | Total tensor |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | sTotEigen | AD | N | Y | Eigenvalues |  |
    |  |  | siso | D | N | Y |  |  |
    |  |  | saniso | D | N | Y |  |  |
    | MDCI_D_Tensor [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MDCI_G_Tensor [G_Tensor] | Y | g_matrix | AD | N | N |  |  |
    |  |  | g_elec | D | N | N | The free electron g-value contribution |  |
    |  |  | g_RMC | D | N | N | The reduced mass correction |  |
    |  |  | g_DSO | AD | N | N |  |  |
    |  |  | g_PSO | AD | N | N |  |  |
    |  |  | g_Tot | AD | N | N |  |  |
    |  |  | g_iso | D | N | N |  |  |
    |  |  | Delta_g | AD | N | N |  |  |
    |  |  | Delta_g_iso | D | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MDCI_Spin_Spin_Coupling [Spin_Spin_Coupling] | Y | numOfNucPairs | I | N | N | Number of nuclei pairs to calculate |  |
    |  |  | numOfNucPairsDSO | I | N | N | number of nuclear pairs to calculate DSO |  |
    |  |  | numOfNucPairsPSO | I | N | N | number of nuclear pairs to calculate PSO |  |
    |  |  | numOfNucPairsFC | I | N | N | number of nuclear pairs to calculate FC |  |
    |  |  | numOfNucPairsSD | I | N | N | number of nuclear pairs to calculate SD |  |
    |  |  | numOfNucPairsSD_FC | I | N | N | number of nuclear pairs to calculate SD/FC |  |
    |  |  | pairsInfo | AI | N | N | Pairs Info: Col1->Index of A. Col2->Atom. Num. of A. Col3->Index of B. Col4->Atom. Num. of B. |  |
    |  |  | pairsDistances | AD | N | N | The distances of each pair |  |
    |  |  | pairsTotalSSCIso | AD | N | N | The Spin-Spin coupling constant for each pair |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MDCI_Absorption_Spectrum [Absorption_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | MDCI_ECD_Spectrum [ECD_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | MP2_Energies [Energy] | Y | refEnergy | AD | N | N | Reference energy for each state |  |
    |  |  | corrEnergy | AD | N | N | MP2 correlation energy for each state |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | totalEnergy | AD | N | N | Total energy of each state |  |
    |  |  | Mult | AI | Y | N | Multiplicity of each state |  |
    |  |  | Irrep | AI | Y | N | Irreducible representation of each state |  |
    |  |  | RelCorr | S | Y | N | Relativistic correction (SOC and/or SSC) |  |
    |  |  | NBlocks | I | Y | N | Number of multiplicity blocks |  |
    |  |  | NRoots | AI | Y | N | Number of roots in each block |  |
    |  |  | NTotalRoots | I | Y | N | Total number of roots |  |
    |  |  | Block | AI | Y | N | Block index of each state |  |
    |  |  | Root | AI | Y | N | Root index within the block |  |
    |  |  | FollowIRoot | I | Y | N | Index of the followed root |  |
    |  |  | AvgMult | AD | Y | N | Average multiplicity of each SO-/SS-coupled state |  |
    | MP2_Nuc_Gradient [Nuclear_Gradient] | Y | NAtoms | I | N | N |  |  |
    |  |  | gradNorm | D | N | N |  |  |
    |  |  | grad | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MP2_Dipole_Moment [Dipole_Moment] | Y | dipoleMagnitude | D | N | N |  | a.u. |
    |  |  | dipoleElecContrib | AD | N | N | Electronic contribution |  |
    |  |  | dipoleNucContrib | AD | N | N | Nuclear contribution |  |
    |  |  | dipoleTotal | AD | N | N | Total |  |
    |  |  | doAtomicDipole | B | N | N |  |  |
    |  |  | atomicDipole | AD | Y | N | Atomic dipoles (NAtoms * X,Y,Z) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MP2_EFG_Tensor [EFG_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | QFAC | D | N | Y | Prefactor |  |
    |  |  | V | AD | N | Y | Raw tensor |  |
    |  |  | VEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | VIso | D | N | Y |  |  |
    | MP2_Polarizability [Polarizability] | Y | isotropicPolar | D | N | N |  |  |
    |  |  | rawCartesian | AD | N | N |  | a.u |
    |  |  | diagonalizedTensor | AD | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | doAtomicPolar | B | N | N |  |  |
    |  |  | atomicPolarIso | AD | Y | N | Atomic istotropic polarizabilities |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MP2_Quadrupole_Moment [Quadrupole_Moment] | Y | isotropicQuadMoment | D | N | N |  | a.u. |
    |  |  | quadElecContrib | AD | N | N | Electronic contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadNucContrib | AD | N | N | Nuclear contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadTotal | AD | N | N | Total. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadDiagonalized | AD | N | N | The diagonalized tensor | a.u. |
    |  |  | doAtomicQuad | B | N | N |  |  |
    |  |  | atomicQuad | AD | Y | N | Atomic quadrupoles (NAtoms * XX, YY, ZZ, XY, XZ, YZ) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MP2_A_Tensor [A_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elem | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | PFAC | D | N | Y | Prefactor PFAC=gegNbe*bN (in MHz) |  |
    |  |  | ARaw | AD | N | Y | Raw tensor |  |
    |  |  | AEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | AIso | D | N | Y |  |  |
    | MP2_Chemical_Shift [Chemical_Shift] | Y | numOfNucs | I | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | SDSO | AD | N | Y | Diamagnetic contribution |  |
    |  |  | SPSO | AD | N | Y | Paramagnetic contribution |  |
    |  |  | STot | AD | N | Y | Total tensor |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | sTotEigen | AD | N | Y | Eigenvalues |  |
    |  |  | siso | D | N | Y |  |  |
    |  |  | saniso | D | N | Y |  |  |
    | MP2_D_Tensor [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MP2_G_Tensor [G_Tensor] | Y | g_matrix | AD | N | N |  |  |
    |  |  | g_elec | D | N | N | The free electron g-value contribution |  |
    |  |  | g_RMC | D | N | N | The reduced mass correction |  |
    |  |  | g_DSO | AD | N | N |  |  |
    |  |  | g_PSO | AD | N | N |  |  |
    |  |  | g_Tot | AD | N | N |  |  |
    |  |  | g_iso | D | N | N |  |  |
    |  |  | Delta_g | AD | N | N |  |  |
    |  |  | Delta_g_iso | D | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MP2_Spin_Spin_Coupling [Spin_Spin_Coupling] | Y | numOfNucPairs | I | N | N | Number of nuclei pairs to calculate |  |
    |  |  | numOfNucPairsDSO | I | N | N | number of nuclear pairs to calculate DSO |  |
    |  |  | numOfNucPairsPSO | I | N | N | number of nuclear pairs to calculate PSO |  |
    |  |  | numOfNucPairsFC | I | N | N | number of nuclear pairs to calculate FC |  |
    |  |  | numOfNucPairsSD | I | N | N | number of nuclear pairs to calculate SD |  |
    |  |  | numOfNucPairsSD_FC | I | N | N | number of nuclear pairs to calculate SD/FC |  |
    |  |  | pairsInfo | AI | N | N | Pairs Info: Col1->Index of A. Col2->Atom. Num. of A. Col3->Index of B. Col4->Atom. Num. of B. |  |
    |  |  | pairsDistances | AD | N | N | The distances of each pair |  |
    |  |  | pairsTotalSSCIso | AD | N | N | The Spin-Spin coupling constant for each pair |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MP2_Absorption_Spectrum [Absorption_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | MP2_ECD_Spectrum [ECD_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | MRCI_Dipole_Moment [Dipole_Moment] | Y | dipoleMagnitude | D | N | N |  | a.u. |
    |  |  | dipoleElecContrib | AD | N | N | Electronic contribution |  |
    |  |  | dipoleNucContrib | AD | N | N | Nuclear contribution |  |
    |  |  | dipoleTotal | AD | N | N | Total |  |
    |  |  | doAtomicDipole | B | N | N |  |  |
    |  |  | atomicDipole | AD | Y | N | Atomic dipoles (NAtoms * X,Y,Z) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MRCI_EFG_Tensor [EFG_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | QFAC | D | N | Y | Prefactor |  |
    |  |  | V | AD | N | Y | Raw tensor |  |
    |  |  | VEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | VIso | D | N | Y |  |  |
    | MRCI_Polarizability [Polarizability] | Y | isotropicPolar | D | N | N |  |  |
    |  |  | rawCartesian | AD | N | N |  | a.u |
    |  |  | diagonalizedTensor | AD | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | doAtomicPolar | B | N | N |  |  |
    |  |  | atomicPolarIso | AD | Y | N | Atomic istotropic polarizabilities |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MRCI_Quadrupole_Moment [Quadrupole_Moment] | Y | isotropicQuadMoment | D | N | N |  | a.u. |
    |  |  | quadElecContrib | AD | N | N | Electronic contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadNucContrib | AD | N | N | Nuclear contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadTotal | AD | N | N | Total. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadDiagonalized | AD | N | N | The diagonalized tensor | a.u. |
    |  |  | doAtomicQuad | B | N | N |  |  |
    |  |  | atomicQuad | AD | Y | N | Atomic quadrupoles (NAtoms * XX, YY, ZZ, XY, XZ, YZ) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MRCI_A_Tensor [A_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elem | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | PFAC | D | N | Y | Prefactor PFAC=gegNbe*bN (in MHz) |  |
    |  |  | ARaw | AD | N | Y | Raw tensor |  |
    |  |  | AEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | AIso | D | N | Y |  |  |
    | MRCI_Chemical_Shift [Chemical_Shift] | Y | numOfNucs | I | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | SDSO | AD | N | Y | Diamagnetic contribution |  |
    |  |  | SPSO | AD | N | Y | Paramagnetic contribution |  |
    |  |  | STot | AD | N | Y | Total tensor |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | sTotEigen | AD | N | Y | Eigenvalues |  |
    |  |  | siso | D | N | Y |  |  |
    |  |  | saniso | D | N | Y |  |  |
    | MRCI_D_Tensor [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MRCI_G_Tensor [G_Tensor] | Y | g_matrix | AD | N | N |  |  |
    |  |  | g_elec | D | N | N | The free electron g-value contribution |  |
    |  |  | g_RMC | D | N | N | The reduced mass correction |  |
    |  |  | g_DSO | AD | N | N |  |  |
    |  |  | g_PSO | AD | N | N |  |  |
    |  |  | g_Tot | AD | N | N |  |  |
    |  |  | g_iso | D | N | N |  |  |
    |  |  | Delta_g | AD | N | N |  |  |
    |  |  | Delta_g_iso | D | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MRCI_Spin_Spin_Coupling [Spin_Spin_Coupling] | Y | numOfNucPairs | I | N | N | Number of nuclei pairs to calculate |  |
    |  |  | numOfNucPairsDSO | I | N | N | number of nuclear pairs to calculate DSO |  |
    |  |  | numOfNucPairsPSO | I | N | N | number of nuclear pairs to calculate PSO |  |
    |  |  | numOfNucPairsFC | I | N | N | number of nuclear pairs to calculate FC |  |
    |  |  | numOfNucPairsSD | I | N | N | number of nuclear pairs to calculate SD |  |
    |  |  | numOfNucPairsSD_FC | I | N | N | number of nuclear pairs to calculate SD/FC |  |
    |  |  | pairsInfo | AI | N | N | Pairs Info: Col1->Index of A. Col2->Atom. Num. of A. Col3->Index of B. Col4->Atom. Num. of B. |  |
    |  |  | pairsDistances | AD | N | N | The distances of each pair |  |
    |  |  | pairsTotalSSCIso | AD | N | N | The Spin-Spin coupling constant for each pair |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | D_Tensor_MRCI_2ndOrder [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | D_Tensor_MRCI_2ndOrder_ES [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | D_Tensor_MRCI_Heff [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | D_Tensor_MRCI_Heff_ES [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MRCI_Absorption_Spectrum [Absorption_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | MRCI_ECD_Spectrum [ECD_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | Nuclear_Gradient | Y | NAtoms | I | N | N |  |  |
    |  |  | gradNorm | D | N | N |  |  |
    |  |  | grad | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | CHELPG_Population_Analysis | Y | NAtoms | I | N | N |  |  |
    |  |  | ATNO | AI | N | N |  |  |
    |  |  | AtomicCharges | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | Hirshfeld_Population_Analysis | Y | NAtoms | I | N | N |  |  |
    |  |  | ATNO | AI | N | N |  |  |
    |  |  | DENSA | D | N | N | Total integrated alpha density |  |
    |  |  | DENSB | D | N | N | Total integrated beta density |  |
    |  |  | AtomicCharges | AD | N | N |  |  |
    |  |  | Spin | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | Loewdin_Population_Analysis | Y | NAtoms | I | N | N |  |  |
    |  |  | ATNO | AI | N | N |  |  |
    |  |  | AtomicCharges | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | Mayer_Population_Analysis | Y | NAtoms | I | N | N | Total number of atoms |  |
    |  |  | NBondOrdersPrint | I | N | N | The number of bond orders larger than threshold |  |
    |  |  | bondThresh | D | N | N | The threshold for printing |  |
    |  |  | components | AI | Y | N | The indices and atomic numbers of the bonding atoms |  |
    |  |  | BondOrders | AD | Y | N | The bond orders |  |
    |  |  | ATNO | AI | N | N | Atomic number of the elements |  |
    |  |  | NA | AD | N | N | Mulliken gross atomic population |  |
    |  |  | ZA | AD | N | N | Total nuclear charge |  |
    |  |  | QA | AD | N | N | Mulliken gross atomic charge |  |
    |  |  | VA | AD | N | N | Mayer’s total valence |  |
    |  |  | BVA | AD | N | N | Mayer’s bonded valence |  |
    |  |  | FA | AD | N | N | Mayer’s free valence |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MBIS_Population_Analysis | Y | NAtoms | I | N | N |  |  |
    |  |  | ATNO | AI | N | N |  |  |
    |  |  | Thresh | D | N | N |  |  |
    |  |  | Niter | I | N | N |  |  |
    |  |  | LargePrint | B | N | N |  |  |
    |  |  | DENSA | D | N | N | Total integrated alpha density |  |
    |  |  | DENSB | D | N | N | Total integrated beta density |  |
    |  |  | AtomicCharges | AD | N | N |  |  |
    |  |  | Spin | AD | N | N |  |  |
    |  |  | NPOPVAL | AD | N | N |  |  |
    |  |  | SIGMAVAL | AD | N | N |  |  |
    |  |  | AtomicDipole | AD | Y | N |  |  |
    |  |  | AtomicQuadrupole | AD | Y | N |  |  |
    |  |  | AtomicOctupole | AD | Y | N |  |  |
    |  |  | ThirdRadialMoment | AD | Y | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | Mulliken_Population_Analysis | Y | NAtoms | I | N | N |  |  |
    |  |  | ATNO | AI | N | N |  |  |
    |  |  | AtomicCharges | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | RASCI_Nuc_Gradient [Nuclear_Gradient] | Y | NAtoms | I | N | N |  |  |
    |  |  | gradNorm | D | N | N |  |  |
    |  |  | grad | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | RASCI_Dipole_Moment [Dipole_Moment] | Y | dipoleMagnitude | D | N | N |  | a.u. |
    |  |  | dipoleElecContrib | AD | N | N | Electronic contribution |  |
    |  |  | dipoleNucContrib | AD | N | N | Nuclear contribution |  |
    |  |  | dipoleTotal | AD | N | N | Total |  |
    |  |  | doAtomicDipole | B | N | N |  |  |
    |  |  | atomicDipole | AD | Y | N | Atomic dipoles (NAtoms * X,Y,Z) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | RASCI_EFG_Tensor [EFG_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | QFAC | D | N | Y | Prefactor |  |
    |  |  | V | AD | N | Y | Raw tensor |  |
    |  |  | VEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | VIso | D | N | Y |  |  |
    | RASCI_Polarizability [Polarizability] | Y | isotropicPolar | D | N | N |  |  |
    |  |  | rawCartesian | AD | N | N |  | a.u |
    |  |  | diagonalizedTensor | AD | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | doAtomicPolar | B | N | N |  |  |
    |  |  | atomicPolarIso | AD | Y | N | Atomic istotropic polarizabilities |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | RASCI_Quadrupole_Moment [Quadrupole_Moment] | Y | isotropicQuadMoment | D | N | N |  | a.u. |
    |  |  | quadElecContrib | AD | N | N | Electronic contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadNucContrib | AD | N | N | Nuclear contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadTotal | AD | N | N | Total. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadDiagonalized | AD | N | N | The diagonalized tensor | a.u. |
    |  |  | doAtomicQuad | B | N | N |  |  |
    |  |  | atomicQuad | AD | Y | N | Atomic quadrupoles (NAtoms * XX, YY, ZZ, XY, XZ, YZ) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | RASCI_A_Tensor [A_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elem | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | PFAC | D | N | Y | Prefactor PFAC=gegNbe*bN (in MHz) |  |
    |  |  | ARaw | AD | N | Y | Raw tensor |  |
    |  |  | AEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | AIso | D | N | Y |  |  |
    | RASCI_Chemical_Shift [Chemical_Shift] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | RASCI_D_Tensor [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | RASCI_G_Tensor [G_Tensor] | Y | g_matrix | AD | N | N |  |  |
    |  |  | g_elec | D | N | N | The free electron g-value contribution |  |
    |  |  | g_RMC | D | N | N | The reduced mass correction |  |
    |  |  | g_DSO | AD | N | N |  |  |
    |  |  | g_PSO | AD | N | N |  |  |
    |  |  | g_Tot | AD | N | N |  |  |
    |  |  | g_iso | D | N | N |  |  |
    |  |  | Delta_g | AD | N | N |  |  |
    |  |  | Delta_g_iso | D | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | RASCI_Spin_Spin_Coupling [Spin_Spin_Coupling] | Y | numOfNucPairs | I | N | N | Number of nuclei pairs to calculate |  |
    |  |  | numOfNucPairsDSO | I | N | N | number of nuclear pairs to calculate DSO |  |
    |  |  | numOfNucPairsPSO | I | N | N | number of nuclear pairs to calculate PSO |  |
    |  |  | numOfNucPairsFC | I | N | N | number of nuclear pairs to calculate FC |  |
    |  |  | numOfNucPairsSD | I | N | N | number of nuclear pairs to calculate SD |  |
    |  |  | numOfNucPairsSD_FC | I | N | N | number of nuclear pairs to calculate SD/FC |  |
    |  |  | pairsInfo | AI | N | N | Pairs Info: Col1->Index of A. Col2->Atom. Num. of A. Col3->Index of B. Col4->Atom. Num. of B. |  |
    |  |  | pairsDistances | AD | N | N | The distances of each pair |  |
    |  |  | pairsTotalSSCIso | AD | N | N | The Spin-Spin coupling constant for each pair |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | RASCI_Absorption_Spectrum [Absorption_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | RASCI_ECD_Spectrum [ECD_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | ROCIS_Energies | N | refEnergy | D | N | N |  |  |
    |  |  | corrEnergy | D | N | N |  |  |
    |  |  | totalEnergy | D | N | N |  |  |
    |  |  | numOfRoots | I | N | N |  |  |
    |  |  | Energies | AD | N | N | State energies in Hartree |  |
    |  |  | Multiplicities | AI | N | N |  |  |
    | ROCIS_Dipole_Moment [Dipole_Moment] | Y | dipoleMagnitude | D | N | N |  | a.u. |
    |  |  | dipoleElecContrib | AD | N | N | Electronic contribution |  |
    |  |  | dipoleNucContrib | AD | N | N | Nuclear contribution |  |
    |  |  | dipoleTotal | AD | N | N | Total |  |
    |  |  | doAtomicDipole | B | N | N |  |  |
    |  |  | atomicDipole | AD | Y | N | Atomic dipoles (NAtoms * X,Y,Z) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | ROCIS_EFG_Tensor [EFG_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | QFAC | D | N | Y | Prefactor |  |
    |  |  | V | AD | N | Y | Raw tensor |  |
    |  |  | VEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | VIso | D | N | Y |  |  |
    | ROCIS_Polarizability [Polarizability] | Y | isotropicPolar | D | N | N |  |  |
    |  |  | rawCartesian | AD | N | N |  | a.u |
    |  |  | diagonalizedTensor | AD | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | doAtomicPolar | B | N | N |  |  |
    |  |  | atomicPolarIso | AD | Y | N | Atomic istotropic polarizabilities |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | ROCIS_Quadrupole_Moment [Quadrupole_Moment] | Y | isotropicQuadMoment | D | N | N |  | a.u. |
    |  |  | quadElecContrib | AD | N | N | Electronic contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadNucContrib | AD | N | N | Nuclear contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadTotal | AD | N | N | Total. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadDiagonalized | AD | N | N | The diagonalized tensor | a.u. |
    |  |  | doAtomicQuad | B | N | N |  |  |
    |  |  | atomicQuad | AD | Y | N | Atomic quadrupoles (NAtoms * XX, YY, ZZ, XY, XZ, YZ) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | ROCIS_A_Tensor [A_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elem | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | PFAC | D | N | Y | Prefactor PFAC=gegNbe*bN (in MHz) |  |
    |  |  | ARaw | AD | N | Y | Raw tensor |  |
    |  |  | AEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | AIso | D | N | Y |  |  |
    | ROCIS_Chemical_Shift [Chemical_Shift] | Y | numOfNucs | I | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | SDSO | AD | N | Y | Diamagnetic contribution |  |
    |  |  | SPSO | AD | N | Y | Paramagnetic contribution |  |
    |  |  | STot | AD | N | Y | Total tensor |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | sTotEigen | AD | N | Y | Eigenvalues |  |
    |  |  | siso | D | N | Y |  |  |
    |  |  | saniso | D | N | Y |  |  |
    | ROCIS_D_Tensor [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | ROCIS_G_Tensor [G_Tensor] | Y | g_matrix | AD | N | N |  |  |
    |  |  | g_elec | D | N | N | The free electron g-value contribution |  |
    |  |  | g_RMC | D | N | N | The reduced mass correction |  |
    |  |  | g_DSO | AD | N | N |  |  |
    |  |  | g_PSO | AD | N | N |  |  |
    |  |  | g_Tot | AD | N | N |  |  |
    |  |  | g_iso | D | N | N |  |  |
    |  |  | Delta_g | AD | N | N |  |  |
    |  |  | Delta_g_iso | D | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | ROCIS_Spin_Spin_Coupling [Spin_Spin_Coupling] | Y | numOfNucPairs | I | N | N | Number of nuclei pairs to calculate |  |
    |  |  | numOfNucPairsDSO | I | N | N | number of nuclear pairs to calculate DSO |  |
    |  |  | numOfNucPairsPSO | I | N | N | number of nuclear pairs to calculate PSO |  |
    |  |  | numOfNucPairsFC | I | N | N | number of nuclear pairs to calculate FC |  |
    |  |  | numOfNucPairsSD | I | N | N | number of nuclear pairs to calculate SD |  |
    |  |  | numOfNucPairsSD_FC | I | N | N | number of nuclear pairs to calculate SD/FC |  |
    |  |  | pairsInfo | AI | N | N | Pairs Info: Col1->Index of A. Col2->Atom. Num. of A. Col3->Index of B. Col4->Atom. Num. of B. |  |
    |  |  | pairsDistances | AD | N | N | The distances of each pair |  |
    |  |  | pairsTotalSSCIso | AD | N | N | The Spin-Spin coupling constant for each pair |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | ROCIS_Absorption_Spectrum [Absorption_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | ROCIS_ECD_Spectrum [ECD_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | RPA_Dipole_Moment [Dipole_Moment] | Y | dipoleMagnitude | D | N | N |  | a.u. |
    |  |  | dipoleElecContrib | AD | N | N | Electronic contribution |  |
    |  |  | dipoleNucContrib | AD | N | N | Nuclear contribution |  |
    |  |  | dipoleTotal | AD | N | N | Total |  |
    |  |  | doAtomicDipole | B | N | N |  |  |
    |  |  | atomicDipole | AD | Y | N | Atomic dipoles (NAtoms * X,Y,Z) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | RPA_EFG_Tensor [EFG_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | QFAC | D | N | Y | Prefactor |  |
    |  |  | V | AD | N | Y | Raw tensor |  |
    |  |  | VEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | VIso | D | N | Y |  |  |
    | RPA_Polarizability [Polarizability] | Y | isotropicPolar | D | N | N |  |  |
    |  |  | rawCartesian | AD | N | N |  | a.u |
    |  |  | diagonalizedTensor | AD | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | doAtomicPolar | B | N | N |  |  |
    |  |  | atomicPolarIso | AD | Y | N | Atomic istotropic polarizabilities |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | RPA_Quadrupole_Moment [Quadrupole_Moment] | Y | isotropicQuadMoment | D | N | N |  | a.u. |
    |  |  | quadElecContrib | AD | N | N | Electronic contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadNucContrib | AD | N | N | Nuclear contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadTotal | AD | N | N | Total. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadDiagonalized | AD | N | N | The diagonalized tensor | a.u. |
    |  |  | doAtomicQuad | B | N | N |  |  |
    |  |  | atomicQuad | AD | Y | N | Atomic quadrupoles (NAtoms * XX, YY, ZZ, XY, XZ, YZ) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | RPA_A_Tensor [A_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elem | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | PFAC | D | N | Y | Prefactor PFAC=gegNbe*bN (in MHz) |  |
    |  |  | ARaw | AD | N | Y | Raw tensor |  |
    |  |  | AEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | AIso | D | N | Y |  |  |
    | RPA_Chemical_Shift [Chemical_Shift] | Y | numOfNucs | I | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | SDSO | AD | N | Y | Diamagnetic contribution |  |
    |  |  | SPSO | AD | N | Y | Paramagnetic contribution |  |
    |  |  | STot | AD | N | Y | Total tensor |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | sTotEigen | AD | N | Y | Eigenvalues |  |
    |  |  | siso | D | N | Y |  |  |
    |  |  | saniso | D | N | Y |  |  |
    | RPA_D_Tensor [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | RPA_G_Tensor [G_Tensor] | Y | g_matrix | AD | N | N |  |  |
    |  |  | g_elec | D | N | N | The free electron g-value contribution |  |
    |  |  | g_RMC | D | N | N | The reduced mass correction |  |
    |  |  | g_DSO | AD | N | N |  |  |
    |  |  | g_PSO | AD | N | N |  |  |
    |  |  | g_Tot | AD | N | N |  |  |
    |  |  | g_iso | D | N | N |  |  |
    |  |  | Delta_g | AD | N | N |  |  |
    |  |  | Delta_g_iso | D | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | RPA_Spin_Spin_Coupling [Spin_Spin_Coupling] | Y | numOfNucPairs | I | N | N | Number of nuclei pairs to calculate |  |
    |  |  | numOfNucPairsDSO | I | N | N | number of nuclear pairs to calculate DSO |  |
    |  |  | numOfNucPairsPSO | I | N | N | number of nuclear pairs to calculate PSO |  |
    |  |  | numOfNucPairsFC | I | N | N | number of nuclear pairs to calculate FC |  |
    |  |  | numOfNucPairsSD | I | N | N | number of nuclear pairs to calculate SD |  |
    |  |  | numOfNucPairsSD_FC | I | N | N | number of nuclear pairs to calculate SD/FC |  |
    |  |  | pairsInfo | AI | N | N | Pairs Info: Col1->Index of A. Col2->Atom. Num. of A. Col3->Index of B. Col4->Atom. Num. of B. |  |
    |  |  | pairsDistances | AD | N | N | The distances of each pair |  |
    |  |  | pairsTotalSSCIso | AD | N | N | The Spin-Spin coupling constant for each pair |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | RPA_Absorption_Spectrum [Absorption_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | RPA_ECD_Spectrum [ECD_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | Energy | Y | Method | S | N | N |  |  |
    |  |  | totalEnergy | AD | N | N | Total energy of each state |  |
    |  |  | Mult | AI | Y | N | Multiplicity of each state |  |
    |  |  | Irrep | AI | Y | N | Irreducible representation of each state |  |
    |  |  | RelCorr | S | Y | N | Relativistic correction (SOC and/or SSC) |  |
    |  |  | NBlocks | I | Y | N | Number of multiplicity blocks |  |
    |  |  | NRoots | AI | Y | N | Number of roots in each block |  |
    |  |  | NTotalRoots | I | Y | N | Total number of roots |  |
    |  |  | Block | AI | Y | N | Block index of each state |  |
    |  |  | Root | AI | Y | N | Root index within the block |  |
    |  |  | FollowIRoot | I | Y | N | Index of the followed root |  |
    |  |  | AvgMult | AD | Y | N | Average multiplicity of each SO-/SS-coupled state |  |
    | SCF_Energy [Energy] | Y | Method | S | N | N |  |  |
    |  |  | totalEnergy | AD | N | N | Total energy of each state |  |
    |  |  | Mult | AI | Y | N | Multiplicity of each state |  |
    |  |  | Irrep | AI | Y | N | Irreducible representation of each state |  |
    |  |  | RelCorr | S | Y | N | Relativistic correction (SOC and/or SSC) |  |
    |  |  | NBlocks | I | Y | N | Number of multiplicity blocks |  |
    |  |  | NRoots | AI | Y | N | Number of roots in each block |  |
    |  |  | NTotalRoots | I | Y | N | Total number of roots |  |
    |  |  | Block | AI | Y | N | Block index of each state |  |
    |  |  | Root | AI | Y | N | Root index within the block |  |
    |  |  | FollowIRoot | I | Y | N | Index of the followed root |  |
    |  |  | AvgMult | AD | Y | N | Average multiplicity of each SO-/SS-coupled state |  |
    | SCF_Nuc_Gradient [Nuclear_Gradient] | Y | NAtoms | I | N | N |  |  |
    |  |  | gradNorm | D | N | N |  |  |
    |  |  | grad | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | SCF_Dipole_Moment [Dipole_Moment] | Y | dipoleMagnitude | D | N | N |  | a.u. |
    |  |  | dipoleElecContrib | AD | N | N | Electronic contribution |  |
    |  |  | dipoleNucContrib | AD | N | N | Nuclear contribution |  |
    |  |  | dipoleTotal | AD | N | N | Total |  |
    |  |  | doAtomicDipole | B | N | N |  |  |
    |  |  | atomicDipole | AD | Y | N | Atomic dipoles (NAtoms * X,Y,Z) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | SCF_EFG_Tensor [EFG_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | QFAC | D | N | Y | Prefactor |  |
    |  |  | V | AD | N | Y | Raw tensor |  |
    |  |  | VEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | VIso | D | N | Y |  |  |
    | SCF_Polarizability [Polarizability] | Y | isotropicPolar | D | N | N |  |  |
    |  |  | rawCartesian | AD | N | N |  | a.u |
    |  |  | diagonalizedTensor | AD | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | doAtomicPolar | B | N | N |  |  |
    |  |  | atomicPolarIso | AD | Y | N | Atomic istotropic polarizabilities |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | SCF_Quadrupole_Moment [Quadrupole_Moment] | Y | isotropicQuadMoment | D | N | N |  | a.u. |
    |  |  | quadElecContrib | AD | N | N | Electronic contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadNucContrib | AD | N | N | Nuclear contribution. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadTotal | AD | N | N | Total. Order: XX, YY, ZZ, XY, XZ, YZ |  |
    |  |  | quadDiagonalized | AD | N | N | The diagonalized tensor | a.u. |
    |  |  | doAtomicQuad | B | N | N |  |  |
    |  |  | atomicQuad | AD | Y | N | Atomic quadrupoles (NAtoms * XX, YY, ZZ, XY, XZ, YZ) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | SCF_A_Tensor [A_Tensor] | Y | numOfNucs | I | N | N | Number of active nuclei |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elem | I | N | Y | Atomic number of the nuclei |  |
    |  |  | Isotope | D | N | Y | Atomic mass |  |
    |  |  | I | D | N | Y | Spin of the nuclei |  |
    |  |  | PFAC | D | N | Y | Prefactor PFAC=gegNbe*bN (in MHz) |  |
    |  |  | ARaw | AD | N | Y | Raw tensor |  |
    |  |  | AEigenvalues | AD | N | Y | Eigenvalues |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | AIso | D | N | Y |  |  |
    | SCF_Chemical_Shift [Chemical_Shift] | Y | numOfNucs | I | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    |  |  | NUC | I | N | Y | Index of the nuclei |  |
    |  |  | Elems | I | N | Y | Atomic number of the nuclei |  |
    |  |  | SDSO | AD | N | Y | Diamagnetic contribution |  |
    |  |  | SPSO | AD | N | Y | Paramagnetic contribution |  |
    |  |  | STot | AD | N | Y | Total tensor |  |
    |  |  | orientation | AD | N | Y | Eigenvectors |  |
    |  |  | sTotEigen | AD | N | Y | Eigenvalues |  |
    |  |  | siso | D | N | Y |  |  |
    |  |  | saniso | D | N | Y |  |  |
    | SCF_D_Tensor [D_Tensor] | Y | d_raw | AD | N | N |  |  |
    |  |  | d_eigenvalues | AD | N | N |  |  |
    |  |  | d_eigenvectors | AD | N | N |  |  |
    |  |  | D | D | N | N |  |  |
    |  |  | E | D | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | SCF_G_Tensor [G_Tensor] | Y | g_matrix | AD | N | N |  |  |
    |  |  | g_elec | D | N | N | The free electron g-value contribution |  |
    |  |  | g_RMC | D | N | N | The reduced mass correction |  |
    |  |  | g_DSO | AD | N | N |  |  |
    |  |  | g_PSO | AD | N | N |  |  |
    |  |  | g_Tot | AD | N | N |  |  |
    |  |  | g_iso | D | N | N |  |  |
    |  |  | Delta_g | AD | N | N |  |  |
    |  |  | Delta_g_iso | D | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | SCF_Spin_Spin_Coupling [Spin_Spin_Coupling] | Y | numOfNucPairs | I | N | N | Number of nuclei pairs to calculate |  |
    |  |  | numOfNucPairsDSO | I | N | N | number of nuclear pairs to calculate DSO |  |
    |  |  | numOfNucPairsPSO | I | N | N | number of nuclear pairs to calculate PSO |  |
    |  |  | numOfNucPairsFC | I | N | N | number of nuclear pairs to calculate FC |  |
    |  |  | numOfNucPairsSD | I | N | N | number of nuclear pairs to calculate SD |  |
    |  |  | numOfNucPairsSD_FC | I | N | N | number of nuclear pairs to calculate SD/FC |  |
    |  |  | pairsInfo | AI | N | N | Pairs Info: Col1->Index of A. Col2->Atom. Num. of A. Col3->Index of B. Col4->Atom. Num. of B. |  |
    |  |  | pairsDistances | AD | N | N | The distances of each pair |  |
    |  |  | pairsTotalSSCIso | AD | N | N | The Spin-Spin coupling constant for each pair |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | SCF_Absorption_Spectrum [Absorption_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | SCF_ECD_Spectrum [ECD_Spectrum] | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | SOC_Energy_Correction | N | total_SOC_energy | D | N | N |  |  |
    |  |  | total_non_SOC_energy | D | N | N |  |  |
    |  |  | nuclear_energy | D | N | N |  |  |
    |  |  | SOC_correction | D | N | N |  |  |
    | STEOM | N | S2 | AD | N | N | <S**2> |  |
    |  |  | PercentageActiveCharacter | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | excitationEnergies | AD | N | N | Total energy of each state |  |
    |  |  | Mult | AI | Y | N | Multiplicity of each state |  |
    |  |  | Irrep | AI | Y | N | Irreducible representation of each state |  |
    |  |  | RelCorr | S | Y | N | Relativistic correction (SOC and/or SSC) |  |
    |  |  | NBlocks | I | Y | N | Number of multiplicity blocks |  |
    |  |  | NRoots | AI | Y | N | Number of roots in each block |  |
    |  |  | NTotalRoots | I | Y | N | Total number of roots |  |
    |  |  | Block | AI | Y | N | Block index of each state |  |
    |  |  | Root | AI | Y | N | Root index within the block |  |
    |  |  | FollowIRoot | I | Y | N | Index of the followed root |  |
    |  |  | AvgMult | AD | Y | N | Average multiplicity of each SO-/SS-coupled state |  |
    | Absorption_Spectrum | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | ECD_Spectrum | Y | Method | I | N | N |  |  |
    |  |  | RelCorrection | I | N | N | Type of relativistic treatment in QDPT. 0->Unknow, 1->None, 2->SOC, 3->SSC, 4->SOC/SSC |  |
    |  |  | DensType | I | N | N | Type of density (electron/spin …). 0->Unknow, 1->Electronic, 2->Spin, 3->Trans/Electronic, 4->Tran/Spin |  |
    |  |  | DeriType | I | N | N | Type of derivative (w.r.t. to what perturbation). 0->Unknown, 1->No Derivative, 2->Electric/Dipole, 3->Electric/Quad, 4->Magnetic/Dipole, 5->Magnetic/Quad |  |
    |  |  | DensLevel | I | N | N | // Source of density: relaxed, unrelaxed, … 0->Unknown, 1->Linearized, 2->Unrelaxed, 3->Relaxed |  |
    |  |  | Density_name | S | N | N |  |  |
    |  |  | Representation | S | N | N | Possible values: Unknown, Length, Velocity |  |
    |  |  | PointGroup | S | N | N |  |  |
    |  |  | DoHigherMoments | B | N | N |  |  |
    |  |  | NTrans | I | N | N |  |  |
    |  |  | ExcitationEnergies | AD | N | N |  |  |
    |  |  | States | AI | N | N | The initial and Final states. Col1: Initial State Col2: Initial Irrep Col3: Final State Col4: Final Irrep |  |
    |  |  | Multiplicities | AD | N | N | Col1: Multiplicity of the initial state Col2: Multiplicity of the final state |  |
    |  |  | Temperature | D | N | N |  |  |
    | THERMOCHEMISTRY_Energies | Y | temperature | D | N | N |  |  |
    |  |  | pressure | D | N | N |  |  |
    |  |  | totalMass | D | N | N |  |  |
    |  |  | spinDegeneracy | I | N | N |  |  |
    |  |  | elEnergy | D | N | N |  |  |
    |  |  | transEnergy | D | N | N |  |  |
    |  |  | rotEnergy | D | N | N |  |  |
    |  |  | vibEnergy | D | N | N |  |  |
    |  |  | numOfFreqs | I | N | N |  |  |
    |  |  | freqScalingFactor | D | N | N |  |  |
    |  |  | FREQ | AD | N | N |  | cm^-1 |
    |  |  | zpe | D | N | N |  |  |
    |  |  | innerEnergyU | D | N | N |  |  |
    |  |  | enthalpyH | D | N | N |  |  |
    |  |  | qEl | D | N | N |  |  |
    |  |  | qRot | D | N | N |  |  |
    |  |  | qVib | D | N | N |  |  |
    |  |  | qTrans | D | N | N |  |  |
    |  |  | entropyS | D | N | N |  |  |
    |  |  | freeEnergyG | D | N | N |  |  |
    |  |  | isLinear | B | N | N |  |  |
    | VdW_Correction | N | vdW | D | N | N |  |  |
    |  |  | vdW_atomic | AD | Y | N |  |  |
    | Calculation_Status | N | version | S | N | N |  |  |
    |  |  | progName | S | N | N |  |  |
    |  |  | Status | S | N | N |  |  |
    | MDCI_EOM_Energies | Y | groundRefEnergy | D | N | N | Ground State Reference Energy |  |
    |  |  | groundCorrEnergy | D | N | N | Ground State Correlation Energy |  |
    |  |  | groundTotalEnergy | D | N | N | Ground State Total MDCI Energy |  |
    | CASPT2_Dipole_Moment [Dipole_Moment] | Y | dipoleMagnitude | D | N | N |  | a.u. |
    |  |  | dipoleElecContrib | AD | N | N | Electronic contribution |  |
    |  |  | dipoleNucContrib | AD | N | N | Nuclear contribution |  |
    |  |  | dipoleTotal | AD | N | N | Total |  |
    |  |  | doAtomicDipole | B | N | N |  |  |
    |  |  | atomicDipole | AD | Y | N | Atomic dipoles (NAtoms * X,Y,Z) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | CAS_CUSTOM_Dipole_Moment [Dipole_Moment] | Y | dipoleMagnitude | D | N | N |  | a.u. |
    |  |  | dipoleElecContrib | AD | N | N | Electronic contribution |  |
    |  |  | dipoleNucContrib | AD | N | N | Nuclear contribution |  |
    |  |  | dipoleTotal | AD | N | N | Total |  |
    |  |  | doAtomicDipole | B | N | N |  |  |
    |  |  | atomicDipole | AD | Y | N | Atomic dipoles (NAtoms * X,Y,Z) |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | CASPT2_G_Tensor [G_Tensor] | Y | g_matrix | AD | N | N |  |  |
    |  |  | g_elec | D | N | N | The free electron g-value contribution |  |
    |  |  | g_RMC | D | N | N | The reduced mass correction |  |
    |  |  | g_DSO | AD | N | N |  |  |
    |  |  | g_PSO | AD | N | N |  |  |
    |  |  | g_Tot | AD | N | N |  |  |
    |  |  | g_iso | D | N | N |  |  |
    |  |  | Delta_g | AD | N | N |  |  |
    |  |  | Delta_g_iso | D | N | N |  |  |
    |  |  | orientation | AD | N | N |  |  |
    |  |  | Method | S | N | N |  |  |
    |  |  | Level | S | N | N |  |  |
    |  |  | Mult | I | N | N |  |  |
    |  |  | State | I | N | N |  |  |
    |  |  | Irrep | I | N | N |  |  |
    | MDCI_LED | N | numOfFragments | I | N | N | The number of fragments |  |
    |  |  | sumNonDisStrong | D | N | N | Sum of non dispersive correlation strong pairs |  |
    |  |  | sumNonDisWeak | D | N | N | Sum of non dispersive correlation weak pairs |  |
    |  |  | electrostRef | AD | N | N | Electrostatics reference |  |
    |  |  | exchangeRef | AD | N | N | Exchange reference |  |
    |  |  | dispContr | AD | N | N | Strong pair dispersion contribution |  |
    |  |  | dispWeak | AD | N | N | Weak pair dispersion contribution |  |
    |  |  | refInt | AD | N | N | Interaction reference |  |
    |  |  | corrInt | AD | N | N | Interaction correlation |  |
    |  |  | totInt | AD | N | N | Interaction total |  |
    | Natural_Orbitals | N | NEL | I | N | N |  |  |
    |  |  | NSOMO | I | N | N |  |  |
    |  |  | NDOMO | I | N | N |  |  |
    |  |  | NVMO | I | N | N |  |  |
    |  |  | NNatoOrbs | I | N | N |  |  |
    |  |  | OccUno | AD | N | N | Occupation of natural orbitals |  |
    |  |  | OccUnso | AD | N | N | Occupation of spin natural orbitals |  |
    | Calculation_Timings | N | GTOINT | D | Y | N |  |  |
    |  |  | STOINT | D | Y | N |  |  |
    |  |  | SCF | D | Y | N |  |  |
    |  |  | SCFGRAD | D | Y | N |  |  |
    |  |  | GSTEP | D | Y | N |  |  |
    |  |  | PLOT | D | Y | N |  |  |
    |  |  | MOM | D | Y | N |  |  |
    |  |  | MP2 | D | Y | N |  |  |
    |  |  | CPSCF | D | Y | N |  |  |
    |  |  | LOC | D | Y | N |  |  |
    |  |  | CIS | D | Y | N |  |  |
    |  |  | MRCI | D | Y | N |  |  |
    |  |  | REL | D | Y | N |  |  |
    |  |  | SOC | D | Y | N |  |  |
    |  |  | EPRNMR | D | Y | N |  |  |
    |  |  | CASSCF | D | Y | N |  |  |
    |  |  | MDCI | D | Y | N |  |  |
    |  |  | CHELPG | D | Y | N |  |  |
    |  |  | ROCIS | D | Y | N |  |  |
    |  |  | MRCC | D | Y | N |  |  |
    |  |  | FCI | D | Y | N |  |  |
    |  |  | MD | D | Y | N |  |  |
    |  |  | FREQ | D | Y | N |  |  |
    |  |  | FREQ_NUM | D | Y | N |  |  |
    |  |  | COMPOUND | D | Y | N |  |  |
    |  |  | CIPSI | D | Y | N |  |  |
    |  |  | AUTOCI | D | Y | N |  |  |
    |  |  | ESD | D | Y | N |  |  |
    |  |  | DLPNOCC | D | Y | N |  |  |
    |  |  | MCRPA | D | Y | N |  |  |
    |  |  | NEB | D | Y | N |  |  |
    |  |  | CONFSC | D | Y | N |  |  |
    |  |  | ANMR | D | Y | N |  |  |
    |  |  | MM | D | Y | N |  |  |
    |  |  | MMGRAD | D | Y | N |  |  |
    |  |  | XTB | D | Y | N |  |  |
    |  |  | XTBGRAD | D | Y | N |  |  |
    |  |  | LFT | D | Y | N |  |  |
    |  |  | EXT | D | Y | N |  |  |
    |  |  | ONIOM_S | D | Y | N |  |  |
    |  |  | ONIOM_M | D | Y | N |  |  |
    |  |  | ONIOM_L | D | Y | N |  |  |
    |  |  | PROPINT | D | Y | N |  |  |
    |  |  | RESPONSE | D | Y | N |  |  |
    |  |  | PROP | D | Y | N |  |  |
    |  |  | CASRESP | D | Y | N |  |  |
    |  |  | MP2RESP | D | Y | N |  |  |
    |  |  | COSMORS | D | Y | N |  |  |
    |  |  | AUTOCIRESP | D | Y | N |  |  |
    |  |  | GOAT | D | Y | N |  |  |
    |  |  | CISRESP | D | Y | N |  |  |
    |  |  | EDA | D | Y | N |  |  |
    |  |  | SUM | D | Y | N |  |  |
    | SCF_Timings | N | TOTAL | D | Y | N |  |  |
    |  |  | PREP | D | Y | N |  |  |
    |  |  | GUESS | D | Y | N |  |  |
    |  |  | FOCK | D | Y | N |  |  |
    |  |  | DENS | D | Y | N |  |  |
    |  |  | DIAG | D | Y | N |  |  |
    |  |  | ETOT | D | Y | N |  |  |
    |  |  | POP | D | Y | N |  |  |
    |  |  | TRAFO | D | Y | N |  |  |
    |  |  | ORTHO | D | Y | N |  |  |
    |  |  | DIIS | D | Y | N |  |  |
    |  |  | SOSCF | D | Y | N |  |  |
    |  |  | NR | D | Y | N |  |  |
    |  |  | J | D | Y | N |  |  |
    |  |  | X | D | Y | N |  |  |
    |  |  | XC | D | Y | N |  |  |
    |  |  | GRID | D | Y | N |  |  |
    |  |  | FSYMMETR | D | Y | N |  |  |
    |  |  | PSYMMETR | D | Y | N |  |  |
    |  |  | FOCKSTART | D | Y | N |  |  |
    |  |  | SOLV | D | Y | N |  |  |
    |  |  | SOLV_INIT | D | Y | N |  |  |
    |  |  | SOLV_FINAL | D | Y | N |  |  |
    |  |  | INT_PREP | D | Y | N |  |  |
    |  |  | INT_PRESCREEN | D | Y | N |  |  |
    |  |  | INT_BF | D | Y | N |  |  |
    |  |  | INT_DENS | D | Y | N |  |  |
    |  |  | INT_DENSIO | D | Y | N |  |  |
    |  |  | INT_FUNC | D | Y | N |  |  |
    |  |  | INT_POT | D | Y | N |  |  |
    |  |  | INT_POTIO | D | Y | N |  |  |
    |  |  | INT_SUM | D | Y | N |  |  |
    |  |  | SPLITRIJ | D | Y | N |  |  |
    |  |  | COSX | D | Y | N |  |  |
    |  |  | COSX1C | D | Y | N |  |  |
    |  |  | RIJK | D | Y | N |  |  |
    |  |  | STABANA | D | Y | N |  |  |
    |  |  | DFET | D | Y | N |  |  |
    |  |  | ADFT_GUESS | D | Y | N |  |  |
    |  |  | ADFT_JDENS | D | Y | N |  |  |
    |  |  | ADFT_JMAT | D | Y | N |  |  |
    |  |  | ADFT_XDENS | D | Y | N |  |  |
    |  |  | ADFT_XMAT | D | Y | N |  |  |
    |  |  | ADFT_TMAT | D | Y | N |  |  |
    |  |  | ADFT_EQNSOLV | D | Y | N |  |  |
    |  |  | ECRISM | D | Y | N |  |  |
    |  |  | ECRISM_QESP | D | Y | N |  |  |
    |  |  | ECRISM_TOOL | D | Y | N |  |  |
    |  |  | ECRISM_FOCK | D | Y | N |  |  |
    |  |  | FROZCORE | D | Y | N |  |  |
    | Solvation_Details | N | Solvent | S | N | N |  |  |
    |  |  | Epsilon | D | N | N |  |  |
    |  |  | Refrac | D | N | N |  |  |
    |  |  | RSolv | D | N | N |  |  |
    |  |  | SurfaceType | S | N | N |  |  |
    |  |  | CPCMDielEnergy | D | N | N |  |  |
    |  |  | NPoints | I | N | N |  |  |
    |  |  | SurfaceArea | D | N | N |  |  |
    | Geometry | N | NAtoms | I | N | N |  |  |
    |  |  | NCorelessECP | I | N | N |  |  |
    |  |  | NGhostAtoms | I | N | N |  |  |
    |  |  | Coordinates | CC | N | N |  | Bohr |
    |  |  | ATNO | AI | N | N |  |  |
    |  |  | coreless_ECP | AI | Y | N | Non-zero for cECPs |  |
    |  |  | ghostAtoms | AI | Y | N | Non-zero for ghost atoms |  |
    |  |  | fragments | AI | Y | N | Fragment ID |  |
