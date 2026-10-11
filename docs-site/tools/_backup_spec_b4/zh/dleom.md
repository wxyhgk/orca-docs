

<a id="sec:spectroscopyproperties.dleom"></a>
# 通过基于 PNO 的耦合簇方法计算激发态（Excited States via PNO-based coupled cluster）

尽管 DLPNO-CC 近似在基态计算中取得了成功，
但将 PNO 用于激发态的效果却不尽如人意。为激发态定义一种
既能保持基态计算中速度与精度平衡、又可行的 PNO 方案并非易事。
作为一种折中方案，基态 DLPNO 量被变换回正则基（canonical basis），
并在正则 EOM 例程中使用。这一处理是合理的，因为
EOM-CCSD 或 STEOM-CCSD 方法的主要瓶颈在于基态计算。
用 MP2 振幅近似基态 CCSD 振幅也是可行的，如 EOM-CCSD(2) 方法中所做的那样。
然而，这种方法并不可靠，当参考 HF 波函数无法为基态波函数
提供合理的零阶近似时，可能导致很大的误差。请注意，这里描述的
反变换 PNO 方案（bt-PNO）同时适用于开壳层（UHF（QROs）或 ROHF 参考）
和闭壳层（RHF 参考）体系。

<a id="sec:spectroscopyproperties.dleom.general"></a>
## 一般性描述（General Description）

将基态 DLPNO-CCSD 振幅反变换回虚拟空间包含三个步骤。
首先将 PNO 基中的振幅转换为 PAO 基，然后转换为原子轨道（AO）基，
最后转换为正则 MO 基[640]。例如，在闭壳层情形下，有

$$

d_{\tilde{\mu}\tilde{a}_{ij} }^{ij}T^{ij}_{\tilde{a}_{ij}\tilde{b}_{ij} }d_{\tilde{b}_{ij}\tilde{\mu} }^{ij} \Rightarrow
L_{\mu\tilde{\mu} }^{ij}T^{ij}_{\tilde{\mu}\tilde{\nu} }L_{\tilde{\nu}\nu}^{ij} \Rightarrow
C_{a\mu }^{ij}T^{ij}_{\mu\nu}C_{\nu b}^{ij} \Rightarrow
T^{ij}_{ab},

$$

$$

d_{\tilde{\mu}\tilde{a}_{ii} }^{i}T^{i}_{\tilde{a}_{ii} } \Rightarrow
L_{\mu\tilde{\mu} }^{i}T^{i}_{\tilde{\mu} } \Rightarrow
C_{a\mu }^{i}T^{i}_{\mu} \Rightarrow
T^{i}_{a},

$$

AO 基函数记为 $\mu,\nu,\ldots$，
而 $\tilde{\mu},\tilde{\nu},\ldots$ 指 PAO。缺失的电子对
用 MP2 振幅处理。若将所有阈值设为零，反变换后的振幅
与正则 RI-EOM-CCSD 的振幅完全一致。另一方面，当所有阈值
被收紧到无穷紧时，得到的则是 EOM-CCSD(2) 结果。这种基于 PNO 的
激发态方法适用于所有 EOM-CCSD 变体以及 STEOM-CCSD，
可用于开壳层和闭壳层体系。

下面列出了影响基于 DLPNO-CCSD 的激发态计算的所有参数：

```orca
%mdci
#bt-PNO-EOM and STEOM parameters - defaults displayed
DoEOMMP2 true        # MP2 correction for missing pairs
DoRECAN  true        # recanonicalization of the occupied
                     # orbitals before the excited state calculation
                     #(only relevant for the RHF implementation)
end
```

<a id="sec:spectroscopyproperties.dleom.energy"></a>
## 参考态能量（Reference State Energy）

需要指出的是，基于 PNO 的 EOM-CCSD 或 STEOM-CCSD 的参考能量
与收敛的基态 DLPNO-CCSD 计算所打印的能量略有不同，因为前者
包含了对各种截断量的微扰修正。

```
----------------------
COUPLED CLUSTER ENERGY
----------------------

E(0)                                       ...   -113.913498239
E(CORR)(strong-pairs)                      ...     -0.401457078
E(CORR)(weak-pairs)                        ...     -0.000339627
E(CORR)(corrected)                         ...     -0.401796705
E(TOT)                                     ...   -114.315294944
```

在 bt-PNO-EOM-CCSD 方案中，参考态的类 CI 激发态处理由
反变换后的 DLPNO 振幅（弱对则用 MP2 振幅）定义。与这组振幅
相对应的能量打印在 EOM 计算的开头。

```
Dressing integrals for EOM-CCSD            ... 
Reference state energy for EOM-DLPNO-CCSD     ...   -114.314954945

done (    0.4)
```

因此，要计算激发（电离或电子附着）态的总能量，需要在
bt-PNO-EOM-CCSD 中将激发能加到参考态能量上。

<a id="sec:spectroscopyproperties.dleom.localorbitals"></a>
## 局域轨道的使用（Use of Local Orbitals）

局域轨道的使用使得在 EOM-CC 和 STEOM-CC 的 Davidson 对角化过程中
难以追踪特定的试探向量（guess vector）。因此，建议在
基态 DLPNO-CCSD 计算之后通过将 DoRECAN 设为 true 对占据轨道进行
重新正则化（recanonicalize）（这只对闭壳层 RHF 实现有效）。
需要注意的是，重新正则化不会影响 EOM-CCSD 能量。
然而，STEOM-CC 能量对轨道旋转不是不变的，在局域轨道和
正则轨道之间可能略有差异。在开壳层 bt-PNO 实现中，采用的是
另一种流程：在进行反变换和激发态计算之前，所有量都被
变换到离域基（delocalized basis）。

<a id="sec:spectroscopyproperties.dleom.tips"></a>
## bt-PNO 计算的一些提示与技巧（Some tips and tricks for bt-PNO calculations）

-   采用 tightPNO 设置的 bt-PNO 方案所得结果与正则 EOM-CCSD 数值
    相差在 0.01 eV 以内，而计算成本仅为其一小部分[Dutta2016PNO](../../bibliography.md)。
    因此，使用 bt-PNO 方案始终优于正则计算。

-   对于 RHF 参考，应在 mdci 块输入中设置 'DLPNOLINEAR true'
    和 'NEWDOMAINS true'，以使用 2015 年的完全线性标度实现；
    该实现比 bt-PNO 方案中默认使用的 2013 年实现更为稳健。

-   bt-PNO-EOM（仅 RHF）和 bt-PNO-STEOM
    （RHF、UHF（QROs）或 ROHF）中的跃迁矩只能通过
    线性近似获得。
