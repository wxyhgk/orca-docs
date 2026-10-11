---
title: 如何引用
source: https://www.faccts.de/docs/orca/6.1/tutorials/first_steps/howtocite.html
---

# 如何引用

由于 ORCA 目前且将始终免费供学术使用，ORCA 背后的开发人员依赖于您对其辛勤工作的引用——正是这份付出使 ORCA 成为如今这样有用的工具。因此，我们恳请您不仅引用所用 ORCA 版本的通用参考文献，还要引用与您 ORCA 计算中所用方法相关的具体工作。为了便于识别这些文献，我们在 ORCA 6 中添加了自动打印功能，为您提供引用建议。

ORCA 的通用参考文献为：

Neese, F. *The ORCA program system* *Wiley Interdiscip. Rev.: Comput. Mol. Sci.*, **2012**, *2*, *1*, 73–78 (DOI: [10.1002/wcms.81](https://doi.org/10.1002/wcms.81))

### BibTeX

```text
@article{ORCA,
author = {Neese,F.},
title = {The ORCA program system},
journal = {WIRES Comput. Molec. Sci.},
volume = {2},
number = {1},
pages = {73-78},
DOI = {10.1002/wcms.81},
year = {2012},
type = {journal Article}
}
```

ORCA 6 的当前更新版本为：

Neese, F. *Software update: the ORCA program system -- Version 6.0* *Wiley Interdiscip. Rev.: Comput. Mol. Sci.*, **2025**, *15*, *2*, e70019 (DOI: [10.1002/wcms.70019](https://doi.org/10.1002/wcms.70019))

**BibTeX:**

```text
@article{ORCA6,
author = {Neese, Frank},
title = {Software Update: The ORCA Program System—Version 6.0},
journal = {Wiley Interdiscip. Rev. Comput. Mol. Sci.},
volume = {15},
number = {2},
pages = {e70019},
keywords = {ab initio calculations, density functional theory, embedding methods, global optimization, quantum chemistry},
doi = {10.1002/wcms.70019},
year = {2025}
}
```

除上述文献外，ORCA 还会在任何一次运行结束时为您提供详细的推荐引用列表。例如，对于以下输入

```text
! PBE CPCM(Water)

*XYZFILE 0 1 structure.xyz
```

输出的结尾将如下所示：

```text
--------------------------------
SUGGESTED CITATIONS FOR THIS RUN
--------------------------------

Below you find a list of papers that are relevant to this ORCA run
We neither can nor want to force you to cite these papers, but we appreciate if you do
You receive ORCA, which is the product of decades of hard work by many enthusiastic individuals, for free
The only thing we kindly ask in return is that you cite our papers,
We deeply appreciate it, if you show your appreciation for ORCA by not just citing the generic ORCA reference.

Please note that relegating all ORCA citations to the supporting information does *not* help us.
SI sections are not indexed - citations you put there will not count into any citation statistics
But we need these citations in order to attract the funding resources that allow us to do what we are doing

Therefore, if you are a happy ORCA user, please consider citing a few of the papers listed below in the main body of your paper

In addition to the list printed below, the program has created the file orca.bibtex that contains the list in bibtex format
You can import this file easily into all common literature databanks and citation aid programs

List of essential papers. We consider these as the minimum necessary citations

  1. Neese,F.
     Software update: the ORCA program system, version 5.0
     WIRES Comput. Molec. Sci., 2022 12(1)e1606
     doi.org/10.1002/wcms.1606

List of papers to cite with high priority. The work reported in these papers was absolutely
necessary for this run to complete.
Our perspective: the developers of density functionals and basis sets usually get cited in chemistry papers
Good! But without the algorithms to do something with them, the functionals or basis sets would not do anything.
Hence, in our opinion, the algorithm design and method developments papers are equally worthy of getting cited

  1. Neese,F.
     An improvement of the resolution of the identity approximation for the formation of the Coulomb matrix
     J. Comp. Chem., 2003 24(14)1740-1747
     doi.org/10.1002/jcc.10318
  2. Garcia-Rates,M.; Neese,F.
     Effect of the Solute Cavity on the Solvation Energy and its Derivatives within the Framework of the Gaussian Charge Scheme
     J. Comput. Chem., 2020 41 922-939
     doi.org/10.1002/jcc.26139
  3. Neese,F.
     The SHARK Integral Generation and Digestion System
     J. Comp. Chem., 2022  1-16
     doi.org/10.1002/jcc.26942

List of suggested additional citations. These are papers that are important in the 'surrounding' of 
of this run, or papers that preceded the highly important papers. If you like your results we are grateful for a citation.

  1. Neese,F.
     The ORCA program system
     WIRES Comput. Molec. Sci., 2012 2(1)73-78
     doi.org/10.1002/wcms.81
  2. Neese,F.
     Software update: the ORCA program system, version 4.0
     WIRES Comput. Molec. Sci., 2018 8(1)1-6
     doi.org/10.1002/wcms.1327
  3. Neese,F.; Wennmohs,F.; Becker,U.; Riplinger,C.
     The ORCA quantum chemistry program package
     J. Chem. Phys., 2020 152 Art. No. L224108
     doi.org/10.1063/5.0004608

List of optional additional citations

  1. Neese,F.
     Approximate second-order SCF convergence for spin unrestricted wavefunctions
     Chem. Phys. Lett., 2000 325(1-3)93-98
     doi.org/10.1016/s0009-2614(00)00662-x
```

可以看到，即使是隐式水（implicit water）中的简单单点计算，也用到了多种方法。这些方法乍看之下可能并不明显，但都可以被引用。例如，ORCA 使用了改进的 CPCM 处理，应按如下方式引用：

```text
  3. Garcia-Rates,M.; Neese,F.
     Effect of the Solute Cavity on the Solvation Energy and its Derivatives within the Framework of the Gaussian Charge Scheme
     J. Comput. Chem., 2020 41 922-939
     doi.org/10.1002/jcc.26139
```

为方便起见，ORCA 还会提供一个 `basename.bibtex` 文件，其中包含 BibTeX 条目，可轻松导出到任何文献管理软件或您的 LaTeX 参考文献中。
