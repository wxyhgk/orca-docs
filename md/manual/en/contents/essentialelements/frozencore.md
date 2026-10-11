```{index} Frozen Core
```

(sec:essentialelements.frozencore)=
# Frozen Core Options

The frozen core (FC) approximation is usually applied in correlated
calculation and consists in neglecting correlation effects for electrons
in the low-lying core orbitals. The FC approximation and the number of
core electrons per element can be adjusted in the %method block. The
default number of core electrons per element is listed in {numref}`table:Frozen-Core-Defaults`.

(table:Frozen-Core-Defaults)=
::::{list-table} Default values for number of frozen core electrons.
:header-rows: 0
:widths: 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
* - H
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - He
* - 0
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 0
* - Li
  - Be
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - B
  - C
  - N
  - O
  - F
  - Ne
* - 0
  - 0
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 2
  - 2
  - 2
  - 2
  - 2
  - 2
* - Na
  - Mg
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - Al
  - Si
  - P
  - S
  - Cl
  - Ar
* - 2
  - 2
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 
  - 10
  - 10
  - 10
  - 10
  - 10
  - 10
* - K
  - Ca
  - Sc
  - Ti
  - V
  - Cr
  - Mn
  - Fe
  - Co
  - Ni
  - Cu
  - Zn
  - Ga
  - Ge
  - As
  - Se
  - Br
  - Kr
* - 10
  - 10
  - 10
  - 10
  - 10
  - 10
  - 10
  - 10
  - 10
  - 10
  - 10
  - 10
  - 18
  - 18
  - 18
  - 18
  - 18
  - 18
* - Rb
  - Sr
  - Y
  - Zr
  - Nb
  - Mo
  - Tc
  - Ru
  - Rh
  - Pd
  - Ag
  - Cd
  - In
  - Sn
  - Sb
  - Te
  - I
  - Xe
* - 18
  - 18
  - 28
  - 28
  - 28
  - 28
  - 28
  - 28
  - 28
  - 28
  - 28
  - 28
  - 36
  - 36
  - 36
  - 36
  - 36
  - 36
* - Cs
  - Ba
  - Lu
  - Hf
  - Ta
  - W
  - Re
  - Os
  - Ir
  - Pt
  - Au
  - Hg
  - Tl
  - Pb
  - Bi
  - Po
  - At
  - Rn
* - 36
  - 36
  - 46
  - 46
  - 46
  - 46
  - 46
  - 46
  - 46
  - 46
  - 46
  - 46
  - 68
  - 68
  - 68
  - 68
  - 68
  - 68
* - Fr
  - Ra
  - Lr
  - Rf
  - Db
  - Sg
  - Bh
  - Hs
  - Mt
  - Ds
  - Rg
  - Cn
  - 
  - 
  - 
  - 
  - 
  - 
* - 68
  - 68
  - 68
  - 100
  - 100
  - 100
  - 100
  - 100
  - 100
  - 100
  - 100
  - 100
  - 
  - 
  - 
  - 
  - 
  - 
* - Lanthanides
  - 
  - 
  - La
  - Ce
  - Pr
  - Nd
  - Pm
  - Sm
  - Eu
  - Gd
  - Tb
  - Dy
  - Ho
  - Er
  - Tm
  - Yb
  - 
* - 
  - 
  - 
  - 36
  - 36
  - 36
  - 36
  - 36
  - 36
  - 36
  - 36
  - 36
  - 36
  - 36
  - 36
  - 36
  - 36
  - 
* - Actinides
  - 
  - 
  - Ac
  - Th
  - Pa
  - U
  - Np
  - Pu
  - Am
  - Cm
  - Bk
  - Cf
  - Es
  - Fm
  - Md
  - No
  - 
* - 
  - 
  - 
  - 68
  - 68
  - 68
  - 68
  - 68
  - 68
  - 68
  - 68
  - 68
  - 68
  - 68
  - 68
  - 68
  - 68
  - 
:::: 

For systems containing heavy elements, core electrons might have higher
orbital energies compared to the orbital energies of valence MOs of some
lighter elements. In that case, core electrons might be included in the
correlation calculation, which ultimately leads to large errors in
correlation energy. In order to prevent this, the MO ordering is checked: 
Do all lower energy MOs in the core region have core electron character, 
i.e. are they strongly localized on the individual elements? 
For post-(CAS)SCF calulations, this check is always performed both 
after the SCF calculation, and after the initial guess 
(because the SCF may be skipped with `!NoIter`). For other calculations,
the check is off by default but may be switched on with the `CheckFrozenCore` 
keyword in the `%method` block.
If core orbitals are found in the valence region,
while more delocalized orbitals are found in the core region, the
corresponding MO pairs are swapped. This behavior can be disabled using
the `CorrectFrozenCore` keyword.

```orca
%method 
  FrozenCore FC_ELECTRONS #Freeze all core electrons
             FC_EWIN      #Freeze selected core electrons via an energy window
                          #e.g. for MP2: %mp2 EWin EMin,EMax      
             FC_NONE      #No frozencore approximation 
             -n           #Freeze a total of n electrons

  NewNCore Bi 68 end      #Set the number of core electrons for Bi to 68
  CheckFrozenCore   true  #Check whether frozen core orbitals are ordered correctly
                          #Default: true only for post-(CAS)SCF calculations
  CorrectFrozenCore true  #Whether to rotate valence orbitals out of the
                          #core region
end
```

:::{Note}

-   The FrozenCore options are applied to all post Hartree-Fock methods.

-   If including all electrons is desired, the `!NoFrozenCore` keyword
    can be simply inserted. For MP2: Frozen virtual orbitals are not
    allowed in gradient runs or geometry optimization!

-   If ECPs are used, the number for NewNCore has to include the
    electrons represented by the ECPs as well. E.g. if an element is
    supposed to have 60 electrons in the ECP and additional 8 electrons
    should be frozen in the correlation calculation, NewNCore should be
    68.

-   In ORCA we use rather conservative frozencore settings, i. e. a
    large number of electrons are included in the correlation treatment.
    Therefore, we recommend to use properly optimized correlating basis
    functions in all cases, such as the cc-pwCVXZ basis sets.

-   For DLPNO calculations the virtual space for core-core and
    core-valence correlation is adjusted by default, which is described
    in detail in
    section {ref}`sec:modelchemistries.mdci.dlpnocorepno`.

-   In general, `NewNCore` only has an effect in calculations with
    `FC_ELECTRONS`. In calculations using the DLPNO approximation
    (except DLPNO-NEVPT2), `NewNCore` has also an effect in the other
    cases, as is described in
    section {ref}`sec:modelchemistries.mdci.dlpnocorepno`.

-   Double-hybrid density functional
    (section {ref}`sec:modelchemistries.dft.doublehybriddft`)
    calculations by default use the FrozenCore option for the
    perturbative part, as is the case for MP2.
:::