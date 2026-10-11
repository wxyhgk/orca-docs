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
[sec:essentialelements.basics.keywords](#sec:essentialelements.basics.keywords).
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
[sec:essentialelements.basics.keywords](#sec:essentialelements.basics.keywords).

<a id="sec:essentialelements.basics.keywords"></a>
## Keywords

<a id="tab:essentialelements.basics.keywords.simple"></a>
!!! note "Simple input keywords for basic calculation settings."
    :class: footnotesize
    :header-rows: 1

| Item | Value |
| --- | --- |
| **Keyword** | — |

      - Description

| Item | Value |
| --- | --- |
| **{cspan}`1` *Run Types*** | — |
| **`Energy`** | — |

      - Single point energy calculation (Default. Aliases: `SinglePoint`, `SP`)

| Item | Value |
| --- | --- |
| **`EnGrad`** | — |

      - Single point energy and gradient calculation (Alias: `EnergyGrad`)

| Item | Value |
| --- | --- |
| **`Opt`** | — |

      - [Geometry optimization](sec:structurereactivity.optimization),
        see also [tab:structurereactivity.optimization.keywords.simple](#tab:structurereactivity.optimization.keywords.simple)

| Item | Value |
| --- | --- |
| **`MD`** | — |

      - [Molecular dynamics simulation](sec:moldyn)

| Item | Value |
| --- | --- |
| **`CIM`** | — |

      - [Cluster-in-molecules](sec:modelchemistries.mdci.cim) calculation

| Item | Value |
| --- | --- |
| **`PrintThermoChem`** | — |

      - [Thermochemistry calculation](sec:structurereactivity.thermochemistry) 
        from previously calculated Hessian

| Item | Value |
| --- | --- |
| **`PropertiesOnly`** | — |

      - [Compute properties](sec:spectroscopyproperties.properties.proponly)
        from previously calculated densities

| Item | Value |
| --- | --- |
| **`Docker`** | — |

      - [Host-guest docking](sec:structurereactivity.docker)

| Item | Value |
| --- | --- |
| **`EDA`** | — |

      - [Energy decomposition analysis](sec:spectroscopyproperties.nocv)

| Item | Value |
| --- | --- |
| **`NMScan`** | — |

      - **Deprecated!** Normal mode scan (Alias: `NormalModeScan`)

| Item | Value |
| --- | --- |
| **`NMGrad`** | — |

      - **Deprecated!** Normal mode gradient (Alias: `NMGradient`)

| Item | Value |
| --- | --- |
| **`MTR`** | — |

      - **Deprecated!** Mode trajectory (Aliases: `MT`, `ModeTrajectory`) 

| Item | Value |
| --- | --- |
| **{cspan}`1` *Methods*** | — |
| **`HF`** | — |

      - [Hartree--Fock](sec:essentialelements.hartreefock);
        `RHF`, `UHF`, and `ROHF` also set the [wavefunction type](sec:modelchemistries.hftype)

| Item | Value |
| --- | --- |
| **`DFT`** | — |

      - [Density functional theory](sec:modelchemistries.dft);
        `RKS`, `UKS`, and `ROKS` also set the [wavefunction type](sec:modelchemistries.hftype)

| Item | Value |
| --- | --- |
| **`<NDO-Method>`** | — |

      - [NDO](sec:modelchemistries.semiempirical.ndo)-based method keywords are given in 
        [tab:modelchemistries.semiempirical.ndo.keywords.simple](#tab:modelchemistries.semiempirical.ndo.keywords.simple)

| Item | Value |
| --- | --- |
| **`<XTB-Method>`** | — |

      - [Native xTB](sec:modelchemistries.semiempirical.nativextb)-based method keywords are given in
        [tab:modelchemistries.semiempirical.nativextb.keywords.simple](#tab:modelchemistries.semiempirical.nativextb.keywords.simple)

| Item | Value |
| --- | --- |
| **`MM`** | — |

      - [Molecular mechanics](sec:modelchemistries.mm.orca)

<a id="tab:essentialelements.basics.keywords.block"></a>
!!! note "`%method` block input keywords for basic calculation settings."
    :class: footnotesize
    :header-rows: 1

| Item | Value |
| --- | --- |
| **Keyword** | — |

      - Options
      - Description

| Item | Value |
| --- | --- |
| **`RunTyp`** | — |

      - `Energy`
      - Single point energy calculation (Default. Aliases: `SinglePoint`, `SP`)

| Item | Value |
| --- | --- |
| **—** | — |

      - `Gradient`
      - Single point energy and gradient calculation 

| Item | Value |
| --- | --- |
| **—** | — |

      - `Opt`
      - [Geometry optimization](sec:structurereactivity.optimization) 
        (Aliases: `Geom`, `Geometry`, `GeometryOpt`)

| Item | Value |
| --- | --- |
| **—** | — |

      - `Scan`
      - [Unrelaxed geometry parameter scan](sec:essentialelements.coordinates.parascan)
        (Alias: `Trajectory`)

| Item | Value |
| --- | --- |
| **—** | — |

      - `CIM`
      - [Cluster-in-molecules](sec:modelchemistries.mdci.cim) calculation

| Item | Value |
| --- | --- |
| **—** | — |

      - `NMScan`
      - **Deprecated!** Normal mode scan (Alias: `NormalModeScan`)

| Item | Value |
| --- | --- |
| **—** | — |

      - `NMGrad`
      - **Deprecated!** Normal mode gradient (Aliases: `NMGradient`, `NormalModeGradient`)

| Item | Value |
| --- | --- |
| **—** | — |

      - `MTR`
      - **Deprecated!** Mode trajectory (Aliases: `MT`, `ModeTrajectory`) 

| Item | Value |
| --- | --- |
| **`Method`** | — |

      - `HF`
      - (Default) [Hartree--Fock](sec:essentialelements.hartreefock)

| Item | Value |
| --- | --- |
| **—** | — |

      - `DFT`
      - [Density functional theory](sec:modelchemistries.dft)

| Item | Value |
| --- | --- |
| **—** | — |

      - `<NDO-Method>`
      - [NDO](sec:modelchemistries.semiempirical.ndo)-based method options are given in 
        [tab:modelchemistries.semiempirical.ndo.keywords.block](#tab:modelchemistries.semiempirical.ndo.keywords.block)

