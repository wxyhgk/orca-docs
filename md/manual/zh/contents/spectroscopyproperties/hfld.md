```{index} HFLD
```

(sec:spectroscopyproperties.hfld)=
# Hartree-Fock 加伦敦色散（HFLD）方法（The Hartree-Fock plus London Dispersion Method）

高效且准确的 HFLD 方法 {cite}`HFLD`
可用于一对用户定义片段之间非共价相互作用的定量与分析。
从 ORCA 5.0 开始，还提供了 HFLD 方法的开壳层变体。{cite}`HFLDos`

其核心思想是求解 DLPNO 耦合簇方程，但忽略单体内的相关。
随后用 LED 方案从相关能的分子间部分提取伦敦色散（London dispersion，LD）能。
最后，用所得 LD 能校正 HF 水平计算的相互作用能。
因此，HFLD 可被视为一种色散校正的 HF 方法，
其中片段间的色散相互作用在 DLPNO-CC 水平上加入。
正因如此，它对非共价相互作用的定量特别准确，
例如氢键体系、预反应中间体（如受阻路易斯对，Frustrated Lewis Pairs）、
色散和静电束缚体系中的相互作用。
原则上，对过渡金属配合物误差会更大，
这与任何色散校正的 Hartree-Fock 方案都一样。

该方法的高效率使得研究含数百个原子体系中的非共价相互作用成为可能。

该方法一些最重要的方面总结如下：

-   **精度与推荐设置** \
    对于非共价相互作用，
    若采用默认 PNO 设置，HFLD 通常能达到与 DLPNO-CCSD(T) 方法相当的精度。
    对于 HFLD 方案，这些设置定义为 TCutPNO = 3.3e-7 和 TCutPairs 1e-5。
    若与 def2-TZVP(-f) 基组联用，这些设置通常记作 `HFLD*`，
    推荐用于大体系的标准应用 {cite}`HFLDos`。例如，文献 {cite}`altun2021unveiling`
    中就使用 `HFLD*` 设置来阐明决定 DNA 双螺旋稳定性的复杂相互作用图样。
    若需要很高的精度，建议使用 TightPNO 设置，
    联用 TCutPNO 1e-8 以及两点基组外推（aug-cc-pVTZ/aug-cc-pVQZ）
    以逼近 CBS 极限。这些设置通常记作 **gold** HFLD 设置 {cite}`HFLDos`。

-   **开壳层 HFLD 方案中的参考行列式** \
    在开壳层情形下，HFLD 依赖限制性参考行列式来计算 LD 能。
    若以 QRO 行列式作为参考，参考相互作用能原则上可在 UHF 或 QRO 水平计算。
    这导致两种不同的方案，即 QRO/HFLD 和 UHF/HFLD。
    另外，也可在 HFLD 计算中使用限制性开壳层 HF（ROHF）行列式作为参考，
    这对应 ROHF/HFLD 方法。
    输出中报告为 `FINAL SINGLE POINT ENERGY` 的能量值
    默认对应 UHF/HFLD 方案，其精度通常略高。
    详见文献 {cite}`HFLDos`。

-   **效率** \
    色散校正的计算通常与一次 HF 计算耗时相同。
    对小体系和大体系都是如此。

-   **分子间相互作用分析** \
    HFLD 方法可与定域能分解（Local Energy Decomposition，LED）结合，
    以极其细致地研究分子间相互作用。
    由 HFLD 得到的 LED 色散能通常与完整 DLPNO-CCSD(T) 计算所得非常接近。
    因此，HFLD 可作为 DLPNO-CCSD(T) 的高性价比替代，
    用于研究（除其他外）伦敦色散在分子化学中的重要性。

-   **其他注意事项** \
     (i) 可在简单输入行中指定 `NormalPNO` 或 `TightPNO` 设置。
    此时相应的 DLPNO 阈值将与 DLPNO-CCSD(T) 方法中所用的完全一致。
    (ii) HFLD 方法中的色散能略微依赖于占据轨道和 PNO 所用定域化方案的选择。
    就一般用途而言，推荐使用默认设置。
    但务必注意，为获得一致的结果，
    占据轨道和虚轨道的定域化迭代必须完全收敛。
    为此，可能需要增大 `LocMaxIter` 或 `LocMaxIterLed`（见下文）。
    不过，通常只有在使用非常大的基组（如 aug-cc-pV5Z）时才有此必要。
    (iii) 重要的是，该方法受益于收敛严格的 SCF 解。
    对于闭壳层体系，这里一个有用的诊断量是输出 LED 部分中打印的
    "Singles energy" 项。对于闭壳层物种，该项必须小于 1e-6。
    若不满足，应更改 SCF 迭代所用的设置。
    另请注意，LED 方案的所有功能（如自动分片）对 HFLD 方法同样可用。

请注意，由于 HFLD 同时依赖 DLPNO-CCSD(T) 和 LED 方法，
原则上这两种方案的选项都可以与 HFLD 联用。
下面给出一些示例：

```orca
! HFLD aug-cc-pVDZ aug-cc-pVDZ/C aug-cc-pVTZ/JK RIJK TightSCF

%mdci
  LED 1               # localization method for the PNOs. Choices:
                      # 1 = PipekMezey 
                      # 2 = FosterBoys (default, recommeded for the HFLD method)
  PrintLevel 3        # Selects large output for LED and prints the
                      # detailed contribution
                      # of each DLPNO-CCSD strong pair
  LocMaxIterLed 600   # Maximum number of localization iterations for PNOs
  LocMaxIter    300   # Maximum number of localization iterations for 
                      # occupied orbitals
  LocTolLed     1e-6  # Absolute threshold for the localization procedure for PNOs
  DoLEDHF true        # Decomposes the reference energy in the LED part. 
                      # By default, it is set to false in HFLD for efficiency reasons.
  TCutPNO    3.33e-7  # cutoff for PNO occupation numbers.  
  TCutPairs  1e-5     # cutoff for estimated pair correlation energies
                      # to be included in the CC treatment
end
```

(sec:spectroscopyproperties.hfld.basicusage)=
## 基本用法（Basic Usage）

在简单输入行中使用 `!HFLD` 关键词即可调用 Hartree-Fock 加伦敦色散方法：

```orca
! HFLD aug-cc-pvdz aug-cc-pvdz/C
```

(sec:spectroscopyproperties.hfld.example)=
## 示例（Example）

下面给出一个输入示例。

```{literalinclude} ../../orca_working_input/C05S13_241.inp
:language: orca
```

在相应的输出中，DLPNO-CC 迭代和 LED 输出之后会打印如下信息：

```
----------------------------   ----------------
Inter-fragment dispersion       -0.001871763
----------------------------   ----------------


-------------------------   --------------------
FINAL SINGLE POINT ENERGY      -114.932878050741 
-------------------------   --------------------
```

因此该加合物的总 HFLD 能量为 -114.932878050741 a.u.。
要计算相互作用能，需从此值中减去单体在配合物中所取几何构型下的
Hartree-Fock 能量，即 CH$_2$ 和 H$_2$O 分别为
-38.884413525377 和 -76.040412827089 a.u.。
因此总相互作用能为 -0.00805 a.u. 或 -5.1 kcal/mol
（相应的 DLPNO-CCSD(T)/TightPNO/CBS 值为 -5.3 kcal/mol {cite}`altun2018open`）。
请注意，要获得结合能，还需在此值上加上几何准备能
（geometric preparation）。
后者可用标准计算方法（如 DFT 或 DLPNO-CCSD(T)）计算。

(sec:spectroscopyproperties.hfld.led)= 
## HFLD/LED 联合分析（Combined HFLD/LED Analysis）

要进行 HFLD/LED 联合分析，必须在 `%mdci` 块中启用 HF/LED 分解：

```orca
! %mdci DoLEDHF True end
```

### 示例（Example）

下面是 {numref}`fig:LED_HeatMap` 中所示 DNA 超体系（supersystem）的
HFLD/LED 输入示例，采用默认的 `NormalPNO*` 设置：

```orca
! HFLD def2-TZVP(-f) RIJCOSX DefGrid3 def2/J def2-TZVP/C 
! VeryTightSCF CPCM(water)

%mdci DoLedHF True   # HFLD default: False
      HFFragInter {1 2} {1 3} {2 3} {4 5} {4 6} {5 6}
      end
```

坐标和片段标签的指定方式与
{numref}`sec:spectroscopyproperties.led.multifrag_led` 一节相同。

HFLD 方法通过忽略子体系内的电子相关，从根本上简化了计算。
默认情况下，HFLD 实现将每个片段视为一个独立的子体系。
然而，一个子体系未必只由单个片段组成，
例如 DNA 双螺旋中的链间相互作用就是如此。
在这种情况下，必须明确告知程序哪些片段构成每个子体系。
这可以通过在 `%mdci` 块中用 `HFFragInter` 指令
明确指定要从相关中排除的片段对来完成。
在上面的例子中，该指令将链 K 片段（1–3）之间以及链 L 片段（4–6）之间
的相关能设为零。
请注意，片体内相关（如 `HFFragInter {1 1} {2 2} ...`）无需明确指定，
因为使用 `HFLD` 关键词时它们会被自动排除。

要计算相互作用能，还必须为每个子体系准备输入文件。
若某子体系只由一个片段组成，则对该子体系进行参考水平计算（RHF 或 QRO）即可。
此时，必须从相应子体系的输入中删除 `LED` 关键词、
PNO 设置关键词（`LoosePNO`、`NormalPNO` 或 `TightPNO`）以及整个 `%mdci` 块。

对于多片段子体系，则需要参考水平计算结合 LED 分析（RHF/LED 或 QRO/LED）。
然而，在当前 ORCA 版本中，无法单独在参考水平调用 LED 分析。
作为一种变通方法，可执行低成本的 DLPNO-CCSD 或 HFLD 计算，
以高效获得所需的 LED 数据：

```orca
! HFLD def2-TZVP(-f) RIJCOSX DefGrid3 def2/J def2-TZVP/C 
! VeryTightSCF CPCM(water) LoosePNO

%mdci DoLedHF True   # HFLD default: False
      maxiter 0
      end
```

在本例中，`%mdci` 块中的 `maxiter 0` 指令跳过了不必要的耦合簇迭代。
配置此类低成本计算时，请确保相关空间没有被截断得过于激进，
因为至少必须保留一对电子，LED 分析才能进行。
这里使用了 LoosePNO 设置，但若它们排除了所有电子对，
则可能需要略微收紧设置。
对于大体系，HFFragInter 指令可通过选择性排除片体间相关进一步降低成本。
但要避免排除所有电子对，否则将完全禁用 LED 分析。

请注意，若已对单片段子体系执行过 DLPNO-CCSD(T) 计算，
或对多片段子体系执行过 DLPNO-CCSD(T)/LED 计算，
则相应的 ORCA 输出文件可直接用于 HFLD/LED 联合分析，
无需再进行额外的子体系计算。

(sec:spectroscopyproperties.hfld.keywords)=
## 关键词（Keywords）
```{index} HFLD Keywords
```

:::{note}
由于 HFLD 同时依赖 DLPNO-CCSD(T) 和 LED 方法，
原则上这两种方案的选项都可以与 HFLD 联用。
:::

(tab:spectroscopyproperties.hfld.keywords.simple)=
:::{table} Hartree-Fock 加伦敦色散方法的简单输入关键词。
| 关键词                          | 说明                                            |
|:--------------------------------|:--------------------------------------------------|
| `HFLD`                          | 启用 Hartree-Fock 加伦敦色散方法                  |
:::

:::{raw} latex
\begingroup
\footnotesize
:::

:::{tabularcolumns} \Y{0.25}\Y{0.2}\Y{0.55}
:::
(tab:spectroscopyproperties.hfld.keywords.block)=
:::{flat-table} Hartree–Fock 加伦敦色散方法的 `%mdci` 块输入关键词。
:header-rows: 1
:class: longtable
:class: footnotesize
* - 关键词
  - 选项
  - 说明
* - `LED`
  - `1`
  - 使用 Pipek–Mezey 作为 PNO 的定域化方法
* - 
  - `2`
  - 使用 Foster–Boys 作为 PNO 的定域化方法（自 ORCA 4.2 起为默认）
* - `PrintLevel`
  - `3`
  - 选择 LED 的详细输出，打印每个 DLPNO-CCSD 强对的详细贡献
* - `LocMaxIterLed`
  - `<integer>`
  - PNO 定域化迭代的最大次数（默认设为 600）
* - `LocMaxIter`
  - `<integer>`
  - 占据轨道定域化迭代的最大次数（默认设为 128）
* - `LocTocLed`
  - `<real>`
  - PNO 定域化过程的绝对阈值（默认设为 1e-6）
* - `DoLEDHF`
  - `true/false`
  - 在 LED 部分分解参考能量（出于效率考虑，HFLD 中默认设为 false）
* - `TCutPNO`
  - `<real>`
  - PNO 占据数的截断值（默认设为 3.33e-7）
* - `TCutPairs`
  - `<real>`
  - 纳入 CC 处理的对相关能估计值的截断值（默认设为 1e-5）
:::
:::{raw} latex
\endgroup
:::
