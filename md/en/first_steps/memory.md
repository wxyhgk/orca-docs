---
title: Memory Settings
source: https://www.faccts.de/docs/orca/6.1/tutorials/first_steps/memory.html
---

# Memory Settings

Some calculations, in particular these using wave-function based correlation methods, can be very memory-hungry and thus it is important to control the memory settings for your ORCA calculation.

In ORCA, the easiest way to set the memory in megabyte (MB) per processing core is via the global `%MaxCore` variable. For example, `%MaxCore 2000` in a 4 core run (cf. [Parallel Calculations in ORCA](../first_steps/parallel.md#sec-firststeps-parallel)) will reserve 8000 MB of memory.

```orca
%MaxCore 2000
```

> **Notes on Memory in ORCA**
> 1. `%MaxCore` set the memory in megabyte (MB) **per processing core**.
> 2. Memory is given in **megabyte**
> 3. This memory setting always refers to the dominant work area, thus **ORCA can take more memory** than defined via `%MaxCore`! Accordingly, only about 80% of the available memory should be allocated.
> 4. Some memory-hungry operations will take longer if given less than the required memory, while others will abort completely if `%MaxCore` is insufficient.
> 5. The default memory in ORCA is 4096 MB, i.e., `%MaxCore 4096`

## Example 1: `Not enough memory available!`

The self-consistent-field module is one of the modules that aborts immediately when the available memory is insufficient. For example, setting `%MaxCore` to 1 MB will be insufficient for the SCF calculation of dihydrogen with the PBE DFT functional and the large quadruple-$\zeta$ basis def2-QZVPPD.

```orcainput
!PBE def2-QZVPPD

%MaxCore 1

*xyz 0 1
H 0 0 0
H 1 1 1
end
```

The calculation will abort with an error message reporting the given and an estimate of the required memory.

```orca
 Error  (ORCA_SCF): Not enough memory available!
                    Memory available for SCF calculation:          1.0 MB
                    Memory needed (estimated)           :          5.2 MB
       ====>        Please increase MaxCore to more than:          5.2 MB

Error (ORCA_SCF): ... aborting the run
```

If we now increase the given memory to ORCA's default value of 4096 MB, which is much more than needed for this very small calculation, ORCA will run successfully.

```orcainput
!PBE def2-QZVPPD

%MaxCore 4096

*xyz 0 1
H 0 0 0
H 1 1 1
end
```

ORCA will also report the actually used memory per calculation part in its output.

```orca
Maximum memory used throughout the entire STARTUP-calculation: 11.2 MB
[...]
Maximum memory used throughout the entire GUESS-calculation: 5.4 MB
[...]
Maximum memory used throughout the entire LEANSCF-calculation: 4.0 MB
[...]
Maximum memory used throughout the entire PROP-calculation: 2.8 MB
[...]
                             ****ORCA TERMINATED NORMALLY****
```
