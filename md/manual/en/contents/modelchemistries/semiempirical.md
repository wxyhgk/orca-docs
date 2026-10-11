```{index} Semiempirical Methods
```

(sec:modelchemistries.semiempirical)=
# Semiempirical Methods

Semi-empirical quantum mechanical methods (SQM) are very useful to deal with many of very large systems. They use tailored approximations to reduce the computational cost drastically while
keeping a reasonable level of accuracy for large parts of the chemical space. They are specifically useful to simulate raction paths with [NEB-TS](sec:structurereactivity.neb.nebts) or to define a SQM region in [multi-scale approaches](sec:modelchemistries.mm.orca) like ONIOM.

```{index} NDO, CNDO, INDO, NDDO, MNDO
```

(sec:modelchemistries.semiempirical.ndo)=
## Neglect of Differential Overlap: CNDO, INDO, NDDO

A number of methods based on the "neglect of differential overlap"
{cite}`pople1970approx,sedlej1985semi` are currently implemented for
energies and analytic gradients inluding AM1{cite}`dewar1985am`, PM3{cite}`stewart1989comp`, MNDO{cite}`dewar1977theor,thiel1992theor,dewar1977am` and other variants of CNDO, INDO, and NDDO.The methods MNDO , AM1, and PM3 are available for main group elements only and arise from the work of the Dewar group.
They have been optimized to reproduce molecular structure and energetics. The older
CNDO/1,2 and INDO/1,2 were developed by the Pople group
{cite}`pople1965chem,pople1966chem,santry1968am,santry1967chem,pople1967chem,clack1972chem,clack1974mol,clack1974theor,boehm1981theor`
and were designed to roughly mimic minimal basis *ab initio*
calculations. The methods of the Zerner group (ZINDO/1,2 and ZINDO/S)
are closely related to the older methods but have been well
parameterized for transition metals too
{cite}`ridley1973theor,bacon1979theor,zerner1980am,anderson1986inorg,anderson1990inorg,anderson1991int,zerner1990reviews,zerner1992metal,zerner1996metal,cory1991chem,kotzian1992theor`.
ZINDO/1 (and less so ZINDO/2) are suitable for geometry optimization.
ZINDO/S gives good results for electronically excited states at moderate
configuration interaction levels and is also successful for the
calculation of electron and spin distributions in large transition metal
complexes
{cite}`anderson1991int,zerner1990reviews,zerner1992metal,zerner1996metal,cory1991chem,kotzian1992theor`.
The ZNDDO/1,2 methods have been implemented into ORCA as straightforward
extensions of the corresponding INDO methods without changing any
parameter. However, the methods benefit from the somewhat more accurate
representation of the Coulomb interaction within the NDDO approximation
{cite}`nieke1984theor,koehler1972zchem`. The preliminary experience with
these methods is that they are better than the corresponding INDO
methods for calculation of transition metal complex structures but on
the whole have also similar deficiencies. The analytic gradients are available 
for all of these methods and can be used to produce reasonable molecular 
structures at low computational cost or to get preliminary insight in the 
behavior of the system under investigation. However, do not try to use 
ZINDO/S (or CNDO/S) for structure optimizations - it does not make sense 
and will lead to disastrous results because there is no accurate 
representation of nuclear repulsion in these methods.

:::{tip}
Even though ORCA has no implementation of newer MNDO methods like PM6 or RM1, 
they can be used via ORCA's [External Optimizer feature](sec:structurereactivity.optimization.externaloptimizer) 
and [MOPAC](https://github.com/openmopac/mopac). This way, [MOPAC](https://github.com/openmopac/mopac) 
can be interfaced to provide ORCA with energies and gradients via the respective wrapper script 
that can be downloaded from the [ORCA external tools GitHub repository](https://github.com/ORCAQuantumChemistry/orca-external-tools).
:::

(sec:modelchemistries.semiempirical.ndo.basicusage)=
### Basic Usage

The NDDO-based MNDO, AM1, and PM3 methods can be invoked via the simple input keywords `!MNDO`, `!AM1` and `!PM3`.

```orca
!MNDO
```
```orca
!AM1
```
```orca
!PM3
```

These and other methods can be further defined via the `%method` block, e.g. INDO with the INDO/1 parameter set as:

```orca
%method
   METHOD   INDO
   VERSION  INDO_1
end
```

Or by directly invoking the respective parameterization as `METHOD`

```orca
%method
   METHOD   INDO_1
end
```

:::{note}
If you want you can also combine semiempirical methods with MP2
(energies only). For example use `Method AM1` and `DoMP2 true`. It is questionable if this makes the results of
semiempirical calculations any better but at least it is possible in ORCA.
:::

(sec:modelchemistries.semiempirical.ndo.customparams)=
### Custom Parameters

You can change the built-in semiempirical parameters in a
straightforward fashion via the `%ndoparas` block. To do so, any element sepcific parameters
can be defined via an array "P":

```orca
%ndoparas  
   P[<atomic number>,<parameter number>] <real>
end
```

For example, we can set the resonance integral parameter 
BS (s shell beta) with the number 25 for Carbon (Z = 6) to 20 eV:

```orca
%ndoparas  
   P[6,25] 20
end
```

A full list of parameters that can be modified can be found below. Most of them will only be interesting for expert users.
The most commonly modified parameters are the Beta's (number 25 through
28). Note that most programs require a negative number here. In ORCA the
resonance integrals are defined in a way that makes the Beta's positive.


:::{raw} latex
\begingroup
\footnotesize
:::

:::{tabularcolumns} \Y{0.3}\Y{0.3}\Y{0.4}
:::
(tab:modelchemistries.semiempirical.ndo.paras)=
:::{flat-table} List of parameters that can be set in the `%ndoparas` block.
:header-rows: 1
:class: longtable
:class: footnotesize

   * - Parameter
     - Number
     - Description
   * - {cspan}`2` *Core Integrals (in eV):*
   * - `US`
     - `0`
     - 
   * - `UP`
     - `1`
     - 
   * - `UD`
     - `2`
     - 
   * - `UF`
     - `3`
     - 
   * - {cspan}`2` *Basis Set Parameters (double-zeta):*
   * - `NSH`
     - `4`
     - Number of shells for the element
   * - `NZS`
     - `5`
     - Number of Slater type orbitals for the s shell
   * - `ZS1`
     - `6`
     - First exponent
   * - `ZS2`
     - `7`
     - Second exponent
   * - `CS1`
     - `8`
     - First contraction coefficient
   * - `CS2`
     - `9`
     - Second contraction coefficient
   * - `NZP`
     - `10`
     - Number of Slater type orbitals for the p shell
   * - `ZP1`
     - `11`
     - 
   * - `ZP2`
     - `12`
     - 
   * - `CP1`
     - `13`
     - 
   * - `CP2`
     - `14`
     - 
   * - `NZD`
     - `15`
     - Number of Slater type orbitals for the d shell
   * - `ZD1`
     - `16`
     - 
   * - `ZD2`
     - `17`
     - 
   * - `CD1`
     - `18`
     - 
   * - `CD2`
     - `19`
     - 
   * - `NZF`
     - `20`
     - Number of Slater type orbitals for the f shell
   * - `ZF1`
     - `21`
     - 
   * - `ZF2`
     - `22`
     - 
   * - `CF1`
     - `23`
     - 
   * - `CF2`
     - `24`
     - 
   * - {cspan}`2` *Resonance integral parameters (in eV):*
   * - `BS`
     - `25`
     - s shell beta
   * - `BP`
     - `26`
     - p shell beta
   * - `BD`
     - `27`
     - d shell beta
   * - `BF`
     - `28`
     - f shell beta
   * - {cspan}`2` *Number of electrons in the ground state:*
   * - `NEL`
     - `29`
     - Total number of electrons (integer)
   * - `NS`
     - `30`
     - Fractional occupation number of the s shell
   * - `NP`
     - `31`
     - Fractional occupation number of the p shell
   * - `ND`
     - `32`
     - Fractional occupation number of the d shell
   * - `NF`
     - `33`
     - Fractional occupation number of the f shell
   * - {cspan}`2` *One center repulsion (gamma) integrals (in eV):*
   * - `GSS`
     - `34`
     - 
   * - `GSP`
     - `35`
     - 
   * - `GSD`
     - `36`
     - 
   * - `GSF`
     - `37`
     - 
   * - `GPP`
     - `38`
     - 
   * - `GPD`
     - `39`
     - 
   * - `GPF`
     - `40`
     - 
   * - `GDD`
     - `41`
     - 
   * - `GDF`
     - `42`
     - 
   * - `GFF`
     - `43`
     - 
   * - {cspan}`2` *Slater Condon parameters (in eV):*
   * - `F2PP`
     - `44`
     - 
   * - `F2PD`
     - `45`
     - 
   * - `F2DD`
     - `46`
     - 
   * - `F4DD`
     - `47`
     - 
   * - `G1SP`
     - `48`
     - 
   * - `G1PD`
     - `49`
     - 
   * - `G2SD`
     - `50`
     - 
   * - `G3PD`
     - `51`
     - 
   * - `R1SPPD`
     - `52`
     - 
   * - `R2SDPP`
     - `53`
     - 
   * - `R2SDDD`
     - `54`
     - 
   * - {cspan}`2` *The nuclear repulsion parameters for Dewar type models:*
   * - `NR1`
     - `55`
     - 
   * - `NR2`
     - `56`
     - 
   * - `NR3`
     - `57`
     - 
   * - `NR4`
     - `58`
     - 
   * - `NR5`
     - `59`
     - 
   * - `NR6`
     - `60`
     - 
   * - `NR7`
     - `61`
     - 
   * - `NR8`
     - `62`
     - 
   * - `NR9`
     - `63`
     - 
   * - `NR10`
     - `64`
     - 
   * - `NR11`
     - `65`
     - 
   * - `NR12`
     - `66`
     - 
   * - `NR13`
     - `67`
     - 
   * - {cspan}`2` *Nuclear attraction/repulsion parameter for MNDO/d:*
   * - `RHO`
     - `68`
     - 
   * - {cspan}`2` *Spin orbit coupling parameters:*
   * - `SOCP`
     - `69`
     - SOC for the p shell
   * - `SOCD`
     - `70`
     - SOC for the d shell
   * - `SOCF`
     - `71`
     - SOC for the f shell
:::
:::{raw} latex
\endgroup
:::


The "molecular" parameters are also set in the `%ndoparas` block using "`INTFA`"
("interaction factors");

```orca
%ndoparas  
   INTFA[PP_PI] 0.585
  # The interaction factors exist for
  #  ss_sigma
  #  sp_sigma
  #  sd_sigma
  #  pp_sigma
  #  pd_sigma
  #  dd_sigma
  #  pp_pi
  #  pd_pi
  #  dd_pi
  #  dd_delta
  # the parameter entering the Coulomb integrals
  # in INDO/S
   FGAMMA 1.2
end
```
(sec:modelchemistries.semiempirical.ndo.keywords)=
### Keywords

:::{raw} latex
\begingroup
\footnotesize
:::

:::{tabularcolumns} \Y{0.3}\Y{0.7}
:::

(tab:modelchemistries.semiempirical.ndo.keywords.simple)=
:::{flat-table} Simple input keywords for the NDO-based methods.
:class: footnotesize
:header-rows: 1
* - Keyword
  - Description
* - `AM1`
  - Activates AM1
* - `PM3`
  - Activates PM3
* - `MNDO`
  - Activates MNDO
* - `ZINDO/1`
  - Activates ZINDO/1
* - `ZINDO/2`
  - Activates ZINDO/2
* - `ZINDO/S`
  - Activates ZINDO/S
* - `ZNDDO/1`
  - Activates ZNDDO/1
* - `ZNDDO/2`
  - Activates ZNDDO/2
:::
:::{raw} latex
\endgroup
:::

:::{raw} latex
\begingroup
\footnotesize
:::

:::{tabularcolumns} \Y{0.2}\Y{0.2}\Y{0.6}
:::

(tab:modelchemistries.semiempirical.ndo.keywords.block)=
:::{flat-table} `%method` block input keywords for the NDO-based methods.
:class: footnotesize
:header-rows: 1
* - Keyword
  - Options
  - Description
* - `METHOD`
  - `AM1`
  - Activates AM1
* -
  - `PM3`
  - Activates PM3
* -
  - `MNDO`
  - Activates MNDO
* -
  - `CNDO_1`
  - Activates CNDO/1
* -
  - `CNDO_2`
  - Activates CNDO/2
* -
  - `CNDO_S`
  - Activates CNDO/S
* -
  - `INDO_1`
  - Activates INDO/1
* -
  - `INDO_2`
  - Activates INDO/2
* -
  - `INDO_S`
  - Activates INDO/S
* -
  - `ZINDO_1`
  - Activates ZINDO/1
* -
  - `ZINDO_2`
  - Activates ZINDO/2
* -
  - `ZINDO_S`
  - Activates ZINDO/S
* -
  - `ZNDDO_1`
  - Activates ZNDDO/1
* -
  - `ZNDDO_2`
  - Activates ZNDDO/2
* -
  - `CNDO`
  - Activates CNDO, requires a `VERSION` to be set
* -
  - `INDO`
  - Activates INDO, requires a `VERSION` to be set
* -
  - `NDDO`
  - Activates NDDO, requires a `VERSION` to be set
* - `VERSION`
  - `CNDO_1`
  - Sets the parameter set for CNDO to `CNDO_1`
* -
  - `CNDO_2`
  - Sets the parameter set for CNDO to `CNDO_2`
* -
  - `CNDO_S`
  - Sets the parameter set for CNDO to `CNDO_S`
* -
  - `INDO_1`
  - Sets the parameter set for INDO to `INDO_1`
* -
  - `INDO_2`
  - Sets the parameter set for INDO to `INDO_2`
* -
  - `INDO_S`
  - Sets the parameter set for INDO to `INDO_S`
* -
  - `ZINDO_1`
  - Sets the parameter set for INDO to `ZINDO_1`
* -
  - `ZINDO_2`
  - Sets the parameter set for INDO to `ZINDO_2`
* -
  - `ZINDO_S`
  - Sets the parameter set for INDO to `ZINDO_S`
* -
  - `ZNDDO_1`
  - Sets the parameter set for NDDO to `ZNDDO_1`
* -
  - `ZNDDO_2`
  - Sets the parameter set for NDDO to `ZNDDO_2`
* -
  - `MNDO`
  - Sets the parameter set for NDDO to `MNDO`
* -
  - `AM1`
  - Sets the parameter set for NDDO to `AM1`
* -
  - `PM3`
  - Sets the parameter set for NDDO to `PM3`
:::
:::{raw} latex
\endgroup
:::

```{index} GFN-xTB (interfaced)
```

(sec:modelchemistries.semiempirical.xtb)=
## Extended Tight-Binding: GFN0-xTB, GFN-xTB, GFN2-xTB

ORCA is interfaced to the xtb program by Grimme and coworkers, allowing the
user to request all kinds of calculations using the popular GFN0-xTB, GFN-xTB and
GFN2-xTB Hamiltonians.{cite}`grimme2017xtb,grimme2019xtb,pracht2019xtb` From the technical
side, the user has to provide the executable provided by the Grimme
group. The xtb program package can be obtained free of charge from
<https://github.com/grimme-lab/xtb/releases> and detailed information on
the usage of the `xtb` standalone program and its utilities can be found
at <https://xtb-docs.readthedocs.io/en/latest/contents.html>. Only the
file `bin/xtb` is used by ORCA . The user should copy this file into the
directory where the other ORCA executables are located, and rename it as
`otool_xtb`.

:::{warning}
- Please use the 6.7.1 version (or any later version) of `xtb`; 
  older versions are not fully compatible with ORCA anymore or are missing features, 
  for example it may not be possible to invoke the solvation model! 
  Additionally, Windows users should copy `libiomp5md.dll` from the XTB directory to the ORCA directory.
- On Linux, the `xtb` interface only works if the default shell, i.e. `/bin/sh`, is POSIX-compliant,
  for example `bash` or `dash` but not `csh` or `tcsh`.
:::

The xTB method can be invoked via the `GFN0-xTB`, `GFN-xTB`, and `GFN2-xTB` keywords. The GFN-FF generic force-field can be invoked via `GFN-FF`:

```orca
! GFN0-xTB  # Synonym: XTB0
```
```orca
! GFN-xTB  # Synonym: XTB1
```
```orca
! GFN2-xTB  # Synonym: XTB2
```
```orca
! GFN-FF # Synonym: XTBFF
```

The following methods can be used in conjunction with XTB:

-   Single Point Energy

-   Energy and Gradient

-   Optimization, using all kinds of constraints, relaxed surface scans,
    etc.

-   Nudged-Elastic Band calculations

-   Numerical Frequency Calculations

-   Intrinsic Reaction Coordinate

-   Molecular Dynamics Calculations

-   QM/MM calculations

:::{Note}

-   XTB0 is a non-self-consistent tight-binding method, and as such, its accuracy
    is generally inferior to XTB1 and XTB2 (and sometimes even XTBFF), despite that
    it is a few times faster than XTB1 and XTB2. From our experience, we only
    recommend XTB0 when both XTB1 and XTB2 exhibit qualitative failures for the
    system of interest.

-   Please note that XTB0, XTB1 and XTB2 can also be used for the initial path
    generation or for the calculation of an initial TS structure on XTB
    level, both as input for the subsequent NEB calculation on a higher
    level of theory. For more details, please consult
    section {ref}`sec:structurereactivity.neb`.
:::

(sec:modelchemistries.semiempirical.xtb.solvation)=
### Solvation in xTB

Three implicit solvation models can be requested in xTB calculations: 
1. the analytical linearized Poisson-Boltzmann (ALPB){cite}`grimme2021alpb` solvation model
2. the domain decomposition COSMO (ddCOSMO){cite}`ddcosmo2013`
3. the extended conductor-like polarizable continuum model (CPCM-X).{cite}`cpcmx2023` 

These models can be requested via the simple keyword input:

```orca
! ALPB(solvent) # use ALPB
```
```orca
! DDCOSMO(solvent) # use ddCOSMO
```
```orca
! CPCMX(solvent) # use CPCMX
```

where `solvent` is any of the solvents in {numref}`tab:modelchemistries.semiempirical.xtb.solvation.solvents`.

They can further be envoked via the `%xtb` block, here exemplarily shown for ALPB:

```orca
%xtb
  DOALPB true
  ALPBSOLVENT "water"
end
```
:::{raw} latex
\begingroup
\footnotesize
:::

(tab:modelchemistries.semiempirical.xtb.solvation.solvents)=
:::{table} List of available solvents for the different implicit solvation methods that can be used with `xtb`.
:class: footnotesize
|  Solvent             |  ALPB     |   ddCOSMO  |   CPCM-X  |
|:---------------------|:---------:|:----------:|:---------:|
|	1,2,4-trimethylbenzene	|		|		|	X	|
|	1,2-dichloroethane	|		|		|	X	|
|	1,4-dioxane / dioxane	|	X	|	X	|		|
|	1-butanol / butanol	|		|		|	X	|
|	1-chlorohexane / chlorohexane	|		|		|	X	|
|	1-decanol / decanol	|		|		|	X	|
|	1-fluorooctane	|		|		|	X	|
|	1-heptanol / heptanol	|		|		|	X	|
|	1-hexanol / hexanol	|		|		|	X	|
|	1-iodohexadecane / hexadecyliodide	|		|		|	X	|
|	1-nonanol / nonanol	|		|		|	X	|
|	1-octanol / octanol	|	X	|	X	|	X	|
|	1-pentanol / pentanol	|		|		|	X	|
|	1-propanol / propanol	|		|		|	X	|
|	2,2,4-trimethylpentane / isooctane	|		|		|	X	|
|	2,6-dimethylpyridine	|		|		|	X	|
|	2-butanol / secbutanol	|		|		|	X	|
|	2-methoxyethanol / methoxyethanol	|		|		|	X	|
|	2-methyl-1-propanol / isobutanol	|		|		|	X	|
|	2-methylpyridine / 2methylpyridine	|		|		|	X	|
|	2-propanol / isopropanol	|		|		|	X	|
|	4-methyl-2-pentanone / 4methyl2pentanone	|		|		|	X	|
|	acetic acid / aceticacid	|		|		|	X	|
|	acetone	|	X	|	X	|		|
|	acetonitrile / mecn / ch3cn	|	X	|	X	|	X	|
|	acetophenone	|		|		|	X	|
|	aniline	|	X	|	X	|	X	|
|	anisole	|		|		|	X	|
|	benzaldehyde	|	X	|	X	|		|
|	benzene	|	X	|	X	|	X	|
|	benzonitrile	|		|		|	X	|
|	benzyl alcohol / benzylalcohol	|		|		|	X	|
|	bromobenzene	|		|		|	X	|
|	bromoethane	|		|		|	X	|
|	bromoform	|		|		|	X	|
|	butanone	|		|		|	X	|
|	butyl ethanoate / butyl acetate / butylacetate	|		|		|	X	|
|	n-butylbenzene / butylbenzene	|		|		|	X	|
|	sec-butylbenzene / secbutylbenzene	|		|		|	X	|
|	tert-butylbenzene / tbutylbenzene	|		|		|	X	|
|	carbon disulfide / carbondisulfide / cs2	|	X	|	X	|	X	|
|	carbon tetrachloride / ccl4	|		|		|	X	|
|	chlorobenzene	|		|		|	X	|
|	chloroform / chcl3	|	X	|	X	|	X	|
|	conductor	|		|	X	|		|
|	m-cresol / mcresol	|		|		|	X	|
|	cyclohexane	|		|		|	X	|
|	cyclohexanone	|		|		|	X	|
|	decalin	|		|		|	X	|
|	n-decane / decane	|		|		|	X	|
|	dibromomethane	|		|		|	X	|
|	dibutylether	|		|		|	X	|
|	o-dichlorobenzene / odichlorobenzene	|		|		|	X	|
|	dichloromethane / ch2cl2 / dcm	|	X	|	X	|	X	|
|	diethyl ether / diethylether	|	X	|	X	|	X	|
|	diisopropyl ether / diisopropylether	|		|		|	X	|
|	n,n-dimethylacetamide / dimethylacetamide	|		|		|	X	|
|	n,n-dimethylformamide / dimethylformamide / dmf	|	X	|	X	|	X	|
|	dimethylsulfoxide / dmso	|	X	|	X	|	X	|
|	diphenylether	|		|		|	X	|
|	n-dodecane / dodecane	|		|		|	X	|
|	ethanol	|	X	|	X	|	X	|
|	ethyl acetate / ethylacetate / ethanoate	|	X	|	X	|	X	|
|	ethyl phenyl ether / ethoxybenzene	|		|		|	X	|
|	ethylbenzene	|		|		|	X	|
|	fluorobenzene	|		|		|	X	|
|	furan / furane	|	X	|	X	|		|
|	n-heptane / heptane	|		|		|	X	|
|	n-hexadecane / hexadecane	|	X	|	X	|	X	|
|	n-hexane / hexane	|	X	|	X	|	X	|
|	iodobenzene	|		|		|	X	|
|	isopropylbenzene	|		|		|	X	|
|	p-isopropyltoluene / isopropyltoluene	|		|		|	X	|
|	mesitylene	|		|		|	X	|
|	methanol	|	X	|	X	|	X	|
|	n-methylformamide / methylformamide	|		|		|	X	|
|	nitrobenzene / phno2	|		|		|	X	|
|	nitroethane	|		|		|	X	|
|	nitromethane / meno2	|	X	|	X	|	X	|
|	o-nitrotoluene / onitrotoluene	|		|		|	X	|
|	n-nonane / nonane	|		|		|	X	|
|	n-octane / octane	|		|		|	X	|
|	n-pentadecane / pentadecane	|		|		|	X	|
|	octanol(wet) / wetoctanol / woctanol	|	X	|	X	|		|
|	n-pentane / pentane	|		|		|	X	|
|	perfluorobenzene / hexafluorobenzene	|		|		|	X	|
|	phenol	|	X	|	X	|		|
|	pyridine	|		|		|	X	|
|	tetrachloroethene / c2cl4	|		|		|	X	|
|	tetrahydrofuran / thf	|	X	|	X	|	X	|
|	tetrahydrothiophene-s,s-dioxide / tetrahydrothiophenedioxide / sulfolane	|		|		|	X	|
|	tetralin	|		|		|	X	|
|	toluene	|	X	|	X	|	X	|
|	tributylphosphate	|		|		|	X	|
|	triethylamine	|		|		|	X	|
|	n-undecane / undecane	|		|		|	X	|
|	water / h2o	|	X	|	X	|	X	|
|	xylene	|		|		|	X	|
:::

:::{raw} latex
\endgroup
:::

:::{Note}
-   If jobs are run over several nodes, the number of cores used by the
    XTB tool might be lower than requested via the pal keyword.
:::


### Keywords


:::{raw} latex
\begingroup
\footnotesize
:::

:::{tabularcolumns} \Y{0.3}\Y{0.7}
:::

(tab:modelchemistries.semiempirical.xtb.keywords.simple)=
:::{flat-table} Simple input keywords for the extended tight-binding methods.
:class: footnotesize
:header-rows: 1
* - Keyword
  - Description
* - `XTB`
  - Activates GFN2-xTB
* - `XTB0`
  - Activates GFN0-xTB
* - `GFN0-XTB`
  - Activates GFN0-xTB
* - `XTB1`
  - Activates GFN1-xTB
* - `GFN1-XTB`
  - Activates GFN1-xTB
* - `XTB2`
  - Activates GFN2-xTB
* - `GFN2-XTB`
  - Activates GFN2-xTB
* - `XTBFF`
  - Activates GFN-FF
* - `GFN-FF`
  - Activates GFN-FF
* - `ALPB(<solvent>)`
  - Activates ALPB solvation for a `<solvent>`, e.g. ALPB(Water)
* - `DDCOSMO(<solvent>)`
  - Activates DDCOSMO solvation for a `<solvent>`, e.g. DDCOSMO(Water)
* - `CPCMX(<solvent>)`
  - Activates CPCMX solvation for a `<solvent>`, e.g. CPCMX(Water)
:::
:::{raw} latex
\endgroup
:::

:::{raw} latex
\begingroup
\footnotesize
:::

:::{tabularcolumns} \Y{0.2}\Y{0.2}\Y{0.6}
:::

(tab:modelchemistries.semiempirical.xtb.keywords.block)=
:::{flat-table} `%xtb` block input keywords for the extended tight-binding methods.
:class: footnotesize
:header-rows: 1
* - Keyword
  - Options
  - Description
* - `XTBINPUTSTRING`
  - `"<string>"`
  - Parses string to the `otool_xtb` call
* - `XTBINPUTSTRING2`
  - `"<string>"`
  - Parses string to the `otool_xtb` call
* - `NPROCS`
  - `<integer>`
  - Controls number of processors for the `otool_xtb` run, default is ORCA's `PAL` setting
* - `MAXCORE`
  - `<integer>`
  - Memory in MB reserved for the `xtb` run, default is ORCA's `maxcore` setting
* - `ACCURACY`
  - `<real>`
  - Accuracy setting for `--acc` in `otool_xtb`, default is ORCA's accuracy x 1.e6
* - `DOALPB`
  - `true`/`false`
  - Activates ALPB solvation in `xtb` run
* - `ALPBSOLVENT`
  - `"<solvent>"`
  - Controls the `<solvent>` used for ALPB
* - `DODDCOSMO`
  - `true`/`false`
  - Activates DDCOSMO solvation in `xtb` run
* - `DDCOSMOSOLVENT`
  - `"<solvent>"`
  - Controls the `<solvent>` used for DDCOSMO
* - `EPSILON`
  - `<real>`
  - Controls the dielectric constant, only for ddCOSMO
* - `DOCPCMX`
  - `true`/`false`
  - Activates CPCMX solvation in `xtb` run
* - `CPCMXSOLVENT`
  - `"<solvent>"`
  - Controls the `<solvent>` used in CPCMX
* - `ETEMP`
  - `<real>`
  - Controls electronic temperature `--etemp` in `otool_xtb`
:::
:::{raw} latex
\endgroup
:::

```{index} GFN-xTB (native)
```

(sec:modelchemistries.semiempirical.nativextb)=
## Native GFN-xTB and GFN2-xTB
:::{versionadded} 6.1.0
Native implementation of GFN1-xTB and GFN2-xTB
:::

ORCA features its own native implementation of GFN-xTB and GFN2-xTB. Unlike the interface to the `xtb` program, the native xTB implementation can use the {ref}`SCF <sec:essentialelements.scfconvergence>` and {ref}`plotting <sec:utilities.plots>` infrastructure. 

The native xTB methods can be invoked via the `!Native-GFN-xTB`, `!Native-GFN2-xTB` simple keywords:

```orca
! Native-GFN-xTB  # Synonym: Native-GFN1-xTB, Native-XTB1
```
```orca
! Native-GFN2-xTB # Synonym: Native-XTB2
```

:::{warning}
For a faster SCF restart based on atomic charges and multipole moments, the native xTB methods write a `basename.xtbw` file. If such an `.xtbw` file is present, it will be used for the restart instead of the `.gbw` file.
:::

(sec:modelchemistries.semiempirical.nativecustomparam)=
### Custom parameterization

The native implementations feature the use of custom semi-empirical parameters by reading a JSON parameter file with the name `basename.xtb.json`. This file has the same format as the JSON file in the dxtb program ([dxtb documentation](https://dxtb.readthedocs.io/en/latest/)), and can be generated by writing the internal parameters. Reading and writing of semi-empirical parameters can be turned on and off via the `%method` block:

```orca
%method
  XTBParamFile "orca.xtb.json" # set parameter filename to orca.xtb.json
  WriteXTBParam true      # if true: write parameters to orca.xtb.json file
  WriteXTBParamDry false  # if true: write parameters to orca.xtb.json file
                          # and exit
  ReadXTBParam false      # if true: read parameters from orca.xtb.json file
end
```

By default the parameter file will be named according to the basename of your calculation (`basename.xtb.json`), but other names can be chosen ẁith the `XTBParamFile` option in the method block. For a dry run that just generates the parameter file from default parameters set `WriteXTBParamDry true`. 

:::{warning}
Please note that the native xTB implementation does not allow changes in the basis. 
:::

(sec:modelchemistries.semiempirical.nativextb.spinpol)=
### Spin-polarized native xTB
The energy expressions of the original GFNn-xTB methods are spin-independent. Therefore, calculations are typically performed using RHF/RKS-type wavefunctions, even for open-shell systems. Since spin does not enter the energy expression, electronic states with higher spin multiplicity will always be higher in energy compared to the respective low-spin states.
This shortcoming is addressed by the spin-polarized xTB methods. The spin-polarized variants {cite}`grimme2023spxtb`, termed spGFN1-xTB and spGFN2-xTB, employ a simple on-site spin-dependent term, which can stabilize high-spin states and allows for screening of potential high-spin configurations using xTB methods.

The native spin-polarized xTB methods can be invoked via the `!Native-spGFN1-xTB`, `!Native-spGFN2-xTB` simple keywords:

```orca
! Native-spGFN1-xTB  # Synonym: Native-spGFN-xTB, Native-spXTB1
```
```orca
! Native-spGFN2-xTB # Synonym: Native-spXTB2
```

Note that the spin-polarization term will only affect high-spin states. The computational cost increases compared to RHF/RKS-type calculations, as the underlying UHF/UKS-type wavefunctions require two Fock matrix diagonalizations instead of one—approximately doubling the cost.

(sec:modelchemistries.semiempirical.nativextb.scf)=
### SCF with native xTB
The native xTB methods, by default, employ special SCF settings that mimic the SCF procedure of the `xtb` program and override all other ORCA SCF settings. These special settings take advantage of xTB-specific features, most notably, that the Fock matrix can be constructed from atomic charges and multipole moments alone.
Due to these shortcuts, the special SCF settings are typically faster for xTB methods than the default ORCA SCF. However, the default SCF is more robust and may succeed in converging problematic cases where the `xtb` SCF fails.

To use the standard ORCA SCF infrastructure instead, set `UseXTBMixer` to false in the `%scf` block:

```orca
%scf
  UseXTBMixer false    # if true (default): special xTB SCF is used
end
```

With the ORCA default SCF infrastructure, challenging electronic structures can often be converged, but the results should be used with caution. In cases where SCF convergence has to be forced, the GFNn-xTB Hamiltonians are often not adequate to describe the system at hand. In such cases, Mulliken charges should be checked for sanity, and it might be helpful to slightly adjust the element-wise pair parameters via the parameter file described above.

:::{warning}
Note that all SCF iterations are direct with xTB methods. 
:::

(sec:modelchemistries.semiempirical.nativextb.fod)=
### FOD with native xTB
To better account for static correlation, the xTB methods use [finite temperature SCF](sec:essentialelements.scf.finitetemp) by default, with an electronic temperature of 300 K. The corresponding [fractional occupation number weighted density (FOD)](sec:spectroscopyproperties.fod) is not printed by default, since 300 K is a too low temperature to use it as a diagnostic tool. The FOD printout can be enabled by setting `XTBFOD` to true in the `%scf` input block. The electronic temperature can be controlled--just as for other methods--via the `SmearTemp` keyword:

```orca
%scf
  XTBFOD true    # if true: Enable FOD printout and add FOD to density container
  SmearTemp 5000 # 5000 K is typically used for FOD plots with xTB methods
end
```

(sec:modelchemistries.semiempirical.nativextb.solvation)=
### Solvation in native xTB
The native implementation of xTB includes the ALPB solvation model with the same solvents available as in the `xtb` program ({ref}`see above <tab:modelchemistries.semiempirical.xtb.solvation.solvents>`). It is controlled with the same keywords as the external ALPB via the simple keyword input:

```orca
! ALPB(solvent) # use ALPB
```

 In addition, the native implementations can be used with other {ref}`solvation models <sec:essentialelements.solvationmodels>` available in ORCA, but one should consider that the CPCM and SMD models are quite expensive compared to an xTB calculation, and therefore the faster ALPB solvation model is recommended. 

(sec:modelchemistries.semiempirical.nativextb.keywords)=
### Keywords

:::{raw} latex
\begingroup
\footnotesize
:::

:::{tabularcolumns} \Y{0.3}\Y{0.7}
:::

(tab:modelchemistries.semiempirical.nativextb.keywords.simple)=
:::{flat-table} Simple input keywords for the native extended tight-binding methods.
:class: footnotesize
:header-rows: 1
* - Keyword
  - Description
* - `NATIVE-XTB`
  - Activates native GFN2-xTB
* - `NATIVE-spXTB`
  - Activates native spGFN2-xTB
* - `NATIVE-XTB1`
  - Activates native GFN1-xTB
* - `NATIVE-spXTB1`
  - Activates native spGFN1-xTB
* - `NATIVE-GFN-XTB`
  - Activates native GFN1-xTB
* - `NATIVE-spGFN-XTB`
  - Activates native spGFN1-xTB
* - `NATIVE-GFN1-XTB`
  - Activates native GFN1-xTB
* - `NATIVE-spGFN1-XTB`
  - Activates native spGFN1-xTB
* - `NATIVE-XTB2`
  - Activates native GFN2-xTB
* - `NATIVE-spXTB2`
  - Activates native spGFN2-xTB
* - `NATIVE-GFN2-XTB`
  - Activates native GFN2-xTB
* - `NATIVE-spGFN2-XTB`
  - Activates native spGFN2-xTB
* - `ALPB(<solvent>)`
  - Activates ALPB solvation for a `<solvent>`, e.g. ALPB(Water)
:::
:::{raw} latex
\endgroup
:::

:::{raw} latex
\begingroup
\footnotesize
:::

:::{tabularcolumns} \Y{0.2}\Y{0.3}\Y{0.5}
:::

(tab:modelchemistries.semiempirical.nativextb.keywords.methodblock)=
:::{flat-table} `%method` block input keywords for the native extended tight-binding methods.
:class: footnotesize
:header-rows: 1
* - Keyword
  - Options
  - Description
* - `WRITEXTBPARAM`
  - `true/false`
  - Write semi-empirical parameters to xtb.json file
* - `WRITEXTBPARAMDRY`
  - `true/false`
  - Write semi-empirical parameters to xtb.json file and abort
* - `READXTBPARAM`
  - `true/false`
  - Read semi-empirical parameters from xtb.json file
* - `XTBPARAMFILE`
  - `"filename.xtb.json"`
  - Specifies xtb.json filename to "filename.xtb.json"
:::
:::{raw} latex
\endgroup
:::

:::{raw} latex
\begingroup
\footnotesize
:::

:::{tabularcolumns} \Y{0.2}\Y{0.2}\Y{0.6}
:::

(tab:modelchemistries.semiempirical.nativextb.keywords.scfblock)=
:::{flat-table} `%scf` block input keywords for the native extended tight-binding methods.
:class: footnotesize
:header-rows: 1
* - Keyword
  - Options
  - Description
* - `XTBFOD`
  - `true/false`
  - Enable FOD printout
* - `UseXTBMixer`
  - `true/false`
  - Use special SCF settings similar to the ones in `xtb`
:::
:::{raw} latex
\endgroup
:::


