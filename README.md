# pyStructuralAnalysis

A collection of Python notebooks and scripts for structural analysis calculations using symbolic computation and numerical methods.

## Features

- **autoimport.py**: Common imports and functionality (numpy, matplotlib, sympy, pint)
- **Notebooks**: Interactive Jupyter notebooks for structural analysis
- **Scripts**: Python scripts for specific analysis tasks
- **Examples**: Simple examples to get started

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

### Using autoimport in scripts

```python
# Add to path and import common functionality
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from autoimport import import_all
import_all()

# Now you have access to: np, plt, sp, ureg, and common structural symbols
print(f"Beam length: {L}")
deflection = P * L**3 / (48 * E * I)
```

### Using autoimport in notebooks

```python
# In a Jupyter notebook cell
import sys
sys.path.append("..")
from autoimport import import_all
import_all()
```

## Available Symbols

The autoimport module provides these commonly used structural analysis symbols:
- Geometric: `x, y, z, L, a, b, h`
- Material properties: `E, G, nu` (Young's modulus, shear modulus, Poisson's ratio)
- Section properties: `I, A, J` (moment of inertia, area, torsional constant)
- Loads and reactions: `P, q, M, R_A, R_B, M_A, M_B`

## Directory Structure

```
pyStructuralAnalysis/
├── autoimport.py           # Common imports and functionality
├── notebooks/              # Jupyter notebooks
│   ├── basic_structural_analysis.ipynb
│   └── euler_beam_point_load.ipynb
├── scripts/                # Python scripts
│   └── euler_beam_analysis.py
├── examples/               # Simple examples
│   └── example.py
├── docs/                   # Documentation
├── tests/                  # Test files
└── requirements.txt        # Dependencies
```

## Examples

See the `examples/` directory for simple getting-started examples, and `scripts/` for more detailed analysis scripts.
