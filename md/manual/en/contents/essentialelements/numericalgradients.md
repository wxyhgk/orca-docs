```{index} Numerical Gradients, NumGrad
```

(sec:essentialelements.numericalgradients)=
# Numerical Gradients

If the analytic gradient is not available, the numerical gradient can
simply be requested via:

```orca
! NumGrad
```

as in the following example:

```orcainput
!CCSD(T) TZVPP
!Opt NumGrad

* int 0 1
C 0 0 0  0   0   0
O 1 0 0  1.2 0   0
H 1 2 0  1.1 120 0
H 1 2 3  1.1 120 180
*
```

:::{note}
-   Be aware that the numerical gradient is quite expensive. The time
    for one gradient calculation is equal to 6 $\times$ (number of
    atoms) $\times$ (time for one single point calculation).

-   The numerical gradient can be performed in a multi-process run,
    doing each displacement as a parallel calculation (see section
    {ref}`sec:essentialelements.parallel.calling`).
:::


Additionally the various settings for the numerical differentiation can be changed:

```orca
%numgrad
  CentralDiff true # You should use two-sided numerical differentiation, but it 
                   # is possible to switch to one-sided numerical differentiation.
  DX 0.005         # Increment in Bohr for the differentiation.
  TransInvar  true # Take advantage of translation invariance
  Accuracy       2 # 2,4,6,8 - number of points used for numerical differentiation
end
```

:::{tip}
   - Numerical gradients with higher order of accuracy will be drastically more expensive
   than the normal (2-point) numerical gradients, as they do twice (three or four times) the number of displacement calculations.
   - Choosing accuracy higher than `4` normally doesn't pay off    
   (the increase in computational time is considerable, the increase of accuracy is only marginal)
   - For DFT using higher accuracy than `4` can even be counterproductive -    
   leading to accumulation of numerical noise.
   - Using RIJCOSX (or other methods that introduce an additional grid) for gradients of higher oder of accuracy is strongly discouraged as the numerical noise outweighs the gain in accuracy of the increased number of points.
   - Higher order of accuracy for numerical gradients cannot be combined with `CentralDiff false`
:::