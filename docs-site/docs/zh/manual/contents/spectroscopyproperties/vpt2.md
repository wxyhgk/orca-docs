

<a id="sec:spectroscopyproperties.vpt2"></a>
# 使用 VPT2/GVPT2 和 `orca_vpt2` 进行非谐分析与振动修正（Anharmonic Analysis and Vibrational Corrections using VPT2/GVPT2 and `orca_vpt2`）

在（解析的）谐振 Hessian 计算基础上，可以计算三次加半四次力场
以及更高阶的性质导数。为此，VPT2 模块将计算 Hessian，然后为每个
自由度生成两个位移几何结构，并对每个位移再计算一个 Hessian
（在振动修正情形下还要计算另一个性质）。这些是按照二阶振动
微扰理论（second-order vibrational perturbation theory）进行
非谐分析所必需的。总体而言，使用 VPT2 的代价较高，因为数值导数
需要进行大量计算，并且对收敛、近似及其他设置引起的数值噪声
非常敏感。VPT2 计算既可以通过简单输入命令 `!VPT2` 启动，
也可以通过 `%vpt2` 块中的 VPT2 关键词启动。更精细的控制可通过
`%VPT2` 块实现，如下面对水分子的分析所示。

```mol
title: structure 1
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
3
structure (0 1)
O  0.00000000000000 0.06256176106279 0.06256176106280
H  0.00000000000000 -0.06185639479702 0.99929463373422
H  0.00000000000000 0.99929463373424 -0.06185639479703
--- input ---
# VPT2 Analysis of H2O
!RHF def2-SVP ExtremeSCF VPT2

%vpt2
  VPT2               On      # do a VPT2 analysis, same as !VPT2 (see above)
  AnharmDisp         0.05    # anharmonic displacement factor, default is 0.05
  HessianCutoff      1e-12   # cut-off for Hessian elements, default is 1e-10
  PrintLevel         1       # VPT2 print level [1, 2, 3, 4]
  MinimiseOrcaPrint  True    # Minimises the remaining orca output
end

%method
    Z_Tol               1e-14
end

* xyz 0 1
  O   0.00000000000000      0.06256176106279      0.06256176106280
  H   0.00000000000000     -0.06185639479702      0.99929463373422
  H   0.00000000000000      0.99929463373424     -0.06185639479703
*
```

分析完成后，工作目录中应存在一个 `<basename>.vpt2` 文件。
所有力场和性质导数都保存在该文件中。它作为 `orca_vpt2`
程序的输入，该程序会在初始位移计算之后自动调用。也可以
通过命令 `orca_vpt2 <basename>.vpt2` 单独调用该程序。

!!! note
    ***关于 VPT2 计算的几点说明：***

    -   VPT2 的起始几何结构**必须始终紧密收敛**。对于小分子，
        `!TightOPT` 选项是不够的！
        根据您的结构，可能需要尝试 `%geom` 块中的
        `TolE`、`TolRMSG` 和 `TolMaxG` 关键词。

    -   同样，SCF 必须良好收敛。建议使用
        `ExtremeSCF` 关键词，或至少使用 `VeryTightSCF`。

    -   CP-SCF 方程应至少收敛到 $10^{-12}$
        （通过 `%method` 块中的 `Z_Tol` 设置修改）。

    -   对于 DFT 计算，强烈建议使用 `DEFGRID3` 等密集网格。

    -   **目前尚不支持线性分子**

    -   目前仅支持具有解析 Hessian 的方法。此外，**对于不提供解析
        Hessian 的 DFT 泛函，无法进行 VPT2 计算**。

    -   默认情况下，使用更新后的原子质量来生成半四次力场
        （见 [frequencies.massdependencies](#sec:structurereactivity.frequencies.massdependencies)）。
        质量也会打印在 `<basename>.vpt2` 文件中

    -   可以通过运行 `orca_vpt2 <basename>.vpt2`
        对先前的计算重复进行 VPT2 分析。

    -   VPT2 具有有限的重启能力。如果执行 VPT2 的目录中已存在
        `<basename>.hess` 或 `<basename>_eprnmr.property.txt` 文件，
        程序将跳过这些点并使用文件中提供的信息。

VPT2 提供振动分析，从而可以获得：
- 位移的均值和均方期望值
- 离心畸变常数
- Watson 对称约化与非对称约化哈密顿量参数
- 非谐常数
- 费米共振分析
- 转动常数和振动-转动常数
- 基频跃迁（非谐频率）
- 零点转振能量
- 含强度的倍频与组合频
  （与具有完整 VPT2/GVBT2 处理的 NEARIR 相比）
- 面向 SPCAT 等程序的专用文件接口

如果计算数据要用于 SPCAT 等程序进行光谱模拟，
ORCA 可以提供一个专用文件作为输入的基础。在运行 VPT2 计算时，
可在 `%output` 块中触发此功能：

```orca
%output 
 Pickettname "pickett.txt"
end
```

这样，ORCA 将生成一个名为 `pickett.txt` 的文件，其中包含
计算数据和 `.var` 模板，可修改后作为 SPCAT 等程序的输入。
请注意，该功能仍在完善和扩展中。

<a id="sec:spectroscopyproperties.vpt2.properties"></a>
## 使用 VPT2 进行分子性质的振动修正（Vibrational corrections of molecular properties using VPT2）

使用 VPT2 也可以计算分子性质的零点振动修正。目前，这适用于
NMR 化学屏蔽、自旋-自旋耦合常数、g 张量和 A 张量，
并且需要两次连续的计算。第一次计算是如上所示的 VPT2 计算
（`<basename>.inp`），包含 `VPT2` 命令以及计算 Hessian 的
理论水平。第二次计算（我们称其为 `<basename>_Prop.inp`）
将计算性质导数，最后调用 VPT2。为使此流程正常工作，
性质导数计算需要从力场计算中读取 `<basename>.hess` 和
`<basename>.vpt2` 文件。这通过指定 `%geom inhess read`
并使用命令 `inhessname "<basename>.hess"` 来完成。
之所以需要这种方案，是因为除能量、几何结构或频率之外的性质
通常需要专门的方法和基组。对于力场和性质导数的数值计算，
可以通过在 VPT2 输入块中指定 `AnharmDisp` 和 `PropDisp`
使用不同的步长。默认值为 0.05，计算完成后，位移几何结构
存储在名为 `myjob_DH001.xyz` 和 `myjob_DP001.xyz` 等文件中。

一个典型的例子是计算甲醇 $^{13}$C NMR 化学位移的振动修正，
采用 B3LYP/def2-TZVP 非谐力场和 TPSS/pcSseg-2 屏蔽张量，
其输入如下所示：标准输入文件（本例中为
`vpt2_methanol_FF.inp`）包含 Hessian 的理论水平和 VPT2 输入块：

```mol
title: structure 2
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
6
structure (0 1)
C  -1.09849212248373 0.14540972773089 -0.00000275092982
O  0.32138758531316 0.08706714755687 -0.00001212477411
H  0.66732439683790 0.98510769198508 0.00001819506998
H  -1.45583606337199 -0.88374271593276 0.00000595999622
H  -1.49206267729630 0.64725244577978 0.89143349761200
H  -1.49208273899904 0.64724452288014 -0.89144277697426
--- input ---
!B3LYP D3 def2-TZVP def2/J def2/JK DEFGRID3 ExtremeSCF VPT2

%method
    Z_Tol  1e-12
end

* xyz 0 1
C  -1.09849212248373      0.14540972773089     -0.00000275092982
O   0.32138758531316      0.08706714755687     -0.00001212477411
H   0.66732439683790      0.98510769198508      0.00001819506998
H  -1.45583606337199     -0.88374271593276      0.00000595999622
H  -1.49206267729630      0.64725244577978      0.89143349761200
H  -1.49208273899904      0.64724452288014     -0.89144277697426
*
```

接下来的输入文件（例如 `vpt2_methanol_NMR.inp`）使用相同
几何结构和屏蔽张量的理论水平，如下所示：

```mol
title: structure 3
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
6
structure (0 1)
C  -1.09849212248373 0.14540972773089 -0.00000275092982
O  0.32138758531316 0.08706714755687 -0.00001212477411
H  0.66732439683790 0.98510769198508 0.00001819506998
H  -1.45583606337199 -0.88374271593276 0.00000595999622
H  -1.49206267729630 0.64725244577978 0.89143349761200
H  -1.49208273899904 0.64724452288014 -0.89144277697426
--- input ---
!TPSS pcSseg-2 Autoaux ExtremeSCF NMR

%geom inhess read
 inhessname "vpt2_methanol_FF.hess"
end

%vpt2
  VPT2          on
  AvgProp       NMR
  HessianCutoff 1e-12
end

%method
  Z_Tol         1e-12
end

* xyz 0 1
C  -1.09849212248373      0.14540972773089     -0.00000275092982
O   0.32138758531316      0.08706714755687     -0.00001212477411
H   0.66732439683790      0.98510769198508      0.00001819506998
H  -1.45583606337199     -0.88374271593276      0.00000595999622
H  -1.49206267729630      0.64725244577978      0.89143349761200
H  -1.49208273899904      0.64724452288014     -0.89144277697426
*
```

在同一目录中依次对这两个输入文件运行 ORCA，将得到包含每个原子
屏蔽张量零点振动修正的输出。对于原子 0（即甲醇中的碳），
输出如下所示：

```orca
----- 
 Vibrationally averaged isotropic shieldings 
 ---- 

Atom 0 :

 mode    <q>       <q2>      dS/dQ    d2S/dQ2
-----------------------------------------------
   0  -0.000017   0.202578  -0.000089  -5.922644
   1  -0.034052   0.057707   8.269988  -5.666515
   2  -0.036827   0.055687   5.667278 -13.843941
   3   0.000002   0.051446   0.000073  -7.353936
   4   0.027471   0.043993   0.423409  -6.207061
   5  -0.009357   0.040649 -12.736464   3.762324
   6  -0.000001   0.040278  -0.001621  -2.224536
   7   0.001277   0.039898  -1.266298  -3.916647
   8  -0.031609   0.020149  51.647411 -21.635780
   9  -0.000021   0.019859   0.035760 -61.239749
  10  -0.010397   0.019376  18.573156 -50.591165
  11  -0.026641   0.015808  -8.871055  -6.654795
-----------------------------------------------

zpv correction to isotropic shift :  -4.840215 ppm
-----------------------------------------------
```

因此，甲醇中碳的绝对屏蔽常数需要因零点振动而修正 -4.8 ppm。
从位移的均值和均方值以及屏蔽对简正模式的一阶和二阶导数，
还可以识别出对振动修正贡献较大的自由度。

HH 自旋-自旋耦合常数的类似输入如下所示：

```mol
title: structure 4
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
6
structure (0 1)
C  -1.09849212248373 0.14540972773089 -0.00000275092982
O  0.32138758531316 0.08706714755687 -0.00001212477411
H  0.66732439683790 0.98510769198508 0.00001819506998
H  -1.45583606337199 -0.88374271593276 0.00000595999622
H  -1.49206267729630 0.64725244577978 0.89143349761200
H  -1.49208273899904 0.64724452288014 -0.89144277697426
--- input ---
!TPSS pcJ-2 Autoaux ExtremeSCF NMR

%geom inhess read
 inhessname "vpt2_methanol_FF.hess"
end

%maxcore 4096

%vpt2
  VPT2          on
  AvgProp       JCOUPLING
  AnharmDisp    0.05
  HessianCutoff 1e-12
end

%method
  Z_Tol         1e-12
end

%eprnmr
  Tol           1e-10
end

* xyz 0 1
C  -1.09849212248373      0.14540972773089     -0.00000275092982
O   0.32138758531316      0.08706714755687     -0.00001212477411
H   0.66732439683790      0.98510769198508      0.00001819506998
H  -1.45583606337199     -0.88374271593276      0.00000595999622
H  -1.49206267729630      0.64725244577978      0.89143349761200
H  -1.49208273899904      0.64724452288014     -0.89144277697426
*

%eprnmr
Nuclei = all H {ssfc}
end
```

如上所述，完全相同的流程也适用于 A 张量。下面是 NH$_2$ 自由基
的例子，VPT2 输入文件为 `vpt2_NH2_FF.inp`：

```mol
title: structure 5
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
3
structure (0 2)
N  -0.01498947828047 -0.01894387811818 0.00000000000000
H  1.03197835263254 0.00908678452370 0.00000000000000
H  -0.22855980523269 1.00639225931822 0.00000000000000
--- input ---
!UKS BP86 def2-svp def2/J ExtremeSCF defgrid3

%vpt2
    VPT2                On
end

%method
    Z_Tol               1e-12
end

* xyz 0 2
N   -0.01498947828047     -0.01894387811818      0.00000000000000
H   1.03197835263254      0.00908678452370      0.00000000000000
H   -0.22855980523269      1.00639225931822      0.00000000000000
*
```

以及用于 A 张量计算理论水平的输入文件（例如 `vpt2_NH2_A.inp`）：

```mol
title: structure 6
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
3
structure (0 2)
N  -0.01498947828047 -0.01894387811818 0.00000000000000
H  1.03197835263254 0.00908678452370 0.00000000000000
H  -0.22855980523269 1.00639225931822 0.00000000000000
--- input ---
!UKS BP86 def2-SVP TightSCF

%geom inhess read
 inhessname "vpt2_NH2_FF.hess"
end

%vpt2
    VPT2                On
    AvgProp             Atensor
end

*xyz 0 2
N   -0.01498947828047     -0.01894387811818      0.00000000000000
H   1.03197835263254      0.00908678452370      0.00000000000000
H   -0.22855980523269      1.00639225931822      0.00000000000000
*

%eprnmr
Nuclei = all N { aiso, adip }
Nuclei = all H { aiso, adip }
end
```

对于 g 张量也是类似的，只需在 `%vpt2` 块中将 `Atensor`
替换为 `Gtensor`（此时可省略 `%eprnmr` 块）。

请注意，计算振动修正的一种便捷方式是使用复合脚本（compound script）。
使用名为 `NH2.inp` 的输入文件：

```mol
title: structure 7
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
3
structure (0 2)
N  0.00312611577632 0.00395297373474 0.00000000000000
H  1.01930353842041 0.00049997276783 0.00000000000000
H  -0.23400058507735 0.99208221922117 0.00000000000000
--- input ---
* xyz 0 2
N   0.00312611577632      0.00395297373474      0.00000000000000
H   1.01930353842041      0.00049997276783      0.00000000000000
H   -0.23400058507735      0.99208221922117      0.00000000000000
*

%Compound "NH2.cmp"
```

以及对应的复合脚本 `NH2.cmp`：

```mol
title: structure 8
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
6
structure (0 2)
N  0.00312611577632 0.00395297373474 0.00000000000000
H  1.01930353842041 0.00049997276783 0.00000000000000
H  -0.23400058507735 0.99208221922117 0.00000000000000
N  0.00312611577632 0.00395297373474 0.00000000000000
H  1.01930353842041 0.00049997276783 0.00000000000000
H  -0.23400058507735 0.99208221922117 0.00000000000000
--- input ---
New_Step
!UHF def2-SVP VeryTightSCF  

%vpt2
    VPT2                On      
end

%method
    Z_Tol               1e-12
end

* xyz 0 2
N   0.00312611577632      0.00395297373474      0.00000000000000
H   1.01930353842041      0.00049997276783      0.00000000000000
H   -0.23400058507735      0.99208221922117      0.00000000000000
*
Step_End

New_Step
!UHF def2-SVP VeryTightSCF 

%geom inhess read
 inhessname "NH2_Compound_1.hess"
end

%vpt2
    VPT2                On
    AvgProp             Atensor
end

*xyz 0 2
N   0.00312611577632      0.00395297373474      0.00000000000000
H   1.01930353842041      0.00049997276783      0.00000000000000
H   -0.23400058507735      0.99208221922117      0.00000000000000
*

%eprnmr 
Nuclei = all N { aiso, adip }
Nuclei = all H { aiso, adip }
end

Step_End

END
```

这样就可以在一次计算中得到类似的结果。

!!! note
    请确保给出正确的 Hessian 文件名，且输入文件中
    不能包含复合块。您也可以直接使用 `orca_vpt2` 重新运行 VPT2 分析。
    如果有一个名为 `myjob_ff` 的非谐力场计算和一个名为 `myjob_prop`
    的性质导数计算，只需调用
    `orca_vpt myjob_ff.vpt2 myjob_prop.vpt2`。

