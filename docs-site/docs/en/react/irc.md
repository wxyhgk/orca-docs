---
title: Intrinsic Reaction Coordinate (IRC)
source: https://www.faccts.de/docs/orca/6.1/tutorials/react/irc.html
---

# Intrinsic Reaction Coordinate (IRC)

The Intrinsic Reaction Coordinate (IRC) is a special form of a minimum energy path that connects a transition state (TS) with its downhill-nearest intermediates.
A method determining the IRC is thus useful to determine whether a transition state is directly connected to a given reactant and/or product.
ORCA features its own implementation of Morokuma and coworkers’ popular method.[[Morokuma1977]](../bib.md#morokuma1977) The IRC method can be requested via the `IRC` simple keyword:

```text
!r2SCAN-3c IRC

*XYZFILE 0 1 ts.xyz
```

## Example: C-H Activation

In this example, we will compute the IRC for a transition state of the oxidative addition of methane to a simplified version of Vaska's complex
*trans*-IrCl(CO)[P($CH_3$)_3]_2. The TS was previously found and refined with the [NEB-TS](../react/nebts.md) method.

```mol
title: C-H activation TS
theme: chem311
height: 360px
representation: ball-stick
--- xyz ---
17
structure
  Ir         -0.00143203185660     -0.40016488969675      0.03600314399579
  Cl          0.27432628484078     -1.83023426743014     -2.03825688023739
  P           2.30014009485774     -0.48172068528262     -0.14772560683377
  C          -0.02121270169362     -1.23605900736449      1.73436404624705
  P          -2.27594323302349     -0.58761407009326     -0.21317913320443
  H          -2.68663330488284     -1.37330032274147     -1.30871960349281
  H          -3.05919038571534     -1.15082285974451      0.81663891095385
  H          -3.03113073166368      0.58692361406174     -0.44014225111597
  H           2.84623185761250      0.07294458775872     -1.32086169502718
  H           3.14186888192656      0.12479537665057      0.81660238174806
  H           2.85543190418513     -1.77235084163730     -0.18646215265715
  O          -0.07230769468533     -1.69639717783789      2.79715324662842
  C          -0.05176600095842      1.93204198398446      0.03356757877794
  H          -0.04515219643699      0.93288193095392     -0.99727302980658
  H           0.69877281269545      2.50898477621244     -0.51346377818299
  H          -1.03674756641744      2.35694073296797     -0.16633235178920
  H           0.16474401121560      2.01315111923861      1.09808717399636
```


> **Note**
> Note that the IRC method can be directly requested together with the `OPTTS`, `SCANTS`, `NEB-TS`, `FREQ` and `NUMFREQ` keywords. Per default the IRC code checks
> whether a Hessian was computed before the IRC run. If that is not the case, and if no Hessian is provided via the `%IRC` block, a new Hessian is computed at the beginning of the IRC run.

> **Important**
> The same method and basis set as used for optimization and frequency calculation should be used for the IRC run!

We now request the IRC calculation on our given transition state. Note that we exemplarily increased the number of maximum iterations from 20 (default) to 30 via the `%IRC` block.
More details on available IRC settings can be found in the respective section of the [ORCA manual](https://www.faccts.de/docs/orca/6.0/manual/contents/detailed/frequencies.html#sec-frequencies-irc-detailed).

```text
!r2SCAN-3c IRC

%IRC
 MAXITER 30
END

*XYZFILE 0 1 ts.xyz
```

After an initial energy and gradient calculation, the IRC procedure is initiated:

```text
--------------------------------------------------------------------------------
                   Intrinsic Reaction Coordinate Calculation
--------------------------------------------------------------------------------

System:
Nr. of atoms                        .... 17
Algorithm: SD (steepest descent step) plus correction
Settings:
Max. no of cycles        MaxIter    .... 50
Direction                           .... Forward and backward
Initial displacement Hessian type   .... Compute numerically
Following Hessian mode              .... 0
Initial displacement type           .... Energy
  Initial displacement energy change.... 2.000 mEh
Coordinate system following type    .... Cartesian
Length of steepest descent step     .... 0.150 bohr
Do parabolic fit
  if SD step is uphill              .... YES
Do Correction to SD step            .... YES
Scaling for length of correction
  compared to SD step               .... 0.333
Do parabolic fit to SD correction   .... YES
Only interpolate for parabolic fit  .... YES
Do update to length of
  SD step and correction            .... YES
Convergence Tolerances:
  Max. Gradient            TolMAXG  ....  2.0000e-03 Eh/bohr
  RMS Gradient             TolRMSG  ....  5.0000e-04 Eh/bohr
Storing full IRC trajectory in      .... orca_IRC_Full_trj.xyz
Storing forward trajectory in       .... orca_IRC_F_trj.xyz
Storing backward trajectory in      .... orca_IRC_B_trj.xyz
```

As we did not provide any Hessian or specify the Hessian calculation in our input, ORCA will perform a numerical Hessian calculation first:

```text
----------------------------------------------------------------------------
                           ORCA NUMERICAL FREQUENCIES
----------------------------------------------------------------------------
```

Afterwards, the computed Hessian will be read automatically and the forward IRC calculation will start:

```text
*************************************************************
         *                          FORWARD IRC                      *
         *************************************************************

Iteration    E(Eh)      dE(kcal/mol)  max(|G|)   RMS(G)
Convergence thresholds                0.002000  0.000500
    0     -1404.718702   -0.809101    0.020193  0.004018
[...]
```

Next, the backward IRC is computed:

```text
*************************************************************
         *                          BACKWARD IRC                     *
         *************************************************************

Iteration    E(Eh)      dE(kcal/mol)  max(|G|)   RMS(G)
Convergence thresholds                0.002000  0.000500
    0     -1404.719178   -1.108245    0.014077  0.003383
[...]
```

Finally, the IRC path is summarized:

```text
---------------------------------------------------------------
                       IRC PATH SUMMARY
---------------------------------------------------------------
All gradients are in Eh/Bohr.

Step        E(Eh)      dE(kcal/mol)  max(|G|)   RMS(G)
   1     -1404.757622   -25.231708    0.004829  0.001679
[...]
  31     -1404.717412    0.000000    0.000149  0.000056 <= TS
[...]
  61     -1404.775014   -36.145667    0.005752  0.002294
```

Additionally, various useful files are written:

1. `basename_IRC_F.xyz`: endpoint of the forward run.
2. `basename_IRC_F_trj.xyz`: trajectory of the forward run.
3. `basename_IRC_B.xyz`: endpoint of the backward run.
4. `basename_IRC_B_trj.xyz`: trajectory of the backward run.
5. `basename_IRC_Full_trj.xyz`: full trajectory of the complete IRC run.

If we now look at the end-point of the backward IRC, we see that it the expected product of the oxidative addition or C-H activation of methane with the methyl and hydrogen substituents in *cis* arrangement
in the equatorial plane of the octahedral product complex. The end-point of the forward IRC is the quadratic planar Vaska's type complex with a weakly coordinated methane molecule.

[![irc-full](../images/irc-full.png)](../images/irc-full.png)

*Figure: IRC path with molecular structures of the starting TS and the end-points.*

> **Important**
> The end-point of the IRC are not fully optimized structures and subsequent [geometry optimizations](../prop/geoopt.md) should be performed to obtain the final reactant and product structures!
