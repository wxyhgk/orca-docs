---
title: Thermodynamics
source: https://www.faccts.de/docs/orca/6.1/tutorials/prop/thermo.html
---

# Thermodynamics

If you have successfully done a [Vibrational frequencies](../prop/freq.md#vibfreq) calculation, now you have access to the thermodynamic functions such as enthalpy ($H$), entropy ($S$) and the Gibbs free energy ($G$)!

Let's follow an example and use this to predict the relative enthalpy ordering of some [butadiene isomers](https://cccbdb.nist.gov/getisox.asp?isof=C4H8&amp;charge=0).

[![butene](../images/butene.png)](../images/butene.png)

*Figure: Experimental relative free energies of *gem*-, *trans*-, and *cis*-butene (T = 298.15 K, p = 1 atm).*

```mol
title: gem-butene
theme: chem311
height: 360px
representation: ball-stick
--- xyz ---
12
structure
  C          -1.43333641710982      0.99750434133223     -0.11833314354528
  C          -0.18475482717332      0.62759099420377     -0.39181661341896
  C           0.13812904158972     -0.69904137413719     -1.01927936124571
  C           0.99530997982103      1.50886801088864     -0.09403775990942
  H           0.66526364427023     -0.56158725840381     -1.96888083944946
  H          -0.75974400764642     -1.28775885666908     -1.20721189335260
  H           0.80403526745525     -1.28218576008005     -0.37502483269079
  H          -2.27650846609433      0.35335064429450     -0.33755880129752
  H          -1.65451309098319      1.95681047014208      0.33410795230859
  H           1.55825458218721      1.72631922619331     -1.00745285372439
  H           0.69222808602999      2.45448923561900      0.35550308769672
  H           1.69049620765366      1.00988032661660      0.58883505862882
```

```mol
title: trans-butene
theme: chem311
height: 360px
representation: ball-stick
--- xyz ---
12
structure
  C           1.31005769169158      0.51452879141346      0.05804263697398
  C          -0.04819313785594     -0.09253207982925      0.22254234005303
  H           1.79539655204235      0.66757127845972      1.02702463158789
  H           1.25730597675553      1.47886263622368     -0.45054128881957
  H           1.96882389016151     -0.13975288898310     -0.52148647916325
  C          -1.18726477431566      0.45327229214244     -0.18976017691771
  C          -2.54552738268524     -0.15377457291609     -0.02524544056845
  H          -3.03091939506206     -0.30671024889310     -0.99422100546098
  H          -3.20425241496413      0.50046308281000      0.55438662370226
  H          -2.49276412960279     -1.11816170340100      0.48323797563451
  H          -0.08496173672054     -1.05895215397092      0.72255102983275
  H          -1.15050113944460      1.41969556694416     -0.68977084685447
```

```mol
title: cis-butene
theme: chem311
height: 360px
representation: ball-stick
--- xyz ---
12
structure
  C           1.47970360709777     -0.47841743730424      0.16222562758688
  C           0.02367038098010     -0.80795303233869      0.28562414393012
  H           1.66007607442031      0.57369355392531     -0.05439609169518
  H           1.94416186497463     -1.06912909934475     -0.63340002033858
  H           2.01226039794254     -0.72697631354996      1.08545344375310
  C          -1.01190540852076      0.02068494444637      0.16549233572241
  H          -0.19509791907163     -1.85098304967194      0.49893762893694
  C          -0.98084493396470      1.49003154320377     -0.12391775381971
  H          -2.00537265760596     -0.40248869126449      0.28901974823120
  H          -1.46501764033373      2.05312506426319      0.67997591564265
  H           0.02985297930524      1.87869926998700     -0.24179411861463
  H          -1.53582674522382      1.71592324764843     -1.03973085933522
```

using the following keywords and the geminal isomer as an example:

```text
!B3LYP D4 DEF2-TZVP OPT FREQ
* XYZFILE 0 1 gem-butene.xyz
```

## Thermodynamic functions

Assuming you had `!FREQ` on the input, immediately after the frequencies and normal modes, one will see that the thermochemistry section starts:

```text
Temperature         ...   298.15 K
Pressure            ...     1.00 atm  
Total Mass          ...    56.11 AMU
Quasi RRHO          ...     True
Cut-Off Frequency   ...     1.00 cm^-1 
```

> **Note**
> These properties will be computed for a given temperature and pressure, assuming a gas-phase molecule and using statistical mechanics. For thermodynamics in solution, check the [Implicit Solvation Models](../prop/cpcm.md#solvation) section.

### Inner energy

The first function is the inner energy ($U$), that is computed following the output:

```text
------------
INNER ENERGY
------------

The inner energy is: U= E(el) + E(ZPE) + E(vib) + E(rot) + E(trans)
    E(el)   - is the total energy from the electronic structure calculation
              = E(kin-el) + E(nuc-el) + E(el-el) + E(nuc-nuc)
    E(ZPE)  - the the zero temperature vibrational energy from the frequency calculation
    E(vib)  - the the finite temperature correction to E(ZPE) due to population
              of excited vibrational states
    E(rot)  - is the rotational thermal energy
    E(trans)- is the translational thermal energy

Summary of contributions to the inner energy U:
Electronic energy                ...   -157.18614555 Eh
Zero point energy                ...      0.10746477 Eh      67.44 kcal/mol
Thermal vibrational correction   ...      0.00246995 Eh       1.55 kcal/mol
Thermal rotational correction    ...      0.00141627 Eh       0.89 kcal/mol
Thermal translational correction ...      0.00141627 Eh       0.89 kcal/mol
-----------------------------------------------------------------------
Total thermal energy                   -157.07337829 Eh
```

The `Electronic energy` is what you get from the `FINAL SINGLE POINT ENERGY`, then the `Zero-Point Energy (ZPE)` is calculated, together with the `Thermal correction`, which has to do with the rotational, vibrational and translational degrees of freedom.

The `Total correction` is amount the of energy you have to add to your `FINAL SINGLE POINT` electronic energy to convert $E_{el}$ into $U$.

### Enthalpy

Then the calculation of the enthalpy. That is simply $U + k_BT$:

```text
--------
ENTHALPY
--------

The enthalpy is H = U + kB*T
                kB is Boltzmann's constant
Total thermal energy              ...   -157.07337829 Eh
Thermal Enthalpy correction       ...      0.00094421 Eh       0.59 kcal/mol
-----------------------------------------------------------------------
Total Enthalpy                    ...   -157.07243408 Eh
```

Again, the `Thermal Enthalpy correction` is what one has to add to $U$ to compute $H$.

### Entropy

The entropy term follows:

```text
-------
ENTROPY
-------

The entropy contributions are T*S = T*(S(el)+S(vib)+S(rot)+S(trans))
     S(el)   - electronic entropy
     S(vib)  - vibrational entropy
     S(rot)  - rotational entropy
     S(trans)- translational entropy
The entropies will be listed as multiplied by the temperature to get
units of energy

Electronic entropy                ...      0.00000000 Eh      0.00 kcal/mol
Vibrational entropy               ...      0.00393432 Eh      2.47 kcal/mol
Rotational entropy                ...      0.01154964 Eh      7.25 kcal/mol
Translational entropy             ...      0.01805279 Eh     11.33 kcal/mol
-----------------------------------------------------------------------
Final entropy term                ...      0.03353675 Eh     21.04 kcal/mol
```

with its different components and a *Final entropy term* that is already multiplied by the temperature, the $TS$ term that is latter used for the free energy.

### Gibbs free energy

Finally, the free energy term is printed:

```text
-------------------
GIBBS FREE ENERGY
-------------------

The Gibbs free energy is G = H - T*S

Total enthalpy                    ...   -157.07243408 Eh
Total entropy correction          ...     -0.03353675 Eh    -21.04 kcal/mol
-----------------------------------------------------------------------
Final Gibbs free energy         ...   -157.10597083 Eh

For completeness - the Gibbs free energy minus the electronic energy
G-E(el)                           ...      0.08017472 Eh     50.31 kcal/mol
```

The last term, *G-E(el)* is the term that you would have to add to your electronic energy to transform $E_{el}$ into $G^o$ at **a given temperature and pressure**.

> **Note**
> This *G-E(el)* only depends on the geometry and frequencies, and thus can be computed in a lower level method, such as DFT, and later combined with the $E_{el}$ of a higher level method, such as DLPNO-CCSD(T) to achieve a very good prediction of the $G^o$!

## Comparison to experiment

The `Final Gibbs free energy` values yield relative free energies of $3.4$ $kJ mol^{-1}$ and $7.1$ $kJ mol^{-1}$.

To improve the agreement with the experimental data, the electronic energy component $E_{el}$ can also
be computed at the DLPNO-CCSD(T) level. The respective values are given by the `FINAL SINGLE POINT ENERGY`.

```text
!DLPNO-CCSD(T) aug-cc-pVTZ AUTOAUX RIJCOSX
* XYZFILE 0 1 butene_optimized_dft.xyz
```

These electronic energies are now corrected by the `G-E(el)` values from the DFT calculations.

| Compound | $\Delta E_{DFT} + \Delta (G-E_{el, DFT})$ | $\Delta E_{CCSD(T)} + \Delta (G-E_{el, DFT})$ | $\Delta G_{Exp.}$ |
| --- | --- | --- | --- |
| *gem*-butene | 0.0 | 0.0 | 0.0 |
| *trans*-butene | 3.4 | 4.8 | 6.2 |
| *cis*-butene | 7.1 | 8.6 | 7.8 |

## Thermodynamics at different temperatures

To compute these thermodynamic properties at different temperatures, or at several, one can use:

```text
%FREQ TEMP 77, 298, 330, 450 END
```

and the thermodynamic functions will be separated by the headers:

```text
--------------------------
THERMOCHEMISTRY AT 77K
--------------------------
[...]
--------------------------
THERMOCHEMISTRY AT 298K
--------------------------
[...]
```

and so on.

### Changing the temperature after the calculation

If you want to compute thermodynamic functions **after** you calculation has already finished, that can be done setting a simple input such as:

```text
!PRINTTHERMOCHEM
%GEOM
         INHESSNAME "basename.hess"
END
%FREQ TEMP 290, 295, 300
END
* XYZFILE 0 1 geometry.xyz
```

as one can save a lot of time from recalculations.

> **Note**
> One could use this to also include isotopic effects, by changing the masses in the `basename.hess` file and recomputing the thermodynamics (see [Kinectic Isotope Effects (KIE)](../react/KIE.md#kie)).
