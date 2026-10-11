---
title: 绘制福井函数
source: https://www.faccts.de/docs/orca/6.1/tutorials/react/FUKUI.html
---

# 绘制福井函数

在众多化学反应性描述符中，例如电负性和 Pearson 的"硬软"酸碱理论，由 Parr 和 Yang 定义的"福井函数"（Fukui function, FF）[[Yang1984]](../bib.md#yang1984) 是密度泛函理论（Density Functional Theory, DFT）中应用最广的描述符之一。

根据与 DFT 相关的论证以及能量导数的有限差分方法，福井概念实际上可以分成三个函数。其中一个与对亲核试剂的反应性（$f^+$）有关，其表达式为：

$$
f^+(\mathbf r) = \rho_{N + 1}(\mathbf r) - \rho_{N}(\mathbf r)
$$

这里 $\rho$ 是电子密度，$N$ 是电子数，也就是说 $\rho_{N + 1}(\mathbf r)$ 是在 $\rho_N(\mathbf r)$ 上增加一个电子所生成的阴离子的密度。

该函数的高正值区域指示了分子中最可能受到亲核试剂进攻的部位，事实上从有机化学到代谢产物 [[Beck2005]](../bib.md#beck2005) 都存在与之的相关性。

另外两个函数分别与亲电（$f^-$）或自由基（$f^0$）进攻有关，定义为：

$$
f^-(\mathbf r) = \rho_{N}(\mathbf r) - \rho_{N - 1}(\mathbf r)
$$

或

$$
f^0(\mathbf r) = 1/2[\rho_{N + 1}(\mathbf r) - \rho_{N - 1}(\mathbf r)]
$$

让我们用 ORCA 计算并绘制这些函数，并配合 [Chemcraft](https://www.chemcraftprog.com/) 软件进行可视化。

## 丁内酯的福井函数

丁内酯与其他内酯一样，已知会在羰基的碳原子上遭受亲核进攻。它也可以被质子化，或在"亲电进攻"中通过该基团的氧原子配位 [[Gazquez1994]](../bib.md#gazquez1994)：

[![lactone](../images/lactone.png)](../images/lactone.png)

当然，这些都是基础有机化学的常识，但我们想展示它也可以用福井函数从第一性原理预测出来。

第一步是优化目标分子，在本例中是内酯的中性形式，例如使用 B3LYP：

```text
!B3LYP D3 DEF2-SVP OPT KEEPDENS
* XYZFILE 0 1 butyrolactone_guess.xyz
```

这里加上了 KEEPDENS 标志，以保留 basename.scfp 密度文件，稍后将用它来绘制密度图。

在得到优化几何结构和密度（即 $\rho_{N}(\mathbf r)$）之后，我们还需要相应阴离子 $\rho_{N + 1}(\mathbf r)$ 和阳离子 $\rho_{N -1}(\mathbf r)$ 的密度，且必须在**与中性密度相同的几何结构**上计算。这可以用如下输入简单完成：

```text
!B3LYP D3 DEF2-SVP KEEPDENS
* XYZFILE -1 2 butyrolactone_optimized.xyz
```

以及：

```text
!B3LYP D3 DEF2-SVP KEEPDENS
* XYZFILE 1 2 butyrolactone_optimized.xyz
```

注意此时多重度为二，因为每种情形都有一个未配对电子，而且去掉了 OPT 标志。

## 生成 .cube 文件

要把计算得到的密度变成图像，可以使用 ORCA 软件自带的 ORCA_PLOT 模块。用法很简单，只要把 basename.gbw 和 basename.scfp 放在同一目录下并运行：

```text
./orca_plot basename.gbw -i
```

或者，如果使用 Windows：

```text
orca_plot basename.gbw -i
```

*-i* 标志表示应出现交互式菜单：

```text
Current-settings:

PlotType       ... MO-PLOT
MO/Operator    ... 0 0
Output file    ... (null)
Format         ... Grid3D/Binary
Resolution     ... 40 40 40
Boundaries     ...   -16.609820     3.250952 (x direction)
                      -9.340979    12.515542 (y direction)
                      -9.284442     9.293555 (z direction)

       1 - Enter type of plot
       2 - Enter no of orbital to plot
       3 - Enter operator of orbital (0=alpha,1=beta)
       4 - Enter number of grid intervals
       5 - Select output file format
       6 - Plot CIS/TD-DFT difference densities
       7 - Plot CIS/TD-DFT transition densities
       8 - Set AO(=1) vs MO(=1) to plot
       9 - List all available densities

      10 - Generate the plot
      11 - exit this program
Enter a number:
```

然后选择 1 设置*绘图类型*，再选择 2 即*电子密度*。如果软件询问密度文件的名称，选择 *y* 或给出不同于 basename.scfp 的名称。

之后，选择 5 设置*文件格式*，再选择 7 即 *3D Gaussian cube*——这正是我们稍后要打开的文件类型。也可以选择 4 来增加*网格间隔数*，以获得更高分辨率的图像。选项编号 10 将生成我们的 basename.eldens.cube 文件。

对阳离子和阴离子的密度重复上述操作，就可以开始计算福井函数了。

> **注意**
> 值得在菜单中浏览一番，看看还有哪些其他选项！

> **重要**
> 这些文件的大小会随 `Resolution` 显著增大。通常 100 左右的数值对发表就足够好了，超过 200 的数值几乎没必要！

## 计算福井函数

要读取密度文件并对其执行必要的运算，现在打开 [Chemcraft](https://www.chemcraftprog.com/)。为了计算 $f^+(\mathbf r)$ 函数，首先点击"File"再点击"Open"，打开**阴离子**的 cube 文件，选择 basename.eldens.cube。

> **重要**
> 注意不要被公式搞混！在 $\rho_{N + 1}(\mathbf r)$ 中，$N$ 指的是电子数，而 $N+1$ 并不表示阳离子，而是多加了一个电子的阴离子。

如果现在点击"Show isosurface"和"Both-signed"，你应当看到如下电子密度：

[![lac_dens](../images/lac_dens.png)](../images/lac_dens.png)

然而，这并不是我们想要的，我们要得到的福井函数实际上是密度之间的一种*数学运算*。这正是软件能帮上忙的地方：点击"Multiple cubes operations..."，然后选择"Add cube(s)"并打开中性分子的 cube 文件。

现在你会有两个同名为 "Total electron density" 的文件，它们实际上代表不同的物理量：第一个是阴离子的，第二个是中性分子的。

为了真正绘制 $f^+(\mathbf r)$，运算 $\rho_{N + 1}(\mathbf r) - \rho_{N}(\mathbf r)$ 可以这样完成：再次点击"Multiple cubes operations..."，然后点击"Perform operation on two cubes (subtract, etc.)"。必须相应地选择第一个和第二个 cube，选项应为"Subtract"。

点击"OK"之后，会出现第三个文件，它是前两者之差，恰好对应 $f^+(\mathbf r)$。点击"Show isosurface"和"Both-signed"查看图像：

[![lac_fplus](../images/lac_fplus.png)](../images/lac_fplus.png)

红色表示正的 $f^+(\mathbf r)$，蓝色表示负的。也可以把"Contour value"改成别的数值以便更好地可视化这些图。如你所见，尽管有些分散，最大值位于羰基的碳原子上，正是基础有机化学所预期的。

用同样方法计算的相应 $f^-(\mathbf r)$ 函数为：

[![lac_fminus](../images/lac_fminus.png)](../images/lac_fminus.png)

它显示最高值位于羰基的氧原子周围，该原子应当与亲电物种有更强的相互作用，这同样符合经验上的预测。

## 自由基反应的情形

尽管这些反应并不完全直截了当，但分子中最容易受到自由基进攻的位置也可以用 $f^0(\mathbf r)$ 函数来考察。

让我们以 2-甲基丙烷为例。已知叔碳上的氢原子对自由基的反应性远高于末端甲基。

[![tbut](../images/tbut.png)](../images/tbut.png)

按照相同的步骤，从阳离子密度中减去阴离子密度得到 $f^0(\mathbf r)$ 后，我们得到的图像为：

[![tbut_fzero](../images/tbut_fzero.png)](../images/tbut_fzero.png)

同样与实验观测一致！

## 结构

### 内酯

```text
12

C         -2.19840        3.00305       -0.20666
C         -2.50179        1.55642        0.08284
O         -1.29812        0.85411       -0.22491
H         -3.31949        1.17786       -0.53711
H         -2.74629        1.38587        1.13674
C         -0.73652        3.10508        0.14798
H         -2.83435        3.69747        0.34848
H         -2.33068        3.20260       -1.27718
C         -0.24607        1.72326       -0.16280
H         -0.58903        3.30540        1.21300
H         -0.22545        3.85317       -0.46203
O          0.92223        1.40071       -0.30020
```

### 2-甲基丙烷

```text
14

C         -2.00101        1.13154       -0.01481
C         -0.74766        0.35180       -0.40610
H         -2.03259        2.09886       -0.52726
H         -2.03355        1.31857        1.06399
H         -2.90487        0.57775       -0.28989
C          0.50935        1.14534       -0.05653
H          0.51275        2.11333       -0.56869
H          1.40954        0.60194       -0.36262
H          0.57626        1.33191        1.02076
C         -0.72878       -1.01302        0.27864
H         -0.76482        0.19312       -1.49129
H          0.15463       -1.58631       -0.02178
H         -1.61458       -1.59659        0.00638
H         -0.71202       -0.91168        1.36919
```
