
(sec:modelchemistries.rpa)=
# 无规相近似（Random Phase Approximation, RPA）
```{index} Random Phase Approximation, RPA
```

无规相近似（random phase approximation, RPA）是一种颇为不同的 DFT 方法，它基于频率依赖的响应函数（response function）。它的计算量高于标准 DFT（与 RI-MP2 同一量级），但具有许多吸引人的特点，尤其是其良好至优秀的精度，同时本质上是非经验的（non-empirical）。将 RPA 引入量子化学领域的奠基性工作归功于 Furche，其基础是 Langreth 和 Perdew 的原始工作。ORCA 中的实现紧密遵循 Görling 及其合作者的工作，我们也在此衷心感谢他们在实现过程中提供的帮助。

RPA 能量使用某组输入轨道和轨道能量进行计算（实践中推荐使用 PBE 轨道和能量）。计算通过在频率上进行数值积分（numerical integration）来完成：

$$E_{RPAC} \approx - \frac{\pi}{2}\sum_{g}^{}{w_{g}\sum_{K}^{}h_{K}}\left( \omega_{g} \right)$$

$$h_{K}(\omega) = - log\left( 1 + x_{K}(\omega) \right) + x_{K}(\omega)$$

其中 $x_{K}$ 是 Kohn-Sham 响应矩阵在辅助拟合基组（auxiliary fitting basis，即 '/C' 类型的辅助基组）中表达的负本征值。

$$X_{KL}(\omega) = \sum_{i}^{}{\left( \mathbf{X}^{i} \right)^{T}\mathbf{Y}^{i}}(\omega)$$

其中

$$X_{aK}^{i}\mathbf{=}\left( ia|K \right)$$

$$Y_{aK}^{i}(\omega)\mathbf{=}\left( ia|K \right)\lambda_{ia}(\omega)$$

$$\lambda_{ia} = f_{\sigma}\frac{\epsilon_{i} - \epsilon_{a}}{\left( \epsilon_{i} - \epsilon_{a} \right)^{2} + (\omega)^{2}}$$

这里 $\epsilon_{i},\epsilon_{a}$ 是来自 SCF 计算的占据轨道和虚轨道能量；$(ia | K)$ 是 MO 基组下的三指标电子排斥积分；对于闭壳层（closed-shell）态 $f_{\sigma} = 4$，对于自旋非限制（spin-unrestricted）计算 $f_{\sigma} = 2$。数值积分采用 Gauss-Legendre 求积（quadrature）完成，所用权重和频率由下式给出：

$$w_{g} = w_{g0}\frac{5}{\left( 1 - \omega_{g0} \right)^{2}}$$

$$\omega_{g} = \frac{5}{2}\left( \frac{1 + \omega_{g0}}{1 - \omega_{g0}} \right)$$

其中 $w_{g0}$ 和 $\omega_{g0}$ 是映射到 -1 至 1 区间上的 Gauss-Legendre 权重和根。

在 ORCA 中使用 RPA 非常直接

```orca
! PBE RPAC def2-SVP def2/J def2-SVP/C
# we need a /C basis for RPAC and the /J basis for PBE

%method RPACNPoints 50  # Number of numerical integration points (def=50)
end
```

:::{note} 注意
-   这是一个试验性（pilot）实现，仅提供闭壳层和自旋非限制能量。梯度通过数值方式计算，密度矩阵取自底层 DFT 计算，并非真正的 RPA 密度。
-   该方法**不**提供激发态（excited states）和响应性质（response properties）。
-   该方法需要一次标度为 O(N$^4$) 的积分变换（integral transformation），以及大约 50 次对响应矩阵（维度为 NAUXC）的对角化。对于较大的分子，这可能变得相当昂贵。
:::

```{bibliography} ../../bibliography.bib
:list: enumerated
:filter: False

LANGRETH19751425
FurchePhysRevB2001
FurcheJCP2008
TrushinJCP2021
```
