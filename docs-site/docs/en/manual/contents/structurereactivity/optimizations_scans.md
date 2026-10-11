<a id="sec:structurereactivity.optimization.scans"></a>
# Surface Scans  

Relaxed surface scans are an invaluable tool when exploring potential energy surfaces. They allow the user to vary one or more coordinates (bond lengths, angles, or dihedrals) while relaxing the remaining degrees of freedom. This section outlines the theoretical background, gives practical examples, and summarizes relevant input keywords.

---
<a id="sec:structurereactivity.optimization.relaxedsurface"></a>
## Theory  

In a relaxed surface scan, a selected coordinate is varied over a defined range, and at each point, a constrained geometry optimization is performed. This can reveal transition states, reaction mechanisms, or approximate energy barriers. ORCA supports scans over bond lengths (`B`), bond angles (`A`), and dihedral angles (`D`).

Multiple coordinates can also be scanned either independently (nested loops) or simultaneously using the `Simul_Scan` keyword, the latter reducing computational cost.

---

## Simple Example  

The following input scans the bond length between C and O from 1.35 Å to 1.10 Å in 12 equidistant steps. Each step involves a constrained geometry optimization.

```
! B3LYP SV(P) Opt
%geom 
     scan
        B 0 1 = 1.35, 1.10, 12 # C-O distance that will be scanned
     end
end

* int 0 1
    C  0 0 0 0.0000   0.000    0.00
    O  1 0 0 1.3500   0.000    0.00
    H  1 2 0 1.1075 122.016    0.00
    H  1 2 3 1.1075 122.016  180.00
*
```

!!! note

    -   As in constrained geometry optimizations it is possible to start the
        relaxed surface scan with a different scan parameter than the value
        present in your molecule. But keep in mind that this value should
        not be too far away from your initial structure.

## Complex Example  

A more challenging example is shown below. Here, the H-atom abstraction
step from $\text{CH}_4$ to OH-radical is computed with a relaxed surface scan
(*vide supra*). The job was run as follows:

```
! B3LYP SV(P) Opt SlowConv NoTRAH
%geom 
    scan 
        B 1 0 = 2.0, 1.0, 15 
    end 
end
* int 0 2
 C     0   0   0   0.000000     0.000     0.000
 H     1   0   0   1.999962     0.000     0.000
 H     1   2   0   1.095870   100.445     0.000
 H     1   2   3   1.095971    90.180   119.467
 H     1   2   3   1.095530    95.161   238.880
 O     2   1   3   0.984205   164.404    27.073
 H     6   2   1   0.972562   103.807    10.843
*
```

It is obvious that the reaction is exothermic and passes through an
early transition state in which the hydrogen jumps from the carbon to
the oxygen. The structure at the maximum of the curve is probably a very
good guess for the true transition state that might be located by a
transition state finder.

You will probably find that such relaxed surface scans are incredibly
useful but also time consuming. Even the simple job shown below required
several hundred single point and gradient evaluations (convergence
problems appear for the SCF close to the transition state and for the
geometry once the reaction partners actually dissociate -- this is to be
expected). Yet, when you search for a transition state or you want to
get insight into the shapes of the potential energy surfaces involved in
a reaction it might be a good idea to use this feature. One possibility
to ease the burden somewhat is to perform the relaxed surface scan with
a "fast" method and a smaller basis set and then do single point
calculations on all optimized geometries with a larger basis set and/or
higher level of theory. At least you can hope that this should give a
reasonable approximation to the desired surface at the higher level of
theory -- this is the case if the geometries at the lower level are
reasonable.

<a id="fig:13"></a>
*Relaxed surface scan for the H-atom abstraction from CH$_4$ by
OH-radical (B3LYP/SV(P)).*

## Multidimensional Scans

After several requests from our users ORCA now allows up to three
coordinates to be scanned within one calculation.

```
! B3LYP SV(P) Opt
%geom 
     scan
        B 0 1 = 1.35, 1.10, 12 # C-O distance that will be scanned
        B 0 2 = 1.20, 1.00, 5  # C-H distance that will be scanned
        A 2 0 1 = 140, 100, 5  # H-C-O angle that will be scanned
     end
end

* int 0 1
    C  0 0 0 0.0000   0.000    0.00
    O  1 0 0 1.3500   0.000    0.00
    H  1 2 0 1.1075 122.016    0.00
    H  1 2 3 1.1075 122.016  180.00
*
```

!!! note

    -   For finding transition state structures of more complicated reaction
        paths ORCA now offers its very efficient NEB-TS implementation (see
        section
        [structurereactivity.neb](neb.md#sec:structurereactivity.neb)).

    -   2-dimensional or even 3-dimensional relaxed surface scans can become
        very expensive - e.g. requesting 10 steps per scan, ORCA has to
        carry out 1000 constrained optimizations for a 3-D scan.

    -   The results can depend on the direction of the individual scans and
        the ordering of the scans.

Simultaneous multidimensional scans, in which all scan coordinates are 
changed at the same time, can be requested via the following keyword (which
brings the cost of a multidimensional relaxed surface scan down 
to the cost of a single relaxed surface scan):

```orca
%geom 
  Scan B 0 1 = 3, 1, 15 end
  Scan B 1 2 = 1, 3, 15 end
  Simul_Scan true
end
```

<a id="sec:structurereactivity.optimization.multiplexyz"></a>
## Multiple XYZ File Scans

A different type of scan is implemented in ORCA in conjunction with
relaxed surface scans. Such scans produce a series of structures that
are typically calculated using some ground state method. Afterwards one
may want to do additional or different calculations along the generated
pathway such as excited state calculations or special property
calculations. In this instance, the "multiple XYZ scan" feature is
useful. If you request reading from a XYZ file via:

```orca
* xyzfile Charge Multiplicity FileName
```

this file could contain a number of structures. The format of the file
is:

```orca
Number of atoms M
  Comment line
AtomName1 X Y Z
AtomName2 X Y Z
...
AtomNameM X Y Z
Number of atoms M
  Comment line
AtomName1 X Y Z
...
```

Thus, the structures are simply of the standard XYZ format and they are
provided one after the other. There is no need to add any extra character between
them. This was the case for ORCA versions older than 6.0.0, where the
structures were separated by a "\>" sign. The user can still use this format, if
preferred, but is not needed anymore. After processing the XYZ file, single point
calculations are performed on each structure in sequence and the results
are collected at the end of the run in the same kind of trajectory`.dat`
files as produced from trajectory calculations.

In order to aid in using this feature, the relaxed surface scans produce
a file called `MyJob.allxyz` that is of the correct format to be re-read
in a subsequent run.

<a id="sec:structurereactivity.optimization_scan.keywords"></a>
## Surface Scan Keywords

<a id="tab:geomscan.options"></a>
!!! note "`%geom` block input keywords and options for surface scanned geometry optimization."


| ****Keyword**** | Option / Value | Description |
| --- | --- | --- |
| **`Scan`** | `B 1 2 = v1, v2, N` | Scan atom 1 to atom 2 bond distance from v1 to v2 in N steps. |
| **—** | `B 1 2 [v1 v2 ...]` | Scan atom 1 to atom 2 bond with custom step values. |
| **—** | `A 1 2 3` | Scan an angle using atoms 1,2,3. |
| **—** | `D 1 2 3 4` | Scan a dihedral of atoms 1,2,3,4. |
| **`Simul_Scan`** | `true` | Enable simultaneous multidimensional scans (up to 3 coordinates). |
| **`FullScan`** | `true` | Forces full surface scan before TS optimization (`!ScanTS`). |

