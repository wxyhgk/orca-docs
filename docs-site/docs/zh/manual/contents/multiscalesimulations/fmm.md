

<a id="sec:multiscalesimulations.fmm"></a>
# 快速多极方法（Fast Multipole Method）

快速多极方法（Fast Multipole Method，FMM）算法于 20 世纪 80 年代提出[Greengard1987](../../bibliography.md)，用于减少大体系中双中心相互作用的计算时间，将计算时间与粒子数 $N$（原子、点电荷等）的关系从二次关系（O($N^2$)）转变为准线性关系（O$(Nlog(N))$）。该算法对于难以忽略的长程相互作用尤其有用，例如对任何体系都至关重要、但随中心数目二次增长的库仑相互作用（1/r）。

FMM 在 ORCA 中用于加速静电嵌入范围内的 QMMM 计算：FMM-QMMM（参见 [multiscalesimulations.qmmm-embedding](qmmm-general.md#sec:multiscalesimulations.qmmm-embedding)）。

<a id="sec:multiscalesimulations.fmm.octree"></a>
## 八叉树层次结构（The Octree hierarchy）

关于这一主题已有大量详细且具教学性的文献（我们推荐例如 [Anisimov2019](../../bibliography.md) 和 [Helgaker2013](../../bibliography.md)）。下面我们将只描述主要参数。

算法的思想是划分空间，以便对短程和长程相互作用区别处理。后者将被近似（参见 [multiscalesimulations.fmm](#sec:multiscalesimulations.fmm)）。为此，整个体系被置于一个立方盒中，该立方盒被迭代地划分为 8 个子盒（形成层级 L: $\text{L}=0 \rightarrow \text{L}=\text{L}_{\text{max}}$），从而形成称为八叉树（Octree）的结构（见图 [fig:FMM_pres](#fig:FMM_pres)）。

<a id="fig:FMM_pres"></a>
*体系划分为盒子的示意，以 2D 表示。*

在最深层级 $\text{L}=\text{L}_{\text{max}}$，对每个盒子，我们可以定义一层最近邻盒子（nearest neighbours，NN），它们将负责近场（Near-Field，NF，即短程）。其余盒子产生的静电势定义为远场（Far-Field，FF，即长程）。

$$
\begin{aligned}
\forall B \;\; ,\;\; V_B = V_B^{NF} + V_B^{FF}
\end{aligned}
$$

如图 [fig:FMM_pres](#fig:FMM_pres) 所示，可以将 FF 区域划分为局域远场（Local Far Field，LFF，绿色）区域和远程远场（Remote Far Field，RFF，灰色）区域，这样便在各层级之间出现了递归方案：

$$
\begin{aligned}
\forall B \;\; V_B^{FF} &= V_B^{{\textcolor{darkgreen}{LFF}}} + V_B^{RFF}\\
 &= V_B^{{\textcolor{pinegreen}{LFF}}} + W_{Parent(B)\rightarrow B}^T V_{Parent(B)}^{FF}
 \end{aligned}
$$

LFF 盒子是位于父盒子 NF 中但不在子盒子 NF 中的盒子，最多可达 189 个盒子。RFF 势来自实际上代表 B 的父盒子 FF 区域的盒子。这意味着只需在每个层级计算 LFF 项，其余势将从父盒子继承。

层级数 $\text{L}_{\text{max}}$ 可以直接在输入中设置（FMMQMMM_Levels），也可以根据所提供的盒子尺寸推导（FMMQMMM_BoxDimInp，$\text{L}_{\text{max}}$ 处盒子的尺寸）。推荐第二种选项（默认），盒子尺寸约 9.0 Bohr（FMMQMMMM_BoxDimInp      9.0 ）。
如果 FMMQMMM_DoBoxDimOpt 选项设为 TRUE（默认），盒子尺寸将尽可能缩小，同时保持 $\text{L}_{\text{max}}$ 的值不变，以确保算法在精度和效率两方面都达到最优。

```orca
%method
  DOFMMQMMM            True  # turn ON the use of the FMM   
  FMMQMMM_BoxDimInp     9.0  # higher boundary to set up the dimension (in Bohr!)
  FMMQMMM_DoBoxDimOpt  True  # optimize the box dimension
end
```

$\text{L}_{\text{max}}$ 越高，盒子数目越多：在 $\text{L}=2$ 时只有 64 个盒子，而对 $\text{L}=6$，程序会生成超过 200,000 个盒子（$8^6$）。当 $\text{L}_{\text{max}} \geq 7$ 时，会生成超过 2 百万个盒子，这可能开始导致内存问题，因此用户应确保有足够的可用内存（参见 [input.globalmemuse](../essentialelements/input.md#sec:essentialelements.input.globalmemuse) ）。

如果体系特别致密，可以将 $\text{L}_{\text{max}}$ 处盒子的尺寸除以 2，以使方法更高效。类似地，对于粒子分布稀疏的体系，$\text{L}_{\text{max}}$ 处盒子的输入尺寸可以设为 18.0 Bohr。

<a id="sec:multiscalesimulations.fmm.FF"></a>
## 远场相互作用的近似（Approximation of the Far Field interactions）
在原点为 O(0,0,0) 的空间中，设 P（$r_P$）为某一电荷分布（例如高斯重叠或点电荷分布）的中心。考虑 P 附近的一点 A，使得 A = ($q_A$; $r_A$)，其中 $q_A$ 为点电荷的电荷，或者若考虑高斯重叠则 q$_A = -1$。在后一种情况下，电荷实际上是位于距高斯重叠中心 $r_{AP} = r_{A} - r_{P} $ 处的电子的电荷。类似地，设 Q（$r_Q$）为某一电荷分布的中心，B 为 Q 附近的一点，使得 B = (q$_B$; $r_B$)。记 $r_{QP} = r_Q-r_P$。

A 与 B 之间的库仑相互作用可以表示为：

$$
\begin{aligned}
    U_{AB} = f\Big( \frac{1}{|r_a-r_b|} \Big)
,\end{aligned}
$$

该算法的名称来源于 FF 相互作用的求值方式。它通过对 $\frac{1}{|r_a-r_b|}$ 项进行多极展开来完成，得到下列表达式：

$$
\begin{aligned}
\frac{1}{|r_A-r_B|}  = \sum_{l=0}^{\in fty} \sum^{l}_{m=-l} \sum_{j=0}^{\in fty} \sum^{j}_{k=-j} (-1)^j R_{l,m}(r_{AP})I_{l+j,m+k}(r_{QP})R_{j,k}(r_{BQ}) 
,\end{aligned}
$$

该级数仅在中心充分分离时收敛，这就是需要 NF 层的原因。
$R_{l,m}$ 和 $I_{l,m}$ 是正规和非正规固体标度谐函数（solid scaled harmonics）[Perez1996](../../bibliography.md)：

$$
\begin{aligned}
R_{l,m}(r) &= \frac{1}{\sqrt{(l-m)!(l+m)!}} r^l \sqrt{\frac{4\pi}{2l+1}} Y_{l,m}(r) \\
I_{l,m}(r) &= \sqrt{(l-m)!(l+m)!} \frac{1}{r^{l+1}} \sqrt{\frac{4\pi}{2l+1}} Y_{l,m}(r) 
\end{aligned}
$$

$Y_{l,m}$ 是 $l$ 阶 $m$ 次球谐函数。有关该方程推导的细节，见 [Anisimov2019](../../bibliography.md)。

现在我们可以引入以 P（$r_P$）为中心、电荷分布 $Q(r,P)$ 的多极展开，表示为：

$$
\begin{aligned}
Q(r,P) = f\Big(\sum_{l=0}^{\in fty} \sum^{l}_{m=-l} R_{l,m}(r-r_P) \Big)
\end{aligned}
$$

实践中：

$$
\begin{aligned}
Q(r,P) \approx f\Big(\sum_{l=0}^{\textcolor{blue}{MAM}} \sum^{l}_{m=-l} R_{l,m}(r-r_P) \Big)
\end{aligned}
$$

$Q$ 是一个向量，其元素 $Q_{l,m}$ 由一对值（$l$,$m$）定义。
对于点电荷 A（$q_A$,$r$），有：

$$
\begin{aligned}
   Q_{l,m}^A(r,P) = q_A \times R_{l,m}(r-r_P) 
,\end{aligned}
$$

而对于高斯重叠分布 $\braket{\mu|\nu}$ 则变为：

$$
\begin{aligned}
   Q_{l,m}^{\mu\nu}(r,P) &= \langle\mu|R_{l,m}(r-r_P)|\nu\rangle\\
   &=  \in t \mu(r')R_{l,m}(r-r_P)\nu(r') dr'
\end{aligned}
$$

这样我们就可以通过下列展开来近似中心位于 $r_B$ 的高斯重叠 $\braket{\mu |\nu}$ 与 FF 中点电荷 A（$q_A$,$r_A$）之间的静电相互作用：

$$
\begin{aligned}
\frac{\in t q_A \mu(r)\nu(r)dr}{|r_A-r_B|}  \approx   Q^{\mu\nu}(r_b,P')  I(r_{PP'})Q^A(r_A,P)  
,\end{aligned}
$$

其中 $P$ 和 $P$' 分别是多极展开的中心，I 是相互作用矩阵。

展开的截断参数 MAM 是底层固体标度谐函数的最大角动量（Maximum Angular Momentum）。在我们的设置中，嵌入中点电荷的展开与 QM 部分高斯重叠的展开使用相同的值。它可以通过关键词 FMMQMMM_MAM 设置。我们建议 FMMQMMM_MAM = 20 以确保良好的精度，约为 0.0001-0.0001 Ha。取较低的 MAM=15 值时，通常可预期 mHa（0.63 kcal.mol$^{-1}$）量级的精度。不过这与体系有关，因此我们建议您从 MAM=20 开始，然后观察将其减小到 15 时的表现。MAM 的可用取值范围是 1-25。

```orca
%method
  DOFMMQMMM             True  # turn ON the use of the FMM   
  FMMQMMM_MAM             20  # default Maximum Angular Momentum
end
```

<a id="sec:multiscalesimulations.fmm.VFMM"></a>
## “超”快速多极方法（VFMM）（The "Very" Fast Multipole Method）

由于层级间的递归方案，盒子中心所感受到的 FF 是通过在每个层级仅计算与 LFF 盒子的相互作用而构建的。$V^{LFF}$ 的求值成为算法的瓶颈。为加速它，实现了一个选项，对 LFF 区域中所有（>189 个）盒子使用不同的 MAM 截断参数。选项 FMMQMMMM_DoVFMM 默认开启，但当 MAM 小于 15 时应关闭，否则会在效率提升不大的情况下过多影响精度。

```orca
%method
  DOFMMQMMM             True  # turn ON the use of the FMM   
  FMMQMMM_DoVFMM        True  # use the Very Fast Multipole Method 
end
```
<a id="sec:multiscalesimulations.fmm.reco"></a>
## 推荐输入（Recommended input）
只要有静电嵌入，对于包含超过 10,000 个点电荷（ECM）或 MM 原子（QMMM）的体系，建议开启 FMM 以加速静电势的计算。不过，当使用超过 24 个处理器的高度并行化时，对于较小的嵌入规模，启用快速多极方法（FMM）的影响可能可以忽略。

!!! note "小心"
    FMM-QMMM 并不取代 QMMM 关键词。

可以调整的两个要素是展开的截断参数 MAM 和最深层级（$\text{L}_{\text{max}}$）处的盒子尺寸。推荐/默认参数可以直接在关键词行使用 FMM-QMMM 调用，也可以在 %method 块中相应设置参数：

```orca
#keyword line
! FMM-QMMM

#OR through method block

%method
 DOFMMQMMM            True  # turn ON the use of the FMM   
 USEFMMQMMM           True  # turn ON the use of the FMM  
 ###parameters:
 FMMQMMM_DoVFMM       True  # use the Very Fast Multipole Method 
 FMMQMMM_MAM            20  # Maximum Angular Momentum
 FMMQMMM_Levels          0  # number of levels set to 0, will be set automatically
                            # by box dimension 
 FMMQMMM_BoxDimInp     9.0  # higher boundary to set up the dimension (in Bohr!)
 FMMQMMM_DoBoxDimOpt  True  # optimize the box dimension
end
```
算法所用的参数默认会打印在输出中，我们建议您在最初的计算中检查它们：
```orca
----------------------
SHARK INTEGRAL PACKAGE
----------------------

[...]

Use FMM for one center integrals with PCs

- - - - - - - FMM PARAMETERS- - - - - - - 
num PCs              75894
VFMM                  USED
MAM                   20
Input box dim        9.000
Refined box dim      5.197
Tree depth/levels      6
- - - - - - - - - - - - - - - - - - - - - 
```

这可以通过修改相应的打印选项来关闭。

```orca
%method
 FMMQMMM_Printing 1 # remove FMM PARMETERS printing, default value is  2
end
```

<a id="sec:multiscalesimulations.fmm.example"></a>
## 一些示例（Some examples）
通过关键词行调用推荐的 FMM 参数：
```orca
!QMMM wB97X-D3BJ RIJCOSX FMM-QMMM

%qmmm
 ORCAFFFilename "file.prms"
 Embedding Electrostatic
 ChargeAlteration CS
 QMAtoms {2016:2026} end
end

*pdbfile 0 1 file.pdb
```

将 MAM 从 20（使用关键词行时的值）改为 15，并使用 5 个层级：

```orca
!QMMM wB97X-D3BJ RIJCOSX

%method
  DOFMMQMMM             True  # turn ON the use of the FMM   
  USEFMMQMMM            True  # turn ON the use of the FMM  
  ###parameters:
  FMMQMMM_DoVFMM        True  # use the Very Fast Multipole Method 
  FMMQMMM_MAM             15  # maximum Angular Momentum
  FMMQMMM_Levels           5  # number of levels
end

%qmmm
 ORCAFFFilename "file.prms"
 Embedding Electrostatic
 ChargeAlteration CS
 QMAtoms {2016:2026} end
end

*pdbfile 0 1 file.pdb
```

指定盒子尺寸而不进行优化：

```orca
!QMMM wB97X-D3BJ RIJCOSX

%method
  DOFMMQMMM             True  # turn ON the use of the FMM   
  USEFMMQMMM            True  # turn ON the use of the FMM  
  ###parameters:
  FMMQMMM_DoVFMM        True  # use the Very Fast Multipole Method 
  FMMQMMM_MAM             15  # Maximum Angular Momentum
  FMMQMMM_Levels           0  # number of levels
  FMMQMMM_BoxDimInp      9.0  # higher boundary to set up the dimension (in Bohr!)
  FMMQMMM_DoBoxDimOpt   False # does not optimize the box dimension
end

%qmmm
 ORCAFFFilename "file.prms"
 Embedding Electrostatic
 ChargeAlteration CS
 QMAtoms {2016:2026} end
end

*pdbfile 0 1 file.pdb
```

指定盒子尺寸并要求对其进行优化：

```orca
!QMMM wB97X-D3BJ RIJCOSX

%method
  DOFMMQMMM             True  # turn ON the use of the FMM   
  USEFMMQMMM            True  # turn ON the use of the FMM  
  ###parameters:
  FMMQMMM_DoVFMM        True  # use the Very Fast Multipole Method 
  FMMQMMM_MAM             15  # Maximum Angular Momentum
  FMMQMMM_Levels           0  # number of levels
  FMMQMMM_BoxDimInp      9.0  # higher boundary to set up the dimension (in Bohr!)
  FMMQMMM_DoBoxDimOpt   True  # optimize the box dimension
end

%qmmm
 ORCAFFFilename "file.prms"
 Embedding Electrostatic
 ChargeAlteration CS
 QMAtoms {2016:2026} end
end

*pdbfile 0 1 file.pdb
```
