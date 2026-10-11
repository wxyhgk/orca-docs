(sec:essentialelements.parallel)=
# 并行与多进程运行（Parallel and Multi-Process Runs）

ORCA 中大多数重要模块都可以以并行或多进程模式运行：
Linux、Mac 和 Windows 计算机都有并行版本，它们使用 [OpenMPI（开源 MPI
实现）](https://www.open-mpi.org/) 和 Microsoft MPI（仅 Windows）。
并行执行意味着不同进程以同步方式执行任务，通过 MPI 通信结果并同步执行。
多进程模式也使用多个进程。但这些进程各自独立工作，不知道——也不需要知道其他进程在做什么。最新的 ORCA 版本甚至可以将这两种模式结合起来。详情请参见 {ref}`sec:essentialelements.parallel.hints.multiprocess` 中的说明。

并行（或多进程）执行通过在输入中
   ```orca
   ! PAL4  # everything from PAL2 to PAL8 and Pal16, Pal32, Pal64 is recognized
   ```
   或
   ```orca
   %pal nprocs 4 end # any number (positive integer)
   ```
来请求。
假设 MPI 库已在你的计算机上正确安装，运行并行版 ORCA 相当容易：
你只需在输入中指定并行进程数，然后（用完整路径！）调用（串行的）ORCA。
ORCA 的并行化模块由（串行的）ORCA-Driver 启动。
如果 driver 在输入中发现 `PAL4` 或 `%pal nprocs 4 end`（例如），
它将启动并行模块而非串行模块。
:::{warning}
不要用 mpirun 启动 ORCA driver！
:::
（关于成功进行 ORCA 并行运行还需要注意什么，请参见 {ref}`sec:essentialelements.parallel.hints` 一节。）

(sec:essentialelements.parallel.calling)=
## 并行与多进程模块（Parallel and Multi-Process Modules）
以下模块和实用程序目前已
并行化——或可在多进程模式下使用：


### 已并行化模块列表（List of Parallelized Modules）
:::{list-table}
* - AUTOCI - all methods
* - CASSCF / NEVPT2 / CASPT2 / CASSCFRESP
* - CIPSI
* - CIS/TDDFT / CISRESP
* - EDA
* - GRAD
* - GUESS
* - LEANSCF
* - MAGRELAX
* - MCRPA
* - MDCI (Canonical- and DLPNO-Methods)
* - MM
* - MP2 and RI-MP2 (including Gradients)
* - MRCI
* - PC
* - PLOT
* - PNMR
* - POP
* - PROP
* - PROPINT
* - REL
* - ROCIS
* - SCFGRAD
* - SCFRESP (with SCFHessian)
* - STARTUP
* - VPOT
:::
（关于所有模块的完整列表及其功能说明，请参阅 {ref}`sec:programs.general`）

并行模块的效率大致如下：对于 RI-DFT，最多用 16 个处理器可能是
个好主意，而对于杂化 DFT 和 Hartree--Fock，再多几个处理器较为合适。
超过这个数目，开销就会变得显著，并行化效率降低。
耦合簇计算通常至少到 8 个处理器都能良好扩展，但尝试 16 个也可能是值得的。

### 多进程模块列表（List of Multi-Process Modules）
:::{list-table}
* - Numerical Gradients, Frequencies, Overtones-and-Combination-Bands
* - VPT2
* - NEB (Nudged Elastic Band)
* - GOAT (Global Optimizer Algorithm)
:::

对于数值梯度或频率计算，选择 nprocs = 4 或 8 乘以 6\*原子数 是有意义的。
对于较大体系的 VPT2，如果每个位移使用多个进程，
你甚至完全可以尝试 16 乘以 6\*原子数——
（关于这类计算需要注意什么，请查看 {ref}`sec:essentialelements.parallel.hints` 一节。）


:::{note}
并行化是一项艰巨的任务，而且有许多
不同的协议，它们在不同机器上的表现各不相同。
请理解我们无法为每一个
平台都提供支持。我们正在尽力使并行化
保持透明，并为各种平台提供可执行文件，但我们
不能保证它们在每个系统上都能正常工作。有关版本的详细信息，
请参阅下载信息。
:::


(sec:essentialelements.parallel.hints)=
## 并行 ORCA 使用提示（Hints on the Use of Parallel ORCA）

讨论论坛中提出的许多问题都涉及
并行版 ORCA。请理解我们不可能为世界上的每一台并行计算机
提供一对一的支持。因此，
请尽一切努力与你的系统管理员一起在本地
解决技术问题。以下是一些关于并行版
有何特殊之处、可能因此产生哪些问题以及如何应对的说明：


(sec:essentialelements.parallel.hints.singlenode)=
### 单节点运行（Single Node Runs）

1. 并行 ORCA 只能与 OpenMPI（在 Linux 和 Mac 上）或 MS-MPI
   （在 Windows 上）一起使用。有关适用于你的平台的
   OpenMPI 版本的详细信息，请参阅下载信息。

   OpenMPI 版本可以通过多种方式配置，
   这里无法一一涵盖。关于所有
   可用选项的更详细说明，参见 <http://www.open-mpi.org>

2. 请注意，OpenMPI 版本是动态链接的，也就是说，
   它在运行时需要 OpenMPI 库（以及其他若干标准
   库）！如果你在自己的计算机上编译 MPI，你还需要一个
   Fortran 编译器，因为 `mpirun` 会包含 Fortran 绑定。

   （记得把 `PATH` 和 `LD_LIBRARY_PATH` 设置为 mpirun 和 mpi 库的路径）

3. 许多问题的产生是因为 ORCA 找不到其并行
   可执行文件。为避免这一点，关键是用
   完整路径名调用 ORCA。最简单也最安全的方式是把
   包含 ORCA 可执行文件的目录加入你的 `$PATH`。然后启动
   计算：
   ```sh
   - interactively: 
     start orca with full path: "/mypath_orca_executables/orca MyMol.inp"
   - batch : 
     set your path: `export PATH=/mypath_orca_executables:$PATH` (for bash) then 
     start orca with full path: "$PATH/orca $jobname.inp"
   ```
   这看起来是多余的，但如果你要运行
   并行计算，用完整路径调用 ORCA 真的很重要！否则它将
   无法找到并行可执行文件。

4. 建议在本地（非 NFS 挂载的）
   scratch 目录中运行 orca（例如 `/tmp1` 或 `/usr/local`），并且
   每次运行都重新创建这些目录，以避免与上次运行的
   残留文件混淆。

5. 实践证明，使用"包装"（wrapper）脚本很方便。这些脚本应当

   ```orca
   - set the path
   - create local scratch directories
   - copy input files to the scratch directory
   - start orca
   - save your results
   - remove the scratch directory
   ```
   
   并行 ORCA
   版本的此类提交脚本的基本示例在后面（13.）给出（这是用于 Torque/PBS 排队系统，
   运行在 Apple Mac OS X 上）：

6. 并行 ORCA 区分以下几种磁盘可用情况：

   1. 每个进程使用自己的（私有的）scratch 目录
      （该目录上的数据无法被任何其他进程看到）。
      这由 **"working on local scratch directories"** 标示
   2. 所有进程在一个公共 scratch 目录中工作（所有进程都能
      看到所有文件数据）。ORCA 会区分两种情况：
      * 所有进程在同一节点上——由 **"working on a common directory"** 标示
      * 进程分布在多个节点上，
        但访问共享文件系统——由 **"working on a shared directory"** 标示
   3. 至少有 2 组进程位于不同的 scratch
      目录上，其中一组由多于 1 个进程组成——
      由 **"working on distributed directories"** 标示

   并行 ORCA 会查明存在哪种情况，并据此
   处理 I/O。如果 ORCA 声明的磁盘可用情况与你
   预期的不同，请检查可用节点的数量和/或
   分配模式（fill_up/round_robin）

7. 可以通过在 ORCA 调用中加入这些参数来把额外的 MPI 参数传递给 mpirun——所有参数都括在一对引号内：

   ```sh
   /mypath_orca_executables/orca MyMol.inp "--bind-to none"
   ```
   -- 或 -- 对于多个参数
   ```sh
   /mypath_orca_executables/orca MyMol.inp "--bind-to none --verbose"
   ```

(sec:essentialelements.parallel.hints.multiplenodes)=
### 多节点运行——远程执行（Multi-Node Runs - Remote Execution）

1. 如果并行 ORCA 在其运行的目录中发现名为 "`MyMol.nodes`" 的文件，
   只要你的输入文件是 "`MyMol.inp`"，它就会使用此文件中列出的节点来
   启动进程。你可以把这个文件当作指定节点的机器文件，
   使用通常的 OpenMPI machinefile 记法。

   ```orca
   node1 cpu=2
   node2 cpu=2
   ```
   或
   ```orca
   node1
   node1
   node2
   node2
   ```

   如果你只在一台计算机上运行并行 ORCA 版本，则不需要提供节点文件，
   也不必启用 rsh/ssh 访问，因为在这种情况下进程
   只是被 fork 出来！如果你在排队系统中启动 ORCA，
   同样不需要提供节点文件。排队系统会处理此事。

2. 如果 ORCA 环境变量在所有
   参与的计算节点上定义不一致，导出这些变量可能是明智的。
   这可以通过在 ORCA 调用中向 mpirun
   传递以下附加参数来实现：

   ```sh
   /mypath_orca_executables/orca MyMol.inp "-x LD_LIBRARY_PATH -x PATH"
    ```

3. OpenMPI 要求设置 PATH 环境变量以便在远程节点上找到可执行文件。
    由于并不总是能相应地更改启动脚本，OpenMPI 提供了附加选项："`--prefix`"
    调用 ORCA 并为并行化模块请求多个进程时，应如下所示
    ```
    /mypath_orca_executables/orca MyMol.inp "--prefix /my-openmpi-folder"
    /mypath_orca_executables/orca MyMol.inp "--prefix /my-openmpi-folder --machinefile MyMol.nodes" (if not started via queueing system)
    ```
    由于 ORCA 是动态链接的，它还需要知道 ORCA 库的位置。
    这可以通过以下方式告知
    ```
    /mypath_orca_executables/orca MyMol.inp "--prefix /my-openmpi-folder --machinefile MyMol.nodes -x LD_LIBRARY_PATH"
    ```

(sec:essentialelements.parallel.hints.multiprocess)=
### 多进程计算（Multi-Process Calculations）

1. 关于多进程数值计算（频率、梯度、（混合）Hessian）、VPT2、NEB、GOAT 的补充说明：\
    执行这些计算的进程不是并行工作的，而是独立工作，往往以
    完全异步的方式。这些数值计算将启动
    与你先前为并行部分指定的进程数一样多的进程，并且
    它们将在相同的节点上运行。如果你的计算在多个节点上运行，
    你必须把环境变量 `RSH_COMMAND` 设为 "`rsh`" 或 "`ssh`"。
    如果未定义 `RSH_COMMAND`，ORCA 将中止。这可防止多节点运行的所有进程
    都在"主"节点上启动。

2. 应多个用户的要求，NumCalc 的"并行化"已变得更灵活。
    如果以前 ORCA 会用单个进程启动 nprocs 个位移，
    用户现在可以决定应有多少进程共同处理一个位移。

    为此，nprocs 关键词有了一个兄弟选项：

    ```orca
    %pal nprocs       32 # or nprocs_world - total number of parallel processes
         nprocs_group  4 #                 - number of parallel processes per sub-task
         end
    ```

    这一设置将使 ORCA 使用 32 个进程，其中 4 个进程处理同一位移，
    从而同时运行 8 个位移。
    可以从这一新功能中受益的方法有
    - 所有 NumCalc 方法：即 NumGrad、NumFreq、VPT2、Overtones、NEB 和 GOAT。
    - 解析（并行）Hessian，这对非常大的计算能带来可观的并行性能提升。

    强烈建议选择 nprocs_group 为 nprocs_world 的整数因子！

    为方便使用，一些标准的"分组"可以通过简单输入关键词获得：
    ```orca
    !PAL4(2x2)  # 2 groups a 2 workers
    !PAL8(4x2)  # 4 groups a 2 workers
    !PAL8(2x4)  # ...
    !PAL16(4x4)
    !PAL32(8x4)
    !PAL32(4x8)
    !PAL64(8x8)
    ```
    :::{tip}
    从 v1.8 系列开始，mpirun 会自动绑定进程。
    对于 NumCalc，这可能导致所有位移都在同一组核心上运行，从而造成严重的性能下降。
    有几种不同的解决方法：

    - 你可以通过向 ORCA 传递 `bind-to none` 作为附加 MPI 参数来关闭此行为。
    - 或者你可以通过环境设置禁用绑定：`OMPI_MCA_hwloc_base_binding_policy none`
    - 最有效的解决方案是使用资源管理器（如 SLURM、PBS 或其他）并确保 Open MPI 是为支持它而构建的。
    这些资源管理器将确保每个作业都在不同的核心组上运行。
    这样，你既能享受绑定的好处，又不会遇到多个计算跑在相同核心上的问题。
    :::

    :::{note}
    如果你的系统管理不允许通过 rsh/ssh 连接到其他计算节点，那么很遗憾，你无法在 NumCalc 运行中使用并行子计算。
    这既影响 NEB，也影响 GOAT、VPT2、倍频与组合频以及数值频率和梯度。
    :::


4. 启动 ORCA 的包装脚本
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
