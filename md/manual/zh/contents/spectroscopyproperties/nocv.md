```{index} NOCV, EDA
```

(sec:spectroscopyproperties.nocv)=
# 含化学价自然轨道的扩展过渡态方法（ETS-NOCV/EDA-NOCV）

:::{Caution}
ORCA 5.0 中的 NOCV 实现已重写 {cite}`cardenas2025`。
因此，NOCV 的生成不再需要用户事先对分子片段做单点能计算。
这种产生 NOCV 的方式已弃用。
:::

在 ORCA 中可用 EDA-NOCV 框架分析化学键 {cite}`cardenas2025`。
该框架将扩展过渡态（Extended Transition State，ETS）能量分解方法
与化学价自然轨道（Natural Orbitals for Chemical Valence，NOCV）相结合，
以分析成键时发生的电子密度重排 {cite}`nocv2009`。
ETS 方法将与成键相关的能量分解为四个分量：

$$\Delta E_\text{int}=\Delta E_\text{elstat}+ \Delta E_\text{Pauli} +\Delta E_\text{orb} + \Delta E_\text{disp}$$


这表示两个不相互作用的分子片段之间导致成键过程的"瞬时"相互作用。
分子片段的确定是按照所研究的化学键将分子划分为两个片段。
所谓不相互作用，是指分子片段被视为处在无穷远距离，
且每个片段的电子密度保持冻结。
第一个能量项对应于两个不相互作用的分子片段
被置于它们在分子中所占位置时所经历的静电相互作用。
第二项包含由泡利不相容原理引起的总"交换排斥"
以及片段相互靠近时交换-相关能的变化。

$$\Delta E_{Pauli}=\Delta \tilde{E}_{Pauli}+\Delta E^{0}_{XC}$$

需要强调的是，EDA/ETS 分解中报告为 `Pauli Energy` 的值对应于 $\tilde{E}_{Pauli}$。

ETS 分解的第三项对应于一个分子片段的占据轨道
与另一个分子片段的未占据轨道之间相互作用相关的能量。
因此，它与成键过程中电子密度的变化相关。

最后一项表示相互作用的"色散"（dispersion）贡献，
当使用半经典校正方案（如 Grimme 的 D4 校正）
或非局域（non-local，如 NL 和 SCNL）校正时会出现该项。
这些校正适用于局域泛函、杂化泛函和双杂化泛函，
更多细节参见 {ref}`sec:modelchemistries.dispersioncorrections` 一节。

一个用于更细致研究色散贡献的补充框架是
伦敦色散能的原子分解（Atomic Decomposition of London Dispersion Energy）{cite}`regni2025ADLD`
（[ADLD](sec:spectroscopyproperties.led.ad.ld)）。
用户可以为片段和加合物的 [DFT-D](sec:modelchemistries.dispersioncorrections) 校正
都设置这种色散分解。然后便可考察色散贡献的原子分辨变化。

EDA-NOCV 方法将该项分解为与轨道对相关的贡献。
这些轨道通过将分子与由不相互作用的分子片段构成的"超分子"（supermolecule）
之间的差密度矩阵对角化得到。

$$\Delta E_{orb}=\sum_{k=1}^{N/2} \Delta E_{k}^{orb}$$


## 在 ORCA 中运行 EDA-NOCV 分析

:::{Note}
ORCA 6.1 中 EDA-NOCV 方法的当前实现对开壳层和闭壳层计算均支持平均场方法。
:::

要执行 EDA-NOCV 分析，必须指定三个关键要素：

1. **计算类型**：这定义了整体计算框架，并确定分析是用限制性还是非限制性平均场方法进行。
2. **各片段所用的方法**：包括对每个片段单独采用的基组、交换-相关泛函或其他理论方法的选择。通常，每个片段应与加合物在同一理论水平上处理。
3. **对应于每个片段的原子**：这需要定义分子体系中哪些原子属于哪个片段，以便 ORCA 相应地划分分子。

EDA-NOCV 分析通过简单输入行中的 `EDA` 关键词执行。
在下面的例子中，我们给出乙烷分子中两个碳原子之间化学键的 EDA-NOCV 分析输入文件。
新实现允许将两个甲基作为分子片段来研究该体系，
且未配对电子的自旋相反。

```orcainput
#
# Example of an EDA-NOCV calculation for the CH3-CH3 system with triplet fragments
#

!BP86 TZVP EDA        #EDA keyword

%EDA                #EDA block                       
  FRAG1 "BP86 TZVP"  #Method for fragment 1 
  FRAG2 "BP86 TZVP"  #Method for fragment 2
  FRAG1_C 0          #Charge of fragment 1
  FRAG1_M 2          #Multiplicity of fragment 1
  FRAG1_SF TRUE      #Flip spin option for fragment 1
  FRAG2_C 0          #Charge of fragment 2
  FRAG2_M 2          #Multiplicity of fragment 2
END

*xyz 0 1                                            
 C  0.019664  -0.034069   0.009101
 H  0.039672  -0.069395   1.109620
 H  1.063205  -0.065727  -0.341092
 H -0.474230  -0.953693  -0.341621
 C -0.703210   1.217999  -0.497874
 H -0.723753   1.252869  -1.598316
 H -1.746567   1.250049  -0.147169
 H -0.208833   2.137544  -0.147653
*

%Frag              #Fragment assignment using %frag block
  Definition
    1 {0:3} end
    2 {4:7} end
  end
end
```


所有与 EDA-NOCV 计算相关的参数都可以在 `%EDA` 块中指定。
各片段所用的方法可以用两种方式指定：使用关键词或传递文件。
第一种方法用 `FRAG1` 和 `FRAG2` 关键词分别为片段 1 和片段 2 指定。
在引号中，必须指定每个片段所用的理论水平和基组，以及任何其他关键词选项。
标准做法是对每个片段和分子使用相同的理论水平，
但也可以指定不同的理论水平。

:::{Caution}
每个分子片段和完整分子所用的基组必须一致。
每个分子片段可以使用不同的基组，
但这必须在分子计算中通过 `%basis` 块为相应的原子/片段加以指定。例如：

```orca
!B3LYP EDA

%basis
  FragBasis 1 "TZVP"
  FragBasis 2 "def2-SVP"
end

%EDA
  FRAG1 "B3LYP TZVP"
  FRAG2 "B3LYP def2-SVP"
end
.
.
.

```

:::


若片段计算需要额外参数，可通过关键词 `FRAG1_METHODFILE` 和
`FRAG2_METHODFILE` 将其传递到单独的文件中。
```orca
%EDA
  FRAG1_METHODFILE "method.txt"
  FRAG2_METHODFILE "method.txt"
END
```

当方法无法仅用关键词指定、而必须使用方法块时，尤其应使用此选项。
例如，要在隐式溶剂化方法（如 C-PCM）中指定不受支持的溶剂。
此时，方法文件如下所示：

```orca
BP86 TZVP

%CPCM            #CPCM block
  epsilon 80          #Dielectric constant
  refrac  1.0         #Refractive index
END
```

:::{Note}
为每个片段指定方法时不需要 "!" 符号。
无论是在 `%EDA` 块中使用 `FRAG1` 和 `FRAG2` 关键词，
还是在使用 `FRAG1_METHODFILE` 和 `FRAG2_METHODFILE` 时的方法文件中，都是如此。
:::



当前实现允许带电和开壳层片段。
要指定每个片段的电荷，必须使用关键词 `FRAG1_C` 和 `FRAG2_C`。
类似地，关键词 `FRAG1_M` 和 `FRAG2_M` 可用于指定每个片段的多重度。
除非另有说明，默认每个片段被视为中性闭壳层。
各片段的总电荷必须等于分子的电荷。

新实现还允许指定其中一个片段中未配对电子的自旋。
例如，在研究 CH$_3$-CH$_3$ 体系时，
先前的 ORCA 实现只允许使用带电的闭壳层片段
CH$_3^{+1}$ 和 CH$_3^{-1}$。
现在则可以考虑中性开壳层的甲基作为分子片段。
默认情况下，ORCA 中开壳层体系的未配对电子被视为自旋向上电子，
但可通过关键词 `FRAG1_SF` 和 `FRAG2_SF` 加以改变。
这一调整可减小两个甲基片段之间的泡利排斥。

分子片段可用 `%Frag` 块指定，也可在每个原子旁标出它们属于哪个分子片段。
具体做法是在每个原子旁的括号中放置数字 1（第一个片段）或数字 2（第二个片段）。

```orcainput
#
# Example of an EDA-NOCV calculation for Li-NH3 bonding
#
!BP86 TZVP EDA  

%EDA
  FRAG1 "BP86 TZVP"
  FRAG2 "BP86 TZVP"
  FRAG1_M 1
  FRAG1_C 1
END

*xyz 1 1
Li(1)     -0.212072      1.951867      0.003088
N (2)     -0.424027     -0.022414     -0.010889
H (2)     -0.914047     -0.381589     -0.841562
H (2)     -0.958117     -0.388240      0.789150
H (2)      0.468043     -0.535155      0.011083
* 
```
需要注意的是，使用 `%Frag` 块时原子索引从 0 开始。
例如，上面 Li$^+$-NH$_3$ 的输入中片段也可指定为：

```orca
%Frag            #Fragment assignment using frag block
  Definition
    1 {0} end
    2 {1:4} end
  end
end
```
## EDA-NOCV 输出文件

EDA-NOCV 输出分为两部分。
第一部分对应 ETS 能量分解分析（Energy Decomposition Analysis）。
在这一部分中，ETS 分解方法的每个能量项以 Hartree 和 kcal/mol 为单位打印。
此外，若计算中使用了色散校正，
还会打印分子的色散校正与分子片段的色散校正之差。
以下是上一节中 Li$^+$-NH$_3$ 输入的 EDA-NOCV 结果：

```orca
--------------------------------------------------------------------------------
                         Energy Decomposition Analysis
--------------------------------------------------------------------------------
     Energy Term                      Hartree         Kcal/mol
--------------------------------------------------------------------------------
     Bond Energy                   -0.0606951779       -38.09
     Orbital Energy                -0.0181138301       -11.37
     Electrostatic Energy          -0.0698943902       -43.86
     Pauli Energy                   0.0311314946        19.54
     Delta E^0(XC)                 -0.0038170134        -2.40
     Delta Dispersion               0.0000000000         0.00 

```

第二部分对应于按 NOCV 的轨道能量分解。
在这一部分中，打印与每对 NOCV 相关的正本征值和负本征值。
每对 NOCV 的轨道能量贡献以 kcal/mol 给出。
此外，每个贡献还进一步分为动能分量和势能分量。
所有轨道贡献之和必须与能量分解部分所示的总量相符。

```orca
--------------------------------------------------------------------------------
                                NOCV analysis                                   
--------------------------------------------------------------------------------
  negative eigen.    positive eigen.    DE_k          DT_k        DV_k
         (e)                (e)      (Kcal/mol)   (Kcal/mol)   (Kcal/mol)
--------------------------------------------------------------------------------
    -0.1972432025      0.1972432025     -7.50      -104.45        96.96 
    -0.0804518243      0.0804518243     -1.84        37.57       -39.41 
    -0.0804301830      0.0804301830     -1.84        37.56       -39.40 
    -0.0193872139      0.0193872139     -0.16         7.73        -7.89 
    -0.0062264967      0.0062264967     -0.03       -14.21        14.19 
    -0.0006108673      0.0006108673     -0.00         1.68        -1.68 

                             Sum_k:    -11.37       -34.13        22.76 


```

若使用的是开壳层体系或分子片段，NOCV 部分会分为两部分：
一部分为自旋向上（Alpha），另一部分为自旋向下（Beta）的 NOCV 对。
能量分解部分保持不变。
以下是上一节中 CH$_3\cdot$ 与 CH$_3\cdot$ 输入的 EDA-NOCV 结果：

```orca
--------------------------------------------------------------------------------
                         Energy Decomposition Analysis
--------------------------------------------------------------------------------
     Energy Term                      Hartree         Kcal/mol
--------------------------------------------------------------------------------
     Bond Energy                   -0.1776418532      -111.47
     Orbital Energy                -0.2616245160      -164.17
     Electrostatic Energy          -0.2105241711      -132.11
     Pauli Energy                   0.4120105303       258.54
     Delta E^0(XC)                 -0.1174259863       -73.69
     Delta Dispersion               0.0000000000         0.00 


--------------------------------------------------------------------------------
                             NOCV analysis  Alpha                                  
--------------------------------------------------------------------------------
  negative eigen.    positive eigen.    DE_k          DT_k        DV_k
         (e)                (e)      (Kcal/mol)   (Kcal/mol)   (Kcal/mol)
--------------------------------------------------------------------------------
    -0.4750327845      0.4750327845    -75.83      -124.63        48.80 
    -0.0599933854      0.0599933854     -1.69         8.51       -10.19 
    -0.0599917403      0.0599917403     -1.69         8.51       -10.20 
    -0.0510118074      0.0510118074     -0.85       -32.69        31.84 
    -0.0510053349      0.0510053349     -0.85       -32.68        31.83 
    -0.0412188369      0.0412188369     -0.92         9.08       -10.00 
    -0.0252608236      0.0252608236     -0.28       -19.31        19.04 
    -0.0006887548      0.0006887548     -0.00        -6.18         6.18 
    -0.0003325354      0.0003325354      0.00         4.22        -4.21 

                       Sum_k Alpha:    -82.09      -185.17       103.09 

--------------------------------------------------------------------------------
                             NOCV analysis  Beta                                  
--------------------------------------------------------------------------------
  negative eigen.    positive eigen.    DE_k          DT_k        DV_k
         (e)                (e)      (Kcal/mol)   (Kcal/mol)   (Kcal/mol)
--------------------------------------------------------------------------------
    -0.4750299362      0.4750299362    -75.83      -124.66        48.84 
    -0.0599969082      0.0599969082     -1.69         8.47       -10.16 
    -0.0599919936      0.0599919936     -1.69         8.50       -10.18 
    -0.0510107218      0.0510107218     -0.85       -32.65        31.80 
    -0.0510066746      0.0510066746     -0.85       -32.66        31.82 
    -0.0412230078      0.0412230078     -0.92         9.10       -10.01 
    -0.0252605237      0.0252605237     -0.28       -19.31        19.04 
    -0.0006887767      0.0006887767     -0.00        -6.19         6.18 
    -0.0003325489      0.0003325489      0.00         4.21        -4.21 

                       Sum_k  Beta:    -82.09      -185.20       103.11 
```

此外，NOCV 轨道保存在名为 `base_name.NOCV.gbw` 的文件中。
这些轨道可用 Molden 或 Avogadro 等标准可视化程序显示。

## 用 `orca_plot` 可视化变形密度贡献
变形密度（deformation density）可表示为与成对 NOCV 相关的一组贡献：
$\Delta \rho(r)=\sum_{k=1}^{n/2} v_k \left[ -\psi_{-k}^2 +\psi_{k}^2 \right]= \sum_{k=1}^{n/2} \Delta \rho_k(r)$

新的 ORCA 实现允许可视化这些变形密度贡献。
这些密度保存在 EDA-NOCV 分析过程中生成的密度容器中。
可以用 `orca_plot` 将这些密度转换为标准可视化程序可读的格式来显示它们。
为此，需要使用以下命令：


```orca
orca_plot gbwfilename -i
```

这会显示一组用于生成相应文件的不同选项。

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

选项 9 会列出 EDA-NOCV 计算过程中保存的所有密度。
对应于 NOCV 对的密度记为 `base_name.NOCV0_0.tmp`，
其中 "base_name" 是输入文件的名称，
`.tmp` 扩展名前的数字对应于对变形密度的贡献。
保存前五个密度贡献，因此该数字范围为 0 到 4。
在开壳层计算中，保存前五个自旋向上和自旋向下的贡献。
自旋向上贡献标记为 `.NOCV0`，自旋向下贡献标记为 `.NOCV1`。

```orca
Index:                                                   Name of Density
------------------------------------------------------------------------
    0:                                                        base_name.scfp
    1:                                                        base_name.scfr
    2:                                                      base_name.P0.tmp
    3:                                                      base_name.P1.tmp
    4:                                                 base_name.NOCV0_0.tmp
    5:                                                 base_name.NOCV0_1.tmp
    6:                                                 base_name.NOCV0_2.tmp
    7:                                                 base_name.NOCV0_3.tmp
    8:                                                 base_name.NOCV0_4.tmp
    9:                                                 base_name.NOCV1_0.tmp
   10:                                                 base_name.NOCV1_1.tmp
   11:                                                 base_name.NOCV1_2.tmp
   12:                                                 base_name.NOCV1_3.tmp
   13:                                                 base_name.NOCV1_4.tmp
```

要生成图，先从主菜单选择选项 `1 - Enter type of plot`。
随后会打开一个子菜单：

```orca
     1 -   molecular orbitals
     2 -   (scf) electron density          ......  (scfp   )  => AVAILABLE
     3 -   (scf) spin density              ......  (scfr   )  => AVAILABLE
     4 -   natural orbitals
     .
     .
     .
```

这里我们选择第二个选项 ` 2 -   (scf) electron density`。
然后它会询问 `base_name.scfp` 是否是我们想使用的密度。
这对应于总密度，因此我们必须回答否。
接着，它会要求输入我们决定使用的密度名称。
这里，我们填入所关注的 NOCV 贡献的名称，
即在主菜单中选择选项 `9 - List all available densities` 时所列出的名称。

也可以用主菜单中的 `5 - Select output file format` 选择所生成文件的格式，
以及用选项 `4 - Enter number of grid intervals` 选择所用网格。
最后，用选项 `11 - Generate the plot` 生成图。
{numref}`fig:nocvsdens` 展示了前四个 NOCV 的变形密度贡献。

:::{Caution}
要绘制变形密度时，不要混淆 `base_name.gbw` 与 `base_name.NOCV.gbw`。
前者包含与 NOCV 相关联的变形密度，而后者包含 NOCV 轨道。
:::


(fig:nocvsdens)=
```{figure} ../../images/NOCVs_densities_Li_NH3.png
Li$^+$-NH$_3$ 前四个 NOCV 所关联的变形密度
```


## 处理基态简并的片段
在片段基态电子组态简并的体系中，
可能需要采取额外的预防措施才能得到 EDA-NOCV 分解的准确结果。
处理简并片段时，预分子（promolecule）和分子的部分占据分子轨道
可能不具有相同的取向。
这表现为 NOCV 分解的本征值为整数，并且轨道能量较高。
其成因是：由于片段基态电子组态的简并，
从片段分子轨道构建预分子分子轨道时轨道占据不恰当。

一个例子是考虑 C 和 O 片段处于三重态基态时的 C-O 体系。
在此情形下，C 原子的电子组态为 $2s^22p^2$，
而 O 原子的组态为 $2s^22p^4$。
两个片段的 2p 轨道都是简并的。
当它们结合成键时，分子片段按 {numref}`fig:co_orbitals` 所示方式组合。
因此，一个片段中含有未配对电子的轨道
应当与另一个片段中相应的轨道相一致。
这可通过确保两个片段中部分占据轨道具有相同取向来实现。

(fig:co_orbitals)=
```{figure} ../../images/C-O_molecular_orbitals.png
CO 分子的分子轨道
```

所以在 C-O 体系中，我们必须确保 C 原子的两个未配对电子
处于相应的 $2p^1_y$ 和 $2p^1_z$ 轨道上，
以便它们能与 O 原子 $2p^1_y$ 和 $2p^1_z$ 轨道上的两个相应未配对电子组合。
在此情形下，这相当于将 C 原子的第一个部分占据轨道 $2p^1_x$
与未占据轨道 $2p^0_z$ 交换。
为此，我们需要先对需要修改的片段运行一次单点计算。
然后，我们可以在 EDA-NOCV 分析中通过在相应片段的方法文件中
指定 `MOREAD` 关键词、并用 `%moinp` 传递 `.gbw` 文件，
将该计算的轨道用作 C 片段计算的输入。
接着我们需要指定要交换的片段分子轨道。
这可用 `%scf` 块中的 `Rotate` 功能完成。

```orca
%scf
  Rotate
   { MO1, MO2, Angle }
   { MO1, MO2, Angle, Operator1, Operator2 }
   { MO1, MO2} # Shortcut to swap MO1 and MO2. Angle=90 degrees.
  end
end
```

其中 `MO1` 和 `MO2` 指我们想要交换的分子轨道的索引。
更多细节参见
[改变初始猜测 MO 的顺序并破坏初始猜测对称性](#sec:essentialelements.initialguess.changes) 一节。

:::{Note}
分子轨道的索引从零开始。
:::

下一个输入对应于由三重态基态片段计算 C-O 体系。
关键词 `FRAG1_FS` 用于翻转 C 原子未配对电子的自旋。

```orcainput
!BP86 TZVPP  EDA

%EDA
  FRAG1_METHODFILE "frag1.method"
  FRAG2_METHODFILE "BP86 TZVPP"
  FRAG1_M 3
  FRAG1_FS TRUE
  FRAG2_M 3
end

*xyz 0 1
  C(1)           0.00000000000000      0.00000000000000      0.0
  O(2)           0.00000000000000      0.00000000000000      1.136
*
```

为获得正确的占据数，需要交换 C 片段的分子轨道。
下一个输入对应于 C 片段的方法文件。
通过在简单输入行使用关键词 `MOREAD` 并用 `%moinp` 传递 `.gbw` 文件，
其中含有 C 原子前一次单点计算的分子轨道。
在 `Rotate` 小节中，交换 $2p_x^1$ 和 $2p_z^0$ 轨道，
即索引 2 和 4。
这样碳的 $p$ 轨道就从 $2p^1_x2p^1_y2p^0_z$ 变为 $2p^0_x2p^1_y2p^1_z$，
与氧的 $2p^2x2p^1_y2p^1_z$ 相一致。

```orca
BP86 TZVPP MOREAD

%moinp "carbon.gbw"

%scf
  Rotate
  {2,4}
  end
end
```

这确保了预分子与分子轨道之间的一致性，并使轨道能量最小化。


## EDA-NOCV 与双杂化泛函
ORCA 的新特性之一是可以对 EDA-NOCV 分析使用双杂化泛函。
这些泛函将 MP2 相关能贡献引入 DFT 计算所得的能量中。
使用这些泛函时，在能量分解分析中会新增一个标记为 `MP2 correlation` 的项。
该项对应于分子与其片段之间 MP2 相关分量之差。

使用双杂化泛函时，必须指定所计算密度的类型：
`relaxed` 或 `unrelaxed`，
且必须用 `%mp2` 块为分子和片段分别指定，如下所示：

```
!B2PLYP def2-TZVP def2-TZVP/C EDA
%mp2 Density relaxed end
```

NOCV 分解是用 DFT 计算的密度进行的。
也可以获得并绘制与 MP2 相关对变形密度矩阵的贡献所对应的密度。
该密度贡献定义为 $DP_{mp2\_contribution}=\Delta P_{mp2\_level}-\Delta P_{DFT\_level}$。
对于限制性计算，该密度保存为 `base_name.DP0.mp2`；
对于非限制性计算，自旋向上贡献保存为 `base_name.DP0.mp2`，
自旋向下贡献保存为 `base_name.DP1.mp2`。



## 相关关键词列表
```{index} NOCV Keywords, EDA Keywords
```

:::{raw} latex
\begingroup
\footnotesize
:::
:::{tabularcolumns} \Y{0.3}\Y{0.2}\Y{0.5}
:::
(tab:NOCV_keywords)=
:::{flat-table} 用于 EDA/ETS-NOCV 分解分析的 `%eda` 块关键词。
:header-rows: 1
* - 关键词
  - 选项
  - 说明
* - `FRAG1`
  - `"<keywords>"`
  - 片段 1 的方法，以简单输入关键词形式给出
* - `FRAG2`
  - `"<keywords>"`
  - 片段 2 的方法，以简单输入关键词形式给出
* - `FRAG1_METHODFILE`
  - `"<filename>"`
  - 含片段 1 方法（简单和/或块）输入的文件
* - `FRAG2_METHODFILE`
  - `"<filename>"`
  - 含片段 2 方法（简单和/或块）输入的文件
* - `FRAG1_C`
  - `0`
  - 分子片段 1 的电荷
* - `FRAG2_C`
  - `0`
  - 分子片段 2 的电荷
* - `FRAG1_M`
  - `1`
  - 分子片段 1 的多重度
* - `FRAG2_M`
  - `1`
  - 分子片段 2 的多重度
* - `FRAG1_SF`
  - `false`
  - 若为 true，翻转片段 1 中未耦合电子的自旋
* - `FRAG2_SF`
  - `false`
  - 若为 true，翻转片段 2 中未耦合电子的自旋
:::
:::{raw} latex
\endgroup
:::


<!-- //Natural Orbitals for Chemical Valence commented out for ORCA 6.0 release, should be put back once ready 
cf. Giovanni Bistoni and Ronald Cardenas Sabando
(sec:spectroscopyproperties.nocv.theory)=
## 化学价自然轨道（Natural Orbitals for Chemical Valence）

在 ORCA 中，化学键可按成键时发生的电子密度重排来分析。
该量定义为加合物 AB 的电子密度与所谓"超分子"电子密度之差，
后者由不相互作用的片段 A 和 B 波函数的反对称化乘积得到。
该电子密度差可通过利用化学价自然轨道
{cite}`nocv2009`（NOCV）的性质来分析，
NOCV 就是相应单电子密度差矩阵的本征矢。
在 ORCA 中，该分析适用于 HF 和 DFT（仅限闭壳层体系），
详见文献 {cite}`altun2018therole`。

NOCV 的生成分三步完成。

第一步，必须对孤立片段（本例中的 A 和 B）执行单点能计算，
并保存相应的 `.gbw` 文件（A.gbw 和 B.gbw）。

第二步，必须用以下命令生成同时含两个片段轨道的 `.gbw` 文件（AB.gbw）：

```orca
orca_mergefrag A.gbw B.gbw AB.gbw
```

第三步，必须用 AB.gbw 文件中的轨道作为初始猜测运行 SCF 计算，
使用 `MORead` 并在 SCF 块中将 `EDA` 关键词设为 `true`。

```orca
! blyp def2-tzvpp verytightscf moread 
%moinp  "AB.gbw"

%scf
EDA true
end

*xyz 0 1
---AB coordinates---
*
```

轨道由此被正确正交化，随后执行分析。
若请求了 NOCV 分析但未给出初始猜测，
则分析将使用 SCF 计算中的默认猜测进行，
这会导致完全不同的结果。

该分析的典型输出如下：

```
-----------------------------------------------------------
ENERGY DECOMPOSITION ANALYSIS OF THE SCF INTERACTION ENERGY
-----------------------------------------------------------

Delta Total Energy  (Kcal/mol) :     -9.998

-----------------------------------------------------------
                     NOCV/ETS analysis                     
-----------------------------------------------------------

  negative eigen. (e)   positive eigen.(e)    DE_k (Kcal/mol) 

    -0.1739401311         0.1739401311       -5.952 
    -0.0607716293         0.0607716293       -1.180 
    -0.0420733869         0.0420733869       -1.278 
    -0.0288977718         0.0288977718       -0.490 
    -0.0207403772         0.0207403772       -0.220 
    -0.0192167553         0.0192167553       -0.219 
    -0.0126925147         0.0126925147       -0.148 
    -0.0077091386         0.0077091386       -0.043 
    -0.0064403861         0.0064403861       -0.329 
    -0.0042036490         0.0042036490       -0.139 
    -0.0000000000         0.0000000000       -0.000 

Consistency Check           Sum_k DE_k :     -9.998 

NOCV were saved in : jobname.nocv.gbw
```

NOCV 本征值与相应的能量贡献一起打印，
后者用 Ziegler 的扩展过渡态（ETS）方法计算 {cite}`nocv2009`。
NOCV 连同相应的本征值存储在 `.gbw` 文件中，可用于后续分析。
"Delta Total Energy" 是参考（超分子）与收敛 SCF 波函数之间的能量差。
在 NOCV/ETS 能量分解方案中，该量也称为"轨道相互作用"（Orbital Interaction）项。
为检验结果相对于积分网格是否收敛，
可将该值与收敛 SCF 波函数的能量同 SCF 迭代第一步之差作比较。
这两个数值应当完全相同。
-->
