<a id="sec:essentialelements.output"></a>
# Control of Output

ORCA provides various options to control the amount of printed output.
This is specifically important as some methods and protocols can create
very large amount of output and data. General control of the output is provided
by the `PrintLevel` and `Print[<option>]` keywords in the `%output` block:
`PrintLevel` can be used to select certain default settings for the print array. Specifying `Print` after `PrintLevel` can
be used to modify these defaults.

```orca
%output
  PrintLevel     Normal
  Print[ Flag ]  0  # turn print off
                 1  # turn print on
                 n  # some flags are more sophisticated
end
```

<a id="sec:essentialelements.printoptions"></a>
## Print Options

A detailed list of options for `PrintLevel` and `Print` is given in table [tab:essentialelements.output.printoptions.options](#tab:essentialelements.output.printoptions.options).
A list of option toggled by each printlevel can be found in [tab:essentialelements.output.printoptions.printleveldefaults](#tab:essentialelements.output.printoptions.printleveldefaults).

<a id="tab:essentialelements.output.printoptions.options"></a>
!!! note "`%output` block input keywords and options for print control."
    | Keyword                         | Option                    | Description                                            |
    |:--------------------------------|:--------------------------|:-------------------------------------------------------|
    | `PrintLevel`                    | `nothing`                 | Deactivates output printing                            |
    |                                 | `mini`                    | Sets printlevel to mini                                |
    |                                 | `small`                   | Sets printlevel to small                               |
    |                                 | `normal`                  | Sets printlevel to normal (default)                    |
    |                                 | `maxi`                    | Sets printlevel to maxi                                |
    |                                 | `large`                   | Sets printlevel to large                               |
    |                                 | `huge`                    | Sets printlevel to huge                                |
    |                                 | `debug`                   | Sets printlevel to debug                               |
    | `Print[ <option> ]`             | `P_InputFile`             | Echo the input file                                    |
    |                                 | `P_Cartesian`             | Print the cartesian coordinates                        |
    |                                 | `P_Internal`              | Print the internal coordinates                         |
    |                                 | `P_Basis`                 | $=1:$ Print the basis set information                  |
    |                                 |                           | $=2:$ Also print the primitives in input format        |
    |                                 | `P_OneElec`               | Print of the one electron matrix                       |
    |                                 | `P_Overlap`               | Print the overlap matrix                               |
    |                                 | `P_KinEn`                 | Print the kinetic energy matrix                        |
    |                                 | `P_S12`                   | Print the S$^{-1/2}$ matrix                            |
    |                                 | `P_GuessOrb`              | Print the initial guess orbitals                       |
    |                                 | `P_OrbEn`                 | $=1:$ Print orbital energies up to LUMO+9              |
    |                                 |                           | $=2:$ Print all orbital energies                       |
    |                                 | `P_MOs`                   | Print the MO coefficients on convergence               |
    |                                 | `P_Density`               | Print the converged electron density                   |
    |                                 | `P_SpinDensity`           | Print the converged spin density                       |
    |                                 | `P_EHTDetails`            | Print initial guess extended Hückel details            |
    |                                 | `P_SCFInfo`               | Print the SCF input flags                              |
    |                                 | `P_SCFMemInfo`            | Print the estimated SCF memory requirements            |
    |                                 | `P_SCFIterInfo`           | $=1:$ Print short iteration information                |
    |                                 |                           | $=2:$ Print longer iteration information               |
    |                                 |                           | $=3:$ In a direct SCF also print integral progress     |
    |                                 | `P_Fockian`               | Print Fockian matrix                                   |
    |                                 | `P_DIISMat`               | Print DIIS matrix                                      |
    |                                 | `P_DIISError`             | Print DIIS error                                       |
    |                                 | `P_Iter_P`                | Print Density                                          |
    |                                 | `P_Iter_C`                | Print MO coefficients                                  |
    |                                 | `P_Iter_F`                | Print Fock matrix                                      |
    |                                 | `P_Mayer`                 | Print Mayer population analysis (Default = on)         |
    |                                 | `P_NatPop`                | Print Natural population analysis (Default = off)      |
    |                                 | `P_NPA`                   | Print Natural population analysis (Default = off)      |
    |                                 | `P_Hirshfeld`             | Print Hirshfeld population analysis (Default = off)    |
    |                                 | `P_MBIS`                  | Print MBIS population analysis (Default = off)         |
    |                                 | `P_Mulliken`              | Print Mulliken population analysis (Default = on)      |
    |                                 | `P_AtCharges_M`           | Print Mulliken atomic charges                          |
    |                                 | `P_OrbCharges_M`          | Print Mulliken orbital charges                         |
    |                                 | `P_FragCharges_M`         | Print Mulliken fragment charges                        |
    |                                 | `P_FragBondOrder_M`       | Print Mulliken fragment bond orders                    |
    |                                 | `P_BondOrder_M`           | Print Mulliken bond orders                             |
    |                                 | `P_ReducedOrbPop_M`       | Print Mulliken reduced orbital charges                 |
    |                                 | `P_FragPopMO_M`           | Print Mulliken fragment population for each MO         |
    |                                 | `P_FragOvlMO_M`           | Print Mulliken overlap populations per fragment pair   |
    |                                 | `P_AtPopMO_M`             | Print Mulliken atomic charges in each MO               |
    |                                 | `P_OrbPopMO_M`            | Print Mulliken orbital population for each MO          |
    |                                 | `P_ReducedOrbPopMO_M`     | Print Mulliken reduced orbital population for each MO  |
    |                                 | `P_Loewdin`               | Print Loewdin population analysis (Default = on)       |
    |                                 | `P_AtCharges_L`           | Print Loewdin atomic charges                           |
    |                                 | `P_OrbCharges_L`          | Print Loewdin orbital charges                          |
    |                                 | `P_FragCharges_L`         | Print Loewdin fragment charges                         |
    |                                 | `P_FragBondOrder_L`       | Print Loewdin fragment bond orders                     |
    |                                 | `P_BondOrder_L`           | Print Loewdin bond orders                              |
    |                                 | `P_ReducedOrbPop_L`       | Print Loewdin reduced orbital charges                  |
    |                                 | `P_FragPopMO_L`           | Print Loewdin fragment population for each MO          |
    |                                 | `P_FragOvlMO_L`           | Print Loewdin overlap populations per fragment pair    |
    |                                 | `P_AtPopMO_L`             | Print Loewdin atomic charges in each MO                |
    |                                 | `P_OrbPopMO_L`            | Print Loewdin orbital population for each MO           |
    |                                 | `P_ReducedOrbPopMO_L`     | Print Loewdin reduced orbital population for each MO   |
    |                                 | `P_NPA`                   | Natural population analysis                            |
    |                                 | `P_Fragments`             | Print fragment information                             |
    |                                 | `P_GUESSPOP`              | Print initial guess populations                        |
    |                                 | `P_UNO_FragPopMO_M`       | Print Mulliken fragment population per UNO                      |
    |                                 | `P_UNO_OrbPopMO_M`        | Print Mulliken orbital pop. per UNO                             |
    |                                 | `P_UNO_AtPopMO_M`         | Print Mulliken atomic charges per UNO                           |
    |                                 | `P_UNO_ReducedOrbPopMO_M` | Print Mulliken reduced orbital pop. per UNO                     |
    |                                 | `P_UNO_FragPopMO_L`       | Print Loewdin fragment population per UNO                       |
    |                                 | `P_UNO_OrbPopMO_L`        | Print Loewdin orbital pop. per UNO                              |
    |                                 | `P_UNO_AtPopMO_L`         | Print Loewdin atomic charges per UNO                            |
    |                                 | `P_UNO_ReducedOrbPopMO_L` | Print Loewdin reduced orbital pop. per UNO                      |
    |                                 | `P_UNO_OccNum`            | Print occupation numbers per UNO                                |
    |                                 | `P_AtomExpVal`            | Print atomic expectation values                                 |
    |                                 | `P_AtomBasis`             | Print atomic basis                                              |
    |                                 | `P_AtomDensFit`           | Print electron density fit                                      |
    |                                 | `P_Symmetry`              | Symmetry basic information                                      |
    |                                 | `P_Sym_Salc`              | Symmetry process printing                                       |
    |                                 | `P_SCFSTABANA`            | Information on progress, convergence, and results of SCF stability analysis |
    |                                 | `P_DFTD`                  | Print info on Grimme's dispersion correction                    |
    |                                 | `P_DFTD_GRAD`             | Print gradient info on Grimme's dispersion correction           |
    |                                 | `P_G1EL2EL`               | Print one- and two-electron contributions to g-tensor           |

The various choices for PrintLevel have the following defaults:

<a id="tab:essentialelements.output.printoptions.printleveldefaults"></a>
!!! note "Default print options invoked by the respective `PrintLevel`."
    | PrintLevel | Print options included   |        |
    |:-----------|:-------------------------|:-------|
    | `mini`     | `P_OrbEn`                | `= 1`  |
    |            | `P_Cartesian`            | `= 1`  |
    |            | `P_InputFile`            | `= 1`  |
    |            | `P_SCFIterInfo`          | `= 1`  |
    | `small`    | all the previous plus    |        |
    |            | `P_SCFInfo`              | `= 1`  |
    |            | `P_Mayer`                | `= 1`  |
    |            | `P_MULLIKEN`             | `= 1`  |
    |            | `P_AtCharges_M`          | `= 1`  |
    |            | `P_ReducedOrbPop_M`      | `= 1`  |
    |            | `P_Loewdin `             | `= 1`  |
    |            | `P_AtCharges_L`          | `= 1`  |
    |            | `P_ReducedOrbPop_L`      | `= 1`  |
    |            | `P_Fragments`            | `= 1`  |
    |            | `P_FragCharges_M`        | `= 1`  |
    |            | `P_FragBondOrder_M`      | `= 1`  |
    |            | `P_FragCharges_L`        | `= 1`  |
    |            | `P_FragBondOrder_L`      | `= 1`  |
    |            | `P_DFTD`                 | `= 1`  |
    | `normal`   | all the previous plus    |        |
    |            | `P_Internal`             | `= 1`  |
    |            | `P_BondOrder_L`          | `= 1`  |
    |            | `P_BondOrder_M`          | `= 1`  |
    |            | `P_FragPopMO_L`          | `= 1`  |
    |            | `P_ReducedOrbPopMO_L`    | `= 1`  |
    |            | `P_SCFIterInfo`          | `= 2 ` |
    | `maxi`     | all the previous plus    |        |
    |            | `P_OrbEn`                | `= 2`  |
    |            | `P_GuessOrb`             | `= 1`  |
    |            | `P_MOs`                  | `= 1`  |
    |            | `P_Density`              | `= 1`  |
    |            | `P_SpinDensity`          | `= 1`  |
    |            | `P_Basis`                | `= 1`  |
    |            | `P_FragOVLMO_M `         | `= 1`  |
    |            | `P_OrbPopMO_M`           | `= 1`  |
    |            | `P_OrbCharges_M`         | `= 1`  |
    |            | `P_DFTD`                 | `= 2`  |
    |            | `P_DFTD_GRAD`            | `= 1`  |
    | `huge`     |  All the previous plus   |        |
    |            | `P_OneElec`              | `= 1`  |
    |            | `P_Overlap`              | `= 1 ` |
    |            | `P_S12`                  | `= 1`  |
    |            | `P_AtPopMO_M`            | `= 1`  |
    |            | `P_OrbPopMO_M`           | `= 1`  |
    |            | `P_AtPopMO_L`            | `= 1`  |
    |            | `P_EHTDetails`           | `= 1`  |
    |            | `P_DFTD_GRAD`            | `= 2`  |
    | `debug`    | Prints everything        |        |

<a id="sec:essentialelements.output.simplekeywords"></a>
## Simple Input Keywords

For convenience, a variety of simple input keywords that control specific print settings and additional outputs
have been implemented as well (cf. [tab:essentialelements.output.simplekeywords.keywords](#tab:essentialelements.output.simplekeywords.keywords)).

<a id="tab:essentialelements.output.simplekeywords.keywords"></a>
!!! note "Simple input keywords for specific output control."
    | Keyword                         | Print options toggled     | Description                                                        |
    |:--------------------------------|:--------------------------|:-------------------------------------------------------------------|
    | `MiniPrint`                     | `PrintLevel mini`         | Activates printlevel mini                                          |
    | `SmallPrint`                    | `PrintLevel small`        | Activates printlevel small (default)                               |
    | `NormalPrint`                   | `PrintLevel normal`       | Activates printlevel normal                                        |
    | `LargePrint`                    | `PrintLevel large`        | Activates printlevel mini                                          |
    | `PrintMOs`                      | `Print[ p_MOs ]`          | Prints MO coefficients                                             |
    | `NoPrintMOs`                    |                           | Suppress printing of MO coefficients                               |
    | `PrintBasis`                    | `Print[ p_basis ]`        | Print the basis set in input format                                |
    | `PrintGap`                      | `Print[ p_homolumogap ]`  | Prints the HOMO/LUMO gap in each SCF iteration.                    |
    | `ReducedPop`                    |                           | Prints Loewdin reduced orb.pop per MO                              |
    | `NoReducedPop`                  |                           | Deactivates printing of Loewdin reduced orb.pop per MO             |
    | `AIM`                           |                           | Produce a WFN file                                                 |
    | `XYZFILE`                       |                           | Produce an XYZ coordinate file                                     |
    | `PDBFILE`                       |                           | Produce a PDB file                                                 |
    | `UNO`                           |                           | Produce a [UHF natural orbitals](../modelchemistries/hftype.md#sec:modelchemistries.hftype.uhfno)|
    | `NoPropFile`                    |                           | Do not write to the [property file](../utilitiesvisualization/property_file.md#sec:property_file.detailed)    |
    | `KeepTransDensity`              |                           | Keep the transition density matrices on disk                       |

