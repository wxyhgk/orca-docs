```{index} Compound
```

(sec:workflowsautomatization.compound)=
# Compound

Compound is a form of sophisticated scripting language that can
be used directly in the input of ORCA. Using '*Compound*' the user can
combine various parts of a normal ORCA calculation to evaluate custom
functions of his own. In order to explain its usage, we will use an
example. For a more detailed description of this module the user is
referred to section
{ref}`sec:workflowsautomatization.compound_detailed`.

(sec:workflowsautomatization.compound.umbrella_example)=
## example

As a typical example we will use the constrained optimization describing
the \"umbrella effect\" of $NH_3$. The script will perform a series of
calculations and in the end it will print the potential of the movement
plus it will identify the minima and the maximum. The corresponding
compound script is the one shown below.

```{literalinclude} ../../orca_working_input/compTypicalExampleUmbrella.cmp
:language: orca
```

Let's start with how somebody can execute this input. In order to run
it, the easiest way is to save it in a normal text file, using the name
\"umbrella.cmp\" and then use the following ORCA input file:

```orca
%Compound "umbrella.cmp"
```

nothing more is needed. ORCA will read the compound file and act
appropriately.

A few notes about this ORCA input. First, there is no simple input line,
(starting with *\"!\"*). A simple input is not required when one uses
the *Compound* feature, but In case the user adds a simple input, all
the information from the simple input will be passed to the actual
compound jobs.

In addition, if one does not want to create a separate compound text
file, it is perfecly possible in ORCA to use the compound feature as any
other ORCA block. This means that after the *%Compound* directive,
instead of giving the filename one can append the contents of the
Compound file.

As we will see, inside the compound script file each compound job can
contain all information of a normal ORCA input file. There are two very
important exceptions here: The number of processors and the *MaxCore*.
These information should be set in the initial ORCA input file and not
in the actual compound files.

The Compound block has the same structure like all ORCA blocks. It
starts with a *\"%\"* and ends with *\"End\"*, if the input is not read
from a file. In case the compound directives are in a file, as in the
example above, then simply the filename inside brackets is needed and no
final *END*.

(sec:workflowsautomatization.compound.umbrella_defining_variables)=
## Defining variables

As we pointed out already, it is possible to either give all the
information for the calculations and the manipulation of the data inside
the Compound block or create a normal text file with all the details and
let ORCA read it. The latter option has the advantage that one can use
the same file with more than one geometries. In the previous example we
refer ORCA to an external file. The file *\"umbrella.cmp\"*, that
contains all necessary information.

Let's try to analyse now the Compound *\"umbrella.cmp\"* file.

```orca
# ----------------------------------------------
# Umbrella coordinate mapping for NH3
# Author: Frank Neese
# ----------------------------------------------
variable JobName = "NH3-umbrella";
variable amin    = 50.0;
variable amax    = 130.0;
variable nsteps  = 21;
Variable energies[21];

Variable angle;
Variable JobStep;
Variable JobStep_m;
variable step;

Variable method = "BP86";
Variable basis  = "def2-SVP def2/J";

step  = 1.0*(amax-amin)/(nsteps-1);
```

The first part contains some general comments and variable definitions.
For the comments we use the same syntax as in the normal ORCA input,
through the *\"#\"* symbol. Plase not that more than one *\"#\"* symbols in the same line cause an error. 

After the initial comments we see some
declarations and definitions. There are many different ways to declare
variables described in detail in section
{ref}`sec:workflowsautomatization.compound_detailed.commands.variables.general`.

All variable declarations begin with the directive *Variable* which is a
sign for the program to expect the declaration of one or more new
variables. Then there are many options, including defining more than one
variable, assigning also a value to the variable or using a list of
values. Nevertheless all declarations **MUST** finish with the *;*
symbol. This symbol is a message to the program that this is the end of
the current command. The need of the *;* symbol in the end of each
command is a general requirement in *Compound* and there are only very
few exceptions to it.

(sec:workflowsautomatization.compound.umbrella_running)=
## Running calculations

```orca
# Loop over the number of steps
# ----------------------------
for iang from 0 to nsteps-1 do
  angle    = amin + iang*step;
  JobStep  = iang+1;
  JobStep_m= JobStep-1;
  if (iang>0) then
    Read_Geom(JobStep_m);
    New_step
      ! &{method} &{basis} TightSCF Opt
      %base "&{JobName}.step&{JobStep}"
      %geom
        constraints
          {A 1 0 2 &{angle} C}
          {A 1 0 3 &{angle} C}
          {A 1 0 4 &{angle} C}
        end
      end
    Step_End
  else
    New_step
      ! &{method} &{basis} TightSCF Opt
      %base "&{JobName}.step&{JobStep}"  
      %geom
        constraints
          {A 1 0 2 &{angle} C}
          {A 1 0 3 &{angle} C}
          {A 1 0 4 &{angle} C}
        end
      end
      * int 0 1
        N 0 0 0 0.0 0.0 0.0
        DA 1 0 0 2.0 0.0 0.0
        H 1 2 0 1.06 &{angle} 0.0
        H 1 2 3 1.06 &{angle} 120.0
        H 1 2 3 1.06 &{angle} 240.0
      *
    Step_End
  endif
  Read energies[iang] = SCF_ENERGY[jobStep];
  print(" index: %3d Angle %6.2lf Energy: %16.12lf Eh\textbackslash{}n", iang, angle, energies[iang]);
EndFor
```

Then we have the most information dense part. We start with the
definition of a *for* loop. The syntax in compound for *for* loops is:

**For** *variable* **From** *startValue* **To** *endValue* **Do**\
&nbsp; *directives*\
**EndFor**

As we can see in the example above, the *startValue* and *endValue* can
be constant numbers or previously defined variables, or even functions
of these variables. Keep in mind that they have to be integers. The
signal that the loop has reached it's end is the *EndFor* directive. For
more details with regard to the *for* loops please refer to section
{ref}`sec:workflowsautomatization.compound_detailed.commands.for`.

Then we proceed to assign some variables.


```orca
angle     = amin + iang*step;
JobStep   = iang+1;
JobStep_m = JobStep-1;
```

The syntax of the variable assignement is like in every programming
language with a variable, followed with the *=* symbol and then the
value or an equation. Please keep in mind, that the assignement **must** always finish with the *;* symbol.

The next step is another significant part of every programming language,
namely the *if* block. The syntax of the *if* block is the following:

**if** (*expression to evaluate* **) Then**\
&nbsp; *directives*\
**else if (** *expression to evaluate* **) Then**\
&nbsp; *directives*\
**else**\
&nbsp; *directives*\
**EndIf**

The *else if* and *else* parts of the block are optional but the final
*EndIf* must always signal the end of the *if* block. For more details
concerning the usage of the *if* block please refer to section
{ref}`sec:workflowsautomatization.compound_detailed.commands.if` of the manual.

Next we have a command which is specific for compound and not a part of
a normal programming language. This is the *ReadGeom* command. It's
syntax is:

**Read_Geom**(*integer value*);

Before explaining this command we will proceed with the next one
in the compound script and return for this one.

The next command is the basis of all compound scripts. This is the
*New_Step* Command. This command signals compound that a normal ORCA
calculation follows. It's syntax is:

**New_Command**
&nbsp; *Normal ORCA input*
**Step_End**

Some comments about the *New_Step* command. Firstly, inside the
*New_Step* - *Step_End* commands one can add all possilbe commands that
a normal ORCA input accepts. We should remember here that the commands
that define the number of processors and the *MaxCore* command will be
ignored.

A second point to keep in mind is the idea of the *step*. Every
*New_Step - Step_End* structure corresponds to a step, starting counting
from 1 (The first ORCA calculation). This helps us define the property
file that this calculation will create, so that we can use it to
retrieve information from it.

A singificant feature in the *New_Step - Step_End* block. is the usage of the structure
**&{***variable***}** . This structure allows the user to use variables
that are defined outside the *New_Step - Step_End* block inside it,
making the ORCA input more generic. For example, in the script given
above, we build the *basename* of the calculations

```orca
  %base "&{JobName}.step&{JobStep}"
```

using the defined variables *JobName* and *JobStep*. For more details
regarding the usage of the **&{}** structure please refer to section
{ref}`sec:workflowsautomatization.compound_detailed.commands.ampersand`
while for the *New_Step - Step_End* structure please refer to the section
{ref}`sec:workflowsautomatization.compound_detailed.commands.newstep`.

Finally, a few comments about the geometries of the calculation. There
are 3 ways to provide a geometry to a *New_Step - Step_End* calculation.
The first one is the traditional ORCA input way, where we can give the
coordinates or the name of a file with coordinates, like we do in all
ORCA inputs. In *Compound* though, if we do not pass any information
concerning the geometry of the calculation, then *Compound* will
automatically try to read the geometry of the previous calculation. This
is the second (implicit) way to give a geometry to a compound Step. Then
there is a third way and this is the one we used in the example above.
This is the **Read_Geom** command. The syntat of this command is:\
**Read_Geom** (*Step number*);\
We can use this command when we want to pass a specific geometry to a
calculation that is not explicitly given inside the *New_Step -
Step_End* structure and it is also not the one from the previous step.
Then we just pass the number of the step of the calculation we are
interesting in just before we run our new calculation. For more details
regarding the *Read_Geom* command please refer to section
{ref}`sec:workflowsautomatization.compound_detailed.commands.read_geom`.

(sec:workflowsautomatization.compound.umbrella_data_manipulation)=
## Data manipulation

One of the most powerfull features of *Compound* is it's direct access
to properties of the calculation. In order to use these properties we
defined the *Read* command. In the previous example we use it to read
the SCF energy of the calculation:

```orca
Read energies[iang] = SCF\_ENERGY[jobStep];
```

The syntax of the command is:

**Read** *variable name* **=** *property* 

where *variable name* is the name of a variable that is already defined, *property* is the property from the known
properties found in table {ref}`sec:workflowsautomatization.compound_detailed.knownProperties` and *step* is
the step of the calculation we are interested in. For more details in the *Read* command please refer to
the corresponding section.


```orca
# Print a summary at the end of the calculation
  # ---------------------------------------------
  print("////////////////////////////////////////////////////////\\n");
  print("// POTENTIAL ENERGY RESULT\\n");
  print("////////////////////////////////////////////////////////\\n");
  variable minimum,maximum;
  variable Em,E0,Ep;
  variable i0,im,ip;
  for iang from 0 to nsteps-1 do
    angle   = amin + 1.0*iang*step;
    JobStep = iang+1;
    minimum = 0;
    maximum = 0;
    i0      = iang;
    im      = iang-1;
    ip      = iang+1;
    E0      = energies[i0];
    Em      = E0;
    Ep      = E0;
    if (iang>0 and iang<nsteps-1) then
      Em = energies[im];
      Ep = energies[ip];
    endif
    if (E0<Em and E0<Ep) then minimum=1; endif
    if (E0>Em and E0>Ep) then maximum=1; endif
    if (minimum = 1 ) then
      print(" %3d  %6.2lf %16.12lf (-)\textbackslash{}n",JobStep,angle, E0 );
    endif
    if (maximum = 1 ) then
      print(" %3d  %6.2lf %16.12lf (+)\textbackslash{}n",JobStep,angle, E0 );
    endif
    if (minimum=0 and maximum=0) then
      print(" %3d  %6.2lf %16.12lf    \textbackslash{}n",JobStep,angle, E0 );
    endif
  endfor
  print("////////////////////////////////////////////////////////\\n");
```

Once all data are available we can use them in equations like in any
programming language.

The syntax of the print statement is:

**print(** *format string, \[variables\]***);**

For example in the previous script we use it like:

```orca
print(" %3d  %6.2lf %16.12lf  \n",JobStep,angle, E0 );
```

where *%3d, %6.2lf* and *%16.2lf* are format identifiers and *JobStep,
angle* and *E0* are previously defined variables. The syntax follows
closely the widely accepted syntax of the *printf* command in the
programming language C. For more details regarding the *print*
statememnt please refer to section:
{ref}`sec:workflowsautomatization.compound_detailed.commands.stringrelated.print`.

Similar to the *print* command are the *write2file* and *write2string*
commands that are used to write instead of the output file, either to a
file we choose or to produce a new string.

Finally it is really importnat not to forget that every compound file
should finish with a final **End**.

Once we run the previous example we get the following output:

```orca
////////////////////////////////////////////////////////
// POTENTIAL ENERGY RESULT
////////////////////////////////////////////////////////
1   50.00 -56.486626696200    
2   54.00 -56.498074637200    
3   58.00 -56.505200120800    
4   62.00 -56.508823168800    
5   66.00 -56.509732863600 (-)
6   70.00 -56.508724734300    
7   74.00 -56.506590613800    
8   78.00 -56.504070086000    
9   82.00 -56.501791816800    
10   86.00 -56.500229017900    
11   90.00 -56.499674856600 (+)
12   94.00 -56.500229018100    
13   98.00 -56.501791817200    
14  102.00 -56.504070082800    
15  106.00 -56.506590613300    
16  110.00 -56.508724733100    
17  114.00 -56.509732863700 (-)
18  118.00 -56.508823172900    
19  122.00 -56.505200132200    
20  126.00 -56.498074642900    
21  130.00 -56.486626729200    
////////////////////////////////////////////////////////
```

with the step, the angle for the corresponding step, the energy of the
constrained optimized energy plus the symbols for the two minima and the
maximum in the potential.

