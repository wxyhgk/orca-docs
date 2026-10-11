(sec:workflowsautomatization.compound_examples)=
# Compound Examples

(sec:workflowsautomatization.compound_examples.introduction)=
## Introduction

A library of compound scripts exist in page https://github.com/ORCAQuantumChemistry/CompoundScripts .

(sec:workflowsautomatization.compound_examples.HelloWorld)=
## Hello World

**Introduction**

This is the simplest script that nevertheless points to an important feature of *Compound*. That is the fact that *Compound* does not have to run an actual 'normal' ORCA calculation but it can also be used as a driver for various tasks, in this case to just print a message.

**Filename**

helloWorld.inp

**SCRIPT**
```{literalinclude} ../../orca_working_input//compound_library_examples/helloWorld.inp
:language: orca
```


## New Job

**Introduction**

One of the features of ORCA that will be deprecated in the future and should not be used any more is the *'New_Job'* feature. The current script is a simple example how *Compound* can be used to just run a series of calculations.

**Filename**

replaceNewJob.inp

**SCRIPT**
```{literalinclude} ../../orca_working_input//compound_library_examples/replaceNewJob.inp
:language: orca
```

**Comments**

From the *Compound* point of view the syntax in this script is not the most efficient one. It can be rewritten in more compact, cleaner, general way. Neverteless this is meant only as an exmample of how *Compound* can replace older ORCA calculations that used the, to be deprecated, *'New_Job'* feature. 

## High Accuracy

**Introduction**

This is a script that utilizes the scheme by N. J. DeYonker, T. R. Cundari, and A. K. Wilson published on: J. Chem. Phys. 124, 114104 (2006). The script calculates accurate total energies of molecules.

**Filename**

ccCA_CBS_2.cmp

**SCRIPT**
```{literalinclude} ../../orca_working_input//compound_library_examples/replaceNewJob.inp
:language: orca
```

**Comments**

It is interesting that in this scheme the total energy is treated and there is not separation in extrapolation between HF energy and correlation energy.

## Scan
**Introduction**

This is an example script for a 1-Dimensional geometry scan. It is set up for the Ne-Ne bond distance but can be modified to suit the user's specific needs.

**Filename**

scan_1D_1M_1P.cmp

**SCRIPT**
```{literalinclude} ../../orca_working_input//compound_library_examples/scan_1D_1M_1P.cmp
:language: orca
```

**Comments**

This script has some interesing features. It contains two variables *removeFiles* and *DoPython*. If the first of them is set to *true* then the script will use a system command to remove files that are not needed anymore after the end of the calculation. The latter, *DoPython*, if set to *true* will read the *.csv* file that is created and write a *python* file to make a plot of the results. Then it will run the python script to actually make the plot.


## Numerical polarizabilities


**Introduction**

This script calculates numerically the polarizability of the molecule using single point calculations with an electric field. 

**Filename**

numericalPolarizability.cmp

**SCRIPT**
```{literalinclude} ../../orca_working_input//compound_library_examples/numericalPolarizability.cmp
:language: orca
```

**Comments**

In this script we also use the linear algebra *diagonalize* function that is available in *Compound*.

(sec:workflowsautomatization.compound_examples.iterativeopt)=
## Iterative optimization
**Introduction**

This is a script that will perform a geometry optimization, then run a frequency calculation and in case there are negative frequencies it will adjust the geometry, based on the Hessian, and optimize again.

**Filename**

iterativeOptimization.cmp

**SCRIPT**
```{literalinclude} ../../orca_working_input//compound_library_examples/iterativeOptimization.cmp
:language: orca
```

## Gradient extrapolation

**Introduction**

This script extrapolates the gradient of a molecule. It uses a two point extrapolation where the Hartree-Fock and correlation parts of the gradient are extrapolated separately. This opens the way for geometry optimizations with extrapolated gradients.

**Filename**

gradientExtrapolation.cmp

**SCRIPT**
```{literalinclude} ../../orca_working_input/compound_library_examples/gradientExtrapolation.cmp
:language: orca
```

**Comments**

## BSSE Optimization

**Introduction**

This script optimizes the geometry of a molecule using gradients corrected for Basis Set Superposition Error (BSSE) correction. The basic step is the usage of a second script that calculates BSSE corrected gradients. 

**Filename**

BSSEOptimization.cmp

**SCRIPT**
```{literalinclude} ../../orca_working_input/compound_library_examples/BSSEOptimization.cmp
:language: orca
```

**Comments**

The initial structure should contain some ghost atoms.

## Umbrella script 
**Introduction**

This script calculates the potential for the "umbrella effect" in NH_3. In addition it locates the minima and maxima in the potential surface.

**Filename**

Umbrella.cmp

**SCRIPT**
```{literalinclude} ../../orca_working_input/compound_library_examples/Umbrella.cmp
:language: orca
```

## Multi reference
**Introduction**

This is a script that calculates the atomic electron denstities in free atoms and makes a library of them.

**Filename**

atomDensities.inp

**SCRIPT**
```{literalinclude} ../../orca_working_input/compound_library_examples/atomDensities.inp
:language: orca
```

**Comments**

Here, it's interesting to note that depending on the selected atom, the script either performs a CASSCF calculation, which provides details such as the number of electrons and number of roots, among other parameters, or it carries out a simple Hartree-Fock calculation.


## GoTo
**Introduction**

This is a brief example demonstrating how the *GoTo* command can be used in *Compound*.

**Filename**

goTo_Example.inp

**SCRIPT**
```{literalinclude} ../../orca_working_input/compound_library_examples/goTo_Example.inp
:language: orca
```
