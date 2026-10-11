```{index} Utilities
```

(sec:utilities)=
# 辅助程序（Utility Programs）

:::{tabularcolumns} \Y{0.20}\Y{0.80}
:::

:::{list-table}
* - orca_2aim
  - 生成适用于 AIM 分析的 WFN 和 WFX 文件
* - orca_2json
  - 将 gbw 文件中的信息转换为 JSON 文件
* - orca_2mkl
  - 生成供 molekel、molden 或其他可视化程序读取的 ASCII 文件
* - orca_asa
  - 计算吸收、荧光和共振拉曼光谱的谱带形状
* - orca_chelpg
  - 计算由静电势导出的电荷
* - orca_euler
  - 从 `.property.txt` 文件计算 Euler 角
* - orca_exportbasis
  - 以 ORCA 或 GAMESS-US 格式打印任何基组
* - orca_fitpes
  - 拟合双原子分子的势能曲线
* - orca_mapspc
  - 生成用于传入绘图程序的文件
* - orca_mergefrag
  - 合并两个独立 .gbw 文件的 MO 系数
* - orca_pltvib
  - 生成用于振动动画的文件
* - orca_pnmr
  - 计算顺磁 NMR 屏蔽张量
* - orca_vib
  - 从已完成的频率运行计算振动频率
    （也用于同位素位移计算）
* - otool_gcp
  - 计算几何 Counterpoise 校正（GCP）
* - otool_xtb
  - 允许将来自 [Grimme 实验室](https://github.com/grimme-lab/xtb/releases/tag/v6.7.1) 的独立 xTB 代码与 ORCA 一起使用
:::

ORCA 的朋友们（Friends of ORCA）：

:::{tabularcolumns} \Y{0.20}\Y{0.80}
:::

:::{list-table}
* - gennbo
  - Weinhold 的 NBO 分析程序包。必须从威斯康星大学单独购买。
    互联网上免费提供的较旧版本也许也能工作。
* - Molekel
  - 分子可视化程序（见 {ref}`sec:utilities.plots.surface.molekel`）
* - gOpenMol
  - 分子可视化程序（见 {ref}`sec:utilities.plots.surface.gopenmol`）
* - Avogadro
  - 支持 ORCA 的分子构建与可视化程序
    （登录 [ORCA 论坛](https://orcaforum.kofo.mpg.de/) 然后导航到 Downloads。另见[原始仓库](http://avogadro.cc)）
* - Chemcraft
  - 支持 ORCA 的分子构建与可视化程序（见[下载页面](https://www.chemcraftprog.com/)）
* - SEQCROW
  - 支持 ORCA 的分子构建与可视化程序（见[仓库](https://github.com/QChASM/SEQCROW)）
:::

每个模块都能独立执行；不过，通常更方便的是通过主 ORCA 驱动程序执行所有操作，它会自动处理工作流。

ORCA 以一组预编译可执行文件的形式分发，因此不需要正式安装。
您只需将文件放在您选择的目录中。为确保各组件能够
正确交互，应将该目录添加到系统的 PATH 环境变量中。
或者，也可以在输入文件中手动指定各个组件的位置。

xtb 工具（推荐 6.7.1 或更高版本）必须从
[Grimme 实验室的仓库](https://github.com/grimme-lab/xtb/releases/tag/v6.7.1)单独下载。
下载后，xtb 可执行文件应放在与 ORCA 可执行文件相同的目录中。

我们大量使用 [Chemcraft](http://www.chemcraftprog.com) 进行可视化和分析。
虽然它是基于 Windows 的程序，但使用 Wine、虚拟机或远程桌面在 macOS 和 Linux 系统上运行良好。

另一个流行的可视化程序是
[ChimeraX](https://www.cgl.ucsf.edu/chimerax/) 连同
[SEQCROW 插件](https://github.com/QChASM/SEQCROW)。

[OpenBabel](http://openbabel.org/) 是用于在各种化学文件格式之间转换的
多功能且广泛使用的工具。

最后，[Avogadro](http://avogadro.cc) 是编辑分子几何结构的优秀工具。它还能生成 ORCA 输入文件。包含最新 ORCA 修改的 Avogadro 版本可在
[ORCA 下载](https://orcaforum.kofo.mpg.de/app.php/dlext/)站点获取。

最后，[Avogadro](http://avogadro.cc) 是编辑分子几何结构的优秀工具。它还可以直接生成 ORCA 输入文件。
包含最新 ORCA 特定修改的 Avogadro 版本可在 ORCA Downloads 页面获取，登录
[ORCA 论坛](https://orcaforum.kofo.mpg.de/)后即可访问。

更多信息和建议，请访问
[ORCA 论坛](https://orcaforum.kofo.mpg.de/index.php)。


```{index} orca_mapspc
```

(sec:utilities.mapspc)=
## orca_mapspc

实用程序 `orca_mapspc` 为标准图形软件准备输入文件，以绘制
计算得到的线光谱以及相应的卷积连续谱带形状。
关于使用 `orca_mapspc` 所提供文件生成的绘图光谱示例，
见下列章节：
{ref}`sec:spectroscopyproperties.tddft.semiemp`、
{ref}`sec:spectroscopyproperties.vib.ir`、
{ref}`sec:spectroscopyproperties.vib.raman` 和
{ref}`sec:spectroscopyproperties.rocis.rixs`）：

`orca_mapspc` 的符号命令结构如下：

```orca
orca_mapspc  Output-file Spectrum Options
```
其中
```orca
  Outfile-file    = name of an ORCA output file
                  name of an ORCA Hessian file (for IR and Raman)

  Spectrum        = abs    - Absorption spectra
                    cd     - CD spectra
                    ir     - IR spectra
                    raman  - Raman spectra

  Options         -x0value: Start of the x-axis for the plot
                  -x1value: End of the x-axis for the plot
                  -wvalue : Full-width at half-maximum height in
                            cm**-1 for each transition
                  -nvalue : Number of points to be used
```

有关支持的光谱类型和高级选项的完整列表，在终端中不带参数运行 `orca_mapspc`。

```orca
orca_mapspc
```

这将显示所有支持的光谱类型和选项：

```orca
------------------------------------------------------------------------------
usage: orca_mapspc Output-file {ABS, ABSV, ABSQ, ABSFFMIO, CD, IR, VCD, RAMAN,
                                NRVS, VDOS, MCD, CDV, CDFFMIO, SOCCD, SOCCDV,
				SOCCDFFMIO, SOCABS, SOCABSV, SOCABSQ, 
                                SOCABSFFMIO, XES, XESV, XESQ, XESFFMIO, XAS,
				XASV, XASQ, XASFFMIO, XESSOC, XESSOCV, XESSOCQ,
				XESSOCFFMIO, XASSOC, XASSOCV, XASSOCQ,
				XASSOCFFMIO, RIXS, RIXSSOC, TRANSABS, TRANSCD,
				TRANSSOCABS} -options
------------------------------------------------------------------------------
----General options ----
  -o  output file 
  -cm use cm**-1 (default) 
  -eV use eV (default cm**-1) 
  -g0  use Gaussian lineshape default 
  -l0  use Lorentz  lineshape (only for ABS, ABSV, ABSQ, ABSFFMIO, SOCABS,
                               SOCABSV, SOCABSQ, SOCABSFFMIO,  XES, XESV,
			       XESQ,XESFFMIO, XAS, XASV, XASQ, XASFFMIO,
			       XESSOC, XASSOC, RIXS, RIXSSOC
			       or Transient spectra)
  -v0  use Voigt lineshape (only for ABS, ABSV, ABSQ, ABSFFMIO, SOCABS,
                            SOCABSV, SOCABSQ, SOCABSFFMIO, XES, XESV, XESQ,
			    XESFFMIO, XAS, XASV, XASQ, XASFFMIO, XESSOC,
			    XASSOC, RIXS, RIXSSOC, or Transient spectra)
  -x0 initial point of spectrum 
  -x1 final   point of spectrum 
  -w  line width for Gaussian/Lorenzian linewidth 
  -q  line width for the Gaussian part of Voigt linewidth 
  -kw coeffitient for the line width calculated as kw*sqrt(energy) 
  -n  number of points 
----The following additional options are for IR/VCD/RAMAN spectra types----
  -fac   number for shifting the frequencies 
----The following additional options are for RIXS and RIXSSOC spectra types----
  -x2 initial point of the spectrum along y axis
  -x3 final   point of the spectrum along yaxis 
  -g1, -l1, -v1  line width for Gaussian/Lorenzian linewidth along y axis 
  -m  number of points for the emission spectrum 
  -eaxis plot option for the emission axis: (1) for Energy transfer
                                            (2) for emission spectrum 
  -uex  number of user defined cuts at constant Excitation Energy axis 
  -udw  number of user defined cuts at constant Emission/ Energy Transfer axis 
  -dx   number for shifting the spectra along the Excitation /Emission Energy axis 
  -kg coeffitient for the line width calculated as kg*sqrt(energy) 
  -umem control the memory demand 
----Using external files----
  paras.inp: a list of energy ranges with desired broadening parameters
             for x axis: E_start E_stop Width
             for y axis: 0 0 0 E_start E_stop Width
             for xy axis: E_start1 E_stop1 Width1 E_start2 E_stop2 Width2
  udex.inp: a list of energies for taking cuts at constant Excitation Energy axis
            (Only for RIXS/RIXSOC)
  udem.inp: a list of energies for taking cuts at constant Emission/ Energy
            Transfer axis (Only for RIXS/RIXSOC)
  gfsp.inp: a list of ground-final state pairs to generate individual state pair
            RIXS planes and respective analysis planes (Only for ROCIS RIXS/RIXSOC)
------------------------------------------------------------------------------------------------------------------------------------------------------------------
```
本文档对 ``orca_mapspc`` 支持的光谱关键词按类别分组进行详细说明。

### 光学/X 射线吸收光谱（Optical/X-ray Absorption Spectra）

这些关键词计算光学或 X 射线区域的吸收光谱，描述分子如何在特定能量处吸收光。

#### 偶极近似（Dipole Approximation）

偶极近似假设相互作用由电偶极项主导。

#### 偶极近似（Dipole Approximation）

偶极近似假设相互作用由电偶极项主导。

- **ABS**（偶极长度表示的光学/X 射线吸收光谱）

  - *说明*：使用长度表示的电偶极算符绘制吸收光谱（$\mu = -er$）。
  - *目的*：适用于偶极跃迁主导的 UV-Vis 或 X 射线吸收光谱（XAS）。
  - *用例*：常见于 UV-可见区的任何化学体系或 XAS。
  - *输出*：强度（振子强度，或 UV/Vis 光谱的吸光度 $\epsilon$）对能量（例如波长）
  - *注意*：对低能跃迁更准确；对高能 X 射线跃迁不太可靠。
  - *换算约定*：振子强度 $f_{osc}~= 4.31*10^{-9} * \epsilon$

- **ABSV**（偶极速度表示的光学吸收光谱）

  - *说明*：使用速度表示的偶极算符（$\mu \propto p$）。
  - *目的*：``ABS`` 的替代方案，用于数值稳定性或交叉验证。
  - *用例*：验证 ``ABS`` 结果。
  - *输出*：与 ``ABS`` 类似。
  - *注意*：对精确波函数与 ``ABS`` 等价，但对近似方法可能不同。

#### 超越偶极近似（Beyond Dipole Approximation）

这些方法包含更高阶相互作用（例如四极、磁偶极）以提高精度。

- **ABSFFMIO**（半经典完全物质相互作用算符的吸收光谱）

  - *说明*：基于包含超越偶极近似项的半经典完全物质相互作用算符绘制光谱。
  - *目的*：对具有显著四极或磁偶极贡献的体系准确。
  - *用例*：推荐用于常规 X 射线吸收光谱（例如 K 边 XAS...）或含有电偶极禁阻跃迁的光学光谱。
  - *输出*：含偶极及超越偶极贡献的常规光谱表。强度（振子强度，或 UV/Vis 光谱的吸光度 $\epsilon$）对能量（例如波长）
  - *注意*：对大多数应用推荐且稳健。

- **ABSQ**（含偶极、四极和磁偶极的吸收光谱）

  - *说明*：包含电偶极（长度）、电四极和磁偶极贡献的超越偶极多极公式。
  - *目的*：供专家用户使用的详细光谱，尤其是禁阻跃迁。
  - *用例*：需要做复杂/高级分析的 X 射线吸收（例如过渡金属 K 边）。
  - *输出*：处理所有可用表格，包括：
  1. **与原点相关的表格**
  2. **原点调整后的表格** {cite}`debeer2008tddft`。
  3. **与原点无关的表格**，使用多极展开二阶项的修正高阶矩 {cite}`jacob2012`。
  - *注意*：只要在输入运行中请求了 **DecomposeFosc**，就为高级/专家分析产生全面数据。

### 光学/X 射线圆偏振光谱（Optical/X-ray Circularly Polarized Spectra）

这些关键词处理圆偏振光的光谱，与圆二色（CD）和磁圆二色（(X)MCD）相关。

- **CD**（圆二色）

  - *说明*：绘制左旋和右旋圆偏振光的微分吸收。
  - *目的*：探测手性分子或不对称跃迁。
  - *用例*：对映异构体或手性配合物的 UV-Vis 光谱。
  - *输出*：$(\Delta\epsilon)$ 对能量（例如波长）
  - *注意*：需要手性体系。
  - *换算约定*：旋转强度：$R ~= 22.94 * \Delta\epsilon$

- **MCD**（磁圆二色）

  - *说明*：绘制磁场存在下左旋和右旋圆偏振光的计算微分。
  - *目的*：探测 MCD 过程中的自旋-轨道耦合或 Zeeman 效应
  - *用例*：过渡金属配合物或磁性材料的光学（MCD）或 X 射线光谱（XMCD）性质。
  - *输出*：左-右 (X)MCD 强度对能量（例如波长）以及左+右 ABS/XAS 强度对能量（例如波长）
  - *注意*：需要通过 DoMCD 关键词在有资格的模块（TD-DFT、CASSCF、MRCI、RASCI、ROCIS、LFT...）中进行磁场模拟运行

- **CDV**（速度表示的圆二色）

  - *说明*：速度表示的 ``CD``。
  - *目的*：数值稳定的替代公式。
  - *用例*：验证 ``CD`` 结果。
  - *输出*：与 ``CD`` 类似。

- **CDFFMIO**（完全物质相互作用算符的圆二色）

  - *说明*：绘制采用包含超越偶极近似项的半经典完全物质相互作用算符生成的 ``CD`` 光谱。
  - *目的*：超越偶极近似的更高精度，用于名义上偶极禁阻跃迁的 CD 光谱
  - *用例*：适用于由电偶极禁阻跃迁主导的 CD 光谱。
  - *输出*：超越偶极近似的 CD 光谱，$(\Delta\epsilon)$ 对能量（例如波长）

### 自旋-轨道耦合（SOC）变体（Spin-Orbit Coupling Variants）

这些关键词包含自旋-轨道耦合
1. 用于具有显著多重态结构的化学体系（L 边 XAS）
2. 用于含重元素（镧系、锕系）的化学体系
3. 用于探测自旋禁阻跃迁。

- **SOCABS**（SOC 吸收光谱）

  - *说明*：偶极长度表示下含 SOC 的吸收光谱。
  - *目的*：考虑光学/X 射线吸收中的 SOC 效应。
  - *用例*：SOC 效应主导的 ABS/XAS 光谱。
  - *输出*：含 SOC 效应的吸收光谱。强度（振子强度，或 UV/Vis 光谱的吸光度 $\epsilon$）对能量（例如波长）

- **SOCABSV**（速度表示的 SOC 吸收光谱）

  - *说明*：速度表示的 ``SOCABS``。
  - *目的*：``SOCABS`` 的替代公式，用于数值稳定性或交叉验证
  - *用例*：验证 ``SOCABS`` 结果。
  - *输出*：与 ``SOCABS`` 类似。

- **SOCABSFFMIO**（完全物质相互作用算符的 SOC 吸收光谱）

  - *说明*：``SOCABS`` 采用超越偶极近似的强度贡献。
  - *目的*：推荐用于超越偶极近似的常规 SOC-ABS/XAS。
  - *用例*：例如高对称性过渡金属或重元素化学体系的 XAS
  - *输出*：FFMIO 算符超越偶极近似、含 SOC 校正的常规 ABS 光谱。强度（振子强度，或 UV/Vis 光谱的吸光度 $\epsilon$）对能量（例如波长）

- **SOCABSQ**（含偶极、四极和磁偶极贡献的 SOC 吸收光谱）

  - *说明*：``SOCABS`` 超越偶极近似的强度贡献。
  - *目的*：多极公式下 SOC 吸收光谱的详细表格。
  - *用例*：需要做复杂/高级分析的含 SOC 的 X 射线吸收（例如 L 边）。
  - *输出*：处理所有可用表格，包括：
  1. **与原点相关的表格**
  2. **原点调整后的表格** {cite}`debeer2008tddft`。
  3. **与原点无关的表格**，使用多极展开二阶项的修正高阶矩 {cite}`jacob2012`。
  - *注意*：只要在输入运行中请求了 **DecomposeFosc**，就为高级/专家分析产生全面数据。


- **SOCCD**（SOC 圆二色）

  - *说明*：含自旋-轨道耦合的 ``CD``。
  - *目的*：捕捉手性体系中的 SOC。
  - *用例*：具有复杂多重态结构（例如含镧系、锕系金属中心）的化学体系的光学 CD。
  - *输出*：含 SOC 效应的 CD 光谱。$(\Delta\epsilon)$ 对能量（例如波长）

- **SOCCDV**（速度表示的 SOC 圆二色）

  - *说明*：速度表示的 ``SOCCD``。
  - *目的*：``SOCCD`` 的替代公式。
  - *用例*：验证或数值稳定性。
  - *输出*：与 ``SOCCD`` 类似。

- **SOCCDFFMIO**（完全物质相互作用算符的 SOC 圆二色）

  - *说明*：``SOCCD`` 采用超越偶极近似的强度贡献。
  - *目的*：推荐用于处理超越偶极近似的常规 SOC-CD 光谱。
  - *用例*：高对称性过渡金属或重元素化学体系（含复杂多重态结构）的 CD 研究
  - *输出*：FFMIO 算符超越偶极近似、含 SOC 校正的 CD 光谱。$(\Delta\epsilon)$ 对能量（例如波长）

### X 射线发射光谱（X-ray Emission Spectroscopy, XES）

这些关键词绘制 X 射线发射光谱，由 %xes 模块
或可在 OPE 框架内生成 XES 光谱的相关方法产生。

- **XES**（X 射线发射光谱）

  - *说明*：处理偶极长度表示的 XES。
  - *目的*：处理基于芯电子电离后 X 射线电子衰变产生的光谱。
  - *用例*：材料的 X 射线光谱。
  - *输出*：发射光谱，强度（振子强度）对能量（例如电子伏特）

- **XESV**（速度表示的 X 射线发射光谱）

  - *说明*：速度表示的 ``XES``。
  - *目的*：``XES`` 的替代公式。
  - *输出*：与 ``XES`` 类似。

- **XESFFMIO**（完全物质相互作用算符的 X 射线发射光谱）

  - *说明*：``XES`` 采用超越偶极近似的强度贡献。
  - *目的*：推荐用于处理超越偶极近似的常规 XES 光谱。
  - *输出*：FFMIO 算符超越偶极近似的 XES 光谱。强度（振子强度）对能量（例如电子伏特）

- **XESQ**（含偶极、四极和磁偶极的 X 射线发射光谱）

  - *说明*：``XES`` 包含电偶极（长度）、电四极和磁偶极贡献的超越偶极多极公式。
  - *目的*：供专家用户使用的详细 XES 光谱，用于需要做复杂/高级分析的场合。
  - *输出*：与 ``ABSQ`` 相同，处理所有可用表格，包括：
  1. **与原点相关的表格**
  2. **原点调整后的表格** {cite}`debeer2008tddft`。
  3. **与原点无关的表格**，使用多极展开二阶项的修正高阶矩 {cite}`jacob2012`。
  - *注意*：只要在输入运行中请求了 **DecomposeFosc**，就为高级/专家分析产生全面数据。

- **XESSOC**（SOC X 射线发射光谱）

  - *说明*：含自旋-轨道耦合的 ``XES``。
  - *目的*：处理基于含 SOC 效应的芯电子电离后 X 射线电子衰变产生的光谱。
  - *用例*：推荐用于处理常规 SOC-XES 光谱。
  - *输出*：含 SOC 效应的发射光谱。强度（振子强度）对能量（例如电子伏特）

- **XESSOCV**（速度表示的 SOC X 射线发射光谱）

  - *说明*：速度表示的 ``XESSOC``。
  - *目的*：``XESSOC`` 的替代公式。
  - *输出*：与 ``XESSOC`` 类似。

- **XESSOCFFMIO**（完全物质相互作用算符的 SOC X 射线发射光谱）

  - *说明*：``XESSOC`` 采用超越偶极近似的强度贡献。
  - *目的*：推荐用于处理超越偶极近似的常规 SOC-XES。
  - *输出*：FFMIO 算符超越偶极近似、含 SOC 校正的 X 射线发射光谱，以强度（振子强度）对能量（例如电子伏特）绘制

- **XESSOCQ**（含偶极、四极和磁偶极的 SOC X 射线发射光谱）

  - *说明*：含非偶极贡献的 ``XESSOC``。
  - *目的*：需要做复杂/高级分析的详细 SOC-XES 光谱。
  - *输出*：与 ``SOCABSQ`` 相同，处理所有可用表格，包括：
  1. **与原点相关的表格**
  2. **原点调整后的表格** {cite}`debeer2008tddft`。
  3. **与原点无关的表格**，使用多极展开二阶项的修正高阶矩 {cite}`jacob2012`。
  - *注意*：只要在输入运行中请求了 **DecomposeFosc**，就为高级/专家分析产生全面数据。

### X 射线吸收光谱（X-ray Absorption Spectroscopy, XAS）

这些关键词绘制 X 射线吸收光谱，由 %xes 模块产生。

- **XAS**（X 射线吸收光谱）

  - *说明*：绘制偶极长度表示的 XAS。
  - *目的*：处理探测芯电子激发（例如 K 边）的光谱。
  - *用例*：单电子 DFT X 射线吸收光谱。
  - *输出*：X 射线能量的吸收光谱。（强度（振子强度）对能量（例如电子伏特））

- **XASV**（速度表示的 X 射线吸收光谱）

  - *说明*：速度表示的 ``XAS``。
  - *目的*：``XAS`` 的替代公式。
  - *输出*：与 ``XAS`` 类似。


- **XASFFMIO**（完全物质相互作用算符的 X 射线吸收光谱）

  - *说明*：``XAS`` 采用超越偶极近似的强度贡献。
  - *目的*：推荐用于处理超越偶极近似的常规 XAS 光谱。
  - *输出*：FFMIO 算符超越偶极近似的 XAS 光谱（强度（振子强度）对能量（例如电子伏特））。

- **XASQ**（含偶极、四极和磁偶极的 X 射线吸收光谱）
  - *说明*：``XASS`` 包含电偶极（长度）、电四极和磁偶极贡献的超越偶极多极公式。
  - *目的*：供专家用户使用的详细 XAS 光谱，用于需要做复杂/高级分析的场合。
  - *输出*：与 ``ABSQ`` 相同，处理所有可用表格，包括：
  1. **与原点相关的表格**
  2. **原点调整后的表格** {cite}`debeer2008tddft`。
  3. **与原点无关的表格**，使用多极展开二阶项的修正高阶矩 {cite}`jacob2012`。
  - *注意*：只要在输入运行中请求了 **DecomposeFosc**，就为高级/专家分析产生全面数据。

- **XASSOC**（SOC X 射线吸收光谱）

  - *说明*：含自旋-轨道耦合的 ``XAS``。
  - *目的*：处理基于含 SOC 效应的芯电子电离后 X 射线吸收产生的光谱。
  - *用例*：推荐用于处理常规 SOC-XAS 光谱。
  - *输出*：含 SOC 效应的吸收光谱（强度（振子强度）对能量（例如电子伏特））

- **XASSOCV**（速度表示的 SOC X 射线吸收光谱）

  - *说明*：速度表示的 ``XASSOC``。
  - *目的*：``XASSOC`` 的替代公式。
  - *输出*：与 ``XASSOC`` 类似。

- **XASSOCFFMIO**（完全物质相互作用算符的 SOC X 射线吸收光谱）

  - *说明*：``XASSOC`` 采用超越偶极近似的强度贡献。
  - *目的*：推荐用于处理超越偶极近似的常规 SOC-XAS 光谱。
  - *输出*：FFMIO 算符超越偶极近似、含 SOC 校正的 X 射线吸收（强度（振子强度）对能量（例如电子伏特））

- **XASSOCQ**（含偶极、四极和磁偶极的 SOC X 射线吸收光谱）

  - *说明*：``XASSOC`` 包含电偶极（长度）、电四极和磁偶极贡献的超越偶极多极公式。
  - *目的*：供专家用户使用的详细 XASSOC 光谱，用于需要做复杂/高级分析的场合。
  - *输出*：与 ``SOCABSQ`` 相同，处理所有可用表格，包括：
  1. **与原点相关的表格**
  2. **原点调整后的表格** {cite}`debeer2008tddft`。
  3. **与原点无关的表格**，使用多极展开二阶项的修正高阶矩 {cite}`jacob2012`。
  - *注意*：只要在输入运行中请求了 **DecomposeFosc**，就为高级/专家分析产生全面数据。

### 共振非弹性 X 射线散射（Resonant Inelastic X-ray Scattering, RIXS）

这些关键词处理由多种方法生成的 RIXS 光谱

- **RIXS**（共振非弹性 X 射线散射）

  - *说明*：处理 RIXS 光谱（散射 X 射线的能量损失，沿入射和发射/能量损失轴）。
  - *目的*：探测电子和振动结构。
  - *用例*：过渡金属、催化剂。
  - *输出*：二维光谱以及沿恒定发射/入射轴的一维剖面光谱。
  - *注意*：见章节 {ref}`sec:spectroscopyproperties.rocis.rixs`

- **RIXSSOC**（SOC 共振非弹性 X 射线散射）

  - *说明*：含自旋-轨道耦合的 ``RIXS``。
  - *目的*：考虑 RIXS 光谱中的 SOC。
  - *用例*：具有显著多重态结构（2p3d RIXS）的化学体系的 RIXS。
  - *输出*：含 SOC 效应的二维光谱以及沿恒定发射/入射轴的一维剖面光谱。
  - *注意*：见章节 {ref}`sec:spectroscopyproperties.rocis.rixs`

### 瞬态光谱（Transient Spectroscopy）

这些关键词计算泵浦-探测实验的时间分辨光谱。

- **TRANSABS**（瞬态吸收光谱）

  - *说明*：处理瞬态吸收光谱。
  - *目的*：建模随时间变化的吸收变化。
  - *用例*：光化学或时间分辨或泵浦-探测 UV 吸收研究。
  - *输出*：瞬态吸收光谱，（强度对能量）。

- **TRANSCD**（瞬态圆二色）

  - *说明*：处理瞬态 CD 光谱。
  - *目的*：建模随时间变化的 CD 变化。
  - *用例*：手性体系中时间分辨或泵浦-探测 CD 光谱。
  - *输出*：$(\Delta\epsilon)$ 对能量。

- **TRANSSOCABS**（SOC 瞬态吸收光谱）

  - *说明*：含自旋-轨道耦合的 ``TRANSABS``。
  - *目的*：考虑瞬态吸收中的 SOC。
  - *用例*：具有复杂多重态结构的化学体系的时间分辨或泵浦-探测 ABS/XAS/XUV
  - *输出*：含 SOC 的瞬态吸收光谱（强度对能量）

### 振动光谱（Vibrational Spectroscopy）

这些关键词计算与振动跃迁相关的光谱。

- **IR**（红外光谱）

  - *说明*：处理红外吸收光谱。
  - *目的*：建模振动跃迁。
  - *用例*：分子振动分析/结构分析。
  - *输出*：强度对波数。

- **VCD**（振动圆二色）

  - *说明*：处理振动 CD 光谱。
  - *目的*：探测手性振动跃迁。
  - *用例*：手性分子（例如生物分子）。
  - *输出*：$(\Delta\epsilon)$ 对波数。

- **RAMAN**（拉曼光谱）

  - *说明*：处理拉曼散射光谱。
  - *目的*：通过拉曼散射建模振动跃迁。
  - *用例*：分子振动分析/结构分析。
  - *输出*：强度对波数。

- **NRVS**（核共振振动光谱）

  - *说明*：处理核共振振动光谱。
  - *目的*：探测与核跃迁耦合的振动模式（例如 Fe-57）。
  - *用例*：在生物无机化学分析中有用。
  - *输出*：强度对能量。

- **VDOS**（振动态密度）

  - *说明*：处理振动态密度。
  - *目的*：提供振动模式的分布。
  - *用例*：在固体或大体系分析中有用。
  - *输出*：密度对能量。

### 一般说明（General Notes）

- *偶极对速度*：长度（``ABS``）和速度（``ABSV``）表示对精确波函数等价，但在近似计算中可能不同。
- *超越偶极*：``FFMIO`` 和 ``Q`` 关键词包含四极和磁偶极项，对 X 射线光谱至关重要。
- *自旋-轨道耦合*：``SOC`` 关键词对重元素或自旋禁阻跃迁必不可少。
- *专家对常规*：``Q`` 变体产生供专家使用的详细输出；``FFMIO`` 变体应用于常规分析。
- *ORCA 要求*：某些关键词需要特定设置（例如 ``SOC`` 需要相对论方法，瞬态吸收方法需请求 ``DOTRANS true/all``）。

### 用法示例（Example Usage）

注意：

-   `orca_mapspc` 程序的输入可以是标准 ORCA 输出文件
	或用于 IR 和 Raman 等振动光谱的 .hess 文件。

-   除非另有说明，线型假定为 Gaussian。
    

-   `orca_mapspc` 程序生成两个输出文件：

    -   `Input-file.spc.dat`（spc $=$ abs、cd、ir 或 raman）：该文件
        包含绘制连续谱带形状光谱所需的数据。

    -   `Input-file.spc.stk`：该文件包含各个
        跃迁（波数和强度），用于绘制线光谱。

-   对于吸收光谱，.dat 文件包含五列：
	波数（单位为厘米的倒数）、总强度、入射光电场矢量沿
	-x、y- 和 z-轴的偏振分量。
	偏振分量对解释偏振单晶光谱特别有用。

-   当 ORCA 输出文件中存在多个同类光谱时，
	`orca_mapspc` 将自动处理所有这些光谱数据集。例如，
	如果 ORCA 输出同时包含 CASSCF 和 NEVPT2 激发，将处理
	两种方法对应的光谱数据。为说明这一点，假设
	CASSCF 和 NEVPT2 吸收数据同时存在于名为
	My-NEVPT2.out 的 ORCA 输出文件中。让我们将该文件传给 `orca_mapspc`：
	
```orca
orca_mapspc My-NEVPT2.out SOCABS -x07000 -x18000 -eV -n10000 -w2.0 -l
```

`orca_mapspc` 将打印出：

```orca
Mode is SOCABS
Entering SOC-ABS reading
Using eV units
Using Lorentzian shape
Multiple SOCABS (2) spectra detected ...
----------------------------------
Plotting SOCABS Spectrum 0
----------------------------------
Cannot read the paras.inp file ... 
taking the line width parameter from the command line 
Number of peaks            ...   4455
Start energy [eV]          ...  7000.00
Stop energy [eV]           ...  8000.00
Peak FWHM [eV]             ...     2.00
Number of points           ...   10000
----------------------------------
Plotting SOCABS Spectrum 1
----------------------------------
Cannot read the paras.inp file ... 
taking the line width parameter from the command line 
Number of peaks            ...   4455
Start energy [eV]          ...  7000.00
Stop energy [eV]           ...  8000.00
Peak FWHM [eV]             ...     2.00
Number of points           ...   10000
```

最后，它将为 CASSCF 和 NEVPT2 标志生成数据文件：

```orca
CASSCF:
       My-NEVPT2.out.0.socabs.dat
       My-NEVPT2.out.0.socabs.stk
NEVPT2:
       My-NEVPT2.out.1.socabs.dat
       My-NEVPT2.out.1.socabs.stk
```

My-NEVPT2.out 文件中其他可用的光谱数据（例如 CD 光谱）
也可以用同样的方式处理。

(sec:utilities.chelpg)=
## orca_chelpg

`orca_chelpg` 程序按照 Breneman 和 Wiberg{cite}`breneman1990` 的方法计算 CHELPG 原子电荷。原子电荷通过拟合以再现分子周围规则网格上的静电势（ESP），同时将所有原子电荷之和约束为分子的总电荷。有关默认值的更多信息见 {ref}`sec:spectroscopyproperties.pop.chelpg`。

要从终端运行该程序，只需提供一个参数：gbw 文件名：

```orca
orca_chelpg  MyJob.gbw
```

作为可选参数，可以通过文件名提供总溶质密度矩阵。

(sec:utilities.pltvib)=
## orca_pltvib

`orca_pltvib` 程序与 gOpenMol（或 xmol）配合使用，在频率计算后生成振动模式的动画或图形。其用法很简单，在章节
{ref}`sec:spectroscopyproperties.vib.animation` 中描述，同时附有在 gOpenMol 中生成这些图形的简要指南。

该程序为每个振动模式生成 20 个动画帧。第一帧和最后一帧对应于 TS，中间帧按
$sin(2\pi frame/20-1) * displacement$ 计算。
这产生以平衡几何结构为中心的平滑振荡图样。

(sec:utilities.vib)=
## orca_vib

`orca_vib` 是一个用于执行振动分析的小型"独立"程序。
它让用户可以控制原子质量等参数，这些参数影响
预测的振动频率，但与电子结构计算本身无关。

该程序以 "`.hess`" 文件作为输入，生成的输出
本质上与标准 ORCA 频率计算产生的输出等价。关键优势是 `.hess` 文件是用户可编辑的
纯文本文件，允许手动修改，例如用于同位素位移
预测或自定义质量调整。

`orca_vib` 的用法连同示例在章节
{ref}`sec:spectroscopyproperties.vib.isotopeshifts` 中提供。通过将屏幕
输出通过管道传给文本文件，可以进一步用 `orca_mapspc` 处理振动数据，
从修改后的 Hessian 生成用于绘制 IR、Raman 或 NRVS 光谱的数据文件。

(sec:utilities.loc)=
## orca_loc

定域化是量子化学中广泛使用的技术。通过定义不同的
泛函，发展了各种定域化方法。其中最广泛使用的是 Foster–Boys（FB）和 Pipek–Mezey（PM）方法。在 ORCA 中，六种定域化方法可用：
Pipek-Mezey 方法（PM）、
Foster-Boys 方法（FB）、
基于内禀原子轨道（IAO）的 PM 方法、
基于 IAO 的 FB 方法、
价层虚轨道的 PM 定域化（PMVVO），
以及定域化内禀价层虚轨道（LIVVO）。

FB 定域化有三种可用算法：常规算法（`FB`）、
更快的替代方案 `NEWBOYS`（推荐用于大体系中虚 MO 的定域化），
以及增广 Hessian FB（`AHFB`）算法，适合获得紧密收敛的
轨道（例如用于具有适当容差的局域相关方法）。

`AHFB` 算法系统地收敛到局部极小点，而不是
其他类型的驻点，它分三个阶段进行：
(i) 获得一组初始的 `NEWBOYS` 定域轨道。
(ii) 接着进行增广 Hessian 极大化（有理函数优化），
使用直接或 Davidson 对角化，取决于轨道数目，
以使其对小体系和大体系都高效。
(iii) 如果优化失败但增广 Hessian 具有正确的本征值结构，
则触发 Newton-Raphson 极大化。

`AHFB` 中唯一可由用户调整的参数是容差 Tol。当本征值结构正确且轨道梯度的最大元素
$4 \left<i|\mathbf{r}|j\right> \left(  \left<j|\mathbf{r}|j\right> - \left<i|\mathbf{r}|i\right> \right)$
低于 Tol 时发出收敛信号。这与其他定域化方法不同，后者使用两次连续迭代之间
定域化泛函变化量的总和作为收敛判据。

由 Gerald Knizia {cite}`knizia2013` 开发的内禀原子轨道和内禀键轨道（`IAOIBO`）定域化方法按如下步骤进行：
(i) 将占据 MO 投影到最小基组上得到 IAO。
在 ORCA 中，IAO 默认从原子的收敛 SCF MO 生成，
而不是像原始方法那样使用 MINI 或 STO-3G 基组。
不过，ORCA 默认计算的 IAO 电荷与原始 IAO 电荷非常相似。
默认行为可以用 `IAOBasis` 关键词更改。
(ii) 使用 PM 泛函将这些 IAO 定域化为 IBO。
(iii) 将 IBO 反变换回其原始基组。

注意：在 IAOIBO 定域化之前打印正则 MO 的 IAO 部分电荷。
请务必包含所有占据 MO，因为缺少任何一个都会使 IAO 电荷失去意义。

ORCA 中该方法的改进版本用 FB 替代 PM 作为定域化泛函，
得到 IAOBOYS 方法。对大体系，IAOBOYS 在计算上比标准 FB 方法更高效。
不过，值得注意的是基于 IAO 的定域化目前仅适用于占据 MO。

价层虚轨道（VVO）可以按照参考文献
{cite}`Derricotte2017LIVVO` 中描述的方法定域化。该方法可简述如下：通过 IAO 与虚 MO 之间重叠的奇异值分解获得 VVO。
IAO 数目与占据 MO 数目之差即为 VVO 数目。不过，完整的虚轨道窗口
必须作为输入提供给 `orca_loc`！最终的 VVO 窗口打印在输出中。其余
虚 MO 不被修改，因此与 VVO 不正交。然后可以分别使用 `PMVVO` 和 `LIVVO` 关键词
按 PM 或 IBO 判据定域化 VVO。
后一选项对应于参考文献 {cite}`Derricotte2017LIVVO` 中的定域化内禀 VVO。

在 ORCA 中请求 MO 定域化有两种方式：(i) 在输入文件中使用 `%loc` 块内联请求，
(ii) 对预计算的 MO 使用 `orca_loc` 实用程序。

在输入文件的 `%loc` 块中请求时，可以设置下列选项：

```orca
%loc   
LocMet      PM            # Localization method e.g. PIPEK-MEZEY 
            FB            # FOSTER-BOYS
            IAOIBO        # IAOIBO 
            IAOBOYS       # IAOBOYS
            NEWBOYS       # FOSTER-BOYS
            AHFB          # Augmented Hessian Foster-Boys
            PMVVO         # PM-localized valence virtual orbitals
            LIVVO         # localized intrinsic valence virtual orbitals
LocMetVirt  0             # If given, used for the virtual space instead of LocMet;
                          # the same options are available
Tol         1e-6          # absolute convergence tolerance for the localization sum
                          # default value is 1e-6
                          # In the case of AHFB, however, this is the gradient
			  # threshold !
Random      0             # Always take the same seed for start for localization
                          # (For testing/debug purpose,optional)
            1             # Take a random seed for start of localization (default)
PopMethod   MULLIKEN      # Population method for the final analysis
            LOEWDIN       # of the localized orbitals (default: Mulliken) 
PrintLevel  2             # Amount of printing 
OrbSpread   false         # Whether to compute and print the localized orbital
                          # spread: sqrt(<i|(r-<i|r|i>)^2|i>)
MaxIter     64            # Max number of iterations 
T_Bond      0.85          # Thresh that classifies orbitals in bond-like at
                          # the printing 
T_Strong    0.95          # Thresh that classifies orbitals into strongly-localized
                          # at the printing 
OCC         true          # Localize the occupied space 
T_CORE      -99.9         # The Energy window for the first OCC MO to be localized
                          # (in a.u.)
                          # Here, we localize all occupied MOs including
			  # core orbitals.
VIRT        true          # Localize the virtual space 
IAOBasis    SCF_SV        # (default) Basis of MOs obtained from HF/SV calculations 
            STO_3G        # STO-3G
            MINI          # MINI
            ANO_SZ        # ANO-SZ
            ANO_RCC_MB    # ANO-RCC-MB
            MINAO_AUTO_PP # MINAO-AUTO-PP basis (presumes ECPs beyond Kr)
end
```

MO 在 ORCA 中迭代定域化。当定域化泛函值变得自洽时达到收敛，
由 Tol 参数控制。如果 %loc 块中的 `OCC` 或 `VIRT` 标志设为
true，则对相应的占据或虚轨道子空间执行定域化。如果 `OCC` 和 `VIRT` 标志都设为 true，
则执行两次连续的定域化——每个子空间一次。用于虚轨道的定域化方法通过
`LocMetVirt` 关键词指定（若提供）；否则默认为 `LocMet`。定域化轨道
存储在标准 `.gbw` 文件格式中，但扩展名为 `.loc.gbw`。

注意：使用定域化占据轨道可能会改变总能量。对 RHF 和 UHF，这通常
不会造成问题。但对 CASSCF，仅 OCC 标志是不够的，因为 CASSCF 在
所有占据轨道的旋转下不是不变的。

当从命令行调用 `orca_loc` 程序时，它需要一个单独的基于文本的输入文件，
包含所有必要参数。如果未指定输入，`orca_loc` 返回列出
所有可用选项的帮助消息。通常需要在 `orca_loc` 输入中指定输入和输出 gbw
文件，以及轨道范围和所用的定域化方法。容易混淆的是算符
行 op（alpha $=$ 0 或 beta $=$ 1）。对 RHF(ROHF) 和 CASSCF，应设为零。
`orca_loc` 的输入文件如下所示：

```orca
Myjob.gbw     # input orbitals 
Myjob.loc.gbw # output orbitals 
10            # orbital window: first orbital to be localized e.g. first active 
15            # orbital window: last orbital to be localized e.g. last active 
0             # localization method:
              # 1=PIPEK-MEZEY,2=FOSTER-BOYS,3=IAO-IBO,4=IAO-BOYS,5=NEW-BOYS,
	      # 6=AHFB,7=PMVVO,8=LIVVO
# The following parameters are optional
# However, if you want to change one of them, all preceding ones have to be
# set, too.
0             # operator: 0 for alpha, 1 for beta
128           # maximum number of iterations 
1e-6          # convergence tolerance of the localization functional value 
0.0           # relative convergence tolerance of the localization functional value              
0.95          # printing thresh to call an orbital strongly localized 
0.85          # printing thresh to call an orbital bond-like
2             # printlevel
1             # use Cholesky Decomposition (0=false, 1=true)
1             # randomize seed for localization (0=false, 1=true)
0             # IAO basis (0-5 in the order given above)
0             # Population analysis method (0=Mulliken, 1=Lowedin)
0             # Print orbital spread (0=false, 1=true)
```

如果该输入文件命名为 myloc.inp，运行 \"orca_loc myloc.inp\"
将产生包含定域化轨道的 Myjob.loc.gbw 文件。
请确保 Myjob.gbw 与 myloc.inp 在同一目录中。

(sec:utilities.blockf)=
## orca_blockf

`orca_blockf` 实用程序对 `.gbw` 文件中任意子空间内的轨道进行正则化。
在这里，正则化指的是 Fock 矩阵在指定轨道子空间内的
块对角化。

在命令行运行 `orca_blockf`：

```orca
orca_blockf Fock.gbw Orbitals.gbw Output.gbw firstOrb lastOrb 
```

使用需要两个 `.gbw` 文件。一个用于重建 Fock 矩阵（上述的 Fock.gbw），
另一个包含待重新正则化的轨道（上述的 Orbitals.gbw）。如果用户不提供
输出 `gbw` 名称，程序将覆盖第二个参数 `gbw` 文件。

该程序在章节 {ref}`sec:modelchemistries.mrci.soc.lzfs` 中有进一步描述。

(sec:utilities.plot)=
## orca_plot

`orca_plot` 为用 ORCA 计算的各种轨道和密度类型生成可直接绘图的文件（如 `.plt` 和 `.cube`），
以便用外部 2D 和 3D 图形软件进行可视化。
它可以用两种方式调用：

1) 在 ORCA 输入文件中通过 `%plots` 块。这种方式允许您在运行过程中自动生成图形数据
（例如 .plt 或 .cube 文件）。细节见章节 {ref}`sec:utilities.plots`。

2) 计算后交互式地，使用已生成的 `.gbw` 文件，有下列可用参数：

```orca
gbwfile     # name of gbw-file
-i          # interactive use of orca_plot
-m 256      # max. memory in MB (if needed)
```

如有需要，-m 选项可用于控制绘图作业的内存使用。
`orca_plot` 可以在终端中调用，例如对名为 my.gbw 的 gbw 文件，调用方式为：

```orca
orca_plot my.gbw -i
```

这将列出可用选项：

```orca
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

```

下面，让我们用上述选项列表演示 `orca_plot` 对不同绘图类型的用法。

(sec:utilities.plot.orbital_plots)=
### 执行轨道绘图（Perform Orbital Plots）

让我们考虑一个对吡啶分子进行单点能计算的 ORCA 输入文件：

(sec:utilities.plot.inpscfplot)=
```orca
! RHF def2-SVP 

*xyz 0 1
C        0.690940233      0.417992301     -1.170801378
C        0.690940233      1.616339301     -0.458357378
C        0.690940233      1.560238301      0.936438622
N        0.690940233      0.417992301      1.635468622
C        0.690940233     -0.724253699      0.936438622
C        0.690940233     -0.780354699     -0.458357378
H        0.690940233      0.417992301     -2.257043378
H        0.690940233      2.574997301     -0.967574378
H        0.690940233      2.478336301      1.521602622
H        0.690940233     -1.642351699      1.521602622
H        0.690940233     -1.739012699     -0.967574378
*       

```

我们想绘制 HOMO 轨道。首先，需要从 ORCA 输出文件的 `ORBITAL ENERGIES` 部分确定其轨道编号（20）：

 ```orca
----------------
ORBITAL ENERGIES
----------------

  NO   OCC          E(Eh)            E(eV) 
   0   2.0000     -15.563726      -423.5105 
 ...
 Occupied Orbitals Manifold
 ...
  20   2.0000      -0.349834        -9.5195 
 ...
 Unoccupied Orbitals Manifold
 ...
  21   0.0000       0.111722         3.0401 
 ...

```

然后让我们为选项 `2`、`3`、`4`、`5` 和 `8` 指定合适的选择：

```orca

Enter a number: 2       
Enter MO: 20

Enter a number: 3
Enter OP: 0

Enter a number: 4
Enter NGRID: 80

Enter a number: 5
File-Format is presently: 7 
(7 -  3D   Gaussian cube)

Enter a number: 8
Enter 0(MO) or 1(AO): 0

```

要生成图形，选择 `11`。然后，如果不需要额外图形，选择 `12` 退出 `orca_plot`。
否则，可以在一次运行中顺序请求多个图形。

```orca
11 - Generate the plot
Enter a number: 11 =>

PlotType       ... MO-PLOT
MO/Operator    ... 20 0
Output file    ... pyridine_scf.mo20a.cube
Format         ... Grid3d/Cube
Resolution     ... 80 80 80

Calling PlotGrid3d with ATOM-A,B=0,0
Entering PlotGrid3d with Plottype =1
                 *** PLOTTING FINISHED ***
Output file: pyridine_scf.mo20a.cube

```

这生成一个 `.cube` 文件，可用于可视化程序中可视化 HOMO 轨道。
在 `Chimera` 中以该 cube 文件为输入获得的 HOMO 轨道图像
如 {numref}`fig:Pyridine_HOMO` 所示。

(fig:Pyridine_HOMO)=
```{figure} ../../images/orca_plot_pyridine_HOMO.*

吡啶 HOMO
```

(sec:utilities.plot.list_densities)=
### 密度图列表（List of Density Plots）
如果需要密度图而非轨道图，可以使用选项 `1` 和 `9` 列出可用密度。

例如选项 `1` 将为上述吡啶示例提供下列计算得到的可用密度。
                
    
```orca
Enter a number: 1
-----------------------------------------------------------------------
Reading Over   2 Saved Densities                                    ...
-----------------------------------------------------------------------
-----------------------------------------------------------------------
Plot-Type is presently: 1
-----------------------------------------------------------------------
Searching for Ground State Electron or Spin Densities:              ...
-----------------------------------------------------------------------
     1 -   molecular orbitals                  
     2 -   (scf) electron density               ......  (scfp    )  => AVAILABLE
     3 -   (scf) spin density                   ......  (scfr    )  - NOT AVAILABLE
     4 -   natural orbitals                    
     5 -   corresponding orbitals              
     6 -   atomic orbitals                     
     7 -   mdci electron density                ......  (mdcip   )  - NOT AVAILABLE
     8 -   mdci spin density                    ......  (mdcir   )  - NOT AVAILABLE
     9 -   OO-RI-MP2 density                    ......  (pmp2re  )  - NOT AVAILABLE
    10 -   OO-RI-MP2 spin density               ......  (pmp2ur  )  - NOT AVAILABLE
    11 -   MP2 relaxed density                  ......  (pmp2re  )  - NOT AVAILABLE
    12 -   MP2 unrelaxed density                ......  (pmp2ur  )  - NOT AVAILABLE
    13 -   MP2 relaxed spin density             ......  (rmp2re  )  - NOT AVAILABLE
    14 -   MP2 unrelaxed spin density           ......  (rmp2ur  )  - NOT AVAILABLE
    15 -   LED dispersion interaction density   ......  (ded21   )  - NOT AVAILABLE
    16 -   Atom pair density                   
    17 -   Shielding Tensors                   
    18 -   Polarisability Tensor               
    19 -   AutoCI relaxed density               ......  (autocipr)  - NOT AVAILABLE
    20 -   AutoCI unrelaxed density             ......  (autocipu)  - NOT AVAILABLE
    21 -   AutoCI relaxed spin density          ......  (autocirr)  - NOT AVAILABLE
    22 -   AutoCI unrelaxed spin density        ......  (autociru)  - NOT AVAILABLE

```

这种情况下，只有 SCF 电子密度（选项 `2`）可用，因而可以用 `orca_plot` 处理以准备可视化软件的输入
文件。选择该选项生成必要的 `scfp` 文件：

```orca
Enter Type: 2
The default name of the density would be: pyridine_scf.scfp
Is this the one you want (y/n)?
```

生成的文件随后将出现在选项 `9` 的可用密度文件列表中。

```orca
---------------------
List of density names
---------------------

Index:                                                   Name of Density
------------------------------------------------------------------------
    0:                                                 pyridine_scf.scfp
```

按照生成 HOMO 轨道 cube 文件所述的步骤，也可以生成可视化吡啶 SCF 电子密度所必需的文件（cube、plt 等）。选择选项 `11` 时，终端中将打印出如下内容。

```orca
PlotType       ... DENSITY-PLOT
ElDens File    ... pyridine_scf.scfp
Output file    ... MyElDens
Format         ... Grid3d/Cube
Resolution     ... 80 80 80

Calling PlotGrid3d with ATOM-A,B=0,0
Entering PlotGrid3d with Plottype =2
                 *** PLOTTING FINISHED ***
 Output file: pyridine_scf.eldens.cube
```

在 Chimera 中以生成的 cube 文件为输入绘制的该 SCF 电子密度图
如 {numref}`fig:Pyridine_ElDens` 所示。

(fig:Pyridine_ElDens)=
```{figure} ../../images/orca_plot_pyridine_ElDens.*

吡啶 SCF 电子密度
```

(sec:utilities.plot.algebraic_operations)=
### 执行代数运算（Perform Algebraic Operations）

从 ORCA 6 起，可以对计算得到的密度执行简单的代数运算。当前可用的运算列在菜单选项 `10` 中：

```orca
Enter a number: 10
-----------------------------------------------------------------------
Available Algebraic Operations:
-----------------------------------------------------------------------
       1 - Pair Densities Addition

       1 - Pair Densities Addition
       2 - Pair Densities Subtraction
       3 - Pair Densities Multiplication
       4 - Pair Densities Division
       5 - Density Normalization
       6 - Make Natural Transition Orbitals
       7 - Make Natural Difference Orbitals
       8 - Leave Section - Return to Main Menu
```

要执行此类运算，所需的状态或跃迁态密度必须在 `.densities` 文件中可用。
这可以通过在输入中使用 `!KeepDens` 或 `!KeepTransDensity`
关键词请求将相关密度写入磁盘来实现。

注意：存储成百上千个这样的密度需要小心，因为它们可能占用数百 GB 的磁盘空间。

除吡啶的 SCF 计算外，现在让我们用下列输入执行正则 CCSD 计算：

```orca
! CCSD def2-SVP KeepDens

*xyz 0 1
C        0.690940233      0.417992301     -1.170801378
C        0.690940233      1.616339301     -0.458357378
C        0.690940233      1.560238301      0.936438622
N        0.690940233      0.417992301      1.635468622
C        0.690940233     -0.724253699      0.936438622
C        0.690940233     -0.780354699     -0.458357378
H        0.690940233      0.417992301     -2.257043378
H        0.690940233      2.574997301     -0.967574378
H        0.690940233      2.478336301      1.521602622
H        0.690940233     -1.642351699      1.521602622
H        0.690940233     -1.739012699     -0.967574378
*       

```

`orca_plot` 菜单中的选项 `1` 现在将同时提供 scf 和 mdci 电子密度。

```orca
-----------------------------------------------------------------------
Plot-Type is presently: 1
-----------------------------------------------------------------------
Searching for Ground State Electron or Spin Densities:              ...
-----------------------------------------------------------------------
     1 -   molecular orbitals                          
     2 -   (scf) electron density        ......  (scfp    )  => AVAILABLE
     3 -   (scf) spin density            ......  (scfr    )  - NOT AVAILABLE
     4 -   natural orbitals             
     5 -   corresponding orbitals       
     6 -   atomic orbitals              
     7 -   mdci electron density         ......  (mdcip   )  => AVAILABLE

```

让我们通过取 CCSD 和 HF 电子密度之差来计算相关电子密度。
然后，我们需要选择 `Available Algebraic Operations` 菜单的选项 `2`（Pair Densities Subtraction）：

```orca
---------------------
List of density names
---------------------

Index:                                                   Name of Density
------------------------------------------------------------------------
    0:                                                pyridine_ccsd.scfp
    1:                                              pyridine_ccsd.P0.tmp
    2:                                               pyridine_ccsd.mdcip


-----------------------------------------------------------------------
Performing Algebraic Operations Over Densities: => SUBTRACTION
-----------------------------------------------------------------------
Number of Densities to be Processed from the List =>   2:
-----------------------------------------------------------------------
Enter FileName for Density[  0]: pyridine_ccsd.scfp
Provide a Scale Factor for Density[  0] (Default => 1.00): 1
Enter FileName for Density[  1]: pyridine_ccsd.mdcip
Provide a Scale Factor for Density[  1] (Default => 1.00): 1
-----------------------------------------------------------------------
INTERPRETTING EQUATION:
-----------------------------------------------------------------------
1/sqrt(N) * [(1.00) * {pyridine_ccsd.scfp} - (1.00) * {pyridine_ccsd.mdcip}]
-----------------------------------------------------------------------

PlotType       ... DENSITY-PLOT
ElDens File    ... pyridine_ccsd.scfp_minus_pyridine_ccsd.mdcip
Output file    ... pyridine_ccsd.scfp_minus_pyridine_ccsd.mdcip.cube
Format         ... Grid3d/Cube
Resolution     ... 80 80 80

```

生成的 `pyridine_ccsd.scfp_minus_pyridine_ccsd.mdcip.cube` 文件可以直接
用 Chimera 等软件可视化（见 {numref}`fig:Pyridine_ElDens_CCSD_minus_HF`）。

(fig:Pyridine_ElDens_CCSD_minus_HF)=
```{figure} ../../images/orca_plot_pyridine_ElDens_CCSD_minus_HF.*

吡啶 CCSD-HF 电子密度
```

注意：生成的密度存储在密度容器中，以便
进一步处理或妥善存储以备将来使用。
现在选择选项 `9` 时，差值密度将出现在
可用密度中。

```orca
---------------------
List of density names
---------------------

Index:                                                   Name of Density
------------------------------------------------------------------------
    0:                                                pyridine_ccsd.scfp
    1:                                              pyridine_ccsd.P0.tmp
    2:                                               pyridine_ccsd.mdcip
    3:                      pyridine_ccsd.scfp_minus_pyridine_ccsd.mdcip

```

(sec:utilities.plot.natural_transition_difference_orbitals)=
### 绘制自然跃迁轨道（NTO）和自然差值轨道（NDO）（Plot Natural Transition Orbitals and Natural Difference Orbitals）

`orca_plot` 还可用于从任何可用的状态或跃迁密度生成自然跃迁轨道（NTO）和
自然差值轨道（NDO），
无论所用的理论水平如何。现在让我们在吡啶分子上
对态平均 CASSCF(7,8) 计算演示这一点。对该分析，相关密度
需要通过在输入行中包含 `!KeepTransDensity` 关键词存储到磁盘。
相应的 ORCA 输入如下：

```orca
! def2-SVP KeepTransDensity 
  
%casscf
 nel 8
 norb 7
 mult 1
 nroots 10
end


*xyz 0 1
C        0.690940233      0.417992301     -1.170801378
C        0.690940233      1.616339301     -0.458357378
C        0.690940233      1.560238301      0.936438622
N        0.690940233      0.417992301      1.635468622
C        0.690940233     -0.724253699      0.936438622
C        0.690940233     -0.780354699     -0.458357378
H        0.690940233      0.417992301     -2.257043378
H        0.690940233      2.574997301     -0.967574378
H        0.690940233      2.478336301      1.521602622
H        0.690940233     -1.642351699      1.521602622
H        0.690940233     -1.739012699     -0.967574378
*

```

运行该计算后，除 CASSCF 电子密度外，
所有相关的 CASSCF 态和跃迁密度都可用，
正如在主 `orca_plot` 菜单中选择选项 `1` 所见：

```orca
-----------------------------------------------------------------------
Plot-Type is presently: 1
-----------------------------------------------------------------------
Searching for Ground State Electron or Spin Densities:              ...
-----------------------------------------------------------------------
   1 -   molecular orbitals                     
   2 -   (scf) electron density                  ......  (scfp          )  => AVAILABLE
   3 -   (scf) spin density                      ......  (scfr          )  - NOT AVAILABLE
   ...
-----------------------------------------------------------------------
Searching for State or Transition State AO Electron Densities:      ...
-----------------------------------------------------------------------
  23 -   CIS unrelaxed transition AO density     ......  (Tdens-CIS     )  - NOT AVAILABLE
  24 -   ROCIS unrelaxed transition AO density   ......  (Tdens-ROCIS   )  - NOT AVAILABLE
  25 -   CAS unrelaxed transition AO density     ......  (Tdens-CAS     )  => AVAILABLE
  ...
-----------------------------------------------------------------------
Searching for State or Transition State MO Electron Densities:      ...
-----------------------------------------------------------------------
  29 -   CIS unrelaxed transition MO density     ......  (Tdens-CISMO   )  - NOT AVAILABLE
  30 -   ROCIS unrelaxed transition MO density   ......  (Tdens-ROCISMO )  - NOT AVAILABLE
  31 -   CAS unrelaxed transition MO density     ......  (Tdens-CASMO   )  => AVAILABLE
  ...

```

我们现在可以继续生成主导计算得到的 State 1 的 NTO 和 NDO。

```orca
ROOT   1:  E=    -246.3609192216 Eh  5.176 eV  41749.8 cm**-1
      0.82391 [   346]: 2212100
      0.06447 [   295]: 2112200

```

使用 `Available Algebraic Operations` 菜单的选项 `6 =>NTOs`，
可以找到 NTO 的 AO 跃迁密度 ${D}_{01}$ 文件如下：

```orca
-----------------------------------------------------------------------
Performing Algebraic Operations Over Densities: => MAKE_NTOS
-----------------------------------------------------------------------
Enter FileName for Density[  0]: Tdens-CAS-0-0-0-1
Provide a Scale Factor for Density[  0] (Default => 1.00): 1
-----------------------------------------------------------------------
NATURAL TRANSITION ORBITALS GENERATION:
-----------------------------------------------------------------------
Warning: The one-electron matrix doesn't exist - is recalculated (SHARK)
Calculating the overlap matrix            ... done!

------------------------------------------------
NATURAL TRANSITION ORBITALS FOR STATE     1 1A  
------------------------------------------------

STATE    1 1A  :  E=   0.190226 au      5.176 eV    41749.8 cm**-1

Threshold for printing occupation numbers 1.0000e-04

     0  : n=  1.28519446
     1  : n=  0.03997952
     2  : n=  0.01505089
     3  : n=  0.00336119

=> Natural Transition Orbitals (donor   ) were saved in Tdens-CAS-0-0-0-1.1-1A_nto-donor.gbw
=> Natural Transition Orbitals (acceptor) were saved in Tdens-CAS-0-0-0-1.1-1A_nto-acceptor.gbw
-----------------------------------------------------------------------
Provide a Number of NTOs to plot (Default => 1): 1
-----------------------------------------------------------------------
-----------------------------------------------------------------------
Reading Donor NTO-file   : Tdens-CAS-0-0-0-1.1-1A_nto-donor.gbw
-----------------------------------------------------------------------
Generating cube file for Donor NTO[0]:=> Tdens-CAS-0-0-0-1.1-1A_nto-donor.gbw.0.cube
-----------------------------------------------------------------------
Reading Acceptor NTO-file   : Tdens-CAS-0-0-0-1.1-1A_nto-acceptor.gbw
-----------------------------------------------------------------------
Generating cube file for Acceptor NTO[0]:=> Tdens-CAS-0-0-0-1.1-1A_nto-acceptor.gbw.0.cube
Current-settings:

PlotType       ... MO-PLOT
MO/Operator    ... 0 0
Output file    ... Tdens-CAS-0-0-0-1.1-1A_nto-acceptor.gbw.0.cube
Format         ... Grid3d/Cube
Resolution     ... 80 80 80

```

使用 `Available Algebraic Operations` 菜单的选项 `7 =>NDOs`，
可以找到 NDO 的 AO 态密度 $D_{00}-D_{11}$ 文件如下：

```orca
-----------------------------------------------------------------------
Performing Algebraic Operations Over Densities: => MAKE_NDOS
-----------------------------------------------------------------------
Enter FileName for Density[  0]: Tdens-CAS-0-0-0-0
Provide a Scale Factor for Density[  0] (Default => 1.00): 1
Enter FileName for Density[  1]: Tdens-CAS-0-0-1-1
Provide a Scale Factor for Density[  1] (Default => 1.00): 1
-----------------------------------------------------------------------
NATURAL DIFFERENCE ORBITALS GENERATION:
-----------------------------------------------------------------------
Warning: The one-electron matrix doesn't exist - is recalculated (SHARK)
Calculating the overlap matrix            ... done!

------------------------------------------------
NATURAL DIFFERENCE ORBITALS FOR STATE     1 1A  
------------------------------------------------

STATE    1 1A  :  E=   0.190226 au      5.176 eV    41749.8 cm**-1

Threshold for printing occupation numbers 1.0000e-04

     0  : n=  0.49881235
     1  : n=  0.08492368
     2  : n=  0.06708141
     3  : n=  0.01254920
     4  : n=  0.00667407
     5  : n=  0.00006162

=> Natural Difference Orbitals (donor   ) were saved in Tdens-CAS-0-0-0-0-Tdens-CAS-0-0-1-1.1-1A_ndo-donor.gbw
=> Natural Difference Orbitals (acceptor) were saved in Tdens-CAS-0-0-0-0-Tdens-CAS-0-0-1-1.1-1A_ndo-acceptor.gbw
-----------------------------------------------------------------------
Provide a Number of NDOs to plot (Default => 1): 1
-----------------------------------------------------------------------
-----------------------------------------------------------------------
Reading Donor NDO-file   : Tdens-CAS-0-0-0-0-Tdens-CAS-0-0-1-1.1-1A_ndo-donor.gbw
-----------------------------------------------------------------------
Generating cube file for Donor NDO[0]:=> Tdens-CAS-0-0-0-0-Tdens-CAS-0-0-1-1.1-1A_ndo-donor.gbw.0.cube
-----------------------------------------------------------------------
Reading Acceptor NDO-file   : Tdens-CAS-0-0-0-0-Tdens-CAS-0-0-1-1.1-1A_ndo-acceptor.gbw
-----------------------------------------------------------------------
Generating cube file for Acceptor NDO[0]:=> Tdens-CAS-0-0-0-0-Tdens-CAS-0-0-1-1.1-1A_ndo-acceptor.gbw.0.cube
Current-settings:

PlotType       ... MO-PLOT
MO/Operator    ... 0 0
Output file    ... Tdens-CAS-0-0-0-0-Tdens-CAS-0-0-1-1.1-1A_ndo-acceptor.gbw.0.cube
Format         ... Grid3d/Cube
Resolution     ... 80 80 80

```

使用所得 cube 文件，可以方便地可视化相应的 Donor 和 Acceptor NTO 与 NDO 轨道
对，如 {numref}`fig:Pyridine_s1_casscf_nto_ndo` 中所示。

(fig:Pyridine_s1_casscf_nto_ndo)=
```{figure} ../../images/orca_plot_pyridine_pyridine_s1_casscf_nto_ndo.*

吡啶 SA-CASSCF(8,7) State 1 的 NTO/NDO donor/acceptor 轨道对
```

注意：始终处理 AO 基密度既有益又更准确。
特别是，处理约化的 MO 基密度既不可能也不正确。

(sec:utilities.plot.ESP)=
### 执行静电势绘图（Perform Electrostatic Potental Plots）

从 ORCA 6.1 起，可以在 `orca_plot` 中为密度容器中可用的任何态密度生成静电势（ESP）。

执行电子结构计算后（例如使用 [输入](#sec:utilities.plot.inpscfplot)），在 `orca_plot` 中按如下步骤进行：

首先，选择 `1 - Enter type of plot`，然后选择 `43 - Electrostatic potential`。

```orca
    41 -   ROCIS QDPT unrelaxed transition AO density ......  (Tdens-ROCISQDSOC )  - NOT AVAILABLE
    42 -   LFT QDPT unrelaxed transition AO density   ......  (Tdens-LFTQDSOC   )  - NOT AVAILABLE
-----------------------------------------------------------------------
    43 -   Electrostatic Potential   
```

系统将提示您指定要计算静电势的态密度名称。

```orca
Enter Type: 43

---------------------
List of density names
---------------------

Index:                                                   Name of Density
------------------------------------------------------------------------
    0:                                                 pyridine_scf.scfp


Enter Name for an STATE Density: pyridine_scf.scfp
```

最后，选择选项 `11 - Generate the plot` 计算静电势并生成文件 `pyridine_scf.scfp.esp.cube`。

所得 `.cube` 文件包含静电势数据，可以直接可视化或用于在任何兼容的图形用户界面工具中为密度图着色。


(fig:Pyridine_ElDensESP)=
```{figure} ../../images/orca_plot_pyridine_ElDens_ESPcolour.*

使用 ESP 着色的吡啶 SCF 电子密度
```

(sec:utilities.plot.tips)=
### 关于密度图的更多提示（Additional TIPS regarding Density Plots）

1) 作为菜单选项 `9` 的替代方案，可以通过读取 `.densities` 文件中包含的所有密度列表
直接查看计算目录中有哪些密度可用：

```orca
orca_plot mymol.densities
```

2) `orca_plot` 也可以为计算量大的绘图以并行模式运行：

```orca
mpirun -np 4 /orca_path/orca_plot_mpi MyGBWFile.gbw -i MyGBWFile
```

3) 可以使用 `orca_plot` 直接从 .cis 计算信息创建 CIS 或 TD-DFT 计算中
基态与激发态之间的差值密度。这作为一个额外的
交互式菜单项实现，（希望）是不言自明的。
从 ORCA 6 起可以使用 `Algebraic Operations`
实用菜单直接从生成的态和跃迁密度
执行这些运算。

3) 也可以使用 `orca_plot` 通过 `.cis` 文件创建 CIS 或 TD-DFT 计算中
基态与激发态之间的差值密度。
该功能作为额外的交互式菜单选项实现，（希望）是不言自明的。从 ORCA 6 起，这些密度也可以通过
`Algebraic Operations` 菜单获得，直接处理生成的态和跃迁密度。

(sec:utilities.2mkl)=
## orca_2mkl：旧版 Molekel 以及 Molden 输入（Old Molekel as well as Molden inputs）

`orca_2mkl` 实用程序将 `.gbw` 文件转换为 `.mkl` ASCII 文件。
`.mkl` 文件包含的信息与 `.gbw` 文件基本相同，
但不包括 ORCA 特定的内部标志。ASCII 格式使其适合
外部使用——例如，可以由 Molekel 读取用于可视化
或由自定义后处理脚本访问。因此，`.mkl` 文件
为开发与第三方工具的接口提供了便捷的起点。
`orca_2mkl` 可以简单地这样调用：

```orca
orca_2mkl BaseName 
      (will produce BaseName.mkl from BaseName.gbw)
orca_2mkl BaseName -molden
      (writes a file in molden format)
orca_2mkl BaseName -mkl
      (writes a file in MKL format)
```

任何 gbw 类文件（包含 QRO、UNO、UCO 等轨道）都可以用 `orca_2mkl` 转换为
mkl 和 Molden 格式：

```orca
orca_2mkl gbw_type_file.extension mkl_file.extension -mkl -anyorbs 
# or
orca_2mkl gbw_type_file.extension molden_file.extension -molden -anyorbs
```

`orca_2mkl` 也可以反向运行，从 `.mkl` 文件生成 `.gbw` 类文件：

```orca
orca_2mkl BaseName -gbw
      (will produce BaseName.gbw out of BaseName.mkl)
```

该功能允许用户将分子轨道从外部来源导入 ORCA。虽然此功能很少使用且能力有限，但为希望尝试的用户在此列出。该用法的示例在随 ORCA 手册附带的 CASSCF 教程中演示。

最后，一些第三方工具可用于将其他量子化学程序的波函数文件与 MKL 格式相互转换，例如 MOKIT（https://gitlab.com/jxzou/mokit）。与 `orca_2mkl` 结合，这提供了一种便捷方式，可在其他程序中使用 ORCA 生成的分子轨道，或反过来。一个示例应用是使用 ORCA 的 TRAH 方法收敛困难的 SCF 问题，然后将收敛的轨道传递给没有 TRAH 收敛器的另一个程序。另一个示例是从另一个程序读入困难体系的轨道，然后用 ORCA 计算其高水平单点能（使用另一个程序不支持的泛函或方法），而不必从 PModel 初始猜测收敛波函数。最后，MOKIT 可以将 MKL 格式转换为 PySCF 格式，这允许在 Python 环境中操作 ORCA 分子轨道。

(sec:utilities.2aim)=
## orca_2aim

该实用程序读取 `.gbw` 文件并创建 `.wfn` 和 `.wfx` 文件，可供其他程序用于电子密度的拓扑分析。这适用于开壳层和闭壳层波函数。它可以通过在 ORCA 输入文件的简单输入行中包含 `! AIM` 来调用，或在终端中输入如下：

```orca
orca_2aim BaseName 
      (will produce BaseName.wfn and BaseName.wfx from BaseName.gbw)
```

(sec:utilities.vpot)=
## orca_vpot

`orca_vpot` 程序计算用户定义的一组给定点上的静电势。它既可以与输入文件一起使用，也可以在交互模式下使用。它需要四个参数：

```orca
orca_vpot  MyJob.gbw  MyJob.scfp  MyJob.vpot.xyz  MyJob.vpot.out
```

*第一*：包含正确几何结构和基组的 `gbw` 文件

*第二*：该基组下所需的密度矩阵（也许使用 `KeepDens` 关键词）

*第三*：目标位置的 ASCII 文件（原子单位），例如

```
6                 (number_of_points)
  5.0 0.0  0.0    (XYZ coordinates)
 -5.0 0.0  0.0
  0.0 5.0  0.0
  0.0-5.0  0.0
  0.0 0.0  5.0
  0.0 0.0 -5.0
```

*第四*：目标文件，它将包含静电势，例如

```
6                 (number of points)
 VX1  VY1  VZ1    (potential for first point)
 VX2  VY2  VZ2    (potential for second point)
  etc.
```

读取该文件并将势用于预期目的是很直接的。

`orca_vpot` 可以按如下方式以并行模式调用：

```
mpirun -np 4 /full_path/orca_vpot_mpi MyJob.gbw MyJob.scfp MyJob.pot.xyz MyJob.pot.out
```

它可用于检查 MyJob.densities 中的可用密度：

```
orca_vpot  MyJob.densities
```

如果 `.gbw` 和 `.densities` 文件的基名不匹配，
`.densities` 文件的基名必须作为第五个参数传递：

```
orca_vpot  MyJob.gbw  OtherJob.scfp  MyJob.pot.xyz  MyJob.pot.out  OtherJob
```

不带任何参数调用 `orca_vpot` 将显示帮助消息。

(sec:utilities.euler)=
## orca_euler

`orca_euler` 实用程序计算所计算的超精细耦合（HFC）或核四极耦合（NQC）张量与参考张量（通常是 g 张量或 D 张量）之间的相对取向。
如果在同一次运行中既计算了 HFC/NQC 又计算了 g-/D-张量，`orca_euler` 程序会在 ORCA 作业结束时自动调用。
或者，它可以作为独立程序执行，前提是
来自先前 NQC/HFC- 和 D- 或 g-张量计算的 .property.txt 文件可用。

张量之间的取向表示为 3×3 旋转矩阵 R，
由三个 Euler 角参数化：$\alpha$、$\beta$ 和 $\gamma$。
这些角通过三次绕不同轴的连续旋转将 A 与 B 对齐，
定义张量 A 相对于张量 B 的相对取向，
即在常用的 z-y-z 约定中：

-   **将 A$_{xyz}$ 绕其 $z$ 轴逆时针旋转 $\alpha$
    得到 A$_{x'y'z'}$。**

-   **将 A$_{x'y'z'}$ 绕其 $y'$ 轴逆时针旋转
    $\beta$ 得到 A$_{x''y''z''}$。**

-   **将 A$_{x''y''z''}$ 绕其 $z''$ 轴逆时针旋转
    $\gamma$ 使其与 B 对齐。**

`orca_euler` 程序的选项如下：

```orca
orca_euler prop-file options

  file    = basename of an ORCA .property.txt file

  options  
   -refg/-refD:         Reference tensor (g-tensor or D-tensor, default is -refg)
   -conv zyz/-conv zxz: Euler rotation convention (default is zyz)
   -order:              Ordering of the reference tensor (x, y, z) with respect to 
                        ORCA output (min, mid, max)
   -plotA:              plot the HFC-tensors
   -plotQ:              plot the NQC-tensors
   -detail:             print detailed information
```

注意：

-   默认情况下，只有当 $S$
    \>$\frac{1}{2}$ 且 D\>0.3 cm$^{-1}$ 时才将 D 张量用作参考张量。在所有其他情况下，将
    g 张量用作参考张量。用户可以通过使用 --`refg` 或 --`refD`
	手动选择参考张量（如果在 `.property.txt` 文件中可用）。

-   默认情况下，Euler 旋转使用 z–y–z 约定执行。
    可以通过使用选项 --`conv zxz` 手动选择 z-x-z 约定。

-   默认情况下，g- 或 D-张量的轴根据其分量的大小分配：
    g$_{\text{min} }\to  g_{x}$、
    g$_{\text{mid} }\to g_{y}$、g$_{\text{max} }\to  g_{z}$（D 类似）。
    运行独立程序时可以用 --`order` 选项手动修改此排序，如下所示：

|                |                                          |
|---------------:|:-----------------------------------------|
|  -order 3 2 1: | min $\to$ z                              |
|                | mid $\to$ y                              |
|                | max $\to$ x                              |
| -order 1 -2 3: | min $\to$ x                              |
|                | mid $\to$ y (flipped in the orientation) |
|                | max $\to$ z                              |

-   可以生成 `.xyz` 格式的文件，使用 `orca_euler` 程序
	配合选项 --`plotA` 或 --`plotQ` 来绘制核超精细
	和四极耦合张量。例如，原子 3（从零开始计数）的 HFC 张量
	保存为 `prop-file.3.A.xyz`，
	相应的 NQC 张量保存为 `prop-file.3.Q.xyz`。这些 xyz 文件
	包含四个虚构原子（He、Ne、Ar、Kr），其中张量轴的方向
	定义为向量：x 轴从 He 到 Ne；
	y 轴从 He 到 Ar；z 轴从 He 到 Kr。

-   要打印旋转矩阵的实际定义以及关于相对取向的更多信息，
    使用 --`detail` 选项。

(sec:utilities.exportbasis)=
## orca_exportbasis

`orca_exportbasis` 实用程序打印出 ORCA 使用的基组。它需要 ORCA 输入行中指定的基组名称。可选参数包括 ECP 基组、特定原子列表和输出文件名。输出以 ASCII 格式写入，可以查看和手动编辑。用户可以选择以 `ORCA` 格式（可直接复制到输入文件中）或 `GAMESS-US` 格式（可通过 %basis 块作为外部指定基组使用）导出基组。

**注意：** 含特殊字符的基组名称可能需要一对引号（" 或 '）才能正确识别。

`orca_exportbasis` 的用法和选项如下：

```
USAGE: orca_exportbasis keywords options

       -b, --basis  : name of basis set                                                        
                      def2-svp                                                                 
                      'def2-tzvp(-f)' - string to be passed with literals                       

EXAMPLE: orca_exportbasis -b svp
```

```
Additional Options:

       -e, --ecp    : ecp basis                                                                
                      sdd                                                                      
                      default        - ECP-part of basis (if present)                          

       -f, --format : output format                                                            
                      ORCA           - to be read via %basis NewGTO                           
                      GAMESS-US      - to be read as %basis GTOName 'mybasis.bas'             
                      default        - ORCA                                       
       -a, --atoms  : list of elements                                                         
                      Cu             - single element                                          
                      Ga Ge As Se    - list of elements separated by blanks                    
                      default        - whole periodic table is printed                         

       -o, --outfile: name of outputfile                                                       
                      mybasis.bas                                                              
                      default        - derived name                                            

EXAMPLE: orca_exportbasis -b svp -e sdd -a Ag -f GAMESS-US -o mybasis.bas
```

以 `GAMESS-US` 格式存储的输出文件可以在下一次 ORCA 计算的 %basis 块中调用——见 {ref}`sec:essentialelements.basisset.file`。

```orca
%basis
GTOName      "mybasis.bas"
GTOAuxJName  "myauxjbasis.bas"
GTOAuxJKName "myauxjkbasis.bas"
GTOAuxCName  "myauxjcbasis.bas"
end
```

(sec:utilities.eca)=
## orca_eca

`orca_eca` 实用程序使用计算得到的交换耦合常数，通过对角化自旋哈密顿量计算所有可能自旋态的相对能量。所得自旋态的绝对和相对能量分别打印在 `*.en` 和 `*.en0` 文件中。此外，现场自旋期望值写入 `*.sp` 文件。下列示例计算 Mn(III) 与 Mn(IV) 之间交换耦合常数为 -152.48 cm\*\*-1 的体系的自旋阶梯。

```orca
%sim
ms_bs 0.5 # Arbitrary spin state 
end

# specification of spin centers
$spins 2 
1 2.0  # Spin on first manganese
2 1.5  # Spin on second manganese

# Exchange coupling constant (H = -2J S1 S2)
$ecc 1
1 -152.48
    
$aiso_bs 2 # A false segment just to print the *.sp file
1 0.00
2 0.00
```

(sec:utilities.pnmr)=
## orca_pnmr

`orca_pnmr` 程序使用 EPR $g$、$A$ 和 $D$ 张量计算 NMR 屏蔽张量的顺磁贡献（理论背景见章节 {ref}`sec:spectroscopyproperties.pnmr`）。它是一个独立程序，可以在主 ORCA 计算完成后从命令行执行。或者，它可以使用选项 `-i` 从输入文件读取用户提供的 $g$/$A$/$D$ 张量。请注意 `orca_pnmr` 期望 $g$ 和 $A$ 张量遵循章节 {ref}`sec:spectroscopyproperties.properties.eprnmrConv` 中描述的约定。

`orca_pnmr` 的用法和选项如下：

```orca
USAGE:    orca_pnmr BaseName [-i] [-v]

OPTIONS:  -i  : read from the input file "BaseName.pnmr.inp"
          -v  : print more output (Z matrices)
```

不带任何选项运行时，`orca_pnmr` 尝试从文件 `BaseName.property.txt` 中提取 $g$、$D$ 和 $A$ 张量并计算 298 K 下的顺磁屏蔽。此功能仅在张量是用 EPRNMR 模块计算时才有效。更灵活、可控的方法是手动编辑 `BaseName.pnmr.inp`（内容见下文）然后用选项 --`i` 运行 `orca_pnmr`。

```orca
3    # Spin multiplicity (2S+1)
298  # Temperature range minimum [K]
300  # Temperature range maximum [K]
1    # Temperature step [K]
1    # Have g-tensor? 0 or 1
  2.004689   0.000000  -0.000000 # Cartesian g-tensor
  0.000000   2.004689   0.000000 # (if available)
  0.000000   0.000000   2.002123
1    # Have D-tensor? 0 or 1
 -0.514341  -0.000000  -0.000000 # Cartesian D-tensor [cm-1]
 -0.000000  -0.514341  -0.000000 # (if available)
 -0.000000  -0.000000   1.028682
2    # Number of A-tensors
0O   # First nucleus (index,element)
-72.358765                       # Prefactor [MHz]
-78.989514   0.000000  -0.000000 # Cartesian A-tensor [MHz]
  0.000000 -78.989514  -0.000000
 -0.000000  -0.000000  53.478581
1O   # Next nucleus (index,element)
-72.358765                       # Prefactor [MHz]
-78.989516   0.000000  -0.000000 # Cartesian A-tensor [MHz]
  0.000000 -78.989516  -0.000000
 -0.000000  -0.000000  53.478580
# ... Further nuclei
```

-   $D$ 和 $g$ 张量是可选的。如果未提供，`orca_pnmr` 
    假定各向同性的自由电子 $g$ 值并设 $D = 0$。

-   $A$ 张量是必需的。如果给定核没有提供 $A$ 张量，
	则无法为该核计算顺磁 NMR 屏蔽。

(sec:utilities.lft)=
## orca_lft

从 ORCA 5.0 起，ORCA 提供了一个名为 `orca_lft` 的独立多重态程序。

-   `orca_lft` 专为实验光谱学家打造。

-   它能够运行任意数量的光谱模拟，重点是 X 射线光谱。

本节我们简要回顾 `orca_lft` 的主要功能。
更详细的描述和示例讨论请参阅 `orca_lft` 教程。

1.  目标是能够计算给定 LFT 中心（离子）的各种光谱性质，
    前提是能以例如 LFT 矩阵的对角元
    （LFT 轨道能量）和给定 LFT 问题的 Slater-Condon 参数
    的形式手动传递单电子和双电子积分的信息。

2.  这将使实验光谱学家能够在实际运行实验期间
    执行大量光谱模拟

任何 LFT 问题都可以用单电子 $H_{LF}$ 矩阵
元和 Slater-Condon 双电子积分 F0、F2、F4（或 d 壳层的
Racah 参数 A、B、C）来参数化。（图：
{numref}`fig:LFT_Integrals`）

(fig:LFT_Integrals)=
```{figure} ../../images/LFT_Integrals.*

用单电子能量和 Slater Condon 参数（SCP）定义 LFT 问题

```

实践中我们需要知道：

1.  给定 LFT 问题的 Slater Condon 参数

2.  $H_{LF}$ 矩阵元或它们之间的关系（配体场
    分裂、10Dq、AOM 模型）

orca_lft 的设计工作流如下：

-   在用户指定的 LFT 问题上求解一般 CI 问题：离子
    类型、电子数、涉及的壳层、涉及的
    多重度

-   计算所有可能的非相对论态/多重度

-   在 CSF 基上计算跃迁密度

-   在给定 LFT 基（即 2p3d）中计算所需的跃迁矩

-   计算各种性质，重点是 X 射线光谱（ABS、
    XAS、XES、RIXS）的非相对论极限

-   在准简并微扰理论基础上计算相应的
    相对论校正态

-   提供对各种相对论校正性质的访问（ABS、
    XAS、XES、RIXS、MCD、XMCD、G 张量、D 张量、超精细耦合、
    电场梯度）

`orca_lft` 需要自己的输入。只需从终端执行它

```orca
orca_lft
```

即可获得用法打印：

```
********************************************************************
Simulate or Fit Spectra
********************************************************************

====================================================================
Usage: orca_lft BaseName.lft.inp [options]
====================================================================

--------------------------------------------------------------------
[Options]:
--------------------------------------------------------------------
-sim                       Simulate Spectra
-fit                       Fit Spectra (This is not yet availiable!)
--------------------------------------------------------------------

********************************************************************
Generate Initial Input
********************************************************************

====================================================================
Usage: orca_lft BaseName [options]
====================================================================
```

各种运行选项：

```
------------------------------------------------------------------------------------------------------------
[Options]:
------------------------------------------------------------------------------------------------------------
-p_case                       Requests  p-shell case
-d_case                       Requests  d-shell case
-f_case                       Requests  f-shell case
-sp_case                      Requests sp-shell case
-ps_case                      Requests sp-shell case
-sd_case                      Requests sd-shell case
-ds_case                      Requests ds-shell case
-sf_case                      Requests sf-shell case
-fs_case                      Requests fs-shell case
-pd_case                      Requests pd-shell case
-dp_case                      Requests dp-shell case
-pf_case                      Requests pf-shell case
-fp_case                      Requests fp-shell case
-df_case                      Requests pf-shell case

-fd_case                      Requests fp-shell case
-spd_case                     Requests spd-shell case
-spf_case                     Requests spf-shell case
-sdf_case                     Requests sdf-shell case
-pdf_case                     Requests pdf-shell case
-soc                          Requests Input with SOC Constants
-atnoN                        Sets Atomic Number N
------------------------------------------------------------------------------------------------------------
-Special Cases for known Elements. LFT Parameters are filled from an internal AILFT NEVPT2 database

--------------------------------------Supported Oxidation States--------------------------------------------
Presently Default Oxidation States are supported except for Fe:
Main Elements                 -> O
TM Elements (Fe(26))          -> I,II,III
TM Elements (All other)       -> II
Lanthanide/Actinide Elements  -> III
--------------------------------------------Valence Cases---------------------------------------------------
-atnoN  -2s2p_case            Requests 2s2p-shell case for element with atomic number N (4-9)  
-atnoN  -3s3p_case            Requests 3s3p-shell case for element with atomic number N (12-18)
-atnoN  -4s4p_case            Requests 4s4p-shell case for element with atomic number N (20,31-36)
-atnoN  -4s4p_case            Requests 5s5p-shell case for element with atomic number N (38,49-54)
-atnoN  -3d4s_case            Requests 3d4s-shell case for element with atomic number N (22-29)
-atnoN  -4d5s_case            Requests 4d5s-shell case for element with atomic number N (40-47)
-atnoN  -5d6s_case            Requests 4d6s-shell case for element with atomic number N (72-79)
-atnoN  -4f5d_case            Requests 4d5d-shell case for element with atomic number N (59-70)
-atnoN  -5f6d_case            Requests 5d6d-shell case for element with atomic number N (91-102)
-----------------------------------------Core-Valence Cases------------------------------------------------
-atnoN  -1s3d_case            Requests 1s3d-shell case for element with atomic number N (22-29)
-atnoN  -2p3d_case            Requests 2p3d-shell case for element with atomic number N (22-29)
-atnoN  -3p3d_case            Requests 3p3d-shell case for element with atomic number N (22-29)
--------------------------------------Core-Valence XES Cases------------------------------------------------
-atnoN  -1s2p3d_case          Requests 1s2p3d-shell case for element with atomic number N (22-29)
-atnoN  -1s3p3d_case          Requests 1s3p3d-shell case for element with atomic number N (22-29)
------------------------------------------------------------------------------------------------------------
```

以及各种光谱模拟选项：

```
************************************************************************************************************
Spectra Simulation Options for the BaseName.lft.inp:
************************************************************************************************************

------------------------------------------------------------------------------------------------------------
TIP: Switch ON a Property calculation as DoProperty true:
------------------------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------------------------
General Input Parameters:
------------------------------------------------------------------------------------------------------------
NEl                           Sets the number of electrons
Shell_PQN                     Sets the principle quantum number per type of shells (s,p,d,f)
LFTCase                       !!!ALTERNATIVE TO Shell_PQN!!! Sets the given LFT problem (2p3d, 1s3p3d, ...)
----------------------------------------------------------------------------------------------------------- 
LFTCase WILL replace Shell_PQN                                                
----------------------------------------------------------------------------------------------------------- 
(e.g. Shell_PQN = 0,2,3,0 for a 2p3d calculation)
Mult                          Sets the Multiplicity/Multiplicities
NRoots                        Sets the number of Roots/Multiplicity
TMultiplets (0.01)            Threshold for the Multiplets grouping in eV
DoeV                          All values in eV. This is default. If set false the cm-1 unit is used throughout
DoRAS                         Requests a RASCI calculation
RAS(nel: m1 h/ m2 / m3 p)     Computes the X-Ray Emission Spectra

RAS-reference with nel electrons
m1= number orbitals in RAS-1
h = max. number of holes in RAS-1
m2= number of orbitals in RAS-2 (any number of electrons or holes)
m3= number of orbitals in RAS-3
p = max. number of particles in RAS-3

DoElastic                     Computes in addition the Elastic Scattering terms in RIXS/RIXSSOC calculations
------------------------------------------------------------------------------------------------------------
Non Relativistic Spectroscopic Properties:
------------------------------------------------------------------------------------------------------------
DoABS/DoXAS                   Computes the Absorption like Spectra
DoCD                          Computes the CD Spectra
DoXES                         Computes the X-Ray Emission Spectra
DoRIXS                        Computes the RIXS Spectra
DoQuadrupole                  Computes the ABS,XAS,RIXS Spectra beyond dipole approximation
------------------------------------------------------------------------------------------------------------
Relativistically Corrected Spectroscopic Properties:
------------------------------------------------------------------------------------------------------------
DoSOC                         Requests the Spin Orbit Coupling Calculations
Note that this turned on automatically if zeta SOC
constant are provided
------------------------------------------------------------------------------------------------------------
DoABS/DoXAS                   Computes the SOC Corrected Absorption like Spectra
DoCD                          Computes the SOC Corrected CD Spectra
DoMCD/DoXMCD                  Computes the SOC Corrected MCD/XMCD Spectra
DoXESSOC:                     Computes the SOC Corrected XES Spectra
DoRIXSSOC:                    Computes the SOC Corrected RIXS Spectra
DoQuadrupole                  Computes the SOC Corrected ABS,XAS, XES RIXS Spectra beyond dipole approximation
------------------------------------------------------------------------------------------------------------
Magnetic Properties:
------------------------------------------------------------------------------------------------------------
DoMagnetization               Computes the Magnetization
DoSusceptibility              Computes the Susceptibilities
DoGTensor                     Computes the g-Tensors/Matrices
DoDTensor                     Computes the Zero-Field Splittings
DoATensor                     Computes the Hyperfine Tensors
DoEFGTensor                   Computes the Electric Field Gradient Tensors
(also Moesbauer Parameters in the presence of Fe centers)
------------------------------------------------------------------------------------------------------------
Variable Parameters (if they are not given, default values are used)
------------------------------------------------------------------------------------------------------------
Temperature(300)              Temperature to be used in the SOC calculations
MagneticField(0)              Magnetic Field (in Gauss)
NPointsPsi(10)                Solid Angle Integration points Psi for MCD and XMCD
NPointsPhi(10)                Solid Angle Integration points Phi for MCD and XMCD
NPointsTheta(10)              Solid Angle Integration points Theta for MCD and XMCD
------------------------------------------------------------------------------------------------------------
Variable Parameters needed for Magnetization and Susceptibility calculations
------------------------------------------------------------------------------------------------------------
LebedevIntegrationPoints(26)  Number for Integration points for Lebedev)
LebedevPrec(5)                Precision of the grid for different field directions
(meaningful values range from 1 (smallest) to 10 (largest)
nPointsFStep (5)              Number of steps for numerical differentiation
(def: 5, meaningful values are 3, 5 7 and 9)
MAGTemperatureMIN(4.0)        Minimum Temperature (K) for Magnetization
MAGTemperatureMAX(4.0)        Maximum Temperature (K) for Magnetization
MAGTemperatureNPoints(1)      Number of Temperature points for Magnetization
MAGFieldStep(100.0)           Size of Field step for numerical differentiation (def: 100 Gauss)
MAGFieldMin(0.0)              Minimum Field (Gauss) for Magnetization
MAGFieldMax(70000.0)          Minimum Field (Gauss) for Magnetization
MAGNPoints(15)                Number of Field points for Magnetization
SUSTempMin(1)                 Minimum Temperature (K) for Susceptibility
SUSTempMxn(300.0)             Maximum Temperature (K) for Susceptibility
SUSNPoints(300)               Number of Temperature points for Susceptibility
SUSStatFieldMIN(0.0)          Minimum Static Field (Gauss) for Susceptibility
SUSStatFieldMAX(1)            Maximum Static field (Gauss) for Susceptibility
SUSStatFieldNPoints(1)        Number of Static Fields for Susceptibility
------------------------------------------------------------------------------------------------------------
```

`orca_lft` 可以通过用 orca_lft 处理输入文件（`Basename.lft.inp`）独立运行

```orca
orca_lft BaseName.lft.inp -sim
```

或者，可以这样调用主 orca 程序

```orca
orca BaseName.lft.inp
```

两种运行方式的不同优势在 `orca_lft` 教程中提供

`orca_lft` 还可用于自动生成初始的正确输入文件。例如，可以通过运行

```orca
orca_lft BaseName -pd_case
```

生成初始的裸输入文件 `basename.lft_pd.inp`

```
-----------------------------------------------------------------
Initial Input: BaseName.lft_pd.inp for Orca_LFT has been generated: 
-----------------------------------------------------------------
```

生成的示例输入必须填入所需的 LFT 参数和所期望的光谱性质，然后即可启动模拟——就像在任何标准多重态程序中一样。

```orca
%lft


#-----Parameters------
NEl= 0
Shell_PQN= 0, 2, 3, 0
Mult= 0
NRoots= -1
#--------------------


#---Slater-Condon Parameters---
#---All Values in eV---
PARAMETERS
F0pp =  0.00
F2pp =  0.00
F0dd =  0.00
F2dd =  0.00
F4dd =  0.00
F0pd =  0.00
F2pd =  0.00
G1pd =  0.00
G3pd =  0.00
end
#--------------------


#---Diagonal LFT-Matrix Elelemnts---
#---All Values in eV---
FUNCTIONS
0   0 " 0.00"
1   1 " 0.00"
2   2 " 0.00"
3   3 " 0.00"
4   4 " 0.00"
5   5 " 0.00"
6   6 " 0.00"
7   7 " 0.00"
end
#--------------------


#---SPECTRA/PROPERTIES---
DoABS true
#---------
end


*xyz 0 0
Atom 0.00 0.00 0.00
*
```

也可以生成基于内部 NEVPT2 数据库的特殊初始输入。对 Ni(II) 的 2p3d LFT 情形，可按如下方式操作：

```orca
orca_lft BaseName -atno28 -2p3d_case
```

```
------------------------------------------------------------------------------
Creating input for Atom Ni(II) ...
------------------------------------------------------------------------------

-----------------------------------------------------------------
Initial Input: BaseName.lft_pd.inp for Orca_LFT has been generated: 
-----------------------------------------------------------------
```

生成的 `BaseName.lft_pd.inp` 文件包含从内部 NEVPT2 数据库预填充的 LFT 参数，基于预计算的 CASCI/NEVPT2 AILFT 值。所得可直接运行的 $Ni^{II}$ 输入如下：

```orca
%lft


#-----Parameters------
NEl= 14
LFTCase 2p3d
Mult= 3, 1
NRoots= 25, 30
#--------------------


#---Slater-Condon Parameters---
#---All Values in eV---
PARAMETERS
F0pp =  85.88
F2pp =  54.77
F0dd =  23.31
F2dd =  13.89
F4dd =  9.14
F0pd =  33.03
F2pd =  7.76
G1pd =  6.42
G3pd =  2.11
end
#--------------------


#---Diagonal LFT-Matrix Elelemnts---
#---All Values in eV---
FUNCTIONS
0   0 " 0.00"
1   1 " 0.00"
2   2 " 0.00"
3   3 "1138.35"
4   4 "1138.35"
5   5 "1138.35"
6   6 "1138.35"
7   7 "1138.35"
end
#--------------------


#---SPECTRA/PROPERTIES---
DoABS true
#---------
end


*xyz 2 3
Ni 0.00 0.00 0.00
*
```

或者，如从头算配体场理论章节
（{ref}`sec:modelchemistries.casscf.AbInitioLFT`）所讨论的，可以实际运行
双壳层 AILFT 计算并生成相应的 `.nevpt2.lft.inp` 文件

```orca
!NoIter NEVPT2 def2-SVP def2-SVP/C


%method
frozencore fc_none
end

#--------------------
#Rotate Orbitals
#--------------------
%scf
rotate
{2,6,90}
{3,7,90}
{4,8,90}
end
end

#--------------------
#General Options
#--------------------
%casscf
nel 14
norb 8
mult 3,1
nroots 100,100

LFTCase 2p3d
rel
dosoc true
end
end


*xyz 2 3
Ni      0.0000000000      0.0000000000      0.0000000000
*
```

`orca_lft` 输入的结构如下：

它包含：

-   定义 LFT 问题的通用参数块
    
    ```orca
    -----Parameters------ 
    NEl= 14 
    LFTCase 2p3d 
    #Shells_PQN 0,2,3,0, Alternative definition using s,p,d,f main quantum numbers Mult= 3, 1
    NRoots= 25, 30 
    --------------------
    ```

-   定义 SCP 和 SOC 常数参数的 PARAMETERS 块
    
    ```orca
    ---Slater-Condon Parameters---
    ---All Values in eV--- 
    PARAMETERS
    F0pp = 85.88 
    F2pp = 54.77 
    F0dd = 23.31 
    F2dd = 13.89 
    F4dd = 9.14 
    F0pd = 33.03 
    F2pd = 7.76 
    G1pd = 6.42 
    G3pd = 2.11 
    end 
    --------------------
    ```

    ```orca
    ---SOC-CONSTANTS---
    ---All Values in eV--- 
    PARAMETERS 
    ZETA_P = 10.68
    ZETA_D = 0.08 
    end 
    --------------------
    ```

-   定义 LFT 矩阵的 FUNCTIONS 块

    ```orca
    ---Diagonal LFT-Matrix Elelemnts---
    ---All Values in eV--- 
    FUNCTIONS
    0   0 " 0.00"
    1   1 " 0.00"
    2   2 " 0.00"
    3   3 "1138.35"
    4   4 "1138.35"
    5   5 "1138.35"
    6   6 "1138.35"
    7   7 "1138.35"
    end
    --------------------
    ```

-   指定所期望模拟性质的性质块

    ```orca
    ---SPECTRA/PROPERTIES--- 
    DoABS true 
    --------------------
    ```

-   定义离子、电荷、多重度和坐标（0. 0. 0.）的 xyz 块

    ```orca
    *xyz 2 3 Ni 0.0000000000 0.0000000000 0.0000000000
    ```


:::{admonition} 注意
:class: note
应当强调的是，`orca_lft` 通过 FUNCTIONS 和 PARAMETERS
子块提供

-   单电子 LFT 矩阵和 Slater–Condon 参数的任意参数化
-   强大的参数扫描能力

这有助于在没有任何对称性限制的情况下执行任何类型的模拟。下面提供了一个关于 FUNCTIONS 和 PARAMETERS
子块使用的示例，而带有详细算例的 `orca_lft` 教程
将很快推出。
:::

让我们用下列输入执行 $Ni^{2+}$ L 边 XAS 光谱模拟：

```
%lft


  #-----Parameters------
  NEl= 14
  LFTCase 2p3d
  Mult= 3, 1
  NRoots= 25, 30
  #--------------------
  
  
  #---Slater-Condon Parameters---
  #---All Values in eV---
  PARAMETERS
    F0pp =  85.88
    F2pp =  54.77
    F0dd =  23.31
    F2dd =  13.89
    F4dd =  9.14
    F0pd =  33.03
    F2pd =  7.76

    G1pd =  6.42
    G3pd =  2.11
  end
  #--------------------
  
  
  #---Diagonal LFT-Matrix Elelemnts---
  #---All Values in eV---
  FUNCTIONS
    0   0 " 0.00"
    1   1 " 0.00"
    2   2 " 0.00"
    3   3 "1138.35"
    4   4 "1138.35"
    5   5 "1138.35"
    6   6 "1138.35"
    7   7 "1138.35"
  end
  #--------------------
  
  #---SOC-CONSTANTS---
  #---All Values in eV---
  PARAMETERS
    ZETA_P = 11.341 
    ZETA_D = 0.085 
  end   
  #--------------------
  
  #---SPECTRA/PROPERTIES---
  DoABS true
  Rel
    DoSOC true
  End
  #---------
end


*xyz 2 3
Ni 0.00 0.00 0.00
*
```

:::{admonition} 注意
:class: note
- 从 ORCA 6.1 起 orca_lft 已正确连接到 QDPT 驱动程序
- 这意味着所有 QDPT 性质 {ref}`sec:spectroscopyproperties.qdpt_magnetic_properties` 都可以在 Rel 块中请求
:::

第一步，定义所讨论的 LFT 问题：

```
------------------------------------------------------------------------------
                      L I G A N D    F I E L D    T H E O R Y
------------------------------------------------------------------------------


==============================================================================
                      LFT PARAMETERS DEFINITION BLOCK
==============================================================================


Number of electrons        = 14
Multiplicities             = 3 1 
Roots                      = 25 30 
Shells included            = 0 2 3 0 


----------------------------------------------------------
Definition of the ligand field basis set:
----------------------------------------------------------
   0  = pz     
   1  = px     
   2  = py     
   3  = dz2    
   4  = dxz    
   5  = dyz    
   6  = dx2y2  
   7  = dxy    


----------------------------------------------------------
Definition of the static ligand field by the user:
There are 11 ligand field parameters

----------------------------------------------------------
  Nr.               Name       Initial Value
  -----------------------------------------
    1               F0PP          85.880000
    2               F2PP          54.770000
    3               F0DD          23.310000
    4               F2DD          13.890000
    5               F4DD           9.140000
    6               F0PD          33.030000
    7               F2PD           7.760000
    8               G1PD           6.420000
    9               G3PD           2.110000
   10             ZETA_P          11.341000
   11             ZETA_D           0.085000


----------------------------------------------------------
Definition of the ligand field functions by the user:
There are 8 ligand field functions

----------------------------------------------------------
  Nr.      H-element         value   function
  ----------------------------------------------
 1   H(0,0)      0.000000000   0.00
 2   H(1,1)      0.000000000   0.00
 3   H(2,2)      0.000000000   0.00
 4   H(3,3)   1138.350000000  1138.35
 5   H(4,4)   1138.350000000  1138.35
 6   H(5,5)   1138.350000000  1138.35
 7   H(6,6)   1138.350000000  1138.35
 8   H(7,7)   1138.350000000  1138.35
```

然后，定义 CI 问题：

```
=> Defining the CI spaces and setting up the CI             ... 
==============================================================================
                             CI SETUP AND SOLUTION BLOCK
==============================================================================


Making Checks...
  Multiplicty =   3, #(configurations) =     28 #(CSF's) =     28 #(Roots) = 25 
  NRoots<NCSFs Adjussting  ==> (CSF's) =     25
Setting up CI...
  Multiplicty =   3, #(configurations) =     28 #(CSF's) =     25 #(Roots) = 25 
=============================================================================
                             CI SETUP AND SOLUTION BLOCK
=============================================================================


Making Checks...
  Multiplicty =   1, #(configurations) =     36 #(CSF's) =     36 #(Roots) = 30 
  NRoots<NCSFs Adjussting  ==> (CSF's) =     30
Setting up CI...
  Multiplicty =   1, #(configurations) =     36 #(CSF's) =     30 #(Roots) = 30 
CI setup done

```

然后，求解 CI 问题：

```
-----------------------------
 LFT-CI TRANSITION ENERGIES
------------------------------

LOWEST ROOT (ROOT 0, MULT 3) =    460.113216547 Eh 12520.317 eV

STATE ROOT MULT  DE/a.u.     DE/eV    DE/cm**-1
   1:   1    3   0.000000     0.000      0.0
   2:   2    3   0.000000     0.000      0.0
   3:   3    3   0.000000     0.000      0.0
   4:   5    3   0.000000     0.000      0.0
   5:   4    3   0.000000     0.000      0.0
   6:   6    3   0.000000     0.000      0.0
   7:   0    1   0.086266     2.347  18933.2
   8:   1    1   0.086266     2.347  18933.2
   9:   2    1   0.086266     2.347  18933.2
  10:   3    1   0.086266     2.347  18933.2
  11:   4    1   0.086266     2.347  18933.2
  12:   7    3   0.099001     2.694  21728.2
  13:   8    3   0.099001     2.694  21728.2
  14:   9    3   0.099001     2.694  21728.2
  15:   5    1   0.132624     3.609  29107.7
  16:   6    1   0.132624     3.609  29107.7
  17:   7    1   0.132624     3.609  29107.7
  18:   8    1   0.132624     3.609  29107.7
  19:   9    1   0.132624     3.609  29107.7
  20:  10    1   0.132624     3.609  29107.7
  21:  12    1   0.132624     3.609  29107.7
  22:  11    1   0.132624     3.609  29107.7
  23:  13    1   0.132624     3.609  29107.7
  24:  14    1   0.331652     9.025  72789.3
  25:  15    1  29.897078   813.541 6561650.2
  26:  16    1  29.897078   813.541 6561650.2
  27:  17    1  29.897078   813.541 6561650.2
  28:  18    1  29.897078   813.541 6561650.2
  29:  19    1  29.897078   813.541 6561650.2
  30:  10    3  29.915627   814.046 6565721.2
  31:  11    3  29.915627   814.046 6565721.2
  32:  13    3  29.915627   814.046 6565721.2
  33:  12    3  29.915627   814.046 6565721.2
  34:  14    3  29.915627   814.046 6565721.2
  35:  15    3  29.915627   814.046 6565721.2
  36:  16    3  29.915627   814.046 6565721.2
  37:  17    3  29.978158   815.747 6579445.1
  38:  18    3  29.978158   815.747 6579445.1
  39:  19    3  29.978158   815.747 6579445.1
  40:  20    3  29.978158   815.747 6579445.1
  41:  21    3  29.978158   815.747 6579445.1
  42:  22    3  30.016020   816.777 6587754.9
  43:  23    3  30.016020   816.777 6587754.9
  44:  24    3  30.016020   816.777 6587754.9
  45:  20    1  30.087356   818.719 6603411.3
  46:  21    1  30.087356   818.719 6603411.3
  47:  22    1  30.087356   818.719 6603411.3
  48:  23    1  30.106270   819.233 6607562.6
  49:  24    1  30.106270   819.233 6607562.6
  50:  25    1  30.106270   819.233 6607562.6
  51:  26    1  30.106270   819.233 6607562.6
  52:  27    1  30.106270   819.233 6607562.6
  53:  29    1  30.106270   819.233 6607562.6
  54:  28    1  30.106270   819.233 6607562.6
```

伴随着多重态分析：

```
---------------------------------------------------
Atomic calculation : Multiplet analysis (LFT)
---------------------------------------------------
11 multiplets found (Threshold = 0.01 eV)
  0 3F | E =     0.000 eV | 2p(6)3d(8) 
  1 3P | E =     2.694 eV | 2p(6)3d(8) 
  2 3F | E =   814.046 eV | 2p(5)3d(9) 
  3 3D | E =   815.747 eV | 2p(5)3d(9) 
  4 3P | E =   816.777 eV | 2p(5)3d(9) 
  5 1D | E =     2.347 eV | 2p(6)3d(8) 
  6 1G | E =     3.609 eV | 2p(6)3d(8) 
  7 1S | E =     9.025 eV | 2p(6)3d(8) 
  8 1D | E =   813.541 eV | 2p(5)3d(9) 
  9 1P | E =   818.719 eV | 2p(5)3d(9) 
 10 1F | E =   819.233 eV | 2p(5)3d(9) 
---------------------------------------------------
```

随后在 QDPT 框架中进行 SOC 计算：

```
*************************************
Doing QDPT with ONLY SOC!
*************************************

------------------------------------
NONZERO SOC MATRIX ELEMENTS (cm**-1)
------------------------------------

Bra                        Ket       
<Block Root S Ms  | HSOC | Block Root S  Ms>  =  Real-part     Imaginary part
-----------------------------------------------------------------------------
0    1  1.0  1.0           0     0  1.0  1.0       0.000           -685.571
0    3  1.0  1.0           0     2  1.0  1.0       0.000            342.781
0    4  1.0  1.0           0     2  1.0  1.0       0.000              0.134
0    4  1.0  1.0           0     3  1.0  1.0       0.000             -2.946
0    5  1.0  1.0           0     2  1.0  1.0       0.000              0.987
0    5  1.0  1.0           0     3  1.0  1.0       0.000              7.920
0    5  1.0  1.0           0     4  1.0  1.0       0.000          -1022.995
0    6  1.0  1.0           0     2  1.0  1.0       0.000             -3.379

...

1   29  0.0  0.0           0    17  1.0 -1.0   -2850.628           3039.103
1   29  0.0  0.0           0    18  1.0 -1.0   -16745.172           2885.219
1   29  0.0  0.0           0    19  1.0 -1.0   -1533.311           4672.283
1   29  0.0  0.0           0    20  1.0 -1.0     105.943            -43.140
1   29  0.0  0.0           0    21  1.0 -1.0      14.076             39.149

Note: In the following the full <I|HBO+SOC|J> are printed in the CI Basis.     
I,J are compound indices for |Block/Mult, Ms, Root>, where the states    
are ordered first by MultBlock, then Ms and finally Root.  

...
```

然后打印出 SOC 校正后的态：

```
The threshold for printing is 0.0010
Eigenvectors:
                         Weight      Real          Image    : Block Root    Spin   Ms
 STATE   0:       0.0000
                         0.014868    -0.121920     0.001813 :     0    0    1    1
                         0.158642     0.118778     0.380175 :     0    1    1    1
                         0.022316     0.003329     0.149347 :     0    2    1    1
                         0.073524    -0.037132     0.268598 :     0    3    1    1
                         0.071062    -0.251422     0.088592 :     0    4    1    1
                         0.068532    -0.250758     0.075180 :     0    5    1    1
                         0.010310     0.057750     0.083513 :     0    6    1    1
                         0.003333    -0.030103    -0.049264 :     0    0    1    0
                         0.007037     0.072029    -0.042999 :     0    1    1    0
                         0.245464     0.484256     0.104691 :     0    2    1    0
                         0.052920    -0.229815    -0.010229 :     0    3    1    0
                         0.017953     0.132002     0.022989 :     0    4    1    0
                         0.005423    -0.072174     0.014613 :     0    5    1    0
                         0.003723     0.024970     0.055669 :     0    6    1    0
                         0.018821     0.098122     0.095882 :     0    0    1   -1
                         0.081892    -0.206481     0.198135 :     0    1    1   -1
                         0.002458    -0.042784     0.025041 :     0    2    1   -1
                         0.057211    -0.099749     0.217397 :     0    3    1   -1
                         0.039565     0.098450     0.172838 :     0    4    1   -1
                         0.043388     0.182357     0.100666 :     0    5    1   -1
                         0.001044     0.019418     0.025827 :     0    6    1   -1
 STATE   1:       0.0000
                         0.042839    -0.206750    -0.009682 :     0    0    1    1
                         0.030129    -0.131357    -0.113467 :     0    1    1    1
                         0.004821    -0.067710    -0.015378 :     0    2    1    1
                         0.096567     0.259529     0.170915 :     0    3    1    1
                         0.019022    -0.134583    -0.030166 :     0    4    1    1
                         0.029125    -0.070877     0.155246 :     0    5    1    1
                         0.024443     0.150354     0.042856 :     0    6    1    1
                         0.126000    -0.140903    -0.325802 :     0    0    1    0
                         0.066620    -0.112104    -0.232493 :     0    1    1    0
                         0.034344    -0.075363    -0.169305 :     0    2    1    0
                         0.043496    -0.012839    -0.208161 :     0    3    1    0
                         0.035068    -0.017670     0.186428 :     0    4    1    0
                         0.088777    -0.019366    -0.297325 :     0    5    1    0
                         0.032394    -0.009435    -0.179735 :     0    6    1    0
                         0.033273    -0.179716    -0.031232 :     0    0    1   -1
                         0.038086    -0.175066     0.086245 :     0    1    1   -1
                         0.058972    -0.201976     0.134823 :     0    2    1   -1
                         0.091992     0.163866    -0.255226 :     0    3    1   -1
                         0.051908    -0.117870     0.194975 :     0    4    1   -1
                         0.015287    -0.106696    -0.062470 :     0    5    1   -1
                         0.036319     0.039383    -0.186462 :     0    6    1   -1
...
STATE 104: 6683223.2237
                         0.048335    -0.215907     0.041467 :     0   17    1    1
                         0.001350    -0.015566    -0.033287 :     0   18    1    1
                         0.058642    -0.018471    -0.241456 :     0   19    1    1
                         0.014743    -0.111453    -0.048181 :     0   20    1    1
                         0.019424    -0.128940     0.052904 :     0   21    1    1
                         0.013441    -0.042408    -0.107900 :     0   22    1    1
                         0.013136     0.106586    -0.042134 :     0   23    1    1
                         0.027360    -0.066625    -0.151399 :     0   24    1    1
                         0.030687     0.028711     0.172808 :     0   17    1    0
                         0.005134    -0.016659    -0.069691 :     0   18    1    0
                         0.006811    -0.016403    -0.080880 :     0   20    1    0
                         0.100510    -0.057415    -0.311791 :     0   21    1    0
                         0.054414    -0.044209    -0.229041 :     0   23    1    0
                         0.048345    -0.215766     0.042306 :     0   17    1   -1
                         0.001057    -0.001549     0.032472 :     0   18    1   -1
                         0.060316     0.071066     0.235085 :     0   19    1   -1
                         0.015880    -0.093356     0.084643 :     0   20    1   -1
                         0.019274    -0.138702    -0.005996 :     0   21    1   -1
                         0.013436    -0.004756     0.115817 :     0   22    1   -1
                         0.013139     0.114517     0.004987 :     0   23    1   -1
                         0.026471    -0.005403     0.162611 :     0   24    1   -1
                         0.050526     0.219718    -0.047434 :     1   20    0    0
                         0.293497    -0.532819     0.097985 :     1   21    0    0
                         0.064015     0.249661    -0.041039 :     1   22    0    0
```

然后，给出 SOC 校正后的吸收（此处为 XAS）光谱：

```
--------------------------------------------------------------------------------------------------------
      SOC CORRECTED ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS    
--------------------------------------------------------------------------------------------------------
      Transition         Energy     Energy  Wavelength fosc(D2)      D2       |DX|      |DY|      |DZ|  
                          (eV)      (cm-1)    (nm)  (*population)  (au**2)    (au)      (au)      (au)  
--------------------------------------------------------------------------------------------------------
  1-3.0A  ->  2-3.0A    0.000000       0.0     0.0   0.000000000   0.00000   0.00000   0.00000   0.00000
  0-3.0A  ->  1-3.0A    0.000000       0.0     0.0   0.000000000   0.00000   0.00000   0.00000   0.00000
  0-3.0A  ->  2-3.0A    0.000000       0.0     0.0   0.000000000   0.00000   0.00000   0.00000   0.00000
  1-3.0A  ->  3-3.0A    0.000000       0.0     0.0   0.000000000   0.00000   0.00000   0.00000   0.00000
  2-3.0A  ->  3-3.0A    0.000000       0.0     0.0   0.000000000   0.00000   0.00000   0.00000   0.00000
  0-3.0A  ->  3-3.0A    0.000000       0.0     0.0   0.000000000   0.00000   0.00000   0.00000   0.00000
  1-3.0A  ->  4-3.0A    0.000000       0.0     0.0   0.000000000   0.00000   0.00000   0.00000   0.00000
  2-3.0A  ->  4-3.0A    0.000000       0.0     0.0   0.000000000   0.00000   0.00000   0.00000   0.00000
  2-3.0A  ->  5-3.0A    0.000000       0.0     0.0   0.000000000   0.00000   0.00000   0.00000   0.00000
  2-3.0A  ->  6-3.0A    0.000000       0.0     0.0   0.000000000   0.00000   0.00000   0.00000   0.00000
  0-3.0A  ->  4-3.0A    0.000000       0.0     0.0   0.000000000   0.00000   0.00000   0.00000   0.00000
  1-3.0A  ->  7-3.0A    0.000000       0.0     0.0   0.000000000   0.00000   0.00000   0.00000   0.00000
  1-3.0A  ->  6-3.0A    0.000000       0.0     0.0   0.000000000   0.00000   0.00000   0.00000   0.00000
  2-3.0A  ->  7-3.0A    0.000000       0.0     0.0   0.000000000   0.00000   0.00000   0.00000   0.00000
  1-3.0A  ->  5-3.0A    0.000000       0.0     0.0   0.000000000   0.00000   0.00000   0.00000   0.00000
  0-3.0A  ->  6-3.0A    0.000000       0.0     0.0   0.000000000   0.00000   0.00000   0.00000   0.00000
  0-3.0A  ->  7-3.0A    0.000000       0.0     0.0   0.000000000   0.00000   0.00000   0.00000   0.00000
  0-3.0A  ->  5-3.0A    0.000000       0.0     0.0   0.000000000   0.00000   0.00000   0.00000   0.00000
  1-3.0A  ->  8-3.0A    0.000000       0.0     0.0   0.000000000   0.00000   0.00000   0.00000   0.00000
  2-3.0A  ->  8-3.0A    0.000000       0.0     0.0   0.000000000   0.00000   0.00000   0.00000   0.00000
  0-3.0A  ->  8-3.0A    0.000000       0.0     0.0   0.000000000   0.00000   0.00000   0.00000   0.00000
  2-3.0A  ->  9-3.0A    0.171933    1386.7  7211.2   0.000000000   0.00000   0.00000   0.00000   0.00000
  1-3.0A  ->  9-3.0A    0.171933    1386.7  7211.2   0.000000000   0.00000   0.00000   0.00000   0.00000
  0-3.0A  ->  9-3.0A    0.171933    1386.7  7211.2   0.000000000   0.00000   0.00000   0.00000   0.00000
  1-3.0A  -> 10-3.0A    0.171933    1386.7  7211.2   0.000000000   0.00000   0.00000   0.00000   0.00000
  2-3.0A  -> 10-3.0A    0.171933    1386.7  7211.2   0.000000000   0.00000   0.00000   0.00000   0.00000
  0-3.0A  -> 10-3.0A    0.171933    1386.7  7211.2   0.000000000   0.00000   0.00000   0.00000   0.0

...

2-3.0A  -> 45-3.0A   808.419525 6520343.9     1.5   0.001132627   0.00052   0.01199   0.00520   0.01856
1-3.0A  -> 45-3.0A   808.419525 6520343.9     1.5   0.000466250   0.00021   0.00950   0.00818   0.00742
0-3.0A  -> 45-3.0A   808.419525 6520343.9     1.5   0.001659029   0.00075   0.01729   0.00696   0.02018
2-3.0A  -> 46-3.0A   808.419525 6520343.9     1.5   0.001163057   0.00053   0.01282   0.00222   0.01896
1-3.0A  -> 46-3.0A   808.419525 6520343.9     1.5   0.000718139   0.00033   0.00902   0.01359   0.00780
0-3.0A  -> 46-3.0A   808.419525 6520343.9     1.5   0.000710800   0.00032   0.01397   0.01112   0.00211
2-3.0A  -> 47-3.0A   808.419525 6520343.9     1.5   0.002893681   0.00132   0.02588   0.01640   0.01943
1-3.0A  -> 47-3.0A   808.419525 6520343.9     1.5   0.001285542   0.00058   0.02045   0.00869   0.00955
2-3.0A  -> 48-3.0A   808.419525 6520343.9     1.5   0.000921831   0.00042   0.00885   0.01380   0.01228
```

像往常一样用 orca_mapspc {ref}`sec:utilities.mapspc` 处理 `*.out` 文件，生成 \*.dat 和 \*.stk 文件。用这些文件绘制的 XAS 光谱
如 {numref}`fig:LFT_XAS` 所示。

(fig:LFT_XAS)=
```{figure} ../../images/Ni_L_edge_LFT_XAS.*

orca_lft 模拟的镍原子 $Ni^{2+}$ L 边 XAS 光谱（红色）以及
存在 Oh 场时镍原子的 XAS 光谱
```

orca_lft 的强大之处在于它完全可参数化。
这种灵活性通过 PARAMETERS 和 FUNCTIONS 子块的内在能力实现
- **参数可扫描性**
任何给定参数——例如 D 壳层的 `ZETA_D` 自旋-轨道耦合（SOC）常数——可以：
- *开启/关闭*：`ZETA_D= 0.0`
- *在参数范围内扫描*：`ZETA_D= 0.0, 0.1, 11`，即在 0.0-0.1 eV 范围内取 11 步。
- **新参数的定义**
- *用户可以在 PARAMETERS 子块内定义任意数量或类型的自定义参数*：例如 `10Dq= 1.2`
- **PARAMETERS 和 FUNCTIONS 子块中的代数关系**
- *PARAMETERS 子块中的代数关系*：
```orca
`DOh = 1.2`
`D1 = {-0.4*DOh}`
`D2 = {0.6*DOh}`
```
- *FUNCTIONS 子块中的代数关系*：
```orca
`3   3 "1138.35 + D2" # => dz2`
`4   4 "1138.35 + D1" # => dxz`
```

这提供了必要的灵活性，可以设置针对特定实验化学问题量身定制的任意参数化配体场理论（LFT）模型。

作为示例，让我们重新审视上面讨论的镍配合物，并引入 d 轨道壳层的重心八面体配体场分裂 10Dq=1.2 eV。

输入现在为：

```orca
%lft


  #-----Parameters------
  NEl= 14
  LFTCase 2p3d
  Mult= 3, 1
  NRoots= 25, 30
  #--------------------


  #---Slater-Condon Parameters---
  #---All Values in eV---
  PARAMETERS
    F0pp =  85.88
    F2pp =  54.77
    F0dd =  23.31
    F2dd =  13.89
    F4dd =  9.14
    F0pd =  33.03
    F2pd =  7.76
    G1pd =  6.42

    G1pd =  6.42
    G3pd =  2.11
    DOh = 1.2
    D1 = {-0.4*DOh}
    D2 = {0.6*DOh}
  end
  #--------------------


  #---Diagonal LFT-Matrix Elelemnts---
  #---All Values in eV---
  FUNCTIONS
    0   0 " 0.00"
    1   1 " 0.00"
    2   2 " 0.00"
    3   3 "1138.35 + D2" # => dz2
    4   4 "1138.35 + D1" # => dxz
    5   5 "1138.35 + D1" # => dyz
    6   6 "1138.35 + D2" # => dx2-y2
    7   7 "1138.35 + D1" # => dxy
  end
  #--------------------

  #---SOC-CONSTANTS---
  #---All Values in eV---
  PARAMETERS
    ZETA_P = 11.341
    ZETA_D = 0.085
  end
  #--------------------

  #---SPECTRA/PROPERTIES---
  DoABS true
  Rel
    DoSOC true
  End
  #---------
End

*xyz 2 3
Ni 0.00 0.00 0.00
*
```

运行上述输入可以看到新参数 `DOH`、`D1` 和 `D2` 已成功定义：

```orca
----------------------------------------------------------
Definition of the ligand field basis set:
----------------------------------------------------------
   0  = pz     
   1  = px     
   2  = py     
   3  = dz2    
   4  = dxz    
   5  = dyz    
   6  = dx2y2  
   7  = dxy    


----------------------------------------------------------
Definition of the static ligand field by the user:
There are 14 ligand field parameters

----------------------------------------------------------
  Nr.               Name       Initial Value
  -----------------------------------------
    1               F0PP          85.880000
    2               F2PP          54.770000
    3               F0DD          23.310000
    4               F2DD          13.890000
    5               F4DD           9.140000
    6               F0PD          33.030000
    7               F2PD           7.760000
    8               G1PD           6.420000
    9               G3PD           2.110000
   10                DOH           1.200000
   11                 D1          -0.480000
   12                 D2           0.720000
   13             ZETA_P          11.341000
   14             ZETA_D           0.085000
```
并且 Oh LFT 分裂在单电子 LFT 矩阵中被考虑为：

```orca
----------------------------------------------------------
Definition of the ligand field functions by the user:
There are 8 ligand field functions

----------------------------------------------------------
  Nr.      H-element         value   function
  ----------------------------------------------
 1   H(0,0)      0.000000000   0.00
 2   H(1,1)      0.000000000   0.00
 3   H(2,2)      0.000000000   0.00
 4   H(3,3)   1139.070000000  1138.35 + D2
 5   H(4,4)   1137.870000000  1138.35 + D1
 6   H(5,5)   1137.870000000  1138.35 + D1
 7   H(6,6)   1139.070000000  1138.35 + D2
 8   H(7,7)   1137.870000000  1138.35 + D1


=> Defining the one-electron LFT matrix                     ... done
----------------------------------------------------------
The ligand field one electron eigenfunctions:
----------------------------------------------------------
Orbital    Energy (eV) Energy(cm-1)          pz         px         py         dz2        dxz        dyz       dx2-y2       dxz
    1          0.000        0.0           1.000000   0.000000   0.000000   0.000000   0.000000   0.000000   0.000000   0.000000
    2          0.000        0.0           0.000000   1.000000   0.000000   0.000000   0.000000   0.000000   0.000000   0.000000
    3          0.000        0.0           0.000000   0.000000   1.000000   0.000000   0.000000   0.000000   0.000000   0.000000
    4       1137.870  9177541.4           0.000000   0.000000   0.000000   0.000000   1.000000   0.000000   0.000000   0.000000
    5       1137.870  9177541.4           0.000000   0.000000   0.000000   0.000000   0.000000   1.000000   0.000000   0.000000
    6       1137.870  9177541.4           0.000000   0.000000   0.000000   0.000000   0.000000   0.000000   0.000000   1.000000
    7       1139.070  9187220.1           0.000000   0.000000   0.000000   0.000000   0.000000   0.000000   1.000000   0.000000
    8       1139.070  9187220.1           0.000000   0.000000   0.000000   1.000000   0.000000   0.000000   0.000000   0.000000
```

成功终止后，可以处理 Ni L 边 XAS 光谱并绘制所得数据，如 {numref}`fig:LFT_XAS`（蓝线）所示，
它确实再现了例如 $Ni(H_{2}O)_6$ 的 Ni L 边 XAS 光谱的特征。

:::{admonition} 注意
:class: note
- 详细教程将很快推出，进一步探索 orca_lft 的能力
:::

(sec:utilities.crystalprep)=
## orca_crystalprep

ORCA 提供实用程序 `orca_crystalprep`，可以处理
晶体学 `.cif` 文件或 `.xyz` 超胞文件，并为嵌入簇计算生成
正确的输入。

要进行常规的或 Ionic-Crystal-QMMM 中的嵌入簇计算，基本上需要定义 3 个区域：

1.  将被量子力学处理的量子簇（QC）。

2.  表示固体环境的点电荷区域（PC）。

3.  位于 QC 和 PC 之间、主要作用是防止 QC
    和 PC 区域之间电荷传递的边界区域（BR）或 ECP。

这意味着第一步必须生成超胞（.xyz），
并按计算设计分离不同区域。
第二步必须平衡体系的电荷。
最后，所有这些需要组合成正确的计算
输入。

这显然是一个多步骤、常常跨平台的过程，

1.  复杂，

2.  耗时，

3.  对用户不友好。

`orca_crystalprep` 实用程序旨在自动生成
ORCA 嵌入簇计算的正确输入，目标是
让广大有经验和无经验的用户都能
以最小的工作量设置嵌入簇计算。

`orca_crystalprep` 需要自己的输入。只需从终端执行它：

```orca
orca_crystalprep
```

即可获得用法打印

```
**********************************************************************
Generate initial ORCA CrystalPrep Input
**********************************************************************

======================================================================
Usage: orca_crystalprep [Basename Input] [options]
======================================================================

----------------------------------------------------------------------
[Options]:
----------------------------------------------------------------------
-geninput                     Generate Initial Input
----------------------------------------------------------------------

**********************************************************************
Generate ORCA Embedding Cluster Inputs using the CrystalPrep Utility
**********************************************************************

======================================================================
Usage: orca_crystalprep [CrystalPrep Input]
======================================================================
```

以及不同选项：

```
------------------------------------------------------------------------------------------------------------
[CrystalPrep Input Options]:
-------------------------------------------------------------------------------------------------------------
General Definitions
-------------------------------------------------------------------------------------------------------------
DoCIF                       true                     This will process a .cif file                         
DoXYZ                       true                     This will process a .xyz file                         
InputCIF                    "CIFFileName"            Set the name of the CIFFileName                     
InputXYZ                    "XYZFileName"            Set the name of the XYZFileName                     
-------------------------------------------------------------------------------------------------------------
SuperCell Construction Definitions
-------------------------------------------------------------------------------------------------------------
DoSuperCell                 true                     Flag to generate a SuperCell                          
SCDimension                 "axbxc"                  The Dimension of the SuperCell (e.g. "1x1x1")     
InputCIF                    "CIFFileName"            Set the name of the CIFFileName                     
InputXYZ                    "XYZFileName"            Set the name of the XYZFileName                     
-------------------------------------------------------------------------------------------------------------
Special Tasks on SuperCells
-------------------------------------------------------------------------------------------------------------
DoFractional                 true                    Flag to Transform Cartesian to Fractional coordinates   
DoSymmetryOperations         true                    Flag to enforce using built in Symmetry Operations      
DoHemiSphereSC               true                    Flag to request a Hemisphere Super Cell build           
DoSymetricSC                 true/false              Flag to request a Symmetric Super Cell build            
                             false => Origin Build    :  0 - ra,   0 - rb,   0 - rc  => Default for Now!                     
                             true  => Symmetric Build :  -ra - ra, -rb - rb, -rc - rc                                         
-------------------------------------------------------------------------------------------------------------
Embedding Cluster Definitions
-------------------------------------------------------------------------------------------------------------
DoEmbedding                  true                    Flag to generate the files for the embedding approach   
UseVolumeCriterion           true                    Volume Criterion to generate layers                     
UseDistanceCriterion         true                    Distance Criterion to generate layers                   
CellVolumeFraction           value                   Cell(UniCell/SuperCell) fraction (default 1.0)          
DoMolecularFragments         value                   Define Molecular Fragments during the build             
DoSimpleInput                true                    Flag to generate a conventional Embedding Cluster input 
DoICQMMMInput                true                    Flag to generate a Ionic-Crystal-QMMM input             
DoMCQMMMInput                true                    Flag to generate a Mol-Crystal-QMMM input               
WritePDB                     true                    Flag to run a Ionic-Crystal-QMMM input from a PDF file  
QCCharge                     Charge Number           Specify the total QC Charge                             
QCMult                       Multiplicity Number     Specify the total Multiplicity                          
-------------------------------------------------------------------------------------------------------------
Special Tasks on Embedding Cluster Construction/Definition
-------------------------------------------------------------------------------------------------------------
DoLayers                     true                    Request Layers Definition                               
1) Layers Definition. There are 2 Options:                                                                   
             a) The Differnt regions are build in layers as multipoles of the UnitCell                       
             b) The Differnt regions are build in layers around a predefined QC cluster via a QCAtom List    
QCLayers                     QC Layers Number        Specify the number of the QC Layers                     
ECPLayers                    ECP Layers Number       Specify the number of the ECP Layers                     
PCLayers                     PC Layers Number        Specify the number of the PC Layers                     
HFLayers                     HF Layers Number        Specify the number of the HF Layers                     
Example Input
QCLayers 1 
2) Atoms Definition. This is alternative to Layers Definition (e.g. DoLayers false)                          
NQCAtoms                     QC Atoms  Number        Specify the number of the QC Atoms                      
NHFAtoms                     HF Atoms  Number        Specify the number of the HF Atoms                      
NECPAtoms                    ECP Atoms  Number       Specify the number of the ECP Atoms                     
NPCAtoms                     PC Atoms  Number        Specify the number of the PC Atoms                      
QCAtoms                      QC Atoms  List          Specify the List   of the QC Atoms (e.g. 0,1,4,10...    
HFAtoms                      HF Atoms  List          Specify the List   of the HF Atoms (e.g. 0,1,4,10...    
ECPAtoms                     ECP Atoms  List         Specify the List   of the ECP Atoms (e.g. 0,1,4,10...   
PCAtoms                      PC Atoms  List          Specify the List   of the PC Atoms (e.g. 0,1,4,10...    
Example Input
NQAtoms= 4 
QCAtoms 0,1,4,10 
-------------------------------------------------------------------------------------------------------------
Request an Explicit Atom Definion in Ionic-Crystal-QMMM 
HINT: This is automatically Set to true if an Atom List (QC Atoms, ECP Atoms, ...) is provided by the user
-------------------------------------------------------------------------------------------------------------
SetQCAtoms                   true                    Set explicitely the QC Atoms                            
SetHFAtoms                   true                    Set explicitely the HF Atoms                            
SetECPAtoms                  true                    Set explicitely the ECP Atoms                           
SetPCAtoms                   true                    Set explicitely the PC Atoms                            
SetPC2Atoms                  true                    Set explicitely the PC2 Atoms                           
-------------------------------------------------------------------------------------------------------------
Load a User Defined QC Cluster
-------------------------------------------------------------------------------------------------------------
LoadQCCluster                true                    Load the QC Cluster                                     
InputXYZ                   "QCXYZFileName"         Set the name of the QC XYZFileName                      
-------------------------------------------------------------------------------------------------------------
NOTE: This ALWAYS requires to build symmetric Super Cells. Hence DoSymetricSC turns on by default!           
-------------------------------------------------------------------------------------------------------------
STEPS:                                                                                                       
      1) Build a minimal (1x1x1 or 2x2x2) and define the QC cluster that is saved as QCXYZFileName           
      2) Build the actual SuperCell (e.g. 10x10x10) by Loading the QC cluster                                
         and define the QC cluster that is saved as QCXYZFileName                                            
      3) Build the Embedded Cluster around the Loaded QC employin the Layers scheme                          
-------------------------------------------------------------------------------------------------------------
Redefine SuperCell Origin. This is for shifting the center origin to a desired atom during the SC Construction  
This Helps to automatically construct desired Cluster structures using the Layers Definition 
-------------------------------------------------------------------------------------------------------------
ShiftOrigin                  true                    Request Origin Shift  to a particular Atom              
ChosenAtom                   an Atom Number          The Number of the Chosen atom (e.g. 2)                  
-------------------------------------------------------------------------------------------------------------
Neutralize the Embedded Cluster in the Simple Input
Note that in the Ionic-Crustal QMMM Input this step is taken care on demand during the QM/MM run
-------------------------------------------------------------------------------------------------------------
ChargePoints                the charge points        Specify the number of the charge points (default 1000)  
ChargeStep                  the charge points        Define the step during the iterations (default 0.01)    
ChargeThres                 the threshold            Define the neutralization threshold (default 0.01)      
Neutralization Schemes:                                                                                      
NeutralizingScheme1         true                 ->  Neutralization is based on All Charges                  
NeutralizingScheme2         true                 ->  Neutralization is based on different charges            
                                                     Equiping the ECP and PC regions                         
NeutralizingScheme3         true                 ->  Neutralization is based on PC2 Region                   
-------------------------------------------------------------------------------------------------------------
Special Definitions for the .metainfo File in the Ionic-Crustal QMMM
This helps Setting Charge/Spin in a specific atom type
It can also aid the neutralization step of the Embedded Cluster in the Simple Input 
-------------------------------------------------------------------------------------------------------------
NAtomTypes                  Number of Atom Types     Specify The Atom types that will be defined             
Example Input
#-------------------------
#Atom Type Charge Spin
#-------------------------
AtomTypes 2
Co    1    2.0   1.5
Co    2    3.0   0
end
This specifies the local Spin and Charge of a Td HS Co2+ center (Type 1) and a OH Co3+ center (Type 2)
During the Embedding cluster construction
-------------------------------------------------------------------------------------------------------------
```

第一步，可以使用 `orca_crystalprep` 工具通过运行下列命令生成其自身输入：

```orca
orca_crystalprep crystalprep.inp -geninput
```

这将生成初始输入：

```
---------------------------------------------------------------------------------
Initial Input: crystalprep.inp for Orca_CrystalPrep has been generated. All Done! 
---------------------------------------------------------------------------------
```

它如下所示：

```orca
%crystalprep


#************************
#Read CIF/XYZ
#************************
DoCIF true  

#------------------------
#INPUT CIF/XYZ
#------------------------
#InputCIF "CIFName.cif"
#------------------------
#Set Special Tasks
#------------------------
#SpaceGroupNumber 200

#************************
#Generate SuperCell      
#************************
DoSuperCell true
SCDimension "1x1x1"

#************************
#Setup Embedding Approach
#************************
DoEmbedding true
DoLayers true

#------------------------
#Atom Type Charge Spin
#------------------------
#NAtomTypes 2
#Co 1 2.0  1.5
#Co 2 3.0  0.0

#************************
#Generate Inputs
#************************
#DoSimpleInput true
#DoICQMMMInput true

#Neutralize true
#QCCharge 0
#QCMult 1
#------------------------
end
```

如 {numref}`fig:CrystalPrep_ICQMMM` 所示，通过指定所需的
`*.cif` 或 `*.xyz` 文件名以及相应选项，即可生成可直接运行的
嵌入簇输入。

(fig:CrystalPrep_ICQMMM)=
```{figure} ../../images/CrystalPrep_ICQMMM.*

嵌入簇 IC-QM/MM 输入的生成
```

默认情况下，嵌入簇结构采用基于层的方法构建，
其中不同的结构层以晶胞的倍数或分数生成。

晶胞分数以体积单位表示，用下列关键词指定：

```orca
CellVolumeFraction N #by default N=1
```

作为示例，让我们详细考虑 NaCl 的情况。我们的目标是生成完整的嵌入簇设置，包括：

1.  由 nacl.cif 文件构建的 20x20x20 超胞，

2.  含 1 个 QC 层和 1 个 ECP 层的嵌入簇，以及

3.  IC-QM/MM 嵌入簇输入

这些可以通过下列 ORCA 输入文件通过 `%crystalprep` 块调用 `orca_crystalprep` 程序来准备：

```orca
%crystalprep


#************************
#Read CIF/XYZ
#************************
DoCIF true

#------------------------
#INPUT CIF/XYZ
#------------------------
InputCIF "nacl.cif"

#************************
#Generate SuperCell
#************************
DoSuperCell true
SCDimension "20x20x20"

#************************
#Setup Embedding Approach
#************************
DoEmbedding true
DoLayers true

#------------------------
#Atom Type Charge Spin
#------------------------
NAtomTypes 2
Na 0  1.0  0.0
Cl 1 -1.0  0.0

#************************
#Generate Inputs
#************************
DoICQMMMInput true
QCCharge 0
QCMult 1  
#------------------------
end

end
```

第一步，`the orca_crystalprep` 处理 nacl.cif 文件并创建晶胞和请求的 20x20x20 超胞：

```
-------------------------------------------------------------
Reading Information from the provided CIF file: nacl.cif
-------------------------------------------------------------

------------------------Unit Cell Parameters-----------------
Hermann-Mauguin Space Group:     P1
Space Group ID:                1
Unit Cell Symmetry:                
Unit Cell Volume:             46.09
Unit Cell alpha angle:        60.00
Unit Cell beta angle:         60.00
Unit Cell gamma angle:        60.00
Unit Cell alpha length:       4.024
Unit Cell beta length:        4.024
Unit Cell gamma length:       4.024
Atom   Type   AO    x     y     z    occ
Na     0     11 0.000 0.000 0.000  1.00
Cl     1     17 0.500 0.500 0.500  1.00
Done
-------------------------------------------------------------

----------Making a SuperCell with 20x20x20 dimensions-----------
Unit Cell:
0          1          2    
0       4.024000   0.000000   0.000000
1       0.000000   4.024000   0.000000
2       0.000000   0.000000   4.024000

Transformation Matrix:
0          1          2    
0      80.480000   0.000000   0.000000
1       0.000000  80.480000   0.000000
2       0.000000   0.000000  80.480000


---------------------------------------------------------------------
Saving xyz file: nacl4.cif_20x20x20.xyz                   ...Done
---------------------------------------------------------------------
```

然后，开始构建嵌入簇结构：

```
------------Making a Embedding Cluster Input ------------
------------Using the Layers Approach with: ------------
QC_Layers: 1
ECP_Layers: 1
PC_Layers: 1
--------------
Preparing Inputs ...
```

下一步，超胞（`.xyz`）的中心被指派到离中心最近的原子：

```
-------------------------------
The Center of XYZ Coordinates
-------------------------------
41.246, 41.246, 41.246
-------------------------------
Closest Atom to Center
-------------------------------
Na(4630) 40.240, 40.240, 40.240
-------------------------------
Shifting Origin to closest atom
-------------------------------
40.240, 40.240, 40.240
```

之后，自动生成各层：

```
--------------------------------------
Saving Generated Layers XYZ Files ...
--------------------------------------
Saving Layer 0 XYZ File: nacl.cif_20x20x20.xyz_0.xyz
Saving Layer 1 XYZ File: nacl.cif_20x20x20.xyz_1.xyz
Saving Layer 2 XYZ File: nacl.cif_20x20x20.xyz_2.xyz
Saving Layer 3 XYZ File: nacl.cif_20x20x20.xyz_3.xyz
Saving Layer 4 XYZ File: nacl.cif_20x20x20.xyz_4.xyz
Saving Layer 5 XYZ File: nacl.cif_20x20x20.xyz_5.xyz
Saving Layer 6 XYZ File: nacl.cif_20x20x20.xyz_6.xyz
Saving Layer 7 XYZ File: nacl.cif_20x20x20.xyz_7.xyz
Saving Layer 8 XYZ File: nacl.cif_20x20x20.xyz_8.xyz
Saving Layer 9 XYZ File: nacl.cif_20x20x20.xyz_9.xyz

--------------------------------------
Saving Generated Layers PDB File ...
--------------------------------------
```

随后是嵌入簇构建：

```
--------------------------------------
Saving Generated Cluster XYZ Files ...
--------------------------------------
Saving QC XYZ File: nacl.cif_20x20x20.xyz_QC.xyz
Saving ECP Region XYZ File: nacl.cif_20x20x20.xyz_ECP.xyz
Saving PC Region XYZ File: nacl.cif_20x20x20.xyz_PC.xyz
```

最后，生成 IC-QM/MM 嵌入簇：

```
--------------------------------------
Saving Embedding Cluster Inputs ...
--------------------------------------
Saving ICQMMM Input: nacl.cif_20x20x20.xyz.ICQMMM.inp
Done
--------------------------------------------------------------
```

离子晶体 QM/MM 计算需要生成简单力场，
它存储在 `*.prms` 文件中，如章节
{ref}`sec:multiscalesimulations.qmmm.orca` 中所述。
必要信息（包括电荷和自旋）取自 `.metainfo` 文件。
`orca_crystalprep` 工具允许在 `.metainfo` 文件中外部设置电荷和自旋，
如下所述：

首先，在处理 .cif 文件期间，为不对称单元中检测到的所有原子指派原子类型。

```
Atom   Type   AO    x     y     z    occ
Na     0     11 0.000 0.000 0.000  1.00
Cl     1     17 0.500 0.500 0.500  1.00
```

在 `orca_crystalprep` 输入中，特定原子类型的电荷和自旋可按如下方式指派：

```orca
NAtomTypes 2
Na 0  1.0  0.0
Cl 1 -1.0  0.0
```

然后这些信息传递到 `.metainfo` 文件中

```orca
18522 
# atom nr. - element - atom type - formal charge - formal spin - molecule nr
0  Na   0  1  0           1
1  Na   0  1  0           1
2  Na   0  1  0           1
...

9261  Cl   1 -1  0        1
9262  Cl   1 -1  0        1
9263  Cl   1 -1  0        1
...
```

完成准备步骤后，嵌入簇如 {numref}`fig:Embedded_Cluster` 所示构建。

(fig:Embedded_Cluster)=
```{figure} ../../images/Embedded_Cluster.*

生成的嵌入簇。QC：${Na_4}{Cl_4}$，ECP 区域红点，
PC 区域小绿点和紫点
```

用于运行 IC-QM/MM 嵌入簇计算的生成输入如下：

```orca
!Ionic-Crystal-QMMM
#Include Method
```

```orca
%qmmm
#--------Define the Cluster---------
ORCAFFFilename= ""
Use_QM_InfoFromPDB true
Use_QM3_InfoFromPDB true
ECPLayerECP= "SDD"
#--------Charge Convergence---------
CONV_Charges false
ENFORCETOTALCHARGE true
CHARGE_TOTAL    0
PrintLevel 4
end
#-----------------------------------

*pdbfile 0  1 nacl.cif_20x20x20.pdb
```

从 ORCA 6.1 起，orca_crystalprep 实用程序在以下方面扩展了其能力：

- **处理各种各样的 .cif 文件**

原则上任何类型的 .cif 文件都可以处理，以创建从分子到固体的任何化学体系的各种超胞，
涵盖大量结构复杂性和空间群对称性，如图 {numref}`fig:SuperCells_CrystalPrep` 所示。值得注意的是
晶体学信息文件（.cif）的结构自国际晶体学联合会（IUCr）引入以来经历了相当大的演变。在较早的 .cif 文件中——尤其是在 CIF 核心字典标准化之前生成的那些——头部
部分常常不一致，缺少诸如 _symmetry_space_group_name_H-M、_cell_length_a 或 _atom_site_label 等标准化数据项。
取而代之的是经常使用自定义或缩写记法，而必要的元数据（例如单位、对称操作或出版物引用）
常常不完整或完全省略。相比之下，符合 IUCr Core CIF 和 mmCIF 字典的现代 .cif 文件遵循严格
定义的语法，并包含支持互操作性、可重复性和自动化处理的广泛元数据。这些增强包括
显式的数据块命名约定、原子位置的层次化循环结构，以及通过 _space_group_symop_operation_xyz 等条目
明确定义的对称操作。鉴于这种差异，当代 .cif 解析器的设计必须具有足够的灵活性
以适应结构异质性，同时确保准确提取固有的晶体学信息。这包括对国际晶体学表所定义的全部 230 个晶体学空间群及其相应
子群的对称操作和晶格参数的正确识别和解释。这种稳健性对于实现可靠的对称分析、
结构精修以及晶体学和材料科学中的高通量计算工作流至关重要。在此背景下 Orca_crystalprep 包含
自己的对称操作库，它将尝试修复 .cif 文件中包含的任何潜在缺陷。如果未检测到对称操作则自动激活，
或者也可以通过关键词 `SymmetryOperations true` 请求



例如对 CeO2，用于生成球形超胞的 orca_crystalprep 输入文件
将如下所示


(fig:SuperCells_CrystalPrep)=
```{figure} ../../images/SuperCells_CrystalPrep.*

使用 orca_crystalprep 实用程序生成的各种超胞

```

```orca
%crystalprep


#************************
#Read CIF/XYZ
#************************
DoCIF true                #Turn on the cif file reading

#------------------------
#INPUT CIF/XYZa
#------------------------
InputCIF "CeO2.cif"       #The cif file 
#------------------------
#Set Special Tasks
#------------------------

#************************
#Generate SuperCell
#************************
DoSuperCell true           #Turn on the supecell construction
SCDimension "10x10x10"     #Construct a 10x10x10 supercell
DoSymetricSC true          #Construct symmetric supercell 
DoSymmetryOperations true  #Use the buildin Crystallographic database
DoHemiSphereSC true/false  #Build the supecell in cubic or hemisphere fashion
PrintLevel 2
#************************
#Setup Embedding Approach
#************************
DoEmbedding false          #Turn off the Embended Cluster generation
```

运行这将处理 .cif 文件

```orca
*************** ORCA CRYSTALPREP TOOL ************

-------------------------------------------------------------
Reading Information from the provided CIF file: CeO2.cif
-------------------------------------------------------------

------------------------Unit Cell Parameters-----------------
Hermann-Mauguin Space Group:     P1
Space Group ID:                1
Unit Cell Symmetry:                
Unit Cell Volume:            163.40
Unit Cell alpha angle:        90.00
Unit Cell beta angle:         90.00
Unit Cell gamma angle:        90.00
Unit Cell alpha length:       5.467
Unit Cell beta length:        5.467
Unit Cell gamma length:       5.467
Atom   Type  AO    x     y     z    occ   ox
 Ce     0    58 0.000 0.000 0.000  1.00  4.00
 Ce     1    58 0.000 0.500 0.500  1.00  4.00
 Ce     2    58 0.500 0.000 0.500  1.00  4.00
 Ce     3    58 0.500 0.500 0.000  1.00  4.00
 O      4     8 0.250 0.750 0.750  1.00 -2.00
 O      5     8 0.750 0.250 0.250  1.00 -2.00
 O      6     8 0.250 0.250 0.250  1.00 -2.00
 O      7     8 0.750 0.750 0.750  1.00 -2.00
 O      8     8 0.750 0.750 0.250  1.00 -2.00
 O      9     8 0.250 0.250 0.750  1.00 -2.00
 O     10     8 0.750 0.250 0.750  1.00 -2.00
 O     11     8 0.250 0.750 0.250  1.00 -2.00
Done
-------------------------------------------------------------

----------Making a SuperCell with 10x10x10 dimensions-----------
Doing Symmetry Operations ...
Detected   1 Operations for 
Hermann-Mauguin Space Group:     P1
Space Group ID:                  1
Done
Unit Cell:
                  0          1          2    
      0       5.467000   0.000000   0.000000
      1       0.000000   5.467000   0.000000
      2       0.000000   0.000000   5.467000

Transformation Matrix:
                  0          1          2    
      0      54.670000   0.000000   0.000000
      1       0.000000  54.670000   0.000000
      2       0.000000   0.000000  54.670000

-----------------------------
Super Cell Origin:   0,   0,   0
-----------------------------
-----------------------------
The Center of XYZ Coordinates
-----------------------------
2.278, 2.278, 2.278

---------------------------------------------------------------------
Saving xyz file: CeO2.cif_10x10x10.xyz                   ...Done
---------------------------------------------------------------------


*************** ORCA CRYSTALPREP TOOL TERMINATED SUCCESFULLY ************
```

并将在打开 `DoHemiSphereSC` 关键词时以立方（a）或半球（b）构建方式创建图 {numref}`fig:CeO2_Supecells_CrystalPrep` 中所示的 10x10x10 球形超胞。注意立方超胞构建方案适合创建用于处理体相
化学问题的嵌入簇（例如半导体光学带隙的计算，{cite}`Dittmer2019`）。相比之下，半球超胞构建选项预计
对构建用于处理表面相关问题的嵌入簇（例如分子在表面上吸附能的计算，{cite}`kubas2016surface`）非常有用。


(fig:CeO2_Supecells_CrystalPrep)=
```{figure} ../../images/CeO2_Supecells_CrystalPrep.*

CeO2 生成的立方（左）与半球（右）10x10x10 超胞
```

- **支持加载定制的 QC.xyz 文件**

从 ORCA 6.1 起，可以在 orca_crystalprep 中直接生成和加载定制的 QC 文件。

这通过启用 `DoSymetricSC` 关键词实现。这样所有生成的超胞共享相同的中心。
因此对 CeO2，可以生成 1x1x1 或 2x2x2 最小超胞并构建/定制 QC.xyz 文件（本例中为 Ce24O64.xyz）。
随后可以通过设置 `LoadQCCluster true` 加载 QC 文件来重新执行 orca_crystalprep

```orca
%crystalprep


#************************
#Read CIF/XYZ
#************************
DoCIF true

#------------------------
#INPUT CIF/XYZa
#------------------------
InputCIF "CeO2.cif"
InputQCXYZ "Ce24O64.xyz"
LoadQCCluster true
#------------------------
#Set Special Tasks
#------------------------
#SpaceGroupNumber 200

#************************
#Generate SuperCell
#************************
DoSuperCell true
SCDimension "10x10x10"
PrintLevel 2
#************************
#Setup Embedding Approach
#************************
DoEmbedding true
DoSymetricSC true
DoSymmetryOperations true
DoHemiSphereSC true
CellVolumeFraction 0.01
DoLayers true
ECPLayers 3
#------------------------
#Atom Type Charge Spin
#------------------------
NAtomTypes 12
 Ce     0    4.0  0.0
 Ce     1    4.0  0.0
 Ce     2    4.0  0.0
 Ce     3    4.0  0.0
 O      4    -2.0  0.0
 O      5    -2.0  0.0
 O      6    -2.0  0.0
 O      7    -2.0  0.0
 O      8    -2.0  0.0
 O      9    -2.0  0.0
 O     10    -2.0  0.0
 O     11    -2.0  0.0

#************************
#Generate Inputs
#************************
#------------------------
# Simple/IC-QMMM inputs
#------------------------
DoICQMMMInput true

#------------------------
#QCCharge 0
#QCMult 1
#------------------------
end
```

这将为定制的 QC=$[Ce_{24}O_{48}]^0$ 量子簇和 3 层 ECP 生成图 {numref}`fig:CeO2_embedded_cluster` 中所示的嵌入簇。

注意在这种情况下，装配 ECP 和 PC 区域的不同层默认基于所选
QC 簇的体积生成。这种情况下使用由 `CellVolumeFraction 0.01` 定义的晶胞体积的小分数是有益的，它可以用作
层生成的判据。

(fig:CeO2_embedded_cluster)=
```{figure} ../../images/CeO2_embedded_cluster.*

为 QC=$[Ce_{24}O_{48}]^0$ 量子簇和 3 层 ECP 生成的 CeO2 嵌入簇
```

最后一步，orca_crystalprep 生成 IC-QM/MM 输入文件为

```orca
!Ionic-Crystal-QMMM
#Include Method


%qmmm
#--------Define the Cluster---------
ORCAFFFilename= "CeO2.cif_10x10x10.ORCAFF.prms"
Use_QM_InfoFromPDB true
Use_QM3_InfoFromPDB true
ECPLayerECP= "SDD"
#--------Charge Convergence---------
CONV_Charges false
ENFORCETOTALCHARGE true
CHARGE_TOTAL    0
PrintLevel 4
end
#-----------------------------------

*pdbfile 0  1 CeO2.cif_10x10x10.pdb

```

注意 QC、ECP 和 PC 区域的信息从生成的 `.pdb` 文件读取。

-   关于 IC-QM/MM 和 QM/MM 模块的一般信息可在章节
    {ref}`sec:multiscalesimulations.qmmm.orca` 中找到

-   与 `orca_crystalprep` 工具和嵌入方法相关的更多细节和示例
    在教程"用嵌入簇方法处理固体"中提供。
