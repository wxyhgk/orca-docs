<a id="sec:essentialelements.numericalintegration"></a>
# Numerical Integration

Starting from its version 5.0, ORCA has a new scheme for the quadratures
used in numerical integration. It is based on the same general ideas
which were used for the old grids, except that we used machine learning
methods, together with some final hands-on optimization, to find the
optimal parameters for all atoms up to the 6th row of the periodic
table, with the 7th row being extrapolated from that. For further
details look at Ref. [Helmich-Paris2021a](../../bibliography.md). We also realized that the
COSX and DFT grids have overall different requirements, and these were
optimized separately.

The big advantage of this new scheme is that it is significantly more
accurate and robust than the old one, even if having the same number of
grid points. We tested energies, geometries, frequencies, excitation
energies and properties to develop three new grid schemes named:
DEFGRID1, DEFGRID2 and DEFGRID3, that will automatically fix all grids
that are used in the calculations. DEFGRID1 behaves essentially like the
old defaults, but it is more robust. The second is the new default, and
is expected to yield sufficiently small errors for all kinds of
applications. The last is a heavier,
higher-quality grid, that is close to the limit if one considers an
enormous grid as a reference.

In order to change from the default DEFGRID2, one just needs to add
!DEFGRID1 or !DEFGRID3 to the main input.

It is also important to note that the COSX approximation is now the
default for DFT, whenever HFexchange is neede. This can always be
turned off by using !NOCOSX.

# Details on the Numerical Integration Grids

As in all other popular grid schemes, our grids are constructed from
assembling a set of atomic grids into a molecular one, using Becke's
approach. Each individual atomic grid is build based on optimized
parameters for that atom, and are composed of an angular and a radial
part, that are defined separately.

The whole scheme was updated from ORCA 5.0, but we tried to keep things
as close as possible to the previous one. First, the overall
construction of these grids needs to be explained.

<a id="sec:essentialelements.numericalintegration.anggrid"></a>
## The Angular Grid Scheme

Instead of using a single angular grid throughout the whole atom, most
schemes apply a so-called grid pruning in order to reduce the number of
grid points outside of the most important regions, as we do in ORCA. In
the current scheme, we split the atomic grids into five regions, using
Lebedev grids with the following number of points on each of those:

<a id="tab:anggridscheme"></a>
!!! note "Different angular grid schemes used in ORCA. The numbers indicate the Lebedev grids used."

    | AngularGrid | Region 1| Region 2 | Region 3 | Region 4 | Region 5 |
    |:------------|:-------:|:--------:|:--------:|:--------:|:--------:|
    | **1**       |   14    |   26     |   50     |   50     |   26     |
    | **2**       |   14    |   26     |   50     |   110    |   50     |
    | **3**       |   26    |   50     |   110    |   194    |   110    |
    | **4**       |   26    |   110    |   194    |   302    |   194    |
    | **5**       |   26    |   194    |   302    |   434    |   302    |
    | **6**       |   50    |   302    |   434    |   590    |   434    |
    | **7**       |   110   |   434    |   590    |   770    |   590    |

The ideal cutoffs between those regions were subjected to optimization,
and are defined for all atoms. Whenever we refer to a AngularGrid flag
in ORCA, one of these schemes is chosen.

<a id="sec:essentialelements.numericalintegration.radgrid"></a>
## The Radial Grid Scheme

The number of radial points ($n_r$) for a given atom is simply defined
using the equation first defined by Krack and Köster:

$$

n_r = (15 \times \varepsilon - 40) + b \times ROW

$$

where $\varepsilon$ is called the IntAcc of that grid in ORCA, b is any
number and ROW refers to the row of the periodic table for that atom. In
its original formulation, $b$ was set to $5$, but here it as now
optimized and varies slightly depending on the AngularGrid schemes shown
above.

One important thing to note is that each increase of IntAcc by $1$, adds
$15$ radial points to the atomic grids, as in the previous grid scheme.
These IntAcc values were optimized for each angular grid:

<a id="tab:intaccs"></a>
!!! note "Optmimized IntAcc parameters for the exchange-correlation and COSX grids."

    | AngularGrid | XC | COSX |
    |:-----------------------------------------|:-------------------------------:|:---------------------------------:|
    | **1**      |              4.004              |3.816|
    | **2**      |              4.004              |4.020|
    | **3**      |              4.159              |4.338|
    | **4**      |              4.388              |4.871|
    | **5**      |              4.629              |4.871|
    | **6**      |              4.959              |4.871|
    | **7**      |              4.959              |4.871|

After defining the number of radial points $n_r$, the actual radial grid
is then defined from a Gauss-Chebyschev quadrature using the so-called
M3 mapping from Treutler and Ahlrich:

$$

r = \frac{\xi}{ln 2} ln \frac{2}{1-x}

$$

where $-1 \le x \le 1$, and the center of the grid ($x=0$) coincides
with the value of $\xi$. These $\xi$ parameters were also optimized for
each atom type.

<a id="sec:essentialelements.numericalintegration.defgrid"></a>
## The DEFGRIDs

With all that in mind, we can now present how the DEFGRIDs are built in
terms of their AngularGrid scheme and IntAccs, which define the angular
and radial parts of the atomic grids. More details can be found in
Ref. [Helmich-Paris2021a](../../bibliography.md).

<a id="tab:defgrids"></a>
!!! note "Angular grid schemes used in different part of ORCA. The XC and COSX grids are separated by a slash, and multiple COSX grid schemes are separated by a comma."

    | Grid Name    | SCF         | TD-DFT | CP-SCF | MP2 grad | MP2 2ndder |
    |:-------------|:-----------:|:------:|:------:|:--------:|:----------:|
    | **DEFGRID1** | 3 / 1, 1, 2 | 1 / 1  | 1 / 1  | 3        | 1          |
    | **DEFGRID2** | 4 / 1, 2, 3 | 1 / 1  | 1 / 1  | 4        | 4          |
    | **DEFGRID3** | 6 / 2, 3, 4 | 3 / 2  | 3 / 2  | 5        | 4          |

OBS.: The IntAccs for TD-DFT and the CP-SCF are 3.467 for the XC and
3.067 for the COSX instead of the default. These numbers can be smaller
here and we exploit this to increase the overall speed.

From the [tab:defgrids](#tab:defgrids) one can see, for instance, that the default
SCF XC grid now is defined from AngularGrid 4 (with no extra final
integration in the end). The default COSX uses a 1,2,3 grid scheme, with
the COSX third grid being used to update the energy after the SCF
converges and for the gradients.

<a id="sec:essentialelements.numericalintegration.detailsandoptions"></a>
## Other Details and Options

**The new adaptive pruning.** The current pruning scheme uses lower
grids close to the nucleus, and far away from the bonding region.
However, if the basis set has polarized functions close to the nuclei,
or diffuse Gaussians, this might not be sufficient.

To improve the grids for these problems, we now use by default an
adaptive pruning scheme, that detects core-polarization, diffuse
functions and steep basis set orbitals by analyzing the expectation
value of the position operator, $\langle \hat r  \rangle$, and fixes the
grid accordingly. This can increase the grids in these cases by 10-20%,
but gives significantly better results. To use the non-adaptive scheme,
just set %METHOD GRIDPRUNING OLDPRUNING END. For a completely unpruned
grid, set GRIDPRUNING to UNPRUNED.

**A simpler Gauss-Legendre angular grid.** By setting AngularGrid to
$0$, instead of using the Lebedev grids, a Gauss-Legendre angular grid
will be built, as suggested by Treutler and Ahlrich [treutler1994chem](../../bibliography.md).
The number of $\theta$ points is defined as $0.4 n_r$ by default and the
number of $\phi$ points is chosen as to avoid crowding close to the
poles.

These grids are in general less efficient than the Lebedev's, but are
useful if one needs to construct extremely large grids for specific
applications.

**The SpecialGrid Option.** Sometimes, you might want to increase the
integration accuracy for some atoms that need special care, while it is
not necessary to enlarge the grid generally. ORCA provides you with a
basic mechanism to increase the radial integration accuracy for a few
atoms while maintaining the chosen grid for all others.

```orca
%METHOD
   # a maximum of 64 assignments can be made
   #  in = 0 : no changes are made
   #  in > 0 : the grid will be changed for all atoms with
   #           atomic number=in to IntAcc=an
   #  in < 0 : only the specific n'th atom will have its
   #           IntAcc value changed to an
   SpecialGridAtoms  i1, i2, i3,...,in;
   SpecialGridIntAcc a1,a2,a3,...,an;
END
```

OBS.: Starting from ORCA 5.0 it is not necessary to use this option
anymore unless you have very specific reasons. The basis set is
considered during the grid construction and that is automatically
extended if needed.

<a id="sec:essentialelements.numericalintegration.SCFkeys"></a>
## SCF Grid Keyword List

A complete description of the SCF grid options is given below. There are
keywords specific to the XC integration, COSX integration and a general
part that applies to all:

```orca
%METHOD
# XC grids
AngularGrid    1    #Lebedev50
               2    #Lebedev110
               3    #Lebedev194
               4    #Lebedev302
               5    #Lebedev434 
               6    #Lebedev590 
               7    #Lebedev770 
               0    #SimpleGrid 
IntAcc         5.0  # determines no. of radial points

# COSX grids
AngularGridX   1,1,2,4,5    # the first three are used in the SCF
                            # the 4th in the MP2 gradient and
                            # the 5th for MP2 second derivatives
IntAccX        3.56,-1,4.5  # if a -1 is given, the default IntAcc is used.

# General
NThetaMax      0.4          # only for AngularGrid=0, multiplier for nr
GridPruning    Unpruned     # no Pruning
               OldPruning   # the old pruning
               Adaptive     # default (and recommended)
HGridReduced   true         # Reduce grids for H and He by one
                            # unit (default and recommended)
BFCut          1e-10        # basis fcn. cut. Is adjusted according to
                            # convergence tolerances
WeightCut      1e-14        # grid weight cut. default: 1e-14
END
```

<a id="sec:essentialelements.numericalintegration.gridothers"></a>
## Changing TD-DFT, CP-SCF and Hessian Grids

**TD-DFT.** The grids used in CIS or TD-DFT can be changed in their
respective block:

```orca
%TDDFT  # or %CIS, they are equivalent
  # XC grids
  IntAccXC 3.467
  GridXC   1

  #COSX grids
  IntAccX  3.076
  GridX    1
END
```

**CP-SCF.** The CP-SCF grids are changed in the %METHOD block:

```orca
%METHOD 
  # XC grids
  Z_IntAccXC  3.467
  Z_GridXC    1

  #COSX grids
  Z_IntAccX   3.076
  Z_GridX     1
  Z_GridX_RHS 2
END
```

OBS.: The Z_Grid_RHS is only used in MP2 and the number here has a
different meaning. It refers to which of the COSX grids used in the SCF
will be chosen, rather than an AngularGrid scheme. The default is to use
the second COSX grid.

**Hessian.** The XC grids used to compute the DFT terms in the Hessian
are automatically chosen to be one unit higher than the SCF grids.
Because of the second derivative terms, we found that it is better to
have a slightly higher XC grid here. The COSX grid can be changed
freely:

```orca
%FREQ 
  HessGridX = 2,2,2,2
END
```

These four numbers refer to the possible usages of COSX in the Hessian,
as explained in Sec.
[sec:structurereactivity.frequencies](#sec:structurereactivity.frequencies)

**Non-local functionals (VV10 and alike).** The default non-local grid
is defined by AngularGrid 2, and is not recommended to be changed. In
any case, these can be altered by using:

```orca
%METHOD
  # non-local grids
  VdwAngularGrid    2        # same scheme as the SCF ones
  VdWIntAcc         5.0      # determines no. of radial points
  VdwGridPruning    Adaptive # default
  VdwDistTCut       10       # cutoff distance between grid points, in angstroem
END
```

<a id="sec:essentialelements.numericalintegration.whenchangedefault"></a>
## When to Change from the Default Grids?

In general, the errors from the default grids are rather small and
reasonable for most applications. After benchmarking against the GMTNK55
test set with the default !DEFGRID2, we found an error of about
$0.01 \pm 0.03$ kcal/mol from DFT (compared to a reference grid), and
$0.05 \pm 0.10$ kcal/mol for the COSX (compared to the analytical
integration). We also benchmarked geometries, excitation energies and
frequencies, and all errors are systematically low.

However, there might still be cases where an improved grid is needed:

-   If you need to be confident that your energy error is below 0.2
    kcal/mol;

-   When dealing with anions with large negative charges ($<-3$);

-   For very subtle intermolecular interactions;

-   When dealing with weird electronic structures;

-   With large conjugated systems - graphene-like structures and large
    polyaromatics.

When needed, the !DEFGRID3 is very large and conservative - it was built
to cover almost all these cases. In contrast, !DEFGRID1 will yield grids
of the size close to previous ORCA versions defaults, but still with
increased accuracy.
