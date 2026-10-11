<a id="sec:essentialelements.parallel"></a>
# Parallel and Multi-Process Runs

Most of the important modules in ORCA can run in parallel or in multi-process mode:
There are parallel versions for Linux, MAC and Windows computers which make use of [OpenMPI (open-source MPI
implementation)](https://www.open-mpi.org/) and Microsoft MPI (Windows only).
Parallel execution means that the different processes perform the task in synchronous manner, communicating results and synchronizing execution (via MPI).
The multi-process mode also employs multiple processes. But these work independently, not knowing - and not needing to know what the other processes are doing. The latest ORCA version even can combine both modes. Please see the remarks in [hints.multiprocess](#sec:essentialelements.parallel.hints.multiprocess) for more details.

Parallel (or multi-process) execution is requested in the input via
   ```orca
   ! PAL4  # everything from PAL2 to PAL8 and Pal16, Pal32, Pal64 is recognized
   ```
   or
   ```orca
   %pal nprocs 4 end # any number (positive integer)
   ```
Assuming that the MPI libraries are properly installed on your computer, it is fairly easy to
run the parallel version of ORCA:
You simply specify the number of parallel processes in the input and call (serial) ORCA (with full path!)
The parallelized modules of ORCA are started by the (serial) ORCA-Driver.
If the driver finds `PAL4` or `%pal nprocs 4 end` (e.g.) in the input,
it will start up the parallel modules instead of the serial ones.
!!! warning
    Do not start the ORCA driver with mpirun!

(Please see section [parallel.hints](#sec:essentialelements.parallel.hints) for what else has to be taken care of for a successfull parallel run of ORCA.)

<a id="sec:essentialelements.parallel.calling"></a>
## Parallel and Multi-Process Modules
The following modules and utility programs are presently
parallelized - or usable in Multi-Process Mode:

### List of Parallelized Modules
|  |
| --- |
| AUTOCI - all methods |
| CASSCF / NEVPT2 / CASPT2 / CASSCFRESP |
| CIPSI |
| CIS/TDDFT / CISRESP |
| EDA |
| GRAD |
| GUESS |
| LEANSCF |
| MAGRELAX |
| MCRPA |
| MDCI (Canonical- and DLPNO-Methods) |
| MM |
| MP2 and RI-MP2 (including Gradients) |
| MRCI |
| PC |
| PLOT |
| PNMR |
| POP |
| PROP |
| PROPINT |
| REL |
| ROCIS |
| SCFGRAD |
| SCFRESP (with SCFHessian) |
| STARTUP |
| VPOT |

(For a complete list of all modules and the description of their functionality, please refer to [programs.general](../orcaarchitecture/components.md#sec:programs.general))

The efficiency of the parallel modules is such that for RI-DFT perhaps up to 16 processors are a
good idea while for hybrid DFT and Hartree-Fock a few more processors are appropriate.
Above this, the overhead becomes significant and the parallelization loses efficiency.
Coupled-cluster calculations usually scale well up to at least 8 processors but probably it is also worthwhile to try 16.

### List of Multi-Process Modules
|  |
| --- |
| Numerical Gradients, Frequencies, Overtones-and-Combination-Bands |
| VPT2 |
| NEB (Nudged Elastic Band) |
| GOAT (Global Optimizer Algorithm) |

For Numerical Frequencies or Gradient runs it makes sense to choose nprocs = 4 or 8 times 6\*Number of Atoms.
For VPT2 on larger systems you may well even try 16 times 6\*Number of Atoms -
if you use multiple processes per displacement.
(Please check out the section [parallel.hints](#sec:essentialelements.parallel.hints) what you have to take care of for such kind of calculations.)

!!! note
    Parallelization is a difficult undertaking and there are many
    different protocols that work differently for different machines.
    Please understand that we can not provide support for each and every
    platform. We are trying our best to make the parallelization
    transparent and provide executables for various platforms but we can
    not guarantee that they always work on every system. Please
    see the download information for details of the version.

<a id="sec:essentialelements.parallel.hints"></a>
## Hints on the Use of Parallel ORCA

Many questions that are asked in the discussion forum deal with the
parallel version of ORCA. Please understand that we cannot possibly
provide one-on-one support for every parallel computer in the world. So,
 please make every effort to solve the technical problems locally
together with your system administrator. Here are some explanations about what
is special to the parallel version, which problems might arise from this and how to deal with them:

<a id="sec:essentialelements.parallel.hints.singlenode"></a>
### Single Node Runs

1. Parallel ORCA can be used with OpenMPI (on Linux and MAC) or MS-MPI
   (on windows) only. Please see the download information for details of
   the relevant OpenMPI-version for your platform.

   The OpenMPI version is configurable in a large variety of ways,
   which cannot be covered here. For a more detailed explanation of all
   available options, cf. <http://www.open-mpi.org>

2. Please note that the OpenMPI version is dynamically linked, that is,
   it needs at runtime the OpenMPI libraries (and several other standard
   libraries)! If you compile MPI on your own computer, you also need to have
   a fortran compiler, as `mpirun` will contain fortran bindings.

   (Remember to set `PATH` and `LD_LIBRARY_PATH` to mpirun and the mpi libraries)

3. Many problems arise, because ORCA does not find its parallel
   executables. To avoid this, it is crucial to call ORCA with its
   complete pathname. The easiest and safest way to do so is to include the
   directory with the ORCA-executables in your `$PATH`. Then start the
   calculation:
   ```sh
   - interactively: 
     start orca with full path: "/mypath_orca_executables/orca MyMol.inp"
   - batch : 
     set your path: `export PATH=/mypath_orca_executables:$PATH` (for bash) then 
     start orca with full path: "$PATH/orca $jobname.inp"
   ```
   This seems redundant, but it really is important if you want to run a
   parallel calculation to call ORCA with the full path! Otherwise it will not
   be able to find the parallel executables.

4. It is recommended to run orca in local (not nfs-mounted)
   scratch-directories, (`/tmp1` or `/usr/local` e.g.) and to
   renew these directories for each run to avoid confusion with left-overs
   of a previous run.

5. It has proven convenient to use "wrapper" scripts. These scripts should

   ```orca
   - set the path
   - create local scratch directories
   - copy input files to the scratch directory
   - start orca
   - save your results
   - remove the scratch directory
   ```

   A basic example of such a submission script for the parallel ORCA
   version is shown later (13.) (this is for the Torque/PBS queuing system,
   running on Apple Mac OS X):

6. Parallel ORCA distinguishes the following cases of disk availability:

   1. each process works on its own (private) scratch directory
      (the data on this directory cannot be seen by any other process).
      This is flagged by **"working on local scratch directories"**
   2. all processes work in a common scratch directory (all processes can
      see all file-data) ORCA will distinguish two situations:
      * all processes are on the same node - flagged by **"working on a common directory"**
      * the processes are distributed over multiple nodes
        but accessing a shared filesysten - flagged by **"working on a shared directory"**
   3. there are at least 2 groups of processes on different scratch
      directories, one of the groups consisting of more than 1 process -
      flagged by **"working on distributed directories"**

   Parallel ORCA will find out, which of these cases exists and will handle the I/O
   respectively. If ORCA states disk availability differently from what you
   would expect, check the number of available nodes and/or the
   distribution pattern (fill_up/round_robin)

7. It is possible to pass additional MPI-parameters to mpirun by
   adding these arguments to the ORCA call - all arguments enclosed in a single pair of quotes:

   ```sh
   /mypath_orca_executables/orca MyMol.inp "--bind-to none"
   ```
   -- or -- for multiple arguments
   ```sh
   /mypath_orca_executables/orca MyMol.inp "--bind-to none --verbose"
   ```

<a id="sec:essentialelements.parallel.hints.multiplenodes"></a>
### Multi-Node Runs - Remote Execution

1. If Parallel ORCA finds a file named "`MyMol.nodes`" in the directory
   where it's running, it will use the nodes listed in this file to start
   the processes on, provided your input file was "`MyMol.inp`". You can
   use this file as your machinefile specifying your nodes, using the usual
   OpenMPI machinefile notation.

   ```orca
   node1 cpu=2
   node2 cpu=2
   ```
   or
   ```orca
   node1
   node1
   node2
   node2
   ```

   If you run the Parallel ORCA version on only one computer, you do not need to provide a nodefile, and
   neither have to enable an rsh/ssh access, as in this case the processes
   will simply be forked! If you start ORCA within a queueing system, you
   also don't need to provide a nodefile. The queueing system will care for it.

2. If the ORCA-environment variables are not equally defined on all
   participating compute nodes it might be advisable to export these variables.
   This can be achieved by passing the following additional parameters to mpirun
   via the ORCA call:

   ```sh
   /mypath_orca_executables/orca MyMol.inp "-x LD_LIBRARY_PATH -x PATH"
    ```

3. OpenMPI requires that the PATH environment variable be set to find executables on remote nodes.
    As it is not always possible to change the startup scripts accordingly, OpenMPI provides the additional option: "`--prefix`"
    Calling ORCA and requesting multiple processes for the parallelized modules should then look like
    ```
    /mypath_orca_executables/orca MyMol.inp "--prefix /my-openmpi-folder"
    /mypath_orca_executables/orca MyMol.inp "--prefix /my-openmpi-folder --machinefile MyMol.nodes" (if not started via queueing system)
    ```
    As ORCA is dynamically linked it also needs to know the location of the ORCA libraries
    This can be communicated via
    ```
    /mypath_orca_executables/orca MyMol.inp "--prefix /my-openmpi-folder --machinefile MyMol.nodes -x LD_LIBRARY_PATH"
    ```

<a id="sec:essentialelements.parallel.hints.multiprocess"></a>
### Multi-Process Calculations

1. An additional remark on multi-process numerical calculations (Frequencies, Gradient, (Hybrid) Hessian), VPT2, NEB, GOAT:\
    The processes that execute these calculations do not work in parallel, but independently, often in
    a totally asynchronous manner. The numerical calculations will start as
    many processes, as you dedicated for the parallel parts before and they
    will run on the same nodes. If your calculation runs on multiple nodes,
    you have to set the environment variable `RSH_COMMAND` to either "`rsh`" or "`ssh`".
    If `RSH_COMMAND` is not defined, ORCA will abort. This prevents that all processes of a
    multi-node run are started on the 'master'-node.

2. On multiple user request the 'parallelization' of NumCalc has been made more flexible.
    If before ORCA would start nprocs displacements with a single process each,
    the user can now decide on how many processes should work together on a single displacement.

    For this the nprocs keyword got a sibling:

    ```orca
    %pal nprocs       32 # or nprocs_world - total number of parallel processes
         nprocs_group  4 #                 - number of parallel processes per sub-task
         end
    ```

    This setting will ORCA make use 32 processes, with 4 processes working on the same displacement,
    thus running 8 displacements simultaneously.
    The methods that can profit from this new feature are
    - all NumCalc-methods: as NumGrad, NumFreq, VPT2, Overtones, NEB, and GOAT.
    - the analytical (parallel) Hessian, leading to a nice increase of parallel performance for really large calculations.

    It is highly recommended to choose nprocs_group to be an integer divisor of nprocs_world!

    For convenient use a couple of standard 'groupings' are made available via simple input keyword:
    ```orca
    !PAL4(2x2)  # 2 groups a 2 workers
    !PAL8(4x2)  # 4 groups a 2 workers
    !PAL8(2x4)  # ...
    !PAL16(4x4)
    !PAL32(8x4)
    !PAL32(4x8)
    !PAL64(8x8)
    ```
!!! tip
    mpirun automatically binds processes as of the start of the v1.8 series.
    For NumCalc this can result in all displacements being run on the same set of cores, leading to severe performance degradation.
    There are different workarounds for this:

    - You can switch off this behaviour by passing `bind-to none` as additional MPI-parameter to ORCA.
    - Alternatively you can disable the binding via environment setting: `OMPI_MCA_hwloc_base_binding_policy none`
    - The most efficient solution is to use a resource manager (such as SLURM, PBS or others) and make sure Open MPI was built to support it.
    These resource managers will make sure that each job will run on a different set of cores.
    This way you will have the advantage of binding without the problem of running multiple calculations on the same cores.

!!! note
    If your system-administration does not allow to connect via rsh/ssh to other compute nodes, you unfortunately cannot make use of parallel sub-calculations within NumCalc runs.
    This affects NEB as well as GOAT, VPT2, Overtone-and-Combination-Bands, and Numerical Frequencies and Gradients.

4. Wrapper script to start ORCA
   ```zsh
   #!/bin/zsh 
   
   setopt EXTENDED_GLOB
   setopt NULL_GLOB  
   #export MKL_NUM_THREADS=1
   
   b=${1:r}
   
   #get number of procs.... close your eyes... (it really works!)
   if [[ ${$(grep -e '^!' $1):u} == !*(#b)PAL(<0-9>##)* ]]; then
     nprocs=$match
   let "nodes=nprocs"
   elif [[ ${(j: :) $(grep -v '^#' $1):u} == *%(#b)PAL*NPROCS' '#(<0-9>##)* ]]; then
     nprocs=$match
     let "nodes=nprocs"
   fi
   
   cat > ${b}.job <<EOF
   #!/bin/zsh
   #PBS -l nodes=1:ppn=${nodes:=1}
   #PBS -S /bin/zsh
   #PBS -l walltime=8760:00:00
   
   setopt EXTENDED_GLOB
   setopt NULL_GLOB
   export PATH=$PBS_O_PATH
   
   logfile=$PBS_O_WORKDIR/${b}.log
   tdir=$(mktemp -d /Volumes/scratch/$USER/${b}__XXXXXX)
   
   trap '
   echo "Job terminated from outer space!" >> $logfile
   rm -rf $tdir
   exit
   ' TERM 
   
   cp $PBS_O_WORKDIR/$1 $tdir
   foreach f ($PBS_O_WORKDIR/*.gbw $PBS_O_WORKDIR/*.pot) { cp $f $tdir }
   cd $tdir
   
   echo "Job started from ${PBS_O_HOST}, running on $(hostname) in $tdir using 
   $(which orca)" > $log
   file
   =orca $1 1>>$logfile 2>&1
   
   cp ^(*.(inp|tmp*))  $PBS_O_WORKDIR/
   rm -rf $tdir
   
   EOF

   qsub -j oe -o ${b}.job.out ${b}.job
   ```
