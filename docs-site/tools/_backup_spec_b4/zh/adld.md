

<a id="sec:spectroscopyproperties.adldd"></a>
# ADLD(D)：DFT-D 伦敦色散能的原子分解（Atomic Decomposition of DFT-D London Dispersion Energy）

从 6.1 版本开始，ORCA 提供了一种方法，可在多种电子结构技术结合下
以原子分辨率量化伦敦色散能（London dispersion energy，LD），
详见 [baldinelli2024unraveling](../../bibliography.md) 和 [regni2025ADLD](../../bibliography.md)。
该分解方案的一个特例是
[DFT-D](sec:modelchemistries.dispersioncorrections) 伦敦色散能的原子分解
（例如 DFT-D4 对应 ADLD(D4)）。
本方案适用于 D2、D3 和 D4。
基于 DLPNO 的 LED 方法的原始方案记录在
[ADLD(LED) 一节](sec:spectroscopyproperties.led.ad)中。

<a id="sec:spectroscopyproperties.adld.dftd.theory"></a>
## 理论（Theory）

DFT-D 的原子 LD 能通过将每对原子的成对贡献各分一半给该对中的每个原子、
并对所有原子求和来评估：

$$

E_{\text{disp}}^{\text{DFT-D}} (AB) = \sum_{A>B} \epsilon_{AB}^{\text{DFT-D}} = \frac{1}{2} \sum_{A} \sum_{B \neq A} \epsilon_{AB}^{\text{DFT-D}} = \sum_{A} \epsilon_{A}^{\text{DFT-D}} (AB)\qquad \text{(eqn:spectroscopyproperties.adld.dftd.theory.ab)}

$$ 

若计算中包含了三体效应，分解中也会将其纳入：

$$

E_{\text{disp}}^{\text{DFT-D}} (ABC) = \sum_{A>B>C} \epsilon_{ABC}^{\text{DFT-D}} = \frac{1}{6} \sum_{A} \sum_{B \neq A \neq C} \epsilon_{ABC}^{\text{DFT-D}} = \sum_{A} \epsilon_{A}^{\text{DFT-D}} (ABC)\qquad \text{(eqn:spectroscopyproperties.adld.dftd.theory.abc)}

$$ 

<a id="sec:spectroscopyproperties.adld.dftd.basicusage"></a>
### 基本用法（Basic Usage）

在简单输入行中使用 `!ADLD` 关键词即可调用 LD 能的原子分解。

```orca
! PBE D3 def2-TZVP ADLD
```

<a id="sec:spectroscopyproperties.adld.dftd.example"></a>
### 示例（Example）

例如，可用以下输入文件分析水二聚体在 B3LYP-D4/def2-TZVP 水平下的原子色散能：

```orcainput
! B3LYP D4 def2-TZVP ADLD

# H2O dimer geometry optimized at the B3LYP-D4/def2-TZVP level.

* xyz 0 1
  O       0.00736774224494      0.01160693915772      0.01654049355157
  H       0.96923953706804      0.01163512314627     -0.00786387302697
  H      -0.23645852051665      0.94172445362186     -0.01797690491825
  O      -0.98965374142797     -1.29474095640989      2.41552530001642
  H      -0.69837507632022     -0.90508483715064      1.57804074703869
  H      -1.52582551183659     -2.04783550111168      2.15519678840530
*
```

相应的输出文件如下所示。
每个原子的 LD 能以原子单位打印，同时给出总色散能。
对于其他 -D 校正，输出格式保持一致。

```orca
------------------------------------------------------------
      ADLD - Atomic Decomposition of London Dispersion      
------------------------------------------------------------

Atom   Type     Dispersion (a.u.)
---------------------------------
 1      O            -0.000523477  
 2      H            -0.000128807  
 3      H            -0.000128264  
 4      O            -0.000477971  
 5      H            -0.000163561  
 6      H            -0.000120093  

Total dispersion     -0.001542174
```

<a id="sec:spectroscopyproperties.adld.dftd.keywords"></a>
### 关键词（Keywords）

<a id="tab:spectroscopyproperties.ADLD.dftd.keywords.simple"></a>
!!! note "用 DFT-D 校正计算伦敦色散原子分解的简单输入关键词。"
    | 关键词                          | 说明                                             |
    |:--------------------------------|:-------------------------------------------------|
    | `ADLD`                          | 启用 LD 的原子分解                               |

