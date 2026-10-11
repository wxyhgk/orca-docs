```{index} EPR
```

(sec:spectroscopyproperties.epr)=
# Electron Paramagnetic Resonance (EPR) Parameters

Electron paramagnetic resonance probes the magnetic sublevels of the
electronic ground state. In the `%eprnmr` input block, calculations of
the parameters of a spin Hamiltonian of the form

$$H_S = \beta_e \mathbf{B}\mathbf{g}\mathbf{S} + \sum_N\mathbf{S}\mathbf{A}_N\mathbf{I}_N
      + \mathbf{S}\mathbf{D}\mathbf{S}
$$ (eq:epr_SH)

can be requested. The properties are evaluated *via* analytical derivative/response
theory methods. For the analytic response approach based on CC, please see
{ref}`sec:modelchemistries.autoci.autociresp`. For evaluation of spin Hamiltonian parameters using quasi-degenerate
perturbation theory, you may be interested in {ref}`sec:spectroscopyproperties.qdpt_magnetic_properties`
A complete list of possible keywords for the eprnmr module can be
found in {ref}`sec:spectroscopyproperties.properties.eprnmr`.
The cartesian index convention for EPR can be found in {ref}`sec:spectroscopyproperties.properties.eprnmrConv`.

(sec:spectroscopyproperties.epr.g)=
## The g-Tensor
```{index} G-Tensor
```

The g-tensor determines the position of the signal in an EPR spectrum.
It can be calculated as a second derivative of the energy and it is
implemented as such in ORCA for the SCF methods (HF and DFT),
CASSCF, as well as all-electron MP2 (or RI-MP2) and double-hybrid DFT,
plus Coupled Cluster (CCSD and CCSD(T)).

### Theory

The g-tensor has four contributions which may be evaluated in ORCA,

$$
\mathbf{g} = g_e\mathbf{1} + \mathbf{g}^{\text{RMC} }
              +\mathbf{g}^{\text{DSO} } + \mathbf{g}^{\text{PSO}}.
$$ (eq:g_contrib)

These contributions are:

- The **spin Zeeman** contribution, which is isotropic and characterized
by a simple constant, the free-electron g-value $g_{e} = 2.002319\dots$

  $$
  g_{\mu \nu }^{{ \text{SZ} } } =\delta_{\mu \nu } g_{e}
  $$ (eqn:249)

  meaning that it doesn't require any computation. The remaining terms
  contribute to the deviation from the free-electron value, which is
  sometimes called the g-shift.

- The first-order **relativistic mass correction**, which is a usually
  rather small scalar-relativistic correction and can be evaluated as
  an expectation value over the spin density

  $$\mathbf{g}^{ \text{RMC} } =-\frac{\alpha^{2} g_e}{2S}\sum\limits_{k,l}
  {P_{kl}^{\alpha -\beta } \left\langle { \phi_{k} \left|{ \hat{{T} }}
  \right|\phi_{l} } \right\rangle}.
  $$ (eqn:250)

- The **diamagnetic spin-orbit** (also called gauge correction) term,
  another first-order correction which is often small

  $$g_{\mu \nu }^{ \text{DSO} } =\frac{\alpha^2 g_e}{4S}\sum\limits_{k,l}
  {P_{kl}^{\alpha -\beta } \left\langle { \phi_{k} \left|{ \sum\limits_A { \xi
  \left({ r_{A} } \right)\left[{ \mathrm{\mathbf{r} }_{A} \mathrm{\mathbf{r} }_{O} -\mathrm{\mathbf{r} }_{A,\mu } \mathrm{\mathbf{r} }_{O,\nu } } \right]} } \right|\phi_{l} }
  \right\rangle}.
  $$ (eqn:251)

- The second-order **orbital Zeeman/SOC** contribution, usually the main source
  of deviation from the free-electron g-value in a molecule,

  $$g_{\mu \nu }^{ \text{PSO} } = - \frac{g_e}{2S}\sum\limits_{k,l} { \frac{\partial
  P_{kl}^{\alpha -\beta } }{\partial B_{\mu } }\left\langle { \phi_{k} \left|{h_{\nu }^{\text{SOC} } } \right|\phi_{l} } \right\rangle}.
  $$ (eqn:252)
  
  Its calculation requires the solution of response equations to obtain the perturbed 
  spin density, this is done for the magnetic field perturbation in ORCA. Precise details
  depend on the level of theory. At the SCF level, it is achieved by solving
  coupled-perturbed SCF equations (see {ref}`sec:essentialelements.cpscf`). At the
  CASSCF level, the CP-CASSCF equations are solved ({ref}`sec:spectroscopyproperties.casscfresp`).

In these equations, $S$ is the total spin, $\alpha$ the
fine structure constant, $P^{\alpha -\beta }$ is the spin density
matrix, $\phi$ is the basis set, $\hat{T}$ is the kinetic energy
operator, $\xi \left({ r_{A} } \right)$ an approximate radial operator,
$h^{\text{SOC} }$ the spatial part of an effective one-electron
spin-orbit operator and $B_{\mu }$ is a component of the magnetic field.

### Basic usage

As an example, consider the following simple g-tensor job:

```{literalinclude} ../../orca_working_input/C05S13_228.inp
:language: orca
```

The simplest way is to call the g-tensor property in the simple input
line as shown above. It can also be specified in the `%eprnmr` block
with `gtensor true`. `SOMF(1X) ` defines the chosen spin-orbit coupling
(SOC) operator.

The output looks like the following. It contains information on the
contributions to the g-tensor (relativistic mass correction, diamagnetic
spin-orbit term (= gauge-correction), paramagnetic spin-orbit term (=
OZ/SOC)), the isotropic g-value and the orientation of the total tensor.

```orca
-------------------
ELECTRONIC G-MATRIX
-------------------

The g-matrix:
              2.0104321   -0.0031354   -0.0000000
             -0.0031354    2.0081968   -0.0000000
             -0.0000000   -0.0000000    2.0021275

Breakdown of the contributions
 gel          2.0023193    2.0023193    2.0023193
 gRMC        -0.0003174   -0.0003174   -0.0003174
 gDSO(tot)    0.0000808    0.0001539    0.0001515
 gPSO(tot)    0.0000449    0.0038301    0.0104898
             ----------   ----------   ----------
 g(tot)       2.0021275    2.0059858    2.0126431 iso=  2.0069188
 Delta-g     -0.0001917    0.0036665    0.0103238 iso=  0.0045995

 Orientation:
  X           0.0000000    0.5762906   -0.8172448
  Y           0.0000000    0.8172448    0.5762906
  Z           1.0000000   -0.0000000    0.0000000
```

g-tensor calculations at the SCF level are not highly demanding in terms
of basis set size. Basis sets that give reliable SCF
results (at least valence double-zeta plus polarization) usually also
give reliable g-tensor results. For many molecules the Hartree-Fock
approximation will give reasonable predictions. In a number of cases,
however, it breaks down completely. DFT is more robust and the number of
molecules where it fails is much smaller. Among the
density functionals, the hybrid functionals seem to be the most
accurate.

:::{note}
There are different options for treatment of the spin-orbit coupling
operator available in the program. The defaults should be quite reliable.
Check out {ref}`sec:spectroscopyproperties.soc` for more information.
:::

(sec:spectroscopyproperties.epr.gaugeorigin)=
### Gauge origin treatment

The g-tensor is not gauge-independent. Without
taking special precautions, the results will have an unphysical dependence
on where the gauge origin is placed with respect to the molecule.
Unless a fully invariant procedure (such as GIAOs) is used, this
undesirable aspect is always present in the calculations.

Starting from ORCA 5.0, the default treatment for g-tensor calculations
gauge is the **GIAO** approach (GIAO stands for "gauge including atomic orbitals").
GIAOs are available at the SCF level, RI-MP2 as well as Coupled Cluster up to CCSD(T) level. GIAOs are ***not*** currently available with CASSCF linear response
and a common gauge origin must be provided in the `%eprnmr` block.

| Method for EPR g-Tensor                                |GIAO   |CGO    |
|--------------------------------------------------------|-------|-------|
| [SCF](sec:essentialelements.cpscf)                     |&check;|&check;|
| [RI-MP2](sec:modelchemistries.mp2.2ndder)              |&check;|&check;|
| [CASSCF](sec:spectroscopyproperties.casscfresp)        |       |&check;|
| [CCSD, CCSD(T)](sec:modelchemistries.autoci.autociresp)|&check;|       |

The GIAO one-electron integrals are done analytically by
default whereas the treatment of the GIAO two-electron integrals is
chosen to be same as for the SCF. The available options which can be set
with `giao_1el / giao_2el` in the `%eprnmr` block can be found in
section {ref}`sec:spectroscopyproperties.properties.eprnmr`.
Concerning the computational time, for small systems, e.g. phenyl
radical (41 electrons), the `rijk`-approximation is good to use for the
SCF-procedures as well as the GIAO two-electron integrals. Going to
larger systems, e.g. chlorophyll radical (473 electrons), the
`rijcosx`-approximation reduces the computational time enormously. While
the new default grid settings in ORCA 5.0 (`defgrid2`) should be
sufficient in most cases, certain cases might need the use of
`defgrid3`. Note that for the current implementation of CC-NMR/EPR, both 
`giao_1el` and `giao_2el` need to be evaluated fully analytically, which is also
the default when CC-NMR/EPR is requested.

If the choice of the gauge origin is not outrageously poor, a **common gauge
origin** often gives reasonable results for g-tensors (much more reasonable than
in NMR, where it shouldn't be used). This is especially true with a large basis set.
The origin may be modified with the keyword `ori` inside the `%eprnmr` input block.
If you are using a common gauge origin, it is wise to check the sensitivity of the
results with respect to origin location, especially when small
g-shifts on the order of only a few hundred ppm are calculated.

### Keywords
```{index} G-Tensor Keywords
```

:::{raw} latex
\begingroup
\footnotesize
:::

:::{tabularcolumns} \Y{0.3}\Y{0.3}\Y{0.4}
:::
(tab:spectroscopyproperties.epr.g.keywords.block)=
:::{flat-table} `%eprnmr` block input keywords relevant for g-tensor calculations. For more GIAO-related options, see {ref}`sec:spectroscopyproperties.properties.eprnmr`
:header-rows: 1
:class: longtable
:class: footnotesize
* - Keyword
  - Options
  - Description
* - `gtensor`
  - `true/false`
  - Calculate the g-tensor
* - `gtensor_1el2el`
  - `true/false`
  - Print the 1- and 2-electron contributions to the g-tensor
* - `ori`
  - `GIAO`
  - Use the GIAO formalism (default)
* - 
  - `CenterOfElCharge`
  - Common gauge origin at center of electronic charge
* - 
  - `CenterOfNucCharge`
  - Common gauge origin at center of nuclear charge
* - 
  - `CenterOfSpinDens`
  - Common gauge origin at center of spin density
* - 
  - `CenterOfMass`
  - Common gauge origin at center of mass
* - 
  - `N`
  - Common gauge origin at atom `N`
* - 
  - `x, y, z`
  - Common gauge origin at position `x, y, z` (in coordinate input units, default Angstrom)
* - `do_giao_soc2el`
  - `true/false`
  - Whether to include the 2-electron contribution to the GIAO term from the SOMF operator (usually small but expensive, disabled by default)
:::

:::{raw} latex
\endgroup
:::

(sec:spectroscopyproperties.epr.hyperfine)=
## Hyperfine Coupling
```{index} Hyperfine Coupling
```


Hyperfine couplings characterize the interaction between the electronic spin
and the spin of a nucleus in the molecule. In typical EPR spectra, they lead
to a splitting of the signal.

(sec:spectroscopyproperties.epr.hyperfine.contrib)=
### Theory
The hyperfine coupling has four contributions which may be evaluated in ORCA,

$$
\mathbf{A}_N = a_{iso}\mathbf{1} + \mathbf{A}^{\text{dip} }
              +\mathbf{A}^{\text{orb} } + \mathbf{A}^{\text{GC}}.
$$ (eq:A_contrib)

These contributions are:

- The isotropic **Fermi contact** term that arises from finite spin
density on the nucleus under investigation. It is calculated for nucleus
$N$ from:

  $$a_{\text{iso} } \left( N \right)=\left( \frac{4}{3}\pi
  \left\langle { S_{z} } \right\rangle^{-1} \right)g_{e} g_{N} \beta_{e}
  \beta_{N} \rho \left({ \vec{{R} }_{N} } \right)$$ (eqn:244)

  Here, $\left\langle { S_{z} } \right\rangle$ is the expectation value of
  the z-component of the total spin, $g_{e}$ and $g_{N}$ are the electron
  and nuclear g-factors and $\beta_{e}$ and $\beta_{N}$ are the electron
  and nuclear magnetons respectively.
  $\rho \left({ \vec{{R} }_{N} } \right)$ is the spin density at the
  nucleus. The proportionality factor $P_{N} = \alpha^2 g_{e}
  g_{N} \beta_{e} \beta_{N}$ is commonly used and has the dimensions MHz
  bohr$^{3}$ in ORCA.

- The **spin dipole** term that arises from the through-space dipole-dipole
interaction of the magnetic nucleus with the magnetic moment of the
electron. It is also calculated as an expectation value over the spin
density as:

  $$A_{\mu \nu}^{\text{dip} } \left( N \right) =
  P_N \sum\limits_{kl} \rho_{kl}
  \left\langle\phi_k \left| r_N^{-5} \left(3\vec{r}_{N \mu}\vec{r}_{N \nu}
  -\delta_{\mu \nu}r_N^2 \right)\right|\phi_l \right\rangle
  $$ (eqn:245)

  where $\mathrm{\mathbf{\rho } }$ is the spin-density matrix and
  $\vec{{r} }_{N}$ is a vector of magnitude $r_{N}$ that points from the
  nucleus in question to the electron ($\left\{\phi \right\}$ is the set
  of basis functions).

- The second-order **spin-orbit** contribution, which arises as a cross-term
between the spin-orbit and nucleus-orbit coupling operators. It requires the solution
of coupled-perturbed SCF equations and is consequently more computationally
demanding. The contribution can be written as:

  $$A_{\mu \nu }^{\text{orb} } \left( N \right)=-\frac{1}{2S}P_{N} \sum\limits_{kl}
  {\frac{\partial \rho_{kl} }{\partial I_{\nu } }\left\langle { \phi_{k}
  \left|{ h_{\mu }^{\text{SOC} } } \right|\phi_{l} } \right\rangle}
  $$ (eqn:246)

  The derivative of the spin density is computed by solving the
  coupled-perturbed SCF equations with respect to the nucleus-orbit
  coupling perturbation, which is represented by the operator

  $$h_{\nu }^{\text{NOC} } \left( N \right)=\sum\limits_i { r_{iA}^{-3} l_{i,\nu
  }^{\left( N \right)} }
  $$ (eqn:247)

  where the sum is over electrons and $N$ is the nucleus in question.

- The **gauge-correction** contribution (sometimes also called diamagnetic).
This term is often small. However, it is needed in order to get exactly gauge-invariant
results. We recently showed that the gauge correction can become crucial
in the long-distance limit between the nuclear spin and the electron
spin. This is relevant for pseudocontact NMR chemical shifts (PCS).{cite}`LangPCS`

:::{note}
Second-order HFCs can be quite significant for heavier nuclei and are certainly good
to include for transition metal complexes. Available treatments of the
spin-orbit coupling operator are described under {ref}`sec:spectroscopyproperties.soc`.
:::

### Basic usage
Hyperfine and quadrupole couplings can be requested in the `%eprnmr` input block.
Since there may be several nuclei that you are interested in, the input is
relatively sophisticated.

An example how to calculate the hyperfine and field gradient tensors for
the CN radical is given below:

```{literalinclude} ../../orca_working_input/C05S13_226.inp
:language: orca
```

In this example, the hyperfine tensor is calculated for all carbon atoms
and atom 2, which is nitrogen in this case. (Additionally, the electric field
gradient is calculated for nitrogen.)

:::{Note}
-   Counting of atom numbers starts from 1.

-   Beware - all nuclei mentioned in one line will be assigned the same isotopic
    mass! If several different nuclei are desired (such as C and H), there has
    to be a new line for each of them.

-   You have to specify the `Nuclei` statement *after* the definition of
    the atomic coordinates or the program will not figure out what is
    meant by "`all`".
:::

The output looks like the following. It contains detailed
information about the individual contributions to the hyperfine
couplings, its orientation, its eigenvalues, the isotropic part and (if
requested) also the quadrupole coupling tensor.

```orca
-----------------------------------------
ELECTRIC AND MAGNETIC HYPERFINE STRUCTURE
-----------------------------------------

 -----------------------------------------------------------
 Nucleus   0C : A:ISTP=   13 I=  0.5 P=134.1903 MHz.au**3
                Q:ISTP=   13 I=  0.5 Q=  0.0000 barn
 -----------------------------------------------------------
 Raw HFC matrix (all values in MHz):
 -----------------------------------
               695.8952           0.0000          -0.0000
                 0.0000         543.0617          -0.0000
                -0.0000          -0.0000         543.0617

 A(FC)         594.0062         594.0062         594.0062
 A(SD)         -50.9445         -50.9445         101.8890
             ----------       ----------       ----------
 A(Tot)        543.0617         543.0617         695.8952  A(iso)=594.0062
 Orientation:
  X           0.0000000        0.0000000       -1.0000000
  Y          -0.8111216       -0.5848776       -0.0000000
  Z          -0.5848776        0.8111216        0.0000000

Notes:  (1) The A matrix conforms to the "SAI" spin Hamiltonian convention.
        (2) Tensor is right-handed.

 -----------------------------------------------------------
 Nucleus   1N : A:ISTP=   14 I=  1.0 P= 38.5677 MHz.au**3
                Q:ISTP=   14 I=  1.0 Q=  0.0204 barn
 -----------------------------------------------------------
 Raw HFC matrix (all values in MHz):
 -----------------------------------
                13.2095         -0.0000          0.0000
                -0.0000        -45.6036         -0.0000
                 0.0000         -0.0000        -45.6036

 A(FC)         -25.9993        -25.9993        -25.9993
 A(SD)          39.2088        -19.6044        -19.6044
             ----------      ----------      ----------
 A(Tot)         13.2095        -45.6036        -45.6036  A(iso)=-25.9993
 Orientation:
  X           1.0000000       0.0000000      -0.0000000
  Y          -0.0000000       0.9996462       0.0265986
  Z           0.0000000      -0.0265986       0.9996462

Notes:  (1) The A matrix conforms to the "SAI" spin Hamiltonian convention.
        (2) Tensor is right-handed.

 Raw EFG matrix (all values in a.u.**-3):
 -----------------------------------
            -0.1832      -0.0000       0.0000
            -0.0000       0.0916       0.0000
             0.0000       0.0000       0.0916

 V(El)       0.6468       0.6468      -1.2935
 V(Nuc)     -0.5551      -0.5551       1.1103
         ----------   ----------   ----------
 V(Tot)      0.0916       0.0916      -0.1832
 Orientation:
  X      -0.0000003    0.0000002    1.0000000
  Y       0.9878165    0.1556229    0.0000003
  Z      -0.1556229    0.9878165   -0.0000002

Note: Tensor is right-handed


 Quadrupole tensor eigenvalues (in MHz;Q= 0.0204 I=  1.0)
  e**2qQ            =    -0.880 MHz
  e**2qQ/(4I*(2I-1))=    -0.220 MHz
  eta               =     0.000
  NOTE: the diagonal representation of the SH term
  I*Q*I = e**2qQ/(4I(2I-1))*[-(1-eta),-(1+eta),2]
```

If also EPR g-tensor or D-tensor calculations (see next section) are
carried out in the same job, ORCA automatically prints the orientation
between the hyperfine/quadrupole couplings and the molecular g- or
D-tensor. For more information on this see section
{ref}`sec:utilities.euler`.

:::{note}
For heavy nuclei you may want to consider the possibility of relativistic effects. 
Scalar relativistic effects can be handled with several quasi-relativistic Hamiltonians
in ORCA. An overview of the possibilities and some recommendations can be found in
{ref}`sec:essentialelements.relativistic`. Note that relativistic calculations may have
special requirements on basis sets. In relativistic property calculations, you should
be aware of the importance of picture change corrections
(see {ref}`sec:essentialelements.relativistic.picturechange`).
In quasi-relativistic calculations with DFT, one should also be very cautious about
accuracy of the numerical integration, especially for heavier (transition metal) nuclei.
:::

:::{note}
For the calculation of HFCCs using DLPNO-CCSD, it is recommended to use
the tailored truncation settings `!DLPNO-HFC1` or `!DLPNO-HFC2` in the
simple keyword line which correspond to the "Default1" and "Default2"
setting in Ref. {cite}`saitow2018dlpnohfc`.
:::

If you wish to extract the *A* tensor for an oligonuclear transition metal complex, the
`A(iso)` value in the output can be processed according to the method described
in ref. {cite}`Pantazis2009ChemEurJ`.

### A note on basis sets

For hyperfine (and quadrupole) couplings, standard basis sets designed
for energies and geometry optimizations and are often not satisfactory
(especially for atoms heavier than Ne). You should look into a basis set
capable of describing the electronic structure near the nucleus.
One option is to use a basis set tailored towards "core-property"
calculations. The following are good options:

-   `EPR-II` basis of Barone and co-workers: It is only available for a
    few light atoms (H, B, C, N, O, F) and is essentially of double-zeta
    plus polarization quality with added flexibility in the core region,
    which should give reasonable results.

-   `IGLO-II` and `IGLO-III` bases of Kutzelnigg and co-workers: They are
    fairly accurate but also only available for some first and second
    row elements.

-   CP basis: They are accurate for first row transition metals as well.

-   uncontracted Partridge basis: They are general purpose HF-limit
    basis sets and will probably be too expensive for routine use, but
    are very useful for calibration purposes.

-   the `pcH` basis sets by Jensen tailored towards hyperfine coupling
    calculations, also with limited availability
    (see {ref}`sec:essentialelements.basisset.builtin.jensen`).

If ORCA does not yet have a dedicated basis set for your element, you will likely
have to tailor the basis set to your needs. You can
do this by manually adding s-type primitives with large exponents, or by
decontracting core parts of the basis set (see {ref}`sec:essentialelements.basisset`
for description of the decontraction feature).
You can start by examining the basis set you already have - if you
add the statement `Print[p_basis] 2` in the `%output` block
(or `PrintBasis` in the simple input line) the program
will print the basis set in input format (for the basis block).
You can then add or remove primitives, uncontract core functions, etc. For
example, here is a printout of the carbon basis DZP in input format:

```orca
# Basis set for element : C
  NewGTO 6
  s 5
   1  3623.8613000000      0.0022633312
   2   544.0462100000      0.0173452633
   3   123.7433800000      0.0860412011
   4    34.7632090000      0.3022227208
   5    10.9333330000      0.6898436475
  s 1
   1     3.5744765000      1.0000000000
  s 1
    1    0.5748324500      1.0000000000
  s 1
    1    0.1730364000      1.0000000000
  p 3
    1    9.4432819000      0.0570590790
    2    2.0017986000      0.3134587330
    3    0.5462971800      0.7599881644
  p 1
    1    0.1520268400      1.0000000000
  d 1
    1    0.8000000000      1.0000000000
  end;
```

Reading this information is relatively straightforward.
For example: the "`s 5`" stands for the angular momentum and the number
of primitives in the first basis function. The following five lines
then contain the number of the primitive, the exponent and the contraction
coefficient (unnormalized) for each primitive in the function.

**Remember that if you add very steep functions, you *must* increase the
size of the integration grid if your calculation uses DFT! Otherwise,
your results will be inaccurate.** To some extent, the program now
automatically adapts the grids when it detects steep functions.
If you further need to increase integration accuracy, you could globally
increase the radial grid size by increasing `IntAcc`
in the `Method` block, or increase integration accuracy for individual atoms
only, with the latter option being less expensive. More detail can be found
in section {ref}`sec:essentialelements.numericalintegration.detailsandoptions`.
In the present example the changes caused by larger basis sets in the core
region and more accurate integration are relatively modest -- on the order
of 3%. This is, however, still significant if you are a little puristic.

### Hyperfine Coupling Keywords
```{index} Hyperfine Coupling Keywords
```

:::{warning}
All nuclei specified on one line will be assigned with the same isotopic mass (and
other parameters)!
:::


(tab:spectroscopyproperties.epr.hyperfine.keywords.block)=
:::{table} `%eprnmr` block input keywords relevant for HFC calculations
:class: footnotesize
| Keyword         | Selection         | What to do        | Description                                      |
|:----------------|:------------------|:------------------|:-------------------------------------------------|
| `nuclei`        | `all <type>`      |                   | Selects all nuclei of element `<type>`           |
|                 | `i1,i2,i3...`     |                   | Selects atoms `i1`, `i2`, `i3`... (starts at 1!) |
|                 |                   | `{ aiso  }`       | Calculates the isotropic Fermi-contact contribution |                   
|                 |                   | `{ adip  }`       | Calculates the spin-dipole contribution          |                   
|                 |                   | `{ aorb  }`       | Calculates the spin-orbit contribution           |                   
|                 |                   | `{ ist=<N> }`       | Selects isotope `<N>` for selection                |
|                 |                   | `{ PPP=<N> }`       | Sets HFC proportionality factor $\alpha^2 g_e g_N \beta_E \beta_N$ to `<N>` for selection    |
|                 |                   | `{ III=<N> }`       | Sets nuclear spin to `<N>` for selection         |
|                 |                   | `{ aiso, adip, aorb }`  | example requesting multiple actions for selection                 |
:::

:::{raw} latex
\begingroup
\footnotesize
:::

:::{tabularcolumns} \Y{0.35}\Y{0.15}\Y{0.5}
:::
(tab:spectroscopyproperties.epr.tweaks)=
:::{flat-table} `%eprnmr` block possible tweaks for the diamagnetic gauge correction. Unless you have a special reason, it is unlikely that you need to use these settings.
:header-rows: 1
:class: longtable
:class: footnotesize
* - Keyword
  - Options
  - Description
* - `hfcgaugecorrection_zeff`
  - `true/false`
  - Use effective nuclear charges for the gauge correction
* - `hfcgaugecorrection_numeric`
  - `true/false`
  - Calculate DSO integrals numerically (faster)
* - `hfcgaugecorrection_angulargrid`
  - `-1`
  - < 0 means to use the DFT grid setting
* - `hfcgaugecorrection_intacc`
  - `-1`
  - < 0 means to use the DFT grid setting
* - `hfcgaugecorrection_prunegrid`
  - `-1`
  - < 0 means to use the DFT grid setting
* - `hfcgaugecorrection_bfcutoff`
  - `-1`
  - < 0 means to use the DFT grid setting
* - `hfcgaugecorrection_wcutoff`
  - `-1`
  - < 0 means to use the DFT grid setting
:::

:::{raw} latex
\endgroup
:::

(sec:spectroscopyproperties.epr.D)=
## Zero-Field Splitting
```{index} Zero-Field Splitting
```

The zero-field splitting (ZFS) is typically the leading term in the
Spin-Hamiltonian (SH) for transition metal complexes with a total ground
state spin $S$\>1/2 (for reviews and references see chapter
{ref}`sec:appendix.publications`). Its effect is to introduce a
splitting of the $2S+1$ $M_{S}$ sublevels, which are exactly degenerate at
the level of the Born-Oppenheimer Hamiltonian, even in the absence of
an external magnetic field.

### Theory

There are two important contributions to zero-field splitting {cite}`harriman1978ESR`:

- A first order term arising from the direct **spin-spin** interaction

  $$D_{KL}^{ \text{SS} } =\frac{1}{2}\frac{\alpha^{2} }{S\left({ 2S-1}
  \right)}\left\langle { 0SS\left|{ \sum\limits_i { \sum\limits_{j\ne i}
  {\frac{r_{ij}^{2} \delta_{KL} -3\left({ \mathrm{\mathbf{r} }_{ij} } \right)_{K}
  \left({ \mathrm{\mathbf{r} }_{ij} } \right)_{L} }{r_{ij}^{5} }\left\{{2\hat{{s} }_{zi} \hat{{s} }_{zj} -\hat{{s} }_{xi} \hat{{s} }_{xj}
  -\hat{{s} }_{yi} \hat{{s} }_{yj} } \right\}} } } \right|0SS} \right\rangle$$ (eqn:253)

  where $K$,$L=$x,y,z, $\alpha$ is the fine structure constant ($\approx$
  1/137 in atomic units), $\mathrm{\mathbf{r} }_{ij}$ is the electronic
  distance vector with magnitude $r_{ij}$ and $\hat{{s} }_{i}$ is the
  spin-vector operator for the $i$'th electron. $\left|0SS \right\rangle$
  is the exact ground state eigenfunction of the Born-Oppenheimer
  Hamiltonian with total spin $S$ and projection quantum number
  $M_{S} = S$. Since the spin-spin interaction is of first order, its evaluation
  presents no particular difficulties.

- A second-order **spin-orbit** contribution, which is substantially more complicated.
  Under the assumption that the spin-orbit coupling (SOC) operator can to a good
  approximation be represented by an effective one-electron operator
  ($\hat{{H} }_{\text{SOC} } =\sum\nolimits_i { \mathrm{\mathbf{\hat{{h} }} }_{i}^{\text{SOC} } { \mathrm{\mathbf{\hat{s} }} }_{i} } )$, ref {cite}`neese1998inorgchem` has derived the following sum-over-states
  (SOS) equations for the SOC contribution to the ZFS tensor:

  $$D_{KL}^{\text{SOC}-\left( 0 \right)} =-\frac{1}{S^{2} }\sum\limits_{b\left({ S_{b}
  =S} \right)} { \Delta_{b}^{-1} \left\langle { 0^{SS}\left|{ \sum\limits_i
  {\hat{{h} }_{i}^{K;\text{SOC} } \hat{{s} }_{i,0} } } \right|b^{SS} } \right\rangle\left\langle { b^{SS}\left|{ \sum\limits_i { \hat{{h} }_{i}^{L;\text{SOC} }
  \hat{{s} }_{i,0} } } \right|0^{SS} } \right\rangle}
  $$ (eqn:254)

  $$D_{KL}^{\text{SOC}-\left({ -1} \right)} =-\frac{1}{S\left({ 2S-1}
  \right)}\sum\limits_{b\left({ S_{b} =S-1} \right)} { \Delta_{b}^{-1}
  \left\langle { 0^{SS}\left|{ \sum\limits_i { \hat{{h} }_{i}^{K;\text{SOC} }
  \hat{{s} }_{i,+1} } } \right|b^{S-1S-1} } \right\rangle\left\langle {b^{S-1S-1}\left|{ \sum\limits_i { \hat{{h} }_{i}^{L;\text{SOC} } \hat{{s} }_{i,-1} } }
  \right|0^{SS} } \right\rangle}
  $$ (eqn:255)

  $$\begin{array}{l}
  D_{KL}^{\text{SOC}-\left({ +1} \right)} =-\frac{1}{\left({ S+1} \right)\left({2S+1} \right)} \cdot \\
  \hspace{2cm}
  \sum\limits_{b\left({ S_{b} =S+1} \right)} { \Delta_{b}^{-1}
  \left\langle { 0^{SS}\left|{ \sum\limits_i { \hat{{h} }_{i}^{K;\text{SOC} }
  \hat{{s} }_{i,-1} } } \right|b^{S+1S+1} } \right\rangle\left\langle {b^{S+1S+1}\left|{ \sum\limits_i { \hat{{h} }_{i}^{L;\text{SOC} } \hat{{s} }_{i,+1} } }
  \right|0^{SS} } \right\rangle}
  \end{array}
  $$ (eqn:256)

  Here the one-electron spin-operator for electron $i$ has been written in
  terms of spherical vector operator components $s_{i,m}$ with $m=0,\pm 1$
  and $\Delta_{b} =E_{b} -E_{0}$ is the excitation energy to the excited
  state multiplet $\left| b^{SS} \right\rangle$ (all $M_{S}$ components
  are degenerate at the level of the BO Hamiltonian).

:::{note}
The second-order spin-orbit term may be evaluated using the above sum-over-states
formulation in the context of wavefunction theory methods. The following section
focuses on a formulation based on SCF analytical derivative/response theory.
You may also be interested in QDPT, which is more reliable particularly in systems
where zero-field splitting is large.
:::

:::{note}
Available treatments of the
spin-orbit coupling operator are described under {ref}`sec:spectroscopyproperties.soc`.
:::

### Basic usage

For example, consider the following job on a hypothetical Mn(III)-complex.

```{literalinclude} ../../orca_working_input/C05S13_229.inp
:language: orca
```

The output documents the individual contributions to the D-tensor, which
also contains (unlike the g-tensor) contributions from spin-flip terms.

:::{note}
There are four different variants of the SOC-contribution, which alone
should demonstrate that this is a difficult property. The options are:

-   The QRO method is fully documented{cite}`neese2006am` and is based on a
    theory developed earlier.{cite}`neese1998inorgchem` The QRO method is
    reasonable but somewhat simplistic and is superseded by the CP
    method described below.
  
-   The Pederson-Khanna model was brought forward in 1999 from
    qualitative reasoning.{cite}`pedersonkhanna1999gtensor-zfs` It also
    contains incorrect prefactors for the spin-flip terms. We have
    nevertheless implemented the method for comparison. In the original
    form it is only valid for local functionals. In ORCA it is extended
    to hybrid functionals and HF.

-   The default coupled-perturbed method is a generalization of the DFT method
    for ZFSs; it uses revised prefactors for the spin-flip terms and
    solves a set of coupled-perturbed equations for the SOC
    perturbation. Therefore it is valid for hybrid functionals. It has
    been described in detail.{cite}`Neese2007zfs`
:::

The present implementation in ORCA is valid for HF, DFT and hybrid DFT.

The DSS part is an expectation value that involves the spin density
of the system. In detailed calibration work{cite}`sinnecker2006` it was
found that the spin-unrestricted DFT methods behave somewhat
erratically and that much more accurate values were obtained from
open-shell spin-restricted DFT. Therefore the "UNO" option allows
the calculation of the SS term with a restricted spin density
obtained from the singly occupied unrestricted natural orbitals.

The DSS part contains an erratic self-interaction term for UKS/UHF
wavefunction and canonical orbitals. Thus, `UNO` is recommended for
these types of calculations.{cite}`riplinger2009epr` If the option
`DIRECT` is used nevertheless, ORCA will print a warning in the
respective part of the output.

:::{note}
In case that D-tensor is calculated using the correlated wave
function methods such as (DLPNO-/LPNO-)CCSD, one should not use
`DSS=UNO` option.
:::

(sec:spectroscopyproperties.epr.D.detail)=
### Detailed theory of the coupled-perturbed formulation

In 2007, we have developed a procedure that makes the ZFS calculation
compatible with the language of analytic derivatives.{cite}`Neese2007zfs`
Perhaps the most transparent route is to start from the exact solutions
of the Born-Oppenheimer Hamiltonian. To this end, we look at the second
derivative of the ground state energy
($E=\left\langle { 0^{SS}\left|{\hat{{H} }} \right|0^{SS} } \right\rangle)$
with respect to a spin-dependent one-electron operator of the general
form:

$$\hat{{h} }^{K;\left( m \right)}=x_{K}^{\left( m \right)} \sum\limits_{pq}
{h_{pq}^{K} \hat{{S} }_{pq}^{\left( m \right)} }
$$ (eqn:260)

Where $h_{pq}^{K}$ is the matrix of the $K$'th component of the spatial
part of the operator (assumed to be imaginary Hermitian as is the case
for the spatial components of the SOC operator) and
$\hat{{S} }_{pq}^{\left( m
\right)}$ is the second quantized form of the spin vector operator
($m=0,\pm 1$). The quantity $x_{K}^{\left( m \right)}$ is a formal
perturbation parameter. Using the exact eigenfunctions of the BO
operator, the first derivative is:

$$\left.{ \frac{\partial E}{\partial x_{K}^{\left( m \right)} } }
\right|_{x_{K}^{\left( m \right)} =0} =\sum\limits_{pq} { h_{pq}^{K}
P_{pq}^{\left( m \right)} }
$$ (eqn:261)

With the components of the spin density:

$$P_{pq}^{\left( m \right)} =\left\langle { 0^{SS}\vert \hat{{S} }_{pq}^{\left(m \right)} \vert 0^{SS} } \right\rangle$$ (eqn:262)

The second derivative with respect to a second component for $m'=-m$ is:

$$\left.{ \frac{\partial^{2}E}{\partial x_{K}^{\left( m \right)} \partial
x_{L}^{\left({ -m} \right)} } } \right|_{x_{K}^{\left( m \right)}
=x_{L}^{\left({ -m} \right)} =0} =\sum\limits_{pq} { h_{pq}^{K}
\frac{\partial P_{pq}^{\left( m \right)} }{x_{L}^{\left({ -m} \right)} } }
$$ (eqn:263)

The derivative of the spin density may be written as:

$$\frac{\partial P_{pq}^{\left( m \right)} }{x_{L}^{\left({ -m} \right)}
}=\left\langle { 0_{L}^{SS\left({ -m} \right)} \vert \hat{{S} }_{pq}^{\left( m
\right)} \vert 0^{SS} } \right\rangle+\left\langle { 0^{SS}\vert
\hat{{S} }_{pq}^{\left( m \right)} \vert 0_{L}^{SS\left({ -m} \right)} }
\right\rangle$$ (eqn:264)

Expanding the perturbed wavefunction in terms of the unperturbed states
gives to first order:

$$\left| 0_L^{SS\left(-m\right)}\right\rangle=
-\sum\limits{n \ne 0} \Delta_n^{-1} \left| n \right \rangle \left\langle n \left| \hat{h}^
{L;\left(-m\right)} \right| 0^{SS} \right \rangle
$$ (eqn:265)

Where $\left| n \right\rangle$ is any of the
$\left| b^{S'M'} \right\rangle$. Thus, one gets:

$$\frac{\partial^{2}E}{\partial x_{K}^{\left( m \right)} \partial
x_{L}^{\left({ -m} \right)} }=\sum\limits_{pq} { h_{pq}^{K} \frac{\partial
P_{pq}^{\left( m \right)} }{x_{L}^{\left({ -m} \right)} } }
$$ (eqn:266)

$$\hspace{2cm}
=-\sum\limits_{n\ne 0} { \Delta
_{n}^{-1} \left[{ \left\langle { 0^{SS}\vert \hat{{h} }^{L;\left({ -m}
\right)}\vert n} \right\rangle\left\langle { n\vert \hat{{h} }^{K;\left( m
\right)}\vert 0^{SS} } \right\rangle+\left\langle { 0^{SS}\vert
\hat{{h} }^{K;\left( m \right)}\vert n} \right\rangle\left\langle { n\vert
\hat{{h} }^{L;\left({ -m} \right)}\vert 0^{SS} } \right\rangle} \right]}
$$ (eqn:267)

The equality holds for exact states. For approximate electronic
structure treatments, the analytic derivative approach is more
attractive since an infinite sum over states can never be performed in
practice and the calculation of analytic derivative is computationally
less demanding than the calculation of excited many electron states.

Using eq. {eq}`eqn:266`, the components of the SOC-contribution to the
**D**-tensor are reformulated as

$$D_{KL}^{\text{SOC}-\left( 0 \right)} =\frac{1}{2S^{2} }\sum\limits_{pq}
{h_{pq}^{K;\text{SOC} } \frac{\partial P_{pq}^{\left( 0 \right)} }{\partial
x_{L}^{\left( 0 \right)} } }
$$ (eqn:268)

$$D_{KL}^{\text{SOC}-\left({ -1} \right)} =\frac{1}{S\left({ 2S-1}
\right)}\sum\limits_{pq} { h_{pq}^{K;\text{SOC} } \frac{\partial P_{pq}^{\left({ +1}
\right)} }{\partial x_{L}^{\left({ -1} \right)} } }
$$ (eqn:269)

$$D_{KL}^{\text{SOC}-\left({ +1} \right)} =\frac{1}{\left({ S+1} \right)\left({ 2S+1}
\right)}\sum\limits_{pq} { h_{pq}^{K;\text{SOC} } \frac{\partial P_{pq}^{\left({ -1}
\right)} }{\partial x_{L}^{\left({ +1} \right)} } }
$$ (eqn:270)

These are general equations that can be applied together with any
non-relativistic or scalar relativistic electronic structure method that
can be cast in second quantized form. Below, the formalism is applied to
the case of a self-consistent field (HF, DFT) reference state.

For DFT or HF ground states, the equations are further developed as
follows:

The SCF energy is:

$$E_{\text{SCF} } =V_{\text{NN} } +\left\langle { \mathrm{\mathbf{Ph} }^{+} } \right\rangle+\frac{1}{2}\int{ \int{ \frac{\rho \left({ \mathrm{\mathbf{r} }_{1} } \right)\rho
\left({ \mathrm{\mathbf{r} }_{2} } \right)}{\left|{ \mathrm{\mathbf{r} }_{1} -\mathrm{\mathbf{r} }_{2} } \right|}d\mathrm{\mathbf{r} }_{1} d\mathrm{\mathbf{r} }_{2} } }
-\frac{1}{2}a_{\text{X} } \sum\limits_{\mu \nu \kappa \tau \sigma } { P_{\mu \kappa
}^{\sigma } P_{\nu \tau }^{\sigma } \left({ \mu \nu \vert \kappa \tau }
\right)} +c_{\text{DF} } E_{\text{XC} } \left[{ \rho_{\alpha } ,\rho_{\beta } } \right]$$ (eqn:271)

Here $V_{\text{NN} }$ is the nuclear repulsion energy and $h_{\mu \nu }$
is a matrix element of the one-electron operator which contains the
kinetic energy and electron-nuclear attraction terms
($\left\langle { \mathrm{\mathbf{ab} }}
\right\rangle$ denotes the trace of the matrix product
$\mathrm{\mathbf{ab} }$). As usual, the molecular spin-orbitals
$\psi_{p}^{\sigma }$ are expanded in atom centered basis functions
($\sigma =\alpha ,\beta )$:

$$\psi_{p}^{\sigma } \left({ \mathrm{\mathbf{r} }} \right)=\sum\limits_\mu{ c_{\mu
p}^{\sigma } \phi_{\mu } \left({ \mathrm{\mathbf{r} }} \right)}
$$ (eqn:272)

with MO coefficients $c_{\mu p}^{\sigma }$. The two-electron integrals
are defined as:

$$\left({ \mu \nu \vert \kappa \tau } \right)=\int{ \int{ \phi_{\mu } \left({\mathrm{\mathbf{r} }_{1} } \right)\phi_{\nu } \left({ \mathrm{\mathbf{r} }_{1} }
\right)r_{12}^{-1} \phi_{\kappa } \left({ \mathrm{\mathbf{r} }_{2} } \right)\phi
_{\tau } \left({ \mathrm{\mathbf{r} }_{2} } \right)d\mathrm{\mathbf{r} }_{1} d\mathrm{\mathbf{r} }_{2} } }
$$ (eqn:273)

The mixing parameter $a_{\text{X} }$ controls the fraction of
Hartree-Fock exchange and is of a semi-empirical nature.
$E_{\text{XC} } \left[{ \rho_{\alpha } ,\rho
_{\beta } } \right]$ represent the exchange-correlation energy. The
parameter $c_{\text{DF} }$ is an overall scaling factor that allows one
to proceed from Hartree-Fock theory
($a_{\text{X} } =1, c_{\text{DF} } =0)$ to pure DFT ($a_{\text{X} }
=0, c_{\text{DF} } =1)$ to hybrid DFT
($0<a_{\text{X} } <1, c_{\text{DF} } =1$). The orbitals satisfy the
spin-unrestricted SCF equations:

$$F_{\mu \nu }^{\sigma } =h_{\mu \nu } +\sum\limits_{\kappa \tau } { P_{\kappa
\tau } \left({ \mu \nu \vert \kappa \tau } \right)-a_{\text{X} } P_{\kappa \tau
}^{\sigma } \left({ \mu \kappa \vert \nu \tau } \right)} +c_{\text{DF} } \left({ \mu
\vert V_{XC}^{\alpha } \vert \nu } \right)$$ (eqn:274)

With
$V_{XC}^{\sigma } =\frac{\delta E_{XC} }{\delta \rho_{\sigma } \left({\mathrm{\mathbf{r} }} \right)}$
and $P_{\mu \nu } =P_{\mu \nu }^{\alpha } +P_{\mu
\nu }^{\beta }$ being the total electron density. For the SOC
perturbation it is customary to regard the basis set as perturbation
independent. In a spin-unrestricted treatment, the first derivative is:

$$\frac{\partial E_{\text{SCF} } }{\partial x_{K}^{\left( m \right)}
}=\sum\limits_{i_{\alpha } } { \left({ i_{\alpha } \vert h^{K}s_{m} \vert
i_{\alpha } } \right)} +\sum\limits_{i_{\beta } } { \left({ i_{\beta } \vert
h^{K}s_{m} \vert i_{\beta } } \right)} =0
$$ (eqn:275)

For the second derivative, the perturbed orbitals are required. However,
in the presence of a spin-dependent perturbation they can no longer be
taken as pure spin-up or spin-down orbitals. With respect to the $L$'th
component of the perturbation for spin-component $m$, the orbitals are
expanded as:

$$\psi_{i}^{\alpha ;\left( m \right)L} \left({ \mathrm{\mathbf{r} }}
\right)=\sum\limits_{a_{\alpha } } { U_{a_{\alpha } i_{\alpha } }^{\left( m
\right);L} \psi_{a}^{\alpha } \left({ \mathrm{\mathbf{r} }} \right)}
+\sum\limits_{a_{\beta } } { U_{a_{\beta } i_{\alpha } }^{\left( m \right);L}
\psi_{a}^{\beta } \left({ \mathrm{\mathbf{r} }} \right)}
$$ (eqn:276)

$$\psi_{i}^{\beta ;\left( m \right)L} \left({ \mathrm{\mathbf{r} }}
\right)=\sum\limits_{a_{\alpha } } { U_{a_{\alpha } i_{\beta } }^{\left( m
\right);L} \psi_{a}^{\alpha } \left({ \mathrm{\mathbf{r} }} \right)}
+\sum\limits_{a_{\beta } } { U_{a_{\beta } i_{\beta } }^{\left( m \right);L}
\psi_{a}^{\beta } \left({ \mathrm{\mathbf{r} }} \right)}
$$ (eqn:277)

Since the matrix elements of the spin-vector operator components are
purely real and the spatial part of the SOC operator has purely
imaginary matrix elements, it follows that the first order coefficients
are purely imaginary. The second derivative of the total SCF energy
becomes:

$$
\begin{split}
 \frac{\partial^{2}E_{\text{SCF} } }{\partial x_{K}^{\left( m \right)} \partial x_{L}^{\left({ -m} \right)} }=\sum\limits_{i_{\alpha } a_{\alpha } }
{\left\{{ U_{a_{\alpha } i_{\alpha } }^{\left({ -m} \right);L\ast } \left({a_{\alpha } \vert h^{K}s_{m} \vert i_{\alpha } } \right)+U_{a_{\alpha }
i_{\alpha } }^{\left({ -m} \right);L} \left({ i_{\alpha } \vert h^{K}s_{m}
\vert a_{\alpha } } \right)} \right\}} \\
 +\sum\limits_{i_{\alpha } a_{\beta } } { \left\{{ U_{a_{\beta } i_{\alpha }
}^{\left({ -m} \right);L\ast } \left({ a_{\beta } \vert h^{K}s_{m} \vert
i_{\alpha } } \right)+U_{a_{\beta } i_{\alpha } }^{\left({ -m} \right);L}
\left({ i_{\alpha } \vert h^{K}s_{m} \vert a_{\beta } } \right)} \right\}}
\\
 +\sum\limits_{i_{\beta } a_{\alpha } } { \left\{{ U_{a_{\alpha } i_{\beta }
}^{\left({ -m} \right);L\ast } \left({ a_{\alpha } \vert h^{K}s_{m} \vert
i_{\beta } } \right)+U_{a_{\alpha } i_{\beta } }^{\left({ -m} \right);L}
\left({ i_{\beta } \vert h^{K}s_{m} \vert a_{\alpha } } \right)} \right\}}
\\
 +\sum\limits_{i_{\beta } a_{\beta } } { \left\{{ U_{a_{\beta } i_{\beta }
}^{\left({ -m} \right);L\ast } \left({ a_{\beta } \vert h^{K}s_{m} \vert
i_{\beta } } \right)+U_{a_{\beta } i_{\beta } }^{\left({ -m} \right);L}
\left({ i_{\beta } \vert h^{K}s_{m} \vert a_{\beta } } \right)} \right\}}
\end{split}
$$(eqn:278)

Examination of the three cases $m=0, \pm 1$ leads to the following
equations for the **D**-tensor components:

$$D_{KL}^{\left( 0 \right)} =-\frac{1}{4S^{2} }\sum\limits_{\mu \nu }
{\frac{\partial P_{\mu \nu }^{\left( 0 \right)} }{\partial x_{L}^{\left( 0
\right)} }\left({ \mu \vert h^{K;\text{SOC} }\vert \nu } \right)}
$$ (eqn:279)

$$D_{KL}^{\left({ +1} \right)} =\frac{1}{2\left({ S+1} \right)\left({ 2S+1}
\right)}\sum\limits_{\mu \nu } { \left({ \mu \vert h^{K;\text{SOC} }\vert \nu }
\right)\frac{\partial P_{\mu \nu }^{\left({ -1} \right)} }{\partial
x_{L}^{\left({ +1} \right)} } }
$$ (eqn:280)

$$D_{KL}^{\left({ -1} \right)} =\frac{1}{2S\left({ 2S-1}
\right)}\sum\limits_{\mu \nu } { \left({ \mu \vert h^{K;\text{SOC} }\vert \nu }
\right)} \frac{\partial P_{\mu \nu }^{\left({ +1} \right)} }{\partial
x_{L}^{\left({ -1} \right)} }
$$ (eqn:281)

Where a special form of the perturbed densities has been chosen. They
are given in the atomic orbital basis as:

$$\frac{\partial P_{\mu \nu }^{\left( 0 \right)} }{\partial x_{L}^{\left( 0
\right)} }=\sum\limits_{i_{\alpha } a_{\alpha } } { U_{a_{\alpha } i_{\alpha
} }^{\left( 0 \right);L} c_{\mu i}^{\alpha } c_{\nu a}^{\alpha } }
+\sum\limits_{i_{\beta } a_{\beta } } { U_{a_{\beta } i_{\beta } }^{\left( 0
\right);L} c_{\mu i}^{\beta } c_{\nu a}^{\beta } }
$$ (eqn:282)

$$\frac{\partial P_{\mu \nu }^{\left({ +1} \right)} }{\partial x_{L}^{\left({-1} \right)} }=\sum\limits_{i_{\alpha } a_{\beta } } { U_{a_{\beta }
i_{\alpha } }^{\left({ -1} \right);L} c_{\mu i}^{\alpha } c_{\nu a}^{\beta }
} -\sum\limits_{i_{\beta } a_{\alpha } } { U_{a_{\alpha } i_{\beta }
}^{\left({ -1} \right);L} c_{\mu a}^{\alpha } c_{\nu i}^{\beta } }
$$ (eqn:283)

$$\frac{\partial P_{\mu \nu }^{\left({ -1} \right)} }{\partial x_{L}^{\left({+1} \right)} }=-\sum\limits_{i_{\alpha } a_{\beta } } { U_{a_{\beta }
i_{\alpha } }^{\left({ +1} \right);L} c_{\mu a}^{\beta } c_{\nu i}^{\alpha }
} +\sum\limits_{i_{\beta } a_{\alpha } } { U_{a_{\alpha } i_{\beta }
}^{\left({ +1} \right);L} c_{\mu i}^{\beta } c_{\nu a}^{\alpha } }
$$ (eqn:284)

The special form of the coupled perturbed equations are implemented in
ORCArun as follows: The perturbation is of the general form
$h^{K}\hat{{s} }_{m}$. The equations
{eq}`eqn:279`-{eq}`eqn:284` and {eq}`eqn:285`-{eq}`eqn:290` below have been written in such a way that the spin
integration has been performed but that the spin-dependent factors have
been dropped from the right-hand sides and included in the prefactors of
eqs. {eq}`eqn:279`-{eq}`eqn:281`. The explicit forms of the linear equations to be
solved are:

$m=0$:

$$\left({ \varepsilon_{a_{\alpha } }^{\left( 0 \right)} -\varepsilon
_{i_{\alpha } }^{\left( 0 \right)} } \right)U_{a_{\alpha } i_{\alpha }
}^{K\left( 0 \right)} +a_{\text{X} } \sum\limits_{j_{\alpha } b_{\alpha } }
{U_{b_{\alpha } j_{\alpha } }^{K\left( m \right)} \left\{{ \left({ b_{\alpha
} i_{\alpha } \vert a_{\alpha } j_{\alpha } } \right)-\left({ j_{\alpha }
i_{\alpha } \vert a_{\alpha } b_{\alpha } } \right)} \right\}} =-\left({a_{\alpha } \vert h^{K}\vert i_{\alpha } } \right)$$ (eqn:285)

$$\left({ \varepsilon_{a_{\beta } }^{\left( 0 \right)} -\varepsilon
_{i_{\beta } }^{\left( 0 \right)} } \right)U_{a_{\beta } i_{\beta }
}^{K\left( 0 \right)} +a_{\text{X} } \sum\limits_{j_{\beta } b_{\beta } }
{U_{b_{\beta } j_{\beta } }^{K\left( m \right)} \left\{{ \left({ b_{\beta }
i_{\beta } \vert a_{\beta } j_{\beta } } \right)-\left({ j_{\beta } i_{\beta
} \vert a_{\beta } b_{\beta } } \right)} \right\}} =-\left({ a_{\beta }
\vert h^{K}\vert i_{\beta } } \right)$$ (eqn:286)

$m=+1$:

$$\left({ \varepsilon_{a_{\alpha } }^{\left( 0 \right)} -\varepsilon
_{i_{\beta } }^{\left( 0 \right)} } \right)U_{a_{\alpha } i_{\beta }
}^{K\left({ +1} \right)} +a_{\text{X} } \sum\limits_{j_{\alpha } b_{\alpha } }
{U_{b_{\beta } j_{\alpha } }^{K\left({ +1} \right)} \left({ b_{\beta }
i_{\beta } \vert a_{\alpha } j_{\alpha } } \right)} -a_{\text{X} }
\sum\limits_{b_{\alpha } j_{\beta } } { U_{b_{\beta } j_{\alpha } }^{K\left({+1} \right)} \left({ j_{\beta } i_{\beta } \vert a_{\alpha } b_{\alpha } }
\right)} =-\left({ a_{\alpha } \vert h^{K}\vert i_{\beta } } \right)$$ (eqn:287)

$$\left({ \varepsilon_{a_{\beta } }^{\left( 0 \right)} -\varepsilon
_{i_{\alpha } }^{\left( 0 \right)} } \right)U_{a_{\beta } i_{\alpha }
}^{K\left({ +1} \right)} +a_{\text{X} } \sum\limits_{j_{\beta } b_{\alpha } }
{U_{b_{\alpha } j_{\beta } }^{K\left({ +1} \right)} \left({ b_{\alpha }
i_{\alpha } \vert a_{b} j_{\beta } } \right)} -a_{\text{X} } \sum\limits_{b_{\beta }
j_{\alpha } } { U_{b_{\beta } j_{\alpha } }^{K\left({ +1} \right)} \left({j_{\alpha } i_{\alpha } \vert a_{\beta } b_{\beta } } \right)} =0
$$ (eqn:288)

$m=-1$:

$$\left({ \varepsilon_{a_{\beta } }^{\left( 0 \right)} -\varepsilon
_{i_{\alpha } }^{\left( 0 \right)} } \right)U_{a_{\beta } i_{\alpha }
}^{K\left({ -1} \right)} +a_{\text{X} } \sum\limits_{j_{\beta } b_{\alpha } }
{U_{b_{\alpha } j_{\beta } }^{K\left({ -1} \right)} \left({ b_{\alpha }
i_{\alpha } \vert a_{b} j_{\beta } } \right)} -a_{\text{X} } \sum\limits_{b_{\beta }
j_{\alpha } } { U_{b_{\beta } j_{\alpha } }^{K\left({ -1} \right)} \left({j_{\alpha } i_{\alpha } \vert a_{\beta } b_{\beta } } \right)} =-\left({a_{\beta } \vert h^{K}\vert i_{\alpha } } \right)$$ (eqn:289)

$$\left({ \varepsilon_{a_{\alpha } }^{\left( 0 \right)} -\varepsilon
_{i_{\beta } }^{\left( 0 \right)} } \right)U_{a_{\alpha } i_{\beta }
}^{K\left({ -1} \right)} +a_{\text{X} } \sum\limits_{j_{\alpha } b_{\alpha } }
{U_{b_{\beta } j_{\alpha } }^{K\left({ -1} \right)} \left({ b_{\beta }
i_{\beta } \vert a_{\alpha } j_{\alpha } } \right)} -a_{\text{X} }
\sum\limits_{b_{\alpha } j_{\beta } } { U_{b_{\beta } j_{\alpha } }^{K\left({-1} \right)} \left({ j_{\beta } i_{\beta } \vert a_{\alpha } b_{\alpha } }
\right)} =0
$$ (eqn:290)

Note that these coupled-perturbed (CP) equations contain no contribution
from the Coulomb potential or any other local potential such as the
exchange-correlation potential in DFT. Hence, in the absence of HF
exchange, the equations are trivially solved:

$$U_{a_{\alpha } i_{\alpha } }^{K\left( 0 \right)} =-\frac{\left({ a_{\alpha }
\vert h^{K}\vert i_{\alpha } } \right)}{\varepsilon_{a_{\alpha } }^{\left(0 \right)} -\varepsilon_{i_{\alpha } }^{\left( 0 \right)} }
$$ (eqn:291)

$$U_{a_{\beta } i_{\beta } }^{K\left( 0 \right)} =-\frac{\left({ a_{\beta }
\vert h^{K}\vert i_{\beta } } \right)}{\varepsilon_{a_{\beta } }^{\left( 0
\right)} -\varepsilon_{i_{\beta } }^{\left( 0 \right)} }
$$ (eqn:292)

$$U_{a_{\alpha } i_{\beta } }^{K\left({ +1} \right)} =-\frac{\left({ a_{\alpha
} \vert h^{K}\vert i_{\beta } } \right)}{\varepsilon_{a_{\alpha } }^{\left(0 \right)} -\varepsilon_{i_{\beta } }^{\left( 0 \right)} }
$$ (eqn:293)

$$U_{a_{\beta } i_{\alpha } }^{K\left({ +1} \right)} =0
$$ (eqn:294)

$$U_{a_{\beta } i_{\alpha } }^{K\left({ -1} \right)} =-\frac{\left({ a_{\beta
} \vert h^{K}\vert i_{\alpha } } \right)}{\varepsilon_{a_{\beta } }^{\left(0 \right)} -\varepsilon_{i_{\alpha } }^{\left( 0 \right)} }
$$ (eqn:295)

$$U_{a_{\alpha } i_{\beta } }^{K\left({ -1} \right)} =0
$$ (eqn:296)

It is interesting that the "reverse spin flip coefficients"
$U_{a_{\beta }
i_{\alpha } }^{K\left({ +1} \right)}$ and $U_{a_{\alpha } i_{\beta }
}^{K\left({ -1} \right)}$ are only nonzero in the presence of HF
exchange. In a perturbation expansion of the CP equations they arise at
second order (V$^{2}$/$\Delta \varepsilon^{2})$ while the other
coefficients are of first order (V/$\Delta \varepsilon$; V represents
the matrix elements of the perturbation). Hence, these contributions are
of the order of $\alpha^{4}$ and one could conceive dropping them from
the treatment in order to stay consistently at the level of
$\alpha^{2}$. These terms were nevertheless kept in the present
treatment.

Equations {eq}`eqn:285`-{eq}`eqn:290` are referred to as CP-SOC (coupled-perturbed
spin-orbit coupling) equations. They can be solved by standard
techniques and represent the desired analogue of the CP-SCF magnetic
response equations solved for the determination of the g-tensor and
discussed in detail earlier {cite}`perdew1992physa`. It is readily confirmed
that in the absence of HF exchange, eqs.
{eq}`eqn:291`-{eq}`eqn:296` inserted into eqs.
{eq}`eqn:279`-{eq}`eqn:284` lead back to a modified Pederson-Khanna type
treatment of the SOC contributions to the **D**-tensor
{cite}`perdew1996phys`. In the framework of the formalism developed above,
the Pederson-Khanna formula can be re-written in the form:

$$\begin{split}
 D_{KL}^{\left({ \text{SOC};\text{PK} } \right)} =\frac{1}{4S^{2} }\sum\limits_{i_{\beta }
,a_{\beta } } { \left({ \psi_{i}^{\beta } \left|{ h^{K;\text{SOC} } } \right|\psi
_{a}^{\beta } } \right)U_{a_{\beta } i_{\beta } }^{L;\left( 0 \right)} }
+\frac{1}{4S^{2} }\sum\limits_{i_{\alpha } ,a_{\alpha } } { \left({ \psi
_{i}^{\alpha } \left|{ h^{K;\text{SOC} } } \right|\psi_{a}^{\alpha } }
\right)U_{a_{\alpha } i_{\alpha } }^{L;\left( 0 \right)} } \\
\hspace{3cm}
-\frac{1}{4S^{2} }\sum\limits_{i_{\alpha
} ,a_{\beta } } { \left({ \psi_{i}^{\alpha } \left|{ h^{K;\text{SOC} } }
\right|\psi_{a}^{\beta } } \right)U_{a_{\beta } i_{\alpha } }^{L;\left({-1} \right)} } -\frac{1}{4S^{2} }\sum\limits_{i_{\beta } ,a_{\alpha } }
{\left({ \psi_{i}^{\alpha } \left|{ h^{K;\text{SOC} } } \right|\psi_{a}^{\alpha
} } \right)U_{a_{\alpha } i_{\beta } }^{L;\left({ +1} \right)} }
\end{split}
$$ (eqn:297)

This equation was derived from second-order non-self-consistent
perturbation theory without recourse to spin-coupling. For the special
case of no Hartree-Fock exchange, the main difference to the treatment
presented here is that the correct prefactors from eqs.
{eq}`eqn:268`-{eq}`eqn:270` occur in front of the spin-flip contributions
rather than $\pm$ 1/(4$S^{2})$ in eq.
{eq}`eqn:297`. In
the presence of HF exchange it is suggested that the consistent
generalization of the PK method are eqs.
{eq}`eqn:279`-{eq}`eqn:281` with the $\pm$ 1/(4$S^{2})$ prefactors and this way
the method has been implemented as an option into the ORCA program.

For completeness, the evaluation of the spin-spin term in the SCF case
proceeds conveniently through:

$$D_{KL}^{\left( \text{SS} \right)} =\frac{g_{e}^{2} }{4}\frac{\alpha^{2} }{S\left({2S-1} \right)}\sum\limits_{\mu \nu } { \sum\limits_{\kappa \tau } { \left\{{P_{\mu \nu }^{\alpha -\beta } P_{\kappa \tau }^{\alpha -\beta } -P_{\mu
\kappa }^{\alpha -\beta } P_{\nu \tau }^{\alpha -\beta } } \right\}} }
\left\langle { \mu \nu \left|{ r_{12}^{-5} \left\{{ 3r_{12,K} r_{12,L}
-\delta_{KL} r_{12}^{2} } \right\}} \right|\kappa \tau } \right\rangle$$ (eqn:298)

as derived by McWeeny and Mizuno and discussed in some detail by
Sinnecker and Neese.{cite}`sinnecker2006` In this reference it was found that
DFT methods tend to overestimate the spin-spin contribution if the
calculations are based on a spin-unrestricted SCF treatment. A much
better correlation with experiment was found for open-shell spin
restricted calculations. The origin of this effect proved to be
difficult to understand but it was shown in ref {cite}`hammer1999phys` that
in the case of small spin-contamination, the results of ROKS
calculations and of those that are obtained on the basis of the
spin-unrestricted natural orbital (UNO) determinant are virtually
indistinguishable. It is therefore optionally possible in the ORCA
program to calculate the spin-spin term on the basis of the UNO
determinant.

### ZFS Keywords
```{index} Zero-Field Splitting Keywords
```

(tab:spectroscopyproperties.epr.D.keywords.block)=
:::{table} `%eprnmr` block input keywords relevant for ZFS calculations
| Keyword         | Options          | Description                                      |
|:----------------|:-----------------|:-------------------------------------------------|
| `dtensor`       | `ss`             | Calculate spin-spin part                         |
|                 | `so`             | Calculate spin-orbit part                        |
|                 | `ssandso`        | Calculate both parts                             |
| `DSOC`          | `qro`            | quasi-restricted method for SOC, must be combined with `!UNO`|
|                 | `pk`             | Pederson-Khanna method for SOC                   |
|                 | `cp`             | coupled-perturbed method for SOC (default)       |
|                 | `cvw`            | van Wüllen method for SOC                        |
| `DSS`           | `direct`         | directly use the canonical orbitals for the spin density|
|                 | `uno`            | use spin density from UNOs                       |
| `printEuler`    | `true/false`     | Whether to calculate Euler angles via `orca_euler` |
:::

