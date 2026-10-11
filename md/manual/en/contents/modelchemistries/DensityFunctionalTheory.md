```{index} Density Functional Theory, Density Functional Theory; DFT
```
(sec:modelchemistries.dft)=
# Density Functional Theory (DFT)

Due to its good cost-accuracy ratio, Kohn-Sham density functional theory (DFT) has become the workhorse of quantum chemistry. 
Over the last few decades, a whole zoo of density functionals has been developed that differ in terms of their construction and design philosophy.
The so-called Jacob's Ladder picture ({numref}`fig:modelchemistries.dft.jacobsladder`) coined by Perdew {cite}`perdew2001jacobsladder` categorizes density functionals according to their basic physical ingredients into rungs .
With higher rungs. the cost of the given functionals increased but also higher accuracy is conceptionally expected. 
However, the accuracy of density functionals strongly varies and careful study of benchmark studies is generally recommended.

(fig:modelchemistries.dft.jacobsladder)=
```{figure} ../../images/jacobsladder.*
:width: 400px
:align: center

Jacob's ladder picture of density functionals.
```

ORCA features various density functionals of each rung either implemented natively or via the {ref}`sec:modelchemistries.dft.libxc`.
These functionals can be combined with various [basis sets](../essentialelements/basisset.md) and [relativistic approaches](../essentialelements/relativistic.md).
Further, ORCA features a useful toolkit of [resolution-of-identity (RI)](../essentialelements/RI.md) methods to speed-up DFT calculations.

For dispersion corrections that can be used with DFT and the respective available functional-specific parameters refer to the [Dispersion Corrections section](../modelchemistries/dispersioncorrections.md).

Also note that some functionals like the SCAN and Minnesota families may require enhanced [numerical integration grid settings](../essentialelements/numericalintegration.md).


(sec:modelchemistries.dft.basicusage)=
## Basic Usage

All implemented DFT methods can be invoked via their respective keywords, e.g. `!PBE` using the simple input line:

```orca
! PBE
```
:::{warning}
If only a functional is defined, various default settings will be used including a small def2-SVP basis set, an appropriate [RI](../essentialelements/RI.md) treatment and default [numerical integration grids](../essentialelements/numericalintegration.md)! To achieve higher accuracy, specifically the [basis set](../essentialelements/basisset.md) should be adjusted!
:::

Many functionals can also be invoked via the `%method` block even though double-hybrid functionals being not available due to technical reasons:

```orca
%method
   Method DFT        # equivalent to method DFGTO
   Functional PBE
end
```

ORCA further provides some more utility to construct and modify functionals via the `%method` block. These expert options are described in the respective sections of each functional rung. Various other functionals can also be invoked via the {ref}`sec:modelchemistries.dft.libxc`.

:::{warning}
[RI](sec:essentialelements.ri)/[RIJCOSX](sec:essentialelements.ri.rijcosx) 
are only activated by default if a DFT functional is chosen in the simple input!
If the `%method` block is used instead,
these approximations should be specified explicitly via `!RI` or `!RIJCOSX`.
:::

```{index} Density Functional Theory; Local Functionals
```
(sec:modelchemistries.dft.local)=
## Local Functionals 

Local exchange-correlation functionals are the most basic examples of functionals constructed according to equation {eq}`eqn:modelchemistries.dft.gga.exlocal`:

$$E_{\text{XC} } = E_{\text{LSD} }^{\text{X} } + E_{\text{LSD} }^{\text{C} }
$$ (eqn:modelchemistries.dft.gga.exlocal)

They typically the original Slater exchange functional with different local correlations functionals like VWN-V{cite}`vosko1980can` or PW-LDA{cite}`perdew1992physb`.
All available local functional that are available in ORCA can be found in {numref}`tab:modelchemistries.dft.local`.

(tab:modelchemistries.dft.local)=
:::{table} List of available local functionals.
:class: footnotesize
| Functional                           | Keywords     | Description                                                 |
|:-------------------------------------|:-------------|:------------------------------------------------------------|
| HFS                                  | `HFS`        | Hartree--Fock--Slater Exchange only functional              |
| LDA or LSD                           | `LDA`, `LSD` | Local density approximation (defaults to VWN5)              |
| VWN-V {cite}`vosko1980can`           | `VWN`,`VWN5` | Vosko-Wilk-Nusair local density approx. parameter set "V"   |
| VWN-III {cite}`vosko1980can`         | `VWN3`       | Vosko-Wilk-Nusair local density approx. parameter set "III" |
| PW-LDA {cite}`perdew1992physb`       | `PWLDA`      | Perdew-Wang parameterization of LDA                         |
:::

```{index} Density Functional Theory; GGA, meta-GGA
```
(sec:modelchemistries.dft.gga)=
## Gradient Corrected Functionals: (meta-)GGAs

The next rung corresponds to gradient corrected functional of the generalized gradient approximation (GGA) and the meta-generalized gradient approximation (meta-GGA) types.
A simplified exchange-correlation energy expression for these types of functionals is given in {eq}`eqn:modelchemistries.dft.gga.excgga`. (meta-)GGAs are specifically useful for 
[geometry optimizations](../structurereactivity/optimizations.md) and screening purposes due to their comparably small computational cost.

$$E_{\text{XC} } = E_{\text{LSD} }^{\text{X} } + E_{\text{GGA} }^{\text{X} } + E_{\text{LSD} }^{\text{C} } + E_{\text{GGA} }^{\text{C} }
$$ (eqn:modelchemistries.dft.gga.excgga)

(tab:modelchemistries.dft.gga)=
:::{table} List of available (meta-)GGA functionals.
:class: footnotesize
| Functional      | Keyword | Description |
|:----------------|:--------|:------------|
| **GGAs** | | |
| BP86 {cite}`becke1988phys, perdew1986phys` | `BP86`       | Becke '88 exchange and Perdew '86 correlation  |
| BLYP {cite}`BLYP` | `BLYP`       | Becke '88 exchange and Lee-Yang-Parr correlation  |
| OLYP {cite}`handy2001molphys` | `OLYP`       | Handy's "optimal" exchange and Lee-Yang-Parr correlation  |
| GLYP {cite}`gill1996mol` | `GLYP`       | Gill's '96 exchange and Lee-Yang-Parr correlation  |
| XLYP {cite}`goddard2004pnas` | `XLYP`       | The Xu and Goddard exchange and Lee-Yang-Parr correlation  |
| PW91 {cite}`perdew1991pw91` | `PW91`       | Perdew-Wang '91 GGA functional  |
| mPWPW {cite}`barone1997jcp` | `MPWPW`      | Modified PW exchange and PW correlation  |
| mPWLYP {cite}`barone1997jcp` | `MPWLYP`     | Modified PW exchange and LYP correlation  |
| PBE {cite}`perdew1996phys` | `PBE`        | Perdew-Burke-Erzerhoff GGA functional  |
| RPBE {cite}`hammer1999phys` | `RPBE`      | "Modified" PBE  |
| revPBE {cite}`zhang1998phys` | `REVPBE`     | "Revised" PBE  |
| RPW86PBE {cite}`rPW86PBE` | `RPW86PBE`   | PBE correlation with refitted Perdew '86 exchange  |
| PWP {cite}`perdew1991pw91` | `PWP` | Perdew-Wang '91 exchange and Perdew '86 correlation  |
| **composite** | | |
| B97-3c {cite}`grimme2018b973c` | `B97-3C` | Composite DFT method by Grimme et al. |
| **meta-GGAs** | | |
| B97M-V {cite}`headgordon2015B97MV`    | `B97M-V` | Head-Gordon's DF B97M-V with VV10 nonlocal correlation  |
| B97M-D3(BJ) {cite}`goerigk2018` | `B97M-D3BJ` | Modified version of B97M-V with D3BJ correction by Najibi and Goerigk  |
| B97M-D4 {cite}`najibi2020`   | `B97M-D4` | Modified version of B97M-V with DFT-D4 correction by Najibi and Goerigk  |
| SCAN {cite}`perdew2015scan`  | `SCANFUNC` | Perdew's SCAN functional  |
| rSCAN {cite}`bartok2019rscan`     | `RSCAN` | Regularized SCAN functional
| r²SCAN {cite}`furness2020r2scan`      | `R2SCAN` | Regularized and restored SCAN functional by Furness, Sun et al.  |
| M06-L {cite}`m06l`      | `M06L` | The Minnesota M06-L meta-GGA functional  |
| TPSS {cite}`TPSS2003`       | `TPSS` | The TPSS meta-GGA functional  |
| revTPSS {cite}`revtpss, revtpsserratum`       | `REVTPSS` | Revised TPSS meta-GGA functional  |
| **composite** | | |
| r²SCAN-3c {cite}`grimme2020r2scan3c` | `R2SCAN-3C` | Composite DFT method by Grimme et al. |
:::

```{index} Density Functional Theory; Custom Functionals
```
(sec:modelchemistries.dft.gga.customizexc)=
### Customization of Basic Functionals

Basic exchange-correlation functionals can also be constructed from their components via the `%method` block using the `Exchange`, `Correlation`, and `LDAOpt` keywords.
These controle the exchange and correlation parts of the functional as well as the local part of the correlation functional, respectively.
For example BP86 (`!BP86`) is constructed from Becke's ‘88 exchange via `X_BECKE` and Perdew's ‘86 correlation functional via `C_P86`. In ORCA, it further
employs Perdew and Wang's LDA reparameterization{cite}`perdew1992physb` `PWLDA` for the local part of the correlation functional via `C_PWLDA`:

```orca
%method
   Method DFT
   Exchange     X_BECKE
   Correlation  C_P86
   LDAOpt       C_PWLDA
end
```

For a full list of available components see {numref}`tab:modelchemistries.dft.gga.customizexc.keywords.block`.

The correct choice of the local part of the correlation functional is crucial to ensure
reproducibility of the results. In ORCA, almost all functionals choose `PWLDA`{cite}`perdew1992physb` as the
underlying LDA functional as it represents a slightly better fit to
the uniform electron gas than VWN. For VWN (Vosko, Wilk, and Nusair{cite}`vosko1980can`), several parameterizations
exist. In their classic paper give two sets of parameters -- one in
the main body (parametrization of RPA results; known as VWN-III) and
one in their table 5 of correlation energies (parametrization of the
Ceperley/Alder Monte Carlo results; known as VWN-V). The results from PW-LDA are very similar to those
of VWN-V, whereas VWN-III yields quite different values.
Over the years, the usage of different parameterizations for the same functional name throughout different quantum chemistry 
programs caused some confusion and deviating results. A prominent example is the different implementation of the
B3LYP [hybrid functional](sec:modelchemistries.dft.globalhybrids) within ORCA and Gaussian. While ORCA uses VNW-V consistent 
with the TURBOMOLE program{cite}`ahlrichs2000turbo,ahlrichs2000ency,ahlrichs1989chem`, the Gaussian program{cite}`frisch1998gauss`
employs VWN-III. Using the `LDAOpt` keyword, both variants can be constructed:

```orca
# consistent with TURBOMOLE
%method
   Method DFT
   Functional B3LYP
   LDAOpt C_VWN5
end
```

```orca
# consistent with Gaussian
%method
   Method DFT
   Functional B3LYP
   LDAOpt C_VWN3
end
```

For convenience both functionals can be invoked separately via the simple input keywords `!B3LYP` for the ORCA/TURBOMOLE variant and `!B3LYP/G` for the Gaussian variant.

:::{note}
A special situation arises if LYP is the
correlation functional {cite}`lee1988phys` since LYP is *not* a
correction to the correlation, but rather includes the full correlation. 
It is therefore used in the B3LYP functional as:

$$E_{\text{B3LYP} }^{\text{C} } =E_{\text{LSD} }^{\text{C} } +c\left({ E_{\text{LYP} }^{\text{C} } -E_{\text{LSD} }^{\text{C} } } \right)$$ (eqn:modelchemistries.dft.gga.customizexc.ecb3lyp)
:::

Some functionals further incorporate empirical parameters that can be changed to improve
agreement with experiment. Currently, there are a few parameters that can
be changed (other than the parameters used in the [hybrid functionals](sec:modelchemistries.dft.hybriddft),
which are described later).

The first of these parameters is $\alpha$ of Slater's X$_{\alpha }$
method. Theoretically, it has a value of 2/3 and this is used in the HFS
and LSD functionals. However, the exchange contribution is underestimated 
by about 10% by this approximation (quite significant!) and a value around 0.70-0.75
is recommended for molecules. 

The second parameter is the $\beta$ for Becke's gradient-corrected exchange functional. 
Becke determined the value 0.0042 by fitting the exchange energies for rare
gas atoms. There is some evidence that with smaller basis sets,
a slightly smaller value such as 0.0039 gives improved results for molecules. 

The next parameter is the value $\kappa$, which occurs in the PBE
exchange functional. It has been given the value 0.804 by Perdew et al.
in order to satisfy the Lieb-Oxford bound. Since then, other workers
have argued that a larger value for this parameter (around 1.2) gives
better energetics, which is explored in the revPBE functional. Note, however,
that while revPBE gives slightly better energetics, it also gives 
slightly poorer geometries. 

The last two parameters are also related to PBE. Within the PBE 
correlation functional, there is $\beta_C$ (not to be confused
with the $\beta$ exchange parameter in Becke's exchange functional), whose
original value is $\beta_C=0.066725$. Modified variants exist with different
$\beta_C$ values, e.g., the PBEsol functional and the [PBEh-3c
composite method](sec:modelchemistries.3cmethods.pbeh3c). Furthermore, the $\mu$ parameter in the PBE exchange
functional may be modified. In the original formulation, it is related to
$\beta_C$ via $\mu = \beta_C \frac{\pi^{2} }{3}$, but has been modified
in later variants as well.

(tab:modelchemistries.dft.gga.customizexc.keywords.block)=
:::{table} `%method` block input keywords to modify basic exchange-correlation functionals.
:class: footnotesize
| Keyword                         | Options           | Description                                                         |
|:--------------------------------|:------------------|:--------------------------------------------------------------------|
| `Exchange`                      | `X_NOX`           | No exchange                                                         |
|                                 | `X_SLATER`        | Slater's local exchange                                             |
|                                 | `X_BECKE`         | Becke's ‘88 exchange                                                |
|                                 | `X_wB88`          | Short-range Becke '88 exchange for range-separated functionals      |
|                                 | `X_G96`           | Gill '96 gradient exchange                                          |
|                                 | `X_PW91`          | Perdew-Wang (PW) '91 gradient exchange                              |
|                                 | `X_mPW`           | Adamo-Barone modification of PW exchange                            |
|                                 | `X_PBE`           | Perdew-Burke-Ernzerhof (PBE) exchange                               |
|                                 | `X_RPBE`          | Revised PBE exchange                                                |
|                                 | `X_OPTX`          | Hoe/Cohen/Handy's optimized exchange                                |
|                                 | `X_X`             | Xu/Goddard exchange                                                 |
|                                 | `X_TPSS`          | TPSS meta-GGA exchange                                              |
|                                 | `X_B97D`          | Grimme's modified exchange for the B97-D GGA                        |
|                                 | `X_B97BECKE`      | Becke's original exchange for the B97 hybrid                        |
|                                 | `X_SCAN`          | Perdew's constrained exchange for the SCAN meta-GGA                 |
|                                 | `X_RSCAN`         | Perdew's constrained exchange for the rSCAN meta-GGA                |
|                                 | `X_R2SCAN`        | Perdew's constrained exchange for the r²SCAN meta-GGA               |
| `Correlation`                   | `C_NOC`           | No correlation                                                      |
|                                 | `C_VWN5`          | Local Vosko-Wilk-Nusair correlation (parameter set "V")             |
|                                 | `C_VWN3`          | Local Vosko-Wilk-Nusair correlation (parameter set "III")           |
|                                 | `C_PWLDA`         | Local PW correlation                                                |
|                                 | `C_P86`           | Perdew '86 correlation                                              |
|                                 | `C_PW91`          | PW '91 correlation                                                  |
|                                 | `C_PBE`           | PBE correlation                                                     |
|                                 | `C_LYP`           | LYP correlation                                                     |
|                                 | `C_TPSS`          | TPSS meta-GGA correlation                                           |
|                                 | `C_B97D`          | Grimme's modified correlation for the B97-D GGA                     |
|                                 | `C_B97BECKE`      | Becke's original correlation for the B97 hybrid                     |
|                                 | `C_SCAN`          | Perdew's constrained correlation for the SCAN meta-GGA              |
|                                 | `C_RSCAN`         | Perdew's constrained correlation for the rSCAN meta-GGA             |
|                                 | `C_R2SCAN`        | Perdew's constrained correlation for the r²SCAN meta-GGA            |
| `LDAOpt`                        | `C_NOC`           | Sets the local part of any correlation functional to no correlation |
|                                 | `C_PWLDA`         | Sets the local part of any correlation functional to PWLDA          |
|                                 | `C_VWN5`          | Sets the local part of any correlation functional to VWN5           |
|                                 | `C_VWN3`          | Sets the local part of any correlation functional to VWN3           |
| **Specific Parameters**         |                   |                                                                     |
| `XAlpha`                        | `<real>`          | Modifies Slater's $\alpha$ parameter (default 2/3)                  |
| `XBeta`                         | `<real>`          | Modifies Becke's $\beta$ parameter (default 0.0042)                 |
| `XKappa`                        | `<real>`          | Modifies the PBE(exchange) $\kappa$ parameter (default 0.804)       |
| `XMuePBE`                       | `<real>`          | Modifies the PBE(exchange) $\kappa$ parameter (default 0.21952)     |
| `CBetaPBE`                      | `<real>`          | Modifies the PBE(correlation) beta parameter (default 0.066725)     |
:::

```{index} Density Functional Theory; Hybrid Functionals
```
(sec:modelchemistries.dft.hybriddft)=
## Hybrid DFT

The idea of replacing a portion of the DFT exchange by exact exchange from Hartree-Fock theory (HFX) was introduced by Becke in 1993{cite}`becke1993chem1,becke1993chem2`.
This scheme is typically referred to as hybrid DFT and the most simple formulation of a one-parameter hybrid functional is depicted in equation {eq}`eqn:modelchemistries.dft.hybriddft.exchybrid`

$$E_{\text{hyb}}^{\text{XC}} =aE_{\text{HF}}^{\text{X}} + (1-a){ E_{\text{GGA}}^{\text{X}}} + E_{\text{GGA}}^{\text{C}}$$ (eqn:modelchemistries.dft.hybriddft.exchybrid)
:::

A more general description is given by the adiabatic connection model (ACM). In the ACM, hybrid functionals are constructed with three parameters according to equation {eq}`eqn:modelchemistries.dft.hybriddft.acm`:

$$E_{\text{XC} } = a E_{\text{HF} }^{\text{X} } +\left( 1 - a \right)E_{\text{LSD} }^{\text{X} } +bE_{\text{GGA} }^{\text{X} } +E_{\text{LSD} }^{\text{C} } +cE_{\text{GGA} }^{\text{C} }
$$ (eqn:modelchemistries.dft.hybriddft.acm)

Here, $E_{\text{XC} }$ is the total exchange/correlation energy,
$E_{\text{HF} }^{\text{X} }$ is the Hartree-Fock exchange,
$E_{\text{LSD} }^{\text{X} }$ is the local (Slater) exchange,
$E_{\text{GGA} }^{\text{X} }$ is the gradient correction to the
exchange, $E_{\text{LSD} }^{\text{C} }$ is the local, spin-density based
part of the correlation energy, and $E_{\text{GGA} }^{\text{C} }$ is the
gradient correction to the correlation energy. 

Over the years, various strategies to construct hybrid functionals have been developed. These range from physics motivated approaches relying on as few as possible parameters like the overall well-balanced PBE0 functional{cite}`adamo1999chem` to more empirical variants like the prominent three-parameter hybrid B3LYP{cite}`b3lyp`. 
Furthermore, various treatments of the HF exchange admixture were developed. The basic hybrids that use a static amount of HFX are typically referred to as [global hybrids](sec:modelchemistries.dft.globalhybrids) while functionals with variable amounts of HFX include [range-separated hybrids](sec:modelchemistries.dft.hybriddft.rangeseparatedhybrids) and local hybrids. Various [global](sec:modelchemistries.dft.globalhybrids) and [range-separated hybrid functionals](sec:modelchemistries.dft.hybriddft.rangeseparatedhybrids) are available in ORCA. Local hybrids may be implemented in a future version.

ORCA also provides a sophisticated infrastructure to create and [customize global](sec:modelchemistries.dft.globalhybrids.customization) and [range-separated hybrid functionals](sec:modelchemistries.dft.rangeseparatedhybrids.customization).

:::{note}
As by theory hybrid functionals are significantly more costly than (meta-)GGAs, ORCA uses the sophisticated [RIJCOSX](../essentialelements/RI.md) algorithm as a default to 
speed up hybrid DFT calculations.
:::

```{index} Density Functional Theory; Global Hybrid Functionals
```
(sec:modelchemistries.dft.globalhybrids)=
### Global Hybrid Functionals

Global hybrid functionals employ a fixed amount of Hartree-Fock exact exchange. ORCA features various
representatives with different compositions and amounts of HFX. The optimal amount of HFX is controversially discussed in the literature
and many empirical functionals were constructed by fitting it to reproduce an experimental property.
However, it has been argued from a theoretical viewpoint that the optimal mixing of HF exchange is 25%
{cite}`ernzerhof1998density` and large amounts of HFX are known to be disadvantageous for transition metal complexes.

A list of natively implemented global hybrid functionals is given in {numref}`tab:modelchemistries.dft.hybriddft.globlhybrids`.

(tab:modelchemistries.dft.hybriddft.globlhybrids)=
:::{table} List of available global hybrid functionals.
:class: footnotesize
| Functional                                    | Keyword       | %HFX  | Description                                                                                                  |
|:----------------------------------------------|:--------------|:-----:|:-------------------------------------------------------------------------------------------------------------|
| **hybrid GGAs**                               |               |       |                                                                                                              |
| B1LYP {cite}`adamo1997b1lyp`                  | `B1LYP`       | 25    | The one-parameter hybrid functional with Becke '88 exchange and Lee-Yang-Parr correlation (25% HF exchange)  |
| B3LYP {cite}`b3lyp`                           | `B3LYP`       | 20    | The popular B3LYP functional (20% HF exchange) as defined in the TurboMole program system (`LDAOPT C_VWN5`)  |
| B3LYP/G {cite}`b3lyp`                         | `B3LYP/G`     | 20    | The popular B3LYP functional (20% HF exchange) as defined in the Gaussian program system (`LDAOPT C_VWN3`)   |
| O3LYP {cite}`cohen2001o3lyp`                  | `O3LYP`       | 11.61 | The Handy hybrid functional                                                                                  |
| X3LYP {cite}`goddard2004pnas`                 | `X3LYP`       | 21.8  | The Xu and Goddard hybrid functional                                                                         |
| B1P86 {cite}`perdew1986phys`                  | `B1P86`       | 25    | The one-parameter hybrid version of BP86                                                                     |
| B3P86 {cite}`becke1993chem1`                  | `B3P86`       | 20    | The three-parameter hybrid version of BP86                                                                   |
| B3PW91 {cite}`becke1993chem1`                 | `B3PW91`      | 20    | The three-parameter hybrid version of PW91                                                                   |
| PW1PW {cite}`adamo1999chem`                   | `PW1PW`       | 25    | One-parameter hybrid version of PW91                                                                         |
| mPW1PW {cite}`barone1997jcp`                  | `MPW1PW`      | 25    | One-parameter hybrid version of mPWPW                                                                        |
| mPW1LYP {cite}`barone1997jcp`                 | `MPW1LYP`     | 25    | One-parameter hybrid version of mPWLYP                                                                       |
| PBE0 {cite}`adamo1999chem`                    | `PBE0`        | 25    | One-parameter hybrid version of PBE                                                                          |
| revPBE0 {cite}`grimme2011gmtkn30`             | `REVPBE0`     | 25    | "Revised" PBE0                                                                                               |
| revPBE38 {cite}`grimme2011gmtkn30`            | `REVPBE38`    | 37.5  | "Revised" PBE0 with 37.5% HF exchange                                                                        |
| BHandHLYP {cite}`becke1993chem1`              | `BHANDHLYP`   | 50    | Half-and-half hybrid functional by Becke                                                                     |
| **hybrid meta-GGAs**                          |               |       |                                                                                                              |
| M06 {cite}`m06`                               | `M06`         | 27    | |
| M06-2X {cite}`m06`                            | `M062X`       | 54    | |
| PW6B95 {cite}`zhao2005phys`                   | `PW6B95`      | 28    | |
| TPSSh {cite}`TPSS2003`                        | `TPSSH`       | 10    | The hybrid version of TPSS (10% HF exchange)                                                                 |
| TPSS0  {cite}`grimme2005tpss0`                | `TPSS0`       | 25    | A 25% exchange version of TPSSh that yields improved energetics                                              |
| r²SCANh {cite}`bursch_r2scanhybrids_2022`     | `R2SCANH`     | 10    | Global hybrid variant of r²SCAN with 10% HF exchange                                                         |
| r²SCAN0 {cite}`bursch_r2scanhybrids_2022`     | `R2SCAN0`     | 25    | Global hybrid variant of r²SCAN with 25% HF exchange                                                         |
| r²SCAN50 {cite}`bursch_r2scanhybrids_2022`    | `R2SCAN50`    | 50    | Global hybrid variant of r²SCAN with 50% HF exchange                                                         |
| **composite**                                 |               |       |                                                                                                              |
| PBEh-3c {cite}`grimme_pbeh3c`                 | `PBEH-3C`     | 42    | Composite DFT approach by Grimme et al.                                                                      |
| B3LYP-3c {cite}`grimme2020b3lyp3c`            | `B3LYP-3C`    | 20    | Composite DFT approach by Grimme et al.                                                                      |
:::

(sec:modelchemistries.dft.globalhybrids.customization)=
#### Customization of Global Hybrids

Global hybrid functional parameters can be customized via the `%method` block. For the customization of the basic exchange and correlation components
see the [Customization of Basic Functionals](sec:modelchemistries.dft.gga.customizexc) section. The important parameters for hybrid functionals are
those used in the ACM model (cf. equation {eq}`eqn:modelchemistries.dft.hybriddft.acm`). In this case, we will recreate the PBE0 functional (25% HFX) by
using the ACM syntax:

```orca
! RIJCOSX
# PBE0
%method
   Method DFT
   Functional PBE
   ACM_A        0.25      # fraction of Hartree-Fock exchange
   ACM_B        0.75      # fraction of the GGA exchange
   ACM_C        1.00      # fraction of the GGA correlation
   ScalLDAC     1.00      # fraction of LDA correlation, must be
                          # equal to ACM_C 
end
```
For simplicity, the ACM parameters can also be given as one string.

```orca
! RIJCOSX
# PBE0
%method
   Method DFT
   Functional PBE
   ACM       0.25, 1.00, 1.00   # as ACM   ACM-A, ACM-B, ACM-C
   ScalLDAC  1.00               # fraction of LDA correlation,
                                # must be equal to ACM_C 
end
```

As the ACM formalism can be non-intutive, ORCA provides an equivalent syntax to control the respective parameters.

```orca
! RIJCOSX
# PBE0
%method
   Method DFT
   Functional PBE
   ScalHFX        0.25      # fraction of Hartree-Fock exchange
   ScalDFX        0.75      # fraction of GGA exchange
   ScalGGAC       1.00      # fraction of GGA correlation
   ScalLDAC       1.00      # fraction of LDA correlation,
                            # must be equal to ScalGGAC 
end
```

:::{warning}
Note that `Functional` chooses specific predefined values
for the variables `Exchange`, `Correlation`, `LDAOpt` and `ACM` described below.
If given as a simple input keyword, in some cases, it will also activate
a dispersion correction. You can explicitly give these variables instead
or in addition to `Functional`. However, make sure that you specify
these variables *after* you have assigned a value to `Functional` or the
others will be reset to the values chosen by `Functional`.
:::

:::{tabularcolumns} \Y{0.2}\Y{0.3}\Y{0.5}
:::

(tab:modelchemistries.dft.globalhybrids.customization.keywords.block)=
:::{flat-table} `%method` block input keywords to modify global hybrid functionals.
:class: footnotesize
:header-rows: 1
* - Keyword
  - Options
  - Description
* - `ACM`
  - `<real, real, real>`
  - Defines the ACM-A, ACM-B, and ACM-C parameters  
* - `ACM_A`
  - `<real>`
  - Defines the ACM-A parameter (fraction of Hartree-Fock exchange)     
* - `ACM_B`
  - `<real>`
  - Defines the ACM-B parameter (fraction of GGA exchange) 
* - `ACM_C`
  - `<real>`
  - Defines the ACM-C parameter (fraction of GGA correlation)
* - `ScalHFX`
  - `<real>`
  - Controls the fraction of Hartree-Fock exchange, equiv. to `ACM_A`
* - `ScalDFX`
  - `<real>`
  - Controls the fraction of GGA exchange, equiv. to `ACM_B` 
* - `ScalGGAC`
  - `<real>`
  - Controls the fraction of GGA correlation, equiv. to `ACM_C`
:::

```{index} Density Functional Theory; Range-Separated Hybrid Functionals
```
(sec:modelchemistries.dft.hybriddft.rangeseparatedhybrids)=
### Range-Separated Hybrid Functionals

Unlike [global hybrids](sec:modelchemistries.dft.globalhybrids), range-separated hybrid (RSH) split the two-electron operator used for the exchange into a short-range (SR) and a long-range (LR) regime wherein the short-range part is typically described by DFT exchange and the long-range part by Hartree-Fock exchange. In ORCA, all range-separated hybrids use the error function splitting approach by Hirao and coworkers to distinguish both regimes (cf. equation {eq}`eqn:modelchemistries.dft.hybriddft.rangeseparatedhybrids.erf`).{cite}`hirao2001rangeseparation` This allows the definition of DFT functionals that dominate the short-range part by an adapted exchange functional of [LDA](sec:modelchemistries.dft.local), [GGA or meta-GGA](sec:modelchemistries.dft.gga) level and the long-range part by Hartree-Fock exchange.

$$r_{12}^{-1} = \underbrace{\text{erfc}(\mu \cdot r_{12}) \cdot r_{12}^{-1} }_{\text{SR} } + \underbrace{\text{erf}(\mu \cdot r_{12}) \cdot r_{12}^{-1} }_{\text{LR} }$$ (eqn:modelchemistries.dft.hybriddft.rangeseparatedhybrids.erf)

where
$\text{erf}(x) = \frac{2}{\sqrt{\pi} } \int_{0}^{x} \exp(-t^{2}) dt$ and
$\text{erfc}(x) = 1 - \text{erf}(x)$. Note that the splitting is only
applied to the exchange contribution; all other contributions (one-electron
parts of the Hamiltonian, the electron-electron Coulomb interaction and the 
approximation for the DFT correlation) are not affected. Later, Handy and coworkers{cite}`handy2004CAMB3LYPLC` generalized the
ansatz to:

$$r_{12}^{-1} = \underbrace{\frac{1 - [ \alpha + \beta \cdot \text{erf}(\mu \cdot r_{12})]}{ r_{12} }}_{\text{SR} } + \underbrace{\frac{\alpha + \beta \cdot \text{erf}(\mu \cdot r_{12}) }{r_{12} }}_{\text{LR} }$$ (eqn:modelchemistries.dft.hybriddft.rangeseparatedhybrids.erfgeneralized)

This form of the splitting used in ORCA is shown visually (according to Handy
and coworkers) in {numref}`fig:modelchemistries.dft.hybriddft.rangeseparatedhybrids.ansatz`.

(fig:modelchemistries.dft.hybriddft.rangeseparatedhybrids.ansatz)=
```{figure} ../../images/743.*

Graphical description of the range-separation ansatz. The gray area
corresponds to Hartree-Fock exchange. $\alpha$ and $\beta$ follow
Handy's terminology {cite}`handy2004CAMB3LYPLC`.

```

:::{important}
Currently, RSH functionals can be used for integral-direct single-point calculations, calculations
involving the first nuclear gradient (i.e. geometry optimizations),
frequency calculations, TDDFT, TDDFT nuclear gradient, and EPR/NMR calculations.
As with the [global hybrids](sec:modelchemistries.dft.globalhybrids), [RIJCOSX](../essentialelements/RI.md) is used by default
to drastically speed up the calculations. Alternatively, only RIJONX can be used.
:::


A list of available range-separated hybrid functionals is given in {numref}`tab:modelchemistries.dft.rangeseparatedhybrids`


(tab:modelchemistries.dft.rangeseparatedhybrids)=
:::{table} List of available range-separated hybrid functionals. $\mu$ is the range-separation parameter.
:class: footnotesize
| Functional                                        | Keyword        | %HFX             | $\mu$ / $\text{bohr}^{-1}$ | % fixed DFX |
|:--------------------------------------------------|:---------------|:----------------:|:--------------------------:|:-----------:|
| **hybrid GGAs**                                   |                |                  |                            |             |
| $\omega$B97 {cite}`headgordon2008wB97wB97X`       | `WB97`         | 0 -- 100         | 0.40                       | ---         |
| $\omega$B97X {cite}`headgordon2008wB97wB97X`      | `WB97X`        | 15.7706 -- 100   | 0.30                       | ---         |
| $\omega$B97X-V {cite}`headgordon2014wB97XV`       | `WB97X-V`      | 16.7 -- 100      | 0.30                       | ---         |
| $\omega$B97X-D3 {cite}`chai2013wB97XD3`           | `WB97X-D3`     | 19.5728 -- 100   | 0.25                       | ---         |
| $\omega$B97X-D3(BJ) {cite}`goerigk2018`           | `WB97X-D3BJ`   | 16.7 -- 100      | 0.30                       | ---         |
| $\omega$B97X-D4 {cite}`najibi2020`                | `WB97X-D4`     | 16.7 -- 100      | 0.30                       | ---         |
| $\omega$B97X-D4rev{cite}`grimme2022wb97x3c`       | `WB97X-D4REV`  | 16.7 -- 100      | 0.30                       | ---         |
| CAM-B3LYP {cite}`handy2004CAMB3LYPLC`             | `CAM-B3LYP`    | 19 -- 65         | 0.33                       | 35%         |
| LC-BLYP {cite}`hirao2004LC_TDDFT`                 | `LC-BLYP`      | 0 -- 100         | 0.33                       | ---         |
| LC-PBE {cite}`hirao2001rangeseparation`           | `LC-PBE`       | 0 -- 100         | 0.47                       | ---         |
| **hybrid meta-GGAs**                              |                |                  |                            |             |
| $\omega$B97M-V {cite}`headgordon2016wB97MV`       | `WB97M-V`      | 15 -- 100        | 0.30                       | ---         |
| $\omega$B97M-D3(BJ) {cite}`goerigk2018`           | `WB97M-D3BJ`   | 15 -- 100        | 0.30                       | ---         |
| $\omega$B97M-D4 {cite}`najibi2020`                | `WB97M-D4`     | 15 -- 100        | 0.30                       | ---         |
| $\omega$B97M-D4rev {cite}`grimme2022wb97x3c`      | `WB97M-D4REV`  | 15 -- 100        | 0.30                       | ---         |
| $\omega$r²SCAN {cite}`Wittmann2023`               | `WR2SCAN`      | 0 -- 100         | 0.30                       | ---         |
| **composite**                                     |                |                  |                            |             |
| $\omega$B97X-3c {cite}`grimme2022wb97x3c`         | `WB97X-3C`     | 16.7 -- 100      | 0.30                       | ---         |
::: 

(sec:modelchemistries.dft.rangeseparatedhybrids.customization)=
#### Customizing Range-Separated Hybrids

Range-separated hybrid functional parameters can also be customized via the `%method` block. For the customization of the basic exchange and correlation components
see the [Customization of Basic Functionals](sec:modelchemistries.dft.gga.customizexc) section. Basic hybrid-related keywords and the respective ACM model are described in the [Hybrid DFT](sec:modelchemistries.dft.hybriddft) and [Customization of Global Hybrids](sec:modelchemistries.dft.globalhybrids.customization) sections.

In this example, we will recreate the LC-PBE functional:

```orca
! RIJCOSX
# LC-PBE
%method
   Method DFT
   Exchange X_LRCPBE
   Correlation C_PBE
   LDAOpt C_PWLDA
   ACM_A        0.00   # fraction of static Hartree-Fock exchange
   ACM_B        0.00   # fraction of static GGA exchange
   ACM_C        1.00   # fraction of GGA correlation
   ScalLDAC     1.00   # fraction of LDA correlation, must be equal to ScalGGAC 
   RangeSepEXX  true   # activates range-separated exchange
   RangeSepMu   0.47   # range-separation parameter, should be >0
   RangeSepScal 1.00   # fraction of variable HFX, should sum to 1
                       # with ACM-A and ACM-B
end
```
Which is equivalent to the `ScalX` syntax described before.

```orca
! RIJCOSX
# LC-PBE
%method
   Method DFT
   Exchange X_LRCPBE
   Correlation C_PBE
   LDAOpt C_PWLDA
   ScalHFX      0.00   # fraction of static Hartree-Fock exchange
   ScalDFX      0.00   # fraction of static GGA exchange
   ScalGGAC     1.00   # fraction of GGA correlation
   ScalLDAC     1.00   # fraction of LDA correlation, must be equal to ScalGGAC 
   RangeSepEXX  true   # activates range-separated exchange
   RangeSepMu   0.47   # range-separation parameter, should be >0
   RangeSepScal 1.00   # fraction of variable HFX, should sum to 1
                       # with ScalHFX and ScalDFX
end
```

:::{warning}
The amount of fixed DFT Exchange (`ACM_B` or `ScalDFX`) can
only be changed for CAM-B3LYP and LC-BLYP. Accordingly, ACM-B is
ignored by the $\omega$B97 approaches as no corresponding
$\mu$-independent exchange functional has been defined. While
it is technically possible to choose an exchange functional that has no
$\mu$-dependence, this makes no sense conceptually.
:::

(tab:modelchemistries.dft.rangeseparatedhybrids.customization.keywords.block)=
:::{table} `%method` block input keywords to modify range-separated hybrid functionals.
:class: footnotesize
| Keyword                         | Options              | Description                                                     |
|:--------------------------------|:---------------------|:----------------------------------------------------------------|
| `RangeSepEXX`                   | `true`               | Activates range-separated exchange                              |
| `RangeSepMu`                    | `<real>`             | Controls the range-separation parameter, should be >0           |
| `RangeSepScal`                  | `<real>`             | Controls the fraction of variable Hartree-Fock exchange         |
:::

(sec:modelchemistries.dft.doublehybriddft)=
## Double-Hybrid DFT
```{index} Density Functional Theory; Double-Hybrid Functionals
```

In addition to mixing the HF-exchange into a given density functional, Grimme has proposed to mix in a fraction of
the [MP2 correlation energy](../modelchemistries/MP2.md) as calculated with hybrid DFT
orbitals {cite}`Grimme2006jcp`. Such functionals may be referred to as
"double-"hybrid functionals. The original expression by Grimme is:

$$E_{\text{XC}} = aE_{\text{X}}^{\text{HF}} +\left({1-a} \right)E_{\text{X}}^{\text{DFT}} +\left({1-c}
\right)E_{\text{C}}^{\text{DFT}} +cE_{\text{C}}^{\text{MP2}}
$$ (eqn:modelchemistries.dft.doublehybriddft.exc)

The first proposed double-hybrid functional by Grimme was B2PLYP.{cite}`Grimme2006jcp` This double-hybrid functional utilizes the B88 exchange functional and the LYP correlation
functionals. It introduces 53% of Hartree-Fock exchange ($a = 0.53$) and replaces 27% of the DFT correlation energy by MP2 correlation energy ($c = 0.27$).
Since then many other DH-DFT approaches that deviate from the original theme were developed. For example Grimme proposed DH functionals like PWPB95{cite}`goerigk2011chem` that use spin-component-scaled MP2. 
Further, functionals whose composition was empirically fitted against databases without any physical constraints or restrictions as previously proposed in {eq}`eqn:modelchemistries.dft.doublehybriddft.exc` 
like Martin's DSD (dispersion corrected, spin-component scaled double-hybrid) functionals{cite}`martin2010dsd,martin2011dsd,martin2013dsd` were developed and refined with revDSD-PBEP86-D4{cite}`martin2021revdsd` being one of 
the most well known representatives. Functionals of the XYG$n$ family{cite}`goddard2009xyg` or Head-Gordon's $\omega$B97M(2){cite}`Mardirossian2018` employ differently constructed densities for the DFT and the 
perturbation-theory parts with the latter also basing on a [range-separated hybrid functional](sec:modelchemistries.dft.hybriddft.rangeseparatedhybrids).
In principle, other correlated methods like dRPA or higher order MP theory may be used within the double hybrid scheme. However, the most common approach employs classical [MP2](../modelchemistries/MP2.md) or its spin-component-scaled variants. The [DLPNO approximation to MP2](sec:modelchemistries.mp2.dlpno) is also available within ORCA and can
be used to massively speed up the energy and gradient calculations for large systems. The accuracy and efficiency of DLPNO-DHs was extensively studied
by Bursch, Neese and co-workers{cite}`bursch2023dlpnodhs`.
Common to almost all double-hybrid functionals is a comparably large amount of Hartree-Fock exchange of 50% and more.
Most classical double-hybrid functionals following the scheme by Grimme can be utilized for single point calculations, analytic gradients
(and thus also geometry optimizations{cite}`Neese2007doublehybrid`, relaxed scans, and transition
state searches), dipole moments and other first order properties, magnetic second order properties
(chemical shifts and g-tensors without the frozen core approximation in the MP2 part), as well as for numerical polarizabilities
and frequencies. 

Some double-hybrid functionals were further optimized for excited state applications and will make use of a [Doubles Corrections](sec:spectroscopyproperties.tddft.doubles) to correct the singles-only excited states within the [time-dependent DFT (TD-DFT)](sec:spectroscopyproperties.excitedstates.tddft) framework. Some of them, 
like SCS-PBE-QIDH only make use of spin-component-scaling for the CIS(D) component of the calculation. However, many of them have recently also been
tested for ground-state properties.{cite}`GS_RSDHDFs`

:::{note}
ORCA employs the [RIJCOSX](../essentialelements/RI.md) and [RI-MP2](../essentialelements/RI.md) by default. If this is not wanted, RI can be deactivated generally by using the `!NORI` 
keyword or if only the RI approximation of the MP2 part should be deactivated via the `%mp2` block:

```orca
%mp2
   RI false
end
```

Indeed, there is hardly ever any reason to use conventional MP2.
:::

:::{note}
Note that per default no MP2 response density is calculated as its construction adds
significant overhead. In this case, only the double-hybrid energy is correct. 
The computation of the MP2 response density that is consistent with first-order properties from analytic first-derivatives can be requested
via the `%mp2 density relaxed end` statement in the `%mp2` block. The considerably less costly unrelaxed (expectation value-like) density 
may instead requested by `%mp2 density unrelaxed end`. However, this is not recommended
since the changes to the relaxed density are considerable in our
experience and the unrelaxed density has a much weaker theoretical
status than its relaxed counterpart.
:::

```{index} Density Functional Theory; Global Double-Hybrid Functionals
```
(sec:modelchemistries.dft.doublehybriddft.globaldoublehybrids)=
### Global Double-Hybrid Functionals

Global double-hybrid functionals are based on the respective [global hybrid functionals](sec:modelchemistries.dft.globalhybrids)
and employ static admixtures of [Hartree-Fock](sec:essentialelements.hartreefock) exchange and [the MP2 correlation energy](../modelchemistries/MP2.md). 
A list of currently implemented global double-hybrid functionals is given in {numref}`tab:modelchemistries.dft.doublehybriddft.globaldoublehybrids`. 
The revDSD-PBEP86-D4{cite}`martin2021revdsd` by Martin and co-workers has proven to be accurate for most thermochemistry applications. 

:::{warning}
For some functionals of the DSD/DOD family, different parameters for the same functional name were provided by the authors. The employed parameterization
is indicated by the `(year-of-publication)` suffix of the functional and the respective keywords. Also not that for some of them, the basic parameters change
in presence of different [dispersion corrections](../modelchemistries/dispersioncorrections.md). Please carefully check, if the employed parameters agree
with your expectations!
:::

:::{hint}
For most natively implemented double-hybrids you can simple add the `DLPNO-` prefix to the respective functional simple input keyword, e.g. `DLPNO-B2PLYP`.
For all others, the DLPNO treatment can be activated via the `%mp2` block using the `DLPNO true` keyword.
:::

:::{raw} latex
\begingroup
\footnotesize
:::

:::{tabularcolumns} \Y{0.25}\Y{0.2}\Y{0.15}\Y{0.08}\Y{0.08}\Y{0.08}\Y{0.08}\Y{0.08}
:::

(tab:modelchemistries.dft.doublehybriddft.globaldoublehybrids)=
:::{flat-table} List of available global double-hybrid functionals. `PS` is the opposite-spin, `PT` the same-spin scaling parameter. Excited-states optimized functionals only employ spin-component-scaling for the [CIS(D) doubles correction](sec:spectroscopyproperties.tddft.doubles) within the the TD-DFT framework. Same-spin indirect term (CTss), opposite-spin indirect term (CTos), same-spin direct term (CUss), and opposite-spin direct term (CUos) parameters are given in the footnotes.
:class: footnotesize
:header-rows: 1
* - Functional
  - Keywords
  - `%HFX`
  - `%DFX`
  - `%GGAC`
  - `%MP2C`
  - `PS`
  - `PT`   
* - DSD-BLYP {cite}`martin2010dsd`
  - `DSD-BLYP D3BJ`
  - 69
  - 31
  - 54
  - 100
  - 0.46
  - 0.37
* - DSD-BLYP-NoDisp(2013) {cite}`martin2013dsd`
  - `DSD-BLYP/2013`
  - 75
  - 25
  - 53
  - 100
  - 0.46
  - 0.60 
* - DSD-BLYP-D3(BJ)(2013) {cite}`martin2013dsd`
  - `DSD-BLYP/2013 D3BJ`
  - 71
  - 29
  - 54
  - 100
  - 0.47
  - 0.40   
* - DSD-PBEP86 {cite}`martin2011dsd`
  - `DSD-PBEP86 D3BJ`
  - 70
  - 30
  - 43
  - 100
  - 0.53
  - 0.25
* - DSD-PBEP86-NoDisp(2013) {cite}`martin2013dsd`
  - `DSD-PBEP86/2013`
  - 72
  - 28
  - 44
  - 100
  - 0.51
  - 0.36 
* - DSD-PBEP86-D3(BJ)(2013) {cite}`martin2013dsd`
  - `DSD-PBEP86/2013 D3BJ`
  - 69
  - 31
  - 44
  - 100
  - 0.52
  - 0.22 
* - DSD-PBEB95-NoDisp {cite}`martin2013dsd`
  - `DSD-PBEB95`
  - 70
  - 30
  - 52
  - 100
  - 0.48
  - 0.22   
* - DSD-PBEB95-D3(BJ) {cite}`martin2013dsd`
  - `DSD-PBEB95 D3BJ`
  - 66
  - 34
  - 55
  - 100
  - 0.46
  - 0.09
* - B2PLYP {cite}`Grimme2006jcp`
  - `B2PLYP`
  - 53
  - 47
  - 73
  - 27
  - 
  - 	        
* - mPW2PLYP {cite}`Schwabe2006pccp`
  - `mPW2PLYP`
  - 55
  - 45
  - 75
  - 25
  -
  -      
* - B2GP-PLYP {cite}`b2gpplyp`
  - `B2GP-PLYP`
  - 65
  - 35
  - 64
  - 36
  - 
  -      
* - B2K-PLYP {cite}`b2kplyp`
  - `B2K-PLYP`
  - 72
  - 28
  - 58
  - 42
  - 
  -  
* - B2T-PLYP {cite}`b2kplyp`
  - `B2T-PLYP`
  - 60
  - 40
  - 69
  - 31
  - 
  -      
* - B2NC-PLYP {cite}`b2ncplyp`
  - `B2NC-PLYP`
  - 81
  - 19
  - 45
  - 55
  - 
  -      
* - PWPB95 {cite}`goerigk2011chem`
  - `PWPB95`
  - 50
  - 50
  - 73.1
  - 26.9
  - 1.0
  - 0.0    
* - PBE-QIDH {cite}`PBEQIDH`
  - `PBE-QIDH`
  - 69
  - 31
  - 67
  - 33
  - 
  - 
* - PBE0-DH {cite}`PBE0DH`
  - `PBE0-DH`
  - 50
  - 50
  - 87.5
  - 12.5
  - 
  - 
* - revDSD-PBEP86(2021) {cite}`martin2021revdsd`
  - `REVDSD-PBEP86/2021`
  - 69
  - 31
  - 42.24
  - 100
  - 0.5935
  - 0.0566
* - revDSD-PBEP86-D4(2021) {cite}`martin2021revdsd`
  - `REVDSD-PBEP86-D4/2021`
  - 69
  - 31
  - 42.24
  - 100
  - 0.5935
  - 0.0566
* - revDOD-PBEP86(2021) {cite}`martin2021revdsd`
  - `REVDOD-PBEP86/2021`
  - 69
  - 31
  - 43.01
  - 100
  - 0.6131
  - 0.0
* - revDOD-PBEP86-D4(2021) {cite}`martin2021revdsd`
  - `REVDOD-PBEP86-D4/2021`
  - 69
  - 31
  - 43.01
  - 100
  - 0.6131
  - 0.0
* - SOS1-r²SCAN-CIDH {cite}`Wittmann2023`
  - `R2SCAN-CIDH`
  - 55
  - 45
  - 83.33
  - 16.67
  - 1.333
  - 0.0
* - SOS1-r²SCAN-QIDH {cite}`Wittmann2023`
  - `R2SCAN-QIDH`
  - 69.34
  - 30.76
  - 66.67
  - 33.33
  - 1.333
  - 0.0
* - SOS1-r²SCAN0-2 {cite}`Wittmann2023`
  - `R2SCAN0-2`
  - 79.37
  - 20.63
  - 50
  - 50
  - 1.333
  - 0.0
* - SOS1-r²SCAN0-DH {cite}`Wittmann2023`
  - `R2SCAN0-DH`
  - 50
  - 50
  - 87.50
  - 12.50
  - 1.333
  - 0.0
* - Pr²SCAN50 {cite}`Wittmann2023`
  - `PR2SCAN50`
  - 50
  - 50
  - 75
  - 25
  - 1.333
  - 0.0
* - Pr²SCAN69 {cite}`Wittmann2023`
  - `PR2SCAN69`
  - 69.34
  - 30.76
  - 55.56
  - 44.44
  - 1.333
  - 0.0
* - $\kappa$Pr²SCAN50 {cite}`Wittmann2023`
  - `KPR2SCAN50`
  - 50
  - 50
  - 70
  - 30
  - 1.333
  - 0.0
* - **excited state opt.**
  -
  -
  -
  -
  -
  -
  -
* - SCS/SOS-B2PLYP21 {cite}`SCSTDDHDFs`
  - `SCS/SOS-B2PLYP21`
  - 53
  - 47
  - 73
  - 27
  - [^a]
  - [^a]
* - SCS-PBE-QIDH {cite}`SCSTDDHDFs`
  - `SCS-PBE-QIDH`
  - 69
  - 31
  - 67
  - 33
  - [^b]
  - [^b]
* - SOS-PBE-QIDH {cite}`SCSTDDHDFs`
  - `SOS-PBE-QIDH`
  - 69
  - 31
  - 67
  - 33
  - [^c]
  - [^c]
* - SCS-B2GP-PLYP21 {cite}`SCSTDDHDFs`
  - `SCS-B2GP-PLYP21`
  - 65
  - 35
  - 64
  - 36
  - [^d]
  - [^d]
* - SOS-B2GP-PLYP21 {cite}`SCSTDDHDFs`
  - `SOS-B2GP-PLYP21`
  - 65
  - 35
  - 64
  - 36
  - [^e]
  - [^e]   
:::
:::{raw} latex
\endgroup
:::


[^a]: SCS/SOS-B2PLYP21: CTss: 0.000; CTos: 0.334; CUss: 0.000; CUos: 0.283.
[^b]: SCS-PBE-QIDH: CTss: 0.070; CTos: 0.515; CUss: 0.096; CUos: 0.524.
[^c]: SOS-PBE-QIDH: CTss: 0.000; CTos: 0.547; CUss: 0.000; CUos: 0.573.
[^d]: SCS-B2GP-PLYP21: CTss: 0.018; CTos: 0.475; CUss: 0.000; CUos: 0.468.
[^e]: SOS-B2GP-PLYP21: CTss: 0.000; CTos: 0.489; CUss: 0.000; CUos: 0.484.

```{index} Density Functional Theory; Range-Separated Double-Hybrid Functionals
```
(sec:modelchemistries.dft.doublehybriddft.rangeseparateddoublehybrids)=
### Range-Separated Double-Hybrid Functionals

Range-separated double-hybrids employ variable amounts of Hartree-Fock exchange much like
[range-separated hybrid functionals](sec:modelchemistries.dft.hybriddft.rangeseparatedhybrids) 
and static amounts of [MP2 correlation](../modelchemistries/MP2.md). A list of available range-separated
double-hybrid functionals is given in {numref}`tab:modelchemistries.dft.doublehybriddft.rangeseparateddoublehybrids`.

:::{hint}
For most natively implemented double-hybrids you can simple add the `DLPNO-` prefix to the respective functional simple input keyword, e.g. `DLPNO-WPR2SCAN50`.
For all others, the DLPNO treatment can be activated via the `%mp2` block using the `DLPNO true` keyword.
:::

:::{raw} latex
\begingroup
\footnotesize
:::

:::{tabularcolumns} \Y{0.32}\Y{0.2}\Y{0.08}\Y{0.08}\Y{0.08}\Y{0.08}\Y{0.08}\Y{0.08}
:::

(tab:modelchemistries.dft.doublehybriddft.rangeseparateddoublehybrids)=
:::{flat-table} List of available range-separated double-hybrid functionals. `PS` is the opposite-spin, `PT` the same-spin scaling parameter. $\mu$ is the range-separation parameter. Excited-states optimized (ES-Opt.) functionals only employ spin-component-scaling for the [CIS(D) doubles correction](sec:spectroscopyproperties.tddft.doubles) within the the TD-DFT framework. Same-spin indirect term (CTss), opposite-spin indirect term (CTos), same-spin direct term (CUss), and opposite-spin direct term (CUos) parameters are given in the footnotes.
:class: footnotesize
:header-rows: 1
* - Functional
  - Keywords
  - `%HFX`
  - $\mu$ / $\text{bohr}^{-1}$
  - `%GGAC`
  - `%MP2C`
  - `PS`
  - `PT`
* - $\omega$B97M(2)[^f] {cite}`Mardirossian2018`
  - `WB97M(2)`
  - 62.194 `-` 100
  - 0.30
  - 100
  - 34.096
  - `-`
  - `-`
* - $\omega$B97X-2(TQZ) {cite}`Chai2009`
  - `WB97X-2`
  - 63.6158 `-` 95.1661
  - 0.30
  - 100
  - 100
  - 0.447105
  - 0.529319
* - $\omega$Pr2SCAN50 {cite}`Wittmann2023`
  - `WPR2SCAN50`
  - 50 `-` 100
  - 0.214013
  - 65
  - 35
  - 1.333
  - 0.000
* - RSX-QIDH {cite}`RSXQIDH`
  - `RSX-QIDH`
  - 69 `-` 100
  - 0.27
  - 67
  - 33
  - `-`
  - `-`
* - RSX-0DH {cite}`RSX0DH`
  - `RSX-0DH`
  - 50 `-` 100
  - 0.33
  - 87.5
  - 12.5
  - `-`
  - `-`
* - $\omega$B2PLYP {cite}`goerigk2019RSDHTDDFT`
  - `WB2PLYP`
  - 53 `-` 100
  - 0.30
  - 73
  - 27
  - `-`
  - `-`
* - $\omega$B2GP-PLYP {cite}`goerigk2019RSDHTDDFT`
  - `WB2GP-PLYP`
  - 65 `-` 100
  - 0.27
  - 64
  - 36
  - `-`
  - `-`
* - $\omega$B88PP86 {cite}`goerigk2019RSDHTDDFT`
  - `WB88PP86`
  - 65 `-` 100
  - 0.20
  - 58
  - 42
  - `-`
  - `-`
* - $\omega$PBEPP86 {cite}`goerigk2019RSDHTDDFT`
  - `WPBEPP86`
  - 70 `-` 100
  - 0.18
  - 68
  - 48
  - `-`
  - `-`
* - **excited state opt.**
  - 
  - 
  - 
  - 
  - 
  - 
  - 
* - SCS/SOS-$\omega$B2PLYP {cite}`SCSTDDHDFs`
  - `SCS/SOS-WB2PLYP`
  - 53 `-` 100
  - 0.30
  - 73
  - 27
  - [^g]
  - [^g]
* - SCS-$\omega$B2GP-PLYP {cite}`SCSTDDHDFs`
  - `SCS-WB2GP-PLYP`
  - 65 `-` 100
  - 0.27
  - 64
  - 36
  - [^h]
  - [^h]
* - SOS-$\omega$B2GP-PLYP {cite}`SCSTDDHDFs`
  - `SOS-WB2GP-PLYP`
  - 65 `-` 100
  - 0.27
  - 64
  - 36
  - [^i]
  - [^i]
* - SCS-RSX-QIDH {cite}`SCSTDDHDFs`
  - `SCS-RSX-QIDH`
  - 69 `-` 100
  - 0.27
  - 67
  - 33
  - [^j]
  - [^j]
* - SOS-RSX-QIDH {cite}`SCSTDDHDFs`
  - `SOS-RSX-QIDH`
  - 69 `-` 100
  - 0.27
  - 67
  - 33
  - [^k]
  - [^k]
* - SCS-$\omega$B88PP86 {cite}`SCSTDDHDFs`
  - `SCS-WB88PP86`
  - 65 `-` 100
  - 0.20
  - 58
  - 42
  - [^l]
  - [^l]
* - SOS-$\omega$B88PP86 {cite}`SCSTDDHDFs`
  - `SOS-WB88PP86`
  - 65 `-` 100
  - 0.20
  - 58
  - 42
  - [^m]
  - [^m]
* - SCS-$\omega$PBEPP86 {cite}`SCSTDDHDFs`
  - `SCS-WPBEPP86`
  - 70 `-` 100
  - 0.18
  - 68
  - 48
  - [^n]
  - [^n]
* - SOS-$\omega$PBEPP86 {cite}`SCSTDDHDFs`
  - `SOS-WPBEPP86`
  - 70 `-` 100
  - 0.18
  - 68
  - 48
  - [^o]
  - [^o]
:::
:::{raw} latex
\endgroup
:::


[^f]: Must be used with ωB97M-V orbitals (cf. {numref}`sec:modelchemistries.dft.doublehybriddft.rangeseparateddoublehybrids.wb97m2`).
[^g]: SCS/SOS-$\omega$B2PLYP: CTss: 0.000; CTos: 0.433; CUss: 0.000; CUos: 0.460.
[^h]: SCS-$\omega$B2GP-PLYP: CTss: 0.000; CTos: 0.571; CUss: 0.135; CUos: 0.558.
[^i]: SOS-$\omega$B2GP-PLYP: CTss: 0.000; CTos: 0.570; CUss: 0.000; CUos: 0.610.
[^j]: SCS-RSX-QIDH: CTss: 0.174; CTos: 0.541; CUss: 0.586; CUos: 0.424.
[^k]: SOS-RSX-QIDH: CTss: 0.000; CTos: 0.632; CUss: 0.000; CUos: 0.714.
[^l]: SCS-$\omega$B88PP86: CTss: 0.000; CTos: 0.557; CUss: 0.092; CUos: 0.545.
[^m]: SOS-$\omega$B88PP86: CTss: 0.000; CTos: 0.559; CUss: 0.000; CUos: 0.599.
[^n]: SCS-$\omega$PBEPP86: CTss: 0.000; CTos: 0.610; CUss: 0.297; CUos: 0.540.
[^o]: SOS-$\omega$PBEPP86: CTss: 0.000; CTos: 0.613; CUss: 0.000; CUos: 0.669.

(sec:modelchemistries.dft.doublehybriddft.rangeseparateddoublehybrids.wb97m2)=
#### $\omega$B97M(2)

Some double-hybrid functionals, such as $\omega$B97M(2){cite}`Mardirossian2018` must be applied to orbitals converged with a
different functional. This can be accomplished with a two-step
calculation using `MORead` and `MaxIter=1`. Note that because the
orbitals are not obtained self-consistently, only single point energies
can be computed in this way, i.e. no density, gradient, or properties!
The usage of such functionals may be automatized using the [Compound script language](../workflowsautomatization/compound.md).
An exemplary compound script for a $\omega$B97M(2) single-point calculation is given below:

```orca
*xyz 0 1
  H 0.0 0.0 0.0
  F 0.0 0.0 0.9
*
# ------------------------------------------------------------------------------------
# Energy calculation with the wB97M(2) double-hybrid functional, as defined in
# N. Mardirossian, M. Head-Gordon, J. Chem. Phys. 2018, 148, 241736.
# The final energy is calculated non-variatonally using wB97M-V orbitals.
# Note that FrozenCore is on default - one can turn it off using kw2 = "NoFrozenCore".
# Author: Georgi L. Stoychev
# ------------------------------------------------------------------------------------

# Optional variables:
Variable molecule = "water.xyz";
Variable charge   = 0;
Variable mult     = 1;
Variable NLOpt = "SCNL";        # Consistent with Q-Chem. "NL" likely very similar. Only matters for Step 1.
Variable Basis = "def2-TZVP";   # Should be TZ or higher for reliable results
Variable AuxC  = "def2-TZVP/C"; # RI-MP2 is used by default. Must be compatible with the Basis
Variable AuxJ  = "def2/J";      # RIJCOSX is used by default
Variable RIMP2 = True;          # Set to false to turn off RI-MP2
Variable Grid  = "defGrid2";    # Should be OK.
Variable kw1   = "";            # Additional simple input keywords for step 1
Variable kw2   = "";            # Additional simple input keywords for step 2

# Output variables
Variable EwB97MV, EwB97M2;      # Will hold the final energies

# Step 1: wB97M-V calculation to obtain the orbitals
NewStep
  ! wB97M-V &{NLOpt} &{Grid} &{kw1}
  *xyzfile &{charge} &{mult} &{molecule}
  %basis
    Basis "&{Basis}"
    AuxJ  "&{AuxJ}"
  end
StepEnd
EwB97MV.ReadProperty(propertyName="DFT_Total_En");

# Step 2: single iteration with the wB97M(2) functional + MP2 correlation to get the final energy
ReadMOs(1);
NewStep
  ! wB97M(2) &{NLOpt} &{Grid} &{kw2} NoIter CalcGuessEnergy
  %basis
    Basis "&{Basis}"
    AuxC  "&{AuxC}"
    AuxJ  "&{AuxJ}"
  end
  %scf
    IgnoreConv 1
  end
  %mp2 RI &{RIMP2} end
Step_End

EwB97M2.ReadProperty(propertyName="MP2_Total_Energy");

Print("");
Print("================================================================================\n");
Print(" wB97M-V Energy:  %20.10lf\n",EwB97MV);
Print(" wB97M(2) Energy: %20.10lf\n",EwB97M2);

End
```

(sec:modelchemistries.dft.doublehybrids.customization)=
### Customization of Double-Hybrids

As double-hybrid functionals make use of customizable components of [global hybrids](sec:modelchemistries.dft.rangeseparatedhybrids.customization) or 
[range-separated hybrids](sec:modelchemistries.dft.rangeseparatedhybrids.customization) they can can be constructed and customized in similar fashion. 
The MP2 correlation treatment for double-hybrids can be controlled via the `DoMP2 true` and `ScalMP2C` keywords within the `%method` block. 
Moreover, the MP2 treatment can be further customized via the `%mp2` block. For example, the spin-composite-scaled, range-separated double-hybrid functional $\omega$Pr²SCAN50
can be constructed as follows:

```orca
! RIJCOSX def2-TZVP/C NOTRAH
# wPr2SCAN50
%method
   Method       DFT
   DoMP2        true       # activates MP2 correlation part
   Exchange     X_WR2SCAN
   Correlation  C_R2SCAN
   LDAOpt       C_PWLDA
   ScalHFX      0.50       # fraction of static Hartree-Fock exchange
   ScalDFX      0.00       # fraction of static GGA exchange
   ScalGGAC     0.65       # fraction of GGA correlation
   ScalLDAC     0.65       # fraction of LDA correlation, must be equal to ScalGGAC 
   ScalMP2C     0.35       # fraction of MP2 correlation
   RangeSepEXX  true       # activates range-separated exchange
   RangeSepMu   0.214013   # range-separation parameter, should be >0
   RangeSepScal 0.50       # fraction of variable HFX, should sum to 1 with ScalHFX and ScalDFX
end
%mp2
   DoSCS        true       # activates spin-component-scaling
   RI           true       # activate RI-MP2
   PS           1.333      # opposite-spin-scaling parameter
   PT           0.000      # same-spin-scaling parameter
end
```

Many other MP2 related options like the DLPNO treatment and ragularization can be found in the [MP2](../modelchemistries/MP2.md) section of the manual.

(tab:modelchemistries.dft.doublehybriddft.customization.keywords.block.method)=
:::{table} Most important `%method` block input keywords to customize double-hybrid functionals.
:class: footnotesize
| Keyword                         | Options              | Description                                                     |
|:--------------------------------|:---------------------|:----------------------------------------------------------------|
| `DoMP2`                         | `true`               | Activates MP2 correlation part                                  |
| `ScalMP2C`                      | `<real>`             | Controls the fraction of GGA exchange                           |
:::

(tab:modelchemistries.dft.doublehybriddft.customization.keywords.block.mp2)=
:::{table} Most important `%mp2` block input keywords to customize double-hybrid functionals. For more details see the [MP2 section](../modelchemistries/MP2.md).
:class: footnotesize
| Keyword                         | Options              | Description                                                     |
|:--------------------------------|:---------------------|:----------------------------------------------------------------|
| `DoSCS`                         | `true`               | Activates spin-component-scaling of MP2 part                    |
| `PS`                            | `<real>`             | Controls the opposite-spin-scaling parameter                    |
| `PT`                            | `<real>`             | Controls the same-spin-scaling parameter                        |
| `RI`                            | `true`               | Activates RI-MP2                                                |
| `DLPNO`                         | `true`               | Activates DLPNO-MP2                                             |
:::

```{index} Density Functional Theory; LibXC
```
(sec:modelchemistries.dft.libxc)=
## LibXC Functional Library

It is possible to use the functionals provided by
LibXC within the ORCA framework [^libxc]. The LibXC version used by ORCA is
printed at the beginning of the output. The LibXC reference should be
cited when LibXC is used as part of your calculations. For reference,
see {cite}`libxc`.

The complete list of functionals available via the LibXC interface can
always be inspected by typing at the command line

```orca
orca -libxcfunctionals
```

The list of functionals has the following form:

```orca
Functionals available via LibXC:
  No.:     ID / Keyword                    - Name
    0:     18 / lda_c_1d_csc               - Casula, Sorella & Senatore
    1:     26 / lda_c_1d_loos              - P-F Loos correlation LDA
    2:     15 / lda_c_2d_amgb              - AMGB (for 2D systems)
    3:     16 / lda_c_2d_prm               - PRM (for 2D systems)
    4:    552 / lda_c_br78                 - Brual & Rothstein 78

   ...
```

The list is grouped by "level" of functional (LDA, GGA, 
meta-GGA, etc.) and then by part of the energy it models 
(correlation, exchange, exchange-correlation).
Correlation functionals carry a `’_c_’` in their names, exchange
functionals an `’_x_’`, and combined exchange-correlation
functionals an `’_xc_’`. Additional information for a specific
functional can be requested using

```orca
orca -libxcinfo [functional name]
```

where the functional name is the keyword in the above list.

Specification of LibXC functionals in the ORCA input follows 
the standard format:

```orca
%method 
  Method     DFT
  Functional hyb_gga_xc_b3lyp
end
```

or in the case of separate exchange and correlation specifications:

```orca
%method 
  Method      DFT
  Exchange    mgga_x_m06_l
  Correlation mgga_c_m06_l
end
```

CAM-type range-separated functionals are supported through the LibXC
interface since ORCA 5.0. So are functionals that include non-local
(VV10) correlation (see {ref}`sec:modelchemistries.dispersioncorrections.nl.theory`). The VV10 part is computed
internally by ORCA. Other non-local functionals, such as BEEF-vdW, are
not supported. Meta-GGA functionals that depend on the kinetic energy density $\tau$
are supported, but not those that depend on the Laplacian of the density
$\nabla^2\rho$.

Double-hybrid functionals can be constructed with LibXC components as
described in the previous customization sections, but only with
separate exchange and correlation components. So `exchange=gga_x_pbe`
and `correlation=gga_c_pbe` can be used, but `functional=hyb_gga_xc_pbeh`
**cannot** be used in a double-hybrid formulation. Beware that the
exchange and correlation contributions calculated by LibXC are simply
scaled by `ScalDFX` and `ScalGGAC`, respectively, and no care is taken
to separately scale LDA components or alter other internal parameters!

(sec:modelchemistries.dft.libxc.screeningthresholds)=
### Screening Thresholds

When the density is smaller than a certain threshold, LibXC skips
the evaluation of the functional and instead sets all the output
quantities to zero in order to avoid under- and/or overflows. The
default thresholds for different functionals are set by the LibXC
developers, but may sometimes be too low. We have not performed
extensive testing, but allow the user to set the threshold. Similarly,
there are thresholds for minimum values of $\zeta$ and $\tau$ in order
to avoid division by zero. The default values are functional-independent
and can be changed using the following keywords.

```orca
%method 
  LibXCDensityThreshold 1e-12    # seems to be reasonable
  LibXCZetaThreshold    2e-16    # default value in LibXC
  LibXCTauThreshold     1e-20    # default value in LibXC
end
```

(sec:modelchemistries.dft.libxc.modifyingparameters)=
### Modifying LibXC Functional Parameters

Starting with ORCA 5.1 it is possible to modify the "external
parameters" of a functional that the LibXC interface provides.
The available parameters and their default values can be seen in the
output or with the `orca -libxcinfo` command above. Please exercise
caution when using this interface and if using a published functional
reparametrization, make sure you can reproduce results from the
original publication. The syntax requires one of the `ExtParamX`,
`ExtParamC`, or `ExtParamXC` keywords (depending on which functional is
modified), followed by the parameter name in quotation marks, and
finally the new value. For example, here is an input for the PWPB95
double-hybrid functional, where the simple input keyword is used to set
most parameters (such as the MP2 scaling factors) and only the exchange
and correlation parameters of the mPW91 and B95 LibXC functionals, respectively, are modified.

```orca
! Opt PWPB95 def2-SVP def2-SVP/C

%method
  Exchange    gga_x_mpw91
  Correlation mgga_c_bc95
  ExtParamX   "_bt"     0.00444
  ExtParamX   "_alpha" 19.823391
  ExtParamX   "_expo"   3.7868
  ExtParamC   "_css"    0.03241
  ExtParamC   "_copp"   0.00250
end

*xyz 0 1
  H 0 0 0
  F 0 0 0.9
*
```

Note that the variable definitions in LibXC may be different from the
ones used internally in ORCA or in the original publication, due to
various constant factors, etc. When in doubt, please consult the LibXC
documentation or source code repository --- we simply provide access to
the interface.


(sec:modelchemistries.dft.libxc.simpleinput)=
### Simple Input of LibXC Functionals

Some LibXC functionals are accessible via the simple input keyword
`!LibXC(Keyword)`, e.g. `!LibXC(TPSS)`. The keywords match those of the natively implemented in ORCA. Using this syntax, parameters for the
[DFT-D dispersion corrections](../modelchemistries/dispersioncorrections.md) are also set automatically (if
implemented). Table {numref}`tab:modelchemistries.dft.libxc.simpleinput` lists the available functionals and their
LibXC names.

(tab:modelchemistries.dft.libxc.simpleinput)=
:::{table} LibXC functionals available via the simple input `!LibXC(Keyword)`
:class: footnotesize
| Keyword                     | LibXC components                    | Notes                          |
|:----------------------------|:------------------------------------|:-------------------------------|
| **LDA functionals**         |                                     |                                |
| `PWLDA`                     | lda_x + gga_c\_pw                   |                                |
| `VWN5`                      | lda_x + gga_c\_vwn                  |                                |
| **GGAs**                    |                                     |                                |
| `B97-D`                     | gga_xc_b97_d                        | Uses D2                        |
| `B97-D3`                    | gga_xc_b97_d                        | Uses D3(0)                     |
| `B97-D4`                    | gga_xc_b97_d                        | Uses D4                        |
| `BLYP`                      | gga_x\_b88 + gga_c\_lyp             |                                |
| `BPBE`                      | gga_x\_b88 + gga_c\_pbe             |                                |
| `BPW91`                     | gga_x\_b88 + gga_c\_pw91            |                                |
| `BVWN`                      | gga_x\_b88 + lda_c\_vwn             |                                |
| `GLYP`                      | gga_x\_g96 + gga_c\_lyp             |                                |
| `KT2`                       | gga_xc_kt2                          |                                |
| `KT3`                       | gga_xc_kt3                          |                                |
| `MPWLYP`                    | gga_x\_mpw91 + gga_c\_lyp           |                                |
| `MPWPW`                     | gga_x\_mpw91 + gga_c\_pw91          |                                |
| `OPBE`                      | gga_x\_optx + gga_c\_pbe            |                                |
| `OLYP`                      | gga_x\_optx + gga_c\_lyp            |                                |
| `RPW86PBE`                  | gga_x\_rpw86 + gga_c\_pbe           |                                |
| `PW86PBE`                   | gga_x\_pw86 + gga_c\_pbe            |                                |
| `PW91`                      | gga_x\_pw91 + gga_c\_pw91           |                                |
| `PBE`                       | gga_x\_pbe + gga_c\_pbe             |                                |
| `RPBE`                      | gga_x\_rpbe + gga_c\_pbe            |                                |
| `REVPBE`                    | gga_x\_pbe + gga_c\_pbe             | $\kappa$=1.245                 |
| `XLYP`                      | gga\_xc\_xlyp                       |                                |
**meta-GGAs**                 |                                     |                                |
| `B97M-V`                    | mgga_xc_b97m_v                      | Uses VV10                      |
| `B97M-D3BJ`                 | mgga_xc_b97m_v                      | Uses D3(BJ)                    |
| `B97M-D4`                   | mgga_xc_b97m_v                      | Uses D4                        |
| `M06L`                      | mgga_x\_m06_l + mgga_c\_m06_l       |                                |
| `MN15L`                     | mgga_x\_mn15_l + mgga_c\_mn15_l     |                                |
| `MTASK-LDA`                 | mgga_x\_mtask + lda_c\_pw_mod       |                                |
| `MTASK-SCAN`                | mgga_x\_mtask + mgga_c\_scan        |                                |
| `REVTM`                     | mgga_x\_revtm + mgga_c\_revtm       |                                |
| `R2SCAN`                    | mgga_x\_r2scan + mgga_c\_r2scan     |                                |
| `RSCAN`                     | mgga_x\_rscan + mgga_c\_rscan       |                                |
| `SCAN`                      | mgga_x\_scan + mgga_c\_scan         |                                |
| `TASK-CCALDA`               | mgga_x\_task + mgga_c\_ccalda       |                                |
| `TASK-CC`                   | mgga_x\_task + mgga_c\_cc           |                                |
| `TASK-LDA`                  | mgga_x\_task + lda_c\_pw_mod        |                                |
| `TASK-SCAN`                 | mgga_x\_task + mgga_c\_scan         |                                |
| `TM`                        | mgga_x\_tm + mgga_c\_tm             |                                |
| `TPSS`                      | mgga_x\_tpss + mgga_c\_tpss         |                                |
| **Hybrid LDA functionals**  |                                     |                                |
| `HFLDA`                     | lda_x + lda_c\_pw                   |                                |
| **Hybrid GGAs**             |                                     |                                |
| `BHANDHLYP`                 | hyb_gga_xc_bhandhlyp                |                                |
| `B1LYP`                     | hyb_gga_xc_b1lyp                    |                                |
| `B1PW91`                    | hyb_gga_xc_b1pw91                   |                                |
| `B1PW`                      | gga_x\_b88,gga_c\_pw91              | Custom mixing                  |
| `B1PBE`                     | gga\_x\_b88 + gga\_c\_pbe           | Custom mixing                  |
| `B3PW91`                    | hyb\_gga\_xc\_b3pw91                | Custom mixing                  |
| `B3LYP`                     | hyb_gga_xc_b3lyp5                   |                                |
| `B3LYP/G`                   | hyb_gga_xc_b3lyp                    |                                |
| `B3LYPS`                    | hyb_gga_xc_b3lyps                   | B3LYP*, 15% HFX                |
| `BLYP35`                    | hyb_gga_xc_blyp35                   |                                |
| `B97`                       | hyb_gga_xc_b97                      |                                |
| `CAM-B3LYP`                 | hyb\_gga\_xc\_cam\_b3lyp            | Custom mixing                  |
| `CASE21`                    | hyb_gga_xc_case21                   |                                |
| `G1LYP`                     | gga\_x\_g96 + gga\_c\_lyp           | Custom mixing                  |
| `HSE03`                     | hyb_gga_xc_hse03                    |                                |
| `HSE12`                     | hyb_gga_xc_hse12                    |                                |
| `HSE12S`                    | hyb_gga_xc_hse12s                   |                                |
| `HSESOL`                    | hyb_gga_xc_hse_sol                  |                                |
| `KMLYP`                     | hyb_gga_xc_kmlyp                    |                                |
| `LB07`                      | hyb_gga_xc_lb07                     |                                |
| `LC-BLYP`                   | hyb\_gga\_xc\_lc\_blyp              | Custom mixing                  |
| `MPW1LYP`                   | hyb\_gga\_xc\_mpw1lyp               | Custom mixing                  |
| `MPW1PW`                    | hyb\_gga\_xc\_mpw1pw                | Custom mixing                  |
| `PBE0`                      | hyb_gga_xc_pbeh                     |                                |
| `PBE38`                     | hyb_gga_xc_pbe38                    |                                |
| `PBE50`                     | hyb_gga_xc_pbe50                    |                                |
| `PW91_0`                    | gga\_x\_pw91 + gga\_c\_pw91         | Custom mixing                  |
| `PW1PW`                     | gga\_x\_pw91 + gga\_c\_pw91         | Custom mixing                  |
| `REVPBE0`                   | gga_x\_pbe,gga_c\_pbe               | $\kappa$=1.245                 |
| `REVPBE38`                  | gga_x\_pbe,gga_c\_pbe               | 37.5% HFX, $\kappa$=1.245      |
| `WHPBE0`                    | hyb_gga_xc_whpbe0                   |                                |
| `WB97`                      | hyb_gga_xc_wb97                     |                                |
| `WB97X`                     | hyb_gga_xc_wb97x                    |                                |
| `WB97X-D3`                  | hyb_gga_xc_wb97x_d3                 | Uses D3(0)                     |
| `WB97X-V`                   | hyb_gga_xc_wb97x_v                  | Uses VV10                      |
| `WB97X-D3BJ`                | hyb_gga_xc_wb97x_v                  | Uses D3(BJ)                    |
| `WB97X-D4`                  | hyb_gga_xc_wb97x_v                  | Uses D4                        |
| `WB97X-D4REV`               | hyb_gga_xc_wb97x_v                  | Uses D4 with revised parameters        |
| **Hybrid meta-GGAs**        |                                     |                                |
| `GAS22`                     | hyb_mgga_xc_gas22                   |                                |
| `M05`                       | hyb_mgga_x\_m05 + mgga_c\_m05       |                                |
| `M052X`                     | hyb_mgga_x\_m05_2x + mgga_c\_m05_2x |                                |
| `M06`                       | hyb_mgga_x\_m06 + mgga_c\_m06       |                                |
| `M062X`                     | hyb_mgga_x\_m06_2x + mgga_c\_m06_2x |                                |
| `M06SX`                     | hyb_mgga_x\_m06_sx + mgga_c\_m06_sx |                                |
| `MN15`                      | hyb_mgga_x\_mn15 + mgga_c\_mn15     |                                |
| `LC-TMLYP`                  | hyb_mgga_xc_lc_tmlyp                |                                |
| `PW6B95`                    | hyb_mgga_xc_pw6b95                  |                                |
| `R2SCANH`                   | hyb_mgga_xc_r2scanh                 |                                |
| `R2SCAN0`                   | hyb_mgga_xc_r2scan0                 |                                |
| `R2SCAN38`                  | hyb_mgga_xc_r2scanh                 | 37.5% HFX                      |
| `R2SCAN50`                  | hyb_mgga_xc_r2scan50                |                                |
| `SCAN0`                     | hyb_mgga_x\_scan0 + mgga_c\_scan    |                                |
| `TPSS0`                     | hyb_mgga_xc_tpss0                   |                                |
| `TPSSH`                     | hyb_mgga_xc_tpssh                   |                                |
| `WB97M-V`                   | hyb_mgga_xc_wb97m_v                 | Uses VV10                      |
| `WB97M-D3BJ`                | hyb_mgga_xc_wb97m_v                 | Uses D3(BJ)                    |
| `WB97M-D4`                  | hyb_mgga_xc_wb97m_v                 | Uses D4                        |
| `WB97M-D4REV`               | hyb_mgga_xc_wb97m_v                 | Uses D4 with revised parameters      |
| **Double-hybrids**          |                                     |                                |
| `B2PLYP`                    | gga\_x\_b88 + gga\_c\_lyp           | Custom mixing                  |
| `B2GP-PLYP`                 | gga\_x\_b88 + gga\_c\_lyp           | Custom mixing                  |
| `B2T-PLYP`                  | gga\_x\_b88 + gga\_c\_lyp           | Custom mixing                  |
| `B2K-PLYP`                  | gga\_x\_b88 + gga\_c\_lyp           | Custom mixing                  |
| `B2NC-PLYP`                 | gga\_x\_b88 + gga\_c\_lyp           | Custom mixing                  |
| `DSD-PBEB95-D3`             | gga_x\_pbe + mgga_c\_bc95           | Custom mixing, uses D3(BJ)     |
| `DSD-PBEB95-D4`             | gga_x\_pbe + mgga_c\_bc95           | Custom mixing, uses D4         |
| `MPW2-PLYP`                 | gga\_x\_mpw91 + gga\_c\_lyp         | Custom mixing                  |
| `PWPB95`                    | gga_x\_mpw91 + mgga_c\_bc95         | Custom mixing and `ExtParam`'s |
| `PBE0-DH`                   | gga\_x\_pbe + gga\_c\_pbe           | Custom mixing                  |
| `PBE0-2`                    | gga\_x\_pbe + gga\_c\_pbe           | Custom mixing                  |
| `PBE-QIDH`                  | gga\_x\_pbe + gga\_c\_pbe           | Custom mixing                  |
| `PR2SCAN50`                 | mgga\_x\_r2scan + mgga\_c\_r2scan   | Custom mixing                  |
| `PR2SCAN69`                 | mgga\_x\_r2scan + mgga\_c\_r2scan   | Custom mixing                  |
| `SOS1-R2SCAN0-DH`           | mgga\_x\_r2scan + mgga\_c\_r2scan   | Custom mixing                  |
| `SOS1-R2SCAN-CIDH`          | mgga\_x\_r2scan + mgga\_c\_r2scan   | Custom mixing                  |
| `SOS1-R2SCAN-QIDH`          | mgga\_x\_r2scan + mgga\_c\_r2scan   | Custom mixing                  |
| `SOS1-R2SCAN0-2`            | mgga\_x\_r2scan + mgga\_c\_r2scan   | Custom mixing                  |
:::

[^libxc]: https://libxc.gitlab.io

