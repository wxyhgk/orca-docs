

<a id="sec:installation"></a>
# Installation
## Download

ORCA is available for Linux, MacOS, and Windows. Respective installers can be downloaded from the [ORCA forum](https://orcaforum.kofo.mpg.de/app.php/dlext/) (registration required).

## Installation

On Linux and MacOS the most convenient way to install ORCA is by using
the command-line installer. You have to download a .run file, e.g.
`orca_6_1_0_linux_x86-64_shared_openmpi416.run`.
Then make the file executable, that is, open a terminal, enter
the directory in which you stored the file and enter:

`chmod a+x orca_6_1_0_linux_x86-64_shared_openmpi416.run`

Afterwards you can simple execute the file, like

`./orca_6_1_0_linux_x86-64_shared_openmpi416.run`

The installer will install orca in a user directory, as well as set
the path to include the orca directory. After *opening a new
window* ORCA can be used as indicated.

The installer has a few more options, like extract-only, setting the path
interactively, and setting the path by option:

```
  -i        : Set a different install path interactively
  -p <path> : Set a different install path
  -x        : Just extract
```

The options have to be given *after* a double dash, e. g.

`./orca_6_1_0_linux_x86-64_shared_openmpi416.run -- -p /my/home/orca/dir`

On Window the installer is contained in a zip file `Orca6.1.0.Win64.zip` that must be unzipped before you can start the installation.
Than double-click `Orca6.1.0.Win64.exe` and follow the instructions. If you choose a `typical` installation only the serial modules of ORCA are copied. 
To also install the parallel part of ORCA please use `Custom` or `Full` installation.
The ORCA default directory is `C:\Orca_6.1.0` but you can choose a different folder if necessary.
The required environment variables will be set accordingly.

Additionally the ORCA AUTOCI executables are provided in 2 different files. `Orca6.1.0.Win64_autoci.zip` contains the modules for serial execution and `Orca6.1.0.Win64_autoci_msmpi10.zip` for the parallel execution.
Please extract the zip-files into the ORCA installation directory.

After opening a new command window ORCA can be used as indicated.

!!! note
    The ORCA main modules can be uninstalled via the `Apps & features` function of Windows but the ORCA AUTOCI modules have to be deleted manually.

## Path Variables

Only necessary environment variables are added or modified during the ORCA installation.

On Linux:
```
PATH	   : updated with the new orca installation directory
```

On Windows:

```
  PATH	   : modified with the new orca installation directory`
  ORCADIR  : created or modified with the new orca installation directory`
  XTBEXE   : created or replaced with the xtb module path`
```

!!! note
    Please be aware that the changes of environment variables only effect newly opened command windows.

## How do I install the xtb module?

Many feature of ORCA are connected to the xtb module. While
there is a native ORCA implementation, the package of the Grimme lab
is also integrated into the ORCA workflow, so installing it is advisable.
Since ORCA 6 on Linux and Windows the xtb version 7.6.1 is provided with the installation of ORCA.
The executable can be found in the orca installation directory (Linux) or in a sub-directory of the orca directory (Windows).

For updates or other xtb versions please download the reqiured xtb version from the Grimme lab's
repository [Grimme lab's repository](https://github.com/grimme-lab/xtb/releases/tag/)
and copy the xtb binary into the orca directory and rename it to `otool_xtb` for Linux.
On Windows you have to set the XTBEXE variable to point to the xtb executable itself. 
```
  set XTBEXE=<path>xtb.exe
```

