

<a id="sec:essentialelements.cpscf"></a>
# CP-SCF Options

The coupled perturbed self-consistent field (CP-SCF) equations have to
be solved in many cases, such as when second derivative properties (e.g.
vibrational frequencies, polarizability, NMR shielding, indirect
spin-spin coupling, hyperfine coupling, g-tensor) or the MP2 relaxed
density (in this case they are referred to as Z-vector equations) are
calculated. They are a set of linear equations generally expressed as

$$
\mathbf A \mathbf U^x = \mathbf B^x,
$$

where $\mathbf U^x$ is the vector of solutions for perturbation $x$, the
right-hand side (RHS) matrix $\mathbf B^x$ is perturbation-specific and
the left-hand side (LHS) matrix $\mathbf A$ is perturbation-independent
and contains, among other terms, the two-electron repulsion integrals
$\left(ij\vert ab\right)$ and $\left(ia\vert jb\right)$. The equations
are solved iteratively and the LHS is reassembled at every step, while
the RHS does not change. The generation and transformation of the
two-electron integrals are therefore the most time-consuming parts of
the CP-SCF solution.

The ORCA module which solves these equations accepts several options
given below with their default values:

```orca
%method
  Z_Solver     Pople # (default) Use the Pople algorithm to solve the equations
               DIIS  # Use the DIIS algorithm
               CG    # Use the conjugate gradient algorithm
  Z_Tol        1e-3  # Convergence tolerance for the residual norm. 
                     # Default is 1e-5 for VeryTightOpt
                     # and varies from 3e-3 to 3e-6 from LooseSCF to ExtremeSCF
  Z_MaxIter    128   # Maximum number of iterations
  Z_MaxDIIS    12    # Maximum number of DIIS vectors
  Z_Shift      0.3   # Level shift for DIIS
  Z_GridXC     1     # XC angular grid used for the LHS
  Z_IntAccXC   3.467 # XC radial grid accuracy used for the LHS
  Z_GridX      1     # COSX angular grid used for the LHS
  Z_IntAccX    3.067 # COSX radial grid accuracy used for the LHS
  Z_GridX_RHS  2     # COSX grid used for the RHS of MP2 Z-vector eqs (see below)
  Z_COSX_Alg   0     # (default) choose the best COSX algorithm automatically
               1     # better prescreening, more efficient for few densities
               2     # uses more memory, more efficient for many densities
end
```

Since ORCA 6, the same settings are used for all electric response
property calculations as well as for CIS/TD-DFT gradients and relaxed densities.
For convenience, the keywords in the `%elprop` input block are still
available but they modify the same internal variables as those in `%method`.
For magnetic response properties, the solver and convergence tolerance are
set separately in `%eprnmr`, because the convergence behavior of the magnetic
response CP-SCF equations is sometimes different.

```orca
%elprop
  Solver     # Alias, see: %method Z_Solver
  Tol        # Alias, see: %method Z_Tol
  MaxIter    # Alias, see: %method Z_MaxIter
  MaxDIIS    # Alias, see: %method Z_MaxDIIS
  LevelShift # Alias, see: %method Z_Shift
end

%eprnmr
  Solver     # Solver for magnetic response, see options at: %method Z_Solver
  Tol        # Convergence tolerance for magnetic response
  MaxIter    # Alias, see: %method Z_MaxIter
  MaxDIIS    # Alias, see: %method Z_MaxDIIS
  LevelShift # Alias, see: %method Z_Shift
end
```

The keywords `Z_GridX` and `Z_IntAccX` are applicable if the
RIJCOSX approximation is chosen for the
treatment of two-electron integrals. They determine the angular and
radial COSX integration grids, as discussed in
section [numericalintegration.gridothers](numericalintegration.md#sec:essentialelements.numericalintegration.gridothers). Analogously, the keywords
`Z_Grid` and `Z_IntAcc` determine the integration grid for DFT XC
functionals.

Integrals on the RHS are evaluated differently for different
perturbations - refer to
sections [ri.rijcosx](RI.md#sec:essentialelements.ri.rijcosx),
[properties.eprnmr](../spectroscopyproperties/nmr.md#sec:spectroscopyproperties.properties.eprnmr),
[mp2.rijcosxrigrad](../modelchemistries/MP2.md#sec:modelchemistries.mp2.rijcosxrigrad),
[mp2.2ndder](../modelchemistries/MP2.md#sec:modelchemistries.mp2.2ndder) and
[rimp2.response](../modelchemistries/MP2.md#sec:modelchemistries.mp2.rimp2.response) for SCF-level gradients,
EPR/NMR calculations with GIAOs, MP2 gradients, and MP2 second
derivatives, respectively. For MP2 Z-vector equations, the RIJCOSX
Fock-response terms in the RHS are evaluated with the COSX grid
specified by `Z_GridX_RHS`. Note that it is used differently to
`Z_GridX`: instead, it selects one of the three grids used in the SCF
(see Sections [ri.rijcosx](RI.md#sec:essentialelements.ri.rijcosx),
[rijcosx.grids](RI.md#sec:essentialelements.ri.rijcosx.grids),
[essentialelements.numericalintegration](numericalintegration.md#sec:essentialelements.numericalintegration) for details) and it is not recommended
to change the default value of 2.

If the RIJONX or RIJK approximation is used in the SCF,
the same is also employed in the CP-SCF.
Note, however, that the RI-K approximation is not efficient for these terms.

For properties based on correlated methods like CCSD, CCSD(T),
the solution of the CP-SCF equations are needed during the construction of the response integrals
as part of the RHS of the linear response equations, therefore a consistent `Z_Tol` is needed. For
more details, see [autoci.autociresp](../modelchemistries/autoci.md#sec:modelchemistries.autoci.autociresp).

!!! note
    When running RPA or the CP-SCF with COSX, the algorithm from ORCA-6.0.0 was hard-coded to a
    memory-hungry one, which was not the original intention. In ORCA-6.0.1 that was fixed,
    and the automatic one is now the default. This might cause very small differences to
    these results, specially if the number of densities is small. As a result,
    calculations give slightly different results with ORCA-6.0.0. This does not affect
    any "normal" energy, gradient or etc. calculations. Only those particular cases of RPA and CP-SCF.

