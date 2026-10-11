---
title: Hello water! Your first ORCA calculation
source: https://www.faccts.de/docs/orca/6.1/tutorials/first_steps/first_calc.html
---

# Hello water! Your first ORCA calculation

Interactive structure (switch tabs to copy the ORCA input):

```mol
title: Water
theme: chem311
height: 360px
representation: ball-stick
--- xyz ---
3
water
O   0.0000   0.0000   0.0626
H  -0.7920   0.0000  -0.4973
H   0.7920   0.0000  -0.4973
--- input ---
!HF DEF2-SVP
* xyz 0 1
O   0.0000   0.0000   0.0626
H  -0.7920   0.0000  -0.4973
H   0.7920   0.0000  -0.4973
*
```

Our first calculation will be the energy of a water molecule, using Hartree-Fock theory and the DEF2-SVP basis. All you need to run ORCA is an input text file, such as this `water.inp`:

> **Note**
> The input usually has the .inp extension, but .txt is also ok.

We strongly recommend to create a new folder for any calculation. In this case we will create our input file in a new
directory called `firstcalc` and navigate to it.

Linux/Mac:

```text
mkdir ~/firstcalc
cd ~/firstcalc
```

Windows:

```text
mkdir C:\firstcalc
cd C:\firstcalc
```

(To find the Windows prompt, click windows key and type "prompt".)

You can now run ORCA. First, make sure that it is installed correctly and the system path is set (see [Assigning PATH variables](../first_steps/trouble_install.md#path-variable)).

```text
orca water.inp
```

The output is then printed on the screen.

## Save output to a file

To save the output in a text file `water.out` instead, use the `>` operator (on both Linux/Mac and Windows):

```text
orca water.inp > water.out
```

You can then open the file to see the output (make sure not to overwrite it while the calculation is running). More on the input and output analysis [next](../first_steps/input_output.md).

> **Note**
> You don't need to worry about the other programs in the installation folder for now, ORCA will take care of calling the right one when needed.
