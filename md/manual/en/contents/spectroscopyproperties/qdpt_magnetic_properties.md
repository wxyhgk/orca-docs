```{index} QDPT, Magnetic Properties via QDPT
```

(sec:spectroscopyproperties.qdpt_magnetic_properties)=
# Magnetic Properties Through Quasi Degenerate Perturbation Theory 

(sec:spectroscopyproperties.qdpt_magnetic_properties.general)=
## Quasi Degenerate Perturbation Theory (QDPT) in a nutshell

Quasi Degenerate Perturbation Theory offers a versatile and accurate approach to 
to a number of magnetic properties for basically every wavefunction-based excited 
state method. 

In a nutshell, at the non-relativistic limit for every excited state 
single- or multi-reference wavefunction-based method, bearing a CASSCF, MRCI, or a ROCIS 
type of zeroth order wavefunction, one can set up an excitation problem that is 
a combination of the zeroth order wavefunction and excited spin-adapted 
configuration state functions (CSFs) $\left| \Phi_{\mu}^{SS} \right \rangle$. 

That takes the form:

$$\left| \Psi_{I}^{SS} \right\rangle= \sum\nolimits_{\mu} { C_{\mu l} \left| \Phi_{\mu}^{SS} \right \rangle }
$$ (eqn:H_BO)

Here, the upper indices $SS$ stand for a wavefunction of the spin
quantum number $S$ and spin projection $M_{S} = S$. Since the BO
Hamiltonian does not contain any complex-valued operator, the solutions
$\left| \Psi_{I}^{SS}\right\rangle$ may be chosen to be real-valued.

Obtaining a solution to the above eigenvalue problem provides the coefficients
with which the CSFs enter into the chosen wavefunction, as well as the eigenstates 
of the spin-free operator. These eigenstates may be used to expand towards 
the respective relativistic eigenstates by setting up the relevant 
quasi-degenerate eigenvalue problem. In fact, the spin-orbit coupling (SOC) and 
spin-spin coupling (SSC) effects along with the Zeeman interaction can be
included by means of the quasi-degenerate perturbation theory (QDPT). In
this approach, the SOC, SSC, and Zeeman operators are calculated
in the basis of pre-selected solutions of the BO
Hamiltonian $\left\{{ \Psi_{I}^{SM} }\right\}$.


$$\left\langle { \Psi_{I}^{SM} \left|{ \hat{{H} }_{\text{BO} } +\hat{{H} }_{\text{SOC} }
+\hat{{H} }_{\text{SSC} } +\hat{{H} }_{\text{Z} } } \right|\Psi_{J}^{{S}'{M}'} }
\right\rangle=\delta_{IJ} \delta_{S{S}'} \delta_{M{M}'} E_{I}^{\left( S
\right)} +\left\langle { \Psi_{I}^{SM} \left|{ \hat{{H} }_{\text{SOC} }
+\hat{{H} }_{\text{SSC} } +\hat{{H} }_{\text{Z} } } \right|\Psi_{J}^{{S}'{M}'} }
\right\rangle$$ (eqn:H_QDPT)

Diagonalization of this matrix yields the energy levels and eigenvectors
of the coupled states. These eigenvectors in fact represent linear
combinations of the solutions of $\hat{{H} }_{\text{BO} }$ with complex
coefficients.

The effective one-electron SOC operator in second quantized form can be
written as {cite}`neese2005jchemphys`:

$$\hat{{H} }_{\text{SOMF} } =\frac{1}{2}\sum\limits_{pq} { z_{pq}^{-}
\hat{{a} }_{p}^{\uparrow } \hat{{b} }_{q} +z_{pq}^{+} \hat{{b} }_{p}^{\uparrow }
\hat{{a} }_{q} +z_{pq}^{0} \left[{ \hat{{a} }_{p}^{\uparrow } \hat{{a} }_{q}
-\hat{{b} }_{p}^{\uparrow } \hat{{b} }_{q} } \right]}
$$ (eqn:H_SOMF)

Here, $\hat{{a} }_{p}^{\uparrow }$ and $\hat{{b} }_{p}^{\uparrow }$ stand
for creation of $\alpha$ and $\beta$ electrons, respectively;
$\hat{{a} }_{p}$ and $\hat{{b} }_{p}$ represent the corresponding
annihilation operators. The matrix elements
$z_{pq}^{-} = z_{pq}^{x} - iz_{pq}^{y}$, $z_{pq}^{+}
= z_{pq}^{x} + iz_{pq}^{y}$, and $z_{pq}^{0} = z_{pq}^{z}$ (upper $x$,
$y$, $z$ indices denote the Cartesian components) are constructed from
the matrix elements described in section {ref}`sec:spectroscopyproperties.epr.D`.

In this concept, the SOC Hamiltonian reads:

$$\left\langle {{\Psi}_I^{SM}\left|{ \hat{{H} }_{\text{SOC} } } \right|{\Psi}_J^{S^\prime M^\prime}} \right\rangle=
\sum_{m=0,\pm1}\left(-1\right) \left( \begin{matrix}S^\prime&1\\M^\prime&m\\\end{matrix} \left|{\begin{matrix}
S\\
M\\
\end{matrix} } \right. \right)
\underset{Y_{II^\prime}^{SS^\prime}(m)}{\underbrace{\left\langle {{\Psi}_I^{SS}||H_{-m}^{SOC}||{\Psi}_J^{SS}} \right\rangle}}
$$(eqn:H_SOC)


where $m$ represents the standard vector operator components.
$\left( \begin{matrix}S^\prime&1\\M^\prime&m\\\end{matrix} \left|{\begin{matrix}
S\\
M\\
\end{matrix} } \right. \right)$ is a Clebsch–Gordon coefficient that has a single numerical 
value that is tabulated. It satisfies certain selection rules and
contains all of the M-dependence of the SOC matrix elements. The
quantity $Y_{II^\prime}^{SS^\prime}(m)$ is a reduced matrix element. It only depends on the
standard components of the two states involved. There are only three cases of non-zero 
$Y_{II^\prime}^{SS^\prime}(m)$, which arise from state pairs that either have the same 
total spin or differ by one unit.{cite}`neese1998inorgchem`

The SSC Hamiltonian reads:

$$\hat{{H} }_{\text{SSC} } =-\frac{3g_{e}^{2} \alpha^{2} }{8}\sum\limits_{i\ne j}
{\sum\limits_{m=0,\pm 1,\pm 2} { \frac{\left({ -1} \right)^{m} }{r_{ij}^{5}
} } \left[{ \mathrm{\mathbf{r} }_{ij} \times \mathrm{\mathbf{r} }_{ij} }
\right]_{-m}^{\left( 2 \right)} \left[{ \mathrm{\mathbf{S} }\left( i \right)\times
\mathrm{\mathbf{S} }\left( j \right)} \right]}_{m}^{\left( 2 \right)}
$$ (eqn:H_SSC)

For matrix elements between states of the same multiplicity, it can be
simplified to

$$\begin{array}{l}
 \left\langle { aSM\left|{ \hat{{H} }_{\text{SSC} } } \right|a'SM'} \right\rangle=\frac{\sqrt{ \left({ S+1} \right)\left({ 2S+3} \right)} }{\sqrt{ S\left({2S-1} \right)} } \\
\hspace{2cm}
\times \sum\limits_m { \left({ -1}
\right)^{m} } \left(\begin{matrix}{ S'}  & 2  \\
 { M'}  & m
\end{matrix} \left|{\begin{matrix}
 S  \\
 M  \\
\end{matrix} } \right. \right) \sum\nolimits_{pqrs} { D_{pqrs}^{\left({ -m}
\right)} \left\langle { aSS\left|{ Q_{pqrs}^{0} } \right|a'SS} \right\rangle}
 \end{array}
$$ (eqn:SSC_RMEs)

Here,

$$Q_{pqrs}^{\left( 0 \right)} =\frac{1}{4\sqrt 6 }\left\{{ E_{pq} \delta
_{sr} -S_{ps}^{z} S_{rq}^{z} +\frac{1}{2}\left({ S_{pq}^{z} S_{rs}^{z}
-E_{pq} E_{rs} } \right)} \right\}$$ (eqn:Qpqrs)

represents the two-electron quintet density. The operators 
$E_{pq}=\hat{{a} }_{p}^{\uparrow } \hat{{a} }_{q} +\hat{{b} }_{p}^{\uparrow } \hat{{b} }_{q}$
and
$S_{pq}^{z} =\hat{{a} }_{p}^{\uparrow } \hat{{a} }_{q} -\hat{{b} }_{p}^{\uparrow }
\hat{{b} }_{q}$ symbolize the one-electron density operator and the
spin density operator, respectively. The spatial part

$$D_{pqrs}^{\left( 0 \right)} =\frac{1}{\sqrt 6 }\iint{ \varphi_{p}
\left({ \mathrm{\mathbf{r} }_{1} } \right)\varphi_{r} \left({ \mathrm{\mathbf{r} }_{2}
} \right)}\frac{3r_{1z} r_{2z} -\mathrm{\mathbf{r} }_{1} \mathrm{\mathbf{r} }_{2}
}{r_{12}^{5} }\varphi_{q} \left({ \mathrm{\mathbf{r} }_{1} } \right)\varphi
_{s} \left({ \mathrm{\mathbf{r} }_{2} } \right)d\mathrm{\mathbf{r} }_{1} d\mathrm{\mathbf{r} }_{2}
$$ (eqn:Dpqrs)

denotes the two-electron field gradient integrals. These two-electron
integrals can be evaluated using the RI approximation.

Finally, the Zeeman Hamiltonian is included in the form of:

$$\hat{{H} }_{\text{Z} } =\mu_{B} \left({ \mathrm{\mathbf{\hat{{L} }} }+g_{e} \mathrm{\mathbf{\hat{{S} }} }} \right)\mathrm{\mathbf{B} }
$$ (eqn:H_Zeeman)

with $\mathrm{\mathbf{\hat{L} }}$ representing the total orbital
momentum operator, and $\mathrm{\mathbf{\hat{S} }}$ being the total spin
operator.

In this concept, the solution of a selected relativistic Hamiltonian provides access to 
numerous magnetic properties, namely EPR properties ({ref}`sec:spectroscopyproperties.properties.eprnmr`) and
magnetization and susceptibility properties ({ref}`sec:modelchemistries.mrci.soc.magnet`).
Additionally, monitoring the impact of an external magnetic field to the relativistic eigenstates
and eigenvectors ({ref}`sec:modelchemistries.mrci.soc.magField`) becomes straightforward.

Collectively within the QDPT framework, the following magnetic properties become available:  

- Common QDPT magnetic properties  

  (1) g-Tensor/Matrix 
\
  (2) D-Tensor/Matrix (Zero Field Splitting, ZFS)
\
  (3) A-Tensor/Matrix (Hyperfine, HFC)
\
  (4) Electric Field Gradient 
\
  (5) Magnetization 
\
  (6) Susceptibility 
\
  (7) Inclusion of Magnetic Fields

- Special treatments also include

  (8) g-Tensor/Matrix and A-Tensor/Matrix using the 2nd-order sum-over-states approximation
\
  (9) {ref}`sec:spectroscopyproperties.magrelax` functionality


(sec:spectroscopyproperties.qdpt_magnetic_properties.effective_hamiltonian)=
## Magnetic Properties Through the Effective Hamiltonian 

Since both the energies and the wavefunction of the low-lying
spin-orbit states are available, the effective Hamiltonian theory can be
used to extract EPR parameters such as the full g-,  Zero Field Splitting (ZFS) 
and hyperfine A-tensors.

Provided that the ground state is non-degenerate. By applying this
Hamiltonian on the basis of the model space, i.e. the $|S, M_S\rangle$
components of the ground state, the interaction matrix is constructed.

The construction of effective Hamiltonian relies on the information
contained in both the energies and the wavefunctions of the low-lying
spin-orbit states. Following des Cloizeaux formalism, the effective
Hamiltonian reproduces the energy levels of the "exact" Hamiltonian
$E_k$ and the wavefunctions of the low-lying states projected onto the
model space $\tilde{\Psi}$:

$$\hat{H}_{\text{eff} }|\tilde{\Psi}_{k}\rangle = E_{k}|\tilde{\Psi}_{k}\rangle$$

These projected vectors are then symmetrically orthonormalized resulting
in an Hermitian effective Hamiltonian, which can be written as:

$$\hat{H}_{\text{eff} }|\tilde{\Psi}\rangle = \sum_{k}|S^{-\frac{1}{2} }\tilde{\Psi}_{k}\rangle
E_{k} \langle S^{-\frac{1}{2} }\tilde{\Psi}_{k}|$$

The effective interaction matrix obtained by expanding this Hamiltonian
into the basis of determinants belonging to the model space, is then
compared to the matrix resulted from expanding the model Hamiltonian.
Based on a singular value decomposition procedure, all 9 elements of the
g-, A- and/or ZFS-tensors may be extracted.


(sec:spectroscopyproperties.qdpt_magnetic_properties.keywords)=
## QDPT Keywords

Starting from ORCA 6.0, the calculation of the magnetic properties through the 
Quasi Degenerate Perturbation Theory (QDPT) in all available correlation-type modules is unified 
and simplified. Following the general architecture design of ORCA 6.0, the computation 
of all the involved magnetic properties are centrally performed by a driver data structure called the QDPT Driver.
The Driver takes into account all of the specific variables that are populated by the involved module
and proceeds accordingly to calculate and represent the requested property in a uniform fashion. 
This presently involves the `casscf`, `mrci`, `rocis`, and `lft` modules

In this way,
1) the analysis of results from the user's perspective is simplified 
2) cross-module correlation and comparisons are easily accessible

The general keywords that activate the generation of QDPT properties are: 

```orca
%METHOD (casscf, mrci, rasci, rocis, lft, ...)
  REL            # the name of the relativistic block
    DoSOC true   # include the SOC contribution
    DoSSC true   # include the SSC contribution
  END
END
```

Starting from ORCA 6.1, the relativistic bock has a common structure across the methods that are connected to the 
QDPT driver. Hence, `rel` is the default block name for all connected methods. In the case of the `%mrci` block, `soc` is an 
alternative name to maintain for this release consistency with the old input relativistic blocks. The `soc` block name 
will be deprecated in the next release, so one is recommended to use the `rel` block name for requesting QDPT properties. 

The QDPT keywords are:
```orca
%METHOD (CASSCF, RASCI, MRCI, ROCIS, LFT)
  REL
   #-------------------------------------------------------
   # SOC/SSC
   #-------------------------------------------------------
   DoSOC true
   DoSSC true
   PrintLevel 4

   #=======================================================
   # MAGNETIC PROPERIES
   #=======================================================

   #-------------------------------------------------------
   #Do Magnetization Magntization/Susceptibily Properties
   #-------------------------------------------------------
   DoMagnetization true
   DoSusceptibility true
   #-------------------------------------------------------
   LebedevPrec 5           # Precision of the grid for different field
   nPointsFStep 5          # number of steps for numerical differentiation
   MAGFieldStep 100.0      # Size of field step for numerical differentiation
   MAGTemperatureMIN 4.0   # minimum temperature (K) for magnetization
   MAGTemperatureMAX 4.0   # maximum temperature (K) for magnetization
   MAGTemperatureNPoints 1 # number of temperature points for magnetization
   MAGFieldMIN 0.0         # minimum field (Gauss) for magnetization
   MAGFieldMAX 70000.0     # maximum field (Gauss) for magnetization
   MAGNpoints 15           # number of field points for magnetization
   SUSTempMIN 1.0          # minimum temperature (K) for susceptibility
   SUSTempMAX 300.0        # maximum temperature (K) for susceptibility
   SUSNPoints 300          # number of temperature points for susceptibility
   SUSStatFieldMIN 0.0     # minimum static field (Gauss) for susceptibility
   SUSStatFieldMAX 0.0     # maximum static field (Gauss) for susceptibility
   SUSStatFieldNPoints 1   # number of static fields for susceptibility

   #-------------------------------------------------------
   # Magnetic Field Magnetic Filed Perturbation (Zeeman Effect)
   #-------------------------------------------------------
   DoMagneticField true
   Temperature 10, 50, 300
   B 10000, 20000, 30000

   #-------------------------------------------------------
   # EPR g-Tensor/Matrix
   #-------------------------------------------------------
   DoGTensor true
   NDoubGtensor 2

   #-------------------------------------------------------
   # EPR D-Tensor/Matrix (Zero Field Splitting, ZFS)
   #-------------------------------------------------------
   DoDTensor true

   #-------------------------------------------------------
   # EPR A-Tensor/Matrix (Hyperfine, HFC)
   # => Presently only in CASSCF and LFT
   #-------------------------------------------------------
   DoAMatrix true
   AMatrixNuc 0,1

   #-------------------------------------------------------
   # 2nd-order SUM OVER STATES (g-, A-Tensors/Matrices)
   # => Presently only in CASSCF and MRCI
   #-------------------------------------------------------
   DoSOS True

   #-------------------------------------------------------
   # ZFS from an excited state multiplet
   #-------------------------------------------------------
   IStates 4,5,6

   #-------------------------------------------------------
   # Magnetic Relaxation 
   # => Presently only in CASSCF and MRCI
   #-------------------------------------------------------
   DoMagrelax True
   projectHSOC True       # Project QDPT ground multiplet (always true)
   projectedstates Number # Multiplicity of the ground multipler  

   #=======================================================
   # OPTICAL/X-RAY SPECTROSCOPIES
   #=======================================================

   #-------------------------------------------------------
   # (X)MCD (X-ray) Magnetic Circular Dichroism Spectroscopy
   #-------------------------------------------------------
   DoMCD True

   #-------------------------------------------------------
   # XESSOC X-ray Emission Spectroscopy
   #-------------------------------------------------------
   DoXESSOC True

   #-------------------------------------------------------
   # RIXSSOC X-ray Resonance Inelastic Scattering Spectroscopy
   #-------------------------------------------------------
   DoRIXSSOC True
   DoElastic True
  END
END 
```

(sec:spectroscopyproperties.qdpt_magnetic_properties.properties_organization)=
## Organization of QDPT Magnetic Properties Computation 

In a first step, SOC contributions will be computed for any level of theory that is available

```orca
----------------------------------
QDPT WITH CASSCF/NEVPT2/MRCI/LFT... DIAGONAL ENERGIES
----------------------------------


*************************************
COMPUTING QDPT HAMILTONIAN
*************************************
```

Initially, the SOC part to the splitting is calculated. Firstly, the diagonal
(with respect to the spin) matrix element type of

$\left\langle { \Psi_{I} }
\right|\sum\limits_{pq} { \mathrm{\mathbf{z} }_{pq}^{x} S_{pq}^{z} } \left| \Psi_{J}
\right\rangle$, $\left\langle { \Psi_{I} }
\right|\sum\limits_{pq} { \mathrm{\mathbf{z} }_{pq}^{y} S_{pq}^{z} } \left| \Psi_{J}
\right\rangle$, $\left\langle { \Psi_{I} }
\right|\sum\limits_{pq} { \mathrm{\mathbf{z} }_{pq}^{z} S_{pq}^{z} } \left| \Psi_{J}
\right\rangle$

are evaluated between states of the same multiplicity and

$\left\langle { \Psi_{I} }
\right|\sum\limits_{pq} { \mathrm{\mathbf{z} }_{pq}^{x} S_{pq}^{+} } \left| \Psi_{J}
\right\rangle$, $\left\langle { \Psi_{I} }
\right|\sum\limits_{pq} { \mathrm{\mathbf{z} }_{pq}^{y} S_{pq}^{+} } \left| \Psi_{J}
\right\rangle$, $\left\langle { \Psi_{I} }
\right|\sum\limits_{pq} { \mathrm{\mathbf{z} }_{pq}^{z} S_{pq}^{+} } \left| \Psi_{J}
\right\rangle$ 

between states of different multiplicities.


Requesting `PrintLevel > 3` prints this table:

```orca
----------------------------------------------------------------------------
                        CALCULATED REDUCED SOC MATRIX ELEMENTS              
----------------------------------------------------------------------------
        Block               Root         <I|Lx S |J> <I|Ly S |J> <I|Lz S |J>
 I(Mult)     J(Mult)      I        J        cm-1        cm-1        cm-1    
----------------------------------------------------------------------------
 0( 3)       0( 3)        0        0         0.00       -0.00       -0.00  
 0( 3)       0( 3)        1        0        -0.00       -0.00        0.00  
 0( 3)       0( 3)        1        1         0.00       -0.00       -0.00  
 0( 3)       0( 3)        2        0         0.00       -0.00       -0.00  
 0( 3)       0( 3)        2        1      -199.78      174.81     -142.34  
...

 0( 3)       1( 1)        0        1        -0.67        0.59       -0.48  
 0( 3)       1( 1)        0        2      -157.31      137.65     -112.09  
 0( 3)       1( 1)        0        3        -0.00       -0.00       -0.00  
 0( 3)       1( 1)        0        4       -79.51      -33.73       70.17  
 0( 3)       1( 1)        0        5        24.77       84.05       68.46
... 
  
```

```orca
*************************************
Doing QDPT with ONLY SOC!
*************************************
```

Next, the non-zero SOC Matrix Elements will be printed 

```orca
------------------------------------
NONZERO SOC MATRIX ELEMENTS (cm**-1)
------------------------------------

           Bra                       Ket       
<Block Root S   Ms  | HSOC | Block Root S   Ms>    =  Real-part     Imaginary part
----------------------------------------------------------------------------------
   0    2  1.0  1.0           0     1  1.0  1.0          0.000            -71.172
   0    3  1.0  1.0           0     2  1.0  1.0          0.000              1.542
   0    4  1.0  1.0           0     0  1.0  1.0          0.000             50.048
   0    5  1.0  1.0           0     0  1.0  1.0          0.000            -48.827
   0    5  1.0  1.0           0     4  1.0  1.0          0.000            -40.119
   0    6  1.0  1.0           0     1  1.0  1.0          0.000             -0.197
   0    6  1.0  1.0           0     3  1.0  1.0          0.000              8.724
   0    7  1.0  1.0           0     1  1.0  1.0          0.000             -2.695

...

   1    0  0.0  0.0           0     4  1.0  1.0         16.671            -39.318
   1    0  0.0  0.0           0     5  1.0  1.0        -41.569             12.256
   1    0  0.0  0.0           0     4  1.0  0.0         -0.000            -49.087
   1    0  0.0  0.0           0     5  1.0  0.0         -0.000            -47.869
   1    0  0.0  0.0           0     4  1.0 -1.0         16.671             39.318
   1    0  0.0  0.0           0     5  1.0 -1.0        -41.569            -12.256
   1    1  0.0  0.0           0     0  1.0  1.0          0.294              0.336
   1    1  0.0  0.0           0     4  1.0  1.0         41.742            -12.307
/
...
```

followed by the printing of the SOC Hamiltonian 

```orca
Note: In the following the full <I|HBO+SOC|J> are printed in the CI Basis.     
      I,J are compound indices for |Block/Mult, Ms, Root>, where the states    
      are ordered first by MultBlock, then Ms and finally Root.                
-----------------
SOC MATRIX (A.U.)
-----------------
```

Finally, the relativistically corrected eigenvalues and eigenvectors are printed

```orca
Lowest eigenvalue of the SOC matrix:    -149.86223277 Eh
Energy stabilization:    -2.54512 cm-1
Eigenvalues:     cm-1         eV      Boltzmann populations at T =  300.000 K
   0:            0.00        0.0000       3.36e-01
   1:            2.37        0.0003       3.32e-01
   2:            2.37        0.0003       3.32e-01
   3:         7757.65        0.9618       2.33e-17
   4:         7757.66        0.9618       2.33e-17
   5:        11913.81        1.4771       5.15e-26

...

The threshold for printing is 0.0100
Eigenvectors:
                         Weight      Real          Image    : Block Root  Spin   Ms
 STATE   0:       0.0000
                         0.388265     0.410320    -0.468937 :     0    0    1    1
                         0.223270    -0.000000     0.472514 :     0    0    1    0
                         0.388265     0.410320     0.468937 :     0    0    1   -1
 STATE   1:       2.3703
                         0.310686     0.534586     0.157809 :     0    0    1    1
                         0.378606     0.000017    -0.615309 :     0    0    1    0
                         0.310706     0.534623    -0.157747 :     0    0    1   -1
 STATE   2:       2.3703
                         0.300970    -0.214003    -0.505146 :     0    0    1    1
                         0.398078    -0.000007    -0.630934 :     0    0    1    0
                         0.300949    -0.214019     0.505119 :     0    0    1   -1

...


```

Now, all relevant QDPT properties are calculated and printed:

```orca
*************************************
COMPUTING QDPT PROPERTIES
*************************************
```

(1) For g-Tensor/Matrix
```orca
----------------------------------------------
ELECTRONIC G-MATRIX FROM EFFECTIVE HAMILTONIAN
----------------------------------------------
```

(2) For ZFS (D-Tensor/Matrix) on the basis of the 2nd-order and Effective Hamiltonian approximations
```orca
--------------------------------------------
           ZERO-FIELD SPLITTING
2ND ORDER SOC CONTRIBUTION
--------------------------------------------
--------------------------------------------------------
                  ZERO-FIELD SPLITTING
EFFECTIVE HAMILTONIAN SOC CONTRIBUTION
--------------------------------------------------------
```

(3) For HFC (A-Tensor/Matrix)
```orca
-------------------------
QDPT HFC A-MATRICES
-------------------------
```

In the CASSCF and LFT modules, one may request the A-Matrix using, for example:
```orca
AMatrix true
AMatrixNuc 0, 2      
```

If requested, one can specify isotopes for the calculations 

```orca
AMatrix true
AMatrixNuc 0, 2, 3

# e.g. for Nuclei 0, this requires partially or fully populating the
# following quantities:

AMATRIXP[0]=125.6   #the P-value for the hyperfine ge*gN*beta*betaN
AMATRIXQ[0]=3.87    #the quadrupole value (in barn)
AMATRIXIP[0]=2.5    #spin of the isotope for the A-tensor
AMATRIXIQ[0]=0.0    #spin of the isotope of the Q-tensor
AMATRIXTP[0]=237    #AMatrixISTPP[0]
AMATRIXTQ[0]=0      #AMatrixISTPQ[0]

# It follows that for Nuclei 2, one does 
AMATRIXTP[1]=36
...
# and so on.
```

(4) For Electric Field Gradient Tensor
```orca
---------------------------------------
EFG TENSOR
---------------------------------------
```

(5) & (6) For Magnetization/Susceptibility 
```orca
-------------------------------------------------
SOC CORRECTED MAGNETIZATION AND/OR SUSCEPTIBILITY
-------------------------------------------------
```

(7) For External Magnetic Fields Contributions 
```orca
----------------------------------------------------------------------------------------------------------
               SOC TRANSITION MAGNETIC DIPOLE CONTRIBUTIONS IN EXTERNAL MAGNETIC FIELD                
           Magnetic field Bx =       1.00 Gauss  By =       0.00 Gauss  Bz =       0.00 Gauss
----------------------------------------------------------------------------------------------------------
 States       Energy      Energy     Osh.Str           M2            MX             MY             MZ     
              (cm-1)       (eV)        (au)          (au**2)        (au)           (au)           (au)    
----------------------------------------------------------------------------------------------------------
 0  0         0.00       0.0000     0.00000000     0.00000145     0.00090159     0.00061858     0.00050413
 0  1        20.20       0.0025     0.00000000     0.00000126     0.00042808     0.00067630     0.00078545
 1  1         0.00       0.0000     0.00000000     0.00000000     0.00003430     0.00002347     0.00001909
----------------------------------------------------------------------------------------------------------
```

Following this, all relativistically corrected optical spectra are printed under the same correction scheme
(as Discussed in {ref}`sec:spectroscopyproperties.ops`).

```orca
--------------------------------------------------------------------------------------------------------
      SOC CORRECTED ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS    
--------------------------------------------------------------------------------------------------------
      Transition         Energy     Energy  Wavelength fosc(D2)      D2       |DX|      |DY|      |DZ|  
                          (eV)      (cm-1)    (nm)  (*population)  (au**2)    (au)      (au)      (au)  
--------------------------------------------------------------------------------------------------------

...

```

(8) Sum-over-states g- and A-tensors/matrices (for now, available only in CASSCF and MRCI) get printed in much
the same way as those of the Effective Hamiltonian. The main difference here is the designator:
```orca
---------------------------------------------------------------------------
SUM OVER STATES CALCULATION OF THE SPIN HAMILTONIAN (for g and HFC tensors)
---------------------------------------------------------------------------
```
The matrix elements that are used in the summation are printed after
```orca
-----------------------
MATRIX ELEMENT PRINTING
-----------------------
```
The g-tensor additionally prints out the contribution of each state to the `g(OZ/SOC)` term.
```orca
-------------------------------
BREAKDOWN OF g(OZ/SOC) BY STATE
-------------------------------

STATE                                g1           g2           g3
--------------------------------------------------------------------
```
Note that for CASSCF, {ref}`sec:spectroscopyproperties.casscfresp` without the orbital response is equivalent 
to the sum-over-states when including all states. As such, the main draw of the sum-over-states is this
state-by-state breakdown.


If the SSC is requested, Spin-Spin Coupling contributions will be generated in a second step and will be added to the SOC Hamiltonian to generate SOC+SSC contributions

```orca
-------------------------------------------
Calculating Spin-Spin Coupling Integrals
-------------------------------------------
```

The program will then undergo the exact same analysis as above, printing the SOC+SSC analysis.
 ```orca
***********************************************************
* DOING EVERYTHING A SECOND TIME: THIS TIME INCLUDING SSC *
***********************************************************

*************************************
COMPUTING QDPT HAMILTONIAN
*************************************

*************************************
Doing QDPT with SOC AND SSC!
*************************************

------------------------------------
NONZERO SOC and SSC MATRIX ELEMENTS (cm**-1)
------------------------------------

           Bra                       Ket       
<Block Root S   Ms  | HSOC + HSSC |  Block Root  S    Ms> =  Real-part  Imaginary part
--------------------------------------------------------------------------------------
   0    2  1.0  1.0                  0     1  1.0  1.0       -0.000        -71.172
   0    3  1.0  1.0                  0     1  1.0  1.0       -0.001          0.000
   0    3  1.0  1.0                  0     2  1.0  1.0        0.020          1.542
   0    4  1.0  1.0                  0     0  1.0  1.0       -0.222         50.048
   0    5  1.0  1.0                  0     0  1.0  1.0       -0.228        -48.827
   0    5  1.0  1.0                  0     4  1.0  1.0        0.332        -40.119
   0    6  1.0  1.0                  0     1  1.0  1.0       -0.030         -0.197

```

This is done for both the magnetic properties, e.g. the ZFS,

```orca
--------------------------------------------------------
                  ZERO-FIELD SPLITTING
EFFECTIVE HAMILTONIAN SOC and SSC CONTRIBUTION
--------------------------------------------------------
```

as well as the optical properties

```orca
--------------------------------------------------------------------------------------------------------
  SOC+SSC CORRECTED ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS    
--------------------------------------------------------------------------------------------------------
      Transition         Energy     Energy  Wavelength fosc(D2)      D2       |DX|      |DY|      |DZ|  
                          (eV)      (cm-1)    (nm)  (*population)  (au**2)    (au)      (au)      (au)  
--------------------------------------------------------------------------------------------------------
```

