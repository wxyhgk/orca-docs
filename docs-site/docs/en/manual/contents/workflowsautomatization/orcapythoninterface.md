

<a id="sec:workflowsautomatization.opi"></a>
# ORCA Python Interface (OPI)

!!! warning
    **For comprehensive information on OPI, please refer to the [OPI documentation](https://www.faccts.de/docs/opi/docs) and the [OPI GitHub repository](https://github.com/faccts/opi).**

The ORCA Python interface (OPI) is a versatile tool that provides seamless access to ORCA calculations through Python. The OPI library offers many functions and classes to easily define calculation settings, perform different kinds of ORCA calculations, and process the resulting output data. It is open-source and freely available at [GitHub](https://github.com/faccts/opi). For detailed installation instructions and usage examples, please refer to the official [OPI documentation](https://www.faccts.de/docs/opi/docs).

!!! note "6.1.0"
    The first version of OPI was released with ORCA 6.1. Please note that OPI’s open-source development is managed independently of the ORCA software itself. For the latest updates and changes, consult the [OPI GitHub repository](https://github.com/faccts/opi) and the [OPI documentation](https://www.faccts.de/docs/opi/docs).

## Installation

OPI can either be installed directly from PyPI:

```orca
pip install orca-pi
```

or from GitHub:

```orca
git clone https://github.com/faccts/opi.git
cd opi
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install .
```

In order to use OPI properly we recommend to install it in a venv environment. For more instructions refer to the [OPI documentation](https://www.faccts.de/docs/opi/docs).

