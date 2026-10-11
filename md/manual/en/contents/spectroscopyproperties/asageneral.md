(sec:spectroscopyproperties.asa)=
# Simulation and Fit of Vibronic Structure in Electronic Spectra, Resonance Raman Excitation Profiles and Spectra with the orca_asa Program 

:::{admonition} Deprecated since ORCA 6.0.0
:class: warning
- The `orca_asa` program is no longer supported.
  It is still included in the 6.0.0 release and the documentation is preserved below.
  However, it may not function correctly and will be removed in a future ORCA version!
- The `!NMScan` and `!NMGrad` keywords are still available but these calculations may
  fail or not generate valid input for `orca_asa`. 
  Please use the [ESD module](#sec:spectroscopyproperties.esd) instead, if applicable.
:::


In this section various aspects of the simulation and fit of optical
spectra, including absorption, fluorescence, and resonance Raman are
considered. This part of the ORCA is fairly autonomous and can also be
used in a data analysis context, not only in a "quantum chemistry" mode.
The program is called `orca_asa`, where ASA stands for
"[A]{.underline}dvanced [ S]{.underline}pectral [
A]{.underline}nalysis". The program was entirely designed by Dr. Taras
Petrenko.

The general philosophy is as follows: An ORCA run produces the necessary
data to be fed into the `orca_asa` program and writes an initial input
file. This input file may be used to directly run `orca_asa` in order to
predict an absorption, fluorescence or resonance Raman spectrum.
Alternatively, the input file may be edited to change the parameters
used in the simulations. Last -- but certainly not least -- the
`orca_asa` program can be used to perform a fit of the model parameters
relative to experimental data.

(fig:714)=
```{figure} ../../images/714.*
:height: 400px
```

All examples below are taken from {cite}`petrenko2007analysis`, which must be cited if you perform any work with the `orca_asa` program!

(sec:spectroscopyproperties.asa.general)=
## General Description of the Program

The program input comprises the following information: (1) model and
specification of the model parameters characterizing the electronic
structure of a molecule, as well as lineshape factors; (2) spectral
ranges and resolution for simulations; (3) specification of vibrational
transitions for rR excitation profile and spectra generation; (4)
certain algorithm-selecting options depending on the model; (5) fitting
options.

All optional parameters (1)-(3) are given in the `%sim` block, and
fitting options are in the `%fit` block. The model parameters are
specified within various blocks that will be described below. The
program `orca_asa` is interfaced to ORCA and inherits its input style.
The input for `orca_asa` run can be also generated upon ORCA run.

The current implementation features so called "simple", "independent
mode, displaced harmonic oscillator" (IMDHO), and "independent mode,
displaced harmonic oscillator with frequency alteration" (IMDHOFA)
models.

(sec:spectroscopyproperties.asa.input)=
## Spectral Simulation Procedures: Input Structure and Model Parameters

(sec:spectroscopyproperties.asa.input.simple)=
### Example: Simple Mode

This model represents the simplest approach which is conventionally used
in analysis of absorption spectra. It neglects vibrational structure of
electronic transitions and approximates each individual electronic band
by a standard lineshape, typically a Gaussian, Lorentzian or mixed
(Voigt) function. This model can only make sense if vibrational
progressions are not resolved in electronic spectra. Upon this
approximation the intensity of absorption spectrum depends on the energy
of the incident photon ($E_{L} )$, the electronic transition energy
($E_{T} )$, the transition electric dipole moment
($\mathrm{\mathbf{M} }$, evaluated at the ground-state equilibrium
geometry). Lineshape factors are specified by homogeneous linewidth
$\Gamma$ and standard deviation parameter $\sigma$ corresponding to
Gaussian distribution of transition energies. The following example
illustrates a simple input for simulation of absorption bandshapes using
various intensity and lineshape parameters.

```orca
# example001.inp
#
# Input file to generate absorption spectrum consisting
# of 3 bands   with different lineshape factors:
#
# 1. Lorentzian centered at 18000cm**-1 (damping factor Gamma= 100 cm**-1)
# 2. Gaussian   centered at 20000cm**-1
#    (standard deviation Sigma= 100 cm**-1)
# 3. Mixed Gaussian-Lorentzian band representing Voigt profile
#    centered at 21000 cm**-1

%sim
         Model Simple

         # Spectral range for absorption simulation:
         AbsRange     17000.0,   23000.0

         # Number of points to simulate absorption spectrum:
         NAbsPoints  2000

end


#---------------------------------------------------------------------------
#  Transition        Gamma    Sigma  Transition Dipole Moment (atomic unit)
#  Energy (cm**-1)  (cm**-1) (cm**-1)      Mx          My        Mz
#---------------------------------------------------------------------------

$el_states
3     # number of electronic states
   1  18000.0        100.00      0.0        1.0         0.0       0.0
   2  20000.0          0.00    100.0        1.0         0.0       0.0
   3  22000.0         50.00     50.0        1.0         0.0       0.0
```

The parameters of of the final electronic states reached by the
respective transitions are specified in the `$el_states` block. The
spectral range and resolution used in the calculation are defined by the
`AbsRange` and `NAbsPoints` keywords in `%sim` block. The calculation of
the absorption spectrum is automatically invoked if `NAbsPoints>1`.
After the `orca_asa` run you will find in your directory file
`example001.abs.dat` containing absorption spectrum in simple two-column
ASCII format suitable to be plotted with any spreadsheet program.
Absorption spectra corresponding to individual electronic transitions
are stored in file `example001.abs.as.dat` ( the suffix "`as`" stands
for "All States").

(fig:715)=
```{figure} ../../images/715.*

 Absorption spectrum generated after orca_asa run on file
`example001.inp.` Three bands have different lineshape pararameters.
Note that although all transitions are characterized by the same
transition electric dipole moment their intensities are scaled
proportionally to the transition energies.
```

The output of the program run also contains information about oscillator
strengths and full-width-half-maximum (FWHM) parameters corresponding to
each electronic band:

```orca
----------------------------------------------
   State       EV        fosc    Stokes shift
            (cm**-1)               (cm**-1)
----------------------------------------------
    1:      18000.00   0.054676      0.00
    2:      20000.00   0.060751      0.00
    3:      22000.00   0.066826      0.00


----------------------------------------
   BROADENING PARAMETETRS (cm**-1)
----------------------------------------
   State     Gamma     Sigma      FWHM
----------------------------------------
    1:        100.00      0.00    200.00
    2:          0.00    100.00    235.48
    3:         50.00     50.00    180.07
```

Note that although all three types of lineshape functions are symmetric
this is not true for the overall shapes of individual absorption bands
since the extinction coefficient (absorption cross-section) is also
proportional to the incident photon energy. Therefore, if the linewidth
is larger than 10% of the peak energy the asymmetry of the electronic
band can be quite noticeable.

(sec:spectroscopyproperties.asa.input.imdho)=
### Example: Modelling of Absorption and Fluorescence Spectra within the IMDHO Model

The IMDHO model is the simplest approach that successfully allows for
the prediction of vibrational structure in electronic spectra as well as
rR intensities for a large variety of real systems. This model assumes:

1.  harmonic ground- and excited-state potential energy surfaces;

2.  origin shift of the excited-state potential energy surface relative
    to the ground-state one;

3.  no vibrational frequency alteration or normal mode rotation occurs
    in the excited state;

4.  no coordinate dependence of the electronic transition dipole moment.

In addition to the parameters that enter the "Simple model" defined
above it requires some information about the vibrational degrees of
freedom. The required information consists of the ground-state
vibrational frequencies $\left\{{ \omega_{gm} } \right\}$ and
(dimensionless) origin shifts $\left\{{ \Delta_{mi} } \right\}$, where
$i$ and $m$ refer to electronic states and normal modes respectively.
$\Delta$ is expressed in terms of dimensionless normal coordinates.
Accordingly, for the IMDHO model one has to specify the following blocks

-   The `$el_states` block contains the parameters
    $E_{T}, \Gamma, \sigma, \mathrm{\mathbf{M} }$ for each electronic
    state. By default $E_{T}$ is assumed to be adiabatic minima
    separation energy. Alternatively, it can be redefined to denote for
    the vertical transition energy.This is achieved by specifiying the
    keyword `EnInput=EV` in the `%sim` block.

-   A `$vib_freq_gs` block specifies ground-state vibrational
    frequencies.

-   A `$sdnc` block contains parameters
    $\left\{{ \Delta_{mi} } \right\}$ in matrix form such that the
    $i$-th column represents the dimensionless displacements along all
    normal modes for the $i$-th excited-state PES.

The file `example002.inp` provides the input for simulation of
absorption and fluorescence spectra of a system characterized by
significant displacements of the excited-state origin along 5 normal
coordinates.

```orca
# example002.inp
#
# Input file for simulation  of vibrational structure
# in absorption and fluorescence spectra assuming
# origin shift of excited PES along 5 normal coordinates.
# The simulated spectra closely reproduce the experimental
# optical bandshapes for the tetracene molecule.
#
%sim
     Model IMDHO

     # spectral range for absorption simulation (cm**-1)
     AbsRange    20000.0, 27000.0
     NAbsPoints  2000             # number of points in absorption spectrum

     # spectral range for simulation of fluorescence (cm**-1)
     FlRange     22000.0, 16000.0
     NFlPoints   2000      # number of points in fluorescence spectrum

     # the following options require the spectra to be normalized
     # so that their maxima are equal to 1.0
     AbsScaleMode Rel
     FlScaleMode  Rel   # default  for fluorescence

     # for absorption spectrum the default option is AbsScaleMode= Ext
     # which stands for extinction coefficient

end

#---------------------------------------------------------------------------
#   Transition        Gamma    Sigma  Transition Dipole Moment (atomic unit)
#   Energy (cm**-1)  (cm**-1) (cm**-1)      Mx          My          Mz
#---------------------------------------------------------------------------

$el_states
1
   1  21140.0         50.00    100.0        1.0         0.0         0.0


# Block specifying Stokes Shift parameter for each electronic state
# This information is optional
$ss
1   # number of excited states
  1   300.0      # the Stokes shift for the 1st electronic transition

# Block providing the values of VIBrational FREQuencies
# for 5 Ground-State normal modes.
# Obligatory for IMDHO and IMDHOFA models.
$vib_freq_gs
5
    1      310.0
    2     1193.0
    3     1386.0
    4     1500.0
    5     1530.0


# Block specifying origin Shift of the excite-state PES
# along each normal mode in terms of the ground-state
# Dimensionless Normal Coordinates
# Obligatory for IMDHO and IMDHOFA models.
$sdnc
5 1
               1
     1       0.698
     2      -0.574
     3       0.932
     4      -0.692
     5       0.561
```

The calculation of absorption and fluorescence spectra is automatically
invoked if the parameters `NAbsPoints>1` and `NFlPoints> 1`. The input
file also contains the optional block `$ss `which specifies the Stokes
shift $\lambda$ for each electronic transition. This parameter is equal
to the energy separation between the 0-0 vibrational peaks in the
absorption and fluorescence spectra as shown in {numref}`fig:716` . In general
$\lambda$ accounts for solvent induced effects as well as unresolved
vibrational structure corresponding to low-frequency modes that are not
specified in the input. Note that we have specified parameters
`AbsScaleMode=Rel` and `FlScaleMode=Rel` in `%sim` block in order to
ensure that the simulated spectra are normalized to unity. The
calculated absorption and fluorescence spectra are stored in
`example002.abs.dat` and `example002.fl.dat` files, respectively.

(fig:716)=
```{figure} ../../images/716.*

Absorption and fluorescence spectra generated after `orca_asa` run on
the file `example002.inp.` If the homogeneous broadening is set to be
$\Gamma = 10 \, \text{cm}^{-1}$ one can resolve underlying vibrational
structure and identify various fundamental and combination
transitions.
```

(sec:spectroscopyproperties.asa.input.imdhofa)=
### Example: Modelling of Absorption and Fluorescence Spectra within the IMDHOFA Model

IMDHOFA (Independent Mode Displaced Harmonic Oscillators with Frequency
Alteration) is based on the same assumptions as the IMDHO model except
for vibrational frequency alteration in excited state can take place.
The file `example003.inp` features almost the same input parameters as
`example002.inp`. The IMDHOFA model is invoked by the keyword
`Model=IMDHOFA` in the `%sim` block. Additionally, one has to provide
the obligatory block `$vib_freq_es`. It contains the excited-state
vibrational frequencies $\left\{{ \omega_{emi} } \right\}$ in matrix
form such that the $i$-th column represents the vibrational frequencies
of all normal modes for the $i$-th excited-state PES.

```orca
# Block providing the values of VIBrational FREQuencies
# for 5 Excited-State normal modes.
# Obligatory for IMDHOFA model.

$vib_freq_es
5  1         # number of modes and number of excited states
             1
    1      410.0
    2     1293.0
    3     1400.0
    4     1600.0
    5     1730.0
```

(fig:717)=
```{figure} ../../images/717.*

Absorption and fluorescence spectra generated after `orca_asa` run on
the file `example003.inp`. Also, the high-resolution spectra
corresponding to homogeneous broadening $\Gamma = 10 \, \text{cm}^{-1}$
are shown.
```

(sec:spectroscopyproperties.asa.input.paraimdho)=
### Example: Modelling of Effective Broadening, Effective Stokes Shift and Temperature Effects in Absorption and Fluorescence Spectra within the IMDHO Model

For the IMDHO model the `orca_asa` is capable to model absorption and
emission spectra in the finite-temperature approximation. While the
keyword `Model=IMDHO ` assumes the zero-temperature approximation, the
value of `Model=IMDHOT` invokes the calculation of the spectra for the
finite temperature which is specified by the paramter `TK` in the block
`%sim`:

```orca
# example004.inp
#
#
%sim
     Model IMDHOT
     TK 300 # temperature (in Kelvin)

     # spectral range for absorption simulation (cm**-1)
     AbsRange    18000.0, 35000.0
     NAbsPoints  5000             # number of points in absorption spectrum

     # spectral range for simulation of fluorescence (cm**-1)
     FlRange     22000.0, 10000.0
     NFlPoints   5000      # number of points in fluorescence spectrum

     # the following options require the spectra to be normalized
     # so that their maxima are equal to 1.0
     AbsScaleMode Rel
     FlScaleMode  Rel   # default  for fluorescence
end

#---------------------------------------------------------------------------
#   Transition        Gamma    Sigma  Transition Dipole Moment (atomic unit)
#   Energy (cm**-1)  (cm**-1) (cm**-1)      Mx          My          Mz
#---------------------------------------------------------------------------

$el_states
1
   1  21140.0         50.00    100.0        1.0         0.0         0.0


# Block specifying Stokes Shift parameter for each electronic state
$ss
1   # number of excited states
  1   300.0      # the Stokes shift for the 1st electronic transition

# Block providing the values of VIBrational FREQuencies
# for 10 Ground-State normal modes.
$vib_freq_gs
10
    1       30.0
    2       80.0
    3       100.0
    4       120.0
    5       130.0
    6      140.0
    7      160.0
    8      200.0
    9      310.0
   10     1300.0

# Block specifying origin Shift of the excite-state PES
# along each normal mode in terms of the ground-state
# Dimensionless Normal Coordinates
$sdnc
 10  1
              1
     1       2.5
     2       2.0
     3       1.8
     4       1.9
     5       1.5
     6       1.9
     7       2.4
     8       1.9
     9       2.5
    10       0.9
```

This example illustrates a typical situation in large molecules which
feature a number of low frequency modes with significant values of
dimensionless displacements for a given excited-state PES. In the case
of high density of vibrational states with frequencies below or
comparable to the intrincic value of FWHM (determined by $\Gamma$ and
$\sigma$) the vibrational progression is unresolved, whereby the spectra
become very diffuse and show large separation between the maxima of
absorption and emission spectra ({numref}`fig:717`). Besides, upon
the condition $h\nu_{i} \leqslant kT$ the effective bandwidths and
positions of maxima in the spectra can be strongly subject to
temperature effects.

(fig:718)=
```{figure} ../../images/718.*

Absorption and fluorescence spectra for T$=$0 K
(blue) and T$=$300 K (red) generated after `orca_asa`
run on the file `example004.inp`. Black lines show spectra corresponding
to the case where all low-frequency modes were excluded from the
calculation.
```

The effective Stokes shift and linewidth parameters which are evaluated
in the simple self-consistent procedure are given in the output of the
`orca_asa` run:

```orca
------------------------------------------------------------------------------
State      E0           EV       fosc    Stokes shift  Effective Stokes shift
          (cm**-1)     (cm**-1)              (cm**-1)           (cm**-1)
------------------------------------------------------------------------------
    1:     21140.00   24535.85   0.074529    300.00             7091.70


-------------------------------------------------------------------------------------------
                                BROADENING PARAMETETRS (cm**-1)
-------------------------------------------------------------------------------------------
               Intrinsic                                    Effective
State  --------------------------  --------------------------------------------------------
                                                  Sigma                         FWHM
      Gamma    Sigma    FWHM      ---------------------------   ---------------------------
                                    0K     298.15K   300.00K      0K     298.15K   300.00K
-------------------------------------------------------------------------------------------
 1:  50.00   100.00   293.50     1125.34   1411.13   1413.57   2703.84   3376.75   3382.48
```

Note that the evaluation of the effective parameters is rather
approximate and these values can noticeable deviate from those which can
be directly deduced from the calculated spectra. However, such an
information usually provides the proper order of magnitude of the
effective vibronic broadening and Stokes shift. As indicated in the
program output above, the effective bandshape has predominantly a
Gaussian character which varies with the temperature so that
$\sigma = 1125 \, \text{cm}^{-1}$ ($T = 0$ K) and
$\sigma =1414 \, \text{cm}^{-1}$ ($T=300$ K). Indeed, as shown in {numref}`fig:719` the absorption
spectrum at $T=300$ K can be well fitted using Gaussian lineshape with
$\sigma = 1388 \, \text{cm}^{-1}$ (FWHM$= 3270 \, \text{cm}^{-1}$). One
can see that at higher temperatures the deviation between the spectrum
and its Gauss fit becomes even smaller.

In molecules the normal distribution of the electronic transition
energies in the ensemble would give rise to a Gaussian bandshape of the
absorption band. However, the corresponding standard deviation is
expected to be of the order of 100 cm$^{-1}$, whereby a typical Gaussian
bandwidth of the order of 1000 cm$^{-1}$ appears to result from
unresolved vibronic progression. In general, this statement is supported
by quantum chemical calculation of the model parameters. In principle
the effective bandwidth parameters can also be used for characterization
and assignement of individual electronic bands.

(fig:719)=
```{figure} ../../images/719.*

Absorption spectrum (blue) for $T=300$ K generated after `orca_asa`
run on the file `example004.inp`. Red line represents the Gauss-fit of
the calculated spectrum.
```

(sec:spectroscopyproperties.asa.input.raman1)=
### Example: Modelling of Absorption and Resonance Raman Spectra for the 1-$^1$A$_g$ $\rightarrow$ 1-$^1$B$_u$ Transition in *trans*-1,3,5-Hexatriene

The hexatriene molecule is characterized by 9 totally-symmetric normal
modes which dominate vibrational structure in absorption and are active
in rR spectra corresponding to the strongly dipole-allowed
$1-^{1}A_{g} \rightarrow 1-^{1}B_{u}$ transition around 40000 cm$^{-1}$
. Except for some peculiarities related to the neglect of normal mode
rotations in the excited state the optical spectra are quite
satisfactorily described by the IMDHO model.

The following input exemplifies simulation of absorption spectrum and rR
spectra for an arbitrary predefined number of excitation energies.

```orca
#
# example005.inp
#
# input for simulation of absorption and resonance Raman spectra
# using experimental values of transition energy and displacement
# parameters corresponding to the strongly allowed 1-1Ag 1-1Bu transition
# in trans-1,3,5-hexatriene
#
%sim
   Model IMDHO

   AbsRange     38000.0,   48000.0
   NAbsPoints   2000
   AbsScaleMode Rel

   # resonance Raman intensities will be calculated
   # for all vibrational states with excitation number
   # up to RamanOrder:
   RamanOrder  4

   # excitation energies (cm**-1) for which rR spectra will be calculated:
   RRSE 39500, 39800, 41400

   # full width half maximum of Raman bands in rR spectra (cm**-1):
   RRS_FWHM  10

   RSRange   0, 5000  # spectral range for simulation of rR spectra (cm**-1)
   NRRSPoints  5000   # number of points to simulate rR spectra (cm**-1)

end


$el_states
1
   1  39800.0      150.00    0.0     1.0   0.0   0.0


$vib_freq_gs
9
    1      354.0
    2      444.0
    3      934.0
    4     1192.0
    5     1290.0
    6     1305.0
    7     1403.0
    8     1581.0
    9     1635.0

$sdnc
9 1
               1
      1       0.55
      2       0.23
      3       0.23
      4       0.82
      5       0.485
      6       0.00
      7       0.085
      8       0.38
      9       1.32
```

After the `orca_asa` run the following files will be created:

-   `example005abs.dat` contains the simulated absorption spectrum. It
    is shown in {numref}`fig:720`.

-   `example005.o4.rrs.39500.dat`, `example005.o4.rrs.39800.dat` and
    `example005.o4.rrs.41400.dat` contain the simulated rR spectra for
    excitation energies at 39500, 39800 and 41400 cm$^{-1}$,
    respectively. The suffix "`o4`" stands for the order of Raman
    scattering specified in the input by keyword `RamanOrder=4`. The rR
    specta are shown in {numref}`fig:721`.

-   `example005.o4.rrs.39500.stk`, `example005.o4.rrs.39800.stk` and
    `example005.o4.rrs.41400.stk` provide Raman shifts and intensities
    for each vibrational transition. Corresponding vibrational states
    are specified by the quantum numbers of excited modes.

(fig:720)=
```{figure} ../../images/720.*

Absorption spectrum corresponding to
$1-^{1}A_{g} \rightarrow 1-^{1}B_{u}$ transition in
*trans*-1,3,5-hexatriene generated after `orca_asa` run on the file
`example005.inp`.
```

(fig:721)=
```{figure} ../../images/721.*

Resonance Raman spectra for 3 different excitation energies which fall
in resonance with $1-^{1}A_{g} \rightarrow 1-^{1}B_{u}$ transition in
*trans*-1,3,5-hexatriene.
```

:::{note}

-   By default the program provides rR spectra on an arbitrary scale
    since only relative rR intensities within a single rR spectrum are
    of major concern in most practical cases. However, one can put rR
    spectra corresponding to different excitation energies on the same
    intensity scale by providing the keyword `RSISM=ASR` in `%sim` block
    (RSISM -- Raman Spectra Intensity Scaling Mode; ASR -- All Spectra
    Relative). By default `RSISM=SSR` (SSR -- Single Spectrum Relative)
    for which each rR spectrum is normalized so that the most intense
    band in it has intensity 1.0. The relative intensities of bands in
    rR spectra measured for different excitation energies can be
    compared if they are appropriately normalized relative to the
    intensity of a reference signal (e.g. Raman band of the solvent). We
    also keep in mind the possibility to extend our methodology in order
    to provide the absolute measure of rR intensities in terms of the
    full or differential cross-sections.

-   Within the harmonic model, for a single electronic state neither
    relative rR intensities nor absorption bandshapes in the case of
    `AbsScaleMode=Rel` do depend on the values of the electronic
    transition dipole moment (unless it is precisely zero).
:::

In the example above resonance Raman spectra have been generated for all
vibrational transitions with total excitation number up to the value
specified by the parameter `RamanOrder`. Its is also possible to make
explicit specification of vibrational states corresponding to various
fundamental, overtone and combination bands via the `$rr_vib_states`
block. In such a case rR spectra involving only these vibrational
transitions will be generated separately.

```orca
$rr_vib_states 5 # total number of vibrational transitions
 1
   modes 1
   quanta 1; # final vibrational state for the fundamental
             # band corresponding to mode 1
 2
   modes 9
   quanta 1; # final vibrational state for the fundamental
             # band corresponding to mode 9
 3
   modes 3, 4
   quanta 1, 1; # final vibrational state for the combination band involving 
                # single excitations in modes 3 and 4
 4
   modes 5
   quanta 3; # final vibrational state for the second overtone band 
             # corresponding to mode 5
 5
   modes 1, 5,9
   quanta 1,2, 1; # final vibrational state for the combination band
                  # involving single excitations in modes 1 and 2, and
		  # double excitation in mode 5
```

Each vibrational transition is specified via the subblock which has the
following structure:

```orca
k
          modes m1,m2,...mn
          quanta q1,q2,...qn;
```

This means that the $k$-th transition is characteriezed by excitation
numbers $q_{i}$ for modes $m_{i}$ so that corresponding Raman shift is
equal to $\nu =\sum\nolimits{ q_{i} \nu_{i} }$, where $\nu_{i}$ is
vibrational frequency of the mode $m_{i}$.

After the `orca_asa` run the following files will be created in
addition:

-   `example005.us.rrs.39500.dat`, `example005.us.rrs.39800.dat` and
    `example005.us.rrs.41400.dat` contain the simulated rR spectra
    involving only vibrational transitions specified in the
    `$rr_vib_states` block, for excitations energies at 39500, 39800 and
    41400 cm$^{-1}$, respectively. The suffix "us" stands for "User
    specified vibrational States".

-   `example005.us.rrs.39500.stk`, `example005.us.rrs.39800.stk` and
    `example005.us.rrs.41400.stk` provide Raman shifts and intensities
    for each vibrational transition specified in the `$rr_vib_states`
    block.

(sec:spectroscopyproperties.asa.input.raman2)=
### Example: Modelling of Absorption Spectrum and Resonance Raman Profiles for the 1-$^1$A$_g$ $\rightarrow$ 1-$^1$B$_u$ Transition in *trans*-1,3,5-Hexatriene

The following example illustrates an input for simulation of absorption
bandshape and resonance Raman profiles (RRP):

```orca
#
# example006.inp
#
# input for simulation of absorption and resonance Raman profiles
# using experimental values of transition energy and displacement
# parameters corresponding to the strongly allowed 1-1Ag 1-1Bu transition
# in trans-1,3,5-hexatriene
#

%sim
     Model IMDHO

     AbsRange     38000.0,   48000.0
     NAbsPoints   2000
     AbsScaleMode Rel

     RRPRange   38000.0, 48000.0 # spectral range for simulation of
                                 # rR profiles (cm**-1)

     NRRPPoints   2000 # number of points for simulation of rR profiles
     CAR 0.8

     RamanOrder 2
end

$el_states
1
   1  39800.0      150.00    0.0     1.0   0.0   0.0

$vib_freq_gs
9
    1      354.000000
    2      444.000000
    3      934.000000
    4     1192.000000
    5     1290.000000
    6     1305.000000
    7     1403.000000
    8     1581.000000
    9     1635.000000

$sdnc
9 1
               1
      1       0.55
      2       0.23
      3       0.23
      4       0.82
      5       0.485
      6       0.00
      7       0.085
      8       0.38
      9       1.32

$rr_vib_states 5 # total number of vibrational transitions
 1
    modes 1
    quanta 1;
 2
    modes 9
    quanta 1;
 3
    modes 3, 4
    quanta 1, 1;
 4
    modes 5
    quanta 3;
5
     modes 1, 5,9
     quanta 1,2, 1;
```

The keyword `RamanOrder=2` will invoke generation of rR profiles for all
vibrational transitions with total excitation number up to 2 in the
range of excitation energies specified by the keywords `RRPRange` and
`NRRPPoints`. Likewise, rR profiles for the vibrational states given in
the `$rr_vib_states` block will be generated separately. Since in most
cases only relative rR intensities are important, and one would be
interested to compare absorption bandshape and shapes of individual rR
profiles, the keyword `CAR = 0.8` is used to scale rR profiles for all
vibrational transitions by a common factor in such a way that the ratio
of the maximum of all rR intensities and the maximum of absorption band
is equal to 0.8.

After the `orca_asa` run the following files will be created:

-   `example006.abs.dat` contains the simulated absorption spectrum
    ({numref}`fig:722`).

-   `example006.o1.rrp.dat` and `example006.o2.rrp.dat` contain rR
    profiles for vibrational transitions with total excitation numbers 1
    and 2, respectively. RR profiles for all fundamental bands (from the
    file `example006.o1.rrp.dat`) are shown in
    {numref}`fig:722`.

-   `example006.o1.info` and `example006.o1.info `contain specification
    of vibrational transitions with total excitation numbers 1 and 2,
    respectively, as well as corresponding Raman shifts.

-   `example006.us.rrp.1.dat–example006.us.rrp.5.da`t contain rR
    profiles for vibrational transitions 1--5 specified in the
    `$rr_vib_states` block.

(fig:722)=
```{figure} ../../images/722.*

Absorption spectrum and resonance Raman profiles of fundamental bands
corresponding to $1-^1A_g \rightarrow 1-^1B_u$ transition in
*trans*-1,3,5-hexatriene.
```

(sec:spectroscopyproperties.asa.fit)=
## Fitting of Experimental Spectra

(sec:spectroscopyproperties.asa.fit.gauss)=
### Example: Gauss-Fit of Absorption Spectrum

An absorption spectrum basically consists of a number of absorption
bands. Each absorption band corresponds to a transition of the ground
electronic state to an excited electronic state. In molecules such
transitions are usually considerably broadened. In many cases there will
be overlapping bands and one would need to deconvolute the broad
absorption envelope into contributions from individual transitions.
Within the "Simple model" the `orca_asa` program enables fit of an
absorption spectrum with a sum of standard lineshape functions
(Gaussian, Lorentzian) or more general Voigt functions. In most cases,
one simply performs a "Gauss-Fit". That is, it is assumed that the shape
of each individual band is that of a Gaussian function. Then one applies
as many (or as few) Gaussians as are necessary for an accurate
representation of the absorption envelope. In order to explain the
fitting procedures within the "Simple model" let us consider an
experimental absorption spectrum in
{numref}`fig:723`:

(fig:723)=
```{figure} ../../images/723.*

Experimental absorption spectrum. Bars indicate transition energies
which were used for the initial guess in the input for spectral
fitting.
```

As shown in {numref}`fig:723` one can identify roughly 7 electronic bands. The
initial estimates of transition energies corresponding to the maxima and
shoulders in the absorption spectrum (indicated by bars in
{numref}`fig:723`) and
rather approximate values of inhomogeneous broadening and transition
dipole moment components are specified in the `$el_states` block of the
input file for the spectral fitting:

```orca
# example007.inp 
#
# Input file for fitting of experimental absorption spectrum
#

%sim
        model Simple
end

%fit
       Fit true               # Global flag to turn on the fit
       AbsFit true            # Flag to include absorption into the fit
       method Simplex
       WeightsAdjust true

       AbsRange 0.0, 100000.0 # absorption spectral range to be included in the fit;
                              # in the present case all experimental points 
                              # will be included


       AbsName "absexp.dat"   # name of the file containing experimental
                              # absorption spectrum in a simple two-column 
                              # ASCII format

       ExpAbsScaleMode Ext    # This keyword indicates that the experimental 
                              # absorption intensity is given in terms of
                              # the extinction coefficient. This is important
                              # for the proper fitting of transition dipole  
                              # moments and oscillator strengths

       NMaxFunc 10000   # maximum number of function evaluations in simplex
                        # algorithm 

       MWADRelTol 1e-5  # Relative Tolerance of the Mean Weighted Absolute 
                        # Difference  (MWAD) function which specifies the        
                        # convergence criterion


       E0Step 500.00    # initial step for the transition energies
                        # in the simplex fitting

       TMStep 0.5       # initial step for the transition dipole moments
                        # in the simplex fitting

       E0SDStep 500.0   # initial step for the inhomogeneous linewidth (Sigma)
                        # in the simplex fitting


end

# ! Parameters specified in the $el_states block 
#   are used as initial guess in the fit

#---------------------------------------------------------------------------
#  Transition        Gamma    Sigma  Transition Dipole Moment (atomic unit)
#  Energy (cm**-1)  (cm**-1) (cm**-1)      Mx          My        Mz
#---------------------------------------------------------------------------

$el_states
7
    1 11270           0.0     1000.00    1.0000     0.0000     0.0000
    2 15100           0.0     1000.00    1.0000     0.0000     0.0000
    3 20230           0.0     1000.00    1.0000     0.0000     0.0000
    4 27500           0.0     1000.00    1.0000     0.0000     0.0000
    5 31550           0.0     1000.00    1.0000     0.0000     0.0000
    6 37070           0.0     1000.00    1.0000     0.0000     0.0000
    7 39800           0.0     1000.00    1.0000     0.0000     0.0000


# the integer values specified in $el_states_c block indicate parameters
# in the $el_states block to be varied
$el_states_c
7
    1    1             0          1          1         0         0
    2    2             0          2          2         0         0
    3    3             0          3          3         0         0
    4    4             0          4          4         0         0
    5    5             0          5          5         0         0
    6    6             0          6          6         0         0
    7    7             0          7          7         0         0
```

The functionality of the constraint block `$el_states_c` should be
understood as follows: 1) 0 flag indicates that the corresponding
parameter in the `$el_state` block will not be varied in the fitting; 2)
if the number corresponding to a certain parameter coincides with the
number of the corresponding electronic state this parameter will be
varied independently. Thus, the block `$el_states_c` in the input
indicates that all transition energies, inhomogeneous linewidths and
x-components of the transition electric dipole moment will be varied
independently, while homogeneous linewidths, y- and z-components of the
transition dipole moment will be fixed to their initial values.

The following considerations are important:

-   Since in conventional absorption spectroscopy one deals with the
    orientationally averaged absorption cross-section, the signal
    intensity is proportional to the square of the transition electric
    dipole moment $\left|{ \mathrm{\mathbf{M} }} \right|^{2}$. Thus, the
    intensities do not depend on the values of the individual components
    of $\mathrm{\mathbf{M} }$ as long as
    $\left|{ \mathrm{\mathbf{M} }} \right|^{2}= \text{const}$.
    Therefore, we have allowed to vary only $M_{x}$ components.
    Otherwise there can be problems in convergence of the fitting
    algorithm.

-   The sum of the weights of experimental points which enter the mean
    absolute difference function employed in the minimization is always
    kept equal to the number of experimental points. In the case of
    equidistant experimental photon energies all weights are assumed to
    be equal. However, in experimental electronic spectra the density of
    spectral points can increase significantly upon going from high- to
    low-energy spectral regions, which is due to the fact that
    experimental absorption spectra are initially acquired on the
    wavelength scale. In such a case the quality of the fit can be
    noticeably biased towards low-energy spectral region. Therefore, it
    is advisable to adjust relative weights of experimental points
    according to the their density which is controlled by the keyword
    `WeightsAdjust` in the `%fit` block. Although this parameter is not
    crucial for the present example, in general, it will provide a more
    balanced fit.

-   The parameters `E0Step`, `TMStep`, `E0SDStep` in the `%fit` block
    specify the initial dimension of the simplex in the space of
    $E_{T} ,\mathrm{\mathbf{M} }, \sigma$ and should roughly correspond
    to the expected uncertainty of initial guess on these parameters in
    the `$el_states` block relative to their actual values. The quality
    of the fit can noticeably deteriorate if the parameters specifying
    initial steps are too low or too high.

The fit run of `orca_asa` on file `example007.inp` will converge upon
approximately 3600 function evaluations (for `MWADRelTol=1e-5`). The
results of the fit will be stored in file `example007.001.inp` which has
the same structure as the input file `example007.inp`. Thus, if the fit
is not satisfactory and/or it is not fully converged it can be refined
in a subsequent `orca_asa` run upon which file `example007.002.inp` will
be created, and so on. Some model parameters in intermediate files can
be be additionally modified and/or some constraints can be lifted or
imposed if so desired. The output file `example007.001.inp` will contain
fitted model parameters stored in the `$el_states` block:

```orca
$el_states
7
   1 11368.24     0.00  732.50     1.6290   0.0000   0.0000
   2 15262.33     0.00  495.17    -0.2815   0.0000   0.0000
   3 19500.08     0.00  1023.39     0.2300   0.0000   0.0000
   4 26969.01     0.00  1832.30     1.4089   0.0000   0.0000
   5 31580.41     0.00  1440.87     1.8610   0.0000   0.0000
   6 35769.07     0.00  1804.02     1.5525   0.0000   0.0000
   7 39975.11     0.00  1909.38     2.4745   0.0000   0.0000
```

The overall quality of the fit is determined by the parameter MWAD which
upon convergence reaches the value of $\approx$0.009
(MWAD stands for Mean Weighted Absolute Difference).

After the `orca_asa` run files `absexp.fit.dat` and `absexp.fit.as.dat`
will be created. Both files contain the experimental and fitted spectra
which are shown in {numref}`fig:724` . In addition, the file `absexp.fit.as.dat` will
contain individual contributions to the absorption spectrum
corresponding to different excited states.

(fig:724)=
```{figure} ../../images/724.*

Comparison of the experimental (black curve) and fitted (red)
absorption spectra corresponding to the fit run of `orca_asa` on the
file `example007.inp`. Blue curves represent individual contributions to
the absorption spectrum from each state.
```

Since there is a noticeable discrepancy between the fitted and
experimental spectra around 13000 cm$^{-1}$ ({numref}`fig:724`) it is
worthwhile to refine the fit after adding parameters for a new state in
the file `example007.001.inp`:

```orca
$el_states
8
   1 11368.24     0.00  732.50     1.6290   0.0000   0.0000
... ... ...
   8 13280.00     0.00  1000.00     1.000   0.0000   0.0000


$el_states_c
8
   1     1         0        1          1        0        0
... ... ...
   8     8         0        8          8        0        0
```

Actually, the character of the discrepancy in the present case is very
similar to that in {numref}`fig:721` (section
{ref}`sec:spectroscopyproperties.asa.input.paraimdho`) where a vibronically
broadened absorption spectrum was fitted with a Gaussian lineshape.
Thus, the poor fit in the region around 1300 cm$^{-1}$ is most likely
due to the essentially asymmetric character of the vibronic broadening
rather than to the presence of another electronic band.

As shown in {numref}`fig:725` the refined fit leads to much better agreement
between the experimental and fitted absorption spectra
(MWAD$=$0.0045).

(fig:725)=
```{figure} ../../images/725.*

Comparison of the experimental (black) and fitted (red) absorption
spectra corresponding to the fit run of `orca_asa` on the file
`example007.001.inp`. Blue curves represent individual contributions to
the absorption spectrum from each state.
```

Due to some peculiarities of the simplex algorithm for function
minimization, you can still refine the fit by rerunning `orca_asa` on
the file `example007.002.inp`! This leads to an even lower value of the
parameter MWAD$=$ 0.0038, and therefore to better agreement of
experimental and fitted spectra (even though the previous run has been
claimed to be converged).

It is also possible to perform a fit using the same value of
inhomogeneous linewidth for all electronic states. For this purpose one
needs to choose as a guess the same linewidth parameters in the
`$el_states ` block:

```orca
$el_states
8
   1 11118.58     0.00  1000.0      1.0687   0.0000   0.0000
   2 13673.38     0.00  1000.0     -0.5530   0.0000   0.0000
   3 21267.40     0.00  1000.0      0.3675   0.0000   0.0000
   4 27024.71     0.00  1000.0      1.4041   0.0000   0.0000
   5 31414.74     0.00  1000.0      1.7279   0.0000   0.0000
   6 35180.77     0.00  1000.0      1.6246   0.0000   0.0000
   7 39985.52     0.00  1000.0      2.5708   0.0000   0.0000
   8 11665.01     0.00  1000.0      1.2332   0.0000   0.0000
```

In addition the constraint block should be modified as follows:

```orca
$el_states_c
8
   1     1         0        1          1        0        0
   2     2         0        1          2        0        0
   3     3         0        1          3        0        0
   4     4         0        1          4        0        0
   5     5         0        1          5        0        0
   6     6         0        1          6        0        0
   7     7         0        1          7        0        0
   8     8         0        1          8        0        0
```

The constraint parameters for the inhomogeneous broadening were chosen
to be 1, which means that formally $\sigma_{1}$ corresponding to the
first state is varied independently while the linewidths
$\left\{{ \sigma_{i} } 
\right\}$ for other bands are varied in such a way that the ratios
$\sigma 
_{i} /\sigma_{1}$ are kept fixed to their initial values, whereby the
same linewidth parameter will be used for all states.

(fig:726)=
```{figure} ../../images/726.*

 Comparison of the experimental (black) and fitted (red) absorption
spectra corresponding to the fit run of `orca_asa` on the file
`example007.002.inp` in which equal broadening was assumed for all
electronic bands. Blue curves represent individual contributions to the
absorption spectrum from each state.
```

One can see ({numref}`fig:726`) that the assumption of equal linewidths for all
electronic bands leads to a rather pronounced deterioration of the
quality of the fit in the low-energy spectral range
(MWAD$=$0.017). Apparently, this discrepancy can be
fixed assuming more electronic states at higher energies.

NOTE

-   The homogeneous linewidth parameters can also be included in the fit
    in a similar way. However, one can see that in most cases they
    appear to be much smaller than corresponding Gaussian linewidth
    parameters.

-   Gauss-fit of absorption spectra is coventionally performed assuming
    the same linewidth parameters for all bands. However, since a large
    portion of Gaussian broadening is mainly due to the unresolved
    vibronic structure in the spectra which can significantly vary
    depending on the nature of transition, the assumption of unequal
    Gaussian bandwidths seems to be a physical one.

(sec:spectroscopyproperties.asa.fit.raman)=
### Example: Fit of Absorption and Resonance Raman Spectra for 1-$^1$A$_g$ $\rightarrow$ 1-$^1$B$_u$ Transition in *trans*-1,3,5-Hexatriene

Below we provide an example of the fit of the lineshape parameters and
$\left\{{\Delta_{m} } \right\}$ corresponding to the strongly
dipole-allowed 1-$^{1}$A$_{g}$
$\rightarrow$1-$^{1}$B$_{u}$ transition in hexatriene.
It is known that the most intense bands in rR spectra correspond to the
most vibronically active in absorption spectrum. For the IMDHO model
this correlation is determined by the values of $\left\{{ \Delta_{m} } 
\right\}$. Thus, the larger $\Delta$, the larger is the rR intensity of
a given mode and the more pronounced is the progression in the
absorption spectrum corresponding to this mode. In principle, if all
vibrational transitions in absorption are well resolved it is possible
to determine $\left\{{ \Delta 
_{m} } \right\}$ by a fit of the absorption spectrum alone. In practice
this task is ambiguous due to the limited resolution of the experimental
absorption spectra. The observation of a rR spectrum enables the
identification of the vibrational modes that are responsible for the
progression in the absorption spectrum, as well as a quantitative
analysis in terms of $\left\{{ \Delta_{m} } \right\}$. The file
`example006.inp `provides a brute-force example on how to approach the
fit employing the minimal possible experimental information: 1) An
absorption spectrum; 2) relative rR intensities of fundamental bands for
a given excitation energy. The rR spectrum upon the excitation in
resonance with the 0-0 vibronic band at 39809 cm$^{-1}$ is shown in
{numref}`fig:715`.

(fig:727)=
```{figure} ../../images/727.*

Experimental Resonance Raman spectrum corresponding to 1-$^1$A$_g$
$\rightarrow$ 1-$^1$B$_u$ transition in
*trans*-1,3,5-hexatriene.
```

The experimental rR spectrum has enabled the identification of seven
vibrational modes that give rise to the most intense resonance Raman
bands. Therefore, they are expected to have the largest excited-state
displacements and the most pronounced effect on the vibrational
structure of the absorption spectrum. Their vibrational frequencies have
been entered as input for the fit as shown below:

```orca
#
# example008.inp
#
# Input for fit of absorption and resonance Raman spectra
# corresponding to the strongly allowed 1-1Ag 1-1Bu transition
# in 1,3,5 trans-hexatriene.
# 
# Parameters to be varied:
# 1) adiabatic minima transiton energy
# 2) homogeneous linewidth (Gamma)
# 3) dimensionless normal coordinate displacements of the 
#    excited-state origin 
#

%sim
      Model IMDHO
end


%fit 
    
    Fit true     # boolean parameter to switch on the fit

    # boolean parameter to include experimental absorption 
    # spectrum in the fit:
    AbsFit true  

    # boolean parameter to include experimental rR spectra
    # specified in $rrs_exp block in the fit:
    RRSFit true

    AbsExpName "hex-abs.dat" # name of the file with experimental absorption
                             # spectrum

    # the following value of keyword ExpAbsScaleMode
    # indicates that only the shape of absorption band 
    # but not its total intensity will be accounted in the fit:
    ExpAbsScaleMode Rel

    # the weight of absorption relative to the total weight of
    #  rR intensities in the difference function to be minimized:
    CWAR  5.0

    NMaxFunc  1000   # maximum number of function evaluations in simplex
                     # algorithm 

    MWADRelTol 1e-4  # Relative Tolerance of the Mean Weighted Absolute 
                     # Difference  (MWAD) function which specifies the        
                     # convergence criterion
    SDNCStep  1.0
                    
end  


# The values specified in $el_states block serve as initial guess in the fit
$el_states
1
   1  40000.0      200.00    0.0     1.0   0.0   0.0

# the integer values specified in $el_states_c block indicate parameters
# in $el_states block to be varied
$el_states_c
1
   1     1            1       0       0     0     0 

# 7 totally symmetric vibrations which give rise to the most
# intense bands in the rR spectra are included into analysis.
# Experimental values of vibration frequencies are given: 
$vib_freq_gs
7
    1      354.0
    2      444.0 
    3      934.0
    4     1192.0
    5     1290.0
    6     1403.0
    7     1635.0

# Initial guess for the values of dimensionless normal
# coordinate displacements of the excited-state origin 
$sdnc
7 1
               1
      1       0.0    
      2       0.0     
      3       0.0      
      4       0.0      
      5       0.0   
      6       0.0    
      7       0.0     

# the integer values specified in $sdnc_c block indicate parameters
# in $sdnc block to be varied
$sdnc_c
7 1
             1
      1        1
      2        2
      3        3
      4        4
      5        5
      6        6
      7        7


# specification  of vibrational transitions and their intensities 
# in experimental rR spectra:
$rrs_exp 
1         # number of rR spectra
1 1       # start of the block specifying the 1st rR spectrum
    Ex 39809.0 # excitation energy for the first rR spectrum
    NTr  7     # number of vibrational transitions for which intensities are 
               # provided 
    1     
       int   10.0  1.0
       modes  1
       quanta 1;
    2     
       int   5.0  1.0
       modes  2
       quanta 1;
    3     
       int   1.5  1.0
       modes  3
       quanta 1;
    4     
       int   21.0  1.0
       modes  4
       quanta 1;
    5     
       int   7.5  1.0
       modes  5
       quanta 1;
    6     
       int   2.0  1.0
       modes  6
       quanta 1;
    7     
       int   46.0  1.0
       modes  7
       quanta 1;
```

The input of rR intensities for an arbitrary number of excitation
energies follows the keyword `$rrs_exp` block:

```orca
$rrs_exp 
1         # number of rR spectra
1 1
```

The first "1" in the last line denotes the number of the rR spectrum for
which specification starts below. If the second number is the same as
the number of the spectrum, then it means that only relative intensities
for the first rR spectrum are meaningful in the fit. If several spectra
are given in the input then the second number may have a different
value, e.g.:

```orca
$rrs_exp 
3         # number of rR spectra
1 2 
...
```

This input is to be interpreted as indicating that 3 rR spectra are
provided and the relative intensities for the first spectrum are given
on the same scale as the second one that will be accounted for in the
fit. The value of the excitation energies and the number of vibrational
transitions specified are indispensable within the blocks specifying
intensities for each rR spectrum.

Following the number of vibrational transitions given by the keyword
`NTr` one has to specify each vibrational transition and its intensity.
Thus, in the present case there are seven subblocks with the following
structure:

```orca
k    int   I  W
          modes m1,m2,...mn  
          quanta q1,q2,...qn;
```

This means that the $k$-th transition has intensity $I$ and weight $W$
in the mean absolute difference function that is used for the
minimization ($W$ is an optional parameter). The following 2 lines
specify the vibrational transitions by providing excitation numbers
$q_{i}$ for modes $m_{i}$ so that the corresponding Raman shift is equal
to $\nu =\sum\limits_ { q_{i} \nu 
_{i} }$, where $\nu_{i}$ is vibrational frequency of the mode $m_{i}$.

The parameters that are to be varied are specified within the constraint
blocks `$el_states_c` and `$sdnc_c`. Both blocks have the same structure
and number of parameters as `$el_states` and `$sdnc`, respectively. A
parameter from the `$el_states` block is supposed to be independently
varied if its counterpart from the `$el_states_c` block is equal to the
number of the electronic state. Likewise, a parameter from the `$sdnc`
block is supposed to be independently varied if its counterpart from the
`$sdnc_c` block is equal to the number of the normal mode. Model
parameters that are set to 0 in the corresponding constraint blocks are
not varied in the fit. The values of the following parameters may be
important for the quality of the fit:

-   `CWAR` in the `%fit` block specifies the weight of absorption
    relative to the weight of rR intensities in the difference function
    to be minimized. If this parameter was not specified the fit would
    be almost insensitive to the rR intensities in the input, since
    typically the number of experimental absorption points is much
    larger than the number of rR transitions in the input. In most cases
    the value of `CWAR` in the range 1.0--5.0 is a good choice since the
    error in the measured experimental intensity is expected to be much
    smaller for absorption than for resonance Raman.

-   `SDNCStep` in the `%fit` block specifies the initial dimension of
    the simplex in the space of $\left\{{ \Delta_{m} } \right\}$ and
    should roughly correspond to the expected uncertainty of initial
    guess on $\left\{{ \Delta_{m} } \right\}$ in the `$sdnc `block
    compared to their actual values. You can notice in the present
    example that if this parameter is too large (\>2.0) or too small
    (\<0.4) the quality of the fit may significantly deteriorate

-   Although the default initial dimensions of the simplex have
    reasonable values for different types of parameters it may turn out
    to be helpful in some cases to modify the default values:

```orca
  FREQGStep 10.0  # ground-state vibrational frequencies
  FREQEStep 10.0  # excited-state vibrational frequencies
  E0Step    300.0 # transition energies
  SSStep     20.0 # Stokes shift
  TMStep      0.5 # electronic transition dipole moment
  GammaStep  50.0 # homogeneous linewidth
  E0SDStep   50.0 # inhomogeneous linewidth
  SDNCStep    1.0 # origin shift along dimensionless normal coordinate
```

The fit run of `orca_asa` on the file `example008.inp` will converge
upon approximately 700 function evaluations (for `MWADRelTol=1e-4`). The
results of the fit will be stored in file `example008.001.inp` which has
the same structure as the input file `example008.inp`. Thus, if the fit
is not satisfactory and/or it is not fully converged it can be refined
in subsequent `orca_asa` run upon which file `example008.002.inp` will
be created, and so on. Some model parameters in intermediate files can
be be additionally modified and/or some constraints can be lifted if so
desired. The output file `example008.001.inp` will contain fitted
displacement parameters $\left\{{ \Delta_{m} } \right\}$stored in the
`$sdnc` block:

```orca
$sdnc                  
7 1                    
                   1   
      1       0.675000 
      2      -0.194484 
      3      -0.217527 
      4       0.811573 
      5       0.529420 
      6      -0.149991 
      7       1.314915
```

In the present example, these parameters are actually in very close
agreement with those published for the hexatriene molecule!

The overall quality of the fit is determined by the parameter MWAD which
upon convergence reaches the value of $\approx$0.027.
The fitted rR intensities are presented in the commented lines next to
the experimental rR intensities in file `example008.001.inp`:

```orca
$rrs_exp
1
   1   1 3.495285e+001
   Ex    39809.00
   NT   7
      1
        Int 10.0 1.0  # simulated intensity: 1.000982e+001
        modes  1
        quanta 1;
      2
        Int 5.0 1.0   # simulated intensity: 8.976285e-001
        modes  2
        quanta 1;
      3
        Int 1.5 1.0   # simulated intensity: 1.255880e+000
        modes  3
        quanta 1;
      4
        Int 21.0 1.0  # simulated intensity: 1.761809e+001
        modes  4
        quanta 1;
      5
        Int 7.5 1.0   # simulated intensity: 7.499749e+000
        modes  5
        quanta 1;
      6
        Int 2.0 1.0   # simulated intensity: 6.014466e-001
        modes  6
        quanta 1;
      7
        Int 46.0 1.0  # simulated intensity: 4.600071e+001
        modes  7
        quanta 1;
```

The file hex-abs.fit.dat will contain the experimental and fitted
absorption spectra in ASCII format which can be plotted in order to
visualize the quality of absorption fit
({numref}`fig:728`).

(fig:728)=
```{figure} ../../images/728.*

Experimental (black) and fitted (red) absorption spectrum
corresponding to 1-$^1$A$_g$ $\rightarrow$ 1-$^1$B$_u$ transition in
1,3,5 *trans*-hexatriene.
```

:::{note}

-   The more experimental rR intensities are included in the analysis
    the more reliable is the fit. In principle it is possible to obtain
    fully consistent results even if only a limited number of
    vibrational transitions is provided. However, in such a case it is
    desirable to include into analysis at least a single Raman
    transition involving the mode for which $\Delta$ is to be
    determined.

-   The quality of the fit can be improved if the IMDHOFA model is
    invoked and excited-state vibrational frequencies are allowed to
    vary.

-   Due to the initial guess and dimension of the simplex, as well as
    some peculiarities of the simplex algorithm for function
    minimization, you can still refine the fit by rerunning `orca_asa`
    on file `example008.001.inp` that may lead to an even lower value of
    the parameter `MWAD = 0.021`, and therefore to better agreement of
    experimental and fitted spectra (even though the previous run has
    been claimed to be converged).

-   In this respect it appears to be wise to perform the fit in 3 steps:

    1.  Fit the preresonance region below the 0-0 vibronic band with a
        single Lorentzian band, from which the adiabatic transition
        energy $E_{0}$, and homogeneous linewidth $\Gamma$ are obtained.
        The range for fit of the absorption spectrum can be specified by
        the `AbsRange` keyword in the `%fit` block.

    2.  Fix $E_{0}$ and $\Gamma$, and optimize
        $\left\{{ \Delta_{m} } \right\}$ fitting the entire spectral
        range and rR intensities.

    3.  Lift constraints on $E_{0}$ and $\Gamma$, and reoptimize
        simultaneously all parameters.
:::

(sec:spectroscopyproperties.asa.fit.singleMode)=
### Example: Single-Mode Fit of Absorption and Fluorescence Spectra for 1-$^1$A$_g$ $\rightarrow$ 1-$^1$B$_{2u}$ Transition in Tetracene

In this section we provide an example and discuss the most important
aspects of joint fit of fluorescence and absorption spectra.
{numref}`fig:729` displays
the experimental emission and absorption spectra corresponding to
1-$^1$A$_g$ $\rightarrow$ 1-$^1$B$_{2u}$ transition in tetracene.

(fig:729)=
```{figure} ../../images/729.*

Deconvoluted absorption (red) and fluorescence (blue) spectra of
tetracene in cyclohexane upon the assumption of a single vibronically
active mode. The black solid lines represent experimental
spectra.
```

Both spectra show pronounced effective vibrational progressions that are
dominated by 3 and 5 peaks, respectively. As can be shown on the basis
of quantum chemical calculations this progression has essentially
multimode character. However, the experimental spectra can be well
fitted under the assumption of a single vibronically active mode. The
input has the following structure:

```orca
#
# example009.inp
# 
# Parameters to be varied:
# 1) adiabatic minima transition energy
# 2) homogeneous and inhomogeneous linewidths
# 3) normal mode frequency and corresponding dimensionless displacement of the 
#    excited-state origin 
#

%sim
      Model IMDHO
      EnInput E0 # we assume adiabatic minima separation energies 
end

%fit
    Fit true       # global flag to turn on the fit
    AbsFit true    # flag to include absorption spectrum into the fit
    FlFit true     # flag to include fluorescence spectrum into the fit

    WeightsAdjust true

    AbsRange 19000.0, 28000.0 # spectral range for absorption
                              # which will be included into the fit

    FlRange  17800.0, 22300.0 # spectral range for absorption
                              # which will be considered in the fit

    AbsName "absexp.dat" # name of the file containing experimental
                         # absorption spectrum in a simple two-column 
                         # ASCII format
    FlName  "flexp.dat"  # name of the file with experimental fluorescence spectrum 

    ExpAbsScaleMode Rel  # flags indicating that only relative shapes of the 
    ExpFlScaleMode Rel   # absorption and fluorescence bands will be fitted.
    

    CWAF   1.000 # important parameter to have a balanced relative quality of fit
                 # of fluorescence and absorption

    NMaxFunc 10000  # maximum number of function evaluations in simplex
                    # algorithm 

    MWADRelTol= 0.0001  # Relative Tolerance of the Mean Weighted Absolute 
                        # Difference  (MWAD) function which specifies the        
                        # convergence criterion

    TMStep 0.5       # initial step for the transition dipole moments
                     # in the simplex fitting

    E0SDStep 500.0   # initial step for the inhomogeneous linewidth (Sigma)

    FREQGStep 100.00 # initial step for the vibrational frequencies

    E0Step 1000.0    # initial step for the transition energies

    SSStep 10.0      # initial step for the Stokes shift

    GammaStep 100    # initial step for the homogeneous linewidth

    SDNCStep 0.5    # initial step for the displacement parameter

end

$el_states
2
   1 21100.00    100.00   100.00     1.0000   0.0000   0.0000
   2 24000.00    100.00   1000.00    1.0000   0.0000   0.0000

$el_states_c
2
   1     1         1        1          0        0        0
   2     2         2        2          2        0        0

$abs_bool
2
  1  1
  2  1

$fl_bool
2
  1  1
  2  0

$ss
2
    1      100.000000
    2        0.000000

$ss_c
2
    1            1
    2            0


$vib_freq_gs
1
    1      1500.0


$vib_freq_gs_c
1
    1            1

$sdnc
1 2
                   1          2    
      1       2.0000000   0.000000
 
$sdnc_c
1 2
                   1          2    
      1         1          0
```

The parameter `CWAF=1.0` in the `%fit` block specifies the weight of
absorption relative to the weight of fluorescence in the difference
function to be minimized. If this parameter was not specified the
quality of the fit would be biased towards the spectrum with a larger
number of experimental points. In some typical situations where the
error in the measured experimental intensity is expected to be smaller
for absorption than for emission it is desirable to choose the value of
`CWAF` to be more than 1.0.

In order to account for a broad featureless background signal in the
absorption spectrum above 24000 cm$^{-1}$, the second band was included
into the analysis and approximated with a Voigt lineshape which means
also that the corresponding frequency in the `$vib_freq_gs` block and
displacement parameter in the `$sdnc ` block are fixed to zero in the
fit. Thus, the `$el_states ` block contains an initial guess on the
transition energies, transition electric dipole moments and linewidth
parameters for 2 states:

```orca
$el_states
2
   1 21100.00    100.00   100.00     1.0000   0.0000   0.0000
   2 24000.00    100.00   1000.00    1.0000   0.0000   0.0000
```

The initial value of the adiabatic minima separation energy for the
first state was approximated by the energy corresponding to the first
vibronic peak in the absorption spectrum (21100 cm$^{-1})$. The
transition energies and linewidth parameters are varied independently as
indicated in the `$el_states_c` block. Since we allow to fit only
bandshapes, but not the overall intensities of the spectra, only
relative absolute values of the transition electric dipole moments of
two bands are important. Therefore it is reasonable to fix all
components of the transition moment for the first state and vary only
$M_{x}$ component for the second one:

```orca
$el_states_c
2
   1     1         1        1          0        0        0
   2     2         2        2          2        0        0
```

Since we assume the absorption by both states and emission only from the
first one, it is necessary to include Boolean arrays \$abs_bool and
\$fl_bool which specify states which will be included in the treatment
of the absorption and fluorescence spectra, respectively:

```orca
$abs_bool
2
  1  1 # 1 indicates that the corresponding state will be included 
  2  1 # in the calculation of absorption
  

$fl_bool
2
  1  1
  2  0 # 0 indicates that the corresponding state will be excluded 
       # from the calculation of emission spectrum
```

We need also to vary the value of vibrational frequency of the mode
which determines separation of vibrational peaks in the spectra. This is
done via the constraint block `$vib_freq_gs_c`:

```orca
$vib_freq_gs_c
1
    1            1
```

Note that it is meaningless to include into the treatment the Stokes
shift for the second state which give rise to the background signal in
the absorption since the corresponding emission is not present.
Therefore $\lambda$ for the second state is fixed to zero as indicated
in the `$ss ` block and its constraint counterpart `$ss_c`:

```orca
$ss
2
    1    100.000000 # initialization of the Stokes shift for 
    2      0.000000 # the 1st electronic state

$ss_c
2
    1    1 # the Stokes shift for the 1st electronic state will be varied in the fit
    2    0 # the Stokes shift for the 2nd electronic state will be fixed in the fit
```

The fit run of `orca_asa` on file `example009.inp` will converge upon
approximately 700 function evaluations (for `MWADRelTol=1e-4`). The file
`example009.001.inp` will contain the fitted effective values of the
vibrational frequency and dimensionless displacement:
$\omega = 1404 \, \text{cm}^{-1}$, $\Delta = 1.35$. One can notice that
the fit is rather poor in the low- and high-energy edges of the
absorption and fluorescence spectra, respectively
({numref}`fig:729`). The
source of this discrepancy is the single-mode approximation which was
employed here. The quality of the fit can be significantly improved
assuming several modes with non-zero displacement parameters. Note that
in such a case the proper guess on the number of active modes and
corresponding dimensionless displacements can be deduced from quantum
chemical calculations.

(sec:spectroscopyproperties.asa.fitvalues)=
## Quantum-Chemically Assisted Simulations and Fits of Optical Bandshapes and Resonance Raman Intensities

In this section we finally connect the spectra simulation algorithms to
actual quantum chemical calculations and outline a detailed approach for
the analysis of absorption, fluorescence and resonance Raman spectra
within the IMDHO model. Our procedure becomes highly efficient and
nearly automatic if analytical excited state derivatives with respect to
nuclear displacements are available. However, this availability is not
mandatory and hence, spectral predictions may as well be achieved by
means of normal mode scan calculations for high-level electronic
structure methods for which analytic gradients have not been
implemented.

(sec:spectroscopyproperties.asa.fitvalues.raman)=
### Example: Quantum-Chemically Assisted Analysis and Fit of the Absorption and Resonance Raman Spectra for 1-$^1$A$_g$ $\rightarrow$ 1-$^1$B$_u$ Transition in *trans*-1,3,5-Hexatriene

The following input file for an ORCA run invokes the calculation of the
excited-state origin displacements along all normal modes by means of
energy and excited state gradient calculations at the ground-state
equilibrium geometry. The method is valid for the IMDHO model for which
the excited-state energy gradient along a given normal mode and
corresponding origin shift are related in a very simple way.

```orca
#
# example010.inp
#
# TDDFT BHLYP Normal Mode Gradient Calculation
#
#   The keyword NMGrad invokes the normal mode gradient calculation
#
! RKS BHandHLYP TightSCF SV(P) NMGrad

%cis    NRoots 1
        triplets false
end

%rr
    # the nuclear Hessian must have been calculated before - for example by a 
    # DFT calculation.
    HessName= "hexatriene.hess"

    states 1    # Perform energy-gradient calculations for the 1st 
                # excited state.
    Tdnc 0.005  # Threshold for dimensionless displacements to be 
                # included in the input file for spectral simulations 
                # generated at the end of the program run.
                # By default Tdnc= 0.005

    ASAInput true # Generate the input file for spectra simulations   
 end    

* xyz   0 1
  C    -0.003374    0.678229   0.00000
  H    -0.969173    1.203538   0.00000
  C     1.190547    1.505313   0.00000
  H     2.151896    0.972469   0.00000
  C     1.189404    2.852603   0.00000
  H     0.251463    3.423183   0.00000
  H     2.122793    3.426578   0.00000
  C     0.003374   -0.678229   0.00000
  H     0.969172   -1.203538   0.00000
  C    -1.190547   -1.505313   0.00000
  H    -2.151897   -0.972469   0.00000
  C    -1.189404   -2.852603   0.00000
  H    -0.251463   -3.423183    0.00000
  H    -2.122793   -3.426578    0.00000
*
```

In the ORCA run the TDDFT excited state gradient calculations are
performed on top of a TDDFT calculation. Note, that the numbers of the
excited-states which have to be included into analysis and input file
for spectral simulations must be specified after the `States` keyword in
the `%rr` block. They should also be consistent with the required number
of roots in the `%tddft` block. The 1-$^{1}$B$_{u}$ excited state
appears to be the first root in the TDDFT calculation. Therefore,
`NRoots=1` in the `%tddft` block, and `States=1` in the `%rr` block. One
should also provide the name of the file containing the nuclear Hessian
matrix via the `HessName` keyword in the `%rr` block. Here we used the
`.hess` file obtained in a frequency calculation at the BHLYP/SV(P)
level of theory.

After the ORCA calculation you will find in your directory a file called
`example010.asa.inp` that is appropriate to be used together with the
`orca_asa program` as defined in the preceding sections.

```orca
#
# example010.asa.inp
#
# ASA input
#
%sim
         model IMDHO
         method Heller
         AbsRange     5000.0,  100000.0
         NAbsPoints    0

         FlRange      5000.0,  100000.0
         NFlPoints     0

         RRPRange     5000.0,  100000.0
         NRRPPoints    0

         RRSRange        0.0,    4000.0
         NRRSPoints 4000

         RRS_FWHM 10.0


         AbsScaleMode Ext
         FlScaleMode Rel
         RamanOrder  0

         EnInput E0

         CAR   0.800

end

%fit
         Fit false
         AbsFit false
         FlFit false
         RRPFit fsalse
         RRSFit false
         method Simplex
         WeightsAdjust true

         AbsRange        0.0,  10000000.0
         FlRange         0.0,  10000000.0
         RRPRange        0.0,  10000000.0
         RRSRange        0.0,  10000000.0
         AbsName ""
         FlName  ""

         ExpFlScaleMode  Rel
         ExpAbsScaleMode Rel

         CWAR  -1.000
         CWAF  -1.000

         NMaxFunc 100
         MWADRelTol= 1.000000e-004

         SFRRPSimStep= 1.000000e+002
         SFRRSSimStep 1.000000e+002
         FREQGStep 1.000000e+001
         FREQEStep 1.000000e+001
         E0Step 3.000000e+002
         SSStep 2.000000e+001
         TMStep 5.000000e-001
         GammaStep 5.000000e+001
         E0SDStep 5.000000e+001
         SDNCStep 4.000000e-001
end

$el_states
1
   1 42671.71   100.00    0.00     1.0725   3.3770  -0.0000

$vib_freq_gs
12
    1      359.709864
    2      456.925612
    3      974.521651
    4     1259.779018
    5     1356.134238
    6     1370.721341
    7     1476.878592
    8     1724.259894
    9     1804.572974
   10     3236.588264
   11     3244.034359
   12     3323.831066


$sdnc
12 1
                   1    
      1      -0.594359
      2       0.369227
      3      -0.132430
      4      -0.727616
      5       0.406841
      6      -0.105324
      7       0.177617
      8      -0.090105
      9      -1.412258
     10       0.048788
     11       0.021438
     12       0.008887
```

This input file can be used to construct theoretical absorption and rR
spectra. **In order to compare experimental and theoretical rR spectra,
it is necessary to use in both cases excitation energies that are
approximately in resonance with the same vibrational transitions in the
absorption spectrum. Therefore, in the case of the absorption spectrum
with resolved or partially resolved vibrational structure it is
necessary to modify the transition energies in the `%el_states ` such
that they coincide with the experimentally observed 0-0 vibrational
peaks.** It is also desirable to roughly adjust homogeneous and,
possibly, inhomogeneous linewidth parameters such that the experimental
and calculated absorption spectra show similar slopes in the
preresonance region (below the 0-0 transition). Then the assignment of
experimental rR spectra can be done on the basis of comparison with the
theoretical rR spectra calculated for the corresponding experimental
excitation energies. For the sake of consistency and simplicity it is
better to use those excitation energies which fall into the preresonace
region and/or are in resonance with the 0-0 transition. **In the case of
diffuse absorption spectra (i.e. those not showing resolved vibrational
structure) it is also necessary to adjust the theoretical transition
energies and linewidth parameters such that experimental and calculated
positions of absorption maxima roughly coincide, and corresponding
slopes below the maxima have a similar behavior.** According to above
mentioned considerations one needs to modify the `%el_states` block in
the file `example010.asa.inp`:

```orca
$el_states
1
   1 39808.0   150.00    0.00  1.0725   3.3770  -0.0000
```

The calculated absorption spectrum obtained by providing
`AbsScaleMode= Rel`, `AbsRange= 39000`, `49000` and `NAbsPoints= 2000`
is shown in {numref}`fig:730`. Upon comparison with the experimental spectrum one
can notice that the BHLYP functional gives relatively small
discrepancies with somewhat lower intensity in the low-frequency edge
and larger intensity on the high-energy side of the spectrum. Besides,
there is a noticeable mismatch in the separation between individual
vibronic peaks which is due to overestimation of vibrational frequencies
by the BHLYP functional (typically by $\approx$ 10%).

You can arbitrarily vary various normal coordinate displacements in
`%sdnc` block within 10--30% of their values in order to observe
modifications of the calculated spectrum. This will tell you how these
parameters influence the spectrum and probably it will be possible to
obtain better initial guesses for the fit. In the present example you
will find that reduction of the absolute value of the displacement
parameter corresponding to the ninth mode by $\approx$ 10%, and
reduction of vibrational frequencies by $\approx$ 10% can noticeably
improve the spectral envelope. Such a quick analysis suggests that
experimentally observed peaks in the absorption spectrum represent
different vibrational transitions corresponding to a single
electronically excited state rather than to different electronic
excitations. This conclusion will be confirmed upon establishing the
fact that the absorption and rR spectra can be successfully fitted based
on the assumption of a single electronic transition.

(fig:730)=
```{figure} ../../images/730.*

Experimental and calculated at the BHLYP/SV(P) and B3LYP/SV(P) levels
of theory absorption (left panel) and rR spectra (right panel)
corresponding to 1-$^1$A$_g$ $\rightarrow$ 1-$^1$B$_u$ transition in
*trans*-1,3,5-hexatriene.
```

In order to calculate the rR spectrum for experimental excitation
energies you need to specify its value through `RRSE` keyword in `%sim`
block as well as possibly to modify the parameters related to the
spectral range and linewidth of rR bands which are suitable for
comparison with the experimental rR spectrum:

```orca
# excitation energies (cm**-1) for which rR spectra will be calculated:
   RRSE 39808

   # full width half maximum of Raman bands in rR spectra (cm**-1):
   RRS_FWHM  20  

   RSRange   0, 4000  # spectral range for simulation of rR spectra (cm**-1)
   NRRSPoints  4000   # number of points to simulate rR spectra (cm**-1)

   # resonance Raman intensities will be calculated
   # for all vibrational states with excitation number
   # up to RamanOrder:
   RamanOrder 3
```

The calculated rR spectrum is shown in
{numref}`fig:730`. In the
input we have invoked the calculation of rR intensities for the
transitions with up to 3 vibrational quanta in the final vibrational
state (`RamanOrder = 3`). Make sure that the rR intensity pattern in the
given spectral range does not change noticeably upon further increase of
this parameter. Typically, the larger are the normal coordinate
displacements the greater order of Raman scattering is required in the
calculation to account for all the most intense transitions in the rR
spectrum. The inclusion of vibrational transitions beyond the
fundamentals is a particular feature of the `orca_asa` program.

Comparison of the calculated and experimental rR spectra
({numref}`fig:730`) mainly
shows discrepancies in the values of the Raman shifts that are mainly
related to the low accuracy of the vibrational frequencies obtained at
the BHLYP level (typically overestimated by $\approx$ 10%). However, the
intensity patterns of the calculated and experimental rR spectra show
very nice agreement with experiment that is already sufficient to assign
the experimental peaks to individual vibrational transitions. This can
be done upon examination of file `example010.asa.o3.rrs.39808.stk` which
provides intensity, Raman shift, and specification for each vibrational
transition. It is actually one of the most consistent procedures that
enables one to identify different fundamental, overtone and combination
bands in the experimentally observed rR spectrum. Such an assignment is
a necessary prerequisite for the fit. The current example is relatively
straightforward since the spectral region 1--1700 cm$^{-1}$ is actually
dominated by fundamental bands while the most intense overtone and
combination transitions occur at higher frequencies. However, in many
cases even the low-frequency spectral range is characterized by
significant contributions from overtone and combination bands that
sometimes are even more intense than fundamental transitions! Thus,
quantum chemical calculations can greatly facilitate the assignment of
experimental rR bands.

After having performed the assignment it is advisable to discard those
modes from the analysis that are not involved in any of the
experimentally observed fundamental, overtone, or combination rR bands
with noticeable intensities. In the present example these are the modes
6, 8, 10--12 from the input file given above. For these modes it is
implied that the fitted displacement parameters are zero. You will find
that the calculated displacement values are rather small indeed. Also it
is advisable to change the ground-state vibrational frequencies in the
`$vib_freq_gs` block to their experimental values.

Below is the modified input file for the fit run:

```orca
#
# example010-01.asa.inp
#
# ASA input
#
%sim
         model IMDHO
         method Heller
end


%fit 
    
    Fit true  
    AbsFit true  
    RRSFit true
    AbsExpName "hex-abs.dat"  
    ExpAbsScaleMode Rel
    CWAR  5.0

    NMaxFunc  1000 

    SDNCStep  0.5
                    
end  

$el_states
1
   1 39808.0   150.00    0.00    -0.8533  -3.3690  -0.0000

$el_states_c
1
   1     1        1       0           0        0       0 


$vib_freq_gs
7
    1      354.0
    2      444.0 
    3      934.0
    4     1192.0
    5     1290.0
    6     1403.0
    7     1635.0



$sdnc
7 1
                   1    
      1      -0.594359
      2       0.369227
      3      -0.132430
      4      -0.727616
      5       0.406841
      6       0.177617
      7      -1.412258

$sdnc_c
7 1
             1
      1        1
      2        2
      3        3
      4        4
      5        5
      6        6
      7        7

$rrs_exp 
1         
1 1 
    Ex 39809.0 
    NTr  11
    1     
       int   10.0  1.0
       modes  1
       quanta 1;
    2     
       int   5.0  1.0
       modes  2
       quanta 1;
    3     
       int   1.5  1.0
       modes  3
       quanta 1;
    4     
       int   21.0  1.0
       modes  4
       quanta 1;
    5     
       int   7.5  1.0
       modes  5
       quanta 1;
    6     
       int   2.0  1.0
       modes  6
       quanta 1;
    7     
       int   46.0  1.0
       modes  7
       quanta 1;

    8  
       int  6.8 1.0
       modes  1, 7
       quanta 1, 1;

    9  
       int  4.0 1.0
       modes  2, 7
       quanta 1, 1;

   10  
       int  2.0 1.0
       modes  3, 7
       quanta 1, 1;
   
   11  
       int 17.0 1.0
       modes  7   
       quanta 2;
```

In addition to the experimental intensities of fundamental bands the
input file also contains the information about some overtone and
combination transitions. Note that it is not really necessary to include
all of them them into the fit, in particular if some of the rR bands are
strongly overlapping with each other.

Fitted normal coordinate displacements of the excited-state origin show
nice agreement with the published values:

```orca
$sdnc
7 1
                   1    
      1      -0.638244
      2       0.455355
      3      -0.229126
      4      -0.854357
      5       0.501219
      6       0.197679
      7      -1.292997
```

:::{note}

-   It is not really important to employ the BHLYP/SV(P) method in the
    frequency calculations in order to obtain the `.hess` file (this was
    merely done to be consistent with the TDDFT/BHLYP/SV(P) method for
    the excited-state model parameters calculation). The frequency
    calculations can for example be carried out at the BP86/TZVP or
    RI-SCS-MP2/TZVP level of theory. This will provide displacements
    pattern very similar to that of the BHLYP/SV(P) method, but much
    more accurate vibrational frequencies which will further facilitate
    the assignment of rR spectra
    ({numref}`fig:730`).
    However, such a procedure can be inconsistent if the two methods
    give noticeably different normal mode compositions and/or
    vibrational frequencies. From our experience it can lead to
    significant overestimation of the excited-state displacements for
    some low-frequency modes.

-   It is known that predicted dimensionless normal coordinate
    displacements critically depend on the fraction of the "exact"
    Hartree-Fock exchange (EEX) included in hybrid functionals. In
    general no universal amount of EEX exists that provides a uniformly
    good description for all systems and states. Typically, for a given
    molecule either the BHLYP/TZVP (50% of EEX) or B3LYP/TZVP (20% of
    EEX) methods yields simulated spectra that compare very well with
    those from experiment if vibrational frequencies are appropriately
    scaled.
:::

(sec:spectroscopyproperties.asa.notes)=
### Important Notes about Proper Comparison of Experimental and Quantum Chemically Calculated Resonance Raman Spectra

In order to compare experimental and theoretical rR spectra, **it is
necessary to use in both cases excitation energies that are
approximately in resonance with the same vibrational transitions in the
absorption spectrum**. Therefore, in the case of diffuse absorption
spectra (i.e. those not showing resolved vibrational structure) one
needs to adjust the transition energies and linewidth paramters in the
`%el_states` block such that the envelopes of the experimental and
theoretical spectra rouhgly coincide, and then to employ experimental
values of excitation energies to construct theoretical rR spectra.
Typically in the case of diffuse absorption spectra rR profiles are
rather smooth. Therefore, even though excitation energies are not in
resonance with the same vibrational transition in the absorption
spectrum, the rR spectra are not expected to vary significantly in the
case of such mismatch.

In the case of the absorption spectrum with resolved or partially
resolved vibrational structure it is necessary to modify the transition
energies in the `%el_states` block such that the calculated and
experimentally observed 0-0 vibrational peaks coincide, and modify
linewidth parameters so that the low-energy slopes in the calculated and
experimental spectra have a similar behavior.

Consider a single-mode model system for which "experimental" and
calculated absorption spectra are shown in
{numref}`fig:731`.

(fig:731)=
```{figure} ../../images/731.*

Experimental and theoretical absorption spectra for a single-mode
model system. The calculated spectrum is adjusted such that the position
of 0-0 peak coincide with the experimental
one.
```

Comparison of the calculated and experimental spectra shows that some
adjustment of the linewidth parameters is neceassy before construction
of theoretical rR spectra. One can directly compare calculated and
experimental rR spectra upon the excitation at 16200 cm$^{-1}$ which is
in resonance with the 0-0 vibronic band. However, it is not consistent
to use experimental values of the excitation energy in the calculation
of rR spectrum which is in resonance with one of the other vibronic
bands since the separation between vibrational peaks in the experimental
and calculated spectra is different whereby positions of the peaks in
both spectra do not coincide. Instead **one should use the excitaition
energy which corresponds to the same vibronic peak in the calculated
absorption spectrum as in the experimental one**. Alternatively, one can
adjust theoretical value of vibrational frequency such that positions of
corresponding vibronic peaks in the spectra coincide, and then use
experimental values of excitation energies for the calculation of rR
spectra.

(sec:spectroscopyproperties.asa.fitvalues.scan)=
### Example: Normal Mode Scan Calculations of Model Parameters for 1-$^1$A$_g$ $\rightarrow$ 1-$^1$B$_u$ Transition in *trans*-1,3,5-Hexatriene

If excited state gradients are not available (which is the case for many
of the electronic structure methods supported by ORCA), you have to
resort to a more laborious procedure -- single point calculations at
geometries that are displaced along the various normal modes of the
system. This roughly corresponds to taking numerical derivatives --
however, once this extra effort is invested more information can be
obtained from the calculation than what would be possible from an
analytic derivative calculation.

The present example illustrates the application of normal mode scan
calculations for the evaluation of excited state harmonic parameters
that are necessary to simulate optical spectra within the IMDHO model.
This method can be applied with any method like CIS, CASSCF, MRCI or
TD-DFT.

The reference wavefunctions for the multireference calculations reported
below are of the state-averaged CASSCF (SA-CASSCF) type. The complete
active space CAS(6,6) includes all 6 valence shell $\pi$-orbitals. The
average is taken over the first four states which was found necessary in
order to include the ground state and the strongly allowed
1-$^{1}$B$_{u}$state.

```orca
#
# example011.inp
#
# CASSCF normal mode scan calculations
#

# first do single point RHF calculation
! RHF TZVP TightSCF  

* xyz 0 1
 C       -0.002759    0.680006    0.000000
 H       -0.966741    1.204366    0.000000
 C        1.187413    1.500920    0.000000
 H        2.146702    0.969304    0.000000
 C        1.187413    2.850514    0.000000
 H        0.254386    3.420500    0.000000
 H        2.116263    3.422544    0.000000
 C        0.002759   -0.680006    0.000000
 H        0.966741   -1.204366    0.000000
 C       -1.187413   -1.500920    0.000000
 H       -2.146702   -0.969304    0.000000
 C       -1.187413   -2.850514    0.000000
 H       -0.254386   -3.420500    0.000000
 H       -2.116263   -3.422544    0.000000
*


# perform SA-CASSCF calculation upon appropriate rotation of MOs
$new_job
! TZVP TightSCF  

%scf
    rotate {23,27} end
end 

%casscf
        nel 6
        norb  6
        mult  1
        nroots  4
end

* xyz 0 1
 C       -0.002759    0.680006    0.000000
 H       -0.966741    1.204366    0.000000
 C        1.187413    1.500920    0.000000
 H        2.146702    0.969304    0.000000
 C        1.187413    2.850514    0.000000
 H        0.254386    3.420500    0.000000
 H        2.116263    3.422544    0.000000
 C        0.002759   -0.680006    0.000000
 H        0.966741   -1.204366    0.000000
 C       -1.187413   -1.500920    0.000000
 H       -2.146702   -0.969304    0.000000
 C       -1.187413   -2.850514    0.000000
 H       -0.254386   -3.420500    0.000000
 H       -2.116263   -3.422544    0.000000
*


# do normal mode scan calculations
# to map CASSCF ground and excited-state PESs
$new_job
! TZVP TightSCF  NMScan 

%casscf
        nel 6
        norb  6
        mult  1
        nroots  4
end

%rr
    HessName "hexatriene_bp86.hess"
    NMList 10,11,18,24,26,28,29,31,32
    NSteps 6
    FreqAlter true
    EnStep 0.0001
    State 3
end

* xyz 0 1
 C       -0.002759    0.680006    0.000000
 H       -0.966741    1.204366    0.000000
 C        1.187413    1.500920    0.000000
 H        2.146702    0.969304    0.000000
 C        1.187413    2.850514    0.000000
 H        0.254386    3.420500    0.000000
 H        2.116263    3.422544    0.000000
 C        0.002759   -0.680006    0.000000
 H        0.966741   -1.204366    0.000000
 C       -1.187413   -1.500920    0.000000
 H       -2.146702   -0.969304    0.000000
 C       -1.187413   -2.850514    0.000000
 H       -0.254386   -3.420500    0.000000
 H       -2.116263   -3.422544    0.000000
*
```

The file containing the Hessian matrix (`"hexatriene_bp86.hess"`) was
obtained from the BP86/TZVP frequency calculations. The keyword `NMList`
provides the list of the normal modes to be scanned. These should be
only the totally symmetric vibrations, since only they can be
significant for absorption and resonance Raman spectra within the
constraints of the IMDHO model. The `FreqAlter` flag indicates whether
frequency alterations are assumed in the post-scan potential surface
fit. The Parameter `EnStep` is used to select the appropriate step
during the scan calculations. The value is chosen such that the average
energy change (in Eh) in both directions is not less than this
parameter.
