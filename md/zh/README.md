# ORCA 6.1 教程（简体中文）

译自官方 Sphinx 文档：https://www.faccts.de/docs/orca/6.1/tutorials/

- 英文 Markdown 源：`../md/`
- 离线 HTML 镜像：`../tutorials/`
- 图片资源：`images/`（软链接至 `md/images/`）

## 目录

### 入门（First steps）
- [如何引用](first_steps/howtocite.md)
- [安装 ORCA](first_steps/install.md)
- [Hello water！你的第一个 ORCA 计算](first_steps/first_calc.md)
- [输入与输出](first_steps/input_output.md)
- [并行运行计算](first_steps/parallel.md)
- [内存设置](first_steps/memory.md)
- [图形用户界面（GUI）](first_steps/GUI.md)
- [解决常见问题](first_steps/trouble_install.md)

### 工作流（Workflows）
- [复合作业](workflows/compound.md)
- [外推技术](workflows/extrapol.md)
- [ORCA 与外部方法](workflows/extopt.md)
- [ORCA Python 接口（OPI）](workflows/opi.md)

### 性质（Properties）
- [单点能](prop/single_point.md)
- [几何优化](prop/geoopt.md)
- [振动频率](prop/freq.md)
- [热力学](prop/thermo.md)
- [隐式溶剂化模型](prop/cpcm.md)
- [显式溶剂化（SOLVATOR）](prop/solvator.md)
- [构象搜索（GOAT）](prop/goat.md)
- [相对论校正](prop/relativistic.md)
- [色散校正](prop/disp.md)
- [化学键分析](prop/bonds.md)
- [定域能分解（LED）](prop/led.md)
- [分数占据密度（FOD）](prop/fod.md)
- [电荷模型](prop/charges.md)
- [静电势（ESP）](prop/esp.md)
- [相关能](prop/corren.md)

### 反应性（Reactivity）
- [用 NEB-TS 寻找过渡态](react/nebts.md)
- [过渡态优化](react/tsopt.md)
- [过渡态构象](react/tsconf.md)
- [内禀反应坐标（IRC）](react/irc.md)
- [计算精确的能垒](react/actibar.md)
- [动力学同位素效应（KIE）](react/KIE.md)
- [绘制福井函数](react/FUKUI.md)
- [自动对接（DOCKER）](react/docker.md)

### 波谱（Spectroscopy）
- [红外与拉曼](spec/IR.md)
- [紫外-可见光谱（UV/Vis）](spec/UVVis.md)
- [电子圆二色谱（ECD）](spec/ECD.md)
- [振动圆二色谱（VCD）](spec/vcd.md)
- [核磁共振（NMR）](spec/NMR.md)
- [电子顺磁共振（EPR）](spec/EPR.md)
- [自旋轨道耦合（SOC）](spec/SOC.md)

### 多尺度方法（Multiscale methods）
- [多尺度模型入门：QM/XTB ONIOM](multi/basics.md)
- [QM/XTB 之外的 ONIOM 方法](multi/basics-otheroniom.md)
- [用于过渡态的多尺度 NEB-TS](multi/oniom-nebts.md)
- [离子晶体-QM/MM](multi/ionic_crystal.md)
- [自动碎片化](multi/fragmentator.md)

### 附录
- [参考文献](bib.md)
- [索引](genindex.md)

## 翻译约定

- 代码块、行内代码、公式（LaTeX）、ORCA 关键词、文件名、引用键保持原文
- 专业术语首次出现采用「中文（English）」形式
- 提示框：Note→注意、Warning→警告、Important→重要、Hint/Tip→提示
