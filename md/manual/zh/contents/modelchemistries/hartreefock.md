```{index} Hartree-Fock Theory (HF)
```

(sec:essentialelements.hartreefock)=
# 哈特里-福克理论（Hartree Fock Theory）

哈特里-福克（Hartree-Fock, HF）方法{cite}`hartree1928hf, slater1929spectra, fock1930hf`是一种基本的*从头算*（*ab-initio*）量子力学方法，用于在平均场理论（mean field theory）框架内近似多体电子波函数。许多后哈特里-福克（post-Hartree-Fock）方法（如耦合簇（Coupled-Cluster）方法）通常采用 HF 参考波函数。

通过简单的输入关键词 `!HF` 即可调用基本的哈特里-福克计算：

```orca
! HF
```

也可以通过 `%method` 块来调用：

```orca
%method
   method HF    # equivalent to method HFGTO
end
```

如果未另行指定，ORCA 默认使用 `def2-SVP` [基组](sec:essentialelements.basisset)。使用不同的 [RI 近似](sec:essentialelements.ri)可以极大地加速哈特里-福克计算。

:::{seealso} 另请参阅
ORCA 提供多种波函数（wavefunction）类型供选择，例如限制性（restricted, RHF）、非限制性（unrestricted, UHF）或非限制性开壳层 HF（unrestricted open-shell HF, ROKS）。这些选项记录在 {numref}`sec:modelchemistries.hftype` 中。HF 也是[杂化](sec:modelchemistries.dft.hybriddft)和[双杂化](sec:modelchemistries.dft.doublehybriddft)DFT 不可或缺的组成部分。
:::

:::{tip} 提示
Grimme 及其同事开发了一种基于 HF 的低成本方法，称为 [HF-3c](sec:modelchemistries.3cmethods.hf3c)，可用于非常大的体系。一些基于 HF 的[半经验方法](sec:modelchemistries.semiempirical)（如 AM1 或 PM3）也可用。
:::
