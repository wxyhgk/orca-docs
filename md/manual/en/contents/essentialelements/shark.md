(sec:essentialelements.shark)=
# The SHARK Integral Package and Task Driver

## Preface

Starting with ORCA 5.0 very large changes have taken place in the way
that the program handles integrals and integral related tasks like
building Fock matrices. SHARK is a powerful and efficient infrastructure
that greatly facilitates the handling of these tasks. This allows
developers to write highly streamlined code with optimal performance and
a high degree of reliability. Compared to the way ORCA handled integrals
before ORCA 5.0, tens of thousands of lines of codes, often duplicated
or nearly duplicated from closely related parts of the program could be
eliminated. From the perspective of the user, the visible changes to the
input and output of the program compared to ORCA 4.2.1 and earlier are
relatively limited. However, under the hood, the changes are vast and
massive and will ensure that ORCA's infrastructure is modern and very
well suited for the future of scientific computing.

The benefits of SHARK for the users of ORCA are:

1.  Improved code efficiency that is consistent through all program
    tasks. In particular, complicated two-electron integrals, for
    example in the context of GIAOs, two-electron spin-orbit coupling
    and two-electron spin-spin coupling integrals are handled with
    vastly improved efficiency. Also, integral digestion has been vastly
    improved with very large benefits for calculations that build many
    Fock matrices at a time, for example in CIS/TD-DFT, analytic
    Hessians or response property calculations.

2.  Improved code reliability, since all integrals now run through a
    well debugged, common interface

3.  Shorter development times. The new infrastructure is so user
    friendly to programmers that writing new code that makes use of
    SHARK is much faster than in the past.

4.  SHARK handles basis sets much better than the old infrastructure.
    Whether the basis sets used follow a segmented contraction, general
    contraction or partial general contraction is immaterial since the
    algorithms have been optimized carefully for each kind of basis
    throughout.

## The SHARK integral algorithm

One cornerstone of SHARK is a new integral algorithm that allows for
highly efficient evaluation of molecular integrals. The algorithm is
based on the beautiful McMurchie-Davidson algorithm which leads to the
following equation for a given two-electron integral:

$$({\mu _A}{\nu _B}|{\kappa _C}{\tau _D}) = C\sum\limits_{tuv} { E_t^{\mu \nu ;x}E_u^{\mu \nu ;y}E_v^{\mu \nu ;z} } \sum\limits_{t'u'v'} { E_{t'}^{\kappa \tau ;x}E_{u'}^{\kappa \tau ;y}E_{v'}^{\kappa \tau ;z}{{( - 1) }^{t' + u' + v'} }{R_{t + t',u + u',v + v'} }}$$

Here

$$C = 8{\pi ^{{\raise0.5ex\hbox{$\scriptstyle 5$}
\kern-0.1em/\kern-0.15em
\lower0.25ex\hbox{$\scriptstyle 2$} }} } = { 139.947346620998902770103}$$

and the primitive Cartesian Gaussian basis functions $\{\mu_A\}$ where
$A$ is the atomic center, where basis function $\mu$ is centered at
position ${{{\mathbf{R} }_A} }$. In order to catch a glimpse of what the
McMurchie-Davidson algorithm is about, consider two unnormalized,
primitive Gaussians centered at atoms $A$ and $B$, respectively:

$$\begin{aligned}
{ G_A} &= x_A^iy_A^jz_A^k\exp ( - \alpha R_A^2) \\
  { G_B} &= x_B^{i'}y_B^{j'}z_B^{k'}\exp ( - \beta R_B^2)\end{aligned}$$

By means of the Gaussian product theorem, the two exponentials are
straightforwardly rewritten as:

$$\exp ( - \alpha R_A^2)\exp ( - \beta R_B^2) = { K_{AB} }\exp\Bigl( - (\alpha  + \beta)r_P^2\Bigr)$$

With

$${K_{AB} } = \exp\left( - { \textstyle{{\alpha \beta } \over{ \alpha  + \beta } }}{\left|{ {{\mathbf{R} }_A} - { {\mathbf{R} }_B} } \right|^2}\right)$$

$r_P^2 = { \left|{ {\mathbf{r} } - { {\mathbf{R} }_P} } \right|^2}$ is
the electronic position relative to the point

$${{\mathbf{R} }_P} = { \textstyle{\alpha  \over{ \alpha  + \beta } }}{{\mathbf{R} }_A} + { \textstyle{\beta  \over{ \alpha  + \beta } }}{{\mathbf{R} }_B}$$

at which the new Gaussian is centered. The ingenious invention of
McMurchie and Davidson was to realize that the complicated polynomial
that arises from multiplying the two primitive Cartesian Gaussians can
be nicely written in terms of Hermite polynomials
$\left\{\Lambda  \right\}$. In one dimension:

$$x_A^ix_B^{i'} = \sum\limits_{t = 0}^{i + i'} { {E_t} }$$

And hence:

$${G_A}{G_B} = { K_{AB} }\sum\limits_{t = 0}^{i + i'} { E_t^{AB} } \sum\limits_{u = 0}^{j + j'} { E_u^{AB} } \sum\limits_{v = 0}^{k + k'} { E_v^{AB}\Lambda _{tuv}^{AB} }$$

With

$$\Lambda _{tuv}^{AB} = { \left({ {\partial  \over{ \partial{ X_P} }} } \right)^{\!\!t} }{\left({ {\partial  \over{ \partial{ Y_P} }} } \right)^{\!\!u} }{\left({ {\partial  \over{ \partial{ Z_P} }} } \right)^{\!\!v} }\exp\Bigl( - (\alpha  + \beta )R_P^2\Bigr)$$

This means that the original four center integral is reduced to a sum of
two-center integrals over Hermite Gaussian functions. These integrals
are denoted as

$${R_{t + t',u + u',v + v'} } = \int{ \int{ \Lambda _{tuv}^{AB}({{\mathbf{r} }_1};{{\mathbf{R} }_P})\Lambda _{t'u'v'}^{CD}({{\mathbf{r} }_2};{{\mathbf{R} }_Q})r_{12}^{ - 1}d{{\mathbf{r} }_1}d{{\mathbf{r} }_2} } }$$

With these definitions one understands the McMurchie Davidson algorithm
as consisting of three steps:

1.  Transformation of the Bra function product into the Hermite Gaussian
    Basis

2.  Transformation of the Ket function product into the Hermite Gaussian
    Basis

3.  Calculation of the Hermite Gaussian electron repulsion integral

SHARK is the realization that these three steps can be efficiently
executed by a triple matrix product:

$$({\mu _A}{\nu _B}|{\kappa _C}{\tau _D}) = { \left({ {{\mathbf{E} }^\text{bra} }{\mathbf{R} }{{\mathbf{E} }^\text{ket} }} \right)_{\mu \nu ,\kappa \tau } }$$

Here ${{{\mathbf{E} }^\text{bra} }}$ and ${{{\mathbf{E} }^\text{ket} }}$
collect the $E$ coefficients for all members of the shell product on the
bra and ket side ($E_{\mu \nu ,tuv}^\text{bra}$ and
$E_{\kappa\tau,tuv}^\text{ket}$), respectively, and ${\mathbf{R} }$
collects the integrals over Hermite Gaussian functions
(${R_{tuv,t'u'v'} }$).

There are many benefits to this formulation:

1.  The integral is factorized allowing steps to be performed
    independent of each other. For example, the E matrices can be
    calculated at the beginning of the calculation and reused whenever
    needed. Their storage is unproblematic

2.  Matrix multiplications lead to extremely efficient formation of the
    target integrals and drive the hardware at peak performance

3.  Steps like contraction of primitive integrals and transformation
    from the Cartesian to the spherical Harmonics basis can be folded
    into the definition of the E matrices thus leading to extremely
    efficient code with next to no overhead creates by short loops.

4.  Programming integrals becomes very easy and efficient. Other types
    of integrals as well as derivative integrals are readily approached
    in the same way. Also, two- and three-index repulsion integrals, as
    needed for the RI approximation are also readily formulated in this
    way.

5.  One-electron integrals are equally readily done with this approach.

There is a very large number of technicalities that we will not describe
in this manual which is only intended to provide the gist of the
algorithm.

## SHARK and libint

Up to ORCA 4.2.1, ORCA has almost entirely relied on the libint2
integral library which is known to be very efficient and powerful.
Starting from ORCA 5.0, both SHARK and libint are used for integral
evaluations and libint is fully integrated into the SHARK programming
environment. Integrals that are only available in one of the packages
are done with this package (e. g. GIAO, SOC and Spin-Spin integrals in
SHARK; F12 or second derivative integrals in libint). For the integrals
available in both packages, the program makes a judicious choice about
the most efficient route. The reason for this hybrid approach is the
following:

The SHARK integral algorithm is at its best for higher angular momentum
functions ($l>2$; $d$-functions) which is where the efficiency of the
matrix multiplications leads to very large computational benefits.
Integrals over, say, four $f$- or $g$-functions perform much faster (up
to a factor of five) than with traditional integral algorithms. However,
for low angular momenta, there is overhead created by the matrix
multiplications and also by the fact that the McMurchie Davidson
algorithm is known to not be the most FLOP count efficient algorithm. To
some extent, this is take care of by using highly streamlined routines
for low angular momenta that perform extremely well. However, there are
penalties for intermediate angular momenta, where the efficiency of the
matrix multiplications has not set in and the integrals are too
complicated for hand coding. These integrals perform best with libint
and consequently, the program will, by default, select libint to perform
such integral batches.

## Basis set types

One significant aspect of molecular integral evaluation is the type of
contraction that is present in a Gaussian basis set. The most general
type of basis set is met in the "general contraction" scheme. Here all
primitive Gaussian basis functions of a given angular momentum are
collected in a vector $\left\{\phi  \right\}$. In general, all
primitives will contribute to all basis functions
$\left\{\varphi  \right\}$ of this same angular momentum. Hence, we can
write:

$$\left(\begin{array}{l}
          \varphi_1 \\
          \varphi_2 \\
          ~\vdots \\
          \varphi_{{N_l} }
        \end{array}\right) =
  \left(\begin{array}{llll}{ {d_{11} }} & { {d_{11} }} &  \cdots  & { {d_{1{M_l} }} }  \\
   { {d_{21} }} & { {d_{21} }} &  \cdots  & { {d_{2{M_l} }} }  \\
    ~\vdots  &  ~\vdots  &  \ddots  &  ~\vdots   \\
   { {d_{{N_l}1} }} & { {d_{{N_l}2} }} &  \cdots  & { {d_{{N_l}{M_l} }} }
        \end{array}\right)        \left(\begin{array}{l}
          \phi_1 \\
          \phi_2 \\
          ~\vdots \\
          \phi_{{M_l} }
        \end{array}\right)$$

Where ${N_l}$ and ${M_l}$ are the number of actual basis functions and
primitives respectively. Typically, the number of primitives is much
larger than the number of basis functions. The matrix ${\mathbf{d} }$
collects the contraction coefficients for each angular momentum. Typical
basis sets that follow this contraction pattern are atomic natural
orbital (ANO) basis sets. They are typically based on large primitive
sets of Gaussians. Such basis sets put very demands on the integral
package since there are many integrals over primitive Gaussian basis
functions that need to be generated. If the integral package does not
take advantage of the general contraction, then this integral evaluation
will be highly redundant since identical integrals will be calculated
${N_l}$ times (and hence, integrals over four generally contracted
shells will be redundantly generated ${N_l^4}$ times). SHARK takes full
advantage of general contraction for all one- and two-electron integrals
that it can generate. Here, the unique advantages of the integral
factorization come to full benefit since all integral quadruples of a
given atom quadruple/angular momentum quadruple can be efficiently
generated by just two large matrix multiplications.

The opposite of general contraction is met with segmented contraction.
Here each basis function involves a number of primitives:

$${\varphi _\mu } = \sum\limits_k { {d_{k\mu } }{\phi _k} }$$

Quite typically, none of the ${{\phi _k} }$ that occur in the
contraction of one basis functions occurs in any other basis function.
Typical basis sets of this form are the "def2" basis sets of the
Karlsruhe group. They are readily handled by most integral packages and
both SHARK and libint are efficient in this case.

The third class of basis sets is met, when general contraction is
combined with segmented contraction. Basis sets of this type are, for
example, the correlation consistent (cc) basis sets. We call such basis
sets "partially generally contracted". In such basis sets, part of the
basis functions are generally contracted (for example, the s- and
p-functions in main group elements), while other basis functions (e. g.
polarization functions, diffuse functions, core correlation functions)
are not generally contracted. It is difficult to take full advantage of
such basis sets given their complicated structure. In ORCA 5, special
code has been provided that transforms the basis set into an
intermediate basis set that does not contain any redundancies and hence
drives SHARK or libint at peak performance.

In assessing the efficiency vs the accuracy of different integral
algorithms, it is clear that segmented basis sets lead to the highest
possible efficiency if they are well constructed. For such basis set the
pre-screening that is an essential step of any integral direct algorithm
performs best. The highest possible accuracy (per basis functions) is
met with generally contracted basis sets. However, here the
pre-screening becomes rather inefficient since it can only be performed
at the level of atom/angular momentum combinations rather than
individual shell quadruples. Thus, as soon as a given atom/angular
momentum combination leads to any non-negligible integral, all integrals
for this combination need to be calculated. This created a sizeable
overhead. Consequently, SCF calculations can never be as efficient as
with segmented basis sets. If this is immaterial, for example, because a
subsequent coupled cluster or MRCI calculation is dominating the
calculation time, general contraction is very worthwhile to be explored.
For partial general contraction, our algorithm performs very nearly as
efficiently as for segmented contraction in SCF calculations. However,
since the intermediate basis set is larger than the original orbital
basis, certain limited performance penalties can arise in some job
types.

## Task drivers

In traditional algorithms, quantum chemical programs frequently contain
many instances of nested loops over basis function shells, the integral
package is called and the integrals are "digested" for a given task.
While these steps are inevitable, programming them repeatedly is
laborious and error prone. In addition, improvements, say in the
handling of contractions or symmetry, need to implemented in many
different places. In the SHARK infrastructure all of this is unnecessary
since it is programmed in an object-oriented fashion, where the
programmer does not need to take care of any detail. Hence, developers
only need to write short code sections that distribute the generated
integrals into whatever data structure they need, while the SHARK
interface takes care of all technical aspects and triggers the
sophisticated and efficient machinery that underlies it.

Given this situation, the future of ORCA will involve SHARK taking care
of nearly of the compute intensive, laborious tasks, while ORCA will
organize and trigger all of these tasks. ORCA and SHARK communicate via
a lean and well-defined interface to exchange the necessary data. In
this way, a modern, efficient, easy to use and readily maintainable
development environment is created.

(sec:essentialelements.shark.keywords)=
## SHARK User Interface

While SHARK is a large and complicated machinery, we have deliberately
kept the interface as straightforward and simple as possible. 

In the simple input line there are keywords to turn SHARK on (default) or off:

```orca
! UseShark
! NoUseShark
```

:::{deprecated} 6.0.0
The legacy (non-SHARK code) was removed from the program,
so SHARK can no longer be disabled in calculations, which require integrals
(as opposed to MM calculations, for example).
:::

Further, there are a few flags that can be set in the `%shark` block:

```orca
%shark
 UseGeneralContraction false  # turns general contraction algorithm on or
                              # off. There normally is no need to set this
                              # flag since the program will find the
                              # contraction case automatically
 Printlevel 1                 # Amount of output generated. Choose 0 to
                              # suppress output and 2 for more output.
                              # Everything else is debug level printing and
                              # will fill your harddrive very quickly with
                              # unusable information
 PartialGCFlag -1             # Let the program decide whether to use PGC
                0             # do not use it
                1             # Enforce PGC (even for ANO bases)
 FockFlag SHARK_libint_hybrid # default: best of both worlds
          force_shark         # Force Shark where possible
          force_libint        # Force libint where possible
 RIJFlag  RIJ_Auto            # default: program decides the best way
          Split_rij           # new SHARK Split-RI-J algorithm
          Split_rij_2003      # Highly efficient re-implementation of the
                              # Original 2003 algorithm. Mostly used!
          rij_regular         # Use traditional 3 center integrals
                              # (not recommended)
end
```