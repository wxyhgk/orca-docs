<a id="sec:essentialelements.basics"></a>
# Basic Calculation Settings

<a id="sec:essentialelements.basics.runtypes"></a>
## Run Types

The type of calculation to be performed can be chosen
via the simple input -- for example, `! Opt` --
or via the `RunTyp` variable in `%method`:

```orca
%method
  RunTyp  Gradient  # Single point energy and gradient
end
```

The full list of available run types is given in
[basics.keywords](#sec:essentialelements.basics.keywords).
Note that some run types are triggered automatically under certain conditions
and cannot be requested explicitly via the `RunTyp` keyword.

<a id="sec:essentialelements.basics.hamiltonians"></a>
## Method Classes
ORCA provides several classes of methods:
Hartree--Fock (HF), Density functional theory (DFT),
semi-empirical methods based on the NDDO approach, etc.
This choice is controlled via the simple input, e.g. `!HF`,
or via the `method` variable in the `%method` block:

```orca
%method
  method DFT
end
```

The list of available methods is given in
[basics.keywords](#sec:essentialelements.basics.keywords).

<a id="sec:essentialelements.basics.keywords"></a>
## Keywords

<a id="tab:essentialelements.basics.keywords.simple"></a>
!!! note "Simple input keywords for basic calculation settings."
    | Keyword | Description |
    | --- | --- |
    | *Run Types* |  |
    | `Energy` | Single point energy calculation (Default. Aliases: `SinglePoint`, `SP`) |
    | `EnGrad` | Single point energy and gradient calculation (Alias: `EnergyGrad`) |
    | `Opt` | [Geometry optimization](../structurereactivity/optimizations.md#sec:structurereactivity.optimization), see also [tab:structurereactivity.optimization.keywords.simple](#tab:structurereactivity.optimization.keywords.simple) |
    | `MD` | [Molecular dynamics simulation](../moleculardynamics/moldyn.md#sec:moldyn) |
    | `CIM` | [Cluster-in-molecules](../modelchemistries/mdci.md#sec:modelchemistries.mdci.cim) calculation |
    | `PrintThermoChem` | [Thermochemistry calculation](../structurereactivity/thermochemistry.md#sec:structurereactivity.thermochemistry) from previously calculated Hessian |
    | `PropertiesOnly` | [Compute properties](../spectroscopyproperties/postHF_magprop.md#sec:spectroscopyproperties.properties.proponly) from previously calculated densities |
    | `Docker` | [Host-guest docking](../structurereactivity/docker.md#sec:structurereactivity.docker) |
    | `EDA` | [Energy decomposition analysis](../spectroscopyproperties/nocv.md#sec:spectroscopyproperties.nocv) |
    | `NMScan` | **Deprecated!** Normal mode scan (Alias: `NormalModeScan`) |
    | `NMGrad` | **Deprecated!** Normal mode gradient (Alias: `NMGradient`) |
    | `MTR` | **Deprecated!** Mode trajectory (Aliases: `MT`, `ModeTrajectory`) |
    | *Methods* |  |
    | `HF` | [Hartree--Fock](../modelchemistries/hartreefock.md#sec:essentialelements.hartreefock); `RHF`, `UHF`, and `ROHF` also set the [wavefunction type](../modelchemistries/hftype.md#sec:modelchemistries.hftype) |
    | `DFT` | [Density functional theory](../modelchemistries/DensityFunctionalTheory.md#sec:modelchemistries.dft); `RKS`, `UKS`, and `ROKS` also set the [wavefunction type](../modelchemistries/hftype.md#sec:modelchemistries.hftype) |
    | `<NDO-Method>` | [NDO](../modelchemistries/semiempirical.md#sec:modelchemistries.semiempirical.ndo)-based method keywords are given in [tab:modelchemistries.semiempirical.ndo.keywords.simple](#tab:modelchemistries.semiempirical.ndo.keywords.simple) |
    | `<XTB-Method>` | [Native xTB](../modelchemistries/semiempirical.md#sec:modelchemistries.semiempirical.nativextb)-based method keywords are given in [tab:modelchemistries.semiempirical.nativextb.keywords.simple](#tab:modelchemistries.semiempirical.nativextb.keywords.simple) |
    | `MM` | [Molecular mechanics](../modelchemistries/mm.md#sec:modelchemistries.mm.orca) |

<a id="tab:essentialelements.basics.keywords.block"></a>
!!! note "`%method` block input keywords for basic calculation settings."
    | Keyword | Options | Description |
    | --- | --- | --- |
    | `RunTyp` | `Energy` | Single point energy calculation (Default. Aliases: `SinglePoint`, `SP`) |
    |  | `Gradient` | Single point energy and gradient calculation |
    |  | `Opt` | [Geometry optimization](../structurereactivity/optimizations.md#sec:structurereactivity.optimization) (Aliases: `Geom`, `Geometry`, `GeometryOpt`) |
    |  | `Scan` | [Unrelaxed geometry parameter scan](coordinates.md#sec:essentialelements.coordinates.parascan) (Alias: `Trajectory`) |
    |  | `CIM` | [Cluster-in-molecules](../modelchemistries/mdci.md#sec:modelchemistries.mdci.cim) calculation |
    |  | `NMScan` | **Deprecated!** Normal mode scan (Alias: `NormalModeScan`) |
    |  | `NMGrad` | **Deprecated!** Normal mode gradient (Aliases: `NMGradient`, `NormalModeGradient`) |
    |  | `MTR` | **Deprecated!** Mode trajectory (Aliases: `MT`, `ModeTrajectory`) |
    | `Method` | `HF` | (Default) [Hartree--Fock](../modelchemistries/hartreefock.md#sec:essentialelements.hartreefock) |
    |  | `DFT` | [Density functional theory](../modelchemistries/DensityFunctionalTheory.md#sec:modelchemistries.dft) |
    |  | `<NDO-Method>` | [NDO](../modelchemistries/semiempirical.md#sec:modelchemistries.semiempirical.ndo)-based method options are given in [tab:modelchemistries.semiempirical.ndo.keywords.block](#tab:modelchemistries.semiempirical.ndo.keywords.block) |
