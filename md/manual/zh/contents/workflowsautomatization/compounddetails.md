(sec:workflowsautomatization.compound_detailed)=
# Compound 的更多细节（More Details on Compound）
本部分我们更详细地描述 "Compound"。
## 命令（Commands）

下面是 *Compound* 中所有可用命令的列表

**--------------------------------- 数据集相关 --------------------------------**

-   Dataset({ref}`sec:workflowsautomatization.compound_detailed.commands.dataset.declaration`)

-   MakeReferenceFromDir({ref}`sec:workflowsautomatization.compound_detailed.commands.dataset.makeReferenceFromDir`)
    
-   Print({ref}`sec:workflowsautomatization.compound_detailed.commands.dataset.print`)

**------------------------------ 文件处理相关 -----------------------------**
-   CloseFile
    ({ref}`sec:workflowsautomatization.compound_detailed.commands.closeFile`)

-   OpenFile
    ({ref}`sec:workflowsautomatization.compound_detailed.commands.openFile`)

**------------------------------- *For* 循环相关 -------------------------------**
-   Break
    ({ref}`sec:workflowsautomatization.compound_detailed.commands.break`)

-   Continue
    ({ref}`sec:workflowsautomatization.compound_detailed.commands.continue`)

-   EndFor
    ({ref}`sec:workflowsautomatization.compound_detailed.commands.endfor`)

-   For
    ({ref}`sec:workflowsautomatization.compound_detailed.commands.for`)


**-------------------------------- 几何结构相关 -------------------------------**

-   Geometry({ref}`sec:workflowsautomatization.compound_detailed.commands.geometry`)

-   BohrToAngs({ref}`sec:workflowsautomatization.compound_detailed.commands.geometry.BohrToAngs`)
   
-   CreateBSSE({ref}`sec:workflowsautomatization.compound_detailed.commands.geometry.createBSSE`)

-   CreateFragments({ref}`sec:workflowsautomatization.compound_detailed.commands.geometry.createFragments`)
  
-   DisplaceAtom({ref}`sec:workflowsautomatization.compound_detailed.commands.geometry.displaceAtom`)
  
-   FollowNormalMode({ref}`sec:workflowsautomatization.compound_detailed.commands.geometry.followNormalMode`)
     
-   GetAngle({ref}`sec:workflowsautomatization.compound_detailed.commands.geometry.getAngle`)
   
-   GetAtomicNumbers({ref}`sec:workflowsautomatization.compound_detailed.commands.geometry.getAtomicNumbers`)

-   GetBondDistance({ref}`sec:workflowsautomatization.compound_detailed.commands.geometry.getBondDistance`)
  
-   GetCartesians({ref}`sec:workflowsautomatization.compound_detailed.commands.geometry.getCartesians`)

-   GetGhostAtoms({ref}`sec:workflowsautomatization.compound_detailed.commands.geometry.getGhostAtoms`)   
   
-   GetNumOfAtoms({ref}`sec:workflowsautomatization.compound_detailed.commands.geometry.getNumOfAtoms`)

-   MoveAtomToCenter({ref}`sec:workflowsautomatization.compound_detailed.commands.geometry.moveAtomToCenter`)   
   
-   Read({ref}`sec:workflowsautomatization.compound_detailed.commands.geometry.read`)

-   RemoveAtoms({ref}`sec:workflowsautomatization.compound_detailed.commands.geometry.removeAtoms`)
   
-   RemoveElements({ref}`sec:workflowsautomatization.compound_detailed.commands.geometry.removeElements`)
      
-   WriteXYZFile({ref}`sec:workflowsautomatization.compound_detailed.commands.geometry.writeXYZFile`)

**--------------------------------   GOAT 相关  -------------------------------**

-   GOAT({ref}`sec:workflowsautomatization.compound_detailed.commands.goat`)

-   Get_Energy ({ref}`sec:workflowsautomatization.compound_detailed.commands.goat.getEnergy`)
  
-   Get_Num_Of_Geometries ({ref}`sec:workflowsautomatization.compound_detailed.commands.goat.getNumOfGeometries`)
  
-   ParseEensembleFfile ({ref}`sec:workflowsautomatization.compound_detailed.commands.goat.parseEnsembleFile`)
    
-   Set_Basename ({ref}`sec:workflowsautomatization.compound_detailed.commands.goat.setBasename`)

-   Print ({ref}`sec:workflowsautomatization.compound_detailed.commands.goat.print`)
  
-   WriteXYZFile ({ref}`sec:workflowsautomatization.compound_detailed.commands.goat.writeXYZFile`)  

**------------------------------ *If* 块相关 ------------------------------**

-   If
    ({ref}`sec:workflowsautomatization.compound_detailed.commands.if`)

**---------------------------- 线性代数相关 ----------------------------**

-   Diagonalize({ref}`sec:workflowsautomatization.compound_detailed.commands.linAlgegra.diagonalize`)

-   InvertMatrix({ref}`sec:workflowsautomatization.compound_detailed.commands.linAlgegra.invertMatrix`)  
 
-   Mat_p_Mat({ref}`sec:workflowsautomatization.compound_detailed.commands.linAlgegra.Mat_p_Mat`)     
   
-   Mat_x_Mat({ref}`sec:workflowsautomatization.compound_detailed.commands.linAlgegra.Mat_x_Mat`)  

-   Mat_x_Scal({ref}`sec:workflowsautomatization.compound_detailed.commands.linAlgegra.Mat_x_Scal`) 

**--------------------------- ORCA 计算相关 ---------------------------**

-   Basenames({ref}`sec:workflowsautomatization.compound_detailed.commands.orca.basenames`)

-   ReadMOs({ref}`sec:workflowsautomatization.compound_detailed.commands.orca.readMOs`) 

**----------------------------- 程序流程相关 -----------------------------**

-   Abort
    ({ref}`sec:workflowsautomatization.compound_detailed.commands.abort`)

-   End
    ({ref}`sec:workflowsautomatization.compound_detailed.commands.end`)

-   EndRun
    ({ref}`sec:workflowsautomatization.compound_detailed.commands.endrun`)

-   GoTo
    ({ref}`sec:workflowsautomatization.compound_detailed.commands.goto`)

**--------------------------- 性质文件相关 ----------------------------**

-   GetNumOfInstances({ref}`sec:workflowsautomatization.compound_detailed.commands.propertyFile.getNumOfInstances`) 
   
-   ReadProperty({ref}`sec:workflowsautomatization.compound_detailed.commands.propertyFile.readProperty`) 

**-------------------------- 字符串处理相关 --------------------------**

-   GetBasename ({ref}`sec:workflowsautomatization.compound_detailed.commands.stringrelated.getBasename`)

-   GetChar ({ref}`sec:workflowsautomatization.compound_detailed.commands.stringrelated.getChar`)
  
-   GetSuffix ({ref}`sec:workflowsautomatization.compound_detailed.commands.stringrelated.getSuffix`)
  
-   Print ({ref}`sec:workflowsautomatization.compound_detailed.commands.stringrelated.print`)
   
-   Write2File ({ref}`sec:workflowsautomatization.compound_detailed.commands.stringrelated.write2file`)
   
-   Write2String ({ref}`sec:workflowsautomatization.compound_detailed.commands.stringrelated.write2string`)

**--------------------------------- Step 相关 ---------------------------------**

-   &
    ({ref}`sec:workflowsautomatization.compound_detailed.commands.ampersand`)

-   Alias
    ({ref}`sec:workflowsautomatization.compound_detailed.commands.alias`)

**----------------------------- 计时器相关 ------------------------------------**

- Timer ({ref}`sec:workflowsautomatization.compound_detailed.commands.timerrelated.timer`)

- Last ({ref}`sec:workflowsautomatization.compound_detailedd.commands.timer.last`)

- Reset ({ref}`sec:workflowsautomatization.compound_detailedd.commands.timer.reset`)

- Start ({ref}`sec:workflowsautomatization.compound_detailedd.commands.timer.start`)

- Stop ({ref}`sec:workflowsautomatization.compound_detailedd.commands.timer.stop`)

- Total ({ref}`sec:workflowsautomatization.compound_detailedd.commands.timer.total`)

**--------------------------- 变量相关 ----------------------------------**

-  Variables ({ref}`sec:workflowsautomatization.compound_detailed.commands.variables.general`)

-  Variables - Assignment ({ref}`sec:workflowsautomatization.compound_detailed.commands.variables.assignement`)

-  Variables - Declaration ({ref}`sec:workflowsautomatization.compound_detailed.commands.variables.declaration`)

-  Variables - Functions ({ref}`sec:workflowsautomatization.compound_detailed.commands.variables.functions`)

-  Variable - With ({ref}`sec:workflowsautomatization.compound_detailed.commands.variables.with`)

-  GetBool() {ref}`sec:workflowsautomatization.compound_detailed.commands.variables.functions.getBool` 

-  GetDim1() {ref}`sec:workflowsautomatization.compound_detailed.commands.variables.functions.getDim1` 

-  GetDim2() {ref}`sec:workflowsautomatization.compound_detailed.commands.variables.functions.getDim2` 

-  GetDouble() {ref}`sec:workflowsautomatization.compound_detailed.commands.variables.functions.getDouble` 

-  GetInteger() {ref}`sec:workflowsautomatization.compound_detailed.commands.variables.functions.getInteger` 

-  GetSize() {ref}`sec:workflowsautomatization.compound_detailed.commands.variables.functions.getSize` 

-  GetString() {ref}`sec:workflowsautomatization.compound_detailed.commands.variables.functions.getString` 

-  PrintMatrix() {ref}`sec:workflowsautomatization.compound_detailed.commands.variables.functions.printMatrix` 

-  Write2File ({ref}`sec:workflowsautomatization.compound_detailed.commands.stringrelated.write2file`)

-  Write2String ({ref}`sec:workflowsautomatization.compound_detailed.commands.stringrelated.write2string`)


(sec:workflowsautomatization.compound_detailed.commands.ampersand)=
### &

*&* 符号在 compound 块中具有特殊含义。在 *NewStep* - *StepEnd* 块内部使用该符号，用户可以使用定义在块外的变量。字符串变量和数值变量都允许。

**语法（Syntax）：**

**&{*variable*}**

**示例**

```{literalinclude} ../../orca_working_input/ORCA_Test_0958.inp
:language: orca
```

(sec:workflowsautomatization.compound_detailed.commands.abort)=
### Abort
当用户想要立即退出程序时使用 *Abort*。
**语法（Syntax）：**\
Abort;\
**或者：**\
Abort

**示例：**
```{literalinclude} ../../orca_working_input/compound_example_abort.inp
:language: orca
```

(sec:workflowsautomatization.compound_detailed.commands.alias)=
### Alias

*Alias* 用于将一个整数替换为更有代表性的字符串。当执行多次计算而步骤编号变得过于复杂难以求值时很有用。这种情况下在 Step_End 命令之后使用 Alias_Step 将把前面的计算步骤编号与所提供的名称关联起来。

**语法（Syntax）：**\
Alias $name$;\
**或者：**\
Alias $name$\
**示例：**

```{literalinclude} ../../orca_working_input/0960.cmp
:language: orca
```
:::{admonition} 注意
:class: note
对于 **Alias** 命令，最后的 ';' 是可选的。
:::

(sec:workflowsautomatization.compound_detailed.commands.orca.basenames)=
### Basenames
*Basenames* 是每次使用 *NewStep* 时在 *Compound* 中自动创建的变量，它保存该步骤的名称。可以在计算运行过程中用它恢复该名称。它实际上是一个向量，其中值零对应于任何 *new_step* 命令之前的主计算。

**示例：**
```{literalinclude} ../../orca_working_input/compound_example_basenames.inp
:language: orca
```

(sec:workflowsautomatization.compound_detailed.commands.break)=
### Break
当需要在一定条件下中断循环时，可以在 *For* 循环内部使用 *Break*（见（见 {ref}`sec:workflowsautomatization.compound_detailed.commands.for`））。语法如下：


**语法（Syntax）：**\
*For* *variable* *From* *Start value* *To* *End value* *Do*\
*commands*\
**break ;**\
*commands*\
*EndFor;*

**注意** *break* 和 *break;* 两种形式都是合法的。

break 实际所做的是将循环的运行索引设为最后一个允许的值，然后跳转到 *EndFor*（见 {ref}`sec:workflowsautomatization.compound_detailed.commands.endfor`））。

**示例：**
```{literalinclude} ../../orca_working_input/ORCA_Test_1796.inp
:language: orca
```

(sec:workflowsautomatization.compound_detailed.commands.closeFile)=
### CloseFile

当在 *Compound* 中使用 *openFile* 命令（见 {ref}`sec:workflowsautomatization.compound_detailed.commands.openFile`）打开文件后，必须用 *closeFile* 命令关闭它。

**语法（Syntax）：**\
*closeFile*(file);

*file* 是由 *openFile* 命令创建的文件指针。示例见段落 {ref}`sec:workflowsautomatization.compound_detailed.commands.openFile`。

(sec:workflowsautomatization.compound_detailed.commands.continue)=
### Continue
当需要跳过循环的当前步骤并继续下一步时，可以在 *For* 循环内部使用 *Continue*（见（见 {ref}`sec:workflowsautomatization.compound_detailed.commands.for`））。语法如下：


**语法（Syntax）：**\
*For* *variable* *From* *Start value* *To* *End value* *Do*\
*commands*\
**continue ;**\
*commands*\
*EndFor;*

**注意** *continue* 和 *continue;* 两种形式都是合法的。

continue 实际所做的是跳转到 *EndFor*（见 {ref}`sec:workflowsautomatization.compound_detailed.commands.endfor`））。

**示例：**
```{literalinclude} ../../orca_working_input/ORCA_Test_1797.inp
:language: orca
```

(sec:workflowsautomatization.compound_detailed.commands.dataset.declaration)=
### Dataset

在 *Compound* 中我们有 *Dataset* 对象。这些对象可以像 '*compDataset*' 类型的普通变量一样处理。普通变量与 *Dataset* 变量的一个重要区别在于声明方式。不是普通的：
```orca
Variable x;
```
我们必须显式声明这是一个数据集。因此数据集声明的语法是：

**语法（Syntax）：**
```orca
Dataset mySet;
```

**注意** 对于数据集，我们不允许每行声明多个数据集。


下面是在 *Dataset* 上工作的函数列表。

-   MakeReferenceFromDir({ref}`sec:workflowsautomatization.compound_detailed.commands.dataset.makeReferenceFromDir`)
   
-   Print({ref}`sec:workflowsautomatization.compound_detailed.commands.dataset.print`)


**示例：**
```{literalinclude} ../../orca_working_input/compound_example_dataset_declaration.inp
:language: orca
```

(sec:workflowsautomatization.compound_detailed.commands.dataset.makeReferenceFromDir)=
### D.MakeReferenceFromDir

*MakeReferenceFromDir* 命令作用于数据集对象（见 {ref}`sec:workflowsautomatization.compound_detailed.commands.dataset.declaration`）。它基于当前文件夹的 *xyz 文件创建一个 json 参考文件。
**注意** 默认情况下所有电荷和多重度分别设为 0 和 1。

**语法（Syntax）：**\
*mySet.MakeReferenceFromDir(dirName);*

其中：

- *mySet* 是已声明的数据集对象

- *dirName* 应包含一些 xyz 文件的目录名称。


**示例：**
```{literalinclude} ../../orca_working_input/compound_example_dataset_makeReferenceFromDir.inp
:language: orca
```


(sec:workflowsautomatization.compound_detailed.commands.dataset.print)=
### D.Print

*Print* 命令作用于数据集对象（见 {ref}`sec:workflowsautomatization.compound_detailed.commands.dataset.declaration`）。它打印该数据集对象的所有细节。

**语法（Syntax）：**\
*mySet.Print();*

其中：

- *mySet* 是已声明的数据集对象


**示例：**
```{literalinclude} ../../orca_working_input/compound_example_dataset_declaration.inp
:language: orca
```

(sec:workflowsautomatization.compound_detailed.commands.linAlgegra.diagonalize)=
### Diagonalize
*Compound* 可以执行矩阵代数运算，可用的代数运算之一是矩阵对角化。请注意，待对角化的矩阵**必须是**方阵且对称。还要记住只有矩阵的上三角部分用于对角化。如果一切顺利，该函数将返回矩阵的本征向量和本征值。

**语法（Syntax）：**\
*A.Diagonalize(eigenValues, eigenVectors);*

其中：

- *A：* 待对角化的矩阵。
- *eigenValues：* 含本征值的向量
- *eigenVectors：* 含初始矩阵本征向量的方阵。

**示例：**
```{literalinclude} ../../orca_working_input/compound_example_linAlgebra_diagonalize.inp
:language: orca
```

(sec:workflowsautomatization.compound_detailed.commands.end)=
### End
*End* 是每个 compound 脚本必须有的最终命令（除非有 *EndRun* 命令（见 {ref}`sec:workflowsautomatization.compound_detailed.commands.endrun`））。*Compound* 执行完脚本中所写内容后，控制权再次交回常规 ORCA 输入读取。ORCA 将继续分析 *Compound* 部分之后剩余的输入，但不会运行任何计算。

(sec:workflowsautomatization.compound_detailed.commands.endrun)=
### EndRun
*EndRun* 是结束 *Compound* 脚本执行的 *End* 命令的替代命令（见 {ref}`sec:workflowsautomatization.compound_detailed.commands.endrun`）。*end* 与 *EndRun* 的区别在于 *EndRun* 忽略 *Compound* 块之后的一切。这使得将 *Compound* 用作完整工作流运行更加容易。

(sec:workflowsautomatization.compound_detailed.commands.endfor)=
### EndFor

所有 *For* 循环（见 {ref}`sec:workflowsautomatization.compound_detailed.commands.for`）都必须以 *EndFor* 结束。语法和示例见 *For* 章节（见 {ref}`sec:workflowsautomatization.compound_detailed.commands.for`）。

**注意** 对于 *EndFor*，*EndFor* 和 *EndFor;* 都可以。

(sec:workflowsautomatization.compound_detailed.commands.for)=
### For

*For* 循环用于执行重复性任务。语法如下：

**语法（Syntax）：**

**For** *variable* **From** *Start value* **To** *End value* **Do**

*commands*

**EndFor** 或 **EndFor;**

*Variable* 应是先前未定义的变量名。
*Start value* 和 *End value* 应是定义 *variable* 起始值和结束值的整数。*Start value* 和 *End value* 可以是数字、预定义变量或先前定义变量的函数。唯一要求是它们必须是**整数**。请记住循环将从第一个值执行到 *End value*，包含 *End value*。

**示例：**

```{literalinclude} ../../orca_working_input/0977.cmp
:language: orca
```


(sec:workflowsautomatization.compound_detailed.commands.geometry)=
### Geometry

在 *Compound* 中我们有 *Geometry* 对象。这些对象可以像 '*compGeometry*' 类型的普通变量一样处理。普通变量与 *Geometry* 变量的一个重要区别在于声明方式。不是普通的：
```
Variable myGeom;
```
我们必须显式声明这是一个几何结构。因此几何结构声明的语法是：

**语法（Syntax）：**
```
Geometry myGeom;

Geometry myGeom1, myGeom2;
```

使用第二种定义可以在同一行定义两个几何结构对象。

下面是在 *Geometry* 对象上工作的函数列表。

-   BohrToAngs({ref}`sec:workflowsautomatization.compound_detailed.commands.geometry.BohrToAngs`)
-   CreateBSSE ({ref}`sec:workflowsautomatization.compound_detailed.commands.geometry.createBSSE`)
-   CreateFragments({ref}`sec:workflowsautomatization.compound_detailed.commands.geometry.createFragments`)
-   DisplaceAtom({ref}`sec:workflowsautomatization.compound_detailed.commands.geometry.displaceAtom`)
-   FollowNormalMode ({ref}`sec:workflowsautomatization.compound_detailed.commands.geometry.followNormalMode`)
-   GetAngle({ref}`sec:workflowsautomatization.compound_detailed.commands.geometry.getAngle`)
-   GetAtomicNumbers({ref}`sec:workflowsautomatization.compound_detailed.commands.geometry.getAtomicNumbers`)
-   GetBondDistance({ref}`sec:workflowsautomatization.compound_detailed.commands.geometry.getBondDistance`)
-   GetCartesians({ref}`sec:workflowsautomatization.compound_detailed.commands.geometry.getCartesians`)
-   GetGhostAtoms({ref}`sec:workflowsautomatization.compound_detailed.commands.geometry.getGhostAtoms`)   
-   GetNumOfAtoms({ref}`sec:workflowsautomatization.compound_detailed.commands.geometry.getNumOfAtoms`)
-   MoveAtomToCenter({ref}`sec:workflowsautomatization.compound_detailed.commands.geometry.moveAtomToCenter`)
-   Read({ref}`sec:workflowsautomatization.compound_detailed.commands.geometry.read`)
-   RemoveAtoms({ref}`sec:workflowsautomatization.compound_detailed.commands.geometry.removeAtoms`)
-   RemoveElements({ref}`sec:workflowsautomatization.compound_detailed.commands.geometry.removeElements`)
-   WriteXYZFile({ref}`sec:workflowsautomatization.compound_detailed.commands.geometry.writeXYZFile`)
   
(sec:workflowsautomatization.compound_detailed.commands.geometry.BohrToAngs)=
### G.BohrToAngs
*BohrToAngs* 命令作用于几何结构对象（见见 {ref}`sec:workflowsautomatization.compound_detailed.commands.geometry`）。它将加载的几何结构对象的几何结构从 Bohr 转换为 Angstrom。实际上它只是将坐标乘以因子 *0.529177249*。

**语法（Syntax）：**\
*myGeom.BohrToAngs();*

其中：

- *myGeom* 是已包含几何结构的几何结构对象


**示例：**
```{literalinclude} ../../orca_working_input/compound_example_geometry_BohrToAngs.inp
:language: orca
```


(sec:workflowsautomatization.compound_detailed.commands.geometry.createBSSE)=
### G.CreateBSSE

*CreateBSSE* 命令作用于几何结构对象（见见 {ref}`sec:workflowsautomatization.compound_detailed.commands.geometry`）。如果几何结构对象包含 *ghost* 原子，则 *CreateBSSE* 将创建五个新文件：
- myFilename_FragmentA.xyz
- myFilename_MonomerA.xyz
- myFilename_FragmentB.xyz
- myFilename_MonomerB.xyz
- myFilename_Total.xyz

**语法（Syntax）：**\
*myGeom.CreateBSSE(filename=myFilename);*

其中：

- *myGeom* 是已包含几何结构的几何结构对象

- *filename* 是所创建文件的基文件名。

**示例：**
```{literalinclude} ../../orca_working_input/compound_example_geometry_createbsse.inp
:language: orca
```

**注意** 这些文件将包含以 **BOHRS** 为单位的 XYZ 几何结构。

(sec:workflowsautomatization.compound_detailed.commands.geometry.createFragments)=
### G.CreateFragments

*CreateBSSE* 命令作用于几何结构对象（见见 {ref}`sec:workflowsautomatization.compound_detailed.commands.geometry`）。如果几何结构对象包含 *ghost* 原子，则 *CreateBSSE* 将创建五个新文件：
- myFilename_FragmentA.xyz
- myFilename_MonomerA.xyz
- myFilename_FragmentB.xyz
- myFilename_MonomerB.xyz
- myFilename_Total.xyz

**语法（Syntax）：**\
*myGeom.CreateBSSE(filename=myFilename);*

其中：

- *myGeom* 是已包含几何结构的几何结构对象

- *filename* 是所创建文件的基文件名。

**示例：**
```{literalinclude} ../../orca_working_input/compound_example_geometry_createbsse.inp
:language: orca
```

**注意** 这些文件将包含以 **BOHRS** 为单位的 XYZ 几何结构。

(sec:workflowsautomatization.compound_detailed.commands.geometry.followNormalMode)=
### G.FollowNormalMode

*FollowNormalMode* 命令作用于几何结构对象（见见 {ref}`sec:workflowsautomatization.compound_detailed.commands.geometry`）。它将按所选振动简正模式位移加载的几何结构

**语法（Syntax）：**\
*myGeom.FollowNormalMode(vibrationSN=myVibration, [ScalingFactor=myScalingFactor]);*

其中：

- *myGeom* 是已包含几何结构的几何结构对象

- *vibrationSN* 是振动的序号。
**注意** 请记住计数从 1 开始。

- *scalingFactor* 是简正振动模式的缩放因子。该参数可选。

**示例：**
```{literalinclude} ../../orca_working_input/compound_example_geometry_followNormalMode.inp
:language: orca
```

(sec:workflowsautomatization.compound_detailed.commands.geometry.displaceAtom)=
### G.DisplaceAtom
函数 *DisplaceAtom* 作用于几何结构对象，移动当前几何结构中给定原子的笛卡尔坐标。位移以 Bohr 为单位。

**语法（Syntax）：**

*res = geom.DisplaceAtom(atomID, dx, dy, dz)*

其中：

*geom* 先前加载的几何结构对象。

*atomID* 我们要移动的原子索引。请注意计数从零开始。

*dx* x 轴上的位移，以 Bohr 为单位。

*dy* y 轴上的位移，以 Bohr 为单位。

*dz* z 轴上的位移，以 Bohr 为单位。

**示例：**

```{literalinclude} ../../orca_working_input/compound_example_geometry_displaceAtom.inp
:language: orca
```

(sec:workflowsautomatization.compound_detailed.commands.geometry.getAngle)=
### G.GetAngle
函数 *GetAngle* 作用于几何结构对象，返回三个原子之间的夹角，单位为**度（Degrees）**。

**语法（Syntax）：**

*res = geom.GetAngle(atomA, atomB, atomC)*

其中：

*res* 原子 atomA、atomB 和 atomC 之间的夹角。

*geom* 先前加载的几何结构对象。

*atomA* atomA 在几何结构中的索引。

*atomB* atomB 在几何结构中的索引。

*atomC* atomC 在几何结构中的索引。

**注意** 请注意原子的顺序很重要


**示例：**

```{literalinclude} ../../orca_working_input/compound_example_geometry_getAngle.inp
:language: orca
```


(sec:workflowsautomatization.compound_detailed.commands.geometry.getAtomicNumbers)=
### G.GetAtomicNumbers
函数 *GetAtomicNumbers* 作用于几何结构对象，返回一个数组，其中包含工作几何结构中各元素的原子序数。

**语法（Syntax）：**
*atomNumbers = geom.GetAtomicNumbers()*

*atomNumbers* 将被填入原子序数值的变量

*geom* 应已加载的几何结构对象。

**示例：**

```{literalinclude} ../../orca_working_input/compound_example_geometry_GetAtomicNumbers.inp
:language: orca
```

(sec:workflowsautomatization.compound_detailed.commands.geometry.getBondDistance)=
### G.GetBondDistance
函数 *GetBondDistance* 作用于几何结构对象，返回两个原子之间的距离，单位为 **Bohr**。

**语法（Syntax）：**

*res = geom.GetBondDistance(atomA, atomB)*

其中：

*res* 原子 atomA 和 atomB 之间的距离。

*geom* 先前加载的几何结构对象。

*atomA* atomA 在几何结构中的索引。

*atomB* atomB 在几何结构中的索引。

**注意** 索引从 0 开始计数


**示例：**

```{literalinclude} ../../orca_working_input/compound_example_geometry_getBondDistance.inp
:language: orca
```

(sec:workflowsautomatization.compound_detailed.commands.geometry.getCartesians)=
### G.GetCartesians

函数 *GetCartesians* 作用于几何结构对象（见 {ref}`sec:workflowsautomatization.compound_detailed.commands.geometry`），返回 xyz 笛卡尔坐标。请记住它始终以 **BOHRS** 为单位返回坐标。

**语法（Syntax）：**

*coords = geom.GetCartesians()*

其中：

*coords*：一个 (*nAtoms*,3) 数组，含以 **BOHRS** 为单位的笛卡尔坐标。

*geom*：先前加载的几何结构对象。


**示例：**

```{literalinclude} ../../orca_working_input/compound_example_geometry_GetCartesians.inp
:language: orca
```

(sec:workflowsautomatization.compound_detailed.commands.geometry.getGhostAtoms)=
### G.GetGhostAtoms   
函数 *GetGhostAtoms* 作用于几何结构对象（见 {ref}`sec:workflowsautomatization.compound_detailed.commands.geometry`）。它返回一个大小为 nAtoms 的向量，其中对每个原子，若它是 ghost 原子则值为 -1，否则为该元素的原子序数

**语法（Syntax）：**

*ghostAtoms = geom.GetGhostAtoms()*

*ghostAtoms*：一个 (*nAtoms*,1) 整数向量，取值为 -1 或该原子的原子序数（若它不是 ghost 原子）。

*geom*：先前加载的几何结构对象。

**示例：**

```{literalinclude} ../../orca_working_input/compound_example_geometry_getGhostAtoms.inp
:language: orca
```

(sec:workflowsautomatization.compound_detailed.commands.geometry.getNumOfAtoms)=
### G.GetNumOfAtoms

*GetNumOfAtoms* 返回工作几何结构的原子数目（整数）。

**语法（Syntax）：**

*res = geom.GetNumOfAtoms();*

其中：

*res* 是结果原子数

*geom* 是我们所用几何结构变量的名称（见 {ref}`sec:workflowsautomatization.compound_detailed.commands.geometry`）。

**示例：**
```{literalinclude} ../../orca_working_input/compound_example_geometry_getNumOfAtoms.inp
:language: orca
```

(sec:workflowsautomatization.compound_detailed.commands.geometry.moveAtomToCenter)=
### G.MoveAtomToCenter

函数 *MoveAtomToCenter* 作用于几何结构对象（见 {ref}`sec:workflowsautomatization.compound_detailed.commands.geometry`）。它将调整笛卡尔坐标，使所选原子位于 (0.0 0.0 0.0)。

**语法（Syntax）：**

*geom.MoveAtomToCenter(atom serial nubmer);*

其中：

*geom*：先前加载的几何结构对象。

*atom serial number*：原子在几何结构中的序号。


**示例：**

```{literalinclude} ../../orca_working_input/compound_example_geometry_MoveAtomToCenter.inp
:language: orca
```
**注意** 请记住计数**从 0 开始**，即第一个原子是 0 而不是 1！


(sec:workflowsautomatization.compound_detailed.commands.geometry.read)=
### G.Read

函数 *Read* 作用于几何结构对象（见 {ref}`sec:workflowsautomatization.compound_detailed.commands.geometry`），从与先前步骤相关的性质文件中读取几何结构。

**语法（Syntax）：**

*geom.Read([stepID=myStepID], propertySN=myPropertySN)*

其中：

*geom*：将被更新的几何结构对象。

*stepID*：我们要从中读取几何结构的步骤。若未给出则使用上一步。

*propertySN*：几何结构在性质文件中的序号。若未给出则使用最后一个可用的几何结构。

**示例：**

```{literalinclude} ../../orca_working_input/compound_example_geometry_read.inp
:language: orca
```

(sec:workflowsautomatization.compound_detailed.commands.geometry.removeAtoms)=
### G.RemoveAtoms

函数 *RemoveAtoms* 作用于几何结构对象（见 {ref}`sec:workflowsautomatization.compound_detailed.commands.geometry`）。它接受一个原子列表并从加载的几何结构中移除它们。最终几何结构对象会被更新。

**语法（Syntax）：**

*geom.RemoveAtoms(atom1, atom2, ...);*

其中：

*geom*：先前加载的几何结构对象。

*atom1, atom2, ...*：原子在几何结构中的序号。


**示例：**

```{literalinclude} ../../orca_working_input/compound_example_geometry_RemoveAtoms.inp
:language: orca
```
**注意** 请记住计数**从 0 开始**，即第一个原子是 0 而不是 1！

(sec:workflowsautomatization.compound_detailed.commands.geometry.removeElements)=
### G.RemoveElements

函数 *RemoveElements* 作用于几何结构对象（见 {ref}`sec:workflowsautomatization.compound_detailed.commands.geometry`）。它将从加载的几何结构中移除所有原子序数在给定列表中的原子。

**语法（Syntax）：**

*geom.RemoveElements(atomNumber1, atomicNumber2, ...);*

其中：

*geom*：先前加载的几何结构对象。

*atomicNumber1, atomicNumber2, ...*：要从当前几何结构中移除的元素的原子序数。


**示例：**

```{literalinclude} ../../orca_working_input/compound_example_geometry_RemoveElements.inp
:language: orca
```

(sec:workflowsautomatization.compound_detailed.commands.geometry.writeXYZFile)=
### G.WriteXYZFile

函数 *WriteXYZFile* 作用于几何结构对象（见 {ref}`sec:workflowsautomatization.compound_detailed.commands.geometry`），将当前几何结构对象的坐标写入磁盘上的 xyz 文件。请记住默认以 **Angstrom** 为单位写入坐标。

**语法（Syntax）：**

*res = geom.WriteXYZFile(filename=myFilename, [useBohr=True/False])*

其中：

*res*：若一切顺利则返回 '0' 的整数。

*myFilename* 将包含坐标的文件名。

*useBohr*：布尔值，可取 "True" 或 "False"。这是可选参数，默认值为 "False"。

*geom*：先前加载的几何结构对象。

**注意：** 请注意我们更改了默认单位。现在默认以 Angstrom 为单位写入 xyz 文件。我们添加了参数 UseBohr，默认设为 "False"，但若以 "True" 值使用，则几何结构以 Bohr 保存。

**示例：**

```{literalinclude} ../../orca_working_input/compound_example_geometry_WriteXYZ.inp
:language: orca
```



(sec:workflowsautomatization.compound_detailed.commands.goat)=
### GOAT

在 *Compound* 中我们有 *GOAT* 对象。这些对象可以像 '*compGOAT*' 类型的普通变量一样处理。普通变量与 *GOAT* 变量的一个重要区别在于声明方式。不是普通的：
```
Variable myGoat;
```
我们必须显式声明这是一个 GOAT 对象。因此 goat 声明的语法是：

**语法（Syntax）：**
```
GOAT myGoat;
```

下面是在 *Geometry* 对象上工作的函数列表。

-   Get_Energy ({ref}`sec:workflowsautomatization.compound_detailed.commands.goat.getEnergy`)

-   Get_Num_Of_Geometries ({ref}`sec:workflowsautomatization.compound_detailed.commands.goat.getNumOfGeometries`)

-   ParseEensembleFile ({ref}`sec:workflowsautomatization.compound_detailed.commands.goat.parseEnsembleFile`)

-   Set_Basename ({ref}`sec:workflowsautomatization.compound_detailed.commands.goat.setBasename`)

-   Print ({ref}`sec:workflowsautomatization.compound_detailed.commands.goat.print`)

-   WriteXYZFile ({ref}`sec:workflowsautomatization.compound_detailed.commands.goat.writeXYZFile`)  

**示例：**

```{literalinclude} ../../orca_working_input/compound_example_goat.inp
:language: orca
```

(sec:workflowsautomatization.compound_detailed.commands.goat.getEnergy)=
### Goat.Get_Energy

函数 *Get_Energy* 作用于 goat 对象（见 {ref}`sec:workflowsautomatization.compound_detailed.commands.goat`），返回所请求结构的能量（双精度数）。

**语法（Syntax）：**

*res = myGoat.Get_Energy(geomID=myGeomID)*

其中：

*res*：所请求结构的能量（双精度数）。

*myGoat* 已加载的 GOAT 对象（意味着它已解析过系综文件，见（见 {ref}`sec:workflowsautomatization.compound_detailed.commands.goat.parseEnsembleFile`）。

*myGeomID*：所请求结构的几何结构 ID。计数从 1 开始。


**示例：**

  见 {ref}`sec:workflowsautomatization.compound_detailed.commands.goat` 中的示例


(sec:workflowsautomatization.compound_detailed.commands.goat.getNumOfGeometries)=
### Goat.Get_Num_Of_Geometries

函数 *Get_Num_Of_Geometries* 作用于 goat 对象（见 {ref}`sec:workflowsautomatization.compound_detailed.commands.goat`），返回当前 *GOAT* 对象中可用结构的数目（整数）。

**语法（Syntax）：**

*res = myGoat.Get_Num_Of_Geometries()*

其中：

*res*：当前 *GOAT* 对象中几何结构数目的整数。

*myGoat* 已加载的 GOAT 对象（意味着它已解析过系综文件，见（见 {ref}`sec:workflowsautomatization.compound_detailed.commands.goat.parseEnsembleFile`）。

**示例：**

  见 {ref}`sec:workflowsautomatization.compound_detailed.commands.goat` 中的示例

(sec:workflowsautomatization.compound_detailed.commands.goat.parseEnsembleFile)=
### Goat.ParseEnsembleFile

函数 *ParseEnsembleFile* 作用于 goat 对象（见 {ref}`sec:workflowsautomatization.compound_detailed.commands.goat`）。它将读取 GOAT 运行创建的系综文件，然后用当前 *GOAT* 对象中每个可用几何结构的几何结构和能量更新该对象。

**语法（Syntax）：**

*res = geom.ParseEnesembleFile(filename=myFilename)*

其中：

*res*：若一切顺利则返回 '0' 的整数。

*myFilename* 将包含坐标的文件名。

*myGoat*：先前加载的 GOAT 对象。


**示例：**

  见 {ref}`sec:workflowsautomatization.compound_detailed.commands.goat` 中的示例

**注意：** 旧语法（Parse_Ensemble_File）仍然兼容，但请不要使用，因为它将来会被弃用。

(sec:workflowsautomatization.compound_detailed.commands.goat.setBasename)=
### Goat.Set_Basename

函数 *Set_Basename* 作用于 goat 对象（见 {ref}`sec:workflowsautomatization.compound_detailed.commands.goat`）。它设置 GOAT 运行所创建系综文件的基名。它会在基名末尾自动添加扩展名：`'.finalensemble.xyz'`。

**语法（Syntax）：**

*myGoat.Set_Basename(myFilename)*

其中：

*myFilename* GOAT 系综文件的基名（**不带扩展名 'finalensemble.xyz'**）。

*myGOAT*：先前加载的 GOAT 对象。


**示例：**

见 {ref}`sec:workflowsautomatization.compound_detailed.commands.goat` 中的示例

(sec:workflowsautomatization.compound_detailed.commands.goat.print)=
### Goat.Print

函数 *Print* 作用于 goat 对象（见 {ref}`sec:workflowsautomatization.compound_detailed.commands.goat`）。它将在输出中打印当前 GOAT 对象的几何结构。

**语法（Syntax）：**

*myGoat.Print()*

其中：

*myGoat*：先前加载的 GOAT 对象。


**示例：**

见 {ref}`sec:workflowsautomatization.compound_detailed.commands.goat` 中的示例

(sec:workflowsautomatization.compound_detailed.commands.goat.writeXYZFile)=
### Goat.WriteXYZFile

函数 *WriteXYZFile* 作用于 goat 对象（见 {ref}`sec:workflowsautomatization.compound_detailed.commands.goat`）。它将所请求的几何结构写入磁盘上的 XYZ 文件。它需要两个参数：
1. 几何结构的几何结构 ID 和
2. 用于存储几何结构的文件名

**语法（Syntax）：**

*myGoat.WriteXYZFile(geomID=myGeomID, filename=myFilename)*

其中：

*myFilename：* 用于在磁盘上存储几何结构的名称。

*myGeomID*：所请求结构的几何结构 ID。计数从 1 开始。


**示例：**

见 {ref}`sec:workflowsautomatization.compound_detailed.commands.goat` 中的示例


(sec:workflowsautomatization.compound_detailed.commands.propertyFile.getNumOfInstances)= 
###  GetNumOfInstances
*GetNumOfInstances* 返回性质文件中特定对象的实例数目。

**语法（Syntax）：**

*[res=] GetNumOfInstances(propertyName=myName, [step=myStep], [filename=myFilename], [baseProperty=true/false])*

*其中：*

*res：* 返回性质文件中所请求性质实例数目的整数。

*propertyName：* 定义用户要读取变量的字符串别名。

*step：* 我们要从中读取性质的步骤。若未给出则读取最后一步的性质文件。

*filename：* 性质文件的文件名。若同时提供了文件名和步骤，程序将忽略步骤并尝试读取给定文件名的性质文件。

**注意** 请注意文件名末尾会添加扩展名 *.property.txt*。

*baseProperty：* true/false 布尔值。默认值为 false。若设为 true，则读取所询问类型的通用性质。这意味着如果询问偶极矩，将返回最后一个偶极矩，而不管定义的是 MP2 还是 SCF 的。


 **示例**
```{literalinclude} ../../orca_working_input/compound_example_propertyFile_getNumOfInstances.inp
:language: orca
```

(sec:workflowsautomatization.compound_detailed.commands.goto)=
### GoTo
*GoTo* 命令允许在 *compound* 脚本的正常流程内"跳转"。该命令的语法通过示例可以最好地说明。

**示例：**
```{literalinclude} ../../orca_working_input/compound_example_goto.inp
:language: orca
```

请注意，我们用作 *GoTo* 命令标签的变量应像普通变量一样事先定义。

(sec:workflowsautomatization.compound_detailed.commands.if)=
### If
*if* 块允许用户做出决策。*Compound* 中的语法如下：\
**语法（Syntax）：**

**If** *(expression)* **Then**

*actions*

**Else if** *(expression)* **Then**

*actions*

**Else**

*actions*

**Endif**

下面是 *compound* 中 *if 块* 用法的示例。

```{literalinclude} ../../orca_working_input/0976.cmp
:language: orca
```

关于语法的一些说明：

*Else if* 或 *Else* 块不是必需的。

可用的数值运算符有：*'>'、'<'、'>='、'<=',
'='*。

可用的逻辑运算符有：*'and' 和 'or'*。

遗憾的是当前版本不允许多重括号。

现在可以比较字符串了。


(sec:workflowsautomatization.compound_detailed.commands.linAlgegra.invertMatrix)=
### InvertMatrix
*Compound* 可以执行矩阵代数运算，可用的代数运算之一是矩阵求逆。请注意，我们要求逆的矩阵**必须是**实的方阵。

**语法（Syntax）：**\
*AInvert = A.InvertMatrix();*

其中：

- *A：* 待求逆的矩阵。
- *AInvert：* A 的逆矩阵。它可以是 A 本身，这样 A 就会被更新。

**示例：**
```{literalinclude} ../../orca_working_input/compound_example_linAlgebra_invertMatrix.inp
:language: orca
```

(sec:workflowsautomatization.compound_detailed.commands.linAlgegra.Mat_p_Mat)=
### Mat_p_Mat
*Compound* 可以执行矩阵代数运算，可用的代数运算之一是矩阵加法。要将两个矩阵相加，它们**必须**具有相同的维度。


**语法（Syntax）：**\
*C=Mat_p_Mat(alpha, A, beta, B);*

其中：

- *C：* 结果矩阵。
- *alpha：* 矩阵 A 的系数。
- *A：* 加法的左矩阵。
- *beta：* 矩阵 B 的系数。
- *B：* 加法的右矩阵。

**示例：**
```{literalinclude} ../../orca_working_input/compound_example_linAlgebra_mat_p_mat.inp
:language: orca
```

(sec:workflowsautomatization.compound_detailed.commands.linAlgegra.Mat_x_Mat)=
### Mat_x_Mat
*Compound* 可以执行矩阵代数运算，可用的代数运算之一是矩阵乘法。一般我们可以将每个矩阵乘以常数 *alpha* 和 *beta*，使得一般乘法为：

*C=(alpha*A)*(beta*B)

此外矩阵 A 和 B 都允许转置。

**语法（Syntax）：**\
*C=Mat_x_Mat(A, B, [transposeA], [transposeB], [alpha], [beta]);*

其中：

- *C：* 结果矩阵。
- *A：* 乘法的左矩阵。
- *B：* 乘法的右矩阵。
- *transposeA：* 布尔值，表明矩阵 A 在乘法前是否应转置（默认：False）。
- *transposeB：* 布尔值，表明矩阵 B 在乘法前是否应转置（默认：False）。
- *alpha：* 乘法前乘矩阵 A 的标量（默认 1.0）。
- *beta：* 乘法前乘矩阵 B 的标量（默认 1.0）。

**示例：**
```{literalinclude} ../../orca_working_input/compound_example_linAlgebra_mat_x_mat.inp
:language: orca
```

(sec:workflowsautomatization.compound_detailed.commands.linAlgegra.Mat_x_Scal)=
### Mat_x_Scal
*Compound* 可以执行矩阵代数运算，可用的代数运算之一是矩阵元素与标量相乘。该函数返回相乘后的矩阵，它可以是我们在括号中用作参数的那个（即被更新），也可以是另一个。

**语法（Syntax）：**\
*C=Mat_x_Scal(alpha, A);*

其中：

- *C：* 结果矩阵。
- *alpha：* 乘矩阵 A 元素的标量。
- *A：* 待相乘的矩阵。

**示例：**
```{literalinclude} ../../orca_working_input/compound_example_linAlgebra_mat_x_scal.inp
:language: orca
```


(sec:workflowsautomatization.compound_detailed.commands.newgeom)=
### NewGeom

*NewGeom* 是几何结构操作的平台。基本思想是拥有能够读取几何结构、然后根据我们需要的某些特性产生一个或多个新几何结构的函数。目前 *NewGeom* 名下有 4 个不同函数，即：
Displace、Remove_Atom、Remove_Element。

**注意：** 旧语法（New_Geom）仍然兼容，但请不要使用，因为它将来会被弃用。

(sec:workflowsautomatization.compound_detailed.commands.new_geom.displace)=
#### Displace

"*Displace'*" 背后的思想是有一个结构，对其执行解析频率计算（目前我们不在性质文件中存储数值频率），然后从该计算读取 Hessian，根据我们选择的振动简正模式调整几何结构。该命令的语法是：

**语法：** NewGeom = (Displace, step, hessian, frequency, scaling)

其中：\
*step* 是我们选择原始几何结构的步骤\
*hessian* 是从性质文件读取的 Hessian\
*frequency* 定义我们将使用哪个简正模式，\
*scaling* 是我们希望位移严重程度的因子。

我们应当注意 *Displace* 是 *new_geom*
命令家族中唯一不在磁盘上存储几何结构、而只是将新几何结构在内部传递给下一次计算的命令。该命令用法的示例可以在随 ORCA 提供的脚本
'iterativeOptimization' 中找到。相关部分如下：**示例：**

```orca
# Define variables
		Variable MaxNTries    =  25; 
		Variable CutOff       = -50;
		Variable displacement = 0.6;
		Variable NNegative =   0;  
		Variable freqs[];
		Variable modes[];
		Variable NFreq;
		Variable limit;
		Variable done;
		Variable FinalEnergy; 
		
		# ===========================================================
		# Start a for loop over number of tries
		# ===========================================================
		For itry From 1 To maxNTries Do
		
		# ----------------------------------
		# Run a geometry optimization
		# ----------------------------------
		New_Step
		! tightopt freq verytightscf nopop def2-TZVP xyzfile
		Step_End
		Read freqs  = THERMO_FREQS[itry];
		Read modes  = HESSIAN_MODES[itry];
		Read NFreq  = THERMO_NUM_OF_FREQS[itry];
		limit = NFreq - 1;
		# ----------------------------------
		#  check for sufficeintly negative 
		#  frequencies
		# ----------------------------------
		NNegative = 0;
		For ifreq From 0 to limit Do
		if ( freqs[ifreq] < CutOff )  then
		New_Geom = (Displace, itry,  modes,  ifreq, displacement);
```

(sec:workflowsautomatization.compound_detailed.commands.openFile)=
### OpenFile

*Compound* 可以在磁盘上写文本文件。要写入文件必须先创建文件指针。为此 *Compound* 中有命令 *OpenFile*。

**语法（Syntax）：**\
filePtr = *OpenFile*(*Filename*, "*open mode*");

*filePtr* 是先前声明的变量。

*Filename* 可以是字符串或字符串类型的变量，表示磁盘上文件的名称。

有两种可用的*打开模式*：
- 'w'。该模式下将创建新文件，用户可以在其上写入。如果存在同名旧文件，其内容将被删除。
- 'a'。该模式下如果文件已存在，用户将追加到文件中已有内容之后。
  

**示例：**
```{literalinclude} ../../orca_working_input/ORCA_Test_1798.inp
:language: orca
```

(sec:workflowsautomatization.compound_detailed.commands.new_geom.remove_atom)=
#### Remove_Atom

Remove_atom 根据原子索引从几何结构中移除一个原子。我们应当指出 ORCA 中原子计数从 0 开始。执行该命令后，它将在磁盘上以 xyz 格式存储一个新的几何结构，其中只有给定索引的原子缺失。

**语法（Syntax）：**

NewGeom = ( Remove_atom, atomIndex, \"filename\", stepIndex, \[geometry
Index\]);

其中：\
*atom Index* 是我们要移除的原子编号。它可以是整数或变量。\
*filename* 是我们想用于新 xyz 文件的文件名。它可以是引号中的字符串或先前已定义的变量。在名称中 xyz 扩展名会自动追加。*step Index* 是我们从中获取初始几何结构的步骤编号。它必须是整数。*geometry Index* 如果相应性质文件中有多个几何结构，我们可以选择一个。如果未给出数字，默认程序将使用最后一个。

**示例：**

如果我们使用常规 ORCA 输入文件：

```{literalinclude} ../../orca_working_input/runRemoveAtom.inp
:language: orca
```

连同 compound 文件 \"removeAtom.cmp\"：

```{literalinclude} ../../orca_working_input/removeAtom.cmp
:language: orca
```

则将创建 xyz 文件 'newGeom.xyz'，应如下所示：

```orca
2

   H         2.5974927       -0.4116633        0.7667449
   H         2.5931354       -0.4494962       -0.7447820
```

其中 *atomIndex = 0* 的原子（即第一个原子，即氧）被移除。

(sec:workflowsautomatization.compound_detailed.commands.new_geom.remove_elements)=
#### Remove_Element

Remove_element 与 Remove_atom 类似，但不是使用原子索引而是使用其原子序数。因此语法是：

**语法（Syntax）：** NewGeom = ( Remove_Element, atomic number, \"filename\",
stepIndex, \[geometry Index\]);

其中：\
*atomic number* 是我们要移除的原子的原子序数。它可以是整数或变量。\
*filename* 是我们想用于新 xyz 文件的文件名。它可以是引号中的字符串或先前已定义的变量。在名称中 xyz 扩展名会自动追加。*step Index* 是我们从中获取初始几何结构的步骤编号。它必须是整数。*geometry Index* 如果相应性质文件中有多个几何结构，我们可以选择一个。如果未给出数字，默认程序将使用最后一个。

**示例：**

如果我们再次使用段落
[1.1.7.2](#sec:workflowsautomatization.compound_detailed.commands.new_geom.remove_atom){reference-type="ref"
reference="sec:workflowsautomatization.compound_detailed.commands.new_geom.remove_atom"} 中的输入，但不是请求 compound 文件 \"removeAtom.cmp\"，而是请求如下所示的 compound 文件 \"removeElement.cmp\"：

```{literalinclude} ../../orca_working_input/removeElement.cmp
:language: orca
```

则我们将再次得到段落
{ref}`sec:workflowsautomatization.compound_detailed.commands.new_geom.remove_atom` 中创建的同一个 xyz 文件，因为原子序数为 8 的原子（即氧）将从原始几何结构中移除。


(sec:workflowsautomatization.compound_detailed.commands.newstep)=
### NewStep

NewStep 标志新的 ORCA 输入的开始。

**语法（Syntax）：**

NewStep\
*\...Normal ORCA input commands*\
StepEnd

对 ORCA 输入没有限制，当然除了它不应包含另一个 Compound 块。重要的是要记住 *NewStep* 命令应始终以 *Step_End* 命令结束。下面给出一个简单示例。

**注意：** 旧语法（New_Step/Step_End）仍然兼容，但请不要使用，因为它将来会被弃用。

**示例：**

```orca
NewStep
! BP86 def2-SVP
StepEnd
```

与常规 ORCA 输入只有一个基本的根本区别。
在 *NewStep* 块内不需要包含几何结构。
ORCA 将自动尝试从上一次计算读取几何结构。当然也可以给出几何结构，那样 ORCA 将使用它。

(sec:workflowsautomatization.compound_detailed.commands.stringrelated.print)=
### Print

ORCA 输出中的打印可以用 *print* 命令自定义。
*print* 命令的语法紧密遵循 C/C++ 中相应的 printf 命令。因此 *print* 命令的用法是：

**语法（Syntax）：**\
*print(format string, \[variables\]);*

对每个变量可以有说明符和说明符的标志。目前 *print* 命令支持三种数据类型，即整数、双精度数和字符串。

格式说明符遵循下列原型：
*%\[flags\]\[width\]\[.precision\]specifier*

其中说明符和标志的细节见表
{numref}`compoundPrintSpecifiers`

(compoundPrintSpecifiers)=
:::{table} compound 打印说明符
| 说明符    |                                       |     |
|:----------|:--------------------------------------|:----|
| s         | 字符串                                |     |
| d         | 整数                                  |     |
| lf        | 双精度数                              |     |
|           |                                       |     |
| 标志      |                                       |     |
|           |                                       |     |
| number    | 宽度                                  |     |
| .number   | 小数位数                              |     |
| \-        | 左对齐（默认为右对齐）                |     |
|           |                                       |     |
:::

**示例：**

```{literalinclude} ../../orca_working_input/0954.cmp
:language: orca
```

(sec:workflowsautomatization.compound_detailed.commands.propertyFile.readProperty)= 
### ReadProperty
*Compound* 的基本特性之一是能够轻松地从性质文件读取 ORCA 计算得到的值。

**语法（Syntax）：**

*[res=] readProperty(propertyName=myName, [stepID=myStep], [filename=myFilename], [baseProperty=true/false])*

*其中：*
*res：* 若在性质文件中找到该性质则返回其索引的整数，若性质不存在则返回 -1。这不是必需的。

*propertyName：* 定义用户要读取变量的字符串别名。

*stepID：* 我们要从中读取性质的步骤。若未给出则读取最后一步的性质文件。

*filename：* 性质文件的文件名。若同时提供了文件名和步骤，程序将忽略步骤并尝试读取给定文件名的性质文件。

**注意** 请注意文件名末尾会添加扩展名 *.property.txt*。

*baseProperty：* true/false 布尔值。默认值为 false。若设为 true，则读取所询问类型的通用性质。这意味着如果询问偶极矩，将返回最后一个偶极矩，而不管定义的是 MP2 还是 SCF 的。


 **示例**
```{literalinclude} ../../orca_working_input/compound_example_propertyFile_readProperty.inp
:language: orca
```


(sec:workflowsautomatization.compound_detailed.commands.read_geom)=
### Read_Geom

Read_Geom 将从先前步骤读取几何结构。

**语法（Syntax）：**\
Read_Geom $number$

这里 number 是我们想要从中读取几何结构的作业编号。该指令应位于 *NewStep* -
*StepEnd* 块之前。

**示例：**

```orca
#Compound Job 1
New_Step
!BP86 def2-SVP
Step_End

#Compound Job 2
New_Step
!BP86 def2-SVP opt
Step_End

#Compound Job 3
Read_Geom 1
New_Step
!CCSD  def2-SVP
Step_End

End  #Final End
```

这种情况下，第三次计算通过 *Read_MGeom 1* 命令
将从第一次计算读取几何结构。

(sec:workflowsautomatization.compound_detailed.commands.orca.readMOs)=
### ReadMOs

ReadMOs 从先前步骤读取分子轨道。

**语法（Syntax）：**\
*ReadMOs(stepNumber);*

其中：

- *stepNumber：* 是我们想要从中读取轨道的步骤编号。

**示例：**
```{literalinclude} ../../orca_working_input/compound_example_readMOs.inp
:language: orca
```

(sec:workflowsautomatization.compound_detailed.commands.stringrelated.getBasename)=
### S.GetBasename

在 *Compound* 中字符串具有普通变量的全部功能。此外它们还有一些仅作用于字符串的附加函数。其中之一是函数 *GetBasename*。该函数搜索字符串，如果包含点，则返回点之前的字符串部分。

**语法（Syntax）：**

*result = source.GetBasename();*

*其中：*

*result* 是返回的字符串。

*source* 是原始字符串。

**注意** 如果原始字符串不包含点，则结果字符串将是源字符串的副本。

**示例：**

```{literalinclude} ../../orca_working_input/compound_example_string_getBasename.inp
:language: orca
```
(sec:workflowsautomatization.compound_detailed.commands.stringrelated.getChar)=
### S.GetChar

在 *Compound* 中字符串具有普通变量的全部功能。此外它们还有一些仅作用于字符串的附加函数。其中之一是函数 *GetChar*。该函数搜索字符串，如果包含点，则返回点之后的字符串部分。

**语法（Syntax）：**

*result = source.GetChar(index);*

*其中：*

*result* 是返回的字符串。

*index* 是字符串中字符的索引。请记住计数从 **0** 开始而不是 1。

*source* 是原始字符串。

**注意** 如果索引大于字符串长度或为负，则程序将退出。

**示例：**

```{literalinclude} ../../orca_working_input/compound_example_string_getBasename.inp
:language: orca
```

(sec:workflowsautomatization.compound_detailed.commands.stringrelated.getSuffix)=
### S.GetSuffix

在 *Compound* 中字符串具有普通变量的全部功能。此外它们还有一些仅作用于字符串的附加函数。其中之一是函数 *GetSuffix*。该函数搜索字符串，如果包含点，则返回点之后的字符串部分。

**语法（Syntax）：**

*result = source.GetSuffix();*

*其中：*

*result* 是返回的字符串。

*source* 是原始字符串。

**注意** 如果原始字符串不包含点，则结果字符串将为空字符串。

**示例：**

```{literalinclude} ../../orca_working_input/compound_example_string_getBasename.inp
:language: orca
```


(sec:workflowsautomatization.compound_detailed.commands.endstep)=
### StepEnd

StepEnd 标志 ORCA 输入的结束。它应始终是 compound 块内以
*New_Step* 开始的 ORCA 输入的最后一条指令（见段落
{ref}`sec:workflowsautomatization.compound_detailed.commands.newstep`）

**注意：** 旧语法（New_Step/Step_End）仍然兼容，但请不要使用，因为它将来会被弃用。

(sec:workflowsautomatization.compound_detailed.commands.syscmd)=
### Sys_cmd

Sys_cmd 将读取系统命令并执行它。

**语法（Syntax）：**\
Sys_cmd *command*

**示例：**

```orca
SYS_CMD "orca_mapspc test.out SOCABS -x0700 -x1900 -w0.5 -eV -n10000 "
```

(sec:workflowsautomatization.compound_detailed.commands.timerrelated.timer)=
### Timer

*timer* 是可以为 compound 中的任务计时的对象。在使用 timer 对象之前必须先声明它。*timer* 的声明与其他变量略有不同，因为它必须显式声明其类型。

**语法（Syntax）**

*timer myTimer;*

*其中* 

*timer* 代替普通的 *variable* 命令，将变量类型显式设为 *compTimer*。

*myTimer* 是该对象的普通实例。


**示例：**

```{literalinclude} ../../orca_working_input/0961.cmp
:language: orca
```

下面是在 *Timer* 对象上专用的函数列表。

- Last ({ref}`sec:workflowsautomatization.compound_detailedd.commands.timer.last`)

- Reset ({ref}`sec:workflowsautomatization.compound_detailedd.commands.timer.reset`)

- Start ({ref}`sec:workflowsautomatization.compound_detailedd.commands.timer.start`)

- Stop ({ref}`sec:workflowsautomatization.compound_detailedd.commands.timer.stop`)

- Total ({ref}`sec:workflowsautomatization.compound_detailedd.commands.timer.total`)

(sec:workflowsautomatization.compound_detailedd.commands.timer.last)=
### T.Last 

Last 是作用于 *timer* 对象的函数。它以实数形式返回计时器的上一次值。

**语法（Syntax）**

*myTimer.Last();*

*其中：*

*myTimer：* 是先前初始化的 *timer* 对象。

**示例：**

```{literalinclude} ../../orca_working_input/0961.cmp
:language: orca
```
**注意** 在使用 last 之前，*timer* 对象除定义外还必须使用 *Start* 初始化（见 {ref}`sec:workflowsautomatization.compound_detailedd.commands.timer.start`）


(sec:workflowsautomatization.compound_detailedd.commands.timer.reset)=
### T.Reset 

*Reset* 是作用于 *timer* 对象的函数。它将 *timer* 对象重置为初始状态。

**语法（Syntax）**

*myTimer.Reset();*

*其中：*

*myTimer：* 是先前初始化的 *timer* 对象。

**示例：**

```{literalinclude} ../../orca_working_input/0961.cmp
:language: orca
```


(sec:workflowsautomatization.compound_detailedd.commands.timer.start)=
### T.Start 

*Start* 是作用于 *timer* 对象的函数。它将 *timer* 对象返回到初始状态。

**语法（Syntax）**

*myTimer.Start();*

*其中：*

*myTimer：* 是先前初始化的 *timer* 对象。

**示例：**

```{literalinclude} ../../orca_working_input/0961.cmp
:language: orca
```


(sec:workflowsautomatization.compound_detailedd.commands.timer.stop)=
### T.Stop

*Stop* 是作用于 *timer* 对象的函数。它停止计时器计数。

**语法（Syntax）**

*myTimer.Stop();*

*其中：*

*myTimer：* 是先前初始化的 *timer* 对象。

**示例：**

```{literalinclude} ../../orca_working_input/0961.cmp
:language: orca
```

(sec:workflowsautomatization.compound_detailedd.commands.timer.total)=
### T.Total 

*Total* 是作用于 *timer* 对象的函数。它返回总时间（实数）。

**语法（Syntax）**

*myTimer.Total();*

*其中：*

*myTimer：* 是先前初始化的 *timer* 对象。

**示例：**

```{literalinclude} ../../orca_working_input/0961.cmp
:language: orca
```


(sec:workflowsautomatization.compound_detailed.commands.variables.general)=
### 变量 - 概述（Variables - General）

*Compound* 语言中的一切都基于变量。它们的含义和用法与任何编程语言中类似：需要先声明变量然后给它赋值。值得注意的是，在 *Compound* 中，变量必须在赋值之前声明，遵循类似 C 的语言的语法规则。这与 Python 等语言不同，在那些语言中可以不事先声明就给变量赋值。Compound 中这一规则的唯一例外是 for 循环中的索引，它不需要事先声明。

在 *Compound* 中我们支持下列变量数据类型：

-   整数（Integer）

-   双精度数（Double）

-   字符串（String）

-   布尔值（Boolean）

-   文件指针（File pointer）

除这些数据类型外 *Compound* 还支持 *Geometry* 和 *Timer* 类型的变量，但它们单独处理
（见 {ref}`sec:workflowsautomatization.compound_detailed.commands.geometry` 和 {ref}`sec:workflowsautomatization.compound_detailed.commands.timerrelated.timer`）。

*Compound* 中每个变量有 3 大使用类别：

- 声明（见 {ref}`sec:workflowsautomatization.compound_detailed.commands.variables.general`）
  
- 赋值（见 {ref}`sec:workflowsautomatization.compound_detailed.commands.variables.assignement`）和 
  
- 变量函数（见 {ref}`sec:workflowsautomatization.compound_detailed.commands.variables.functions`）

(sec:workflowsautomatization.compound_detailed.commands.variables.declaration)=
### 变量 - 声明（Variables - Declaration）

目前在 *Compound* 中有 6 种不同的变量声明方式。其语法如下：

**语法（Syntax）：**

**A.** *Variable name;*

**B.** *Variable name1, name2;*

**C.** *Variable name=value;*

**D.** *Variable name\[$n$\];*

**E.** *Variable name\[$n1$\]\[$n2$\];*

**F.** *Variable name={value1, value2, \...}*;



**注意** 在以前版本的 *Compound* 中，对于是矩阵但大小未知的变量，必须用下列语法声明变量：

*Variable name = \[\];*

现在已经改变，不再需要空括号，因此该变量可以像情形 *A* 中那样定义为普通变量。

**示例**

```{literalinclude} ../../orca_working_input/0973.cmp
:language: orca
```

关于不同变量声明情形的一些说明。\
**情形 A** 是最简单的，我们只是声明变量名。

**情形 B** 类似于*情形 A*，但这里同时声明多个变量。

在**情形 C** 中我们将变量声明与为变量赋值结合起来。值得注意的是这种情况下 *Compound* 会根据给定的值自动推断变量类型。

**情形 D** 声明一个给定大小的一维数组。

**情形 E** 声明一个给定大小的二维数组。对这种情形，以及相应地对*情形 E*，可以使用先前定义的整数变量代替数字。

**情形 F** 基于给定值的列表定义数组。数组将根据列表的大小自动定义其大小。列表中的值不必都是同一类型。

**注意** 过去对*情形 F* 需要在变量名后写空括号。这不再必要了。

**注意** 重要的是不要忘记每个声明末尾的最终 **;** 符号，因为省略它的结果是未定义的。

(sec:workflowsautomatization.compound_detailed.commands.variables.assignement)=
### 变量 - 赋值（Variables - Assignment）

为变量赋值有相当直接的语法。

**语法（Syntax）：**\
*VariableName = CustomFunction;*

*其中：*

*VariableName* 是已声明的变量。

*CustomFunction* 是数学表达式。

**示例：**

```{literalinclude} ../../orca_working_input/0974.cmp
:language: orca
```

**注意** 重要的是记住用 **';'** 符号结束变量赋值。

(sec:workflowsautomatization.compound_detailed.commands.variables.functions)=
### 变量 - 函数（Variables - Functions）

*Compound* 中的变量有少量函数可以帮助提取关于它们的信息。在当前版本的 *Compound* 中这些函数如下：


**语法（Syntax）：**\
VariableName.Function();

其中 *VariableName* 是已声明的变量。然后该函数将返回一个值，取决于我们所用的 *Function*。


目前 *Compound* 支持下列函数：

-  GetBool() {ref}`sec:workflowsautomatization.compound_detailed.commands.variables.functions.getBool` 
-  GetDim1() {ref}`sec:workflowsautomatization.compound_detailed.commands.variables.functions.getDim1` 
-  GetDim2() {ref}`sec:workflowsautomatization.compound_detailed.commands.variables.functions.getDim2` 
-  GetDouble() {ref}`sec:workflowsautomatization.compound_detailed.commands.variables.functions.getDouble` 
-  GetInteger() {ref}`sec:workflowsautomatization.compound_detailed.commands.variables.functions.getInteger` 
-  GetSize() {ref}`sec:workflowsautomatization.compound_detailed.commands.variables.functions.getSize` 
-  GetString() {ref}`sec:workflowsautomatization.compound_detailed.commands.variables.functions.getString` 
-  PrintMatrix() {ref}`sec:workflowsautomatization.compound_detailed.commands.variables.functions.printMatrix` 
  
**示例：**

```{literalinclude} ../../orca_working_input/0974.cmp
:language: orca
```

(sec:workflowsautomatization.compound_detailed.commands.variables.functions.getBool)=
### V.GetBool()

如果变量是布尔值或整数，该函数将返回布尔值。对整数，0 返回 *false*，所有其他整数值返回 *true*。在所有其他情况下程序将崩溃并提供相关消息。


**语法（Syntax）：**

*myVar.GetBool();*

*其中：* 

*myVar* 是已初始化的变量。

**示例**

```{literalinclude} ../../orca_working_input/compound_example_variables_functions_getDouble.inp
:language: orca
```

(sec:workflowsautomatization.compound_detailed.commands.variables.functions.getDim1)=
### V.GetDim1()

 该函数作用于变量。它将返回数组第一维的大小。如果变量是标量则返回 1。

**语法（Syntax）：**

*myVar.GetDim1();*

*其中：* 

*myVar* 是已初始化的变量。

**示例**

```{literalinclude} ../../orca_working_input/compound_example_variables_functions_getDim1.inp
:language: orca
```


(sec:workflowsautomatization.compound_detailed.commands.variables.functions.getDim2)=
### V.GetDim2()

该函数作用于变量。它将返回数组第二维的大小。如果变量是标量或一维数组则返回 1。

**语法（Syntax）：**

*myVar.GetDim2();*

*其中：* 

*myVar* 是已初始化的变量。

**示例**

```{literalinclude} ../../orca_working_input/compound_example_variables_functions_getDim1.inp
:language: orca
```

(sec:workflowsautomatization.compound_detailed.commands.variables.functions.getDouble)=
### V.GetDouble()

该函数作用于变量。如果变量是整数或双精度数则返回双精度值。在所有其他情况下程序将崩溃并提供相关消息。

**语法（Syntax）：**

*myVar.GetDouble();*

*其中：* 

*myVar* 是已初始化的变量。

**示例**

```{literalinclude} ../../orca_working_input/compound_example_variables_functions_getDouble.inp
:language: orca
```

(sec:workflowsautomatization.compound_detailed.commands.variables.functions.getInteger)=
### V.GetInteger()
该函数作用于变量。如果变量是整数或双精度数则返回整数值。在所有其他情况下程序将崩溃并提供相关消息。

**语法（Syntax）：**

*myVar.GetInteger();*

*其中：* 

*myVar* 是已初始化的变量。

**示例**

```{literalinclude} ../../orca_working_input/compound_example_variables_functions_getDouble.inp
:language: orca
```

(sec:workflowsautomatization.compound_detailed.commands.variables.functions.getSize)=
### V.GetSize()

该函数作用于变量。如果变量是标量则返回 1。如果变量是一维数组则返回数组大小，与 *GetDim1()* 相同。如果变量是二维数组则返回结果 Dim1\*Dim2。

**语法（Syntax）：**

*myVar.GetSize();*

*其中：* 

*myVar* 是已初始化的变量。

**示例**

```{literalinclude} ../../orca_working_input/compound_example_variables_functions_getDim1.inp
:language: orca
```

(sec:workflowsautomatization.compound_detailed.commands.variables.functions.getString)=
### V.GetString()
该函数作用于变量。它将返回变量值的字符串形式。它适用于双精度数、整数和布尔值。

**语法（Syntax）：**

*myVar.GetString();*

*其中：* 

*myVar* 是已初始化的变量。

**示例**

```{literalinclude} ../../orca_working_input/compound_example_variables_functions_getDouble.inp
:language: orca
```

(sec:workflowsautomatization.compound_detailed.commands.variables.functions.printMatrix)=
### V.PrintMatrix()
该函数作用于变量。它将以 8 列的格式打印数组。

**语法（Syntax）：**
*myVar.PrintMatrix([NCols=numOfColumns]);*

*其中：* 

*myVar* 是已初始化的变量。

*numOfColumns* 是打印所期望的列数。这不是必需的，若不使用则默认 ORCA 将使用 **4** 列打印。

**示例**

**示例：**
```{literalinclude} ../../orca_working_input/compound_example_variables_functions_printMatrix.inp
:language: orca
```
**注意** 对于标量，它只打印表头而不打印任何值。

**注意** 它只适用于 *'double'* 或 *'integer'* 类型的数组。对所有其他类型的变量程序将退出并提供错误消息。

(sec:workflowsautomatization.compound_detailed.commands.variables.with)=
### With

"with" 命令的目的是增加在调用 compound 时调整 compound 文件中已定义的某些变量的能力。这意味着如果 compound 文件中定义了一个变量并给它赋了值，我们可以在调用期间更改变量的赋值。

可以传递数字、字符串或布尔变量。

应当注意，无法以这种方式调用数组变量。除了这一限制外，with 情况下变量赋值的语法与普通 *Compound* 脚本中的变量赋值相同。

这里一个重要说明是，如果我们使用 *With* 命令，即使我们调用的是 *Compound* 脚本文件，*%Compound* 块也应以 *'End'* 结束。\
**语法（Syntax）：**\
**% compound** *\"filename\"*\
**With**\
*var1* = *val1*;\
*var2* = *val2*;\
**End**\
**示例：**

```{literalinclude} ../../orca_working_input/0975.cmp
:language: orca
```

(sec:workflowsautomatization.compound_detailed.commands.stringrelated.write2file)=
### Write2File

使用 *Print* 命令（见 {ref}`sec:workflowsautomatization.compound_detailed.commands.stringrelated.print`）可以写入 ORCA 输出。不过
可能更希望写入不同的文件。在
*Compound* 中可以用 *write2File* 命令实现这一点。其
语法紧密遵循编程语言 C 的 'fprintf' 命令的语法。参数定义和语法
与 *Compound 'Print'* 命令的语法相同，只是
应定义一个文件对象来接收打印内容。

**语法（Syntax）：**\
*Write2File(file variable, format string, \[variables\]);*

*其中：*

*file variable：* 是对应于已通过 *OpenFile* 命令打开的文件的预定义变量。

*format string* 和 *variables* 完全遵循 *Print* 命令的语法，更多
细节请参阅章节 {ref}`sec:workflowsautomatization.compound_detailed.commands.stringrelated.print`。

**注意** 请记住一旦所有内容都写入文件，就用
*CloseFile* 命令关闭文件（见 {ref}`sec:workflowsautomatization.compound_detailed.commands.closeFile`）。

**示例：**

```{literalinclude} ../../orca_working_input/ORCA_Test_0955.inp
:language: orca
```

(sec:workflowsautomatization.compound_detailed.commands.stringrelated.write2string)=
### Write2String

如果需要用某些变量构造字符串，*Compound* 提供 *Write2String* 命令。该
命令的语法与 *Write2File*（见 {ref}`sec:workflowsautomatization.compound_detailed.commands.stringrelated.write2file`）
命令相同，唯一的
例外是我们应提供文件中已声明变量的名称而不是文件。格式和所用变量的语法与 *Print* 命令相同（请
参阅 {ref}`sec:workflowsautomatization.compound_detailed.commands.stringrelated.print`。）

**语法（Syntax）：**

*Write2String(variable, format string, \[variables\]);*

*其中：*

*variable：* 是应已声明的变量名。

*format string* 和 *variables* 完全遵循 *Print* 命令的语法，更多
细节请参阅章节 {ref}`sec:workflowsautomatization.compound_detailed.commands.stringrelated.print`。

**示例：**

```{literalinclude} ../../orca_working_input/ORCA_Test_0955.inp
:language: orca
```
(sec:workflowsautomatization.compound_detailed.knownProperties)=
## 已知性质列表（List of known Properties）

所有可以从性质文件自动恢复的已知变量的名称和简要说明
见下表：

:::{raw} latex
\begingroup
\footnotesize
:::

:::{tabularcolumns} \Y{0.45}\Y{0.55}
:::

(tab:knownVariables)=
:::{flat-table} compound 块已知的变量及其简要说明
:header-rows: 1
:class: footnotesize
* - 关键词
  - 说明
* - `AUTOCI_REF_ENERGY`
  - AutoCI 参考能
* - `AUTOCI_CORR_ENERGY`
  - AutoCI 相关能
* - `AUTOCI_TOTAL_ENERGY`
  - AutoCI 总能量
* - === 能量 ===
  - 
* - `AUTOCI_NUCLEAR_GRADIENT`
  - AutoCI 能量核梯度
* - `AUTOCI_NUCLEAR_GRADIENT_NORM`
  - AutoCI 核梯度的范数
* - `AUTOCI_NUCLEAR_GRADIENT_ATOM_NUMBERS`
  - AutoCI 梯度中原子的原子序数
* - === 电性质（偶极矩） ===
  - 
* - `AUTOCI_DIPOLE_MAGNITUDE`
  - AutoCI 偶极矩大小
* - `AUTOCI_DIPOLE_ELEC_CONTRIB`
  - AutoCI 偶极矩的电子贡献
* - `AUTOCI_DIPOLE_NUC_CONTRIB`
  - AutoCI 偶极矩的核贡献
* - `AUTOCI_DIPOLE_TOTAL`
  - AutoCI 总偶极矩
* - `SCF_ENERGY`
  - SCF 能量
* - === 电性质（极化率） ===
  - 
* - `AUTOCI_POLAR_ISOTROPIC`
  - AutoCI 各向同性极化率
* - `AUTOCI_POLAR_RAW`
  - AutoCI 原始极化率张量
* - `AUTOCI_POLAR_DIAG_TENSOR`
  - AutoCI 对角化极化率张量
* - `AUTOCI_POLAR_ORIENTATION`
  - AutoCI 极化率取向（本征向量）
* - === 电性质（四极矩） ===
  - 
* - `AUTOCI_QUADRUPOLE_MOMENT_ISOTROPIC`
  - AutoCI 各向同性四极矩
* - `AUTOCI_QUADRUPOLE_MOMENT_DIAG_TENSOR`
  - AutoCI 对角化四极张量
* - `AUTOCI_QUADRUPOLE_MOMENT_ELEC_CONTRIB`
  - AutoCI 四极矩的电子贡献
* - `AUTOCI_QUADRUPOLE_MOMENT_NUC_CONTRIB`
  - AutoCI 四极矩的核贡献
* - `AUTOCI_QUADRUPOLE_MOMENT_TOTAL`
  - AutoCI 总四极矩
* - === 磁性质（D 张量） ===
  - 
* - `AUTOCI_D_TENSOR_EIGENVALUES`
  - AutoCI D 张量本征值
* - `AUTOCI_D_TENSOR_EIGENVECTORS`
  - AutoCI D 张量本征向量
* - `AUTOCI_D_TENSOR_RAW`
  - AutoCI 原始 D 张量
* - `AUTOCI_D_TENSOR_D`
  - AutoCI D 张量的 D 值
* - `AUTOCI_D_TENSOR_E`
  - AutoCI D 张量的 E 值
* - `AUTOCI_D_TENSOR_MULTIPLICITY`
  - AutoCI 用于 D 张量的自旋多重度
* - === 磁性质（G 张量） ===
  - 
* - `AUTOCI_G_TENSOR_RAW`
  - AutoCI 原始 G 张量
* - `AUTOCI_G_TENSOR_ELEC`
  - AutoCI G 张量的电子部分
* - `AUTOCI_G_TENSOR_TOT`
  - AutoCI 总 G 张量
* - `AUTOCI_G_TENSOR_ISO`
  - AutoCI 各向同性 g 值
* - `AUTOCI_G_TENSOR_ORIENTATION`
  - AutoCI G 张量取向（本征向量）
* - === 额外 SCF 性质 ===
  - 
* - `SCF_ENERGY`
  - SCF 能量
* - `VDW_CORRECTION`
  - van der Waals 校正

* - `SCF Electric properties`
  - 
* - `SCF_DIPOLE_MAGNITUDE`
  - SCF 偶极矩（Debye）
* - `SCF_DIPOLE_ELEC_CONTRIB`
  - SCF 偶极矩的电子贡献
* - `SCF_DIPOLE_NUC_CONTRIB`
  - SCF 偶极矩的核贡献
* - `SCF_DIPOLE_TOTAL`
  - SCF 总偶极矩
* - `SCF_QUADRUPOLE_ISOTROPIC`
  - SCF 各向同性四极矩
* - `SCF_QUADRUPOLE_DIAG_TENSOR`
  - SCF 对角化四极张量
* - `SCF_QUADRUPOLE_ELEC_CONTRIB`
  - SCF 四极矩的电子贡献
* - `SCF_QUADRUPOLE_NUC_CONTRIB`
  - SCF 四极矩的核贡献
* - `SCF_QUADRUPOLE_TOTAL`
  - SCF 总四极矩
* - `SCF_POLAR_ISOTROPIC`
  - SCF 各向同性极化率
* - `SCF_POLAR_RAW`
  - SCF 原始极化率张量
* - `SCF_POLAR_DIAG_TENSOR`
  - SCF 对角化极化率张量
* - === DBOC 能量校正 ===
  - 
* - `DBOC_ENERGY`
  - 对角 Born-Oppenheimer 校正（DBOC）能量
* - === DBOC 能量校正 ===
  - 
* - `DBOC_ENERGY`
  - 对角 Born-Oppenheimer 能量校正
* - === DFT ===
  - 
* - `DFT_NUM_OF_ALPHA_EL`
  - alpha 电子数目
* - `DFT_NUM_OF_BETA_EL`
  - beta 电子数目
* - `DFT_NUM_OF_TOTAL_EL`
  - 电子总数
* - `DFT_TOTAL_EN`
  - DFT 总能量
* - `DFT_EXCHANGE_EN`
  - DFT 交换能
* - `DFT_CORR_EN`
  - DFT 相关能
* - `DFT_XC_EN`
  - DFT 交换-相关能
* - `DFT_NON_LOC_EN`
  - DFT 非局域相关能
* - `DFT_EMBED_CORR`
  - DFT 嵌入校正
* - === gCP 校正 ===
  - 
* - `GCP_CORRECTION`
  - 几何 counterpoise（gCP）能量校正
* - === MP2 ===
  - 
* - `MP2_REF_ENERGY`
  - 参考 SCF 能量
* - `MP2_CORR_ENERGY`
  - MP2 相关能
* - `MP2_TOTAL_ENERGY`
  - 总能量（SCF + MP2）
* - === MP2 电性质 ===
  - 
* - `MP2_DIPOLE_MAGNITUDE`
  - MP2 偶极矩（Debye）
* - `MP2_DIPOLE_ELEC_CONTRIB`
  - MP2 偶极矩的电子贡献
* - `MP2_DIPOLE_NUC_CONTRIB`
  - MP2 偶极矩的核贡献
* - `MP2_DIPOLE_TOTAL`
  - MP2 总偶极矩
* - `MP2_QUADRUPOLE_ISOTROPIC`
  - MP2 各向同性四极矩
* - `MP2_QUADRUPOLE_DIAG_TENSOR`
  - MP2 对角化四极张量
* - `MP2_QUADRUPOLE_ELEC_CONTRIB`
  - MP2 四极矩的电子贡献
* - `MP2_QUADRUPOLE_NUC_CONTRIB`
  - MP2 四极矩的核贡献
* - `MP2_QUADRUPOLE_TOTAL`
  - MP2 总四极矩
* - `MP2_POLAR_ISOTROPIC`
  - MP2 各向同性极化率
* - `MP2_POLAR_RAW`
  - MP2 原始极化率张量
* - `MP2_POLAR_DIAG_TENSOR`
  - MP2 对角化极化率张量
* - === MDCI ===
  - 
* - `MDCI_REF_ENERGY`
  - 参考 SCF 能量
* - `MDCI_CORR_ENERGY`
  - 总相关能
* - `MDCI_TOTAL_ENERGY`
  - 总能量（SCF + 相关能）
* - `MDCI_ALPHA_ALPHA_CORR_ENERGY`
  - 来自 αα 电子对的相关能
* - `MDCI_BETA_BETA_CORR_ENERGY`
  - 来自 ββ 电子对的相关能
* - `MDCI_ALPHA_BETA_CORR_ENERGY`
  - 来自 αβ 电子对的相关能
* - `MDCI_DSINGLET_CORR_ENERGY`
  - 来自单重态（双激发，仅闭壳层）的相关能
* - `MDCI_DTRIPLET_CORR_ENERGY`
  - 来自三重态（双激发，仅闭壳层）的相关能
* - `MDCI_SSINGLET_CORR_ENERGY`
  - 来自单重态（单激发，仅闭壳层）的相关能
* - `MDCI_STRIPLET_CORR_ENERGY`
  - 来自三重态（单激发，仅闭壳层）的相关能
* - `MDCI_TRIPLES_ENERGY`
  - 微扰三重激发相关能
* - `MDCI_ALL_ELECTRONS`
  - 电子总数
* - `MDCI_CORR_ELECTRONS`
  - 相关电子数目
* - `MDCI_CORR_ALPHA_ELECTRONS`
  - 相关 α 电子数目
* - `MDCI_CORR_BETA_ELECTRONS`
  - 相关 β 电子数目
* - === MDCI 电性质 ===
  - 
* - `MDCI_DIPOLE_MAGNITUDE`
  - MDCI 偶极矩（Debye）
* - `MDCI_DIPOLE_ELEC_CONTRIB`
  - MDCI 偶极矩的电子贡献
* - `MDCI_DIPOLE_NUC_CONTRIB`
  - MDCI 偶极矩的核贡献
* - `MDCI_DIPOLE_TOTAL`
  - MDCI 总偶极矩
* - `MDCI_QUADRUPOLE_ISOTROPIC`
  - MDCI 各向同性四极矩
* - `MDCI_QUADRUPOLE_DIAG_TENSOR`
  - MDCI 四极矩对角化张量
* - `MDCI_QUADRUPOLE_ELEC_CONTRIB`
  - MDCI 四极矩的电子贡献
* - `MDCI_QUADRUPOLE_NUC_CONTRIB`
  - MDCI 四极矩的核贡献
* - `MDCI_QUADRUPOLE_TOTAL`
  - MDCI 总四极矩
* - `MDCI_POLAR_ISOTROPIC`
  - MDCI 各向同性极化率
* - `MDCI_POLAR_RAW`
  - MDCI 原始极化率张量
* - `MDCI_POLAR_DIAG_TENSOR`
  - MDCI 对角化极化率张量
* - === CASSCF / CASPT2 / DCDCAS ===
  - 
* - `CASSCF_NUM_OF_MULTS`
  - CASSCF 自旋多重度数目
* - `CASSCF_NUM_OF_IRREPS`
  - CASSCF 不可约表示数目
* - `CASSCF_FINAL_ENERGY`
  - 最终 CASSCF 能量
* - `PT2_NUM_OF_MULTS`
  - CASPT2 自旋多重度
* - `PT2_NUM_OF_IRREPS`
  - CASPT2 不可约表示数目
* - `PT2_FINAL_ENERGY`
  - CASPT2 能量
* - `DCDCAS_NUM_OF_MULTS`
  - DCDCAS 自旋多重度数目
* - `DCDCAS_NUM_OF_IRREPS`
  - DCDCAS 不可约表示数目
* - `DCDCAS_FINAL_ENERGY`
  - DCDCAS 能量
* - === 光谱（吸收与 CD） ===
  - 
* - `CASSCF_ABS_SPECTRUM`
  - CASSCF 吸收光谱
* - `CASSCF_ABS_SPECTRUM_INFO`
  - CASSCF 光谱激发信息
* - `CASSCF_ABS_SPECTRUM_NROOTS`
  - CASSCF 吸收中的根数
* - `CASSCF_CD_SPECTRUM`
  - CASSCF 圆二色光谱
* - `CASSCF_CD_SPECTRUM_INFO`
  - CASSCF CD 光谱中激发的信息
* - `CASSCF_CD_SPECTRUM_NROOTS`
  - CASSCF CD 中的根数
* - `CASPT2_ABS_SPECTRUM`
  - CASPT2 吸收光谱
* - `CASPT2_ABS_SPECTRUM_INFO`
  - CASPT2 光谱中激发的信息
* - `CASPT2_ABS_SPECTRUM_NROOTS`
  - CASPT2 吸收中的根数
* - `CASPT2_CD_SPECTRUM`
  - CASPT2 圆二色光谱
* - `CASPT2_CD_SPECTRUM_INFO`
  - CASPT2 CD 光谱中激发的信息
* - `CASPT2_CD_SPECTRUM_NROOTS`
  - CASPT2 CD 中的根数
* - `CAS_CUSTOM_ABS_SPECTRUM`
  - 自定义 CASSCF 吸收光谱
* - `CAS_CUSTOM_ABS_SPECTRUM_INFO`
  - 自定义 CASSCF 吸收光谱的激发信息
* - `CAS_CUSTOM_ABS_SPECTRUM_NROOTS`
  - 自定义吸收光谱中的根数
* - `CAS_CUSTOM_CD_SPECTRUM`
  - 自定义 CASSCF CD 光谱
* - `CAS_CUSTOM_CD_SPECTRUM_INFO`
  - 自定义 CD 光谱激发的信息
* - `CAS_CUSTOM_CD_SPECTRUM_NROOTS`
  - 自定义 CD 光谱中的根数
* - `DCDCAS_ABS_SPECTRUM`
  - DCDCAS 吸收光谱
* - `DCDCAS_ABS_SPECTRUM_INFO`
  - DCDCAS 吸收光谱的激发信息
* - `DCDCAS_ABS_SPECTRUM_NROOTS`
  - DCDCAS 吸收中的根数
* - === 零场分裂（ZFS） ===
  - 
* - `CASSCF_DTENSOR_EIGENVALUES`
  - CASSCF D 张量本征值
* - `CASSCF_DTENSOR_RAW_EIGENVECTORS`
  - CASSCF D 张量的原始本征向量
* - `CASSCF_DTENSOR_D`
  - CASSCF ZFS 的 D 值
* - `CASSCF_DTENSOR_E`
  - CASSCF ZFS 的 E 值
* - `CASSCF_DTENSOR_MULTIPLICITY`
  - CASSCF 的自旋多重度
* - `CASPT2_DTENSOR_EIGENVALUES`
  - CASPT2 D 张量本征值
* - `CASPT2_DTENSOR_RAW_EIGENVECTORS`
  - CASPT2 D 张量的原始本征向量
* - `CASPT2_DTENSOR_D`
  - CASPT2 ZFS 的 D 值
* - `CASPT2_DTENSOR_E`
  - CASPT2 ZFS 的 E 值
* - `CASPT2_DTENSOR_MULTIPLICITY`
  - CASPT2 的自旋多重度
* - `CAS_CUSTOM_DTENSOR_EIGENVALUES`
  - 自定义 CASSCF D 张量本征值
* - `CAS_CUSTOM_DTENSOR_RAW_EIGENVECTORS`
  - 自定义 CASSCF 原始 D 张量本征向量
* - `CAS_CUSTOM_DTENSOR_D`
  - 自定义 CASSCF ZFS 的 D 值
* - `CAS_CUSTOM_DTENSOR_E`
  - 自定义 CASSCF ZFS 的 E 值
* - `CAS_CUSTOM_DTENSOR_MULTIPLICITY`
  - 自定义 CASSCF 的自旋多重度
* - === CIPSI ===
  - 
* - `CIPSI_SPIN_MULTIPLICITY`
  - CIPSI 自旋多重度
* - `CIPSI_NUM_OF_ROOTS`
  - CIPSI 中的根数
* - `CIPSI_FINAL_ENERGY`
  - 最终 CIPSI 能量
* - `CIPSI_ENERGIES`
  - 所有 CIPSI 能量
* - === CIS ===
  - 
* - `CIS_FINAL_ENERGY`
  - 来自 CIS 的最终总能量
* - `CIS_ESCF`
  - SCF 能量
* - `CIS_E0`
  - 基态能量
* - `CIS_ENERGIES`
  - 单重态激发能
* - `CIS_ENERGIESP1`
  - 三重态激发能
* - `CIS_MODE`
  - CIS 计算模式
* - `CIS_NUM_OF_ROOTS`
  - 根数
* - `CIS_ROOT`
  - 待优化的态
* - `CIS_ABS_SPECTRUM_NROOTS`
  - 吸收光谱的根数
* - `CIS_ABS_SPECTRUM`
  - CIS 吸收光谱
* - `CIS_ABS_SPECTRUM_VELOCITY`
  - CIS 吸收光谱（速度表示）
* - `CIS_ABS_SOC_SPECTRUM_NROOTS`
  - 含 SOC 的根数（吸收）
* - `CIS_ABS_SOC_SPECTRUM`
  - 含 SOC 的 CIS 吸收光谱
* - `CIS_CD_SPECTRUM_NROOTS`
  - CD 光谱中的根数
* - `CIS_CD_SPECTRUM`
  - CIS 圆二色光谱
* - `CIS_CD_SOC_SPECTRUM_NROOTS`
  - 含 SOC 的 CD 中的根数
* - `CIS_CD_SOC_SPECTRUM`
  - 含 SOC 的 CIS CD 光谱
* - === ROCIS ===
  - 
* - `ROCIS_STATE`
  - ROCIS 态
* - `ROCIS_REF_ENERGY`
  - ROCIS 参考能
* - `ROCIS_CORR_ENERGY`
  - ROCIS 相关能
* - `ROCIS_TOTAL_ENERGY`
  - 总 ROCIS 能量
* - `ROCIS_ABS_SPECTRUM_NROOTS`
  - ROCIS 吸收中的根数
* - `ROCIS_ABS_SPECTRUM`
  - ROCIS 吸收光谱
* - `ROCIS_ABS_SOC_SPECTRUM_NROOTS`
  - 含 SOC 的根数（吸收）
* - `ROCIS_ABS_SOC_SPECTRUM`
  - 含 SOC 的 ROCIS 吸收光谱
* - `ROCIS_CD_SPECTRUM_NROOTS`
  - ROCIS CD 中的根数
* - `ROCIS_CD_SPECTRUM`
  - ROCIS 圆二色光谱
* - `ROCIS_CD_SOC_SPECTRUM_NROOTS`
  - 含 SOC 的 ROCIS CD 中的根数
* - `ROCIS_CD_SOC_SPECTRUM`
  - 含 SOC 的 ROCIS CD 光谱
* - === MRCI ===
  - 
* - `MRCI_ABS_SPECTRUM`
  - MRCI 吸收光谱
* - `MRCI_ABS_SPECTRUM_INFO`
  - MRCI 吸收光谱信息
* - `MRCI_ABS_SPECTRUM_NROOTS`
  - MRCI 吸收中的根数
* - `MRCI_CD_SPECTRUM`
  - MRCI CD 光谱
* - `MRCI_CD_SPECTRUM_INFO`
  - MRCI CD 光谱信息
* - `MRCI_CD_SPECTRUM_NROOTS`
  - MRCI CD 中的根数
* - `MRCI_DIPOLE_MOMENTS`
  - MRCI 偶极矩
* - `MRCI_DIPOLE_MOMENTS_INFO`
  - MRCI 偶极矩信息
* - `MRCI_DTENSOR_EIGENVECTORS`
  - MRCI D 张量本征向量
* - `MRCI_DTENSOR_EIGENVALUES`
  - MRCI D 张量本征值
* - `MRCI_DTENSOR_RAW_EIGENVECTORS`
  - MRCI D 张量的原始本征向量
* - `MRCI_DTENSOR_D`
  - MRCI ZFS 的 D 值
* - `MRCI_DTENSOR_E`
  - MRCI ZFS 的 E 值
* - `MRCI_DTENSOR_MULTIPLICITY`
  - MRCI 自旋多重度
* - === 外推 ===
  - 
* - `EXTRAP_SCF_ENERGIES`
  - 各种基组的 SCF 能量
* - `EXTRAP_CBS_SCF`
  - 外推的 SCF 能量（CBS 极限）
* - `EXTRAP_CORR_ENERGIES`
  - 不同基组的相关能
* - `EXTRAP_CBS_CORR`
  - 外推的相关能
* - `EXTRAP_CBS_TOTAL`
  - 外推的总能量
* - `EXTRAP_CCSDT_X`
  - 能量的 (T) 贡献
* - `EXTRAP_NUM_OF_ENERGIES`
  - 外推中使用的基组数
* - === 热化学 ===
  - 
* - `THERMO_TEMPERATURE`
  - 温度（°K）
* - `THERMO_PRESSURE`
  - 压力（atm）
* - `THERMO_TOTAL_MASS`
  - 总分子质量（AMU）
* - `THERMO_SPIN_DEGENERACY`
  - 电子简并度
* - `THERMO_ELEC_ENERGY`
  - 电子能量（Eh）
* - `THERMO_TRANS_ENERGY`
  - 平动能（Eh）
* - `THERMO_ROT_ENERGY`
  - 转动能（Eh）
* - `THERMO_VIB_ENERGY`
  - 振动能（Eh）
* - `THERMO_NUM_OF_FREQS`
  - 振动频率数目
* - `THERMO_FREQS`
  - 振动频率
* - `THERMO_ZPE`
  - 零点能（Eh）
* - `THERMO_INNER_ENERGY_U`
  - 内能 U（Eh）
* - `THERMO_ENTHALPY_H`
  - 焓 H（Eh）
* - `THERMO_ELEC_ENTROPY`
  - （电子熵）× T（Eh）
* - `THERMO_ROR_ENTROPY`
  - （转动熵）× T（Eh）
* - `THERMO_VIB_ENTROPY`
  - （振动熵）× T（Eh）
* - `THERMO_TRANS_ENTROPY`
  - （平动熵）× T（Eh）
* - `THERMO_ENTROPY_S`
  - 总熵 × T（Eh）
* - `THERMO_FREE_ENERGY_G`
  - 自由能 G（Eh）
* - === EPR-NMR 自旋-自旋耦合 ===
  - 
* - `EPRNMR_SSC_NUM_OF_NUC_PAIRS`
  - 用于 SSC 计算的核对
* - `EPRNMR_SSC_NUM_OF_NUC_PAIRS_DSO`
  - DSO 项的核对
* - `EPRNMR_SSC_NUM_OF_NUC_PAIRS_PSO`
  - PSO 项的核对
* - `EPRNMR_SSC_NUM_OF_NUC_PAIRS_FC`
  - Fermi 接触（FC）项的核对
* - `EPRNMR_SSC_NUM_OF_NUC_PAIRS_SD`
  - 自旋偶极（SD）项的核对
* - `EPRNMR_SSC_NUM_OF_NUC_PAIRS_SD_FC`
  - SD/FC 混合项的核对
* - `EPRNMR_SSC_NUM_OF_NUCLEI_PSO`
  - 涉及 PSO 微扰的核
* - `EPRNMR_SSC_NUM_OF_NUCLEI_FC`
  - 涉及 SD/FC 微扰的核
* - === SOC 能量校正 ===
  - 
* - `SOC_NUCLEAR_ENERGY`
  - 核能量
* - `SOC_2C_ENERGY`
  - 二分量总能量
* - `SOC_NON_SOC_ENERGY`
  - 不含 SOC 的总能量
* - `SOC_ENERGY_CORRECTION`
  - SOC 能量校正
* - === 溶剂化 ===
  - 
* - `SOLVATION_EPSILON`
  - 介电常数
* - `SOLVATION_REFRAC`
  - 折射率
* - `SOLVATION_RSOLV`
  - 溶剂探针半径
* - `SOLVATION_SURFACE_TYPE`
  - 所用空腔表面的类型
* - `SOLVATION_CPCM_DIEL_ENERGY`
  - 含 CPCM 介电校正的总能量
* - `SOLVATION_NPOINTS`
  - 高斯表面的点数
* - `SOLVATION_SURFACE_AREA`
  - 总表面积
* - === 一般作业信息 ===
  - 
* - `JOB_INFO_MULT`
  - 自旋多重度
* - `JOB_INFO_CHARGE`
  - 分子电荷
* - `JOB_INFO_NUM_OF_ATOMS`
  - 原子数目
* - `JOB_INFO_NUM_OF_EL`
  - 电子数目
* - `JOB_INFO_NUM_OF_FC_EL`
  - 冻结核电子数目
* - `JOB_INFO_NUM_OF_CORR_ELC`
  - 相关电子数目
* - `JOB_INFO_NUM_OF_BASIS_FUNCS`
  - 基函数数目
* - `JOB_INFO_NUM_OF_AUXC_BASIS_FUNCS`
  - 辅助 C 基函数数目
* - `JOB_INFO_NUM_OF_AUXJK_BASIS_FUNCS`
  - 辅助 JK 基函数数目
* - `JOB_INFO_NUM_OF_AUX_CABS_BASIS_FUNCS`
  - 辅助 JK CABS 基函数数目
* - `JOB_INFO_TOTAL_EN`
  - 最终总能量
* - === HESSIAN ===
  - 
* - `HESSIAN_MODES`
  - Hessian 矩阵或振动模式
* - === 数学函数 ===
  - 
* - `ABS`
  - 绝对值
* - `COS`
  - 余弦
* - `SIN`
  - 正弦
* - `TAN`
  - 正切
* - `ACOS`
  - 反余弦
* - `ASIN`
  - 反正弦
* - `ATAN`
  - 反正切
* - `COSH`
  - 双曲余弦
* - `SINH`
  - 双曲正弦
* - `TANH`
  - 双曲正切
* - `EXP`
  - 指数
* - `LOG`
  - 常用对数（以 10 为底）
* - `LN`
  - 自然对数
* - `SQRT`
  - 平方根
* - `ROUND`
  - 向下取整到最近的整数
:::
:::{raw} latex
\endgroup
:::



