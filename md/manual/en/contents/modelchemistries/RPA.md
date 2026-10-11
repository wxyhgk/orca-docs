
(sec:modelchemistries.rpa)=
# Random Phase Approximation (RPA)
```{index} Random Phase Approximation, RPA
```

The random phase approximation is a rather different DFT method that is
based on the frequency dependent response function. It is more expensive
than standard DFT (same order of magnitude as RI-MP2), has many
attractive features, in particular it's good to excellent accuracy while
being essentially non-empirical. The seminal work that established RPA
in a quantum chemical context is due to Furche and is based on the
original work of Langreth and Perdew. The implementation in ORCA closely
follows the work of Görling and co-workers who we also gratefully
acknowledge for help with the implementation.

The RPA energy is calculated using some set of input orbitals and
orbitals energies (in practice, PBE orbitals and energies are
recommended). The calculation proceeds by a numerical integration over
frequencies:

$$E_{RPAC} \approx - \frac{\pi}{2}\sum_{g}^{}{w_{g}\sum_{K}^{}h_{K}}\left( \omega_{g} \right)$$

$$h_{K}(\omega) = - log\left( 1 + x_{K}(\omega) \right) + x_{K}(\omega)$$

Where $x_{K}$ are the negative eigenvalues of the Kohn-Sham response
matrix expressed in an auxiliary fitting basis (an auxiliarly basis of
the '/C' type).

$$X_{KL}(\omega) = \sum_{i}^{}{\left( \mathbf{X}^{i} \right)^{T}\mathbf{Y}^{i}}(\omega)$$

With

$$X_{aK}^{i}\mathbf{=}\left( ia|K \right)$$

$$Y_{aK}^{i}(\omega)\mathbf{=}\left( ia|K \right)\lambda_{ia}(\omega)$$

$$\lambda_{ia} = f_{\sigma}\frac{\epsilon_{i} - \epsilon_{a}}{\left( \epsilon_{i} - \epsilon_{a} \right)^{2} + (\omega)^{2}}$$

Here $\epsilon_{i},\epsilon_{a}$ are occupied and virtual orbital
energies from the SCF calculation $(ia | K)$ is a three-index
electron repulsion integral in the MO basis $f_{\sigma} = 4$ for
closed-shell states and $f_{\sigma} = 2$ for spin-unrestricted
calculations. The numerical integration is carried out with a
Gauss-Legendre quadrature using the weights and frequencies given by:

$$w_{g} = w_{g0}\frac{5}{\left( 1 - \omega_{g0} \right)^{2}}$$

$$\omega_{g} = \frac{5}{2}\left( \frac{1 + \omega_{g0}}{1 - \omega_{g0}} \right)$$

Where $w_{g0}$ and $\omega_{g0}$ are the Gauss-Legendre weights and
roots mapped on the interval -1 to 1.

The usage of RPA in ORCA is straightforward

```orca
! PBE RPAC def2-SVP def2/J def2-SVP/C
# we need a /C basis for RPAC and the /J basis for PBE

%method RPACNPoints 50  # Number of numerical integration points (def=50)
end
```

:::{note}
-   This is a pilot implementation that only features closed-shell and
    spin-unrestricted energies. Gradients are done numerically and
    density matrices are the ones from the underlying DFT calculation,
    NOT genuine RPA densities.
-   Excited states and response properties are NOT available with this
    method.
-   The method requires an integral transformation with scaling O(N$^4$)
    and on the order of 50 diagonalizations of the response matrix which
    is of dimension NAUXC. This can become expensive for larger
    molecules.
:::

```{bibliography} ../../bibliography.bib
:list: enumerated
:filter: False

LANGRETH19751425
FurchePhysRevB2001
FurcheJCP2008
TrushinJCP2021
```
