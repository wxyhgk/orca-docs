```{index} Symmetry
```

(sec:essentialelements.symmetry)=
# ORCA 与对称性（ORCA and Symmetry）

在其发展历程的大部分时间里，ORCA 并未利用分子对称性（molecular
symmetry）。从 2.8 版（2010 年 9 月发布）开始，至少有了有限的使用。
在用户请求时（例如使用简单关键词 `! UseSym`，见下文），程序会检测点群
（point group）、定向分子、清理坐标，并产生对称性适配的分子轨道
（symmetry-adapted molecular orbitals）。

对于几何结构和梯度的清理，会考虑完整的点群。对于几何 Hessian
（geometric Hessian）的对角化，支持所有仅含实特征标（real characters）
的有限点群，即 $C_i$、$C_s$、$C_2$、$C_{2h}$、$C_{nv}$、$D_n$、
$D_{nh}$、$D_{nd}$、$T$、$T_d$、$O$、$O_h$、$I$ 和 $I_h$，其中 $n\ge 2$。
对于所有其他用途，如构建对称性适配分子轨道或描述电子态，目前仅支持
$D_{2h}$ 及其子群。这里会根据自动检测或用户指定的点群，
自动选取 $D_{2h}$ 的相应子群（称为约化点群，reduced point group），
对称性的使用有助于控制计算和结果的解释。请注意，在使用对称性时，
角动量量子数 $\ell$ 目前仍限于 $\ell\le 8$。

## 入门（Getting started）

对称性的使用可通过简单关键词 `UseSymmetry`（可缩写为 `UseSym`）开启，
或者当输入中存在 `%Symmetry`（或 `%Sym`）输入块时开启。ORCA 随后会
自动确定点群、重新定向并居中分子，使其对称元素与坐标系对齐，
并用一个几何结构替换输入结构——该结构精确对应于此点群，
且使两结构原子间平方距离之和最小。

任何试图确定任意原子簇点群的程序，都必须准备好应对原子坐标中一定程度的
数值噪声。ORCA 默认允许每个原子相对于与所考察点群一致的理想位置
最多偏离 $10^{-4}$ 原子单位。这一数值的理由是：当用户把小数点后有
五位有效数字的 Cartesian 坐标输入程序时，会产生舍入误差，
而这些坐标原本表示一个精确的（对称性适配的）几何结构。
比坐标中数值噪声高约一个数量级的阈值通常是十分安全的。

如果 Cartesian 坐标中的最大误差超过这 $10^{-4}$ 原子单位，
ORCA 的对称性模块将无法识别预期的点群。强烈建议用户始终确认
所检测到的点群符合预期。如果对称性模块报告的点群显得过低，
用户可以尝试用 `%Symmetry` 输入块中的 `SymThresh` 选项把检测阈值提高到
$10^{-3}$ 或 $10^{-2}$ Bohr 半径：

```orca
%Sym SymThresh 0.01 End
```

一种获得完美对称结构而又避免任何昂贵计算的好方法，是使用简单关键词
`! NoIter XYZFile` 并配以合适的阈值。所得 `.xyz` 扩展名文件中的结构
随后可用作实际计算的输入。

举一个说明性的例子：交叉式乙烷（staggered ethane）的坐标是通过*不*使用
对称性的几何优化得到的。开启对称性后，由于残留的数值噪声，
识别出的点群是 $C_i$ 而不是预期的 $D_{3d}$。为解决这一问题，
把检测阈值提高到 $10^{-2}$ 原子单位，并通过以下输入产生一个具有完美
对称性的坐标文件：

```{literalinclude} ../../orca_working_input/C03S03_017.inp
:language: orca
```

如果即使 `SymThresh` 取 $10^{-2}$ 原子单位，ORCA 仍未能找到预期的点群，
强烈建议用户在进一步增大该值之前，先用自己常用的可视化工具仔细检查结构。
查找任何明显的畸变甚至缺失的原子。一个特别棘手的点可能是甲基的取向
或柔性侧链的构象。绕单键的一个小旋转就可能足以把某些原子位置推到限值之外。
如果构象偏差无法用分子编辑器或建模程序修正，一种可能的替代方案是
先用较廉价的方法（如 `PB86`）和较小的基组（如 `def2-SVP`）
在不使用对称性的情况下预优化该结构。甚至可以考虑多轮预优化与结构编辑，
直到所有对称性等价的侧链都锁定在相同构象，使 ORCA 最终检测到正确的点群。

不建议使用过高或过低的 `SymThresh` 值进行计算，因为这可能导致对称性模块
出现非常奇怪的行为。例如考虑以下输入文件，其中包含一个六氟化硫
（sulfur hexafluoride）分子的完美八面体几何结构。其坐标可以轻松地手工创建：
把硫原子放在原点，在每根坐标轴上各放置两个氟原子，到原点的距离均为 $r$
（$r=1.56$ &#x212B;，约合 $2.95$ 原子单位）。在这种情况下，
把 `SymThresh` 取大到 $0.1$ Bohr 半径也能正常工作，得到正确的点群 O$_h$。

```{literalinclude} ../../orca_working_input/C03S03_018.inp
:language: orca
```

然而，如果把 `SymThresh` 进一步增大到 $t=0.5$ 原子单位，
点群检测算法就会崩溃（其后果是打印出奇怪的警告），
所报告的点群降为 C$_i$（其中反演中心是唯一的非平凡对称元素）。
这是因为反演中心易于检测，而且它是早期检查之一完成的。
点群识别的崩溃可以解释如下。在点群检测过程中，对称性模块当然不知道
给定的输入几何结构是精确的。因此它会像处理任何其他输入结构一样被处理。
`SymThresh` 取 $t=0.5$ Bohr 半径意味着未知的精确原子位置位于以输入原子
位置为中心、半径为 $t=0.5$ 原子单位的球内。两个相邻氟原子之间的输入距离
$a=\sqrt{2}\,r$ 约为 $a\approx 2.21$ &#x212B; $\approx 4.17$ 原子单位，
因此它们未知的精确距离 $d$ 可能在如下区间内变化
（见 {numref}`fig:symthresh` 中的示意图）：

$$d_{\rm min}=a-2t=3.17\:{\rm a. u.}\leq d\leq d_{\rm max}=a+2t=5.17\:{\rm a. u.}$$

类似地，两个相对氟原子之间未知的精确距离 $d'$（其输入距离为
$a'=2r=5.90$ 原子单位）为：

$$d'_{\rm min}=a'-2t=4.90\:{\rm a. u.}\leq d'\leq d'_{\rm max}=a'+2t=6.90\:{\rm a. u.}$$

由于 $d$ 和 $d'$ 的可能区间相互重叠（因为 $d_{\rm max}>d'_{\rm min}$），
*全部*十五个 F--F 距离都被认为相等。由于三维空间中不存在具有六个顶点
且十五条顶点间距离全相等的固体，点群检测算法因此失败。

(fig:symthresh)=
```{figure} ../../images/symthresh.png

`SymThresh` 的取值 $t$、某对输入原子间距离 $a$，以及精确原子位置之间
距离 $d$ 的允许区间 $[d_{\rm min},d_{\rm max}]$ 之间的关系。
该区间的宽度为 $d_{\rm max}-d_{\rm min}=4t$。
```

(sec:essentialelements.symmetry.geomopt_using_sym)=
## 使用对称性进行几何优化

如果在开启对称性的情况下进行几何优化，ORCA 会首先确定起始结构的点群，
并把被认为含有数值噪声的几何结构替换为具有完美对称性的几何结构。
从 ORCA 6 开始，如果通过在 `%Symmetry` 输入块中设置选项
`CleanUpGradient true` 提出请求，优化器会在优化的每一步清理梯度。
梯度清理是通过投影掉所有非全对称分量来完成的。这样，
分子的对称性在优化过程中就不会降低。

自 ORCA 6.1.1 起，设置 `SymRelaxOpt false` 和 `CleanUpGradient true`
成为默认值。原因在于：在几何优化过程中，ORCA 由于其设计无法处理
优化期间分子的旋转——而要把改变后的对称元素与坐标轴对齐是需要这种旋转的。
选项 `SymRelaxOpt` 将在下一个主版本或次版本中被彻底移除。

下表总结了优化器随 `SymRelaxOpt` 和 `CleanUpGradient` 选项的行为：

| `SymRelaxOpt` | `CleanUpGradient` | 行为 |
| :-----------: | :---------------: | :-------- |
| `false`       | `true`            | 对称性将被冻结（新的默认值）。 |
| `false`       | `false`           | 不推荐使用该设置。 |
| `true`        | `true`            | 对称性可能升高但不会降低（可能不工作）。 |
| `true`        | `false`           | 对称性可自由变化（可能不工作）。 |

把两个开关都设为 `false` 会使分子的对称性在优化每一步更新几何时发生变化，
但在对坐标进行对称化时这一变化会立即被撤销，因为不允许点群改变。
因此不推荐该设置。

(sec:essentialelements.symmetry.geometric_hessian)=
## 使用对称性对几何 Hessian 对角化

自 6.0 版起，如果用户同时请求了频率和对称性，且自动检测或用户指定的点群
是有限的并仅含实特征标，ORCA 就能用对称性对几何 Hessian 进行对角化。
这些点群是 $C_i$、$C_s$、$C_2$、$C_{2h}$、$C_{nv}$、$D_n$、$D_{nh}$、
$D_{nd}$、$T$、$T_d$、$O$、$O_h$、$I$ 和 $I_h$，其中 $n\ge 2$。

为此，质量加权 Cartesian 坐标下的 Hessian 被逐块变换到对称性适配的
位移基（symmetry-adapted displacement basis）中。由于简并不可约表示
（degenerate irreducible representation）的所有分量除数值噪声外给出相同的块，
该块会对各分量取平均，并且每个不可约表示只做一次对角化。
因此，一个简并能级的振动频率完全相同。简并能级的分量从 0 开始编号，
该编号写在指定不可约表示的 Mulliken 符号后的圆括号中。

(sec:essentialelements.symmetry.default_alignment)=
## 对称元素与坐标系的默认取向

如果 ORCA 确定分子的点群且用户未选择任何特殊选项，则完整点群的对称元素
与坐标系的对齐方式遵循以下原则：

1.  分子的质心默认将被移到原点。[^zmatnoatoms] 如果该点群有一个*唯一*
    顶点在所有对称操作下保持不变，则质心与该顶点重合。
    除 $C_s$、$C_n$ $(n\ge 1)$、$C_{nv}$ $(n\ge 2)$ 和 $C_{\infty v}$
    外，所有点群都属于这种情况。

2.  如果分子有一个具有最高重数的唯一对称轴，该轴将成为 $z$ 轴。
    这适用于除 $C_1$、$C_i$、$C_s$、$D_2$、$D_{2h}$、立方点群和 $K_h$
    外的所有点群。

3.  对于点群 $C_s$，镜面（mirror plane）将成为 $xy$ 平面。

4.  对于点群 $C_{nv}$ $(n\ge 2)$，其中一个竖直镜面将成为 $xz$ 平面。

5.  对于点群 $D_n$ $(n\ge 3)$、$D_{nh}$ $(n\ge 3)$ 和 $D_{nd}$ $(n\ge 2)$，
    垂直于最高重数轴的某个二重旋转轴将成为 $x$ 轴。

6.  对于点群 $D_2$、$D_{2h}$、$T$ 和 $T_h$，三个相互正交的 $C_2$ 轴
    将成为坐标轴。

7.  对于点群 $T_d$、$O$ 和 $O_h$，三个相互正交的四重旋转轴或旋转-反映轴
    将成为坐标轴。

8.  最后，对于点群 $I$ 和 $I_h$，五组相互正交的 $C_2$ 轴中的某一组
    将成为坐标轴。离 $z$ 轴最近的那对 $C_5$ 或 $S_{10}$ 轴将位于 $yz$ 平面内。

9.  一般而言，分子的取向将尽可能少地改动以满足上述标准。
    如果输入几何结构已经满足这些标准，分子将完全不被移动或旋转。

如果体系的点群是 $n\ge 2$ 的 $D_{nd}$ 或 $T_d$，而用户用选项 `PreferC2v`
选择了子群 $C_{2v}$，则改用以下规则：

-   对于 $n\ge 2$ 的点群 $D_{nd}$，其中一个对角镜面将成为 $xz$ 平面。

-   对于点群 $T_d$，某个包含 $z$ 轴的对角镜面将成为 $xz$ 平面，
    即与默认取向相比，分子将绕 $z$ 轴旋转 45 度。

{numref}`table:subgroups` 概述了所有点群，以及约化点群
（$D_{2h}$ 的最大公共子群）的对称元素与坐标系的对齐方式。

(table:subgroups)=
:::{list-table} 适用于电子结构计算的点群及相应子群。
:header-rows: 3

* - 完整
  - 指数
  - 唯一
  - 与平面
  - 所选
  - 子群
* - 点群
  - $n$
  - 中心[^inversioncenter]
  - 分子[^column]
  - 子群
  - 的
* -
  -
  -
  - 相容
  -
  - 取向[^nextcolumn]
* - $C_1$
  -
  - 无
  - 无
  - $C_1$
  -
* - $C_i$
  -
  - $i$
  - 无
  - $C_i$
  -
* - $C_s$
  -
  - 无
  - 有
  - $C_s$
  -
* - $C_n$
  - 奇
  - 无
  - 无
  - $C_1$
  -
* -
  - 偶
  - 无
  - 无
  - $C_2$
  - $z$ 轴
* - $C_{nv}$
  - 奇
  - 无
  - 无
  - $C_s$
  - $xz$ 平面
* -
  - 偶
  - 无
  - $n=2$ 时
  - $C_{2v}$
  - $z$、$xz$、$yz$
* - $C_{nh}$
  - 奇
  - 有
  - 有
  - $C_s$
  - $xy$ 平面
* -
  - 偶
  - $i$
  - 有
  - $C_{2h}$
  - $z$、$xy$
* - $D_n$
  - 奇
  - 有
  - 无
  - $C_2$
  - $x$ 轴
* -
  - 偶
  - 有
  - 无
  - $D_2$
  -
* - $D_{nh}$
  - 奇
  - 有
  - 有
  - $C_{2v}$
  - $x$、$xy$、$xz$
* -
  - 偶
  - $i$
  - 有
  - $D_{2h}$
  -
* - $D_{nd}$
  - 奇
  - $i$
  - 无
  - $C_{2h}$
  - $x$、$yz$
* -
  - 偶
  - 有
  - 无
  - $D_2$
  -
* -
  -
  -
  -
  - $C_{2v}$
  - $z$、$xz$、$yz$
* - $S_{2n}$
  - 奇
  - $i$
  - 无
  - $C_i$
  -
* -
  - 偶
  - 有
  - 无
  - $C_2$
  - $z$ 轴
* - $T$
  -
  - 有
  - 无
  - $D_2$
  -
* - $T_h$
  -
  - $i$
  - 无
  - $D_{2h}$
  -
* - $T_d$
  -
  - 有
  - 无
  - $D_2$
  -
* -
  -
  -
  -
  - $C_{2v}$
  - $z$、$xz$、$yz$
* - $O$
  -
  - 有
  - 无
  - $D_2$
  -
* - $O_h$
  -
  - $i$
  - 无
  - $D_{2h}$
  -
* - $I$
  -
  - 有
  - 无
  - $D_2$
  -
* - $I_h$
  -
  - $i$
  - 无
  - $D_{2h}$
  -
* - $C_{\infty v}$
  -
  - 无
  - 无
  - $C_{2v}$
  - $z$、$xz$、$yz$
* - $D_{\infty h}$
  -
  - $i$
  - 无
  - $D_{2h}$
  -
* - $K_h$
  -
  - $i$
  - 无
  - $D_{2h}$
  -
:::

## $D_{2h}$ 及其子群的不可约表示

{numref}`table:species_table_c2v`、{numref}`table:species_table_d2`
和 {numref}`table:species_table_d2h` 列出了 ORCA 中支持用于电子结构计算的
各点群的不可约表示（irreducible representations，也称谱项 species）
及相应特征标，以及这些不可约表示的乘积表。凡数据依赖于对称元素与坐标系
取向之处，均遵循 Mulliken 的建议 {cite}`mulliken1955sym`。
这一做法与 IUPAC 的建议 {cite}`schutte1997sym` 一致。

(table:species_table_c2v)=
:::{list-table} 点群 $C_{2v}$ 的谱项及谱项乘积表。$C_{2v}$ 的谱项表对应于 {cite}`mulliken1955sym` 中的表 III。各列中二重轴与镜面的方向彼此通过循环置换相联系。

* - $\begin{array}{@{}c@{\hspace{10mm}}c@{}}
       \begin{array}[b]{|c|cccc|}\hline
                &      & C_2(z) & \sigma_v(xz) & \sigma_v(yz) \\
         C_{2v} &   E  & C_2(x) & \sigma_v(xy) & \sigma_v(xz) \\
                &      & C_2(y) & \sigma_v(yz) & \sigma_v(xy) \\\hline
          A_1   &  +1  &   +1   &      +1      &      +1      \\
          A_2   &  +1  &   +1   &      -1      &      -1      \\
          B_1   &  +1  &   -1   &      +1      &      -1      \\
          B_2   &  +1  &   -1   &      -1      &      +1      \\\hline
       \end{array} &
       \begin{array}[b]{|c|cccc|}\hline
         \times &  A_1  &  A_2  &  B_1  &  B_2  \\\hline
          A_1   &  A_1  &  A_2  &  B_1  &  B_2  \\
          A_2   &  A_2  &  A_1  &  B_2  &  B_1  \\
          B_1   &  B_1  &  B_2  &  A_1  &  A_2  \\
          B_2   &  B_2  &  B_1  &  A_2  &  A_1  \\\hline
       \end{array}
     \end{array}$
:::

(table:species_table_d2)=
:::{list-table} 点群 $D_2$ 的谱项及谱项乘积表。$D_2$ 的谱项表是从 $D_{2h}$ 的谱项表中去掉反演中心和镜面得到的（见 {numref}`table:species_table_d2h`）。

* - $\begin{array}{@{}c@{\hspace{10mm}}c@{}}
       \begin{array}{|l|cccc|}\hline
         D_2    &   E  & C_2(z) & C_2(y) & C_2(x) \\\hline
         A      &  +1  &   +1   &   +1   &   +1   \\
         B_1    &  +1  &   +1   &   -1   &   -1   \\
         B_2    &  +1  &   -1   &   +1   &   -1   \\
         B_3    &  +1  &   -1   &   -1   &   +1   \\\hline
       \end{array} &
       \begin{array}{|c|cccc|}\hline
         \times & A    &   B_1  &   B_2  &   B_3  \\\hline
         A      & A    &   B_1  &   B_2  &   B_3  \\
         B_1    & B_1  &   A    &   B_3  &   B_2  \\
         B_2    & B_2  &   B_3  &   A    &   B_1  \\
         B_3    & B_3  &   B_2  &   B_1  &   A    \\\hline
       \end{array}
     \end{array}$
:::

(table:species_table_d2h)=
:::{list-table} 点群 $D_{2h}$ 的谱项及谱项乘积表。$D_{2h}$ 的谱项表对应于 {cite}`mulliken1955sym` 中的表 IV。

* - $\begin{array}{@{}c@{}}
      \begin{array}{|l|cccccccc|}\hline
        D_{2h} &   E  & C_2(z) & C_2(y) & C_2(x) &  i & \sigma(xy) & \sigma(xz) & \sigma(yz) \\\hline
        A_g    &  +1  &   +1   &   +1   &   +1   & +1 &     +1     &     +1     &     +1     \\
        B_{1g} &  +1  &   +1   &   -1   &   -1   & +1 &     +1     &     -1     &     -1     \\
        B_{2g} &  +1  &   -1   &   +1   &   -1   & +1 &     -1     &     +1     &     -1     \\
        B_{3g} &  +1  &   -1   &   -1   &   +1   & +1 &     -1     &     -1     &     +1     \\
        A_u    &  +1  &   +1   &   +1   &   +1   & -1 &     -1     &     -1     &     -1     \\
        B_{1u} &  +1  &   +1   &   -1   &   -1   & -1 &     -1     &     +1     &     +1     \\
        B_{2u} &  +1  &   -1   &   +1   &   -1   & -1 &     +1     &     -1     &     +1     \\
        B_{3u} &  +1  &   -1   &   -1   &   +1   & -1 &     +1     &     +1     &     -1     \\\hline
      \end{array} \\[3mm]
      \begin{array}{|c|cccccccc|}\hline
        \times & A_g    & B_{1g} & B_{2g} & B_{3g} & A_u    & B_{1u} & B_{2u} & B_{3u} \\\hline
        A_g    & A_g    & B_{1g} & B_{2g} & B_{3g} & A_u    & B_{1u} & B_{2u} & B_{3u} \\
        B_{1g} & B_{1g} & A_g    & B_{3g} & B_{2g} & B_{1u} & A_u    & B_{3u} & B_{2u} \\
        B_{2g} & B_{2g} & B_{3g} & A_g    & B_{1g} & B_{2u} & B_{3u} & A_u    & B_{1u} \\
        B_{3g} & B_{3g} & B_{2g} & B_{1g} & A_g    & B_{3u} & B_{2u} & B_{1u} & A_u    \\
        A_u    & A_u    & B_{1u} & B_{2u} & B_{3u} & A_g    & B_{1g} & B_{2g} & B_{3g} \\
        B_{1u} & B_{1u} & A_u    & B_{3u} & B_{2u} & B_{1g} & A_g    & B_{3g} & B_{2u} \\
        B_{2u} & B_{2u} & B_{3u} & A_u    & B_{1u} & B_{2g} & B_{3g} & A_g    & B_{1u} \\
        B_{3u} & B_{3u} & B_{2u} & B_{1u} & A_u    & B_{3g} & B_{2g} & B_{1g} & A_g    \\\hline
      \end{array}
    \end{array}$
:::

## `%Symmetry` 输入块中的选项

{numref}`table:symmetry_block_options` 列出了 `%Symmetry`（或 `%Sym`）
输入块中的可用选项。为向后兼容，选项 `SymThresh` 和 `SymRelax`
（与下文的 `SymRelaxSCF` 相同）也可以在 `%Method` 输入块中访问。
不过，这种用法已弃用，不建议在新的输入文件中使用。

:::{tabularcolumns} \Y{0.2}\Y{0.1}\Y{0.15}\Y{0.55}
:::
(table:symmetry_block_options)=
:::{list-table} `%Symmetry`（`%Sym`）输入块中的选项列表
:header-rows: 1
:class: longtable

* - 选项
  - 类型
  - 默认值
  - 说明
* - `UseSymmetry`
  - Boolean
  - `True`
  - 把该选项设为 `False` 时，
即使输入文件中存在 `%Symmetry` 块，也可以关闭对称性。
* - `UseSym`
  - Boolean
  - `True`
  - 与 `UseSymmetry` 相同。
* - `SymThresh`
  - Real
  - $10^{-4}$
  - 在点群识别过程中，距离短于该阈值（以原子单位计）的两个顶点
被视为等同。
* - `PreferC2v`
  - Boolean
  - `False`
  - 指示在两种选择都合适的电子结构计算中（$n$ 为奇数的点群 $D_{nd}$
以及 $T_d$），是否优先选用子群 $C_{2v}$ 而非 $D_2$。
* - `PointGroup`
  - String
  - 空字符串
  - 如果用户用该选项指定了点群，则跳过点群识别，
用户必须确保分子在坐标系中的取向符合
{ref}`sec:essentialelements.symmetry.default_alignment` 中的约定。
注意，点群标签必须用双引号括起来，否则 ORCA 会报无效赋值。
* - `SymRelaxSCF`
  - Boolean
  - `False`
  - 指示在 SCF 过程中是否允许各不可约表示的轨道占据数发生变化。
* - `SymRelaxOpt`
  - Boolean
  - `False`
  - 指示是否在几何优化的每一步从头确定点群。
使用新的默认值 `False` 时，无论当前结构与理想结构之间的距离超出
`SymThresh` 多少，每一步都会施加初始点群。
取 `True` 时允许点群任意变化，但 ORCA 由于其设计无法处理这种情况下
分子的旋转——而要把改变后的对称元素与坐标轴对齐是需要这种旋转的——
因此该设置可能不工作。该选项将在下一个主版本或次版本中被彻底移除。
* - `CleanUpCoords`
  - Boolean
  - `True`
  - 决定是否用自动检测或用户指定的点群清理分子几何结构。
即使 `CleanUpCoords` 为 `False`，仍会临时计算对称化坐标，
并且若与原始几何结构的最大偏差超过 `SymThresh`，将打印警告。
* - `CleanUpGeom`
  - Boolean
  - `True`
  - 与 `CleanUpCoords` 相同。
* - `CleanUpGrad`
  - Boolean
  - `True`
  - 指示是否用分子的完整点群从梯度中移除所有非全对称分量。
这可确保点群在整个优化过程中不会降低。
* - `CleanUpGradient`
  - Boolean
  - `True`
  - 与 `CleanUpGrad` 相同。
* - `Print`
  - Integer
  - 1
  - 决定对称性处理总体上、尤其是点群检测的输出量；
    0 —— 点群检测期间无输出；
    1 —— 正常输出；
    2 —— 详细信息；
    3 —— 调试打印。
* - `PrtSALC`
  - Integer
  - 0
  - 指定构建原子轨道对称性适配线性组合（symmetry-adapted linear
    combinations, SALCs）时的输出量；
    0 —— 对称性适配轨道无输出；
    1 —— 正常输出；
    2 —— 详细信息（例如 SALC 本身）；
    3 —— 调试打印。
:::

[^zmatnoatoms]: 在 Z 矩阵不含任何有质量原子这一非常特殊的情况下，
    改用几何中心。

[^inversioncenter]: 反演中心记作 $i$。"有"表示存在一个*唯一*顶点，
    它在该点群的所有对称操作下保持不变。

[^column]: 该列表示给定点群是否可以是平面分子的*完整*点群。

[^nextcolumn]: 该列包含*默认*情况下与约化点群（完整点群与 $D_{2h}$ 的
    最大公共子群）的对称元素相重合的坐标系元素（轴或平面）。
    如果完整点群包含一个唯一的主对称轴（具有最高重数），
    则认为该轴与 $z$ 轴重合。
