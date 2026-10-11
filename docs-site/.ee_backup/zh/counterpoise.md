

<a id="sec:essentialelements.counterpoise"></a>
# Counterpoise 校正（Counterpoise Corrections）

<a id="sec:essentialelements.counterpoise.bbcp"></a>
## Boys-Bernardi Counterpoise 校正（BB-CP）

在计算弱分子间相互作用时，总会遇到基组重叠误差（basis set superposition error，BSSE）这个棘手问题。其本质在于：描述二聚体时，A 上的基函数有助于降低片段 B 的能量，反之亦然。因此，由于基组效应，得到的能量会偏向于二聚体的形成。由于这不是我们所希望的，Boys 和 Bernardi 的方法旨在通过估算单体若在二聚体基组下计算时的能量来修正这一缺陷。这将使单体相对于二聚体得到稳定化。该效应可能占相互作用能相当可观的份额，因此应当加以考虑。原始的 Boys-Bernardi 公式中，片段 A 与 B 之间的相互作用能为：

$$

\Delta E = E^{AB}_{AB}(AB) - E^{A}_{A}(A) - E^{B}_{B}(B) - \left[E^{AB}_{A}(AB) - E^{AB}_{A}(A) + E^{AB}_{B}(AB) - E^{AB}_{B}(B)\right]\qquad \text{(eqn:5)}

$$

这里 $E_{X}^{Y} \left( Z \right)$ 表示片段 X 在片段 Y 的优化几何结构下、使用片段 Z 的基组计算得到的能量。因此，总共需要进行以下一系列计算：

1. 用某个基组 Z 优化二聚体和各单体的几何结构。这给出 $E_{AB}^{AB} \left({ AB} \right)$、$E_{A}^{A} \left( A \right)$ 和 $E_{B}^{B} \left( B \right)$。

2. 从优化后的二聚体结构中删除片段 A（或 B），用基组 Z 重新进行单点计算。这给出 $E_{B}^{AB} \left( B \right)$ 和 $E_{A}^{AB} \left( A \right)$。

3. 最后一步是在二聚体几何结构下、用二聚体基组计算 A 和 B 的能量。这给出 $E_{A}^{AB} \left({ AB} \right)$ 和 $E_{B}^{AB} \left({ AB} \right)$。

为了高效完成最后一步，ORCA 中引入了一种特殊记号，允许删除某些原子所带的电子和核电荷、但保留其分配的基组。这个技巧是在原子元素符号后加一个 ":"。下面是在 MP2 级别（冻结核）对水二聚体进行此类计算的示例：

```
#
# Calculations for Boys-Bernardi CP correction
#

# --------------------------------------------
# First the monomer. In principle, you only need
# to run it once, but we keep it for clarity.
# --------------------------------------------
! RHF MP2 cc-pVTZ VeryTightSCF PModel
%id "monomer"
* xyz 0 1
 O     7.405639     6.725069     7.710504
 H     7.029206     6.234628     8.442160
 H     8.247948     6.296600     7.554030
*

$new_job
! RHF MP2 cc-pVTZ VeryTightSCF PModel
%id "monomer"
* xyz 0 1
 O     7.405639     6.725069     7.710504
 H     7.029206     6.234628     8.442160
 H     8.247948     6.296600     7.554030
*

# --------------------------------------------
# now the dimer
# --------------------------------------------
$new_job
! RHF MP2 cc-pVTZ VeryTightSCF PModel
%id "dimer"
* xyz 0 1
O   7.439917   6.726792   7.762120
O   5.752050   6.489306   5.407671
H   7.025510   6.226170   8.467436
H   8.274883   6.280259   7.609894
H   6.313507   6.644667   6.176902
H   5.522285   7.367132   5.103852
*

# --------------------------------------------
# Now the calculations of the monomer at the
# dimer geometry
# --------------------------------------------
$new_job
! RHF MP2 cc-pVTZ VeryTightSCF PModel
%id "monomer_1"

* xyz 0 1
O   7.439917   6.726792   7.762120
H   7.025510   6.226170   8.467436
H   8.274883   6.280259   7.609894
*

$new_job
! RHF MP2 cc-pVTZ VeryTightSCF PModel
%id "monomer_1"
* xyz 0 1
O   5.752050   6.489306   5.407671
H   6.313507   6.644667   6.176902
H   5.522285   7.367132   5.103852
*

# --------------------------------------------
# Now the calculation of the monomer at the
# dimer geometry but with the dimer basis set
# --------------------------------------------
$new_job
! RHF MP2 cc-pVTZ VeryTightSCF PModel
%id "monomer_2"
* xyz 0 1
O   7.439917   6.726792   7.762120
O : 5.752050   6.489306   5.407671
H   7.025510   6.226170   8.467436
H   8.274883   6.280259   7.609894
H : 6.313507   6.644667   6.176902
H : 5.522285   7.367132   5.103852
*

$new_job
! RHF MP2 cc-pVTZ VeryTightSCF PModel
%id "monomer_2"
* xyz 0 1
O : 7.439917   6.726792   7.762120
O   5.752050   6.489306   5.407671
H : 7.025510   6.226170   8.467436
H : 8.274883   6.280259   7.609894
H   6.313507   6.644667   6.176902
H   5.522285   7.367132   5.103852
*
```
由这些计算可以得到用于计算 BB-CP 校正的各能量：

<a id="tab:essentialelements.counterpoise.bbcp"></a>
!!! note "为 Boys-Bernardi counterpoise 校正所计算的能量及最终的二聚化能。"

    | Component                   | E [a.u.]            | E [kcal/mol]  | 
    |:----------------------------|--------------------:|--------------:|
    | $E^{AB}_{AB}(AB)$           | -152.646980         |               |
    | $E^{A}_{A}(A)$              | -76.318651          |               |
    | $E^{B}_{B}(B)$              | -76.318651          |               |
    | $E^{AB}_{A}(AB)$            | -76.320799          |               |
    | $E^{AB}_{A}(A)$             | -76.318635          |               |
    | $E^{AB}_{B}(AB)$            | -76.319100          |               |
    | $E^{AB}_{B}(B)$             | -76.318605          |               |
    | $\Delta E_{dim.}$           | -0.009677           | -6.07         |
    | $\Delta E_{BB-CP}$          | 0.002659            | 1.67          |
    | $\Delta E_{dim., corr.}$    | -0.007018           | -4.40         |

在本例中，我们算得的 BSSE 校正为 1.67 kcal/mol。

也可以用 `GhostFrags` 关键字把整个片段设为幽灵原子（ghost atoms），如下所示。定义片段的不同方式见章节 [sec:essentialelements.coordinates](#sec:essentialelements.coordinates)。

```
! MP2 cc-pVTZ VeryTightSCF PModel
* xyz 0 1
  O   7.439917   6.726792   7.762120
  O   5.752050   6.489306   5.407671
  H   7.025510   6.226170   8.467436
  H   8.274883   6.280259   7.609894
  H   6.313507   6.644667   6.176902
  H   5.522285   7.367132   5.103852
*
%frag
  Definition
    1 {0 2 3} end
    2 {1 4 5} end
  end
end
%geom
  GhostFrags {1} end # space-separated list and X:Y ranges accepted
end
```

从 ORCA 6.0 起，我们支持带 counterpoise 校正的几何优化（使用解析梯度）。这为使用中等基组获得精确的非共价复合物几何结构（而不仅仅是相互作用能）开辟了道路。要使用这一功能，不应简单地在上述输入文件中添加 `!Opt`，而应使用 ORCA [复合脚本仓库（Compound Script repository）](https://github.com/ORCAQuantumChemistry/CompoundScripts/blob/main/GeometryOptimization/BSSEOptimization.cmp)中提供的专用复合脚本 `BSSEOptimization.cmp`。详细用法见该复合脚本中的注释。

<a id="sec:essentialelements.counterpoise.gcp"></a>
## 几何 Counterpoise 校正（Geometrical Counterpoise Correction, gCP）

gCP 校正 [KrusegCP](../../bibliography.md) 的核心思想是向分子体系的能量添加一个半经验校正 $\Delta E_{\text{gCP} }$，以消除 BSSE 造成的虚假过强结合效应。gCP 采用原子校正，因此也有能力校正分子内 BSSE。其参数化方式使其在分子间情形下近似于 Boys-Bernardi counterpoise（CP）校正 $\Delta E_{CP}$，即

$$

\Delta E_{CP}\approx \Delta E_{\text{gCP} }\qquad \text{(eqn:ecp-gcp)}

$$

其中例如对于络合反应 $A+B\to C$，我们的校正由下式给出

$$

\Delta E_{\text{gCP} }=E_{\text{gCP} }(C)-E_{\text{gCP} }(A)-E_{\text{gCP} }(B)\qquad \text{(eqn:de-gcp)}

$$

在实践中，$E_{\text{gCP} }$ 可以简单地加到 HF/DFT 能量上

$$

E_{\text{total}}  =  E_{\text{HF/DFT}} + E_{\text{gCP} }\qquad \text{(eqn:etot-gcp)}

$$

这在 ORCA 中是自动完成的（`FINAL SINGLE POINT ENERGY` 包含 gCP 校正）。

对所有原子 $N$ 求和的 gCP 校正核心方程为：

$$

E_{\text{gCP} }  =  \sigma \cdot \sum_{a}^{N} \sum_{b \neq a}^{N}  e_a^{\text{miss} }  \cdot f_{\text{dec} }(R_{ab})\qquad \text{(eqn:gcp)}

$$

其中能量 $e_a^{\text{miss} }$ 是所选目标基组不完全性（通常较小）的度量，$f_{\text{dec} }(R_{ab})$ 是依赖于原子间距离 $R_{ab}$ 的衰减函数。标度因子 $\sigma$ 是每个 `method/basis set` 组合所需的 4 个参数之一。更多细节见 gCP 原始文献 [KrusegCP](../../bibliography.md)。

gCP 的解析梯度可用于几何优化。由于其半经验性质，即使对于非常大的体系，校正也能在几秒内算完。

<a id="sec:essentialelements.counterpoise.gcp.basicusage"></a>
### 基本用法（Basic Usage）
gCP 校正可通过 `!GCP(level)` 关键字调用，其中 `level` 是方法（Hartree-Fock，`HF`；或密度泛函理论，`DFT`）与基组定义的组合。可用基组及相应关键字见 [tab:essentialelements.counterpoise.gcp](#tab:essentialelements.counterpoise.gcp)。例如，在使用 def2-SV(P) 基组的 B3LYP 计算中，可通过如下输入调用 gCP：

```orca
! B3LYP def2-SV(P) GCP(DFT/SV(P))
```
gCP 输入也可以在输入文件的 `%method` 模块块中定义：

```orca
! B3LYP def2-SV(P)

%method
  DoGCP       true
  GCPMETHOD   dft/sv(p)
end
```

<a id="tab:essentialelements.counterpoise.gcp"></a>
!!! note "已参数化基组概览。`!GCP(level)` 中的 `level` 关键字是 `HF` 或 `DFT` 与 `basis set` 关键字的组合。有效输入例如：`!GCP(HF/MINIS)`、`!GCP(DFT/LANL)`、`!GCP(HF/TZ)`、`!GCP(DFT/631GD)`、$\ldots$"

    | Parametrized basis set     | Definition          | HF  | DFT | 
    |:---------------------------|:--------------------|:---:|:---:|
    | MINIS                      | MINIS               | yes | yes |
    | SV                         | SV                  | yes | yes |
    | 6-31G(d)                   | 631GD               | yes | yes |
    | 6-31G(d) + LANL2DZ (Sc-Zn) | LANL                | no  | yes |
    | def2-SV(P)                 | SV(P)               | no  | yes |
    | def2-SVP                   | SVP                 | yes | yes |
    | def2-TZVP                  | TZ                  | yes | yes |

在所有打印级别下，gCP 程序的警告都会被打印出来。使用默认打印级别时，额外的输出只有 `FINAL SINGLE POINT ENERGY` 之前的最终 gCP 校正。使用 `!LargePrint` 或 `%output Print[P_gCP] 2 end` 会给出 gCP 的 `level`、上述 4 个参数以及计算得到的校正值。还可以指定更高的打印级别以获取更多细节（下文有更多说明）。

可能会发出若干警告和提示。第五周期及更高周期的元素按其第四周期的同族元素处理——例如 Sn 用与 Ge 相同的参数处理。若出现这种情况，会打印一条提示。若 SCF 计算所用基组与请求的 gCP 计算基组不匹配，也会打印另一条提示。例如，下面这个四甲基锡的输入

```orca
! HF def2-SVP GCP(HF/MINIS)
*xyzfile 0 1 tetramethyltin.xyz
```

应当用 Ge 的参数代替 Sn，并且 ORCA 中的基组（def2-SVP）与 gCP 的基组（MINIS）之间应当存在不匹配。输出确实如下：

```orca
 ** NOTE ** -> element sn will be treated as ge
NOTIFICATION: Different basis set in ORCA and otool_gcp:
ORCA: 142  gCP: 32 
If you are NOT using ECPs, check your basis set inputs!
------------------   -----------------
gCP correction             0.073031339
------------------   -----------------
```

由于轻微的不匹配只会带来很小的误差，因此允许所用基组之间存在不匹配。不过对这类结果仍应谨慎——请自行判断！这也允许在使用未参数化基组的计算中使用 gCP。但在这种情况下，基函数数目和指数应当非常接近！

需要注意的是，取决于所用的 gCP `level`，有些元素可能没有参数化。如果大分子中只有少数原子处理不精确或完全未处理，预计误差不大。要检查所用的全部参数以及各原子的贡献，请指定打印级别 `%output Print[P_gCP] 3 end`。例如，上述四甲基锡输入在该打印级别下的输出如下：

```orca
------------------------------------------------------------------------------
                                                                              
                  g C P  - geometrical counterpoise correction     
                                                                              
------------------------------------------------------------------------------
Method:  hf/minis 
  
 ** NOTE ** -> element sn will be treated as ge
Parameters:   sigma        eta         alpha        beta 
              0.1290      1.1526      1.1549       1.1763 
Nbf:   32  
NAtoms:   17  
  
gCP element parameters: 
  elem   emiss   nbas    elem   emiss   nbas    elem   emiss   nbas
    h    0.04240    1      he   0.02832    1      li   0.25266    2
    be   0.19720    2      b    0.22424    5      c    0.27995    5
    n    0.35791    5      o    0.47901    5      f    0.63852    5
    ne   0.83235    5      na   1.23292    6      mg   1.34339    6
    al   1.44828    9      si   1.61336    9      p    1.76814    9
    s    1.99201    9      cl   2.23311    9      ar   2.49323    9
    k    3.02964   10      ca   3.38998   10      sc   0.00000    0
    ti   0.00000    0      v    0.00000    0      cr   0.00000    0
    mn   0.00000    0      fe   0.00000    0      co   0.00000    0
    ni   0.00000    0      cu   0.00000    0      zn   0.00000    0
    ga   0.00000    0      ge   0.00000    0      as   0.00000    0
    se   0.00000    0      br   0.00000    0      kr   0.00000    0
  
      #     ON  sites    Nvirt           Emiss    BSSE [kcal/mol]
      1      6     15      2.0          0.2799         10.0090
      2     32     16    -16.0          0.0000          0.0000
      3      6     15      2.0          0.2799         10.0084
      4      6     15      2.0          0.2799         10.0095
      5      6     15      2.0          0.2799         10.0083
      6      1     15      0.5          0.0424          0.4827
      7      1     15      0.5          0.0424          0.4828
      8      1     15      0.5          0.0424          0.4828
      9      1     15      0.5          0.0424          0.4827
     10      1     15      0.5          0.0424          0.4827
     11      1     15      0.5          0.0424          0.4827
     12      1     15      0.5          0.0424          0.4828
     13      1     15      0.5          0.0424          0.4827
     14      1     15      0.5          0.0424          0.4828
     15      1     15      0.5          0.0424          0.4827
     16      1     15      0.5          0.0424          0.4827
     17      1     15      0.5          0.0424          0.4827
Egcp:       0.0730313386 a.u.
NOTIFICATION: Different basis set in ORCA and otool_gcp:
ORCA: 142  gCP: 32 
If you are NOT using ECPs, check your basis set inputs!
------------------   -----------------
gCP correction             0.073031339
------------------   -----------------
```

由此可以看出，Sn 原子（原子贡献列表中的原子 2）没有贡献，因为它的 `Emiss` 为零（对于给定的 gCP `level` 未参数化）。查看 `gCP element parameters` 部分也可以确认这一点：对于 `!GCP(HF/MINIS)`，其中列出的 Sn 的 `emiss` 为零。用 `!GCP(HF/SVP)` 重新运行本例，Sn 就有了贡献，如下列输出所示。注意该计算的基组不匹配也小得多，因此两者中它应该是更精确的 gCP 校正。

```orca
------------------------------------------------------------------------------
                                                                              
                  g C P  - geometrical counterpoise correction     
                                                                              
------------------------------------------------------------------------------
Method:  hf/svp 
  
 ** NOTE ** -> element sn will be treated as ge
Parameters:   sigma        eta         alpha        beta 
              0.2054      1.3157      0.8136       1.2572 
Nbf:   148  
NAtoms:   17  
  
gCP element parameters: 
  elem   emiss   nbas    elem   emiss   nbas    elem   emiss   nbas
    h    0.00811    5      he   0.00805    5      li   0.11358    9
    be   0.02837    9      b    0.04937   14      c    0.05538   14
    n    0.07278   14      o    0.10031   14      f    0.13327   14
    ne   0.17360   14      na   0.18114   15      mg   0.12556   18
    al   0.16719   18      si   0.14984   18      p    0.14540   18
    s    0.16431   18      cl   0.18299   18      ar   0.20567   18
    k    0.20096   24      ca   0.29966   24      sc   0.32599   31
    ti   0.30549   31      v    0.29172   31      cr   0.29380   31
    mn   0.29179   31      fe   0.29673   31      co   0.30460   31
    ni   0.24204   31      cu   0.35419   31      zn   0.35072   31
    ga   0.35002   32      ge   0.34578   32      as   0.34953   32
    se   0.36731   32      br   0.38201   32      kr   0.39971   32
  
      #     ON  sites    Nvirt           Emiss    BSSE [kcal/mol]
      1      6     16     11.0          0.0554          2.5093
      2     32     16     16.0          0.3458          6.8274
      3      6     16     11.0          0.0554          2.5092
      4      6     16     11.0          0.0554          2.5094
      5      6     16     11.0          0.0554          2.5092
      6      1     16      4.5          0.0081          0.1703
      7      1     16      4.5          0.0081          0.1703
      8      1     16      4.5          0.0081          0.1703
      9      1     16      4.5          0.0081          0.1703
     10      1     16      4.5          0.0081          0.1703
     11      1     16      4.5          0.0081          0.1703
     12      1     16      4.5          0.0081          0.1703
     13      1     16      4.5          0.0081          0.1703
     14      1     16      4.5          0.0081          0.1703
     15      1     16      4.5          0.0081          0.1703
     16      1     16      4.5          0.0081          0.1703
     17      1     16      4.5          0.0081          0.1703
Egcp:       0.0301322002 a.u.
NOTIFICATION: Different basis set in ORCA and otool_gcp:
ORCA: 142  gCP: 148 
If you are NOT using ECPs, check your basis set inputs!
------------------   -----------------
gCP correction             0.030132200
------------------   -----------------
```

!!! note "一般性建议（General advice）"

    -   小基组不仅带来大的 BSSE，还存在普遍的缺陷。这些效应并不总是能清楚地区分开来。

    -   如果计算资源允许，总是优先选用大基组（三重-$\zeta$ 及以上）。

    -   gCP 只对稍大的分子才有意义

    -   gCP 应当始终与色散校正一起使用。gCP 与 D3 或 D4 的组合经过了充分测试，gCP 与 NL 的组合也工作良好（见章节 [sec:modelchemistries.dispersioncorrections](#sec:modelchemistries.dispersioncorrections)）。

    -   已有研究表明，常用的 B3LYP 与 6-31G(d) 组合可以通过 DFT-D3 和 gCP 得到显著改进 [KruseB3LYPgCPD3](../../bibliography.md)。为方便起见，已定义关键字 `!B3LYP-gCP-D3/6-31G*`。它等价于 `!B3LYP 6-31G* D3BJ GCP(DFT/631GD)`。

!!! note "技术说明（Technical Notes）"
    -   `!GCP(HF/MINIS)` 会自动设置重新拟合的 D3 参数，如 gCP 原始文献中所建议。

    -   gCP 方法通过一个名为 **otool_gcp** 的外部工具实现，该工具基于文献中所用的原始 Fortran 程序。因此，`otool_gcp` 二进制程序也可以直接通过命令行调用（`otool_gcp -h` 给出选项概览）。

    -   也可以用 `!GCP(FILE)` 关键字读取外部参数文件（`$HOME/.gcppar`）。更多信息请参阅 Grimme 课题组提供的 gcp 程序手册（[gCP manual](https://www.chemie.uni-bonn.de/grimme/de/software/gcp/mangcp.pdf)）。

    -   计算过程中，ORCA 会写一些临时输出文件：`BASENAME.gcp.in.tmp` 和 `BASENAME.gcp.out.tmp` 分别包含 `otool_gcp` 的输入和输出。

<a id="sec:essentialelements.counterpoise.gcp.keywords"></a>
### 关键字（Keywords）

<a id="tab:essentialelements.counterpoise.gcp.keywords.simple"></a>
!!! note "gCP 校正的简单输入关键字。"
    | Keyword                         | Description                                                          |
    |:--------------------------------|:---------------------------------------------------------------------|
    | `GCP(<level>)`                  | 为由 `<level>` 定义的指定理论级别激活 gCP 校正                                 |

<a id="tab:essentialelements.counterpoise.gcp.keywords.block"></a>
!!! note "gCP 校正的 `%method` 模块块输入关键字与选项。"
    | Keyword                         | Option            | Description                                      |
    |:--------------------------------|:------------------|:-------------------------------------------------|
    | `DoGCP`                         | `true`/`false`    | 激活/关闭 gCP 校正                                   |
    | `GCPMETHOD`                     | `<level>`         | 定义 gCP 级别字符串，例如 `dft/svp`                       |
    |                                 | `hf/minis`        | HF 与 MINIS 基组的参数化                               |
    |                                 | `hf/sv`           | HF 与 SV 基组的参数化                                  |
    |                                 | `hf/631gd`        | HF 与 6-31G(d) 基组的参数化                             |
    |                                 | `hf/svp`          | HF 与 def2-SVP 基组的参数化                             |
    |                                 | `hf/tz`           | HF 与 def2-TZVP 基组的参数化                            |
    |                                 | `dft/minis`       | DFT 与 MINIS 基组的参数化                              |
    |                                 | `dft/sv`          | DFT 与 SV 基组的参数化                                 |
    |                                 | `dft/631gd`       | DFT 与 6-31G(d) 基组的参数化                            |
    |                                 | `dft/lanl`        | DFT 与混合 6-31G(d) + LANL2DZ (Sc-Zn) 基组的参数化          |
    |                                 | `dft/sv(p)`       | DFT 与 def2-SV(P) 基组的参数化                          |
    |                                 | `dft/svp`         | DFT 与 def2-SVP 基组的参数化                            |
    |                                 | `dft/tz`          | DFT 与 def2-TZVP 基组的参数化                           |
    |                                 | `file`            | 从外部参数文件 `$HOME/.gcppar` 读取参数                    |
    | `GCP.D3MINIS`                   | `true`/`false`    | 对 HF/MINIS 使用特殊的 DFT-D3 重新拟合（默认=true）            |

