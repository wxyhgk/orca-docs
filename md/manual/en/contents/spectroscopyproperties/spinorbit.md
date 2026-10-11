```{index} Spin-Orbit Coupling, SOMF, AMFI
```

(sec:spectroscopyproperties.soc)=
# The Spin-Orbit Coupling Operator

Several variants of spin-orbit coupling operators can be used for
property calculations {cite}`neese2005jchemphys`. They are based on effective
potential and mean-field approaches, and have various parameters that
can be selected via the `%rel` block. Note that the SOMF operator
depends on the density matrix, so the operator itself can differ for
example between a CASSCF and an MRCI calculation.

**Note**: The defaults have slightly changed in ORCA 5.0, see `SOCFlags`
in the following.

```orca
%rel
     # ---------------------------------------------------
     # SPIN ORBIT COUPLING OPERATORS
     # ---------------------------------------------------
     SOCType 0  # none
             1  # effective nuclear charge
             2  # DEPRECATED
             3  # mean-field/effective potential (default)
             4  # DEPRECATED
     # ---------------------------------------------------
     # Flags for construction of potential; operative
     # only for SOCType 3.
     # ---------------------------------------------------
     SOCFlags 1,4,3,0 # default if nothing is specified
                      # 1,3,3,0 default if RI is applied and AuxJ available
                      # e.g. when using !RIJCOSX (default for DFT) or !RIJONX     
     # Flag 1 = 0 - do not include 1-electron terms
     #        = 1 - do include 1-electron terms
     # Flag 2 = 0 - do not include Coulomb terms
     #        = 1 - compute Coulomb terms fully numeric
     #        = 2 - compute Coulomb term seminumeric
     #        = 3 - compute Coulomb term with RI approx
     #        = 4 - compute Coulomb term exactly
     # Flag 3 = 0 - do not include exchange terms
     #        = 1 - do include local X-alpha exchange
     #              the X-Alpha parameter can be chosen via
     #              % rel Xalpha 0.7 (default)
     #        = 2 - same as 1 but with sign reversed
     #        = 3 - exchange via one-center exact
     #              integrals including the spin-other
     #              orbit interaction
     #        = 4 - all exchange terms full analytic
     #              (this is expensive)
     # Flag 4 = 0 - do not include DFT local correlation
     #              terms
     #        = 1 - do include local DFT correlation (here
     #              this is done with VWN5)
     #
     SOCMaxCenter 4 # max. number of centers to include in
                    # the integrals (not fully consistently
                    # implemented yet; better leave equal to 4)
     #  The following simple input equivalents can also be used:
     #  SOMF(1X)      = SOCType 3, SOCFlags 1,2,3,0 and SOCMaxCenter 4
     #  RI-SOMF(1X)   = SOCType 3, SOCFlags 1,3,3,0 and SOCMaxCenter 4
     #  VEFF-SOC      = SOCType 3, SOCFlags 1,3,1,1 and SOCMaxCenter 4
     #  VEFF(-2X)-SOC = SOCType 3, SOCFlags 1,3,2,1 and SOCMaxCenter 4
     #  AMFI          = SOCType 3, SOCFlags 1,4,3,0 and SOCMaxCenter 1
     #  NOTE: If you choose the RI option you need to specify an auxiliary basis
     #        set even if the underlying SCF calculation does not make use of any
     #        from of RI!
     # -----------------------------------------------
     # For the effective nuclear charge SOC operator
     # the nuclear charges can be adjusted.
     # -----------------------------------------------
     Zeff[26] 0.0   # set the effective nuclear charge
                    # of iron (Z = 26) to zero
     # -----------------------------------------------
     # Neglecting SOC contributions from particular
     # atoms
     # -----------------------------------------------
     SOCOff 0,5     # turn off the SOC for atoms 0 and 5
                    # this makes sense if the SOC operator
                    # has only one center contributions
                    # (e.g. effective nuclear charge)
```

Simple input equivalents are listed in {numref}`tab:spectroscopyproperties.soc.keywords.simple` 
and described in more detail in {cite}`neese2005jchemphys`. 
More details on the (deprecated) AMFI-A approach which uses pre-calculated atomic densities can be found in {cite}`ganyushin2013jcp`.

The Breit-Pauli spin-orbit coupling operator is given by:

$$\hat{{H} }_{\text{SOC} } =\hat{{H} }_{\text{SOC} }^{\left( 1 \right)}
+\hat{{H} }_{\text{SOC} }^{\left( 2 \right)}$$

with the one- and two-electron contributions

$$\hat{{H} }_{\text{SOC} }^{\left( 1 \right)} =\frac{\alpha^{2} }{2}\sum\limits_i
{\sum\limits_A { Z_{A} \frac{\left({ \mathrm{\mathbf{r} }_{i} -\mathrm{\mathbf{R} }_{A} } \right)\times \mathrm{\mathbf{p} }_{i} }{\left|{ \mathrm{\mathbf{r} }_{i} -\mathrm{\mathbf{R} }_{A} } \right|^{3} }\hat{{s} }_{i} } } \equiv \frac{\alpha
^{2} }{2}\sum\limits_i { \sum\limits_A { Z_{A} r_{iA}^{-3} { \mathrm{\mathbf{ \hat{l} }} }_{iA} \mathrm{\mathbf{\hat{{s} }} }_{i} } }
$$ (eqn:240)

$$\hat{{H} }_{\text{SOC} }^{\left( 2 \right)} =-\frac{\alpha^{2} }{2}\sum\limits_i
{\sum\limits_{j\ne i} { \frac{\left({ \mathrm{\mathbf{r} }_{i} -\mathrm{\mathbf{r} }_{j} } \right)\times \mathrm{\mathbf{p} }_{i} }{\left|{ \mathrm{\mathbf{r} }_{i} -\mathrm{\mathbf{r} }_{j} } \right|^{3} }\left({ \mathrm{\mathbf{\hat{{s} }} }_{i}
+2{\mathrm{\mathbf{\hat{s} }} }_{j} } \right)} }
$$ (eqn:241)

$$\hspace{2cm}
\equiv -\frac{\alpha^{2} }{2}\sum\limits_i
{\sum\limits_{j\ne i} { \mathrm{\mathbf{\hat{{l} }} }_{ij} r_{ij}^{-3} \left({\mathrm{\mathbf{\hat{{s} }} }_{i} +2\mathrm{\mathbf{\hat{{s} }} }_{j} } \right)} }
$$ (eqn242)

:::{note}
One attractive possibility is to represent the SOC by the spin-orbit
mean-field (SOMF) method developed by Hess et al.,{cite}`hess1996cpl` widely
used in the AMFI program by Schimmelpfennig {cite}`schimmelpfennigAMFIprog`
and discussed in detail by Berning et al.{cite}`berning2000molphys` as well
as in ref. {cite}`neese2005jchemphys`. In terms of an (orthonormal)
one-electron basis, the matrix elements of the SOMF operator are:

$$\begin{array}{c}
 h_{rs}^{K;\text{SOC} } =\left({ p\left|{ \hat{{h} }_{K}^{1el-\text{SOC} } } \right|q}
\right) \\
 +\sum\limits_{rs} { P_{rs} } \left[{ \left({ pq\left|{ \hat{{g} }_{K}^{\text{SOC} } }
\right|rs} \right)-\frac{3}{2}\left({ pr\left|{ \hat{{g} }_{K}^{\text{SOC} } }
\right|sq} \right)-\frac{3}{2}\left({ sq\left|{ \hat{{g} }_{K}^{\text{SOC} } }
\right|pr} \right)} \right] \\
 \end{array}
$$ (eqn:257)

and:

$$\hat{{h} }_{k}^{1el-\text{SOC} } \left({ \mathrm{\mathbf{r} }_{i} } \right)=\frac{\alpha
^{2} }{2}\sum\limits_i { \sum\limits_A { Z_{A} r_{iA}^{-3} { \mathrm{\mathbf{\hat{l} }} }_{iA;k} } }
$$ (eqn:258)

$$\hat{{g} }_{k}^{\text{SOC} } \left({ \mathrm{\mathbf{r} }_{i,} \mathrm{\mathbf{r} }_{j} }
\right)=-\frac{\alpha^{2} }{2}\mathrm{\mathbf{\hat{{l} }} }_{ij;k} r_{ij}^{-3}
$$ (eqn:259)

$\mathrm{\mathbf{\hat{l} }}_{iA} =(\mathrm{\mathbf{\hat{r} }}_{i} -\mathrm{\mathbf{R} }_{A}
)\times \mathrm{\mathbf{\hat{p} }}_{i}$ is the angular momentum of the
$i$'th electron relative to nucleus $A$. The vector
$\mathrm{\mathbf{\hat{r} }}_{iA} ={\mathrm{\mathbf{\hat{r} }} }_{i} -\mathrm{\mathbf{R} }_{A}$
of magnitude $r_{iA}$ is the position of the $i$'th electron relative to
atom $A$. Likewise, the vector
${\mathrm{\mathbf{\hat{r} }} }_{ij} =\mathrm{\mathbf{\hat{r} }}_{i} -\mathrm{\mathbf{\hat{r} }}_{j}$
of magnitude $r_{ij}$ is the position of the $i$th electron relative to
electron $j$ and
$\mathrm{\mathbf{\hat{l} }}_{ij} =(\mathrm{\mathbf{\hat{r} }}_{i}
-\mathrm{\mathbf{\hat{r} }}_{j} )\times \mathrm{\mathbf{\hat{p} }}_{i}$
is its angular momentum relative to this electron. **P** is the charge
density matrix of the electron ground state
($P_{pq} =\left\langle { 0SS\left|{E_{q}^{p} } \right|0SS} \right\rangle$with
$E_{q}^{p} =a_{p\beta }^{+}
a_{q\beta } +a_{p\alpha }^{+} a_{q\alpha }$ where $a_{p\sigma }^{+}$ and
$a_{q\sigma }$ are the usual Fermion creation and annihilation
operators).
:::

This operator would be hard to handle exactly; therefore it is common to
introduce mean field and/or effective potential approaches in which the
operator is written as an effective one-electron operator:

$$\hat{{H} }_{\text{SOC} } \cong \sum\limits_i { \mathrm{\mathbf{\hat{{h} }} }_{i}^{\left({\text{eff} } \right)} \mathrm{\mathbf{\hat{{s} }} }_{i} }
$$ (eqn:243)

The simplest approximation is to simply use the one-electron part and
regard the nuclear charges as adjustable parameters. Reducing their
values from the exact nuclear charge is supposed to account in an
average way for the screening of the nuclear charge by the electrons. In
our code we use the effective nuclear charges of Koseki et al. ({cite}`schmidt1992phys,koseki1995phys,koseki1998phys`) This
approximation introduces errors which are usually smaller than 10% but
sometimes are larger and may approach 20% in some cases. The
approximation is best for first row main group elements and the first
transition row (2p and 3d elements). For heavier elements it becomes
unreliable.

A much better approximation is to take the two-electron terms into
account precisely. Without going into details here -- the situation is
as in Hartree-Fock (or density functional) theory and one gets Coulomb,
exchange and correlation terms. The correlation terms (evaluated in a
local DFT fashion) are negligible and can be safely neglected. They are
optionally included and are not expensive computationally. The Coulomb
terms is (after the one-electron term) the second largest contribution
and is expensive to evaluate exactly. The situation is such that in the
Coulomb-part the spin-other orbit interaction (the second term in the
two-electron part) does not contribute and one only has to deal with the
spin-own-orbit contribution. The exact evaluation is usually too
expensive to evaluate. The RI and seminumeric approximation are much
more efficient and introduce only minimal errors (on the order of
usually not more than 1 ppm in g-tensor calculations for example) and
are therefore recommended. The RI approximation is computationally more
efficient. Please note that you have to specify an auxiliary basis set
to take advantage of the RI approximation, even if the preceding SCF
calculation does not make use of any form of RI. The one-center
approximation to the Coulomb term introduces much larger errors. The
fully numeric method is both slower and less accurate and is not
recommended.

The exchange term has contributions from both the spin-own-orbit and
spin-other-orbit interaction. These are taken both into account in the
mean-field approximation which is accessed by `Flag 3 = 3`. Here a
one-center approximation is much better than for the Coulomb term since
both the integrals and the density matrix elements are short ranged.
Together with the Coulomb term this gives a very accurate SOC operator
which is recommended. The DFT-Veff operator suffers from not treating
the spin-other-orbit part in the exchange which gives significant errors
(also, local DFT underestimates the exchange contributions from the
spin-same-orbit interaction by some 10% relative to HF but this is not a
major source of error). However, it is interesting to observe that in
the precise analytical evaluation of the SOMF operator, the
spin-other-orbit interaction is exactly -2 times the spin-own-orbit
interation. Thus, in the DFT framework one gets a *much* better SOC
operator if the sign of the DFT exchange term is simply reversed! This is accessed by` Flag 3 = 2`.

## Exclusion of Atomic Centers

In ORCA it is possible to change the spin-orbit coupling operator in
order to exclude contributions from user-defined atoms. This approach
can be useful, for example, in quantifying the contribution of the
ligands to the zero-field splitting (ZFS); for an application of this
method see Ref. {cite}`suturina2015inorgchem`.

This is illustrated for the calculation of the SOC contribution to the
ZFS of the triplet oxygen molecule. Using the input below we start by a
normal calculation of the ZFS, including both oxygen atoms. Note that we
use here the effective nuclear charge operator. This is required as not
all implemented SOC operators are compatible with the decomposition in
terms of individual centers contributions.

```{literalinclude} ../../orca_working_input/C06S25_511.inp
:language: orca
```

The calculated value of the D parameter is approximately 2.573
cm$^{-1}$. In a second calculation we exclude the contribution from the
first oxygen atom. For this we change the `%rel` block to the one below.

```orca
%rel
    SOCType 1
    SOCOff 0
    end
```

Now the D parameter is calculated to be approximately 0.643 cm$^{-1}$, a
result that deviates quite significantly from half of the value
calculated previously, implying that non-additive effects are important.
In addition to the effective nuclear charge operator, the AMFI-A
operator described previously can be used. Given that this is based on
precalculated atomic densities, it might be preferred for heavier
elements where the effective nuclear charge operator becomes unreliable.
The method is not limited to CASSCF calculations as described above, and
can be used in DFT, MRCI and ROCIS calculations.

(sec:spectroscopyproperties.soc.keywords)=
## Simple Input Keywords

:::{raw} latex
\begingroup
\footnotesize
:::
(tab:spectroscopyproperties.soc.keywords.simple)=
:::{flat-table} Simple input keywords to choose the SOC operator handling and their equivalent `%rel` block settings
:header-rows: 1
:class: footnotesize
* - Keyword
  - `SOCType`
  - `SOCFlags`
  - `SOCMaxCenter`
* - `ZEFF-SOC`
  - 1
  -
  -
* - `SOMF`
  - 3
  - 1,4,4,0
  - 4
* - `SOMF(1X)`
  - 3
  - 1,2,3,0
  - 4
* - `RI-SOMF`
  - 3
  - 1,3,3,0 
  - 4
* - `RI-SOMF(1X)`
  - 3
  - 1,3,3,0 
  - 4
* - `SOMF(4X)`
  - 3
  - 1,2,4,0
  - 4
* - `RI-SOMF(4X)`
  - 3
  - 1,3,4,0
  - 4
* - `VEFF-SOC`
  - 3
  - 1,3,1,1
  - 4
* - `VEFF(-2X)-SOC`
  - 3
  - 1,3,2,1
  - 4
* - `AMFI`
  - 3
  - 1,4,3,0
  - 1
:::
:::{raw} latex
\endgroup
:::