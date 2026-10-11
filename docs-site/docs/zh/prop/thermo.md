---
title: 热力学
source: https://www.faccts.de/docs/orca/6.1/tutorials/prop/thermo.html
---

# 热力学

如果你已经成功完成了[振动频率](../prop/freq.md#vibfreq)计算，现在就可以获得焓（enthalpy，$H$）、熵（entropy，$S$）和吉布斯自由能（Gibbs free energy，$G$）等热力学（thermodynamics）函数了！

让我们用一个例子来说明：用它预测一些[丁烯异构体](https://cccbdb.nist.gov/getisox.asp?isof=C4H8&amp;charge=0)的相对焓序。

[![butene](../images/butene.png)](../images/butene.png)

*图：*gem*-、*trans*- 和 *cis*-丁烯的实验相对自由能（T = 298.15 K，p = 1 atm）。*

```mol
title: gem-丁烯
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
title: trans-丁烯
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
title: cis-丁烯
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

使用如下关键词，并以偕位（geminal）异构体为例：

```text
!B3LYP D4 DEF2-TZVP OPT FREQ
* XYZFILE 0 1 gem-butene.xyz
```

## 热力学函数

假设输入中带有 `!FREQ`，那么在频率和简正模式之后，紧接着就能看到热化学（thermochemistry）部分的开始：

```text
Temperature         ...   298.15 K
Pressure            ...     1.00 atm  
Total Mass          ...    56.11 AMU
Quasi RRHO          ...     True
Cut-Off Frequency   ...     1.00 cm^-1 
```

> **注意**
> 这些性质是针对给定温度和压力、假设为气相分子并采用统计力学（statistical mechanics）计算得到的。关于溶液中的热力学，请查阅[隐式溶剂化模型](../prop/cpcm.md#solvation)一节。

### 内能

第一个函数是内能（inner energy，$U$），它按输出中所示的方式计算：

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

`Electronic energy` 就是从 `FINAL SINGLE POINT ENERGY` 得到的能量，接着计算 `Zero-Point Energy (ZPE)`，以及与转动、振动和平动自由度（degrees of freedom）有关的 `Thermal correction`。

`Total correction` 是需要加到 `FINAL SINGLE POINT` 电子能量上的能量值，用以将 $E_{el}$ 转换为 $U$。

### 焓

接下来是焓的计算。它就是 $U + k_BT$：

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

同样，`Thermal Enthalpy correction` 就是需要加到 $U$ 上以计算 $H$ 的项。

### 熵

随后是熵项：

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

其中列出了各个分量，以及已经乘上温度的*最终熵项*，也就是稍后用于自由能的 $TS$ 项。

### 吉布斯自由能

最后打印出自由能项：

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

最后一项 *G-E(el)* 就是在**给定温度和压力**下，为把 $E_{el}$ 转换为 $G^o$ 需要加到电子能量上的项。

> **注意**
> 这个 *G-E(el)* 只依赖于几何结构和频率，因此可以在较低级别（如 DFT）的方法上计算，再与较高级别方法（如 DLPNO-CCSD(T)）的 $E_{el}$ 组合，从而对 $G^o$ 作出非常好的预测！

## 与实验结果的比较

`Final Gibbs free energy` 的数值给出 $3.4$ $kJ mol^{-1}$ 和 $7.1$ $kJ mol^{-1}$ 的相对自由能。

为改善与实验数据的吻合，电子能量分量 $E_{el}$ 也可以在 DLPNO-CCSD(T) 级别上计算。相应数值由 `FINAL SINGLE POINT ENERGY` 给出。

```text
!DLPNO-CCSD(T) aug-cc-pVTZ AUTOAUX RIJCOSX
* XYZFILE 0 1 butene_optimized_dft.xyz
```

这些电子能量再用 DFT 计算所得的 `G-E(el)` 值进行校正。

| 化合物 | $\Delta E_{DFT} + \Delta (G-E_{el, DFT})$ | $\Delta E_{CCSD(T)} + \Delta (G-E_{el, DFT})$ | $\Delta G_{Exp.}$ |
| --- | --- | --- | --- |
| *gem*-butene | 0.0 | 0.0 | 0.0 |
| *trans*-butene | 3.4 | 4.8 | 6.2 |
| *cis*-butene | 7.1 | 8.6 | 7.8 |

## 不同温度下的热力学

要在不同温度（或多个温度）下计算这些热力学性质，可以使用：

```text
%FREQ TEMP 77, 298, 330, 450 END
```

热力学函数将按如下标题分开：

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

依此类推。

### 计算完成后改变温度

如果想在计算**已经结束之后**再计算热力学函数，可以设置一个简单的输入，例如：

```text
!PRINTTHERMOCHEM
%GEOM
         INHESSNAME "basename.hess"
END
%FREQ TEMP 290, 295, 300
END
* XYZFILE 0 1 geometry.xyz
```

这样可以省去重新计算所花费的大量时间。

> **注意**
> 也可以用它来引入同位素效应：修改 `basename.hess` 文件中的质量并重新计算热力学量（参见[动力学同位素效应（KIE）](../react/KIE.md#kie)）。
