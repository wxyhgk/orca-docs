

<a id="sec:spectroscopyproperties.rocis"></a>
# Excited States via ROCIS and ROCIS/DFT

The ORCA program package can perform configuration interaction with single excitations (CIS) 
calculations using a restricted open-shell Hartee-Fock (ROHF) reference function. 
It produces excitation energies, absorption energies and CD intensities.
It was designed with the aim to reproduce and - even more importantly -
reliably predict transition metal L-edges as observed in X-ray
absorption spectroscopy (XAS).

The original ROCIS implementation [roemelt2013](../../bibliography.md), [roemelt2013b](../../bibliography.md) is able to perform the CIS calculations
only on top of a high-spin ROHF reference function. Starting in ORCA 6.0 the new 
General Spin ROCIS (GS-ROCIS) implementation [gouveia2025JPCA](../../bibliography.md), [gouveia2025SOC](../../bibliography.md) is also available upon request by the user.
This new implementation can perform the CIS calculation on top of any spin coupling situation
obtained with the CSF-ROHF method. This includes the high-spin situations covered previously
by the original implementation.

<a id="sec:spectroscopyproperties.rocis.general"></a>
## General Description

<a id="sec:spectroscopyproperties.rocis.general.gsrocis"></a>
### General Spin ROCIS

The GS-ROCIS method is described as follows:

Starting from a reference CSF constructed in the genealogical coupling scheme (obtained by a `CSF-ROHF` calculation),
four classes of excited CSFs are defined according to the occupation number of the orbitals involved in the excitation.

These excitation classes are:
-  DOMO to SOMO excitations -  $\left| \Phi_i^t \right\rangle$
-  SOMO to VMO excitations - $\left| \Phi_t^a \right\rangle$
-  DOMO to VMO excitations - $\left| \Phi_i^a \right\rangle$
-  DOMO to VMO excitations coupled with SOMO to SOMO excitations - $\left| \Phi_{ui}^{at} \right\rangle$

This way, the GS-ROCIS wavefunction is defined as:

$$

\begin{array}{l}
  \Psi_{GS-ROCIS} = c_0 \left| \Phi_0 \right\rangle + \sum_{i,t}{c_i^t\left| \Phi_i^t \right\rangle} + \sum_{t,a}{c_t^a\left| \Phi_t^a \right\rangle}
  + \sum_{i,a}{c_i^a\left| \Phi_i^a \right\rangle} + \sum_{i,t,a,u\neq t}{c_{ui}^{at}\left| \Phi_{ui}^{at} \right\rangle}
 \end{array}

$$

Where the expansion coefficients $c_p^q$ are determined in the CI procedure.
`GS-ROCIS` can be requested by:
```orca
%rocis
  DoGenROCIS true  # Turns the general-spin ROCIS procedure on 
  ReferenceMult 1  # The reference wavefunction multiplicity
                   # (it needs to agree with the ROHF solution)
end
```
A number of basic variables in the `%rocis` block control the settings
of the Davidson procedure that is used to solve the CI problem:
```orca
%rocis
  NRoots    6     # Number of desired roots.
  MaxDim    5     # Davidson expansion space = MaxDim * NRoots.
  ETol      1e-6  # Energy convergence tolerance.
  RTol      1e-6  # Residual vector convergence tolerance.
  MaxIter   35    # Maxmimum number of iterations.
  NGuessMat 512   # Dimension of the guess matrix: 512x512.
end
```
The amount of output produced during the calculation is controlled via the `PrintLevel` variable:
```orca
%rocis
  PrintLevel 3
end
```
Note, that this does not influence which spectra are calculated or
printed.
The `orca_rocis` module provides two ways of choosing the orbital
excitation space: by orbital energy or orbital number. In the former
case an energy window has to be specified and the program will then take
all orbitals, whose orbital energies lie within this window, into
account. Note, that one actually has to define two orbital windows: One
for the donor and the second for the acceptor orbital. The input of the
windows is done as an array: The first two numbers define the donor
space while the last two numbers define the acceptor space.
```orca
%rocis
  NRoots 3
  EWin = -5,5,-5,5
end
```
The default is to keep core orbitals and very high lying virtual
orbitals out of their respective orbital excitation spaces. Since these
orbitals span a space that is usually not reachable with regular UV/Vis
spectroscopy, this is a reasonable approximation. One has to keep in
mind that an orbital energy window makes only sense if the orbitals used
in the calculation have a well-defined orbital energy. As a consequence
one cannot use an orbital energy window for a calculation with localized
orbitals. The second way to specify the excitation space is by orbital
numbering.
```orca
%rocis
  NRoots 3
  OrbWin = 1,13,9,22
end
```
In restricted calculations only one set of spatial orbitals is created.
Hence it is not necessary to provide orbital windows for $\alpha$ and
$\beta$ electrons separately. Of course, only doubly or singly occupied
orbitals can act as donor orbitals and only singly and nonoccupied
orbitals can act as acceptor orbitals. The program recognises
nonoccupied orbitals in the donor space and doubly occupied orbitals in
the acceptor space and removes both.
The absorption spectrum calculated on the basis of the pure
dipole approximation for your calculation is always printed.
Furthermore like in TD-DFT (section
[sec:spectroscopyproperties.tddft](#sec:spectroscopyproperties.tddft)) or CASSCF one may obtain 
intensities by evaluating the 2nd order oscillation strengths, or
the full semi-classical oscillation strengths. 
-   The exact oscillation strengths behave like the multipole expansion
    in the velocity representation.
-   They are by definition origin independent they do not suffer from
    artificial negative values like the multipole moments beyond 1st
    order.
-   They are used with the multipole moments up to 2nd order to
    regenerate the electric dipole, electric quadrupole and magnetic
    dipole contributions in either length or the velocity
    representation.
```orca
%rocis
  DoDipoleLength        true
  DoDipoleVelocity      true
  DecomposeFosc         true
  DoFullSemiclassical   true
  DoCD                  true
end
```
Further details can be found in the section [sec:spectroscopyproperties.ops](#sec:spectroscopyproperties.ops).
The user can control which orbital excitations to include in the ROCIS problem:
```orca
%rocis
  Do_is true     # Include DOMO->SOMO excitations
  Do_sa true     # Include SOMO->Virtual excitations
  Do_ia true     # Include DOMO->Virtual excitations
  Do_ista true   # Include DOMO->SOMO coupled to
                 # SOMO->Virtual excitations with s not equal t
  # For GS-ROCIS, the following excitation is included in the DOMO->VMO class
  # Only on the original ROCIS implementation it is a separate class.
  Do_isa true    # Include DOMO->SOMO coupled to
                 # SOMO->Virtual excitations with s = t
end
```
By default, all excitations are included.
When the program finishes the ROCIS calculation
it gives the excitation energy together with the composition for each
root and the respective spin coupling situation.
According to the number of labels of the respective functions
$\left|\Phi \right\rangle$, contributions from excited configuration
state functions belonging to the different excitation classes are given
by two, three or four numbers.
```orca
STATE  16   Exc. Energy: 27294.664mEh  742.726eV     5990486.3cm**-1
       8->50                 :   0.0145   (-0.120499) : spin coupling: +1-1+1+1+1+1
       8->51                 :   0.0317   (0.178098)  : spin coupling: +1+1+1+1+1-1
       8->51                 :   0.2212   (-0.470333) : spin coupling: +1+1-1+1+1+1
       8->51                 :   0.4135   (-0.643076) : spin coupling: +1-1+1+1+1+1
       6->46   ;   48->51    :   0.0843   (-0.290338) : spin coupling: +1 2+1 0+1+1
       6->47   ;   49->51    :   0.1252   (-0.353805) : spin coupling: +1+1 2+1 0+1 
       7->46   ;   49->51    :   0.0452   (-0.212665) : spin coupling: +1 2+1+1 0+1 
       7->47   ;   48->51    :   0.0133   (0.115519)  : spin coupling: +1+1 2 0+1+1
       7->49   ;   46->51    :   0.0109   (0.104242)  : spin coupling: +1 0+1+1 2+1 
```
Furthermore the ROCIS is able to calculate the effect of
spin-orbit coupling (SOC) on the calculated ground and excited states.
It introduces SOC in the framework of quasi-degenerate perturbation
theory (QDPT). The SOC Hamiltonian is diagonalized in the basis of the
calculated ROCIS states $\left| \Psi_I^{SM} \right\rangle$, where $I$ is
the root label and $S$ and $M$ are the spin and magnetic spin quantum
numbers, respectively[neese1998inorgchem](../../bibliography.md), [roemelt2013](../../bibliography.md).
```orca
%rocis
  rel
    DoSOC true        # invokes the calculation of SOC effects
    TEMPERATURE 10    # temperature for SOC corrected spectra in Kelvin
  end
end
```
After the SOC calculation the program will produce additional spectra
for the SOC corrected results. The spectra contain transitions from the
$2S+1$ lowest lying states into all excited states, where S is the spin
quantum number of the electronic ground state. These $2S+1$ lowest
states may be split up in the order of 1-100 cm$^{-1}$. Due to the small
magnitude of the splitting, all of the  $2S+1$ states
can be significantly populated even at low temperatures. Experimentally,
the intensity of a given transition is dependent on the population of
the corresponding initial state. With the `TEMPERATURE` keyword the
population of the theoretically calculated states can be manipulated by
the varying the fictive temperature of the system. It has to be
mentioned that the electric quadrupole transitions between spin-orbit
coupled states are not well defined and are likely to give unreasonable
results. Hence it is recommended to use the `Decomposefosc` keyword only
for calculations that do not include SOC.
```orca
--------------------------------------------------------------------------------------------------------
      SOC CORRECTED ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS
--------------------------------------------------------------------------------------------------------
      Transition         Energy     Energy  Wavelength fosc(D2)      D2       |DX|      |DY|      |DZ|
                          (eV)      (cm-1)    (nm)  (*population)  (au**2)    (au)      (au)      (au)
--------------------------------------------------------------------------------------------------------
  0-5.0A  ->  1-5.0A    0.000000       0.0     0.0   0.000000000   0.00000   0.00000   0.00000   0.00000
  2-5.0A  ->  3-5.0A    0.000000       0.0  2927278012.6   0.000000000   0.00000   0.00000   0.00000   0.00000
  3-5.0A  ->  4-5.0A    0.000001       0.0  2013441147.3   0.000000000   0.00000   0.00000   0.00000   0.00000
  2-5.0A  ->  4-5.0A    0.000001       0.0  1192923906.3   0.000000000   0.00000   0.00000   0.00000   0.00000
  1-5.0A  ->  2-5.0A    0.000002       0.0  559585326.1   0.000000000   0.00000   0.00000   0.00000   0.00000
  0-5.0A  ->  2-5.0A    0.000002       0.0  554991701.4   0.000000000   0.00000   0.00000   0.00000   0.00000
  1-5.0A  ->  3-5.0A    0.000003       0.0  469780906.9   0.000000000   0.00000   0.00000   0.00000   0.00000
  0-5.0A  ->  3-5.0A    0.000003       0.0  466539107.5   0.000000000   0.00000   0.00000   0.00000   0.00000
  1-5.0A  ->  4-5.0A    0.000003       0.0  380906816.8   0.000000000   0.00000   0.00000   0.00000   0.00000
  0-5.0A  ->  4-5.0A    0.000003       0.0  378772788.3   0.000000000   0.00000   0.00000   0.00000   0.00000
  4-5.0A  ->  5-5.0A   715.072294 5767447.6     1.7   0.000853852   0.00024   0.00000   0.01494   0.00454
  3-5.0A  ->  5-5.0A   715.072294 5767447.6     1.7   0.000001143   0.00000   0.00021   0.00018   0.00050
  2-5.0A  ->  5-5.0A   715.072295 5767447.6     1.7   0.000001245   0.00000   0.00024   0.00053   0.00012
  1-5.0A  ->  5-5.0A   715.072297 5767447.6     1.7   0.000000330   0.00000   0.00000   0.00029   0.00010
  0-5.0A  ->  5-5.0A   715.072297 5767447.6     1.7   0.000024144   0.00001   0.00000   0.00251   0.00076
  4-5.0A  ->  6-5.0A   715.089740 5767588.3     1.7   0.000002661   0.00000   0.00067   0.00036   0.00042
  3-5.0A  ->  6-5.0A   715.089741 5767588.3     1.7   0.000008083   0.00000   0.00000   0.00145   0.00045
  2-5.0A  ->  6-5.0A   715.089742 5767588.3     1.7   0.000775076   0.00022   0.00001   0.01423   0.00432
  1-5.0A  ->  6-5.0A   715.089744 5767588.4     1.7   0.000000497   0.00000   0.00002   0.00015   0.00035
  0-5.0A  ->  6-5.0A   715.089744 5767588.4     1.7   0.000001537   0.00000   0.00056   0.00035   0.00007
  4-5.0A  ->  7-5.0A   715.115140 5767793.2     1.7   0.000001500   0.00000   0.00027   0.00020   0.00056
  3-5.0A  ->  7-5.0A   715.115141 5767793.2     1.7   0.000834113   0.00024   0.00001   0.01476   0.00449
  2-5.0A  ->  7-5.0A   715.115141 5767793.2     1.7   0.000008694   0.00000   0.00002   0.00150   0.00050
  1-5.0A  ->  7-5.0A   715.115143 5767793.2     1.7   0.000000562   0.00000   0.00026   0.00025   0.00018
  0-5.0A  ->  7-5.0A   715.115143 5767793.2     1.7   0.000003341   0.00000   0.00036   0.00031   0.00085
  4-5.0A  ->  8-5.0A   715.184940 5768356.2     1.7   0.000000146   0.00000   0.00004   0.00020   0.00001
  3-5.0A  ->  8-5.0A   715.184940 5768356.2     1.7   0.000019943   0.00001   0.00206   0.00012   0.00120
...
```
If the `PrintLevel` value is set to 3 or higher, the program will print
out the composition of the SOC corrected states in the basis of states
$\left| \Psi_I^{SM} \right\rangle$.
```orca
Eigenvectors of SOC calculation:
the threshold for printing is: 0.010000
          weight         real           image    :   Root   Block   Spin    Ms
State 0:           0.00 cm**-1         0.00000 eV
        0.135363      -0.028407       0.366819   :      0     0     2      2
        0.181749       0.224125       0.362653   :      0     0     2      1
        0.367330      -0.135925      -0.590639   :      0     0     2      0
        0.180828       0.039792      -0.423372   :      0     0     2     -1
        0.134728       0.185875       0.316510   :      0     0     2     -2
State 1:           0.00 cm**-1         0.00000 eV
        0.078367      -0.271364       0.068762   :      0     0     2      2
        0.306783       0.460606       0.307612   :      0     0     2      1
        0.228162       0.440545       0.184613   :      0     0     2      0
        0.307656      -0.543907      -0.108722   :      0     0     2     -1
        0.079031      -0.142362      -0.242414   :      0     0     2     -2
State 2:           0.02 cm**-1         0.00000 eV
        0.416636       0.252581       0.594003   :      0     0     2      2
        0.072004      -0.082420       0.255363   :      0     0     2      1
        0.022669      -0.134504       0.067662   :      0     0     2      0
        0.071994       0.254211       0.085850   :      0     0     2     -1
        0.416695      -0.326890      -0.556631   :      0     0     2     -2
State 3:           0.02 cm**-1         0.00000 eV
        0.080023      -0.256741       0.118772   :      0     0     2      2
        0.319001       0.556244       0.097947   :      0     0     2      1
        0.201858      -0.134225       0.428768   :      0     0     2      0
        0.319074       0.512787       0.236903   :      0     0     2     -1
        0.080042       0.143270       0.243959   :      0     0     2     -2
State 4:           0.03 cm**-1         0.00000 eV
        0.289609      -0.315623      -0.435879   :      0     0     2      2
        0.120461       0.303600      -0.168190   :      0     0     2      1
        0.179979      -0.232115      -0.355108   :      0     0     2      0
        0.120448       0.275975      -0.210441   :      0     0     2     -1
        0.289502      -0.272469      -0.463963   :      0     0     2     -2
State 5:     5767447.63 cm**-1       715.07230 eV
        0.191190      -0.086278       0.428656   :      1     0     2      2
        0.061035      -0.247045      -0.001820   :      1     0     2      1
        0.055460      -0.038920       0.232262   :      1     0     2      0
        0.061035      -0.234143      -0.078813   :      1     0     2     -1
        0.191190      -0.058171       0.433366   :      1     0     2     -2
        0.109587      -0.316206      -0.097982   :      2     0     2      2
        0.026192      -0.108605      -0.119987   :      2     0     2      1
        0.010968       0.017308      -0.103287   :      2     0     2      0
        0.026192      -0.141786       0.078029   :      2     0     2     -1
        0.109587       0.330874       0.010450   :      2     0     2     -2
        0.015452       0.114128      -0.049265   :      3     0     2      2
        0.041882      -0.204634      -0.002607   :      3     0     2      1
        0.027697       0.027504      -0.164135   :      3     0     2      0
        0.041882      -0.194305      -0.064244   :      3     0     2     -1
        0.015452      -0.091834      -0.083778   :      3     0     2     -2
State 6:     5767588.34 cm**-1       715.08974 eV
        0.198585      -0.131642       0.425741   :      1     0     2      2
        0.047453      -0.161434       0.146261   :      1     0     2      1
        0.019867      -0.139025      -0.023213   :      1     0     2      0
        0.047453       0.105160       0.190773   :      1     0     2     -1
        0.198585       0.013812      -0.445415   :      1     0     2     -2
        0.160559      -0.388214      -0.099243   :      2     0     2      2
        0.044707      -0.072788      -0.198517   :      2     0     2      1
        0.014352      -0.118163      -0.019729   :      2     0     2      0
        0.044707       0.133333      -0.164102   :      2     0     2     -1
        0.160559      -0.399398      -0.032262   :      2     0     2     -2
        0.012669      -0.111020      -0.018537   :      3     0     2      0
...
```
Further details of the SOC calculation such as the procedure of SOC
integral calculation can be controlled via the `%rel` block (section
[sec:essentialelements.relativistic](#sec:essentialelements.relativistic).
<a id="sec:spectroscopyproperties.rocis.general.hsrocis"></a>
### Original ROCIS Implementation
It is still possible to use the original implementation of ROCIS[roemelt2013](../../bibliography.md), [roemelt2013b](../../bibliography.md)
which is able to perform CIS calculations only on top of a high-spin ROHF reference function.
All spins of the unpaired electrons have to be coupled ferromagnetically
to give a total spin of $S = \frac{1}{2}N$, where $N$ is the number of
unpaired electrons.
The usage of the original ROCIS implementation can be requested by:
```orca
%rocis
  DoGenROCIS false
end
```
In our experience ROHF calculations suffer a lot from convergence
problems. UHF calculations generally exhibit better convergence
properties. In most cases the quasi-restricted orbitals (qro's) of a UHF
calculation resemble the ROHF orbitals. Thus the original ROCIS features the
ability to start a calculation on top of a UHF calculation. It
will automatically create the qro's and build the reference determinant
with them. If one wants to avoid the (small) errors that are introduced
by this procedure, one may take the qro's of a UHF calculation as
starting orbitals for a subsequent ROHF calculation.
<a id="sec:spectroscopyproperties.rocis.general.dftrocis"></a>
### ROCIS/DFT
!!! warning
    -   Currently, `ROCIS/DFT` is not implemented for the general-spin (`GS-ROCIS`) procedure.
For many transition metal compounds the description of the electronic
ground and excited states by Hartree-Fock theory and CIS is of rather
poor quality. Especially covalency and relative spin state energetics
are not reproduced correctly. This in turn might lead to wrong intensity
distributions in the calculated L-edge spectra. In the majority of these
cases the quality of the description and hence the predicted L-edge
spectra can be significantly improved with the ROCIS/DFT method[roemelt2013](../../bibliography.md).
It features the usage of a restricted open-shell Kohn-Sham matrix as reference 
and also uses the DFT orbitals for setting up the excited configuration state 
functions in the CI expansion.
The two electron integrals that include the DFT orbitals are scaled
according to their nature and their position in the CI matrix by the
parameters $c_{1}$, $c_{2}$ and $c_{3}$. They all lie in the interval
[0;1]. Parameters $c_{1}$ and $c_{2}$ scale coulomb- and exchange-
like terms in the diagonal part of the CI matrix, whereas $c_{3}$
reduces the size of all off-diagonal elements of the CI matrix. For
example:

$$

\begin{array}{l}
 H_{ia,ia}^{\text{DFT/ROCIS} } =F_{aa}^{C\left( \text{KS} \right)} -F_{ii}^{C\left( \text{KS}
\right)} -c_{1} \left({ ii\vert aa} \right)+2c_{2} \left({ ia\vert ia}
\right) \\
 H_{ia,jb}^{\text{DFT/ROCIS} } =c_{3} \left\{{ \delta_{ij} F_{ab}^{C\left( \text{KS}
\right)} -\delta_{ab} F_{ji}^{C\left( \text{KS} \right)} -\left({ ij\vert ab}
\right)+2\left({ ia\vert jb} \right)} \right\} \end{array}\qquad \text{(eqn:219)}

$$

The three default parameters $c_{1} = 0.18$, $c_{2} = 0.20$ and
$c_{3} = 0.40$ have been optimized for a test set of molecules and their
excited states on a B3LYP/def2-TZVP(-f) level of theory but can be
freely chosen[roemelt2013](../../bibliography.md). It is most likely that for a different
combination of test molecules, functional and basis set, a different set
of parameters gives better results. Since the parameters are chosen with
regard of a good \"balance\" between orbital energies, Coulomb and
exchange integrals, a new set of parameters should at least crudely
resemble their relative proportions.

The ROCIS/DFT method can be requested by the following keywords:

```orca
%rocis
  DoGenROCIS            false   # ROCIS/DFT is available only for the
                                # high-spin implementation of ROCIS.
  DoDFTCIS               true   # Switches on the ROCIS/DFT method.
  DFTCIS_c = 0.18, 0.20, 0.40   # Array input of the three parameters.
end
```

<a id="sec:spectroscopyproperties.rocis.general.ri"></a>
### Resolution of the Identity

If calculations on large molecules are conducted, the integral
transformation will be the most time-consuming part. Therefore it is
strongly recommended to use the resolution of the identity (RI)
approximation in those cases. It effectively reduces the computational
costs of the transformation step by only introducing minor errors to the
calculation. It has to be kept in mind that in order to keep the
introduced errors small, one has to provide a reasonable auxiliary basis
sets along with your normal basis set input.

```orca
! def2-SVP def2-SVP/C TightSCF

%scf
  HFTyp ROHF
  ROHF_Case HighSpin
  ROHF_Nel[1] = 1
end

%rocis
  NRoots 5
  DoRI true   # invokes the RI approximation
end

* xyz 0 2
 N 0 0 0
 O 0 0 1.15
*
```

<!-- >```orca
%rocis
  DoGenROCIS true  # Turns the general-spin ROCIS procedure on 
  ReferenceMult 1  # The reference wavefunction multiplicity
                   # (it needs to agree with the ROHF solution)
end
```-->

<a id="sec:spectroscopyproperties.rocis.PNO"></a>
## Core PNO-ROCIS, PNO-ROCIS/DFT

It has been shown [2018pnorocis](../../bibliography.md) that it is possible to combine
the powerful machinery of Pair Natural Orbitals (PNOs) with the ROCIS and
ROCIS/DFT methods to formulate the core PNO-ROCIS and PNO-ROCIS/DFT methods.
The usage of PNOs here is somewhat unconventional since they are not used to treat
electron correlation effects in a state specific manner. Rather, the
PNOs are used to identify the relevant part of the virtual space that
can be reached by excitation out of local core orbitals. This subspace
of the virtual space is local, thus leading to a linear scaling, state
universal method.

The PNO-ROCIS calculations can be requested with the following keywords:

```orca
%rocis
  DoPNO     true       # Flag to call the PNO truncation
  TCutPNO   1e-11      # Threshold to cutout the PNO populations
  XASElems  0          # Number of the involved element to the
                       # calculated core XAS calculation
end
```

As shown in reference[2018pnorocis](../../bibliography.md), a universal TCutPNO 1e-11
threshold can be defined for all edges provided that the PNOs are
constructed by taking into account all the available core orbitals in
the systems. For example in the case of a 1st row transition metal this
will be the 9 1s, 2s, 2p, 3s and 3p MOs. These orbitals will be
identified automatically by the program provided that the elements for which
the XAS calculation will be performed are specified within the XASElems keyword.

```orca
===============================================================
Core PNO/ROCIS truncation
===============================================================

...

================================================================
TCutPNO:                              1.000e-13
Virtual orbitals before selection:   303 ... 2772 (2470 MO's)
Virtual orbitals after selection:    303 ...  558 (256 MO's)
PNO transformation completed in:    3253.03 sec 
================================================================

```

From this point and on the programm will proceed the usual way. This
will result in extraordinary computation speeding ups without loss in
accuracy.

<a id="sec:spectroscopyproperties.rocis.transMetal"></a>
## Transition Metal L-Edges with ROCIS or DFT/ROCIS

The ROCIS method was designed to calculate transition metal
L-edge spectra of large molecules as they are observed in X-ray
absorption spectroscopy (XAS). An L-edge results when an electron is
promoted from the 2p shell of a transition metal ion into the valence d
shell by an X-ray photon. Strong spin-orbit coupling in the 2p shell and
p-d coupling phenomena complicate the interpretation and even more so
the prediction of these spectra. It has to be kept in mind that the
present program applies a variety of approximations which might lead to
observable deviations from experimentally determined spectra. However,
we believe that the results obtained from the program are in general
qualitatively correct and in most cases accurate close to the
experimental uncertainty. In cases where quantitative accuracy is not
met, the provided results might still give some insight into the
mechanisms of intensity distribution in the spectra.

The special input structure for orbital windows described in
[sec:spectroscopyproperties.excitedstates.rocis](#sec:spectroscopyproperties.excitedstates.rocis) allows the user to restrict the
donor orbital space to the transition metal 2p shell. The acceptor
orbital space is the same as in regular UV/Vis spectroscopy. It should
include all singly occupied molecular orbitals and as many virtual
orbitals as one can afford in the calculation (preferably all).
The number of roots should be chosen large enough so that at least all 2p-3d single
excitations are calculated. In many cases even more roots are required
since doubly excited or charge transfer states may become important.
Moreover the strong SOC apparent in the 2p shell of transition metal
ions necessitates the additional calculation of excited states with a
total spin of $S' = S + 1$ and $S' = S -1$ where $S$ is the total spin
of the electronic ground state.
Accordingly, additional excitation classes introduce excited configuration state functions
with a lower and higher spin multiplicity.

for $S' = S + 1$:
-  DOMO to SOMO excitations -  $\left| \Phi_i^{t+} \right\rangle$
-  SOMO to VMO excitations - $\left| \Phi_t^{a+} \right\rangle$
-  DOMO to VMO excitations - $\left| \Phi_i^{a+} \right\rangle$

for $S' = S -1$:
-  DOMO to SOMO excitations -  $\left| \Phi_i^{t-} \right\rangle$
-  SOMO to VMO excitations - $\left| \Phi_t^{a-} \right\rangle$
-  DOMO to VMO excitations - $\left| \Phi_i^{a-} \right\rangle$
-  SOMO to SOMO excitations - $\left| \Phi_t^{u-} \right\rangle$

!!! note
    -   Depending on the ground state multiplicity and/or occupation of the involved orbitals,
        some excitations are not possible. The program automatically includes only the allowed excitations
        into the respective multiplicities.

Inclusion of configuration state functions with higher or lower
multiplicity is invoked with the keywords `DoLowerMult` and
`DoHigherMult`, respectively.

```orca
%rocis
  DoLowerMult true     #Invokes a CI calculation  #with S'=S-1
  DoHigherMult true    #Invokes a CI calculation  #with S'=S+1
end
```

The program will conduct a separate Davidson procedure for each
multiplicity. Subsequently it gives the excitation energies and
compositions of the calculated excited states for all included
multiplicities.

Here is an example calculation of L-edge XAS on [FeCl$_4$]$^{2-}$:

```orca
# [Fe(II)Cl4]2- - ROCIS - L-edge

!x2c x2c-SVPall AutoAux TightSCF

%pal
  nproc 12
end

%scf
  HFTyp ROHF
  ROHF_CASE HIGHSPIN
  ROHF_NEL[1] 4
end

%rocis
  DoGenROCIS true
  ReferenceMult 5
  NRoots 50
  OrbWin 6,8,0,2000
  DoPNO true
  TCutPNO 1e-11
  XASelems 0
  rel
    DoSOC true
  end
  DoHigherMult true
  DoLowerMult true
  DoRI true
  Decomposefosc true
end

*xyz -2 5
  Fe    -0.009575    0.000087    0.011550
  Cl    -1.774578   -1.558533   -0.219791
  Cl    -0.681385    1.874633    1.289404
  Cl     0.666770    0.847828   -2.091305
  Cl     1.756927   -1.164015    1.071196
end
```

After all CI calculations are finished, the program
gives a list of all calculated roots with their excitation energies and
their multiplicities. It is this number that will be referred to as
label $I$ in the decomposition of spin-orbit coupled states in the basis
$\left| \Psi_{I}^{SM} \right\rangle$. It is very important to note, that
when states with different multiplicities are calculated this number
might deviate from the number that appears in the respective CI part of
the output. If one gets confused about the numbering of the states, the
state energies might act as a guideline through the output of the
program.

```orca
-------------------
Excitation energies
-------------------

--------------------------------------------------------------------------------
    ROOT    Mult      Excitation energy[Eh]           [cm-1]          [eV]
--------------------------------------------------------------------------------
     0       5            0.00000000                      0.00          0.000
     1       5            26.41778649                5798033.94        718.865
     2       5            26.42452401                5799512.66        719.048
     3       5            26.42621555                5799883.91        719.094
     4       5            26.44615744                5804260.65        719.637
     5       5            26.45323131                5805813.18        719.829
     6       5            26.47192609                5809916.21        720.338
     7       5            26.47357807                5810278.78        720.383
     8       5            26.48177016                5812076.74        720.606
     9       5            26.49063895                5814023.21        720.847
    10       5            26.50722706                5817663.88        721.298
    11       5            26.50759779                5817745.25        721.308
    12       5            26.50982238                5818233.49        721.369
    13       3            26.55037043                5827132.76        722.472
    14       3            26.58407940                5834531.02        723.390
    15       3            26.58587963                5834926.12        723.439
    16       3            26.58857702                5835518.13        723.512
    17       3            26.59674863                5837311.59        723.734
    18       3            26.59825865                5837643.00        723.775
    19       3            26.61152227                5840554.03        724.136
    20       3            26.61806435                5841989.85        724.314
    21       3            26.62812795                5844198.56        724.588
    22       3            26.63079807                5844784.58        724.661
    23       3            26.63345218                5845367.09        724.733
    24       3            26.64337021                5847543.85        725.003
    25       3            26.65680719                5850492.92        725.369
    26       3            26.66486245                5852260.85        725.588
    27       3            26.66512507                5852318.49        725.595
    28       3            26.66741755                5852821.63        725.657
    29       3            26.68096811                5855795.63        726.026
    30       3            26.68291870                5856223.74        726.079
    31       3            26.68410859                5856484.89        726.112
    32       3            26.68502036                5856685.00        726.136
    33       3            26.68625712                5856956.44        726.170
    34       3            26.68835097                5857415.98        726.227
    35       3            26.69951161                5859865.46        726.531
    36       3            26.70277202                5860581.04        726.619
    37       3            26.71055426                5862289.04        726.831
    38       3            26.71604333                5863493.75        726.980
    39       3            26.71631714                5863553.85        726.988
    40       3            26.71801283                5863926.01        727.034
    41       3            26.71869535                5864075.80        727.053
    42       3            26.71953590                5864260.28        727.076
    43       3            26.72200411                5864801.99        727.143
    44       3            26.72811146                5866142.40        727.309
    45       3            26.73591005                5867853.99        727.521
    46       3            26.73675062                5868038.48        727.544
    47       3            26.75216877                5871422.37        727.964
    48       3            26.78204828                5877980.17        728.777
    49       7            27.21891306                5973860.90        740.664
    50       7            27.21926225                5973937.54        740.674
    51       7            27.21931555                5973949.24        740.675
    52       5            27.26974929                5985018.16        742.048
    53       5            27.26978849                5985026.77        742.049
    54       5            27.27023065                5985123.81        742.061
    55       5            27.29466376                5990486.26        742.726
    56       5            27.29677691                5990950.04        742.783
    57       5            27.31333680                5994584.52        743.234
    58       7            27.31641173                5995259.39        743.317
    59       5            27.31967798                5995976.24        743.406
    60       7            27.32002169                5996051.68        743.416
...
```

Without SOC the spin exclusion rule applies which means that only
excited states with a total spin equal to the ground state spin
($S' = S$) give rise to non-vanishing intensities. Hence, only these
transitions are listed in the spectra before SOC.

```orca
------------------------
ROCIS-EXCITATION SPECTRA
------------------------

Center of mass = ( -0.0160,  0.0000,  0.0229)
Reading integrals                                                ...
Reading the Dipole integrals                                     ... done
Reading the Linear Momentum integrals                            ... done
Reading the Angular momentum integrals                           ... done
Reading the Quadrupole integrals                                 ... done
Reading the Higher Moment integrals                              ... done
--------------------------------------------------------------------
Using One-Photon Spectroscopy Tool
--------------------------------------------------------------------

----------------------------------------------------------------------------------------------------
                     ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS
----------------------------------------------------------------------------------------------------
     Transition      Energy     Energy  Wavelength fosc(D2)      D2        DX        DY        DZ
                      (eV)      (cm-1)    (nm)                 (au**2)    (au)      (au)      (au)
----------------------------------------------------------------------------------------------------
  0-5A  ->  1-5A   718.864517 5798034.0     1.7   0.007967331   0.00045   0.00001  -0.02035   0.00619
  0-5A  ->  2-5A   719.047854 5799512.7     1.7   0.000032204   0.00000   0.00123  -0.00019  -0.00052
  0-5A  ->  3-5A   719.093883 5799883.9     1.7   0.000038607   0.00000  -0.00060  -0.00039  -0.00130
  0-5A  ->  4-5A   719.636530 5804260.7     1.7   0.000000074   0.00000  -0.00004  -0.00001  -0.00005
  0-5A  ->  5-5A   719.829019 5805813.2     1.7   0.000257559   0.00001  -0.00007  -0.00364   0.00116
  0-5A  ->  6-5A   720.337730 5809916.2     1.7   0.045609938   0.00258  -0.04638   0.00619   0.01987
  0-5A  ->  7-5A   720.382683 5810278.8     1.7   0.043374431   0.00246   0.02031   0.01315   0.04327
  0-5A  ->  8-5A   720.605601 5812076.7     1.7   0.000000543   0.00000   0.00005   0.00005   0.00016
  0-5A  ->  9-5A   720.846933 5814023.2     1.7   0.180244898   0.01021   0.00031   0.09663  -0.02948
  0-5A  -> 10-5A   721.298318 5817663.9     1.7   0.084488140   0.00478  -0.02823  -0.01833  -0.06040
  0-5A  -> 11-5A   721.308407 5817745.3     1.7   0.085964316   0.00486   0.06366  -0.00850  -0.02719
  0-5A  -> 12-5A   721.368941 5818233.5     1.7   0.000000007   0.00000  -0.00000   0.00002   0.00001
  0-5A  -> 13-5A   742.047603 5985018.2     1.7   0.002287503   0.00013   0.00507   0.00276   0.00962
  0-5A  -> 14-5A   742.048670 5985026.8     1.7   0.002278095   0.00013   0.00999  -0.00164  -0.00477
  0-5A  -> 15-5A   742.060702 5985123.8     1.7   0.001342355   0.00007   0.00019   0.00823  -0.00246
  0-5A  -> 16-5A   742.725560 5990486.3     1.7   0.000418059   0.00002   0.00197   0.00126   0.00419
  0-5A  -> 17-5A   742.783062 5990950.1     1.7   0.000464555   0.00003   0.00461  -0.00063  -0.00197
  0-5A  -> 18-5A   743.233680 5994584.5     1.7   0.000000003   0.00000  -0.00001  -0.00000  -0.00001
  0-5A  -> 19-5A   743.406232 5995976.3     1.7   0.000000000   0.00000  -0.00000  -0.00000  -0.00000
  0-5A  -> 20-5A   743.562910 5997239.9     1.7   0.000577479   0.00003   0.00001   0.00538  -0.00165
  0-5A  -> 21-5A   743.597306 5997517.4     1.7   0.000009265   0.00000  -0.00029  -0.00017  -0.00063
  0-5A  -> 22-5A   743.658216 5998008.6     1.7   0.000010720   0.00000  -0.00070   0.00011   0.00029
  0-5A  -> 23-5A   744.043391 6001115.3     1.7   0.000081920   0.00000  -0.00088  -0.00059  -0.00184
  0-5A  -> 24-5A   744.092953 6001515.0     1.7   0.000301862   0.00002  -0.00017  -0.00389   0.00119
...
```

After calculation of SOC in the basis of all calculated ROCIS roots, the
program prints out the composition of the spin-orbit coupled states (if
`PrintLevel` \>2) and the corresponding absorption spectrum.

```orca
Eigenvectors of SOC calculation:
the threshold for printing is: 0.010000
          weight         real           image    :   Root   Block   Spin    Ms
State 0:           0.00 cm**-1         0.00000 eV
        0.135363      -0.028407       0.366819   :      0     0     2      2
        0.181749       0.224125       0.362653   :      0     0     2      1
        0.367330      -0.135925      -0.590639   :      0     0     2      0
        0.180828       0.039792      -0.423372   :      0     0     2     -1
        0.134728       0.185875       0.316510   :      0     0     2     -2

State 1:           0.00 cm**-1         0.00000 eV
        0.078367      -0.271364       0.068762   :      0     0     2      2
        0.306783       0.460606       0.307612   :      0     0     2      1
        0.228162       0.440545       0.184613   :      0     0     2      0
        0.307656      -0.543907      -0.108722   :      0     0     2     -1
        0.079031      -0.142362      -0.242414   :      0     0     2     -2

State 2:           0.02 cm**-1         0.00000 eV
        0.416636       0.252581       0.594003   :      0     0     2      2
        0.072004      -0.082420       0.255363   :      0     0     2      1
        0.022669      -0.134504       0.067662   :      0     0     2      0
        0.071994       0.254211       0.085850   :      0     0     2     -1
        0.416695      -0.326890      -0.556631   :      0     0     2     -2

State 3:           0.02 cm**-1         0.00000 eV
        0.080023      -0.256741       0.118772   :      0     0     2      2
        0.319001       0.556244       0.097947   :      0     0     2      1
        0.201858      -0.134225       0.428768   :      0     0     2      0
        0.319074       0.512787       0.236903   :      0     0     2     -1
        0.080042       0.143270       0.243959   :      0     0     2     -2

State 4:           0.03 cm**-1         0.00000 eV
        0.289609      -0.315623      -0.435879   :      0     0     2      2
        0.120461       0.303600      -0.168190   :      0     0     2      1
        0.179979      -0.232115      -0.355108   :      0     0     2      0
        0.120448       0.275975      -0.210441   :      0     0     2     -1
        0.289502      -0.272469      -0.463963   :      0     0     2     -2

State 5:     5767447.63 cm**-1       715.07230 eV
        0.191190      -0.086278       0.428656   :      1     0     2      2
        0.061035      -0.247045      -0.001820   :      1     0     2      1
        0.055460      -0.038920       0.232262   :      1     0     2      0
        0.061035      -0.234143      -0.078813   :      1     0     2     -1
        0.191190      -0.058171       0.433366   :      1     0     2     -2
        0.109587      -0.316206      -0.097982   :      2     0     2      2
        0.026192      -0.108605      -0.119987   :      2     0     2      1
        0.010968       0.017308      -0.103287   :      2     0     2      0
        0.026192      -0.141786       0.078029   :      2     0     2     -1
        0.109587       0.330874       0.010450   :      2     0     2     -2
        0.015452       0.114128      -0.049265   :      3     0     2      2
        0.041882      -0.204634      -0.002607   :      3     0     2      1
        0.027697       0.027504      -0.164135   :      3     0     2      0
        0.041882      -0.194305      -0.064244   :      3     0     2     -1
        0.015452      -0.091834      -0.083778   :      3     0     2     -2

State 6:     5767588.34 cm**-1       715.08974 eV
        0.198585      -0.131642       0.425741   :      1     0     2      2
        0.047453      -0.161434       0.146261   :      1     0     2      1
        0.019867      -0.139025      -0.023213   :      1     0     2      0
        0.047453       0.105160       0.190773   :      1     0     2     -1
        0.198585       0.013812      -0.445415   :      1     0     2     -2
        0.160559      -0.388214      -0.099243   :      2     0     2      2
        0.044707      -0.072788      -0.198517   :      2     0     2      1
        0.014352      -0.118163      -0.019729   :      2     0     2      0
        0.044707       0.133333      -0.164102   :      2     0     2     -1
        0.160559      -0.399398      -0.032262   :      2     0     2     -2
        0.012669      -0.111020      -0.018537   :      3     0     2      0
...
```

```orca
Energy levels:  cm-1      eV      Boltzmann populations for T = 300.00  K

   0 :         0.000     0.0000         2.00e-01
   1 :         0.000     0.0000         2.00e-01
   2 :         0.018     0.0000         2.00e-01
   3 :         0.021     0.0000         2.00e-01
   4 :         0.026     0.0000         2.00e-01

--------------------------------------------------------------------------------------------------------
      SOC CORRECTED ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS
--------------------------------------------------------------------------------------------------------
      Transition         Energy     Energy  Wavelength fosc(D2)      D2       |DX|      |DY|      |DZ|
                          (eV)      (cm-1)    (nm)  (*population)  (au**2)    (au)      (au)      (au)
--------------------------------------------------------------------------------------------------------
  0-5.0A  ->  1-5.0A    0.000000       0.0     0.0   0.000000000   0.00000   0.00000   0.00000   0.00000
  2-5.0A  ->  3-5.0A    0.000000       0.0  2927278012.6   0.000000000   0.00000   0.00000   0.00000   0.00000
  3-5.0A  ->  4-5.0A    0.000001       0.0  2013441147.3   0.000000000   0.00000   0.00000   0.00000   0.00000
  2-5.0A  ->  4-5.0A    0.000001       0.0  1192923906.3   0.000000000   0.00000   0.00000   0.00000   0.00000
  1-5.0A  ->  2-5.0A    0.000002       0.0  559585326.1   0.000000000   0.00000   0.00000   0.00000   0.00000
  0-5.0A  ->  2-5.0A    0.000002       0.0  554991701.4   0.000000000   0.00000   0.00000   0.00000   0.00000
  1-5.0A  ->  3-5.0A    0.000003       0.0  469780906.9   0.000000000   0.00000   0.00000   0.00000   0.00000
  0-5.0A  ->  3-5.0A    0.000003       0.0  466539107.5   0.000000000   0.00000   0.00000   0.00000   0.00000
  1-5.0A  ->  4-5.0A    0.000003       0.0  380906816.8   0.000000000   0.00000   0.00000   0.00000   0.00000
  0-5.0A  ->  4-5.0A    0.000003       0.0  378772788.3   0.000000000   0.00000   0.00000   0.00000   0.00000
  4-5.0A  ->  5-5.0A   715.072294 5767447.6     1.7   0.000853852   0.00024   0.00000   0.01494   0.00454
  3-5.0A  ->  5-5.0A   715.072294 5767447.6     1.7   0.000001143   0.00000   0.00021   0.00018   0.00050
  2-5.0A  ->  5-5.0A   715.072295 5767447.6     1.7   0.000001245   0.00000   0.00024   0.00053   0.00012
  1-5.0A  ->  5-5.0A   715.072297 5767447.6     1.7   0.000000330   0.00000   0.00000   0.00029   0.00010
  0-5.0A  ->  5-5.0A   715.072297 5767447.6     1.7   0.000024144   0.00001   0.00000   0.00251   0.00076
  4-5.0A  ->  6-5.0A   715.089740 5767588.3     1.7   0.000002661   0.00000   0.00067   0.00036   0.00042
  3-5.0A  ->  6-5.0A   715.089741 5767588.3     1.7   0.000008083   0.00000   0.00000   0.00145   0.00045
  2-5.0A  ->  6-5.0A   715.089742 5767588.3     1.7   0.000775076   0.00022   0.00001   0.01423   0.00432
  1-5.0A  ->  6-5.0A   715.089744 5767588.4     1.7   0.000000497   0.00000   0.00002   0.00015   0.00035
  0-5.0A  ->  6-5.0A   715.089744 5767588.4     1.7   0.000001537   0.00000   0.00056   0.00035   0.00007
  4-5.0A  ->  7-5.0A   715.115140 5767793.2     1.7   0.000001500   0.00000   0.00027   0.00020   0.00056
  3-5.0A  ->  7-5.0A   715.115141 5767793.2     1.7   0.000834113   0.00024   0.00001   0.01476   0.00449
  2-5.0A  ->  7-5.0A   715.115141 5767793.2     1.7   0.000008694   0.00000   0.00002   0.00150   0.00050
  1-5.0A  ->  7-5.0A   715.115143 5767793.2     1.7   0.000000562   0.00000   0.00026   0.00025   0.00018
  0-5.0A  ->  7-5.0A   715.115143 5767793.2     1.7   0.000003341   0.00000   0.00036   0.00031   0.00085
  4-5.0A  ->  8-5.0A   715.184940 5768356.2     1.7   0.000000146   0.00000   0.00004   0.00020   0.00001
  3-5.0A  ->  8-5.0A   715.184940 5768356.2     1.7   0.000019943   0.00001   0.00206   0.00012   0.00120
  2-5.0A  ->  8-5.0A   715.184941 5768356.2     1.7   0.000019954   0.00001   0.00119   0.00064   0.00197
  1-5.0A  ->  8-5.0A   715.184943 5768356.2     1.7   0.000507851   0.00014   0.00004   0.01152   0.00348
  0-5.0A  ->  8-5.0A   715.184943 5768356.2     1.7   0.000022305   0.00001   0.00003   0.00240   0.00077
  4-5.0A  ->  9-5.0A   715.206052 5768526.4     1.7   0.000049980   0.00001   0.00006   0.00360   0.00113
  3-5.0A  ->  9-5.0A   715.206053 5768526.4     1.7   0.000007590   0.00000   0.00077   0.00040   0.00119
...
```

The obtained spectra can be prepared for ploting with the use of `orca_mapspc`.
Check section [sec:utilities.mapspc](#sec:utilities.mapspc) for details.

<a id="sec:spectroscopyproperties.rocis.rixs"></a>
## Resonant Inelastic Scattering Spectroscopy

<a id="sec:spectroscopyproperties.rocis.rixs.general"></a>
### General

Starting from ORCA version 4.0 ROCIS module can be used to calculate
RIXS spectra

The present implementation is directly based on the Kramers Heisenerg
Dirac (KDH) expression formula for near resonant and resonant conditions

$$

\left|{ {\alpha _{\rho \lambda } }({E_{ex} },{E_{sc} }) } \right|_{Total}^2 = { \sum\limits_F { \left|{ \sum\limits_V { \frac{{\left\langle F \right|{ m_\rho }\left| V \right\rangle\left\langle V \right|{ m_\lambda }\left| I \right\rangle} }{{{E_{VI} } - { E_{ex} } - i\frac{1}{2}{\Gamma _V} }} } } \right|} ^2}\left\{{ \frac{{{\Gamma _F} }}{{{{({E_{FV} } - { E_{ex} } + { E_{sc} }) }^2} + \frac{1}{4}{\Gamma _F}^2} }} \right\}

$$

$$

\left|{ {\alpha _{\rho \lambda } }({E_{ex} },{E_{sc} },V) } \right|_{resonant}^2 = \sum\limits_F { {{\left|{ \left\langle F \right|{ m_\rho }\left| V \right\rangle} \right|}^2}{{\left|{ \left\langle V \right|{ m_\lambda }\left| I \right\rangle} \right|}^2} } f({E_{VI} },{E_{FV} },{E_{ex} },{E_{sc} },{\Gamma _V},{\Gamma _F})

$$

$$

\left|{ {\alpha _{\rho \lambda } }({E_{VI} },{E_{sc} }) } \right|_{Direct}^2 = \sum\limits_V { \left|{ {\alpha _{\rho \lambda } }({E_{VI} },{E_{sc} },V) } \right|_{resonant}^2}

$$

The resonance scattering cross section for total and direct cases,
averaged over all orientations of the molecule and integrated over all
directions and polarizations of scattered radiation is given in
equations:

$$

\sigma _{_{RXES} }^{Total}({E_{ex} },{E_{sc} }) = \frac{{8\pi E_{sc}^3{E_{ex} }} }{{9{c^4} }}\sum\limits_{\rho ,\lambda  = x,y,z} { \left|{ {\alpha _{\rho \lambda } }({E_{ex} },{E_{sc} }) } \right|_{Total}^2}

$$

$$

\sigma _{_{RXES} }^{Direct}({E_{ex} },{E_{sc} }) = \frac{{8\pi E_{sc}^3{E_{ex} }} }{{9{c^4} }}\sum\limits_{\rho ,\lambda  = x,y,z} { \left|{ {\alpha _{\rho \lambda } }({E_{ex} },{E_{sc} }) } \right|_{Direct}^2}

$$

Interference effects can be then derived in a straightforward way from
equation:

$$

\sigma _{RXES}^{interference}(E_{ex}^{},E_{sc}^{}) = \sigma _{RXES}^{Total}(E_{ex}^{},E_{sc}^{}) - \sigma _{RXES}^{Direct}(E_{ex}^{},E_{sc}^{})

$$

In order to access RIXS spectroscopy in the ROCIS module one needs in
addition to specify a 2nd donor space. This is specified by defining an
OrbWin array with 6 elements: The first four elements define the ranges
of the two donor spaces while the last two elements the respective
acceptor space range.

```orca
OrbWin = 0,0,2,4,45,60
```

An important difference with respect to the conventional ROCIS or
DFT/ROCIS calculations is the fact that two donor spaces of very
different energy ranges are involved (e.g. K-edge, L-edge) which
requires to restrict somewhat the acceptor space and saturate it with as
many states as possible.

The main calling commands in order to perform a RIXS calculation within
both ROCIS and CASSCF blocks are the following:

-   DoRIXS true. Similar to absorption spectroscopy, this requests the
    RIXS calculation to be performed based on the calculated
    non-relativistic ground state multiplicity States

-   DoRIXSSOC true. By turning-on this flag the RIXS is calculated by
    taking in account the relativistically corrected Ms States.

-   DoElastic true. This flag indicates whether the resonant condition in
    which the initial and Final states coincide should be taken into
    account. Note that the intensity of this spectral feature might be
    overestimated as presently the non resonant terms are not treated

The respective ROCIS input reads then as follows:

```orcainput
!B3LYP def2-TZVP def2-TZVP/C

%ROCIS
  NRoots 200
  MaxCore 4048
  DoRI true
  DoHigherMult true
  DoDFTCIS true
  DFTCIS_c =0.18,0.20,0.40
  OrbWin = 2,4,25,33,0,100
  rel
    DoSOC true
    DoRIXS true    # Request RIXS calculation (NoSOC)
    DoRIXSSOC true # Request RIXS calculation (with SOC)
    DoElastic true # Request RIXS calculation (Elastic)
  end
end
* xyzfile 2 2 test.xyz
```

When running the calculation one can monitor if the requested NRoots
were sufficient enough to select the states dominated by both the donor
orbital spaces

```orca
--------------------------------------------------------------------------------
ROOT    Mult      Excitation energy[Eh]           [cm-1]          [eV]
--------------------------------------------------------------------------------
0       2            0.00000000                      0.00          0.000
1       2            0.06611737                  14511.08          1.799
2       2            0.07728471                  16962.03          2.103
3       2            0.07732428                  16970.72          2.104
...
84       2            33.75471831                7408304.35        918.513
85       2            33.77073325                7411819.22        918.948
86       2            33.77076955                7411827.19        918.949
87       4            34.06882971                7477243.83        927.060
88       2            34.07021441                7477547.74        927.098
...
```

If that is not the case the respective RIXS calculations will not be
performed and a Warning Message will be generated:

```orca
Making the RIXS files ...
WARNING!: Flag for RIXS property calculation was identified but
there is zero number of Intermediate  and/or Final states:
No Cross-Section properties will be evaluated ...Skipping this part
TIP: Increase the number of NRoots and/or decrease or increase 
the acceptor orbital space
...Done
```

A successful run on the other hand will generate the following messages
for RIXS and RIXSSOC calculations.

```orca
----------------------------------------------------------------------------------
ROCIS RIXSSOC SPECTRUM                             
----------------------------------------------------------------------------------

Making the RIXS-SOC data files for Inelastic and Elastic Scattering
Ms States:                  2
Intermediate States:        78
Final States:               214
The RIXS cross section will be generated from:          
432 Ground-Final State Pairs and   78 Intermediate States/Pair

Calculating Intensities...
10% done
20% done
30% done
40% done
50% done
60% done
70% done
80% done
90% done
100% done

Storing the files...All Done
----------------------------------------------------------------------------------
```

In both cases the number of involved Initial, Final and Intermediate
states is specified explicitly.

For example in the case of RIXSSOC 2 Ms Ground states, 78 Intermediate
states and 214 Final states are involved. Then the RIXS cross section
for elastic and inelastic scattering will be generated by 432
(2\*(2+214)) Ground-Final State-Pairs and 78 Intermediate States per
Ground-Final state pair.

<a id="sec:spectroscopyproperties.rocis.rixs.mapspc"></a>
### Processing the spectra with `orca_mapspc` 

By calling `orca_mapspc` with the following keywords:

```orca
orca_mapspc test.el_inel.rocis.rixssoc RIXS -x0871 -x1876 -x2-1 -x34 -w0.4 -g0.4
	-l -n125 -m125 -dx20 -eaxis1
```

The program will process the `test.el_inel.rocis.rixssoc` file with the
following parameters:

Energy range along x : 871-876 eV

Energy range along y: -1-34 eV

-l indicates Lorentzian broadening

Width along x (gamma): 0.4 eV

Width along y (gamma): 0.4 eV

Points along x: 125

Points along y:125

Shift to be applied along Incident energy/Emission axis: 20 eV

The y axis will be Energy Transfer axis. If -eaxis2 is the y axis will
be then Emission Energy axis

All this information is printed during the data processing:

```orca
Mode is RIXS
Using Lorentzian shape
Cannot read the paras.inp file ... 
taking the line width parameter from the command line 
Cannot read the udex.inp file ... 
taking the excitation energy ranges from the command line 
Cannot read the udem.inp file ... 
taking the emission energy ranges from the command line 
Cannot read the gfsp.inp file ... 
No Ground-Final State Pairs will be evaluated 
---------------------------------------------------------------------------------
PLOTTING RIXS SPECTRA
---------------------------------------------------------------------------------
Input File : test.el_inel.rocis.rixssoc
Incident Energy Excitation axis :   871.000 ...   876.000 eV  125 points
Energy transfer axis            :    -1.000 ...     4.000 eV  125 points
Incident Energy Shift         :    20.000 eV
Lorenzian Linewidth along Incident Axis                   :     0.400 eV
Lorenzian Linewidth along Energy Transfer/Emission Axis   :     0.400 eV
y axis  :     1 -> Energy transfer 
Number of user defined cuts at constant Excitation Energy axis:    0 
Number of user defined cuts at constant Emission/Energy Transfer Energy axis  : 0 

Making checks...Done

Proccessing data...
10% done
20% done
...
100% done

RIXS-plotting done
Incident Energy range:            845.800 ...   869.249
Emission/Energy-transfer range:     0.000 ...     4.853

Now storing the 2D file...
Done

Making the Integrated spectra along Energy Transfer/Emission axis... Done

Making the Integrated spectra along Incident axis... Done

All Done
---------------------------------------------------------------------------------
```

Successful run will generate the following files: The RIXS planes of the
Total, Direct and Interference RIXS intensity as indicated in the above
equations:

```orca
test.el_inel.rocis.rixssoc.total_rixs.dat
test.el_inel.rocis.rixssoc.direct_rixs.dat
test.el_inel.rocis.rixssoc.interference_rixs.dat
```

In addition one obtains the integrated spectra at constant Incident
energies (CIE):

```orca
test.el_inel.rocis.rixssoc.dw.dat
```

as well as at constant Emission/Energy Transfer energies (CEE/CET):

```orca
test.el_inel.rocis.rixssoc.wex.dat
```

<a id="fig:ROCIS_RIXS"></a>
*DFT/ROCIS calculated RIXS planes for ${[Cu{(N{H_3})_4}]^{2 - } }$.
Left: Total RIXS Intensity, Middle: Direct RIXS intensity and Right:
Interference RIXS intensity. Lorentzian lineshape broadening with
constant widths along Incident and Energy Transfer axis (0.5 and 0.2 eV
respectively) were used
throughout.*

<a id="sec:spectroscopyproperties.rocis.rixs.cut"></a>
### Generating Cuts

Cuts along x and y axis can be generated with two ways:

1\) At first, this action can be performed by adding the following
keywords: `uex` and `udw` accounting for generating cuts at constant
Incident Energies (CIE) and at constant Emission (CEE)/or at constant
Energy Transfer (CET) respectively, together with the desired number of
cuts.

2\) Alternatively, the energies of the desired cuts can be specified as
lists in the files udex.inp (user defined excitations) udem.inp (user
defined emissions)

For example if in udex.inp one specifies:

```orca
872.5 
874.2
```

and for the cuts along Energy Transfer axis one just specify -udw3

```orca
orca_mapspc test.el_inel.rocis.rixssoc RIXS -x0871 -x1876 -x2-1 -x34 -w0.4 -g0.4
	-l -n125 -m125 -dx20 -eaxis1 -udw3
```

Then at the end one gets:

```orca
Making the specified  cuts (2) at constant Excitation Energy axis...
	Writing file: test.el_inel.rocis.rixssoc_872.50.rxes_vs.dat  ...Done
	Writing file: test.el_inel.rocis.rixssoc_872.50.rxes_fs.dat  ...Done
	Writing file: test.el_inel.rocis.rixssoc_874.20.rxes_vs.dat  ...Done
	Writing file: test.el_inel.rocis.rixssoc_874.20.rxes_fs.dat  ...Done
	Done
	
	Making the specified cuts (3) at constant Emission/Energy Transfer axis...
	Writing file: test.el_inel.rocis.rixssoc_-1.00.xas_vs.dat  ...Done
	Writing file: test.el_inel.rocis.rixssoc_-1.00.xas_fs.dat  ...Done
	Writing file: test.el_inel.rocis.rixssoc_1.50.xas_vs.dat  ...Done
	Writing file: test.el_inel.rocis.rixssoc_1.50.xas_fs.dat  ...Done
	Writing file: test.el_inel.rocis.rixssoc_4.00.xas_vs.dat  ...Done
	Writing file: test.el_inel.rocis.rixssoc_4.00.xas_fs.dat  ...Done
	Done
	All Done
	------------------------------------------------------------------
```

The files `*_rxes_fs.dat` are RXES spectra containing all individual
contributions from all Final states together with the Direct, the Total
and the Interference contributions at the given constant Incident
Energy.

Similarly, the `*_rxes_vs.dat` are RXES spectra containing individual
contributions of the Intermediate states, together with the Direct the
Total and the Interference contributions at the given constant Incident
Energy

Likewise, the respective `*_xas_fs.dat` and `*_xas_vs.dat` are XAS type
spectra with individual contributions at a given constant Emission or
Energy transfer Energy

These files are Energy vs Intensity files and read like:

1\) for `*fs.dat`

```orca
X     S-  1(  0- 0)      S-  2(  0- 1)       DIRECT       TOT       INTERFERENCE
```

2\) for `*vs.dat`

```orca
X     S-  1(  45)        S-  2(  47)         DIRECT       TOT       INTERFERENCE
```

In the first case S -1(0-0) represents the individual contribution of a
given Ground-Final state pair. The numbering follows the numbering of
the output file e.g.:

```orca
Eigenvalues:     cm-1         eV      Boltzmann populations at T =  300.000 K
	0:          0.0000     0.0000         3.44e-01
	1:          8.3818     0.0010         3.31e-01
```

Hence, in this case S -1 represents the elastic scattering intensity.

In the second case S -1(45) represents the individual contribution of a
given Intermediate state.

```orca
44:      66918.6071     8.2968         1.43e-140
45:    6996678.8061   867.4775         0.00e+00
46:    6996693.0276   867.4793         0.00e+00
```

In this case S -1 represents the intensity contribution of the first
Intermediate state.

Starting from ORCA 4.2 in every RIXS requested calculation the Off
resonant XES spectrum is automatically generated in every RIXS requested
calculation.

```orca
----------------------------------------------------------------------------------
ROCIS RIXS SPECTRUM                             
----------------------------------------------------------------------------------

Making the RIXS data files for Inelastic and Elastic Scattering
Ground State:                  1
Intermediate States:           28
Final States:                  588
The RIXS cross section will be generated from:          
589 Ground-Final State Pairs and   28 Intermediate States/Pair
The Off-Resonance XES spectrum will be printed

Calculating Intensities...
10% done
20% done
30% done
40% done
50% done
60% done
70% done
80% done
90% done
100% done

Printing the XES spectrum and Storing the files...
-----------------------------------------------------------------------------
X-RAY EMISSION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS
-----------------------------------------------------------------------------
Transition          Energy           INT             TX        TY        TZ 
(eV)           (fosc)          (au)      (au)      (au)
-----------------------------------------------------------------------------
1  589 ->    0      6403.377     0.000000000721     0.00000   0.00000   0.00000
2  590 ->    0      6403.380     0.000000000083    -0.00000   0.00000   0.00000
3  591 ->    0      6403.685     0.000873238810     0.00236   0.00000   0.00000
4  592 ->    0      6404.766     0.000000000154     0.00000   0.00000   0.00000
5  593 ->    0      6408.288     0.000000006850    -0.00001   0.00000   0.00000
6  594 ->    0      6408.295     0.000034710300    -0.00047   0.00000   0.00000
...
16490  614 ->  588  6387.989     0.000000000000     0.00000   0.00000   0.00000
16491  615 ->  588  6388.222     0.000000000000     0.00000   0.00000   0.00000
16492  616 ->  588  6388.881     0.000000000000     0.00000   0.00000   0.00000
All Done
-----------------------------------------------------------------------------
```

Hence also the myfile-rixs.out file can also be processed with the
`orca_mapspc` to generate the respective XES spectra:

```orca
orca_mapspc myfile_rixs.out XES/XESSOC -x06000 -x16500 -w2.0 -eV -n10000
```

<a id="sec:spectroscopyproperties.rocis.magProp"></a>
## ROCIS Magnetic Properties

Several magnetic properies are availiable in the ROCIS method Including
g-tensors (G-Matrix), zero field splittings (ZFS), hyperfine couplings
(HFCs) and electric field gradients (EFGs).

The g-tensors as well as the zfs are calculated on the basis of the
Effective Hamiltonian as well in the sum over states (SOS) framework.
HFCs are calculated in the SOS framework while EFGs are calculated as
expectation values. Please consult also the respective discussion in the
MRCI chapter (section
[sec:modelchemistries.mrci](#sec:modelchemistries.mrci))

```orca
...
DoHeff true    # Requests calculation of G-tenosrs and ZFS 
               # in the effective Hamiltonian framework
DoEPR true     # Requests calculation of G-tenosrs, ZFS and HFCs
               # in the Sum over states (SOS) framework
AtensorNuc 0   # Nuclei to account for the HFCs calculation
NAtensors 1    # How many Nuclei are included in the HFCs calculation
ATensor 0      # Nucleus to calculate HFCs and EFGs
NDoubGtensor 1 # Kramers doublets to account for the g tensor calculations
...
```

This will enter the calculation in the ROCIS Spin Hamiltonian section

```orca
--------------------------------------------------------
ROCIS SPIN HAMILTONIAN PROPERTIES           
--------------------------------------------------------
```

<a id="sec:spectroscopyproperties.rocis.natTransOrb"></a>
## Natural Transition Orbitals/ Natural Difference Orbitals

Likewise to CIS and TD-DFT (section
[sec:spectroscopyproperties.tddft.natTransOrb](#sec:spectroscopyproperties.tddft.natTransOrb)) The nature of the
calculated excited states in ROCIS and DFT/ROCIS can be analyzed by
using the Natural Transition Orbitals (NTO) or Natural Difference
Orbitals (NDO) machineries.[felix2014](../../bibliography.md) 

!!! note
    -   The NTO analysis is based on the transition density between ground
        and excited states. Hence is valid for singly excited states and for
        states of the same multiplicity.

    -   The NDO analysis on the otherhand is somewhat more flexible in this
        respect as it is based on the difference density between ground and
        excited states.

    -   Presently, only one analysis (NTO or NDO) can be performed at a time
        while when both flags are on the NTO analysis switches off.

To request for NTOs or NDOs the user needs to provide which states are
to be calculated:

```orca
DoNTO true
NTOStates = 1,2,3,4,5,6,7,8,9,10,13,14,15
```

```orca
DoNDO true
NDOStates = 1,2,3,4,5,6,7,8,9,10,13,14,15
```

Which gives:

```orca
------------------------------------------
NATURAL TRANSITION ORBITALS FOR STATE   14
------------------------------------------

done
Solving eigenvalue problem for the Occupied space  ... done
Solving eigenvalue problem for the Acceptor space   ... done
Natural Transition Orbitals were saved in nto.14.nto
Threshold for printing occupation numbers 1.0e-04

E=  25.447756 au    692.469 eV  5585137.0 cm**-1
49[0] ->  46[1]  : n=  0.39056909
48[0] ->  47[1]  : n=  0.08619374
47[0] ->  48[1]  : n=  0.00441125
```

```orca
-------------------------------------------------
NATURAL DIFFERENCE ORBITALS FOR STATE   14
-----------------------------------------------

done
Solving eigenvalue problem for the Occupied space  ... done
Solving eigenvalue problem for the Acceptor space   ... done
Natural Difference Orbitals were saved in ndo.14.ndo
Threshold for printing occupation numbers 1.0e-04

E=  25.447756 au    692.469 eV  5585137.0 cm**-1
49[0] ->  46[1]  : n=  0.81173217
48[0] ->  47[1]  : n=  0.17903699
47[0] ->  48[1]  : n=  0.01165859
46[0] ->  49[1]  : n=  0.00922738
45[0] ->  50[1]  : n=  0.00112567
```

For closed shell cases the orbitals are save in similar way to TDDFT and
CIS (section [sec:spectroscopyproperties.tddft.natTransOrb](#sec:spectroscopyproperties.tddft.natTransOrb)).
In the case of open shell
cases for convenience donor orbitals are saved with orbital operator 0
while acceptor orbitals with orbital operator 1. This needs to be
specified in the `orca_plot` program and should not be confused with the
`spin-up` and `spin-down` orbitals in the UHF and UKS cases.

<a id="sec:spectroscopyproperties.rocis.keywords"></a>
## Keyword List

<a id="tab:spectroscopyproperties.rocis.keywords"></a>
!!! note "`%rocis` block input keywords."
    :class: footnotesize
    | Keyword                          | Option / Value            | Description                                                                                         |
    |:---------------------------------|:--------------------------|:----------------------------------------------------------------------------------------------------|
    | `DoGenROCIS`                     | `true`                    | Requests the GS-ROCIS method (default: `false`).                                                    |
    | `ReferenceMult`                  | `1`                       | Sets the multiplicity for the reference CSF for the GS-ROCIS method.                                |
    | `NRoots`                         | `5`                       | The number of desired roots.                                                                        |
    | `MaxDim`                         | `25`                      | Davidson expansion space = MaxDim * NRoots.                                                         |
    | `MaxIter`                        | `100`                     | Maximum CI Iterations.                                                                              |
    | `NGuessMat`                      | `512`                     | The dimension of the guess CI matrix.                                                               |
    | `ETol`                           | `1e-6`                    | Energy convergence tolerance.                                                                       |
    | `RTol`                           | `1e-6`                    | Residual Convergence tolerance.                                                                     |
    | `MaxCore`                        | `4096`                    | Maximum memory used by the ROCIS moduleduring the calculation in MB.                                |
    | `EWin =`                         | `-5,5-5,5`                | Energy Window that defines orbital excitation space.                                                |
    | `OrbWin =`                       | `6,8,0,2000`              | Orbital Window that defines orbital excitation space (overrides EWin).                              |
    | `DoLoc`                          | `true`                    | Switch for localization of Donor orbital space (default: `false`).                                  |
    | `LocOrbWin =`                    | `6,11`                    | Obital window for the localization scheme.                                                          |
    | `LocMet`                         | `PipekMezey` `PM`         | Chooses the Pipek Mezey localization method.                                                        |
    |                                  | `FosterBoys` `FB`         | Chooses the Foster Boys localization method.                                                        |
    | `DoPNO`                          | `true`                    | Performs the calculation in the PNO-ROCIS framework (default: `false`).                             |
    | `TCutPNO`                        | `1e-16`                   | Threshold for PNO selection.                                                                        |
    | `XASelems`                       | `0,2`                     | Selects from which atoms are the core MOs going to be used in the PNO procedure.                    |
    | `LocMet`                         | `PipekMezey` `PM`         | Chooses the Pipek Mezey localization method.                                                        |
    |                                  | `FosterBoys` `FB`         | Chooses the Foster Boys localization method.                                                        |
    | `DoNTO`                          | `true`                    | Request Natural Transition Orbital Analysis (default: `false`)                                      |
    | `NTOThresh`                      | `1e-4`                    | Threshold for printing occupation numbers.                                                          |
    | `NTOStates =`                    | `1,2`                     | Array input for states to be taken into account.                                                    |
    | `DoNDO`                          | `true`                    | Request Natural Difference Orbital Analysis (default: `false`)                                      |
    |                                  |                           | (if true it switches off the NTO analysis)                                                          |
    | `NDOThresh`                      | `1e-4`                    | Threshold for printing occupation numbers.                                                          |
    | `NDOStates =`                    | `1,2`                     | Array input for states to be taken into account.                                                    |
    | `PrintLevel`                     | `3`                       | Controls the amount of output produced during the calculation.                                      |
    | `Do_is`                          | `true`                    | Include DOMO->SOMO excitations.                                                                     |
    | `Do_sa`                          | `true`                    | Include SOMO->Virtual excitation.                                                                   | 
    | `Do_ia`                          | `true`                    | Include DOMO->Virtual excitations.                                                                  |
    | `Do_ista`                        | `true`                    | Include DOMO->SOMO excitations coupled to SOMO->Virtual excitations with s$\neq{}$t.                |
    | `Do_isa`                         | `true`                    | Include DOMO->SOMO excitations coupled to SOMO->Virtual excitations with s$=$ t.                    |
    |                                  |                           | (only used in the original ROCIS implementation)                                                    |
    | `DoLowerMult`                    | `true`                    | Switch for excitation with S’=S-1.                                                                  |
    | `Do_LM_is`                       | `true`                    | Include DOMO->SOMO excitations with S’=S-1.                                                         |
    | `Do_LM_sa`                       | `true`                    | Include SOMO->Virtual excitations with S’=S-1.                                                      |
    | `Do_LM_ia`                       | `true`                    | Include DOMO->Virtual excitations with S’=S-1.                                                      |
    | `Do_LM_ss`                       | `true`                    | Include SOMO->SOMO excitations with S’=S-1.                                                         |
    | `DoHigherMult`                   | `true`                    | Switch for excitations with S’=S+1.                                                                 |
    | `Do_HM_is`                       | `true`                    | Include DOMO->SOMO excitations with S’=S+1.                                                         |
    | `Do_HM_sa`                       | `true`                    | Include SOMO->Virtual excitations with S’=S+1.                                                      |
    | `Do_HM_ia`                       | `true`                    | Include DOMO->Virtual excitations with S’=S+1.                                                      |
    | `DoCD`                           | `true`                    | Request circular dichroism calculation.                                                             |
    | `DoDipoleLength`                 | `true`                    | Request the use of electric moments in a length formulation (default: `false`).                     |
    | `DoDipoleVelocity`               | `true`                    | Request the use of electric moments in a velocity formulation (default: `false`).                   |
    | `DoFullSemiclassical`            | `true`                    | Request the calculation of complete semiclassical multipolar moments (default: `false`).            |
    | `DecomposeFosc`                  | `true`                    | Request the decomposition of the oscillator strengths in a multipolar expansion. (default: `false`) |
    | `PlotDiffDens =`                 | `1,2`                     | Array input for plotting difference densities of CI roots to the ground state.                      |
    | `PlotSOCDiffDens =`              | `1,2`                     | Array input for plotting difference densities of SOC states to the ground state.                    |
    | `TPrint`                         | `0.01`                    | Threshold for contributions to CI and SOC states to be printed.                                     |
    | `rel`                            |                           | Signals the begining of the relativistic block.                                                     |
    | `DoSOC`                          | `true`                    | Requests the inclusion of spin-orbit coupling (part of the `rel` block).                            |
    | `DoMCD`                          | `true`                    | Requests the calculation of MCD spectra (part of the `rel` block).                                  |
    | `B`                              | `30000`                   | Sets external magnetic field (part of the `rel` block).                                             |
    | `Temperature`                    | `5`                       | Sets the temperature for the SOC spectra (part of the `rel` block).                                 |
    | `DoRIXS`                         | `true`                    | Requests a RIXS calculation (part of the `rel` block).                                              |
    | `DoRIXSSOC`                      | `true`                    | Perform a RIXS calculation on the basis of SOC corrected states (part of the `rel` block).          |
    | `DoElastic`                      | `true`                    | Include the elastic line in the generation of the RIXS or RIXSSOC spectra (part of the `rel` block).|

