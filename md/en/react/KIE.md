---
title: Kinectic Isotope Effects (KIE)
source: https://www.faccts.de/docs/orca/6.1/tutorials/react/KIE.html
---

# Kinectic Isotope Effects (KIE)

Kinetic isotope effects (KIE) are changes in reaction rates caused by a change in a given isotope in a molecule. That is caused due to the difference in mass, that affects vibrational frequencies and/or tunneling probabilities.

It is an effect often exploited to investigate reaction mechanisms, when there is bond breaking or forming to an atom that can be substituted by an isotope.
These KIE are predictable, depending on the mass ratios, and thus can be used to validate proposed mechanisms.
The origin of the KIE is related to a change on the **Zero Point Energy** (ZPE) of the system, that is affected when the vibrational frequencies are lowered or increased due to the mass change.
For the heavier deuterium the vibrational frequencies are lowered, thus lowering the ZPE and altering the free energy barrier.

[![kie](../images/kie.png)](../images/kie.png)

*Figure: Schematic origin of the KIE.*

Typically, the KIE is quantified by the ratio of the reaction rates of both reactions $\frac {k_H} {k_D}$. This can be calculated from the free energy reaction barriers of both reactions according to:

$$
\frac {k_H} {k_D} = e^{-(\Delta G^{\ddagger}_H - \Delta G^{\ddagger}_D) / RT}
$$

To obtain these barriers, we can use the usual [transition state search and optimization](../react/nebts.md) algorithms in ORCA, we just have to adjust the mass of the respective atoms
to simulate the corresponding isotopes. This can be easily done via the geometry input within the ORCA input file:

```text
!wB97X-3c

* XYZ 0 1
  H     -2.411352    1.128722    0.029849		<= Hydrogen
  H     -1.342943    1.352019   -0.097229 M 2.0141	<= Deuterium
*
```

Here, we adjusted the mass of H to 2.0141 amu which corresponds to deuterium.

## Example 1: H-atom Abstraction

In this example, we use ORCA to make a quantum-mechanical prediction of the KIE for the H-atom abstraction from methane by the hydroxyl radical. The respective KIE ratio
is known from highly accurate gas-phase experiments ($6.75 \pm 0.83$).[[Tully1993]](../bib.md#tully1993)

[![reaction2](../images/reaction2.png)](../images/reaction2.png)

First, we searched for the transition states of the respective reactions with the [NEB-TS](../react/nebts.md) method. In this case, we employed the ωB97X-3c composite method. It is
based on a range-separated hybrid functional that is specifically suited to compute transition states and reaction barriers at a reasonable cost. Note, that we also adjusted the temperature
for the [thermochemistry calculation](../prop/thermo.md) to obtain free energies at the same conditions as in the experiment (T = 293 K). We further optimize the isolated reactants for both cases.
The respective inputs can be found in the tabs below:

NEB-TS $CH_4$

```text
!wB97X-3c NEB-TS FREQ

%FREQ   
 TEMP 293     
END

%NEB 
 NEB_END_XYZFILE "products.xyz"
 PREOPT_ENDS true
END

*XYZ 0 2
C     -2.42007     1.14475     0.00503
H     -1.37176     1.42602    -0.24888
H     -2.95035     0.87504    -0.97240
H     -2.97696     2.02414     0.50780
H     -2.39461     0.26127     0.72431
O      1.11295     1.79481    -0.12688
H      0.85814     0.90892     0.95813
*
```

NEB-TS $CD_4$

```text
!wB97X-3c NEB-TS FREQ

%FREQ   
 TEMP 293     
END

%NEB 
 NEB_END_XYZFILE "products-deuterated.xyz"
 PREOPT_ENDS true
END

*XYZ 0 2
C     -2.42007     1.14475     0.00503
H     -1.37176     1.42602    -0.24888 M 2.0141
H     -2.95035     0.87504    -0.97240 M 2.0141
H     -2.97696     2.02414     0.50780 M 2.0141
H     -2.39461     0.26127     0.72431 M 2.0141
O      1.11295     1.79481    -0.12688
H      0.85814     0.90892     0.95813
*
```

Opt OH

```text
!wB97X-3c OPT FREQ

%FREQ   
 TEMP 293 
END

*XYZ 0 2
O      1.11295     1.79481    -0.12688
H      0.85814     0.90892     0.95813
*
```

Opt $CH_4$

```text
!wB97X-3c OPT FREQ

%FREQ   
 TEMP 293 
END

* XYZ 0 1
C     -2.42007     1.14475     0.00503
H     -1.37176     1.42602    -0.24888
H     -2.95035     0.87504    -0.97240
H     -2.97696     2.02414     0.50780
H     -2.39461     0.26127     0.72431
*
```

Opt $CD_4$

```text
!wB97X-3c OPT FREQ

%FREQ 
 TEMP 293 
END

* XYZ 0 1
C     -2.42007     1.14475     0.00503
H     -1.37176     1.42602    -0.24888 M 2.0141
H     -2.95035     0.87504    -0.97240 M 2.0141
H     -2.97696     2.02414     0.50780 M 2.0141
H     -2.39461     0.26127     0.72431 M 2.0141
*
```

After the successful NEB-TS calculations, we obtain the respective optimized transition states:

[![kie-ts](../images/kie-ts.png)](../images/kie-ts.png)

*Figure: Transition states of the H-atom abstraction from methane and deuterated methane.*

Single imaginary frequencies of -1312.67 $cm^{-1}$ for the hydrogen case and -977.51 $cm^{-1}$ for the deuterated transition state verify the structures to be true transition states and
already reflect the KIE.

The activation barriers $\Delta G_H^{\ddagger}$ are now calculated as the difference of the free energy of the transition state and the sum of the free energies of the isolated reactants.
For our example, we obtain 47.63 and 53.14 $kJ \cdot mol^{-1}$, respectively. From these values, a $\frac {k_H} {k_D}$ ration of 9.2 is calculated. This value is in reasonable agreement with the experimental value of $6.75 \pm 0.83$.

> **Important**
> By simply computing the KIE in terms of changes on the free energy barriers like that, we are not considering any tunneling effects. Those can be quite important, and sometimes need to be included using
> one of various different approaches, e.g. [[Aquilanti2019]](../bib.md#aquilanti2019).

### Structures

### Encounter Complex Reactants

```text
7

C     -2.42007     1.14475     0.00503
H     -1.37176     1.42602    -0.24888
H     -2.95035     0.87504    -0.97240
H     -2.97696     2.02414     0.50780
H     -2.39461     0.26127     0.72431
O      1.11295     1.79481    -0.12688
H      0.85814     0.90892     0.95813
```

### Encounter Complex Products

```text
7

C     -2.640806    0.931381    0.002030
H      0.593417    1.397564   -0.537054
H     -3.426646    1.364904   -0.619289
H     -1.670863    1.425720    0.075351
H     -2.839810    0.009183    0.550600
O      0.590809    2.120231    0.105838
H      0.558140    1.654177    0.952824
```

### OH

```text
2

O           1.07245474036562      1.65402139061456      0.04555342747891
H           0.89863525963438      1.04970860938544      0.78569657252109
```

### CH4

```text
5

C          -2.42279670517834      1.14622317818710      0.00323817339640
H          -1.40192098310125      1.43684600255195     -0.23012434766673
H          -2.93991006551667      0.87362369062480     -0.91291202682640
H          -2.93736663378777      1.97868527517785      0.47584250425215
H          -2.41175561241597      0.29584185345830      0.67981569684457
```

### CD4

```text
5

C          -2.42279665366144      1.14622313561044      0.00323814877091
H          -1.40192106623947      1.43684582662702     -0.23012433408547
H          -2.93991000369491      0.87362377747566     -0.91291195537196
H          -2.93736668375609      1.97868503351161      0.47584254392506
H          -2.41175559264808      0.29584222677526      0.67981559676145
```

### TSH

```text
7

C          -0.77611078480638     -0.11113494264923     -0.05780330905632
H           0.40528667930059      0.09836365588496     -0.23895997983456
H          -1.25333044819185      0.33081699664358     -0.92613288529126
H          -1.05358753581224      0.38209040934547      0.86689883085638
H          -0.89078558373194     -1.18834497089553     -0.01594155651396
O           1.67913078304498      0.31070162375100     -0.28088078119606
H           1.88939689019685      0.17750722791974      0.65281968103578
```

### TSD

```text
7

C          -0.77763363568364     -0.10797089595840     -0.04542126753852
H           0.39770017833434      0.12502500664978     -0.23608569551649
H          -1.27059074160330      0.33349472967111     -0.90517953709156
H          -1.05192912823705      0.37375855786028      0.88624232462495
H          -0.87633089384211     -1.18706486112168     -0.01146605413402
O           1.66719744479660      0.35805425386556     -0.29402167824388
H           1.91158677623516      0.10470320903337      0.60593190789951
```
