```{index} DLPNO-STEOM-CCSD
```

(sec:spectroscopyproperties.dlpno-steom)=
# Excited States via DLPNO-STEOM-CCSD

The powerful coupled cluster methods can be used for excited states also. 
STEOM-CCSD is an improvement over the costly EOM-CCSD method which allows
a lower computational scaling for calculating excitation energies. The DLPNO 
approximation on the orbital space makes the theory even more compact by
further optimizing the computational cost. 
For general description, please read {ref}`sec:spectroscopyproperties.steom`.


(sec:spectroscopyproperties.dlpno-steom-dressing.general)=
## PNO dressing (experimental keyword) 

In STEOM-DLPNO-CCSD method most of the steps are done using the powerful
PNO approximation except the last one corresponding to the STEOM-CCSD
calculation itself. In the canonical version of the dressing (default in
ORCA) all the amplitudes previously computed at the PNO level are
recanonicalized which increases the calculation cost.PNO dressing uses
some of the PNO intermediates to reduce the dressing time. It has
however no effect on the storage size.

Using this PNO dressing will reduce the calculation timing but at a
reduce accuracy for the excitation energies. We thus recommend this
option only for specific large systems (\>2500 basis functions).

The keyword $\textbf{DirectDressSTEOM}$ is set to true enable this option.

(sec:spectroscopyproperties.dlpno-steom-keyword.general)=
## Keywords from STEOM-CCSD

Most of the keywords from STEOM-CCSD can be used within the DLPNO
version. More information on the
{ref}`sec:spectroscopyproperties.steom` section.

## Example

We would recommend this input for standard organic molecules. Formaldehyde 
is used as an example with def2-TZVP basis set.

As a general guideline we will discuss some of the keywords used there:

```{literalinclude} ../../orca_working_input/C05S09_165.inp
:language: orca
```

## Tips and Tricks

:::{important}
 For DLPNO calculations we need at least one auxiliary basis set. Therefore
 we have used def2-TZVP/C def2/J for this input. Without using explicit auxiliary
basis sets, a generic keyword "AutoAux" can also be used. 
:::

In that case, the first line of the same input would look like
```orca
! STEOM-DLPNO-CCSD def2-TZVP AutoAux TightSCF
```

:::{note}
DLPNO-STEOM-CCSD is not yet available for UHF wavefunctions. Therefore
open shell calculations are currently not possible.
:::

- TIGHTSCF is a must for any CCSD calculation.

- We will recommend using TIGHTPNO for all molecules as it is not a lot
more expensive and helps achieving a better convergence.

- The OTHRESH, VTHRESH and TCutPNOSingles keywords help with converging
the calculations, increasing the percentage active of each root. In
contrary to standard STEOM-CCSD, we would acknowledge that the roots are
converged when the percentage active character is at least 96%. Of
course you have to check that the amplitude and orbitals associated with
the excitation are correct (and what you expect). Tightening the 3
keywords mentioned above will increase this percentage active character. The
most important being the TCutPNOSingles one. Be careful, the
computational cost increases exponentially when thresholds are tightened. 
In most cases $10^{-12}$ or $5\times 10^{-12}$ should be enough. For OTHRESH and
VTHRESH you should not go below $10^{-3}$, as the benefits are not so
obvious. A trick to achieve a better convergence is to play with the number
of roots. It is often not necessary to compute a lot of roots if you are
only interested in the first 3 for example. If some high energy roots
have some low percentage active character, removing them can help for
the convergence of other roots.

- As shown in the related paper{cite}`Ghosh2020`, the STEOM density with the
L2term is now the default for computing the excited state properties.

- The choice of the basis set can also speed up the calculation without
a significant loss of accuracy. For most organic molecules def2-TZVP(-f)
is enough. Trying def2-SVP is also a good idea for preliminary tests.

- The STEOM-CCSD excitation energies are very dependent from the
starting geometry. Geometries optimised with several DFT functional can
yield significant differences for the excitation energies (about 0.1
eV).

- It has happened that some roots were missing with the keyword
$\textbf{Dorootwise}$ set to true. Turning it off solved the issue but
this keyword should be on by default.
