```{index} DMRG, BLOCK Interface
```

(sec:modelchemistries.dmrg)=
# 密度矩阵重整化群（Density Matrix Renormalization Group，DMRG）

::: center
*ORCA 中的 `BLOCK` 代码仅在 Linux 平台上可用！*
:::

`BLOCK` 是 Chan 课题组密度矩阵重整化群（density matrix renormalization
group，DMRG）算法的一种实现。
{cite}`chan2002jcp,chan2004jcp,gosh2008jcp,sharma2012jcp,sharma2011AnnRev`
使用本程序的这一部分时应引用所列文献。`BLOCK` 是平台相关的，过去曾有若干崩溃报告。
若你受到影响，请联系 [`BLOCK` 开发者](https://github.com/sanshar/Block)。

DMRG 是一种变分波函数方法。它可以被看作：(i) 处理大完全活性空间（complete
active space）中强关联（strong correlation）的有效方法；(ii) 系统逼近大数目
电子与轨道的 FCI 的蛮力方法；(iii) 在链、环等准一维（pseudo-one-dimensional）
分子中以多项式代价获得精确相关能的途径。

尽管与许多量子化学方法相比该算法略显复杂，`BLOCK` 中已投入大量精力确保它可以
以简单的黑箱（black-box）方式运行。在大多数情况下只需指定一个关键词。

为给出 DMRG 如何使用的大致概念，下面是一些示例。计时会随你的计算环境而变化，
但以下计算在单个 12 核 Xeon Westmere 集群节点上从数小时到一天不等：

-   对于活性空间中最多 30 个电子在 30 个活性轨道中的完全活性空间（CAS）CI
    计算，目标态数为 1--10 个，例如 Jacobsen 催化剂在 32 电子、25 轨道的活性空间中，

-   "宽度"最多 4 个轨道、总计约 100 个轨道的一维链分子，
    例如 4$\times$25 石墨烯纳米带（graphene nanoribbon）的 $\pi$ 活性空间，

-   少于 20 个电子、最多 100 个轨道的分子中的 FCI 基准解，
    例如 cc-pVTZ 基组下 D$_{\text{2h}}$ 对称的 C$_2$（12 个电子在 60 个轨道中），

-   能量差或总能量的精度约为 1 kcal/mol。

以下计算用 `BLOCK` 代码是可行的，但具有挑战性，且需要大内存
（例如每核高达 8 GB）和大量计算时间（例如在多达 6 个 12 核 Xeon Westmere
节点上从一天到一周以上不等），

-   在约 40 个电子、40 个活性轨道的活性空间中进行完全活性空间（CAS）CI 计算，
    目标为若干个态，例如 Fe(II)-卟啉（Fe(II)-porphine，38 个轨道中 40 个电子），
    活性空间为 Fe 3d、4d 以及卟啉所有 $\pi$ 与 $\sigma$ 供体轨道；
    或者 \[Fe$_4$S$_4$(SCH$_3$) $_4$\]$^{2-}$ 的 Fe 3d、S 3p 活性空间计算，

-   "宽度"最多 6 个轨道、总计约 100 个轨道的一维链分子，

-   小分子中顶级的 FCI 基准解，例如 cc-pVDZ 基组下的丁二烯（butadiene）
    （82 个轨道中 22 个电子），

-   能量差或总能量的精度约为 1 kcal/mol。

如果你对上述任何计算感兴趣，不妨用 `BLOCK` 试一次 DMRG 计算！

## 技术能力（Technical capabilities）

目前 `BLOCK` 实现了如下功能

-   面向量子化学哈密顿量的高效 DMRG 算法

-   完全自旋适配（spin-adaptation，SU(2) 对称性）与阿贝尔点群对称性

-   态平均激发态（state-averaged excited state）

注意，`BLOCK` 的独立版本可能提供比外部接口更多的功能。详见 `BLOCK`
网站{cite}`chan`。

(sec:modelchemistries.dmrg.papers)=
## 如何引用（How to cite）

若在使用 `BLOCK` 的成果发表中引用以下论文，我们将不胜感激：

-   G. K.-L. Chan and M. Head-Gordon, *J. Chem. Phys.* **116**, 4462
    (2002),

-   G. K.-L. Chan, *J. Chem. Phys.* **120**, 3172 (2004),

-   D. Ghosh, J. Hachmann, T. Yanai, and G. K.-L. Chan, *J. Chem.
    Phys.*, **128**, 144117 (2008),

-   S. Sharma and G. K-.L. Chan, *J. Chem. Phys.* **136**, 124121
    (2012).

此外，Chan 与 Sharma 的下述综述中可以找到与量子化学相关的有用 DMRG 文献。

-   G. K-.L. Chan and S. Sharma, *Ann. Rev. Phys. Chem.* **62**, 465
    (2011),
(sec:modelchemistries.dmrg.commands)=
## 基本用法（Basic Usage）

在 ORCA 中，`BLOCK` 程序作为 CASSCF 模块的一部分来调用。`BLOCK` 可以两种模式
运行：CASCI 模式（不做轨道优化）或 CASSCF 模式。要启用 CASCI 模式，设置
`maxiter 1`。

```orca
%casscf
   maxiter 1 # remove if doing CASSCF
   CIStep DMRGCI
   ...
   end
```

对小分子的 CASCI 计算，或许可以将所有轨道都纳入相关。一般而言，与标准 CASSCF
计算类似，需要选择一个合理的活性空间来进行相关（关于 CASSCF，参见
{ref}`sec:modelchemistries.dmrg.commands.casscf` 一节）。这是用户的责任。

一旦选定了要相关的轨道，并指定了波函数对称性与量子数，DMRG 计算的精度便由两个
参数控制：最大重整化态数（number of renormalized states）$M$，以及轨道的顺序与定域性。

DMRG 计算中最重要的参数是 $M$，即重整化态数。它定义了波函数展开的最大长度，
在重整化基下为 $O(M^2)$。随着 $M$ 增大，DMRG 能量收敛到精确（FCI 或 CASCI）极限。

DMRG 将轨道映射到一维格点（lattice）上，因此若把强相互作用的轨道彼此相邻放置，
结果最佳。因此，DMRG 能量一般不对活性空间内的轨道旋转不变，轨道旋转与排序可以
改进给定 $M$ 下的 DMRG 能量。随着 $M$ 增大，DMRG 能量对轨道顺序与定域性越来越不敏感。

为尽量减少波函数优化步数，通常宜先以较小的 $M$ 进行 DMRG 计算，然后再把 $M$
增加到最终的最大值。这一优化序列由 *sweep 调度*（sweep schedule）控制，
它规定在每个中间 $M$ 值下执行多少个优化步（sweep）。

上述内容也许使 DMRG 计算看起来比通常的量子化学计算更复杂，然而 `BLOCK` 提供了
一组默认设置，无需手动指定上述参数。我们强烈建议你先*在这些默认设置下*学习使用
`BLOCK` 程序。在默认模式下，轨道会被自动排序（Fiedler 向量方法
{cite}`Fiedler1973,Fiedler1975,Atkins1998,Barcza2011`），并设置默认的 sweep 调度。

下面是 C~2~ 分子在 VTZ 基组下关联所有电子的默认 CASCI 计算示例：

```{literalinclude} ../../orca_working_input/C06S12_405.inp
:language: orca
```

熟悉默认模式后，我们建议探索轨道的定域化。一般而言，DMRG 受益于使用定域轨道
（localized orbital），除非分子的高对称性（例如 D$_{2h}$ 对称性）能提供补偿性的
计算优势，否则都应使用定域轨道。我们建议使用"分离定域"（split-localized）轨道，
即分别对占据轨道与虚拟轨道进行定域化。关于卟啉（porphine）分子在 cc-pVDZ 基组下
关联完整 $\pi$ 空间（24 个轨道中 26 个电子）的分离定域默认 DMRG 计算示例，
见 {ref}`sec:dmrg.orcaporphine.detailed` 一节。

对于给定的 `maxM`，将 DMRG 计算紧收敛（例如到默认的 1e-9 容差）可能需要很长时间。
为缩短计算时间，你可以放宽默认的紧 sweep 容差，或用命令 `sweeptol` 与 `maxIter`
控制 sweep 迭代的最大次数。

(sec:modelchemistries.dmrg.commands.casscf)=
### 轨道优化（Orbital optimization）

DMRG 计算中的轨道优化（将外部/内部空间与活性空间混合，不要与活性空间内的轨道
旋转和排序混淆）可以通过在 CASSCF 计算中把 `BLOCK` 程序用作 "CIStep" 来实现，
如上所述。目前，该 `CIStep` 尚不提供自旋密度及相关性质。

在优化迭代过程中，重要的是活性轨道与前一次迭代保持重叠与排序。这是用
`actConstrains` 实现的。该标志默认设置。

```orca
%casscf
ActConstrains  1 # maintain shape and ordering of active orbitals
...
end
```

一般而言，带轨道优化的 DMRG 计算相当昂贵。因此，通常最好用较小的 `maxM` 值
（由默认参数 `maxM=25` 及相应的 sweep 调度启用）进行轨道优化，然后用较大的
`maxM` 值进行最终的单点计算。

### 高级选项（Advanced options）

有时可能需要对 DMRG 计算作更精细的控制。所有关键词见下文的 *BLOCK 完整选项集*
{ref}`sec:modelchemistries.dmrg.commands.block`。命令 `startM` 允许更改 DMRG 计算
的起始态数。也可以手动指定整个 sweep 调度。下面是一个 sweep 调度示例：

```orca
%casscf
   ...
  dmrg

    MaxIter          14
    switch_rst       1e-3
    TwoDot_to_oneDot 12
    NSchedule        3
    sche_iteration   0,     4,    8
    sche_M          50,   100,  500
    sche_sweeptol 1e-4,  1e-6, 1e-9
    sche_noise    1e-8, 1e-11,  0.0

  end
end
```

上述命令为：

-   `MaxIter`，对应 DMRG 执行的 sweep 最大次数；

-   `NSchedule`，指定我们将给出的调度参数总数；

-   `Sche_iteration`，详细说明在哪个 sweep 号上更改计算参数。注意计数从 0 开始；

-   `Sche_M`，是每次 sweep 的重整化态数；

-   `Sche_sweeptol`，是 Davidson 算法的容差；

-   `Sche_noise`，是我们每次 sweep 添加的微扰噪声量；

-   `Twodot_to_onedot`，指定从 twodot 算法切换到 onedot 算法的 sweep 号。
    推荐的选择是以 twodot 算法开始，在达到最大 $M$ 之后的几次 sweep 切换到
    onedot 算法。若要完全用 twodot 或 onedot 算法进行计算，请将
    `twodot_to_onedot` 行替换为 `twodot 1` 或 `onedot 1`；

-   `switch_rst`，定义轨道梯度（orbital gradient）的切换阈值，低于该阈值时
    DMRG 转向 onedot 算法，并从之前的算符与波函数重新启动。这对于避免轨道优化中
    能量值的振荡至关重要。

默认的 DMRG sweep 调度根据计算模式的选择自动确定。默认情况下，CASCI 与 CASSCF
计算分别支持两组不同的预定义调度。

在 CASCI 模式下，默认调度对应如下：从给定的 `startM` 开始（默认为 250 且 8 次 sweep），
增加到 1000（8 次 sweep），然后每 4 次迭代递增 1000，直到达到 `maxM`。
在达到 `maxM` 之后两次 sweep，算法从 twodot 切换到 onedot。

在 CASSCF 模式下，轨道优化在相对于轨道旋转的波函数收敛上所需的重整化态少得多。
因此默认调度以 `startM` 开始（默认为 25 且 2 次 sweep），每 2 次 sweep 递增 2 倍，
直到达到 `maxM`。算法在 `maxM` 处继续 sweep，每 2 个循环将 Davidson 容差
`sche_sweeptol` 与噪声水平 `sche_noise` 降低 10 倍，直到 `sche_sweeptol` 小于
`sweeptol`。

为了更好地控制轨道排序，我们还提供了加权交换矩阵（weighted exchange matrix）
的遗传算法（genetic algorithm）最小化方法。遗传算法通常给出优于默认排序的轨道顺序，
但当轨道数目很大时它本身也可能需要一些运行时间。可以通过如下方式启用遗传算法

```orca
%casscf
   ...
   DMRG
     auto_ordering GAOPT
   end
end
```

在 `%casscf` 输入中设置。

### 故障排查（Troubleshooting）

DMRG 计算最常见的两个问题是：(i) 随 `maxM` 的收敛比期望的慢，或 (ii) DMRG sweep
陷入局域极小值（local minimum）。(i) 由轨道顺序/轨道选择控制。为改进收敛，请开启
遗传算法的轨道排序。

若怀疑发生了 (ii)，最简单的做法是用 `startM` 增加起始态数（例如从 500 增加到
1000 个态）。局域极小值有时也可以通过增大 DMRG 调度中的噪声来避免，例如增大
10 倍。为检查是否陷入局域极小值，可以进行 DMRG 外推（详见 `BLOCK` 网站上的扩展手册）。

注意，当前的 DMRG-SCF 依据 Hartree-Fock 占据数（occupancy）来确定活性空间轨道的
输入顺序，即使这些轨道最终本质上是正则（canonical）或分离定域正则的。
这是由 `hf_occ` 指定的，其中 Hartree-Fock 占据数默认由单电子积分导出。
获取占据数的其他选项也可用（见
{ref}`sec:modelchemistries.dmrg.commands.block`）。

有时从一个 SCF 循环到下一个 SCF 循环产生的能量值可能会振荡。这种非线性数值行为
通常出现在最后几次迭代中，很可能是由于在分块与抽稀（blocking and decimation）
过程中因多体基不完全而丢失了某些量子数分布（例如粒子数、不可约表示对称性与自旋）。
另一方面，量子数的丢失是使用较少重整化态数的 DMRG-SCF 所计算势能曲线上能量不连续的
主要来源。

在当前 DMRG-SCF 实现版本中，量子态数被锁定（lock）以避免这些问题。当轨道梯度
低于由关键词 `switch_rst`（默认：0.001）定义的某个阈值时，锁定机制开启。
随后 DMRG 计算从之前的算符与波函数开始，且不添加微扰噪声。锁定量子态并重新启动
DMRG 波函数不仅能确保向最终能量的平滑收敛，还能使迭代次数最少。注意，在使用非常
小的 $M$ 时，锁定过程会给最终能量引入任意性，因为能量的最后几位数字取决于锁定
从何处开始。因此不建议在迭代中过早开始锁定，那可能将轨道解困在局域极小值中。
最后，可以通过用足够多的重整化态数进行一次 DMRG 计算来检查所得轨道的质量。
使用 `switch_rst` 默认值时，DMRG-SCF 通常得到足以复现 CASSCF 能量的轨道。

(sec:modelchemistries.dmrg.commands.block)=
## 关键词（Keywords）

```orca
%casscf
 ...
 # enable DMRG as CI solver (mandatory)
 CIStep DMRGCI
 
 # refined optional settings for DMRG
 dmrg
 startM   25     # CASSCF mode: number of re-normalized states for a singlee root
          250    # CASCI mode: number of re-normalized states for a single root
 maxM     25     # CASSCF mode: number of re-normalized states for a singlee root
          250    # CASCI mode: number of re-normalized states for a single root
 DryRun   false  # just create an input for Block
 SweepTol 1e-9   # energy tolerance for the sweeps 
 auto_ordering NOREORDER # auto_ordering is an int. If set to 0
                         # or the alias NOREORDER, the reordering is skipped.
               FIEDLER   # (default) let Block optimize the active orbital ordering
               GAOPT     # let Block optimize the active orbital ordering
                         # using genetic algorithm
 hf_occ   0 # user-defined initial Hartree-Fock occupancy manually
          1 # default: initial Hartree-Fock occupancy based on the values of 
              the one-electron integrals
          2 # initial Hartree-Fock occupancy based on the energy ordering 
              of canonical orbitals

 TwoDot_to_OneDot  1  # Switch from two-dot expressions to one-dot
 OneDot  0   # Only one-dot expressions. %In CASCI mode only.
 TwoDot  0   # Only two-dot expressions. %In CASCI mode only.
 switch_rst 1e-3   # Specify the threshold of orbital gradient below which DMRG
                     swithches to one-dot expression by reading previous wavefunction.
 warmup  1   # wilson warm-up type
         2, 3 or 4   # n=3 is the default option. 
                       The full configuration space of the n sites next to the system 
                       constitutes the environment states in the warm-up. 
                       The remaining sites use the Hartree-Fock guess occupation
 nonspinadapted 0   # default: spin-adapted DMRG
                1   # non-spin-adatped DMRG in which the spin-density calculation 
                      is available
                

 # Define a schedule for DMRG
 MaxIter   14   # Specify maximum number of iterations
 NSchedule -1   # default sweep schedule in CASSCF mode 
            0   # default sweep schedule in CASCI mode
           >0   # Number of manual sweep schedule parameters 
                # All schedule parameters must be set if this flag is set manually!
 sche_iteration 0, 4, 8   # vector with sweep-number to execute changes
                          # (schedule parameter)

 sche_M       50,100,500 # vector with corresponding M values (schedule parameter)
 sche_sweeptol 1e-4,1e-6,1e-9  # vector with sweep tolerances (schedule parameter)
 sche_noise     1e-8, 1e-11,0.0 # vector with the noise level (schedule parameter)

 # Define a separate maxM for DMRG-NEVPT2
 nevpt2_maxm 25   # set maximum number of renormalized states 
                    for DMRG-NEVPT2 calculation (default: MaxM)

 end
end
```

(sec:dmrg.orcaporphine.detailed)=
## 示例：卟啉 $\pi$ 活性空间计算（Example: Porphine $\pi$-active space calculation）

我们给出关于定域化卟啉分子 $\pi$ 轨道并在该体系上运行 CASSCF-DMRG 计算的逐步基础流程。
重要的是获得一组初始轨道、旋转将要定域化的轨道、对它们进行定域化，最后运行 CASSCF 计算。
在第一个输入文件中展示坐标之后，我们将坐标缩写为 $\left[\dots\right]$，
但请注意它们始终需要包含在内。

1.  首先获得 RHF 轨道：

    ```orcainput
    # To obtain RHF orbitals 
    !cc-pVDZ 
    * xyz 0 1
    N      2.10524     -0.00000     0.00000 
    N     -0.00114      1.95475    -0.00000
    N     -2.14882      0.00000    -0.00000 
    N     -0.00114     -1.95475     0.00000
    C      2.85587     -1.13749    -0.00000
    C      2.85587      1.13749     0.00000 
    C      1.02499      2.75869    -0.00000 
    C     -1.10180      2.78036     0.00000
    C     -2.93934      1.13019    -0.00000
    C     -2.93934     -1.13019     0.00000
    C     -1.10180     -2.78036    -0.00000
    C      1.02499     -2.75869     0.00000
    C      4.23561     -0.67410    -0.00000
    C      4.23561      0.67410     0.00000 
    C      0.69482      4.18829    -0.00000 
    C     -0.63686      4.14584    -0.00000 
    C     -4.25427      0.70589    -0.00000 
    C     -4.25427     -0.70589     0.00000
    C     -0.63686     -4.14584     0.00000 
    C      0.69482     -4.18829     0.00000
    H      5.10469     -1.31153     0.00000 
    H      5.10469      1.31153    -0.00000
    H      1.36066      5.02946     0.00000 
    H     -1.28917      5.00543     0.00000 
    H     -5.12454      1.34852     0.00000 
    H     -5.12454     -1.34852    -0.00000 
    H     -1.28917     -5.00543    -0.00000 
    H      1.36066     -5.02946    -0.00000 
    C      2.46219      2.41307     0.00000 
    C     -2.39783      2.44193     0.00000 
    C     -2.39783     -2.44193    -0.00000 
    C      2.46219     -2.41307    -0.00000 
    H      3.18114      3.22163    -0.00000 
    H     -3.13041      3.24594    -0.00000 
    H     -3.13041     -3.24594     0.00000 
    H      3.18114     -3.22163     0.00000
    H      1.08819      0.00000    -0.00000 
    H     -1.13385     -0.00000     0.00000 
    *  
    ```

2.  接着交换具有 $\pi$ 特征的轨道，使它们在活性空间中彼此相邻。
    （$\pi$ 轨道通过查看 MO 系数来识别。）当它们在活性空间中相邻时，
    就可以在下一步中容易地对它们进行定域化。

    ```orca
    #To rotate the orbitals (so that we can localize them in the next step) 
    !cc-pvdz moread noiter 
    %moinp "porphine.gbw" 
    %scf 
        rotate 
        # Swap orbitals
        {70, 72}
        {65, 71}
        {61, 70}
        {59, 69}
        {56, 68}
        {88, 84}
        {92, 85}
        {93, 86}
        {96, 87}
        {99, 88} 
        {102, 89}
        {103, 90}
        {104, 91}
        end
    end 
    * xyz 0 1
    [...] 
    *
    ```

3.  旋转轨道后，我们对 13 个占据 $\pi$ 轨道进行定域化。这通过 `orca_loc` 代码
    执行。输入文件如下。

    ```orca
    porphine_rot.gbw 
    porphine_loc.gbw 
    0
    68
    80
    120
    1e-3
    0.9
    0.9
    1
    ```

4.  定域化占据轨道之后，我们再次使用 `orca_loc` 代码对 11 个虚拟 $\pi$ 轨道
    进行定域化。输入文件如下。
    
    ```orca
    porphine_loc.gbw
    porphine_loc2.gbw
    0
    81
    91
    120
    1e-3
    0.9
    0.9
    1
    ```

5.  上述步骤完成后，我们运行 CASSCF-DMRG 计算。标准输入文件如下所示

    ```orca
    !cc-pVDZ moread pal4 
    %moinp "porphine_loc2.gbw" 
    %MaxCore 16000

    %casscf nel 26
    norb 24
    nroots 1
    CIStep DMRGCI 
    end 
    * xyz 0 1
    [...] 
    *
    ```
