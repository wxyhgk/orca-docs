(sec:essentialelements.input)=
# General Structure of the Input File

In general, the input file is a free format ASCII file and can contain:
- one or more ["simple" keyword lines](sec:essentialelements.input.keywordlines) 
  that start with a "`!`" character, 
- one or more [input blocks](sec:essentialelements.input.blocks) 
  enclosed between an "`%`" sign and "`end`" that provide
  finer control over specific aspects of the calculation, 
- the [specification of the coordinates](sec:essentialelements.coordinates),
  total charge, and spin multiplicity for the system, either with a `%coords` block, 
  or more usually enclosed within two "`*`" symbols. 
  
Here is an example of a simple input file that contains all three input elements:

```orca
! HF def2-TZVP

%scf
   convergence tight
end

* xyz 0 1
C  0.0  0.0  0.0
O  0.0  0.0  1.13
*
```

Comments in the file start by a "\#". For example:

```orca
# This is a comment. Continues until the end of the line
```

Comments can also be closed by a second "\#", as the example below where
`TolE` and `TolMaxP` are two variables that can be user specified:

```orca
TolE=1e-5;    #Energy conv.#  TolMaxP=1e-6; #Density conv.#
```

The input may contain several blocks, which consist of logically related
data that can be user controlled. The program tries to choose sensible
default values for all of these variables. However, it is impossible to
give defaults that are equally sensible for all systems. In general the
defaults are slightly on the conservative side and more aggressive
cutoffs etc. can be chosen by the user and may help to speed things up
for actual systems or give higher accuracy if desired.

:::{note}
- The ORCA input is **NOT** case sensitive. UPPER CASE, lower case, or aNy cOMmBINAtiON are allowed.
  An exception is file names (e.g. for `%MOInp` or `*XYZName`), which are case-sensitive on Unix-like OSs.
- In general, the order of the simple keywords and input blocks is not important -- 
  see {ref}`sec:essentialelements.input.order` for the finer details.
:::

(sec:essentialelements.input.blocks)=
## Input Blocks

Input blocks start with "`%`", followed by the block name and end with "`end`". 
For example:

```orca
%method  
  method HF
END
```

A list of available input blocks is given in 
{numref}`sec:essentialelements.input.blocklist`.
No blocks *need* to be present in an input file but they *can* be
present if detailed control over the behavior of the program is desired.
Otherwise, most jobs can be defined via the simple keywords described in
{numref}`sec:essentialelements.input.keywordlines`. 
Variable assignments within blocks have the following general structure:

```orca
VariableName Value
# or with an optional "=" sign
OtherVariableName = OtherValue
```

Values can be either numeric, quote-delimited strings (see below), 
or predefined aliases (such as `HF` in the example above), 
which are internally converted to some numeric representation.

Some variables are actually arrays. In this case several possible
assignments are useful:

```orca
Array[1]  Value1
Array[1]  Value1,Value2,Value3
Array  Value1,Value2
```

:::{note}
Arrays always start with index 0 in ORCA (this is because ORCA
is a C++ program). The first line in the example gives the value
"`Value1`" to `Array[1]`, which is the *second* member of this array.
The second line assigns `Value1` to `Array[1]`, `Value2` to `Array[2]`
and `Value3` to `Array[3]`. The third line assigns `Value1` to
`Array[0]` and `Value2` to `Array[1]`. 
:::

Strings (such as filenames) must be enclosed in quotes. For example:

```orca
%scf
  MOInp  "Myfile.gbw"
end
```

Note that file names on Unix-like systems are case-sensitive 
(i.e., `MYFILE.GBW` and `MyFile.gbw` are different files). 
Under Windows the file names are not case sensitive.

Some input block keywords either open a nested sub-block, 
which must be closed with an additional `end`,
or have a specific syntax, different from the simple variable assignment described above.
For example:

```orca
%scf
  Guess PModel  # variable assignment
  SOSCF  # nested sub-block
    start 0.002  # variable assignment
  end  # closes the SOSCF sub-block
end
%mdci
  # special syntax
  MP2FragInter {1 1} {2 2}  
end
%basis
  NewGTO  # nested sub-block
    # special syntax inside
    H "def2-SVP"
    S 1
    1 0.05 1.0
  end  # closes the NewGTO sub-block
end
```

Finally, there are input "blocks" which only set a single variable 
and are not closed with "`end`".
These are listed in {numref}`tab:essentialelements.input.simpleblocks`. 
For example:

```orca
%MOInp "MyFile.gbw"
%maxcore 3000
```

(sec:essentialelements.input.order)=
## Input Priority and Processing Order

In more complicated calculations, the input can get quite involved.
Therefore it is worth knowing how it is internally processed by the
program:

- First, all the simple input lines (starting with "`!`") are
  collected into a single string.
- The program looks for all known keywords in a predefined order,
  regardless of the order in the input file.
- An exception are basis sets: if two different orbital basis sets
  (e.g. `!` `def2-SVP` `def2-TZVP`) are given, the latter takes
  priority. The same applies to auxiliary basis sets of the same type
  (e.g. `!` `def2/J` `SARC/J`).
- Some simple input keywords set multiple internal variables.
  Therefore, it is possible for one keyword to overwrite an option,
  set by another keyword. We have tried to resolve most such cases in
  a reasonable way (e.g. the more "specific" keyword should take
  precedence over a more "general" one) but it is difficult to foresee
  every combination of options.
- Next, the block input is parsed in the order it is given in the
  input file.
- Most block input keywords control a single variable (although there
  are exceptions). If a keyword is duplicated, the latter value is
  used.
- In principle, the same block may exist multiple times with different variables set within. 
  However, some blocks "reset" certain internal data whenever they are opened,
  or have certain mandatory contents, which must be present in each block instance
  (and override previous instances).
  Therefore, it is not recommended to have multiple instances of the same block.

Consider the following (bad) example:

```orca
! def2-TZVP UKS
%method
  functional BP86
  correlation C_LYP
  SpecialGridAtoms[1]  26, 27
  SpecialGridIntacc 8,  8,  8
  SpecialGridAtoms 28, 29
end
! PBE def2-SVP RKS
```

Using the rules above, one can figure out why it is equivalent to this
one:

```orca
! UKS BLYP def2-SVP
%method
  SpecialGridAtoms 28, 29, 27
  SpecialGridIntacc 8,  8,  8
end
```

(sec:essentialelements.input.globalmemuse)=
## Global Memory Use
Some ORCA modules (in particular those that
perform some kind of wavefunction based correlation calculations)
require large scratch arrays. Each module has an independent variable to
control the size of these dominant scratch arrays. However, since these
modules are never running simultaneously, we provide a global variable
`MaxCore` that assigns a certain amount of scratch memory to all of
these modules. Thus:

```orca
%MaxCore 2000
```

sets 2000 MB as the limit for these scratch arrays. **This
limit applies per processing core**. Do not be surprised if the program
takes more than that -- this size only refers to the dominant work
areas. Thus, you are well advised to provide a number that is
no more than 75-80% of your physical memory. 
Some memory-hungry operations will take longer if given less than the required memory,
while others will abort completely if `MaxCore` is insufficient.
The default value is 4GB, which is plenty for most standard DFT calculations.
For coupled clusters and the like, at least 8GB are recommended.

(sec:essentialelements.input.basename)=
## Changing the Default BaseName

ORCA generates a number of output files, as well as many temporary files,
which are removed at the end of a successful run.
To prevent filename clashes, all generated files start with the same prefix or *BaseName*.
This is usually inferred from the name of the input file by removing the extension,
i.e. running ORCA with `MyJob.inp` will create `MyJob.gbw`, `MyJob.properties.txt`, etc.
It is also possible to set the BaseName explicitly using the `%base` variable.
In the following example, the names of all generated files will start with `job1`,
regardless of the name of the input file:
```orca
%base "job1"
```

(sec:essentialelements.input.newjob)=
## Jobs with Multiple Steps

:::{warning}
The `$new_job` feature is a deprecated function. Using `$new_job` might
result in erratic results and strange behavior of succeeding calculations.
Please use the [compound](sec:workflowsautomatization.compound) feature
of ORCA for tasks like this -- it is safer and by far more powerful!
:::

ORCA supports input files with multiple jobs. This feature is designed
to simplify series of closely related calculations on the same molecule
or calculations on different molecules. The objectives for implementing
this feature include:

-   Calculate of a molecular property using different theoretical
    methods and/or basis sets for one molecule.

-   Calculations on a series of molecules with identical settings.

-   Geometry optimization followed by more accurate single points and
    perhaps property calculations.

-   Crude calculations to provide good starting orbitals that may then
    be used for subsequent calculations with larger basis sets.

For example consider the following job that in the first step computes
the g-tensor of BO at the LDA level, and in the second step using the
BP86 functional.

```{literalinclude} ../../orca_working_input/C03S04_018.inp
:language: orca
```

What happens if you use the `$new_job` feature is that all calculation
flags for the actual job are transferred from the previous job and that
only the changes in the settings must be input by the user. Thus if you
turn on some flags for one calculation that you do not want for the
next, you have to turn them off again yourself (for example the use of
the RI approximation)! In addition, the default is that the new job
takes the orbitals from the old job as input. If you do not want this
you have to overwrite this default by specifying your desired guess
explicitly.

(sec:essentialelements.input.blocklist)=
## List of Input Blocks

{numref}`tab:essentialelements.input.blocks` lists the known input block names,
along with any accepted synonyms/aliases.
The keywords defined in each block are listed in the respective section of the manual
and references to these lists are also given in the table.
The list of "blocks" which are not closed with `end` is given in 
{numref}`tab:essentialelements.input.simpleblocks`.

(tab:essentialelements.input.blocks)=
:::{flat-table} Input block keywords. Synonyms are given in parentheses.
:header-rows: 1
:class: longtable
* - Block
  - Description (Keyword Reference)
* - `autoci`
  - Autogenerated single- and multi-reference correlation methods 
    ({numref}`sec:modelchemistries.autoci.keywords`)
* - `basis`
  - Basis sets 
    ({numref}`tab:essentialelements.basisset.keywords.block`)
* - `casresp`
  - CASSCF static linear response 
    ({numref}`sec:spectroscopyproperties.casscfresp.keywords`)
* - `casscf`
  - CASSCF/NEVPT2 and DMRG calculations 
    ({numref}`sec:modelchemistries.casscf.keywords`)
* - `chelpg`
  - CHELPG charges 
    ({numref}`sec:spectroscopyproperties.pop.chelpg.basicusage`)
* - `cim`
  - Cluster-in-molecules calculations 
    ({numref}`sec:modelchemistries.mdci.cim`)
* - `cis` (`tddft`)
  - CIS and TD-DFT calculations
    ({numref}`sec:spectroscopyproperties.tddft.keywords`)
* - `compound`
  - Compound jobs
    ({numref}`sec:workflowsautomatization.compound`)
* - `conical`
  - Optimization of conical intersections
    ({numref}`sec:structurereactivity.conicalintersections`)
* - `coords`
  - Input of atomic coordinates
    ({numref}`sec:essentialelements.coordinates`)
* - `cosmors`
  - OpenCOSMO-RS options
    ({numref}`sec:essentialelements.solvationmodels.opencosmors.keywords`)
* - `cpcm`
  - Conductor-like Polarizable Continuum Model
    ({numref}`sec:essentialelements.solvationmodels.keyword-list.detailed`)
* - `docker`
  - Host-guest docking algorithm
    ({numref}`tab:structurereactivity.docker.keywords.block`)
* - `eda`
  - ({numref}`tab:NOCV_keywords`)
* - `elprop`
  - Electric properties
    ({numref}`sec:spectroscopyproperties.properties.elprop.keywords`)
* - `eprnmr`
  - EPR and NMR properties
    ({numref}`sec:spectroscopyproperties.properties.eprnmr`;
    g-tensor: {numref}`tab:spectroscopyproperties.epr.g.keywords.block`,
    HFC: {numref}`tab:spectroscopyproperties.epr.hyperfine.keywords.block`,
    ZFS: {numref}`tab:spectroscopyproperties.epr.D.keywords.block`,
    Mössbauer: {numref}`tab:spectroscopyproperties.moessbauer.keywords.block`)
* - `esd`
  - Excited state dynamics
    ({numref}`sec:spectroscopyproperties.esd.keywordlist`)
* - `frag`
  - Automatic fragmentation procedure
    ({numref}`tab:essentialelements.keywordlist`)
* - `freq`
  - Vibrational frequencies
    ({numref}`sec:structurereactivity.frequencies.keywords`)
* - `geom`
  - Geometry optimization
    ({numref}`tab:structurereactivity.optimization.keywords.geom`;
    Scan: {numref}`tab:geomscan.options`,
    TS: {numref}`tab:ts.options`)
* - `goat`
  - Global optimization algorithm
    ({numref}`tab:structurereactivity.goat.keywords.block`)
* - `ice` (`iceci`,`cipsi`)
  - Iterative configuration expansion CI calculations 
    ({numref}`sec:modelchemistries.iceci.keywords`)
* - `irc`
  - Intrinsic reaction coordinate calculations
    ({numref}`sec:structurereactivity.irc.keywords`)
* - `lft`
  - Ligand field theory utility `orca_lft`
    ({numref}`sec:utilities.lft`)
* - `loc`
  - Localization of orbitals
    ({numref}`sec:utilities.loc`)
* - `mcrpa`
  - CASSCF linear response
    ({numref}`sec:spectroscopyproperties.mcrpa.keywords`)
* - `md`
  - Molecular dynamics
    ({numref}`tab:moldyn:commands.overview`)
* - `mdci`
  - Single reference correlation methods
    ({numref}`sec:modelchemistries.mdci.keywords`;
    RHF EOM-CC: {numref}`tab:spectroscopyproperties.eom.options.rhfmdciblock`,
    UHF EOM-CC: {numref}`tab:spectroscopyproperties.eom.options.uhfmdciblock`,
    STEOM-CC: {numref}`sec:spectroscopyproperties.steom.general`,
    MR-EOM-CC: {numref}`sec:modelchemistries.mreom.details`,
    LED: {numref}`sec:spectroscopyproperties.led.features`,
    ADLD/ADEX: {numref}`sec:spectroscopyproperties.led.ad.keywords`,
    HFLD: {numref}`tab:spectroscopyproperties.hfld.keywords.block`)
* - `mecp`
  - Minimum energy crossing points optimization 
    ({numref}`sec:structurereactivity.mecp.keywords`)
* - `method`
  - Choice of computation method and various options
    - Run types and method classes: {numref}`tab:essentialelements.basics.keywords.block`
    - RI/COSX: {numref}`tab:essentialelements.ri.keywords.block`
    - Grids: {numref}`sec:essentialelements.numericalintegration.SCFkeys`
    - CP-SCF: {numref}`sec:essentialelements.cpscf`
    - Frozen core: {numref}`sec:essentialelements.frozencore`
    - Population analysis: {numref}`tab:spectroscopyproperties.pop.keywords.block.method`
    - DFT: {numref}`tab:modelchemistries.dft.gga.customizexc.keywords.block`
    - DFT/hybrid: {numref}`tab:modelchemistries.dft.globalhybrids.customization.keywords.block`
    - DFT/range-separated: {numref}`tab:modelchemistries.dft.rangeseparatedhybrids.customization.keywords.block`
    - DFT/double-hybrid: {numref}`tab:modelchemistries.dft.doublehybriddft.customization.keywords.block.method`
    - DFT/LibXC: {numref}`sec:modelchemistries.dft.libxc`
    - DFT/dispersion: {numref}`tab:modelchemistries.dispersioncorrections.dftd.keywords.block`
    - DFT/NLC: {numref}`tab:modelchemistries.dispersioncorrections.nl.keywords.block`
    - gCP: {numref}`tab:essentialelements.counterpoise.gcp.keywords.block`
    - NDO: {numref}`tab:modelchemistries.semiempirical.ndo.keywords.block`
    - Native xTB: {numref}`tab:modelchemistries.semiempirical.nativextb.keywords.methodblock`
    - FMM: {numref}`sec:multiscalesimulations.fmm.reco`
* - `mm`
  - Molecular mechanics force-fields
    ({numref}`sec:modelchemistries.mm-keywords`)
* - `mp2`
  - MP2 calculations
    ({numref}`sec:modelchemistries.mp2.standard`;
    DLPNO: {numref}`sec:modelchemistries.mp2.dlpno`,
    DLPNO/gradient: {numref}`sec:modelchemistries.mp2.dlpnograd`,
    DLPNO/response: {numref}`sec:modelchemistries.mp2.dlpnoresp`,
    DLPNO/multi-level: {numref}`sec:modelchemistries.mp2.multilevel`,
    OO-RI-MP2: {numref}`sec:modelchemistries.mp2.optmethod.usage`,
    regularized: {numref}`sec:modelchemistries.mp2.regularized`)
* - `mrcc`
  - Multi-reference CC calculations
    ({numref}`sec:modelchemistries.mrcc`)
* - `mrci`
  - Multi-reference CI calculations
    ({numref}`sec:modelchemistries.mrci.keywords`)
* - `mtr`
  - Normal mode trajectory/scan
    ({numref}`sec:spectroscopyproperties.tddft.scan.normalSurfaceScan`)
* - `nbo`
  - NBO analysis
    ({numref}`sec:spectroscopyproperties.nbo`)
* - `ndoparas`
  - Parameters for NDO-based semi-empirical methods
    ({numref}`tab:modelchemistries.semiempirical.ndo.paras`)
* - `neb`
  - NEB calculations
    ({numref}`sec:structurereactivity.neb.keywords`)
* - `numgrad`
  - Numerical gradients
    ({numref}`sec:essentialelements.numericalgradients`)
* - `output`
  - Control of output
    ({numref}`tab:essentialelements.output.printoptions.options`)
* - `pal`
  - Parallel jobs
    ({numref}`sec:essentialelements.parallel`)
* - `paras`
  - Input of geometric parameters, equivalent to `paras` or `pardef` in `%coords`
    ({numref}`sec:essentialelements.coordinates.parascan`)
* - `plots`
  - Plot generation
    ({numref}`sec:utilities.plots`)
* - `qmmm`
  - Multiscale (QM/MM) calculations
    ({numref}`sec:multiscalesimulations.qmmm.orca`)
* - `rel`
  - Relativistic options
    ({numref}`tab:essentialelements.relativistic.keywords.block`;
    SOC: {numref}`sec:spectroscopyproperties.soc`)
* - `rocis`
  - Restricted-open-shell CIS
    ({numref}`sec:spectroscopyproperties.rocis.keywords`)
* - `rr`
  - Resonance Raman and absorption/fluorescence band-shape calculations via `orca_asa`
    ({numref}`sec:spectroscopyproperties.asa.fitvalues`)
* - `scf`
  - SCF procedure settings
    ({numref}`sec:essentialelements.scfconvergence`;
    TRAH-SCF: {numref}`sec:essentialelements.scfconvergence.trahscf.keywords`,
    AVAS: {numref}`sec:modelchemistries.casscf.avas`,
    ROHF: {numref}`sec:modelchemistries.hftype.rohf`,
    native xTB: {numref}`tab:modelchemistries.semiempirical.nativextb.keywords.scfblock`,
    $\Delta$SCF: {numref}`tab:spectroscopyproperties.deltascf.options.scfblock`,
    initial guess: {numref}`sec:essentialelements.initialguess`,
    rotate MOs: {numref}`sec:essentialelements.initialguess.changes`
    )
* - `shark`
  - SHARK integral package
    ({numref}`sec:essentialelements.shark.keywords`)
* - `solvator`
  - Explicit solvation algorithm
    ({numref}`tab:structurereactivity.solvator.keywords.block`)
* - `symmetry` (`sym`)
  - Spatial symmetry recognition
    ({numref}`table:symmetry_block_options`)
* - `vpt2`
  - Vibrational perturbation theory
    ({numref}`sec:spectroscopyproperties.vpt2`)
* - `xtb`
  - Options for the `xtb` program interface
    ({numref}`tab:modelchemistries.semiempirical.xtb.keywords.block`)
:::

(tab:essentialelements.input.simpleblocks)=
:::{flat-table} Input keywords, which are prefixed with `%` but have no closing `end`.
:header-rows: 1
:class: longtable
* - Keyword
  - Value
  - Description (Reference)
* - `base`
  - `"<BaseName>"`
  - Base name for the files created by the job 
    ({numref}`sec:essentialelements.input.basename`)
* - `cclib`
  - `"<FileName>"`
  - File with one-particle coupling coefficients for ICE-CI
    ({numref}`sec:modelchemistries.iceci.cclib`)
* - `id`
  - `"<string>"`
  - **Deprecated!** Identifier for the job used to summarize computed energies
    ({numref}`sec:essentialelements.counterpoise.bbcp`)
* - `ljcoefficients`
  - `"<FileName>"`
  - File with Lennard--Jones coefficients for PHVA
    ({numref}`sec:structurereactivity.geomopt.partialhess`)
* - `maxcore`
  - `4096`
  - Maximum heap memory to use in MB, default: 4GB
    ({numref}`sec:essentialelements.input.globalmemuse`)
* - `moinp`
  - `"<FileName>"`
  - GBW file from which to read guess MOs for the `MORead` guess
    ({numref}`sec:essentialelements.initialguess.restart`)
* - `pointcharges`
  - `"<FileName>"`
  - File to read external point charges from
    ({numref}`sec:essentialelements.coordinates.pointcharges`)
:::

(sec:essentialelements.input.keywordlines)=
## Simple Keyword Lines

It is possible to give a line of keywords that assign certain variables
that normally belong to different input blocks. 
The syntax for this "simple input" is line-oriented. 
A keyword line starts with the "`!`" sign and can contain 
any number of space-separated keywords.
The input file can contain any number of keyword lines 
and they do not need to be at the beginning (although that is common practice) --
see also {ref}`sec:essentialelements.input.order`.

```orca
! Keyword1 Keyword2
! Keyword3
```

Most simple input keywords are documented in the relevant section of the manual.
{numref}`tab:essentialelements.input.keywordlines` 
provides references to these sections, grouped by topic.
Since simple keywords are usually related to variables within one or more input blocks,
it is also instructive to consult the documentation for the respective block -- 
see {numref}`tab:essentialelements.input.blocks`.

(tab:essentialelements.input.keywordlines)=
:::{flat-table} References to the documentation of simple input keywords. Related input blocks are also listed.
:header-rows: 1
:class: longtable
* - Keyword Group
  - Reference
  - Input block
* - Run types and method classes
  - {numref}`tab:essentialelements.basics.keywords.simple`
  - `method`
* - Basis sets
  - {numref}`tab:essentialelements.basisset.keywords.simple`
  - `basis`
* - DFT functionals
  - - LDA: {numref}`tab:modelchemistries.dft.local`
    - GGA: {numref}`tab:modelchemistries.dft.gga`
    - global hybrid: {numref}`tab:modelchemistries.dft.hybriddft.globlhybrids`
    - range-separated hybrid: {numref}`tab:modelchemistries.dft.rangeseparatedhybrids`
    - global double-hybrid: {numref}`tab:modelchemistries.dft.doublehybriddft.globaldoublehybrids`
    - range-separated double hybrid: {numref}`tab:modelchemistries.dft.doublehybriddft.rangeseparateddoublehybrids`
    - LibXC: {numref}`tab:modelchemistries.dft.libxc.simpleinput`
    - Non-local correlation: {numref}`tab:modelchemistries.dispersioncorrections.nl.keywords.simple`
  - `method`
* - Dispersion corrections
  - {numref}`tab:modelchemistries.dispersioncorrections.dftd.keywords.simple`
  - `method`
* - Composite (3c) methods
  - {numref}`tab:modelchemistries.3cmethods.keywords.simple`
  - 
* - NDO-based semi-empirical methods
  - {numref}`tab:modelchemistries.semiempirical.nativextb.keywords.simple`
  - `method`
* - Native xTB-based methods  
  - {numref}`tab:modelchemistries.semiempirical.ndo.keywords.simple`
  - `method`
* - Second order Møller--Plesset perturbation theory
  - {numref}`tab:modelchemistries.mp2.keywords.simple`
  - `mp2`
* - Single-reference correlated methods via MDCI
  - {numref}`tab:modelchemistries.mdci.keywords.simple`
  - `mdci`
* - Correlated methods using automatic code generation (AUTOCI)
  - {numref}`sec:modelchemistries.autoci.available`
  - `autoci`
* - CASSCF
  - {numref}`tab:modelchemistries.casscf.keywords.simple`
  - `casscf`
* - Multireference correlated methods via MRCI
  - {numref}`tab:modelchemistries.mrci.keywords.simple`
  - `mrci`
* - Excited states via correlated wavefunction-based methods
  - - EOM-CC: {numref}`tab:spectroscopyproperties.eom.options.simple`
    - STEOM-CC: {numref}`sec:spectroscopyproperties.steom`
    - others: {numref}`sec:spectroscopyproperties.excitedstates`
  - `mdci`
* - Initial guess
  - {numref}`tab:essentialelements.initialguess.keywords.simple`
  - `scf`
* - SCF procedure
  - {numref}`tab:essentialelements.scf.keywords.simple`
  - `scf`
* - Integral approximations (RI/COSX)
  - {numref}`tab:essentialelements.ri.keywords.simple`
  - `method`
* - Relativistic methods
  - {numref}`tab:essentialelements.relativistic.keywords.simple`
  - `rel`
* - Implicit solvation (CPCM)
  - {numref}`table:list-solvents`
  - `cpcm`
* - Spin-orbit coupling operator
  - {numref}`tab:spectroscopyproperties.soc.keywords.simple`
  - `rel`
* - Numerical integration grids
  - {numref}`tab:defgrids`
  - `method`
* - Integral storage and handling
  - {numref}`tab:essentialelements.integralhandling.keywords.simple`
  - `scf`
* - Population analysis
  - {numref}`tab:spectroscopyproperties.pop.keywords.simple`
  - `output`
* - Output control
  - {numref}`tab:essentialelements.output.simplekeywords.keywords`
  - `output`
* - Nudged elastic band method
  - {numref}`sec:structurereactivity.neb.keywords`
  - `neb`
:::
    
