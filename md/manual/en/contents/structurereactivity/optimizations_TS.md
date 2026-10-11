```{index} Transition States
```

(sec:structurereactivity.optimization.transitionstate)=
# Transition State Searches

## Transition State Search Theory

As transition state finder we implemented the well-established
eigenvector following algorithm using a P-RFO step as implemented by
Baker {cite}`baker1986comp`. This algorithm is a quasi-Newton like algorithm.

The Taylor series of the energy, truncated after the quadratic term, is:

$$E=E_{0} +g_{q}\,^{+}\Delta q_{q} +\frac{1}{2}\Delta q\, ^{+}\mathrm{H}_{q} \Delta q
$$ (eqn:200)

The Newton-Raphson step to get from the actual point to a stationary
point is:

$$\Delta q=- \mathrm{H}_{q}^{-1} g_{q} =\sum{ -\frac{V_{i}^{+} g_{q} V_{i} }{b_{i} }}
$$ (eqn:201)

with $V_{i}$ and $b_{i}$ as eigenvectors and eigenvalues of the Hessian
$\mathrm{H}_{q}$. This step leads to the nearest stationary point on the
PES. This stationary point can be a minimum or a saddle point, according
to the curvature of the PES at the actual point.

With a simple shift of the Hessian eigenvalues $b_{i}$ in this equation
one can guide the step to a stationary point with the required
characteristics (Hessian with exactly one negative eigenvalue). The
transition state search is separated into two different optimization
problems. The energy is maximized along one Hessian eigenmode and
minimized along the remaining 3$N-7(6)$ eigenmodes. We introduce two
different shift parameters $\lambda_{p}$ and $\lambda_{n}$, where
$\lambda_{p}$ is the shift parameter for the eigenmode being maximized
and $\lambda_{n}$ shifts the Hessian eigenvalues of the modes being
minimized. This method allows us to maximize along any mode, not only
the one with smallest eigenvalue. Starting from two different
RFO-matrices for the different optimization problems (see description
above) we get for $\lambda_{p}$ and $\lambda_{n}$:

$$\lambda_{p} =\frac{1}{2}b_{k} +\frac{1}{2}\sqrt{ b_{k}^{2} +4F_{k}^{2} } \quad
\text{and} \quad \sum\limits_{i\ne k} { \frac{F_{i}^{2} }{\lambda_{n} -b_{i} } } = \lambda_{n}
$$ (eqn:202)

whereas $F_{i} =V_{i}^{+} g$ is the component of $g$ along the Hessian
eigenmode $V_{i}$ and $\lambda_{n}$ has to get solved iteratively. The
solution for $\lambda_{n}$ has to be negative and lower than $b_{2}$ (or
lower than $b_{1}$, if not the lowest mode is being followed). If the
Hessian has more than one negative eigenvalue, these properties might
not be fulfilled, and the Hessian would have to be modified. In our
implementation the Hessian diagonal elements are either shifted or
reversed in such a case.

Once the shift parameters are known the P-RFO step $h$ is calculated as
follows:

$$\Delta q_{k} = -\frac{\bar{{F} }_{k} V_{k} }{b_{k} -\lambda_{p} } \quad  \text{and} \quad \Delta q_{i} = -\frac{\bar{{F} }_{i} V_{i} }{b_{i} -\lambda_{n} } \quad \text{with} \quad i=1\dots n,\, \, \, i\ne k
$$ (eqn:203)

$$\Delta q=\sum\limits_{j=1}^n { \Delta q_{j} }
$$ (eqn:204)


(sec:structurereactivity.optimization.transitionstate.intro)=
## Introduction to Transition State Searches

If you provide a good estimate for the structure of the transition state
(TS) structure, then you can find the respective transition state with
the following keywords OptTS and ScanTS (in this example we take the structure with
highest energy of the above relaxed surface scan):

```orca
! B3LYP SV(P) TightSCF SlowConv OptTS       
# performs a TS optimization with the EF-algorithm
# Transition state: H-atom abstraction from CH4 to OH-radical

%geom 
   Calc_Hess true  # calculation of the exact Hessian
                   #  before the first optimization step
end

* int 0 2
    C  0 0 0 0.000000   0.000   0.000
    H  1 0 0 1.285714   0.000   0.000
    H  1 2 0 1.100174 107.375   0.000
    H  1 2 3 1.100975 103.353 119.612
    H  1 2 3 1.100756 105.481 238.889
    O  2 1 3 1.244156 169.257  17.024
    H  6 2 1 0.980342 100.836  10.515
*
```

:::{Note}

-   You need a good guess of the TS structure. Relaxed surface scans can
    help in almost all cases (see also example above).

-   For TS optimization (in contrast to geometry optimization) an exact
    Hessian, a Hybrid Hessian or a modification of selected second
    derivatives is necessary.

-   Analytic Hessian evaluation is available for HF and SCF methods,
    including the RI and RIJCOSX approximations and canonical MP2.

-   Check the eigenmodes of the optimized structure for the eigenmode
    with a single imaginary frequency. You can also visualize this
    eigenmode with `orca_pltvib` (section
    {ref}`sec:spectroscopyproperties.vib.animation`) or any other
    visualization program that reads ORCA output files.

-   If the Hessian is calculated during the TS optimization, it is
    stored as basename.001.hess, if it is recalculated several times,
    then the subsequently calculated Hessians are stored as
    basename.002.hess, basename.003.hess, ...

-   If you are using the Hybrid Hessian, then you have to check
    carefully at the beginning of the TS optimization (after the first
    three to five cycles) whether the algorithm is following the correct
    mode (see TIP below). If this is not the case you can use the same
    Hybrid Hessian again via the inhess read keyword and try to target a
    different mode (via the `TS_Mode` keyword, see below).
:::

In the example above the TS mode is of local nature. In such a case you
can directly combine the relaxed surface scan with the TS optimization
with the

```orca
! ScanTS
```

command, as used in the following example:

```
! B3LYP SV(P) TightSCF SlowConv
! ScanTS 
# perform a relaxed surface scan and TS optimization
#  in one calculation
%geom 
     scan 
        B 1 0 = 2.0, 1.0, 15 
     end 
end
* int 0 2
 C     0   0   0   0.000000     0.000     0.000
 H     1   0   0   1.999962     0.000     0.000
 H     1   2   0   1.095870   100.445     0.000
 H     1   2   3   1.095971    90.180   119.467
 H     1   2   3   1.095530    95.161   238.880
 O     2   1   3   0.984205   164.404    27.073
 H     6   2   1   0.972562   103.807    10.843
*
```

:::{Note}

-   The algorithm performs the relaxed surface scan, aborts the Scan
    after the maximum is surmounted, chooses the optimized structure
    with highest energy, calculates the second derivative of the scanned
    coordinate and finally performs a TS optimization.

-   If you do not want the scan to be aborted after the highest point
    has been reached but be carried out up to the last point, then you
    have to type:

```orca
%geom
  fullScan true # do not abort the scan with !ScanTS
end
```
:::

As transition state finder we implemented the quasi-Newton like Hessian
mode following
algorithm.{cite}`schlegel1987ab,schlegel1995modern,schlegel1998encyclopedia,eckert1997comp,horn1991comp,baker1986comp,hess2008chem,harvey1998theor,li2002theor`
This algorithm maximizes the energy with respect to one (usually the
lowest) eigenmode and minimizes with respect to the remaining $3N-7$(6)
eigenmodes of the Hessian.

:::{Tip}

-   You can check at an early stage if the optimization will lead to the
    "correct" transition state. After the first optimization step you
    find the following output for the redundant internal coordinates:

```orca
---------------------------------------------------------------------------
                     Redundant Internal Coordinates
                        (Angstroem and degrees)
   Definition                Value    dE/dq     Step   New-Value comp.(TS mode)
----------------------------------------------------------------------------
 1. B(H  1,C  0)              1.2857  0.013136  0.0286    1.3143      0.58
 2. B(H  2,C  0)              1.1002  0.014201 -0.0220    1.0782
 3. B(H  3,C  0)              1.1010  0.014753 -0.0230    1.0779
 4. B(H  4,C  0)              1.1008  0.014842 -0.0229    1.0779
 5. B(O  5,H  1)              1.2442 -0.015421 -0.0488    1.1954      0.80
 6. B(H  6,O  5)              0.9803  0.025828 -0.0289    0.9514
 7. A(H  1,C  0,H   2)        107.38 -0.001418   -0.88    106.49
 8. A(H  1,C  0,H   4)        105.48 -0.002209   -0.46    105.02
 9. A(H  1,C  0,H   3)        103.35 -0.003406    0.08    103.43
10. A(H  2,C  0,H   4)        113.30  0.001833    0.35    113.65
11. A(H  3,C  0,H   4)        113.38  0.002116    0.26    113.64
12. A(H  2,C  0,H   3)        112.95  0.001923    0.45    113.40
13. A(C  0,H  1,O   5)        169.26 -0.002089    4.30    173.56
14. A(H  1,O  5,H   6)        100.84  0.003097   -1.41     99.43
15. D(O  5,H  1,C   0,H   2)   17.02  0.000135    0.24     17.26
16. D(O  5,H  1,C   0,H   4) -104.09 -0.000100    0.52   -103.57
17. D(O  5,H  1,C   0,H   3)  136.64  0.000004    0.39    137.03
18. D(H  6,O  5,H   1,C   0)   10.52  0.000078   -0.72      9.79
----------------------------------------------------------------------------
```
:::

Every Hessian eigenmode can be represented by a linear combination of
the redundant internal coordinates. In the last column of this list the
internal coordinates, that represent a big part of the mode which is
followed uphill, are labelled. The numbers reflect their magnitude in
the TS eigenvector (fraction of this internal coordinate in the linear
combination of the eigenvector of the TS mode). Thus at this point you
can already check whether your TS optimization is following the right
mode (which is the case in our example, since we are interested in the
abstraction of H1 from C0 by O5.

-   If you want the algorithm to follow a different mode than the one
    with lowest eigenvalue, you can either choose the number of the
    mode or you can give an internal coordinate that should be strongly involved
in this mode using the `TS_Mode` keyword.

:::{Tip}
-   If you look for a TS of a breaking bond the respective internal
    coordinate might not be included in the list of redundant internal
    coordinates due to the bond distance being slightly too large,
    leading to slow or even no convergence at all. In order to prevent
    that behavior a region of atoms that are active in the TS search can
    be defined, consisting of e.g. the two atoms of the breaking bond.
    During the automatic generation of the internal coordinates the bond
    radii of these atoms (and their neighbouring atoms) are increased,
    making it more probable that breaking or forming bonds in the TS are
    detected as bonds. See keywords `TS_Active_Atoms` and `TS_Active_Atoms_Factor` in the keywords list below.
:::

(sec:structurereactivity.optimization.transitionstate.hessian)=
### Hessians for Transition State Calculations

For transition state (TS) optimization a simple initial Hessian, which
is used for minimization, is not sufficient. In a TS optimization we are
looking for a first order saddle point, and thus for a point on the PES
where the curvature is negative in the direction of the TS mode (the TS
mode is also called transition state vector, the only eigenvector of the
Hessian at the TS geometry with a negative eigenvalue). Starting from an
initial guess structure the algorithm used in the ORCA TS optimization
has to climb uphill with respect to the TS mode, which means that the
starting structure has to be near the TS and the initial Hessian has to
account for the negative curvature of the PES at that point. The simple
force-field Hessians cannot account for this, since they only know
harmonic potentials and thus positive curvature.

The most straightforward option in this case would be (after having
looked for a promising initial guess structure with the help of a
relaxed surface scan) to calculate the exact Hessian before starting the
TS optimization. With this Hessian (depending on the quality of the
initial guess structure) we know the TS eigenvector with its negative
eigenvalue and we have also calculated the exact force constants for all
other eigenmodes (which should have positive force constants). For the
HF, DFT methods and MP2, the analytic Hessian evaluation is available
and is the best choice, for details see section Frequencies
({ref}`sec:structurereactivity.frequencies`).

When only the gradients are available (most notably the CASSCF), the
numerical calculation of the exact Hessian is very time consuming, and
one could ask if it is really necessary to calculate the full exact
Hessian since the only special thing (compared to the simple force-field
Hessians) that we need is the TS mode with a negative eigenvalue.

Here ORCA provides two different possibilities to speed up the Hessian
calculation, depending on the nature of the TS mode: the Hybrid Hessian
and the calculation of the Hessian value of an internal coordinate. For
both possibilities the initial Hessian is based on a force-field Hessian
and only parts of it are calculated exactly. If the TS mode is of very
local nature, which would be the case when e.g. cleaving or forming a
bond, then the exactly calculated part of the Hessian can be the second
derivative of only one internal coordinate, the one which is supposed to
make up the TS mode (the formed or cleaved bond). If the TS mode is more
complicated and more delocalized, as e.g. in a concerted proton transfer
reaction, then the hybrid Hessian, a Hessian matrix in which the
numerical second derivatives are calculated only for those atoms, which
are involved in the TS mode (for more details, see section
{ref}`sec:structurereactivity.optimization`), should be sufficient. If you are
dealing with more complicated cases where these two approaches do not
succeed, then you still have the possibility to start the TS
optimization with a full exact Hessian.

Numerical Frequency calculations are quite expensive. You can first
calculate the Hessian at a lower level of theory or with a smaller basis
set and use this Hessian as input for a subsequent TS optimization:

```orca
%geom
  inhess   Read                   # this command comes with:
  InHessName "yourHessian.hess"   # filename of Hessian input file
end
```

Another possibility to save computational time is to calculate exact
Hessian values only for those atoms which are crucial for the TS
optimization and to use approximate Hessian values for the rest. This
option is very useful for big systems, where only a small part of the
molecule changes its geometry during the transition and hence the
information of the full exact Hessian is not necessary. With this option
the coupling of the selected atoms are calculated exactly and the
remaining Hessian matrix is filled up with a model initial Hessian:

```orca
%geom
  Calc_Hess true
  Hybrid_Hess {0 1 5 6} end   # calculates a Hybrid Hessian with
                              # exact calculation for atoms 0, 1, 5 and 6
end
```

For some molecules the PES near the TS can be very far from ideal for a
Newton-Raphson step. In such a case ORCA can recalculate the Hessian
after a number of steps:

```orca
%geom
  Recalc_Hess  5   # calculate the Hessian at the beginning
                   # and recalculate it after 5,10,15,... steps
end
```

Another solution in that case is to switch on the trust radius update,
which reduces the step size if the Newton-Raphson steps behave
unexpected and ensures bigger step size if the PES seems to be quite
quadratic:

```orca
%geom
  Trust 0.3 # Trust <0 - use fixed trust radius (default: -0.3 au)
            # Trust >0 - use trust radius update, i.e. 0.3 means: 
            # start with trust radius 0.3 and use trust radius update 
end
```

(sec:structurereactivity.optimizatiom.transitionstate.coords)=
### Special Coordinates for Transition State Optimizations

-   If you look for a TS of a breaking bond the respective internal
    coordinate might not be included in the list of redundant internal
    coordinates (but this would accelerate the convergence). In such a
    case (and of course in others) you can add coordinates to or remove
    them from the set of autogenerated redundant internal coordinates
    (alternatively check the TS_Active_Atoms keyword):

```orca
# add ( A ) or remove ( R ) internal coordinates
%geom
  modify_internal
      { B 10 0 A }      # add a bond between atoms 0 and 10
      { A 8 9 10 R }    # remove the angle defined
                        # by atoms 8, 9 and 10
      { D 7 8 9 10 R }  # remove the dihedral angle defined
  end                   # by atoms 7, 8, 9 and 10
end
```

## ScanTS option

For TS modes of rather local nature (involving only one bond or an
angle; no concerted movements over multiple atoms) we implemented the
ScanTS feature. Here the user can carry out a relaxed surface scan and a
TS optimization in one calculation. After the relaxed surface scan the
algorithm chooses the optimized structure of the scan with highest
energy as initial guess structure and the two neighbouring structures
for the calculation of the second derivative of the scanned coordinate
(e.g., if scan step number 4 gives the structure with highest energy,
then structure `basename.004.xyz` is the initial guess for the TS
optimization; the structures `basename.003.xyz` and `basename.005.xyz`
are used for the calculation of the second derivative). Before the first
step of the subsequent TS optimization the energies and gradients for
all three structures are calculated. The gradients are then transformed
to internal coordinates. The diagonal Hessian value of the scanned
coordinate is then calculated via finite difference of the internal
gradients of the two given structures (003 and 005 in our example).

For the construction of the initial Hessian a model force field Hessian
is built up (this Hessian has got only diagonal entries and zeros as
off-diagonal elements). The exactly calculated diagonal Hessian value
replaces the model force field Hessian entry for the respective internal
coordinate.

If the user already performed a regular relaxed surface scan without the
subsequent TS optimization, then he can nevertheless use these
structures for the same procedure. A relaxed surface scan always gives
you the xyz-files and gbw-files of the optimized structures of each scan
step. A separate TS optimization can be carried out where the structure
with highest energy is the starting structure. Additionally the two
files with the two adjacent structures (as explained above) have to be
provided (via the Hess_Internal keyword, see below). Furthermore, the
internal coordinate, for which the diagonal Hessian value has to be
calculated, has to be given (the previously scanned coordinate). This
exact Hessian calculation is only possible for one internal coordinate:

```orca
%geom
  Hess_Internal
     {B 1 0 C}               # previously scanned coordinate
     XYZ1 "scanName.003.xyz" # the xyz-files of the structures
     XYZ2 "ScanName.005.xyz" #  next to the highest energy point
     GBW1 "ScanName.003.gbw" # the gbw-files of the structures
     GBW2 "ScanName.005.xyz" #  next to the highest energy
                             # the gbw-files are optional
   end
end
```

Additionally the manipulation of the diagonal Hessian values of the
internal Hessian is possible for further internal coordinates, but
without an extra calculation. Here the user can just define a value (in
Eh/Bohr$^2$).

```orca
Hess_Internal
  {A 3 2 1 D 2.0} # define a diagonal Hessian value of
                  #  2 Eh/Bohr2 for the angle between
                  #  atoms 3 2 1
  {B 1 0 D -0.5}  # define a diagonal Hessian value of
                  #  -0.5 Eh/Bohr2 for the bond between
                  #  atoms 1 and 0
end
```

The definition of such Hessian (diagonal) elements is possible for
multiple internal coordinates. These just replace the values of the
force field model Hessian.

(sec:structurereactivity.geomopt.hybridhess)=
## Hybrid Hessian

We implemented the calculation of a "Hybrid Hessian" as an alternative
to the full Hessian calculation for TS optimization. Here only those
parts of the Hessian, that are important for the TS optimization, are
calculated exactly. For this calculation we define two kinds of atoms:
atoms whose couplings with the other atoms are treated exactly (E) and
atoms whose couplings are treated approximately (A).

In a first step an Almloef model Hessian is built up in redundant
internal coordinates and transformed to Cartesian coordinates. This
Hessian gives the second derivative elements for atom pairs A/A. In a
second step the second derivative elements between pairs E/E and E/A are
calculated numerically as in a numerical frequency calculation:

$$\frac{\boldsymbol{\Delta E} }{\Delta i_{B} \Delta j_{C} }=\frac{\boldsymbol{\Delta E} }{\Delta j_{C} \Delta i_{B} }=\frac{g_{j,C}^{i,B} -g_{j,C}^{eq.}}{displ.}
$$ (eqn:205)

with:

|                 |                                                                                    |
|:----------------|:-----------------------------------------------------------------------------------|
| $i,j$           | x-, y- or z-direction                                                              |
| $B,C$           | pairs of E/E, E/A, A/E                                                             |
| $displ.$        | magnitude of displacement                                                          |
| $g_{j,C}^{eq.}$ | force on atom $C$ in direction $j$ in current geometry                             |
| $g_{j,C}^{i,B}$ | force on atom $C$ in direction $j$ after displacement of atom $B$ in direction $i$ |


(sec:structurereactivity.geomopt.partialhess)=
## Partial Hessian Vibrational Analysis

We implemented the Partial Hessian Vibrational Analysis (PHVA), as
published by Li, Jensen in {cite}`li2002theor`, for the analysis of the
nature of stationary points of structures obtained with QM/MM
optimizations.

```orca
# PHVA after a QM/MM optimization in the (dispersion-/PC-) field
# caused by the MM-atoms
! NumFreq
%LJCoefficients "temp.LJ" # file with the Lennard Jones
                          #  coefficients for dispersion interaction
                          # obtained from last QM/MM run
%pointcharges "temp.pc"   # file with the point charges for
                          #  electrostatic interaction
                          # obtained from last QM/MM run
 #
%freq
    PARTIAL_Hess {0 1 2}  # atoms which are "frozen" and which make
                          #  the boundary to the MM-system
     end
   end
```

:::{note}
-   This procedure should be used for QM/MM optimized structures only to
    verify the nature of the stationary point and have an estimate of
    the ZPE.
:::

Here we shortly describe the procedure: In PHVA we divide the system
into two parts $B$ (of size $n$ atoms) and $C$ (size $N-n$). Let the
atom set $B$ belong to the region where the chemical change is
localized. The Partial Hessian matrix is built up as follows:

$$\begin{pmatrix}
K_{BB} & 0  \\
 0  & K_{CC}^{\varepsilon }\\
\end{pmatrix}
$$ (eqn:206)

With:

$$K_{BB} \quad : x,y,z \quad \text{direction}$$

$$K_{CC}^{\varepsilon } =
\begin{pmatrix}
\varepsilon & 0 & 0 \\
 0 & \ddots & 0  \\
 0  & 0 & \varepsilon \\
\end{pmatrix}, \, \varepsilon =10^{-8} \, \text{au},
$$ (eqn:207)

this corresponds to using near-infinite masses for the atoms in $C$.

With this procedure we get the following eigenvalue structure:

-   Six zero eigenvalues with modes corresponding to translational and
    rotational motion of the entire molecule.

-   $3(N - n) - 6$ small (less than 1 cm$^{-1})$ eigenvalues with modes
    corresponding mainly to internal motion within region $C$.

-   Three eigenvalues (typically less than 10 cm$^{-1})$ with modes
    corresponding mainly to motion of region $C$ relative to region $B$.

-   $(3n - 3)$ eigenvalues with modes corresponding mainly to relative
    motion of $B$ and $C$ as well as internal motion within region $B$.


(sec:structurereactivity.optimization_ts.keywords)=
## Tranistion State Theory Keywords

:::{raw} latex
\begingroup
\footnotesize
:::

:::{tabularcolumns} \Y{0.3}\Y{0.3}\Y{0.4}
:::

(tab:ts.options)=
:::{flat-table} `%geom` block input keywords and options for transition state geometry optimization.
:header-rows: 1
:class: footnotesize

* - Keyword
  - Option / Value
  - Description
* - `OptTS`
  - 
  - Transition structure optimization. Included as `!OptTS`
* - `Scan`
  - 
  - Must include `!ScanTS` for transition state scan.
* - 
  - `B 1 2 = v1, v2, N`
  - Scan atom 1 to atom 2 bond distance from v1 to v2 in N steps.
* - 
  - `B 1 2 [v1 v2 ...]`
  - Scan atom 1 to atom 2 bond with custom step values.
* - 
  - `A 1 2 3`
  - Scan an angle using atoms 1,2,3.
* - 
  - `D 1 2 3 4`
  - Scan a dihedral of atoms 1,2,3,4.
* - `Simul_Scan`
  - `true`
  - Enable simultaneous multidimensional scans (up to 3 coordinates).
* - `FullScan`
  - `true`
  - Forces full surface scan before TS optimization (`!ScanTS`).
* - `TS_search`
  - `EF`
  - Enable TS search using Eigenvector Following.
* - `TS_Mode`
  - `{M 0}`
  - Follow eigenvector 0 (lowest mode).
* - 
  - `{B 0 1}`
  - Follow bond between atoms 0 and 1.
* - 
  - `{A 2 1 0}`
  - Follow angle between atoms 2, 1, and 0.
* - 
  - `{D 3 2 1 0}`
  - Follow dihedral between atoms 3, 2, 1, and 0.
* - `TS_Active_Atoms`
  - `{ 1 2 3 }`
  - Atoms that are involved in TS, e.g. for proton transfer the proton, its acceptor and its donor
* - `TS_Active_Atoms_Factor`
  - `1.5`
  - Factor by which the cutoff for bonds is increased for the above defined atoms. Default 1.5, i.e. increased by 50%
* - `inhess`
  - `unit`
  - Start optimization with a unit matrix Hessian.
* - 
  - `Read`
  - Read Hessian from external file. Requires `InHessName`.
* - `InHessName`
  - `"filename.hess"`
  - Specifies file containing the Hessian (e.g., `.hess`, `.opt`, `.carthess`).
* - 
  - `Lindh`
  - Use Lindh’s model Hessian (only for redundant coordinates).
* - 
  - `Almloef`
  - Use Almloef’s model Hessian.
* - 
  - `Schlegel`
  - Use Schlegel’s model Hessian.
* - 
  - `Swart`
  - Use Swart and Bickelhaupt’s model Hessian.
* - 
  - `XTB0`
  - Use GFN0-xTB Hessian.
* - 
  - `XTB1`
  - Use GFN1-xTB Hessian.
* - 
  - `XTB2`
  - Use GFN2-xTB Hessian.
* - 
  - `GFNFF`
  - Use GFN-FF Hessian.
* - `Calc_Hess`
  - `true`
  - Calculate numerical Hessian at the beginning of optimization.
* - `Recalc_Hess`
  - `5`
  - Recalculate Hessian every 5 cycles.
* - `Hybrid_Hess`
  - `{0 1 5 6} end`
  - Calculate exact Hessian for specified atoms, use model for the rest.
* - `NumHess`
  - `true`
  - Request numerical Hessian.
* - `Hess_Internal`
  - `{A 3 2 1 D 2.0}`
  - Manually set Hessian value (Eh/Bohr²) for angle between atoms 3-2-1.
* - 
  - `reset 5`
  - Reset modified Hessian values after 5 cycles.
* - 
  - `{B 1 0 C}`
  - Coordinates for Hessian refinement after a relaxed surface scan.
* - 
  - `XYZ1` `"scanName.003.xyz"`
  - Structure file before maximum in scan.
* - 
  - `XYZ2` `"ScanName.005.xyz"`
  - Structure file after maximum in scan.
* - 
  - `GBW1` `"ScanName.003.gbw"`
  - Optional GBW file before max in scan.
* - 
  - `GBW2` `"ScanName.005.xyz"`
  - Optional GBW file after max in scan.
* - `Update`
  - `Powell`
  - Use Powell update for Hessian.
* - 
  - `Bofill`
  - Use Bofill update (default for TS optimization).
* - 
  - `BFGS`
  - Use BFGS update (default for geometry optimization).
* - `HESS_Modification`
  - `Shift_Diag`
  - Shift diagonal elements of Hessian (default).
* - 
  - `EV_Reverse`
  - Reverse sign of diagonal elements.
* - `HESS_MinEV`
  - `0.0001`
  - Minimum allowed Hessian eigenvalue.
* - `NResetHess`
  - `20`
  - Rebuild model Hessian after 20 steps (BFGS only).
* - `NStepsInResetHess`
  - `5`
  - Number of previous steps used to inform new model Hessian.
* - `Trust`
  - `-0.3`
  - Use fixed trust radius of 0.3 au (negative sign indicates fixed).
* - `modify_internal`
  - `{B 10 0 A}`
  - Add bond between atoms 0 and 10.
* - 
  - `{A 8 9 10 R}`
  - Remove angle between atoms 8, 9, and 10.
* - 
  - `{D 7 8 9 10 R}`
  - Remove dihedral between atoms 7, 8, 9, and 10.
:::
:::{raw} latex
\endgroup
:::
