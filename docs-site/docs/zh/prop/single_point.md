---
title: 单点能
source: https://www.faccts.de/docs/orca/6.1/tutorials/prop/single_point.html
---

# 单点能

单点能（single point energy）是我们可以获取的最简单的性质，它对应薛定谔方程的最低能量解。不过，计算单点能有多种不同的方法，其精度水平也不尽相同：

## Hartree-Fock（HF）

这是最早发展起来的近似方法之一 [[Slater1951]](../bib.md#slater1951)，它不包含所谓的*动态*相关（dynamic correlation）甚至*静态*相关（static correlation）。要运行一个 HF 单点计算示例，只需在主输入文件中写入：

```mol
title: single_point #1
theme: chem311
height: 360px
representation: ball-stick
--- xyz ---
3
structure
O         -3.56626        1.77639        0.00000
H         -2.59626        1.77639        0.00000
H         -3.88959        1.36040       -0.81444
--- input ---
!HF DEF2-SVP
* xyz 0 1
O         -3.56626        1.77639        0.00000
H         -2.59626        1.77639        0.00000
H         -3.88959        1.36040       -0.81444
*
```

这样，基组（basis set）DEF2-SVP 将被指定给列表中的每一个原子。总能量会打印在文件末尾，例如：

```text
-------------------------   --------------------
FINAL SINGLE POINT ENERGY       -75.959334985643
-------------------------   --------------------
```

它是最古老也是最简单的方法之一，一般不推荐在需要可靠能量时使用。然而，它是 CCSD、CASSCF 等更完备方法的基础。

### 非限制性 HF（Unrestricted HF，UHF）

如果选择的多重度（multiplicity）不是 1，例如三重态（triplet）取 3，就会执行 UHF 计算。在这种情况下，务必检查结果的*自旋污染*（spin contamination）。

> **警告**
> 如果 $S^2$（写作 <S**2>）算符的期望值（expectation value）与理想值相差很大，那么你的体系可能只能用 CASSCF 这类多参考（multi-reference）计算来处理。

以上述水分子取三重态为例，可以得到：

```text
----------------------
UHF SPIN CONTAMINATION
----------------------

Expectation value of <S**2>     :     2.005700
Ideal value S*(S+1) for S=1.0   :     2.000000
Deviation                       :     0.005700
```

可以看到偏差极小，因此这里的结果是可以使用的。

### SCF 的加速（RIJDX 与 RIJCOSX）

求解 SCF 方程是计算能量的必要步骤，加速它的方法之一是使用 RI 选项来计算库仑积分（Coulomb integrals）[[Neese2003]](../bib.md#neese2003)。此时还需要辅助基组（auxiliary basis）。对于 DEF2 系列，默认设置为 DEF2/J：

```text
!HF DEF2-SVP DEF2/J RIJDX
```

如果所选基组没有对应的辅助基组，可以加入 `AUTOAUX` 标志来自动生成该辅助基组：

```text
!HF 6-31+G(d,p) AUTOAUX RIJDX
```

若要进一步加速，可以将 COSX 算法 [[Helmich-Paris2021]](../bib.md#helmich-paris2021) 与 RI 联用，高效地计算交换积分（exchange integrals）。

```text
!HF DEF2-SVP DEF2/J RIJCOSX
```

## 密度泛函理论（Density Functional Theory，DFT）

DFT 能量可以用类似方式获得，只需从可用的泛函（functional）中选择一个。例如：

```mol
title: single_point #7
theme: chem311
height: 360px
representation: ball-stick
--- xyz ---
3
structure
O         -3.56626        1.77639        0.00000
H         -2.59626        1.77639        0.00000
H         -3.88959        1.36040       -0.81444
--- input ---
!B3LYP DEF2-SVP
* xyz 0 1
O         -3.56626        1.77639        0.00000
H         -2.59626        1.77639        0.00000
H         -3.88959        1.36040       -0.81444
*
```

上述输入请求使用 B3LYP [[Becke1993]](../bib.md#becke1993)、[[Parr1988]](../bib.md#parr1988) 泛函进行计算。计算得到的能量为：

```text
-------------------------   --------------------
FINAL SINGLE POINT ENERGY       -76.320253532344
-------------------------   --------------------
```

关于检查自旋污染的论述同样适用于此。请始终牢记，DFT 结果可能随泛函不同而变化，因此在使用前应当加以考察，并且绝不要比较不同方法得到的能量！

ORCA 6 完全兼容 [LibXC](https://libxc.gitlab.io/) 中的泛函。完整的泛函列表及更多细节请查阅 [ORCA 手册](https://www.faccts.de/docs/orca/6.0/manual)。

> **注意**
> 由于标准 DFT 不涵盖相关效应（包括伦敦色散，London dispersion），通常建议施加[色散校正](../prop/disp.md)。

> **注意**
> 上述用于加速 SCF 的近似（RIJDX 与 RIJCOSX）同样可用于 DFT。当然，RIJCOSX 仅在使用杂化泛函（hybrid functional）时才有意义，因为杂化泛函中也会计算 HF 交换项。

> **重要**
> 对于非杂化泛函，默认采用 RIJDX 近似；对于杂化泛函，默认采用 RIJCOSX。要关闭这些近似，可以使用 `!NORI` 或 `!NOCOSX`。

## MP2 微扰理论

MP2 是一种后哈特里-福克（post-Hartree-Fock）方法，即以 HF 为基础，并设法补上 HF 所缺失的*动态*相关。ORCA 以非常高效的方式实现了它：既可以使用 RI 近似，也可以使用极其高效的对自然轨道变体（pair-natural variant，DLPNO）[[Neese2015]](../bib.md#neese2015)。两者分别用如下方式调用：

```text
!RI-MP2 cc-pVTZ cc-pVTZ/C
```

或

```text
!DLPNO-MP2 cc-pVTZ cc-pVTZ/C
```

由于它属于所谓的**相关**（correlated）方法，RI 部分需要专门的 "/C" 基组。并非所有基组都提供这类辅助基组，但可以通过 `AUTOAUX` 获得：

```mol
title: single_point #11
theme: chem311
height: 360px
representation: ball-stick
--- xyz ---
3
structure
O         -3.56626        1.77639        0.00000
H         -2.59626        1.77639        0.00000
H         -3.88959        1.36040       -0.81444
--- input ---
!DLPNO-MP2 6-311++G(2d,2p) AUTOAUX
*XYZ 0 1
O         -3.56626        1.77639        0.00000
H         -2.59626        1.77639        0.00000
H         -3.88959        1.36040       -0.81444
*
```

可以按如下方式查看相关能（correlation energy）贡献：

```text
------------------------------------------------------
 DLPNO-MP2 CORRELATION ENERGY:      -0.240752222110 Eh
------------------------------------------------------
```

最终能量则照常打印出来。

> **警告**
> 相关方法通常比 DFT 更依赖基组大小。请选择足够大的基组以避免较大误差。

### 自旋分量标度 MP2（Spin-Component-Scaled MP2，SCS-MP2）

引入自旋分量标度（spin-component-scaling）可以大幅提高 MP2 的精度。异自旋分量的标度参数 `PS` 与同自旋分量的标度参数 `PT` 可通过 `%mp2` 块进行调节：

```text
!RI-SCS-MP2 cc-pVTZ cc-pVTZ/C

%mp2
  DOSCS       true
  PS          1.2    
  PT          0.333
end

*XYZFILE 0 1 structure.xyz
```

如果只使用 `RI-SCS-MP2` 关键词，则采用默认值 `PS=1.2` 和 `PT=0.333`。

### 轨道优化 MP2（Orbital-Optimized MP2，OO-MP2）

使 Hylleraas 泛函对轨道旋转取驻值，便得到 ORCA 中实现的轨道优化 MP2 方法。其 RI 加速版本可通过以下方式调用：

```text
!OO-RI-MP2 cc-pVTZ cc-pVTZ/C

*XYZFILE 0 1 structure.xyz
```

> **警告**
> 请注意，OO-RI-MP2 方法的每一次迭代都与一次 RI-MP2 弛豫密度计算一样昂贵！

### 正则化 MP2（Regularized MP2）

Shee、Head-Gordon 等人提出的正则化方法 [[Shee2021]](../bib.md#shee2021) 引入了一个单参数、依赖于能隙的正则化项，用于阻尼被高估的成对加和贡献，从而对一阶振幅（amplitudes）进行重整化，以经验方式模拟更高阶的相关效应。ORCA 中提供三种正则化函数：$\kappa$、$\sigma$ 和 ${\sigma}^2$。最常用的正则化函数是 $\kappa$，可通过 `%mp2` 块控制：

```text
!RI-MP2 cc-pVTZ cc-pVTZ/C

%mp2
    DoRegMP2     true   # activates MP2 regularization
    RegMP2Type   0      # 0 = kappa regularizer
    RegMP2Kappa  1.1    # kappa parameter
end

*XYZFILE 0 1 structure.xyz
```

> **注意**
> 正则化 MP2 尚不提供梯度。

## 双杂化 DFT（Double-Hybrid DFT，DH-DFT）

用 MP2 等方法替换密度泛函中的部分相关分量，可以在多种性质上获得更好的结果。这类方法称为双杂化泛函（double-hybrid functional）[[Grimme2006]](../bib.md#grimme2006)，因为它们同时包含 HF 交换和 MP2 相关。许多预定义的双杂化泛函可以像常规泛函一样通过简单关键词调用。B2PLYP 泛函的示例输入如下：

```text
!B2PLYP DEF2-QZVPP

*XYZFILE 0 1 structure.xyz
```

双杂化方法同样可以受益于 RI 近似

```text
!RI-B2PLYP DEF2-QZVPP DEF2-QZVPP/C

*XYZFILE 0 1 structure.xyz
```

甚至可以使用 DLPNO 方案来加速 MP2 计算。

```text
!DLPNO-B2PLYP DEF2-QZVPP DEF2-QZVPP/C

*XYZFILE 0 1 structure.xyz
```

一个进一步利用 SCS-MP2 的著名双杂化泛函是 revDSD-PBEP86-D4。这个经验泛函在拟合中还纳入了 D4 色散校正，通常在热化学（thermochemistry）方面给出非常好的结果。

```text
!revDSD-PBEP86-D4/2021 DEF2-QZVPP DEF2-QZVPP/C

*XYZFILE 0 1 structure.xyz
```

> **注意**
> 请注意，与常规 DFT 泛函相比，双杂化泛函通常也需要更大的基组。双杂化泛函还可以与 D4 等色散校正结合使用。
> 像 revDSD-PBEP86-D4 这样的泛函是在 D4 校正下拟合的，绝不能在不加 D4 校正的情况下使用！

## 耦合簇（Coupled Cluster，CC）

耦合簇计算，尤其是 CCSD(T) 变体，是单点能的金标准（gold standard）。然而在其常规表述下，它们的计算代价也极其高昂。

ORCA 提供了一种 DLPNO 变体，其效率**高得多**，并且对大体系几乎呈线性标度增长 [[Neese2016]](../bib.md#neese2016)，[[Neese2013a]](../bib.md#neese2013a)，[[Neese2013b]](../bib.md#neese2013b)。要使用它，只需在输入中设置 DLPNO-CCSD(T) 并选择合适的基组（同样需要 "/C" 基组或 AUTOAUX）

```mol
title: single_point #20
theme: chem311
height: 360px
representation: ball-stick
--- xyz ---
3
structure
O         -3.56626        1.77639        0.00000
H         -2.59626        1.77639        0.00000
H         -3.88959        1.36040       -0.81444
--- input ---
!DLPNO-CCSD(T) cc-pVTZ cc-pVTZ/C
*XYZ 0 1
O         -3.56626        1.77639        0.00000
H         -2.59626        1.77639        0.00000
H         -3.88959        1.36040       -0.81444
*
```

CC 结果打印如下：

```text
----------------------
COUPLED CLUSTER ENERGY
---------------------- 
 
E(0)                                       ...    -76.055469392
E(CORR)(strong-pairs)                      ...     -0.267934875
E(CORR)(weak-pairs)                        ...     -0.000104142
E(CORR)(corrected)                         ...     -0.268039017
E(TOT)                                     ...    -76.323508409
Singles Norm <S|S>**1/2                    ...      0.018659847
T1 diagnostic                              ...      0.006597252
```

最终的单点能在末尾给出：

```text
-------------------------   --------------------
FINAL SINGLE POINT ENERGY       -76.330949256808
-------------------------   --------------------
```

请务必检查打印出的 T1 诊断（T1 diagnostic）值。经验规则是：若诊断值大于 0.02，则结果不可信，HF 参考波函数可能质量较差。

ORCA 中可以使用许多不同的耦合簇和耦合对方法，详情请查阅 [ORCA 手册](https://www.faccts.de/docs/orca/6.0/manual)。

> **注意**
> RIJCOSX 算法可用于显著加速 MP2 和 CC 计算！

## 半经验方法（Semiempirical Methods，SQM）

ORCA 中提供了多种半经验（semiempirical）方法。这些方法速度快，但在精度和稳健性上不及更复杂的 DFT 或波函数理论（WFT）方法。尽管如此，它们非常适用于高通量筛选（high-throughput screening），或处理含数百到数千个原子的超大体系。一个著名的例子是 Grimme 的 GFN2-xTB 扩展紧束缚（extended tight-binding）方法 [[Grimme2019]](../bib.md#grimme2019)。它可以很方便地调用：

```mol
title: single_point #23
theme: chem311
height: 360px
representation: ball-stick
--- xyz ---
3
structure
O         -3.56626        1.77639        0.00000
H         -2.59626        1.77639        0.00000
H         -3.88959        1.36040       -0.81444
--- input ---
!XTB2

*XYZ 0 1
O         -3.56626        1.77639        0.00000
H         -2.59626        1.77639        0.00000
H         -3.88959        1.36040       -0.81444
*
```

> **警告**
> 目前 xtb 方法是通过与 xtb 独立程序的接口调用的。因此，请务必使用 xtb 6.4.0 或更高版本以确保完全兼容！
