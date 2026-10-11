

<a id="sec:running"></a>
# 运行 ORCA

在 Windows 下，程序从命令提示符（command prompt）调用！（请确保 PATH 变量已设置，使 orca 可执行文件可见）

```sh
orca orca.inp > orca.out
```

在基于 UNIX 的操作系统下，以下调用方式比较方便
（同样：请确保 PATH 变量已设置到 orca 可执行文件所在的目录）：

```sh
orca orca.inp >& orca.out &
```

程序输出写入 *stdout* 和 *stderr*。因此在本例中必须将输出重定向到文件 *orca.out*。*orca.inp* 是一个自由格式的 ASCII 文件，包含输入描述。程序会生成若干 *orca.x.tmp* 文件和一个 *orca.gbw* 文件。
"\*.gbw" 文件包含计算的二进制摘要。GBW
代表 "Geometry-Basis-Wavefunction"（几何-基组-波函数）。基本上，该文件中存储的就是这些内容以及计算标志。重启 SCF（自洽场）计算，或以本次计算的轨道作为输入开始其他计算时，都需要用到该文件。"\*.tmp" 文件是临时文件，包含积分、Fock 矩阵等在计算中用作中间量的内容。如果程序正常退出，所有这些文件都会被删除。如果程序意外崩溃，您必须手动删除这些文件（在 Unix 下用 `rm orca*.tmp`，在 Windows 下用 `del orca*.tmp`）。如果您想在输出文件写入的同时监控它，可以使用命令（在 Unix 下）：

```sh
tail -f orca.out
```

以跟踪（选项 -f）计算的进展。在 Windows 下，您需要打开另一个命令行窗口并使用：

```bat
type orca.out
type orca.out |more
```

或者将输出文件复制到另一个文件中，然后用任意文本编辑器查看。

```bat
copy orca.out temp.out
edit temp.out
```

您不能使用 `edit orca.out`，因为这会导致共享冲突（sharing violation）。

<a id="sec:exampleinput"></a>
## 一个简单示例

ORCA 的一大优势在于其输入文件结构简单。ORCA 输入文件可以轻松地用任何简单文本编辑器生成。
只需创建一个扩展名为 `.inp` 的文件，例如 `orca.inp`，然后在其中添加输入信息。最基本的输入文件如下所示：

```orca
! METHOD

*XYZ CHARGE MULTIPLICITY
Atom1   X1  Y1  Y1
Atom2   X2  Y2  Y2
*
```

在此，我们通过以感叹号开头的所谓*简单输入行（simple input line）*来定义所选的量子力学方法。随后，我们定义分子的结构、净电荷和多重度（multiplicity，M = 2S+1）。在本例中，我们选择了 XYZ 格式的笛卡尔坐标（cartesian coordinates），单位为埃（Å）。
坐标块必须以 `*` 结束。

以 Hartree-Fock 理论和 def2-SVP 基组（basis set）计算中性单重态氢分子的示例如下：

```mol
title: structure 1
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
2
structure (0 1)
H             0            0            0
H          0.74            0            0
--- input ---
! HF DEF2-SVP

*XYZ 0 1
H   0  0  0
H   0.74  0  0
*
```

关于 ORCA 输入文件语法的更多细节，请参见 [sec:essentialelements.input](#sec:essentialelements.input) 一节，
[sec:hellowater](#sec:hellowater) 一节将带您完成使用 ORCA 的第一步。
