

<a id="sec:spectroscopyproperties.properties.eprnmr.MP2magnetic"></a>
# MP2 Level Magnetic Properties

Presently, hyperfine couplings (excluding the $A_\text{orb}$ term),
g-tensors, and shielding tensors without GIAOs can be calculated for
both canonical and RI-MP2 and double-hybrid DFT without the frozen core
approximation. The $A_\text{orb}$ term of the hyperfine couplings is
available only for RI-MP2 and double-hybrid DFT with and without frozen
core approximation. In case the RIJCOSX approximation is used, the
keywords `Z_GridX`, `Z_GridX_RHS`, `KCOpt`, `KC_GridX` and `KC_IntAccX`
are relevant -- see
sections [mp2.rijcosxrigrad](#sec:modelchemistries.mp2.rijcosxrigrad) and
[mp2.2ndder](#sec:modelchemistries.mp2.2ndder). NMR shielding and g-tensor
calculations with GIAOs are available for RI-MP2 and double-hybrid DFT
with or without a frozen core. The implementation is described in detail
in refs [Stoychev2018RIMP2NMR,Tran2020RIMP2GIAO](../../bibliography.md) and the available
options are shown in
section [rimp2.response](#sec:modelchemistries.mp2.rimp2.response). Note that for double-hybrid
DFT the correct properties are printed after the density heading containing
"Method : MP2" and "Level : Relaxed density". 
DLPNO-MP2 (and double-hybrid) shielding tensors are also available - see
section [mp2.dlpnoresp](#sec:modelchemistries.mp2.dlpnoresp).

<a id="sec:spectroscopyproperties.properties.proponly"></a>
## Calculating Properties from Existing Densities

Occasionally, one may calculate a density matrix using an expensive
correlated method such as CCSD and realize afterwards that a certain
property such as the quadrupole moment or a hyperfine coupling constant
(HFCC) is also required. Rather than start the whole calculation from
scratch, one may wish to use the existing density matrix to calculate
the properties. For this purpose, we have experimentally introduced a
"properties only" calculation mode, whereby the MOs are read from an
existing *BaseName.gbw* file and the densities are read from an existing
*BaseName.densities* file and only the property calculations are
performed. Note however, that this presents many possibilities for
error, so **only use it as a last resort and be very careful with the
results**!

Take, for example, this CCSD calculation:

```mol
title: structure 1
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
2
structure (0 2)
B             0            0            0
O             0            0       1.2049
--- input ---
! CCSD def2-SVP

%base "BO-CCSD"

%mdci density unrelaxed end

*xyz 0 2
B 0 0 0
O 0 0 1.2049
*
```

This produces the files *BO-CCSD.gbw* and *BO-CCSD.densities*. To obtain
the CCSD quadrupole moment and HFCCs without repeating the whole
calculation, we can copy these two files into a new directory (highly
recommended!) and start a second job with the `!PropertiesOnly` keyword.
Note that the basename of the second job must be identical!

```mol
title: structure 2
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
2
structure (0 2)
B             0            0            0
O             0            0       1.2049
--- input ---
! CCSD def2-SVP

%base "BO-CCSD"

%mdci density unrelaxed end

*xyz 0 2
B 0 0 0
O 0 0 1.2049
*
# Everything above must be the same as in the first job!

# Request the property calculations
! PropertiesOnly 
%elprop
  quadrupole true
end
%eprnmr
  Nuclei = all B { Aiso, Adip }
  Nuclei = all O { Aiso, Adip }
end
```

