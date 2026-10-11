---
title: Hello water！您的第一个 ORCA 计算
source: https://www.faccts.de/docs/orca/6.1/tutorials/first_steps/first_calc.html
---

# Hello water！您的第一个 ORCA 计算

交互式结构（切换标签页可复制 ORCA 输入）：

```mol
title: 水分子
theme: chem311
height: 360px
representation: ball-stick
--- xyz ---
3
water
O   0.0000   0.0000   0.0626
H  -0.7920   0.0000  -0.4973
H   0.7920   0.0000  -0.4973
--- input ---
!HF DEF2-SVP
* xyz 0 1
O   0.0000   0.0000   0.0626
H  -0.7920   0.0000  -0.4973
H   0.7920   0.0000  -0.4973
*
```

我们的第一个计算将是水分子的能量，使用哈特里-福克（Hartree-Fock）理论和 DEF2-SVP 基组（basis set）。运行 ORCA 所需要的只是一个输入文本文件，例如这个 `water.inp`：

> **注意**
> 输入文件通常使用 .inp 扩展名，但 .txt 也可以。

我们强烈建议为每次计算创建一个新文件夹。在本例中，我们将在一个名为 `firstcalc` 的新目录中创建输入文件并切换到该目录。

Linux/Mac：

```text
mkdir ~/firstcalc
cd ~/firstcalc
```

Windows：

```text
mkdir C:\firstcalc
cd C:\firstcalc
```

（要找到 Windows 命令提示符，请按 Windows 键并输入 "prompt"。）

现在您可以运行 ORCA 了。首先，请确保它已正确安装并且系统路径（PATH）已设置（参见[设置 PATH 变量](../first_steps/trouble_install.md#path-variable)）。

```text
orca water.inp
```

输出随后会打印在屏幕上。

## 将输出保存到文件

要将输出保存到文本文件 `water.out` 中，请使用 `>` 运算符（在 Linux/Mac 和 Windows 上均适用）：

```text
orca water.inp > water.out
```

然后您可以打开该文件查看输出（注意不要在计算运行时覆盖它）。关于输入和输出分析的更多内容见[下一篇](../first_steps/input_output.md)。

> **注意**
> 目前您不需要担心安装文件夹中的其他程序，ORCA 会在需要时自动调用正确的程序。
