(sec:essentialelements.basics)=
# Basic Calculation Settings

(sec:essentialelements.basics.runtypes)=
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
{numref}`sec:essentialelements.basics.keywords`.
Note that some run types are triggered automatically under certain conditions
and cannot be requested explicitly via the `RunTyp` keyword.

(sec:essentialelements.basics.hamiltonians)=
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
{numref}`sec:essentialelements.basics.keywords`.

(sec:essentialelements.basics.keywords)=
## Keywords

:::{raw} latex
\begingroup
\footnotesize
:::

:::{tabularcolumns} \Y{0.3}\Y{0.7}
:::

(tab:essentialelements.basics.keywords.simple)=
:::{flat-table} Simple input keywords for basic calculation settings.
:class: footnotesize
:header-rows: 1
* - Keyword
  - Description
* - {cspan}`1` *Run Types*
* - `Energy`
  - Single point energy calculation (Default. Aliases: `SinglePoint`, `SP`)
* - `EnGrad`
  - Single point energy and gradient calculation (Alias: `EnergyGrad`)
* - `Opt`
  - [Geometry optimization](sec:structurereactivity.optimization),
    see also {numref}`tab:structurereactivity.optimization.keywords.simple`
* - `MD`
  - [Molecular dynamics simulation](sec:moldyn)
* - `CIM`
  - [Cluster-in-molecules](sec:modelchemistries.mdci.cim) calculation
* - `PrintThermoChem`
  - [Thermochemistry calculation](sec:structurereactivity.thermochemistry) 
    from previously calculated Hessian
* - `PropertiesOnly`
  - [Compute properties](sec:spectroscopyproperties.properties.proponly)
    from previously calculated densities
* - `Docker`
  - [Host-guest docking](sec:structurereactivity.docker)
* - `EDA`
  - [Energy decomposition analysis](sec:spectroscopyproperties.nocv)
* - `NMScan`
  - **Deprecated!** Normal mode scan (Alias: `NormalModeScan`)
* - `NMGrad`
  - **Deprecated!** Normal mode gradient (Alias: `NMGradient`)
* - `MTR`
  - **Deprecated!** Mode trajectory (Aliases: `MT`, `ModeTrajectory`) 
* - {cspan}`1` *Methods*
* - `HF`
  - [Hartree--Fock](sec:essentialelements.hartreefock);
    `RHF`, `UHF`, and `ROHF` also set the [wavefunction type](sec:modelchemistries.hftype)
* - `DFT`
  - [Density functional theory](sec:modelchemistries.dft);
    `RKS`, `UKS`, and `ROKS` also set the [wavefunction type](sec:modelchemistries.hftype)
* - `<NDO-Method>`
  - [NDO](sec:modelchemistries.semiempirical.ndo)-based method keywords are given in 
    {numref}`tab:modelchemistries.semiempirical.ndo.keywords.simple`
* - `<XTB-Method>`
  - [Native xTB](sec:modelchemistries.semiempirical.nativextb)-based method keywords are given in
    {numref}`tab:modelchemistries.semiempirical.nativextb.keywords.simple`
* - `MM`
  - [Molecular mechanics](sec:modelchemistries.mm.orca)
:::
:::{raw} latex
\endgroup
:::

:::{raw} latex
\begingroup
\footnotesize
:::

:::{tabularcolumns} \Y{0.1}\Y{0.2}\Y{0.7}
:::

(tab:essentialelements.basics.keywords.block)=
:::{flat-table} `%method` block input keywords for basic calculation settings.
:class: footnotesize
:header-rows: 1
* - Keyword
  - Options
  - Description
* - `RunTyp`
  - `Energy`
  - Single point energy calculation (Default. Aliases: `SinglePoint`, `SP`)
* - 
  - `Gradient`
  - Single point energy and gradient calculation 
* - 
  - `Opt`
  - [Geometry optimization](sec:structurereactivity.optimization) 
    (Aliases: `Geom`, `Geometry`, `GeometryOpt`)
* - 
  - `Scan`
  - [Unrelaxed geometry parameter scan](sec:essentialelements.coordinates.parascan)
    (Alias: `Trajectory`)
* - 
  - `CIM`
  - [Cluster-in-molecules](sec:modelchemistries.mdci.cim) calculation
* - 
  - `NMScan`
  - **Deprecated!** Normal mode scan (Alias: `NormalModeScan`)
* - 
  - `NMGrad`
  - **Deprecated!** Normal mode gradient (Aliases: `NMGradient`, `NormalModeGradient`)
* - 
  - `MTR`
  - **Deprecated!** Mode trajectory (Aliases: `MT`, `ModeTrajectory`) 
* - `Method`
  - `HF`
  - (Default) [Hartree--Fock](sec:essentialelements.hartreefock)
* - 
  - `DFT`
  - [Density functional theory](sec:modelchemistries.dft)
* - 
  - `<NDO-Method>`
  - [NDO](sec:modelchemistries.semiempirical.ndo)-based method options are given in 
    {numref}`tab:modelchemistries.semiempirical.ndo.keywords.block`
:::
:::{raw} latex
\endgroup
:::
