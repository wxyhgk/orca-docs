

<a id="sec:essentialelements.initialguess"></a>
# Choice of Initial Guess and Restart of SCF Calculations

The initial guess is an important issue in each SCF calculation. If this
guess is reasonable, the convergence of the procedure will be much
better. ORCA makes some effort to provide a good initial guess and gives
the user enough flexibility to tailor the initial guess to his or her
needs.

The initial guess is also controlled via the `%scf` block and the
variables `Guess`, `MOInp` and `GuessMode`.

```orca
%scf
  Guess     HCore       # One electron matrix
            Hueckel     # Extended H\"uckel guess
            PAtom       # Polarized atomic densities
            PModel      # Model potential 
            MORead      # Restart from an earlier calc.
  MOInp     "Name.gbw"  # orbitals used for MORead
  GuessMode FMatrix     # FMatrix projection
            CMatrix     # Corresponding orbital projection
  AutoStart true        # try to use the orbitals from the existing
                        # GBW file of the same name (if possible)
                        # (default)
            false       # don't use orbitals from existing GBW file
end
```

<a id="sec:essentialelements.initialguess.oneElectron"></a>
## One Electron Matrix Guess

The simplest guess is to diagonalize the one electron matrix to obtain
starting orbitals. This guess is very simple but usually also a disaster
because it produces orbitals that are far too compact.

<a id="sec:essentialelements.initialguess.projection"></a>
## Basis Set Projection

The remaining guesses (may) need the projection of initial guess
orbitals onto the actual basis set. In ORCA there are two ways this can
be done. `GuessMode FMatrix` and `GuessMode CMatrix`. The results from
the two methods are usually rather similar. In certain cases
`GuessMode CMatrix` may be preferable. `GuessMode FMatrix` is simpler
and faster. In short the `FMatrix` projection defines an effective one
electron operator:

$$
\hat{f}=\sum\limits_p { \varepsilon_{p} a_{p}^{\dagger} a_{p} }\qquad \text{(eqn:49)}
$$

where the sum is over all orbitals of the initial guess orbital set,
$a_{p}^{\dagger}$ is the creation operator for an electron in guess MO
$p$, $a_{p}$ is the corresponding annihilation operator and
$\varepsilon_{i}$ is the orbital energy. This effective one electron
operator is diagonalized in the actual basis and the eigenvectors are
the initial guess orbitals in the target basis. For most wavefunctions
this produces a fairly reasonable guess.

`CMatrix` is more involved. It uses the theory of corresponding orbitals
to fit each MO subspace (occupied, partially occupied or spin-up and
spin-down occupied) separately [amos1961proc,king1967chem](../../bibliography.md). After
fitting the occupied orbitals, the virtual starting orbitals are chosen
in the orthogonal complement of the occupied orbitals. In some cases,
especially when restarting ROHF calculations, this may be an advantage.
Otherwise, it is not expected that `CMatrix` will be grossly superior to
`FMatrix` for most cases.

<a id="sec:essentialelements.initialguess.PModel"></a>
## PModel Guess

The PModel guess (chosen by `Guess PModel` in the `%scf` block or simply
a keyword line with `!PModel`) is one that is usually considerably
successful. It consists of building and diagonalizing a Kohn--Sham
matrix with an electron density which consists of the superposition of
spherical neutral atoms densities which are predetermined for both
relativistic and nonrelativistic methods. This guess is valid for both
Hartree--Fock and DFT methods, but not for semiempirical models.
However, due to the complexity of the guess it will also take a little
computer time (usually less than one SCF iteration). The model densities
are available for most atoms of the periodic table and consequently the
PModel guess is usually the method of choice (particularly for molecules
containing heavy elements) unless you have more accurate starting
orbitals available.

<a id="sec:essentialelements.initialguess.PAtom"></a>
## Hückel and PAtom Guesses

The extended Hückel guess proceeds by performing a minimal basis
extended Hückel calculation and projecting the MOs from this calculation
onto the actual basis set using one of the two methods described above.
The minimal basis is the STO-3G basis set. The Hückel guess may not be
very good because the STO-3G basis set is so poor. There is also
accumulating evidence that the superposition of atomic densities
produces a fairly good initial guess. The critique of the atomic density
method is that the actual shape of the molecule is not taken into
account and it is more difficult to reliably define singly occupied
orbitals for ROHF calculations or a reasonable spin density for UHF
calculations. Therefore ORCA chooses a different way in the `PAtom`
guess (which is the default guess): the Hückel calculation is simply
carried out *for all electrons* in a minimal basis of atomic SCF
orbitals. These were determined once and for all and are stored inside
the program. This means that the densities around the atoms are very
close to the atomic ones, all orbitals on one center are exactly
orthogonal, the initial electron distribution already reflects the
molecular shape and there are well defined singly occupied orbitals for
ROHF calculations.

<a id="sec:essentialelements.initialguess.restart"></a>
## Restarting SCF Calculations

To restart SCF calculations, it can be very helpful and time-saving to
read in the orbital information of a previous calculation. To do this,
specify:

```orca
! moread
%moinp "name.gbw"
```

This is done by default for single-point calculations
if the `.gbw` file of the same name exists --
see [initialguess.autostart](#sec:essentialelements.initialguess.autostart).

The program stores the current orbitals in every SCF cycle. Should a job
crash, it can be restarted from the orbitals that were present at this
time by just re-running the calculation to use the present `.gbw` file.
In addition, an effort has been made to make `.gbw` files from different
releases compatible with each other. If your input `.gbw` file is from
an older release, use `! rescue moread noiter` with `% moinp "name.gbw"`
to produce an up-to-date `.gbw`. When the `rescue` keyword is invoked,
only the orbital coefficients are read from the `.gbw` file, and
everything else from the input file. Thus, make sure that the geometry
and the basis set of the old `.gbw` file and the new input match.

Within the same ORCA version, neither the geometry nor the basis set
stored in `name.gbw` need to match the present geometry or basis set.
The program merely checks if the molecules found in the current
calculation and `name.gbw` are consistent with each other and then
performs one of the possible orbital projections. If the two basis sets
are identical the program by default only reorthogonalizes and
renormalizes the input orbitals. However, this can be overruled by
explicitly specifying `GuessMode` in the `% scf` block as `CMatrix` or
`FMatrix`.

**If redundant components were removed from the basis (see
[essentialelements.lindep](basisset.md#sec:essentialelements.lindep)), then `! moread noiter` must
not be used to read SCF orbitals from a previous calculation, as it is
going to lead to wrong results. In that case, `! moread` may be
used (without `noiter`) if doing the entire calculation in one go is not
possible.**

If `!moread` and `%moinp` are used, the input `.gbw` file from the earlier
calculation must have a different name than the new calculation, because
in the very beginning of a calculation, a new `.gbw` file is written. If
the names are the same, the `.gbw` file from the earlier calculation is
overwritten and all information is lost. Therefore, if you want to
restart a calculation with an input file of the same name as the
previous calculation, you have to rename the `.gbw` file first. This is
good practice anyway to avoid surprises, particularly for expensive calculations.
Alternatively, you can use the
[AutoStart feature](#sec:essentialelements.initialguess.autostart)
instead of explicitly specifying `!moread` and `%moinp`.

There is an additional aspect of restarting SCF calculations --- if you
have chosen `SCFMode = Conventional` the program stores a large number
of integrals that might have been time consuming to calculate on disk.
Normally the program deletes these integrals at the end of the
calculation. However, if you want to do a closely related calculation
that requires the same integrals (i.e. the *geometry*, the *basis set*
and the *threshold* `Thresh` are the same) it is faster to use the
integrals generated previously. This is done by using `KeepInts = true`
in the `% scf` block of the first calculation and then use
`ReadInts = true` in the `% scf` block of the second calculation. If the
second calculation has a different name than the first calculation you
have to use `IntName = "FirstName"` to tell the program the name of the
integral files. Note that the file containing the integrals does not
have an extension --- it is simply the name of the previous input file
with `.inp` stripped off.

```orca
%scf
  KeepInts true         # Keep integrals on disk
  ReadInts true         # Read integrals from disk
  IntName  "MyInts"     # Name of the integral files without extension
end
```

Note that, in general, restarting calculations with old integral files
requires the awareness and responsibility of the user. If properly used,
this feature can save considerable amounts of time.

<a id="sec:essentialelements.initialguess.autostart"></a>
## AutoStart feature

Older versions of ORCA always created a new GBW file at the beginning of
the run no matter whether a file of the same name existed or perhaps
contained orbitals. Now, in the case of single-point calculations the
program automatically checks if a `.gbw` file of the same name exists.
If yes, the program checks if it contains orbitals and all other
necessary information for a restart. If yes, the variable `Guess` is set
to `MORead`. The existing `.gbw` file is renamed to `BaseName.ges` and
`MOInp` is set to this filename. If the `AutoStart` feature is not
desired, set `AutoStart false` in the `%scf` block or give the keyword
`!NoAutoStart` in the simple input line. Note that `AutoStart` is
ignored for geometry optimizations: in this case, using previously
converged orbitals contained in a `.gbw` file (of a different name) can
be achieved via `MORead` and `MOInp`.

<a id="sec:essentialelements.initialguess.changes"></a>
## Changing the Order of Initial Guess MOs and Breaking the Initial Guess Symmetry

Occasionally you will want to change the order of initial guess MOs ---
be it because the initial guess yielded an erroneous occupation pattern
or because you want to converge to a different electronic state using
the orbitals of a previous calculation. Reordering of MOs and other
tasks (like breaking the symmetry of the electronic wavefunction) are
conveniently handled with the `Rotate` feature in ORCA. `Rotate` is a
subblock of the SCF block that allows you to linearly transform pairs of
MOs.

```orca
%scf
  Rotate
   { MO1, MO2, Angle }
   { MO1, MO2, Angle, Operator1, Operator2 }
   { MO1, MO2} # Shortcut to swap MO1 and MO2. Angle=90 degrees.
  end
end
```

Here, `MO1` and `MO2` are the indices of the two MOs of interest. Recall
that ORCA starts counting MOs with index 0, i.e. the MO with index 1 is
the *second* MO. `Angle` is the rotation angle in degrees. A rotation
angle of 90$^{\circ}$ corresponds to flipping two MOs, an angle of
45$^{\circ}$ leads to a 50:50 mixture of two MOs, and a 180$^{\circ}$
rotation leads to a change of phase. `Operator1` and `Operator2` are the
orbitals sets for the rotation. For UHF calculations spin-up orbitals
belong to operator 0 and spin-down orbitals to operator 1. RHF and ROHF
calculations only have a single orbital set.

Among others, the `Rotate` feature can be used to produce
broken-symmetry solutions, for example in transition metal dimers. In
order to do that, first perform a high-spin calculation, then find the
pairs of MOs that are symmetric and antisymmetric combinations of each
other. Take these MOs as the initial guess and use rotations of
45$^{\circ}$ for each pair to localize the starting MOs. If you are
lucky and the broken symmetry solution exists, you have a good chance of
finding it this way. See section [spectroscopyproperties.magnx](../spectroscopyproperties/magnx.md#sec:spectroscopyproperties.magnx)
for more details on the broken-symmetry approach.

<a id="sec:essentialelements.initialguess.guessmix"></a>
## Automatically Breaking of the Initial Guess Symmetry

Another simple way to break the initial guess symmetry for more trivial cases, is to simply use the keyword `!GUESSMIX`. This will automatically mix 50% of the alpha LUMO into the alpha HOMO. That is equivalent to a 45 degree rotation as done above and only for these orbitals. It might be useful when one wants an open-shell singlet and needs the alpha and beta orbitals to start differently.

The specific angle of rotation can be controlled with:

```orca
%scf
  guessmix 75 # angle in degrees, default is 45
end
```

<a id="sec:essentialelements.initialguess.scfguessenergy"></a>
## Calculating only the energy of an input density

In case you want to give the result of a previous SCF and recalculate the energy,
or maybe some other property (like the MP2 energy) using that density without changing the orbitals,
 you can use the flags `!CALCGUESSENERGY NOITER`.

The SCF program will read the orbitals, compute the density and
one Fock matrix necessary to get the energy and move on with no orbital updates. This
can be used to combine DFT orbitals with DLPNO-CCSD(T) for example. Be careful
with the results you get from this because these orbitals are not variational anymore!

<a id="sec:essentialelements.initialguess.keywords"></a>
## Keywords

<a id="tab:essentialelements.initialguess.keywords.simple"></a>
!!! note "Simple input keywords related to the initial guess."
    | Keyword | Description |
    | --- | --- |
    | `PAtom` | Selects the polarized atoms guess |
    | `PModel` | Selects the model potential guess |
    | `Hueckel` | Selects the extended Hückel guess |
    | `HCore` | Selects the one-electron matrix guess |
    | `MORead` | Read MOs from a previous calculation (use together with `%moinp "myorbitals.gbw"`) |
    | `AutoStart` | Try to start from an existing GBW file of the same name as the present one (default; only for single-point calculations) |
    | `NoAutoStart` | Don't try to do that |
    | `NoIter` | Sets the number of SCF iterations to 0. This works together with MOREAD and means that the program will work with the provided starting orbitals. |
    | `KeepInts` | Do not delete the integrals from disk after a calculation in conventional mode |
    | `ReadInts` | Read the existing integrals from a previous calculation in conventional mode (use together with `%scf IntName "PreviousBaseName" end`) |
    | `CalcGuessEnergy` | Calculate the energy of the initial guess orbitals (use together with `NoIter`) |
