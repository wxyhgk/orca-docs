(sec:hellowater)=
# Hello water! Your first ORCA calculation

After [setting up ORCA correctly](sec:installation), you are ready to perform your first calculation with ORCA! Here, we will exemplarily compute the energy of a water molecule using [Hartree-Fock theory](sec:essentialelements.hartreefock) and the def2-SVP [basis set](sec:essentialelements.basisset). We will use the following `hellowater.inp` ORCA input file:

```
! HF DEF2-SVP

* XYZ 0 1
O   0.0000   0.0000   0.0626
H  -0.7920   0.0000  -0.4973
H   0.7920   0.0000  -0.4973
*
```

:::{hint}
The input usually has the `.inp` extension, but `.txt` is also ok.
:::

You can now run ORCA.

```orca
orca hellowater.inp > hellowater.out
```

The output is then printed in the file `hellowater.out` in working directory. 

```orca
                                 *****************
                                 * O   R   C   A *
                                 *****************

                                            #,                                       
                                            ###                                      
                                            ####                                     
                                            #####                                    
                                            ######                                   
                                           ########,                                 
                                     ,,################,,,,,                         
                               ,,#################################,,                 
                          ,,##########################################,,             
                       ,#########################################, ''#####,          
                    ,#############################################,,   '####,        
                  ,##################################################,,,,####,       
                ,###########''''           ''''###############################       
              ,#####''   ,,,,##########,,,,          '''####'''          '####       
            ,##' ,,,,###########################,,,                        '##       
           ' ,,###''''                  '''############,,,                           
         ,,##''                                '''############,,,,        ,,,,,,###''
      ,#''                                            '''#######################'''  
     '                                                          ''''####''''         
             ,#######,   #######,   ,#######,      ##                                
            ,#'     '#,  ##    ##  ,#'     '#,    #''#        ,####,    ,#,          
            ##       ##  ##   ,#'  ##            #'  '#       #'       ,# #          
            ##       ##  #######   ##           ,######,      #####,      #          
            '#,     ,#'  ##    ##  '#,     ,#' ,#      #,     #,   #      #          
             '#######'   ##     ##  '#######'  #'      '#     '####' #    #          



                #########################################################
                #                        -***-                          #
                #          Department of theory and spectroscopy        #
                #                                                       #
                #                      Frank Neese                      #
                #                                                       #
                #     Directorship, Architecture, Infrastructure        #
                #                    SHARK, DRIVERS                     #
                #        Core code/Algorithms in most modules           #
                #                                                       #
                #        Max Planck Institute fuer Kohlenforschung      #
                #                Kaiser Wilhelm Platz 1                 #
                #                 D-45470 Muelheim/Ruhr                 #
                #                      Germany                          #
                #                                                       #
                #                  All rights reserved                  #
                #                        -***-                          #
                #########################################################
[...]
```

You can then open the output file to see the results of your calculation (make sure not to overwrite it while the calculation is running). If the calculation ended normally, a respective message is printed to the end of the output file.

```orca
                             ****ORCA TERMINATED NORMALLY****
```

The energy of the water molecule can now be found in the output file:

```orca
-------------------------   --------------------
FINAL SINGLE POINT ENERGY       -75.959340303174
-------------------------   --------------------
```

Congratulations, you successfully ran your first quantum chemical calculation with ORCA! 
