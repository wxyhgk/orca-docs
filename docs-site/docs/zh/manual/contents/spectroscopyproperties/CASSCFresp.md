

<a id="sec:spectroscopyproperties.casscfresp"></a>
# CASSCF 线性响应（CASSCF Linear Response）

## 引言（Introduction）
与 SCF 线性响应类似（参见 [essentialelements.cpscf](#sec:essentialelements.cpscf)），
可通过求解耦合微扰（CP-）CASSCF 方程来计算 CASSCF 水平的二阶导数性质，
即波函数参数对微扰的线性响应。
这些线性响应方程表示为

$$
\frac{\partial^2 E}{\partial\lambda^2} \frac{\partial\lambda}{\partial\mathbf R} = -\frac{\partial^2 E}{\partial\lambda \partial\mathbf R}
$$

其中 $\lambda$ 是 CASSCF 波函数参数，
$\mathbf R$ 是所求解响应方程对应的微扰 [Helgaker1986, vahtras1997](../../bibliography.md)。
右端（RHS）的性质梯度是已知的、依赖于微扰的量，
但左端（LHS）依赖于波函数参数对 $\mathbf R$ 的响应解。
因此，对微扰的响应必须迭代求解，这通过试探矢量 $\mathbf X$ 完成。
这使得 LHS 被计算为一个 sigma 矢量，并在每次迭代中重新组装。
于是，微扰 $R_i$ 的线性响应方程可写为

$$
\sigma = \mathbf H \mathbf X^{(R_i)} = -\mathbf G^{(R_i)}
$$

其中 $\mathbf H$ 是与微扰无关的 Hessian 矩阵，
$\mathbf G$ 是特定于微扰的 RHS 矩阵。
一旦线性方程收敛，响应参数的解矢量便可与电子密度矩阵和自旋密度矩阵收缩，
得到 AO 响应密度矩阵 $\left[\mathbf P^{\alpha \pm \beta}\right]^{(\mathbf R)}$。
随后，响应密度与相应的 AO 单电子性质积分收缩，
即可计算二阶导数性质的二阶贡献。

在 ORCA 中，这些方程由 `orca_casscfresp` 程序求解，
其底层求解器是 `BHP22`（一种 Davidson 型线性方程求解器）。
RHS 由 `orca_propint` 程序计算的性质积分构建。
在解收敛并生成、存储响应密度之后，会调用 `orca_prop` 程序，
在其中将适当的密度和响应密度与所需的性质积分（同样来自 `orca_propint`）收缩。
这种对密度的使用使得 `orca_prop` 中的响应性质计算
对所有方法普遍适用，因为方法特有的信息都包含在密度之中。

## 技术说明（Technical Notes）
需要注意的是，CASSCF 线性响应以优化后的 CASSCF 波函数为起点。
因此，输入中必须提供含适当参数的 `%casscf` 块
（参见 [CASSCF](#sec:modelchemistries.casscf)）。
态特定（SS-）CASSCF 响应在 SS（`NRoots 1`）CASSCF 波函数上运行。
若 CASSCF 波函数是态平均（SA）的，
则响应在整个平均态流形上运行，而非针对某个特定根。
此时应仔细分析输出。
一个明智的做法是只对（近）简并的态求平均。

默认情况下，会先从头运行一次 CASSCF 计算，然后再运行 CASSCF 响应。
另外，也可用 `!MOREAD NoIter` 并通过 `%moinp` 提供相应的 `.gbw` 文件，
以使用先前收敛的 CASSCF 计算的轨道。
此时，请确保 `%casscf` 块中的输入与先前收敛计算中同一输入块的参数一致，
并务必仔细检查轨道！

线性响应方程迭代求解，直到达到残差范数的收敛阈值（`TolR`）。
该值可由用户设置，但 ORCA 默认会将其设为最严格的合理收敛判据，
同时考虑底层 CASSCF 计算的轨道梯度和 CI 梯度容差。
这应当是最合理的设置；若试图收紧该阈值，请务必小心！

必须在 `%elprop` 和 `%eprnmr` 块中设置适当的性质标志，
才能计算所需的性质（参见 [spectroscopyproperties.elprop](#sec:spectroscopyproperties.elprop) 和
[properties.eprnmr](#sec:spectroscopyproperties.properties.eprnmr)）。
虽然所有一阶导数性质都可与 CASSCF 配合使用，
但目前并非所有二阶导数性质都可用于 CASSCF。
当前可用的静态性质（按响应所取的微扰排序）包括：
* 电（$\mathbf E$）场
    * 偶极/偶极极化率
    * 偶极/四极极化率
* 四极（$\mathbf Q$）场
    * 四极/四极极化率
* 速度（$\mathbf v$）
    * 速度极化率
* 磁（$\mathbf B$）场（**不含** GIAO）
    * EPR g 张量
    * NMR 化学位移屏蔽
* 核磁矩（$I^{(A)}$）
    * EPR A 矩阵（Aorb 贡献） 

磁性质目前的实现不含规范包含原子轨道
（gauge-including atomic orbitals，GIAO）。
因此，必须在 `%eprnmr` 块中提供合适的规范原点（gauge-origin）！
对于 EPR g 张量，建议使用大基组并选取化学上合理的规范原点。
不过，一般而言，对不含 GIAO 的 NMR 化学位移屏蔽应保持警惕。

## 基本用法（Basic Usage）
以下是用进行性质计算所需各块的概览：

```orca
! def2-TZVP AutoAux    # (or other appropriate basis & auxiliary)

%casscf
  ...
end

%casresp     # only required to change solver, printing, or preconditioner options
  ...
end

%elprop      # only required if electric property requested
  ...
end

%eprnmr      # only required if magnetic property requested
  ...
  ORI ...
end

* xyzfile ...
```

## 故障排查（Troubleshooting）
若指定了 `%casresp` 块，但计算没有运行到 CASSCF 响应部分，
则说明所请求的性质不是二阶导数，因此无需求解线性响应方程。
然而，若作业中止，请注意以下可能性：
* 所请求的二阶导数性质中至少有一个在 CASSCF 水平不可用（见上文当前已实现的列表）
* 可能需要增大 `MaxIter` 或放宽 `TolR`
* 若某个或某些微扰先满足收敛判据、后来又不满足，可尝试关闭解锁定（solution locking）。
    * 这可能表明 `TolR` 过严
* 请求了磁场性质，却未在 `%eprnmr` 块中设置规范原点
* 可能需要合适的辅助基组（或 `!AutoAux` 关键词），尤其对于：
    * 试探矢量预条件子（trial vector preconditioner，默认开启）
    * `%casscf` 块中的 `TrafoStep RI`
    * RIJCOSX、RIJONX
* 指定了 RIJK（此**不**受支持）

请注意，`%elprop` 和 `%eprnmr` 块中与求解器相关的选项
不影响 CP-CASSCF 方程的求解。

## 关于输出打印的说明（Notes on Printing）
有关所计算性质积分类型的信息可在输出文件的
`ORCA PROPERTY INTEGRAL CALCULATIONS` 部分找到。
`orca_casscfresp` 的输出以标题 `ORCA CASSCF RESPONSE CALCULATION` 开始。
在有关微扰类型和数量的信息之后，
计算按微扰的主要类型分为实微扰和虚微扰两部分。
同一类型的所有响应方程可同时求解。

这两类在输出文件中各有自己的部分。
这些部分以轨道范围和 CI 空间的信息开始，然后进入方程的迭代求解。
这里的打印给出迭代编号、每个响应方程的残差范数
以及该响应方程是否满足收敛判据的概览。
下面是这类输出的示例（为简洁起见，省略了第 3--7 次迭代）：

```orca
 ------------------------------------------------------------------------------

                      SOLVER Davidson-type linear equation solver 

   Iter.                  ||Error||_2   Conv.                (TolR = 1.000e-08)
 ------------------------------------------------------------------------------
    0  (rhs    0)        1.645417e-01     No
       (rhs    1)        1.826041e-01     No
       (rhs    2)        2.047543e-01     No
    1  (rhs    0)        7.069575e-02     No
       (rhs    1)        3.363295e-02     No
       (rhs    2)        7.229274e-02     No
    2  (rhs    0)        9.183136e-03     No
       (rhs    1)        3.922435e-03     No
       (rhs    2)        7.152764e-03     No
(...)
 ------------------------------------------------------------------------------

     All 3 Linear Equations CONVERGED Below 1.000e-08

 ------------------------------------------------------------------------------
    8  (rhs    0)        4.070240e-09    Yes
       (rhs    1)        1.186846e-09    Yes
       (rhs    2)        4.407666e-09    Yes
```

在进入必要的性质模块之前，
若请求了 RHS 和/或响应矢量的重要贡献（通过 `PrintRHSVec` 和 `PrintRspVec`），
则会将其输出。这里可以看到如下输出。

```orca
  ---------------------------------
   CASSCF Response Vector Analysis
  ---------------------------------
 square of coefficients of particle-hole and CAS-CI excitations are printed
 if larger than 1.0e-02

IPERT: 0

   (-) I   9 (   9) -> V   0 (  17) :      0.07167 (c= -0.26772137)
(...)
   (-) A   1 (  14) -> V  13 (  30) :      0.07323 (c=  0.27061481)
(...)
   (-) I   4 (   4) -> A   0 (  13) :      0.02915 (c=  0.17074032)
(...)
   (-) CI                                  1.65592 [     7]: 1201
(...)
```

为简洁起见，大部分输出已省略。
这里，若矢量元素的平方大于 `1.0e-02`（`TolPrintVec` 的默认值），
则打印响应矢量的重要贡献。
每行以 `(+)` 或 `(-)` 开头，表示激发算符的厄米性（Hermiticity）。
在静态 CASSCF 线性响应中，`(+)` 总是表示虚微扰，`(-)` 表示实微扰。
对于第一个矢量（即 `IPERT: 0`），这里列出了四个贡献。

前三个来自粒子-空穴激发，方向从箭头左侧到右侧。
箭头两侧各有三项：一个字母，标明是惰性（`I`）、活性（`A`）还是虚（`V`）轨道；
一个数字，标明该轨道子块内的索引；
以及括号中的一个数字，标明总的轨道编号。
更右侧给出的是系数（即矢量元素），其左侧给出该值的平方。
由此可以分析每个激发的相对贡献。

最后展示的贡献来自 CI 激发。
先列出其权重，然后是方括号中的索引，
以及活性电子在活性轨道中的相应组态。

<a id="sec:spectroscopyproperties.casscfresp.keywords"></a>
## 关键词（Keywords）
!!! note "`%casresp` 块输入关键词。"
    | 关键词                       | 选项                  | 说明                                                         |
    |:-------------------------------|:----------------------|:--------------------------------------------------------------------|
    | `TolR`                         | `<real>`              | 收敛阈值（LR 方程的残差范数）                                     |
    |                                |                       | *（默认）使用最严格的合理阈值*                                    |
    | `MaxIter`                      | `64`                  | 最大迭代次数                                                      |
    | `MaxRed`                       | `100`                 | 每个 RHS 约化空间的最大尺寸                                       |
    | `PrintRHSVec`                  | `false`               | 打印 RHS 矢量的重要贡献                                           |
    | `PrintRspVec`                  | `false`               | 打印响应矢量的重要贡献                                            |
    | `PrintWF`                      | `CFG`                 | *（默认）* 以组态基打印 RHS/响应矢量的 CI 部分                     |
    |                                | `CSF`                 | 以 CSF 基打印 RHS/响应矢量的 CI 部分                              |
    |                                | `DET`                 | 以行列式基打印 RHS/响应矢量的 CI 部分                             |
    | `TolPrintVec`                  | `1.e-2`               | 打印 RHS/响应矢量某项贡献的阈值                                   |
    | `PreCondType`                  | `full`                | *（默认）* 试探矢量的完整预条件子（需要辅助基组）                  |
    |                                | `diag`                | 试探矢量的对角预条件子（需要辅助基组）                            |
    |                                | `none`                | 试探矢量不作预条件                                                | 
    | `PreCondMaxRed`                | `400`                 | Hessian 预条件子集大小                                            |
    | `DoOrbResp`                    | `true`                | 包含轨道响应                                                      |
    | `DoLocking`                    | `true`                | 当微扰满足收敛判据时锁定其解                                      |
    | `DoOlsen`                      | `false`               | 使用 Olsen 预条件子                                              |

