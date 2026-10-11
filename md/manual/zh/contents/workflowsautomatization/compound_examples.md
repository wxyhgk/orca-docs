(sec:workflowsautomatization.compound_examples)=
# Compound 示例（Compound Examples）

(sec:workflowsautomatization.compound_examples.introduction)=
## 简介（Introduction）

在页面 https://github.com/ORCAQuantumChemistry/CompoundScripts 上有一个 compound 脚本库。

(sec:workflowsautomatization.compound_examples.HelloWorld)=
## Hello World

**简介（Introduction）**

这是最简单的脚本，但它指向了 *Compound* 的一个重要特性。即 *Compound* 不必运行真正的“常规”ORCA 计算，也可以用作各种任务的驱动程序，在本例中只是打印一条消息。

**文件名（Filename）**

helloWorld.inp

**SCRIPT**
```{literalinclude} ../../orca_working_input//compound_library_examples/helloWorld.inp
:language: orca
```


## New Job

**简介（Introduction）**

ORCA 中将来会被弃用、且不应再使用的特性之一是 *'New_Job'* 特性。本脚本是一个简单示例，展示如何用 *Compound* 仅运行一系列计算。

**文件名（Filename）**

replaceNewJob.inp

**SCRIPT**
```{literalinclude} ../../orca_working_input//compound_library_examples/replaceNewJob.inp
:language: orca
```

**注释（Comments）**

从 *Compound* 的角度来看，本脚本中的语法并非最高效的写法。它可以改写成更紧凑、更清晰、更通用的形式。不过，这只是一个示例，说明 *Compound* 如何取代使用了即将弃用的 *'New_Job'* 特性的较旧 ORCA 计算。

## 高精度（High Accuracy）

**简介（Introduction）**

这是一个利用 N. J. DeYonker、T. R. Cundari 和 A. K. Wilson 所提出方案的脚本，发表于：J. Chem. Phys. 124, 114104 (2006)。该脚本计算分子的精确总能量。

**文件名（Filename）**

ccCA_CBS_2.cmp

**SCRIPT**
```{literalinclude} ../../orca_working_input//compound_library_examples/replaceNewJob.inp
:language: orca
```

**注释（Comments）**

有意思的是，在该方案中处理的是总能量，外推时不区分 HF 能量和相关能。

## 扫描（Scan）
**简介（Introduction）**

这是一维几何扫描的示例脚本。它针对 Ne-Ne 键长设置，但可以修改以适应用户的具体需求。

**文件名（Filename）**

scan_1D_1M_1P.cmp

**SCRIPT**
```{literalinclude} ../../orca_working_input//compound_library_examples/scan_1D_1M_1P.cmp
:language: orca
```

**注释（Comments）**

本脚本有一些有趣的特性。它包含两个变量 *removeFiles* 和 *DoPython*。如果第一个设为 *true*，脚本将使用系统命令删除计算结束后不再需要的文件。后者 *DoPython* 若设为 *true*，则会读取所创建的 *.csv* 文件并写出一个 *python* 文件来绘制结果图。随后它将运行该 python 脚本实际绘图。


## 数值极化率（Numerical polarizabilities）


**简介（Introduction）**

该脚本使用带电场的单点计算来数值计算分子的极化率。

**文件名（Filename）**

numericalPolarizability.cmp

**SCRIPT**
```{literalinclude} ../../orca_working_input//compound_library_examples/numericalPolarizability.cmp
:language: orca
```

**注释（Comments）**

在本脚本中我们还使用了 *Compound* 中提供的线性代数 *diagonalize* 函数。

(sec:workflowsautomatization.compound_examples.iterativeopt)=
## 迭代优化（Iterative optimization）
**简介（Introduction）**

该脚本执行几何优化，然后运行频率计算；如果存在虚频，它会基于 Hessian 调整几何结构并再次优化。

**文件名（Filename）**

iterativeOptimization.cmp

**SCRIPT**
```{literalinclude} ../../orca_working_input//compound_library_examples/iterativeOptimization.cmp
:language: orca
```

## 梯度外推（Gradient extrapolation）

**简介（Introduction）**

该脚本对分子的梯度进行外推。它使用两点外推，其中梯度的 Hartree-Fock 部分和相关部分分别外推。这为使用外推梯度进行几何优化开辟了道路。

**文件名（Filename）**

gradientExtrapolation.cmp

**SCRIPT**
```{literalinclude} ../../orca_working_input/compound_library_examples/gradientExtrapolation.cmp
:language: orca
```

**注释（Comments）**

## BSSE 优化（BSSE Optimization）

**简介（Introduction）**

该脚本使用经过基组重叠误差（Basis Set Superposition Error，BSSE）校正的梯度来优化分子几何结构。基本步骤是使用第二个脚本来计算经 BSSE 校正的梯度。

**文件名（Filename）**

BSSEOptimization.cmp

**SCRIPT**
```{literalinclude} ../../orca_working_input/compound_library_examples/BSSEOptimization.cmp
:language: orca
```

**注释（Comments）**

初始结构应包含一些 ghost 原子。

## 伞形翻转脚本（Umbrella script）
**简介（Introduction）**

该脚本计算 NH_3 中“伞效应（umbrella effect）”的势能。此外，它还定位势能面上的极小点和极大点。

**文件名（Filename）**

Umbrella.cmp

**SCRIPT**
```{literalinclude} ../../orca_working_input/compound_library_examples/Umbrella.cmp
:language: orca
```

## 多参考（Multi reference）
**简介（Introduction）**

这是一个计算自由原子中原子电子密度并建立其库的脚本。

**文件名（Filename）**

atomDensities.inp

**SCRIPT**
```{literalinclude} ../../orca_working_input/compound_library_examples/atomDensities.inp
:language: orca
```

**注释（Comments）**

这里值得注意的是，根据所选原子的不同，脚本要么进行 CASSCF 计算（提供诸如电子数和根数等细节参数），要么进行简单的 Hartree-Fock 计算。


## GoTo
**简介（Introduction）**

这是一个简短示例，演示如何在 *Compound* 中使用 *GoTo* 命令。

**文件名（Filename）**

goTo_Example.inp

**SCRIPT**
```{literalinclude} ../../orca_working_input/compound_library_examples/goTo_Example.inp
:language: orca
```
