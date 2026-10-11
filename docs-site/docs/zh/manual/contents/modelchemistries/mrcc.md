

<a id="sec:modelchemistries.mrcc"></a>
# 任意阶耦合簇理论（MRCC 接口）
各种高阶理论（CC3、CISDT、CCSDTQ、MP4）均通过[自动代码生成](autoci.md#sec:modelchemistries.autoci)实现。此外，ORCA 还提供了通往 Kallay 强大的 MRCC 程序的接口。该程序需单独获取。此接口仅限于单点能计算，但可用于刚性扫描计算或数值频率计算。

该接口的使用很简单：

```mol
title: structure 1
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
2
structure (0 1)
F             0            0            0
H             0            0         0.95
--- input ---
#
# Test the MRCC code of Mihael Kallay
#
! cc-pVDZ Conv SCFConv10 UseSym 

%mrcc method   "CCSDT"
      ETol     9
      end 

* xyz 0 1
F 0 0 0
H 0 0 0.95
*
```

Method 字符串可以是以下任意一种：

```orca
# The excitation level specification can be anything
# like SD, SDT, SDTQ, SDTQP etc.
 %mrcc method   "CCSDT"
                "CCSD(T)"
                "CCSD[T]"
                "CCSD(T)_L"  (the lambda version)
                "CC3"
                "CCSDT-1a"
                "CCSDT-1b"
                "CISDT"
```

当然，用这套代码来做 CCSD、CCSD(T) 或 CISD 并不是个好主意。它真正的威力在于执行更高阶的计算。目前该接口还无法进行开壳层（open-shell）计算。

