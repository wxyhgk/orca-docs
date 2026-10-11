

<a id="sec:spectroscopyproperties.mcd"></a>
# （磁）圆二色谱与吸收谱的模拟（Simulation of (Magnetic) Circular Dichroism and Absorption Spectra）

<a id="sec:spectroscopyproperties.mcd.general"></a>
## 程序概述（General description of the program）

ORCA 现已能通过一套通用实现，在所有理论水平上模拟包含自旋-轨道耦合
（spin-orbit coupling）贡献的光谱。
[foglia_mcd_2022](../../bibliography.md)

按照能量损失（energy-loss）方法，态 $\tilde{P}$ 与 $\tilde{Q}$ 之间
跃迁的吸收截面可表示为：

$$
\begin{split}
     \sigma_{\tilde{P}\tilde{Q} } = \frac{4 \pi^2}{c (E_{\tilde{Q} }-E_{\tilde{P} }) } |T_{\tilde{P}\tilde{Q} }|^2,
\end{split}
$$

其中 c 是光速；$E_{\tilde{P} }$ 和 $E_{\tilde{Q} }$
分别是态 ${\tilde{P} }$ 和 ${\tilde{Q} }$ 的能量；
$T_{{\tilde{P} }{\tilde{Q} }}$ 是态 ${\tilde{P} }$ 与 ${\tilde{Q} }$
之间的跃迁矩（transition moment），根据所采用的近似，
它可以用不同的表达式计算。
在光-物质相互作用的偶极近似（dipolar approximation）下，
跃迁矩的形式为：

$$
\begin{split}
     T_{{\tilde{P} }{\tilde{Q} }} =& { \sum_{i=1}^N  \bra{{\tilde{P} }}
     \mathcal{E} \cdot \hat{p }_i
     %
     \ket{{\tilde{Q} }} }, \\
\end{split}
$$

其中求和遍历所有电子 $i$；$\hat{p }_i$ 是线性动量算符；
$\mathcal{E}$ 是入射光的偏振矢量。
为考虑跃迁中所有的电机制和磁机制，
必须使用完整的场-物质相互作用算符
（full field-matter interaction operator，FFMIO）。
对于跃迁矩，这导出式 [Eq](#eqn:exactTM)。

<a id="eqn:exactTM"></a>

$$
\begin{split}
     T_{{\tilde{P} }{\tilde{Q} }} =& \frac{e}{m_e} \sum_{i=1}^N  \bra{{\tilde{P} }}
     \mathcal{E} \cdot \Big[     e^{ik\cdot \hat{r }_i }
     %\hat{r}_i }
     %
     \hat{p }_i \Big]\ket{{\tilde{Q} }}
     %
\end{split}\qquad \text{(eqn:exactTM)}
$$

其中 $\hat{r}_i$ 是第 i 个电子的位置算符，$k$ 是
指向光传播方向的波矢，其大小与波长的关系为 $\lambda = 2 \pi / |k|$。

对于自由转动的分子，需要考虑分子相对于入射光方向的所有可能取向。
在某些情况下（例如偶极近似下线偏振光的吸收），
取向效应可以解析地平均掉。然而，一般仍需对若干选定的分子取向
（在式 [Eq](#eqn:OrientAver) 中标记为 $o$）进行数值积分。

<a id="eqn:OrientAver"></a>

$$
\begin{split}
     <\sigma_{{\tilde{P} }{\tilde{Q} }}> = \sum_o w_o \frac{4 \pi^2}{c (E_{{\tilde{Q} }}(o)-E_{\tilde{P} }(o)) } |T_{{\tilde{P} }{\tilde{Q} }}(o)|^2
\end{split}\qquad \text{(eqn:OrientAver)}
$$

其中 $w_o$ 是该取向在求积中的权重。

该实现旨在计算在外加磁场 B 作用下体系对圆偏振光的吸收。
外磁场通过塞曼微扰（Zeeman perturbation）改变每个取向 $o$ 下的
态 $\tilde{P}$ 和 $\tilde{Q}$。
计算结果以左旋（-）与右旋（+）圆偏振光吸收之差
（$\Delta$f$_{osc}$）以及振子强度之和（f$_{osc}$，对应于线偏振光吸收）给出。
分子取向由三个欧拉角的转动矩阵构建：$\chi$、$\theta$ 和 $\phi$。
其中，$\chi$（在垂直于外磁场/入射光方向的平面内的转角）
被解析积分，而 $\theta$ 和 $\phi$ 则在网格上取值。

最后，态 $\tilde{P}$ 和 $\tilde{Q}$ 由 QDPT 获得：
将这些态按 $\hat{H}_{0}$ 的非相对论本征态（$\{I,J\}$）展开，
展开系数（$d_{I\tilde{Q} }$）由复矩阵的对角化得到。
该矩阵包含 $\hat{H}_{0}$ 以及用 $\{I,J\}$ 表示的 SOC 和塞曼贡献
（若所选电子结构理论已实现 SSC，则也包含 SSC）。

<a id="eqn:mcdqdpt"></a>

$$
\begin{split}
    \bra{\Psi_I^{SM} }\hat{H}_{0}+\hat{H}_{SOC}+\hat{H}_{Zeeman}\ket{\Psi_J^{S'M'} }= \delta_{IJ}\delta_{SS'}\delta_{MM'}E_I^S +  \bra{\Psi_I^{SM} }\hat{H}_{SOC}+\hat{H}_{Zeeman}\ket{\Psi_J^{S'M'} }
\end{split}\qquad \text{(eqn:mcdqdpt)}
$$

<a id="sec:spectroscopyproperties.mcd.example"></a>
## 在 TDDFT 模块中运行与分析 MCD 计算

计算磁圆二色谱（Magnetic Circular Dichroism，MCD）的最小输入
需要将关键词 DoMCD 设为 true，
并为外磁场 B 指定强度（单位为高斯 Gauss）。
TD-DFT 模块的示例输入如下：

```mol
title: structure 1
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
9
structure (0 1)
O  0.24287127056830 0.00033994295362 0.29479344369591
C  0.13113617562040 0.00013705972874 1.65093880501262
C  1.35780003491446 -0.00017874911331 2.22574232397512
C  2.30247996517358 -0.00017814489451 1.14947275232337
C  1.57300244613625 0.00013652073221 0.00793218434497
H  -0.86951534119903 0.00025858475406 2.04160438459058
H  1.56899490845286 -0.00038874637444 3.28047030533440
H  3.37570289422870 -0.00038632501973 1.22171814100713
H  1.83015664610447 0.00025985723335 -1.03506234028415
--- input ---
! B3LYP def2-QZVPP

%tddft
    TDA False
    NROOTS 10
    DoSOC True
    DoMCD True
    B 50000.0
end

*xyz 0 1
 O     0.24287127056830      0.00033994295362      0.29479344369591
 C     0.13113617562040      0.00013705972874      1.65093880501262
 C     1.35780003491446     -0.00017874911331      2.22574232397512
 C     2.30247996517358     -0.00017814489451      1.14947275232337
 C     1.57300244613625      0.00013652073221      0.00793218434497
 H    -0.86951534119903      0.00025858475406      2.04160438459058
 H     1.56899490845286     -0.00038874637444      3.28047030533440
 H     3.37570289422870     -0.00038632501973      1.22171814100713
 H     1.83015664610447      0.00025985723335     -1.03506234028415
*
```

在该作业的输出文件中，给出了估算的振子强度（f$_{osc}$）
以及左旋与右旋圆偏振光吸收之差（$\Delta$f$_{osc}$）：

```orca
------------------------------------------------------------------------------
           MCD Transitions via transition electric dipole moments
                B =  50000.00 Gauss  T =   300.000 K
------------------------------------------------------------------------------

                   dfosc             fosc           dfosc/fosc

 0 -> 1       -0.0000000000       0.0000000003      -0.0663180503
 0 -> 2        0.0000000000       0.0000000005       0.0000209714
 0 -> 3        0.0000000000       0.0000000003       0.0661609417
 0 -> 4       -0.0000000001       0.0000000004      -0.2991916107
 0 -> 5       -0.0000000000       0.0000000006      -0.0009270335
 0 -> 6        0.0000000001       0.0000000004       0.2984154405
 0 -> 7        0.0000000003       0.0000000008       0.3721777693
 0 -> 8       -0.0000000000       0.0000000009      -0.0002960328
 0 -> 9       -0.0000000003       0.0000000008      -0.3689867758
 0 ->10       -0.0000050986       0.1741092913      -0.0000292840
```

当态的能量顺序随分子与外磁场相对取向的改变而变化时，
这些结果可能不准确。
要获得准确结果，必须用 `orca_mapspc` 程序对所有取向执行
后处理步骤，该程序将结果保存在扩展名为
`.cis-el.dipole-length.1.mcd` 的文件中：

```orca
orca_mapspc fur-mcd.cis-el.exact.1.mcd MCD -x050000 -x155000 -n10000 -w2000
```

在本例中，我们生成 50000 至 55000 cm$^{-1}$ 之间的谱图（M$^{-1}$）
（-x050000 -x155000），使用 10000 个点（-n10000），
并采用半高全宽为 2000 cm$^{-1}$ 的归一化高斯展宽函数（-w2000）。

通过为 B 设置多个数值，可在一次运行中执行多个 MCD 计算。
跃迁矩也可通过 ED 速度表式（velocity formulation）和 FFMIO 算符获得，
只需分别将关键词 `DoDipoleVelocity` 和 `DoFullSemiClassical` 设为 true：

```orca
------------------------------------------------------------------------------
           MCD Transitions via transition electric dipole moments
                B =  50000.00 Gauss  T =   300.000 K
------------------------------------------------------------------------------

                   dfosc             fosc           dfosc/fosc

 0 -> 1       -0.0000000000       0.0000000003      -0.0663180503
 0 -> 2        0.0000000000       0.0000000005       0.0000209714
 0 -> 3        0.0000000000       0.0000000003       0.0661609417
 0 -> 4       -0.0000000001       0.0000000004      -0.2991916107
 0 -> 5       -0.0000000000       0.0000000006      -0.0009270335
 0 -> 6        0.0000000001       0.0000000004       0.2984154405
 0 -> 7        0.0000000003       0.0000000008       0.3721777693
 0 -> 8       -0.0000000000       0.0000000009      -0.0002960328
 0 -> 9       -0.0000000003       0.0000000008      -0.3689867758
 0 ->10       -0.0000050986       0.1741092913      -0.0000292840
```

对于每种设置，结果在输出文件中分别打印：

```orca
------------------------------------------------------------------------------
           MCD Transitions via transition electric dipole moments
                B =  50000.00 Gauss  T =   300.000 K
------------------------------------------------------------------------------

                   dfosc              fosc            dfosc/fosc

 0 -> 1       -0.0000000000       0.0000000003      -0.0663180503
 .
 .
 .
 ------------------------------------------------------------------------------
           MCD Transitions via transition velocity dipole moments
                B =  50000.00 Gauss  T =   300.000 K
------------------------------------------------------------------------------

                   dfosc              fosc            dfosc/fosc

 0 -> 1       -0.0000000001       0.0000000013      -0.0477214281
.
.
.

------------------------------------------------------------------------------
           MCD Transitions via full Semi-classical formulation
                B =  50000.00 Gauss  T =   300.000 K
------------------------------------------------------------------------------

                   dfosc              fosc            dfosc/fosc

 0 -> 1       -0.0000000001       0.0000000016      -0.0731029604
.
.
.
```

后处理结果保存在扩展名为 `.cis-el.dipole-length.1.mcd`、
`.cis-el.dipole-vel.1.mcd` 和 `.cis-el.exact.1.mcd` 的文件中。

$NOTE:$ 值得强调的是，计算得到的 $\Delta$f$_{osc}$ 值
对应于所选跃迁矩下左旋与右旋圆偏振光吸收之差。
在两种 ED 近似下，$\Delta$f$_{osc}$ 对应于 MCD 信号。
当请求 FFMIO 时，得到的是天然圆二色（natural circular dichroism）
与磁诱导圆二色（magnetic-induced circular dichroism）之和。
若要在 FFMIO 方案下仅获得 MCD 谱，
需将 B 设为 0.0 以扣除天然圆二色。

<a id="sec:spectroscopyproperties.mcd.modules"></a>
## 在其他模块中运行 MCD 计算

MCD 实现也可用于其他模块，如
STEOM-CCSD、CAS、ROCIS 和 MRCI（见下文给出的输入文件示例），
所用关键词与 TDDFT 模块中所述相同。

```orca
%mrci
     DoDipoleLength true
     DoDipoleVelocity true
     DoFullSemiClassical true
     Soc
          DoSoc true
          DoMCD true
          B 50000.0
     end
end
```

```orca
%casscf
     DoDipoleLength true
     DoDipoleVelocity true
     DoFullSemiClassical true
     rel 
          DoSoc true
          DoMCD true
          B 50000.0
     end
end
```

```orca
%rocis
  DoDipoleLength true
  DoDipoleVelocity true
  DoFullSemiClassical true
  rel
   DoSOC true
   DoMCD true
   B 50000.0
  end
end
```

```orca
%mdci
     DoSOC true
     DoMCD true
     DoDipoleLength true
     DoDipoleVelocity true
     B 50000.0
end
```

必须牢记，MCD 的计算依赖于对跃迁矩和角动量的正确描述
（角动量用于计算塞曼微扰）。
因此，选择合适的电子结构方法是用户的责任。

<a id="sec:spectroscopyproperties.mcd.keywordlist"></a>
## 相关关键词列表（List of related keywords）

```orca
%selected module
  DoMCD false         # Enables the use of the MCD module
  DoDipoleVelocity true # Use the electric dipolar velocity formulation 
                        # for the light-matter interaction
  DoFullSemiClassical false  # Use the full semiclasical ligth-matter
                             # interaction transition moments
  MCDGridtype 1      # Grid for the molecular orientational average
                            # 1 = Lebedev grid (default)
                            # 2 = Regular grid
  MCDLebedev 14    # Number of points if Lebedev grid is selected
                   # 6, 12, 14(default), 26, 50, 110, 194, 302, 434, 590, 770
  NPOINTSPHI 10    # Number of points for phi angle if regular grid is selected
  NPOINTSTHETA 10  # Number of points for theta angle if regular grid is selected
  B 3000.0          # Magnetic field in Gauss
  Temperature 300.0 # Self-explanatory. One temperature must be defined 
                    # for each B value 
end
```
