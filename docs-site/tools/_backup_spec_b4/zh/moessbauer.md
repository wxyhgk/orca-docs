

<a id="sec:spectroscopyproperties.moessbauer"></a>
# 穆斯堡尔参数（Mössbauer Parameters）

$^{57}$Fe 穆斯堡尔谱学（Mössbauer spectroscopy）探测的是原子核在
$I = \frac{1}{2}$ 基态与位于基态之上 14.4 keV 处的 $I = \frac{3}{2}$
激发态之间的跃迁。穆斯堡尔谱的重要特征是
同质异能移（isomer shift，$\delta$）和
四极分裂（quadrupole splitting，$\Delta E_\mathrm{Q}$）。
一个理想化的谱图见 [fig:Moessbauer](#fig:Moessbauer)。

<a id="fig:Moessbauer"></a>
*理想化的穆斯堡尔谱，同时标出同质异能移 $\delta$ 和四极分裂 $\Delta E_\mathrm{Q}$。*

## 同质异能移（Isomer Shift）

同质异能移衡量的是 $\gamma$ 射线吸收能量相对于标准样品
（通常是铁箔）的位移。同质异能移对核处的电子密度敏感，
并可间接探测因共价性和 3d 屏蔽变化引起的价轨道成键变化。
因此，它可用于探测氧化态、自旋态以及铁的配位环境。

同质异能移和四极分裂均可通过 DFT 方法成功预测。
同质异能移与核处的 s 电子密度直接相关，可用下式计算

$$

\delta = \alpha (\rho_0 - C) + \beta\qquad \text{(eqn:MB_isomer_shift)}

$$

其中 $\alpha$ 是一个常数，取决于吸收过程中核电荷分布的变化，
$\rho_0$ 是核处的电子密度 [Neese2002Moessbauer](../../bibliography.md)。
常数 $\alpha$ 和 $\beta$ 通常通过对一系列具有不同氧化态和自旋态的铁化合物，
将实验同质异能移与理论计算的电子密度作线性回归分析来确定。
由于电子密度依赖于所用的泛函和基组，
因此对每一种所用组合都必须单独进行拟合。
已有文献汇编了各种方法的校准常数（$\alpha$、$\beta$ 和 $C$）。[roemelt2009moessbauer](../../bibliography.md)
通常，对于采用适中大小基组的 DFT，可达到优于 0.10 mm s$^{-1}$ 的精度。

## 四极分裂（Quadrupole splitting）

四极分裂源于激发态的核四极矩与核处电场梯度（electric field gradient）的相互作用。
前者与激发态中非球形的电荷分布有关。
因此，四极分裂对配合物的配位环境和几何结构极为敏感。

四极分裂与核处**电场梯度**（electric field gradient，EFG）张量的最大分量成正比，
可用下式计算：

$$

\Delta E_\mathrm{Q} = \frac{1}{2}eQV_{zz} \left( 1+\frac{\eta^2}{3} \right)^{\frac{1}{2} }\qquad \text{(eqn:MB_quadrupole_splitting)}

$$

其中 $e$ 是电子的电荷，$Q$ 是 Fe 的核四极矩（约为 0.16 barn）。
$V_{xx}$、$V_{yy}$ 和 $V_{zz}$ 是电场梯度张量的分量，
而不对称参数 $\eta$ 定义为

$$

\eta = \left| \frac{V_{xx} - V_{yy} }{V_{zz} } \right|\qquad \text{(eqn:MB_eta)}

$$

其坐标系选取满足 $|V_{zz}| \geq |V_{yy}| \geq |V_{xx}|$。

电场梯度张量与超精细耦合的偶极贡献密切相关。
主要区别在于：其计算中进入的是电子密度而非自旋密度，
并且它还包含来自周围原子核的核贡献。其计算式为

$$

\begin{array}{l}
 V_{\mu \nu } \left( N \right)=-\sum\limits_{kl} { P_{kl} } \left\langle {\phi_{k} \left|{ r_{N}^{-5} \left({ 3\vec{{r} }_{N\mu } \vec{{r} }_{N\nu }
-\delta_{\mu \nu } r_{N}^{2} } \right)} \right|\phi_{l} } \right\rangle\\
\hspace{1.5cm}
+\sum\limits_{A\ne
N} { Z_{A} \vec{{R} }_{AN}^{-5} \left({ 3\vec{{R} }_{AN\mu } \vec{{R} }_{AN\nu }
-\delta_{\mu \nu } R_{AN}^{2} } \right)} \\
 \end{array}\qquad \text{(eqn:248)}

$$

其中 $Z_{A}$ 是原子核 $A$ 的核电荷，$\vec{{R} }_{AN}$
是大小为 $R_{AN}$、由原子核 $A$ 指向原子核 $N$ 的矢量。
$\mathrm{\mathbf{P} }$ 是一阶密度矩阵。

## 基本用法（Basic usage）

计算铁中心的电子密度和四极分裂的示例如下：

```orca
%eprnmr
  nuclei = all Fe {fgrad, rho}
end
```

若采用含紧缩函数的基组（如 CP(PPP)），
可能需要提高铁原子的径向积分精度。
从 ORCA 5.0 起，网格构建时已考虑这一点，默认设置通常工作得很好。
但对于非常棘手的情况，
可通过控制 `%METHOD` 下的 `SPECIALGRIDINTACC` 标志来提高精度
（详见 [sec:essentialelements.numericalintegration.radgrid](#sec:essentialelements.numericalintegration.radgrid) 一节）。

输出文件应包含以下几行，
由此可直接得到计算的四极分裂和 RHO(0) 值（铁核处的电子密度）。
要获得同质异能移，需将 RHO(0) 值代入相应的线性方程
（式 [Eq](#eqn:MB_isomer_shift)）。

```orca
Moessbauer quadrupole splitting parameter (proper coordinate system)
e**2qQ  = -0.406 MHz = -0.035 mm/s
eta     = 0.871
Delta-EQ=(1/2{e**2qQ}*sqrt(1+1/3*eta**2) = -0.227 MHz = -0.020 mm/s
RHO(0)=  11581.352209571 a.u.**-3   # the electron density at the Fe nucleus.
```

!!! note
    -   按照同样的步骤，也可用 CASSCF 波函数计算穆斯堡尔参数。
        若是态平均 CASSCF（state-averaged CASSCF）计算，
        后续穆斯堡尔计算中使用的是平均密度。

## 关键词（Keywords）

分子中给定原子核关联的所有性质（NMR 屏蔽、超精细耦合、四极耦合）
共享一套通用的输入语法。
该语法由两部分组成：一个选择（selection，即你想要处理的原子核）
和花括号内的一系列动作（actions，即你希望程序对这些原子核执行的操作）。
eprnmr 模块的完整关键词列表见
[sec:spectroscopyproperties.properties.eprnmr](#sec:spectroscopyproperties.properties.eprnmr)。
下面用一个例子来说明最为清楚。以下输入

```orca
%eprnmr
  nuclei = all O { aiso, adip, fgrad, shift, ist=17 }
end
```

将选择分子中所有氧原子，挑选 $^{17}$O 同位素，
并请求为它们计算各向同性 + 自旋-偶极超精细耦合、电场梯度和 NMR 屏蔽。

!!! note
    写在同一行上的所有原子核都会被赋予相同的同位素质量（以及其他参数）！

<a id="tab:spectroscopyproperties.moessbauer.keywords.block"></a>
!!! note "与穆斯堡尔计算相关的 `%eprnmr` 块输入关键词"
    :header-rows: 1
    :class: longtable
    :class: footnotesize

| 项目 | 内容 |
| --- | --- |
| **关键词** | 无 |

      - 选择
      - 执行动作
      - 说明

| 项目 | 内容 |
| --- | --- |
| **`nuclei`** | 无 |

      - `all <type>`
      - 
      - 选择元素 `<type>` 的所有原子核

| 项目 | 内容 |
| --- | --- |
| **—** | 无 |

      - `i1,i2,i3...`
      - 
      - 选择原子 `i1`、`i2`、`i3`……（从 1 开始计数！）

| 项目 | 内容 |
| --- | --- |
| **—** | 无 |

      - `{ rho }`
      - 为所选原子核计算核处电子密度

| 项目 | 内容 |
| --- | --- |
| **—** | 无 |

      - `{ fgrad }`
      - 为所选原子核计算 EFG

| 项目 | 内容 |
| --- | --- |
| **—** | 无 |

      - `{ ist=<N> }`
      - 为所选原子核选择同位素 `<N>`

| 项目 | 内容 |
| --- | --- |
| **—** | 无 |

      - `{ QQQ=<N> }`
      - 将所选原子核的四极矩设为 `<N>`

| 项目 | 内容 |
| --- | --- |
| **—** | 无 |

      - `{ III=<N> }`
      - 将所选原子核的核自旋设为 `<N>`

| 项目 | 内容 |
| --- | --- |
| **—** | 无 |

      - `{ fgrad, rho, ist=57 }`
      - 为所选原子核同时请求多个动作的示例

