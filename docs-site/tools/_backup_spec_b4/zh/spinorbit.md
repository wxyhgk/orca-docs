

<a id="sec:spectroscopyproperties.soc"></a>
# 自旋-轨道耦合算符（The Spin-Orbit Coupling Operator）

可用于性质计算的自旋-轨道耦合（spin-orbit coupling，SOC）算符有若干变体 [neese2005jchemphys](../../bibliography.md)。
它们基于有效势（effective potential）和平均场（mean-field）方法，
并通过 `%rel` 块可选择各种参数。
请注意，SOMF 算符依赖于密度矩阵，
因此算符本身在例如 CASSCF 与 MRCI 计算之间可能不同。

**注意**：默认值在 ORCA 5.0 中略有变化，见下文 `SOCFlags`。

```orca
%rel
     # ---------------------------------------------------
     # SPIN ORBIT COUPLING OPERATORS
     # ---------------------------------------------------
     SOCType 0  # none
             1  # effective nuclear charge
             2  # DEPRECATED
             3  # mean-field/effective potential (default)
             4  # DEPRECATED
     # ---------------------------------------------------
     # Flags for construction of potential; operative
     # only for SOCType 3.
     # ---------------------------------------------------
     SOCFlags 1,4,3,0 # default if nothing is specified
                      # 1,3,3,0 default if RI is applied and AuxJ available
                      # e.g. when using !RIJCOSX (default for DFT) or !RIJONX     
     # Flag 1 = 0 - do not include 1-electron terms
     #        = 1 - do include 1-electron terms
     # Flag 2 = 0 - do not include Coulomb terms
     #        = 1 - compute Coulomb terms fully numeric
     #        = 2 - compute Coulomb term seminumeric
     #        = 3 - compute Coulomb term with RI approx
     #        = 4 - compute Coulomb term exactly
     # Flag 3 = 0 - do not include exchange terms
     #        = 1 - do include local X-alpha exchange
     #              the X-Alpha parameter can be chosen via
     #              % rel Xalpha 0.7 (default)
     #        = 2 - same as 1 but with sign reversed
     #        = 3 - exchange via one-center exact
     #              integrals including the spin-other
     #              orbit interaction
     #        = 4 - all exchange terms full analytic
     #              (this is expensive)
     # Flag 4 = 0 - do not include DFT local correlation
     #              terms
     #        = 1 - do include local DFT correlation (here
     #              this is done with VWN5)
     #
     SOCMaxCenter 4 # max. number of centers to include in
                    # the integrals (not fully consistently
                    # implemented yet; better leave equal to 4)
     #  The following simple input equivalents can also be used:
     #  SOMF(1X)      = SOCType 3, SOCFlags 1,2,3,0 and SOCMaxCenter 4
     #  RI-SOMF(1X)   = SOCType 3, SOCFlags 1,3,3,0 and SOCMaxCenter 4
     #  VEFF-SOC      = SOCType 3, SOCFlags 1,3,1,1 and SOCMaxCenter 4
     #  VEFF(-2X)-SOC = SOCType 3, SOCFlags 1,3,2,1 and SOCMaxCenter 4
     #  AMFI          = SOCType 3, SOCFlags 1,4,3,0 and SOCMaxCenter 1
     #  NOTE: If you choose the RI option you need to specify an auxiliary basis
     #        set even if the underlying SCF calculation does not make use of any
     #        from of RI!
     # -----------------------------------------------
     # For the effective nuclear charge SOC operator
     # the nuclear charges can be adjusted.
     # -----------------------------------------------
     Zeff[26] 0.0   # set the effective nuclear charge
                    # of iron (Z = 26) to zero
     # -----------------------------------------------
     # Neglecting SOC contributions from particular
     # atoms
     # -----------------------------------------------
     SOCOff 0,5     # turn off the SOC for atoms 0 and 5
                    # this makes sense if the SOC operator
                    # has only one center contributions
                    # (e.g. effective nuclear charge)
```

简单输入等价形式列于 [tab:spectroscopyproperties.soc.keywords.simple](#tab:spectroscopyproperties.soc.keywords.simple)，
更详细的说明见 [neese2005jchemphys](../../bibliography.md)。
关于（已弃用的）AMFI-A 方法（使用预先计算的原子密度）的更多细节见 [ganyushin2013jcp](../../bibliography.md)。

Breit-Pauli 自旋-轨道耦合算符为：

$$

\hat{{H} }_{\text{SOC} } =\hat{{H} }_{\text{SOC} }^{\left( 1 \right)}
+\hat{{H} }_{\text{SOC} }^{\left( 2 \right)}

$$

其中单电子和双电子贡献分别为

$$

\hat{{H} }_{\text{SOC} }^{\left( 1 \right)} =\frac{\alpha^{2} }{2}\sum\limits_i
{\sum\limits_A { Z_{A} \frac{\left({ \mathrm{\mathbf{r} }_{i} -\mathrm{\mathbf{R} }_{A} } \right)\times \mathrm{\mathbf{p} }_{i} }{\left|{ \mathrm{\mathbf{r} }_{i} -\mathrm{\mathbf{R} }_{A} } \right|^{3} }\hat{{s} }_{i} } } \equiv \frac{\alpha
^{2} }{2}\sum\limits_i { \sum\limits_A { Z_{A} r_{iA}^{-3} { \mathrm{\mathbf{ \hat{l} }} }_{iA} \mathrm{\mathbf{\hat{{s} }} }_{i} } }\qquad \text{(eqn:240)}

$$

$$

\hat{{H} }_{\text{SOC} }^{\left( 2 \right)} =-\frac{\alpha^{2} }{2}\sum\limits_i
{\sum\limits_{j\ne i} { \frac{\left({ \mathrm{\mathbf{r} }_{i} -\mathrm{\mathbf{r} }_{j} } \right)\times \mathrm{\mathbf{p} }_{i} }{\left|{ \mathrm{\mathbf{r} }_{i} -\mathrm{\mathbf{r} }_{j} } \right|^{3} }\left({ \mathrm{\mathbf{\hat{{s} }} }_{i}
+2{\mathrm{\mathbf{\hat{s} }} }_{j} } \right)} }\qquad \text{(eqn:241)}

$$

$$

\hspace{2cm}
\equiv -\frac{\alpha^{2} }{2}\sum\limits_i
{\sum\limits_{j\ne i} { \mathrm{\mathbf{\hat{{l} }} }_{ij} r_{ij}^{-3} \left({\mathrm{\mathbf{\hat{{s} }} }_{i} +2\mathrm{\mathbf{\hat{{s} }} }_{j} } \right)} }\qquad \text{(eqn242)}

$$

!!! note
    一种很有吸引力的可能是用 Hess 等人发展的
    自旋-轨道平均场（spin-orbit mean-field，SOMF）方法来表示 SOC，[hess1996cpl](../../bibliography.md)
    该方法在 Schimmelpfennig 的 AMFI 程序中被广泛使用 [schimmelpfennigAMFIprog](../../bibliography.md)，
    并由 Berning 等人 [berning2000molphys](../../bibliography.md)
    以及文献 [neese2005jchemphys](../../bibliography.md) 作了详细讨论。
    在（正交归一）单电子基下，SOMF 算符的矩阵元为：

    $$

\begin{array}{c}
     h_{rs}^{K;\text{SOC} } =\left({ p\left|{ \hat{{h} }_{K}^{1el-\text{SOC} } } \right|q}
    \right) \\
     +\sum\limits_{rs} { P_{rs} } \left[{ \left({ pq\left|{ \hat{{g} }_{K}^{\text{SOC} } }
    \right|rs} \right)-\frac{3}{2}\left({ pr\left|{ \hat{{g} }_{K}^{\text{SOC} } }
    \right|sq} \right)-\frac{3}{2}\left({ sq\left|{ \hat{{g} }_{K}^{\text{SOC} } }
    \right|pr} \right)} \right] \\
     \end{array}\qquad \text{(eqn:257)}

$$

    且：

    $$

\hat{{h} }_{k}^{1el-\text{SOC} } \left({ \mathrm{\mathbf{r} }_{i} } \right)=\frac{\alpha
    ^{2} }{2}\sum\limits_i { \sum\limits_A { Z_{A} r_{iA}^{-3} { \mathrm{\mathbf{\hat{l} }} }_{iA;k} } }\qquad \text{(eqn:258)}

$$

    $$

\hat{{g} }_{k}^{\text{SOC} } \left({ \mathrm{\mathbf{r} }_{i,} \mathrm{\mathbf{r} }_{j} }
    \right)=-\frac{\alpha^{2} }{2}\mathrm{\mathbf{\hat{{l} }} }_{ij;k} r_{ij}^{-3}\qquad \text{(eqn:259)}

$$

    $\mathrm{\mathbf{\hat{l} }}_{iA} =(\mathrm{\mathbf{\hat{r} }}_{i} -\mathrm{\mathbf{R} }_{A}
    )\times \mathrm{\mathbf{\hat{p} }}_{i}$ 是第 $i$ 个电子相对于原子核 $A$ 的角动量。
    大小为 $r_{iA}$ 的矢量
    $\mathrm{\mathbf{\hat{r} }}_{iA} ={\mathrm{\mathbf{\hat{r} }} }_{i} -\mathrm{\mathbf{R} }_{A}$
    是第 $i$ 个电子相对于原子 $A$ 的位置。
    类似地，大小为 $r_{ij}$ 的矢量
    ${\mathrm{\mathbf{\hat{r} }} }_{ij} =\mathrm{\mathbf{\hat{r} }}_{i} -\mathrm{\mathbf{\hat{r} }}_{j}$
    是第 $i$ 个电子相对于电子 $j$ 的位置，
    而
    $\mathrm{\mathbf{\hat{l} }}_{ij} =(\mathrm{\mathbf{\hat{r} }}_{i}
    -\mathrm{\mathbf{\hat{r} }}_{j} )\times \mathrm{\mathbf{\hat{p} }}_{i}$
    是它相对于该电子的角动量。**P** 是电子基态的电荷密度矩阵
    （$P_{pq} =\left\langle { 0SS\left|{E_{q}^{p} } \right|0SS} \right\rangle$，
    其中 $E_{q}^{p} =a_{p\beta }^{+}
    a_{q\beta } +a_{p\alpha }^{+} a_{q\alpha }$，而 $a_{p\sigma }^{+}$ 和
    $a_{q\sigma }$ 是通常的费米子产生和湮灭算符）。

该算符很难精确处理；因此通常引入平均场和/或有效势方法，
将算符写成有效单电子算符：

$$

\hat{{H} }_{\text{SOC} } \cong \sum\limits_i { \mathrm{\mathbf{\hat{{h} }} }_{i}^{\left({\text{eff} } \right)} \mathrm{\mathbf{\hat{{s} }} }_{i} }\qquad \text{(eqn:243)}

$$

最简单的近似是只用单电子部分，
并把核电荷视为可调参数。
将它们的值从精确核电荷减小，
被认为是以平均方式考虑了电子对核电荷的屏蔽。
在我们的代码中使用 Koseki 等人的有效核电荷
（[schmidt1992phys,koseki1995phys,koseki1998phys](../../bibliography.md)）。
该近似引入的误差通常小于 10%，但有时更大，
在某些情况下可能接近 20%。
该近似对第一周期主族元素和第一过渡系（2p 和 3d 元素）效果最好。
对较重元素则变得不可靠。

好得多的近似是精确考虑双电子项。
这里不展开细节——情形与 Hartree-Fock（或密度泛函）理论相同，
会得到库仑项、交换项和相关项。
相关项（以局域 DFT 方式评估）可忽略，可以安全地略去。
它们可选地被包含，且计算代价不高。
库仑项是（在单电子项之后）第二大的贡献，
精确评估代价昂贵。情形是这样的：
在库仑部分中，自旋-他轨（spin-other-orbit）相互作用
（双电子部分中的第二项）没有贡献，
只需处理自旋-自轨（spin-own-orbit）贡献。
精确评估通常太昂贵。
RI 和半数值近似效率高得多，且只引入极小的误差
（例如 g 张量计算中通常不超过 1 ppm 量级），
因此推荐使用。RI 近似在计算上更高效。
请注意，要利用 RI 近似，必须指定辅助基组，
即使前面的 SCF 计算没有使用任何形式的 RI。
对库仑项采用单中心近似会引入大得多的误差。
全数值方法既慢又不准确，不推荐使用。

交换项同时有自旋-自轨和自旋-他轨相互作用的贡献。
在平均场近似中这两者都被考虑在内，
通过 `Flag 3 = 3` 访问。
这里单中心近似比库仑项好得多，
因为积分和密度矩阵元都是短程的。
与库仑项一起，这给出一个非常准确的 SOC 算符，值得推荐。
DFT-Veff 算符的不足在于交换中未处理自旋-他轨部分，
这会产生显著误差（另外，局域 DFT 相对 HF
低估自旋-自轨相互作用的交换贡献约 10%，
但这并非主要误差来源）。
然而，值得注意的是，在 SOMF 箢符的精确解析评估中，
自旋-他轨相互作用恰好是自旋-自轨相互作用的 -2 倍。
因此，在 DFT 框架下，只需简单反转 DFT 交换项的符号，
就能得到一个好*得多*的 SOC 箢符！这通过 `Flag 3 = 2` 访问。

## 排除原子中心（Exclusion of Atomic Centers）

在 ORCA 中可以修改自旋-轨道耦合算符，
以排除用户指定原子的贡献。
这种方法可用来，例如，定量配体对零场分裂（zero-field splitting，ZFS）的贡献；
该方法的一个应用见文献 [suturina2015inorgchem](../../bibliography.md)。

下面以三重态氧分子 ZFS 的 SOC 贡献计算为例加以说明。
使用下面的输入，我们先进行一次包含两个氧原子的正常 ZFS 计算。
请注意，这里我们使用有效核电荷算符。
这是必须的，因为并非所有已实现的 SOC 算符都兼容按单个中心贡献的分解。

```orca
%rel
     # ---------------------------------------------------
     # SPIN ORBIT COUPLING OPERATORS
     # ---------------------------------------------------
     SOCType 0  # none
             1  # effective nuclear charge
             2  # DEPRECATED
             3  # mean-field/effective potential (default)
             4  # DEPRECATED
     # ---------------------------------------------------
     # Flags for construction of potential; operative
     # only for SOCType 3.
     # ---------------------------------------------------
     SOCFlags 1,4,3,0 # default if nothing is specified
                      # 1,3,3,0 default if RI is applied and AuxJ available
                      # e.g. when using !RIJCOSX (default for DFT) or !RIJONX     
     # Flag 1 = 0 - do not include 1-electron terms
     #        = 1 - do include 1-electron terms
     # Flag 2 = 0 - do not include Coulomb terms
     #        = 1 - compute Coulomb terms fully numeric
     #        = 2 - compute Coulomb term seminumeric
     #        = 3 - compute Coulomb term with RI approx
     #        = 4 - compute Coulomb term exactly
     # Flag 3 = 0 - do not include exchange terms
     #        = 1 - do include local X-alpha exchange
     #              the X-Alpha parameter can be chosen via
     #              % rel Xalpha 0.7 (default)
     #        = 2 - same as 1 but with sign reversed
     #        = 3 - exchange via one-center exact
     #              integrals including the spin-other
     #              orbit interaction
     #        = 4 - all exchange terms full analytic
     #              (this is expensive)
     # Flag 4 = 0 - do not include DFT local correlation
     #              terms
     #        = 1 - do include local DFT correlation (here
     #              this is done with VWN5)
     #
     SOCMaxCenter 4 # max. number of centers to include in
                    # the integrals (not fully consistently
                    # implemented yet; better leave equal to 4)
     #  The following simple input equivalents can also be used:
     #  SOMF(1X)      = SOCType 3, SOCFlags 1,2,3,0 and SOCMaxCenter 4
     #  RI-SOMF(1X)   = SOCType 3, SOCFlags 1,3,3,0 and SOCMaxCenter 4
     #  VEFF-SOC      = SOCType 3, SOCFlags 1,3,1,1 and SOCMaxCenter 4
     #  VEFF(-2X)-SOC = SOCType 3, SOCFlags 1,3,2,1 and SOCMaxCenter 4
     #  AMFI          = SOCType 3, SOCFlags 1,4,3,0 and SOCMaxCenter 1
     #  NOTE: If you choose the RI option you need to specify an auxiliary basis
     #        set even if the underlying SCF calculation does not make use of any
     #        from of RI!
     # -----------------------------------------------
     # For the effective nuclear charge SOC operator
     # the nuclear charges can be adjusted.
     # -----------------------------------------------
     Zeff[26] 0.0   # set the effective nuclear charge
                    # of iron (Z = 26) to zero
     # -----------------------------------------------
     # Neglecting SOC contributions from particular
     # atoms
     # -----------------------------------------------
     SOCOff 0,5     # turn off the SOC for atoms 0 and 5
                    # this makes sense if the SOC operator
                    # has only one center contributions
                    # (e.g. effective nuclear charge)
```

计算得到的 D 参数约为 2.573 cm$^{-1}$。
在第二次计算中，我们排除第一个氧原子的贡献。
为此将 `%rel` 块改为下面的形式。

```orca
%rel
    SOCType 1
    SOCOff 0
    end
```

现在计算得到的 D 参数约为 0.643 cm$^{-1}$，
该结果与先前计算值的一半偏差相当大，
表明非可加效应很重要。
除有效核电荷算符外，也可使用前面描述的 AMFI-A 算符。
鉴于它基于预先计算的原子密度，
对于有效核电荷算符变得不可靠的较重元素，它可能更可取。
该方法不限于上述 CASSCF 计算，
也可用于 DFT、MRCI 和 ROCIS 计算。

<a id="sec:spectroscopyproperties.soc.keywords"></a>
## 简单输入关键词（Simple Input Keywords）

<a id="tab:spectroscopyproperties.soc.keywords.simple"></a>
!!! note "用于选择 SOC 算符处理方式的简单输入关键词及其等价的 `%rel` 块设置"
    :header-rows: 1
    :class: footnotesize

| 项目 | 内容 |
| --- | --- |
| **关键词** | 无 |

      - `SOCType`
      - `SOCFlags`
      - `SOCMaxCenter`

| 项目 | 内容 |
| --- | --- |
| **`ZEFF-SOC`** | 无 |

      - 1
      -
      -

| 项目 | 内容 |
| --- | --- |
| **`SOMF`** | 无 |

      - 3
      - 1,4,4,0
      - 4

| 项目 | 内容 |
| --- | --- |
| **`SOMF(1X)`** | 无 |

      - 3
      - 1,2,3,0
      - 4

| 项目 | 内容 |
| --- | --- |
| **`RI-SOMF`** | 无 |

      - 3
      - 1,3,3,0 
      - 4

| 项目 | 内容 |
| --- | --- |
| **`RI-SOMF(1X)`** | 无 |

      - 3
      - 1,3,3,0 
      - 4

| 项目 | 内容 |
| --- | --- |
| **`SOMF(4X)`** | 无 |

      - 3
      - 1,2,4,0
      - 4

| 项目 | 内容 |
| --- | --- |
| **`RI-SOMF(4X)`** | 无 |

      - 3
      - 1,3,4,0
      - 4

| 项目 | 内容 |
| --- | --- |
| **`VEFF-SOC`** | 无 |

      - 3
      - 1,3,1,1
      - 4

| 项目 | 内容 |
| --- | --- |
| **`VEFF(-2X)-SOC`** | 无 |

      - 3
      - 1,3,2,1
      - 4

| 项目 | 内容 |
| --- | --- |
| **`AMFI`** | 无 |

      - 3
      - 1,4,3,0
      - 1

