```{only} html
<span data-index="remove-from-meili" hidden></span>
```

(sec:appendix.changelog)=
# Detailed change log

## Changes ORCA 6.1.1

### New Features

#### TD-DFT / CIS
- Natural transition orbitals (NTO) for spin-flip calculations (if invoked via the `%cis` block).

#### STEOM-CC
- Symmetry labels and $S^2$ values in RHF STEOM/IP/EA (previously only in UHF).
- Export STEOM singles amplitudes to JSON using `orca_2json`
  (requires `%mdci DoStoreSTEOM true end`).
- Export excitation energy, percentage active character,
  $S^2$ and optionally irrep for all roots to property file.

#### SOC-CI
- SOC-CI for HEAT thermochemistry.


### Fixed

#### DFT
- Crash for the Approximate Spin Projection Method (APM) with either
  analytical gradients + CPCM or `optTS` + `NumHess`
- Enabled calculations with D4 and point charges.

#### MP2
- Crash in orbital-optimized double hybrids.

#### DeltaSCF
- GMF now correctly allows for manually set saddle point orders different from the estimate.

#### TD-DFT
- Linear dependencies leading to 0 vector LUMOs.
- Restart fixed.
- sTDA/sTD-DFT absorption and CD spectra are compatible with `orca_mapspc` again.

#### ROCIS
- Crash for RIXS calculations with spin-orbit coupling.

#### (ST)EOM-CC
- Fixed parallel sync problem in UHF DressJK.
- Fixed parallel implementation for AO-K(C) in 3-internals dressing (UHF) with `DoCOSXEOM = true`.
- Fixed matrix containers in T1K/T1J and AO-K(C) (UHF EOM).
- Remove matrix containers after job is done.
- Use `orca_cis` for the CIS part in STEOM to improve stability and find low-lying states.
- Fixed problem of 1 beta-electron in DressJK.
- RHF STEOM: pass symmetry information to OPA.

#### AUTOCI
- Crash due to integer overflow in NEVPT4/FIC-MRCI/FIC-MRCC.
- Memory consumption over `%maxcore` due to batching mistake.
- High memory usage in amplitude printing.
- Response equations now abort if not converged.
- Reduced numerical noise in lambda and response equation and failures due to stagnation.
- Fixed crashes when gradient and response are both requested.

#### CASSCF
- Crash: `!MORead`/`!PAtom` and `!CMatrix` leading to non-orthogonal MO coefficients
  in case of linear dependencies in the basis set.
- Fixed `PModel` guess for CAS(0,0).
- Crash for combination of CPCM and NEVPT2-F12/DLPNO-F12.
- DMRG crashing with "number of Sweep_iteration less than Num_schedule" resolved.
- Crash when providing references in the ref sub-block `%casscf refs ...`.

#### MCRPA
- Fix for orbital trial vectors that have zero norm.

#### Molecular mechanics
- Random deviations in LJ/Coulomb energy/gradient due to `SwitchForceLJ` and `ShiftForceCoulomb`.

#### QM/MM
- Crash in FMM-QM/MM.
- GOAT with QM/MM: Fixed occasional crash when reading full structure ensemble.

#### Basis Sets
- Fixed pcH-n and aug-pcH-n basis sets.

#### Solvation
- Crash for DLPNO-CCSD/PTES with ANO basis.
- Crash for SMD + dummy atoms or point charges.
- Crash for `LRCPCM = false`.
- `MaxCore` not ignored anymore in ORCA/openCOSMO-RS calculations.
- Fixed chloroform for native ALPB.

#### Fragments
- GOAT missing fragment 0 printing.
- Fragmentator: fragment numbers fix on `Extend` and `NotAssigned`.

#### Geometry optimization
- `%geom MAXITER 50` was ignored.
- `OptimizeHydrogens` did not include all non-H dihedrals.

#### IRC
- Corrected order of `Monitor_internals`.
- IRC on TDDFT excited states.

#### GOAT
- GOAT-COARSE fragment counting on manual definitions.

#### DOCKER/SOLVATOR
- Solute fragment indices assigned by the Solvator now correctly start from 1.
- The DOCKER is only supposed to do single-points during the swarm step (not optimizations).
- Fix for failed optimizations during the DOCKER last step.
  These are now not saved into the final file anymore.

#### Hessian
- Crash of numerical Hessian with OOMP2 and OOCCD using `FrozenCore`.
- Crash of numerical Hessian with MDCI using `MDCI_DEN_NONE`.
- Crash of analytical Hessian with PGC.
- Store correct multiplicity in Hessian file.

#### EPR
- Crash in orbital hyperfine contribution (`Aorb`) with DKH.

#### EDA-NOCV
- The missing SMD–CDS term has been included in the EDA decomposition for implicit solvation methods.
- The nonlocal dispersion correction has been incorporated into the EDA decomposition
  for both self-consistent and non-self-consistent variants.
- The CPCM contribution has been removed from the Fock operator.
  The Delta CPCM dielectric term now represents the difference between the molecular
  and fragment dielectric contributions.
- For hybrid functionals, the Hartree–Fock exchange energy contribution has been excluded
  from the electrostatic term and added to the total exchange term.

#### Symmetry
- The defaults for input options `SymRelaxOpt` and `CleanUpGradient` in the `%Symmetry` input block have been changed.
  Redetermining the point group of a molecule during a geometry optimization is now disabled by default
  (`SymRelaxOpt false`) because ORCA by its design cannot handle a rotation of the molecule under these circumstances
  which would be needed to align the changed symmetry elements with the coordinate axes. Instead, the point group
  will be kept by removing all components from the gradient that are not totally symmetric (`CleanUpGradient true`).
- When performing an MOREAD guess, the irreducible representations of the guess orbitals are determined and the MOs
  are cleaned up by projection onto the symmetry-adapted orbitals.
- The CMATRIX and CACTIVE guess modes are now available with symmetry and may be selected by the user.
- Several bugs concerning the integration of symmetry into LeanSCF have been fixed.

#### Parallelization
- Multi-node runs for MCRPA and EDA.
- IAJB trafo disk usage increased with `NProcs` due to redundant writing per process.
- RPA-correlation energy was printed wrong in parallel.
- I/O race condition (unreproducible crashes) in USTEOM.
- Crash of UHF STEOM on multiple nodes.
- Parallel bug in GS-ROCIS preconditioner.
- Disabled group parallelization for GOAT, since cores are distributed automatically by GOAT.

#### JSON export
- Fixed X-Y amplitudes for TDDFT/RPA.

#### Property File
- Store numerically computed Hessian.
- `orca_pnmr` cannot find D-tensor in property file.
- JSON stored via `JSONPropFile True` not complete for certain run types.

#### Miscellaneous
- Fixed `NaN`s printed for MBIS charges in certain situations.
- SOC-CI sign error fixed.
- Prevent crash when ADLD(D3/D4) is performed with dummy or ghost atoms.
- For mixed Cartesian/internal coordinates, preserve the given internal connectivities.
- Bugs with missing response spin densities for UHF singlet.
- Lifted hard limits on number of atoms and basis functions in SHARK.
- ESD: J matrix was not being printed as unit matrix with `USEJ FALSE` (when it is ignored anyway).
- Wrong DOI for ORCA 6.0 citation.


### Improvements
#### DFT
- Reduced computation time for LibXC LDA functionals.

#### DeltaSCF
- The LSR1 preconditioner can now be updated with the lowest eigenvalues of the electronic Hessian
  to make variational collapse less likely.
- The GMF preconditioner can now be mixed with a dynamical gradient expansion preconditioner
  to make it more robust.

#### F12
- Added new keyword to define the maximum iterations in the CABS singles equations:
  `%method F12CABSSingles_MaxIter 100`.

#### Miscellaneous
- Optimized I/O for parallel runs in SOS EPR properties.
- Optimized formation of QDPT transition densities.
- Catch unavailable option combinations: AutoCI + Conventional, SDiagnostic + DLPNO.
- sTDA/sTD-DFT: print both length and velocity gauge CD spectra.


## Changes ORCA 6.1

### New Features

#### Startup, Guess, LeanSCF
- BUPO algorithm.
- Significant memory improvements in Startup, Guess and LeanSCF.

#### DFT
- Added B3LYP-3c method.
- Extension of HF-3c, PBEh-3c, B97-3c, and B3LYP-3c for elements Fr-Pu (using original D3 parameters)
  and r2SCAN-3c up to Lr (Z=103).
- ADFT (Energies, gradient, response, TD-DFT, NOT GIAO, NOT analytic Hessian).
- RPA correlation energy a la Andreas Görling (no gradient, density or response yet; NumGrad, NumFreq).
- Simple input keyword for B2NC-PLYP double-hybrid.
- Added various simple input `LibXC(method)` keywords for DFT functionals, e.g. TASK-LDA, revTM, HSE06, GAS22.

#### Native xTB Methods
- Native implementation of GFN1-xTB with energy & gradient.
- Native implementation of GFN2-xTB with energy & gradient.
- Native xTB methods can use the ORCA SCF and plotting infrastructure.
  Plotting of molecular orbitals, densities, and fractional occupation densities (FODs) can be done with `orca_plot`.
- Spin-polarized methods spGFN1-xTB and spGFN2-xTB.
- JSON parameter file for custom parameterizations of GFN1- and GFN2-xTB.
- Native implementation of the ALPB solvation model for xTB methods.

#### Solvation
- Analytical DRACO gradient.

#### SCF Linear Response
- Analytical Raman intensities: HF, DFT up to meta-GGAs, RIJ and COSX,
  implicit solvation, external point charges. Significantly faster than NumFreq.
- Static dip/dip/dip hyperpolarizability: same range of validity as Raman intensities.

#### Orbital localization
- IAO-based valence virtual orbital localization methods (`PMVVO`, `LIVVO`).
- Different options for IAO minimal basis.
- Optionally use a different localization method for virtual MOs via `%loc`.
- LMO plotting enabled in input file.

#### Optimization
- New redesigned L-OPT - an L-BFGS optimizer for geometry optimization of large systems -
  more efficient than before.
- !RIGIDBODYOPT for optimization of structures/fragments as rigid bodies.
- Replaced frozen coordinates (`$` syntax) with X/Y/Z Cartesian constraints.

#### NEB
- More robust initial path generation using S-IDPP.

#### Excited states
- Core ionization/excitation energies using UHF IP-EOM-CCSD and STEOM-CCSD.
- Multi-core calculations for RHF/UHF Canonical and BT-PNO IP-EOM and STEOM-CCSD
  (DLPNO for now can only do 1 core at the time).

#### GS-ROCIS:
- Spin-orbit coupling is now implemented.

#### DeltaSCF
- Generalized mode following method.
- Freeze-and-release method.

#### MDCI
- Add `DT_in_Triples` correction for RHF reference with a check to skip for small $F_{ia}$.

#### AutoCI
- Third order NEVPT (NEVPT3).
- Fourth order NEVPT restricted to singles and double excitation (NEVPT4(SD)).
- Export single-reference CI/CC 2RDM to JSON.
- UHF CCSDTQ.

#### AutoCI Response
- RHF CCSD dipole-dipole polarizability, with and without orbital relaxation.
- RHF and UHF CCSD(T) dipole-dipole polarizability, with and without orbital relaxation.
- RHF and UHF CCSD quadrupole-quadrupole polarizability, with and without orbital relaxation.
- RHF and UHF CCSD(T) quadrupole-quadrupole polarizability, with and without orbital relaxation.
- RHF and UHF GIAO-CCSD NMR shielding, with and without orbital relaxation.
- RHF and UHF GIAO-CCSD(T) NMR shielding, with and without orbital relaxtion.
- UHF GIAO-CCSD EPR g-Tensor, with and without orbital relaxation.
- UHF GIAO-CCSD(T) EPR g-Tensor, with and without orbital relaxation.

#### CASSCF Module
- ICE NEVPT2 using the full ranked formulation (ICE-FR-NEVPT2).
- Multiconfiguration pair density functional theory (MCPDFT)
  - with translated functionals tLDA, tPBE, and tPBE0
  - and with complex translated functionals ctLDA, ctPBE, and ctPBE0
- Long-range CASSCF short-range DFT (srDFT)
  - with short-range functionals sr-LDA, sr-PBE, and sr-PBE0
  - short-range pair density functionals: sr-ctLDA, sr-ctPBE, and sr-ctPBE0
  - robust RI approximation for range-separated integrals used for RI-J and RI integral transformation
- Effective Hamiltonian CI-DFT approach for excited states with MCPDFT and srDFT.

#### CASSCF Linear Response
- New options to toggle the orbital response, solution locking, and Olsen preconditioner in `%casresp` block.
- Nuclear-orbit perturbation implemented (allows for calculation of `Aorb` contribution to EPR A-tensor).
- Block preconditioner to reduce the number of iterations and computation time.

#### MR methods
- RASCI / ORMAS module.

#### MCRPA module
- Block preconditioner to reduce the number of iterations and computation time.
- Orbital response can be turned off. This corresponds to a CAS-CI calculation.

#### Multiscale
- Automated generation of QM and active regions.
- MM-only calculations can now make use of active atoms keyword.
- Added fast Simple_Eq option for topology preparation of QM/QM2 runs.

#### MD Module
- Langevin thermostats are now available (random force and drag term can be switched on separately).
- Constraints: Can now automatically constraint all bonds/angles involving a certain element (e.g. H).
- Restraints: Can now define custom restraint function by arbitrary mathematical expression.
- Added new "Radius of Gyration" Colvar (can restrain the system to spherical shape, e.g. a drop).
- Metadynamics: Can now define custom Colvars by arbitrary mathematical expression.
- Can now modify atom masses during MD simulation.
- Many more options for velocity initialization (e.g. let certain molecules rotate or translate).
- "Reference trajectory" feature to re-compute snapshots from an existing trajectory.
  Can also compute work along a path.
- Wavefunction extrapolation (ASPC) to reduce number of required SCF cycles.
- Possibility to apply additional arbitrary forces to atoms (e.g. for experiments with own bias potentials).

#### Thermochemistry
- Diagonal Born-Oppenheimer correction.
- Spin orbit coupling correction to the total energy via approximate 2 components.

#### NMR
- Enabled shielding calculations with X2C and the finite nucleus model.

#### Energy Decomposition and Wavefunction Analysis
- Atomic decomposition of London dispersion (ADLD).
- Atomic decomposition of exchange energy (ADEX).
- LED for covalent bonds (COVALED).
- New implementation of ETS-NOCV.
- Enabled LED with X2C Hamiltonian.
- RIJCOSX can now be used for DLPNO-CCSD(T)-LED with non-hybrid DFT as reference wavefunction.

#### AILFT
- Extended Spaces AILFT (ESAILFT).

#### Magnetic Relaxation Rates
- Orbach and Raman II pathways (`orca_magrelax`).

#### RESP/CHELPG charges
- RESP charges with parabolic and hyperbolic constraints.
- Can now define sets of equivalent atoms which will have identical charges.

#### ANISO
- Update of the ANISO interface in ORCA to support MRCI.

#### Basis Sets
- 6-31G* for Ga-Kr.
- CRENBL basis and CRENBL-ECP.
- New Jensen basis sets: pcX-n, aug-pcX-n, pcH-n, aug-pcH-n (n = 1,2,3,4).
- Reimplemented def-SVP, def-SV(P), def-TZVP, def-TZVPP (H-Lr).
- Extended def2-mSVP, def2-mTZVP, and MINIX up to Lr.
- Extended def2/J option for elements Fr-Lr.
- Extended def2/JK option for elements La-Lu, Fr-Lr.

#### Property File
- Added SCF and job timings.
- Added DBOC, gCP, and SOC energy contributions.
- Added ESD fluorescence rates.
- Easier conversion to JSON via `%output JSONPropFile=true`.

#### `orca_2json`
- Compute and export AO-basis Fock matrix as well as separate J, K, XC, and CPCM terms.
- Convert JSON property files back to native ORCA format
  (with limited support for 6.0 files).
- Added SOC integrals.

#### Miscellaneous
- Geometry input from GBW files.
- TransInvar for Numerical Hessian.
- Thermochemistry Compound script for the HEAT protocol by Stanton et al.


### Improvements

#### TDDFT
- Improved `FollowIRoot` stability.
- TD-DFT amplitudes now stored in GBW file.
- TD-DFT calculations are restartable from a GBW file.

#### GOAT
- GOAT-COARSE option for automated coarse-grained conformational search.
- GOAT-DIVERSITY for a conformational search looking for maximal structure diversity.

#### DOCKER/SOLVATOR
- Faster by about 100x, with many improvements and updates.
- DOCKER can now do the search only on limited region of the host by defining a center and extent of the search.

#### AutoCI
- Significantly improved scaling and runtime performance (speed, memory and disk space requirements)
  for AUTOCI-MP5 energy.
- Improved RHF CCSD(T) 2RDM performance.
- UHF CCSD(T) gradient accuracy (disconnected 3rd and 4th order contributions were missing, now corrected).
- Response: UHF CCSD Polarizability, solver performance improved significantly.
- Response: switched to sequential handling of response equations
  (less disk requirements for large calculations, compared to solving all perturbations together).
- Printing improvements.

#### CASSCF
- Aborts at beginning if CASSCF is requested with a dispersion correction.
- General warnings added about number of roots when CASSCF LR is run.
- TRAH submodule: final active orbitals are the same and sorted the same as in other CAS convergers.

#### CASSCF Linear Response
- More reasonable threshold for LR equation solution is determined by default.
- Uses solution locking by default.
- Checking at start that there are response parameters with which to perform LR calculation.

#### OpenCOSMO-RS
- Gas-phase orbitals can be used for the calculations in solution.

#### MD Module
- Added many more warnings (e.g. when two atoms come too close during a simulation).
- Added many different options how to handle non-converged SCF.
- Random velocity initialization now yields a zero angular momentum by default (i.e. system will not rotate).

#### Thermochemistry
- Extended max number of allowed temperatures and pressures to 100.

#### DKH
- Only compute the shell-pair data once.

#### X2C
- Skip grid setup if not needed.

#### OPS refactor
- Important: keywords to request multipolar spectrum has been simplified.
  Some Orca 6.0 keywords are no longer available.

#### QDPT module
- g-tensor `g(OZ/SOC)` now includes QED correction factor.
- g-tensor `ggauge` and `g(OZ/SOC)` can now be printed in molecular frame (with higher print level associated with QDPT).
- Enabled sum-over-states for CAS and MRCI.
- Reduced memory usage for SSC ZFS calculation.

#### Property File
- All properties and components now documented in the manual.
- Some components are now stored optionally/conditionally.
- Disable property file storage by default for `!MM` and `!GFN-FF`
  (in addition to `!GOAT` and `!MD-L-Opt`).
- Common component structure for energy properties:.
  `SCF_Energy`, `AutoCI_Energies`,
  `CAS_SCF_Energies`, `CAS_DCD_Energies`, `CAS_PT2_Energies`,
  `CIS_Energies`, `MDCI_Energies`, `MP2_Energies`.
- `Calculation_info`: Removed (unassigned) `NumOfFCElectrons` and `NumOfCorrElectrons`;
  moved "final single point energy" to geometry-dependent `Single_Point_Data` property.
- Stored MR-AUTOCI energies.
- Method-specific population analyses.
- Method- and state-specific nuclear gradient, removed `ATNO` component.
- `G_Tensor`: also store `g_PSO`, `g_DSO`, `Delta_g` components.
- `A_Tensor`, `EFG_Tensor`: removed `activeNucs`.

#### Miscellaneous
- Default MaxCore increased to 4GB.
- UCO/UNO generation performance improvement.
- Allowed simple input of DSD-PBEP86, DSD-BLYP and DSD-PBEB95 with D4.
- DeltaSCF: improved preconditioner with SOSCF.
- NEB: fragment preparation.
- Various improvements in `orca_mapspc`.
- Various fixes, additions, and improvements in Compound.


### Fixed

#### TDDFT
- DCORR should now respect MaxCore and abort neatly if it is insufficient.
- Wrong JSON output of TDDFT/TDA amplitudes and TDA excitation energy.
- Fix bug of TDDFT calculations with semiempirical methods.
- Fixed GS energy storage when SOC is enabled.

#### MDCI
- Respect MaxCore when building CPCM containers for PTE(S) and PTES.
- UHF-based CCSD producing wrong results with `!CONV`.
- Race condition resulting in wrong results in parallel for PTE(S) and PTES.
- S-diagnostic for canonical RHF and UHF.
- Fixed integral transformation problems.
- Fixed problems with Brückner and orbital optimized UHF CCD.
- Estimate required memory in RI/DLPNO exchange-like
  integral half-transformation to prevent OOM death.
- Stop calculation if MDCI equations do not converge (same as for SCF).
- Rare pair-pair integral crash.

#### MP2
- MP2 with ANOs works now.

#### CASSCF/NEVPT2
- FIX: Custom `EDIAG` failed due to wrong unit conversion - the input energies should now be in Eh.
- FIX: Increased number of states for custom EDIAG (hard-wired).
- FIX: Abort if an unsupported CI solver is requested with TRAH.
- CABSSinglesCorrection is now default in a DLPNO-F12-NEVPT2 (DoCABSSingles=1).
- FIX: MaxIter not properly passed in DLPNO-NEVPT2.
- FIX: QD-NEVPT2 densities not properly used in property calculations.
- FIX: NEVPT2 property calculations now track ground state changes.

#### MCRPA module
- Removed runtime bottleneck in final CI wave function printing
  that became an issue for many roots and long CI expansions.

#### QDPT Module
- `ggauge` was still using `CenterOfNucCharge` for magnetic gauge origin;
  now uses globally set magnetic origin.
- Other g-tensor fixes to first-order contributions (now consistent with `orca_prop`).
- Issues with QDPT transition densities from ROCIS.

#### CASSCF QDPT properties
- Corrected indexing of transition densities and ground-state spin densities.
   - Affected properties: EFG tensor, RHO, first-order g-tensor contributions, SOS properties.
- Memory issue in SSC calculation.

#### QDPT Module Sum-over-states
- Runs now if g-tensor is requested with `DoSOS true`
  (before, A-tensor had to also be requested).
- SOS g-tensor now gives full agreement with CAS LR (without orbital response)
  when all roots are included in CAS/MRCI QDPT calculation.
- Corrected general retrieval of transition spin densities.
   - NOTE: SOS is thus only available for methods where transition spin densities are available
           (now: MRCI, CASSCF, CASSCF+NEVPT2, CASSCF+Custom diagonal energies)

#### MD Module
- External forces on Colvars are now properly computed
  (relevant e.g. for thermodynamic integration).
- Many bugfixes (e.g. for the "too many arguments" bug).
- Gradients were not computed for CIS and broken symmetry.

#### Solvation
- Various options for CPCM: analytic, numeric RI, multipole.
- DRACO keyword not ignored anymore for QM/MM calculations.
- Fix crash for calculations requesting CPCM (bare CPCM / SMD / openCOSMO-RS)
  if the atomic number of an element in the solute is >= 106.

#### Dispersion
- Additional `!ATM` alias for the Axilrod-Teller-Muto type
  three-body-dispersion treatment available via `!ABC`.

#### EPR
- Crash in `orca_euler` when number of EFG and HFC nuclei differ.

#### NMR
- ZORA NMR now automatically triggers numeric GIAO 1-el integrals, as in ORCA 5.
- Fixed parallel race condition in DLU-X2C NMR leading to wrong results.
- `Tau=Dobson` default now correctly applied to GIAO calculations.
- Abort for NMR couplings with ZORA (not implemented).
- Fixed hanging of DSO coupling term with X2C when shieldings are also requested.
- Fixed GIAO XC integration for B97-3c with XCFun.

#### Optimization
- The "big step" fallback should also work if only Cartesian constraints are used.
- Switch off group parallelization if `(Re)CalcHess` is needed.

#### Relaxed Surface Scan
- Now it allows negative dihedrals on input, improved error report.

#### DOCKER/SOLVATOR
- Issue when swarming the best structures.
- Fix the chirality of the moment of inertia to avoid creating stereoisomers.
- Wall potential issue when some atoms are very far from the centroid.
- Small fix for solvent dimensions.

#### Hessian
- Fix for NearIR in `PrintThermoChem` if `InHessName` is different from `BaseName.hess`.
- Fixed issue when writing the IR spectrum multiple times.

#### X2C
- Disable general contraction for decontracted ANO basis, which led to slowdown.
- CIS/TDDFT gradients with X2C were not picture-change corrected.

#### Thermochemistry
- D(inf)h point group was not correctly parsed for rotational entropy contribution.

#### Inertia Tensor
- VPT2 and PAF : Fixed Inertia Tensor calculation.

#### Rotational Constants
- Minor fixed on unit transformation constants.

#### Basis sets
- All of SHARK and ORCA now works up to L=10 (except Hessian).

#### SCF Linear Response
- Fixed issue with initialization of BHP22 solver.

#### Windows
- Windows-specific crash in `orca_mapspc` fixed.
- Parallel subcalculations in NumCalc (NEB, NumGrad, VPT2, ...) now also available on Windows

#### Property File
- Re-implemented JSON output via the N. Lohmann library (version 3.11.3)
  to guarantee valid syntax.
- Alleviated memory and timing overhead.
- Respect `%output PropFile=false`/`!NoPropFile` keywords.
- `Quadrupole_Moment`: `EXZ` and `NUCXZ` components held YZ value instead.
- Hessian was stored incorrectly in XTB jobs.
- CIS/TDDFT gradient root was stored incorrectly.
- `Chemical_Shift` components `SPSO`, `SDSO`, and `saniso` were not stored.
- `Calculation_Info` was not stored in some calculations.
- MM, XTB, and ExtOpt jobs now store the geometry and final energy.
- Geometry in JSON output was missing ghost, fragment, and ECP data.

#### Miscellaneous
- Crash in SOSCF.
- Cleanup leftover files of stability analysis with DFT.
- Atomic fitting density not working with partial general contraction.
- Occasional crash in integral loop.
- Missing PDB file output in QM/MM NEB.
- Prevent crash when reading the nodefile in GOAT, NumFreq, etc.
- Bug in one-sided numerical gradient `TransInvar=true`.
- Restored functionality of `!AIM`.
- Removed leftover temporary files in AUTOCI.
- Restore original irreps if the prediagonalization is skipped in SCF.
- Crash in Hessian for systems with no beta electrons.
- Restored functionality of the `!DoEQ` keyword.
- Opt+NumFreq or Opt+IRC jobs with `!ExtOpt` were stopping after the optimization.
- Print headers for all monitored internals in IRC.
- Fixed HFLD when no pairs are identified.
- Removed RIJCOSX-only restriction for wB97X-3c.
- CP-SCF now aborts if unconverged.
- RI Trafo in CIPSI works now.
- Fixed memory leaks in AO-MP2, QDPT, `orca_2json`, ECPs, ROCIS, LFT, and others.
- Spectrum intensity printing and decomposition in `orca_mapspc` for cases beyond the dipole approximation.
- `orca_vpot`: Fixed ESP calculation when contraction change.


### Removed

#### CASSCF/NEVPT2
- QD-NEVPT2 with Cloiszeaux Hamiltonian (QDType=QD_Cloiszeaux).
- Some options for the handling of reduced density matrices in NEVPT2  (D4Step=core, D4Step=D4PT).

#### MCRPA module
- If the eigenvalue equations fail to converge,
  the connection to CASSCF wave function instability is not mentioned anymore.
  The manual section has also been removed.


## Changes ORCA 6.0.1

### Fixed

#### DFT
  - Crash when XCFun functional was overwritten with LibXC.
  - Hessian fixed for DFT GGA, NoRI, RKS.
  - VV10 Hessian is blocked even if invoked with `CALC_HESS=TRUE` and similar.
  - Wrong orbitals for non-self-consistent DFT-NL calculations (wB97M-V, wB97X-V, B97M-V).
  - `X_WR2SCAN`:
    - Exchange can now be specified individually in the `%method` block.
    - Fixed crashes when second derivatives are requested.
    - TRAH is now disabled per default when using `X_WR2SCAN`.
    - If second derivatives are requested, will now automatically switch to numerical second derivatives.
    - Added appropriate warnings for the above changes.
  - Fixed PBEh-3c gCP parameters for Krypton and Lithium to be consistent with Grimme's stand-alone.
  - gCP is now fixed (and extended) for r2SCAN-3c up to Z=103.
  - Remove restriction to COSX for wB97X-3c .
#### TD-DFT
  - Ground state gradient for TDDFT calculations with `sgradlist` was wrong.
  - `DCORR` 2/3 with `DoSCS` giving wrong results in parallel.
  - (D)-Correction not available for full TDDFT.
  - Fix for memory estimates for Hessian/TDDFT when running without COSX.
  - `FollowIRoot` was not supposed to do anything if the overlap was to small, was still updating.
  - Fixed interface to `BHP22` solver in CIS.
#### MP2
  - Crash in conventional U-MP2.
  - Parallel crash in RI-MP2 density.
  - Crash in (RI-)MP2 gradient with SMD.
  - Crash in (RI-)MP2 density with PGC and RIJK.
  - MP2+CPCM gradient was wrong.
  - Crash in NearIR + B2PLYP.
  - Bug with MP2 gradient in property file.
#### MDCI
  - SemiCore was not applied correctly if ECP is present.
  - ECP-related crashes.
  - Fixed redundant integral generation for specific problems.
  - Restored old CITrafos to address reported performance issues.
  - Added missing 4th-order doubles term in (T) for RKS reference (already present in UKS-(T), RKS-DLPNO-(T), and UKS-DLPNO-(T) and zero for RHF/UHF reference).
  - UHF CIS/STEOM calculation with `UseCISUpdate` is set to `false`.
  - RHF STEOM: TD-DFT initial guess.
#### AutoCI
  - Fixed large stack allocation, e.g., in MRCC.
  - Fixed runtime behavior for `!Moread Noiter` (falsely reporting "not converged").
  - Fixed `!UseSym` falsely aborting.
  - AutoCI gradients: abort at start of a calculation when RI is requested instead of after coupled cluster iterations.
#### CASSCF/NEVPT2/QD-NEVPT2
  - Issue running LR over SA-CASSCF solution.
  - Incorrect setting of gauge origin in CASSCF QDPT led to misleading output and in some cases complained about not being able to find densities for the origin evaluation.
  - Canonicalize the inactive and virtual spaces of AVAS guesses, to avoid spurious warnings about core orbitals in the following CASSCF calculation.
  - AVAS: fixed wrong number of occupied orbitals in case no occupied orbitals should have been selected.
  - TRAH-CASSCF: compute generalized Fock matrix which is needed for the CASSCF nuclear gradient.
  - Fixed redundant generation of coupling coefficients in the CI guess.
  - Fixed ABS/CD spectra in calculation with !UseSym and QD-NEVPT2: The wrong densities were picked for the CASSCF transition moments.
  - Fixed ABS/CD when the NEVPT/QD-NEVPT2 ground state differs from CASSCF. Respecitve transition were missing.
  - Fixed MCD spectra not using transition densities from QD-NEVPT2 for the flag `DoFullSemiclassical=true`.
  - Updated manual: Reported `D4TPre` are updated to the new default value 1e-12. ORCA 5 used `D4TPre=1e-10`.
  - Fixed closed-shell case, e.g. CAS(6,3), crashing in NEVPT2.
  - Fixed NEVPT2/FIC-NEVPT2 wrong energies or crashing for the Vija class to wrong addressing.
  - Fixed ICE densities not stored in density container.
#### ANISO
  - Fixed T and L matrices passed to the single-aniso.
  - Fixed wrong number of non-relativistic states passed to single-aniso.
#### QDPT
  - Corrected QDPT transition density for excitations beyond "none".
  - Information added to QDPT AMatrix.
  - Issues in QDPT properties in `orca_lft` have been addressed.
#### QM/MM
  - Speed issue for QMMM optimizations.
  - Crystal-QMMM and compound crashed.
  - Removed leftover files from QMMM-IRC amd QMMM-NEB.
#### Relativity
  - Crash for F12 + X2C/ZORA/DKH.
  - Unnecessary abort in AutoCI gradients with X2C/DKH/ZORA.
  - Disabled X2C+GIAO+FiniteNuc (not yet implemented).
  - 2nd-order PC correction to DKH gDSO now skipped when `fpFWtrafo==false` due to numerical instability.
#### Solvation
  - Disabled analytical gradient and Hessian for XTB calculations requesting CPCMX (not implemented).
  - FINAL SINGLE POINT ENERGY for calculations requesting CPCMX was wrong.
  - Crash for calculations requesting Freq + CPCM + dummy atoms.
  - Crash for QM/QM2 calculations with CPCM requesting excited states.
  - Crash for multiple XYZ File Scans for DRACO.
  - Crash with CPCM + NoIter + Pal + open-shell.
  - Fix for GC and CPCM. 
#### Optimization
  - Multi-XYZ optimization crash.
  - Random possible break when using GFN-xTB Hessian.
  - Random crashes for `RECALC_HESS=TRUE`.
  - COPT was saving wrong Cartesian Hessian under certain conditions, would break.
  - Maximum number of angles that can be included is fixed + better error message.
  - Analytic Hessian as initial Hessian option crashed with IRC.
  - Crash in NEB-TS with subsequent Hessian, caused by change of number of parallel processes for NEB (max 32).
  - NEB parallelization (will - again - automatically start in parallel, if enough processes are available).
#### GOAT
  - GOAT/DOCKER/SOLVATOR now running on Windows.
  - WorkerRandomStart fixed and working as intended.
  - `-REACT` and `-EXPLORE` were (by mistake) not included sqrt(NFrag) to number of opts.
  - Missing timings for GOAT.
#### DOCKER
  - Abort if all final optimizations fail, was ending normally.
  - Do not switch to COPT if constraints are given.
#### Stability analysis
  - Stability analysis + closed-shell systems + post-processing (Hirshfeld, NBO, ...).
  - `SkipSecondSTAB` was still checking for energy differences between steps. Now will move on regardless.
#### `orca_2json`
  - Exported relativistic integrals were wrong in, HMO and angular momentum were missing.
  - Choice of origin corrected.
  - Empty `[]` and `[""]` are no longer crashing but disabling the options.
  - Invalid property JSON syntax in the following cases:
    - multiple geometries (e.g. optimizations);
    - some jobs with multiple properties of the same kind;
    - CIPSI energies;
    - MDCI EOM energies;
    - XTB jobs;
    - energy extrapolation.
#### `orca_mapspc`
  -  XAS/XES broadening functions satisfy FWHM.
  -  Adjusted .stk files normalization to report band integrals.
#### Compound
  - MORead with same type and number of atoms but different arrangement.
  - Bugs in statistical functions.
#### Miscellaneous
  - SOMF(1X) parallel bug in semi-numeric Coulomb.
  - Dummy/ghost atoms lead to crash in Hessian (partial fix).
  - Fixed bug of Fermi smearing calculations of two-electron systems.
  - Hangup in `leanscf_aftermath` when using F12 and ECPs.
  - Issues in RIXSSOC, XESSOC spectra in ROCIS have been addressed.
  - Issues in computing RI-SSC Integrals have been addressed. This property is now turned on in CASSCF, LFT and MRCI modules.
  - Fixed a crash in MD and L-OPT when the input file name was "orca".
  - Default COSX algorithm is set to AUTO everywhere, as originally intended.
  - Disable frozen-core approximation when no frozen-core electrons are present.
  - `orca_vib` was not able to read hess file from AnFreq run.
  - For very small systems restart Hessian could crash.
  - Small deviations between the Guess CI Matrix and the Sigma Vector in GS-ROCIS.
  - DCD-CAS: Removed left-over files.
  - Uncontracted MRCI: Fixed partial general contraction calls in the MRCI integral transformation (crashed before).
  - Crash for geometry optimization followed by a vibrational frequency calculation with fixed point group Ci.
  - Removal of `posix_memalign`, due to glibc/kernel bug.
  - NBO communication fixed.
  - Fixes a crash in the integral transformation.
  - Crash in `orca_vpot` due to missing prescreening matrix.

### Improvements

#### Output
  - Print all orbital energies for `!PrintMOs` and `!LargePrint`.
  - Removed redundant warning when using gCP for elements Z > 36 (Kr).
  - Added citations for wr2SCAN and DFT-D4 extension.
  - Better printing of the spin coupling situation of the states resulting from GS-ROCIS calculations.
  - Prepended a counter to irrep labels when printing vibrational frequencies.
#### `orca_2json`
  - Citations added to json output file.
  - Absolute path in basename possible.
#### `orca_mapspc`
  - Added support for VCD, XASSOCV and XESSOCV spectrum processing.
#### Symmetry
  - Ensured correctness of gradient cleanup, geometry optimizations with fixed point groups and calculations of vibrational frequencies  (for point groups with real irreps using pure Hartree-Fock).
  - Ensured correctness of the petite-list algorithm for SCF energy and gradient.
#### Compound
  - Implemented automatic knowledge of basenames.
  - Added GOAT interface.
#### Miscellaneous
  - Added ASCII checker to input file.
  - Add the possibility to read multi-XYZ files with no '>'.
  - QDPT in CASSCF now uses the magnetic origin as defined in `%eprnmr` (if not set, defaults to CenterOfNucCharge for backwards compatibility).
  - Reduced disk usage and optimized performance for CASSCF (transition) densities in density container.
  - Keep topology in initial IDPP path generation.
  - Add CIS Gradient in property file.






## Changes ORCA 6.0.0

### SCF and Infrastructure

- Significant improvements to the SOSCF solver to make it more robust, preventing huge steps that break the SCF. Overall improvements on the DIIS solvers.
- Due to the SCF updates, the AutoTRAH is now not so often needed and will start now only from above 50 cycles (`AutoTRAHIter`).
- Improvements to the memory handling of TD-DFT, CP-SCF and the Hessian

### Basis sets

- def-TZVP and ma-def-TZVP pseudo-potential basis sets for the actinides (Z = 89, Ac - 103, Lr)
- Lehtola's hydrogenic gaussian basis set family (HGBS) including polarized (HGBSP) and augmented (AHGBS, AHGBSP) variants for all elements up to Oganesson (Z = 118)
- def2-SVPD, def2-TZVPD, def2-TZVPPD, def2-QZVPD, def2-QZVPPD basis sets for lanthanoids
- vDZP Grimme's double-zeta valence basis set
- `!MINIX` now correctly activates the corresponding ECP
- Added user-specified L-limit to AutoAux `AutoAuxLLimit`
- Fixed segfault in dhf-ECP
- Fix for `DelECP` in `%coords`
- Added `ReadFragBasis` keywords read fragment-specific basis sets from a file

### Solvation

- New charge correction / compensation algorithm (corrected charges printed in an additional file)
- C-PCM/B scheme for QM/MM calculations
- DDCOSMO and CPCM/X available for XTB calculations and QM/MM calculations
- Generalization of names within all solvation models (C-PCM/SMD/ALPB/DDCOSMO/CPCM-X)
- New discretization scheme for the cavity (C-PCM) based on a constant number of charges per unit of area
 
### DFT

- Allow LibXC functional customization via external parameters
- Simple input keywords added for some LibXC functionals
- Added wB97M(2) functional parameters: must be used with wB97M-V orbitals in a two-step job (compound script available)
- D4 for elements 87 (Fr) - 103 (Lr)
- r2SCAN-3c extension to elements 87 (Fr) - 103 (Lr)
- Simple input keyword for functionals with revised D4 parameters by Grimme (wB97X-D4rev, wB97M-D4rev)
- New hybrid functionals: r2SCANh, r2SCAN0, r2SCAN50, wr2SCAN, wB97X-3c
- New double-hybrid functionals: Pr2SCAN50, Pr2SCAN69, wPr2SCAN50, kPr2SCAN50
- Simple input keywords for 2021 variants of revDSD-PBEP86-D4 and revDOD-PBEP86-D4
- Bugfixes for LibXC combined `*_xc_*` functionals
- Fixed crash for D4 + ghost atoms

### Excited states

- Analytical gradient for meta-GGA functionals
- Small bugfix to spin-adapted triplets and NACMEs.
- The FolllowIRoot for excited state optimization uses now a much more robust algorithm.
- New implementation for UHF EOM-CCSD and STEOM-CCSD.
- Core ionization/excitation energies using UHF IP-EOM-CCSD and STEOM-CCSD. 

### Relativity

- Enabled `NumGrad` with relativistic methods
- Second order DKH picture-change correction of contact density
- Minor fixes in DKH picture-change corrections of magnetic properties
- Picture change corrections are activated automatically

### Multiscale

- Reading PDB files for 10k+ atoms with HETATMs now possible
- Enabled correct FlipSpin behavior with QMMM
- More efficient MM Module
- Implemented wall potential

### Coupled cluster / DLPNO

- Implemented energy ordering for PNO generation
- Added semicore treatment for DLPNO
- Enable DLPNO-CCSD(T) calculations to run DLPNO-CCSD unrelaxed densities

### MP2
- Corrected memory estimates and batching in response and gradient
- Removed the slow and limited analytic (RI-)MP2 Hessian code
- Removed non-default Gamma-in-core option for RI-MP2 response
- Disabled single-precision calculations
- Disabled SemiDirect option in AO-MP2
- Enabled range-separated DHDFT gradients with RIJDX

### NEB

- Improved IDPP initial path
- More efficient GFN-xTB runs for NEB

### COSX

- Improvements to numerical integration grids, both for DFT and COSX
- Faster grid step
- Improved performance and accuracy in COSX, also for the gradient and Hessian

### Properties

- NMR spin-spin coupling: 
  - Added `SpinSpinElemPairs` and `SpinSpinAtomPairs` keywords to limit which couplings are computed
  - Reduced the number of CP-SCF perturbations necessary via a stochastic selection 
  - DSO term was transposed.
  - Off-diagonal PSO elements had the wrong sign
  - Efficiency improvement: solve SD/FC CP-SCF equations in restricted mode for RHF, instead of always using UHF
- Optimized numeric integration for HFC gauge correction
- Removed `RITRAFO` option for CP-SCF
- Switched to `tau=Dobson` as default handling of the kinetic energy density in meta-GGA magnetic properties with GIAOs

### Hessian

- Improvements to the Hessian to avoid accumulation on numerical noise and reduce the number of spurious negative frequencies.

### Geometry Optimization

- Several improvements to the geometry optimization, making is much more stable. Complete redesign of the Cartesian optimizer (!COPT), making it quick enough to be used together with faster methods.
- Fallbacks in the geometry optimization in case something fails, e.g. if the internal coordinates are unacceptable.
- Arbitrary spherical, ellipsoidal or box-like wall potentials can be added, which will reflect on the energy and gradients and can be used during geometry optimization.

### Symmetry

- To be filled in

### Miscellaneous

- CHELPG charges that reproduce the ESP together with the molecular dipole moment
- Fixed issues with constraints in multi-step jobs
- Molden output: store ECP info in `[Pseudo]` block, set point charge atomic number to 0, handling of ghost atoms
- Made the `ExtOpt` interface easier to use
- Store energy from NEB and IRC in the XYZ file
- The definitions of the real solid harmonic orbitals used in ORCA have been documented in this manual
  in {numref}`sec:orca_2json.real_solid_harmonics` for angular momentum quantum numbers $\ell\le 8$
