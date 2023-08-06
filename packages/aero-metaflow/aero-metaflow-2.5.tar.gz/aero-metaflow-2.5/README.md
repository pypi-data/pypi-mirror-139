![Metaflow_Logo_Horizontal_FullColor_Ribbon_Dark_RGB](https://user-images.githubusercontent.com/763451/89453116-96a57e00-d713-11ea-9fa6-82b29d4d6eff.png)

# Aero Metaflow

This library contains a fork of Metaflow (http://metaflow.org/) which is used by Aero to orchestrate Jobs.

While this library has been heavily edited in parts, credit still goes to the amazing work the Metaflow team have done.
For more information, see [Metaflow's website](https://metaflow.org) and [documentation](https://docs.metaflow.org).

## Getting Started

Getting up and running with Metaflow is easy. 

### Python
Install metaflow from [pypi](https://pypi.org/project/metaflow/):

```sh
pip install metaflow
```

and access tutorials by typing:

```sh
metaflow tutorials pull
```

### R

Install Metaflow from [github](https://github.com/Netflix/metaflow/tree/master/R):

```R
devtools::install_github("Netflix/metaflow", subdir="R")
metaflow::install()
```

and access tutorials by typing:

```R
metaflow::pull_tutorials()
```

## Get in Touch
There are several ways to get in touch with us:

* Open an issue at: https://github.com/Netflix/metaflow 
* Email us at: help@metaflow.org
* Chat with us on: http://chat.metaflow.org 

## Contributing

We welcome contributions to Metaflow. Please see our [contribution guide](https://docs.metaflow.org/introduction/contributing-to-metaflow) for more details.

### Code style

We use [black](https://black.readthedocs.io/en/stable/) as a code formatter. The easiest way to ensure your commits are always formatted with the correct version of `black` it is to use [pre-commit](https://pre-commit.com/): install it and then run `pre-commit install` once in your local copy of the repo. 
