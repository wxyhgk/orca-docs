

<a id="sec:essentialelements.numericalgradients"></a>
# 数值梯度（Numerical Gradients）

如果没有解析梯度（analytic gradient），可以直接通过以下方式请求
数值梯度（numerical gradient）：

```orca
! NumGrad
```

例如下例所示：

```orcainput
!CCSD(T) TZVPP
!Opt NumGrad

* int 0 1
C 0 0 0  0   0   0
O 1 0 0  1.2 0   0
H 1 2 0  1.1 120 0
H 1 2 3  1.1 120 180
*
```

!!! note "注意"
    -   请注意，数值梯度的计算代价相当高。一次梯度计算所需的时间等于
        6 $\times$（原子数）$\times$（一次单点计算的时间）。

    -   数值梯度可以在多进程运行（multi-process run）中进行，
        把每个位移作为一次并行计算来处理（见
        [sec:essentialelements.parallel.calling](#sec:essentialelements.parallel.calling) 一节）。

此外，还可以修改数值微分（numerical differentiation）的各种设置：

```orca
%numgrad
  CentralDiff true # You should use two-sided numerical differentiation, but it 
                   # is possible to switch to one-sided numerical differentiation.
  DX 0.005         # Increment in Bohr for the differentiation.
  TransInvar  true # Take advantage of translation invariance
  Accuracy       2 # 2,4,6,8 - number of points used for numerical differentiation
end
```

!!! tip "提示"
       - 更高精度阶数的数值梯度会比常规（两点）数值梯度昂贵得多，
       因为它需要进行两倍（三倍或四倍）的位移计算。
       - 选择高于 `4` 的精度通常是不划算的
       （计算时间的增加相当可观，而精度的提升却很有限）
       - 对 DFT 而言，使用高于 `4` 的精度甚至可能适得其反——
       导致数值噪声的累积。
       - 强烈不建议在使用 RIJCOSX（或其他会引入额外积分格点的方法）时
       计算更高精度阶数的梯度，因为数值噪声会超过增加格点数所带来的精度收益。
       - 更高精度阶数的数值梯度不能与 `CentralDiff false` 一起使用

