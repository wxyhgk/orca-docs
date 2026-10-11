<a id="sec:.quickstartguide.recommendations"></a>
# General Recommendations

!!! warning
    There are certainly differing opinions among scientists on what method to use when and why. However, we want to give some subjective
    advise in the context of ORCA based on the developers experience.

ORCA provides a comprehensive and powerful toolkit for quantum chemical calculations. However, the choice of a suitable method
for the chemical challenge at hand is often difficult, yet essential to obtain reasonable results. Nevertheless, some general subjective recommendations can be made to navigate through the sheer mass of available method combinations and computational approaches. We further recommend to check for educational review articles that cover
the basics of computational chemistry applications.

!!! note "Educative Reviews on Computational Chemistry"

    - [bursch20222bestpracticedft](../../bibliography.md)

<a id="sec:.quickstartguide.recommendations.knowyourmethods"></a>
## Know Your Methods

Even though the theoretical background of some methods can be complicated, one should know the strengths and limitations of the chosen method. Accordingly, it is recommended
to get a fundamental idea of the theoretical basis of any method before using it. Some prominent examples are:

*   Typical DFT functionals cannot recover London dispersion effects by theory. Therefore employing a suitable [dispersion correction](#sec:modelchemistries.dispersioncorrections) is mandatory, especially for large systems.

*   Second order Møller-Plesset perturbation theory relies on an energy difference of occupied and unoccupied orbitals in the denominator of its energy expression. Thus, it
    may break down for systems with small orbital gaps or near-degenerate electronic states (e.g. in many 3d transition metal complexes)

*   Single-reference methods like conventional DFT and [single-reference Coupled-Cluster may not be useful for multi-reference cases](#sec:modelchemistries.CCsDiagnostic). When to go to multireference methods 
    is a more complicated question. Typically, this will be the case if multiplets are desired, pure spin functions for systems with several unpaired electrons, in bond breaking situations or for certain classes of excited states (loosely speaking: whenever there are weakly interacting electrons in the system). However, whenever you decide to do so, please be aware that this require substantial insight into the physics and chemistry of the problem at hand. An uneducated use of [CASSCF](#sec:modelchemistries.casscf) or MRCI/MRPT method likely yields numbers that are nonsensical and that at tremendous computational cost. Here, there is no substitute for experience (and patience).

!!! tip
    **Know the strengths and weaknesses of your method of choice**. After all, the accuracy of any approximate method is limited and whether its perfectly suited to compute a desired property can only be answered by experimentation and comparison to experimental results or high-level *ab initio* calculations. In this respect, we recommend to make use of various very useful benchmark studies that provide useful data and method recommendations for various properties!

<a id="sec:.quickstartguide.recommendations.costvsaccuracy"></a>
## Cost vs. Accuracy

Time and computer resources are not endless. Accordingly, it is important to know if the method of choice is capable of yielding sufficient accuracy at a given timeframe. Further, the fact that you may be able to compute one or the other number a little more accurate doesn’t mean that this helps understanding the physics and chemistry of a target system any better. The danger of getting locked into technicalities and miss the desired insight is real! The most relevant aspects that determine the cost-accuracy-ratio are (a) the method used, (b) the basis set used and (c) the cutoffs and tolerances used. Some example cases are:

*   Even high-level electronic structure methods will yield bad or at least unreliable results when used with minimal or small split-valence basis sets like STO-3G or 3-21G.
    However, they may be useful for very large molecules or in screening and exploratory approaches, if purely qualitative results are required. Basis sets of triple-$\zeta$ quality and beyond are recommended to obtain reliable results. Some examples are the Karlsruhe def2-TZVPP and the Dunning cc-pVTZ [basis sets](../essentialelements/basisset.md).

*   Using very loose optimization thresholds may speed up the optimization but can prevent your system to reach the real minimum at the given potential energy surface. 
    This is specifically the case for flexible molecules with relatively flat potential energy surfaces.

*   Insufficiently tight [numerical integration](../essentialelements/numericalintegration.md) grids can speed up the calculation but can also limit the accuracy of 
    otherwise highly accurate method/basis set combinations. Even though, the defaults in ORCA are chosen to give reasonable results in most cases, you should increase the numerical integration grid if you are aiming for high accuracy.

*   Some approximations harm more than others. For example, the [RI approximation](../essentialelements/RI.md) combined with sufficiently large auxiliary basis sets  
    drastically reduces the computation times without at almost no loss in accuracy. Therefore, we generally recommend the usage of RI techniques in line with ORCA's defaults.

!!! tip
    **Be clear about the level of accuracy you want to achieve.** If qualitative results are sufficient, it may make sense to reduce the base set size or thresholds. Nevertheless, there are limits beyond which any results are to be considered questionable.

<a id="sec:.quickstartguide.recommendations.model"></a>
## Creating the Right Model

Reproducing properties of a system at experimental conditions, e.g. at elevated temperatures or in solution, is one of the holy grails of quantum chemistry. However,
even the best electronic structure method will not help if the model for your system is incomplete or wrong. Some examples are:

*   If a molecule is flexible and has a flat potential energy surface, its molecular properties under experimental conditions may not be described by only one conformer. 
    In such cases, multi-structure approaches should be used to describe properties via Boltzmann-weighted conformer ensembles that may be generated with [GOAT](../structurereactivity/goat.md).

*   If your experiment is performed in solution, gas-phase simulations may not give reasonably accurate results. Inclusion of solvation effects either by 
    [implicit solvation](../essentialelements/solvationmodels.md) or explicit solvent molecules that can be added with the [SOLVATOR](../structurereactivity/solvator.md) tool may be necessary.

*   Creating a smaller model system may reduce the computation times but bears the risk of missing subtile effects that can cause significant differences compared to 
    the experiment.

!!! tip
    **Create your model wisely.** Always consider inclusion of environmental effects in your calculations and make sure that your structural model can reproduce the desired property.

<a id="sec:.quickstartguide.recommendations.match"></a>
## Matching Method and Property

A method that performs well for one property does not necessarily have to do so for another. This applies in particular to more approximate methods like [DFT](../modelchemistries/DensityFunctionalTheory.md). Therefore, we recommend to consult benchmark studies to find accurate and robust density functional approximations and method combinations for a given property. Some prominent cases are:

*   [(meta-)GGA functionals](#sec:modelchemistries.dft.gga) like PBE or r²SCAN yield good geometries even when combined with relatively small basis sets. 
    However, for energies  at least [hybrid](#sec:modelchemistries.dft.hybriddft) or even [double-hybrid functionals](#sec:modelchemistries.dft.doublehybriddft) are required to reach sufficiently high accuracies.

!!! warning
    Some researchers like to adjust the amount of Hartree-Fock
    exchange according to their needs or what they think is "better"
    than the standard. This increases the semiempirical character of the
    calculations and may represent fixes that only work for a given
    class of compounds and/or properties while worsening the results for
    others. With this caveat in mind it is one of the things that you
    are free to try if you like it. However, we do not recommend it
    since it will deteriorate the comparability of your results with
    those of other workers the vast majority of which use standard
    functionals. An alternative to changing the amount of HF exchange
    could be to simply construct a linear regression for a number of
    known cases and then use the linear regression.

*   Functionals that give mediocre energies like TPSS or TPSSh can be very useful in the context of computing spectroscopic properties like NMR shielding constants or
    EPR g-Tensors and hyperfine couplings.

*   Double-hybrid functionals yield high accuracies for most organic systems but should be avoided for systems with small HOMO-LUMO gaps (e.g. 3d transition metal complexes).

!!! tip
    **Check your method of choice**. We generally recommend to check for detailed benchmark studies on different properties. If none is available, it may be worth investing the time to benchmark promising methods for your system class and the desired property to compute. If that is not feasible, choosing less empirical higher-level *ab-initio* methods may be the better choice to increase the reliability of the results.

<a id="sec:.quickstartguide.recommendations.specific"></a>
## Some Method-specific Recommendations

-   DH's The perturbatively corrected functionals
    (B2PLYP) may also be a very good choice for many problems (at comparable
    cost to MP2; note that even for large molecules with more than 1000
    basis functions the MP2 correction only takes about 10-20% of the time
    required for the preceding SCF calculation if the RI approximation is
    invoked. For even larger molecules one has the option of speeding up the
    MP2 part even further by the DLPNO approximation).

-   DLPNO-CCSD(T)
    Beyond DFT and (SCS-)MP2 there are coupled-cluster methods and their
    implementation in ORCA is efficient. With the local pair natural orbital
    methods you can even study molecules of substantial size and with
    appealing turnaround times.

-   **def2-TZVP** is different from the old TZVP. It has been realized that
    if one invests into an accurate triple-zeta description of the
    valence region it makes limited sense to only employ a single
    polarization function. The accuracy is then limited by the
    polarization set and is not much better than what one gets from
    SV(P). Hence, def2-TZVP contains a single p-set for hydrogens but is
    otherwise very similar to the old TZVPP basis set, e.g. it contains
    2d1f polarization for main group elements and much more extensive
    polarization sets for transition metals. The highest polarization
    function (f for main group) does add substantially to the
    computational effort. Hence, we often use def2-TZVP without the f
    polarization function. In order to do that one can use the keyword
    def2-TZVP(-f). Together with RI or RIJCOSX this is still
    computationally economic enough for most studies.

-   **def2-TZVPP** is a fully consistent triple-zeta basis set that provides
    excellent accuracy for SCF calculations (HF and DFT) and is still
    pretty good for correlated calculations. It is a good basis set to
    provide final single point energies.

-   **def2-QZVPP** is a high accuracy basis set for all kinds of
    calculations. It provides SCF energies near the basis set limit and
    correlation energies that are also excellent. It is computationally
    expensive but with RI and RIJCOSX in conjunction with
    parallelization it can often still be applied for final single-point
    energy calculations. In conjunction with such large basis sets one
    should also increase the accuracy of the integration grids in DFT
    and RIJCOSX --- it would be a shame to limit the accuracy of
    otherwise very accurate calculations by numerical noise due to the
    grid.

-   **Correlation consistent basis sets** provide good correlation energies
    but poor to very poor SCF energies. For the same size, the ano-pVDZ
    basis sets are much more accurate but are also computationally more
    expensive. Except for systematic basis set extrapolation we see
    little reason to use the cc bases.

-   **Pople basis sets** are somewhat old fashioned and also much less
    consistent across the periodic table than the basis from the
    Karlsruhe group. Hence, we generally prefer the latter.

-   For **scalar relativistic calculations** (X2C,ZORA and DKH) we strongly
    recommend to use [basis sets that are recontracted for the respective relativistic correction](#sec:essentialelements.basisset.builtin.rel).

-   **Effective core potentials (ECPs)** lead to some savings (but not necessarily
    spectacular ones) compared to all-electron relativistic
    calculations. For accurate results, small core [ECPs](#sec:essentialelements.basisset.ecps) should be used.
    They are generally available for the def2 Karlsruhe type basis sets
    for elements past krypton. In general we prefer Stuttgart--Dresden
    ECPs over LANL ones. For the first transition row, the choices are
    more meager. Here Karlsruhe basis sets do not exist in conjunction
    with ECPs and you are bound to either SDD or LANL of which we
    recommend the former. Geometries and energies are usually good from
    ECPs, but for property calculations we strongly recommend to switch
    to all electron scalar relativistic calculations using ZORA
    (magnetic properties) or DKH (electric properties).

-   You can take advantage of a built-in basis set (printed using
    `!PrintBasis` or `orca_exportbasis`) and then modify it by
    uncontracting primitives, adding steeper functions etc. (fully
    uncontracted bases are generated via `uncontract` in `%basis`)
    Alternatively, some basis sets exist that are of at least
    double-zeta quality in the core region including the DZP and Dunning
    basis sets. For higher accuracy you may want to consider the `aug-`
    series of basis sets. See section
    [sec:essentialelements.basisset](#sec:essentialelements.basisset) for more about basis set input.

-   Likewise, if you are doing calculations on anions in the gas phase
    it is advisable to include diffuse functions in the basis set.
    Having these diffuse functions, however, makes things much more
    difficult as the locality of the basis set is significantly reduced.
    If these functions are included it is advisable to choose a small
    value for `Thresh` (10$^{-12}$ or lower). This is automatically done
    if the smallest eigenvalue of the overlap matrix is below DiffSThresh
    (which is 1e-6 by default). Also, diffuse functions
    tend to introduce basis set linear dependency issues, which can be
    solved by setting `Sthresh` to a larger value than the default
    10$^{-7}$ (see
    Section [sec:essentialelements.lindep](#sec:essentialelements.lindep)). Any value of `Sthresh` 
    beyond 1e-6 has to be used carefully, specially if one is running
    geometry optimizations, were different basis might be cut off during
    different geometry steps, or when comparing different conformers 
    since there could be some discontinuity on the final basis set.

-   The **integration grids** used in DFT should be viewed together with the
    basis set. If large basis set calculations are converged to high
    accuracy it is advisable to also use large DFT integration grids
    (like `! DEFGRID3`). For "unlimited" accuracy (i.e. benchmark
    calculations) it is probably best to use product grids (`Grid=0`)
    with a large value for `IntAcc` (perhaps around 6.0). The default
    grids have been chosen such that they provide adequate accuracy at
    the lowest possible computational cost, but for all-electron
    calculations on heavy elements in conjunction with scalar
    relativistic Hamiltonians you should examine the grid dependency
    very carefully and adjust these parameters accordingly to minimize
    errors. You should be aware that for large molecules the
    exchange-correlation integration is usually *not* the dominating
    factor (not even in combination with RI-J).

-   Similarly important is the value of `Thresh` that will largely
    determine the tunaround time for direct SCF calculations. It may be
    possible to go to values of 10$^{-6}$--10$^{-8}$ which will result
    in large speed-ups. However, the error in the final energy may then
    be 3 orders of magnitude larger than the cutoff or, sometimes, your
    calculation will fail to converge, due to the limited integral
    accuracy. In general it will not be possible to converge a direct
    SCF calculation to better than `Thresh` (the program will also not
    allow this). For higher accuracy values of maybe
    10$^{-10}$--10$^{-12}$ may be used with larger molecules requiring
    smaller cutoffs. In cases where the SCF is almost converged but then
    fails to finally converge (which is very annoying) decreasing
    `Thresh` and switch to `TRAH` SCF is recommended. In general, `TCut`
    should be around `0.01` $\times$`Thresh` in order to be on the safe
    side.

-   DFT calculations have many good features and in many cases they
    produce reliable results. In particular if you study organic
    molecules it is nevertheless a good idea to check on your DFT
    results using MP2. MP2 in the form of RI-MP2 is usually affordable
    and produces reliable results (in particular for weaker interactions
    where DFT is less accurate). In case of a large mismatch between the
    MP2 and DFT results the alarm rings --- in many such cases MP2 is
    the better choice, but in others (e.g. for redox processes or
    transition metal systems) it is not. Remember that SCS-MP2
    (RI-SCS-MP2) and double hybrid functionals will usually produce more
    accurate results than MP2 itself.

-   Coupled-cluster calculations become more and more feasible and
    should be used whenever possible. The DLPNO-CCSD and
    DLPNO-CCSD(T) calculations are available for single-point
    calculations and provide accurate results. However, a
    coupled-cluster study does require careful study of basis set
    effects because convergence to the basis set limit is very slow. The
    established basis set extrapolation schemes may be very helpful
    here. For open-shell molecules and in particular for transition
    metals one cannot be careful enough with the reference. You have to
    carefully check that the Hartree-Fock calculation converged to the
    desired state in order to get coupled-cluster results that are
    meaningful. Orbital optimized MP2, CASSCF or DFT orbitals may help
    but we have often encountered convergence difficulties in the
    coupled-cluster equations with such choices.

-   Generally speaking, CEPA is often better than CCSD and approaches
    the quality of CCSD(T). It is, however, also a little less robust
    than CC methods because of the less rigorous treatment of the single
    excitations in relation to electronic relaxation.

