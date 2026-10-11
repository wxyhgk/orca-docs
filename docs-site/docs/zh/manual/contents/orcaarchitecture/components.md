<a id="sec:orcaarchitecture.general"></a>
# ORCA 结构（ORCA Structure）

<a id="sec:programs.general"></a>
## 程序组件（Program Components）

程序系统 ORCA 由若干相互独立的程序组成，这些程序在运行过程中彼此调用。本版本包含以下基本模块（按字母顺序排列）：

|  |  |
|---|---|
| orca | 主输入与驱动程序 |
| orca_ailft | 从头算配体场理论（Ab Initio Ligand Field Theory） |
| orca_autoci | 使用自动生成环境（ORCA-AGE）的 CI 类型程序 |
| orca_casscf | CASSCF 驱动主程序 |
| orca_casscfresp | CASSCF 静态线性响应 |
| orca_cclib | 为 ACCCI 预计算单粒子耦合系数 |
| orca_chelpg | 计算各种 ESP 电荷 |
| orca_ciprep | 为 MRCI 计算准备数据（冻结核矩阵等） |
| orca_cipsi | 迭代组态展开组态相互作用（ICE-CI） |
| orca_cis | 通过 CIS 和 TD-DFT 计算激发态 |
| orca_cisresp | CIS 响应计算 |
| orca_compound | ORCA compound 语言的通用驱动程序 |
| orca_crystalprep | 从晶体结构文件设置嵌入计算 |
| orca_eca | 求解磁性模型哈密顿量的辅助程序 |
| orca_eda | 能量分解分析模块 |
| orca_esd | 激发态动力学程序，用于计算振动光谱、共振拉曼光谱等 |
| orca_grad | 通用梯度模块 |
| orca_guess | 为 SCF 和 CASSCF 生成初始猜测 |
| orca_leanscf | 用于 HF 和 DFT 的自洽场程序 |
| orca_lft | 配体场理论（Ligand Field Theory） |
| orca_loc | 计算定域分子轨道 |
| orca_mcrpa | 用于激发态的 CASSCF 线性响应 |
| orca_md | 分子动力学程序 |
| orca_mdci | 矩阵驱动相关程序：CI、CEPA、CPF、QCISD、CCSD(T) |
| orca_mm | 经典力场组件 |
| orca_mp2 | MP2 程序（常规、直接和 RI） |
| orca_mrci | MRCI 和 MRPT 计算（逐个选择） |
| orca_ndoint | 计算半经验积分和梯度 |
| orca_nmrspectrum | 根据计算得到的 NMR 参数模拟 NMR 谱 |
| orca_numfreq | 数值 Hessian 计算 |
| orca_pc | 向单电子矩阵中添加点电荷项 |
| orca_plot | 生成轨道图和密度图 |
| orca_pop | 针对给定密度进行布居分析的外部程序 |
| orca_prop | 计算分子性质 |
| orca_propint | 计算性质积分 |
| orca_rel | （准）相对论校正 |
| orca_rocis | 通过 ROCIS 方法计算激发态 |
| orca_scfgrad | SCF 能量（HF 和 DFT）的解析导数 |
| orca_scfresp | 自洽场响应 |
| orca_startup | 在每次单点计算前计算启动数据 |
| orca_vpot | 在给定分子表面上计算静电势 |
| orca_vpt2 | VPT2 分析 |

