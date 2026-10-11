```{index} MECP
```

(sec:structurereactivity.mecp)=
# 最小能量交叉点（Minimum Energy Crossing Points，MECP）

MECP 优化允许用户优化到两个不同势能面（PES1 和 PES2）相互交叉的结构。在此优化中适用两个条件：在最小化 PES1 能量 $E_{1}$ 的同时，最小化两个势能面的能量差 $\left({ E_{1} -E_{2} } \right)^{2}$。在实现上，我们原则上遵循 Harvey 等人在 {cite}`harvey1998theor` 中的建议。

对于最小化过程，构造了两个不同的梯度：

用于最小化的第一个梯度为

$$\mathbf{f}=\frac{\partial }{\partial q}\left({ E_{1} -E_{2} }
\right)^{2}=2\left({ E_{1} -E_{2} } \right)\cdot x_{1}
$$ (eq199)

其中 $x_1$ 是梯度差矢量（gradient difference vector）

$$x_{1} =\left[{ \left({ \frac{\partial E_{1} }{\partial q} } \right)-\left({\frac{\partial E_{2} }{\partial q} } \right)} \right]$$ (eqn:209)

它在 MECP 附近与交叉超线（crossing hyperline）正交。

梯度

$$\mathbf{g}=\left({ \frac{\partial E_{1} }{\partial q} }
\right)-\frac{x_{1} }{\left|{ x_{1} } \right|}\left[{ \left({ \frac{\partial
E_{1} }{\partial q} } \right)\cdot \frac{x_{1} }{\left|{ x_{1} } \right|} }
\right]$$ (eqn:210)

与 $x_1$ 正交。

两个梯度组合得到有效的表面交叉梯度（surface crossing gradient）

$$\mathbf{g}_{\mathbf{SC} } =\mathbf{\, g+f}
$$ (eqn:211)

交叉超线定义为 PES1 中与 $x_1$ 正交的 $3N-7$ 维子空间。在 MECP 优化中，我们要寻找该子空间内的最低能量点。

我们对沿交叉超线运动的简正模式和力常数的计算方式与 Harvey 等人提出的方法不同。标准的频率分析无法执行，但采用了类似的过程：

让我们考察在 MECP 附近沿交叉超线（与 $x_1$ 正交）发生位移时两个势能面能量的二阶泰勒展开：

$$\mathbf{E}_{A} =E_{\mathrm{MECP} } +\frac{1}{2}\Delta
q^{T}H_{\mathrm{eff},A} \Delta q
$$ (eqn:212)

其中：

|                    |                                           |
|:-------------------|:------------------------------------------|
| $\mathbf{E}_{A}$   | PES1 上的能量 E$_{1}$ 或 PES2 上的 E$_{2}$ |
| $H_{\mathrm{eff},A}$ | PES1 或 PES2 的有效 Hessian              |
| $\Delta q$         | 沿交叉超线的位移 |

对该有效 Hessian 进行对角化，即可得到交叉超线的简正模式，从而可以判断 MECP 优化是否在交叉超线的 $3N-7$ 维子空间中收敛到极小值点。

有效 Hessian 的计算过程如下：对两个势能面中的每一个都计算二阶导数矩阵。然后从 Hessian 矩阵中投影掉 6 个转动和平动，以及梯度差矢量 $x_1$ 的方向（这确保了与交叉超线正交的运动被排除——对于该运动我们并不满足驻点条件）。

作为示例，我们展示 \[FeO\]$^{+}$ 四重态和六重态的 MECP 优化。

```orcainput
! B3LYP TZVP Opt SurfCrossOpt SlowConv

%mecp
   Mult 4
end

* xyz +1 6
Fe 0.000000     0.000000     0.000000
O  0.000000     0.000000     1.670000
*
```


:::{tip}
你通常可以用其中一个自旋态的极小值点或过渡态结构作为 MECP 优化的初始猜测。如果这不起作用，可以尝试用扫描获得更好的初始猜测。
:::

MECP 优化的结果在以下输出中给出。两个势能面交叉处的距离为 1.994 Å。在这个简单示例中只有一个自由度，我们也可以通过参数扫描定位 MECP。作为对比，扫描结果见 {numref}`fig:14`。从中可以看到，交叉发生在 Fe–O 距离约为 2 Å 处。

对于多于两个原子的体系，扫描就不再够用了，必须使用 MECP 优化。

```orca
***********************HURRAY********************
***        THE OPTIMIZATION HAS CONVERGED     ***
*************************************************

-------------------------------------------------------------------
                   Redundant Internal Coordinates
                   --- Optimized Parameters ---
                   (Angstroem and degrees)
  Definition                   OldVal   dE/dq     Step     FinalVal
   -------------------------------------------------------------------
1. B(O   1,Fe  0)              1.9940 -0.000001  0.0000    1.9940
   -------------------------------------------------------------------

      *******************************************************
      *** FINAL ENERGY EVALUATION AT THE STATIONARY POINT ***
      ***               (AFTER    8 CYCLES)               ***
      *******************************************************

    -------------------------------------   ----------------
    Energy difference between both states       -0.000000004
    -------------------------------------   ----------------
```

(fig:14)=
:::{figure} ../../images/614.*
:width: 50%
[FeO]$^+$ 四重态和六重态的参数扫描（B3LYP/SV(P)）。
:::

一个更实际的、具有多于一个自由度的例子是 CH$_{3}$O $\leftrightarrow$ CH$_{2}$OH 异构化反应路径上某一结构的 MECP 优化。

```orcainput
! B3LYP SV SurfCrossOpt SurfCrossNumFreq

%mecp 
   Mult 1
end

*xyz 1 3
 C     0.000000     0.000000     0.000000
 H     0.000000     0.000000     1.300000
 H     1.026719     0.000000    -0.363000
 O    -0.879955     0.000000    -1.088889
 H    -0.119662    -0.866667     0.961546
*
```

:::{Note}
-   要验证 MECP 优化中的驻点是否为极小值点，必须使用一种改进的频率分析，通过 `SurfCrossNumFreq` 调用。
:::

(sec:structurereactivity.mecp.keywords)=
## 关键词（Keywords）

MECP 优化有以下选项：

```orca
%mecp
   SurfCrossOpt true  # switches on the MECP optimization
                      #  alternatively use: ! SurfCrossOpt
   SurfCrossNumFreq true # switches on the MECP effective Hessian
                         #  calculation
                         #  alternatively use: ! SurfCrossNumFreq
 # separate MO input for the second spin state (PES2)
   moinp "Myfile.gbw"# MO input for PES2
 # information on the electronic structure of PES 2
   Mult 3            # multiplicity of PES2
   brokenSym 1,1     # broken symmetry for PES2
 # CASSCF options for PES2 (also see the CASSCF chapter)
   casscf_nel 6       # number of active space electrons
   casscf_norb 6      # number of active orbitals
   casscf_mult 1,3    # multiplicities singlet and triplet
   casscf_nroots 4,2  # four singlets, two triplets
   casscf_bweight 2,1 # singlets and triplets weighted 2:1
   casscf_weights[0] = 0.5,0.2,0.2,0.2 # singlet weights
   casscf_weights[1] = 0.7,0.3         # triplet weights
end
```
