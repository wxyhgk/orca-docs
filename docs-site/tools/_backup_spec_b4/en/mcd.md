

<a id="sec:spectroscopyproperties.mcd"></a>
# Simulation of (Magnetic) Circular Dichroism and Absorption Spectra 

<a id="sec:spectroscopyproperties.mcd.general"></a>
## General description of the program

ORCA can now simulate optical spectra that include spin-orbit coupling
contributions at all levels of theory by using a common implementation.
[foglia_mcd_2022](../../bibliography.md)

Following the energy-loss approach, the absorption cross section for a
transition between states $\tilde{P}$ and $\tilde{Q}$ can be expressed
as:

$$

\begin{split}
     \sigma_{\tilde{P}\tilde{Q} } = \frac{4 \pi^2}{c (E_{\tilde{Q} }-E_{\tilde{P} }) } |T_{\tilde{P}\tilde{Q} }|^2,
\end{split}

$$

where c is the speed of light; $E_{\tilde{P} }$ and $E_{\tilde{Q} }$
are the energy of the states ${\tilde{P} }$ and ${\tilde{Q} }$, respectively; 
$T_{{\tilde{P} }{\tilde{Q} }}$ is the transition moment between states
${\tilde{P} }$ and ${\tilde{Q} }$ and it can be computed with different
expressions based on the applied approximation.
Under a dipolar approximation to the light-matter interaction, the
transition moment takes the form:

$$

\begin{split}
     T_{{\tilde{P} }{\tilde{Q} }} =& { \sum_{i=1}^N  \bra{{\tilde{P} }}
     \mathcal{E} \cdot \hat{\textbf{p} }_i
     %
     \ket{{\tilde{Q} }} }, \\
\end{split}

$$

where the sum runs over all electrons $i$; $\hat{\textbf{p} }_i$ is the
linear momentum operator; and $\mathcal{E}$ is the polarization vector
of the incident light.
In order to take into account all the electric and magnetic mechanisms
in the transition, it is necessary to use the full field-matter 
interaction operator (FFMIO). For transition moment, it leads to the 
equation [Eq](#eqn:exactTM).

$$

\begin{split}
     T_{{\tilde{P} }{\tilde{Q} }} =& \frac{e}{m_e} \sum_{i=1}^N  \bra{{\tilde{P} }}
     \mathcal{E} \cdot \Big[     e^{i\textbf{k}\cdot \hat{\textbf{r} }_i }
     %\textbf{\hat{r}_i} }
     %
     \hat{\textbf{p} }_i \Big]\ket{{\tilde{Q} }}
     %
\end{split}\qquad \text{(eqn:exactTM)}

$$

where $\hat{r}_i$ is the position operator of i-th electron and $\textbf{k}$ is
the wave vector that points in the direction of the light propagation whose 
magnitude is related to the wavelength by $\lambda = 2 \pi / |\textbf{k}|$.

For free-rotating molecules, it is necessary to consider all possible orientations
of the molecule with respect to the direction of the incident light. In some cases,
such as the absorption of linear-polarized light under a dipolar approximation, 
the effect of the orientation can be averaged analytically. However, numerical 
integration over some selected molecular orientations, labeled as $o$ in equation
[Eq](#eqn:OrientAver), is generally necessary.

$$

\begin{split}
     <\sigma_{{\tilde{P} }{\tilde{Q} }}> = \sum_o w_o \frac{4 \pi^2}{c (E_{{\tilde{Q} }}(o)-E_{\tilde{P} }(o)) } |T_{{\tilde{P} }{\tilde{Q} }}(o)|^2
\end{split}\qquad \text{(eqn:OrientAver)}

$$

where $w_o$ is the weight of the orientation in the quadrature.

The implementation has been designed to compute the absorption of
circularly-polarized light on systems under the effect of an additional
external magnetic field, B, which modifies the states $\tilde{P}$ and
$\tilde{Q}$ for each orientation $o$ through a Zeeman perturbation. The
computed results are presented as the difference in the absorption of
the left (-) and right (+) circularly-polarized light ($\Delta$f$_{osc}$) and
as the sum of the oscillator strength (f$_{osc}$), which corresponds to the
linearly-polarized light absorption. The molecular orientations are
constructed by using rotation matrices with three Euler angles: $\chi$,
$\theta$, and $\phi$. Herein, $\chi$ (the rotation angle on a plane
perpendicular to the direction of external magnetic field/incident
light) is integrated analytically whereas $\theta$ and $\phi$ are taken
on a grid.

Finally, the states $\tilde{P}$ and $\tilde{Q}$ are obtained from QDPT
by expanding the states over non-relativistic eigenstates of
$\hat{H}_{0}$ ($\{I,J\}$) and the coefficients of the expansion
($d_{I\tilde{Q} }$) are obtained from the diagonalization of the complex
matrix, which contains $\hat{H}_{0}$ as well as the SOC and Zeeman
contributions (and SSC, if it is implemented in the selected electronic
structure theory) expressed in $\{I,J\}$.

$$

\begin{split}
    \bra{\Psi_I^{SM} }\hat{H}_{0}+\hat{H}_{SOC}+\hat{H}_{Zeeman}\ket{\Psi_J^{S'M'} }= \delta_{IJ}\delta_{SS'}\delta_{MM'}E_I^S +  \bra{\Psi_I^{SM} }\hat{H}_{SOC}+\hat{H}_{Zeeman}\ket{\Psi_J^{S'M'} }
\end{split}\qquad \text{(eqn:mcdqdpt)}

$$

<a id="sec:spectroscopyproperties.mcd.example"></a>
## Running and analyzing MCD calculations in TDDFT module 

A minimum input to compute the Magnetic Circular Dichroism (MCD) requires
setting the keyword DoMCD to true and to include an intensity for the
external magnetic field B (in Gauss). An example input for the TD-DFT module
is as follows:

```orca
! B3LYP def2-QZVPP

%tddft
    TDA False
    NROOTS 10
    DoSOC True
    DoMCD True
    B 50000.0
end

*xyz 0 1
 O     0.24287127056830      0.00033994295362      0.29479344369591
 C     0.13113617562040      0.00013705972874      1.65093880501262
 C     1.35780003491446     -0.00017874911331      2.22574232397512
 C     2.30247996517358     -0.00017814489451      1.14947275232337
 C     1.57300244613625      0.00013652073221      0.00793218434497
 H    -0.86951534119903      0.00025858475406      2.04160438459058
 H     1.56899490845286     -0.00038874637444      3.28047030533440
 H     3.37570289422870     -0.00038632501973      1.22171814100713
 H     1.83015664610447      0.00025985723335     -1.03506234028415
*
```

In the output file of this job, the estimated oscillator strengths (f$_{osc}$)
and the difference between left and right circularly polarized light absorption
($\Delta$f$_{osc}$) are provided:

```orca
------------------------------------------------------------------------------
           MCD Transitions via transition electric dipole moments
                B =  50000.00 Gauss  T =   300.000 K
------------------------------------------------------------------------------

                   dfosc             fosc           dfosc/fosc

 0 -> 1       -0.0000000000       0.0000000003      -0.0663180503
 0 -> 2        0.0000000000       0.0000000005       0.0000209714
 0 -> 3        0.0000000000       0.0000000003       0.0661609417
 0 -> 4       -0.0000000001       0.0000000004      -0.2991916107
 0 -> 5       -0.0000000000       0.0000000006      -0.0009270335
 0 -> 6        0.0000000001       0.0000000004       0.2984154405
 0 -> 7        0.0000000003       0.0000000008       0.3721777693
 0 -> 8       -0.0000000000       0.0000000009      -0.0002960328
 0 -> 9       -0.0000000003       0.0000000008      -0.3689867758
 0 ->10       -0.0000050986       0.1741092913      -0.0000292840
```

These results may not be accurate when the energetic order of the states changes
with respect to the relative orientation between the molecule and the external
magnetic field. To obtain accurate results, it is necessary to perform a 
post-processing step for all orientations using the `orca_mapspc` program,
which saves the results in a file that has the `.cis-el.dipole-length.1.mcd` extension: 

```orca
orca_mapspc fur-mcd.cis-el.exact.1.mcd MCD -x050000 -x155000 -n10000 -w2000
```

In this example, we generate the spectrum (M$^{-1}$) between
50000 and 55000 cm$^{-1}$ (-x050000 -x155000), using 10000 points
(-n10000) and including a broadened normalized Gaussian function with a
full width at half maximum of 2000cm$^{-1}$ (-w2000).

Multiple MCD calculations can be performed in one run by setting multiple
values for B. Transition moments can be also obtained through ED velocity 
formulation and FFMIO operator by setting the keywords `DoDipoleVelocity`
and `DoFullSemiClassical` to true, respectively:

```orca
------------------------------------------------------------------------------
           MCD Transitions via transition electric dipole moments
                B =  50000.00 Gauss  T =   300.000 K
------------------------------------------------------------------------------

                   dfosc             fosc           dfosc/fosc

 0 -> 1       -0.0000000000       0.0000000003      -0.0663180503
 0 -> 2        0.0000000000       0.0000000005       0.0000209714
 0 -> 3        0.0000000000       0.0000000003       0.0661609417
 0 -> 4       -0.0000000001       0.0000000004      -0.2991916107
 0 -> 5       -0.0000000000       0.0000000006      -0.0009270335
 0 -> 6        0.0000000001       0.0000000004       0.2984154405
 0 -> 7        0.0000000003       0.0000000008       0.3721777693
 0 -> 8       -0.0000000000       0.0000000009      -0.0002960328
 0 -> 9       -0.0000000003       0.0000000008      -0.3689867758
 0 ->10       -0.0000050986       0.1741092913      -0.0000292840
```

The results are printed separately in the output file for each setting: 

```orca
------------------------------------------------------------------------------
           MCD Transitions via transition electric dipole moments
                B =  50000.00 Gauss  T =   300.000 K
------------------------------------------------------------------------------

                   dfosc              fosc            dfosc/fosc

 0 -> 1       -0.0000000000       0.0000000003      -0.0663180503
 .
 .
 .
 ------------------------------------------------------------------------------
           MCD Transitions via transition velocity dipole moments
                B =  50000.00 Gauss  T =   300.000 K
------------------------------------------------------------------------------

                   dfosc              fosc            dfosc/fosc

 0 -> 1       -0.0000000001       0.0000000013      -0.0477214281
.
.
.

------------------------------------------------------------------------------
           MCD Transitions via full Semi-classical formulation
                B =  50000.00 Gauss  T =   300.000 K
------------------------------------------------------------------------------

                   dfosc              fosc            dfosc/fosc

 0 -> 1       -0.0000000001       0.0000000016      -0.0731029604
.
.
.
```

Post-processing results are saved in the files having the `.cis-el.dipole-length.1.mcd`, 
`.cis-el.dipole-vel.1.mcd`, and `.cis-el.exact.1.mcd` extensions.

$\textbf{NOTE:}$ It is worth enphasizing that the computed values of $\Delta$f$_{osc}$
correspond to the difference in absorption between left and right
circularly polarized light for the selected transition moments. In the
case of both ED approximations, $\Delta$f$_{osc}$ corresponds to the MCD
signal. The sum of natural circular dichroism and magnetic-induced circular
dichroism is obtained when the FFMIO is requested. To obtain only the 
MCD spectrum in an FFMIO scheme, it is necessary to subtract the natural
circular dichroism by setting B to 0.0.

<a id="sec:spectroscopyproperties.mcd.modules"></a>
## Running MCD calculations in other modules

The MCD implementation can also be used in other modules such as 
STEOM-CCSD, CAS, ROCIS, and MRCI (see the input file examples given
below) by using the same keywords as those described for the TDDFT module. 

```orca
%mrci
     DoDipoleLength true
     DoDipoleVelocity true
     DoFullSemiClassical true
     Soc
          DoSoc true
          DoMCD true
          B 50000.0
     end
end
```

```orca
%casscf
     DoDipoleLength true
     DoDipoleVelocity true
     DoFullSemiClassical true
     rel 
          DoSoc true
          DoMCD true
          B 50000.0
     end
end
```

```orca
%rocis
  DoDipoleLength true
  DoDipoleVelocity true
  DoFullSemiClassical true
  rel
   DoSOC true
   DoMCD true
   B 50000.0
  end
end
```

```orca
%mdci
     DoSOC true
     DoMCD true
     DoDipoleLength true
     DoDipoleVelocity true
     B 50000.0
end
```

It is important to keep in mind that the calculation of the MCD relies
on the proper description of the transition moments and angular momentum
for calculating the Zeeman perturbation. Therefore, the user is
responsible for selecting the proper electronic structure method.

<a id="sec:spectroscopyproperties.mcd.keywordlist"></a>
## List of related keywords

```orca
%selected module
  DoMCD false         # Enables the use of the MCD module
  DoDipoleVelocity true # Use the electric dipolar velocity formulation 
                        # for the light-matter interaction
  DoFullSemiClassical false  # Use the full semiclasical ligth-matter
                             # interaction transition moments
  MCDGridtype 1      # Grid for the molecular orientational average
                            # 1 = Lebedev grid (default)
                            # 2 = Regular grid
  MCDLebedev 14    # Number of points if Lebedev grid is selected
                   # 6, 12, 14(default), 26, 50, 110, 194, 302, 434, 590, 770
  NPOINTSPHI 10    # Number of points for phi angle if regular grid is selected
  NPOINTSTHETA 10  # Number of points for theta angle if regular grid is selected
  B 3000.0          # Magnetic field in Gauss
  Temperature 300.0 # Self-explanatory. One temperature must be defined 
                    # for each B value 
end
```
