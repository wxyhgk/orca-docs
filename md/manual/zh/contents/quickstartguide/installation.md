```{index} 安装
```

(sec:installation)=
# 安装
## 下载

ORCA 适用于 Linux、MacOS 和 Windows。相应的安装程序可从 [ORCA 论坛](https://orcaforum.kofo.mpg.de/app.php/dlext/) 下载（需注册）。

## 安装

在 Linux 和 MacOS 上，安装 ORCA 最便捷的方式是使用命令行安装程序。您需要下载一个 `.run` 文件，例如
`orca_6_1_0_linux_x86-64_shared_openmpi416.run`。
然后将该文件设为可执行，即打开终端，进入保存该文件的目录并输入：

`chmod a+x orca_6_1_0_linux_x86-64_shared_openmpi416.run`

之后您就可以直接执行该文件，例如

`./orca_6_1_0_linux_x86-64_shared_openmpi416.run`

安装程序会将 ORCA 安装到用户目录中，并设置包含 ORCA 目录的路径。*打开一个新窗口*后，即可按上述方式使用 ORCA。

安装程序还有几个额外选项，例如仅解压、交互式设置路径，以及通过选项设置路径：

```
  -i        : Set a different install path interactively
  -p <path> : Set a different install path
  -x        : Just extract
```

这些选项必须写在双横线（`--`）*之后*，例如

`./orca_6_1_0_linux_x86-64_shared_openmpi416.run -- -p /my/home/orca/dir`

在 Windows 上，安装程序包含在 zip 文件 `Orca6.1.0.Win64.zip` 中，必须先解压才能开始安装。
然后双击 `Orca6.1.0.Win64.exe` 并按照提示操作。如果选择 `typical`（典型）安装，则只复制 ORCA 的串行模块。
要同时安装 ORCA 的并行部分，请使用 `Custom`（自定义）或 `Full`（完全）安装。
ORCA 的默认目录是 `C:\Orca_6.1.0`，如有必要您也可以选择其他文件夹。
所需的环境变量会相应地进行设置。

此外，ORCA AUTOCI 可执行文件以 2 个不同的文件提供。`Orca6.1.0.Win64_autoci.zip` 包含用于串行执行的模块，`Orca6.1.0.Win64_autoci_msmpi10.zip` 用于并行执行。
请将这些 zip 文件解压到 ORCA 安装目录中。

打开一个新的命令窗口后，即可按上述方式使用 ORCA。

:::{note}
ORCA 主模块可通过 Windows 的 `Apps & features`（应用和功能）功能卸载，但 ORCA AUTOCI 模块必须手动删除。
:::

## 路径变量

ORCA 安装过程中只会添加或修改必要的环境变量。

在 Linux 上：
```
PATH	   : updated with the new orca installation directory
```

在 Windows 上：

```
  PATH	   : modified with the new orca installation directory`
  ORCADIR  : created or modified with the new orca installation directory`
  XTBEXE   : created or replaced with the xtb module path`
```

:::{note}
请注意，环境变量的更改只对新打开的命令窗口生效。
:::

## 如何安装 xtb 模块？

ORCA 的许多功能都与 xtb 模块相关。虽然 ORCA 有原生实现，但 Grimme 实验室的程序包也已集成到 ORCA 的工作流（workflow）中，因此建议安装它。
自 ORCA 6 起，在 Linux 和 Windows 上，xtb 7.6.1 版本已随 ORCA 的安装一同提供。
可执行文件可在 ORCA 安装目录（Linux）或 ORCA 目录的子目录（Windows）中找到。

如需更新或使用其他 xtb 版本，请从 Grimme 实验室的仓库
[Grimme lab's repository](https://github.com/grimme-lab/xtb/releases/tag/)
下载所需的 xtb 版本，并将 xtb 二进制文件复制到 ORCA 目录中，在 Linux 上将其重命名为 `otool_xtb`。
在 Windows 上，您必须将 XTBEXE 变量设置为指向 xtb 可执行文件本身。
```
  set XTBEXE=<path>xtb.exe
```
