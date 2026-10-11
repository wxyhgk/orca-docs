```{index} Property File
```

(sec:property_file.detailed)=
# 性质文件（Property File）

ORCA 在计算过程中生成的文件之一是*性质文件（property file）*。该文件名为 `basename.property.txt`，其中 `basename` 是输入文件的基名。

性质文件在 ORCA 中主要有两种用途。第一种用途是作为 *Compound* 脚本语言的基础。*Compound* 通过性质文件读取其所有与性质相关的信息，而不是通过解析 ORCA 输出。性质文件的第二种用途是让其他程序或潜在的 GUI 更容易与 ORCA 创建接口。

与常规 ORCA 输出相比，性质文件的优点是其语法定义良好，因此更容易解析。
它也可以转换为 JSON 格式，如下所示。

对于大多数计算，写入性质文件默认启用。
可以通过 `!NoPropFile` 禁用，或在 `%output` 块中切换开/关：

``` orca
%output
  PropFile false  # default: true
end
```

:::{admonition} 小心
:class: caution
由于整个文件在每次单点计算中会被多次读取和重写，
对含数千个原子的体系进行优化时，每个优化周期可能产生几毫秒的堆积 I/O 开销
（即几百步之后每个周期约几秒）。
因此，建议在此类计算中禁用性质文件，
在简单输入中选择 `GOAT`、`MD-L-Opt`、`MM` 或 `GFN-FF` 时默认已禁用。
:::

(sec:property_file.txtFormat.detailed)=
## TXT 格式（TXT Format）

任何 ORCA 计算之后都会创建扩展名为 `.property.txt` 的性质文件。该文件是文本文件，可以用任何可用的文本编辑器读取和编辑。下面我们分析该文件的语法。

文件总是以下面三行开始：

```orca
*************************************************
******************* ORCA 6.1.x ******************
*************************************************
```

显然，其中 ORCA 的版本号会变化
（它也存储在 `Calculation_Status -> version` 中）。

然后，文件由一系列性质组成。每个性质以符号 `$` 加性质名开始，以符号 `$` 加 `End` 结束。

例如：
```orca
$SCF_Nuc_Gradient
   &GeometryIndex 1
   &NAtoms [&Type "Integer"] 2
   &gradNorm [&Type "Double"]       7.6940943132805237e-02
   &grad [&Type "ArrayOfDoubles", &Dim (6,1)]
                                                         0

0                                      6.7009699964043727e-10
1                                     -1.3755030800675890e-10
2                                      5.4405462640094826e-02
3                                     -6.7009699282161039e-10
4                                      1.3755031156980307e-10
5                                     -5.4405462640095381e-02
   &Method [&Type "String"] "SCF"
   &Level [&Type "String"] "Relaxed density"
   &Mult [&Type "Integer"] 1
   &State [&Type "Integer"] 0
   &Irrep [&Type "Integer"] 0
$End
```

每个性质由*分量（components）*组成。每个分量以符号 `&` 开始，没有结束符号。

例如：

```orca
   &gradNorm [&Type "Double"]       7.6940943132805237e-02
```

每个性质中的第一个分量是 `GeometryIndex`，
它表示当前性质所属的几何结构。
例如：

```orca
&GeometryIndex 1
```

请注意，几何索引从 1 开始。

其余分量具有以下语法：
- 首先是分量起始符号 `&`。
- 接着是分量名称。
- 然后是一个方括号，其中包含关于该分量的各种括号信息。有关括号信息语法的细节，请查看 {ref}`sec:property_file.txtFormat.bracketInfo.detailed`。

括号之后有不同的选项。

如果类型是 `String`，则期望一个以引号开始的字符串。
例如：

```orca
&Method [&Type "String"] "SCF"
```

如果类型是 `Double` 或 `Integer`，则期望相应类型的数值。
例如：

```orca
&NAtoms [&Type "Integer"] 2 "Number of atoms"
```

如上例所示，在与分量名同一行的数值之后可以可选地出现引号括起的分量描述或注释。
请注意，对于 `Array` 分量，注释实际上出现在数据*之前*。

最后，如果类型是某种 `Array`，则在可选注释之后，
数组从下一行开始写出。
数组按最多 8 个空白符分隔的列写成块。
每个块以一行列索引（从 0 开始）开始。
块中的第二行保留，但当前被忽略。
接下来的各行以行索引开始，后接相应行/列的数据。
例如：

```orca
   &dipoleTotal [&Type "ArrayOfDoubles", &Dim (3,1)] "Total"
                                                         0

0                                     -5.1716015643064861e-01
1                                      5.1774970936823518e-02
2                                      7.8324050140722279e-01
```

请注意，`Complex` 标量打印为两个连续的值，分别代表实部和虚部（位于可选注释之前），
而对于 `ArrayOfComplex`，则先打印整个数组的实部，
再打印虚部。

(sec:property_file.txtFormat.bracketInfo.detailed)=
### 括号信息（Bracket Information）

括号信息是用 ',' 分隔的条目列表。
第一个也是最重要的括号条目是 `Type`，
它可以是以下之一：
- `Double`
- `Integer`
- `Boolean`
- `Complex`
- `String`
- `ArrayOfDoubles`
- `ArrayOfIntegers`
- `ArrayOfBooleans`
- `ArrayOfComplex`
- `Coordinates`
%-  "MixedMatrix"  % NOT IMPLEMENTED

例如：

```orca
&NAtoms [&Type "Integer"] 2
```

然后，在 `Type` 是某种数组的情况下，括号必须使用 `Dim` 条目包含数组的维度。请注意，所有数组都是二维的！
例如：

```orca
&ATNO [&Type "ArrayOfIntegers", &Dim (2,1)]
```

如果数值不是原子单位，也可以可选地给出 `Units`。例如：

```orca
&dipoleMagnitude [&Type "Double", &Units "Debye"]       9.4000050960598935e-01
```

(sec:property_file.jsonFormat.detailed)=
## JSON 格式（JSON Format）

性质文件也可以以 JSON 格式生成。在内部，这是通过将 `txt` 格式转换为 JSON 格式来实现的。有两种创建 JSON 性质文件的方式。

第一种方式是通过常规 ORCA 输入使用 `JSONPropFile` 关键词。

```orca
%Output
  JSONPropFile True
End
```

这将创建 `basename.property.txt`，此外还会创建 `basename.property.json` 文件。

第二种方式是通过 [`orca_2json` 命令](sec:orca_2json.availableinformation.propertyFile)。
为此，首先需要运行常规 ORCA 输入，它会创建 `basename.property.txt` 文件，
然后使用以下命令将其转换为 `basename.property.json`：

```orca
orca_2json basename -property
```

该文件结构如下：
```orca
{
  "<GlobalPropertyName>": {
    "<ComponentName>": <value>,
    <More components>
  },
  <More global properties>
  "Geometries": [
    {
      "Geometry": {
        "Coordinates": {
            "Cartesians": [
                [
                    "<Symbol>",
                    <X>,
                    <Y>,
                    <Z>
                ],
                <More atoms>
            ],
            "Type": "Cartesians",
            "Units": "a.u."
        },
        "NAtoms": <value>,
        <More components>
      },
      "<PropertyName>": {
        "<ComponentName>": <value>,
        <More components>
      },
      <More properties for this geometry>
    },
    <More geometries>
  ]
}
```

“全局”性质（即与几何无关的性质）是：
`Calculation_Status`、`Calculation_Info` 和 `Calculation_Timings`。

大多数分量数据类型都直接转换为相应的 JSON 类型。
所有 `Array` 分量都使用嵌套列表以二维形式存储（即使某一维长度为 1）。`Complex` 和 `ArrayOfComplex` 值以分开的实部和虚部存储：
```orca
"ComplexComponentName": {
  "re": <real part>,
  "im": <imaginary part>
},
"ComplexArrayComponentName": {
  "re": [
      [<r11>, <r12>, <...>],
      [<r21>, <r22>, <...>],
      <...>
    ],
  "im": [
      [<i11>, <i12>, <...>],
      [<i21>, <i22>, <...>],
      <...>
    ]
}
```


(sec:property_file.list)=
## 可用性质列表（List of Available Properties）

```{include} property_file_list.md
```
