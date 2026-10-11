```{index} Relaxation, Magnetic Relaxation
```

(sec:spectroscopyproperties.magrelax)=
# Magnetic Relaxation

(sec:spectroscopyproperties.magrelax.general)=
## General description of the program.

For magnetic molecules, ORCA now offers the possibility of computing the magnetic relaxation times. This is done using the Orca_Magrelax module.
In general, for a system with electronic and vibrational degrees of freedom, the Hamiltonian can be written as {cite}`lunghi2017intra,atanasov2015smm`:

$$
\begin{split}\hat{H} &= \hat{H}_{spin} + \hat{H}_{ph} + \hat{H}_{sph} \\\hat{H}_{sph} &= \sum_{\alpha} \frac{\partial \hat{H}_{spin}}{\partial Q_{\alpha}} \hat{Q}_{\alpha}+ \frac{1}{2}\sum_{\alpha \beta} \left( \frac{\partial^2 \hat{H}_{spin}}{\partial Q_{\alpha} \partial Q_{\beta}} \right) \hat{Q}_{\alpha} \hat{Q}_{\beta} + \dots \\
&=\sum_{\alpha} \hat{V}_\alpha \hat{Q}_{\alpha}+ \frac{1}{2}\sum_{\alpha \beta} \hat{V}_{\alpha,\beta} \hat{Q}_{\alpha} \hat{Q}_{\beta} + \dots \\\hat{H}_{ph} &= \sum_{\alpha} \hbar \omega_{\alpha} \left( \hat{n}_{\alpha} + \frac{1}{2} \right)
\end{split}
$$
Here $\hat{H}_{spin}$ is the electronic Hamiltonian and $\hat{H}_{ph}$ is the phononic (vibrational) Hamiltonian. These first two terms constitute the Born-Oppenheimer approach and if this all that the hamiltonian contained then the total wavefunction would just be the product of the electronic and phononic wavefunctions. The $\hat{H}_{sph}$ term is the term that introduces interaction between the electronic and phononic parts and makes the total wavefunction a linear combination of the aforementioned product states.

The phononic Hamiltonian can be approximated as a harmonic oscillator. The coupling $\hat{H}_{sph}$ is usually expressed as a Herzberg-Teller expansion of $\hat{H}_{spin}$.
The $\hat{H}_{spin}$ has been expressed in literature {cite}`reta2021ab,kragskow2023spin` as a parametric spin hamiltonian and more recently as a CASSCF Hamiltonian {cite}`mariano2025role`. In our present methodology, the QDPT Hamiltonian is used as $\hat{H}_{spin}$({ref}`sec:spectroscopyproperties.qdpt_magnetic_properties`). This allows for a parameter-free first-principles estimation of magnetic relaxation. The derivatives of the QDPT matrix are numerically computed.
We use the Fermi golden rule to compute the elements of the rate matrix.

$$
\begin{split}
P_{FI}=\frac{2\pi}{\hbar} \int|\langle F|\hat{H}_{pert}^{\mu}|I\rangle|^{2} \delta(E_F-E_I) \rho (E_F) dE_F
\end{split}
$$

Where the $\hat{H}_{pert}^{\mu}$ is the $\mu$-order perturbation theory expansion of the transition operator. It is described by the expression{cite}`timm2011time`:

$$
\begin{split}
\hat{H}_{pert}^{\mu}=\sum_{\mu=1}^{\infty}\hat{H}_{sph}(\frac{1}{E_I-H_0+i(0)^{+}}\hat{H}_{sph})^{(\mu-1)}
\end{split}
$$
Thus we see that our implmentation depends on the two infinite order expansions that must be truncted in a finite manner for practical considerations. The first is the Herzberg-Teller expansion and the second is the perturbation theory expression. 

(fig:relaxation mechanisms)=
```{figure} ../images/RelaxationPathwaysSVR.*

Mechanism of energy exchange between the electronic and phononic degrees of freedom.
```

If we truncate both of these at the first order, we recover expressions for the one-phonon process, also known as the Orbach Relaxation. If one of these expressions is truncated to the second order, we get a component of the two-phonon processes collectively known as the Raman processes. The second-order Herzberg-Teller gives the so-called Raman I component, and the second-order perturbation theory gives the Raman II component.

The Raman I process is rapid and oscillatory and is presently assumed to average out to zero in our implementation {cite}`lunghi2020limit`. This leaves the Orbach process, which dominates magnetic relaxation at higher temperatures, and the Raman Process, which dominates magnetic relaxation at lower temperatures.
The resulting rate equations for Orbach process are as follows {cite}`lunghi2019phonons`:

$$
\begin{split}
\Gamma_{FI}^{-}=\frac{\pi}{2\hbar} \sum_\alpha\int|V_{FI}^\alpha|^{2} \bar{n}(\hbar \omega)\delta(\Delta E_{FI}-\hbar\omega) \rho_{\alpha} (\hbar\omega) d\hbar\omega\\
\Gamma_{Fi}^{+}=\frac{\pi}{2\hbar} \sum_\alpha\int|V_{FI}^\alpha|^{2} (\bar{n}(\hbar \omega)+1)\delta(\Delta E_{FI}+\hbar\omega) \rho_{\alpha} (\hbar\omega) d\hbar\omega
\end{split}
$$

and the Raman rate equations become{cite}`lunghi2022toward`:

$$
\begin{split}
\Gamma_{FI}^{--}=\frac{\pi}{\hbar} \sum_{\alpha,\beta}\int\int|\sum_{C}\frac{V_{FC}^\alpha}{\Delta E_{CI}-\hbar\omega'}+\frac{V_{CI}^\alpha}{\Delta E_{CI}-\hbar\omega}|^{2} \\
\bar{n}(\hbar \omega)\bar{n}(\hbar \omega')\delta(\Delta E_{FI}-\hbar\omega-\hbar\omega') \rho_{\alpha} (\hbar\omega)\rho_{\beta} (\hbar\omega') d\hbar\omega d\hbar\omega'\\
\Gamma_{FI}^{++}=\frac{\pi}{\hbar} \sum_{\alpha,\beta}\int\int|\sum_{C}\frac{V_{FC}^\alpha}{\Delta E_{CI}+\hbar\omega'}+\frac{V_{CI}^\alpha}{\Delta E_{CI}+\hbar\omega}|^{2} \\
(\bar{n}(\hbar \omega)+1)(\bar{n}(\hbar \omega')+1)\delta(\Delta E_{FI}+\hbar\omega+\hbar\omega') \rho_{\alpha} (\hbar\omega)\rho_{\beta} (\hbar\omega') d\hbar\omega d\hbar\omega'\\
\Gamma_{FI}^{-+}=\frac{\pi}{\hbar} \sum_{\alpha,\beta}\int\int|\sum_{C}\frac{V_{FC}^\alpha}{\Delta E_{CI}-\hbar\omega'}+\frac{V_{CI}^\alpha}{\Delta E_{CI}+\hbar\omega}|^{2} \\
(\bar{n}(\hbar \omega)+1)\bar{n}(\hbar \omega')\delta(\Delta E_{FI}-\hbar\omega+\hbar\omega') \rho_{\alpha} (\hbar\omega)\rho_{\beta} (\hbar\omega') d\hbar\omega d\hbar\omega'\\
\Gamma_{FI}^{+-}=\frac{\pi}{\hbar} \sum_{\alpha,\beta}\int\int|\sum_{C}\frac{V_{FC}^\alpha}{\Delta E_{CI}+\hbar\omega'}+\frac{V_{CI}^\alpha}{\Delta E_{CI}-\hbar\omega}|^{2} \\
\bar{n}(\hbar \omega)(\bar{n}(\hbar \omega')+1)\delta(\Delta E_{FI}+\hbar\omega-\hbar\omega') \rho_{\alpha} (\hbar\omega)\rho_{\beta} (\hbar\omega') d\hbar\omega d\hbar\omega'
\end{split}
$$

Here, $V_{FI}^\alpha=\langle F|\hat{V}^\alpha|I\rangle$      is a matrix element of the linear spin-phonon coupling for the mode $\alpha$ on the electronic basis. The convention $\alpha\ge\beta$ for the phonon modes is a convenient choice. This convention introduces a factor of $(1-(\delta_{\alpha\beta}/2))$ inside the first summation.
The diagonal element of the rate matrix is determined by $\Gamma_{II}=\sum_{F\ne I}-\Gamma_{FI}$. This rate matrix can be diagonalised to give eigenvalues that are $-\tau^{-1}_k$ for each mode of relaxation $k$. The lowest eigenvalue corresponds to the system being in equilibrium. The second lowest value is the magnetic relaxation rate.

(sec:spectroscopyproperties.magrelax.example)=
## Computing magnetic relaxation times using Orca_Magrelax. 

Orca_Magrelax can be used either from an Orca input or as a standalone module. The following example shows how such a calculation can be run from the ORCA main program for a $[DyF_2]^{2+}$ toy system. 'dyf2casoptfreq' is a separately converged geometry optimisation + hessian calculation in ORCA, and 'dyf2cas' is a converged CASSCF calculation on the optimised geometry.
The use of magrelax inside orca requires the following additions to a typical CASSCF calculation. Inside the CASSCF block, 'projectHSOC' must be set to true, and the keyword 'projectedstates' must be set to the multiplicity of the lowest multiplet of the magnetic system. In the example, the lowest multiplet is $^6H_{15/2}$ state, which has a multiplicity of 16. The keyword 'domagrelax' must be set to true in the rel block of CASSCF. The '%qgprop' block tells the program to compute numerical derivatives for the QDPT matrix. Then the magrelax block itself provides additional details on the computation of the magnetic relaxation rates.

```orca
!DKH2 DKH-def2-TZVP AutoAux moread
%moinp "dyf2cas.gbw"  # converged CASSCF single point calculation
 
%rel                  # picture change effects for DKH2
 picturechange 2
end
 

%basis                # SARC2 basis for the Dy atom
NewGTO Dy "SARC2-DKH-QZV" end
NewAuxGTO Dy  "SARC/J" end
end

%casscf               #CASSCF settings
   nel 9            # number of electrons in valence                      
   norb 7           # number of orbitals in valence
   mult 6           # list of multiplicities to be considered
   nroots 21        # number of roots corresponding to each multiplicity
   trafostep RI     # Use RI
   maxiter 400      # maximum iterations for CASSCF
   projectHSOC true # project H_SOC = QDPT matrix to the lowest multiplet
   projectedstates 16 # number of states in the lowest multiplet
   rel
   dosoc true       # enables generation of QDPT matrix
   domagrelax true  # stores data from the QDPT driver needed for magrelax
   end
end

%qgprop #quantized geometry properties module (generates derivatives of H_SOC)
MODE DERIV           # compute derivatives
COORDSTYPE ENWNORMAL # displace energy weighted distance along normal modes
STEPSIZE 0.00005     #  base displacement
HESSIAN "dyf2casoptfreq.hess" # hessian file
DERHSOC true         # property for which derivatives are needed (H_SOC)
end
 
%magrelax #magrelax settings
magfld 0.0, 0.0,0.01  # magnetic field in x, y, z directions (in Tesla)
           # use if casscf and qgprop blocks are in a separate file:
           # inputfile "dyf2test_magrelax2_maxsoc" 
HESSIAN "dyf2casoptfreq.hess" # hessian file
temperature 2,150,1   # temperature range start, finish, step size (K)
degenThresh 0.1       # energy threshold for detecting degeneracy (in cm-1)
doRaman false         # orbach is always true raman can be selected
gridMax 8000          # upper limit of integration (Raman only)
gridMin 0             # lower limit of integration (Raman only)
nGrid 2000            # no of integration grid points of integration (Raman only)
keepData true         # keep coupling constants for future runs
end
 
*xyzfile 1 6 dyf2casoptfreq.xyz   #optimized geometry
```

Every time magrelax is run from Orca, it generates a magrelax input file which can be modified to run for different experimental conditions. It will read the files generated by the previous run. The file contains all the keywords that can be called from within ORCA, described with the comments next to each line. This file can be run from the command line as 'orca_magrelax dyf2.magrelaxinp' as long as the main orca program is in the path directory.

```orca
none #DMAGRELAXINP InputFile
dyf2casoptfreq.hess             #DMAGRELAXINP Hessfile
2.000000 150.000000 1.000000    #DMAGRELAXINP templist start, stop, stepsize
0.000000 0.00000000 0.010000    #DMAGRELAXINP magfld x, y, z
1 0 1 0                         #DMAGRELAXINP ratemodes, doRaman, keepData, debug
0.10                            #DMAGRELAXINP degenThresh
1000.00 0.00 1000               #DMAGRELAXINP gridmax, gridmin, ngrid
10.00                           #DMAGRELAXINP gamma
```

(sec:spectroscopyproperties.magrelax.modules)=
## Running Orca_Magrelax calculations in various modules

It is also possible to compute magnetic relaxation in other modules, which produce a QDPT matrix in ORCA, such as NEVPT2 or HQD-NEVPT2. These can be simply enabled in the CASSCF and they will be automatically used for the magrelax calculations.
For calculations that involve the %mrci block the magrelax keywords must not be put in the CASSCF block and instead included in the respective mrci input block. If calculation such as MREOM, MRCEPA or MRACPF that requires an mrci block is run then the magrelax related keywords would still go into the mrci block.
```{literalinclude} ../../orca_working_input/magrelaxDyF2_mrci.inp
:language: orca
```

(sec:spectroscopyproperties.magrelax.FAQ)=
## Fixing common issues
* Single point crashes: QGPROP will generate 2 geometries per vibrational mode. This can result in $(3N-6)\times 2$ geometries which have to be run in single point. These are named '\<Basename\>.geom-\<geometry index\>'. A user can rerun any geometry that didn't run with modified settings if needed.
* Modified settings don't show up in computation of linear spin phonon coupling constants: Each time QGPROP is run, it looks if the displaced geometries have converged from a previous run. If converged files are found, they are not recomputed to save on compute time. If the data of a previous run is not need by user 'keepData false' in the magrelax block will delete magrelax and qgprop related data after each run.
* Integration Grid: The Raman computation involves a numerical integration over phonon energies. The upper limit, lower limit and the number of grid points can be selected using the keywords 'gridMax', 'gridMin' and 'nGrid'.
* Differentiation grid: Since linear derivatives are calculated numerically, the step size given to qgprop can have influence the numerical stability of the results. Currently, the displacement of each vibrational mode is weighted by the reciprocal of energy. The 'Stepsize' keyword in qgprop can be used to scale a base displacement of 1 Angstrom.
* Magnetic Field misaligned: Current implmentation requires the user to input the magnetic field to be parallel with the axis of anisotropy. The ground KD g-tensor in CASSCF provides a rotation matrix that can be used to rotate from the molecular frame z-axis.
```{index} Magrelax Keywords
```

(sec:spectroscopyproperties.magrelax.keywords)=
## Magrelax Keywords


(tab:spectroscopyproperties.magrelax.method.keywords)=
:::{table} `%method` block input keywords relevant for Magrelax calculations
| Keyword            | Options       | Description                                      |
|:-------------------|:--------------|:-------------------------------------------------|
| `domagrelax`       | `true`        | Store data needed for magrelax                   |
| `projectHSOC`      | 'true'        | project QDPT ground multiplet (always true)      |
| `projectedstates`  | number        | multiplicity of ground multipler                 |
:::
(tab:spectroscopyproperties.magrelax.qgprop.keywords)=
:::{table} `%qgprop` block input keywords relevant for Magrelax calculations
| Keyword            | Options       | Description                                      |
|:-------------------|:--------------|:-------------------------------------------------|
| `MODE`             | `DERIV`       | Calculate derivatives                            |
| `COORDSTYPE`       | `ENWNORMAL`   | Use energy weighted displacements for normal modes|
| `STEPSIZE`         | number        | scaling of the unweighted step size              |
| `HESSIAN`          | name          | hessian file name                                |
| `DERHSOC`          | `true`        | Calculate derivatives of the QDPT hamiltonian with SOC|
:::
(tab:spectroscopyproperties.magrelax.magrelax.keywords)=
:::{table} `%magrelax` block input keywords relevant for Magrelax calculations
| Keyword            | Options       | Description                                      |
|:-------------------|:--------------|:-------------------------------------------------|
| `magfld`           | vector        | magnetic field (T)                               |
| `inputfile`        | name          | input file name (no file extension) for data if casscf and qgprop is skipped (optional)|
| `HESSIAN`          | name          | hessian file name                                |
| `temperature`      | start, end, step| temperature start,end, step size (K)           |
| `degenThresh`      | threshold     | threshold of degeneracy (states within this are ignored) (cm-1)|
| `doRaman`          | 'true'/'false'| include raman relaxation (orbach always on)      |
| `gridMax`          | number        | upper limit for numerical integration (raman only)|
| `gridMin`          | number        | lower limit for numerical integration (raman only)|
| `nGrid`            | number        | number of grid points for numerical integration (raman only)|
| `keepData`         | 'true'/'false'| keepData generated by magrelax for future run    |
:::


