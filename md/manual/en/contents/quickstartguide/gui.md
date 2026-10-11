```{index} Graphical User Interfaces (GUI)
```

(sec:quickstartguide.gui)=
# Graphical User Interfaces (GUI)

Currently, there is no native graphical user interface (GUI) developed by the ORCA developers. However, there are several
programs that provide functionalities to create ORCA inputs and read, and visualize ORCA output files. Some useful programs
are outlined in {numref}`tab:quickstartguide.gui.programlist` and some applications can be found at the [ORCA tutorials website](https://www.faccts.de/docs/orca/6.0/tutorials/).

:::{warning}
None of the programs mentioned are developed by the ORCA team. We can therefore not guarantee their functionality. 
Please contact the developers of the respective program in case of problems and feature requests.
:::


:::{raw} latex
\begingroup
\footnotesize
:::

:::{tabularcolumns} \Y{0.15}\Y{0.25}\Y{0.6}
:::
(tab:quickstartguide.gui.programlist)=
:::{flat-table} Selected programs that may be used as GUI to ORCA.
:header-rows: 1
:class: longtable
:class: footnotesize

   * - Program
     - Platform
     - Comment
   * - [Avogadro 2](https://two.avogadro.cc/index.html)
     - Windows, Linux, MacOS
     - 3D molecule builder, creation of ORCA input, visualization of ORCA outputs.
   * - [ChimeraX](https://www.cgl.ucsf.edu/chimerax/)
     - Windows, Linux, MacOS
     - Visualization of ORCA outputs. Very powerful visualization suite. The [SEQCROW](https://github.com/QChASM/SEQCROW) plugin is very useful. It can be downloaded from the `Tools/More`$\rightarrow$`Tools` menu.
   * - [Chemcraft](https://www.chemcraftprog.com/)
     - Windows, Linux
     - 3D molecule builder, creation of ORCA input, visualization of ORCA outputs. For Linux, we recommend to use the Windows version via a virtual machine. 
:::
:::{raw} latex
\endgroup
:::

:::{note}
The ORCA enhanced version of Avogadro 1 was not further developed or tested for ORCA 6 and beyond! We recommend to try Avogadro 2 instead.
:::