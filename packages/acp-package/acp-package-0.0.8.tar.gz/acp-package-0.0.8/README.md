This repository contains the Python implementation of [Approximating Full Conformal Prediction at Scale via Influence Functions](https://arxiv.org/abs/2202.01315).

* [Overview](#overview)
* [Usage](#usage)
* [Reference](#reference)

## Overview

Approximate full Conformal Prediction (ACP) outputs a prediction set that provably contains the true label with at least a probability specified by the practicioner. In large datasets, ACP inherits the statistical power of full Conformal Prediction, yielding tight prediction sets with validity guarantees. The method works as a wrapper for any differentiable ML model.

## Usage

### Requirements

* python 3.6 or higher
* numpy
* torch
* tqdm
* pandas

### Installation

First of all, install the package:

```bash
pip install acp-package
```

### Constructing valid prediction sets

Include the following import in your file:

```bash
from acp.methods import ACP_D #Deleted scheme, import ACP_O for the ordinary scheme
```
Now you can use ACP in your own models. The framework is compatible with any PyTorch model with methods `.predict()` and `.fit()`. 

Once you instantiate your model, wrap ACP around it. ACP allows generating tight prediction sets with validity guarantees.

```bash
ACP = ACP_D(Xtrain, Ytrain, model, seed = SEED, verbose = True)
sets = ACP.predict(Xtest, epsilon, out_file = "results/test")
```

## Reference

Abad J., Bhatt U., Weller A. and Cherubin G. 
“Approximating Full Conformal Prediction at Scale via Influence Functions.” 2022.

 BiBTeX:

```
@inproceedings{Abad2022ApproximatingFC,
  title={Approximating Full Conformal Prediction at Scale via Influence Functions},
  author={Javier Abad and Umang Bhatt and Adrian Weller and Giovanni Cherubin},
  year={2022}
}
```