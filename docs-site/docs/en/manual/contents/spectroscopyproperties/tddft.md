

<a id="sec:spectroscopyproperties.tddft"></a>
# Excited States via RPA, CIS, TD-DFT and SF-TDA

ORCA features a relatively efficient single-excitation CI (CIS),
"random-phase approximation" (RPA) and time-dependent DFT module that
can be used to calculate excitation energies, absorption intensities and
CD intensities. Especially TD-DFT became very popular for excited state
calculations as it offers significantly better results than HF-CIS at
about the same cost. However, there are also many pitfalls of TD-DFT,
some of which are discussed in
reviews[neese2006jbiolinorgchem](../../bibliography.md)[neese2009coordchemreviews](../../bibliography.md). TD-DFT
methods are available for closed-shell and spin-unrestricted reference
states, together with its collinear spin-flip variant. Analytic
gradients are available for all these cases. There also is a doubles
correction implemented that improves the results (but also the
computational cost). It is often used together with double-hybrid
functionals as explained below. The TD-DFT module of ORCA is also
extensively used for the calculation of X-ray absorption spectra at the
K-edge of a given element.

Starting from version 6.0.0, the output format of the absorption wavelength,
oscillator strength etc. has changed compared to the 5.0.x version. For more
details on the interpretation of the output, please refer to [spectroscopyproperties.ops](#sec:spectroscopyproperties.ops).

<a id="sec:spectroscopyproperties.tddft.general"></a>
## General Features

The module is invoked with the block:

```orca
%cis  end

# or equivalently

%tddft end
```

There are a variety of options. The most important one is the number of
excited states that you want to have calculated:

```orca
%cis NRoots    10  end
```

The convergence tolerances are given by:

```orca
%cis
  ...
  ETol  1e-6
  RTol  1e-6
end
```

The variable `ETol` gives the required convergence of the energies of
the excited states (in Eh) and `RTol` is the required convergence on the
norm of the residual vectors. Under normal ciorcumstances the
calculations need about 5-10 iterations to converge to the default
convergence tolerances.

Once converged, the program prints the wave function composition. To
keep the printing concise, coefficients smaller than 0.01 are omitted.
The threshold can be adjusted with the keyword `TPrint`.

```orca
%cis 
  ...
  TPrint 0.0001 # cut-off for the wave function printing, default= 0.01
end
```

If closed-shell references are used the program can calculate the
singlet and spin-adapted triplet excited states at the same time by
using:

```orca
%cis 
  ...
  triplets  true
end
```

This is available for all combinations of methods, including analytic
gradients, and for double-hybrids.

In order to control the orbitals that should be taken into account in
the calculation two mechanisms are available. The first mechanism is the
default mechanism and consists of specifying and orbital energy window
within which all single excitations will be considered:

```orca
%cis 
  ...
  EWin  -3,3  # (orbital energy window in Eh)
end
```

Thus, the default is to keep core orbitals frozen and to neglect very
high lying virtual orbitals which is a sensible approximation. However,
you may want to consider to include all virtual orbitals by choosing for
example `EWin -3,10000`. The second mechanism is to explicitly give an
orbital energy window for each operator, i.e.

```orca
%cis
  ...
  OrbWin[0] = 2,-1,-1,14 # orbital window for spin-up MOs
  OrbWin[1] = 2,-1,-1,16 # orbital window for spin-down MOs
end
```

The "-1"'s in the above example mean that the HOMO and LUMO for the
spin-.up and spin-down orbitals will be automatically determined by the
program. In other words, in the above example, only the following
excitations are included in the TDDFT calculation:

-   Excitations from any occupied alpha orbital whose index is between 2
    (inclusive) and that of the alpha HOMO (inclusive), to any virtual
    alpha orbital whose index is between that of alpha LUMO (inclusive)
    and 14 (inclusive)

-   Excitations from any occupied beta orbital whose index is between 2
    (inclusive) and that of the beta HOMO (inclusive), to any virtual
    beta orbital whose index is between that of beta LUMO (inclusive)
    and 16 (inclusive)

For calculations based on a restricted reference, `OrbWin[1]` will be
ignored.

In using the CIS/TD-DFT module five different types of calculations
should be distinguished:

-   Semiempirical methods

-   Hartree-Fock calculations

-   DFT calculations without HF exchange (non-hybrid functionals)

-   DFT calculations with HF exchange (hybrid functionals)

-   DFT calculations with HF exchange and MP2 correlation (double-hybrid
    functionals)

<a id="sec:spectroscopyproperties.tddft.semiemp"></a>
## Semiempirical Methods

The semiempirical INDO/S method is very suitable to calculate absorption
spectra of medium sized to large organic and inorganic molecules. It has
been parameterized by the late M. C. Zerner for optical spectroscopy and
in my experience at least, it tends to work nicely for many systems.
With the semiempirical approach it is easy to calculate many states of
large molecules. For example, consider the following calculation on a
bis-histidine ligated iron-porphyrin model (in the Fe(II) state) that
includes 92 atoms and $\approx$ 16,500 CSFs in the single excitation
space. Yet the calculation requires only a few minutes on an ordinary
computer for the prediction of the first 40 excited states.

The calculated spectrum is in essentially reasonable agreement with
experiment in showing a huge band around 400 nm (the famous Soret band)
and a smaller but still intense band between 500 and 550 nm (the
Q-band). There are no predicted absorptions below $\approx$ 10,000
cm$^{-1}$.

The input for the job is shown below:

```mol
title: structure 1
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
93
structure (0 1)
Fe     -0.01736      0.71832     -0.30714
C       2.65779      4.03195     -0.13175
C       3.51572      3.02488     -0.24101
C       2.66971      1.82027     -0.30891
C       3.30062      0.51609     -0.42755
C       2.61022     -0.60434     -0.47131
C       3.32146     -1.89491     -0.57434
C       2.35504     -2.79836     -0.57179
C       1.11740     -1.99868     -0.46878
C      -0.04908     -2.61205     -0.44672
C      -1.30967     -1.89127     -0.38984
C      -2.58423     -2.63345     -0.40868
C      -3.50492     -1.68283     -0.37930
C      -2.72946     -0.42418     -0.33711
C      -3.35747      0.73319     -0.28970
C      -2.66935      2.01561     -0.22869
C      -3.31167      3.19745     -0.16277
C      -4.72835      3.62642     -0.14517
C      -5.84825      2.89828     -0.20597
C      -2.21443      4.15731     -0.09763
C      -1.11572      3.39398     -0.14235
C       0.19578      4.02696     -0.10122
C       1.33370      3.36290     -0.15370
C       3.09165      5.44413     -0.02579
C       2.35656      6.55323      0.10940
N       1.43216      2.09428     -0.24815
N       1.34670     -0.74673     -0.42368
N      -1.39885      2.15649     -0.21891
N      -1.47620     -0.63353     -0.34705
C       5.03025      3.02708     -0.28544
C       4.81527     -2.12157     -0.66646
C      -5.01065     -1.83771     -0.38886
C      -2.28137      5.66820     -0.00321
C      -2.73691     -4.14249     -0.43699
C      -2.42579     -4.72805     -1.83259
C       2.45978     -4.31073     -0.64869
C       2.19678     -4.82182     -2.08201
C       1.60835     -6.22722     -2.10748
C      -1.90102     -6.15737     -1.82447
O      -1.96736     -6.92519     -2.75599
O       1.60982     -7.01844     -1.19330
O      -1.15355     -6.41323     -0.74427
O       0.89871     -6.41433     -3.22828
H       4.17823      5.62170     -0.05623
H       2.86221      7.53117      0.17503
H       1.26303      6.57673      0.17212
H       0.21799      5.11603     -0.03468
H      -1.78003      6.14426     -0.87498
H      -3.32281      6.05139      0.01906
H      -1.78374      6.03115      0.92347
H      -4.89690      4.71221     -0.07358
H      -6.82566      3.40843     -0.18007
H      -5.88239      1.80643     -0.28628
H      -4.44893      0.70720     -0.28575
H      -5.32107     -2.89387     -0.54251
H      -5.45075     -1.49552      0.57400
H      -5.46788     -1.24144     -1.20929
H      -2.05997     -4.55939      0.34045
H      -3.76430     -4.43895     -0.12880
H      -3.33638     -4.66246     -2.47119
H      -1.65517     -4.10119     -2.33605
H      -0.56422     -7.14866     -1.00437
H       0.26056     -7.12181     -3.00953
H       1.48118     -4.13253     -2.58671
H       3.13949     -4.79028     -2.67491
H       3.46153     -4.65168     -0.30336
H       1.73023     -4.75206      0.06633
H       5.26172     -1.51540     -1.48550
H       5.31767     -1.84036      0.28550
H       5.06416     -3.18438     -0.87628
H      -0.07991     -3.70928     -0.48866
H       4.39835      0.46775     -0.47078
H       5.39550      2.59422     -1.24309
H       5.47197      4.04179     -0.19892
H       5.44914      2.41988      0.54738
N       0.01831      0.60829      1.68951
C       0.02054      1.64472      2.54371
C       0.04593     -0.50152      2.45186
N       0.04934      1.20474      3.84418
C       0.06582     -0.16578      3.80848
H       0.00322      2.72212      2.31829
N      -0.05051      0.81937     -2.30431
H       0.05251     -1.53704      2.08183
C       0.11803      1.92670     -3.04495
H       0.05712      1.81091      4.70485
H       0.08982     -0.83278      4.68627
C      -0.24302     -0.18840     -3.17641
C      -0.19749      0.28568     -4.49059
N       0.03407      1.63309     -4.38373
H       0.30109      2.95786     -2.70479
H      -0.41432     -1.24242     -2.91290
H      -0.31761     -0.27403     -5.43315
H       0.12975      2.31943     -5.17616
--- input ---
# Test CIS in conjunction with INDO/S

! ZINDO/S TightSCF DIIS NoMOPrint
%cis  NRoots  40
      end
* xyz 0 1
Fe   -0.01736     0.71832    -0.30714
C     2.65779     4.03195    -0.13175
C     3.51572     3.02488    -0.24101
C     2.66971     1.82027    -0.30891
C     3.30062     0.51609    -0.42755
C     2.61022    -0.60434    -0.47131
C     3.32146    -1.89491    -0.57434
C     2.35504    -2.79836    -0.57179
C     1.11740    -1.99868    -0.46878
C    -0.04908    -2.61205    -0.44672
C    -1.30967    -1.89127    -0.38984
C    -2.58423    -2.63345    -0.40868
C    -3.50492    -1.68283    -0.37930
C    -2.72946    -0.42418    -0.33711
C    -3.35747     0.73319    -0.28970
C    -2.66935     2.01561    -0.22869
C    -3.31167     3.19745    -0.16277
C    -4.72835     3.62642    -0.14517
C    -5.84825     2.89828    -0.20597
C    -2.21443     4.15731    -0.09763
C    -1.11572     3.39398    -0.14235
C     0.19578     4.02696    -0.10122
C     1.33370     3.36290    -0.15370
C     3.09165     5.44413    -0.02579
C     2.35656     6.55323     0.10940
N     1.43216     2.09428    -0.24815
N     1.34670    -0.74673    -0.42368
N    -1.39885     2.15649    -0.21891
N    -1.47620    -0.63353    -0.34705
C     5.03025     3.02708    -0.28544
C     4.81527    -2.12157    -0.66646
C    -5.01065    -1.83771    -0.38886
C    -2.28137     5.66820    -0.00321
C    -2.73691    -4.14249    -0.43699
C    -2.42579    -4.72805    -1.83259
C     2.45978    -4.31073    -0.64869
C     2.19678    -4.82182    -2.08201
C     1.60835    -6.22722    -2.10748
C    -1.90102    -6.15737    -1.82447
O    -1.96736    -6.92519    -2.75599
O     1.60982    -7.01844    -1.19330
O    -1.15355    -6.41323    -0.74427
O     0.89871    -6.41433    -3.22828
H     4.17823     5.62170    -0.05623
H     2.86221     7.53117     0.17503
H     1.26303     6.57673     0.17212
H     0.21799     5.11603    -0.03468
H    -1.78003     6.14426    -0.87498
H    -3.32281     6.05139     0.01906
H    -1.78374     6.03115     0.92347
H    -4.89690     4.71221    -0.07358
H    -6.82566     3.40843    -0.18007
H    -5.88239     1.80643    -0.28628
H    -4.44893     0.70720    -0.28575
H    -5.32107    -2.89387    -0.54251
H    -5.45075    -1.49552     0.57400
H    -5.46788    -1.24144    -1.20929
H    -2.05997    -4.55939     0.34045
H    -3.76430    -4.43895    -0.12880
H    -3.33638    -4.66246    -2.47119
H    -1.65517    -4.10119    -2.33605
H    -0.56422    -7.14866    -1.00437
H     0.26056    -7.12181    -3.00953
H     1.48118    -4.13253    -2.58671
H     3.13949    -4.79028    -2.67491
H     3.46153    -4.65168    -0.30336
H     1.73023    -4.75206     0.06633
H     5.26172    -1.51540    -1.48550
H     5.31767    -1.84036     0.28550
H     5.06416    -3.18438    -0.87628
H    -0.07991    -3.70928    -0.48866
H     4.39835     0.46775    -0.47078
H     5.39550     2.59422    -1.24309
H     5.47197     4.04179    -0.19892
H     5.44914     2.41988     0.54738
N     0.01831     0.60829     1.68951
C     0.02054     1.64472     2.54371
C     0.04593    -0.50152     2.45186
N     0.04934     1.20474     3.84418
C     0.06582    -0.16578     3.80848
H     0.00322     2.72212     2.31829
N    -0.05051     0.81937    -2.30431
H     0.05251    -1.53704     2.08183
C     0.11803     1.92670    -3.04495
H     0.05712     1.81091     4.70485
H     0.08982    -0.83278     4.68627
C    -0.24302    -0.18840    -3.17641
C    -0.19749     0.28568    -4.49059
N     0.03407     1.63309    -4.38373
H     0.30109     2.95786    -2.70479
H    -0.41432    -1.24242    -2.91290
H    -0.31761    -0.27403    -5.43315
H     0.12975     2.31943    -5.17616
*
```

```orca
%cis  end

# or equivalently

%tddft end
```

<a id="fig:77"></a>
*Structure of the iron-porphyrin used for the prediction of its
absorption spectrum (the structure was obtained from a molecular
mechanics calculation and the iron-imidazole bondlength was set to 2.0
Å).*

<a id="fig:78"></a>
*The ZINDO/S predicted absorption spectrum of the model iron porphyrin
shown above. The spectrum has been plotted using the `orca_mapspc`
tool.*

!!! note
    ORCA slightly departs from standard ZINDO/S in using dipole
    integrals in the intensity calculations that include all one- and
    two-center terms which are calculated via a STO-3G expansion of the
    Slater basis orbitals. The calculated intensities are not highly
    accurate anyways. In the present case they are overestimated by a factor
    of $\approx$ 2.

<a id="sec:spectroscopyproperties.tddft.hf"></a>
## Hartree-Fock Wavefunctions

When applying the procedures outlined above to pure Hartree-Fock, one
obtains the "random-phase approximation" (RPA) or the CI singles (CIS)
model (when effectively using the Tamm-Dancoff Approximation, TDA). In
general, RPA and CIS calculations do not lead to good agreement with
experimental excitation energies and errors of 1-5 eV are common.
Therefore HF/CIS is mostly a qualitative tool or can be used with
caution for larger molecules if more extensive and more well balanced CI
calculations are not computationally tractable.

<a id="sec:spectroscopyproperties.tddft.dft"></a>
## Non-Hybrid and Hybrid DFT

For DFT functionals there is the choice between the full TD-DFT (eq.
[Eq](#eqrpa)) treatment
and the so-called Tamm-Dancoff approximation (TDA).

<a id="eqrpa"></a>

$$
\left(\begin{array}{cc}
 A & B \\
 B* & A* \\
\end{array} \right) \left(\begin{array}{c}
 X \\
 Y  \\
\end{array} \right) = \left(\begin{array}{cc}
 \omega & 0 \\
 0 & -\omega \\
\end{array} \right) \left(\begin{array}{c}
 X \\
 Y  \\
\end{array} \right)\qquad \text{(eqrpa)}
$$

The TDA is the same approximation that leads from RPA to CIS (i.e.
neglect of the so-called "B" matrix, see eq.
[Eq](#eqtda)). The
results for vertical excitation energies are usually very similar
between the two approaches.

<a id="eqtda"></a>

$$
A X_{\text{TDA} } = \omega_{\text{TDA} } X_{\text{TDA} }\qquad \text{(eqtda)}
$$

In general, the elements of matrix "A" and "B" for singlet-singlet
excitations in the spin-restricted case are given by eqs.
[Eq](#eqamat) and
[Eq](#eqbmat).

<a id="eqamat"></a>

$$
\begin{split}
A_{ia,jb} = & \delta_{ij} \delta_{ab} ( \epsilon_{a} - \epsilon_{i} )  + 2 (ia|jb) - a_{\text{X} } (ij|ab) \\
            & + (1 - a_{\text{X} }) (ia|f_{\text{XC} }|jb)
\end{split}\qquad \text{(eqamat)}
$$

and

<a id="eqbmat"></a>

$$
B_{ia,jb} =  2 (ia|bj)  - a_{\text{X} } (ib|aj) + (1 - a_{x}) (ia|f_{\text{XC} }|bj) \text{.}\qquad \text{(eqbmat)}
$$

Here, $i,j$ denote occupied and $a,b$ virtual orbitals. $a_{\text{X} }$
is the amount of non-local Fock exchange in the density functional. If
$a_{\text{X} }$ is equal to one, eqs.
[Eq](#eqrpa) and
[Eq](#eqtda) correspond
to the RPA and CIS case, based on a Hartree-Fock ground state
determinant.

The TDA is actually the default method for TD-DFT, and can be turned off
by:

```orca
%tddft
  TDA  false
end
```

There are situations where hybrid functionals give significantly better
results than pure functionals since they suffer less from the
self-interaction error. In those cases, the RIJCOSX
procedure[neese2009chemphys](../../bibliography.md) [izsak2011jchemphys](../../bibliography.md)[Helmich-Paris2021a](../../bibliography.md)
leads to very large speedups in such calculations at virtually no loss
in accuracy[petrenko2011jchemphys](../../bibliography.md), and is turned on by default
whenever the SCF uses that too.

<a id="sec:spectroscopyproperties.sftddft.dft"></a>
## Collinear Spin-Flip TDA (SF-TD-DFT) 

Another approach to obtain excited states via CIS/TD-DFT are the so
called spin-flip methods (for a good review, please check ref
[casanova_spin-flip_2020](../../bibliography.md)). The idea is to start from an UHF state, and
then "flip" one of the alpha electrons to generate states with
$MS_{SF} = MS_{UHF} - 1$. In order to do that, we look for excitations
from alpha-to-beta orbitals only, and that makes the A matrix from TDA
even simpler:

$$
A_{i\bar a,j\bar b}^{SF} = \delta_{ij} \delta_{\bar a\bar b} ( \epsilon_{\bar a} - \epsilon_{i} ) 
- a_{\text{X} } (ij|\bar a\bar b)\qquad \text{(eqbmat_sf)}
$$

where the overbar represent beta orbitals, and no-overbars alpha
orbitals.

!!! note
    Please note that for pure DFT (with $a_X=0$, and no HF
    contribution), the A matrix is based simply in the orbital energies, and
    thus it is always good to have a good amount of HF on the functional!

In order to facilitate the discussion on the results one gets from the
SF-TDA, let's take a closer look at the picture representing some
possible excitations:

<a id="fig:sf-td-dft"></a>
*Effect of the spin-flip operator on a UHF ($MS=3$) wavefunction. The
"spin-complete" states are eigenvectors of the $S^2$ operator, while the
"spin-incomplete" are not. Alpha and beta orbitals here are represented
with the same energy, just to simplify the image. Adapted from the
previously mentioned review.*

It is important to note that no all SF-excitations lead to determinants
that are eigenvalues of the $S^2$ operator. That means, depending on how
much of these "spin incomplete" excitations are present in the final
SF-state, the spin-contamination could be high, and in this case, states
with $\langle S^2 \rangle \simeq 1$ would be predicted. These are
undefined states within the SF theory and should be treated carefully.

!!! warning
    - Any SF method can only be used starting from a UHF wavefunction, with a multiplicity of at least 3!

<a id="sec:spectroscopyproperties.sftddft_CH2.dft"></a>
### First example: methylene and SF-CIS

One simple example is the calculation of the vertical singlet-triplet
splitting of the methylene radical within CIS, using the following input
with symmetry included:

```mol
title: structure 2
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
3
structure (0 3)
C             0            0       0.1058
H             0       0.9910      -0.3174
H             0      -0.9910      -0.3174
--- input ---
!def2-SVP USESYM 

%TDDFT 
 SF TRUE 
END

* xyz 0 3 
 C 0  0       0.1058
 H 0  0.9910 -0.3174
 H 0 -0.9910 -0.3174
*
```

```orca
%cis NRoots    10  end
```

The geometry was taken from a high-level CCSD(T)/cc-pVQZ ($X^3B_1$)
optimized geometry, and after the regular UHF SCF, the SF-CIS result is:

```orca
---------------------
SF-CIS EXCITED STATES
---------------------

the weight of the individual excitations are printed if larger than 1.0e-02

UHF/UKS reference: multiplicity estimated based on rounded <S**2> value, RELEVANCE IS LIMITED!

(SPIN-FLIP GROUND STATE)
STATE  1:  E=   0.005456 au      0.148 eV     1197.5 cm**-1 <S**2> =   2.041850 Sym: B1 Mult 3
     1a ->   3b  :     0.017437 (c= -0.13204740)
     3a ->   3b  :     0.465217 (c=  0.68206845)
     3a ->   9b  :     0.026214 (c=  0.16190881)
     4a ->   4b  :     0.443967 (c= -0.66630872)
     4a ->  10b  :     0.028255 (c= -0.16809333)

STATE  2:  E=   0.058434 au      1.590 eV    12824.9 cm**-1 <S**2> =   0.022791 Sym: A1 Mult 1
     3a ->   4b  :     0.128149 (c= -0.35797971)
     4a ->   3b  :     0.810350 (c=  0.90019420)
     4a ->   9b  :     0.032289 (c=  0.17969015)

STATE  3:  E=   0.079264 au      2.157 eV    17396.4 cm**-1 <S**2> =   0.032278 Sym: B1 Mult 1
     3a ->   3b  :     0.446020 (c= -0.66784709)
     3a ->   9b  :     0.018620 (c= -0.13645512)
     4a ->   4b  :     0.494589 (c= -0.70327031)
     4a ->  10b  :     0.023225 (c= -0.15239893)
```

```orca
%cis
  ...
  ETol  1e-6
  RTol  1e-6
end
```

Now, **it is very important to consider that the SF ground state is not
the UHF ground state anymore**, the "new" ground state within the SF
scheme is actually STATE 1. You can think of the UHF as being only an
initial model, on the basis of which the SF states are built. The final
energy of the new ground state is actually the SCF energy + energy of
the STATE 1 (which is the one given as the FINAL SINGLE POINT ENERGY is
no IROOT is given). This last contribution can be either positive or
negative, depending on the case.

Anyway, the ground state is predicted to be a triplet state (here with
$M_S=0$), as expected for this carbene, and the S-T spiting energy is
1.590 - 0.148 eV = 1.442 eV. The full CI results for that is 1.50 eV,
so it is already almost there! Of course, in this case computing the RHF
singlet - UHF triplet makes no sense, since the RHF singlet would not
have the necessary open-shell singlet character.

<a id="sec:spectroscopyproperties.sftddft_benzyne.dft"></a>
### Benzyne and SF-TDA

Benzyne is a classic diradical that can be generated from benzene by
hydrogen abstraction ([fig:SF_benzyne](#fig:SF_benzyne)). It is known to have an open-shell singlet
ground state, and has its adiabatic sinlget-triplet splitting measured
experimentally. Let's try to compute this value using SF-TDA with ORCA.

<a id="fig:SF_benzyne"></a>
*Lewis representation of the benzene and benzyne molecules, indicating
the diradical character of the
later.*

First, we optimize the open-shell singlet by using SF, and the input
that follows. Here we use now DFT, in particular the BHANDHLYP
functional, which uses 50% of HF correlation, and is recommended for
this kind of application. By default, the IROOT to be optimized is 1,
which in this case corresponds to the SF ground state.

```mol
title: structure 3
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
10
structure (0 3)
C      -1.39113      0.00000      0.00000
C       0.69557      1.20476      0.00000
C      -0.69557      1.20476      0.00000
C      -0.69557     -1.20476      0.00000
C       0.69557     -1.20476      0.00000
C       1.39113      0.00000      0.00000
H      -1.24291      2.15278      0.00000
H      -1.24291     -2.15278      0.00000
H       1.24291     -2.15278      0.00000
H       1.24291      2.15278      0.00000
--- input ---
!DEF2-TZVPD OPT 

%method
 Method DFT 
 Functional hyb_gga_xc_bhandhlyp
end

%tddft
  SF true
  NRoots  3
end

* xyz 0 3 
  C         -1.39113        0.00000        0.00000
  C          0.69557        1.20476        0.00000
  C         -0.69557        1.20476        0.00000
  C         -0.69557       -1.20476        0.00000
  C          0.69557       -1.20476        0.00000
  C          1.39113        0.00000        0.00000
  H         -1.24291        2.15278        0.00000
  H         -1.24291       -2.15278        0.00000
  H          1.24291       -2.15278        0.00000
  H          1.24291        2.15278        0.00000
*
```

```orca
%cis 
  ...
  TPrint 0.0001 # cut-off for the wave function printing, default= 0.01
end
```

And after the optimization of IROOT 1, the final SF-TDA result is:

```orca
---------------------
SF-TDA EXCITED STATES
---------------------

the weight of the individual excitations are printed if larger than 1.0e-02

UHF/UKS reference: multiplicity estimated based on rounded <S**2> value, RELEVANCE IS LIMITED!

(SPIN-FLIP GROUND STATE)
STATE  1:  E=   0.024173 au      0.658 eV     5305.3 cm**-1 <S**2> =   0.023478 Mult 1
    11a ->  19b  :     0.018563 (c= -0.13624537)
    17a ->  20b  :     0.245232 (c=  0.49520915)
    17a ->  27b  :     0.016815 (c= -0.12967111)
    20a ->  19b  :     0.667236 (c=  0.81684517)
    20a ->  25b  :     0.019935 (c= -0.14119296)

STATE  2:  E=   0.032615 au      0.887 eV     7158.1 cm**-1 <S**2> =   2.018056 Mult 3
    11a ->  20b  :     0.015462 (c= -0.12434444)
    17a ->  19b  :     0.448809 (c=  0.66993209)
    17a ->  25b  :     0.017854 (c= -0.13361796)
    20a ->  20b  :     0.460923 (c=  0.67891314)
    20a ->  27b  :     0.024031 (c= -0.15501804)

STATE  3:  E=   0.106201 au      2.890 eV    23308.4 cm**-1 <S**2> =   1.029543 Mult 3
    15a ->  20b  :     0.051523 (c= -0.22698783)
    18a ->  19b  :     0.910633 (c= -0.95427103)
    18a ->  25b  :     0.017352 (c=  0.13172868)
```

```orca
%cis 
  ...
  triplets  true
end
```

confirming the singlet ground state, with an upper triplet excited
state.

Now to optimize the triplet state using SF-TDA, one has to use a similar
input, except that now IROOT 2 has to be chosen as the one to be
optimized:

```mol
title: structure 4
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
10
structure (0 3)
C      -1.39113      0.00000      0.00000
C       0.69557      1.20476      0.00000
C      -0.69557      1.20476      0.00000
C      -0.69557     -1.20476      0.00000
C       0.69557     -1.20476      0.00000
C       1.39113      0.00000      0.00000
H      -1.24291      2.15278      0.00000
H      -1.24291     -2.15278      0.00000
H       1.24291     -2.15278      0.00000
H       1.24291      2.15278      0.00000
--- input ---
!DEF2-TZVPD OPT

%method
  Method DFT
  Functional hyb_gga_xc_bhandhlyp
end

%tddft
  SF true
  NRoots  3
  IRoot   2
end

* xyz 0 3
  C         -1.39113        0.00000        0.00000
  C          0.69557        1.20476        0.00000
  C         -0.69557        1.20476        0.00000
  C         -0.69557       -1.20476        0.00000
  C          0.69557       -1.20476        0.00000
  C          1.39113        0.00000        0.00000
  H         -1.24291        2.15278        0.00000
  H         -1.24291       -2.15278        0.00000
  H          1.24291       -2.15278        0.00000
  H          1.24291        2.15278        0.00000
*
```

Giving the following results:

```orca
---------------------
SF-TDA EXCITED STATES
---------------------

the weight of the individual excitations are printed if larger than 1.0e-02

UHF/UKS reference: multiplicity estimated based on rounded <S**2> value, RELEVANCE IS LIMITED!

(SPIN-FLIP GROUND STATE)
STATE  1:  E=   0.028669 au      0.780 eV     6292.1 cm**-1 <S**2> =   0.022484 Mult 1
    11a ->  19b  :     0.018011 (c= -0.13420632)
    17a ->  20b  :     0.293971 (c=  0.54219090)
    17a ->  27b  :     0.017459 (c= -0.13213220)
    20a ->  19b  :     0.611212 (c=  0.78180024)
    20a ->  25b  :     0.023243 (c=  0.15245717)

STATE  2:  E=   0.032738 au      0.891 eV     7185.1 cm**-1 <S**2> =   2.018181 Mult 3
    11a ->  20b  :     0.014963 (c= -0.12232498)
    17a ->  19b  :     0.444520 (c=  0.66672364)
    17a ->  25b  :     0.021443 (c=  0.14643407)
    20a ->  20b  :     0.462361 (c=  0.67997124)
    20a ->  27b  :     0.022005 (c= -0.14834057)

STATE  3:  E=   0.108154 au      2.943 eV    23737.1 cm**-1 <S**2> =   1.030736 Mult 3
    15a ->  20b  :     0.052291 (c= -0.22867148)
    18a ->  19b  :     0.904505 (c= -0.95105480)
    18a ->  25b  :     0.021057 (c= -0.14511042)
```

```orca
%cis 
  ...
  EWin  -3,3  # (orbital energy window in Eh)
end
```

After the optimization, the final predicted adiabatic singlet-triplet
gap is 0.233 eV, compared to the experimental value of 0.165 eV
[clark_p-benzyne_2003](../../bibliography.md).

<a id="sec:spectroscopyproperties.tddft.lrcpcm"></a>
## Including solvation effects via LR-CPCM theory

The LR-CPCM theory, as developed by Cammi and Tomasi [cammi_fast_2000](../../bibliography.md),
is implemented for both energies and gradients of excited states. It is
turned on by default, whenever CPCM is also requested for the ground
state.

The major change is that now there is a $G_{ia,jb}$ term in the
$\mathbf A$ part of Eq. [Eq](#eqrpa), related to solvation effects.

$$
\begin{split}
A_{ia,jb} = & \delta_{ij} \delta_{ab} ( \epsilon_{a} - \epsilon_{i} )  + 2 (ia|jb) + 2 G_{ia,jb} \\
& - a_{\text{X} } (ij|ab) + (1 - a_{\text{X} }) (ia|f_{\text{XC} }|jb)
\end{split}\qquad \text{(eqbmat_lrcpcm)}
$$

where $G_{ia,bj}$ is defined as:

$$
G_{ia,jb} = ( V_{ia})^T  q_{jb}\qquad \text{(lrcpcm_G)}
$$

### Equilibrium and non-equilibrium conditions

These charges $q_{jb}$ are calculated in the same way as described in
[cpcm.detailed](#sec:essentialelements.solvationmodels.cpcm.detailed), but for excited states,
two different values of $\varepsilon$ can be used, depending on the
dynamics of the system:

-   **Non-equilibrium**: If the calculation assumes that the electronic
    excitation is so fast, that there is no time for the solvent to
    reorganize around the solute, then the $\varepsilon_{\in f}$ of the
    solvent is used, which is equivalent to the square of the refractive
    index. That is the case if one wants to compute the vertical
    excitation energy, and it is the default in that case.

-   **Equilibrium**: If the excited state is assumed to be completely
    solvated, then the true dielectric constant $\varepsilon$ of the
    solvent should be used. That is the case for geometry optimizations,
    frequencies or inside ORCA_ESD. This is turned on by default
    whenever analytic gradients are requested.

In any case, these conditions can be controlled by the flag CPCMEQ, that
can be set to TRUE or FALSE by the user, and will then override the
defaults.

These are available to all CIS/TD-DFT options: singlets, spin-adapted
triplets, UHF and spin-flip variants. It works inclusive for
double-hybrids and whenever SOC is requested.

<a id="sec:spectroscopyproperties.tddft.popan"></a>
## Population Analysis of Excited States

If you want to print a population analysis for the excited state using
CIS/TD-DFT, there are two options available: using **unrelaxed** or
**relaxed** densities. For the unrelaxed densities, simply use UPOP
TRUE:

```mol
title: structure 5
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
4
structure (0 1)
O      -1.88199      1.42016     -0.00000
C      -1.80947      0.20286      0.00000
H      -2.50488     -0.38174     -0.59212
H      -1.04956     -0.29504      0.59212
--- input ---
!PBE def2-SVP

%tddft   
  NROOTS  5
  UPOP    TRUE
end

* xyz 0 1 
  O         -1.88199        1.42016       -0.00000
  C         -1.80947        0.20286        0.00000
  H         -2.50488       -0.38174       -0.59212
  H         -1.04956       -0.29504        0.59212
*
```

and the atomic changes and bond orders will be printed for the chosen
IROOT (default 1):

```orca
------------------------------------------------------------------------------
                 UNRELAXED CIS/TDA DENSITY POPULATION ANALYSIS
                                   IROOT 1
------------------------------------------------------------------------------
------------------------------------------------------------------------------
                           ORCA POPULATION ANALYSIS
------------------------------------------------------------------------------
Input electron density              ... example5.cispur.singlet.iroot0
BaseName (.gbw .S,...)              ... example5

                    ********************************
                    * MULLIKEN POPULATION ANALYSIS *
                    ********************************

-----------------------
MULLIKEN ATOMIC CHARGES
-----------------------
   0 O :    0.177629
   1 C :   -0.438661
   2 H :    0.130515
   3 H :    0.130518
Sum of atomic charges:   -0.0000000

(...)

                      *****************************
                      * MAYER POPULATION ANALYSIS *
                      *****************************

  NA   - Mulliken gross atomic population
  ZA   - Total nuclear charge
  QA   - Mulliken gross atomic charge
  VA   - Mayer's total valence
  BVA  - Mayer's bonded valence
  FA   - Mayer's free valence

  ATOM       NA         ZA         QA         VA         BVA        FA
  0 O      7.8224     8.0000     0.1776     2.5554     1.4462     1.1092
  1 C      6.4387     6.0000    -0.4387     3.8364     3.1848     0.6516
  2 H      0.8695     1.0000     0.1305     0.9720     0.8521     0.1199
  3 H      0.8695     1.0000     0.1305     0.9720     0.8521     0.1199

  Mayer bond orders larger than 0.100000
B(  0-O ,  1-C ) :   1.4477 B(  1-C ,  2-H ) :   0.8685 B(  1-C ,  3-H ) :   0.8685
```

To get the analysis from the relaxed density, simply use `!ENGRAD` to a
run a gradient calculation:

```mol
title: structure 6
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
4
structure (0 1)
O      -1.88199      1.42016     -0.00000
C      -1.80947      0.20286      0.00000
H      -2.50488     -0.38174     -0.59212
H      -1.04956     -0.29504      0.59212
--- input ---
!PBE def2-SVP ENGRAD

%tddft   
  NROOTS  5
  UPOP    TRUE
end

* xyz 0 1 
  O         -1.88199        1.42016       -0.00000
  C         -1.80947        0.20286        0.00000
  H         -2.50488       -0.38174       -0.59212
  H         -1.04956       -0.29504        0.59212
*
```

and the printout is:

```orca
------------------------------------------------------------------------------
                  RELAXED CIS/TDA DENSITY POPULATION ANALYSIS
                                   IROOT 1
------------------------------------------------------------------------------
------------------------------------------------------------------------------
                           ORCA POPULATION ANALYSIS
------------------------------------------------------------------------------
Input electron density              ... example6.cispre.singlet.iroot1
BaseName (.gbw .S,...)              ... example6

                    ********************************
                    * MULLIKEN POPULATION ANALYSIS *
                    ********************************

-----------------------
MULLIKEN ATOMIC CHARGES
-----------------------
   0 O :   -0.092919
   1 C :   -0.088136
   2 H :    0.090533
   3 H :    0.090522
Sum of atomic charges:   -0.0000000

(...)

                      *****************************
                      * MAYER POPULATION ANALYSIS *
                      *****************************

  NA   - Mulliken gross atomic population
  ZA   - Total nuclear charge
  QA   - Mulliken gross atomic charge
  VA   - Mayer's total valence
  BVA  - Mayer's bonded valence
  FA   - Mayer's free valence

  ATOM       NA         ZA         QA         VA         BVA        FA
  0 O      8.0929     8.0000    -0.0929     2.2728     1.3646     0.9082
  1 C      6.0881     6.0000    -0.0881     3.9322     3.1290     0.8031
  2 H      0.9095     1.0000     0.0905     0.9876     0.8843     0.1034
  3 H      0.9095     1.0000     0.0905     0.9876     0.8843     0.1034

  Mayer bond orders larger than 0.100000
B(  0-O ,  1-C ) :   1.3485 B(  1-C ,  2-H ) :   0.8902 B(  1-C ,  3-H ) :   0.8902
```

In order to print the analysis for multiple states, simply use `IROOTLIST`
and `TROOTLIST`:

```mol
title: structure 7
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
4
structure (0 1)
O      -1.88199      1.42016     -0.00000
C      -1.80947      0.20286      0.00000
H      -2.50488     -0.38174     -0.59212
H      -1.04956     -0.29504      0.59212
--- input ---
!PBE def2-SVP

%tddft   
  NROOTS  5
  IROOTLIST 1,2,3
  TROOTLIST 1,2,3
  UPOP    TRUE
end

* xyz 0 1 
  O         -1.88199        1.42016       -0.00000
  C         -1.80947        0.20286        0.00000
  H         -2.50488       -0.38174       -0.59212
  H         -1.04956       -0.29504        0.59212
*
```

<a id="sec:spectroscopyproperties.tddft.stda"></a>
## Simplified TDA and TD-DFT

ORCA also supports calculations of excited states using the simplified
Tamm-Dancoff approach (sTDA) by S. Grimme[GrimmeSTDA](../../bibliography.md). The sTDA is
particularly suited to calculate absorption spectra of very large
systems. sTDA as well as the simplified time-dependent density
functional theory (sTD-DFT)[BannwarthSTDDFT](../../bibliography.md) approach require a
(hybrid) DFT ground state calculation. For large systems, using
range-separated hybrid functionals (e.g. $\omega$B97X) is
recommended.[RisthausRSHSTDA](../../bibliography.md)\
The sTD-DFT approach in particular yields much better electronic
circular dichroism (ECD) spectra and should be used for this purpose.

### Theoretical Background

A brief outline of the theory will be given in the following. For more
details, please refer to the original
papers[GrimmeSTDA,BannwarthSTDDFT](../../bibliography.md). In the sTDA, the TDA eigenvalue
problem from eq. [Eq](#eqtda) is solved using a truncated and semi-empirically
simplified $A^{\prime}$ matrix. The trunctation negelects all
excitations that are beyond the energy range of interest, except a few
strongly coupled ones. The matrix elements from eq.
[Eq](#eqamat) are
simplified by neglecting the response of the density functional and by
approximating the remaining two-electron integrals as damped Coulomb
interactions between transition/charge density monopoles. In the
following, the indices $i,j$ denote occupied, $a,b$ virtual and $p,q$
either kind of orbitals.

<a id="eqamatstda"></a>

$$
A^{\prime}_{ia,jb} = \delta_{ij} \delta_{ab} ( \epsilon_{a} - \epsilon_{i} )  + \sum\limits_{A,B}^{N_{\text{atoms} }}
( 2 q^{A}_{ia} \gamma^{K}_{AB} q^{B}_{jb}  - q^{A}_{ij} \gamma^{J}_{AB} q^{B}_{ab} )\qquad \text{(eqamatstda)}
$$

$q^{A}_{pq}$ and $q^{B}_{pq}$ are the transition/charge density
monopoles located on atom $A$ and $B$, respectively. These are obtained
from Löwdin population analysis (see Sec.
[pop.loewdin](#sec:spectroscopyproperties.pop.loewdin)). $\epsilon_{p}$ is the Kohn-Sham
orbital energy of orbital $p$. $\gamma^{K}_{AB}$ and $\gamma^{J}_{AB}$
are the Mataga-Nishimoto-Ohno-Klopman damped Coulomb operators for
exchange-type ($K$) and Coulomb-type ($J$) integrals, respectively.

$$
\gamma_{AB}^J=\left(\frac{1}{(R_{AB})^{\beta}+(a_{\text{X} } \eta)^{-\beta} }\right)^{\frac{1}{\beta} }\qquad \text{(eqgammaj)}
$$

$$
\gamma_{AB}^K=\left(\frac{1}{(R_{AB})^{\alpha}+\eta^{-\alpha} }\right)^{\frac{1}{\alpha} }\qquad \text{(eqgammak)}
$$

Here, $\eta$ is the arithmetic mean of the chemical hardness of atom $A$
and $B$. $\alpha$ and $\beta$ are the parameters of the method and are
given by:

$$
\alpha = \alpha_{1} + a_{x} \alpha_{2}\qquad \text{(eqalphastda)}
$$

$$
\beta = \beta_{1} + a_{x} \beta_{2}\qquad \text{(eqbetastda)}
$$

For any global hybrid functional, $\alpha_{1}$, $\alpha_{2}$,
$\beta_{1}$ and $\beta_{2}$ are identical. $\alpha$ and $\beta$ then
depend on the amount of Fock exchange ($a_{\text{X} }$) only. This is
different for range-separated hybrid functionals where $\alpha_{2}$ and
$\beta_{2}$ are set to zero. $\alpha_{1}$ and $\beta_{1}$ along with a
value $a_{x}$ for the sTDA treatment are individually fitted for each
range-separated hybrid functional.[RisthausRSHSTDA](../../bibliography.md) It can bee seen
from eq. [Eq](#eqamatstda) that the method is asymptotically correct which
is crucial for excitations of charge transfer type.

In sTD-DFT, eq. [Eq](#eqrpa) is solved using the simplified matrices $A^{\prime}$
(see above) and $B^{\prime}$.

$$
B^{\prime}_{ia,jb} = \sum\limits_{A,B}^{N_{\text{atoms} }} ( 2 q^{A}_{ia} \gamma^{K}_{AB} q^{B}_{bj}  - a_{\text{X} } q^{A}_{ib} \gamma^{K}_{AB} q^{B}_{aj} )\qquad \text{(eqbmatsrpa)}
$$

This approach yields better transition dipole moments and therefore
spectra but the method is more costly than sTDA (a factor of 2--5 for
typical systems). The parameters used in sTDA and sTD-DFT are identical.
There are **no** additional parameters fitted for this method.

### Calculation Set-up

sTDA and sTD-DFT can be combined with any (restricted or unrestricted)
hybrid DFT singlepoint calculation. Gradients and frequencies are
**not** implemented! The methods can be invoked via the `%tddft` block.
Table [tblstdakw](#tblstdakw) gives
a list of the possible keywords.

<a id="tblstdakw"></a>
!!! note "Keyword list for sTDA and sTD-DFT."
    |                 |                                                                                        |
    |:----------------|:---------------------------------------------------------------------------------------|
    | Mode sTDA       | Invokes a sTDA calculation                                                             |
    | Mode sTDDFT     | Invokes a sTD-DFT calculation                                                          |
    | EThresh $value$ | Energy threshold up to which CSFs are included (in eV)                                 |
    | PTLimit $value$ | Energy threshold up to which CSFs beyond EThresh may be selected (in eV)               |
    | PThresh $value$ | Selection criterion to include CSF beyond EThresh (in Eh)                              |
    | axstda $value$  | Fock exchange parameter used in sTDA/sTD-DFT calculation (for range-separated hybrids) |
    | beta1 $value$   | Constant part of $J$ integral parameter $\beta$                                        |
    | beta2 $value$   | $a_{\text{X} }$ scaled part of $J$ integral parameter $\beta$                          |
    | alpha1 $value$  | Constant part of $K$ integral parameter $\alpha$                                       |
    | alpha2 $value$  | $a_{\text{X} }$ scaled part of $K$ integral parameter $\alpha$                         |
    | triplets true   | Calculate singlet-triplet excitations (default: singlet-singlet)                       |

The following example shows how to run such a sTDA calculation using the
BHLYP functional if one is interested in all excitations up to 10 eV.

```mol
title: structure 8
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
38
structure (0 1)
N     -1.726176     0.687742    -0.007335
N      1.213763     0.735949    -0.027163
N     -1.545188    -2.243058    -0.016803
N      1.395005    -2.195166    -0.036972
C      2.736733    -1.895646    -0.045209
C      3.277248    -0.608637    -0.045175
C      2.575908     0.605756    -0.036945
C      0.977551     2.083559    -0.021690
C     -0.288108     2.687287    -0.011220
C     -1.529488     2.048274    -0.004419
C     -3.067756     0.388045     0.001354
H     -0.976948    -0.007843    -0.015911
C     -3.608477    -0.899096     0.001258
C     -2.907149    -2.113434    -0.007085
C     -1.308388    -3.590806    -0.022331
C     -0.042695    -4.194596    -0.032673
C      1.198590    -3.555847    -0.039419
H      0.645751    -1.499625    -0.028098
C     -3.768181     1.641701     0.010433
C     -2.832985     2.651061     0.006924
C      2.228928     2.835679    -0.028158
C      3.228183     1.912006    -0.037679
C      3.437220    -3.149227    -0.053963
C      2.502048    -4.158627    -0.050442
C     -3.558669    -3.420017    -0.006390
C     -2.559381    -4.343652    -0.015901
H     -4.633051    -3.589818     0.000518
H     -2.644718    -5.427990    -0.018393
H     -0.016400    -5.285446    -0.035842
H      2.681678    -5.229875    -0.055110
H      4.519010    -3.247119    -0.061999
H      4.366739    -0.548807    -0.052422
H      2.314239     3.920088    -0.025633
H      4.302487     2.081864    -0.044563
H     -0.315062     3.778120    -0.007889
H     -3.013895     3.722099     0.011827
H     -4.849852     1.740964     0.018679
H     -4.697992    -0.958441     0.008649
--- input ---
! bhlyp def2-SVP tightscf smallprint printgap nopop 

%tddft
 Mode sTDA
 Ethresh 10.0
end

*xyz 0 1 
  N     -1.726176    0.687742   -0.007335
  N      1.213763    0.735949   -0.027163
  N     -1.545188   -2.243058   -0.016803
  N      1.395005   -2.195166   -0.036972
  C      2.736733   -1.895646   -0.045209
  C      3.277248   -0.608637   -0.045175
  C      2.575908    0.605756   -0.036945
  C      0.977551    2.083559   -0.021690
  C     -0.288108    2.687287   -0.011220
  C     -1.529488    2.048274   -0.004419
  C     -3.067756    0.388045    0.001354
  H     -0.976948   -0.007843   -0.015911
  C     -3.608477   -0.899096    0.001258
  C     -2.907149   -2.113434   -0.007085
  C     -1.308388   -3.590806   -0.022331
  C     -0.042695   -4.194596   -0.032673
  C      1.198590   -3.555847   -0.039419
  H      0.645751   -1.499625   -0.028098
  C     -3.768181    1.641701    0.010433
  C     -2.832985    2.651061    0.006924
  C      2.228928    2.835679   -0.028158
  C      3.228183    1.912006   -0.037679
  C      3.437220   -3.149227   -0.053963
  C      2.502048   -4.158627   -0.050442
  C     -3.558669   -3.420017   -0.006390
  C     -2.559381   -4.343652   -0.015901
  H     -4.633051   -3.589818    0.000518
  H     -2.644718   -5.427990   -0.018393
  H     -0.016400   -5.285446   -0.035842
  H      2.681678   -5.229875   -0.055110
  H      4.519010   -3.247119   -0.061999
  H      4.366739   -0.548807   -0.052422
  H      2.314239    3.920088   -0.025633
  H      4.302487    2.081864   -0.044563
  H     -0.315062    3.778120   -0.007889
  H     -3.013895    3.722099    0.011827
  H     -4.849852    1.740964    0.018679
  H     -4.697992   -0.958441    0.008649
end
```

```orca
%cis
  ...
  OrbWin[0] = 2,-1,-1,14 # orbital window for spin-up MOs
  OrbWin[1] = 2,-1,-1,16 # orbital window for spin-down MOs
end
```

Replacing `Mode sTDA` by `Mode sTDDFT` will invoke a sTD-DFT calculation
instead. This is shown in the next example in combination with the
$\omega$B97X functional and user specified parameters:

```mol
title: structure 9
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
38
structure (0 1)
N     -1.726176     0.687742    -0.007335
N      1.213763     0.735949    -0.027163
N     -1.545188    -2.243058    -0.016803
N      1.395005    -2.195166    -0.036972
C      2.736733    -1.895646    -0.045209
C      3.277248    -0.608637    -0.045175
C      2.575908     0.605756    -0.036945
C      0.977551     2.083559    -0.021690
C     -0.288108     2.687287    -0.011220
C     -1.529488     2.048274    -0.004419
C     -3.067756     0.388045     0.001354
H     -0.976948    -0.007843    -0.015911
C     -3.608477    -0.899096     0.001258
C     -2.907149    -2.113434    -0.007085
C     -1.308388    -3.590806    -0.022331
C     -0.042695    -4.194596    -0.032673
C      1.198590    -3.555847    -0.039419
H      0.645751    -1.499625    -0.028098
C     -3.768181     1.641701     0.010433
C     -2.832985     2.651061     0.006924
C      2.228928     2.835679    -0.028158
C      3.228183     1.912006    -0.037679
C      3.437220    -3.149227    -0.053963
C      2.502048    -4.158627    -0.050442
C     -3.558669    -3.420017    -0.006390
C     -2.559381    -4.343652    -0.015901
H     -4.633051    -3.589818     0.000518
H     -2.644718    -5.427990    -0.018393
H     -0.016400    -5.285446    -0.035842
H      2.681678    -5.229875    -0.055110
H      4.519010    -3.247119    -0.061999
H      4.366739    -0.548807    -0.052422
H      2.314239     3.920088    -0.025633
H      4.302487     2.081864    -0.044563
H     -0.315062     3.778120    -0.007889
H     -3.013895     3.722099     0.011827
H     -4.849852     1.740964     0.018679
H     -4.697992    -0.958441     0.008649
--- input ---
! wb97x def2-SVP tightscf smallprint printgap nopop 

%tddft
 Mode sTDDFT
 Ethresh 10.0
 axstda  0.56
 beta1  8.00
 beta2  0.00
 alpha1 4.58
 alpha2 0.00
end

*xyz 0 1 
  N     -1.726176    0.687742   -0.007335
  N      1.213763    0.735949   -0.027163
  N     -1.545188   -2.243058   -0.016803
  N      1.395005   -2.195166   -0.036972
  C      2.736733   -1.895646   -0.045209
  C      3.277248   -0.608637   -0.045175
  C      2.575908    0.605756   -0.036945
  C      0.977551    2.083559   -0.021690
  C     -0.288108    2.687287   -0.011220
  C     -1.529488    2.048274   -0.004419
  C     -3.067756    0.388045    0.001354
  H     -0.976948   -0.007843   -0.015911
  C     -3.608477   -0.899096    0.001258
  C     -2.907149   -2.113434   -0.007085
  C     -1.308388   -3.590806   -0.022331
  C     -0.042695   -4.194596   -0.032673
  C      1.198590   -3.555847   -0.039419
  H      0.645751   -1.499625   -0.028098
  C     -3.768181    1.641701    0.010433
  C     -2.832985    2.651061    0.006924
  C      2.228928    2.835679   -0.028158
  C      3.228183    1.912006   -0.037679
  C      3.437220   -3.149227   -0.053963
  C      2.502048   -4.158627   -0.050442
  C     -3.558669   -3.420017   -0.006390
  C     -2.559381   -4.343652   -0.015901
  H     -4.633051   -3.589818    0.000518
  H     -2.644718   -5.427990   -0.018393
  H     -0.016400   -5.285446   -0.035842
  H      2.681678   -5.229875   -0.055110
  H      4.519010   -3.247119   -0.061999
  H      4.366739   -0.548807   -0.052422
  H      2.314239    3.920088   -0.025633
  H      4.302487    2.081864   -0.044563
  H     -0.315062    3.778120   -0.007889
  H     -3.013895    3.722099    0.011827
  H     -4.849852    1.740964    0.018679
  H     -4.697992   -0.958441    0.008649
end
```

```mol
title: structure 10
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
93
structure (0 1)
Fe     -0.01736      0.71832     -0.30714
C       2.65779      4.03195     -0.13175
C       3.51572      3.02488     -0.24101
C       2.66971      1.82027     -0.30891
C       3.30062      0.51609     -0.42755
C       2.61022     -0.60434     -0.47131
C       3.32146     -1.89491     -0.57434
C       2.35504     -2.79836     -0.57179
C       1.11740     -1.99868     -0.46878
C      -0.04908     -2.61205     -0.44672
C      -1.30967     -1.89127     -0.38984
C      -2.58423     -2.63345     -0.40868
C      -3.50492     -1.68283     -0.37930
C      -2.72946     -0.42418     -0.33711
C      -3.35747      0.73319     -0.28970
C      -2.66935      2.01561     -0.22869
C      -3.31167      3.19745     -0.16277
C      -4.72835      3.62642     -0.14517
C      -5.84825      2.89828     -0.20597
C      -2.21443      4.15731     -0.09763
C      -1.11572      3.39398     -0.14235
C       0.19578      4.02696     -0.10122
C       1.33370      3.36290     -0.15370
C       3.09165      5.44413     -0.02579
C       2.35656      6.55323      0.10940
N       1.43216      2.09428     -0.24815
N       1.34670     -0.74673     -0.42368
N      -1.39885      2.15649     -0.21891
N      -1.47620     -0.63353     -0.34705
C       5.03025      3.02708     -0.28544
C       4.81527     -2.12157     -0.66646
C      -5.01065     -1.83771     -0.38886
C      -2.28137      5.66820     -0.00321
C      -2.73691     -4.14249     -0.43699
C      -2.42579     -4.72805     -1.83259
C       2.45978     -4.31073     -0.64869
C       2.19678     -4.82182     -2.08201
C       1.60835     -6.22722     -2.10748
C      -1.90102     -6.15737     -1.82447
O      -1.96736     -6.92519     -2.75599
O       1.60982     -7.01844     -1.19330
O      -1.15355     -6.41323     -0.74427
O       0.89871     -6.41433     -3.22828
H       4.17823      5.62170     -0.05623
H       2.86221      7.53117      0.17503
H       1.26303      6.57673      0.17212
H       0.21799      5.11603     -0.03468
H      -1.78003      6.14426     -0.87498
H      -3.32281      6.05139      0.01906
H      -1.78374      6.03115      0.92347
H      -4.89690      4.71221     -0.07358
H      -6.82566      3.40843     -0.18007
H      -5.88239      1.80643     -0.28628
H      -4.44893      0.70720     -0.28575
H      -5.32107     -2.89387     -0.54251
H      -5.45075     -1.49552      0.57400
H      -5.46788     -1.24144     -1.20929
H      -2.05997     -4.55939      0.34045
H      -3.76430     -4.43895     -0.12880
H      -3.33638     -4.66246     -2.47119
H      -1.65517     -4.10119     -2.33605
H      -0.56422     -7.14866     -1.00437
H       0.26056     -7.12181     -3.00953
H       1.48118     -4.13253     -2.58671
H       3.13949     -4.79028     -2.67491
H       3.46153     -4.65168     -0.30336
H       1.73023     -4.75206      0.06633
H       5.26172     -1.51540     -1.48550
H       5.31767     -1.84036      0.28550
H       5.06416     -3.18438     -0.87628
H      -0.07991     -3.70928     -0.48866
H       4.39835      0.46775     -0.47078
H       5.39550      2.59422     -1.24309
H       5.47197      4.04179     -0.19892
H       5.44914      2.41988      0.54738
N       0.01831      0.60829      1.68951
C       0.02054      1.64472      2.54371
C       0.04593     -0.50152      2.45186
N       0.04934      1.20474      3.84418
C       0.06582     -0.16578      3.80848
H       0.00322      2.72212      2.31829
N      -0.05051      0.81937     -2.30431
H       0.05251     -1.53704      2.08183
C       0.11803      1.92670     -3.04495
H       0.05712      1.81091      4.70485
H       0.08982     -0.83278      4.68627
C      -0.24302     -0.18840     -3.17641
C      -0.19749      0.28568     -4.49059
N       0.03407      1.63309     -4.38373
H       0.30109      2.95786     -2.70479
H      -0.41432     -1.24242     -2.91290
H      -0.31761     -0.27403     -5.43315
H       0.12975      2.31943     -5.17616
--- input ---
# Test CIS in conjunction with INDO/S

! ZINDO/S TightSCF DIIS NoMOPrint
%cis  NRoots  40
      end
* xyz 0 1
Fe   -0.01736     0.71832    -0.30714
C     2.65779     4.03195    -0.13175
C     3.51572     3.02488    -0.24101
C     2.66971     1.82027    -0.30891
C     3.30062     0.51609    -0.42755
C     2.61022    -0.60434    -0.47131
C     3.32146    -1.89491    -0.57434
C     2.35504    -2.79836    -0.57179
C     1.11740    -1.99868    -0.46878
C    -0.04908    -2.61205    -0.44672
C    -1.30967    -1.89127    -0.38984
C    -2.58423    -2.63345    -0.40868
C    -3.50492    -1.68283    -0.37930
C    -2.72946    -0.42418    -0.33711
C    -3.35747     0.73319    -0.28970
C    -2.66935     2.01561    -0.22869
C    -3.31167     3.19745    -0.16277
C    -4.72835     3.62642    -0.14517
C    -5.84825     2.89828    -0.20597
C    -2.21443     4.15731    -0.09763
C    -1.11572     3.39398    -0.14235
C     0.19578     4.02696    -0.10122
C     1.33370     3.36290    -0.15370
C     3.09165     5.44413    -0.02579
C     2.35656     6.55323     0.10940
N     1.43216     2.09428    -0.24815
N     1.34670    -0.74673    -0.42368
N    -1.39885     2.15649    -0.21891
N    -1.47620    -0.63353    -0.34705
C     5.03025     3.02708    -0.28544
C     4.81527    -2.12157    -0.66646
C    -5.01065    -1.83771    -0.38886
C    -2.28137     5.66820    -0.00321
C    -2.73691    -4.14249    -0.43699
C    -2.42579    -4.72805    -1.83259
C     2.45978    -4.31073    -0.64869
C     2.19678    -4.82182    -2.08201
C     1.60835    -6.22722    -2.10748
C    -1.90102    -6.15737    -1.82447
O    -1.96736    -6.92519    -2.75599
O     1.60982    -7.01844    -1.19330
O    -1.15355    -6.41323    -0.74427
O     0.89871    -6.41433    -3.22828
H     4.17823     5.62170    -0.05623
H     2.86221     7.53117     0.17503
H     1.26303     6.57673     0.17212
H     0.21799     5.11603    -0.03468
H    -1.78003     6.14426    -0.87498
H    -3.32281     6.05139     0.01906
H    -1.78374     6.03115     0.92347
H    -4.89690     4.71221    -0.07358
H    -6.82566     3.40843    -0.18007
H    -5.88239     1.80643    -0.28628
H    -4.44893     0.70720    -0.28575
H    -5.32107    -2.89387    -0.54251
H    -5.45075    -1.49552     0.57400
H    -5.46788    -1.24144    -1.20929
H    -2.05997    -4.55939     0.34045
H    -3.76430    -4.43895    -0.12880
H    -3.33638    -4.66246    -2.47119
H    -1.65517    -4.10119    -2.33605
H    -0.56422    -7.14866    -1.00437
H     0.26056    -7.12181    -3.00953
H     1.48118    -4.13253    -2.58671
H     3.13949    -4.79028    -2.67491
H     3.46153    -4.65168    -0.30336
H     1.73023    -4.75206     0.06633
H     5.26172    -1.51540    -1.48550
H     5.31767    -1.84036     0.28550
H     5.06416    -3.18438    -0.87628
H    -0.07991    -3.70928    -0.48866
H     4.39835     0.46775    -0.47078
H     5.39550     2.59422    -1.24309
H     5.47197     4.04179    -0.19892
H     5.44914     2.41988     0.54738
N     0.01831     0.60829     1.68951
C     0.02054     1.64472     2.54371
C     0.04593    -0.50152     2.45186
N     0.04934     1.20474     3.84418
C     0.06582    -0.16578     3.80848
H     0.00322     2.72212     2.31829
N    -0.05051     0.81937    -2.30431
H     0.05251    -1.53704     2.08183
C     0.11803     1.92670    -3.04495
H     0.05712     1.81091     4.70485
H     0.08982    -0.83278     4.68627
C    -0.24302    -0.18840    -3.17641
C    -0.19749     0.28568    -4.49059
N     0.03407     1.63309    -4.38373
H     0.30109     2.95786    -2.70479
H    -0.41432    -1.24242    -2.91290
H    -0.31761    -0.27403    -5.43315
H     0.12975     2.31943    -5.17616
*
```

For the range-separated hybrid functionals LC-BLYP, CAM-B3LYP,
$\omega$B97, $\omega$B97X, $\omega$B97X-D3 and $\omega$B97X-D3BJ,
parameters are available and will be used by default if one of these
functionals is used. The way of specifying parameters as shown above is
useful if there is a range-separated hybrid functional that has not been
parametrized for sTDA yet. For very large systems (e.g. $>$ 500 atoms),
it may be useful to define an upper boundary `PTLimit` for the selection
of configurations that are beyond `EThresh` (otherwise the whole
configuration space will be scanned). This can be done as shown below:

```mol
title: structure 11
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
38
structure (0 1)
N     -1.726176     0.687742    -0.007335
N      1.213763     0.735949    -0.027163
N     -1.545188    -2.243058    -0.016803
N      1.395005    -2.195166    -0.036972
C      2.736733    -1.895646    -0.045209
C      3.277248    -0.608637    -0.045175
C      2.575908     0.605756    -0.036945
C      0.977551     2.083559    -0.021690
C     -0.288108     2.687287    -0.011220
C     -1.529488     2.048274    -0.004419
C     -3.067756     0.388045     0.001354
H     -0.976948    -0.007843    -0.015911
C     -3.608477    -0.899096     0.001258
C     -2.907149    -2.113434    -0.007085
C     -1.308388    -3.590806    -0.022331
C     -0.042695    -4.194596    -0.032673
C      1.198590    -3.555847    -0.039419
H      0.645751    -1.499625    -0.028098
C     -3.768181     1.641701     0.010433
C     -2.832985     2.651061     0.006924
C      2.228928     2.835679    -0.028158
C      3.228183     1.912006    -0.037679
C      3.437220    -3.149227    -0.053963
C      2.502048    -4.158627    -0.050442
C     -3.558669    -3.420017    -0.006390
C     -2.559381    -4.343652    -0.015901
H     -4.633051    -3.589818     0.000518
H     -2.644718    -5.427990    -0.018393
H     -0.016400    -5.285446    -0.035842
H      2.681678    -5.229875    -0.055110
H      4.519010    -3.247119    -0.061999
H      4.366739    -0.548807    -0.052422
H      2.314239     3.920088    -0.025633
H      4.302487     2.081864    -0.044563
H     -0.315062     3.778120    -0.007889
H     -3.013895     3.722099     0.011827
H     -4.849852     1.740964     0.018679
H     -4.697992    -0.958441     0.008649
--- input ---
! cam-b3lyp def2-SVP tightscf smallprint printgap nopop

%tddft
 Mode sTDDFT
 Ethresh 10.0
 PThresh 1e-4
 PTLimit 30
end

*xyz 0 1 
  N     -1.726176    0.687742   -0.007335
  N      1.213763    0.735949   -0.027163
  N     -1.545188   -2.243058   -0.016803
  N      1.395005   -2.195166   -0.036972
  C      2.736733   -1.895646   -0.045209
  C      3.277248   -0.608637   -0.045175
  C      2.575908    0.605756   -0.036945
  C      0.977551    2.083559   -0.021690
  C     -0.288108    2.687287   -0.011220
  C     -1.529488    2.048274   -0.004419
  C     -3.067756    0.388045    0.001354
  H     -0.976948   -0.007843   -0.015911
  C     -3.608477   -0.899096    0.001258
  C     -2.907149   -2.113434   -0.007085
  C     -1.308388   -3.590806   -0.022331
  C     -0.042695   -4.194596   -0.032673
  C      1.198590   -3.555847   -0.039419
  H      0.645751   -1.499625   -0.028098
  C     -3.768181    1.641701    0.010433
  C     -2.832985    2.651061    0.006924
  C      2.228928    2.835679   -0.028158
  C      3.228183    1.912006   -0.037679
  C      3.437220   -3.149227   -0.053963
  C      2.502048   -4.158627   -0.050442
  C     -3.558669   -3.420017   -0.006390
  C     -2.559381   -4.343652   -0.015901
  H     -4.633051   -3.589818    0.000518
  H     -2.644718   -5.427990   -0.018393
  H     -0.016400   -5.285446   -0.035842
  H      2.681678   -5.229875   -0.055110
  H      4.519010   -3.247119   -0.061999
  H      4.366739   -0.548807   -0.052422
  H      2.314239    3.920088   -0.025633
  H      4.302487    2.081864   -0.044563
  H     -0.315062    3.778120   -0.007889
  H     -3.013895    3.722099    0.011827
  H     -4.849852    1.740964    0.018679
  H     -4.697992   -0.958441    0.008649
end
```

```orca
%tddft
  TDA  false
end
```

In this case, all excitations up to 10 eV are considered from the very
beginning. Configurations between 10 and 30 eV are included if their
coupling to the configurations below 10 eV is strong enough (in total
larger than `PThresh`). All configurations beyond 14 eV are neglected.
Note furthermore that for very large systems,
using a functional with the correct asymptotic behaviour is very
important (due to the fixed amount of GGA exchange, CAM-B3LYP does
**not** provide this property).

The ORCA output will summarize the important properties of your
calculation which allows you to check your input:

```orca
---------------------------------------------------------------------------------

                       ORCA sTD-DFT CALCULATION

                       please cite in your paper    
 orginal sTDA method:  S. Grimme, J. Chem. Phys. 138, 244104 (2013)    
 range-separated sTDA: T. Risthaus, A. Hansen, S. Grimme, Phys. Chem. Chem. Phys.
                       16, 14408-14419 (2014) 
 sTD-DFT approach:     C. Bannwarth, S. Grimme, Comp. Theor. Chem. 
                       1040-1041, 45-53 (2014)

---------------------------------------------------------------------------------

spectral range up to (eV)      ...   10.000000
occ. MO cut-off (eV)           ...   -27.751992
virt. MO cut-off (eV)          ...   19.711835
perturbation threshold         ...   1.000e-04 
CSF selection range up to (eV) ...   30.000000
MOs in sTD-DFT                 ...         150 
occ. MOs in sTD-DFT            ...          55  
virt. in sTD-DFT               ...          95  
calculate triplets           ...   no  

Transforming dipole length integrals   ... (read-ok)(trafo-ok)
Transforming dipole velocity integrals ... (read-ok)(trafo-ok)
Transforming ang. momentum integrals   ... (read-ok)(trafo-ok)

SCF atom population (using active MOs):

   4.196   5.171   5.171   4.196   3.616   3.996   3.991   3.991   3.996   3.616
   3.616   0.796   3.996   3.991   3.991   3.996   3.616   0.796   3.893   3.893
   4.040   4.040   3.893   3.893   4.040   4.040   0.971   0.971   0.956   0.957
   0.957   0.956   0.971   0.971   0.956   0.957   0.957   0.956

Number of electrons in sTDA:  110.000

ax(DF)   :  0.3800
s^k      :  2.0000
beta  (J):  1.8600
alpha (K):  0.9000

```

The spectroscopic data is also printed out after the calculation has
finished:

```orca
-----------------------------------------------------------------------------
         ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS
-----------------------------------------------------------------------------
State   Energy  Wavelength   fosc         T2         TX        TY        TZ
        (cm-1)    (nm)                  (au**2)     (au)      (au)      (au)
-----------------------------------------------------------------------------
   0   16964.7    589.5   0.000083715   0.00162   0.02872  -0.02828  -0.00022
   1   19477.4    513.4   0.001269789   0.02146  -0.09723  -0.10958   0.00035
   2   25753.4    388.3   1.245683315  15.92387   2.92682  -2.71234  -0.02807
   3   26309.7    380.1   1.402883697  17.55424   2.84893   3.07209  -0.01073
   4   30311.6    329.9   0.000000355   0.00000  -0.00146  -0.00131   0.00001
   5   32710.4    305.7   0.000000640   0.00001   0.00178  -0.00181   0.00000
   6   33285.3    300.4   0.349285082   3.45464   1.37427  -1.25134  -0.01315
   7   33622.4    297.4   0.097718276   0.95680   0.64724   0.73340  -0.00233
   8   34974.4    285.9   0.000000018   0.00000  -0.00024   0.00024   0.00024
   9   34994.6    285.8   0.000000073   0.00000  -0.00005  -0.00002   0.00082
  10   35723.1    279.9   0.000000022   0.00000  -0.00021  -0.00022  -0.00033
  11   35826.4    279.1   0.008160622   0.07499   0.00215  -0.00104   0.27383
  12   36282.4    275.6   0.000000000   0.00000  -0.00004   0.00000   0.00000
  13   37373.0    267.6   0.000000104   0.00000  -0.00067   0.00067  -0.00012
  14   37439.7    267.1   0.000000030   0.00000   0.00036   0.00037   0.00000
  15   38835.7    257.5   0.101992631   0.86460   0.63387   0.68029  -0.00240
  16   40111.9    249.3   0.000001866   0.00002  -0.00286   0.00267   0.00010
  17   40376.1    247.7   0.119778731   0.97663   0.72310  -0.67358  -0.00678
  18   41527.5    240.8   0.000000020   0.00000   0.00024   0.00031  -0.00000
  19   43202.8    231.5   0.000000006   0.00000   0.00015  -0.00014  -0.00008
  20   45265.3    220.9   0.000000008   0.00000   0.00013  -0.00014   0.00014
  21   46775.7    213.8   0.000000000   0.00000   0.00002   0.00003   0.00001
  22   49449.3    202.2   0.151078886   1.00582   0.73590  -0.68133  -0.00709
  23   51144.8    195.5   0.000000001   0.00000   0.00005  -0.00007   0.00003
  24   51371.9    194.7   0.000000069   0.00000  -0.00047  -0.00047  -0.00000
  25   53195.6    188.0   0.002581321   0.01598   0.00537  -0.00532  -0.12617
  26   53198.4    188.0   0.000000045   0.00000  -0.00031  -0.00038  -0.00020
  27   53341.2    187.5   0.065343188   0.40329   0.46944  -0.42767  -0.00298
  28   54136.6    184.7   0.006562015   0.03990   0.13280   0.14923  -0.00049
  29   54279.9    184.2   0.086565034   0.52502   0.49226   0.53170  -0.00183
  30   54285.4    184.2   0.078803195   0.47790  -0.46967  -0.50725   0.00179
  31   54351.4    184.0   0.000000001   0.00000   0.00005   0.00004  -0.00006
  32   54428.8    183.7   0.000000565   0.00000   0.00124   0.00137  -0.00011
  33   55214.4    181.1   0.130630885   0.77888   0.64617  -0.60109  -0.00629
  34   55671.1    179.6   0.000000219   0.00000   0.00083  -0.00077   0.00011
  35   56264.4    177.7   0.000000097   0.00000   0.00051   0.00055  -0.00000
  36   56499.9    177.0   0.013901825   0.08100  -0.19211  -0.20999   0.00072
  37   56694.8    176.4   0.000000005   0.00000  -0.00012  -0.00011   0.00000
  38   56885.1    175.8   0.000000018   0.00000  -0.00022  -0.00024  -0.00001
  39   57366.4    174.3   0.000144667   0.00083   0.01438   0.02497  -0.00003
  40   57498.6    173.9   0.000000213   0.00000  -0.00082   0.00074  -0.00002
  ...
```

<a id="sec:spectroscopyproperties.tddft.doubles"></a>
## Double-hybrid functionals and Doubles Correction

The program can compute a doubles correction to the CIS excitation
energies. The theory is due to Head-Gordon and
co-workers.[headgordon1994](../../bibliography.md) The basic idea is to compute a perturbative
estimate (inspired by EOM-CCSD theory) to the CIS excited states that is
compatible with the MP2 ground state energy. In many cases this is a
significant improvement over CIS itself and comes at a reasonable cost
since the correction is computed *a posteriori*. Of course, if the CIS
prediction of the excited state is poor, the (D) correction -- being
perturbative in nature -- cannot compensate for qualitatively wrong
excited state wavefunctions.

In addition -- and perhaps more importantly -- the (D) correction is
compatible with the philosophy of the double-hybrid functionals and
should be used if excited states are to be computed with these
functionals. The results are usually much better than those from TD-DFT
since due to the large fraction HF exchange, the self-interaction error
is much smaller than for other functionals and after the (D) correction
the results do not suffer from the overestimation of transition energies
that usually comes with increased amounts of HF exchange in TD-DFT
calculations.

Since the calculations would require a fairly substantial integral
transformation that would limit it to fairly small molecules if no
approximation are introduced we have decided to only implement a RI
version of it. With this approximation systems with more than 1000 basis
functions are readily within the reach of the implementation.

Since one always has a triad of computational steps: MP2-CIS
solution-(D) correction, we have implemented several algorithms that may
each become the method of choice under certain circumstances. The choice
depends on the size of the system, the number of roots, the available
main memory and the available disk space together with the I/O rate of
the system. The formal cost of the (D) correction is $O(N^{5})$ and its
prefactor is higher than that of RI-MP2. In the best case scenario, the
rate limiting step would be the calculation of the pair-contribution in
the "U-term" which requires (for a closed-shell system) twice the effort
of a RI-MP2 calculation *per state*.

The use of the (D)-correction is simple. Simply write:

```orca
! HF DEF2-SVP DEF2-SVP/C TightSCF
%cis dcorr n # n=1-4. The meaning of the four algorithms is
             # explained below.
   # algorithm 1 Is perhaps the best for small systems. May use a
   #             lot of disk space
   # algorithm 2 Stores less integrals
   # algorithm 3 Is good if the system is large and only a few
   #             states are calculated. Saves disk and main
   #             memory.
   # algorithm 4 Uses only transformed RI integrals. May be the
   #             fastest for large systems and a larger number
   #             of states
end
```

<a id="tab:8"></a>
!!! note "Integral handling in various implementations of the (D) correction (i,j=occupied MOs, a,b=virtual MOs, Q=aux function; NumInt=numerical integration)."
    | [**DCORR** $=$]{style="color: white"} | [**1** ]{style="color: white"} | [**2** ]{style="color: white"} | [**3** ]{style="color: white"} | [**4** ]{style="color: white"} |
    |:--------------------------------------|:------------------------------:|:------------------------------:|:------------------------------:|:------------------------------:|
    | **(ia\|jb) integrals**                  |             Stored             |             Stored             |           Not stored           |           Not stored           |
    | **(ij\|ab) integrals**                  |             Stored             |            Not made            |            Not made            |            Not made            |
    | **(ab\|Q) integrals**                   |             Stored             |            Not made            |            Not made            |             Stored             |
    | **(ij\|Q) integrals**                   |             Stored             |             Stored             |             Stored             |             Stored             |
    | **(ia\|Q) integrals**                   |             Stored             |             Stored             |             Stored             |             Stored             |
    | **Coulomb CIS**                         |          From (ia\|jb)         |          From (ia\|jb)         |           From (ia\|Q)         |           From (ia\|Q)         |
    | **Exchange CIS**                        |          From (ij\|ab)         |          RI-AO-direct          |          RI-AO-direct          |           From (ab\|Q)         |
    | **XC-CIS**                              |           Num. Int.            |           Num. Int.            |           Num. Int.            |           Num. Int.            |
    | **V-term in (D)**                       |          From (ia\|jb)         |          From (ia\|jb)         |           From (ia\|Q)         |           From (ia\|Q)         |
    | **U-term in (D)**                       |           From (ab\|Q)         |          RI-AO-direct          |          RI-AO-direct          |           From (ab\|Q)         |

Spin-component scaling versions of CIS(D) can be evoked in the %cis
block by setting DOSCS TRUE and the four scaling parameters, as defined
by Head-Gordon and co-workers [Rhee2007](../../bibliography.md), in the following order:
same-spin indirect term (CTss), opposite-spin indirect term(CTos),
same-spin direct term(CUss), and opposite-spin direct term(CUos). Note
that this implementation only works for the version with the parameter
$\lambda=1$ as defined in Ref. [Rhee2007](../../bibliography.md). The example below shows how
to apply the SCS-CIS(D) version with $\lambda=1$ whose usage has been
advocated in Ref. [Goerigk_2010](../../bibliography.md). The user is able to specify other
scaling parameters.

```orca
%cis
dcorr     # n=1,2,3,4
doscs     true                    # set SCS-CIS(D) to true (default: false) 
scspar    0.333, 1.2, 0.43, 1.24  #SCS-CIS(D) scaling parameters in this order
                                  CTss, CTos, CUss, CUos     
end
```

Note the use of commas to separate the parameters. These parameters do
not communicate with the SCS/SOS parameters set for ground-state
SCS/SOS-MP2 in the %mp2 block.

!!! note
    -   CIS(D) is often a quite big improvement over CIS.

    -   In all three involved code sections (MP2, CIS, (D)) the storage
        format FLOAT is respected. It cuts down use of disk and main memory
        by a factor of two compared the default double precision version.
        The loss of accuracy should be negligible; however it is -- as
        always in science -- better to double check.

    -   The (ab|Q) list of integrals may be the largest for many systems and
        easily occupies several GB of disk space (hence algorithms 2 and 3).
        However, that disk-space is often well invested unless you run into
        I/O bottlenecks.

    -   The (ia|jb) and (ij|ab) lists of integrals is also quite large but is
        relatively efficiently handled. Nevertheless, I/O may be a problem.

    -   The cost of the (D) correction is O(N$^{5})$ and therefore
        comparable to RI-MP2. Since there are quite a few things more to be
        done for (D) compared to RI-MP2, expect the calculations to take
        longer. In the most elementary implementation the cost is about two
        times the time for RI-MP2 for each root.

    -   The (D) correction is compatible with the philosophy of the
        double-hybrid density functionals and should be used if these
        functionals are combined with TD-DFT. The program takes this as the
        default but will not enforce it. The (D) correction can be used both
        in a TD-DFT and TDA-DFT context.

    -   In our implementation it is only implemented together with the RI
        approximation and therefore you need to supply an appropriate ("/C")
        fitting basis.

    -   The program will automatically put the RI-MP2 module into operation
        together with the (D) correction. This will result in the necessary
        integrals becoming available to the CIS module.

    -   Making the exchange contribution to the CIS residual vector in an
        RI-AO direct fashion becomes quite expensive for a larger number of
        states. It may be a good choice if only one or two excited states
        are to be calculated for a larger system.

    -   Singlet-triplet excitations can be calculated by setting TRIPLETS
        TRUE in the %cis or %tddft blocks, respectively. The implementation
        has been tested for double hybrids in Ref. [tripletTDDH](../../bibliography.md).

    -   For spin-adapted triplets (TRIPLETS TRUE), the only option available
        currently is DCORR 1.

    -   Spin-component and spin-opposite scaling techniques for
        double-hybrids within the TD- and TDA-DFT frameworks, as defined by
        Schwabe and Goerigk [schwabetdpbe02017](../../bibliography.md), can be evoked in the same
        way in the %tddft block as described for SCS-CIS(D) above. While
        user-defined parameters can be entered in such a way, a series of
        new functionals are available through normal keywords, which use the
        herein presented SCS/SOS-CIS(D) implementation. [SCSTDDHDFs](../../bibliography.md) See
        Sec. [dft.basicusage](#sec:modelchemistries.dft.basicusage) for a list of those
        functionals.

    -   Usage of time-dependent double-hybrids should be cited as follows:
        For TD or TDA with any double hybrid,[tdtdadftgrimme2007](../../bibliography.md)
        TD-B2GPLYP,[goerigktdb2gplyp2009](../../bibliography.md) TDA-PBE0-DH or
        TDA-PBE0-2,[meotdapbe02013](../../bibliography.md) TD-PBE0-DH, TD-PBE0-2, or TDA-B2GP-PLYP
        [schwabetdpbe02017](../../bibliography.md), TD-$\omega$B2PLYP or TD-$\omega$B2GPPLYP
        [goerigk2019RSDHTDDFT](../../bibliography.md), TDA-$\omega$B2PLYP or TDA-$\omega$B2GPPLYP
        [tripletTDDH](../../bibliography.md), TD(A)-RSX-QIDH or TD(A)-RSX-0DH [tripletTDDH](../../bibliography.md),
        TDA-PBE-QIDH [RSXQIDH](../../bibliography.md), TD-PBE-QIDH [ADAMOIJQC2020](../../bibliography.md),
        TD(A)-DSD-BLYP or TD(A)-DSD-PBEP86 or many other
        spin-component-scaled double-hybrid functionals with TD(A)-DFT from
        2017 [schwabetdpbe02017](../../bibliography.md), TD(A) $\omega$B88PP86 or TD(A)
        $\omega$PBEPP86 or many other spin-component and opposite scaled
        double hybrids with TD(A)-DFT from 2021 [SCSTDDHDFs](../../bibliography.md).

    -   Note that SCS/SOS-CIS(D) is only automatically used when a TD(A)-DFT
        calculation is requested for the functionals from 2021 by
        Casanova-Páez and Goerigk. [SCSTDDHDFs](../../bibliography.md) In those instances,
        \"doscs\" has not to be set. SCS/SOS-CIS(D) is not automatically
        used for PWPB95, $\omega$wB97X-2, or the DSD functionals.

<a id="sec:spectroscopyproperties.tddft.spinorbitcoupling"></a>
## Spin-orbit coupling

It also possible to include spin-orbit coupling between singlets and
triplets calculated from TD-DFT by using quasi-degenerate perturbation
theory (please refer to the relevant publication
[de_souza_phosp_2019](../../bibliography.md)), similarly to what is done in ROCIS. In order to
do that, the flag DOSOC must be set to TRUE. The reduced matrix elements
are printed and the new transition dipoles between all SOC coupled
states are also printed after the regular ones. This option is currently
still not compatible with double hybrids, but works for all other cases
including CPCM. All the options regarding the SOC integrals can be
altered in the %rel block, as usual.

```orca
%CIS DOSOC  TRUE END
```

Please have in mind that, as it is, you can only calculate the SOC
between excited singlets and the spin-adapted triplets. There is no SOC
starting from a UHF/UKS wavefunction. If you want more information
printed such as the full SOC matrix or triplet-triplet couplings, please
set a higher PRINTLEVEL.

<a id="sec:spectroscopyproperties.tddft.spinorbitcoupling.ECPs"></a>
### SOC and ECPs 

ORCA currently does not have SOC integrals for ECPs, and these are by
default ignored in the SOC module. If you try to use ORCA together with
ECPs, an abort message will be printed. If you absolutely need to use
ECPs, for instance for embedded potentials, please use:

```orca
%TDDFT FORCEECP TRUE END
```

OBS.: Do not use ECPs in atoms where SOC might be important. In that
case, always use all-electron basis functions or the results will not
make sense.

<a id="sec:spectroscopyproperties.tddft.natTransOrb"></a>
## Natural Transition Orbitals

Results of TD-DFT or CIS calculations can be tedious to interprete as
many individual MO pairs may contribute to a given excited state. In
order to facilitate the analysis while keeping the familiar picture of
an excited state originating from essentially an electron being promoted
from a donor orbital to an acceptor orbital, the concept of \"natural
transition orbitals\" can be used.

The procedure is quite straightforward. For example, consider the
following job on the pyridine molecule:

```mol
title: structure 12
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
11
structure (0 1)
N      0.000000     0.000000     1.401146
C      0.000000     1.146916     0.702130
C      0.000000    -1.146916     0.702130
C     -0.000000     1.205574    -0.702848
C     -0.000000    -1.205574    -0.702848
C      0.000000    -0.000000    -1.421344
H     -0.000000     2.079900     1.297897
H     -0.000000    -2.079900     1.297897
H     -0.000000     2.179600    -1.219940
H     -0.000000    -2.179600    -1.219940
H      0.000000     0.000000    -2.525017
--- input ---
! PBE def2-SVP tightscf 

%tddft 
 nroots 5
 DoNTO  true      # flag to turn on generation of natural transition orbitals
 NTOStates 1,2,3  # States to consider for NTO analysis; 
                  # if empty all will be done
 NTOThresh 1e-4   # threshold for printing occupation numbers  
end

* xyz 0 1 
  N      0.000000    0.000000    1.401146
  C      0.000000    1.146916    0.702130
  C      0.000000   -1.146916    0.702130
  C     -0.000000    1.205574   -0.702848
  C     -0.000000   -1.205574   -0.702848
  C      0.000000   -0.000000   -1.421344
  H     -0.000000    2.079900    1.297897
  H     -0.000000   -2.079900    1.297897
  H     -0.000000    2.179600   -1.219940
  H     -0.000000   -2.179600   -1.219940
  H      0.000000    0.000000   -2.525017
*
```

```mol
title: structure 13
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
3
structure (0 3)
C             0            0       0.1058
H             0       0.9910      -0.3174
H             0      -0.9910      -0.3174
--- input ---
!def2-SVP USESYM 

%TDDFT 
 SF TRUE 
END

* xyz 0 3 
 C 0  0       0.1058
 H 0  0.9910 -0.3174
 H 0 -0.9910 -0.3174
*
```

which results in:

```orca
------------------------------------------
NATURAL TRANSITION ORBITALS FOR STATE    1
------------------------------------------

Making the (pseudo)densities                       ... done
Solving eigenvalue problem for the occupied space  ... done
Solving eigenvalue problem for the virtual space   ... done
Natural Transition Orbitals were saved in example10.s1.nto
Threshold for printing occupation numbers 0.000100

 E=   0.157831 au      4.295 eV    34639.9 cm**-1
    20a ->  21a  : n=  0.99945993
    19a ->  22a  : n=  0.00018772
    18a ->  23a  : n=  0.00018562

------------------------------------------
NATURAL TRANSITION ORBITALS FOR STATE    2   
------------------------------------------

Making the (pseudo)densities                       ... done
Solving eigenvalue problem for the occupied space  ... done
Solving eigenvalue problem for the virtual space   ... done
Natural Transition Orbitals were saved in example10.s2.nto
Threshold for printing occupation numbers 0.000100

 E=   0.158973 au      4.326 eV    34890.5 cm**-1
    20a ->  21a  : n=  0.99857289
    19a ->  22a  : n=  0.00054014
    18a ->  23a  : n=  0.00039643
    17a ->  24a  : n=  0.00029339

------------------------------------------
NATURAL TRANSITION ORBITALS FOR STATE    3   
------------------------------------------

Making the (pseudo)densities                       ... done
Solving eigenvalue problem for the occupied space  ... done
Solving eigenvalue problem for the virtual space   ... done
Natural Transition Orbitals were saved in example10.s3.nto
Threshold for printing occupation numbers 0.000100

 E=   0.200016 au      5.443 eV    43898.4 cm**-1
    20a ->  21a  : n=  0.63243468
    19a ->  22a  : n=  0.36314467
    18a ->  23a  : n=  0.00120185
    17a ->  24a  : n=  0.00103035
    16a ->  25a  : n=  0.00063379
    15a ->  26a  : n=  0.00051555
    14a ->  27a  : n=  0.00040257
    13a ->  28a  : n=  0.00020605
    12a ->  29a  : n=  0.00013070
    11a ->  30a  : n=  0.00010297

-----------------------------
TD-DFT/TDA-EXCITATION SPECTRA
-----------------------------

Center of mass = (  0.0000,  0.0000,  0.0036)
Generating CIS transition densities           ... done

----------------------------------------------------------------------------------------------------
                     ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS
----------------------------------------------------------------------------------------------------
     Transition      Energy     Energy  Wavelength fosc(D2)      D2        DX        DY        DZ
                      (eV)      (cm-1)    (nm)                 (au**2)    (au)      (au)      (au)
----------------------------------------------------------------------------------------------------
  0-1A  ->  1-1A    4.294795   34639.9   288.7   0.000000000   0.00000   0.00000  -0.00000  -0.00000
  0-1A  ->  2-1A    4.325874   34890.5   286.6   0.003830922   0.03615   0.19012   0.00000   0.00000
  0-1A  ->  3-1A    5.442702   43898.4   227.8   0.019114326   0.14335   0.00000  -0.37861   0.00000
  0-1A  ->  4-1A    6.579556   53067.7   188.4   0.017637721   0.10942   0.00000   0.00000   0.33078
  0-1A  ->  5-1A    6.739163   54355.0   184.0   0.007560799   0.04579  -0.00000  -0.00000   0.21399
```

We see that there is a weakly allowed transition (STATE 2) that is
essentially totally composed of a single NTO pair
(20a$\rightarrow$21a : n= 0.99857289), while the third
excited state (S3) is strongly allowed and requires two NTO pairs for
its description (20a$\rightarrow$21a : n= 0.63243468
and 19a$\rightarrow$22a : n= 0.36314467).

These orbitals are shown below. It is evident that the state 2 donor
orbital (NTO20) is a nitrogen lone pair and the acceptor orbital is a
$\pi*$ orbital of the ring. For the state 3 the two NTO donor orbitals
are comprised of a nearly degenerate set of $\pi$ orbitals (they would
be degenerate in the parent benzene) and the acceptor orbitals are a
pair of nearly degenerate $\pi*$ orbitals. It is evident from this
example that by looking at the NTOs one can obtain a nicely pictorial
view of the transition process, even if many orbital pairs contribute to
a given excited state in the canonical basis.

<a id="fig:742"></a>
*Natural transition orbitals for the pyridine molecule in state 2 and state 3.*

Similar analysis can be performed in the case of ROCIS and DFT/ROCIS
calculations as it will be described in section
[rocis.natTransOrb](#sec:spectroscopyproperties.rocis.natTransOrb).

<a id="sec:spectroscopyproperties.tddft.compute"></a>
## Computational Aspects

<a id="sec:spectroscopyproperties.tddft.compute.aobasis"></a>
### RI Approximation (AO-Basis) 

If the SCF calculation used the RI approximation it will also be used in
the TD-DFT calculation. The RI approximation saves a large amount of
time while giving close to identical results (the errors will usually be
$<$0.1 eV) and is generally recommended. If the
functional is a hybrid functional the RI-approximation will only be
applied to the Coulomb term while the exchange will be treated as
before. In the SCF you can use this feature with the keyword
(`! RIJONX`). It will then also be used in the TD-DFT calculation.
Again, the RIJCOSX approximation can be used in TD-DFT and CIS
calculations and leads to very large speedups at virtually no loss in
accuracy.

<a id="sec:spectroscopyproperties.tddft.compute.integral"></a>
### Integral Handling

If the SCF calculation is carried out in an integral direct fashion this
will also be done in the CIS/TD-DFT calculation. Thus, no bottlenecks
arising from large integral transformations or large disk space
requirement arise in the calculations. An exception is the MO based RI
approximations described in the previous section.

<a id="sec:spectroscopyproperties.tddft.compute.valence"></a>
### Valence versus Rydberg States

For valence excited states the usual orbital basis sets are reasonable.
Thus, with polarized double-zeta basis sets sensible results are
obtained. Especially DFT calculations have the nice feature of not being
overly basis set dependent.

If Rydberg states are desired, you should make sure that diffuse
functions are present in your basis set. You could always use the
augmented-specific basis, e.g. DEF2-TZVPD, ma-DEF2-TZVP, or aug-cc-pVTZ,
or add some extra diffuse basis to your regular basis. These can be
added to any "normal" basis set. For example, the following example
provides a rather high quality basis for excited state calculations that
is based on the Ahlrichs basis set:

```orca
%basis 
  # augment the carbon basis set by diffuse functions
  addgto 6
    s 1
       1 0.01 1.0
    p 1
       1 0.01 1.0
    d 1
       1 0.07 1.0
    end
end
```

!!! note
    If you want to augment a given basis set it is sensible to run a
    preliminary SCF calculation and use `%output print[p_basis] 2 end`.
    This will provide you with a detailed listing of basis functions and
    their exponents. You can then add additional s, p and perhaps
    d-functions with the `AddGTO` command as in the example above. It is
    sensible to decrease the exponent of the diffuse functions by
    roughly a factor of 3 from the smallest exponent in the original
    basis.

<a id="sec:spectroscopyproperties.tddft.compute.restrictionsRS"></a>
### Restrictions for Range-Separated Density Functionals

Several restrictions apply for range-separated (hybrid as well as
double-hybrid) density functionals. They are currently only implemented
to work with the AO-based algorithm within the RIJONX, RIJCOSX, and NORI
integral schemes. Additionally, the asymptotic correction has been disabled.
However, the nuclear gradient for the excited states is now available,
including for the triplets. Please no that the IROOTMULT flag must be
set to TRIPLET under %CIS or %TDDFT in order to obtain that.

<a id="sec:spectroscopyproperties.tddft.compute.printGrad"></a>
### Printing Extra Gradients Sequentially

If you want to print extra gradients for external applications or any
other reason, you can use the keywords SGRADLIST and TGRADLIST, for
singlets and triplets. This will print the gradients sequentially after
the CIS/TDDFT run. If you put 0 on the singlet list, the ground state
gradient will also be added, always at the end.

```orca
%TDDFT SGRADLIST  0, 1, 2
       TGRADLIST  2, 3 
END
```

In order to save this gradients in a text file, please use:

```orca
%METHOD STORECISGRAD TRUE END
```

<a id="sec:spectroscopyproperties.tddft.restart"></a>
## Restarting TD-DFT Calculations 

TD-DFT amplitudes are stored by default in the GBW file. This also means that TD-DFT calculations can be restarted, if a suitable GBW file is provided. The restart is relatively flexible. It allows for the geometry, basis set or density functional to change between the source and target calculation. However, the source calculation must at least have the same number of roots than the target calculation or more, fewer roots in the source is not allowed.  
Here is a simple example: 

```orca
* gzmt 0 1 
  O
  H  1 1.0 
  H  1 1.0 2 104.0
*

%compound
 New_Step 
   ! B3LYP def2-SVP def2/J VeryTightSCF PModel 
   %Base "FirstJob"
   %cis nroots   10
        triplets true
        tda      true
        end 
  Step_end
 
  New_Step
   ! B3LYP def2-SVP def2/J VeryTightSCF 
   %Base "SecondJob"
   %cis nroots   10
        triplets true
        tda      true
        Restart "FirstJob.gbw" 
        end 
  Step_end
 
endrun; 
```
 
!!! note
    - This is supposed to work for all combinations of TDA or RPA, singlets and triplets and also for spin-flip TD-DFT calculations. 
    - We make several consistency checks but it will certainly be possible to create nonsensical inputs that will fail – please proceed with caution. 

<a id="sec:spectroscopyproperties.tddft.xas"></a>
## Use of TD-DFT for the Calculation of X-ray Absorption Spectra

In principle X-ray absorption spectra are "normal" absorption spectra
that are just taken in a special high-energy wavelength range. Due to
the high energy of the radiation employed (several thousand eV),
core-electrons rather than valence electrons are excited. This has two
consequences: a) the method becomes element specific because the
core-level energies divide rather cleanly into regions that are specific
for a given element. b) the wavelength of the radiation is so short that
higher-order terms in the expansion of the light-matter interaction
become important. Most noticeably, quadrupole intensity becomes
important.

X-ray absorption spectra can be generally divided into three regions: a)
the pre-edge that corresponds to transitions of core electrons into low
lying virtual orbitals that lead to bound states. b) the rising edge
that corresponds to excitations to high-lying states that are barely
bound, and c) the extended X-ray absorption fine structure region
(EXAFS) that corresponds to electrons being ejected from the absorber
atom and scattered at neighbouring atoms.

With the simple TD-DFT calculations described here, one focuses the
attention on the pre-edge region. Neither the rising edge nor the EXAFS
region are reasonably described with standard electronic structure
methods and no comparison should be attempted. In addition, these
calculations are restricted to K-edges as the calculation of L-edges is
much more laborious and requires a detailed treatment of the core hole
spin orbit coupling.

It is clearly hopeless to try to calculate enough states to cover all
transitions from the valence to the pre-edge region. Hence, instead one
hand-selects the appropriate donor core orbitals and only allows
excitations out of these orbitals into the entire virtual space. This
approximation has been shown to be justified.[debeer2008jpca](../../bibliography.md) One
should distinguish two situations: First, the core orbital in question
may be well isolated and unambiguously defined. This is usually the case
for metal 1s orbitals if there is only one metal of the given type in
the molecule. Secondly, there may be several atoms of the same kind in
the molecule and their core orbitals form the appropriate symmetry
adapted linear combinations dictated by group theory. In this latter
case special treatment is necessary: The sudden approximation dictates
that the excitations occurs from a local core orbital. In previous
versions of the program you had to manually localize the core holes. In
the present version there is an automatic procedure that is described
below.

A typical example is TiCl$_4$. If we want to calculate the titanium
K-edge, the following input is appropriate:

```orca
! BP86 x2c x2c-SVPall x2c/J TightSCF 

%tddft   
 OrbWin[0] = 0,0,-1,-1
 NRoots 25
 DecomposeFosc true
 DoFullSemiclassical true
end 

* int 0 1 
 Ti 0 0 0  0 0 0 
 Cl 1 2 3 2.15 0 0 
 Cl 1 2 3 2.15 109.4712 0
 Cl 1 2 3 2.15 109.4712 120 
 Cl 1 2 3 2.15 109.4712 240 
*
```

```orca
---------------------
SF-CIS EXCITED STATES
---------------------

the weight of the individual excitations are printed if larger than 1.0e-02

UHF/UKS reference: multiplicity estimated based on rounded <S**2> value, RELEVANCE IS LIMITED!

(SPIN-FLIP GROUND STATE)
STATE  1:  E=   0.005456 au      0.148 eV     1197.5 cm**-1 <S**2> =   2.041850 Sym: B1 Mult 3
     1a ->   3b  :     0.017437 (c= -0.13204740)
     3a ->   3b  :     0.465217 (c=  0.68206845)
     3a ->   9b  :     0.026214 (c=  0.16190881)
     4a ->   4b  :     0.443967 (c= -0.66630872)
     4a ->  10b  :     0.028255 (c= -0.16809333)

STATE  2:  E=   0.058434 au      1.590 eV    12824.9 cm**-1 <S**2> =   0.022791 Sym: A1 Mult 1
     3a ->   4b  :     0.128149 (c= -0.35797971)
     4a ->   3b  :     0.810350 (c=  0.90019420)
     4a ->   9b  :     0.032289 (c=  0.17969015)

STATE  3:  E=   0.079264 au      2.157 eV    17396.4 cm**-1 <S**2> =   0.032278 Sym: B1 Mult 1
     3a ->   3b  :     0.446020 (c= -0.66784709)
     3a ->   9b  :     0.018620 (c= -0.13645512)
     4a ->   4b  :     0.494589 (c= -0.70327031)
     4a ->  10b  :     0.023225 (c= -0.15239893)
```

!!! note
    -   The absolute transition energies from such calculations are off by a
        few hundred electron volts due to the shortcomings of DFT. The shift
        is constant and very systematic for a given element. Hence,
        calibration is possible and has been done for a number of edges
        already. Calibration depends on the basis set!

    -   Electric quadrupole contributions and magnetic dipole contributions have
        been invoked with `DecomposeFosc true` (check section [spectroscopyproperties.ops](#sec:spectroscopyproperties.ops)
        for more information), which is essential for metal edges. For ligand 
        edges, the contributions are much smaller.

    -   `OrbWin` is used to select the single donor orbital (in this case
        the metal 1s). The LUMO (45) and last orbital in the set (174) are
        selected automatically if "-1" is given. This is different from
        previous program versions where the numbers had to be given
        manually.

The output contains standard TD-DFT output:

```orca
----------------------------------------------------------------------------------------------------
                     ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS    
----------------------------------------------------------------------------------------------------
     Transition      Energy     Energy  Wavelength fosc(D2)      D2        DX        DY        DZ   
                      (eV)      (cm-1)    (nm)                 (au**2)    (au)      (au)      (au)  
----------------------------------------------------------------------------------------------------
  0-1A  ->  1-1A   4864.738909 39236769.5     0.3   0.000000000   0.00000  -0.00000   0.00000   0.00000
  0-1A  ->  2-1A   4864.738936 39236769.7     0.3   0.000000000   0.00000   0.00000   0.00000  -0.00000
  0-1A  ->  3-1A   4865.587026 39243610.0     0.3   0.000378325   0.00000  -0.00041   0.00173   0.00000
  0-1A  ->  4-1A   4865.587084 39243610.5     0.3   0.000378325   0.00000  -0.00000  -0.00000   0.00178
  0-1A  ->  5-1A   4865.587090 39243610.6     0.3   0.000378325   0.00000   0.00173   0.00041   0.00000
  0-1A  ->  6-1A   4868.943422 39270681.2     0.3   0.000000000   0.00000   0.00000   0.00000   0.00000
  0-1A  ->  7-1A   4872.449970 39298963.4     0.3   0.000822318   0.00001   0.00000  -0.00000  -0.00262
  0-1A  ->  8-1A   4872.450113 39298964.6     0.3   0.000822428   0.00001   0.00168  -0.00202   0.00000
  0-1A  ->  9-1A   4872.450248 39298965.7     0.3   0.000822896   0.00001   0.00202   0.00168  -0.00000
  0-1A  -> 10-1A   4873.185027 39304892.1     0.3   0.000000000   0.00000   0.00000   0.00000  -0.00000
  0-1A  -> 11-1A   4873.752986 39309473.0     0.3   0.001152303   0.00001   0.00035  -0.00309   0.00000
  0-1A  -> 12-1A   4873.753219 39309474.8     0.3   0.001152646   0.00001  -0.00001   0.00000   0.00311
  0-1A  -> 13-1A   4873.753350 39309475.9     0.3   0.001152359   0.00001  -0.00309  -0.00035  -0.00001
  0-1A  -> 14-1A   4873.877226 39310475.0     0.3   0.000000003   0.00000  -0.00000   0.00000   0.00000
  0-1A  -> 15-1A   4873.877345 39310476.0     0.3   0.000000000   0.00000   0.00000   0.00000   0.00000
  0-1A  -> 16-1A   4881.110098 39368812.1     0.3   0.000000000   0.00000  -0.00000  -0.00000  -0.00000
  0-1A  -> 17-1A   4881.110123 39368812.3     0.3   0.000000000   0.00000  -0.00000  -0.00000   0.00000
  0-1A  -> 18-1A   4883.621665 39389069.2     0.3   0.000014919   0.00000   0.00021  -0.00029  -0.00000
  0-1A  -> 19-1A   4883.621737 39389069.8     0.3   0.000014917   0.00000  -0.00000   0.00000  -0.00035
  0-1A  -> 20-1A   4883.621842 39389070.7     0.3   0.000014922   0.00000   0.00029   0.00021  -0.00000
  0-1A  -> 21-1A   4884.177852 39393555.2     0.3   0.000158653   0.00000  -0.00069   0.00092   0.00000
  0-1A  -> 22-1A   4884.178076 39393557.0     0.3   0.000158639   0.00000  -0.00092  -0.00069   0.00001
  0-1A  -> 23-1A   4884.178104 39393557.2     0.3   0.000158643   0.00000  -0.00001  -0.00001  -0.00115
  0-1A  -> 24-1A   4885.935396 39407730.7     0.3   0.000000000   0.00000   0.00000   0.00000   0.00000
  0-1A  -> 25-1A   4885.941881 39407783.0     0.3   0.000000000   0.00000  -0.00000  -0.00000   0.00000
```

One may obtain origin independent transition
moments formulations which can be combined with the multipole moments up
to 2nd order to regenerate the electric dipole, electric quadrupole and
magnetic dipole contributions in either length or the velocity
representations. This requires in addition to the electric dipole (D),
electric quadrupole (Q) and magnetic dipole (m) intensities the
corresponding electric dipole - magnetic quadrupole (DM) and the
electric dipole - electric octupole (DO)
intensities.[lungberg2016](../../bibliography.md)[jacob2012](../../bibliography.md). See also section
[excitedstates.rocis](#sec:spectroscopyproperties.excitedstates.rocis).

These spectra are requested by:

```orca
DecomposeFosc   true   
```

Check section [spectroscopyproperties.ops](#sec:spectroscopyproperties.ops) for more information.

Resulting in:

```orca
--------------------------------------------------------------------------------------------------------------------------------
                     ABSORPTION SPECTRUM COMBINED ELECTRIC DIPOLE + MAGNETIC DIPOLE + ELECTRIC QUADRUPOLE SPECTRUM (Origin Independent, Length)
--------------------------------------------------------------------------------------------------------------------------------
     Transition      Energy     Energy  Wavelength fosc(D2)  fosc(M2)  fosc(Q2) fosc(D2+M2+Q2+DM+DO) D2/TOT    M2/TOT    Q2/TOT
                      (eV)      (cm-1)    (nm)       (au)    (au*1e6)  (au*1e6)
--------------------------------------------------------------------------------------------------------------------------------
  0-1A  ->  1-1A   4864.738909 39236769.5     0.3     0.00000   0.00000   3.57414   0.00000357413611   0.00000   0.00000   1.00000
  0-1A  ->  2-1A   4864.738936 39236769.7     0.3     0.00000   0.00000   3.57419   0.00000357419113   0.00000   0.00000   1.00000
  0-1A  ->  3-1A   4865.587026 39243610.0     0.3     0.00038   0.00000   2.91269   0.00014515284191   2.60639   0.00000   0.02007
  0-1A  ->  4-1A   4865.587084 39243610.5     0.3     0.00038   0.00000   2.91280   0.00014514667816   2.60650   0.00000   0.02007
  0-1A  ->  5-1A   4865.587090 39243610.6     0.3     0.00038   0.00000   2.91281   0.00014515283005   2.60639   0.00000   0.02007
  0-1A  ->  6-1A   4868.943422 39270681.2     0.3     0.00000   0.00000   0.00000   0.00000000001034   0.12373   0.00000   0.00436
  0-1A  ->  7-1A   4872.449970 39298963.4     0.3     0.00082   0.00000  66.02903   0.00020716626448   3.96936   0.00000   0.31872
  0-1A  ->  8-1A   4872.450113 39298964.6     0.3     0.00082   0.00000  66.03525   0.00020716617979   3.96990   0.00000   0.31875
  0-1A  ->  9-1A   4872.450248 39298965.7     0.3     0.00082   0.00000  66.06697   0.00020743853075   3.96694   0.00000   0.31849
  0-1A  -> 10-1A   4873.185027 39304892.1     0.3     0.00000   0.00000   0.00000   0.00000000001255   1.59564   0.00000   0.11619
  0-1A  -> 11-1A   4873.752986 39309473.0     0.3     0.00115   0.00000  65.17922   0.00112267473065   1.02639   0.00000   0.05806
  0-1A  -> 12-1A   4873.753219 39309474.8     0.3     0.00115   0.00000  65.20318   0.00112279513057   1.02659   0.00000   0.05807
  0-1A  -> 13-1A   4873.753350 39309475.9     0.3     0.00115   0.00000  65.18429   0.00112283712761   1.02629   0.00000   0.05805
  0-1A  -> 14-1A   4873.877226 39310475.0     0.3     0.00000   0.00000   0.95985   0.00000096238863   0.00274   0.00000   0.99737
  0-1A  -> 15-1A   4873.877345 39310476.0     0.3     0.00000   0.00000   0.95957   0.00000096000219   0.00031   0.00000   0.99955
  0-1A  -> 16-1A   4881.110098 39368812.1     0.3     0.00000   0.00000  59.20440   0.00005920440172   0.00000   0.00000   1.00000
  0-1A  -> 17-1A   4881.110123 39368812.3     0.3     0.00000   0.00000  59.20493   0.00005920493511   0.00000   0.00000   1.00000
  0-1A  -> 18-1A   4883.621665 39389069.2     0.3     0.00001   0.00000   1.60824  -0.00004102527947  -0.36365  -0.00000  -0.03920
  0-1A  -> 19-1A   4883.621737 39389069.8     0.3     0.00001   0.00000   1.60871  -0.00004102945913  -0.36356  -0.00000  -0.03921
  0-1A  -> 20-1A   4883.621842 39389070.7     0.3     0.00001   0.00000   1.60930  -0.00004103096489  -0.36367  -0.00000  -0.03922
  0-1A  -> 21-1A   4884.177852 39393555.2     0.3     0.00016   0.00000   7.33000  -0.00001710675356  -9.27427  -0.00000  -0.42849
  0-1A  -> 22-1A   4884.178076 39393557.0     0.3     0.00016   0.00000   7.32938  -0.00001711175162  -9.27075  -0.00000  -0.42832
  0-1A  -> 23-1A   4884.178104 39393557.2     0.3     0.00016   0.00000   7.32928  -0.00001712730312  -9.26257  -0.00000  -0.42793
  0-1A  -> 24-1A   4885.935396 39407730.7     0.3     0.00000   0.00000   0.00000  -0.00000000000329  -1.98584  -0.00000  -0.11175
  0-1A  -> 25-1A   4885.941881 39407783.0     0.3     0.00000   0.00017   0.00000   0.00000000016832   0.01099   1.00335   0.00021
```

The multipole moments up to 2nd order:

-   Only approximate origin independence is achieved by using the length
    approximation for distances from the excited atom up to about 5
    Angstrom.

-   Can form negative intensities which can be partly cured by using
    larger basis sets.

Starting from ORCA version 6.0 the full semi-classical ligth-matter interaction[jacob2012](../../bibliography.md)[List2017](../../bibliography.md)[List2020](../../bibliography.md)
can be computed by including the keyword:

```orca
DoFullSemiclassical true
```

Resulting in:

```orca
-----------------------------------------------------------------------------
                     ABSORPTION SPECTRUM VIA FULL SEMI-CLASSICAL FORMULATION
-----------------------------------------------------------------------------
     Transition      Energy     Energy  Wavelength   fosc(FFMIO)
                      (eV)      (cm-1)    (nm)
-----------------------------------------------------------------------------
  0-1A  ->  1-1A   4864.738909 39236769.5     0.3     0.00000225252009
  0-1A  ->  2-1A   4864.738936 39236769.7     0.3     0.00000225274848
  0-1A  ->  3-1A   4865.587026 39243610.0     0.3     0.00021278365996
  0-1A  ->  4-1A   4865.587084 39243610.5     0.3     0.00021278361154
  0-1A  ->  5-1A   4865.587090 39243610.6     0.3     0.00021278187385
  0-1A  ->  6-1A   4868.943422 39270681.2     0.3     0.00000000000237
  0-1A  ->  7-1A   4872.449970 39298963.4     0.3     0.00024200529569
  0-1A  ->  8-1A   4872.450113 39298964.6     0.3     0.00024205635341
  0-1A  ->  9-1A   4872.450248 39298965.7     0.3     0.00024227298357
  0-1A  -> 10-1A   4873.185027 39304892.1     0.3     0.00000000004292
  0-1A  -> 11-1A   4873.752986 39309473.0     0.3     0.00086416333614
  0-1A  -> 12-1A   4873.753219 39309474.8     0.3     0.00086431970479
  0-1A  -> 13-1A   4873.753350 39309475.9     0.3     0.00086419143873
  0-1A  -> 14-1A   4873.877226 39310475.0     0.3     0.00000011039866
  0-1A  -> 15-1A   4873.877345 39310476.0     0.3     0.00000010856486
  0-1A  -> 16-1A   4881.110098 39368812.1     0.3     0.00000159577723
  0-1A  -> 17-1A   4881.110123 39368812.3     0.3     0.00000159558300
  0-1A  -> 18-1A   4883.621665 39389069.2     0.3     0.00000254791052
  0-1A  -> 19-1A   4883.621737 39389069.8     0.3     0.00000254735746
  0-1A  -> 20-1A   4883.621842 39389070.7     0.3     0.00000254890168
  0-1A  -> 21-1A   4884.177852 39393555.2     0.3     0.00008141388446
  0-1A  -> 22-1A   4884.178076 39393557.0     0.3     0.00008141175909
  0-1A  -> 23-1A   4884.178104 39393557.2     0.3     0.00008140437907
  0-1A  -> 24-1A   4885.935396 39407730.7     0.3     0.00000000004646
  0-1A  -> 25-1A   4885.941881 39407783.0     0.3     0.00000000003815
```

The full-semiclassical transition moments:

-   Behave like the multipole expansion in the velocity representation.

-   They are by definition origin independent they do not suffer from
    artificial negative values like the multipole moments beyond 1st
    order.

!!! note
    -   For information on plotting the obtained spectra check [utilities.mapspc](#sec:utilities.mapspc)

Now, let us turn to the Cl K-edge. Looking at the output of the first
calculation, we have:

```orca
----------------
ORBITAL ENERGIES
----------------

  NO   OCC          E(Eh)            E(eV)
   0   2.0000    -178.943613     -4869.3033
   1   2.0000    -101.066445     -2750.1578
   2   2.0000    -101.066399     -2750.1565
   3   2.0000    -101.066377     -2750.1559
   4   2.0000    -101.066372     -2750.1558
   5   2.0000     -19.810459      -539.0700
   6   2.0000     -16.410626      -446.5558
   7   2.0000     -16.410625      -446.5558
   8   2.0000     -16.410625      -446.5558
   9   2.0000      -9.272000      -252.3039
  10   2.0000      -9.271962      -252.3029
  11   2.0000      -9.271945      -252.3024
  12   2.0000      -9.271940      -252.3023
  ...
```

And looking at the energy range or the orbital composition, we find that
orbitals 1 through 4 are Cl 1s-orbitals. They all have the same energy
since they are essentially non-interacting. Hence, we can localize them
without invalidating the calculation. To this end, you can invoke the
automatic localization for XAS which modifies the input to:

```orca
! BP86 x2c x2c-SVPall x2c/J TightSCF 

%tddft   
 XASLoc[0] = 1,4 
 OrbWin[0] = 1,1,-1,-1
 NRoots    25  
 DecomposeFosc  true
 DoFullSemiclassical true
end

* int 0 1 
 Ti 0 0 0  0 0 0 
 Cl 1 2 3 2.15 0 0 
 Cl 1 2 3 2.15 109.4712 0
 Cl 1 2 3 2.15 109.4712 120 
 Cl 1 2 3 2.15 109.4712 240 
*
```

!!! note
    -   This localizes the orbitals 1 through 4 of operator 0 (the
        closed-shell) and then allows excitations (arbitrarily) from core
        hole 1 only. You could choose any of the three other localized 1s
        orbitals instead without changing the result. You could even do all
        four core holes simultaneously (they produce identical spectra) in
        which case you have the entire ligand K-edge intensity and not just
        the one normalized to a single chlorine (this would be achieved with
        `OrbWin[0] = 1,4,-1,-1`).

    -   If you have a spin unrestricted calculation, you need to give the
        same `XASLoc` and `OrbWin` information for the spin-down orbitals as
        well.

```mol
title: structure 14
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
10
structure (0 3)
C      -1.39113      0.00000      0.00000
C       0.69557      1.20476      0.00000
C      -0.69557      1.20476      0.00000
C      -0.69557     -1.20476      0.00000
C       0.69557     -1.20476      0.00000
C       1.39113      0.00000      0.00000
H      -1.24291      2.15278      0.00000
H      -1.24291     -2.15278      0.00000
H       1.24291     -2.15278      0.00000
H       1.24291      2.15278      0.00000
--- input ---
!DEF2-TZVPD OPT 

%method
 Method DFT 
 Functional hyb_gga_xc_bhandhlyp
end

%tddft
  SF true
  NRoots  3
end

* xyz 0 3 
  C         -1.39113        0.00000        0.00000
  C          0.69557        1.20476        0.00000
  C         -0.69557        1.20476        0.00000
  C         -0.69557       -1.20476        0.00000
  C          0.69557       -1.20476        0.00000
  C          1.39113        0.00000        0.00000
  H         -1.24291        2.15278        0.00000
  H         -1.24291       -2.15278        0.00000
  H          1.24291       -2.15278        0.00000
  H          1.24291        2.15278        0.00000
*
```

The obtained Cl K-edge absorption is:

```orca
----------------------------------------------------------------------------------------------------
                     ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS    
----------------------------------------------------------------------------------------------------
     Transition      Energy     Energy  Wavelength fosc(D2)      D2        DX        DY        DZ   
                      (eV)      (cm-1)    (nm)                 (au**2)    (au)      (au)      (au)  
----------------------------------------------------------------------------------------------------
  0-1A  ->  1-1A   2745.600263 22144761.9     0.5   0.000527911   0.00001   0.00000   0.00000   0.00280
  0-1A  ->  2-1A   2745.600291 22144762.1     0.5   0.000527960   0.00001  -0.00000  -0.00280   0.00000
  0-1A  ->  3-1A   2746.447743 22151597.3     0.5   0.000444357   0.00001   0.00001  -0.00257  -0.00000
  0-1A  ->  4-1A   2746.447798 22151597.7     0.5   0.000444395   0.00001   0.00000   0.00000  -0.00257
  0-1A  ->  5-1A   2746.458249 22151682.0     0.5   0.001391214   0.00002  -0.00455  -0.00000  -0.00000
  0-1A  ->  6-1A   2749.820836 22178803.1     0.5   0.000108586   0.00000  -0.00127   0.00000  -0.00000
  0-1A  ->  7-1A   2753.309672 22206942.5     0.5   0.000642499   0.00001  -0.00000  -0.00000  -0.00309
  0-1A  ->  8-1A   2753.309873 22206944.1     0.5   0.000643000   0.00001  -0.00004  -0.00309   0.00000
  0-1A  ->  9-1A   2753.320060 22207026.2     0.5   0.001717215   0.00003   0.00505  -0.00002  -0.00000
  0-1A  -> 10-1A   2753.907046 22211760.6     0.5   0.001737693   0.00003  -0.00507  -0.00000   0.00000
  0-1A  -> 11-1A   2754.608481 22217418.1     0.5   0.000027939   0.00000   0.00000   0.00064  -0.00000
  0-1A  -> 12-1A   2754.608709 22217419.9     0.5   0.000027879   0.00000  -0.00000   0.00000   0.00064
  0-1A  -> 13-1A   2754.709845 22218235.6     0.5   0.000149389   0.00000   0.00149  -0.00001   0.00000
  0-1A  -> 14-1A   2754.736803 22218453.0     0.5   0.000681956   0.00001  -0.00001  -0.00318   0.00000
  0-1A  -> 15-1A   2754.736928 22218454.0     0.5   0.000682692   0.00001  -0.00000   0.00000   0.00318
  0-1A  -> 16-1A   2761.966240 22276762.4     0.4   0.000069982   0.00000   0.00000  -0.00000   0.00102
  0-1A  -> 17-1A   2761.966265 22276762.6     0.4   0.000069999   0.00000   0.00000   0.00102   0.00000
  0-1A  -> 18-1A   2764.478344 22297023.9     0.4   0.000309542   0.00000   0.00000  -0.00214  -0.00001
  0-1A  -> 19-1A   2764.478355 22297024.0     0.4   0.000309644   0.00000   0.00000  -0.00001   0.00214
  0-1A  -> 20-1A   2764.662301 22298507.6     0.4   0.000422965   0.00001  -0.00250  -0.00000   0.00000
  0-1A  -> 21-1A   2765.033563 22301502.0     0.4   0.000115414   0.00000   0.00000   0.00131  -0.00000
  0-1A  -> 22-1A   2765.033736 22301503.4     0.4   0.000115508   0.00000   0.00000   0.00000   0.00131
  0-1A  -> 23-1A   2765.243962 22303199.0     0.4   0.000222110   0.00000  -0.00181   0.00000   0.00000
  0-1A  -> 24-1A   2766.796424 22315720.5     0.4   0.000000384   0.00000   0.00000  -0.00000   0.00008
  0-1A  -> 25-1A   2766.796522 22315721.3     0.4   0.000002667   0.00000   0.00000   0.00020   0.00000
```

Quite nice results have been obtained for a number of systems in this way.[ray2007xray](../../bibliography.md)

<a id="sec:spectroscopyproperties.tddft.transientspectra"></a>
## Transient spectra

If one wants to compute transient spectra, or transition dipoles
starting from a given excited state, the option DOTRANS must be set to
TRUE and an IROOT should be given for the initial state (the default is
1). If `DOTRANS ALL` is requested instead, the transition dipoles between
all states are computed. The transient transition dipoles will then be
printed after the normal spectra. This option is currently only
available for CIS/TDA and is done usng the expectation value formalism,
as the other transition dipole moments in ORCA.

```orca
%cis
  DOTRANS  TRUE
           #or
  DOTRANS  ALL
end
```

<a id="sec:spectroscopyproperties.tddft.geometry"></a>
## Excited State Geometry Optimization

For RPA, CIS, TDA and TD-DFT the program can calculate analytic
gradients. With the help of the `IRoot` keyword, a given state can be
selected for geometry optimization. Note however, that if two states
cross during the optimization it may fail to converge or fail to
converge to the desired excited state (see section
[tddft.followiroot](#sec:spectroscopyproperties.tddft.followiroot) below)!

!!! note
    -   If you want to follow a triplet state instead of the singlet, please include
        `IROOTMULT  TRIPLET`.

```orca
!def2-SVP Opt Freq

%cis  
 NRoots    1   
 IRoot     1   
end

* int 0 1 
    C  0 0 0 0.00 0.0     0.00
    O  1 0 0 1.20 0.0     0.00
    H  1 2 0 1.08 120     0.00
    H  1 2 3 1.08 120   180.00
*
```

```orca
---------------------
SF-TDA EXCITED STATES
---------------------

the weight of the individual excitations are printed if larger than 1.0e-02

UHF/UKS reference: multiplicity estimated based on rounded <S**2> value, RELEVANCE IS LIMITED!

(SPIN-FLIP GROUND STATE)
STATE  1:  E=   0.024173 au      0.658 eV     5305.3 cm**-1 <S**2> =   0.023478 Mult 1
    11a ->  19b  :     0.018563 (c= -0.13624537)
    17a ->  20b  :     0.245232 (c=  0.49520915)
    17a ->  27b  :     0.016815 (c= -0.12967111)
    20a ->  19b  :     0.667236 (c=  0.81684517)
    20a ->  25b  :     0.019935 (c= -0.14119296)

STATE  2:  E=   0.032615 au      0.887 eV     7158.1 cm**-1 <S**2> =   2.018056 Mult 3
    11a ->  20b  :     0.015462 (c= -0.12434444)
    17a ->  19b  :     0.448809 (c=  0.66993209)
    17a ->  25b  :     0.017854 (c= -0.13361796)
    20a ->  20b  :     0.460923 (c=  0.67891314)
    20a ->  27b  :     0.024031 (c= -0.15501804)

STATE  3:  E=   0.106201 au      2.890 eV    23308.4 cm**-1 <S**2> =   1.029543 Mult 3
    15a ->  20b  :     0.051523 (c= -0.22698783)
    18a ->  19b  :     0.910633 (c= -0.95427103)
    18a ->  25b  :     0.017352 (c=  0.13172868)
```

Note that this example converges to a saddle point as can be verified
through the numerical frequency calculation:

```orca
-----------------------
VIBRATIONAL FREQUENCIES
-----------------------

Scaling factor for frequencies =  1.000000000  (already applied!)

     0:       0.00 cm**-1
     1:       0.00 cm**-1
     2:       0.00 cm**-1
     3:       0.00 cm**-1
     4:       0.00 cm**-1
     5:       0.00 cm**-1
     6:    -365.27 cm**-1  ***imaginary mode***
     7:     949.68 cm**-1
     8:    1396.45 cm**-1
     9:    1688.28 cm**-1
    10:    3200.58 cm**-1
    11:    3313.95 cm**-1
```

The excited state relaxed density matrixis available from such gradient runs
(`MyJob.cisp` when using the `KeepDens` keyword) and can be used for various types of analysis.

<a id="sec:spectroscopyproperties.tddft.followiroot"></a>
### Root Following Scheme for Difficult Cases

In case there is a root flipping after a step during the geometry
optimization, it might be impossible to converge an excited state
geometry using the regular methods. To help in those cases, the flag
FOLLOWIROOT might be set to TRUE. Then, excited state wavefunction will
be analyzed and compared with the reference one (more below), and the
IROOT will be automatically adjusted to keep homing the target state.

One example of such a calculation is:

```mol
title: structure 15
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
4
structure (0 1)
N           0.0          0.0          0.0
H           0.0          0.0          1.0
H           0.0         -0.9          0.5
H           0.0          0.9          0.5
--- input ---
! wB97X OPT 

%tddft
 NRoots        5   
 IRoot         3   
 FOLLOWIROOT   TRUE
end

* xyz 0 1 
 N 0.0  0.0  0.0 
 H 0.0  0.0  1.0 
 H 0.0 -0.9  0.5 
 H 0.0  0.9  0.5 
*
```

This will ask for an optimization of the third excited state of ammonia.
At some point, there is a state crossing and what was state 3 now
becomes state 2. The algorithm will recognize this and automatically
change the `IROOT` flag, to keep following the same state:

```orca
The IROOT now is:                                ... 2
```

`FOLLOWIROOT` also works with spin-adapted triplets and spin-flip states.

In cases where you want to keep the comparison only with the density
from **the very first** computed excited state, e.g. the one you get on
the first cycle of a geometry optimization, you can use FIRKEEPFIRSTREF, as
in:

```orca
%tddft
  NRoots           5
  IRoot            3
  FOLLOWIROOT      TRUE
  FIRKEEPFIRSTREF  TRUE # default false
end
```

### Criteria to Follow IROOTs - starting from ORCA6

Starting from ORCA6 we have a much more robust algorithm to follow
these excited states, inspired by some of the recent literature
[steinmetzer_pysisyphus_2021](../../bibliography.md) [campetella_following_2020](../../bibliography.md). The 
algorithm now works as follows, after each excited state calculation using CIS/TDDFT:

1. Given a reference state, take all states within an energy difference of up to 
1 eV to it. We don't want to check states that are too far apart in energy. 
Controlled by `%TDDFT FIRENTHRESH 1.0 END`, number in eV.
2. Now take all states with a difference of $\hat{S}^2$ not larger than 0.5.
We don't want to compare singlets to triplets. Controlled by `%TDDFT FIRS2THRESH 0.5 END`.
3. Calculate the overlap between the transition densities of all states with the reference - this is the core part.
4. In case there is ambiguity - that is if two states have overlaps differing by only 0.05 - take the one with the closer transition dipole angle. Controlled by `%TDDFT FIRSTHRESH 0.05 END`.
5. Update the IROOT to the state that went best on all these tests.

!!! note
     These `FIR` keywords are specific to **F**ollow **IR**oot.

Now by default we might also update the reference state from time to time in case
the separation of states is very clear. The way it work is:

1. If the best overlap is larger than `FIRMINOVERLAP`, which is 0.5 by default and
`FIRDYNOVERLAP` is `FALSE`, we will assume that the overlap is good enough and we will always update the 
reference. However, the default is `FIRDYNOVERLAP TRUE`, which means also have a second check for robustness.
2. If `FIRDYNOVERLAP TRUE` and the best overlap is larger than 0.5 (or `FIRMINOVERLAP`),
we will check for the `ratio` between the best and the second best states. If this `ratio` is between 0.3 and 0.6
(controlled by `%TDDFT FIRDYNOVERRATIO 0.3,0.6 END`), it means that there is a clear separation between
the best and the second best and the reference can be updated safely. 
If the ratio is too close to 1, both states are too similar and it would be dangerous to update the reference state. 
If it is too close to zero, they are easy to distinguish and 
we don't need to update the reference yet [steinmetzer_pysisyphus_2021](../../bibliography.md).

!!! warning
    It is important to stress that this will not necessarily solve all
    problems (root flipping can be particularly bad if the system is highly
    symmetric), for the excited states may change too much during the
    optimization. If that happens, it is advisable to restart the
    calculation after some steps and check which IROOT you still want. This
    can also be used when calculating numerical gradients and Hessians, in
    case you suspect of root flipping after the displacements.

!!! warning
    This algorithm is completely general and should work for any excited state
    method, as long as there are transition densities. We will include more
    methods in the future when possible.

<a id="sec:spectroscopyproperties.tddft.SOCgeom"></a>
### Geometry Optimization of SOC States 

If you want to compute geometries for the SOC states, just choose
`SOCGRAD TRUE` and a given `IROOT`. The weigthed "unrelaxed" gradient will
then be calculated after selecting the CIS/TD-DFT states with
contribution larger than 0.01%. Each gradient will be calculated
separately and, after that, the final SOC gradient will be computed as a
weighted sum. Setting `IROOT 0` in this case corresponds to ask for the
SOC ground state, which is NOT necessarily equal to the ground state
from HF/DFT.

<a id="sec:spectroscopyproperties.tddft.scan"></a>
## Potential Energy Surface Scans

ORCA allows the combination the scan feature with CIS or TD-DFT. This
can be used to map out the excited state potential energy surfaces as a
function of one- two- or three parameters. The output of the
"trajectory" run automatically contains the excited state energies in
addition to the ground state energy. For example consider the following
simple job.

```mol
title: structure 16
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
1
structure (0 1)
O             0            0            0
--- input ---
! def2-TZVPD

%method 
 scanguess pmodel  # this assignment forces a PModel guess at each step 
                   # which is often better if diffuse functions are present
end
 
%cis  
NRoots 7   
end

%paras 
 rCO = 0.85,1.45,21;
end

* xyz 0 1 
  O  0  0  0
  C  0  0  {rCO}
*
```

```mol
title: structure 17
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
10
structure (0 3)
C      -1.39113      0.00000      0.00000
C       0.69557      1.20476      0.00000
C      -0.69557      1.20476      0.00000
C      -0.69557     -1.20476      0.00000
C       0.69557     -1.20476      0.00000
C       1.39113      0.00000      0.00000
H      -1.24291      2.15278      0.00000
H      -1.24291     -2.15278      0.00000
H       1.24291     -2.15278      0.00000
H       1.24291      2.15278      0.00000
--- input ---
!DEF2-TZVPD OPT

%method
  Method DFT
  Functional hyb_gga_xc_bhandhlyp
end

%tddft
  SF true
  NRoots  3
  IRoot   2
end

* xyz 0 3
  C         -1.39113        0.00000        0.00000
  C          0.69557        1.20476        0.00000
  C         -0.69557        1.20476        0.00000
  C         -0.69557       -1.20476        0.00000
  C          0.69557       -1.20476        0.00000
  C          1.39113        0.00000        0.00000
  H         -1.24291        2.15278        0.00000
  H         -1.24291       -2.15278        0.00000
  H          1.24291       -2.15278        0.00000
  H          1.24291        2.15278        0.00000
*
```

The output file from this job contains the *total* energies (i.e. the
ground state energy plus the excitation energy) for each excited state
as a function of C-O bondlength as shown below. Howerver, the assignment
of the individual states will change with geometry due to curve
crossings. Thus, the state-to-state correlation must be worked out "by
hand". These calculations are nevertheless very helpful in obtaining at
least a rough idea about excited state energy surfaces.

<a id="fig:79"></a>
*Result of a potential energy surface scan for the excited states of
the CO molecule using the `orca_cis` module.*

<a id="sec:spectroscopyproperties.tddft.scan.normalSurfaceScan"></a>
### Potential Energy Surface Scans along Normal Coordinates

The ground and excited state potential energy surfaces can also be
mapped as a function of normal coordinates. The normal mode trajectory
run is invoked by the keyword `!MTR`. In addition several parameters
have to be specified in the block `%mtr`. The following example
illustrates the use:

First you run a frequency job:

```orca
---------------------
SF-TDA EXCITED STATES
---------------------

the weight of the individual excitations are printed if larger than 1.0e-02

UHF/UKS reference: multiplicity estimated based on rounded <S**2> value, RELEVANCE IS LIMITED!

(SPIN-FLIP GROUND STATE)
STATE  1:  E=   0.028669 au      0.780 eV     6292.1 cm**-1 <S**2> =   0.022484 Mult 1
    11a ->  19b  :     0.018011 (c= -0.13420632)
    17a ->  20b  :     0.293971 (c=  0.54219090)
    17a ->  27b  :     0.017459 (c= -0.13213220)
    20a ->  19b  :     0.611212 (c=  0.78180024)
    20a ->  25b  :     0.023243 (c=  0.15245717)

STATE  2:  E=   0.032738 au      0.891 eV     7185.1 cm**-1 <S**2> =   2.018181 Mult 3
    11a ->  20b  :     0.014963 (c= -0.12232498)
    17a ->  19b  :     0.444520 (c=  0.66672364)
    17a ->  25b  :     0.021443 (c=  0.14643407)
    20a ->  20b  :     0.462361 (c=  0.67997124)
    20a ->  27b  :     0.022005 (c= -0.14834057)

STATE  3:  E=   0.108154 au      2.943 eV    23737.1 cm**-1 <S**2> =   1.030736 Mult 3
    15a ->  20b  :     0.052291 (c= -0.22867148)
    18a ->  19b  :     0.904505 (c= -0.95105480)
    18a ->  25b  :     0.021057 (c= -0.14511042)
```

and then:

```mol
title: structure 18
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
4
structure (0 1)
O      -1.88199      1.42016     -0.00000
C      -1.80947      0.20286      0.00000
H      -2.50488     -0.38174     -0.59212
H      -1.04956     -0.29504      0.59212
--- input ---
!PBE def2-SVP

%tddft   
  NROOTS  5
  UPOP    TRUE
end

* xyz 0 1 
  O         -1.88199        1.42016       -0.00000
  C         -1.80947        0.20286        0.00000
  H         -2.50488       -0.38174       -0.59212
  H         -1.04956       -0.29504        0.59212
*
```

The `HessName` parameter specifies the name of the file which contains
nuclear Hessian matrix calculated in the frequency run. The Hessian
matrix is used to construct normal mode trajectories. The keyword
`MList` provides the list of the normal modes to be scanned. The
parameters `RSteps` and `LSteps` specify the number of steps in positive
and negative direction along each mode in the list. In general, for a
given set of parameters

```orca
mlist m1,m2,...mn
rsteps rm1,rm2,...rmn
lsteps lm1,lm2,...lmn
```

the total number of the displaced geometries for which single point
calculations will be performed is equal to
$\prod\limits_{m_{i} } { \left({r_{m_{i} } +l_{m_{i} } +1} \right)}$.
Thus, in the present case this number is equal to
$\left({ 4+4+1} \right)\left({ 5+5+1} \right)=99$.

The `ddnc` parameter specifies increments $\delta q_{\alpha }$ for
respective normal modes in the list in terms of dimensionless normal
coordinates (DNC's). The trajectories are constructed so that
corresponding normal coordinates are varied in the range from
$-l_{\alpha } \delta q_{\alpha }$ to $r_{\alpha } \delta q_{\alpha }$.
The measure of normal mode displacements in terms DNC's is appropriate
choice since in spectroscopical applications the potential energy
function $U$ is usually expressed in terms of the DNC's. In particular,
in the harmonic approximation $U(q_{\alpha } )$ has a very simple form
around equilibrium geometry:

$$
U=U_{0} +\sum\limits_\alpha^{3N-6} { \frac{\hslash \omega_{\alpha }
}{2}q_{\alpha }^{2} }\qquad \text{(eqn:213)}
$$

where $\omega_{\alpha }$is the vibrational frequency of the $\alpha$-th
mode.

Dimensionless normal coordinate $q_{\alpha }$ can be related to the
vector of atomic Cartesian displacements $\delta \mathrm{X }$
as follows:

$$
q_{\alpha } =\left({ \frac{\omega_{\alpha } }{\hslash } }
\right)^{\frac{1}{2} }\sum\limits_{k=1}^{3N}
{L_{k\alpha } \delta X_{k} \sqrt{ M_{k} } }\qquad \text{(eqn:214)}
$$

where $\left\{{ L_{k\alpha } } \right\}$ is the orthogonal matrix
obtained upon numerical diagonalization of the mass-weighted Hessian
matrix, and $\mathrm{M }$ is the vector of atomic masses.
Accordingly, the atomic Cartesian displacements corresponding to a given
dimensionless normal coordinate $q_{\alpha }$ are given by:

$$
\delta X_{k} =\left({ \frac{\hslash }{\omega_{\alpha } } }
\right)^{\frac{1}{2} }L_{k\alpha } q_{\alpha } \left({ M_{k} }
\right)^{-\frac{1}{2} }\qquad \text{(eqn:215)}
$$

Alternatively, it is possible to specify in the input the Cartesian
increment for each normal mode. In such a case, instead of the `ddnc`
parameter one should use the `dxyz` keyword followed by the values of
Cartesian displacements, for example:

```orca
%mtr
   HessName "ethene.hess"
   modetype normal
   MList 9,13
   RSteps   4,5
   LSteps   4,5
   dxyz     0.01, 0.02 # increments in the Cartesian basis
                       # are given in angstrom units
end
```

For a given Cartesian increment $d_{X,\alpha }$ along the $\alpha$--th
normal mode the atomic displacements are calculated as follows:

$$
\delta X_{k} =\frac{d_{X,\alpha } }{\left\| { \mathrm{T }_{\alpha } }
\right\|}L_{k\alpha } \left({ M_{k} } \right)^{-\frac{1}{2} }\qquad \text{(eqn:216)}
$$

The vector $\mathrm{T }_{\alpha }$ in the Cartesian basis has
components $T_{i\alpha } =L_{k\alpha } \left({ M_{k} } \right)^{-\frac{1}{2} }$ and length (norm)
$\left\| { \mathrm{T }_{k} } \right\|$.

The increment length can also be selected on the basis of an estimate
for the expected change in the total energy $\Delta E$ due to the
displacement according to
eq.[Eq](../modelchemistries/mdci.md#eqn:121).
The value of $\Delta E$ can be specified via the `EnStep` parameter:

```orca
%mtr
   HessName "ethene.hess"
   modetype normal
   MList 9,13
   RSteps   4,5
   LSteps   4,5
   EnStep   0.001, 0.001 # the values are given in Eh
end
```

All quantum chemical methods have to tolerate a certain amount of
numerical noise that results from finite convergence tolerances or other
cutoffs that are introduced into the theoretical procedures. Hence, it
is reasonable to choose $\Delta E$ such that it is above the
characteristic numerical noise level for the given method of
calculation.

At the beginning of the program run the following trajectory files which
can be visualized in gOpenMol will be created:

-   `BaseName.m9.xyz` and `BaseName.m13.xyz` contain trajectories along
    normal modes 9 and 13, respectively.

-   `BaseName.m13s1.m9.xyz - BaseName.m13s5.m9.xyz` contain trajectories
    along normal mode 9 for different fixed displacements along mode 13,
    so that the file `BaseName.m13sn.m9.xyz `corresponds to the $n$-th
    step in the positive direction along mode 13.

-   `BaseName.m13s-1.m9.xyz - BaseName.m13s-5.m9.xyz` contain
    trajectories along normal mode 9 for different fixed displacements
    along mode 13, so that the file `BaseName.m13s-n.m9.xyz `corresponds
    to the $n$-th step in the negative direction along mode 13.

-   `BaseName.m9s1.m13.xyz - BaseName.m9s4.m13.xyz` contain trajectories
    along normal mode 13 for different fixed displacements along mode 9,
    so that the file `BaseName.m9sn.m13.xyz` corresponds to the $n$-th
    step in the positive direction along mode 9.

-   `BaseName.m9s-1.m13.xyz - BaseName.m9s-4.m13.xyz` contain
    trajectories along normal mode 13 for different fixed displacements
    along mode 9, so that the file `BaseName.m9s-n.m13.xyz` corresponds
    to the $n$-th step in the negative direction along mode 9.

The results of energy single point calculations along the trajectories
will be collected in files `BaseName.mtr.escf.S.dat` (for the SCF total
energies) and files `BaseName.mtr.ecis.S.dat` (for the CIS/TDDFT total
energies), where "S" in the suffix of `*.S.dat` filenames provides
specification of the corresponding trajectory in the same way as it was
done for the case of trajectory files `*.xyz` (e.g. `S=”m9s-1.m13”`).
Likewise, the calculated total energies along the trajectories will be
collected in files `BaseName.mtr.emp2.S.dat` in the case of MP2
calculations, `BaseName.mtr.emdci.S.dat `(MDCI),
`BaseName.mtr.ecasscf.S.dat` (CASSCF), `BaseName.mtr.emrci.S.dat`
(MRCI).

!!! note
    In principle normal coordinate trajectories can be performed
    for an arbitrary number normal modes. This implies that in general
    trajectories will contain geometries which involve simultataneous
    displacement along several (\>2) modes. However, trajectory files
    `*.xyz` and corresponding `*.dat` files will be generated only for the
    structures which are simultaneously displaced along not more than 2
    normal coordinates.

<a id="fig:710"></a>
*Result of a potential energy surface scan along C-C stretching normal
coordinate (mode 13 in the present example) for the excited states of
the ethene molecule using the `orca_cis`
module.*

<a id="sec:spectroscopyproperties.tddft.scan.normalModeScan"></a>
### Normal Mode Scan Calculations Between Different Structures

This type of job allows to map PES between two different structures as a
function of normal coordinates. The H$_{2}$O molecule represent a
trivial case which has formally 2 equivalent equilibrium structures
which differ by angle H$_{1}$---O---H$_{2}$ ( 103.5$^{\circ}$ and
256.5$^{\circ}$, respectively, as follows from the BP86/SV(P)
calculations). In such a case the input for the nomal mode trajectory
run would require the calculation of geometry difference between both
structures in terms of the dimensionless normal coordinates. This can be
done in `orca_vib` run as follows :

```orca
> orca_vib water.hess ddnc geom.xyz
```

The second parameter ddnc in the command line invokes the calculation of
geometry difference in terms of the DNC's. Both structures are specified
in the file `geom.xyz` which has a strict format:

```orca
2  3
0
        0.000000      0.000000      0.000000
        0.000000      0.607566      0.770693
        0.000000      0.607566     -0.770693
1
        0.000000      0.000000      0.000000
        0.000000     -0.607566      0.770693
        0.000000     -0.607566     -0.770693
```

The first line of the input specifies the number of the structures and
total number of atoms (2 and 3, respectively). Specification of each
structure in sequence starts with a new line containing the number of
the structure. The number 0 in the second line is used to denote the
reference structure. Note that atomic coordinates should be given in
units of Å and in the same order as in the ORCA input for the frequency
run from which the file `water.hess` was calculated.

At the end of the `orca_vib` run the file `geom.ddnc` is generated. It
contains the geometry difference in terms of the dimensionless normal
coordinates between the structures with nonzero numbers and the
reference one in `geom.xyz` :

```orca
1
1 9
    0       0.000000
    1       0.000000
    2       0.000000
    3       0.000000
    4       0.000000
    5       0.000000
    6       9.091932
    7      -9.723073
    8       0.000000
```

The output file indicates that the structural difference occurs along 2
normal coordinates: 6 (bending mode) and 7 (totally symmetric O---H
stretching mode). On the basis of the calculated displacement pattern
the following input for the normal mode trajectory run between two
structures can be designed:

```orca
------------------------------------------------------------------------------
                 UNRELAXED CIS/TDA DENSITY POPULATION ANALYSIS
                                   IROOT 1
------------------------------------------------------------------------------
------------------------------------------------------------------------------
                           ORCA POPULATION ANALYSIS
------------------------------------------------------------------------------
Input electron density              ... example5.cispur.singlet.iroot0
BaseName (.gbw .S,...)              ... example5

                    ********************************
                    * MULLIKEN POPULATION ANALYSIS *
                    ********************************

-----------------------
MULLIKEN ATOMIC CHARGES
-----------------------
   0 O :    0.177629
   1 C :   -0.438661
   2 H :    0.130515
   3 H :    0.130518
Sum of atomic charges:   -0.0000000

(...)

                      *****************************
                      * MAYER POPULATION ANALYSIS *
                      *****************************

  NA   - Mulliken gross atomic population
  ZA   - Total nuclear charge
  QA   - Mulliken gross atomic charge
  VA   - Mayer's total valence
  BVA  - Mayer's bonded valence
  FA   - Mayer's free valence

  ATOM       NA         ZA         QA         VA         BVA        FA
  0 O      7.8224     8.0000     0.1776     2.5554     1.4462     1.1092
  1 C      6.4387     6.0000    -0.4387     3.8364     3.1848     0.6516
  2 H      0.8695     1.0000     0.1305     0.9720     0.8521     0.1199
  3 H      0.8695     1.0000     0.1305     0.9720     0.8521     0.1199

  Mayer bond orders larger than 0.100000
B(  0-O ,  1-C ) :   1.4477 B(  1-C ,  2-H ) :   0.8685 B(  1-C ,  3-H ) :   0.8685
```

Here the parameters `RSteps`, `LSteps` and `ddnc` are chosen in such a
way that in the scan along modes 6 and 7 the corresponding dimensionless
normal coordinates will be varied in the range 0 $-$ 9.091932 and
-9.723073 $-$ 0, respectively, in accordance with the projection pattern
indicated in the file `geom.ddnc`. Note that normal modes are only
defined up to an arbitrary choice of sign. Consequently, the absolute
sign of the dimensionless displacements is ambiguous and in principle
can vary in different `orca_vib `runs. It is important that the normal
mode scan between different structures exemplified above is performed
using the same sign of normal modes as in the calculation of normal mode
displacements. This condition is fulfilled if the same normal modes are
used in `orca_vib `run and trajectory calculation. Thus, since in
`orca_vib` calculation normal modes are stored in `.hess` file it is
necessary to use the same Hessian file in the trajectory calculation.

<a id="sec:spectroscopyproperties.tddft.nacmes"></a>
## Non-adiabatic coupling matrix elements

The CIS module can compute the non-adiabatic coupling matrix elements
(NACME) between ground and an excited state given by an IROOT,
$\langle \Psi_{GS} | \frac{\partial}{\partial R_x} | \Psi_{IROOT} \rangle$
[send_first-order_2010](../../bibliography.md). These can also include LR-CPCM effects if
!CPCM(solvent) is chosen in the main input, ZORA effects and will make
use of RIJ and COSX, if they are chosen for the SCF. The usage is
simple, e.g.:

```mol
title: structure 19
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
4
structure (0 1)
O   0.000000000  0.000000000  0.611403292
C   0.000000000  0.000000000 -0.613232096
H   0.931880792  0.000000000 -1.200880848
H  -0.931880792  0.000000000 -1.200880848
--- input ---
!PBE0 DEF2-SVP TIGHTSCF
%TDDFT  NROOTS  5
        IROOT   2
        NACME   TRUE
END
* xyz 0 1
O        0.000000000      0.000000000      0.611403292
C        0.000000000      0.000000000     -0.613232096
H        0.931880792      0.000000000     -1.200880848
H       -0.931880792      0.000000000     -1.200880848
*
```

By choosing NACME TRUE under %TDDFT, a regular gradient calculation will
be done, and the NACMEs will be computed together with it. After the
usual gradient output, the NACMEs will be printed as:

```orca
---------------------------------
CARTESIAN NON-ADIABATIC COUPLINGS
       <GS|d/dx|ES>
---------------------------------

1   O   :   -0.161958900   -0.000000135    0.000001029
2   C   :   -0.088213027   -0.000000024    0.000000167
3   H   :    0.226241398    0.000000001   -0.109102154
4   H   :    0.226241406   -0.000000000    0.109102161

Difference to translation invariance:
:    0.2023108777   -0.0000001585    0.0000012017

Norm of the NACs                   ...    0.4002363416
RMS NACs                           ...    0.1155382798
MAX NAC                            ...    0.2262414063
```

The NACMEs are given under the Cartesian basis; this may differ from some
other programs where NACMEs are given under the normal mode basis. To obtain
NACMEs under the normal mode basis, one can perform an internal conversion (IC)
rate calculation (see [esd.ic](#sec:spectroscopyproperties.esd.ic)) and obtain them from the output
file.

<a id="sec:spectroscopyproperties.tddft.nacmes.etf"></a>
### NACMEs with built-in electron-translation factor

As you can see, the calculation above does not have full translation
invariance! That is a feature of NACs calculated from CI wavefunctions,
due to the Born-Oppenheimer approximation. It can be somehow fixed by
including the so-called "electron-translation factors\" (ETFs)
[fatehi_analytic_2011](../../bibliography.md), and those are added with ETF TRUE under %TDDFT.
By now using the input:

```mol
title: structure 20
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
4
structure (0 1)
O   0.000000000  0.000000000  0.611403292
C   0.000000000  0.000000000 -0.613232096
H   0.931880792  0.000000000 -1.200880848
H  -0.931880792  0.000000000 -1.200880848
--- input ---
!PBE0 DEF2-SVP
%TDDFT  NROOTS  5
     IROOT   2
     NACME   TRUE
     ETF     TRUE
END
* xyz 0 1
O        0.000000000      0.000000000      0.611403292
C        0.000000000      0.000000000     -0.613232096
H        0.931880792      0.000000000     -1.200880848
H       -0.931880792      0.000000000     -1.200880848
*
```

one gets the following output:

```orca
---------------------------------
CARTESIAN NON-ADIABATIC COUPLINGS
           <GS|d/dx|ES>
        with built-in ETFs
---------------------------------

1   O   :   -0.071334028   -0.000001941    0.000003727
2   C   :   -0.362514525   -0.000000130   -0.000000776
3   H   :    0.217014763    0.000000003   -0.128968922
4   H   :    0.217014813   -0.000000002    0.128968939

Difference to translation invariance:
:    0.0001810232   -0.0000020693    0.0000029689

Norm of the NACs                   ...    0.5137724505
RMS NACs                           ...    0.1483133313
MAX NAC                            ...    0.3625145251
```

where the residual translation variance is due to the DFT and COSX grids
only.

!!! note
    These are the recommended NACs to be used with any kind of
    dynamics or conical intersection optimization, otherwise moving the
    center of mass of you system would already change the couplings!

<a id="sec:spectroscopyproperties.tddft.nacmes.numnacme"></a>
### Numerical non-adiabatic coupling matrix elements 

The numerical non-adiabatic coupling matrix elements between ground and
excited states from CIS/TD-DFT can be calculated in a numerical fashion,
by setting the NumNACME flag on the main input line:

```orca
! NumNACME
```

ORCA will then calculate both the NACMEs and the numerical gradient for
a given IROOT at the same cost. Please be careful with the SCF options
and GRID sizes since there are displacements involved, for more
information check
[essentialelements.numericalgradients](#sec:essentialelements.numericalgradients). All options regarding
step size and so on can be changed from %NUMGRAD.

These are current implemented in both RHF/RKS and UHF/UKS, but only for
CIS/TDA and RPA/TD-DFT, no multireference methods yet. For the latter
case, the overlap of the $| X -Y \rangle$ vector is used
[Liu_HFNacme_2014](../../bibliography.md).

<a id="sec:spectroscopyproperties.tddft.keywords"></a>
## Keyword List

<a id="tab:spectroscopyproperties.tddft.keywords"></a>
!!! note "`%tddft` or `%cis` block input keywords."
    | Keyword                          | Option / Value            | Description                                                                                            |
    |:---------------------------------|:--------------------------|:-------------------------------------------------------------------------------------------------------|
    | `NRoots`                         | `3`                       | The number of desired roots.                                                                           |
    | `IRoot`                          | `1`                       | The root to be optimized.                                                                              |
    | `IRootMult`                      | `singlet`                 | Multiplicity of the root to be optimized.                                                              |
    |                                  | `triplet`                 |                                                                                                        |  
    | `MaxDim`                         | `5`                       | Davidson expansion space = MaxDim * NRoots.                                                            |
    | `MaxIter`                        | `35`                      | Maximum CI Iterations.                                                                                 |
    | `NGuessMat`                      | `512`                     | The dimension of the guess matrix.                                                                     |
    | `MaxCore`                        | `4096`                    | The maximum memory to be used on this calculation.                                                     |
    | `ETol`                           | `1e-6`                    | Energy convergence tolerance.                                                                          |
    | `RTol`                           | `1e-6`                    | Residual Convergence tolerance.                                                                        |                    
    | `TDA`                            | `false`                   | Switch off for full TDDFT.                                                                             |
    | `LRCPCM`                         | `true`                    | Use LRCPCM.                                                                                            |
    | `CPCMEQ`                         | `false`                   | Which epsilon is used to compute the charges.                                                          |
    | `DoNTO`                          | `true`                    | Generate Natural Transition Orbitals. (For double hybrids, the NTOs do not contain PT2 contributions)  |
    | `NTOStates`                      | `1,2,3`                   | States to consider for NTO analysis. If empty, all will be done.                                       |
    | `NTOThresh`                      | `1e-4`                    | Threshold for printing occupation numbers.                                                             |
    | `SaveUnrNatOrb`                  | `true`                    | Saves natural orbitals (not NTO) from unrelaxed densities for the IROOT chosen (including IROOTLISTs). |
    | `DoSoc`                          | `false`                   | Include spin-orbit coupling.                                                                           |
    | `SocGrad`                        | `false`                   | Set true to compute the SOC gradient for a given IROOT.                                                |
    | `DOTRANS`                        | `false`                   | Transient spectra - starting from IROOT.                                                               |
    |                                  | `ALL`                     | Compute all possible transitions.                                                                      |

