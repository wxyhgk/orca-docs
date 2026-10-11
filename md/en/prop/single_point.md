---
title: Single point energies
source: https://www.faccts.de/docs/orca/6.1/tutorials/prop/single_point.html
---

# Single point energies

Single point energies are the simplest properties one might aim to obtain, they are the lowest energy solution for the Schrödinger equation. However, there are different methods to compute those, with varying quality levels:

## Hartree-Fock (HF)

It is one of the first approximations developed [[Slater1951]](../bib.md#slater1951), which does not include the so-called *dynamic* or even *static correlation*. To run an example HF single point calculation, simply use:

```text
!HF DEF2-SVP
* xyz 0 1
O         -3.56626        1.77639        0.00000
H         -2.59626        1.77639        0.00000
H         -3.88959        1.36040       -0.81444
*
```

on your main input, and the basis DEF2-SVP will be assigned to each atom on your list. The total energy will be printed in the end of the file, e.g.:

```text
-------------------------   --------------------
FINAL SINGLE POINT ENERGY       -75.959334985643
-------------------------   --------------------
```

It is one of the oldest and simpler methods,  and it is not in general recommended if you need good energies. However, it is the basis of more complete methods such as CCSD and CASSCF.

### Unrestricted HF (UHF)

If one chooses any multiplicity other than one, say three for a triplet, an UHF calculation is performed. In this particular case, one should always check the *spin contamination* of the results.

> **Warning**
> If the expectation value of the $S^2$ (written as <S**2>) operator differs significantly from the ideal value, it might be that your system could only be treated with a multi-reference calculation    such as CASSCF.

In the case of the water above as a triplet, one gets:

```text
----------------------
UHF SPIN CONTAMINATION
----------------------

Expectation value of <S**2>     :     2.005700
Ideal value S*(S+1) for S=1.0   :     2.000000
Deviation                       :     0.005700
```

which shows a minimal deviation and is thus suitable for use here.

### Acceleration of the SCF (RIJDX and RIJCOSX)

One way to accelerate the solution of the SCF equations, necessary to compute the energy, is to use the RI option to compute the Coulomb integrals [[Neese2003]](../bib.md#neese2003). In that case, an auxiliary basis is also necessary. For the DEF2 family, the DEF2/J is set by default:

```text
!HF DEF2-SVP DEF2/J RIJDX
```

If the basis chosen has no corresponding auxiliary basis, you can include de `AUTOAUX` flag for an automatic generation of this auxiliary basis:

```text
!HF 6-31+G(d,p) AUTOAUX RIJDX
```

For an even faster speed-up, the COSX algorithm [[Helmich-Paris2021]](../bib.md#helmich-paris2021) can be used together with the RI to compute the exchange integrals efficiently.

```text
!HF DEF2-SVP DEF2/J RIJCOSX
```

## Density functional theory (DFT)

DFT energies can be obtained in a similar fashion, by choosing any functional from the ones available. For instance:

```text
!B3LYP DEF2-SVP
* xyz 0 1
O         -3.56626        1.77639        0.00000
H         -2.59626        1.77639        0.00000
H         -3.88959        1.36040       -0.81444
*
```

requests a calculation using the B3LYP [[Becke1993]](../bib.md#becke1993), [[Parr1988]](../bib.md#parr1988) functional. The calculated energy is:

```text
-------------------------   --------------------
FINAL SINGLE POINT ENERGY       -76.320253532344
-------------------------   --------------------
```

The same argument for checking spin-contamination applies here. Always have in mind that the DFT results may change depending on the functional, so one should check before using these and never compare energies from different methods!

ORCA 6 is fully compatible with functionals from [LibXC](https://libxc.gitlab.io/). For a complete list of functionals and more details, please check the [ORCA manual](https://www.faccts.de/docs/orca/6.0/manual).

> **Note**
> As standard DFT does not cover correlation effects, including London dispersion, the application of a [dispersion correction](../prop/disp.md) is generally recommended.

> **Note**
> The same approximations to accelerate the SCF, the RIJDX and RIJCOSX described above can be used with DFT. Of course, the RIJCOSX only makes sense when using a hybrid functional, where HF exchange is also calculated.

> **Important**
> The RIJDX approximation is the default for non-hybrid functionals and RIJCOSX the default for hybrid ones. To turn these of, you can use `!NORI` or `!NOCOSX`.

## MP2 perturbation theory

MP2 is a post Hartree-Fock method, which means it starts with HF as a basis and tries to include its missing *dynamic correlation*. It is implemented in ORCA in a very efficient way using the RI approximation or even in a pair-natural variant (DLPNO) that is extremely efficient [[Neese2015]](../bib.md#neese2015), both can be called using:

```text
!RI-MP2 cc-pVTZ cc-pVTZ/C
```

or

```text
!DLPNO-MP2 cc-pVTZ cc-pVTZ/C
```

Because it is a so called **correlated** method, it needs a special basis "/C" for the RI part.
These are not available for all basis sets, but can be obtain through `AUTOAUX`:

```text
!DLPNO-MP2 6-311++G(2d,2p) AUTOAUX
*XYZ 0 1
O         -3.56626        1.77639        0.00000
H         -2.59626        1.77639        0.00000
H         -3.88959        1.36040       -0.81444
*
```

You can check the correlation energy contribution as:

```text
------------------------------------------------------
 DLPNO-MP2 CORRELATION ENERGY:      -0.240752222110 Eh
------------------------------------------------------
```

and the final energy is printed as usual.

> **Warning**
> Correlated methods are typically more basis set size dependent than DFT. Choose sufficiently large basis sets to avoid large errors.

### Spin-component-scaled MP2 (SCS-MP2)

The accuracy of MP2 can be greatly improved by introduction of spin-component-scaling. The spin-component-scaling parameters `PS` of the opposite-spin and `PT` of the same-spin components can be adjusted via the `%mp2`block:

```text
!RI-SCS-MP2 cc-pVTZ cc-pVTZ/C

%mp2
  DOSCS       true
  PS          1.2    
  PT          0.333
end

*XYZFILE 0 1 structure.xyz
```

If only the `RI-SCS-MP2` keyword is used, default values for `PS=1.2` and `PT=0.333` are used.

### Orbital optimized MP2 (OO-MP2)

By making the Hylleraas functional stationary with respect to the orbital rotations one obtains the
orbital-optimized MP2 method that is implemented in ORCA. The RI-accelerated variant can be envoked by:

```text
!OO-RI-MP2 cc-pVTZ cc-pVTZ/C

*XYZFILE 0 1 structure.xyz
```

> **Warning**
> Note that every iteration of the OO-RI-MP2 method is as expensive as a single RI-MP2 relaxed density calculation!

### Regularized MP2

The regularization approach by Shee, Head-Gordon, and co-workers [[Shee2021]](../bib.md#shee2021) introduces a single-parameter, energy-gap dependent regularization term that dampens overestimated pairwise additive contributions, thus renormalizing first-order amplitudes to empirically mimic higher-order correlations. Three regularization functions are available in ORCA, $\kappa$, $\sigma$, and ${\sigma}^2$.
The most commonly used regularizer is $\kappa$ which can be controlled via the `%mp2` block:

```text
!RI-MP2 cc-pVTZ cc-pVTZ/C

%mp2
    DoRegMP2     true   # activates MP2 regularization
    RegMP2Type   0      # 0 = kappa regularizer
    RegMP2Kappa  1.1    # kappa parameter
end

*XYZFILE 0 1 structure.xyz
```

> **Note**
> No gradients are available for regularized MP2.

## Double-hybrid DFT (DH-DFT)

By replacing part of the correlation component oft a density functional by e.g. MP2 improved results can be obtained for a variety of properties. These methods are called double-hybrid functionals
[[Grimme2006]](../bib.md#grimme2006) as they include both HF exchange and MP2 correlation. Many pre-defined double hybrid functionals can be envoked via simple keyword similar to conventional functionals. An exemplary
input for the B2PLYP functional would look like:

```text
!B2PLYP DEF2-QZVPP

*XYZFILE 0 1 structure.xyz
```

Double hybrids can also benefit from RI approximations

```text
!RI-B2PLYP DEF2-QZVPP DEF2-QZVPP/C

*XYZFILE 0 1 structure.xyz
```

and even the DLPNO scheme to speed up the MP2 calculation.

```text
!DLPNO-B2PLYP DEF2-QZVPP DEF2-QZVPP/C

*XYZFILE 0 1 structure.xyz
```

A prominent double hybrid further making use of SCS-MP2 is revDSD-PBEP86-D4. This empirical functional is obtained by also incorporating the D4 dispersion correction into the fit and typically yields
very good results for thermochemistry.

```text
!revDSD-PBEP86-D4/2021 DEF2-QZVPP DEF2-QZVPP/C

*XYZFILE 0 1 structure.xyz
```

> **Note**
> Note that double hybrid functionals typically also require larger basis sets compared to conventional DFT functionals. Double hybrids can also be combined with dispersion corrections like D4.
> Functionals like revDSD-PBEP86-D4 were fit with the D4 correction and should never be used without it!

## Coupled Cluster (CC)

Coupled cluster calculations, in particular the CCSD(T) variant, are the gold standard for single point energies. However, in their usual formulation, they are also extremely costly from a computational point of view.

ORCA features a DLPNO variant that is **much** more efficient and presents almost linear scaling growth for larger systems [[Neese2016]](../bib.md#neese2016), [[Neese2013a]](../bib.md#neese2013a), [[Neese2013b]](../bib.md#neese2013b). In order to use that, simply set DLPNO-CCSD(T) in your input and choose an appropriate basis (also needs a "/C" basis or AUTOAUX)

```text
!DLPNO-CCSD(T) cc-pVTZ cc-pVTZ/C
*XYZ 0 1
O         -3.56626        1.77639        0.00000
H         -2.59626        1.77639        0.00000
H         -3.88959        1.36040       -0.81444
*
```

and the CC results are printed as:

```text
----------------------
COUPLED CLUSTER ENERGY
---------------------- 
 
E(0)                                       ...    -76.055469392
E(CORR)(strong-pairs)                      ...     -0.267934875
E(CORR)(weak-pairs)                        ...     -0.000104142
E(CORR)(corrected)                         ...     -0.268039017
E(TOT)                                     ...    -76.323508409
Singles Norm <S|S>**1/2                    ...      0.018659847
T1 diagnostic                              ...      0.006597252
```

with the final single point energy at the end:

```text
-------------------------   --------------------
FINAL SINGLE POINT ENERGY       -76.330949256808
-------------------------   --------------------
```

Please always check the T1 diagnostic value printed. A rule of thumb says, that for a value of the diagnostic of larger than 0.02 the
results are not to be trusted and the HF reference might be poor.

There are many different coupled cluster and coupled pair methods that can be use in ORCA, check the [ORCA manual](https://www.faccts.de/docs/orca/6.0/manual) for more details.

> **Note**
> The RIJCOSX algorithm can be used to significantly accelerate MP2 and CC calculations!

## Semiempirical Methods (SQM)

Various semi-empirical methods are available within ORCA. These methods are fast but lack the accuracy and robustness of more sophisticated DFT or WFT methods. Nevertheless, they are very
useful for high-throughput screening or treatment of very large systems with hundreds to thousands of of atoms. A prominent example is Grimme's GFN2-xTB extended tight-binding method [[Grimme2019]](../bib.md#grimme2019).
It can be easily invoked by:

```text
!XTB2

*XYZ 0 1
O         -3.56626        1.77639        0.00000
H         -2.59626        1.77639        0.00000
H         -3.88959        1.36040       -0.81444
*
```

> **Warning**
> The xtb methods are currently invoked through an interface to the xtb standalone program. Therefore, make sure to use xtb 6.4.0 or later to ensure full compatibilty!
