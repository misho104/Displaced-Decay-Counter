# Light Neutral Fermions from Bottom Decays

## Overview

This directory contains sample codes for the first example of the paper: a quasi-stable light neutral fermion $N$.

We consider a hypothetical neutral fermion $N$ with $m_N=1\text{ GeV}$.
It is assumed to be produced in B-hadron decays and long-lived enough to reach the (far) detectors.
The detectors will observe the particle $N$ if it decays into visible particles inside the detector.

To simplify the situation, only the operator
$$(\overline N\Gamma_l e)(\overline b\Gamma_q u)$$
is introduced for the production channel and $N$ is generated only from the decays of $B^\pm$.

## Input files

### The command file

The key declarations are given in `cmnd` file:

```plaintext
HardQCD:hardbbbar = on

1000022:new = hnl
1000022:spinType = 2
1000022:chargeType = 0
1000022:colType = 0
1000022:m0 = 1
1000022:tau0 = 0
1000022:mayDecay = False

521:oneChannel = 1 1 0 -11 1000022
```

The simulated process is `hardbbbar` at the 14-TeV LHC ($q\bar q\to b\bar b$ and $gg\to b\bar b$) and then some of the b-quarks hadronize into $B^\pm$ (`521`).
The $B^\pm$ mesons are set to decay exclusively as $B^\pm \to e^\pm N$, which is just to save computing resources and the branching fraction should be imposed later by users.

The particle $N$ is described by the ID `1000022`.
As its decays are handled by DDC with the value specified in the LLP file (see below), Pythia should treat it as a stable particle.
Meanwhile, `m0` must be set the same value as in the LLP file.

### The LLP file

The DDC simulates the decays of the LLPs, which are left as stable in Pythia-generated events.
The simulation is based on the information in the LLP file.

```json
{
  "LLP": { "LLPPID": 1000022, "ctau": 1, "mass": 1, "visibleBR": 1 }
}
 ```

Here, `LLP` is the name of this LLP ($N$) and its lifetime and mass is set as $m_N=1\text{ GeV}$ and $c\tau=1\text{ m}$.

The probability `visibleBR` of $N$ decaying into particles that are visible (for the detector considered) are also set to 100%.

### The Event file

The Event file declares the cross section `sigma` (fb) of the hard process simulated by Pythia.
We take the value
$$\sigma(pp\to b\bar b) = 560\text{ $\mu$b}$$
[estimated by the LHCb collaboration (arXiv:v9)](https://arxiv.org/abs/1612.05140v9) for LHC-13.
This value is consistent with the value 506 ub estimated with [FONLL](http://www.lpthe.jussieu.fr/~cacciari/fonll/fonllform.html) for LHC-14.

## Result

You can start the simulation with

```console
> DIR=examples/1_light_neutral_fermion_Bmeson/1_input
> ./bin/ddc $DIR/light_neutralino_test_Events.dat $DIR/light_neutralino_test_LLP.dat output.txt
```

to obtain an output like

```plaintext
AL3X, LLP0:       0.0604456 ,      7.24736e+12
ANUBIS0, LLP0:    4.24207e-05 ,    6.10343e+10
ANUBIS1, LLP0:    3.40169e-05 ,    4.89431e+10
CODEXB0, LLP0:    8.28331e-06 ,    1.19179e+09
CODEXB1, LLP0:    8.42271e-06 ,    1.21185e+09
FACET, LLP0:      0.000255901 ,    3.68186e+11
FASER, LLP0:      4.17493e-08 ,    3.00342e+06
FASER2, LLP0:     8.27475e-06 ,    1.19056e+10
MAPP1, LLP0:      0.000186855 ,    2.68845e+09
MAPP2, LLP0:      0.00035379 ,     5.09029e+10
MATHUSLA0, LLP0:  7.41567e-06 ,    1.06696e+10
MATHUSLA1, LLP0:  5.37804e-06 ,    7.73784e+09
MATHUSLA2, LLP0:  5.58827e-06 ,    8.04032e+09
```

The first number is the acceptance of LLPs and the second is the number of accepted LLPs.
For example, in AL3X experiment,

- cross section is set to 5.6e11 fb,
- luminosity is hard-coded to 250 /fb,
- 1.4e14 pp-to-bb events are expected,
- approximately 6e13 B+ mesons and 6e13 B- mesons are expected,
- 1.2e14 LLPs are produced because B+ and B- are set to decay exclusively to the LLP,
- and 6% of them are accepted in the simulation, which are 7.2e12.

Therefore, if the B- branching ratio to the LLP is 1/(2.4e12), three LLPs are expected at the AL3X experiment.
