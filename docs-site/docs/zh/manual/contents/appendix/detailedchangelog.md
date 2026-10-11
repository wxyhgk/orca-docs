

<a id="sec:appendix.changelog"></a>
# 详细变更日志（Detailed change log）

## ORCA 6.1.1 的变更（Changes ORCA 6.1.1）

### 新特性（New Features）

#### TD-DFT / CIS
- 自旋翻转计算的自然跃迁轨道（NTO）（若通过 `%cis` 块调用）。

#### STEOM-CC
- RHF STEOM/IP/EA 中的对称性标签和 $S^2$ 值（此前仅在 UHF 中）。
- 使用 `orca_2json` 将 STEOM 单激发振幅导出到 JSON
  （需要 `%mdci DoStoreSTEOM true end`）。
- 将激发能、活性特征百分比、
  $S^2$ 以及可选的 irrep 导出到性质文件中的所有根。

#### SOC-CI
- 用于 HEAT 热化学的 SOC-CI。

### 修复（Fixed）

#### DFT
- 近似自旋投影方法（APM）在解析梯度 + CPCM 或 `optTS` + `NumHess` 时崩溃。
- 启用了 D4 与点电荷的计算。

#### MP2
- 轨道优化双杂化中的崩溃。

#### DeltaSCF
- GMF 现在正确允许手动设置与估计不同的鞍点阶数。

#### TD-DFT
- 导致 0 向量 LUMO 的线性相关。
- 重启已修复。
- sTDA/sTD-DFT 吸收和 CD 光谱再次与 `orca_mapspc` 兼容。

#### ROCIS
- 含自旋-轨道耦合的 RIXS 计算崩溃。

#### (ST)EOM-CC
- 修复了 UHF DressJK 中的并行同步问题。
- 修复了 `DoCOSXEOM = true` 时 3-内部 dressing（UHF）中 AO-K(C) 的并行实现。
- 修复了 T1K/T1J 和 AO-K(C)（UHF EOM）中的矩阵容器。
- 作业完成后移除矩阵容器。
- 在 STEOM 的 CIS 部分使用 `orca_cis` 以提高稳定性并找到低能态。
- 修复了 DressJK 中 1 个 beta 电子的问题。
- RHF STEOM：将对称性信息传递给 OPA。

#### AUTOCI
- NEVPT4/FIC-MRCI/FIC-MRCC 中整数溢出导致的崩溃。
- 因批处理错误导致内存消耗超过 `%maxcore`。
- 振幅打印时内存占用过高。
- 响应方程若未收敛现在会中止。
- 降低了 lambda 和响应方程中的数值噪声以及因停滞导致的失败。
- 修复了同时请求梯度和响应时的崩溃。

#### CASSCF
- 崩溃：`!MORead`/`!PAtom` 和 `!CMatrix` 在基组线性相关时导致非正交 MO 系数。
- 修复了 CAS(0,0) 的 `PModel` 初始猜测。
- CPCM 与 NEVPT2-F12/DLPNO-F12 组合时的崩溃。
- 解决了 DMRG 因"Sweep_iteration 数目小于 Num_schedule"而崩溃的问题。
- 在 ref 子块 `%casscf refs ...` 中提供参考时的崩溃。

#### MCRPA
- 修复了范数为零的轨道试探向量。

#### 分子力学（Molecular mechanics）
- `SwitchForceLJ` 和 `ShiftForceCoulomb` 导致的 LJ/库仑能量/梯度的随机偏差。

#### QM/MM
- FMM-QM/MM 中的崩溃。
- GOAT 与 QM/MM：修复了读取完整结构系综时偶发的崩溃。

#### 基组（Basis Sets）
- 修复了 pcH-n 和 aug-pcH-n 基组。

#### 溶剂化（Solvation）
- DLPNO-CCSD/PTES 与 ANO 基组时的崩溃。
- SMD + 虚拟原子或点电荷时的崩溃。
- `LRCPCM = false` 时的崩溃。
- 在 ORCA/openCOSMO-RS 计算中 `MaxCore` 不再被忽略。
- 修复了原生 ALPB 的氯仿。

#### 片段（Fragments）
- GOAT 缺少片段 0 的打印。
- Fragmentator：修复了 `Extend` 和 `NotAssigned` 的片段编号。

#### 几何优化（Geometry optimization）
- `%geom MAXITER 50` 被忽略。
- `OptimizeHydrogens` 未包含所有非 H 二面角。

#### IRC
- 更正了 `Monitor_internals` 的顺序。
- TDDFT 激发态上的 IRC。

#### GOAT
- GOAT-COARSE 在手动定义时的片段计数。

#### DOCKER/SOLVATOR
- 由 Solvator 分配的溶质片段索引现在正确地从 1 开始。
- DOCKER 在 swarm 步骤中只应做单点计算（而不是优化）。
- 修复了 DOCKER 最后一步中失败的优化。
  这些现在不再保存到最终文件中。

#### Hessian
- 使用 `FrozenCore` 的 OOMP2 和 OOCCD 数值 Hessian 崩溃。
- 使用 `MDCI_DEN_NONE` 的 MDCI 数值 Hessian 崩溃。
- PGC 解析 Hessian 崩溃。
- 在 Hessian 文件中存储正确的多重度。

#### EPR
- DKH 下轨道超精细贡献（`Aorb`）崩溃。

#### EDA-NOCV
- 隐式溶剂化方法的 EDA 分解中已包含缺失的 SMD–CDS 项。
- 非局域色散校正已并入自洽和非自洽变体的 EDA 分解。
- CPCM 贡献已从 Fock 算符中移除。
  Delta CPCM 介电项现在表示分子与片段介电贡献之差。
- 对于杂化泛函，Hartree–Fock 交换能贡献已从静电项中排除，
  并加入到总交换项中。

#### 对称性（Symmetry）
- `%Symmetry` 输入块中输入选项 `SymRelaxOpt` 和 `CleanUpGradient` 的默认值已更改。
  几何优化过程中重新确定分子点群现在默认禁用（`SymRelaxOpt false`），
  因为 ORCA 按其设计无法处理这种情况下分子的旋转，
  而旋转是使改变的对称性元素与坐标轴对齐所必需的。取而代之的是，
  通过从梯度中移除所有非全对称的分量来保持点群（`CleanUpGradient true`）。
- 执行 MOREAD 初始猜测时，确定猜测轨道的不可约表示，
  并通过投影到对称性适配轨道上对 MO 进行清理。
- CMATRIX 和 CACTIVE 初始猜测模式现在支持对称性，可由用户选择。
- 修复了对称性集成到 LeanSCF 中的若干缺陷。

#### 并行化（Parallelization）
- MCRPA 和 EDA 的多节点运行。
- 由于每个进程的冗余写入，IAJB 变换的磁盘占用随 `NProcs` 增加。
- RPA 相关能在并行中打印错误。
- USTEOM 中的 I/O 竞态条件（不可复现的崩溃）。
- 多节点上 UHF STEOM 的崩溃。
- GS-ROCIS 预条件子中的并行缺陷。
- 禁用了 GOAT 的分组并行化，因为核由 GOAT 自动分配。

#### JSON 导出（JSON export）
- 修复了 TDDFT/RPA 的 X-Y 振幅。

#### 性质文件（Property File）
- 存储数值计算的 Hessian。
- `orca_pnmr` 无法在性质文件中找到 D 张量。
- 通过 `JSONPropFile True` 存储的 JSON 对某些运行类型不完整。

#### 其他（Miscellaneous）
- 修复了某些情况下 MBIS 电荷打印出 `NaN` 的问题。
- 修复了 SOC-CI 的符号错误。
- 防止 ADLD(D3/D4) 与虚拟或 ghost 原子一起进行时崩溃。
- 对于混合笛卡尔/内坐标，保留给定的内坐标连接关系。
- UHF 单重态缺失响应自旋密度的缺陷。
- 解除了 SHARK 中原子数和基函数数目的硬性限制。
- ESD：`USEJ FALSE` 时 J 矩阵未按单位矩阵打印（反正它会被忽略）。
- ORCA 6.0 引用的 DOI 错误。

### 改进（Improvements）
#### DFT
- 减少了 LibXC LDA 泛函的计算时间。

#### DeltaSCF
- LSR1 预条件子现在可以用电子 Hessian 的最低本征值更新，
  以降低变分坍缩的可能性。
- GMF 预条件子现在可以与动态梯度展开预条件子混合，
  使其更加稳健。

#### F12
- 添加了新关键词以定义 CABS singles 方程中的最大迭代次数：
  `%method F12CABSSingles_MaxIter 100`。

#### 其他（Miscellaneous）
- 优化了 SOS EPR 性质中并行运行的 I/O。
- 优化了 QDPT 跃迁密度的形成。
- 捕获不可用的选项组合：AutoCI + Conventional、SDiagnostic + DLPNO。
- sTDA/sTD-DFT：同时打印长度和速度规范 CD 光谱。

## ORCA 6.1 的变更（Changes ORCA 6.1）

### 新特性（New Features）

#### Startup, Guess, LeanSCF
- BUPO 算法。
- Startup、Guess 和 LeanSCF 的显著内存改进。

#### DFT
- 添加了 B3LYP-3c 方法。
- HF-3c、PBEh-3c、B97-3c 和 B3LYP-3c 扩展到元素 Fr-Pu（使用原始 D3 参数），
  r2SCAN-3c 扩展到 Lr（Z=103）。
- ADFT（能量、梯度、响应、TD-DFT，非 GIAO，非解析 Hessian）。
- 按 Andreas Görling 方式的 RPA 相关能（暂无梯度、密度或响应；NumGrad、NumFreq）。
- B2NC-PLYP 双杂化的简单输入关键词。
- 为 DFT 泛函添加了各种简单输入 `LibXC(method)` 关键词，例如 TASK-LDA、revTM、HSE06、GAS22。

#### 原生 xTB 方法（Native xTB Methods）
- GFN1-xTB 的原生实现，含能量和梯度。
- GFN2-xTB 的原生实现，含能量和梯度。
- 原生 xTB 方法可以使用 ORCA SCF 和绘图基础设施。
  分子轨道、密度和分数占据密度（FOD）可以用 `orca_plot` 绘制。
- 自旋极化方法 spGFN1-xTB 和 spGFN2-xTB。
- 用于 GFN1- 和 GFN2-xTB 自定义参数化的 JSON 参数文件。
- xTB 方法的 ALPB 溶剂化模型的原生实现。

#### 溶剂化（Solvation）
- 解析 DRACO 梯度。

#### SCF 线性响应（SCF Linear Response）
- 解析 Raman 强度：HF、DFT 直到 meta-GGA、RIJ 和 COSX、
  隐式溶剂化、外点电荷。显著快于 NumFreq。
- 静态 dip/dip/dip 超极化率：适用范围与 Raman 强度相同。

#### 轨道定域化（Orbital localization）
- 基于 IAO 的价层虚轨道定域化方法（`PMVVO`、`LIVVO`）。
- IAO 最小基组的不同选项。
- 可通过 `%loc` 对虚 MO 使用不同的定域化方法。
- 在输入文件中启用了 LMO 绘图。

#### 优化（Optimization）
- 重新设计的 L-OPT —— 用于大体系几何优化的 L-BFGS 优化器，
  比以前更高效。
- `!RIGIDBODYOPT` 用于将结构/片段作为刚体优化。
- 用 X/Y/Z 笛卡尔约束替换了冻结坐标（`$` 语法）。

#### NEB
- 使用 S-IDPP 生成更稳健的初始路径。

#### 激发态（Excited states）
- 使用 UHF IP-EOM-CCSD 和 STEOM-CCSD 计算芯电离/激发能。
- RHF/UHF 正则和 BT-PNO IP-EOM 与 STEOM-CCSD 的多芯计算
  （DLPNO 目前一次只能做 1 个芯）。

#### GS-ROCIS：
- 现已实现自旋-轨道耦合。

#### DeltaSCF
- 广义模式跟踪方法。
- 冻结-释放方法。

#### MDCI
- 为 RHF 参考添加 `DT_in_Triples` 校正，并检查在小 $F_{ia}$ 时跳过。

#### AutoCI
- 三阶 NEVPT（NEVPT3）。
- 限制于单双激发的四阶 NEVPT（NEVPT4(SD)）。
- 将单参考 CI/CC 2RDM 导出到 JSON。
- UHF CCSDTQ。

#### AutoCI 响应（AutoCI Response）
- RHF CCSD 偶极-偶极极化率，含和不含轨道弛豫。
- RHF 和 UHF CCSD(T) 偶极-偶极极化率，含和不含轨道弛豫。
- RHF 和 UHF CCSD 四极-四极极化率，含和不含轨道弛豫。
- RHF 和 UHF CCSD(T) 四极-四极极化率，含和不含轨道弛豫。
- RHF 和 UHF GIAO-CCSD NMR 屏蔽，含和不含轨道弛豫。
- RHF 和 UHF GIAO-CCSD(T) NMR 屏蔽，含和不含轨道弛豫。
- UHF GIAO-CCSD EPR g 张量，含和不含轨道弛豫。
- UHF GIAO-CCSD(T) EPR g 张量，含和不含轨道弛豫。

#### CASSCF 模块（CASSCF Module）
- 使用全秩格式的 ICE NEVPT2（ICE-FR-NEVPT2）。
- 多组态对密度泛函理论（MCPDFT）
  - 含转换泛函 tLDA、tPBE 和 tPBE0
  - 以及复数转换泛函 ctLDA、ctPBE 和 ctPBE0
- 长程 CASSCF 短程 DFT（srDFT）
  - 含短程泛函 sr-LDA、sr-PBE 和 sr-PBE0
  - 短程对密度泛函：sr-ctLDA、sr-ctPBE 和 sr-ctPBE0
  - 用于 RI-J 和 RI 积分变换的范围分离积分的稳健 RI 近似
- 用于 MCPDFT 和 srDFT 激发态的有效哈密顿量 CI-DFT 方法。

#### CASSCF 线性响应（CASSCF Linear Response）
- 在 `%casresp` 块中新增用于切换轨道响应、解锁定和 Olsen 预条件子的选项。
- 实现了核-轨道微扰（允许计算 EPR A 张量的 `Aorb` 贡献）。
- 分块预条件子以减少迭代次数和计算时间。

#### 多参考方法（MR methods）
- RASCI / ORMAS 模块。

#### MCRPA 模块（MCRPA module）
- 分块预条件子以减少迭代次数和计算时间。
- 轨道响应可以关闭。这对应于 CAS-CI 计算。

#### 多尺度（Multiscale）
- 自动生成 QM 和活性区域。
- 纯 MM 计算现在可以使用活性原子关键词。
- 添加了用于 QM/QM2 运行拓扑准备的快速 Simple_Eq 选项。

#### MD 模块（MD Module）
- 现已提供 Langevin 恒温器（随机力和拖曳项可分别开启）。
- 约束：现在可以自动约束涉及某一元素（例如 H）的所有键/角。
- 限制：现在可以通过任意数学表达式定义自定义限制函数。
- 添加了新的"回转半径（Radius of Gyration）"Colvar（可将体系限制为球形，例如液滴）。
- Metadynamics：现在可以通过任意数学表达式定义自定义 Colvar。
- 现在可以在 MD 模拟过程中修改原子质量。
- 速度初始化有更多选项（例如让某些分子旋转或平移）。
- "参考轨迹"特性可从已有轨迹重新计算快照。
  也可以计算沿路径的功。
- 波函数外推（ASPC）以减少所需的 SCF 循环次数。
- 可以对原子施加额外的任意力（例如用于自定义偏置势的实验）。

#### 热化学（Thermochemistry）
- 对角 Born-Oppenheimer 校正。
- 通过近似二分量方法对总能量进行自旋-轨道耦合校正。

#### NMR
- 启用了 X2C 和有限核模型的屏蔽计算。

#### 能量分解与波函数分析（Energy Decomposition and Wavefunction Analysis）
- London 色散的原子分解（ADLD）。
- 交换能的原子分解（ADEX）。
- 共价键的 LED（COVALED）。
- ETS-NOCV 的新实现。
- 启用了 X2C 哈密顿量下的 LED。
- RIJCOSX 现在可用于以非杂化 DFT 作为参考波函数的 DLPNO-CCSD(T)-LED。

#### AILFT
- 扩展空间 AILFT（ESAILFT）。

#### 磁弛豫速率（Magnetic Relaxation Rates）
- Orbach 和 Raman II 路径（`orca_magrelax`）。

#### RESP/CHELPG 电荷
- 具有抛物线和双曲约束的 RESP 电荷。
- 现在可以定义具有相同电荷的等价原子集合。

#### ANISO
- 更新了 ORCA 中的 ANISO 接口以支持 MRCI。

#### 基组（Basis Sets）
- Ga-Kr 的 6-31G*。
- CRENBL 基组和 CRENBL-ECP。
- 新的 Jensen 基组：pcX-n、aug-pcX-n、pcH-n、aug-pcH-n（n = 1,2,3,4）。
- 重新实现了 def-SVP、def-SV(P)、def-TZVP、def-TZVPP（H-Lr）。
- 扩展了 def2-mSVP、def2-mTZVP 和 MINIX 至 Lr。
- 扩展了元素 Fr-Lr 的 def2/J 选项。
- 扩展了元素 La-Lu、Fr-Lr 的 def2/JK 选项。

#### 性质文件（Property File）
- 添加了 SCF 和作业计时。
- 添加了 DBOC、gCP 和 SOC 能量贡献。
- 添加了 ESD 荧光速率。
- 通过 `%output JSONPropFile=true` 更方便地转换为 JSON。

#### `orca_2json`
- 计算并导出 AO 基 Fock 矩阵以及分开的 J、K、XC 和 CPCM 项。
- 将 JSON 性质文件转换回原生 ORCA 格式
  （对 6.0 文件支持有限）。
- 添加了 SOC 积分。

#### 其他（Miscellaneous）
- 从 GBW 文件输入几何结构。
- 数值 Hessian 的 TransInvar。
- 用于 Stanton 等人 HEAT 方案的热化学 Compound 脚本。

### 改进（Improvements）

#### TDDFT
- 改进了 `FollowIRoot` 的稳定性。
- TD-DFT 振幅现在存储在 GBW 文件中。
- TD-DFT 计算可以从 GBW 文件重启。

#### GOAT
- GOAT-COARSE 选项用于自动粗粒度构象搜索。
- GOAT-DIVERSITY 用于寻找最大结构多样性的构象搜索。

#### DOCKER/SOLVATOR
- 速度提升约 100 倍，并有大量改进和更新。
- DOCKER 现在可以通过定义搜索的中心和范围，仅在宿主的限定区域中搜索。

#### AutoCI
- 显著改进了 AUTOCI-MP5 能量的标度和运行性能（速度、内存和磁盘空间需求）。
- 改进了 RHF CCSD(T) 2RDM 性能。
- UHF CCSD(T) 梯度精度（缺失的非连通三阶和四阶贡献现已更正）。
- 响应：UHF CCSD 极化率求解器性能显著提升。
- 响应：改为顺序处理响应方程
  （相比同时求解所有微扰，大计算的磁盘需求更低）。
- 打印改进。

#### CASSCF
- 如果请求了色散校正的 CASSCF，计算开始时即中止。
- 添加了关于运行 CASSCF LR 时根数目的通用警告。
- TRAH 子模块：最终活性轨道与其他 CAS 收敛器相同且排序一致。

#### CASSCF 线性响应（CASSCF Linear Response）
- 默认确定更合理的 LR 方程求解阈值。
- 默认使用解锁定。
- 在开始时检查是否存在可执行 LR 计算的响应参数。

#### OpenCOSMO-RS
- 气相轨道可用于溶液中的计算。

#### MD 模块（MD Module）
- 添加了更多警告（例如模拟过程中两个原子靠得太近时）。
- 添加了多种处理 SCF 不收敛的选项。
- 随机速度初始化现在默认产生零角动量（即体系不会旋转）。

#### 热化学（Thermochemistry）
- 允许的温度和压力最大数目扩展到 100。

#### DKH
- 只计算一次 shell-pair 数据。

#### X2C
- 若不需要则跳过网格设置。

#### OPS 重构（OPS refactor）
- 重要：请求多极光谱的关键词已简化。
  某些 Orca 6.0 关键词不再可用。

#### QDPT 模块（QDPT module）
- g 张量 `g(OZ/SOC)` 现在包含 QED 校正因子。
- g 张量 `ggauge` 和 `g(OZ/SOC)` 现在可以在分子坐标系中打印（与 QDPT 关联的更高打印级别）。
- 启用了 CAS 和 MRCI 的态求和（sum-over-states）。
- 降低了 SSC ZFS 计算的内存占用。

#### 性质文件（Property File）
- 所有性质和分量现在已在手册中记录。
- 某些分量现在按可选/条件方式存储。
- 对 `!MM` 和 `!GFN-FF` 默认禁用性质文件存储
  （此外还有 `!GOAT` 和 `!MD-L-Opt`）。
- 能量性质的通用分量结构：
  `SCF_Energy`、`AutoCI_Energies`、
  `CAS_SCF_Energies`、`CAS_DCD_Energies`、`CAS_PT2_Energies`、
  `CIS_Energies`、`MDCI_Energies`、`MP2_Energies`。
- `Calculation_info`：移除了（未分配的）`NumOfFCElectrons` 和 `NumOfCorrElectrons`；
  将"final single point energy"移至与几何相关的 `Single_Point_Data` 性质。
- 存储了 MR-AUTOCI 能量。
- 方法特定的布居分析。
- 方法和状态特定的核梯度，移除了 `ATNO` 分量。
- `G_Tensor`：还存储 `g_PSO`、`g_DSO`、`Delta_g` 分量。
- `A_Tensor`、`EFG_Tensor`：移除了 `activeNucs`。

#### 其他（Miscellaneous）
- 默认 MaxCore 增加到 4GB。
- UCO/UNO 生成性能改进。
- 允许 DSD-PBEP86、DSD-BLYP 和 DSD-PBEB95 与 D4 的简单输入。
- DeltaSCF：改进了带 SOSCF 的预条件子。
- NEB：片段准备。
- `orca_mapspc` 的各种改进。
- Compound 中的各种修复、添加和改进。

### 修复（Fixed）

#### TDDFT
- DCORR 现在应遵守 MaxCore 并在不足时正常中止。
- TDDFT/TDA 振幅和 TDA 激发能的 JSON 输出错误。
- 修复了半经验方法 TDDFT 计算的缺陷。
- 修复了启用 SOC 时基态能量的存储。

#### MDCI
- 为 PTE(S) 和 PTES 构建 CPCM 容器时遵守 MaxCore。
- 基于 UHF 的 CCSD 与 `!CONV` 产生错误结果。
- 导致 PTE(S) 和 PTES 并行结果错误的竞态条件。
- 正则 RHF 和 UHF 的 S 诊断。
- 修复了积分变换问题。
- 修复了 Brückner 和轨道优化 UHF CCD 的问题。
- 估计 RI/DLPNO 类交换积分半变换所需的内存以防止 OOM 终止。
- 若 MDCI 方程不收敛则停止计算（与 SCF 相同）。
- 罕见的对-对积分崩溃。

#### MP2
- MP2 与 ANO 现在可以工作。

#### CASSCF/NEVPT2
- 修复：自定义 `EDIAG` 因错误的单位转换而失败——输入能量现在应以 Eh 为单位。
- 修复：增加了自定义 EDIAG 的态数（硬编码）。
- 修复：若与 TRAH 一起请求了不支持的 CI 求解器则中止。
- DLPNO-F12-NEVPT2 中 CABSSinglesCorrection 现在为默认（DoCABSSingles=1）。
- 修复：DLPNO-NEVPT2 中 MaxIter 未正确传递。
- 修复：QD-NEVPT2 密度未在性质计算中正确使用。
- 修复：NEVPT2 性质计算现在跟踪基态变化。

#### MCRPA 模块（MCRPA module）
- 移除了最终 CI 波函数打印中的运行时瓶颈，
  该瓶颈在根数多、CI 展开长时会成为问题。

#### QDPT 模块（QDPT Module）
- `ggauge` 仍在使用 `CenterOfNucCharge` 作为磁规范原点；
  现在使用全局设置的磁原点。
- 其他 g 张量一阶贡献的修复（现在与 `orca_prop` 一致）。
- 来自 ROCIS 的 QDPT 跃迁密度问题。

#### CASSCF QDPT 性质（CASSCF QDPT properties）
- 更正了跃迁密度和基态自旋密度的索引。
   - 受影响的性质：EFG 张量、RHO、一阶 g 张量贡献、SOS 性质。
- SSC 计算中的内存问题。

#### QDPT 模块态求和（QDPT Module Sum-over-states）
- 当使用 `DoSOS true` 请求 g 张量时现在可以运行
  （之前还必须同时请求 A 张量）。
- 当所有根都包含在 CAS/MRCI QDPT 计算中时，
  SOS g 张量现在与 CAS LR（不含轨道响应）完全一致。
- 更正了跃迁自旋密度的一般检索。
   - 注意：因此 SOS 仅在跃迁自旋密度可用的方法中可用
           （目前：MRCI、CASSCF、CASSCF+NEVPT2、CASSCF+Custom diagonal energies）

#### MD 模块（MD Module）
- Colvar 上的外力现在被正确计算
  （例如与热力学积分相关）。
- 许多缺陷修复（例如"参数过多"缺陷）。
- CIS 和破缺对称性下未计算梯度。

#### 溶剂化（Solvation）
- CPCM 的各种选项：解析、数值 RI、多极。
- QM/MM 计算中 DRACO 关键词不再被忽略。
- 修复了请求 CPCM（裸 CPCM / SMD / openCOSMO-RS）的计算
  在溶质中某元素原子序数 >= 106 时的崩溃。

#### 色散（Dispersion）
- 为可通过 `!ABC` 获取的 Axilrod-Teller-Muto 型
  三体色散处理添加了额外的 `!ATM` 别名。

#### EPR
- 当 EFG 和 HFC 核数目不同时 `orca_euler` 崩溃。

#### NMR
- ZORA NMR 现在自动触发数值 GIAO 单电子积分，与 ORCA 5 相同。
- 修复了 DLU-X2C NMR 中导致错误结果的并行竞态条件。
- `Tau=Dobson` 默认值现在正确应用于 GIAO 计算。
- ZORA 下的 NMR 耦合中止（未实现）。
- 修复了同时请求屏蔽时 X2C 下 DSO 耦合项挂起的问题。
- 修复了 B97-3c 与 XCFun 的 GIAO XC 积分。

#### 优化（Optimization）
- 如果仅使用笛卡尔约束，"大步长"回退也应有效。
- 若需要 `(Re)CalcHess` 则关闭分组并行化。

#### 弛豫势能面扫描（Relaxed Surface Scan）
- 现在允许输入负二面角，改进了错误报告。

#### DOCKER/SOLVATOR
- swarm 最佳结构时的问题。
- 修正惯量矩的手性以避免产生立体异构体。
- 某些原子离质心很远时的壁势问题。
- 溶剂尺寸的小修复。

#### Hessian
- 修复了 `InHessName` 与 `BaseName.hess` 不同时 `PrintThermoChem` 中的 NearIR。
- 修复了多次写入 IR 光谱时的问题。

#### X2C
- 禁用解收缩 ANO 基组的通用收缩，这会导致变慢。
- X2C 下的 CIS/TDDFT 梯度未做图像变换校正。

#### 热化学（Thermochemistry）
- 转动熵贡献中 D(inf)h 点群解析不正确。

#### 惯量张量（Inertia Tensor）
- VPT2 和 PAF：修复了惯量张量计算。

#### 转动常数（Rotational Constants）
- 单位转换常数的小修复。

#### 基组（Basis sets）
- SHARK 和 ORCA 的全部现在支持到 L=10（Hessian 除外）。

#### SCF 线性响应（SCF Linear Response）
- 修复了 BHP22 求解器初始化的问题。

#### Windows
- 修复了 `orca_mapspc` 中 Windows 特有的崩溃。
- NumCalc 中的并行子计算（NEB、NumGrad、VPT2 等）现在在 Windows 上也可用。

#### 性质文件（Property File）
- 通过 N. Lohmann 库（版本 3.11.3）重新实现了 JSON 输出，
  以保证语法有效。
- 减轻了内存和计时开销。
- 遵守 `%output PropFile=false`/`!NoPropFile` 关键词。
- `Quadrupole_Moment`：`EXZ` 和 `NUCXZ` 分量保存的却是 YZ 值。
- XTB 作业中 Hessian 存储不正确。
- CIS/TDDFT 梯度根存储不正确。
- `Chemical_Shift` 分量 `SPSO`、`SDSO` 和 `saniso` 未被存储。
- `Calculation_Info` 在某些计算中未被存储。
- MM、XTB 和 ExtOpt 作业现在存储几何结构和最终能量。
- JSON 输出中的几何结构缺少 ghost、fragment 和 ECP 数据。

#### 其他（Miscellaneous）
- SOSCF 中的崩溃。
- 清理 DFT 稳定性分析的残留文件。
- 原子拟合密度在部分通用收缩下不工作。
- 积分循环中的偶发崩溃。
- QM/MM NEB 中缺少 PDB 文件输出。
- 防止在 GOAT、NumFreq 等中读取 nodefile 时崩溃。
- 单侧数值梯度 `TransInvar=true` 中的缺陷。
- 恢复了 `!AIM` 的功能。
- 移除了 AUTOCI 中残留的临时文件。
- 若 SCF 中跳过预对角化则恢复原始不可约表示。
- 无 beta 电子体系 Hessian 中的崩溃。
- 恢复了 `!DoEQ` 关键词的功能。
- 带 `!ExtOpt` 的 Opt+NumFreq 或 Opt+IRC 作业在优化后停止。
- 在 IRC 中为所有监控的内坐标打印表头。
- 修复了未识别对时的 HFLD。
- 移除了 wB97X-3c 的仅 RIJCOSX 限制。
- CP-SCF 若未收敛现在会中止。
- CIPSI 中的 RI 变换现在可以工作。
- 修复了 AO-MP2、QDPT、`orca_2json`、ECP、ROCIS、LFT 等中的内存泄漏。
- `orca_mapspc` 中超出偶极近似情形的光谱强度打印和分解。
- `orca_vpot`：修复了收缩改变时的 ESP 计算。

### 移除（Removed）

#### CASSCF/NEVPT2
- Cloiszeaux 哈密顿量的 QD-NEVPT2（QDType=QD_Cloiszeaux）。
- NEVPT2 中处理约化密度矩阵的某些选项（D4Step=core、D4Step=D4PT）。

#### MCRPA 模块（MCRPA module）
- 如果本征值方程收敛失败，
  不再提及与 CASSCF 波函数不稳定性的联系。
  手册相应章节也已移除。

## ORCA 6.0.1 的变更（Changes ORCA 6.0.1）

### 修复（Fixed）

#### DFT
  - XCFun 泛函被 LibXC 覆盖时崩溃。
  - 修复了 DFT GGA、NoRI、RKS 的 Hessian。
  - 即使以 `CALC_HESS=TRUE` 等方式调用，VV10 Hessian 也被阻止。
  - 非自洽 DFT-NL 计算（wB97M-V、wB97X-V、B97M-V）的轨道错误。
  - `X_WR2SCAN`：
    - 交换现在可以在 `%method` 块中单独指定。
    - 修复了请求二阶导数时的崩溃。
    - 使用 `X_WR2SCAN` 时 TRAH 现在默认禁用。
    - 若请求二阶导数，现在会自动切换到数值二阶导数。
    - 为上述更改添加了相应的警告。
  - 修复了 PBEh-3c 的氪和锂 gCP 参数，使其与 Grimme 的独立程序一致。
  - r2SCAN-3c 的 gCP 现在已修复（并扩展）至 Z=103。
  - 移除了 wB97X-3c 的 COSX 限制。
#### TD-DFT
  - 使用 `sgradlist` 的 TDDFT 计算的基态梯度错误。
  - `DCORR` 2/3 与 `DoSCS` 在并行中给出错误结果。
  - (D)-校正对完整 TDDFT 不可用。
  - 修复了不使用 COSX 时 Hessian/TDDFT 的内存估计。
  - 若重叠太小，`FollowIRoot` 本不应做任何事，却仍在更新。
  - 修复了 CIS 中到 `BHP22` 求解器的接口。
#### MP2
  - 常规 U-MP2 中的崩溃。
  - RI-MP2 密度中的并行崩溃。
  - (RI-)MP2 梯度与 SMD 时的崩溃。
  - (RI-)MP2 密度与 PGC 和 RIJK 时的崩溃。
  - MP2+CPCM 梯度错误。
  - NearIR + B2PLYP 时的崩溃。
  - 性质文件中 MP2 梯度的缺陷。
#### MDCI
  - 存在 ECP 时 SemiCore 未正确应用。
  - ECP 相关的崩溃。
  - 修复了特定问题中冗余的积分生成。
  - 恢复了旧的 CITrafos 以解决报告的性能问题。
  - 添加了 RKS 参考 (T) 中缺失的四阶双激发项（已存在于 UKS-(T)、RKS-DLPNO-(T) 和 UKS-DLPNO-(T) 中，RHF/UHF 参考下为零）。
  - `UseCISUpdate` 设为 `false` 的 UHF CIS/STEOM 计算。
  - RHF STEOM：TD-DFT 初始猜测。
#### AutoCI
  - 修复了大栈分配，例如在 MRCC 中。
  - 修复了 `!Moread Noiter` 的运行时行为（错误报告"未收敛"）。
  - 修复了 `!UseSym` 错误中止的问题。
  - AutoCI 梯度：当请求 RI 时在计算开始时中止，而不是在耦合簇迭代之后。
#### CASSCF/NEVPT2/QD-NEVPT2
  - 在 SA-CASSCF 解上运行 LR 的问题。
  - CASSCF QDPT 中规范原点设置不正确，导致误导性输出，某些情况下还抱怨无法为原点求值找到密度。
  - 对 AVAS 初始猜测的非活性和虚空间进行正则化，以避免后续 CASSCF 计算中关于芯轨道的虚假警告。
  - AVAS：修复了本应不选择任何占据轨道时占据轨道数目错误的问题。
  - TRAH-CASSCF：计算 CASSCF 核梯度所需的广义 Fock 矩阵。
  - 修复了 CI 初始猜测中耦合系数的冗余生成。
  - 修复了 !UseSym 和 QD-NEVPT2 计算中的 ABS/CD 光谱：CASSCF 跃迁矩选取了错误的密度。
  - 修复了 NEVPT/QD-NEVPT2 基态与 CASSCF 不同时的 ABS/CD。相应跃迁缺失。
  - 修复了 `DoFullSemiclassical=true` 标志下 MCD 光谱未使用 QD-NEVPT2 跃迁密度的问题。
  - 更新了手册：报告的 `D4TPre` 已更新为新的默认值 1e-12。ORCA 5 使用 `D4TPre=1e-10`。
  - 修复了闭壳层情形（例如 CAS(6,3)）在 NEVPT2 中崩溃的问题。
  - 修复了 NEVPT2/FIC-NEVPT2 因错误寻址导致 Vija 类错误能量或崩溃的问题。
  - 修复了 ICE 密度未存储在密度容器中的问题。
#### ANISO
  - 修复了传递给 single-aniso 的 T 和 L 矩阵。
  - 修复了传递给 single-aniso 的非相对论态数目错误的问题。
#### QDPT
  - 更正了"none"之外激发的 QDPT 跃迁密度。
  - 在 QDPT AMatrix 中添加了信息。
  - 已解决 `orca_lft` 中 QDPT 性质的问题。
#### QM/MM
  - QMMM 优化的速度问题。
  - Crystal-QMMM 和 compound 崩溃。
  - 移除了 QMMM-IRC 和 QMMM-NEB 的残留文件。
#### 相对论（Relativity）
  - F12 + X2C/ZORA/DKH 时的崩溃。
  - X2C/DKH/ZORA 下 AutoCI 梯度中不必要的中止。
  - 禁用了 X2C+GIAO+FiniteNuc（尚未实现）。
  - 由于数值不稳定性，当 `fpFWtrafo==false` 时现在跳过 DKH gDSO 的二阶 PC 校正。
#### 溶剂化（Solvation）
  - 禁用了请求 CPCMX 的 XTB 计算的解析梯度和 Hessian（未实现）。
  - 请求 CPCMX 的计算的 FINAL SINGLE POINT ENERGY 错误。
  - 请求 Freq + CPCM + 虚拟原子时的崩溃。
  - 带 CPCM 请求激发态的 QM/QM2 计算崩溃。
  - DRACO 多个 XYZ 文件扫描时的崩溃。
  - CPCM + NoIter + Pal + 开壳层时的崩溃。
  - 修复了 GC 和 CPCM。
#### 优化（Optimization）
  - Multi-XYZ 优化崩溃。
  - 使用 GFN-xTB Hessian 时随机中断。
  - `RECALC_HESS=TRUE` 时的随机崩溃。
  - COPT 在某些条件下保存了错误的笛卡尔 Hessian，会导致崩溃。
  - 可包含的最大角度数目已修复 + 更好的错误消息。
  - 以解析 Hessian 作为初始 Hessian 选项时与 IRC 一起崩溃。
  - NEB-TS 与后续 Hessian 的崩溃，由 NEB 并行进程数变更引起（最多 32）。
  - NEB 并行化（若有足够进程，将——再次——自动并行启动）。
#### GOAT
  - GOAT/DOCKER/SOLVATOR 现在可在 Windows 上运行。
  - 修复了 WorkerRandomStart 并按预期工作。
  - `-REACT` 和 `-EXPLORE` （错误地）未在优化次数中包含 sqrt(NFrag)。
  - GOAT 缺少计时。
#### DOCKER
  - 若所有最终优化都失败则中止，之前却正常结束。
  - 若给出约束则不切换到 COPT。
#### 稳定性分析（Stability analysis）
  - 稳定性分析 + 闭壳层体系 + 后处理（Hirshfeld、NBO 等）。
  - `SkipSecondSTAB` 仍在检查步骤间的能量差。现在无论如何都会继续。
#### `orca_2json`
  - 导出的相对论积分有误，缺少 HMO 和角动量。
  - 原点选择已更正。
  - 空的 `[]` 和 `[""]` 不再崩溃，而是禁用相关选项。
  - 以下情况的性质 JSON 语法无效：
    - 多个几何结构（例如优化）；
    - 某些含同类多个性质的作业；
    - CIPSI 能量；
    - MDCI EOM 能量；
    - XTB 作业；
    - 能量外推。
#### `orca_mapspc`
  - XAS/XES 展宽函数满足 FWHM。
  - 调整了 .stk 文件归一化以报告谱带积分。
#### Compound
  - 相同类型和原子数但排列不同的 MORead。
  - 统计函数中的缺陷。
#### 其他（Miscellaneous）
  - SOMF(1X) 半数值库仑中的并行缺陷。
  - 虚拟/ghost 原子导致 Hessian 崩溃（部分修复）。
  - 修复了双电子体系 Fermi smearing 计算的缺陷。
  - 使用 F12 和 ECP 时 `leanscf_aftermath` 挂起。
  - 已解决 ROCIS 中 RIXSSOC、XESSOC 光谱的问题。
  - 已解决计算 RI-SSC 积分的问题。该性质现在在 CASSCF、LFT 和 MRCI 模块中开启。
  - 修复了输入文件名为"orca"时 MD 和 L-OPT 中的崩溃。
  - 按最初意图，COSX 算法在所有地方默认设为 AUTO。
  - 当不存在冻结核电子时禁用冻结核近似。
  - `orca_vib` 无法从 AnFreq 运行读取 hess 文件。
  - 对非常小的体系，重启 Hessian 可能崩溃。
  - GS-ROCIS 中 Guess CI Matrix 与 Sigma Vector 之间的小偏差。
  - DCD-CAS：移除了残留文件。
  - 非收缩 MRCI：修复了 MRCI 积分变换中的部分通用收缩调用（之前会崩溃）。
  - 几何优化后进行振动频率计算且固定点群为 Ci 时的崩溃。
  - 由于 glibc/内核缺陷移除了 `posix_memalign`。
  - 修复了 NBO 通信。
  - 修复了积分变换中的崩溃。
  - 因缺少预筛选矩阵导致 `orca_vpot` 崩溃。

### 改进（Improvements）

#### 输出（Output）
  - `!PrintMOs` 和 `!LargePrint` 打印所有轨道能量。
  - 移除了对元素 Z > 36（Kr）使用 gCP 时的冗余警告。
  - 添加了 wr2SCAN 和 DFT-D4 扩展的引用。
  - 更好地打印 GS-ROCIS 计算所得态的自旋耦合情况。
  - 打印振动频率时在 irrep 标签前加了计数器。
#### `orca_2json`
  - 在 json 输出文件中添加了引用。
  - basename 可使用绝对路径。
#### `orca_mapspc`
  - 添加了对 VCD、XASSOCV 和 XESSOCV 光谱处理的支持。
#### 对称性（Symmetry）
  - 确保了梯度清理、固定点群几何优化和振动频率计算的正确性（对使用纯 Hartree-Fock 的含实不可约表示的点群）。
  - 确保了 SCF 能量和梯度的 petite-list 算法的正确性。
#### Compound
  - 实现了 basename 的自动识别。
  - 添加了 GOAT 接口。
#### 其他（Miscellaneous）
  - 在输入文件中添加了 ASCII 检查器。
  - 添加了读取不含'>'的多 XYZ 文件的功能。
  - CASSCF 中的 QDPT 现在使用 `%eprnmr` 中定义的磁原点（若未设置，默认为 CenterOfNucCharge 以保持向后兼容）。
  - 降低了密度容器中 CASSCF（跃迁）密度的磁盘占用并优化了性能。
  - 在初始 IDPP 路径生成中保留拓扑。
  - 在性质文件中添加 CIS 梯度。

## ORCA 6.0.0 的变更（Changes ORCA 6.0.0）

### SCF 与基础设施（SCF and Infrastructure）

- 对 SOSCF 求解器进行重大改进以使其更稳健，防止破坏 SCF 的大步长。对 DIIS 求解器的整体改进。
- 由于 SCF 更新，AutoTRAH 现在不那么频繁需要，仅在 50 个循环以上才启动（`AutoTRAHIter`）。
- 改进了 TD-DFT、CP-SCF 和 Hessian 的内存处理。

### 基组（Basis sets）

- 锕系元素（Z = 89, Ac - 103, Lr）的 def-TZVP 和 ma-def-TZVP 赝势基组
- Lehtola 的类氢高斯基组家族（HGBS），包括极化（HGBSP）和增广（AHGBS、AHGBSP）变体，适用于直到 Oganesson（Z = 118）的所有元素
- 镧系元素的 def2-SVPD、def2-TZVPD、def2-TZVPPD、def2-QZVPD、def2-QZVPPD 基组
- vDZP Grimme 双 zeta 价基组
- `!MINIX` 现在正确激活相应的 ECP
- 为 AutoAux 添加了用户指定的 L 极限 `AutoAuxLLimit`
- 修复了 dhf-ECP 中的段错误
- 修复了 `%coords` 中的 `DelECP`
- 添加了 `ReadFragBasis` 关键词，从文件读取片段特定的基组

### 溶剂化（Solvation）

- 新的电荷校正/补偿算法（校正后的电荷打印在额外文件中）
- QM/MM 计算的 C-PCM/B 方案
- DDCOSMO 和 CPCM/X 可用于 XTB 计算和 QM/MM 计算
- 所有溶剂化模型（C-PCM/SMD/ALPB/DDCOSMO/CPCM-X）中名称的统一
- 空腔（C-PCM）基于单位面积恒定电荷数的新离散化方案
 
### DFT

- 允许通过外部参数自定义 LibXC 泛函
- 为某些 LibXC 泛函添加了简单输入关键词
- 添加了 wB97M(2) 泛函参数：必须在两步作业中与 wB97M-V 轨道一起使用（提供 compound 脚本）
- 元素 87（Fr）- 103（Lr）的 D4
- r2SCAN-3c 扩展到元素 87（Fr）- 103（Lr）
- 含 Grimme 修订 D4 参数的泛函的简单输入关键词（wB97X-D4rev、wB97M-D4rev）
- 新的杂化泛函：r2SCANh、r2SCAN0、r2SCAN50、wr2SCAN、wB97X-3c
- 新的双杂化泛函：Pr2SCAN50、Pr2SCAN69、wPr2SCAN50、kPr2SCAN50
- revDSD-PBEP86-D4 和 revDOD-PBEP86-D4 2021 变体的简单输入关键词
- LibXC 组合 `*_xc_*` 泛函的缺陷修复
- 修复了 D4 + ghost 原子的崩溃

### 激发态（Excited states）

- meta-GGA 泛函的解析梯度
- 自旋适配三重态和 NACME 的小缺陷修复
- 激发态优化的 FollowIRoot 现在使用更稳健的算法
- UHF EOM-CCSD 和 STEOM-CCSD 的新实现
- 使用 UHF IP-EOM-CCSD 和 STEOM-CCSD 计算芯电离/激发能

### 相对论（Relativity）

- 启用了相对论方法的 `NumGrad`
- 接触密度的二阶 DKH 图像变换校正
- 磁性质 DKH 图像变换校正的小修复
- 图像变换校正自动激活

### 多尺度（Multiscale）

- 现在可以读取含 HETATM 的 10k+ 原子的 PDB 文件
- 启用了 QMMM 下正确的 FlipSpin 行为
- 更高效的 MM 模块
- 实现了壁势

### 耦合簇 / DLPNO（Coupled cluster / DLPNO）

- 实现了 PNO 生成的能量排序
- 为 DLPNO 添加了半芯处理
- 启用 DLPNO-CCSD(T) 计算运行 DLPNO-CCSD 非弛豫密度

### MP2
- 更正了响应和梯度中的内存估计和批处理
- 移除了缓慢且受限的解析 (RI-)MP2 Hessian 代码
- 移除了 RI-MP2 响应的非默认 Gamma-in-core 选项
- 禁用了单精度计算
- 禁用了 AO-MP2 中的 SemiDirect 选项
- 启用了 RIJDX 下的范围分离 DHDFT 梯度

### NEB

- 改进了 IDPP 初始路径
- NEB 的更高效 GFN-xTB 运行

### COSX

- 改进了 DFT 和 COSX 的数值积分网格
- 更快的网格步
- 改进了 COSX 的性能和精度，对梯度和 Hessian 同样如此

### 性质（Properties）

- NMR 自旋-自旋耦合：
  - 添加了 `SpinSpinElemPairs` 和 `SpinSpinAtomPairs` 关键词以限制计算哪些耦合
  - 通过随机选择减少了所需的 CP-SCF 微扰数目
  - DSO 项被转置了。
  - 非对角 PSO 元素符号错误
  - 效率改进：对 RHF 以限制模式求解 SD/FC CP-SCF 方程，而不是始终使用 UHF
- 优化了 HFC 规范校正的数值积分
- 移除了 CP-SCF 的 `RITRAFO` 选项
- 在 GIAO 的 meta-GGA 磁性质中动能密度的默认处理方式切换为 `tau=Dobson`

### Hessian

- 改进了 Hessian 以避免数值噪声累积并减少虚假虚频的数目。

### 几何优化（Geometry Optimization）

- 对几何优化进行了多项改进，使其更加稳定。完全重新设计了笛卡尔优化器（!COPT），使其足够快以与更快的方法一起使用。
- 几何优化中出现故障时的回退机制，例如内坐标不可接受时。
- 可添加任意球形、椭球形或盒状壁势，这些壁势会反映在能量和梯度上，并可在几何优化过程中使用。

### 对称性（Symmetry）

- 待补充

### 其他（Miscellaneous）

- 能与分子偶极矩一起再现 ESP 的 CHELPG 电荷
- 修复了多步作业中约束的问题
- Molden 输出：在 `[Pseudo]` 块中存储 ECP 信息，将点电荷原子序数设为 0，ghost 原子的处理
- 使 `ExtOpt` 接口更易用
- 在 XYZ 文件中存储 NEB 和 IRC 的能量
- ORCA 中使用的实固体谐波轨道的定义已在本手册的 [orca_2json.real_solid_harmonics](../utilitiesvisualization/orca_2json.md#sec:orca_2json.real_solid_harmonics) 中记录，适用于角动量量子数 $\ell\le 8$
