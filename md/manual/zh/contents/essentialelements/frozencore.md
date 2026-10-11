```{index} Frozen Core
```

(sec:essentialelements.frozencore)=
# 冻结核选项（Frozen Core Options）

冻结核（frozen core，FC）近似通常用于相关计算，其核心思想是在相关计算中忽略低能级核轨道中电子的相关效应。FC 近似以及每种元素的冻结核电子数可在 `%method` 模块块中调节。各元素的默认冻结核电子数列于 {numref}`table:Frozen-Core-Defaults`。

(table:Frozen-Core-Defaults)=
::::{list-table} 各元素默认冻结核电子数。
:header-rows: 0
:widths: 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
* - H
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - He
* - 0
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 0
* - Li
  - Be
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - B
  - C
  - N
  - O
  - F
  - Ne
* - 0
  - 0
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 2
  - 2
  - 2
  - 2
  - 2
  - 2
* - Na
  - Mg
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - Al
  - Si
  - P
  - S
  - Cl
  - Ar
* - 2
  - 2
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 10
  - 10
  - 10
  - 10
  - 10
  - 10
* - K
  - Ca
  - Sc
  - Ti
  - V
  - Cr
  - Mn
  - Fe
  - Co
  - Ni
  - Cu
  - Zn
  - Ga
  - Ge
  - As
  - Se
  - Br
  - Kr
* - 10
  - 10
  - 10
  - 10
  - 10
  - 10
  - 10
  - 10
  - 10
  - 10
  - 10
  - 10
  - 18
  - 18
  - 18
  - 18
  - 18
  - 18
* - Rb
  - Sr
  - Y
  - Zr
  - Nb
  - Mo
  - Tc
  - Ru
  - Rh
  - Pd
  - Ag
  - Cd
  - In
  - Sn
  - Sb
  - Te
  - I
  - Xe
* - 18
  - 18
  - 28
  - 28
  - 28
  - 28
  - 28
  - 28
  - 28
  - 28
  - 28
  - 28
  - 36
  - 36
  - 36
  - 36
  - 36
  - 36
* - Cs
  - Ba
  - Lu
  - Hf
  - Ta
  - W
  - Re
  - Os
  - Ir
  - Pt
  - Au
  - Hg
  - Tl
  - Pb
  - Bi
  - Po
  - At
  - Rn
* - 36
  - 36
  - 46
  - 46
  - 46
  - 46
  - 46
  - 46
  - 46
  - 46
  - 46
  - 46
  - 68
  - 68
  - 68
  - 68
  - 68
  - 68
* - Fr
  - Ra
  - Lr
  - Rf
  - Db
  - Sg
  - Bh
  - Hs
  - Mt
  - Ds
  - Rg
  - Cn
  - 
  - 
  - 
  - 
  - 
  - 
* - 68
  - 68
  - 68
  - 100
  - 100
  - 100
  - 100
  - 100
  - 100
  - 100
  - 100
  - 100
  - 
  - 
  - 
  - 
  - 
  - 
* - Lanthanides
  - 
  - 
  - La
  - Ce
  - Pr
  - Nd
  - Pm
  - Sm
  - Eu
  - Gd
  - Tb
  - Dy
  - Ho
  - Er
  - Tm
  - Yb
  - 
* - 
  - 
  - 
  - 36
  - 36
  - 36
  - 36
  - 36
  - 36
  - 36
  - 36
  - 36
  - 36
  - 36
  - 36
  - 36
  - 36
  - 
* - Actinides
  - 
  - 
  - Ac
  - Th
  - Pa
  - U
  - Np
  - Pu
  - Am
  - Cm
  - Bk
  - Cf
  - Es
  - Fm
  - Md
  - No
  - 
* - 
  - 
  - 
  - 68
  - 68
  - 68
  - 68
  - 68
  - 68
  - 68
  - 68
  - 68
  - 68
  - 68
  - 68
  - 68
  - 68
  - 
:::: 

对于含重元素的体系，核电子的轨道能量可能高于某些较轻元素价层分子轨道（MO）的能量。在这种情况下，核电子可能被纳入相关计算，最终导致相关能出现较大误差。为避免这一问题，程序会检查 MO 的排序：核区域中所有能量较低的 MO 是否都具有核电子特征，即是否高度定域在各个原子上？对于后（CAS）SCF 计算（post-(CAS)SCF），该检查始终在 SCF 计算之后和初始猜测（initial guess）之后各进行一次（因为使用 `!NoIter` 时可能跳过 SCF）。对于其他类型的计算，该检查默认关闭，但可以在 `%method` 模块块中用 `CheckFrozenCore` 关键字开启。如果在价层区域发现了核轨道，而在核区域发现了更离域的轨道，则相应的 MO 对会被交换。这一行为可以用 `CorrectFrozenCore` 关键字关闭。

```orca
%method 
  FrozenCore FC_ELECTRONS #Freeze all core electrons
             FC_EWIN      #Freeze selected core electrons via an energy window
                          #e.g. for MP2: %mp2 EWin EMin,EMax      
             FC_NONE      #No frozencore approximation 
             -n           #Freeze a total of n electrons

  NewNCore Bi 68 end      #Set the number of core electrons for Bi to 68
  CheckFrozenCore   true  #Check whether frozen core orbitals are ordered correctly
                          #Default: true only for post-(CAS)SCF calculations
  CorrectFrozenCore true  #Whether to rotate valence orbitals out of the
                          #core region
end
```

:::{admonition} 注意
:class: note
-   FrozenCore 选项适用于所有后 Hartree-Fock 方法。

-   若希望包含所有电子，只需插入 `!NoFrozenCore` 关键字。对于 MP2：在梯度计算或几何优化中不允许使用冻结虚轨道！

-   若使用了 ECP（赝势），NewNCore 的数值还必须包含由 ECP 所代表的电子。例如，若某元素在 ECP 中有 60 个电子，另外还有 8 个电子需要在相关计算中冻结，则 NewNCore 应设为 68。

-   在 ORCA 中我们采用较为保守的冻结核设置，即在相关处理中包含大量电子。因此，我们建议在所有情况下都使用经过适当优化的相关函数（correlating basis functions），例如 cc-pwCVXZ 基组。

-   对于 DLPNO 计算，核-核与核-价相关所用的虚空间默认会进行调整，详见章节 {ref}`sec:modelchemistries.mdci.dlpnocorepno`。

-   一般而言，`NewNCore` 仅在使用 `FC_ELECTRONS` 的计算中起作用。在使用 DLPNO 近似（DLPNO-NEVPT2 除外）的计算中，`NewNCore` 在其他情况下同样起作用，详见章节 {ref}`sec:modelchemistries.mdci.dlpnocorepno`。

-   双杂交密度泛函（double-hybrid density functional，见章节 {ref}`sec:modelchemistries.dft.doublehybriddft`）计算中，微扰部分默认使用 FrozenCore 选项，与 MP2 的情况相同。
:::
