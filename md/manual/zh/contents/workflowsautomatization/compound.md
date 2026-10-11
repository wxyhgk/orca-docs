```{index} Compound
```

(sec:workflowsautomatization.compound)=
# Compound

Compound 是一种复杂的脚本语言形式，可以直接在 ORCA 的输入中使用。使用 '*Compound*'，用户可以组合常规 ORCA 计算的各个部分，以求值自己定义的自定义函数。为了说明其用法，我们将使用一个示例。有关该模块的更详细描述，请参阅章节
{ref}`sec:workflowsautomatization.compound_detailed`。

(sec:workflowsautomatization.compound.umbrella_example)=
## 示例（example）

作为典型示例，我们将使用描述 $NH_3$ “伞效应（umbrella effect）”的约束优化。该脚本将执行一系列计算，最后打印该运动的势能并识别极小点和极大点。相应的 compound 脚本如下所示。

```{literalinclude} ../../orca_working_input/compTypicalExampleUmbrella.cmp
:language: orca
```

让我们从如何执行这个输入开始。要运行它，最简单的方式是把它保存在一个普通文本文件中，命名为
\"umbrella.cmp\"，然后使用下列 ORCA 输入文件：

```orca
%Compound "umbrella.cmp"
```

不需要更多内容。ORCA 将读取 compound 文件并相应地执行。

关于这个 ORCA 输入有几点说明。首先，没有简单输入行
（以 *\"!\"* 开头）。使用 *Compound* 特性时不需要简单输入，但如果用户添加了简单输入，简单输入中的所有信息都将传递给实际的 compound 作业。

此外，如果不想创建单独的 compound 文本文件，在 ORCA 中完全可以像使用任何其他 ORCA 块一样使用 compound 特性。这意味着在 *%Compound* 指令之后，可以不给出文件名，而是附加 Compound 文件的内容。

正如我们将看到的，在 compound 脚本文件内部，每个 compound 作业都可以包含常规 ORCA 输入文件的全部信息。这里有两个非常重要的例外：处理器数目和 *MaxCore*。这些信息应在初始 ORCA 输入文件中设置，而不是在实际的 compound 文件中。

Compound 块具有与所有 ORCA 块相同的结构。它以 *\"%\"* 开始，如果输入不是从文件读取的，则以 *\"End\"* 结束。如果 compound 指令在文件中（如上例所示），则只需方括号中的文件名，不需要最后的 *END*。

(sec:workflowsautomatization.compound.umbrella_defining_variables)=
## 定义变量（Defining variables）

如我们已经指出的，可以在 Compound 块内给出计算和数据处理的全部信息，也可以创建一个包含所有细节的普通文本文件让 ORCA 读取。后一个选项的优点是可以将同一个文件用于多个几何结构。在前面的例子中，我们让 ORCA 引用一个外部文件，即包含所有必要信息的文件 *\"umbrella.cmp\"*。

现在让我们尝试分析 Compound 文件 *\"umbrella.cmp\"*。

```orca
# ----------------------------------------------
# Umbrella coordinate mapping for NH3
# Author: Frank Neese
# ----------------------------------------------
variable JobName = "NH3-umbrella";
variable amin    = 50.0;
variable amax    = 130.0;
variable nsteps  = 21;
Variable energies[21];

Variable angle;
Variable JobStep;
Variable JobStep_m;
variable step;

Variable method = "BP86";
Variable basis  = "def2-SVP def2/J";

step  = 1.0*(amax-amin)/(nsteps-1);
```

第一部分包含一些一般性注释和变量定义。注释使用与常规 ORCA 输入相同的语法，即 *\"#\"* 符号。请注意，同一行中出现多个 *\"#\"* 符号会导致错误。

初始注释之后是一些声明和定义。声明变量有许多不同方式，在章节
{ref}`sec:workflowsautomatization.compound_detailed.commands.variables.general` 中有详细描述。

所有变量声明都以指令 *Variable* 开始，这是向程序发出的信号，表示期望声明一个或多个新变量。然后有许多选项，包括定义多个变量、同时为变量赋值或使用值列表。不过，所有声明**必须**以 *;* 符号结束。该符号向程序表明这是当前命令的结束。在 *Compound* 中每条命令末尾都需要 *;* 符号，这是普遍要求，只有极少数例外。

(sec:workflowsautomatization.compound.umbrella_running)=
## 运行计算（Running calculations）

```orca
# Loop over the number of steps
# ----------------------------
for iang from 0 to nsteps-1 do
  angle    = amin + iang*step;
  JobStep  = iang+1;
  JobStep_m= JobStep-1;
  if (iang>0) then
    Read_Geom(JobStep_m);
    New_step
      ! &{method} &{basis} TightSCF Opt
      %base "&{JobName}.step&{JobStep}"
      %geom
        constraints
          {A 1 0 2 &{angle} C}
          {A 1 0 3 &{angle} C}
          {A 1 0 4 &{angle} C}
        end
      end
    Step_End
  else
    New_step
      ! &{method} &{basis} TightSCF Opt
      %base "&{JobName}.step&{JobStep}"  
      %geom
        constraints
          {A 1 0 2 &{angle} C}
          {A 1 0 3 &{angle} C}
          {A 1 0 4 &{angle} C}
        end
      end
      * int 0 1
        N 0 0 0 0.0 0.0 0.0
        DA 1 0 0 2.0 0.0 0.0
        H 1 2 0 1.06 &{angle} 0.0
        H 1 2 3 1.06 &{angle} 120.0
        H 1 2 3 1.06 &{angle} 240.0
      *
    Step_End
  endif
  Read energies[iang] = SCF_ENERGY[jobStep];
  print(" index: %3d Angle %6.2lf Energy: %16.12lf Eh\textbackslash{}n", iang, angle, energies[iang]);
EndFor
```

然后是信息最密集的部分。我们从定义一个 *for* 循环开始。Compound 中 *for* 循环的语法是：

**For** *variable* **From** *startValue* **To** *endValue* **Do**\
&nbsp; *directives*\
**EndFor**

如上例所示，*startValue* 和 *endValue* 可以是常数或先前定义的变量，甚至是这些变量的函数。请记住它们必须是整数。循环到达末尾的标志是 *EndFor* 指令。关于 *for* 循环的更多细节，请参阅章节
{ref}`sec:workflowsautomatization.compound_detailed.commands.for`。

然后我们继续为一些变量赋值。


```orca
angle     = amin + iang*step;
JobStep   = iang+1;
JobStep_m = JobStep-1;
```

变量赋值的语法与每种编程语言一样：变量后跟 *=* 符号，然后是值或一个表达式。请记住，赋值**必须**总是以 *;* 符号结束。

下一步是每种编程语言的另一个重要部分，即 *if* 块。*if* 块的语法如下：

**if** (*expression to evaluate* **) Then**\
&nbsp; *directives*\
**else if (** *expression to evaluate* **) Then**\
&nbsp; *directives*\
**else**\
&nbsp; *directives*\
**EndIf**

该块的 *else if* 和 *else* 部分是可选的，但最后的 *EndIf* 必须始终标志 *if* 块的结束。关于 *if* 块用法的更多细节，请参阅手册的章节
{ref}`sec:workflowsautomatization.compound_detailed.commands.if`。

接下来是一个 compound 特有、而非普通编程语言一部分的命令。这就是 *ReadGeom* 命令。其语法是：

**Read_Geom**(*integer value*);

在解释这个命令之前，我们先继续看 compound 脚本中的下一个命令，稍后再回到它。

下一个命令是所有 compound 脚本的基础。这就是 *New_Step* 命令。该命令向 compound 表明随后是一个常规 ORCA 计算。其语法是：

**New_Command**
&nbsp; *Normal ORCA input*
**Step_End**

关于 *New_Step* 命令的一些说明。首先，在 *New_Step* - *Step_End* 命令内部可以添加常规 ORCA 输入所接受的所有命令。这里要记住，定义处理器数目的命令和 *MaxCore* 命令将被忽略。

第二点要记住的是 *step* 的概念。每个 *New_Step - Step_End* 结构对应一个 step，从 1（第一次 ORCA 计算）开始计数。这有助于定义该计算将创建的性质文件，以便我们用它从中检索信息。

*New_Step - Step_End* 块的一个重要特性是使用 **&{***variable***}** 结构。该结构允许用户在 *New_Step - Step_End* 块内部使用定义在块外的变量，使 ORCA 输入更加通用。例如，在上面给出的脚本中，我们用已定义的变量 *JobName* 和 *JobStep* 构建计算的 *basename*：

```orca
  %base "&{JobName}.step&{JobStep}"
```

关于 **&{}** 结构用法的更多细节，请参阅章节
{ref}`sec:workflowsautomatization.compound_detailed.commands.ampersand`；
关于 *New_Step - Step_End* 结构，请参阅章节
{ref}`sec:workflowsautomatization.compound_detailed.commands.newstep`。

最后，关于计算的几何结构有几点说明。向 *New_Step - Step_End* 计算提供几何结构有 3 种方式。第一种是传统的 ORCA 输入方式，我们可以给出坐标或含坐标的文件名，就像在所有 ORCA 输入中所做的那样。但在 *Compound* 中，如果我们不传递任何关于计算几何结构的信息，*Compound* 将自动尝试读取上一次计算的几何结构。这是向 compound Step 提供几何结构的第二种（隐式）方式。还有第三种方式，也就是我们在上例中使用的，即 **Read_Geom** 命令。该命令的语法是：\
**Read_Geom** (*Step number*);\
当我们想把一个特定的几何结构传递给某个计算、而该几何结构既没有在 *New_Step -
Step_End* 结构内显式给出，也不是上一步的几何结构时，就可以使用该命令。然后只需在运行新计算之前传递我们感兴趣的那一步计算的编号。关于 *Read_Geom* 命令的更多细节，请参阅章节
{ref}`sec:workflowsautomatization.compound_detailed.commands.read_geom`。

(sec:workflowsautomatization.compound.umbrella_data_manipulation)=
## 数据处理（Data manipulation）

*Compound* 最强大的特性之一是直接访问计算的性质。为了使用这些性质，我们定义了 *Read* 命令。在前面的例子中，我们用它读取计算的 SCF 能量：

```orca
Read energies[iang] = SCF\_ENERGY[jobStep];
```

该命令的语法是：

**Read** *variable name* **=** *property* 

其中 *variable name* 是已定义变量的名称，*property* 是表 {ref}`sec:workflowsautomatization.compound_detailed.knownProperties` 中已知性质里的性质，*step* 是我们感兴趣的计算步骤。关于 *Read* 命令的更多细节，请参阅相应章节。


```orca
# Print a summary at the end of the calculation
  # ---------------------------------------------
  print("////////////////////////////////////////////////////////\\n");
  print("// POTENTIAL ENERGY RESULT\\n");
  print("////////////////////////////////////////////////////////\\n");
  variable minimum,maximum;
  variable Em,E0,Ep;
  variable i0,im,ip;
  for iang from 0 to nsteps-1 do
    angle   = amin + 1.0*iang*step;
    JobStep = iang+1;
    minimum = 0;
    maximum = 0;
    i0      = iang;
    im      = iang-1;
    ip      = iang+1;
    E0      = energies[i0];
    Em      = E0;
    Ep      = E0;
    if (iang>0 and iang<nsteps-1) then
      Em = energies[im];
      Ep = energies[ip];
    endif
    if (E0<Em and E0<Ep) then minimum=1; endif
    if (E0>Em and E0>Ep) then maximum=1; endif
    if (minimum = 1 ) then
      print(" %3d  %6.2lf %16.12lf (-)\textbackslash{}n",JobStep,angle, E0 );
    endif
    if (maximum = 1 ) then
      print(" %3d  %6.2lf %16.12lf (+)\textbackslash{}n",JobStep,angle, E0 );
    endif
    if (minimum=0 and maximum=0) then
      print(" %3d  %6.2lf %16.12lf    \textbackslash{}n",JobStep,angle, E0 );
    endif
  endfor
  print("////////////////////////////////////////////////////////\\n");
```

一旦所有数据都可用，我们就可以像在任何编程语言中一样在表达式中使用它们。

print 语句的语法是：

**print(** *format string, \[variables\]***);**

例如在前面的脚本中我们这样使用它：

```orca
print(" %3d  %6.2lf %16.12lf  \n",JobStep,angle, E0 );
```

其中 *%3d、%6.2lf* 和 *%16.2lf* 是格式标识符，*JobStep、angle* 和 *E0* 是先前定义的变量。该语法紧密遵循编程语言 C 中广泛接受的 *printf* 命令语法。关于 *print* 语句的更多细节，请参阅章节：
{ref}`sec:workflowsautomatization.compound_detailed.commands.stringrelated.print`。

与 *print* 命令类似的是 *write2file* 和 *write2string* 命令，它们用于写到输出文件之外的地方——写到我们选择的文件，或生成一个新字符串。

最后，非常重要的是不要忘记每个 compound 文件都应以最终的 **End** 结束。

运行上面的例子后，我们得到如下输出：

```orca
////////////////////////////////////////////////////////
// POTENTIAL ENERGY RESULT
////////////////////////////////////////////////////////
1   50.00 -56.486626696200    
2   54.00 -56.498074637200    
3   58.00 -56.505200120800    
4   62.00 -56.508823168800    
5   66.00 -56.509732863600 (-)
6   70.00 -56.508724734300    
7   74.00 -56.506590613800    
8   78.00 -56.504070086000    
9   82.00 -56.501791816800    
10   86.00 -56.500229017900    
11   90.00 -56.499674856600 (+)
12   94.00 -56.500229018100    
13   98.00 -56.501791817200    
14  102.00 -56.504070082800    
15  106.00 -56.506590613300    
16  110.00 -56.508724733100    
17  114.00 -56.509732863700 (-)
18  118.00 -56.508823172900    
19  122.00 -56.505200132200    
20  126.00 -56.498074642900    
21  130.00 -56.486626729200    
////////////////////////////////////////////////////////
```

其中包含 step 编号、相应 step 的角度、约束优化后的能量，以及势能中两个极小点和一个极大点的符号。
