```{index} ICE-CI
```

(sec:modelchemistries.iceci)=
# Approximate Full CI Calculations in Subspace: ICE-CI

(sec:modelchemistries.iceci.introduction)=
## Introduction

In many circumstances, one would like to generate a wavefunction that is
as close as possible to the full-CI result, but Full CI itself is out of
the question for computational reasons. Situations in which that may be
desirable include a) one wants to generate highly accurate energies for
small molecules or b) one wants to sort out a number of low-lying states
or c) one wants to run [CASSCF calculations](sec:modelchemistries.casscf.iceci) with larger active spaces
than the about fourteen orbitals that have been the state of the art for
a long time.

ORCA features a method that has been termed Iterative-Configuration
Expansion Configuration Interaction
(ICE-CI).{cite}`chilkuri_ice1,chilkuri_ice2` It is based on much older
ideas brought forward by Jean-Paul Malrieu and his co-workers in the
framework of the CIPSI (an abbreviation for a method with a rather bulky
name *Configuration Interaction by Perturbation with
multiconfigurational zeroth-order wave functions Selected by Iterative
process*) in the early 1970s.

The goal of the ICE-CI is to provide compact wavefunction(s) (e.g. one
or several states) close to the full-CI limit at a small fraction of the
computational cost. However, ICE-CI itself is not designed to deal with
hundreds of atoms or thousands of basis functions. Thus, unlike, say
DLPNO-CCSD(T) which is a high accuracy method for treating large systems,
ICE-CI is either a highly robust high accuracy method for very small
systems or a "building block" for large systems. By itself it can treat
a few dozen electrons and orbitals -- e.g. *much* more than full CI --
but it cannot do wonders. Its scope is similar to the density matrix
renormalization group (DMRG) or Quantum Monte Carlo Full CI (QMCFCI)
procedures.

ICE-CI should be viewed as a multireference approach. It is
self-adaptive and robust, even in the presence of near or perfect
degeneracies. It yields orthogonal states (when applied to several
states) and spin eigenfunctions. It also yields a density and a spin
density.

(sec:modelchemistries.iceci.algrorithms)=
## The ICE-CI and CIPSI Algorithms 

The general idea of ICE-CI is straightforward: Consider a many-particle
state that has at least a sizable contribution from a given
configuration $\mathrm{\mathbf{n} }^{0}$ (this is a set of occupation
numbers for the active orbitals that are $n_{p}^{0} =0,1\,\,or\,\,2$
($p \quad =$ any active orbital). By nature of the non-relativistic
Hamiltonian only configurations that differ by at most two orbital
occupations from $\mathrm{\mathbf{n} }^{0}$ will interact with it. We
can use perturbation theory to select the subset of singles and doubles
that interact most strongly with $\mathrm{\mathbf{n} }^{0}$ and then
solve the variational problem. We can then analyze the CI vector for
configurations that make a dominant contribution to the ground state.
Say, we single out the configurations with $C_{I}^{2} >T_{\text{gen} }$.
This defines the "generator" set of configurations. The other
configurations are called "variational" configurations. They are treated
to infinite order by the variational principle, but are not important
enough to bring in their single and double excitations. In the next
iteration, we perform singles and doubles relative to these general
configurations and select according to their interaction with the
dominant part of the previous CI vector (truncated to the generators).
This procedure can be repeated until no new important configurations are
found and the total energy converges (See {numref}`icecifig:flowchart`).

(icecifig:flowchart)=
```{figure} ../../images/ICE1-alter.*

Flowchart of the ICE-CI
procedure.
```

The described procedure is very similar to Malrieu's three level CIPSI
procedure. One major technical difference, is that ICE is centered
around *configurations* and *configuration state functions* rather than
*determinants*. A configuration is a set of occupation numbers 0, 1 or 2
that describes how the electrons are distributed among the available
spatial orbitals. A *configuration state function* (CSF) is created by
coupling the unpaired spins in a given configuration to a given total
spin $S$. In general there are several, if not many ways to construct a
linearly independent set of CSFs. CSFs on the other hand can be expanded
in terms of Slater determinants, but there are more Slater determinants
to a given configuration than CSFs. For example for a CAS(14,18)
calculation one has about 10$^{\mathrm{9} }$ determinants, but only
about 3x10$^{\mathrm{8} }$ CSFs and 3x10$^{\mathrm{7} }$ configurations.
In the configuration based ICE (CFG-ICE) all logic happens at the level
of configurations. That is, it is the relationship between two
configurations that determines whether and if yes, by which integrals
the CSFs or determinants of two given configurations interact. Since the
configuration space is so much more compact than the determinant space
substantial computational benefit can be realized by organizing the
calculation around the concept of a configuration. In general, in
CFG-ICE all CSFs that belong to a given configuration are included and
all selection quantities are summed over all CSFs of a given
configuration before it is decided whether this CSFs is included or not.
In the configuration state functions based ICE (CSF-ICE) the logic of
generation and selection occurs at the level of individual CSFs and
therefore we get rid of the requirement to carry around all the CSFs for
a given configuration. This provides substantial gains in the case of
molecules containing a large number of transition metal atoms, where
each atom contains a high-spin center. In such cases only a few CSFs of
a the dominant CFG play a dominant role and other show negligible
contribution to the wavefunction. Finally, in some cases the original
determinant based CIPSI procedure could be preferred. Such cases can be
handled by the determinant based ICE termed DET-ICE. The three variants
of ICE therefore cover all the possible types of multi-reference systems
that one encounters in quantum chemistry.

It should be noted that although the procedure contains a perturbative
element, the final energy is strongly dominated by the variational
energy and hence, for all intents and purposes, the ICE-CI procedure is
variational (but not rigorously size consistent -- size consistency
errors are on the same order of magnitude as the error in absolute
energy).

(sec:modelchemistries.iceci.example)=
## A Simple Example Calculation

Let us look at a simple calculation on the water molecule:

```orcainput
#
# Check the ICECI implementation
#

! SV 

%ice  nel 10           # number of active electrons
      norb 13          # number of active orbitals
      nroots 1         # number of requested roots 
      integrals exact  # exact 4-index transformation 
                       # can be set to RI to avoid bottlenecks

      icetype   CFGs   # The configuration based ICE-CI
                CSFs   # The CSF based ICE-CI         
                DETs   # The determinnat based ICE-CI 
                       # please choose one of these three

      Tgen 1e-04       # value for Tgen. Default is 1e-4
      Tvar 1e-11       # value for Tvar. Default is 1e-11 (1e-7*Tgen)

      etol 1e-06       # energy convergence tolerance 
end

* int 0 1
O 0 0 0 0.0   0.000 0.000
H 1 0 0 1.0   0.000 0.000
H 1 2 0 1.0 104.060 0.000
*
```

Let us look at the output:

```orca
------------------------------------------------------------------------------
                ORCA Iterative Configuration Expansion
             - a configuration driven CIPSI type approach -
------------------------------------------------------------------------------

(some startup information)

Making an initial 'Aufbau' configuration      ... done
Performing S+D excitations from     1   configs ... done (  0.0 sec) NCFG=581
Performing perturbative selection             ... done (  0.0 sec)
   # of configurations before selection       ... 581
   # of configurations after selection        ... 191
   'rest' energy (probably not very physical) ... -3.736391e-10

                    ******************************
                    *  ICECI MACROITERATION   1  *
                    ******************************

   # of active configurations =    191
   Now calling CI solver (269 CSFs)
(...)
CI SOLUTION :
STATE   0 MULT= 1: E=    -76.0463127108 Eh W=  1.0000 DE= 0.000 eV      0.0 cm**-1
      0.95752  : 2222200000000
   Selecting new configurations         ... done (  0.0 sec)
   # of selected configurations          ...    191
   # of generator configurations         ...     69
  Performing single and double excitations relative to generators .. done (0.0 sec)
   # of configurations after S+D         ...  13174
   Selecting from the generated configurations  ... done (  0.1 sec)
   # of configurations after Selection  ...   3827
    Root   0:    -76.046312711       -0.000000063     -76.046312773
(...)
                    ******************************
                    *  ICECI MACROITERATION   3  *
                    ******************************

   # of active configurations =   3866
   Now calling CI solver (9606 CSFs)

CI SOLUTION :
STATE   0 MULT= 1: E=    -76.0539542296 Eh W=  1.0000 DE= 0.000 eV      0.0 cm**-1
      0.95097  : 2222200000000
(...)

             ********* ICECI IS CONVERGED *********
(one final CI)

           ********************************************
           **   ICECI Problem solved in    2.6 sec   **
           ********************************************


FINAL CIPSI ENERGIES
  Final CIPSI Energy Root   0:    -76.053954291 EH
```

From the output the individual steps in the calculation are readily
appreciated. The program keeps cycling between variational solution of
the CI problem, generation of new configurations and perturbative
selection until convergence of the energy is achieved. Normally, this
occurs rapidly and rarely requires more than five iterations. The result
will be close to the Full CI result.

Let us look at a H$_{\mathrm{2} }$O/cc-pVDZ calculation in a bit more
detail (See {numref}`icecifig:example-water`). The calculation starts out with a
single Hartree-Fock configuration. The first iteration of ICE-CI creates
the singles and doubles and altogether 544 configurations are selected.
These singles and doubles bring in about half of the correlation energy.
Already the second iteration, which leads to 73000 selected CSFs
provides a result close to the full CI. At this point up to quadruple
excitations from the Hartree-Fock reference have been included. It is
well known that such quadruple excitations are important for the correct
behavior of the CI procedure (near size consistency will come from the
part of the quadruple excitations that are products of doubles).
However, only a very small fraction of quadruples will be necessary for
achieving the desired accuracy. In the first iteration the procedure is
already converged and provides 99.8% of the correlation energy, using
0.5% of the CSFs in the full CI space and at less than 0.2% the
calculation time required for solving the full CI problem. Hence, it is
clear that near exact results can be obtained while realizing
spectacular savings.

(icecifig:example-water)=
```{figure} ../../images/ICE2.*

An ICE-CI calculation on the water molecule in the cc-pVDZ basis (1s
frozen) 
```

(sec:modelchemistries.iceci.accuracy)=
## Accuracy

The accuracy of the procedure is controlled by two parameters
T$_{\mathrm{gen} }$ and T$_{\mathrm{var} }$ Since we have found that
T$_{\mathrm{var} } \quad =$ 10$^{\mathrm{-7} }$ T$_{\mathrm{gen} }$
always provides converged results, this choice is the default. However,
T$_{\mathrm{var} }$ can be set manually. It can be reduced considerably
in order to speed up the calculations at the expense of some accuracy.
Our default values are T$_{\mathrm{gen} } \quad =$ 10$^{\mathrm{-4} }$
and T$_{\mathrm{var} } \quad =$ 10$^{\mathrm{-11} }$. This provides
results within about 1 mEh of the full CI results (roughly speaking, a
bit better than CCSDT for genuine closed-shell systems).

During the development of ICE-CI systematic test calculations have been
performed using a reference set of 21 full CI energies on small
molecules. The convergence pattern of the mean absolute error is shown
in {numref}`icecifig:convergence`. It is evident from the figure that
the convergence of ICE-CI towards the FCI result is very smooth and that
high accuracy can be obtained. In fact, the default settings lead to an
accuracy of \<1 mEh deviation to the full-CI result. $\mu$Eh accuracy
can be achieved by further tightening. The achieved accuracy relative to
accurate coupled-cluster results shows that the accuracy of even CCSDTQ
can be surpassed by ICE-CI. The achievable accuracy is only limited by
the value of T$_{\mathrm{gen} }$ and much less so by the value of
T$_{\mathrm{var} }$. Hence, it is advisable to use a value for
T$_{\mathrm{var} }$ that is essentially converged and control the
accuracy of the procedure by T$_{\mathrm{gen} }$.

(icecifig:convergence)=
```{figure} ../../images/ICE3_new.*

Convergence of the ICE-CI procedure towards the full CI results for a
test set of 21 full CI energy. Shown is the RMS error relative to the
Full CI results. The corresponding errors for various coupled-cluster
variants is shown by broken horizontal
lines.
```

(sec:modelchemistries.iceci.scaling)=
## Scaling behavior

ICE-CI will break the factorial scaling of the full CI problem and scale
polynomially. The actual order of the polynomial scaling is system
dependent and accuracy dependent. In order to provide some impression,
consider some calculations on linear polyene chains.

(icecifig:polyene-chain)=
```{figure} ../../images/ICE4.*

Polyene chains used for scaling
calculations.
```

The results are displayed in the {numref}`icecifig:polyene-scaling`. It is evident from {numref}`icecifig:polyene-scaling` that ICE-CI breaks the factorial
scaling of the full CI problem. In fact, for a thresholds of
T$_{\mathrm{gen} }=$10$^{\mathrm{-4} }$,
10$^{\mathrm{-3} }$ and 10$^{\mathrm{-2} }$ the observed scalings are
approximately $O$(N$^{\mathrm{8} })$, $O$(N$^{\mathrm{7} })$ and
$O$(N$^{\mathrm{6} })$ respectively. These numbers will obviously be
very system dependent but should serve as a rough guide. The
calculations become quickly much more expensive if T$_{\mathrm{gen} }$
is tightened. A rule of thumb is that each order of magnitude tightening
of T$_{\mathrm{gen} }$ increases the computation time by a factor of 10.
The above calculations have been performed on a simple desktop computer
and it was already possible to solve a CAS(30,30) problem in less than
one day of elapsed time using the default thresholds. Large active
spaces will require either loosening of the thresholds or large, more
powerful machines.

(icecifig:polyene-scaling)=
```{figure} ../../images/ICE5.*

Scaling behavior of ICE-CI for linear polyene chains (Full
$\pi$-electron active space) as a functions of system size for different
generator thresholds.
```

(sec:modelchemistries.iceci.accuracywavefunction)=
## Accuracy of the Wavefunction

The accuracy of the many particle wavefunction is not straightforward to
check. A reasonable measure, however, is how well it converges towards
the exact result for one-electron expectation values. Since every
expectation value can be written in terms of natural orbitals of the
one-particle density as:

$$ \left\langle { \hat{{O} }} \right\rangle=\left\langle { \Psi \left|{\sum\nolimits_o { \hat{{o} }(\mathrm{\mathbf{x} }_{i} ) } } \right|\Psi } \right\rangle = \sum\limits_{pq} { D_{pq} \left\langle { \psi_{p} \vert \hat{{o} }\vert \psi_{q} } \right\rangle} =\sum\limits_p { n_{p} \left\langle { \tilde{{\psi } }_{p} \vert \hat{{o} }\vert \tilde{{\psi 
} }_{p} } \right\rangle} $$

where $\hat{o}(\mathrm{\mathbf{x}}_{i})$ is an arbitrary one-particle operator, $D_{pq}$ is the density matrix of
the ICE-CI wavefunction, $\tilde{{\psi}}_{p}$ are the natural orbitals of the ICE-CI wavefunction and $n_{p}$ are their occupations numbers. It is reasonable to take the deviation of the natural orbital occupation
numbers as a measure for wavefunction convergence.

For example, we treat the H$_{\mathrm{2} }$O/cc-pVDZ problem again. From
the results in {numref}`icecifig:occ-convergence` it becomes evident that the ICE-CI
wavefunction is fairly accurate. At the default threshold the occupation
numbers agree to within 10$^{\mathrm{-3} }$ with the full CI reference
numbers, which means that expectation values will be of similar
accuracy. Interestingly, the largest errors occur in the region of the
HOMO-LUMO gap, where apparently all approximate wavefunction approaches
tend to depopulate the high lying orbitals too much and put too much
electron density in the low lying empty orbitals. From comparison, it is
seen, that the CCSD natural occupation numbers for this problem are
significantly less accurate. Hence, this is evidence that the ICE-CI
wavefunction is properly converging to the right result.

(icecifig:occ-convergence)=
```{figure} ../../images/ICE6.*

Convergence of the ICE-CI natural orbital occupation numbers. The
upper panel is showing the Full CI occupation numbers, the lower panel
the deviation of the ICE-CI values from these exact values. For
comparison, the CCSD natural orbital occupation numbers are also
provided. 
```

(sec:modelchemistries.iceci.pes)=
## Potential Energy Surfaces

You can use ICE-CI to scan entire potential energy surfaces. In general,
the non-parallelity error along a potential energy surface is very
small. Thus, ICE-CI yields consistent quality throughout the surface.

For example, let us look at the potential energy surface of the
N$_{\mathrm{2} }$ molecule ({numref}`icecifig:n2-surface`) -- a common test case for quantum
chemical methods. There are not too many methods that would dissociate
the triple bond of N$_{\mathrm{2} }$ correctly -- ICE-CI is one of them.
The potential energy surface is entirely smooth and also correctly
behaves in the dissociation limit. Near the minimum it is very close to
high-level coupled-cluster methods that, however, all fail badly as the
bond is stretched.

(icecifig:n2-surface)=
```{figure} ../../images/ICE7.*

Potential energy surface of the N$_2$ molecule in the SV basis. For
comparison higher level coupled-cluster results are also
shown.
```

It is interesting to observe the variations of the ICE-CI wavefunction
along the dissociation potential energy surface. As an example, we look
at the dissociation curve of H$_{\mathrm{2} }$O where both O-H bonds are
simultaneously stretched ({numref}`icecifig:h2o-error`). It is seen that the ICE-CI method is
extremely parallel to the full CI curve at all distances. Hence, the
description of the bond remains consistent, even when Hartree-Fock
becomes a bad approximation. The agreement is particularly good if MP2
natural orbitals are used in the ICE-CI procedure. With the default
value of T$_{\mathrm{gen\thinspace } }=$ 10$^{\mathrm{-4} }$ and MP2
natural orbitals the error is consistently below 0.2 mEh. For tighter
thresholds, the error is below 0.05 mEh. By contrast, the CCSD(T) method
shows relatively large deviations from the full CI results and also
behaves very non-parallel as a function of O-H distance.

(icecifig:h2o-error)=
```{figure} ../../images/ICE8.*

Non-parallelity error of ICE-CI for the H$_2$O molecule in the SV
basis. Shown is the deviation from the full CI value as a function of
O-H distance (both bonds stretched). For comparison, the CCSD(T) curve
is also shown
```

It is instructive to analyze the ICE-CI wavefunction along the
dissociation pathway ({numref}`icecifig:h2o-bond`). It becomes apparent that the
wavefunctions stays compact along the entire surface, even in the
dissociation limit, where the weight of the Hartree-Fock wavefunction
drops to less than 25%. Even in this drastic limit, the ICE-CI
wavefunction consists of only about 60000 CSFs, which is very similar to
the size of the wavefunction at equilibrium geometry. As the
wavefunction becomes more multiconfigurational, the number of generator
configurations goes slightly up from the equilibrium value of 77 to a
maximum of 118 and finally 112 at dissociation. It is also interesting
to note that along the entire dissociation pathway no configuration with
more than 8 open shells is generated, which means that no more than
quadruple excitations are contained in the ICE-CI wavefunction. The
number of iterations required in the ICE-CI procedure also stays
constant along the surface at 4 iterations, which impressively shows
that a dominant configuration is not necessary for a successful ICE-CI
calculation.

(icecifig:h2o-bond)=
```{figure} ../../images/ICE9.*

Analysis of the ICE-CI wavefunction along the O-H dissociation
pathway.
```

## Excited States

ICE-CI can be used to obtain some insight into excited states starting
from no knowledge at all. Of course, the best was to start an excited
state calculation is to have some idea which configurations are
important for the low-lying states of the system. If this is not the
case, an automated procedure is used. The program will first generate an
"Aufbau" configuration using the orbitals that are provided on input.
Starting from this Aufbau configuration, single excitations at the
configuration level are performed an the Hamiltonian is diagonalized for
the required number of roots. These roots are then analyzed for the
leading configurations and the regular ICE-CI procedure is started from
those configurations. For example, look at a calculation on the CN
radical. In this case, we know the relevant orbitals and leading
configurations for the lowest four roots (a doublet $\Sigma$ ground
state, a doublet $\Pi$ excited state and a doublet $\Sigma$ excited
state) and hence can provide them in the input file as shown below.

```orcainput
#
! cc-pVDZ VeryTightSCF 

%maxcore 4096

%casscf nel 7
        norb 4
        nroots 4
        mult 2
        end

%ice   nel 9
        norb 26
        nroots 4
        cimode 3
        tvar 1e-11
        tgen 1e-4
        refs { 2 2 2 2 1 }
             { 2 2 2 1 2 }
             { 2 2 1 2 2 }
             { 2 1 2 2 2 }
             end
        end

* xyz 0 2
C 0 0 0
N 0 0 1.07
*
```

The result is shown below. The excitation energies are reasonable but
not highly accurate due to the limitations of the basis set
(experimentally the doublet $\Pi$ state is at 1.32 eV and the doublet
$\Sigma$ state at 3.22 eV). There is a very slight symmetry breaking In
the doublet $\Pi$ state that arises from the selection procedure. It
should be noted that the state averaged CASSCF excitation energies are
0.25 eV and 3.18 eV.

```orca
STATE   0 MULT= 2: E=    -92.4542949092 Eh W=  0.2500 DE= 0.000 eV      0.0 cm**-1
      0.67408  : 22221000000000000000000000
STATE   1 MULT= 2: E=    -92.3777338429 Eh W=  0.2500 DE= 2.083 eV  16803.2 cm**-1
      0.65997  : 22212000000000000000000000
      0.12092  : 22122000000000000000000000
      0.11545  : 22221000000000000000000000
STATE   2 MULT= 2: E=    -92.3776916150 Eh W=  0.2500 DE= 2.084 eV  16812.5 cm**-1
      0.69860  : 21222000000000000000000000
      0.16565  : 22122000000000000000000000
STATE   3 MULT= 2: E=    -92.3412510872 Eh W=  0.2500 DE= 3.076 eV  24810.3 cm**-1
      0.51251  : 22122000000000000000000000
      0.16825  : 22212000000000000000000000
      0.11151  : 21222000000000000000000000
```

Below, it is described how to do ICE-CI calculations on excited states
if the dominant configurations are not known.

(sec:modelchemistries.iceci.tips)=
## Tips and Tricks

(sec:modelchemistries.iceci.tips.csf)=
### Using the CSF-Based Algorithm

The CSF-ICE-CI offers substantial gains in the case of molecules containing a large number of transition metal atoms, where each atom contains a high-spin center.
In such cases only a few CSFs of a the dominant CFG play a dominant role and other show negligible contribution to the wavefunction.
However, CSF-ICE-CI comes with the caveat that a memory buffer is needed to store all significant singles and doubles excitation per CSF.

```orca
%ice 
 # Scratch space dimension (number of singles/double excitations per CSF) 
 # If scratch is too small, the program may crash.
 CIBufferLength 10240 # ~82kB (factor 8/10³ to get the memory in kB): 
end
```

The default buffer size `CIBufferLength` is usually sufficient for most frequent calculations.
If `CIBufferLength` is too small for a given calculation, the ICE-CI program will crash.
Restarting with a significantly larger buffer size, e.g. `%ice CIBufferLength 1000000 end`, will often fix this issue.
Keep that workaround in mind when running ICE-CI calculations for large multi-center transition metal clusters and complexes.


(sec:modelchemistries.iceci.tips.orbitals)=
### Choice of Orbitals

ICE-CI can be used very fruitfully together with, say, MP2 natural
orbitals. This usually results in results that are closer to full CI
results and at the same time lead to more compact wavefunctions (it may be
called nICE). The use of MP2 natural orbitals is requested by choosing
`UseMP2nat true` inside the %ice block. Alternatively, improved virtual
orbitals can be used (requested by `UseIVOs true`). A comparison is
shown in Scheme {ref}`icecifig:startorbitals`. It is evident that the calculations
based on the MP2 natural orbitals show an error relative to full CI that
is almost a factor of two smaller than the corresponding result with
canonical orbitals while at the same time the wavefunction is more
compact by more than 30%. Hence, the use of MP2 natural orbitals appears
to be a very good idea in conjunction with the ICE-CI procedure. This
also holds when MP2 itself is a bad approximation (for example in the
dissociation limit of the H2O molecule as shown above). On the other
hand, the IVOs behave very similar to canonical orbitals and hence, seem
to offer fewer advantages.

(icecifig:startorbitals)=
```{figure} ../../images/ICE10.*

Comparison of MP2 natural orbitals and improved virtual orbitals for
the ICE-CI procedure (H2O molecule, cc-pVDZ basis, equilibrium geometry)

```

If ICE-CI is used in conjunction with MP2 natural orbitals, there also
is the possibility of letting the program automatically choose the
active space (this is called auto-ICE). The general idea is simple -- we
base the active space on the MP2 natural orbitals and their occupation
numbers. All orbitals between occupation number say 1.98 down to 0.02
will be included in the active space. A relevant input is shown below.

```orcainput
! cc-pVDZ aug-cc-pV6Z/C Auto-ICE
%ice nmin 1.99 nmax 0.01 end

%paras R= 1.0 end

* int 0 1
O 0 0 0 0 0 0
H 1 0 0 { R} 0 0
H 1 2 0 { R} 104 0
*
```

If we scan along the H$_{\mathrm{2} }$O dissociation surface one can see
that despite changing active spaces, the dissociation curves are smooth
and remain fairly parallel to the full CI dissociation curve. Depending
on the tightness of the thresholds the active space may change from a
small 6 electrons in 5 orbitals to a larger 8 electrons in 7 or 8
orbitals upon dissociation. This is the expected behavior as the
$\sigma$-antibonding orbital becomes more stable along the bond
stretching coordinate. Hence, these results are encouraging in as far as
in many situations the program will be able to select a sensible active
space without extended input from the user.

(icecifig:auto-space)=
```{figure} ../../images/ICE11.*

Automatic active space selection along the H$_2$O dissociation
surface. The reference curve (blue triangles) is the ICE-CI method for
the full orbital space with the default parameters.

```

Another place, where automatic selection comes in conveniently is in the
calculation of excited states. If there are no user supplied
configurations, what happens is that the program will first choose an
Aufbau "reference" configuration and then perform all single excitations
relative to this configuration. The program will then diagonalize the
Hamiltonian over the this set of configurations to create
0$^{\mathrm{th} }$ order approximations for the chosen number of roots
of interest and then initiate the ICE-CI procedure starting from the
leading configurations of these states. Here is an example for the
benzene molecule:

```orcainput
! RHF def2-SVPD def2-SVP/C Auto-ICE
%cclib "/user/me/orca/cclib/orcacc"
%ice nroots 5
     nmin 1.98
     nmax 0.02
     integrals ri
     end

* int 0 1
C 0 0 0 0.000000 0.000 0.000
C 1 0 0 1.389437 0.000 0.000
C 2 1 0 1.389437 120.000 0.000
C 3 2 1 1.389437 120.000 0.000
C 4 3 2 1.389437 120.000 0.000
C 5 4 3 1.389437 120.000 0.000
H 1 2 3 1.082921 120.000 180.000
H 2 1 3 1.082921 120.000 180.000
H 3 2 1 1.082921 120.000 180.000
H 4 3 2 1.082921 120.000 180.000
H 5 4 3 1.082921 120.000 180.000
H 6 5 4 1.082921 120.000 180.000
*
```

(The %cclib statement is explained below and is not mandatory here). The
Auto-ICE procedure comes up with as many as 24 electrons in 19 orbitals,
which already is a fairly heavy calculation. The procedure converges in
five iterations and provides indeed the correct states: the ground
state, the $^{\mathrm{1} }$B$_{\mathrm{2u} }$ state at 6.4 eV, the
$^{\mathrm{1} }$B$_{\mathrm{1u} }$ state at 8.9 eV and a degenerate
$^{\mathrm{1} }$E$_{\mathrm{1u} }$ state at 10.0 eV. These excitation
energies are still in error by about 2 eV relative to experiment, which
is mainly due to missing dynamic correlation. However, the correct
states and their sequence has been found.

(sec:modelchemistries.iceci.tips.states)=
### State Detection

The ICE-CI can be used to find the ground state if the actual ground
state is not known. To this end, one simply has to turn off the
selection steps. This makes the calculations more expensive, but they
will converge to the lowest state. In the example below (again, the
H$_{\mathrm{2} }$O molecule) we start from a random quintuply excited
configuration -- the ICE-CI still finds the ground state after four
iterations:

```orca
%ice
  nel     8
  norb    23
  nroots   1
  tvar 1e-11
  tgen 1e-04
  etol 1e-06

  # selection
  SelStart false 
  SelIter  false 
  
  # algorithm details
  useivos   false
  integrals exact
  cimaxdim     5 #Davidson expansion space = MaxDim * NRoots
  cimode       3

  # spatial sym (only supported for ICEType = CFGs)
  irrep 0
  # startup (optional)
  refs { 2 1 0 1 0 2 1 0 1 } 
       end
end
```

However, if one wants to converge to an excited state, one should turn
on the selection. In the example below (once more the water molecule)
one can converge to the second excited singlet state by judicious
choice of the start configuration:

```orca
%ice 
  nel 8
  norb 23
  nroots 1
  tvar 1e-11
  tgen 1e-04
  etol 1e-06
  
  # selection
  SelStart true 
  SelIter true 
  
  # algorithm details
  useivos false
  integrals exact
  cimaxdim 5 
  cimode 3
  
  # spatial sym (only supported for ICEType = CFGs)
  irrep 0
  { #} startup (optional)
  refs 
    { 2 2 1 2 0 1 } 
  end
end
```

(sec:modelchemistries.iceci.cistep)=
## Large-scale approximate CASSCF: ICE-SCF 

ICE-CI can be used in place of the default `CIStep` in a [CASSCF](sec:modelchemistries.casscf)
framework. In this way, much [larger CASSCF calculations](sec:modelchemistries.casscf.iceci) than previously
possible can be envisioned. In using the ICE-CI in this way, the active
orbitals should be chosen as natural orbitals in order to ensure a
proper canonicalization. In general, ICE-CI results will not be
invariant with respect to the choice of orbitals. However, in practice
we have not found this to be problematic. We refer to this as ICE-SCF.

The use is simple: In the `%casscf` block choose `CIStep ICE`. Optionally, starting
configurations (CFGs) or configuration state functions (CSFs) can be defined in the `refs` sub-block.
All other parameters are accessible through the 'CI' sub-block in `%casscf`. The program also supports
[FIC-NEVPT2 calculations with the ICE](sec:modelchemistries.nevpt2.ice) as reference wavefunction.{cite}`guo_icenevpt2_2025`

```orca
%casscf 
...
  # mandatory
  CIStep ICE
  
  # optional starting references for ICE 
  # using the refs sub-block
  # refs {2 2 ...} end
  
  # optional refined settings
  # with keywords as in the %ice block
  ci
     ICEType CFGs   # select ICE expansion type: 
                    # 'CFGs' (default), 'DETS' or 'CSFs'
     TGen 1e-4      # controls accuracy (default = 1e-4)
     TVar 1e-11     # default = 1e-7 * TGen
     MaxIter 100    # number of allowed cycles (default = 64)
     
     # Scratch space dimension (number of singles/double excitations per CSF) 
     # If scratch is too small, the program may crash.
     CIBufferLength 10240 # ~82kB (factor 8/10³ to get the memory in kB): 
  end
end
```

The entire remaining input is the one for standard CASSCF calculations.
In this way one can do CASSCF calculations with very large active space
in reasonable turnaround times. We have not observed convergence
problems that are worse than in the standard CASSCF procedure. The
results in {numref}`icecifig:casdevs-energies` show that the deviations from
regular CASSCF energies are very small. The largest deviation observed
for C$_{\mathrm{2} }$H$_{\mathrm{4} }$ is on the order of 0.2 mEh, which
appears acceptable. Note that the [CASSCF tutorial](https://orcaforum.kofo.mpg.de/app.php/dlext/?cat=4&sid=9d58efcf2208abe23b1af87a601b42f6) also covers larger
examples and excitations energies computed with the ICE-CI as CI solver.

(icecifig:casdevs-energies)=
```{figure} ../../images/ICE12.*

Deviations of ICE-SCF from CASSCF energies for a selection of
molecules (standard truncation parameters $T_{\text{gen} } = 10^{-4}$
and $T_{\text{var} } = 10^{-11}$)

```

Since CASSCF is fully variational, it is possible to optimize geometries
with that procedure. It is our experience so far, that the ICE-SCF
geometries are virtually indistinguishable from CASSCF geometries (an
example is shown in {numref}`icecifig:casdevs-geometries`).

(icecifig:casdevs-geometries)=
```{figure} ../../images/ICE13.*

CASSCF and ICE-SCF optimized geometries for methylene and ozone
(cc-pVDZ basis set, default parameters).

```

(sec:modelchemistries.iceci.keywords)=
## Keywords

For completeness, the parameters that can be specified in the input
block are summarized below:

```orca
%ice 
        nel           8 # number of active electrons
        norb         23 # number of active orbitals
        nroots        1 # number of roots
        mult          1 # requested multiplicity
        irrep         0 # requested irrep (only supported for ICEType=CFGs)only s
        tgen      1e-04 # generator threshold
        tvar      -1e-7 # negative -> 1e-7*tgen
        etol      1e-06 # convergence tolerance 

        icetype     CFGs # The configuration based ICE-CI                     
                    CSFs # The CSF based ICE-CI                               
                    DETs # The determinant based ICE-CI 

        # algorithm details
   
        
        useMP2nat  false  # use MP2 natural orbitals
        useIVOs    false  # use improved virtual orbitals
        useQROs    false  # For UHF: use quasi-restricted MOs?
        integrals  exact  # exact or ri transformation
        CIMaxIter     64  # max. number of CI iterations in the Davidson procedure
        CINGuessMat   512 # size of the CI guess matrix in the Davidson procedure
        CIMaxDim      10  # max. size of expansion space in the Davidson procedure
        CIMode         3  # default=accelerated CI, other settings not recommended
        CSFCIwithRI    1  # 1=with RI, 0=without RI, use withour RI
	                  # when norb >> nel (e.g. (30e, 120o))
        CIPSIOrbSweepWindow 1 # Use in case of large size of the S+D list and
	                      # small available memory. MOs can be divided into
			      # chunks (e.g. MOblock = MO/CIPSIOrbSweepWindow)                                                     
                              
        # scratch space dimension (number of singles/double excitations per CSF) 
        # If scratch is too small, the program may crash.
        CIBufferLength 10240 # ~82kB (factor 8/10³ to get the memory in kB):

        # startup configurations(optional)
        refs { 2 2 2 2 0 }
             { 2 2 2 0 2 }
             end
        end
        
        # natural orbitals with the ICE ansatz
        NatOrbs 1          # generates the .cipsi.nat GWB file containing
	                   # the natural orbitals
```

(sec:modelchemistries.iceci.cclib)=
## A Technical Note: `orcacclib` 

We should finally mention a technical aspect. The CI procedure in ICE-CI
is based around the so-called one particle coupling coefficients

$$A_{pq}^{IJ} = \left< I | E_p^q | J \right>$$

where $A_{pq}^{IJ}$ is a coupling coefficient, $I$ and $J$ are
configuration state functions (CSFs) and $E_p^q$ is the spin-free
excitation operator that promotes an electron from orbital $p$ to
orbital $q$. The values of these coupling coefficients only depend on
the logical relationship between the CSFs $I$ and $J$ but not on the
absolute values of $I$, $J$, $p$, $q$. In fact, they only depend on the
number of unpaired electrons in $I$ and the total spin $S$ that both
CSFs refer to. Hence, prototype coefficients can be pre-tabulated. This
is normally done in a CI run at the beginning of the run. However, in
ICE-CI it may have to be repeated several dozen times and for large
numbers of open shells (say 14), the process is time and memory
consuming.

In order to ease the computational burden, we have provided a small
utility program that tabulates the coupling coefficients for a given
total spin $S$ (rather the multiplicity $M = 2S + 1$) and maximum number
of open shells. This program is called `orcacclib`. It is called like:

```orca
orca_cclib Mult MaxNOpen
```

or - if you want to speed up the generation of the cclib:

```orca
mpirun -np 4 /full_path/orca_cclib_mpi Mult MaxNOpen cclib  # using 4 processes
```

It will produce a series of files orcacc.el.mult.nopen (electron density
coupling coefficients) and orcacc.sp.mult.nopen (spin-density coupling
coefficients) in the current directory. These files are binary files.
They can be copied to an arbitrary directory. You instruct the program
to read these coefficients (rather than to recalculate them all the
time) by setting the path to this directory:

```orca
# My Job
! def2-SVP Auto-ICE
%cclib "/user/me/orca/cclib/orcacc"
```

The remaining part of the filename will be automatically added by the
program. This option can save humongous amounts of time. The coupling
coefficient library needs to be made for the desired multiplicities only
once. The practical limit will be 14-16 open shells. If you are running
the calculation on a cluster using some submit script, you have to
ensure that the provided `cclib` path is accessible from the compute
node.
