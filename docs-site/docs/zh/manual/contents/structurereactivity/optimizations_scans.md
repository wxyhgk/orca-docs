<a id="sec:structurereactivity.optimization.scans"></a>
# 势能面扫描（Surface Scans）

弛豫势能面扫描（relaxed surface scan）是探索势能面时的宝贵工具。它允许用户改变一个或多个坐标（键长、键角或二面角），同时弛豫其余自由度。本节概述理论背景，给出实际示例，并总结相关输入关键词。

---
<a id="sec:structurereactivity.optimization.relaxedsurface"></a>
## 理论（Theory）

在弛豫势能面扫描中，选定的坐标在给定范围内变化，并在每个点上执行约束几何优化（constrained geometry optimization）。这可以揭示过渡态、反应机理或近似能垒。ORCA 支持对键长（`B`）、键角（`A`）和二面角（`D`）进行扫描。

多个坐标也可以独立扫描（嵌套循环）或使用 `Simul_Scan` 关键词同时扫描，后者的计算成本更低。

---

## 简单示例（Simple Example）

以下输入将 C 与 O 之间的键长从 1.35 Å 扫描到 1.10 Å，共 12 个等距步长。每一步都涉及一次约束几何优化。

```
! B3LYP SV(P) Opt
%geom 
     scan
        B 0 1 = 1.35, 1.10, 12 # C-O distance that will be scanned
     end
end

* int 0 1
    C  0 0 0 0.0000   0.000    0.00
    O  1 0 0 1.3500   0.000    0.00
    H  1 2 0 1.1075 122.016    0.00
    H  1 2 3 1.1075 122.016  180.00
*
```

!!! note

    -   与约束几何优化中一样，弛豫势能面扫描的起始扫描参数可以不同于分子中当前存在的值。但请记住，该值不应偏离初始结构太远。

## 复杂示例（Complex Example）

下面给出了一个更具挑战性的示例。这里用弛豫势能面扫描计算 OH 自由基从 $\text{CH}_4$ 抽取氢原子的步骤（*vide supra*）。该作业的运行方式如下：

```
! B3LYP SV(P) Opt SlowConv NoTRAH
%geom 
    scan 
        B 1 0 = 2.0, 1.0, 15 
    end 
end
* int 0 2
 C     0   0   0   0.000000     0.000     0.000
 H     1   0   0   1.999962     0.000     0.000
 H     1   2   0   1.095870   100.445     0.000
 H     1   2   3   1.095971    90.180   119.467
 H     1   2   3   1.095530    95.161   238.880
 O     2   1   3   0.984205   164.404    27.073
 H     6   2   1   0.972562   103.807    10.843
*
```

很明显，该反应是放热的，并经过一个早期过渡态（early transition state），其中氢原子从碳跳跃到氧。曲线极大值处的结构很可能是真正过渡态的一个非常好的初始猜测，可用过渡态查找算法进一步定位。

你可能会发现，这类弛豫势能面扫描极其有用，但也非常耗时。即使下面这个简单的作业也需要数百次单点能和梯度计算（在接近过渡态时 SCF 会出现收敛问题，而一旦反应物真正解离，几何优化也会出现收敛问题——这是意料之中的）。然而，当你在寻找过渡态，或想深入了解反应所涉及的势能面形状时，使用这一功能或许是个好主意。减轻负担的一种可能性是：先用"快速"方法和较小的基组进行弛豫势能面扫描，然后对所有优化得到的几何结构用较大的基组和/或更高理论水平做单点计算。至少可以期望，只要低理论水平下的几何结构是合理的，这就能给出目标高理论水平势能面的一个合理近似。

<a id="fig:13"></a>
*OH 自由基从 CH$_4$ 抽取氢原子的弛豫势能面扫描（B3LYP/SV(P)）。*

## 多维扫描（Multidimensional Scans）

应广大用户的要求，ORCA 现在允许在一次计算中扫描多达三个坐标。

```
! B3LYP SV(P) Opt
%geom 
     scan
        B 0 1 = 1.35, 1.10, 12 # C-O distance that will be scanned
        B 0 2 = 1.20, 1.00, 5  # C-H distance that will be scanned
        A 2 0 1 = 140, 100, 5  # H-C-O angle that will be scanned
     end
end

* int 0 1
    C  0 0 0 0.0000   0.000    0.00
    O  1 0 0 1.3500   0.000    0.00
    H  1 2 0 1.1075 122.016    0.00
    H  1 2 3 1.1075 122.016  180.00
*
```

!!! note

    -   为了寻找更复杂反应路径的过渡态结构，ORCA 现在提供了非常高效的 NEB-TS 实现（见
        [structurereactivity.neb](neb.md#sec:structurereactivity.neb) 一节）。

    -   二维甚至三维弛豫势能面扫描可能变得非常昂贵——例如，若每个扫描请求 10 步，三维扫描中 ORCA 需要执行 1000 次约束优化。

    -   结果可能取决于各个扫描的方向以及扫描的顺序。

同时多维扫描（即所有扫描坐标同时改变）可通过以下关键词请求（它将多维弛豫势能面扫描的成本降低到单次弛豫势能面扫描的成本）：

```orca
%geom 
  Scan B 0 1 = 3, 1, 15 end
  Scan B 1 2 = 1, 3, 15 end
  Simul_Scan true
end
```

<a id="sec:structurereactivity.optimization.multiplexyz"></a>
## 多 XYZ 文件扫描（Multiple XYZ File Scans）

ORCA 中还结合弛豫势能面扫描实现了另一种类型的扫描。这类扫描产生一系列结构，这些结构通常用某种基态方法计算。之后，人们可能希望沿生成的反应路径做额外的或不同的计算，例如激发态计算或特殊性质计算。在这种情况下，"多 XYZ 扫描（multiple XYZ scan）"功能非常有用。若通过以下方式请求从 XYZ 文件读取：

```orca
* xyzfile Charge Multiplicity FileName
```

该文件可以包含若干结构。文件格式为：

```orca
Number of atoms M
  Comment line
AtomName1 X Y Z
AtomName2 X Y Z
...
AtomNameM X Y Z
Number of atoms M
  Comment line
AtomName1 X Y Z
...
```

也就是说，这些结构就是标准 XYZ 格式，并依次给出。它们之间无需添加任何额外字符。在 6.0.0 以前的 ORCA 版本中，结构之间用 "\>" 符号分隔。如果用户愿意，仍可使用该格式，但已不再需要。处理完 XYZ 文件后，将依次对每个结构执行单点计算，并在运行结束时将结果收集到与轨迹计算产生的相同类型的轨迹`.dat`文件中。

为了便于使用该功能，弛豫势能面扫描会生成一个名为 `MyJob.allxyz` 的文件，其格式正确，可在后续运行中重新读取。

<a id="sec:structurereactivity.optimization_scan.keywords"></a>
## 势能面扫描关键词（Surface Scan Keywords）

<a id="tab:geomscan.options"></a>
!!! note "`%geom` 块中用于势能面扫描几何优化的输入关键词和选项。"


| ****关键词**** | 选项 / 取值 | 说明 |
| --- | --- | --- |
| **`Scan`** | `B 1 2 = v1, v2, N` | 将原子 1 到原子 2 的键长从 v1 扫描到 v2，共 N 步。 |
| **—** | `B 1 2 [v1 v2 ...]` | 用自定义步长值扫描原子 1 到原子 2 的键。 |
| **—** | `A 1 2 3` | 用原子 1,2,3 扫描一个键角。 |
| **—** | `D 1 2 3 4` | 扫描原子 1,2,3,4 的二面角。 |
| **`Simul_Scan`** | `true` | 启用同时多维扫描（最多 3 个坐标）。 |
| **`FullScan`** | `true` | 在过渡态优化（`!ScanTS`）之前强制进行完整的势能面扫描。 |

