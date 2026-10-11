---
title: Relativistic corrections
source: https://www.faccts.de/docs/orca/6.1/tutorials/prop/relativistic.html
---

# Relativistic corrections

When calculating properties or geometries of systems that contain heavy elements (fourth row and beyond), relativistic effects can have a big impact and should not be ignored.
There are even studies that show that for some third row elements, relativistic effects can become significant.

Currently, there are four methods that can be used in ORCA to include that

1. Effective core potentials (ECPs)
2. Zeroth-Order Regular Approximation (ZORA, [[Baerends1996]](../bib.md#baerends1996))
3. Douglas-Kroll-Hess (DKH, [[Kroll1974]](../bib.md#kroll1974) [[Hess1985]](../bib.md#hess1985)) Hamiltonians of first and second order
4. spin-free variant of exact two component treatment (X2C, [[Weigend2013]](../bib.md#weigend2013))

They are somewhat different and have specific strengths - so
one should consider the results carefully - but maybe the most widely used is ZORA and its variants.

## Effective Core Potentials (ECPs)

Pseudopotentials or effective core potentials are a very convenient and efficient way to treat relativistic effects. They replace the core electrons with an effective potential that may cover
relativistic effects by parameterization. Another benefit of ECPs is the reduced number of electrons that have to be treated explicitly, thus reducing the computation time. One of the most prominent
and robust ECP families are the def2-ECPs by Dolg and co-workers.[[Dolg2000]](../bib.md#dolg2000) These are usually used in combination with the matching def2 basis sets by Ahlrichs.[[Ahlrichs2005]](../bib.md#ahlrichs2005)
Within ORCA these are automatically used if the respective basis set is requested. For example, if the def2-TZVP basis is used for a Hg atom the output will indicate the use of the respective ECP.

```text
!wB97X-V def2-TZVP

*XYZ 0 1 
Hg 0 0 0
*
```

```text
-------------------------
ECP PARAMETER INFORMATION
-------------------------

 Group 1, Type Hg ECP Def2-ECP (replacing 60 core electrons, lmax=3)
```

ECPs can further be assigned individually in the `%basis` block

```text
%basis
  ECP       "def2-ECP"     # All heavy elements for which the ECP is defined
  NewECP Pt "def2-SD" end  # Different ECP for Pt
end
```

Here, we defined the def2-ECP to all heavy elements and replaced it by the def2-SD ECP only for platinum.

> **Note**
> Many different ECP options are available within ORCA. However, the usage of ECPs is still an approximation that has to be made with care. A recent study by Head-Gordon [[Head-Gordon2023]](../bib.md#head-gordon2023)
> and co-workers discusses various ECP families and their strengths and weaknesses.

> **Warning**
> ECPs should never be used when core properties like NMR chemical shielding tensors are calculated!

## Scalar Relativistic Hamiltonians (ZORA/DKH/X2C)

An explicit relativistic treatment of the core electrons with  scalar-relativistic Hamiltonians like ZORA, DKH, or X2C is also possible. These can easily be envoked by the simple input keywords `ZORA`,
`DKH`, or `X2C`:

```text
!PBE0 D4 ZORA ZORA-DEF2-TZVP
```

or

```text
!PBE0 D4 DKH DKH-DEF2-TZVP
```

or

```text
!PBE0 D4 X2C X2C-TZVPALL
```

Note that here we are using specific basis for each method, named ZORA- or DKH-DEF2-TZVP, and X2C-TZVPALL. This is necessary because these basis have been specifically designed for these all-electrons calculations, and the relativistic correction should **NOT** be used together with the regular basis or pseudopotentials. For a detailed description of options, please check the
[ORCA manual](https://www.faccts.de/docs/orca/6.0/manual).

## RI and ZORA/DKH/X2C

If you want to use any of the RI methods to accelerate the SCF, another set of special /J basis has to be used:

```text
!PBE0 D4 ZORA ZORA-DEF2-TZVP RIJDX SARC/J
```

or

```text
!PBE0 D4 DKH DKH-DEF2-TZVP RIJDX SARC/J
```

or

```text
!PBE0 D4 X2C X2C-TZVPALL RIJDX X2C/J
```

For instance, the SARC/J auxiliary basis can be used for all the ZORA or DKH-DEF2 basis. If no specific basis is available, then one can always use AUTOAUX to automatically generate one.

> **Important**
> The SARC/J basis were optimized for RI on the SCF part, not the MP2 or higher-level correlated methods! For correlation specific /C basis consult the [ORCA manual](https://www.faccts.de/docs/orca/6.0/manual) and in case of abscence use !AUTOAUX.

## Example 1: the Hg dimer

Let's test the impact of these effects on the Hg dimer, that has an experimental bond length of $3.69 Å$ [[Sattler2017]](../bib.md#sattler2017).

[![hgdimer](../images/hgdimer.png)](../images/hgdimer.png)

The geometry can be optimized at a regular DFT level using the DEF2-TZVP basis, that makes use of pseudopotentials or using the all-electron Hamiltonians with matching basis sets:

```text
!PBE0 D4 DEF2-TZVP OPT

*XYZ 0 1
Hg 0 0 0
Hg 0 0 3
*
```

```text
!PBE0 D4 ZORA SARC-ZORA-TZVP SARC/J OPT
```

```text
!PBE0 D4 DKH2 SARC-DKH-TZVP SARC/J OPT
```

```text
!PBE0 D4 X2C x2c-TZVPall X2C/J OPT
```

> **Note**
> The auxiliary basis for the RIJ approximation used during the relativistic case here was chosen as the appropriate SARC/J.

We can now compare the obtained Hg-Hg bond lengths to the experimental value of 3.69 Å.

| Relativistic treatment | d(Hg-Hg) / Å |
| --- | --- |
| ECP | 3.64 |
| ZORA | 3.58 |
| DKH2 | 3.55 |
| X2C | 3.49 |
| Exp. | 3.69 |

In this case, the geometry optimized with the ECP basis set is closest to the experimental value. In general, all relativistic treatments drastically improve the agreement compared
to a non-relativistic all-electron calculation. This also shows, that ECPs are in many cases sufficient to optimize geometries.

> **Warning**
> Geometry optimizations using relativistic corrections turn on by default a one-center approximation by default, that changes the energy values.
> Do not compare single point energies from those you obtain from an !OPT run, these numbers are be incompatible.

## Example 2: ^119Sn NMR

In this example, we calculate the ^119Sn NMR chemical shift with different relativistic treatments. To do so, we calculate the magnetic shielding tensors of the reference molecule $SnMe_4$
and the investigated teravalent tin compound with the B97M-V functional.

[![27-snnmr](../images/27-snnmr.png)](../images/27-snnmr.png)

Respective inputs are:

```text
!B97M-V X2C X2C-TZVPALL RIJDX X2C/J

*XYZFILE 0 1 structure.xyz

%eprnmr
  Nuclei = all Sn {shift}
end
```

```text
!B97M-V ZORA ZORA-DEF2-TZVP RIJDX AUTOAUX

%basis
NewGTO Sn "SARC-ZORA-TZVP" end
end

*XYZFILE 0 1 structure.xyz

%eprnmr
  Nuclei = all Sn {shift}
end
```

```text
!B97M-V ZORA DKH-DEF2-TZVP RIJDX AUTOAUX

%basis
NewGTO Sn "SARC-DKH-TZVP" end
end

*XYZFILE 0 1 structure.xyz

%eprnmr
  Nuclei = all Sn {shift}
end
```

> **Note**
> Note that if your desired basis set for the nucleus of interest is not available for all elements in the
> molecule, you can define individual basis sets.

If we now calculate the approximated chemical shift as described in the [NMR spectroscopy](../spec/NMR.md)
tutorial, we obtain following values:

| Relativistic treatment | δ(^119Sn) / ppm |
| --- | --- |
| ECP | -6.0 |
| ZORA | -137.4 |
| DKH2 | -140.5 |
| X2C | -169.8 |
| Exp. | -115.5 |

Here, we see that employing an effective core potential (ECP) at the tin nucleus yields very bad results compared to the experiment. All other scalar-relativistic approaches yield reasonable agreement with the experiment considering the lack of spin-orbit coupling and environmental effects in our calculations.

### Structures Example 2

### SnMe4

```text
17

Sn    0.0005923   -0.0014311   -0.0010591 
C    -1.8246906    1.0428310    0.5123121 
H    -1.8968101    1.9779519   -0.0503263 
H    -1.8390187    1.2745996    1.5810708 
H    -2.6947269    0.4235163    0.2760765 
C     0.0022619   -0.4476130   -2.1196361 
H    -0.0615151    0.4762808   -2.7015104 
H    -0.8520890   -1.0814782   -2.3737238 
H     0.9217464   -0.9722039   -2.3946139 
C     0.1172065   -1.8479379    1.1228006 
H    -0.7382074   -2.4878220    0.8880831 
H     0.1142356   -1.6384147    2.1962259 
H     1.0361742   -2.3858484    0.8730152 
C     1.7072527    1.2423453    0.4747488 
H     2.6361335    0.7254508    0.2172133 
H     1.7197696    1.4744460    1.5434473 
H     1.6601065    2.1794430   -0.0872452 
```

### SnPh3(o-SMe-Bz)

```text
52

Sn    0.0042910    0.2777589    0.6815371 
S    -1.8228668   -2.1815750   -1.2865088 
C    -2.0834352    0.5257377    0.0403132 
H    -2.6651544   -0.2812639    0.4938959 
H    -2.4243327    1.4798780    0.4516251 
C    -2.1240841    0.5331602   -1.4466049 
C    -1.9690250   -0.6528583   -2.1950717 
C    -1.9186608   -0.6086149   -3.5892967 
H    -1.8073751   -1.5229476   -4.1627313 
C    -2.0027016    0.6076303   -4.2582191 
H    -1.9552523    0.6274544   -5.3432503 
C    -2.1531230    1.7882353   -3.5352860 
H    -2.2225303    2.7424243   -4.0498268 
C    -2.2173593    1.7422447   -2.1476695 
H    -2.3262702    2.6641442   -1.5803867 
C    -0.7961317   -3.2030334   -2.4024549 
H    -0.4686389   -4.0593611   -1.8072503 
H     0.0773629   -2.6279057   -2.7221497 
H    -1.3643593   -3.5639460   -3.2627402 
C     1.2652726   -0.4886069   -0.8834057 
C     1.3109506    0.1110170   -2.1468220 
H     0.7033664    0.9878017   -2.3633592 
C     2.1235662   -0.4108806   -3.1525605 
H     2.1433474    0.0630500   -4.1306974 
C     2.9047592   -1.5373593   -2.9059941 
H     3.5383994   -1.9439849   -3.6898085 
C     2.8696052   -2.1420015   -1.6511866 
H     3.4765671   -3.0218015   -1.4528113 
C     2.0532778   -1.6203522   -0.6489745 
H     2.0302475   -2.1087739    0.3240815 
C     0.7153143    2.2551627    1.1717372 
C     1.8937948    2.7523286    0.6053950 
H     2.4692081    2.1359903   -0.0834815 
C     2.3461288    4.0361317    0.9085482 
H     3.2628804    4.4082318    0.4582856 
C     1.6236995    4.8403236    1.7863726 
H     1.9744963    5.8412601    2.0232562 
C     0.4492510    4.3577740    2.3602410 
H    -0.1174189    4.9812496    3.0471452 
C    -0.0006141    3.0752690    2.0519541 
H    -0.9214039    2.7173913    2.5109503 
C     0.1850137   -0.9614959    2.4334013 
C     0.8673240   -0.4855370    3.5582255 
H     1.2988719    0.5141367    3.5525532 
C     1.0034379   -1.2781835    4.6971325 
H     1.5362198   -0.8948733    5.5636138 
C     0.4572175   -2.5589682    4.7239117 
H     0.5625341   -3.1778370    5.6110141 
C    -0.2251080   -3.0444526    3.6104513 
H    -0.6536009   -4.0433300    3.6273967 
C    -0.3606615   -2.2496217    2.4735304 
H    -0.8956996   -2.6426928    1.6110032 
```
