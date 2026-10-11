```{index} 图形用户界面（GUI）
```

(sec:quickstartguide.gui)=
# 图形用户界面（GUI）

目前，ORCA 开发者尚未开发原生的图形用户界面（graphical user interface, GUI）。不过，有若干程序提供了创建 ORCA 输入文件以及读取和可视化 ORCA 输出文件的功能。{numref}`tab:quickstartguide.gui.programlist` 概述了一些有用的程序，另外在 [ORCA 教程网站](https://www.faccts.de/docs/orca/6.0/tutorials/) 上也可以找到一些应用。

:::{warning}
上述程序均非由 ORCA 团队开发。因此我们无法保证其功能。如遇问题或有功能需求，请联系相应程序的开发者。
:::


:::{raw} latex
\begingroup
\footnotesize
:::

:::{tabularcolumns} \Y{0.15}\Y{0.25}\Y{0.6}
:::
(tab:quickstartguide.gui.programlist)=
:::{flat-table} 可用作 ORCA 图形界面的部分程序。
:header-rows: 1
:class: longtable
:class: footnotesize

   * - 程序
     - 平台
     - 说明
   * - [Avogadro 2](https://two.avogadro.cc/index.html)
     - Windows, Linux, MacOS
     - 三维分子构建器，创建 ORCA 输入文件，可视化 ORCA 输出。
   * - [ChimeraX](https://www.cgl.ucsf.edu/chimerax/)
     - Windows, Linux, MacOS
     - 可视化 ORCA 输出。功能非常强大的可视化套件。[SEQCROW](https://github.com/QChASM/SEQCROW) 插件非常有用，可从 `Tools/More`$\rightarrow$`Tools` 菜单下载。
   * - [Chemcraft](https://www.chemcraftprog.com/)
     - Windows, Linux
     - 三维分子构建器，创建 ORCA 输入文件，可视化 ORCA 输出。对于 Linux，我们建议通过虚拟机使用 Windows 版本。
:::
:::{raw} latex
\endgroup
:::

:::{note}
Avogadro 1 的 ORCA 增强版本未针对 ORCA 6 及更高版本进行进一步开发或测试！我们建议改用 Avogadro 2。
:::
