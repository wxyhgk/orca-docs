

<a id="sec:quickstartguide.troubleshooting"></a>
# ORCA 问题排查

在刚开始使用 ORCA、初次尝试某些功能，
或深入进行计算研究时，您可能会遇到
需要排查的问题。本节汇总了典型的
错误来源以及会遇到的错误信息，以帮助
排查常见问题。

!!! note
    本节旨在成为不断扩充的常见问题示例库。如果您
    在此无法找到问题的解决方案，请在 [ORCA 论坛](https://orcaforum.kofo.mpg.de/)
    上发帖，简要描述您的问题，并尽可能附上能展示
    该问题的输入和/或输出文件。如果某类问题出现得足够频繁，
    它将被收录到本节中用于未来版本！

## ORCA 根本不运行……

如果 ORCA 似乎根本没有运行，请确保路径变量已正确设置（参见
[sec:installation](#sec:installation) 一节），并且您的系统上没有其他程序干扰
ORCA 的使用。一个例子是存在另一个名为 ORCA 的程序。要检查是否属于这种情况，请确认
`which orca` 或 `where orca`（或其等效命令）输出的是正确的 ORCA 可执行文件。如果
不是，请在运行作业时尝试使用 ORCA 可执行文件的完整路径。如有疑问，请查阅
关于 [sec:running](#sec:running) 的部分。

如果 ORCA 串行运行正常，但并行运行不行，首先请确保您没有用 mpirun 运行
主 ORCA 可执行文件。主 ORCA 驱动程序需要以串行方式运行，并且会
根据输入文件中的请求并行调用不同的模块。如果您尝试用
mpirun 运行，通常会得到如下输出
```orca
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!                        FATAL ERROR ENCOUNTERED               !!!
!!!                        -----------------------               !!!
!!!                          I/O OPERATION FAILED                !!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
```
而且您可能还会收到来自 prterun/mpirun 的错误。如果有任何输出产生，它可能会
被多次重复。

要并行运行 ORCA，您还必须提供 ORCA 可执行文件的完整路径。简单地
使用 `orca` 会导致如下错误：
```orca
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!     ERROR (ORCA_MAIN): For parallel runs                     !!!
!!!     ORCA has to be called with full pathname                 !!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
```
更多技巧请参见 [sec:essentialelements.parallel.hints](#sec:essentialelements.parallel.hints)。

## 我的 ORCA 输出在哪里？

如果您运行了 ORCA，看到生成了一些文件，但找不到输出文件本身，
那么您很可能是在没有将输出重定向到文件的情况下运行 ORCA。参见 [sec:running](#sec:running)
了解操作说明。

然而，如果您缺少的是其他本应由 ORCA
生成的文件，而且您使用的是提交脚本，请确保该脚本
正在从实际运行作业的位置复制所有相关文件。

## ORCA 突然终止

当 ORCA 意外终止时，一般建议是始终查看输出的
最后几行——ORCA 通常会告诉您发生了什么！
例如，
```orca
            !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                                 INPUT ERROR
            UNRECOGNIZED OR DUPLICATED KEYWORD(S) IN SIMPLE INPUT LINE
                       PAL12 
            !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
[file orca_main/main_input_keywordline.cpp, line 13941]: 
```
告诉我们关键词 `PAL12` 未被识别。这是因为
只有针对较常见处理器数量的简单关键词。
此时查阅手册（例如搜索 "parallel" 或 "processors"）
告诉我们只有 "PAL2 to PAL8 and PAL16, PAL32, PAL64" 是
可识别的简单输入。手册的同一部分还展示了如何使用
`%pal` 输入块中的 `nprocs` 关键词来指定
任意数量的处理器。

然而，也有一些情形下不会打印明确的错误信息。
它可能看起来像这样：
```orca
ORCA finished by error termination in <ORCA MODULE>
Calling Command: mpirun -np 8 /path/to/orca/module myjob.moduleinp.tmp myjob
[file orca_tools/qcmsg.cpp, line 394]:
.... aborting the run".
```

此时，查看 ORCA 在启动时发出的警告会非常
有帮助。它位于输出文件中标题为 `WARNINGS` 的部分——就在
ORCA 贡献者列表之后、输入文件副本之前：
```orca
===========================================================================
                                   WARNINGS
                  Please study these warnings very carefully!
===========================================================================
WARNING: Geometry Optimization
  ===> : Switching off AutoStart
         For restart on a previous wavefunction, please use MOREAD
```

如果 ORCA 发现了某些异常，但决定不终止、
而是假定这是用户的本意，这一点尤其有帮助。

其他警告可能在启动警告之后发出。在输出中搜索
其他 `WARNING` 出现之处，以查看 ORCA 在计算过程中将哪些问题标记为可能的隐患。
这可能包括但不限于：(CAS)SCF、CPSCF 或 CC 迭代不收敛、基组中的线性
相关（linear dependence），以及内存问题。几何
和/或 SCF 运行收敛不佳的典型特征包括例如：
```orca
                                   *** Resetting DIIS ***
 WARNING: the maximum gradient error descreased on average only by a factor   0.9
          during the last 20 iterations
                      *** Initiating the TRAH-SCF procedure ***
```
或
```orca
  0    -4604.304089906417    2.255713e+02                    0.400 (TRAH MAcro)   No
WARNING : negative HOMO - LUMO gap : -60.865582
  0   dE    -8.949363e+01    1.445336e+01    -5.5474e+02     0.400 (TRAH MIcro)
```

接下来，请检查问题是否可能来自 ORCA 之外。例如，
如果您超出了提交 ORCA 作业所用排队系统的时间、磁盘或
内存限制，系统（有时甚至是管理员）会终止您的作业。在这种
情况下，可能没有错误信息，或者只有来自排队系统或系统 shell 的错误信息。
您看到的错误信息形式取决于您的操作系统以及排队系统
的设置方式。排队系统也可能将错误收集在单独的文件中。

## 输入文件语法不正确

以下各小节探讨输入文件中的常见语法错误。一般而言，
参考 [sec:essentialelements.input](#sec:essentialelements.input) 和 [sec:essentialelements.coordinates](#sec:essentialelements.coordinates) 两节可能会有所帮助。

### 未知的简单输入关键词
如上所示，与无法识别的简单输入关键词相关的典型错误信息是
```orca
            !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                                 INPUT ERROR
            UNRECOGNIZED OR DUPLICATED KEYWORD(S) IN SIMPLE INPUT LINE
                       <KEYWORD>
            !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
```

### 未知的输入块关键词
输入文件语法的另一个问题可能是输入块中存在无法识别的关键词。
其错误信息通常是
```orca
         Unknown identifier in <BLOCK_NAME> block line <LINE_NUMBER>  :
         Last token : <KEYWORD>
```
如果您确定该关键词存在，请检查是否已用 `end` 语句关闭了所有
输入块。此外，输入块中可能还有一些子块需要
`end` 语句。

### 缺少必需的输入
最佳实践是所有 ORCA 输入文件至少指定三件事：(1) 一个几何结构，(2) 要运行的方法，
以及 (3) 一个基组。(1) 可以在 `%coords` 块中设置，或使用简单输入语法。它也可以从
外部文件读取。(2) 和 (3) 可以使用简单输入关键词或其相应的输入块来设置。
请参见 [sec:essentialelements.input](#sec:essentialelements.input)、[sec:essentialelements.coordinates](#sec:essentialelements.coordinates)、
[sec:essentialelements.basisset](#sec:essentialelements.basisset) 各节，以及手册中所需方法的相应部分。

如果未指定方法或基组，通常不会有错误信息，
而是设置一个默认值。在这些情况下，仔细检查输出非常重要！
但是，缺少几何结构以及某些辅助基组没有默认值，会导致错误。
以下是这些问题所遇错误的示例。

缺少几何结构：
```orca
You must have a [COORDS] ... [END] block in your input
```
缺少辅助基组（在主检查中捕获）：
```orca
ERROR: RI-MP2 needs an AuxC basis but none was defined!
```
缺少辅助基组（由 SHARK 捕获）：
```orca
Error (TMOIntegrals): Aux/C requested but not available in SHARK
ORCA finished by error termination in <MODULE>
```
如果不确定使用哪个辅助基组，`!AutoAux` 是一个便捷的功能。请注意，
这些自动生成的辅助基组可能会导致线性相关问题。

此外，如果原子 `Xx` 未在所提供的基组中定义，会给出如下错误：
```orca
               *****************************************************************
               ** There are no main   basis functions on atom number   0 (Xx) **
               *****************************************************************
    The basis set was either not assigned or not available for this element - Aborting the run
```
这可以通过以下方式修复：(1) 改用一个定义了该元素的基组，或 (2) 对所有其他元素使用所请求的
基组，仅为该元素指定另一个基组。这可以通过
使用 `NewGTO` 来实现（参见[为元素指定基函数](#sec:essentialelements.basisset.element)）。

当所选方法使用交换积分（exchange integral）时，仅仅请求 `RI` 也会导致 ORCA 中止，
因为它不知道如何处理这些积分。错误信息给出了用户可以
指定的选项：
```orca
Error: RI is on but the HF exchange must be handled somehow
Use one of the keywords
     RIJDX  : treat the HF exchange exactly (equals RIJONX)
     RIJCOSX: treat the HF exchange by chain-of-spheres
     RIJK   : treat Coulomb and exchange both by RI
```

根据所运行的方法以及指定了哪些其他关键词，可能还需要其他输入。
在这些情形的大多数情况下，ORCA 输出的错误应当是不言自明的。
例如，此错误可能形如：
```orca
         Error: Missing keyword in <BLOCK_NAME> block                   
         Missing keyword : <KEYWORD>
```

### 缺少 `end` 语句
如果缺少用于关闭输入块的 `end` 语句，可能会出现若干错误。
通常，人们会遇到 `Unrecognized symbol` 错误，其中下一个符号被解释为
上一个输入块的一部分。此错误的形式为：
```orca
         Unrecognized symbol in <BLOCK_NAME> block line <LINE_NUMBER>  :
         Last token : %
```
也可能得到更明确的错误信息：
```orca
         'END' was expected at the end of the <BLOCK_NAME> block line <LINE_NUMBER>  :
         Last token : <PREVIOUS_KEYWORD>
```

### 符号缺失或多余
正如 `end` 语句不足会导致错误一样，`end` 语句过多也会如此。
例如，有些输入如 `%base`、`%moinp` 和 `%MaxCore` 是全局变量而不是输入块。
因此它们不期望有 `end` 语句。在这种情况下，错误可能形如：
```orca
ERROR: expect a '$', '!', '%', '*' or '[' in the input
       Line <LINE_NUMBER> of <INPUT_FILE> (END)
```
这里，ORCA 没有预料到又一个关键词，而是在寻找一个能
开启新输入块、几何块等的符号。

相反，如果您在输入块之外提供关键词、忘记简单输入行开头的 `!`、忘记几何块的 `*`，或者写了不带 `#` 的注释，您会得到
与上面相同的错误信息，只是用缺失符号之后遇到的第一个关键词代替 `END`。

尝试读取外部文件通常要求文件名用引号括起来。例如，如果 `%moinp` 关键词缺少引号，错误信息为：
```orca
Error: Quotes expected after scanning %%moinp
```
一个例外是，在简单几何输入部分（例如通过 `*xyzfile`）不应为外部坐标文件指定引号。

### 无法识别的符号
另一个问题是出现了超出 ORCA 预期的多余符号。
一个常见的例子是简单坐标输入：它以星号开始，如果您在输入文件中提供坐标，则在新的一行以星号结束。然而，从外部文件读取坐标
——例如使用 `*xyzfile` 语法——的同时又提供第二个星号（在新的一行）会给出如下错误：
```orca
ERROR: found a coordinate definition line (* ctyp charge mult)
   but could not read ctyp, charge and multiplicity
```

用 `%%` 而不是 `%` 来开启输入块，或者输入文件中有多余的 `%`，会导致如下错误：
```orca
Error: expected an identifier after '%%' in the input
```
不过，简单输入关键词用 `!!` 代替 `!` 会给出无法识别的关键词错误，因为
它把第二个感叹号解释为自己的关键词。ORCA 未预期的其他符号会给出如下错误：
```orca
ERROR: expect a '$', '!', '%', '*' or '[' in the input
```

### 无法打开文件
如果需要 ORCA 从另一个文件读取，当指定的文件不存在时您会遇到错误。例如，使用 `*xyzfile 0 1 geom.xyz` 在 `geom.xyz` 不存在时会给出如下错误
```orca
ORCA_ReadXYZFile::Error
There was a problem reading file: geom.xyz
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!                        FATAL ERROR ENCOUNTERED               !!!
!!!                        -----------------------               !!!
!!!                           CANNOT OPEN FILE                   !!!
!!!               Filename: geom.xyz                                   !!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
```
如果文件存在但文件名周围加了引号，也可能看到同样的错误。在这种情况下，错误信息中的文件名输出会包含引号。

此外，如果坐标通过简单几何输入块在输入文件中指定，但所用关键词却表明 ORCA 应从外部文件读取，您也可能遇到此错误。例如，使用 `*xyz`
坐标语法却搭配关键词 `*xyzfile` 会给出如下错误：
```orca
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!                        FATAL ERROR ENCOUNTERED               !!!
!!!                        -----------------------               !!!
!!!                           CANNOT OPEN FILE                   !!!
!!!               Filename:                                    !!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
```
其特征是文件名缺失，因为使用了 `*xyzfile`，但并未提供外部文件。

其他文件类型可能有不同的错误信息。例如，如果用 `%moinp MOs.gbw` 读入 GBW 文件，
但 `MOs.gbw` 不存在，会给出如下错误：
```orca
Cannot open GBW file: MOs.gbw
```

### Windows 机器上的文件结束符（EOF）问题
如果在 Windows 机器上运行 ORCA，当输入文件不以空行结尾时，您可能会遇到问题。常见的情形是最后一行试图从外部文件读取坐标，导致错误信息声称文件缺失。如果在输入文件末尾添加空行没有帮助，也可以尝试在 ORCA 要读取的（用户创建的）外部文件末尾添加空行。

### 非 ASCII 字符
如果尝试在输入文件中使用非 ASCII 字符，您也可能收到错误。
在较旧的 ORCA 版本中，不检查非 ASCII 字符，这可能导致看似有效的关键词被标记为无法识别。
自 ORCA 6.0.1 起，会打印一条有用的错误信息来帮助定位这些字符：
```orca
ERROR: non-ASCII character(s) found in words on line <LINE_NUMBER>: 
<KEYWORD W/ NON-ASCII> Please remove all non-ASCII characters from your input file
```
尤其难以发现的是不换行空格、短横线和长横线以及各种引号这类非 ASCII 字符，因为它们看起来与 ASCII 对应字符非常相似。

## 内存不足（OOM）

如果未给出 `%MaxCore`，或者可用于继续计算的内存不足，
典型的错误信息是 `Please increase MaxCore`。这通常发生在
ORCA 试图估算所需内存并发现 `MaxCore`
不够的时候。

!!! note
    `MaxCore` 的单位是 MB，是**每个处理核心**要分配的最大内存量！
    ORCA 在计算过程中也可能超出 `MaxCore`，而且并非对所有方法都进行了相应设置。因此，一般建议将
    `MaxCore` 设置为满足 `MaxCore * nprocs <= 0.75(Available Memory)`。

对于某些方法，ORCA 会在计算早期估算所需内存。如果该估算大于 `MaxCore`，但小于
2 倍的 `MaxCore`，ORCA 会发出警告并继续。但如果估算大于
2 倍的 `MaxCore`，ORCA 将中止。届时您必须在输入文件中增大 `MaxCore`
并重新运行作业。

在某些情况下，这种对所需内存的粗略估算还不够，
ORCA 在计算过程中意识到没有足够内存
继续。这样的错误可能形如：

```orca
[file orca_tools/qcmem.cpp, line 949, Process 7]:  OUT OF MEMORY ERROR! 

--------------------------------------------------------------------------
Primary job  terminated normally, but 1 process returned
a non-zero exit code. Per user-direction, the job has been aborted.
--------------------------------------------------------------------------
--------------------------------------------------------------------------
mpirun noticed that process rank 0 with PID <PID> on node <NODE> exited on signal 11 (Segmentation fault).
--------------------------------------------------------------------------
4 total processes killed (some possibly by mpirun during cleanup)

ORCA finished by error termination in SCF
Calling Command: mpirun -np 8  /path/to/orca_scf_mpi myjob.gbw b myjob 
[file orca_tools/qcmsg.cpp, line 458]: 
  .... aborting the run
```
请注意，根据所运行的方法，`OUT OF MEMORY ERROR` 信息可能不会出现在输出中。

## 磁盘写满

某些 ORCA 计算需要向磁盘写入大量数据。这些数据可能是计算期间使用、
之后删除的临时文件，也可能是计算结束后仍保留的文件。
如果在计算过程中某个时刻磁盘写满，ORCA 将中止。这可能悄无声息地发生（没有
明确的错误信息），也可能伴随一条通常提到无法写入矩阵或
设置指针的错误信息。例如：
```orca
Error TMatrixContainers::AddMatrix - Failed to add <INDICES> to <TMP_FILE>
```
或
```orca
Error TMatrixContainers::AddMatrix - Failed to set FilePointer
```

## 基组线性相关

如果所用基组中的某些函数（几乎）线性相关，可能会导致计算中的数值问题。这更常见于带弥散函数（diffuse function）的基组和由 `!AutoAux` 生成的辅助基组。ORCA 和 SHARK 会尝试尽早捕捉这些问题。例如，您可能会在输出中看到
```orca
WARNING! Potentially linear dependencies in the auxiliary basis
===>>    At the moment, SHARK is not equipped to deal with this
  ... sorry, have to bail out
```
然而，这有时捕捉不到，并可能导致数值不稳定，甚至在后续过程中使 ORCA 中止。例如，可能遇到如下问题：
```orca
Diagonalization failed with error code: -5 !
```
此时输出中需要检查的一部分是重叠矩阵（overlap matrix）的对角化。非常小的
本征值可能指向线性相关问题。这段输出可能形如：
```orca
Diagonalization of the overlap matrix:
Smallest eigenvalue                        ... 3.064e-08
Time for diagonalization                   ... 3.223 sec
Threshold for overlap eigenvalues          ... 1.000e-07
Number of eigenvalues below threshold      ... 3
Smallest eigenvalue above threshold        ... 1.002e-07
```
有一些选项可以帮助缓解线性相关问题，在
[sec:essentialelements.lindep](#sec:essentialelements.lindep) 一节中有更详细的说明。

## 分子对称性与预期不符

如果以对称性（通过 `!UseSym`）运行 ORCA，请务必检查 `Auto-detected point group`（自动检测的点群）与
预期是否一致。由于数值噪声，输入几何结构可能并不完全对称。在这种情况下，
放宽点群识别的阈值（例如用 `%sym SymThresh 0.01 end`）应当
能得到预期的点群，ORCA 将使用一个对称性完美的几何结构进行计算。更多信息
请参见 [sec:essentialelements.symmetry](#sec:essentialelements.symmetry) 一节。

## 使用旧的 ORCA 输入

如果尝试将旧的 ORCA 输入文件与较新版本的 ORCA 一起使用，
您可能会发现它无法运行。通常在这种情况下，计算启动过程中会发出
一条错误信息。该信息
应能帮助您排查问题。

这里，问题通常是由于关键词和默认值可能
从一个版本到另一个版本发生了变化。在某些情况下，某个关键词甚至可能
已被弃用。更新到新的 ORCA 版本时，
参考 [sec:appendix.changelog](#sec:appendix.changelog) 往往很有帮助，因为许多此类变更都有记录。

如果尝试读入来自另一 ORCA 版本的 GBW 文件，您可能会
遇到如下错误：
```orca
WARNING!!!!!!!
Your GBWFile is either corrupt or from a different ORCA version!
Please be VERY careful with your calculation results!!!

Data_size, sizeof( TOrcaInfo ): 974880, 980832

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!                        FATAL ERROR ENCOUNTERED               !!!
!!!                        -----------------------               !!!
!!!                          I/O OPERATION FAILED                !!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
```
这在使用 `!MORead` 或使用 ORCA 工具程序（如 `orca_plot`）时尤其常见。在为后续
计算读入初始轨道的情况下，附加关键词 `!Rescue` 可能会有帮助。请注意，这样做时
执行的检查更少，因此务必确保 GBW 文件所代表的
体系与当前输入文件兼容。

对于用 `orca_plot` 绘制轨道和某些密度的情形，
您可以使用与产生 GBW 文件的版本相同的 ORCA 版本，
或者通过在输入文件中使用 `!Rescue MORead NoIter`
（并经由 `%moinp` 关键词读入 GBW 文件），用较新的 ORCA 版本运行一次计算。该计算
不应耗时很久，而且新产生的 GBW 文件应能被 `orca_plot` 读取。请注意
在这种情况下，所有其他设置都应与产生旧 GBW 文件的那次计算
保持一致。

如果对某个输入不确定，请首先查阅本 ORCA 手册的相关部分。
它由 ORCA 开发者提供，应包含本版 ORCA 中已实现功能的
全部信息。同样重要的是，要参考您所使用 ORCA 版本对应的 ORCA 手册。如果您正在在线查看本手册，而
使用的并非最新发布版本的 ORCA，请更新您的 ORCA 版本，或找到
与您所用版本对应的 ORCA 手册。如果仍然无法让输入文件
正常工作，[ORCA 论坛](https://orcaforum.kofo.mpg.de/) 是寻求解答的绝佳去处！

## 复现其他程序包或旧版 ORCA 的结果

结果的可复现性是科学的基石，因此当从一个程序切换到
另一个程序、或从一个 ORCA 版本切换到另一个版本时，比较结果是
良好的做法。如果您正在
尝试这样做，并观察到偏差比预期的大，
这里有一些提示和技巧。

较新版本的 ORCA 可能包含对默认设置的更改，这可能影响
数值结果。例如，ORCA 6 对数值积分格点（numerical integration grid）做了改进。
在大多数情况下，这些更改应带来更好的结果，而且极可能是
最新 ORCA 发布版与先前版本之间存在差异的原因。通常可以
手动将这些值设回旧的默认值以便比较。在进行此类检查时，
请比较输出中的信息以查看哪些值发生了变化。参考本手册的相关章节
以确定如何更改这些值。

在尝试用 ORCA 复现另一程序的结果（或反之）时，
重要的是检查所用方法确实等价，
并且两个程序以相同的方式计算所讨论的数值。
这可能意味着要使用一些您平时不会使用的设置，以确保
两者具有可比性。例如，ORCA 对所有基组使用纯 d 和 f 函数
（即 5 个 d 函数和 7 个 f 函数，而非笛卡尔坐标的 6 个 d 函数和
10 个 f 函数），因此在与不这样做的程序比较时
应考虑到这一点。

如果仍然遇到可复现性问题，请在 [ORCA 论坛](https://orcaforum.kofo.mpg.de/) 上发帖，
并提供足够详细的信息说明正在比较什么，以便其他用户和开发者
能够提供帮助。附上输入和/或输出文件通常会很有帮助。

## 找不到轨道

如果遇到如下错误：
```orca
No orbitals were found in the gbw file
```
这极有可能是您试图用 `!MORead` 读入一个与当前输入文件
同名（basename 相同）的 GBW 文件。ORCA 的
AutoStart 功能（默认开启）会自动完成此事，因此您只需移除输入文件中 `!MORead`
和 `%moinp` 部分即可。如果您想保存先前的轨道（以便
日后访问）并将其读入，请将 GBW 文件复制为具有不同 basename 的文件，然后
照常读入该文件。

## 重启输入文件时的困难

另一个 AutoStart 相关问题是：当您对输入文件做了重大更改
并尝试重新运行，却没有删除旧的 ORCA 输出文件时。这通常发生在
几何结构存在显著不匹配时——例如原子被
重新排序或删除。在这种情况下，遇到的错误是：
```orca
Error: Input geometry does not match current geometry
```
通常，更改基组不会有问题，因为 ORCA 会在需要时
将旧轨道投影到新的基组上。

如果重启文件时出现问题，您总可以通过在输入文件中添加 `!NoAutoStart`，
或在重新运行前删除所有与输入文件同名的其他文件，来从头运行作业。

## SCF 收敛问题

对于电子结构复杂的体系（如过渡金属配合物或在狭窄能量范围内有许多轨道的体系
（例如金属团簇）），一个典型问题是 SCF 收敛不佳。虽然 ORCA 提供了
像 `!SlowConv` 这样的关键词，但这可能不是最佳选择。具体而言，`!SlowConv` 可能
会收敛到一个更接近初始猜测的局部极小解。
我们在[收敛 SCF 计算](#sec:essentialelements.scfconvergence.tips)一节中汇总了一些提示和技巧。

### 示例：开壳层过渡金属的 DFT 收敛
由于 DFT 经常应用于开壳层（open-shell）过渡金属，我们
在此展示一个用 DFT 处理 Cu(II) 配合物的（多少有些平凡的）示例：

```mol
title: structure 1
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
5
structure (-2 2)
Cu            0            0            0
Cl         2.25            0            0
Cl        -2.25            0            0
Cl            0         2.25            0
Cl            0        -2.25            0
--- input ---
*xyz -2 2
  Cu  0     0     0
  Cl  2.25  0     0
  Cl -2.25  0     0
  Cl  0     2.25  0
  Cl  0    -2.25  0
*

%compound
NewStep
  !BP86 SV SlowConv  
StepEnd

ReadMOs(1);
NewStep
  ! B3LYP NoRI TZVP TightSCF 
  %scf GuessMode CMatrix end
StepEnd
EndRun
```

虽然对这个特定示例而言并非必要，但它展示了
收敛此类计算的一种可行方法。我们首先使用 RI 近似、一个 GGA
泛函和不含极化函数的小基组执行一次精度较低
（但更快）的作业。请注意
这里使用了较大的阻尼因子（damping factor）来引导
计算（`!SlowConv`）。

第二个作业以第一个作业的轨道作为输入，执行一次更精确的
杂化 DFT 计算。在这个气相二价阴离子（dianion）计算中，
一个微妙之处在于输入设定 `GuessMode CMatrix`，它请求使用相应的
轨道投影（orbital projection）。这会将小基组计算的轨道
与大基组的轨道相匹配。当小基组计算的轨道能量
为正时（阴离子即是如此），这总是必需的。

## 棘手的几何优化

虽然优化作业中的一些问题会给出上文已涵盖的错误，
但也可能出现不产生错误信息、也不终止 ORCA 的问题。
在某些情况下，您可能得到正常终止，但所获结果
并不有效。人们往往必须依靠化学直觉来判断几何
优化是否给出了合理的结构和频率。

### 优化后出现虚频
如果几何优化正常终止，说明算法已判定它足够
接近势能面（potential energy surface）上的一个驻点（stationary point）。要检验该驻点是
极小点、极大点还是过渡态（transition state），或检查结构距该驻点有多近，
必须运行一次频率计算。这可能会给出虚频（imaginary frequency）（由于负的
力常数（force constant）而产生，因为频率正比于力常数的平方根），表明我们
并不处于极小点。

```orca
-----------------------
VIBRATIONAL FREQUENCIES
-----------------------

Scaling factor for frequencies =  1.000000000  (already applied!)

   0:         0.00 cm**-1
   1:         0.00 cm**-1
   2:         0.00 cm**-1
   3:         0.00 cm**-1
   4:         0.00 cm**-1
   5:         0.00 cm**-1
   6:        -5.66 cm**-1 ***imaginary mode***
   7:        14.88 cm**-1
   8:        21.54 cm**-1
```

有几种处理此问题的方法。通常，使用更严格的优化判据、
更精确的 DFT 格点和/或更严格的 SCF 收敛判据会有所帮助，对小的虚频尤其如此。
另一种方法是识别与虚频相关的简正模式（normal mode），
沿这些矢量对分子进行畸变，并重新优化结构。请注意 compound
脚本 [sec:workflowsautomatization.compound_examples.iterativeopt](#sec:workflowsautomatization.compound_examples.iterativeopt) 正是以
自动化方式执行这一过程。

### 得到不想要的局部极小
如果您得到的优化几何结构不是所期望的，您可能碰上了
势能面上一个邻近的局部极小（local minimum）。在优化具有许多旋转异构体（rotamer）的分子时，
这很常见。

首先，检查您提供的输入几何结构是否合理地
接近您所瞄准的构象。用低成本方法对结构进行预优化可能会有所帮助。如果目标是全局极小（global minimum），可以利用 [GOAT](#sec:structurereactivity.GOAT)
将结构预优化到一个合理的全局极小猜测。

如果优化过程中出现对称性破缺（symmetry breaking），而您希望强制保持原始点群，
请查看 [sec:essentialelements.symmetry.geomopt_using_sym](#sec:essentialelements.symmetry.geomopt_using_sym) 中的选项。

### 优化收敛问题
当计算在设定的最大迭代次数内无法达到优化收敛判据时，您有几种选择。检查优化
轨迹上最后一次单点的几何结构。如果直觉上它已接近驻点，请尝试从该
几何结构重新开始优化。这等同于重新运行原始输入文件，但增加
优化中的迭代次数。

另一种方法是先用较便宜的方法和/或较小的基组优化，然后用
该几何结构在所需理论水平上进行优化。也可以先用较宽松的收敛阈值进行优化，然后再根据需要收紧。

如果这些提示都无济于事，可以通过分析优化轨迹来识别
结构中出现问题的部分。优化可能在末期卡在
势能面几乎平坦或有许多浅极小的区域——例如具有许多旋转异构体的结构
或多分子体系。在这种情况下，可能需要设置一些合理的几何约束（geometry constraint）。
改变信赖半径（trust radius）或内坐标中的最大步长（maximum step）也可能是明智的。在某些情况下，
甚至可能需要通过 `!COPT` 进行笛卡尔坐标优化（cartesian optimization）。

更多细节请参见 [sec:structurereactivity.optimization](#sec:structurereactivity.optimization) 一节，
尤其是 [sec:structurereactivity.optimization.keywords](#sec:structurereactivity.optimization.keywords) 部分。

## 能量与性质结果"奇怪"

如果能量或性质的结果看起来不对，首先请确保所用的几何结构、自旋多重度（spin multiplicity）和电荷
对手头的体系是合理的。确保输入是对您试图建模的
真实体系的良好近似。为此，请考虑使用溶剂模型（solvent model）是否合适。这对带电体系尤其重要。对于平均场（mean-field）方法，如果尚未包含色散校正（dispersion correction），也请考虑使用。
如果体系中包含重元素，标量相对论（scalar relativistic）方法可能是合适的，可能还需要图像变换（picture-change）
和有限核（finite nucleus）校正。

接下来，确保 SCF 收敛良好。对于性质以及后 Hartree-Fock（post-HF）
的能量和性质，SCF 应收敛得足够紧，使后续计算不至于受
底层 SCF 结果数值噪声的影响。宽松的收敛阈值最终会影响
由 SCF 结果导出的性质。

对于非限制性（unrestricted）方法，建议查看输出中计算出的自旋污染（spin contamination）。如果它很显著，
则用该方法得到的该体系结果可能不可靠。在这种情况下，分析输出文件时应格外小心。在某些情况下，体系的底层表示有缺陷或不完整，但在另一些情况下，
您可以考虑改用给出纯自旋态（pure spin state）解的方法，如 ROHF、ROKS 或多参考（multireference）方法。

一般而言，使用单参考（single-reference）方法时，应当质疑该体系是否可能表现出多参考特征。
在这种情形下，单参考方法的结果可能不可靠。为帮助判断这一点，可以计算若干
诊断量。运行耦合簇（coupled cluster）计算时，通常使用 $T_1$ 诊断（T1 diagnostic）来
估算静态相关（static correlation）在体系描述中的重要性。运行耦合簇计算时会打印计算出的数值，如果大于 0.02，该体系**可能**具有多参考特征。更可靠的是
较新的 S 诊断（S-diagnostic），可通过 `%mdci DoSDiagnostic true end` 请求。详见
[耦合簇 S 诊断](#sec:modelchemistries.CCsDiagnostic)一节。

运行多参考计算时，重要的是确保最终的活性空间（active space）合理，
并包含所有对静态相关有重要贡献的轨道。这可能需要更改 `nel` 和 `norb`。
这里良好的起始轨道很重要（参见[初始猜测的选择](#sec:essentialelements.initialguess)一节）。
起始轨道也可以从其他计算生成——例如使用 MP2 自然轨道（natural orbital）或
UKS 的 QRO——这往往代表物理上更相关的起始猜测。[AVAS](#sec:modelchemistries.casscf.avas) 有助于
从这些起始猜测构建活性空间，前提是您能直观地确定
贡献于要纳入活性空间的 MO 的原子轨道（AO）。请注意，即使某个活性空间看起来
合理，当某些活性轨道占据数非常高/极低时，CASSCF 或后 CASSCF 计算中
仍可能出现收敛问题。最后，还应考虑对于该体系而言，特定态（state-specific）解还是
态平均（state-averaged）解最为合适。这里可能需要更改的关键词是 `nroots`、`mult`、`weights` 和 `irrep`。

最后，还应检查所用方法对手头的体系是否合适。例如，
MP2——CCSD(T) 程度较轻——在轨道简并（orbital degeneracy）方面存在问题。对于性质，线性响应（linear response）
和态求和（sum-over-states）结果仅对没有低激发态的体系可靠。如果体系处于
所请求方法不可靠的范围之外，应考虑改用其他方法。

如果一切看起来都合理，但似乎仍有问题，请将该案例发布到
[ORCA 论坛](https://orcaforum.kofo.mpg.de/) 上。可能是存在某种技术原因导致数值如此，
也可能是有一个应当修复的缺陷（bug）。
