<a id="sec:workflowsautomatization.compound_detailed"></a>
# More Details on Compound
In this part we describe "Compound" in more detail. 
## Commands

Below is a list of all available commands available in *Compound*

**--------------------------------- Dataset Related --------------------------------**

-   Dataset([dataset.declaration](#sec:workflowsautomatization.compound_detailed.commands.dataset.declaration))

-   MakeReferenceFromDir([dataset.makeReferenceFromDir](#sec:workflowsautomatization.compound_detailed.commands.dataset.makeReferenceFromDir))
    
-   Print([dataset.print](#sec:workflowsautomatization.compound_detailed.commands.dataset.print))

**------------------------------ File Handling Related -----------------------------**
-   CloseFile
    ([commands.closeFile](#sec:workflowsautomatization.compound_detailed.commands.closeFile))

-   OpenFile
    ([commands.openFile](#sec:workflowsautomatization.compound_detailed.commands.openFile))

**------------------------------- *For* Loop Related -------------------------------**
-   Break
    ([commands.break](#sec:workflowsautomatization.compound_detailed.commands.break))

-   Continue
    ([commands.continue](#sec:workflowsautomatization.compound_detailed.commands.continue))

-   EndFor
    ([commands.endfor](#sec:workflowsautomatization.compound_detailed.commands.endfor))

-   For
    ([commands.for](#sec:workflowsautomatization.compound_detailed.commands.for))

**-------------------------------- Geometry Related -------------------------------**

-   Geometry([commands.geometry](#sec:workflowsautomatization.compound_detailed.commands.geometry))

-   BohrToAngs([geometry.BohrToAngs](#sec:workflowsautomatization.compound_detailed.commands.geometry.BohrToAngs))
   
-   CreateBSSE([geometry.createBSSE](#sec:workflowsautomatization.compound_detailed.commands.geometry.createBSSE))

-   CreateFragments([geometry.createFragments](#sec:workflowsautomatization.compound_detailed.commands.geometry.createFragments))
  
-   DisplaceAtom([geometry.displaceAtom](#sec:workflowsautomatization.compound_detailed.commands.geometry.displaceAtom))
  
-   FollowNormalMode([geometry.followNormalMode](#sec:workflowsautomatization.compound_detailed.commands.geometry.followNormalMode))
     
-   GetAngle([geometry.getAngle](#sec:workflowsautomatization.compound_detailed.commands.geometry.getAngle))
   
-   GetAtomicNumbers([geometry.getAtomicNumbers](#sec:workflowsautomatization.compound_detailed.commands.geometry.getAtomicNumbers))

-   GetBondDistance([geometry.getBondDistance](#sec:workflowsautomatization.compound_detailed.commands.geometry.getBondDistance))
  
-   GetCartesians([geometry.getCartesians](#sec:workflowsautomatization.compound_detailed.commands.geometry.getCartesians))

-   GetGhostAtoms([geometry.getGhostAtoms](#sec:workflowsautomatization.compound_detailed.commands.geometry.getGhostAtoms))   
   
-   GetNumOfAtoms([geometry.getNumOfAtoms](#sec:workflowsautomatization.compound_detailed.commands.geometry.getNumOfAtoms))

-   MoveAtomToCenter([geometry.moveAtomToCenter](#sec:workflowsautomatization.compound_detailed.commands.geometry.moveAtomToCenter))   
   
-   Read([geometry.read](#sec:workflowsautomatization.compound_detailed.commands.geometry.read))

-   RemoveAtoms([geometry.removeAtoms](#sec:workflowsautomatization.compound_detailed.commands.geometry.removeAtoms))
   
-   RemoveElements([geometry.removeElements](#sec:workflowsautomatization.compound_detailed.commands.geometry.removeElements))
      
-   WriteXYZFile([geometry.writeXYZFile](#sec:workflowsautomatization.compound_detailed.commands.geometry.writeXYZFile))

**--------------------------------   GΟΑΤ Related  -------------------------------**

-   GOAT([commands.goat](#sec:workflowsautomatization.compound_detailed.commands.goat))

-   Get_Energy ([goat.getEnergy](#sec:workflowsautomatization.compound_detailed.commands.goat.getEnergy))
  
-   Get_Num_Of_Geometries ([goat.getNumOfGeometries](#sec:workflowsautomatization.compound_detailed.commands.goat.getNumOfGeometries))
  
-   ParseEensembleFfile ([goat.parseEnsembleFile](#sec:workflowsautomatization.compound_detailed.commands.goat.parseEnsembleFile))
    
-   Set_Basename ([goat.setBasename](#sec:workflowsautomatization.compound_detailed.commands.goat.setBasename))

-   Print ([goat.print](#sec:workflowsautomatization.compound_detailed.commands.goat.print))
  
-   WriteXYZFile ([goat.writeXYZFile](#sec:workflowsautomatization.compound_detailed.commands.goat.writeXYZFile))  

**------------------------------ *If* block Related ------------------------------**

-   If
    ([commands.if](#sec:workflowsautomatization.compound_detailed.commands.if))

**---------------------------- Linear Algebra Related ----------------------------**

-   Diagonalize([linAlgegra.diagonalize](#sec:workflowsautomatization.compound_detailed.commands.linAlgegra.diagonalize))

-   InvertMatrix([linAlgegra.invertMatrix](#sec:workflowsautomatization.compound_detailed.commands.linAlgegra.invertMatrix))  
 
-   Mat_p_Mat([linAlgegra.Mat_p_Mat](#sec:workflowsautomatization.compound_detailed.commands.linAlgegra.Mat_p_Mat))     
   
-   Mat_x_Mat([linAlgegra.Mat_x_Mat](#sec:workflowsautomatization.compound_detailed.commands.linAlgegra.Mat_x_Mat))  

-   Mat_x_Scal([linAlgegra.Mat_x_Scal](#sec:workflowsautomatization.compound_detailed.commands.linAlgegra.Mat_x_Scal)) 

**--------------------------- ORCA calculation Related ---------------------------**

-   Basenames([orca.basenames](#sec:workflowsautomatization.compound_detailed.commands.orca.basenames))

-   ReadMOs([orca.readMOs](#sec:workflowsautomatization.compound_detailed.commands.orca.readMOs)) 

**----------------------------- Program flow Related -----------------------------**

-   Abort
    ([commands.abort](#sec:workflowsautomatization.compound_detailed.commands.abort))

-   End
    ([commands.end](#sec:workflowsautomatization.compound_detailed.commands.end))

-   EndRun
    ([commands.endrun](#sec:workflowsautomatization.compound_detailed.commands.endrun))

-   GoTo
    ([commands.goto](#sec:workflowsautomatization.compound_detailed.commands.goto))

**--------------------------- Property File Related ----------------------------**

-   GetNumOfInstances([propertyFile.getNumOfInstances](#sec:workflowsautomatization.compound_detailed.commands.propertyFile.getNumOfInstances)) 
   
-   ReadProperty([propertyFile.readProperty](#sec:workflowsautomatization.compound_detailed.commands.propertyFile.readProperty)) 

**-------------------------- String Handling Related --------------------------**

-   GetBasename ([stringrelated.getBasename](#sec:workflowsautomatization.compound_detailed.commands.stringrelated.getBasename))

-   GetChar ([stringrelated.getChar](#sec:workflowsautomatization.compound_detailed.commands.stringrelated.getChar))
  
-   GetSuffix ([stringrelated.getSuffix](#sec:workflowsautomatization.compound_detailed.commands.stringrelated.getSuffix))
  
-   Print ([stringrelated.print](#sec:workflowsautomatization.compound_detailed.commands.stringrelated.print))
   
-   Write2File ([stringrelated.write2file](#sec:workflowsautomatization.compound_detailed.commands.stringrelated.write2file))
   
-   Write2String ([stringrelated.write2string](#sec:workflowsautomatization.compound_detailed.commands.stringrelated.write2string))

**--------------------------------- Step Related ---------------------------------**

-   &
    ([commands.ampersand](#sec:workflowsautomatization.compound_detailed.commands.ampersand))

-   Alias
    ([commands.alias](#sec:workflowsautomatization.compound_detailed.commands.alias))

**----------------------------- Timer Related ------------------------------------**

- Timer ([timerrelated.timer](#sec:workflowsautomatization.compound_detailed.commands.timerrelated.timer))

- Last ([timer.last](#sec:workflowsautomatization.compound_detailedd.commands.timer.last))

- Reset ([timer.reset](#sec:workflowsautomatization.compound_detailedd.commands.timer.reset))

- Start ([timer.start](#sec:workflowsautomatization.compound_detailedd.commands.timer.start))

- Stop ([timer.stop](#sec:workflowsautomatization.compound_detailedd.commands.timer.stop))

- Total ([timer.total](#sec:workflowsautomatization.compound_detailedd.commands.timer.total))

**--------------------------- Variables Related ----------------------------------**

-  Variables ([variables.general](#sec:workflowsautomatization.compound_detailed.commands.variables.general))

-  Variables - Assignment ([variables.assignement](#sec:workflowsautomatization.compound_detailed.commands.variables.assignement))

-  Variables - Declaration ([variables.declaration](#sec:workflowsautomatization.compound_detailed.commands.variables.declaration))

-  Variables - Functions ([variables.functions](#sec:workflowsautomatization.compound_detailed.commands.variables.functions))

-  Variable - With ([variables.with](#sec:workflowsautomatization.compound_detailed.commands.variables.with))

-  GetBool() [functions.getBool](#sec:workflowsautomatization.compound_detailed.commands.variables.functions.getBool) 

-  GetDim1() [functions.getDim1](#sec:workflowsautomatization.compound_detailed.commands.variables.functions.getDim1) 

-  GetDim2() [functions.getDim2](#sec:workflowsautomatization.compound_detailed.commands.variables.functions.getDim2) 

-  GetDouble() [functions.getDouble](#sec:workflowsautomatization.compound_detailed.commands.variables.functions.getDouble) 

-  GetInteger() [functions.getInteger](#sec:workflowsautomatization.compound_detailed.commands.variables.functions.getInteger) 

-  GetSize() [functions.getSize](#sec:workflowsautomatization.compound_detailed.commands.variables.functions.getSize) 

-  GetString() [functions.getString](#sec:workflowsautomatization.compound_detailed.commands.variables.functions.getString) 

-  PrintMatrix() [functions.printMatrix](#sec:workflowsautomatization.compound_detailed.commands.variables.functions.printMatrix) 

-  Write2File ([stringrelated.write2file](#sec:workflowsautomatization.compound_detailed.commands.stringrelated.write2file))

-  Write2String ([stringrelated.write2string](#sec:workflowsautomatization.compound_detailed.commands.stringrelated.write2string))

<a id="sec:workflowsautomatization.compound_detailed.commands.ampersand"></a>
### &

The *&* symbol has a special meaning in the compound block. Using this
symbol inside the *NewStep* - *StepEnd* block the user can use variables
that are defined outside the block. Both string and numerical variables
are allowed.

**Syntax:**

**&{*variable*}**

**Example**

```mol
title: structure 1
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
1
structure (0 1)
H           0.0          0.0          0.0
--- input ---
# --------------------------------------------
# This script checks the options for the 
#             '&' symbol
# --------------------------------------------
%Compound 

  Variable method   = "BP86";              #string variable'
  Variable basis    = "def2-TZVP def2/J";
  Variable name     = "base";
  Variable number   = 0;                   #integer variable
  Variable distance = 0.8;                 #double variable
  New_step
    ! &{method} &{basis} TightSCF
    %base "&{name}_&{number}"              #combination of variables
    *xyz 0 1
      H 0.0 0.0 0.0
      H 0.0 0.0 &{distance} 
    *
  Step_End
  # ------------------------------------------
  # Add some printing
  # ------------------------------------------
  print("SUMMARY OF VARIABLES\n");
  print("Method:   %s\n",    method);
  print("Basis:    %s\n",    basis);
  print("Name:     %s\n",    name);
  print("Number:   %d\n",    number);
  print("Distance: %.2lf\n", distance);
End
```

<a id="sec:workflowsautomatization.compound_detailed.commands.abort"></a>
### Abort
*Abort* is used when the user wants to exit the program instantly.
**Syntax:**\
Abort;\
**or alternatively:**\
Abort

**Example:**
```orca
%Compound
for i from 0 to 4 do
  print("i: %d\n", i);
  if (i=2) then 
    abort;
  endif
endfor
End
```

<a id="sec:workflowsautomatization.compound_detailed.commands.alias"></a>
### Alias

*Alias* is used to replace an integer number with a more representative string. It is useful when one performs more than one calculations and the step numbers become too complicated to evaluate. In this case
using Alias_Step after the Step_End command will connect the preceeding
calculation step number with the provided name.

**Syntax:**\
Alias $name$;\
**or alternatively:**\
Alias $name$\
**Example:**

```mol
title: structure 2
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
1
structure (0 1)
H           0.0          0.0          0.0
--- input ---
# ----------------------------------
# This script checks 'alias' keyword
# ----------------------------------
Variable numOfSteps = 20;
Variable Range      = 4.0;
Variable distStart  = 0.4;
Variable Step       = Range/numOfSteps;
Variable distance;
Variable Energies[numOfSteps];
Variable simpleInput  = "BP86 def2-SVP def2/J";

For index from 0 to numOfSteps-1 Do
  Distance =  distStart+ index*Step;
  New_Step
    !&{simpleInput} 
    *xyz 0 1
      H 0.0 0.0 0.0
      H 0.0 0.0 &{Distance}
    *
  Step_End
  Alias currStep;
  print("Current step: %d\n", currStep);
  Read Energies[index] = JOB_INFO_TOTAL_EN[currStep];
EndFor

print("--------------------------------------\n");
print("       Compound Printing              \n");
print("%s  %12s  %16s \n","Step",  "Distance", "Energy");
print("--------------------------------------\n");
For index from 0 to numOfSteps - 1 Do
  Distance = distStart + index*Step;
  print("%4d  %12.4lf   %16.8lf \n", index, Distance, Energies[index]);
EndFor

End
```
!!! note
    For the **Alias** command the final ';' is optional.

<a id="sec:workflowsautomatization.compound_detailed.commands.orca.basenames"></a>
### Basenames
*Basenames* in a variable that is automatically created in *Compound* everytime a *NewStep* is used and it holds the name of this step. It can be used to recover this name during running of a calculation. It practically is a vector were value zero corresponds to the main calculation before any *new_step* command.

**Example:**
```mol
title: structure 3
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
2
structure (0 1)
H           0.0          0.0          0.0
H           0.0          0.0          0.8
--- input ---
*xyz 0 1
  H 0.0 0.0 0.0
  H 0.0 0.0 0.8
*
%Compound
  new_step
    !BP86
  step_end
  alias lala;
  print("Basaenames[0]: %s\n", basenames[0]);
  print("Basaenames[1]: %s\n", basenames[lala]);
End
```

<a id="sec:workflowsautomatization.compound_detailed.commands.break"></a>
### Break
*Break* can be used inside a *For* loop (see (see [commands.for](#sec:workflowsautomatization.compound_detailed.commands.for))) when one needs to break the loop under certain conditions. The syntax is the following:

**Syntax:**\
*For* *variable* *From* *Start value* *To* *End value* *Do*\
*commands*\
**break ;**\
*commands*\
*EndFor;*

**NOTE** both versions *break* and *break;* are legal. 

What break actually does is to set the running index of the loop to the last allowed value and then jump
to the *EndFor* (see [commands.endfor](#sec:workflowsautomatization.compound_detailed.commands.endfor))).

**Example:**
```orca
#
# This a script to check Compound 'break' command
#
%Compound
print(" Test for 'break'\n");
print(" It should print 0, 1 and 2\n");
for i from 0 to 6 Do
  if (2*i > 4) then
    break
  endIF
  print("index: %d\n", i);
EndFor

print("Continued outside the 'for' loop\n");

End
```

<a id="sec:workflowsautomatization.compound_detailed.commands.closeFile"></a>
### CloseFile

When a file is opened in *Compound* using the *openFile* command (see [commands.openFile](#sec:workflowsautomatization.compound_detailed.commands.openFile)), then it must be closed using the *closeFile* command.

**Syntax:**\
*closeFile*(file);

*file* is the file pointer created from the *openFile* command. For an example see paragraph [commands.openFile](#sec:workflowsautomatization.compound_detailed.commands.openFile).

<a id="sec:workflowsautomatization.compound_detailed.commands.continue"></a>
### Continue
*Continue* can be used inside a *For* loop (see (see [commands.for](#sec:workflowsautomatization.compound_detailed.commands.for))) when one needs to skip the current step of the loop and proceed to the next one. The syntax is the following:

**Syntax:**\
*For* *variable* *From* *Start value* *To* *End value* *Do*\
*commands*\
**continue ;**\
*commands*\
*EndFor;*

**NOTE** both versions *continue* and *continue;* are legal. 

What continue actually does is to jump to the *EndFor* (see [commands.endfor](#sec:workflowsautomatization.compound_detailed.commands.endfor))).

**Example:**
```orca
# -----------------------------------------------------
# This is a script to check Compound 'continue' command
# ----------------------------------------------------
%Compound
print(" Test for 'continue'\n");
print(" It should print 0, 1, 2 and 4\n");
for i from 0 to 4 Do
  if ( i=3) then
    continue;
  endIf
  print("index: %d\n", i);
EndFor
End
```

<a id="sec:workflowsautomatization.compound_detailed.commands.dataset.declaration"></a>
### Dataset

In *Compound* we have *Dataset* objects. These objects can be treated like normal variables of type '*compDataset*'. An important difference between normal variables and *Dataset* variables is the declaration. Instead of the normal:
```orca
Variable x;
```
we excplicitly have to declare that this is a dataset. So the syntax for a dataset declaration is:

**Syntax:**
```orca
Dataset mySet;
```

**NOTE** in the case of datasets we do not allow multiple dataset declarations per line.

Below is a list of functions that work on *Dataset*. 

-   MakeReferenceFromDir([dataset.makeReferenceFromDir](#sec:workflowsautomatization.compound_detailed.commands.dataset.makeReferenceFromDir))
   
-   Print([dataset.print](#sec:workflowsautomatization.compound_detailed.commands.dataset.print))

**Example:**
```orca
Variable x;
```

<a id="sec:workflowsautomatization.compound_detailed.commands.dataset.makeReferenceFromDir"></a>
### D.MakeReferenceFromDir

*MakeReferenceFromDir* command acts on a dataset object (see [dataset.declaration](#sec:workflowsautomatization.compound_detailed.commands.dataset.declaration)). It creates a json reference file based on the *xyz files of the current folder. 
**NOTE** By default all charges and multplicities will be set to 0 and 1 respectively.

**Syntax:**\
*mySet.MakeReferenceFromDir(dirName);*

Where:

- *mySet* is a dataset object that is already declared

- *dirName* The name of a directory that should contain some xyz files. 

**Example:**
```orca
Dataset mySet;
```

<a id="sec:workflowsautomatization.compound_detailed.commands.dataset.print"></a>
### D.Print

*Print* command acts on a dataset object (see [dataset.declaration](#sec:workflowsautomatization.compound_detailed.commands.dataset.declaration)). It prints all details of the specific dataset object.

**Syntax:**\
*mySet.Print();*

Where:

- *mySet* is a dataset object that is already declared

**Example:**
```orca
# ----------------------------------------------------
# This is an example script for dataset definition
# -----------------------------------------------------
%Compound
  dataset mySet;
  mySet.Print();
End
```

<a id="sec:workflowsautomatization.compound_detailed.commands.linAlgegra.diagonalize"></a>
### Diagonalize
*Compound* can peform matrix algebraic operations, one of the available algebraic operation is matrix diagonalization. Be carefull that the matrix, that is to be diagonalized, **must be** a square symmetric matrix. It is also important to remember that only the upper triangle part of the matrix will be used for the diagonalization. If everything proceeds smoothly then the function will return the eigenvectors and eigenvalues of the matrix.

**Syntax:**\
*A.Diagonalize(eigenValues, eigenVectors);*

Where:

- *A:* The matrix to be diagonalized.
- *eigenValues:* The vector with the eigenvalues
- *eigenVectors:* The square matrix with the eigenvectros of the initial matrix.

**Example:**
```orca
%Compound
  # ------------------------------------
  #   This is a compound script that will 
  #   check dataset.MakeReferenceFromDir 
  #   function
  #   NOTE: The script assumes that some
  #         xyz files rest in the current
  #         directory
  # ------------------------------------

  # First some definitions
  Variable name = "mySet";
  Variable numOfMolecules = 0;
  dataset mySet;
  Variable myDir="./";
  mySet.MakeReferenceFromDir(myDir);
  mySet.ReadReferenceFile();
  mySet.Print();
End
```

<a id="sec:workflowsautomatization.compound_detailed.commands.end"></a>
### End
*End* is the final command each compound script must have (unless there  is an *EndRun* command (see [commands.endrun](#sec:workflowsautomatization.compound_detailed.commands.endrun))). After *Compound* executes what is written in the script then it passes control again to normal ORCA input reading. ORCA will continue analyze the input that rests after the *Compound* part but it will not run any calculation.

<a id="sec:workflowsautomatization.compound_detailed.commands.endrun"></a>
### EndRun
#EndRun* is an alternative to the *End* command (see [commands.endrun](#sec:workflowsautomatization.compound_detailed.commands.endrun)) for ending the execution of a *Compound* script. The difference between *end* and *EndRun* is that *EndRun* ignores everything after the *Compound* block. This makes it even easier to use *Compound* as a full workflow run.

<a id="sec:workflowsautomatization.compound_detailed.commands.endfor"></a>
### EndFor

All *For* loops (see [commands.for](#sec:workflowsautomatization.compound_detailed.commands.for)) must finish with *EndFor*. The syntax and an example is shown in the *For* section (see [commands.for](#sec:workflowsautomatization.compound_detailed.commands.for)).

**NOTE** For *EndFor* both *EndFor* and *EndFor;* are possible.

<a id="sec:workflowsautomatization.compound_detailed.commands.for"></a>
### For

*For* loops are used to perform repetitive tasks. The syntax is the
following:

**Syntax:**

**For** *variable* **From** *Start value* **To** *End value* **Do**

*commands*

**EndFor** or **EndFor;**

*Variable* should be a variable name not previously defined.
*Start value* and *End value* should be integers defining the start and end value of the *variable*. *Start value* and *End value* can be numbers, predefined variables or
functions of previously defined variables. The only requirement is that they should be **integers**. Keep in mind that the loop will be performed from the first value to the *End value*, including the *End value*.

**Example:**

```orca
# ----------------------------------------------------
# This is an example script for dataset definition
# -----------------------------------------------------
%Compound
  dataset mySet;
  mySet.Print();
End
```

<a id="sec:workflowsautomatization.compound_detailed.commands.geometry"></a>
### Geometry

In *Compound* we have *Geometry* objects. These objects can be treated like normal variables of type '*compGeometry*'. An important difference between normal variables and *Geometry* variables is the declaration. Instead of the normal:
```
Variable myGeom;
```
we excplicitly have to declare that this is a geometry. So the syntax for a geometry declaration is:

**Syntax:**
```
Geometry myGeom;

Geometry myGeom1, myGeom2;
```

Using the second definition one can define two geometry objects in the same line.

Below is a list of functions that work on *Geometry* objects. 

-   BohrToAngs([geometry.BohrToAngs](#sec:workflowsautomatization.compound_detailed.commands.geometry.BohrToAngs))
-   CreateBSSE ([geometry.createBSSE](#sec:workflowsautomatization.compound_detailed.commands.geometry.createBSSE))
-   CreateFragments([geometry.createFragments](#sec:workflowsautomatization.compound_detailed.commands.geometry.createFragments))
-   DisplaceAtom([geometry.displaceAtom](#sec:workflowsautomatization.compound_detailed.commands.geometry.displaceAtom))
-   FollowNormalMode ([geometry.followNormalMode](#sec:workflowsautomatization.compound_detailed.commands.geometry.followNormalMode))
-   GetAngle([geometry.getAngle](#sec:workflowsautomatization.compound_detailed.commands.geometry.getAngle))
-   GetAtomicNumbers([geometry.getAtomicNumbers](#sec:workflowsautomatization.compound_detailed.commands.geometry.getAtomicNumbers))
-   GetBondDistance([geometry.getBondDistance](#sec:workflowsautomatization.compound_detailed.commands.geometry.getBondDistance))
-   GetCartesians([geometry.getCartesians](#sec:workflowsautomatization.compound_detailed.commands.geometry.getCartesians))
-   GetGhostAtoms([geometry.getGhostAtoms](#sec:workflowsautomatization.compound_detailed.commands.geometry.getGhostAtoms))   
-   GetNumOfAtoms([geometry.getNumOfAtoms](#sec:workflowsautomatization.compound_detailed.commands.geometry.getNumOfAtoms))
-   MoveAtomToCenter([geometry.moveAtomToCenter](#sec:workflowsautomatization.compound_detailed.commands.geometry.moveAtomToCenter))
-   Read([geometry.read](#sec:workflowsautomatization.compound_detailed.commands.geometry.read))
-   RemoveAtoms([geometry.removeAtoms](#sec:workflowsautomatization.compound_detailed.commands.geometry.removeAtoms))
-   RemoveElements([geometry.removeElements](#sec:workflowsautomatization.compound_detailed.commands.geometry.removeElements))
-   WriteXYZFile([geometry.writeXYZFile](#sec:workflowsautomatization.compound_detailed.commands.geometry.writeXYZFile))
   
<a id="sec:workflowsautomatization.compound_detailed.commands.geometry.BohrToAngs"></a>
### G.BohrToAngs
*BohrToAngs* command acts on a geometry object (see see [commands.geometry](#sec:workflowsautomatization.compound_detailed.commands.geometry)). It will transform the geometry of the loaded geometry object from Bohr to Angstroms. Practically it will just multiply the coordinates with the 
factor *0.529177249*. 

**Syntax:**\
*myGeom.BohrToAngs();*

Where:

- *myGeom* is a geometry object that already contains a geometry

**Example:**
```orca
# ----------------------------------------------------
# This is an example script for diagonalization
# -----------------------------------------------------
%Compound
  Variable Dim=3;
  Variable A[Dim][Dim];
  Variable eigenVal;
  Variable eigenVec;
  for i from 0 to Dim-1 Do
    for j from 0 to Dim-1 Do
      if (i<=j) then
        A[i][j] = i+j+1;
      else
        A[i][j] =  A[j][i];
      EndIf
    EndFor
  EndFor
  A.Diagonalize(eigenVal, eigenVec);
  A.PrintMatrix(); 
  eigenVal.PrintMatrix();
  eigenVec.PrintMatrix();
End
```

<a id="sec:workflowsautomatization.compound_detailed.commands.geometry.createBSSE"></a>
### G.CreateBSSE

*CreateBSSE* command acts on a geometry object (see see [commands.geometry](#sec:workflowsautomatization.compound_detailed.commands.geometry)). In the case that the geometry object contains *ghost* atoms then *CreateBSSE* will create five new files:
- myFilename_FragmentA.xyz
- myFilename_MonomerA.xyz
- myFilename_FragmentB.xyz
- myFilename_MonomerB.xyz
- myFilename_Total.xyz

**Syntax:**\
*myGeom.CreateBSSE(filename=myFilename);*

Where:

- *myGeom* is a geometry object that already contains a geometry

- *filename* is a base filename for the created files.

**Example:**
```orca
# ---------------------------------------
# This is a script to check 'for' loops
# ---------------------------------------

# ---------------------------------
# Some necessary initial definitions
# ----------------------------------
Variable x = {0.0, 1.0, 2.0, 3.0, 4.0};
Variable f;
Variable loopStart;
Variable upLimit;

# -----------------------------------
# Case 1. 
# Constant Start / Constant End
# -----------------------------------
print(" --------------  Case 1 --------------\n");
print("     Constant Start / Constant End    \n");
print("          f = index*x[index]          \n");
print( "      for index from 0 to 4 Do     \n");
print(" -------------------------------------\n");
for index from 0 to 4 Do
  f = index*x[index];
  print("Index: %3d    x[index]:  %.2lf   f:   %.2lf\n", index, x[index], f); 
EndFor

loopStart = 0;
upLimit   = 4;
print(" --------------  Case 2 --------------\n");
print("     Variable Start / Variable End    \n");
print("          f = index*x[index]          \n");
print( "   for index from loopStart to upLimit Do\n");
print(" -------------------------------------\n");
for index from loopStart to upLimit Do
  f = index*x[index];
  print("Index: %3d    x[index]:  %.2lf   f:   %.2lf\n", index, x[index], f); 
EndFor

loopStart  = 1;
upLimit    = 3;
print(" --------------  Case 3 --------------    \n");
print("     function Start / function End        \n");
print("          f = index*x[index]              \n");
print( "   for index from start-1 to upLimit+1 Do\n");
print(" -------------------------------------    \n");
for index from loopStart-1 to upLimit+1 Do
  f = index*x[index];
  print("Index: %3d    x[index]:  %.2lf   f:   %.2lf\n", index, x[index], f);
EndFor

End
```

**NOTE** The files will contain XYZ geometries in **BOHRS**.

<a id="sec:workflowsautomatization.compound_detailed.commands.geometry.createFragments"></a>
### G.CreateFragments

*CreateBSSE* command acts on a geometry object (see see [commands.geometry](#sec:workflowsautomatization.compound_detailed.commands.geometry)). In the case that the geometry object contains *ghost* atoms then *CreateBSSE* will create five new files:
- myFilename_FragmentA.xyz
- myFilename_MonomerA.xyz
- myFilename_FragmentB.xyz
- myFilename_MonomerB.xyz
- myFilename_Total.xyz

**Syntax:**\
*myGeom.CreateBSSE(filename=myFilename);*

Where:

- *myGeom* is a geometry object that already contains a geometry

- *filename* is a base filename for the created files.

**Example:**
```orca
Variable myGeom;
```

**NOTE** The files will contain XYZ geometries in **BOHRS**.

<a id="sec:workflowsautomatization.compound_detailed.commands.geometry.followNormalMode"></a>
### G.FollowNormalMode

*FollowNormalMode* command acts on a geometry object (see see [commands.geometry](#sec:workflowsautomatization.compound_detailed.commands.geometry)). It will displace the loaded geometry following a chosen normal mode of vibtation

**Syntax:**\
*myGeom.FollowNormalMode(vibrationSN=myVibration, [ScalingFactor=myScalingFactor]);*

Where:

- *myGeom* is a geometry object that already contains a geometry

- *vibrationSN* is the serial number of the vibration.
**NOTE** Please remember that counting starts with 1.

- *scalingFactor* is the scaling of the normal mode of vibration. This argument is optional.

**Example:**
```orca
Geometry myGeom;

Geometry myGeom1, myGeom2;
```

<a id="sec:workflowsautomatization.compound_detailed.commands.geometry.displaceAtom"></a>
### G.DisplaceAtom
Function *DisplaceAtom* acts on geometry objects and moves the cartesian coordintates of a given atom of the current geometry. The displacement is in Bohrs.

**Syntax:**

*res = geom.DisplaceAtom(atomID, dx, dy, dz)*

Where:

*geom* A geometry object previously loaded.

*atomID* The index of the atom we want to move. Please note that counting starts with zero.

*dx* The displacement in the x axis in Bohrs.

*dy* The displacement in the y axis in Bohrs.

*dz* The displacement in the z axis in Bohrs.

**Example:**

```mol
title: structure 4
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
3
structure (0 1)
O   -1.69296787  -0.05579265   0.00556629
H   -2.01296504   0.84704339  -0.01586469
H   -0.73325076   0.04238910   0.00084302
--- input ---
# ----------------------------------------------------
# This is a script to check the BohrToAngs function
# -----------------------------------------------------
*xyz 0 1
  O      -1.69296787   -0.05579265    0.00556629
  H      -2.01296504    0.84704339   -0.01586469
  H      -0.73325076    0.04238910    0.00084302
*

%Compound
  Geometry myGeom;
  Variable CC;
  New_Step
    !BP86
  Step_End
  myGeom.Read();
  myGeom.BohrToAngs();
  CC = myGeom.GetCartesians();
  CC.PrintMatrix();
End
```

<a id="sec:workflowsautomatization.compound_detailed.commands.geometry.getAngle"></a>
### G.GetAngle
Function *GetAngle* acts on geometry objects and returns the angle between three atoms in **Degrees**.

**Syntax:**

*res = geom.GetAngle(atomA, atomB, atomC)*

Where:

*res* The angle between atoms atomA, atomB and atomC.

*geom* A geometry object previously loaded.

*atomA* The index of atomA in the geometry.

*atomB* The index of atomB in the geometry.

*atomC* The index of atomC in the geometry.

**NOTE** Please not that the ordering of atoms is important

**Example:**

```mol
title: structure 5
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
3
structure (0 1)
o    1.23009925   0.02698440  -0.00375550
h    1.60672086  -0.41139567   0.76236888
h    1.60236356  -0.44922858  -0.74915800
--- input ---
# --------------------------------------------------------
# This is a scrtipt to check the geom.CreateBSSE command
# -------------------------------------------------------

*xyz 0 1
o:      -1.69296787   -0.05579265    0.00556629
h:      -2.01296504    0.84704339   -0.01586469
h:      -0.73325076    0.04238910    0.00084302
o        1.23009925    0.02698440   -0.00375550
h        1.60672086   -0.41139567    0.76236888
h        1.60236356   -0.44922858   -0.74915800
*

%Compound
  Geometry monomerA;
  variable myFilename     = "BSSE";
  Variable method         = "BP86";

  # --------------------------------------
  # Calculation for Fragment A
  # --------------------------------------
  New_Step
    !&{method} 
  Step_End

  # -------------------------------------
  # Read the geometry of Fragment A
  # -------------------------------------
  monomerA.Read();

  # -------------------------------------
  # Create the missing xyz files
  # -------------------------------------
  monomerA.CreateBSSE(filename=myFilename);

End
```

<a id="sec:workflowsautomatization.compound_detailed.commands.geometry.getAtomicNumbers"></a>
### G.GetAtomicNumbers
Function *GetAtomicNumbers* acts on geometry objects and returns and array with the atomic numbers of the elements in the working geometry.

**Syntax:**
*atomNumbers = geom.GetAtomicNumbers()*

*atomNumbers* A  variable that will be filled with the values of the atomic numbers

*geom* A geometry object that should already be loaded.

**Example:**

```mol
title: structure 6
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
3
structure (0 1)
o    1.23009925   0.02698440  -0.00375550
h    1.60672086  -0.41139567   0.76236888
h    1.60236356  -0.44922858  -0.74915800
--- input ---
# --------------------------------------------------------
# This is a scrtipt to check the geom.CreateBSSE command
# -------------------------------------------------------

*xyz 0 1
o:      -1.69296787   -0.05579265    0.00556629
h:      -2.01296504    0.84704339   -0.01586469
h:      -0.73325076    0.04238910    0.00084302
o        1.23009925    0.02698440   -0.00375550
h        1.60672086   -0.41139567    0.76236888
h        1.60236356   -0.44922858   -0.74915800
*

%Compound
  Geometry monomerA;
  variable myFilename     = "BSSE";
  Variable method         = "BP86";

  # --------------------------------------
  # Calculation for Fragment A
  # --------------------------------------
  New_Step
    !&{method} 
  Step_End

  # -------------------------------------
  # Read the geometry of Fragment A
  # -------------------------------------
  monomerA.Read();

  # -------------------------------------
  # Create the missing xyz files
  # -------------------------------------
  monomerA.CreateBSSE(filename=myFilename);

End
```

<a id="sec:workflowsautomatization.compound_detailed.commands.geometry.getBondDistance"></a>
### G.GetBondDistance
Function *GetBondDistance* acts on geometry objects and returns the distance between two atoms **in Bohrs**.

**Syntax:**

*res = geom.GetBondDistance(atomA, atomB)*

Where:

*res* The distance between atoms atomA and atomB.

*geom* A geometry object previously loaded.

*atomA* The index of atomA in the geometry.

*atomB* The index of atomB in the geometry.

**NOTE** indices start counting from 0

**Example:**

```mol
title: structure 7
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
3
structure (0 1)
O   -1.69296787  -0.05579265   0.00556629
H   -2.01296504   0.84704339  -0.01586469
H   -0.73325076   0.04238910   0.00084302
--- input ---
# ----------------------------------------------------
# This is a script to check the followNormalMode function
# -----------------------------------------------------
*xyz 0 1
  O      -1.69296787   -0.05579265    0.00556629
  H      -2.01296504    0.84704339   -0.01586469
  H      -0.73325076    0.04238910    0.00084302
*

%Compound
  Geometry myGeom;
  Variable CC, normalModes;
  Variable res = -1;
  New_Step
    !BP86 Freq
  Step_End
  myGeom.Read();
  myGeom.FollowNormalMode(vibrationSN=7, scalingFactor=0.8);
  CC = myGeom.GetCartesians();
  CC.PrintMatrix();
End
```

<a id="sec:workflowsautomatization.compound_detailed.commands.geometry.getCartesians"></a>
### G.GetCartesians

Function *GetCartesians* acts on geometry objects (see [commands.geometry](#sec:workflowsautomatization.compound_detailed.commands.geometry)) and returns the distance xyz cartesian coordinates. Please remember that it alsways returns the cooridnates in **BOHRS**.

**Syntax:**

*coords = geom.GetCartesians()*

Where:

*coords*: A (*nAtoms*,3) array with the cartesian coordinates in **BOHRS**.

*geom*: A geometry object previously loaded.

**Example:**

```mol
title: structure 8
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
3
structure (0 1)
O         0.000        0.000        0.394
H        -0.755        0.000       -0.197
H         0.755        0.000       -0.197
--- input ---
# ------------------------------------
# This is to test Geometry function
#         DisplaceAtom
# ------------------------------------
%Compound
  Variable dist=0.1;
  Geometry myGeom;
  NewStep
    !BP86
    *xyz 0 1
       O  0.000  0.000   0.394
       H -0.755  0.000  -0.197
       H  0.755  0.000  -0.197
    *
  StepEnd
  myGeom.Read();
  myGeom.DisplaceAtom(0, 0.0, 0.0, -dist);  #Move the z coordinate of Oxygen
  myGeom.WriteXYZFile(filename="displaced.xyz");

End
```

<a id="sec:workflowsautomatization.compound_detailed.commands.geometry.getGhostAtoms"></a>
### G.GetGhostAtoms   
Function *GetGhostAtoms* acts on geometry objects (see [commands.geometry](#sec:workflowsautomatization.compound_detailed.commands.geometry)). It returns a vector of size nAtoms where for each atom the value will be -1 if it is a ghost atom, otherwise the atomic number of the element

**Syntax:**

*ghostAtoms = geom.GetGhostAtoms()*

Where:

*ghostAtoms*: A (*nAtoms*,1) integer vector with values -1 or the atomic number of the atom, in case it is not a ghost atom.

*geom*: A geometry object previously loaded.

**Example:**

```mol
title: structure 9
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
3
structure (0 1)
O    0.00000000   0.00000000   0.39393904
H   -0.75503878   0.00000000  -0.19696952
H    0.75503878   0.00000000  -0.19696952
--- input ---
# ------------------------------------
# This is to test Geometry function
#           GetAngle  
# ------------------------------------
%Compound
  Variable dist;
  Geometry myGeom;
  New_Step
    !BP86
    *xyz 0 1
       O  0.00000000  0.00000000   0.39393904
       H -0.75503878  0.00000000  -0.19696952
       H  0.75503878  0.00000000  -0.19696952
    *
  Step_End
  myGeom.Read();  #Reads teh geometry of the previous step
  print( " -------------------------------------------------------\n");
  print( "  Compound Geometry functions test (GetAngle) \n");
  print( "  It should print 103.9051 Degrees\n");
  print( " -------------------------------------------------------\n");
  print( " The angle between atom %d, atom %d and atom %d  is: %.4lf Degreess\n", 
           1, 0, 2, myGeom.GetAngle(1,0,2));

End
```

<a id="sec:workflowsautomatization.compound_detailed.commands.geometry.getNumOfAtoms"></a>
### G.GetNumOfAtoms

*GetNumOfAtoms* returns an integer with the number of atoms of the working geometry.

**Syntax:**

*res = geom.GetNumOfAtoms();*

Where:

*res* is the resulting number of atoms

*geom* is the name of a geometry variable (see [commands.geometry](#sec:workflowsautomatization.compound_detailed.commands.geometry)) we are using.

**Example:**
```mol
title: structure 10
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
3
structure (0 1)
O   -1.69296787  -0.05579265   0.00556629
H   -2.01296504   0.84704339  -0.01586469
H   -0.73325076   0.04238910   0.00084302
--- input ---
*xyz 0 1
  O      -1.69296787   -0.05579265    0.00556629
  H      -2.01296504    0.84704339   -0.01586469
  H      -0.73325076    0.04238910    0.00084302
*

%Compound
  Geometry myGeom;
  Variable atomicNumbers;

  New_Step
    !BP86
  Step_End
  myGeom.Read();
  atomicNumbers = myGeom.GetAtomicNumbers();
  print("\nCompound \n");
  for i from 0 to atomicNumbers.GetSize()-1 Do
    print("Atom '%d': atomic number: %d\n", i, atomicNumbers[i]);
  EndFor
End
```

<a id="sec:workflowsautomatization.compound_detailed.commands.geometry.moveAtomToCenter"></a>
### G.MoveAtomToCenter

Function *MoveAtomToCenter* acts on geometry objects (see [commands.geometry](#sec:workflowsautomatization.compound_detailed.commands.geometry)). It will adjust the cartesian coordinates so that the chosen atom will rest at (0.0 0.0 0.0).

**Syntax:**

*geom.MoveAtomToCenter(atom serial nubmer);*

Where:

*geom*: A geometry object previously loaded.

*atom serial number*: The serial number of the atom in the geometry.

**Example:**

```mol
title: structure 11
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
2
structure (0 1)
H           0.0          0.0          0.0
H           0.0          0.0          0.8
--- input ---
# ------------------------------------
# This is to test Geometry function
#    GetBondDistance
# ------------------------------------
%Compound
  Variable dist;
  Geometry myGeom;
  New_Step
    !BP86
    *xyz 0 1
      H 0.0 0.0 0.0
      H 0.0 0.0 0.8
    * 
  Step_End
  myGeom.Read();  #Reads teh geometry of the previous step
  print( " -------------------------------------------------------\n");
  print( "  Compound Geometry functions test (GetBondDistance) \n");
  print( "  It should print 1.5118\n");
  print( " -------------------------------------------------------\n");
  print( " The distance between atom %d and atom %d  is: %.4lf Bohr\n", 
           0, 1, myGeom.GetBondDistance(0,1));

End
```
**NOTE** Please remember that counting **starts with 0**, meaning that the first atom is 0 and not 1!

<a id="sec:workflowsautomatization.compound_detailed.commands.geometry.read"></a>
### G.Read

Function *Read* acts on geometry objects (see [commands.geometry](#sec:workflowsautomatization.compound_detailed.commands.geometry)) and reads a geometry from a property file related to a previous step.

**Syntax:**

*geom.Read([stepID=myStepID], propertySN=myPropertySN)*

Where:

*geom*: A geometry object that will be updated.

*stepID*: The step from which we are going to read the geometry. If not given the previous step  will be used.

*propertySN*: The serial number the geometry in the property file. If not given the last available geometry will be used.

**Example:**

```mol
title: structure 12
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
3
structure (0 1)
O   -1.69296787  -0.05579265   0.00556629
H   -2.01296504   0.84704339  -0.01586469
H   -0.73325076   0.04238910   0.00084302
--- input ---
# ----------------------------------------------------
# This is a script to check the GetCartesians function
# NOTE: It always return it in Bohrs!
# -----------------------------------------------------
*xyz 0 1
  O      -1.69296787   -0.05579265    0.00556629
  H      -2.01296504    0.84704339   -0.01586469
  H      -0.73325076    0.04238910    0.00084302
*

%Compound
  Geometry myGeom;
  Variable CC;
  New_Step
    !BP86
  Step_End
  myGeom.Read();
  CC = myGeom.GetCartesians();
  for i from 0 to CC.GetDim1()-1 Do
    print("%12.9lf  %12.9lf  %12.9lf\n", 
    CC[i][0], CC[i][1], CC[i][2]);
  endFor
End
```

<a id="sec:workflowsautomatization.compound_detailed.commands.geometry.removeAtoms"></a>
### G.RemoveAtoms

Function *RemoveAtoms* acts on geometry objects (see [commands.geometry](#sec:workflowsautomatization.compound_detailed.commands.geometry)). It accepts a list of atoms and removes them from the loaded geometry. In the end the geometry object will be updated.

**Syntax:**

*geom.RemoveAtoms(atom1, atom2, ...);*

Where:

*geom*: A geometry object previously loaded.

*atom1, atom2, ...*: The serial number of the atoms in the geometry.

**Example:**

```mol
title: structure 13
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
3
structure (0 1)
o    1.23009925   0.02698440  -0.00375550
h    1.60672086  -0.41139567   0.76236888
h    1.60236356  -0.44922858  -0.74915800
--- input ---
# ----------------------------------------------------
# This is a script to check the getGhostAtoms function
# -----------------------------------------------------
*xyz 0 1
o:      -1.69296787   -0.05579265    0.00556629
h:      -2.01296504    0.84704339   -0.01586469
h:      -0.73325076    0.04238910    0.00084302
o        1.23009925    0.02698440   -0.00375550
h        1.60672086   -0.41139567    0.76236888
h        1.60236356   -0.44922858   -0.74915800
*

%Compound
  Geometry myGeom;
  Variable ghostAtoms;
  New_Step
    !BP86 
  Step_End
  myGeom.Read();
  ghostAtoms = myGeom.GetGhostAtoms();
  ghostAtoms.PrintMatrix();
End
```
**NOTE** Please remember that counting **starts with 0**, meaning that the first atom is 0 and not 1!

<a id="sec:workflowsautomatization.compound_detailed.commands.geometry.removeElements"></a>
### G.RemoveElements

Function *RemoveElements* acts on geometry objects (see [commands.geometry](#sec:workflowsautomatization.compound_detailed.commands.geometry)). It will remove from the loaded geometry all atoms with an atomic number given in the
list.

**Syntax:**

*geom.RemoveElements(atomNumber1, atomicNumber2, ...);*

Where:

*geom*: A geometry object previously loaded.

*atomicNumber1, atomicNumber2, ...*: The atomic number of elements to be removed from the current geometry.

**Example:**

```mol
title: structure 14
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
3
structure (0 1)
O   -1.69296787  -0.05579265   0.00556629
H   -2.01296504   0.84704339  -0.01586469
H   -0.73325076   0.04238910   0.00084302
--- input ---
*xyz 0 1
  O      -1.69296787   -0.05579265    0.00556629
  H      -2.01296504    0.84704339   -0.01586469
  H      -0.73325076    0.04238910    0.00084302
*

%Compound
  Geometry myGeom;
  Variable numOfAtoms = 0;

  New_Step
    !BP86
  Step_End
  Alias currStep;
  myGeom.Read(currStep);
  numOfAtoms = myGeom.GetNumOfAtoms();
  print("\nCompound \n");
  print("Number of atoms: %d (it should print 3)\n", numOfAtoms);

End
```

<a id="sec:workflowsautomatization.compound_detailed.commands.geometry.writeXYZFile"></a>
### G.WriteXYZFile

Function *WriteXYZFile* acts on geometry objects (see [commands.geometry](#sec:workflowsautomatization.compound_detailed.commands.geometry)) and writes on disc an xyz file with the coordinates of the current goemetry object. Please remember that by default it writes the coordinates in **Angstroems**. 

**Syntax:**

*res = geom.WriteXYZFile(filename=myFilename, [useBohr=True/False])*

Where:

*res*: An integer that returns '0' if everything worked smoothly.

*myFilename* The name of the file that will contain the coordinates.

*useBohr*: A boolean that can take the value of "True" or "False". This is an optional argument and the default value is "False".

*geom*: A geometry object previously loaded.

**NOTE:** Please note that we changed the default units. Now by default we write the xyz file in Angstroems. We added the parameter UseBohr that is set by default to "False" but if it is used with the value "True" then the geometry is saved in Bohrs.

**Example:**

```mol
title: structure 15
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
3
structure (0 1)
O   -1.69296787  -0.05579265   0.00556629
H   -2.01296504   0.84704339  -0.01586469
H   -0.73325076   0.04238910   0.00084302
--- input ---
# ----------------------------------------------------
# This is a script to check the moveAtomToCenter function
# -----------------------------------------------------
*xyz 0 1
  O      -1.69296787   -0.05579265    0.00556629
  H      -2.01296504    0.84704339   -0.01586469
  H      -0.73325076    0.04238910    0.00084302
*

%Compound
  Geometry myGeom;
  Variable CC;
  New_Step
    !BP86
  Step_End
  myGeom.Read();
  myGeom.MoveAtomToCenter(0);
  myGeom.BohrToAngs();
  CC = myGeom.GetCartesians();
  CC.PrintMatrix();
End
```

<a id="sec:workflowsautomatization.compound_detailed.commands.goat"></a>
### GOAT

In *Compound* we have *GOAT* objects. These objects can be treated like normal variables of type '*compGOAT*'. An important difference between normal variables and *GOAT* variables is the declaration. Instead of the normal:
```
Variable myGoat;
```
we excplicitly have to declare that this is a GOAT object. So the syntax for a goat declaration is:

**Syntax:**
```
GOAT myGoat;
```

Below is a list of functions that work on *Geometry* objects. 

-   Get_Energy ([goat.getEnergy](#sec:workflowsautomatization.compound_detailed.commands.goat.getEnergy))

-   Get_Num_Of_Geometries ([goat.getNumOfGeometries](#sec:workflowsautomatization.compound_detailed.commands.goat.getNumOfGeometries))

-   ParseEensembleFile ([goat.parseEnsembleFile](#sec:workflowsautomatization.compound_detailed.commands.goat.parseEnsembleFile))

-   Set_Basename ([goat.setBasename](#sec:workflowsautomatization.compound_detailed.commands.goat.setBasename))

-   Print ([goat.print](#sec:workflowsautomatization.compound_detailed.commands.goat.print))

-   WriteXYZFile ([goat.writeXYZFile](#sec:workflowsautomatization.compound_detailed.commands.goat.writeXYZFile))  

**Example:**

```mol
title: structure 16
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
3
structure (0 1)
O   -1.69296787  -0.05579265   0.00556629
H   -2.01296504   0.84704339  -0.01586469
H   -0.73325076   0.04238910   0.00084302
--- input ---
# ----------------------------------------------------
# This is a script to check the Read function for 
#   geometries
# -----------------------------------------------------
*xyz 0 1
  O      -1.69296787   -0.05579265    0.00556629
  H      -2.01296504    0.84704339   -0.01586469
  H      -0.73325076    0.04238910    0.00084302
*

%Compound
  Geometry myGeom;
  Variable CC;
  New_Step
    !BP86 opt
  Step_End
  myGeom.Read(propertySN=2);
End
```

<a id="sec:workflowsautomatization.compound_detailed.commands.goat.getEnergy"></a>
### Goat.Get_Energy

Function *Get_Energy* acts on goat objects (see [commands.goat](#sec:workflowsautomatization.compound_detailed.commands.goat)) and returns a double with the energy of the requested structure.

**Syntax:**

*res = myGoat.Get_Energy(geomID=myGeomID)*

Where:

*res*: A double with the energy of the requested structure.

*myGoat* A GOAT object that is already loaded (meaning it has already parse an ensemble file, see (see [goat.parseEnsembleFile](#sec:workflowsautomatization.compound_detailed.commands.goat.parseEnsembleFile)).

*myGeomID*: The geometry ID of the requested structure. Counting starts from 1. 

**Example:**

  see example in [commands.goat](#sec:workflowsautomatization.compound_detailed.commands.goat)

<a id="sec:workflowsautomatization.compound_detailed.commands.goat.getNumOfGeometries"></a>
### Goat.Get_Num_Of_Geometries

Function *Get_Num_Of_Geometries* acts on goat objects (see [commands.goat](#sec:workflowsautomatization.compound_detailed.commands.goat)) and returns an integer with the number of structures available in the current *GOAT* object.

**Syntax:**

*res = myGoat.Get_Num_Of_Geometries()*

Where:

*res*: An integer with the number of geometries in the current *GOAT* object.

*myGoat* A GOAT object that is already loaded (meaning it has already parse an ensemble file, see (see [goat.parseEnsembleFile](#sec:workflowsautomatization.compound_detailed.commands.goat.parseEnsembleFile)).

**Example:**

  see example in [commands.goat](#sec:workflowsautomatization.compound_detailed.commands.goat)

<a id="sec:workflowsautomatization.compound_detailed.commands.goat.parseEnsembleFile"></a>
### Goat.ParseEnsembleFile

Function *ParseEnsembleFile* acts on goat objects (see [commands.goat](#sec:workflowsautomatization.compound_detailed.commands.goat)). It will read an ensemble file created by a GOAT run and then update the object with the geometries and energies of each geometry available in the current *GOAT* object.

**Syntax:**

*res = geom.ParseEnesembleFile(filename=myFilename)*

Where:

*res*: An integer that returns '0' if everything worked smoothly.

*myFilename* The name of the file that will contain the coordinates.

*myGoat*: A GOAT object previously loaded.

**Example:**

  see example in [commands.goat](#sec:workflowsautomatization.compound_detailed.commands.goat)

**NOTE:** The old syntax (Parse_Ensemble_File) is still compatible but please do not use it because in the future it will be deprecated.

<a id="sec:workflowsautomatization.compound_detailed.commands.goat.setBasename"></a>
### Goat.Set_Basename

Function *Set_Basename* acts on goat objects (see [commands.goat](#sec:workflowsautomatization.compound_detailed.commands.goat)). It set the basename of the ensemble file created by a GOAT run. It will automatically add the extension: `'.finalensemble.xyz'` in the end of the basename.

**Syntax:**

*myGoat.Set_Basename(myFilename)*

Where:

*myFilename* The basename of the GOAT ensemble file (**without the extension 'finalensemble.xyz'**).

*myGOAT*: A GOAT object previously loaded.

**Example:**

see example in [commands.goat](#sec:workflowsautomatization.compound_detailed.commands.goat)

<a id="sec:workflowsautomatization.compound_detailed.commands.goat.print"></a>
### Goat.Print

Function *Print* acts on goat objects (see [commands.goat](#sec:workflowsautomatization.compound_detailed.commands.goat)). It will print in the output the geometries of current GOAT object.

**Syntax:**

*myGoat.Print()*

Where:

*myGoat*: A GOAT object previously loaded.

**Example:**

see example in [commands.goat](#sec:workflowsautomatization.compound_detailed.commands.goat)

<a id="sec:workflowsautomatization.compound_detailed.commands.goat.writeXYZFile"></a>
### Goat.WriteXYZFile

Function *WriteXYZFile* acts on goat objects (see [commands.goat](#sec:workflowsautomatization.compound_detailed.commands.goat)). It will write the requested geometry to an XYZ file on disk. It expects two arguments: 
1. The geometry ID of the geometry and 
2. The filename that it will use to store the geometry

**Syntax:**

*myGoat.WriteXYZFile(geomID=myGeomID, filename=myFilename)*

Where:

*myFilename:* The name that it will be used to store the geometry on the disk.

*myGeomID*: The geometry ID of the requested structure. Counting starts from 1. 

**Example:**

see example in [commands.goat](#sec:workflowsautomatization.compound_detailed.commands.goat)

<a id="sec:workflowsautomatization.compound_detailed.commands.propertyFile.getNumOfInstances"></a>
###  GetNumOfInstances
The *GetNumOfInstances* returns the number of instances of a specific object in a propertyfile.

**Syntax:**

*[res=] GetNumOfInstances(propertyName=myName, [step=myStep], [filename=myFilename], [baseProperty=true/false])*

*Where:*

*res:* An integer that returns the number of instances of the required property in the property file.

*propertyName:* A string alias that defines the variable the user wants to read.

*step:* The step from which we want to read the property. If not given the property file from the last step will be read.

*filename:* A filename of a property file. If a filename and at the same time a step are provided the program will ignore the step and try to read the property file with the given filename. 

**NOTE** please note that in the end of filename the extension *.property.txt* will be added.

*baseProperty:* A true/false boolean. The default value is set to false. If the value is set to true then a generic property of the type asked will be read. This means if dipole moment is asked, it will return the last dipole moment, irrelevant if and MP2 or SCF one wad defined.

 **Example**
```mol
title: structure 17
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
3
structure (0 1)
O   -1.69296787  -0.05579265   0.00556629
H   -2.01296504   0.84704339  -0.01586469
H   -0.73325076   0.04238910   0.00084302
--- input ---
# ----------------------------------------------------
# This is a script to check the RemoveAtoms function
# -----------------------------------------------------
*xyz 0 1
  O      -1.69296787   -0.05579265    0.00556629
  H      -2.01296504    0.84704339   -0.01586469
  H      -0.73325076    0.04238910    0.00084302
*

%Compound
  Geometry myGeom;
  Variable numOfAtoms;
  New_Step
    !BP86
  Step_End
  myGeom.Read();
  numOfAtoms = myGeom.GetNumOfAtoms();
  print("Number of atoms before: %d (It should print 3)\n", numOfAtoms);
  myGeom.RemoveAtoms(0);  #Remove the first atom
  numOfAtoms = myGeom.GetNumOfAtoms();
  print("Number of atoms after : %d (It should print 2)\n", numOfAtoms);
End
```

<a id="sec:workflowsautomatization.compound_detailed.commands.goto"></a>
### GoTo
The *GoTo* command allows the 'jump' inside the normal flow of a *compound* script. The syntax of the command can be best presented through an example.

**Example:**
```mol
title: structure 18
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
3
structure (0 1)
O   -1.69296787  -0.05579265   0.00556629
H   -2.01296504   0.84704339  -0.01586469
H   -0.73325076   0.04238910   0.00084302
--- input ---
# ----------------------------------------------------
# This is a script to check the RemoveElements function
# -----------------------------------------------------
*xyz 0 1
  O      -1.69296787   -0.05579265    0.00556629
  H      -2.01296504    0.84704339   -0.01586469
  H      -0.73325076    0.04238910    0.00084302
*

%Compound
  Geometry myGeom;
  Variable numOfAtoms;
  Variable CC;
  New_Step
    !BP86
  Step_End
  myGeom.Read();
  numOfAtoms = myGeom.GetNumOfAtoms();
  CC = myGeom.GetCartesians();
  CC.PrintMatrix();
  print("Number of atoms before: %d (It should print 3)\n", numOfAtoms);
  myGeom.RemoveElements(8);  #Remove the oxygen
  numOfAtoms = myGeom.GetNumOfAtoms();
  print("Number of atoms after : %d (It should print 2)\n", numOfAtoms);
  CC = myGeom.GetCartesians();
  CC.PrintMatrix();
End
```

Please note that the variable we use as a label for the *GoTo* command should be previously defined like a normal variable.

<a id="sec:workflowsautomatization.compound_detailed.commands.if"></a>
### If
The *if* block allows the user to make decisions. The syntax in
*Compound* is the following:\
**Syntax:**

**If** *(expression)* **Then**

*actions*

**Else if** *(expression)* **Then**

*actions*

**Else**

*actions*

**Endif**

Below is an example of the usage of *if block* in *compound*.

```mol
title: structure 19
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
3
structure (0 1)
O   -1.69296787  -0.05579265   0.00556629
H   -2.01296504   0.84704339  -0.01586469
H   -0.73325076   0.04238910   0.00084302
--- input ---
# -------------------------------------------------------
# This is a script to check the WriteXYZ function
# NOTE: By default it write the coordinates in Angstroems!
# -------------------------------------------------------
*xyz 0 1
  O      -1.69296787   -0.05579265    0.00556629
  H      -2.01296504    0.84704339   -0.01586469
  H      -0.73325076    0.04238910    0.00084302
*

%Compound
  Geometry myGeom;
  Variable res=-1;
  New_Step
    !BP86
  Step_End
  myGeom.Read();
  res = myGeom.WriteXYZFile(filename="myGeom.xyz",useBohr=false);
End
```

Some comments about the syntax:

The *Else if* or *Else* blocks are not obligatory.

The numerical operators that can be used are: *'\>', '\<', '\>=', '\<=',
'='*.

The available logical operators are: *'and' and 'or'*.

Unfortunately in the current version multi-parentheses are not allowed.

There is now the possibility to compare strings.

<a id="sec:workflowsautomatization.compound_detailed.commands.linAlgegra.invertMatrix"></a>
### InvertMatrix
*Compound* can peform matrix algebraic operations, one of the available algebraic operation is the inversion of a matrix. Be carefull that the matrix, whose the invert we are looking for, **must be** a real, square matrix. 

**Syntax:**\
*AInvert = A.InvertMatrix();*

Where:

- *A:* The matrix to be inverted.
- *AInvert:* The invert of A. It can be A itself and then A will just be updated.

**Example:**
```orca
Variable myGoat;
```

<a id="sec:workflowsautomatization.compound_detailed.commands.linAlgegra.Mat_p_Mat"></a>
### Mat_p_Mat
*Compound* can peform matrix algebraic operations, one of the available algebraic operation is matrix addittion. In order to add two matrices they **must** have the same dimensions.

**Syntax:**\
*C=Mat_p_Mat(alpha, A, beta, B);*

Where:

- *C:* The resulting matrix.
- *alpha:* The coefficient for matrix A.
- *A:* The left matrix of the addition.
- *beta:* The coefficient for matrix B.
- *B:* The right matrix of the addition.

**Example:**
```orca
GOAT myGoat;
```

<a id="sec:workflowsautomatization.compound_detailed.commands.linAlgegra.Mat_x_Mat"></a>
### Mat_x_Mat
*Compound* can peform matrix algebraic operations, one of the available algebraic operation is matrix multiplication. In general we can multiply each matrix with constants *alpha* and *beta* so that the general multiplication is:

*C=(alpha*A)*(beta*B)

In addition each of matrices A and B are allowed to be transposed.

**Syntax:**\
*C=Mat_x_Mat(A, B, [transposeA], [transposeB], [alpha], [beta]);*

Where:

- *C:* The resulting matrix.
- *A:* The left matrix of the multiplication.
- *B:* The right matrix of the multiplication.
- *transposeA:* A boolean to state if matrix A should be transposed before the mutliplication (default: False).
- *transposeB:* A boolean to state if matrix B should be transposed before the multiplication (default: False).
- *alpha:* A scalar to multiply matrix A before the mutliplication (default 1.0).
- *beta:* A scalar to mutliply matrix B before the multiplication (default 1.0).

**Example:**
```orca
# Example for the usage of GOAT objects in compound
#  
# NOTE:  The file 'test.finalensemble.xyz'
#        should be availablie in the directory
%Compound
  goat myGoat;
  variable myFilename;
  myGoat.Set_Basename("test");
  myGoat.ParseEnsemblefile();
  for myGeomID from 1 to myGoat.Get_Num_of_Geometries() Do
    write2String(myFilename, "goatGeom_%d.xyz", myGeomID);
    myGoat.WriteXYZFile(geomID=myGeomID, filename=myFilename);
    print("geomID: %d Energy: %lf\n", myGeomID, myGoat.Get_Energy(geomID=myGeomID));
  EndFor
  myGoat.Print();
EndRun
```

<a id="sec:workflowsautomatization.compound_detailed.commands.linAlgegra.Mat_x_Scal"></a>
### Mat_x_Scal
*Compound* can peform matrix algebraic operations, one of the available algebraic operation is multiplication of the elements of a matrix with a scalar. The function returns the multiplied matrix that can be the one that we use as an argument in the parenthesis, meaning it is updated, or a different one.

**Syntax:**\
*C=Mat_x_Scal(alpha, A);*

Where:

- *C:* The resulting matrix.
- *alpha:* A scalar to multiply the elements of matrix A.
- *A:* The matrix to be mutliplied.

**Example:**
```mol
title: structure 20
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
2
structure (0 1)
H           0.0          0.0          0.0
H           0.0          0.0          0.8
--- input ---
# ----------------------------------------------------
# This is an example script for readNumOfInstances
# -----------------------------------------------------
%Compound
  Variable res = 0;
  Variable myProperty="MP2_DIPOLE_TOTAL";
  Variable myBaseProperty="DIPOLE_MOMENT_TOTAL";
  New_Step
    !MP2
    #%mp2
    #  density relaxed
    #end
    *xyz 0 1
      H 0.0 0.0 0.0
      H 0.0 0.0 0.8
    *
  Step_End
  # First read the MP2 dipole moment
  res = GetNumOfInstances(propertyName=myProperty);
  print("Num of MP2 dipole moments   : %d\n", res);
  res = GetNumOfInstances(propertyName=myBaseProperty, Property_Base=true);
  print("Num of total dipole moments : %d\n", res);
End
```

<a id="sec:workflowsautomatization.compound_detailed.commands.newgeom"></a>
### NewGeom

*NewGeom* is a platform for geometry manipulation. The basic idea is to
have functions that can read a geometry and then produce one or more new
geometries with some characteristics that we need. For the moment under
the umbrella of *NewGeom* fall 4 different functions, and these are:
Displace, Remove_Atom, Remove_Element.

**NOTE:** The old syntax (New_Geom) is still compatible but please do not use it because in the future it will be deprecated.

<a id="sec:workflowsautomatization.compound_detailed.commands.new_geom.displace"></a>
#### Displace

The idea behind \"*Displace'*\" is to have a structure, perform an
analytical frequncy calculation on it (currently we do not store
numerical frequencies in the property file) and then read the Hessian
from this calculation to adjust the geometry based on a normal mode of
vibration that we choose. The syntax of this command is:

**syntax:** NewGeom = (Displace, step, hessian, frequency, scaling)

where:\
*step* is the step from which we choose the original geometry\
*hessian* is the hessian read from a property file\
*frequency* defines which normal mode we will use and\
*scaling* is a factor of how severe we want the displacement to be.

We should note that *Displace* is the only command of the *new_geom*
family of commands that will not store a geometry on disk but only
internally pass the new geometry to the next calculation. An example of
the usage of this command can be found in the script
'iterativeOptimization' that is given with ORCA. The relevant part is as
follows: **example:**

```orca
# Define variables
		Variable MaxNTries    =  25; 
		Variable CutOff       = -50;
		Variable displacement = 0.6;
		Variable NNegative =   0;  
		Variable freqs[];
		Variable modes[];
		Variable NFreq;
		Variable limit;
		Variable done;
		Variable FinalEnergy; 
		
		# ===========================================================
		# Start a for loop over number of tries
		# ===========================================================
		For itry From 1 To maxNTries Do
		
		# ----------------------------------
		# Run a geometry optimization
		# ----------------------------------
		New_Step
		! tightopt freq verytightscf nopop def2-TZVP xyzfile
		Step_End
		Read freqs  = THERMO_FREQS[itry];
		Read modes  = HESSIAN_MODES[itry];
		Read NFreq  = THERMO_NUM_OF_FREQS[itry];
		limit = NFreq - 1;
		# ----------------------------------
		#  check for sufficeintly negative 
		#  frequencies
		# ----------------------------------
		NNegative = 0;
		For ifreq From 0 to limit Do
		if ( freqs[ifreq] < CutOff )  then
		New_Geom = (Displace, itry,  modes,  ifreq, displacement);
```

<a id="sec:workflowsautomatization.compound_detailed.commands.openFile"></a>
### OpenFile

*Compound* can write text files on disk. In order to write to a file  a filepointer must be created. For this in *Compound* exists the command *OpenFile*.

**Syntax:**\
filePtr = *OpenFile*(*Filename*, "*open mode*");

*filePtr* is a variable previously declared.

*Filename* can be a string or a variable of string type and represents the name of the file on disk.

There are two available *opening modes*: 
- 'w'. In this mode a new file will be created and the user can write on it. If an old file with the same name exists, it's contents will be deleted.
- 'a'. In this mode if a file already exists, the user will append to what already exists in the file.
  

**Example:**
```orca
# ----------------------------------------------------
# This is an example script for GoTo
# (It should print only 0,1,2,3)
# -----------------------------------------------------
%Compound
  Variable TCut=3;
  Variable Done;
  for i from 0 to 6 Do
    print("Index: %d\n", i);
    if (i >= TCut) then
      GoTo Done;
    EndIf
  EndFor
  Done:
    print("Done\n");
End
```

<a id="sec:workflowsautomatization.compound_detailed.commands.new_geom.remove_atom"></a>
#### Remove_Atom

Remove_atom removes an atom from a geometry given its index. We should
point out that counting of atoms in ORCA starts with 0. After this
command is executed it will store on a disk a new geomety in a xyz
format where only the atom with the given index will be missing.

**Syntax:**

NewGeom = ( Remove_atom, atomIndex, \"filename\", stepIndex, [geometry
Index]);

where:\
*atom Index* is the number of the atom we want to remove. It can be an
integer number or a variable.\
*filename* is the name of the file that we want to use for the new xyz
file. It can be a string in quotation marks or a variable already
defined before. In the name the xyz extension will be automatically
appended. *step Index* the number of the step from which we will get the
initial geometry. It has to be an integer number. *geometry Index* In
case there are more than one geometries in the corresponding property
file we can choose one. If no number is given but default the program
will use the last one.

**example:**

if we use the normal ORCA input file:

```orca
# -------------------------------------------------------------
# This is to check all available ways of 'if blocks'
# -------------------------------------------------------------
Variable x1 = 10.0;
Variable y1 = 20.0; 
Variable b1 = False;
Variable b2 = True;
Variable s1 = "alpha";
Variable s2 = "beta";
Variable s3 = "alpha";
print( " --------------------------------------------------------- \n");
print( " ----------      SUMMARY OF IF CASES        -------------- \n");
print( " --------------------------------------------------------- \n");

print(" x1: %.1lf\n", x1);
print(" y1: %.1lf\n", y1);
print(" b1: %s\n", b1.GetString());
print(" b2: %s\n", b2.GetString());
print(" s1: %s\n", s1);
print(" s2: %s\n", s2);
print(" s3: %s\n", s3);
# ****************************************************************
#                           DOUBLES
# ****************************************************************
print(" -------------------     Doubles     ---------------------- \n");
print("      Variable/constant / One operator  / if (x1>5)         \n");
print("                    No else if/No else                      \n");
if (x1>5) then
  print(" %.2lf > 5 \n", x1);
endif    
# ----------------------------------------------------------------
print("      function / Variable / One operator  / if (3*x1>y1)    \n");
print("                   no else if /   else                      \n");
if (3*x1>y1) then
  print(" 3*%.1lf > %.1lf\n", x1, y1);
else
  print(" 3*%.1lf < %.1lf\n", x1, y1);  
endif
# ----------------------------------------------------------------
print("     function / function / One operator  / if (x1-y1>-10.0) \n");
print("                    else if/else                      \n");
if (x1-y1>-10.0) then
  print(" %.2lf - %.2lf > -10.0\n", x1, y1); 
else if (x1-y1 < -10.0) then
  print(" %.2lf - %.2lf < -10.0\n", x1, y1); 
else
  print(" %.2lf - %.2lf = -10.0\n", x1, y1);  
endif
# ****************************************************************
#                          BOOLEANS
# ****************************************************************
print(" ---------------      Booleans      ---------------------------\n");
print("       Variable  /  No operator  /  if (b1)                   \n");
if (b1) then
  print("b1 is True\n");
else
  print("b1 is False\n");
endIf
# --------------------------------------------------------------------
# ---------------------------------------------------------------------
print("       Constant  / No operator  / if (true)                   \n");
if (True) then
  print( "True\n");
else
  print( "False");
endIf
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
print("       Variable/Variable / AND operator / if (b1 and b2)                 \n");
if (b1 and b2) then
  print("(%s and %s) is true\n", b1.GetString(), b2.GetString());
else
  print("(%s and %s) is not true\n", b1.GetString(), b2.GetString());
endIf
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
print("       Variable/Variable / OR operator / if (b1 or b2)                 \n");
if (b1 OR b2) then
  print("(%s or %s) is true\n", b1.GetString(), b2.GetString());
else
  print("(%s or %s) is not true\n", b1.GetString(), b2.GetString());
endIf
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
print("       Bool /Doubles Function / AND operator / if (b1 and x1>y1 )\n");
if (b1 and y1>x1) then
  print("(%s and %.1lf>%.1lf) is True\n", b1.GetString(), x1, y1);
else
  print("(%s and %.1lf>%.1lf) is False\n", b1.GetString(), x1, y1);
endIf
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
print("       Nested if / if (b2) then if (y1>x1)\n");
if (b2) then
  if (y1 > x1) then
    print ( "(%s is True) and (%.1lf>%.1lf)\n", b2.GetString(), y1, x1);
  else
    print ( "(%s is True) and (%.1lf<%.1lf)\n", b2.GetString(), y1, x1);
  endIf
else
    print ( "%s is False\n", b2.GetString());
endIf
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
print(" ----------------      Strings     ---------------------------\n");
print(" -------------------------------------------------------------\n");
print(" -------------------------------------------------------------\n");
print("       Variable/Variable / if s1=s2\n");
if (s1=s2) then
  print("%s is same as %s \n", s1, s2);
else
  print("%s is not same as %s \n", s1, s2);
EndIf

# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
print(" ----------------      Strings     ---------------------------\n");
print(" -------------------------------------------------------------\n");
print(" -------------------------------------------------------------\n");
print("       Variable/constant / if s1=\"alpha\"\n");
if (s1="alpha") then
  print("%s is same as %s \n", s1, "alpha");
else
  print("%s is not same as %s \n", s1, "alpha");
EndIf
End
```

together with the compound file \"removeAtom.cmp\" :

```orca
# ----------------------------------------------------
# This is an example script for matrix inversion
# -----------------------------------------------------
%Compound
  Variable Dim=3;
  Variable A[Dim][Dim];
  Variable invertA, C;
  Variable res=-1;
  for i from 0 to Dim-1 Do
    for j from 0 to Dim-1 Do
      if (i=j) then
        A[i][j] = i+1;
      else
        A[i][j] =  0.0;
      EndIf
    EndFor
  EndFor
  invertA = A.invertMatrix();
  A.PrintMatrix(); 
  invertA.PrintMatrix();
  C = Mat_x_Mat(A,invertA,false, false, 1.0, 1.0);
  C.PrintMatrix();
End
```

then the xyz file 'newGeom.xyz' will be created that should look like:

```mol
title: structure 21
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
2
structure
H     2.5974927   -0.4116633    0.7667449
H     2.5931354   -0.4494962   -0.7447820
```

where the atom with *atomIndex = 0* meaning the first atom, meaning the
oxygen is removed.

<a id="sec:workflowsautomatization.compound_detailed.commands.new_geom.remove_elements"></a>
#### Remove_Element

Remove_element is similar to the Remove_atom but instead of using the
index of the atom we use its atomic number. Thus the syntax is:

**Syntax:** NewGeom = ( Remove_Element, atomic number, \"filename\",
stepIndex, [geometry Index]);

where:\
*atomic number* is the atomic number of the atom we want to remove. It
can be an integer number or a variable.\
*filename* is the name of the file that we want to use for the new xyz
file. It can be a string in quotation marks or a variable already
defined before. In the name the xyz extension will be automatically
appended. *step Index* the number of the step from which we will get the
initial geometry. It has to be an integer number. *geometry Index* In
case there are more than one geometries in the corresponding property
file we can choose one. If no number is given but default the program
will use the last one.

**example:**

if we use again the input from paragraph
[1.1.7.2](#sec:workflowsautomatization.compound_detailed.commands.new_geom.remove_atom) but
instead of asking the compound file \"removeAtom.cmp\" we ask for the
compound file \"removeElement.cmp\" that looks like:

```orca
# ----------------------------------------------------
# This is an example script for matrix addition
# -----------------------------------------------------
%Compound
  Variable Dim=3;
  Variable A[Dim][Dim];
  Variable B[Dim][Dim];
  Variable C;
  Variable res=-1;
  for i from 0 to Dim-1 Do
    for j from 0 to Dim-1 Do
      A[i][j] = 1.0;
      B[i][j] = 2.0;
    EndFor
  EndFor
  A.PrintMatrix();
  B.PrintMatrix();
  C = Mat_p_Mat(2.0, A, 3.0, B);
  C.PrintMatrix();
End
```

then we will get again the same xyz file that was crated in paragraph
[new_geom.remove_atom](#sec:workflowsautomatization.compound_detailed.commands.new_geom.remove_atom) since
the atom with atomic number 8 (meaning the Oxygen) will be removed from
the original geometry.

<a id="sec:workflowsautomatization.compound_detailed.commands.newstep"></a>
### NewStep

NewStep signals the beginning of a new ORCA input. 

**Syntax:**

NewStep\
*\...Normal ORCA input commands*\
StepEnd

There is no restriction in the input of ORCA, except of course that it
should not include another Compound block. It is important to remember
that a *NewStep* command should always end with a *Step_End* command.
Below we show a simple example.

**NOTE:** The old syntax (New_Step/Step_End) is still compatible but please do not use it because in the future it will be deprecated.

**Example:**

```orca
NewStep
! BP86 def2-SVP
StepEnd
```

There is only a basic fundamental difference with a normal ORCA input.
Inside the *NewStep* block it is not necessary to include a geometry.
ORCA will automatically try to read the geometry from the previous
calculation. Of course a geometry can be given and then ORCA will use
it.

<a id="sec:workflowsautomatization.compound_detailed.commands.stringrelated.print"></a>
### Print

Printing in the ORCA outpug can be customized using the *print* command.
The syntax of the *print* command closely follows the corresponding
printf command from C/C++. So the usage of the *print* command is:

**Syntax:**\
*print(format string, [variables]);*

For each variable there can be specifiers and flags for the specifiers.
Currently *print* command supports three datatypes namely integers,
doubles and strings.

A format specifier follows this prototype:
*%[flags][width][.precision]specifier*

where details for the specifiers and flags can be found in table
[compoundPrintSpecifiers](#compoundPrintSpecifiers)

<a id="compoundPrintSpecifiers"></a>
!!! note "compound print Specifiers"
    | Specifier |                                       |     |
    |:----------|:--------------------------------------|:----|
    | s         | strings                               |     |
    | d         | integers                              |     |
    | lf        | doubles                               |     |
    |           |                                       |     |
    | Flags     |                                       |     |
    |           |                                       |     |
    | number    | width                                 |     |
    | .number   | number of decimal digits              |     |
    | \-        | left alignement (by default is right) |     |
    |           |                                       |     |

**Example:**

```orca
# ----------------------------------------------------
# This is an example script for matrix multiplication
# -----------------------------------------------------
%Compound
  Variable Dim=3;
  Variable A[Dim][Dim];
  Variable invertA;
  Variable C;
  Variable D;
  Variable res=-1;
  for i from 0 to Dim-1 Do
    for j from 0 to Dim-1 Do
      if (i=j) then
        A[i][j] = i+1;
      else
        A[i][j] =  0.0;
      EndIf
    EndFor
  EndFor
  A.invertMatrix(invertA);
  A.PrintMatrix(); 
  invertA.PrintMatrix();
  C = Mat_x_Mat(A,invertA,false, false, 1.0, 1.0);
  C.PrintMatrix();
  C = Mat_x_Mat(A, invertA, true, true, 1.0, 1.0);
  C.PrintMatrix();
  C = Mat_x_Mat(A, invertA, false, false, 2.0);
  C.PrintMatrix();
  C = Mat_x_Mat(A, invertA, false, false, 2.0, 3.0);
  C.PrintMatrix();
End
```

<a id="sec:workflowsautomatization.compound_detailed.commands.propertyFile.readProperty"></a>
### ReadProperty
One of the fundamental features of *Compound* is the ability to easily read ORCA calculated values from the property file.

**Syntax:**

*[res=] readProperty(propertyName=myName, [stepID=myStep], [filename=myFilename], [baseProperty=true/false])*

*Where:*
*res:* An integer that returns the index of the found property if the property was found in the property file, -1 if the property does not exist. This is not obligatory.

*propertyName:* A string alias that defines the variable the user wants to read.

*stepID:* The step from which we want to read the property. If not given the property file from the last step will be read.

*filename:* A filename of a property file. If a filename and at the same time a step are provided the program will ignore the step and try to read the property file with the given filename. 

**NOTE** please note that in the end of filename the extension *.property.txt* will be added.

*baseProperty:* A true/false boolean. The default value is set to false. If the value is set to true then a generic property of the type asked will be read. This means if dipole moment is asked, it will return the last dipole moment, irrelevant if and MP2 or SCF one wad defined.

 **Example**
```orca
# ----------------------------------------------------
# This is an example script for matrix times scalar 
# -----------------------------------------------------
%Compound
  Variable Dim=3;
  Variable A[Dim][Dim];
  Variable alpha=2.0;
  Variable C;
  for i from 0 to Dim-1 Do
    for j from 0 to Dim-1 Do
        A[i][j] = i+j;
    EndFor
  EndFor
  A.PrintMatrix();
  C = Mat_x_Scal(alpha,A);
  A = Mat_x_Scal(alpha,A);
  A.PrintMatrix();
  C.PrintMatrix();
End
```

<a id="sec:workflowsautomatization.compound_detailed.commands.read_geom"></a>
### Read_Geom

Read_Geom will read the geometry from a previous step.

**Syntax:**\
Read_Geom $number$

Here number is the number of the job that we want to read the geometry
from. The directive should be positioned before a *NewStep* -
*StepEnd* block.

**Example:**

```orca
#Compound Job 1
New_Step
!BP86 def2-SVP
Step_End

#Compound Job 2
New_Step
!BP86 def2-SVP opt
Step_End

#Compound Job 3
Read_Geom 1
New_Step
!CCSD  def2-SVP
Step_End

End  #Final End
```

In this case the third calculation, through the *Read_MGeom 1* command,
will read the geometry from the first calculation.

<a id="sec:workflowsautomatization.compound_detailed.commands.orca.readMOs"></a>
### ReadMOs

ReadMOs reads the molecular orbitals from a previous step.

**Syntax:**\
*ReadMOs(stepNumber);*

Where:

- *stepNumber:* is the number of the step from which we want to read the orbitals.

**Example:**
```orca
# Define variables
		Variable MaxNTries    =  25; 
		Variable CutOff       = -50;
		Variable displacement = 0.6;
		Variable NNegative =   0;  
		Variable freqs[];
		Variable modes[];
		Variable NFreq;
		Variable limit;
		Variable done;
		Variable FinalEnergy; 
		
		# ===========================================================
		# Start a for loop over number of tries
		# ===========================================================
		For itry From 1 To maxNTries Do
		
		# ----------------------------------
		# Run a geometry optimization
		# ----------------------------------
		New_Step
		! tightopt freq verytightscf nopop def2-TZVP xyzfile
		Step_End
		Read freqs  = THERMO_FREQS[itry];
		Read modes  = HESSIAN_MODES[itry];
		Read NFreq  = THERMO_NUM_OF_FREQS[itry];
		limit = NFreq - 1;
		# ----------------------------------
		#  check for sufficeintly negative 
		#  frequencies
		# ----------------------------------
		NNegative = 0;
		For ifreq From 0 to limit Do
		if ( freqs[ifreq] < CutOff )  then
		New_Geom = (Displace, itry,  modes,  ifreq, displacement);
```

<a id="sec:workflowsautomatization.compound_detailed.commands.stringrelated.getBasename"></a>
### S.GetBasename

In *Compound* strings have all the functionality of a normal variable. In addition they have some additional functions that act only on strings. On of these functions is the function *GetBasename*. This function searches the string and if it contains a dot it will return the part of the string before the dot. 

**Syntax:**

*result = source.GetBasename();*

*Where:*

*result* is the returned string.

*source* is the original string.

**NOTE** If the original string contains no dot then the result string will be a copy of the source one.

**Example:**

```orca
%Compound 

# -------------------------------------------------------------
#      This is to check all available open and close 
#                file options 
# -------------------------------------------------------------
Variable myFilename    = "myFile.txt";
Variable file;

# ---------------------------
# First open for writing
# ---------------------------
file = openFile(myFilename, "w");
write2File(file, "This is the first time we write.\n");
closeFile(file);

# ---------------------------
# Re-open to append
# ---------------------------
file = openFile(myFilename, "a");
write2File(file, "This is the second time we write.\n");
closeFile(file);

End
```
<a id="sec:workflowsautomatization.compound_detailed.commands.stringrelated.getChar"></a>
### S.GetChar

In *Compound* strings have all the functionality of a normal variable. In addition they have some additional functions that act only on strings. On of these functions is the function *GetChar*. This function searches the string and if it contains a dot it will return the part of the string after the dot. 

**Syntax:**

*result = source.GetChar(index);*

*Where:*

*result* is the returned string.

*index* is the index of the curracter in the string. Keep in mind that counting starts with **0** and not 1.

*source* is the original string.

**NOTE** If the index is larger than the size of the string or negative then the program will exit. 

**Example:**

```mol
title: structure 22
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
3
structure (0 1)
O   2.220871067  0.026716792  0.000620476
H   2.597492682 -0.411663274  0.766744858
H   2.593135384 -0.449496183 -0.744782026
--- input ---
*xyz 0 1 
O	 2.220871067	 0.026716792	 0.000620476
H	 2.597492682	-0.411663274	 0.766744858
H	 2.593135384	-0.449496183	-0.744782026
*

%Compound "removeAtom.cmp"
```

<a id="sec:workflowsautomatization.compound_detailed.commands.stringrelated.getSuffix"></a>
### S.GetSuffix

In *Compound* strings have all the functionality of a normal variable. In addition they have some additional functions that act only on strings. On of these functions is the function *GetSuffix*. This function searches the string and if it contains a dot it will return the part of the string after the dot. 

**Syntax:**

*result = source.GetSuffix();*

*Where:*

*result* is the returned string.

*source* is the original string.

**NOTE** If the original string contains no dot then the result string will be an empty string.

**Example:**

```orca
Variable filename  = "newGeom";
Variable atomIndex = 0;

New_Step
  !BP86
Step_End

New_Geom = ( Remove_atom, atomIndex, filename, 1);

end
```

<a id="sec:workflowsautomatization.compound_detailed.commands.endstep"></a>
### StepEnd

StepEnd signals the end of an ORCA Input. It should always be the last
directive of an ORCA input inside the compound block that starts with
*New_Step* (see paragraph
[commands.newstep](#sec:workflowsautomatization.compound_detailed.commands.newstep))

**NOTE:** The old syntax (New_Step/Step_End) is still compatible but please do not use it because in the future it will be deprecated.

<a id="sec:workflowsautomatization.compound_detailed.commands.syscmd"></a>
### Sys_cmd

Sys_cmd will read a system command and execute it.

**Syntax:**\
Sys_cmd *command*

**Example:**

```orca
SYS_CMD "orca_mapspc test.out SOCABS -x0700 -x1900 -w0.5 -eV -n10000 "
```

<a id="sec:workflowsautomatization.compound_detailed.commands.timerrelated.timer"></a>
### Timer

A *timer* is an object that can keep time for tasks in compound. Before a timer object is used it has to be declared. The declaration of a *timer* is slightly different that the rest of variables, because it has to explicitly declare it's type.

**Syntax**

*timer myTimer;*

*where* 

*timer* is used instead of the normal *variable* command to explicitly set the variable type to *compTimer*.

*myTimer* is a normal instance of the object.

**Example:**

```mol
title: structure 23
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
2
structure
H     2.5974927   -0.4116633    0.7667449
H     2.5931354   -0.4494962   -0.7447820
```

Below is a lit of functions that work exclusively on *Timer* objects. 

- Last ([timer.last](#sec:workflowsautomatization.compound_detailedd.commands.timer.last))

- Reset ([timer.reset](#sec:workflowsautomatization.compound_detailedd.commands.timer.reset))

- Start ([timer.start](#sec:workflowsautomatization.compound_detailedd.commands.timer.start))

- Stop ([timer.stop](#sec:workflowsautomatization.compound_detailedd.commands.timer.stop))

- Total ([timer.total](#sec:workflowsautomatization.compound_detailedd.commands.timer.total))

<a id="sec:workflowsautomatization.compound_detailedd.commands.timer.last"></a>
### T.Last 

Last is a function that works on a *timer* object. It returns, as a real number, the last value of the timer.

**Syntax**

*myTimer.Last();*

*Where:*

*myTimer:* is the *timer* object initialized before.

**Example:**

```orca
Variable filename  = "newGeom";

New_Step
  !BP86
Step_End

New_Geom = ( Remove_element, 8, filename, 1);

end
```
**NOTE** Before using last the *timer* object must, beside defined, be also initializee, using *Start* (see [timer.start](#sec:workflowsautomatization.compound_detailedd.commands.timer.start))

<a id="sec:workflowsautomatization.compound_detailedd.commands.timer.reset"></a>
### T.Reset 

*Reset* is a function that works on a *timer* object. It resets the *timer* object to its initial state.

**Syntax**

*myTimer.Reset();*

*Where:*

*myTimer:* is the *timer* object initialized before.

**Example:**

```orca
NewStep
! BP86 def2-SVP
StepEnd
```

<a id="sec:workflowsautomatization.compound_detailedd.commands.timer.start"></a>
### T.Start 

*Start* is a function that works on a *timer* object. It retunrs the *timer* object to its initial state.

**Syntax**

*myTimer.Start();*

*Where:*

*myTimer:* is the *timer* object initialized before.

**Example:**

```orca
# -------------------------------------------------------------
# This is to check all available print defintions 
# -------------------------------------------------------------
Variable x1    = 2.0;                        
Variable x2    = {10.0, 20.0, 30.0, 40.0};
Variable x3    = {10,   20,   30,   40};
Variable x4    = {"ten", "twenty", "thirty", "fourty"};
Variable x5 = "test";
Variable index = 2;

print( " --------------------------------------------- \n");
print( " ------ SUMMARY OF PRINT DEFINITIONS --------- \n");
print( " --------------------------------------------- \n");
# ---------- No variables ------------
print( " No variables: \n" );
# ------------- Doubles --------------
print( " -------- Doubles --------------\n");
print( " constant double ( no format)             : %lf\n", 3.5);
print( " constant double (defined width)          : %16lf\n",3.5);
print( " constant double (defined width/accuracy) : %16.8lf\n", 3.5);
print( " variable double (x1)                     : %lf\n", x1);
print( " function double 2*x1*x1                  : %lf\n", 2*x1*x1);
print( " array element double                     : %lf\n", x2[2]);
print( " array element double with var index      : %lf\n", x2[index]);
#print( " array element double with function index : %lf\n", x2[index + 1];
# ------------ Integers --------------
print( " -------- Integers --------------\n");
print( " constant integer ( no format)            : %d\n", 3);
print( " constant integeer (defined width)        : %8d\n",3);
print( " variable integer (index)                 : %d\n", index);
print( " function integer 2*index*index           : %d\n", 2*index*index);
print( " array element                            : %d\n", x3[2]);
print( " array element intteger with var index    : %lf\n",x3[index]);
# ------------  Strings --------------
print( " -------- Strings --------------\n");
print( " constant string ( no format)             : %s\n", "test");
print( " constant string (defined width)          : %8s\n","test");
print( " variable string                          : %s\n", x5);
print( " array element                            : %s\n", x4[2]);
print( " array element intteger with var index    : %s\n",x4[index]);
print(" ----------------------------------------------\n");
print(" ----------------------------------------------\n"); 
End
```

<a id="sec:workflowsautomatization.compound_detailedd.commands.timer.stop"></a>
### T.Stop

*Stop* is a function that works on a *timer* object. It stops the timer from counting.

**Syntax**

*myTimer.Stop();*

*Where:*

*myTimer:* is the *timer* object initialized before.

**Example:**

```mol
title: structure 24
theme: chem311
height: 320px
representation: ball-stick
--- xyz ---
2
structure (0 1)
H           0.0          0.0          0.0
H           0.0          0.0          0.8
--- input ---
# ----------------------------------------------------
# This is an example script for readProperty
# -----------------------------------------------------
%Compound
  Variable enDirect=0.0;
  Variable enFilename=0.0;
  Variable myProperty="DFT_Total_en";
  Variable basename="compound_example_properertFile_readProperty";
  Variable newBasename ="newFilename";
  Variable res = -1;
  NewStep
    !BP86
    *xyz 0 1
      H 0.0 0.0 0.0
      H 0.0 0.0 0.8
    *
  StepEnd
  NewStep
    !B3LYP
  StepEnd
  # First read the energy directly
  res = enDirect.ReadProperty(propertyName=myProperty, stepID=2);
  print("res : %d\n", res);
  # Now read the same energy through filename
  SysCmd("cp %s_Compound_2.property.txt %s.property.txt", basename, newBasename);
  enFilename.ReadProperty(propertyName=myProperty, filename=newBasename);
  print(" Energy direct    : %.9lf\n", enDirect);
  print(" Energy from file : %.9lf\n", enFilename);
  print("Difference between 2 energies : %.12lf\n", enDirect-enFilename);
End
```

<a id="sec:workflowsautomatization.compound_detailedd.commands.timer.total"></a>
### T.Total 

*Total* is a function that works on a *timer* object. It returns a real number with the total time.

**Syntax**

*myTimer.Total();*

*Where:*

*myTimer:* is the *timer* object initialized before.

**Example:**

```orca
#Compound Job 1
New_Step
!BP86 def2-SVP
Step_End

#Compound Job 2
New_Step
!BP86 def2-SVP opt
Step_End

#Compound Job 3
Read_Geom 1
New_Step
!CCSD  def2-SVP
Step_End

End  #Final End
```

<a id="sec:workflowsautomatization.compound_detailed.commands.variables.general"></a>
### Variables - General

Everything in the *Compound* language is based on variables. Their meaning and usage are similar to those in any programming language: you need to declare a variable and then assign a value to it. Notably, in *Compound*, a variable must be declared before it is assigned a value, following the syntax rules of languages like C. This differs from languages like Python, where you can assign a value to a variable without prior declaration. The only exception to this rule in Compound is the index in a for loop, which does not require prior declaration.

In *Compound* we support the following data types for variables:

-   Integer

-   Double

-   String

-   Boolean

-   File pointer

In addition to these data types *Compound* supports also variables of type *Geometry* and *Timer* but these are treated separately
(see [commands.geometry](#sec:workflowsautomatization.compound_detailed.commands.geometry) and [timerrelated.timer](#sec:workflowsautomatization.compound_detailed.commands.timerrelated.timer)).

For each variable in *Compound* there are 3 major categories of usage:

- The declaration (see [variables.general](#sec:workflowsautomatization.compound_detailed.commands.variables.general))
  
- The assignement (see [variables.assignement](#sec:workflowsautomatization.compound_detailed.commands.variables.assignement)) and 
  
- Variable functions (see [variables.functions](#sec:workflowsautomatization.compound_detailed.commands.variables.functions))

<a id="sec:workflowsautomatization.compound_detailed.commands.variables.declaration"></a>
### Variables - Declaration

There are currently 6 different ways to declare a variable in
*Compound*. Their syntax is the following:

**Syntax:**

**A.** *Variable name;*

**B.** *Variable name1, name2;*

**C.** *Variable name=value;*

**D.** *Variable name[$n$];*

**E.** *Variable name[$n1$][$n2$];*

**F.** *Variable name={value1, value2, \...}*;

**NOTE** In previous versions of *Compound* for variables that were matrices but the size was not known one had to declare the variable using the following syntax:

*Variable name = [];*

This is now changed and the empty brackets are no longer needed, so that this variable can be defined like a normal variable as in case *A*.

**Example**

```orca
# ----------------------------------------------------
# This is an example script for ReadMOs
# -----------------------------------------------------
%Compound
  Variable step = 1;
  New_Step
    !BP86
    *xyzfile 0 1 h2o.xyz
  Step_End

  ReadMOs(step);
  New_Step
    !BP86
  Step_End
End
```

Some comments for the different cases of variable declaration.\
**Case A** is the simplest one were we just declare the name of a variable.

**Case B** is similar to *Case A* but here more than one variables are
declared simultaneously.

In **Case C** we combine the variable declaration with the assignment of a
value to the variable. It worth noting that in this case *Compound*
automatically deducts the type of the variable based on the given value.

**Case D** declares a 1-Dimensional array of a defined size.

**Case E** declares a 2-Dimensional array of defined size. For this case, and
also accordingly for *Case E*, one can use previously defined integer
variables instead of numbers.

**Case F** defines an array based on a list of given values. The array will
automatically define it's size based on the size of the list. The values
in the list do not have to be all of the same type. 

**NOTE** In the past for *Case F* empty brackets were needed after the name of the variable. This is no longer necessary.

**NOTE** It is important not to forget the final **;** symbol in the end of
each declaration because the result of omitting it is undefined.

<a id="sec:workflowsautomatization.compound_detailed.commands.variables.assignement"></a>
### Variables - Assignment

Assigning a value to a variable has a rather straightforward syntax.

**Syntax:**\
*VariableName = CustomFunction;*

*Where:*

*VariableName* is a variable already declared.

*CustomFunction* a mathematical expression. 

**Example:**

```orca
# ------------------------------------------------------
# This is an example script for string related functions:
#    - GetBasename
#    - GetSuffix
#    - GetChar
# ------------------------------------------------------
%Compound
  Variable original = "lala.xyz";
  Variable basename, suffix;
  Variable constructed = "";
  basename = original.GetBasename();
  suffix   = original.GetSuffix();
  for i from 0 to original.stringlength()-1 Do
    write2String(constructed,"%s%s", constructed, original.GetChar(i));
  endfor
  print("Original    : %s\n", original);
  print("Basename    : %s\n", basename);
  print("Sufix       : %s\n", suffix);
  print("Constructed : %s\n", constructed);
End
```

**NOTE** It is important to remember to finish the variable assignment using the **';'** symbol.

<a id="sec:workflowsautomatization.compound_detailed.commands.variables.functions"></a>
### Variables - Functions

Variables in *Compound* have a small number of functions that can help
exctract information about them. In the current version of *Compound*
these functions are the following:

**Syntax:**\
VariableName.Function();

where *VariableName* is a variable that is already declared. Then the
function will return a value that depends on the *Function* that we
used.

Currenlty *Compound* supports the following functions:

-  GetBool() [functions.getBool](#sec:workflowsautomatization.compound_detailed.commands.variables.functions.getBool) 
-  GetDim1() [functions.getDim1](#sec:workflowsautomatization.compound_detailed.commands.variables.functions.getDim1) 
-  GetDim2() [functions.getDim2](#sec:workflowsautomatization.compound_detailed.commands.variables.functions.getDim2) 
-  GetDouble() [functions.getDouble](#sec:workflowsautomatization.compound_detailed.commands.variables.functions.getDouble) 
-  GetInteger() [functions.getInteger](#sec:workflowsautomatization.compound_detailed.commands.variables.functions.getInteger) 
-  GetSize() [functions.getSize](#sec:workflowsautomatization.compound_detailed.commands.variables.functions.getSize) 
-  GetString() [functions.getString](#sec:workflowsautomatization.compound_detailed.commands.variables.functions.getString) 
-  PrintMatrix() [functions.printMatrix](#sec:workflowsautomatization.compound_detailed.commands.variables.functions.printMatrix) 
  
**Example:**

```orca
# ------------------------------------------------------
# This is an example script for string related functions:
#    - GetBasename
#    - GetSuffix
#    - GetChar
# ------------------------------------------------------
%Compound
  Variable original = "lala.xyz";
  Variable basename, suffix;
  Variable constructed = "";
  basename = original.GetBasename();
  suffix   = original.GetSuffix();
  for i from 0 to original.stringlength()-1 Do
    write2String(constructed,"%s%s", constructed, original.GetChar(i));
  endfor
  print("Original    : %s\n", original);
  print("Basename    : %s\n", basename);
  print("Sufix       : %s\n", suffix);
  print("Constructed : %s\n", constructed);
End
```

<a id="sec:workflowsautomatization.compound_detailed.commands.variables.functions.getBool"></a>
### V.GetBool()

This function will return a boolean value in case the variable is boolean or integer. For integers it will return *false* for 0 and *true* for all other integer values. In all other cases the program will crash providing a relevant message.

**Syntax:**

*myVar.GetBool();*

*where:* 

*myVar* is an already initialized variable.

**Example**

```orca
# ------------------------------------------------------
# This is an example script for string related functions:
#    - GetBasename
#    - GetSuffix
#    - GetChar
# ------------------------------------------------------
%Compound
  Variable original = "lala.xyz";
  Variable basename, suffix;
  Variable constructed = "";
  basename = original.GetBasename();
  suffix   = original.GetSuffix();
  for i from 0 to original.stringlength()-1 Do
    write2String(constructed,"%s%s", constructed, original.GetChar(i));
  endfor
  print("Original    : %s\n", original);
  print("Basename    : %s\n", basename);
  print("Sufix       : %s\n", suffix);
  print("Constructed : %s\n", constructed);
End
```

<a id="sec:workflowsautomatization.compound_detailed.commands.variables.functions.getDim1"></a>
### V.GetDim1()

 This function works on a variable. It will return the size of the first dimension of an array. If the variable is a scalar it will return 1.

**Syntax:**

*myVar.GetDim1();*

*where:* 

*myVar* is an already initialized variable.

**Example**

```orca
SYS_CMD "orca_mapspc test.out SOCABS -x0700 -x1900 -w0.5 -eV -n10000 "
```

<a id="sec:workflowsautomatization.compound_detailed.commands.variables.functions.getDim2"></a>
### V.GetDim2()

This function works on a variable. It will return the size of the second dimension of an array. If the variable is a scalar or a 1-Dimensional array it will return 1.

**Syntax:**

*myVar.GetDim2();*

*where:* 

*myVar* is an already initialized variable.

**Example**

```orca
# -----------------------------------------------
# This is to test timer functions.  
# --------------------------------
timer tm;
Variable x = 0.0;
tm.start();
for index from 0 to 100000 Do
  x = x + 0.1;
EndFor
tm.stop();
x = tm.Total();
print( "------------------------------\n");
print( "   Compound - Timer Results   \n");
print( "------------------------------\n");
print( " First total time:   %.2lf\n", x); 

x = tm.total();
tm.Reset();
tm.Start();
for index from 0 to 200000 Do
  x = x + 0.1;
EndFor
tm.Stop();
x = tm.total();

print( " Second total time:   %.2lf\n", x); 
End
```

<a id="sec:workflowsautomatization.compound_detailed.commands.variables.functions.getDouble"></a>
### V.GetDouble()

This function works on a variable. It will return a double value in case the variable is integer or double. In all other cases the program will crash providing a relevant message.

**Syntax:**

*myVar.GetDouble();*

*where:* 

*myVar* is an already initialized variable.

**Example**

```orca
# -----------------------------------------------
# This is to test timer functions.  
# --------------------------------
timer tm;
Variable x = 0.0;
tm.start();
for index from 0 to 100000 Do
  x = x + 0.1;
EndFor
tm.stop();
x = tm.Total();
print( "------------------------------\n");
print( "   Compound - Timer Results   \n");
print( "------------------------------\n");
print( " First total time:   %.2lf\n", x); 

x = tm.total();
tm.Reset();
tm.Start();
for index from 0 to 200000 Do
  x = x + 0.1;
EndFor
tm.Stop();
x = tm.total();

print( " Second total time:   %.2lf\n", x); 
End
```

<a id="sec:workflowsautomatization.compound_detailed.commands.variables.functions.getInteger"></a>
### V.GetInteger()
This function works on a variable. It will return an integer value in case the variable is integer or double. In all other cases the program will crash providing a relevant message.

**Syntax:**

*myVar.GetInteger();*

*where:* 

*myVar* is an already initialized variable.

**Example**

```orca
# -----------------------------------------------
# This is to test timer functions.  
# --------------------------------
timer tm;
Variable x = 0.0;
tm.start();
for index from 0 to 100000 Do
  x = x + 0.1;
EndFor
tm.stop();
x = tm.Total();
print( "------------------------------\n");
print( "   Compound - Timer Results   \n");
print( "------------------------------\n");
print( " First total time:   %.2lf\n", x); 

x = tm.total();
tm.Reset();
tm.Start();
for index from 0 to 200000 Do
  x = x + 0.1;
EndFor
tm.Stop();
x = tm.total();

print( " Second total time:   %.2lf\n", x); 
End
```

<a id="sec:workflowsautomatization.compound_detailed.commands.variables.functions.getSize"></a>
### V.GetSize()

This function works on a variable. If the variable is a scalar it will return 1. If the variable is a 1-Dimensional array it will return the size of the array which is the same with the *GetDim1()* . If the variable is a 2-Dimensional array it will return the results Dim1\*Dim2.

**Syntax:**

*myVar.GetSize();*

*where:* 

*myVar* is an already initialized variable.

**Example**

```orca
# -----------------------------------------------
# This is to test timer functions.  
# --------------------------------
timer tm;
Variable x = 0.0;
tm.start();
for index from 0 to 100000 Do
  x = x + 0.1;
EndFor
tm.stop();
x = tm.Total();
print( "------------------------------\n");
print( "   Compound - Timer Results   \n");
print( "------------------------------\n");
print( " First total time:   %.2lf\n", x); 

x = tm.total();
tm.Reset();
tm.Start();
for index from 0 to 200000 Do
  x = x + 0.1;
EndFor
tm.Stop();
x = tm.total();

print( " Second total time:   %.2lf\n", x); 
End
```

<a id="sec:workflowsautomatization.compound_detailed.commands.variables.functions.getString"></a>
### V.GetString()
This function works on a variable. It will return a string of the value of the variable. It works for doubles, integers and booleans.

**Syntax:**

*myVar.GetString();*

*where:* 

*myVar* is an already initialized variable.

**Example**

```orca
# -----------------------------------------------
# This is to test timer functions.  
# --------------------------------
timer tm;
Variable x = 0.0;
tm.start();
for index from 0 to 100000 Do
  x = x + 0.1;
EndFor
tm.stop();
x = tm.Total();
print( "------------------------------\n");
print( "   Compound - Timer Results   \n");
print( "------------------------------\n");
print( " First total time:   %.2lf\n", x); 

x = tm.total();
tm.Reset();
tm.Start();
for index from 0 to 200000 Do
  x = x + 0.1;
EndFor
tm.Stop();
x = tm.total();

print( " Second total time:   %.2lf\n", x); 
End
```

<a id="sec:workflowsautomatization.compound_detailed.commands.variables.functions.printMatrix"></a>
### V.PrintMatrix()
This function works on variables. It will print print an array on a format with 8 columns.

**Syntax:**
*myVar.PrintMatrix([NCols=numOfColumns]);*

*where:* 

*myVar* is an already initialized variable.

*numOfColumns* is the desired number of columns for the printing. This is not obligatory and if not used then by default ORCA will print using **4** columns.

**Example**

**Example:**
```orca
# -----------------------------------------------
# This is to test timer functions.  
# --------------------------------
timer tm;
Variable x = 0.0;
tm.start();
for index from 0 to 100000 Do
  x = x + 0.1;
EndFor
tm.stop();
x = tm.Total();
print( "------------------------------\n");
print( "   Compound - Timer Results   \n");
print( "------------------------------\n");
print( " First total time:   %.2lf\n", x); 

x = tm.total();
tm.Reset();
tm.Start();
for index from 0 to 200000 Do
  x = x + 0.1;
EndFor
tm.Stop();
x = tm.total();

print( " Second total time:   %.2lf\n", x); 
End
```
**NOTE** In case of scalars it will only print the header without any values.

**NOTE** It only works for arrays of type *'double'* or type *'integer'*. With all variables of other types the program will exit providing an error message.

<a id="sec:workflowsautomatization.compound_detailed.commands.variables.with"></a>
### With

The purpose of the \"with\" command is to add the ability to call
compound while adjusting some of the variables that are already defined
in the compound file. This means that if there is a variable defined in
the compound file and a value is assigned to it, we can during the call
change the assigned value of this variable.

One can pass numbers, string or boolean variables.

It should be noted that it is not possible to call array variables this
way. Beside this restriction, the syntax of the variable assignment in
the case of with is the same with the variable assignment in a normal
*Compound* script.

An important note here is that in case we use the *With* command the
*%Compound* block should end with an *'End'* even if we call a
*Compound* script file.\
**Syntax:**\
**% compound** *\"filename\"*\
**With**\
*var1* = *val1*;\
*var2* = *val2*;\
**End**\
**Example:**

```orca
# -------------------------------------------------------------
# This is to check all available ways of 
#   Variable declaration in Compound
# -------------------------------------------------------------
Variable size = 5;
Variable x1;                              #caseA
Variable x2,x3;                           #caseB
Variable x4 = 1.0;                        #caseC
Variable x5 = 0;                          #caseC
Variable x6 = "Test";                     #caseC
Variable x7 = True;                       #caseC
Variable x8 = 2*x4;                       #caseC
Variable x9 = x6;                         #caseC
Variable x10 = x7;                        #caseC
Variable x11;                             #caseA
Variable x12[3];                          #caseD
Variable x12b[size-2];                    #caseD
Variable x12c[size][size-1];              #caseE
x12b[1] = 4.0;
x12c[2][2] = 7.0;
Variable x13[3][3];                       #caseE
Variable x14 = {2.0, 4*x4, 2, "lala"};    #caseF
Variable x15 = {0, 1, 2, 3, 4};
Variable x15b = {0, 1, 2, 3, 4};
Variable x15c[x15[x15b[2]-1]+2]; 
Variable x16, x17=x10, x18;
Variable x19=2.0, x20, x21[2], x23[size][size];
print( " --------------------------------------------- \n");
print( " ---------- SUMMARY OF DEFINITIONS ----------- \n");
print( " --------------------------------------------- \n");
print( " x4 (1.0)          :  %.2lf\n", x4);
print( " x5 (0)            :  %.2d\n",  x5);
print( " x6 (\"Test\")       :  %s\n",    x6);
if (x7) then 
  print(" x7 (True)         :  TRUE\n");
else
  print(" x7 (True)         :  FALSE\n");
endIf
print(" x8 (2*x4)         :  %.2lf\n", x8);
print(" x9 (x6)           :  %s\n", x9);
print(" x12b[1] (4.0)     :  %lf\n", x12b[1]);
print(" x12c[2][2] (7.0)  :  %lf\n", x12c[2][2]);
print(" Variable x14 = {2.0, 4*x4, 2, \"lala\"};\n");
print(" x14[0]            :  %lf\n", x14[0]);
print(" x14[1]            :  %lf\n", x14[1]);
print(" x14[2]            :  %d\n",  x14[2]);
print(" x14[3]            :  %s\n",  x14[3]);
print(" Variable x15  = {0, 1, 2, 3, 4};\n");
print(" Variable x15b = {0, 1, 2, 3, 4};\n");
print(" Variable x15c[x15[x15b[2]-1]+2];\n"); 
print(" x15c.GetSize()    :  %d\n",  x15c.GetSize());
print(" ----------------------------------------------\n");
print(" ----------------------------------------------\n"); 
End
```

<a id="sec:workflowsautomatization.compound_detailed.commands.stringrelated.write2file"></a>
### Write2File

With the *Print* command (see [stringrelated.print](#sec:workflowsautomatization.compound_detailed.commands.stringrelated.print)) one can write in the ORCA output. Nevertheless
it might be that one would prefer to write to a different file. In
*Compound* one can achieve this using the *write2File* command. The
syntax follows closely the syntax of 'fprintf' command of the
programming language C. The arguments definition and the syntax is
identical with the syntax of the *Compound 'Print'* command with the
addition that one should define a file object to send the printing.

**Syntax:**\
*Write2File(file variable, format string, [variables]);*

*Where:*

*file variable:* is a predefined variable corresponding to an
already open, through the *OpenFile* command, file. 

*format string* and *variables* follow exactly the syntax of the *Print* command, so for
more details please refere to section [stringrelated.print](#sec:workflowsautomatization.compound_detailed.commands.stringrelated.print).

**NOTE** Please remember once everything is writen to the file to close the file, using the
*CloseFile* command (see [commands.closeFile](#sec:workflowsautomatization.compound_detailed.commands.closeFile)).

**Example:**

```orca
# -------------------------------------------------------------
# This is to check all available ways of variable assignement
#   (It does not take care of 'with' we will have a separate
#         file for this)
# -------------------------------------------------------------

# -----------------------------------
# Some necessary initial declarations
# -----------------------------------
Variable x1, x2, x3, x4;  
Variable y1, y2, y3, y4;
Variable x5[4]; 
Variable y5[4];                        
Variable x6[3][3];                      
Variable y6[3][3];

# -----------------------------------
# Now the assignements
# -----------------------------------
#Scalars doubles
x1 = 1.0;
y1 = 2*x1;
#Scalars integers
x2 = 1;
y2 = 2*x2;
#Scalars strings
x3 = "test";
y3 = x3;
#Scalars bools
x4 = True;
y4 = x4;
#1D Arrays
x5[0] = 2.0;
y5[0] = x5[0];
x5[1] = 1;
y5[1] = 2*x5[1];
x5[2] = "test";
y5[2] = x5[2];
x5[3] = True;
y5[3] = x5[3];
#2D Arrays
x6[0][0] = 1.0;
y6[0][0] = 2*x6[0][0];
print( " --------------------------------------------- \n");
print( " ---------- SUMMARY OF ASSIGNMENTS ---------- \n");
print( " --------------------------------------------- \n");
print( " ---------------- Scalars -------------------- \n");
print( " x1         :  %.2lf\n", x1);
print( " y1         :  %.2lf\n", y1);
print( " x2         :  %d\n", x2);
print( " y2         :  %d\n", y2);
print( " x3         :  %s\n", x3);
print( " y3         :  %s\n", y3);
print( " ---------------- 1D - Arrays----------------- \n");
print( " x5[0]      :  %.2lf\n", x5[0]);
print( " y5[0]      :  %.2lf\n", y5[0]);
print( " x5[1]      :  %d\n", x5[1]);
print( " y5[1]      :  %d\n", y5[1]);
print( " x5[2]      :  %s\n", x5[2]);
print( " y5[2]      :  %s\n", y5[2]);
print( " ---------------- 2D - Arrays----------------- \n");
print( " x6[0][0]   :  %lf\n", x6[0][0]);
print( " y6[0][0]   :  %lf\n", y6[0][0]);
print(" ----------------------------------------------\n");
print(" ----------------------------------------------\n"); 
End
```

<a id="sec:workflowsautomatization.compound_detailed.commands.stringrelated.write2string"></a>
### Write2String

In case one needs to construct a string using some variables, *Compound* provides the *Write2String* command. The syntax of the
command is identical with the *Write2File* (see [stringrelated.write2file](#sec:workflowsautomatization.compound_detailed.commands.stringrelated.write2file))
command with the only
exception that instead of a file we should provide the name of a
variable that is already declared in the file. The syntax of the format
and the variables used is identical with the *Print* command (please
refer to [stringrelated.print](#sec:workflowsautomatization.compound_detailed.commands.stringrelated.print). )

**Syntax:**

*Write2String(variable, format string, [variables]);*

*where:*

*variable:* is the name of a variable that should already be declared.

*format string* and *variables* follow exactly the syntax of the *Print* command, so for
more details please refer to section [stringrelated.print](#sec:workflowsautomatization.compound_detailed.commands.stringrelated.print).

**Example:**

```orca
# -------------------------------------------------------------
# This is to check all available ways of variable assignement
#   (It does not take care of 'with' we will have a separate
#         file for this)
# -------------------------------------------------------------

# -----------------------------------
# Some necessary initial declarations
# -----------------------------------
Variable x1, x2, x3, x4;  
Variable y1, y2, y3, y4;
Variable x5[4]; 
Variable y5[4];                        
Variable x6[3][3];                      
Variable y6[3][3];

# -----------------------------------
# Now the assignements
# -----------------------------------
#Scalars doubles
x1 = 1.0;
y1 = 2*x1;
#Scalars integers
x2 = 1;
y2 = 2*x2;
#Scalars strings
x3 = "test";
y3 = x3;
#Scalars bools
x4 = True;
y4 = x4;
#1D Arrays
x5[0] = 2.0;
y5[0] = x5[0];
x5[1] = 1;
y5[1] = 2*x5[1];
x5[2] = "test";
y5[2] = x5[2];
x5[3] = True;
y5[3] = x5[3];
#2D Arrays
x6[0][0] = 1.0;
y6[0][0] = 2*x6[0][0];
print( " --------------------------------------------- \n");
print( " ---------- SUMMARY OF ASSIGNMENTS ---------- \n");
print( " --------------------------------------------- \n");
print( " ---------------- Scalars -------------------- \n");
print( " x1         :  %.2lf\n", x1);
print( " y1         :  %.2lf\n", y1);
print( " x2         :  %d\n", x2);
print( " y2         :  %d\n", y2);
print( " x3         :  %s\n", x3);
print( " y3         :  %s\n", y3);
print( " ---------------- 1D - Arrays----------------- \n");
print( " x5[0]      :  %.2lf\n", x5[0]);
print( " y5[0]      :  %.2lf\n", y5[0]);
print( " x5[1]      :  %d\n", x5[1]);
print( " y5[1]      :  %d\n", y5[1]);
print( " x5[2]      :  %s\n", x5[2]);
print( " y5[2]      :  %s\n", y5[2]);
print( " ---------------- 2D - Arrays----------------- \n");
print( " x6[0][0]   :  %lf\n", x6[0][0]);
print( " y6[0][0]   :  %lf\n", y6[0][0]);
print(" ----------------------------------------------\n");
print(" ----------------------------------------------\n"); 
End
```
<a id="sec:workflowsautomatization.compound_detailed.knownProperties"></a>
## List of known Properties

The name and a sort explanation of all the known variables that can be
automatically recovered, from the property file, are given in the next
table:

<a id="tab:knownVariables"></a>
!!! note "Variables, known to the compound block, with short explanation"
    | Keyword | Description |
    |---|---|
    | `AUTOCI_REF_ENERGY` | AutoCI Reference Energy |
    | `AUTOCI_CORR_ENERGY` | AutoCI Correlation Energy |
    | `AUTOCI_TOTAL_ENERGY` | AutoCI Total Energy |
    | === Energies === |  |
    | `AUTOCI_NUCLEAR_GRADIENT` | AutoCI Energy nuclear gradient |
    | `AUTOCI_NUCLEAR_GRADIENT_NORM` | AutoCI Norm of the nuclear gradient |
    | `AUTOCI_NUCLEAR_GRADIENT_ATOM_NUMBERS` | AutoCI Atomic numbers of the atoms in the gradient |
    | === Electric Properties (Dipole moment) === |  |
    | `AUTOCI_DIPOLE_MAGNITUDE` | AutoCI Dipole moment magnitude |
    | `AUTOCI_DIPOLE_ELEC_CONTRIB` | AutoCI Electronic contribution to dipole moment |
    | `AUTOCI_DIPOLE_NUC_CONTRIB` | AutoCI Nuclear contribution to dipole moment |
    | `AUTOCI_DIPOLE_TOTAL` | AutoCI Total dipole moment |
    | `SCF_ENERGY` | SCF Energy |
    | === Electric Properties (Polarizability) === |  |
    | `AUTOCI_POLAR_ISOTROPIC` | AutoCI Isotropic polarizability |
    | `AUTOCI_POLAR_RAW` | AutoCI Raw polarizability tensor |
    | `AUTOCI_POLAR_DIAG_TENSOR` | AutoCI Diagonalized polarizability tensor |
    | `AUTOCI_POLAR_ORIENTATION` | AutoCI Polarizability orientation (eigenvectors) |
    | === Electric Properties (Quadrupole moment) === |  |
    | `AUTOCI_QUADRUPOLE_MOMENT_ISOTROPIC` | AutoCI Isotropic quadrupole moment |
    | `AUTOCI_QUADRUPOLE_MOMENT_DIAG_TENSOR` | AutoCI Diagonalized quadrupole tensor |
    | `AUTOCI_QUADRUPOLE_MOMENT_ELEC_CONTRIB` | AutoCI Electronic contribution to quadrupole moment |
    | `AUTOCI_QUADRUPOLE_MOMENT_NUC_CONTRIB` | AutoCI Nuclear contribution to quadrupole moment |
    | `AUTOCI_QUADRUPOLE_MOMENT_TOTAL` | AutoCI Total quadrupole moment |
    | === Magnetic Properties (D Tensor) === |  |
    | `AUTOCI_D_TENSOR_EIGENVALUES` | AutoCI D Tensor eigenvalues |
    | `AUTOCI_D_TENSOR_EIGENVECTORS` | AutoCI D Tensor eigenvectors |
    | `AUTOCI_D_TENSOR_RAW` | AutoCI Raw D Tensor |
    | `AUTOCI_D_TENSOR_D` | AutoCI D value for D Tensor |
    | `AUTOCI_D_TENSOR_E` | AutoCI E value for D Tensor |
    | `AUTOCI_D_TENSOR_MULTIPLICITY` | AutoCI Spin-multiplicity used for D Tensor |
    | === Magnetic Properties (G Tensor) === |  |
    | `AUTOCI_G_TENSOR_RAW` | AutoCI Raw G Tensor |
    | `AUTOCI_G_TENSOR_ELEC` | AutoCI Electronic part of G Tensor |
    | `AUTOCI_G_TENSOR_TOT` | AutoCI Total G Tensor |
    | `AUTOCI_G_TENSOR_ISO` | AutoCI Isotropic g value |
    | `AUTOCI_G_TENSOR_ORIENTATION` | AutoCI G Tensor orientation (eigenvectors) |
    | === Additional SCF Properties === |  |
    | `SCF_ENERGY` | SCF Energy |
    | `VDW_CORRECTION` | van der Waals correction |
    | `SCF Electric properties` |  |
    | `SCF_DIPOLE_MAGNITUDE` | SCF Dipole moment (Debye) |
    | `SCF_DIPOLE_ELEC_CONTRIB` | SCF Electronic contribution to dipole moment |
    | `SCF_DIPOLE_NUC_CONTRIB` | SCF Nuclear contribution to dipole moment |
    | `SCF_DIPOLE_TOTAL` | SCF Total dipole moment |
    | `SCF_QUADRUPOLE_ISOTROPIC` | SCF Isotropic quadrupole moment |
    | `SCF_QUADRUPOLE_DIAG_TENSOR` | SCF Diagonalized quadrupole tensor |
    | `SCF_QUADRUPOLE_ELEC_CONTRIB` | SCF Electronic contribution to quadrupole moment |
    | `SCF_QUADRUPOLE_NUC_CONTRIB` | SCF Nuclear contribution to quadrupole moment |
    | `SCF_QUADRUPOLE_TOTAL` | SCF Total quadrupole moment |
    | `SCF_POLAR_ISOTROPIC` | SCF Isotropic polarizability |
    | `SCF_POLAR_RAW` | SCF Raw polarizability tensor |
    | `SCF_POLAR_DIAG_TENSOR` | SCF Diagonalized polarizability tensor |
    | === DBOC Energy Correction === |  |
    | `DBOC_ENERGY` | Diagonal Born-Oppenheimer correction (DBOC) energy |
    | === DBOC Energy Correction === |  |
    | `DBOC_ENERGY` | Diagonal Born-Oppenheimer energy correction |
    | === DFT === |  |
    | `DFT_NUM_OF_ALPHA_EL` | Number of alpha electrons |
    | `DFT_NUM_OF_BETA_EL` | Number of beta electrons |
    | `DFT_NUM_OF_TOTAL_EL` | Total number of electrons |
    | `DFT_TOTAL_EN` | DFT Total energy |
    | `DFT_EXCHANGE_EN` | DFT Exchange energy |
    | `DFT_CORR_EN` | DFT Correlation energy |
    | `DFT_XC_EN` | DFT Exchange-Correlation energy |
    | `DFT_NON_LOC_EN` | DFT Non-local correlation energy |
    | `DFT_EMBED_CORR` | DFT Embedding correction |
    | === gCP Correction === |  |
    | `GCP_CORRECTION` | Geometrical counterpoise (gCP) energy correction |
    | === MP2 === |  |
    | `MP2_REF_ENERGY` | Reference SCF Energy |
    | `MP2_CORR_ENERGY` | MP2 Correlation energy |
    | `MP2_TOTAL_ENERGY` | Total Energy (SCF + MP2) |
    | === MP2 Electric Properties === |  |
    | `MP2_DIPOLE_MAGNITUDE` | MP2 Dipole moment (Debye) |
    | `MP2_DIPOLE_ELEC_CONTRIB` | MP2 Electronic contribution to dipole moment |
    | `MP2_DIPOLE_NUC_CONTRIB` | MP2 Nuclear contribution to dipole moment |
    | `MP2_DIPOLE_TOTAL` | MP2 Total dipole moment |
    | `MP2_QUADRUPOLE_ISOTROPIC` | MP2 Isotropic quadrupole moment |
    | `MP2_QUADRUPOLE_DIAG_TENSOR` | MP2 Diagonalized quadrupole tensor |
    | `MP2_QUADRUPOLE_ELEC_CONTRIB` | MP2 Electronic contribution to quadrupole moment |
    | `MP2_QUADRUPOLE_NUC_CONTRIB` | MP2 Nuclear contribution to quadrupole moment |
    | `MP2_QUADRUPOLE_TOTAL` | MP2 Total quadrupole moment |
    | `MP2_POLAR_ISOTROPIC` | MP2 Isotropic polarizability |
    | `MP2_POLAR_RAW` | MP2 Raw polarizability tensor |
    | `MP2_POLAR_DIAG_TENSOR` | MP2 Diagonalized polarizability tensor |
    | === MDCI === |  |
    | `MDCI_REF_ENERGY` | Reference SCF Energy |
    | `MDCI_CORR_ENERGY` | Total Correlation Energy |
    | `MDCI_TOTAL_ENERGY` | Total Energy (SCF + Correlation) |
    | `MDCI_ALPHA_ALPHA_CORR_ENERGY` | Correlation energy from αα electron pairs |
    | `MDCI_BETA_BETA_CORR_ENERGY` | Correlation energy from ββ electron pairs |
    | `MDCI_ALPHA_BETA_CORR_ENERGY` | Correlation energy from αβ electron pairs |
    | `MDCI_DSINGLET_CORR_ENERGY` | Correlation energy from singlet (double excitations, closed-shell only) |
    | `MDCI_DTRIPLET_CORR_ENERGY` | Correlation energy from triplet (double excitations, closed-shell only) |
    | `MDCI_SSINGLET_CORR_ENERGY` | Correlation energy from singlet (single excitations, closed-shell only) |
    | `MDCI_STRIPLET_CORR_ENERGY` | Correlation energy from triplet (single excitations, closed-shell only) |
    | `MDCI_TRIPLES_ENERGY` | Perturbative triples correlation energy |
    | `MDCI_ALL_ELECTRONS` | Total number of electrons |
    | `MDCI_CORR_ELECTRONS` | Number of correlated electrons |
    | `MDCI_CORR_ALPHA_ELECTRONS` | Number of correlated α electrons |
    | `MDCI_CORR_BETA_ELECTRONS` | Number of correlated β electrons |
    | === MDCI Electric Properties === |  |
    | `MDCI_DIPOLE_MAGNITUDE` | MDCI Dipole moment (Debye) |
    | `MDCI_DIPOLE_ELEC_CONTRIB` | MDCI Electronic contribution to dipole moment |
    | `MDCI_DIPOLE_NUC_CONTRIB` | MDCI Nuclear contribution to dipole moment |
    | `MDCI_DIPOLE_TOTAL` | MDCI Total dipole moment |
    | `MDCI_QUADRUPOLE_ISOTROPIC` | MDCI Isotropic quadrupole moment |
    | `MDCI_QUADRUPOLE_DIAG_TENSOR` | MDCI Quadrupole moment diagonalised tensor |
    | `MDCI_QUADRUPOLE_ELEC_CONTRIB` | MDCI Electronic contribution to quadrupole moment |
    | `MDCI_QUADRUPOLE_NUC_CONTRIB` | MDCI Nuclear contribution to quadrupole moment |
    | `MDCI_QUADRUPOLE_TOTAL` | MDCI Total quadrupole moment |
    | `MDCI_POLAR_ISOTROPIC` | MDCI Isotropic polarizability |
    | `MDCI_POLAR_RAW` | MDCI Raw polarizability tensor |
    | `MDCI_POLAR_DIAG_TENSOR` | MDCI Diagonalised polarizability tensor |
    | === CASSCF / CASPT2 / DCDCAS === |  |
    | `CASSCF_NUM_OF_MULTS` | Number of CASSCF spin multiplicities |
    | `CASSCF_NUM_OF_IRREPS` | Number of CASSCF irreducible representations |
    | `CASSCF_FINAL_ENERGY` | Final CASSCF energy |
    | `PT2_NUM_OF_MULTS` | CASPT2 spin multiplicities |
    | `PT2_NUM_OF_IRREPS` | Number of CASPT2 irreducible representations |
    | `PT2_FINAL_ENERGY` | CASPT2 energy |
    | `DCDCAS_NUM_OF_MULTS` | Number of DCDCAS spin multiplicities |
    | `DCDCAS_NUM_OF_IRREPS` | Number of DCDCAS irreducible representations |
    | `DCDCAS_FINAL_ENERGY` | DCDCAS energy |
    | === Spectra (Absorption and CD) === |  |
    | `CASSCF_ABS_SPECTRUM` | CASSCF Absorption spectrum |
    | `CASSCF_ABS_SPECTRUM_INFO` | Information on CASSCF spectrum excitations |
    | `CASSCF_ABS_SPECTRUM_NROOTS` | Number of roots in CASSCF absorption |
    | `CASSCF_CD_SPECTRUM` | CASSCF Circular Dichroism spectrum |
    | `CASSCF_CD_SPECTRUM_INFO` | Info on excitations in CASSCF CD spectrum |
    | `CASSCF_CD_SPECTRUM_NROOTS` | Number of roots in CASSCF CD |
    | `CASPT2_ABS_SPECTRUM` | CASPT2 Absorption spectrum |
    | `CASPT2_ABS_SPECTRUM_INFO` | Info on excitations in CASPT2 spectrum |
    | `CASPT2_ABS_SPECTRUM_NROOTS` | Number of roots in CASPT2 absorption |
    | `CASPT2_CD_SPECTRUM` | CASPT2 Circular Dichroism spectrum |
    | `CASPT2_CD_SPECTRUM_INFO` | Info on excitations in CASPT2 CD spectrum |
    | `CASPT2_CD_SPECTRUM_NROOTS` | Number of roots in CASPT2 CD |
    | `CAS_CUSTOM_ABS_SPECTRUM` | Custom CASSCF Absorption spectrum |
    | `CAS_CUSTOM_ABS_SPECTRUM_INFO` | Excitation info of custom CASSCF absorption spectrum |
    | `CAS_CUSTOM_ABS_SPECTRUM_NROOTS` | Number of roots in custom absorption spectrum |
    | `CAS_CUSTOM_CD_SPECTRUM` | Custom CASSCF CD spectrum |
    | `CAS_CUSTOM_CD_SPECTRUM_INFO` | Info on excitations of custom CD spectrum |
    | `CAS_CUSTOM_CD_SPECTRUM_NROOTS` | Number of roots in custom CD spectrum |
    | `DCDCAS_ABS_SPECTRUM` | DCDCAS Absorption spectrum |
    | `DCDCAS_ABS_SPECTRUM_INFO` | Excitation info for DCDCAS absorption spectrum |
    | `DCDCAS_ABS_SPECTRUM_NROOTS` | Number of roots in DCDCAS absorption |
    | === Zero-Field Splitting (ZFS) === |  |
    | `CASSCF_DTENSOR_EIGENVALUES` | CASSCF D tensor eigenvalues |
    | `CASSCF_DTENSOR_RAW_EIGENVECTORS` | Raw eigenvectors of CASSCF D tensor |
    | `CASSCF_DTENSOR_D` | D value of CASSCF ZFS |
    | `CASSCF_DTENSOR_E` | E value of CASSCF ZFS |
    | `CASSCF_DTENSOR_MULTIPLICITY` | Spin multiplicity of CASSCF |
    | `CASPT2_DTENSOR_EIGENVALUES` | CASPT2 D tensor eigenvalues |
    | `CASPT2_DTENSOR_RAW_EIGENVECTORS` | Raw eigenvectors of CASPT2 D tensor |
    | `CASPT2_DTENSOR_D` | D value of CASPT2 ZFS |
    | `CASPT2_DTENSOR_E` | E value of CASPT2 ZFS |
    | `CASPT2_DTENSOR_MULTIPLICITY` | Spin multiplicity of CASPT2 |
    | `CAS_CUSTOM_DTENSOR_EIGENVALUES` | Custom CASSCF D tensor eigenvalues |
    | `CAS_CUSTOM_DTENSOR_RAW_EIGENVECTORS` | Custom CASSCF raw D tensor eigenvectors |
    | `CAS_CUSTOM_DTENSOR_D` | D value of custom CASSCF ZFS |
    | `CAS_CUSTOM_DTENSOR_E` | E value of custom CASSCF ZFS |
    | `CAS_CUSTOM_DTENSOR_MULTIPLICITY` | Spin multiplicity of custom CASSCF |
    | === CIPSI === |  |
    | `CIPSI_SPIN_MULTIPLICITY` | CIPSI spin multiplicity |
    | `CIPSI_NUM_OF_ROOTS` | Number of roots in CIPSI |
    | `CIPSI_FINAL_ENERGY` | Final CIPSI energy |
    | `CIPSI_ENERGIES` | All CIPSI energies |
    | === CIS === |  |
    | `CIS_FINAL_ENERGY` | Final total energy from CIS |
    | `CIS_ESCF` | SCF Energy |
    | `CIS_E0` | Ground state energy |
    | `CIS_ENERGIES` | Singlet excitation energies |
    | `CIS_ENERGIESP1` | Triplet excitation energies |
    | `CIS_MODE` | CIS calculation mode |
    | `CIS_NUM_OF_ROOTS` | Number of roots |
    | `CIS_ROOT` | State to be optimized |
    | `CIS_ABS_SPECTRUM_NROOTS` | Number of roots for absorption spectrum |
    | `CIS_ABS_SPECTRUM` | CIS absorption spectrum |
    | `CIS_ABS_SPECTRUM_VELOCITY` | CIS absorption spectrum (velocity representation) |
    | `CIS_ABS_SOC_SPECTRUM_NROOTS` | Number of roots including SOC (absorption) |
    | `CIS_ABS_SOC_SPECTRUM` | CIS absorption spectrum with SOC |
    | `CIS_CD_SPECTRUM_NROOTS` | Number of roots in CD spectrum |
    | `CIS_CD_SPECTRUM` | CIS circular dichroism spectrum |
    | `CIS_CD_SOC_SPECTRUM_NROOTS` | Number of roots in CD with SOC |
    | `CIS_CD_SOC_SPECTRUM` | CIS CD spectrum including SOC |
    | === ROCIS === |  |
    | `ROCIS_STATE` | ROCIS state |
    | `ROCIS_REF_ENERGY` | ROCIS reference energy |
    | `ROCIS_CORR_ENERGY` | ROCIS correlation energy |
    | `ROCIS_TOTAL_ENERGY` | Total ROCIS energy |
    | `ROCIS_ABS_SPECTRUM_NROOTS` | Number of roots in ROCIS absorption |
    | `ROCIS_ABS_SPECTRUM` | ROCIS absorption spectrum |
    | `ROCIS_ABS_SOC_SPECTRUM_NROOTS` | Number of roots with SOC (absorption) |
    | `ROCIS_ABS_SOC_SPECTRUM` | ROCIS absorption spectrum including SOC |
    | `ROCIS_CD_SPECTRUM_NROOTS` | Number of roots in ROCIS CD |
    | `ROCIS_CD_SPECTRUM` | ROCIS circular dichroism spectrum |
    | `ROCIS_CD_SOC_SPECTRUM_NROOTS` | Number of roots in ROCIS CD with SOC |
    | `ROCIS_CD_SOC_SPECTRUM` | ROCIS CD spectrum including SOC |
    | === MRCI === |  |
    | `MRCI_ABS_SPECTRUM` | MRCI absorption spectrum |
    | `MRCI_ABS_SPECTRUM_INFO` | Info about MRCI absorption spectrum |
    | `MRCI_ABS_SPECTRUM_NROOTS` | Number of roots in MRCI absorption |
    | `MRCI_CD_SPECTRUM` | MRCI CD spectrum |
    | `MRCI_CD_SPECTRUM_INFO` | Info about MRCI CD spectrum |
    | `MRCI_CD_SPECTRUM_NROOTS` | Number of roots in MRCI CD |
    | `MRCI_DIPOLE_MOMENTS` | MRCI dipole moments |
    | `MRCI_DIPOLE_MOMENTS_INFO` | Info about MRCI dipole moments |
    | `MRCI_DTENSOR_EIGENVECTORS` | MRCI D tensor eigenvectors |
    | `MRCI_DTENSOR_EIGENVALUES` | MRCI D tensor eigenvalues |
    | `MRCI_DTENSOR_RAW_EIGENVECTORS` | Raw eigenvectors of MRCI D tensor |
    | `MRCI_DTENSOR_D` | D value of MRCI ZFS |
    | `MRCI_DTENSOR_E` | E value of MRCI ZFS |
    | `MRCI_DTENSOR_MULTIPLICITY` | MRCI spin multiplicity |
    | === EXTRAPOLATION === |  |
    | `EXTRAP_SCF_ENERGIES` | SCF energies for various basis sets |
    | `EXTRAP_CBS_SCF` | Extrapolated SCF energy (CBS limit) |
    | `EXTRAP_CORR_ENERGIES` | Correlation energies for different basis sets |
    | `EXTRAP_CBS_CORR` | Extrapolated correlation energy |
    | `EXTRAP_CBS_TOTAL` | Extrapolated total energy |
    | `EXTRAP_CCSDT_X` | (T) contribution to energy |
    | `EXTRAP_NUM_OF_ENERGIES` | Number of basis sets used in extrapolation |
    | === THERMOCHEMISTRY === |  |
    | `THERMO_TEMPERATURE` | Temperature (°K) |
    | `THERMO_PRESSURE` | Pressure (atm) |
    | `THERMO_TOTAL_MASS` | Total molecular mass (AMU) |
    | `THERMO_SPIN_DEGENERACY` | Electronic degeneracy |
    | `THERMO_ELEC_ENERGY` | Electronic energy (Eh) |
    | `THERMO_TRANS_ENERGY` | Translational energy (Eh) |
    | `THERMO_ROT_ENERGY` | Rotational energy (Eh) |
    | `THERMO_VIB_ENERGY` | Vibrational energy (Eh) |
    | `THERMO_NUM_OF_FREQS` | Number of vibrational frequencies |
    | `THERMO_FREQS` | Vibrational frequencies |
    | `THERMO_ZPE` | Zero-point energy (Eh) |
    | `THERMO_INNER_ENERGY_U` | Inner energy U (Eh) |
    | `THERMO_ENTHALPY_H` | Enthalpy H (Eh) |
    | `THERMO_ELEC_ENTROPY` | (Electronic entropy) × T (Eh) |
    | `THERMO_ROR_ENTROPY` | (Rotational entropy) × T (Eh) |
    | `THERMO_VIB_ENTROPY` | (Vibrational entropy) × T (Eh) |
    | `THERMO_TRANS_ENTROPY` | (Translational entropy) × T (Eh) |
    | `THERMO_ENTROPY_S` | Total entropy × T (Eh) |
    | `THERMO_FREE_ENERGY_G` | Free energy G (Eh) |
    | === EPR-NMR Spin-Spin Coupling === |  |
    | `EPRNMR_SSC_NUM_OF_NUC_PAIRS` | Nuclear pairs used for SSC calculations |
    | `EPRNMR_SSC_NUM_OF_NUC_PAIRS_DSO` | Nuclear pairs for DSO terms |
    | `EPRNMR_SSC_NUM_OF_NUC_PAIRS_PSO` | Nuclear pairs for PSO terms |
    | `EPRNMR_SSC_NUM_OF_NUC_PAIRS_FC` | Nuclear pairs for Fermi Contact (FC) terms |
    | `EPRNMR_SSC_NUM_OF_NUC_PAIRS_SD` | Nuclear pairs for Spin Dipole (SD) terms |
    | `EPRNMR_SSC_NUM_OF_NUC_PAIRS_SD_FC` | Nuclear pairs for SD/FC mixed terms |
    | `EPRNMR_SSC_NUM_OF_NUCLEI_PSO` | Nuclei involved in PSO perturbation |
    | `EPRNMR_SSC_NUM_OF_NUCLEI_FC` | Nuclei involved in SD/FC perturbation |
    | === SOC Energy Correction === |  |
    | `SOC_NUCLEAR_ENERGY` | Nuclear energy |
    | `SOC_2C_ENERGY` | Two-component total energy |
    | `SOC_NON_SOC_ENERGY` | Total energy without SOC |
    | `SOC_ENERGY_CORRECTION` | SOC energy correction |
    | === Solvation === |  |
    | `SOLVATION_EPSILON` | Dielectric constant |
    | `SOLVATION_REFRAC` | Refractive index |
    | `SOLVATION_RSOLV` | Solvent probe radius |
    | `SOLVATION_SURFACE_TYPE` | Type of cavity surface used |
    | `SOLVATION_CPCM_DIEL_ENERGY` | Total energy with CPCM dielectric correction |
    | `SOLVATION_NPOINTS` | Number of points for Gaussian surface |
    | `SOLVATION_SURFACE_AREA` | Total surface area |
    | === General Job Information === |  |
    | `JOB_INFO_MULT` | Spin multiplicity |
    | `JOB_INFO_CHARGE` | Molecular charge |
    | `JOB_INFO_NUM_OF_ATOMS` | Number of atoms |
    | `JOB_INFO_NUM_OF_EL` | Number of electrons |
    | `JOB_INFO_NUM_OF_FC_EL` | Number of frozen core electrons |
    | `JOB_INFO_NUM_OF_CORR_ELC` | Number of correlated electrons |
    | `JOB_INFO_NUM_OF_BASIS_FUNCS` | Number of basis functions |
    | `JOB_INFO_NUM_OF_AUXC_BASIS_FUNCS` | Number of auxiliary C basis functions |
    | `JOB_INFO_NUM_OF_AUXJK_BASIS_FUNCS` | Number of auxiliary JK basis functions |
    | `JOB_INFO_NUM_OF_AUX_CABS_BASIS_FUNCS` | Number of auxiliary JK CABS basis functions |
    | `JOB_INFO_TOTAL_EN` | Final total energy |
    | === HESSIAN === |  |
    | `HESSIAN_MODES` | Hessian matrix or vibrational modes |
    | === Math Functions === |  |
    | `ABS` | Absolute value |
    | `COS` | Cosine |
    | `SIN` | Sine |
    | `TAN` | Tangent |
    | `ACOS` | Inverse cosine |
    | `ASIN` | Inverse sine |
    | `ATAN` | Inverse tangent |
    | `COSH` | Hyperbolic cosine |
    | `SINH` | Hyperbolic sine |
    | `TANH` | Hyperbolic tangent |
    | `EXP` | Exponential |
    | `LOG` | Common logarithm (base 10) |
    | `LN` | Natural logarithm |
    | `SQRT` | Square root |
    | `ROUND` | Round down to nearest integer |

