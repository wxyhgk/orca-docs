<a id="sec:orcaarchitecture.general"></a>
# ORCA Structure

<a id="sec:programs.general"></a>
## Program Components

The program system ORCA consists of several separate programs that call
each other during a run. The following basic modules are included in
this release (listed in alphabetical order):

|  |  |
|---|---|
| orca | Main input+driver program |
| orca_ailft | Ab Initio Ligand Field Theory |
| orca_autoci | CI type program using the automated generation environment (ORCA-AGE) |
| orca_casscf | Main program for CASSCF driver |
| orca_casscfresp | CASSCF static linear response |
| orca_cclib | Precalculation of one particle coupling coefficients for ACCCI |
| orca_chelpg | Calculation of different kinds of ESP charges |
| orca_ciprep | Preparation of data for MRCI calculations (frozen core matrices and the like) |
| orca_cipsi | Iterative Configuration Expansion Configuration Interaction (ICE-CI) |
| orca_cis | Excited states via CIS and TD-DFT |
| orca_cisresp | CIS response calculation |
| orca_compound | General driver of the ORCA compound language |
| orca_crystalprep | Set up an embedding calculation from a crystal structure file |
| orca_eca | Auxiliary program for solving magnetic model Hamiltonians |
| orca_eda | Energy decomposition analysis module |
| orca_esd | Excited state dynamics program for calculating vibronic spectra, resonance Raman, ... |
| orca_grad | General gradient module |
| orca_guess | Generation of an intial guess for SCF and CASSCF |
| orca_leanscf | Self consistent field program for HF and DFT |
| orca_lft | Ligand Field Theory |
| orca_loc | Calculation of localized molecular orbitals |
| orca_mcrpa | CASSCF linear response for excited states |
| orca_md | Molecular dynamics program |
| orca_mdci | Matrix driven correlation program: CI, CEPA, CPF, QCISD, CCSD(T) |
| orca_mm | Classical forcefield components |
| orca_mp2 | MP2 program (conventional, direct and RI) |
| orca_mrci | MRCI and MRPT calculations (individually selecting) |
| orca_ndoint | Calculates semiempirical integrals and gradients |
| orca_nmrspectrum | Simulates NMR spectra from calculated NMR parameters |
| orca_numfreq | Numerical Hessian computation |
| orca_pc | Addition of point charge terms to the one-electron matrix |
| orca_plot | Generation of orbital and density plots |
| orca_pop | External program for population analysis on a given density |
| orca_prop | Calculation of molecular properties |
| orca_propint | Calculation of property integrals |
| orca_rel | (Quasi) Relativistic corrections |
| orca_rocis | Excited states via the ROCIS method |
| orca_scfgrad | Analytic derivatives of SCF energies (HF and DFT) |
| orca_scfresp | self consistent field response |
| orca_startup | Calculation of startup data before each single point |
| orca_vpot | Calculation of the electrostatic potential on a given molecular surface |
| orca_vpt2 | VPT2 analysis |

