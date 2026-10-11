
<a id="sec:modelchemistries.dft"></a>
# Density Functional Theory (DFT)

Due to its good cost-accuracy ratio, Kohn-Sham density functional theory (DFT) has become the workhorse of quantum chemistry. 
Over the last few decades, a whole zoo of density functionals has been developed that differ in terms of their construction and design philosophy.
The so-called Jacob's Ladder picture ([fig:modelchemistries.dft.jacobsladder](#fig:modelchemistries.dft.jacobsladder)) coined by Perdew [perdew2001jacobsladder](../../bibliography.md) categorizes density functionals according to their basic physical ingredients into rungs .
With higher rungs. the cost of the given functionals increased but also higher accuracy is conceptionally expected. 
However, the accuracy of density functionals strongly varies and careful study of benchmark studies is generally recommended.

<a id="fig:modelchemistries.dft.jacobsladder"></a>
*:width: 400px

Jacob's ladder picture of density functionals.*

ORCA features various density functionals of each rung either implemented natively or via the [dft.libxc](#sec:modelchemistries.dft.libxc).
These functionals can be combined with various [basis sets](../essentialelements/basisset.md) and [relativistic approaches](../essentialelements/relativistic.md).
Further, ORCA features a useful toolkit of [resolution-of-identity (RI)](../essentialelements/RI.md) methods to speed-up DFT calculations.

For dispersion corrections that can be used with DFT and the respective available functional-specific parameters refer to the [Dispersion Corrections section](../modelchemistries/dispersioncorrections.md).

Also note that some functionals like the SCAN and Minnesota families may require enhanced [numerical integration grid settings](../essentialelements/numericalintegration.md).

<a id="sec:modelchemistries.dft.basicusage"></a>
## Basic Usage

All implemented DFT methods can be invoked via their respective keywords, e.g. `!PBE` using the simple input line:

```orca
! PBE
```
!!! warning
    If only a functional is defined, various default settings will be used including a small def2-SVP basis set, an appropriate [RI](../essentialelements/RI.md) treatment and default [numerical integration grids](../essentialelements/numericalintegration.md)! To achieve higher accuracy, specifically the [basis set](../essentialelements/basisset.md) should be adjusted!

Many functionals can also be invoked via the `%method` block even though double-hybrid functionals being not available due to technical reasons:

```orca
%method
   Method DFT        # equivalent to method DFGTO
   Functional PBE
end
```

ORCA further provides some more utility to construct and modify functionals via the `%method` block. These expert options are described in the respective sections of each functional rung. Various other functionals can also be invoked via the [dft.libxc](#sec:modelchemistries.dft.libxc).

!!! warning
    [RI](../essentialelements/RI.md#sec:essentialelements.ri)/[RIJCOSX](../essentialelements/RI.md#sec:essentialelements.ri.rijcosx) 
    are only activated by default if a DFT functional is chosen in the simple input!
    If the `%method` block is used instead,
    these approximations should be specified explicitly via `!RI` or `!RIJCOSX`.

<a id="sec:modelchemistries.dft.local"></a>
## Local Functionals 

Local exchange-correlation functionals are the most basic examples of functionals constructed according to equation [Eq](#eqn:modelchemistries.dft.gga.exlocal):

<a id="eqn:modelchemistries.dft.gga.exlocal"></a>

$$
E_{\text{XC} } = E_{\text{LSD} }^{\text{X} } + E_{\text{LSD} }^{\text{C} }\qquad \text{(eqn:modelchemistries.dft.gga.exlocal)}
$$

They typically the original Slater exchange functional with different local correlations functionals like VWN-V[vosko1980can](../../bibliography.md) or PW-LDA[perdew1992physb](../../bibliography.md).
All available local functional that are available in ORCA can be found in [tab:modelchemistries.dft.local](#tab:modelchemistries.dft.local).

<a id="tab:modelchemistries.dft.local"></a>
!!! note "List of available local functionals."
    | Functional                           | Keywords     | Description                                                 |
    |:-------------------------------------|:-------------|:------------------------------------------------------------|
    | HFS                                  | `HFS`        | Hartree--Fock--Slater Exchange only functional              |
    | LDA or LSD                           | `LDA`, `LSD` | Local density approximation (defaults to VWN5)              |
    | VWN-V [vosko1980can](../../bibliography.md)           | `VWN`,`VWN5` | Vosko-Wilk-Nusair local density approx. parameter set "V"   |
    | VWN-III [vosko1980can](../../bibliography.md)         | `VWN3`       | Vosko-Wilk-Nusair local density approx. parameter set "III" |
    | PW-LDA [perdew1992physb](../../bibliography.md)       | `PWLDA`      | Perdew-Wang parameterization of LDA                         |

<a id="sec:modelchemistries.dft.gga"></a>
## Gradient Corrected Functionals: (meta-)GGAs

The next rung corresponds to gradient corrected functional of the generalized gradient approximation (GGA) and the meta-generalized gradient approximation (meta-GGA) types.
A simplified exchange-correlation energy expression for these types of functionals is given in [Eq](#eqn:modelchemistries.dft.gga.excgga). (meta-)GGAs are specifically useful for 
[geometry optimizations](../structurereactivity/optimizations.md) and screening purposes due to their comparably small computational cost.

<a id="eqn:modelchemistries.dft.gga.excgga"></a>

$$
E_{\text{XC} } = E_{\text{LSD} }^{\text{X} } + E_{\text{GGA} }^{\text{X} } + E_{\text{LSD} }^{\text{C} } + E_{\text{GGA} }^{\text{C} }\qquad \text{(eqn:modelchemistries.dft.gga.excgga)}
$$

<a id="tab:modelchemistries.dft.gga"></a>
!!! note "List of available (meta-)GGA functionals."
    | Functional      | Keyword | Description |
    |:----------------|:--------|:------------|
    | **GGAs** | | |
    | BP86 [becke1988phys, perdew1986phys](../../bibliography.md) | `BP86`       | Becke '88 exchange and Perdew '86 correlation  |
    | BLYP [BLYP](../../bibliography.md) | `BLYP`       | Becke '88 exchange and Lee-Yang-Parr correlation  |
    | OLYP [handy2001molphys](../../bibliography.md) | `OLYP`       | Handy's "optimal" exchange and Lee-Yang-Parr correlation  |
    | GLYP [gill1996mol](../../bibliography.md) | `GLYP`       | Gill's '96 exchange and Lee-Yang-Parr correlation  |
    | XLYP [goddard2004pnas](../../bibliography.md) | `XLYP`       | The Xu and Goddard exchange and Lee-Yang-Parr correlation  |
    | PW91 [perdew1991pw91](../../bibliography.md) | `PW91`       | Perdew-Wang '91 GGA functional  |
    | mPWPW [barone1997jcp](../../bibliography.md) | `MPWPW`      | Modified PW exchange and PW correlation  |
    | mPWLYP [barone1997jcp](../../bibliography.md) | `MPWLYP`     | Modified PW exchange and LYP correlation  |
    | PBE [perdew1996phys](../../bibliography.md) | `PBE`        | Perdew-Burke-Erzerhoff GGA functional  |
    | RPBE [hammer1999phys](../../bibliography.md) | `RPBE`      | "Modified" PBE  |
    | revPBE [zhang1998phys](../../bibliography.md) | `REVPBE`     | "Revised" PBE  |
    | RPW86PBE [rPW86PBE](../../bibliography.md) | `RPW86PBE`   | PBE correlation with refitted Perdew '86 exchange  |
    | PWP [perdew1991pw91](../../bibliography.md) | `PWP` | Perdew-Wang '91 exchange and Perdew '86 correlation  |
    | **composite** | | |
    | B97-3c [grimme2018b973c](../../bibliography.md) | `B97-3C` | Composite DFT method by Grimme et al. |
    | **meta-GGAs** | | |
    | B97M-V [headgordon2015B97MV](../../bibliography.md)    | `B97M-V` | Head-Gordon's DF B97M-V with VV10 nonlocal correlation  |
    | B97M-D3(BJ) [goerigk2018](../../bibliography.md) | `B97M-D3BJ` | Modified version of B97M-V with D3BJ correction by Najibi and Goerigk  |
    | B97M-D4 [najibi2020](../../bibliography.md)   | `B97M-D4` | Modified version of B97M-V with DFT-D4 correction by Najibi and Goerigk  |
    | SCAN [perdew2015scan](../../bibliography.md)  | `SCANFUNC` | Perdew's SCAN functional  |
    | rSCAN [bartok2019rscan](../../bibliography.md)     | `RSCAN` | Regularized SCAN functional
    | r²SCAN [furness2020r2scan](../../bibliography.md)      | `R2SCAN` | Regularized and restored SCAN functional by Furness, Sun et al.  |
    | M06-L [m06l](../../bibliography.md)      | `M06L` | The Minnesota M06-L meta-GGA functional  |
    | TPSS [TPSS2003](../../bibliography.md)       | `TPSS` | The TPSS meta-GGA functional  |
    | revTPSS [revtpss, revtpsserratum](../../bibliography.md)       | `REVTPSS` | Revised TPSS meta-GGA functional  |
    | **composite** | | |
    | r²SCAN-3c [grimme2020r2scan3c](../../bibliography.md) | `R2SCAN-3C` | Composite DFT method by Grimme et al. |

<a id="sec:modelchemistries.dft.gga.customizexc"></a>
### Customization of Basic Functionals

Basic exchange-correlation functionals can also be constructed from their components via the `%method` block using the `Exchange`, `Correlation`, and `LDAOpt` keywords.
These controle the exchange and correlation parts of the functional as well as the local part of the correlation functional, respectively.
For example BP86 (`!BP86`) is constructed from Becke's ‘88 exchange via `X_BECKE` and Perdew's ‘86 correlation functional via `C_P86`. In ORCA, it further
employs Perdew and Wang's LDA reparameterization[perdew1992physb](../../bibliography.md) `PWLDA` for the local part of the correlation functional via `C_PWLDA`:

```orca
%method
   Method DFT
   Exchange     X_BECKE
   Correlation  C_P86
   LDAOpt       C_PWLDA
end
```

For a full list of available components see [tab:modelchemistries.dft.gga.customizexc.keywords.block](#tab:modelchemistries.dft.gga.customizexc.keywords.block).

The correct choice of the local part of the correlation functional is crucial to ensure
reproducibility of the results. In ORCA, almost all functionals choose `PWLDA`[perdew1992physb](../../bibliography.md) as the
underlying LDA functional as it represents a slightly better fit to
the uniform electron gas than VWN. For VWN (Vosko, Wilk, and Nusair[vosko1980can](../../bibliography.md)), several parameterizations
exist. In their classic paper give two sets of parameters -- one in
the main body (parametrization of RPA results; known as VWN-III) and
one in their table 5 of correlation energies (parametrization of the
Ceperley/Alder Monte Carlo results; known as VWN-V). The results from PW-LDA are very similar to those
of VWN-V, whereas VWN-III yields quite different values.
Over the years, the usage of different parameterizations for the same functional name throughout different quantum chemistry 
programs caused some confusion and deviating results. A prominent example is the different implementation of the
B3LYP [hybrid functional](#sec:modelchemistries.dft.globalhybrids) within ORCA and Gaussian. While ORCA uses VNW-V consistent 
with the TURBOMOLE program[ahlrichs2000turbo,ahlrichs2000ency,ahlrichs1989chem](../../bibliography.md), the Gaussian program[frisch1998gauss](../../bibliography.md)
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

!!! note
    A special situation arises if LYP is the
    correlation functional [lee1988phys](../../bibliography.md) since LYP is *not* a
    correction to the correlation, but rather includes the full correlation. 
    It is therefore used in the B3LYP functional as:

<a id="eqn:modelchemistries.dft.gga.customizexc.ecb3lyp"></a>

$$
E_{\text{B3LYP} }^{\text{C} } =E_{\text{LSD} }^{\text{C} } +c\left({ E_{\text{LYP} }^{\text{C} } -E_{\text{LSD} }^{\text{C} } } \right)\qquad \text{(eqn:modelchemistries.dft.gga.customizexc.ecb3lyp)}
$$

Some functionals further incorporate empirical parameters that can be changed to improve
agreement with experiment. Currently, there are a few parameters that can
be changed (other than the parameters used in the [hybrid functionals](#sec:modelchemistries.dft.hybriddft),
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
correlation functional, there is $\beta_C$ (not to be confusedwith the $\beta$ exchange parameter in Becke's exchange functional), whose
original value is $\beta_C=0.066725$. Modified variants exist with different
$\beta_C$ values, e.g., the PBEsol functional and the [PBEh-3ccomposite method](3cmethods.md#sec:modelchemistries.3cmethods.pbeh3c). Furthermore, the $\mu$ parameter in the PBE exchange
functional may be modified. In the original formulation, it is related to
$\beta_C$ via $\mu = \beta_C \frac{\pi^{2} }{3}$, but has been modified
in later variants as well.
<a id="tab:modelchemistries.dft.gga.customizexc.keywords.block"></a>
!!! note "`%method` block input keywords to modify basic exchange-correlation functionals."
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
    | `XAlpha`                        | `<real>`          | Modifies Slater's $\alpha$ parameter (default 2/3)                  || `XBeta`                         | `<real>`          | Modifies Becke's $\beta$ parameter (default 0.0042)                 |
    | `XKappa`                        | `<real>`          | Modifies the PBE(exchange) $\kappa$ parameter (default 0.804)       || `XMuePBE`                       | `<real>`          | Modifies the PBE(exchange) $\kappa$ parameter (default 0.21952)     |
    | `CBetaPBE`                      | `<real>`          | Modifies the PBE(correlation) beta parameter (default 0.066725)     |
<a id="sec:modelchemistries.dft.hybriddft"></a>
## Hybrid DFT
The idea of replacing a portion of the DFT exchange by exact exchange from Hartree-Fock theory (HFX) was introduced by Becke in 1993[becke1993chem1,becke1993chem2](../../bibliography.md).
This scheme is typically referred to as hybrid DFT and the most simple formulation of a one-parameter hybrid functional is depicted in equation [Eq](#eqn:modelchemistries.dft.hybriddft.exchybrid)
<a id="eqn:modelchemistries.dft.hybriddft.exchybrid"></a>

$$
E_{\text{hyb}}^{\text{XC}} =aE_{\text{HF}}^{\text{X}} + (1-a){ E_{\text{GGA}}^{\text{X}}} + E_{\text{GGA}}^{\text{C}}\qquad \text{(eqn:modelchemistries.dft.hybriddft.exchybrid)}
$$

A more general description is given by the adiabatic connection model (ACM). In the ACM, hybrid functionals are constructed with three parameters according to equation [Eq](#eqn:modelchemistries.dft.hybriddft.acm):
<a id="eqn:modelchemistries.dft.hybriddft.acm"></a>

$$
E_{\text{XC} } = a E_{\text{HF} }^{\text{X} } +\left( 1 - a \right)E_{\text{LSD} }^{\text{X} } +bE_{\text{GGA} }^{\text{X} } +E_{\text{LSD} }^{\text{C} } +cE_{\text{GGA} }^{\text{C} }\qquad \text{(eqn:modelchemistries.dft.hybriddft.acm)}
$$

Here, $E_{\text{XC} }$ is the total exchange/correlation energy,$E_{\text{HF} }^{\text{X} }$ is the Hartree-Fock exchange,
$E_{\text{LSD} }^{\text{X} }$ is the local (Slater) exchange,$E_{\text{GGA} }^{\text{X} }$ is the gradient correction to the
exchange, $E_{\text{LSD} }^{\text{C} }$ is the local, spin-density basedpart of the correlation energy, and $E_{\text{GGA} }^{\text{C} }$ is the
gradient correction to the correlation energy. 
Over the years, various strategies to construct hybrid functionals have been developed. These range from physics motivated approaches relying on as few as possible parameters like the overall well-balanced PBE0 functional[adamo1999chem](../../bibliography.md) to more empirical variants like the prominent three-parameter hybrid B3LYP[b3lyp](../../bibliography.md). 
Furthermore, various treatments of the HF exchange admixture were developed. The basic hybrids that use a static amount of HFX are typically referred to as [global hybrids](#sec:modelchemistries.dft.globalhybrids) while functionals with variable amounts of HFX include [range-separated hybrids](#sec:modelchemistries.dft.hybriddft.rangeseparatedhybrids) and local hybrids. Various [global](#sec:modelchemistries.dft.globalhybrids) and [range-separated hybrid functionals](#sec:modelchemistries.dft.hybriddft.rangeseparatedhybrids) are available in ORCA. Local hybrids may be implemented in a future version.
ORCA also provides a sophisticated infrastructure to create and [customize global](#sec:modelchemistries.dft.globalhybrids.customization) and [range-separated hybrid functionals](#sec:modelchemistries.dft.rangeseparatedhybrids.customization).
!!! note
    As by theory hybrid functionals are significantly more costly than (meta-)GGAs, ORCA uses the sophisticated [RIJCOSX](../essentialelements/RI.md) algorithm as a default to 
    speed up hybrid DFT calculations.
<a id="sec:modelchemistries.dft.globalhybrids"></a>
### Global Hybrid Functionals
Global hybrid functionals employ a fixed amount of Hartree-Fock exact exchange. ORCA features various
representatives with different compositions and amounts of HFX. The optimal amount of HFX is controversially discussed in the literature
and many empirical functionals were constructed by fitting it to reproduce an experimental property.
However, it has been argued from a theoretical viewpoint that the optimal mixing of HF exchange is 25%
[ernzerhof1998density](../../bibliography.md) and large amounts of HFX are known to be disadvantageous for transition metal complexes.
A list of natively implemented global hybrid functionals is given in [tab:modelchemistries.dft.hybriddft.globlhybrids](#tab:modelchemistries.dft.hybriddft.globlhybrids).
<a id="tab:modelchemistries.dft.hybriddft.globlhybrids"></a>
!!! note "List of available global hybrid functionals."
    | Functional                                    | Keyword       | %HFX  | Description                                                                                                  |
    |:----------------------------------------------|:--------------|:-----:|:-------------------------------------------------------------------------------------------------------------|
    | **hybrid GGAs**                               |               |       |                                                                                                              |
    | B1LYP [adamo1997b1lyp](../../bibliography.md)                  | `B1LYP`       | 25    | The one-parameter hybrid functional with Becke '88 exchange and Lee-Yang-Parr correlation (25% HF exchange)  |
    | B3LYP [b3lyp](../../bibliography.md)                           | `B3LYP`       | 20    | The popular B3LYP functional (20% HF exchange) as defined in the TurboMole program system (`LDAOPT C_VWN5`)  |
    | B3LYP/G [b3lyp](../../bibliography.md)                         | `B3LYP/G`     | 20    | The popular B3LYP functional (20% HF exchange) as defined in the Gaussian program system (`LDAOPT C_VWN3`)   |
    | O3LYP [cohen2001o3lyp](../../bibliography.md)                  | `O3LYP`       | 11.61 | The Handy hybrid functional                                                                                  |
    | X3LYP [goddard2004pnas](../../bibliography.md)                 | `X3LYP`       | 21.8  | The Xu and Goddard hybrid functional                                                                         |
    | B1P86 [perdew1986phys](../../bibliography.md)                  | `B1P86`       | 25    | The one-parameter hybrid version of BP86                                                                     |
    | B3P86 [becke1993chem1](../../bibliography.md)                  | `B3P86`       | 20    | The three-parameter hybrid version of BP86                                                                   |
    | B3PW91 [becke1993chem1](../../bibliography.md)                 | `B3PW91`      | 20    | The three-parameter hybrid version of PW91                                                                   |
    | PW1PW [adamo1999chem](../../bibliography.md)                   | `PW1PW`       | 25    | One-parameter hybrid version of PW91                                                                         |
    | mPW1PW [barone1997jcp](../../bibliography.md)                  | `MPW1PW`      | 25    | One-parameter hybrid version of mPWPW                                                                        |
    | mPW1LYP [barone1997jcp](../../bibliography.md)                 | `MPW1LYP`     | 25    | One-parameter hybrid version of mPWLYP                                                                       |
    | PBE0 [adamo1999chem](../../bibliography.md)                    | `PBE0`        | 25    | One-parameter hybrid version of PBE                                                                          |
    | revPBE0 [grimme2011gmtkn30](../../bibliography.md)             | `REVPBE0`     | 25    | "Revised" PBE0                                                                                               |
    | revPBE38 [grimme2011gmtkn30](../../bibliography.md)            | `REVPBE38`    | 37.5  | "Revised" PBE0 with 37.5% HF exchange                                                                        |
    | BHandHLYP [becke1993chem1](../../bibliography.md)              | `BHANDHLYP`   | 50    | Half-and-half hybrid functional by Becke                                                                     |
    | **hybrid meta-GGAs**                          |               |       |                                                                                                              |
    | M06 [m06](../../bibliography.md)                               | `M06`         | 27    | |
    | M06-2X [m06](../../bibliography.md)                            | `M062X`       | 54    | |
    | PW6B95 [zhao2005phys](../../bibliography.md)                   | `PW6B95`      | 28    | |
    | TPSSh [TPSS2003](../../bibliography.md)                        | `TPSSH`       | 10    | The hybrid version of TPSS (10% HF exchange)                                                                 |
    | TPSS0  [grimme2005tpss0](../../bibliography.md)                | `TPSS0`       | 25    | A 25% exchange version of TPSSh that yields improved energetics                                              |
    | r²SCANh [bursch_r2scanhybrids_2022](../../bibliography.md)     | `R2SCANH`     | 10    | Global hybrid variant of r²SCAN with 10% HF exchange                                                         |
    | r²SCAN0 [bursch_r2scanhybrids_2022](../../bibliography.md)     | `R2SCAN0`     | 25    | Global hybrid variant of r²SCAN with 25% HF exchange                                                         |
    | r²SCAN50 [bursch_r2scanhybrids_2022](../../bibliography.md)    | `R2SCAN50`    | 50    | Global hybrid variant of r²SCAN with 50% HF exchange                                                         |
    | **composite**                                 |               |       |                                                                                                              |
    | PBEh-3c [grimme_pbeh3c](../../bibliography.md)                 | `PBEH-3C`     | 42    | Composite DFT approach by Grimme et al.                                                                      |
    | B3LYP-3c [grimme2020b3lyp3c](../../bibliography.md)            | `B3LYP-3C`    | 20    | Composite DFT approach by Grimme et al.                                                                      |
<a id="sec:modelchemistries.dft.globalhybrids.customization"></a>
#### Customization of Global Hybrids
Global hybrid functional parameters can be customized via the `%method` block. For the customization of the basic exchange and correlation components
see the [Customization of Basic Functionals](#sec:modelchemistries.dft.gga.customizexc) section. The important parameters for hybrid functionals are
those used in the ACM model (cf. equation [Eq](#eqn:modelchemistries.dft.hybriddft.acm)). In this case, we will recreate the PBE0 functional (25% HFX) by
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
!!! warning
    Note that `Functional` chooses specific predefined values
    for the variables `Exchange`, `Correlation`, `LDAOpt` and `ACM` described below.
    If given as a simple input keyword, in some cases, it will also activate
    a dispersion correction. You can explicitly give these variables instead
    or in addition to `Functional`. However, make sure that you specify
    these variables *after* you have assigned a value to `Functional` or the
    others will be reset to the values chosen by `Functional`.
<a id="tab:modelchemistries.dft.globalhybrids.customization.keywords.block"></a>
!!! note "`%method` block input keywords to modify global hybrid functionals."

| ****Keyword**** | Options | Description |
| --- | --- | --- |
| **`ACM`** | `<real, real, real>` | Defines the ACM-A, ACM-B, and ACM-C parameters |
| **`ACM_A`** | `<real>` | Defines the ACM-A parameter (fraction of Hartree-Fock exchange) |
| **`ACM_B`** | `<real>` | Defines the ACM-B parameter (fraction of GGA exchange) |
| **`ACM_C`** | `<real>` | Defines the ACM-C parameter (fraction of GGA correlation) |
| **`ScalHFX`** | `<real>` | Controls the fraction of Hartree-Fock exchange, equiv. to `ACM_A` |
| **`ScalDFX`** | `<real>` | Controls the fraction of GGA exchange, equiv. to `ACM_B` |
| **`ScalGGAC`** | `<real>` | Controls the fraction of GGA correlation, equiv. to `ACM_C` |

<a id="sec:modelchemistries.dft.hybriddft.rangeseparatedhybrids"></a>
### Range-Separated Hybrid Functionals
Unlike [global hybrids](#sec:modelchemistries.dft.globalhybrids), range-separated hybrid (RSH) split the two-electron operator used for the exchange into a short-range (SR) and a long-range (LR) regime wherein the short-range part is typically described by DFT exchange and the long-range part by Hartree-Fock exchange. In ORCA, all range-separated hybrids use the error function splitting approach by Hirao and coworkers to distinguish both regimes (cf. equation [Eq](#eqn:modelchemistries.dft.hybriddft.rangeseparatedhybrids.erf)).[hirao2001rangeseparation](../../bibliography.md) This allows the definition of DFT functionals that dominate the short-range part by an adapted exchange functional of [LDA](#sec:modelchemistries.dft.local), [GGA or meta-GGA](#sec:modelchemistries.dft.gga) level and the long-range part by Hartree-Fock exchange.
<a id="eqn:modelchemistries.dft.hybriddft.rangeseparatedhybrids.erf"></a>

$$
r_{12}^{-1} = \underbrace{\text{erfc}(\mu \cdot r_{12}) \cdot r_{12}^{-1} }_{\text{SR} } + \underbrace{\text{erf}(\mu \cdot r_{12}) \cdot r_{12}^{-1} }_{\text{LR} }\qquad \text{(eqn:modelchemistries.dft.hybriddft.rangeseparatedhybrids.erf)}
$$

where
$\text{erf}(x) = \frac{2}{\sqrt{\pi} } \in t_{0}^{x} \exp(-t^{2}) dt$ and$\text{erfc}(x) = 1 - \text{erf}(x)$. Note that the splitting is only
applied to the exchange contribution; all other contributions (one-electron
parts of the Hamiltonian, the electron-electron Coulomb interaction and the 
approximation for the DFT correlation) are not affected. Later, Handy and coworkers[handy2004CAMB3LYPLC](../../bibliography.md) generalized the
ansatz to:
<a id="eqn:modelchemistries.dft.hybriddft.rangeseparatedhybrids.erfgeneralized"></a>

$$
r_{12}^{-1} = \underbrace{\frac{1 - [ \alpha + \beta \cdot \text{erf}(\mu \cdot r_{12})]}{ r_{12} }}_{\text{SR} } + \underbrace{\frac{\alpha + \beta \cdot \text{erf}(\mu \cdot r_{12}) }{r_{12} }}_{\text{LR} }\qquad \text{(eqn:modelchemistries.dft.hybriddft.rangeseparatedhybrids.erfgeneralized)}
$$

This form of the splitting used in ORCA is shown visually (according to Handy
and coworkers) in [fig:modelchemistries.dft.hybriddft.rangeseparatedhybrids.ansatz](#fig:modelchemistries.dft.hybriddft.rangeseparatedhybrids.ansatz).
<a id="fig:modelchemistries.dft.hybriddft.rangeseparatedhybrids.ansatz"></a>
*Graphical description of the range-separation ansatz. The gray area
corresponds to Hartree-Fock exchange. $\alpha$ and $\beta$ follow
Handy's terminology [handy2004CAMB3LYPLC](../../bibliography.md).*
!!! warning
    Currently, RSH functionals can be used for integral-direct single-point calculations, calculations
    involving the first nuclear gradient (i.e. geometry optimizations),
    frequency calculations, TDDFT, TDDFT nuclear gradient, and EPR/NMR calculations.
    As with the [global hybrids](#sec:modelchemistries.dft.globalhybrids), [RIJCOSX](../essentialelements/RI.md) is used by default
    to drastically speed up the calculations. Alternatively, only RIJONX can be used.
A list of available range-separated hybrid functionals is given in [tab:modelchemistries.dft.rangeseparatedhybrids](#tab:modelchemistries.dft.rangeseparatedhybrids)
<a id="tab:modelchemistries.dft.rangeseparatedhybrids"></a>
!!! note "List of available range-separated hybrid functionals. $\mu$ is the range-separation parameter."| Functional                                        | Keyword        | %HFX             | $\mu$ / $\text{bohr}^{-1}$ | % fixed DFX |
    |:--------------------------------------------------|:---------------|:----------------:|:--------------------------:|:-----------:|
    | **hybrid GGAs**                                   |                |                  |                            |             |
    | $\omega$B97 [headgordon2008wB97wB97X](../../bibliography.md)       | `WB97`         | 0 -- 100         | 0.40                       | ---         |
    | $\omega$B97X [headgordon2008wB97wB97X](../../bibliography.md)      | `WB97X`        | 15.7706 -- 100   | 0.30                       | ---         |
    | $\omega$B97X-V [headgordon2014wB97XV](../../bibliography.md)       | `WB97X-V`      | 16.7 -- 100      | 0.30                       | ---         |
    | $\omega$B97X-D3 [chai2013wB97XD3](../../bibliography.md)           | `WB97X-D3`     | 19.5728 -- 100   | 0.25                       | ---         |
    | $\omega$B97X-D3(BJ) [goerigk2018](../../bibliography.md)           | `WB97X-D3BJ`   | 16.7 -- 100      | 0.30                       | ---         |
    | $\omega$B97X-D4 [najibi2020](../../bibliography.md)                | `WB97X-D4`     | 16.7 -- 100      | 0.30                       | ---         |
    | $\omega$B97X-D4rev[grimme2022wb97x3c](../../bibliography.md)       | `WB97X-D4REV`  | 16.7 -- 100      | 0.30                       | ---         |
    | CAM-B3LYP [handy2004CAMB3LYPLC](../../bibliography.md)             | `CAM-B3LYP`    | 19 -- 65         | 0.33                       | 35%         |
    | LC-BLYP [hirao2004LC_TDDFT](../../bibliography.md)                 | `LC-BLYP`      | 0 -- 100         | 0.33                       | ---         |
    | LC-PBE [hirao2001rangeseparation](../../bibliography.md)           | `LC-PBE`       | 0 -- 100         | 0.47                       | ---         |
    | **hybrid meta-GGAs**                              |                |                  |                            |             |
    | $\omega$B97M-V [headgordon2016wB97MV](../../bibliography.md)       | `WB97M-V`      | 15 -- 100        | 0.30                       | ---         |
    | $\omega$B97M-D3(BJ) [goerigk2018](../../bibliography.md)           | `WB97M-D3BJ`   | 15 -- 100        | 0.30                       | ---         |
    | $\omega$B97M-D4 [najibi2020](../../bibliography.md)                | `WB97M-D4`     | 15 -- 100        | 0.30                       | ---         |
    | $\omega$B97M-D4rev [grimme2022wb97x3c](../../bibliography.md)      | `WB97M-D4REV`  | 15 -- 100        | 0.30                       | ---         |
    | $\omega$r²SCAN [Wittmann2023](../../bibliography.md)               | `WR2SCAN`      | 0 -- 100         | 0.30                       | ---         |
    | **composite**                                     |                |                  |                            |             |
    | $\omega$B97X-3c [grimme2022wb97x3c](../../bibliography.md)         | `WB97X-3C`     | 16.7 -- 100      | 0.30                       | ---         |
<a id="sec:modelchemistries.dft.rangeseparatedhybrids.customization"></a>
#### Customizing Range-Separated Hybrids
Range-separated hybrid functional parameters can also be customized via the `%method` block. For the customization of the basic exchange and correlation components
see the [Customization of Basic Functionals](#sec:modelchemistries.dft.gga.customizexc) section. Basic hybrid-related keywords and the respective ACM model are described in the [Hybrid DFT](#sec:modelchemistries.dft.hybriddft) and [Customization of Global Hybrids](#sec:modelchemistries.dft.globalhybrids.customization) sections.
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
!!! warning
    The amount of fixed DFT Exchange (`ACM_B` or `ScalDFX`) can
    only be changed for CAM-B3LYP and LC-BLYP. Accordingly, ACM-B is
    ignored by the $\omega$B97 approaches as no corresponding
    $\mu$-independent exchange functional has been defined. While
    it is technically possible to choose an exchange functional that has no
    $\mu$-dependence, this makes no sense conceptually.
<a id="tab:modelchemistries.dft.rangeseparatedhybrids.customization.keywords.block"></a>
!!! note "`%method` block input keywords to modify range-separated hybrid functionals."
    | Keyword                         | Options              | Description                                                     |
    |:--------------------------------|:---------------------|:----------------------------------------------------------------|
    | `RangeSepEXX`                   | `true`               | Activates range-separated exchange                              |
    | `RangeSepMu`                    | `<real>`             | Controls the range-separation parameter, should be >0           |
    | `RangeSepScal`                  | `<real>`             | Controls the fraction of variable Hartree-Fock exchange         |
<a id="sec:modelchemistries.dft.doublehybriddft"></a>
## Double-Hybrid DFT
In addition to mixing the HF-exchange into a given density functional, Grimme has proposed to mix in a fraction of
the [MP2 correlation energy](../modelchemistries/MP2.md) as calculated with hybrid DFT
orbitals [Grimme2006jcp](../../bibliography.md). Such functionals may be referred to as
"double-"hybrid functionals. The original expression by Grimme is:
<a id="eqn:modelchemistries.dft.doublehybriddft.exc"></a>

$$
E_{\text{XC}} = aE_{\text{X}}^{\text{HF}} +\left({1-a} \right)E_{\text{X}}^{\text{DFT}} +\left({1-c}
\right)E_{\text{C}}^{\text{DFT}} +cE_{\text{C}}^{\text{MP2}}\qquad \text{(eqn:modelchemistries.dft.doublehybriddft.exc)}
$$

The first proposed double-hybrid functional by Grimme was B2PLYP.[Grimme2006jcp](../../bibliography.md) This double-hybrid functional utilizes the B88 exchange functional and the LYP correlation
functionals. It introduces 53% of Hartree-Fock exchange ($a = 0.53$) and replaces 27% of the DFT correlation energy by MP2 correlation energy ($c = 0.27$).
Since then many other DH-DFT approaches that deviate from the original theme were developed. For example Grimme proposed DH functionals like PWPB95[goerigk2011chem](../../bibliography.md) that use spin-component-scaled MP2. 
Further, functionals whose composition was empirically fitted against databases without any physical constraints or restrictions as previously proposed in [Eq](#eqn:modelchemistries.dft.doublehybriddft.exc) 
like Martin's DSD (dispersion corrected, spin-component scaled double-hybrid) functionals[martin2010dsd,martin2011dsd,martin2013dsd](../../bibliography.md) were developed and refined with revDSD-PBEP86-D4[martin2021revdsd](../../bibliography.md) being one of 
the most well known representatives. Functionals of the XYG$n$ family[goddard2009xyg](../../bibliography.md) or Head-Gordon's $\omega$B97M(2)[Mardirossian2018](../../bibliography.md) employ differently constructed densities for the DFT and the 
perturbation-theory parts with the latter also basing on a [range-separated hybrid functional](#sec:modelchemistries.dft.hybriddft.rangeseparatedhybrids).
In principle, other correlated methods like dRPA or higher order MP theory may be used within the double hybrid scheme. However, the most common approach employs classical [MP2](../modelchemistries/MP2.md) or its spin-component-scaled variants. The [DLPNO approximation to MP2](MP2.md#sec:modelchemistries.mp2.dlpno) is also available within ORCA and can
be used to massively speed up the energy and gradient calculations for large systems. The accuracy and efficiency of DLPNO-DHs was extensively studied
by Bursch, Neese and co-workers[bursch2023dlpnodhs](../../bibliography.md).
Common to almost all double-hybrid functionals is a comparably large amount of Hartree-Fock exchange of 50% and more.
Most classical double-hybrid functionals following the scheme by Grimme can be utilized for single point calculations, analytic gradients
(and thus also geometry optimizations[Neese2007doublehybrid](../../bibliography.md), relaxed scans, and transition
state searches), dipole moments and other first order properties, magnetic second order properties
(chemical shifts and g-tensors without the frozen core approximation in the MP2 part), as well as for numerical polarizabilities
and frequencies. 
Some double-hybrid functionals were further optimized for excited state applications and will make use of a [Doubles Corrections](../spectroscopyproperties/tddft.md#sec:spectroscopyproperties.tddft.doubles) to correct the singles-only excited states within the [time-dependent DFT (TD-DFT)](../spectroscopyproperties/excitedstates.md#sec:spectroscopyproperties.excitedstates.tddft) framework. Some of them, 
like SCS-PBE-QIDH only make use of spin-component-scaling for the CIS(D) component of the calculation. However, many of them have recently also been
tested for ground-state properties.[GS_RSDHDFs](../../bibliography.md)
!!! note
    ORCA employs the [RIJCOSX](../essentialelements/RI.md) and [RI-MP2](../essentialelements/RI.md) by default. If this is not wanted, RI can be deactivated generally by using the `!NORI` 
    keyword or if only the RI approximation of the MP2 part should be deactivated via the `%mp2` block:
    ```orca
    %mp2
       RI false
    end
    ```
    Indeed, there is hardly ever any reason to use conventional MP2.
!!! note
    Note that per default no MP2 response density is calculated as its construction adds
    significant overhead. In this case, only the double-hybrid energy is correct. 
    The computation of the MP2 response density that is consistent with first-order properties from analytic first-derivatives can be requested
    via the `%mp2 density relaxed end` statement in the `%mp2` block. The considerably less costly unrelaxed (expectation value-like) density 
    may instead requested by `%mp2 density unrelaxed end`. However, this is not recommended
    since the changes to the relaxed density are considerable in our
    experience and the unrelaxed density has a much weaker theoretical
    status than its relaxed counterpart.
<a id="sec:modelchemistries.dft.doublehybriddft.globaldoublehybrids"></a>
### Global Double-Hybrid Functionals
Global double-hybrid functionals are based on the respective [global hybrid functionals](#sec:modelchemistries.dft.globalhybrids)
and employ static admixtures of [Hartree-Fock](hartreefock.md#sec:essentialelements.hartreefock) exchange and [the MP2 correlation energy](../modelchemistries/MP2.md). 
A list of currently implemented global double-hybrid functionals is given in [tab:modelchemistries.dft.doublehybriddft.globaldoublehybrids](#tab:modelchemistries.dft.doublehybriddft.globaldoublehybrids). 
The revDSD-PBEP86-D4[martin2021revdsd](../../bibliography.md) by Martin and co-workers has proven to be accurate for most thermochemistry applications. 
!!! warning
    For some functionals of the DSD/DOD family, different parameters for the same functional name were provided by the authors. The employed parameterization
    is indicated by the `(year-of-publication)` suffix of the functional and the respective keywords. Also not that for some of them, the basic parameters change
    in presence of different [dispersion corrections](../modelchemistries/dispersioncorrections.md). Please carefully check, if the employed parameters agree
    with your expectations!
!!! tip
    For most natively implemented double-hybrids you can simple add the `DLPNO-` prefix to the respective functional simple input keyword, e.g. `DLPNO-B2PLYP`.
    For all others, the DLPNO treatment can be activated via the `%mp2` block using the `DLPNO true` keyword.
<a id="tab:modelchemistries.dft.doublehybriddft.globaldoublehybrids"></a>
!!! note "List of available global double-hybrid functionals. `PS` is the opposite-spin, `PT` the same-spin scaling parameter. Excited-states optimized functionals only employ spin-component-scaling for the [CIS(D) doubles correction](../spectroscopyproperties/tddft.md#sec:spectroscopyproperties.tddft.doubles) within the the TD-DFT framework. Same-spin indirect term (CTss), opposite-spin indirect term (CTos), same-spin direct term (CUss), and opposite-spin direct term (CUos) parameters are given in the footnotes."

| | **Keywords** | `%HFX` | `%DFX` | `%GGAC` | `%MP2C` | `PS` | `PT` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Functional** | Keywords | `%HFX` | `%DFX` | `%GGAC` | `%MP2C` | `PS` | `PT` |
| **DSD-BLYP [martin2010dsd](../../bibliography.md)** | `DSD-BLYP D3BJ` | 69 | 31 | 54 | 100 | 0.46 | 0.37 |
| **DSD-BLYP-NoDisp(2013) [martin2013dsd](../../bibliography.md)** | `DSD-BLYP/2013` | 75 | 25 | 53 | 100 | 0.46 | 0.60 |
| **DSD-BLYP-D3(BJ)(2013) [martin2013dsd](../../bibliography.md)** | `DSD-BLYP/2013 D3BJ` | 71 | 29 | 54 | 100 | 0.47 | 0.40 |
| **DSD-PBEP86 [martin2011dsd](../../bibliography.md)** | `DSD-PBEP86 D3BJ` | 70 | 30 | 43 | 100 | 0.53 | 0.25 |
| **DSD-PBEP86-NoDisp(2013) [martin2013dsd](../../bibliography.md)** | `DSD-PBEP86/2013` | 72 | 28 | 44 | 100 | 0.51 | 0.36 |
| **DSD-PBEP86-D3(BJ)(2013) [martin2013dsd](../../bibliography.md)** | `DSD-PBEP86/2013 D3BJ` | 69 | 31 | 44 | 100 | 0.52 | 0.22 |
| **DSD-PBEB95-NoDisp [martin2013dsd](../../bibliography.md)** | `DSD-PBEB95` | 70 | 30 | 52 | 100 | 0.48 | 0.22 |
| **DSD-PBEB95-D3(BJ) [martin2013dsd](../../bibliography.md)** | `DSD-PBEB95 D3BJ` | 66 | 34 | 55 | 100 | 0.46 | 0.09 |
| **B2PLYP [Grimme2006jcp](../../bibliography.md)** | `B2PLYP` | 53 | 47 | 73 | 27 |  |  |
| **mPW2PLYP [Schwabe2006pccp](../../bibliography.md)** | `mPW2PLYP` | 55 | 45 | 75 | 25 |  |  |
| **B2GP-PLYP [b2gpplyp](../../bibliography.md)** | `B2GP-PLYP` | 65 | 35 | 64 | 36 |  |  |
| **B2K-PLYP [b2kplyp](../../bibliography.md)** | `B2K-PLYP` | 72 | 28 | 58 | 42 |  |  |
| **B2T-PLYP [b2kplyp](../../bibliography.md)** | `B2T-PLYP` | 60 | 40 | 69 | 31 |  |  |
| **B2NC-PLYP [b2ncplyp](../../bibliography.md)** | `B2NC-PLYP` | 81 | 19 | 45 | 55 |  |  |
| **PWPB95 [goerigk2011chem](../../bibliography.md)** | `PWPB95` | 50 | 50 | 73.1 | 26.9 | 1.0 | 0.0 |
| **PBE-QIDH [PBEQIDH](../../bibliography.md)** | `PBE-QIDH` | 69 | 31 | 67 | 33 |  |  |
| **PBE0-DH [PBE0DH](../../bibliography.md)** | `PBE0-DH` | 50 | 50 | 87.5 | 12.5 |  |  |
| **revDSD-PBEP86(2021) [martin2021revdsd](../../bibliography.md)** | `REVDSD-PBEP86/2021` | 69 | 31 | 42.24 | 100 | 0.5935 | 0.0566 |
| **revDSD-PBEP86-D4(2021) [martin2021revdsd](../../bibliography.md)** | `REVDSD-PBEP86-D4/2021` | 69 | 31 | 42.24 | 100 | 0.5935 | 0.0566 |
| **revDOD-PBEP86(2021) [martin2021revdsd](../../bibliography.md)** | `REVDOD-PBEP86/2021` | 69 | 31 | 43.01 | 100 | 0.6131 | 0.0 |
| **revDOD-PBEP86-D4(2021) [martin2021revdsd](../../bibliography.md)** | `REVDOD-PBEP86-D4/2021` | 69 | 31 | 43.01 | 100 | 0.6131 | 0.0 |
| **SOS1-r²SCAN-CIDH [Wittmann2023](../../bibliography.md)** | `R2SCAN-CIDH` | 55 | 45 | 83.33 | 16.67 | 1.333 | 0.0 |
| **SOS1-r²SCAN-QIDH [Wittmann2023](../../bibliography.md)** | `R2SCAN-QIDH` | 69.34 | 30.76 | 66.67 | 33.33 | 1.333 | 0.0 |
| **SOS1-r²SCAN0-2 [Wittmann2023](../../bibliography.md)** | `R2SCAN0-2` | 79.37 | 20.63 | 50 | 50 | 1.333 | 0.0 |
| **SOS1-r²SCAN0-DH [Wittmann2023](../../bibliography.md)** | `R2SCAN0-DH` | 50 | 50 | 87.50 | 12.50 | 1.333 | 0.0 |
| **Pr²SCAN50 [Wittmann2023](../../bibliography.md)** | `PR2SCAN50` | 50 | 50 | 75 | 25 | 1.333 | 0.0 |
| **Pr²SCAN69 [Wittmann2023](../../bibliography.md)** | `PR2SCAN69` | 69.34 | 30.76 | 55.56 | 44.44 | 1.333 | 0.0 |
| **$\kappa$Pr²SCAN50 [Wittmann2023](../../bibliography.md)** | `KPR2SCAN50` | 50 | 50 | 70 | 30 | 1.333 | 0.0 |
| ****excited state opt.**** |  |  |  |  |  |  |  |

| **SCS/SOS-B2PLYP21 [SCSTDDHDFs](../../bibliography.md)** | — |
      - `SCS/SOS-B2PLYP21`
      - 53
      - 47
      - 73
      - 27
      - [^a]
      - [^a]

| | **`SCS-PBE-QIDH`** | 69 | 31 | 67 | 33 | [^b] | [^b] |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **SCS-PBE-QIDH [SCSTDDHDFs](../../bibliography.md)** | `SCS-PBE-QIDH` | 69 | 31 | 67 | 33 | [^b] | [^b] |
| **SOS-PBE-QIDH [SCSTDDHDFs](../../bibliography.md)** | `SOS-PBE-QIDH` | 69 | 31 | 67 | 33 | [^c] | [^c] |
| **SCS-B2GP-PLYP21 [SCSTDDHDFs](../../bibliography.md)** | `SCS-B2GP-PLYP21` | 65 | 35 | 64 | 36 | [^d] | [^d] |
| **SOS-B2GP-PLYP21 [SCSTDDHDFs](../../bibliography.md)** | `SOS-B2GP-PLYP21` | 65 | 35 | 64 | 36 | [^e] | [^e] |

[^a]: SCS/SOS-B2PLYP21: CTss: 0.000; CTos: 0.334; CUss: 0.000; CUos: 0.283.
[^b]: SCS-PBE-QIDH: CTss: 0.070; CTos: 0.515; CUss: 0.096; CUos: 0.524.
[^c]: SOS-PBE-QIDH: CTss: 0.000; CTos: 0.547; CUss: 0.000; CUos: 0.573.
[^d]: SCS-B2GP-PLYP21: CTss: 0.018; CTos: 0.475; CUss: 0.000; CUos: 0.468.
[^e]: SOS-B2GP-PLYP21: CTss: 0.000; CTos: 0.489; CUss: 0.000; CUos: 0.484.
<a id="sec:modelchemistries.dft.doublehybriddft.rangeseparateddoublehybrids"></a>
### Range-Separated Double-Hybrid Functionals
Range-separated double-hybrids employ variable amounts of Hartree-Fock exchange much like
[range-separated hybrid functionals](#sec:modelchemistries.dft.hybriddft.rangeseparatedhybrids) 
and static amounts of [MP2 correlation](../modelchemistries/MP2.md). A list of available range-separated
double-hybrid functionals is given in [tab:modelchemistries.dft.doublehybriddft.rangeseparateddoublehybrids](#tab:modelchemistries.dft.doublehybriddft.rangeseparateddoublehybrids).
!!! tip
    For most natively implemented double-hybrids you can simple add the `DLPNO-` prefix to the respective functional simple input keyword, e.g. `DLPNO-WPR2SCAN50`.
    For all others, the DLPNO treatment can be activated via the `%mp2` block using the `DLPNO true` keyword.
<a id="tab:modelchemistries.dft.doublehybriddft.rangeseparateddoublehybrids"></a>
!!! note "List of available range-separated double-hybrid functionals. `PS` is the opposite-spin, `PT` the same-spin scaling parameter. $\mu$ is the range-separation parameter. Excited-states optimized (ES-Opt.) functionals only employ spin-component-scaling for the [CIS(D) doubles correction](../spectroscopyproperties/tddft.md#sec:spectroscopyproperties.tddft.doubles) within the the TD-DFT framework. Same-spin indirect term (CTss), opposite-spin indirect term (CTos), same-spin direct term (CUss), and opposite-spin direct term (CUos) parameters are given in the footnotes."

| | **Keywords** | `%HFX` | $\mu$ / $\text{bohr}^{-1}$ | `%GGAC` | `%MP2C` | `PS` | `PT` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Functional** | Keywords | `%HFX` | $\mu$ / $\text{bohr}^{-1}$ | `%GGAC` | `%MP2C` | `PS` | `PT` |
| **$\omega$B97M(2)[^f] [Mardirossian2018](../../bibliography.md)** | `WB97M(2)` | 62.194 `-` 100 | 0.30 | 100 | 34.096 | `-` | `-` |
| **$\omega$B97X-2(TQZ) [Chai2009](../../bibliography.md)** | `WB97X-2` | 63.6158 `-` 95.1661 | 0.30 | 100 | 100 | 0.447105 | 0.529319 |
| **$\omega$Pr2SCAN50 [Wittmann2023](../../bibliography.md)** | `WPR2SCAN50` | 50 `-` 100 | 0.214013 | 65 | 35 | 1.333 | 0.000 |
| **RSX-QIDH [RSXQIDH](../../bibliography.md)** | `RSX-QIDH` | 69 `-` 100 | 0.27 | 67 | 33 | `-` | `-` |
| **RSX-0DH [RSX0DH](../../bibliography.md)** | `RSX-0DH` | 50 `-` 100 | 0.33 | 87.5 | 12.5 | `-` | `-` |
| **$\omega$B2PLYP [goerigk2019RSDHTDDFT](../../bibliography.md)** | `WB2PLYP` | 53 `-` 100 | 0.30 | 73 | 27 | `-` | `-` |
| **$\omega$B2GP-PLYP [goerigk2019RSDHTDDFT](../../bibliography.md)** | `WB2GP-PLYP` | 65 `-` 100 | 0.27 | 64 | 36 | `-` | `-` |
| **$\omega$B88PP86 [goerigk2019RSDHTDDFT](../../bibliography.md)** | `WB88PP86` | 65 `-` 100 | 0.20 | 58 | 42 | `-` | `-` |
| **$\omega$PBEPP86 [goerigk2019RSDHTDDFT](../../bibliography.md)** | `WPBEPP86` | 70 `-` 100 | 0.18 | 68 | 48 | `-` | `-` |
| ****excited state opt.**** |  |  |  |  |  |  |  |

| **SCS/SOS-$\omega$B2PLYP [SCSTDDHDFs](../../bibliography.md)** | — |
      - `SCS/SOS-WB2PLYP`
      - 53 `-` 100
      - 0.30
      - 73
      - 27
      - [^g]
      - [^g]

| | **`SCS-WB2GP-PLYP`** | 65 `-` 100 | 0.27 | 64 | 36 | [^h] | [^h] |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **SCS-$\omega$B2GP-PLYP [SCSTDDHDFs](../../bibliography.md)** | `SCS-WB2GP-PLYP` | 65 `-` 100 | 0.27 | 64 | 36 | [^h] | [^h] |
| **SOS-$\omega$B2GP-PLYP [SCSTDDHDFs](../../bibliography.md)** | `SOS-WB2GP-PLYP` | 65 `-` 100 | 0.27 | 64 | 36 | [^i] | [^i] |
| **SCS-RSX-QIDH [SCSTDDHDFs](../../bibliography.md)** | `SCS-RSX-QIDH` | 69 `-` 100 | 0.27 | 67 | 33 | [^j] | [^j] |
| **SOS-RSX-QIDH [SCSTDDHDFs](../../bibliography.md)** | `SOS-RSX-QIDH` | 69 `-` 100 | 0.27 | 67 | 33 | [^k] | [^k] |
| **SCS-$\omega$B88PP86 [SCSTDDHDFs](../../bibliography.md)** | `SCS-WB88PP86` | 65 `-` 100 | 0.20 | 58 | 42 | [^l] | [^l] |
| **SOS-$\omega$B88PP86 [SCSTDDHDFs](../../bibliography.md)** | `SOS-WB88PP86` | 65 `-` 100 | 0.20 | 58 | 42 | [^m] | [^m] |
| **SCS-$\omega$PBEPP86 [SCSTDDHDFs](../../bibliography.md)** | `SCS-WPBEPP86` | 70 `-` 100 | 0.18 | 68 | 48 | [^n] | [^n] |
| **SOS-$\omega$PBEPP86 [SCSTDDHDFs](../../bibliography.md)** | `SOS-WPBEPP86` | 70 `-` 100 | 0.18 | 68 | 48 | [^o] | [^o] |

[^f]: Must be used with ωB97M-V orbitals (cf. [rangeseparateddoublehybrids.wb97m2](#sec:modelchemistries.dft.doublehybriddft.rangeseparateddoublehybrids.wb97m2)).
[^g]: SCS/SOS-$\omega$B2PLYP: CTss: 0.000; CTos: 0.433; CUss: 0.000; CUos: 0.460.
[^h]: SCS-$\omega$B2GP-PLYP: CTss: 0.000; CTos: 0.571; CUss: 0.135; CUos: 0.558.
[^i]: SOS-$\omega$B2GP-PLYP: CTss: 0.000; CTos: 0.570; CUss: 0.000; CUos: 0.610.
[^j]: SCS-RSX-QIDH: CTss: 0.174; CTos: 0.541; CUss: 0.586; CUos: 0.424.
[^k]: SOS-RSX-QIDH: CTss: 0.000; CTos: 0.632; CUss: 0.000; CUos: 0.714.
[^l]: SCS-$\omega$B88PP86: CTss: 0.000; CTos: 0.557; CUss: 0.092; CUos: 0.545.
[^m]: SOS-$\omega$B88PP86: CTss: 0.000; CTos: 0.559; CUss: 0.000; CUos: 0.599.
[^n]: SCS-$\omega$PBEPP86: CTss: 0.000; CTos: 0.610; CUss: 0.297; CUos: 0.540.
[^o]: SOS-$\omega$PBEPP86: CTss: 0.000; CTos: 0.613; CUss: 0.000; CUos: 0.669.
<a id="sec:modelchemistries.dft.doublehybriddft.rangeseparateddoublehybrids.wb97m2"></a>
#### $\omega$B97M(2)
Some double-hybrid functionals, such as $\omega$B97M(2)[Mardirossian2018](../../bibliography.md) must be applied to orbitals converged with a
different functional. This can be accomplished with a two-step
calculation using `MORead` and `MaxIter=1`. Note that because the
orbitals are not obtained self-consistently, only single point energies
can be computed in this way, i.e. no density, gradient, or properties!
The usage of such functionals may be automatized using the [Compound script language](../workflowsautomatization/compound.md).
An exemplary compound script for a $\omega$B97M(2) single-point calculation is given below:
```mol
title: structure 1
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
2
structure (0 1)
H           0.0          0.0          0.0
F           0.0          0.0          0.9
--- input ---
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
<a id="sec:modelchemistries.dft.doublehybrids.customization"></a>
### Customization of Double-Hybrids
As double-hybrid functionals make use of customizable components of [global hybrids](#sec:modelchemistries.dft.rangeseparatedhybrids.customization) or 
[range-separated hybrids](#sec:modelchemistries.dft.rangeseparatedhybrids.customization) they can can be constructed and customized in similar fashion. 
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
<a id="tab:modelchemistries.dft.doublehybriddft.customization.keywords.block.method"></a>
!!! note "Most important `%method` block input keywords to customize double-hybrid functionals."
    | Keyword                         | Options              | Description                                                     |
    |:--------------------------------|:---------------------|:----------------------------------------------------------------|
    | `DoMP2`                         | `true`               | Activates MP2 correlation part                                  |
    | `ScalMP2C`                      | `<real>`             | Controls the fraction of GGA exchange                           |
<a id="tab:modelchemistries.dft.doublehybriddft.customization.keywords.block.mp2"></a>
!!! note "Most important `%mp2` block input keywords to customize double-hybrid functionals. For more details see the [MP2 section](../modelchemistries/MP2.md)."
    | Keyword                         | Options              | Description                                                     |
    |:--------------------------------|:---------------------|:----------------------------------------------------------------|
    | `DoSCS`                         | `true`               | Activates spin-component-scaling of MP2 part                    |
    | `PS`                            | `<real>`             | Controls the opposite-spin-scaling parameter                    |
    | `PT`                            | `<real>`             | Controls the same-spin-scaling parameter                        |
    | `RI`                            | `true`               | Activates RI-MP2                                                |
    | `DLPNO`                         | `true`               | Activates DLPNO-MP2                                             |
<a id="sec:modelchemistries.dft.libxc"></a>
## LibXC Functional Library
It is possible to use the functionals provided by
LibXC within the ORCA framework [^libxc]. The LibXC version used by ORCA is
printed at the beginning of the output. The LibXC reference should be
cited when LibXC is used as part of your calculations. For reference,
see [libxc](../../bibliography.md).
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
(VV10) correlation (see [nl.theory](dispersioncorrections.md#sec:modelchemistries.dispersioncorrections.nl.theory)). The VV10 part is computed
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
<a id="sec:modelchemistries.dft.libxc.screeningthresholds"></a>
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
<a id="sec:modelchemistries.dft.libxc.modifyingparameters"></a>
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
```mol
title: structure 2
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
2
structure (0 1)
H             0            0            0
F             0            0          0.9
--- input ---
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
<a id="sec:modelchemistries.dft.libxc.simpleinput"></a>
### Simple Input of LibXC Functionals
Some LibXC functionals are accessible via the simple input keyword
`!LibXC(Keyword)`, e.g. `!LibXC(TPSS)`. The keywords match those of the natively implemented in ORCA. Using this syntax, parameters for the
[DFT-D dispersion corrections](../modelchemistries/dispersioncorrections.md) are also set automatically (if
implemented). Table [tab:modelchemistries.dft.libxc.simpleinput](#tab:modelchemistries.dft.libxc.simpleinput) lists the available functionals and their
LibXC names.
<a id="tab:modelchemistries.dft.libxc.simpleinput"></a>
!!! note "LibXC functionals available via the simple input `!LibXC(Keyword)`"
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
[^libxc]: https://libxc.gitlab.io
