

<a id="sec:essentialelements.scfconvergence"></a>
# Self-Consistent-Field (SCF)

SCF convergence is a pressing problem in any electronic structure
package because the total execution times increases linearly with the
number of iterations. Thus, it remains true that the best way to enhance
the performance of an SCF program is to make it converge better. In some
cases, especially for open-shell transition metal complexes, convergence
may be very difficult. ORCA makes a dedicated effort to achieve
reasonable SCF convergence for these cases without compromising
efficiency.

Another issue is whether the solution found by ORCA is stable, i.e. a
minimum on the surface of orbital rotations. Especially for open-shell
singlets it can be hard to achieve a broken-symmetry solution. The SCF
stability analysis (section
[sec:essentialelements.stabilityanalysis](#sec:essentialelements.stabilityanalysis)) may be able to help in
such situations. Please also note that if `! TRAH` is used the solution
must be a true local minimum though not necessarily a global.

!!! tip
    The expectation value $\langle S^2\rangle$ is an estimation of the spin
    contamination in the system. It is highly recommended for open-shell
    systems, especially with transition metal complexes, to check the UCO
    (unrestricted corresponding orbitals, see [sec:modelchemistries.hftype.unoucoqro](#sec:modelchemistries.hftype.unoucoqro))
    overlaps and visualise the corresponding orbitals.
    Additionally, spin-population on atoms that contribute to the singly occupied
    orbitals is also an identifier of the electronic structure.

<a id="sec:essentialelements.scfconvergence.tol"></a>
## Convergence Tolerances

Before discussing how to converge a SCF calculation it should be defined
what is meant by "converged". ORCA has a variety of options to control
the target precision of the energy and the wavefunction that can be
selected in the `% scf` block, or with a simple input line keyword that
merges the criterion label with "SCF", e.g. `! StrongSCF` or
`! VeryTightSCF`:

```orca
%scf
  Convergence             # The default convergence is between medium and strong
               Sloppy     # very weak convergence
               Loose      # still weak convergence
               Medium     # intermediate accuracy
               Strong     # stronger
               Tight      # still stronger
               VeryTight  # even stronger
               Extreme    # close to numerical zero of the computer
                          # in double precision arithmetic
 end
```

Like other keys, `Convergence` is a compound key that assigns default
values to a variety of other variables given in the box below.
In [compoundConvergenceThresholds](#compoundConvergenceThresholds) we present the chosen values
for each compound key. If the corresponding simple inputs are given 
(`!StrongSCF`, `!VeryTightSCF`, \...etc), then in addition the values in
[compoundAdditionalConvergenceThresholds](#compoundAdditionalConvergenceThresholds) are also set,
which also influence the behavior of post-SCF modules.
The default convergence criteria are reasonable and should be sufficient for
most purposes. For a cursory look at populations weaker convergence may
be sufficient, whereas other cases may require stronger than default
convergence. Note that `Convergence` does not only affect the target
convergence tolerances but also the integral accuracy as discussed in
the section about direct SCF and alike. 
**This is very important: if the
error in the integrals is larger than the convergence criterion, a
direct SCF calculation cannot possibly converge.**

The convergence criteria are always printed in the output. Given below
is a list of the convergence criteria for `! TightSCF`, which is often
used for calculations on transition metal complexes.

```orca
%scf
  TolE        1e-8  # energy change between two cycles
  TolRMSP     5e-9  # RMS density change
  TolMaxP     1e-7  # maximum density change
  TolErr      5e-7  # DIIS error convergence
  TolG        1e-5  # orbital gradient convergence
  TolX        1e-5  # orbital rotation angle convergence
  Thresh    2.5e-11 # integral prescreening threshold
  TCut      2.5e-12 # primitive integral prescreening cutoff
  ConvCheckMode  2  # = 0: check all convergence criteria
                    # = 1: stop if one of criterion is met, this is sloppy!
                    # = 2: check change in total energy and in one-electron energy
                    #      Converged if delta(Etot)<TolE and delta(E1)<1e3*TolE
  ConvForced        # = 0: convergence not mandatory for next calculation step
                    # = 1: break, if you did not meet the convergence criteria
end
%method
  Z_Tol       1e-4  # CP-SCF solver tolerance
  BFCut       1e-11 # basis function cutoff for numerical integration
end

# Additional tolerances modified by the simple input
%casscf
  GTol       2.5e-4
  ETol       2.5e-8
end
%mdci
  STol         1e-5
end
%autoci
  STol         1e-5
end
%mrci
  ETol       2.5e-7
  RTol       2.5e-7
end
%cis
  ETol       2.5e-7
  RTol       2.5e-7
end
```

<a id="compoundConvergenceThresholds"></a>
!!! note "Threshold choices for convergence keywords."
    :header-rows: 1

| Item | Value |
| --- | --- |
| **Variable** | — |

      - Value

| Item | Value |
| --- | --- |
| **{cspan}`1` *Sloppy* (`!SloppySCF`/`Convergence Sloppy`)** | — |

| Item | Value |
| --- | --- |
| **`TolE`** | — |

      - 3e-5

| Item | Value |
| --- | --- |
| **`TolMAXP`** | — |

      - 1e-4

| Item | Value |
| --- | --- |
| **`TolRMSP`** | — |

      - 1e-5

| Item | Value |
| --- | --- |
| **`TolErr`** | — |

      - 1e-4

| Item | Value |
| --- | --- |
| **`Thresh`** | — |

      - 1e-9

| Item | Value |
| --- | --- |
| **`TCut`** | — |

      - 1e-10

| Item | Value |
| --- | --- |
| **`BFCut`** | — |

      - 1e-10

| Item | Value |
| --- | --- |
| **`TolG`** | — |

      - 3e-4

| Item | Value |
| --- | --- |
| **`TolX`** | — |

      - 3e-4

| Item | Value |
| --- | --- |
| **`Z_Tol`** | — |

      - 5e-3

| Item | Value |
| --- | --- |
| **{cspan}`1` *Loose* (`!LooseSCF`/`Convergence Loose`)** | — |

| Item | Value |
| --- | --- |
| **`TolE`** | — |

      - 1e-5

| Item | Value |
| --- | --- |
| **`TolMAXP`** | — |

      - 1e-3

| Item | Value |
| --- | --- |
| **`TolRMSP`** | — |

      - 1e-4

| Item | Value |
| --- | --- |
| **`TolErr`** | — |

      - 5e-4

| Item | Value |
| --- | --- |
| **`Thresh`** | — |

      - 1e-9

| Item | Value |
| --- | --- |
| **`TCut`** | — |

      - 1e-10

| Item | Value |
| --- | --- |
| **`BFCut`** | — |

      - 1e-10

| Item | Value |
| --- | --- |
| **`TolG`** | — |

      - 1e-4

| Item | Value |
| --- | --- |
| **`TolX`** | — |

      - 1e-4

| Item | Value |
| --- | --- |
| **`Z_Tol`** | — |

      - 3e-3

| Item | Value |
| --- | --- |
| **{cspan}`1` *Medium* (`!MediumSCF`/`Convergence Medium`)** | — |

| Item | Value |
| --- | --- |
| **`ConvCheckMode`** | — |

      - 2

| Item | Value |
| --- | --- |
| **`TolE`** | — |

      - 1e-6

| Item | Value |
| --- | --- |
| **`TolMAXP`** | — |

      - 1e-5

| Item | Value |
| --- | --- |
| **`TolRMSP`** | — |

      - 1e-6

| Item | Value |
| --- | --- |
| **`TolErr`** | — |

      - 1e-5

| Item | Value |
| --- | --- |
| **`Thresh`** | — |

      - 1e-10

| Item | Value |
| --- | --- |
| **`TCut`** | — |

      - 1e-11

| Item | Value |
| --- | --- |
| **`BFCut`** | — |

      - 1e-10

| Item | Value |
| --- | --- |
| **`TolG`** | — |

      - 5e-5

| Item | Value |
| --- | --- |
| **`TolX`** | — |

      - 5e-5

| Item | Value |
| --- | --- |
| **`Z_Tol`** | — |

      - 1e-3

| Item | Value |
| --- | --- |
| **{cspan}`1` *Strong* (`!StrongSCF`/`Convergence Strong`)** | — |

| Item | Value |
| --- | --- |
| **`ConvCheckMode`** | — |

      - 2

| Item | Value |
| --- | --- |
| **`TolE`** | — |

      - 3e-7

| Item | Value |
| --- | --- |
| **`TolMAXP`** | — |

      - 3e-6

| Item | Value |
| --- | --- |
| **`TolRMSP`** | — |

      - 1e-7

| Item | Value |
| --- | --- |
| **`TolErr`** | — |

      - 3e-6

| Item | Value |
| --- | --- |
| **`Thresh`** | — |

      - 1e-10

| Item | Value |
| --- | --- |
| **`TCut`** | — |

      - 3e-11

| Item | Value |
| --- | --- |
| **`BFCut`** | — |

      - 3e-11

| Item | Value |
| --- | --- |
| **`TolG`** | — |

      - 2e-5

| Item | Value |
| --- | --- |
| **`TolX`** | — |

      - 2e-5

| Item | Value |
| --- | --- |
| **`Z_Tol`** | — |

      - 7e-4

| Item | Value |
| --- | --- |
| **{cspan}`1` *Tight* (`!TightSCF`/`Convergence Tight`)** | — |

| Item | Value |
| --- | --- |
| **`ConvCheckMode`** | — |

      - 2

| Item | Value |
| --- | --- |
| **`TolE`** | — |

      - 1e-8

| Item | Value |
| --- | --- |
| **`TolMAXP`** | — |

      - 1e-7

| Item | Value |
| --- | --- |
| **`TolRMSP`** | — |

      - 5e-9

| Item | Value |
| --- | --- |
| **`TolErr`** | — |

      - 5e-7

| Item | Value |
| --- | --- |
| **`Thresh`** | — |

      - 2.5e-11

| Item | Value |
| --- | --- |
| **`TCut`** | — |

      - 2.5e-12

| Item | Value |
| --- | --- |
| **`BFCut`** | — |

      - 1e-11

| Item | Value |
| --- | --- |
| **`TolG`** | — |

      - 1e-5

| Item | Value |
| --- | --- |
| **`TolX`** | — |

      - 1e-5

| Item | Value |
| --- | --- |
| **`Z_Tol`** | — |

      - 1e-4

| Item | Value |
| --- | --- |
| **{cspan}`1` *VeryTight* (`!VeryTightSCF`/`Convergence VeryTight`)** | — |

| Item | Value |
| --- | --- |
| **`ConvCheckMode`** | — |

      - 2

| Item | Value |
| --- | --- |
| **`TolE`** | — |

      - 1e-9

| Item | Value |
| --- | --- |
| **`TolMAXP`** | — |

      - 1e-8

| Item | Value |
| --- | --- |
| **`TolRMSP`** | — |

      - 1e-9

| Item | Value |
| --- | --- |
| **`TolErr`** | — |

      - 1e-8

| Item | Value |
| --- | --- |
| **`Thresh`** | — |

      - 1e-12

| Item | Value |
| --- | --- |
| **`TCut`** | — |

      - 1e-14

| Item | Value |
| --- | --- |
| **`BFCut`** | — |

      - 1e-12

| Item | Value |
| --- | --- |
| **`TolG`** | — |

      - 2e-6

| Item | Value |
| --- | --- |
| **`TolX`** | — |

      - 2e-6

| Item | Value |
| --- | --- |
| **`Z_Tol`** | — |

      - 3e-5

| Item | Value |
| --- | --- |
| **{cspan}`1` *Extreme* (`!ExtremeSCF`/`Convergence Extreme`)** | — |

| Item | Value |
| --- | --- |
| **`ConvCheckMode`** | — |

      - 0

| Item | Value |
| --- | --- |
| **`TolE`** | — |

      - 1e-14

| Item | Value |
| --- | --- |
| **`TolMAXP`** | — |

      - 1e-14

| Item | Value |
| --- | --- |
| **`TolRMSP`** | — |

      - 1e-14

| Item | Value |
| --- | --- |
| **`TolErr`** | — |

      - 1e-14

| Item | Value |
| --- | --- |
| **`Thresh`** | — |

      - 3e-16

| Item | Value |
| --- | --- |
| **`TCut`** | — |

      - 3e-16

| Item | Value |
| --- | --- |
| **`TolG`** | — |

      - 1e-09

| Item | Value |
| --- | --- |
| **`TolX`** | — |

      - 1e-09

| Item | Value |
| --- | --- |
| **`Z_Tol`** | — |

      - 3e-06

| Item | Value |
| --- | --- |
| **`BFCut`** | — |

      - 3e-16

<a id="compoundAdditionalConvergenceThresholds"></a>
!!! note "Additional threshold choices set by the simple input keys (`!StrongSCF`, ...etc.)"
    :header-rows: 1

| Item | Value |
| --- | --- |
| **Block** | — |

      - Variable
      - Value

| Item | Value |
| --- | --- |
| **{cspan}`2` *Sloppy* (`!SloppySCF`)** | — |
| **`casscf`** | — |

      - `GTol`
      - 5.0e-3

| Item | Value |
| --- | --- |
| **—** | — |

      - `ETol`
      - 1.0e-6

| Item | Value |
| --- | --- |
| **`mdci`** | — |

      - `STol`
      - 1.0e-4

| Item | Value |
| --- | --- |
| **`mrci`** | — |

      - `ETol`
      - 1.0e-5

| Item | Value |
| --- | --- |
| **—** | — |

      - `RTol`
      - 1.0e-5

| Item | Value |
| --- | --- |
| **`cis`** | — |

      - `ETol`
      - 1.0e-5

| Item | Value |
| --- | --- |
| **—** | — |

      - `RTol`
      - 1.0e-5

| Item | Value |
| --- | --- |
| **{cspan}`2` *Loose* (`!LooseSCF`)** | — |
| **`casscf`** | — |

      - `GTol`
      - 5.0e-3

| Item | Value |
| --- | --- |
| **—** | — |

      - `ETol`
      - 1.0e-6

| Item | Value |
| --- | --- |
| **`mdci`** | — |

      - `STol`
      - 1.0e-4

| Item | Value |
| --- | --- |
| **`autoci`** | — |

      - `STol`
      - 1.0e-4

| Item | Value |
| --- | --- |
| **`mrci`** | — |

      - `ETol`
      - 1.0e-5

| Item | Value |
| --- | --- |
| **—** | — |

      - `RTol`
      - 1.0e-5

| Item | Value |
| --- | --- |
| **`cis`** | — |

      - `ETol`
      - 1.0e-5

| Item | Value |
| --- | --- |
| **—** | — |

      - `RTol`
      - 1.0e-5

| Item | Value |
| --- | --- |
| **{cspan}`2` *Normal* (`!NormalSCF`)** | — |
| **`casscf`** | — |

      - `GTol`
      - 1.0e-3

| Item | Value |
| --- | --- |
| **—** | — |

      - `ETol`
      - 1.0e-7

| Item | Value |
| --- | --- |
| **`mdci`** | — |

      - `STol`
      - 2.5e-5

| Item | Value |
| --- | --- |
| **`autoci`** | — |

      - `STol`
      - 2.5e-5

| Item | Value |
| --- | --- |
| **`mrci`** | — |

      - `ETol`
      - 1.0e-6

| Item | Value |
| --- | --- |
| **—** | — |

      - `RTol`
      - 1.0e-6

| Item | Value |
| --- | --- |
| **`cis`** | — |

      - `ETol`
      - 1.0e-6

| Item | Value |
| --- | --- |
| **—** | — |

      - `RTol`
      - 1.0e-6

| Item | Value |
| --- | --- |
| **{cspan}`2` *Strong* (`!StrongSCF`)** | — |
| **`casscf`** | — |

      - `GTol`
      - 5.00e-4

| Item | Value |
| --- | --- |
| **—** | — |

      - `ETol`
      - 6.66e-8

| Item | Value |
| --- | --- |
| **`mdci`** | — |

      - `STol`
      - 7.50e-6

| Item | Value |
| --- | --- |
| **`autoci`** | — |

      - `STol`
      - 7.50e-6

| Item | Value |
| --- | --- |
| **`mrci`** | — |

      - `ETol`
      - 6.66e-7

| Item | Value |
| --- | --- |
| **—** | — |

      - `RTol`
      - 6.66e-7

| Item | Value |
| --- | --- |
| **`cis`** | — |

      - `ETol`
      - 6.66e-7

| Item | Value |
| --- | --- |
| **—** | — |

      - `RTol`
      - 6.66e-7

| Item | Value |
| --- | --- |
| **{cspan}`2` *Tight* (`!TightSCF`)** | — |
| **`casscf`** | — |

      - `GTol`
      - 2.5e-4

| Item | Value |
| --- | --- |
| **—** | — |

      - `ETol`
      - 2.5e-8

| Item | Value |
| --- | --- |
| **`mdci`** | — |

      - `STol`
      - 1.0e-5

| Item | Value |
| --- | --- |
| **`autoci`** | — |

      - `STol`
      - 1.0e-5

| Item | Value |
| --- | --- |
| **`mrci`** | — |

      - `ETol`
      - 2.5e-7

| Item | Value |
| --- | --- |
| **—** | — |

      - `RTol`
      - 2.5e-7

| Item | Value |
| --- | --- |
| **`cis`** | — |

      - `ETol`
      - 2.5e-7

| Item | Value |
| --- | --- |
| **—** | — |

      - `RTol`
      - 2.5e-7

| Item | Value |
| --- | --- |
| **{cspan}`2` *VeryTight* (`!VeryTightSCF`)** | — |
| **`casscf`** | — |

      - `GTol`
      - 1.0e-5

| Item | Value |
| --- | --- |
| **—** | — |

      - `ETol`
      - 1.0e-8

| Item | Value |
| --- | --- |
| **`mdci`** | — |

      - `STol`
      - 1.0e-6

| Item | Value |
| --- | --- |
| **`autoci`** | — |

      - `STol`
      - 1.0e-6

| Item | Value |
| --- | --- |
| **—** | — |

      - `D3Thresh`
      - 1.0e-14

| Item | Value |
| --- | --- |
| **—** | — |

      - `D4Thresh`
      - 1.0e-14

| Item | Value |
| --- | --- |
| **—** | — |

      - `D5Thresh`
      - 1.0e-14

| Item | Value |
| --- | --- |
| **`mrci`** | — |

      - `ETol`
      - 1.0e-7

| Item | Value |
| --- | --- |
| **—** | — |

      - `RTol`
      - 1.0e-7

| Item | Value |
| --- | --- |
| **`cis`** | — |

      - `ETol`
      - 1.0e-7

| Item | Value |
| --- | --- |
| **—** | — |

      - `RTol`
      - 1.0e-7

| Item | Value |
| --- | --- |
| **{cspan}`2` *Extreme* (`!ExtremeSCF`)** | — |
| **`casscf`** | — |

      - `GTol`
      - 1.0e-9

| Item | Value |
| --- | --- |
| **—** | — |

      - `ETol`
      - 1.0e-12

| Item | Value |
| --- | --- |
| **`mdci`** | — |

      - `STol`
      - 1.0e-9

| Item | Value |
| --- | --- |
| **—** | — |

      - `TCutInt`
      - 0.0

| Item | Value |
| --- | --- |
| **`autoci`** | — |

      - `STol`
      - 1.0e-9

| Item | Value |
| --- | --- |
| **—** | — |

      - `D3Thresh`
      - 1.0e-14

| Item | Value |
| --- | --- |
| **—** | — |

      - `D4Thresh`
      - 1.0e-14

| Item | Value |
| --- | --- |
| **—** | — |

      - `D5Thresh`
      - 1.0e-14

| Item | Value |
| --- | --- |
| **`mrci`** | — |

      - `ETol`
      - 1.0e-12

| Item | Value |
| --- | --- |
| **—** | — |

      - `RTol`
      - 1.0e-12

| Item | Value |
| --- | --- |
| **`cis`** | — |

      - `ETol`
      - 1.0e-12

| Item | Value |
| --- | --- |
| **—** | — |

      - `RTol`
      - 1.0e-12

There is an additional set of simple keywords, 
`!SCFCONV<n>` with $n$ = 6--12 (e.g. `!SCFCONV8`),
which sets `TolE` = $10^{-n}$ and *most* of the other tolerances 
listed above to appropriate values. 
However, some, like `Z_Tol`, `TolRMSP`, and `TolMAXP` are not adjusted!
Hence, it is recommended to use the keywords given above instead.

If `ConvCheckMode=0`, *all* convergence criteria have to be satisfied
for the program to accept the calculation as converged, which is a quite
rigorous criterion. In this mode, the program also has mechanisms to
decide that a calculation is converged even if one convergence criterion
is not fulfilled but the others are overachieved. `ConvCheckMode=1`
means that one criterion is enough. This is quite dangerous, so ensure
that none of the criteria are too weak, otherwise the result will be
unreliable. The default `ConvCheckMode=2` is a check of medium rigor ---
the program checks for the change in total energy and for the change in
the one-electron energy. If the ratio of total energy and one-electron
energy is constant, the self-consistent field does not fluctuate anymore
and the calculation can be considered converged. If you have small
eigenvalues of the overlap matrix, the density may not be converged to
the number of significant figures requested by `TolMaxP` and `TolRMSP`.

`ConvForced` is a flag to prevent time consuming calculations on
non-converged wave functions. It will default to `ConvForced=1` for
Post-HF methods, Excited States runs and Broken Symmetry calculations.
You can overwrite this default behavior by setting `ConvForced=0`.

Irrespective of the `ConvForced` value that has been chosen, properties
or numerical calculations (NumGrad, NumFreq) will not be performed on
non-converged wavefunctions!

<a id="sec:essentialelements.scfconvergence.damping"></a>
## Dynamic and Static Damping

Damping is the oldest and simplest convergence aid. It was already
invented by Douglas Hartree when he did his famous atomic calculations.
Damping consists of mixing the old density with the new density as:

$$

P_{\text{new, damped} } =\left({ 1-\alpha } \right)P_{\text{new} } +\alpha P_{\text{old} }\qquad \text{(eq:50)}

$$

where $\alpha$ is the damping factor, which must have a value of less
than 1. Thus the permissible range (not checked by the program) is 0
...0.999999. For $\alpha$ values larger than 1, the calculation cannot
proceed since no new density is admixed. Damping is important in the
early stages of a calculation where $P_{\text{old} }$ and
$P_{\text{new} }$ are very different from each other and the energy is
strongly fluctuating. Many schemes have been suggested that vary the
damping factor dynamically to give strong damping in the beginning and
no damping in the end of an SCF. The scheme implemented in ORCA is that
by Hehenberger and Zerner [zerner1979chem](../../bibliography.md) and is invoked with
`CNVZerner=true`. Static damping is invoked with `CNVDamp=true`. These
convergers are mutually exclusive. They can be used in the beginning of
a calculation when it is not within the convergence radius of DIIS or
SOSCF. Damping works reasonably well, but most other convergers in ORCA
are more powerful.

If damping used in conjunction with DIIS or SOSCF, the value of
`DampErr` is important: once the DIIS error falls below `DampErr`, the
damping is turned off. In case SOSCF is used, `DampErr` refers to the
orbital gradient value at which the damping is turned off. The default
value is 0.1 Eh. In difficult cases, however, it is a good idea to
choose `DampErr` much smaller, e.g. 0.001. This is --- to some extent
--- chosen automatically together with the keyword `! SlowConv`.

```orca
%scf
  # control of the Damping procedure
  CNVDamp   true    # default: true
  CNVZerner false   # default: false
  DampFac   0.98    # default: 0.7
  DampErr   0.05    # default: 0.1
  DampMin   0.1     # default: 0.0
  DampMax   0.99    # default: 0.98
  # more convenient:
  Damp fac 0.98 ErrOff 0.05 Min 0.1 Max 0.99 end
end
```

<a id="sec:essentialelements.scfconvergence.levelshift"></a>
## Level Shifting

Level shifting is a frequently used technique. The basic idea is to
shift the energies of the virtual orbitals such that after
diagonalization the occupied and virtual orbitals mix less strongly and
the calculation converges more smoothly towards the desired state. Also,
level shifting should prevent flipping of electronic states in
near-degenerate cases. In a special context it has been shown by
Saunders and Hillier [guest1974mol,saunders1973int](../../bibliography.md) to be equivalent
to damping.

Similar to `DampErr` described in the previous section, `ShiftErr`
refers to the DIIS error at which the level shifting is turned off.

```orca
%scf
  # control of the level shift procedure
  CNVShift   true  # default: true
  LShift     0.1   # default: 0.25, energy unit is Eh.
  ShiftErr   0.1   # default: 0.0
  # more convenient:
  Shift Shift 0.1 ErrOff 0.1 end
end
```

<a id="sec:essentialelements.scfconvergence.diis"></a>
## Direct Inversion in Iterative Subspace (DIIS) 

The direct inversion in iterative subspace (DIIS) is a technique
that was invented by Pulay [pulay1980chem,pulay1982comp](../../bibliography.md). It has
become the *de facto* standard in most modern electronic structure
programs, because DIIS is robust, efficient and easy to implement.
Basically DIIS uses a criterion to judge how far a given trial density
is from self-consistency. The commutator of the Fock and density
matrices [**F**,**P**] is a convenient measure for this error. With
this information, an extrapolated Fock matrix from the present and
previous Fock matrices is constructed, which should be much closer to
self-consistency. In practice this is usually true, and better than
linear convergence has been observed with DIIS. In some rare
(open-shell) cases however, DIIS convergence is slow or absent after
some initial progress. As self-consistency is approached, the set of
linear equations to be solved for DIIS approaches linear dependency and
it is useful to bias DIIS in favor of the SCF cycle that had the lowest
energy using the factor `DIISBfac`. This is achieved by multiplying all
diagonal elements of the DIIS matrix with this factor unless it is the
Fock matrix/density which leads to the lowest energy. The default value
for `DIISBfac` is 1.05.

The value of `DIISMaxEq` is the maximum number of old Fock matrices to
remember. Values of 5-7 have been recommended, while other users store
10-15 Fock matrices. Should the standard DIIS not achieve convergence,
some experimentation with this parameter can be worthwhile. In cases
where DIIS causes problems in the beginning of the SCF, it may have to
be invoked at a later stage. The start of the DIIS procedure is
controlled by `DIISStart`. It has a default value of 0.2 Eh, which
usually starts DIIS after 0-3 cycles. A different way of controlling the
DIIS start is adjusting the value `DIISMaxIt`, which sets the maximum
number of cycles after which DIIS will be started irrespective of the
error value.

```orca
%scf
  # control of the DIIS procedure
  CNVDIIS     true  # default: true
  DIISStart   0.1   # default: 0.2
  DIISMaxIt   5     # default: 12
  DIISMaxEq   7     # default: 5
  DIISBFac    1.2   # default: 1.05
  # more convenient:
  DIIS Start 0.1  MaxIt 5  MaxEq 7  BFac 1.2  MaxC 15.0  end
end
```

Note that for troublesome or lacking SCF convergence the `TRAH` algorithm should be used
(see Sec. [sec:essentialelements.scfconvergence.trahscf](#sec:essentialelements.scfconvergence.trahscf)).
If not turned off explicitly, `TRAH` is switched on automatically
whenever convergence problems are present by means of the `AutoTRAH` feature
(see Sec. [sec:essentialelements.scfconvergence.trahscf](#sec:essentialelements.scfconvergence.trahscf)).

<a id="sec:essentialelements.scfconvergence.kdiis"></a>
## Kolmar's DIIS (KDIIS)

An alternative algorithm that makes use of the DIIS concept is called
KDIIS (Kolmar's DIIS[kollmar1996chem,kollmar1997int](../../bibliography.md)) in ORCA. The KDIIS algorithm is designed to bring the orbital
gradient of any energy expression to zero using a combination of DIIS
extrapolation and first order perturbation theory. Thus, the method is
diagonalization-free. In our hands it is superior to the standard DIIS
algorithm in many cases, but not always. The algorithm is invoked with
the keyword `! KDIIS` and is available for RHF, UHF and CASSCF.

<a id="sec:essentialelements.scfconvergence.soscf"></a>
## Approximate Second Order SCF (SOSCF) 

SOSCF is an approximately quadratically convergent variant of the SCF
procedure [fischer1992phys,neese2000chem](../../bibliography.md). The theory is relatively
involved and will not be described here. In short -- SOSCF computes an
initial guess to the inverse orbital Hessian and then uses the BFGS
formula in a recursive way to update orbital rotation angles. As
information from a few iterations accumulates, the guess to the inverse
orbital Hessian becomes better and better and the calculation reaches a
regime where it converges superlinearly. As implemented, the procedure
converges as well or slightly better than DIIS and takes a somewhat less
time. However, it is also *a lot* less robust, so that DIIS is the
method of choice for many problems (see also the description of the full second-order trust-region
augmented Hessian (`TRAH`) procedure in the next section). On the other hand, SOSCF
is useful when DIIS gets stuck at some error around $\sim$ 0.001 or
0.0001. Such cases were the primary motive for the implementation of
SOSCF into ORCA.

The drawback of SOSCF is the following: in the beginning of the SCF, the
orbital gradient (the derivative of the total energy with respect to
rotations that describe the mixing of occupied and virtual MOs) is
large, so that one is far from the quadratic regime. In such cases, the
procedure is not successful and may even wildly diverge. Therefore it is
recommended to only invoke the SOSCF procedure in the very end of the
SCF where DIIS may lead to "trailing" convergence. SOSCF is controlled
by the variables `SOSCFStart` and `SOSCFMaxIt`. `SOSCFStart` is a
threshold for the orbital gradient. When the orbital gradient, or
equivalently the DIIS Error, fall below `SOSCFStart`, the SOSCF
procedure is initiated. `SOSCFMaxIt` is the latest iteration to start
the SOSCF even if the orbital gradient is still above `SOSCFStart`.

```orca
%scf
  # control of the SOSCF procedure
  CNVSOSCF    true  # default: false
  SOSCFStart  0.1   # default: 0.01
  SOSCFMaxIt  5     # default: 1000
  # more convenient:
  SOSCF Start 0.1  MaxIt 5  end
end
```

For many calculations on transition metal complexes, it is a good idea
to be conservative in the startup criterion for SOSCF, it may diverge
otherwise. A choice of 0.01 or lower is recommended.

<a id="sec:essentialelements.scfconvergence.trahscf"></a>
## Trust-Region Augmented Hessian (TRAH) SCF

The **Trust-Region Augmented Hessian (TRAH)** method[Bacskay1981,Salek2007,Hoeyvik2012,Helmich-Paris2021b](../../bibliography.md)
 is a robust SCF convergence algorithm that ensures reliable convergence
 to the electronic ground state by using information from the electronic Hessian.
 It is especially useful for difficult SCF cases where standard DIIS/SOSCF approaches fail,
 such as open-shell systems or molecules with complex electronic structures.

### When to Use TRAH

The TRAH-SCF procedure can be:
- **Activated manually** using the `! TRAH` keyword.
- **Triggered automatically** (`AutoTRAH`) when standard SCF convergence is too slow or diverges.

```orca
%scf
  AutoTRAH true
end
```

#### AutoTRAH

The automatic mode (`AutoTRAH`) monitors the convergence behavior by performing a log-scale
 linear interpolation of the electronic gradient norm over several SCF iterations. 
After a minimum number of SCF iterations (`AutoTRAHIter`, default: 20), the algorithm
 analyzes the last `AutoTRAHNInter` (default: 10) values of the gradient norm. 
A linear fit is performed in $\log_{10}(||\mathbf{g}||)$ space, and the slope $s$ of
 this interpolation is used to assess convergence. 
If the slope indicates a convergence rate slower than $10^{-s}$, with $s < \texttt{AutoTRAHTol}$ 
(default: 1.125), standard SCF is stopped and TRAH-SCF is initiated using the current set of orbitals.

This mechanism allows ORCA to switch to the more robust TRAH-SCF method only when necessary, improving efficiency for difficult SCF cases while avoiding unnecessary overhead for easy ones.

To disable automatic activation:

```orca
! NOTRAH
```
or
```orca
%scf
  AutoTRAH false
end
```

### Theoretical Basis

TRAH builds a quadratic model of the SCF energy as a function of orbital rotations $\mathbf{x}$:

$$

E(\mathbf{x}) = E_0 + \mathbf{g}^T \mathbf{x} + \frac{1}{2} \mathbf{x}^T \mathbf{H} \mathbf{x}, \quad ||\mathbf{x}|| \le h

$$

Minimizing $E(\mathbf{x})$ under the trust region constraint leads to level-shifted Newton equations:\qquad \text{(\mathbf{H} - \mu \mathbf{I})}

$$

\mathbf{x} = -\mathbf{g}

$$

Instead of solving these directly, the algorithm solves the eigenvalue problem of the scaled augmented Hessian matrix:

$$

\begin{pmatrix}
  0 & \alpha \mathbf{g}^T \\
  \alpha \mathbf{g} & \mathbf{H}
\end{pmatrix}
\begin{pmatrix}
  1 \\
  \tilde{\mathbf{x}}
\end{pmatrix}
= \mu
\begin{pmatrix}
  1 \\
  \tilde{\mathbf{x}}
\end{pmatrix}

$$

The Davidson algorithm is used for iterative diagonalization until the residual norm of $\tilde{\mathbf{x}}$ is below `TolFacMicro × ||g||`.
The scaling factor $\alpha$ is adjusted via bisection
in the interval $[\alpha_0,\alpha_1]$ to ensure the trust region constraint is satisfied.

### Performance and Implementation Details

- **Parallelization**: TRAH is MPI-parallel and supports large molecules using AO-based Fock matrices.
- **Acceleration**: TRAH supports `RIJ`, `RIJONX`, `RIJK`, and `RIJCOSX`, and is compatible with solvation models like `C-PCM` and `SMD`.
- **Available Methods**: Implemented for `RHF`, `RKS`, `UHF`, and `UKS`. `ROHF` and `ROKS` are not yet supported.
- **Efficient Hessian Operations**: Similar to CP-SCF and TD-DFT, gradient and Hessian operations use AO-basis sigma vectors for efficiency.

Grid parameters to speed up these steps:

```orca
%method
  Z_GridXC   1      // Lebedev Grid
  Z_IntAccXC 3.467  // eps parameter of radial grid
  Z_GridX    1      // Lebedev Grid
  Z_IntAccX  3.067  // eps parameter of radial grid
end
```

<a id="sec:essentialelements.scfconvergence.trahscf.keywords"></a>
### Input Parameters

```orca
%scf

 # AutoTRAH parameter
 AutoTRAH       true      # enables by default
 AutoTRAHTol    1.125     # slop of gradient convergence
 AutoTRAHIter   20        # first iteration for which TRAH could be called
 AutoTRAHNInter 10        # number of iteration for monitoring convergence progress

 # TRAH parameter
 trah
   MaxRed          24     # maximum number of Davidson micro iterations
   NStart          2      # number of start vectors for Davidson (at least 2)
   TolFacMicro     0.1    # Scaling factor for Davidson convergence
                          #  threshold =  TolFacMicro * || G ||    
   MinTolMicro     1.e-2  # minimum accuracy of micro iterations
   QuadRegionStart 1.e-4  # start Newton-Raphson if || G || < QuadRegionStart 
   tradius         0.4    # initial trust radius
   AlphaMin        0.1    # lower bound of gradient scaling parameter
   AlphaMax        1000.  # upper bound of gradient scaling parameter
   Randomize       true   # add white noise to Davidson start vectors
   PseudoRand      false  # use pseudo random numbers for comparibility
   MaxNoise        1.e-2  # maximum random number magnitude
   OrbUpdate       Taylor # orbital update algorithm (TAYLOR or CAYLEY)
   InactiveMOs     Canonical # CANONICAL or NOTSET
   Precond         Diag   # DIAG, FULL, or NONE
   PreconMaxRed    250    # maximum dimension of FULL Hessian for preconditioning
 end

 TolG 1.e-6  # SCF convergence threshold for gradient norm

end
```

- `Precond = FULL` uses the exact Hessian for a subset of important MO pairs, improving convergence for small RHF/UHF systems but not necessarily for large molecules or DFT.
- For `FULL`, ensure RI and auxiliary basis (`/C`) are provided.

### Practical Notes

- **Quadratic Convergence**: Near the solution, TRAH achieves quadratic convergence.
- **Guaranteed Convergence**: In exact arithmetic and absent numerical noise, TRAH will always converge. If not, increase `MAXITER` or tighten numerical thresholds (e.g., grid accuracy).
- **LibXC Compatibility**: Some functionals lack ORCA-native kernels (e.g., `PWPB95`). Use `LIBXC(...)` for TRAH support.

### Example Case

In a high-spin $\mathrm{Rh}_{12}^+$ cluster, DIIS fails to converge while TRAH steadily reduces the gradient norm below $10^{-6}$:

*TRAH-SCF gradient norm of a PBE/def2-TZVP calculation for a
$\mathrm{Rh}_{12}^+$ cluster in high-spin configuration
($\mathrm{M_s} = 36$). Structure from Ref. [Harding2010](../../bibliography.md).*

<a id="sec:essentialelements.scf.finitetemp"></a>
## Finite Temperature SCF

A finite temperature can be used to apply a Fermi-like occupation number
smearing over the orbitals of the system, which may sometimes help to
get convergence of the SCF equations in near hopeless cases. Through the
smearing, the electrons are distributed according to Fermi statistics
among the available orbitals. The "chemical potential" is found through
the condition that the total number of electrons remains correct.
Gradients can be computed in the presence of occupation number smearing.

```orca
%scf SmearTemp 5000  # ``temperature'' in Kelvin
 end
```

!!! note

    -   Finite temperature SCF (fractional occupation numbers or FOD
        analysis,
        see sections [sec:essentialelements.scf.fracocc](#sec:essentialelements.scf.fracocc) and
        [sec:spectroscopyproperties.fod](#sec:spectroscopyproperties.fod), respectively) *cannot*
        be used together with `SOSCF` methods.

<a id="sec:essentialelements.scf.fracocc"></a>
### Fractional Occupation Numbers

Only a very basic implementation of fractional occupation numbers is
presently provided. It is meant to deal with orbitally degenerate states
in the UHF/UKS method. Mainly it was implemented to avoid symmetry
breaking in DFT calculations on orbitally degenerate molecules and
atoms. The program checks the orbital energies of the initial guess
orbitals, finds degenerate sets and averages the occupation numbers
among them. Currently the criterion for degenerate orbitals is $10^{-3}$
Eh. The fractional occupation number option is invoked by:

```orca
%scf
  FracOcc true
end
```

Clearly, the power of fractional occupation numbers goes far beyond what
is presently implemented in the program and future releases will likely
make more use of them. The program prints a warning whenever it uses
fractional occupation numbers. The fractionally occupied orbitals should
be checked to ensure they are actually the intended ones.

!!! note

    -   Using `GuessMode = CMatrix` will cause problems because there are no
        orbital energies for the initial guess orbitals. The program will
        then average over *all* orbitals --- which makes no sense at all.

<a id="sec:essentialelements.scfconvergence.tips"></a>
## Tips and Tricks: Converging SCF Calculations

Despite all efforts you may still find molecules where SCF convergence
is poor. These are almost invariably related to open-shell situations
and the answer is almost always to provide "better" starting orbitals.
Here is my standard strategy to deal with this (assuming a DFT
calculation):

-   Perform a small basis set (`SV`) calculation in using the `LSD` or
    `BP` functional and RI approximation with a cheap auxiliary basis
    set. Set `Convergence=Loose` and `MaxIter=200` or so. The key point
    is to use a large damping factor and damp until the DIIS comes into
    a domain of convergence. This is accomplished by `SlowConv` or even
    `VerySlowConv`. If you have an even more pathological case you may
    need to set `DampFac` larger and `DampErr` smaller than chosen by
    these defaults. This calculation is quite crude and may take many
    cycles to converge. It will however be rather quick in terms of wall
    clock time. If the DIIS gets stuck at some error 0.001 or so the
    `SOSCF` (or even better `TRAH`) could be put in operation from this
    point on.

-   Use the orbitals of this calculation and `GuessMode=CMatrix` to
    start a calculation with the target basis set. In DFT we normally
    use a pure GGA functional (e.g. BP86). This calculation normally
    converges relatively smoothly.

-   Use the target functional, grid etc. to get the final calculation
    converged. In many cases this should converge fairly well now.

Here are a few other things that can be tried:

-   Try to start from the orbitals of a related closed-shell species. In
    general closed-shell MO calculations tend to converge better. You
    then hope to reach the convergence radius of another converger for
    the open-shell case.

-   Try to start from the orbitals of a more positive cation. Cation
    calculations tend to converge better.

-   Try to start from a calculation with a smaller basis set. Smaller
    basis sets converge better. Then you have the choice of
    `GuessMode=CMatrix` or `GuessMode=FMatrix` which will affect the
    convergence behavior.

-   Use large level shifts. This increases the number of iterations but
    stabilizes the converger. (`shift shift 0.5 erroff 0 end`)

-   If you are doing DFT calculations try to start from a Hartree-Fock
    solution for your molecule. HF calculations tend to converge
    somewhat better because they have a larger HOMO-LUMO gap (there are
    of course exceptions).

-   Carefully look at the starting orbitals (`Print[P_GuessOrb]=1`) and
    see if they make sense for your molecule. Perhaps you have to
    reorder them (using `Rotate`) to obtain smooth convergence.

-   Most of the time the convergence problems come from "unreasonable"
    structures. Did you make sure that your coordinates are in the
    correct units (Angström or Bohrs?) and have been correctly
    recognized as such by the program?

-   If you have trouble with UHF calculations try ROHF (especially SAHF
    or CAHF) first and then go to the UHF calculation.

-   Fool around with `Guess=Hueckel`, `PAtom `or even `HCore`.

-   It may sometimes be better to converge to an undesired state and
    then take the orbitals of this state, reorder them (using `Rotate`)
    and try to converge to the desired state.

-   Similarly, bad orbitals may be manipulated using the SCF stability
    analysis (section
    [sec:essentialelements.stabilityanalysis](#sec:essentialelements.stabilityanalysis)) to provide a new
    guess.

-   Try to start the calculation with a large damping factor
    (`DampFac=0.90`; or even larger) and specify a relatively small DIIS
    error to turn damping off (say `DampErr=0.02`;). This will increase
    the number of cycles but may guide you into a regime were the
    calculation actually converges.

-   The advices above mostly apply to Hartree-Fock and DFT. For CASSCF,
    the available options and how they can aid to overcome convergence
    problems are described in the CASSCF manual section. In many cases
    modifying the initial guess or adding a level shift will help. Do
    not hesitate to use large level-shifts (e.g 2.0 or even 3.0). The
    manual is accompanied by CASSCF tutorial that goes through many
    details of the process including practical advices on convergence.
    The choice of initial guess is crucial. Some guesses work better for
    organic molecules while others excel for transition-metal complexes.
    The tutorial therefore discusses various initial guess options
    available in ORCA.

-   If you managed to converge your system in another quantum chemistry
    program, and do not want to waste time re-converging it in ORCA, then
    you may convert the converged orbitals in the other program to the
    ORCA format using third-party tools like MOKIT (section [sec:utilities.2mkl](#sec:utilities.2mkl)).
    However, keep in mind that converging a wavefunction in program A and
    reconverging it in program B comes with an inevitable overhead: program
    B usually has to perform a few extra SCF iterations even if the wavefunction
    is fully converged in program A, because (among many other reasons) the
    two programs in general use different integration grids. Therefore,
    use this method only when you expect a significant time saving.

-   If nothing else helps, stop, grab a friend and go to the next pub
    (you can also send me an unfriendly e-mail but this will likely not
    make your calculation converge any quicker; $\ddot \smile$).

<a id="sec:essentialelements.localSCF"></a>
## Local-SCF Method

The Local SCF (LSCF) method developed by X. Assfeld and J.-L. Rivail ([LSCF](../../bibliography.md)) allows optimising single determinant wave functions within the constraint of keeping some selected orbitals frozen (i.e. unchanged), whilst all orbitals fulfill orthogonality requirements. The LSCF method may be applied to unrestricted Hartree-Fock or DFT calculations.

The use of the LSCF method consists of selecting the set of orbitals to freeze during the SCF process according to the guess orbitals of the calculation. The selection is done by employing the `LSCFalpha` and/or `LSCFbeta` keywords in the SCF bloc for alpha and beta orbitals, respectively, followed by the orbital selection. **Intervals** are used to define the selection and one may go up to five intervals (5$\times$2 numbers separate with commas).  In the example below, `LSCFalpha 0,1,4,4,10,12` corresponds to freezing the alpha orbitals from 0 to 1 (**0,1**,4,4,10,12), orbital 4 (0,1,**4,4**,10,12), and from 10 to 12 (0,1,4,4,**10,12**). Accordingly, `LSCFbeta  0,3,5,5` corresponds to freezing beta orbitals 0 to 3 and orbital 5.

```orca
%scf
LSCFalpha 0,1,4,4,10,12
LSCFbeta  0,3,5,5
end
```

The energy of frozen orbitals is meaningless since they are not eigenfunctions of the Fockian. During the LSCF process, the energy of the occupied frozen orbitals is artificially defined as the lowest occupied orbital energy of the guess orbitals minus 1000 Hartree, while for the virtual frozen orbitals, the energy is defined as the highest virtual orbital energy plus 1000 Hartree. Hence, all occupied frozen orbitals are sorted at the beginning of the orbital distribution and the virtual frozen orbitals at the end.

<a id="sec:essentialelements.scf.keywords"></a>
## Keywords

Simple input keywords related to the SCF procedure are summarized in
[sec:essentialelements.scf.keywords](#sec:essentialelements.scf.keywords).

<a id="tab:essentialelements.scf.keywords.simple"></a>
!!! note "Simple input keywords for the SCF procedure"
    :header-rows: 1
    :class: footnotesize

| Item | Value |
| --- | --- |
| **Keyword** | — |

      - Description

| Item | Value |
| --- | --- |
| **{cspan}`1` *Convergence acceleration*** | — |
| **`DIIS`** | — |

      - Enable [DIIS](sec:essentialelements.scfconvergence.diis)

| Item | Value |
| --- | --- |
| **`NoDIIS`** | — |

      - Disable [DIIS](sec:essentialelements.scfconvergence.diis)

| Item | Value |
| --- | --- |
| **`KDIIS`** | — |

      - Enable [Kollmar's DIIS](sec:essentialelements.scfconvergence.kdiis)

| Item | Value |
| --- | --- |
| **`TRAH`** | — |

      - Enable [TRAH](sec:essentialelements.scfconvergence.trahscf)

| Item | Value |
| --- | --- |
| **`NoTRAH`** | — |

      - Disable [TRAH](sec:essentialelements.scfconvergence.trahscf)

| Item | Value |
| --- | --- |
| **`SOSCF`** | — |

      - Enable [SOSCF](sec:essentialelements.scfconvergence.soscf)

| Item | Value |
| --- | --- |
| **`NoSOSCF`** | — |

      - Disable [SOSCF](sec:essentialelements.scfconvergence.soscf)

| Item | Value |
| --- | --- |
| **`Damp`** | — |

      - Enable [damping](sec:essentialelements.scfconvergence.damping)

| Item | Value |
| --- | --- |
| **`NoDamp`** | — |

      - Disable [damping](sec:essentialelements.scfconvergence.damping)

| Item | Value |
| --- | --- |
| **`LShift`** | — |

      - Enable [level shifting](sec:essentialelements.scfconvergence.levelshift)

| Item | Value |
| --- | --- |
| **`NoLShift`** | — |

      - Disable [level shifting](sec:essentialelements.scfconvergence.levelshift)

| Item | Value |
| --- | --- |
| **{cspan}`1` *Solver parameter selection (see [sec:essentialelements.scfconvergence.damping](#sec:essentialelements.scfconvergence.damping))*** | — |
| **`EasyConv`** | — |

      - Assumes no convergence problems.

| Item | Value |
| --- | --- |
| **`NormalConv`** | — |

      - Default solver parameters

| Item | Value |
| --- | --- |
| **`SlowConv`** | — |

      - Selects appropriate SCF solver parameters for difficult cases. 
        Most transition metal complexes fall into this category.

| Item | Value |
| --- | --- |
| **`VerySlowConv`** | — |

      - Selects appropriate SCF solver parameters for very difficult cases.

| Item | Value |
| --- | --- |
| **`SCFCONV<n>`** | — |

      - Adjusts `TolE` to 10e-n and most of the other tolerances according to [compoundConvergenceThresholds](#compoundConvergenceThresholds) and [compoundAdditionalConvergenceThresholds](#compoundAdditionalConvergenceThresholds) (not recommended!)

| Item | Value |
| --- | --- |
| **{cspan}`1` *[Fractional occupation numbers](sec:essentialelements.scf.fracocc)*** | — |
| **`FracOcc`** | — |

      - Enable fractional occupations (also compute [FOD](sec:spectroscopyproperties.fod))

| Item | Value |
| --- | --- |
| **`Smear`** | — |

      - Enable occupation number smearing with `SmearTemp=5000` 
        (also compute [FOD](sec:spectroscopyproperties.fod))

| Item | Value |
| --- | --- |
| **`NoSmear`** | — |

      - Disable occupation number smearing

| Item | Value |
| --- | --- |
| **`FOD`** | — |

      - Perform [FOD analysis](sec:spectroscopyproperties.fod)
        with default settings (TPSS/def2-TZVP, TightSCF, SmearTemp = 5000 K)

