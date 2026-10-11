<a id="sec:preface.howtousethismanual"></a>
# How to use this manual

The ORCA manual has been growing for decades and all developers
take great care to document and describe all features or ORCA
as good as they can. From ORCA 6.0 to ORCA 6.1 this manual has undergone a major
restructuring. What you are looking at has been and is a
huge team effort and should meet the needs of absolute beginners
with little theory background as well as the requirements of
experienced developers.

!!! note "Help us with your feedback"

    With the initial restructuring of the manual for ORCA 6.1, we made substantial changes that hopefully
    improve the readbility and general quality of the manual. However, this was only the beginning and we are
    glad to hear any constructive feedback from you via the [ORCA forum](https://orcaforum.kofo.mpg.de/app.php/portal) 
    on how to improve further future.

The new structure starts with a [quickstart guide](../quickstartguide/index_quickstartguide.md) and a
[guideline for installation](#sec:installation) that should get everyone
started. The overall structure is ordered such that
we first summarize the [essential elements of ORCA](../essentialelements/index_essentialelements.md) that a user
needs to know when perfoming standard calcuations like
[how to structure the input](#sec:essentialelements.coordinates), which
[basis sets](#sec:essentialelements.basisset) and algorithms
are available etc. Next, we outline the available [electronic structure approaches](../modelchemistries/index_modelchemistries.md)
that can be used to compute energies, structures and properties
ranging from [Hartree-Fock](#sec:modelchemistries.hftype) and [DFT](#sec:modelchemistries.dft)
to high level ab-initio methods.
The next chapter focuses on [structure and reactivity](../structurereactivity/index_structurereactivity.md) and includes
all approaches to optimize [geometries](#sec:structurereactivity.optimization),
find [transition states](#sec:structurereactivity.optimization.transitionstate)
and compute relative (free) energies in various settings.
[Molecular spectroscopy and properties](../spectroscopyproperties/index_spectroscopyproperties.md) includes everything that can
be computed once a structure has been established and ranges from
density and wavefunction analysis to ground- and excited state properties
up to complex higher order properties like, for example, [MCD](#sec:spectroscopyproperties.mcd).
The last few sections deal with important features for complex
tasks like running [molecular dynamics](../moleculardynamics/index_moleculardynamics.md),
[multiscale approaches](../multiscalesimulations/index_multiscalesimulations.md) or orchestrating
[automated workflows with ORCA](../workflowsautomatization/index_workflowsautomatization.md) using, e.g., 
the [compound](#sec:workflowsautomatization.compound) script language. Last but not least we have notes on important
[utilities](../utilitiesvisualization/index_utilitiesvisualization.md) that can be used for post-processing and some technical notes
on the [ORCA architecture](../orcaarchitecture/index_orcaarchitecture.md).

Most sections will start with a short outline of the theory with
references and some simple examples to get you started, further
details like keyword lists and advanced examples are typically found
later on in the sections.

We hope that you will find the manual useful and would be very
happy if you give feedback online in the [ORCA forum](https://orcaforum.kofo.mpg.de/app.php/portal).
