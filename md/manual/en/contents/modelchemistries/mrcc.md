```{index} Coupled-Cluster
```

(sec:modelchemistries.mrcc)=
# Arbitrary Order Coupled-Cluster (MRCC interface)
Various higher order theories (CC3, CISDT, CCSDTQ, MP4) are implemented using the [automatic code-generation](sec:modelchemistries.autoci). In addition,  ORCA features an interface to Kallay's powerful MRCC program. This program must be obtained separately. The interface is restricted to single point energies but can be used for rigid scan calculations or
numerical frequencies.

The use of the interface is simple:

```{literalinclude} ../../orca_working_input/C05S01_065.inp
:language: orca
```

The Method string can be any of:

```orca
# The excitation level specification can be anything
# like SD, SDT, SDTQ, SDTQP etc.
 %mrcc method   "CCSDT"
                "CCSD(T)"
                "CCSD[T]"
                "CCSD(T)_L"  (the lambda version)
                "CC3"
                "CCSDT-1a"
                "CCSDT-1b"
                "CISDT"
```

It is not a good idea, of course, to use this code for CCSD or CCSD(T)
or CISD. Its real power lies in performing the higher order
calculations. Open-shell calculations can presently not be done with the
interface.


