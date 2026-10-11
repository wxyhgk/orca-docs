

<a id="sec:modelchemistries.dmrg"></a>
# Density Matrix Renormalization Group (DMRG)

*The `BLOCK` code in ORCA is only available on the Linux platform!*

`BLOCK` is an implementation of the density matrix renormalization group
(DMRG) algorithm from the Chan group.
[chan2002jcp,chan2004jcp,gosh2008jcp,sharma2012jcp,sharma2011AnnRev](../../bibliography.md)
The references given should be cited when using this part of the
program. `BLOCK` is platform dependent and several crashes have been reported in the past. 
Please contact the [`BLOCK` developers](https://github.com/sanshar/Block) when you are affected.

The DMRG is a variational wavefunction method. It can be viewed as (i)
an efficient method for strong correlation in large complete active
spaces, (ii) a brute force method to systematically approach FCI for a
large number of electrons and orbitals, (iii) a polynomial cost route to
exact correlation in pseudo-one-dimensional molecules, such as chains
and rings.

Although the algorithm is somewhat complicated compared to many quantum
chemistry methods, significant effort has been devoted in `BLOCK` to
ensure that it can be run in a simple black-box fashion. In most cases,
only a single keyword needs to be specified.

To provide an idea of how the DMRG can be used, here are some examples.
The timings will vary depending on your computational setup, but the
following are calculations that run in a few hours to a day, on a single
12-core Xeon Westmere cluster node:

-   Complete active space (CAS) CI calculations for active spaces with
    up to 30 electrons in 30 active orbitals, targetting up to 1--10
    states, e.g. Jacobsen's catalyst in a 32 electron, 25 orbital active
    space,

-   One-dimensional chain molecules, with "widths" of up to 4 orbitals,
    and about 100 orbitals in total, e.g. the$\pi$-active space of a
    4$\times$25 graphene nanoribbon,

-   FCI benchmark solutions in molecules with fewer than 20 electrons,
    and up to 100 orbitals, e.g. C$_2$ in a cc-pVTZ basis,D$_{\text{2h} }$ symmetry (12 electrons in 60 orbitals),

-   Accuracies in energy differences or total energies of about 1
    kcal/mol.

The following are calculations which are possible with the `BLOCK` code,
but which are challenging, and require large memory (e.g. up to 8 GB per
core) and computational time (e.g. from a day to more than a week on up
to 6 12-core Xeon Westmere nodes),

-   Complete active space (CAS) CI calculations in active spaces with
    around 40 electrons in 40 active orbitals, targetting a few states,
    for example, an Fe(II)-porphine (40 electrons in 38 orbitals) with
    an active space of Fe 3d, 4d and all porphine$\pi$ and$\sigma$
    donor orbitals, or an Fe 3d, S 3p active space calculation for
    [Fe$_4$S$_4$(SCH$_3$)$_4$]$^{2-}$,

-   One-dimensional chain molecules, with "widths" of up to 6 orbitals,
    and about 100 total orbitals,

-   Champion FCI benchmark solutions in small molecules, such as
    butadiene in a cc-pVDZ basis (22 electrons in 82 orbitals),

-   Accuracies in energy differences or total energies of about 1
    kcal/mol.

If any these calculations interest you, then you might want to try a
DMRG calculation with `BLOCK`!

## Technical capabilities

Currently, `BLOCK` implements the following

-   An efficient DMRG algorithm for quantum chemistry Hamiltonians

-   Full spin-adaptation (SU(2) symmetry) and Abelian point-group
    symmetries

-   State-averaged excited states

Note that the standalone version of `BLOCK` may provide more
capabilities than are available through the external interface. See the
`BLOCK` website for details [chan](../../bibliography.md).

<a id="sec:modelchemistries.dmrg.papers"></a>
## How to cite

We would appreciate if you cite the following papers in publications
resulting from the use of `BLOCK` :

-   G. K.-L. Chan and M. Head-Gordon, *J. Chem. Phys.* **116**, 4462
    (2002),

-   G. K.-L. Chan, *J. Chem. Phys.* **120**, 3172 (2004),

-   D. Ghosh, J. Hachmann, T. Yanai, and G. K.-L. Chan, *J. Chem.
    Phys.*, **128**, 144117 (2008),

-   S. Sharma and G. K-.L. Chan, *J. Chem. Phys.* **136**, 124121
    (2012).

In addition, useful DMRG references relevant to quantum chemistry can be
found in the review below by Chan and Sharma.

-   G. K-.L. Chan and S. Sharma, *Ann. Rev. Phys. Chem.* **62**, 465
    (2011),
<a id="sec:modelchemistries.dmrg.commands"></a>
## Basic Usage 

Within ORCA, the `BLOCK` program is accessed as part of the CASSCF
module. `BLOCK` can be run in two modes: CASCI mode (no orbital
optimization) or CASSCF mode. To enable CASCI mode, set `maxiter 1`.

```orca
%casscf
   maxiter 1 # remove if doing CASSCF
   CIStep DMRGCI
   ...
   end
```

For small molecule CASCI it may be possible to correlate all orbitals.
In general, similar to a standard CASSCF calculation, it is necessary to
select a sensible active space to correlate. (See
Section [commands.casscf](#sec:modelchemistries.dmrg.commands.casscf) on CASSCF). This is the
responsibility of the user.

Once the orbitals to correlate have been chosen, and the wavefunction
symmetries and quantum numbers are specified, the accuracy of the DMRG
calculation is governed by two parameters: the maximum number of
renormalized states$M$; and, the order and localization of the
orbitals.

The most important parameter in the DMRG calculation is$M$, the number
of renormalized states. This defines the maximum size of the
wave-function expansion, which is$O(M^2)$ in length in the renormalizedbasis. As$M$ is increased, the DMRG energy converges to the exact (FCI
or CASCI) limit.

The DMRG maps orbitals onto a 1D lattice, thus the best results are
achieved if strongly interacting orbitals are placed next to each other.
For this reason, the DMRG energy is not generally invariant to orbital
rotations within the active space, and orbital rotation and ordering can
improve the DMRG energy for a given$M$. As$M$ is increased, the DMRG
energy becomes less and less sensitive to the orbital ordering and
localization.

To minimize the number of wavefunction optimization steps, it is often
advantageous to perform DMRG calculations at small$M$, then increase
$M$ to the final maximum value. This sequence of optimizations is
governed by the *sweep schedule*, which specifies how many optimization
steps (sweeps) to perform at each intermediate value of$M$.

The above may seem to make running a DMRG calculation more complicated
than a usual quantum chemistry calculation, however, `BLOCK` provides a
set of default settings which eliminate the need to specify the above
parameters by hand. We highly recommend that you first learn to use the
`BLOCK` program *with these default settings*. In the default mode, the
orbitals are ordered automatically (Fiedler vector
method [Fiedler1973,Fiedler1975,Atkins1998,Barcza2011](../../bibliography.md)) and a
default sweep schedule is set.

An example of a default CASCI calculation on the C~2~ molecule
correlating all electrons in a VTZ basis, is given here:

```orca
%casscf
   maxiter 1 # remove if doing CASSCF
   CIStep DMRGCI
   ...
   end
```

Once you are familiar with the default mode, we recommend exploring the
localization of orbitals. In general, DMRG benefits from the use of
localized orbitals, and these should be used unless the high-symmetry of
the molecule (e.g., D$_{2h}$ symmetry) provides compensating
computational benefits. We recommend using "split-localized" orbitals,
which correspond to localizing the occupied and virtual orbitals
separately. An example of a split-localized default DMRG calculation on
the porphine molecule, correlating the full$\pi$-space (26 electrons in
24 orbitals), in a cc-pVDZ basis is given in
Sec. [orcaporphine.detailed](#sec:dmrg.orcaporphine.detailed).

For a given `maxM`, it can take a long time to tightly converge DMRG
calculations (e.g. to the default 1e-9 tolerance). To decrease
computation time, you may wish to loosen the default tight sweep
tolerance or control the maximum number of sweep iterations with the
commands `sweeptol` and `maxIter`.

<a id="sec:modelchemistries.dmrg.commands.casscf"></a>
### Orbital optimization

Orbital optimization (mixing the external/internal space with the active
space, not to be confused with orbital rotation and ordering in the
active space) in DMRG calculation can be performed by using the `BLOCK`
program as the "CIStep" within a CASSCF calculation, as described above.
For the moment, spin-densities and related properties are not available
for this `CIStep`.

During the optimization iterations it is important that the active
orbitals maintain their overlap and ordering with previous iterations.
This is done using `actConstrains`. This flag is set by default.

```orca
%casscf
ActConstrains  1 # maintain shape and ordering of active orbitals
...
end
```

In general, performing a DMRG calculation with orbital optimization is
quite expensive. Therefore, it is often best to carry out the orbital
optimization using a small value of `maxM` (enabled by the default
parameters `maxM=25` and the resulting sweep schedule), and to carry out
a final single-point calculation using a larger value of `maxM`.

### Advanced options

There may be times when one wants finer control of the DMRG calculation.
All keywords are shown in the *complete set of BLOCK
options* [commands.block](#sec:modelchemistries.dmrg.commands.block) below. The `startM`
command allows to change the starting number of states in DMRG
calculations. It is also possible to specify the entire sweep schedule
manually. A sweep schedule example follows:

```orca
%casscf
   ...
  dmrg

    MaxIter          14
    switch_rst       1e-3
    TwoDot_to_oneDot 12
    NSchedule        3
    sche_iteration   0,     4,    8
    sche_M          50,   100,  500
    sche_sweeptol 1e-4,  1e-6, 1e-9
    sche_noise    1e-8, 1e-11,  0.0

  end
end
```

The commands above are:

-   `MaxIter`, corresponds to the maximum number of sweeps done by DMRG;

-   `NSchedule`, specifies the total number of schedule parameters we
    will specify;

-   `Sche_iteration`, details the sweep number at which to change the
    parameters of the calculation. Notice count begins at 0;

-   `Sche_M`, is the number of renormalized states at each sweep;

-   `Sche_sweeptol`, is the tolerance of the Davidson algorithm;

-   `Sche_noise`, is the amount of perturbative noise we add each sweep;

-   `Twodot_to_onedot`, specifies the sweep at which the switch is made
    from a twodot to a onedot algorithm. The recommended choice is to
    start with twodot algorithm and then switch to onedot algorithm a
    few sweeps after the maximum$M$ has been reached. To do a
    calculation entirely with the twodot or the onedot algorithm,
    replace the `twodot_to_onedot` line with `twodot 1` or `onedot 1`;

-   `switch_rst`, defines the switching threshold of orbital gradient
    below which DMRG turns to onedot algorithm and restarts from
    previous operators and wavefunction. This is essential to avoid
    oscillation of energy values in the orbital optimization.

The default DMRG sweep schedule is selected automatically according to
the choice of computational mode. By default two different sets of
predefined schedules are supported for CASCI and CASSCF computations,
respectively.

In CASCI mode, the default schedule corresponds to the following:
starting from a given `startM` (where the default is 250 and 8 sweeps),
increase to a value of 1000 (8 sweeps) and increment by 1000 every 4
iterations until `maxM` is reached. The algorithm switches from twodot
to onedot two sweeps after the `maxM` has been reached.

In CASSCF mode, the orbital optimization requires much fewer
renormalized states to converge the wavefunction with respect to orbital
rotations. The default schedule therefore starts with `startM` (where
the default is 25 and 2 sweeps), and increments by a factor of 2 every 2
sweeps util `maxM` is reached. The algorithm continues the sweep at
`maxM` by decreasing the Davison tolerance `sche_sweeptol` and noise
level `sche_noise` every 2 cycles by a factor of 10, until
`sche_sweeptol` becomes smaller than `sweeptol`.

For better control of the orbital ordering, we also provide a genetic
algorithm minimization method of a weighted exchange matrix. The genetic
algorithm usually provides a superior orbital ordering to the default
ordering, but can itself take some time to run for large numbers of
orbitals. The genetic algorithm can be enabled by

```orca
%casscf
   ...
   DMRG
     auto_ordering GAOPT
   end
end
```

within the `%casscf` input.

### Troubleshooting

The two most common problems with DMRG calculations are that (i)
convergence with `maxM` is slower than desired, or (ii) the DMRG sweeps
get stuck in a local minimum. (i) is governed by the orbital ordering /
choice of orbitals. To improve convergence, turn on the genetic
algorithm orbital ordering.

If you suspect (ii) is occurring, the simplest thing to do is to
increase the starting number of states with the `startM` (e.g. from 500
to 1000 states). Local minima can also sometimes be avoided by
increasing the noise in the DMRG schedule, e.g. by a factor of 10. To
check that you are stuck in a local minimum, you can carry out a DMRG
extrapolation (see extended Manual in the `BLOCK` website).

Note that the present DMRG-SCF establishes the input order of active
space orbitals according to their Hartree-Fock occupancy, even if these
orbitals are ultimately canonical or split-localized canonical in
nature. This is specified by `hf_occ` in which the Hartree-Fock
occupancy is derived by default from the one-electron integrals. Other
options for obtaining the occupancy are available
(see [commands.block](#sec:modelchemistries.dmrg.commands.block)).

Somet times the energy values produced from one SCF cycle to another may
oscillate. Such a nonlinear numerical behaviour may occur typically by
the last few iterations, most likely caused by the loss of a certain
distribution of quantum numbers (eg, particle number, irrep symmetry and
spin) in the blocking and decimation procedure due to incomplete
many-body basis. On the other hand, the loss of quantum numbers is the
main source of energy discontinuities on potential energy curves
calculated by DMRG-SCF using a small number of renormalized states.

In the current release of DMRG-SCF implementation, the number of quantum
states is locked to avoid these problems. The locking mechanism is
turned on when the orbital gradient falls below a certain threshold
defined by the keyword `switch_rst` (default: 0.001). The DMRG
calculation then starts from previous operators and wavefunction in
which a perturbative noise is not added. Locking quantum states and
restaring DMRG wavefunction not only ensures a smooth convergence
towards the final energy but also minimizes the number of iterations.
Note that the locking procedure introduces an arbitrariness to the final
energy, when a very small$M$ is used, since the final digits of energy
depend on where the locking begins. It is therefore not recommended to
start locking too early in iterations which could trap the orbital
solution in a local mimimum. Finally the quality of resulting orbitals
can be checked by carrying out a DMRG calculation with sufficient
renormalized states. Using the default value of `switch_rst` DMRG-SCF
usually results in the orbitals that are good enough to reproduce the
CASSCF energy.

<a id="sec:modelchemistries.dmrg.commands.block"></a>
## Keywords

```orca
%casscf
 ...
 # enable DMRG as CI solver (mandatory)
 CIStep DMRGCI
 
 # refined optional settings for DMRG
 dmrg
 startM   25     # CASSCF mode: number of re-normalized states for a singlee root
          250    # CASCI mode: number of re-normalized states for a single root
 maxM     25     # CASSCF mode: number of re-normalized states for a singlee root
          250    # CASCI mode: number of re-normalized states for a single root
 DryRun   false  # just create an input for Block
 SweepTol 1e-9   # energy tolerance for the sweeps 
 auto_ordering NOREORDER # auto_ordering is an int. If set to 0
                         # or the alias NOREORDER, the reordering is skipped.
               FIEDLER   # (default) let Block optimize the active orbital ordering
               GAOPT     # let Block optimize the active orbital ordering
                         # using genetic algorithm
 hf_occ   0 # user-defined initial Hartree-Fock occupancy manually
          1 # default: initial Hartree-Fock occupancy based on the values of 
              the one-electron integrals
          2 # initial Hartree-Fock occupancy based on the energy ordering 
              of canonical orbitals

 TwoDot_to_OneDot  1  # Switch from two-dot expressions to one-dot
 OneDot  0   # Only one-dot expressions. %In CASCI mode only.
 TwoDot  0   # Only two-dot expressions. %In CASCI mode only.
 switch_rst 1e-3   # Specify the threshold of orbital gradient below which DMRG
                     swithches to one-dot expression by reading previous wavefunction.
 warmup  1   # wilson warm-up type
         2, 3 or 4   # n=3 is the default option. 
                       The full configuration space of the n sites next to the system 
                       constitutes the environment states in the warm-up. 
                       The remaining sites use the Hartree-Fock guess occupation
 nonspinadapted 0   # default: spin-adapted DMRG
                1   # non-spin-adatped DMRG in which the spin-density calculation 
                      is available
                

 # Define a schedule for DMRG
 MaxIter   14   # Specify maximum number of iterations
 NSchedule -1   # default sweep schedule in CASSCF mode 
            0   # default sweep schedule in CASCI mode
           >0   # Number of manual sweep schedule parameters 
                # All schedule parameters must be set if this flag is set manually!
 sche_iteration 0, 4, 8   # vector with sweep-number to execute changes
                          # (schedule parameter)

 sche_M       50,100,500 # vector with corresponding M values (schedule parameter)
 sche_sweeptol 1e-4,1e-6,1e-9  # vector with sweep tolerances (schedule parameter)
 sche_noise     1e-8, 1e-11,0.0 # vector with the noise level (schedule parameter)

 # Define a separate maxM for DMRG-NEVPT2
 nevpt2_maxm 25   # set maximum number of renormalized states 
                    for DMRG-NEVPT2 calculation (default: MaxM)

 end
end
```

<a id="sec:dmrg.orcaporphine.detailed"></a>
## Example: Porphine$\pi$-active space calculation

We provide a step-by-step basis on localizing the$\pi$-orbitals of the
porphine molecules and running a CASSCF-DMRG calculation on this system.
It will be important to obtain an initial set of orbitals, rotate the
orbitals which are going to be localized, localize them, and finally run
the CASSCF calculation. We will abbreviate the coordinates as
$\left[\dots\right]$ after showing the coordinates in the first input
file, but please note they always need to be included.

1.  First obtain RHF orbitals:

    ```orcainput
    # To obtain RHF orbitals 
    !cc-pVDZ 
    * xyz 0 1
    N      2.10524     -0.00000     0.00000 
    N     -0.00114      1.95475    -0.00000
    N     -2.14882      0.00000    -0.00000 
    N     -0.00114     -1.95475     0.00000
    C      2.85587     -1.13749    -0.00000
    C      2.85587      1.13749     0.00000 
    C      1.02499      2.75869    -0.00000 
    C     -1.10180      2.78036     0.00000
    C     -2.93934      1.13019    -0.00000
    C     -2.93934     -1.13019     0.00000
    C     -1.10180     -2.78036    -0.00000
    C      1.02499     -2.75869     0.00000
    C      4.23561     -0.67410    -0.00000
    C      4.23561      0.67410     0.00000 
    C      0.69482      4.18829    -0.00000 
    C     -0.63686      4.14584    -0.00000 
    C     -4.25427      0.70589    -0.00000 
    C     -4.25427     -0.70589     0.00000
    C     -0.63686     -4.14584     0.00000 
    C      0.69482     -4.18829     0.00000
    H      5.10469     -1.31153     0.00000 
    H      5.10469      1.31153    -0.00000
    H      1.36066      5.02946     0.00000 
    H     -1.28917      5.00543     0.00000 
    H     -5.12454      1.34852     0.00000 
    H     -5.12454     -1.34852    -0.00000 
    H     -1.28917     -5.00543    -0.00000 
    H      1.36066     -5.02946    -0.00000 
    C      2.46219      2.41307     0.00000 
    C     -2.39783      2.44193     0.00000 
    C     -2.39783     -2.44193    -0.00000 
    C      2.46219     -2.41307    -0.00000 
    H      3.18114      3.22163    -0.00000 
    H     -3.13041      3.24594    -0.00000 
    H     -3.13041     -3.24594     0.00000 
    H      3.18114     -3.22163     0.00000
    H      1.08819      0.00000    -0.00000 
    H     -1.13385     -0.00000     0.00000 
    *  
    ```

2.  We then swap orbitals with$\pi$-character so they are adjacent to
    each other in the active space. ($\pi$ orbitals are identified by
    looking at the MO coefficients). When they are adjacent in the
    active space, they can be easily localized in the next step.

    ```orca
    #To rotate the orbitals (so that we can localize them in the next step) 
    !cc-pvdz moread noiter 
    %moinp "porphine.gbw" 
    %scf 
        rotate 
        # Swap orbitals
        {70, 72}
        {65, 71}
        {61, 70}
        {59, 69}
        {56, 68}
        {88, 84}
        {92, 85}
        {93, 86}
        {96, 87}
        {99, 88} 
        {102, 89}
        {103, 90}
        {104, 91}
        end
    end 
    * xyz 0 1
    [...] 
    *
    ```

3.  After rotating the orbitals, we localize the 13 occupied
$\pi$-orbitals. This is performed using the `orca_loc` code. The
    input file follows.

    ```orca
    porphine_rot.gbw 
    porphine_loc.gbw 
    0
    68
    80
    120
    1e-3
    0.9
    0.9
    1
    ```

4.  After localizing the occuppied orbitals, we localize the 11 virtual
$\pi$-orbitals using the `orca_loc` code once again. The input file
    follows.
    
    ```orca
    porphine_loc.gbw
    porphine_loc2.gbw
    0
    81
    91
    120
    1e-3
    0.9
    0.9
    1
    ```

5.  After these steps are complete, we run a CASSCF-DMRG calculation.
    The standard input file is shown below

    ```orca
    !cc-pVDZ moread pal4 
    %moinp "porphine_loc2.gbw" 
    %MaxCore 16000

    %casscf nel 26
    norb 24
    nroots 1
    CIStep DMRGCI 
    end 
    * xyz 0 1
    [...] 
    *
    ```    
