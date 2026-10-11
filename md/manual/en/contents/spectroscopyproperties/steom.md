```{index} STEOM
```

(sec:spectroscopyproperties.steom)=
# Excited States via STEOM-CCSD

```{index} Excited States via STEOM
```

The EOM-CCSD approach for excitation energies becomes prohibitively
costly for large systems because of its O($N^{6}$) scaling. Therefore,
one needs a more compact form of the wave-function ansatz. A second
similarity transformation can compress the final matrix diagonalization
step to the CIS space only. The resulting STEOM-CCSD method of Marcel
Nooijen and co-workers {cite}`Rodney1997JCP` is an efficient way for accurate calculations of
excitation energies.

(sec:spectroscopyproperties.steom.general)=
## General Description

In the standard EOM-CC method, the transformed Hamiltonian is
diagonalized over a singles and doubles space to obtain ionized,
attached, or excited states of the reference state. In STEOM-CC, one
performs a second similarity transformation

$$\begin{aligned}
\hat{G}=\{e^{\hat{S} }\}^{-1}\hat{\bar{H} }\{e^{\hat{S} }\}\end{aligned}$$

The transformation operator $\hat{S}$, including singles and doubles, is
defined as

$$\begin{aligned}
\hat{S}=\hat{S}^{IP}+\hat{S}^{EA},\end{aligned}$$

$$\begin{aligned}
\hat{S}^{IP}=S_{i^{\prime} }^{m}\hat{E}^{m}_{i^{\prime} }+\dfrac{1}{2}S^{mb}_{ij}\hat{E}^{mb}_{ij},\end{aligned}$$

$$\begin{aligned}
\hat{S}^{EA}=S^{a^{\prime} }_{e}\hat{E}_{e}^{a^{\prime} }+\dfrac{1}{2}S^{ab}_{ej}\hat{E}^{ab}_{ej}.\end{aligned}$$

In the above equations, $m$ and $e$ denote active indices of the hole
and particle type respectively, while a prime denotes a restriction to
orbitals that are not active. The amplitudes of the operator $\hat{S}$
are defined in such a way that matrix elements of the transformed
Hamiltonian, in second quantized notation, become equal to zero.

$$\begin{aligned}
g_{i^{\prime} }^{m}=g_{ij}^{mb}=g^{a^{\prime} }_{e}=g^{ab}_{ej}=0\end{aligned}$$

In addition, the zeros which pre-existed in $\bar{H}$, after solving the
CCSD equations, remain preserved. The above equations are linear in
$\hat{S}$ and are equivalent to the Fock space multireference coupled
cluster equations for the one valence problem. However, to ensure
numerical stability, the equations are re-casted as matrix
diagonalization problem and solved as IP-EOM-CCSD and EA-EOM-CCSD
problems. The $\hat{S}^{IP}$ and $\hat{S}^{EA}$ are then extracted from
the converged previous calculations, respectively, by
invoking intermediate normalization on the suitably chosen eigenvectors
corresponding to active holes and active particles. The total process
can be described as following

-   Solution of the ground state coupled cluster equations

-   Construct the first similarity transformed Hamiltonian as
    $\hat{\bar{H} }=e^{-\hat{T} }\hat{H}e^{\hat{T} }$

-   Solution of the IP-EOM and EA-EOM equations

-   Extraction of the $\hat{S}$ amplitudes

-   Construct the second similarity transformed Hamiltonian as
    $\hat{\bar{G} }=e^{-\hat{S} }\hat{\bar{H} }e^{\hat{S} }$

-   Diagonalization of $\hat{\bar{G} }$ in CIS space

The advantage of the above method is that, instead of one iterative
O($N^{6}$) scaling diagonalization step, it requires two iterative
O($N^{5}$) scaling steps, one non-iterative O($N^{5}$) scaling step and
one iterative O($N^{4}$) scaling matrix diagonalization step. The
presence of so-called 'implicit triples excitation' term ensures the charge
transfer separability of the excited states, which is absent in
EOM-CCSD. In addition, since the final diagonalization step is performed
in a CIS space, the spin adaption is trivial and excited states of
triplet multiplicity can be obtained without going through the
complications of a spin orbital based implementation.

The STEOMCC approach has also recently been extended for applications to
open-shell systems within the UHF formalism {cite}`huntington2017UHFSTEOM` {cite}`casanova_neese_2024`.
In this case, the expressions for the operators $\hat{S}^{IP}$ and
$\hat{S}^{EA}$ take the form,

$$\begin{aligned}
\hat{S}^{IP}&=\frac{1}{2}\sum_{i,e,a,b}s_{ie}^{ab}\big\{\hat{a}^{\dagger}\,\hat{b}^{\dagger}\,\hat{e}\,\hat{i}\big\}+\sum_{\bar{i},e,\bar{a},b}s_{\bar{i}e}^{\bar{a}b}\big\{\hat{\bar{a} }^{\dagger}\,\hat{b}^{\dagger}\,\hat{e}\,\hat{\bar{i} }\big\}\nonumber\\
&+\frac{1}{2}\sum_{\bar{i},\bar{e},\bar{a},\bar{b} }s_{\bar{i}\bar{e} }^{\bar{a}\bar{b} }\big\{\hat{\bar{a} }^{\dagger}\,\hat{\bar{b} }^{\dagger}\,\hat{\bar{e} }\,\hat{\bar{i} }\big\}+\sum_{i,\bar{e},a,\bar{b} }s_{i\bar{e} }^{a\bar{b} }\big\{\hat{a}^{\dagger}\,\hat{\bar{b} }^{\dagger}\,\hat{\bar{e} }\,\hat{i}\big\},\\
\widehat{S}_{-}&=\frac{1}{2}\sum_{i,j,a,m}s_{ij}^{am}\big\{\hat{a}^{\dagger}\,\hat{m}^{\dagger}\,\hat{j}\,\hat{i}\big\}+\sum_{\bar{i},j,\bar{a},m}s_{\bar{i}j}^{\bar{a}m}\big\{\hat{\bar{a} }^{\dagger}\,\hat{m}^{\dagger}\,\hat{j}\,\hat{\bar{i} }\big\}\nonumber\\
&+\frac{1}{2}\sum_{\bar{i},\bar{j},\bar{a},\bar{m} }s_{\bar{i}\bar{j} }^{\bar{a}\bar{m} }\big\{\hat{\bar{a} }^{\dagger}\,\hat{\bar{m} }^{\dagger}\,\hat{\bar{j} }\,\hat{\bar{i} }\big\}+\sum_{i,\bar{j},a,\bar{m} }s_{i\bar{j} }^{a\bar{m} }\big\{\hat{a}^{\dagger}\,\hat{\bar{m} }^{\dagger}\,\hat{\bar{j} }\,\hat{i}\big\}.\end{aligned}$$

where we use overbars to distinguish the $\beta$ orbitals from the
$\alpha$ orbitals. The amplitudes
$\big\{s_{ie}^{ab}, s_{\bar{i}e}^{\bar{a}b}\big\}$ are determined by
solving the UHF EA-EOM-CCSD equations for the attachment of an $\alpha$
electron, while the
$\big\{s_{\bar{i}\bar{e} }^{\bar{a}\bar{b} }, s_{i\bar{e} }^{a\bar{b} }\big\}$
amplitudes are extracted from a UHF EA-EOM-CCSD calculation for the
attachment of a $\beta$ electron. Similarly, the sets of amplitudes
$\big\{s_{ij}^{am}, s_{\bar{i}j}^{\bar{a}m}\}$ and
$\big\{s_{\bar{i}\bar{j} }^{\bar{a}\bar{b} }, s_{i\bar{j} }^{a\bar{m} }\big\}$
are determined by solving the decoupled UHF IP-EOM-CCSD problems for the
ionization of an $\alpha$ electron and the ionization of a $\beta$
electron, respectively. Hence, an UHF STEOMCC calculation involves two
separate IP calculations (O($N^{5}$) scaling) and two separate EA
calculations (O($N^{5}$) scaling steps).

All the speed up options, including CCSD(2) (only available in RHF
implementation) and COSX, which are available for EOM-CCSD are also
available for STEOMCC. The most important steps in a STEOMCC calculation are
the IP-EOM and EA-EOM calculations. These steps are performed
using the EOM-CCSD module and the relevant keywords are the same as that
described in
{ref}`sec:spectroscopyproperties.eom`. The keywords which are exclusive to the
RHF STEOM module are:

```orca
%mdci
#
#RHF STEOM parameters - defaults displayed
DoCISNat true     # automatic selection of active space       
NActIP  3         # number of states defined as active in the IP calculation
NActEA  2         # number of states defined as active in the EA calculation
DoTriplet false   # target state of triplet multiplicity
DoDbFilter true   # filters out states with doubles excitation  character 
DoNewActSch true  # new active space selection scheme for STEOM-CCSD                             
DoSOLV            # perturbative correction for solvation effects (experimental) 
#
#Default values for automatic active space selection scheme
OThresh 0.001   # Cut off occupation of CIS natural orbitals in IP calculation 
VThresh 0.001   # Cut off occupation of CIS natural orbitals in EA calculation 
IPSThrs 80      #  The percentage singles threshold for the IP calculation
EASThrs 80      #  The percentage singles threshold for the EA calculation
end
```

The keywords pertaining to the UHF STEOM module are:

```orca
%mdci
#UHF STEOM parameters - defaults displayed
DoCISNat true        # automatic selection of active space       
NActIP_a  3          # number of states defined as active in the IP calculation 
                     # for the removal of an α electron
NActIP_b  3          # number of states defined as active in the IP calculation 
                     # for the removal of a β electron
NActEA_a  2          # number of states defined as active in the EA calculation 
                     # for the attachment of an α electron
NActEA_b 2           # number of states defined as active in the EA calculation 
                     # for the attachment of a β electron
DoDbFilter true      # filters out states with doubles excitation  character 
UseQROs  false       # use QROs or not
DoNewActSch true     # new active space selection scheme for STEOM-CCSD                             
#Default values for automatic active space selection scheme
OThresh 0.001        # Cut off occupation of CIS natural orbitals in tIP calculations
VThresh 0.001        # Cut off occupation of CIS natural orbitals in EA calculations 
IPSThrs 80           #  The percentage singles threshold for the IP calculations
EASThrs 80           #  The percentage singles threshold for the EA calculations
end
```

(sec:spectroscopyproperties.steom.active)=
## Selection of Active space

The results of a STEOM-CC calculation depend upon the number of roots
selected as active in the EOMIP and EOMEA calculations. In ORCA, they
are chosen automatically, by using state-averaged CIS natural transition
orbitals (NTO). By default, the number of roots included in this initial
CIS computation is equal to the number of roots requested in STEOM
(`NRoots`). However, this can be modified setting `NRootsCISNAT` to
higher values. The orbitals up to a predefined occupation are then
chosen to be active in the EOMIP and EOMEA calculations, and this is
controlled by the keywords `OThresh` and `VThresh` respectively. Now,
there are two possible ways to chose active space. One is to use the
criteria of percentage occupation of NTO's as described in ref
{cite}`Dutta2017STEOM`. However, a newer and more robust approach is to use
the criteria of absolute occupation, which is default in the current
implementation. One can switch on the old percentage occupation based
active space selection by setting `DoNewActSch` to false (not recommended).

One can also select the active spaces manually by turning the `DoCISNat`
to false and setting the `NActIP` and `NActEA` (RHF STEOM calculation)
or the `NActIP_a`, `NActIP_b`, `NActEA_a` and `NActEA_b` (UHF STEOM
calculation) to desired values. However, this is not recommended for
general uses. The following snippet shows the output of the active orbital
selection procedure on a closed-shell molecule:

```orca
------------------------------------------
STATE AVERAGED NATURAL ORBITALS FOR ACTIVE SPACE SELECTION
------------------------------------------

Solving eigenvalue problem for the occupied space  ... Occupied block occupation :  
     0   0.000478 
     1   0.002266 
     2   0.169928 
     3   0.171663 
     4   0.310125 
     5   0.345541 
Orbital taken as active for IP roots:  
     0   0.345541 
     1   0.310125 
     2   0.171663 
     3   0.169928 
done
Solving eigenvalue problem for the virtual space   ... Virtual block occupation :  
     6   0.640886 
     7   0.332262 
     8   0.017272 
     9   0.005326 
    10   0.001752 
    11   0.000667 
    12   0.000574 
    13   0.000540 
    14   0.000160 
    15   0.000150 
    16   0.000139 
    17   0.000086 
    18   0.000082 
    19   0.000037 
    20   0.000023 
    21   0.000016 
    22   0.000013 
    23   0.000008 
    24   0.000003 
    25   0.000002 
    26   0.000001 
    27   0.000000 
    28   0.000000 
    29   0.000000 
    30   0.000000 
    31   0.000000 
    32   0.000000 
    33   0.000000 
    34   0.000000 
    35  -0.000000 
Orbital taken as active for EA roots :  
     0   0.640886 
     1   0.332262 
     2   0.017272 
done
 No of roots active in IP calculation:    4  
 No of roots active in EA calculation:    3
```

(sec:spectroscopyproperties.steom.tddftguess)=
## Active space selection using TD-DFT densities 

Instead of using a CIS calculation for selected the Active Space roots,
a TD-DFT based one can also be considered. Be aware that using DFT
Kohn-Sham orbitals for computing the CCSD GS energy can lead to some
instabilities and give incorrect results.

The main interest of this approach is to start the STEOM-CCSD
calculation with TD-DFT electronic densities which are in general better
than the CIS one, especially for some specific compounds (metallic
complexes for example). The computed TD-DFT densities are also often
more stable than the CIS one. It will however slow down the calculation.

The input has to be written like this:

```orca
!RHF/UHF BHANDHLYP STEOM-CCSD TZVP 

%mdci
nroots 10
tddftguess true
end

%tddft
nroots 10
end

*xyz 0 1
```

Any DFT functional can be used but we recommend one with a decent amount
of HF exchange. On top of this, the keyword `TDDFTGuess` has to
be set to true in mdci block and the tddft has to be added together with
the `NRoots` keyword. In both input blocks (`%mdci` and `%tddft`) the
same number of roots has to be given. Starting from ORCA 6, using TD-DFT 
guess with an UHF reference is also possible.

(sec:spectroscopyproperties.steom.reliability)=
## Reliability of the Calculated Excitation Energy 

The excitation energy for any states calculated in STEOM-CC are only
reliable when the dominant excitation for that states are confined
within the active space. This can be verified from the percentage active
character of the calculated states, an *a posteriori* diagnostic which is
defined as

$$\begin{aligned}
A = \frac{\sum\limits_{m,e} C(m,e) \cdot C(m,e) }{\sum\limits_{i,a} C(i,a) \cdot C(i,a) }*100\end{aligned}$$

for closed-shell systems and takes the form,

$$\begin{aligned}
A =\frac{\sum\limits_{m,e}C(m,e) \cdot C(m,e)+\sum\limits_{\bar{m},\bar{e} }C(\bar{m},\bar{ e}) \cdot C(\bar{m},\bar{ e}) }{\sum\limits_{i,a}C(i,a) \cdot C(i,a)+\sum\limits_{\bar{i},\bar{a} }C(\bar{i},\bar{a}) \cdot C(\bar{i},\bar{a}) } \cdot 100.\end{aligned}$$

within the UHF formalism. The roots which have $A$
higher than 98.0 are considered to be converged with respect to the
active space. {cite}`Dutta2018eomvert`

```orca
------------------
STEOM-CCSD RESULTS
------------------

IROOT=  1:  0.145412 au     3.957 eV   31914.3 cm**-1
  Amplitude    Excitation
  -0.169361     4 ->   8
  -0.984822     7 ->   8

Percentage Active Character     99.86

  Amplitude    Excitation in Canonical Basis
  -0.166580     4 ->   8
  -0.975432     7 ->   8
  -0.124356     7 ->  13

IROOT=  2:  0.309409 au     8.419 eV   67907.5 cm**-1
  Amplitude    Excitation
   0.994141     7 ->   9

Percentage Active Character     99.78

  Amplitude    Excitation in Canonical Basis
  -0.990029     7 ->   9

IROOT=  3:  0.336993 au     9.170 eV   73961.4 cm**-1
  Amplitude    Excitation
  -0.994078     5 ->   8

Percentage Active Character     99.10

  Amplitude    Excitation in Canonical Basis
  -0.984116     5 ->   8
  -0.136769     5 ->  13

IROOT=  4:  0.357473 au     9.727 eV   78456.2 cm**-1
  Amplitude    Excitation
   0.181761     4 ->  10
   0.728209     6 ->   8
   0.611668     7 ->  10
  -0.191540     7 ->  12

Percentage Active Character     94.10

Warning:: the state may have not converged with respect to active space 
-------------------- Handle with Care -------------------- 

  Amplitude    Excitation in Canonical Basis
  -0.184144     4 ->  10
  -0.725183     6 ->   8
  -0.633718     7 ->  10

IROOT=  5:  0.386654 au    10.521 eV   84860.8 cm**-1
  Amplitude    Excitation
   0.980406     4 ->   8
  -0.178551     7 ->   8

Percentage Active Character     99.79

  Amplitude    Excitation in Canonical Basis
   0.971678     4 ->   8
   0.122877     4 ->  13
  -0.179242     7 ->   8

IROOT=  6:  0.444881 au    12.106 eV   97640.1 cm**-1
  Amplitude    Excitation
  -0.995150     6 ->   9

Percentage Active Character     99.69

  Amplitude    Excitation in Canonical Basis
  -0.989966     6 ->   9
```

If the $\% active  character$ for any calculated state is less than 98,
that state may have not converged with respect to active space and the
excitation energy for that particular state is less reliable. The user
should request a larger number of roots under those conditions.

(sec:spectroscopyproperties.steom.remove)=
## Removal of IP and EA states with double excitation character

To obtain accurate results with STEOM-CCSD, only the $\hat{S}$
amplitudes corresponding to the states dominated by single excitations
should be included in the second similarity transformation. This is
ensured in ORCA in two ways. First, the root following (`FollowCIS`) is
activated by default so that it converges to the states dominated by
singly excited guess vectors. This avoids the calculation of so called
'satellite states', which are of double excitation character with
respect to the ground state. Secondly, among the converged IP and EA
roots, the states which have %singles character below a certain
predefined threshold (i.e. controlled by the keywords `IPThresh` and
`EAThresh`) are automatically excluded from the second similarity
transformation.

```orca
EOM-CCSD RESULTS
----------------

IROOT=  1:  0.105316 au     2.866 eV   23114.2 cm**-1
  Amplitude    Excitation
   0.697547     x ->   8
IROOT=  2:  0.217925 au     5.930 eV   47829.1 cm**-1
  Amplitude    Excitation
  -0.701454     x ->   9
IROOT=  3:  0.304098 au     8.275 eV   66741.8 cm**-1
  Amplitude    Excitation
  -0.700458     x ->  10
IROOT=  4:  0.350387 au     9.535 eV   76901.1 cm**-1
  Amplitude    Excitation
   0.702705     x ->  11
IROOT=  5:  0.651462 au    17.727 eV  142979.4 cm**-1
  Amplitude    Excitation
   0.637352     x ->  12
   0.121747     x ->   8     4 ->  10
   0.177039     x ->   8     5 ->   9
   0.109987     x ->   9     5 ->   8
  -0.206789     x ->   8     7 ->  10
  -0.109870     x ->  10     7 ->   8

EA STATE=  0:  percentage singles     95.282 
EA STATE=  1:  percentage singles     96.981 
EA STATE=  2:  percentage singles     96.540 
EA STATE=  3:  percentage singles     97.844 
EA STATE=  4:  percentage singles     68.884 

Warning: high double excitation character, excluding from the STEOM transformation
 Final no active EA roots:    4
```

Note that the use of CIS natural transition orbitals can lead to
convergence issues for the IP and EA states which are dominated by
double excitation character. This can be remedied by setting
`DoDbFilter` to true.

(sec:spectroscopyproperties.store)=
## Transition and difference densities

At the end of a STEOM computation, it is possible to store the final
eigenvectors in a file "*job.cis*", in analogy with what is done for CIS
and TD-DFT computations. This file can be obtained by setting
`DoStoreSTEOM true` in the input. This file can then be processed by
`orca_plot` to obtain the difference and / or the transition densities.

An Natural Transition Orbitals analysis can also be performed within the
STEOM-CCSD scheme, as described in
{ref}`sec:spectroscopyproperties.tddft.natTransOrb`. It can be performed by setting
the keyword `DoSTEOMNatTransOrb` to true.

(sec:spectroscopyproperties.steom.properties)=
## Properties

The dipolar and transition moments (as well as the oscillator strength)
can be computed within the STEOM module using different kinds of
approximations. Please cite our paper on these corrected STEOM
transition densities {cite}`ghosh_new_2020`! Starting from ORCA 5,
new defaults (`DoSimpleDens false`) are used that are much better
than the previous CIS-like approximation, and the full option is of
CC3-like quality.

```orca
%mdci

DosimpleDens false  # Default, using STEOM-CCSD density + some doubles effect.
AddL2term true

DosimpleDens false  # using the STEOM-CCSD density + some doubles effect.
AddL2term true      # + neglected GS doubles
UpdateL1 true

DosimpleDens false  # using the STEOM-CCSD density + some doubles effect.
AddL2term true      # + neglected GS double + doubles from EOM-CCSD
UpdateL1 true       # (expensive, but of CC3 quality - see reference)
AddDDTerm true

end
```

By default, the STEOM-CCSD densities with `AddL2term true`
should be used for all calculation as discussed in ref. {cite}`ghosh_new_2020`.

(sec:spectroscopyproperties.steom.solvatation)=
## Solvation (Experimental) 

In STEOM-CCSD, the excitation energies and densities can be corrected
using the CPCM solvation scheme in ORCA. 

To use it, the keyword `DoSolv` has to be set to true in the `%mdci` block and
the simple keyword `CPCM` (or `SMD`) + name of the solvent has to be given.

```orca
!CPCM(ethanol) STEOM-CCSD TightSCF def2-TZVP def2-TZVP/C def2/J 

%mdci
Nroots 5
DoSolv true
end
```

(sec:spectroscopyproperties.steom.SOC)=
## Spin-Orbit Coupling (Experimental) 

You can compute the spin-orbit coupling between singlet and triplets
states in STEOM-CCSD using the keyword `STEOMSOC true`.
Please note that all SOC matrix elements and properties are currently
computed from the **right vector only**!

(sec:spectroscopyproperties.steom.core)=
## Core excitation

The STEOM-CCSD (and bt-PNO-STEOM-CCSD) method can also be used to
compute the K-edge core-excitation energy of molecules. See
{ref}`sec:spectroscopyproperties.eomcore.core-excitation` for more details.

(sec:spectroscopyproperties.steom.trans)=
## Transient absorption

Transient absorption spectra can be computed using the keyword
`DoTrans true`. The `IRoot` keyword will select the
targeted excited state.
