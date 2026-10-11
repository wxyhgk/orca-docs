<a id="sec:howtocite"></a>
# How to cite

As ORCA is, and will always, be free for academic use, the people behind ORCA rely on being cited for their hard work developing it
and making it the useful tool it actually is. Therefore, we kindly ask you to not only cite the actual generic ORCA reference of the used
version but also the individual works relevant to the methods used in your ORCA calculations. To identify these more easily, we added an
automated printout to ORCA 6 that provides you with recommendations.

The generic reference for ORCA is:

Neese, F. *The ORCA program system* *Wiley Interdiscip. Rev.: Comput. Mol. Sci.*, **2012**, *2*, *1*, 73–78 (DOI: [10.1002/wcms.81](https://doi.org/10.1002/wcms.81))

**BibTeX:**
```text
@article{ORCA,
author = {Neese,F.},
title = {The ORCA program system},
journal = {Wiley Interdiscip. Rev. Comput. Mol. Sci.},
volume = {2},
number = {1},
pages = {73-78},
DOI = {10.1002/wcms.81},
year = {2012},
}
```

The current update for ORCA 6 is:

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
doi = {10.1002/wcms.70019},
year = {2025}
}
```

Beside these ORCA provides you with a detailed list of recommended citations at the end of any ORCA run. For example for the input

```text
! PBE CPCM(Water)

*XYZFILE 0 1 structure.xyz
```

the end of the output will look like:

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
     Software update: the ORCA program system, version 6.0
     WIRES Comput. Molec. Sci., 2025 15(2) e70019
     doi.org/10.1002/wcms.70019

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

Here you see, that even a simple single point calculation in implicit water makes use of various methods that may not be obvious at first glance but may be cited.
For example ORCA uses an improved CPCM treatment that should be cited as:

```text
  3. Garcia-Rates,M.; Neese,F.
     Effect of the Solute Cavity on the Solvation Energy and its Derivatives within the Framework of the Gaussian Charge Scheme
     J. Comput. Chem., 2020 41 922-939
     doi.org/10.1002/jcc.26139
```

For convenience, ORCA further provides a `.bibtex` file that contains BibTeX entries that can easily be exported to any reference manager or your LaTeX bibliography.

