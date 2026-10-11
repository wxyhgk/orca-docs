```{index} Self-Consistent-Field (SCF)
```

(sec:essentialelements.scfconvergence)=
# 自洽场（Self-Consistent-Field，SCF）

SCF 收敛是任何电子结构
程序包中的一个紧迫问题，因为总执行时间随
迭代次数线性增长。因此，提升
SCF 程序性能的最佳方式是让它收敛得更好，这一点至今成立。在某些
情况下，尤其是对于开壳层过渡金属配合物，收敛
可能非常困难。ORCA 为此做出了专门努力，在不牺牲
效率的前提下为这些情况实现合理的 SCF 收敛。

另一个问题是 ORCA 找到的解是否稳定，即它是否为
轨道旋转曲面上的极小点。特别是对于开壳层
单重态，获得破缺对称解可能很困难。SCF
稳定性分析（见
{ref}`sec:essentialelements.stabilityanalysis` 一节）在这类
情形下可能会有所帮助。另请注意，如果使用 `! TRAH`，该解
必须是真正的局域极小，但不一定是全局极小。

:::{tip}
期望值 $\left<S^2\right>$ 是体系中自旋
污染的一种估计。对于开壳层
体系，尤其是过渡金属配合物，强烈建议检查 UCO
（非限制性对应轨道，unrestricted corresponding orbitals，参见 {ref}`sec:modelchemistries.hftype.unoucoqro`）
的重叠并可视化对应轨道。
此外，对贡献于单占据
轨道的原子上的自旋布居也是电子结构的一个判据。
:::

(sec:essentialelements.scfconvergence.tol)=
## 收敛容差（Convergence Tolerances）
```{index} SCF Convergence
```

在讨论如何使 SCF 计算收敛之前，应当先定义
"收敛"的含义。ORCA 有多种选项来控制
能量和波函数的目标精度，可在
`% scf` 块中选择，或用把判据标签与 "SCF" 合并的简单输入行关键词
来选择，例如 `! StrongSCF` 或
`! VeryTightSCF`：

```orca
%scf
  Convergence             # The default convergence is between medium and strong
               Sloppy     # very weak convergence
               Loose      # still weak convergence
               Medium     # intermediate accuracy
               Strong     # stronger
               Tight      # still stronger
               VeryTight  # even stronger
               Extreme    # close to numerical zero of the computer
                          # in double precision arithmetic
 end
```

与其他关键词一样，`Convergence` 是一个复合关键词，它为
下面方框中给出的多种其他变量赋默认值。
在 {numref}`compoundConvergenceThresholds` 中我们给出了每个复合关键词
所选的值。如果给出了相应的简单输入
（`!StrongSCF`、`!VeryTightSCF` 等），则还会设置
{numref}`compoundAdditionalConvergenceThresholds` 中的值，
它们也会影响 SCF 之后模块的行为。
默认收敛判据是合理的，对
大多数目的应该足够。对于布居的粗略查看，较弱的收敛可能
就够了，而另一些情况可能需要比默认
更强的收敛。请注意，`Convergence` 不仅影响目标
收敛容差，还影响积分精度，如关于直接 SCF 等的
章节所讨论的那样。
**这一点非常重要：如果
积分误差大于收敛判据，直接 SCF 计算就
不可能收敛。**

收敛判据总是打印在输出中。下面给出
`! TightSCF` 的收敛判据列表，它常用于
过渡金属配合物的计算。

```orca
%scf
  TolE        1e-8  # energy change between two cycles
  TolRMSP     5e-9  # RMS density change
  TolMaxP     1e-7  # maximum density change
  TolErr      5e-7  # DIIS error convergence
  TolG        1e-5  # orbital gradient convergence
  TolX        1e-5  # orbital rotation angle convergence
  Thresh    2.5e-11 # integral prescreening threshold
  TCut      2.5e-12 # primitive integral prescreening cutoff
  ConvCheckMode  2  # = 0: check all convergence criteria
                    # = 1: stop if one of criterion is met, this is sloppy!
                    # = 2: check change in total energy and in one-electron energy
                    #      Converged if delta(Etot)<TolE and delta(E1)<1e3*TolE
  ConvForced        # = 0: convergence not mandatory for next calculation step
                    # = 1: break, if you did not meet the convergence criteria
end
%method
  Z_Tol       1e-4  # CP-SCF solver tolerance
  BFCut       1e-11 # basis function cutoff for numerical integration
end

# Additional tolerances modified by the simple input
%casscf
  GTol       2.5e-4
  ETol       2.5e-8
end
%mdci
  STol         1e-5
end
%autoci
  STol         1e-5
end
%mrci
  ETol       2.5e-7
  RTol       2.5e-7
end
%cis
  ETol       2.5e-7
  RTol       2.5e-7
end
```

(compoundConvergenceThresholds)=
:::{flat-table} 收敛关键词的阈值选择。
:header-rows: 1

* - 变量
  - 值

* - {cspan}`1` *Sloppy* (`!SloppySCF`/`Convergence Sloppy`)

* - `TolE`
  - 3e-5
* - `TolMAXP`
  - 1e-4
* - `TolRMSP`
  - 1e-5
* - `TolErr`
  - 1e-4
* - `Thresh`
  - 1e-9
* - `TCut`
  - 1e-10
* - `BFCut`
  - 1e-10
* - `TolG`
  - 3e-4
* - `TolX`
  - 3e-4
* - `Z_Tol`
  - 5e-3

* - {cspan}`1` *Loose* (`!LooseSCF`/`Convergence Loose`)

* - `TolE`
  - 1e-5
* - `TolMAXP`
  - 1e-3
* - `TolRMSP`
  - 1e-4
* - `TolErr`
  - 5e-4
* - `Thresh`
  - 1e-9
* - `TCut`
  - 1e-10
* - `BFCut`
  - 1e-10
* - `TolG`
  - 1e-4
* - `TolX`
  - 1e-4
* - `Z_Tol`
  - 3e-3

* - {cspan}`1` *Medium* (`!MediumSCF`/`Convergence Medium`)

* - `ConvCheckMode`
  - 2
* - `TolE`
  - 1e-6
* - `TolMAXP`
  - 1e-5
* - `TolRMSP`
  - 1e-6
* - `TolErr`
  - 1e-5
* - `Thresh`
  - 1e-10
* - `TCut`
  - 1e-11
* - `BFCut`
  - 1e-10
* - `TolG`
  - 5e-5
* - `TolX`
  - 5e-5
* - `Z_Tol`
  - 1e-3

* - {cspan}`1` *Strong* (`!StrongSCF`/`Convergence Strong`)

* - `ConvCheckMode`
  - 2
* - `TolE`
  - 3e-7
* - `TolMAXP`
  - 3e-6
* - `TolRMSP`
  - 1e-7
* - `TolErr`
  - 3e-6
* - `Thresh`
  - 1e-10
* - `TCut`
  - 3e-11
* - `BFCut`
  - 3e-11
* - `TolG`
  - 2e-5
* - `TolX`
  - 2e-5
* - `Z_Tol`
  - 7e-4

* - {cspan}`1` *Tight* (`!TightSCF`/`Convergence Tight`)

* - `ConvCheckMode`
  - 2
* - `TolE`
  - 1e-8
* - `TolMAXP`
  - 1e-7
* - `TolRMSP`
  - 5e-9
* - `TolErr`
  - 5e-7
* - `Thresh`
  - 2.5e-11
* - `TCut`
  - 2.5e-12
* - `BFCut`
  - 1e-11
* - `TolG`
  - 1e-5
* - `TolX`
  - 1e-5
* - `Z_Tol`
  - 1e-4

* - {cspan}`1` *VeryTight* (`!VeryTightSCF`/`Convergence VeryTight`)

* - `ConvCheckMode`
  - 2
* - `TolE`
  - 1e-9
* - `TolMAXP`
  - 1e-8
* - `TolRMSP`
  - 1e-9
* - `TolErr`
  - 1e-8
* - `Thresh`
  - 1e-12
* - `TCut`
  - 1e-14
* - `BFCut`
  - 1e-12
* - `TolG`
  - 2e-6
* - `TolX`
  - 2e-6
* - `Z_Tol`
  - 3e-5

* - {cspan}`1` *Extreme* (`!ExtremeSCF`/`Convergence Extreme`)

* - `ConvCheckMode`
  - 0
* - `TolE`
  - 1e-14
* - `TolMAXP`
  - 1e-14
* - `TolRMSP`
  - 1e-14
* - `TolErr`
  - 1e-14
* - `Thresh`
  - 3e-16
* - `TCut`
  - 3e-16
* - `TolG`
  - 1e-09
* - `TolX`
  - 1e-09
* - `Z_Tol`
  - 3e-06
* - `BFCut`
  - 3e-16
:::

(compoundAdditionalConvergenceThresholds)=
:::{flat-table} 由简单输入关键词（`!StrongSCF` 等）设置的额外阈值选择。
:header-rows: 1

* - 块
  - 变量
  - 值

* - {cspan}`2` *Sloppy* (`!SloppySCF`)
* - `casscf`
  - `GTol`
  - 5.0e-3
* - 
  - `ETol`
  - 1.0e-6
* - `mdci`
  - `STol`
  - 1.0e-4
* - `mrci`
  - `ETol`
  - 1.0e-5
* - 
  - `RTol`
  - 1.0e-5
* - `cis`
  - `ETol`
  - 1.0e-5
* - 
  - `RTol`
  - 1.0e-5

* - {cspan}`2` *Loose* (`!LooseSCF`)
* - `casscf`
  - `GTol`
  - 5.0e-3
* - 
  - `ETol`
  - 1.0e-6
* - `mdci`
  - `STol`
  - 1.0e-4
* - `autoci`
  - `STol`
  - 1.0e-4
* - `mrci`
  - `ETol`
  - 1.0e-5
* - 
  - `RTol`
  - 1.0e-5
* - `cis`
  - `ETol`
  - 1.0e-5
* - 
  - `RTol`
  - 1.0e-5

* - {cspan}`2` *Normal* (`!NormalSCF`)
* - `casscf`
  - `GTol`
  - 1.0e-3
* - 
  - `ETol`
  - 1.0e-7
* - `mdci`
  - `STol`
  - 2.5e-5
* - `autoci`
  - `STol`
  - 2.5e-5
* - `mrci`
  - `ETol`
  - 1.0e-6
* - 
  - `RTol`
  - 1.0e-6
* - `cis`
  - `ETol`
  - 1.0e-6
* - 
  - `RTol`
  - 1.0e-6

* - {cspan}`2` *Strong* (`!StrongSCF`)
* - `casscf`
  - `GTol`
  - 5.00e-4
* - 
  - `ETol`
  - 6.66e-8
* - `mdci`
  - `STol`
  - 7.50e-6
* - `autoci`
  - `STol`
  - 7.50e-6
* - `mrci`
  - `ETol`
  - 6.66e-7
* - 
  - `RTol`
  - 6.66e-7
* - `cis`
  - `ETol`
  - 6.66e-7
* - 
  - `RTol`
  - 6.66e-7

* - {cspan}`2` *Tight* (`!TightSCF`)
* - `casscf`
  - `GTol`
  - 2.5e-4
* - 
  - `ETol`
  - 2.5e-8
* - `mdci`
  - `STol`
  - 1.0e-5
* - `autoci`
  - `STol`
  - 1.0e-5
* - `mrci`
  - `ETol`
  - 2.5e-7
* - 
  - `RTol`
  - 2.5e-7
* - `cis`
  - `ETol`
  - 2.5e-7
* - 
  - `RTol`
  - 2.5e-7

* - {cspan}`2` *VeryTight* (`!VeryTightSCF`)
* - `casscf`
  - `GTol`
  - 1.0e-5
* - 
  - `ETol`
  - 1.0e-8
* - `mdci`
  - `STol`
  - 1.0e-6
* - `autoci`
  - `STol`
  - 1.0e-6
* - 
  - `D3Thresh`
  - 1.0e-14
* - 
  - `D4Thresh`
  - 1.0e-14
* - 
  - `D5Thresh`
  - 1.0e-14
* - `mrci`
  - `ETol`
  - 1.0e-7
* - 
  - `RTol`
  - 1.0e-7
* - `cis`
  - `ETol`
  - 1.0e-7
* - 
  - `RTol`
  - 1.0e-7

* - {cspan}`2` *Extreme* (`!ExtremeSCF`)
* - `casscf`
  - `GTol`
  - 1.0e-9
* - 
  - `ETol`
  - 1.0e-12
* - `mdci`
  - `STol`
  - 1.0e-9
* - 
  - `TCutInt`
  - 0.0
* - `autoci`
  - `STol`
  - 1.0e-9
* - 
  - `D3Thresh`
  - 1.0e-14
* - 
  - `D4Thresh`
  - 1.0e-14
* - 
  - `D5Thresh`
  - 1.0e-14
* - `mrci`
  - `ETol`
  - 1.0e-12
* - 
  - `RTol`
  - 1.0e-12
* - `cis`
  - `ETol`
  - 1.0e-12
* - 
  - `RTol`
  - 1.0e-12
:::

还有另一组简单关键词，
`!SCFCONV<n>`，其中 $n$ = 6--12（例如 `!SCFCONV8`），
它将 `TolE` 设为 $10^{-n}$，并把上面列出的*大多数*其他容差
设置为合适的值。
不过，有些容差，如 `Z_Tol`、`TolRMSP` 和 `TolMAXP` 并不会被调整！
因此，建议改用上面给出的关键词。

如果 `ConvCheckMode=0`，*所有*收敛判据都必须满足，
程序才会接受该计算为已收敛，这是一个相当
严格的判据。在这一模式下，程序也有机制来
判定即便某一个收敛判据
未满足但其他判据都超额完成，计算也算收敛。`ConvCheckMode=1`
意味着满足一个判据就够了。这相当危险，因此要确保
没有哪个判据太弱，否则结果将
不可靠。默认的 `ConvCheckMode=2` 是中等严格程度的检查——
程序检查总能量的变化以及
单电子能量的变化。如果总能量与单电子
能量的比值保持不变，自洽场就不再
涨落，计算可视为已收敛。如果重叠矩阵有很小的
本征值，密度可能无法收敛到
`TolMaxP` 和 `TolRMSP` 所要求的有效数字位数。

`ConvForced` 是一个防止在
未收敛波函数上进行耗时计算的标志。对于 Post-HF 方法、激发态计算和破缺对称计算，它默认为
`ConvForced=1`。
你可以通过设置 `ConvForced=0` 来覆盖这一默认行为。

无论选择何种 `ConvForced` 值，都不会对
未收敛的波函数执行性质
或数值计算（NumGrad、NumFreq）！

(sec:essentialelements.scfconvergence.damping)=
## 动态阻尼与静态阻尼（Dynamic and Static Damping）
```{index} SCF Damping
```

阻尼（damping）是最古老也最简单的收敛辅助手段。它早在
Douglas Hartree 做他著名的原子计算时就被发明了。
阻尼是将旧密度与新密度按下式混合：

$$P_{\text{new, damped} } =\left({ 1-\alpha } \right)P_{\text{new} } +\alpha P_{\text{old} }
$$ (eq:50)

其中 $\alpha$ 是阻尼因子，其值必须小于
1。因此允许的范围（程序不检查）是 0
...0.999999。对于大于 1 的 $\alpha$ 值，计算无法
进行，因为没有混入新密度。阻尼在计算的
早期阶段很重要，那时 $P_{\text{old} }$ 与
$P_{\text{new} }$ 彼此差异很大，能量在
强烈涨落。已有许多方案被提出，动态地改变
阻尼因子，以便在开始时强阻尼、
在 SCF 结束时不阻尼。ORCA 中实现的方案是
Hehenberger 和 Zerner 的方案 {cite}`zerner1979chem`，通过
`CNVZerner=true` 调用。静态阻尼通过 `CNVDamp=true` 调用。这些
收敛器互斥。它们可以在计算开始时使用，当计算还不在 DIIS 或
SOSCF 的收敛半径之内时。阻尼效果还行，但 ORCA 中的大多数其他收敛器
更强大。

如果阻尼与 DIIS 或 SOSCF 联用，`DampErr` 的
值很重要：一旦 DIIS 误差降到 `DampErr` 以下，
阻尼就被关闭。如果使用 SOSCF，`DampErr` 指的是
关闭阻尼时的轨道梯度值。默认
值是 0.1 Eh。但在困难的情况下，选择
小得多的 `DampErr` 是个好主意，例如 0.001。这在一定程度上
会随关键词 `! SlowConv` 一起自动选定。

```orca
%scf
  # control of the Damping procedure
  CNVDamp   true    # default: true
  CNVZerner false   # default: false
  DampFac   0.98    # default: 0.7
  DampErr   0.05    # default: 0.1
  DampMin   0.1     # default: 0.0
  DampMax   0.99    # default: 0.98
  # more convenient:
  Damp fac 0.98 ErrOff 0.05 Min 0.1 Max 0.99 end
end
```

(sec:essentialelements.scfconvergence.levelshift)=
## 能级移动（Level Shifting）
```{index} SCF Level Shift
```

能级移动（level shifting）是一种常用技术。其基本思想是
移动虚轨道的能量，使得对角化
之后占据轨道与虚轨道的混合变弱，
计算更平稳地向目标态收敛。此外，
能级移动还应防止在近简并情形下电子态的翻转。在一个特殊语境下，Saunders 和 Hillier {cite}`guest1974mol,saunders1973int` 已证明它
等价于阻尼。

与前一节所述的 `DampErr` 类似，`ShiftErr`
指的是关闭能级移动时的 DIIS 误差。

```orca
%scf
  # control of the level shift procedure
  CNVShift   true  # default: true
  LShift     0.1   # default: 0.25, energy unit is Eh.
  ShiftErr   0.1   # default: 0.0
  # more convenient:
  Shift Shift 0.1 ErrOff 0.1 end
end
```

(sec:essentialelements.scfconvergence.diis)=
## 迭代子空间直接求逆（Direct Inversion in Iterative Subspace，DIIS）
```{index} DIIS
```

迭代子空间直接求逆（DIIS）是
Pulay 发明的一种技术 {cite}`pulay1980chem,pulay1982comp`。它
已成为大多数现代电子结构
程序中的*事实*标准，因为 DIIS 稳健、高效且易于实现。
基本上 DIIS 用一个判据来判断给定试探密度
离自洽还有多远。Fock 矩阵与密度
矩阵的对易子 \[**F**,**P**\] 是衡量这一误差的便捷指标。利用
这些信息，可以从当前和
先前的 Fock 矩阵构造一个外推的 Fock 矩阵，它应该更接近
自洽。实践中通常确实如此，并且用 DIIS 观察到了优于
线性收敛的收敛速度。然而在某些罕见的
（开壳层）情况下，DIIS 在取得一些初步进展后收敛缓慢或不收敛。随着接近自洽，DIIS 要求解的
线性方程组趋于线性相关，此时用因子 `DIISBfac` 使 DIIS 偏向于能量最低的
SCF 循环是有用的。做法是将 DIIS 矩阵的
所有对角元都乘以该因子，除非它对应于导致
最低能量的 Fock 矩阵/密度。`DIISBfac` 的默认值
是 1.05。

`DIISMaxEq` 的值是要记住的旧 Fock 矩阵的最大数目。
有人推荐 5-7，而另一些用户存储
10-15 个 Fock 矩阵。如果标准 DIIS 未能实现收敛，
对该参数做些试验可能是值得的。在 DIIS 于 SCF 开始时
就引起问题的情况下，可能需要
在稍后阶段才启用它。DIIS 过程的开始
由 `DIISStart` 控制。它的默认值是 0.2 Eh，这
通常在 0-3 个循环后启动 DIIS。控制 DIIS
开始的另一种方式是调整 `DIISMaxIt` 的值，它设定
开始 DIIS 的最大循环次数，之后无论
误差值如何都会启动 DIIS。

```orca
%scf
  # control of the DIIS procedure
  CNVDIIS     true  # default: true
  DIISStart   0.1   # default: 0.2
  DIISMaxIt   5     # default: 12
  DIISMaxEq   7     # default: 5
  DIISBFac    1.2   # default: 1.05
  # more convenient:
  DIIS Start 0.1  MaxIt 5  MaxEq 7  BFac 1.2  MaxC 15.0  end
end
```

请注意，对于棘手或缺失的 SCF 收敛，应当使用 `TRAH` 算法
（参见 {ref}`sec:essentialelements.scfconvergence.trahscf` 一节）。
除非被显式关闭，`TRAH` 会在存在收敛问题时通过 `AutoTRAH` 功能
自动开启
（参见 {ref}`sec:essentialelements.scfconvergence.trahscf` 一节）。

(sec:essentialelements.scfconvergence.kdiis)=
## Kolmar 的 DIIS（KDIIS）
```{index} KDIIS
```

另一种利用 DIIS 概念的替代算法在 ORCA 中称为
KDIIS（Kolmar 的 DIIS{cite}`kollmar1996chem,kollmar1997int`）。KDIIS 算法旨在利用 DIIS
外推与一阶微扰理论的组合，将任意能量表达式的轨道
梯度变为零。因此，该方法
无需对角化。根据我们的经验，它在许多情况下优于标准 DIIS
算法，但并非总是如此。该算法通过
关键词 `! KDIIS` 调用，可用于 RHF、UHF 和 CASSCF。

(sec:essentialelements.scfconvergence.soscf)=
## 近似二阶 SCF（Approximate Second Order SCF，SOSCF）
```{index} SOSCF
```

SOSCF 是 SCF
过程的一种近似二次收敛变体 {cite}`fischer1992phys,neese2000chem`。其理论相对
复杂，这里不再赘述。简而言之——SOSCF 计算
轨道 Hessian 之逆的一个初始猜测，然后用
BFGS 公式以递归方式更新轨道旋转角。随着
几次迭代信息的积累，对轨道 Hessian 之逆的
猜测越来越好，计算进入
超线性收敛区。就其实现而言，该过程
收敛得与 DIIS 一样好或略好，耗时也略少。
不过，它也*远*不如 DIIS 稳健，因此对许多问题 DIIS
仍是首选方法（另见下一节中对完整二阶信赖域
增广 Hessian（`TRAH`）过程的描述）。另一方面，当 DIIS 卡在约 $\sim$ 0.001 或
0.0001 的误差上时，SOSCF 是有用的。这类情况正是将
SOSCF 实现到 ORCA 中的主要动机。

SOSCF 的缺点如下：在 SCF 开始时，
轨道梯度（总能量对描述占据 MO 与虚 MO 混合的旋转的
导数）很大，因此远离二次收敛区。在这种情况下，
该过程不会成功，甚至可能严重发散。因此建议
只在 SCF 的最末阶段调用 SOSCF 过程，那时 DIIS 可能导致"拖尾"收敛。SOSCF 由
变量 `SOSCFStart` 和 `SOSCFMaxIt` 控制。`SOSCFStart` 是
轨道梯度的阈值。当轨道梯度，或
等价地 DIIS 误差，降到 `SOSCFStart` 以下时，就启动 SOSCF
过程。`SOSCFMaxIt` 是启动 SOSCF 的最晚迭代次数，即使
轨道梯度仍高于 `SOSCFStart`。

```orca
%scf
  # control of the SOSCF procedure
  CNVSOSCF    true  # default: false
  SOSCFStart  0.1   # default: 0.01
  SOSCFMaxIt  5     # default: 1000
  # more convenient:
  SOSCF Start 0.1  MaxIt 5  end
end
```

对于过渡金属配合物的许多计算，在 SOSCF 的启动判据上
保守一些是个好主意，否则它可能发散。
推荐选择 0.01 或更低。

(sec:essentialelements.scfconvergence.trahscf)=
## 信赖域增广 Hessian（Trust-Region Augmented Hessian，TRAH）SCF
```{index} TRAH
```

**信赖域增广 Hessian（TRAH）**方法{cite}`Bacskay1981,Salek2007,Hoeyvik2012,Helmich-Paris2021b`
是一种稳健的 SCF 收敛算法，它利用电子 Hessian 的信息来确保可靠地收敛
到电子基态。
它对于标准 DIIS/SOSCF 方法失败的困难 SCF 情形尤为有用，
例如开壳层体系或具有复杂电子结构的分子。

### 何时使用 TRAH

TRAH-SCF 过程可以：
- 使用 `! TRAH` 关键词**手动激活**。
- 在标准 SCF 收敛过慢或发散时**自动触发**（`AutoTRAH`）。

```orca
%scf
  AutoTRAH true
end
```

#### AutoTRAH

自动模式（`AutoTRAH`）通过对多次 SCF 迭代中的电子梯度范数做对数尺度
线性插值来监控行为。
在最少 SCF 迭代次数（`AutoTRAHIter`，默认：20）之后，该算法
分析最近 `AutoTRAHNInter`（默认：10）个梯度范数值。
在 $\log_{10}(||\mathbf{g}||)$ 空间中进行线性拟合，并用
该插值的斜率 $s$ 来评估收敛。
如果斜率表明收敛速率慢于 $10^{-s}$，其中 $s < \texttt{AutoTRAHTol}$
（默认：1.125），则停止标准 SCF，并以当前轨道集合启动 TRAH-SCF。

这一机制使 ORCA 仅在必要时才切换到更稳健的 TRAH-SCF 方法，从而在困难 SCF 情形下提高效率，同时避免简单情形下的不必要开销。

要禁用自动激活：

```orca
! NOTRAH
```
或
```orca
%scf
  AutoTRAH false
end
```

### 理论基础（Theoretical Basis）

TRAH 将 SCF 能量构建为轨道旋转 $\mathbf{x}$ 的二次模型：

$$
E(\mathbf{x}) = E_0 + \mathbf{g}^T \mathbf{x} + \frac{1}{2} \mathbf{x}^T \mathbf{H} \mathbf{x}, \quad ||\mathbf{x}|| \le h
$$

在信赖域约束下最小化 $E(\mathbf{x})$ 导出能级移动的 Newton 方程：

$$
(\mathbf{H} - \mu \mathbf{I}) \mathbf{x} = -\mathbf{g}
$$

该算法不直接求解这些方程，而是求解缩放增广 Hessian 矩阵的本征值问题：

$$
\begin{pmatrix}
  0 & \alpha \mathbf{g}^T \\
  \alpha \mathbf{g} & \mathbf{H}
\end{pmatrix}
\begin{pmatrix}
  1 \\
  \tilde{\mathbf{x}}
\end{pmatrix}
= \mu
\begin{pmatrix}
  1 \\
  \tilde{\mathbf{x}}
\end{pmatrix}
$$

使用 Davidson 算法进行迭代对角化，直到 $\tilde{\mathbf{x}}$ 的残差范数低于 `TolFacMicro × ||g||`。
缩放因子 $\alpha$ 通过对分法在
区间 $[\alpha_0,\alpha_1]$ 中调整，以确保信赖域约束得到满足。

### 性能与实现细节（Performance and Implementation Details）

- **并行化**：TRAH 是 MPI 并行的，并支持使用基于 AO 的 Fock 矩阵处理大分子。
- **加速**：TRAH 支持 `RIJ`、`RIJONX`、`RIJK` 和 `RIJCOSX`，并与 `C-PCM` 和 `SMD` 等溶剂化模型兼容。
- **可用方法**：已为 `RHF`、`RKS`、`UHF` 和 `UKS` 实现。`ROHF` 和 `ROKS` 尚不支持。
- **高效的 Hessian 运算**：与 CP-SCF 和 TD-DFT 类似，梯度和 Hessian 运算使用基于 AO 的 sigma 向量以提高效率。

用于加速这些步骤的网格参数：

```orca
%method
  Z_GridXC   1      // Lebedev Grid
  Z_IntAccXC 3.467  // eps parameter of radial grid
  Z_GridX    1      // Lebedev Grid
  Z_IntAccX  3.067  // eps parameter of radial grid
end
```

(sec:essentialelements.scfconvergence.trahscf.keywords)=
### 输入参数（Input Parameters）
```{index} SCF Keywords
```

```orca
%scf

 # AutoTRAH parameter
 AutoTRAH       true      # enables by default
 AutoTRAHTol    1.125     # slop of gradient convergence
 AutoTRAHIter   20        # first iteration for which TRAH could be called
 AutoTRAHNInter 10        # number of iteration for monitoring convergence progress

 # TRAH parameter
 trah
   MaxRed          24     # maximum number of Davidson micro iterations
   NStart          2      # number of start vectors for Davidson (at least 2)
   TolFacMicro     0.1    # Scaling factor for Davidson convergence
                          #  threshold =  TolFacMicro * || G ||    
   MinTolMicro     1.e-2  # minimum accuracy of micro iterations
   QuadRegionStart 1.e-4  # start Newton-Raphson if || G || < QuadRegionStart 
   tradius         0.4    # initial trust radius
   AlphaMin        0.1    # lower bound of gradient scaling parameter
   AlphaMax        1000.  # upper bound of gradient scaling parameter
   Randomize       true   # add white noise to Davidson start vectors
   PseudoRand      false  # use pseudo random numbers for comparibility
   MaxNoise        1.e-2  # maximum random number magnitude
   OrbUpdate       Taylor # orbital update algorithm (TAYLOR or CAYLEY)
   InactiveMOs     Canonical # CANONICAL or NOTSET
   Precond         Diag   # DIAG, FULL, or NONE
   PreconMaxRed    250    # maximum dimension of FULL Hessian for preconditioning
 end

 TolG 1.e-6  # SCF convergence threshold for gradient norm

end
```

- `Precond = FULL` 对重要的 MO 对子集使用精确 Hessian，可改善小型 RHF/UHF 体系的收敛，但对大分子或 DFT 未必如此。
- 对于 `FULL`，请确保提供了 RI 和辅助基组（`/C`）。

### 实用说明（Practical Notes）

- **二次收敛**：在解附近，TRAH 达到二次收敛。
- **保证收敛**：在精确算术且无数值噪声的情况下，TRAH 总会收敛。如果没有，请增大 `MAXITER` 或收紧数值阈值（例如网格精度）。
- **LibXC 兼容性**：某些泛函缺少 ORCA 原生内核（例如 `PWPB95`）。请使用 `LIBXC(...)` 以获得 TRAH 支持。

### 示例案例（Example Case）

在一个高自旋 $\mathrm{Rh}_{12}^+$ 团簇中，DIIS 无法收敛，而 TRAH 稳步将梯度范数降到 $10^{-6}$ 以下：

```{figure} ../../images/trah_scf_typical.*
高自旋组态（$\mathrm{M_s} = 36$）下 $\mathrm{Rh}_{12}^+$ 团簇
PBE/def2-TZVP 计算的 TRAH-SCF 梯度范数。
结构取自参考文献 {cite}`Harding2010`。
```

(sec:essentialelements.scf.finitetemp)=
## 有限温度 SCF（Finite Temperature SCF）
```{index} FT-DFT, Fermi Smearing
```

有限温度可用于在体系的轨道上施加一种类 Fermi 的占据数
抹平（smearing），这有时可能有助于
在几乎无望的情况下获得 SCF 方程的收敛。通过
抹平，电子按 Fermi 统计
分布在可用轨道上。"化学势"通过
总电子数保持正确的条件求得。
在存在占据数抹平的情况下可以计算梯度。

```orca
%scf SmearTemp 5000  # ``temperature'' in Kelvin
 end
```

:::{Note}

-   有限温度 SCF（分数占据数或 FOD
    分析，
    分别参见 {ref}`sec:essentialelements.scf.fracocc` 和
    {ref}`sec:spectroscopyproperties.fod` 两节）*不能*
    与 `SOSCF` 方法一起使用。
:::

(sec:essentialelements.scf.fracocc)=
### 分数占据数（Fractional Occupation Numbers）
```{index} Fractional Occupation
```

目前只提供了分数占据数的一种非常基本的实现。
它旨在处理 UHF/UKS 方法中轨道简并的态。
它主要是为避免 DFT 计算中轨道简并的分子和
原子出现对称性破缺而实现的。程序检查初始猜测
轨道的轨道能量，找出简并集合并在
其中平均占据数。目前简并轨道的判据是 $10^{-3}$
Eh。分数占据数选项通过以下方式调用：

```orca
%scf
  FracOcc true
end
```

显然，分数占据数的威力远远超出
程序目前所实现的范围，未来的版本很可能会
更多地利用它们。程序在使用
分数占据数时会打印警告。应当检查被分数占据的轨道，
以确保它们确实是预期的那些。

:::{Note}

-   使用 `GuessMode = CMatrix` 会引起问题，因为初始猜测轨道
    没有轨道能量。程序随后会对*所有*轨道取平均——
    这完全没有意义。
:::

(sec:essentialelements.scfconvergence.tips)=
## 技巧与窍门：使 SCF 计算收敛（Tips and Tricks: Converging SCF Calculations）
```{index} SCF Convergence Issues
```

尽管尽了一切努力，你仍可能发现某些分子的 SCF 收敛
很差。这些几乎无一例外地与开壳层情形
有关，而答案几乎总是提供"更好的"起始轨道。
下面是我处理这一问题的标准策略（假定是 DFT
计算）：

-   使用 `LSD` 或
    `BP` 泛函做一次小基组（`SV`）计算，并使用 RI 近似和廉价的辅助基组。
    设置 `Convergence=Loose` 和 `MaxIter=200` 左右。关键点
    是使用大的阻尼因子，并一直阻尼到 DIIS 进入
    收敛域。这由 `SlowConv` 甚至
    `VerySlowConv` 完成。如果你的情况更加病态，你可能
    需要把 `DampFac` 设得更大、`DampErr` 设得比这些默认值
    更小。这个计算相当粗糙，可能需要很多
    循环才能收敛。不过就挂钟时间而言它会相当快。如果 DIIS 卡在约 0.001 的误差上，可以
    从这一点起启用 `SOSCF`（或者更好的是 `TRAH`）。

-   用该计算的轨道和 `GuessMode=CMatrix` 来
    启动目标基组的计算。在 DFT 中我们通常
    使用纯 GGA 泛函（例如 BP86）。这一计算通常
    收敛得相对平稳。

-   使用目标泛函、网格等来使最终计算
    收敛。在许多情况下，现在它应该收敛得相当好。

还有几件可以尝试的事情：

-   试着从相关闭壳层物种的轨道开始。一般
    而言，闭壳层 MO 计算往往收敛得更好。这样你
    就有望进入开壳层情形下另一种收敛器的
    收敛半径。

-   试着从更正的阳离子的轨道开始。阳离子
    计算往往收敛得更好。

-   试着从更小基组的计算开始。较小的
    基组收敛得更好。然后你可以选择
    `GuessMode=CMatrix` 或 `GuessMode=FMatrix`，这将影响
    收敛行为。

-   使用大的能级移动。这会增加迭代次数但
    稳定收敛器。（`shift shift 0.5 erroff 0 end`）

-   如果你做的是 DFT 计算，试着从你分子的 Hartree-Fock
    解开始。HF 计算往往收敛得
    略好，因为它们有较大的 HOMO-LUMO 能隙（当然
    也有例外）。

-   仔细查看起始轨道（`Print[P_GuessOrb]=1`），
    看它们对你的分子是否合理。也许你必须
    重排它们（使用 `Rotate`）才能获得平稳的收敛。

-   大多数时候收敛问题来自"不合理的"
    结构。你确认过你的坐标是
    正确的单位（Angström 还是 Bohr？）并且已被
    程序正确识别吗？

-   如果你做 UHF 计算有困难，先试试 ROHF（尤其是 SAHF
    或 CAHF），然后再转到 UHF 计算。

-   捣鼓一下 `Guess=Hueckel`、`PAtom `甚至 `HCore`。

-   有时先收敛到一个不想要的态，
    然后取这个态的轨道，重排它们（使用 `Rotate`），
    再尝试收敛到目标态，可能更好。

-   类似地，可以利用 SCF 稳定性
    分析（见
    {ref}`sec:essentialelements.stabilityanalysis` 一节）来操纵坏轨道，
    以提供新的猜测。

-   试着以大的阻尼因子
    （`DampFac=0.90`；甚至更大）开始计算，并指定一个相对较小的 DIIS
    误差来关闭阻尼（比如 `DampErr=0.02`;）。这会增加
    循环次数，但可能引导你进入一个计算
    实际上能收敛的区域。

-   以上建议大多适用于 Hartree-Fock 和 DFT。对于 CASSCF，
    可用的选项及其如何帮助克服收敛
    问题在 CASSCF 手册章节中有描述。在许多情况下，
    修改初始猜测或添加能级移动会有所帮助。不要
    犹豫使用大的能级移动（例如 2.0 甚至 3.0）。手册
    附有 CASSCF 教程，其中详述了该过程的许多
    细节，包括关于收敛的实用建议。
    初始猜测的选择至关重要。某些猜测对
    有机分子更有效，而另一些则在过渡金属配合物上表现出色。
    因此该教程讨论了 ORCA 中可用的
    各种初始猜测选项。

-   如果你已经在另一个量子化学
    程序中成功收敛了你的体系，而不想浪费时间在 ORCA 中重新收敛，那么
    你可以用 MOKIT 等第三方工具把另一个程序中收敛的轨道转换为
    ORCA 格式（见 {ref}`sec:utilities.2mkl` 一节）。
    不过，请记住，在程序 A 中收敛一个波函数然后
    在程序 B 中重新收敛，会带来不可避免的开销：即使波函数
    在程序 A 中已完全收敛，程序
    B 通常仍要执行几次额外的 SCF 迭代，因为（除许多其他原因外）
    两个程序一般使用不同的积分网格。因此，
    只有当你预期能节省可观的时间时才使用此方法。

-   如果以上都不管用，就停下来，拉上一个朋友去附近的酒吧
    （你也可以给我发一封不友好的电子邮件，但这很可能
    不会让你的计算收敛得更快；$\ddot \smile$）。

(sec:essentialelements.localSCF)=
## 局域 SCF 方法（Local-SCF Method）

由 X. Assfeld 和 J.-L. Rivail 开发的局域 SCF（LSCF）方法（{cite}`LSCF`）允许在保持某些选定轨道冻结（即不变）的约束下优化单行列式波函数，同时所有轨道都满足正交性要求。LSCF 方法可应用于非限制性 Hartree-Fock 或 DFT 计算。

LSCF 方法的使用包括根据计算的猜测轨道来选定在 SCF 过程中要冻结的轨道集合。选择通过在 SCF 块中对 alpha 和 beta 轨道分别使用 `LSCFalpha` 和/或 `LSCFbeta` 关键词来进行，后接轨道选择。使用**区间**来定义选择，最多可达五个区间（5$\times$2 个数字，用逗号分隔）。在下面的例子中，`LSCFalpha 0,1,4,4,10,12` 对应于冻结从 0 到 1 的 alpha 轨道（**0,1**,4,4,10,12）、轨道 4（0,1,**4,4**,10,12）以及从 10 到 12 的轨道（0,1,4,4,**10,12**）。相应地，`LSCFbeta  0,3,5,5` 对应于冻结 beta 轨道 0 到 3 以及轨道 5。

```orca
%scf
LSCFalpha 0,1,4,4,10,12
LSCFbeta  0,3,5,5
end
```

冻结轨道的能量是没有意义的，因为它们不是 Fock 算符的本征函数。在 LSCF 过程中，占据冻结轨道的能量被人为定义为猜测轨道的最低占据轨道能量减去 1000 Hartree，而对于虚冻结轨道，其能量被定义为最高虚轨道能量加上 1000 Hartree。因此，所有占据冻结轨道都被排在轨道分布的最前面，虚冻结轨道排在最后面。

(sec:essentialelements.scf.keywords)=
## 关键词（Keywords）

与 SCF 过程相关的简单输入关键词汇总于
{numref}`sec:essentialelements.scf.keywords`。

:::{raw} latex
\begingroup
\footnotesize
:::
(tab:essentialelements.scf.keywords.simple)=
:::{flat-table} SCF 过程的简单输入关键词
:header-rows: 1
:class: footnotesize
* - 关键词
  - 说明
* - {cspan}`1` *收敛加速*
* - `DIIS`
  - 启用 [DIIS](sec:essentialelements.scfconvergence.diis)
* - `NoDIIS`
  - 禁用 [DIIS](sec:essentialelements.scfconvergence.diis)
* - `KDIIS`
  - 启用 [Kollmar 的 DIIS](sec:essentialelements.scfconvergence.kdiis)
* - `TRAH`
  - 启用 [TRAH](sec:essentialelements.scfconvergence.trahscf)
* - `NoTRAH`
  - 禁用 [TRAH](sec:essentialelements.scfconvergence.trahscf)
* - `SOSCF`
  - 启用 [SOSCF](sec:essentialelements.scfconvergence.soscf)
* - `NoSOSCF`
  - 禁用 [SOSCF](sec:essentialelements.scfconvergence.soscf)
* - `Damp`
  - 启用[阻尼](sec:essentialelements.scfconvergence.damping)
* - `NoDamp`
  - 禁用[阻尼](sec:essentialelements.scfconvergence.damping)
* - `LShift`
  - 启用[能级移动](sec:essentialelements.scfconvergence.levelshift)
* - `NoLShift`
  - 禁用[能级移动](sec:essentialelements.scfconvergence.levelshift)
* - {cspan}`1` *求解器参数选择（参见 {numref}`sec:essentialelements.scfconvergence.damping`）*
* - `EasyConv` 
  - 假定不存在收敛问题。
* - `NormalConv` 
  - 默认求解器参数
* - `SlowConv` 
  - 为困难情形选择合适的 SCF 求解器参数。
    大多数过渡金属配合物属于这一类。
* - `VerySlowConv` 
  - 为非常困难的情形选择合适的 SCF 求解器参数。
* - `SCFCONV<n>`
  - 根据 {numref}`compoundConvergenceThresholds` 和 {numref}`compoundAdditionalConvergenceThresholds` 将 `TolE` 调整为 10e-n 及大多数其他容差（不推荐！）
* - {cspan}`1` *[分数占据数](sec:essentialelements.scf.fracocc)*
* - `FracOcc` 
  - 启用分数占据（同时计算 [FOD](sec:spectroscopyproperties.fod)）
* - `Smear` 
  - 启用 `SmearTemp=5000` 的占据数抹平
    （同时计算 [FOD](sec:spectroscopyproperties.fod)）
* - `NoSmear` 
  - 禁用占据数抹平
* - `FOD`
  - 以默认设置执行 [FOD 分析](sec:spectroscopyproperties.fod)
    （TPSS/def2-TZVP、TightSCF、SmearTemp = 5000 K）
:::
:::{raw} latex
\endgroup
:::
