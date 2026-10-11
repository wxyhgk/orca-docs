---
title: 内存设置
source: https://www.faccts.de/docs/orca/6.1/tutorials/first_steps/memory.html
---

# 内存设置

某些计算，特别是使用基于波函数的相关方法（wave-function based correlation methods）的计算，可能非常消耗内存，因此控制 ORCA 计算的内存设置非常重要。

在 ORCA 中，设置每个处理核心内存（单位为兆字节，MB）最简单的方式是通过全局 `%MaxCore` 变量。例如，在 4 核运行中设置 `%MaxCore 2000`（参见 [ORCA 中的并行计算](../first_steps/parallel.md#sec-firststeps-parallel)）将预留 8000 MB 内存。

```text
%MaxCore 2000
```

> **关于 ORCA 中内存的说明**
> 1. `%MaxCore` 以兆字节（MB）为单位设置**每个处理核心**的内存。
> 2. 内存以**兆字节**为单位给出
> 3. 此内存设置始终指向主要工作区域，因此 **ORCA 实际占用的内存可能超过** `%MaxCore` 所定义的值！因此，只应分配可用内存的约 80%。
> 4. 一些内存消耗大的操作在内存不足时会耗时更长，而另一些操作在 `%MaxCore` 不足时会完全中止。
> 5. ORCA 的默认内存为 4096 MB，即 `%MaxCore 4096`

## 示例 1：`Not enough memory available!`

自洽场（self-consistent field）模块是可用内存不足时会立即中止的模块之一。例如，将 `%MaxCore` 设置为 1 MB，对于使用 PBE 密度泛函（DFT）和大型四重-$\zeta$ 基组 def2-QZVPPD 的双氢分子 SCF 计算来说是不够的。

```orcainput
!PBE def2-QZVPPD

%MaxCore 1

*xyz 0 1
H 0 0 0
H 1 1 1
end
```

计算将中止，并给出报告给定内存和估计所需内存的错误消息。

```orca
 Error  (ORCA_SCF): Not enough memory available!
                    Memory available for SCF calculation:          1.0 MB
                    Memory needed (estimated)           :          5.2 MB
       ====>        Please increase MaxCore to more than:          5.2 MB

Error (ORCA_SCF): ... aborting the run
```

现在，如果我们把给 ORCA 的内存增加到默认值 4096 MB（这远远超过这个非常小的计算所需），ORCA 将成功运行。

```orcainput
!PBE def2-QZVPPD

%MaxCore 4096

*xyz 0 1
H 0 0 0
H 1 1 1
end
```

ORCA 还会在输出中报告每个计算部分实际使用的内存。

```text
Maximum memory used throughout the entire STARTUP-calculation: 11.2 MB
[...]
Maximum memory used throughout the entire GUESS-calculation: 5.4 MB
[...]
Maximum memory used throughout the entire LEANSCF-calculation: 4.0 MB
[...]
Maximum memory used throughout the entire PROP-calculation: 2.8 MB
[...]
                             ****ORCA TERMINATED NORMALLY****
```
