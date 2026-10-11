```{index} HFLD
```

(sec:spectroscopyproperties.hfld)=
# The Hartree-Fock plus London Dispersion (HFLD) Method

The efficient and accurate HFLD method{cite}`HFLD`
can be used for the quantification and analysis of noncovalent
interactions between a pair of user-defined fragments. Starting from
ORCA 5.0, an open shell variant of the HFLD method is
also available.{cite}`HFLDos`

The leading idea here is to solve the DLPNO coupled cluster equations
while neglecting intramonomer correlation. The LED scheme is then used
to extract the London dispersion (LD) energy from the intermolecular
part of the correlation. Finally, the resulting LD energy is used to
correct interaction energies computed at the HF level. Hence, HFLD can
be considered as a dispersion-corrected HF approach in which the
dispersion interaction between the fragments is added at the DLPNO-CC
level. As such, it is particularly accurate for the quantification of
noncovalent interactions such as those found in H-bonded systems,
pre-reactive intermediates (e.g., Frustrated Lewis Pairs), dispersion
and electrostatically bound systems. Larger errors are in principle
expected for transition metal complexes, as it is the case for any
dispersion corrected Hartree-Fock scheme.

The efficiency of the approach allows the study of noncovalent
interactions in systems with several hundreds of atoms. 

Some of the most important aspects of the method are summarized below:

-   **Accuracy and Recommended Settings** \
    For noncovalent interactions,
    HFLD typically provides an accuracy comparable to that of the
    DLPNO-CCSD(T) method if default PNO settings are used. For the HFLD
    scheme, these are defined as TCutPNO = 3.3e-7 and TCutPairs 1e-5. If
    used in conjuction with a def2-TZVP(-f) basis set, these settings
    are typically denoted as `HFLD*` and are recommended for standard
    applications on large systems {cite}`HFLDos`. For example, `HFLD*`
    settings were used in Ref. {cite}`altun2021unveiling` to elucidate the
    complex pattern of interactions responsible for the stability of the
    DNA duplex. If great accuracy is required, it is recommended to use
    TightPNO settings in conjuction with TCutPNO 1e-8 and two-point
    basis set extrapolation (aug-cc-pVTZ/aug-cc-pVQZ) to approach the
    CBS limit. These settings are typically denoted as the **gold** HFLD
    settings {cite}`HFLDos`.

-   **Reference determinant in the Open shell HFLD scheme** \
    In the open shell case, HFLD relies on a restricted reference determinant for
    the calculation of the LD energy. If the QRO determinant is used as
    reference, the reference interaction energy can in principle be
    computed at the UHF or QRO levels. This leads to two different
    schemes, namely the QRO/HFLD and UHF/HFLD. Alternatively, the
    restricted open-shell HF (ROHF) determinant can be used as reference
    in HFLD calculations, which leads to the ROHF/HFLD approach. The
    energy value reported as `FINAL SINGLE POINT ENERGY` in the output
    corresponds to the UHF/HFLD scheme by default, which is typically
    slightly more accurate. See Ref. {cite}`HFLDos` for details.

-   **Efficency** \
    The calculation of the dispersion correction typically
    requires the same time as an HF calculation. This is true for small
    as well as for large systems.

-   **Analysis of Intermolecular Interactions** \
    The HFLD method can be
    combined with the Local Energy Decomposition (LED) to study
    intermolecular interactions in great detail. The LED dispersion
    energy obtained with HFLD is often very close to that obtained from
    a full DLPNO-CCSD(T) calculation. Hence, HFLD can be used as a
    cost-effective alternative to DLPNO-CCSD(T) to study, among other
    things, the importance of London dispersion in molecular chemistry.

-   **Additional considerations** \
     (i) One can specify `NormalPNO` or
    `TightPNO` settings in the simple input line. The corresponding
    DLPNO thresholds would be in this case fully consistent with those
    used in the DLPNO-CCSD(T) method. (ii) The dispersion energy in the
    HFLD approach slightly depends on the choice of the localization
    scheme used for occupied orbitals and PNOs. Default settings are
    recommended for all intents and purposes. However, it is important to
    note that the localization iterations for occupied and virtual
    orbitals must be fully converged in order to obtain consistent
    results. To achieve this goal, it might be necessary to increase
    `LocMaxIter` or `LocMaxIterLed` (see below). However, this is
    typically necessary only if very large basis sets (e.g. aug-cc-pV5Z)
    are used. (iii) Importantly, the method benefits from the use of
    tightly converged SCF solutions. For closed-shell systems, a useful
    diagnostic in this context is the "Singles energy" term that is
    printed in the LED part of the output. This term must be smaller
    than 1e-6 for closed shell species. If this is not the case, one
    should change the settings used for the SCF iterations. Note also
    that all the features of the LED scheme (e.g. automatic
    fragmentation) are also available for the HFLD method. 

Note that, as HFLD relies on both the DLPNO-CCSD(T) and LED methods, the
options of both schemes can be used in principle in conjunction with
HFLD. Some examples are shown below:

```orca
! HFLD aug-cc-pVDZ aug-cc-pVDZ/C aug-cc-pVTZ/JK RIJK TightSCF

%mdci
  LED 1               # localization method for the PNOs. Choices:
                      # 1 = PipekMezey 
                      # 2 = FosterBoys (default, recommeded for the HFLD method)
  PrintLevel 3        # Selects large output for LED and prints the
                      # detailed contribution
                      # of each DLPNO-CCSD strong pair
  LocMaxIterLed 600   # Maximum number of localization iterations for PNOs
  LocMaxIter    300   # Maximum number of localization iterations for 
                      # occupied orbitals
  LocTolLed     1e-6  # Absolute threshold for the localization procedure for PNOs
  DoLEDHF true        # Decomposes the reference energy in the LED part. 
                      # By default, it is set to false in HFLD for efficiency reasons.
  TCutPNO    3.33e-7  # cutoff for PNO occupation numbers.  
  TCutPairs  1e-5     # cutoff for estimated pair correlation energies
                      # to be included in the CC treatment
end
```

(sec:spectroscopyproperties.hfld.basicusage)=
## Basic Usage

The Hartree-Fock plus London Dispersion method is invoked using the `!HFLD` keyword in the simple input line:

```orca
! HFLD aug-cc-pvdz aug-cc-pvdz/C
```

(sec:spectroscopyproperties.hfld.example)=
## Example

An input example is reported below.

```{literalinclude} ../../orca_working_input/C05S13_241.inp
:language: orca
```

In the corresponding output, after the DLPNO-CC iterations and the LED
output, the following information is printed:

```
----------------------------   ----------------
Inter-fragment dispersion       -0.001871763
----------------------------   ----------------


-------------------------   --------------------
FINAL SINGLE POINT ENERGY      -114.932878050741 
-------------------------   --------------------
```

The total HFLD energy of the adduct is thus -114.932878050741 a.u.. To
compute interaction energies, we have to subtract from this value the
Hartree-Fock energies of the monomers in the geometry they have in the
complex, i.e., -38.884413525377 and -76.040412827089 a.u. for CH$_2$ and
H$_2$O, respectively. The total interaction energy is thus -0.00805 a.u.
or -5.1 kcal/mol (the corresponding DLPNO-CCSD(T)/TightPNO/CBS value is
-5.3 kcal/mol {cite}`altun2018open`). Note that, to obtain binding energies,
the geometric preparation should be added to this value. This can be
computed using a standard computational method, e.g, DFT or
DLPNO-CCSD(T).

(sec:spectroscopyproperties.hfld.led)= 
## Combined HFLD/LED Analysis

For a combined HFLD/LED analysis, the HF/LED decomposition must be enabled in the `%mdci` block:

```orca
! %mdci DoLEDHF True end
```

### Example

Below is a sample HFLD/LED input for the DNA supersystem (supersystem) shown in {numref}`fig:LED_HeatMap`,
using the default `NormalPNO*` settings: 

```orca
! HFLD def2-TZVP(-f) RIJCOSX DefGrid3 def2/J def2-TZVP/C 
! VeryTightSCF CPCM(water)

%mdci DoLedHF True   # HFLD default: False
      HFFragInter {1 2} {1 3} {2 3} {4 5} {4 6} {5 6}
      end
```

Coordinate and fragment label specifications are as in Section {numref}`sec:spectroscopyproperties.led.multifrag_led`.

The HFLD method fundamentally simplifies calculations by neglecting intra-subsystem electron correlation. By default, HFLD implemetation
treats each fragment as a separate subsystem. However, a subsystem does not necessarily consist of a single fragment, as in the case of 
inter-strand interactions in a DNA duplex. In such cases, the program must be explicitly informed which fragments compose each subsystem.
This can be done by specifying fragment pairs to be excluded from correlation explicitly via the `HFFragInter` directive in the `%mdci`
block. In the example above, this directive sets the correlation energy among strand K fragments (1–3) and among strand L fragments (4–6)
to zero. Note that intra-fragment correlations (e.g. `HFFragInter {1 1} {2 2} ...`) do not need to be specified explicitly, as they are
automatically excluded when the `HFLD` keyword is used.

To compute the interaction energy, input files must also be prepared for each subsystem. If a subsystem consists of only one fragment, 
a reference-level calculation (RHF or QRO) is sufficient for that subsystem. In this case, the `LED` keyword, the PNO setting keywords
(`LoosePNO`, `NormalPNO`, or `TightPNO`), and the entire `%mdci` block must be removed from the corresponding subsystem input.

For a multi-fragment subsystem, a reference-level calculation combined with LED analysis (RHF/LED or QRO/LED) is required. However, LED
analysis cannot be invoked at the reference level alone in the current ORCA version. As a workaround, a low-cost DLPNO-CCSD or HFLD
calculation can be performed to obtain the necessary LED data efficiently:

```orca
! HFLD def2-TZVP(-f) RIJCOSX DefGrid3 def2/J def2-TZVP/C 
! VeryTightSCF CPCM(water) LoosePNO

%mdci DoLedHF True   # HFLD default: False
      maxiter 0
      end
```

In this example, the `maxiter 0` directive in the `%mdci` block bypasses unnecessary coupled-cluster iterations. 
While configuring such low-cost calculations, ensure the correlation space is not truncated too aggressively since at least one
electron pair must remain for LED analysis to proceed. Here LoosePNO settings are used, but if they exclude all pairs, slightly
tighter settings may be required. For large systems, the HFFragInter directive can further reduce cost by selectively excluding
interfragment correlations. However, avoid excluding all electron pairs, which disables LED analysis entirely.

Note that if a DLPNO-CCSD(T) calculation for a single-fragment subsystem, or a DLPNO-CCSD(T)/LED calculation for a multi-fragment
subsystem, has already been performed, the corresponding ORCA output file can be used directly in combined HFLD/LED analyses,
eliminating the need for additional subsystem calculations.

(sec:spectroscopyproperties.hfld.keywords)=
## Keywords
```{index} HFLD Keywords
```

:::{note}
As HFLD relies on both the DLPNO-CCSD(T) and LED methods, 
the options of both schemes can be used in principle in conjunction with HFLD.
:::

(tab:spectroscopyproperties.hfld.keywords.simple)=
:::{table} Simple input keywords for the Hartree Fock plus London Dispersion.
| Keyword                         | Description                                       |
|:--------------------------------|:--------------------------------------------------|
| `HFLD`                          | Activates the Hartree Fock plus London Dispersion method |
:::

:::{raw} latex
\begingroup
\footnotesize
:::

:::{tabularcolumns} \Y{0.25}\Y{0.2}\Y{0.55}
:::
(tab:spectroscopyproperties.hfld.keywords.block)=
:::{flat-table} `%mdci` block input keywords for the Hartree–Fock plus London Dispersion.
:header-rows: 1
:class: longtable
:class: footnotesize
* - Keyword
  - Options
  - Description
* - `LED`
  - `1`
  - Pipek–Mezey used as localization method for the PNOs
* - 
  - `2`
  - Foster–Boys used as localization method for the PNOs (default starting from ORCA 4.2)
* - `PrintLevel`
  - `3`
  - Selects large output for LED and prints the detailed contribution of each DLPNO-CCSD strong pair
* - `LocMaxIterLed`
  - `<integer>`
  - Maximum number of localization iterations for PNOs (set to 600 by default)
* - `LocMaxIter`
  - `<integer>`
  - Maximum number of localization iterations for occupied orbitals (set to 128 by default)
* - `LocTocLed`
  - `<real>`
  - Absolute threshold for the localization procedure for PNOs (set to 1e-6 by default)
* - `DoLEDHF`
  - `true/false`
  - Decomposes the reference energy in the LED part (by default, it is set to false in HFLD for efficiency reasons)
* - `TCutPNO`
  - `<real>`
  - Cutoff for PNO occupation numbers (set to 3.33e-7 by default)
* - `TCutPairs`
  - `<real>`
  - Cutoff for estimated pair correlation energies to be included in the CC treatment (set to 1e-5 by default)
:::
:::{raw} latex
\endgroup
:::
