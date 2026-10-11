

<a id="sec:structurereactivity.conicalintersections"></a>
# Conical Intersections

The minima in the conical intersection seam-space between two states
(named here I and J) can be found by using regular geometry optimization
algorithms, except that the gradient to be optimized is
[maeda_updated_2010](../../bibliography.md):

$$
g = g'_{diff}  + Pg_{mean}
$$

where
$g'_{diff} = 2(E_I-E_J)(\partial E_I / \partial q - \partial E_J / \partial q)$
is parallel to the gradient difference vector; $g_{mean}$ is
the gradient mean and $P$ is a projection matrix that projects
out the gradient difference ($x$) and non-adiabatic coupling
($y$) direction components:

$$
P = 1 - x x^T - y y^T
$$

Now we have three approaches to solve this problem in ORCA, that will be
explained next.

<a id="sec:structurereactivity.conicalintersections.gradientprojection"></a>
## Gradient Projection

This is exactly what has been described above,
and will be chosen as default whenever NACMEs between I and J are
available. It is in principle the fastest and most accurate method. It
can be invoked by setting:

```orca
%CONICAL 
  METHOD GRADIENT_PROJECTION  #or simply GP
END
```

OBS.: Turning on the ETF (see Sec. [nacmes.etf](../spectroscopyproperties/tddft.md#sec:spectroscopyproperties.tddft.nacmes.etf)) can improve the
optimization when using the full Gradient Projection method.

<a id="sec:structurereactivity.conicalintersections.gradientprojectionnoacme"></a>
## Gradient Projection without NACME

It is an approximation to the
method above, that one gets by completely neglecting the NACMEs. It is
essentially equivalent to finding a surface crossing point, and will not
necessarily find minima inside the CI seam-space, although the final
$\Delta E_{IJ}$ should be zero.

```orca
%CONICAL 
  METHOD GP_NONACME
END
```

<a id="sec:structurereactivity.conicalintersections.updatedbranchingplane"></a>
## Updated Branching Plane

Here the idea is to start from a guess
NACME, which is any unit vector perpendicular to $x$, and do a
progressive update on it, similar to the BFGS update on the Hessian
[maeda_updated_2010](../../bibliography.md). The "Branching Plane" defined by $x$ and
$y$ then becomes iteratively more accurate until covergence is
achieved. It has been shown to be quite accurate and is the default
whenever NACMEs are not available. Can be used with:

```orca
%CONICAL 
  METHOD UBP
END
```

Finally, the $\Delta E_{IJ}$ energy threshold for the optimization can
be altered with:

```orca
%CONICAL 
  ETOL 1e-4 #default
END
```

As a further example for such an analysis we show the conical intersection
optimization of the ground and first excited state of singlet ethylene.

!!! note "This is currently only available using TD-DFT, will be expanded in"
    future versions. More details about the specific options on
    [spectroscopyproperties.tddft](../spectroscopyproperties/tddft.md#sec:spectroscopyproperties.tddft).

!!! note
    Even though locating the CI of a TD-DFT excited state and the
    reference state is supported, it is not the recommended way of finding
    the ground state-excited state CI, because such CIs are not described
    properly by TD-DFT (in particular, TD-DFT even predicts the wrong
    dimensionality for the intersection space). Instead, it is advised to
    use SF-TD-DFT for this purpose, e.g. use the $T_1$ state as the
    reference state, and calculate both the $S_0$ and $S_1$ states as
    excited states. (*vide infra*)

```mol
title: structure 1
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
6
structure (0 1)
C   0.595560237 -0.010483480 -0.000284187
C  -0.831313750  0.167231832  0.001482505
H  -1.381857976  0.227877089  0.963419721
H   1.265119434  0.874806815  0.006897459
H  -1.382258208  0.243775568 -0.959090898
H   1.027489724 -1.032962768 -0.008829646
--- input ---
!B3LYP DEF2-SVP CI-OPT
%TDDFT IROOT 1 END
* xyz 0 1
C        0.595560237     -0.010483480     -0.000284187
C       -0.831313750      0.167231832      0.001482505
H       -1.381857976      0.227877089      0.963419721
H        1.265119434      0.874806815      0.006897459
H       -1.382258208      0.243775568     -0.959090898
H        1.027489724     -1.032962768     -0.008829646
*
```

!!! note
    You can often use a structure between the optimized structures
    of both states for your CI-optimization. If this doesn't work, you might
    try a scan to get a better initial guess.

The results of the CI-optimization are given in the following output.
The energy difference between the ground and excited state is printed as
E diff. (CI), being reasonably close for a conical intersection. For a
description of the calculation of the non-adiabatic couplings at this
geometry, see section [nacmes.numnacme](../spectroscopyproperties/tddft.md#sec:spectroscopyproperties.tddft.nacmes.numnacme).

```
                                    .--------------------.
              ----------------------|Geometry convergence|-------------------------
              Item                value                   Tolerance       Converged
              ---------------------------------------------------------------------
              Energy change       0.0000164283            0.0000050000      NO
              E diff. (CI)        0.0000025162            0.0001000000      YES
              RMS gradient        0.0000068173            0.0001000000      YES
              MAX gradient        0.0000136891            0.0003000000      YES
              RMS step            0.0000358228            0.0020000000      YES
              MAX step            0.0000821130            0.0040000000      YES
              ........................................................
              Max(Bonds)      0.0000      Max(Angles)    0.00
              Max(Dihed)        0.00      Max(Improp)    0.00
              ---------------------------------------------------------------------

              Everything but the energy has converged. However, the energy
              appears to be close enough to convergence to make sure that the
              final evaluation at the new geometry represents the equilibrium energy.
              Convergence will therefore be signaled now

                        ***********************HURRAY********************
                        ***        THE OPTIMIZATION HAS CONVERGED     ***
                        *************************************************

     --------------------------------------------------------------------------- 
                            Redundant Internal Coordinates

                             --- Optimized Parameters ---  
                               (Angstroem and degrees)

         Definition                    OldVal   dE/dq     Step     FinalVal
     ----------------------------------------------------------------------------
      1. B(C   1,C   0)                1.3254 -0.000005 -0.0000    1.3254
      2. B(H   2,C   1)                1.1270  0.000004 -0.0000    1.1270
      3. B(H   3,C   0)                1.1271 -0.000002  0.0000    1.1271
      4. B(H   4,C   1)                1.1271  0.000000 -0.0000    1.1271
      5. B(H   5,C   0)                1.1271 -0.000002  0.0000    1.1271
      6. A(H   3,C   0,H   5)          106.00  0.000001   -0.00    106.00
      7. A(C   1,C   0,H   5)          126.97 -0.000013    0.00    126.97
      8. A(C   1,C   0,H   3)          127.03  0.000011   -0.00    127.03
      9. A(C   0,C   1,H   4)          127.03  0.000013   -0.00    127.03
     10. A(H   2,C   1,H   4)          106.01 -0.000000    0.00    106.01
     11. A(C   0,C   1,H   2)          127.04  0.000009   -0.00    127.04
     12. D(H   2,C   1,C   0,H   5)    106.86 -0.000005    0.00    106.86
     13. D(H   4,C   1,C   0,H   3)    106.76 -0.000005    0.00    106.76
     14. D(H   4,C   1,C   0,H   5)    -73.62 -0.000004    0.00    -73.61
     15. D(H   2,C   1,C   0,H   3)    -72.76 -0.000005    0.01    -72.76

     ----------------------------------------------------------------------------
                  *******************************************************
                  *** FINAL ENERGY EVALUATION AT THE STATIONARY POINT ***
                  ***               (AFTER   12 CYCLES)               ***
                  *******************************************************
```

<a id="sec:structurereactivity.conicalintersections.ciexcitedstates"></a>
## CI Minima Between Excited States

In an analogous way, the conical
intersection minima between two excited states can be requested by
selection both an IROOT and a JROOT, shown below.

```mol
title: structure 2
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
6
structure (0 1)
C   0.595560237 -0.010483480 -0.000284187
C  -0.831313750  0.167231832  0.001482505
H  -1.381857976  0.227877089  0.963419721
H   1.265119434  0.874806815  0.006897459
H  -1.382258208  0.243775568 -0.959090898
H   1.027489724 -1.032962768 -0.008829646
--- input ---
!B3LYP DEF2-SVP CI-OPT
%TDDFT IROOT 2
       JROOT 1
       #IROOTMULT TRIPLET would search in the triplet PES
       #SF TRUE would search for the S0-S1 CI from a T1 reference, using SF-TD-DFT
       # (but remember to set the multiplicity as 3 instead of 1)
END
* xyz 0 1
C        0.595560237     -0.010483480     -0.000284187
C       -0.831313750      0.167231832      0.001482505
H       -1.381857976      0.227877089      0.963419721
H        1.265119434      0.874806815      0.006897459
H       -1.382258208      0.243775568     -0.959090898
H        1.027489724     -1.032962768     -0.008829646
*
```
