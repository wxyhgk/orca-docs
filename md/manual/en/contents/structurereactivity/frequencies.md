```{index} Vibrational Frequencies
```

(sec:structurereactivity.frequencies)=
# Vibrational Frequencies

Vibrational frequency calculations are available through analytical
differentiation of the SCF energy as well as one- or two-sided numerical
differentiation of analytical gradients, i.e. for Hartree-Fock and DFT
models. For methods without analytical gradient, a numerically calculated
gradient can be used (keyword `NumGrad`) for numerical frequencies.
Please note that this will be a very time-consuming calculation.

At present, analytical Hessians can be calculated for SCF only.
However, there are some additional restrictions. Analytical Hessians
cannot be performed for:

- Double-Hybrid functionals 
- RI-JK approximation       

Note that there is a separate section of the manual dedicated to vibrational spectroscopy
(see section {ref}`sec:spectroscopyproperties.vib`) that contains further examples and
describes the calculation of anharmonic effects, Raman spectra, NRVS and things like
isotope shifts or visualizing normal modes. 

The use of vibrational frequency calculations is fairly simple:

```{literalinclude} ../../orca_working_input/C05S03_148.inp
:language: orca
```

At the end of the frequency job you get an output like this:

```orca
-----------------------
VIBRATIONAL FREQUENCIES
-----------------------

   0:         0.00 cm**-1
   1:         0.00 cm**-1
   2:         0.00 cm**-1
   3:         0.00 cm**-1
   4:         0.00 cm**-1
   5:         0.00 cm**-1
   6:       311.78 cm**-1
   7:       887.65 cm**-1
   8:      1225.38 cm**-1
   9:      1394.81 cm**-1
  10:      3624.88 cm**-1
  11:      3635.73 cm**-1
```

This output consists of the calculated vibrational frequencies, the
vibrational modes and the thermochemical properties at 298.15 K. In the
example above there are six frequencies which are identically zero.
These frequencies correspond to the rotations and translations of the
molecule. They have been projected out of the Hessian before the
calculation of the frequencies and thus, the zero values do not tell you
anything about the quality of the Hessian that has been diagonalized.
The projection can be turned off by `PROJECTTR FALSE` under %FREQ, so that
the frequencies of the translations and rotations can deviate from zero and
the deviations represent a metric of the numerical error of the Hessian
calculation. This is done automatically when there is e.g. an external
electric field that makes the exact translational and/or
rotational modes have non-zero frequencies (see section {ref}`sec:essentialelements.finEfield`).
However, in normal cases where the molecule is expected to obey
both translational and rotational invariance, it is **strongly discouraged**
to turn off `PROJECTTR` when calculating thermochemical quantities
(especially entropies and Gibbs free energies). This is because when the
frequencies of translational and rotational modes exceed `CutOffFreq`
(which is 1 cm$^{-1}$ by default), their contributions to the partition
function will be calculated using the formulas for vibrations. As a
result, the calculated entropy is inaccurate (due to treating translations
and rotations as vibrations), is sensitive to numerical noise, and in
particular exhibits a finite jump when the (theoretically zero) frequencies
of the translational and rotational modes cross `CutOffFreq`. Therefore,
the only case where the user needs to turn off `PROJECTTR` manually is
when the exact Hessian is expected to have zero translational and rotational
frequencies, and one wants to check how much the translational and rotational
eigenvalues of the actually computed Hessian deviate from zero. The
thermochemical quantities from such a calculation are less reliable
and should not be used; even if they differ considerably from the results
with `PROJECTTR TRUE`, this does not necessarily mean that the latter are
unreliable.

Without `PROJECTTR FALSE`, the reliability of the calculated frequencies has to be judged by
comparison of calculations with different convergence criteria,
increments, integration grids etc. The numerical error in the
frequencies may reach 50 cm$^{-1}$ but should be considerably smaller in
most cases. Significant negative frequencies indicate saddle points of
the energy hypersurface and prove that the optimization has not resulted
in an energy minimum.

OBS: By default, the Hessian is made translation invariant by applying
the "acoustic sum rule" ({cite}`shang_moving-grid_2020`), which reduces the
effect of noise from numerical integration coming from DFT or COSX,
except for the Partial and Hybrid Hessians where it does not make sense.
It can be set to false by using TRANSINVAR FALSE under %FREQ.

(sec:structurereactivity.frequencies.massdependencies)=
## Mass dependencies

Of course the calculated frequencies depend on the masses used for each
atom. While this can be influenced later through the `orca_vib` routine
(see Section
{ref}`sec:spectroscopyproperties.vib.isotopeshifts` for more detail)
and individually for each atom in the geometry input, one might prefer
using a set of precise atomic masses rather than the set of atomic
weights (which are set as default). This can be achieved through the
`!Mass2016` keyword, which triggers Orca to use those atomic masses
representing either the most abundant isotope or the most stable isotope
(if all isotopes are unstable) of a certain element (e.g. the mass of
$^{35}Cl$ for chlorine or the mass of $^{98}Tc$).

:::{Note}
The calculation of numerical frequencies puts rather high
demands on both computer time and accuracy. In order to get reliable
frequencies make sure that:

-   Your SCF is tightly converged. A convergence accuracy of at least
    10$^{-7}$ Eh in the total energy and 10$^{-6}$ in the density is
    desirable.

-   Grids of at least `DEFGRID2` (default) are used.

-   The use of two-sided (i.e. central) differences increases the
    computation time by a factor of two but gives more accurate and
    reliable results.

-   Small auxiliary basis sets like DGauss/J or DeMon/J may not result
    in fully converged frequencies (up to 40 cm$^{-1}$ difference
    compared to frequencies calculated without RI). The def2/J universal
    auxiliary basis sets of Weigend that are now the default in ORCA (or
    the SARC/J for scalar relativistic calculations) are thought to give
    sufficiently reliable results.

-   Possibly, the convergence criteria of the geometry optimization need
    to be tightened in order to get fully converged results.

-   If you can afford it, decrease the numerical increment to 0.001 Bohr
    or so. This puts even higher demands on the convergence
    characteristics of the SCF calculation but should also give more
    accurate numerical second derivatives. If the increment is too small
    or too high inaccurate results are expected.
:::

The calculation of analytical frequencies is memory-consuming. To
control memory consumption the `%maxcore` parameter must be set. For
example, `%maxcore 8192` - use 8 Gb of memory per processor for the
calculation. The user should provide the value according to the computer
available memory. The batching based on `%maxcore` parameter will be
introduced automatically to overcome probable memory shortage.

Numerical frequency calculations are restartable (but analytical
frequency calculations are not). If the numerical frequencies job died
for one reason or another you can simply continue from where it stopped
as in the following example:

```{literalinclude} ../../orca_working_input/C05S03_150.inp
:language: orca
```

:::{Note}

-   You must not change the level of theory, basis set or any other
    detail of the calculation. Any change will produce an inconsistent,
    essentially meaningless Hessian.

-   The geometry at which the Hessian is calculated must be identical.
    If you followed a geometry optimization by a frequency run then you
    must restart the numerical frequency calculation from the optimized
    geometry.

-   Numerical frequencies can be performed in multi-process mode. Please
    see section
    {ref}`sec:essentialelements.parallel.calling` ("Hints on the use of parallel
    ORCA") for more information.

-   The restart of Numerical frequencies will take off from the result
    files produced during the preceding run (`BaseName.res.%5d.Type`,
    whith `Type` being `Dipoles`, `Gradients` - and if requested
    `Ramans` or `Nacmes`). Please make sure that all these local result
    files get copied to your compute directory. If restart is set and no
    local files to be found, ORCA will restart from scratch. If ORCA
    finds a Hessian file on disk, it will only repeat the subsequent
    analysis.

-   The Hessian can be transformed to redundant internal coordinates.
    More information can be found in section
    {ref}`sec:structurereactivity.optimization.internalcoords`.
:::

(sec:structurereactivity.frequencies.scalingfactors)=
## Scaling factors for computed frequencies

When comparing computed vibrational frequencies to experiment, effects that are
not regarded in the harmonic approximation are often corrected for by scaling
the computed harmonic freuquencies. 

First of all, a standard frequency calculation has to be carried out.
After that, a .hess file can be found on disk. This file contains a line
with the frequency scaling factor, that can be changed manually:

```orca
$frequency_scale_factor
  0.90      <<<---- you change this to whatever you want
```

then, running `orca_vib` is required:

```orca
orca_vib  myjob_scaled_freq.hess
```

The program reads the Hessian, diagonalizes it and applies the
scaling factor. Whatever scaling factor was used in the actual input
that generated the Hessian is irrelevant since the Hessian is
re-diagonalized. To avoid confusion, we recommend that if the goal is to
play with the scaling factor, leave the scaling factor in the
input at 1.0. Nothing bad happens if you don't though.

(sec:structurereactivity.frequencies.restart)=
## Restarting Numerical Frequency calculations

To restart a numerical frequencies calculation, use:

```orca
%FREQ 
  restart true
END
```

and ORCA will look for basename.res.{} files in the same folder where the
calculation is being run, check for what has already been done and
restart where it is needed.


(sec:structurereactivity.frequencies.keywords)=
## Frequencies keyword list

In the ORCA program package, the calculation of frequencies through
the numerical or analytical Hessian is done via the `orca_numfreq` module and
the combination of the `orca_propint`, `orca_scfresp`, and `orca_prop` modules, respectively.

The parameters to control these frequency calculations can be specified
in the %freq-block.
Relevant simple input keywords are given in 
{numref}`tab:structurereactivity.frequencies.keywords.simple`.

```orca
%freq

  # Flags to switch frequencies calculation on/off
        
  NumFreq    false   # numerical frequencies (available for all methods)
  AnFreq     false   # analytical frequencies (available for HF, DFT)
                     # (One of these options has to be set to true,
                     #  to request a freq calculation)
        
  ScalFreq   1.0     # Scaling factor for frequencies (default = 1.0)
                     # NOTE: Scaling is applied to the frequencies after they are 
                     #       calculated. SCALED frequencies will be stored in the 
                     #       .hess file and printed in the output file. 
                     #       In the .hess file you have accesss to the frequency 
                     #       scaling factor (see below). 
                             

  # Flags to control NumFreq calculation:
                                          
  CentralDiff  true    # use central differences [f(x+h)-f(x-h)]/2h - or - 
                       # use one-sided differences [f(x+h)-f(x)]/h 
  Restart      false   # restart a (numerical) frequency calculation
  DX           0.005   # increment h
  Increment    0.005   # increment h

  Hybrid_Hess  {...} end # calculate (numerical) Hybrid Hessian 
  Partial_Hess [...] end # calculate (numerical) Partial Hessian
        
        
  # Flags to control subsequent vibrational analysis:
        
  QuasiRRHO       true   # Evaluate Vibrational Entropy with 
                         # Quasi-Rigid Rotor Harmonic Oscillator
  QRRHORefFreq    25     # reference frequency used in the QuasiRRHO in cm-1
                         # default value is 100 from original paper
  CutOffFreq      1.0    # Threshold for frequencies to be considered 
                         # in spectra, thermochemistry and printout (cm-1)
  Temp        298.15     # run the thermochemistry calculations at user-defined
                         # temperatures (max 16 temperatures, separated by ',')
  T    290, 292, 295     # same as Temp
  
  XTBVPT2     True       # use XTB for the VPT2 correction of the IR 
  Delq           0.5     # the displacement in dimensionless coordinates used 
                         # during the VPT2
  
  TransInvar  True       # enforce translation invariance after
                         # calculating the Hessian?
  NumHessTransInvar True # enforce translation invariance while
                         # calculating the Hessian?
                  # NOTE: TransInvar does not reduce the computational cost of the
                  # Hessian, and can be applied to analytic as well as numeric
                  # Hessians. NumHessTransInvar reduces the number of gradients
                  # that need to be calculated by 6 (for two-sided differentiation)
                  # or 3 (for one-sided differentiation) for numeric Hessians, but
                  # has no effect for analytic Hessians.
  ProjectTR   True       # project out translation and rotation degrees of freedom
                         # in frequency calculation and thermochemistry analysis?
  
          
end
```


:::{raw} latex
\begingroup
\footnotesize
:::
(tab:structurereactivity.frequencies.keywords.simple)=
:::{flat-table} Simple input keywords for vibrational frequency calculation
:class: footnotesize
* - Keyword
  - Description
* - `Freq`
  - Perform an analytic frequency calculation (Alias: `AnFreq`)
* - `NumFreq`
  - Perform a numerical frequency calculation
* - `Mass2016`
  - Use the latest (2016) atomic masses of the most abundant or most stable isotopes 
    instead of atomic weights
:::
:::{raw} latex
\endgroup
:::
