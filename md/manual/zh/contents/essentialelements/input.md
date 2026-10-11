(sec:essentialelements.input)=
# 输入文件的总体结构（General Structure of the Input File）

一般而言，输入文件是自由格式的 ASCII 文件，可以包含：
- 一行或多行以 "`!`" 字符开头的["简单"关键词行](sec:essentialelements.input.keywordlines)，
- 一个或多个介于 "`%`" 符号与 "`end`" 之间的[输入块](sec:essentialelements.input.blocks)，
  它们提供对计算特定方面的更精细控制，
- 体系的[坐标指定](sec:essentialelements.coordinates)、
  总电荷和自旋多重度，可以使用 `%coords` 块，
  或更常见地用两个 "`*`" 符号括起来。
  
下面是一个包含全部三种输入要素的简单输入文件示例：

```orca
! HF def2-TZVP

%scf
   convergence tight
end

* xyz 0 1
C  0.0  0.0  0.0
O  0.0  0.0  1.13
*
```

文件中的注释以 "\#" 开头。例如：

```orca
# This is a comment. Continues until the end of the line
```

注释也可以用第二个 "\#" 结束，如下面的例子所示，其中
`TolE` 和 `TolMaxP` 是两个可以由用户指定的变量：

```orca
TolE=1e-5;    #Energy conv.#  TolMaxP=1e-6; #Density conv.#
```

输入可以包含若干个块，它们由逻辑相关的、
可由用户控制的数据组成。程序会尝试为所有这些变量选择合理的
默认值。然而，不可能给出
对所有体系都同样合理的默认值。一般而言，
默认值略微偏保守，用户可以选择更激进的
截断阈值等，这可能有助于加快实际体系的计算速度，
或在需要时给出更高的精度。

:::{note}
- ORCA 输入**不**区分大小写。允许使用大写、小写或任意大小写组合。
  文件名是例外（例如 `%MOInp` 或 `*XYZName`），它们在类 Unix 操作系统上区分大小写。
- 一般而言，简单关键词和输入块的顺序并不重要——
  更细致的说明见 {ref}`sec:essentialelements.input.order`。
:::

(sec:essentialelements.input.blocks)=
## 输入块（Input Blocks）

输入块以 "`%`" 开头，后跟块名，并以 "`end`" 结束。
例如：

```orca
%method  
  method HF
END
```

可用输入块的列表见
{numref}`sec:essentialelements.input.blocklist`。
输入文件中*不需要*存在任何块，但如果需要对程序行为进行详细控制，则*可以*包含它们。
否则，大多数作业都可以通过
{numref}`sec:essentialelements.input.keywordlines` 中所述的简单关键词来定义。
块内的变量赋值具有以下一般结构：

```orca
VariableName Value
# or with an optional "=" sign
OtherVariableName = OtherValue
```

值可以是数值、引号定界的字符串（见下文），
或预定义的别名（如上例中的 `HF`），
这些别名在内部被转换为某种数值表示。

有些变量实际上是数组。在这种情况下，以下几种
赋值方式是有用的：

```orca
Array[1]  Value1
Array[1]  Value1,Value2,Value3
Array  Value1,Value2
```

:::{note}
在 ORCA 中数组总是从索引 0 开始（这是因为 ORCA
是一个 C++ 程序）。例子中的第一行将值
"`Value1`" 赋给 `Array[1]`，而这是该数组的*第二个*成员。
第二行将 `Value1` 赋给 `Array[1]`，`Value2` 赋给 `Array[2]`，
`Value3` 赋给 `Array[3]`。第三行将 `Value1` 赋给
`Array[0]`，将 `Value2` 赋给 `Array[1]`。
:::

字符串（例如文件名）必须用引号括起来。例如：

```orca
%scf
  MOInp  "Myfile.gbw"
end
```

请注意，类 Unix 系统上的文件名区分大小写
（即 `MYFILE.GBW` 和 `MyFile.gbw` 是不同的文件）。
在 Windows 下文件名不区分大小写。

某些输入块关键词要么打开一个嵌套的子块，
必须用额外的 `end` 关闭，
要么具有不同于上述简单变量赋值的特定语法。
例如：

```orca
%scf
  Guess PModel  # variable assignment
  SOSCF  # nested sub-block
    start 0.002  # variable assignment
  end  # closes the SOSCF sub-block
end
%mdci
  # special syntax
  MP2FragInter {1 1} {2 2}  
end
%basis
  NewGTO  # nested sub-block
    # special syntax inside
    H "def2-SVP"
    S 1
    1 0.05 1.0
  end  # closes the NewGTO sub-block
end
```

最后，还有一些输入"块"只设置一个变量
且不以 "`end`" 结束。
这些列在 {numref}`tab:essentialelements.input.simpleblocks` 中。
例如：

```orca
%MOInp "MyFile.gbw"
%maxcore 3000
```

(sec:essentialelements.input.order)=
## 输入优先级与处理顺序（Input Priority and Processing Order）

在较复杂的计算中，输入可能相当繁琐。
因此，了解程序在内部如何处理它是值得的：

- 首先，所有简单输入行（以 "`!`" 开头）被
  收集成一个字符串。
- 程序按预定义顺序查找所有已知关键词，
  而与输入文件中的顺序无关。
- 基组是例外：如果给出了两个不同的轨道基组
  （例如 `!` `def2-SVP` `def2-TZVP`），后者
  优先。同样的规则适用于相同类型的辅助基组
  （例如 `!` `def2/J` `SARC/J`）。
- 有些简单输入关键词会设置多个内部变量。
  因此，一个关键词有可能覆盖另一个关键词
  设置的选项。我们已尝试以
  合理的方式解决大多数这类情况（例如，更"具体"的关键词应当
  优先于更"一般"的关键词），但很难预见
  所有的选项组合。
- 接下来，块输入按其在
  输入文件中给出的顺序解析。
- 大多数块输入关键词控制单个变量（尽管存在
  例外）。如果一个关键词重复出现，则使用后一个值。
- 原则上，同一个块可以多次出现，各自设置不同的变量。
  然而，某些块在打开时会"重置"某些内部数据，
  或者具有必须出现在每个块实例中的强制内容
  （并覆盖先前的实例）。
  因此，不建议使用同一块的多个实例。

考虑下面这个（不好的）例子：

```orca
! def2-TZVP UKS
%method
  functional BP86
  correlation C_LYP
  SpecialGridAtoms[1]  26, 27
  SpecialGridIntacc 8,  8,  8
  SpecialGridAtoms 28, 29
end
! PBE def2-SVP RKS
```

运用上述规则，就能理解为什么它等同于下面这个：

```orca
! UKS BLYP def2-SVP
%method
  SpecialGridAtoms 28, 29, 27
  SpecialGridIntacc 8,  8,  8
end
```

(sec:essentialelements.input.globalmemuse)=
## 全局内存使用（Global Memory Use）
某些 ORCA 模块（特别是那些
执行某种基于波函数的关联计算的模块）
需要大型 scratch 数组。每个模块都有一个独立变量来
控制这些主要 scratch 数组的大小。然而，由于这些
模块从不同时运行，我们提供了一个全局变量
`MaxCore`，它为所有这些模块分配一定量的 scratch 内存。因此：

```orca
%MaxCore 2000
```

将这些 scratch 数组的上限设为 2000 MB。**这一
限制按每个处理核心适用**。如果程序占用
超过这个量——不要惊讶——这个大小只指主要的
工作区域。因此，你最好提供一个不超过
物理内存 75-80% 的数值。
有些耗内存的操作如果给的内存少于所需，将花更长时间，
而另一些如果 `MaxCore` 不足则会完全中止。
默认值是 4GB，对于大多数标准 DFT 计算来说已经很充裕。
对于耦合簇之类的计算，建议至少 8GB。

(sec:essentialelements.input.basename)=
## 更改默认 BaseName（Changing the Default BaseName）

ORCA 会生成一些输出文件以及许多临时文件，
后者在成功运行结束时被删除。
为防止文件名冲突，所有生成的文件都以相同的前缀或 *BaseName* 开头。
这通常由输入文件名去掉扩展名推断得到，
即用 `MyJob.inp` 运行 ORCA 将创建 `MyJob.gbw`、`MyJob.properties.txt` 等。
也可以使用 `%base` 变量显式设置 BaseName。
在下面的例子中，无论输入文件的名称是什么，所有生成文件的名称都将以 `job1` 开头：
```orca
%base "job1"
```

(sec:essentialelements.input.newjob)=
## 多步骤作业（Jobs with Multiple Steps）

:::{warning}
`$new_job` 功能是一个已弃用（deprecated）的功能。使用 `$new_job` 可能
导致后续计算结果不稳定、行为怪异。
请对这类任务使用 ORCA 的[复合（compound）](sec:workflowsautomatization.compound)功能
——它更安全，也强大得多！
:::

ORCA 支持包含多个作业的输入文件。此功能旨在
简化对同一分子的一系列密切相关的计算，
或对不同分子的计算。实现这一功能的目标包括：

-   对一个分子使用不同的理论
    方法和/或基组计算分子性质。

-   用相同的设置对一系列分子进行计算。

-   先做几何优化，再做更精确的单点计算，
    也许还要做性质计算。

-   用粗略计算提供良好的起始轨道，这些轨道随后
    可用于更大基组的后续计算。

例如，考虑下面的作业：第一步在 LDA 水平上计算
BO 的 g 张量，第二步使用
BP86 泛函。

```{literalinclude} ../../orca_working_input/C03S04_018.inp
:language: orca
```

使用 `$new_job` 功能时会发生的是，当前作业的
所有计算标志都从上一个作业传过来，用户
只需输入设置上的变化。因此，如果你
为某个计算打开了某些标志，而你不希望它们出现在
下一个计算中，你就必须自己把它们关掉（例如
RI 近似的使用）！此外，默认情况下新作业
会把旧作业的轨道作为输入。如果你不希望这样，
就必须通过显式指定你想要的猜测
来覆盖这一默认行为。

(sec:essentialelements.input.blocklist)=
## 输入块列表（List of Input Blocks）

{numref}`tab:essentialelements.input.blocks` 列出了已知的输入块名称，
以及可接受的同义词/别名。
每个块中定义的关键词列在手册的相应章节中，
表中也给出了指向这些列表的引用。
不以 `end` 结束的"块"列表见
{numref}`tab:essentialelements.input.simpleblocks`。

(tab:essentialelements.input.blocks)=
:::{flat-table} 输入块关键词。同义词列在括号中。
:header-rows: 1
:class: longtable
* - 块
  - 说明（关键词参考）
* - `autoci`
  - 自动生成的单参考与多参考关联方法
    ({numref}`sec:modelchemistries.autoci.keywords`)
* - `basis`
  - 基组
    ({numref}`tab:essentialelements.basisset.keywords.block`)
* - `casresp`
  - CASSCF 静态线性响应
    ({numref}`sec:spectroscopyproperties.casscfresp.keywords`)
* - `casscf`
  - CASSCF/NEVPT2 与 DMRG 计算
    ({numref}`sec:modelchemistries.casscf.keywords`)
* - `chelpg`
  - CHELPG 电荷
    ({numref}`sec:spectroscopyproperties.pop.chelpg.basicusage`)
* - `cim`
  - 分子中的簇（Cluster-in-molecules）计算
    ({numref}`sec:modelchemistries.mdci.cim`)
* - `cis` (`tddft`)
  - CIS 与 TD-DFT 计算
    ({numref}`sec:spectroscopyproperties.tddft.keywords`)
* - `compound`
  - 复合作业（Compound jobs）
    ({numref}`sec:workflowsautomatization.compound`)
* - `conical`
  - 锥形交叉的优化
    ({numref}`sec:structurereactivity.conicalintersections`)
* - `coords`
  - 原子坐标的输入
    ({numref}`sec:essentialelements.coordinates`)
* - `cosmors`
  - OpenCOSMO-RS 选项
    ({numref}`sec:essentialelements.solvationmodels.opencosmors.keywords`)
* - `cpcm`
  - 导体状极化连续模型（Conductor-like Polarizable Continuum Model）
    ({numref}`sec:essentialelements.solvationmodels.keyword-list.detailed`)
* - `docker`
  - 主-客体对接算法
    ({numref}`tab:structurereactivity.docker.keywords.block`)
* - `eda`
  - ({numref}`tab:NOCV_keywords`)
* - `elprop`
  - 电性质
    ({numref}`sec:spectroscopyproperties.properties.elprop.keywords`)
* - `eprnmr`
  - EPR 与 NMR 性质
    ({numref}`sec:spectroscopyproperties.properties.eprnmr`;
    g 张量: {numref}`tab:spectroscopyproperties.epr.g.keywords.block`,
    HFC: {numref}`tab:spectroscopyproperties.epr.hyperfine.keywords.block`,
    ZFS: {numref}`tab:spectroscopyproperties.epr.D.keywords.block`,
    Mössbauer: {numref}`tab:spectroscopyproperties.moessbauer.keywords.block`)
* - `esd`
  - 激发态动力学
    ({numref}`sec:spectroscopyproperties.esd.keywordlist`)
* - `frag`
  - 自动分片流程
    ({numref}`tab:essentialelements.keywordlist`)
* - `freq`
  - 振动频率
    ({numref}`sec:structurereactivity.frequencies.keywords`)
* - `geom`
  - 几何优化
    ({numref}`tab:structurereactivity.optimization.keywords.geom`;
    Scan: {numref}`tab:geomscan.options`,
    TS: {numref}`tab:ts.options`)
* - `goat`
  - 全局优化算法
    ({numref}`tab:structurereactivity.goat.keywords.block`)
* - `ice` (`iceci`,`cipsi`)
  - 迭代组态展开 CI 计算（Iterative configuration expansion CI）
    ({numref}`sec:modelchemistries.iceci.keywords`)
* - `irc`
  - 内禀反应坐标计算
    ({numref}`sec:structurereactivity.irc.keywords`)
* - `lft`
  - 配体场理论实用程序 `orca_lft`
    ({numref}`sec:utilities.lft`)
* - `loc`
  - 轨道定域化
    ({numref}`sec:utilities.loc`)
* - `mcrpa`
  - CASSCF 线性响应
    ({numref}`sec:spectroscopyproperties.mcrpa.keywords`)
* - `md`
  - 分子动力学
    ({numref}`tab:moldyn:commands.overview`)
* - `mdci`
  - 单参考关联方法
    ({numref}`sec:modelchemistries.mdci.keywords`;
    RHF EOM-CC: {numref}`tab:spectroscopyproperties.eom.options.rhfmdciblock`,
    UHF EOM-CC: {numref}`tab:spectroscopyproperties.eom.options.uhfmdciblock`,
    STEOM-CC: {numref}`sec:spectroscopyproperties.steom.general`,
    MR-EOM-CC: {numref}`sec:modelchemistries.mreom.details`,
    LED: {numref}`sec:spectroscopyproperties.led.features`,
    ADLD/ADEX: {numref}`sec:spectroscopyproperties.led.ad.keywords`,
    HFLD: {numref}`tab:spectroscopyproperties.hfld.keywords.block`)
* - `mecp`
  - 最小能量交叉点优化
    ({numref}`sec:structurereactivity.mecp.keywords`)
* - `method`
  - 计算方法的选择与各种选项
    - 运行类型与方法类别: {numref}`tab:essentialelements.basics.keywords.block`
    - RI/COSX: {numref}`tab:essentialelements.ri.keywords.block`
    - 网格: {numref}`sec:essentialelements.numericalintegration.SCFkeys`
    - CP-SCF: {numref}`sec:essentialelements.cpscf`
    - 冻结芯: {numref}`sec:essentialelements.frozencore`
    - 布居分析: {numref}`tab:spectroscopyproperties.pop.keywords.block.method`
    - DFT: {numref}`tab:modelchemistries.dft.gga.customizexc.keywords.block`
    - DFT/杂化: {numref}`tab:modelchemistries.dft.globalhybrids.customization.keywords.block`
    - DFT/范围分离: {numref}`tab:modelchemistries.dft.rangeseparatedhybrids.customization.keywords.block`
    - DFT/双杂化: {numref}`tab:modelchemistries.dft.doublehybriddft.customization.keywords.block.method`
    - DFT/LibXC: {numref}`sec:modelchemistries.dft.libxc`
    - DFT/色散: {numref}`tab:modelchemistries.dispersioncorrections.dftd.keywords.block`
    - DFT/NLC: {numref}`tab:modelchemistries.dispersioncorrections.nl.keywords.block`
    - gCP: {numref}`tab:essentialelements.counterpoise.gcp.keywords.block`
    - NDO: {numref}`tab:modelchemistries.semiempirical.ndo.keywords.block`
    - 原生 xTB: {numref}`tab:modelchemistries.semiempirical.nativextb.keywords.methodblock`
    - FMM: {numref}`sec:multiscalesimulations.fmm.reco`
* - `mm`
  - 分子力学力场
    ({numref}`sec:modelchemistries.mm-keywords`)
* - `mp2`
  - MP2 计算
    ({numref}`sec:modelchemistries.mp2.standard`;
    DLPNO: {numref}`sec:modelchemistries.mp2.dlpno`,
    DLPNO/gradient: {numref}`sec:modelchemistries.mp2.dlpnograd`,
    DLPNO/response: {numref}`sec:modelchemistries.mp2.dlpnoresp`,
    DLPNO/multi-level: {numref}`sec:modelchemistries.mp2.multilevel`,
    OO-RI-MP2: {numref}`sec:modelchemistries.mp2.optmethod.usage`,
    regularized: {numref}`sec:modelchemistries.mp2.regularized`)
* - `mrcc`
  - 多参考 CC 计算
    ({numref}`sec:modelchemistries.mrcc`)
* - `mrci`
  - 多参考 CI 计算
    ({numref}`sec:modelchemistries.mrci.keywords`)
* - `mtr`
  - 简正模式轨迹/扫描
    ({numref}`sec:spectroscopyproperties.tddft.scan.normalSurfaceScan`)
* - `nbo`
  - NBO 分析
    ({numref}`sec:spectroscopyproperties.nbo`)
* - `ndoparas`
  - 基于 NDO 的半经验方法参数
    ({numref}`tab:modelchemistries.semiempirical.ndo.paras`)
* - `neb`
  - NEB 计算
    ({numref}`sec:structurereactivity.neb.keywords`)
* - `numgrad`
  - 数值梯度
    ({numref}`sec:essentialelements.numericalgradients`)
* - `output`
  - 输出控制
    ({numref}`tab:essentialelements.output.printoptions.options`)
* - `pal`
  - 并行作业
    ({numref}`sec:essentialelements.parallel`)
* - `paras`
  - 几何参数的输入，等同于 `%coords` 中的 `paras` 或 `pardef`
    ({numref}`sec:essentialelements.coordinates.parascan`)
* - `plots`
  - 图形生成
    ({numref}`sec:utilities.plots`)
* - `qmmm`
  - 多尺度（QM/MM）计算
    ({numref}`sec:multiscalesimulations.qmmm.orca`)
* - `rel`
  - 相对论选项
    ({numref}`tab:essentialelements.relativistic.keywords.block`;
    SOC: {numref}`sec:spectroscopyproperties.soc`)
* - `rocis`
  - 限制性开壳层 CIS
    ({numref}`sec:spectroscopyproperties.rocis.keywords`)
* - `rr`
  - 通过 `orca_asa` 进行共振拉曼与吸收/荧光带形计算
    ({numref}`sec:spectroscopyproperties.asa.fitvalues`)
* - `scf`
  - SCF 流程设置
    ({numref}`sec:essentialelements.scfconvergence`;
    TRAH-SCF: {numref}`sec:essentialelements.scfconvergence.trahscf.keywords`,
    AVAS: {numref}`sec:modelchemistries.casscf.avas`,
    ROHF: {numref}`sec:modelchemistries.hftype.rohf`,
    native xTB: {numref}`tab:modelchemistries.semiempirical.nativextb.keywords.scfblock`,
    $\Delta$SCF: {numref}`tab:spectroscopyproperties.deltascf.options.scfblock`,
    初始猜测: {numref}`sec:essentialelements.initialguess`,
    旋转 MO: {numref}`sec:essentialelements.initialguess.changes`
    )
* - `shark`
  - SHARK 积分包
    ({numref}`sec:essentialelements.shark.keywords`)
* - `solvator`
  - 显式溶剂化算法
    ({numref}`tab:structurereactivity.solvator.keywords.block`)
* - `symmetry` (`sym`)
  - 空间对称性识别
    ({numref}`table:symmetry_block_options`)
* - `vpt2`
  - 振动微扰理论
    ({numref}`sec:spectroscopyproperties.vpt2`)
* - `xtb`
  - `xtb` 程序接口的选项
    ({numref}`tab:modelchemistries.semiempirical.xtb.keywords.block`)
:::

(tab:essentialelements.input.simpleblocks)=
:::{flat-table} 以 `%` 为前缀但没有结束 `end` 的输入关键词。
:header-rows: 1
:class: longtable
* - 关键词
  - 值
  - 说明（参考）
* - `base`
  - `"<BaseName>"`
  - 作业所创建文件的基本名
    ({numref}`sec:essentialelements.input.basename`)
* - `cclib`
  - `"<FileName>"`
  - 含 ICE-CI 单粒子耦合系数的文件
    ({numref}`sec:modelchemistries.iceci.cclib`)
* - `id`
  - `"<string>"`
  - **已弃用（Deprecated）！** 用于汇总计算能量的作业标识符
    ({numref}`sec:essentialelements.counterpoise.bbcp`)
* - `ljcoefficients`
  - `"<FileName>"`
  - 含 PHVA 用 Lennard--Jones 系数的文件
    ({numref}`sec:structurereactivity.geomopt.partialhess`)
* - `maxcore`
  - `4096`
  - 可使用的最大堆内存（MB），默认：4GB
    ({numref}`sec:essentialelements.input.globalmemuse`)
* - `moinp`
  - `"<FileName>"`
  - 用于 `MORead` 猜测读取猜测 MO 的 GBW 文件
    ({numref}`sec:essentialelements.initialguess.restart`)
* - `pointcharges`
  - `"<FileName>"`
  - 从中读取外部点电荷的文件
    ({numref}`sec:essentialelements.coordinates.pointcharges`)
:::

(sec:essentialelements.input.keywordlines)=
## 简单关键词行（Simple Keyword Lines）

可以给出一行关键词，这些关键词设置某些通常
属于不同输入块的变量。
这种"简单输入"的语法是面向行的。
关键词行以 "`!`" 符号开头，可以包含
任意数量的以空格分隔的关键词。
输入文件可以包含任意数量的关键词行，
它们不需要位于开头（尽管这是常见做法）——
另见 {ref}`sec:essentialelements.input.order`。

```orca
! Keyword1 Keyword2
! Keyword3
```

大多数简单输入关键词都在手册的相关章节中有说明。
{numref}`tab:essentialelements.input.keywordlines`
按主题分组提供了指向这些章节的引用。
由于简单关键词通常与一个或多个输入块中的变量相关，
查阅相应块的文档也很有帮助——
参见 {numref}`tab:essentialelements.input.blocks`。

(tab:essentialelements.input.keywordlines)=
:::{flat-table} 简单输入关键词文档的引用。相关输入块也一并列出。
:header-rows: 1
:class: longtable
* - 关键词组
  - 引用
  - 输入块
* - 运行类型与方法类别
  - {numref}`tab:essentialelements.basics.keywords.simple`
  - `method`
* - 基组
  - {numref}`tab:essentialelements.basisset.keywords.simple`
  - `basis`
* - DFT 泛函
  - - LDA: {numref}`tab:modelchemistries.dft.local`
    - GGA: {numref}`tab:modelchemistries.dft.gga`
    - 全局杂化: {numref}`tab:modelchemistries.dft.hybriddft.globlhybrids`
    - 范围分离杂化: {numref}`tab:modelchemistries.dft.rangeseparatedhybrids`
    - 全局双杂化: {numref}`tab:modelchemistries.dft.doublehybriddft.globaldoublehybrids`
    - 范围分离双杂化: {numref}`tab:modelchemistries.dft.doublehybriddft.rangeseparateddoublehybrids`
    - LibXC: {numref}`tab:modelchemistries.dft.libxc.simpleinput`
    - 非局域关联: {numref}`tab:modelchemistries.dispersioncorrections.nl.keywords.simple`
  - `method`
* - 色散校正
  - {numref}`tab:modelchemistries.dispersioncorrections.dftd.keywords.simple`
  - `method`
* - 复合（3c）方法
  - {numref}`tab:modelchemistries.3cmethods.keywords.simple`
  - 
* - 基于 NDO 的半经验方法
  - {numref}`tab:modelchemistries.semiempirical.nativextb.keywords.simple`
  - `method`
* - 基于原生 xTB 的方法
  - {numref}`tab:modelchemistries.semiempirical.ndo.keywords.simple`
  - `method`
* - 二阶 Møller--Plesset 微扰理论
  - {numref}`tab:modelchemistries.mp2.keywords.simple`
  - `mp2`
* - 通过 MDCI 的单参考关联方法
  - {numref}`tab:modelchemistries.mdci.keywords.simple`
  - `mdci`
* - 使用自动代码生成（AUTOCI）的关联方法
  - {numref}`sec:modelchemistries.autoci.available`
  - `autoci`
* - CASSCF
  - {numref}`tab:modelchemistries.casscf.keywords.simple`
  - `casscf`
* - 通过 MRCI 的多参考关联方法
  - {numref}`tab:modelchemistries.mrci.keywords.simple`
  - `mrci`
* - 通过基于关联波函数方法的激发态
  - - EOM-CC: {numref}`tab:spectroscopyproperties.eom.options.simple`
    - STEOM-CC: {numref}`sec:spectroscopyproperties.steom`
    - 其他: {numref}`sec:spectroscopyproperties.excitedstates`
  - `mdci`
* - 初始猜测
  - {numref}`tab:essentialelements.initialguess.keywords.simple`
  - `scf`
* - SCF 流程
  - {numref}`tab:essentialelements.scf.keywords.simple`
  - `scf`
* - 积分近似（RI/COSX）
  - {numref}`tab:essentialelements.ri.keywords.simple`
  - `method`
* - 相对论方法
  - {numref}`tab:essentialelements.relativistic.keywords.simple`
  - `rel`
* - 隐式溶剂化（CPCM）
  - {numref}`table:list-solvents`
  - `cpcm`
* - 自旋-轨道耦合算符
  - {numref}`tab:spectroscopyproperties.soc.keywords.simple`
  - `rel`
* - 数值积分网格
  - {numref}`tab:defgrids`
  - `method`
* - 积分存储与处理
  - {numref}`tab:essentialelements.integralhandling.keywords.simple`
  - `scf`
* - 布居分析
  - {numref}`tab:spectroscopyproperties.pop.keywords.simple`
  - `output`
* - 输出控制
  - {numref}`tab:essentialelements.output.simplekeywords.keywords`
  - `output`
* - 微动弹性带方法
  - {numref}`sec:structurereactivity.neb.keywords`
  - `neb`
:::
