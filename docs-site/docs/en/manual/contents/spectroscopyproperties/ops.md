

<a id="sec:spectroscopyproperties.ops"></a>
# One Photon Spectroscopy 

<a id="sec:spectroscopyproperties.ops.general"></a>
## General Description

Introduced in Orca 6.0, the One Photon Spectroscopy (OPS) tool takes charge of computing one-photon absorption (OPA), emission (OPE), and natural electric circular dichroism (ECD) intensities.
In each case, the intensity of the spectrum ($I(\omega)$) resulting from a transition between an initial state $I$ and a final state $J$ is determined by the square modulus of the transition moment $T_{IJ}=\langle \Psi_I | \hat{H}_1 | \Psi_J \rangle$, weighted by the populations $N_I$ and $N_J$ of states $I$ and $J$, respectively.

$$
I(\omega) = \alpha  \omega ^{-1} \sum_{IJ} (N_I - N_J) | \langle \Psi_I | \hat{H}_1 | \Psi_J \rangle |^2 \delta(E_{JI} \pm \hslash \omega )\qquad \text{(eqn:masterabs)}
$$

Where, $\alpha$ represents a positive constant, $\hslash \omega$ stands for photon energy, and the expression for $\hat{H}_1$ hinges on the specific modeling of photon-matter interaction.

## Light-matter interaction approaches

Expressions for $\hat{H}_1$ can be derived from different theoretical perspectives. For instructional purposes, a classical electrodynamic approach is adopted here. By representing light classically through a vector potential $\text{(}A\text{)}$ and a scalar potential $\text{(}\phi = 0\text{)}$, the radiation can be integrated into the Hamiltonian that models the molecular system.

$$
\begin{split}
     \hat{H} =& \sum_{i=1}^N \frac{1}{2m_e} \Big[\hat{p}_i - \frac{e}{c} A (r_i,t)\Big]^2 - \frac{ge}{2m_ec}\sum_{i=1}^{N}B(r_i,t) \cdot \hat{s}_i+ V(r_1,...,r_N)\\
\end{split}
$$

By disregarding the coupling between the magnetic field of light and the spin, as well as the $|A|^2$ term, and applying Fermi's golden rule, an expression for $\langle \Psi_I | \hat{H}_1 | \Psi_J \rangle$ under the Full-Semiclassical Light-Matter interaction can be derived.

<a id="eqn:TFFMIO"></a>

$$
\begin{split}
     T_{IJ}^{FFMIO} = \frac{e}{m_e} { \sum_{i=1}^N  \langle I|
     \mathcal{E} \cdot \Big[e^{ik\cdot r_i} \hat{p}_i \Big] |J\rangle}
\end{split}\qquad \text{(eqn:TFFMIO)}
$$

Where $T_{IJ}^{FFMIO}$ is the transition moment for the **F**ull (semiclassical) **F**ield-**M**atter **I**nteraction **O**perator (FFMIO), while $k$ and $\mathcal{E}$ denote the wave and polarization vectors describing the light, respectively. $r_i$ and $p_i$ represent the position and linear momentum operators for the i-th electron.

Proceeding from eq. [Eq](#eqn:TFFMIO) and approximating the exponential term of $T_{IJ}^{FFMIO}$ with a Taylor expansion yields various orders of interaction. The zeroth order ($T_{IJ}^{[0]}$) results in the electric dipolar velocity formulation $\text{(}ED\ vel\text{),}$ which, upon molecular orientational averaging, yields:

<a id="eqn:EDvelocity"></a>

$$
\epsilon_{ED\ vel} (\omega) =  \sum_{IJ} (N_I - N_J) \frac{2}{3 E_{JI}}  | \langle \Psi_I | \hat{p} | \Psi_J \rangle |^2 \delta(E_{JI} \pm \hslash \omega )\qquad \text{(eqn:EDvelocity)}
$$

For exact solutions of the Hamiltonian, or in theories that satisfy the Hypervirial theorem by construction, equation [Eq](#eqn:EDvelocity) can be transformed into a length formulation [Eq](#eqn:EDlength) $\text{(}ED\ len\text{)}$.

<a id="eqn:EDlength"></a>

$$
\epsilon_{ED\ len} (\omega) =  \sum_{IJ} (N_I - N_J) \frac{2 E_{JI} }{3} | \langle \Psi_I | \hat{\mu} | \Psi_J \rangle |^2 \delta(E_{JI} \pm \hslash \omega )\qquad \text{(eqn:EDlength)}
$$

The absorption spectrum under $ED\ len$ and $ED\ vel$ formulations can be obtained in all Orca modules utilizing OPS by setting `DoDipoleLength` and `DoDipoleVelocity` to true, respectively, in the corresponding module's block. The results are then presented in the following tables:

```
----------------------------------------------------------------------------------------------------
                     ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS
----------------------------------------------------------------------------------------------------
     Transition      Energy     Energy  Wavelength fosc(D2)      D2        DX        DY        DZ
                      (eV)      (cm-1)    (nm)                 (au**2)    (au)      (au)      (au)
----------------------------------------------------------------------------------------------------
  0-1Ag ->  1-1B3g  2.507275   20222.5   494.5   0.000000000   0.00000  -0.00000   0.00000   0.00000
  0-1Ag ->  2-1Au   2.726731   21992.6   454.7   0.000000000   0.00000  -0.00000   0.00000  -0.00000
  0-1Ag ->  3-1B2g  3.892633   31396.2   318.5   0.000000000   0.00000   0.00000   0.00000  -0.00000
  0-1Ag ->  4-1B3u  4.973431   40113.4   249.3   0.301976959   2.47833   1.57427  -0.00000  -0.00025
```

```
----------------------------------------------------------------------------------------------------
                     ABSORPTION SPECTRUM VIA TRANSITION VELOCITY DIPOLE MOMENTS
----------------------------------------------------------------------------------------------------
     Transition      Energy     Energy  Wavelength fosc(P2)      P2        PX        PY        PZ
                      (eV)      (cm-1)    (nm)                 (au**2)    (au)      (au)      (au)
----------------------------------------------------------------------------------------------------
  0-1Ag ->  1-1B3g  2.507275   20222.5   494.5   0.000000000   0.00000   0.00000   0.00000  -0.00000
  0-1Ag ->  2-1Au   2.726731   21992.6   454.7   0.000000000   0.00000   0.00000   0.00000  -0.00000
  0-1Ag ->  3-1B2g  3.892633   31396.2   318.5   0.000000001   0.00000  -0.00000  -0.00000  -0.00001
  0-1Ag ->  4-1B3u  4.973431   40113.4   249.3   0.292852326   0.08029  -0.28335   0.00000  -0.00002
```

Here, transitions are denoted using spectroscopic notation, such as 1-3B3g representing $1^3B_{3g}$.
If symmetry is not specified in the calculation (or is unavailable in the selected method), the system defaults to $C_1$ point group.
The **fosc(D2)** and **fosc(P2)** columns indicate the computed oscillator strengths in length and velocity formulations respectively.
Additionally, **D2**, **P2**, **DX**, **DY**, **DZ**, **PX**, **PY**, and **PZ** represent the square modulus of the electric transition dipole moment,
square modulus of the transition linear momentum, and its Cartesian components, respectively (with the imaginary unit in the linear momentum being implicit).

Alternatively, intensity computation directly using $T_{IJ}^{FFMIO}$ is achievable in OPS through the utilization of the keyword `DoFullSemiclassical` set to true. In this scenario, the orientational average is computed semi-numerically due to the absence of available analytical expressions.

```
-----------------------------------------------------------------------------
                     ABSORPTION SPECTRUM VIA FULL SEMI-CLASSICAL FORMULATION
-----------------------------------------------------------------------------
     Transition      Energy     Energy  Wavelength   fosc(FFMIO)
                      (eV)      (cm-1)    (nm)
-----------------------------------------------------------------------------
  0-1Ag ->  1-1B3g  2.507275   20222.5   494.5     0.00000049901134
  0-1Ag ->  2-1Au   2.726731   21992.6   454.7     0.00000000000260
  0-1Ag ->  3-1B2g  3.892633   31396.2   318.5     0.00000116403914
  0-1Ag ->  4-1B3u  4.973431   40113.4   249.3     0.29285049449335
```

Contributions to the intensity can also be decomposed beyond the dipole approximation; however, origin dependence must be treated carefully and typically requires expert-level understanding of the theory. The first-order term $\text{(}T_{IJ}^{[1]}\text{)}$ in the Taylor expansion of $T_{IJ}^{FFMIO}$ gives rise to the electric quadrupole velocity formulation and the magnetic dipole contributions.

$$
\langle \Psi_I |(T_{EQvel})_{\alpha \beta} | \Psi_J \rangle =  \frac{ie}{2 m_e} k_\alpha \epsilon_\beta \langle \Psi_I | r_\alpha p_\beta + p_\alpha r_\beta | \Psi_J \rangle\qquad \text{(eqn:Qvel)}
$$

$$
\langle \Psi_I |T_{MD} | \Psi_J \rangle =  \frac{ie}{2 m_e} \langle \Psi_I | (k \times \epsilon) (r \times p) | \Psi_J \rangle\qquad \text{(eqn:Mdip)}
$$

Under the same conditions applied to the electric dipole transition moment, the quadrupole contribution can be reformulated in terms of a length representation.

$$
\langle \Psi_I |(T_{EQlen})_{\alpha \beta} | \Psi_J \rangle =  \frac{e E_{JI}}{2 m_e} \sum_i k_\alpha \epsilon_\beta \langle \Psi_I | r_\alpha r_\beta | \Psi_J \rangle\qquad \text{(eqn:Qlengh)}
$$

By squaring the modulus of $\text{(}T_{IJ}^{[0]} + T_{IJ}^{[1]}\text{)}$, six terms emerge in the oscillation strength:
 the dipole square contribution as listed previously in the dipole-approximation tables, a magnetic dipole square, an electric quadrupole square, and three cross-product terms: electric dipole-electric quadrupole, electric dipole-magnetic dipole, and magnetic dipole-electric quadrupole.
 Enabling `DecomposeFosc` to true allows for the estimation of spectrum intensity by including all three squared terms in the calculation of the intensity.

```
--------------------------------------------------------------------------------------------------------------------------------
                     ABSORPTION SPECTRUM COMBINED ELECTRIC DIPOLE + MAGNETIC DIPOLE + ELECTRIC QUADRUPOLE SPECTRUM
--------------------------------------------------------------------------------------------------------------------------------
     Transition      Energy     Energy  Wavelength fosc(D2)  fosc(M2)  fosc(Q2)   fosc(D2+M2+Q2)     D2/TOT    M2/TOT    Q2/TOT
                      (eV)      (cm-1)    (nm)       (au)    (au*1e6)  (au*1e6)
--------------------------------------------------------------------------------------------------------------------------------
  0-1Ag ->  1-1B3g  2.507275   20222.5   494.5     0.00000   0.49891   0.00010   0.00000049901544   0.00000   0.99979   0.00021
  0-1Ag ->  2-1Au   2.726731   21992.6   454.7     0.00000   0.00000   0.00000   0.00000000000000   0.00000   0.00000   0.00000
  0-1Ag ->  3-1B2g  3.892633   31396.2   318.5     0.00000   1.12904   0.03298   0.00000116202090   0.00000   0.97162   0.02838
  0-1Ag ->  4-1B3u  4.973431   40113.4   249.3     0.30198   0.00000   0.00000   0.30197695902797   1.00000   0.00000   0.00000
```

```
--------------------------------------------------------------------------------------------------------------------------------
                     ABSORPTION SPECTRUM COMBINED ELECTRIC DIPOLE + MAGNETIC DIPOLE + ELECTRIC QUADRUPOLE SPECTRUM (Velocity)
--------------------------------------------------------------------------------------------------------------------------------
     Transition      Energy     Energy  Wavelength fosc(P2)  fosc(M2)  fosc(Q2)   fosc(P2+M2+Q2)     P2/TOT    M2/TOT    Q2/TOT
                      (eV)      (cm-1)    (nm)       (au)    (au*1e6)  (au*1e6)
--------------------------------------------------------------------------------------------------------------------------------
  0-1Ag ->  1-1B3g  2.507275   20222.5   494.5     0.00000   0.49891   0.00010   0.00000049901234   0.00000   0.99980   0.00020
  0-1Ag ->  2-1Au   2.726731   21992.6   454.7     0.00000   0.00000   0.00000   0.00000000000006   0.99964   0.00012   0.00024
  0-1Ag ->  3-1B2g  3.892633   31396.2   318.5     0.00000   1.12904   0.03441   0.00000116403924   0.00051   0.96993   0.02956
  0-1Ag ->  4-1B3u  4.973431   40113.4   249.3     0.29285   0.00000   0.00000   0.29285232633663   1.00000   0.00000   0.00000
```

Here, the columns **fosc(D2+M2+Q2)** and **fosc(P2+M2+Q2)** refer to the total oscillator strengths obtained in length and velocity formulations, respectively, while the columns **fosc(D2)** (or **fosc(P2)**), **fosc(M2)**, and **fosc(Q2)** refer to the individual contributions of each term.

In scenarios where the dipolar contribution to the intensity is non-zero, dividing the total intensity into **D2** (or **P2**), **M2**, and **Q2** contributions becomes challenging due to the dependence
 of **M2** and **Q2** terms on the chosen origin. To address this origin-dependence issue, OPS offers additional formulations to the multipolar expansion.
 One possible approach devised by our group describes each transition from an origin that minimizes the contributions of **M2** and **Q2**, thereby redistributing the intensity from these
 terms to all other components in the expansion of $e^{ik\cdot r_i}$. This refined formulation is readily accessible in an "origin-adjusted" table. [debeer2008tddft](../../bibliography.md), [debeer2008jpca](../../bibliography.md)

```
--------------------------------------------------------------------------------------------------------------------------------
                     ABSORPTION SPECTRUM COMBINED ELECTRIC DIPOLE + MAGNETIC DIPOLE + ELECTRIC QUADRUPOLE SPECTRUM (origin adjusted)
--------------------------------------------------------------------------------------------------------------------------------
     Transition      Energy     Energy  Wavelength fosc(D2)  fosc(M2)  fosc(Q2)   fosc(D2+M2+Q2)     D2/TOT    M2/TOT    Q2/TOT
                      (eV)      (cm-1)    (nm)       (au)    (au*1e6)  (au*1e6)
--------------------------------------------------------------------------------------------------------------------------------
  0-1Ag ->  1-1B3g  2.507275   20222.5   494.5     0.00000   0.49891   0.00010   0.00000049901544   0.00000   0.99979   0.00021
  0-1Ag ->  2-1Au   2.726731   21992.6   454.7     0.00000   0.00000   0.00000   0.00000000000000   0.00000   0.00000   0.00000
  0-1Ag ->  3-1B2g  3.892633   31396.2   318.5     0.00000   1.12904   0.03298   0.00000116202090   0.00000   0.97162   0.02838
  0-1Ag ->  4-1B3u  4.973431   40113.4   249.3     0.30198   0.00000   0.00000   0.30197695902797   1.00000   0.00000   0.00000
```

Alternatively, the intensity described through a truncated expansion of $e^{ik\cdot r_i}$ be achieved in an origin-independent manner. In this scenario, the cross-terms between the electric dipole moment and the electric octupole, as well as between the electric dipole moment and the magnetic quadrupole moments, arise from the second-order expansion $\text{(}T_{IJ}^{[2]}\text{)}$, resolving the origin dependence on the **D2**, **M2**, and **Q2** contributions. This formulation is provided in both length and velocity representations for the electric operators by setting the keyword `DecomposeFosc` to true, and the results are presented in the tables "Origin Independent, Length" and "Origin Independent, Velocity," respectively."

```
--------------------------------------------------------------------------------------------------------------------------------
                     ABSORPTION SPECTRUM COMBINED ELECTRIC DIPOLE + MAGNETIC DIPOLE + ELECTRIC QUADRUPOLE SPECTRUM (Origin Independent, Length)
--------------------------------------------------------------------------------------------------------------------------------
     Transition      Energy     Energy  Wavelength fosc(D2)  fosc(M2)  fosc(Q2) fosc(D2+M2+Q2+DM+DO) D2/TOT    M2/TOT    Q2/TOT
                      (eV)      (cm-1)    (nm)       (au)    (au*1e6)  (au*1e6)
--------------------------------------------------------------------------------------------------------------------------------
  0-1Ag ->  1-1B3g  2.507275   20222.5   494.5     0.00000   0.49891   0.00010   0.00000049901544   0.00000   0.99979   0.00021
  0-1Ag ->  2-1Au   2.726731   21992.6   454.7     0.00000   0.00000   0.00000   0.00000000000000   0.00000   0.00000   0.00000
  0-1Ag ->  3-1B2g  3.892633   31396.2   318.5     0.00000   1.12904   0.03298   0.00000116202090   0.00000   0.97162   0.02838
  0-1Ag ->  4-1B3u  4.973431   40113.4   249.3     0.30198   0.00000   0.00000   0.30197506344159   1.00001   0.00000   0.00000
```

```
---------------------------------------------------------------------------------------------------------------------------------
                     ABSORPTION SPECTRUM COMBINED ELECTRIC DIPOLE + MAGNETIC DIPOLE + ELECTRIC QUADRUPOLE SPECTRUM (Origin Independent, Velocity)
---------------------------------------------------------------------------------------------------------------------------------
     Transition      Energy     Energy  Wavelength fosc(P2)  fosc(M2)  fosc(Q2) fosc(P2+M2+Q2+PM+PO) P2/TOT    M2/TOT    Q2/TOT
                      (eV)      (cm-1)    (nm)       (au)    (au*1e6)  (au*1e6)
---------------------------------------------------------------------------------------------------------------------------------
  0-1Ag ->  1-1B3g  2.507275   20222.5   494.5     0.00000   0.49891   0.00010   0.00000049901234   0.00000   0.99980   0.00020
  0-1Ag ->  2-1Au   2.726731   21992.6   454.7     0.00000   0.00000   0.00000   0.00000000000006   0.99962   0.00012   0.00024
  0-1Ag ->  3-1B2g  3.892633   31396.2   318.5     0.00000   1.12904   0.03441   0.00000116403924   0.00051   0.96993   0.02956
  0-1Ag ->  4-1B3u  4.973431   40113.4   249.3     0.29285   0.00000   0.00000   0.29285049443551   1.00001   0.00000   0.00000
```

The tables presented in this section can be generated using the following input example:

```orca
----------------------------------------------------------------------------------------------------
                     ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS
----------------------------------------------------------------------------------------------------
     Transition      Energy     Energy  Wavelength fosc(D2)      D2        DX        DY        DZ
                      (eV)      (cm-1)    (nm)                 (au**2)    (au)      (au)      (au)
----------------------------------------------------------------------------------------------------
  0-1Ag ->  1-1B3g  2.507275   20222.5   494.5   0.000000000   0.00000  -0.00000   0.00000   0.00000
  0-1Ag ->  2-1Au   2.726731   21992.6   454.7   0.000000000   0.00000  -0.00000   0.00000  -0.00000
  0-1Ag ->  3-1B2g  3.892633   31396.2   318.5   0.000000000   0.00000   0.00000   0.00000  -0.00000
  0-1Ag ->  4-1B3u  4.973431   40113.4   249.3   0.301976959   2.47833   1.57427  -0.00000  -0.00025
```

## Natural electric circular dichroism 

In the case of ECD modeling, intensity is determined by computing the difference between two absorption spectra: one acquired using left-circularly polarized light and the other utilizing right-circularly polarized light.

$$
\Delta I(\omega) = I_{left} (\omega) - I_{rigth} (\omega)
$$

To initiate these calculations, the keyword `DoCD` should be set to true. There are three available implementations, which involve utilizing the length or velocity representations for the electric dipole moment, and also using the FFMIO, selected by including the keywords `DoDipoleLength`, `DoDipoleVelocity`, and `DoFullSemiclassical` respectively.

```
------------------------------------------------------------------------------------------
                     CD SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS
------------------------------------------------------------------------------------------
     Transition      Energy     Energy  Wavelength    R        MX        MY        MZ
                      (eV)      (cm-1)    (nm)   (1e40*cgs)   (au)      (au)      (au)
------------------------------------------------------------------------------------------
  0-1A  ->  1-1A    5.858500   47252.0   211.6   -9.15001  -0.01149   0.10351  -0.06803
  0-1A  ->  2-1A    6.859736   55327.5   180.7  -10.82714   0.13087   0.17869   0.25077
  0-1A  ->  3-1A    7.025193   56662.0   176.5   10.05878  -0.00526  -0.09041  -0.13618
  0-1A  ->  4-1A    7.837041   63210.0   158.2   33.15402   0.02541  -0.23067   0.15096
```

```
------------------------------------------------------------------------------------------
                     CD SPECTRUM VIA TRANSITION VELOCITY DIPOLE MOMENTS
------------------------------------------------------------------------------------------
     Transition      Energy     Energy  Wavelength    R        MX        MY        MZ
                      (eV)      (cm-1)    (nm)   (1e40*cgs)   (au)      (au)      (au)
------------------------------------------------------------------------------------------
  0-1A  ->  1-1A    5.858500   47252.0   211.6  -10.85364  -0.01149   0.10351  -0.06803
  0-1A  ->  2-1A    6.859736   55327.5   180.7  -15.54410   0.13087   0.17869   0.25077
  0-1A  ->  3-1A    7.025193   56662.0   176.5   12.44178  -0.00526  -0.09041  -0.13618
  0-1A  ->  4-1A    7.837041   63210.0   158.2   38.90662   0.02541  -0.23067   0.15096
```

```
--------------------------------------------------------------------
                     CD SPECTRUM VIA FULL SEMI-CLASSICAL FORMULATION
--------------------------------------------------------------------
     Transition      Energy     Energy  Wavelength    R
                      (eV)      (cm-1)    (nm)   (1e40*cgs)
--------------------------------------------------------------------
  0-1A  ->  1-1A    5.858500   47252.0   211.6   -10.85394
  0-1A  ->  2-1A    6.859736   55327.5   180.7   -15.54405
  0-1A  ->  3-1A    7.025193   56662.0   176.5    12.44211
  0-1A  ->  4-1A    7.837041   63210.0   158.2    38.90630
```

The following input example may be used to generate the CD tables presented in this section:

```orca
----------------------------------------------------------------------------------------------------
                     ABSORPTION SPECTRUM VIA TRANSITION VELOCITY DIPOLE MOMENTS
----------------------------------------------------------------------------------------------------
     Transition      Energy     Energy  Wavelength fosc(P2)      P2        PX        PY        PZ
                      (eV)      (cm-1)    (nm)                 (au**2)    (au)      (au)      (au)
----------------------------------------------------------------------------------------------------
  0-1Ag ->  1-1B3g  2.507275   20222.5   494.5   0.000000000   0.00000   0.00000   0.00000  -0.00000
  0-1Ag ->  2-1Au   2.726731   21992.6   454.7   0.000000000   0.00000   0.00000   0.00000  -0.00000
  0-1Ag ->  3-1B2g  3.892633   31396.2   318.5   0.000000001   0.00000  -0.00000  -0.00000  -0.00001
  0-1Ag ->  4-1B3u  4.973431   40113.4   249.3   0.292852326   0.08029  -0.28335   0.00000  -0.00002
```

## SOC and SSC corrected spectrum

All the OPS keywords and tables listed above are available for the cases in which spin-orbit coupling and spin-spin coupling effects are taken into account by a QDPT formulation
 (when the method is available in the selected ORCA module). In those cases, ORCA 6.0 does not provide symmetry after the relativistic correction; therefore, $C_1$ group symmetry transitions are reported.
 Additionally, the multiplicity of the relativistically corrected roots are not well defined anymore; therefore, the average value is reported.

For the last case example presented in this section, when `DoSOC` is set to true in the input, OPS reports:

```
--------------------------------------------------------------------------------------------------------
      SOC CORRECTED ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS
--------------------------------------------------------------------------------------------------------
      Transition         Energy     Energy  Wavelength fosc(D2)      D2       |DX|      |DY|      |DZ|
                          (eV)      (cm-1)    (nm)                 (au**2)    (au)      (au)      (au)
--------------------------------------------------------------------------------------------------------
  0-1.0A  ->  1-3.0A    4.620455   37266.5   268.3   0.000000105   0.00000   0.00079   0.00024   0.00049
  0-1.0A  ->  2-3.0A    4.620460   37266.5   268.3   0.000000009   0.00000   0.00003   0.00024   0.00016
  0-1.0A  ->  3-3.0A    4.620491   37266.8   268.3   0.000000126   0.00000   0.00093   0.00034   0.00035
  0-1.0A  ->  4-3.0A    5.626046   45377.1   220.4   0.000003140   0.00002   0.00043   0.00397   0.00261
  0-1.0A  ->  5-3.0A    5.626322   45379.4   220.4   0.000000070   0.00000   0.00056   0.00020   0.00040
  0-1.0A  ->  6-3.0A    5.626327   45379.4   220.4   0.000000003   0.00000   0.00002   0.00013   0.00009
  0-1.0A  ->  7-1.0A    5.858722   47253.8   211.6   0.003490904   0.02432   0.01409   0.12986   0.08520
  0-1.0A  ->  8-3.0A    6.537246   52726.4   189.7   0.000000006   0.00000   0.00017   0.00005   0.00008
  0-1.0A  ->  9-3.0A    6.537246   52726.5   189.7   0.000000225   0.00000   0.00011   0.00099   0.00065
  0-1.0A  -> 10-3.0A    6.537257   52726.5   189.7   0.000000032   0.00000   0.00004   0.00037   0.00025
  0-1.0A  -> 11-1.0A    6.859693   55327.2   180.7   0.002900797   0.01726   0.12934   0.02129   0.00891
  0-1.0A  -> 12-1.0A    7.025210   56662.1   176.5   0.011980549   0.06961   0.23240   0.08590   0.09066
  0-1.0A  -> 13-3.0A    7.448215   60073.9   166.5   0.000000040   0.00000   0.00018   0.00022   0.00037
  0-1.0A  -> 14-3.0A    7.448216   60073.9   166.5   0.000000003   0.00000   0.00002   0.00011   0.00006
  0-1.0A  -> 15-3.0A    7.448231   60074.0   166.5   0.000000533   0.00000   0.00116   0.00078   0.00098
  0-1.0A  -> 16-1.0A    7.837071   63210.2   158.2   0.012389093   0.06452   0.02426   0.21144   0.13867
```

In this case, due to the complex nature of the relativistically-corrected wave functions, dipole moments are not necessarily real values, and their modulus are reported in the "|DX|", "|DY|", and "|DZ|" columns. Real and imaginary components may be obtained in extended tables by increasing the selected print level. In this instance, selecting `Printlevel 4` in the %CIS block.

```
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      SOC CORRECTED ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS (- Extended -)
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      Transition         Energy     Energy  Wavelength     fosc(D2)          D2           DX(re)         DX(im)         DY(re)         DY(im)         DZ(re)         DZ(im)
                          (eV)      (cm-1)    (nm)                         (au**2)         (au)           (au)           (au)           (au)           (au)           (au)
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  0-1.0A  ->  1-3.0A    4.620455   37266.5   268.3         1.05e-07       9.31e-07       4.10e-04       6.80e-04      -1.22e-04      -2.02e-04      -2.55e-04      -4.24e-04
  0-1.0A  ->  2-3.0A    4.620460   37266.5   268.3         9.18e-09       8.11e-08      -2.25e-05       1.30e-05       2.05e-04      -1.18e-04      -1.35e-04       7.78e-05
  0-1.0A  ->  3-3.0A    4.620491   37266.8   268.3         1.26e-07       1.11e-06       4.17e-04      -8.35e-04       1.51e-04      -3.01e-04       1.58e-04      -3.17e-04
  0-1.0A  ->  4-3.0A    5.626046   45377.1   220.4         3.14e-06       2.28e-05      -4.31e-04       5.49e-07       3.97e-03      -5.06e-06      -2.61e-03       3.32e-06
  0-1.0A  ->  5-3.0A    5.626322   45379.4   220.4         7.04e-08       5.11e-07       1.13e-04       5.45e-04      -4.10e-05      -1.98e-04      -8.13e-05      -3.92e-04
  0-1.0A  ->  6-3.0A    5.626327   45379.4   220.4         3.42e-09       2.48e-08      -1.52e-05      -1.15e-07       1.31e-04       9.97e-07      -8.58e-05      -6.51e-07
  0-1.0A  ->  7-1.0A    5.858722   47253.8   211.6         3.49e-03       2.43e-02      -1.41e-02      -2.11e-05       1.30e-01       1.94e-04      -8.52e-02      -1.28e-04
  0-1.0A  ->  8-3.0A    6.537246   52726.4   189.7         6.35e-09       3.97e-08      -1.24e-04       1.22e-04       3.61e-05      -3.56e-05       5.89e-05      -5.80e-05
  0-1.0A  ->  9-3.0A    6.537246   52726.5   189.7         2.25e-07       1.40e-06       1.10e-04       1.07e-06      -9.87e-04      -9.61e-06       6.46e-04       6.29e-06
  0-1.0A  -> 10-3.0A    6.537257   52726.5   189.7         3.24e-08       2.02e-07      -4.25e-05      -5.39e-08       3.73e-04       4.74e-07      -2.47e-04      -3.13e-07
  0-1.0A  -> 11-1.0A    6.859693   55327.2   180.7         2.90e-03       1.73e-02       4.49e-02       1.21e-01       7.39e-03       2.00e-02       3.09e-03       8.35e-03
  0-1.0A  -> 12-1.0A    7.025210   56662.1   176.5         1.20e-02       6.96e-02      -2.18e-01       8.17e-02      -8.04e-02       3.02e-02      -8.49e-02       3.19e-02
  0-1.0A  -> 13-3.0A    7.448215   60073.9   166.5         3.95e-08       2.17e-07       6.65e-05      -1.67e-04      -8.19e-05       2.05e-04      -1.37e-04       3.42e-04
  0-1.0A  -> 14-3.0A    7.448216   60073.9   166.5         2.93e-09       1.61e-08      -2.09e-05       6.86e-07       1.12e-04      -3.68e-06      -5.57e-05       1.83e-06
  0-1.0A  -> 15-3.0A    7.448231   60074.0   166.5         5.33e-07       2.92e-06      -6.54e-04      -9.63e-04      -4.40e-04      -6.48e-04      -5.48e-04      -8.07e-04
  0-1.0A  -> 16-1.0A    7.837071   63210.2   158.2         1.24e-02       6.45e-02      -2.40e-02       3.67e-03       2.09e-01      -3.20e-02      -1.37e-01       2.10e-02
```

## OPS full list of keywords

The folowing list of keywords may be included directly in the correcponding module block to trigger OPS compute the corresponding intensities.

```
DoCD                 # request circular dichroism calculation
DoDipoleLength       # request the use of electric moments in a 
                     # length formulation
DoDipoleVelocity     # request the use of electric moments in a 
                     # velocity formulation
DoFullSemiclassical  # request the calculation of complete 
                     # semiclassical multipolar moments
DecomposeFosc        # request the decomposition of the oscillator 
                     # strengths in a multipolar expansion
```

In Orca 6.1, the modules in which OPS is available are: `%cis`, `%tddft`, `%rocis`, `%casscf`, `%mrci`, `%mdci`, `%lft`, `%mcrpa`, `%rasci` and `%xes`.

## Notes

1. All values in the OPS tables are expressed in atomic units (au) unless otherwise specified.
2. Keyword corrections are done internally when necessary.
3. **IMPORTANT**: Input keywords have been standardized across all OPS-utilizing modules; Orca 5.x are no longer valid.
4. **IMPORTANT**: In CASSCF and MRCI, keywords controlling the absorption and ECD spectrum no longer belong in the `%rel` block.
5. Origin-adjusted formulation is approximated in SOC/SSC formulations.
6. OPS is not available for sTDDFT and sTDADFT.
7. The MDCI module reports spectra using left, right, and both solutions.
8. ADC2 and EOM-CCSD methods exclusively utilize ED length tables.
9. Starting in ORCA 6.1, the keywords `DoHigherMoments`, `DecomposeFoscLength` and `DecomposeFoscVelocity` have been consolidated into a single, simplified keyword: `DecomposeFosc`.
