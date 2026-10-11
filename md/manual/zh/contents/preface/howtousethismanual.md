(sec:preface.howtousethismanual)=
# 如何使用本手册

ORCA 手册已历经数十年的积累，所有开发者都竭尽全力记录和描述 ORCA 的各项功能。从 ORCA 6.0 到 ORCA 6.1，本手册经历了一次重大重构。您现在所看到的成果过去是、现在仍然是一个巨大的团队协作结晶，它既应满足几乎没有理论背景的绝对初学者的需要，也应满足经验丰富的开发者的要求。

:::{admonition} 请通过反馈帮助我们
:class: note

在为 ORCA 6.1 进行手册的首次重构时，我们做了大量改动，希望能提升手册的可读性与整体质量。然而，这只是个开始，我们欢迎您通过 [ORCA 论坛](https://orcaforum.kofo.mpg.de/app.php/portal) 提出任何建设性反馈，以帮助我们在未来进一步改进。
:::

新的结构以[快速入门指南](../quickstartguide/index_quickstartguide.md)和
[安装指南](sec:installation)开篇，让所有人都能顺利上手。整体结构的编排顺序如下：
首先概述用户在执行标准计算时需要了解的 [ORCA 基本要素](../essentialelements/index_essentialelements.md)，例如
[如何构建输入文件](sec:essentialelements.coordinates)、可用的
[基组（basis set）](sec:essentialelements.basisset)与算法等。接下来，我们介绍可用于计算能量、结构和性质的各种
[电子结构方法](../modelchemistries/index_modelchemistries.md)，
涵盖从 [Hartree-Fock](sec:modelchemistries.hftype) 和 [DFT](sec:modelchemistries.dft)
直到高级从头算（ab initio）方法。下一章聚焦于[结构与反应性](../structurereactivity/index_structurereactivity.md)，包括
优化[几何结构](sec:structurereactivity.optimization)、寻找
[过渡态（transition state）](sec:structurereactivity.optimization.transitionstate)
以及在各种设定下计算相对（自由）能的全部方法。
[分子光谱与性质](../spectroscopyproperties/index_spectroscopyproperties.md)涵盖一旦确定结构后即可计算的所有内容，范围从
密度与波函数分析到基态与激发态性质，
直至复杂的高阶性质，例如 [MCD](sec:spectroscopyproperties.mcd)。
最后几节讨论复杂任务中的重要功能，例如运行
[分子动力学（molecular dynamics）](../moleculardynamics/index_moleculardynamics.md)、
[多尺度方法](../multiscalesimulations/index_multiscalesimulations.md)，以及使用例如
[compound](sec:workflowsautomatization.compound) 脚本语言来编排
[ORCA 自动化工作流](../workflowsautomatization/index_workflowsautomatization.md)。最后同样重要的是，我们还介绍了可用于后处理的重要
[实用工具]，以及关于
[ORCA 架构](../orcaarchitecture/index_orcaarchitecture.md)的一些技术说明。

大多数章节都以简短的理论提要开篇，并附有参考文献和一些简单示例以帮助您入门；更详细的内容，例如关键词列表和高级示例，通常放在章节的后面部分。

我们希望您觉得本手册有用，也欢迎您在 [ORCA 论坛](https://orcaforum.kofo.mpg.de/app.php/portal) 上在线反馈意见。
