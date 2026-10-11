<a id="sec:structurereactivity.thermochemistry"></a>
# Thermochemistry

The second thing that you get automatically as the result of a frequency
calculation is a thermochemical analysis based on ideal gas statistical
mechanics. This can be used to study heats of formation, dissociation
energies and similar thermochemical properties. To correct for the
breakdown of the harmonic oscillator approximation for low frequencies,
entropic contributions to the free energies are computed, by default,
using the Quasi-RRHO approach of Grimme.[grimme2012chemeurj](../../bibliography.md) To
switch-off the Quasi-RRHO method and use the RRHO method, use:

```orca
%freq  QuasiRRHO false
       CutOffFreq 35 # in cm-1
       end
```

Where the CutOffFreq parameter controls the cut-off for the low
frequencies mode (excluded from the calculation of the thermochemical
properties). Note that the default CutOffFreq is 1 (cm$^{-1}$) when
Quasi-RRHO is on, since Quasi-RRHO behaves much more reasonably for
low frequencies than RRHO does. In particular, the entropy contribution
calculated by Quasi-RRHO approaches a constant value when the vibrational
frequency approaches zero, while the RRHO contribution diverges.

The Quasi-RRHO method smoothly interpolates between the entropy formulas
of a harmonic oscillator and a rigid rotor, such that high frequency
vibrations behave like harmonic vibrations, and low frequency vibrations
behave like rotations with the same frequency. The frequency at which
the entropy contribution is a half-half mixture of rotation and vibration
is called the \"reference frequency\" $\omega_0$ of the Quasi-RRHO method, accessible
via the `QRRHORefFreq` keyword in `%freq` (see [structurereactivity.frequencies](frequencies.md#sec:structurereactivity.frequencies)).
The default value (100 cm$^{-1}$) is consistent with the original Quasi-RRHO
paper[grimme2012chemeurj](../../bibliography.md), but other papers may choose different
values, such as 50 cm$^{-1}$. Meanwhile, ORCA's Quasi-RRHO implementation
deviates from the original paper in the choice of \"average molecular
moment of inertia\" $B_{\rm{av}}$; while in the original paper it is
chosen as a fixed value $10^{-44} \rm{kg}\cdot\rm{m}^2$, in ORCA it is
given as the isotropically averaged moment of inertia of the actual
molecule at hand. This is theoretically more justified than using the
same moment of inertia for molecules of different sizes, although the
resulting difference in the Gibbs free energies is rather small, usually
within 0.1 kcal/mol.

Note that the rotational contribution to the entropy is calculated using
the expressions given by Herzberg [Herzberg1945](../../bibliography.md) including the symmetry
number obtained from the order of the point group.[^1] While this is a
good approximation, one might want to modify the symmetry number or use
a different expression [Gilson2010](../../bibliography.md). For this purpose, the rotational
constants (in cm$^{-1}$) of the molecule are also given in the
thermochemistry output.

For example let us calculate a number for the oxygen-oxygen dissociation
energy in the H$_{2}$O$_{2}$ molecule. First run the following jobs:

```mol
title: structure 1
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
4
structure (0 1)
O     -1.396288    -0.075107     0.052125
O      1.396289    -0.016261    -0.089970
H     -1.775703     1.309756    -1.111179
H      1.775687     0.140443     1.711854
--- input ---
# Calculate a value for the O-O bond strength in H2O2
! B3LYP DEF2-TZVP OPT FREQ BOHRS

* xyz 0 1
 O          -1.396288    -0.075107     0.052125
 O           1.396289    -0.016261    -0.089970
 H          -1.775703     1.309756    -1.111179
 H           1.775687     0.140443     1.711854
*
```

```mol
title: structure 2
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
2
structure (0 2)
O     -1.396288    -0.075107     0.052125
H     -1.775703     1.309756    -1.111179
--- input ---
# Now the OH radical job
! B3LYP DEF2-TZVP OPT FREQ BOHRS

* xyz 0 2
 O          -1.396288    -0.075107     0.052125
 H          -1.775703     1.309756    -1.111179
*
```

The first job gives you the following output following the frequency
calculation:

```orca
--------------------------
THERMOCHEMISTRY AT 298.15K
--------------------------

Temperature         ... 298.15 K
Pressure            ... 1.00 atm
Total Mass          ... 34.01 AMU

Throughout the following assumptions are being made:
  (1) The electronic state is orbitally nondegenerate
  (2) There are no thermally accessible electronically excited states
  (3) Hindered rotations indicated by low frequency modes are not
      treated as such but are treated as vibrations and this may
      cause some error
  (4) All equations used are the standard statistical mechanics
      equations for an ideal gas
  (5) All vibrations are strictly harmonic

freq.     370.67  E(vib)   ...       0.21 
freq.     947.27  E(vib)   ...       0.03 
freq.    1313.46  E(vib)   ...       0.01 
freq.    1440.24  E(vib)   ...       0.00 
freq.    3739.49  E(vib)   ...       0.00 
freq.    3739.86  E(vib)   ...       0.00 

------------
INNER ENERGY
------------

The inner energy is: U= E(el) + E(ZPE) + E(vib) + E(rot) + E(trans)
  E(el)   - is the total energy from the electronic structure calculation
            = E(kin-el) + E(nuc-el) + E(el-el) + E(nuc-nuc)
  E(ZPE)  - the zero temperature vibrational energy from the frequency calculation
  E(vib)  - the finite temperature correction to E(ZPE) due to population
            of excited vibrational states
  E(rot)  - is the rotational thermal energy
  E(trans)- is the translational thermal energy

Summary of contributions to the inner energy U:
Electronic energy                ...   -151.55083691 Eh
Zero point energy                ...      0.02631509 Eh      16.51 kcal/mol
Thermal vibrational correction   ...      0.00040105 Eh       0.25 kcal/mol
Thermal rotational correction    ...      0.00141627 Eh       0.89 kcal/mol
Thermal translational correction ...      0.00141627 Eh       0.89 kcal/mol
-----------------------------------------------------------------------
Total thermal energy                   -151.52128823 Eh

Summary of corrections to the electronic energy:
(perhaps to be used in another calculation)
Total thermal correction                  0.00323359 Eh       2.03 kcal/mol
Non-thermal (ZPE) correction              0.02631509 Eh      16.51 kcal/mol
-----------------------------------------------------------------------
Total correction                          0.02954868 Eh      18.54 kcal/mol

--------
ENTHALPY
--------

The enthalpy is H = U + kB*T
                kB is Boltzmann's constant
Total free energy                 ...   -151.52129054 Eh
Thermal Enthalpy correction       ...      0.00094421 Eh       0.59 kcal/mol
-----------------------------------------------------------------------
Total Enthalpy                    ...   -151.52034633 Eh

Note: Rotational entropy computed according to Herzberg
Infrared and Raman Spectra, Chapter V,1, Van Nostrand Reinhold, 1945
Point Group:  C2, Symmetry Number:   2
Rotational constants in cm-1:    10.087644     0.882994     0.851333

Vibrational entropy computed according to the QRRHO of S. Grimme
Chem.Eur.J. 2012 18 9955

-------
ENTROPY
-------

The entropy contributions are T*S = T*(S(el)+S(vib)+S(rot)+S(trans))
     S(el)   - electronic entropy
     S(vib)  - vibrational entropy
     S(rot)  - rotational entropy
     S(trans)- translational entropy
The entropies will be listed as multiplied by the temperature to get
units of energy

Electronic entropy                ...      0.00000000 Eh      0.00 kcal/mol
Vibrational entropy               ...      0.00059250 Eh      0.37 kcal/mol
Rotational entropy                ...      0.00789993 Eh      4.96 kcal/mol
Translational entropy             ...      0.01734394 Eh     10.88 kcal/mol
-----------------------------------------------------------------------
Final entropy term                ...      0.02583637 Eh     16.21 kcal/mol

In case the symmetry of your molecule has not been determined correctly
or in case you have a reason to use a different symmetry number we print
out the resulting rotational entropy values for sn=1,12 :
 --------------------------------------------------------
|  sn= 1 | S(rot)=       0.00855439 Eh      5.37 kcal/mol|
|  sn= 2 | S(rot)=       0.00789993 Eh      4.96 kcal/mol|
|  sn= 3 | S(rot)=       0.00751710 Eh      4.72 kcal/mol|
|  sn= 4 | S(rot)=       0.00724548 Eh      4.55 kcal/mol|
|  sn= 5 | S(rot)=       0.00703479 Eh      4.41 kcal/mol|
|  sn= 6 | S(rot)=       0.00686265 Eh      4.31 kcal/mol|
|  sn= 7 | S(rot)=       0.00671710 Eh      4.22 kcal/mol|
|  sn= 8 | S(rot)=       0.00659102 Eh      4.14 kcal/mol|
|  sn= 9 | S(rot)=       0.00647981 Eh      4.07 kcal/mol|
|  sn=10 | S(rot)=       0.00638033 Eh      4.00 kcal/mol|
|  sn=11 | S(rot)=       0.00629034 Eh      3.95 kcal/mol|
|  sn=12 | S(rot)=       0.00620819 Eh      3.90 kcal/mol|
 --------------------------------------------------------

-------------------
GIBBS FREE ENERGY
-------------------

The Gibbs free energy is G = H - T*S

Total enthalpy                    ...   -151.52034633 Eh
Total entropy correction          ...     -0.02583637 Eh    -16.21 kcal/mol
-----------------------------------------------------------------------
Final Gibbs free energy         ...   -151.54618270 Eh

For completeness - the Gibbs free energy minus the electronic energy
G-E(el)                           ...      0.00465413 Eh      2.92 kcal/mol
```

And similarly for the OH-radical job.

```orca
------------
INNER ENERGY
------------

The inner energy is: U= E(el) + E(ZPE) + E(vib) + E(rot) + E(trans)
 E(el)   - is the total energy from the electronic structure calculation
           = E(kin-el) + E(nuc-el) + E(el-el) + E(nuc-nuc)
 E(ZPE)  - the zero temperature vibrational energy from the frequency calculation
 E(vib)  - the finite temperature correction to E(ZPE) due to population
           of excited vibrational states
 E(rot)  - is the rotational thermal energy
 E(trans)- is the translational thermal energy

Summary of contributions to the inner energy U:
Electronic energy                ...    -75.73492538 Eh
Zero point energy                ...      0.00837287 Eh       5.25 kcal/mol
Thermal vibrational correction   ...      0.00000000 Eh       0.00 kcal/mol
Thermal rotational correction    ...      0.00094418 Eh       0.59 kcal/mol
Thermal translational correction ...      0.00141627 Eh       0.89 kcal/mol
-----------------------------------------------------------------------
Total thermal energy                    -75.72419205 Eh

Summary of corrections to the electronic energy:
(perhaps to be used in another calculation)
Total thermal correction                  0.00236045 Eh       1.48 kcal/mol
Non-thermal (ZPE) correction              0.00837287 Eh       5.25 kcal/mol
-----------------------------------------------------------------------
Total correction                          0.01073332 Eh       6.74 kcal/mol

--------
ENTHALPY
--------

The enthalpy is H = U + kB*T
                kB is Boltzmann's constant
Total free energy                 ...    -75.72419205 Eh
Thermal Enthalpy correction       ...      0.00094421 Eh       0.59 kcal/mol
-----------------------------------------------------------------------
Total Enthalpy                    ...    -75.72324785 Eh

Note: Rotational entropy computed according to Herzberg
Infrared and Raman Spectra, Chapter V,1, Van Nostrand Reinhold, 1945
Point Group:  C2v, Symmetry Number:   1
Rotational constants in cm-1:     0.000000    18.628159    18.628159

Vibrational entropy computed according to the QRRHO of S. Grimme
Chem.Eur.J. 2012 18 9955

-------
ENTROPY
-------

The entropy contributions are T*S = T*(S(el)+S(vib)+S(rot)+S(trans))
     S(el)   - electronic entropy
     S(vib)  - vibrational entropy
     S(rot)  - rotational entropy
     S(trans)- translational entropy
The entropies will be listed as multiplied by the temperature to get
units of energy

Note: Rotational entropy computed according to Herzberg
Infrared and Raman Spectra, Chapter V,1, Van Nostrand Reinhold, 1945
Point Group:  C2v, Symmetry Number:   1
Rotational constants in cm-1:     0.000000    18.628159    18.628159

Vibrational entropy computed according to the QRRHO of S. Grimme
Chem.Eur.J. 2012 18 9955

-------
ENTROPY
-------

The entropy contributions are T*S = T*(S(el)+S(vib)+S(rot)+S(trans))
     S(el)   - electronic entropy
     S(vib)  - vibrational entropy
     S(rot)  - rotational entropy
     S(trans)- translational entropy
The entropies will be listed as multiplied by the temperature to get
units of energy

Electronic entropy                ...      0.00065446 Eh      0.41 kcal/mol
Vibrational entropy               ...      0.00000000 Eh      0.00 kcal/mol
Rotational entropy                ...      0.00321884 Eh      2.02 kcal/mol
Translational entropy             ...      0.01636225 Eh     10.27 kcal/mol
-----------------------------------------------------------------------
Final entropy term                ...      0.02023555 Eh     12.70 kcal/mol

-------------------
GIBBS FREE ENERGY
-------------------

The Gibbs free energy is G = H - T*S

Total enthalpy                    ...    -75.72324785 Eh
Total entropy correction          ...     -0.02023555 Eh    -12.70 kcal/mol
-----------------------------------------------------------------------
Final Gibbs free energy         ...    -75.74348340 Eh

For completeness - the Gibbs free energy minus the electronic energy
G-E(el)                           ...     -0.00855802 Eh     -5.37 kcal/mol
```

Let us calculate the free energy change for the reaction: $H_2O_2 \rightarrow 2 OH$

The individual energy terms are: 

Electronic Energy: -151.46985 a.u. -(-151.55084) a.u. = 0.08099 a.u. (50.82 kcal/mol)

Zero-point Energy: 0.01675 a.u. - 0.02631 a.u. = -0.00956 a.u. (-6.00 kcal/mol)

Thermal Correction(translation/rotation):  0.00472 a.u. - 0.00283 a.u. = 0.00189 a.u. (1.19 kcal/mol) 

Thermal Enthalpy Correction: 0.00189 a.u. - 0.00094 a.u. = 0.00095 a.u. (0.60 kcal/mol)

Entropy: -0.04047 a.u. -(-0.02584) a.u. = -0.01463 a.u. (-9.18 kcal/mol)

Final $\Delta$G: 37.43 kcal/mol

Thus, both the zero-point energy and the entropy terms contribute
significantly to the total free energy change of the reaction. The
entropy term is favoring the reaction due to the emergence of new
translational and rotational degrees of freedom. The zero-point
correction is also favoring the reaction since the zero-point
vibrational energy of the O-O bond is lost. The thermal correction and
the enthalpy correction are both small.

!!! note

    -   You can run the thermochemistry calculations at several user defined
        temperatures and pressure by providing the program with a list of
        temperatures / pressures:

    ```orca
    %freq  Temp  290, 295, 300     # in Kelvin
            Pressure  1.0, 2.0, 3.0 # in atm
           end
    ```

    -   Once a Hessian is available you can rerun the thermochemistry
        analysis at several user defined temperatures / pressures by
        providing the keyword PrintThermoChem and providing the name of the
        Hessian file:

    ```orca
    ! PrintThermoChem
    %geom 
      inhessname "FreqJob.hess" # default: job-basename.hess
    end
    %freq  Temp  290, 295, 300     # in Kelvin
            Pressure  1.0, 2.0, 3.0 # in atm
           end
    ```

[^1]: the corresponding equation for the partition function (assuming
    sufficiently high temperatures) of a linear molecule is
    $Q_{int} = \frac{kT}{\sigma h c B}$ and for non-linear molecules
    $Q_{int} = \frac{1}{\sigma} \sqrt{\frac{\pi}{ABC}(\frac{kT}{hc})^3}$.
    A, B and C are the corresponding rotational constants, $\sigma$ is
    the symmetry number. If you want to choose a different symmetry
    number, ORCA also provides a table with the values for this entropy
    contribution for other symmetry numbers. Herzberg reports the
    following symmetry numbers for the point groups C$_1$,C$_i$,C$_s$:
    1; C$_2$,C$_{2v}$, C$_{2h}$: 2; C$_3$,C$_{3v}$,C$_{3h}$: 3;
    C$_4$,C$_{4v}$,C$_{4h}$: 4;C$_6$, C$_{6v}$, C$_{6h}$: 6; D$_2$,
    D$_{2d}$, D$_{2h}=$V$_h$: 4; D$_3$, D$_{3d}$, D$_{3h}$: 6; D$_4$,
    D$_{4d}$, D$_{4h}$: 8; D$_6$, D$_{6d}$, D$_{6h}$: 12; S$_6$: 3;
    C$_{\in fty v}$: 1; D$_{\in fty h}$: 2;T,T$_d$: 12; O$_h$: 24.

<a id="sec:structurereactivity.thermochemistry.dboc"></a>
## Diagonal Born-Oppenheimer Correction 

For high-accuracy thermochemistry, one of the higher-order corrections
to the energy that is required is the "diagonal Born-Oppenheimer
correction" (DBOC). The expression for the DBOC correction is derived by
first-order perturbation theory and reads:

$$
E_{DBOC} = \left\langle \Psi_{e}\left( r,R \right)|{\widehat{T}}_{N}|\Psi_{e}\left( r,R \right) \right\rangle
$$

In order to evaluate the DBOC correction it is required to calculate the
response of the orbitals (and the density) with respect to nuclear
perturbations, which is the most expensive step of an analytic Hessian
calculation. The correction is therefore best be evaluated in parallel
with the usual thermochemical corrections. The implementation in ORCA
covers the SCF level (e.g. closed-shell and spin-unrestricted
Hartree-Fock and DFT).

```orca
! DBOC
# or NoDBOC to turn it off (which is the default)
```

**Relevant Papers:**

1. [HandyYamaguchiJCP1986](../../bibliography.md)

<a id="sec:structurereactivity.thermochemistry.socc"></a>
## Spin-Orbit Coupling Correction to the Total Energy

Another correction that is required for high-accuracy thermochemistry is
the estimation of the energetic effect of Spin-Orbit-Coupling (SOC) on
the total energy. While most of ORCA treats the SOC as a perturbation
and estimates its effect on molecular properties and spectra, the total
energy contribution would require relativistic two-component theory.
This is not yet implemented in ORCA. Thus, for the time being, there is
a first-order perturbation correction for the SOC that proceeds as
follows:

The SCF energy is:

$$
E_{SCF} = E_{Nuc} + \frac{1}{2}Tr\left( P,H + F \right)
$$

In two-component theory, the Fock operator is:

$$
\overline{F}=\begin{pmatrix}
F^{\alpha} & 0 \\
0 & F^{\beta}
\end{pmatrix}+\begin{pmatrix}
{\frac{1}{2}T}^{z} & {\frac{1}{2}T}^{x}+{\frac{i}{2}T}^{y} \\
{\frac{1}{2}T}^{x}-{\frac{i}{2}T}^{y} & -{\frac{1}{2}T}^{z}
\end{pmatrix}
$$

Where $T^{x,y,z}$ are the 3 components of the SOC matrix.

We then solve the eigenvalue problem:

$$
\overline{F}\overline{C}=\overline{\varepsilon}\overline{SC}
$$

With the two-component overlap matrix

$$
\overline{S}=\begin{pmatrix}
S & 0 \\
0 & S
\end{pmatrix}
$$

Now we calculate the 2C density matrix from the eigenvectors

$$
\overline{P} = {\breve{C}}^{*}{\breve{C}}^{T}
$$

Where $\breve{C}$ is the occupied part of $\overline{C}$. This then
leads to the approximate 2 component energy:

$$
E_{2C} = E_{Nuc} + \frac{1}{2}Tr\left( \overline{P},\overline{H}+\overline{F} \right)
$$

And the SOC correction is then simply:

$$
{\Delta}_{SOC} = E_{2C} - E_{SCF}
$$

$$
= \frac{1}{2}Tr\left( \overline{P},\overline{H}+\overline{F} \right) - \frac{1}{2}Tr\left( P,H + F \right)
$$

This is obviously neglecting the relaxation of the orbitals due to the
SOC. The approximation is necessarily rather crude and consequently,
this term does require a bit of empirical scaling in actual applications
to reach high accuracy.

**Relevant Papers:**

- Kayal, R.; Neese, F. **2025**, in preparation

<a id="sec:structurereactivity.thermochemistry.HEAT"></a>
## High Accuracy Thermochemistry: the HEAT protocol

The HEAT (High accuracy Extrapolated Ab initio Thermochemistry) protocol
was established by Gauss, Stanton, Kallay and co-workers and aims at high
accuracy total energies that are systematically within 1 kJ/mol of the
most accurate experimental energies.

The original HEAT formula contains eight terms:

$$
E_{HEAT} = E_{HF}^{\in fty} + {\Delta}E_{CCSD(T)}^{\in fty} +{\Delta}E_{CCSDT} + {\Delta}E_{CCSDTQ} + {\Delta}E_{rel} + {\Delta}E_{ZPE} + {\Delta}E_{DBOC} + {\Delta}E_{SOC}
$$

Where the individual contributions are:

| **Term**     | **Original Definition**              | **Implementation in ORCA** |
|--------------|--------------------------------------|---------------------|
| Geometry     | Optimized using CCSD(T)/cc-pVQZ      | Same                |
|              |                                      |                     |
|$E_{HF}^{\in fty}$   | Complete basis set limit       | Same                |
|        | extrapolated Hartree-Fock energy     |                     |
|        | using aug-cc-pCVXZ (X=T,Q,5) and the |                     |
|        | formula                              |                     |
|        | $E_{HF}^{X} =$                       |                     |
|        | $E_{HF}^{\in fty} + a\exp( - bX)$     |                     |
|        | $E_{HF}^{\in fty},a,b$ are determined |                     |
|        | from the three energies              |                     |
|        |                                      |                     |        
|${\Delta}E_{CCSD(T)}^{\in fty}$ | Complete basis set limit  | Same    |
|        | extrapolated CCSD(T) energy using    |                     |
|        | aug-cc-pCVXZ (X=Q,5) and the         |                     |
|        | formula                              |                     |
|        | $E_{CCSD(T)}^{X} = $                 |                     |
|        | $E_{CCSD(T)}^{\in fty} + aX^{- 3}$    |                     |
|        |                                      |                     |        
|${\Delta}E_{CCSDT}$       | Compensation of the difference  | Same   |
|        | between CCSD(T) and CCSDT.           |                     |
|        | Difference between two-point         |                     |
|        | extrapolated frozen-core CCSDT and   |                     |
|        | CCSD(T) using                        |                     |
|        | ${\Delta}E_{CCSDT} =$                |                     |
|        | $E_{CCS DT}^{TQ}(FC) - E_{CCSD(T)}^{TQ}(FC)$ |             |
|        |                                      |                     |        
|${\Delta}E_{CCSDTQ}$        | Compensation of the difference  | Same |
|        | between CCSDT and CCSDTQ using the   |                     |
|        | cc-pVDZ basis set                    |                     |
|        | ${\Delta}E_{CCSDTQ} =$               |                     |
|        | $E_{CCSDTQ}^{DZ}(FC) - E_{CCSDT}^{DZ}(FC)$ |                |
|        |                                      |                     |        
|${\Delta}E_{rel}$ | Effects of scalar relativity. | Estimated using the |
|        | Expectation value of the CCSD(T)/    |difference in  CCSD(T)|
|        |aug-cc-pCVTZ-DK                       |energies betweeen aug-cc-pCVTZ and|
|        | density with the Darwin and          | aug-cc-pCVTZ-DK basis|
|        | Mass-Velocity Hamiltonians.          |sets (with the DKH Hamiltonian).|
|        |                                      |                     |
|        |                                      |                     |        
|${\Delta}E_{ZPE}$  | Zero-point energy using an| With the harmonic   |
|        | anharmonic Force Field calculated at | approximation at the |
|        | CCSD(T)/cc-pVQZ                      | CCSD(T)/cc-pVQZ level|
|        | ${\Delta}E_{ZPE} =$                  | with a scaling factor|
|        | $\frac{1}{2}\sum_{i}^{}\omega_{i} +$ |for linear and symmetric|
|        | $\frac{1}{4}\sum_{i \leq j}^{}x_{ij}$|top molecules, with the VPT2|
|        | Where $\omega$ and $x$ are harmonic  |module for rest of the|
|        | and cubic force constants.           |molecules.     |
|        |                                      |                     |        
|${\Delta}E_{DBOC}$ | Diagonal Born-Oppenheimer correction | Same     |
|        | calculated at the SCF level.         |                     |
|        |                                      |                     |        
|${\Delta}E_{SOC}$ | Spin-Orbit-Coupling correction. Full | SCF level first     |
|        | Valence CASSCF with singles- and     | order correction as |
|        | doubles CI together with spin-orbit  | described in  |
|        | effective core potentials.           |[thermochemistry.socc](#sec:structurereactivity.thermochemistry.socc)| 
|        |                                      |and empirically     |
|        |                                      | scaled.             |

Thus, for the most part, the ORCA implementation follows the original prescription with some limited changes that arise from the
unavailability of all energy components in ORCA. The HEAT protocol is computed by a compound script HEAT.cmp that is delivered with ORCA.

**Relevant Papers:**

1. [HEAT2004](../../bibliography.md)
-   Kayal, R.; Neese, F. **2025**, in preparation

