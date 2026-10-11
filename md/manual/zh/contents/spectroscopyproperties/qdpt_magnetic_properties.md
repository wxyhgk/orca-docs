```{index} QDPT, Magnetic Properties via QDPT
```

(sec:spectroscopyproperties.qdpt_magnetic_properties)=
# 通过准简并微扰理论计算磁性质（Magnetic Properties Through Quasi Degenerate Perturbation Theory）

(sec:spectroscopyproperties.qdpt_magnetic_properties.general)=
## 准简并微扰理论（QDPT）简介

准简并微扰理论（Quasi Degenerate Perturbation Theory，QDPT）
为几乎所有基于波函数的激发态方法的多种磁性质
提供了一种通用且准确的途径。

简言之，在非相对论极限下，
对任何单参考或多参考的激发态波函数方法
（以 CASSCF、MRCI 或 ROCIS 型的零级波函数为基础），
都可以建立一个激发问题，
它是零级波函数与激发的自旋适配组态状态函数
（configuration state functions，CSF）$\left| \Phi_{\mu}^{SS} \right \rangle$ 的组合。

其形式为：

$$\left| \Psi_{I}^{SS} \right\rangle= \sum\nolimits_{\mu} { C_{\mu l} \left| \Phi_{\mu}^{SS} \right \rangle }
$$ (eqn:H_BO)

这里上标 $SS$ 表示自旋量子数为 $S$、
自旋投影 $M_{S} = S$ 的波函数。
由于 BO 哈密顿量不含任何复值算符，
解 $\left| \Psi_{I}^{SS}\right\rangle$ 可取为实值。

求解上述本征值问题可给出 CSF 进入所选波函数的系数，
以及无自旋算符的本征态。
这些本征态可通过建立相应的准简并本征值问题
来向相对论本征态展开。
事实上，自旋-轨道耦合（SOC）和自旋-自旋耦合（SSC）效应
连同塞曼相互作用都可以通过准简并微扰理论（QDPT）纳入。
在这一途径中，SOC、SSC 和塞曼算符
在预先选定的 BO 哈密顿量解 $\left\{{ \Psi_{I}^{SM} }\right\}$ 的基下计算。


$$\left\langle { \Psi_{I}^{SM} \left|{ \hat{{H} }_{\text{BO} } +\hat{{H} }_{\text{SOC} }
+\hat{{H} }_{\text{SSC} } +\hat{{H} }_{\text{Z} } } \right|\Psi_{J}^{{S}'{M}'} }
\right\rangle=\delta_{IJ} \delta_{S{S}'} \delta_{M{M}'} E_{I}^{\left( S
\right)} +\left\langle { \Psi_{I}^{SM} \left|{ \hat{{H} }_{\text{SOC} }
+\hat{{H} }_{\text{SSC} } +\hat{{H} }_{\text{Z} } } \right|\Psi_{J}^{{S}'{M}'} }
\right\rangle$$ (eqn:H_QDPT)

该矩阵的对角化给出耦合态的能级和本征矢。
这些本征矢实际上是 $\hat{{H} }_{\text{BO} }$ 的解
以复系数构成的线性组合。

二次量子化形式的有效单电子 SOC 算符可写为 {cite}`neese2005jchemphys`：

$$\hat{{H} }_{\text{SOMF} } =\frac{1}{2}\sum\limits_{pq} { z_{pq}^{-}
\hat{{a} }_{p}^{\uparrow } \hat{{b} }_{q} +z_{pq}^{+} \hat{{b} }_{p}^{\uparrow }
\hat{{a} }_{q} +z_{pq}^{0} \left[{ \hat{{a} }_{p}^{\uparrow } \hat{{a} }_{q}
-\hat{{b} }_{p}^{\uparrow } \hat{{b} }_{q} } \right]}
$$ (eqn:H_SOMF)

其中，$\hat{{a} }_{p}^{\uparrow }$ 和 $\hat{{b} }_{p}^{\uparrow }$
分别表示 $\alpha$ 和 $\beta$ 电子的产生；
$\hat{{a} }_{p}$ 和 $\hat{{b} }_{p}$ 表示相应的湮灭算符。
矩阵元
$z_{pq}^{-} = z_{pq}^{x} - iz_{pq}^{y}$、$z_{pq}^{+}
= z_{pq}^{x} + iz_{pq}^{y}$ 以及 $z_{pq}^{0} = z_{pq}^{z}$
（上标 $x$、$y$、$z$ 表示笛卡尔分量）
由 {ref}`sec:spectroscopyproperties.epr.D` 一节所述的矩阵元构建。

在这一框架下，SOC 哈密顿量为：

$$\left\langle {{\Psi}_I^{SM}\left|{ \hat{{H} }_{\text{SOC} } } \right|{\Psi}_J^{S^\prime M^\prime}} \right\rangle=
\sum_{m=0,\pm1}\left(-1\right) \left( \begin{matrix}S^\prime&1\\M^\prime&m\\\end{matrix} \left|{\begin{matrix}
S\\
M\\
\end{matrix} } \right. \right)
\underset{Y_{II^\prime}^{SS^\prime}(m)}{\underbrace{\left\langle {{\Psi}_I^{SS}||H_{-m}^{SOC}||{\Psi}_J^{SS}} \right\rangle}}
$$(eqn:H_SOC)


其中 $m$ 代表标准矢量算符分量。
$\left( \begin{matrix}S^\prime&1\\M^\prime&m\\\end{matrix} \left|{\begin{matrix}
S\\
M\\
\end{matrix} } \right. \right)$ 是 Clebsch–Gordon 系数，
它是一个有表可查的确定数值。
它满足一定的选择定则，并包含 SOC 矩阵元对 M 的全部依赖关系。
量 $Y_{II^\prime}^{SS^\prime}(m)$ 是约化矩阵元。
它只依赖于所涉及两个态的标准分量。
$Y_{II^\prime}^{SS^\prime}(m)$ 只有三种非零情形，
来自总自旋相同或相差一个单位的态对。{cite}`neese1998inorgchem`

SSC 哈密顿量为：

$$\hat{{H} }_{\text{SSC} } =-\frac{3g_{e}^{2} \alpha^{2} }{8}\sum\limits_{i\ne j}
{\sum\limits_{m=0,\pm 1,\pm 2} { \frac{\left({ -1} \right)^{m} }{r_{ij}^{5}
} } \left[{ \mathrm{\mathbf{r} }_{ij} \times \mathrm{\mathbf{r} }_{ij} }
\right]_{-m}^{\left( 2 \right)} \left[{ \mathrm{\mathbf{S} }\left( i \right)\times
\mathrm{\mathbf{S} }\left( j \right)} \right]}_{m}^{\left( 2 \right)}
$$ (eqn:H_SSC)

对于相同多重度的态之间的矩阵元，它可简化为

$$\begin{array}{l}
 \left\langle { aSM\left|{ \hat{{H} }_{\text{SSC} } } \right|a'SM'} \right\rangle=\frac{\sqrt{ \left({ S+1} \right)\left({ 2S+3} \right)} }{\sqrt{ S\left({2S-1} \right)} } \\
\hspace{2cm}
\times \sum\limits_m { \left({ -1}
\right)^{m} } \left(\begin{matrix}{ S'}  & 2  \\
 { M'}  & m
\end{matrix} \left|{\begin{matrix}
 S  \\
 M  \\
\end{matrix} } \right. \right) \sum\nolimits_{pqrs} { D_{pqrs}^{\left({ -m}
\right)} \left\langle { aSS\left|{ Q_{pqrs}^{0} } \right|a'SS} \right\rangle}
 \end{array}
$$ (eqn:SSC_RMEs)

其中，

$$Q_{pqrs}^{\left( 0 \right)} =\frac{1}{4\sqrt 6 }\left\{{ E_{pq} \delta
_{sr} -S_{ps}^{z} S_{rq}^{z} +\frac{1}{2}\left({ S_{pq}^{z} S_{rs}^{z}
-E_{pq} E_{rs} } \right)} \right\}$$ (eqn:Qpqrs)

代表双电子五重态密度。
算符
$E_{pq}=\hat{{a} }_{p}^{\uparrow } \hat{{a} }_{q} +\hat{{b} }_{p}^{\uparrow } \hat{{b} }_{q}$
和
$S_{pq}^{z} =\hat{{a} }_{p}^{\uparrow } \hat{{a} }_{q} -\hat{{b} }_{p}^{\uparrow }
\hat{{b} }_{q}$ 分别表示单电子密度算符和自旋密度算符。
空间部分

$$D_{pqrs}^{\left( 0 \right)} =\frac{1}{\sqrt 6 }\iint{ \varphi_{p}
\left({ \mathrm{\mathbf{r} }_{1} } \right)\varphi_{r} \left({ \mathrm{\mathbf{r} }_{2}
} \right)}\frac{3r_{1z} r_{2z} -\mathrm{\mathbf{r} }_{1} \mathrm{\mathbf{r} }_{2}
}{r_{12}^{5} }\varphi_{q} \left({ \mathrm{\mathbf{r} }_{1} } \right)\varphi
_{s} \left({ \mathrm{\mathbf{r} }_{2} } \right)d\mathrm{\mathbf{r} }_{1} d\mathrm{\mathbf{r} }_{2}
$$ (eqn:Dpqrs)

表示双电子场梯度积分。
这些双电子积分可用 RI 近似评估。

最后，塞曼哈密顿量以下述形式纳入：

$$\hat{{H} }_{\text{Z} } =\mu_{B} \left({ \mathrm{\mathbf{\hat{{L} }} }+g_{e} \mathrm{\mathbf{\hat{{S} }} }} \right)\mathrm{\mathbf{B} }
$$ (eqn:H_Zeeman)

其中 $\mathrm{\mathbf{\hat{{L} }}}$ 表示总轨道动量算符，
$\mathrm{\mathbf{\hat{{S} }}}$ 为总自旋算符。

在这一框架下，求解所选相对论哈密顿量可获得众多磁性质，
即 EPR 性质（{ref}`sec:spectroscopyproperties.properties.eprnmr`）
以及磁化率和磁化强度性质
（{ref}`sec:modelchemistries.mrci.soc.magnet`）。
此外，监测外磁场对相对论本征态和本征矢的影响
（{ref}`sec:modelchemistries.mrci.soc.magField`）也变得简单直接。

总体而言，在 QDPT 框架下可获得以下磁性质：

- 常见 QDPT 磁性质

  (1) g 张量/矩阵
\
  (2) D 张量/矩阵（零场分裂，ZFS）
\
  (3) A 张量/矩阵（超精细，HFC）
\
  (4) 电场梯度
\
  (5) 磁化强度
\
  (6) 磁化率
\
  (7) 外磁场的纳入

- 特殊处理还包括

  (8) 用二阶态求和（sum-over-states）近似的 g 张量/矩阵和 A 张量/矩阵
\
  (9) {ref}`sec:spectroscopyproperties.magrelax` 功能


(sec:spectroscopyproperties.qdpt_magnetic_properties.effective_hamiltonian)=
## 通过有效哈密顿量计算磁性质

由于低能自旋-轨道态的能量和波函数都可获得，
有效哈密顿量理论可用于提取 EPR 参数，
如完整的 g 张量、零场分裂（Zero Field Splitting，ZFS）
和超精细 A 张量。

前提是基态非简并。通过在模型空间
（即基态的 $|S, M_S\rangle$ 分量）的基下作用该哈密顿量，
构建相互作用矩阵。

有效哈密顿量的构建依赖于低能自旋-轨道态的能量和波函数两方面所含的信息。
按照 des Cloizeaux 形式，有效哈密顿量重现"精确"哈密顿量的能级 $E_k$
以及低能态投影到模型空间的波函数 $\tilde{\Psi}$：

$$\hat{H}_{\text{eff} }|\tilde{\Psi}_{k}\rangle = E_{k}|\tilde{\Psi}_{k}\rangle$$

然后对这些投影矢量作对称正交归一化，
得到厄米的有效哈密顿量，可写为：

$$\hat{H}_{\text{eff} }|\tilde{\Psi}\rangle = \sum_{k}|S^{-\frac{1}{2} }\tilde{\Psi}_{k}\rangle
E_{k} \langle S^{-\frac{1}{2} }\tilde{\Psi}_{k}|$$

将该哈密顿量在属于模型空间的行列式基下展开，得到有效相互作用矩阵，
再与模型哈密顿量展开所得的矩阵作比较。
基于奇异值分解（singular value decomposition）过程，
可提取 g、A 和/或 ZFS 张量的全部 9 个分量。


(sec:spectroscopyproperties.qdpt_magnetic_properties.keywords)=
## QDPT 关键词

从 ORCA 6.0 开始，所有可用关联类型模块中
通过准简并微扰理论（QDPT）计算磁性质的方式被统一和简化。
按照 ORCA 6.0 的总体架构设计，
所有相关磁性质的计算由一个称为 QDPT Driver 的驱动数据结构集中执行。
该 Driver 考虑了相关模块填入的所有特定变量，
并以统一的方式计算和表示所请求的性质。
这目前涉及 `casscf`、`mrci`、`rocis` 和 `lft` 模块。

这样，
1) 从用户角度对结果的分析被简化
2) 跨模块的关联和比较易于进行

启用 QDPT 性质生成的通用关键词是：

```orca
%METHOD (casscf, mrci, rasci, rocis, lft, ...)
  REL            # the name of the relativistic block
    DoSOC true   # include the SOC contribution
    DoSSC true   # include the SSC contribution
  END
END
```

从 ORCA 6.1 开始，相对论块在所有连接到 QDPT driver 的方法中具有统一的结构。
因此，`rel` 是所有连接方法的默认块名。
对于 `%mrci` 块，`soc` 是一个备选名称，
以在本版本中保持与旧输入相对论块的兼容性。
`soc` 块名将在下个版本中弃用，
因此建议使用 `rel` 块名来请求 QDPT 性质。

QDPT 关键词如下：
```orca
%METHOD (CASSCF, RASCI, MRCI, ROCIS, LFT)
  REL
   #-------------------------------------------------------
   # SOC/SSC
   #-------------------------------------------------------
   DoSOC true
   DoSSC true
   PrintLevel 4

   #=======================================================
   # MAGNETIC PROPERIES
   #=======================================================

   #-------------------------------------------------------
   #Do Magnetization Magntization/Susceptibily Properties
   #-------------------------------------------------------
   DoMagnetization true
   DoSusceptibility true
   #-------------------------------------------------------
   LebedevPrec 5           # Precision of the grid for different field
   nPointsFStep 5          # number of steps for numerical differentiation
   MAGFieldStep 100.0      # Size of field step for numerical differentiation
   MAGTemperatureMIN 4.0   # minimum temperature (K) for magnetization
   MAGTemperatureMAX 4.0   # maximum temperature (K) for magnetization
   MAGTemperatureNPoints 1 # number of temperature points for magnetization
   MAGFieldMIN 0.0         # minimum field (Gauss) for magnetization
   MAGFieldMAX 70000.0     # maximum field (Gauss) for magnetization
   MAGNpoints 15           # number of field points for magnetization
   SUSTempMIN 1.0          # minimum temperature (K) for susceptibility
   SUSTempMAX 300.0        # maximum temperature (K) for susceptibility
   SUSNPoints 300          # number of temperature points for susceptibility
   SUSStatFieldMIN 0.0     # minimum static field (Gauss) for susceptibility
   SUSStatFieldMAX 0.0     # maximum static field (Gauss) for susceptibility
   SUSStatFieldNPoints 1   # number of static fields for susceptibility

   #-------------------------------------------------------
   # Magnetic Field Magnetic Filed Perturbation (Zeeman Effect)
   #-------------------------------------------------------
   DoMagneticField true
   Temperature 10, 50, 300
   B 10000, 20000, 30000

   #-------------------------------------------------------
   # EPR g-Tensor/Matrix
   #-------------------------------------------------------
   DoGTensor true
   NDoubGtensor 2

   #-------------------------------------------------------
   # EPR D-Tensor/Matrix (Zero Field Splitting, ZFS)
   #-------------------------------------------------------
   DoDTensor true

   #-------------------------------------------------------
   # EPR A-Tensor/Matrix (Hyperfine, HFC)
   # => Presently only in CASSCF and LFT
   #-------------------------------------------------------
   DoAMatrix true
   AMatrixNuc 0,1

   #-------------------------------------------------------
   # 2nd-order SUM OVER STATES (g-, A-Tensors/Matrices)
   # => Presently only in CASSCF and MRCI
   #-------------------------------------------------------
   DoSOS True

   #-------------------------------------------------------
   # ZFS from an excited state multiplet
   #-------------------------------------------------------
   IStates 4,5,6

   #-------------------------------------------------------
   # Magnetic Relaxation 
   # => Presently only in CASSCF and MRCI
   #-------------------------------------------------------
   DoMagrelax True
   projectHSOC True       # Project QDPT ground multiplet (always true)
   projectedstates Number # Multiplicity of the ground multipler  

   #=======================================================
   # OPTICAL/X-RAY SPECTROSCOPIES
   #=======================================================

   #-------------------------------------------------------
   # (X)MCD (X-ray) Magnetic Circular Dichroism Spectroscopy
   #-------------------------------------------------------
   DoMCD True

   #-------------------------------------------------------
   # XESSOC X-ray Emission Spectroscopy
   #-------------------------------------------------------
   DoXESSOC True

   #-------------------------------------------------------
   # RIXSSOC X-ray Resonance Inelastic Scattering Spectroscopy
   #-------------------------------------------------------
   DoRIXSSOC True
   DoElastic True
  END
END 
```

(sec:spectroscopyproperties.qdpt_magnetic_properties.properties_organization)=
## QDPT 磁性质计算的组织流程

第一步，将为任何可用的理论水平计算 SOC 贡献

```orca
----------------------------------
QDPT WITH CASSCF/NEVPT2/MRCI/LFT... DIAGONAL ENERGIES
----------------------------------


*************************************
COMPUTING QDPT HAMILTONIAN
*************************************
```

首先计算劈裂的 SOC 部分。
首先在相同多重度的态之间评估对角（相对于自旋）矩阵元类型

$\left\langle { \Psi_{I} }
\right|\sum\limits_{pq} { \mathrm{\mathbf{z} }_{pq}^{x} S_{pq}^{z} } \left| \Psi_{J}
\right\rangle$、$\left\langle { \Psi_{I} }
\right|\sum\limits_{pq} { \mathrm{\mathbf{z} }_{pq}^{y} S_{pq}^{z} } \left| \Psi_{J}
\right\rangle$、$\left\langle { \Psi_{I} }
\right|\sum\limits_{pq} { \mathrm{\mathbf{z} }_{pq}^{z} S_{pq}^{z} } \left| \Psi_{J}
\right\rangle$

而在不同多重度的态之间评估

$\left\langle { \Psi_{I} }
\right|\sum\limits_{pq} { \mathrm{\mathbf{z} }_{pq}^{x} S_{pq}^{+} } \left| \Psi_{J}
\right\rangle$、$\left\langle { \Psi_{I} }
\right|\sum\limits_{pq} { \mathrm{\mathbf{z} }_{pq}^{y} S_{pq}^{+} } \left| \Psi_{J}
\right\rangle$、$\left\langle { \Psi_{I} }
\right|\sum\limits_{pq} { \mathrm{\mathbf{z} }_{pq}^{z} S_{pq}^{+} } \left| \Psi_{J}
\right\rangle$。


请求 `PrintLevel > 3` 会打印如下表格：

```orca
----------------------------------------------------------------------------
                        CALCULATED REDUCED SOC MATRIX ELEMENTS              
----------------------------------------------------------------------------
        Block               Root         <I|Lx S |J> <I|Ly S |J> <I|Lz S |J>
 I(Mult)     J(Mult)      I        J        cm-1        cm-1        cm-1    
----------------------------------------------------------------------------
 0( 3)       0( 3)        0        0         0.00       -0.00       -0.00  
 0( 3)       0( 3)        1        0        -0.00       -0.00        0.00  
 0( 3)       0( 3)        1        1         0.00       -0.00       -0.00  
 0( 3)       0( 3)        2        0         0.00       -0.00       -0.00  
 0( 3)       0( 3)        2        1      -199.78      174.81     -142.34  
...

 0( 3)       1( 1)        0        1        -0.67        0.59       -0.48  
 0( 3)       1( 1)        0        2      -157.31      137.65     -112.09  
 0( 3)       1( 1)        0        3        -0.00       -0.00       -0.00  
 0( 3)       1( 1)        0        4       -79.51      -33.73       70.17  
 0( 3)       1( 1)        0        5        24.77       84.05       68.46
... 
  
```

```orca
*************************************
Doing QDPT with ONLY SOC!
*************************************
```

接下来，将打印非零的 SOC 矩阵元

```orca
------------------------------------
NONZERO SOC MATRIX ELEMENTS (cm**-1)
------------------------------------

           Bra                       Ket       
<Block Root S   Ms  | HSOC | Block Root S   Ms>    =  Real-part     Imaginary part
----------------------------------------------------------------------------------
   0    2  1.0  1.0           0     1  1.0  1.0          0.000            -71.172
   0    3  1.0  1.0           0     2  1.0  1.0          0.000              1.542
   0    4  1.0  1.0           0     0  1.0  1.0          0.000             50.048
   0    5  1.0  1.0           0     0  1.0  1.0          0.000            -48.827
   0    5  1.0  1.0           0     4  1.0  1.0          0.000            -40.119
   0    6  1.0  1.0           0     1  1.0  1.0          0.000             -0.197
   0    6  1.0  1.0           0     3  1.0  1.0          0.000              8.724
   0    7  1.0  1.0           0     1  1.0  1.0          0.000             -2.695

...

   1    0  0.0  0.0           0     4  1.0  1.0         16.671            -39.318
   1    0  0.0  0.0           0     5  1.0  1.0        -41.569             12.256
   1    0  0.0  0.0           0     4  1.0  0.0         -0.000            -49.087
   1    0  0.0  0.0           0     5  1.0  0.0         -0.000            -47.869
   1    0  0.0  0.0           0     4  1.0 -1.0         16.671             39.318
   1    0  0.0  0.0           0     5  1.0 -1.0        -41.569            -12.256
   1    1  0.0  0.0           0     0  1.0  1.0          0.294              0.336
   1    1  0.0  0.0           0     4  1.0  1.0         41.742            -12.307
/
...
```

随后打印 SOC 哈密顿量

```orca
Note: In the following the full <I|HBO+SOC|J> are printed in the CI Basis.     
      I,J are compound indices for |Block/Mult, Ms, Root>, where the states    
      are ordered first by MultBlock, then Ms and finally Root.                
-----------------
SOC MATRIX (A.U.)
-----------------
```

最后，打印经相对论校正的本征值和本征矢

```orca
Lowest eigenvalue of the SOC matrix:    -149.86223277 Eh
Energy stabilization:    -2.54512 cm-1
Eigenvalues:     cm-1         eV      Boltzmann populations at T =  300.000 K
   0:            0.00        0.0000       3.36e-01
   1:            2.37        0.0003       3.32e-01
   2:            2.37        0.0003       3.32e-01
   3:         7757.65        0.9618       2.33e-17
   4:         7757.66        0.9618       2.33e-17
   5:        11913.81        1.4771       5.15e-26

...

The threshold for printing is 0.0100
Eigenvectors:
                         Weight      Real          Image    : Block Root  Spin   Ms
 STATE   0:       0.0000
                         0.388265     0.410320    -0.468937 :     0    0    1    1
                         0.223270    -0.000000     0.472514 :     0    0    1    0
                         0.388265     0.410320     0.468937 :     0    0    1   -1
 STATE   1:       2.3703
                         0.310686     0.534586     0.157809 :     0    0    1    1
                         0.378606     0.000017    -0.615309 :     0    0    1    0
                         0.310706     0.534623    -0.157747 :     0    0    1   -1
 STATE   2:       2.3703
                         0.300970    -0.214003    -0.505146 :     0    0    1    1
                         0.398078    -0.000007    -0.630934 :     0    0    1    0
                         0.300949    -0.214019     0.505119 :     0    0    1   -1

...


```

现在，所有相关的 QDPT 性质都被计算并打印：

```orca
*************************************
COMPUTING QDPT PROPERTIES
*************************************
```

(1) g 张量/矩阵
```orca
----------------------------------------------
ELECTRONIC G-MATRIX FROM EFFECTIVE HAMILTONIAN
----------------------------------------------
```

(2) 基于二阶和有效哈密顿量近似的 ZFS（D 张量/矩阵）
```orca
--------------------------------------------
           ZERO-FIELD SPLITTING
2ND ORDER SOC CONTRIBUTION
--------------------------------------------
--------------------------------------------------------
                  ZERO-FIELD SPLITTING
EFFECTIVE HAMILTONIAN SOC CONTRIBUTION
--------------------------------------------------------
```

(3) HFC（A 张量/矩阵）
```orca
-------------------------
QDPT HFC A-MATRICES
-------------------------
```

在 CASSCF 和 LFT 模块中，可以用如下方式请求 A 矩阵：
```orca
AMatrix true
AMatrixNuc 0, 2      
```

若需要，可以为计算指定同位素

```orca
AMatrix true
AMatrixNuc 0, 2, 3

# e.g. for Nuclei 0, this requires partially or fully populating the
# following quantities:

AMATRIXP[0]=125.6   #the P-value for the hyperfine ge*gN*beta*betaN
AMATRIXQ[0]=3.87    #the quadrupole value (in barn)
AMATRIXIP[0]=2.5    #spin of the isotope for the A-tensor
AMATRIXIQ[0]=0.0    #spin of the isotope of the Q-tensor
AMATRIXTP[0]=237    #AMatrixISTPP[0]
AMATRIXTQ[0]=0      #AMatrixISTPQ[0]

# It follows that for Nuclei 2, one does 
AMATRIXTP[1]=36
...
# and so on.
```

(4) 电场梯度张量
```orca
---------------------------------------
EFG TENSOR
---------------------------------------
```

(5) 与 (6) 磁化强度/磁化率
```orca
-------------------------------------------------
SOC CORRECTED MAGNETIZATION AND/OR SUSCEPTIBILITY
-------------------------------------------------
```

(7) 外磁场贡献
```orca
----------------------------------------------------------------------------------------------------------
               SOC TRANSITION MAGNETIC DIPOLE CONTRIBUTIONS IN EXTERNAL MAGNETIC FIELD                
           Magnetic field Bx =       1.00 Gauss  By =       0.00 Gauss  Bz =       0.00 Gauss
----------------------------------------------------------------------------------------------------------
 States       Energy      Energy     Osh.Str           M2            MX             MY             MZ     
              (cm-1)       (eV)        (au)          (au**2)        (au)           (au)           (au)    
----------------------------------------------------------------------------------------------------------
 0  0         0.00       0.0000     0.00000000     0.00000145     0.00090159     0.00061858     0.00050413
 0  1        20.20       0.0025     0.00000000     0.00000126     0.00042808     0.00067630     0.00078545
 1  1         0.00       0.0000     0.00000000     0.00000000     0.00003430     0.00002347     0.00001909
----------------------------------------------------------------------------------------------------------
```

随后，在同一校正方案下打印所有经相对论校正的光谱
（详见 {ref}`sec:spectroscopyproperties.ops`）。

```orca
--------------------------------------------------------------------------------------------------------
      SOC CORRECTED ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS    
--------------------------------------------------------------------------------------------------------
      Transition         Energy     Energy  Wavelength fosc(D2)      D2       |DX|      |DY|      |DZ|  
                          (eV)      (cm-1)    (nm)  (*population)  (au**2)    (au)      (au)      (au)  
--------------------------------------------------------------------------------------------------------

...

```

(8) 态求和（sum-over-states）g 张量和 A 张量/矩阵
（目前仅在 CASSCF 和 MRCI 中可用）
其打印方式与有效哈密顿量的结果基本相同。
主要区别在于标记：
```orca
---------------------------------------------------------------------------
SUM OVER STATES CALCULATION OF THE SPIN HAMILTONIAN (for g and HFC tensors)
---------------------------------------------------------------------------
```
求和中所用的矩阵元在以下内容之后打印
```orca
-----------------------
MATRIX ELEMENT PRINTING
-----------------------
```
g 张量还会额外打印每个态对 `g(OZ/SOC)` 项的贡献。
```orca
-------------------------------
BREAKDOWN OF g(OZ/SOC) BY STATE
-------------------------------

STATE                                g1           g2           g3
--------------------------------------------------------------------
```
请注意，对于 CASSCF，不含轨道响应的 {ref}`sec:spectroscopyproperties.casscfresp`
等价于包含所有态的态求和。因此，态求和的主要优点就在于这种逐态分解。


若请求了 SSC，将在第二步生成自旋-自旋耦合贡献，
并将其加入 SOC 哈密顿量以产生 SOC+SSC 贡献

```orca
-------------------------------------------
Calculating Spin-Spin Coupling Integrals
-------------------------------------------
```

程序随后将执行与上述完全相同的分析，打印 SOC+SSC 分析结果。
 ```orca
***********************************************************
* DOING EVERYTHING A SECOND TIME: THIS TIME INCLUDING SSC *
***********************************************************

*************************************
COMPUTING QDPT HAMILTONIAN
*************************************

*************************************
Doing QDPT with SOC AND SSC!
*************************************

------------------------------------
NONZERO SOC and SSC MATRIX ELEMENTS (cm**-1)
------------------------------------

           Bra                       Ket       
<Block Root S   Ms  | HSOC + HSSC |  Block Root  S    Ms> =  Real-part  Imaginary part
--------------------------------------------------------------------------------------
   0    2  1.0  1.0                  0     1  1.0  1.0       -0.000        -71.172
   0    3  1.0  1.0                  0     1  1.0  1.0       -0.001          0.000
   0    3  1.0  1.0                  0     2  1.0  1.0        0.020          1.542
   0    4  1.0  1.0                  0     0  1.0  1.0       -0.222         50.048
   0    5  1.0  1.0                  0     0  1.0  1.0       -0.228        -48.827
   0    5  1.0  1.0                  0     4  1.0  1.0        0.332        -40.119
   0    6  1.0  1.0                  0     1  1.0  1.0       -0.030         -0.197

```

这既针对磁性质（如 ZFS）执行，

```orca
--------------------------------------------------------
                  ZERO-FIELD SPLITTING
EFFECTIVE HAMILTONIAN SOC and SSC CONTRIBUTION
--------------------------------------------------------
```

也针对光学性质执行

```orca
--------------------------------------------------------------------------------------------------------
  SOC+SSC CORRECTED ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS    
--------------------------------------------------------------------------------------------------------
      Transition         Energy     Energy  Wavelength fosc(D2)      D2       |DX|      |DY|      |DZ|  
                          (eV)      (cm-1)    (nm)  (*population)  (au**2)    (au)      (au)      (au)  
--------------------------------------------------------------------------------------------------------
```
