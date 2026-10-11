

<a id="sec:essentialelements.counterpoise"></a>
# Counterpoise Corrections

<a id="sec:essentialelements.counterpoise.bbcp"></a>
## Boys-Bernardi Counterpoise Correction (BB-CP)

In calculating weak molecular interactions the nasty subject of the
basis set superposition error (BSSE) arises. It consists of the fact
that if one describes a dimer, the basis functions on A help to lower
the energy of fragment B and vice versa. Thus, one obtains an energy
that is biased towards the dimer formation due to basis set effects.
Since this is unwanted, the Boys and Bernardi procedure aims to correct
for this deficiency by estimating what the energies of the monomers
would be if they had been calculated with the dimer basis set. This will
stabilize the monomers relative to the dimers. The effect can be a quite
sizable fraction of the interaction energy and should therefore be
taken into account. The original Boys and Bernardi formula for the
interaction energy between fragments A and B is:

$$
\Delta E = E^{AB}_{AB}(AB) - E^{A}_{A}(A) - E^{B}_{B}(B) - \left[E^{AB}_{A}(AB) - E^{AB}_{A}(A) + E^{AB}_{B}(AB) - E^{AB}_{B}(B)\right]\qquad \text{(eqn:5)}
$$

Here $E_{X}^{Y} \left( Z \right)$ is the energy of fragment X calculated
at the optimized geometry of fragment Y with the basis set of fragment
Z. Thus, you need to do a total the following series of calculations:

1. optimize the geometry of the dimer and the monomers with some basis
set Z. This gives you $E_{AB}^{AB} \left({ AB} \right)$,
$E_{A}^{A} \left( A \right)$ and $E_{B}^{B} \left( B \right)$

2. delete fragment A (B) from the optimized structure of the dimer and re-run the
single point calculation with basis set Z. This gives you
$E_{B}^{AB} \left( B \right)$ and $E_{A}^{AB} \left( A \right)$.

3. Now, the final calculation consists of calculating the
energies of A and B at the dimer geometry but with the dimer basis set.
This gives you $E_{A}^{AB} \left({ AB} \right)$ and
$E_{B}^{AB} \left({ AB} \right)$.

In order to achieve the last step efficiently, a special notation was
put into ORCA which allows you to delete the electrons and nuclear
charges that come with certain atoms but retain the assigned basis set.
This trick consists of putting a ":" after the symbol of the atom. Here
is an example of how to run such a calculation of the water dimer at the
MP2 level (with frozen core):

```mol
title: structure 1
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
24
structure (0 1)
O      7.405639     6.725069     7.710504
H      7.029206     6.234628     8.442160
H      8.247948     6.296600     7.554030
O      7.405639     6.725069     7.710504
H      7.029206     6.234628     8.442160
H      8.247948     6.296600     7.554030
O      7.439917     6.726792     7.762120
O      5.752050     6.489306     5.407671
H      7.025510     6.226170     8.467436
H      8.274883     6.280259     7.609894
H      6.313507     6.644667     6.176902
H      5.522285     7.367132     5.103852
O      7.439917     6.726792     7.762120
H      7.025510     6.226170     8.467436
H      8.274883     6.280259     7.609894
O      5.752050     6.489306     5.407671
H      6.313507     6.644667     6.176902
H      5.522285     7.367132     5.103852
O      7.439917     6.726792     7.762120
H      7.025510     6.226170     8.467436
H      8.274883     6.280259     7.609894
O      5.752050     6.489306     5.407671
H      6.313507     6.644667     6.176902
H      5.522285     7.367132     5.103852
--- input ---
#
# Calculations for Boys-Bernardi CP correction
#

# --------------------------------------------
# First the monomer. In principle, you only need
# to run it once, but we keep it for clarity.
# --------------------------------------------
! RHF MP2 cc-pVTZ VeryTightSCF PModel
%id "monomer"
* xyz 0 1
 O     7.405639     6.725069     7.710504
 H     7.029206     6.234628     8.442160
 H     8.247948     6.296600     7.554030
*

$new_job
! RHF MP2 cc-pVTZ VeryTightSCF PModel
%id "monomer"
* xyz 0 1
 O     7.405639     6.725069     7.710504
 H     7.029206     6.234628     8.442160
 H     8.247948     6.296600     7.554030
*

# --------------------------------------------
# now the dimer
# --------------------------------------------
$new_job
! RHF MP2 cc-pVTZ VeryTightSCF PModel
%id "dimer"
* xyz 0 1
O   7.439917   6.726792   7.762120
O   5.752050   6.489306   5.407671
H   7.025510   6.226170   8.467436
H   8.274883   6.280259   7.609894
H   6.313507   6.644667   6.176902
H   5.522285   7.367132   5.103852
*

# --------------------------------------------
# Now the calculations of the monomer at the
# dimer geometry
# --------------------------------------------
$new_job
! RHF MP2 cc-pVTZ VeryTightSCF PModel
%id "monomer_1"

* xyz 0 1
O   7.439917   6.726792   7.762120
H   7.025510   6.226170   8.467436
H   8.274883   6.280259   7.609894
*

$new_job
! RHF MP2 cc-pVTZ VeryTightSCF PModel
%id "monomer_1"
* xyz 0 1
O   5.752050   6.489306   5.407671
H   6.313507   6.644667   6.176902
H   5.522285   7.367132   5.103852
*

# --------------------------------------------
# Now the calculation of the monomer at the
# dimer geometry but with the dimer basis set
# --------------------------------------------
$new_job
! RHF MP2 cc-pVTZ VeryTightSCF PModel
%id "monomer_2"
* xyz 0 1
O   7.439917   6.726792   7.762120
O : 5.752050   6.489306   5.407671
H   7.025510   6.226170   8.467436
H   8.274883   6.280259   7.609894
H : 6.313507   6.644667   6.176902
H : 5.522285   7.367132   5.103852
*

$new_job
! RHF MP2 cc-pVTZ VeryTightSCF PModel
%id "monomer_2"
* xyz 0 1
O : 7.439917   6.726792   7.762120
O   5.752050   6.489306   5.407671
H : 7.025510   6.226170   8.467436
H : 8.274883   6.280259   7.609894
H   6.313507   6.644667   6.176902
H   5.522285   7.367132   5.103852
*
```
From these calculations, you obtain the respective energies to compute the BB-CP correction:

<a id="tab:essentialelements.counterpoise.bbcp"></a>
!!! note "Energies calculated for the Boys-Bernardi counter-poise correction and final dimerization energies."
    | Component                   | E [a.u.]            | E [kcal/mol]  |
    |:----------------------------|--------------------:|--------------:|
    | $E^{AB}_{AB}(AB)$           | -152.646980         |               |
    | $E^{A}_{A}(A)$              | -76.318651          |               |
    | $E^{B}_{B}(B)$              | -76.318651          |               |
    | $E^{AB}_{A}(AB)$            | -76.320799          |               |
    | $E^{AB}_{A}(A)$             | -76.318635          |               |
    | $E^{AB}_{B}(AB)$            | -76.319100          |               |
    | $E^{AB}_{B}(B)$             | -76.318605          |               |
    | $\Delta E_{dim.}$           | -0.009677           | -6.07         |
    | $\Delta E_{BB-CP}$          | 0.002659            | 1.67          |
    | $\Delta E_{dim., corr.}$    | -0.007018           | -4.40         |

In this example, we calculated a BSSE correction of 1.67 kcal/mol.

It is also possible to set entire fragments as ghost atoms using the
`GhostFrags` keyword as shown below. See
section [essentialelements.coordinates](coordinates.md#sec:essentialelements.coordinates) for different ways of defining
fragments.

```mol
title: structure 2
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
6
structure (0 1)
O      7.439917     6.726792     7.762120
O      5.752050     6.489306     5.407671
H      7.025510     6.226170     8.467436
H      8.274883     6.280259     7.609894
H      6.313507     6.644667     6.176902
H      5.522285     7.367132     5.103852
--- input ---
! MP2 cc-pVTZ VeryTightSCF PModel
* xyz 0 1
  O   7.439917   6.726792   7.762120
  O   5.752050   6.489306   5.407671
  H   7.025510   6.226170   8.467436
  H   8.274883   6.280259   7.609894
  H   6.313507   6.644667   6.176902
  H   5.522285   7.367132   5.103852
*
%frag
  Definition
    1 {0 2 3} end
    2 {1 4 5} end
  end
end
%geom
  GhostFrags {1} end # space-separated list and X:Y ranges accepted
end
```

Starting from ORCA 6.0, we support geometry optimizations with
the counterpoise correction, using analytic gradients. This
opens up the way of obtaining accurate non-covalent complex
geometries (instead of just interaction energies) using modest basis sets.
To use this functionality, one should NOT simply add `!Opt` to the
above input files, but should instead use the dedicated compound
script `BSSEOptimization.cmp` available in the ORCA [Compound Script
repository](https://github.com/ORCAQuantumChemistry/CompoundScripts/blob/main/GeometryOptimization/BSSEOptimization.cmp).
Detailed usage are described in the comments of the
compound script.

<a id="sec:essentialelements.counterpoise.gcp"></a>
## Geometrical Counterpoise Correction (gCP)

The central idea of the gCP correction [KrusegCP](../../bibliography.md) is to add a semi-empirical
correction $\Delta E_{\text{gCP} }$ to the energies of molecular systems
that removes artificial overbinding effects from BSSE. gCP
uses atomic corrections and therefore also has the ability to correct for
intramolecular BSSE. The parametrization is constructed such that it
approximates the Boys and Bernadi counterpoise (CP) correction
$\Delta E_{CP}$ in the intermolecular case. That is,

$$
\Delta E_{CP}\approx \Delta E_{\text{gCP} }\qquad \text{(eqn:ecp-gcp)}
$$

where e.g. for a complexation reaction $A+B\to C$, our correction is
given by

$$
\Delta E_{\text{gCP} }=E_{\text{gCP} }(C)-E_{\text{gCP} }(A)-E_{\text{gCP} }(B)\qquad \text{(eqn:de-gcp)}
$$

In practice, $E_{\text{gCP} }$ can be simply added to the HF/DFT energy

$$
E_{\text{total}}  =  E_{\text{HF/DFT}} + E_{\text{gCP} }\qquad \text{(eqn:etot-gcp)}
$$

which is done automatically in ORCA (the `FINAL SINGLE POINT ENERGY` includes
the gCP correction).

The central equation of the gCP correction over all atoms $N$ reads:

$$
E_{\text{gCP} }  =  \sigma \cdot \sum_{a}^{N} \sum_{b \neq a}^{N}  e_a^{\text{miss} }  \cdot f_{\text{dec} }(R_{ab})\qquad \text{(eqn:gcp)}
$$

where the energy $e_a^{\text{miss} }$ is a measure of the
incompleteness of the chosen target basis set (which is typically small)
and $f_{\text{dec} }(R_{ab})$ is a decay function that depends on the
interatomic distance $R_{ab}$. The scaling factor $\sigma$ is one of 4 parameters needed for every
`method/basis set` combination. More details on this can be found in the
original gCP paper [KrusegCP](../../bibliography.md).

Analytical gradients with gCP are available for geometry optimization. Due to its
semi-empirical nature, the correction is calculated within seconds,
even for very large systems.

<a id="sec:essentialelements.counterpoise.gcp.basicusage"></a>
### Basic Usage
The gCP correction can be invoked by the `!GCP(level)` keyword, where
`level` is a combination of the method (Hartree-Fock, `HF` or density functional theory, `DFT`) and a
basis set definition. See [tab:essentialelements.counterpoise.gcp](#tab:essentialelements.counterpoise.gcp) for the available basis sets and the corresponding
keywords. For example, gCP can be invoked in a B3LYP calculation with the def2-SV(P) basis set
using the input:

```orca
! B3LYP def2-SV(P) GCP(DFT/SV(P))
```
The gCP input can also be defined in the `%method` block of the input:

```orca
! B3LYP def2-SV(P)

%method
  DoGCP       true
  GCPMETHOD   dft/sv(p)
end
```

<a id="tab:essentialelements.counterpoise.gcp"></a>
!!! note "Overview of parametrized basis sets. The `level` keyword in `!GCP(level)` is a combination of `HF` or `DFT` and the `basis set` keyword. Valid inputs are, for example: `!GCP(HF/MINIS)`, `!GCP(DFT/LANL)`, `!GCP(HF/TZ)`, `!GCP(DFT/631GD)`, $\ldots$"
    | Parametrized basis set     | Definition          | HF  | DFT |
    |:---------------------------|:--------------------|:---:|:---:|
    | MINIS                      | MINIS               | yes | yes |
    | SV                         | SV                  | yes | yes |
    | 6-31G(d)                   | 631GD               | yes | yes |
    | 6-31G(d) + LANL2DZ (Sc-Zn) | LANL                | no  | yes |
    | def2-SV(P)                 | SV(P)               | no  | yes |
    | def2-SVP                   | SVP                 | yes | yes |
    | def2-TZVP                  | TZ                  | yes | yes |

At all print levels, warnings from the gCP program are printed. Using the default
print level, the only additional output is the final gCP correction before
`FINAL SINGLE POINT ENERGY`. Using `!LargePrint` or `%output Print[P_gCP] 2 end`
states the gCP `level`, the 4 parameters mentioned above, and the computed correction.
A larger print level can be specified to get more details (more information on this below).

Several warnings and notices may be issued. Elements of the 5th
and higher periods are treated as their 4th period analogs --- e.g. Sn is
treated with the same parameters as Ge. If this is the case, a
note is printed. Another note is printed if there is a mismatch between
the basis used for the SCF calculation and that of the requested gCP
calculation. For example, the following input with tetramethyltin

```orca
! HF def2-SVP GCP(HF/MINIS)
*xyzfile 0 1 tetramethyltin.xyz
```

should use the parameters of Ge in place of Sn and there should be a
mismatch between the basis set in ORCA (def2-SVP) and gCP (MINIS).
Sure enough, the output is as follows:

```orca
 ** NOTE ** -> element sn will be treated as ge
NOTIFICATION: Different basis set in ORCA and otool_gcp:
ORCA: 142  gCP: 32 
If you are NOT using ECPs, check your basis set inputs!
------------------   -----------------
gCP correction             0.073031339
------------------   -----------------
```

A mismatch between the basis sets used is allowed since
a minor mismatch may only result in a small error. One should still be careful
with such results; use your own judgment! This also allows gCP in calculations that
use an unparametrized basis set. However, in this case, the number of basis functions
and exponents should be very similar!

It should be noted that some elements are not parametrized, depending on the
gCP `level` used. If only a few atoms in a large molecule are treated inaccurately or not at all,
the error is expected to be small. To check all parameters used and the individual atomic
contributions, specify the print level `%output Print[P_gCP] 3 end`. For example, the above
tetramethyltin input with this print level has the following output:

```orca
------------------------------------------------------------------------------
                                                                              
                  g C P  - geometrical counterpoise correction     
                                                                              
------------------------------------------------------------------------------
Method:  hf/minis 
  
 ** NOTE ** -> element sn will be treated as ge
Parameters:   sigma        eta         alpha        beta 
              0.1290      1.1526      1.1549       1.1763 
Nbf:   32  
NAtoms:   17  
  
gCP element parameters: 
  elem   emiss   nbas    elem   emiss   nbas    elem   emiss   nbas
    h    0.04240    1      he   0.02832    1      li   0.25266    2
    be   0.19720    2      b    0.22424    5      c    0.27995    5
    n    0.35791    5      o    0.47901    5      f    0.63852    5
    ne   0.83235    5      na   1.23292    6      mg   1.34339    6
    al   1.44828    9      si   1.61336    9      p    1.76814    9
    s    1.99201    9      cl   2.23311    9      ar   2.49323    9
    k    3.02964   10      ca   3.38998   10      sc   0.00000    0
    ti   0.00000    0      v    0.00000    0      cr   0.00000    0
    mn   0.00000    0      fe   0.00000    0      co   0.00000    0
    ni   0.00000    0      cu   0.00000    0      zn   0.00000    0
    ga   0.00000    0      ge   0.00000    0      as   0.00000    0
    se   0.00000    0      br   0.00000    0      kr   0.00000    0
  
      #     ON  sites    Nvirt           Emiss    BSSE [kcal/mol]
      1      6     15      2.0          0.2799         10.0090
      2     32     16    -16.0          0.0000          0.0000
      3      6     15      2.0          0.2799         10.0084
      4      6     15      2.0          0.2799         10.0095
      5      6     15      2.0          0.2799         10.0083
      6      1     15      0.5          0.0424          0.4827
      7      1     15      0.5          0.0424          0.4828
      8      1     15      0.5          0.0424          0.4828
      9      1     15      0.5          0.0424          0.4827
     10      1     15      0.5          0.0424          0.4827
     11      1     15      0.5          0.0424          0.4827
     12      1     15      0.5          0.0424          0.4828
     13      1     15      0.5          0.0424          0.4827
     14      1     15      0.5          0.0424          0.4828
     15      1     15      0.5          0.0424          0.4827
     16      1     15      0.5          0.0424          0.4827
     17      1     15      0.5          0.0424          0.4827
Egcp:       0.0730313386 a.u.
NOTIFICATION: Different basis set in ORCA and otool_gcp:
ORCA: 142  gCP: 32 
If you are NOT using ECPs, check your basis set inputs!
------------------   -----------------
gCP correction             0.073031339
------------------   -----------------
```

From this, it can be seen that the Sn atom (atom 2 in the list of atomic contributions)
gives no contribution because its `Emiss` is zero (unparametrized for the given gCP `level`).
This is confirmed by looking at the `gCP element parameters` section, which lists the `emiss` of
Sn as zero for `!GCP(HF/MINIS)`. Rerunning this example with `!GCP(HF/SVP)` now gives a
contribution for Sn, as seen by the following output. Note that this calculation also has a
much smaller basis set mismatch, and so should be the more accurate gCP correction of the two.

```orca
------------------------------------------------------------------------------
                                                                              
                  g C P  - geometrical counterpoise correction     
                                                                              
------------------------------------------------------------------------------
Method:  hf/svp 
  
 ** NOTE ** -> element sn will be treated as ge
Parameters:   sigma        eta         alpha        beta 
              0.2054      1.3157      0.8136       1.2572 
Nbf:   148  
NAtoms:   17  
  
gCP element parameters: 
  elem   emiss   nbas    elem   emiss   nbas    elem   emiss   nbas
    h    0.00811    5      he   0.00805    5      li   0.11358    9
    be   0.02837    9      b    0.04937   14      c    0.05538   14
    n    0.07278   14      o    0.10031   14      f    0.13327   14
    ne   0.17360   14      na   0.18114   15      mg   0.12556   18
    al   0.16719   18      si   0.14984   18      p    0.14540   18
    s    0.16431   18      cl   0.18299   18      ar   0.20567   18
    k    0.20096   24      ca   0.29966   24      sc   0.32599   31
    ti   0.30549   31      v    0.29172   31      cr   0.29380   31
    mn   0.29179   31      fe   0.29673   31      co   0.30460   31
    ni   0.24204   31      cu   0.35419   31      zn   0.35072   31
    ga   0.35002   32      ge   0.34578   32      as   0.34953   32
    se   0.36731   32      br   0.38201   32      kr   0.39971   32
  
      #     ON  sites    Nvirt           Emiss    BSSE [kcal/mol]
      1      6     16     11.0          0.0554          2.5093
      2     32     16     16.0          0.3458          6.8274
      3      6     16     11.0          0.0554          2.5092
      4      6     16     11.0          0.0554          2.5094
      5      6     16     11.0          0.0554          2.5092
      6      1     16      4.5          0.0081          0.1703
      7      1     16      4.5          0.0081          0.1703
      8      1     16      4.5          0.0081          0.1703
      9      1     16      4.5          0.0081          0.1703
     10      1     16      4.5          0.0081          0.1703
     11      1     16      4.5          0.0081          0.1703
     12      1     16      4.5          0.0081          0.1703
     13      1     16      4.5          0.0081          0.1703
     14      1     16      4.5          0.0081          0.1703
     15      1     16      4.5          0.0081          0.1703
     16      1     16      4.5          0.0081          0.1703
     17      1     16      4.5          0.0081          0.1703
Egcp:       0.0301322002 a.u.
NOTIFICATION: Different basis set in ORCA and otool_gcp:
ORCA: 142  gCP: 148 
If you are NOT using ECPs, check your basis set inputs!
------------------   -----------------
gCP correction             0.030132200
------------------   -----------------
```

!!! note "General advice"
    -   Small basis sets show not only a large BSSE, but general
        shortcomings. These effects are not always clearly distinguishable.

    -   If computationally affordable, large basis sets (triple-$\zeta$ and
        higher) are always preferable.

    -   gCP only makes sense for somewhat large molecules

    -   gCP should always be applied together with a dispersion correction.
        gCP in combination with D3 or D4 is well tested, but gCP with NL also works well (see
        chapter [modelchemistries.dispersioncorrections](../modelchemistries/dispersioncorrections.md#sec:modelchemistries.dispersioncorrections)).

    -   It has been demonstrated that the popular combination of B3LYP with
    6-31G(d) can be strongly improved using DFT-D3 and
    gCP [KruseB3LYPgCPD3](../../bibliography.md). For convenience, the keyword `!B3LYP-gCP-D3/6-31G*`
    has been defined. This is equivalent to `!B3LYP 6-31G* D3BJ GCP(DFT/631GD)`.

!!! note "Technical Notes"
    -   `!GCP(HF/MINIS)` automatically sets the refitted D3 parameter, as proposed in
    the original gCP paper.

    -   The gCP method is implemented via an external tool called **otool_gcp**,
    which is based on the original Fortran program used in the publication.
    Thus, the `otool_gcp` binary can also be called directly via the command
    line (`otool_gcp -h` gives an overview of the options).

    -   It is also possible to read an external parameter file (`$HOME/.gcppar`) using the
    `!GCP(FILE)` keyword. For further information, please look at the manual for
    the gcp program as provided by the Grimme group ([gCP manual](https://www.chemie.uni-bonn.de/grimme/de/software/gcp/mangcp.pdf)).

    -   During the calculation, some temporary output files are written by ORCA:
    `BASENAME.gcp.in.tmp` and `BASENAME.gcp.out.tmp` will contain the input for
    `otool_gcp` and its output, respectively.

<a id="sec:essentialelements.counterpoise.gcp.keywords"></a>
### Keywords

<a id="tab:essentialelements.counterpoise.gcp.keywords.simple"></a>
!!! note "Simple input keywords for the gCP correction."
    | Keyword                         | Description                                                          |
    |:--------------------------------|:---------------------------------------------------------------------|
    | `GCP(<level>)`                  | Activates the gCP correction for a specified level of theory defined as `<level>`          |

<a id="tab:essentialelements.counterpoise.gcp.keywords.block"></a>
!!! note "`%method` block input keywords and options for the gCP correction."
    | Keyword                         | Option            | Description                                      |
    |:--------------------------------|:------------------|:-------------------------------------------------|
    | `DoGCP`                         | `true`/`false`    | Activate/deactivate the gCP correction           |
    | `GCPMETHOD`                     | `<level>`         | Define the gCP level string, e.g. `dft/svp`     |
    |                                 | `hf/minis`        | Parameterization for HF with MINIS basis set     |
    |                                 | `hf/sv`           | Parameterization for HF with SV basis set        |
    |                                 | `hf/631gd`        | Parameterization for HF with 6-31G(d) basis set  |
    |                                 | `hf/svp`          | Parameterization for HF with def2-SVP basis set  |
    |                                 | `hf/tz`           | Parameterization for HF with def2-TZVP basis set |
    |                                 | `dft/minis`       | Parameterization for DFT with MINIS basis set    |
    |                                 | `dft/sv`          | Parameterization for DFT with SV basis set       |
    |                                 | `dft/631gd`       | Parameterization for DFT with 6-31G(d) basis set |
    |                                 | `dft/lanl`        | Parameterization for DFT with mixed 6-31G(d) + LANL2DZ (Sc-Zn) basis set        |
    |                                 | `dft/sv(p)`       | Parameterization for DFT with def2-SV(P) basis set |
    |                                 | `dft/svp`         | Parameterization for DFT with def2-SVP basis set |
    |                                 | `dft/tz`          | Parameterization for DFT with def2-TZVP basis set|
    |                                 | `file`            | Read parameters from external parameterfile `$HOME/.gcppar` |
    | `GCP.D3MINIS`                   | `true`/`false`    | Use special DFT-D3 refit for HF/MINIS (default=true) |

