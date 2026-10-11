

<a id="sec:spectroscopyproperties.fod"></a>
# 分数占据数加权密度（FOD）（Fractional Occupation Number Weighted Density）

许多近似量子化学方法对具有显著静态电子相关
（static electron correlation，SEC）的体系不能给出可靠结果，
而且往往很难预判所讨论的体系是否受 SEC 影响。
现有的标量 SEC 诊断量（如 $T_1$ 诊断）不提供
SEC 在分子中何处的任何信息。
此外，通常必须先执行相当昂贵的计算（如 CCSD），
才能根据单一数值判断结果的可靠性。
具有强 SEC 的分子体系（如共价键断裂、双自由基、
开壳层过渡金属配合物）通常以较小的前线轨道能隙为特征，
因而其电子波函数中存在许多同等重要的行列式。
Hansen 和 Grimme 提出的分数占据数加权密度
（fractional occupation number weighted density，FOD）分析正是利用了这一认识。[hansen2015](../../bibliography.md)
FOD 分析基于[有限温度 KS-DFT](sec:essentialelements.scf.finitetemp)，
其中[分数占据数](sec:essentialelements.scf.fracocc)由
费米分布（"费米涂抹"，Fermi smearing）确定。

$$

f_i=\frac{1}{e^{(\varepsilon_i-E_F)/kT_{el} }+1}\qquad \text{(eqn:spectroscopyproperties.fod.fermi)}

$$

FOD 分析的核心量是分数占据数加权电子密度（$\rho^{FOD}$），
它是位置矢量 $r$ 的实空间函数：

$$

\rho^{FOD}(r)=\sum_i^N (\delta_1-\delta_2f_i) |\varphi_i(r)|^2\qquad \text{(eqn:spectroscopyproperties.fod.fod)}

$$

（若能级低于 $E_F$，则 $\delta_1$ 和 $\delta_2$ 均为 1；
而对于高于 $E_F$ 的能级，它们分别为 0 和 $-1$）。
$f_i$ 表示分数占据数（0$\leq f_i\leq$1；对通过自洽求解 KS-SCF 方程、
使*自由*电子能量最小化所得的所有电子单粒子能级求和）。

$\rho^{FOD}(r)$ 可用预定义的等值面值绘制
（参见 [sec:spectroscopyproperties.fod.plot](#sec:spectroscopyproperties.fod.plot) 一节）。
对 $\rho^{FOD}$ 全空间积分还给出一个附加信息——
称为 $N_{FOD}$ 的单一尺寸可加（size-extensive）数值，
它与其他标量 SEC 诊断量相关性良好，
可用于对分子中的 SEC 效应作全局定量。
因此，FOD 分析和 FOD 图是一种高性价比且稳健的方式，
可用来识别分子中的"热"（强相关）电子，
并为所研究体系的后续计算选取合适的近似量子化学方法。
根据我们的经验，可归纳出以下经验规则：

-   无显著 $\rho^{FOD}$：使用（双）杂化泛函或
    （DLPNO-）CCSD(T)（单参考电子结构）

-   有显著但较定域的 $\rho^{FOD}$：使用半局域 GGA
    泛函（或低 Fock 交换成分的杂化泛函；避免 HF 或 MP2；
    轻微的多参考特征）

-   显著*且*离域的 $\rho^{FOD}$：使用多参考方法
    （或有限温度 DFT；强多参考特征）

!!! note
    尽管 FOD 直观易用，但它并非多参考（MR）特征的 100% 可靠诊断量，
    只应作为初步判据。
    我们建议始终将 FOD 分析与更精细的多参考诊断结合使用。

!!! note
    基于 $\rho^{FOD}(r)$ 的 Mulliken 约化轨道布居
    （参见 [sec:spectroscopyproperties.pop.mulliken](#sec:spectroscopyproperties.pop.mulliken)）
    提供了一种快速替代方法，可获得 FOD 图中的信息
    （参见 [sec:spectroscopyproperties.fod.pbenzyne](#sec:spectroscopyproperties.fod.pbenzyne)）。

<a id="sec:spectroscopyproperties.fod.basicusage"></a>
## 基本用法（Basic Usage）

FOD 分析是一个非常高效实用的工具，
可提供所研究体系中 SEC 的数量与定域化信息，
通过简单输入关键词 `!FOD` 即可调用。

```orca
! FOD
```
这将在默认的 TPSS/def2-TZVP（`TightSCF`）水平上执行分析，
该水平因其快速稳健而被选为默认。
除标准分析输出外（参见 [sec:spectroscopyproperties.fod.pbenzyne](#sec:spectroscopyproperties.fod.pbenzyne)），
$\rho^{FOD}$ 还存储在 `basename.scfp_fod` 文件中，
该文件包含在通用的 `basename.densities` 容器内
（绘制 FOD 图见 [sec:spectroscopyproperties.fod.plot](#sec:spectroscopyproperties.fod.plot)）。

FOD 分析可通过简单输入和 `%scf` 块进行定制。

```orca
! B3LYP def2-TZVP TightSCF

%scf
 SmearTemp 9000
end
```

!!! note
    *   $\rho^{FOD}$（和 $N_{FOD}$）强烈依赖于轨道能隙，
        而轨道能隙本身几乎线性地依赖于非局域 Fock 交换成分 $a_x$
        （参见[杂化 DFT](sec:modelchemistries.dft.hybriddft)）。
        以下将最优电子温度 $T_{el}$ 与 $a_x$ 关联的（经验）函数

        $$

T_{el}=20000\, { \textup K} \times a_x +5000\, { \textup K}\qquad \text{(eqn:spectroscopyproperties.fod.tel)}

$$

        用于确保不同泛函下 FOD 分析得到相似的结果。
        例如，TPSS（$a_x$ = 0）的 `SmearTemp` 须为 5000 K，
        B3LYP（$a_x$ = 20%）为 9000 K，
        PBE0（$a_x$ = 25%）为 10000 K，
        M06-2x（$a_x$ = 54%）为 15800 K。

!!! note "关于 FOD 的几点说明"
    :class: note
    *   FOD 分析对所用基组的依赖性不强（见原始出版物的补充材料[hansen2015](../../bibliography.md)）。

    *   只要 `SmearTemp` $>$ 0 K，FOD 分析总会被打印
        （包括基于 $\rho^{FOD}$ 的 Mulliken 约化轨道布居）。

    *   由于分数占据数下 $\hat{S}^2$ 期望值没有定义，故省略其打印。

    *   FOD 分析对于寻找合适的活性空间也可能有用，
        例如用于 [CASSCF](sec:modelchemistries.casscf) 计算。

<a id="sec:spectroscopyproperties.fod.plot"></a>
## FOD 图（FOD Plots）

分数占据数加权电子密度（$\rho^{FOD}$，参见
[sec:spectroscopyproperties.fod](#sec:spectroscopyproperties.fod)）可按预定义的等值面值绘制成三维图，
经过大量测试，该值被设为默认的 $\sigma=0.005$ e/Bohr$^{3}$。
为便于比较不同体系，该值应固定不变
（在关键情况下，也可用更小的 $\sigma=0.002$ e/Bohr$^{3}$ 检查 FOD 图作对比）。
FOD 在全空间严格为正，
在简单情形下类似于轨道密度（如长链多烯中的 $\pi$ 形状）
或具有完全轨道简并的理想"金属"的总电荷密度。

基本上，$\rho^{FOD}$ 可以用与电子密度类似的方式，
借助 [`orca_plot`](sec:utilities.plot) 工具程序和所生成的 `basename.scfp_fod` 密度文件来绘制，
该密度文件存储于 `basename.densities` 容器中。

为此，以交互模式调用 `orca_plot`：

```orca
orca_plot basename.gbw -i
```
界面随后会显示各种绘图选项。

```orca
PlotType       ... MO-PLOT
MO/Operator    ... 0 0
Output file    ... (null)
Format         ... Grid3D/Binary
Resolution     ... 40 40 40
Boundaries     ...   -22.359392    16.311484 (x direction)
                     -12.628859    13.574504 (y direction)
                      -7.001812     7.002006 (z direction)

       1 - Enter type of plot
       2 - Enter no of orbital to plot
       3 - Enter operator of orbital (0=alpha,1=beta)
       4 - Enter number of grid intervals
       5 - Select output file format
       6 - Plot CIS/TD-DFT difference densities
       7 - Plot CIS/TD-DFT transition densities
       8 - Set AO(=1) vs MO(=0) to plot
       9 - List all available densities
      10 - Perform Density Algebraic Operations

      11 - Generate the plot
      12 - exit this program
Enter a number: 
```

要检查 `basename.densities` 容器中所有可用的密度，
可使用 `9 - List all available densities` 选项。

```orca
---------------------
List of density names
---------------------

Index:                               Name of Density
----------------------------------------------------
    0:                             basename.scfp_fod   <--- required for FOD plot
    1:                                 basename.scfp
    2:                                 basename.scfr
```

生成 FOD 图最通用的方式是创建一个 `.cube` 文件，
它可用 ChimeraX、Chemcraft 等许多外部程序可视化
（参见[图形用户界面](sec:quickstartguide.gui)）。

为此，我们向 `orca_plot` 依次输入以下内容：
```orca
1 (type of plot)
2 (electron density)
n (default name: no)
basename.scfp_fod (name of the FOD file)
4 (number of grid intervals)
120 (NGrid)
5 (output file format)
7 (cube)
10 (generate plot)
11 (exit)
```
!!! note
    请注意，生成的 `.cube` 文件可能非常大，
    而且对较大的分子，用 `orca_plot` 生成它们可能耗费相当长的时间。
    若为了发表而使用高质量的紧密网格分辨率设置
    （即 120x120x120 分辨率），情况尤其如此。

也可以用其他能读取 ORCA 的 `baseame.gbw` 和电子密度文件的程序
从 $\rho^{FOD}$ 生成 `*.cube` 文件
（与电子密度图类似），
只需改用 `basename.scfp_fod` 文件代替 `basename.scfp` 文件即可。

下图是 Ni(bis-dithiolene) 的 FOD 图示例
（[fig:fod-nibdt](#fig:fod-nibdt)）。
它由 ChimeraX 加上 `orca_plot` 生成的 `.cube` 文件绘制而成，
清楚地显示了金属中心和相邻配体上的强 FOD。
这一观察与关于该配合物多参考特征的多项研究一致。

<a id="fig:fod-nibdt"></a>
!!! note "../../images/fod-nibdt.*"
    :width: 70%

    NiBDT 配合物在 $\sigma=0.005$ e/Bohr$^{3}$ 下的 FOD 图
    （TPSS/def2-TZVP (T = 5000 K) 水平，FOD 以黄色表示）。

用相同设置生成的更多 FOD 图示例见
原始出版物及其补充材料。[hansen2015](../../bibliography.md)

<a id="sec:spectroscopyproperties.fod.pbenzyne"></a>
## 示例：*p*-苯炔（*p*-Benzyne）

本例对 *p*-苯炔基态执行 FOD 分析。

```orcainput
! FOD 

* xyz 0 1
C 0.0000000  1.2077612  0.7161013
C 0.0000000  0.0000000  1.3596219
C 0.0000000 -1.2077612  0.7161013
C 0.0000000 -1.2077612 -0.7161013
C 0.0000000  0.0000000 -1.3596219
C 0.0000000  1.2077612 -0.7161013
H 0.0000000  2.1606260  1.2276695
H 0.0000000 -2.1606260  1.2276695
H 0.0000000 -2.1606260 -1.2276695
H 0.0000000  2.1606260 -1.2276695
*
```

相应的输出为：

```orca
-------------------------------------------------------------------------------------------
                                      ORCA LEAN-SCF
                              memory conserving SCF solver
-------------------------------------------------------------------------------------------

----------------------------------------D-I-I-S--------------------------------------------
Iteration    Energy (Eh)           Delta-E    RMSDP     MaxDP     DIISErr   Damp  Time(sec)
-------------------------------------------------------------------------------------------
               ***  Starting incremental Fock matrix formation  ***
    1    -230.8982516003082139     0.00e+00  5.01e-03  1.01e-01  1.12e-01  0.700   1.7
Warning: op=0 Small HOMO/LUMO gap (  -0.021) - skipping pre-diagonalization
         Will do a full diagonalization
    2    -230.9463607195993120    -4.81e-02  1.15e-03  2.59e-02  4.06e-02  0.700   1.6
                               ***Turning on AO-DIIS***
  ... etc.
   12    -231.0033984839932089    -5.02e-09  3.33e-07  7.37e-06  7.95e-06  0.000   1.1
                 **** Energy Check signals convergence ****

FOD:
 Fermi smearing:E(HOMO(Eh)) = -0.201252 MUE = -0.179318 gap=   1.119 eV

 N_FOD =  0.920364
```
较高的 $N_{FOD}$ 已表明存在强 SEC，
检查基于 $\rho^{FOD}(r)$ 的 Mulliken 约化轨道布居
（参见 [sec:spectroscopyproperties.pop.mulliken](#sec:spectroscopyproperties.pop.mulliken)）
可对分子中热电子的定域化获得初步印象。
第一个碳原子的打印结果如下：

```orca
------------------------------------------
FOD BASED MULLIKEN REDUCED ORBITAL CHARGES
------------------------------------------
  0 C s       :     0.006371  s :     0.006371
      pz      :     0.016375  p :     0.030785
      px      :     0.009893
      py      :     0.004516
      dz2     :     0.004248  d :     0.010308
      dxz     :     0.000254
      dyz     :     0.004855
      dx2y2   :     0.000860
      dxy     :     0.000091
      f0      :     0.000006  f :     0.000378
      f+1     :     0.000014
      f-1     :     0.000309
      f+2     :     0.000002
      f-2     :     0.000006
      f+3     :     0.000010
      f-3     :     0.000032
```

若需要其他布居分析输出，
请用户参阅 Löwdin 分析（[sec:spectroscopyproperties.pop.loewdin](#sec:spectroscopyproperties.pop.loewdin)），
它默认开启，使用该计算的总 SCF 密度，
在有限电子温度的情形下也是如此。

*p*-苯炔的 $\rho^{FOD}$ 图清楚地显示了显著且相当离域的 FOD（$^1A_g$），
这表明要对该分子进行可靠的计算研究，
需要使用多参考方法。

<a id="fig:pbenzyne_fod"></a>
!!! note "../../images/pbenzyne_fod.*"
    :width: 50%

    $p$-苯炔 $^1A_g$ 基态在 $\sigma=0.005$ e/Bohr$^{3}$ 下的 FOD 图
    （TPSS/def2-TZVP (T = 5000 K) 水平，FOD 以黄色表示）。

