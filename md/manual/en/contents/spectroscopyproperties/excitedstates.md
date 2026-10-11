```{index} Excited States Calculations
```

(sec:spectroscopyproperties.excitedstates)=
# Excited States Calculations

A plethora of methods to compute excited states exists in ORCA.
Here we give a brief overview of the main methods, with focus on the basic usage 
and current capabilities of each. Detailed documentation for each method
is indicated in each subsection.

Multi-reference methods, such as NEVPT2 or MRCI, are described elsewhere
({ref}`sec:modelchemistries.nevpt2`, {ref}`sec:modelchemistries.mrci`) in the manual.

```{index} TD-DFT
```
(sec:spectroscopyproperties.excitedstates.tddft)=
## Excited States with RPA, CIS, TD-DFT and SF-TDA

ORCA features a module to perform TD-DFT, single-excitation CI (CIS) and RPA.
The module works with either closed-shell (RHF or RKS) or unrestricted (UHF or UKS) reference wavefunctions.
For DFT models the module automatically chooses TD-DFT and for HF wavefunctions the CIS model.
If the RI approximation is used in the SCF part it will also be used in the excited states calculation.
A detailed documentation is provided in section {ref}`sec:spectroscopyproperties.tddft`

(sec:spectroscopyproperties.excitedstates.tddft.general)=
### General Use

In its simplest form it is only necessary to provide the number of roots
sought:

```orca
! BP86 def2-SVP TightSCF

%tddft
  Nroots   10
  triplets true
end

*xyz 0 1
  C     0.016227   -0.000000    0.000000
  O     1.236847    0.000000   -0.000000
  H    -0.576537    0.951580   -0.000000
  H    -0.576537   -0.951580   -0.000000
end
```

Which gives the following output:

```orca
------------------------------------
TD-DFT/TDA EXCITED STATES (SINGLETS)
------------------------------------

the weight of the individual excitations are printed if larger than 1.0e-02

STATE  1:  E=   0.142238 au      3.870 eV    31217.5 cm**-1 <S**2> =   0.000000 Mult 1
     7a ->   8a  :     0.999852 (c=  0.99992610)

STATE  2:  E=   0.279148 au      7.596 eV    61265.8 cm**-1 <S**2> =   0.000000 Mult 1
     7a ->   9a  :     0.991058 (c=  0.99551880)

STATE  3:  E=   0.326547 au      8.886 eV    71668.9 cm**-1 <S**2> =   0.000000 Mult 1
     5a ->   8a  :     0.992394 (c= -0.99618994)

STATE  4:  E=   0.339416 au      9.236 eV    74493.3 cm**-1 <S**2> =   0.000000 Mult 1
     6a ->   8a  :     0.214928 (c=  0.46360308)
     7a ->  10a  :     0.760130 (c= -0.87185424)

STATE  5:  E=   0.357323 au      9.723 eV    78423.4 cm**-1 <S**2> =   0.000000 Mult 1
     4a ->   8a  :     0.998607 (c=  0.99930350)

STATE  6:  E=   0.396031 au     10.777 eV    86918.7 cm**-1 <S**2> =   0.000000 Mult 1
     7a ->  11a  :     0.995757 (c= -0.99787607)

STATE  7:  E=   0.412518 au     11.225 eV    90537.2 cm**-1 <S**2> =   0.000000 Mult 1
     3a ->   8a  :     0.015703 (c=  0.12531336)
     6a ->   9a  :     0.982525 (c=  0.99122380)

STATE  8:  E=   0.420413 au     11.440 eV    92270.0 cm**-1 <S**2> =   0.000000 Mult 1
     4a ->  10a  :     0.023644 (c= -0.15376603)
     5a ->   9a  :     0.184687 (c= -0.42975192)
     5a ->  11a  :     0.029413 (c= -0.17150093)
     6a ->   8a  :     0.535798 (c= -0.73198239)
     7a ->  10a  :     0.161330 (c= -0.40165919)
     7a ->  14a  :     0.031134 (c=  0.17644805)

STATE  9:  E=   0.454354 au     12.364 eV    99719.1 cm**-1 <S**2> =   0.000000 Mult 1
     5a ->   9a  :     0.801630 (c=  0.89533782)
     5a ->  11a  :     0.012558 (c= -0.11206253)
     6a ->   8a  :     0.103311 (c= -0.32142015)
     7a ->  10a  :     0.051303 (c= -0.22650208)
     7a ->  14a  :     0.016544 (c=  0.12862428)

STATE 10:  E=   0.474384 au     12.909 eV   104115.2 cm**-1 <S**2> =   0.000000 Mult 1
     6a ->  10a  :     0.998860 (c= -0.99942977)
```

and the triplets:

```orca
------------------------------------
TD-DFT/TDA EXCITED STATES (TRIPLETS)
------------------------------------

the weight of the individual excitations are printed if larger than 1.0e-02

STATE 11:  E=   0.114291 au      3.110 eV    25084.1 cm**-1 <S**2> =   2.000000 Mult 3
     7a ->   8a  :     0.999453 (c=  0.99972624)

STATE 12:  E=   0.213324 au      5.805 eV    46819.1 cm**-1 <S**2> =   2.000000 Mult 3
     6a ->   8a  :     0.996522 (c=  0.99825941)

STATE 13:  E=   0.255583 au      6.955 eV    56094.1 cm**-1 <S**2> =   2.000000 Mult 3
     7a ->   9a  :     0.992767 (c=  0.99637714)

STATE 14:  E=   0.276345 au      7.520 eV    60650.8 cm**-1 <S**2> =   2.000000 Mult 3
     5a ->   8a  :     0.998251 (c= -0.99912505)

STATE 15:  E=   0.316749 au      8.619 eV    69518.3 cm**-1 <S**2> =   2.000000 Mult 3
     7a ->  10a  :     0.991502 (c= -0.99574190)

STATE 16:  E=   0.327793 au      8.920 eV    71942.2 cm**-1 <S**2> =   2.000000 Mult 3
     4a ->   8a  :     0.994029 (c=  0.99701018)

STATE 17:  E=   0.377551 au     10.274 eV    82862.9 cm**-1 <S**2> =   2.000000 Mult 3
     7a ->  11a  :     0.998586 (c= -0.99929259)

STATE 18:  E=   0.400159 au     10.889 eV    87824.7 cm**-1 <S**2> =   2.000000 Mult 3
     3a ->   8a  :     0.062364 (c=  0.24972706)
     6a ->   9a  :     0.934672 (c= -0.96678411)

STATE 19:  E=   0.433339 au     11.792 eV    95107.0 cm**-1 <S**2> =   2.000000 Mult 3
     5a ->   9a  :     0.988277 (c=  0.99412115)

STATE 20:  E=   0.445213 au     12.115 eV    97713.0 cm**-1 <S**2> =   2.000000 Mult 3
     3a ->   8a  :     0.934403 (c=  0.96664514)
     6a ->   9a  :     0.063400 (c=  0.25179341)
```

By default, it also prints the dipole absorption and circular dichroism spectra:

```orca
----------------------------------------------------------------------------------------------------
                     ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS
----------------------------------------------------------------------------------------------------
     Transition      Energy     Energy  Wavelength fosc(D2)      D2        DX        DY        DZ
                      (eV)      (cm-1)    (nm)                 (au**2)    (au)      (au)      (au)
----------------------------------------------------------------------------------------------------
  0-1A  ->  1-3A    3.110029   25084.1   398.7   0.000000000   0.00000   0.00000   0.00000   0.00000
  0-1A  ->  1-1A    3.870479   31217.5   320.3   0.000000000   0.00000  -0.00000   0.00000   0.00000
  0-1A  ->  2-3A    5.804830   46819.1   213.6   0.000000000   0.00000   0.00000   0.00000   0.00000
  0-1A  ->  3-3A    6.954778   56094.1   178.3   0.000000000   0.00000   0.00000   0.00000   0.00000
  0-1A  ->  4-3A    7.519743   60650.8   164.9   0.000000000   0.00000   0.00000   0.00000   0.00000
  0-1A  ->  2-1A    7.595990   61265.8   163.2   0.139374365   0.74893  -0.00000   0.86541  -0.00000
  0-1A  ->  5-3A    8.619170   69518.3   143.8   0.000000000   0.00000   0.00000   0.00000   0.00000
  0-1A  ->  3-1A    8.885804   71668.9   139.5   0.002010847   0.00924   0.00000  -0.00000  -0.09611
  0-1A  ->  6-3A    8.919695   71942.2   139.0   0.000000000   0.00000   0.00000   0.00000   0.00000
  0-1A  ->  4-1A    9.235990   74493.3   134.2   0.021695302   0.09588  -0.30964  -0.00000  -0.00000
  0-1A  ->  5-1A    9.723256   78423.4   127.5   0.000000000   0.00000  -0.00000   0.00000  -0.00000
  0-1A  ->  7-3A   10.273692   82862.9   120.7   0.000000000   0.00000   0.00000   0.00000   0.00000
  0-1A  ->  6-1A   10.776542   86918.7   115.1   0.009793664   0.03709   0.00000  -0.19260  -0.00000
  0-1A  ->  8-3A   10.888868   87824.7   113.9   0.000000000   0.00000   0.00000   0.00000   0.00000
  0-1A  ->  7-1A   11.225180   90537.2   110.5   0.002033718   0.00740   0.00000  -0.00000   0.08599
  0-1A  ->  8-1A   11.440020   92270.0   108.4   0.371220034   1.32448  -1.15086  -0.00000   0.00000
  0-1A  ->  9-3A   11.791761   95107.0   105.1   0.000000000   0.00000   0.00000   0.00000   0.00000
  0-1A  -> 10-3A   12.114872   97713.0   102.3   0.000000000   0.00000   0.00000   0.00000   0.00000
  0-1A  ->  9-1A   12.363588   99719.1   100.3   0.259360077   0.85625  -0.92534   0.00000   0.00000
  0-1A  -> 10-1A   12.908634  104115.2    96.0   0.000000000   0.00000  -0.00000  -0.00000  -0.00000
```

```orca
------------------------------------------------------------------------------------------
                     CD SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS
------------------------------------------------------------------------------------------
     Transition      Energy     Energy  Wavelength    R        MX        MY        MZ
                      (eV)      (cm-1)    (nm)   (1e40*cgs)   (au)      (au)      (au)
------------------------------------------------------------------------------------------
  0-1A  ->  1-3A    3.110029   25084.1   398.7   -0.00000   0.00000   0.00000   0.00000
  0-1A  ->  1-1A    3.870479   31217.5   320.3    0.00000   0.58235   0.00000   0.00000
  0-1A  ->  2-3A    5.804830   46819.1   213.6   -0.00000   0.00000   0.00000   0.00000
  0-1A  ->  3-3A    6.954778   56094.1   178.3   -0.00000   0.00000   0.00000   0.00000
  0-1A  ->  4-3A    7.519743   60650.8   164.9   -0.00000   0.00000   0.00000   0.00000
  0-1A  ->  2-1A    7.595990   61265.8   163.2   -0.00000  -0.00000   0.00000   0.32961
  0-1A  ->  5-3A    8.619170   69518.3   143.8   -0.00000   0.00000   0.00000   0.00000
  0-1A  ->  3-1A    8.885804   71668.9   139.5   -0.00000  -0.00000  -0.73058   0.00000
  0-1A  ->  6-3A    8.919695   71942.2   139.0   -0.00000   0.00000   0.00000   0.00000
  0-1A  ->  4-1A    9.235990   74493.3   134.2   -0.00000  -0.00000  -0.00000  -0.00000
  0-1A  ->  5-1A    9.723256   78423.4   127.5    0.00000   0.31342  -0.00000   0.00000
  0-1A  ->  7-3A   10.273692   82862.9   120.7   -0.00000   0.00000   0.00000   0.00000
  0-1A  ->  6-1A   10.776542   86918.7   115.1    0.00000   0.00000   0.00000   0.58743
  0-1A  ->  8-3A   10.888868   87824.7   113.9   -0.00000   0.00000   0.00000   0.00000
  0-1A  ->  7-1A   11.225180   90537.2   110.5   -0.00000   0.00000  -0.06966   0.00000
  0-1A  ->  8-1A   11.440020   92270.0   108.4   -0.00000  -0.00000  -0.00000   0.00000
  0-1A  ->  9-3A   11.791761   95107.0   105.1   -0.00000   0.00000   0.00000   0.00000
  0-1A  -> 10-3A   12.114872   97713.0   102.3   -0.00000   0.00000   0.00000   0.00000
  0-1A  ->  9-1A   12.363588   99719.1   100.3   -0.00000  -0.00000  -0.00000  -0.00000
  0-1A  -> 10-1A   12.908634  104115.2    96.0    0.00000   0.00260   0.00000   0.00000
```

Which can be processed with {ref}`sec:utilities.mapspc` for plotting.

<!--```{literalinclude} ../../orca_working_input/C05S05_154.inp
:language: orca
``` -->

The triplets parameter is only valid for closed-shell references. If
chosen as true the program will also determine the triplet excitation
energies in addition to the singlets.

The collinear spin-flip version of CIS/TDA (always starting from an
open-shell reference!) can be invoked in a similar manner, using:

```orca
%tddft
  Nroots 5
  sf     true
end
```

Please check the section {ref}`sec:spectroscopyproperties.sftddft.dft` for more details
on how to use it, and how to understand its results.

If one wants to compute transient spectra, or transition dipoles
starting from a given excited state, the option `DOTRANS` must be set to
TRUE and an IROOT should be given for the initial state (the default is
1). If `DOTRANS ALL` is requested instead, the transition dipoles between
all states are computed. The transient transition dipoles will then be
printed after the normal spectra.

This option is currently only available for CIS/TDA and is done using the expectation
value formalism, as the other transition dipole moments in ORCA.

```orca
%tddft
  IROOT    2
  DOTRANS  TRUE
           #or
  DOTRANS  ALL
end
```

(sec:spectroscopyproperties.excitedstates.tddft.ccapabilities)=
### Capabilities

Currently, the TD-DFT/CIS module is able to calculate excitation energies, absorption spectra and
circular dichroism spectra. Within the TD-DFT method, magnetic circular dichroism (see {ref}`sec:spectroscopyproperties.mcd`)
and transient spectra can also be calculated.

Analytical gradients are available for TD-DFT in both restricted and unrestricted 
formalisms and also for the collinear spin-flip variant, which allows for geometry optimizations
of excited states as described in {ref}`sec:spectroscopyproperties.tddft.geometry`.


```{index} ROCIS
```

(sec:spectroscopyproperties.excitedstates.rocis)=
## Excited States with Restricted Open-shell CIS - ROCIS

In addition to the CIS/TD-DFT description of excited states, ORCA
features the ROCIS method{cite}`roemelt2013`, {cite}`roemelt2013b`, which performs 
configuration interaction with single excitations calculations using a restricted open-shell
Hartree-Fock (ROHF) reference.

Starting from ORCA 6.0, the general-spin ROCIS (`GS-ROCIS`) {cite}`gouveia2025JPCA` implementation is available.
This new implementation can handle CSFs with arbitrary spin couplings obtained via
the `CSF-ROHF` method as references.

The main scope of ROCIS is to calculate L-edge and M-edge X-ray absorption spectra (XAS) as well as X-ray
magnetic circular dichroism (XMCD) and resonant inelastic X-ray scattering (RIXS). The computational costs
are usually larger than TD-DFT, but significantly smaller than coupled-cluster based methods.
Together with the pair natural orbital approach (`PNO-ROCIS`), spectra of medium to large molecular sizes are feasible
to be calculated.

For a detailed documentation check {ref}`sec:spectroscopyproperties.rocis`.

(sec:spectroscopyproperties.excitedstates.rocis.general)=
### General Use

The method is invoked by providing the number of roots sought in the
`%rocis` block of the input file:

<!-- >```{literalinclude} ../../orca_working_input/C05S05_160.inp
:language: orca
``` -->

```orca
!def2-SVP TightSCF

%scf
 HFTyp ROHF
 ROHF_CASE HIGHSPIN
 ROHF_NEL[1] 2
end

%rocis
 NRoots 10
end

* xyz 0 3 
 C 0  0       0.1058
 H 0  0.9910 -0.3174
 H 0 -0.9910 -0.3174
end
```

By default, the original `ROCIS` implementation is invoked, which is capable of dealing
only with high-spin `ROHF` references, giving the following output:

```orca
Eigenvectors of ROCIS calculation:
the threshold for printing is: 1e-02

i->a        single excitation from orbital i to a
i->t->a     single excitation from orbital i to a with a spin flip in orbital t
i->t ; w->a double excitation from orbital i to t and orbital w to a

STATE   0   Exc. Energy:   0.000mEh   0.000eV           0.0cm**-1
        0                  :   0.9880  (0.993993)

STATE   1   Exc. Energy: 291.825mEh   7.941eV       64048.2cm**-1
       2->3                 :   0.9602   (0.979900)

STATE   2   Exc. Energy: 307.258mEh   8.361eV       67435.4cm**-1
       1->4                 :   0.0244   (-0.156226)
       4->5                 :   0.9086   (-0.953183)
       4->11                :   0.0379   (-0.194741)
       1->3    ;    4->5     :   0.0126   (-0.112387)

STATE   3   Exc. Energy: 311.967mEh   8.489eV       68468.7cm**-1
       2->4                 :   0.9558   (-0.977660)
       4->6                 :   0.0181   (0.134462)

STATE   4   Exc. Energy: 349.147mEh   9.501eV       76629.0cm**-1
       3->5                 :   0.8588   (-0.926723)
       3->11                :   0.0299   (-0.173056)
       1->3   ->5           :   0.0561   (0.236925)

STATE   5   Exc. Energy: 374.241mEh  10.184eV       82136.4cm**-1
       2->4                 :   0.0187   (0.136885)
       4->6                 :   0.9224   (0.960395)
       4->12                :   0.0360   (0.189800)

STATE   6   Exc. Energy: 413.285mEh  11.246eV       90705.6cm**-1
       3->6                 :   0.8368   (0.914777)
       3->12                :   0.0307   (0.175082)
       1->6                 :   0.0148   (-0.121572)
       1->3   ->6           :   0.0376   (-0.193912)
       2->3   ->5           :   0.0456   (0.213492)

STATE   7   Exc. Energy: 474.514mEh  12.912eV      104143.8cm**-1
       1->3                 :   0.8308   (-0.911467)
       2->3   ->6           :   0.0826   (0.287351)
       2->3   ->12          :   0.0148   (0.121501)

STATE   8   Exc. Energy: 501.672mEh  13.651eV      110104.2cm**-1
       1->4                 :   0.8364   (-0.914550)
       4->5                 :   0.0249   (0.157804)
       4->7                 :   0.0561   (0.236863)
       2->4    ;    3->6     :   0.0324   (-0.180124)

STATE   9   Exc. Energy: 511.571mEh  13.921eV      112276.9cm**-1
       3->6                 :   0.0580   (0.240898)
       1->6                 :   0.0166   (-0.128707)
       2->5                 :   0.1178   (0.343223)
       2->3   ->5           :   0.3041   (-0.551423)
       2->4   ->5           :   0.2625   (-0.512374)
```

The general-spin version `GS-ROCIS` can be requested via:

```orca
!def2-SVP TightSCF

%scf
 HFTyp ROHF
 ROHF_CASE HIGHSPIN
 ROHF_NEL[1] 2
end

%rocis
 DoGenROCIS true
 ReferenceMult 3
 NRoots 10
end

* xyz 0 3 
 C 0  0       0.1058
 H 0  0.9910 -0.3174
 H 0 -0.9910 -0.3174
end
```

The output gives the resulting spin coupling in addition to orbital information:

```orca
Eigenvectors of ROCIS calculation:
the threshold for printing is: 1e-02

  i->a            single excitation from orbital i to a
  i->t ; w->a     double excitation from orbital i to t and orbital w to a

STATE   0   Exc. Energy:   0.000mEh   0.000eV           0.0cm**-1
        0                   :   0.9880   (-0.993993)  : spin coupling:  2+1+1 0

STATE   1   Exc. Energy: 291.825mEh   7.941eV       64048.2cm**-1
       2->3                  :   0.9602   (0.979900)  : spin coupling: +1 2+1 0

STATE   2   Exc. Energy: 307.258mEh   8.361eV       67435.4cm**-1
       1->4                  :   0.0244   (-0.156226) : spin coupling: +1+1 2 0 
       4->5                  :   0.9086   (-0.953183) : spin coupling:  2+1 0+1 
       4->11                 :   0.0379   (-0.194741) : spin coupling:  2+1 0+1 
       1->3    ;    4->5     :   0.0126   (0.112387)  : spin coupling: +1 2 0+1 

STATE   3   Exc. Energy: 311.967mEh   8.489eV       68468.7cm**-1
       2->4                  :   0.9558   (0.977660)  : spin coupling: +1+1 2 0 
       4->6                  :   0.0181   (-0.134462) : spin coupling:  2+1 0+1 

STATE   4   Exc. Energy: 349.147mEh   9.501eV       76629.0cm**-1
       3->5                  :   0.8588   (-0.926723) : spin coupling:  2 0+1+1
       3->11                 :   0.0299   (-0.173056) : spin coupling:  2 0+1+1
       1->5                  :   0.0695   (-0.263669) : spin coupling: +1-1+1+1

STATE   5   Exc. Energy: 374.241mEh  10.184eV       82136.4cm**-1
       2->4                  :   0.0187   (-0.136885) : spin coupling: +1+1 2 0 
       4->6                  :   0.9224   (-0.960395) : spin coupling:  2+1 0+1 
       4->12                 :   0.0360   (-0.189800) : spin coupling:  2+1 0+1 

STATE   6   Exc. Energy: 413.285mEh  11.246eV       90705.6cm**-1
       3->6                  :   0.8368   (-0.914777) : spin coupling:  2 0+1+1
       3->12                 :   0.0307   (-0.175082) : spin coupling:  2 0+1+1
       1->6                  :   0.0609   (-0.246700) : spin coupling: +1-1+1+1
       2->5                  :   0.0242   (-0.155666) : spin coupling: +1+1+1-1
       2->5                  :   0.0345   (0.185684)  : spin coupling: +1-1+1+1

STATE   7   Exc. Energy: 474.514mEh  12.912eV      104143.8cm**-1
       1->3                  :   0.8308   (-0.911467) : spin coupling: +1 2+1 0
       2->6                  :   0.0374   (0.193474)  : spin coupling: +1+1+1-1
       2->6                  :   0.0631   (-0.251226) : spin coupling: +1-1+1+1
       2->12                 :   0.0134   (-0.115919) : spin coupling: +1-1+1+1

STATE   8   Exc. Energy: 501.672mEh  13.651eV      110104.2cm**-1
       1->4                  :   0.8364   (0.914550)  : spin coupling: +1+1 2 0 
       4->5                  :   0.0249   (-0.157804) : spin coupling:  2+1 0+1 
       4->7                  :   0.0561   (-0.236863) : spin coupling:  2+1 0+1 
       2->4    ;    3->6     :   0.0324   (0.180124)  : spin coupling: +1 0 2+1 

STATE   9   Exc. Energy: 511.571mEh  13.921eV      112276.9cm**-1
       3->6                  :   0.0580   (0.240898)  : spin coupling:  2 0+1+1
       1->6                  :   0.0311   (0.176432)  : spin coupling: +1+1+1-1
       2->5                  :   0.6111   (-0.781719) : spin coupling: +1+1+1-1
       2->5                  :   0.0557   (0.235994)  : spin coupling: +1+1-1+1
       2->5                  :   0.2060   (0.453844)  : spin coupling: +1-1+1+1
       2->11                 :   0.0115   (0.107060)  : spin coupling: +1-1+1+1
```

`GS-ROCIS` requires a valid `ROHF` solution as reference (either high-spin or a specific CSF).
For this, one would use the `CSF-ROHF` method to obtain the reference wavefunction for 
which `GS-ROCIS` will be performed:

```orca
%scf
  HFTyp ROHF
  ROHF_CASE HIGHSPIN, USER_CSF or AF_CSF
end
```

For more details on the `CSF-ROHF` method, check {ref}`sec:modelchemistries.hftype.rohf`.

The parametrized `ROCIS/DFT` formulation can be requested by:

```orca
%rocis
  DoGenROCIS            false   # ROCIS/DFT is available only for the high-spin implementation of ROCIS.
  DoDFTCIS               true   # Switches on the ROCIS/DFT method.
  DFTCIS_c = 0.18, 0.20, 0.40   # Array input of the three parameters.
end
```

:::{important}
-   Currently, `ROCIS/DFT` is not implemented for the general-spin (`GS-ROCIS`) procedure.
:::


(sec:spectroscopyproperties.excitedstates.rocis.capabilities)=
### Capabilities

At the present, ROCIS can be used to calculate excitation energies, absorption, circular dichroism and
magnetic circular dichroism spectra. It is also capable of calculating resonant inelastic X-ray scattering
(RIXS) spectra. Magnetic properties such as g-tensors, zero-field splittings, hyperfine couplings and
electric field gradients are also available.


```{index} MC-RPA
```

(sec:spectroscopyproperties.excitedstates.mcrpa)=
## Excited States for Open-Shell Molecules with CASSCF Linear Response (MC-RPA) 

ORCA has the possibility to calculate excitation energies, oscillator
and rotatory strengths for CASSCF wave functions within the response
theory (MC-RPA)
formalism.{cite}`Yeager1979,Joergensen1988,Helmich-Paris2019a` The main
scope of MC-RPA is to simiulate UV/Vis and ECD absorption spectra of
open-shell molecules like transition metal complexes and organic
radicals. MC-RPA absorption spectra are usually more accurate than those
obtained from the state-averaged CASSCF ansatz as orbital relaxation
effects for excited states are taken into account. The computational
costs are ususally larger than those of SA-CASSCF and should be
comparable to a TD-DFT calculation for feasible active space sizes.

(sec:spectroscopyproperties.excitedstates.mcrpa.general)=
### General Use

MC-RPA needs a converged state-specific CASSCF calculation of the
electronic ground state. The only necessary information that the user
has to provide is the desired number of excited states (roots). All
other keywords are just needed to control the Davidson algorithm or post
process the results. A minimal input for calculating the four lowest
singlet excited states of ethylene could like the following:

```orca
#
# CASSCF + MCRPA for C2H4
#
! DEF2-SVP DEF2-TZVP/C VeryTightSCF

%casscf 
 nel          2 
 norb         2
 mult         1
 nroots       1
 gtol 1e-6
 etol 1e-10
end

%mcrpa
 nroots       8
end

* int 0 1
C  0  0  0 0         0    0
C  1  0  0 1.3385    0    0
H  1  2  0 1.07    120    0
H  1  2  3 1.07    120  180
H  2  1  3 1.07    120    0
H  2  1  3 1.07    120  180
*
```

<!-- >```{literalinclude} ../../orca_working_input/C08S06_01.inp
:language: orca
``` -->

After the residual norm is below a user-given threshold `TolR` we get
the following information

```orca
 -------------------------------------------------------------

     All 8 RPA Roots CONVERGED Below 1.000e-05

 -------------------------------------------------------------
    3  (root    0)       3.352976e-01     3.489323e-07    Yes 
       (root    1)       3.485288e-01     1.656998e-08    Yes 
       (root    2)       3.514846e-01     2.178527e-08    Yes 
       (root    3)       3.741213e-01     2.577113e-07    Yes 
       (root    4)       3.743973e-01     2.416887e-08    Yes 
       (root    5)       4.040700e-01     4.609207e-08    Yes 
       (root    6)       4.479248e-01     1.240222e-08    Yes 
       (root    7)       4.609744e-01     6.311327e-09    Yes 
```

and the absorption and ECD spectrum

```orca
----------------------------------------------------------------------------------------------------
                     ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS
----------------------------------------------------------------------------------------------------
     Transition      Energy     Energy  Wavelength fosc(D2)      D2        DX        DY        DZ
                      (eV)      (cm-1)    (nm)                 (au**2)    (au)      (au)      (au)
----------------------------------------------------------------------------------------------------
  0-1A  ->  1-1A    9.123912   73589.3   135.9   0.430768702   1.92710   1.38820  -0.00000  -0.00000
  0-1A  ->  2-1A    9.483952   76493.2   130.7   0.009915132   0.04267   0.00000  -0.00000  -0.20657
  0-1A  ->  3-1A    9.564384   77142.0   129.6   0.000000000   0.00000   0.00000   0.00000  -0.00000
  0-1A  ->  4-1A   10.180358   82110.1   121.8   0.000000000   0.00000  -0.00000  -0.00000  -0.00000
  0-1A  ->  5-1A   10.187869   82170.7   121.7   0.000000000   0.00000  -0.00000   0.00000   0.00000
  0-1A  ->  6-1A   10.995304   88683.1   112.8   0.000000000   0.00000   0.00000  -0.00000  -0.00000
  0-1A  ->  7-1A   12.188654   98308.1   101.7   0.000000000   0.00000  -0.00000  -0.00000  -0.00000
  0-1A  ->  8-1A   12.543751  101172.2    98.8   0.000000000   0.00000  -0.00000  -0.00000  -0.00000
...
------------------------------------------------------------------------------------------
                     CD SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS
------------------------------------------------------------------------------------------
     Transition      Energy     Energy  Wavelength    R        MX        MY        MZ
                      (eV)      (cm-1)    (nm)   (1e40*cgs)   (au)      (au)      (au)
------------------------------------------------------------------------------------------
  0-1A  ->  1-1A    9.123912   73589.3   135.9   -0.00000   0.00000   0.00000   0.00000
  0-1A  ->  2-1A    9.483952   76493.2   130.7   -0.00000  -0.00000   0.00000  -0.00000
  0-1A  ->  3-1A    9.564384   77142.0   129.6   -0.00000   0.69943   0.00000   0.00000
  0-1A  ->  4-1A   10.180358   82110.1   121.8   -0.00000  -0.15776   0.00000   0.00000
  0-1A  ->  5-1A   10.187869   82170.7   121.7   -0.00000   0.00000   0.73302  -0.00000
  0-1A  ->  6-1A   10.995304   88683.1   112.8    0.00000  -0.00000   0.54037   0.00000
  0-1A  ->  7-1A   12.188654   98308.1   101.7    0.00000  -0.00000   0.00000   0.00000
  0-1A  ->  8-1A   12.543751  101172.2    98.8   -0.00000  -0.00000   0.00000  -0.90854
```

(sec:spectroscopyproperties.excitedstates.mcrpa.ccapabilities)=
### Capabilities

At the moment, we can simulate UV/Vis and ECD absorption spectra by
computing excitation energies, oscillator and rotatory strengths 
(check section {ref}`sec:spectroscopyproperties.ops` for more information).
The code is parallelized and the computational bottleneck is the integral
direct AO-Fock matrix construction. All intermediates that depend on the
number of states are stored on disk, which makes the MC-RPA
implementation suitable for computing many low-lying electronic states
of larger molecules. Abelian point-group symmetry can be exploited in
the calculation (up to D$_{\textrm{2h} }$). But there are no
calculations of spin-flip excitations possible at the moment. That means
all excited states will have the same spin as the reference state, which
is specified in the `%casscf` input block.

It is also possible to analyze and visualize the ground-to-excited-state
transitions by means of natural transition orbitals{cite}`Martin2003` (NTO),
which is explained in more detail in section
{ref}`sec:spectroscopyproperties.excitedstates.mcrpa`.

For further details, please study our recent
publications{cite}`Helmich-Paris2019a,Helmich-Paris2019b`.

```{index} ADC2
```

(sec:spectroscopyproperties.excitedstates.ADC2)=
## Excited States with ADC2

Among the various approximate correlation methods available for excited
states, one of the most popular one is algebraic diagrammatic
construction(ADC) method. The ADC has it origin in the Green's function
theory. It expands the energy and wave-function in perturbation order
and can directly calculate the excitation energy, ionization potential
and electron affinity, similar to that in the EOM-CCSD method. Because
of the symmetric eigenvalue problem in ADC, the calculation of
properties are more straight forward to calculate than EOM-CCSD. In
ORCA, only the second-order approximation to ADC(ADC2) is implemented.
It scales as O($N^{5}$) power of the basis set.

(sec:spectroscopyproperties.excitedstates.ADC2.general)=
### General Use

The simplest way to perform an ADC2 calculation is via the usage of the
`ADC2` keyword, together with the specification of the desired number of
roots:

```orcainput
! ADC2 cc-pVDZ cc-pVDZ/C TightSCF

%mdci
  nroots 9
end

*xyz 0 1
  C     0.016227   -0.000000    0.000000
  O     1.236847    0.000000   -0.000000
  H    -0.576537    0.951580   -0.000000
  H    -0.576537   -0.951580   -0.000000
*
```

The above input will call the ADC2 routine with default settings. The
main output is a list of excitation energies, augmented with some
further state specific data. The integral transformation in the ADC2
implementation of ORCA is done using the density-fitting approximation.
Therefore, one need to specify an auxiliary basis. For the above input,
the following output is obtained:

```orca
----------------------
ADC(2) RESULTS (RHS)
----------------------

IROOT=  1:  0.146914 au     3.998 eV   32243.8 cm**-1
  Amplitude    Excitation
  -0.116970     4 ->   8   
   0.672069     7 ->   8   
IROOT=  2:  0.286012 au     7.783 eV   62772.3 cm**-1
  Amplitude    Excitation
  -0.659777     7 ->   9   
IROOT=  3:  0.341919 au     9.304 eV   75042.5 cm**-1
  Amplitude    Excitation
  -0.676913     5 ->   8   
IROOT=  4:  0.352206 au     9.584 eV   77300.2 cm**-1
  Amplitude    Excitation
   0.126824     4 ->  10  
   0.360690     6 ->   8   
  -0.547670     7 ->  10  
IROOT=  5:  0.393965 au    10.720 eV   86465.3 cm**-1
  Amplitude    Excitation
   0.551345     6 ->   8   
   0.363450     7 ->  10  
  -0.109270     6 ->   8     6 ->   8   
IROOT=  6:  0.404946 au    11.019 eV   88875.4 cm**-1
  Amplitude    Excitation
   0.669682     4 ->   8   
   0.126557     7 ->   8   
IROOT=  7:  0.412800 au    11.233 eV   90599.2 cm**-1
  Amplitude    Excitation
  -0.100274     4 ->  11  
   0.671884     7 ->  11  
IROOT=  8:  0.439251 au    11.953 eV   96404.5 cm**-1
  Amplitude    Excitation
  -0.674114     6 ->   9   
   0.104541     6 ->   9     6 ->   8   
IROOT=  9:  0.486582 au    13.241 eV  106792.5 cm**-1
  Amplitude    Excitation
  -0.654624     5 ->   9   
```

The transition moment for ADC2 in ORCA is calculated using an EOM-like
expectation value approach, unlike the traditionally used intermediate
state representation. However, the two approaches gives almost identical
result.

```orca
--------------------------------------------------------------------
                    SPECTRUM FOR LEFT-RIGHT TRANSITION MOMENTS
--------------------------------------------------------------------


----------------------------------------------------------------------------------------------------
                     ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS
----------------------------------------------------------------------------------------------------
     Transition      Energy     Energy  Wavelength fosc(D2)      D2        DX        DY        DZ
                      (eV)      (cm-1)    (nm)                 (au**2)    (au)      (au)      (au)
----------------------------------------------------------------------------------------------------
  0-1A  ->  1-1A    3.997726   32243.8   310.1   0.000000000   0.00000   0.00000   0.00000   0.00000
  0-1A  ->  2-1A    7.782776   62772.3   159.3   0.096710371   0.50720  -0.00000  -0.70536   0.00000
  0-1A  ->  3-1A    9.304078   75042.5   133.3   0.002261744   0.00992  -0.00000   0.00000  -0.09835
  0-1A  ->  4-1A    9.584003   77300.2   129.4   0.007937829   0.03381  -0.18502  -0.00000  -0.00000
  0-1A  ->  5-1A   10.720332   86465.3   115.7   0.465055079   1.77067   1.32377   0.00000  -0.00000
  0-1A  ->  6-1A   11.019150   88875.4   112.5   0.000000000   0.00000  -0.00000   0.00000  -0.00000
  0-1A  ->  7-1A   11.232869   90599.2   110.4   0.022236623   0.08080   0.00000  -0.28105  -0.00000
  0-1A  ->  8-1A   11.952640   96404.5   103.7   0.009103120   0.03109   0.00000  -0.00000   0.17328
  0-1A  ->  9-1A   13.240575  106792.5    93.6   0.071433742   0.22021  -0.46692  -0.00000   0.00000
```

The IP and EA versions can be called using the keywords IP-ADC2 and
EA-ADC2, respectively.

(sec:spectroscopyproperties.excitedstates.ADC2.capabilities)=
### Capabilities

At present, the ADC2 module is able to perform excited, ionized and
electron attached state calculations, only for closed-shell systems. No
open-shell version of the ADC2 is currently available. Below are all the
parameters that influence the ADC2 module.

```orca
%mdci
#ADC2 parameters - defaults displayed
  NDav 20              # maximum size of reduced space (i.e. 20*NRoots)
  CheckEachRoot true   # check convergence for each root separately
  RootHoming true      # apply root homing
  DoLanczos false      # use the Lanczos procedure rather than Davidson
  UseCISUpdate true    # use diagonal CIS for updating
  NInitS 0             # number of roots in the initial guess, if 0,
                       # use preset value
  DoRootwise false     # solves for each root separately,
                       # more stable for large number of roots
  FOLLOWCIS false      # follows the initial singles guess                      
end
```

One can notice that features available in the ADC2 module is quite
limited as compared to the EOM module and the option to specifically
target the core-orbitals are yet not available. A word of caution, **The
'second order black magic' of ADC2 can fail in many of the cases.** The
readers are encouraged to try the DLPNO based EOM-CCSD
methods({ref}`sec:spectroscopyproperties.excitedstates.dlpnoeom`) which are much more accurate and
computationally efficient.

```{index} STEOM-CCSD
```

(sec:spectroscopyproperties.excitedstates.steom)=
## Excited States with STEOM-CCSD

The STEOM-CCSD method provides an efficient way to calculate excitation
energies, with an accuracy comparable to the EOM-CCSD approach, at a
nominal cost. A detailed description will be given in Section
{ref}`sec:spectroscopyproperties.steom`.

(sec:spectroscopyproperties.excitedstates.steom.general)=
### General Use

The simplest way to perform a STEOM calculation is using the
`STEOM-CCSD` keyword, together with the specification of the desired
number of roots (`NRoots`):

```orca
! STEOM-CCSD cc-pVDZ TightSCF

%mdci
  NRoots 9        # Number of excited states 
  DoDbfilter true # Remove doubly excited states
end

*xyz 0 1
  C     0.016227   -0.000000    0.000000
  O     1.236847    0.000000   -0.000000
  H    -0.576537    0.951580   -0.000000
  H    -0.576537   -0.951580   -0.000000
*
```

<!-- >```{literalinclude} ../../orca_working_input/C05S08_163.inp
:language: orca
``` -->

The above input calls the STEOM routine with default settings, where,
for instance, the doubly excited states are eliminated
(`DoDbFilter true`). The main output is a list of excitation energies,
augmented with some further state specific data. The STEOMCC approach in
ORCA uses state-averaged CIS natural transition orbitals (NTO) for the
selection of the active space. For the above input, the following output
is obtained:

```orca
-------------------------------
STEOM-CCSD RESULTS (SINGLETS)
-------------------------------

IROOT=  1:  0.145378 au     3.956 eV   31906.7 cm**-1
  Amplitude    Excitation
  -0.168322     4 ->   8
  -0.984801     7 ->   8
  Ground state amplitude: -0.000000

Percentage Active Character     99.91

  Amplitude    Excitation in Canonical Basis
  -0.166144     4 ->   8
  -0.975626     7 ->   8
   0.123172     7 ->  13

IROOT=  2:  0.309944 au     8.434 eV   68024.9 cm**-1
  Amplitude    Excitation
  -0.993139     7 ->   9
  Ground state amplitude:  0.000000

Percentage Active Character     99.94

  Amplitude    Excitation in Canonical Basis
  -0.989653     7 ->   9

IROOT=  3:  0.337588 au     9.186 eV   74092.0 cm**-1
  Amplitude    Excitation
  -0.993709     5 ->   8
  Ground state amplitude: -0.000002

Percentage Active Character     99.23

  Amplitude    Excitation in Canonical Basis
  -0.984171     5 ->   8
   0.136295     5 ->  13

IROOT=  4:  0.357393 au     9.725 eV   78438.7 cm**-1
  Amplitude    Excitation
  -0.186839     4 ->  10
  -0.755864     6 ->   8
  -0.601549     7 ->  10
  -0.112921     7 ->  12
  Ground state amplitude:  0.026385

Percentage Active Character     99.71

  Amplitude    Excitation in Canonical Basis
  -0.182608     4 ->  10
  -0.752095     6 ->   8
  -0.598472     7 ->  10

IROOT=  5:  0.386751 au    10.524 eV   84882.0 cm**-1
  Amplitude    Excitation
  -0.980511     4 ->   8
   0.178900     7 ->   8
  Ground state amplitude:  0.000000

Percentage Active Character     99.90

  Amplitude    Excitation in Canonical Basis
  -0.971593     4 ->   8
   0.121664     4 ->  13
   0.179278     7 ->   8

IROOT=  6:  0.406225 au    11.054 eV   89156.2 cm**-1
  Amplitude    Excitation
   0.532674     6 ->   8
  -0.825021     7 ->  10
  Ground state amplitude: -0.065794

Percentage Active Character     99.70

  Amplitude    Excitation in Canonical Basis
   0.526200     6 ->   8
  -0.817279     7 ->  10

IROOT=  7:  0.421236 au    11.462 eV   92450.6 cm**-1
  Amplitude    Excitation
  -0.125749     4 ->  11
  -0.985406     7 ->  11
  Ground state amplitude:  0.000000

Percentage Active Character     99.85

  Amplitude    Excitation in Canonical Basis
   0.124222     4 ->  11
   0.983485     7 ->  11

IROOT=  8:  0.443588 au    12.071 eV   97356.3 cm**-1
  Amplitude    Excitation
   0.106457     3 ->   8
   0.992884     6 ->   9
  Ground state amplitude:  0.000092

Percentage Active Character     99.78

  Amplitude    Excitation in Canonical Basis
   0.106009     3 ->   8
   0.987228     6 ->   9

IROOT=  9:  0.512311 au    13.941 eV  112439.3 cm**-1
  Amplitude    Excitation
  -0.995561     6 ->  10
  Ground state amplitude: -0.000001

Percentage Active Character     99.94

  Amplitude    Excitation in Canonical Basis
  -0.985669     6 ->  10
   0.157781     6 ->  15
```

The first set of excitation amplitudes, printed for each root, have been
calculated in the CIS NTO (Natural Transition Orbitals) basis. The
second set of amplitudes have been evaluated in the RHF canonical basis.

(sec:spectroscopyproperties.excitedstates.steom.capabilities)=
### Capabilities

At present, the STEOM routine is able to calculate excitation energies,
for both closed- or open-shell systems, using an RHF or UHF reference
function, respectively. It can be used for both serial and parallel
calculations. The method is available in the back-tranformed PNO and
DLPNO framework allowing the calculation of large molecules (Section
{ref}`sec:spectroscopyproperties.excitedstates.dleom.capabilities` and
{ref}`sec:spectroscopyproperties.excitedstates.dlpnoeom`). In the closed-shell case (RHF), a
lower scaling version can be invoked by setting the `CCSD2` keyword to
true in the %mdci section, which sets a second order approximation to
the exact parent approach. The transition moments can also be obtained
for closed- and open-shell systems. For more details see Section
{ref}`sec:spectroscopyproperties.steom`.

```{index} IH-FSMR-CCSD
```
(sec:spectroscopyproperties.excitedstates.ihfsmr)=
## Excited States with IH-FSMR-CCSD

The intermediate Hamiltonian Fock-space coupled cluster method
(IH-FSMR-CCSD) provides an alternate way to calculate excitation
energies, with an accuracy comparable to the STEOM-CCSD approach. A
detailed description is given in Section
{ref}`sec:spectroscopyproperties.ihfsmrcc`.

(sec:spectroscopyproperties.excitedstates.ihfsmr.general)=
### General Use

The IH-FSMR-CCSD calculation is called using the simple input keyword
`IH-FSMR-CCSD` and specifying the desired number of excited states
(`NRoots`) in the %mdci block.:

```orca
! IH-FSMR-CCSD cc-pVDZ TightSCF
  
%mdci
  nroots 6
end

*xyz 0 1
  C     0.016227   -0.000000    0.000000
  O     1.236847    0.000000   -0.000000
  H    -0.576537    0.951580   -0.000000
  H    -0.576537   -0.951580   -0.000000
*
```

<!-- >```{literalinclude} ../../orca_working_input/ihfsmrcc.inp
:language: orca
``` -->

The above input will call the IH-FSMR-CCSD routine with default
settings. The main output is a list of excitation energies, augmented
with some further state specific data. The IH-FSMR-CCSD approach in ORCA
uses state-averaged CIS natural transition orbitals(NTO) for the
selection of the active space - similar to STEOM-CCSD. For the above
input, the following output is obtained:

```orca
-------------------------------
IH-FSMR-CCSD RESULTS (SINGLETS) 
-------------------------------

IROOT=  1:  0.144808 au     3.940 eV   31781.8 cm**-1
  Amplitude    Excitation
  -0.171178     4 ->   8   
  -0.984024     7 ->   8   
  Ground state amplitude:  0.000000

Percentage Active Character     99.96

  Amplitude    Excitation in Canonical Basis
  -0.169804     4 ->   8   
  -0.976596     7 ->   8   
   0.111105     7 ->  13  

IROOT=  2:  0.309569 au     8.424 eV   67942.6 cm**-1
  Amplitude    Excitation
  -0.994029     7 ->   9   
  Ground state amplitude:  0.000000

Percentage Active Character     99.79

  Amplitude    Excitation in Canonical Basis
  -0.991036     7 ->   9   

IROOT=  3:  0.337609 au     9.187 eV   74096.7 cm**-1
  Amplitude    Excitation
   0.992246     5 ->   8   
  Ground state amplitude:  0.000000

Percentage Active Character     99.29

  Amplitude    Excitation in Canonical Basis
   0.985970     5 ->   8   
  -0.120519     5 ->  13  

IROOT=  4:  0.354726 au     9.653 eV   77853.3 cm**-1
  Amplitude    Excitation
  -0.167422     4 ->  10  
   0.125754     5 ->  11  
  -0.748485     6 ->   8   
  -0.575997     7 ->  10  
  -0.204999     7 ->  14  
  Ground state amplitude:  0.000000

Percentage Active Character     94.11

Warning:: the state may have not converged with respect to active space 
-------------------- Handle with Care -------------------- 

  Amplitude    Excitation in Canonical Basis
  -0.175024     4 ->  10  
   0.110821     5 ->  11  
  -0.745514     6 ->   8   
  -0.609903     7 ->  10  

IROOT=  5:  0.386134 au    10.507 eV   84746.6 cm**-1
  Amplitude    Excitation
  -0.980436     4 ->   8   
   0.180972     7 ->   8   
  Ground state amplitude:  0.000000

Percentage Active Character     99.91

  Amplitude    Excitation in Canonical Basis
  -0.972869     4 ->   8
   0.111877     4 ->  13
   0.180279     7 ->   8

IROOT=  6:  0.443256 au    12.062 eV   97283.4 cm**-1
  Amplitude    Excitation
  -0.110780     3 ->   8
  -0.991903     6 ->   9
  Ground state amplitude:  0.000000

Percentage Active Character     99.71

  Amplitude    Excitation in Canonical Basis
  -0.109728     3 ->   8
  -0.988030     6 ->   9
```

The first set of excitation amplitudes, printed for each root, have been
calculated in the CIS NTO (Natural Transition Orbitals) basis. The
second set of amplitudes have been evaluated in the RHF canonical basis.

(sec:spectroscopyproperties.excitedstates.ihfsmr.capabilities)=
### Capabilities

At present, the IH-FSMR-CCSD routine is able to calculate excitation
energies, for only closed shell systems using an RHF reference. It can
be used for both serial and parallel calculations. In the closed-shell
case (RHF), a lower scaling version can be invoked by using bt-PNO
approximation. The transition moments and solvation correction can be
obtained using the CIS approximation.

```{index} PNO-CC
```
(sec:spectroscopyproperties.excitedstates.dleom)=
## Excited States with PNO based coupled cluster methods

The methods described in the previous section are performed over a
canonical CCSD or MP2 ground state. The use of canonical CCSD amplitudes
restricts the use of EOM-CC and STEOM-CC methods to small molecules. The
use of MP2 amplitudes is possible (e.g. the EOM-CCSD(2) or STEOM-CCSD(2)
approaches), but it seriously compromises the accuracy of the method.

The bt-PNO-EOM-CCSD methods gives an economical compromise between
accuracy and computational cost by replacing the most expensive ground
state CCSD calculation with a DLPNO based CCSD calculation. The typical
deviation of the results from the canonical EOM-CCSD results is around
0.01 eV. A detailed description will be given in
{ref}`sec:spectroscopyproperties.dleom`.

(sec:spectroscopyproperties.excitedstates.dleom.general)=
### General Use

The simplest way to perform a PNO based EOM calculation is via the usage
of the bt-PNO-EOM-CCSD keyword, together with the specification of the
desired number of roots. The specification of an auxilary basis set is
also required, just as for ground state DLPNO-CCSD calculations.

```orca
! bt-PNO-EOM-CCSD def2-TZVP def2-TZVP/C def2/J TightSCF

%mdci
  nroots 9
end

*xyz 0 1
  C     0.016227   -0.000000    0.000000
  O     1.236847    0.000000   -0.000000
  H    -0.576537    0.951580   -0.000000
  H    -0.576537   -0.951580   -0.000000
*
```

<!-- >```{literalinclude} ../../orca_working_input/C05S09_164.inp
:language: orca
``` -->

The output is similar to that from a canonical EOM-CCSD calculation:

```orca
----------------------
EOM-CCSD RESULTS (RHS)
----------------------

IROOT=  1:  0.145420 au     3.957 eV   31915.9 cm**-1
  Amplitude    Excitation
   0.650351     7 ->   8   
  -0.162540     7 ->  13  
  Ground state amplitude:  0.000000
Percentage singles character=     92.33

IROOT=  2:  0.311168 au     8.467 eV   68293.4 cm**-1
  Amplitude    Excitation
   0.650800     7 ->   9   
  -0.155532     7 ->  11  
  Ground state amplitude: -0.000000
Percentage singles character=     90.95

IROOT=  3:  0.337404 au     9.181 eV   74051.7 cm**-1
  Amplitude    Excitation
   0.652018     5 ->   8   
  -0.169980     5 ->  13  
  Ground state amplitude:  0.000000
Percentage singles character=     91.87

IROOT=  4:  0.348225 au     9.476 eV   76426.6 cm**-1
  Amplitude    Excitation
   0.152132     7 ->   9   
   0.652819     7 ->  11  
  Ground state amplitude:  0.000000
Percentage singles character=     92.35

IROOT=  5:  0.354668 au     9.651 eV   77840.6 cm**-1
  Amplitude    Excitation
   0.545649     6 ->   8   
  -0.339835     7 ->  10  
   0.170720     6 ->   8     6 ->   8   
  Ground state amplitude:  0.032711
Percentage singles character=     87.10

IROOT=  6:  0.379606 au    10.330 eV   83313.9 cm**-1
  Amplitude    Excitation
   0.636153     4 ->   8   
  -0.160301     4 ->  13  
  -0.109552     7 ->   8   
   0.143497     7 ->   8     6 ->   8   
  Ground state amplitude:  0.000000
Percentage singles character=     88.55

IROOT=  7:  0.386807 au    10.526 eV   84894.3 cm**-1
  Amplitude    Excitation
   0.257812     6 ->   8   
   0.584151     7 ->  10  
   0.181783     7 ->  14  
  Ground state amplitude:  0.038804
Percentage singles character=     90.30

IROOT=  8:  0.440552 au    11.988 eV   96690.1 cm**-1
  Amplitude    Excitation
  -0.655574     6 ->   9   
  -0.104097     6 ->  16  
  -0.112700     6 ->   9     6 ->   8   
  Ground state amplitude:  0.000000
Percentage singles character=     87.92

IROOT=  9:  0.447219 au    12.169 eV   98153.2 cm**-1
  Amplitude    Excitation
   0.162756     7 ->   8
   0.651078     7 ->  13
  Ground state amplitude:  0.000000
Percentage singles character=     90.36
```

The IP and EA versions can be called by using the keywords
bt-PNO-IP-EOM-CCSD and bt-PNO-EA-EOM-CCSD, respectively. Furthermore,
the STEOM version can be invoked by using the keywords
bt-PNO-STEOM-CCSD.

(sec:spectroscopyproperties.excitedstates.dleom.capabilities)=
### Capabilities

All of the features of canonical EOM-CC and STEOM-CC are available in
the PNO based approaches for both closed- and open-shell systems.

```{index} DLPNO-EOM-CC
```
(sec:spectroscopyproperties.excitedstates.dlpnoeom)=
## Excited States with DLPNO based coupled cluster methods

The DLPNO-STEOM-CCSD method uses the full potential of DLPNO to reduce
the computational scaling while keeping the accuracy of STEOM-CCSD.

:::{important}
-   DLPNO-STEOM-CCSD is currently only available for closed-shell systems!
:::

(sec:spectroscopyproperties.excitedstates.dlpnoeom.general)=
### General Use

The simplest way to perform a DLPNO based STEOM calculation is via the
usage of the `STEOM-DLPNO-CCSD` keyword, together with the specification
of the desired number of roots. The specification of an auxiliary basis
set is also required, just as for ground state DLPNO-CCSD calculations.

As any CCSD methods, it is important to allow ORCA to access a
significant amount of memory. In terms of scaling the limiting factor of
the method is the size of temporary files and thus the disk space. For
molecules above 1500 basis functions it starts to increase exponentially
up to several teraoctets.

Here is the standard input we would recommend for STEOM-DLPNO-CCSD
calculations. More information on the different keywords and other
capabilities are available in the detailed part of the manual
{ref}`sec:spectroscopyproperties.steom`,
{ref}`sec:spectroscopyproperties.dlpno-steom`. The following publications
referenced some applications for this method either in organic molecules
{cite}`Berraud-Pache2020`, {cite}`Sirohiwal2020` or for Semiconductors
{cite}`Dittmer2019`.

```orca
! STEOM-DLPNO-CCSD def2-TZVP def2-TZVP/C def2/J TightSCF

%mdci
  NRoots 6
  DoRootWise true
  OThresh 0.005
  VThresh 0.005
  TCutPNOSingles 1e-11
  NDAV 400
  DoStoreSTEOM true
  DoSimpleDens false
  AddL2Term True
  DTol 1e-5
end

* xyz 0 1
  C     0.016227   -0.000000    0.000000
  O     1.236847    0.000000   -0.000000
  H    -0.576537    0.951580   -0.000000
  H    -0.576537   -0.951580   -0.000000
*
```

<!-- >```{literalinclude} ../../orca_working_input/C05S09_165.inp
:language: orca
``` -->

The output is similar to that from a canonical DLPNO-STEOM-CCSD
calculation:

```orca
-------------------------------
STEOM-CCSD RESULTS (SINGLETS) 
-------------------------------

IROOT=  1:  0.144275 au     3.926 eV   31664.7 cm**-1
  Amplitude    Excitation
  -0.142146     4 ->   8   
  -0.988793     7 ->   8   
  Ground state amplitude:  0.000000

Percentage Active Character     99.79

  Amplitude    Excitation in Canonical Basis
  -0.134936     4 ->   8   
  -0.955031     7 ->   8   
   0.236743     7 ->  13  

IROOT=  2:  0.308093 au     8.384 eV   67618.5 cm**-1
  Amplitude    Excitation
   0.971471     7 ->   9   
   0.214898     7 ->  10  
  Ground state amplitude: -0.000000

Percentage Active Character     99.67

  Amplitude    Excitation in Canonical Basis
   0.956929     7 ->   9   
  -0.236568     7 ->  11  
   0.102573     7 ->  16  

IROOT=  3:  0.331790 au     9.028 eV   72819.4 cm**-1
  Amplitude    Excitation
   0.993677     5 ->   8   
  Ground state amplitude: -0.000000

Percentage Active Character     98.87

  Amplitude    Excitation in Canonical Basis
   0.957221     5 ->   8   
  -0.250140     5 ->  13
  -0.105951     5 ->  18

IROOT=  4:  0.346876 au     9.439 eV   76130.4 cm**-1
  Amplitude    Excitation
  -0.104901     4 ->  10
   0.198176     7 ->   9
  -0.972572     7 ->  10
  Ground state amplitude: -0.000000

Percentage Active Character     99.65

  Amplitude    Excitation in Canonical Basis
   0.100880     4 ->  11
   0.218873     7 ->   9
   0.956923     7 ->  11
  -0.113897     7 ->  19

IROOT=  5:  0.347460 au     9.455 eV   76258.7 cm**-1
  Amplitude    Excitation
   0.139551     4 ->  11
   0.106649     4 ->  12
  -0.801186     6 ->   8
   0.455613     7 ->  11
   0.302458     7 ->  12
  Ground state amplitude:  0.027275

  Percentage Active Character     87.08

Warning:: the state may have not converged with respect to active space
-------------------- Handle with Care --------------------

  Amplitude    Excitation in Canonical Basis
   0.163791     4 ->  10
  -0.785701     6 ->   8
   0.159149     6 ->  13
   0.527833     7 ->  10
  -0.133085     7 ->  17

IROOT=  6:  0.379059 au    10.315 eV   83193.9 cm**-1
  Amplitude    Excitation
  -0.983700     4 ->   8
   0.155239     7 ->   8
  Ground state amplitude:  0.000000

Percentage Active Character     99.48

  Amplitude    Excitation in Canonical Basis
  -0.951092     4 ->   8
   0.235046     4 ->  13
   0.157714     7 ->   8
```

The IP and EA versions can be called by using the keywords
IP-EOM-DLPNO-CCSD and EA-EOM-DLPNO-CCSD, respectively. As in canonical
STEOM-CCSD, the first set of excitation amplitudes, printed for each
root, are calculated in the CIS NTO (Natural Transition Orbitals) basis,
while the second set is evaluated in the RHF canonical basis.
