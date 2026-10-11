

<a id="sec:spectroscopyproperties.asa.bandshapes"></a>
# Absorption and Fluorescence Bandshapes using `ORCA_ASA` 

**Please also consider using the more recent ORCA_ESD, described in
Section [spectroscopyproperties.esd](#sec:spectroscopyproperties.esd), to compute bandshapes.**

Bandshape calculations are nontrivial but can be achieved with ORCA
using the procedures described in section [spectroscopyproperties.asa](#sec:spectroscopyproperties.asa).
Starting from version 2.80, analytical TD-DFT gradients are available,
which make these calculations quite fast and applicable without
expert knowledge to larger molecules.

!!! note
    -   Functionals with somewhat more HF exchange produce better results
        and are not as prone to "ghost states" as GGA functionals
        unfortunately are!

    -   Calculations can be greatly sped up by the RI or RIJCOSX
        approximations!

    -   Analytic gradients for the (D) correction and hence for
        double-hybrid functionals are NOT available.

In a nutshell, let us look into the H$_{2}$CO molecule. First we
generate some Hessian (e.g. BP86/SV(P)). Then we run the job that makes
the input for the `orca_asa` program. For example, let us calculate the
five lowest excited states:

```orca
! aug-cc-pVDZ BHandHLYP TightSCF NMGrad 

%tddft nroots 5 end

# this is ASA-specific input
%rr    states 1,2,3,4,5
       HessName "Test-ASA-H2CO-freq.hess"
       ASAInput True
       end 

*int 0 1
 C 0 0 0  0   0     0 
 O 1 0 0  1.2 0     0
 H 1 2 0  1.1 120   0
 H 1 2 3  1.1 120 180
*
```

The ORCA run will produce a file `Test-ASA-H2CO.asa.inp` that is an
input file for the program that generates various spectra. It is an
ASCII file that is very similar in appearance to an ORCA input file:

```orca
#
# ASA input
#
%sim     model IMDHO
         method Heller

         AbsRange     25000.0,  100000.0
         NAbsPoints   1024

         FlRange      25000.0,  100000.0
         NFlPoints    1024

         RRPRange     5000.0,  100000.0
         NRRPPoints   1024

         RRSRange        0.0,    4000.0
         NRRSPoints   4000

         # Excitation energies (cm**-1) for which rR spectra will
         # be calculated. Here we choose all allowed transitions
         # and the position of the 0-0 band
         RRSE 58960, 66884, 66602

         # full width half maximum of Raman bands in rR spectra
         # (cm**-1):
         RRS_FWHM 10.0

         AbsScaleMode Ext
         FlScaleMode  Rel
         # RamanOrder=1 means only fundamentals. For 2 combination
         # bands and first overtones are also considered, for 3
         # one has second overtones etc.
         RamanOrder   1

         # E0 means the adiabatic excitation energy
         # EV would mean the vertical one. sprints vertical
         # excitations in the TD-DFT output but for the input into
         # the ASA program the adiabatic excitation energies are
         # estimated. A rigorous calculation would of course in-
         # volve excited state geometry optimization
         EnInput E0

         CAR   0.800
         end

# These are the calculated electronic states and transition moments
# Note that this is in the Franck-Condon approximation and thus
# the transition moments have been calculated vertically
$el_states
5
   1 32200.79   100.00    0.00    -0.0000   0.0000  -0.0000
   2 58960.05   100.00    0.00     0.0000  -0.4219   0.0000
   3 66884.30   100.00    0.00    -0.0000   0.4405   0.0000
   4 66602.64   100.00    0.00    -0.5217  -0.0000   0.0000
   5 72245.42   100.00    0.00     0.0000   0.0000   0.0000

# These are the calculated vibrational frequencies for the totally
# symmetric modes. These are the only ones that contribute. They
# correspond to x, H-C-H bending, C=O stretching and C-H stretching
# respectively
$vib_freq_gs
3
    1     1462.948534
    2     1759.538581
    3     2812.815170

# These are the calculated dimensional displacements for all
# electronic states along all of the totally symmetric modes.
$sdnc
3 5
                   1          2          3          4          5
      1      -0.326244   0.241082  -0.132239   0.559635   0.292190
      2      -1.356209   0.529823   0.438703   0.416161   0.602301
      3      -0.183845   0.418242   0.267520   0.278880   0.231340
```

After setting `NAbsPoints` variable and spectral ranges in this file
to the desired values, we invoke `orca_asa` as:

```orca
orca_asa Test-ASA-H2CO.asa.inp
```

This produces the following output:

```orca
******************
                                    * O R C A  A S A *
                                    ******************

                    --- A program for analysis of electronic spectra ---

Reading file: Test-ASA-H2CO.asa.inp ... done

         **************************************************************
         *        GENERAL CHARACTERISTICS OF ELECTRONIC SPECTRA        *
         **************************************************************

--------------------------------------------------------------------------------
  State      E0           EV       fosc    Stokes shift  Effective Stokes shift
          (cm**-1)     (cm**-1)              (cm**-1)           (cm**-1)
--------------------------------------------------------------------------------
    1:     30457.24   32200.79   0.000000      0.00                0.00
    2:     58424.56   58960.05   0.031879      0.00                0.00
    3:     66601.54   66884.30   0.039422      0.00                0.00
    4:     66111.80   66602.64   0.055063      0.00                0.00
    5:     71788.55   72245.42   0.000000      0.00                0.00

------------------------------------------------------------------------------------------
                              BROADENING PARAMETETRS (cm**-1)
------------------------------------------------------------------------------------------
             Intrinsic                                    Effective
 State -------------------------  --------------------------------------------------------
                                               Sigma                         FWHM
        Gamma    Sigma    FWHM    --------------------------   ---------------------------
                                    0K       77K     298.15K      0K       77K     298.15K
-------------------------------------------------------------------------------------------
  1:   100.00     0.00   200.00     0.00      0.00      0.00    200.00    200.00    200.00
  2:   100.00     0.00   200.00     0.00      0.00      0.00    200.00    200.00    200.00
  3:   100.00     0.00   200.00     0.00      0.00      0.00    200.00    200.00    200.00
  4:   100.00     0.00   200.00     0.00      0.00      0.00    200.00    200.00    200.00
  5:   100.00     0.00   200.00     0.00      0.00      0.00    200.00    200.00    200.00

Calculating absorption spectrum   ...
The maximum number of grid points ... 5840
Time for absorption               ...       9.569 sec (=   0.159 min)
Writing file: Test-ASA-H2CO.asa.abs.dat ... done
Writing file: Test-ASA-H2CO.asa.abs.as.dat ... done

Generating vibrational states up to the  1-th(st) order  ...   done
Total number of vibrational states                       ...      3

Calculating rR profiles for all vibrational states up to the 1-th order
State 1 ...
The maximum number of grid points ... 6820
Resonance Raman profile is done
State 2 ...
The maximum number of grid points ... 6820
Resonance Raman profile is done
State 3 ...
The maximum number of grid points ... 6820
Resonance Raman profile is done
Writing file: Test-ASA-H2CO.asa.o1.dat... done
Writing file: Test-ASA-H2CO.asa.o1.info... done

Calculating rR spectra involving vibrational states up to the 1-th(st) order
State    1 ... done
State    2 ... done
State    3 ... done

Writing file: Test-ASA-H2CO.asa.o1.rrs.58960.dat      ... done
Writing file: Test-ASA-H2CO.asa.o1.rrs.58960.stk      ... done
Writing file: Test-ASA-H2CO.asa.o1.rrs.66884.dat      ... done
Writing file: Test-ASA-H2CO.asa.o1.rrs.66884.stk      ... done
Writing file: Test-ASA-H2CO.asa.o1.rrs.66602.dat      ... done
Writing file: Test-ASA-H2CO.asa.o1.rrs.66602.stk      ... done
Writing file: Test-ASA-H2CO.asa.o1.rrs.as.58960.dat   ... done
Writing file: Test-ASA-H2CO.asa.o1.rrs.as.58960.stk   ... done
Writing file: Test-ASA-H2CO.asa.o1.rrs.as.66884.dat   ... done
Writing file: Test-ASA-H2CO.asa.o1.rrs.as.66884.stk   ... done
Writing file: Test-ASA-H2CO.asa.o1.rrs.as.66602.dat   ... done
Writing file: Test-ASA-H2CO.asa.o1.rrs.as.66602.stk   ... done
Writing file: Test-ASA-H2CO.asa.o1.rrs.all.xyz.dat    ... done

TOTAL RUN TIME: 0 days 0 hours 1 minutes 17 seconds 850 msec
```

The computed vibrationally resolved absorption spectrum is plotted as
shown in Figure [fig:633](#fig:633). 

<a id="fig:633"></a>
!!! note "../../images/633.*"
    The computed vibrationally resolved absorption spectrum of the H$_{2}$CO molecule

The computed fluorescence spectrum of the lowest energy peak is 
plotted as shown in Figure [fig:634](#fig:634). This peak corresponds to
S2. Although it is not realistic, it is sufficient for illustrative purposes.

<a id="fig:634"></a>
!!! note "../../images/634.*"
    The computed fluorescence spectrum of the lowest energy peak of the H$_{2}$CO molecule

The computed Resonance Raman (rR) excitation profiles of the three totally symmetric
vibrational modes are plotted as shown in Figure [fig:635](#fig:635).

<a id="fig:635"></a>
!!! note "../../images/635.*"
    The computed Resonance Raman excitation profiles of the three totally symmetric
    vibrational modes of the H$_{2}$CO molecule

As might be expected, the dominant enhancement occurs under the main
peaks for the C$=$O stretching vibration. Higher energy excitations
particularly enhance the C-H vibrations. The computed rR spectra at 
the vertical excitation energies are provided in Figure [fig:636](#fig:636).

<a id="fig:636"></a>
!!! note "../../images/636.*"
    The computed Resonance Raman spectra at the vertical excitation energies
    of the H$_{2}$CO molecule

In this toy example, the dominant mode is the C$=$O stretching,
and the spectra look similar for all excitation wavelengths. However, 
electronically excited states are mostly of different natures, yielding
drastically different rR spectra. Thus, rR spectra serve as powerful 
fingerprints of the electronic excitation being studied. 
This is also true even if the vibrational structure of the absorption 
band is not resolved, which is usually the case for large molecules.

The `orca_asa` program is much more powerful than described in this section.
Please refer to section [spectroscopyproperties.asa](#sec:spectroscopyproperties.asa) for a full description of its
features. The `orca_asa` program can also be interfaced to other electronic
structure codes that deliver excited state gradients and can be used to fit
experimental data. It is thus a tool for experimentalists and theoreticians
at the same time!
