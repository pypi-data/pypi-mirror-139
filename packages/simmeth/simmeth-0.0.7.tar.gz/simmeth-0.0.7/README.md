# Simulation Methods - Wiki

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

Simple python package to test simulation methods.

# Getting Started

## Installation :hammer:

```commandline
pip install simmeth
```

## Basic Usage

To set up a simulation simply create an instance of `Simulation` class. In order to run the simulation call `run()` on
simulation object.

```python
from simmeth.simulation import Simulation

env_scenarios = [
    {
        'prefix': "no_turb",
        'turb': 0,
        'max_confidence': 1,
        'unlearn': True
    }
]
sim = Simulation(scenarios=env_scenarios, n_strategies=3, t=100, n=100)
sim.run()
```