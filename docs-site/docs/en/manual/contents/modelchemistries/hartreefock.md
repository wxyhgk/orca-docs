

<a id="sec:essentialelements.hartreefock"></a>
# Hartree Fock Theory

The Hartree-Fock (HF) method[hartree1928hf, slater1929spectra, fock1930hf](../../bibliography.md) is a basic *ab-initio* quantum mechanical 
method that is used to approximate many-body electronic wavefunctions within mean field theory. 
Many post-Hartree-Fock methods like Coupled-Cluster typically make use of HF reference wavefunctions. 

A basic Hartree-Fock calculation can be invoked via the simple input keyword `!HF`

```orca
! HF
```

or via the `%method` block.

```orca
%method
   method HF    # equivalent to method HFGTO
end
```

By default, ORCA will make use of the `def2-SVP` [basis set](../essentialelements/basisset.md#sec:essentialelements.basisset) if not specified else. Hartree-Fock calculations
can be accelerated drastically by using different [RI approximations](../essentialelements/RI.md#sec:essentialelements.ri).

!!! info
    ORCA provides several choices of wavefunction types like resticted (RHF), unresticted (UHF), or unrestricted open-shell HF (ROKS).
    These options are documented in [modelchemistries.hftype](hftype.md#sec:modelchemistries.hftype). HF is also an integral part of [hybrid-](DensityFunctionalTheory.md#sec:modelchemistries.dft.hybriddft) and [double-hybrid](DensityFunctionalTheory.md#sec:modelchemistries.dft.doublehybriddft) DFT.

!!! tip
    Grimme and co-workers developed a low-cost method based on HF called [HF-3c](3cmethods.md#sec:modelchemistries.3cmethods.hf3c) that can be employed for very large systems.
    Some HF-based [semi-empirical methods](semiempirical.md#sec:modelchemistries.semiempirical) like AM1 or PM3 are also available. 
