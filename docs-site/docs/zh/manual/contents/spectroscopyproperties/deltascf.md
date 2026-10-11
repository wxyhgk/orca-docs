

<a id="sec:spectroscopyproperties.deltascf"></a>
# DeltaSCF

`DeltaSCF` 是含时 DFT 的一种不含时替代方法，用于在平均场 DFT 框架内描述激发电子态，
已有研究表明，对于乙烯分子（光化学的典型范例）中避免交叉和圆锥交叉的拓扑结构，
它比常用线性响应绝热近似下的 TDDFT 给出更好的结果[Schmerwitz2022](../../bibliography.md)；
对于电荷转移激发态也是如此——TDDFT 的绝对误差随电荷转移距离迅速增大，
而 `DeltaSCF` 可给出均衡的描述[Selenius2024](../../bibliography.md)。

通常，SCF 过程用于获得基电子态，即能量面关于电子轨道旋转自由度上的一个极小值。
$\Delta$SCF 的思想是收敛到电子能量面上一个更高能量的解（通常是一个鞍点），
以找到激发电子态的平均场表示。由于仅仅形成一个接近该激发态解的初始猜测
并使用常规 SCF 方法通常是不够的，人们在 ORCA 中开发并实现了多种策略，
使 SCF 收敛到目标鞍点并防止所谓的变分坍缩（variational collapse）——
即收敛到不需要的低能量解。

Peter Gill 课题组[gilbert_self-consistent_2008](../../bibliography.md) 引入了一种简单但往往有效的方法，
即最大重叠法（Maximum Overlap Method，MOM）。在 ORCA 中，我们还提供了
Hrant Hratchian 课题组较新的 PMOM[corzo_using_2022](../../bibliography.md)。此外，ORCA
还提供了一种 SOSCF 优化技术，它利用有限内存对称秩 1 拟牛顿方法，
以及广义模式追踪（generalized mode following）方法，两者都能系统地
收敛到鞍点解。激发态初始猜测可以通过 freeze-and-release SOSCF 策略中的
约束优化来细化。$\Delta$SCF 也被称为
"用于电子激发态的轨道优化 DFT"（orbital optimized DFT for electronic excited states）[Hait2021](../../bibliography.md)
和"激发态平均场理论"（excited state mean-field theory）[Hardikar2020](../../bibliography.md)。

图 [fig:deltascf_basics](#fig:deltascf_basics) 展示了 $\Delta$SCF 中一般 HOMO-LUMO
激发的示意图。首先，通过常规 SCF 计算获得基态。然后，
将占据数改变为反映目标激发的非 aufbau 占据。
对于 HOMO-LUMO 激发，选择两个自旋通道之一的 HOMO 使其空出，
而 LUMO 被占据。这种非 aufbau 占据连同基态轨道一起
作为变分鞍点搜索的初始猜测，从而得到 $\Delta$SCF 激发态解。

<a id="fig:deltascf_basics"></a>
!!! note "../../images/deltascf_basics.*"
    使用 $\Delta$SCF 的 HOMO-LUMO 激发态的简单示意图

使用 ORCA 的 `DeltaSCF`，我们可以**选择**将 SCF 收敛到 HOMO/LUMO 激发态。
激发态通过完全弛豫轨道获得，可以包含任何贡献，例如
VV10 相关或 CPCM 溶剂化。由于波函数的变分优化，
Hellman-Feynman 定理成立，这意味着可以得到原子核位置上的梯度，
从而可用于几何优化、分子动力学模拟、反应路径计算
以及 ORCA 提供的所有其他几何搜索功能。此外，ORCA 用基态
SCF 密度计算的所有性质也都可以用激发态 $\Delta$SCF 密度计算。

!!! warning
      $\Delta$SCF 态由 DFT 框架内的单行列式波函数表示。
      正如基态 DFT 在多行列式情形下会遇到困难一样，激发态 DFT 也是如此。
      处理这类情形时请牢记这一点！

      例如，这种描述在以下情况下相对合理：
      1. 激发态可以用粒子-空穴相互作用描述。例如，苯分子的 HOMO-LUMO 激发
      或大多数 $\pi$-$\pi^{*}$ 激发态**不属于**这种情况，
      2. 占据轨道和虚拟轨道在空间上分离，使得相关交换积分为零。
      例子包括某些 $n$-$\pi^{*}$ 态、长程电荷转移态等，
      3. 对于可用单行列式波函数表示的闭壳层双激发态。

      此外，$\Delta$SCF 波函数可能破坏哈密顿量的对称性（这对基态和
      激发态都成立）。开壳层单重激发态本身就破坏自旋对称性，
      需要自旋纯化[Ziegler1977](../../bibliography.md)。

<a id="sec:spectroscopyproperties.deltascf.theory"></a>
## 理论（Theory）

本节讨论 $\Delta$SCF 方法背后的理论。

<a id="sec:spectroscopyproperties.deltascf.theory.lsr1"></a>
### SOSCF L-SR1 方法（SOSCF L-SR1 method）

在 $\Delta$SCF 中，人们寻找能量面关于电子轨道旋转自由度的驻点，
这些自由度收集在轨道旋转矩阵中

$$
\kappa = \begin{pmatrix}\kappa_{\mathrm{oo}} = 0 &
\kappa_{\mathrm{ov}}\\ -\kappa_{\mathrm{ov}}^{+} &
\kappa_{\mathrm{vv}} = 0\end{pmatrix}\,,
$$

其中 oo、ov 和 vv 分别表示 $\kappa$ 中包含混合两个占据轨道、
一个占据与一个虚拟轨道、以及两个虚拟轨道的成对轨道旋转的块。
驻点由下式求得

$$
C_{\mathrm{stat}} = C_{0}e^{\kappa}\,,
$$

能量梯度为

$$
\frac{\partial E}{\partial \kappa_{ij}} = \frac{2 - \delta_{ij}}{2}\left[\in t_{0}^{1}dte^{t\kappa}Le^{-t\kappa}\right]_{ji} = \frac{2 - \delta_{ij}}{2}\left[L + \frac{1}{2!}\left[\kappa, L\right] + \frac{1}{3!}\left[\kappa, \left[\kappa, L\right]\right] + ...\right]_{ji}\,,
$$

其中右边是 Baker-Campbell-Hausdorff 公式的一个特例，之所以成立
是因为 $\kappa$ 的空间构成其指数所对应李群的李代数。
由于梯度对 $\kappa_{\mathrm{oo}}$ 和
$\kappa_{\mathrm{vv}}$ 的所有元素总是为零，
这些 $\kappa$ 块在优化中被丢弃为自由度。
由于要求 $e^{\kappa}$ 是幺正的，
$\kappa$ 必须是反厄米的，这又在优化中丢弃了
若干轨道旋转自由度。

鞍点搜索使用 L-SR1 拟牛顿优化器进行，它能够形成不定模型 Hessian，
从激发态初始猜测开始。为提高方法的性能并使其更稳健，
使用了以下标准 SOSCF 预条件子，并允许其也变为不定的：

$$
\frac{\partial^{2}E}{\partial \kappa_{ij}^{2}} \approx 2\left(f_{j} - f_{i}\right)\left(\epsilon_{i} - \epsilon_{j}\right)\,,
$$

其中 $f_{i}$ 是轨道 $i$ 的占据数，$\epsilon_{i}$ 是其能量。

<a id="sec:spectroscopyproperties.deltascf.theory.gmf"></a>
### 广义模式追踪（Generalized Mode Following）

广义模式追踪（GMF）方法[Schmerwitz2023,Schmerwitz2024b](../../bibliography.md) 是一种更稳健
但也稍贵一些的鞍点搜索方法，可用于收敛到 $\Delta$SCF 激发态解。
该方法通过修改梯度将鞍点搜索重新表述为极小化问题，
使得它对应于一个修改后的目标函数，该函数在能量函数具有
目标鞍点处取得极小值。现在可以执行极小化来定位
对应于目标激发态的目标鞍点，这意味着可以使用稳健的 L-BFGS
优化器代替 L-SR1 优化器，预条件子可以设为正定的，
而且通过构造，变分坍缩到目标之外的低能量解变得不可能，
因此 GMF 不需要 MOM。为此，需要在计算开始时估计目标解的
鞍点阶数 $n$，并且在每个电子优化步骤中需要用有限差分
Davidson 方法求电子 Hessian 的最低 $n$ 个本征对。

一旦在每个优化步骤求得电子 Hessian 的最低 $n$ 个本征向量 $v_{i}$，
修改后的梯度按下式计算

$$
g^{\mathrm{\,mod}} = g - 2\sum_{i = 1}^{n}v_{i}v_{i}^{\mathrm{T}}g\,.
$$

<a id="sec:spectroscopyproperties.deltascf.theory.fr"></a>
## Freeze-and-release 策略（Freeze-and-release strategy）

在棘手的情形下，特别是激发导致大量电荷转移时，
改用 freeze-and-release SOSCF 策略[Schmerwitz2025](../../bibliography.md) 可能更为有利，
它分两步收敛 DeltaSCF：

1. 约束优化，冻结所有被激发的轨道，即占据数与 aufbau 占据不同的那些轨道。
   这一步对未受约束的轨道归结为极小化。

2. 像往常一样进行无约束优化。

第 1 步考虑了激发后电子密度一阶变化对未参与激发的轨道的轨道弛豫效应。
它可以看作是为第 2 步激发态鞍点搜索生成优质初始猜测的一种精细方式。

<a id="sec:spectroscopyproperties.deltascf.examples"></a>
## 输入与示例（Input and examples）

本节给出一些示例计算及其输入。

<a id="sec:spectroscopyproperties.deltascf.examples.simple"></a>
### 第一个示例：甲醛的 HOMO-LUMO 激发态（First Example: HOMO-LUMO Excited State of Formaldehyde）

让我们从尝试收敛到甲醛的第一激发态并在该电子态下优化几何结构开始，
从常规平面结构出发：

```mol
title: structure 1
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
4
structure (0 1)
C      0.000000     0.000000    -0.602985
O      0.000000     0.000000     0.605394
H      0.000000     0.934673    -1.182175
H      0.000000    -0.934673    -1.182175
--- input ---
!PBE DEF2-TZVP OPT FREQ DELTASCF UHF 
%SCF ALPHACONF 0,1 END
* XYZ 0 1
C      0.000000    0.000000   -0.602985
O      0.000000    0.000000    0.605394
H      0.000000    0.934673   -1.182175
H      0.000000   -0.934673   -1.182175
*
```

除了常规关键词（如方法、基组、`OPT` 和 `FREQ`）外，需要在简单输入中
指定 `DELTASCF`，本例中还需要 `UHF`，因为由于单激发，alpha 和 beta
轨道将会不同（对于双激发态 `RHF` 可能就足够了）。

还需要在 `%SCF` 块下添加 `ALPHACONF` 或 `BETACONF`。这是您想要收敛到的
组态的最小表示。本例中，`0,1` 表示 HOMO/LUMO 跃迁，其中 HOMO 占据为零、
LUMO 占据为一。对于 HOMO-1/LUMO 跃迁，应为 `ALPHACONF 0,1,1`。
对于 HOMO/LUMO+1，应为 `ALPHACONF 0,0,1`，依此类推。
只要想象一下前线轨道的占据应该是什么样即可。
第一个零以下的任何轨道都被假定为占据，最后一个占据以上的任何轨道
都被假定为空。

常规启动之后，$\Delta$SCF 特有的打印显示：

```orca
-------------------------------
DELTA-SCF INITIAL CONFIGURATION
-------------------------------

Alpha: 1.00 1.00 1.00 0.00 1.00 0.00 0.00 0.00
Beta : 1.00 1.00 1.00 1.00 0.00 0.00 0.00 0.00

Hessian update                             ... L-SR1
Aufbau metric                              ... MOM
Keep initial reference                     ... true
```

在这里您可以跟踪初始组态以及其他一些重要事项：

1. `Hessian update` 指的是用于 SOSCF Hessian 更新的方法。ORCA 的默认值是
`L-BFGS`，它强制电子 Hessian 为正定，并且总是将体系推向极小值。
由于我们要去鞍点，`DeltaSCF` 默认设置 `L-SR1`。关于 Hessian 更新
及其后果的更多细节见 Hannes Jónsson 课题组的这篇参考文献[Levi2020b](../../bibliography.md)。

2. `Aufbau metric` 是衡量实际波函数与参考波函数之间"重叠"的方式
（更多细节见 [corzo_using_2022](../../bibliography.md)）。默认是 `MOM`，
但也可以设置 `%SCF PMOM TRUE END` 来使用 `PMOM`。

3. `Keep initial reference TRUE` 意味着我们将始终尝试保持 guess 阶段
之后定义的初始参考态。这在文献中有时称为 `IMOM`
[barca_simple_2018](../../bibliography.md)。如果设置了 `%SCF KEEPINITIALREF FALSE END`，
则总是取最后一次 SCF 迭代作为参考。

!!! warning
    这里我们使用 `PMODEL` 猜测的轨道，因为它很简单。一般而言，
    我们建议始终通过读取先前收敛的基态 SCF 轨道来启动 SCF！
    请查看 [initialguess.restart](#sec:essentialelements.initialguess.restart) 获取更多信息。

这个计算在 12 步内轻而易举地收敛了：

```orca
----------------------------------D-I-I-S--------------------------------------------
Iteration    Energy (Eh)       Delta-E    RMSDP     MaxDP     DIISErr  Damp  Time(sec)
-------------------------------------------------------------------------------------
               ***  Starting incremental Fock matrix formation  ***
MOM changed the orbital occupation numbers
  1   -114.2533654537761123     0.00e+00  2.06e-03  6.64e-02  7.14e-02  0.700   0.1
MOM changed the orbital occupation numbers
  2   -114.2675698961360382    -1.42e-02  4.71e-04  1.46e-02  3.08e-02  0.700   0.1
                               ***Turning on AO-DIIS***
MOM changed the orbital occupation numbers
  3   -114.2754325617175226    -7.86e-03  1.98e-04  3.98e-03  2.21e-02  0.700   0.1
MOM changed the orbital occupation numbers
  4   -114.2806616906060100    -5.23e-03  4.98e-04  6.40e-03  1.60e-02  0.000   0.1
MOM changed the orbital occupation numbers
                              *** Initializing SOSCF ***
---------------------------------------S-O-S-C-F-----------------------------------
Iteration   Energy (Eh)           Delta-E    RMSDP     MaxDP    MaxGrad  Time(sec)
-----------------------------------------------------------------------------------
  5    -114.2932665018211225    -1.26e-02  7.19e-05  1.55e-03  2.33e-03     0.1
             *** Restarting incremental Fock matrix formation ***
                          *** Restarting Hessian update ***
  6    -114.2932913947584979    -2.49e-05  5.82e-05  1.33e-03  1.11e-03     0.1
  7    -114.2932671856877818     2.42e-05  2.54e-05  5.00e-04  2.58e-03     0.1
  8    -114.2932914986330530    -2.43e-05  1.76e-05  3.20e-04  1.02e-03     0.1
  9    -114.2932961472105404    -4.65e-06  2.13e-06  6.94e-05  6.42e-05     0.1
 10    -114.2932961779292640    -3.07e-08  2.99e-05  1.10e-03  8.27e-06     0.1
 11    -114.2932921911087050     3.99e-06  3.05e-05  1.12e-03  5.44e-04     0.1
 12    -114.2932961794015654    -3.99e-06  2.45e-08  5.31e-07  2.39e-07     0.1
                *** Gradient check signals convergence ***
```

!!! note
      `MOM changed the orbital occupation numbers` 这句话是正常的，
      它只是在打印它正在做什么。不用担心。

从自旋污染可以看出，这确实是一个开壳层单重态：

```orca
----------------------
UHF SPIN CONTAMINATION
----------------------

Warning: in a DFT calculation there is little theoretical justification to
         calculate <S**2> as in Hartree-Fock theory. We will do it anyways
         but you should keep in mind that the values have only limited relevance

Expectation value of <S**2>     :     1.006910
Ideal value S*(S+1) for S=0.0   :     0.000000
Deviation                       :     1.006910
```

然后计算梯度，几何结构被优化直到收敛。最后，频率表明这实际上
不是极小值，而是几何空间上的一个鞍点！

```orca
-----------------------
VIBRATIONAL FREQUENCIES
-----------------------

Scaling factor for frequencies =  1.000000000  (already applied!)
      
     0:       0.00 cm**-1
     1:       0.00 cm**-1
     2:       0.00 cm**-1
     3:       0.00 cm**-1
     4:       0.00 cm**-1
     5:       0.00 cm**-1
     6:    -591.31 cm**-1 ***imaginary mode***
     7:     799.56 cm**-1
     8:    1228.37 cm**-1
     9:    1271.29 cm**-1
    10:    2971.77 cm**-1
    11:    3067.96 cm**-1
```

原因在于：甲醛的 HOMO/LUMO 跃迁占据了 $\pi^*$ LUMO，从而破坏了双键，
使碳原子变为锥形。如果从略微扭曲的结构开始，就会收敛到实际的几何极小值。
从锥形结构开始：

```mol
title: structure 2
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
4
structure (0 1)
C       0.00000      0.00000     -0.60298
O      -0.74131     -0.10909      0.45746
H       0.00000      0.93467     -1.18217
H       0.00000     -0.93467     -1.18217
--- input ---
!wB97M-D4 DEF2-TZVP DELTASCF UHF OPT FREQ
%SCF ALPHACONF 0,1 END
* XYZ 0 1
C          0.00000        0.00000       -0.60298
O         -0.74131       -0.10909        0.45746
H          0.00000        0.93467       -1.18217
H          0.00000       -0.93467       -1.18217
*
```

现在收敛到一个极小值，如没有负频率所示：

```orca
-----------------------
VIBRATIONAL FREQUENCIES  
-----------------------  

Scaling factor for frequencies =  1.000000000  (already applied!)
      
     0:       0.00 cm**-1
     1:       0.00 cm**-1
     2:       0.00 cm**-1    
     3:       0.00 cm**-1
     4:       0.00 cm**-1
     5:       0.00 cm**-1
     6:     713.25 cm**-1
     7:     826.75 cm**-1
     8:    1206.57 cm**-1
     9:    1292.70 cm**-1
    10:    2826.06 cm**-1
    11:    2893.16 cm**-1
```

最终几何结构对气相甲醛来说也出奇地准确！我们这里也给出
使用范围校正的 meta-GGA 杂化泛函 `wB97M-D4` 和双杂化 DFT
`!B2PLYP DEF2-QZVPP AUTOAUX` 的结果，只是为了表明 MP2 也适用。

<a id="tab:form_geom"></a>
!!! note "气相甲醛的几何结构与 DeltaSCF 结果比较，单位为埃和度。"
    | 参数         |  实验值 |   PBE    | wB97M-D4 | B2PLYP   | 
    |:------------:|:-------:|:--------:|:--------:|:--------:|
    | r(C-O)       |   1.323 |  1.300   |   1.310  | 1.311    |
    | r(C-H)       |   1.098 |  1.113   |   1.093  | 1.090    |
    | $\angle$HCH  |   118.8 |  115.0   |   117.0  | 116.8    |
    | $\angle$OOP  |   34.0  |  41.1    |   36.5   | 37.0     |

* 实验值取自 [gilbert_self-consistent_2008](../../bibliography.md)。

!!! warning
      这里我们使用默认的基态 SCF 算法 `AO-DIIS` + `SOSCF`，因为这相对简单。
      一般而言，对于更复杂的情形，我们建议使用近似二阶方法，
      以 `!NODIIS NOTRAH`（$\Delta$SCF 的默认设置）避免逃回基态。

!!! warning
      **不要**将 $\Delta$SCF 波函数与 CCSD 或任何此类单激发方法结合使用。
      这需要 CC 的一个专门版本，我们目前还没有。

!!! warning
      用 `wB97M-D4` 运行上述同样的计算时，alpha HOMO-1 和 HOMO 之间
      **不会**有虚拟轨道（因此没有负的 HOMO-LUMO 能隙）。这里没有任何问题，
      它只是将轨道优化到了激发态，使得占据数对应于 aufbau 占据。
      杂化泛函倾向于降低占据轨道相对于虚拟轨道的能量。

      能量仍然高于非 $\Delta$SCF 解，如果绘制轨道图，您会看到
      alpha HOMO 现在是一个 $\pi$ 轨道而不是 $n$ 轨道。电子 Hessian 的
      本征值表明该解是一个一阶鞍点。

<a id="sec:spectroscopyproperties.deltascf.examples.ionized"></a>
### 芯电离态（Core-ionized States）

$\Delta$SCF 的另一个大优点是可能收敛到芯激发和/或芯电离态。
我们有一个简单关键词可以从任何轨道（甚至是深层芯轨道）移除电子：

```orca
%SCF IONIZEALPHA 2 END
```

这样 2 号轨道的电子将被移除。`IONIZEBETA` 对 beta 轨道起作用。
也可以从通过添加一个额外电子获得的阴离子 UHF 电子结构开始，
像这样移除一个芯电子以获得芯激发态。几何优化、EPR 甚至
TDDFT 计算对这些态都有效。

例如，下面的输入将从水分子电离 1s 电子，这里对应于 MO 0：

```mol
title: structure 3
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
3
structure (0 1)
O      2.127880    -0.361920     0.104770
H      3.117210    -0.387460     0.070360
H      1.838520    -0.926280    -0.655730
--- input ---
!PBE0 DEF2-TZVP DELTASCF NODIIS UHF
%SCF IONIZEALPHA 0 END
* xyz 0 1
  O      2.127880   -0.361920    0.104770
  H      3.117210   -0.387460    0.070360
  H      1.838520   -0.926280   -0.655730
*
```

!!! note
      如果轨道不是定域在单个原子上，可能需要先将其定域！

从结果可以看出，它确实收敛到了那里。

```orca
----------------
ORBITAL ENERGIES
----------------
                 SPIN UP ORBITALS
  NO   OCC          E(Eh)            E(eV) 
   0   0.0000     -20.108086      -547.1688 
   1   1.0000      -1.567415       -42.6515 
   2   1.0000      -1.057257       -28.7694 
   3   1.0000      -0.939315       -25.5601 
   4   1.0000      -0.882871       -24.0241 
   5   0.0000      -0.304254        -8.2792 
   6   0.0000      -0.239285        -6.5113 
   7   0.0000       0.044344         1.2066 
        (...)
```

!!! note
      ORCA 会在这里自动调整电荷和多重度。**输入应包含参考体系的那些值！**

这里给出一些 1s 电子结合能的例子。移除电子的原子用粗体标出：

<a id="tab:core_ion"></a>
!!! note "DeltaSCF 使用 wB97M-V/DEF2-TZVPP 得到的 1s 电子结合能，单位 eV。"
    | 1s 电离        |  实验值   | wB97M-V  |
    |:---------------:|:---------:|:--------:|
    | H2**O**         |   539.82  | 541.17   | 
    | **C**O2         |   297.69  | 299.10   |
    | **N**H3         |   405.56  | 406.82   |
    | CH3C**N**       |   405.64  | 406.92   |

* 实验值取自 [carter-fenk_state-targeted_2020](../../bibliography.md)

<a id="sec:spectroscopyproperties.deltascf.examples.couplings"></a>
### 透热耦合（Diabatic Couplings）

$\Delta$SCF 也是获得透热耦合的一种相当精确的方法，
这些耦合随后可用于 Marcus 理论计算电子转移速率。
它们可以通过计算电子转移态之间的能量差并使用
广义 Mulliken-Hush 方法（GMH）来计算。
更多细节请参考例如 Blumberger 课题组的这篇论文
[kubas_electronic_2014](../../bibliography.md)。

这里没有足够的篇幅详述细节，但基本上可以通过一次常规基态 SCF
加一次激发态 $\Delta$SCF 来获得这些透热耦合。
对于对称体系，这是简单的：

$$
2|H_{ab}| = \Delta E_{12}
$$

其中态 $a$ 和 $b$ 是透热态，$\Delta E_{12}$ 是绝热态 $1$ 和 $2$
之间的能量差（通过 SCF 解获得）。下面是苯二聚体透热耦合的例子，
通过从基态阳离子开始并激发 beta 电子获得：

```orca
%SCF BETACONF 0,1 END
```

<a id="tab:diabatic_couplings"></a>
!!! note "$\Delta$SCF 使用 wB97M-V/DEF2-TZVPP 得到的透热耦合，单位 meV。"
    | 距离（埃） |  MRCI+Q  | wB97M-V  | TD-DFT |
    |:---------------:|:--------:|:--------:|:------:|
    | 3.5             |  435.2   | 473.1    |  593   |
    | 4.0             |  214.3   | 236.7    |  374   |
    | 4.5             |  104.0   | 115.9    |  267.5 |
    | 5.0             |  51.70   | 56.7     |  218.5 |

* MRCI+Q 取自 [kubas_electronic_2014](../../bibliography.md)

<a id="sec:spectroscopyproperties.deltascf.examples.gmf"></a>
### 广义模式追踪（Generalized Mode Following）

作为一个 GMF 计算示例，我们回到甲醛分子，这次以 HOMO-LUMO+1
激发为目标以增加趣味性，并添加简单输入关键词 `GMF`：

```mol
title: structure 4
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
4
structure (0 1)
O      -3.54418      1.61112      0.04891
C      -4.12047      0.61074     -0.35955
H      -3.36418     -0.41948     -0.79627
H      -4.84699      0.73407     -1.42962
--- input ---
!WB97X-D4 DEF2-SVP UKS DELTASCF GMF
%SCF ALPHACONF 0,0,1 END
* XYZ 0 1
O         -3.54418        1.61112        0.04891
C         -4.12047        0.61074       -0.35955
H         -3.36418       -0.41948       -0.79627
H         -4.84699        0.73407       -1.42962
*
```

如果输入中未提供，目标鞍点阶数通过使用轨道能或计算电子 Hessian
的负本征值数目来估计。在前一种情况下，目标鞍点阶数近似为
激发后激发态初始猜测中占据轨道能量高于虚拟轨道的占据-虚拟
轨道对的数量。在我们的例子中，这给出鞍点阶数 2，
如默认估计的那样，并与其他一些默认输入参数一起
打印在 `DeltaSCF` 块中：

```orca
-------------------------------
DELTA-SCF INITIAL CONFIGURATION
-------------------------------

Alpha: 1.00 1.00 1.00 0.00 0.00 1.00 0.00 0.00 0.00
Beta : 1.00 1.00 1.00 1.00 0.00 0.00 0.00 0.00 0.00

Hessian update                             ... L-BFGS/GMF
Generalized mode following:
 Target saddle point order                 ... 2
 Finite difference generalized Davidson method:
  Finite difference mode                   ... Forward
  Finite difference step size              ... 1.000e-03
  Max. size of Krylov subspace             ... 20
  Convergence tolerance                    ... 1.000e-02
  Max. number of iterations                ... 100
Aufbau metric                              ... Fixed occupations
```

在每个优化步之前，计算电子 Hessian 的最低 2 个（与目标鞍点阶数相同）
本征对，一旦收敛到容差以下，就打印本征值，例如第一次优化步：

```orca
Solving for 2 Hessian eigenvectors
    It.    Root MAX Err.:          1          2
    1                      6.520e-02  6.276e-02
    2                      3.193e-02  2.817e-02
    3                      1.511e-02  9.423e-03
    4                      3.889e-03  9.417e-03
    Eigenvalues:          -3.316e-01 -2.404e-01
```

经过几步优化后，Hessian 本征对的求解不再需要进一步调整，
因此 Davidson 运行立即收敛：

```orca
        Solving for 2 Hessian eigenvectors
            It.    Root MAX Err.:          1          2
            1                      5.165e-03  8.433e-03
            Eigenvalues:          -2.574e-01 -1.792e-01
   11    -114.1023998750192305    -1.06e-05  1.06e-03  1.96e-02  5.46e-04     1.3
        Solving for 2 Hessian eigenvectors
            It.    Root MAX Err.:          1          2
            1                      5.755e-03  8.231e-03
            Eigenvalues:          -2.575e-01 -1.791e-01
   12    -114.1024101850037624    -1.03e-05  6.43e-04  1.25e-02  3.11e-04     1.3
        Solving for 2 Hessian eigenvectors
            It.    Root MAX Err.:          1          2
            1                      6.190e-03  8.354e-03
            Eigenvalues:          -2.575e-01 -1.790e-01
   13    -114.1024129524389963    -2.77e-06  3.67e-04  7.30e-03  2.00e-04     1.3
        Solving for 2 Hessian eigenvectors
            It.    Root MAX Err.:          1          2
            1                      6.264e-03  8.286e-03
            Eigenvalues:          -2.574e-01 -1.790e-01
   14    -114.1024142211099530    -1.27e-06  8.68e-05  1.34e-03  1.46e-04     1.3
        Solving for 2 Hessian eigenvectors
            It.    Root MAX Err.:          1          2
            1                      6.396e-03  8.439e-03
            Eigenvalues:          -2.574e-01 -1.790e-01
   15    -114.1024145538739987    -3.33e-07  4.56e-05  7.31e-04  9.17e-05     1.3
                **** Energy Check signals convergence ****
```

在这个简单例子中，人们会期望组态在优化过程中保持不变。
这里并非如此，同样是因为使用了杂化泛函。占据轨道相对于
虚拟轨道被稳定化，导致如下组态：

```orca
----------------
ORBITAL ENERGIES
----------------
                 SPIN UP ORBITALS
  NO   OCC          E(Eh)            E(eV)
   0   1.0000     -19.374322      -527.2021
   1   1.0000     -10.431285      -283.8497
   2   1.0000      -1.258409       -34.2430
   3   1.0000      -0.755807       -20.5666
   4   1.0000      -0.635639       -17.2966
   5   1.0000      -0.591213       -16.0877
   6   1.0000      -0.584445       -15.9036
   7   0.0000      -0.143277        -3.8988
   8   1.0000      -0.113247        -3.0816
   9   0.0000      -0.061224        -1.6660
  10   0.0000       0.146574         3.9885
  11   0.0000       0.251438         6.8420
  12   0.0000       0.490702        13.3527
  13   0.0000       0.537161        14.6169
  14   0.0000       0.565655        15.3923
  15   0.0000       0.624632        16.9971
  16   0.0000       0.649717        17.6797
  17   0.0000       0.710983        19.3468
  18   0.0000       0.928559        25.2674
```

最后优化步 Hessian 的两个最低本征值明显为负，
因此该解是一个二阶鞍点，正如优化中预期和以之为目标的那样。
如果使用杂化泛函，不要依赖组态来确定鞍点阶数！

<a id="sec:spectroscopyproperties.deltascf.examples.fr-soscf"></a>
### Freeze-and-release 策略（Freeze-and-release strategy）

让我们来看一下 90 度扭转的 N-苯基吡咯分子的一个棘手激发态。
我们首先使用以下输入进行不带 `DeltaSCF` 的基态 SCF 计算：

```mol
title: structure 5
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
20
structure (0 1)
C   10.13954933  10.09711395  12.38421108
C   11.34646202  10.09711395  13.07460199
C    8.93263664  10.09711395  13.07460199
C   10.13954933  10.09711395  15.16101197
C   11.34465495  10.09711395  14.46510328
C    8.93444370  10.09711395  14.46510328
C   10.13954933  11.21630306  10.16939448
C   10.13954933   8.97792484  10.16939448
C   10.13954933  10.80761594   8.85675649
C   10.13954933   9.38661196   8.85675649
N   10.13954933  10.09711395  10.96513494
H   12.26979504  10.09711395  12.51888639
H    8.00930362  10.09711395  12.51888639
H   12.27909865  10.09711395  15.00190089
H    8.00000000  10.09711395  15.00190089
H   10.13954933  10.09711395  16.23847837
H   10.13954933  12.19422790  10.60962753
H   10.13954933   8.00000000  10.60962753
H   10.13954933  11.45309491   8.00000000
H   10.13954933   8.74113299   8.00000000
--- input ---
!UKS aug-cc-pVDZ PBE

*xyz 0 1
C       10.13954933      10.09711395      12.38421108
C       11.34646202      10.09711395      13.07460199
C        8.93263664      10.09711395      13.07460199
C       10.13954933      10.09711395      15.16101197
C       11.34465495      10.09711395      14.46510328
C        8.93444370      10.09711395      14.46510328
C       10.13954933      11.21630306      10.16939448
C       10.13954933       8.97792484      10.16939448
C       10.13954933      10.80761594       8.85675649
C       10.13954933       9.38661196       8.85675649
N       10.13954933      10.09711395      10.96513494
H       12.26979504      10.09711395      12.51888639
H        8.00930362      10.09711395      12.51888639
H       12.27909865      10.09711395      15.00190089
H        8.00000000      10.09711395      15.00190089
H       10.13954933      10.09711395      16.23847837
H       10.13954933      12.19422790      10.60962753
H       10.13954933       8.00000000      10.60962753
H       10.13954933      11.45309491       8.00000000
H       10.13954933       8.74113299       8.00000000
*
```

该计算给出能量 -440.702 E$_\mathrm{h}$ 和偶极矩 2.181 D。现在我们
从这个收敛的基态解出发，使用 `DeltaSCF` 进行激发态计算，
在 alpha 自旋通道中将一个电子从 HOMO 激发到 LUMO，输入如下：

```mol
title: structure 6
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
20
structure (0 1)
C   10.13954933  10.09711395  12.38421108
C   11.34646202  10.09711395  13.07460199
C    8.93263664  10.09711395  13.07460199
C   10.13954933  10.09711395  15.16101197
C   11.34465495  10.09711395  14.46510328
C    8.93444370  10.09711395  14.46510328
C   10.13954933  11.21630306  10.16939448
C   10.13954933   8.97792484  10.16939448
C   10.13954933  10.80761594   8.85675649
C   10.13954933   9.38661196   8.85675649
N   10.13954933  10.09711395  10.96513494
H   12.26979504  10.09711395  12.51888639
H    8.00930362  10.09711395  12.51888639
H   12.27909865  10.09711395  15.00190089
H    8.00000000  10.09711395  15.00190089
H   10.13954933  10.09711395  16.23847837
H   10.13954933  12.19422790  10.60962753
H   10.13954933   8.00000000  10.60962753
H   10.13954933  11.45309491   8.00000000
H   10.13954933   8.74113299   8.00000000
--- input ---
!UKS aug-cc-pVDZ PBE DeltaSCF
!SOSCF NoDIIS NoTRAH
!MORead
!SCFCheckGrad

%moinp "gs.gbw"

%scf
AlphaConf 0,1
DoMOM false
SOSCFMaxStep 0.1
end

*xyz 0 1
C       10.13954933      10.09711395      12.38421108
C       11.34646202      10.09711395      13.07460199
C        8.93263664      10.09711395      13.07460199
C       10.13954933      10.09711395      15.16101197
C       11.34465495      10.09711395      14.46510328
C        8.93444370      10.09711395      14.46510328
C       10.13954933      11.21630306      10.16939448
C       10.13954933       8.97792484      10.16939448
C       10.13954933      10.80761594       8.85675649
C       10.13954933       9.38661196       8.85675649
N       10.13954933      10.09711395      10.96513494
H       12.26979504      10.09711395      12.51888639
H        8.00930362      10.09711395      12.51888639
H       12.27909865      10.09711395      15.00190089
H        8.00000000      10.09711395      15.00190089
H       10.13954933      10.09711395      16.23847837
H       10.13954933      12.19422790      10.60962753
H       10.13954933       8.00000000      10.60962753
H       10.13954933      11.45309491       8.00000000
H       10.13954933       8.74113299       8.00000000
*
```

这个看似简单的激发导致从苯基到吡咯基的大量电荷转移，
使得这个激发态很难收敛。为此，我们用 `SOSCFMaxStep 0.1` 将
SOSCF 优化的最大步长从 0.2（默认）减小到 0.1，并用 `DoMOM false`
停用 MOM，因为 MOM 在大量电荷转移的情形下往往会适得其反。
我们还只使用 SOSCF，通过简单输入 `!SOSCF NoDIIS NoTRAH` 停用
DIIS 和 TRAH，并用 `!SCFCheckGrad` 强制对 SOSCF 梯度进行收敛检查。
后者属于个人偏好。

该计算收敛到一个解，激发能为 189 mE$_{\mathrm{h}}$，
与基态的偶极矩差为 4.958 D，对于这个重电荷转移态来说，
两者都小于预期。这就是所谓的变分坍缩，即计算收敛到了比
所需更低能量的解。

为对抗这种变分坍缩，我们在简单输入行中添加
`FreezeAndRelease`（或 `FRSOSCF`）以使用 freeze-and-release
SOSCF 方法：

```mol
title: structure 7
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
20
structure (0 1)
C   10.13954933  10.09711395  12.38421108
C   11.34646202  10.09711395  13.07460199
C    8.93263664  10.09711395  13.07460199
C   10.13954933  10.09711395  15.16101197
C   11.34465495  10.09711395  14.46510328
C    8.93444370  10.09711395  14.46510328
C   10.13954933  11.21630306  10.16939448
C   10.13954933   8.97792484  10.16939448
C   10.13954933  10.80761594   8.85675649
C   10.13954933   9.38661196   8.85675649
N   10.13954933  10.09711395  10.96513494
H   12.26979504  10.09711395  12.51888639
H    8.00930362  10.09711395  12.51888639
H   12.27909865  10.09711395  15.00190089
H    8.00000000  10.09711395  15.00190089
H   10.13954933  10.09711395  16.23847837
H   10.13954933  12.19422790  10.60962753
H   10.13954933   8.00000000  10.60962753
H   10.13954933  11.45309491   8.00000000
H   10.13954933   8.74113299   8.00000000
--- input ---
!UKS aug-cc-pVDZ PBE DeltaSCF FreezeAndRelease
!MORead
!SCFCheckGrad

%moinp "gs.gbw"

%scf
AlphaConf 0,1
DoMOM 0
SOSCFConvFactor 500
SOSCFMaxStep 0.1
end

*xyz 0 1
C       10.13954933      10.09711395      12.38421108
C       11.34646202      10.09711395      13.07460199
C        8.93263664      10.09711395      13.07460199
C       10.13954933      10.09711395      15.16101197
C       11.34465495      10.09711395      14.46510328
C        8.93444370      10.09711395      14.46510328
C       10.13954933      11.21630306      10.16939448
C       10.13954933       8.97792484      10.16939448
C       10.13954933      10.80761594       8.85675649
C       10.13954933       9.38661196       8.85675649
N       10.13954933      10.09711395      10.96513494
H       12.26979504      10.09711395      12.51888639
H        8.00930362      10.09711395      12.51888639
H       12.27909865      10.09711395      15.00190089
H        8.00000000      10.09711395      15.00190089
H       10.13954933      10.09711395      16.23847837
H       10.13954933      12.19422790      10.60962753
H       10.13954933       8.00000000      10.60962753
H       10.13954933      11.45309491       8.00000000
H       10.13954933       8.74113299       8.00000000
*
```

`FreezeAndRelease` 仅适用于 SOSCF，因此 `SOSCF`、`NoDIIS` 和
`NoTRAH` 是隐含的，无需指定。我们还应用了因子 500，
约束极小化的收敛判据乘以该因子，因为约束极小化不需要像
随后的无约束优化那样紧密收敛。该策略在计算的约束部分
节省了一些迭代，同时不损害最终结果。

该策略给出 194 mE$_{\mathrm{h}}$ 的激发能，比前一个略高，
与基态的偶极矩差为 9.669 D。这就是期望的结果。

通常，freeze-and-release 方法比常规 SOSCF 多需要几次迭代，
但它能更可靠地避免变分坍缩。在所展示的情形中，常规 SOSCF
总共需要 38 次能量/梯度评估收敛，而 freeze-and-release 策略
只需要 21 次能量/梯度评估。

!!! note
      `Scaled step length from x to 0.100000` 这句话表示即将采取
      一个相对较大的步长。将其缩小通常会导致更稳健但效率较低的收敛。
      可以根据所研究体系的挑战进行调整。

freeze-and-release 策略可以与 GMF 结合，产生更稳健的策略。
在这种情况下，目标鞍点阶数在约束极小化步的解处估计，
因为此时估计的质量更高。对于杂化泛函，默认估计在第一次
Davidson 运行中获得。否则，使用轨道能。

<a id="sec:spectroscopyproperties.deltascf.options"></a>
## 完整关键词列表（Full keyword list）

与 $\Delta$SCF 相关的简单输入关键词汇总于表
[tab:spectroscopyproperties.deltascf.options.simple](#tab:spectroscopyproperties.deltascf.options.simple)。

<a id="tab:spectroscopyproperties.deltascf.options.simple"></a>
!!! note "$\Delta$SCF 的简单输入关键词。"
    | 关键词                          | 说明                                       |
    |:--------------------------------|:-----------------------------------------|
    | `DeltaSCF`                      | 激活 $\Delta$SCF                           |
    | `FreezeAndRelease` 或 `FRSOSCF` | 激活 freeze-and-release 策略               |
    | `GMF`                           | 激活广义模式追踪                           |
    | `SCFLBFGS`                      | 将 SOSCF 拟牛顿方法设为 L-BFGS             |
    | `SCFLSR1`                       | 将 SOSCF 拟牛顿方法设为 L-SR1              |

与 $\Delta$SCF 相关的 `%SCF` 块输入关键词汇总于表
[tab:spectroscopyproperties.deltascf.options.scfblock](#tab:spectroscopyproperties.deltascf.options.scfblock)。

<a id="tab:spectroscopyproperties.deltascf.options.scfblock"></a>
!!! note "$\Delta$SCF 的 `%scf` 块输入关键词，括号内为默认值"
    | 关键词                               | 选项                | 说明                                                                                     |
    |:---------------------------------------|:--------------------|:---------------------------------------------------------------------------------------------------------------------------------------|
    | `SOSCFMaxStep` (0.2)                   | `<real>`            | 最大步长                                                                                     |
    | `DeltaSCFFromGS` (true)                | `true/false`        | 从输入的收敛基态解开始 DeltaSCF，还是假设它是激发态解？                                     |
    | `SOSCFBlockDiag` (false)               | `true/false`        | 开始时对 Fock 矩阵的占据和虚拟轨道块进行对角化？                                           |
    | `DoMOM` (true)                         | `true/false`        | 使用最大重叠法？                                                                           |
    | `KeepInitialRef` (true)                | `true/false`        | 始终保持初始参考：IMOM？                                                                   |
    | `PMOM` (false)                         | `true/false`        | 使用 PMOM 度量代替常规 MOM？                                                               |
    | `AlphaConf` 和 `BetaConf`              |                     | 定义 alpha 和 beta 自旋通道中前线轨道的占据                                                |
    |                                        | `0,1`               | HOMO$\rightarrow$LUMO 激发                                                                |
    |                                        | `0,0,1`             | HOMO$\rightarrow$LUMO+1 激发                                                              |
    |                                        | `0,1,1`             | HOMO-1$\rightarrow$LUMO 激发                                                              |
    |                                        | `0,2`               | 双重 HOMO$\rightarrow$LUMO 激发（仅对 `RHF` 和 `AlphaConf` 有效！）                         |
    | `IonizeAlpha` 和 `IonizeBeta`          | `<int>`             | 从 alpha 和 beta 自旋通道的指定 MO 移除电子                                                |
    | `SOSCFHessUp` (LSR1)                   |                     | Hessian 更新的 SOSCF 拟牛顿方法                                                            |
    |                                        | `LSR1`              | 有限内存对称秩 1 更新                                                                      |
    |                                        | `LBFGS`             | 有限内存 Broyden-Fletcher-Goldfarb-Shanno 更新                                             |
    |                                        | `LPOWELL`           | 有限内存 Powell 更新                                                                       |
    |                                        | `LBOFILL`           | 有限内存 Bofill 更新，L-SR1 和 L-Powell 的组合                                             |
    | `SOSCFConstraints` (false)             | `true/false`        | 激活 freeze-and-release SOSCF？                                                            |
    | `SOSCFConstrainedMaxStep` (0.2)        | `<real>`            | 约束极小化的最大步长                                                                       |
    | `SOSCFConvFactor` (1)                  | `<real>`            | 约束极小化中收敛判据的乘数因子。例如 100 将判据放宽两个数量级                               |
    | `SOSCFConstrainedHessUp` (LBFGS)       |                     | 约束极小化的 Hessian 更新                                                                  |
    |                                        | `LSR1`              | 有限内存对称秩 1 更新                                                                      |
    |                                        | `LBFGS`             | 有限内存 Broyden-Fletcher-Goldfarb-Shanno 更新                                             |
    |                                        | `LPOWELL`           | 有限内存 Powell 更新                                                                       |
    |                                        | `LBOFILL`           | 有限内存 Bofill 更新，L-SR1 和 L-Powell 的组合                                             |
    | `SOSCFWriteConstrainedGBW` (true)      | `true/false`        | 为约束解写入 GBW 文件                                                                      |
    | `SOSCFGMF` (false)                     | `true/false`        | 使用广义模式追踪？                                                                         |
    | `SOSCFDavidsonMaxIt` (100)             | `<int>`             | Davidson 迭代的最大次数                                                                    |
    | `SOSCFDavidsonTolR` (0.01)             | `<real>`            | 每个残差向量最大分量的 Davidson 收敛容差                                                   |
    | `SOSCFDavidsonMaxRed` (20)             | `<int>`             | 每个目标本征向量的 Davidson Krylov 子空间最大尺寸，即乘以目标鞍点阶数                       |
    | `SOSCFDavidsonFDMode` (`Forward`)      |                     | 要使用的 Davidson 有限差分模板                                                              |
    |                                        | `Forward`           | 一次位移梯度评估，有限差分步长的线性精度                                                   |
    |                                        | `Central`           | 两次位移梯度评估，有限差分步长的二次精度                                                   |
    | `SOSCFDavidsonFDStep` (0.001)          | `<real>`            | Davidson 有限差分步长                                                                      |
    | `SOSCFSPO`                             | `<int>`             | GMF 可选的用户定义目标鞍点阶数                                                             |
    | `SOSCFSPOEst` (Auto)                   |                     | GMF 目标鞍点阶数估计                                                                       |
    |                                        | `Auto`              | 让算法决定什么是最好的                                                                     |
    |                                        | `Excitation`        | 使用激发组态                                                                               |
    |                                        | `HDiag`             | 使用对角 Hessian 近似（仅在使用 freeze-and-release 时与 `Excitation` 不同）                 |
    |                                        | `Davidson`          | 使用第一次 Davidson 运行中的负本征值数目（第一次运行中以更多本征对为目标）                 |
    | `SOSCFUpdateSPOEst` (true)             | `true/false`        | 仅 GMF：用第一次 Davidson 运行的负本征值数目更新 SPO？                                     |
    | `SOSCFSPOEstNTrial` (3)                | `<int>`             | 为 SPO 估计多以多少个 Hessian 本征向量为目标                                               |
    | `SOSCFUpdateSPOThresh` (-1 eV)         | `<real>`            | 只有低于此阈值的本征值才被认为对 SPO 估计足够负                                            |
    | `SOSCFPrecondType` (OrbitalEnergyDiff) |                     | 要使用的 SOSCF 预条件子                                                                    |
    |                                        | `OrbitalEnergyDiff` | 基于轨道能差的常规预条件子                                                                 |
    |                                        | `DavidsonUpdate`    | `OrbitalEnergyDiff` 预条件子，但最小的元素（数目由 `SOSCFSPOEstNTrial` 给出）在开始时用一次有限差分 Davidson 运行的本征值更新 |
    |                                        | `GradientExpansion` | 仅 GMF：将预条件子与梯度展开混合（比例由 `SOSCFPrecondGamma` 给出）。这倾向于强制预条件子为正定 |
    | `SOSCFPrecondGamma` (0.25)             | `<real>`       | `GradientExpansion` 预条件子的混合因子                                                         |

