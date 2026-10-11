<a id="sec:modelchemistries.hftype"></a>
# 波函数类型（Wavefunction Types）：RHF/RKS、UHF/UKS、ROKS 等

控制所计算波函数（wavefunction）类型的基本变量是 `%scf` 块中的变量 `HFTyp`。如果未指定 `HFTyp`，程序将检查输入中给出的多重度（multiplicity）：对于多重度为 1 的闭壳层（closed-shell）分子，假定为 RHF/RKS；对于多重度大于 1 的开壳层（open-shell）分子，则调用 UHF/UKS。`RHF` 将进行自旋限制（spin restricted）的闭壳层类型计算[szabo1989modern](../../bibliography.md)，而 UHF 则进行自旋非限制（spin unrestricted）计算。

对于 DFT 计算，`RKS`、`UKS` 和 `ROKS` 可分别作为 `RHF`、`UHF` 和 `ROHF` 的同义词使用。限制性开壳层 DFT 方法（`ROKS`）仅对具有$n$ 个未配对电子且$S=n/2$ 的高自旋（high-spin）态有效。`UKS` 波函数不会进行自旋纯化（spin-purified）。

```orca
%scf
  HFTyp  RHF     # closed-shell (RKS for DFT)
         UHF     # unrestricted open-shell (UKS for DFT)
         ROHF    # restricted open-shell (ROKS for DFT)
         CASSCF  # complete active space SCF
end
```

在某些情况下，您可能希望对开壳层体系使用 RHF/RKS 来获得"半电子"（half-electron）类型的波函数[dewar1968am](../../bibliography.md)。总能量并未加以校正！有时这类半电子计算可以达到可接受的收敛，所得轨道可用作 ROHF、UHF 或 MRCI 计算的输入。对于过渡金属配合物需特别注意，因为 RHF/RKS 轨道与 ROHF 或 UHF 轨道差别很大，因此不建议过度解读此类计算所得波函数的含义。计算按如下方式设置：

```orca
%method AllowRHF true end
# or simply: ! AllowRHF
```

<a id="sec:modelchemistries.hftype.rohf"></a>
## ROHF 选项（ROHF Options）

对于 ROHF 计算[mcweeny1974mol,brobowicz1977methods,carbo1978general,binkley1974mol,edwards1987theor,muller1994chem,kollmar1996chem,kollmar1997int,bofill1998comp](../../bibliography.md)，程序会根据初始猜测轨道（initial guess orbitals）及其能量来推断存在何种类型的开壳层情形。大多数"简单"情形都能被正确识别，但有时需要用户稍加辅助。

最简单的 ROHF 情形是 `HIGHSPIN`（高自旋）情形，其中开壳层中所有未配对电子均为铁磁耦合（ferromagnetically coupled，即彼此平行），从而得到尽可能高的多重度。用户可按如下方式请求该情形：

```orca
%scf
  HFTyp       ROHF
  ROHF_case   HIGHSPIN
  ROHF_NEl[1] 4          # number of electrons in the open-shell
end
```

ROHF 代码还具备一项非常强大的功能，其思想源于 Mike Zerner 的洞见[stavrev1997int,zerner1989int](../../bibliography.md)。它可以对给定组态（configuration）的*所有*态进行平均（`CAHF`），或对给定组态中*给定自旋的所有态*进行平均（`SAHF`）。尤其是 `SAHF` 功能，能让您轻松处理大多数简并（degenerate）的高对称性情形，此类计算所得轨道用作 CI 计算的输入将非常方便。

```orca
%scf
  HFTyp         ROHF
  ROHF_case     CAHF    # configuration averaged HF
                SAHF    # spin averaged HF
  ROHF_NumOp    3       # number of operators (3, 2 or 1)
  ROHF_NOrb[1]  2,1     # number of orbitals in each open-shell
  ROHF_NEl[1]   1,1     # number of electrons in each open-shell
end
```

下面这个假设性的例子可以代表一个八面体 d$^{3}$ 过渡金属配合物的激发态（excited state）。在这种情况下有五个开壳层轨道：前三个开壳层轨道各含两个电子，最后两个各含一个电子。SAHF 计算的输入是相同的，只需将 CAHF 替换为 SAHF 即可。

```orca
%scf
  HFTyp         ROHF
  ROHF_case     CAHF   # configuration averaged HF
  ROHF_NumOp    3      # 3 operators in this case: closed, open1, open2
  ROHF_NOrb[1]  3,2    # 3 orbitals in first open shell, 2 in the second
  ROHF_NEl[1]   2,1    # 2 electrons in first open shell, 1 in the second
end
```

ROHF 代码的另一项功能是能够将 SCF 收敛到给定的组态状态函数（Configuration State Function, `CSF-ROHF`）[gouveia2024JPCA](../../bibliography.md)。通过这种方式可以逼近 MCSCF 计算的结果。可以通过两种方式来请求该功能。

用户可以给出具体的耦合情形（coupling situation）：
```orca
%scf
  HFTyp      ROHF
  ROHF_CASE  USER_CSF          # User defined CSF
  ROHF_REF   {1 1 -1 -1} end   # CSF to be converged to a 2 open shell antiferromagnetically coupled
end
```

或者用户可以给出每个壳层的轨道数，其中每个开壳层都会与前一个开壳层以反平行自旋相耦合。
```orca
%scf
  HFTyp       ROHF
  ROHF_CASE   AF_CSF          # User defined CSF
  ROHF_AFORBS 2,2             # Coupling Situation
end
```

例如，可以设想一个 Fe(III) 二聚体，其中每个中心局部都是高自旋的，但彼此之间反铁磁耦合（antiferromagnetically coupled）。为了获得该体系的 ROHF 解，首先需要一组初始猜测轨道。猜测轨道可以通过以下任一方式获得：UHF 计算的 QRO（准限制轨道）、高自旋 ROHF 计算，甚至 SAHF 或 CAHF。无论采用何种方法，轨道都需要进行定域化并排序，使每个铁原子的 3d 轨道集合按顺序分组在一起。在此基础上，就可以针对反铁磁 CSF 运行 CSF-ROHF 计算，如下所示：

```orca
%scf
  HFTyp      ROHF
  ROHF_CASE  USER_CSF                         # User defined CSF
  ROHF_REF   {1 1 1 1 1 -1 -1 -1 -1 -1} end   # 2 open shells coupling antiparallel
end

or

%scf
  HFTyp       ROHF
  ROHF_CASE   AF_CSF                          # User defined CSF
  ROHF_AFORBS 5,5                             # 2 open shells coupling antiparallel
end
```

当调用 `USER_CSF` 情形时，CSF-ROHF 流程能够在 CSF 的定义中识别出双占据轨道（doubly occupied orbitals）和虚轨道（virtual orbitals）。一旦检测到这些轨道，它们就会被旋转出 ROHF 方法中所定义的开壳层，计算将正常进行：

```orca
%scf
  HFTyp      ROHF
  ROHF_CASE  USER_CSF                   # User defined CSF
  ROHF_REF   {1 1 2 1  -1 -1 0 -1} end  # the DOMO will be rotated to
                                        # the closed-shell and the VMO
					# will be rotated to the virtual space. 
end
```

用户也可以通过 `ROHFOPT Case User` 关键词直接输入 ROHF 变量。例如，对于三个轨道中有三个电子的高自旋情形，它给出两个算符，其矢量耦合系数（vector coupling coefficients）为$a=1$ 和$b=2$（Zerner 约定）。

```orca
%scf
  HFTyp      ROHF
  ROHFOP  Case    User  # manual input of ROHF variables
    Nop     2           # number of operators
    Norb[1] 3           # number of open-shell orbitals
    Nel[1]  3           # number of open-shell electrons
    A[1,1]  1           # Coulomb vector in the open shell
    B[1,1]  2           # Exchange vector in the open shell
  end
end
```

ROHF 理论中一个不太方便的特性是 Fock 算符（Fock operator）的定义带有一定的任意性。不同的选择会给出相同的波函数，但具有不同的收敛性质，而且这些性质会因体系而异。因此 ORCA 允许用户选择所需的变体。尝试这些不同的选择，可能会把一个发散或收敛缓慢的 ROHF 计算变成一次成功的计算！

`ROHF_Restrict` 功能是另一项可能有用的功能。如果您怀疑 ROHF 计算不收敛是因为开壳层轨道与闭壳层轨道之间来回翻转（flipping），可以尝试选择 `ROHF_Restrict true` 来避免这种行为。当然，不能保证它一定有效，也不能保证体系保持在所需的状态。不过，它可以降低出现大幅度、不受控步长的几率。

```orca
%scf
  ROHF_Mode 0   # construct F according to Pulay (default)
            1   # construct F as in the Gamess program
            2   # construct F according to Kollmar

  ROHF_Restrict false # restrict orbital interchanges and off-diagonal elements
                      # (default=false)
                      
  # a complete list of ROHF variables
  ROHFOP 
    Case      User   # manual input of ROHF variables
    Nop       2      # number of operators
    Norb[1]   3      # number of open-shell orbitals
    Nel[1]    3      # number of open-shell electrons
    A[1,1]    1      # Coulomb vector in the open shell
    B[1,1]    2      # Exchange vector in the open shell
    Mode      2      # use the Kollmar operator
    Restrict  false  # do not restrict
  end
end
```

<a id="sec:modelchemistries.hftype.uhfno"></a>
## UHF 自然轨道（UHF Natural Orbitals）

程序可以生成 UHF 自然轨道（UHF natural orbitals, UNO）。借助这些轨道，可以很方便地对开壳层波函数进行直观描绘。语法很简单：

```orca
%scf
  UHFNO true
end
# or simply: ! UNO
```

关于 UNO 有多种输出选项，详见输出章节 [spectroscopyproperties.pop](../spectroscopyproperties/population.md#sec:spectroscopyproperties.pop)。UNO 也可以按绘图章节 [utilities.plots](../utilitiesvisualization/plots.md#sec:utilities.plots) 中所述进行绘制。一般来说，程序会存储一个 `BaseName.uno` 文件，其中 `BaseName` 默认是您的输入文件名去掉 `.inp` 后缀后的名称。相应地，gbw 文件命名为 `BaseName.gbw`。`.uno` 文件是一个普通的 gbw 文件，其中包含几何结构、基组和 UNO 轨道。例如，它可用于启动 ROHF 计算。

<a id="sec:modelchemistries.hftype.unoucoqro"></a>
## UNO、UCO 与 QRO 的输入

对于开壳层体系的计算，我们建议在输入行中使用关键词 `!UNO` `!UCO`。这将生成准限制分子轨道（quasi-restricted molecular orbitals）`QRO`、非限制性自然自旋轨道（unrestricted natural spin-orbitals）`UNSO`、非限制性自然轨道（unrestricted natural orbitals）`UNO` 以及非限制性对应轨道（unrestricted corresponding orbitals）`UCO`。此外，它还会在输出中打印 UCO 重叠（UCO overlaps），这些信息可以非常清晰地反映体系中的自旋耦合（spin-coupling）情况。下面给出一个输入示例以及输出片段。

```orca
!B3LYP def2-SVP UNO UCO TightSCF
```

输出中的 UCO 重叠部分如下所示：

```orca
***UHF Corresponding Orbitals were saved in MyJob.uco***

----------------------
Orbital    Overlap(*)
----------------------
.
.
.
96:       0.99968
97:       0.99955
98:       0.99947
99:       0.99910
100:      0.99873
101:      0.99563
102:      0.74329
103:      0.00000
```

对应数值通常小于 0.85 的重叠表示一对自旋耦合的电子对。而接近 1.00 和 0.00 的值则分别对应双占据轨道（doubly occupied orbitals）和单占据轨道（singly occupied orbitals）。
