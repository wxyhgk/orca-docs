

<a id="sec:essentialelements.ri"></a>
# Resolution-of-the-Identity (RI)

A very efficient and well-established way to speed up DFT calculations are resolution-of-the-idendity (RI) techniques also know as density-fitting.[whitten1973chem,baerends1973chem,dunlap1979chem,vanalsenoy1988comp,kendall1997theor,eichkorn1995chem,eichkorn1997theor](../../bibliography.md) Various variants to address the Coulomb part and Hartree-Fock exchange parts (cf. [Hartree-Fock](sec:essentialelements.hartreefock) and [Hybrid DFT](sec:modelchemistries.dft.hybriddft)). Available options available in ORCA include [RI-J](sec:essentialelements.ri.rij), [Split-RI-J](sec:essentialelements.ri.splitrij), [RIJONX](sec:essentialelements.ri.rijonx), [RI-JK](sec:essentialelements.ri.rijk), and [RIJCOSX](sec:essentialelements.ri.rijcosx). 

!!! note "Some Notes on RI in ORCA"
    :class: note
    * Any RI approximation requires the choice of a sufficiently large [auxiliary basis set](sec:essentialelements.basisset.aux).
    * [Split-RI-J](sec:essentialelements.ri.splitrij) using the `def2/J` auxiliary basis is the default for [non-hybrid DFT](sec:modelchemistries.dft.gga).
    * [RIJCOSX](sec:essentialelements.ri.rijcosx) using the `def2/J` auxiliary basis is the default for [hybrid DFT](sec:modelchemistries.dft.hybriddft).
    * When [scalar relativistic Hamiltonians](../essentialelements/relativistic.md) are used with all-electron basis sets, then `SARC/J` can be chosen as ageneral-purpose [auxiliary basis set](../essentialelements/basisset.md). Other choices are documented in the [basis sets section](sec:essentialelements.basisset).
    * The usage of RI is generally recommended as the introduced error is very small. The speedup further enables the usage of larger [basis sets](../essentialelements/basisset.md) for large
    systems which will improve the results significantly.
    * The default usage of RI approximations can be disabled by the `!NORI` keyword (not recommended!).
    * If you do not want to depend on the RI approximation, a reasonable yet inconvenient approach is to converge a RI-J calculation and then take the
    resulting orbitals as initial guess for a calculation with exact Coulomb term. This should converge within a few cycles and the total execution
    time should still be lower than just converging the calculation directly with exact Coulomb treatment.

<a id="sec:essentialelements.ri.rij"></a>
## RI-J

!!! note
    This is the default for non-hybrid DFT! Can be turned off by using `!NORI`.

A very useful approximation that greatly speeds up DFT calculations
unless the molecule gets very large is the so called "RI-approximation"

RI stands for "Resolution of the identity". In short, charge
distributions arising from *products of basis functions* are
approximated by a linear combination of *auxiliary basis functions*.

$$

\phi_{i} \left({ \vec{{r} }} \right)\phi_{j} \left({ \vec{{r} }}
\right)\approx \sum\limits_k { c_{k}^{ij} \eta_{k} (\mathrm{\mathbf{r} }) }\qquad \text{(eqn:15)}

$$

There are a variety of different possibilities to determine the
expansion coefficients $c_{k}^{ij}$. A while ago, Almlöf and coworkers
[vahtras1993chem](../../bibliography.md) have shown that for the approximation of electron
repulsion integrals, the best choice is to minimize the *residual
repulsion*.

!!! note
    The basic theory behind the RI method has been known for a long time and since at 
    least the late sixties, methods similar to the RI approximation have been used — 
    mainly in the context of “approximate ab initio methods” such as LEDO, PDDO, and MADO, 
    but also in density functional theory in the mid and late seventies by Baerends, Dunlap, 
    and others [baerends1973chem, dunlap1979chem, vanalsenoy1988comp, whitten1973chem](../../bibliography.md)

Define:

$$

R_{ij} \equiv \phi_{i} \left({ \vec{{r} }} \right)\phi_{j} \left({\vec{{r} }} \right)-\sum\limits_k { c_{k}^{ij} \eta_{k} \left({ \vec{{r} }}
\right)}\qquad \text{(eqn:16)}

$$

and

$$

T_{ij} =\int{ \int{ R_{ij} \left({ \vec{{r} }} \right)\frac{1}{\left|{\vec{{r} }-{\vec{{r} }}'} \right|}R_{ij} \left({ \vec{{r} }}
\right)d^{3}rd^{3}{r}'} }\qquad \text{(eqn:17)}

$$

Determining the coefficients that minimize $T_{ij}$ leads to

$$

\mathrm{\mathbf{c} }^{ij} =\mathrm{\mathbf{V} }^{-1}\mathrm{\mathbf{t} }^{ij}\qquad \text{(eqn:18)}

$$

where:

$$

t_{k}^{ij} =\left\langle { \phi_{i} \phi_{j} \left|{ r_{12}^{-1} }
\right|\eta_{k} } \right\rangle\qquad \text{(eqn:19)}

$$

$$

V_{ij} =\left\langle { \eta_{i} \left|{ r_{12}^{-1} } \right|\eta_{j} }\right\rangle\qquad \text{(eqn:20)}

$$

Thus, an ordinary two-electron integral becomes

$$

\begin{aligned}
  \left\langle { \phi_{i} \phi_{j} \left|{ r_{12}^{-1} } \right|\phi_{k}
    \phi_{l} } \right\rangle &\approx \sum\limits_{p,q} { c_{p}^{ij} c_{q}^{kl} V_{pq} } \\
  &=\sum\limits_{p,q} {V_{pq} \sum\limits_r { \left({ \mathrm{\mathbf{V} }^{-1} } \right)_{pr} t_{r}^{ij} }
    \sum\limits_s { \left({ \mathrm{\mathbf{V} }^{-1} } \right)_{qs} t_{s}^{kl} } } \\
  &=\sum\limits_{r,s}
    {\left({ \mathrm{\mathbf{V} }^{-1} } \right)_{rs} t_{r}^{ij} t_{s}^{kl} }
\end{aligned}\qquad \text{(eqn:21)}

$$

and the total Coulomb energy becomes

$$

\begin{aligned}
  E_{J} &=\sum\limits_{i,j} { \sum\limits_{k,l} { P_{ij} P_{kl} \left\langle {\phi_{i} \phi_{j} \left|{ r_{12}^{-1} } \right|\phi_{k}
    \phi_{l} }\right\rangle} } \\
  &\approx \sum\limits_{i,j} { \sum\limits_{k,l} { P_{ij} P_{kl} \sum\limits_{r,s} { 
    \left({ \mathrm{\mathbf{V} }^{-1} } \right)_{rs} t_{r}^{ij} t_{s}^{kl} } } } \\
  &=\sum\limits_{r,s} { \left({ \mathrm{\mathbf{V} }^{-1} } \right)_{rs} }
    \underbrace{ \sum\limits_{i,j} { P_{ij} t_{r}^{ij} } }_{\mathrm{\mathbf{X} }_{r}}
    \underbrace{ \sum\limits_{k,l} { P_{kl} t_{s}^{kl} } }_{\mathrm{\mathbf{X} }_{s}}
\end{aligned}\qquad \text{(eqn:23)}

$$ 

where $\mathrm{\mathbf{P} }$ is the total density matrix.

In a similar way, the Coulomb contribution to the Kohn-Sham matrix is
calculated. There are substantial advantages from this approximation:
the quantities to be stored are the matrix $\mathrm{\mathbf{V} }^{-1}$ ---
which depends only on two indices --- and the three-index auxiliary
integrals $t_{r}^{ij}$. This leads to a tremendous reduction of
storage requirements compared to a four-index list of repulsion integrals.
In addition, the two- and three-index electron repulsion integrals are 
easier to compute than the four-index integrals, leading to further 
reductions in processing time. Furthermore, the Coulomb energy and the Kohn-Sham matrix
contributions can be quickly assembled by simple vector/matrix
operations, leading to large time savings. This arises because each
auxiliary basis function $\eta_{k} \left({ \vec{{r} }} \right)$ appears
in the expansion of many charge distributions
$\phi_{i} \left({\vec{{r} }} \right)\phi_{j} \left({ \vec{{r} }} \right)$.
Unfortunately, a similar strategy is less easily applied (or, at least, with less benefit)
to the Hartree-Fock exchange term. 

If the auxiliary basis set $\left\{\eta \right\}$ is large enough, the
approximation is also highly accurate. Since any DFT procedure already
has a certain, sometimes sizable, error from the noise in the numerical
integration of the XC part, it might be argued that a similarly large
error in the Coulomb part is perfectly acceptable without affecting the
overall accuracy of the calculation much. Furthermore, the errors
introduced by the RI method are usually much smaller than the errors in
the calculation due to basis set incompleteness. It
is therefore recommended to use the RI procedure for pure DFs. However,
one should probably not directly mix absolute total energies obtained
from RI and non-RI calculations as the error in the total energy
accumulates and will rise with increased molecular size, while the
errors in the relative energies will tend to cancel.

There are several choices for auxiliary basis sets described in the next
section, which depend on the choice of the primary GTO basis set used to
expand the molecular orbitals [^cholesky]. The RI procedure requires the inversion of the auxiliary basis metric $\mathbf{V}$,
which is often the most expensive matrix operation in the calculation,
due to the O(N$^{3}$) scaling and the large size of the auxiliary basis.
However, in ORCA this is done via an efficient Cholesky decomposition,
which is only performed once during the startup phase of a single point caclulation.
Hence, this step is usually of no concern in practice.

In ORCA, the RI approximation is toggled by the input

```orca
%method
  RI  on   # do use the RI-J approximation
      off  # do not use the RI-J approximation
end
```

!!! note
    If you use RI, you *must* specify an auxiliary basis set (in the
    `%basis` section or using the appropriate simple keyword) or use
    the `!AutoAux` simple keyword. 

[^cholesky]: It probably should be noted that a slightly awkward step in the procedure is the inversion of the auxiliary integral matrix V, which can easily become very large. Matrix inversion is an $O(N^3)$ process such that for large molecules, this step takes some real time. However, in ORCA, this is only done once during the calculation, whereas other programs that constrain the fit to also exactly reproduce the number of electrons perform a similar process each iteration. Starting from ORCA 2.2.09, the Cholesky decomposition is used in favor of matrix inversion, removing any bottleneck concerning the solution of the linear equation system.

<a id="sec:essentialelements.ri.splitrij"></a>
## Split-RI-J

There is an improved version of the RI-algorithm that has been
implemented since ORCA 2.2.09. This Split-RI-J algorithm yields the same Coulomb
energy as the standard RI-algorithm, but is significantly faster if the
basis set contains many high angular momentum functions (d-, f-,
g-functions). For small basis sets, there is virtually no difference
between the two algorithms, except that Split-RI-J uses more memory than
standard RI. However, calculations with ca. 2000 basis functions only need
about an extra 13 MB for Split-RI-J, which is a trivial requirement on
present-day hardware.

The Split-RI-J algorithm is invoked with the `!Split-RI-J` simple keyword.
Split-RI-J is presently only available for SCF and gradient
calculations.

!!! note
    -   The Split-RI-J algorithm is the default if RI is turned on via
        `!RI`. If you do not want to use Split-RI-J, please also use the
        keyword `!NoSplit-RI-J`

<a id="sec:essentialelements.ri.rijonx"></a>
## RIJONX 

Alternatively, the RI method can be used for the
Coulomb term and the standard treatment for the exchange term. This
method is called RIJONX since the exchange term should tend towards
linear scaling for large molecules. RIJONX can be invoked via the `!RIJONX` keyword for
Hartree-Fock and hybrid DFT calculations.

```orca
! HF RIJONX
```

The requirements for the auxiliary basis are the same as for the normal
RI-J method.

<a id="sec:essentialelements.ri.rijcosx"></a>
## RIJCOSX 

Frustrated by the large difference in execution times between pure and
hybrid functionals, we have been motivated to study approximations to
the Hartree-Fock exchange term. The method that we have finally come up
with is called the "chain of spheres" COSX approximation and may be
thought of as a variant of the pseudo-spectral philosophy. Essentially,
in performing two electron integrals, the first integration is done
numerically on a grid and the second (involving the Coulomb singularity)
is done analytically. For algorithmic and theoretical details see Refs.
[neese2009chemphys](../../bibliography.md) and [Helmich-Paris2021a](../../bibliography.md). Upon combining this
treatment with the [Split-RI-J](sec:essentialelements.ri.splitrij) method for the Coulomb term (thus, a
Coulomb fitting basis is needed!), we have designed the RIJCOSX
approximation that can be used to accelerate Hartree-Fock and hybrid DFT
calculations. Note that this introduces another grid on top of the DFT
integration grid which is usually significantly smaller.

!!! note
    Since ORCA 5, RIJCOSX is the default option for hybrid DFT (can be
    turned off by using `!NOCOSX` ). However, it is by default NOT turned on
    for HF.

In particular for large and accurate basis sets, the speedups obtained
in this way are very large - we have observed up to a factor of sixty!
The procedure is essentially linear scaling such that large and accurate
calculations become possible with high efficiency. The RIJCOSX
approximation is basically available throughout the program. The default
errors are on the order of 0.05 $\pm$ 0.1 kcal mol$^{-1}$ or less in the
total energies as well as in energy differences and can be made smaller
with larger than the default grids or by running the final SCF cycle
without this approximation. The impact on bond distances is a fraction
of a pm, angles are better than a few tenth of a degree and soft
dihedral angles are good to about 1 degree. To the limited extent to
which it has been tested, vibrational frequencies are roughly good to
0.1 wavenumbers with the default settings.

The aim of this approximation is to efficiently compute the elements of
exchange-type matrices as described in refs. [Helmich-Paris2021a, neese2009chemphys](../../bibliography.md):

$$

K_{\mu \nu } =\sum\limits_{\kappa \tau } { P_{\kappa \tau } } (\mu \kappa
\vert \nu \tau )\qquad \text{(eqn:25)}

$$

where $\mathrm{\mathbf{P} }$ is some kind of density-type matrix (not
necessarily symmetric) and the two-electron integrals are defined over
the basis set $\{\varphi \}$ by:

$$

(\mu \kappa \vert \nu \tau )=\int{ \mu (\mathrm{\mathbf{r} }_{1} )\kappa (\mathrm{\mathbf{r} }_{1} )\nu (\mathrm{\mathbf{r} }_{2} )\tau (\mathrm{\mathbf{r} }_{2} )r_{12}^{-1} }
d\mathrm{\mathbf{r} }_{1} d\mathrm{\mathbf{r} }_{2}\qquad \text{(eqn:26)}

$$

The approximation pursued here can be written as follows:

$$

K_{\mu \nu } \approx \sum\limits_g { X_{\mu g} } \sum\limits_\tau{A_{\upsilon \tau } (\mathrm{\mathbf{r} }_{g} ) } \sum\limits_\kappa{ P_{\kappa \tau
} X_{\kappa g} }\qquad \text{(eqn:27)}

$$

Here, the index $g$ refers to grid points $\mathrm{\mathbf{r} }_{g}$ and:

$$

X_{\kappa g} =w_{g}^{1/2} \kappa (\mathrm{\mathbf{r} }_{g} )\qquad \text{(eqn:28)}

$$

$$

A_{\upsilon \tau } (\mathrm{\mathbf{r} }_{g} )=\int{ \frac{\nu (\mathrm{\mathbf{r} })\tau
(\mathrm{\mathbf{r} }) }{\vert \mathrm{\mathbf{r} }-\mathrm{\mathbf{r} }_{g} \vert }d\mathrm{\mathbf{r} }}\qquad \text{(eqn:29)}

$$

where $w_{g}$ denotes the grid weights. Thus, the first integration is
carried out numerically and the second one analytically. Note that this
destroys the Hermitian character of the two-electron integrals.

Equation [Eq](#eqn:27)
is perhaps best evaluated in three steps:

$$

F_{\tau g} =(\mathrm{\mathbf{PX} })_{\tau g}\qquad \text{(eqn:30)}

$$

$$

G_{\nu g} =\sum\limits_\tau{ A_{\nu \tau } (\mathrm{\mathbf{r} }_{g} )F_{\tau g} }\qquad \text{(eqn:31)}

$$

$$

K_{\mu \nu } =(\mathrm{\mathbf{XG} }^{+})_{\mu \nu }\qquad \text{(eqn:32)}

$$

As such, the equations are very similar to the pseudo-spectral method
extensively developed and discussed by Friesner and co-workers since the
mid 1980s and commercially available in the Jaguar quantum chemistry
package. The main difference at this point is that instead of
$X_{\kappa g}$ there appears a least-square fitting operator
$Q_{\kappa g}$ in Friesner's formulation. Note that an analogue of the
fitting procedure has also been implemented in ORCA and --- in contrast to
Friesner's pseudo-spectral method --- does not need specially optimized grids. 
The basic idea is to remove the grid errors within the basis set
by "fitting" the numerical overlap to the analytical one. Due to its
nature, overlap fitting is supposed to work better with larger basis
sets.

<a id="sec:essentialelements.ri.rijcosx.basicusage"></a>
### Basic Usage

The RIJCOSX approximation can be invoked by the `!RIJCOSX` keyword:

```orca
! HF RIJCOSX 
```

By default, RIJCOSX will make use of the `def2/J` [auxiliary basis set](../essentialelements/basisset.md).
Note that as the requirements for the SCF and correlation fitting bases are
quite different an [correlation auxiliary basis set](../essentialelements/basisset.md) has to be defined additionally.
This is e.g. the case for [RI-MP2](../modelchemistries/MP2.md) or [double-hybrid DFT](sec:modelchemistries.dft.doublehybriddft).

```orca
! RI-MP2 def2-TZVPP def2/J def2-TZVPP/C RIJCOSX
```

!!! note
    This is the default for hybrid DFT! The COSX part can be turned off by using the `!NOCOSX` keyword.

<a id="sec:essentialelements.ri.rijcosx.gradient"></a>
### RIJCOSX Gradient

Given the exchange matrix, the exchange energy is given by (a sum over
spin cases is left out here for simplicity):

$$

E_{\text{X} } =\frac{1}{2}\sum\limits_{\mu \nu } { P_{\mu \nu } K_{\mu \nu } (\mathrm{\mathbf{P} }) }\qquad \text{(eqn:33)}

$$

Previous to ORCA6, the gradient of the COSX contribution to the energy was taken 
as an approximation:

$$

\frac{\partial E_{X} }{\partial \lambda }\approx 2\sum\limits_g
{\sum\limits_{\mu \nu } { \frac{\partial F_{\mu g} }{\partial \lambda } } }
 G_{\nu g}\qquad \text{(eqn:34)}

$$

with

$$

\frac{\partial F_{\mu g} }{\partial \lambda }=w_{g}^{1/2} \sum\limits_\kappa{P_{\kappa \mu } \frac{\partial X_{\mu g} }{\partial \lambda } }\qquad \text{(eqn:35)}

$$

as published in the original implementation paper [neese2009chemphys](../../bibliography.md).

Starting from ORCA6, this was updated to the full derivative of the energy component,
including the derivative of all terms: grid weight derivatives, derivative of the SFitting matrices
and all derivatives of $F$ and $G$ [^a]. The gradient is thus now more accurate and less noisy. In
case one wants to revert to the previous approximated version (not recommended), just set:

[^a]:  The theory is not yet published, but will be soon.

```orca
%method
  cosxgradtype grad_n
  useqgradfit false
end
```

<a id="sec:essentialelements.ri.rijcosx.grids"></a>
### COSX Numerical Grids

For expert users, the grid parameters for the exchange grids can be even
more finely controlled:

```orca
%method
  IntAccX  Acc1, Acc2, Acc3
  GridX    Ang1, Ang2, Ang3
end
```

There are three grids involved: the smallest grid (Acc1, Ang1) that is
used for the initial SCF iterations, the medium grid (Acc2, Ang2) that
is used until the end of the SCF and the largest grid (Acc3, Ang3) that
is used for the final energy and the gradient evaluations. `UseFinalGridX`
can be used to turn this last grid on or off, though changing this is not
generally recommended. More details about the grid constructions can be
found in [sec:essentialelements.numericalintegration](#sec:essentialelements.numericalintegration). 

<a id="sec:essentialelements.ri.rijcosx.sfitting"></a>
### SFitting Parameters

To modify the overlap fitting parameters, the following input can be specified:

```orca
%method
  UseSFitting false   # Same as NoSFitting in the simple input
                      # (Default is true)
  UseQGradFit false   # Uses the SCF fitting matrix for gradient calculations
                      # (Default is true)
end
```

Note that overlap fitting also works for HF and MP2 gradients without
specifying any additional keyword. The `UseQGradFit` parameter uses
the same fitting matrix for the gradients as for the energy calculation and
is the default behavior since ORCA6.

<a id="sec:essentialelements.ri.rijcosx.partialcontraction"></a>
### Partial Contraction Scheme

Since ORCA 5.0, generally-contracted basis sets can be handled efficiently
by using an intermediate partially contracted (pc) atomic-orbital basis
for the exchange-matrix computation without affecting the
results [Helmich-Paris2021a](../../bibliography.md). Depending on the basis set and element
type, computational speedups by many orders of magnitude are possible.
For testing or benchmark purposes, the K matrix computation can be done
in the original basis by using the flag

```orca
%method
  COSX_PartialContraction false   # No intermediate basis for generally contracted shells
                                  # (Default is true)
end
```
<a id="sec:essentialelements.ri.rijcosx.fullsymmetry"></a>
### Restoring Full Symmetry

The semi-numerical integration scheme in the default COSX algorithm
breaks the permutational symmetry of the two-electron integrals.
We have observed that this flaw is often the cause of convergence problems
for iterative algorithms, in particular for multi-reference theories [Helmich-Paris2022](../../bibliography.md).
An input option is available since ORCA 6.0 to preserve the full eight-fold 
permutational symmetry of the two-electron integrals:

```orca
%method
  COSX_IntSymmetry Full      # Fully symmetrized integrals
                   Standard  # Original COSX algorithm
end
```

The full-symmetrization algorithm often improves the numerical stability and is enabled by default for
TRAH-CASSCF and CASSCF linear-response calculations.
However, the full-symmetrization algorithm may come with additional costs that depend on the number of $\mathbf{F}$ intermediates.
The number of $\mathbf{F}$ intermediates depends on the symmetry of the density matrix
(symmetric (S), anti-symmetric (A), and non-symmetric (N))
and whether overlap fitting is employed, as summarized in the table below.

<a id="tab:cosx-full-sym"></a>
!!! note "Number of COSX $\mathbf{F}$ intermediates per density matrix"

    | S fitting                   | P symmetry (S, A, N)                | Number of $\mathbf{F}$ intermediates      |
    |:----------------------------|:------------------------------------|:-------------------------------|
    | No                          | S / A                               | 1                              |
    | No                          | N                                   | 2                              |
    | Yes                         | S / A                               | 2                              |
    | Yes                         | N                                   | 4                              |

Note that for symmetric (S) and anti-symmetric (A) densities, we symmetrize and anti-symmetrize, respectively, 
exchange matrices at the end, which reduces the number of $\mathbf{F}$ intermediates by a factor of 2.
The actual computational costs usually do not increase linearly with the number of $\mathbf{F}$ intermediates
since we compute the costly analytic integrals ($A_{\nu\tau}(\mathbf{r}_g)$) only once and then contract them
with the additional $\mathbf{F}$ intermediates.
From our experience the overhead of the full-symmetrization algorithm
is roughly between 1.2 and 1.5 times that of the original algorithm.

<a id="sec:essentialelements.ri.rijcosx.convergence"></a>
### COSX Grid and Convergence Issues

**Symptoms of convergence issues:** Erratic convergence behavior, often
starting from the first SCF step or possibly setting in at a later
stage, which produce crazy energy values with "megahartree" jumps. If
overlap fitting is on, the following error message may also be
encountered: "Error in Cholesky inversion of numerical overlap".

Convergence issues may arise when the chosen grid has difficulties in
representing the basis set. This is the "grid equivalent" of a linear
dependence problem, as discussed in
[sec:essentialelements.lindep](#sec:essentialelements.lindep). It should also be mentioned
that the grid-related problem discussed here often goes hand in hand
with basis set linear dependence, although not necessarily. The most
straightforward way of dealing with this is to increase the size of the
integration grid. This, however, is not always desirable or possible.

One way to avoid the Cholesky inversion issue is to turn overlap fitting
off (`!NoSFitting`). However, this means that the numerical problems are
still present, but are ignored. Due to the fact that overlap
fitting operates with the numerical overlap and its inverse, it is more
sensitive to linear dependence issues, so turning off the fitting
procedure may lead to convergence. This may be a pragmatic --- but by no
means clean --- solution, since it relies on the assumption that the
numerical errors are small.

On the other hand, overlap fitting also gives a similar tool to deal
with linear dependence issues as the one discussed for basis sets. The
eigenvalues of the numerical overlap can be similarly inspected and
small values screened out. There is unfortunately no universal
way to determine this screening parameter, but see
[sec:essentialelements.lindep](#sec:essentialelements.lindep) for typical values.

The parameters influencing the method used for inversion and obtaining
the fitting matrix are:

```orca
%method
  SFitInvertType Cholesky    # Cholesky inversion (default)
                 Cholesky_Q  # Cholesky + full Q matrix
                 Diag        # Inversion via diagonalization
                 Diag_Q      # Diag + full Q matrix
  SInvThresh     1e-8        # Inversion threshold for Diag and Diag_Q (default 1e-8)
end
```

By default, the inversion procedure proceeds through Cholesky
decomposition as it is the fastest option. Ideally, the overlap matrix is
non-singular if the basis set is not linearly dependent. For
singular matrices, the Cholesky procedure will fail. It should be noted
at this point that the numerical overlap can become linearly dependent
even if the overlap of basis functions is not, and so a separate
parameter will be needed to take care of grid-related issues. To achieve
this, a diagonalization procedure (`Diag`) can be used instead of
Cholesky with the corresponding parameter to screen out eigenvectors
belonging to eigenvalues below a threshold (`SInvThresh`). For both
Cholesky and diagonalization procedures, a "full Q" approach is also
available (`Cholesky_Q` and `Diag_Q`), which corresponds to the use of a
more accurate (untruncated) fitting matrix.

<a id="sec:essentialelements.ri.rijk"></a>
## RI-JK

An alternative algorithm for accelerating the HF exchange in hybrid DFT
or HF calculations is RI-JK developed by Kendall and Früchtl[kendall1997theor](../../bibliography.md).
It will use the RI approximation for both Coulomb and exchange and allows for a fair approximation to the
Hartree-Fock exchange matrix. It can be difficult to make this
approximation highly accurate. It is, however, usefully fast compared to
direct SCF if the molecule is "dense" enough. There are special
auxiliary basis sets for this purpose (see section [sec:essentialelements.basisset](#sec:essentialelements.basisset)).
RI-JK is implemented in ORCA for SCF single point energies but
not for gradients. The speedups for small molecules are better than for 
[RIJCOSX](sec:essentialelements.ri.rijcosx), for medium sized molecules 
(e.g. $(\text{gly})_{4}$) similar, and for larger molecules
RI-JK is less efficient than RIJCOSX. A detailed comparison can be found in 
[sec:essentialelements.ri.speedcomparison](#sec:essentialelements.ri.speedcomparison). The errors of RI-JK are usually
below 1 mEh and the error is very smooth (smoother than for [RIJCOSX](sec:essentialelements.ri.rijcosx)).
Hence, for small calculations with large basis sets, RI-JK is a good
idea, for large calculations on large molecules [RIJCOSX](sec:essentialelements.ri.rijcosx) is better.

!!! note
    *   RI-JK requires a larger auxiliary basis set. For the
        [Karlsruhe basis set](../essentialelements/basisset.md), the universal `def2/JK` and `def2/JKsmall` basis
        sets are available. They are large and accurate.

    *   For UHF RI-JK is roughly twice as expensive as for RHF. This is not
        true for RIJCOSX.

    *   RI-JK is available for conventional and direct runs and also for ANO
        bases. There the conventional mode is recommended.

<a id="sec:essentialelements.ri.rijk.basicusage"></a>
### Basic Usage

The RI-JK approximation can be invoked by the `!RI-JK` keyword:

```orca
! RHF def2/JK RI-JK
```

<a id="sec:essentialelements.ri.speedcomparison"></a>
## Speed Comparison of RIJCOSX and RI-JK

A comparison of the [RIJCOSX](sec:essentialelements.ri.rijcosx) and [RI-JK](sec:essentialelements.ri.rijk) methods is shown in [tab:essentialelements.ri.speedcomparison](#tab:essentialelements.ri.speedcomparison).

<a id="tab:essentialelements.ri.speedcomparison"></a>
!!! note "Comparison of wall clock times in seconds for a full SCF for $\text{(gly)}_{2}$, $\text{(gly)}_{4}$, and $\text{(gly)}_{8}$. Data taken from Ref. [Kossmann2009](../../bibliography.md)"
    |                            |           | **def2-SVP**| **def2-TZVP(-df)**| **def2-TZVPP** | **def2-QZVPP** |
    |:--------------------------:|:---------:|:-----------:|:-----------------:|:--------------:|:--------------:|
    | **$\text{(gly)}_{2}$**     | *Default* | 105         | 319               | 2574           | 27856          |
    |                            |  *RI-JK*  | 44          | 71                | 326            | 3072           |
    |                            | *RIJCOSX* | 70          | 122               | 527            | 3659           |
    | **$\text{(gly)}_{4}$**     | *Default* | 609         | 1917              | 13965          | 161047         |
    |                            |  *RI-JK*  | 333         | 678               | 2746           | 30398          |
    |                            | *RIJCOSX* | 281         | 569               | 2414           | 15383          |
    | **$\text{(gly)}_{8}$**     | *Default* | 3317        | 12505             | 82774          |                |
    |                            |  *RI-JK*  | 3431        | 5452              | 16586          | 117795         |
    |                            | *RIJCOSX* | 1156        | 2219              | 8558           | 56505          |

It is obvious from the data that for small molecules the [RI-JK](sec:essentialelements.ri.rijk)
approximation is the most efficient choice. For $\text{(gly)}_{4}$ this is
already no longer obvious. For up to the def2-TZVPP basis set, [RI-JK](sec:essentialelements.ri.rijk) and
[RIJCOSX](sec:essentialelements.ri.rijcosx) are almost identical and for def2-QZVPP [RIJCOSX](sec:essentialelements.ri.rijcosx) is already a
factor of two faster than [RI-JK](sec:essentialelements.ri.rijk). For large molecules like $\text{(gly)}_{8}$
with small basis sets [RI-JK](sec:essentialelements.ri.rijk) is not a big improvement but for large basis
set it still beats the normal 4-index calculation. [RIJCOSX](sec:essentialelements.ri.rijcosx) on the other
hand is consistently faster. It leads to speedups of around 10 for
def2-TZVPP and up to 50-60 for def2-QZVPP. Here it outperforms [RI-JK](sec:essentialelements.ri.rijk) by,
again, a factor of two.

<a id="sec:essentialelements.ri.keywords"></a>
## Keywords

<a id="tab:essentialelements.ri.keywords.simple"></a>
!!! note "Simple input keywords for the RI approximations."
    | Keyword                         | Description                                                                                                           |
    |:--------------------------------|:----------------------------------------------------------------------------------------------------------------------|
    | `RI`                            | Activates [RI-J](sec:essentialelements.ri.rij) (uses [Split-RI-J](sec:essentialelements.ri.splitrij) by default)      |
    | `NORI`                          | Deactivates RI treaments                                                                                              |
    | `SplitRIJ`, `Split-RI-J`        | Activates [Split-RI-J](sec:essentialelements.ri.splitrij)                                                             |
    | `NoSplitRIJK`, `NoSplit-RI-J`   | Activates [Split-RI-J](sec:essentialelements.ri.splitrij)                                                             |
    | `RIJONX`, `RIJDX`               | Activates [RIJONX](sec:essentialelements.ri.rijonx)                                                                   |
    | `RIJCOSX`, `RIJDX`              | Activates [RIJCOSX](sec:essentialelements.ri.rijcosx)                                                                 |
    | `NORIJCOSX`, `NOCOSX`           | Deactivates RIJCOSX, will activate RIJONX instead                                                                     |
    | `RIJK`, `RI-JK`                 | Activates [RI-JK](sec:essentialelements.ri.rijk)                                                                      |
    | `NoSFitting`                    | Deactivates [SFitting](sec:essentialelements.ri.rijcosx.sfitting)                                                     |

<a id="tab:essentialelements.ri.keywords.block"></a>
!!! note "`%method` block input keywords for the RI approximations."
    | Keyword                         | Options              | Description                                                                      |
    |:--------------------------------|:---------------------|:---------------------------------------------------------------------------------|
    | `RI`                            | `on`/`off`           | Activates/deactivates RI (default: Split-RI-J)                                   |
    | `IntAccX`                       | `<Acc1, Acc2, Acc3>` | Control exchange grid accuracy parameters (cf. [Numerical Integration](sec:essentialelements.numericalintegration.SCFkeys))  |
    | `GridX`                         | `<Ang1, Ang2, Ang3>` | Controls exchange grid parameters (cf. [Numerical Integration](sec:essentialelements.numericalintegration.SCFkeys))  |
    | `UseSFitting`                   | `true`/`false`       | Activates [SFitting](sec:essentialelements.ri.rijcosx.sfitting) (default: true)  |
    | `SFitInvertType`                | `Cholesky`           | Uses Cholesky inversion (default)                                                |
    |                                 | `Cholesky_Q`         | Uses Cholesky + full Q matrix                                                    |
    |                                 | `Diag`               | Activates inversion via diagonalization                                          |
    |                                 | `Diag_Q`             | Activates diagonalization + full Q matrix                                        |
    | `SInvThresh`                    | `<real>`             | Inversion threshold for Diag and Diag_Q (default: 1e-8)                          |
    | `UseQGradFit`                   | `true`/`false`       | Activates SCF fitting matrix for gradient calculations (default: true)           |
    | `COSX_PartialContraction`       | `true`/`false`       | Activates intermediate basis for generally contracted shells (default: true)     |
    | `COSX_IntSymmetry`              | `full`               | Use fully symmetrized integrals                                                  |
    |                                 | `standard`           | Use original COSX algorithm                                                      |

