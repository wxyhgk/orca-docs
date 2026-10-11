```{index} IRC
```

(sec:structurereactivity.irc)=
# Intrinsic Reaction Coordinate

The Intrinsic Reaction Coordinate (IRC) is a special form of a minimum
energy path, connecting a transition state (TS) with its
downhill-nearest intermediates. A method determining the IRC is thus
useful to determine whether a transition state is directly connected to
a given reactant and/or a product. The implementation in ORCA follows
the method suggested by Morokuma and coworkers.{cite}`Morokuma:JCP1977`
The IRC method follows the gradient of the nuclear coordinates. As the
gradient is negligible at a TS, first an initial displacement from the
TS structure has to be carried out, based on the eigenmodes of the
Hessian, in order to get to a region with a non-negligible gradient. For
the initial displacement the eigenvector of the eigenmode with the lowest
frequency (hessMode=0) is normalized and then scaled by Scale_Displ_SD
(which by default is chosen such that an energy change of Init_Displ_DE
can be expected). Two initial displacements, forward and backward, are
taken by adding the resulting displacement vector (multiplied with +1
and -1, respectively) to the initial structure. If the user requests the
downhill direction (e.g. from a previous unconverged IRC run), it is
assumed that the gradient is nonzero and thus no initial displacement is
carried out.

After the initial displacement, the iterations of the IRC method begin.
Each iteration consists of two main steps, each of which consists again of
multiple SP and gradient runs:

1.  Initial steepest descent (SD) step:

    1.  The gradient (grad0) of the starting geometry (G0) is
        normalized, scaled by Scale_Displ_SD, and the resulting
        displacement vector (SD1) is applied to G0.

2.  Optional (if SD_ParabolicFit is true): If SD1 increases the
        energy, a linear search is taken along the direction of the
        displacement vector:

        1.  The displacement vector SD1 is scaled by 0.5 (SD2 = 0.5 x
            SD1) and again added to G0.

        2.  A parabolic fit for finding the displacement vector (SD3)
            which leads to minimal energy is carried out using the three
            SP energies (G0, geometry after SD1 and after SD2 step). SD3
            has the same direction as SD1 and SD2, but can have a
            different length.

        3.  The keyword Interpolate_only controls whether the length of
            SD3 has to be in between 0 and the length of SD1. If
            that is the case, the maximum length is determined by SD1,
            the minimum length is zero.

    3.  At the resulting geometry G1 (G0+SD1 or G0+SD3) the gradient is
        calculated (grad1).

2.  Optional (if Do_SD_Corr is true): Correction to the steepest descent
    step:

    1.  Based on grad0 and grad1 a vector is computed which represents a
        correction to the first SD (SD1 or SD3) step. This correction
        brings the geometry closer to the IRC.

    2.  This vector is normalized, scaled by Scale_Displ_SD_Corr times
        the length of SD1 or SD3, and the resulting displacement vector
        (SDC1) is applied to G1.

    3.  Optional (if SD_Corr_ParabolicFit is true):

        1.  If the energy increases after applying step SDC1, SDC1 is
            scaled by 0.5 (SDC2 = 0.5 x SD1), if the energy decreases,
            SDC1 is scaled by 2 (SDC2 = 2 x SD1). SDC2 is then added to
            G1.

        2.  A parabolic fit for finding the displacement vector (SDC3)
            which leads to minimal energy is carried out using the three
            SP energies (G1, geometry after SDC1 and after SDC2 step).
            SDC3 has the same direction as SDC1 and SDC2, but can have a
            different length.

        3.  The keyword Interpolate_only controls whether the length of
            SDC3 has to be in between 0 and the length of SDC1. If
            that is the case, the maximum length is determined by SDC1,
            the minimum length is zero.

    4.  At the resulting geometry G2 (G1+SDC1 or G1+SDC3) the gradient
        is calculated (grad2).

3.  The gradient at the new geometry is checked for convergence.

4.  Optional (if Adapt_Scale_Displ is true):

    1.  If the resulting overall step size is smaller than 0.5 times
        Scale_Displ_SD, Scale_Displ_SD is multiplied by 0.5.

    2.  If the resulting overall step size is larger than 2 times
        Scale_Displ_SD, Scale_Displ_SD is multiplied by 2.

    3.  Scale_Displ_SD may not become smaller than 1/16 times the
        initial Scale_Displ_SD and not larger than 4 times the initial
        Scale_Displ_SD.

## Basic Usage

The following keywords are available:

```orcainput
! B3LYP SV(P) TightSCF KDIIS SOSCF Freq IRC 
* xyz 0 2
  C  -0.000   0.001   -0.000
  H   1.290   0.005   -0.006
  H  -0.330   1.050   -0.002
  H  -0.252  -0.532   -0.929
  H  -0.286  -0.545    0.911
  O   2.499   0.220    0.065
  H   2.509   1.085    0.525
*
```

:::{Note}
-   The same method and basis set as used for optimization and frequency
    calculation should be used for the IRC run.

-   The IRC keyword can be requested without, but also together with
    OptTS, ScanTS, NEB-TS, AnFreq and NumFreq keywords.

-   In its default settings the IRC code checks whether a Hessian was
    computed before the IRC run. If that is not the case, and if no
    Hessian is defined via the %irc block, a new Hessian is computed at
    the beginning of the IRC run.

-   A final trajectory (\_IRC_Full_trj.xyz) is generated which contains
    both directions, forward and backward, by starting from one endpoint
    and going to the other endpoint, visualizing the entire IRC. Forward
    (\_IRC_F\_trj.xyz and \_IRC_F.xyz) and backward (\_IRC_B\_trj.xyz
    and \_IRC_B.xyz) trajectories and xyz files contain the IRC and the
    last geometry of that respective run.
:::

(sec:structurereactivity.irc.keywords)=
## Keywords
```orca
! IRC
%irc
   MaxIter    20
   PrintLevel 1   
   Direction  both # both - default
                   # forward
                   # backward
                   # down
 # Initial displacement  
   InitHess   read # by default ORCA uses the Hessian from AnFreq or NumFreq, or
                   # computes a new one
                   # read    - reads the Hessian that is defined via Hess_Filename
                   # calc_anfreq  - computes the analytic Hessian
                   # calc_numfreq - computes the numeric Hessian 
   Hess_Filename "h2o.hess"  # input Hessian for initial displacement, must be used
                             # together with InitHess = read
   hessMode   0  # Hessian mode that is used for the initial displacement. Default 0                
   Init_Displ_DE      # DE (default) - energy difference
                      # length       - step size
   Scale_Init_Displ 0.1 # step size for initial displacement from TS. Default 0.1 a.u.
   DE_Init_Displ    2.0 # energy difference that is expected for initial displacement 
                        #  based on provided Hessian (Default: 2 mEh)
 # Steps
   Follow_CoordType cartesian # default and only option
   Scale_Displ_SD       0.15  # Scaling factor for scaling the 1st SD step
   Adapt_Scale_Displ    true  # modify Scale_Displ_SD when the step size becomes 
                              # smaller or larger
   SD_ParabolicFit      true  # Do a parabolic fit for finding an optimal SD step
                              # length
   Interpolate_only     true  # Only allow interpolation for parabolic fit, not
                              # extrapolation
   Do_SD_Corr           true  # Apply a correction to the 1st SD step
   Scale_Displ_SD_Corr  0.333 # Scaling factor for scaling the correction step to 
                              # the SD step. It is multiplied by the length of the 
                              # final 1st SD step
   SD_Corr_ParabolicFit true  # Do a parabolic fit for finding an optimal correction
                              # step length
 # Convergence thresholds - similar to LooseOpt
   TolRMSG   5.e-4      # RMS gradient (a.u.)
   TolMaxG   2.e-3      # Max. element of gradient (a.u.)
 # Output options   
   Monitor_Internals # Up to three internal coordinates can be defined 
      {B 0 1}        # for which the values are printed during the IRC run.
      {B 1 5}        # Possible are (B)onds, (A)ngles, (D)ihedrals and (I)mpropers
   end 
 end
```

NOTE

-   For direction=down (downhill) no initial displacement is necessary,
    and thus no Hessian is needed.
