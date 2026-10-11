
另一方面，二阶 CASSCF 方法计算 Hessian 矩阵并需要积分 $(pq|xy)$ 和
$(px|qy)$（$p,q=$ 内部、活性；$x,y=$ 任意轨道）。这是一组相当大的积分，其生成在 CPU 时间和磁盘存储方面都很费力。标准的二阶方法（如增广 Hessian（`NR`））在可良好处理的分子大小方面更为有限。虽然 `NR` 在极小值附近效率很高，但当初始轨道偏离太远时鲁棒性较差。
[受限步长增广 Hessian（`TRAH`）](sec:modelchemistries.casscf.trah)缓解了许多缺点，提供了一个更鲁棒的二阶拟设，也可以处理更大的体系。{cite}`helmich_trahcasscf_2022`
这里大多数积分使用 [RI 近似](sec:modelchemistries.casscf.ri)以 AO 直接策略处理。更多细节请参考原始出版物。

### 态平均
在许多情况下，希望不是为单个态而是为多个态的平均优化轨道。为了看清所做的工作，态 $I$ 的能量被重写为：

$$E_{I} \left({ \mathrm{\mathbf{c} },\mathrm{\mathbf{C} }} \right)=\sum\limits_{pq} { \Gamma
_{q}^{p\left( I \right)} h_{pq} } +\sum\limits_{pqrs} { \Gamma
_{qs}^{pr\left( I \right)} \left({ pq\left|{ rs} \right.} \right)}
$$ 

这里 $\Gamma_{q}^{p\left( I \right)}$ 和
$\Gamma_{qs}^{pr\left( I \right)}$ 是该态的单粒子和双粒子约化
电子密度矩阵（标记 $p, q, r, s$ 张成
非活性和活性子空间）：

$$\Gamma_{q}^{p\left( I \right)} =\left\langle { \Psi_{I}^{S} \left|{E_{q}^{p} } \right|\Psi_{I}^{S} } \right\rangle$$

$$\Gamma_{qs}^{pr\left( I \right)} =\frac{1}{2}\left\langle { \Psi_{I}^{S}
\left|{ E_{q}^{p} E_{s}^{r} -\delta_{qr} E_{s}^{p} } \right|\Psi_{I}^{S} }
\right\rangle$$

平均能量只需通过对密度
矩阵使用任意权重 $w_I$ 求平均得到，权重由用户定义但
约束为总和为一。

$$\Gamma_{q}^{p\left({ av} \right)} =\sum\limits_I { w_{I} \Gamma _{q}^{p\left( I \right)} }
$$ 

$$\Gamma_{qs}^{pr\left({ av} \right)} =\sum\limits_I { w_{I} \Gamma_{qs}^{pr\left( I \right)} }
$$ 

$$\sum\limits_I { w_{I} } =1
$$ 


## 基本用法

CASSCF 计算始终需要的最基本输入信息是活性电子数和轨道数的指定。

```orca
%casscf 
        nel  4  # number of active space electrons
        norb 6  # number of active orbitals
end
```

ORCA 中的 CASSCF 程序可以平均多个多重度的态。
多重度以列表给出。对于每个多重度，应指定根数：

```orca
%casscf mult   1,3 # here: multiplicities singlet and triplet

        nroots 4,2 # four singlets, two triplets
        end
```

如果启用了 ORCA 中的对称性处理（`! UseSym`），每个多重度块必须分配一个不可约表示。
给定对称性中对应于"irrep\"的数字
在 ORCA 的输出中打印。

```orca
%casscf mult   1,3 # here: multiplicities singlet and triplet
        irrep  0,1 # here: irrep for each mult. block (mandatory!)
        nroots 4,2 # four singlets, two triplets
```

多个根和多重度通常意味着态平均 CASSCF（SA-CASSCF）计算。注意程序默认为多重度块选择相等
权重。给定块内的根具有
相等权重。用户可以为多重度块和根定义自定义加权方案：

```orca
%casscf mult 1,3   # here: multiplicities singlet and triplet
        nroots 4,2  # four singlets, two triplets
        bweight 2,1 # singlets and triplets weighted 2:1
        weights[0] = 0.5,0.2,0.2,0.2 # singlet weights
        weights[1] = 0.7,0.3         # triplet weights
        end
```

程序自动归一化这些权重，使所有权重之和为一。如果希望收敛到激发态，
则 `weights[0]` 数组可能类似于 `0.0,0.0,1.0`（这将
为第三激发态优化轨道）。如果多个态
在轨道优化过程中交叉，最终会导致
收敛问题。

我们顺带指出，态平均
过程的收敛轨道是这组态的折中。ORCA 默认只
打印 SA-CASSCF 梯度范数。态特定梯度在计算结束时用关键词 `PrintGState` 汇总。

```orca
%casscf
  ...
  printgstate true # optional printing of the state-specific orbital gradients
end
```
(sec:modelchemistries.casscf.2step)=
### 轨道优化（两步方法）

下面我们讨论两步拟设的可用选项，其中轨道更新和 CI 问题按顺序求解。更强大且稍昂贵的一步拟设在第 {numref}`sec:modelchemistries.casscf.trah` 节中描述。我们指出，许多收敛问题已经可以通过更换初始轨道来解决。

:::{warning} 警告
以下关键词是可选的，只应在面临严重收敛困难时使用。理想情况下，默认或 `!TRAH` 应该足够。
:::

除微扰 SuperCI（`SuperCI_PT` - 默认）{cite}`kollmarSXPT2019`外，还实现了几种轨道优化方法。

```orca
# Keywords to be used as Orbstep/Switchstep
SuperCI_PT  # perturbative SuperCI (first-order) - default
TRAH        # restricted-step augmented Hessian (second-order 1-step)
#
SuperCI     # SuperCI (first-order)
DIIS        # DIIS (first-order)
KDIIS       # KDIIS (first-order)
SOSCF       # approx. Newton-Raphson (first-order)
NR          # augmented Hessian Newton-Raphson
            # unfolded two-step procedure
            # - still not true second-order
```

不同的收敛器有不同的优势。一阶方法
便宜但通常比二阶
方法需要更多迭代。当梯度远离收敛时，程序使用
定义为 `orbstep` 的收敛器，而在接近收敛时使用
`switchstep`。switchstep 的实际判据由
关键词 `SwitchConv` 和 `SwitchIter` 定义。

```orca
%casscf 
  OrbStep    SuperCI # or any other from the list above
  SwitchStep DIIS    # or any other from the list above

  SwitchConv 0.03 # gradient at which to switch
```
