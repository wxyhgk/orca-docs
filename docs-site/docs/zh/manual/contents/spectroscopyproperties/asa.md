

<a id="sec:spectroscopyproperties.asa.bandshapes"></a>
# 使用 `ORCA_ASA` 计算吸收与荧光谱带形状（Absorption and Fluorescence Bandshapes）

**也请考虑使用更近期的 ORCA_ESD 来计算谱带形状，详见
[spectroscopyproperties.esd](#sec:spectroscopyproperties.esd) 一节。**

谱带形状（bandshape）的计算并不简单，但借助
[spectroscopyproperties.asa](#sec:spectroscopyproperties.asa) 一节所述的流程，
可以用 ORCA 实现。
从 2.80 版本开始，可使用解析 TD-DFT 梯度，
这使得此类计算相当快捷，并且无需专业知识即可应用于较大的分子。

!!! note
    -   HF 交换成分略多一些的泛函能给出更好的结果，
        也不像 GGA 泛函那样容易出现"鬼态"（ghost states）——遗憾的是后者常有此问题！

    -   采用 RI 或 RIJCOSX 近似可以大大加快计算！

    -   (D) 校正以及双杂化泛函的解析梯度**不可用**。

简而言之，让我们来看 H$_{2}$CO 分子。
首先生成某个 Hessian（例如 BP86/SV(P)）。
然后运行生成 `orca_asa` 程序输入文件的作业。
例如，计算五个最低激发态：

```orca
! aug-cc-pVDZ BHandHLYP TightSCF NMGrad 

%tddft nroots 5 end

# this is ASA-specific input
%rr    states 1,2,3,4,5
       HessName "Test-ASA-H2CO-freq.hess"
       ASAInput True
       end 

*int 0 1
 C 0 0 0  0   0     0 
 O 1 0 0  1.2 0     0
 H 1 2 0  1.1 120   0
 H 1 2 3  1.1 120 180
*
```

ORCA 运行会生成一个 `Test-ASA-H2CO.asa.inp` 文件，
它是生成各种谱图的程序的输入文件。
这是一个 ASCII 文件，外观与 ORCA 输入文件非常相似：

```orca
#
# ASA input
#
%sim     model IMDHO
         method Heller

         AbsRange     25000.0,  100000.0
         NAbsPoints   1024

         FlRange      25000.0,  100000.0
         NFlPoints    1024

         RRPRange     5000.0,  100000.0
         NRRPPoints   1024

         RRSRange        0.0,    4000.0
         NRRSPoints   4000

         # Excitation energies (cm**-1) for which rR spectra will
         # be calculated. Here we choose all allowed transitions
         # and the position of the 0-0 band
         RRSE 58960, 66884, 66602

         # full width half maximum of Raman bands in rR spectra
         # (cm**-1):
         RRS_FWHM 10.0

         AbsScaleMode Ext
         FlScaleMode  Rel
         # RamanOrder=1 means only fundamentals. For 2 combination
         # bands and first overtones are also considered, for 3
         # one has second overtones etc.
         RamanOrder   1

         # E0 means the adiabatic excitation energy
         # EV would mean the vertical one. sprints vertical
         # excitations in the TD-DFT output but for the input into
         # the ASA program the adiabatic excitation energies are
         # estimated. A rigorous calculation would of course in-
         # volve excited state geometry optimization
         EnInput E0

         CAR   0.800
         end

# These are the calculated electronic states and transition moments
# Note that this is in the Franck-Condon approximation and thus
# the transition moments have been calculated vertically
$el_states
5
   1 32200.79   100.00    0.00    -0.0000   0.0000  -0.0000
   2 58960.05   100.00    0.00     0.0000  -0.4219   0.0000
   3 66884.30   100.00    0.00    -0.0000   0.4405   0.0000
   4 66602.64   100.00    0.00    -0.5217  -0.0000   0.0000
   5 72245.42   100.00    0.00     0.0000   0.0000   0.0000

# These are the calculated vibrational frequencies for the totally
# symmetric modes. These are the only ones that contribute. They
# correspond to x, H-C-H bending, C=O stretching and C-H stretching
# respectively
$vib_freq_gs
3
    1     1462.948534
    2     1759.538581
    3     2812.815170

# These are the calculated dimensional displacements for all
# electronic states along all of the totally symmetric modes.
$sdnc
3 5
                   1          2          3          4          5
      1      -0.326244   0.241082  -0.132239   0.559635   0.292190
      2      -1.356209   0.529823   0.438703   0.416161   0.602301
      3      -0.183845   0.418242   0.267520   0.278880   0.231340
```

在该文件中将 `NAbsPoints` 变量和谱范围设置为所需值后，
按如下方式调用 `orca_asa`：

```orca
orca_asa Test-ASA-H2CO.asa.inp
```

这会产生如下输出：

```orca
******************
                                    * O R C A  A S A *
                                    ******************

                    --- A program for analysis of electronic spectra ---

Reading file: Test-ASA-H2CO.asa.inp ... done

         **************************************************************
         *        GENERAL CHARACTERISTICS OF ELECTRONIC SPECTRA        *
         **************************************************************

--------------------------------------------------------------------------------
  State      E0           EV       fosc    Stokes shift  Effective Stokes shift
          (cm**-1)     (cm**-1)              (cm**-1)           (cm**-1)
--------------------------------------------------------------------------------
    1:     30457.24   32200.79   0.000000      0.00                0.00
    2:     58424.56   58960.05   0.031879      0.00                0.00
    3:     66601.54   66884.30   0.039422      0.00                0.00
    4:     66111.80   66602.64   0.055063      0.00                0.00
    5:     71788.55   72245.42   0.000000      0.00                0.00

------------------------------------------------------------------------------------------
                              BROADENING PARAMETETRS (cm**-1)
------------------------------------------------------------------------------------------
             Intrinsic                                    Effective
 State -------------------------  --------------------------------------------------------
                                               Sigma                         FWHM
        Gamma    Sigma    FWHM    --------------------------   ---------------------------
                                    0K       77K     298.15K      0K       77K     298.15K
-------------------------------------------------------------------------------------------
  1:   100.00     0.00   200.00     0.00      0.00      0.00    200.00    200.00    200.00
  2:   100.00     0.00   200.00     0.00      0.00      0.00    200.00    200.00    200.00
  3:   100.00     0.00   200.00     0.00      0.00      0.00    200.00    200.00    200.00
  4:   100.00     0.00   200.00     0.00      0.00      0.00    200.00    200.00    200.00
  5:   100.00     0.00   200.00     0.00      0.00      0.00    200.00    200.00    200.00

Calculating absorption spectrum   ...
The maximum number of grid points ... 5840
Time for absorption               ...       9.569 sec (=   0.159 min)
Writing file: Test-ASA-H2CO.asa.abs.dat ... done
Writing file: Test-ASA-H2CO.asa.abs.as.dat ... done

Generating vibrational states up to the  1-th(st) order  ...   done
Total number of vibrational states                       ...      3

Calculating rR profiles for all vibrational states up to the 1-th order
State 1 ...
The maximum number of grid points ... 6820
Resonance Raman profile is done
State 2 ...
The maximum number of grid points ... 6820
Resonance Raman profile is done
State 3 ...
The maximum number of grid points ... 6820
Resonance Raman profile is done
Writing file: Test-ASA-H2CO.asa.o1.dat... done
Writing file: Test-ASA-H2CO.asa.o1.info... done

Calculating rR spectra involving vibrational states up to the 1-th(st) order
State    1 ... done
State    2 ... done
State    3 ... done

Writing file: Test-ASA-H2CO.asa.o1.rrs.58960.dat      ... done
Writing file: Test-ASA-H2CO.asa.o1.rrs.58960.stk      ... done
Writing file: Test-ASA-H2CO.asa.o1.rrs.66884.dat      ... done
Writing file: Test-ASA-H2CO.asa.o1.rrs.66884.stk      ... done
Writing file: Test-ASA-H2CO.asa.o1.rrs.66602.dat      ... done
Writing file: Test-ASA-H2CO.asa.o1.rrs.66602.stk      ... done
Writing file: Test-ASA-H2CO.asa.o1.rrs.as.58960.dat   ... done
Writing file: Test-ASA-H2CO.asa.o1.rrs.as.58960.stk   ... done
Writing file: Test-ASA-H2CO.asa.o1.rrs.as.66884.dat   ... done
Writing file: Test-ASA-H2CO.asa.o1.rrs.as.66884.stk   ... done
Writing file: Test-ASA-H2CO.asa.o1.rrs.as.66602.dat   ... done
Writing file: Test-ASA-H2CO.asa.o1.rrs.as.66602.stk   ... done
Writing file: Test-ASA-H2CO.asa.o1.rrs.all.xyz.dat    ... done

TOTAL RUN TIME: 0 days 0 hours 1 minutes 17 seconds 850 msec
```

计算得到的振动分辨吸收谱绘于图 [fig:633](#fig:633) 中。

<a id="fig:633"></a>
!!! note "../../images/633.*"
    计算得到的 H$_{2}$CO 分子振动分辨吸收谱

最低能量峰的计算荧光谱绘于图 [fig:634](#fig:634) 中。该峰对应于 S2。
尽管它并不真实，但足以用于说明目的。

<a id="fig:634"></a>
!!! note "../../images/634.*"
    计算得到的 H$_{2}$CO 分子最低能量峰的荧光谱

三个全对称振动模式的计算共振拉曼（Resonance Raman，rR）激发轮廓
绘于图 [fig:635](#fig:635) 中。

<a id="fig:635"></a>
!!! note "../../images/635.*"
    计算得到的 H$_{2}$CO 分子三个全对称振动模式的共振拉曼激发轮廓

可以预料，C$=$O 伸缩振动的主导增强出现在主峰之下。
较高能量的激发则特别增强了 C-H 振动。
在垂直激发能处计算得到的 rR 谱见图 [fig:636](#fig:636)。

<a id="fig:636"></a>
!!! note "../../images/636.*"
    计算得到的 H$_{2}$CO 分子在垂直激发能处的共振拉曼谱

在这个简单的示例中，主导模式是 C$=$O 伸缩，
且所有激发波长下的谱图看起来都很相似。
然而，电子激发态大多具有不同的性质，
因而会产生截然不同的 rR 谱。
因此，rR 谱是所研究电子激发的有力指纹。
即使吸收带的振动结构未被分辨（大分子通常如此），
这一点同样成立。

`orca_asa` 程序的功能远比本节所描述的强大。
其完整功能说明请参见
[spectroscopyproperties.asa](#sec:spectroscopyproperties.asa) 一节。
`orca_asa` 程序还可与提供激发态梯度的其他电子结构代码对接，
并可用于拟合实验数据。
因此，它同时是实验学家和理论学家的工具！
