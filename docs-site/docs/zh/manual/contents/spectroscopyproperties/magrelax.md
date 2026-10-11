

<a id="sec:spectroscopyproperties.magrelax"></a>
# 磁弛豫（Magnetic Relaxation）

<a id="sec:spectroscopyproperties.magrelax.general"></a>
## 程序概述（General description of the program）

对于磁性分子，ORCA 现在提供了计算磁弛豫时间的可能性。
这通过 Orca_Magrelax 模块完成。
一般而言，对于具有电子自由度和振动自由度的体系，
哈密顿量可写为 [lunghi2017intra,atanasov2015smm](../../bibliography.md)：

$$
\begin{split}\hat{H} &= \hat{H}_{spin} + \hat{H}_{ph} + \hat{H}_{sph} \\\hat{H}_{sph} &= \sum_{\alpha} \frac{\partial \hat{H}_{spin}}{\partial Q_{\alpha}} \hat{Q}_{\alpha}+ \frac{1}{2}\sum_{\alpha \beta} \left( \frac{\partial^2 \hat{H}_{spin}}{\partial Q_{\alpha} \partial Q_{\beta}} \right) \hat{Q}_{\alpha} \hat{Q}_{\beta} + \dots \\
&=\sum_{\alpha} \hat{V}_\alpha \hat{Q}_{\alpha}+ \frac{1}{2}\sum_{\alpha \beta} \hat{V}_{\alpha,\beta} \hat{Q}_{\alpha} \hat{Q}_{\beta} + \dots \\\hat{H}_{ph} &= \sum_{\alpha} \hbar \omega_{\alpha} \left( \hat{n}_{\alpha} + \frac{1}{2} \right)
\end{split}
$$

其中 $\hat{H}_{spin}$ 是电子哈密顿量，$\hat{H}_{ph}$ 是声子（振动）哈密顿量。
前两项构成 Born-Oppenheimer 方法，
若哈密顿量只包含这些，则总波函数就只是电子波函数与声子波函数的乘积。
$\hat{H}_{sph}$ 项则引入电子部分与声子部分之间的相互作用，
使总波函数成为上述乘积态的线性组合。

声子哈密顿量可近似为谐振子。耦合项 $\hat{H}_{sph}$ 通常表示为 $\hat{H}_{spin}$ 的
Herzberg-Teller 展开。
文献中 $\hat{H}_{spin}$ 曾被表示为参数化自旋哈密顿量 [reta2021ab,kragskow2023spin](../../bibliography.md)，
更近的则表示为 CASSCF 哈密顿量 [mariano2025role](../../bibliography.md)。
在我们目前的方法中，QDPT 哈密顿量被用作 $\hat{H}_{spin}$
（[spectroscopyproperties.qdpt_magnetic_properties](#sec:spectroscopyproperties.qdpt_magnetic_properties)）。
这使得磁弛豫的从头算（无参数）第一性原理估计成为可能。
QDPT 矩阵的导数通过数值方法计算。
我们用费米黄金规则（Fermi golden rule）计算速率矩阵的矩阵元。

$$
\begin{split}
P_{FI}=\frac{2\pi}{\hbar} \in t|\langle F|\hat{H}_{pert}^{\mu}|I\rangle|^{2} \delta(E_F-E_I) \rho (E_F) dE_F
\end{split}
$$

其中 $\hat{H}_{pert}^{\mu}$ 是跃迁算符的 $\mu$ 阶微扰理论展开。
其表达式为 [timm2011time](../../bibliography.md)：

$$
\begin{split}
\hat{H}_{pert}^{\mu}=\sum_{\mu=1}^{\in fty}\hat{H}_{sph}(\frac{1}{E_I-H_0+i(0)^{+}}\hat{H}_{sph})^{(\mu-1)}
\end{split}
$$

由此可见，我们的实现依赖于两个无穷阶展开，
出于实际考虑必须以有限方式将它们截断。
第一个是 Herzberg-Teller 展开，第二个是微扰理论表达式。

<a id="fig:relaxation mechanisms"></a>
*电子与声子自由度之间能量交换的机制。*

若将两者都截断到一阶，我们就得到单声子过程的表达式，
也称为 Orbach 弛豫（Orbach Relaxation）。
若其中一个表达式截断到二阶，
则得到双声子过程的一个分量，
它们统称为拉曼过程（Raman processes）。
二阶 Herzberg-Teller 给出所谓的 Raman I 分量，
而二阶微扰理论给出 Raman II 分量。

Raman I 过程快速且振荡，在我们目前的实现中假定其平均为零 [lunghi2020limit](../../bibliography.md)。
这样就剩下 Orbach 过程（在较高温度下主导磁弛豫）
和拉曼过程（在较低温度下主导磁弛豫）。
Orbach 过程的速率方程如下 [lunghi2019phonons](../../bibliography.md)：

$$
\begin{split}
\Gamma_{FI}^{-}=\frac{\pi}{2\hbar} \sum_\alpha\in t|V_{FI}^\alpha|^{2} \bar{n}(\hbar \omega)\delta(\Delta E_{FI}-\hbar\omega) \rho_{\alpha} (\hbar\omega) d\hbar\omega\\
\Gamma_{Fi}^{+}=\frac{\pi}{2\hbar} \sum_\alpha\in t|V_{FI}^\alpha|^{2} (\bar{n}(\hbar \omega)+1)\delta(\Delta E_{FI}+\hbar\omega) \rho_{\alpha} (\hbar\omega) d\hbar\omega
\end{split}
$$

拉曼速率方程则变为 [lunghi2022toward](../../bibliography.md)：

$$
\begin{split}
\Gamma_{FI}^{--}=\frac{\pi}{\hbar} \sum_{\alpha,\beta}\in t\in t|\sum_{C}\frac{V_{FC}^\alpha}{\Delta E_{CI}-\hbar\omega'}+\frac{V_{CI}^\alpha}{\Delta E_{CI}-\hbar\omega}|^{2} \\
\bar{n}(\hbar \omega)\bar{n}(\hbar \omega')\delta(\Delta E_{FI}-\hbar\omega-\hbar\omega') \rho_{\alpha} (\hbar\omega)\rho_{\beta} (\hbar\omega') d\hbar\omega d\hbar\omega'\\
\Gamma_{FI}^{++}=\frac{\pi}{\hbar} \sum_{\alpha,\beta}\in t\in t|\sum_{C}\frac{V_{FC}^\alpha}{\Delta E_{CI}+\hbar\omega'}+\frac{V_{CI}^\alpha}{\Delta E_{CI}+\hbar\omega}|^{2} \\
(\bar{n}(\hbar \omega)+1)(\bar{n}(\hbar \omega')+1)\delta(\Delta E_{FI}+\hbar\omega+\hbar\omega') \rho_{\alpha} (\hbar\omega)\rho_{\beta} (\hbar\omega') d\hbar\omega d\hbar\omega'\\
\Gamma_{FI}^{-+}=\frac{\pi}{\hbar} \sum_{\alpha,\beta}\in t\in t|\sum_{C}\frac{V_{FC}^\alpha}{\Delta E_{CI}-\hbar\omega'}+\frac{V_{CI}^\alpha}{\Delta E_{CI}+\hbar\omega}|^{2} \\
(\bar{n}(\hbar \omega)+1)\bar{n}(\hbar \omega')\delta(\Delta E_{FI}-\hbar\omega+\hbar\omega') \rho_{\alpha} (\hbar\omega)\rho_{\beta} (\hbar\omega') d\hbar\omega d\hbar\omega'\\
\Gamma_{FI}^{+-}=\frac{\pi}{\hbar} \sum_{\alpha,\beta}\in t\in t|\sum_{C}\frac{V_{FC}^\alpha}{\Delta E_{CI}+\hbar\omega'}+\frac{V_{CI}^\alpha}{\Delta E_{CI}-\hbar\omega}|^{2} \\
\bar{n}(\hbar \omega)(\bar{n}(\hbar \omega')+1)\delta(\Delta E_{FI}+\hbar\omega-\hbar\omega') \rho_{\alpha} (\hbar\omega)\rho_{\beta} (\hbar\omega') d\hbar\omega d\hbar\omega'
\end{split}
$$

这里，$V_{FI}^\alpha=\langle F|\hat{V}^\alpha|I\rangle$ 是电子基下模式 $\alpha$ 的
线性自旋-声子耦合的矩阵元。
对声子模式采用 $\alpha\ge\beta$ 的约定是个方便的选择。
该约定在第一个求和号内引入一个 $(1-(\delta_{\alpha\beta}/2))$ 因子。
速率矩阵的对角元由 $\Gamma_{II}=\sum_{F\ne I}-\Gamma_{FI}$ 确定。
该速率矩阵可对角化，对每个弛豫模式 $k$ 给出本征值 $-\tau^{-1}_k$。
最小本征值对应体系处于平衡。
次小的值就是磁弛豫速率。

<a id="sec:spectroscopyproperties.magrelax.example"></a>
## 用 Orca_Magrelax 计算磁弛豫时间

Orca_Magrelax 既可从 ORCA 输入中使用，也可作为独立模块使用。
下面的示例展示如何针对一个 $[DyF_2]^{2+}$ 测试体系
从 ORCA 主程序运行这样的计算。
'dyf2casoptfreq' 是在 ORCA 中单独收敛的几何优化 + Hessian 计算，
而 'dyf2cas' 是在优化几何上收敛的 CASSCF 计算。
在 ORCA 内部使用 magrelax 需要在典型的 CASSCF 计算中作如下补充。
在 CASSCF 块内，必须将 'projectHSOC' 设为 true，
且关键词 'projectedstates' 必须设为磁体系最低多重态的多重度。
在本例中，最低多重态是 $^6H_{15/2}$ 态，多重度为 16。
在 CASSCF 的 rel 块中，关键词 'domagrelax' 必须设为 true。
'%qgprop' 块告知程序为 QDPT 矩阵计算数值导数。
然后 magrelax 块本身提供磁弛豫速率计算的额外细节。

```orca
!DKH2 DKH-def2-TZVP AutoAux moread
%moinp "dyf2cas.gbw"  # converged CASSCF single point calculation
 
%rel                  # picture change effects for DKH2
 picturechange 2
end
 

%basis                # SARC2 basis for the Dy atom
NewGTO Dy "SARC2-DKH-QZV" end
NewAuxGTO Dy  "SARC/J" end
end

%casscf               #CASSCF settings
   nel 9            # number of electrons in valence                      
   norb 7           # number of orbitals in valence
   mult 6           # list of multiplicities to be considered
   nroots 21        # number of roots corresponding to each multiplicity
   trafostep RI     # Use RI
   maxiter 400      # maximum iterations for CASSCF
   projectHSOC true # project H_SOC = QDPT matrix to the lowest multiplet
   projectedstates 16 # number of states in the lowest multiplet
   rel
   dosoc true       # enables generation of QDPT matrix
   domagrelax true  # stores data from the QDPT driver needed for magrelax
   end
end

%qgprop #quantized geometry properties module (generates derivatives of H_SOC)
MODE DERIV           # compute derivatives
COORDSTYPE ENWNORMAL # displace energy weighted distance along normal modes
STEPSIZE 0.00005     #  base displacement
HESSIAN "dyf2casoptfreq.hess" # hessian file
DERHSOC true         # property for which derivatives are needed (H_SOC)
end
 
%magrelax #magrelax settings
magfld 0.0, 0.0,0.01  # magnetic field in x, y, z directions (in Tesla)
           # use if casscf and qgprop blocks are in a separate file:
           # inputfile "dyf2test_magrelax2_maxsoc" 
HESSIAN "dyf2casoptfreq.hess" # hessian file
temperature 2,150,1   # temperature range start, finish, step size (K)
degenThresh 0.1       # energy threshold for detecting degeneracy (in cm-1)
doRaman false         # orbach is always true raman can be selected
gridMax 8000          # upper limit of integration (Raman only)
gridMin 0             # lower limit of integration (Raman only)
nGrid 2000            # no of integration grid points of integration (Raman only)
keepData true         # keep coupling constants for future runs
end
 
*xyzfile 1 6 dyf2casoptfreq.xyz   #optimized geometry
```

每次从 ORCA 运行 magrelax 时，它都会生成一个 magrelax 输入文件，
可对其加以修改以针对不同的实验条件运行。
它会读取前次运行所生成的文件。
该文件包含所有可在 ORCA 内部调用的关键词，
每行旁边以注释加以说明。
只要主 ORCA 程序在 path 目录中，
该文件即可从命令行以 'orca_magrelax dyf2.magrelaxinp' 运行。

```orca
none #DMAGRELAXINP InputFile
dyf2casoptfreq.hess             #DMAGRELAXINP Hessfile
2.000000 150.000000 1.000000    #DMAGRELAXINP templist start, stop, stepsize
0.000000 0.00000000 0.010000    #DMAGRELAXINP magfld x, y, z
1 0 1 0                         #DMAGRELAXINP ratemodes, doRaman, keepData, debug
0.10                            #DMAGRELAXINP degenThresh
1000.00 0.00 1000               #DMAGRELAXINP gridmax, gridmin, ngrid
10.00                           #DMAGRELAXINP gamma
```

<a id="sec:spectroscopyproperties.magrelax.modules"></a>
## 在各模块中运行 Orca_Magrelax 计算

也可在其他产生 QDPT 矩阵的 ORCA 模块（如 NEVPT2 或 HQD-NEVPT2）中计算磁弛豫。
这些只需在 CASSCF 中简单启用，就会自动用于 magrelax 计算。
对于涉及 %mrci 块的计算，magrelax 关键词不得放在 CASSCF 块中，
而应放在相应的 mrci 输入块中。
若运行的是需要 mrci 块的计算（如 MREOM、MRCEPA 或 MRACPF），
则 magrelax 相关关键词仍应放在 mrci 块中。

```orca
!DKH2 DKH-def2-TZVP AutoAux moread
%moinp "dyf2cas.gbw"  # converged CASSCF single point calculation
 
%rel                  # picture change effects for DKH2
 picturechange 2
end
 

%basis                # SARC2 basis for the Dy atom
NewGTO Dy "SARC2-DKH-QZV" end
NewAuxGTO Dy  "SARC/J" end
end

%casscf               #CASSCF settings
   nel 9            # number of electrons in valence                      
   norb 7           # number of orbitals in valence
   mult 6           # list of multiplicities to be considered
   nroots 21        # number of roots corresponding to each multiplicity
   trafostep RI     # Use RI
   maxiter 400      # maximum iterations for CASSCF
   projectHSOC true # project H_SOC = QDPT matrix to the lowest multiplet
   projectedstates 16 # number of states in the lowest multiplet
   rel
   dosoc true       # enables generation of QDPT matrix
   domagrelax true  # stores data from the QDPT driver needed for magrelax
   end
end

%qgprop #quantized geometry properties module (generates derivatives of H_SOC)
MODE DERIV           # compute derivatives
COORDSTYPE ENWNORMAL # displace energy weighted distance along normal modes
STEPSIZE 0.00005     #  base displacement
HESSIAN "dyf2casoptfreq.hess" # hessian file
DERHSOC true         # property for which derivatives are needed (H_SOC)
end
 
%magrelax #magrelax settings
magfld 0.0, 0.0,0.01  # magnetic field in x, y, z directions (in Tesla)
           # use if casscf and qgprop blocks are in a separate file:
           # inputfile "dyf2test_magrelax2_maxsoc" 
HESSIAN "dyf2casoptfreq.hess" # hessian file
temperature 2,150,1   # temperature range start, finish, step size (K)
degenThresh 0.1       # energy threshold for detecting degeneracy (in cm-1)
doRaman false         # orbach is always true raman can be selected
gridMax 8000          # upper limit of integration (Raman only)
gridMin 0             # lower limit of integration (Raman only)
nGrid 2000            # no of integration grid points of integration (Raman only)
keepData true         # keep coupling constants for future runs
end
 
*xyzfile 1 6 dyf2casoptfreq.xyz   #optimized geometry
```

<a id="sec:spectroscopyproperties.magrelax.FAQ"></a>
## 常见问题的解决（Fixing common issues）
* 单点计算崩溃：QGPROP 会对每个振动模式生成 2 个几何结构。
  这会得到 $(3N-6)\times 2$ 个需要用单点能计算的几何结构。
  它们命名为 '\<Basename\>.geom-\<geometry index\>'。
  如有需要，用户可用修改后的设置重跑任何未成功运行的几何结构。
* 修改后的设置未在线性自旋-声子耦合常数计算中生效：
  每次运行 QGPROP 时，它会检查位移几何是否已在前次运行中收敛。
  若找到已收敛的文件，则不会重新计算以节省机时。
  若用户不需要前次运行的数据，在 magrelax 块中设置 'keepData false'
  会在每次运行后删除 magrelax 和 qgprop 相关数据。
* 积分网格：拉曼计算涉及对声子能量的数值积分。
  上限、下限和网格点数可用关键词 'gridMax'、'gridMin' 和 'nGrid' 选择。
* 微分网格：由于线性导数是数值计算的，
  给 qgprop 的步长会影响结果的数值稳定性。
  目前，每个振动模式的位移按能量的倒数加权。
  qgprop 中的 'Stepsize' 关键词可用于对 1 埃的基础位移进行缩放。
* 磁场未对齐：当前实现要求用户输入的磁场与各向异性轴平行。
  CASSCF 中的基态 KD g 张量提供一个转动矩阵，
  可用于从分子坐标系 z 轴进行旋转。

<a id="sec:spectroscopyproperties.magrelax.keywords"></a>
## Magrelax 关键词（Magrelax Keywords）

<a id="tab:spectroscopyproperties.magrelax.method.keywords"></a>
!!! note "与 Magrelax 计算相关的 `%method` 块输入关键词"
    | 关键词             | 选项          | 说明                                       |
    |:-------------------|:--------------|:-------------------------------------------------|
    | `domagrelax`       | `true`        | 存储 magrelax 所需的数据                         |
    | `projectHSOC`      | 'true'        | 将 QDPT 基态多重态投影（总是为 true）            |
    | `projectedstates`  | number        | 基态多重态的多重度                               |

<a id="tab:spectroscopyproperties.magrelax.qgprop.keywords"></a>
!!! note "与 Magrelax 计算相关的 `%qgprop` 块输入关键词"
    | 关键词             | 选项          | 说明                                       |
    |:-------------------|:--------------|:-------------------------------------------------|
    | `MODE`             | `DERIV`       | 计算导数                                         |
    | `COORDSTYPE`       | `ENWNORMAL`   | 对简正模式使用能量加权位移                       |
    | `STEPSIZE`         | number        | 未加权步长的缩放因子                             |
    | `HESSIAN`          | name          | Hessian 文件名                                   |
    | `DERHSOC`          | `true`        | 计算含 SOC 的 QDPT 哈密顿量的导数                |

<a id="tab:spectroscopyproperties.magrelax.magrelax.keywords"></a>
!!! note "与 Magrelax 计算相关的 `%magrelax` 块输入关键词"
    | 关键词             | 选项          | 说明                                       |
    |:-------------------|:--------------|:-------------------------------------------------|
    | `magfld`           | vector        | 磁场（T）                                        |
    | `inputfile`        | name          | 当跳过 casscf 和 qgprop 时，数据的输入文件名（无扩展名）（可选）|
    | `HESSIAN`          | name          | Hessian 文件名                                   |
    | `temperature`      | start, end, step| 温度起始、终止、步长（K）                      |
    | `degenThresh`      | threshold     | 简并阈值（此范围内的态被忽略）（cm-1）           |
    | `doRaman`          | 'true'/'false'| 包含拉曼弛豫（Orbach 总是开启）                  |
    | `gridMax`          | number        | 数值积分上限（仅拉曼）                           |
    | `gridMin`          | number        | 数值积分下限（仅拉曼）                           |
    | `nGrid`            | number        | 数值积分的网格点数（仅拉曼）                     |
    | `keepData`         | 'true'/'false'| 保留 magrelax 生成的数据以供后续运行             |

