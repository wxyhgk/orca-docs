

<a id="sec:spectroscopyproperties.vpt2"></a>
# Anharmonic Analysis and Vibrational Corrections using VPT2/GVPT2 and `orca_vpt2`

Building upon (analytical) harmonic calculations of the Hessian, it is
possible to calculate the cubic plus semi-quartic force field as well as higher-order
property derivatives. For this purpose, the VPT2 module will compute the
Hessian and then generate two displaced geometries for each degree of
freedom and for each displacement another Hessian (and another property
in case of vibrational corrections) will be computed. These are required
for an anharmonic analysis according to second-order vibrational
perturbation theory. So overall, using VPT2 is costly due to the number
of calculations required for the numerical derivatives and is very
sensitive to numerical noise due to convergence, approximations and
other settings. The VPT2 calculation can be initiated either via the
simple input command `!VPT2` or via the VPT2 keyword in the `%vpt2`
block. Finer control can be achieved through the `%VPT2` block, as
exemplified in this analysis of water.

```orcainput
# VPT2 Analysis of H2O
!RHF def2-SVP ExtremeSCF VPT2

%vpt2
  VPT2               On      # do a VPT2 analysis, same as !VPT2 (see above)
  AnharmDisp         0.05    # anharmonic displacement factor, default is 0.05
  HessianCutoff      1e-12   # cut-off for Hessian elements, default is 1e-10
  PrintLevel         1       # VPT2 print level [1, 2, 3, 4]
  MinimiseOrcaPrint  True    # Minimises the remaining orca output
end

%method
    Z_Tol               1e-14
end

* xyz 0 1
  O   0.00000000000000      0.06256176106279      0.06256176106280
  H   0.00000000000000     -0.06185639479702      0.99929463373422
  H   0.00000000000000      0.99929463373424     -0.06185639479703
*
```

After the analysis, a `<basename>.vpt2` file should be present in the
working directory. Within that file all the force field and property
derivatives are saved. It is used as an input for the `orca_vpt2`
programme which is called automatically after the initial displacement
calculations. The programme can also be called separately with the
command `orca_vpt2 <basename>.vpt2`.

!!! note
    ***A few remarks about VPT2 calculations:***

    -   A VPT2 starting geometry **should always be tightly converged**. For
        small molecules the `!TightOPT` option is not good enough !
        Depending on your structure, you might want to experiment with the
        `TolE`, `TolRMSG` and `TolMaxG` keywords of the `%geom` block.

    -   Similarly, a well converged SCF is required. The use of the
        `ExtremeSCF` keyword or at least `VeryTightSCF` is recommended.

    -   The CP-SCF equations should be converged to at least $10^{-12}$
        (modified via the `Z_Tol` setting in the `%method` block.

    -   For DFT calculations, tight grids like `DEFGRID3` are strongly recommended.

    -   **Linear molecules are not supported yet**

    -   Currently, only methods for which analytical Hessians are available
        are supported. Furthermore, **VPT2 calculations with DFT functionals
        which do not provide analytical Hessians cannot be carried out**.

    -   By default, updated atomic masses are used to generate the
        semi-quartic force field (see
        [sec:structurereactivity.frequencies.massdependencies](#sec:structurereactivity.frequencies.massdependencies)). The masses
        are also printed in the `<basename>.vpt2` file

    -   A VPT2 analysis can be repeated on a previous calculation
        by running `orca_vpt2 <basename>.vpt2`.

    -   VPT2 does have limited restart capabilities. If the directory in
        which the VPT2 run is carried out already contains `<basename>.hess`
        or `<basename>_eprnmr.property.txt` files, the program will skip
        these points and use the information provided in the files.

VPT2 provides a vibrational analysis and thus access to :
- mean and mean square displacement expectation values
- centrifugal distortion constants
- Watson's symmetrically and asymmetrically reduced Hamiltonian parameters
- anharmonic constants 
- Fermi resonance analysis
- rotational and vibrational-rotational constants
- fundamental transition (anharmonic frequencies)
- zero-point ro-vibrational energies 
- overtones and combination bands with intensities
  (in contrast to NEARIR with full VPT2/GVBT2 treatment)
- dedicated file interface for codes like SPCAT

If the computed data should be used for the simulation of spectra 
with codes like SPCAT, ORCA can provide a dedicated file that 
can serve as a basis for an input. This is triggered in the 
`%output` block when a VPT2 calculation is run:  

```orca
%output 
 Pickettname "pickett.txt"
end
```

This way, ORCA will generate a file called `pickett.txt` that contains 
the computed data and templates for `.var` which can be modified 
to serve as input for codes like SPCAT. Please note that this feature
is still being refined and extended.  

<a id="sec:spectroscopyproperties.vpt2.properties"></a>
## Vibrational corrections of molecular properties using VPT2

Using VPT2 it is also possible to compute zero-point vibrational
corrections to molecular properties. Currently, this is available for
NMR chemical shieldings, spin-spin coupling constants, g- and A-tensors
and requires two successive calculations. The first calculation is a
VPT2 calculation just as shown above (`<basename>.inp`) that contains
the `VPT2` command and the level of theory at which the Hessians are
computed. The second calculation (let's call it `<basename>_Prop.inp`
will compute the property derivatives with a final call to VPT2. In
order for this to work, the property derivative calculation needs to
read the `<basename>.hess` and `<basename>.vpt2` file from the
forcefield calculation. This is done by specifying the
`%geom inhess read` with the command `inhessname "<basename>.hess"`.
This scheme is necessary as properties other than energies, geometries
or frequencies often require specialized methods and basis sets. For the
numerical calculation of the force field and property derivatives different
stepsizes can be used by specifying `AnharmDisp` and `PropDisp` in the
VPT2 input block. The defaults are 0.05, and after the calculation, the
displaced geometries are stored in files named `myjob_DH001.xyz` and
`myjob_DP001.xyz` etc.

A typical example for calculating the vibrational correction to the
$^{13}$C NMR chemical shifts of methanol with a B3LYP/def2-TZVP
anharmonic forcefield and TPSS/pcSseg-2 shielding tensors would look
like the following: the standard input file, in our case `vpt2_methanol_FF.inp` with the
level of theory for the Hessian and the VPT2 input block :

```orcainput
!B3LYP D3 def2-TZVP def2/J def2/JK DEFGRID3 ExtremeSCF VPT2

%method
    Z_Tol  1e-12
end

* xyz 0 1
C  -1.09849212248373      0.14540972773089     -0.00000275092982
O   0.32138758531316      0.08706714755687     -0.00001212477411
H   0.66732439683790      0.98510769198508      0.00001819506998
H  -1.45583606337199     -0.88374271593276      0.00000595999622
H  -1.49206267729630      0.64725244577978      0.89143349761200
H  -1.49208273899904      0.64724452288014     -0.89144277697426
*
```

and the next input file, say `vpt2_methanol_NMR.inp` with the same
geometry and the level of theory for the shielding tensor will look like
this:

```orca
!TPSS pcSseg-2 Autoaux ExtremeSCF NMR

%geom inhess read
 inhessname "vpt2_methanol_FF.hess"
end

%vpt2
  VPT2          on
  AvgProp       NMR
  HessianCutoff 1e-12
end

%method
  Z_Tol         1e-12
end

* xyz 0 1
C  -1.09849212248373      0.14540972773089     -0.00000275092982
O   0.32138758531316      0.08706714755687     -0.00001212477411
H   0.66732439683790      0.98510769198508      0.00001819506998
H  -1.45583606337199     -0.88374271593276      0.00000595999622
H  -1.49206267729630      0.64725244577978      0.89143349761200
H  -1.49208273899904      0.64724452288014     -0.89144277697426
*
```

Running ORCA successively on both of these input files in the same
directory will yield an output that contains the zero-point vibrational
corrections to the shielding tensors for each atom. For Atom 0, which is
the carbon in methanol, it looks like this:

```orca
----- 
 Vibrationally averaged isotropic shieldings 
 ---- 

Atom 0 :

 mode    <q>       <q2>      dS/dQ    d2S/dQ2
-----------------------------------------------
   0  -0.000017   0.202578  -0.000089  -5.922644
   1  -0.034052   0.057707   8.269988  -5.666515
   2  -0.036827   0.055687   5.667278 -13.843941
   3   0.000002   0.051446   0.000073  -7.353936
   4   0.027471   0.043993   0.423409  -6.207061
   5  -0.009357   0.040649 -12.736464   3.762324
   6  -0.000001   0.040278  -0.001621  -2.224536
   7   0.001277   0.039898  -1.266298  -3.916647
   8  -0.031609   0.020149  51.647411 -21.635780
   9  -0.000021   0.019859   0.035760 -61.239749
  10  -0.010397   0.019376  18.573156 -50.591165
  11  -0.026641   0.015808  -8.871055  -6.654795
-----------------------------------------------

zpv correction to isotropic shift :  -4.840215 ppm
-----------------------------------------------
```

So the absolute shielding constant of carbon in methanol needs to be
corrected by -4.8 ppm due to zero-point vibration. From the mean and
mean square displacements and the first and second derivatives of the
shieldings with respect to the normal modes, one can also identify
degrees of freedom which give rise to larger contributions of the
vibrational correction.

A similar input for the HH spin-spin coupling constants would look
like this : 

```orca
!TPSS pcJ-2 Autoaux ExtremeSCF NMR

%geom inhess read
 inhessname "vpt2_methanol_FF.hess"
end

%maxcore 4096

%vpt2
  VPT2          on
  AvgProp       JCOUPLING
  AnharmDisp    0.05
  HessianCutoff 1e-12
end

%method
  Z_Tol         1e-12
end

%eprnmr
  Tol           1e-10
end

* xyz 0 1
C  -1.09849212248373      0.14540972773089     -0.00000275092982
O   0.32138758531316      0.08706714755687     -0.00001212477411
H   0.66732439683790      0.98510769198508      0.00001819506998
H  -1.45583606337199     -0.88374271593276      0.00000595999622
H  -1.49206267729630      0.64725244577978      0.89143349761200
H  -1.49208273899904      0.64724452288014     -0.89144277697426
*

%eprnmr
Nuclei = all H {ssfc}
end

```

As mentioned above, the exact same procedure is also available for
A-tensors. Here is an example for the NH$_2$ radical with the VPT2 input
file `vpt2_NH2_FF.inp` :

```orcainput
!UKS BP86 def2-svp def2/J ExtremeSCF defgrid3

%vpt2
    VPT2                On
end

%method
    Z_Tol               1e-12
end

* xyz 0 2
N   -0.01498947828047     -0.01894387811818      0.00000000000000
H   1.03197835263254      0.00908678452370      0.00000000000000
H   -0.22855980523269      1.00639225931822      0.00000000000000
*
```

and the input file - something like `vpt2_NH2_A.inp` - for the level of
theory that will be used in the A-tensor computation:

```orca
!UKS BP86 def2-SVP TightSCF

%geom inhess read
 inhessname "vpt2_NH2_FF.hess"
end

%vpt2
    VPT2                On
    AvgProp             Atensor
end

*xyz 0 2
N   -0.01498947828047     -0.01894387811818      0.00000000000000
H   1.03197835263254      0.00908678452370      0.00000000000000
H   -0.22855980523269      1.00639225931822      0.00000000000000
*

%eprnmr
Nuclei = all N { aiso, adip }
Nuclei = all H { aiso, adip }
end
```

and similarly for the g-tensor if `Atensor` is replaced by `Gtensor` in the `%vpt2` 
block (the `%eprnmr` block can be omitted then). 

Note that a convenient way to compute vibrational corrections is the usage
of a compound script. With an input file called `NH2.inp` :

```orca
* xyz 0 2
N   0.00312611577632      0.00395297373474      0.00000000000000
H   1.01930353842041      0.00049997276783      0.00000000000000
H   -0.23400058507735      0.99208221922117      0.00000000000000
*

%Compound "NH2.cmp"
```

and the corresponding compound script `NH2.cmp`:

```orca
New_Step
!UHF def2-SVP VeryTightSCF  

%vpt2
    VPT2                On      
end

%method
    Z_Tol               1e-12
end

* xyz 0 2
N   0.00312611577632      0.00395297373474      0.00000000000000
H   1.01930353842041      0.00049997276783      0.00000000000000
H   -0.23400058507735      0.99208221922117      0.00000000000000
*
Step_End

New_Step
!UHF def2-SVP VeryTightSCF 

%geom inhess read
 inhessname "NH2_Compound_1.hess"
end

%vpt2
    VPT2                On
    AvgProp             Atensor
end

*xyz 0 2
N   0.00312611577632      0.00395297373474      0.00000000000000
H   1.01930353842041      0.00049997276783      0.00000000000000
H   -0.23400058507735      0.99208221922117      0.00000000000000
*

%eprnmr 
Nuclei = all N { aiso, adip }
Nuclei = all H { aiso, adip }
end

Step_End

END
```
a similar result can be obtained in one calculation. 

!!! note
    Make sure the correct hessian file names are
    given and the input files MUST not contain a compound block. You can also
    rerun the VPT2 analysis using `orca_vpt2` directly. If you have an anharmonic force field
    calculation named `myjob_ff` and a property derivative calculation named `myjob_prop` just
    call `orca_vpt myjob_ff.vpt2 myjob_prop.vpt2`.

