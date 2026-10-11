---
title: Input and Output
source: https://www.faccts.de/docs/orca/6.1/tutorials/first_steps/input_output.html
---

# Input and Output

## Structure of the input

Everything that comes after the "!" is called the `main input`, and if specific options are necessary, they will be usually set in a section initiated by a % symbol and closed by and END.

Suppose, in the water case, one wants to increase the maximum number of SCF iterations to 500, then the input should be:

```mol
title: input_output #1
theme: chem311
height: 360px
representation: ball-stick
--- xyz ---
3
structure
O   0.0000   0.0000   0.0626
H  -0.7920   0.0000  -0.4973
H   0.7920   0.0000  -0.4973
--- input ---
!HF DEF2-SVP
%SCF
   MAXITER 500
END
* xyz 0 1
O   0.0000   0.0000   0.0626
H  -0.7920   0.0000  -0.4973
H   0.7920   0.0000  -0.4973
*
```

The main input can also be split over many lines, for the sake of readability, for instance:

```mol
title: input_output #2
theme: chem311
height: 360px
representation: ball-stick
--- xyz ---
3
structure
O   0.0000   0.0000   0.0626
H  -0.7920   0.0000  -0.4973
H   0.7920   0.0000  -0.4973
--- input ---
!HF
!DEF2-SVP
%SCF
   MAXITER 500
END
* xyz 0 1
O   0.0000   0.0000   0.0626
H  -0.7920   0.0000  -0.4973
H   0.7920   0.0000  -0.4973
*
```

For a complete discussion of all the main keywords and options, check the [ORCA manual](https://www.faccts.de/docs/orca/6.0/manual).

> **Note**
> The input reader is **not** case-sensitive. UPPER CASE, lower case, or aNy cOMmBINAtiON are allowed.

### Structure section

After the main input and options, comes the structure section, separated by stars. You can input the coordinates in Cartesian form, using the "xyz" flag or in Internal coordinates, using "int". Then come the system's charge and multiplicity ($2S+1$).

For a hydroxide radical ($S=1/2$) in internal coordinates, one input could be like:

```text
!HF DEF2-SVP
* int 0 2
O  0 0 0 0.0    0.0 0.0
H  1 0 0 0.9903 0.0 0.0
*
```

> **Note**
> The atoms can be chosen by their symbol (H, C, Cu, Te) or by atomic number (1, 6, 29, 52), and the coordinates must be in Ångström.

### Reading from external file

The geometry can also be read from an external .xyz file using the "xyzfile" flag. In the previous case, if one had a "hydroxide.xyz" file in the same folder as the input, the input would be:

```text
!HF DEF2-SVP
* xyzfile 0 2 hydroxide.xyz
```

In this case, there is no need to close the section with a second star below. The "hydroxide.xyz" should look like:

```mol
title: input_output #5
theme: chem311
height: 360px
representation: ball-stick
--- xyz ---
2
structure
O  0 0 0
H  0 0 0.9903
```

It starts with the number of atoms, then comes a blank or comment line and then the structure - with coordinates in Angstroem.

## The output file

The first part of the output is a header with references to contributors and basis set information. After that come the WARNINGS, that should be carefully checked and:

```text
****************************
* Single Point Calculation *
****************************
```

as a reference to the kind of calculation that will be performed. Then comes detailed information about the integral module (SHARK) and SCF parameters:

```text
----------------------
SHARK INTEGRAL PACKAGE
----------------------

Number of atoms                             ...      2
Number of basis functions                   ...     19
Number of shells                            ...      9
Maximum angular momentum                    ...      2
Integral batch strategy                     ... SHARK/LIBINT Hybrid
RI-J (if used) integral strategy            ... SPLIT-RIJ (Revised 2003 algorithm where possible)
Printlevel                                  ...      1
Contraction scheme used                     ... SEGMENTED contraction

[...]

------------
SCF SETTINGS
------------
Hamiltonian:
 Ab initio Hamiltonian  Method          .... Hartree-Fock(GTOs)

General Settings:
 Integral files         IntName         .... orca
 Hartree-Fock type      HFTyp           .... UHF
 Total Charge           Charge          ....    0    
 Multiplicity           Mult            ....    2

[...]
```

Then the initial guess is built:

```text
------------------------------
INITIAL GUESS: MODEL POTENTIAL
------------------------------
Loading Hartree-Fock densities                     ... done
Calculating cut-offs                               ... done
Initializing the effective Hamiltonian             ... done
Setting up the integral package (SHARK)            ... done
Starting the Coulomb interaction                   ... done (   0.0 sec)
Making the grid                                    ... done (   0.0 sec)
Mapping shells                                     ... done
Starting the XC term evaluation                    ... done (   0.0 sec)
Transforming the Hamiltonian                       ... done (   0.0 sec)
Diagonalizing the Hamiltonian                      ... done (   0.0 sec)
Back transforming the eigenvectors                 ... done (   0.0 sec)
Now organizing SCF variables                       ... done
```

and if the SCF converges, you will see a message, together with a discrimination of the energy components:

```text
*****************************************************
               *                     SUCCESS                       *
               *           SCF CONVERGED AFTER  11 CYCLES          *
               *****************************************************

             **** ENERGY FILE WAS UPDATED (orca.en.tmp) ****

----------------
TOTAL SCF ENERGY
----------------

Total Energy       :        -75.32415421767207 Eh           -2049.67444 eV

Components:
Nuclear Repulsion  :          4.27488404160356 Eh             116.32551 eV
Electronic Energy  :        -79.59903825927563 Eh           -2165.99995 eV
One Electron Energy:       -112.46709636116736 Eh           -3060.38528 eV
Two Electron Energy:         32.86805810189173 Eh             894.38533 eV

Virial components:
Potential Energy   :       -150.52264633450642 Eh           -4095.92944 eV
Kinetic Energy     :         75.19849211683436 Eh            2046.25500 eV
Virial Ratio       :          2.00167107208270
```

The orbitals energies are printed, along with information on charges and timings. If some other method is required, such as MP2 or TD-DFT, it will appear next and the final calculated energy is printed as:

```text
-------------------------   --------------------
FINAL SINGLE POINT ENERGY       -75.324154217672
-------------------------   --------------------
```

after which an overview of calculated properties, the dipole moment, and the rotational spectrum for
the system are printed. In the end, recommended citations for the methods and implementations
used in your calculation are printed alongside the timings. For more details on how to cite ORCA
properly, see the [How to cite tutorial](../first_steps/howtocite.md).

## Visualization programs

If you want to visualize the data using a graphical user interface, there are many programs you can
find online. Some that have proven specifically useful for ORCA output visualization are [Avogadro](https://avogadro.cc), [Chemcraft](https://www.chemcraftprog.com/), [Gabedit](https://sites.google.com/site/allouchear/Home/gabedit/download), and [ChimeraX](https://www.rbvi.ucsf.edu/chimerax/).

For details, refer to the [Graphical User Interfaces (GUI)](../first_steps/GUI.md) section.
