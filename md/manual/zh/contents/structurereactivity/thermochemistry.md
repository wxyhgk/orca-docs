(sec:structurereactivity.thermochemistry)=
# 热化学（Thermochemistry）
```{index} Thermochemistry, RRHO
```

作为频率计算的结果，你自动得到的第二样东西是基于理想气体统计力学的热化学分析。这可用于研究生成热、解离能及类似的热化学性质。为校正谐振子近似在低频下的失效，自由能中的熵贡献默认采用 Grimme 的 Quasi-RRHO 方法计算。{cite}`grimme2012chemeurj` 要关闭 Quasi-RRHO 方法而使用 RRHO 方法，请用：

```orca
%freq  QuasiRRHO false
       CutOffFreq 35 # in cm-1
       end
```

其中 CutOffFreq 参数控制低频模式的截断（被排除在热化学性质的计算之外）。注意，当 Quasi-RRHO 开启时，默认的 CutOffFreq 为 1（cm$^{-1}$），因为 Quasi-RRHO 在低频下的行为比 RRHO 合理得多。特别是，当振动频率趋近于零时，Quasi-RRHO 计算的熵贡献趋近于一个常数值，而 RRHO 的贡献则发散。

Quasi-RRHO 方法在谐振子和刚性转子的熵公式之间平滑插值，使得高频振动表现为谐振动，而低频振动表现为具有相同频率的转动。熵贡献为转动和振动各占一半的频率称为 Quasi-RRHO 方法的"参考频率（reference frequency）"$\omega_0$，可通过 `%freq` 中的 `QRRHORefFreq` 关键词访问（见 {ref}`sec:structurereactivity.frequencies`）。默认值（100 cm$^{-1}$）与原始 Quasi-RRHO 论文 {cite}`grimme2012chemeurj` 一致，但其他论文可能选择不同的值，例如 50 cm$^{-1}$。与此同时，ORCA 的 Quasi-RRHO 实现在"平均分子转动惯量（average molecular moment of inertia）"$B_{\rm{av}}$ 的选择上偏离了原始论文：原始论文中它被取为固定值 $10^{-44} \rm{kg}\cdot\rm{m}^2$，而在 ORCA 中它取为实际分子的各向同性平均转动惯量。这在理论上比对不同大小的分子使用相同转动惯量更有依据，尽管所得吉布斯自由能的差别相当小，通常在 0.1 kcal/mol 以内。

注意，熵的转动贡献是使用 Herzberg {cite}`Herzberg1945` 给出的表达式计算的，包括从点群阶数得到的对称数（symmetry number）。[^1] 虽然这是一个很好的近似，但你可能希望修改对称数或使用不同的表达式 {cite}`Gilson2010`。为此目的，分子的转动常数（单位为 cm$^{-1}$）也在热化学输出中给出。

例如，让我们计算 H$_{2}$O$_{2}$ 分子中氧-氧解离能的数值。首先运行以下作业：

```orcainput
# Calculate a value for the O-O bond strength in H2O2
! B3LYP DEF2-TZVP OPT FREQ BOHRS

* xyz 0 1
 O          -1.396288    -0.075107     0.052125
 O           1.396289    -0.016261    -0.089970
 H          -1.775703     1.309756    -1.111179
 H           1.775687     0.140443     1.711854
*
```

```orcainput
# Now the OH radical job
! B3LYP DEF2-TZVP OPT FREQ BOHRS

* xyz 0 2
 O          -1.396288    -0.075107     0.052125
 H          -1.775703     1.309756    -1.111179
*
```

第一个作业在频率计算后给出如下输出：

```orca
--------------------------
THERMOCHEMISTRY AT 298.15K
--------------------------

Temperature         ... 298.15 K
Pressure            ... 1.00 atm
Total Mass          ... 34.01 AMU

Throughout the following assumptions are being made:
  (1) The electronic state is orbitally nondegenerate
  (2) There are no thermally accessible electronically excited states
  (3) Hindered rotations indicated by low frequency modes are not
      treated as such but are treated as vibrations and this may
      cause some error
  (4) All equations used are the standard statistical mechanics
      equations for an ideal gas
  (5) All vibrations are strictly harmonic

freq.     370.67  E(vib)   ...       0.21 
freq.     947.27  E(vib)   ...       0.03 
freq.    1313.46  E(vib)   ...       0.01 
freq.    1440.24  E(vib)   ...       0.00 
freq.    3739.49  E(vib)   ...       0.00 
freq.    3739.86  E(vib)   ...       0.00 

------------
INNER ENERGY
------------

The inner energy is: U= E(el) + E(ZPE) + E(vib) + E(rot) + E(trans)
  E(el)   - is the total energy from the electronic structure calculation
            = E(kin-el) + E(nuc-el) + E(el-el) + E(nuc-nuc)
  E(ZPE)  - the zero temperature vibrational energy from the frequency calculation
  E(vib)  - the finite temperature correction to E(ZPE) due to population
            of excited vibrational states
  E(rot)  - is the rotational thermal energy
  E(trans)- is the translational thermal energy

Summary of contributions to the inner energy U:
Electronic energy                ...   -151.55083691 Eh
Zero point energy                ...      0.02631509 Eh      16.51 kcal/mol
Thermal vibrational correction   ...      0.00040105 Eh       0.25 kcal/mol
Thermal rotational correction    ...      0.00141627 Eh       0.89 kcal/mol
Thermal translational correction ...      0.00141627 Eh       0.89 kcal/mol
-----------------------------------------------------------------------
Total thermal energy                   -151.52128823 Eh


Summary of corrections to the electronic energy:
(perhaps to be used in another calculation)
Total thermal correction                  0.00323359 Eh       2.03 kcal/mol
Non-thermal (ZPE) correction              0.02631509 Eh      16.51 kcal/mol
-----------------------------------------------------------------------
Total correction                          0.02954868 Eh      18.54 kcal/mol


--------
ENTHALPY
--------

The enthalpy is H = U + kB*T
                kB is Boltzmann's constant
Total free energy                 ...   -151.52129054 Eh
Thermal Enthalpy correction       ...      0.00094421 Eh       0.59 kcal/mol
-----------------------------------------------------------------------
Total Enthalpy                    ...   -151.52034633 Eh


Note: Rotational entropy computed according to Herzberg
Infrared and Raman Spectra, Chapter V,1, Van Nostrand Reinhold, 1945
Point Group:  C2, Symmetry Number:   2
Rotational constants in cm-1:    10.087644     0.882994     0.851333

Vibrational entropy computed according to the QRRHO of S. Grimme
Chem.Eur.J. 2012 18 9955


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
Vibrational entropy               ...      0.00059250 Eh      0.37 kcal/mol
Rotational entropy                ...      0.00789993 Eh      4.96 kcal/mol
Translational entropy             ...      0.01734394 Eh     10.88 kcal/mol
-----------------------------------------------------------------------
Final entropy term                ...      0.02583637 Eh     16.21 kcal/mol

In case the symmetry of your molecule has not been determined correctly
or in case you have a reason to use a different symmetry number we print
out the resulting rotational entropy values for sn=1,12 :
 --------------------------------------------------------
|  sn= 1 | S(rot)=       0.00855439 Eh      5.37 kcal/mol|
|  sn= 2 | S(rot)=       0.00789993 Eh      4.96 kcal/mol|
|  sn= 3 | S(rot)=       0.00751710 Eh      4.72 kcal/mol|
|  sn= 4 | S(rot)=       0.00724548 Eh      4.55 kcal/mol|
|  sn= 5 | S(rot)=       0.00703479 Eh      4.41 kcal/mol|
|  sn= 6 | S(rot)=       0.00686265 Eh      4.31 kcal/mol|
|  sn= 7 | S(rot)=       0.00671710 Eh      4.22 kcal/mol|
|  sn= 8 | S(rot)=       0.00659102 Eh      4.14 kcal/mol|
|  sn= 9 | S(rot)=       0.00647981 Eh      4.07 kcal/mol|
|  sn=10 | S(rot)=       0.00638033 Eh      4.00 kcal/mol|
|  sn=11 | S(rot)=       0.00629034 Eh      3.95 kcal/mol|
|  sn=12 | S(rot)=       0.00620819 Eh      3.90 kcal/mol|
 --------------------------------------------------------


-------------------
GIBBS FREE ENERGY
-------------------

The Gibbs free energy is G = H - T*S

Total enthalpy                    ...   -151.52034633 Eh
Total entropy correction          ...     -0.02583637 Eh    -16.21 kcal/mol
-----------------------------------------------------------------------
Final Gibbs free energy         ...   -151.54618270 Eh

For completeness - the Gibbs free energy minus the electronic energy
G-E(el)                           ...      0.00465413 Eh      2.92 kcal/mol
```

OH 自由基作业的情况类似。

```orca
------------
INNER ENERGY
------------

The inner energy is: U= E(el) + E(ZPE) + E(vib) + E(rot) + E(trans)
 E(el)   - is the total energy from the electronic structure calculation
           = E(kin-el) + E(nuc-el) + E(el-el) + E(nuc-nuc)
 E(ZPE)  - the zero temperature vibrational energy from the frequency calculation
 E(vib)  - the finite temperature correction to E(ZPE) due to population
           of excited vibrational states
 E(rot)  - is the rotational thermal energy
 E(trans)- is the translational thermal energy

Summary of contributions to the inner energy U:
Electronic energy                ...    -75.73492538 Eh
Zero point energy                ...      0.00837287 Eh       5.25 kcal/mol
Thermal vibrational correction   ...      0.00000000 Eh       0.00 kcal/mol
Thermal rotational correction    ...      0.00094418 Eh       0.59 kcal/mol
Thermal translational correction ...      0.00141627 Eh       0.89 kcal/mol
-----------------------------------------------------------------------
Total thermal energy                    -75.72419205 Eh


Summary of corrections to the electronic energy:
(perhaps to be used in another calculation)
Total thermal correction                  0.00236045 Eh       1.48 kcal/mol
Non-thermal (ZPE) correction              0.00837287 Eh       5.25 kcal/mol
-----------------------------------------------------------------------
Total correction                          0.01073332 Eh       6.74 kcal/mol


--------
ENTHALPY
--------

The enthalpy is H = U + kB*T
                kB is Boltzmann's constant
Total free energy                 ...    -75.72419205 Eh
Thermal Enthalpy correction       ...      0.00094421 Eh       0.59 kcal/mol
-----------------------------------------------------------------------
Total Enthalpy                    ...    -75.72324785 Eh


Note: Rotational entropy computed according to Herzberg
Infrared and Raman Spectra, Chapter V,1, Van Nostrand Reinhold, 1945
Point Group:  C2v, Symmetry Number:   1
Rotational constants in cm-1:     0.000000    18.628159    18.628159

Vibrational entropy computed according to the QRRHO of S. Grimme
Chem.Eur.J. 2012 18 9955


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


Note: Rotational entropy computed according to Herzberg
Infrared and Raman Spectra, Chapter V,1, Van Nostrand Reinhold, 1945
Point Group:  C2v, Symmetry Number:   1
Rotational constants in cm-1:     0.000000    18.628159    18.628159

Vibrational entropy computed according to the QRRHO of S. Grimme
Chem.Eur.J. 2012 18 9955


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

Electronic entropy                ...      0.00065446 Eh      0.41 kcal/mol
Vibrational entropy               ...      0.00000000 Eh      0.00 kcal/mol
Rotational entropy                ...      0.00321884 Eh      2.02 kcal/mol
Translational entropy             ...      0.01636225 Eh     10.27 kcal/mol
-----------------------------------------------------------------------
Final entropy term                ...      0.02023555 Eh     12.70 kcal/mol


-------------------
GIBBS FREE ENERGY
-------------------

The Gibbs free energy is G = H - T*S

Total enthalpy                    ...    -75.72324785 Eh
Total entropy correction          ...     -0.02023555 Eh    -12.70 kcal/mol
-----------------------------------------------------------------------
Final Gibbs free energy         ...    -75.74348340 Eh

For completeness - the Gibbs free energy minus the electronic energy
G-E(el)                           ...     -0.00855802 Eh     -5.37 kcal/mol
```

让我们计算反应 $H_2O_2 \rightarrow 2 OH$ 的自由能变化：

各项能量为：

电子能：-151.46985 a.u. -(-151.55084) a.u. = 0.08099 a.u.（50.82 kcal/mol）

零点能：0.01675 a.u. - 0.02631 a.u. = -0.00956 a.u.（-6.00 kcal/mol）

热校正（平动/转动）：0.00472 a.u. - 0.00283 a.u. = 0.00189 a.u.（1.19 kcal/mol）

热焓校正：0.00189 a.u. - 0.00094 a.u. = 0.00095 a.u.（0.60 kcal/mol）

熵：-0.04047 a.u. -(-0.02584) a.u. = -0.01463 a.u.（-9.18 kcal/mol）

最终 $\Delta$G：37.43 kcal/mol

可见，零点能和熵项都对反应的总自由能变化有显著贡献。由于新的平动和转动自由度的出现，熵项有利于该反应。零点校正同样有利于该反应，因为 O–O 键的零点振动能被损失了。热校正和焓校正都很小。

:::{Tip}

-   你可以通过向程序提供温度/压强列表，在若干用户自定义的温度和压强下运行热化学计算：

```orca
%freq  Temp  290, 295, 300     # in Kelvin
        Pressure  1.0, 2.0, 3.0 # in atm
       end
```

-   一旦有了 Hessian，你可以通过提供关键词 PrintThermoChem 和 Hessian 文件的名称，在若干用户自定义的温度/压强下重新运行热化学分析：

```orca
! PrintThermoChem
%geom 
  inhessname "FreqJob.hess" # default: job-basename.hess
end
%freq  Temp  290, 295, 300     # in Kelvin
        Pressure  1.0, 2.0, 3.0 # in atm
       end
```
:::

[^1]: 线性分子配分函数的相应公式（假定温度足够高）为
    $Q_{int} = \frac{kT}{\sigma h c B}$，非线性分子为
    $Q_{int} = \frac{1}{\sigma} \sqrt{\frac{\pi}{ABC}(\frac{kT}{hc})^3}$。
    A、B 和 C 是相应的转动常数，$\sigma$ 是对称数。
    如果你想选择不同的对称数，ORCA 还提供了一个表格，给出其他对称数下该熵贡献的值。Herzberg 报告的各点群对称数如下：C$_1$,C$_i$,C$_s$:
    1; C$_2$,C$_{2v}$, C$_{2h}$: 2; C$_3$,C$_{3v}$,C$_{3h}$: 3;
    C$_4$,C$_{4v}$,C$_{4h}$: 4;C$_6$, C$_{6v}$, C$_{6h}$: 6; D$_2$,
    D$_{2d}$, D$_{2h}=$V$_h$: 4; D$_3$, D$_{3d}$, D$_{3h}$: 6; D$_4$,
    D$_{4d}$, D$_{4h}$: 8; D$_6$, D$_{6d}$, D$_{6h}$: 12; S$_6$: 3;
    C$_{\infty v}$: 1; D$_{\infty h}$: 2;T,T$_d$: 12; O$_h$: 24.

(sec:structurereactivity.thermochemistry.dboc)=
## 对角 Born-Oppenheimer 校正（Diagonal Born-Oppenheimer Correction）
```{index} Diagonal Born-Oppenheimer Correction
```

对于高精度热化学，所需的能量高阶校正之一是"对角 Born-Oppenheimer 校正"（diagonal Born-Oppenheimer correction，DBOC）。DBOC 校正的表达式由一阶微扰理论导出，为：

$$E_{DBOC} = \left\langle \Psi_{e}\left( \mathbf{r},\mathbf{R} \right)|{\widehat{T}}_{N}|\Psi_{e}\left( \mathbf{r},\mathbf{R} \right) \right\rangle$$

为计算 DBOC 校正，需要计算轨道（和密度）对核微扰的响应，这是解析 Hessian 计算中最昂贵的步骤。因此，该校正最好与常规热化学校正一起并行计算。ORCA 中的实现涵盖 SCF 水平（例如闭壳层和自旋非限制性 Hartree–Fock 与 DFT）。

```orca
! DBOC
# or NoDBOC to turn it off (which is the default)
```

**相关文献（Relevant Papers）：**

```{bibliography} ../../bibliography.bib
:list: enumerated
:filter: False

HandyYamaguchiJCP1986
```

(sec:structurereactivity.thermochemistry.socc)=
## 总能量的自旋-轨道耦合校正（Spin-Orbit Coupling Correction to the Total Energy）
```{index} Spin-Orbit Coupling Correction to the Total Energy
```

高精度热化学所需的另一项校正是对自旋-轨道耦合（Spin-Orbit-Coupling，SOC）在总能量上的能量效应的估计。虽然 ORCA 的大部分功能将 SOC 作为微扰处理并估计其对分子性质和光谱的影响，但总能量的贡献将需要相对论二分量理论。这在 ORCA 中尚未实现。因此，目前有一个 SOC 的一阶微扰校正，其过程如下：

SCF 能量为：

$$E_{SCF} = E_{Nuc} + \frac{1}{2}Tr\left( \mathbf{P},\mathbf{H + F} \right)$$

在二分量理论中，Fock 算符为：

$$\overline{\mathbf{F}}\mathbf{=}\begin{pmatrix}
\mathbf{F}^{\alpha} & \mathbf{0} \\
\mathbf{0} & \mathbf{F}^{\beta}
\end{pmatrix}\mathbf{+}\begin{pmatrix}
{\frac{1}{2}\mathbf{T}}^{z} & {\frac{1}{2}\mathbf{T}}^{x}\mathbf{+}{\frac{i}{2}\mathbf{T}}^{y} \\
{\frac{1}{2}\mathbf{T}}^{x}\mathbf{-}{\frac{i}{2}\mathbf{T}}^{y} & \mathbf{-}{\frac{1}{2}\mathbf{T}}^{z}
\end{pmatrix}$$

其中 $T^{x,y,z}$ 是 SOC 矩阵的 3 个分量。

然后求解本征值问题：

$$\overline{\mathbf{F}}\overline{\mathbf{C}}\mathbf{=}\overline{\boldsymbol{\varepsilon}}\overline{\mathbf{SC}}$$

其中二分量重叠矩阵为

$$\overline{\mathbf{S}}\mathbf{=}\begin{pmatrix}
\mathbf{S} & \mathbf{0} \\
\mathbf{0} & \mathbf{S}
\end{pmatrix}$$

现在由本征矢量计算 2C 密度矩阵

$$\overline{\mathbf{P}} = {\breve{\mathbf{C}}}^{\mathbf{*}}{\breve{\mathbf{C}}}^{T}$$

其中 $\breve{C}$ 是 $\overline{C}$ 的占据部分。于是得到近似的二分量能量：

$$E_{2C} = E_{Nuc} + \frac{1}{2}Tr\left( \overline{\mathbf{P}},\overline{\mathbf{H}}\mathbf{+}\overline{\mathbf{F}} \right)$$

SOC 校正于是简单地为：

$${\Delta}_{SOC} = E_{2C} - E_{SCF}$$

$$= \frac{1}{2}Tr\left( \overline{\mathbf{P}},\overline{\mathbf{H}}\mathbf{+}\overline{\mathbf{F}} \right) - \frac{1}{2}Tr\left( \mathbf{P},\mathbf{H + F} \right)$$

这显然忽略了由 SOC 引起的轨道弛豫。该近似必然相当粗糙，因此，在实际应用中，这一项确实需要一定的经验标度才能达到高精度。

**相关文献（Relevant Papers）：**

- Kayal, R.; Neese, F. **2025**, in preparation

(sec:structurereactivity.thermochemistry.HEAT)=
## 高精度热化学：HEAT 方案（High Accuracy Thermochemistry: the HEAT protocol）
```{index} High Accuracy Thermochemistry: the HEAT protocol
```

HEAT（High accuracy Extrapolated Ab initio Thermochemistry，高精度外推从头算热化学）方案由 Gauss、Stanton、Kallay 及其合作者建立，旨在实现系统性地与最精确实验能量相差 1 kJ/mol 以内的高精度总能量。

原始的 HEAT 公式包含八项：

$$E_{HEAT} = E_{HF}^{\infty} + {\Delta}E_{CCSD(T)}^{\infty} +{\Delta}E_{CCSDT} + {\Delta}E_{CCSDTQ} + {\Delta}E_{rel} + {\Delta}E_{ZPE} + {\Delta}E_{DBOC} + {\Delta}E_{SOC}$$

其中各项贡献为：

| **项**     | **原始定义**              | **ORCA 中的实现** |
|--------------|--------------------------------------|---------------------|
| 几何结构（Geometry）     | 用 CCSD(T)/cc-pVQZ 优化      | 相同                |
|              |                                      |                     |
|$E_{HF}^{\infty}$   | 完全基组极限       | 相同                |
|        | 外推的 Hartree–Fock 能量     |                     |
|        | 使用 aug-cc-pCVXZ (X=T,Q,5) 和公式                              |                     |
|        | $E_{HF}^{X} =$                       |                     |
|        | $E_{HF}^{\infty} + a\exp( - bX)$     |                     |
|        | $E_{HF}^{\infty},a,b$ 由三个能量确定 |                     |
|        |                                      |                     |        
|${\Delta}E_{CCSD(T)}^{\infty}$ | 完全基组极限  | 相同    |
|        | 外推的 CCSD(T) 能量，使用    |                     |
|        | aug-cc-pCVXZ (X=Q,5) 和公式         |                     |
|        | $E_{CCSD(T)}^{X} = $                 |                     |
|        | $E_{CCSD(T)}^{\infty} + aX^{- 3}$    |                     |
|        |                                      |                     |        
|${\Delta}E_{CCSDT}$       | 补偿 CCSD(T) 与 CCSDT 之间的差异  | 相同   |
|        |           |                     |
|        | 两点外推的冻结芯 CCSDT 与   |                     |
|        | CCSD(T) 之差，使用                        |                     |
|        | ${\Delta}E_{CCSDT} =$                |                     |
|        | $E_{CCS DT}^{TQ}(FC) - E_{CCSD(T)}^{TQ}(FC)$ |             |
|        |                                      |                     |        
|${\Delta}E_{CCSDTQ}$        | 补偿 CCSDT 与 CCSDTQ 之间的差异  | 相同 |
|        | 使用 cc-pVDZ 基组   |                     |
|        | ${\Delta}E_{CCSDTQ} =$               |                     |
|        | $E_{CCSDTQ}^{DZ}(FC) - E_{CCSDT}^{DZ}(FC)$ |                |
|        |                                      |                     |        
|${\Delta}E_{rel}$ | 标量相对论效应。 | 使用 aug-cc-pCVTZ 与|
|        | CCSD(T)/    | aug-cc-pCVTZ-DK 基组|
|        |aug-cc-pCVTZ-DK                       | 之间 CCSD(T) 能量之差|
|        | 密度与 Darwin 和          |来估计（采用 DKH 哈密顿量）。|
|        | Mass-Velocity 哈密顿量的期望值。          |                     |
|        |                                      |                     |
|        |                                      |                     |        
|${\Delta}E_{ZPE}$  | 零点能，采用在 | 在 CCSD(T)/cc-pVQZ 水平|
|        | CCSD(T)/cc-pVQZ 计算的 | 上采用谐近似|
|        | 非谐力场 | |
|        | ${\Delta}E_{ZPE} =$                  |对线性分子和对称陀螺分子使用标度因子|
|        | $\frac{1}{2}\sum_{i}^{}\omega_{i} +$ |，对其余分子使用 VPT2|
|        | $\frac{1}{4}\sum_{i \leq j}^{}x_{ij}$|模块。     |
|        | 其中 $\omega$ 和 $x$ 是谐  |                     |
|        | 和三次力常数。           |                     |
|        |                                      |                     |        
|${\Delta}E_{DBOC}$ | 对角 Born-Oppenheimer 校正 | 相同     |
|        | 在 SCF 水平计算。         |                     |
|        |                                      |                     |        
|${\Delta}E_{SOC}$ | 自旋-轨道耦合校正。全价层 | SCF 水平的一阶校正 |
|        | CASSCF，含单双激发 CI，并     | 如  |
|        | 与自旋-轨道有效芯势一起。           |{ref}`sec:structurereactivity.thermochemistry.socc`所述| 
|        |                                      |并进行经验标度。             |


因此，ORCA 的实现在很大程度上遵循原始方案，仅有因 ORCA 中无法获得所有能量分量而带来的一些有限改动。HEAT 方案由随 ORCA 一同提供的复合脚本 HEAT.cmp 计算。

**相关文献（Relevant Papers）：**

```{bibliography} ../../bibliography.bib
:list: enumerated
:filter: False

HEAT2004
```
-   Kayal, R.; Neese, F. **2025**, in preparation
