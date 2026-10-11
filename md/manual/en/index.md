# Suggested Topics

::::{grid} 1 1 2 4
:gutter: 3

:::{grid-item-card} DFT
:link: sec:modelchemistries.dft
:link-type: ref
:class-card: feature-card

![DFT](images/dft.svg)
:::

:::{grid-item-card} DLPNO-CC
:link: sec:modelchemistries.mdci.localcorrelation
:link-type: ref
:class-card: feature-card

![DLPNO-CC](images/dlpnoccsdt.svg)
:::

:::{grid-item-card} NEB-TS
:link: sec:structurereactivity.neb.nebts
:link-type: ref
:class-card: feature-card

![NEB-TS](images/nebts.svg)
:::

:::{grid-item-card} Conformers (GOAT)
:link: sec:structurereactivity.goat
:link-type: ref
:class-card: feature-card

![GOAT](images/goat.svg)
:::

::::

```{toctree}
:maxdepth: 2
:hidden:

html_versions
```

# ORCA 6.1 Manual

```{image} images/ORCA_Logo_2.*
:alt: ORCA
:width: 80%
:align: center
```

**- An *ab initio*, DFT and semiempirical SCF-MO package -**

**Version 6.1**

*Design and Scientific Directorship:*
**Frank Neese**\
*Technical Directorship:* **Frank Wennmohs**

Max-Planck-Institut für Kohlenforschung\
Kaiser-Wilhelm-Platz 1, 45470 Mülheim a. d. Ruhr, Germany\
`department-mts@kofo.mpg.de`


*With contributions from:*

*MPI für Kohlenforschung:*\
Ahmet Altun, Daniel Aravena, Michael Atanasov, Alexander A. Auer, Ute Becker,
Giovanni Bistoni, Markus Bursch, Dmytro Bykov, Marcos Casanova-Páez, Vijay G. Chilkuri, Pauline Colinet, Dipayan Datta,
Achintya Kumar Dutta, Nicolas Foglia, Dmitry Ganyushin,
Miquel Garcia-Rates, Tiago L. C. Gouveia, Yang Guo, Andreas Hansen, Ingolf Harden, Benjamin Helmich-Paris,
Lee Huntington, Róbert Izsák, Riya Kayal, Emily Kempfer, Christian Kollmar, Axel Koslowski,
Simone Kossmann, Lucas Lang, Marvin Lechner, Spencer Leger,
Dagmar Lenk, Dimitrios G. Liakos, Dimitrios Manganas,
Dimitrios A. Pantazis, Anastasios Papadopoulos, Taras Petrenko, Petra Pikulová,
Peter Pinski, Shashank V. Rao, Christoph Reimann, Marius Retegan,
Christoph Riplinger, Michael Roemelt, Masaaki Saitow,
Barbara Sandhöfer, Yorick L. A. Schmerwitz, Kantharuban Sivalingam,
Bernardo de Souza, Georgi L. Stoychev, Van Anh Tran, Willem Van den Heuvel, Zikuan Wang, Hang Xu

*FACCTs GmbH:*\
Markus Bursch, Nicolas Foglia, Miquel Garcia-Rates, Ingolf Harden, Hagen Neugebauer, Mustafa C. Ozdemir, Anastasios Papadopoulos, Christoph Plett, Christoph Riplinger, Bernardo de Souza, Georgi L. Stoychev

*Other institutions:*\
Vilhjálmur Åsgeirsson, Christoph Bannwarth, Giovanni Bistoni, Martin Brehm, Ronald Cardenas, Garnet Chan, Martina Colucci, Sebastian Ehlert, Marvin Friede, Lars Goerigk, Stefan Grimme, Waldemar Hujo, Mihály Kállay, Holger Kruse, Marcel Müller, Jiri Pittner, Philipp Pracht, Gianluca Regni, Liviu Ungur, Edward Valeev, Lukas Wittmann

*Additional contributions to the manual from:*\
Wolfgang Schneider, Gregor Giesen, Johannes Grün

```{only} html
<a href="_static/pdf/orca.pdf" download="orca_manual_6_1_0.pdf" target="_blank" class="orca-btn">Download PDF</a>
```

<!--- FRONTMATTER --->
```{raw} latex
\frontmatter
```

<!--- PREFACE --->
```{toctree}
:caption: 'Preface'
contents/preface/foreword
contents/preface/changes
contents/preface/howtocite
contents/preface/howtousethismanual
```

<!--- MAINMATTER --->
```{raw} latex
\mainmatter
```

```{toctree}
:caption: 'Main Part'
:numbered:
contents/quickstartguide/index_quickstartguide
contents/essentialelements/index_essentialelements
contents/modelchemistries/index_modelchemistries
contents/structurereactivity//index_structurereactivity
contents/spectroscopyproperties/index_spectroscopyproperties
contents/multiscalesimulations/index_multiscalesimulations
contents/moleculardynamics/index_moleculardynamics
contents/workflowsautomatization/index_workflowsautomatization
contents/utilitiesvisualization/index_utilitiesvisualization
contents/orcaarchitecture/index_orcaarchitecture
```

<!--- APPENDIX --->
```{raw} latex
\begin{appendix}
```

```{toctree}
:caption: 'Appendix'
:numbered:
contents/appendix/detailedchangelog
contents/appendix/public
contents/appendix/glossary
```

```{bibliography}
:filter: cited
```

```{raw} latex
\end{appendix}
```

```{eval-rst}
.. only:: html

   .. toctree::
      :caption: Bibliography & Index

      bibliography
      genindex
```


