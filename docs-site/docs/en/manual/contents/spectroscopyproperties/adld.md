

<a id="sec:spectroscopyproperties.adldd"></a>
# ADLD(D): Atomic Decomposition of DFT-D London Dispersion Energy

Starting from version 6.1, ORCA offers a method to quantify the London dispersion energy (LD) with atomic resolution in conjunction with a wide range of electronic structure techniques, as described in [baldinelli2024unraveling](../../bibliography.md) and [regni2025ADLD](../../bibliography.md). A special case of this decomposition scheme is the atomic decomposition of the [DFT-D](#sec:modelchemistries.dispersioncorrections) London Dispersion energies (e.g. ADLD(D4) for DFT-D4). This scheme is available for D2, D3, and D4. The original scheme for DLPNO-based LED methods is documented in the [ADLD(LED) section](#sec:spectroscopyproperties.led.ad).

<a id="sec:spectroscopyproperties.adld.dftd.theory"></a>
## Theory

The atomic LD energy for DFT-D is assessed by assigning half of the pairwise contribution to each atom of the pair and iterating over all atoms:

$$
E_{\text{disp}}^{\text{DFT-D}} (AB) = \sum_{A>B} \epsilon_{AB}^{\text{DFT-D}} = \frac{1}{2} \sum_{A} \sum_{B \neq A} \epsilon_{AB}^{\text{DFT-D}} = \sum_{A} \epsilon_{A}^{\text{DFT-D}} (AB)\qquad \text{(eqn:spectroscopyproperties.adld.dftd.theory.ab)}
$$

If three-body effects are included in the calculation, the decomposition includes them as well:

$$
E_{\text{disp}}^{\text{DFT-D}} (ABC) = \sum_{A>B>C} \epsilon_{ABC}^{\text{DFT-D}} = \frac{1}{6} \sum_{A} \sum_{B \neq A \neq C} \epsilon_{ABC}^{\text{DFT-D}} = \sum_{A} \epsilon_{A}^{\text{DFT-D}} (ABC)\qquad \text{(eqn:spectroscopyproperties.adld.dftd.theory.abc)}
$$

<a id="sec:spectroscopyproperties.adld.dftd.basicusage"></a>
### Basic Usage

The atomic decomposition of LD energy is invoked using the `!ADLD` keyword in the simple input line.

```orca
! PBE D3 def2-TZVP ADLD
```

<a id="sec:spectroscopyproperties.adld.dftd.example"></a>
### Example

As an example, the atomic dispersion energies at the B3LYP-D4/def2-TZVP level of a water dimer can be analyzed using the following input file:

```mol
title: structure 1
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
6
structure (0 1)
O  0.00736774224494 0.01160693915772 0.01654049355157
H  0.96923953706804 0.01163512314627 -0.00786387302697
H  -0.23645852051665 0.94172445362186 -0.01797690491825
O  -0.98965374142797 -1.29474095640989 2.41552530001642
H  -0.69837507632022 -0.90508483715064 1.57804074703869
H  -1.52582551183659 -2.04783550111168 2.15519678840530
--- input ---
! B3LYP D4 def2-TZVP ADLD

# H2O dimer geometry optimized at the B3LYP-D4/def2-TZVP level.

* xyz 0 1
  O       0.00736774224494      0.01160693915772      0.01654049355157
  H       0.96923953706804      0.01163512314627     -0.00786387302697
  H      -0.23645852051665      0.94172445362186     -0.01797690491825
  O      -0.98965374142797     -1.29474095640989      2.41552530001642
  H      -0.69837507632022     -0.90508483715064      1.57804074703869
  H      -1.52582551183659     -2.04783550111168      2.15519678840530
*
```

The corresponding output file is reported below. The LD energy in atomic units is printed for each atom, along with the total dispersion. The output format remains consistent for the other -D corrections.

```orca
------------------------------------------------------------
      ADLD - Atomic Decomposition of London Dispersion      
------------------------------------------------------------

Atom   Type     Dispersion (a.u.)
---------------------------------
 1      O            -0.000523477  
 2      H            -0.000128807  
 3      H            -0.000128264  
 4      O            -0.000477971  
 5      H            -0.000163561  
 6      H            -0.000120093  

Total dispersion     -0.001542174
```

<a id="sec:spectroscopyproperties.adld.dftd.keywords"></a>
### Keywords

<a id="tab:spectroscopyproperties.ADLD.dftd.keywords.simple"></a>
!!! note "Simple input keywords for the atomic decomposition of London dispersion calculated with DFT-D correction."
    | Keyword                         | Description                                      |
    |:--------------------------------|:-------------------------------------------------|
    | `ADLD`                          | Activates atomic decomposition of LD             |

