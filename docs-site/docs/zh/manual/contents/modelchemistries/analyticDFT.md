<a id="sec:modelchemistries.analyticDFT"></a>
# 解析密度泛函理论（Analytic Density Functional Theory, ADFT）

这一后来被称为"解析密度泛函理论（analytic density functional theory, ADFT）"的方法是 DFT 的一种变体，它避免了极为常见的数值积分（numerical integration）的使用。早期的网格 DFT（grid DFT）方法依赖于对密度矩阵（density matrix）进行对角化，将 DFT 泛函应用于密度矩阵的本征值，然后再进行反变换。这些方法虽然可行，但已被放弃，转而采用数值积分。

ORCA 提供了一种替代方法，不过该方法目前仍仅限于所有密度泛函中最基本的一种，即哈特里-福克-斯莱特（Hartree-Fock Slater, HFS）泛函，或其略微参数化后的形式——X-Alpha 方法。该方法基于将库仑势（Coulomb potential）和交换势（exchange potential）分别拟合到各自的辅助基组（auxiliary basis set）上。对于库仑相互作用，这就是广为人知的 RI-J 近似形式。对于交换作用，由于斯莱特交换（Slater-exchange）对密度的非线性依赖关系，ADFT 的构造建立在一种相关但更为棘手的推导之上。

交换能为：

$$
E_{X}^{\sigma} = - \frac{3}{4}\left( \frac{6}{\pi} \right)^{\frac{1}{3}}\in t_{}^{}{\rho_{\sigma}^{4/3}\left( r \right)}
$$

由此得到交换势：

$$
V_{X}^{\sigma}\left( r \right) = - \left( \frac{6}{\pi} \right)^{\frac{1}{3}}\rho_{\sigma}^{1/3}\left( r \right)
$$

$$
C_{X} = - \left( \frac{6}{\pi} \right)^{\frac{1}{3}} = - 1.24\ldots
$$

将$C_{X}$ 替换为${\frac{3}{2}\alpha C}_{X}$ 即得到 X-Alpha 方法。其中$\alpha$ 是一个经验参数，默认值为 2/3，以便还原出 HFS 方法。然而，经验表明 2/3 到 1 之间的取值更为合适，其中 0.7 是被广泛接受的默认值。

接下来需要处理这个奇次幂律，所用技术由 Cook 以及 Dunlap 等人发展而来。其思路是将${\rho_{\sigma}(r)}^{\frac{1}{3}}$ 本身在另一组辅助基组中展开：

$$
{\rho_{\sigma}\left( r \right)}^{1/3} = \sum_{K}^{}{a_{K}^{\sigma}A_{K}(r)}
$$

事实表明我们还需要（或者说未必需要但希望得到）：

$$
{\rho_{\sigma}\left( r \right)}^{2/3} = \sum_{K}^{}{b_{K}^{\sigma}B_{K}(r)}
$$

函数 {A} 和 {B} 是未收缩的交换辅助基函数（uncontracted exchange auxiliary basis functions）。这些辅助基组最简单的选取方式是从库仑拟合基组（Coulomb fitting basis set）导出，可选地对最大角动量加以限制。另一种选择是使用程序提供的、目前有四种尺寸递增的拟合基组之一，称为 XFIT/1 到 XFIT/4。

基于理论论证，这些拟合基组的指数采用了不同的缩放方式。A 基组的指数按因子 1/3 缩放，而 B 基组的指数按 2/3 缩放。Dunlap 指出，仅对 s 函数的指数进行缩放就已足够，我们采纳了这一建议，但并未观察到与对所有指数进行缩放相比有明显差异。

拟合系数 {a} 和 {b} 的确定会导出一组非线性方程，例如可通过 Newton-Raphson（牛顿-拉夫森）方法求解。这些方程也可以用数值积分更高效地求解，但这就违背了该方法学的初衷。需要满足的方程为：

$$
\frac{\partial E}{\partial a_{K}^{\sigma}} = C_{X}\left\{ \sum_{\mu\nu}^{}{P_{\mu\nu}^{\sigma}(\mu\nu A_{K})} - \sum_{LM}^{}{a_{L}^{\sigma}b_{M}^{\sigma}(A_{K}A_{L}B_{M})} \right\}
$$

$$
\frac{\partial E}{\partial b_{M}^{\sigma}} = \frac{1}{2}C_{X}\left\{ - \sum_{KL}^{}{a_{K}^{\sigma}a_{L}^{\sigma}\left( A_{K}A_{L}B_{M} \right)} + \sum_{N}^{}{b_{N}^{\sigma}(B_{M}B_{N})} \right\}
$$

其中$(A_{K}A_{L}B_{M})$ 是三中心重叠积分（3-center overlap integrals），$\mu,\nu$ 是基函数，$P^{\sigma}$ 是自旋$\sigma = \alpha,\beta$ 的密度矩阵。可以将其整理为如下形式：

$$
\left( H(a)^{AB} \overline{S}^{- 1} H(a)^{AB+} \right) a
= P^{X}
$$

其中

$$
P_{K}^{X;\sigma} = \sum_{\mu\nu}^{}P_{\mu\nu}^{\sigma}(\mu\nu A_{L})
$$

$$
{\overline{S}}_{MN} = (B_{M}B_{N})
$$

$$
H_{KM}^{AB;\sigma} = \sum_{L}^{}{a_{L}^{\sigma}\left( A_{K}A_{L}B_{M} \right)}
$$

需要对其求解$a$。随后由下式得到$b$：

$$
b = \overline{S}^{- 1} H(a)^{AB+} a
$$

这基本上就是 ORCA 实现中所遵循的流程。我们为三中心重叠积分编写了优化的代码。

ORCA 中的实现涵盖闭壳层和自旋非限制性（spin-unrestricted）能量、解析几何梯度（analytic geometry gradients）、响应性质（response properties）与激发能（excitation energies），以及数值 Hessian 矩阵。该实现的效率特点是：能量计算比数值积分慢，而所有其他步骤的执行速度更快。

ADFT 提供的一个独特机会是能够对分子中的每个原子分别缩放交换作用。这样做似乎是有依据的，因为针对原子的 X-Alpha 研究表明，最优的$\alpha$ 值会随原子不同而变化。稍加推导即可发现，可以通过如下方式对交换计算所用的密度矩阵进行缩放来实现这一点：

$$
P_{\mu_{A}\nu_{B}}^{\sigma} \rightarrow P_{\mu_{A}\nu_{B}}^{\sigma}\left( {\frac{3}{2}\alpha_{A}} \right)^{3/8}\left( {\frac{3}{2}\alpha_{B}} \right)^{3/8}
$$

除了赋予全局值 0.7 之外，Alpha 值还可以通过多种其他方式选取。例如，可以将 alpha 值拟合到原子哈特里-福克能量或原子耦合簇能量上；也可以通过优化使其重现分子能量学性质。

在 ORCA 中使用 ADFT 很简单：

```orca
! ADFT def2-SVP def2/J XFit/3
# or ADFT(XAlpha), ADFT(HF), ADFT(CC)
# default parameters for HF are H-Kr
# default parameters for CC are H-Zn
# XFIT/1 -- XFIT/4 exists but only /3 and /4 are recommended

%method ADFTNRTol 1e-9           # tol. for NR equation solution (def=1e-9)
        ADFTNRMaxIter 6          # max no of NR iterations (def=15)
        ADFTLmaxAuxJ  5          # max L allowed in the AUXJ basis (def=3)
        ADFTLmaxAuxX  5          # max L allowed in the AUXX basis (def=2)
        ADFTXAlpha  [36] 0.71337 # array with alpha values for each element
end
```

!!! note "注意"
    -   ADFT 实际上仅限于 HFS/X-Alpha 方法。输入任何其他泛函的名称都没有意义，它将被忽略。这是由交换项的拟合方式所决定的——该拟合方式高度依赖于这一特定泛函，而对于其他泛函，整套理论将完全不同。
    -   该实现是实验性的。其动机在于这一构造在理论上的优美性，以及在早期计算化学中，用户从该方法获得了大量实际收益的事实。因此，这是一场"回归本源"式的探索，其理念是或许能将无网格（grid free）DFT 带向新的高度。

**相关论文（Relevant Papers）：**

- Neese, F. 2025, in preparation 
