

<a id="sec:essentialelements.stabilityanalysis"></a>
# SCF 稳定性分析（SCF Stability Analysis）

SCF 稳定性（SCF stability）可以指示当前 SCF 解是处于局域极小值（local
minimum）还是鞍点（saddle
point）。[SeegerPopleXVIIIStability,AhlrichsDFTStability](../../bibliography.md) 该功能适用于
RHF/RKS 和 UHF/UKS。对于后一种情况，如果检测到不稳定性
（instability），默认会使用新的非限制性起始轨道（unrestricted start
orbitals）重新启动 SCF。作为演示，考虑以下输入：

```orca
! BHLYP def2-SVP NORI

%scf
 guess hcore
 HFTyp UHF
 STABPerform true
end

* xyz 0 1 
h 0.0 0.0 0.0
h 0.0 0.0 1.4
*
```

HCORE 初始猜测会得到一个对称的/限制性的猜测，无法给出非限制性解。
其他初始猜测选项往往也是如此。关于稳定性分析的更多细节，
见 [sec:essentialelements.stabilityanalysis](#sec:essentialelements.stabilityanalysis) 一节。

SCF 稳定性分析会在 SCF 解所指示的点处计算电子 Hessian（electronic
Hessian，对轨道旋转而言），以确定 Hessian 的最低本征值
（eigenvalue）。如果发现一个或多个负本征值，则说明该 SCF 解对应于一个鞍点，
而不是分析所考虑空间中的真正局域极小值。一个典型的例子是双原子分子的拉伸键
（stretched bonds），此时初始猜测的对称性导致得到限制性解，
而不是通常更受青睐的非限制性解。理论上可以考虑多种空间
[SeegerPopleXVIIIStability](../../bibliography.md)。不过 ORCA 仅限于在 UHF/UKS 空间中分析
RHF/RKS，或在 UHF/UKS 空间中分析 UHF/UKS。因此，它仅适用于 DFT 和 HF 的
SCF 部分。[AhlrichsDFTStability](../../bibliography.md)
下文中用 HF 同时表示 HF 和 KS。考虑以下输入（除特别说明外，均显示默认值）：

```orca
! BHLYP def2-SVP NORI

%scf 
 guess hcore # for illustrative purposes only 
 HFTyp UHF # default based on spin multiplicity
 STABPerform true # default false
 STABRestartUHFifUnstable true # restart the UHF-SCF if unstable 
 STABNRoots 3                  # number of eigenpairs sought
 STABMaxDim 3                  # Davidson expansion space = MaxDim * NRoots
 STABMaxIter 100               # maximum number of Davidson iterations
 STABNGuess 4096               # size of initial guess matrix: 4096 x 4096
 STABDTol 0.0001               # convergence criterion from iteration to iteration
 STABRTol 0.0001               # convergence criterion max residual norm
 STABlambda +0.5               # mixing parameter 
 STABORBWIN -1, -1, -1, -1,  -1, -1, -1, -1 # defines the donor / acceptor spaces
                               # 4 parameters for RHF
                               # 8 paramters for UHF (4 alpha, 4 beta) orbital
			       # window, -1 refers to automatic determination
 STABEWIN -5.0, 5.0            # lower and upper cutoff in Eh for automatic
                               # freezing 
 #---------------------------------------------------------------------------------
 # alternative specification using a sub-block: 
 stab
  NRoots 3
  MaxDim 3 # etc.
 end
end

* xyz 0 1 
h 0.0 0.0 0.0
h 0.0 0.0 1.4
*
```

电子 Hessian 的确定在结构上与 TDHF/CIS/TDDFT 流程类似。因此，
许多选项都非常相似，建议用户阅读 TDDFT 一节（[sec:spectroscopyproperties.tddft](#sec:spectroscopyproperties.tddft)
），以澄清此处给出的部分选项。由于通常只关心"稳定与否"这一定性判断，
三个根应当足以找到最低本征值。基于同样的考虑，`StabMaxDim`、`StabMaxIter`、
`StabNGuess` 以及收敛判据也是这样选取的。参数 `StabLambda` 对应于参考文献
[SeegerPopleXVIIIStability](../../bibliography.md) 中公式 37 的 $\lambda$，它决定了原始 SCF 解与
新轨道的混合方式，从而产生新的猜测。该值的选取并不简单，因为正值和负值可能
（至少在原则上）导致不同的新解。随后 SCF 的收敛也依赖于它，
因为所有 SCF 流程都需要足够好的猜测才能在合理次数的迭代内收敛（甚至才能收敛）。

轨道窗口（orbital window）和能量窗口（energy window）都可以指定。请注意，
`StabEWIN` 会被相应的 `StabORBWIN` 值覆盖。自动确定也会受到
`%method FrozenCore` 设置的影响。测试表明，对实际轨道窗口的大幅削减
会显著影响结果，甚至导致定性上的失败。

该方法目前的限制有：

-   仅支持类单点计算。对于几何优化等，必须使用初始猜测的 MORead 功能
    [sec:essentialelements.initialguess](#sec:essentialelements.initialguess) 来采用这里得到的猜测。
    同样地，如果对 SCF 稳定性感兴趣，也必须提取几何结构并另做一次计算。

-   与 TDDFT 一样，支持 NORI、RIJONX 和 RIJCOSX。不支持 RI-JK。

-   其他更高级的功能，如有限温度计算（finite-temperature calculations）
    和相对论计算（ECP 除外），目前尚不支持。

总的来说，提醒用户不要盲目使用稳定性分析，
而应从能量差的角度批判性地评估结果，并通过（打印输出或作图）考察轨道。
它的有用性不可否认，但它绝不是一个黑箱工具。

可以在简单输入行（simple input line）上通过 STABILITY、SCFSTABILITY、
SCFSTAB 或 STAB 来请求默认设置的 SCF 稳定性分析。
