<a id="sec:essentialelements.fragmentation"></a>
# 片段指定（Fragment Specification）

计算中的原子可以被分组为特定的*片段（fragments）*，片段有多种用途。片段定义可用于[分配基组和 ECP](#sec:essentialelements.basisset.fragments)、在[布居分析部分](#sec:spectroscopyproperties.pop.lsa)组织输出，以及启用[片段约束优化](#sec:structurereactivity.geomopt.constrainedfragment)和[刚体优化（Rigid Body Optimization）](#sec:structurereactivity.optimization.rigidbody)等功能。它们还用于[局域能量分解](#sec:spectroscopyproperties.led)和[多层级计算](#sec:modelchemistries.mdci.multilevel)。

<a id="sec:essentialelements.fragmentation.Inputdef"></a>
## 在输入文件中定义片段

有三种方式可以通过输入文件把原子分配到片段。第一种方法是在坐标部分的原子符号后直接放置 `(n)`，把特定原子分配到特定片段。

```orca
*xyz -2 2
 Cu(1)  0.00  0.00  0.00
 Cl(2)  2.25  0.00  0.00
 Cl(2) -2.25  0.00  0.00
 Cl(2)  0.00  2.25  0.00
 Cl(2)  0.00 -2.25  0.00
*
```

本例中使用片段功能把分子划分为"金属"和"配体"两个片段，程序相应地会打印金属和配体的电荷与布居。

```orca
----------------------------------------------
CARTESIAN COORDINATES OF FRAGMENTS (ANGSTROEM)
----------------------------------------------

 FRAGMENT 1
  Cu    0.000000    0.000000    0.000000

 FRAGMENT 2
  Cl    2.250000    0.000000    0.000000
  Cl   -2.250000    0.000000    0.000000
  Cl    0.000000    2.250000    0.000000
  Cl    0.000000   -2.250000    0.000000

...

----------------------------------------------
MULLIKEN FRAGMENT CHARGES AND SPIN POPULATIONS
----------------------------------------------
 Fragment   0 :   0.752589     0.842580
 Fragment   1 :  -2.752589     0.157420
Sum of fragment charges         :   -2.0000000
Sum of fragment spin populations:    1.0000000

...

--------------------------------------------
LOEWDIN FRAGMENT CHARGES AND SPIN POPULATONS
--------------------------------------------
 Fragment   0 :   0.222028     0.851552
 Fragment   1 :  -2.222028     0.148448

```

另外，也可以用 `%coords` 模块块以同样的方式定义片段——在原子符号后直接放置 `(n) `。

```orca
%coords
 CTyp   xyz  # the type of coordinates xyz or internal
 Charge -2   # the total charge of the molecule
 Mult   2    # the multiplicity = 2S+1
 coords
    Cu(1)  0.00  0.00  0.00
    Cl(2)  2.25  0.00  0.00
    Cl(2) -2.25  0.00  0.00
    Cl(2)  0.00  2.25  0.00
    Cl(2)  0.00 -2.25  0.00
 end
end
```

!!! note "重要"
    :class: important
    - 当所有原子都被显式分配到片段时，片段编号必须从 1 开始并使用连续整数。不连续或不正确的编号可能导致错误。

    - 如果有任何原子未被分配（或被显式分配到片段 0），它将按照[自动片段划分](#sec:essentialelements.fragmentation.inputfile)一节中描述的片段划分流程自动分配到某个片段。在这种情况下——即只有一部分原子被手动分配到片段——不需要使用连续的片段编号。但输入中指定的最大片段编号必须小于手动与自动流程组合所产生的片段总数。如果这一条件不满足，ORCA 会自动按升序从 1 开始重新排列所有片段编号。

最后，第三种定义片段的方式是在 `%frag` 模块块内使用 `Definition`。在这种方案中，片段编号写在最前面，随后是用花括号 `{}` 括起、以 `end` 结尾的原子列表（原子从 0 开始编号）。连续的原子也可以用 `initial_atom`:`final_atom` 记号指定。

```orca
*xyz -2 2
 Cu  0.00  0.00  0.00
 Cl  2.25  0.00  0.00
 Cl -2.25  0.00  0.00
 Cl  0.00  2.25  0.00
 Cl  0.00 -2.25  0.00
*

%frag
 Definition
  1 {0} end    # atom 0 for fragment 1
  2 {1:4} end  # atoms 1 to 4 for fragment 2
 end
end
```

```orca
*xyz -2 2
 Cl  2.25  0.00  0.00
 Cl -2.25  0.00  0.00
 Cu  0.00  0.00  0.00
 Cl  0.00  2.25  0.00
 Cl  0.00 -2.25  0.00
*

%frag
 Definition
  1 {2} end        # atom 2 for fragment 1
  2 {0:1 3:4} end  # atoms 0, 1, 3, and 4 for fragment 2
 end
end
```

!!! note "注意"
    :class: note
    -   对于最后一种选项（`Definition`），`%frag` 模块块必须写在坐标部分之后。

    -   `%frag Definition` 也适用于通过外部文件定义的坐标。

<a id="sec:essentialelements.fragmentation.inputfile"></a>
## 自动片段划分（Automatic Fragmentation）

从 ORCA 6.1 起，引入了一套自动片段划分算法，用于自动识别并将原子分组为片段。

当输入文件中包含 `%frag` 模块块，或只有部分原子被手动分配到片段时，就会触发自动片段划分流程。

自动片段划分由一组流程完成，用户可在 `%frag` 模块块中选择。每个流程都会尝试在尚未分配的原子中识别新的片段。例如，考虑下面的例子：前 11 个原子属于一个丙烷分子，最后三个属于一个水分子。`FragProc` 中的 `Water` 流程把最后三个原子识别为水分子并分配到第一个片段，而 `FunctionalGroups` 流程则检测并将丙烷的 CH<sub>3</sub> 和 CH<sub>2</sub> 基团分配为片段 2 到 4。

<a id="sec:essentialelements.fragmentation.intlibex"></a>
```orca
%frag
   FragProc Water, FunctionalGroups
end

* xyz 0 1
 C     0.000000     1.270000    -0.260000
 C     0.000000    -0.000000     0.580000
 C     0.000000    -1.270000    -0.260000
 H    -0.890000     1.320000    -0.910000
 H     0.890000     1.320000    -0.910000
 H     0.000000     2.180000     0.370000
 H     0.880000    -0.000000     1.250000
 H    -0.880000    -0.000000     1.250000
 H     0.890000    -1.320000    -0.910000
 H     0.000000    -2.180000     0.370000
 H    -0.880000    -1.300000    -0.910000
 H    -0.920000     0.850000    -2.430000
 O    -1.690000     0.830000    -3.000000
 H    -1.640000     1.630000    -3.510000
*
```

```orca
  ----------------------------------------------
  CARTESIAN COORDINATES OF FRAGMENTS (ANGSTROEM)
  ----------------------------------------------
  
   FRAGMENT 1
    H    -0.920000    0.850000   -2.430000
    O    -1.690000    0.830000   -3.000000
    H    -1.640000    1.630000   -3.510000
  
   FRAGMENT 2
    C     0.000000    1.270000   -0.260000
    H    -0.890000    1.320000   -0.910000
    H     0.890000    1.320000   -0.910000
    H     0.000000    2.180000    0.370000
  
   FRAGMENT 3
    C     0.000000   -1.270000   -0.260000
    H     0.890000   -1.320000   -0.910000
    H     0.000000   -2.180000    0.370000
    H    -0.880000   -1.300000   -0.910000
  
   FRAGMENT 4
    C     0.000000   -0.000000    0.580000
    H     0.880000   -0.000000    1.250000
    H    -0.880000   -0.000000    1.250000

```
这种自动片段划分给出的结果与下面所示的手动片段定义相同，而无需查看几何结构并手动分配片段。

```orca
%frag
 Definition
 1 { 11:13} end  # water
 2 { 0 3:5} end  # CH3
 3 { 2 8:10} end # CH3
 4 { 1 6:7} end  # CH2
 end
end
```

!!! note "注意"
    :class: note
    -   在[输入文件](#sec:essentialelements.fragmentation.Inputdef)中定义的任何片段优先于自动分配。
    -   ORCA 的 `FragProc` 最多支持 10 个流程，完整列表见 [tab:essentialelements.fragmentationprocedures](#tab:essentialelements.fragmentationprocedures) 和 [tab:essentialelements.delprocedures](#tab:essentialelements.delprocedures)。
    -   当存在未分配到片段的原子时，[约束片段](#sec:structurereactivity.geomopt.constrainedfragment)不会自动启用自动片段划分。但可以通过在输入文件中包含 `%frag` 模块块来激活自动片段划分。

ORCA 提供了 30 多种 `FragProc` 方法，可以组合成列表，为各种目的生成片段。下面是对各个流程的说明和示例。

<a id="sec:essentialelements.fragmentation.inputfile.connectivity"></a>
### 自动片段划分：连通性（Connectivity）

`FragProc Connectivity` 把由化学键连接的原子分组到一起，化学键基于原子半径估计。在下面的例子中，前九个原子属于一个二甲醚分子，被自动检测并分配到一个片段；最后三个原子——属于一个水分子——被分配到第二个片段。
 
```orca
%frag
  PrintLevel 3
  FragProc Connectivity
end

*xyz 0 1
 O     0.000000     0.000000     0.000000
 C     0.000000     0.000000     1.380000
 C     1.300000     0.000000    -0.460000
 H    -0.500000     0.870000     1.740000
 H    -0.500000    -0.870000     1.740000
 H     1.000000     0.000000     1.740000
 H     1.300000     0.000000    -1.530000
 H     1.800000     0.870000    -0.100000
 H     1.800000    -0.870000    -0.100000
 H    -1.840000     0.000000    -0.650000
 O    -2.440000     0.000000     0.080000
 H    -3.300000     0.000000    -0.300000
*
```

在这种情况下，自动片段划分工具的输出表明两个片段由 `Connectivity` 流程分配。

```orca
------------------------------------------
 Assigned Fragment: 1 
------------------------------------------
  Name: Connectivity:0 Method: Connectivity 
  Natoms: 9 Charge: 0 Mult: 1 

 0 O     0.000000    0.000000    0.000000 
 1 C     0.000000    0.000000    1.380000 
 2 C     1.300000    0.000000   -0.460000 
 3 H    -0.500000    0.870000    1.740000 
 4 H    -0.500000   -0.870000    1.740000 
 5 H     1.000000    0.000000    1.740000 
 6 H     1.300000    0.000000   -1.530000 
 7 H     1.800000    0.870000   -0.100000 
 8 H     1.800000   -0.870000   -0.100000 
------------------------------------------

------------------------------------------
 Assigned Fragment: 2 
------------------------------------------
  Name: Connectivity:1 Method: Connectivity 
  Natoms: 3 Charge: 0 Mult: 1 

 9 H    -1.840000    0.000000   -0.650000 
 10 O    -2.440000    0.000000    0.080000 
 11 H    -3.300000    0.000000   -0.300000 
------------------------------------------
```

每个片段划分流程只适用于尚未分配到片段的原子。因此，基于连通性的片段划分会忽略与已在输入文件中或由先前 `FragProc` 分配的原子之间的任何键。

例如，在上例中如果把氧原子在输入文件中手动分配到片段 1，则该手动分配优先于 `FragProc Connectivity`。结果会创建四个片段：一个包含手动分配的氧原子的片段、两个 CH<sub>3</sub> 基团和一个水分子。

```orca
%frag
  PrintLevel 3
  FragProc Connectivity
end

*xyz 0 1
 O(1)  0.000000     0.000000     0.000000
 C     0.000000     0.000000     1.380000
 C     1.300000     0.000000    -0.460000
 H    -0.500000     0.870000     1.740000
 H    -0.500000    -0.870000     1.740000
 H     1.000000     0.000000     1.740000
 H     1.300000     0.000000    -1.530000
 H     1.800000     0.870000    -0.100000
 H     1.800000    -0.870000    -0.100000
 H    -1.840000     0.000000    -0.650000
 O    -2.440000     0.000000     0.080000
 H    -3.300000     0.000000    -0.300000
*
```

自动片段划分工具的输出表明，第一个片段由 `Orca_Input` 流程分配，其余三个片段由 `Connectivity` 流程分配。

```orca
===================================================
Tfragmentator: Fragmenting by Orca_input
===================================================

------------------------------------------
 Assigned Fragment: 1
------------------------------------------
  Name: User-defined:0 Method: Orca_input
  Natoms: 1 Charge: 0 Mult: 1 InputId: 1

 0 O     0.000000    0.000000    0.000000
------------------------------------------

===================================================
Tfragmentator: Fragmenting by Connectivity
===================================================

------------------------------------------
 Assigned Fragment: 2 
------------------------------------------ 
  Name: Connectivity:1 Method: Connectivity
  Natoms: 4 Charge: 0 Mult: 1 

 1 C     0.000000    0.000000    1.380000 
 3 H    -0.500000    0.870000    1.740000 
 4 H    -0.500000   -0.870000    1.740000 
 5 H     1.000000    0.000000    1.740000 
------------------------------------------

------------------------------------------
 Assigned Fragment: 3 
------------------------------------------
  Name: Connectivity:2 Method: Connectivity 
  Natoms: 4 Charge: 0 Mult: 1 

 2 C     1.300000    0.000000   -0.460000 
 6 H     1.300000    0.000000   -1.530000 
 7 H     1.800000    0.870000   -0.100000 
 8 H     1.800000   -0.870000   -0.100000
------------------------------------------

------------------------------------------
 Assigned Fragment: 4
------------------------------------------
  Name: Connectivity:3 Method: Connectivity
  Natoms: 3 Charge: 0 Mult: 1

 9 H    -1.840000    0.000000   -0.650000
 10 O    -2.440000    0.000000    0.080000
 11 H    -3.300000    0.000000   -0.300000
------------------------------------------

```

<a id="sec:essentialelements.fragmentation.inputfile.atnoas"></a>
### 自动片段划分：Atomic 与 NotAssigned

`FragProc Atomic` 和 `FragProc NotAssigned` 是终止流程。`FragProc Atomic` 把每个先前未分配的原子各自作为一个独立片段，而 `FragProc NotAssigned` 把所有剩余未分配的原子分配到同一个片段。

与其他 `FragProc` 方法类似，自动片段划分工具的输出表明使用了 `Atomic` 或 `Not_assigned` 流程来生成相应片段。

```orca
%frag
  PrintLevel 3
  FragProc Atomic
end

*xyz 0 1
 O(1)  0.000000     0.000000     0.000000
 C     0.000000     0.000000     1.380000
 C     1.300000     0.000000    -0.460000
 H    -0.500000     0.870000     1.740000
 H    -0.500000    -0.870000     1.740000
 H     1.000000     0.000000     1.740000
 H     1.300000     0.000000    -1.530000
 H     1.800000     0.870000    -0.100000
 H     1.800000    -0.870000    -0.100000
 H    -1.840000     0.000000    -0.650000
 O    -2.440000     0.000000     0.080000
 H    -3.300000     0.000000    -0.300000
*
```

```orca
===================================================
Tfragmentator: Fragmenting by Orca_input
===================================================

------------------------------------------
 Assigned Fragment: 1
------------------------------------------
  Name: User-defined:0 Method: Orca_input
  Natoms: 1 Charge: 0 Mult: 1 InputId: 1

 0 O     0.000000    0.000000    0.000000
------------------------------------------

===================================================
Tfragmentator: Fragmenting by Atomic
===================================================

------------------------------------------
 Match: 1, Assigned Fragment: 2
------------------------------------------
  Name: C  Method: Atomic
  Natoms: 1 Charge: 0 Mult: 1

 1 C     0.000000    0.000000    1.380000
------------------------------------------

------------------------------------------
 Match: 2, Assigned Fragment: 3
------------------------------------------
  Name: C  Method: Atomic
  Natoms: 1 Charge: 0 Mult: 1

 2 C     1.300000    0.000000   -0.460000
------------------------------------------

...

------------------------------------------
 Match: 11, Assigned Fragment: 12
------------------------------------------
  Name: H  Method: Atomic
  Natoms: 1 Charge: 0 Mult: 1

 11 H    -3.300000    0.000000   -0.300000
------------------------------------------

```

```orca
%frag
  PrintLevel 3
  FragProc NotAssigned
end

*xyz 0 1
 O(1)  0.000000     0.000000     0.000000
 C     0.000000     0.000000     1.380000
 C     1.300000     0.000000    -0.460000
 H    -0.500000     0.870000     1.740000
 H    -0.500000    -0.870000     1.740000
 H     1.000000     0.000000     1.740000
 H     1.300000     0.000000    -1.530000
 H     1.800000     0.870000    -0.100000
 H     1.800000    -0.870000    -0.100000
 H    -1.840000     0.000000    -0.650000
 O    -2.440000     0.000000     0.080000
 H    -3.300000     0.000000    -0.300000
*
```

```orca
===================================================
Tfragmentator: Fragmenting by Orca_input
===================================================

------------------------------------------
 Assigned Fragment: 1
------------------------------------------ 
  Name: User-defined:0 Method: Orca_input 
  Natoms: 1 Charge: 0 Mult: 1 InputId: 1

 0 O     0.000000    0.000000    0.000000
------------------------------------------

===================================================
Tfragmentator: Setting not assigned atoms to a fragment
===================================================

------------------------------------------
 Assigned Fragment: 1 
------------------------------------------
  Name: Not Assigned Method: Not_assigned
  Natoms: 11 Charge: 0 Mult: 1 

 1 C     0.000000    0.000000    1.380000 
 2 C     1.300000    0.000000   -0.460000
 3 H    -0.500000    0.870000    1.740000
 4 H    -0.500000   -0.870000    1.740000
 5 H     1.000000    0.000000    1.740000 
 6 H     1.300000    0.000000   -1.530000  
 7 H     1.800000    0.870000   -0.100000
 8 H     1.800000   -0.870000   -0.100000
 9 H    -1.840000    0.000000   -0.650000  
 10 O    -2.440000    0.000000    0.080000 
 11 H    -3.300000    0.000000   -0.300000
------------------------------------------
 
```

!!! note "注意"
    :class: note
    -   `FragProc NotAssigned` 总是在所有 `FragProc` 流程的最后应用，以确保没有原子遗漏片段分配。

<a id="sec:essentialelements.fragmentation.inputfile.intlib"></a>
### 自动片段划分：内部库（Internal Libraries）

ORCA 包含一系列内部库，其中含有许多常见分子结构的定义。在所有情况下，结构识别都是对由笛卡尔坐标构建的分子图应用 VF2 子图同构算法完成的。

利用内部库的可用片段划分流程列于 [tab:essentialelements.fragmentationprocedures](#tab:essentialelements.fragmentationprocedures)。

<a id="tab:essentialelements.fragmentationprocedures"></a>
!!! note "片段检测的简单输入关键字。"
    :header-rows: 1
    :class: longtable
    :class: footnotesize

| 项目 | 内容 |
| --- | --- |
| **Fragment detection Keyword** | 无 |

      - Description

| 项目 | 内容 |
| --- | --- |
| **`FunctionalGroups`** | 无 |

      - 包含最常见有机官能团的列表。

| 项目 | 内容 |
| --- | --- |
| **`Aminoacids`** | 无 |

      - 包含所有氨基酸的列表，涵盖所有常见质子化状态，但不包括两性离子形式。

| 项目 | 内容 |
| --- | --- |
| **`AABackbone`** | 无 |

      - 包含氨基酸主链检测的片段定义。

| 项目 | 内容 |
| --- | --- |
| **`Backbone`** | 无 |

      - 先执行 `AABackbone`，随后把所有片段合并为一个蛋白质主链片段。

| 项目 | 内容 |
| --- | --- |
| **`SeqBackbone`** | 无 |

      - 与 `AABackbone` 类似，但肽键被分配为单独的片段。

| 项目 | 内容 |
| --- | --- |
| **`AASidechains`** | 无 |

      - 包含所有氨基酸侧链的列表。

| 项目 | 内容 |
| --- | --- |
| **`AASCFinegrained`** | 无 |

      - 包含氨基酸侧链内有机官能团的详细列表。

| 项目 | 内容 |
| --- | --- |
| **`NABackbone`** | 无 |

      - 包含 DNA/RNA 主链的片段定义；磷酸基团被分配到 3′ 位。

| 项目 | 内容 |
| --- | --- |
| **`SEQNABackbone`** | 无 |

      - 包含 DNA/RNA 主链的片段定义；磷酸基团被分配到 5′ 位。

| 项目 | 内容 |
| --- | --- |
| **`NABBFinegrained`** | 无 |

      - 与 `NABackbone` 相同，但进一步拆分磷酸基团。

| 项目 | 内容 |
| --- | --- |
| **`Nucleoticacid`** | 无 |

      - 包含所有核酸的列表。

| 项目 | 内容 |
| --- | --- |
| **`NASidechains`** | 无 |

      - 包含所有核酸侧链的列表。

| 项目 | 内容 |
| --- | --- |
| **`Solvents`** | 无 |

      - 包含常见溶剂的定义：1-辛醇、正己烷、环己烷、甲苯、氯苯、四氢呋喃、苯、N,N-二甲基甲酰胺、吡啶、二甲基亚砜、丙酮、乙醇、乙腈、甲醇、氯仿、四氯化碳、二氯甲烷、氨和水。

| 项目 | 内容 |
| --- | --- |
| **`Water`** | 无 |

      - 包含水分子的定义，如果只需划分水分子片段，比 `Solvents` 更快。

与其他片段划分流程类似，在 `FragProc` 中列出多个库将依次应用这些流程。使用[自动片段划分](#sec:essentialelements.fragmentation.inputfile)中列出的第一个例子（[输入](#sec:essentialelements.fragmentation.intlibex)），并在 `%frag` 模块块中加入 `PrintLevel 3` 以提高输出详细程度，输出将表明由 `Water` 和 `Functional_groups` 流程完成的片段分配。

```orca
===================================================
Tfragmentator: Fragmenting by Water
===================================================

------------------------------------------
 Match: 1, Assigned Fragment: 1
------------------------------------------
  Name:  WATER Method: Water
  Natoms: 3 Charge: 0 Mult: 1

 11 H    -0.920000    0.850000   -2.430000
 12 O    -1.690000    0.830000   -3.000000
 13 H    -1.640000    1.630000   -3.510000
------------------------------------------

===================================================
Tfragmentator: Fragmenting by Functional_groups
===================================================

------------------------------------------
 Match: 1, Assigned Fragment: 2
------------------------------------------
  Name:  CH3 Method: Functional_groups
  Natoms: 4 Charge: 0 Mult: 1

 0 C     0.000000    1.270000   -0.260000
 3 H    -0.890000    1.320000   -0.910000
 4 H     0.890000    1.320000   -0.910000
 5 H     0.000000    2.180000    0.370000
------------------------------------------

------------------------------------------
 Match: 2, Assigned Fragment: 3
------------------------------------------
  Name:  CH3 Method: Functional_groups
  Natoms: 4 Charge: 0 Mult: 1

 2 C     0.000000   -1.270000   -0.260000
 8 H     0.890000   -1.320000   -0.910000
 9 H     0.000000   -2.180000    0.370000
 10 H    -0.880000   -1.300000   -0.910000
------------------------------------------

------------------------------------------
 Match: 1, Assigned Fragment: 4
------------------------------------------
  Name:  CH2 Method: Functional_groups
  Natoms: 3 Charge: 0 Mult: 1

 1 C     0.000000   -0.000000    0.580000
 6 H     0.880000   -0.000000    1.250000
 7 H    -0.880000   -0.000000    1.250000
------------------------------------------

```

<a id="sec:essentialelements.fragmentation.inputfile.externallib"></a>
### 自动片段划分：外部库（External Libraries）

自动片段划分器还允许用户通过 `%frag` 模块块中的 `XZYFRAGLIB` 变量提供 `.xyz` 文件，其中包含应被识别为片段的几何结构。`FragProc Extlib` 流程会自动把每个提供的几何结构转换为分子图，然后应用 VF2 子图同构算法——与内部库的处理方式相同。

下面的例子使用文件 `Mylib.xyz` 中 CH<sub>3</sub>O 和 CH<sub>3</sub> 片段的定义，在如下给出的二甲醚几何结构中识别并生成片段：

<a id="sec:essentialelements.fragmentation.intextlib"></a>
```orca
%frag
  PrintLevel 3
  FragProc Extlib
  XZYFRAGLIB "Mylib.xyz"
end

*xyz 0 1
 O     0.000000     0.000000     0.000000
 C     0.000000     0.000000     1.380000
 C     1.300000     0.000000    -0.460000
 H    -0.500000     0.870000     1.740000
 H    -0.500000    -0.870000     1.740000
 H     1.000000     0.000000     1.740000
 H     1.300000     0.000000    -1.530000
 H     1.800000     0.870000    -0.100000
 H     1.800000    -0.870000    -0.100000
*
```

其中 `Mylib.xyz` 包含甲基和甲氧基的定义。

```orca
    5
CHARGE 0 MULT 1 NAME CH3O
 O     0.000000     0.000000     0.000000
 C     0.000000     0.000000     1.380000
 H     1.008807     0.000000     1.736663
 H    -0.328435     0.953845     1.736667
 H    -0.794950    -0.621083     1.736667
    4
CHARGE 0 MULT 1 NAME CH3
 C     0.000000     0.000000     0.000000
 H     0.000000     0.000000     1.070000
 H     1.008807     0.000000    -0.356663
 H    -0.328435    -0.953845    -0.356667
```

结果是原子 0、1、3、4 和 5 被分配到一个 CH<sub>3</sub>O 片段，其余原子由 `Ext_lib` 流程分配到一个 CH<sub>3</sub>。

```orca
===================================================
Tfragmentator: Fragmenting by Ext_lib
===================================================
****
**** There are 2 Ref structures found in file Mylib.xyz
****

------------------------------------------
 Match: 1, Assigned Fragment: 1
------------------------------------------
  Name:  CH3O Method: Ext_lib
  Natoms: 5 Charge: 0 Mult: 1

 0 O     0.000000    0.000000    0.000000
 1 C     0.000000    0.000000    1.380000
 3 H    -0.500000    0.870000    1.740000
 4 H    -0.500000   -0.870000    1.740000
 5 H     1.000000    0.000000    1.740000
------------------------------------------

------------------------------------------
 Match: 1, Assigned Fragment: 2
------------------------------------------
  Name:  CH3 Method: Ext_lib
  Natoms: 4 Charge: 0 Mult: 1

 2 C     1.300000    0.000000   -0.460000
 6 H     1.300000    0.000000   -1.530000
 7 H     1.800000    0.870000   -0.100000
 8 H     1.800000   -0.870000   -0.100000
------------------------------------------
```

!!! note "注意"
    :class: note
    -   `XZYFRAGLIB` 最多允许包含 10 个文件。每个文件可以包含多个片段定义；但每个定义必须由单个连通的分子组成——单个定义内不允许出现不连通的结构。

    -   `Mylib.xyz` 的格式遵循标准 XYZ 文件结构，但可选地支持三个标识符：`CHARGE`、`MULT` 和 `NAME`，其中 `NAME` 应出现在最后。识别到片段时会打印这些标识符，但目前它们不用于任何计算。

    -   随后其他方法对片段的修改（见下文的 [Fusebyatoms](#sec:essentialelements.fragmentation.inputfile.fuse) 和 [Extend](#sec:essentialelements.fragmentation.inputfile.extend)）不会影响标识符中片段的 CHARGE 或 MULT 值。

!!! note "重要"
    :class: important
    -    ORCA 的 VF2 子图同构算法仅基于原子连接性；它不考虑立体化学或键级。
    -    `FragProc Extlib` 的片段分配遵循 `XZYFRAGLIB` 中列出文件的顺序以及每个文件内片段定义的顺序。由于原子一旦被分配到片段就会从后续匹配中排除，因此库中定义片段的顺序至关重要。例如，在前面的[例子](#sec:essentialelements.fragmentation.intextlib)中，如果 CH<sub>3</sub> 在 `Mylib.xyz` 中定义在 CH<sub>3</sub>O 之前，则[输入文件](#sec:essentialelements.fragmentation.intextlib)中的两个 CH<sub>3</sub> 基团会先被匹配。这将阻止 CH<sub>3</sub>O 在之后被识别，即使它存在于体系中。

    -    原子到片段的分配遵循原子在几何结构中出现的顺序。在[前面的例子](#sec:essentialelements.fragmentation.intextlib)中，CH<sub>3</sub>O 片段既可以按 C(1)-O 键也可以按 C(2)-O 键分配。但由于 C(1) 在几何结构中先出现，它被选入 CH<sub>3</sub>O 片段。

<a id="sec:essentialelements.fragmentation.inputfile.extend"></a>
### 自动片段划分：Extend
内部库中的许多片段代表不完整的分子结构。因此，在某些情况下需要添加额外的氢原子——或在某些情况下添加羟基——来补全体系。`FragProc Extend` 通过识别与先前分配片段中碳原子成键的氧原子，以及与碳、氮或氧成键的氢原子来解决这一问题，然后扩展相应片段以包含这些原子。

考虑下面的例子，它由一个两性离子（zwitterionic）甘氨酸分子组成，使用定义了 C–C–N 片段的外部库进行片段划分。在这种情况下，可以应用 `FragProc Extend` 添加缺失的氧和氢原子，从而补全分子结构。

```orca
%frag
  PrintLevel 3
  FragProc Extlib, Extend
  XZYFRAGLIB "Mylib.xyz"
end

*xyz 0 1
 N     0.000000     0.000000     0.000000
 C     0.000000     0.000000     1.460000
 C     1.403962     0.000000     2.015868
 O     1.837767     0.962613     2.627089
 O     2.161436    -0.947142     1.883370
 H     0.423874    -0.764689    -0.525339
 H    -0.538292    -0.884247     1.831954
 H    -0.538292     0.884247     1.831954
 H    -0.970478     0.016940    -0.313504
 H     0.499909     0.831989    -0.313504
*
```

本例中的 `Mylib.xyz` 为：

```orca
    3
Name CCN
 C     0.000000     0.000000     0.000000
 C     0.000000     0.000000     1.500000
 N     1.376503     0.000000    -0.486661
```

结果是对 C–C–N 片段的初始分配，随后将片段扩展以包含两个氧原子和五个氢原子。

```orca
------------------------------------------
 Match: 1, Assigned Fragment: 1 
------------------------------------------
  Name:  CCN Method: Ext_lib 
  Natoms: 3 Charge: 0 Mult: 1 

 0 N     0.000000    0.000000    0.000000 
 1 C     0.000000    0.000000    1.460000 
 2 C     1.403962    0.000000    2.015868 
------------------------------------------

===================================================
Tfragmentator: Extending Fragments
===================================================
 Extending Fragment 0 with O  (3)
 Extending Fragment 0 with O  (4)
 Extending Fragment 0 with H  (6)
 Extending Fragment 0 with H  (7)
 Extending Fragment 0 with H  (5)
 Extending Fragment 0 with H  (8)
 Extending Fragment 0 with H  (9) 
```

!!! note "重要"
    :class: important
    -    `FragProc Extend` 会尝试扩展任何先前已分配的片段。
    -    `FragProc Extend` 不会修改片段的 `Charge` 和 `Mult` 标识符。

<a id="sec:essentialelements.fragmentation.inputfile.fuse"></a>
### 自动片段划分：Fusebyatoms

当多个片段划分流程组合使用时，可能需要把两个先前已分配的片段合并为一个。这可以通过 `FragProc Fusebyatoms` 流程实现，它按照 `FuseAtomPairs` 中的指定识别应当属于同一片段的原子对。

在下面的例子中，目标是把丙烷分子划分为一个 CH<sub>3</sub> 基团和一个 CH<sub>3</sub>–CH<sub>2</sub> 片段。实现这一点的一种方法是先应用 `FragProc FunctionalGroups`，把分子划分为两个 CH<sub>3</sub> 基团和一个 CH<sub>2</sub> 基团。然后把 CH<sub>2</sub> 基团与其中一个 CH<sub>3</sub> 基团合并。这通过在 `FuseAtomPairs` 指令中指定 CH<sub>2</sub> 和一个 CH<sub>3</sub> 基团的碳原子来完成：`FuseAtomPairs {0 1} end`。

```orca
%frag
        printlevel 3
        FragProc FunctionalGroups, Fusebyatoms
        FuseAtomPairs {0 1} end
end

*xyz 0 1
 C     0.000000     1.270000    -0.260000
 C     0.000000    -0.000000     0.580000
 C     0.000000    -1.270000    -0.260000
 H    -0.890000     1.320000    -0.910000
 H     0.890000     1.320000    -0.910000
 H     0.000000     2.180000     0.370000
 H     0.880000    -0.000000     1.250000
 H    -0.880000    -0.000000     1.250000
 H     0.890000    -1.320000    -0.910000
 H     0.000000    -2.180000     0.370000
 H    -0.880000    -1.300000    -0.910000
*
```

片段划分器的输出首先报告由 `Functional_groups` 库完成的初始片段划分，随后是一条表明按 `FuseAtomPairs` 指令进行片段合并的消息。

```orca
===================================================
Tfragmentator: Fragmenting by Functional_groups
===================================================

------------------------------------------
 Match: 1, Assigned Fragment: 1
------------------------------------------
  Name:  CH3 Method: Functional_groups
  Natoms: 4 Charge: 0 Mult: 1

 0 C     0.000000    1.270000   -0.260000
 3 H    -0.890000    1.320000   -0.910000
 4 H     0.890000    1.320000   -0.910000
 5 H     0.000000    2.180000    0.370000
------------------------------------------

------------------------------------------
 Match: 2, Assigned Fragment: 2
------------------------------------------
  Name:  CH3 Method: Functional_groups
  Natoms: 4 Charge: 0 Mult: 1

 2 C     0.000000   -1.270000   -0.260000
 8 H     0.890000   -1.320000   -0.910000
 9 H     0.000000   -2.180000    0.370000
 10 H    -0.880000   -1.300000   -0.910000
------------------------------------------

------------------------------------------
 Match: 1, Assigned Fragment: 3
------------------------------------------
  Name:  CH2 Method: Functional_groups
  Natoms: 3 Charge: 0 Mult: 1

 1 C     0.000000   -0.000000    0.580000
 6 H     0.880000   -0.000000    1.250000
 7 H    -0.880000   -0.000000    1.250000
------------------------------------------

===================================================
Tfragmentator: Fusing Fragments
===================================================
Fusing Fragment 0 (atom 0) with Fragment 2 (atom 1)

```

<a id="sec:essentialelements.fragmentation.inputfile.delete"></a>
### 自动片段划分：Delete 与高级片段划分工作流

几乎所有的片段划分方案都有一个对应的删除（delete）流程，用于移除该特定方案生成的片段。这使得构建高级片段划分工作流成为可能，其中一个流程可以临时"保护"某些原子不被后续方法划分。这些受保护的片段之后可以被删除，从而允许用不同的片段划分方法重新处理这些原子。

考虑[下面](#sec:essentialelements.fragmentation.intdelaa)的体系，它同时包含一个苯丙氨酸分子和一个苯分子。目标是把苯丙氨酸划分为它的主链、一个 CH<sub>2</sub> 基团和苯环，同时把苯划分为六个独立的 CH 片段。

一方面，通过组合三个片段划分流程——`FragProc AABackbone, Extend, AASCFinegrained`——可以实现苯丙氨酸所需的片段划分。`AABackbone` 和 `Extend` 选项识别氨基酸主链，而 `AASCFinegrained` 把 CH<sub>2</sub> 基团和苯环分离为不同的片段。同时，可以用 `FragProc Extlib` 通过定义 CH 片段的外部库把苯分子划分为六个独立的 CH 片段。然而这两种片段划分方案并不兼容。当对整个体系应用 `FragProc AASCFinegrained` 时，它不仅会划分苯丙氨酸侧链，还会把苯环拆成一个苯基和一个氢原子。反之，如果先对苯应用 `FragProc Extlib`，它可能无意中划分苯丙氨酸残基，导致不希望的结构拆分。

实现目标片段划分的一种可行方法是先用 `FragProc Aminoacids` 识别氨基酸。该流程分配所有属于氨基酸片段的原子，从而保护它们不被后续片段划分步骤重新分配。然后可以用 `FragProc Extlib` 通过外部库划分苯分子。最后用 `FragProc DelAminoacids` 删除苯丙氨酸片段，以便按需要重新划分。所有这些操作只需按如下方式串联流程即可执行：`FragProc Aminoacids, Extlib, DelAminoacids, AABackbone, Extend, AASCFinegrained`

<a id="sec:essentialelements.fragmentation.intdelaa"></a>
```orca
%frag
  PrintLevel 3
  FragProc Aminoacids, Extlib, DelAminoacids, AABackbone, Extend, AASCFinegrained
  XZYFRAGLIB "Mylib.xyz"
  STOREFRAGS true
end

*xyz 0 1
 O     1.300780     3.093320     1.571260
 C     0.407700     2.826000     0.770390
 O    -0.101890     3.606620    -0.030470
 C    -0.115350     1.396690     0.770390
 N    -1.564350     1.396690     0.770390
 H    -1.900780     1.872730     1.595200
 H     0.242580     0.884560     1.663540
 H    -1.901490     0.444630     0.770390
 H    -1.901016     1.873069    -0.054118
 C     0.436090     0.696200    -0.461750
 H     1.512450     0.863150    -0.502770
 H    -0.018950     1.150700    -1.341790
 C     0.178410    -0.790680    -0.515340
 C    -0.895760    -1.288470    -1.262580
 C    -1.134680    -2.667040    -1.312270
 C    -0.299410    -3.547820    -0.614730
 C     0.774760    -3.050040     0.132500
 C     1.013680    -1.671470     0.182200
 H     1.842330    -1.287460     0.758630
 H     1.419110    -3.729500     0.670600
 H    -0.483720    -4.611290    -0.653070
 H    -1.963330    -3.051050    -1.888700
 H    -1.540110    -0.609010    -1.800680
 C     1.181325    -3.732146    -2.620584
 C     2.016592    -4.612923    -1.923046
 C     3.090772    -4.115131    -1.175824
 C     3.329684    -2.736563    -1.126139
 C     2.494417    -1.855785    -1.823677
 C     1.420237    -2.353577    -2.570900
 H     0.770518    -1.668458    -3.113485
 H     0.422252    -4.288369    -3.129823
 H     1.830753    -5.685253    -1.961693
 H     3.740491    -4.800250    -0.633239
 H     4.165243    -2.349352    -0.544907
 H     2.680256    -0.783455    -1.785030
*
```

其中本例的 "Mylib.xyz" 为：
```orca
2
NAME CH
C 0.00 0.00 0.00
H 1.08 0.00 0.00
```

完整的片段划分序列与前面的例子结构相同。在本例中，`Ext_lib` 完成片段分配后会打印消息 `Deleted 1 fragments`，表明先前由 `FragProc Aminoacids` 定义的一个片段已被成功移除。

```orca
===================================================
Tfragmentator: Fragmenting by Amino_Acids
===================================================

------------------------------------------
 Match: 1, Assigned Fragment: 1
------------------------------------------
  Name:  CPHE Method: Amino_Acids
  Natoms: 21 Charge: -1 Mult: 1

 0 O     1.300780    3.093320    1.571260
 1 C     0.407700    2.826000    0.770390
 2 O    -0.101890    3.606620   -0.030470
 3 C    -0.115350    1.396690    0.770390
 4 N    -1.564350    1.396690    0.770390
 5 H    -1.900780    1.872730    1.595200
 6 H     0.242580    0.884560    1.663540
 9 C     0.436090    0.696200   -0.461750
 10 H     1.512450    0.863150   -0.502770
 11 H    -0.018950    1.150700   -1.341790
 12 C     0.178410   -0.790680   -0.515340
 13 C    -0.895760   -1.288470   -1.262580
 14 C    -1.134680   -2.667040   -1.312270
 15 C    -0.299410   -3.547820   -0.614730
 16 C     0.774760   -3.050040    0.132500
 17 C     1.013680   -1.671470    0.182200
 18 H     1.842330   -1.287460    0.758630
 19 H     1.419110   -3.729500    0.670600
 20 H    -0.483720   -4.611290   -0.653070
 21 H    -1.963330   -3.051050   -1.888700
 22 H    -1.540110   -0.609010   -1.800680
------------------------------------------

===================================================
Tfragmentator: Fragmenting by Ext_lib
===================================================
****
**** There are 1 Ref structures found in file Mylib.xyz
****

------------------------------------------
 Match: 1, Assigned Fragment: 2
------------------------------------------
  Name:  CH Method: Ext_lib
  Natoms: 2 Charge: 0 Mult: 1

 23 C     1.181325   -3.732146   -2.620584
 30 H     0.422252   -4.288369   -3.129823
------------------------------------------

------------------------------------------
 Match: 2, Assigned Fragment: 3
------------------------------------------
  Name:  CH Method: Ext_lib
  Natoms: 2 Charge: 0 Mult: 1

 24 C     2.016592   -4.612923   -1.923046
 31 H     1.830753   -5.685253   -1.961693
------------------------------------------

...

------------------------------------------
 Match: 6, Assigned Fragment: 7
------------------------------------------
  Name:  CH Method: Ext_lib
  Natoms: 2 Charge: 0 Mult: 1

 28 C     1.420237   -2.353577   -2.570900
 29 H     0.770518   -1.668458   -3.113485
------------------------------------------

===================================================
Tfragmentator: Deleting Fragments (Amino_Acids)
===================================================
 Deleted 1 fragments
===================================================
Tfragmentator: Fragmenting by Backbone
===================================================

------------------------------------------
 Match: 1, Assigned Fragment: 7
------------------------------------------
  Name: CO-NH3-CH Method: AA_Backbone
  Natoms: 8 Charge: 0 Mult: 0

 0 O     1.300780    3.093320    1.571260
 1 C     0.407700    2.826000    0.770390
 3 C    -0.115350    1.396690    0.770390
 4 N    -1.564350    1.396690    0.770390
 5 H    -1.900780    1.872730    1.595200
 6 H     0.242580    0.884560    1.663540
 7 H    -1.901490    0.444630    0.770390
 8 H    -1.901016    1.873069   -0.054118
------------------------------------------
===================================================
Tfragmentator: Extending Fragments
===================================================
 Extending Fragment 6 with O  (2)

===================================================
Tfragmentator: Fragmenting by AA_SideChains_FG
===================================================

------------------------------------------
 Match: 1, Assigned Fragment: 8
------------------------------------------
  Name: Ph Method: AA_SideChains_FG
  Natoms: 11 Charge: 0 Mult: 1

 12 C     0.178410   -0.790680   -0.515340
 13 C    -0.895760   -1.288470   -1.262580
 14 C    -1.134680   -2.667040   -1.312270
 15 C    -0.299410   -3.547820   -0.614730
 16 C     0.774760   -3.050040    0.132500
 17 C     1.013680   -1.671470    0.182200
 18 H     1.842330   -1.287460    0.758630
 19 H     1.419110   -3.729500    0.670600
 20 H    -0.483720   -4.611290   -0.653070
 21 H    -1.963330   -3.051050   -1.888700
 22 H    -1.540110   -0.609010   -1.800680
------------------------------------------

------------------------------------------
 Match: 1, Assigned Fragment: 9
------------------------------------------
  Name: CH2 Method: AA_SideChains_FG
  Natoms: 3 Charge: 0 Mult: 1

 9 C     0.436090    0.696200   -0.461750
 10 H     1.512450    0.863150   -0.502770
 11 H    -0.018950    1.150700   -1.341790
------------------------------------------

```

表 [tab:essentialelements.delprocedures](#tab:essentialelements.delprocedures) 列出了与每种片段划分方法对应的删除流程。

<a id="tab:essentialelements.delprocedures"></a>
!!! note "片段检测的简单输入关键字及其对应的删除流程"
    | Fragment detection Keyword | Fragment deletion Keyword  |
    |:---------------------------|:---------------------------|
    | `Extlib`                   | `DELExtlib`                |
    | `Connectivity`             | `DELConnectivity`          |
    | `Atomic`                   | `DELAtomic`                |
    | `FunctionalGroups`         | `DELFunctionalGroups`      |
    | `NotAssigned`              |                            |
    | `Backbone`                 | `DELBackbone`              |
    | `SeqBackbone`              | `DELSeqBackbone`           |
    | `AABackbone`               | `DELAABackbone`            |
    | `Aminoacids`               | `DELAminoacids`            |
    | `AASideChains`             | `DELAASideChains`          |
    | `AASCFineGrained`          | `DELAASCFineGrained`       |
    | `NABackbone`               | `DELNABackbone`            |
    | `NABBFineGrained`          | `DELNABBFineGrained`       |
    | `SEQNABackbone`            | `DELSEQNABackbone`         |
    | `NucleoticAcid`            | `DELNucleoticAcid`         |
    | `NASideChains`             | `DELNASideChains`          |
    | `Solvents`                 | `DELSolvents`              |
    | `Water`                    | `DELWater`                 |
    | `Extend`                   |                            |
    | `FuseByAtoms`              |                            |

<a id="sec:essentialelements.fragmentation.inputfile.keywordlist"></a>
## `%frag` 输入块中的可用选项

表 [tab:essentialelements.keywordlist](#tab:essentialelements.keywordlist) 包含 `%frag` 输入块中可用选项的列表。

<a id="tab:essentialelements.keywordlist"></a>
!!! note "`%frag` 输入块中的选项列表"
    :header-rows: 1
    :class: longtable

| 项目 | 内容 |
| --- | --- |
| **Option** | 无 |

      - Type
      - Default
      - Description

| 项目 | 内容 |
| --- | --- |
| **`Printlevel`** | 无 |

      - Integer
      - `1`
      - 自动片段划分的详细输出控制。

| 项目 | 内容 |
| --- | --- |
| **`STOREFRAGS`** | 无 |

      - Boolean
      - `False`
      - 将已分配的片段存储到 `.fragments.xyz` 文件中。

| 项目 | 内容 |
| --- | --- |
| **`DoInterFragBonds`** | 无 |

      - Boolean
      - `False`
      - 自动检测片段之间的键，用于 CoVaLED 分析。

| 项目 | 内容 |
| --- | --- |
| **`XZYFRAGLIB`** | 无 |

      - String
      - `None`
      - `FragProc Extlib` 中使用的文件名。

| 项目 | 内容 |
| --- | --- |
| **`FragProc`** | 无 |

      - 参见 [tab:essentialelements.fragmentationprocedures](#tab:essentialelements.fragmentationprocedures) 和 [tab:essentialelements.delprocedures](#tab:essentialelements.delprocedures)
      - `ExtLib, Connectivity`
      - 要自动应用的片段划分流程。

| 项目 | 内容 |
| --- | --- |
| **`Usetopology`** | 无 |

      - Boolean
      - `False`
      - 基于 .prms 文件生成主几何图。

| 项目 | 内容 |
| --- | --- |
| **`TopolFile`** | 无 |

      - String
      - `""`
      - 当 `Usetopology True` 时使用的拓扑文件名

| 项目 | 内容 |
| --- | --- |
| **`PrintInputFrags`** | 无 |

      - Boolean
      - `True`
      - 写出与当前计算片段等价的 `%frag` 模块块。

