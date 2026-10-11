```{index} NEVPT2
```

(sec:modelchemistries.nevpt2)=
# N 电子价态微扰理论（N-Electron Valence State Perturbation Theory, NEVPT2）
N 电子价态微扰理论（NEVPT）属于内收缩（internally contracted）方法家族，适用于 CASSCF/CAS-CI 类型的参考波函数。Angeli 等人发展的 NEVPT2 方法学存在两种表述，即强收缩 NEVPT2（strongly-contracted NEVPT2, SC-NEVPT2）和部分收缩 NEVPT2（partially contracted NEVPT2, PC-NEVPT2）。{cite}`angeli2001journal,angeli2001chemical,angeli2002journal`
尽管 Angeli 等人使用了"部分收缩"这一名称，该方法实际采用的是完全内收缩（fully internally contracted, FIC）的波函数。因此，我们用术语 "FIC-NEVPT2" 来代替 PC-NEVPT2。NEVPT2 具有许多令人满意的性质——其中包括：

-   由于选择 Dyall 哈密顿量 {cite}`dyall1995journal` 作为零阶哈密顿量，它**无侵入态（intruder state free）**。

-   **零阶哈密顿量在微扰空间中是对角的**。因此无需求解线性方程组。

-   它是**严格尺寸一致（size consistent）**的。两个无相互作用体系的总能量等于两个孤立体系能量之和。

-   它在活性子空间内的**幺正变换下不变**。

-   "**强收缩（strongly contracted）**"：微扰函数仅通过其活性部分相互作用。不同子空间相互正交，因此不会在正交化问题上浪费时间。

-   "**完全内收缩（fully internally contracted）**"：对非活性和虚子空间的旋转不变。
    
  两种方法给出的能量质量与 CASPT2 方法相当。{cite}`havenith_calibration_2004,schapiro_assessment_2013` 
ORCA 中实现了强收缩和完全内收缩的 NEVPT2 方法，以及一系列显著提升该方法学可扩展性的近似，使其对大规模应用极具吸引力。这包括处理[大基组](sec:modelchemistries.nevpt2.f12)、[大分子](sec:modelchemistries.nevpt2.dlpno)和[扩展活性空间](sec:modelchemistries.nevpt2.ice)的能力。

除相关能校正外，ORCA 还为 NEVPT2 提供了一系列光谱性质，包括 UV、IR、CD 和 MCD 光谱以及 EPR 参数。这些性质使用第 {ref}`sec:modelchemistries.casscf.properties` 节中描述的"拟简并微扰理论（quasi-degenerate perturbation theory）"计算。在该形式框架中，NEVPT2 校正以"改进的对角能量"形式引入。ORCA 还为强收缩 NEVPT2 变体提供多态扩展（[QD-NEVPT2](sec:modelchemistries.nevpt2.qdnev)）。{cite}`angeli_qdnevpt2,vanvleck` 在此，参考波函数会在动态相关存在的情况下被修正。对于这种参考弛豫（reference relaxation）很重要的体系，计算所得的光谱性质将会改善。

**NEVPT2 只需在一个可正常运行的 CASSCF 输入之上添加一个关键词即可**。 
```orca
!SC-NEVPT2    # for the strongly contracted NEVPT2
!FIC-NEVPT2   # for the fully internally contracted NEVPT2
!DLPNO-NEVPT2 # for the DLPNO variant of the FIC-NEVPT2
! ...
%casscf ...
```
或者，这些方法也可以在 CASSCF 块内部调用，详细设置可在 `PTSettings` 子块中调整。 

我们将在接下来的几个小节中介绍一些[详细设置](sec:modelchemistries.nevpt2.keywords)。由于历史原因，一些特性（例如拟简并 NEVPT2）仅可用于强收缩 NEVPT2。如其他地方所示，强收缩并不是线性标度方法的良好起点。{cite}`sivalingam_comparison_2016` 因此，较新的扩展（如 DLPNO 和 F12 校正）依赖于 FIC 变体。
{cite}`guo_sparsemapssystematic_2016,guo_nevpt2_f12_2017,guo_dlpnof12_2021`
[]{#nevpt2frozen label="nevpt2frozen"} 请注意，ORCA 默认采用冻核近似（frozen core approximation），可通过简单关键词 `!NoFrozenCore` 关闭。冻核设置的完整描述见第 {ref}`sec:essentialelements.frozencore` 节。

(sec:modelchemistries.nevpt2.n2)=
## 一个简单示例：$N_2$ 基态
让我们以氮分子的基态作为一个简单示例。 
在定义了 CASSCF 计算的计算细节之后，我们插入 "`!SC-NEVPT2`" 作为简单输入，或在 `%casscf` 块中指定 "`PTMethod SC_NEVPT2`"。请注意两个关键词拼写上的差异：简单输入使用连字符，而块输入由于技术原因使用下划线。 

```orca
!def2-svp nofrozencore PAtom
%casscf nel  6
        norb 6
        mult 1
        PTMethod SC_NEVPT2 # SC_NEVPT2 for strongly contracted NEVPT2
                           # FIC_NEVPT2 for the fully internally
			   # contracted NEVPT2
                           # DLPNO_NEVPT2 for the FIC-NEVPT2 with DLPNO
                           # DLPNO requires: trafostep RI and an aux basis
end

* xyz 0 1
N       0.0     0.0     0.0
N       0.0     0.0     1.09768
*
```

为了更好地控制程序流程，建议将计算分为两个不同的部分。首先，使 CASSCF 波函数收敛并检查所得轨道。然后，在第二步中读取收敛的轨道并运行实际的 NEVPT2 计算。

```orca
---------------------------------------------------------------
                        ORCA-CASSCF
---------------------------------------------------------------

...
PT2-SETTINGS:
A PT2 calculation will be performed on top of the CASSCF wave function (PT2=SC-NEVPT2)
...
---------------------------------------------------------------
                         < NEVPT2  >
---------------------------------------------------------------
...
 ===============================================================
                       NEVPT2 Results
 ===============================================================
   *********************
    MULT 1, ROOT 0
   *********************

  Class V0_ijab :        dE = -0.017748
  Class Vm1_iab :        dE = -0.023171
  Class Vm2_ab  :        dE = -0.042194
  Class V1_ija  :        dE = -0.006806
  Class V2_ij   :        dE = -0.005056
  Class V0_ia   :        dE = -0.054000
  Class Vm1_a   :        dE = -0.007091
  Class V1_i    :        dE = -0.001963

---------------------------------------------------------------
         Total Energy Correction : dE = -0.15802909
---------------------------------------------------------------
         Zero Order Energy       : E0 = -108.98888640
---------------------------------------------------------------
         Total Energy (E0+dE)    : E  = -109.14691549
---------------------------------------------------------------
```

用 SC-NEVPT2 方法引入动态相关（dynamic correlation）使能量降低了 150 mEh。ORCA 还会打印每个"激发类 V（excitation class V）"对一阶波函数的贡献。我们注意到，对于对应于 CAS(0,0) 的单参考波函数，`V0_ijab` 激发类给出的正是精确的 MP2 相关能。 

在第 {ref}`sec:modelchemistries.casscf.breakingbonds` 节中，我们用 CASSCF 方法研究了 N$_{2}$ 分子的解离。在 `%casscf` 块中插入 `PTMethod SC_NEVPT2`，我们就得到了作为附加信息的 NEVPT2 校正。

```{literalinclude} ../../orca_working_input/C05S01_108.inp
:language: orca
```

(fig:11)=
```{figure} ../../images/611.*

由 CASSCF(6,6) 和 NEVPT2 计算得到的 N$_2$ 分子势能面（def2-SVP）。
```

原则上，CASSCF 中可用的所有选项都可以应用于 NEVPT2。由于 NEVPT2 是作为 CASSCF 的子模块实现的，它将继承 CASSCF 的所有设置（`!tightscf`、`!UseSym`、`!RIJCOSX` 等）。

(sec:modelchemistries.nevpt2.ri)=
## RI、RIJK 和 RIJCOSX 近似

在 [CASSCF](sec:modelchemistries.casscf.ri) 层面设置 RI 近似，将分别设置 NEVPT2 的 RI 选项。三指标积分会被计算并部分存储在磁盘上。带有两个内部指标的三指标积分保存在主内存中。双电子积分则即时组装（on the fly）。辅助基组必须足够大，以拟合出现在 CASSCF 轨道梯度/黑塞矩阵（gradient/Hessian）以及 NEVPT2 部分中的积分。/J 类型的辅助基组在这里是不够的。

```orca
%casscf
  ...
  TrafoStep RI   # enable RI approximation in CASSCF and NEVPT2
  PTMethod  SC_NEVPT2 # or the NEVPT2 approach or your choice
end
```
通过使用 `!RIJCOSX` 或 `!RIJK` 技术近似 Fock 算符，还可以获得额外的加速。使用 `RIJCOSX` 时，必须为 `AuxJ` 辅助基组槽（slot）指定额外的辅助基组。 
关于基组槽的更多信息，参见第 {ref}`sec:essentialelements.basisset.builtin` 节。

```orca
#RIJCOSX one-liner
! def2-svp def2/J RIJCOSX def2-svp/C

# Commented out: alternative definition via %basis block
#%basis
#auxJ "def2/J"
#auxC "def2-svp/C"
#end
```

而 `RIJK` 只需要一个辅助基组（`AuxJK` 槽），且该基组必须足够大，以拟合 Fock 矩阵构建、轨道梯度/黑塞矩阵以及相关部分中的积分。与 COSX 不同，该计算也可以在 `conv` 模式下进行（将 AO 积分存储在磁盘上）。

```orca
#RIJK one-liner: !conv is recommended.
! def2-svp def2/JK RIJK

# Commented out: Alternative definition via %basis block
#%basis
#auxJK "def2/JK" 
#end
```

上述方法学允许计算基函数数量多达 2000 个的体系。在下一小节描述的 DLPNO-NEVPT2 框架下，还可以处理更大的分子。若干示例可以在 [CASSCF 教程](https://orcaforum.kofo.mpg.de/app.php/dlext/?cat=4&sid=9d58efcf2208abe23b1af87a601b42f6)中找到。

(sec:modelchemistries.nevpt2.dlpno)=
## 超越 RI 近似：DLPNO-NEVPT2

对于原子数超过 80 的体系，我们推荐使用 DLPNO-NEVPT2 方法，它将 DLPNO 拟设（ansatz）与 FIC-NEVPT2 方法相结合。{cite}`guo_sparsemapssystematic_2016`
该方法特别有效，因为即使对于大体系，它也能恢复 99.9% 的 FIC-NEVPT2 相关能。 
DLPNO-NEVPT2 的输入结构与其母体 FIC-NEVPT2 方法相似。 
下面，我们给出 {numref}`fig:DLPNONEVFe` 中所示 Fe(II) 配合物的示例输入，
其中活性空间由金属 3d 轨道组成。该示例使用 8 个核心（2.60GHz Intel E5-2670 CPU）大约需要 9 小时（其中一次 CASSCF 迭代需要 3 小时）才能完成计算。DLPNO-NEVPT2 方法学的详细描述可以在我们的文章中找到。{cite}`guo_sparsemapssystematic_2016` 许多 DLPNO 特有的参数可以在 `PTSettings` 子块中设置。相应的关键词与[本手册其他地方描述的 DLPNO 耦合簇拟设](sec:modelchemistries.mdci.localcorrelation)中的关键词相同。
最重要的参数是 `TCutPNO`、`TCutMKN` 和 `TCutDO`。不过，推荐使用简单关键词 `!TightPNO`、`!NormalPNO` 或 `!LoosePNO` 来调节精度。
与正则 FIC-NEVPT2 方法不同，DLPNO 振幅方程需要求解一组线性方程组。 
后者通过 DIIS 求解器迭代求解，该求解器有自己的一套控制参数。

```orca
# DLPNO-NEVPT2 calculation for quintet state of FeC72N2H100
!PAL8 def2-TZVP def2/JK
!moread noiter
%moinp "FeC72N2H100.gbw-CASSCF"
%MaxCore 8000
%casscf
  nel 6
  norb 5 
  mult 5
  
  # mandatory for DLPNO-NEVPT2:
  PTMethod DLPNO_NEVPT2  # will automatically set `TrafoStep RI`
    
    
  # optional settings reapting the defaults
  PTSettings
    # DLPNO specific settings (see DLPNO-NEVPT2 article):
    TCutPNO      1e-8 # cutoff for PNO occupation numbers
    TCutPNO_Core 1e-2 # cutoff for PNO occupation numbers for core orbitals 
    TCutMKN      1e-3 # cutoff for Mulliken populations in the PNO
                      # integral transformation
    TCutDO       1e-2 # cutoff for the sparse map construction of domain
    TCutDOij     1e-5 # cutoff for the differential overlap matrix of ij pairs 
                      # in the prescreening step
    
    # DLPNO DIIS solver settings:
    MaxIter    30    # maximum number of iterations
    MaxDIIS    7     # DIIS max. dimension
    DIISDamp1  0.5   # damping of the residual before DIIS is switched ON
    DIISDamp2  0     # damping of the residual after DIIS is switched ON
    LevelShift 0.2   # LevelShift during update
    LMP2TolE   1e-7  # energy convergence criteria
    LMP2TolR   5e-7  # residual convergence criteria
    LMP2Damp   1.0   # damping for the LMP2 amplitude update
    
  end
end
*xyz 0 5 FeC72N2H100.xyz
```

与 RI-NEVPT2 一样，该计算需要辅助基组。辅助基组应为 /C 或 /JK 类型（更精确）。除了 Guo 等人的论文 {cite}`guo_sparsemapssystematic_2016` 之外，关于精度的简明报告可以在 [CASSCF 教程](https://orcaforum.kofo.mpg.de/app.php/dlext/?cat=4&sid=9d58efcf2208abe23b1af87a601b42f6)中找到，我们在其中计算了交换耦合参数。请注意，在上面的代码片段中，我们注释掉了 `PTSettings` 子块中的默认设置。

如前所述，CASSCF 步骤可以用 RIJK 或 RIJCOSX 近似加速。这两个选项对 DLPNO-NEVPT2 同样有效。RIJK 变体通常比 RIJCOSX 产生更精确的结果。输入文件与之前几乎相同，只是关键词行不同：

```orca
# The combination of RIJK with DLPNO-NEVPT2
!PAL8 def2-TZVP def2/JK conv RIJK
```

(fig:DLPNONEVFe)=
```{figure} ../../images/DLPNO-NEV-Fe.*

FeC$_{72}$N$_{2}$H$_{100}$ 的结构
```

(sec:modelchemistries.nevpt2.f12)=
## 显式相关：NEVPT2-F12 和 DLPNO-NEVPT2-F12
```{index} NEVPT2-F12, DLPNO-NEVPT2-F12
```

与单参考 MP2 理论一样，NEVPT2 相关能随基组收敛缓慢。除基组外推（basis set extrapolation）外，R12/F12 方法是达到基组极限（basis set limit）的常用方法。关于 F12 与外推技术的比较，我们参考 Liakos 等人的研究。{cite}`liakos2013basissetMP2` ORCA 为 FIC-NEVPT2 波函数提供了使用 RI 近似的 F12 校正。{cite}`guo_nevpt2_f12_2017` 由于所涉积分代价高昂，RI 近似是必需的。与单参考 MP2-F12 完全类似，输入需要一个 [F12 基组](sec:essentialelements.basisset.builtin.f12)、一个 [F12-cabs 基组](sec:essentialelements.basisset.aux.cabs) 和一个足够大的 RI 基组（/JK 或 /C）。应当注意，CASSCF 波函数本身也受到基组不完备性的影响。当调用 `F12` 时，会添加一个针对 CASSCF 参考的微扰校正，称为 CABS singles 校正。{cite}`kong_perturbative_2010`

```orcainput
# aug-cc-pvdz/C used as RI basis
 ! cc-pvdz-F12 aug-cc-pvdz/C cc-pvdz-f12-cabs
 %casscf nel 8
         norb 6
         mult 3,1

         # mandatory:
         TrafoStep RI        # RI approximation must be on for F12
         PTMethod FIC_NEVPT2 # FIC-NEVPT2
         PTSettings
           F12 true    # request the F12 correction and CABS singles correction.
         end
 end
 *xyz 0 3
  O      0.0 0.0 0.0
  O      0.0 0.0 1.207
 *
```

NEVPT2-F12 的线性标度版本 DLPNO-NEVPT2-F12，可以处理基函数数量达数千个的体系。{cite}`guo_dlpnof12_2021,guo_nevpt2_f12_2017` 
除 `DLPNO_NEVPT2` 关键词外，输入结构与 NEVPT2-F12 方法完全相同。

```orcainput
# aug-cc-pvdz/C used as RI basis
! cc-pvdz-F12 aug-cc-pvdz/C cc-pvdz-f12-cabs
%casscf nel 8
        norb 6
        mult 3,1

        # mandatory:
        TrafoStep RI           # RI approximation must be on for F12
        PTMethod DLPNO_NEVPT2  # DLPNO variant
        PTSettings
          F12 true             # request the F12 correction and CABS singles correction.
        end
end
*xyz 0 3
 O      0.0 0.0 0.0
 O      0.0 0.0 1.207
*
```

请注意，DLPNO-NEVPT2-F12 算法对于非活性和活性轨道的子空间旋转是幺正不变的。通过收紧 DLPNO 截断阈值（`TCutPNO`、`TCutDO`、`TCutCMO` 和 `TCutDOij`），即使使用定域的内部和活性分子轨道，也可以重现正则 NEVPT2-F12 的结果。

## 约化密度矩阵的处理
NEVPT2 计算涉及高阶约化密度矩阵（reduced density matrices, RDM）的计算，对于 CAS(10,10) 及更大的活性空间，这很快就会成为主要瓶颈。使用 Dyall 的秩缩减方案（rank-reduction scheme），{cite}`dyall_choice_1995` 标准实现最多涉及四阶约化密度矩阵（4-RDM）。{cite}`angeli2002journal` 
相反，若省略秩缩减方案，全秩 NEVPT2（FR-NEVPT2）则需要 5-RDM 及其缩并。{cite}`guo_nevpt2_approx2_2021` 
后者应当在[近似 CAS-CI 参考波函数（如 ICE）](sec:modelchemistries.nevpt2.ice)的背景下使用。

ORCA 使用 NEVPT2 方法的高效重构，避免了显式构建 4-RDM 和 5-RDM。{cite}`kollmar_d4efficient_2021`
其基本思想与 Sokolov 及其合作者最近报道的一项工作类似。{cite}`sokolov_mradc_2020`
该算法需要一个内存密集的中间量，其规模随 CAS-CI 中组态状态函数（configuration state functions, CSF）的数量而增长。
使用选项 `D4Step fly`，通过省略上述中间量，以内存需求降低为代价（增加计算时间）来运行。

```orca
%casscf
  ...
  PTMethod     FIC_NEVPT2  # or SC_NEVPT2

  # detailed settings (optional)
  PTSettings
  D4Step efficient # efficient: calling the default RDM handling
                   # fly      : slower but more economic code
                   #
                   # Cu4 : cumulant approximation of the 4-RDM
                   # Cu34: cumulant approximation of the 3-RDM and 4-RDM
  D4TPre 1e-12     # default PS approximation 4-RDM 
  D3TPre 1e-14     # default PS approximation 3-RDM 
  imaginary 0.0    # imaginary shift (only for FIC-NEVPT2)
end
```

### PS 近似（默认）
为了加速高阶 RDM 的求值，ORCA 对参考波函数使用预筛选近似（prescreening approximation, PS）。{cite}`guo_nevpt2_approx1_2021` 
只有权重大于指定参数 `D4TPre` 的组态才会被考虑。同样的约化也可以通过关键词 `D3TPre` 用于三阶密度矩阵。这两个参数都可以在 CASSCF 模块的 `PTSettings` 子块中调整。 
将参数设为零即可恢复精确的 NEVPT2 能量。该近似适用于 NEVPT2 的所有变体（SC、FIC 和 DLPNO-FIC）。默认阈值 `D4TPre 1e-12` 和 `D3TPre=1e-14` 选择得非常保守，因为降低阈值可能导致伪侵入态（false intruder states）。{cite}`guo_nevpt2_approx1_2021,guo_nevpt2_approx2_2021`

这些近似自然也会影响"组态 RI（configuration RI）"。在此应当指出，一个组态（configuration）对应于一组具有相同轨道占据的 CSF。对于每个态，CI 和 RI 空间的维度都会被打印出来。

```orca
  D3 Build          ... CI space truncated: 141 -> 82  CFGs
                    ... RI space truncated: 141 -> 141 CFGs
  D4 Build          ... CI space truncated: 141 -> 82  CFGs
                    ... RI space truncated: 141 -> 141 CFGs
```

### 累积量近似（可选）
通过累积量展开（cumulant expansion）可以实现大幅的计算节省，该展开最近已被重新评估。{cite}`guo_nevpt2_approx1_2021` 
结果应谨慎对待，因为可能出现伪侵入态。{cite}`falseintruder` 在这些情况下，虚数能级移动（imaginary level shift）是唯一的缓解手段。{cite}`forsberg_ishift_1997` 请注意，虚数移动仅在 FIC-NEVPT2 中实现。

```orca
PTSettings
  D4Step Cu4    # Cu4  : approximate the 4-RDM
                # Cu34 : approximate the 3-RDM and 4-RDM
  imaginary 0.0 # imaginary shift (only for FIC-NEVPT2)
end
```

## 伪侵入态与虚数移动
伪侵入态（false intruder states）是由约化密度矩阵或参考波函数的粗糙近似引入的。{cite}`guo_nevpt2_approx1_2021,guo_nevpt2_approx2_2021`
其出现具有很强的体系特异性。迹象是来自 1-空穴激发类（记作 "V_i" 或 "ITUV"）或 1-粒子激发类（记作 "V_a" 或 "TUVA"）的不合理相关能贡献，例如，
与 2-空穴-2-粒子激发类（记作 "V_ijab" 或 "IJAB"）相比出现正的或过大的相关能。 
为透明起见，当 Koopmans 能量或能量分母为负时，ORCA 会打印警告。

```orca
...
WARNING: Denominator is negative for DEpsilon ITUV i=2 mu=1 : -344.12813836782095 < 0    
WARNING: Denominator is negative for DEpsilon ITUV i=2 mu=2 : -228.47393616112132 < 0    
WARNING: Denominator is negative for DEpsilon ITUV i=2 mu=3 : -218.57612632153200 < 0    
WARNING: Denominator is negative for DEpsilon ITUV i=2 mu=4 : -127.85082085035380 < 0    
Skipped =       126 of          432 LowestEV=-3.843455e+02 ... done in        0.1 sec    
 Reached max. number of intruder state warning (5). Thus, warnings were suppressed for   
 this class to limit the output! 

WARNING: Koopmans matrices have at least one negative eigenvalue (-1.519147e+06) 
         Please check your results carefully.         
```
为避免刷屏输出，警告数量由 `MaxWarnings`（默认=5）限制。当遇到这些警告时，建议检查约化密度矩阵的近似情况。例如，对于 PS 近似，收紧阈值（`D4TPre=1e-14`）应能立即缓解该问题。累积量近似尤其容易出现伪侵入态，因此应予以避免。

作为最后手段，可以添加虚数移动来缓解侵入态。{cite}`forsberg_ishift_1997` 请注意，虚数移动（默认=0.0）仅限于正则 FIC-NEVPT2 实现。

```orca
PTSettings
  imaginary 0.2 # imaginary shift (only for FIC-NEVPT2) . default = 0.0
  MaxWarnings 5 # Max number of denominator warnings before going silent. 
end
```
(sec:modelchemistries.nevpt2.ice)=
## 大活性空间：ICE-NEVPT2
```{index} ICE-NEVPT2
```


标准 CAS-CI 求解器可以进行最大至 CAS(14,14) 活性空间的常规计算。更大的活性空间可以通过 [ICE 拟设](sec:modelchemistries.iceci.cistep)来访问。{cite}`chilkuri_ice1,chilkuri_ice1`
借助 FIC-NEVPT2 方法学的最新扩展（该扩展也允许 ICE 参考波函数），最大至 CAS(34,34) 活性空间的计算成为可能。{cite}`guo_icenevpt2_2025` 
如 Guo 等人的论文所示，对于近似 CAS-CI 解，使用 Dyall 秩缩减方案的正则实现在不引入伪侵入态的情况下无法应用。因此，对于 ICE 参考波函数，ORCA 默认采用全秩 NEVPT2 表述（FR-NEVPT2），其中会考虑额外的 5-RDM 贡献。后者通过 `CASCI_Approx true` 启用。
虽然 ICE 默认参数 `TVar` 是为 ICE-CASSCF 迭代设计的，但它对 NEVPT2 方法并不理想。这里，高阶 RDM 的计算是主要瓶颈，使用相同的阈值是不可行的。正如 Guo 等人所证明的，参数 `TVar 1e-7`（=TGen × $10^{-3}$）已经能得到平衡精度与效率的合理结果。 
按照论文中的方案，建议将计算分为两部分。首先用默认参数收敛 ICE-CASSCF 解并检查所得轨道。 
然后，在第二步中，以更大的 `TVar` 运行 FIC-NEVPT2，并读取第一步的收敛轨道。对于这类计算，我们推荐使用 `D4Step fly` 算法，因为它在处理 RDM 时避免了内存密集的中间量。

```orca
# Starting with converged CASSCF orbitals
!MORead NoIter
%moinp "converged.ice-casscf.gbw" 
%casscf
  ...
  # mandatory keywords for ICE-NEVPT2
  CIStep ICE 
  PTMethod FIC_NEVPT2  
  CI
    TVar 1e-7 # ICE parameter TVar for ICE-NEVPT2 runs.
              # TVar ~ TGen x 1e-3 - this is larger than the default.
  end
  
  
  # optional settings (repeating the defaults)
  PTSettings
    D4Step fly        # memory saving algorithm for larger active spaces
    CASCI_Approx true # setting FR-NEVPT2
    D4TPre 0.0        # recommendation: disabling PS approximation.
                      # No benefit from screening here.
    D3TPre 1e-14      # recommendation: default PS approximation for 3-RDM.
  end
```

## 大活性空间：DMRG-NEVPT2
DMRG 拟设为更大的活性空间提供了另一种选择。可以使用 Chan 课题组发展的方法学对 FIC-NEVPT2 和 SC-NEVPT2 拟设运行 DMRG-NEVPT2 计算。{cite}`guo_dmrg_nevpt2_2016` 此处，约化密度矩阵由 [BLOCK 程序](https://github.com/sanshar/Block)提供。 
应当指出，后者是平台相关的，过去曾有若干崩溃的报告。如需故障排除，请直接联系 BLOCK 开发者。
除了常规的 [DMRG 输入](sec:modelchemistries.dmrg)之外，该程序在 DMRG 块中还需要一个附加参数（`nevpt2_MaxM`）。 

```orca
%casscf 
  cistep DMRGCI
  %dmrg 
    ...
    nevpt2_MaxM 2000 # (see Note below)
  end
  PTMethod SC_NEVPT2 # or FIC_NEVPT2
end
```



## 为 NEVPT2 选择特定的态

ORCA 默认使用 NEVPT2 方法计算 CASSCF 块输入中定义的所有态。有些情况下并不希望如此，用户希望跳过其中一些态。`SelectedRoots[block]` 输入掩码允许只为少数几个态进行计算，其中 "block" 指多重度块（multiplicity block）的编号。块和根（root）的编号从 0 开始。

```orca
!NEVPT2 ...
%casscf
  ...
  MULT   3,1 # multiplicity block
  NRoots 2,3 # number of roots for the MULT blocks

  # detailed settings (optional) for the PT2 approaches
  PTSettings
    # option to skip the PT2 correction for all states except for the ones
    # specified for a selected multiplicity block and root 
    # selectedRoots[block]  = root number counting from 0.
    selectedRoots[1]=0,1 # compute MULT=1 root=0,1 and skip all others.
    
  end
end
```

## 非弛豫密度与自然轨道

对于 FIC-NEVPT2 拟设，可以请求态特定的非弛豫密度（unrelaxed densities）

$$\gamma(p,q)=\langle\Psi_I|E^p_q|\Psi_I\rangle,$$

其中 $\Psi_I$ 指第 I 个态的 NEVPT2 波函数，由零阶和一阶波函数组成

$$ \Psi_I = |0\rangle + |1\rangle.$$

该代码使用 ORCA AGE 工具链实现。{cite}`lechner2024code` 
精确的非弛豫密度需要 CAS-CI 参考波函数的高阶约化密度矩阵（RDM）。 
当使用关键词 `FirstOrder` 将非弛豫密度近似到一阶时，可以避免这一点。 
在这种情况下，昂贵的二阶贡献 $\langle 1|E^p_q)|1\rangle$ 被省略。
一种保留二阶项的经济高效替代方案是累积量近似 `Cu4` 和 `Cu34`。这里，4-RDM 以及可选的 3-RDM 本身被近似以加速其计算。

非弛豫密度可以通过关键词 `NatOrbs true` 来生成自然轨道（natural orbitals）。 
对于每个态，ORCA 将所得轨道存储在单独的 GBW 文件中，后缀为 ".mult.A.root.B.pt2.nat"，其中 "A" 标记其多重度，"B" 其根计数。在 `!UseSymmetry` 的情况下，后缀还将包含该态的不可约表示。 
NEVPT2 自然轨道对于各种分析工具是必需的，例如 [MultiWFN 程序](https://pubs.aip.org/aip/jcp/article/161/8/082503/3309709/A-comprehensive-electron-wavefunction-analysis)。
这些轨道也可以用于自然轨道迭代（`!MORead NoIter`）或系统性地扩展活性空间。{cite}`nevpt2natorbs` 

```orca
%casscf
  ...
  PTMethod     FIC_NEVPT2  
  
  # detailed settings (optional)
  PTSettings
    # densities are disabled by default
    Density Unrelaxed  # unrelaxed density <0+1|E(p,q)|0+1> 
            Cu4        # cumulant 4-rdm approximated unrel. density 
            Cu34       # cumulant 3/4-rdm approximated unrel. density
            FirstOrder # approximate unrel. density <0|E(p,q)|1>
    
    NatOrbs True       # produces the natural orbitals (default=False)
  end
end
```

请注意，ORCA 会对每个态重复布居分析（population analysis）。加上关键词
`!KeepDens` 后，NEVPT2 密度会以 "Tdens-CASNEV" 为前缀存储在密度容器（磁盘上的 **.densities** 文件）中。 
后者可用于交互式地创建密度图（参见第 {ref}`sec:utilities.plot` 节）。 

下面是典型输出的快照：

```orca
Unrelaxed Density     ...
Incorizing ADC        ... done in      0.6 sec
Norm <Psi|Psi>        ... done in      0.1 sec (NORM=     1.064186836)
RDM1 <Psi|E|Psi>      ... done in      0.7 sec
Reference Weight      ...     0.939684618
Trace RDM1            ...    20.000000000 (prior correction)

*** Repeating the population analysis with unrelaxed density.
Orbital energies/occupations assumed diagonal. ***
(Note: Temporarily storing unrelaxed densities as cas.scfp)
------------------------------------------------------------------------------
ORCA POPULATION ANALYSIS
------------------------------------------------------------------------------

...
Natural Orbital Occupation Numbers:
...
N[  4] =   1.98812992
N[  5] =   1.98308480
N[  6] =   1.93858508
N[  7] =   1.49303660
N[  8] =   1.49303660
N[  9] =   1.48519842
N[ 10] =   1.48519842
N[ 11] =   0.05922342
N[ 12] =   0.00921465
N[ 13] =   0.00921465
N[ 14] =   0.00794869
N[ 15] =   0.00620254
...
 ===============================================================
 NEVPT2 Results  
 ===============================================================
 ...
```



## 态平均 SC-NEVPT2
```{index} State-averaged SC-NEVPT2
```

在 Dyall 哈密顿量的定义中，{cite}`dyall1995journal` CASSCF 轨道被选择用来对角化 Fock 算符（伪正则化，pseudo-canonicalized）。因此，使用态平均（state-averaged）CASSCF 波函数时，NEVPT2 过程涉及构建和对角化"态特定"的 Fock 算符，从而为每个态产生一组独特的轨道。对于大量态或较大的分子，这很快就会变得低效，因为每一组轨道都意味着一次积分变换。这是 NEVPT2 的**默认**设置，输出中会打印

```orca
NEVPT2-SETTINGS:
Orbitals      ... canonical for each state
```

对于 **SC-NEVPT2**，可以使用关键词 `canonstep` 设置其他轨道选项。

```orca
%casscf
  ...
  # detailed settings (optional)
  PTSettings 
  # SC-NEVPT2 specific options
  canonstep      0         # state-averaged orbitals and specific orbital energies
                 canonical # canonical for each state (default)
                 averaged  # state-averaged orbitals and orbital energies
                 relaxed   # 1-step orbital relaxation
                           # and canonical for each state (partially relaxed)
  end
end
```

态平均 CASSCF 的最终轨道对角化态平均 Fock 算符。如果对所有态都使用这些轨道，可以节省大量计算。`canonstep 0` 选择轨道能量作为态特定 Fock 算符的对角元素。在 ORCA 3.0 及更早的发布版本中，这曾是默认设置。如果被平均的态性质相似，这些选项效果最好。对于 SC-NEVPT2，我们还实现了另外两个 `canonstep`，它们以精度换取速度，反之亦然。
`canonstep averaged` 更为近似，采用态平均计算中的轨道能量。因此，在这个近似层面上，激发能没有来自 2-空穴-2-粒子微扰类（记作 "V_ijab" 或 "IJAB"）的贡献。

如果所考虑的态差异很大，这些近似的质量会很差，应当关闭。如果态平均轨道在实际 SC-NEVPT2 计算之前对每个态进行了部分弛豫，可以得到更好的结果。
{cite}`domingo2012tca` 通常不可能单独优化每个激发态的轨道。因此，`canonstep relaxed` 会在用正则化轨道运行实际 SC-NEVPT2 计算之前，对每个态尝试一次最速下降（steepest descent）步骤。作为替代，也可以不用近似对角黑塞矩阵的最速下降，而是进行一次 Newton-Raphson 步。

```orca
%casscf
  ...
  PTMethod SC_NEVPT2
  # detailed settings
  PTSettings 
  canonstep relaxed # orbital relaxation for each state
  gstep SOSCF true  # steepest descent step
  NR    false       # Newton-Raphson   step
  end
end
```

尽管态平均计算已经收敛，各个态的梯度仍可能大得出奇。因此，当两种方法都超出其收敛半径时，轨道弛豫可能会失败。ORCA 会以增大的阻尼（damping）重试弛豫。如果轨道更新仍然失败，程序将保留初始轨道。手动设置一个总体阻尼可能有助于弛豫过程。

```orca
%casscf
  ...
  PTMethod SC_NEVPT2
  # detailed settings
  PTSettings
    gscaling 0.5 # damp gradient with a pre-factor
  end
end
```

(sec:modelchemistries.nevpt2.qdnev)=
## 拟简并 SC-NEVPT2
```{index} Quasi-Degenerate SC-NEVPT2
```

前几小节介绍的 NEVPT2 方法遵循"先对角化再微扰"（diagonalize and perturb）的方案。零阶波函数由 CAS-CI 矩阵的对角化确定。CAS-CI 向量张成的空间通常被称为"模型空间（model space）"。随后的微扰理论基于这样的假设构建：所考虑的态在模型空间内已被良好描述。
因此，波函数的一阶校正 $\Psi^{(1) }_I$ 不影响参考态 $\left|I\right\rangle$ 的组成。波函数和能量的校正来自参考态与贡献的一阶相互作用空间中函数 $\left|k\right\rangle$ 的相互作用

$$\Psi^{(1) }_I = \sum_{K} C_K \left|K\right\rangle$$

$$E^{(2) }_I = \sum_{K} \frac{\left\langle I\left|H\right|K\right\rangle\left\langle K\left|H\right|I\right\rangle}{E^{(0) }_I-E_K}$$

当态之间的相互作用/混合在 CASSCF 层面上被错误描述时，这就成了问题。一个典型的例子是氟化锂的解离。

```{literalinclude} ../../orca_working_input/C06S11_399.inp
:language: orca
```

这里，$\Sigma^+$ 的基态和第一激发态不应发生交叉。
然而，在 NEVPT2 层面上，观察到的却是反常的双交叉（double crossing）。

(fig:lifavoided)=
```{figure} ../../images/lif.*

CAS(2,2) 参考下基态和第一激发态的 SC-NEVPT2 与 QD-SC-NEVPT2 Li-F 解离曲线
```

参考态的重新组织可以在拟简并微扰理论的框架内引入。在实践中，构建一个有效哈密顿量（effective Hamiltonian），允许对二阶能量进行"非对角"校正

$$H_{IJ}=\delta_{IJ}E^{(0) }_I + \sum_{K} \frac{\left\langle I\left|H\right|K\right\rangle\left\langle K\left|H\right|J\right\rangle}{E^{(0) }_I-E_K}$$

对该有效哈密顿量进行对角化会给出改进的能量和一个旋转矩阵（右本征向量），从而引入参考态所需的再混合（re-mixing）。SC-NEVPT2 的拟简并扩展 {cite}`AngeliQDNEV` 可以通过关键词 `QDType` 开启。

```orca
%casscf
  ...
  PTMethod SC_NEVPT2     # Must be SC_NEVPT2
  PTSettings
    PrintLevel 1         # default printing
    
    # mandatory
    QDType QD_VanVleck # QD_VanVleck: Hermitian  eff. Hamiltonian (recommended)
                       # QD_Bloch   : non-Hermitian eff. 
                       # 0: disabled (default)
           
    # optional: compute the QD-Corrected density.
    QDPopulationAnalysis True # Repeat population analysis with the corrected density
    QDNatOrbs            True # Get natural orbitals with the corrected density
  end
end
```

对于 `PrintLevel 4`，ORCA 会在计算结束时打印有效哈密顿量矩阵及其本征向量。

```orca
==============================================================
                      QD-NEVPT2 Results
==============================================================
  *********************
   MULT 1,
  *********************

  Total Hamiltonian to be diagonalized
                  0          1
     0    -107.074594  -0.012574
     1      -0.011748-107.003810

  Right Eigenvectors
                 0          1
    0      -0.987232   0.170171
    1      -0.159292  -0.985414

--------------------------
        ROOT = 0
--------------------------
        Total Energy Correction : dE = -0.25309172934720
        Zero Order Energy       : E0 = -106.82353108218946
        Total Energy (E0+dE)    : E  = -107.07662281153667

--------------------------
        ROOT = 1
--------------------------
        Total Energy Correction : dE = -0.23103459727281
        Zero Order Energy       : E0 = -106.77074682157986
        Total Energy (E0+dE)    : E  = -107.00178141885267
```

根据构造，该哈密顿量是非厄米的（`QDType QD_Bloch`）。
因此，用修正后的波函数计算性质（例如期望值）需要左本征向量和右本征向量。对 Bloch 表述中出现的一般矩阵进行对角化，偶尔会导致复本征对——这是不希望出现的伪影。尽管理论上本征值通常只有很小的虚部，但结果并不可靠，ORCA 会打印警告。

```orca
--- complex eigenvalues and eigenvectors
  WARNING! QD-Matrix has eigenvalues with imaginary component! iE(0)=-0.000016                                                                                                            
  WARNING! QD-Matrix has eigenvalues with imaginary component! iE(1)=0.000016
```

`QD_VanVleck` 选项避免了一般本征值分解。
这些方程源自二阶 Van Vleck 微扰理论，由此得到厄米的有效哈密顿量。{cite}`vanvleck` 该方法学等价于 Bloch 哈密顿量的对称化。解总是实的，性质也易于获得。因此，**`QD_VanVleck` 是 ORCA 中推荐的方法**。
关于不同有效哈密顿量理论的更详细比较，我们参考相关文献。{cite}`redmond,brandow`\
在所有表述中，拟简并 NEVPT2 中的能量分母对近似都非常敏感。使用平均轨道和轨道能量的正则化选项（`canonstep 0/2`）有使能量分母减小的趋势。为避免伪影，计算仅限于 `canonstep 1`，此时每个态都有自己的一组轨道。

如果在 casscf 模块中请求了性质，例如[零场分裂（zero-field splitting）](sec:modelchemistries.casscf.properties)，将会额外打印修正后的 CI 向量和能量。 

此外，通过 `QDPopulationAnalysis true`，布居分析会使用修正后的参考波函数和非弛豫密度重复进行。使用指令 `!KeepDens`，这些密度会以 "Tdens-CAS-DPDICPT2" 为名存储并保留在密度容器中，同时附有包含态细节（多重度和根）的后缀。按照 ORCA 的约定，密度和自旋密度的后缀分别以 ".p" 和 ".r" 结尾。为清晰起见，我们附上了密度容器的快照（"orca_plot jobname.densities"）。
请注意，在 `orca_prop` 中处理的[性质](sec:orcaarchitecture.architecture.properties)（例如 [Mössbauer](sec:spectroscopyproperties.moessbauer)），在修正后的密度可用/被允许时，将会用这些密度重新计算。

```orca
Index:                                                   Name of Density    
------------------------------------------------------------------------    
    0:                                                          cas.scfp    
    1:                             Tdens-CAS-DPDICPT2MO.mult.1.iroot.0.p    
    2:                               Tdens-CAS-DPDICPT2.mult.1.iroot.0.p    
    3:                             Tdens-CAS-DPDICPT2MO.mult.1.iroot.1.p    
    4:                               Tdens-CAS-DPDICPT2.mult.1.iroot.1.p    
    5:                               Tdens-CAS-DPDICPT2.mult.1.iroot.0.r    
    6:                               Tdens-CAS-DPDICPT2.mult.1.iroot.1.r    
                                                                            

```

修正后的密度也可以通过设置 `QDNatorbs true` 来构成自然轨道。所得轨道存储在 GBW 文件中，后缀为 "mult.A.iroot.B.QD-NEVPT2.natorbs"，其中 "A" 表示多重度，"B" 表示根计数。


(sec:modelchemistries.nevpt2.keywords)=
## 关键词
```{index} NEVPT2 Keywords
```


NEVPT2 也可以使用 `%casscf` 块中的 `PTMethod` 关键词来设置。注意块输入中关键词里的下划线。 
精细设置在 `PTSettings` 子块中调整。这些方法需要高阶约化密度矩阵，而它们并非对所有 CIStep 都已实现。除默认的 CIStep 外，还支持 `ACCCI`、`ICE` 和 `DMRGCI`。

```orca
%casscf

  # usual CASSCF settings defining the active space and states of interest
  ...
  MULT   3,1 # multiplicity block
  NRoots 2,3 # number of roots for the MULT blocks

  CIStep    ICE     # CSFCI  : default (recommended)
                    # ACCCI  : fast, but memory intense
                    # ICE    : larger active spaces with ICE FIC-NEVPT2
                    # DMRGCI : larger active spaces with DMRG SC-NEVPT2

  TrafoStep RI      # RI approximation for CASSCF and NEVPT2

  # calling the PT2 method of choice
  PTMethod    SC_NEVPT2    # strongly contracted NEVPT2
              FIC_NEVPT2   # fully internally contracted / partially
	                   # contracted NEVPT2
              DLPNO_NEVPT2 # FIC-NEVPT2 using the DLPNO framework for
	                   # large molecules

  # detailed settings (optional) for the PT2 approaches
  PTSettings
    PrintLevel 1      # default printing
    EWIN  -3,1000     # Energy window for the frozencore setting fc_ewin
    NThresh 1e-6      # FIC-NEVPT2 cut off for linear dependencies
    
    # handling of reduced density matrices:
    D4Step  efficient # efficient: default 4-RDM handling 
                      # fly      : memory saving algorithm for larger active spaces 
                      # cu4 : cumulant approximation of the 4-RDM
                      # cu34: cumulant approximation of the 3-RDM and 4-RDM
    D4Tpre  1e-12     # PS approximation of the 4-pdm
    D3Tpre  1e-14     # PS approximation of the 3-pdm
    
    # false intruder state related options:
    TSMallDenom 1e-2 # printing thresh for small denominators
    MaxWarnings  5   # max number of warning before going silent
    imaginary    0.0 # imaginary shift for FIC-NEVPT2

    # option to skip the PT2 correction for all states except for the ones
    # specified for a selected multiplicity block and root 
    # selectedRoots[block]  = root number counting from 0.
    selectedRoots[1]=0,1 # compute MULT=1 root=0,1 and skip all others.
    

    # SC-NEVPT2 specific features:
    QDType    QD_VanVleck      # QD_VanVleck: Van Vleck (recommended)
                               # QD_Bloch: Bloch Hamiltonian
                               # 0: disabled
    QDNatOrbs True             # get revised density and natural orbitals
    QDPopulationAnalysis True  # get revised density and repeat population analysis
    
    # SC-NEVPT2 state-average orbital canonicalization options:
    CanonStep   canonical # canonical for each state (default)
                averaged  # state-average
                relaxed   # canonical and partially relaxed for each state.
                0         # state-average, but state-specific orbital energies
                
    # canonstep=relaxed additional control parameters:
    GScaling 0.5          # damping factor for the stepsize
    GStep    NR           # relax with NR
             SOSCF        # relax with SOSCF
             SUPERCI_PT   # relax with perturbation based SuperCI
    
    # FIC-NEVPT2 specific features:
    F12       true      # add F12 correction  and CABSSingles correction for CASSCF
    Density   unrelaxed # unrelaxed density generated for each state. 
    NatOrbs   true      # computes the natural orbitals
    
    # DLPNO specific settings for expert users (see DLPNO-NEVPT2 article):
    TCutPNO      1e-8 # cutoff for PNO occupation numbers
    TCutPNO_Core 1e-2 # cutoff for PNO occupation numbers for core orbitals 
    TCutMKN      1e-3 # cutoff for Mulliken populations in the PNO
                      # integral transformation
    TCutDO       1e-2 # cutoff for the sparse map construction of domain
    TCutDOij     1e-5 # cutoff for the differential overlap matrix of ij
                      # pairs in the Prescreen step
    # DLPNO DIIS solver settings:
    MaxIter    30    # maximum number of iterations
    MaxDIIS    7     # DIIS max. dimension
    DIISDamp1  0.5   # damping of the residual before DIIS is switched ON
    DIISDamp2  0     # damping of the residual after DIIS is switched ON
    LevelShift 0.2   # LevelShift during update
    LMP2Damp   1.0   # damping for the LMP2 amplitude update
    LMP2TolE   1e-7  # energy convergence criteria
    LMP2TolR   5e-7  # residual convergence criteria
  end
end
```
