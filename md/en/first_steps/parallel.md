---
title: Running a Calculation in Parallel
source: https://www.faccts.de/docs/orca/6.1/tutorials/first_steps/parallel.html
---

# Running a Calculation in Parallel

ORCA can run in multiple processors with the aid of [OpenMPI](https://www.open-mpi.org/)
(the recommended version for ORCA 6 is 4.1.6). After installing it and setting the `PATH` and `LD_LIBRARY_PATH` variables (what is that? [Assigning PATH variables](../first_steps/trouble_install.md#path-variable), you can simply run in parallel using the PAL keyword. For instance, a calculation using four processors requires:

```text
!HF def2-SVP PAL4
```

For more than eight (`!PAL8`) or exactly 16 (`!PAL16`) processors, the explicit `NProcs` setting in the `%pal` block has to be used:

```text
!HF def2-SVP

%pal 
   NProcs 28 
end
```

When running calculations in parallel, always use the full path to ORCA:

```text
./full/path/to/orca input.inp
```

> **Important**
> Always install the OpenMPI version indicated in the Download section!
