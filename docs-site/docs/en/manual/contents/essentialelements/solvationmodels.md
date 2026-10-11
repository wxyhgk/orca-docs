

<a id="sec:essentialelements.solvationmodels"></a>
# Implicit Solvation

Implicit solvation models play an important role in quantum chemistry.
Without resorting to placing multiple solvation shells of solvent
molecules implicit solvent models are able to mimic the effect of a
specific solvent on the solute.

The implicit solvent models available in ORCA are

1.   C-PCM[barone1998,garcia_neese_gcs](../../bibliography.md) : The Conductor-like Continuum Polarization Model

2.   SMD[marenich2009](../../bibliography.md) : The Solvation Model based on Density

3.   OpenCOSMO-RS[gerlachcosmors2022](../../bibliography.md)  : Interface to the open source implementation of the COSMO-RS model

4.   ALPB/ddCOSMO/CPCM-X     : The solvation models available in XTB

Regarding C-PCM and SMD, they are natively implemented in ORCA. With these models, various types of calculations can be performed
using a polarizable continuum with a realistic van der Waals cavity as summarized below:

-   Energies of molecules in solution with a finite dielectric constant
    $\varepsilon$ at the HF and DFT level, as well as for post-HF methods.

-   Optimization of molecular structures in solution using HF or any DFT
    method with analytic gradients.

-   Calculation of vibrational frequencies using the analytic Hessian
    for HF or any DFT method, provided that the same calculation is
    available in vacuum.

-   Calculation of solvent effects on response properties like
    polarizabilities through coupled-perturbed SCF theory. For magnetic
    response properties, such as the g-tensor, the C-PCM response
    vanishes.

-   Calculations of solvent shifts on transition energies using the
    time-dependent DFT or CIS method. The refractive index of the solvent
    needs to be provided in addition to the dielectric constant.

-   First order perturbation estimate of solvent effects on state and
    transition energies in multireference perturbation and
    configuration-interaction calculations.

A detailed overview of the  available implicit solvation methods and their usage is provided in Sections
[cpcm.detailed](#sec:essentialelements.solvationmodels.cpcm.detailed), [smd.detailed](#sec:essentialelements.solvationmodels.smd.detailed),
[solvationmodels.opencosmors](#sec:essentialelements.solvationmodels.opencosmors) , [semiempirical.xtb](../modelchemistries/semiempirical.md#sec:modelchemistries.semiempirical.xtb), and [oniom](../multiscalesimulations/qmmm-molecules.md#sec:oniom).

<a id="sec:essentialelements.solvationmodels.cpcm.detailed"></a>
## The Conductor-like Polarizable Continuum Model (C-PCM)

The conductor-like polarizable continuum model (C-PCM) is an
implementation of the conductor-like apparent surface charge methods. In
these models the solute is placed in a cavity of roughly molecular
shape. The solvent reaction field is described by apparent polarization
charges on the cavity surface, which are in turn determined by the
solute. These charges can be treated as punctual (point charges) or be
modelled as spherical Gaussians [york_gauss](../../bibliography.md). The cavity in ORCA is
constructed differently depending on how the charges are treated. In the
case of using point charges, the cavity is generated through the
GEPOL[gepol1,gepol2,gepol3](../../bibliography.md) algorithm, either as solvent-excluding
surface (SES), or solvent-accessible surface (SAS). When Gaussian
charges are considered, the user can choose between a scaled vdW surface
or the GEPOL SES, and the charge positions are determined following a
Lebedev quadrature approach. This scheme is known as Gaussian Charge
Scheme[garcia_neese_gcs](../../bibliography.md) and more details on how to use it are given in
Section [solvationmodels.gaussian_charge](#sec:essentialelements.solvationmodels.gaussian_charge).

Within C-PCM the molecular Hamiltonian of the isolated system is perturbed by
the solvent:

$$
\hat{H} = \hat{H}^0 + \hat{V}
$$

where $\hat{H}^0$ is the Hamiltonian of the isolated molecule, whereas
$\hat{V}$ describes the solute -- solvent interactions. The SCF
procedure leads to the variational minimization of the free energy of
the solute, $G$:

$$
G = \left\langle\Psi \left| \hat{H}^0 \right| \Psi \right\rangle+
\frac{1}{2} \left\langle\Psi \left| \hat{V} \right| \Psi \right\rangle
$$

Using the conductor-like boundary condition the electrostatic potential
can be determined by

$$
V(\vec{r}) + \sum_i^{N_q} V_{q_i} (\vec{r}) = 0
$$

where $V$ and $V_{q_i}$ are the electrostatic potential due to the
solute and to the polarization charges, $\vec{r}$ is a point on the
cavity surface, and $N_q$ is the total number of solvation charges. The
vector of polarization charge can then be determined by

$$
AQ = -V\qquad \text{(eqn:feps)}
$$

where the vector $V$ contains the electrostatic potential due
to the solute at the position of the charges. The elements of the matrix
$A$ have a different functional form depending on how the
charges are treated. If we use point charges:

$$
A_{ii} = 1.07 \sqrt{ \frac{4\pi}{S_i} }
$$
$$
A_{ij} = \frac{1}{r_{ij} }\qquad \text{(eq:Aijp)}
$$

in which $S_i$ is the area of the surface element $i$, and
$r_{ij}=\left| \vec{r}_i - \vec{r}_j \right|$. When Gaussian charges are
considered:

$$
A_{ii} = \frac{\zeta_i\sqrt{2/\pi} }{F_i}
$$
$$
A_{ij} = \frac{\mathrm{erf}\left(\zeta_{ij}r_{ij}\right)}{r_{ij} }
$$

Here, $\zeta_i$ is the exponent of the Gaussian charge $i$ ($i$ belongs
to sphere $I$). This quantity is calculated as
$\zeta_i=\zeta/(R_I\sqrt{w_i})$, where $R_I$ is the radius of sphere
$I$, $w_i$ is the weight of the Lebedev point $i$, and $\zeta$ is a
width parameter optimized for each particular Lebedev grid
[york_gauss](../../bibliography.md). On the other hand,
$\zeta_{ij}=\zeta_i\zeta_j/\sqrt{\zeta_i^2+\zeta_j^2}$. The function
$F_i$, known as switching function, measures the contribution of the
Gaussian charge $i$ to the solvation energy. This function is calculated
as

$$
F_i=\prod^{\mathrm{atoms} }_{J,i\notin J}g(\vec{r}_i,\vec{R}_J)
$$

where $g(\vec{r}_i,\vec{R}_J)$ is the elementary switching function. In
ORCA we use the improved Switching/Gaussian (ISWIG) function for
$g(\vec{r}_i,\vec{R}_J)$ proposed in ref. [lange2010](../../bibliography.md):

$$
g(\vec{r}_i,\vec{R}_J)=1-\frac{1}{2}\left\{\mathrm{erf}\left[\zeta_i\left(R_J-r_{iJ}\right)\right]+\mathrm{erf}\left[\zeta_i\left(R_J+r_{iJ}\right)\right]\right\}
$$

If $g(\vec{r}_i,\vec{R}_J)<10^{-7}$ the value of $g$ is set equal to 0.
If we consider a solvent with a dielectric constant $\varepsilon$, eq.
[Eq](#eqn:feps)
reads as

$$
AQ = -f(\varepsilon)V\qquad \text{(eq_cpcm)}
$$

where $f(\varepsilon)=(\varepsilon - 1)/(\varepsilon + x)$ is a scaling
function, and $x$ is in the range 0-2. In C-PCM $x$ is equal to 0.

The C-PCM model can be used via

```orca
! CPCM(solvent)
```

where `solvent` is one of the available solvents in [table:list-solvents](#table:list-solvents)

<a id="table:list-solvents"></a>
!!! note "List of available solvents for the C-PCM, SMD, openCOSMO-RS, and ALPB in ORCA. The data for the dielectric constant used within C-PCM is that at 293.15,[crcchemistry2014](../../bibliography.md) except for ammonia, which has a boiling point of 239.81 K. For the rest of solvation models, see the corresponding sources.[marenich2009](../../bibliography.md)[cpcmx2023](../../bibliography.md) Notice that ALPB is only available in the context of XTB calculations. The list of solvents for ddCOSMO and CPCM-X is, on the other hand, provided in [tab:modelchemistries.semiempirical.xtb.solvation.solvents](#tab:modelchemistries.semiempirical.xtb.solvation.solvents)."
    |  Solvent             |   C-PCM     |   SMD      |   COSMO-RS  |  ALPB     |
    |:--------------------:|:-----------:|:----------:|:---------:|:---------:|
    | 1,1,1-trichloroethane            | X | X |  |  |
    | 1,1,2-trichloroethane            | X | X |  |  |
    | 1,2,4-trimethylbenzene           | X | X |  |  |
    | 1,2-dibromoethane                | X | X | X |  |
    | 1,2-dichloroethane               | X | X | X |  |
    | 1,2-ethanediol                   | X | X |  |  |
    | 1,4-dioxane / dioxane            | X | X | X | X |
    | 1-bromo-2-methylpropane          | X | X |  |  |
    | 1-bromooctane / bromooctane      | X | X | X |  |
    | 1-bromopentane                   | X | X |  |  |
    | 1-bromopropane                   | X | X |  |  |
    | 1-butanol / butanol              | X | X | X |  |
    | 1-chlorohexane / chlorohexane    | X | X | X |  |
    | 1-chloropentane                  | X | X |  |  |
    | 1-chloropropane                  | X | X |  |  |
    | 1-decanol / decanol              | X | X | X |  |
    | 1-fluorooctane                   | X | X | X |  |
    | 1-heptanol / heptanol            | X | X | X |  |
    | 1-hexanol / hexanol              | X | X | X |  |
    | 1-hexene                         | X | X |  |  |
    | 1-hexyne                         | X | X |  |  |
    | 1-iodobutane                     | X | X |  |  |
    | 1-iodohexadecane / hexadecyliodide| X | X | X |  |
    | 1-iodopentane                    | X | X |  |  |
    | 1-iodopropane                    | X | X |  |  |
    | 1-nitropropane                   | X | X |  |  |
    | 1-nonanol / nonanol              | X | X | X |  |
    | 1-octanol / octanol              | X | X | X | X |
    | 1-pentanol / pentanol            | X | X | X |  |
    | 1-pentene                        | X | X |  |  |
    | 1-propanol / propanol            | X | X | X |  |
    | 2,2,2-trifluoroethanol           | X | X |  |  |
    | 2,2,4-trimethylpentane / isooctane | X | X | X |  |
    | 2,4-dimethylpentane              | X | X |  |  |
    | 2,4-dimethylpyridine             | X | X |  |  |
    | 2,6-dimethylpyridine             | X | X | X |  |
    | 2-bromopropane                   | X | X |  |  |
    | 2-butanol / secbutanol           | X | X | X |  |
    | 2-chlorobutane                   | X | X |  |  |
    | 2-heptanone                      | X | X |  |  |
    | 2-hexanone                       | X | X |  |  |
    | 2-methoxyethanol / methoxyethanol| X | X | X |  |
    | 2-methyl-1-propanol / isobutanol | X | X | X |  |
    | 2-methyl-2-propanol              | X | X |  |  |
    | 2-methylpentane                  | X | X |  |  |
    | 2-methylpyridine / 2methylpyridine| X | X | X |  |
    | 2-nitropropane                   | X | X |  |  |
    | 2-octanone                       | X | X |  |  |
    | 2-pentanone                      | X | X |  |  |
    | 2-propanol / isopropanol         | X | X | X |  |
    | 2-propen-1-ol                    | X | X |  |  |
    | e-2-pentene                      | X | X |  |  |
    | 3-methylpyridine                 | X | X |  |  |
    | 3-pentanone                      | X | X |  |  |
    | 4-heptanone                      | X | X |  |  |
    | 4-methyl-2-pentanone / 4methyl2pentanone| X | X | X |  |
    | 4-methylpyridine                 | X | X |  |  |
    | 5-nonanone                       | X | X |  |  |
    | acetic acid / aceticacid         | X | X | X |  |
    | acetone                          | X | X | X | X |
    | acetonitrile / mecn / ch3cn      | X | X | X | X |
    | acetophenone                     | X | X | X |  |
    | ammonia                          | X |  | X |  |
    | aniline                          | X | X | X | X |
    | anisole                          | X | X | X |  |
    | benzaldehyde                     | X | X | X | X |
    | benzene                          | X | X | X | X |
    | benzonitrile                     | X | X | X |  |
    | benzyl alcohol / benzylalcohol   | X | X | X |  |
    | bromobenzene                     | X | X | X |  |
    | bromoethane                      | X | X | X |  |
    | bromoform                        | X | X | X |  |
    | butanal                          | X | X |  |  |
    | butanoic acid                    | X | X |  |  |
    | butanone                         | X | X | X |  |
    | butanonitrile                    | X | X |  |  |
    | butyl ethanoate / butyl acetate / butylacetate| X | X | X |  |
    | butylamine                       | X | X |  |  |
    | n-butylbenzene / butylbenzene    | X | X | X |  |
    | sec-butylbenzene / secbutylbenzene| X | X | X |  |
    | tert-butylbenzene / tbutylbenzene| X | X | X |  |
    | carbon disulfide / carbondisulfide / cs2| X | X | X | X |
    | carbon tetrachloride / ccl4      | X | X | X |  |
    | chlorobenzene                    | X | X | X |  |
    | chloroform / chcl3               | X | X | X | X |
    | a-chlorotoluene                  | X | X |  |  |
    | o-chlorotoluene                  | X | X |  |  |
    | conductor                        | X |  |  |  |
    | m-cresol / mcresol               | X | X | X |  |
    | o-cresol                         | X | X |  |  |
    | cyclohexane                      | X | X | X |  |
    | cyclohexanone                    | X | X | X |  |
    | cyclopentane                     | X | X |  |  |
    | cyclopentanol                    | X | X |  |  |
    | cyclopentanone                   | X | X |  |  |
    | decalin                          | X | X | X |  |
    | cis-decalin                      | X | X |  |  |
    | n-decane / decane                | X | X | X |  |
    | dibromomethane                   | X | X |  |  |
    | dibutylether                     | X | X | X |  |
    | o-dichlorobenzene / odichlorobenzene| X | X | X |
    | e-1,2-dichloroethene             | X | X |  |  |
    | z-1,2-dichloroethene             | X | X |  |  |
    | dichloromethane / ch2cl2 / dcm   | X | X | X | X |
    | diethyl ether / diethylether     | X | X | X | X |
    | diethyl sulfide                  | X | X |  |  |
    | diethylamine                     | X | X |  |  |
    | diiodomethane                    | X | X |  |  |
    | diisopropyl ether / diisopropylether| X | X | X |  |
    | cis-1,2-dimethylcyclohexane      | X | X |  |  |
    | dimethyl disulfide               | X | X |  |  |
    | n,n-dimethylacetamide / dimethylacetamide| X | X | X |  |
    | n,n-dimethylformamide / dimethylformamide / dmf| X | X | X | X |
    | dimethylsulfoxide / dmso         | X | X | X | X |
    | diphenylether                    | X | X | X |  |
    | dipropylamine                    | X | X |  |  |
    | n-dodecane / dodecane            | X | X | X |  |
    | ethanethiol                      | X | X |  |  |
    | ethanol                          | X | X | X | X |
    | ethyl acetate / ethylacetate / ethanoate| X | X | X | X |
    | ethyl methanoate                 | X | X |  |  |
    | ethyl phenyl ether / ethoxybenzene| X | X | X |  |
    | ethylbenzene                     | X | X | X |  |
    | fluorobenzene                    | X | X | X |  |
    | formamide                        | X | X |  |  |
    | formic acid                      | X | X |  |  |
    | furan / furane                   |  |  | X | X |
    | n-heptane / heptane              | X | X | X |  |
    | n-hexadecane / hexadecane        | X | X | X | X |
    | n-hexane / hexane                | X | X | X | X |
    | hexanoic acid                    | X | X |  |  |
    | iodobenzene                      | X | X | X |  |
    | iodoethane                       | X | X |  |  |
    | iodomethane                      | X | X |  |  |
    | isopropylbenzene                 | X | X | X |  |
    | p-isopropyltoluene / isopropyltoluene| X | X |  |  |
    | mesitylene                       | X | X | X |  |
    | methanol                         | X | X | X | X |
    | methyl benzoate                  | X | X |  |  |
    | methyl butanoate                 | X | X |  |  |
    | methyl ethanoate                 | X | X |  |  |
    | methyl methanoate                | X | X |  |  |
    | methyl propanoate                | X | X |  |  |
    | n-methylaniline                  | X | X |  |  |
    | methylcyclohexane                | X | X |  |  |
    | n-methylformamide / methylformamide | X | X | X |  |
    | nitrobenzene / phno2             | X | X | X |  |
    | nitroethane                      | X | X | X |  |
    | nitromethane / meno2             | X | X | X | X |
    | o-nitrotoluene / onitrotoluene   | X | X |  |  |
    | n-nonane / nonane                | X | X | X |  |
    | n-octane / octane                | X | X | X |  |
    | n-pentadecane / pentadecane      | X | X | X |  |
    | octanol(wet) / wetoctanol / woctanol|  |  |  | X |
    | pentanal                         | X | X |  |  |
    | n-pentane / pentane              | X | X | X |  |
    | pentanoic acid                   | X | X |  |  |
    | pentyl ethanoate                 | X | X |  |  |
    | pentylamine                      | X | X |  |  |
    | perfluorobenzene / hexafluorobenzene | X | X | X |  |
    | phenol                           | X |   | X | X |
    | propanal                         | X | X |  |  |
    | propanoic acid                   | X | X |  |  |
    | propanonitrile                   | X | X |  |  |
    | propyl ethanoate                 | X | X |  |  |
    | propylamine                      | X | X |  |  |
    | pyridine                         | X | X | X |  |
    | tetrachloroethene / c2cl4        | X | X | X |  |
    | tetrahydrofuran / thf            | X | X | X | X |
    | tetrahydrothiophene-s,s-dioxide /| X | X |  |  |
    | / tetrahydrothiophenedioxide / sulfolane| X | X |  |  |
    | tetralin                         | X | X | X |  |
    | thiophene                        | X | X |  |  |
    | thiophenol                       | X | X |  |  |
    | toluene                          | X | X | X | X |
    | trans-decalin                    | X | X |  |  |
    | tributylphosphate                | X | X | X |  |
    | trichloroethene                  | X | X |  |  |
    | triethylamine                    | X | X | X |  |
    | n-undecane / undecane            | X | X | X |  |
    | water / h2o                      | X | X | X | X |
    | xylene                           | X | X |  |  |
    | m-xylene                         | X | X |  |  |
    | o-xylene                         | X | X |  |  |
    | p-xylene                         | X | X |  |  |

The parameters related to each implicit solvation method, as well as to the solvents can be more accurately defined using the `%cpcm` block
input. A complete list of the available options are described in [keyword-list.detailed](#sec:essentialelements.solvationmodels.keyword-list.detailed).

The type of cavites surrounding the solute and how the solvation charges are treated in ORCA
is explained in subsections [solvationmodels.gaussian_charge](#sec:essentialelements.solvationmodels.gaussian_charge), and
[solvationmodels.point_charge](#sec:essentialelements.solvationmodels.point_charge).
ORCA supports two types of solvation charge schemes: (i) the point
charge scheme, (ii) the Gaussian charge scheme. The default solvation scheme
from ORCA 5.0 on is the Gaussian charge scheme with a vdW-type cavity
(`surfacetype vdw_gaussian`). Older ORCA versions considered
`surfacetype gepol_ses` and the point charge scheme as defaults. So,
if one wants to reproduce the results obtained with ORCA versions older
than ORCA 5.0, please use the tag `surfacetype gepol_ses` in the
`%cpcm` block.

The different charge schemes are described in the subsections
[solvationmodels.gaussian_charge](#sec:essentialelements.solvationmodels.gaussian_charge), and
[solvationmodels.point_charge](#sec:essentialelements.solvationmodels.point_charge).
The availability of the analytical gradient and Hessian for the
different combinations of charge scheme and surface is shown in Table
[table:CPCM-features](#table:CPCM-features).

<a id="table:CPCM-features"></a>
!!! note "Available type of gradients and Hessians within the C-PCM in ORCA. The tag "YES" means that the feature is implemented, and "NO" that it isn't. For clarity, we denote by "\*" the default scheme in ORCA (`surfacetype vdw_gaussian`)."
    |                      |             |            |           |            |           |
    |:--------------------:|:-----------:|:----------:|:---------:|:----------:|:---------:|
    |    `surfacetype`     | Charge type |  Gradient  |           |  Hessian   |           |
    |                      |             | Analytical | Numerical | Analytical | Numerical |
    |     `gepol_ses`      |    Point    |    Yes     |    Yes    |    Yes     |    Yes    |
    |     `gepol_sas`      |    Point    |    Yes     |    Yes    |    Yes     |    Yes    |
    |   `vdw_gaussian^*`   |  Gaussian   |    Yes     |    Yes    |    Yes     |    Yes    |
    | `gepol_ses_gaussian` |  Gaussian   |     No     |    Yes    |     No     |    Yes    |

**Note 1:** If the user wants to turn off the C-PCM, one has to write the
following tag in the simple input:

```orca
! NOCPCM
```

This is needed, for instance, in the context of concatenated
calculations using the `$new_job` feature, where the previous
calculation involved solvation, but one wants to turn it off for the
next one.

**Note 2:** As stated above, the default for C-PCM in ORCA is the Gaussian charge scheme
with a vdW-type cavity. The implementation is done following ref. [garcia_neese_gcs](../../bibliography.md). Hence,
if C-PCM is used in ORCA calculations, one must cite this paper together with ref. [barone1998](../../bibliography.md).
Ref. [garcia_neese_gcs](../../bibliography.md) must also be cited if SMD, or openCOSMO-RS are requested, since these
type of calculations rely on C-PCM.
<a id="sec:essentialelements.solvationmodels.gaussian_charge"></a>
### Use of the Gaussian Charge Scheme

The Gaussian charge scheme avoids the Coulomb singularity present in
conventional point charge surface element models. This approach, when
applied together with a switching function, results in a smooth
solvation potential and, more importantly, on smooth derivatives of this
quantity with respect to external perturbations. Then, it is highly
recommended to adopt this approach within the C-PCM. The Gaussian charge
scheme can be used with two types of solute cavity surfaces: (1) a
scaled vdW surface, (2) a solvent-excluded surface (SES). To assign the
radii for the different atoms we follow the scheme proposed in ref.
[lange2010](../../bibliography.md). That is, we use Bondi radii [radii_1](../../bibliography.md) for all elements,
except for hydrogen where we adopt 1.1 Å. For 16 of the main-group
elements in the periodic table, where Bondi's radii are not defined, we
adopt the radii proposed in ref. [radii_2](../../bibliography.md) by Mantina et al. This is
the case for elements: Be, B, Al, Ca, Ge, Rb, Sr, Sb, Cs, Ba, Bi, Po,
At, Rn, Fr, Ra. For the elements that are not covered neither by Bondi
nor by Mantina, we consider a radius of 2 Å.

-   **Scaled vdW cavity**

The Gaussian charge scheme with a scaled vdW-type cavity is now the
default in ORCA, so one just needs to add the C-PCM tag in the `%cpcm`
block in the input file. That would correspond to (although the user
does not need to write that, as it is internally processed by ORCA):

```orca
%cpcm
  surfacetype vdw_gaussian
end
```

In this case, the radius $R_I$ of atom $I$ for the scaled vdW cavity is
calculated as

$$
R_I=f_{scal}R_I^{\mathrm{vdW} }
$$

where $R_I^{\mathrm{vdW} }$ is the vdW radius of atom $I$ and $f_{scal}$
is a scaling factor. This parameter is by default equal to 1.2, as
suggested in ref. [lange2010](../../bibliography.md). However, the user can modify its value
through the `scale_gauss` tag in the `%cpcm` block in the input file.
The number of C-PCM charges per atom is such that we have an approximate
density of 5.0 charges/Å$^2$ on the surface of the cavity. This number
corresponds approximately to 110 points on a hydrogen atom
(110/$(4\pi\times 1.32^2)\approx 5.0$Å$^{-2}$). ORCA will choose then
different levels of discretization (Lebedev grids) depending on the
radii of the atoms. This scheme is called isodensity scheme. The threshold
for the number of charges per unit of area on hydrogens and non-hydrogen
atoms can be specified by the user via `thresh_h` and `thresh_noth`, respectively.
Alternatively, the user can request a fixed number
of Lebedev points per sphere in the cavity (independent of the radius of
the sphere). This can be done via the `num_leb` tag. This parameter can
adopt the following values: 50, 110, 194, 302, 434, 590, 770, 974, and
1202. ORCA versions older than ORCA 6.0 use this last scheme.
The analytical gradient, as well as the analytical Hessian are available
for this solvation method.
-   **Solvent-excluded surface**
The GEPOL-generated SES can be used together with the Gaussian charge
scheme. In this case, the Gaussian charges are not only placed on the
surface of the atomic spheres but also on the surface of the new spheres
generated through the GEPOL algorithm. To use this approach we should
modify the ORCA input file as follows
```orca
%cpcm
  surfacetype gepol_ses_gaussian
end
```
The SES is in general recommended when the solute is explicitly solvated
by few solvation layers. In this case, the additional GEPOL spheres
prevent the solvent to fill the space between explicit solvent molecules
or between those molecules and the solute. The radius of the solvent
sphere that rolls over the solute vdW-type surface to generate the SES
is controlled by the keyword `rsolv`. This radius has a default
value of 1.30 Å, but the user can change it by specifying another value
for `rsolv` in the `%cpcm` block. The minimum radius for an added
GEPOL sphere is controlled by `rmin`.
Neither the analytical gradient nor the analytical Hessian are available
for this strategy. They should be computed numerically. Due to the
interdependency between GEPOL spheres and the atoms present in our
system, the analytical gradient computed using the SES does not converge
as smooth as compared to that using the vdW-type cavity (see ref.
[garcia_neese_gcs](../../bibliography.md)) and can lead to wrong minima. The Hessian is
affected in the same way. Then, ORCA 6.0 does not support anymore the
analytical gradient/Hessian for such surface to prevent inaccurate
results.
<a id="sec:essentialelements.solvationmodels.point_charge"></a>
### Use of the Point Charge Scheme
Within this scheme, the solvation charges are treated as punctual and no
switching function is used to accept/discard charges in the intersection
between the spheres that form the solute cavity. These two facts lead to
a discontinuous potential energy surface (numerical instabilities in the
SCF energy and its derivatives). Then, the point charge scheme is not
recommended within the C-PCM. If the user still wants to use this charge
scheme it can be used together with two different type of surfaces for
the solute cavity: (1) the SES, and (2) the SAS.
-   **Solvent-excluded surface**
In the same way as for the Gaussian charge scheme with the SES, this
surface is generated for the point charge scheme through the GEPOL
algorithm. However, while for the case of
`surfacetype gepol_ses_gaussian`, the surface is discretized using
Lebedev-type grids, in the point charge scheme, the surface is divided
in spherical triangles called "tesserae". The level of tesselation is
controlled by the tag `ndiv`. The radii used for the solute atoms in
order to construct the GEPOL cavity are those optimized for the COSMO-RS
model[cosmors_radii](../../bibliography.md) for H, C, N, O, F, S, Cl, Br, and I, while for the
rest of elements scaled Bondi radii are used.
In order to use the point charge scheme with the SES, we should add the
following tag in the `%cpcm` block:
```orca
%cpcm
  surfacetype gepol_ses
end
```
-   **Solvent-accessible surface**
Here, the surface of the solute cavity is generated by following the
center of a sphere with radius `rsolv` (representing the solvent
molecule) rolling over the surface of the vdW surface of the solute. The
discretization of the resulting surface is done via tesserae, as done
for the SES. In order to use the point charge scheme together with the
SAS, one should add the following tag in the `%cpcm` block:
```orca
%cpcm
  surfacetype gepol_sas
end
```
-   **How to circumvent the numerical instabilities in the point charge
    scheme**
Numerical instabilities are implicit in the point charge scheme due to
the "punctual" nature of the charges and to the fact that no switching
function is considered in the intersection between the spheres that form
the solute cavity. At the same time, there is no way to predict, in
advance if there will be discontinuities in the SCF energy and/or in its
derivatives. However, if the user still wants to use this charge scheme,
no matter with which type of surface (SES or SAS), there are two things
that one can try to minimize the aforementioned problems:
-   [**Change `ndiv`** ]{.underline}: The parameter `ndiv` controls
    the number of triangles per sphere in the solute cavity. By changing
    the number of triangles, it also changes the number of triangles in
    the intersection between spheres and, then, this can solve those
    situations where two point charges get too close making the elements
    $A_{ij}$ in eq [Eq](#eq:Aijp) to diverge (and the solvation charges to suddenly
    have very large values). However, this strategy can be a solution
    for a particular case, but will never ensure that for the same
    system with another geometry the discontinuities in the SCF energy
    do not show (as it does not prevent point charges to be too close
    from each other).
-   [**Increase `pmin`** ]{.underline}: This parameter removes those
    charges that are at a distance lower than `pmin` from each other.
    The default value for `pmin` is of 0.1 a.u. ($\approx 0.0529$ Å).
    Then, by incrasing `pmin` one removes all pairs of charges that are
    too close from each other in the intersection between the spheres.
    **Note:** Be careful when increasing `pmin`. Although this prevents
    sudden jumps in the SCF energy, it can lead to "biasing" the
    solute-solvent interaction, as one is removing a significant number
    of charges that represent the effect of the solvent.
### Calculation of the free energy of solvation within the C-PCM
The solvation free energy, $\Delta G_{solv}$, is defined as the free
energy of transfer of a solute from the gas phase to the condensed
phase. This quantity can be written as (see eq 27 in ref.
[garcia_neese_gcs](../../bibliography.md))

$$
\Delta G_{solv}=E_{solv}(\vec{R}_l,\vec{R}_v)+\Delta G_{el}+\Delta G_{cav}+\Delta G_{disp}\qquad \text{(eq_g_solv)}
$$

The first term, $E_{solv}(\vec{R}_v,\vec{R}_l)$, corresponds to the
difference between the liquid-phase expectation value of the gas-phase
Hamiltonian, $E(\vec{R}_l)$, and the gas-phase potential energy surface
$E(\vec{R}_v)$

$$
E_{solv}(\vec{R}_v,\vec{R}_l)=E(\vec{R}_l)-E(\vec{R}_v)
$$

The second term in eq [Eq](#eq_g_solv) accounts for the electronic-polarization
contribution to $\Delta G_{solv}$ and is calculated from the charges
spread over the surface of the solute cavity (vdW-type or the SES).
Finally, $\Delta G_{cav}$ is the cavitation energy, that is, the
reversible work required to create a cavity inside the bulk of the
solvent in order to accommodate the solute, while $\Delta G_{disp}$
accounts for the changes in the dispersion energy occuring when
solvating the solute. The sum of these last two terms correspond to the
non-electrostatic contribution, $\Delta G_{nel}$, to $\Delta G_{solv}$

$$
\Delta G_{nel}=\Delta G_{cav}+\Delta G_{disp}
$$

In ORCA, if a system is solvated within the C-PCM (defining
`!CPCM(solvent name)` in the input file, within either the point charge
scheme or the Gaussian charge scheme) there is no "non-electrostatic
solvation contribution" neither to the SCF energy, nor to its
derivatives. In order to have a rough idea of the value of
$\Delta G_{nel}$, one can estimate this quantity through empirical
equations available in the literature obtained from experimental data.
For instance, $\Delta G_{nel}$ can be estimated from the free energy of
hydration for linear-chain alkanes[truong1995](../../bibliography.md)

$$
\Delta G_{\text{nel} } = 1.321 + 0.0067639\times\mathrm{SASA}\qquad \text{(eq:delta_truong)}
$$

where SASA is the solvent-accessible surface area. However, although eq
[Eq](#eq:delta_truong) may give a good estimation of $\Delta G_{nel}$
for organic molecules in water, it is a bad approximation for
non-electrostatic solvation effects when considering solvents different
than water (as well as for many solutes in water). There are two
alternatives to this approximation that one can adopt in order to
include non-electrostatic solvation effects in ORCA calculations:

1.  The use of the SMD model in combination with the C-PCM (see section
    [smd.detailed](#sec:essentialelements.solvationmodels.smd.detailed)). This is
    the most adopted strategy within the QM community.

2.  The use of Gaussian charges to compute the electrostatic
    contribution to $\Delta G_{solv}$ together with an equation for
    $\Delta G_{\text{nel} }$ calculated from the contribution of the
    solute atoms to the SASA.[garcia_neese_gcs](../../bibliography.md)

Focusing on the second strategy, the cavitation energy, $\Delta G_{cav}$
is calculated through the equation proposed by Pierotti and
Claverie.[pierotti1976,claverie1978](../../bibliography.md) In this case, $\Delta G_{cav}$
is expanded in powers of the ratio $\overline{R }$ between the
radius of the solute sphere $R_I$ and that of the solvent spheres $R_S$.
Then, the cavitation energy for the solute sphere centered at atom $I$
reads as,

$$
\Delta G_{cav,I}=-\mathrm{ln}(1-y)+\left(\frac{3y}{1-y}\right)\overline{R }+\left[\frac{3y}{1-y}+\frac{9}{2}\left(\frac{y}{1-y}\right)^2\right]\overline{R }^2+\frac{yP}{\rho_Sk_BT}\overline{R }^3
$$

with $y=8\pi\rho_SR_S^3/6$, being $\rho_S$ the density of the solvent,
$\overline{R }=R_I/R_S$, $T$ the temperature and $P$ the
pressure. If we consider the solvent-accessible surface (SAS), then, the
total $\Delta G_{cav}$ is the sum of the $\Delta G_{cav,I}$ weighted by
a factor that depends on the exposed $\mathrm{SASA}_I$ of sphere $I$

$$
\Delta G_{cav}=\sum_{i=1}^{N_{\mathrm{sph} }}\frac{\mathrm{SASA}_I}{4\pi R_I^2}\Delta G_{cav,I}=\sum_{i=1}^{N_{el} }\frac{\mathrm{SASA}_i}{4\pi R_I^2}\Delta G_{cav,i}\qquad \text{(eq_g_cav)}
$$

Here, the summation over the total number of spheres
($N_{\mathrm{sph} }$) that conform the SAS is replaced by a summation
over the total number of surface elements ($N_{\mathrm{el} }$) in which
the SAS is divided into.

With respect to $\Delta G_{disp}$, this quantity is assumed to depend
linearly on the contribution of each surface element to the SASA

$$
\Delta G_{disp}=\sum_{i=1}^{N_{\mathrm{el} }}\sigma_I\mathrm{SASA}_i\qquad \text{(eq_g_disp)}
$$

Here, the factor $\sigma_I$ is the atomic surface tension of the sphere
$I$ to which the surface element $i$ belongs to.

This strategy, that considers eqs
[Eq](#eq_g_cav)
and [Eq](#eq_g_disp) to compute $\Delta G_{nel}$ assumes the use of
Gaussian charges for the calculation of $\Delta G_{el}$ in eq
[Eq](#eq_g_solv). When a vdW-type cavity is used to account for
electrostatic solvation effects, then the solvation approach is called
GVDW_nel, while when a SES-type cavity is used we refer to the solvation
approach as GSES_nel ("G" for Gaussian charges and "nel" because of the
inclusion of non-electrostatic solvation effects). Details on the
GVDW_nel and GSES_nel models can be found in ref. [garcia_neese_gcs](../../bibliography.md).

The GVDW_nel and GSES_nel models have been parametrized for solutes
containing H, C, N and O atoms in the following solvents: benzene,
chloroform, cyclohexane, octanol, toluene and water. The parameters for
the $\sigma_I$ atomic surface tensions in eq
[Eq](#eq_g_disp)
together with the radius of the solvent molecules $R_S$ used to generate
the SAS are provided in ref. [garcia_neese_gcs](../../bibliography.md). The use of the
GVDW_nel and GSES_nel is controlled by the string `cds_cpcm` to add in
the `%cpcm` block. This flag should be equal to 2 within these two
models (by default, when we use C-PCM together with the Gaussian Charge
Scheme without non-electrostatic solvation effects, `cds_cpcm` is equal
to 0). In order to calculate $\Delta G_{solv}$ for the GVDW_nel scheme
one has to do the following steps:

1.  Optimize the geometry of the solute (anisole in this case) in
    vacuum. For a DFT calculation at the B3LYP/def2-TZVP level of theory
    (with RIJCOSX), our input file would read like:

    ```orcainput
    ! B3LYP def2-TZVP D3BJ tightopt

    %maxcore 4000

    * xyz 0 1
    C   0.66588156410505    1.19833878437922    -0.02647672759883
    C   1.95470174000504    0.69483871574862    -0.01927812843331
    C   2.17893173780041   -0.68097630146538     0.00933914777704
    C   1.09270919891774   -1.54252176637089     0.03141990372830
    C  -0.21073409652496   -1.05179390481975     0.02471602253843
    C  -0.42517201252444    0.32533458015547    -0.00499572635290
    H   0.47565631823749    2.26336213776820    -0.05012843684387
    H   2.79210971512409    1.38085300778245    -0.03749594945361
    H   3.18771596563920   -1.07149825338966     0.01433233618265
    H   1.25061585302875   -2.61357041387417     0.05495238973649
    H  -1.03877793934640   -1.74453554370491     0.04346162651229
    O  -1.65366310927299    0.90979347913477    -0.01693978807213
    C  -2.79791686738707    0.07370821312998     0.01117694976431
    H  -2.83142307710305   -0.58944196707467    -0.85867919998175
    H  -3.65619850989594    0.74176224021803    -0.00958531946332
    H  -2.82883648080292   -0.53125300761732     0.92288089996024
    *
    ```

2.  Use the resulting structure (`anisole.xyz`) as input structure for
    the subsequent geometry optimization in solution. In this case, we
    consider water as the solvent. The input file looks like:

    ```orcainput
    ! B3LYP def2-TZVP D3BJ tightopt CPCM(Water)

    %cpcm
      cds_cpcm 2
    end

    %maxcore 4000

    * xyzfile 0 1 anisole.xyz

    ```

3.  Search for the `FINAL SINGLE POINT ENERGY` in the output file for
    the solvated system (we call it $E_s$):

    ```orca
    -------------------------   --------------------
    FINAL SINGLE POINT ENERGY      -346.723542928703
    -------------------------   --------------------
    ```

4.  Search for the `FINAL SINGLE POINT ENERGY` in the output file for
    the system in vacuum (we call it $E_0$):

    ```orca
    -------------------------   --------------------
    FINAL SINGLE POINT ENERGY      -346.719657761697
    -------------------------   --------------------

    ```

5.  Calculate $\Delta G_{solv}=E_s-E_0=-0.003885$ a.u. If we convert it
    to kcal/mol and round it to two decimal digits, we have
    $\Delta G_{solv}=-2.44$ kcal/mol. This quantity is in very good
    agreement with its experimental counterpart (-2.45
    kcal/mol[marenich2009](../../bibliography.md)).

6.  In case the user is interested in the value of $\Delta G_{nel}$,
    this quantity is printed in the `CPCM Solvation Model Properties`
    block:

    ```orca
    CPCM Solvation Model Properties:
    Surface-charge          :  -0.02580688416088
    Corrected charge        :   0.00000000000000
    Outlying charge corr.   :   0.00005046206545 Eh    0.00137 eV
    Free-energy (cav+disp)  :   0.00272597402638 Eh    0.07418 eV
    ```

Here, $\Delta G_{nel}$ corresponds to `Free-energy (cav+disp)` and is
calculated through eqs [Eq](#eq_g_cav) and
[Eq](#eq_g_disp). The term called `Surface-charge` corresponds
to the solute net charge that lies outside the C-PCM cavity. It is
basically the sum of the C-PCM charges (without the scaling by
$f(\varepsilon)$). The effect of this excess of charge on the energy and
the C-PCM charges themselves can be corrected by the so-called outlying
charge correction. In ORCA, this correction is calculated through a
Lagrangian-based algorithm,[pye1999](../../bibliography.md) but only printed for information
purposes. That is, the outlying charge effect is neither added to the
SCF energy nor to its derivatives. In any case, the corrected total
charge is printed in `Corrected charge`, while the correction term for
the energy is printed in `Outlying charge corr.`. To further help the
user, ORCA also prints a file with extension `.cpcm_corr`, where the
corrected C-PCM charges are provided.

If we want to use, instead, the GSES_nel model, one just needs to add
`surfacetype` `gepol_ses_gaussian` in the `%cpcm` block.

**[Note:]{.underline}** The analytical Hessian is not available for the
GVDW_nel and GSES_nel models as the second derivative of
$\Delta G_{nel}$ with respect to nuclear displacements is not
implemented.

### Options for Computing the CPCM terms

In CPCM calculations, there are three major steps. The first step is the
calculation of the electrostatic potential created by the quantum object
on the surface grid. This step is characterized by:

$$
V\left( r_{g} \right) = \sum_{A}^{}\frac{Z_{A}}{\left| R_{A} - r_{g} \right|} - \sum_{\mu\nu}^{}P_{\mu\nu}\in t_{}^{}{\frac{\mu(r)\nu(r)}{\left| r - r_{g} \right|}dr}
$$
$$
= \sum_{A}^{}\frac{Z_{A}}{\left| R_{A} - r_{g} \right|} - \sum_{\mu\nu}^{}P_{\mu\nu}\left( \mu\nu|g \right)
$$

The first sum is over atomic nuclei, the second over basis functions.
The second step in the calculation consists of converting the surface
potential into surface screening charges **q**. We are not writing it
out here, since this step is slightly different for each variant of
CPCM. In a nutshell, it involves solving a linear equation system of the
dimension of the number of surface segments which is usually done by
Cholesky decomposition.
The third, step is to sum the interaction of the surface charges with
the quantum electrons into the Fock matrix. This step is given by:

$$
F_{\mu\nu}^{(CPCM)} = - \sum_{g}^{}q_{q}\in t_{}^{}{\frac{\mu\left( r \right)\nu\left( r \right)}{\left| r - r_{g} \right|}dr}
$$
$$
= - \sum_{g}^{}q_{q}\left( \mu\nu|g \right)
$$

Here the sum is over surface segments with surface screening charges
$q_g$.
The time consuming step in these calculations is the calculation of the
three-center electrostatic integrals $(\mu\nu | g)$. By default,
these integrals are calculated using efficient analytic integration
provided by SHARK. However, there are the following alternatives
available:
1)  The integrals can be evaluated by numeric integration
2)  The potential and Fock matrix contributions can be evaluated using
    the RI density and the RI approximation respectively
3)  The potential and Fock matrix elements can be evaluated using
    multipole approximations to the integrals.
These options are triggered by:
```orca
%cpcm UseAnalyticOnRebuild true # if true, full Fock matrix builds
                                # are done with analytic integrals
                                # (strongly recommended)
Vopt v_analytic
 # = v_multipole
 # = v_RI
 # = v_numeric
Fopt f_analytic
 # = f_multipole
 # = f_RI
 # = f_numeric
```
!!! note
    -   Our experience indicates that analytic integration is still the
        safest and most accurate options.
    -   Analytic integration will win out over numerical integration or
        multipole approximations
    -   Some savings can be realized with the RI approximation, but it may
        also introduce non-negligible errors.
<a id="sec:essentialelements.solvationmodels.cosmo.detailed"></a>
## The Conductor-like Screening Solvation Model (COSMO)
!!! note
    The COSMO solvation model has been removed from ORCA v4.0.0 !!!
    *Please use the C-PCM solvation model in combination with the COSMO
    epsilon function if required!*\
    As a short form to use the C-PCM model with the COSMO epsilon function,
    you can specify the solvent via `!CPCMC(solvent)`.
<a id="sec:essentialelements.solvationmodels.smd.detailed"></a>
## The SMD Solvation Model
The SMD solvation model has been proposed by the Cramer and Truhlar
groups,[marenich2009](../../bibliography.md) and is based on the quantum mechanical charge
density of a solute molecule interacting with a continuum description of
the solvent. In the model the full solute electron density is used
without defining partial atomic charges and the solvent is not
represented explicitly but rather as a dielectric medium with the
surface tension at the solute--solvent boundary. SMD is a universal
solvation model, in the sense that it is applicable to any charged or
uncharged solute in any solvent or liquid medium for which a few key
descriptors are known. In particular, these descriptors are the
dielectric constant, refractive index, bulk surface tension, and acidity
and basicity parameters. Neglecting the concentration contribution, the
model separates the observable solvation free energy into two main
components,

$$
\Delta G_{\mathrm{S} } = \Delta G_{\mathrm{ENP} } + \Delta G_{\mathrm{CDS} }.\qquad \text{(eq_smdg)}
$$

In ORCA, the first component is the bulk electrostatic contribution
arising from a self-consistent reaction field treatment that involves
the electrostatic interaction using the Conductor-like Polarizable
Continuum Model (C-PCM). However, the radii are set to "intrinsic atomic
Coulomb radii". The second component, called the cavity-dispersion
solvent-structure (CDS) term, is the contribution resulting from
short-range interactions between the solute and solvent molecules in the
first solvation shell. This contribution is a sum of terms that are
proportional (with geometry-dependent proportionality constants called
atomic surface tensions) to the solvent-accessible surface areas of the
individual atoms of the solute. The CDS contribution to the free energy
of solvation is given by

$$
\Delta G_{\mathrm{CDS} }=\sum_{k}^{\text{atoms} }\sigma_{k}A_{k}(R,{R_{Z_{k} }+r_{s} }) + \sigma^{\mathrm{[M]} }\sum_{k}^{\text{atoms} }A_{k}(R,{R_{Z_{k} }+r_{s} }),
$$

where $\sigma_{k}$ and $\sigma^{\mathrm{[M]} }$ are the atomic surface
tension of atom $k$ and the molecular surface tension, respectively, and
$A_{k}$ is the solvent-accessible surface area (SASA). The SASA depends
on the geometry **R**, the set ${R_{Z_{k} }}$ of all atomic van der
Waals radii, and the solvent radius $r_{s}$, which is added to each of
the atomic van der Waals radii. In the program Bondi radii are used for
CDS contribution.
More details can be found in the original paper of Marenich et al.
[marenich2009](../../bibliography.md), which should be cited in publications using results of
SMD calculations (together with ref. [garcia_neese_gcs](../../bibliography.md), describing the implementation of the C-PCM
in ORCA, which is used by SMD).
SMD can be employed in single point calculations and geometry
optimizations, using single-determinant SCF (HF and DFT) and CASSCF
methods. In post-SCF methods the result is corrected in the reference
wave function. The SMD solvation model is invoked in the input file via
```orca
! SMD(solvent)
```
where `solvent` is one of the 179 solvents in the SMD library (see Table
[table:list-solvents](#table:list-solvents)).
Alternatively, one can request the SMD model via the `%cpcm` block by
writing:
```orca
%cpcm
  smd true             # turn on SMD
  SMDsolvent "solvent" # specify the name of solvent from the list
end
```
Independently on the way the user invokes the SMD model, ORCA
automatically sets a number of default SMD parameters for the chosen
solvent. If required, the user can also manually specify the solvent
descriptors used in an SMD calculation in the `%cpcm` block.
```orca
%cpcm
  soln      # index of refraction at optical frequencies at 293 K
  soln25    # index of refraction at optical frequencies at 298 K
  sola      # Abraham's hydrogen bond acidity
  solb      # Abraham's hydrogen bond basicity
  solg      # relative macroscopic surface tension
  solc      # aromaticity, fraction of non-hydrogenic solvent atoms
            # that are aromatic carbon atoms
  solh      # electronegative halogenicity, fraction of non-hydrogenic
            # solvent atoms that are F, Cl, or Br
 end
```
Let's consider the following input for a water molecule solvated by water,
```mol
title: structure 1
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
3
structure (0 1)
O  -0.00000018976103 0.00606010894837 0.00000000004527
H  0.76098169249695 -0.58891312953082 -0.00000000000022
H  -0.76098151333900 -0.58891299029372 -0.00000000000022
--- input ---
! B3LYP def2-SVP tightscf SMD(water)
* xyz 0 1
O  -0.00000018976103    0.00606010894837    0.00000000004527
H   0.76098169249695   -0.58891312953082   -0.00000000000022
H  -0.76098151333900   -0.58891299029372   -0.00000000000022
*
```
Before the SCF part starts, the program prints the SMD information. This
part reads as:
```orca
--------------------
CPCM SOLVATION MODEL
--------------------
CPCM parameters:
  Epsilon                                         ...      78.3550
  Refrac                                          ...       1.3328
  Rsolv                                           ...       1.3000
  Surface type                                    ... GAUSSIAN VDW
  Discretization scheme                           ... Constant charge density
    Threshold for H atoms                         ...       5.0000 (charges/Ang^2)
    Threshold for non-H atoms                     ...       5.0000 (charges/Ang^2)
  Epsilon function type                           ...         CPCM
Solvent:                                          ... WATER
SMD-CDS solvent descriptors:
  Soln                                            ...       1.3328
  Soln25                                          ...       1.3323
  Sola                                            ...       0.0000
  Solb                                            ...       0.0000
  Solg                                            ...       0.0000
  Solc                                            ...       0.0000
  Solh                                            ...       0.0000
Radii:
  Scheme                                          ... Element-dependent radii
  Radius for O  used is    2.8724 Bohr (=   1.5200 Ang.)
  Radius for H  used is    2.2677 Bohr (=   1.2000 Ang.)
Calculating surface                               ...        done! (  0.0s)
Cavity surface points                             ...          244
Cavity Volume                                     ...     130.0616
Cavity Surface-area                               ...     129.3354
Calculating surface distance matrix               ...        done! (  0.0s)
Performing Cholesky decomposition & store         ...        done! (  0.0s)
Overall time for CPCM initialization              ...                 0.0s
```
After the SCF is converged, the SMD contribution to the total energy is
printed (this term is labelled as "SMD CDS" term).
```orca
               *****************************************************
               *                     SUCCESS                       *
               *           SCF CONVERGED AFTER  10 CYCLES          *
               *****************************************************
Recomputing exchange energy using gridx3       ... done (    0.056 sec)
Old exchange energy                            :     -1.791736873 Eh
New exchange energy                            :     -1.791694663 Eh
Exchange energy change after final integration :      0.000042211 Eh
Total energy after final integration           :    -76.335230273 Eh
SMD CDS free energy correction energy :                 1.44927     Kcal/mol
Total Energy after SMD CDS correction =               -76.332920707 Eh
             **** ENERGY FILE WAS UPDATED (water.en.tmp) ****
----------------
TOTAL SCF ENERGY
----------------
Total Energy       :        -76.33292070695327 Eh           -2077.12437 eV
Components:
Nuclear Repulsion  :          9.11286213981824 Eh             247.97359 eV
Electronic Energy  :        -85.43200537714571 Eh           -2324.72305 eV
One Electron Energy:       -123.06209110061025 Eh           -3348.68974 eV
Two Electron Energy:         37.63008572346453 Eh            1023.96669 eV
CPCM Dielectric    :         -0.01612924659271 Eh              -0.43890 eV
SMD CDS (Gcds)     :          0.00230956608299 Eh               0.06285 eV
```
In ORCA, the user can also request the SMD18 model,[engelageSMD18](../../bibliography.md) which involves refined radii for Bromine
and Iodine (the radii adopted for the construction of the cavity used in the C-PCM part). The SMD18 model
is shown to accurately describe Halogen-bonding interactions in solution. It is requested via the `SMD18`
tag in the simple input:
```orca
! SMD(solvent) SMD18
```
or via the `%cpcm` block:
```orca
%cpcm
  SMD18 true  # default = false
end
```
**[Notes:]{.underline}**
-   If one is interested in the calculation of free energies of
    solvation using the SMD model, one just needs to compute
    $\Delta G_{\mathrm{S}}$ according to eq
    [Eq](#eq_smdg).
    However, here one should take into account that the SMD model
    considers the same concentration (1 mol/L) in both the gaseous and
    solution phases. Then, if a gas-phase standard state of 1 atm is
    considered, and we want to compare the calculated
    $\Delta G_{\mathrm{S} }$ with its experimental counterpart, a
    concentration term equal to 1.89 kcal/mol has to be added to the
    calculated $\Delta G_{\mathrm{S} }$.
<a id="sec:essentialelements.solvationmodels.draco"></a>
## Dynamic Radii Adjustment for Continuum Solvation (DRACO)
The DRACO scheme is an approach that improves the performance of implicit solvation models, in particular
 the accuracy of the calculated solvation free energies.[Plettdraco2024](../../bibliography.md) It is based on a dynamic scaling of the
original static radii used to describe the atoms/spheres that define the cavity of the solute.
In this approach, the original radii $r_i$ of an atom $i$ is scaled according to

$$
r_{i\text{scale}} = f_{i\text{scale}}r_i\qquad \text{(eq_dracosc)}
$$

with the scaling factor $f_{i\text{scale}}$ determined from

$$
f_{i\text{scale}} = \text{erf}(a_Z(q_{\text{eff},i}-b_Z)) + 1\qquad \text{(eq_dracof)}
$$

Here, $q_{\text{eff},i}$ corresponds to the effective partial charge and is defined as

$$
q_{\text{eff},i} = q_i + k_Zq_i\text{CN}_i\qquad \text{(eq_dracoq)}
$$

where $q_i$ is the atomic partial charge. The parameters $a_Z$, $b_Z$ and $k_Z$ are
element-specific parameters, and $\text{CN}_i$ is the fractional coordination number.

For oxygen atoms, the $f_{i\text{scale}}$ is corrected via a term that depends on the Abraham's hydrogen bond acidity ($\alpha$):

$$
f_{i\text{scale}}^{\text{O}} = f_{i\text{scale}} +c_{\text{O}}(0.43-\alpha)\qquad \text{(eq_dracoo)}
$$

with $c_{\text{O}}$ a parameter that is different for pure C-PCM or SMD. The correction in eq [Eq](#eq_dracoo) is only applied for solvents
with $\alpha<0.43$.

DRACO is parametrized for C-PCM and SMD for the following solvents: acetonitrile, DMSO, methanol, and water. The element-specific parameters in eqs [Eq](#eq_dracof),[Eq](#eq_dracoq), and [Eq](#eq_dracoo) are available in <https://github.com/grimme-lab/DRACO>.

The use of DRACO with C-PCM or SMD is triggered via the following tags in the simple input:

```orca
! CPCM(solvent) DRACO
```

or

```orca
! SMD(solvent) DRACO
```

Alternatively, it can also be requested in the `%cpcm` block:

```orca
%cpcm
  DRACO true
end
```

In ORCA, the default scheme to calculate the partial charges in eq [Eq](#eq_dracoq) is the electronegativity-equilibration (EEQ) charge model (D4 case),[caldeweyher2019](../../bibliography.md). However, one can also request the Charge Extended Hückel (CEH) model.[grimme2023AOmin](../../bibliography.md) The charge scheme within DRACO is controlled by the following tag in the `%cpcm` block:

```orca
%cpcm
  draco_charges ceh  # default = eeq
end
```

If CEH charges are requested, ORCA needs to run an XTB calculation to generate them. Here, one should have at least the version 6.7.1 of XTB (older versions will not generate the CEH charges, see section [programs.general](../orcaarchitecture/components.md#sec:programs.general)). Regarding the fractional coordination number in eq [Eq](#eq_dracoq), it is calculated as described in GFN2-XTB calculations.[grimme2019xtb](../../bibliography.md)

DRACO can be used in single-point energy calculations (with both CEH and EEQ charges) and in geometry optimizations (with the EEQ charges)[wittmann2025draco](../../bibliography.md). The DRACO contributions to the analytical Hessian are not yet implemented. In this case, the user should request `numfreq`.

Notice that calculations where DRACO is requested involve a discretization scheme of the surface of the cavity based on a constant number of charges per sphere. The default is 194 Lebedev points. This contrast with the scheme used for C-PCM/SMD calculations without DRACO, where the default is the isodensity scheme, as discussed in Section [solvationmodels.gaussian_charge](#sec:essentialelements.solvationmodels.gaussian_charge). This choice is needed, specially for geometry optimizations. For DRACO, the radii of the spheres in the cavity changes in each optimization step. Then, if ORCA used by default the isodensity scheme for DRACO, the associated Lebedev grid per atom could change between two consecutive steps, leading to discontinuities in the total energy and its gradient. Nevertheless, the isodensity scheme can still be requested for calculations involving DRACO via the tag `DRACOisodens` in the `%cpcm` block:

```orca
%cpcm
  dracoisodens true  # default = false
end
```

<a id="sec:essentialelements.solvationmodels.opencosmors"></a>
## OpenCOSMO-RS

ORCA is interfaced to openCOSMO-RS,[gerlachcosmors2022,Muellercosmors2025](../../bibliography.md) an open source implementation of the COSMO-RS model.[cosmors_1995,cosmors_1998](../../bibliography.md) This model is widely used in both academia and industry to predict fluid phase thermodynamics.

The main idea behind COSMO-RS is that the interaction between molecules in the liquid phase can de depicted as an ensemble of interacting surface segments. The properties on the surface segments are calculated via QM calculations of the solute and the solvent in a perfect conductor ($\epsilon = \in fty$), and the interaction free energies between segments are functions of a set of descriptors. Among them, the most relevant one is the screening charge density ($\sigma$).

A complete description of the COSMO-RS model used in ORCA is provided in refs [gerlachcosmors2022,Muellercosmors2025](../../bibliography.md), and the code is available in <https://github.com/TUHH-TVT>. In particular, the parametrization for ORCA 6.0 is called openCOSMO-RS 24a. The corresponding the executable is shipped together with the ORCA 6.0 binaries and called `openCOSMORS`. ORCA will then call internally this executable whenever it is needed.

COSMO-RS calculations within ORCA are a special type of calculation. By requesting COSMO-RS, ORCA runs a set of single-point-energy calculations for both the solute and the solvent and then calls the openCOSMO-RS executable, which expects an input geometry for the solute and the solvent and calculates the free energy of solvation of the solute in the solvent. A workflow of a calculation requesting COSMO-RS in ORCA is the following:

1. Single-point-energy calculation of the solute in the gas-phase
2. Single-point-energy calculation of the solute in a conductor ($\epsilon = \in fty$)
3. Single-point-energy calculation of the solvent in a conductor ($\epsilon = \in fty$)
4. Do COSMO-RS via the openCOSMO-RS executable and compute solvation properties

Points 1 to 3 correspond to DFT calculations at the BP86/def2-TZVPD level. This is the level of theory used to parametrize COSMO-RS for ORCA 6.0. As it is shown later, the user can change the functional and basis set, but this is not recommended!

Regarding calculations 2 and 3, to produce smooth $\sigma$ profiles, ORCA discards the surface segments with an area < 0.01 Å$^2$. For these two calculations, the radii of several elements used to construct the cavity of solute and solvent are different than the defaults employed within non-COSMO-RS calculations (using C-PCM). This is due to the fact that the provided openCOSMO-RS binaries involve a special parametrization of COSMO-RS for ORCA 6.0, and this does not only affect the COSMO-RS parameters, but also the radii of several elements used in the C-PCM part.

After point 4 is done, the free energy of solvation ($\Delta G_{\mathrm{S}}$) of the solute in the solvent is printed in the ORCA output file. In ORCA 6.0 the use of openCOSMO-RS is restricted to the calculation of $\Delta G_{\mathrm{S}}$.

<a id="sec:essentialelements.solvationmodels.usecosmors"></a>
### How to Run a ORCA/COSMO-RS Calculation
ORCA/COSMO-RS calculations are controlled through the `%cosmors` block. These type of calculations require two input structures, one for the solute and one for the solvent. The solute coordinates are provided in the input file as done for any other type of calculation. However, regarding the structure for the solvent, there are two options:

1. Retrieve the structure of the solvent from a database
2. Provide the structure in a separate file

To use strategy 1, we need to request the solvent via:

```orca
COSMORS(Solvent)
```

in the simple input or using the `%cosmors` block:

```orca
%cosmors
  solvent "Solvent"
end
```

The list of internal solvents available in ORCA are shown in [table:list-solvents](#table:list-solvents). For instance, for a water molecule
solvated by acetonitrile, the input file looks like:

```mol
title: structure 2
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
3
structure (0 1)
O  0.00000006589375 0.00157184228646 0.00000000004493
H  0.77316868532439 -0.58666889665624 -0.00000000000005
H  -0.77316876182122 -0.58666895650640 -0.00000000000005
--- input ---
!COSMORS(Acetonitrile)
* xyz 0 1
O    0.00000006589375       0.00157184228646       0.00000000004493
H    0.77316868532439      -0.58666889665624      -0.00000000000005
H   -0.77316876182122      -0.58666895650640      -0.00000000000005
*
```

If the user wants to provide a structure for the solvent (strategy 2), then a separate file with extension **.cosmorsxyz** should be available. The name of this file (without extension) is controlled by the tag `solventfilename` in the `%cosmors` block. For instance, if we want to calculate the free energy of solvation of acetone in water, the ORCA input file would look like this:

```mol
title: structure 3
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
10
structure (0 1)
H  1.99757808828569 0.25022586507917 0.72957579847856
C  1.44666788654273 0.06088176074125 -0.18975506731892
H  1.67115809398389 0.82690156694531 -0.93346420198265
H  1.76410010378270 -0.89580894800398 -0.61702931492419
C  -0.03218812888253 -0.00668250402989 0.08117960952503
O  -0.47126229461002 -0.06383203315654 1.21590571064657
C  -0.93671505604705 -0.00759565576779 -1.12174123739234
H  -0.88761294036774 0.97611724740670 -1.59852429171257
H  -0.58940208311204 -0.73299176093053 -1.85998395179737
H  -1.96332366957567 -0.22151553828368 -0.83026305352213
--- input ---
%cosmors
  solventfilename "water"
end

* xyz 0 1
H    1.99757808828569      0.25022586507917      0.72957579847856
C    1.44666788654273      0.06088176074125     -0.18975506731892
H    1.67115809398389      0.82690156694531     -0.93346420198265
H    1.76410010378270     -0.89580894800398     -0.61702931492419
C   -0.03218812888253     -0.00668250402989      0.08117960952503
O   -0.47126229461002     -0.06383203315654      1.21590571064657
C   -0.93671505604705     -0.00759565576779     -1.12174123739234
H   -0.88761294036774      0.97611724740670     -1.59852429171257
H   -0.58940208311204     -0.73299176093053     -1.85998395179737
H   -1.96332366957567     -0.22151553828368     -0.83026305352213
*
```

The structure of the solvent (water) is the one in the `water.cosmorsxyz` file:

```mol
title: structure 4
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
3
0 1
O  0.00000006589375 0.00157184228646 0.00000000004493
H  0.77316868532439 -0.58666889665624 -0.00000000000005
H  -0.77316876182122 -0.58666895650640 -0.00000000000005
```
where the first line corresponds to the number of atoms, and in the second line the charge
and multiplicity are provided.

The output for COSMO-RS is printed in the ORCA output file after the line that reads `OPENCOSMO-RS CALCULATION`. First
of all, the information regarding the level of theory, the solute and the solvent is printed. For the example above (acetone in water), it reads as,

```mol
title: structure 5
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
13
structure
H      1.997578     0.250226     0.729576
C      1.446668     0.060882    -0.189755
H      1.671158     0.826902    -0.933464
H      1.764100    -0.895809    -0.617029
C     -0.032188    -0.006683     0.081180
O     -0.471262    -0.063832     1.215906
C     -0.936715    -0.007596    -1.121741
H     -0.887613     0.976117    -1.598524
H     -0.589402    -0.732992    -1.859984
H     -1.963324    -0.221516    -0.830263
O      0.000000     0.001572     0.000000
H      0.773169    -0.586669    -0.000000
H     -0.773169    -0.586669    -0.000000
```

After these lines, ORCA prints the final single point energy for each of the QM calculations, together with the output file
to which the ORCA output is redirected:

```orca
----------------------------------------------
Single Point Calculation (solute / gas-phase)
----------------------------------------------
Output single point calculation redirected to >test.solute_vac.lastout

FINAL SINGLE POINT ENERGY (Solute-gas-phase)     -193.233975714789

----------------------------------------------
Single Point Calculation (solute / CPCM)
----------------------------------------------
Output single point calculation redirected to >test.solute_cpcm.lastout

FINAL SINGLE POINT ENERGY (Solute-CPCM)     -193.243987123912

----------------------------------------------
Single Point Calculation (solvent / CPCM)
----------------------------------------------
Output single point calculation redirected to >test.solvent_cpcm.lastout

FINAL SINGLE POINT ENERGY (Solvent-CPCM)      -76.479155022866
```

Once this information is printed, ORCA calls the openCOSMO-RS executable and $\Delta G_{\mathrm{S}}$ is printed in the following block:

```orca
----------------------
SOLVATION DATA
----------------------
Reference temperature             :          298.15 K
Free energy of solvation (dGsolv) : -0.006626234385 Eh   -4.158026 kcal/mol

Note: In order to calculate the free energy of the solvated solute (Gsolv),
      one should add the computed dGsolv to the "Final Gibbs free energy"
      (Gvac = H-T*S) of the solute in gas-phase. That is: Gsolv = Gvac +
      dGsolv. Here, the Gvac has been calculated previously after a frequency
      calculation of the solute at a certain level of theory and printed
      in the "THERMOCHEMISTRY" block.
```

As pointed out in the last paragraph of the COSMO-RS output, to calculate the Gibbs free energy of
the solute solvated by the given solvent, one should add the calculated $\Delta G_{\mathrm{S}}$
to the `Final Gibbs free energy` of the solute in the gas-phase.

**[Note:]{.underline}** The workflow explained above for ORCA/openCOSMO-RS calculations
involves the same structure for the solute in the gas-phase and in solution.
However, these structures may differ substantially depending on the type of solute and solvent. In ORCA,
it is possible to optimize the structures for each of the three calculations needed in the ORCA/openCOSMO-RS
workflow. That is, (1) the solute in gas-phase, (2) the solute in a conductor, and (3) the solvent in a conductor.
To do that, one needs to add the level of optimization via the `dftfunc` tag, which is exclusive for the DFT functional, but
as an exception, can be extended with the optimization tag:

```orca
%cosmors
  dftfunc  "BP86 tightopt"
end
```

<a id="sec:essentialelements.solvationmodels.opencosmors.keywords"></a>
### OpenCOSMO-RS Keywords

The parameters that can be defined in the `%cosmors` block in the ORCA input file are the following:

```orca
%cosmors
  aeff              5.925  # Effective contact area between surface segments (Å^2)
  lnalpha           0.202  # Logarithm of the misfit prefactor
  lnchb             0.166  # Hydrogen bond (HB) strength parameter
  chbt              1.50   # Parameter for the temperature dependence of the HB
  sigmahb           9.61e-3 # HB threshold parameter (e/Å^2)
  rav               0.50   # Radius to average ideal screening charges in Å
  fcorr             2.40   # Parameter adjusted from dielectric screening energies
  ravcorr           1.00   # Additional radius to calculate the misfit energy in Å
  astd              41.624 # Standard surface area (normalization factor) in Å^2
  zcoord            10.0   # Coordination number
  dgsolv_eta       -4.4480 # Offset for the solv. energy calculation
  dgsolv_omegaring  0.2630 # Correction for solv. energy of molecules with rings
  temp              298.15 # Reference temperature in Kelvin
  dftfunc           "BP86" # String for the DFT functional
  dftbas            "def2-TZVPD"  # String for the basis set
  solvent           "THF"  # Solvent from the internal database
  solventfilename   "water" # Name of the .cosmorsxyz solvent file
  orbs_vac          false  # Reuse the gas-phase orbitals for the calculation
                           # involving the solute in a conductor
end
```
It is not recommended to change the defaults of the COSMO-RS parameters.

<a id="sec:essentialelements.solvationmodels.cc"></a>
## Implicit Solvation in Coupled-Cluster Methods

The coupled-cluster Lagrangian, $\mathcal{L}$, for a system implicitly
solvated reads as
follows,[cammi2009,caricato2011,garcia_neese_cc_cpcm](../../bibliography.md)

$$
\mathcal{L}(\Lambda,T)=\langle\psi_0|(1+\Lambda)\mathrm{e}^{-T} H_0 \mathrm{e}^T|\psi_0\rangle+\frac{1}{2}\overline{Q}(\Lambda,T)\cdot\overline{V} (\Lambda,T)\qquad \text{(eq_lag)}
$$

where $\psi_0$ is the reference wave function, and $H_0$ is the
Hamiltonian for the isolated molecule. The operator $T$ for CCSD is
defined in terms of single and double excitations ($T=T_1+T_2$), and
$\Lambda$ is the de-excitation operator, defined in terms of the
Lagrange multipliers:

$$
T=T_1+T_2=\sum_{ia}t_a^ia_a^+a_i+\sum_{ijab}t_{ab}^{ij}a_a^+a_b^+a_ja_i\qquad \text{(eq_t)}
$$

$$
\Lambda=\sum_{ia}\lambda_i^aa_i^+a_a+\frac{1}{2}\sum_{ijab}\lambda_{ij}^{ab}a_i^+a_aa_j^+a_b\qquad \text{(eq_mult)}
$$

Here, $t_a^i$ and $t_{ab}^{ij}$ are the singles and doubles wave
function amplitudes and $a_i$ and $a_a^+$ are standard fermion
annihilation and creation operators, respectively. Canonical occupied
orbitals are denoted by the symbols $i,j,k,\dots$, virtual orbitals by
the symbols $a,b,c,\dots$, and we use the symbols $p,q,r\dots$ for
general orbital indices.

The quantities $\overline{Q} $ and $\overline{V} $ are the CC
expectation values of the C-PCM operators $Q$ and $V$,
which are the solvation charges vector and solute potential vector
defined at the position the charges, respectively.

$$
\overline{Q}(\Lambda,T)=\langle\psi_0|(1+\Lambda)\mathrm{e}^{-T}Q\mathrm{e}^T|\psi_0\rangle\qquad \text{(eq_qbar1)}
$$

$$
\overline{V}(\Lambda,T)=\langle\psi_0|(1+\Lambda)\mathrm{e}^{-T}V\mathrm{e}^T|\psi_0\rangle\qquad \text{(eq_vqbar1)}
$$

Equation [Eq](#eq_lag)
can be rewritten by introducing the normal product form of an operator:

$$
X_N=X-\langle\psi_0|X|\psi_0\rangle=X-X_0\qquad \text{(eq_normalf)}
$$

If one uses this result in eq [Eq](#eq_lag), together with the fact that $Q$ and
$V$ are related through eq
[Eq](#eq_cpcm), then
eq [Eq](#eq_lag) reads
as,

$$
\begin{split}
\mathcal{L}(\Lambda,T)=&\langle\psi_0|H_0|\psi_0\rangle+\langle\psi_0|(1+\Lambda)\mathrm{e}^{-T}H_{0N}\mathrm{e}^T|\psi_0\rangle+\frac{1}{2}Q_0\cdot V_0+Q_0\cdot\overline{V} _N(\Lambda,T)+\frac{1}{2}\overline{Q} _N(\Lambda,T)\cdot\overline{V} _N(\Lambda,T)=\\
&=E_0+\langle\psi_0|(1+\Lambda)\mathrm{e}^{-T}H_{0N}\mathrm{e}^T|\psi_0\rangle+Q_0\cdot\overline{V} _N(\Lambda,T)+\frac{1}{2}\overline{Q} _N(\Lambda,T)\cdot\overline{V} _N(\Lambda,T)
\end{split}\qquad \text{(eq_lag2)}
$$

Here, $Q_0$ and $V_0$ are the $Q$ and
$V$ vectors calculated with the $\psi_0$ wave function, and
$E_0$ is the reference energy
($E_0=\langle\psi_0|H_0|\psi_0\rangle+\frac{1}{2}Q_0\cdot V_0$).
Different approximations can be adopted in eq
[Eq](#eq_lag2)
depending on how one calculates its last term
$\frac{1}{2}\overline{Q} _N(\Lambda,T)\cdot\overline{V} _N(\Lambda,T)$.

In ORCA there are three different CCSD/CPCM approaches: (i) the PTE
scheme, (ii) the PTE(S) scheme, and the (iii) the PTES scheme, being the
last one the default. Here, the acronym PTE stands for "perturbation
theory and energy" and "S" for singles. The choice of any of these
approaches is controlled via the tag `CPCMccm`. Information about
which CCSD/C-PCM is used by ORCA in a calculation is printed in the
`ORCA-MATRIX DRIVEN CI` block in the output file in the line starting
by `CPCM scheme`:

```orca
--------------------------------------------------------------------------------
                             ORCA-MATRIX DRIVEN CI
--------------------------------------------------------------------------------

--------------------------------
AUTOMATIC CHOICE OF INCORE LEVEL
--------------------------------

Memory available                           ...   2000.00 MB
Memory needed for S+T                      ...      9.26 MB
Memory needed for J+K                      ...     18.57 MB
Memory needed for DIIS                     ...    129.61 MB
Memory needed for 3-ext                    ...     72.69 MB
Memory needed for 4-ext                    ...    486.14 MB
Memory needed for triples                  ...      0.00 MB
 -> Final InCoreLevel    ... 5

Wavefunction type
-----------------
Correlation treatment                      ...      CCSD
Single excitations                         ... ON
Orbital optimization                       ... OFF
Calculation of Lambda equations            ... ON
Calculation of Brueckner orbitals          ... OFF
Perturbative triple excitations            ... OFF
CPCM scheme                                ... PTE(S)
Calculation of F12 correction              ... OFF
```

In the following subsections, we describe the different CCSD/C-PCM
approaches available in ORCA and how to use them.

<a id="sec:essentialelements.solvationmodels.sec_pte"></a>
### PTE scheme

In the "perturbation theory energy" (PTE) scheme, the last term in eq
[Eq](#eq_lag2) is
equal to zero (this term does not depend on $\Lambda$ and $T$),

$$
\mathcal{L}(\Lambda,T)=E_0+\langle\psi_0|(1+\Lambda)\mathrm{e}^{-T}H_{0N}\mathrm{e}^T|\psi_0\rangle+Q_0\cdot\overline{V} _N(\Lambda,T)\qquad \text{(eq_pte_lag)}
$$

The potential $\overline{V} _N$ can be written as follows:

$$
\overline{V} _N(\Lambda,T)=\langle\psi_0|(1+\Lambda)\mathrm{e}^{-T}\sum_{pq}v_{pq}\{p^+q\}\mathrm{e}^T|\psi_0\rangle=\sum_{pq}v_{pq}\langle\psi_0|(1+\Lambda)\mathrm{e}^{-T}\{p^+q\}\mathrm{e}^T|\psi_0\rangle=\sum_{pq}v_{pq}\Gamma_{pq}\qquad \text{(eq_vnlt)}
$$

where we have used that $V_N=\sum_{pq}v_{pq}\{p^+q\}$
(second-quantized form of a normal ordered operator), with
$v_{pq}$ the components of the solute potential in the MO
basis. The matrix $\Gamma$ is the CCSD relaxed one-electron density
matrix. Then, the contribution to the equations for the $T$ amplitudes
comes from the derivative of $\overline{V} _N(\Lambda,T)$ with
respect to the $\Lambda$ amplitudes ($Q_0$ does not depend on
the Lagrange multipliers). In this context, the Hamiltonian $H_{0N}$
contains a term that depends on the elements of the Fock matrix
($\sum_{pq}f_{pq}\{p^+q\}$) and that has the same functional form as
$V_N$. As the Fock matrix is updated in the reference
calculation with a C-PCM term that reads as (in AO basis)
$F_{\mu\nu}^{\mathrm{CPCM} }=Q_0\cdot V_{\mu\nu}$, then
the term $Q_0\cdot\overline{V} _N(\Lambda,T)$ is added
implicitly to eq [Eq](#eq_pte_lag).

Once the $T$ amplitudes are obtained, the total energy, $E$, is
calculated as

$$
E=E_0+\langle\psi_0|\mathrm{e}^{-T}(H_{0N}+Q_0\cdot V_N)\mathrm{e}^T|\psi_0\rangle=E_0+\sum_{ia}F_{ia}t_a^i+\frac{1}{4}\sum_{ijab}\langle ij||ab\rangle\left(t_{ab}^{ij}+2t_a^it_b^j\right)\qquad \text{(eq_ecc_pte)}
$$

Then, the C-PCM contribution to the CC energy within the PTE scheme
occurs through the term $\frac{1}{2}Q_0\cdot V_0$ in
$E_0$ and implicitly through the Fock matrix elements $F_{ia}$
($F_{ia}=F_{ia}^0+Q_0\cdot v_{ia}$).

The PTE scheme corresponds to `CPCMccm 0`, and is implemented for
canonical-CCSD (RHF and UHF) and DLPNO-CCSD (RHF and UHF). For instance,
for a DLPNO-CCSD calculation (closed-shell reference) of a system
solvated by water using the PTE scheme, the input file looks like:

```orca

! DLPNO-CCSD cc-pVTZ cc-PVTZ/C TightSCF CPCM(Water)

%cpcm
  CPCMccm 0
end

* xyzfile 0 1 water.xyz
```

<a id="sec:essentialelements.solvationmodels.sec_pte_s"></a>
### PTE(S) scheme

In this scheme (where the "S" stands for singles), the last term in eq
[Eq](#eq_lag2)
depends on the $T$ amplitudes, but not on the $\Lambda$ amplitudes,

$$
\mathcal{L}(\Lambda,T)=E_0+\langle\psi_0|(1+\Lambda)\mathrm{e}^{-T}H_{0N}\mathrm{e}^T|\psi_0\rangle+Q_0\cdot\overline{V} _N(\Lambda,T)+\frac{1}{2}\overline{Q} _N(T)\cdot\overline{V} _N(T)\qquad \text{(eq_pte_s_lag)}
$$

Again, in the same way as for the PTE scheme, the C-PCM contribution to
the equations for the $T$ amplitudes comes from the term
$Q_0\cdot\overline{V} _N(\Lambda,T)$ in eq
[Eq](#eq_pte_s_lag), which is implictly added to the Fock matrix
elements in the MO basis. The last term in eq
[Eq](#eq_pte_s_lag) does not depend on the $\Lambda$ amplitudes
and then does not contribute to the equations for the $T$ amplitudes.
However, this term depends on the $T$ amplitudes through the elements
$\gamma_{ai}$ of the density matrix $\Gamma$,

$$
\gamma_{ai}=t_a^i+\sum_{me}\left(t_{ae}^{im}-t_e^it_a^m\right)\lambda_m^e-\frac{1}{2}\sum_{mnef}\lambda_{mn}^{ef}\left(t_{ef}^{in}t_a^m+t_{af}^{mn}t_e^i\right)\qquad \text{(eq_gai)}
$$

and then it contributes to the final energy $E$ in the following way:

$$
\frac{1}{2}\overline{Q} _N(T)\cdot\overline{V} _N(T)=\frac{1}{2}\left(\sum_{ai}t_a^iq_{ai}\right)\cdot\left(\sum_{ai}t_a^iv_{ai}\right)\qquad \text{(eq_pte_s_ec)}
$$

That gives the final equation for the total energy of our system,

$$
\begin{split}
E&=E_0+\langle\psi_0|\mathrm{e}^{-T}(H_{0N}+Q_0\cdot V_N)\mathrm{e}^T|\psi_0\rangle+\frac{1}{2}\left(\sum_{ai}t_a^iq_{ai}\right)\cdot\left(\sum_{ai}t_a^iv_{ai}\right)=\\
&=E_0+\sum_{ia}F_{ia}t_a^i+\frac{1}{4}\sum_{ijab}\langle ij||ab\rangle\left(t_{ab}^{ij}+2t_a^it_b^j\right)+\frac{1}{2}\left(\sum_{ai}t_a^iq_{ai}\right)\cdot\left(\sum_{ai}t_a^iv_{ai}\right)\end{split}\qquad \text{(eq_ecc_pte_s)}
$$

Therefore, the CC energy for a solvated system within the PTE(S) scheme
involves three C-PCM contributions: (1) the term
$\frac{1}{2}Q_0\cdot V_0$ included in $E_0$, (2) the
term $\sum_{ia}Q_0\cdot v_{ia}t_a^i$ that occurs
implicitly through $\sum_{ia}F_{ia}t_a^i$ and (3) the term
$\frac{1}{2}\left(\sum_{ai}t_a^iq_{ai}\right)\cdot\left(\sum_{ai}t_a^iv_{ai}\right)$.

This scheme is available in ORCA for canonical-CCSD (RHF and UHF) and
DLPNO-CCSD (RHF and UHF). In order to use it, the user needs to add the
tag `CPCMccm 1` in the `%cpcm` block.

```orca

! DLPNO-CCSD cc-pVTZ cc-PVTZ/C TightSCF CPCM(Water)

%cpcm
  CPCMccm 1
end

* xyzfile 0 1 water.xyz
```

<a id="sec:essentialelements.solvationmodels.sec_ptes"></a>
### PTES scheme

In this scheme, both $\overline{Q} _N$ and $\overline{V} _N$ in
the last term in eq [Eq](#eq_lag2) depend on the $T$ amplitudes but just one of them
depends on the $\Lambda$ amplitudes,

$$
\mathcal{L}(\Lambda,T)=E_0+\langle\psi_0|(1+\Lambda)\mathrm{e}^TH_{0N}\mathrm{e}^T|\psi_0\rangle+Q_0\cdot\overline{V} _N(\Lambda,T)+\frac{1}{2}\overline{Q} _N(T)\cdot\overline{V} _N(\Lambda,T)\qquad \text{(eq_lptes)}
$$

The C-PCM terms enter these equations on the one hand, implicitly,
through the elements of the Fock matrix (like for the PTE and PTE(S)
schemes), and on the other hand, explicitly through the derivatives of
$\frac{1}{2}\overline{Q} _N(T)\cdot\overline{V} _N(\Lambda,T)$
with respect to $\Lambda$. If we call $\mathcal{L}_{\mathrm{CPCM} }$ the
last C-PCM term in eq [Eq](#eq_lptes), then the contribution from this term to the $T$
amplitudes equations read as:

$$
\frac{\partial\mathcal{L}_{\mathrm{CPCM} }}{\partial \lambda_i^a}=\frac{1}{2}\left(\sum_{ai}t_a^iq_{ai}\right)\cdot\left[-\sum_jt_a^jv_{ji}+\sum_bt_b^iv_{ab}+v_{ia}+\sum_{bj}\left(t_{ba}^{ji}-t_a^jt_b^i\right)v_{bj}\right]\qquad \text{(eq_ltesd1)}
$$

$$
\frac{\partial\mathcal{L}_{\mathrm{CPCM} }}{\partial \lambda_{ij}^{ab} }=\frac{1}{2}\left(\sum_{ai}t_a^iq_{ai}\right)\cdot\left[-\frac{1}{2}\sum_kt_{ab}^{kj}v_{ki}+\frac{1}{2}\sum_ct_{ac}^{ij}v_{bc}-\frac{1}{2}\sum_{ck}\left(t_{ab}^{kj}t_c^i+t_{cb}^{ij}t_a^k\right)v_{ck}\right]\qquad \text{(eq_ltedd)}
$$

The contribution to the energy is the same as that for the PTE(S)
scheme, but with different values for the $T$ amplitudes (as the
equations to calculate them differ slightly from those for the PTE(S)
scheme).

$$
\begin{split}
E&=E_0+\langle\psi_0|\mathrm{e}^{-T}(H_{0N}+Q_0\cdot V_N)\mathrm{e}^T|\psi_0\rangle+\frac{1}{2}\left(\sum_{ai}t_a^iq_{ai}\right)\cdot\left(\sum_{ai}t_a^iv_{ai}\right)=\\
&=E_0+\sum_{ia}F_{ia}t_a^i+\frac{1}{4}\sum_{ijab}\langle ij||ab\rangle\left(t_{ab}^{ij}+2t_a^it_b^j\right)+\frac{1}{2}\left(\sum_{ai}t_a^iq_{ai}\right)\cdot\left(\sum_{ai}t_a^iv_{ai}\right)\end{split}\qquad \text{(eq_ecc_ptes)}
$$

This scheme is the default CCSD/C-PCM approach in ORCA and is available
in ORCA for canonical-CCSD (RHF and UHF) and DLPNO-CCSD (RHF and UHF).
In this case, the tag `CPCMccm` in the `%cpcm` block is equal to 2.
However, as the PTES scheme is the default in ORCA, the user just needs
to add the information about the solvent in the input file, in order to
use this approach.

```mol
title: structure 6
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
3
structure (0 1)
O  -0.00000018976103 0.00606010894837 0.00000000004527
H  0.76098169249695 -0.58891312953082 -0.00000000000022
H  -0.76098151333900 -0.58891299029372 -0.00000000000022
--- input ---
! DLPNO-CCSD cc-pVTZ cc-PVTZ/C TightSCF CPCM(Water)

* xyz 0 1
O  -0.00000018976103    0.00606010894837    0.00000000004527
H   0.76098169249695   -0.58891312953082   -0.00000000000022
H  -0.76098151333900   -0.58891299029372   -0.00000000000022
*
```

**Notes regarding the use of the CCSD/C-PCM schemes**:

-   For calculations within the PTE(S) and the PTES schemes, the
    explicit C-PCM contribution to the total energy (see eqs.
    [Eq](#eq_ecc_pte_s) and
    [Eq](#eq_ecc_ptes)) is printed in the
    `COUPLED CLUSTER ENERGY` block after the equations for the "T"
    amplitudes converge. In this case, this energy is labelled as
    `C-PCM corr. term` and is already included in the correlation
    energy, `E(CORR)`. For the input example from above, this information
    looks like:

    ```orca
    ----------------------
    COUPLED CLUSTER ENERGY
    ----------------------

    E(0)                                       ...    -76.066903687
    E(CORR)(strong-pairs)                      ...     -0.267203798
    E(CORR)(weak-pairs)                        ...     -0.000106106
    E(CORR)(corrected)                         ...     -0.267309904
    C-PCM corr. term (included in E(CORR))     ...     -0.000003158
    E(TOT)                                     ...    -76.334213591
    Singles Norm <S|S>**1/2                    ...      0.017784967
    T1 diagnostic                              ...      0.006287935
    ```

    This contribution does not represent the whole C-PCM contribution to
    the correlation energy, as this one also occurs, implicitly, through
    the "T" amplitudes.

-   The C-PCM contribution to the $\Lambda$ equations is implemented in
    ORCA for the PTE(S) and PTES schemes. Then, the user can request
    unrelaxed densities.

<a id="sec:essentialelements.solvationmodels.keyword-list.detailed"></a>
## Complete Keyword List for the `%cpcm` Block

The available parameters/options that the user can request via the `%cpcm` block are:

```orca
%cpcm
  epsilon             80.0    # Dielectric constant
  refrac               1.0    # Refractive index
  rsolv                1.3    # Solvent probe radius in Angstroem
                              # (for SES-type cavities)
  rmin                 0.5    # Minimal GEPOL sphere radius in Angstroem
  pmin                 0.1    # Minimal distance between two surface points
                              # in Angstroem
  fepstype            cpcm    # Epsilon function type: cpcm, cosmo
  xfeps                0.0    # X parameter for the feps scaling function
  surfacetype vdw_gaussian    # Cavity surface: gepol_ses, gepol_sas
                                                vdw_gaussian, gepol_ses_gaussian
  ndiv                   5    # Maximum depth for recursive sphere generation
  num_leb              302    # Lebedev points for the Gaussian charge scheme
  radius[N]            1.3    # Atomic radius for atomic number N in Angstroem
  AtomRadii(N,1.4)            # Atomic radius for the Nth atom in Angstroem
  scale_gauss          1.2    # Scaling factor for the atomic radii in the
                                Gaussian charge scheme
  cut_area             0.0    # Cutoff for the area of a surface segment in a.u.
                                Only valid for the Gaussian charge scheme
  cut_swf             1e-7    # Cutoff for the switching function
                                Only valid for the Gaussian charge scheme
  thresh_h             5.0    # Threshold for the charge density on a hydrogen
                                atom in charges/Å^2 (isodensity scheme)
  thresh_noth          5.0    # Threshold for the charge density on non-hydrogen
                                atoms in charges/Å^2 (isodensity scheme)
  solvent          "water"    # Solvent name (for C-PCM)
  smd                 true    # Turn on SMD
  smdsolvent     "ethanol"    # Solvent name for SMD
  soln              1.3611    # Index of refraction at optical frequencies at 293 K
  soln25            1.3593    # Index of refraction at optical frequencies at 298 K
  sola                0.37    # Abraham's hydrogen bond acidity
  solb                0.48    # Abraham's hydrogen bond basicity
  solg               31.62    # Relative macroscopic surface tension
  solc                0.00    # Aromaticity, fraction of non-hydrogenic solvent
                              # atoms that are aromatic carbon atoms
  solh                0.00    # Electronegative halogenicity, fraction of
                              # non-hydrogenic solvent atoms that are F, Cl, or Br
  SMD18              false    # Turn on SMD18
  CPCMccm                0    # Coupled-cluster/C-PCM scheme (default = 2)
  cds_cpcm               0    # Use of the GVDW_nel or GSES_nel scheme
                              # (default = 0)
  draco               true    # Turn on DRACO (default = false)
  dracoisodens       false    # Use isodensity scheme for DRACO (default = false)
  draco_charges        ceh    # Charges used within DRACO (default = eeq)
  vopt          v_analytic    # Method to calculate the ESP at the position
                              # of the charges:
                              #   v_analytic (default): via analytic ESP integrals
                              #   v_numeric: via numerical integration
                              #   v_ri: via the RI-density
                              #   v_multipole: via BUPO
 fopt           f_analytic    # Method to calculate the C-PCM contribution to the
                              # Fock or Kohn-Sham matrix:
                              #   f_analytic (default): via the ESP integrals
                              #   f_numeric: via numerical integration
                              #   f_ri: via the RI-density
                              #   f_multipole: via BUPO
end
```
