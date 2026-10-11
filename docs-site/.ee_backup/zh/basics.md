<a id="sec:essentialelements.basics"></a>
# 基本计算设置（Basic Calculation Settings）

<a id="sec:essentialelements.basics.runtypes"></a>
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
[sec:essentialelements.basics.keywords](#sec:essentialelements.basics.keywords)。
请注意，某些运行类型会在特定条件下自动触发，
无法通过 `RunTyp` 关键词显式请求。

<a id="sec:essentialelements.basics.hamiltonians"></a>
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
[sec:essentialelements.basics.keywords](#sec:essentialelements.basics.keywords)。

<a id="sec:essentialelements.basics.keywords"></a>
## 关键词（Keywords）

<a id="tab:essentialelements.basics.keywords.simple"></a>
!!! note "用于基本计算设置的简单输入关键词。"
    :class: footnotesize
    :header-rows: 1

| 项目 | 内容 |
| --- | --- |
| **关键词** | 无 |

      - 说明

| 项目 | 内容 |
| --- | --- |
| **{cspan}`1` *运行类型（Run Types）*** | 无 |
| **`Energy`** | 无 |

      - 单点能计算（默认。别名：`SinglePoint`、`SP`）

| 项目 | 内容 |
| --- | --- |
| **`EnGrad`** | 无 |

      - 单点能与梯度计算（别名：`EnergyGrad`）

| 项目 | 内容 |
| --- | --- |
| **`Opt`** | 无 |

      - [几何优化](sec:structurereactivity.optimization)，
        另见 [tab:structurereactivity.optimization.keywords.simple](#tab:structurereactivity.optimization.keywords.simple)

| 项目 | 内容 |
| --- | --- |
| **`MD`** | 无 |

      - [分子动力学模拟](sec:moldyn)

| 项目 | 内容 |
| --- | --- |
| **`CIM`** | 无 |

      - [分子中的簇](sec:modelchemistries.mdci.cim)（Cluster-in-molecules）计算

| 项目 | 内容 |
| --- | --- |
| **`PrintThermoChem`** | 无 |

      - 根据先前计算的 Hessian 进行[热化学计算](sec:structurereactivity.thermochemistry)

| 项目 | 内容 |
| --- | --- |
| **`PropertiesOnly`** | 无 |

      - 根据先前计算的密度[计算性质](sec:spectroscopyproperties.properties.proponly)

| 项目 | 内容 |
| --- | --- |
| **`Docker`** | 无 |

      - [主-客体对接](sec:structurereactivity.docker)

| 项目 | 内容 |
| --- | --- |
| **`EDA`** | 无 |

      - [能量分解分析](sec:spectroscopyproperties.nocv)

| 项目 | 内容 |
| --- | --- |
| **`NMScan`** | 无 |

      - **已弃用（Deprecated）！** 简正模式扫描（别名：`NormalModeScan`）

| 项目 | 内容 |
| --- | --- |
| **`NMGrad`** | 无 |

      - **已弃用（Deprecated）！** 简正模式梯度（别名：`NMGradient`）

| 项目 | 内容 |
| --- | --- |
| **`MTR`** | 无 |

      - **已弃用（Deprecated）！** 模式轨迹（别名：`MT`、`ModeTrajectory`）

| 项目 | 内容 |
| --- | --- |
| **{cspan}`1` *方法（Methods）*** | 无 |
| **`HF`** | 无 |

      - [Hartree--Fock](sec:essentialelements.hartreefock)；
        `RHF`、`UHF` 和 `ROHF` 同时设定[波函数类型](sec:modelchemistries.hftype)

| 项目 | 内容 |
| --- | --- |
| **`DFT`** | 无 |

      - [密度泛函理论](sec:modelchemistries.dft)；
        `RKS`、`UKS` 和 `ROKS` 同时设定[波函数类型](sec:modelchemistries.hftype)

| 项目 | 内容 |
| --- | --- |
| **`<NDO-Method>`** | 无 |

      - 基于 [NDO](sec:modelchemistries.semiempirical.ndo) 的方法关键词见
        [tab:modelchemistries.semiempirical.ndo.keywords.simple](#tab:modelchemistries.semiempirical.ndo.keywords.simple)

| 项目 | 内容 |
| --- | --- |
| **`<XTB-Method>`** | 无 |

      - 基于[原生 xTB](sec:modelchemistries.semiempirical.nativextb) 的方法关键词见
        [tab:modelchemistries.semiempirical.nativextb.keywords.simple](#tab:modelchemistries.semiempirical.nativextb.keywords.simple)

| 项目 | 内容 |
| --- | --- |
| **`MM`** | 无 |

      - [分子力学](sec:modelchemistries.mm.orca)

<a id="tab:essentialelements.basics.keywords.block"></a>
!!! note "用于基本计算设置的 `%method` 块输入关键词。"
    :class: footnotesize
    :header-rows: 1

| 项目 | 内容 |
| --- | --- |
| **关键词** | 无 |

      - 选项
      - 说明

| 项目 | 内容 |
| --- | --- |
| **`RunTyp`** | 无 |

      - `Energy`
      - 单点能计算（默认。别名：`SinglePoint`、`SP`）

| 项目 | 内容 |
| --- | --- |
| **—** | 无 |

      - `Gradient`
      - 单点能与梯度计算

| 项目 | 内容 |
| --- | --- |
| **—** | 无 |

      - `Opt`
      - [几何优化](sec:structurereactivity.optimization)
        （别名：`Geom`、`Geometry`、`GeometryOpt`）

| 项目 | 内容 |
| --- | --- |
| **—** | 无 |

      - `Scan`
      - [非弛豫几何参数扫描](sec:essentialelements.coordinates.parascan)
        （别名：`Trajectory`）

| 项目 | 内容 |
| --- | --- |
| **—** | 无 |

      - `CIM`
      - [分子中的簇](sec:modelchemistries.mdci.cim)（Cluster-in-molecules）计算

| 项目 | 内容 |
| --- | --- |
| **—** | 无 |

      - `NMScan`
      - **已弃用（Deprecated）！** 简正模式扫描（别名：`NormalModeScan`）

| 项目 | 内容 |
| --- | --- |
| **—** | 无 |

      - `NMGrad`
      - **已弃用（Deprecated）！** 简正模式梯度（别名：`NMGradient`、`NormalModeGradient`）

| 项目 | 内容 |
| --- | --- |
| **—** | 无 |

      - `MTR`
      - **已弃用（Deprecated）！** 模式轨迹（别名：`MT`、`ModeTrajectory`）

| 项目 | 内容 |
| --- | --- |
| **`Method`** | 无 |

      - `HF`
      - （默认）[Hartree--Fock](sec:essentialelements.hartreefock)

| 项目 | 内容 |
| --- | --- |
| **—** | 无 |

      - `DFT`
      - [密度泛函理论](sec:modelchemistries.dft)

| 项目 | 内容 |
| --- | --- |
| **—** | 无 |

      - `<NDO-Method>`
      - 基于 [NDO](sec:modelchemistries.semiempirical.ndo) 的方法选项见
        [tab:modelchemistries.semiempirical.ndo.keywords.block](#tab:modelchemistries.semiempirical.ndo.keywords.block)

