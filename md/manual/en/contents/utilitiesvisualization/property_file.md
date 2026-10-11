```{index} Property File
```

(sec:property_file.detailed)=
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

:::{caution}
Since the whole file is read and re-written multiple times for each single point calculation,
optimizations of systems with a few thousand atoms can incur a few milliseconds of stacking I/O overhead,
per optimization cycle (i.e., a few seconds per cycle after several hundred steps).
Thus, it is recommended to disable the property file for such calculations
and this is done by default for `GOAT`, `MD-L-Opt`, `MM`, or `GFN-FF` chosen in the simple input.
:::

(sec:property_file.txtFormat.detailed)=
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
- Then a bracket opens with various bracket information about the component. For details on the syntax of the bracket information please check {ref}`sec:property_file.txtFormat.bracketInfo.detailed`.

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

(sec:property_file.txtFormat.bracketInfo.detailed)=
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

(sec:property_file.jsonFormat.detailed)=
## JSON Format

The property file can be also produced in a JSON format. Internally this happens through transformation of the `txt` format to JSON format. There are two ways to create a JSON property file.

The first way is through the normal ORCA input using the `JSONPropFile` keyword.

```orca
%Output
  JSONPropFile True
End
```

this will create a `basename.property.txt` and in addition a `basename.property.json` file.

The second way is through the [`orca_2json` command](sec:orca_2json.availableinformation.propertyFile).
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


(sec:property_file.list)=
## List of Available Properties

```{include} property_file_list.md
```
