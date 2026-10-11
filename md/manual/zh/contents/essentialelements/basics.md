(sec:essentialelements.basics)=
# 基本计算设置（Basic Calculation Settings）

(sec:essentialelements.basics.runtypes)=
## 运行类型（Run Types）

要执行的计算类型既可以通过简单输入（simple input）来选择
——例如 `! Opt`——
也可以通过 `%method` 中的 `RunTyp` 变量来指定：

```orca
%method
  RunTyp  Gradient  # Single point energy and gradient
end
```

可用运行类型的完整列表见
{numref}`sec:essentialelements.basics.keywords`。
请注意，某些运行类型会在特定条件下自动触发，
无法通过 `RunTyp` 关键词显式请求。

(sec:essentialelements.basics.hamiltonians)=
## 方法类别（Method Classes）
ORCA 提供若干类方法：
Hartree--Fock（HF）、密度泛函理论（Density functional theory，DFT）、
基于 NDDO 方法的半经验方法等。
这一选择通过简单输入来控制，例如 `!HF`，
或通过 `%method` 块中的 `method` 变量来控制：

```orca
%method
  method DFT
end
```

可用方法列表见
{numref}`sec:essentialelements.basics.keywords`。

(sec:essentialelements.basics.keywords)=
## 关键词（Keywords）

:::{raw} latex
\begingroup
\footnotesize
:::

:::{tabularcolumns} \Y{0.3}\Y{0.7}
:::

(tab:essentialelements.basics.keywords.simple)=
:::{flat-table} 用于基本计算设置的简单输入关键词。
:class: footnotesize
:header-rows: 1
* - 关键词
  - 说明
* - {cspan}`1` *运行类型（Run Types）*
* - `Energy`
  - 单点能计算（默认。别名：`SinglePoint`、`SP`）
* - `EnGrad`
  - 单点能与梯度计算（别名：`EnergyGrad`）
* - `Opt`
  - [几何优化](sec:structurereactivity.optimization)，
    另见 {numref}`tab:structurereactivity.optimization.keywords.simple`
* - `MD`
  - [分子动力学模拟](sec:moldyn)
* - `CIM`
  - [分子中的簇](sec:modelchemistries.mdci.cim)（Cluster-in-molecules）计算
* - `PrintThermoChem`
  - 根据先前计算的 Hessian 进行[热化学计算](sec:structurereactivity.thermochemistry)
* - `PropertiesOnly`
  - 根据先前计算的密度[计算性质](sec:spectroscopyproperties.properties.proponly)
* - `Docker`
  - [主-客体对接](sec:structurereactivity.docker)
* - `EDA`
  - [能量分解分析](sec:spectroscopyproperties.nocv)
* - `NMScan`
  - **已弃用（Deprecated）！** 简正模式扫描（别名：`NormalModeScan`）
* - `NMGrad`
  - **已弃用（Deprecated）！** 简正模式梯度（别名：`NMGradient`）
* - `MTR`
  - **已弃用（Deprecated）！** 模式轨迹（别名：`MT`、`ModeTrajectory`）
* - {cspan}`1` *方法（Methods）*
* - `HF`
  - [Hartree--Fock](sec:essentialelements.hartreefock)；
    `RHF`、`UHF` 和 `ROHF` 同时设定[波函数类型](sec:modelchemistries.hftype)
* - `DFT`
  - [密度泛函理论](sec:modelchemistries.dft)；
    `RKS`、`UKS` 和 `ROKS` 同时设定[波函数类型](sec:modelchemistries.hftype)
* - `<NDO-Method>`
  - 基于 [NDO](sec:modelchemistries.semiempirical.ndo) 的方法关键词见
    {numref}`tab:modelchemistries.semiempirical.ndo.keywords.simple`
* - `<XTB-Method>`
  - 基于[原生 xTB](sec:modelchemistries.semiempirical.nativextb) 的方法关键词见
    {numref}`tab:modelchemistries.semiempirical.nativextb.keywords.simple`
* - `MM`
  - [分子力学](sec:modelchemistries.mm.orca)
:::
:::{raw} latex
\endgroup
:::

:::{raw} latex
\begingroup
\footnotesize
:::

:::{tabularcolumns} \Y{0.1}\Y{0.2}\Y{0.7}
:::

(tab:essentialelements.basics.keywords.block)=
:::{flat-table} 用于基本计算设置的 `%method` 块输入关键词。
:class: footnotesize
:header-rows: 1
* - 关键词
  - 选项
  - 说明
* - `RunTyp`
  - `Energy`
  - 单点能计算（默认。别名：`SinglePoint`、`SP`）
* - 
  - `Gradient`
  - 单点能与梯度计算
* - 
  - `Opt`
  - [几何优化](sec:structurereactivity.optimization)
    （别名：`Geom`、`Geometry`、`GeometryOpt`）
* - 
  - `Scan`
  - [非弛豫几何参数扫描](sec:essentialelements.coordinates.parascan)
    （别名：`Trajectory`）
* - 
  - `CIM`
  - [分子中的簇](sec:modelchemistries.mdci.cim)（Cluster-in-molecules）计算
* - 
  - `NMScan`
  - **已弃用（Deprecated）！** 简正模式扫描（别名：`NormalModeScan`）
* - 
  - `NMGrad`
  - **已弃用（Deprecated）！** 简正模式梯度（别名：`NMGradient`、`NormalModeGradient`）
* - 
  - `MTR`
  - **已弃用（Deprecated）！** 模式轨迹（别名：`MT`、`ModeTrajectory`）
* - `Method`
  - `HF`
  - （默认）[Hartree--Fock](sec:essentialelements.hartreefock)
* - 
  - `DFT`
  - [密度泛函理论](sec:modelchemistries.dft)
* - 
  - `<NDO-Method>`
  - 基于 [NDO](sec:modelchemistries.semiempirical.ndo) 的方法选项见
    {numref}`tab:modelchemistries.semiempirical.ndo.keywords.block`
:::
:::{raw} latex
\endgroup
:::
