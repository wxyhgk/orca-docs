

<a id="sec:orca_2json"></a>
# orca_2json

This utility program supports the exchange of external ORCA data like
geometry, orbitals and basis sets but also of internal ORCA data like
1-electron and 2-electron integrals with other programs.

<a id="sec:orca_2json.invocation"></a>
## Invocation and configuration

<a id="sec:orca_2json.invocation.manual_export"></a>
### Manual export of ORCA data and other options

The program reads information like geometries, basis sets, MOs etc.
stored in the `.gbw` file or other equivalent ones like `.uno`, `.mp2nat`,
`.qro` etc. and calculates integrals to export them in one of the JSON
standard output formats. For density information, the `.densities` file
must also be available. The program is called as a standalone via command line.

**Syntax:**
```orca
orca_2json BaseName.gbw -options
or
orca_2json BaseName.mp2nat -options
or
orca_2json BaseName.uno -options
```

The following ASCII and binary JSON formats are available as command
line options. It is possible to specify more than one format option.

```orca
  -json             Write ASCII JSON file (default)
  -bson             Write binary JSON file
  -ubjson           Write universal binary JSON specification file
  -msgpack          Write MessagePack file
```

In addition two more options are availble. The first of them is used to translate a basename.property.txt file to a corresponding one in JSON format (see [availableinformation.propertyFile](#sec:orca_2json.availableinformation.propertyFile)).

```orca
   -property        Translate a *.txt property file to a *.json one
```

Finally, orca_2json has the ability to create a `.gbw` file from a JSON file. For this one needs to use the `-gbw` option (see [orca_2json.importData](#sec:orca_2json.importData)).

```orca
   -gbw        Create a GBW file from a JSON one
```

<a id="sec:orca_2json.exportData.input"></a>
### Automatic export from ORCA job
It is also possible to run `orca_2json` on the `.gbw` file automatically
at the end of an ORCA job using the input:

```orca
%output
  JSONGBWFile true
end
```
This will simply run `orca_2json BaseName.gbw` with no additional options,
respecting any applicable configuration file, if present (see below).

<a id="sec:orca_2json.availableinformation.propertyFile"></a>
### Exporting the Property File to JSON

Beside all information that we will see orca_2json can create, it can also translate the property file of ORCA (basename.property.txt) to a JSON file. This option gives access to all properties stored in the property file. (For more information on property file see [property_file.detailed](property_file.md#sec:property_file.detailed)).

The **syntax** is:

```orca
orca_2json basename -property
```

*Where*

*basename* is the name of the property file **without** the extension *property.txt*.

**Example**

If we use the following ORCA input (with the name test.inp):

```orca
orca_2json BaseName.gbw -options
or
orca_2json BaseName.mp2nat -options
or
orca_2json BaseName.uno -options
```

ORCA will create and store on disk, a file named *"test.property.txt"*. The start of the file will look like this:

```orca
  -json             Write ASCII JSON file (default)
  -bson             Write binary JSON file
  -ubjson           Write universal binary JSON specification file
  -msgpack          Write MessagePack file
```

Then running *orca_2json* in the following way:

```orca
orca_2json test -property
```

ORCA will create a new file on disk, named *"test.property.json"*.
The corresponding part of this file will look like this:

```json
   -property        Translate a *.txt property file to a *.json one
```

!!! note
    The `property.json` structure has changed somewhat since ORCA version 6.0 and so have some of the property components.
    Converting an version 6.0 `property.txt` file to the current JSON format is partially possible but some data may be lost (with a warning).

<a id="sec:orca_2json.importData"></a>
### Importing JSON data into ORCA

Some information like geometry, basis set and Molecular orbitals stored in the JSON
format written by orca_2json can be used to create a new `.gbw` file to be
specified as an orbital file in the orca input. The program is called as
a standalone via command line.

```orca
orca_2json BaseName.json -gbw
```

In order to create a functional `.gbw` file, the at least the following information
must be provided:

|              |     |                   |
|:-------------|:---:|:------------------|
| per Atom     | \-  | Basis             |
|              | \-  | Coords            |
|              | \-  | ElementNumber     |
|              | \-  | NuclearCharge     |
| per molecule | \-  | Charge            |
|              | \-  | CoordinateUnits   |
|              | \-  | HFTyp             |
|              | \-  | Multiplicity      |
|              | \-  | MolecularOrbitals |

**NOTE**

Please keep in mind that *MolecularOrbitals* is a composite of 2 different components, namely *"EnergyUnit"* and *"MOs"*. Then *"MOs"* contains *"MOCoefficients"*, *"Occupancy"*, *"OrbitalEnergy"*, "OrbitalSymLabel"* and "OrbitalSymmetry"*.

**Example**

The following file (let's call it *filename.json*) is a JSON file for the H$_2$ molecule using the STO-3G basis set.

```json
   -gbw        Create a GBW file from a JSON one
```

running then the command

```orca
orca_2json filename.json -gbw
```

should create a `.gbw` file that ORCA can read.

<a id="sec:orca_2json.configurationFiles"></a>
### Configuration file

The data stored in the JSON file can be configured more individually.
Some information like atom information, geometry and charge are always
written in the outputfile (see [availableinformation.basic](#sec:orca_2json.availableinformation.basic)).
Other data can be requested via keywords in a
JSON-formatted configuration file that either exists for every ORCA
output file or for all files in a directory. Without these configuration
files **ALL** available data are stored except for the densities and the
integrals. Because of the huge amount of data these are only available
when explicitly requested in the configuration file.

You can specify a basename-dependent configuration file

```orca
BaseName.json.conf
```

or a global file used for all requests in a directory.

```orca
orca.json.conf
```

Most keywords in the configuration file can be activated or deactivated
with true or false but some keywords like densities or output formats
have more options and require a list of values. If an option is not
specifically selected it is omitted.

**Structure of the configuration file**:

```orca
{
	"keyword": true/false,
	...
	"keyword": true/false,
	"keyword": ["option",...."option"]
	...
}
```

**Example**
```orca
%output
  JSONGBWFile true
end
```
Using the above configuration file in the working directory, *orca_2json* will not  export the molecular coefficients and the basis set information.

**Example**

Here is an example configuration file with most available keywords where
everything is disabled except for the basis set information and the specified Integrals, all
densities stored in the density file are requested and the output format
should be ASCII JSON and binary JSON.

```orca
{
	"MOCoefficients": false,
	"Basisset": true,
	"1elPropertyIntegrals": ["dipole", "quadrupole", "velocity", "printLinMom", "angular_momentum", "higherMoment", "soc"],
	"1elPropertyRelIntegrals": ["dipole", "quadrupole", "angular_momentum", "soc"],
	"1elIntegrals": ["H", "S", "T", "V", "HMO"],
	"1elIntegralsRel": ["H", "S", "T", "V", "HMO"],
        "FockMatrix": ["F", "J", "K", "VXC", "Vsol"],
	"Vaux": false,
	"AuxBasisType": "AuxC",
	"FullTrafo": false,
	"OrbWin": [0,0,0,0,0,0,0,0],
	"2elIntegrals": [ "MO_IJKL", "RI_IAV", "RI_IJKL"],
	"2elNonRedIntegrals": false,
	"2elNonRedRIIntegrals": false,
	"MullikenCharge": false,
	"LoewdinCharge": false,
	"Densities": ["all"],   <--- here you specify the names like "scfp" or "scfr" or all
	"JSONFormats": ["json", "bson"]
}
```

<a id="sec:orca_2json.availableinformation.jsonformat"></a>
#### JSON Format

The JSON Format that is created can also be defined in the configuration file through the *JSONFormats* variable.

|                 |     |                                               |
|:----------------|:---:|:----------------------------------------------|
| JSONFormats     | \-  | JSON output format                            |

The available JSON formats are:

|         |     |                              |
|:--------|:---:|:-----------------------------|
| json    | \-  | ASCII JSON format            |
| bson    | \-  | binary JSON format           |
| ubjson  | \-  | universal binary JSON format |
| msgpck  | \-  | MessagePack format           |

**Example**
```json
orca_2json basename -property
```
<a id="sec:orca_2json.availableproperties"></a>
## Available information

<a id="sec:orca_2json.availableinformation.basic"></a>
### Basic Information
Some basic information will always be written into the JSON file as

|              |     |                 |
|:-------------|:---:|:----------------|
| per Atom     | \-  | Coords          |
|              | \-  | ElementLabel    |
|              | \-  | ElementNumber   |
|              | \-  | Idx             |
|              | \-  | NuclearCharge   |
| per molecule | \-  | BaseName        |
|              | \-  | Charge          |
|              | \-  | CoordinateUnits |
|              | \-  | HFTyp           |
|              | \-  | Multiplicity    |
|              | \-  | PointGroup      |

For example using the following configuration file where we set everything to false:
```json
!HF
*xyz 0 1
  H 0.0 0.0 0.0
  H 0.0 0.0 0.8
*
```
 will still produce a json file which for the case of an H$_2$ molecule should look like this:
 ```json
*************************************************
******************* ORCA 6.0.1 ******************
*************************************************
$Calculation_Status
   &GeometryIndex 1
   &version [&Type "String"] "6.0.1"
   &progName [&Type "String"] "LeanSCF"
   &Status [&Type "String"] "NORMAL TERMINATION"
$End
$Geometry
   &GeometryIndex 1
   &NAtoms [&Type "Integer"] 2
   &NCorelessECP [&Type "Integer"] 0
   &NGhostAtoms [&Type "Integer"] 0
   &CartesianCoordinates [&Type "Coordinates", &Dim(2,4), &Units "Bohr"]
              H      0.000000000000    0.000000000000    0.000000000000
              H      0.000000000000    0.000000000000    1.511780907137
$End
$SCF_Energy
   &GeometryIndex 1
   &totalEnergy [&Type "Double"]      -1.1271129220233282e+00
$End
```

<a id="sec:orca_2json.availableinformation.densities"></a>
### Densities

*orca_2json* can also export calculated densities in json format.

|                 |     |                                               |
|:----------------|:---:|:----------------------------------------------|
| Densities       | \-  | densities as available in the .densities file |

#### 2RDM

As of ORCA 6.1.0, it is possible to export 2RDM(s) in MO basis as calculated by the AutoCI module to JSON.
See the [AutoCI keywords table](tab:modelchemistries.autoci.keywords.block) for the available options.
The 2RDMs are not stored inside the `.densities` file, but in their own `.RDM2` files. The following
2RDMs are available
- `RDM2` (RHF, $\Gamma_{qs}^{pr}$)
- `RDM2_aa` (UHF, $\Gamma_{q_\alpha s_\alpha}^{p_\alpha r_\alpha}$)
- `RDM2_ab` (UHF, $\Gamma_{q_\alpha s_\beta}^{p_\alpha r_\beta}$)
- `RDM2_bb` (UHF, $\Gamma_{q_\beta s_\beta}^{p_\beta r_\beta}$)

Consider the general CI 2RDM:

$$
\Gamma_{qs}^{pr} = \langle \Psi | E_{pq} E_{rs} | \Psi \rangle.
$$

For every available combination of `p` and `q`, there will be a matrix `r` x `s` in the JSON. The values of
`p`,`q`,`r`,`s` range from `0` to the number of basis functions. For example, a fictional case in which there are only
2 basis functions and all elements of the 2RDM have been set to 0 will produce the following JSON.
```json
{
    "Densities": {
        "RDM2": {
            "0,0": [[0.0, 0.0], [0.0, 0.0]] // p=0, q=0
            "0,1": [[0.0, 0.0], [0.0, 0.0]] // p=0, q=1
            "1,0": [[0.0, 0.0], [0.0, 0.0]] // p=1, q=0
            "1,1": [[0.0, 0.0], [0.0, 0.0]] // p=1, q=1
        }
    }
}
```
Please note that the relaxed 2RDMs have been symmetrised to posses the following permutational symmetry

$$
\Gamma_{qs}^{pr} = \Gamma_{ps}^{qr} = \Gamma_{qr}^{ps} = \Gamma_{pr}^{qs} = \Gamma_{sq}^{rp} = \Gamma_{rq}^{sp} = \Gamma_{sp}^{rq} = \Gamma_{rp}^{sq}.
$$

#### Syntax
*"Densities" : [list of densities]*

Where *list of densities* should be a list of strings with the expected densities.

**NOTE** By default densities, due to their potential size, are not exported to a json file.

**NOTE** An empty bracket syntax (*"Densities" : []*) will cause the program to crash.

**NOTE** There is the string "All" available where the program will export all available densities.

<a id="sec:orca_2json.availableinformation.electronintegrals"></a>
### Electron Integrals

The list of available electron integrals is shown in the next table.

|                         |     |                                               |
|:------------------------|:---:|:----------------------------------------------|
| 1elIntegrals            | \-  | 1-electron integrals                          |
| 1elPropertyIntegrals    | \-  | 1-electron property integrals                 |
| 1elIntegralsRel         | \-  | relativistic 1-electron integrals             |
| 1elPropertyRelIntegrals | \-  | relativistic 1-electron property integrals    |
| 2elIntegrals            | \-  | two-electron integrals                        |
| 2elNonRedIntegrals      | \-  | non-redundant two-electron integrals          |
| 2elNonRedRIIntegrals    | \-  | non-redundant two-electron RI integrals       |
| FockMatrix              | \-  | two-electron contributions to the Fock matrix |

<a id="sec:orca_2json.availableinformation.electronintegrals.1el"></a>
#### 1-electron integrals

For 1-electron integrals we use the following notation:
|     |     |                                 |
|:----|:---:|:--------------------------------|
| H   | \-  | one electron matrix             |
| HMO | \-  | one electron matrix in MO basis |
| S   | \-  | overlap matrix                  |
| T   | \-  | kinetic energy matrix           |
| V   | \-  | nuclear attraction matrix       |

**Example**
```json
orca_2json test -property
```

will produce a json file were only the H-Matrix and the Overlap matrix are printed (beside the basic information). Please note that for the one electron relativistic integrals there is a separate variable (see [electronintegrals.1elrel](#sec:orca_2json.availableinformation.electronintegrals.1elrel))

<a id="sec:orca_2json.availableinformation.electronintegrals.1elproperty"></a>
#### 1-electron property integrals
Also available are 1-electron property integrals.

|                      |     |                                               |
|:---------------------|:---:|:----------------------------------------------|
| 1elPropertyIntegrals | \-  | 1-electron property integrals                 |

Currently the following options are valid:
|                   |     |                               |
|:------------------|:---:|:------------------------------|
| angular_momentum  | \-  | Angular momentum integrals    |
| dipole            | \-  | Dipole moment integrals       |
| higherMoment      | \-  | Octupole moment integrals     |
| quadrupole        | \-  | Quadrupole moment integrals   |
| velocity          | \-  | Velocity integrals            |
| soc               | \-  | Spin-orbit coupling integrals |

**Example**
```json
{
  "Calculation_Status": {
      "Status": "NORMAL TERMINATION",
      "progName": "LeanSCF",
      "version": "6.0.x"
  },
  "Geometries": [
    {
      "Geometry": {
        "Coordinates": {
            "Cartesians": [
                [
                    "H",
                    0.0,
                    0.0,
                    0.0
                ],
                [
                    "H",
                    0.0,
                    0.0,
                    1.511780907137
                ]
            ],
            "Type": "Cartesians",
            "Units": "a.u."
        },
        "NAtoms": 2,
        "NCorelessECP": 0,
        "NGhostAtoms": 0
      },
      "SCF_Energy": {
        "totalEnergy": -1.1271129220233282
      }
    }
  ]
}
```

!!! note
    SOC integrals are computed with the settings chosen in the `.gbw` file,
    except for the relativistic Hamiltonian (see [electronintegrals.1elrelprop](#sec:orca_2json.availableinformation.electronintegrals.1elrelprop) for the relativistic version).
    In the case of SOMF, the SCF density from the density container is used.

<a id="sec:orca_2json.availableinformation.electronintegrals.1elrel"></a>
#### 1-electron relativistic integrals

1-electron relativistic integrals follow the same notation as the corresponding non-relativistic ones (see [electronintegrals.1el](#sec:orca_2json.availableinformation.electronintegrals.1el)).

**Example**
```json
orca_2json BaseName.json -gbw
```
This example will produce and store in the corresponding json file the X2C-transformed H-Matrix,
as well as the separate potential and kinetic contributions.
Note that while the "relativistic" overlap matrix is available for completeness,
in X2C it is identical to the non-relativistic overlap by construction.

<a id="sec:orca_2json.availableinformation.electronintegrals.1elrelprop"></a>
#### 1-electron relativistic property integrals
Also available are 1-electron relativistic (X2C) property integrals similar to the non-relativistic ones but with reduced options.

|                         |     |                                               |
|:------------------------|:---:|:----------------------------------------------|
| 1elPropertyRelIntegrals | \-  | relativistic 1-electron property integrals    |

Currently the following options are valid:
|                   |     |                               |
|:------------------|:---:|:------------------------------|
| angular_momentum  | \-  | Angular momentum integrals    |
| dipole            | \-  | Dipole moment integrals       |
| quadrupole        | \-  | Quadrupole moment integrals   |
| soc               | \-  | Spin-orbit coupling integrals |

**Example**
```json
{
  "Molecule": {
    "Atoms": [
      {"Basis": [
          {"Coefficients": [ 0.1543289707029839,
              0.5353281424384732,0.44463454202535485],
            "Exponents": [3.42525091,0.62391373,0.1688554],
            "Shell": "s"}],
        "Coords": [0.0,0.0,0.0],
        "ElementNumber": 1,
        "NuclearCharge": 1.0},
      {"Basis": [
          {"Coefficients": [0.1543289707029839,
              0.5353281424384732,0.44463454202535485],
            "Exponents": [3.42525091,0.62391373,0.1688554],
            "Shell": "s"}],
        "Coords": [0.0,0.0,0.8],
        "ElementNumber": 1,
        "NuclearCharge": 1.0}],
    "Charge": 0,
    "CoordinateUnits": "Angs",
    "HFTyp": "RHF",
    "MolecularOrbitals": {
      "EnergyUnit": "Eh",
      "MOs": [{"MOCoefficients": [
            -0.5554171364661243,-0.5554171364661241],
          "Occupancy": 2.0,
          "OrbitalEnergy": -0.5544958795933514,
          "OrbitalSymLabel": "A",
          "OrbitalSymmetry": 0},
        {"MOCoefficients": [
            -1.1482994800696493,1.1482994800696493],
          "Occupancy": 0.0,
          "OrbitalEnergy": 0.6126180830925017,
          "OrbitalSymLabel": "A",
          "OrbitalSymmetry": 0}]},
    "Multiplicity": 1}
}
```
<a id="sec:orca_2json.availableinformation.electronintegrals.1elorigin"></a>
#### Origin setting
The origin of the electric property is per default the Cartesian origin but also the center of mass and the center of nuclear charges can be selected. Additionally an arbitrary position can be given as x,y,z coordinates when ori_el = 3 is chosen.
Currently the following options are valid:
|                   |     |                               |
|:------------------|:---:|:------------------------------|
| ori_el            | \-  | 0 - Cartesian origin          |
|                   | \-  | 1 - center of mass            |
|                   | \-  | 2 - center of nuclear charge  |
|                   | \-  | 3 - arbitrary position        |
| ori_el_xyz        | \-  | position of the origin(x,y,z) |

**Example**
```json
orca_2json filename.json -gbw
```

<a id="sec:orca_2json.availableinformation.electronintegrals.2el"></a>
#### Fock matrix contributions

The following two-electron contributions to the AO-basis Fock matrix can be exported:
|     |     |                                 |
|:----|:---:|:--------------------------------|
| J   | \-  | Coulomb                         |
| K   | \-  | Exchange                        |
| VXC | \-  | DFT XC potential                |
| Vsol| \-  | Implicit solvent potential      |
| F   | \-  | Total Fock matrix               |

!!! note
    - All terms are computed using the SCF (spin-)density from the .densities file (named "scfp" and "scfr").
    - The same settings and approximations (RI, COSX, grids) as in the original calculation are used.
    - All prefactors are already included, such that $\mathrm{F} = \mathrm{J} + \mathrm{K} + \mathrm{VXC} + \mathrm{Vsol}$.
    - For consistency, the output dimensions are always $N_\text{spin-ops} \times N_\text{AO} \times N_\text{AO}$,
      even though all matrices are symmetric and some terms (J and Vsol) are equal for alpha/beta in the UHF case.
    - The 1-electron contributions ("H") are not included and must be requested separately
      (see [electronintegrals.1el](#sec:orca_2json.availableinformation.electronintegrals.1el),
      as well as [electronintegrals.1elrel](#sec:orca_2json.availableinformation.electronintegrals.1elrel) for the relativistic case).

**Example**
```json
BaseName.json.conf
```

#### 2-electron integrals

ORCA_2json can produce and write on disk three main categories of 2-electron integrals.
1. Two-electron integrals in atomic basis ([2el.AO](#sec:orca_2json.availableinformation.electronintegrals.2el.AO))
2. Two-electron integrals in molecular basis ([2el.MO](#sec:orca_2json.availableinformation.electronintegrals.2el.MO))
3. Two-electron integrals using the resolution of identity approximation (RI). ([2el.RI](#sec:orca_2json.availableinformation.electronintegrals.2el.RI))

<a id="sec:orca_2json.availableinformation.electronintegrals.2el.AO"></a>
##### 2-electron integrals in AO basis

In atomic basis the two-electron integrals can be saved in Coulomb order or in Exchange order. The keywords for the two options are shown in the next table.

|             |     |                                               |
|:------------|:---:|:----------------------------------------------|
|  AO_PQRS    | \-  |  AO basis integrals in Coulomb order          |
|  AO_PRQS    | \-  |  AO basis integrals in Exchange order         |

<a id="sec:orca_2json.availableinformation.electronintegrals.2el.MO"></a>
##### 2-electron integrals in MO basis

In molecular basis, ORCA follows the accepted notation where by I,J,K and L we specify "internal" orbitals, meaning occupied in the reference wavefunction while by A,B,C and D we specify "external" orbitals, meaning orbitals that are empty in the reference wavefunction.
With P,Q,R and S we specify all possible orbitals, meaning both "internal" and "external".
The available keywords in *"orca_2json"* for the two-electron integrals in the molecular basis are the ones shown in the table below:
|             |     |                                               |
|:------------|:---:|:----------------------------------------------|
|  MO_IJKL    | \-  |  Coulomb 0-external                           |
|  MO_IJKA    | \-  |  Coulomb 1-external                           |
|  MO_IJAB    | \-  |  Coulomb 2-external                           |
|  MO_IABC    | \-  |  Coulomb 3-external                           |
|  MO_ABCD    | \-  |  Coulomb 4-external                           |
|  MO_PQRS    | \-  |  Coulomb ALL integrals                        |
|  MO_IKJL    | \-  |  Exchange 0-external                          |
|  MO_IKJA    | \-  |  Exchange 1-external                          |
|  MO_IAJB    | \-  |  Exchange 2-external                          |
|  MO_IBAC    | \-  |  Exchange 3-external                          |
|  MO_ACBD    | \-  |  Exchange 4-external                          |
|  MO_PRQS    | \-  |  Exchange ALL integrals                       |

**Example**
```json
orca.json.conf
```

<a id="sec:orca_2json.availableinformation.electronintegrals.2el.RI"></a>
##### RI 2-electron integrals

Using the Resolution of Identity (RI) one can create the integrals in a more efficient way. There are two main categories of RI integrals: the 3-index integrals, where only only half of the transformation has taken place, and the 4-index integrlas where the integrals are totally transformed in the molecular basis. The notation of the integrals follows the one we just described for the two-electron integrals in the molecular basis.

|             |     |                                               |
|:------------|:---:|:----------------------------------------------|
|  RI_IJV     | \-  |  RI 3-index 0-external                        |
|  RI_IAV     | \-  |  RI 3-index 1-external                        |
|  RI_ABV     | \-  |  RI 3-index 2-external                        |
|  RI_IJKL    | \-  |  RI 4-index Coulomb 0-external                |
|  RI_IJKA    | \-  |  RI 4-index Coulomb 1-external                |
|  RI_IJAB    | \-  |  RI 4-index Coulomb 2-external                |
|  RI_IABC    | \-  |  RI 4-index Coulomb 3-external                |
|  RI_ABCD    | \-  |  RI 4-index Coulomb 4-external                |
|  RI_IKJL    | \-  |  RI 4-index Exchange 0-external               |
|  RI_IKJA    | \-  |  RI 4-index Exchange 1-external               |
|  RI_IAJB    | \-  |  RI 4-index Exchange 2-external               |
|  RI_IBAC    | \-  |  RI 4-index Exchange 3-external               |
|  RI_ACBD    | \-  |  RI 4-index Exchange 4-external               |

In addition to the integrals in case of RI integrals also the used RI Metric is available through the option Vaux:
|             |     |                                               |
|:------------|:---:|:----------------------------------------------|
|  Vaux       | \-  |  true/false                                   |

**Example**
```json
{
	"keyword": true/false,
	...
	"keyword": true/false,
	"keyword": ["option",...."option"]
	...
}
```

<a id="sec:orca_2json.availableinformation.electronintegrals.2el.fulltrafo"></a>
##### Full Integral Transformation

The full transformation integrals can be selected via the FullTrafo keyword.

|              |     |                     |
|:-------------|:---:|:--------------------|
|  FullTrafo   | \-  | true/false          |

<a id="sec:orca_2json.availableinformation.electronintegrals.2el.nonred"></a>
##### More 2-electron integrals

Also the non-redundant 2-electron integrals are available for the RI and the nonRI case. Therefore the options 2elNonRedIntegrals or 2elNonRedRIIntegrals must be specified.

|                       |     |                     |
|:----------------------|:---:|:--------------------|
|  2elNonRedIntegrals   | \-  | true/false          |
|  2elNonRedRIIntegrals | \-  | true/false          |

<a id="sec:orca_2json.availableinformation.electronintegrals.2el.orbwin"></a>
##### Orbital Windows, AuxBasisType and Threshold

The orbital window can either be selected automatically by the transformation routine or given by the user via the OrbWin keyword. The internal and external space (i0,i1,a0,a1) is defined via an integer list.

for example:
|              |     |                          |
|:-------------|:---:|:-------------------------|
|  OrbWin      | \-  |  [0,8,9,15]              |
|              | \-  |  [0,12,13,30,0,12,13,30] |

The default AUX basis type is AuxC but can be changed with the keyword AuxBasisType. Please keep in mind that only those basis types used during the ORCA run can be selected.

|               |     |         |
|:--------------|:---:|:--------|
|  AuxBasisType | \-  |  AuxJ   |
|               | \-  |  AuxJK  |
|               | \-  |  AuxC   |

To reduce the number of the integrals the keyword Thresh can be used to decrease the selected integrals to save disk space. This effects ONLY the printing and not the accuracy of the generated integrals. The default print threshold is 1.e-15.

|              |     |                                      |
|:-------------|:---:|:-------------------------------------|
|  Thresh      | \-  |  printout threshold (default 1.e-15) |

**Example**
```json
{
  "MOCoefficients":false,
  "BasisSet":false
}
```

<a id="sec:orca_2json.availableinformation.CIS"></a>
### TDDFT amplitude data (CIS/RPA)

The TDDFT amplitudes and root informations can be requested.
The available options are:

|              |     |                              |
|:-------------|:---:|:-----------------------------|
| CIS          | \-  | TDDFT amplitudes             |
| CISNRoots    | \-  | informations of all roots    |
| CISROOT      | \-  | List of roots                |

**Example**
Print Selected roots. Root number corresponds to `STATE` number from ORCA output file.
```json
{
	"MOCoefficients": false,
	"Basisset": true,
	"1elPropertyIntegrals": ["dipole", "quadrupole", "velocity", "printLinMom", "angular_momentum", "higherMoment", "soc"],
	"1elPropertyRelIntegrals": ["dipole", "quadrupole", "angular_momentum", "soc"],
	"1elIntegrals": ["H", "S", "T", "V", "HMO"],
	"1elIntegralsRel": ["H", "S", "T", "V", "HMO"],
        "FockMatrix": ["F", "J", "K", "VXC", "Vsol"],
	"Vaux": false,
	"AuxBasisType": "AuxC",
	"FullTrafo": false,
	"OrbWin": [0,0,0,0,0,0,0,0],
	"2elIntegrals": [ "MO_IJKL", "RI_IAV", "RI_IJKL"],
	"2elNonRedIntegrals": false,
	"2elNonRedRIIntegrals": false,
	"MullikenCharge": false,
	"LoewdinCharge": false,
	"Densities": ["all"],   <--- here you specify the names like "scfp" or "scfr" or all
	"JSONFormats": ["json", "bson"]
}
```
**Example**
Print all roots.
```json
{
  "JSONFormats":["json","bson","ubjson","msgpck"]
}
```

<a id="sec:orca_2json.availableinformation.STEOM"></a>
### STEOM amplitude data

The STEOM singles amplitudes and root informations can be requested.
The available options are:

|                   |     |                              |
|:------------------|:---:|:-----------------------------|
| STEOM             | \-  | STEOM singles amplitudes     |
| STEOMRootsSinglet | \-  | List of singlet roots        |
| STEOMRootsTriplet | \-  | List of triplet roots        |

**Example**
Print all roots.
```json
{
  "MOCoefficients": false,
  "Basisset": false,
  "MullikenCharge": false,
  "LoewdinCharge": false,
  "JSONFormats": ["json"]
}
```
**Example**
Print selected roots. Root number corresponds to `IROOT` number from ORCA output file.
```json
{
  "Molecule": {
    "Atoms": [
      {
        "Coords": [
          0.0,
          0.0,
          0.0
        ],
        "ElementLabel": "H",
        "ElementNumber": 1,
        "Idx": 0,
        "NuclearCharge": 1.0
      },
      {
        "Coords": [
          0.0,
          0.0,
          0.8
        ],
        "ElementLabel": "H",
        "ElementNumber": 1,
        "Idx": 1,
        "NuclearCharge": 1.0
      }
    ],
    "BaseName": "test",
    "Charge": 0,
    "CoordinateUnits": "Angs",
    "HFTyp": "RHF",
    "Multiplicity": 1,
    "PointGroup": "C1"
  },
  "ORCA Header": {
    "Date": "2024-06-03 00:06:37 +0200",
    "Git": "548015a5a0",
    "Version": "                         Program Version 6.0  -  CURRENT   -\n"
  }
}
```

<a id="sec:orca_2json.availableinformation.mocoefficients"></a>
### MO Coefficients

|                 |     |                                               |
|:----------------|:---:|:----------------------------------------------|
| MOCoefficients  | \-  | molecule orbital information (true\false)     |

**Example**
```json
{
    "Densities": {
        "RDM2": {
            "0,0": [[0.0, 0.0], [0.0, 0.0]] // p=0, q=0
            "0,1": [[0.0, 0.0], [0.0, 0.0]] // p=0, q=1
            "1,0": [[0.0, 0.0], [0.0, 0.0]] // p=1, q=0
            "1,1": [[0.0, 0.0], [0.0, 0.0]] // p=1, q=1
        }
    }
}
```

<a id="sec:orca_2json.real_solid_harmonics"></a>
## Definition of the real solid harmonic orbitals

When integrals over real solid harmonic orbitals are issued
into a JSON file, the precise definition of these orbitals becomes
important. ORCA uses its own peculiar conventions for the arrangement
and the phases of the individual components of the orbital shells.

The definitions of the angular parts of all shell components up to
angular momentum $n$ ($\ell=10$) are documented below. These correspond
to the real solid harmonics $S_{\ell,m}(x,y,z)$ that are normalized the
following way:

$$
\begin{aligned}
    \in t_0^\pi\sin\vartheta\,d\vartheta
    \in t_{-\pi}^\pi d\varphi\,r^{-2\ell}S^2_{\ell,m}(x,y,z)=1
  \end{aligned}
$$

$R_\ell(r)$ is the common radial part of a shell with angular momentum
$\ell$ that consists of a specific basis set dependent linear
combination of atomic primitives. It is normalized independently:

$$
\begin{aligned}
    \in t_0^\in fty r^{2\ell+2}R^2_\ell(r)\,dr=1
  \end{aligned}
$$

The factors $r^2$ and $\sin\vartheta$ in these integrals arise from the
volume element in spherical polar coordinates:

$$
\begin{aligned}
    x &= r\sin\vartheta\cos\varphi \\
    y &= r\sin\vartheta\sin\varphi \\
    z &= r\cos\vartheta \\
    dx\,dy\,dz &= r^2\sin\vartheta\,dr\,d\vartheta\,d\varphi
  \end{aligned}
$$

Please note that the symmetry module is currently still restricted to
a maximum angular momentum quantum number of 8.

### Angular momentum $s$ ($l = 0$)

$$
\begin{aligned}
    s &= \frac{1}{2\sqrt{\pi} }\,R_s(r)
  \end{aligned}
$$

### Angular momentum $p$ ($l = 1$)

$$
\begin{aligned}
    N_p &= \frac{1}{2}\sqrt{\frac{3}{\pi} } \\
    p^{(0) } = p_{0\phantom{+} } &= N_p\,z\,R_p(r) \\
    p^{(1) } = p_{+1} &= N_p\,x\,R_p(r) \\
    p^{(2) } = p_{-1} &= N_p\,y\,R_p(r)
  \end{aligned}
$$

### Angular momentum $d$ ($l = 2$)

$$
\begin{aligned}
    N_d &= \frac{1}{2}\sqrt{\frac{15}{\pi} } \\
    d^{(0) } = d_{0\phantom{+} } &= \frac{\sqrt{3} }{6}\,N_d\left(3z^2-r^2\right)R_d(r) \\
    d^{(1) } = d_{+1} &= N_d\,xz\,R_d(r) \\
    d^{(2) } = d_{-1} &= N_d\,yz\,R_d(r) \\
    d^{(3) } = d_{+2} &= N_d\,\frac{x^2-y^2}{2}\,R_d(r) \\
    d^{(4) } = d_{-2} &= N_d\,xy\,R_d(r)
  \end{aligned}
$$

### Angular momentum $f$ ($l = 3$)

$$
\begin{aligned}
    N_f &= \frac{1}{2}\sqrt{\frac{105}{\pi} } \\
    f^{(0) } = f_{0\phantom{+} } &= \frac{\sqrt{15} }{30}\,N_f\,z\left(5z^2-3r^2\right)R_f(r) \\
    f^{(1) } = f_{+1} &= \frac{\sqrt{10} }{20}\,N_f\,x\left(5z^2-r^2\right)R_f(r) \\
    f^{(2) } = f_{-1} &= \frac{\sqrt{10} }{20}\,N_f\,y\left(5z^2-r^2\right)R_f(r) \\
    f^{(3) } = f_{+2} &= \frac{1}{2}\,N_f\left(x^2-y^2\right)z\,R_f(r) \\
    f^{(4) } = f_{-2} &= N_f\,xyz\,R_f(r) \\
    f^{(5) } = f_{+3} &= -\frac{\sqrt{6} }{12}\,N_f\,x\left(x^2-3y^2\right)R_f(r) \\
    f^{(6) } = f_{-3} &= -\frac{\sqrt{6} }{12}\,N_f\,y\left(3x^2-y^2\right)R_f(r)
  \end{aligned}
$$

### Angular momentum $g$ ($l = 4$)

$$
\begin{aligned}
    N_g &= \frac{3}{2}\sqrt{\frac{35}{\pi} } \\
    g^{(0) } = g_{0\phantom{+} } &= \frac{\sqrt{35} }{280}\,N_g\left(35z^4-30z^2r^2+3r^4\right)R_g(r) \\
    g^{(1) } = g_{+1} &= \frac{\sqrt{14} }{28}\,N_g\,xz\left(7z^2-3r^2\right)R_g(r) \\
    g^{(2) } = g_{-1} &= \frac{\sqrt{14} }{28}\,N_g\,yz\left(7z^2-3r^2\right)R_g(r) \\
    g^{(3) } = g_{+2} &= \frac{\sqrt{7} }{28}\,N_g\left(x^2-y^2\right)\left(7z^2-r^2\right)R_g(r) \\
    g^{(4) } = g_{-2} &= \frac{\sqrt{7} }{14}\,N_g\,xy\left(7z^2-r^2\right)R_g(r) \\
    g^{(5) } = g_{+3} &= -\frac{\sqrt{2} }{4}\,N_g\,x\left(x^2-3y^2\right)z\,R_g(r) \\
    g^{(6) } = g_{-3} &= -\frac{\sqrt{2} }{4}\,N_g\,y\left(3x^2-y^2\right)z\,R_g(r) \\
    g^{(7) } = g_{+4} &= -\frac{1}{8}\,N_g\left(x^4-6x^2y^2+y^4\right)R_g(r) \\
    g^{(8) } = g_{-4} &= -\frac{1}{2}\,N_g\,xy\left(x^2-y^2\right)R_g(r)
  \end{aligned}
$$

### Angular momentum $h$ ($l = 5$)

$$
\begin{aligned}
    N_h &= \frac{1}{2}\sqrt{\frac{11}{\pi} } \\
    h^{(0) }  = h_{0\phantom{+} } &= \frac{1}{8}\,N_h\,z\left(63z^4-70z^2r^2+15r^4\right)R_h(r) \\
    h^{(1) }  = h_{+1} &= \frac{\sqrt{15} }{8}\,N_h\,x\left(21z^4-14z^2r^2+r^4\right)R_h(r) \\
    h^{(2) }  = h_{-1} &= \frac{\sqrt{15} }{8}\,N_h\,y\left(21z^4-14z^2r^2+r^4\right)R_h(r) \\
    h^{(3) }  = h_{+2} &= \frac{\sqrt{105} }{4}\,N_h\left(x^2-y^2\right)z\left(3z^2-r^2\right)R_h(r) \\
    h^{(4) }  = h_{-2} &= \frac{\sqrt{105} }{2}\,N_h\,xyz\left(3z^2-r^2\right)R_h(r) \\
    h^{(5) }  = h_{+3} &= -\frac{\sqrt{70} }{16}\,N_h\,x\left(x^2-3y^2\right)\left(9z^2-r^2\right)R_h(r) \\
    h^{(6) }  = h_{-3} &= -\frac{\sqrt{70} }{16}\,N_h\,y\left(3x^2-y^2\right)\left(9z^2-r^2\right)R_h(r) \\
    h^{(7) }  = h_{+4} &= -\frac{3\sqrt{35} }{8}\,N_h\left(x^4-6x^2y^2+y^4\right)z\,R_h(r) \\
    h^{(8) }  = h_{-4} &= -\frac{3\sqrt{35} }{2}\,N_h\,xy\left(x^2-y^2\right)z\,R_h(r) \\
    h^{(9) }  = h_{+5} &= \frac{3\sqrt{14} }{16}\,N_h\,x\left(x^4-10x^2y^2+5y^4\right)R_h(r) \\
    h^{(10) } = h_{-5} &= \frac{3\sqrt{14} }{16}\,N_h\,y\left(5x^4-10x^2y^2+y^4\right)R_h(r)
  \end{aligned}
$$

### Angular momentum $i$ ($l = 6$)

$$
\begin{aligned}
    N_i &= \frac{1}{2}\sqrt{\frac{13}{\pi} } \\
    i^{(0) }  = i_{0\phantom{+} } &= \frac{1}{16}\,N_i\left(231z^6-315z^4r^2+105z^2r^4-5r^6\right)R_i(r) \\
    i^{(1) }  = i_{+1} &= \frac{\sqrt{21} }{8}\,N_i\,xz\left(33z^4-30z^2r^2+5r^4\right)R_i(r) \\
    i^{(2) }  = i_{-1} &= \frac{\sqrt{21} }{8}\,N_i\,yz\left(33z^4-30z^2r^2+5r^4\right)R_i(r) \\
    i^{(3) }  = i_{+2} &= \frac{\sqrt{210} }{32}\,N_i\left(x^2-y^2\right)\left(33z^4-18z^2r^2+r^4\right)R_i(r) \\
    i^{(4) }  = i_{-2} &= \frac{\sqrt{210} }{16}\,N_i\,xy\left(33z^4-18z^2r^2+r^4\right)R_i(r) \\
    i^{(5) }  = i_{+3} &= -\frac{\sqrt{210} }{16}\,N_i\,x\left(x^2-3y^2\right)z\left(11z^2-3r^2\right)R_i(r) \\
    i^{(6) }  = i_{-3} &= -\frac{\sqrt{210} }{16}\,N_i\,y\left(3x^2-y^2\right)z\left(11z^2-3r^2\right)R_i(r) \\
    i^{(7) }  = i_{+4} &= -\frac{3\sqrt{7} }{16}\,N_i\left(x^4-6x^2y^2+y^4\right)\left(11z^2-r^2\right)R_i(r) \\
    i^{(8) }  = i_{-4} &= -\frac{3\sqrt{7} }{4}\,N_i\,xy\left(x^2-y^2\right)\left(11z^2-r^2\right)R_i(r) \\
    i^{(9) }  = i_{+5} &= \frac{3\sqrt{154} }{16}\,N_i\,x\left(x^4-10x^2y^2+5y^4\right)z\,R_i(r) \\
    i^{(10) } = i_{-5} &= \frac{3\sqrt{154} }{16}\,N_i\,y\left(5x^4-10x^2y^2+y^4\right)z\,R_i(r) \\
    i^{(11) } = i_{+6} &= \frac{\sqrt{462} }{32}\,N_i\left(x^2-y^2\right)\left(x^4-14x^2y^2+y^4\right)R_i(r) \\
    i^{(12) } = i_{-6} &= \frac{\sqrt{462} }{16}\,N_i\,xy\left(x^2-3y^2\right)\left(3x^2-y^2\right)R_i(r)
  \end{aligned}
$$

### Angular momentum $k$ ($l = 7$)

Note that in ORCA 6.0 and earlier, basis functions of angular momentum quantum number 7
had the label $j$, in contrast to the usual convention in spectroscopy where the letter
$j$ is skipped. This inconsistency has been corrected in the ORCA 6.1 release.

$$
\begin{aligned}
N_k &= \frac{1}{2}\sqrt{\frac{15}{\pi} } \\
k^{(0) }  = k_{0\phantom{+} } &= \frac{1}{16}\,N_k\,z\left(429z^6-693z^4r^2+315z^2r^4-35r^6\right)R_k(r) \\
k^{(1) }  = k_{+1} &= \frac{\sqrt{7} }{32}\,N_k\,x\left(429z^6-495z^4r^2+135z^2r^4-5r^6\right)R_k(r) \\
k^{(2) }  = k_{-1} &= \frac{\sqrt{7} }{32}\,N_k\,y\left(429z^6-495z^4r^2+135z^2r^4-5r^6\right)R_k(r) \\
k^{(3) }  = k_{+2} &= \frac{\sqrt{42} }{32}\,N_k\left(x^2-y^2\right)z\left(143z^4-110z^2r^2+15r^4\right)R_k(r) \\
k^{(4) }  = k_{-2} &= \frac{\sqrt{42} }{16}\,N_k\,xyz\left(143z^4-110z^2r^2+15r^4\right)R_k(r) \\
k^{(5) }  = k_{+3} &= -\frac{\sqrt{21} }{32}\,N_k\,x\left(x^2-3y^2\right)\left(143z^4-66z^2r^2+3r^4\right)R_k(r) \\
k^{(6) }  = k_{-3} &= -\frac{\sqrt{21} }{32}\,N_k\,y\left(3x^2-y^2\right)\left(143z^4-66z^2r^2+3r^4\right)R_k(r) \\
k^{(7) }  = k_{+4} &= -\frac{\sqrt{231} }{16}\,N_k\left(x^4-6x^2y^2+y^4\right)z\left(13z^2-3r^2\right)R_k(r) \\
k^{(8) }  = k_{-4} &= -\frac{\sqrt{231} }{4}\,N_k\,xy\left(x^2-y^2\right)z\left(13z^2-3r^2\right)R_k(r) \\
k^{(9) }  = k_{+5} &= \frac{\sqrt{231} }{32}\,N_k\,x\left(x^4-10x^2y^2+5y^4\right)\left(13z^2-r^2\right)R_k(r) \\
k^{(10) } = k_{-5} &= \frac{\sqrt{231} }{32}\,N_k\,y\left(5x^4-10x^2y^2+y^4\right)\left(13z^2-r^2\right)R_k(r) \\
k^{(11) } = k_{+6} &= \frac{\sqrt{6006} }{32}\,N_k\left(x^2-y^2\right)\left(x^4-14x^2y^2+y^4\right)z\,R_k(r) \\
k^{(12) } = k_{-6} &= \frac{\sqrt{6006} }{16}\,N_k\,xy\left(x^2-3y^2\right)\left(3x^2-y^2\right)z\,R_k(r) \\
k^{(13) } = k_{+7} &= -\frac{\sqrt{429} }{32}\,N_k\,x\left(x^6-21x^4y^2+35x^2y^4-7y^6\right)R_k(r) \\
k^{(14) } = k_{-7} &= -\frac{\sqrt{429} }{32}\,N_k\,y\left(7x^6-35x^4y^2+21x^2y^4-y^6\right)R_k(r)
  \end{aligned}
$$

### Angular momentum $l$ ($l = 8$)

Note that in ORCA 6.0 and earlier, basis functions of angular momentum quantum number 8
were never actually supported. The likely result when attempting to use them was a crash.

Also note that the symbol $l$ is reserved in basis set files for $sp$ shells that have
a common set of Gaussian exponents. Thus for angular momentum 8 and higher, the numerical
value needs to be used instead of the letter.

$$
\begin{aligned}
N_l &= \frac{1}{2}\sqrt{\frac{17}{\pi} } \\
l^{(0) }  = l_{0\phantom{+} } &= \frac{1}{128}\,N_l\left(6435z^8-12012z^6r^2+6930z^4r^4-1260z^2r^6+35r^8\right)R_l(r) \\
l^{(1) }  = l_{+1} &= \frac{3}{32}\,N_l\,xz\left(715z^6-1001z^4r^2+385z^2r^4-35r^6\right)R_l(r) \\
l^{(2) }  = l_{-1} &= \frac{3}{32}\,N_l\,yz\left(715z^6-1001z^4r^2+385z^2r^4-35r^6\right)R_l(r) \\
l^{(3) }  = l_{+2} &= \frac{3\sqrt{70} }{64}\,N_l\left(x^2-y^2\right)\left(143z^6-143z^4r^2+33z^2r^4-r^6\right)R_l(r) \\
l^{(4) }  = l_{-2} &= \frac{3\sqrt{70} }{32}\,N_l\,xy\left(143z^6-143z^4r^2+33z^2r^4-r^6\right)R_l(r) \\
l^{(5) }  = l_{+3} &= -\frac{\sqrt{1155} }{32}\,N_l\,x\left(x^2-3y^2\right)z\left(39z^4-26z^2r^2+3r^4\right)R_l(r) \\
l^{(6) }  = l_{-3} &= -\frac{\sqrt{1155} }{32}\,N_l\,y\left(3x^2-y^2\right)z\left(39z^4-26z^2r^2+3r^4\right)R_l(r) \\
l^{(7) }  = l_{+4} &= -\frac{3\sqrt{77} }{64}\,N_l\,\left(x^4-6x^2y^2+y^4\right)\left(65z^4-26z^2r^2+r^4\right)R_l(r) \\
l^{(8) }  = l_{-4} &= -\frac{3\sqrt{77} }{16}\,N_l\,xy\left(x^2-y^2\right)\left(65z^4-26z^2r^2+r^4\right)R_l(r) \\
l^{(9) }  = l_{+5} &= \frac{3\sqrt{1001} }{32}\,N_l\,x\left(x^4-10x^2y^2+5y^4\right)z\left(5z^2-r^2\right)R_l(r) \\
l^{(10) } = l_{-5} &= \frac{3\sqrt{1001} }{32}\,N_l\,y\left(5x^4-10x^2y^2+y^4\right)z\left(5z^2-r^2\right)R_l(r) \\
l^{(11) } = l_{+6} &= \frac{\sqrt{858} }{64}\,N_l\left(x^2-y^2\right)\left(x^4-14x^2y^2+y^4\right)\left(15z^2-r^2\right)R_l(r) \\
l^{(12) } = l_{-6} &= \frac{\sqrt{858} }{32}\,N_l\,xy\left(x^2-3y^2\right)\left(3x^2-y^2\right)\left(15z^2-r^2\right)R_l(r) \\
l^{(13) } = l_{+7} &= -\frac{3\sqrt{715} }{32}\,N_l\,x\left(x^6-21x^4y^2+35x^2y^4-7y^6\right)z\,R_l(r) \\
l^{(14) } = l_{-7} &= -\frac{3\sqrt{715} }{32}\,N_l\,y\left(7x^6-35x^4y^2+21x^2y^4-y^6\right)z\,R_l(r) \\
l^{(15) } = l_{+8} &= -\frac{3\sqrt{715} }{128}\,N_l\left(x^8-28x^6y^2+70x^4y^4-28x^2y^6+y^8\right)R_l(r) \\
l^{(16) } = l_{-8} &= -\frac{3\sqrt{715} }{16}\,N_l\,xy\left(x^2-y^2\right)\left(x^4-6x^2y^2+y^4\right)R_l(r)
  \end{aligned}
$$

### Angular momentum $m$ ($l = 9$)

Please note that the symmetry module is currently still restricted to
a maximum angular momentum quantum number of 8.

$$
\begin{aligned}
N_m &= \frac{1}{2}\sqrt{\frac{19}{\pi} } \\
m^{(0) }  = m_{0\phantom{+} } &= \frac{1}{128}\,N_m\,z\left(12155z^8-25740z^6r^2+18018z^4r^4-4620z^2r^6+315r^8\right)R_m \\
m^{(1) }  = m_{+1} &= \frac{3\sqrt{5}}{128}\,N_m\,x\left(2431z^8-4004z^6r^2+2002z^4r^4-308z^2r^6+7r^8\right)R_m \\
m^{(2) }  = m_{-1} &= \frac{3\sqrt{5}}{128}\,N_m\,y\left(2431z^8-4004z^6r^2+2002z^4r^4-308z^2r^6+7r^8\right)R_m \\
m^{(3) }  = m_{+2} &= \frac{3\sqrt{110}}{64}\,N_m\bigl(x^2-y^2\bigr)z\left(221z^6-273z^4r^2+91z^2r^4-7r^6\right)R_m \\
m^{(4) }  = m_{-2} &= \frac{3\sqrt{110}}{32}\,N_m\,xyz\left(221z^6-273z^4r^2+91z^2r^4-7r^6\right)R_m \\
m^{(5) }  = m_{+3} &= \frac{\sqrt{2310}}{128}\,N_m\,x\left(x^2-3y^2\right)\left(221z^6-195z^4r^2+39z^2r^4-r^6\right)R_m \\
m^{(6) }  = m_{-3} &= \frac{\sqrt{2310}}{128}\,N_m\,y\left(3x^2-y^2\right)\left(221z^6-195z^4r^2+39z^2r^4-r^6\right)R_m \\
m^{(7) }  = m_{+4} &= \frac{3\sqrt{5005}}{64}\,N_m\left(x^4-6x^2y^2+y^4\right)z\left(17z^4-10z^2r^2+r^4\right)R_m \\
m^{(8) }  = m_{-4} &= \frac{3\sqrt{5005}}{16}\,N_m\,xy\left(x^2-y^2\right)z\left(17z^4-10z^2r^2+r^4\right)R_m \\
m^{(9) }  = m_{+5} &= \frac{3\sqrt{286}}{128}\,N_m\,x\left(x^4-10x^2y^2+5y^4\right)\left(85z^4-30z^2r^2+r^4\right)R_m \\
m^{(10)}  = m_{-5} &= \frac{3\sqrt{286}}{128}\,N_m\,y\left(5x^4-10x^2y^2+y^4\right)\left(85z^4-30z^2r^2+r^4\right)R_m \\
m^{(11)}  = m_{+6} &= \frac{\sqrt{4290}}{64}\,N_m\left(x^2-y^2\right)\left(x^4-14x^2y^2+y^4\right)z\left(17z^2-3r^2\right)R_m \\
m^{(12)}  = m_{-6} &= \frac{\sqrt{4290}}{32}\,N_m\,xy\left(x^2-3y^2\right)\left(3x^2-y^2\right)z\left(17z^2-3r^2\right)R_m \\
m^{(13)}  = m_{+7} &= \frac{3\sqrt{1430}}{256}\,N_m\,x\left(x^6-21x^4y^2+35x^2y^4-7y^6\right)\left(17z^2-r^2\right)R_m \\
m^{(14)}  = m_{-7} &= \frac{3\sqrt{1430}}{256}\,N_m\,y\left(7x^6-35x^4y^2+21x^2y^4-y^6\right)\left(17z^2-r^2\right)R_m \\
m^{(15)}  = m_{+8} &= \frac{3\sqrt{12155}}{128}\,N_m\left(x^8-28x^6y^2+70x^4y^4-28x^2y^6+y^8\right)zR_m \\
m^{(16)}  = m_{-8} &= \frac{3\sqrt{12155}}{16}\,N_m\,xy\left(x^2-y^2\right)\left(x^4-6x^2y^2+y^4\right)zR_m \\
m^{(17)}  = m_{+9} &= \frac{\sqrt{24310}}{256}\,N_m\,x\left(x^2-3y^2\right)\left(x^6-33x^4y^2+27x^2y^4-3y^6\right)R_m \\
m^{(18)}  = m_{-9} &= \frac{\sqrt{24310}}{256}\,N_m\,y\left(3x^2-y^2\right)\left(3x^6-27x^4y^2+33x^2y^4-y^6\right)R_m
  \end{aligned}
$$

### Angular momentum $n$ ($l = 10$)

Please note that the symmetry module is currently still restricted to
a maximum angular momentum quantum number of 8.

$$
\begin{aligned}
N_n &= \frac{1}{2}\sqrt{\frac{21}{\pi} } \\
n^{(0) }  = n_{0\phantom{+0}} &= \frac{1}{256}\,N_n\left(46189z^{10}-109395z^8r^2+90090z^6r^4-30030z^4r^6+3465z^2r^8-63r^{10}\right)R_n \\
n^{(1) }  = n_{+1\phantom{0}} &= \frac{\sqrt{55}}{128}\,N_n\,xz\left(4199z^8-7956z^6r^2+4914r^4z^4-1092z^2r^6+63r^8\right)R_n \\
n^{(2) }  = n_{-1\phantom{0}} &= \frac{\sqrt{55}}{128}\,N_n\,yz\left(4199z^8-7956z^6r^2+4914r^4z^4-1092z^2r^6+63r^8\right)R_n \\
n^{(3) }  = n_{+2\phantom{0}} &= \frac{\sqrt{165}}{256}\,N_n\left(x^2-y^2\right)\left(4199z^8-6188z^6r^2+2730z^4r^4-364z^2r^6+7r^8\right)R_n \\
n^{(4) }  = n_{-2\phantom{0}} &= \frac{\sqrt{165}}{128}\,N_n\,xy\left(4199z^8-6188z^6r^2+2730z^4r^4-364z^2r^6+7r^8\right)R_n \\
n^{(5) }  = n_{+3\phantom{0}} &= \frac{\sqrt{4290}}{128}\,N_n\,x\left(x^2-3y^2\right)z\left(323z^6-357z^4r^2+105z^2r^4-7r^6\right)R_n \\
n^{(6) }  = n_{-3\phantom{0}} &= \frac{\sqrt{4290}}{128}\,N_n\,y\left(3x^2-y^2\right)z\left(323z^6-357z^4r^2+105z^2r^4-7r^6\right)R_n \\
n^{(7) }  = n_{+4\phantom{0}} &= \frac{\sqrt{2145}}{128}\,N_n\left(x^4-6x^2y^2+y^4\right)\left(323z^6-255z^4r^2+45z^2r^4-r^6\right)R_n \\
n^{(8) }  = n_{-4\phantom{0}} &= \frac{\sqrt{2145}}{32}\,N_n\,xy\left(x^2-y^2\right)\left(323z^6-255z^4r^2+45z^2r^4-r^6\right)R_n \\
n^{(9) }  = n_{+5\phantom{0}} &= \frac{\sqrt{858}}{128}\,N_n\,x\left(x^4-10x^2y^2+5y^4\right)z\left(323z^4-170z^2r^2+15r^4\right)R_n \\
n^{(10)}  = n_{-5\phantom{0}} &= \frac{\sqrt{858}}{128}\,N_n\,y\left(5x^4-10x^2y^2+y^4\right)z\left(323z^4-170z^2r^2+15r^4\right)R_n \\
n^{(11)}  = n_{+6\phantom{0}} &= \frac{\sqrt{4290}}{512}\,N_n\left(x^2-y^2\right)\left(x^4-14x^2y^2+y^4\right)\bigl(323z^4-102z^2r^2+3r^4\bigr)R_n \\
n^{(12)}  = n_{-6\phantom{0}} &= \frac{\sqrt{4290}}{256}\,N_n\,xy\left(x^2-3y^2\right)\left(3x^2-y^2\right)\bigl(323z^4-102z^2r^2+3r^4\bigr)R_n \\
n^{(13)}  = n_{+7\phantom{0}} &= \frac{\sqrt{72930}}{256}\,N_n\,x\left(x^6-21x^4y^2+35x^2y^4-7y^6\right)z\left(19z^2-3r^2\right)R_n \\
n^{(14)}  = n_{-7\phantom{0}} &= \frac{\sqrt{72930}}{256}\,N_n\,y\left(7x^6-35x^4y^2+21x^2y^4-y^6\right)z\left(19z^2-3r^2\right)R_n \\
n^{(15)}  = n_{+8\phantom{0}} &= \frac{\sqrt{12155}}{256}\,N_n\left(x^8-28x^6y^2+70x^4y^4-28x^2y^6+y^8\right)\left(19z^2-r^2\right)R_n \\
n^{(16)}  = n_{-8\phantom{0}} &= \frac{\sqrt{12155}}{32}\,N_n\,xy\left(x^2-y^2\right)\left(x^4-6x^2y^2+y^4\right)\left(19z^2-r^2\right)R_n \\
n^{(17)}  = n_{+9\phantom{0}} &= \frac{\sqrt{461890}}{256}\,N_n\,x\left(x^2-3y^2\right)\left(x^6-33x^4y^2+27x^2y^4-3y^6\right)zR_n \\
n^{(18)}  = n_{-9\phantom{0}} &= \frac{\sqrt{461890}}{256}\,N_n\,y\left(3x^2-y^2\right)\left(3x^6-27x^4y^2+33x^2y^4-y^6\right)zR_n \\
n^{(19)}  = n_{+10}           &= \frac{\sqrt{92378}}{512}\,N_n\left(x^2-y^2\right)\left(x^8-44x^6y^2+166x^4y^4-44x^2y^6+y^8\right)R_n \\
n^{(20)}  = n_{-10}           &= \frac{\sqrt{92378}}{256}\,N_n\,xy\left(x^4-10x^2y^2+5y^4\right)\left(5x^4-10x^2y^2+y^4\right)R_n
  \end{aligned}
$$
