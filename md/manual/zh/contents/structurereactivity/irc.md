```{index} IRC
```

(sec:structurereactivity.irc)=
# 内禀反应坐标（Intrinsic Reaction Coordinate）

内禀反应坐标（Intrinsic Reaction Coordinate，IRC）是最小能量路径（minimum energy path）的一种特殊形式，它将一个过渡态（TS）与其下坡方向最近的中间体连接起来。因此，确定 IRC 的方法对于判定一个过渡态是否直接与给定的反应物和/或产物相连很有用。ORCA 中的实现遵循 Morokuma 及其合作者提出的方法。{cite}`Morokuma:JCP1977`
IRC 方法沿核坐标的梯度方向行进。由于在过渡态处梯度可忽略，必须首先基于 Hessian 的本征模式对过渡态结构做初始位移，以便进入梯度不可忽略的区域。对于初始位移，将频率最低的本征模式（hessMode=0）的本征矢量归一化，然后乘以 Scale_Displ_SD 进行缩放（默认情况下，该值的选取使得可预期的能量变化为 Init_Displ_DE）。通过将所得位移矢量（分别乘以 +1 和 -1）加到初始结构上，分别得到正向和反向两个初始位移。如果用户请求下坡方向（例如来自先前未收敛的 IRC 运行），则假定梯度非零，从而不执行初始位移。

初始位移之后，IRC 方法的迭代开始。每次迭代由两个主要步骤组成，每个步骤又由多次单点能和梯度计算组成：

1.  初始最速下降（steepest descent，SD）步：

    1.  将起始几何结构（G0）的梯度（grad0）归一化并乘以 Scale_Displ_SD 缩放，然后将所得位移矢量（SD1）施加到 G0 上。

2.  可选（若 SD_ParabolicFit 为 true）：如果 SD1 使能量升高，则沿位移矢量方向做线搜索：

        1.  将位移矢量 SD1 乘以 0.5（SD2 = 0.5 x SD1），再加到 G0 上。

        2.  利用三个单点能（G0、SD1 步之后和 SD2 步之后的几何结构）进行抛物线拟合，以找到能量最低的位移矢量（SD3）。SD3 与 SD1 和 SD2 方向相同，但长度可以不同。

        3.  关键词 Interpolate_only 控制 SD3 的长度是否必须介于 0 和 SD1 的长度之间。若如此，则最大长度由 SD1 决定，最小长度为零。

    3.  在所得几何结构 G1（G0+SD1 或 G0+SD3）处计算梯度（grad1）。

2.  可选（若 Do_SD_Corr 为 true）：对最速下降步的修正：

    1.  基于 grad0 和 grad1 计算一个矢量，它表示对第一个 SD（SD1 或 SD3）步的修正。该修正使几何结构更接近 IRC。

    2.  将该矢量归一化，乘以 Scale_Displ_SD_Corr 与 SD1 或 SD3 长度的乘积进行缩放，然后将所得位移矢量（SDC1）施加到 G1 上。

    3.  可选（若 SD_Corr_ParabolicFit 为 true）：

        1.  如果施加 SDC1 步后能量升高，则将 SDC1 乘以 0.5 缩放（SDC2 = 0.5 x SD1）；如果能量降低，则将 SDC1 乘以 2 缩放（SDC2 = 2 x SD1）。然后将 SDC2 加到 G1 上。

        2.  利用三个单点能（G1、SDC1 步之后和 SDC2 步之后的几何结构）进行抛物线拟合，以找到能量最低的位移矢量（SDC3）。SDC3 与 SDC1 和 SDC2 方向相同，但长度可以不同。

        3.  关键词 Interpolate_only 控制 SDC3 的长度是否必须介于 0 和 SDC1 的长度之间。若如此，则最大长度由 SDC1 决定，最小长度为零。

    4.  在所得几何结构 G2（G1+SDC1 或 G1+SDC3）处计算梯度（grad2）。

3.  检查新几何结构处的梯度是否收敛。

4.  可选（若 Adapt_Scale_Displ 为 true）：

    1.  如果所得总步长小于 Scale_Displ_SD 的 0.5 倍，则将 Scale_Displ_SD 乘以 0.5。

    2.  如果所得总步长大于 Scale_Displ_SD 的 2 倍，则将 Scale_Displ_SD 乘以 2。

    3.  Scale_Displ_SD 不得小于初始 Scale_Displ_SD 的 1/16，也不得大于初始 Scale_Displ_SD 的 4 倍。

## 基本用法（Basic Usage）

可用关键词如下：

```orcainput
! B3LYP SV(P) TightSCF KDIIS SOSCF Freq IRC 
* xyz 0 2
  C  -0.000   0.001   -0.000
  H   1.290   0.005   -0.006
  H  -0.330   1.050   -0.002
  H  -0.252  -0.532   -0.929
  H  -0.286  -0.545    0.911
  O   2.499   0.220    0.065
  H   2.509   1.085    0.525
*
```

:::{Note}
-   IRC 运行应使用与几何优化和频率计算相同的方法和基组。

-   IRC 关键词可以单独使用，也可以与 OptTS、ScanTS、NEB-TS、AnFreq 和 NumFreq 关键词一起使用。

-   在默认设置下，IRC 代码会检查在 IRC 运行之前是否已计算过 Hessian。若没有，且 %irc 块中也未定义 Hessian，则会在 IRC 运行开始时计算一个新的 Hessian。

-   会生成一条最终轨迹（\_IRC_Full_trj.xyz），它从一个端点出发到另一个端点，包含正向和反向两个方向，从而可视化整个 IRC。正向（\_IRC_F\_trj.xyz 和 \_IRC_F.xyz）与反向（\_IRC_B\_trj.xyz 和 \_IRC_B.xyz）的轨迹文件和 xyz 文件分别包含该次运行的 IRC 及其最后一个几何结构。
:::

(sec:structurereactivity.irc.keywords)=
## 关键词（Keywords）
```orca
! IRC
%irc
   MaxIter    20
   PrintLevel 1   
   Direction  both # both - default
                   # forward
                   # backward
                   # down
 # Initial displacement  
   InitHess   read # by default ORCA uses the Hessian from AnFreq or NumFreq, or
                   # computes a new one
                   # read    - reads the Hessian that is defined via Hess_Filename
                   # calc_anfreq  - computes the analytic Hessian
                   # calc_numfreq - computes the numeric Hessian 
   Hess_Filename "h2o.hess"  # input Hessian for initial displacement, must be used
                             # together with InitHess = read
   hessMode   0  # Hessian mode that is used for the initial displacement. Default 0                
   Init_Displ_DE      # DE (default) - energy difference
                      # length       - step size
   Scale_Init_Displ 0.1 # step size for initial displacement from TS. Default 0.1 a.u.
   DE_Init_Displ    2.0 # energy difference that is expected for initial displacement 
                        #  based on provided Hessian (Default: 2 mEh)
 # Steps
   Follow_CoordType cartesian # default and only option
   Scale_Displ_SD       0.15  # Scaling factor for scaling the 1st SD step
   Adapt_Scale_Displ    true  # modify Scale_Displ_SD when the step size becomes 
                              # smaller or larger
   SD_ParabolicFit      true  # Do a parabolic fit for finding an optimal SD step
                              # length
   Interpolate_only     true  # Only allow interpolation for parabolic fit, not
                              # extrapolation
   Do_SD_Corr           true  # Apply a correction to the 1st SD step
   Scale_Displ_SD_Corr  0.333 # Scaling factor for scaling the correction step to 
                              # the SD step. It is multiplied by the length of the 
                              # final 1st SD step
   SD_Corr_ParabolicFit true  # Do a parabolic fit for finding an optimal correction
                              # step length
 # Convergence thresholds - similar to LooseOpt
   TolRMSG   5.e-4      # RMS gradient (a.u.)
   TolMaxG   2.e-3      # Max. element of gradient (a.u.)
 # Output options   
   Monitor_Internals # Up to three internal coordinates can be defined 
      {B 0 1}        # for which the values are printed during the IRC run.
      {B 1 5}        # Possible are (B)onds, (A)ngles, (D)ihedrals and (I)mpropers
   end 
 end
```

注意（NOTE）

-   对于 direction=down（下坡）不需要初始位移，因此也不需要 Hessian。
