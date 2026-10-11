

<a id="sec:essentialelements.stabilityanalysis"></a>
# SCF Stability Analysis

The SCF stability will give an indication whether the SCF solution is at
a local minimum or a saddle
point.[SeegerPopleXVIIIStability,AhlrichsDFTStability](../../bibliography.md) It is
available for RHF/RKS and UHF/UKS. In the latter case, the SCF is
restarted by default using new unrestricted start orbitals if an
instability was detected. For a demonstration, consider the following
input:

```mol
title: structure 1
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
2
structure (0 1)
h           0.0          0.0          0.0
h           0.0          0.0          1.4
--- input ---
! BHLYP def2-SVP NORI

%scf
 guess hcore
 HFTyp UHF
 STABPerform true
end

* xyz 0 1 
h 0.0 0.0 0.0
h 0.0 0.0 1.4
*
```

The HCORE guess leads to a symmetric/restricted guess, which does not
yield the unrestricted solution. The same is often true for other guess
options. For more details on the stability analysis, see Section
[essentialelements.stabilityanalysis](#sec:essentialelements.stabilityanalysis).

The SCF stability analysis evaluates the electronic Hessian (with
respect to orbital rotations) at the point indicated by the SCF solution
to determine the lowest eigenvalues of the Hessian. If one or more
negative eigenvalues are found, the SCF solution corresponds to a saddle
point and not a true local minimum in the space considered in the
analysis. A typical case are stretched bonds of diatomics, where the
symmetry of the initial guess leads to a restricted solution instead of
the often preferred unrestricted one. Several spaces are theoretically
possible[SeegerPopleXVIIIStability](../../bibliography.md). However, ORCA limits itself to the
analysis RHF/RKS in the space of UHF/UKS or UHF/UKS in the space of
UHF/UKS. As such, it is on the available for the SCF parts of DFT and
HF.[AhlrichsDFTStability](../../bibliography.md)
In the following, HF is used to
indicate both HF and KS. Consider the following input (unless indicated
otherwise, default values are shown):

```mol
title: structure 2
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
2
structure (0 1)
h           0.0          0.0          0.0
h           0.0          0.0          1.4
--- input ---
! BHLYP def2-SVP NORI

%scf 
 guess hcore # for illustrative purposes only 
 HFTyp UHF # default based on spin multiplicity
 STABPerform true # default false
 STABRestartUHFifUnstable true # restart the UHF-SCF if unstable 
 STABNRoots 3                  # number of eigenpairs sought
 STABMaxDim 3                  # Davidson expansion space = MaxDim * NRoots
 STABMaxIter 100               # maximum number of Davidson iterations
 STABNGuess 4096               # size of initial guess matrix: 4096 x 4096
 STABDTol 0.0001               # convergence criterion from iteration to iteration
 STABRTol 0.0001               # convergence criterion max residual norm
 STABlambda +0.5               # mixing parameter 
 STABORBWIN -1, -1, -1, -1,  -1, -1, -1, -1 # defines the donor / acceptor spaces
                               # 4 parameters for RHF
                               # 8 paramters for UHF (4 alpha, 4 beta) orbital
			       # window, -1 refers to automatic determination
 STABEWIN -5.0, 5.0            # lower and upper cutoff in Eh for automatic
                               # freezing 
 #---------------------------------------------------------------------------------
 # alternative specification using a sub-block: 
 stab
  NRoots 3
  MaxDim 3 # etc.
 end
end

* xyz 0 1 
h 0.0 0.0 0.0
h 0.0 0.0 1.4
*
```

The determination of the electronic Hessian is structurally comparable
to the TDHF/CIS/TDDFT procedure. Thus, many options are very similar and
the user is encouraged to read the section on TDDFT (Section
[spectroscopyproperties.tddft](../spectroscopyproperties/tddft.md#sec:spectroscopyproperties.tddft)) to clarify some of the options given
here. Since one is usually only interested in the qualitative
determination "stable or not?", three roots should be sufficient to find
the lowest eigenvalue. By the same philosophy, `StabMaxDim`,
`StabMaxIter`, `StabNGuess` and the convergence criteria were chosen.
The parameter `StabLambda` refers to the $\lambda$ of equation 37 of
reference [SeegerPopleXVIIIStability](../../bibliography.md), which determines the mixing of
the original SCF solution and the new orbitals to yield a new guess.
Choosing this value is not trivial, since positive and negative values
can lead to different new solutions (at least in principle). The
convergence of the ensuing SCF depends on it, as well, since all SCF
procedures require a sufficiently good guess to converge in a decent
number of iterations (or even at all).

The orbital window and the energy window can be specified. Note that the
`StabEWIN` will be overridden by the appropriate `StabORBWIN` values.
The automatic determination is also influenced by the
`%method FrozenCore` settings. Tests have shown that significant
curtailing of the actual orbital window can drastically influence the
results to the point of qualitative failure.

Current limitations on the method are:

-   Only single-point-like calculations are supported. For geometry
    optimizations etc., one must use the guess MORead feature
    [essentialelements.initialguess](initialguess.md#sec:essentialelements.initialguess) to employ the guess obtained
    here. Likewise, one must extract a geometry and run a separate
    calculation if one is interested in the SCF stability.

-   As for TDDFT, NORI, RIJONX, and RIJCOSX are supported. RI-JK is not
    supported.

-   Other, more advanced features like finite-temperature calculations
    and relativistic calculations (beside ECPs) are not possible at this
    time.

Overall, the user is cautioned against using the stability analysis
blindly without critically evaluating the result in terms of energy
difference and by investigating the orbitals (by the printout or by
plotting). Its usefulness cannot be denied, but it is certainly not
black-box.

An SCF stability analysis with default settings can be requested via
STABILITY, SCFSTABILITY, SCFSTAB or STAB on the simple input line.
