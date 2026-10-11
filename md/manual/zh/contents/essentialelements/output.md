(sec:essentialelements.output)=
# 输出控制（Control of Output）

ORCA 提供了多种选项来控制输出打印的详细程度。
这一点尤为重要，因为某些方法和流程会产生
非常大量的输出和数据。输出的总体控制由
`%output` 块中的 `PrintLevel` 和 `Print[<option>]` 关键词提供：
`PrintLevel` 可用于为打印数组选择某些默认设置。在 `PrintLevel` 之后指定 `Print` 可
用于修改这些默认值。

```orca
%output
  PrintLevel     Normal
  Print[ Flag ]  0  # turn print off
                 1  # turn print on
                 n  # some flags are more sophisticated
end
```

(sec:essentialelements.printoptions)=
## 打印选项（Print Options）

`PrintLevel` 和 `Print` 的详细选项列表见表 {numref}`tab:essentialelements.output.printoptions.options`。
每个打印级别所切换的选项列表见 {numref}`tab:essentialelements.output.printoptions.printleveldefaults`。

(tab:essentialelements.output.printoptions.options)=
:::{table} `%output` 块中用于打印控制的输入关键词与选项。
| 关键词                          | 选项                      | 说明                                                   |
|:--------------------------------|:--------------------------|:-------------------------------------------------------|
| `PrintLevel`                    | `nothing`                 | 关闭输出打印                                           |
|                                 | `mini`                    | 将打印级别设为 mini                                    |
|                                 | `small`                   | 将打印级别设为 small                                   |
|                                 | `normal`                  | 将打印级别设为 normal（默认）                          |
|                                 | `maxi`                    | 将打印级别设为 maxi                                    |
|                                 | `large`                   | 将打印级别设为 large                                   |
|                                 | `huge`                    | 将打印级别设为 huge                                    |
|                                 | `debug`                   | 将打印级别设为 debug                                   |
| `Print[ <option> ]`             | `P_InputFile`             | 回显输入文件                                           |
|                                 | `P_Cartesian`             | 打印笛卡尔坐标                                         |
|                                 | `P_Internal`              | 打印内坐标                                             |
|                                 | `P_Basis`                 | $=1:$ 打印基组信息                                     |
|                                 |                           | $=2:$ 同时以输入格式打印原始高斯函数                   |
|                                 | `P_OneElec`               | 打印单电子矩阵                                         |
|                                 | `P_Overlap`               | 打印重叠矩阵                                           |
|                                 | `P_KinEn`                 | 打印动能矩阵                                           |
|                                 | `P_S12`                   | 打印 S$^{-1/2}$ 矩阵                                   |
|                                 | `P_GuessOrb`              | 打印初始猜测轨道                                       |
|                                 | `P_OrbEn`                 | $=1:$ 打印至 LUMO+9 的轨道能量                         |
|                                 |                           | $=2:$ 打印所有轨道能量                                 |
|                                 | `P_MOs`                   | 在收敛时打印 MO 系数                                   |
|                                 | `P_Density`               | 打印收敛后的电子密度                                   |
|                                 | `P_SpinDensity`           | 打印收敛后的自旋密度                                   |
|                                 | `P_EHTDetails`            | 打印初始猜测的扩展 Hückel 细节                         |
|                                 | `P_SCFInfo`               | 打印 SCF 输入标志                                      |
|                                 | `P_SCFMemInfo`            | 打印预估的 SCF 内存需求                                |
|                                 | `P_SCFIterInfo`           | $=1:$ 打印简短的迭代信息                               |
|                                 |                           | $=2:$ 打印较详细的迭代信息                             |
|                                 |                           | $=3:$ 在直接 SCF 中同时打印积分进度                    |
|                                 | `P_Fockian`               | 打印 Fock 矩阵（Fockian）                              |
|                                 | `P_DIISMat`               | 打印 DIIS 矩阵                                         |
|                                 | `P_DIISError`             | 打印 DIIS 误差                                         |
|                                 | `P_Iter_P`                | 打印密度                                               |
|                                 | `P_Iter_C`                | 打印 MO 系数                                           |
|                                 | `P_Iter_F`                | 打印 Fock 矩阵                                         |
|                                 | `P_Mayer`                 | 打印 Mayer 布居分析（默认 = 开）                       |
|                                 | `P_NatPop`                | 打印自然布居分析（默认 = 关）                          |
|                                 | `P_NPA`                   | 打印自然布居分析（默认 = 关）                          |
|                                 | `P_Hirshfeld`             | 打印 Hirshfeld 布居分析（默认 = 关）                   |
|                                 | `P_MBIS`                  | 打印 MBIS 布居分析（默认 = 关）                        |
|                                 | `P_Mulliken`              | 打印 Mulliken 布居分析（默认 = 开）                    |
|                                 | `P_AtCharges_M`           | 打印 Mulliken 原子电荷                                 |
|                                 | `P_OrbCharges_M`          | 打印 Mulliken 轨道电荷                                 |
|                                 | `P_FragCharges_M`         | 打印 Mulliken 片段电荷                                 |
|                                 | `P_FragBondOrder_M`       | 打印 Mulliken 片段键级                                 |
|                                 | `P_BondOrder_M`           | 打印 Mulliken 键级                                     |
|                                 | `P_ReducedOrbPop_M`       | 打印 Mulliken 约化轨道电荷                             |
|                                 | `P_FragPopMO_M`           | 打印每个 MO 的 Mulliken 片段布居                       |
|                                 | `P_FragOvlMO_M`           | 打印每对片段的 Mulliken 重叠布居                       |
|                                 | `P_AtPopMO_M`             | 打印每个 MO 中的 Mulliken 原子电荷                     |
|                                 | `P_OrbPopMO_M`            | 打印每个 MO 的 Mulliken 轨道布居                       |
|                                 | `P_ReducedOrbPopMO_M`     | 打印每个 MO 的 Mulliken 约化轨道布居                   |
|                                 | `P_Loewdin`               | 打印 Loewdin 布居分析（默认 = 开）                     |
|                                 | `P_AtCharges_L`           | 打印 Loewdin 原子电荷                                  |
|                                 | `P_OrbCharges_L`          | 打印 Loewdin 轨道电荷                                  |
|                                 | `P_FragCharges_L`         | 打印 Loewdin 片段电荷                                  |
|                                 | `P_FragBondOrder_L`       | 打印 Loewdin 片段键级                                  |
|                                 | `P_BondOrder_L`           | 打印 Loewdin 键级                                      |
|                                 | `P_ReducedOrbPop_L`       | 打印 Loewdin 约化轨道电荷                              |
|                                 | `P_FragPopMO_L`           | 打印每个 MO 的 Loewdin 片段布居                        |
|                                 | `P_FragOvlMO_L`           | 打印每对片段的 Loewdin 重叠布居                        |
|                                 | `P_AtPopMO_L`             | 打印每个 MO 中的 Loewdin 原子电荷                      |
|                                 | `P_OrbPopMO_L`            | 打印每个 MO 的 Loewdin 轨道布居                        |
|                                 | `P_ReducedOrbPopMO_L`     | 打印每个 MO 的 Loewdin 约化轨道布居                    |
|                                 | `P_NPA`                   | 自然布居分析                                           |
|                                 | `P_Fragments`             | 打印片段信息                                           |
|                                 | `P_GUESSPOP`              | 打印初始猜测布居                                       |
|                                 | `P_UNO_FragPopMO_M`       | 打印每个 UNO 的 Mulliken 片段布居                      |
|                                 | `P_UNO_OrbPopMO_M`        | 打印每个 UNO 的 Mulliken 轨道布居                      |
|                                 | `P_UNO_AtPopMO_M`         | 打印每个 UNO 的 Mulliken 原子电荷                      |
|                                 | `P_UNO_ReducedOrbPopMO_M` | 打印每个 UNO 的 Mulliken 约化轨道布居                  |
|                                 | `P_UNO_FragPopMO_L`       | 打印每个 UNO 的 Loewdin 片段布居                       |
|                                 | `P_UNO_OrbPopMO_L`        | 打印每个 UNO 的 Loewdin 轨道布居                       |
|                                 | `P_UNO_AtPopMO_M`         | 打印每个 UNO 的 Loewdin 原子电荷                       |
|                                 | `P_UNO_ReducedOrbPopMO_L` | 打印每个 UNO 的 Loewdin 约化轨道布居                   |
|                                 | `P_UNO_OccNum`            | 打印每个 UNO 的占据数                                  |
|                                 | `P_AtomExpVal`            | 打印原子期望值                                         |
|                                 | `P_AtomBasis`             | 打印原子基组                                           |
|                                 | `P_AtomDensFit`           | 打印电子密度拟合                                       |
|                                 | `P_Symmetry`              | 对称性基本信息                                         |
|                                 | `P_Sym_Salc`              | 对称性处理打印                                         |
|                                 | `P_SCFSTABANA`            | SCF 稳定性分析的进度、收敛与结果信息                   |
|                                 | `P_DFTD`                  | 打印 Grimme 色散校正的相关信息                         |
|                                 | `P_DFTD_GRAD`             | 打印 Grimme 色散校正的梯度信息                         |
|                                 | `P_G1EL2EL`               | 打印对 g 张量的单电子与双电子贡献                      |
:::


各 PrintLevel 选项对应的默认设置如下：


(tab:essentialelements.output.printoptions.printleveldefaults)=
:::{table} 各 `PrintLevel` 所调用的默认打印选项。
| PrintLevel | 所含打印选项             |        |
|:-----------|:-------------------------|:-------|
| `mini`     | `P_OrbEn`                | `= 1`  |
|            | `P_Cartesian`            | `= 1`  |
|            | `P_InputFile`            | `= 1`  |
|            | `P_SCFIterInfo`          | `= 1`  |
| `small`    | 以上全部，外加           |        |
|            | `P_SCFInfo`              | `= 1`  |
|            | `P_Mayer`                | `= 1`  |
|            | `P_MULLIKEN`             | `= 1`  |
|            | `P_AtCharges_M`          | `= 1`  |
|            | `P_ReducedOrbPop_M`      | `= 1`  |
|            | `P_Loewdin `             | `= 1`  |
|            | `P_AtCharges_L`          | `= 1`  |
|            | `P_ReducedOrbPop_L`      | `= 1`  |
|            | `P_Fragments`            | `= 1`  |
|            | `P_FragCharges_M`        | `= 1`  |
|            | `P_FragBondOrder_M`      | `= 1`  |
|            | `P_FragCharges_L`        | `= 1`  |
|            | `P_FragBondOrder_L`      | `= 1`  |
|            | `P_DFTD`                 | `= 1`  |
| `normal`   | 以上全部，外加           |        |
|            | `P_Internal`             | `= 1`  |
|            | `P_BondOrder_L`          | `= 1`  |
|            | `P_BondOrder_M`          | `= 1`  |
|            | `P_FragPopMO_L`          | `= 1`  |
|            | `P_ReducedOrbPopMO_L`    | `= 1`  |
|            | `P_SCFIterInfo`          | `= 2 ` |
| `maxi`     | 以上全部，外加           |        |
|            | `P_OrbEn`                | `= 2`  |
|            | `P_GuessOrb`             | `= 1`  |
|            | `P_MOs`                  | `= 1`  |
|            | `P_Density`              | `= 1`  |
|            | `P_SpinDensity`          | `= 1`  |
|            | `P_Basis`                | `= 1`  |
|            | `P_FragOVLMO_M `         | `= 1`  |
|            | `P_OrbPopMO_M`           | `= 1`  |
|            | `P_OrbCharges_M`         | `= 1`  |
|            | `P_DFTD`                 | `= 2`  |
|            | `P_DFTD_GRAD`            | `= 1`  |
| `huge`     | 以上全部，外加           |        |
|            | `P_OneElec`              | `= 1`  |
|            | `P_Overlap`              | `= 1 ` |
|            | `P_S12`                  | `= 1`  |
|            | `P_AtPopMO_M`            | `= 1`  |
|            | `P_OrbPopMO_M`           | `= 1`  |
|            | `P_AtPopMO_L`            | `= 1`  |
|            | `P_EHTDetails`           | `= 1`  |
|            | `P_DFTD_GRAD`            | `= 2`  |
| `debug`    | 打印全部内容             |        |

:::

(sec:essentialelements.output.simplekeywords)=
## 简单输入关键词（Simple Input Keywords）

为方便起见，还实现了多种控制特定打印设置和额外输出的
简单输入关键词（参见 {numref}`tab:essentialelements.output.simplekeywords.keywords`）。

(tab:essentialelements.output.simplekeywords.keywords)=
:::{table} 用于特定输出控制的简单输入关键词。
| 关键词                          | 所切换的打印选项          | 说明                                                           |
|:--------------------------------|:--------------------------|:---------------------------------------------------------------|
| `MiniPrint`                     | `PrintLevel mini`         | 激活打印级别 mini                                              |
| `SmallPrint`                    | `PrintLevel small`        | 激活打印级别 small（默认）                                     |
| `NormalPrint`                   | `PrintLevel normal`       | 激活打印级别 normal                                            |
| `LargePrint`                    | `PrintLevel large`        | 激活打印级别 mini                                              |
| `PrintMOs`                      | `Print[ p_MOs ]`          | 打印 MO 系数                                                   |
| `NoPrintMOs`                    |                           | 抑制 MO 系数的打印                                             |
| `PrintBasis`                    | `Print[ p_basis ]`        | 以输入格式打印基组                                             |
| `PrintGap`                      | `Print[ p_homolumogap ]`  | 打印每次 SCF 迭代中的 HOMO/LUMO 能隙。                         |
| `ReducedPop`                    |                           | 打印每个 MO 的 Loewdin 约化轨道布居                            |
| `NoReducedPop`                  |                           | 关闭每个 MO 的 Loewdin 约化轨道布居打印                        |
| `AIM`                           |                           | 生成 WFN 文件                                                  |
| `XYZFILE`                       |                           | 生成 XYZ 坐标文件                                              |
| `PDBFILE`                       |                           | 生成 PDB 文件                                                  |
| `UNO`                           |                           | 生成 [UHF 自然轨道](sec:modelchemistries.hftype.uhfno)         |
| `NoPropFile`                    |                           | 不写入[性质文件](sec:property_file.detailed)                   |
| `KeepTransDensity`              |                           | 将跃迁密度矩阵保留在磁盘上                                     |
:::
