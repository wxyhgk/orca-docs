```{index} CP-SCF
```

(sec:essentialelements.cpscf)=
# CP-SCF 选项

在许多情况下需要求解耦合微扰自洽场（coupled perturbed self-consistent field，CP-SCF）方程，例如计算二阶导数性质（振动频率、极化率、NMR 屏蔽常数、间接自旋-自旋耦合、超精细耦合、g 张量）或 MP2 弛豫密度（此时称为 Z 向量方程）时。CP-SCF 方程是一组线性方程，通常写为

$$\mathbf A \mathbf U^x = \mathbf B^x,$$

其中 $\mathbf U^x$ 是微扰 $x$ 的解向量，右端（RHS）矩阵 $\mathbf B^x$ 与具体微扰有关，而左端（LHS）矩阵 $\mathbf A$ 与微扰无关，其中包含双电子排斥积分 $\left(ij\vert ab\right)$ 和 $\left(ia\vert jb\right)$ 等项。方程通过迭代求解，每一步都要重新组装 LHS，而 RHS 保持不变。因此，双电子积分的生成与变换是 CP-SCF 求解过程中最耗时的部分。

求解这些方程的 ORCA 模块接受以下若干选项，及其默认值：

```orca
%method
  Z_Solver     Pople # (default) Use the Pople algorithm to solve the equations
               DIIS  # Use the DIIS algorithm
               CG    # Use the conjugate gradient algorithm
  Z_Tol        1e-3  # Convergence tolerance for the residual norm. 
                     # Default is 1e-5 for VeryTightOpt
                     # and varies from 3e-3 to 3e-6 from LooseSCF to ExtremeSCF
  Z_MaxIter    128   # Maximum number of iterations
  Z_MaxDIIS    12    # Maximum number of DIIS vectors
  Z_Shift      0.3   # Level shift for DIIS
  Z_GridXC     1     # XC angular grid used for the LHS
  Z_IntAccXC   3.467 # XC radial grid accuracy used for the LHS
  Z_GridX      1     # COSX angular grid used for the LHS
  Z_IntAccX    3.067 # COSX radial grid accuracy used for the LHS
  Z_GridX_RHS  2     # COSX grid used for the RHS of MP2 Z-vector eqs (see below)
  Z_COSX_Alg   0     # (default) choose the best COSX algorithm automatically
               1     # better prescreening, more efficient for few densities
               2     # uses more memory, more efficient for many densities
end
```

自 ORCA 6 起，所有电响应性质计算以及 CIS/TD-DFT 梯度和弛豫密度计算都使用相同的设置。为方便起见，`%elprop` 输入块中的关键字仍然可用，但它们与 `%method` 中的关键字修改的是相同的内部变量。对于磁响应性质，求解器与收敛阈值在 `%eprnmr` 中单独设置，因为磁响应 CP-SCF 方程的收敛行为有时有所不同。

```orca
%elprop
  Solver     # Alias, see: %method Z_Solver
  Tol        # Alias, see: %method Z_Tol
  MaxIter    # Alias, see: %method Z_MaxIter
  MaxDIIS    # Alias, see: %method Z_MaxDIIS
  LevelShift # Alias, see: %method Z_Shift
end

%eprnmr
  Solver     # Solver for magnetic response, see options at: %method Z_Solver
  Tol        # Convergence tolerance for magnetic response
  MaxIter    # Alias, see: %method Z_MaxIter
  MaxDIIS    # Alias, see: %method Z_MaxDIIS
  LevelShift # Alias, see: %method Z_Shift
end
```

如果对双电子积分采用 RIJCOSX 近似，则关键字 `Z_GridX` 和 `Z_IntAccX` 适用。它们决定 COSX 积分的角向与径向网格，详见章节 {ref}`sec:essentialelements.numericalintegration.gridothers`。类似地，关键字 `Z_Grid` 和 `Z_IntAcc` 决定 DFT 交换关联（XC）泛函的积分网格。

不同微扰下 RHS 积分的求值方式不同——分别参见章节 {ref}`sec:essentialelements.ri.rijcosx`（SCF 级梯度）、{ref}`sec:spectroscopyproperties.properties.eprnmr`（使用 GIAO 的 EPR/NMR 计算）、{ref}`sec:modelchemistries.mp2.rijcosxrigrad`（MP2 梯度）和 {ref}`sec:modelchemistries.mp2.2ndder`、{ref}`sec:modelchemistries.mp2.rimp2.response`（MP2 二阶导数）。对于 MP2 Z 向量方程，RHS 中的 RIJCOSX Fock 响应项用 `Z_GridX_RHS` 指定的 COSX 网格求值。注意它的用法与 `Z_GridX` 不同：它选择的是 SCF 中所用三个网格之一（详见章节 {ref}`sec:essentialelements.ri.rijcosx`、{ref}`sec:essentialelements.ri.rijcosx.grids`、{ref}`sec:essentialelements.numericalintegration`），不建议修改其默认值 2。

如果 SCF 中使用了 RIJONX 或 RIJK 近似，则 CP-SCF 中同样采用这些近似。但请注意，RI-K 近似对于这些项的计算效率不高。

对于基于 CCSD、CCSD(T) 等相关方法的性质，在构造响应积分（作为线性响应方程 RHS 的一部分）时需要求解 CP-SCF 方程，因此需要一个一致的 `Z_Tol`。更多细节见 {ref}`sec:modelchemistries.autoci.autociresp`。

:::{admonition} 注意
:class: note
使用 COSX 运行 RPA 或 CP-SCF 时，ORCA-6.0.0 中曾将某个非常耗内存的算法硬编码为默认算法，这并非原意。ORCA-6.0.1 已修复该问题，自动选择的算法现为默认值。这可能导致与这些结果有非常微小的差异，尤其当密度数目较少时。因此，计算结果与 ORCA-6.0.0 会略有不同。这不影响任何"常规"的能量、梯度等计算，只影响 RPA 和 CP-SCF 的这些特定情况。
:::
