

<a id="sec:orca_2json"></a>
# orca_2json

该实用程序支持将外部 ORCA 数据（如几何结构、轨道和基组）以及内部 ORCA 数据（如单电子和双电子积分）与其他程序交换。

<a id="sec:orca_2json.invocation"></a>
## 调用与配置（Invocation and configuration）

<a id="sec:orca_2json.invocation.manual_export"></a>
### ORCA 数据的手动导出及其他选项（Manual export of ORCA data and other options）

程序读取存储在 `.gbw` 文件或其他等价文件（如 `.uno`、`.mp2nat`、
`.qro` 等）中的几何结构、基组、MO 等信息，并计算积分以将其导出为某一种 JSON 标准输出格式。对于密度信息，`.densities` 文件也必须可用。程序以独立方式通过命令行调用。

**语法（Syntax）：**
```orca
orca_2json BaseName.gbw -options
or
orca_2json BaseName.mp2nat -options
or
orca_2json BaseName.uno -options
```

下列 ASCII 和二进制 JSON 格式可作为命令行选项使用。可以指定多个格式选项。

```orca
  -json             Write ASCII JSON file (default)
  -bson             Write binary JSON file
  -ubjson           Write universal binary JSON specification file
  -msgpack          Write MessagePack file
```

此外还有两个可用选项。第一个用于将 basename.property.txt 文件转换为对应的 JSON 格式文件（见 [availableinformation.propertyFile](#sec:orca_2json.availableinformation.propertyFile)）。

```orca
   -property        Translate a *.txt property file to a *.json one
```

最后，orca_2json 能够从 JSON 文件创建 `.gbw` 文件。为此需要使用 `-gbw` 选项（见 [orca_2json.importData](#sec:orca_2json.importData)）。

```orca
   -gbw        Create a GBW file from a JSON one
```

<a id="sec:orca_2json.exportData.input"></a>
### 从 ORCA 作业自动导出（Automatic export from ORCA job）
也可以在 ORCA 作业结束时自动对 `.gbw` 文件运行 `orca_2json`，使用输入：

```orca
%output
  JSONGBWFile true
end
```
这将简单地运行 `orca_2json BaseName.gbw`，不带附加选项，并尊重任何适用的配置文件（如果存在）（见下文）。

<a id="sec:orca_2json.availableinformation.propertyFile"></a>
### 将性质文件导出为 JSON（Exporting the Property File to JSON）

除了我们将看到的 orca_2json 能创建的所有信息外，它还可以将 ORCA 的性质文件（basename.property.txt）转换为 JSON 文件。该选项可以访问性质文件中存储的所有性质。（关于性质文件的更多信息见 [property_file.detailed](property_file.md#sec:property_file.detailed)）。

**语法**为：

```orca
orca_2json basename -property
```

*其中*

*basename* 是性质文件的名称，**不带**扩展名 *property.txt*。

**示例**

如果我们使用下列 ORCA 输入（名为 test.inp）：

```orca
orca_2json BaseName.gbw -options
or
orca_2json BaseName.mp2nat -options
or
orca_2json BaseName.uno -options
```

ORCA 将在磁盘上创建并存储名为 *"test.property.txt"* 的文件。该文件的开头如下所示：

```orca
  -json             Write ASCII JSON file (default)
  -bson             Write binary JSON file
  -ubjson           Write universal binary JSON specification file
  -msgpack          Write MessagePack file
```

然后按如下方式运行 *orca_2json*：

```orca
orca_2json test -property
```

ORCA 将在磁盘上创建一个名为 *"test.property.json"* 的新文件。
该文件的相应部分如下所示：

```json
   -property        Translate a *.txt property file to a *.json one
```

!!! note "注意"
    `property.json` 结构自 ORCA 6.0 版以来有所变化，某些性质分量也如此。
    将 6.0 版的 `property.txt` 文件转换为当前 JSON 格式是部分可行的，但某些数据可能丢失（会有警告）。

<a id="sec:orca_2json.importData"></a>
### 将 JSON 数据导入 ORCA（Importing JSON data into ORCA）

存储在 orca_2json 所写的 JSON 格式中的某些信息（如几何结构、基组和分子轨道）可用于创建新的 `.gbw` 文件，以便在 ORCA 输入中指定为轨道文件。程序以独立方式通过命令行调用。

```orca
orca_2json BaseName.json -gbw
```

为了创建可用的 `.gbw` 文件，至少必须提供下列信息：

|              |     |                   |
|:-------------|:---:|:------------------|
| 每个原子     | \-  | Basis             |
|              | \-  | Coords            |
|              | \-  | ElementNumber     |
|              | \-  | NuclearCharge     |
| 每个分子     | \-  | Charge            |
|              | \-  | CoordinateUnits   |
|              | \-  | HFTyp             |
|              | \-  | Multiplicity      |
|              | \-  | MolecularOrbitals |

**注意**

请记住 *MolecularOrbitals* 是 2 个不同分量的复合体，即 *"EnergyUnit"* 和 *"MOs"*。然后 *"MOs"* 包含 *"MOCoefficients"*、*"Occupancy"*、*"OrbitalEnergy"*、"OrbitalSymLabel"* 和 "OrbitalSymmetry"*。

**示例**

下列文件（我们称之为 *filename.json*）是使用 STO-3G 基组的 H$_2$ 分子的 JSON 文件。

```json
   -gbw        Create a GBW file from a JSON one
```

然后运行命令

```orca
orca_2json filename.json -gbw
```

应当创建一个 ORCA 可以读取的 `.gbw` 文件。

<a id="sec:orca_2json.configurationFiles"></a>
### 配置文件（Configuration file）

存储在 JSON 文件中的数据可以更个性化地配置。
原子信息、几何结构和电荷等信息总是写入输出文件（见 [availableinformation.basic](#sec:orca_2json.availableinformation.basic)）。
其他数据可以通过 JSON 格式配置文件中的关键词请求，该配置文件可以针对每个 ORCA
输出文件或目录中的所有文件。没有这些配置文件时，**所有**可用数据都会被存储，密度和积分除外。由于数据量巨大，这些只有在配置文件中显式请求时才可用。

您可以指定依赖于 basename 的配置文件

```orca
BaseName.json.conf
```

或用于目录中所有请求的全局文件。

```orca
orca.json.conf
```

配置文件中的大多数关键词可以用 true 或 false 激活或停用，但某些关键词（如密度或输出格式）有更多选项，需要一个值列表。如果某个选项没有被特别选择，则被省略。

**配置文件的结构**：

```orca
{
	"keyword": true/false,
	...
	"keyword": true/false,
	"keyword": ["option",...."option"]
	...
}
```

**示例**
```orca
%output
  JSONGBWFile true
end
```
在工作目录中使用上述配置文件时，*orca_2json* 将不导出分子系数和基组信息。

**示例**

下面是一个包含大多数可用关键词的配置文件示例，其中
除基组信息和指定的积分外一切都被禁用，密度文件中存储的所有
密度都被请求，输出格式
应为 ASCII JSON 和二进制 JSON。

```orca
{
	"MOCoefficients": false,
	"Basisset": true,
	"1elPropertyIntegrals": ["dipole", "quadrupole", "velocity", "printLinMom", "angular_momentum", "higherMoment", "soc"],
	"1elPropertyRelIntegrals": ["dipole", "quadrupole", "angular_momentum", "soc"],
	"1elIntegrals": ["H", "S", "T", "V", "HMO"],
	"1elIntegralsRel": ["H", "S", "T", "V", "HMO"],
        "FockMatrix": ["F", "J", "K", "VXC", "Vsol"],
	"Vaux": false,
	"AuxBasisType": "AuxC",
	"FullTrafo": false,
	"OrbWin": [0,0,0,0,0,0,0,0],
	"2elIntegrals": [ "MO_IJKL", "RI_IAV", "RI_IJKL"],
	"2elNonRedIntegrals": false,
	"2elNonRedRIIntegrals": false,
	"MullikenCharge": false,
	"LoewdinCharge": false,
	"Densities": ["all"],   <--- here you specify the names like "scfp" or "scfr" or all
	"JSONFormats": ["json", "bson"]
}
```

<a id="sec:orca_2json.availableinformation.jsonformat"></a>
#### JSON 格式（JSON Format）

所创建的 JSON 格式也可以在配置文件中通过 *JSONFormats* 变量定义。

|                 |     |                                               |
|:----------------|:---:|:----------------------------------------------|
| JSONFormats     | \-  | JSON 输出格式                                 |

可用的 JSON 格式为：

|         |     |                              |
|:--------|:---:|:-----------------------------|
| json    | \-  | ASCII JSON 格式              |
| bson    | \-  | 二进制 JSON 格式             |
| ubjson  | \-  | 通用二进制 JSON 格式         |
| msgpck  | \-  | MessagePack 格式             |

**示例**
```json
orca_2json basename -property
```
<a id="sec:orca_2json.availableproperties"></a>
## 可用信息（Available information）

<a id="sec:orca_2json.availableinformation.basic"></a>
### 基本信息（Basic Information）
一些基本信息将始终写入 JSON 文件

|              |     |                 |
|:-------------|:---:|:----------------|
| 每个原子     | \-  | Coords          |
|              | \-  | ElementLabel    |
|              | \-  | ElementNumber   |
|              | \-  | Idx             |
|              | \-  | NuclearCharge   |
| 每个分子     | \-  | BaseName        |
|              | \-  | Charge          |
|              | \-  | CoordinateUnits |
|              | \-  | HFTyp           |
|              | \-  | Multiplicity    |
|              | \-  | PointGroup      |

例如使用下列配置文件，其中我们把所有内容都设为 false：
```json
!HF
*xyz 0 1
  H 0.0 0.0 0.0
  H 0.0 0.0 0.8
*
```
 仍会生成一个 json 文件，对于 H$_2$ 分子的情况应如下所示：
 ```json
*************************************************
******************* ORCA 6.0.1 ******************
*************************************************
$Calculation_Status
   &GeometryIndex 1
   &version [&Type "String"] "6.0.1"
   &progName [&Type "String"] "LeanSCF"
   &Status [&Type "String"] "NORMAL TERMINATION"
$End
$Geometry
   &GeometryIndex 1
   &NAtoms [&Type "Integer"] 2
   &NCorelessECP [&Type "Integer"] 0
   &NGhostAtoms [&Type "Integer"] 0
   &CartesianCoordinates [&Type "Coordinates", &Dim(2,4), &Units "Bohr"]
              H      0.000000000000    0.000000000000    0.000000000000
              H      0.000000000000    0.000000000000    1.511780907137
$End
$SCF_Energy
   &GeometryIndex 1
   &totalEnergy [&Type "Double"]      -1.1271129220233282e+00
$End
```

<a id="sec:orca_2json.availableinformation.densities"></a>
### 密度（Densities）

*orca_2json* 还可以将计算得到的密度以 json 格式导出。

|                 |     |                                               |
|:----------------|:---:|:----------------------------------------------|
| Densities       | \-  | .densities 文件中可用的密度                   |

#### 2RDM

从 ORCA 6.1.0 起，可以将 AutoCI 模块计算的 MO 基下的 2RDM 导出到 JSON。
参见 [AutoCI 关键词表](tab:modelchemistries.autoci.keywords.block) 了解可用选项。
2RDM 不存储在 `.densities` 文件中，而是在其自己的 `.RDM2` 文件中。下列
2RDM 可用
- `RDM2` (RHF, $\Gamma_{qs}^{pr}$)
- `RDM2_aa` (UHF, $\Gamma_{q_\alpha s_\alpha}^{p_\alpha r_\alpha}$)
- `RDM2_ab` (UHF, $\Gamma_{q_\alpha s_\beta}^{p_\alpha r_\beta}$)
- `RDM2_bb` (UHF, $\Gamma_{q_\beta s_\beta}^{p_\beta r_\beta}$)

考虑一般 CI 2RDM：

$$
\Gamma_{qs}^{pr} = \langle \Psi | E_{pq} E_{rs} | \Psi \rangle.
$$

对于每个可用的 `p` 和 `q` 组合，JSON 中都会有一个 `r` x `s` 矩阵。`p`、`q`、`r`、`s`
的取值范围从 `0` 到基函数数目。例如，在一个虚构的情形中只有
2 个基函数且 2RDM 的所有元素都设为 0，将产生如下 JSON。
```json
{
    "Densities": {
        "RDM2": {
            "0,0": [[0.0, 0.0], [0.0, 0.0]] // p=0, q=0
            "0,1": [[0.0, 0.0], [0.0, 0.0]] // p=0, q=1
            "1,0": [[0.0, 0.0], [0.0, 0.0]] // p=1, q=0
            "1,1": [[0.0, 0.0], [0.0, 0.0]] // p=1, q=1
        }
    }
}
```
请注意，弛豫 2RDM 已对称化，具有下列置换对称性

$$
\Gamma_{qs}^{pr} = \Gamma_{ps}^{qr} = \Gamma_{qr}^{ps} = \Gamma_{pr}^{qs} = \Gamma_{sq}^{rp} = \Gamma_{rq}^{sp} = \Gamma_{sp}^{rq} = \Gamma_{rp}^{sq}.
$$

#### 语法（Syntax）
*"Densities" : [密度列表]*

其中 *密度列表* 应为包含所期望密度的字符串列表。

**注意** 默认情况下，由于密度可能很大，不会导出到 json 文件。

**注意** 空括号语法（*"Densities" : []*）会导致程序崩溃。

**注意** 有字符串 "All" 可用，此时程序将导出所有可用密度。

<a id="sec:orca_2json.availableinformation.electronintegrals"></a>
### 电子积分（Electron Integrals）

可用电子积分的列表见下表。

|                         |     |                                               |
|:------------------------|:---:|:----------------------------------------------|
| 1elIntegrals            | \-  | 单电子积分                                    |
| 1elPropertyIntegrals    | \-  | 单电子性质积分                                |
| 1elIntegralsRel         | \-  | 相对论单电子积分                              |
| 1elPropertyRelIntegrals | \-  | 相对论单电子性质积分                          |
| 2elIntegrals            | \-  | 双电子积分                                    |
| 2elNonRedIntegrals      | \-  | 非冗余双电子积分                              |
| 2elNonRedRIIntegrals    | \-  | 非冗余双电子 RI 积分                          |
| FockMatrix              | \-  | Fock 矩阵的双电子贡献                         |

<a id="sec:orca_2json.availableinformation.electronintegrals.1el"></a>
#### 单电子积分（1-electron integrals）

对于单电子积分我们使用下列记号：
|     |     |                                 |
|:----|:---:|:--------------------------------|
| H   | \-  | 单电子矩阵                      |
| HMO | \-  | MO 基下的单电子矩阵            |
| S   | \-  | 重叠矩阵                        |
| T   | \-  | 动能矩阵                        |
| V   | \-  | 核吸引矩阵                      |

**示例**
```json
orca_2json test -property
```

将生成一个只打印 H 矩阵和重叠矩阵的 json 文件（除基本信息外）。请注意，对于单电子相对论积分有单独的变量（见 [electronintegrals.1elrel](#sec:orca_2json.availableinformation.electronintegrals.1elrel)）。

<a id="sec:orca_2json.availableinformation.electronintegrals.1elproperty"></a>
#### 单电子性质积分（1-electron property integrals）
还可获得单电子性质积分。

|                      |     |                                               |
|:---------------------|:---:|:----------------------------------------------|
| 1elPropertyIntegrals | \-  | 单电子性质积分                                |

目前下列选项有效：
|                   |     |                               |
|:------------------|:---:|:------------------------------|
| angular_momentum  | \-  | 角动量积分                    |
| dipole            | \-  | 偶极矩积分                    |
| higherMoment      | \-  | 八极矩积分                    |
| quadrupole        | \-  | 四极矩积分                    |
| velocity          | \-  | 速度积分                      |
| soc               | \-  | 自旋-轨道耦合积分             |

**示例**
```json
{
  "Calculation_Status": {
      "Status": "NORMAL TERMINATION",
      "progName": "LeanSCF",
      "version": "6.0.x"
  },
  "Geometries": [
    {
      "Geometry": {
        "Coordinates": {
            "Cartesians": [
                [
                    "H",
                    0.0,
                    0.0,
                    0.0
                ],
                [
                    "H",
                    0.0,
                    0.0,
                    1.511780907137
                ]
            ],
            "Type": "Cartesians",
            "Units": "a.u."
        },
        "NAtoms": 2,
        "NCorelessECP": 0,
        "NGhostAtoms": 0
      },
      "SCF_Energy": {
        "totalEnergy": -1.1271129220233282
      }
    }
  ]
}
```

!!! note "注意"
    SOC 积分按 `.gbw` 文件中所选设置计算，
    相对论哈密顿量除外（相对论版本见 [electronintegrals.1elrelprop](#sec:orca_2json.availableinformation.electronintegrals.1elrelprop)）。
    在 SOMF 的情况下，使用密度容器中的 SCF 密度。

<a id="sec:orca_2json.availableinformation.electronintegrals.1elrel"></a>
#### 单电子相对论积分（1-electron relativistic integrals）

单电子相对论积分遵循与相应非相对论积分相同的记号（见 [electronintegrals.1el](#sec:orca_2json.availableinformation.electronintegrals.1el)）。

**示例**
```json
orca_2json BaseName.json -gbw
```
本示例将生成并存储在相应 json 文件中的是 X2C 变换后的 H 矩阵，
以及分开的势能和动能贡献。
请注意，虽然"相对论"重叠矩阵为完整性而提供，
但在 X2C 中它按构造与非相对论重叠矩阵相同。

<a id="sec:orca_2json.availableinformation.electronintegrals.1elrelprop"></a>
#### 单电子相对论性质积分（1-electron relativistic property integrals）
还可获得单电子相对论（X2C）性质积分，与非相对论的类似但选项较少。

|                         |     |                                               |
|:------------------------|:---:|:----------------------------------------------|
| 1elPropertyRelIntegrals | \-  | 相对论单电子性质积分                          |

目前下列选项有效：
|                   |     |                               |
|:------------------|:---:|:------------------------------|
| angular_momentum  | \-  | 角动量积分                    |
| dipole            | \-  | 偶极矩积分                    |
| quadrupole        | \-  | 四极矩积分                    |
| soc               | \-  | 自旋-轨道耦合积分             |

**示例**
```json
{
  "Molecule": {
    "Atoms": [
      {"Basis": [
          {"Coefficients": [ 0.1543289707029839,
              0.5353281424384732,0.44463454202535485],
            "Exponents": [3.42525091,0.62391373,0.1688554],
            "Shell": "s"}],
        "Coords": [0.0,0.0,0.0],
        "ElementNumber": 1,
        "NuclearCharge": 1.0},
      {"Basis": [
          {"Coefficients": [0.1543289707029839,
              0.5353281424384732,0.44463454202535485],
            "Exponents": [3.42525091,0.62391373,0.1688554],
            "Shell": "s"}],
        "Coords": [0.0,0.0,0.8],
        "ElementNumber": 1,
        "NuclearCharge": 1.0}],
    "Charge": 0,
    "CoordinateUnits": "Angs",
    "HFTyp": "RHF",
    "MolecularOrbitals": {
      "EnergyUnit": "Eh",
      "MOs": [{"MOCoefficients": [
            -0.5554171364661243,-0.5554171364661241],
          "Occupancy": 2.0,
          "OrbitalEnergy": -0.5544958795933514,
          "OrbitalSymLabel": "A",
          "OrbitalSymmetry": 0},
        {"MOCoefficients": [
            -1.1482994800696493,1.1482994800696493],
          "Occupancy": 0.0,
          "OrbitalEnergy": 0.6126180830925017,
          "OrbitalSymLabel": "A",
          "OrbitalSymmetry": 0}]},
    "Multiplicity": 1}
}
```
<a id="sec:orca_2json.availableinformation.electronintegrals.1elorigin"></a>
#### 原点设置（Origin setting）
电性质的原点默认是笛卡尔原点，但也可以选择质心和核电荷中心。此外，当选择 ori_el = 3 时可以给出 x,y,z 坐标形式的任意位置。
目前下列选项有效：
|                   |     |                               |
|:------------------|:---:|:------------------------------|
| ori_el            | \-  | 0 - 笛卡尔原点                |
|                   | \-  | 1 - 质心                      |
|                   | \-  | 2 - 核电荷中心                |
|                   | \-  | 3 - 任意位置                  |
| ori_el_xyz        | \-  | 原点位置 (x,y,z)              |

**示例**
```json
orca_2json filename.json -gbw
```

<a id="sec:orca_2json.availableinformation.electronintegrals.2el"></a>
#### Fock 矩阵贡献（Fock matrix contributions）

下列 AO 基 Fock 矩阵的双电子贡献可以导出：
|     |     |                                 |
|:----|:---:|:--------------------------------|
| J   | \-  | 库仑（Coulomb）                 |
| K   | \-  | 交换（Exchange）                |
| VXC | \-  | DFT XC 势                       |
| Vsol| \-  | 隐式溶剂势                      |
| F   | \-  | 总 Fock 矩阵                    |

!!! note
    - 所有项使用 .densities 文件中的 SCF（自旋）密度（名为 "scfp" 和 "scfr"）计算。
    - 使用与原计算相同的设置和近似（RI、COSX、网格）。
    - 所有前置因子已包含在内，使得 $\mathrm{F} = \mathrm{J} + \mathrm{K} + \mathrm{VXC} + \mathrm{Vsol}$。
    - 为保持一致性，输出维度始终为 $N_\text{spin-ops} \times N_\text{AO} \times N_\text{AO}$，
      尽管所有矩阵都是对称的，且某些项（J 和 Vsol）在 UHF 情况下对 alpha/beta 相同。
    - 单电子贡献（"H"）不包含在内，必须单独请求
      （见 [electronintegrals.1el](#sec:orca_2json.availableinformation.electronintegrals.1el)，
      相对论情况见 [electronintegrals.1elrel](#sec:orca_2json.availableinformation.electronintegrals.1elrel)）。

**示例**
```json
BaseName.json.conf
```

#### 双电子积分（2-electron integrals）

ORCA_2json 可以生成并写入磁盘三大类双电子积分。
1. 原子基下的双电子积分（[2el.AO](#sec:orca_2json.availableinformation.electronintegrals.2el.AO)）
2. 分子基下的双电子积分（[2el.MO](#sec:orca_2json.availableinformation.electronintegrals.2el.MO)）
3. 使用密度拟合近似（Resolution of Identity，RI）的双电子积分（[2el.RI](#sec:orca_2json.availableinformation.electronintegrals.2el.RI)）

<a id="sec:orca_2json.availableinformation.electronintegrals.2el.AO"></a>
##### AO 基下的双电子积分（2-electron integrals in AO basis）

在原子基中，双电子积分可以按库仑序或交换序保存。两个选项的关键词见下表。

|             |     |                                               |
|:------------|:---:|:----------------------------------------------|
|  AO_PQRS    | \-  |  库仑序的 AO 基积分                           |
|  AO_PRQS    | \-  |  交换序的 AO 基积分                           |

<a id="sec:orca_2json.availableinformation.electronintegrals.2el.MO"></a>
##### MO 基下的双电子积分（2-electron integrals in MO basis）

在分子基中，ORCA 遵循公认的记号，其中 I、J、K 和 L 表示"内部"轨道（即参考波函数中的占据轨道），A、B、C 和 D 表示"外部"轨道（即参考波函数中的空轨道）。
P、Q、R 和 S 表示所有可能的轨道，即既包括"内部"也包括"外部"。
*"orca_2json"* 中分子基双电子积分的可用关键词见下表：
|             |     |                                               |
|:------------|:---:|:----------------------------------------------|
|  MO_IJKL    | \-  |  库仑 0-外部                                  |
|  MO_IJKA    | \-  |  库仑 1-外部                                  |
|  MO_IJAB    | \-  |  库仑 2-外部                                  |
|  MO_IABC    | \-  |  库仑 3-外部                                  |
|  MO_ABCD    | \-  |  库仑 4-外部                                  |
|  MO_PQRS    | \-  |  库仑 全部积分                                |
|  MO_IKJL    | \-  |  交换 0-外部                                  |
|  MO_IKJA    | \-  |  交换 1-外部                                  |
|  MO_IAJB    | \-  |  交换 2-外部                                  |
|  MO_IBAC    | \-  |  交换 3-外部                                  |
|  MO_ACBD    | \-  |  交换 4-外部                                  |
|  MO_PRQS    | \-  |  交换 全部积分                                |

**示例**
```json
orca.json.conf
```

<a id="sec:orca_2json.availableinformation.electronintegrals.2el.RI"></a>
##### RI 双电子积分（RI 2-electron integrals）

使用密度拟合（Resolution of Identity，RI）可以更高效地创建积分。RI 积分有两大类：三指标积分（其中只完成了一半变换）和四指标积分（积分在分子基中完全变换）。积分的记号遵循我们刚才为分子基双电子积分所描述的记号。

|             |     |                                               |
|:------------|:---:|:----------------------------------------------|
|  RI_IJV     | \-  |  RI 三指标 0-外部                             |
|  RI_IAV     | \-  |  RI 三指标 1-外部                             |
|  RI_ABV     | \-  |  RI 三指标 2-外部                             |
|  RI_IJKL    | \-  |  RI 四指标库仑 0-外部                         |
|  RI_IJKA    | \-  |  RI 四指标库仑 1-外部                         |
|  RI_IJAB    | \-  |  RI 四指标库仑 2-外部                         |
|  RI_IABC    | \-  |  RI 四指标库仑 3-外部                         |
|  RI_ABCD    | \-  |  RI 四指标库仑 4-外部                         |
|  RI_IKJL    | \-  |  RI 四指标交换 0-外部                         |
|  RI_IKJA    | \-  |  RI 四指标交换 1-外部                         |
|  RI_IAJB    | \-  |  RI 四指标交换 2-外部                         |
|  RI_IBAC    | \-  |  RI 四指标交换 3-外部                         |
|  RI_ACBD    | \-  |  RI 四指标交换 4-外部                         |

除积分外，在 RI 积分的情况下所用的 RI 度量也可通过选项 Vaux 获得：
|             |     |                                               |
|:------------|:---:|:----------------------------------------------|
|  Vaux       | \-  |  true/false                                   |

**示例**
```json
{
	"keyword": true/false,
	...
	"keyword": true/false,
	"keyword": ["option",...."option"]
	...
}
```

<a id="sec:orca_2json.availableinformation.electronintegrals.2el.fulltrafo"></a>
##### 完全积分变换（Full Integral Transformation）

完全变换积分可以通过 FullTrafo 关键词选择。

|              |     |                     |
|:-------------|:---:|:--------------------|
|  FullTrafo   | \-  | true/false          |

<a id="sec:orca_2json.availableinformation.electronintegrals.2el.nonred"></a>
##### 更多双电子积分（More 2-electron integrals）

非冗余双电子积分对 RI 和非 RI 情况也可用。因此必须指定选项 2elNonRedIntegrals 或 2elNonRedRIIntegrals。

|                       |     |                     |
|:----------------------|:---:|:--------------------|
|  2elNonRedIntegrals   | \-  | true/false          |
|  2elNonRedRIIntegrals | \-  | true/false          |

<a id="sec:orca_2json.availableinformation.electronintegrals.2el.orbwin"></a>
##### 轨道窗口、AuxBasisType 与阈值（Orbital Windows, AuxBasisType and Threshold）

轨道窗口可以由变换例程自动选择，也可以由用户通过 OrbWin 关键词给出。内部和外部空间（i0,i1,a0,a1）通过整数列表定义。

例如：
|              |     |                          |
|:-------------|:---:|:-------------------------|
|  OrbWin      | \-  |  [0,8,9,15]              |
|              | \-  |  [0,12,13,30,0,12,13,30] |

默认 AUX 基类型是 AuxC，但可以用关键词 AuxBasisType 更改。请记住只能选择 ORCA 运行中使用过的基组类型。

|               |     |         |
|:--------------|:---:|:--------|
|  AuxBasisType | \-  |  AuxJ   |
|               | \-  |  AuxJK  |
|               | \-  |  AuxC   |

为减少积分数目，关键词 Thresh 可用于减少所选积分以节省磁盘空间。这只影响打印而不影响所生成积分的精度。默认打印阈值为 1.e-15。

|              |     |                                      |
|:-------------|:---:|:-------------------------------------|
|  Thresh      | \-  |  打印阈值（默认 1.e-15）             |

**示例**
```json
{
  "MOCoefficients":false,
  "BasisSet":false
}
```

<a id="sec:orca_2json.availableinformation.CIS"></a>
### TDDFT 振幅数据（CIS/RPA）

可以请求 TDDFT 振幅和根信息。
可用选项为：

|              |     |                              |
|:-------------|:---:|:-----------------------------|
| CIS          | \-  | TDDFT 振幅                   |
| CISNRoots    | \-  | 所有根的信息                 |
| CISROOT      | \-  | 根的列表                     |

**示例**
打印选定的根。根编号对应 ORCA 输出文件中的 `STATE` 编号。
```json
{
	"MOCoefficients": false,
	"Basisset": true,
	"1elPropertyIntegrals": ["dipole", "quadrupole", "velocity", "printLinMom", "angular_momentum", "higherMoment", "soc"],
	"1elPropertyRelIntegrals": ["dipole", "quadrupole", "angular_momentum", "soc"],
	"1elIntegrals": ["H", "S", "T", "V", "HMO"],
	"1elIntegralsRel": ["H", "S", "T", "V", "HMO"],
        "FockMatrix": ["F", "J", "K", "VXC", "Vsol"],
	"Vaux": false,
	"AuxBasisType": "AuxC",
	"FullTrafo": false,
	"OrbWin": [0,0,0,0,0,0,0,0],
	"2elIntegrals": [ "MO_IJKL", "RI_IAV", "RI_IJKL"],
	"2elNonRedIntegrals": false,
	"2elNonRedRIIntegrals": false,
	"MullikenCharge": false,
	"LoewdinCharge": false,
	"Densities": ["all"],   <--- here you specify the names like "scfp" or "scfr" or all
	"JSONFormats": ["json", "bson"]
}
```
**示例**
打印所有根。
```json
{
  "JSONFormats":["json","bson","ubjson","msgpck"]
}
```

<a id="sec:orca_2json.availableinformation.STEOM"></a>
### STEOM 振幅数据（STEOM amplitude data）

可以请求 STEOM 单激发振幅和根信息。
可用选项为：

|                   |     |                              |
|:------------------|:---:|:-----------------------------|
| STEOM             | \-  | STEOM 单激发振幅             |
| STEOMRootsSinglet | \-  | 单重态根的列表               |
| STEOMRootsTriplet | \-  | 三重态根的列表               |

**示例**
打印所有根。
```json
{
  "MOCoefficients": false,
  "Basisset": false,
  "MullikenCharge": false,
  "LoewdinCharge": false,
  "JSONFormats": ["json"]
}
```
**示例**
打印选定的根。根编号对应 ORCA 输出文件中的 `IROOT` 编号。
```json
{
  "Molecule": {
    "Atoms": [
      {
        "Coords": [
          0.0,
          0.0,
          0.0
        ],
        "ElementLabel": "H",
        "ElementNumber": 1,
        "Idx": 0,
        "NuclearCharge": 1.0
      },
      {
        "Coords": [
          0.0,
          0.0,
          0.8
        ],
        "ElementLabel": "H",
        "ElementNumber": 1,
        "Idx": 1,
        "NuclearCharge": 1.0
      }
    ],
    "BaseName": "test",
    "Charge": 0,
    "CoordinateUnits": "Angs",
    "HFTyp": "RHF",
    "Multiplicity": 1,
    "PointGroup": "C1"
  },
  "ORCA Header": {
    "Date": "2024-06-03 00:06:37 +0200",
    "Git": "548015a5a0",
    "Version": "                         Program Version 6.0  -  CURRENT   -\n"
  }
}
```

<a id="sec:orca_2json.availableinformation.mocoefficients"></a>
### MO 系数（MO Coefficients）

|                 |     |                                               |
|:----------------|:---:|:----------------------------------------------|
| MOCoefficients  | \-  | 分子轨道信息 (true\false)                     |

**示例**
```json
{
    "Densities": {
        "RDM2": {
            "0,0": [[0.0, 0.0], [0.0, 0.0]] // p=0, q=0
            "0,1": [[0.0, 0.0], [0.0, 0.0]] // p=0, q=1
            "1,0": [[0.0, 0.0], [0.0, 0.0]] // p=1, q=0
            "1,1": [[0.0, 0.0], [0.0, 0.0]] // p=1, q=1
        }
    }
}
```

<a id="sec:orca_2json.real_solid_harmonics"></a>
## 实固体谐波轨道的定义（Definition of the real solid harmonic orbitals）

当实固体谐波轨道上的积分被写入 JSON 文件时，
这些轨道的精确定义就变得很重要。ORCA 对轨道壳层各分量的排列和相位
使用其自己特有的约定。

直到角动量 $n$（$\ell=10$）的所有壳层分量的角向部分定义记录如下。这些对应于
按下列方式归一化的实固体谐波 $S_{\ell,m}(x,y,z)$：

$$
\begin{aligned}
    \in t_0^\pi\sin\vartheta\,d\vartheta
    \in t_{-\pi}^\pi d\varphi\,r^{-2\ell}S^2_{\ell,m}(x,y,z)=1
  \end{aligned}
$$

$R_\ell(r)$ 是角动量为 $\ell$ 的壳层的公共径向部分，由依赖于特定基组的
原子高斯函数的线性组合构成。它独立归一化：

$$
\begin{aligned}
    \in t_0^\in fty r^{2\ell+2}R^2_\ell(r)\,dr=1
  \end{aligned}
$$

这些积分中的因子 $r^2$ 和 $\sin\vartheta$ 来自
球极坐标中的体积元：

$$
\begin{aligned}
    x &= r\sin\vartheta\cos\varphi \\
    y &= r\sin\vartheta\sin\varphi \\
    z &= r\cos\vartheta \\
    dx\,dy\,dz &= r^2\sin\vartheta\,dr\,d\vartheta\,d\varphi
  \end{aligned}
$$

请注意，对称性模块目前仍限于
最大角动量量子数为 8。

### 角动量 $s$（$l = 0$）

$$
\begin{aligned}
    s &= \frac{1}{2\sqrt{\pi} }\,R_s(r)
  \end{aligned}
$$

### 角动量 $p$（$l = 1$）

$$
\begin{aligned}
    N_p &= \frac{1}{2}\sqrt{\frac{3}{\pi} } \\
    p^{(0) } = p_{0\phantom{+} } &= N_p\,z\,R_p(r) \\
    p^{(1) } = p_{+1} &= N_p\,x\,R_p(r) \\
    p^{(2) } = p_{-1} &= N_p\,y\,R_p(r)
  \end{aligned}
$$

### 角动量 $d$（$l = 2$）

$$
\begin{aligned}
    N_d &= \frac{1}{2}\sqrt{\frac{15}{\pi} } \\
    d^{(0) } = d_{0\phantom{+} } &= \frac{\sqrt{3} }{6}\,N_d\left(3z^2-r^2\right)R_d(r) \\
    d^{(1) } = d_{+1} &= N_d\,xz\,R_d(r) \\
    d^{(2) } = d_{-1} &= N_d\,yz\,R_d(r) \\
    d^{(3) } = d_{+2} &= N_d\,\frac{x^2-y^2}{2}\,R_d(r) \\
    d^{(4) } = d_{-2} &= N_d\,xy\,R_d(r)
  \end{aligned}
$$

### 角动量 $f$（$l = 3$）

$$
\begin{aligned}
    N_f &= \frac{1}{2}\sqrt{\frac{105}{\pi} } \\
    f^{(0) } = f_{0\phantom{+} } &= \frac{\sqrt{15} }{30}\,N_f\,z\left(5z^2-3r^2\right)R_f(r) \\
    f^{(1) } = f_{+1} &= \frac{\sqrt{10} }{20}\,N_f\,x\left(5z^2-r^2\right)R_f(r) \\
    f^{(2) } = f_{-1} &= \frac{\sqrt{10} }{20}\,N_f\,y\left(5z^2-r^2\right)R_f(r) \\
    f^{(3) } = f_{+2} &= \frac{1}{2}\,N_f\left(x^2-y^2\right)z\,R_f(r) \\
    f^{(4) } = f_{-2} &= N_f\,xyz\,R_f(r) \\
    f^{(5) } = f_{+3} &= -\frac{\sqrt{6} }{12}\,N_f\,x\left(x^2-3y^2\right)R_f(r) \\
    f^{(6) } = f_{-3} &= -\frac{\sqrt{6} }{12}\,N_f\,y\left(3x^2-y^2\right)R_f(r)
  \end{aligned}
$$

### 角动量 $g$（$l = 4$）

$$
\begin{aligned}
    N_g &= \frac{3}{2}\sqrt{\frac{35}{\pi} } \\
    g^{(0) } = g_{0\phantom{+} } &= \frac{\sqrt{35} }{280}\,N_g\left(35z^4-30z^2r^2+3r^4\right)R_g(r) \\
    g^{(1) } = g_{+1} &= \frac{\sqrt{14} }{28}\,N_g\,xz\left(7z^2-3r^2\right)R_g(r) \\
    g^{(2) } = g_{-1} &= \frac{\sqrt{14} }{28}\,N_g\,yz\left(7z^2-3r^2\right)R_g(r) \\
    g^{(3) } = g_{+2} &= \frac{\sqrt{7} }{28}\,N_g\left(x^2-y^2\right)\left(7z^2-r^2\right)R_g(r) \\
    g^{(4) } = g_{-2} &= \frac{\sqrt{7} }{14}\,N_g\,xy\left(7z^2-r^2\right)R_g(r) \\
    g^{(5) } = g_{+3} &= -\frac{\sqrt{2} }{4}\,N_g\,x\left(x^2-3y^2\right)z\,R_g(r) \\
    g^{(6) } = g_{-3} &= -\frac{\sqrt{2} }{4}\,N_g\,y\left(3x^2-y^2\right)z\,R_g(r) \\
    g^{(7) } = g_{+4} &= -\frac{1}{8}\,N_g\left(x^4-6x^2y^2+y^4\right)R_g(r) \\
    g^{(8) } = g_{-4} &= -\frac{1}{2}\,N_g\,xy\left(x^2-y^2\right)R_g(r)
  \end{aligned}
$$

### 角动量 $h$（$l = 5$）

$$
\begin{aligned}
    N_h &= \frac{1}{2}\sqrt{\frac{11}{\pi} } \\
    h^{(0) }  = h_{0\phantom{+} } &= \frac{1}{8}\,N_h\,z\left(63z^4-70z^2r^2+15r^4\right)R_h(r) \\
    h^{(1) }  = h_{+1} &= \frac{\sqrt{15} }{8}\,N_h\,x\left(21z^4-14z^2r^2+r^4\right)R_h(r) \\
    h^{(2) }  = h_{-1} &= \frac{\sqrt{15} }{8}\,N_h\,y\left(21z^4-14z^2r^2+r^4\right)R_h(r) \\
    h^{(3) }  = h_{+2} &= \frac{\sqrt{105} }{4}\,N_h\left(x^2-y^2\right)z\left(3z^2-r^2\right)R_h(r) \\
    h^{(4) }  = h_{-2} &= \frac{\sqrt{105} }{2}\,N_h\,xyz\left(3z^2-r^2\right)R_h(r) \\
    h^{(5) }  = h_{+3} &= -\frac{\sqrt{70} }{16}\,N_h\,x\left(x^2-3y^2\right)\left(9z^2-r^2\right)R_h(r) \\
    h^{(6) }  = h_{-3} &= -\frac{\sqrt{70} }{16}\,N_h\,y\left(3x^2-y^2\right)\left(9z^2-r^2\right)R_h(r) \\
    h^{(7) }  = h_{+4} &= -\frac{3\sqrt{35} }{8}\,N_h\left(x^4-6x^2y^2+y^4\right)z\,R_h(r) \\
    h^{(8) }  = h_{-4} &= -\frac{3\sqrt{35} }{2}\,N_h\,xy\left(x^2-y^2\right)z\,R_h(r) \\
    h^{(9) }  = h_{+5} &= \frac{3\sqrt{14} }{16}\,N_h\,x\left(x^4-10x^2y^2+5y^4\right)R_h(r) \\
    h^{(10) } = h_{-5} &= \frac{3\sqrt{14} }{16}\,N_h\,y\left(5x^4-10x^2y^2+y^4\right)R_h(r)
  \end{aligned}
$$

### 角动量 $i$（$l = 6$）

$$
\begin{aligned}
    N_i &= \frac{1}{2}\sqrt{\frac{13}{\pi} } \\
    i^{(0) }  = i_{0\phantom{+} } &= \frac{1}{16}\,N_i\left(231z^6-315z^4r^2+105z^2r^4-5r^6\right)R_i(r) \\
    i^{(1) }  = i_{+1} &= \frac{\sqrt{21} }{8}\,N_i\,xz\left(33z^4-30z^2r^2+5r^4\right)R_i(r) \\
    i^{(2) }  = i_{-1} &= \frac{\sqrt{21} }{8}\,N_i\,yz\left(33z^4-30z^2r^2+5r^4\right)R_i(r) \\
    i^{(3) }  = i_{+2} &= \frac{\sqrt{210} }{32}\,N_i\left(x^2-y^2\right)\left(33z^4-18z^2r^2+r^4\right)R_i(r) \\
    i^{(4) }  = i_{-2} &= \frac{\sqrt{210} }{16}\,N_i\,xy\left(33z^4-18z^2r^2+r^4\right)R_i(r) \\
    i^{(5) }  = i_{+3} &= -\frac{\sqrt{210} }{16}\,N_i\,x\left(x^2-3y^2\right)z\left(11z^2-3r^2\right)R_i(r) \\
    i^{(6) }  = i_{-3} &= -\frac{\sqrt{210} }{16}\,N_i\,y\left(3x^2-y^2\right)z\left(11z^2-3r^2\right)R_i(r) \\
    i^{(7) }  = i_{+4} &= -\frac{3\sqrt{7} }{16}\,N_i\left(x^4-6x^2y^2+y^4\right)\left(11z^2-r^2\right)R_i(r) \\
    i^{(8) }  = i_{-4} &= -\frac{3\sqrt{7} }{4}\,N_i\,xy\left(x^2-y^2\right)\left(11z^2-r^2\right)R_i(r) \\
    i^{(9) }  = i_{+5} &= \frac{3\sqrt{154} }{16}\,N_i\,x\left(x^4-10x^2y^2+5y^4\right)z\,R_i(r) \\
    i^{(10) } = i_{-5} &= \frac{3\sqrt{154} }{16}\,N_i\,y\left(5x^4-10x^2y^2+y^4\right)z\,R_i(r) \\
    i^{(11) } = i_{+6} &= \frac{\sqrt{462} }{32}\,N_i\left(x^2-y^2\right)\left(x^4-14x^2y^2+y^4\right)R_i(r) \\
    i^{(12) } = i_{-6} &= \frac{\sqrt{462} }{16}\,N_i\,xy\left(x^2-3y^2\right)\left(3x^2-y^2\right)R_i(r)
  \end{aligned}
$$

### 角动量 $k$（$l = 7$）

请注意，在 ORCA 6.0 及更早版本中，角动量量子数为 7 的基函数
标签为 $j$，与光谱学中跳过字母 $j$ 的通常约定相反。这一不一致已在 ORCA 6.1 版本中更正。

$$
\begin{aligned}
N_k &= \frac{1}{2}\sqrt{\frac{15}{\pi} } \\
k^{(0) }  = k_{0\phantom{+} } &= \frac{1}{16}\,N_k\,z\left(429z^6-693z^4r^2+315z^2r^4-35r^6\right)R_k(r) \\
k^{(1) }  = k_{+1} &= \frac{\sqrt{7} }{32}\,N_k\,x\left(429z^6-495z^4r^2+135z^2r^4-5r^6\right)R_k(r) \\
k^{(2) }  = k_{-1} &= \frac{\sqrt{7} }{32}\,N_k\,y\left(429z^6-495z^4r^2+135z^2r^4-5r^6\right)R_k(r) \\
k^{(3) }  = k_{+2} &= \frac{\sqrt{42} }{32}\,N_k\left(x^2-y^2\right)z\left(143z^4-110z^2r^2+15r^4\right)R_k(r) \\
k^{(4) }  = k_{-2} &= \frac{\sqrt{42} }{16}\,N_k\,xyz\left(143z^4-110z^2r^2+15r^4\right)R_k(r) \\
k^{(5) }  = k_{+3} &= -\frac{\sqrt{21} }{32}\,N_k\,x\left(x^2-3y^2\right)\left(143z^4-66z^2r^2+3r^4\right)R_k(r) \\
k^{(6) }  = k_{-3} &= -\frac{\sqrt{21} }{32}\,N_k\,y\left(3x^2-y^2\right)\left(143z^4-66z^2r^2+3r^4\right)R_k(r) \\
k^{(7) }  = k_{+4} &= -\frac{\sqrt{231} }{16}\,N_k\left(x^4-6x^2y^2+y^4\right)z\left(13z^2-3r^2\right)R_k(r) \\
k^{(8) }  = k_{-4} &= -\frac{\sqrt{231} }{4}\,N_k\,xy\left(x^2-y^2\right)z\left(13z^2-3r^2\right)R_k(r) \\
k^{(9) }  = k_{+5} &= \frac{\sqrt{231} }{32}\,N_k\,x\left(x^4-10x^2y^2+5y^4\right)\left(13z^2-r^2\right)R_k(r) \\
k^{(10) } = k_{-5} &= \frac{\sqrt{231} }{32}\,N_k\,y\left(5x^4-10x^2y^2+y^4\right)\left(13z^2-r^2\right)R_k(r) \\
k^{(11) } = k_{+6} &= \frac{\sqrt{6006} }{32}\,N_k\left(x^2-y^2\right)\left(x^4-14x^2y^2+y^4\right)z\,R_k(r) \\
k^{(12) } = k_{-6} &= \frac{\sqrt{6006} }{16}\,N_k\,xy\left(x^2-3y^2\right)\left(3x^2-y^2\right)z\,R_k(r) \\
k^{(13) } = k_{+7} &= -\frac{\sqrt{429} }{32}\,N_k\,x\left(x^6-21x^4y^2+35x^2y^4-7y^6\right)R_k(r) \\
k^{(14) } = k_{-7} &= -\frac{\sqrt{429} }{32}\,N_k\,y\left(7x^6-35x^4y^2+21x^2y^4-y^6\right)R_k(r)
  \end{aligned}
$$

### 角动量 $l$（$l = 8$）

请注意，在 ORCA 6.0 及更早版本中，角动量量子数为 8 的基函数
从未真正被支持过。尝试使用它们很可能导致崩溃。

另请注意，符号 $l$ 在基组文件中保留给具有公共高斯指数集的 $sp$ 壳层。因此对于角动量 8 及以上，需要使用数值而非字母。

$$
\begin{aligned}
N_l &= \frac{1}{2}\sqrt{\frac{17}{\pi} } \\
l^{(0) }  = l_{0\phantom{+} } &= \frac{1}{128}\,N_l\left(6435z^8-12012z^6r^2+6930z^4r^4-1260z^2r^6+35r^8\right)R_l(r) \\
l^{(1) }  = l_{+1} &= \frac{3}{32}\,N_l\,xz\left(715z^6-1001z^4r^2+385z^2r^4-35r^6\right)R_l(r) \\
l^{(2) }  = l_{-1} &= \frac{3}{32}\,N_l\,yz\left(715z^6-1001z^4r^2+385z^2r^4-35r^6\right)R_l(r) \\
l^{(3) }  = l_{+2} &= \frac{3\sqrt{70} }{64}\,N_l\left(x^2-y^2\right)\left(143z^6-143z^4r^2+33z^2r^4-r^6\right)R_l(r) \\
l^{(4) }  = l_{-2} &= \frac{3\sqrt{70} }{32}\,N_l\,xy\left(143z^6-143z^4r^2+33z^2r^4-r^6\right)R_l(r) \\
l^{(5) }  = l_{+3} &= -\frac{\sqrt{1155} }{32}\,N_l\,x\left(x^2-3y^2\right)z\left(39z^4-26z^2r^2+3r^4\right)R_l(r) \\
l^{(6) }  = l_{-3} &= -\frac{\sqrt{1155} }{32}\,N_l\,y\left(3x^2-y^2\right)z\left(39z^4-26z^2r^2+3r^4\right)R_l(r) \\
l^{(7) }  = l_{+4} &= -\frac{3\sqrt{77} }{64}\,N_l\,\left(x^4-6x^2y^2+y^4\right)\left(65z^4-26z^2r^2+r^4\right)R_l(r) \\
l^{(8) }  = l_{-4} &= -\frac{3\sqrt{77} }{16}\,N_l\,xy\left(x^2-y^2\right)\left(65z^4-26z^2r^2+r^4\right)R_l(r) \\
l^{(9) }  = l_{+5} &= \frac{3\sqrt{1001} }{32}\,N_l\,x\left(x^4-10x^2y^2+5y^4\right)z\left(5z^2-r^2\right)R_l(r) \\
l^{(10) } = l_{-5} &= \frac{3\sqrt{1001} }{32}\,N_l\,y\left(5x^4-10x^2y^2+y^4\right)z\left(5z^2-r^2\right)R_l(r) \\
l^{(11) } = l_{+6} &= \frac{\sqrt{858} }{64}\,N_l\left(x^2-y^2\right)\left(x^4-14x^2y^2+y^4\right)\left(15z^2-r^2\right)R_l(r) \\
l^{(12) } = l_{-6} &= \frac{\sqrt{858} }{32}\,N_l\,xy\left(x^2-3y^2\right)\left(3x^2-y^2\right)\left(15z^2-r^2\right)R_l(r) \\
l^{(13) } = l_{+7} &= -\frac{3\sqrt{715} }{32}\,N_l\,x\left(x^6-21x^4y^2+35x^2y^4-7y^6\right)z\,R_l(r) \\
l^{(14) } = l_{-7} &= -\frac{3\sqrt{715} }{32}\,N_l\,y\left(7x^6-35x^4y^2+21x^2y^4-y^6\right)z\,R_l(r) \\
l^{(15) } = l_{+8} &= -\frac{3\sqrt{715} }{128}\,N_l\left(x^8-28x^6y^2+70x^4y^4-28x^2y^6+y^8\right)R_l(r) \\
l^{(16) } = l_{-8} &= -\frac{3\sqrt{715} }{16}\,N_l\,xy\left(x^2-y^2\right)\left(x^4-6x^2y^2+y^4\right)R_l(r)
  \end{aligned}
$$

### 角动量 $m$（$l = 9$）

请注意，对称性模块目前仍限于
最大角动量量子数为 8。

$$
\begin{aligned}
N_m &= \frac{1}{2}\sqrt{\frac{19}{\pi} } \\
m^{(0) }  = m_{0\phantom{+} } &= \frac{1}{128}\,N_m\,z\left(12155z^8-25740z^6r^2+18018z^4r^4-4620z^2r^6+315r^8\right)R_m \\
m^{(1) }  = m_{+1} &= \frac{3\sqrt{5}}{128}\,N_m\,x\left(2431z^8-4004z^6r^2+2002z^4r^4-308z^2r^6+7r^8\right)R_m \\
m^{(2) }  = m_{-1} &= \frac{3\sqrt{5}}{128}\,N_m\,y\left(2431z^8-4004z^6r^2+2002z^4r^4-308z^2r^6+7r^8\right)R_m \\
m^{(3) }  = m_{+2} &= \frac{3\sqrt{110}}{64}\,N_m\bigl(x^2-y^2\bigr)z\left(221z^6-273z^4r^2+91z^2r^4-7r^6\right)R_m \\
m^{(4) }  = m_{-2} &= \frac{3\sqrt{110}}{32}\,N_m\,xyz\left(221z^6-273z^4r^2+91z^2r^4-7r^6\right)R_m \\
m^{(5) }  = m_{+3} &= \frac{\sqrt{2310}}{128}\,N_m\,x\left(x^2-3y^2\right)\left(221z^6-195z^4r^2+39z^2r^4-r^6\right)R_m \\
m^{(6) }  = m_{-3} &= \frac{\sqrt{2310}}{128}\,N_m\,y\left(3x^2-y^2\right)\left(221z^6-195z^4r^2+39z^2r^4-r^6\right)R_m \\
m^{(7) }  = m_{+4} &= \frac{3\sqrt{5005}}{64}\,N_m\left(x^4-6x^2y^2+y^4\right)z\left(17z^4-10z^2r^2+r^4\right)R_m \\
m^{(8) }  = m_{-4} &= \frac{3\sqrt{5005}}{16}\,N_m\,xy\left(x^2-y^2\right)z\left(17z^4-10z^2r^2+r^4\right)R_m \\
m^{(9) }  = m_{+5} &= \frac{3\sqrt{286}}{128}\,N_m\,x\left(x^4-10x^2y^2+5y^4\right)\left(85z^4-30z^2r^2+r^4\right)R_m \\
m^{(10)}  = m_{-5} &= \frac{3\sqrt{286}}{128}\,N_m\,y\left(5x^4-10x^2y^2+y^4\right)\left(85z^4-30z^2r^2+r^4\right)R_m \\
m^{(11)}  = m_{+6} &= \frac{\sqrt{4290}}{64}\,N_m\left(x^2-y^2\right)\left(x^4-14x^2y^2+y^4\right)z\left(17z^2-3r^2\right)R_m \\
m^{(12)}  = m_{-6} &= \frac{\sqrt{4290}}{32}\,N_m\,xy\left(x^2-3y^2\right)\left(3x^2-y^2\right)z\left(17z^2-3r^2\right)R_m \\
m^{(13)}  = m_{+7} &= \frac{3\sqrt{1430}}{256}\,N_m\,x\left(x^6-21x^4y^2+35x^2y^4-7y^6\right)\left(17z^2-r^2\right)R_m \\
m^{(14)}  = m_{-7} &= \frac{3\sqrt{1430}}{256}\,N_m\,y\left(7x^6-35x^4y^2+21x^2y^4-y^6\right)\left(17z^2-r^2\right)R_m \\
m^{(15)}  = m_{+8} &= \frac{3\sqrt{12155}}{128}\,N_m\left(x^8-28x^6y^2+70x^4y^4-28x^2y^6+y^8\right)zR_m \\
m^{(16)}  = m_{-8} &= \frac{3\sqrt{12155}}{16}\,N_m\,xy\left(x^2-y^2\right)\left(x^4-6x^2y^2+y^4\right)zR_m \\
m^{(17)}  = m_{+9} &= \frac{\sqrt{24310}}{256}\,N_m\,x\left(x^2-3y^2\right)\left(x^6-33x^4y^2+27x^2y^4-3y^6\right)R_m \\
m^{(18)}  = m_{-9} &= \frac{\sqrt{24310}}{256}\,N_m\,y\left(3x^2-y^2\right)\left(3x^6-27x^4y^2+33x^2y^4-y^6\right)R_m
  \end{aligned}
$$

### 角动量 $n$（$l = 10$）

请注意，对称性模块目前仍限于
最大角动量量子数为 8。

$$
\begin{aligned}
N_n &= \frac{1}{2}\sqrt{\frac{21}{\pi} } \\
n^{(0) }  = n_{0\phantom{+0}} &= \frac{1}{256}\,N_n\left(46189z^{10}-109395z^8r^2+90090z^6r^4-30030z^4r^6+3465z^2r^8-63r^{10}\right)R_n \\
n^{(1) }  = n_{+1\phantom{0}} &= \frac{\sqrt{55}}{128}\,N_n\,xz\left(4199z^8-7956z^6r^2+4914r^4z^4-1092z^2r^6+63r^8\right)R_n \\
n^{(2) }  = n_{-1\phantom{0}} &= \frac{\sqrt{55}}{128}\,N_n\,yz\left(4199z^8-7956z^6r^2+4914r^4z^4-1092z^2r^6+63r^8\right)R_n \\
n^{(3) }  = n_{+2\phantom{0}} &= \frac{\sqrt{165}}{256}\,N_n\left(x^2-y^2\right)\left(4199z^8-6188z^6r^2+2730z^4r^4-364z^2r^6+7r^8\right)R_n \\
n^{(4) }  = n_{-2\phantom{0}} &= \frac{\sqrt{165}}{128}\,N_n\,xy\left(4199z^8-6188z^6r^2+2730z^4r^4-364z^2r^6+7r^8\right)R_n \\
n^{(5) }  = n_{+3\phantom{0}} &= \frac{\sqrt{4290}}{128}\,N_n\,x\left(x^2-3y^2\right)z\left(323z^6-357z^4r^2+105z^2r^4-7r^6\right)R_n \\
n^{(6) }  = n_{-3\phantom{0}} &= \frac{\sqrt{4290}}{128}\,N_n\,y\left(3x^2-y^2\right)z\left(323z^6-357z^4r^2+105z^2r^4-7r^6\right)R_n \\
n^{(7) }  = n_{+4\phantom{0}} &= \frac{\sqrt{2145}}{128}\,N_n\left(x^4-6x^2y^2+y^4\right)\left(323z^6-255z^4r^2+45z^2r^4-r^6\right)R_n \\
n^{(8) }  = n_{-4\phantom{0}} &= \frac{\sqrt{2145}}{32}\,N_n\,xy\left(x^2-y^2\right)\left(323z^6-255z^4r^2+45z^2r^4-r^6\right)R_n \\
n^{(9) }  = n_{+5\phantom{0}} &= \frac{\sqrt{858}}{128}\,N_n\,x\left(x^4-10x^2y^2+5y^4\right)z\left(323z^4-170z^2r^2+15r^4\right)R_n \\
n^{(10)}  = n_{-5\phantom{0}} &= \frac{\sqrt{858}}{128}\,N_n\,y\left(5x^4-10x^2y^2+y^4\right)z\left(323z^4-170z^2r^2+15r^4\right)R_n \\
n^{(11)}  = n_{+6\phantom{0}} &= \frac{\sqrt{4290}}{512}\,N_n\left(x^2-y^2\right)\left(x^4-14x^2y^2+y^4\right)\bigl(323z^4-102z^2r^2+3r^4\bigr)R_n \\
n^{(12)}  = n_{-6\phantom{0}} &= \frac{\sqrt{4290}}{256}\,N_n\,xy\left(x^2-3y^2\right)\left(3x^2-y^2\right)\bigl(323z^4-102z^2r^2+3r^4\bigr)R_n \\
n^{(13)}  = n_{+7\phantom{0}} &= \frac{\sqrt{72930}}{256}\,N_n\,x\left(x^6-21x^4y^2+35x^2y^4-7y^6\right)z\left(19z^2-3r^2\right)R_n \\
n^{(14)}  = n_{-7\phantom{0}} &= \frac{\sqrt{72930}}{256}\,N_n\,y\left(7x^6-35x^4y^2+21x^2y^4-y^6\right)z\left(19z^2-3r^2\right)R_n \\
n^{(15)}  = n_{+8\phantom{0}} &= \frac{\sqrt{12155}}{256}\,N_n\left(x^8-28x^6y^2+70x^4y^4-28x^2y^6+y^8\right)\left(19z^2-r^2\right)R_n \\
n^{(16)}  = n_{-8\phantom{0}} &= \frac{\sqrt{12155}}{32}\,N_n\,xy\left(x^2-y^2\right)\left(x^4-6x^2y^2+y^4\right)\left(19z^2-r^2\right)R_n \\
n^{(17)}  = n_{+9\phantom{0}} &= \frac{\sqrt{461890}}{256}\,N_n\,x\left(x^2-3y^2\right)\left(x^6-33x^4y^2+27x^2y^4-3y^6\right)zR_n \\
n^{(18)}  = n_{-9\phantom{0}} &= \frac{\sqrt{461890}}{256}\,N_n\,y\left(3x^2-y^2\right)\left(3x^6-27x^4y^2+33x^2y^4-y^6\right)zR_n \\
n^{(19)}  = n_{+10}           &= \frac{\sqrt{92378}}{512}\,N_n\left(x^2-y^2\right)\left(x^8-44x^6y^2+166x^4y^4-44x^2y^6+y^8\right)R_n \\
n^{(20)}  = n_{-10}           &= \frac{\sqrt{92378}}{256}\,N_n\,xy\left(x^4-10x^2y^2+5y^4\right)\left(5x^4-10x^2y^2+y^4\right)R_n
  \end{aligned}
$$
