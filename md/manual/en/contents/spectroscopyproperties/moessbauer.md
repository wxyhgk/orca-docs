```{index} Mössbauer Spectroscopy
```

(sec:spectroscopyproperties.moessbauer)=
# Mössbauer Parameters

$^{57}$Fe Mössbauer spectroscopy probes the transitions of the nucleus
between the $I = \frac{1}{2}$ ground state and the $I = \frac{3}{2}$
excited state at 14.4 keV above the ground state. The important features
of the Mössbauer spectrum are the isomer shift ($\delta$) and the
quadrupole splitting ($\Delta E_\mathrm{Q}$). An idealized spectrum is
shown in {numref}`fig:Moessbauer`.

(fig:Moessbauer)=
```{figure} ../../images/Moessbauer.*

An idealized Mössbauer spectrum showing both the isomer shift,
$\delta$, and the quadrupole splitting,
$\Delta E_\mathrm{Q}$.
```

## Isomer Shift
```{index} Isomer Shift
```

The isomer shift measures the shift in the energy of the $\gamma$-ray
absorption relative to a standard, usually Fe foil. The isomer shift is
sensitive to the electron density at the nucleus, and indirectly probes
changes in the bonding of the valence orbitals due to variations in
covalency and 3d shielding. Thus, it can be used to probe oxidation and
spin states, and the coordination environment of the iron.

Both the isomer shift and quadrupole splitting can be successfully
predicted using DFT methods. The isomer shift is directly related to the
s electron density at the nucleus and can be calculated using the
formula

$$\delta = \alpha (\rho_0 - C) + \beta
$$ (eqn:MB_isomer_shift)

where $\alpha$ is a constant that depends on the change in the
distribution of the nuclear charge upon absorption, and $\rho_0$ is the
electron density at the nucleus {cite}`Neese2002Moessbauer`. The constants
$\alpha$ and $\beta$ are usually determined via linear regression
analysis of the experimental isomer shifts versus the theoretically
calculated electron density for a series of iron compounds with various
oxidation and spin states. Since the electron density depends on the
functional and basis set employed, fitting must be carried out for each
combination used. A compilation of calibration constants ($\alpha$,
$\beta$ and $C$) for various methods was
assembled.{cite}`roemelt2009moessbauer` Usually an accuracy of better than
0.10 mm s$^{-1}$ can be achieved for DFT with reasonably sized basis
sets.

## Quadrupole splitting
```{index} Quadrupole Splitting
```

The quadrupole splitting arises from the interaction of the nuclear
quadrupole moment of the excited state with the electric field gradient
at the nucleus. The former is related to the non-spherical charge
distribution in the excited state. As such it is extremely sensitive to
the coordination environment and the geometry of the complex.

The quadrupole splitting is proportional to the largest component of the
**electric field gradient** (EFG) tensor at the nucleus and can be
calculated using the formula:

$$\Delta E_\mathrm{Q} = \frac{1}{2}eQV_{zz} \left( 1+\frac{\eta^2}{3} \right)^{\frac{1}{2} }
$$ (eqn:MB_quadrupole_splitting)

where $e$ is the electrical charge of an electron and $Q$ is the nuclear
quadrupole moment of Fe (approximately 0.16 barns). $V_{xx}$, $V_{yy}$
and $V_{zz}$ are the electric field gradient tensors and $\eta$, defined
as

$$\eta = \left| \frac{V_{xx} - V_{yy} }{V_{zz} } \right|$$ (eqn:MB_eta)

is the asymmetry parameter in a coordinate system chosen such that
$|V_{zz}| \geq |V_{yy}| \geq |V_{xx}|$.

The electric field gradient tensor is closely related to the dipole
contribution to the hyperfine coupling. The main differences are that
the electron instead of the spin density enters its calculation and that
it contains a nuclear contribution due to the surrounding nuclei. It is
calculated from

$$\begin{array}{l}
 V_{\mu \nu } \left( N \right)=-\sum\limits_{kl} { P_{kl} } \left\langle {\phi_{k} \left|{ r_{N}^{-5} \left({ 3\vec{{r} }_{N\mu } \vec{{r} }_{N\nu }
-\delta_{\mu \nu } r_{N}^{2} } \right)} \right|\phi_{l} } \right\rangle\\
\hspace{1.5cm}
+\sum\limits_{A\ne
N} { Z_{A} \vec{{R} }_{AN}^{-5} \left({ 3\vec{{R} }_{AN\mu } \vec{{R} }_{AN\nu }
-\delta_{\mu \nu } R_{AN}^{2} } \right)} \\
 \end{array}
$$ (eqn:248)

with $Z_{A}$ as the nuclear charge of nucleus $A$ and $\vec{{R} }_{AN}$
as a vector of magnitude $R_{AN}$ that points from nucleus $A$ to
nucleus $N$. $\mathrm{\mathbf{P} }$ is the first order density matrix.

## Basic usage

An example of how to calculate the electron density and quadrupole
splitting of an iron center is as follows:

```orca
%eprnmr
  nuclei = all Fe {fgrad, rho}
end
```

If a basis set with tight functions such as the CP(PPP) is employed, one might have to
increase the radial integration accuracy for the iron atom. From ORCA
5.0, this is considered during grid construction and the defaults should
work very well. However for very problematic cases it can be increased
by controlling the ```SPECIALGRIDINTACC``` flag under ```%METHOD``` (see Sec.
{ref}`sec:essentialelements.numericalintegration.radgrid` for details).

The output file should contain the following lines, where you obtain the
calculated quadrupole splitting directly and the RHO(0) value (the
electron density at the iron nucleus). To obtain the isomer shift one
has to insert the RHO(0) value into the appropriate linear equation (Eq.
{eq}`eqn:MB_isomer_shift`).

```orca
Moessbauer quadrupole splitting parameter (proper coordinate system)
e**2qQ  = -0.406 MHz = -0.035 mm/s
eta     = 0.871
Delta-EQ=(1/2{e**2qQ}*sqrt(1+1/3*eta**2) = -0.227 MHz = -0.020 mm/s
RHO(0)=  11581.352209571 a.u.**-3   # the electron density at the Fe nucleus.
```

:::{Note}
-   Following the same procedure, Mössbauer parameters can be computed
    with the CASSCF wavefunction. In case of a state-averaged CASSCF
    calculation, the averaged density is used in the subsequent
    Mössbauer calculation.
:::

## Keywords
```{index} Mössbauer Spectroscopy Keywords
```

All properties tied to a given nucleus in the molecule (NMR shielding,
hyperfine coupling, quadrupolar coupling) share a common input syntax.
This syntax consists of a selection (the nuclei for which you want to do something) and
a list of actions you want the program to take for these nuclei inside curly brackets.
A complete list of possible keywords for the eprnmr module can be
found in {ref}`sec:spectroscopyproperties.properties.eprnmr`.
It's best explained on an example. The following

```orca
%eprnmr
  nuclei = all O { aiso, adip, fgrad, shift, ist=17 }
end
```

would select all oxygen atoms in the molecule, pick the $^{17}O$ isotope, and request
isotropic + spin-dipolar hyperfine couplings, the electric field gradient, and NMR
shielding to be calculated for them.

:::{warning}
All nuclei specified on one line will be assigned with the same isotopic mass (and
other parameters)!
:::


:::{raw} latex
\begingroup
\footnotesize
:::

:::{tabularcolumns} \Y{0.2}\Y{0.3}\Y{0.3}\Y{0.2}
:::
(tab:spectroscopyproperties.moessbauer.keywords.block)=
:::{flat-table} `%eprnmr` block input keywords relevant for Mössbauer calculations
:header-rows: 1
:class: longtable
:class: footnotesize

* - Keyword
  - Selection
  - What to do
  - Description
* - `nuclei`
  - `all <type>`
  - 
  - Selects all nuclei of element `<type>`
* - 
  - `i1,i2,i3...`
  - 
  - Selects atoms `i1`, `i2`, `i3`... (starts at 1!)
* - 
  - 
  - `{ rho }`
  - Calculates density at nucleus for selection
* - 
  - 
  - `{ fgrad }`
  - Calculates EFG for selection
* - 
  - 
  - `{ ist=<N> }`
  - Selects isotope `<N>` for selection
* - 
  - 
  - `{ QQQ=<N> }`
  - Sets quadrupole moment to `<N>` for selection
* - 
  - 
  - `{ III=<N> }`
  - Sets nuclear spin to `<N>` for selection
* - 
  - 
  - `{ fgrad, rho, ist=57 }`
  - Example requesting multiple actions for selection
:::

:::{raw} latex
\endgroup
:::
