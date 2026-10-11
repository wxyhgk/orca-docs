---
title: 并行运行计算
source: https://www.faccts.de/docs/orca/6.1/tutorials/first_steps/parallel.html
---

# 并行运行计算

ORCA 借助 [OpenMPI](https://www.open-mpi.org/) 可以在多个处理器上运行
（ORCA 6 推荐的版本是 4.1.6）。安装它并设置 `PATH` 和 `LD_LIBRARY_PATH` 变量之后（那是什么？[设置 PATH 变量](../first_steps/trouble_install.md#path-variable)），您只需使用 PAL 关键词即可并行运行。例如，使用四个处理器的计算需要：

```text
!HF def2-SVP PAL4
```

对于超过八个（`!PAL8`）或恰好 16 个（`!PAL16`）处理器的情况，则必须使用 `%pal` 块中显式的 `NProcs` 设置：

```text
!HF def2-SVP

%pal 
   NProcs 28 
end
```

并行运行计算时，请始终使用 ORCA 的完整路径：

```text
./full/path/to/orca input.inp
```

> **重要**
> 始终安装下载部分所指示的 OpenMPI 版本！
