<a id="sec:essentialelements.finEfield"></a>
# 外加电场（Finite Electric Fields）

电场可以对分子的电子结构产生显著影响。一般而言，当对分子施加电场时，分子的电子云会沿场的方向极化。由此引起的电荷重新分布会进一步影响分子的波函数。即使极化效应并不显著，电场仍会对分子中带负电和带正电的原子施加方向相反的作用力，从而影响分子的取向和结构。静电效应与极化效应的结合，使电场成为调节反应活性、分子结构和光谱等性质的有用自由度 [shaik2018CSR](../../bibliography.md)。同时，体系在弱偶极场或四极场中能量/偶极矩/四极矩的变化，可用于通过数值微分计算体系的许多电性质，包括偶极矩、四极矩、偶极-偶极极化率、四极-四极极化率等。这类有限差分性质计算可以方便地使用 [ORCA 复合脚本仓库（ORCA Compound Scripts Repository）](https://github.com/ORCAQuantumChemistry/CompoundScripts/tree/main/Polarizabilities)中的脚本完成。

相关关键字的概述见 [tab:essentialelements.finEfield.keywords.block](#tab:essentialelements.finEfield.keywords.block)。

<a id="sec:essentialelements.finEfield.dipolar"></a>
## 偶极电场（Dipolar Electric Fields）

可以通过 `%scf` 模块块中的 `EField` 关键字向计算中添加均匀（等价地讲，偶极）电场：

```orca
%scf
  EField 0.1, 0.0, 0.0 # x, y, z components (in au) of the electric field
end
```

尽管该关键字位于 `%scf` 模块块中，它同样会把电场施加到所有其他方法（后 HF 方法、多参考方法、TDDFT 等）上。对于所有已支持解析梯度的方法，电场的解析梯度贡献均可用，但解析 Hessian 贡献尚不可用。

!!! warning "警告"
    电场功能不适用于 [GFN-xTB](../modelchemistries/semiempirical.md#sec:modelchemistries.semiempirical.xtb) 和力场方法（以及任何涉及 GFN-xTB 或力场的方法，例如 [QM/XTB](../multiscalesimulations/qmmm-general.md#sec:multiscalesimulations.qmmm.orca) 和 [QM/MM](../multiscalesimulations/qmmm-general.md#sec:multiscalesimulations.qmmm.orca)）！与这些方法组合使用会导致计算中止。

电场的符号约定如下：假设电场由位于负 z 方向的正电荷和位于正 z 方向的负电荷产生，则电场的 z 分量为正。该约定与大多数（但并非全部）其他程序一致 [shaik2018CSR](../../bibliography.md)，因此在将 ORCA 的结果与其他程序比较时必须注意。

另一个重要方面是电场的规范原点（gauge origin）。电场的规范原点是电场产生的电势为零的点（更准确地说，是这样的点之一——这样的点有无穷多个）。规范原点的不同选择不影响分子的几何结构和波函数，因为它们不改变分子感受到的电场，但会改变分子的能量。默认的规范原点是笛卡尔坐标系的 (0,0,0) 点，但可以通过 `%scf` 模块块中的 `EFieldOrigin` 关键字选择其他规范原点。

```orca
%scf
 EFieldOrigin CenterOfMass      # use center of mass
              CenterOfNucCharge # use center of nuclear charge
              0.0, 0.0, 0.0     # use given X,Y,Z as origin (default: 0,0,0)
                                # in the units chosen for the coordinates (Angstrom/Bohr)
end
```

请注意，电场的默认规范原点与 ELPROP 模块的默认规范原点（质心）不同。若用户选择质心/核电荷中心作为电场的规范原点，则规范原点会随分子的平移而移动；这会带来重要影响。例如，在对电场中带电分子进行 MD 模拟时，分子不会加速；而当 `EFieldOrigin` 固定在给定坐标时，分子会一直加速。一般而言，`CenterOfMass` 和 `CenterOfNucCharge` 最适合电性质的有限差分计算，因为此时人们通常希望以质心或核电荷中心作为所得多极矩或极化率张量的规范原点。相反，对于模拟外加电场下波函数、几何结构、反应活性、光谱等的变化，固定原点往往更有用，因为实验中电场通常施加在实验室参考系中，而不是分子的随动参考系中。

<a id="sec:essentialelements.finEfield.quadrupolar"></a>
## 四极电场（Quadrupolar Electric Fields）

与偶极电场类似，四极场可通过 `%scf` 模块块中的 `QField` 关键字添加：

```orca
%scf
  QField 0.1, 0.0, 0.0, 0.05, 0.0, 0.0 # xx, yy, zz, xy, xz, yz components (in au)
                                       # of the quadrupolar field
end
```

四极场的规范原点与[偶极电场](#sec:essentialelements.finEfield.dipolar)相同。

<a id="sec:essentialelements.finEfield.combi"></a>
## 偶极电场与四极电场的组合

[偶极](#sec:essentialelements.finEfield.dipolar)和[四极电场](#sec:essentialelements.finEfield.quadrupolar)可通过 `%scf` 模块块中相应的 `EField` 与 `QField` 关键字组合使用。这使人们能够模拟逐渐变化的电场，例如下面的输入指定的电场在规范原点（默认为 (0,0,0)）处强度为 0.01 au、指向正 z 方向，并且沿正 z 方向每前进 1 Bohr 强度增加 0.001 au：

```orca
%scf
  EField 0.0, 0.0, 0.01
  QField 0.0, 0.0, 0.001, 0.0, 0.0, 0.0
end
```

作为第二个例子，也可以模拟离子阱：

```orca
%scf
  QField -0.01, -0.01, -0.01, 0.0, 0.0, 0.0
end
```

在这样的四极场设置下，粒子会感受到一个指向规范原点的电场，其强度（以 au 为单位）等于到规范原点距离（以 Bohr 为单位）的 0.01 倍。这会把阳离子束缚在原点附近，而把阴离子推离原点。遗憾的是，四极场目前没有解析梯度。

!!! note "关于电场的说明（Notes on Electric Fields）"
    -   au（原子单位）对电场来说是相当大的单位：1 au = 51.4 V/埃（Angstrom）。作为比较，蛋白质中的带电残基以及扫描隧道显微镜（STM）针尖通常产生约 1 V/埃以内的电场；在典型的电解条件下，电极表面通常产生 0.1 V/埃以内的电场 [shaik2018CSR](../../bibliography.md)。如果分子不在电场源附近，产生强电场就更困难：例如，相距 1 mm 的两块金属板之间加 100 V 电压，产生的电场仅为 $10^{-5}$ V/埃。因此，如果实验上某一强度的均匀电场似乎能促进反应，而计算中却看不到这种效应，请考虑实验观测到的反应活性可能来自电极表面附近的强局域电场（远高于体系中的平均场强），或者来自电解等其他效应。反之，如果你预测在例如 $>$ 0.1 au 的电场强度下分子性质会发生某种变化，那么这样的电场能否在实验上轻易实现可能并非一个简单的问题。

    -   电场破坏了分子的旋转对称性，因为旋转分子会改变其能量。因此，在电场中的几何优化不能使用内坐标。当用户请求几何优化时，程序若检测到电场会自动切换到笛卡尔坐标。虽然笛卡尔坐标可以正确处理分子的转动，但它们通常导致收敛较差，因此往往需要大量迭代。此外，由于某些几何优化任务（尤其是过渡态优化）目前只能在内坐标下完成，电场在这类优化任务中还无法使用。

    -   类似地，当分子带电时，其能量不再对平移不变。但是，当只有偶极电场而没有其他破坏平移对称性的力（四极场、点电荷、壁势）时，带电分子会在场中一直加速，其位置永远不会收敛。因此，对于纯偶极电场且无壁势的几何优化，即使平移能降低能量，我们也不允许分子的全局平移。但在 MD 模拟中，默认允许分子的全局平移。如果不希望如此，可以在 MD 运行中用 `CenterCOM` 关键字固定质心（见章节 [moldyn:cmd_run](#moldyn:cmd_run)）。

    -   对于电场中的[频率计算](../structurereactivity/frequencies.md#sec:structurereactivity.frequencies)，我们不对 Hessian 中的平动和转动贡献进行投影（等价于在 `%freq` 中设置 `ProjectTR false`；详见 [structurereactivity.frequencies](../structurereactivity/frequencies.md#sec:structurereactivity.frequencies)）。因此，平动和转动模式的频率可能不为零，并可能与振动模式混合。当电场极小但不为零时，Hessian "真正的"平动/转动对称性破缺可能小于数值误差造成的对称性破缺；在比较小电场下与零电场下的频率结果时必须记住这一点（后者的 `ProjectTR` 默认为 true）。此外，当平动和转动频率超过 `CutOffFreq`（默认为 1 cm$^{-1}$；见章节 [structurereactivity.frequencies](../structurereactivity/frequencies.md#sec:structurereactivity.frequencies)）时，它们的热化学贡献将按振动来计算。

    -   虽然程序允许电场与[隐式溶剂化模型](solvationmodels.md#sec:essentialelements.solvationmodels)联用，但结果必须谨慎解读，因为溶剂介质感受不到电场。因此，结果可能与溶质和溶剂都处于电场中的实验情形有实质性差异。如果溶剂对电场的响应很重要，应改用显式溶剂化模型。另外，也可以通过向体系中添加惰性离子（例如 Na$^+$、Cl$^-$）来模拟隐式溶剂中的电场。类似地，隐式溶剂化模型无法描述电场中双电层的形成及其对溶质性质的影响，因此在双电层很重要时，必须进行显式处理离子的 [MD 模拟](../moleculardynamics/moldyn.md#sec:moldyn)。

    -   电场不仅对核心哈密顿量有贡献，还会在 GIAO 计算中因偶极积分的磁场导数而产生额外贡献。对于偶极电场，GIAO 贡献已经实现，因此可以研究电场对 [NMR 屏蔽常数](../spectroscopyproperties/nmr.md#sec:spectroscopyproperties.nmr)的影响，以及作为特例的核独立化学位移（[NICS](../spectroscopyproperties/nmr.md#sec:spectroscopyproperties.nmr.NICS)），后者是分析芳香性的有用工具。[四极场](#sec:essentialelements.finEfield.quadrupolar)目前不能用于 GIAO 计算。

<a id="sec:essentialelements.finEfield.keywords"></a>
## 关键字（Keywords）

<a id="tab:essentialelements.finEfield.keywords.block"></a>
!!! note "外加电场的 `%scf` 模块块输入关键字与选项。"
    | Keyword          | Option                      | Description                                                                                                           |
    |:-----------------|:----------------------------|:----------------------------------------------------------------------------------------------------------------------|
    | `EField`         | `<x, y, z>`                 | 激活 x、y、z 分量（单位 au）的[偶极电场](#sec:essentialelements.finEfield.dipolar)                                          |
    | `QField`         | `<xx, yy, zz, xz, xz, yz>`  | 激活 xx、yy、zz、xz、xz、yz 分量（单位 au）的[四极电场](#sec:essentialelements.finEfield.quadrupolar)                          |
    | `EFieldOrigin`   | `CenterOfMass`              | 将原点设为质心                                                                                                           |
    |                  | `CenterOfNucCharge`         | 将原点设为核电荷中心                                                                                                       |
    |                  | `<X, Y, Z>`                 | 将原点设为 X,Y,Z 坐标（默认：0,0,0），单位取坐标所用的单位（埃/Bohr）                                                              |

