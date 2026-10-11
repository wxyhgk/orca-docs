

<a id="sec:structurereactivity.optimization"></a>
# Geometry Optimizations

ORCA is able to calculate equilibrium structures (minima and transition
states) using the quasi Newton update procedure with the well known BFGS
update
[schlegel1987ab,schlegel1995modern,schlegel1998encyclopedia,eckert1997comp,horn1991comp,baker1986comp](../../bibliography.md),
the Powell or the Bofill update. The optimization can be carried out in
either redundant internal (recommended in most cases) or Cartesian
displacement coordinates. As initial Hessian the user can choose between
a diagonal initial Hessian, several model Hessians (Swart, Lindh,
Almloef, Schlegel), an exact Hessian and a partially exact Hessian (both
recommended for transition state optimization) for both coordinate
types. In redundant internal coordinates several options for the type of
step to be taken exist. The user can define constraints via two
different paths. He can either define them directly (as bond length,
angle, dihedral or Cartesian constraints) or he can define several
fragments and constrain the fragments internally and with respect to
other fragments. The ORCA optimizer can be used as an external
optimizer, i.e.the energy and gradient calculations done by ORCA.

The usage of analytic gradients is necessary for efficient geometry
optimization. In ORCA 5.0, the following methods provide analytic first
derivatives

-   Hartree-Fock (HF) and DFT (including the RI, RIJK and RIJCOSX
    approximations)

-   MP2, RI-MP2 and DLPNO-MP2

-   TD-DFT for excited states

-   CAS-SCF

When the analytic gradients are not available, it is possible to
evaluate the first derivatives numerically by finite displacements. This
is available for all methods.

<!-- The coordinate system chosen for geometry optimization affects the
convergence rate, with redundant internal coordinates being usually the
best choice. -->

Some methods for locating transition states (TS) require second
derivative matrices (Hessian), implemented analytically for HF, DFT and
MP2. Additionally, several approaches to construct an initial
approximate Hessian for TS optimization are available. A very useful
feature for locating complicated TSs is the Nudged-Elastic Band method
in combination with the TS finding algorithm (NEB-TS, ZOOM-NEB-TS). An
essential feature for chemical processes involving excited states is the
conical intersection optimizer. Another interesting feature are MECP
(Minimum Energy Crossing Point) optimizations.

For very large systems ORCA provides a very efficient L-BFGS optimizer,
which makes use of the orca_md module. It can also be invoked via simple
keywords described at the end of this section.

<a id="sec:structurereactivity.optimization.geometry"></a>
## Basic Usage

The use of the geometry optimization module is relatively
straightforward.[^1] Here are some typical examples:

```
! BLYP SVP Opt
* int 0 1
    C  0 0 0 0.0000   0.000    0.00
    O  1 0 0 1.2029   0.000    0.00
    H  1 2 0 1.1075 122.016    0.00
    H  1 2 3 1.1075 122.016  180.00
*
```
ORCA employs the [RIJ](../essentialelements/RI.md) by default. If this is not wanted, RI can be deactivated generally by using the `!NORI`
keyword.

An optimization of the first excited state of ethylene:

```mol
title: structure 1
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
6
structure (0 1)
C      0.000000     0.000000     0.666723
C      0.000000     0.000000    -0.666723
H      0.000000    -0.928802     1.141480
H     -0.804366    -0.464401    -1.341480
H      0.000000     0.928802     1.241480
H      0.804366     0.464401    -1.241480
--- input ---
! BLYP SVP OPT

%tddft
   IRoot 1  
end
  
* xyz 0 1
 C     0.000000     0.000000     0.666723
 C     0.000000     0.000000    -0.666723
 H     0.000000    -0.928802     1.141480
 H    -0.804366    -0.464401    -1.341480
 H     0.000000     0.928802     1.241480
 H     0.804366     0.464401    -1.241480
*
```

### Geometry Optimization Thresholds

The convergence thresholds for geometry optimizations can generally be controlled via the `%geom` block (see [optimization.keywords](#sec:structurereactivity.optimization.keywords)). For convenience, ORCA offers some simple input keywords to choose reasonable sets of thresholds. The respective keywords are `!LooseOpt`,  `!OPT` (default), `!TightOpt`, and `!VeryTightOpt`. The tolerance settings toggled by these keywords are summarized in [tab:structurereactivity.optimization.thresholds](#tab:structurereactivity.optimization.thresholds). Individual keywords and more options to control the optimization thresholds can be found in [tab:structurereactivity.optimization.keywords.geom](#tab:structurereactivity.optimization.keywords.geom).

<a id="tab:structurereactivity.optimization.thresholds"></a>
!!! note "Thresholds for geometry optimization convergence keywords."


| | **Value** | Comment |
| --- | --- | --- |
| **Variable** | Value | Comment |
| ***Loose* (`!LooseOpt`/`Convergence loose`)** |  |  |
| **`TolE`** | 3e-5 | Max. allowed energy change in a.u. |
| **`TolMaxG`** | 2e-3 | Max. allowed gradient component in a.u. |
| **`TolRMSG`** | 5e-4 | Max. allowed RMS gradient in a.u. |
| **`TolMaxD`** | 1e-2 | Max. allowed displacement in a.u. |
| **`TolRMSD`** | 7e-3 | Max. allowed RMS displacement in a.u. |
| ***Normal* (`!Opt`/`Convergence normal`)** |  |  |
| **`TolE`** | 5e-6 | Max. allowed energy change in a.u. |
| **`TolMaxG`** | 3e-4 | Max. allowed gradient component in a.u. |
| **`TolRMSG`** | 1e-4 | Max. allowed RMS gradient in a.u. |
| **`TolMaxD`** | 4e-3 | Max. allowed displacement in a.u. |
| **`TolRMSD`** | 2e-3 | Max. allowed RMS displacement in a.u. |
| ***Tight* (`!TightOpt`/`Convergence tight`)** |  |  |
| **`TolE`** | 1e-6 | Max. allowed energy change in a.u. |
| **`TolMaxG`** | 1e-4 | Max. allowed gradient component in a.u. |
| **`TolRMSG`** | 3e-5 | Max. allowed RMS gradient in a.u. |
| **`TolMaxD`** | 1e-3 | Max. allowed displacement in a.u. |
| **`TolRMSD`** | 6e-4 | Max. allowed RMS displacement in a.u. |
| ***VeryTight* (`!VeryTightOpt`/`Convergence verytight`)** |  |  |
| **`TolE`** | 2e-7 | Max. allowed energy change in a.u. |
| **`TolMaxG`** | 3e-5 | Max. allowed gradient component in a.u. |
| **`TolRMSG`** | 8e-6 | Max. allowed RMS gradient in a.u. |
| **`TolMaxD`** | 2e-4 | Max. allowed displacement in a.u. |
| **`TolRMSD`** | 1e-4 | Max. allowed RMS displacement in a.u. |

<a id="sec:structurereactivity.optimization.hessian"></a>
## Initial Hessian for Minimization

The convergence of a geometry optimization crucially depends on the
quality of the initial Hessian. In the simplest case it is taken as a
unit matrix (in redundant internal coordinates we use 0.5 for bonds, 0.2
for angles and 0.1 for dihedrals and improper torsions). However, simple
model force-fields like the ones proposed by Schlegel, Lindh, Swart or
Almlöf are available and lead to much better convergence. The different
guess Hessians can be set via the `InHess` option which can be either
`unit`, `Almloef`, `Lindh`, `Swart` or `Schlegel` in redundant internal
coordinates, furhter shown in the keywords list found within Section [optimization.keywords](#sec:structurereactivity.optimization.keywords). Since version 2.5.30, these model force-fields (built up in
internal coordinates) can also be used in optimizations in Cartesian
coordinates.

For minimizations we recommend the `Almloef` Hessian, which is the
default for minimizations. The `Lindh` and `Schlegel` Hessian yield a
similar convergence behaviour. There is also the
option for the `Swart` model Hessian, which is less parametrized and
should improve for weakly interacting and/or unusual structures. Of
course the best Hessian is the exact one. `Read` may be used to input an
exact Hessian or one that has been calculated at a lower level of theory
(or a "faster" level of theory). From version 2.5.30 on this option is
also available in redundant internal coordinates. But we have to point
out that the use of the exact Hessian as initial one is only of little
help, since in these cases the convergence is usually only slightly
faster, while at the same time much more time is spent in the
calculation of the initial Hessian.

To sum it up: we advise to use one of the simple model force-fields for
minimizations.

<a id="sec:structurereactivity.optimization.coords"></a>
## Coordinate Systems for Optimizations

The coordinate system for the optimization can be chosen by the
`coordsys` variable that can be set to `cartesian` or `redundant`within
the `%geom` block. The default is the redundant internal coordinate
system. If the optimization with `redundant` fails, you can still try
`cartesian`. If the optimization is then carried out in Cartesian
displacement coordinates with a simple model force-field Hessian, the
convergence will be only slightly slower. With a unit matrix initial
Hessian very slow convergence will result.

A compound job `two_step_opt.inp` that first computes a semi-empirical 
Hessian to start from is shown below:

```orca
! BLYP SVP Opt
* int 0 1
    C  0 0 0 0.0000   0.000    0.00
    O  1 0 0 1.2029   0.000    0.00
    H  1 2 0 1.1075 122.016    0.00
    H  1 2 3 1.1075 122.016  180.00
*
```

!!! note

    -   For transition metal complexes MNDO, AM1 or PM3 Hessians are not
        available. You can use ZINDO/1 or NDDO/1 Hessians instead. They are
        of lower quality than MNDO, AM1 or PM3 for organic molecules but
        they are still far better than the standard unit matrix choice.

    -   If the quality of the initial semi-empirical Hessian is not
        sufficient you may use a "quick" RI-DFT job (e.g.
        `BP def2-sv(p) defgrid1`)

    -   In semi-empirical geometry optimizations on larger molecules or in
        general when the molecules become larger the redundant internal
        space may become large and the relaxation step may take a
        significant fraction of the total computing time.

For condensed molecular systems and folded molecules (e.g. a U-shaped
carbon chain) atoms can get very close in space, while they are distant
in terms of number of bonds connecting them. As damping of optimization
steps in internal coordinates might not work well for these cases,
convergence can slow down. ORCA's automatic internal coordinate
generation takes care of this problem by assigning bonds to atom pairs
that are close in real space, but distant in terms of number of bonds
connecting them. See keywords `AddExtraBonds`, `AddExtraBonds_MaxLength`, and `AddExtraBonds_MaxDist` within the keyword list found in Section [optimization.keywords](#sec:structurereactivity.optimization.keywords).

For solid systems modeled as embedded solids the automatically generated
set of internal coordinates might become very large, rendering the
computing time spent in the optimization routine unnecessarily large.
Usually, in such calculations the cartesian positions of outer atoms,
coreless ECPs and point charges are constrained during the
optimization - thus most of their internal coordinates are not needed.
By requesting `ReduceRedInts true` within the `%geom` block only the required needed internal coordinates (of the constrained atoms)
are generated.

OBS: If the step in `redundant` fails badly and only Cartesian
constrains are set (or no constrains), ORCA will fallback to a
`cartesian` step automatically. This can be turned off by setting
CARTFALLBACK to FALSE.

<a id="sec:structurereactivity.geomopt.redundantinternal"></a>
### Redundant Internal Coordinates

There are three types of internal coordinates: redundant internals, old
redundant internals (redundant_old) and a new set of redundant internals
(redundant_new, with improved internals for nonbonded systems). All
three sets work with the same "primitive" space of internal coordinates
(stretches, bends, dihedral angles and improper torsions). Only the
redundant internals works with one more type of bends in cases where a
normal bend would have been approximately 180$^{\circ}$. In redundant
internal coordinates the full primitive set is kept and the Hessian and
gradient are transformed into this -- potentially large -- space. A
geometry optimization step requires, depending on the method used for
the geometry update, perhaps a diagonalization or inversion of the
Hessian of dimension equal to the number of variables in the
optimization. In redundant internal coordinates this space may be 2-4
times larger than the nonredundant subspace which is of dimension
3$N_{\mathrm{atoms} }-6(5)$. Since the diagonalization or inversion
scales cubically the computational overhead over nonredundant spaces may
easily reach a factor of 8--64. Thus, in redundant internal coordinates
there are many unnecessary steps which may take some real time if the
number of primitive internals is greater than 2000 or so (which is not
so unusual). The timing problem may become acute in semiempirical
calculations where the energy and gradient evaluations are cheap.

We briefly outline the theoretical background which is not difficult to
understand:

Suppose, we have a set of $n_{I}$ (redundant) primitive internal
coordinates $\mathrm{q }$ constructed by some recipe and a set
of $n_{C}=3N_{\mathrm{atoms} }$ Cartesian coordinates $\mathrm{x }$. The
B-matrix is defined as:

<a id="eqn:183"></a>

$$
B_{ij} =\frac{\partial q_{i} }{\partial x_{j} }\qquad \text{(eqn:183)}
$$

This matrix is rectangular. In order to compute the internal gradient
one needs to compute the "generalized inverse" of
$\mathrm{B }$. However, since the set of primitive internals is
redundant the matrix is rank-deficient and one has to be careful. In
practice one first computes the $n_{I} \times n_{I}$ matrix
$\mathrm{G }$:

<a id="eqn:184"></a>

$$
\mathrm{G } = \mathrm{BB }^{T}\qquad \text{(eqn:184)}
$$

The generalized inverse of $\mathrm{G }$ is denoted
$\mathrm{G }^{-}$ and is defined in terms of the eigenvalues
and eigenvectors of $\mathrm{G }$:

<a id="eqn:185"></a>

$$
\mathrm{G }^{-}=
\begin{pmatrix}
U \\
R
\end{pmatrix}^{T}
\begin{pmatrix}
\Lambda^{-1} & 0 \\
0 & 0
\end{pmatrix}
\begin{pmatrix}
    U\\
    R
\end{pmatrix}\qquad \text{(eqn:185)}
$$

Here $\mathrm{U }$ are the eigenvectors belonging to the
nonzero eigenvalues $\mathrm{\Lambda}$ which span the
nonredundant space and $\mathrm{R }$ are the eigenvectors of
the redundant subspace of the primitive internal space. If the set of
primitive internals is carefully chosen, then there are exactly
3$N_{\mathrm{atoms} }-6(5)$ nonzero eigenvalues of
$\mathrm{G }$. Using this matrix, the gradient in internal
coordinates can be readily computed from the (known) Cartesian gradient:

<a id="eqn:186"></a>

$$
\mathrm{g }_{q} =\mathrm{G }^{-} \mathrm{Bg }_{x}\qquad \text{(eqn:186)}
$$

The initial Hessian is formed directly in the redundant internal space
and then itself or its inverse is updated during the geometry
optimization.

Before generating the Newton step we have to ensure that the
displacements take place only in the nonredundant part of the internal
coordinate space. For this purpose a projector ${P}'$:

<a id="eqn:187"></a>

$$
{P}'=GG^{-}=G^{-}G\qquad \text{(eqn:187)}
$$

is applied on both the gradient and the Hessian:

<a id="eqn:188"></a>

$$
\tilde{g}_{q} = { P}'g_{q} \qquad \text{(eqn:188)}
$$

<a id="eqn:189"></a>

$$
\tilde{H}_{q} = { P}'H_{q} { P}'+\alpha \left({ 1-{P}' } \right)\qquad \text{(eqn:189)}
$$

The second term for $\tilde{{H} }$ sets the matrix elements of the
redundant part of the internal coordinate space to very large values
($\alpha =1000)$.

### Coordinate Steps

A Quasi-Newton (QN) step is the simplest choice to update the
coordinates and is given by:

<a id="eqn:190"></a>

$$
\Delta q = -\tilde{H}_{q}^{-1}\tilde{g}_{q} \qquad \text{(eqn:190)}
$$

A more sophisticated step is the rational function optimization step
which proceeds by diagonalizing the augmented Hessian:

<a id="eqn:191"></a>

$$
\begin{pmatrix}
H_{q} & g_{q}\\
g_{q} & 0
\end{pmatrix}
\begin{pmatrix}
\Delta q \\
 1
\end{pmatrix}
= v
\begin{pmatrix}
\Delta q \\
 1
\end{pmatrix}\qquad \text{(eqn:191)}
$$

The lowest eigenvalue $\nu_{0}$ approaches zero as the equilibrium
geometry is approached and the nice side effect of the optimization is a
step size control. Towards convergence, the RFO step is approaching the
quasi-Newton step and before it leads to a damped step is taken. In any
case, each individual element of $\Delta \mathrm{q }$ is
restricted to magnitude `MaxStep` and the total length of the step is
restricted to `Trust`. In the RFO case, this is achieved by minimizing
the predicted energy on the hypersphere of radius `Trust` which also
modifies the direction of the step while in the quasi-Newton step, the
step vector is simply scaled down.

Thus, the new geometry is given by:

<a id="eqn:192"></a>

$$
\mathrm{q }_{\text{new} } =\mathrm{q }_{\text{old} } +\Delta \mathrm{q }\qquad \text{(eqn:192)}
$$

However, which Cartesian coordinates belong to the new redundant
internal set? This is a somewhat complicated problem since the relation
between internals and Cartesians is very nonlinear and the step in
internal coordinates is not infinitesimal. Thus, an iterative procedure
is taken to update the Cartesian coordinates. First of all consider the
first (linear) step:

<a id="eqn:193"></a>

$$
\Delta \mathrm{x }=\mathrm{A }\Delta \mathrm{q }\qquad \text{(eqn:193)}
$$

with
$\mathrm{A }=\mathrm{B }^{T}\mathrm{G }^{-}$.
With the new Cartesian coordinates
$\mathrm{x }_{k+1} =\mathrm{x }_{k} +\Delta \mathrm{x }$
a trial set of internals $\mathrm{q }_{k+1}$ can be computed.
This new set should ideally coincide with
$\mathrm{q }_{\text{new} }$ but in fact it usually will not.
Thus, one can refine the Cartesian step by forming

<a id="eqn:194"></a>

$$
\Delta \Delta \mathrm{q }=\mathrm{q }_{\text{new} } -\mathrm{q }_{k+1}\qquad \text{(eqn:194)}
$$

which should approach zero. This leads to a new set of Cartesians
$\Delta\mathrm{x'}=\mathrm{A }\Delta \Delta \mathrm{q }$
which in turn leads to a new set of internals and the procedure is
iterated until the Cartesians do not change and the output internals
equal $\mathrm{q }_{new}$ within a given tolerance (10$^{-7}$
RMS deviation in both quantities is imposed in ORCA).

<a id="sec:structurereactivity.geomopt.constrained"></a>
### Constrained Optimization

Constraints on the redundant internal coordinates can be imposed by
modifying the above projector ${P}'$ with a projector for the
constraints $C$:

<a id="eqn:197"></a>

$$
P={P}'-{P}'C\left({ CPC }
\right)^{-1 }C{P}'\qquad \text{(eqn:197)}
$$

$C$ is a diagonal matrix with 1's for the constraints and 0's elsewhere.
The gradient and the Hessian are projected with the modified projector:

<a id="eqn:198"></a>

$$
\tilde{{g} }_{q} =Pg_{q}\qquad \text{(eqn:198)}
$$

<a id="eqn:199"></a>

$$
\tilde{{H} }_{q} =PH_{q} P+\alpha \left({ 1-P} \right)\qquad \text{(eqn:199)}
$$

<a id="sec:structurereactivity.optimization.constrained"></a>
#### Running Constrained Optimizations - Examples

You can perform constrained optimizations which can, at times, be
extremely helpful. This works as shown in the following example:

```mol
title: structure 2
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
6
structure (0 1)
C      0.000000     0.000000     0.666723
C      0.000000     0.000000    -0.666723
H      0.000000    -0.928802     1.141480
H     -0.804366    -0.464401    -1.341480
H      0.000000     0.928802     1.241480
H      0.804366     0.464401    -1.241480
--- input ---
! BLYP SVP OPT

%tddft
   IRoot 1  
end
  
* xyz 0 1
 C     0.000000     0.000000     0.666723
 C     0.000000     0.000000    -0.666723
 H     0.000000    -0.928802     1.141480
 H    -0.804366    -0.464401    -1.341480
 H     0.000000     0.928802     1.241480
 H     0.804366     0.464401    -1.241480
*
```

```orca
Constraining bond distances        :   { B N1 N2 value C }
Constraining bond angles           :   { A N1 N2 N1 value C }
Constraining dihedral angles       :   { D N1 N2 N3 N4 value C }
Constraining cartesian coordinates :   { C N1 C }
Constraining only X-coordinates    :   { X N1 C }
Constraining only Y-coordinates    :   { Y N1 C }
Constraining only Z-coordinates    :   { Z N1 C }
```

!!! note
    -   Like for normal optimizations you can use numerical gradients (see
        [essentialelements.numericalgradients](../essentialelements/numericalgradients.md#sec:essentialelements.numericalgradients).) for constrained
        optimizations. In this case the numerical gradient will be evaluated
        only for non-constrained coordinates, saving a lot of computational
        effort, if a large part of the structure is constrained.

    -   "value" in the constraint input is optional. If you do not give a
        value, the present value in the structure is constrained. For
        cartesian constraints you can't give a value, but always the initial
        position is constrained.

    -   It is recommended to use a value not too far away from your initial
        structure.

    -   It is possible to constrain whole sets of coordinates:

```orca
all bond lengths where N1 is involved       : { B N1 * C}
all bond lengths                            : { B * * C}
all bond angles where N2 is the central atom: { A * N2 * C }
all bond angles                             : { A * * * C }
all dihedral angles with central bond N2-N3 : { D * N2 N3 * C }
all dihedral angles                         : { D * * * * C }
```

-   For Cartesian constraints (full or X/Y/Z-only) lists of atoms can be defined:

```orca
a list of atoms (10 to 17) with Cartesian constraints  : { C 10:17 C}
a list of atoms (0 to 5) with Cartesian Y constraints  : { Y 0:5 C}
```

-   If there are only a few coordinates that have to be optimized you
    can use the `invertConstraints` option:

```orca
%geom Constraints
        { B 0 1 C }
        end
      invertConstraints true # only the C-O distance is optimized
                             # does not affect Cartesian coordinates
      end
```

-   In some cases it is advantageous to optimize only the positions of
    the hydrogen atoms and let the remaining molecule skeleton fixed:

```orca
%geom optimizehydrogens true
      end
```

!!! note
    -   In the special case of a fragment optimization (see next point) the
        `optimizehydrogens` keyword does not fix the heteroatoms, but
        ensures that all hydrogen positions are relaxed.

    -   In Cartesian optimization, only Cartesian constraints are allowed.

<a id="sec:structurereactivity.geomopt.constrainedfragment"></a>
### Constrained Fragments and Molecular Cluster Optimization

The constrained fragments option was implemented in order to provide a
convenient way to handle constraints for systems consisting of several
molecules. The difference to a common optimization lies in the
coordinate setup. In a common coordinate setup the internal coordinates
are built up as described in the following:

In a first step, bonds are constructed between atom pairs which fulfill
certain (atom type specific) distance criteria. If there are fragments
in the system, which are not connected to each other (this is the case
when there are two or more separate molecules), an additional bond is
assigned to the nearest atom pair between the nonbonded fragments. All
other internal coordinates are constructed on the basis of this set of
bonds. Here, in a second step, bond angles are constructed between the
atoms of directly neighboured bonds. If such an angle reaches more than
175$^{\circ}$, a special type of linear angles is constructed. In a
third step, dihedral angles (and improper torsions) are constructed
between the atoms of directly neighbouring angles.

If the constrained fragments option is switched on, the set of bonds is
constructed in a different way. The user defines a number of fragments 
(details on fragments definition can be found in 
[Fragment Specification](../essentialelements/fragmentation.md#sec:essentialelements.fragmentation) section.

For each fragment a full set of bonds (not seeing the atoms of the other
fragments) is constructed as described above. When using this option,
the user also has to define which fragments are to be connected. The
connection between these fragments can either be user-defined or
automatically chosen. If the user defines the connecting atoms N1 and
N2, then the interfragmental bond is the one between N1 and N2. If the
user does not define the interfragmental bond, it is constructed between
the atom pair with nearest distance between the two fragments. Then the
angles and dihedrals are constructed upon this (different) set of bonds
in the already described fashion.

Now let us regard the definition of the fragment constraints: A fragment
is constrained internally by constraining all internal coordinates that
contain only atoms of the respective fragment. The connection between
two fragments A and B is constrained by constraining specific internal
coordinates that contain atoms of both fragments. For bonds, one atom
has to belong to fragment A and the other atom has to belong to fragment
B. Regarding angles, two atoms have to belong to fragment A and one to
fragment B and vice versa. With respect to dihedrals, only those are
constrained where two atoms belong to fragment A and the other two
belong to fragment B.

Here is an example : if you want to study systems, which consist of
several molecules (e.g. the active site of a protein) with constraints,
then you can either use cartesian constraints (see above) or use ORCA's fragment constraint
option. ORCA allows the user to define fragments in the system. For each
fragment one can then choose separately whether it should be optimized
or constrained. Furthermore, it is possible to choose fragment pairs
whose distance and orientation with respect to each other should be
constrained. Here, the user can either define the atoms which make up
the connection between the fragments, or the program chooses the atom
pair automatically via a closest distance criterion. ORCA then chooses
the respective constrained coordinates automatically. An example for
this procedure is shown below.

<a id="fig:12"></a>

The coordinates are taken from a crystal structure [PDB-code 2FRJ]. In
our gas phase model we choose only a small part of the protein, which is
important for its spectroscopic properties. Our selection consists of a
heme-group (fragment 1), important residues around the reaction site
(lysine (fragment 2) and histidine (fragment 3)), an important water
molecule (fragment 4), the NO-ligand (fragment 5) and part of a
histidine (fragment 6) coordinated to the heme-iron. In this constrained
optimization we want to maintain the position of the heteroatoms of the
heme group. Since the protein backbone is missing, we have to constrain
the orientation of lysine and histidine (fragments 2 and 3) side chains
to the heme group. All other fragments (the ones which are directly
bound to the heme-iron and the water molecule) are fully optimized
internally and with respect to the other fragments. Since the crystal
structure does not reliably resolve the hydrogen positions, we relax
also the hydrogen positions of the heme group.

```orca
* int 0 1
C 0 0 0 0 0 0
O 1 0 0 1.3 0 0
H 1 2 0 1.1 110 0
H 1 2 3 1.1 110 180
*

%compound
# Step 1: semiempirical calculation of the Hessian
New_Step
! AM1 NumFreq
Step_End

# Step 2: optimization starting from previous Hessian
New_Step
!B3LYP def2-svp def2/J Opt
%geom
InHess
 Read
InHessName "two_step_opt_Compound_1.hess"
# this file must be either a .hess file from a
# frequency run or, a .opt/.carthess file left over from a
# previous geometry optimization
end
Step_End

End
```

!!! note

    -   You have to connect the fragments in such a way that the whole
        system is connected.

    -   You can divide a molecule into several fragments.

    -   Since the initial Hessian for the optimization is based upon the
        internal coordinates: Connect the fragments in a way that their real
        interaction is reflected.

    -   This option can be combined with the definition of constraints, scan
        coordinates(see [Surface Scans](./optimizations_scans.md)) and the `optimizeHydrogens` option (but: its meaning in
        this context is different to its meaning in a normal optimization
        run, relatively straightforward see section
        [structurereactivity.optimization](#sec:structurereactivity.optimization)).

    -   Can be helpful in the location of complicated transition states
        (with relaxed surface scans), see [Surface Scans](./optimizations_scans.md).

    -   Since constraints must be defined manually, [Automatic Fragmentation](../essentialelements/fragmentation.md#sec:essentialelements.fragmentation.inputfile) 
        will not be enabled automatically if there are unassigned atoms to fragments.
        However, it can be activated by including a `%frag` block.

<a id="sec:structurereactivity.optimization.rigidbody"></a>
## Optimization Assuming a Rigid Body

If you want to optimize one or multiple fragments assuming these as a "rigid bodies", i.e. only allowing for movements of the center of mass and pure rotations for each fragment, the keyword `!RIGIDBODYOPT` can be used. 

It needs to be combined with one of the optimization flags, such as `!OPT RIGIDBODYOPT` or `!L-OPT RIGIDBODYOPT`, and all fragments which were defined in any way will be treated as such.

For a more fine control, whenever fragments are defined for the system, each fragment can be
optimized differently (similar to the fragment optimization described above). The following options are available: `FixFrags`,`RelaxHFrags`,`RelaxFrags`, and `RigidFrags` shown within Section [optimization.keywords](#sec:structurereactivity.optimization.keywords). 

A more complex example is depicted in the following:

```orcainput
! L-Opt # or !COPT or !OPT

*xyzfile 0 1 geometry.xyz

%frag
 Definition
  1 {0:12} end
  2 {13:17} end
  3 {18:38} end
  4 {39:53} end
 end
end

%geom
 RelaxFrags {1} end     # Fragment 1 is fully relaxed
 RigidFrags {2 3 4} end # Fragments 2, 3 and 4 are treated as rigid bodies each.
end
```

!!! note
    The manual definition of fragments have to be done after the coordinate input.

!!! warning
    -   If there are atoms not assigned to any fragment, [Automatic Fragmentation](../essentialelements/fragmentation.md#sec:essentialelements.fragmentation.inputfile) will be enabled by default. Users can explicitly control this behavior, as described in [Fragment Specification](../essentialelements/fragmentation.md#sec:essentialelements.fragmentation).
    -   Fragment enumeration will be reordered if manual assignments exceed the total number of fragments and [Automatic Fragmentation](../essentialelements/fragmentation.md#sec:essentialelements.fragmentation.inputfile) is enabled. However, the values of `RelaxFrags` and `RigidFrags` will not be updated accordingly.

<a id="sec:structurereactivity.optimization.biaspot"></a>
## Adding Arbitrary Bias and Wall Potentials

For some applications, it might be interesting to add arbitrary bias potentials during the geometry optimization. For example, if you want to
optimize an intermolecular complex and need that both structures stick
together, without one flying away during the optimization, you might want to add a wall bias. Or you might need a bond bias to guide the DOCKER to dock structures onto certain specific regions of others.

!!! note
      All these walls and biases are integrated with the other electronic-structure methods in ORCA, including their Hessian.

<a id="sec:structurereactivity.optimization.bondbias"></a>
### Bond Bias Potentials

From ORCA 6.1, we introduced a bond bias potential that can be added between two
arbitrary atoms. It will effectively create a fictitious bond between atoms A and B,
 using a symmetric Morse-like potential:

$$
\begin{aligned}
    V = E_{AB}(1-e^{-\alpha(R_{AB}-R_{min})})^2\end{aligned}
$$

where $E_{AB}$ is the energy difference from the bottom of the well to the top, $R_{min}$
is the equilibrium distance. $\alpha$ is a decay parameter that will be automatically
 determined if not given such as to ensure 50% intensity at $2 \times R_{min}$. In practice, 
 it looks like this:

<a id="fig:bias"></a>
![geom_bondbias](../../../images/manual/geom_bondbias.png)

The input to create a simple bias between atoms 0 and 1 is:

```orca
%GEOM 
  BIAS { B 0 1 } END 
END
```

Up to three other parameters can be given: $R_{min}$ in Angstroem, $E_{AB}$ in kcal/mol
 and the alpha. If none of those are given the default values are: sum of Van der Walls radii,
 25 kcal/mol and $\alpha$ will be chosen as described above.
 
 In order to define a bond with $R_{min}=1.5 \mathring{A}$ and a $E_{AB}=100kcal/mol$, for example:

```orca
%GEOM 
  BIAS { B 0 1 1.5 100 } END 
END
```

If a star symbol (*) is used for any of those three, that quantity will be taken from the defaults. For example, in order to set the energy depth, but not the distance, simply use:

```orca
%GEOM 
  BIAS { B 0 1 * 100 } END 
END
```

!!! note
      A negative number on the $E_{AB}$ will create the inverse, repulsive potential instead!

!!! warning
      The ORCA DOCKER has its own `BIAS` block and needs a different input than this to work there, please check Section [DOCKER.bondbias](docker.md#sec:DOCKER.bondbias) for more details.

<a id="sec:structurereactivity.optimization.wallbias"></a>
### Wall Bias Potentials

you can also add three kinds of arbitrary "wall potentials": an
ellipsoid or spherical of the form

$$
\begin{aligned}
    V = \left(\frac{|R - O|}{ radius}\right)^{30}\end{aligned}
$$

or a rectangular box potential with 6 walls of the form

$$
\begin{aligned}
    V = e^{5(R-wall) }\end{aligned}
$$

These can be given in two ways: by explicitly defining the origin of the
potential and its limits, e.g:

```orca
%GEOM 
    ELLIPSEPOT 0,0,0,5,3,4 # the last are the a,b and c radii
END
```

or:

```orca
%GEOM 
    SPHEREPOT 0,0,0,5 # the last is the radius
END
```

or:

```orca
%GEOM 
    BOXPOT 0,0,0,4,-4,3,-3,6,-6 # maxx, minx, maxy, miny, maxz and minz last
END
```

where the first three numbers are the center and the last is the radius
for the sphere (or a,b and c for the ellipsoid) and the max and min x,y
and z dimensions of the box. All numbers should be given in Ångström.

In case a single number is given instead, the walls will be
automatically centered around the centroid of the molecule and that
number will be added to the minimum sphere or box that is necessary to
contain the molecule. For example:

```orca
%GEOM 
    SPHEREPOT 2
END
```

or:

```orca
%GEOM 
    BOXPOT 2
END
```

will build a minimum wall centered on the centroid that encloses the
molecule and add 2 Ångström on top of it. Still on the sphere case, a
negative number like

```orca
%GEOM 
    SPHEREPOT -2
END
```

will make the total radius of the sphere to be Ångström.

!!! note "This will apply to regular geometry optimizations, as well as to"
    the Global Optimizer (GOAT), NEB, DOCKER, SOLVATOR, etc.

<a id="sec:structurereactivity.optimization.mechanochemistry"></a>
## Constant External Force - Mechanochemistry

Constant external force can be applied on the molecule within the EFEI
formalism[marx:ChemRev2012](../../bibliography.md) by pulling on the two defined atoms. To
apply the external force, use the POTENTIALS in the geom block. The
potential type is C for Constant force, indexes of two atoms
(zero-based) and the value of force in nN.

```orca
! RKS B3LYP/G SV(P) Opt
%geom Constraints
        { B 0 1 1.25 C }
        { A 2 0 3 120.0 C }
        end
      end

* int 0 1
    C  0 0 0 0.0000   0.000    0.00
    O  1 0 0 1.2500   0.000    0.00
    H  1 2 0 1.1075 122.016    0.00
    H  1 2 3 1.1075 122.016  180.00
*
```

The results are seen in the output of the SCF procedure, where the total
energy already contains the force term.

```orca
----------------
TOTAL SCF ENERGY
----------------

Total Energy       :         -150.89704913 Eh           -4106.11746 eV

Components:
Nuclear Repulsion  :           36.90074715 Eh            1004.12038 eV
External potential :           -0.25613618 Eh              -6.96982 eV
Electronic Energy  :         -187.54166010 Eh           -5103.26802 eV
```

<a id="sec:structurereactivity.optimization.internalcoords"></a>
## Printing Hessian in Internal Coordinates

When a Hessian is available, it can be printed out in redundant internal
coordinates as in the following example:

```orca
Constraining bond distances        :   { B N1 N2 value C }
Constraining bond angles           :   { A N1 N2 N1 value C }
Constraining dihedral angles       :   { D N1 N2 N3 N4 value C }
Constraining cartesian coordinates :   { C N1 C }
Constraining only X-coordinates    :   { X N1 C }
Constraining only Y-coordinates    :   { Y N1 C }
Constraining only Z-coordinates    :   { Z N1 C }
```

!!! note
    -   The Hessian in internal coordinates is (for the input `printHess.inp`)
        stored in the file `printHess_internal.hess`.

    -   The corresponding lists of redundant internals is stored in
        `printHess.opt`.

    -   Although the `!Opt` keyword is necessary, an optimization is not
        carried out. ORCA exits after storing the Hessian in internal
        coordinates.

<a id="sec:structurereactivity.optimization.modelHess"></a>
## Using Model Hessian from Previous Calculations

If you had a geometry optimization interrupted, or for some reason want
to use the model Hessian updated from a previous calculation, you can do
that by passing a `basename.opt` file, a `basename.carthess` file or the
initial Hessian on a new calculation.

```orca
%GEOM 
    InHess     READ
    InHessName "basename.carthess"
END
```

<a id="sec:structurereactivity.optimization.lbfgs"></a>
## Geometry Optimizations using the L-BFGS Optimizer

Optimizations using the L-BFGS optimizer are done in Cartesian
coordinates. They can be invoked quite simple as in the following
example:

```orca
! L-Opt
! MM
%MM
  ORCAFFFILENAME "CHMH.ORCAFF.prms"
END
*pdbfile 0 1 CHMH.pdb
```

Using this optimizer systems with 100s of thousands of atoms can be
optimized. Of course, the energy and gradient calculations should not
become the bottleneck for such calculations, thus MM or QM/MM methods
should be used for such large systems.

The default maximum number of iterations is 200, and can be increased as
follows:

```orca
! L-Opt
%GEOM
  maxIter 500 # default 200
END
*pdbfile 0 1 CHMH.pdb
```

Only the hydrogen positions can be optimized with the following command:

```orca
! L-OptH
```

But also other elements can be exclusively optimized with the following
command:

```orca
! L-OptH
%GEOM
 OptElement F  # optimize fluorine only when L-OptH is invoked.
               # Does not work with optimization in internal coordinates.
END
```

!!! note
    If you want to use the previously (ORCA5 and ORCA6.0) available `L-Opt` option, you need 
    to specify `MD-L-Opt` or `MD-L-OptH`.

[^1]: But that doesn't mean that geometry optimization itself is
    straightforward! Sometimes, even when it is not expected the
    convergence can be pretty bad and it may take a better starting
    structure to come to a stationary point. In particular floppy
    structures with many possible rotations around single bonds and soft
    dihedral angle modes are tricky. It may sometimes be advantageous to
    compute a Hessian matrix at a "cheap" level of theory and then do
    the optimization in Cartesian coordinates starting from the
    calculated Hessian.

<a id="sec:structurereactivity.optimization.externaloptimizer"></a>
## Optimizing with External Methods

Although ORCA features a many electronic structure models, it cannot cover all available methods. Therefore, ORCA features an
interface to external programs that allows you to use ORCA's features with electronic structure methods and
model potentials provided by external programs. This way, you'll be able to utilize the latest MNDO based semi-empirical methods like PM7 or
neural network potentials like AIMNet2 and UMA within the ORCA infrastructure, 
e.g. to [optimize structures](optimizations.md), search transition states with [NEB-TS](neb.md), or sample conformers with [GOAT](goat.md).
Other calculations which exclusively rely on energies and gradients are also supported.

The external program infrastructure is activated via the ORCA simple input keyword `!ExtOpt`,
which essentially replaces the electronic structure method used during a single point energy/gradient calculation.
This must be combined with other keywords like `!Opt` or `!GOAT` to select the specific run type.
Other keywords related to the run type, such as constraints, can be used as usual.

As every program typically provides differently formatted output, 
individual wrapper scripts are required to link ORCA and its external optimizer infrastructure. 
The full path to your wrapper script can be provided via the `%method` block in the ORCA input file:

```text
! ExtOpt

%method
  ProgExt "/full/path/to/wrapperscript"
  Ext_Params "optional command line arguments"
end
```

Alternatively, you can also provide the script as a file or link named `otool_external` in the same directory as the ORCA executables, 
or by assigning the `EXTOPTEXE` environment variable to the *full path* to the external program.

Regardless of which option is used, the keyword `Ext_Params` can be used to specify the
additional command line arguments as a single string.

!!! note
    All information that you give on the electronic structure is discarded.

After executing ORCA, it automatically writes an
input file called `basename_EXT.extinp.tmp` in each step containing the following info:

```orca
basename_EXT.xyz # xyz filename: string, ending in '.xyz'
0 # charge: integer
1 # multiplicity: positive integer
1 # NCores: positive integer
0 # do gradient: 0 or 1
pointcharges.pc # point charge filename: string (optional)
```

Comments from `#` until the end of the line should be ignored.
The file `basename_EXT.xyz` will also be written to the working directory.
While the energy is always requested, the gradient is only calculated when needed.

ORCA then calls:

```orca
scriptname basename_EXT.extinp.tmp [args]
```

Here, `args` are the optional command line arguments provided defined with the `Ext_Params` in the ORCA input.
They are passed to the external program without any changes.

The external script starts the energy (and gradient) calculation and finally
provides the results in a file called `basename_EXT.engrad` using the same
`basename` as the XYZ file. This file must have the following format:

```orca
#
# Number of atoms: must match the XYZ
#
3
#
# The current total energy in Eh
#
-5.504066223730
#
# The current gradient in Eh/bohr: Atom1X, Atom1Y, Atom1Z, Atom2X, etc.
#
-0.000123241583
0.000000000160
-0.000000000160
0.000215247283
-0.000000001861
0.000000001861
-0.000092005700
0.000000001701
-0.000000001701
```
Comments from `#` until the end of the line are ignored, as are any comment-only lines.

The script may also print relevant output to `STDOUT` and/or `STDERR`. 
`STDOUT` will either be printed in the ORCA standard output, 
or redirected to a temporary file and removed afterwards, depending on the type of job 
(e.g., for `NumFreq` the output for the displaced geometries is always redirected) 
and the ORCA output settings:

```orca
%output
  Print[P_EXT_OUT]  1 # (default) print the external program output
  Print[P_EXT_GRAD] 1 # (default) print the gradient from the ext. program
end
```

!!! warning
    Some wrapper scripts and how to use them can be found in the [official GitHub repository](https://github.com/faccts/orca-external-tools/).
    While some methods and programs such as MOPAC, AIMNet2, and UMA are already supported, 
    you are free to write your own wrapper scripts to extend the available methods usable with ORCA. 
    If you do so, please contribute to the repository via pull requests to share with the community.

!!! note
    Note that depending on your OS and infrastructure, you may need to do some modifications to the wrapper script.

<a id="sec:structurereactivity.optimization.faq"></a>
## Optimization FAQs

### I can't locate the transition state (TS) for a reaction expected to feature a low/very low barrier, what should I do?

For such critical case of locating the TS, running a very fine
(e.g. 0.01 Å increment of the bond length) relaxed scan of the key reaction
coordinate is recommended, see [Surface Scans](./optimizations_scans.md). In this way the highest energy point on a
very shallow surface can be identified and used for the final TS
optimisation.

### During the geometry optimisation some atoms merge into each other and the optimisation fails. How can this problem be solved?

This usually occurs due to the wrong or poor construction of initial
molecular orbital involving some atoms. Check the basis set definition
on problematic atoms and then the corresponding MOs!

<a id="sec:structurereactivity.optimization.notes"></a>
## Some General Notes on Geometry Optimization

!!! note

    -   `TightSCF` in the SCF part is set as default to avoid the buildup of
        too much numerical noise in the gradients.

    -   Even if the optimization does not converge, the ORCA output may
        still end with \"\*\*\*\*ORCA TERMINATED NORMALLY\*\*\*\*\".
        Therefore do not rely on the presence of this line as an indicator
        of whether the geometry optimization is converged! Rather, one
        should instead rely on the fact that, an optimization job that
        terminates because the maximum number of iterations has been
        reached, will generate the following output message:

!!! note
           The optimization did not converge but reached the maximum number of
           optimization cycles. Please check your results very carefully.

While a successfully converged job will generate the following message
instead:

```
***********************HURRAY********************
***        THE OPTIMIZATION HAS CONVERGED     ***
*************************************************
```

!!! tip

    -   In rare cases the redundant internal coordinate optimization fails.
        In this case, you may try to use `COPT` (optimization in Cartesian
        coordinates). This will likely take many more steps to converge but
        should be stable.

    -   For optimizations in Cartesian coordinates the initial guess Hessian
        is constructed in internal coordinates and thus these optimizations
        should converge only slightly slower than those in internal
        coordinates. Nevertheless, if you observe a slow convergence
        behaviour, it may be a good idea to compute a Hessian initially
        (perhaps at a lower level of theory) and use `InHess read` in order
        to improve convergence.

    -   At the beginning of a TS optimization more information on the
        curvature of the PES is needed than a model Hessian can give. The
        best choice is analytic Hessian, available for HF, DFT and MP2. In
        other cases (e.g. CAS-SCF), the numerical evaluation is necessary.
        Nevertheless you do not need to calculate the full Hessian when
        starting such a calculation. With ORCA we have good experience with
        approximations to the exact Hessian. Here it is recommended to
        either directly combine the TS optimization with the results of a
        relaxed surface scan or to use the Hybrid Hessian as the initial
        Hessian, depending on the nature of the TS mode. Note that these
        approximate Hessians do never replace the exact Hessian at the end
        of the optimization, which is always needed to verify the minimum or
        first order saddle point nature of the obtained structure.

<a id="sec:structurereactivity.optimization.keywords"></a>
## Geometry Optimization Keywords

 Starting from the the simple input form, here is a list of keywords
for optimization options in ORCA: 

```orca
%method RunTyp Opt # use geometry optimization.
                   #(equivalent is RunTyp=Geom)
        end

# or simply "! Opt" in the keyword line

# details of the optimization are controlled here
%geom 
      MaxIter 50  # max. number of geometry iterations
                  #  (default is 3N (N = number of atoms), at least 50 )
      # coordinate type control
      coordsys redundant     # redundant internal coords (2022)
               cartesian     # Cartesian coordinates
      # fallback option to Cartesian step if internals fail
      cartfallback true
      # transition state (TS) optimization
      TS_search EF      # Switch on TS search, EF means
                        #  "eigenvector following"
                        #  alternatively use "! OptTS"
      TS_Mode {M 0} end # Choose the mode to follow uphill in the
                        #  TS optimization. {M X}: eigenvector of
                        #  the Hessian with X. lowest eigenvalue
                        #  (start counting at zero) (default: X=0)
      # Instead of a mode choose an internal coordinate strongly
      #  involved in the eigenmode followed uphill
      TS_Mode {B 0 1} end      # bond between atoms 0 and 1  or
      TS_Mode {A 2 1 0} end    # angle between atoms 2, 1 and 0  or
      TS_Mode {D 3 2 1 0} end  # dihedral of atoms 3, 2, 1 and 0
      # add or remove internal coordinates from the automatically
      #  generated set of redundant internal coords
      modify_internal
          { B 10 0 A }      # add a bond between atoms 0 and 10
          { A 8 9 10 R }    # remove the angle defined
                            #  by atoms 8, 9 and 10
          { D 7 8 9 10 R }  # remove the dihedral angle defined
          end               #  by atoms 7, 8, 9 and 10
      # constrain internal coordinates:
      Constraints
          { B N1 N2 value C }       # the bond between N1 and N2
          { A N1 N2 N1 value C }    # the angle defined by N1, N2
                                    #  and N3
          { D N1 N2 N3 N4 value C } # the dihedral defined by N1,
                                    #  N2, N3 and N4
          { C N1 C }                # the cartesian position of N1
          { X N1 C }                # the cartesian X-position of N1
          { Y N1 C }                # the cartesian Y-position of N1
          { Z N1 C }                # the cartesian Z-position of N1
          { C N1:N2 C }             # the cartesian positions of N1 through N2
          { X N1:N2 C }             # the cartesian X-positions of N1 through N2
          { Y N1:N2 C }             # the cartesian Y-positions of N1 through N2
          { Z N1:N2 C }             # the cartesian Z-positions of N1 through N2
          { B N1 * C}       # all bonds involving N1
          { B * * C}        # all bonds
          { A * N2 * C }    # all angles with N2 as central atom
          { A * * * C }     # all angles
          { D * N2 N3 * C } # all dihedrals with N2 and N3 as
                            #  central atoms
          { D * * * * C }   # all dihedrals
      end
      # scan an internal coordinate:
      Scan B N1 N2 = value1, value2, N end
        # perform constrained optimizations with varying N1-N2-
        #  distance from value1 up to value2 in N steps;
        #  works as well for angles (use A N1 N2 N3) and for
        #  dihedrals (use D N1 N2 N3 N4)
      Scan B N1 N2 [value1 value2 value3 ... valueN] end
        # perform constrained optimizations with N1-N2-distances
        #  as given in the list;
        #  works as well for angles (use A N1 N2 N3) and for
        #  dihedrals (use D N1 N2 N3 N4)
      # perform a simultaneous multidimensional scan
      # possible for up to 3 different scan parameters. They each must 
      # have an identical number of scan steps
      simul_Scan true # default false
      fullScan true   # if !ScanTS is requested, fullScan assures
                      #  that the relaxed surface scan is fully
                      #  carried out before the TS optimization is
                      #  started (Default is false)
      # fragment optimization:
      #  1. all atoms have to belong to a fragment
      #  2. you have to connect the fragments
      ConnectFragments
          {1 2 C}      # constrain the internal coordinates
                       #  connecting fragments 1 and 2
          {1 2 C N1 N2}# constrain the internal coordinates
                       #  connecting fragments 1 and 2, the
                       #  fragments are connected via atoms
                       #  N1 and N2
          {1 3 O}      # optimize the internal coordinates
                       #  connecting fragments 1 and 3
          {1 3 O N1 N2}# optimize the internal coordinates
                       #  connecting fragments 1 and 3, the
                       #  fragments are connected via atoms
                       #  N1 and N2
      end
      #  3. you can constrain the fragment internally
      ConstrainFragments  # constrain all internal coordinates
          { 1 }           #  containing only atoms of fragment 1
      end
      # optimize hydrogens
      optimizeHydrogens true
        # in the context of a normal optimization all internal
        #  coordinates not involving any hydrogens are constrained
        # in the context of a fragment optimization all internal
        #  coordinates involving hydrogens are optimized (also in a
        #  constrained fragment)
      # freeze the hydrogen positions with respect to the
      #  heteroatoms
      freezeHydrogens true
      # invert the defined constraints, i.e. optimize the
      #  constraints and constrain the remaining coordinates
      # this only works for the redundant internal coordinates
      # Cartesian coordinates are not affected by invertConstraints
      invertConstraints true      # step type control
      Step     qn       # quasi-Newton step
               rfo      # Rational function step (Default for !Opt)
               prfo     # partitioned RFO step (Default for !OptTS)
      # Step size control
      MaxStep 0.3 # maximum step length in internal coordi-
                  #  nates. Default is 0.3 au
      Trust -0.3 # Initial trust radius. Default is -0.3 au
                 # Trust <0 - use fixed trust radius
                 #  of size -trust. I.e. -0.3 means fix
                 #  the trust radius at 0.3
                 # Trust >0 - use trust radius update. I.e. 0.3
                 #  means start with trust radius 0.3 and update
                 #  the trust radius after each optimization step
      # Convergence tolerances. Note that the calculation is
      # only converged if all criteria are fullfilled. All
      # values given are default values.
      TolE 5e-6      # Energy change (a.u.)
      TolRMSG  1e-4  # RMS gradient (a.u.)
      TolMaxG  3e-4  # Max. element of gradient (a.u.)
      TolRMSD  2e-3  # RMS displacement (a.u.)
      TolMaxD  4e-3  # Max. displacement (a.u.)
      # keyword for frequently used sets of convergence thresholds
      Convergence normal    # Default
                  loose
                  tight
      ProjectTR false # project translation and rotation
                      # default is false. MUST be false for
                      # redundant internals
  end
```

Keywords for the control of the Hessian (especially important for the TS
optimization):

```orca
# initial Hessian control
      inhess   unit      # unit matrix
               Read      # Hessian in a .hess file (e.g. from
                         #  a previous NumFreq run), this command
                         #  comes with the following:
               InHessName "filename.hess" # filename of
                                          # Hessian input file
                                          # a previous .opt file
                                          # or a previous .carthess file
               # these only for redundants
               Lindh     # Lindh's model Hessian
               Almloef   # Almloef's model Hessian
               Schlegel  # Schlegel's model Hessian
               Swart     # Swart and Bickelhaupt`s model Hessian
               XTB0      # GFN0-xTB Hessian
               XTB1      # GFN1-xTB Hessian
               XTB2      # GFN2-xTB Hessian
               GFNFF     # GFN-FF Hessian
      # additional Hessian control for TS optimization
      Calc_Hess true  # calculate the Hessian numerically at the beginning
      Recalc_Hess  5  # calculate the Hessian at the beginning
                      #  and recalculate it after 5,10,.. cycles
      Hybrid_Hess {0 1 5 6} end # calculates a Hybrid Hessian
                                # exact calculation for
                                # atoms 0, 1, 5 and 6; works also
                                # with Calc_Hess and Recalc_Hess
      NumHess true      # requests use of numerical Hessian
      # modification of the internal Hessian
      Hess_Internal
        {A 3 2 1 D 2.0} # define a diagonal Hessian value of
                        #  2 Eh/Bohr2 for the angle between
                        #  atoms 3 2 1. This can also be done for
                        #  bonds, dihedrals and Cartesian
                        #  coordinates.) The Hessian values of
                        #  multiple coordinates can be modified
        reset 5    # reset the modified internal Hessian values
                   #  after 5 cycles
        # The following is only recommended
        #  after a relaxed surface scan
        #  in this example of the scan coordinate B 1 0;
        #  "basename.004.xyz" contains the optimized structure
        #  of the scan step with highest energy
        {B 1 0 C}
        XYZ1 "scanName.003.xyz" # the xyz-files of the structures
        XYZ2 "ScanName.005.xyz" #  next to the highest energy point
        GBW1 "ScanName.003.gbw" # the gbw-files of the structures
        GBW2 "ScanName.005.xyz" #  next to the highest energy
                                # the gbw-files are optional
       end
      # Hessian update procedure
      Update   Powell
               Bofill  # default for TS optimization
               BFGS    # default for geometry optimization
      # Hessian modification (only for P-RFO step)
      HESS_Modification Shift_Diag # shift the diagonal elements
                                   #  (default)
                        EV_Reverse # reverse the
                                   #  diagonal elements
      # Minimal value of Hessian eigenvalues (only P-RFO step)
      HESS_MinEV 0.0001  # if an absolute Hessian eigenvalue
                         #  is smaller than this value, it is
                         #  set to HESS_MinEV
      # Rebuilding the model Hessian after a number of cycles can
      #  accelerate the convergene of the optimization
      NResetHess 20 # Set the number of geometry steps after which
                    #  a new model Hessian is built (only with BFGS
                    #  update)
      NStepsInResetHess 5  # since previous steps and gradients are
                           #  available, it is possible to include
                           #  information about the PES in the
                           #  newly built Hessian (via a BFGS
                           #  update). This number should be
                           #  smaller than NResetHess
  end
```

As for parameter scan runs ORCA has some special options that may help
to speed up the optimization:

```orca
%geom UseSOSCF false # switches the converger to SOSCF
                     # after the first point. SOSCF may
                     # converge better than DIIS if the
                     # starting orbitals are good.
                     # default = false
      ReducePrint true # reduce printout after the first
                       # point default=true
 # the initial guess can be changed after the first
 # point. The default is MORead. The MOs of the pre-
 # vious point will in many cases be a very good guess
 # for the next point. In some cases however, you may
 # want to be more conservative and use a general guess.
 OptGuess   = OneElec  # the one electron matrix
            = Hueckel  # the extended Hueckel guess
            = PAtom;   # the PAtom guess
            = Pmodel   # the PModel guess
            = MORead   # MOs of the prev. point (default)
 end
```

<a id="tab:structurereactivity.optimization.keywords.simple"></a>
!!! note "Simple input keywords for geometry optimization."


| ****Keyword**** | Description |
| --- | --- |
| **`Opt`** | Optimization with default convergence tolerance (Alias: `NormalOpt`, cf. [tab:structurereactivity.optimization.thresholds](#tab:structurereactivity.optimization.thresholds)) |
| **`LooseOpt`** | Optimization with looser convergence tolerance (cf. [tab:structurereactivity.optimization.thresholds](#tab:structurereactivity.optimization.thresholds)) |
| **`TightOpt`** | Optimization with tight convergence tolerance (cf. [tab:structurereactivity.optimization.thresholds](#tab:structurereactivity.optimization.thresholds)) |
| **`VeryTightOpt`** | Optimization with very tight convergence tolerance (cf. [tab:structurereactivity.optimization.thresholds](#tab:structurereactivity.optimization.thresholds)) |
| **`COpt`** | Optimization in Cartesian coordinates (can be combined with `TightOpt`, etc.) |

<a id="tab:structurereactivity.optimization.keywords.method"></a>
!!! note "`%method` block input keywords and options for geometry optimization."
    | Keyword                  | Option / Value            | Description                                                                 |
    |:---------------------------------|:--------------------------|:----------------------------------------------------------------------------|
    | `%method`                        | `RunTyp Opt`              | Sets geometry optimization as the run type.                                 |
    |                                  | `RunTyp=Geom`             | Alternative syntax for geometry optimization.                               |

<a id="tab:structurereactivity.optimization.keywords.geom"></a>
!!! note "`%geom` block input keywords and options for geometry optimization."
    | **Keyword** | Option / Value | Description |
    |---|---|---|
    | **`MaxIter`** | `50` | Maximum number of geometry iterations (default max(3N, 50)). |
    | **`coordsys`** | `redundant` | Use redundant internal coordinates. |
    |  | `cartesian` | Use Cartesian coordinates. |
    | **`cartfallback`** | `true` | Use Cartesian step if internal coordinate step fails. |
    | **`modify_internal`** | `{B 10 0 A}` | Add bond between atoms 0 and 10. |
    |  | `{A 8 9 10 R}` | Remove angle between atoms 8, 9, and 10. |
    |  | `{D 7 8 9 10 R}` | Remove dihedral between atoms 7, 8, 9, and 10. |
    | **`Constraints`** | `{B 1 2 value C}` | Constrain bond between atoms 1 and N. |
    |  | `{A 1 2 3 value C}` | Constrain angle defined by atoms 1, 2, and 3. |
    |  | `{D 1 2 3 4 value C}` | Constrain dihedral defined by atoms 1–4. |
    |  | `{C 1 C}` | Constrain Cartesian position of atom 1. |
    |  | `{B 1 * C}` | Constrain all bonds involving atom 1. |
    |  | `{B * * C}` | Constrain all bonds. |
    |  | `{A * 2 * C}` | Constrain all angles with atom 2 as central. |
    |  | `{A * * * C}` | Constrain all angles. |
    |  | `{D * 2 3 * C}` | Constrain all dihedrals with 2 and 3 as central atoms. |
    |  | `{D * * * * C}` | Constrain all dihedrals. |
    | **`ReduceRedInts`** | `true` | Generates the internal coordinates of the constrains atoms. |
    | **`ConnectFragments`** | `{1 3 O}` | Optimize internal coordinates connecting fragments 1 and 3. |
    |  | `{1 3 O N1 N2}` | Connect fragments 1 and 3 via atoms N1 and N2. |
    | **`ConstrainFragments`** | `{1}` | Constrain all internal coordinates within fragment 1. |
    | **`Frags`** | `X {0:12}` | Defining fragment X, containing atoms 0-12. Other atoms default to fragment 1. |
    | **`AUTOFRAG`** | `true` | Automatically select fragments based on topology. |
    | **`FixFrags`** | `{1}` | Freeze coordinates of all atoms in specified fragment(s). |
    | **`RelaxHFrags`** | `{1}` | Relax hydrogen atoms of the specified fragment(s). Default if !L-OptH is defined. |
    | **`RelaxFrags`** | `{1}` | Relax all atoms of the specified fragment(s). Default if !L-Opt is defined. |
    | **`RigidFrags`** | `{1}` | Treat fragment(s) as rigid bodies, but relax position/orientation. |
    | **`optimizeHydrogens`** | `true` | Optimize coordinates involving H atoms while constraining others. |
    | **`freezeHydrogens`** | `true` | Freeze H positions relative to heteroatoms. |
    | **`invertConstraints`** | `true` | Invert the defined constraints (only for redundant internals). |
    | **`Step`** | `qn` | Use quasi-Newton step. |
    |  | `rfo` | Use Rational Function Optimization step (default for `!Opt`). |
    |  | `prfo` | Use partitioned RFO step (default for `!OptTS`). |
    | **`MaxStep`** | `0.3` | Maximum step length in internal coordinates (default: 0.3 au). |
    | **`Trust`** | `-0.3` | Fixed trust radius of 0.3 au (negative indicates fixed). |
    | **`TolE`** | `5e-6` | Convergence threshold for energy change (a.u.). |
    | **`TolRMSG`** | `1e-4` | Convergence threshold for RMS gradient (a.u.). |
    | **`TolMaxG`** | `3e-4` | Convergence threshold for max gradient component (a.u.). |
    | **`TolRMSD`** | `2e-3` | Convergence threshold for RMS displacement (a.u.). |
    | **`TolMaxD`** | `4e-3` | Convergence threshold for max displacement (a.u.). |
    | **`Convergence`** | `normal` | Default convergence threshold. |
    |  | `loose` | Looser convergence thresholds. |
    |  | `tight` | Tighter convergence thresholds. |
    | **`ProjectTR`** | `false` | Disable translation and rotation projection (must be false for internals). |
    | **`inhess`** | `unit` | Start optimization with a unit matrix Hessian. |
    |  | `Read` | Read Hessian from external file. Requires `InHessName`. |
    | **`InHessName`** | `"filename.hess"` | File containing the Hessian (`.hess`, `.opt`, `.carthess`). |
    |  | `Lindh` | Use Lindh’s model Hessian (only for redundant coordinates). |
    |  | `Almloef` | Use Almloef’s model Hessian. |
    |  | `Schlegel` | Use Schlegel’s model Hessian. |
    |  | `Swart` | Use Swart and Bickelhaupt’s model Hessian. |
    |  | `XTB0` | Use GFN0-xTB Hessian. |
    |  | `XTB1` | Use GFN1-xTB Hessian. |
    |  | `XTB2` | Use GFN2-xTB Hessian. |
    |  | `GFNFF` | Use GFN-FF Hessian. |
    | **`Calc_Hess`** | `true` | Calculate numerical Hessian at beginning of optimization. |
    | **`Recalc_Hess`** | `5` | Recalculate Hessian every 5 cycles. |
    | **`Hybrid_Hess`** | `{0 1 5 6} end` | Calculate exact Hessian for specified atoms, model for rest. |
    | **`NumHess`** | `true` | Request numerical Hessian. |
    | **`Hess_Internal`** | `{A 3 2 1 D 2.0}` | Set Hessian value (Eh/Bohr²) for angle between atoms 3-2-1. |
    |  | `reset 5` | Reset modified Hessian values after 5 cycles. |
    |  | `{B 1 0 C}` | Coordinates for Hessian refinement after relaxed surface scan. |
    |  | `XYZ1` `"scanName.003.xyz"` | Structure file before maximum in scan. |
    |  | `XYZ2` `"ScanName.005.xyz"` | Structure file after maximum in scan. |
    |  | `GBW1` `"ScanName.003.gbw"` | Optional GBW file before max in scan. |
    |  | `GBW2` `"ScanName.005.xyz"` | Optional GBW file after max in scan. |
    | **`Update`** | `Powell` | Use Powell update for Hessian. |
    |  | `Bofill` | Use Bofill update (default for TS optimization). |
    |  | `BFGS` | Use BFGS update (default for geometry optimization). |
    | **`HESS_Modification`** | `Shift_Diag` | Shift diagonal elements of Hessian (default). |
    |  | `EV_Reverse` | Reverse sign of diagonal elements. |
    | **`HESS_MinEV`** | `0.0001` | Minimum allowed Hessian eigenvalue. |
    | **`NResetHess`** | `20` | Rebuild model Hessian after 20 steps (BFGS only). |
    | **`NStepsInResetHess`** | `5` | Number of previous steps used to inform new model Hessian. |
    | **`UseSOSCF`** | `false` | Use SOSCF after first point. May converge better than DIIS. |
    | **`ReducePrint`** | `true` | Reduces printout after first point. |
    | **`OptGuess`** |  | Initial guess control. Default is `MORead`. |
    |  | `OneElec` | Use the one-electron matrix guess. |
    |  | `Hueckel` | Use the extended Hückel guess. |
    |  | `PAtom` | Use the PAtom guess. |
    |  | `PModel` | Use the PModel guess. |
    |  | `MORead` | Use MOs of the previous point. Default. |
    | **`AddExtraBonds`** | `true` | Enable extra bonds between close atom pairs. |
    | **`AddExtraBonds_MaxLength`** | `10` | Max number of bonds connecting two atoms for extra bonding. |
    | **`AddExtraBonds_MaxDist`** | `5` | Max distance (Å) for considering extra bonding. |
    | **`BIAS`** | `{B 0 1}` | Fictitious bond between atoms 1 and 2 for Morse-like potential. |
    | **`ELLIPSEPOT`** | `0,0,0,5,3,4` | Ellipsoidal potential centered at (0,0,0), semi-axes a=5, b=3, c=4. |
    | **`SPHEREPOT`** | `0,0,0,5` | Spherical potential centered at (0,0,0), radius 5. |
    | **`BOXPOT`** | `0,0,0,4,-4,3,-3,6,-6` | Box potential: maxx=4, minx=–4, maxy=3, miny=–3, maxz=6, minz=–6. |
    | **`OptElement`** | `N` | Optimize element "N" atoms only (requires L-OptH; not for internals). |

