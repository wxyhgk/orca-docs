---
title: 输入与输出
source: https://www.faccts.de/docs/orca/6.1/tutorials/first_steps/input_output.html
---

# 输入与输出

## 输入的结构

"!" 之后的所有内容称为 `main input`（主输入），如果需要特定选项，它们通常在以 % 符号开始、以 END 结束的输入块（input block）中设置。

假设在水分子的例子中，想将自洽场（SCF）的最大迭代次数增加到 500，那么输入应为：

```text
!HF DEF2-SVP
%SCF
   MAXITER 500
END
* xyz 0 1
O   0.0000   0.0000   0.0626
H  -0.7920   0.0000  -0.4973
H   0.7920   0.0000  -0.4973
*
```

为了可读性，主输入也可以拆分成多行，例如：

```text
!HF
!DEF2-SVP
%SCF
   MAXITER 500
END
* xyz 0 1
O   0.0000   0.0000   0.0626
H  -0.7920   0.0000  -0.4973
H   0.7920   0.0000  -0.4973
*
```

关于所有主关键词（keyword）和选项的完整讨论，请查阅 [ORCA 手册](https://www.faccts.de/docs/orca/6.0/manual)。

> **注意**
> 输入读取器**不**区分大小写。大写、小写或任意大小写组合都可以。

### 结构部分

在主输入和选项之后是结构部分，由星号分隔。您可以使用 "xyz" 标志以笛卡尔坐标（Cartesian coordinates）形式输入坐标，或使用 "int" 以内坐标（internal coordinates）形式输入。接着是体系的电荷和多重度（multiplicity）（$2S+1$）。

对于用内坐标表示的羟基自由基（$S=1/2$），一个输入可以是：

```text
!HF DEF2-SVP
* int 0 2
O  0 0 0 0.0    0.0 0.0
H  1 0 0 0.9903 0.0 0.0
*
```

> **注意**
> 原子可以用其元素符号（H、C、Cu、Te）或原子序数（1、6、29、52）来指定，坐标必须以埃（Ångström）为单位。

### 从外部文件读取

也可以使用 "xyzfile" 标志从外部 .xyz 文件读取几何结构。在前面的例子中，如果在与输入文件相同的文件夹中有一个 "hydroxide.xyz" 文件，输入应为：

```text
!HF DEF2-SVP
* xyzfile 0 2 hydroxide.xyz
```

在这种情况下，不需要在下方用第二个星号结束该部分。"hydroxide.xyz" 应如下所示：

```text
2

O  0 0 0
H  0 0 0.9903
```

它以原子数目开始，然后是一个空行或注释行，接着是结构——坐标以埃（Angstroem）为单位。

## 输出文件

输出的第一部分是包含贡献者致谢和基组信息的头部。之后是警告（WARNINGS），应仔细检查，然后是：

```text
****************************
* Single Point Calculation *
****************************
```

作为将要执行的计算类型的提示。接着是关于积分模块（SHARK）和 SCF 参数的详细信息：

```text
----------------------
SHARK INTEGRAL PACKAGE
----------------------

Number of atoms                             ...      2
Number of basis functions                   ...     19
Number of shells                            ...      9
Maximum angular momentum                    ...      2
Integral batch strategy                     ... SHARK/LIBINT Hybrid
RI-J (if used) integral strategy            ... SPLIT-RIJ (Revised 2003 algorithm where possible)
Printlevel                                  ...      1
Contraction scheme used                     ... SEGMENTED contraction

[...]

------------
SCF SETTINGS
------------
Hamiltonian:
 Ab initio Hamiltonian  Method          .... Hartree-Fock(GTOs)

General Settings:
 Integral files         IntName         .... orca
 Hartree-Fock type      HFTyp           .... UHF
 Total Charge           Charge          ....    0    
 Multiplicity           Mult            ....    2

[...]
```

然后构建初始猜测（initial guess）：

```text
------------------------------
INITIAL GUESS: MODEL POTENTIAL
------------------------------
Loading Hartree-Fock densities                     ... done
Calculating cut-offs                               ... done
Initializing the effective Hamiltonian             ... done
Setting up the integral package (SHARK)            ... done
Starting the Coulomb interaction                   ... done (   0.0 sec)
Making the grid                                    ... done (   0.0 sec)
Mapping shells                                     ... done
Starting the XC term evaluation                    ... done (   0.0 sec)
Transforming the Hamiltonian                       ... done (   0.0 sec)
Diagonalizing the Hamiltonian                      ... done (   0.0 sec)
Back transforming the eigenvectors                 ... done (   0.0 sec)
Now organizing SCF variables                       ... done
```

如果 SCF 收敛，您将看到一条消息，以及各能量分量的划分：

```text
               *****************************************************
               *                     SUCCESS                       *
               *           SCF CONVERGED AFTER  11 CYCLES          *
               *****************************************************

             **** ENERGY FILE WAS UPDATED (orca.en.tmp) ****

----------------
TOTAL SCF ENERGY
----------------

Total Energy       :        -75.32415421767207 Eh           -2049.67444 eV

Components:
Nuclear Repulsion  :          4.27488404160356 Eh             116.32551 eV
Electronic Energy  :        -79.59903825927563 Eh           -2165.99995 eV
One Electron Energy:       -112.46709636116736 Eh           -3060.38528 eV
Two Electron Energy:         32.86805810189173 Eh             894.38533 eV

Virial components:
Potential Energy   :       -150.52264633450642 Eh           -4095.92944 eV
Kinetic Energy     :         75.19849211683436 Eh            2046.25500 eV
Virial Ratio       :          2.00167107208270
```

接着打印轨道能量（orbital energies），以及电荷和计时信息。如果需要其他方法，如 MP2 或 TD-DFT，它们将随后出现，最终计算出的能量打印为：

```text
-------------------------   --------------------
FINAL SINGLE POINT ENERGY       -75.324154217672
-------------------------   --------------------
```

之后会打印计算性质的概览、偶极矩（dipole moment）以及体系的转动光谱（rotational spectrum）。最后，程序会连同计时一起打印您计算中所用方法和实现的推荐引用文献。关于如何正确引用 ORCA 的更多细节，请参见[如何引用教程](../first_steps/howtocite.md)。

## 可视化程序

如果您想用图形用户界面可视化数据，可以在网上找到许多程序。其中一些已被证明对 ORCA 输出可视化特别有用：[Avogadro](https://avogadro.cc)、[Chemcraft](https://www.chemcraftprog.com/)、[Gabedit](https://sites.google.com/site/allouchear/Home/gabedit/download) 和 [ChimeraX](https://www.rbvi.ucsf.edu/chimerax/)。

详情请参阅[图形用户界面（GUI）](../first_steps/GUI.md)部分。
