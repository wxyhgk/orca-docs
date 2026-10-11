```{index} MR-EOM-CC
```

(sec:modelchemistries.mreom)=
# Multireference Equation of Motion Coupled-Cluster (MR-EOM-CC)

The Multireference Equation of Motion Coupled-Cluster (MR-EOM-CC ) methodology {cite}`datta2011pICMRCC,datta2012mreom,demel2013mreom,nooijen2014mreom,huntington2015mreom_orb_select,huntington2015mreom_bench` has been implemented in ORCA. The strength of the MR-EOM-CC  methodology lies in its ability to calculate many excited states from a single state-averaged CASSCF solution, for which only a single set of amplitudes needs to be solved and the final transformed Hamiltonian is diagonalized over a small manifold of excited states only through an uncontracted MRCI problem. Hence, a given MR-EOM-CC  calculation involves three steps, performed by three separate modules in ORCA :

1.  a state-averaged CASSCF calculation (CASSCF module),

2.  the solution of amplitude equations and the calculation of the
    elements of the similarity transformed Hamiltonians (MDCI module),

3.  and the uncontracted MRCI diagonalization of the final similarity
    transformed Hamiltonian (MRCI module).

The current implementation allows for MR-EOM-T|T$^{\dagger}$-h-v, MR-EOM-T|T$^{\dagger}$|SXD-h-v and MR-EOM-T|T$^{\dagger}$|SXD|U-h-v calculations. A more detailed description of these methods and the available input parameters will be given in Sec. {numref}`sec:modelchemistries.mreom.details`. We also note that the theoretical details underlying these methods can be found in Ref. {cite}`huntington2015mreom_bench`. In Sec. {numref}`sec:modelchemistries.mreom.calc.sacas`, we will discuss a strategy for the selection of the state-averaged CAS and other steps for setting up an MR-EOM-CC  calculation in more detail. Furthermore, we will discuss how spin-orbit coupling effects can be included in MR-EOM-CC  calculations, a projection scheme to aid with convergence difficulties in the iteration of the $T$ amplitude equations, an orbital selection scheme to reduce the size of the inactive core and virtual subspaces in the calculation of excitation energies and a strategy for obtaining nearly size-consistent results in MR-EOM-CC The purpose of this section is simply to provide a simple example which illustrates the most basic usage of the MR-EOM-CC  implementation in ORCA.

(sec:modelchemistries.mreom.calc)=
## A Simple MR-EOM-CC  Calculation

Let us consider an MR-EOM-T|T$^{\dagger}$|SXD|U-h-v calculation on formaldehyde. An MR-EOM-T|T$^{\dagger}$|SXD|U-h-v calculation is specified via the `MR-EOM` keyword along with the specification of a state-averaged CASSCF calculation (i.e. CASSCF(nel, norb) calculation with the number of roots of each multiplicity to be included in the state-averaging for the reference state) and the number of desired roots in each multiplicity block for the final MRCI diagonalization. We note that the CASSCF module is described in section {numref}`sec:modelchemistries.casscf` and that a description of the MRCI module is given in section {numref}`sec:modelchemistries.mrci`. Here, we have a state-averaged CAS(6,4) calculation, comprised of 3 singlets and 3 triplets and we request 6 singlet roots and 6 triplet roots in our final MRCI diagonalization (i.e. the roots to be computed in the MR-EOM-T|T$^{\dagger}$|SXD|U-h-v calculation): 

```{literalinclude} ../../orca_working_input/C05S10_195.inp
:language: orca
```

One can alternatively perform an MR-EOM-T|T$^{\dagger}$-h-v or
MR-EOM-T|T$^{\dagger}$|SXD-h-v calculation by replacing the `MR-EOM` keyword,
in the first line of the input above, by `MR-EOM-T|Td` or
`MR-EOM-T|Td|SXD`, respectively. Namely, replacing the first line of the
input above with

```orca
!MR-EOM-T|Td def2-TZVP VeryTightSCF
```

runs the MR-EOM-T|T$^{\dagger}$-h-v calculation, while

```orca
!MR-EOM-T|Td|SXD def2-TZVP VeryTightSCF
```

runs the MR-EOM-T|T$^{\dagger}$|SXD-h-v calculation.

The final MRCI diagonalization manifold includes 2h1p, 1h1p, 2h, 1h and
1p excitations in MR-EOM-T|T$^{\dagger}$-h-v calculations, 2h, 1p and 1h
excitations in MR-EOM-T|T$^{\dagger}$|SXD-h-v calculations and 1h and 1p
excitations in MR-EOM-T|T$^{\dagger}$|SXD|U-h-v calculations. Note that in the
`%mdci` block, we have set the convergence tolerance (`STol`) for the
residual equations for the amplitudes to $10^{-7}$, as this default
value is overwritten with the usage of the `TightSCF`, `VeryTightSCF`,
etc. keywords. It is always important to inspect the values of the
largest $T$, $S$ (here, we use $S$ to denote the entire set of $S$, $X$
and $D$ amplitudes) and $U$ amplitudes. If there are amplitudes that are
large (absolute values $> 0.15$), the calculated results should be
regarded with suspicion. For the above calculation, we obtain:

```orca
--------------------
LARGEST T AMPLITUDES
--------------------
   8-> 13   8-> 13       0.060331
   4-> 17   4-> 17       0.029905
   8->  9   8->  9       0.028160
   8-> 16   8-> 16       0.027266
   6-> 20   6-> 20       0.025885
   8-> 21   8-> 21       0.025308
   4-> 16   4-> 16       0.024803
   8-> 12   8-> 12       0.023915
   5-> 18   5-> 18       0.023553
   8-> 23   8-> 23       0.023384
   3-> 16   3-> 16       0.023182
   7-> 19   7-> 19       0.023043
   8-> 13   4-> 11       0.022010
   3-> 19   3-> 19       0.021987
   8-> 16   8->  9       0.021230
   8->  9   8-> 16       0.021230
```

for the $T$ amplitudes,

```orca
--------------------
LARGEST S AMPLITUDES
--------------------
   4->  8   8-> 11       0.074048
   3->  8   8->  9       0.064886
   4->  5   5-> 11       0.045479
   3->  8   8-> 16       0.042657
   4->  7   7-> 11       0.042598
   4->  5   5-> 17       0.042076
   4->  5   8-> 11       0.039958
   4->  8   8-> 17       0.037532
   3->  5   8->  9       0.035907
   4->  7   7-> 17       0.035767
   2->  6   6-> 19       0.034148
   3->  5   5-> 10       0.033339
   2->  6   6-> 10       0.032691
   4->  6   6-> 11       0.032181
   8->  8   3-> 16       0.031775
   2->  7   7-> 22       0.031238
```

for the $S$ amplitudes, and

```orca
--------------------
LARGEST U AMPLITUDES
--------------------
   3->  8   3->  8       0.026128
   3->  8   3->  5       0.007683
   2->  8   2->  8       0.006182
   3->  8   2->  5       0.006154
   2->  8   3->  5       0.004954
   3->  5   3->  5       0.004677
   4->  8   4->  8       0.003989
   3->  8   2->  8       0.002040
   2->  8   3->  8       0.002040
   2->  8   2->  5       0.001818
   4->  8   4->  5       0.001173
   2->  5   2->  5       0.001107
   4->  5   4->  5       0.000714
   3->  7   3->  7       0.000607
   3->  6   3->  6       0.000521
   2->  5   3->  5       0.000365
```

for the $U$ amplitudes. Hence, one can see that there are no unusually
large amplitudes for this calculation. **We note that there can be
convergence issues with the $\boldsymbol{T}$ amplitude iterations and
that in such cases, the flag:**

```orca
DoSingularPT true
```

**should be added to the `%mdci` block.** The convergence issues are
caused by the presence of nearly singular $T_2$ amplitudes and setting
the `DoSingularPT` flag to `true` activates a procedure which projects
out the offending amplitudes (in each iteration) and replaces them by
suitable perturbative amplitudes. For more information, see the examples
in section {numref}`sec:modelchemistries.mreom.singularpt`.

After the computation of the amplitudes and the elements of the
similarity transformed Hamiltonians, within the MDCI module, the
calculation enters the MRCI module. For a complete, step by step
description of the output of an MRCI calculation, we refer the reader to
the example described in section {numref}`sec:modelchemistries.mrci.example`. Let us first focus on the results
for the singlet states (`CI-BLOCK 1`). Following the convergence of the
Davidson diagonalization (default) or DIIS procedure, the following
results of the MRCI calculation for the singlet states are printed:

```orca
----------
CI-RESULTS
----------

The threshold for printing is  0.30 percent
The weights of configurations will be printed. The weights are summed over
all CSFs that belong to a given configuration before printing

STATE   0:  Energy=   -114.321368425 Eh RefWeight=  0.9781  0.00 eV      0.0 cm**-1
      0.0137  : h---h---[0222]
      0.0756  : h---h---[1221]
      0.8879  : h---h---[2220]
STATE   1:  Energy=   -114.176866027 Eh RefWeight=  0.9765  3.93 eV  31714.6 cm**-1
      0.0039  : h---h---[1122]
      0.9726  : h---h---[2121]
      0.0071  : h---h  4[1222]
      0.0085  : h---h  4[2221]
STATE   2:  Energy=   -113.988050555 Eh RefWeight=  0.9774  9.07 eV  73154.8 cm**-1
      0.0044  : h---h---[1212]
      0.9730  : h---h---[2211]
      0.0063  : h---h  3[1222]
      0.0041  : h---h  3[2221]
STATE   3:  Energy=   -113.963862283 Eh RefWeight=  0.8810  9.73 eV  78463.5 cm**-1
      0.7459  : h---h---[1221]
      0.0807  : h---h---[2022]
      0.0533  : h---h---[2220]
      0.0228  : h---h  4[2122]
      0.0034  : h---h---[1220]p13
      0.0072  : h---h---[1220]p18
      0.0236  : h---h---[2120]p11
      0.0148  : h---h---[2120]p14
      0.0069  : h---h---[2120]p17
      0.0056  : h---h---[2120]p20
      0.0098  : h---h---[2210]p19
STATE   4:  Energy=   -113.931144468 Eh RefWeight=  0.0003 10.62 eV  85644.3 cm**-1
      0.0045  : h---h---[0122]p9
      0.0089  : h---h---[1121]p9
      0.9333  : h---h---[2120]p9
      0.0243  : h---h---[2120]p10
      0.0080  : h---h---[2120]p12
      0.0113  : h---h---[2120]p16
STATE   5:  Energy=   -113.929056780 Eh RefWeight=  0.6857 10.68 eV  86102.5 cm**-1
      0.0061  : h---h---[0222]
      0.0918  : h---h---[1221]
      0.5784  : h---h---[2022]
      0.0048  : h---h---[2202]
      0.0047  : h---h---[2220]
      0.2905  : h---h  4[2122]
      0.0045  : h---h---[2021]p13
```

For each state, the total energy is given in $E_\text{h}$; the weight of
the reference configurations (`RefWeight`) in the given state is
provided, and the energy differences from the lowest lying state are
given in eV and cm$^{-1}$. Also, in each case, the weights and a
description of the configurations which contribute most strongly to the
given state are also provided. See section {numref}`sec:modelchemistries.mrci.example` for a discussion of the notation that is used for the description of the various configurations. To avoid
confusion, we note that in the literature concerning the MR-EOM
methodology
{cite}`datta2012mreom,demel2013mreom,nooijen2014mreom,huntington2015mreom_orb_select,huntington2015mreom_bench,liu2015mreom_bench,liu2015mreom_bench_SOC`,
the term "%active" is used to denote the reference weight multiplied by
100%. In general, `RefWeight ` should be $> 0.9$, such that the states
are dominated by reference space configurations. This criterion is
satisfied for the first three states and the reference weight of the
fourth state is sufficiently close to $0.9$. **However, the reference
weights of the two higher lying states (especially state 4) are too
small and these states should be discarded as the resulting energies
will be inaccurate (i.e. states with significant contributions from
configurations outside the reference space cannot be treated
accurately)** .

In the case of the triplet states (`CI-BLOCK 2`), we obtain the
following results:

```orca
----------
CI-RESULTS
----------

The threshold for printing is  0.30 percent
The weights of configurations will be printed. The weights are summed over
all CSFs that belong to a given configuration before printing

STATE   0:  Energy=   -114.190840989 Eh RefWeight=  0.9693  0.00 eV      0.0 cm**-1
      0.9691  : h---h---[2121]
      0.0079  : h---h  4[1222]
      0.0115  : h---h  4[2221]
STATE   1:  Energy=   -114.106733017 Eh RefWeight=  0.9941  2.29 eV  18459.6 cm**-1
      0.9941  : h---h---[1221]
STATE   2:  Energy=   -114.015150051 Eh RefWeight=  0.9787  4.78 eV  38559.7 cm**-1
      0.9786  : h---h---[2211]
      0.0050  : h---h  3[1222]
STATE   3:  Energy=   -113.939299674 Eh RefWeight=  0.0006  6.84 eV  55206.9 cm**-1
      0.0044  : h---h---[0122]p9
      0.0084  : h---h---[1121]p9
      0.9419  : h---h---[2120]p9
      0.0131  : h---h---[2120]p10
      0.0043  : h---h---[2120]p12
      0.0173  : h---h---[2120]p16
STATE   4:  Energy=   -113.925571130 Eh RefWeight=  0.4017  7.22 eV  58220.0 cm**-1
      0.3863  : h---h---[1122]
      0.0154  : h---h---[2121]
      0.1722  : h---h  4[1222]
      0.4098  : h---h  4[2221]
      0.0045  : h---h---[2120]p13
STATE   5:  Energy=   -113.910479339 Eh RefWeight=  0.0009  7.63 eV  61532.3 cm**-1
      0.0088  : h---h---[0122]p10
      0.0030  : h---h---[1121]p10
      0.0120  : h---h---[2120]p9
      0.9408  : h---h---[2120]p10
      0.0106  : h---h---[2120]p16
      0.0112  : h---h---[2120]p19
```

Here, we see that the first three states have reference weights which
are $> 0.9$, while the reference weights of the final three states are
well below that threshold. Hence, the latter three states should be
discarded from any meaningful analysis.

Following the printing of the CI results for the final CI block, the
states are ordered according to increasing energy and the vertical
transition energies are printed:

```orca
-------------------
TRANSITION ENERGIES
-------------------

The lowest energy is   -114.321368425 Eh

State Mult Irrep Root Block    mEh          eV      1/cm
  0    1    -1    0    0      0.000      0.000       0.0
  1    3    -1    0    1    130.527      3.552   28647.5
  2    1    -1    1    0    144.502      3.932   31714.6
  3    3    -1    1    1    214.635      5.841   47107.0
  4    3    -1    2    1    306.218      8.333   67207.2
  5    1    -1    2    0    333.318      9.070   73154.8
  6    1    -1    3    0    357.506      9.728   78463.5
  7    3    -1    3    1    382.069     10.397   83854.4
  8    1    -1    4    0    390.224     10.619   85644.3
  9    1    -1    5    0    392.312     10.675   86102.5
 10    3    -1    4    1    395.797     10.770   86867.5
 11    3    -1    5    1    410.889     11.181   90179.7
```

Furthermore, following the generation of the (approximate) densities,
the absorption and CD spectra are printed:

```orca
==========================================
MR-EOM-CC  Non Relativistic Properties
==========================================

----------------------------------------------------------------------------------------------------
                     ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS    
----------------------------------------------------------------------------------------------------
     Transition      Energy     Energy  Wavelength fosc(D2)      D2        DX        DY        DZ   
                      (eV)      (cm-1)    (nm)                 (au**2)    (au)      (au)      (au)  
----------------------------------------------------------------------------------------------------
  0-1A  ->  1-1A    3.932110   31714.6   315.3   0.000000000   0.00000  -0.00000  -0.00000   0.00000
  0-1A  ->  2-1A    9.070040   73154.8   136.7   0.002137450   0.00962   0.09808  -0.00000  -0.00000
  0-1A  ->  3-1A    9.728237   78463.5   127.4   0.157495738   0.66081  -0.00000   0.00000  -0.81290
  0-1A  ->  4-1A   10.618534   85644.3   116.8   0.025353906   0.09746  -0.00000  -0.31218  -0.00000
  0-1A  ->  5-1A   10.675343   86102.5   116.1   0.024673667   0.09434  -0.00000  -0.00000   0.30715

------------------------------------------------------------------------------------------
                     CD SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS    
------------------------------------------------------------------------------------------
     Transition      Energy     Energy  Wavelength    R        MX        MY        MZ   
                      (eV)      (cm-1)    (nm)   (1e40*cgs)   (au)      (au)      (au)  
------------------------------------------------------------------------------------------
  0-1A  ->  1-1A    3.932110   31714.6   315.3   -0.00000   0.00000   0.00000   0.56273
  0-1A  ->  2-1A    9.070040   73154.8   136.7   -0.00000   0.00000  -0.74486   0.00000
  0-1A  ->  3-1A    9.728237   78463.5   127.4   -0.00000  -0.00000  -0.00000  -0.00000
  0-1A  ->  4-1A   10.618534   85644.3   116.8    0.00000   0.35898   0.00000  -0.00000
  0-1A  ->  5-1A   10.675343   86102.5   116.1    0.00000   0.00000  -0.00000  -0.00000
```

:::{Warning}

-   It is important to note that the transition moments and oscillator
    strengths (and state dipole moments) have been blindly computed by
    the MRCI module and currently, no effort has been made to include
    the effects of the various similarity transformations in the
    evaluation of these quantities. Hence these quantities are only
    approximate and should only be used as a qualitative aid to
    determine which states are dipole allowed or forbidden. Furthermore,
    since the calculated densities are approximate, so are the results
    of the population analysis that are printed before the absorption
    and CD spectra.

-   While both the CASSCF and MRCI modules can make use of spatial
    point-group symmetry to some extent, the MR-EOM-CC  implementation is
    currently limited to calculations in $C_1$ symmetry.
:::

(sec:modelchemistries.mreom.capability)=
## Capabilities

The MR-EOM-CC  methodology can be used to calculate a desired number of
states for both closed- and open-shell systems from a single
state-averaged CASSCF solution. Currently, the approach is limited to
serial calculations and to smaller systems in smaller active spaces. One
should be aware that in the most cost-effective
MR-EOM-T|T$^{\dagger}$|SXD|U-h-v approach (i.e. the smallest diagonalization
manifold), an MRCI diagonalization is performed over all 1h and 1p
excited configurations out of the CAS, which will inevitably limit the
size of the initial CAS which can be used. We have also implemented an
orbital selection scheme which can be used to reduce the size of the
inactive core and virtual subspaces in the calculation of excitation
energies, and this can be employed to extend the applicability of the
approach to larger systems. The current implementation can also be used
in conjunction with the spin-orbit coupling submodule
({ref}`sec:modelchemistries.mrci.soc`) of the MRCI module to calculate
spin-orbit coupling effects in MR-EOM-CC  calculations to first order. These
and other features of the current implementation will be discussed in
{ref}`sec:modelchemistries.mreom.details`.

(sec:modelchemistries.mreom.perturbative)=
## Perturbative MR-EOM-CCPT

The MR-EOM-CC  family of methods now also features an almost fully
perturbative approach called MR-EOM-T {cite}`Lechner2021`. This method shares
the features of the MR-EOM-CC  parent method while using non-iterative
perturbative estimates for the $\hat T$ and $\hat S,\hat X,\hat D$
amplitudes. This slightly reduces the accuracy compared to iterative
MR-EOM-CC  while reducing runtime. Furthermore, convergence issues due to
nearly singular $\hat T$ and $\hat S,\hat X,\hat D$ amplitudes cannot
occur anymore.

This method can be invoked by adding the keyword `DoMREOM_MRPT True` to
the `%mdci` block.

(sec:modelchemistries.mreom.details)=
## Details on the Multireference Equation of Motion Coupled-Cluster (MR-EOM-CC ) Theory

In analogy with single reference EOM-CC and STEOM-CC (see sections {numref}`sec:spectroscopyproperties.eom` and {numref}`sec:spectroscopyproperties.steom`), Multireference Equation of Motion Coupled-Cluster (MR-EOM-CC ) theory {cite}`datta2011pICMRCC,datta2012mreom,demel2013mreom,nooijen2014mreom,huntington2015mreom_orb_select,huntington2015mreom_bench` can be viewed a transform and diagonalize approach to molecular electronic structure theory. An MR-EOM-CC  calculation involves a single state-averaged CASSCF calculation, incorporating a few low-lying states and the solution of a single set of cluster amplitudes, which define a sequence of similarity-transformed Hamiltonians. The ultimate goal of these many-body transformations is to effectively decouple the CAS configurations from important excited configurations (e.g., 2p2h, 2p1h, 1p1h, etc.) which comprise the first-order interacting space. Through the definition of suitable cluster operators, in each of the transformations, most of these excitations can be included in an internally contracted fashion. Hence, the resulting final transformed Hamiltonian can be diagonalized over a small subspace of the original first-order interacting space to gain access to many electronic states. As discussed in section {numref}`sec:modelchemistries.mreom`, the MR-EOM-CC  implementation in ORCA therefore makes use of the CASSCF module (to obtain the state-averaged CASSCF reference), the MDCI module for the solution of the amplitude equations and the calculation of the elements of the various similarity transformed Hamiltonians and the MRCI module for the diagonalization of the final transformed Hamiltonian. Some desirable features of this methodology are: 

-   Many states can be obtained through the diagonalization of a
    similarity transformed Hamiltonian over a compact diagonalization
    manifold (e.g. the final diagonalization space in
    MR-EOM-T|T$^\dagger$|SXD|U only includes the CAS configurations and 1h and
    1p configurations).

-   Only a single state-averaged CASSCF calculation and the solution of
    a single set of amplitudes is required to define the final
    similarity transformed Hamiltonian and the results are typically
    quite insensitive to the precise definition of the CAS (only a few
    low-lying multiplets need to be included in the state-averaging)

-   The MR-EOM-CC  approach is rigorously invariant to rotations of the
    orbitals in the inactive, active and virtual subspaces, and it
    preserves both spin and spatial symmetry.

(table:mreom.trans)=
:::{flat-table} The details of the various MR-EOM-CC  transformations that are considered in the ORCA implementation of MR-EOM-CC. The equations for the operator components and the residual equations which determine the corresponding amplitudes also appear in the Table. Note that we use the usual (Einstein) convention that repeated indices are summed over.
:header-rows: 1
:class: footnotesize

* - Name
  - Transformation
  - Operators
  - Operator Components
  - Residual Equation

* - {rspan}`1` T
  - $\widehat{\xbar{H}}=e^{-\widehat{T} }\widehat{H}e^{\widehat{T} }$
  - $\widehat{T}=\widehat{T}_1+\widehat{T}_2$
  - $\widehat{T}_1=t_i^a\widehat{E}_i^a$
  - $R^{a}_i=\sum_{\mathfrak{m} }w_{\mathfrak{m} }\left\langle\Phi_{\mathfrak{m} }\right\vert \widehat{E}^{i}_{a}\widehat{\xbar{H}}\left\vert\Phi_{\mathfrak{m} }\right\rangle$
* - $=\xbar{h}_0+\xbar{h}^p_q\big\{\widehat{E}^{p}_{q}\big\}+\xbar{h}^{pq}_{rs}\big\{\widehat{E}^{pq}_{rs}\big\}+\ldots$
  - 
  - $\widehat{T}_2=\frac{1}{2}t_{ij}^{ab}\widehat{E}_{ij}^{ab}$
  - $R_{ij}^{ab}=\xbar{h}^{ab}_{ij}$
* - {rspan}`1` T$^{\dagger}$
  - $\widehat{\xbar{H}}_2e^{-\widehat{T}^{\dagger} }$
  - $\widehat{T}^{\dagger}=\widehat{T}^{\dagger}_1+\widehat{T}^{\dagger}_2$
  - $\widehat{T}^{\dagger}_1=t_a^i\widehat{E}_a^i$
  - None (*i.e.* set $t^{i}_{a}\approx t^a_i$)
* - $=\widetilde{h}_0+\widetilde{h}\,^{p}_{q}\big\{\widehat{E}^{p}_{q}\big\}+\widetilde{h}\,^{pq}_{rs}\big\{\widehat{E}^{pq}_{rs}\big\}+\ldots$
  -
  - $\widehat{T}^{\dagger}_2=\frac{1}{2}t_{ab}^{ij}\widehat{E}_{ab}^{ij}$
  - None (*i.e.* set $t^{ij}_{ab}\approx t^{ab}_{ij}$)
* - SXD
  - $\widehat{\xbar{F}}=\big\{e^{\widehat{S}+\widehat{X}+\widehat{D} }\big\}^{-1}\widehat{\mathcal{H} }_2\big\{e^{\widehat{S}+\widehat{X}+\widehat{D} }\big\}$
  - $\widehat{S}=\widehat{S}_2$
  - $\widehat{S}_2=s_{i'j'}^{aw}\widehat{E}_{i'j'}^{aw}$
  - $R^{aw}_{i'j'}=\xbar{f}\,^{aw}_{i'j'}$
* - 
  - $=\xbar{f}_0+\xbar{f}\,^{p}_{q}\big\{\widehat{E}^{p}_{q}\big\}+\xbar{f}\,^{pq}_{rs}\big\{\widehat{E}^{pq}_{rs}\big\}+\ldots$
  - $\widehat{X}=\widehat{X}_2$
  - $\widehat{X}_2=x_{i'x}^{aw}\widehat{E}_{i'x}^{aw}$
  - $R^{aw}_{i'x}=\xbar{f},^{aw}_{i'x}$
* - 
  - 
  - $\widehat{D}=\widehat{D}_2$
  - $\widehat{D}_2=d_{xi'}^{aw}\widehat{E}_{xi'}^{aw}$
  - $R^{aw}_{xi'}=\xbar{f}\,^{aw}_{xi'}$
* - U
  - $\widehat{G}=e^{-\widehat{U} }\widehat{\xbar{F}}_2e^{\widehat{U} }$
  - $\widehat{U}=\widehat{U}_2$
  - $\widehat{U}_2=u_{i'j'}^{wx}\widehat{E}_{i'j'}^{wx}$
  - $R^{wx}_{i'j'}=g^{wx}_{i'j'}$
* - 
  - $=g_0+g^{p}_{q}\big\{\widehat{E}^{p}_{q}\big\}+g^{pq}_{rs}\big\{\widehat{E}^{pq}_{rs}\big\}+\ldots$
  -
  -
  -
:::

As the details concerning the MR-EOM-CC  methodology are rather involved, we
refer the interested reader to
Refs. {cite}`datta2011pICMRCC,datta2012mreom,demel2013mreom,nooijen2014mreom,huntington2015mreom_orb_select,huntington2015mreom_bench`
for a more detailed discussion. Note that the details concerning the
implementation of MR-EOM-CC  in ORCA can be found in
Refs. {cite}`huntington2015mreom_orb_select` and
{cite}`huntington2015mreom_bench`. In the following discussion, we note that
general spatial orbitals $p,q,r,s$, which comprise the molecular orbital
basis, are partitioned into (doubly occupied) inactive core orbitals
$i',j',k',l'$, occupied orbitals $i,j,k,l$ (i.e. the union of the
inactive core and active orbital subspaces), active orbitals $w,x,y,z$
and virtual orbitals $a,b,c,d$. In general, the many-body similarity
transformations assume the general form

$$\begin{aligned}
\widehat{G}=\big\{e^{\widehat{Y} }\big\}^{-1}\widehat{\xbar{H}}_{2}\big\{e^{\widehat{Y} }\big\}=g_0+\sum_{p,q}g^{p}_{q}\big\{\widehat{E}^{p}_{q}\big\}+\sum_{p,q,r,s}g^{pq}_{rs}\big\{\widehat{E}^{pq}_{rs}\big\}+\ldots,\end{aligned}$$

in which $\widehat{Y}$ is a cluster operator and $\widehat{\xbar{H}}_2$ is 
the bare Hamiltonian or a similarity transformed Hamiltonian
truncated up to two-body operators. The braces indicate
Kutzelnigg-Mukherjee normal ordering
{cite}`mukherjee1997normalorder,kutzelnigg1997normalorder`, which is used
extensively in the definition of the MR-EOM-CC  formalism. The various
transformations which need to be considered in the ORCA implementation
of MR-EOM-CC  are summarized in {numref}`table:mreom.trans`. The table also includes the expressions
for the operator components of the various internally contracted cluster
operators and the residual equations that must be solved for the various
amplitudes. Note that the residual equations are typically of the
many-body type (i.e. obtained by setting the corresponding elements of
the similarity transformed Hamiltonian to zero). The only exception is
the residual equation which defines the $t_i^a$ amplitudes, which is a
projected equation of the form

$$R_i^a=\sum_{\mathfrak{m} }w_{\mathfrak{m} }\big\langle\Phi_{\mathfrak{m} }\vert \widehat{E}^{i}_a\widehat{H}\vert\Phi_{\mathfrak{m} }\big\rangle.$$

Here, $\vert \Phi_{\mathfrak{m} }\big\rangle$ is the
$\mathfrak{m}^{\text{th} }$ state included in the state averaged CAS,
with weight $w_{\mathfrak{m} }$. The reason the equation for the singles
is of the projected form is that it satisfies the Brillouin theorem
(i.e. the first order singles vanish for all $i$ and $a$), whereas the
corresponding many-body equation ($\bar{h}_i^a=0)$ does not.

(table:mreom.details)=
:::{table} Details of the three MR-EOM-CC  approaches implemented in ORCA
|          Method           |  Input Keyword  |                                        Operators                                        |  Diagonalization Manifold   |
|:-------------------------:|:---------------:|:---------------------------------------------------------------------------------------:|:---------------------------:|
|   MR-EOM-T\|T$^\dagger$-h-v   |  `MR-EOM-T\|Td`   |                            $\widehat{T}$; $\widehat{T}^\dagger$                            | CAS, 2h1p, 1h1p, 2h, 1h, 1p |
| MR-EOM-T\|T$^\dagger$\|SXD-h-v  | `MR-EOM-T\|Td\|SXD` |        $\widehat{T}$; $\widehat{T}^\dagger$; $\widehat{S}+\widehat{X}+\widehat{D}$         |       CAS, 2h, 1h, 1p       |
| MR-EOM-T\|T$^\dagger$\|SXD\|U-h-v |    `MR-EOM`     | $\widehat{T}$; $\widehat{T}^\dagger$; $\widehat{S}+\widehat{X}+\widehat{D}$; $\widehat{U}$ |         CAS, 1h, 1p         |

:::

Note that there are three different MR-EOM-CC  approaches which have been
implemented in ORCA. Namely, the current implementation allows for
MR-EOM-T|T$^\dagger$-h-v, MR-EOM-T|T$^\dagger$|SXD-h-v and
MR-EOM-T|T$^\dagger$|SXD|U-h-v calculations. At this point it is useful to
discuss the naming convention used for these approaches. We use a
vertical line to separate each transformation involved in the sequence
of transformations defining the given MR-EOM-CC  approach. For example,
T|T$^\dagger$|SXD indicates that a T transformation, is followed by a
T$^\dagger$ transformation, which is then followed by an SXD
transformation. The h-v indicates that the elements of the transformed
Hamiltonian have been hermitized (h) and vertex symmetrized (v) before
entering the MRCI diagonalization (see Ref. {cite}`huntington2015mreom_bench`
for more information). Essentially, this means that the full eightfold
symmetry of the two-electron integrals (and hermiticity of the one-body
elements) have been enforced upon the elements of the transformed
Hamiltonian. The details of the three MR-EOM-CC  approaches are summarized
in Table {numref}`table:mreom.details`. This table includes the keyword (in
the first line of input) used to initiate the calculation in ORCA, the
various operators involved, and the configurations included in the final
diagonalization manifold. One can clearly see that the
MR-EOM-T|T$^\dagger$|SXD|U-h-v approach is the most cost effective, as it only
includes the 1h and 1p configurations, beyond the CAS, in the final
diagonalization manifold.

Some `%mdci` keywords which are important for controlling MR-EOM-CC
calculations are (i.e. default values are given here):

```orca
%mdci
  STol              1e-7        #Convergence Tolerance on Residual Equations
  MaxIter           100         #Maximum Number of Iterations
  DoSingularPT      false       #Activate the Singular PT/Projection Procedure
  SingularPTThresh  0.01        #Threshold for the Singular PT/Projection
                                #Procedure
  PrintOrbSelect    false       #Print the Eigenvalues of the Orbital Selection
                                #Densities (and R_core and R_virt values)
                                #and Terminate the Calculation
  CoreThresh        0.0         #Core Orbital Selection Threshold
  VirtualThresh     1.0         #Virtual Orbital Selection Threshold
end
```

As discussed below, the orbital selection scheme is activated by adding
`!OrbitalSelection` to the simple input line. Keywords that are specific
to the CASSCF and MRCI modules are discussed in
sections {numref}`sec:modelchemistries.casscf`
and {numref}`sec:modelchemistries.mrci`, respectively. We note that in
MR-EOM-T|T$^\dagger$-h-v and MR-EOM-T|T$^\dagger$|SXD-h-v calculations, it is
possible to override the default excitation classes in the final MRCI
diagonalization. This is done by specifying `excitations none` and then
explicitly setting the excitation flags within a given multiplicity
block. For example, if we wanted to have 1h, 1p, 1h1p, 2h and 2h1p
excitations in the final diagonalization manifold, we would specify
(i.e. here we have requested 6 singlets and have a CAS(6,4) reference):

```orca
%mrci
    newblock 1 *
        excitations none
        Flags[is]   1
        Flags[sa]   1
        Flags[ia]   1
        Flags[ijss] 1
        Flags[ijsa] 1
        nroots      6
        refs
            cas(6,4)
        end
    end
end
```

(sec:modelchemistries.mreom.details.calc)=
### The Steps Required to Run an MR-EOM-CC  Calculation

To illustrate the various steps required in a typical MR-EOM-CC calculation, we will consider the calculation of the excitation energies of the neutral Fe atom at the MR-EOM-T|T$^{\dagger}$|SXD|U-h-v level of theory.

(sec:modelchemistries.mreom.calc.sacas)=
#### State-Averaged CASSCF Calculation

Evidently, the first step is to determine a suitable state-averaged
CASSCF reference for the subsequent MR-EOM-CC  calculation. In choosing the
state-averaged CAS for an MR-EOM-CC  calculation, we typically include a few
of the low-lying multiplets that have the same character as the (much
larger number of) states that we wish to compute in the final MR-EOM
calculation. For the neutral Fe atom, we typically have electronic
states which have either 4s$^2$3d$^6$ character or
4s$^1$3d$^7$ character. From the NIST atomic spectra
database {cite}`nist_atomic_spectra,nave1994Fe`, we find that the lowest
lying $^5$D multiplet is of 4s$^2$3d$^6$ character and
the higher lying $^5$F multiplet is of 4s$^1$3d$^7$
character. Hence, we can set up a state-averaged CASSCF(8,6) calculation
(i.e. 8 electrons in 6 orbitals (4s and 3d)) which includes the $^5$D
and $^5$F states and choose the weights such that the average occupation
of the 4s orbital is 1.5. As discussed in Ref. {cite}`liu2015mreom_bench`,
this is done to avoid a preference toward either of the 4s
configurations in the state-averaging. We will run the state-averaged
CASSCF calculation, making use of the second order DKH (see
{ref}`sec:essentialelements.relativistic.dkh`) method for the inclusion of
relativistic effects in a Def2-TZVPP basis (i.e. the DKH-Def2-TZVPP
relativistically recontracted basis, listed in section
{numref}`sec:essentialelements.basisset`). The input file for the
state-averaged CASSCF(8,6) calculation takes the form:

```{literalinclude} ../../orca_working_input/C06S22_485.inp
:language: orca
```

Here, we have requested 12 quintet states (the lowest lying $^5$D and
$^5$F multiplets) and we have chosen the weights to be 0.7 for the five
$^5$D states and 0.5 for the seven $^5$F states, such that the overall
occupation of the 4s orbital will be 1.5. Once the calculation has
converged, it is important to inspect the results printed in the final
macro-iteration of the CASSCF calculation (macro-iteration 8 in this
case). In this case, we have:

```orca
MACRO-ITERATION   8:
   --- Inactive Energy E0 = -1249.82392764 Eh
   --- All densities will be recomputed
CI-ITERATION   0:
 -1271.258899450   0.000000000001 (    0.00)
 -1271.258899450   0.000000000001
 -1271.258899450   0.000000000001
 -1271.258899450   0.000000000001
 -1271.258899450   0.000000000001
 -1271.186288591   0.000000000001
 -1271.186288591   0.000000000001
 -1271.186288591   0.000000000002
 -1271.186288591   0.000000000001
 -1271.186288591   0.000000000001
 -1271.186288591   0.000000000001
 -1271.186288591   0.000000000001
   CI-PROBLEM SOLVED
   DENSITIES MADE
   E(CAS)= -1271.222594021 Eh DE=   -1.591616e-12
   --- Energy gap subspaces: Ext-Act = 0.276   Act-Int = 2.469
   N(occ)=  1.50000 1.30000 1.30000 1.30000 1.30000 1.30000
   ||g|| =     4.669702e-05 Max(G)=    1.104493e-05 Rot=68,1
```

Directly below `CI-ITERATION 0`, the final CAS-CI energies are printed,
and one observes that they follow the correct degeneracy pattern
(i.e. 5 states with energy `-1271.258899450` and 7 states with energy
`-1271.186288591`). Furthermore, the final state-averaged CASSCF energy
(`E(CAS)= -1271.222594021`) and occupation numbers
(`N(occ)= 1.50000 1.30000 1.30000 1.30000 1.30000 1.30000`) are also
printed. As expected, the occupation number of the 4s orbital is indeed
1.5, while the 3d orbitals each have an occupation of 1.3.

#### Selection of the States to Include in the MR-EOM-CC  Calculation

Once a satisfactory CASSCF reference has been obtained, the next step is
to determine the number of states to include in the MR-EOM-CC  calculation.
From the NIST atomic spectra database, one finds that the higher lying
states of 4s$^2$3d$^6$ and
4s$^1$3d$^7$ character are either singlets, triplets,
or quintets. To figure out how many states should be included in each
multiplicity block, one can perform an inexpensive CAS-CI calculation.
This is done by reading in the orbitals from the previous CASSCF
calculation (here they are stored in the file `CAS.gbw`) and requesting
a single iteration (i.e. using the `NoIter` keyword) of a state-averaged
CASSCF calculation:

```{literalinclude} ../../orca_working_input/C06S22_486.inp
:language: orca
```

Here, after some experimentation, we have chosen 15 quintets, 90
triplets and 55 singlets. It is important that we calculate states up to
sufficiently high energy (i.e. all the states that are of interest) and
it is imperative that we have complete multiplets. Hence, several
iterations of this procedure might be required to choose the proper
number of states for each multiplet. The relevant section of the output
file which should be analyzed is the `SA-CASSCF TRANSITION ENERGIES`.
For the above calculation, we obtain (i.e. only the CAS-CI energies for
the first 33 roots are shown here):

```orca
-----------------------------
SA-CASSCF TRANSITION ENERGIES
------------------------------

LOWEST ROOT (ROOT 0 ,MULT 5) =  -1271.258899450 Eh -34592.713 eV

STATE   ROOT MULT  DE/a.u.    DE/eV    DE/cm**-1
   1:    1    5   0.000000     0.000      0.0
   2:    2    5   0.000000     0.000      0.0
   3:    3    5   0.000000     0.000      0.0
   4:    4    5   0.000000     0.000      0.0
   5:    5    5   0.072611     1.976  15936.2
   6:    6    5   0.072611     1.976  15936.2
   7:    7    5   0.072611     1.976  15936.2
   8:    8    5   0.072611     1.976  15936.2
   9:    9    5   0.072611     1.976  15936.2
  10:   10    5   0.072611     1.976  15936.2
  11:   11    5   0.072611     1.976  15936.2
  12:    0    3   0.092859     2.527  20380.2
  13:    1    3   0.092859     2.527  20380.2
  14:    2    3   0.092859     2.527  20380.2
  15:    3    3   0.092859     2.527  20380.2
  16:    4    3   0.092859     2.527  20380.2
  17:    5    3   0.092859     2.527  20380.2
  18:    6    3   0.092859     2.527  20380.2
  19:    7    3   0.092859     2.527  20380.2
  20:    8    3   0.092859     2.527  20380.2
  21:    9    3   0.092859     2.527  20380.2
  22:   10    3   0.092859     2.527  20380.2
  23:   11    3   0.101848     2.771  22353.1
  24:   12    3   0.101848     2.771  22353.1
  25:   13    3   0.101848     2.771  22353.1
  26:   14    3   0.101848     2.771  22353.1
  27:   15    3   0.101848     2.771  22353.1
  28:   16    3   0.101848     2.771  22353.1
  29:   17    3   0.101848     2.771  22353.1
  30:   18    3   0.102559     2.791  22509.1
  31:   19    3   0.102559     2.791  22509.1
  32:   20    3   0.102559     2.791  22509.1
```

#### Running the MR-EOM-CC  Calculation

Now that we have chosen a suitable CASSCF reference and the states that
we wish to calculate, we can finally proceed with the MR-EOM
calculation. The following input file runs an MR-EOM-T|T$^\dagger$|SXD|U-h-v
calculation for 15 quintet, 90 triplet and 55 singlet states of the
neutral Fe atom (i.e. the CASSCF orbitals are read from `CAS.gbw`):

```orcainput
!MR-EOM  DKH-Def2-TZVPP VeryTightSCF DKH

!MOREAD
%moinp "CAS.gbw"

%method frozencore fc_ewin end

%casscf
  nel 8
  norb 6
  mult 5
  nroots 12
  weights[0] = 0.7, 0.7, 0.7, 0.7, 0.7, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5
end

%mdci
  ewin -6, 10000
  STol 1e-7
end

%mrci
  ewin -6, 10000
  MaxIter 200
  newblock 5 *
    nroots 15
    refs cas(8,6) end
  end
  newblock 3 *
    nroots 90
    refs cas(8,6) end
  end
  newblock 1 *
    nroots 55
    refs cas(8,6) end
  end
end

* xyz 0 5
  Fe 0.000000 0.000000 0.000000
end
```

Note that since the default frozen core settings exclude the 3p orbitals
from the correlation treatment, we have used an energy window (i.e. the
line `ewin -6, 10000` in both the `%mdci` and `%mrci` blocks) such that
they are included in the current calculation. We note that a detailed
discussion of the input and output of an MR-EOM-CC  calculation has already
been given in
section {numref}`sec:modelchemistries.mreom` and thus, we do not repeat it here. It is
important to reiterate that one should always inspect the values of the
largest (T, S and U) amplitudes. Ideally, the largest amplitudes should
be smaller than 0.1 and should not exceed 0.15. If some amplitudes are
larger than 0.15, it might be necessary to revisit the definition of the
CAS and the weights used. For the T amplitudes, an alternative solution
is to use the projection/singular PT scheme discussed in
section {numref}`sec:modelchemistries.mreom.singularpt` below.

As discussed in section
{numref}`sec:modelchemistries.mreom`, the excitation energies are printed
under the heading `TRANSITION ENERGIES`. For the current calculation, we
obtain the following results (only the results for 33 states are shown
here):

```orca
-------------------
TRANSITION ENERGIES
-------------------

The lowest energy is  -1271.833871822 Eh

State Mult Irrep Root Block    mEh          eV      1/cm
  0    5    -1    0    0      0.000      0.000       0.0
  1    5    -1    1    0      0.000      0.000       0.0
  2    5    -1    2    0      0.000      0.000       0.0
  3    5    -1    3    0      0.000      0.000       0.0
  4    5    -1    4    0      0.000      0.000       0.0
  5    5    -1    5    0     33.901      0.922    7440.4
  6    5    -1    6    0     33.901      0.922    7440.4
  7    5    -1    7    0     33.901      0.922    7440.4
  8    5    -1    8    0     33.901      0.922    7440.4
  9    5    -1    9    0     33.901      0.922    7440.4
 10    5    -1   10    0     33.901      0.922    7440.4
 11    5    -1   11    0     33.901      0.922    7440.4
 12    3    -1    0    1     54.743      1.490   12014.8
 13    3    -1    1    1     54.743      1.490   12014.8
 14    3    -1    2    1     54.743      1.490   12014.8
 15    3    -1    3    1     54.743      1.490   12014.8
 16    3    -1    4    1     54.743      1.490   12014.8
 17    3    -1    5    1     54.743      1.490   12014.8
 18    3    -1    6    1     54.743      1.490   12014.8
 19    5    -1   12    0     78.790      2.144   17292.5
 20    5    -1   13    0     78.790      2.144   17292.5
 21    5    -1   14    0     78.790      2.144   17292.5
 22    3    -1    7    1     95.413      2.596   20940.8
 23    3    -1    8    1     95.413      2.596   20940.8
 24    3    -1    9    1     95.413      2.596   20940.8
 25    3    -1   10    1     95.413      2.596   20940.8
 26    3    -1   11    1     95.413      2.596   20940.8
 27    3    -1   12    1     95.413      2.596   20940.8
 28    3    -1   13    1     95.413      2.596   20940.8
 29    3    -1   14    1     95.413      2.596   20940.8
 30    3    -1   15    1     95.413      2.596   20940.8
 31    3    -1   16    1     95.413      2.596   20940.8
 32    3    -1   17    1     95.413      2.596   20940.8
```

It is also important to recall that one should always inspect the
reference weights for each state, as only states which are dominated by
reference space configurations can be treated accurately at the MR-EOM
level of theory. Generally, the reference weights should be larger than
(or close to) 0.9. In each multiplicity block, the individual state
energies and reference weights can be found following convergence of the
MRCI procedure, under the heading `CI-RESULTS` (see
section {numref}`sec:modelchemistries.mreom` for a more detailed discussion).

### Approximate Inclusion of Spin-Orbit Coupling Effects in MR-EOM-CC  Calculations

The effects of spin-orbit coupling can approximately be included in
MR-EOM-CC  calculations using the SOC submodule of the MRCI module. This can be viewed as a first order
approximation to the inclusion of spin-orbit coupling effects in MR-EOM-CC.
In a more rigorous formulation, one would have to consider the various
similarity transformations of the spin-orbit coupling operator. The
details of the SOC submodule of the MRCI module have already been
discussed in detail in
Sec. {numref}`sec:modelchemistries.mrci.soc` and its usage within the MR-EOM
formalism is identical to that discussed therein. Let us consider the
calculation of spin-orbit coupling effects in the excitation spectrum of
the neutral Fe atom considered in the previous section. The input file
for this calculation is:

```{literalinclude} ../../orca_working_input/C06S22_488.inp
:language: orca
```

In contrast with the calculation performed in
section {numref}`sec:modelchemistries.mreom.calc`, the convergence thresholds have
been tightened in all aspects of the calculation (i.e. the use of the
`ExtremeSCF` keyword, `etol` and `gtol` (CASSCF energy and orbital
gradient convergence tolerance) are set to $1 \times 10^{-12}$ and the
convergence tolerance for the residuals in the MR-EOM-CC  amplitude
iterations have been set to $1 \times 10^{-12}$). We note that with the
use of the `ExtremeSCF` keyword, the convergence tolerance on the energy
(`Etol`) and residual (`Rtol`) in the MRCI portion of the calculation
are also set to $1 \times 10^{-12}$. Although it is not absolutely
necessary, we have used very strict convergence thresholds to preserve
the degeneracies of the various multiplets as much as possible. The
output of spin-orbit corrected MR-EOM-CC  spectrum appears under the heading
`SOC CORRECTED ABSORPTION SPECTRUM VIA TRANSITION DIPOLE MOMENTS`:

```orca
--------------------------------------------------------------------------------------------------------
      SOC CORRECTED ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS    
--------------------------------------------------------------------------------------------------------
      Transition         Energy     Energy  Wavelength fosc(D2)      D2       |DX|      |DY|      |DZ|  
                          (eV)      (cm-1)    (nm)  (*population)  (au**2)    (au)      (au)      (au)  
--------------------------------------------------------------------------------------------------------
```

It is possible to obtain more accurate results by performing an
MR-EOM-T|T$^\dagger$|SXD-h-v calculation and including the 1h1p excitations.
It is important to note that these calculations are significantly more
expensive. As discussed above, to run an MR-EOM-T|T$^\dagger$|SXD-h-v
calculation, the keyword `MR-EOM-T|Td|SXD` must appear in the first line
of input and, in order to activate the 1h1p excitations in each
multiplicity block of the MRCI calculation, the `%mrci` block takes the
form:

```orca
%mrci
  ewin -6, 10000
  MaxIter 200
  newblock 5 *
    nroots 15
    excitations none
    Flags[is] 1
    Flags[sa] 1
    Flags[ia] 1
    Flags[ijss] 1
    refs cas(8,6) end
  end
  newblock 3 *
    nroots 90
    excitations none
    Flags[is] 1
    Flags[sa] 1
    Flags[ia] 1
    Flags[ijss] 1
    refs cas(8,6) end
  end
  newblock 1 *
    nroots 55
    excitations none
    Flags[is] 1
    Flags[sa] 1
    Flags[ia] 1
    Flags[ijss] 1
    refs cas(8,6) end
  end
  soc
    dosoc true
  end
end
```

We use `excitations none` to set the default excitation flags to false
and then manually set the 1h (`Flags[is]`), 1p (`Flags[sa]`), 1h1p
(`Flags[ia]`) and 2h (`Flags[ijss]`) excitation flags to true.

:::{warning}
-   Currently, MR-EOM-T|T$^\dagger$|SXD|U-h-v calculations can only be run
    with the default excitation classes in the final MRCI (i.e. 1h and
    1p). Any other input options for the excitation flags will
    automatically be overwritten and set to the default values.

-   Only the inclusion of spin-orbit coupling effects has been tested
    for MR-EOM-CC  calculations. Other features that are available in the
    MRCI module (e.g. spin-spin coupling, magnetic property
    calculations, etc.) have not been tested for use within MR-EOM
    calculations.
:::

(sec:modelchemistries.mreom.singularpt)=
### A Projection/Singular PT Scheme to Overcome Convergence Issues in the T Amplitude Iterations

In certain cases, there may be nearly singular T$_2$ amplitudes (often,
but not always large in magnitude), which can cause convergence issues
in the solution of the T amplitude equations. Hence, it is sometimes
necessary to discard some of the amplitudes to remedy these convergence
problems. The nearly singular T$_2$ amplitudes are of the form
$t^{ab}_{wx}$, where ($w,x$) is a pair of active orbitals which
corresponds to a small eigenvalue (pair occupation number $n_{wx}$) of
the two-body reduced density matrix (RDM). When nearly singular
amplitudes are present, it is possible to employ a singular
PT/projection scheme (i.e. Scheme I described in
Ref. {cite}`datta2011pICMRCC`), using the two-body RDM as the metric matrix,
to discard these nearly singular amplitudes and replace them with
suitable perturbative estimates. As a first example, let us consider the
following calculation on the cyclopentadiene molecule:

```{literalinclude} ../../orca_working_input/C06S22_490.inp
:language: orca
```

The T amplitude iterations do not converge after 60 iterations and show
no signs of convergence (i.e. final largest residual of 0.000458135 and
oscillatory behavior over a significant portion of the iterations). If
we inspect the largest T amplitudes,

```orca
--------------------
LARGEST T AMPLITUDES
--------------------
  19-> 24  19-> 24       0.043103
  19-> 23  19-> 23       0.031162
  11-> 25  11-> 25       0.028458
  19-> 41  19-> 41       0.027950
  11-> 47  11-> 47       0.027026
  19-> 22  19-> 22       0.025163
  19-> 21  19-> 21       0.022167
  15-> 26  15-> 26       0.022084
  11-> 47  11-> 25       0.022033
  11-> 25  11-> 47       0.022033
  19-> 24  19-> 29       0.021769
  19-> 29  19-> 24       0.021769
  19-> 36  19-> 36       0.020986
  17-> 38  17-> 38       0.019743
  19-> 41  16-> 36       0.019107
  18-> 40  18-> 40       0.017949
```

one can see that there are no unusually large amplitudes. If we turn on
the singular PT/projection scheme by adding the line `DoSingularPT true`
to the `%mdci` block:

```orca
%mdci
  STol 1e-7
  MaxIter 60
  DoSingularPT true
end
```

and rerun the calculation, we find that the T amplitude iterations now
successfully converge in 22 iterations. If we look at the largest T
amplitudes:

```orca
--------------------
LARGEST T AMPLITUDES
--------------------
  11-> 25  11-> 25       0.028440
  11-> 47  11-> 47       0.027027
  15-> 26  15-> 26       0.022069
  11-> 47  11-> 25       0.022031
  11-> 25  11-> 47       0.022031
  19-> 41  19-> 41       0.020463
  17-> 38  17-> 38       0.018288
  11-> 43  11-> 43       0.017250
  11-> 39  11-> 39       0.016838
  15-> 27  15-> 27       0.016001
  13-> 26  13-> 26       0.015985
  16-> 36  16-> 36       0.015759
  19-> 41  16-> 36       0.015697
  18-> 40  18-> 40       0.015376
  17-> 31  17-> 31       0.015074
  18-> 40  17-> 38       0.014470
```

most of the amplitudes corresponding to the active pair $(w,x)=(19,19)$
no longer appear in the list (i.e. they are nearly singular amplitudes
which have been projected out). The only one that does appear in the
list, corresponds to a projected perturbative estimate
(e.g. `19-> 41 19-> 41 0.020463`).

By default, when the singular PT/projection scheme is active, the
amplitudes $t^{ab}_{wx}$ for which the pair occupation numbers satisfy
$n_{wx}<0.01$ (i.e. `SingularPTThresh = 0.01`), are replaced by
perturbative amplitudes in the procedure. However, in some cases, it
might be necessary to increase the `SingularPTThresh` threshold beyond
the default value to achieve convergence. One such example is the
ferrocene molecule. Consider the following calculation:

```{literalinclude} ../../orca_working_input/C06S23_492.inp
:language: orca
```

The T amplitude iterations do not converge after 50 iterations, even
though the singular PT/projection scheme is activated. If we increase
`SingularPTThresh` to 0.05 by adding `SingularPTThresh 0.05` to the
`%mdci` block:

```orca
%mdci
  DoSingularPT true
  SingularPTThresh 0.05
  MaxIter 50
end
```

the T amplitude iterations successfully converge in 25 iterations.

In conclusion, it occasionally happens that the T amplitude iterations
do not converge. In these cases, the singular PT/projection scheme can
be activated (`DoSingularPT true`) to overcome these convergence
difficulties. Sometimes, like in the case of ferrocene, it is necessary
to adjust the threshold for the singular PT/projection procedure
(`SingularPTThresh`) to achieve convergence. If the procedure still
fails with larger values of the threshold, then it might be necessary to
revisit the definition of the state-averaged CAS.

(sec:modelchemistries.mreom.orbitalselect)=
## An Orbital Selection Scheme for More Efficient Calculations of Excitation Spectra with MR-EOM

As described in Ref. {cite}`huntington2015mreom_orb_select`, the MR-EOM
implementation in ORCA can make use of a sophisticated scheme to discard
inactive and virtual orbitals, which are not important for the
description of the excited states of interest. The selection of inactive
core orbitals is based on the eigenvalues of the core orbital selection
density

$$D_{i'j'}=D^{t}_{i'j'}+\frac{\text{Tr}\left( D^t \right)}{\text{Tr}\left( D^s \right)+\text{Tr}\left( D^u \right)}\left( D^s_{i'j'}+D^u_{i'j'} \right),$$ (os_eq1)

in which

$$\begin{aligned}
D^t_{i'j'}&=\sum_{w,a,b}t_{i'w}^{ab^{(1) }}\left( 2t_{j'w}^{ab^{(1) }}-t_{j'w}^{ba^{(1) }} \right), \\
D^s_{i'j'}&=\sum_{k,w,a}\Big[s_{i'k}^{aw^{(1) }}\left(2_{j'k}^{aw^{(1) }}-s_{kj'}^{aw^{(1) }}\right)+s_{ki'}^{aw^{(1) }}\left(2s_{kj'}^{aw^{(1) }}-s_{j'k}^{aw^{(1) }}\right) \Big], \\
D^u_{i'j'}&=\sum_{k',w,x}u_{i'k'}^{wx^{(1) }}\left( 2u_{j'k'}^{wx^{(1) }}-u_{k'j'}^{wx^{(1) }} \right),\end{aligned}$$

are respectively, the contributions from the first order
$t_{i'w}^{ab^{(1) }}$, $s_{i'k}^{aw^{(1) }}$ and $u_{i'k'}^{wx^{(1) }}$
amplitudes (i.e. note that all amplitudes have at least one active
label). Similarly, the selection of virtual orbitals is based upon the
eigenvalues of the virtual orbital selection density

$$\rho_{ab}=\rho^t_{ab}+\frac{\text{Tr}\left( \rho^t \right)}{\text{Tr}\left( \rho^s \right)} \rho^s_{ab},$$ (os_eq5)

in which, the contribution $\rho^t$, from the first order $T_2$
amplitudes, is given by

$$\rho^t_{ab}=\sum_{k,w,c}t_{wk}^{ac^{(1) }}\left( 2t_{wk}^{bc^{(1) }}-t_{wk}^{cb^{(1) }}\right) +\sum_{i',w,c}t_{i'w}^{ac^{(1) }}\left( 2t_{i'w}^{bc^{(1) }}-t_{i'w}^{cb^{(1) }} \right),$$ (os_eq6)

and the contribution $\rho^s$, from the first order $S_2$ amplitudes, is
given by

$$\rho^s_{ab}=\sum_{i',k,w}s_{i'k}^{aw^{(1) }}\left( 2s_{i'k}^{bw^{(1) }}-s_{ki'}^{bw^{(1) }} \right)+\sum_{i',w,x}s_{xi'}^{aw^{(1) }}\left( 2s_{xi'}^{bw^{(1) }}-s_{i'x}^{bw^{(1) }} \right).$$ (os_eq7)

Diagonalization of the core orbital selection density $D_{i'j'}$ and the
virtual orbital selection density $\rho_{ab}$ then yields two respective
sets of eigenvalues $\{\lambda_{i'}\}$ and $\{\lambda_a\}$. We have
found it useful to compute the ratios,

$$\mathcal{R}_{\text{core} }=\frac{\sum_{i'=0}^{n_{\text{core} }^{\text{excluded} }} \lambda_{i'} }{\sum_{i'=0}^{n_{\text{core} }}
\lambda_{i'} } \times 100\%, $$ (os_eq8)

$$\mathcal{R}_{\text{virt} }=\frac{\sum_{a=0}^{n_{\text{virt} }^{\text{excluded} }}
\lambda_{a} }{\sum_{a=0}^{n_{\text{virt} }}
\lambda_{a} } \times 100\%, $$ (os_eq9)

of the sum of the excluded eigenvalues to the sum over all eigenvalues.
The orbital selection in the core and virtual subspaces is then based
upon the values of these ratios, as will be discussed below.

The orbital selection procedure is activated by adding the keyword
`OrbitalSelection` to the first line of input, e.g.

```orca
! MR-EOM-CC  def2-TZVPP VeryTightSCF OrbitalSelection
```

There are two threshold parameters `CoreThresh` and `VirtualThresh`,
which are used to determine which inactive core and virtual orbitals are
to be discarded in the orbital selection procedure, respectively.
Namely, all inactive core orbitals for which
$\mathcal{R_{\text{core} }}<$ `CoreThresh`
(i.e. $\mathcal{R_{\text{core} }}$ as defined in
Eq. {eq}`os_eq8`) are
discarded and all virtual orbitals satisfying the condition
$\mathcal{R_{\text{virt} }}<$ `VirtualThresh`
(i.e. $\mathcal{R_{\text{virt} }}$ as defined in
Eq. {eq}`os_eq9`) are
discarded. The default values of these thresholds are `CoreThresh = 0.0`
(no core orbital selection) and `VirtualThresh = 1.0`. However, the
values of these parameters can easily be changed by redefining them in
the `%mdci` block:

```orca
%mdci
  CoreThresh 1.0
  VirtualThresh 1.0
end
```

Let us consider the calculation of the previous section
({ref}`sec:modelchemistries.mreom.singularpt`) on ferrocene, with the
orbital selection procedure activated (using the default thresholds):

```{literalinclude} ../../orca_working_input/C06S23_496.inp
:language: orca
```

The details of the orbital selection procedure are printed under the
heading `ORBITAL SELECTION`:

```orca
------------------------------------------------
ORBITAL SELECTION
------------------------------------------------

T1 is NOT used in the construction of the orbital selection densities
Factor (in percent) for inactive (core) orbital selection       ...      0.000000000
Factor (in percent) for virtual orbital selection               ...      1.000000000
Inactive orbitals before selection:    15 ...   44 ( 30 MO's/ 60 electrons)
Virtual orbitals before selection:     50 ...  220 (171 MO's              )
Inactive orbitals after selection:     15 ...   44 ( 30 MO's/ 60 electrons)
Virtual orbitals after selection:      50 ...  126 ( 77 MO's              )

-------------------------------------------
TIMINGS FOR THE ORBITAL SELECTION PROCEDURE
-------------------------------------------

Total Time for Orbital Selection            ...       61.470 sec

First Half Transformation                   ...       58.041 sec ( 94.4%)
Second Half Transformation                  ...        1.789 sec (  2.9%)
Formation of Orbital Selection Densities    ...        1.629 sec (  2.7%)
Core Orbital Selection                      ...        0.000 sec (  0.0%)
Virtual Orbital Selection                   ...        0.003 sec (  0.0%)
Finalization of Orbitals                    ...        0.006 sec (  0.0%)
```

Comparing the number of virtual orbitals before the orbital selection
procedure (171) with the number that are left after orbital selection
(77), we see that more than half have been discarded (94). The canonical
calculation (without orbital selection) takes 149373 seconds to run and
yields the following excitation energies:

```orca
-------------------
TRANSITION ENERGIES
-------------------

The lowest energy is  -1648.190045042 Eh

State Mult Irrep Root Block    mEh          eV      1/cm
  0    1    -1    0    0      0.000      0.000       0.0
  1    3    -1    0    1     65.110      1.772   14289.9
  2    3    -1    1    1     65.110      1.772   14289.9
  3    3    -1    2    1     70.413      1.916   15454.0
  4    3    -1    3    1     70.413      1.916   15454.0
  5    3    -1    4    1     95.979      2.612   21065.0
  6    3    -1    5    1     95.979      2.612   21065.0
  7    1    -1    1    0    105.302      2.865   23111.1
  8    1    -1    2    0    105.302      2.865   23111.1
  9    1    -1    3    0    107.034      2.913   23491.4
 10    1    -1    4    0    107.034      2.913   23491.4
 11    1    -1    5    0    160.595      4.370   35246.6
 12    1    -1    6    0    160.596      4.370   35246.6
 13    3    -1    6    1    164.694      4.482   36146.1
 14    3    -1    7    1    165.379      4.500   36296.6
 15    3    -1    8    1    165.379      4.500   36296.6
 16    3    -1    9    1    171.464      4.666   37632.1
 17    1    -1    7    0    208.587      5.676   45779.6
 18    1    -1    8    0    208.587      5.676   45779.6
 19    1    -1    9    0    213.093      5.799   46768.6
 20    1    -1   10    0    213.093      5.799   46768.6
 21    1    -1   11    0    216.225      5.884   47456.0
 22    1    -1   12    0    220.230      5.993   48334.9
 23    1    -1   13    0    220.230      5.993   48334.9
 24    1    -1   14    0    224.583      6.111   49290.3
 25    1    -1   15    0    224.583      6.111   49290.3
 26    1    -1   16    0    237.914      6.474   52216.0
 27    1    -1   17    0    237.914      6.474   52216.0
```

In contrast, the calculation with the orbital selection procedure
activated runs in 28977 seconds (a factor of 5 speedup) and produces the
following excitation energies:

```orca
-------------------
TRANSITION ENERGIES
-------------------

The lowest energy is  -1647.788478559 Eh

State Mult Irrep Root Block    mEh          eV      1/cm
  0    1    -1    0    0      0.000      0.000       0.0
  1    3    -1    0    1     65.112      1.772   14290.4
  2    3    -1    1    1     65.134      1.772   14295.3
  3    3    -1    2    1     70.520      1.919   15477.3
  4    3    -1    3    1     70.520      1.919   15477.3
  5    3    -1    4    1     96.105      2.615   21092.7
  6    3    -1    5    1     96.134      2.616   21099.0
  7    1    -1    1    0    105.415      2.868   23136.0
  8    1    -1    2    0    105.450      2.869   23143.5
  9    1    -1    3    0    107.294      2.920   23548.3
 10    1    -1    4    0    107.294      2.920   23548.3
 11    1    -1    5    0    161.082      4.383   35353.4
 12    1    -1    6    0    161.094      4.384   35356.0
 13    3    -1    6    1    164.786      4.484   36166.4
 14    3    -1    7    1    165.465      4.503   36315.4
 15    3    -1    8    1    165.465      4.503   36315.5
 16    3    -1    9    1    171.542      4.668   37649.1
 17    1    -1    7    0    208.853      5.683   45838.0
 18    1    -1    8    0    208.853      5.683   45838.0
 19    1    -1    9    0    213.419      5.807   46840.1
 20    1    -1   10    0    213.419      5.807   46840.1
 21    1    -1   11    0    216.526      5.892   47521.9
 22    1    -1   12    0    220.611      6.003   48418.4
 23    1    -1   13    0    220.611      6.003   48418.5
 24    1    -1   14    0    225.135      6.126   49411.5
 25    1    -1   15    0    225.136      6.126   49411.5
 26    1    -1   16    0    238.388      6.487   52320.1
 27    1    -1   17    0    238.388      6.487   52320.1
```

We note that the excitation energies in the orbital selection procedure
agree very nicely with those of the canonical calculation. However, the
total energies are significantly different, as we currently have not
implemented a procedure to correct them. Hence, the following warning is
particularly important.

WARNING

-   The orbital selection procedure should only be used for the
    calculation of excitation energies. Total energies computed with the
    orbital selection procedure have not been corrected and can differ
    greatly from the canonical results.

Before leaving the discussion of the orbital selection procedure, we
note that there is also a keyword `PrintOrbSelect`, which can be added
to the `%mdci` block to print the eigenvalues of the inactive core
orbital selection and virtual orbital selection densities and the
corresponding values of $\mathcal{R}_{\text{core} }$ and
$\mathcal{R}_{\text{virt} }$ defined in
Eqs. {eq}`os_eq8`
and {eq}`os_eq9`,
respectively. This is useful if one wants to manually select the
orbitals to discard in the orbital selection procedure by adjusting the
values of `CoreThresh` and `VirtualThresh`. We note that the program
terminates after printing. In the case of the calculation on ferrocene,
if we modify the `%mdci` block to read

```orca
%mdci
  DoSingularPT true
  SingularPTThresh 0.05
  MaxIter 50
  PrintOrbSelect True
end
```

we find the following information in the `ORBITAL SELECTION` section of
the output (only the first 50 values for the virtual orbital selection
density are shown here):

```orca
Eigenvalues and corresponding R_core values for the core orbital selection density

Orbital        Eigenvalue        R_core
   0           0.00026936        0.419318
   1           0.00027080        0.840883
   2           0.00038739        1.443947
   3           0.00038739        2.047011
   4           0.00040299        2.674355
   5           0.00040299        3.301700
   6           0.00077636        4.510285
   7           0.00086085        5.850394
   8           0.00086085        7.190503
   9           0.00091850        8.620358
  10           0.00091850       10.050213
  11           0.00112826       11.806598
  12           0.00115561       13.605563
  13           0.00137961       15.753236
  14           0.00137961       17.900908
  15           0.00139093       20.066210
  16           0.00139093       22.231512
  17           0.00143349       24.463072
  18           0.00143350       26.694633
  19           0.00148539       29.006985
  20           0.00148539       31.319338
  21           0.00173415       34.018940
  22           0.00224131       37.508054
  23           0.00224132       40.997171
  24           0.00533017       49.294785
  25           0.00533019       57.592429
  26           0.00658679       67.846267
  27           0.00662033       78.152314
  28           0.00701718       89.076149
  29           0.00701719      100.000000

 Eigenvalues and corresponding R_virt values for the virtual orbital selection density

Orbital        Eigenvalue        R_virt
   0           0.00000119        0.000450
   1           0.00000119        0.000899
   2           0.00000134        0.001404
   3           0.00000134        0.001909
   4           0.00000136        0.002423
   5           0.00000177        0.003091
   6           0.00000178        0.003764
   7           0.00000178        0.004437
   8           0.00000215        0.005248
   9           0.00000224        0.006096
  10           0.00000224        0.006944
  11           0.00000238        0.007844
  12           0.00000347        0.009154
  13           0.00000347        0.010465
  14           0.00000364        0.011841
  15           0.00000386        0.013299
  16           0.00000396        0.014793
  17           0.00000396        0.016287
  18           0.00000437        0.017937
  19           0.00000437        0.019587
  20           0.00000499        0.021472
  21           0.00000499        0.023357
  22           0.00000794        0.026354
  23           0.00000794        0.029352
  24           0.00000819        0.032447
  25           0.00000819        0.035543
  26           0.00000927        0.039044
  27           0.00000927        0.042546
  28           0.00001002        0.046332
  29           0.00001002        0.050119
  30           0.00001137        0.054415
  31           0.00001137        0.058711
  32           0.00001158        0.063086
  33           0.00001158        0.067461
  34           0.00001381        0.072678
  35           0.00001381        0.077894
  36           0.00001417        0.083249
  37           0.00001417        0.088604
  38           0.00001465        0.094137
  39           0.00001495        0.099785
  40           0.00001495        0.105432
  41           0.00001554        0.111302
  42           0.00001554        0.117172
  43           0.00001623        0.123303
  44           0.00001689        0.129685
  45           0.00001754        0.136310
  46           0.00001754        0.142934
  47           0.00001805        0.149752
  48           0.00001805        0.156570
  49           0.00002111        0.164546

.
.
.
```

In conclusion, the orbital selection scheme provides a more efficient
way to calculate accurate excitation spectra within the framework of
MR-EOM-CC It can be used to extend the applicability of this approach to
larger systems and we expect it to be much more effective in larger
systems where the chromophore is localized to a small part of the
molecule. We reiterate that it is currently limited to the calculation
of excitation energies and should not be used if one is interested in
total energies.

## Nearly Size Consistent Results with MR-EOM-CC  by Employing an MR-CEPA(0) Shift in the Final Diagonalization Procedure

One drawback of the MR-EOM-CC  methodology is that it is not size-extensive
(or size-consistent). The size-extensivity errors arise due to the final
uncontracted MR-CI diagonalization step. Namely, they result from the
components of the eigenvectors of the transformed Hamiltonian, which lie
outside of the CASSCF reference space (e.g. 1h, 1p, etc.
configurations). As more of the excitation classes are included through
the successive similarity transformations of the Hamiltonian, the size
of the final diagonalization manifold is greatly decreased resulting in
much smaller size-extensivity errors upon going from
MR-EOM-T|T$^\dagger$-h-v to MR-EOM-T|T$^\dagger$|SXD|U-h-v. To illustrate this,
let us consider the O$_2$---O$_2$ dimer where the O$_2$ molecules are
separated by a large distance. For the O$_2$ monomer, we employ a
minimal active space consisting of 2 electrons distributed amongst the
two $\pi^*$ orbitals and we only consider the ground $^3\Sigma^{-}_g$
state (no state-averaging). In the MR-EOM-CC  calculations, we also
calculate the higher lying $^1\Delta_g$ and $^1\Sigma_g^{+}$ singlet
states. For example, the input file for the MR-EOM-T|T$^\dagger$|SXD|U-h-v
calculation is given by:

```{literalinclude} ../../orca_working_input/C06S23_498.inp
:language: orca
```

In the case of the dimer, we take the reference state as the coupled
quintet state which is formed as the product
$^3\Sigma_g^+\otimes\,^3\Sigma_g^+$ of the monomer states. We note that
at large separation, in the non-interacting limit, the dimer state
energies can be decomposed as the sum of monomer state energies. There
are various possibilities, taking into account the degeneracies of the
various states:

1.  a singlet, a triplet, and a quintet with energy
    $E(^3\Sigma_g^{-}+\,^3\Sigma_g^{-})$,

2.  four triplets with energy $E(^3\Sigma_g^{-}+\,^1\Delta_g)$,

3.  two triplets with energy $E(^3\Sigma_g^{-}+\,^1\Sigma_g^{+})$,

4.  four singlets with energy $E(^1\Delta_g+\,^1\Delta_g)$,

5.  four singlets with energy $E(^1\Delta_g+\,^1\Sigma_g^+)$,

6.  a singlet with energy $E(^1\Sigma_g^{+}+\,^1\Sigma_g^{+})$.

Hence, in the final diagonalization step of the MR-EOM-CC  calculation, we
must ask for 10 singlets, 7 triplets and 1 quintet. The input file for
the MR-EOM-T|T$^\dagger|$SXD|U-h-v calculation on the dimer is given by:

```{literalinclude} ../../orca_working_input/C06S23_499.inp
:language: orca
```

In Table {numref}`sc_energies1`, we have compiled the results of the size
consistency test, taking the difference of the dimer state energies (at
large separation) and the sum of the monomer state energies (in
$\text{m}E_\text{h}$). It is evident that as more excitation classes are
included in the similarity transformed Hamiltonian and the size of the
final diagonalization manifold is decreased, the size-consistency errors
decrease. Of particular note are the results for the
MR-EOM-T|T$^\dagger$|SXD|U-h-v approach (only includes 1h and 1p
configurations in the final diagonalization manifold), for which the
largest deviation is $1.25 \times 10^{-2}~\text{m}E_\text{h}$. The much
larger deviations for the MR-EOM-T|T$^\dagger|$SXD-h-v approach clearly
demonstrate the large effect that the 2h excitations have on the
size-consistency errors.

(sc_energies1)=
:::{table} Test for size consistency in MR-EOM-CC Differences in energy (in mE$_\text{h}$) between the  $_2$---O$_2$ dimer energies (at large separation) and the sum of the monomer energies for the ground state and various excited states. The results were obtained in an aug-cc-pVTZ basis using minimal active spaces.

|                                             | T\|T$^{\dagger}$-h-v | T\|T$^{\dagger}$\|SXD-h-v (with 1h1p) | T\|T$^{\dagger}$\|SXD-h-v |   T\|T$^{\dagger}$\|SXD\|U-h-v   |
|:--------------------------------------------|:---------------:|:------------------------------:|:------------------:|:-----------------------:|
| $\Delta E(^3\Sigma_g^{-}+\,^3\Sigma_g^{-})$ |      12.74      |              2.77              |        1.11        | 1.00 $\times$ $10^{-5}$ |
| $\Delta E(^3\Sigma_g^{-}+\,^1\Delta_g)$     |      14.20      |              3.84              |        1.85        | 1.54 $\times$ $10^{-4}$ |
| $\Delta E(^3\Sigma_g^{-}+\,^1\Sigma_g^{+})$ |      17.21      |              5.52              |        2.83        | 4.13 $\times$ $10^{-4}$ |
| $\Delta E(^1\Delta_g+\,^1\Delta_g)$         |      15.69      |              3.10              |        2.31        | 5.26 $\times$ $10^{-3}$ |
| $\Delta E(^1\Delta_g+\,^1\Sigma_g^{+})$     |      18.83      |              7.52              |        4.76        | 5.89 $\times$ $10^{-3}$ |
| $\Delta E(^1\Sigma_g^{+}+\,^1\Sigma_g^{+})$ |      22.34      |             10.75              |        7.31        | 1.25 $\times$ $10^{-2}$ |

:::

To reduce the size-consistency errors, one can make use of the
MR-CEPA(0) shift in the final diagonalization step. This MR-CEPA(0)
shift can easily be activated by adding the line

```orca
citype mrcepa_0
```

to the beginning of the `%mrci` block. The results of the
size-consistency test with the use of the MR-CEPA(0) shift are tabulated
in Table {numref}`sc_energies2`. For each of the methods, we see a marked
improvement over the results of Table
{ref}`sc_energies1`, which
do not make use of the MR-CEPA(0) shift. The greatest improvement occurs
in the MR-EOM-T|T$^\dagger$|SXD-h-v and the MR-EOM-T|T$^\dagger$|SXD|U-h-v results.
Namely, the errors in the former case are on the order of nano Hartrees,
while the errors in the MR-EOM-T|T$^\dagger$|SXD|U-h-v results are not
detectable (sub-nano Hartree), as the energy is only printed with nine
decimal places. It is interesting to note that upon adding the 1h1p
configurations to the diagonalization manifold in the
MR-EOM-T|T$^\dagger$|SXD-h-v calculations (i.e. with 1h1p), the
size-consistency errors increase greatly. Hence, it appears that the use
of the MR-CEPA(0) shift is most effective at reducing the
size-consistency errors resulting from the presence of the 1h, 1p and 2h
configurations in the final diagonalization manifold. In any case, one
can easily take advantage of this approach to obtain nearly
size-consistent results with both the MR-EOM-T|T$^\dagger$|SXD-h-v and
MR-EOM-T|T$^\dagger$|SXD|U-h-v methods.


(sc_energies2)=
:::{table} Test for size consistency in MR-EOM-CC using the MR-CEPA(0) shift: Differences in energy (in mE$_\text{h}$) between the O$_2$---O$_2$ dimer energies (at large separation) and the sum of the monomer energies for the ground state and various excited states. The results were obtained in an aug-cc-pVTZ basis using minimal active spaces and the MR-CEPA(0) shift was applied in the final diagonalization in each case.

|                                             | T\|T$^{\dagger}$-h-v    | T\|T$^{\dagger}$\|SXD-h-v (with 1h1p) | T\|T$^{\dagger}$\|SXD-h-v | T\|T$^{\dagger}$\|SXD\|U-h-v |
|:--------------------------------------------|:-----------------------:|:------------------------------:|:-----------------------:|:--------------------:|
| $\Delta E(^3\Sigma_g^{-}+\,^3\Sigma_g^{-})$ | 2.75 $\times$ $10^{-3}$ |              0.01              | 2.00 $\times$ $10^{-6}$ |         0.00         |
| $\Delta E(^3\Sigma_g^{-}+\,^1\Delta_g)$     |          0.06           |              0.07              |          0.00           |         0.00         |
| $\Delta E(^3\Sigma_g^{-}+\,^1\Sigma_g^{+})$ |          0.14           |              0.15              | 4.00 $\times$ $10^{-6}$ |         0.00         |
| $\Delta E(^1\Delta_g+\,^1\Delta_g)$         |          0.21           |              0.22              | 1.00 $\times$ $10^{-6}$ |         0.00         |
| $\Delta E(^1\Delta_g+\,^1\Sigma_g^{+})$     |          0.42           |              0.44              | 5.00 $\times$ $10^{-6}$ |         0.00         |
| $\Delta E(^1\Sigma_g^{+}+\,^1\Sigma_g^{+})$ |          0.82           |              0.87              | 9.00 $\times$ $10^{-6}$ |         0.00         |

:::

## Perturbative MR-EOM-CCPT

The MR-EOM-T approach was developed for situations where the full
accuracy of the iterative MR-EOM-CC  method is not required. It performs
on par with other multireference perturbation theories such as
fic-NEVPT2 and does not have the convergence difficulties with the
$\hat T$ and $\hat S,\hat X,\hat D$ amplitudes like its iterative parent
method as these amplitudes are computed in a non-iterative fashion. The
only iterative part of the MR-EOM-T method is the calculation of the
$\hat U$ amplitudes since they are quick to converge
anyways {cite}`Lechner2021`.

The setup procedure for the MR-EOM-T method is the same as for the
MR-EOM-CC  method, and the foregoing also applies to the perturbative
variant. Please note that the orbital selection scheme has not been
tested with this variant and should be unnecessary anyways since
calculations are much faster than with the iterative MR-EOM-CC  method.

To invoke the new variant, set up the calculation as you would for an
MR-EOM-CC  calculation and then add the keyword `DoMREOM_MRPT True` to the
`%mdci` block.

The results are interpreted just like results for the iterative MR-EOM-CC 
method. After transforming the Hamiltonian with the perturbatively
estimated amplitudes and the final MRCIS diagonalization step, the final
state energies are printed along with their reference weights. For
reliable results, we again recommend that the reference weight be
\>90%.
