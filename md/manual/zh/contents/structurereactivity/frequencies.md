```{index} Vibrational Frequencies
```

(sec:structurereactivity.frequencies)=
# 振动频率（Vibrational Frequencies）

振动频率计算既可通过 SCF 能量的解析微分获得，也可通过对解析梯度进行单侧或双侧数值微分获得，即适用于 Hartree–Fock 和 DFT 模型。对于没有解析梯度的方法，可以使用数值计算的梯度（关键词 `NumGrad`）来计算数值频率。请注意，这将是非常耗时的计算。

目前，解析 Hessian 只能对 SCF 计算。不过还有一些额外限制。解析 Hessian 不能用于：

- 双杂化泛函（Double-Hybrid functionals）
- RI-JK 近似

请注意，手册中有专门讨论振动光谱的独立章节（见 {ref}`sec:spectroscopyproperties.vib` 一节），其中包含更多示例，并描述了非谐效应、拉曼光谱、NRVS 以及同位素位移或简正模式可视化等内容的计算。

振动频率计算的使用相当简单：

```{literalinclude} ../../orca_working_input/C05S03_148.inp
:language: orca
```

在频率作业结束时，你会得到如下输出：

```orca
-----------------------
VIBRATIONAL FREQUENCIES
-----------------------

   0:         0.00 cm**-1
   1:         0.00 cm**-1
   2:         0.00 cm**-1
   3:         0.00 cm**-1
   4:         0.00 cm**-1
   5:         0.00 cm**-1
   6:       311.78 cm**-1
   7:       887.65 cm**-1
   8:      1225.38 cm**-1
   9:      1394.81 cm**-1
  10:      3624.88 cm**-1
  11:      3635.73 cm**-1
```

该输出由计算得到的振动频率、振动模式以及 298.15 K 下的热化学性质组成。在上面的例子中，有六个频率恒为零。这些频率对应于分子的转动和平动。它们在计算频率之前已从 Hessian 中投影掉，因此这些零值并不能说明所对角化的 Hessian 的质量。可以通过 %FREQ 下的 `PROJECTTR FALSE` 关闭该投影，使平动和转动的频率偏离零，而这些偏差代表了 Hessian 计算数值误差的度量。当存在例如外电场、使得精确的平动和/或转动模式具有非零频率时，会自动执行此操作（见 {ref}`sec:essentialelements.finEfield` 一节）。然而，在分子预期同时满足平动和转动不变性的正常情况下，计算热化学量（尤其是熵和吉布斯自由能）时**强烈不建议**关闭 `PROJECTTR`。这是因为当平动和转动模式的频率超过 `CutOffFreq`（默认为 1 cm$^{-1}$）时，它们对配分函数的贡献将按振动的公式计算。结果，计算出的熵不准确（因为把平动和转动当作振动处理），对数值噪声敏感，并且当平动和转动模式的（理论上为零的）频率越过 `CutOffFreq` 时尤其会出现有限的跳变。因此，用户需要手动关闭 `PROJECTTR` 的唯一情形是：当期望精确 Hessian 具有零平动和零转动频率，而用户想检查实际计算的 Hessian 的平动和转动本征值偏离零的程度。此类计算得到的热化学量可靠性较低，不应使用；即便它们与 `PROJECTTR TRUE` 的结果差别很大，也并不一定意味着后者不可靠。

在不使用 `PROJECTTR FALSE` 的情况下，所计算频率的可靠性必须通过比较不同收敛判据、增量、积分格点等条件下的计算来判断。频率中的数值误差可能达到 50 cm$^{-1}$，但在大多数情况下应小得多。显著的负频率表明能量超曲面上的鞍点，并证明优化并未得到能量极小值点。

注意（OBS）：默认情况下，通过施加"声学求和规则（acoustic sum rule）"（{cite}`shang_moving-grid_2020`）使 Hessian 具有平动不变性，这可减小来自 DFT 或 COSX 数值积分噪声的影响，但对于 Partial Hessian 和 Hybrid Hessian 则不适用。可通过 %FREQ 下的 TRANSINVAR FALSE 将其设为 false。

(sec:structurereactivity.frequencies.massdependencies)=
## 质量依赖性（Mass dependencies）

当然，计算出的频率取决于每个原子所使用的质量。虽然这可以在之后通过 `orca_vib` 程序（详见
{ref}`sec:spectroscopyproperties.vib.isotopeshifts` 一节）以及在几何输入中对每个原子单独设定，但人们可能更愿意使用一套精确的原子质量，而不是默认的原子量。这可通过 `!Mass2016` 关键词实现，它会使 ORCA 使用代表某元素最丰度同位素或（若所有同位素都不稳定）最稳定同位素的原子质量（例如氯用 $^{35}Cl$ 的质量，锝用 $^{98}Tc$ 的质量）。

:::{Note}
数值频率的计算对计算机机时和精度都有相当高的要求。为获得可靠的频率，请确保：

-   你的 SCF 紧密收敛。总能量至少 10$^{-7}$ Eh、密度 10$^{-6}$ 的收敛精度是理想的。

-   使用至少 `DEFGRID2`（默认）的格点。

-   使用双侧（即中心）差分会使计算时间增加一倍，但给出更准确、更可靠的结果。

-   像 DGauss/J 或 DeMon/J 这样的小型辅助基组可能无法得到完全收敛的频率（与不使用 RI 计算的频率相比差异可达 40 cm$^{-1}$）。Weigend 的 def2/J 通用辅助基组现已成为 ORCA 中的默认值（标量相对论计算则用 SARC/J），被认为能给出足够可靠的结果。

-   为了得到完全收敛的结果，可能需要收紧几何优化的收敛判据。

-   如果条件允许，将数值增量减小到 0.001 Bohr 左右。这对 SCF 计算的收敛特性提出了更高的要求，但也应给出更准确的数值二阶导数。若增量太小或太大，预期会有不准确的结果。
:::

解析频率的计算很耗内存。为控制内存消耗，必须设置 `%maxcore` 参数。例如 `%maxcore 8192`——表示计算时每个处理器使用 8 Gb 内存。用户应根据可用的计算机内存提供该值。为克服可能的内存不足，会自动引入基于 `%maxcore` 参数的分批处理。

数值频率计算是可重启的（但解析频率计算不可）。如果数值频率作业因某种原因中断，可以简单地从中断处继续，如下例所示：

```{literalinclude} ../../orca_working_input/C05S03_150.inp
:language: orca
```

:::{Note}

-   你不得更改理论水平、基组或计算的任何其他细节。任何更改都会产生不一致的、本质上无意义的 Hessian。

-   计算 Hessian 的几何结构必须完全相同。如果你是先做几何优化再做频率计算，则必须从优化后的几何结构重新开始数值频率计算。

-   数值频率可以在多进程模式下进行。更多信息请参见
    {ref}`sec:essentialelements.parallel.calling` 一节（"并行 ORCA 使用提示"）。

-   数值频率的重启将从上一次运行产生的结果文件（`BaseName.res.%5d.Type`，其中 `Type` 为 `Dipoles`、`Gradients`——以及在请求时的 `Ramans` 或 `Nacmes`）继续。请确保所有这些局域结果文件都被复制到你的计算目录中。若设置了重启但找不到局域文件，ORCA 将从头重新开始。若 ORCA 在磁盘上找到 Hessian 文件，则只会重复其后的分析。

-   Hessian 可以变换到冗余内坐标。更多信息见
    {ref}`sec:structurereactivity.optimization.internalcoords` 一节。
:::

(sec:structurereactivity.frequencies.scalingfactors)=
## 计算频率的标度因子（Scaling factors for computed frequencies）

将计算的振动频率与实验比较时，通常通过对计算的谐振频率进行标度来校正谐近似中未考虑的效应。

首先必须进行一次标准的频率计算。之后，磁盘上可以找到一个 .hess 文件。该文件包含一行频率标度因子，可手动修改：

```orca
$frequency_scale_factor
  0.90      <<<---- you change this to whatever you want
```

然后需要运行 `orca_vib`：

```orca
orca_vib  myjob_scaled_freq.hess
```

程序读取 Hessian，对其进行对角化并施加标度因子。生成该 Hessian 的实际输入中使用了什么标度因子无关紧要，因为 Hessian 会被重新对角化。为避免混淆，我们建议：如果目的是调整标度因子，请将输入中的标度因子保持为 1.0。不过即使不这样做也不会有不良后果。

(sec:structurereactivity.frequencies.restart)=
## 重启数值频率计算（Restarting Numerical Frequency calculations）

要重启数值频率计算，使用：

```orca
%FREQ 
  restart true
END
```

ORCA 会在运行计算的同一文件夹中查找 basename.res.{} 文件，检查哪些已经完成，并在需要的地方重新开始。


(sec:structurereactivity.frequencies.keywords)=
## 频率关键词列表（Frequencies keyword list）

在 ORCA 程序包中，通过数值或解析 Hessian 计算频率分别由 `orca_numfreq` 模块以及 `orca_propint`、`orca_scfresp` 和 `orca_prop` 模块的组合完成。

控制这些频率计算的参数可在 %freq 块中指定。
相关简单输入关键词见
{numref}`tab:structurereactivity.frequencies.keywords.simple`。

```orca
%freq

  # Flags to switch frequencies calculation on/off
        
  NumFreq    false   # numerical frequencies (available for all methods)
  AnFreq     false   # analytical frequencies (available for HF, DFT)
                     # (One of these options has to be set to true,
                     #  to request a freq calculation)
        
  ScalFreq   1.0     # Scaling factor for frequencies (default = 1.0)
                     # NOTE: Scaling is applied to the frequencies after they are 
                     #       calculated. SCALED frequencies will be stored in the 
                     #       .hess file and printed in the output file. 
                     #       In the .hess file you have accesss to the frequency 
                     #       scaling factor (see below). 
                             

  # Flags to control NumFreq calculation:
                                          
  CentralDiff  true    # use central differences [f(x+h)-f(x-h)]/2h - or - 
                       # use one-sided differences [f(x+h)-f(x)]/h 
  Restart      false   # restart a (numerical) frequency calculation
  DX           0.005   # increment h
  Increment    0.005   # increment h

  Hybrid_Hess  {...} end # calculate (numerical) Hybrid Hessian 
  Partial_Hess [...] end # calculate (numerical) Partial Hessian
        
        
  # Flags to control subsequent vibrational analysis:
        
  QuasiRRHO       true   # Evaluate Vibrational Entropy with 
                         # Quasi-Rigid Rotor Harmonic Oscillator
  QRRHORefFreq    25     # reference frequency used in the QuasiRRHO in cm-1
                         # default value is 100 from original paper
  CutOffFreq      1.0    # Threshold for frequencies to be considered 
                         # in spectra, thermochemistry and printout (cm-1)
  Temp        298.15     # run the thermochemistry calculations at user-defined
                         # temperatures (max 16 temperatures, separated by ',')
  T    290, 292, 295     # same as Temp
  
  XTBVPT2     True       # use XTB for the VPT2 correction of the IR 
  Delq           0.5     # the displacement in dimensionless coordinates used 
                         # during the VPT2
  
  TransInvar  True       # enforce translation invariance after
                         # calculating the Hessian?
  NumHessTransInvar True # enforce translation invariance while
                         # calculating the Hessian?
                  # NOTE: TransInvar does not reduce the computational cost of the
                  # Hessian, and can be applied to analytic as well as numeric
                  # Hessians. NumHessTransInvar reduces the number of gradients
                  # that need to be calculated by 6 (for two-sided differentiation)
                  # or 3 (for one-sided differentiation) for numeric Hessians, but
                  # has no effect for analytic Hessians.
  ProjectTR   True       # project out translation and rotation degrees of freedom
                         # in frequency calculation and thermochemistry analysis?
  
          
end
```


:::{raw} latex
\begingroup
\footnotesize
:::
(tab:structurereactivity.frequencies.keywords.simple)=
:::{flat-table} 振动频率计算的简单输入关键词
:class: footnotesize
* - 关键词
  - 说明
* - `Freq`
  - 执行解析频率计算（别名：`AnFreq`）
* - `NumFreq`
  - 执行数值频率计算
* - `Mass2016`
  - 使用最新（2016 年）的最丰度或最稳定同位素的原子质量，而非原子量
:::
:::{raw} latex
\endgroup
:::
