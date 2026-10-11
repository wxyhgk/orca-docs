---
title: 过渡态优化
source: https://www.faccts.de/docs/orca/6.1/tutorials/react/tsopt.html
---

# 过渡态优化

获取有效的过渡态（transition state, TS）结构初始猜测有多种方法，例如弛豫势能面扫描或 NEB 模拟。若只想优化给定的过渡态猜测结构，而不使用 [NEB-TS](../react/nebts.md) 等自动化流程，可使用 `!OptTS` 关键词。在下面的教程中，我们将设置一个弛豫势能面扫描，以获得乙二醛 *cis*-*trans* 异构化反应过渡态的初始猜测，然后用 `!OptTS` 优化该过渡态。

## 示例：乙二醛的 *cis*-*trans* 异构化

### 弛豫势能面扫描

用例如 [Avogadro 2](../first_steps/GUI.md) 获得乙二醛的有效起始结构后，可以使用 `!Opt` 简单关键词以及 `%geom` 块中相应的扫描定义，围绕 O-C-C-O 二面角设置弛豫势能面扫描。在本示例中，我们将使用 r²SCAN-3c 复合 DFT 方法执行该扫描。

```text
!r2SCAN-3c Opt

%geom
   Scan D 0 1 2 3  = 180, 360, 19 end # Scan of the dihedral angle defined by atoms 0, 1, 2, and 3 from 180° to 360° in 19 steps.
end

*xyz 0 1
  O          -1.80011949735812      0.99666410862853     -0.00003868102245
  C          -1.27328664864401     -0.08847334375096     -0.00001219100927
  C           0.24492627868679     -0.23050598341765     -0.00002272454655
  O           0.77147537164033     -1.31579795317196     -0.00003090426569
  H          -1.83500409491985     -1.04822924700392      0.00001280906050
  H           0.80714603899486      0.72893993091597     -0.00002459971653
```

> **重要**
> 请注意，ORCA 的原子编号从 0 开始，因此原子 1 的标识符是 0。

> **提示**
> 请确保起始角度不要偏离初始结构的角度太远，以避免出现某些假象。

运行该扫描后，我们得到一条平滑的能量曲线，可以从中选取能量最高的结构作为过渡态猜测结构。

[![fig_scan](../images/fig_scan.png)](../images/fig_scan.png)

*图：乙二醛 O-C-C-O 二面角的弛豫扫描。*

### 使用 `!OptTS` 进行过渡态优化

从过渡态猜测结构出发，最常见的流程是：

1. 使用精度较低的近似 Hessian 直接运行 `!OptTS` 计算（**不推荐**）。
2. 直接运行 `!OptTS` 计算，并要求先进行精确 Hessian 计算（**推荐**）。
3. 用 [`!Freq`](../prop/freq.md) 进行精确 Hessian 计算，检查过渡态的虚频模式，然后在读取此前频率计算生成的 `.hess` 文件的情况下运行 `!OptTS`。

> **警告**
> 仅通过直接运行 `!OptTS` 使用近似 Hessian，可能导致过渡态定位出现困难。我们一般建议从精确 Hessian 开始过渡态优化。

> **提示**
> 在 `!OptTS` 旁边加上 `!Freq` 简单输入关键词，即要求在过渡态优化**之后**进行频率计算。这对于验证优化所得结构确实是过渡态（其特征是恰好有一个虚频）非常有用。

> **提示**
> 过渡态优化可以通过多种方式自定义，以提高效率或处理困难的过渡态（例如势垒非常低的情况）。因此，我们建议阅读 [ORCA 手册](https://www.faccts.de/docs/orca/manual/)中的相应章节。请注意，`!OptTS` 的收敛阈值由普通几何优化所用的现有关键词（如 `!TightOpt`）控制。

#### 使用近似 Hessian 的 `!OptTS`

使用近似 Hessian 进行过渡态优化的输入如下所示

```text
!r2SCAN-3c OptTS

*xyzfile 0 1 tsguess.xyz
```

`.out` 文件中会显示使用了 Almlöf 近似 Hessian。

```text
Evaluating the initial hessian          ...  (Almloef) done
[...]
Evaluating the initial hessian          ....  (Almloef) done
```

#### 使用精确 Hessian 的 `!OptTS`

要为过渡态优化计算精确 Hessian，必须在 `%geom` 块中定义 `Calc_Hess true`。

```text
!r2SCAN-3c OptTS

%geom
   Calc_Hess true
end

*xyzfile 0 1 tsguess.xyz
```

`.out` 文件中会显示在过渡态优化之前计算了精确 Hessian。

```text
Evaluating the initial hessian          ...  (Is done on the fly) done
[...]
Evaluating the initial hessian          ....  (read)
```

#### 读入 Hessian 的 `!OptTS`

要读取先前计算的 Hessian，可以在 `%geom` 块中使用 `inhess read` 关键词，并通过 `InHessName "name.hess"` 提供 Hessian 文件的名称。

```text
!r2SCAN-3c OptTS

%geom
  inhess   Read                   # this command comes with:
  InHessName "tsguess.hess"       # filename of Hessian input file
end

*xyzfile 0 1 tsguess.xyz
```

如果 `.hess` 文件读取成功，`.out` 文件中会给出提示：

```text
Evaluating the initial hessian          ... (Reading Exact Hessian)...
[...]
Evaluating the initial hessian          ....  (read)
```

### 过渡态验证

与常规几何优化一样，过渡态优化也必须达到适当的收敛。过渡态优化的收敛会在 `.out` 文件中高亮显示。在本例中，精确 Hessian 和近似 Hessian 两种方案都能正常工作，并得到了收敛的过渡态，其 O-C-C-O 二面角约为 75.5°。

```text
                    ***********************HURRAY********************
                    ***        THE OPTIMIZATION HAS CONVERGED     ***
                    *************************************************
```

[![ts3](../images/ts3.png)](../images/ts3.png)

*图：乙二醛 *cis*-*trans* 异构化优化后的过渡态。*

然而，进一步检查优化后的结构是势能面上的极小点还是鞍点（即过渡态）也很重要。后者的特点是：在最终优化的过渡态几何上进行频率计算时，恰好出现一个虚频。而且该虚频必须对应于我们所关注的结构变化，在本例中即绕 C-C 键的旋转。这样的频率计算既可以通过简单地在 `!OptTS` 旁边加上 `!Freq` 简单输入关键词来请求（这将在过渡态优化**之后**进行频率计算），也可以对优化后的几何结构单独用 `!Freq` 进行一次计算。

> **重要**
> 请注意，频率计算必须在与几何优化相同的理论水平下进行！

下面给出了一个完整输入示例，在一个输入中依次完成过渡态优化所需的精确 Hessian 计算、过渡态优化以及随后的验证频率计算。

```text
!r2SCAN-3c OptTS Freq

%geom
   Calc_Hess true
end

*xyzfile 0 1 tsguess.xyz
```

对于乙二醛 *cis*-*trans* 翻转优化后的过渡态，只得到一个对应于 C-C 键旋转的虚频，从而验证了本例过渡态优化的成功。相应的振动可以用 Avogadro 2 或 ChimeraX 等多种工具进行可视化（参见[图形用户界面](../first_steps/GUI.md)和[红外与拉曼光谱](../spec/IR.md)章节）。

```text
-----------------------
VIBRATIONAL FREQUENCIES
-----------------------

Scaling factor for frequencies =  1.000000000  (already applied!)

     0:       0.00 cm**-1
     1:       0.00 cm**-1
     2:       0.00 cm**-1
     3:       0.00 cm**-1 
     4:       0.00 cm**-1
     5:       0.00 cm**-1
     6:    -189.59 cm**-1  ***imaginary mode***  
     7:     277.42 cm**-1
```

### 结构

### 过渡态猜测结构

```text
6

 O     -1.83324      0.62772      -0.77785
 C     -1.27709     -0.09000       0.01396
 C      0.24881     -0.22901       0.01383
 O      0.80483     -0.94688      -0.77793
 H     -1.83538     -0.69931       0.76395
 H      0.80720      0.38008       0.76393
```

### 优化后的过渡态

```text
6

  O          -1.84421679351156      0.59484103960635     -0.80568139753757
  C          -1.27714789879691     -0.08950826948560      0.00706950134558
  C           0.24885835929743     -0.22962545826381      0.00700905374646
  O           0.81586625296348     -0.91394186131928     -0.80581207877593
  H          -1.82442938469100     -0.65567049798748      0.79869194748586
  H           0.79619946473857      0.33650504744981      0.79861297373560
```
