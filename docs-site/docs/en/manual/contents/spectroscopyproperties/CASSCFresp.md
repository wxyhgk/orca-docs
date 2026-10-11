

<a id="sec:spectroscopyproperties.casscfresp"></a>
# CASSCF Linear Response

## Introduction
Similar to the SCF linear response (see [essentialelements.cpscf](#sec:essentialelements.cpscf)), second-derivative properties can be calculated at the CASSCF level by solving the coupled perturbed (CP-)CASSCF equations for the linear response of the wavefunction parameters to a perturbation.
These linear response equations are expressed as 

$$
\frac{\partial^2 E}{\partial\lambda^2} \frac{\partial\lambda}{\partial\mathbf R} = -\frac{\partial^2 E}{\partial\lambda \partial\mathbf R}
$$

where $\lambda$ are the CASSCF wavefunction parameters and $\mathbf R$ are the perturbations for which the response equations are being solved [Helgaker1986, vahtras1997](../../bibliography.md).
The property gradient on the right-hand side (RHS) is a known perturbation-dependent quantity, but the left-hand side (LHS) depends on the solution of the response of the wavefunction parameters to $\mathbf R$.
Therefore, the response to the perturbation must be solved for iteratively, which is done using the trial vectors $\mathbf X$.
This leads to the LHS being computed as a sigma-vector, which is reassembled at every iteration.
The linear response equation for perturbation $R_i$ can then be written as

$$
\sigma = \mathbf H \mathbf X^{(R_i)} = -\mathbf G^{(R_i)}
$$

where $\mathbf H$ is the perturbation-independent Hessian matrix and $\mathbf G$ is the perturbation-specific RHS matrix. 
Once the linear equation converges, the solution vector of the response parameters can then be contracted with the electron- and spin-density matrices to yield the AO response density matrices, $\left[\mathbf P^{\alpha \pm \beta}\right]^{(\mathbf R)}$.
The response densities can then be contracted with appropriate AO 1-electron property integrals to compute the second-order contributions to second-derivative properties.

In ORCA these equations are solved by the `orca_casscfresp` program and the underlying solver is `BHP22`, a Davidson-type linear equation solver.
The RHS is built from the property integrals calculated in the `orca_propint` program. 
After the solution converges and the response densities are made and stored, the `orca_prop` program is called, wherein the appropriate densities and response densities are contracted with the necessary property integrals (also from `orca_propint`).
This use of densities keeps the response property calculations in `orca_prop` generally applicable to all methods as the densities house the method-specific information.

## Technical Notes
It should be noted that CASSCF linear response uses the optimized CASSCF wavefunction as a starting point.
Thus, a `%casscf` block with the appropriate inputs (see [CASSCF](#sec:modelchemistries.casscf)) must be provided in the input.
State-specific (SS-)CASSCF response is run on SS (`NRoots 1`) CASSCF wavefunctions.
If the CASSCF wavefunction is state-averaged (SA), the response is run over the averaged manifold of states and not on a specific root.
In this case, one should analyze the output carefully.
It is wise to only average states which are (nearly-)degenerate.

By default, a CASSCF calculation will be run from scratch before running the CASSCF Response.
Alternatively, orbitals from a previously converged CASSCF calculation may be used with `!MOREAD NoIter` and supplying the appropriate `.gbw` file via `%moinp`.
In this case, be sure that the input in the `%casscf` block matches that from the same input block of the previously converged calculation and be sure to check the orbitals well!

The linear response equations are solved iteratively until the convergence threshold for the residual norm (`TolR`) is reached.
This value can be set by the user, but ORCA will set it by default to the tightest reasonable convergence criteria, taking into account the orbital- and CI-gradient tolerances of the underlying CASSCF calculation.
This should be the most reasonable setting; be careful if trying to tighten this threshold!

The appropriate property flags in the `%elprop` and `%eprnmr` blocks must be set to calculate the properties that are wanted (see [spectroscopyproperties.elprop](#sec:spectroscopyproperties.elprop) and [properties.eprnmr](#sec:spectroscopyproperties.properties.eprnmr)).
While all first-derivative properties work with CASSCF, not all second-derivative properties are currently available with CASSCF.
The static properties currently available (sorted by perturbation taken for the response) include:
* Electric ($\mathbf E$) Field
    * Dipole/dipole Polarizability
    * Dipole/quadrupole Polarizability
* Quadrupole ($\mathbf Q$) Field
    * Quadrupole/Quadrupole Polarizability
* Velocity ($\mathbf v$)
    * Velocity Polarizability
* Magnetic ($\mathbf B$) Field (**without** GIAOs)
    * EPR g-Tensor
    * NMR Chemical Shieldings
* Nuclear Magnetic Moment ($I^{(A)}$)
    * EPR A-matrix (Aorb contribution) 

The magnetic properties are currently implemented without gauge-including atomic orbitals (GIAOs).
Thus, an appropriate gauge-origin must be provided in the `%eprnmr` block!
For the EPR g-tensor, using a large basis set with a chemically relevant gauge origin is recommended.
However, one should in general be wary of NMR chemical shieldings without GIAOs.

## Basic Usage
The following is an overview of the blocks required for a property calculation with

```orca
! def2-TZVP AutoAux    # (or other appropriate basis & auxiliary)

%casscf
  ...
end

%casresp     # only required to change solver, printing, or preconditioner options
  ...
end

%elprop      # only required if electric property requested
  ...
end

%eprnmr      # only required if magnetic property requested
  ...
  ORI ...
end

* xyzfile ...
```

## Troubleshooting
If the `%casresp` block is specified and the calculation does not run through the CASSCF Response section, then the properties requested are not second-derivatives and therefore do not require linear response equations to be solved. 
If, however, the job aborts, watch for these possibilities:
* At least one of the second-derivative properties requested is not available at the CASSCF level (see list above of those currently implemented)
* `MaxIter` may need to be increased or `TolR` loosened
* If one or more perturbations meet convergence criteria and then later do not, try turning off solution locking.
    * This may point to `TolR` being too tight 
* A magnetic field property is requested without setting the gauge-origin in the `%eprnmr` block
* An appropriate auxiliary basis (or the `!AutoAux` keyword) may be required, especially for:
    * The trial vector preconditioner (which is on by default)
    * `TrafoStep RI` in the `%casscf` block
    * RIJCOSX, RIJONX
* RIJK was specified (this is **NOT** supported)

Note that the solver-related options in the `%elprop` and `%eprnmr` blocks do not affect the solution of the CP-CASSCF equations.

## Notes on Printing
The information on the types of property integrals computed can be found in the `ORCA PROPERTY INTEGRAL CALCULATIONS` section of the output file.
The `orca_casscfresp` output begins with the header `ORCA CASSCF RESPONSE CALCULATION`.
After information about the types and number of perturbations, the calculation splits into the major types of perturbations: real and imaginary.
All response equations of the same type can be solved simultaneously.

Each of these types has its own section in the output file.
These sections begin with information on the orbital ranges and the CI space, then go into the iterative solution of the equations.
The printout here gives an overview of the iteration number, the residual norm of each response equation, and if that response equation has met the convergence criteria.
The following is an example of this output (with iterations 3--7 removed for simplicity):

```orca
 ------------------------------------------------------------------------------

                      SOLVER Davidson-type linear equation solver 

   Iter.                  ||Error||_2   Conv.                (TolR = 1.000e-08)
 ------------------------------------------------------------------------------
    0  (rhs    0)        1.645417e-01     No
       (rhs    1)        1.826041e-01     No
       (rhs    2)        2.047543e-01     No
    1  (rhs    0)        7.069575e-02     No
       (rhs    1)        3.363295e-02     No
       (rhs    2)        7.229274e-02     No
    2  (rhs    0)        9.183136e-03     No
       (rhs    1)        3.922435e-03     No
       (rhs    2)        7.152764e-03     No
(...)
 ------------------------------------------------------------------------------

     All 3 Linear Equations CONVERGED Below 1.000e-08

 ------------------------------------------------------------------------------
    8  (rhs    0)        4.070240e-09    Yes
       (rhs    1)        1.186846e-09    Yes
       (rhs    2)        4.407666e-09    Yes
```

Before going on to the necessary property modules, the significant contributions to the RHS and/or response vectors will be outputted if they were requested (via `PrintRHSVec` and `PrintRspVec`).
Here, outputs such as the following can be seen.

```orca
  ---------------------------------
   CASSCF Response Vector Analysis
  ---------------------------------
 square of coefficients of particle-hole and CAS-CI excitations are printed
 if larger than 1.0e-02

IPERT: 0

   (-) I   9 (   9) -> V   0 (  17) :      0.07167 (c= -0.26772137)
(...)
   (-) A   1 (  14) -> V  13 (  30) :      0.07323 (c=  0.27061481)
(...)
   (-) I   4 (   4) -> A   0 (  13) :      0.02915 (c=  0.17074032)
(...)
   (-) CI                                  1.65592 [     7]: 1201
(...)
```

The majority of the output has been removed for the sake of simplicity.
Here, the significant contributions to the response vector are printed if the square of the vector element is larger than `1.0e-02` (the default value for `TolPrintVec`).
Each line begins with either a `(+)` or `(-)`, which denote the Hermiticity of the excitation operator.
With static CASSCF linear response, `(+)` always denotes an imaginary perturbation and `(-)` a real perturbation.
For the first vector (i.e. `IPERT: 0`), four contributions have been listed here.

The first three are from particle-hole excitations going from the left size of the arrow to the right.
On each side of the arrow has three things: a letter designating if it is an inactive (`I`), active (`A`), or virtual (`V`) orbital; a number designating the index within that orbital subblock, and a number in parentheses designating the overall orbital number. 
Further to the right, the coefficient (i.e. the vector element) is given in parentheses and the square of that value is given to the left of it.
This is how the relative contributions of each excitation can be analyzed.

The final contribution shown is from a CI excitation.
Its weight is listed, followed by the index in brackets and the corresponding configuration of the active electrons among the active orbitals.

<a id="sec:spectroscopyproperties.casscfresp.keywords"></a>
## Keywords
!!! note "`%casresp` block input keywords."
    | Keyword                        | Options               | Description                                                         |
    |:-------------------------------|:----------------------|:--------------------------------------------------------------------|
    | `TolR`                         | `<real>`              | Convergence threshold (residual norm of LR equations)               |
    |                                |                       | *(default) uses tightest reasonable threshold*                      |
    | `MaxIter`                      | `64`                  | Maximum number of iterations                                        |
    | `MaxRed`                       | `100`                 | Maximum size of the reduced space per RHS                           |
    | `PrintRHSVec`                  | `false`               | Print significant contributions to the RHS vector                   |
    | `PrintRspVec`                  | `false`               | Print significant contributions to the response vector              |
    | `PrintWF`                      | `CFG`                 | *(default)* Print CI part of RHS/rsp vector in configuration basis  |
    |                                | `CSF`                 | Print CI part of RHS/rsp vector in CSF basis                        |
    |                                | `DET`                 | Print CI part of RHS/rsp vector in determinant basis                |
    | `TolPrintVec`                  | `1.e-2`               | Threshold to print a contribution to the RHS/response vector        |
    | `PreCondType`                  | `full`                | *(default)* Full preconditioner of trial vector (requires aux basis)|
    |                                | `diag`                | Diagonal preconditioner of trial vector (requires aux basis)        |
    |                                | `none`                | No preconditioning of trial vector                                  | 
    | `PreCondMaxRed`                | `400`                 | Hessian precondition subset size                                    |
    | `DoOrbResp`                    | `true`                | Include orbital response                                            |
    | `DoLocking`                    | `true`                | Lock solutions to perturbations as they meet convergence criteria   |
    | `DoOlsen`                      | `false`               | Use Olsen preconditioner                                            |

