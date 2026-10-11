<a id="sec:modelchemistries.analyticDFT"></a>
# Analytic Density Functional Theory (ADFT)

The method that has come to be known as "analytic density functional
theory" (ADFT) is a variant of DFT that avoids the very common use of
numerical integration. Early approaches to a grid DFT were relying on
diagonalizing the density matrix and applying the DFT functional to the
eigenvalues of the density followed by back transformation. These
methods work but have been abandoned in favor of numerical integration.

ORCA features an alternative approach, that is, however, still limited
to the most elementary of all density functionals, namely the
Hartree-Fock Slater (HFS) or, in a slightly parameterized form, the
X-Alpha method. The method is based on fitting the Coulomb and exchange
potentials to separate auxiliary basis sets. In the case of the Coulomb
interaction, this is very well known in form of the RI-J approximation.
For the exchange, the ADFT construction is based on a related but more
tricky development given the nonlinear dependency of the Slater-exchange
on the density.

The exchange energy is:

$$
E_{X}^{\sigma} = - \frac{3}{4}\left( \frac{6}{\pi} \right)^{\frac{1}{3}}\in t_{}^{}{\rho_{\sigma}^{4/3}\left( r \right)}
$$

Leading to the exchange potential:

$$
V_{X}^{\sigma}\left( r \right) = - \left( \frac{6}{\pi} \right)^{\frac{1}{3}}\rho_{\sigma}^{1/3}\left( r \right)
$$

$$
C_{X} = - \left( \frac{6}{\pi} \right)^{\frac{1}{3}} = - 1.24\ldots
$$

Replacing$C_{X}$ by${\frac{3}{2}\alpha C}_{X}$ leads to the X-Alpha
method. Here,$\alpha$ is an empirical parameter with default value 2/3
in order to recover the HFS method. Empirically, it has been found,
however, that values between 2/3 and 1 are more suitable with the value
0.7 being a widely accepted default.

We now have to deal with the odd power law, using techniques developed
by Cook and also by Dunlap and co-workers. The idea here is to expand
${\rho_{\sigma}(r)}^{\frac{1}{3}}$ itself in another auxiliary basis
set:

$$
{\rho_{\sigma}\left( r \right)}^{1/3} = \sum_{K}^{}{a_{K}^{\sigma}A_{K}(r)}
$$

It turns out that we also need (or perhaps not need but want):

$$
{\rho_{\sigma}\left( r \right)}^{2/3} = \sum_{K}^{}{b_{K}^{\sigma}B_{K}(r)}
$$

The functions {A} and {B} are uncontracted exchange auxiliary basis
functions. The easiest choice for these auxiliary basis sets is to
derive them from the Coulomb fitting basis set, possibly with
restricting the maximum angular momentum. Alternatively, the program can
provide one of presently four fitting basis of increasing size called
XFIT/1 through XFIT/4.

Based on theoretical arguments, the exponents of these fitting bases are
scaled differently. The exponents of the A-basis are scaled by the
factor 1/3 whereas those of the B-basis are scaled by 2/3. Dunlap
remarked that it is sufficient to scale the exponents of the s-functions
and we have followed that recommendation but have not observed large
differences to scaling all exponents.

The determination of the fitting coefficients {a} and {b} leads to a set
of nonlinear equations that can, for example, be solved by a
Newton-Raphson procedure. They can be more efficiently also calculated
by numerical integration, but that defeats the purpose of the
methodology. The equations to be satisfied are:

$$
\frac{\partial E}{\partial a_{K}^{\sigma}} = C_{X}\left\{ \sum_{\mu\nu}^{}{P_{\mu\nu}^{\sigma}(\mu\nu A_{K})} - \sum_{LM}^{}{a_{L}^{\sigma}b_{M}^{\sigma}(A_{K}A_{L}B_{M})} \right\}
$$

$$
\frac{\partial E}{\partial b_{M}^{\sigma}} = \frac{1}{2}C_{X}\left\{ - \sum_{KL}^{}{a_{K}^{\sigma}a_{L}^{\sigma}\left( A_{K}A_{L}B_{M} \right)} + \sum_{N}^{}{b_{N}^{\sigma}(B_{M}B_{N})} \right\}
$$

Where$(A_{K}A_{L}B_{M})$ are 3-center overlap integrals,$\mu,\nu$ are
basis functions and$P^{\sigma}$ is the density matrix for spin$\sigma = \alpha,\beta$. One can bring that into the form:

$$
\left( H(a)^{AB} \overline{S}^{- 1} H(a)^{AB+} \right) a
= P^{X}
$$

With

$$
P_{K}^{X;\sigma} = \sum_{\mu\nu}^{}P_{\mu\nu}^{\sigma}(\mu\nu A_{L})
$$

$$
{\overline{S}}_{MN} = (B_{M}B_{N})
$$

$$
H_{KM}^{AB;\sigma} = \sum_{L}^{}{a_{L}^{\sigma}\left( A_{K}A_{L}B_{M} \right)}
$$

Which needs to be solved for$a$. We then obtain$b$ from

$$
b = \overline{S}^{- 1} H(a)^{AB+} a
$$

This is essentially the procedure followed in the ORCA implementation.
Optimized code has been written for the three center overlap integrals.

The implementation in ORCA covers closed and spin-unrestricted energies,
analytic geometry gradients, response properties and excitation energies
as well as numerical Hessians. The efficiency of the implementation is
such that energies are slower than with numeric integration while all
other steps are executed faster.

One unique opportunity that ADFT offers is to scale the exchange for
each atom in the molecule differently. This seems warranted, because
X-Alpha studies on atoms revealed that optimal$\alpha$ values change
between atoms. Some contemplation shows that this can be achieved by
scaling the density matrix for the exchange calculation as follows:

$$
P_{\mu_{A}\nu_{B}}^{\sigma} \rightarrow P_{\mu_{A}\nu_{B}}^{\sigma}\left( {\frac{3}{2}\alpha_{A}} \right)^{3/8}\left( {\frac{3}{2}\alpha_{B}} \right)^{3/8}
$$

Alpha-values can be chosen in a variety of ways other than assigning a
global value of 0.7. For example, the alpha values can be fitted to
reproduce atomic Hartree-Fock energies or atomic coupled-cluster
energies. They could also be optimized to reproduce molecular
energetics.

The usage of ADFT in ORCA is simple:

```orca
! ADFT def2-SVP def2/J XFit/3
# or ADFT(XAlpha), ADFT(HF), ADFT(CC)
# default parameters for HF are H-Kr
# default parameters for CC are H-Zn
# XFIT/1 -- XFIT/4 exists but only /3 and /4 are recommended

%method ADFTNRTol 1e-9           # tol. for NR equation solution (def=1e-9)
        ADFTNRMaxIter 6          # max no of NR iterations (def=15)
        ADFTLmaxAuxJ  5          # max L allowed in the AUXJ basis (def=3)
        ADFTLmaxAuxX  5          # max L allowed in the AUXX basis (def=2)
        ADFTXAlpha  [36] 0.71337 # array with alpha values for each element
end
```

!!! note
    -   ADFT is really limited to the HFS/X-Alpha method. It makes no sense
        to input the name of any other functional. It will be ignored. This
        is due to the way the exchange is fitted which is very specific to
        this particular functional and the whole theory would be completely
        different for other functionals.
    -   The implementation is experimental. It is motivated by the
        intellectual beauty of the construction and the fact that in early
        computational chemistry, users got a lot of mileage out of the
        method. Hence, this is a "back to the roots" kind of movement with
        the idea to perhaps take grid free DFT to new places in the future.

**Relevant Papers:**

- Neese, F. 2025, in preparation 

