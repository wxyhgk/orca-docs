```{index} Dispersion Corrections
```

(sec:modelchemistries.dispersioncorrections)=
# Dispersion Corrections

A major weakness of conventional density functional theory (and Hartee-Fock) is the lacking description of long-range correlation effects including London dispersion. London dispersion represents the attractive component of the van-der-Waals interaction and even though it is a rather weak interaction, its correct description can be crucial for many cases. This is specifically the case for non-covalent interactions and extended molecules. However, there are several well-established dispersion-corrections available to largely correct for this shortcoming. Within ORCA various options are available that include Grimme's D3 {cite}`grimme2010chem, grimme2011comp` and D4 {cite}`caldeweyher2017, caldeweyher2019` corrections as well as the non-local variant of VV10 (NL, {cite}`vydrov2010chem, hujo2011chem` ) are available.

:::{admonition} Some notes on dispersion corrections
:class: note

-   Dispersion corrections do not only affect non-covalent complexes,
    but also conformational energies and structures which are heavily influenced by intramolecular dispersion. Therefore, 
    including the dispersion correction is almost always recommended or 
    even required (except for a handful of cases where it cannot, should not or need not be used, see below).

-   DFT calculations with small basis sets (such as double-$\zeta$ basis
    sets) often yield attractive potential energy surfaces even without the
    dispersion correction. However, this is due to basis set superposition
    error (BSSE), and the interaction energy brought about by the BSSE
    frequently does not match the true interaction energy due to dispersion
    (because they have completely different origins). Therefore, although
    a DFT double zeta calculation without the dispersion correction may
    appear to give qualitatively correct results, or occasionally even better results than
    a double zeta calculation with dispersion corrections (because in the latter case
    one typically overestimates the total attraction), it is still highly
    recommended to "get the right answer for the right reason" by reducing
    the BSSE and turning on the dispersion correction. The BSSE can be
    corrected by a variety of means, for example (1) by using a larger
    basis set; (2) by using the counterpoise correction
    ({ref}`sec:essentialelements.counterpoise`); or (3) by using the
    geometrical counterpoise correction (section {ref}`sec:essentialelements.counterpoise.gcp`).
    Of these, (3) is available at almost no cost (including analytic gradient
    contributions), and is especially suitable for geometry optimization of
    large molecules. Otherwise (1) (or its combination with (2)) may be
    more appropriate due to its higher accuracy.

-   Functionals that contain VV10-type non-local dispersion (in general,
    these are the functionals whose names end with "-V") do not need
    (and cannot be used together with) dispersion corrections. The same
    holds for post-HF and multireference methods, like MP2, CCSD(T), CASSCF
    and NEVPT2. However, one can add a dispersion correction on top of HF.

-   Certain functionals, especially the Minnesota family of functionals
    (e.g. M06-2X), describe medium-range dispersion but miss long-range dispersion.
    They give reasonable dispersion energies for small to medium systems but
    may slightly underestimate the dispersion energies for large systems.
    As the uncorrected functional already accounts for the bulk of
    the dispersion in this case, the dispersion correction is much less
    important than e.g. the case of B3LYP, and should in general be considered
    as beneficial but not mandatory.
:::

```{index} DFT-D3, DFT-D4
```

(sec:modelchemistries.dispersioncorrections.dftd.theory)=
## Grimme's DFT-D3 and DFT-D4

DFT-D3 and DFT-D4 are atom-pairwise (atom-triplewise) dispersion corrections which
can be added to the KS-DFT energies and gradient {cite}`grimme2010chem`. In ORCA, D3 is available for all elements
up to Pu (Z = 94) and D4 up to Lr (Z = 103).

$$E_{\text{DFT-D}} = E_{\text{KS-DFT}} + E_{\text{disp}}
$$ (eqn:modelchemistries.dispersioncorrections.dftd.theory.edftd)

$E_{\text{disp}}$ is then the sum of the two- and three-body
contributions to the dispersion energy,
$E_{\text{disp} } =E^{(2) }+E^{(3) }$. Most important is the
two-body term, which is given at long range by:

$$E_{\text{disp} } = - \sum_{A < B} \sum_{n=6,8} s_{n} \frac{C_{n}^{AB} }{r_{AB}^{n} }
$$ (eqn:modelchemistries.dispersioncorrections.dftd.theory.twobody)

where $C_{n}^{AB}$ denotes the averaged (isotropic) $n^{\text{th}}$-order dispersion
coefficient for atom pair *AB* and $r_{AB}$ is their internuclear
distance. $s_{n}$ is a functional-dependent scaling factor (see below).
In the general case, an adequate damping function must be employed. The more recent D4 model basically 
uses a similar theory but further introduces an atomic partial charge
dependence of the atomic reference polarizabilities.

(sec:modelchemistries.dispersioncorrections.dftd.theory.damping)=
### Damping Functions

In order to avoid near-singularities for small $r_{AB}$, the dispersion
contribution needs to be damped at short distances. One possible way is
to use rational damping as proposed by Becke and Johnson
{cite}`becke2005chem,johnson2005chem,johnson2006chem`:

$$E^{(2) }= - \sum_{A < B} \sum_{n=6,8} s_{n} \frac{C_{n}^{AB} }{r_{AB}^{n} +f(R_{0}^{AB} )^{n} }
$$ (eqn:modelchemistries.dispersioncorrections.dftd.theory.bj)

with {cite}`johnson2006chem`

$$R_{0}^{AB} =\sqrt{ \frac{C_{8}^{AB} }{C_{6}^{AB} } }
$$ (eqn:modelchemistries.dispersioncorrections.dftd.theory.r0ab)

and

$$f(R_{0}^{AB} )=a_{1} R_{0}^{AB} +a_{2} .
$$ (eqn:modelchemistries.dispersioncorrections.dftd.theory.fbj)

Damping the dispersion contribution to zero for short ranges (as in Ref.
{cite}`grimme2010chem`) is also possible:

$$E^{(2) }= - \sum_{A < B}  \sum_{n=6,8} s_{n} \frac{C_{n}^{AB} }{r_{AB}^{n} }f_{d,n} (r_{AB} )
$$ (eqn:modelchemistries.dispersioncorrections.dftd.theory.zero)

with

$$f_{d,n} =\frac{1}{1+6(\frac{r_{AB} }{s_{r,n} R_{0}^{AB} })^{-\alpha_{n} } }
$$ (eqn:modelchemistries.dispersioncorrections.dftd.theory.fzero)

Note that the $R_{0}^{AB}$ used with this damping are from Ref.
{cite}`grimme2010chem`. For more information on the supported damping
functions, see Ref {cite}`grimme2011comp`. 

(sec:modelchemistries.dispersioncorrections.dftd.theory.atm)=
### Three-body term

It is possible to calculate the three-body dispersion contributions according to

$$E^{(3) }= - \sum_{A < B < C} \frac{C_{9}^{ABC} (3\cos{\theta_{a} } \cos{\theta_{b} } \cos{\theta_{c} } +1) }{(r_{AB} r_{BC} r_{CA} )^{3} } f_{d,(3) }(\overline{r}_{ABC})
$$ (eqn:modelchemistries.dispersioncorrections.dftd.theory.abc)

where $\theta_{a}$, $\theta_{b}$ and $\theta_{c}$ are the internal
angles of the triangle formed by $r_{AB}$, $r_{BC}$ and $r_{CA}$. The
$C_{9}$ coefficient is approximated by

$$C_{9}^{ABC} \approx -\sqrt{ C_{6}^{AB} C_{6}^{AC} C_{6}^{BC} }
$$ (eqn:modelchemistries.dispersioncorrections.dftd.theory.c9abc)

The three-body contribution has a small effect on medium-sized molecules
and is damped according to equation {eq}`eqn:modelchemistries.dispersioncorrections.dftd.theory.abc`. The
damping function $f_{d,(3) }(\overline{r}_{ABC})$ is similar to the one
shown in equation {eq}`eqn:modelchemistries.dispersioncorrections.dftd.theory.fzero` with $\overline{r}_{ABC}$ being the geometric mean
of $r_{AB}$, $r_{BC}$ and $r_{CA}$. It can be used with both variants of
the $E^{(2) }$ term, although the three-body term itself will always be
calculated using the zero damping scheme. Adding the three-body
correction has proven to give quite accurate results for the
thermochemistry of supramolecular systems{cite}`grimme2012chemeurj`. Note that the three-body term
is included in D4 by default.

(sec:modelchemistries.dispersioncorrections.dftd.basicusage)=
### Basic Usage

The D3 correction can be invoked by the `!D3` keyword that will automatically make
use of the default Becke-Johnson damping and is thus equivalent to `!D3BJ`. The zero
damping scheme can be used with `!D3ZERO`. Note that the Becke-Johnson scheme is generally
recommended.

```orca
!PBE D3
```

The three-body term can be invoked via the keyword `!ABC`.

```orca
!PBE D3 ABC
```

:::{note}
Note that not all methods are parameterized for all damping options. E.g. Hartree-Fock (HF) is only parametrized with
BJ-damping, while M06 is only parameterized with zero damping.
:::

The more recent and generally recommended D4 correction can be used with the `!D4` keyword. Note that D4 uses Becke-Johnson damping and the three-body term
by default.

```orca
!PBE D4
```

The D4 correction can also be defined in the `%method` block of the input:

```orca
! PBE def2-TZVP

%method
  DFTDOpt     5     # 5 = D4; 4 = D3(BJ)
end
```

(sec:modelchemistries.dispersioncorrections.dftd.customparams)=
### Custom parameters

If there is a functional for which parameters are known but not yet implemented into ORCA,
they can be sepcified manually via the `%method` block.

:::{warning}
Usage of custom parameters is at own risk and is generally not recommended. A list of some
available parameters for D3 can be found at the [website of the Grimme group](https://www.chemie.uni-bonn.de/grimme/de/software/dft-d3).
:::

:::{important} GGA and hybrid functionals should only be used with
$s_{6}
=1.0$ to ensure asymptotically correct behavior. Double-hybrid
functionals already account for parts of the dispersion interaction and
should therefore be used with $s_{6} < 1.0$.
:::

For D3 with Becke-Johnson damping, the $s_6$, $a_1$, $s_8$, and $a_2$ parameters can be adjusted:


```orca
!B2PLYP D3

%method
  D3S6 0.6400
  D3S8 0.9147
  D3A1 0.3065
  D3A2 5.0570
end
```

For D4, the $s_9$ parameter of the three-body term can be adjusted as well.

```orca
!B2PLYP D4

%method
  D4S6 0.6400
  D4S8 1.1689
  D4A1 0.4415
  D4A2 4.7311
  D4S9 1.0000
end
```

For the D3 variant with zero damping the parameters $s_6$, $rs_6$, $s_8$, and
$\alpha_{6}$ can be adjusted.

```orca
!BLYP D3ZERO

%method
  D3S6     1.000
  D3RS6    1.094
  D3S8     1.682
  D3alpha6 14
end
```

For some functionals, there are also special parameters, which were optimized for use with the def2-TZVPP triple-zeta basis set.
This option is only available with zero damping and can be invoked by
the keywords `!D3ZERO D3TZ`. Preliminary results in the SI of Ref.
{cite}`grimme2010chem` indicate that results are only slightly worse than
with quadruple-zeta basis sets using the default parameters. This option should be
carefully tested for future use in large computations.

(sec:modelchemistries.dispersioncorrections.dftd.example1)=
### Example

In this first example, the DFT-D4 dispersion correction is used.

```orcainput
!PBE def2-TZVP D4

* xyz 0 1
  C     0.000000     0.000000     0.000000
  O     0.000000     0.000000     1.400000
  O     0.000000     0.000000    -1.400000
*
```

The output for the D4 dispersion correction in the ORCA output will look
like this:

```orca
-------------------------------------------------------------------------------
                          DFT DISPERSION CORRECTION                            
                                                                               
                                DFTD4 V3.4.0                                   
-------------------------------------------------------------------------------
The PBE functional is recognized
Active option DFTDOPT                   ...         5   

-------------------------   ----------------
Dispersion correction           -0.000936618
-------------------------   ----------------


-------------------------   --------------------
FINAL SINGLE POINT ENERGY      -188.360452990031
-------------------------   --------------------

```

The total dispersion energy $E_{\text{disp} }$ is given as the `Dispersion correction` and is
automatically included in the final single point energy. As discussed above,
the individual parameters may be adjusted manually.

```orcainput
!PBE def2-TZVP D4

%method
  D4S6 1.0
  D4A1 0.4289
  D4S8 0.7875
  D4A2 4.4407
  D4S9 0.9000
end

* xyz 0 1
  C     0.000000     0.000000     0.000000
  O     0.000000     0.000000     1.400000
  O     0.000000     0.000000    -1.400000
*
```

This results in the same output as above, but with additional
messages that user inputs were found for the parameters:

```orca
A user input s6-coefficient scaling factor has been recognized
A user input a1-coefficient scaling factor has been recognized
A user input s8-coefficient scaling factor has been recognized
A user input a2-coefficient scaling factor has been recognized
A user input s9-coefficient scaling factor has been recognized
```

(sec:modelchemistries.dispersioncorrections.dftd.keywords)=
### Keywords

(tab:modelchemistries.dispersioncorrections.dftd.keywords.simple)=
:::{table} Simple input keywords for the DFT-D corrections.
:class: footnotesize
| Keyword                         | Description                                      |
|:--------------------------------|:-------------------------------------------------|
| `D2`                            | Activates D2 correction                          |
| `D3`                            | Activates D3 correction with BJ damping (D3(BJ)) |
| `D3BJ`                          | Activates D3 correction with BJ damping (D3(BJ)) |
| `D3ZERO`                        | Activates D3 correction with zero damping (D3(0))|
| `D30`                           | Activates D3 correction with zero damping (D3(0)), equivalent to `D3ZERO`         |
| `D3TZ`                          | Activates special triple-$\zeta$ D3 parameterization (only with `D3ZERO`)         |
| `D4`                            | Activates D4 correction (BJ and ATM included)    |
| `ABC`                           | Activates three-body term                        |
| `ATM`                           | Activates three-body term, equivalent to `ABC`   |
| `NOVDW`                         | Deactivates DFT-D dispersion corrections         |
:::

(tab:modelchemistries.dispersioncorrections.dftd.keywords.block)=
:::{table} `%method` block input keywords for the DFT-D corrections.
:class: footnotesize
| Keyword                         | Options           | Description                                      |
|:--------------------------------|:------------------|:-------------------------------------------------|
| `DFTDOPT`                       | `1`               | Activate the original D correction{cite}`GrimmeVDW04` (deprecated)  |
|                                 | `2`               | Activate the D2 correction (deprecated)          |
|                                 | `3`               | Activate the D3ZERO correction                   |
|                                 | `4`               | Activate the D3BJ correction                     |
|                                 | `5`               | Activate the D4 correction                       |
| `D3S6`                          | `<real>`          | Controls $s_6$ parameter for D3                  |
| `D3S8`                          | `<real>`          | Controls $s_8$ parameter for D3                  |
| `D3A1`                          | `<real>`          | Controls $a_1$ parameter for D3                  |
| `D3A2`                          | `<real>`          | Controls $a_2$ parameter for D3                  |
| `D3RS6`                         | `<real>`          | Controls $rs_6$ parameter for zero damping       |
| `D3alpha6`                      | `<real>`          | Controls $\alpha_{6}$ parameter for zero damping |
| `D4S6`                          | `<real>`          | Controls $s_6$ parameter for D4                  |
| `D4S8`                          | `<real>`          | Controls $s_8$ parameter for D4                  |
| `D4A1`                          | `<real>`          | Controls $a_1$ parameter for D4                  |
| `D4A2`                          | `<real>`          | Controls $a_2$ parameter for D4                  |
| `D4S9`                          | `<real>`          | Controls $s_9$ parameter of ABC term for D4      |
| `DFTDScaleC6`                   | `<real>`          | Defines the C6 scaling coefficient               |
:::

(sec:modelchemistries.dispersioncorrections.dftd.params)=
### Available Parameters

(tab:modelchemistries.dispersioncorrections.dftd.params.d4)=
:::{table} DFT-D4 (`!D4`) parameters used for various functionals.
:class: footnotesize
| Functional        | $s_{6}$         | $s_{8}$         | $a_{1}$         | $a_{2}$         | $s_{9}$         |
|:------------------|:---------------:|:---------------:|:---------------:|:---------------:|:---------------:|
|	HF	|	1.0000	|	1.61679827	|	0.44959224	|	3.35743605	|	1.0000	|
|	BLYP	|	1.0000	|	2.34076671	|	0.44488865	|	4.09330090	|	1.0000	|
|	BPBE	|	1.0000	|	3.64405246	|	0.52905620	|	4.11311891	|	1.0000	|
|	BP86	|	1.0000	|	3.35497927	|	0.43645861	|	4.92406854	|	1.0000	|
|	BPW91	|	1.0000	|	3.24571506	|	0.50050454	|	4.12346483	|	1.0000	|
|	GLYP	|	1.0000	|	4.23798924	|	0.38426465	|	4.38412863	|	1.0000	|
|	LB94	|	1.0000	|	2.59538499	|	0.42088944	|	3.28193223	|	1.0000	|
|	mPWLYP	|	1.0000	|	1.25842942	|	0.25773894	|	5.02319542	|	1.0000	|
|	mPWPW	|	1.0000	|	1.82596836	|	0.34526745	|	4.84620734	|	1.0000	|
|	OLYP	|	1.0000	|	2.74836820	|	0.60184498	|	2.53292167	|	1.0000	|
|	OPBE	|	1.0000	|	3.06917417	|	0.68267534	|	2.22849018	|	1.0000	|
|	PBE	|	1.0000	|	0.95948085	|	0.38574991	|	4.80688534	|	1.0000	|
|	RPBE	|	1.0000	|	1.31183787	|	0.46169493	|	3.15711757	|	1.0000	|
|	REVPBE	|	1.0000	|	1.74676530	|	0.53634900	|	3.07261485	|	1.0000	|
|	PW86PBE	|	1.0000	|	1.21362856	|	0.40510366	|	4.66737724	|	1.0000	|
|	RPW86PBE	|	1.0000	|	1.12624034	|	0.38151218	|	4.75480472	|	1.0000	|
|	PW91	|	1.0000	|	0.77283111	|	0.39581542	|	4.93405761	|	1.0000	|
|	PW91P86	|	1.0000	|	0.32801227	|	0.35874687	|	6.05861168	|	1.0000	|
|	XLYP	|	1.0000	|	1.62972054	|	0.11268673	|	5.40786417	|	1.0000	|
|	B97BECKE	|	1.0000	|	0.87854260	|	0.29319126	|	4.51647719	|	1.0000	|
|	TPSS	|	1.0000	|	1.76596355	|	0.42822303	|	4.54257102	|	1.0000	|
|	revTPSS	|	1.0000	|	1.53089454	|	0.44880597	|	4.64042317	|	1.0000	|
|	SCAN	|	1.0000	|	1.46126056	|	0.62930855	|	6.31284039	|	1.0000	|
|	B1LYP	|	1.0000	|	1.98553711	|	0.39309040	|	4.55465145	|	1.0000	|
|	B3LYP	|	1.0000	|	2.02929367	|	0.40868035	|	4.53807137	|	1.0000	|
|	BHANDHLYP	|	1.0000	|	1.65281646	|	0.27263660	|	5.48634586	|	1.0000	|
|	B1P	|	1.0000	|	3.36115015	|	0.48665293	|	5.05219572	|	1.0000	|
|	B3P86	|	1.0000	|	3.08822155	|	0.47324238	|	4.98682134	|	1.0000	|
|	B1PW91	|	1.0000	|	3.02227550	|	0.47396846	|	4.49845309	|	1.0000	|
|	B3PW91	|	1.0000	|	2.88364295	|	0.46990860	|	4.51641422	|	1.0000	|
|	O3LYP	|	1.0000	|	1.75762508	|	0.10348980	|	6.16233282	|	1.0000	|
|	REVPBE0	|	1.0000	|	1.57185414	|	0.38705966	|	4.11028876	|	1.0000	|
|	REVPBE38	|	1.0000	|	1.66597472	|	0.39476833	|	4.39026628	|	1.0000	|
|	PBE0	|	1.0000	|	1.20065498	|	0.40085597	|	5.02928789	|	1.0000	|
|	PWP1	|	1.0000	|	0.60492565	|	0.46855837	|	5.76921413	|	1.0000	|
|	PW1PW	|	1.0000	|	0.96850170	|	0.42427511	|	5.02060636	|	1.0000	|
|	mPW1PW	|	1.0000	|	1.80841716	|	0.42961819	|	4.68892341	|	1.0000	|
|	mPW1LYP	|	1.0000	|	1.15591153	|	0.25603493	|	5.32083895	|	1.0000	|
|	PW6B95	|	1.0000	|	-0.31926054	|	0.04142919	|	5.84655608	|	1.0000	|
|	TPSSh	|	1.0000	|	1.85897750	|	0.44286966	|	4.60230534	|	1.0000	|
|	TPSS0	|	1.0000	|	1.62438102	|	0.40329022	|	4.80537871	|	1.0000	|
|	X3LYP	|	1.0000	|	1.54701429	|	0.20318443	|	5.61852648	|	1.0000	|
|	M06L	|	1.0000	|	0.59493760	|	0.71422359	|	6.35314182	|	1.0000	|
|	M06	|	1.0000	|	0.16366729	|	0.53456413	|	6.06192174	|	1.0000	|
|	wB97	|	1.0000	|	6.55792598	|	0.76666802	|	8.36027334	|	1.0000	|
|	wB97X	|	1.0000	|	-0.07519516	|	0.45094893	|	6.78425255	|	1.0000	|
|	B97M-D4	|	1.0000	|	0.66330000	|	0.42880000	|	3.99350000	|	1.0000	|
|	CAM-B3LYP	|	1.0000	|	1.66041301	|	0.40267156	|	5.17432195	|	1.0000	|
|	LC-BLYP	|	1.0000	|	1.60344180	|	0.45769839	|	7.86924893	|	1.0000	|
|	B2PLYP	|	0.6400	|	1.16888646	|	0.44154604	|	4.73114642	|	1.0000	|
|	B2GP-PLYP	|	0.5600	|	0.94633372	|	0.42907301	|	5.18802602	|	1.0000	|
|	mPW2PLYP	|	0.7500	|	0.45788846	|	0.42997704	|	5.07650682	|	1.0000	|
|	PWPB95	|	0.8200	|	-0.34639127	|	0.41080636	|	3.83878274	|	1.0000	|
|	B97-D	|	1.0000	|	1.69460052	|	0.28904684	|	4.13407323	|	1.0000	|
|	RSCAN	|	1.0000	|	0.87728975	|	0.49116966	|	5.75859346	|	1.0000	|
|	r2SCAN	|	1.0000	|	0.60187490	|	0.51559235	|	5.77342911	|	1.0000	|
|	r2SCANh	|	1.0000	|	0.83240000	|	0.49440000	|	5.90190000	|	1.0000	|
|	r2SCAN0	|	1.0000	|	0.89920000	|	0.47780000	|	5.87790000	|	1.0000	|
|	r2SCAN50	|	1.0000	|	1.04710000	|	0.45740000	|	5.89690000	|	1.0000	|
|	wB97X-D4rev	|	1.0000	|	0.44850000	|	0.33060000	|	4.27900000	|	1.0000	|
|	wB97M-D4rev	|	1.0000	|	0.84200000	|	0.35900000	|	4.66800000	|	1.0000	|
|	wR2SCAN	|	1.0000	|	1.00000000	|	0.38340000	|	5.78890000	|	1.0000	|
|	r2SCAN0-DH	|	0.9424	|	0.38560000	|	0.42710000	|	5.85650000	|	1.0000	|
|	r2SCAN-CIDH	|	0.8666	|	0.53360000	|	0.41710000	|	5.91250000	|	1.0000	|
|	r2SCAN-QIDH	|	0.7867	|	0.29550000	|	0.40010000	|	5.83000000	|	1.0000	|
|	r2SCAN0-2	|	0.7386	|	0.00000000	|	0.40300000	|	5.51420000	|	1.0000	|
|	Pr2SCAN50	|	0.7964	|	0.34210000	|	0.46630000	|	5.79160000	|	1.0000	|
|	kPr2SCAN50	|	0.8402	|	0.12120000	|	0.43820000	|	5.82320000	|	1.0000	|
|	wPr2SCAN50	|	0.8143	|	0.38420000	|	0.41350000	|	5.87730000	|	1.0000	|
|	Pr2SCAN69	|	0.7167	|	0.00000000	|	0.46440000	|	5.25630000	|	1.0000	|
|	revDSD-PBEP86/2021	|	0.5917	|	0.00000000	|	0.37100000	|	4.20140000	|	1.0000	|
|	revDOD-PBEP86/2021	|	0.6158	|	0.00000000	|	0.34400000	|	4.24270000	|	1.0000	|
|	LRC-PBE	|	1.0000	|	1.17000000	|	0.37800000	|	4.81600000	|	1.0000	|
:::

(tab:modelchemistries.dispersioncorrections.dftd.params.d3bj)=
:::{table} DFT-D3(BJ) (`!D3BJ`) parameters used for various functionals.
:class: footnotesize
| Functional        | $s_{6}$         | $s_{8}$         | $a_{1}$         | $a_{2}$         | $s_{9}$         |
|:------------------|:---------------:|:---------------:|:---------------:|:---------------:|:---------------:|
|	HF	|	1.0000	|	0.91710000	|	0.33850000	|	2.88300000	|	1.0000	|
|	BP86	|	1.0000	|	3.28220000	|	0.39460000	|	4.85160000	|	1.0000	|
|	BLYP	|	1.0000	|	2.69960000	|	0.42980000	|	4.23590000	|	1.0000	|
|	REVPBE	|	1.0000	|	2.35500000	|	0.52380000	|	3.50160000	|	1.0000	|
|	B97-D	|	1.0000	|	2.26090000	|	0.55450000	|	3.22970000	|	1.0000	|
|	PBE	|	1.0000	|	0.78750000	|	0.42890000	|	4.44070000	|	1.0000	|
|	RPBE	|	1.0000	|	0.83180000	|	0.18200000	|	4.00940000	|	1.0000	|
|	RPW86PBE	|	1.0000	|	1.38450000	|	0.46130000	|	4.50620000	|	1.0000	|
|	B3LYP	|	1.0000	|	1.98890000	|	0.39810000	|	4.42110000	|	1.0000	|
|	BHANDHLYP	|	1.0000	|	1.03540000	|	0.27930000	|	4.96150000	|	1.0000	|
|	TPSS	|	1.0000	|	1.94350000	|	0.45350000	|	4.47520000	|	1.0000	|
|	TPSS0	|	1.0000	|	1.25760000	|	0.37680000	|	4.58650000	|	1.0000	|
|	PBE0	|	1.0000	|	1.21770000	|	0.41450000	|	4.85930000	|	1.0000	|
|	REVPBE38	|	1.0000	|	1.47600000	|	0.43090000	|	3.94460000	|	1.0000	|
|	PW6B95	|	1.0000	|	0.72570000	|	0.20760000	|	6.37500000	|	1.0000	|
|	B2PLYP	|	0.6400	|	0.91470000	|	0.30650000	|	5.05700000	|	1.0000	|
|	mPWLYP	|	1.0000	|	2.00770000	|	0.48310000	|	4.53230000	|	1.0000	|
|	OLYP	|	1.0000	|	2.62050000	|	0.52990000	|	2.80650000	|	1.0000	|
|	BPBE	|	1.0000	|	4.07280000	|	0.45670000	|	4.39080000	|	1.0000	|
|	OPBE	|	1.0000	|	3.38160000	|	0.55120000	|	2.94440000	|	1.0000	|
|	B3PW91	|	1.0000	|	2.85240000	|	0.43120000	|	4.46930000	|	1.0000	|
|	REVPBE0	|	1.0000	|	1.75880000	|	0.46790000	|	3.76190000	|	1.0000	|
|	TPSSh	|	1.0000	|	2.23820000	|	0.45290000	|	4.65500000	|	1.0000	|
|	CAM-B3LYP	|	1.0000	|	2.06740000	|	0.37080000	|	5.47430000	|	1.0000	|
|	B2GP-PLYP	|	0.5600	|	0.25970000	|	0.00000000	|	6.33320000	|	1.0000	|
|	PWPB95	|	0.8200	|	0.29040000	|	0.00000000	|	7.31410000	|	1.0000	|
|	SCAN	|	1.0000	|	0.00000000	|	0.53800000	|	5.42000000	|	1.0000	|
|	RSCAN	|	1.0000	|	1.08860000	|	0.47020000	|	5.73410000	|	1.0000	|
|	R2SCAN	|	1.0000	|	0.78980000	|	0.49480000	|	5.73080000	|	1.0000	|
|	R2SCANh	|	1.0000	|	1.12360000	|	0.47090000	|	5.91570000	|	1.0000	|
|	R2SCAN0	|	1.0000	|	1.18460000	|	0.45340000	|	5.89720000	|	1.0000	|
|	R2SCAN50	|	1.0000	|	1.32940000	|	0.43110000	|	5.92400000	|	1.0000	|
|	WR2SCAN	|	1.0000	|	1.00000000	|	0.38340000	|	5.78890000	|	1.0000	|
|	r2SCAN0-DH	|	0.9424	|	0.38560000	|	0.42710000	|	5.85650000	|	1.0000	|
|	r2SCAN-CIDH	|	0.8666	|	0.53360000	|	0.41710000	|	5.91250000	|	1.0000	|
|	r2SCAN-QIDH	|	0.7867	|	0.29550000	|	0.40010000	|	5.83000000	|	1.0000	|
|	r2SCAN0-2	|	0.7386	|	0.00000000	|	0.40300000	|	5.51420000	|	1.0000	|
|	Pr2SCAN50	|	0.7964	|	0.34210000	|	0.46630000	|	5.79160000	|	1.0000	|
|	kPr2SCAN50	|	0.8402	|	0.12120000	|	0.43820000	|	5.82320000	|	1.0000	|
|	wPr2SCAN50	|	0.8143	|	0.38420000	|	0.41350000	|	5.87730000	|	1.0000	|
|	Pr2SCAN69	|	0.7167	|	0.00000000	|	0.46440000	|	5.25630000	|	1.0000	|
|	revDSD-PBEP86/2021	|	0.5917	|	0.00000000	|	0.37100000	|	4.20140000	|	1.0000	|
|	revDOD-PBEP86/2021	|	0.6158	|	0.00000000	|	0.34400000	|	4.24270000	|	1.0000	|
|	DSD-BLYP	|	0.5000	|	0.21300000	|	0.00000000	|	6.05200000	|	1.0000	|
|	DSD-BLYP/2013	|	0.5700	|	0.00000000	|	0.00000000	|	5.40000000	|	1.0000	|
|	DSD-PBEB95	|	0.6100	|	0.00000000	|	0.00000000	|	6.20000000	|	1.0000	|
|	DSD-PBEP86	|	0.4180	|	0.00000000	|	0.00000000	|	5.65000000	|	1.0000	|
|	DSD-PBEP86/2013	|	0.4800	|	0.00000000	|	0.00000000	|	5.60000000	|	1.0000	|
|	B97M-D3BJ	|	1.0000	|	0.13840000	|	-0.07800000	|	5.59460000	|	1.0000	|
|	wB97X-D3BJ	|	1.0000	|	0.26410000	|	0.00000000	|	5.49590000	|	1.0000	|
|	wB97M-D3BJ	|	1.0000	|	0.39080000	|	0.56600000	|	3.12800000	|	1.0000	|
|	wB97X-2	|	0.5470	|	0.00000000	|	3.52000000	|	7.79500000	|	1.0000	|
|	PBE0DH	|	0.8800	|	1.08900000	|	0.00000000	|	6.38500000	|	1.0000	|
|	PBE02	|	0.5400	|	0.51500000	|	0.00000000	|	8.34500000	|	1.0000	|
|	PBE-QIDH	|	0.6100	|	0.56600000	|	0.11400000	|	7.53800000	|	1.0000	|
:::

(tab:modelchemistries.dispersioncorrections.dftd.params.d3zero)=
:::{table} DFT-D3(0) (`!D3ZERO`) parameters used for various functionals.
:class: footnotesize
| Functional        | $s_{6}$         | $rs_{6}$         | $s_{8}$         | $\alpha_{6}$         |
|:------------------|:---------------:|:---------------:|:---------------:|:---------------:|
|	HF	|	1.0000	|	1.1580	|	1.7460	|	14	|
|	BLYP	|	1.0000	|	1.0940	|	1.6820	|	14	|
|	BP86	|	1.0000	|	1.1390	|	1.6830	|	14	|
|	B97-D	|	1.0000	|	0.8920	|	0.9090	|	14	|
|	REVPBE	|	1.0000	|	0.9230	|	1.0100	|	14	|
|	PBE	|	1.0000	|	1.2170	|	0.7220	|	14	|
|	RPBE	|	1.0000	|	0.8720	|	0.5140	|	14	|
|	TPSS	|	1.0000	|	1.1660	|	1.1050	|	14	|
|	B3LYP	|	1.0000	|	1.2610	|	1.7030	|	14	|
|	PBE0	|	1.0000	|	1.2870	|	0.9280	|	14	|
|	PW6B95	|	1.0000	|	1.5230	|	0.8620	|	14	|
|	TPSS0	|	1.0000	|	1.2520	|	1.2420	|	14	|
|	B2PLYP	|	0.6400	|	1.4270	|	1.0220	|	14	|
|	B2GP-PLYP	|	0.5600	|	1.5860	|	0.7600	|	14	|
|	PWPB95	|	0.8200	|	1.5570	|	0.7050	|	14	|
|	mPWLYP	|	1.0000	|	1.2390	|	1.0980	|	14	|
|	BPBE	|	1.0000	|	1.0870	|	2.0330	|	14	|
|	BHANDHLYP	|	1.0000	|	1.3700	|	1.4420	|	14	|
|	TPSSh	|	1.0000	|	1.2230	|	1.2190	|	14	|
|	REVPBE0	|	1.0000	|	0.9490	|	0.7920	|	14	|
|	REVPBE38	|	1.0000	|	1.0210	|	0.8620	|	14	|
|	RPW86PBE	|	1.0000	|	1.2240	|	0.9010	|	14	|
|	B3PW91	|	1.0000	|	1.1760	|	1.7750	|	14	|
|	M06L	|	1.0000	|	1.5810	|	0.0000	|	14	|
|	M06	|	1.0000	|	1.3250	|	0.0000	|	14	|
|	M062X	|	1.0000	|	1.6190	|	0.0000	|	14	|
|	wB97X-D3	|	1.0000	|	1.2810	|	1.0000	|	14	|
|	CAM-B3LYP	|	1.0000	|	1.3780	|	1.2170	|	14	|
|	SCAN	|	1.0000	|	1.3240	|	0.0000	|	14	|
|	wB97X-2	|	0.5470	|	4.7330	|	-0.1090	|	14	|
|	PBE0DH	|	0.8800	|	1.1280	|	0.0000	|	14	|
|	PBE02	|	0.5400	|	1.2430	|	-0.2280	|	14	|
|	PBE-QIDH	|	0.4000	|	1.1140	|	0.0540	|	14	|
:::

```{index} DFT-NL, NL
```

(sec:modelchemistries.dispersioncorrections.nl.theory)=
## Non-Local Dispersion Correction (VV10): DFT-NL

A different route to correct for London dispersion is followed by the van der Waals Density Functional
(vdW-DF) as pioneered by Langreth and Lundquist {cite}`lee2010phys`. These
methods use only the electron density to include such
dispersion/correlation effects and can be used in a self-consistent way also correction the molecular orbitals
and not only energies. The vdW correlation functional VV10 of
Vydrov and Van Voorhis {cite}`vydrov2010chem` currently seems to be the most
promising candidate for a general and accurate electronic structure method.

We use the term DFT-NL for any density functional in combination with
the non-local part of the VV10 functional with an optimized parameter
$b$, which will be defined below. The performance of these methods has
been evaluated in Ref. {cite}`hujo2011chem` using the GMTKN30
{cite}`goerigk2010chem,goerigk2011chem,goerigk2011phys` database and the
S66 set {cite}`resac2011chem`. The performance of weak hydrogen bonds were
evaluated in Ref. {cite}`hujo2011phys`.

DFT-NL and DFT-D3/D4 perform very similarly, but NL is to be preferred for
metallic systems or when the basic electronic structure changes
significantly (e.g. oxidations or ionizations). As a recent example,
Janes and Iron showed that for functionals such as wB97X-V, including VV10
correlation results in very high quality reaction barriers when
metals are involved {cite}`iron_evaluating_2019`.

The total exchange-correlation (XC) energy of VV10-type functionals is
defined in eq. {eq}`eqn:modelchemistries.dispersioncorrections.dftnl.theory.exc-dftnl`. It is composed of standard exchange (X) and
correlation (C) parts and the non-local (NL) term, which covers (mainly)
long-range dispersive energy:

$$E_{\text{XC} }^{\text{DFT-NL} } = E_{\text{X} }^{\text{(hybrid)GGA} } +E_{\text{C} }^{\text{GGA} }
+E_{\text{C-NL} }^{\text{VV10} }
$$ (eqn:modelchemistries.dispersioncorrections.dftnl.theory.exc-dftnl)

The NL term is given by the following double integral:

$$E_{\text{C-NL} }^{\text{VV10} }  = \int dr\rho (r)\left[{ \beta
+\frac{1}{2}\mathop \int\nolimits dr'\rho ( { r'}
) \varphi (r,r') } \right]$$ (eqn:modelchemistries.dispersioncorrections.dftnl.theory.ec-vv10)

where $\rho$ is the total electron density, and the definitions of the
kernel $\varphi (r,r')$ and $\beta$ are as follows (in a.u.):

$$\varphi \left({ r,r'} \right) = -\frac{3}{2gg'\left({ g+g'} \right)}
$$ (eqn:modelchemistries.dispersioncorrections.dftnl.theory.vv10-phi)
  
$$\beta = \frac{1}{32}\left[{ \frac{3}{b^{2} }} \right]^{3/4}
$$ (eqn:modelchemistries.dispersioncorrections.dftnl.theory.vv10-beta)

with

$$\begin{aligned}
  g\left( r \right) &= \omega_{0} \left( r \right)R^{2}+\kappa (r) \\ 
  R &= \left|{ r-r'} \right| \\ 
  \omega_{0} \left( r \right) &= \sqrt{ C\left|{ \frac{\nabla \rho (r) }{\rho (r) }} \right|^{4}+\frac{4\pi }{3}\rho (r) } \\ 
  \kappa \left( r \right) &= b\frac{3\pi }{2}\left[{ \frac{\rho (r) }{9\pi } } \right]^{1/6}
\end{aligned}
$$ (eqc:modelchemistries.dispersioncorrections.dftnl.theory.grw0k)

In the original definition, the short-range attenuation parameter $b$
appearing in $\kappa$ and $\beta$ was fitted to the S22 set
{cite}`jurecka2006phys` of non-covalent interactions ($b = 5.9$ for the
rPW86PBE GGA). The other parameter $C = 0.0093$, appearing in
$\omega_{0}$, determines the long-range behavior, and was set to its
original value. Other DFT-NL functionals are constructed analogously.
For a detailed discussion of the derivation of the formulas and their
physical meaning and basis, see the references given above.

The defined energy of the non-local DFT-NL exchange-correlation
functional can be computed in two ways: as a post-SCF addition based on a
converged SCF density or in a self-consistent treatment. In our implementation 
of the non-self-consistent DFT-NL functional,
a self-consistent DFT computation is performed as the first step. In the
second step, the optimized electron density from the DFT computation is
taken as input for the energy calculation of the non-local part. In the self-consistent
treatment, the orbitals and density are optimized in the presence of
the full DFT + VV10 exchange-correlation potential.
According to many test calculations, an self-consistent treatment is rarely
necessary for normal energy evaluations.
The computation of the double integral given in eq. {eq}`eqn:modelchemistries.dispersioncorrections.dftnl.theory.ec-vv10` 
requires using an integration grid, just like for normal exchange-correlation
functionals. This grid is built similarly to the regular grids available
in the ORCA, see Sec. {ref}`sec:essentialelements.numericalintegration`.

(sec:modelchemistries.dispersioncorrections.nl.basicusage)=
### Basic usage

The non-self-consistent variant of NL can be invoked by the `!NL` keyword.

```orca
!B3LYP NL
```
The self-consistent variant by `!SCNL`.

```orca
!B3LYP SCNL
```

In the current version of ORCA, NL parameters are implemented for various functionals and HF:


(tab:modelchemistries.dispersioncorrections.nl.params)=
:::{table} Methods with available NL parameters. If no values are given, the default parameters are used.
:class: footnotesize
| Method                                                    | $b$         | $C$        | $NLScal$                                |
|:----------------------------------------------------------|:-----------:|:----------:|:---------------------------------------:|
| **Hartree-Fock**                                          |             |            |                                         |
| `HF`                                                      | 3.9         |            |                                         |
| **(meta-)GGA**                                            |             |            |                                         |
| `BLYP`                                                    | 4.0         |            |                                         |
| `BP86`                                                    | 4.4         |            |                                         |
| `PBE`                                                     | 6.4         |            |                                         |
| `REVPBE`                                                  | 3.7         |            |                                         |
| `RPBE`                                                    | 4.0         |            |                                         |
| `RPW86PBE`                                                | 5.9         |            |                                         |
| `SCANfunc`                                                | 6.4         |            |                                         |
| `RSCAN`                                                   | 10.8        |            |                                         |
| `R2SCAN`                                                  | 12.3        |            |                                         |
| `TPSS`                                                    | 5.0         |            |                                         |
| `B97M-V`                                                  | 6.0         | 0.01       |                                         |
| **Hybrid**                                                |             |            |                                         |
| `B3LYP`                                                   | 4.8         |            |                                         |
| `B3LYP/G`                                                 | 4.8         |            |                                         |
| `B3P86`                                                   | 5.3         |            |                                         |
| `B3PW91`                                                  | 4.5         |            |                                         |
| `mPW1PW`                                                  | 5.3         |            |                                         |
| `PBE0`                                                    | 6.9         |            |                                         |
| `PW1PW`                                                   | 7.7         |            |                                         |
| `PW6B95`                                                  | 9.0         |            |                                         |
| `REVPBE0`                                                 | 4.3         |            |                                         |
| `REVPBE38`                                                | 4.7         |            |                                         |
| `TPSSh`                                                   | 5.2         |            |                                         |
| `TPSS0`                                                   | 5.5         |            |                                         |
| `R2SCANh` (see {cite}`bursch_r2scanhybrids_2022`)         | 11.9        |            |                                         |
| `R2SCAN0` (see {cite}`bursch_r2scanhybrids_2022`)         | 11.4        |            |                                         |
| `R2SCAN50` (see {cite}`bursch_r2scanhybrids_2022`)        | 10.8        |            |                                         |
| **Range-separated hybrid**                                |             |            |                                         |
| `LRC-PBE`                                                 | 6.4         |            |                                         |
| `WR2SCAN` (see {cite}`Wittmann2023`)                      | 9.2612      |            |                                         |
| `WB97X-V`                                                 | 6.0         | 0.01       |                                         |
| `WB97M-V`                                                 | 6.0         | 0.01       |                                         |
| **Double-hybrid**                                         |             |            |                                         |
| `B2PLYP` (see {cite}`arago_nonlocal_2013`)                | 7.8         |            |                                         |
| `DSD-BLYP` (see {cite}`yu_spin-component-scaled_2014`)    | 12.0        |            |                                         |
| `DSD-PBEP86` (see {cite}`yu_spin-component-scaled_2014`)  | 14.2        |            |                                         |
| `DSD-BLYP/2013`                                           | 12.0        |            |                                         |
| `DSD-PBEP86/2013`                                         | 14.2        |            |                                         |
| `PWPB95` (see {cite}`yu_spin-component-scaled_2014`)      | 11.1        |            |                                         |
| `PR2SCAN50` (see {cite}`Wittmann2023`)                    | 10.9207     |            | 0.75                                    |
| `KPR2SCAN50` (see {cite}`Wittmann2023`)                   | 10.6723     |            | 0.70                                    |
| `PR2SCAN69` (see {cite}`Wittmann2023`)                    | 9.0691      |            | 0.5556                                  |
| **Range-separated double-hybrid**                         |             |            |                                         |
| `WPR2SCAN50` (see {cite}`Wittmann2023`)                   | 9.4149      |            | 0.65                                    |
| `WB97M(2)`                                                | 10.0        | 0.01       | 0.65904                                 |
:::

:::{important}
Head-Gordon's $\omega$B97X-V{cite}`headgordon2014wB97XV`, B97M-V {cite}`headgordon2015B97MV`, and $\omega$B97M-V{cite}`headgordon2016wB97MV` functionals are specially fitted variants that use the non-local VV10 kernel to capture London-dispersion effects.
They employ the non-self-consistent NL correction by default and no additional NL keywords have to be used! A self-consistent treatment can be invoked by the `!SCNL` 
keyword.
:::

:::{admonition} Some notes on the NL corrections in ORCA

* Self-consistent calculations are not possible with the Hartree-Fock method.

* Analytic gradients are available, thus geometry
  optimizations with numerical frequencies can be computed.

* TD-DFT calculations are not yet available.

* Any calculations that require second derivatives of the NL
  functional are not yet possible. These are needed for real type
  perturbations in the CP-SCF solutions, e.g. for analytic Hessians,
  dipole polarizabilities, and double-hybrid gradients.

* Strictly imaginary perturbations such as NMR shielding and EPR
  g-tensors (both also with GIAOs), and hyperfine couplings are
  available.
:::

(sec:modelchemistries.dispersioncorrections.nl.customparams)=
### Custom parameters

For NL, the parameters $b$, $C$, and a global scaling parameter of the NL correlation energy term
can be adjusted via the `%method` block. The global scaling parameter `NLScal` should be used to scale the NL correction
for methods that already partly cover long-range correlatione like double-hybrids.

```orca
!B3LYP NL

%method
  NLb    5.0
  NLC    0.0083
  NLScal 1.0
end
```

:::{Note}
In order to improve the scaling for larger systems,
a distance cutoff was also introduced, controlled by the `vdWdistTCUT` flag in the
`%method` block. The default value is 10 Å, so two grid points more than 10 Å away from each other
do not correlate via the VV10 potential. This is already very conservative
and has practically zero effect on the final energy, but can be altered if needed.
:::

(sec:modelchemistries.dispersioncorrections.nl.example)=
### Example

In the following, we compute the energy of the argon dimer at a
distance of 3.76 Å with the def2-TZVP basis set and using the B3LYP
hybrid functional as an example. Here, we choose the non-self-consistent
variant of the DFT-NL dispersion correction.

```orcainput
!B3LYP NL def2-TZVP

*xyz 0 1
  Ar  0.0 0.0 0.0
  Ar  0.0 0.0 3.76
*
```

The DFT-NL output for this example is shown below:

```orca
-------------------------------------------------------------------------------
                    post-SCF DFT-NL dispersion correction                      
-------------------------------------------------------------------------------

SCF Energy:    -1054.960511496 
NL    Energy:      0.209449910 
SC+NL Energy:  -1054.751061586 
NL done in  :              0.7 sec
-------------------------------------------------------------------------------

[...]

----------------
TOTAL SCF ENERGY
----------------

[...]

DFT components:
N(Alpha)           :       17.999996328440 electrons
N(Beta)            :       17.999996328440 electrons
N(Total)           :       35.999992656880 electrons
E(X)               :      -47.880920358714 Eh       
E(C)               :       -1.761923687962 Eh       
NL Energy, E(C,NL) :        0.209449910227 Eh       
E(XC)              :      -49.433394136450 Eh
```

Here, we find the B3LYP total energy (`SCF Energy`), the
non-local contribution (`NL Energy`), and their sum (`SC+NL Energy`), 
which is the final total energy. In the `DFT components` section, the non-local contribution is
listed separately (`NL Energy, E(C,NL)`) in order to be consistent with the `!SCNL` output.

(sec:modelchemistries.dispersioncorrections.nl.keywords)=
### Keywords

(tab:modelchemistries.dispersioncorrections.nl.keywords.simple)=
:::{table} Simple input keywords for the NL correction.
:class: footnotesize
| Keyword                         | Description                                      |
|:--------------------------------|:-------------------------------------------------|
| `NL`                            | Activates non-self-consistent NL correction      |
| `SCNL`                          | Activates self-consistent NL correction          |
:::

(tab:modelchemistries.dispersioncorrections.nl.keywords.block)=
:::{table} `%method` block input keywords for the NL correction.
:class: footnotesize
| Keyword                         | Options           | Description                                      |
|:--------------------------------|:------------------|:-------------------------------------------------|
| `NLb`                           | `<real>`          | Controls $b$ parameter for NL                    |
| `NLC`                           | `<real>`          | Controls $C$ parameter for NL                    |
| `NLScal`                        | `<real>`          | Controls the global scaling parameter for NL     |
| `vdWdistTCUT`                   | `<real>`          | Controls the correlation distance cutoff for NL  |
:::
