# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.5
# ---

# %%
from __future__ import annotations
import sympy as sp
import sympy.plotting as splot
from sympy.core.function import expand
from sympy.core.numbers import (Rational, pi)
from sympy.core.singleton import S
from sympy.core.symbol import (Symbol, symbols)
from sympy.sets.sets import Interval
from sympy.simplify.simplify import simplify
from sympy.physics.continuum_mechanics.beam import Beam
from sympy.functions import SingularityFunction, Piecewise, meijerg, Abs, log, sqrt, factorial
from sympy.testing.pytest import raises, slow
from sympy.physics.units import meter, newton, kilo, giga, milli
from sympy.physics.continuum_mechanics.beam import Beam3D
from sympy.geometry import Circle, Polygon, Point2D, Triangle
from sympy.core.sympify import sympify

from Curved_beam.curved_beam import plot_lever_arms_crown

x = Symbol('x')
y = Symbol('y')
R1, R2 = symbols('R1, R2')


# %% [raw]
# While it is a clever idea to try and use SymPy's built-in `Beam3D` class from the `sympy.physics.continuum_mechanics` module, **it is not a fully accurate port for this specific Maple workbook.** If you attempt to solve the W10X54 I-beam using `Beam3D`, you will encounter fundamental limitations in how SymPy models physics compared to what the Maple document is actually doing.
#
# Here is a verification and code-review of your `Euler_beam_torsion.py` approach:
#
# ### 1. The Missing Physics: Warping Torsion ($C_w$)
#
# The most critical issue is that SymPy's `Beam3D` class is based entirely on classical Euler-Bernoulli beam theory and **Saint-Venant torsion**. It assumes that the torsional stiffness is strictly a function of the shear modulus ($G$) and the torsional constant ($J_T$).
#
# However, a W10X54 is an "open" cross-section. When open sections twist, their cross-sections warp. The Maple workbook explicitly uses the Lin (1977) formulas, which rely on the **Warping Constant ($C_w$)** and the torsional parameter $\lambda = \sqrt{\frac{G \cdot J_T}{E \cdot C_w}}$.
#
# * `Beam3D` has no input for $C_w$.
# * If you apply a torsional moment to `Beam3D`, it will calculate the twist angle without accounting for warping restraint, resulting in deflections and stresses that are **completely incorrect** (often highly overestimated) for an I-beam.
#
# ### 2. Lack of Combined Stress Assessment
#
# The Maple document evaluates specific AISC 360-10 design checks—specifically the combined normal stress at the flange tips:
# $\sigma = \frac{M_x}{S_x} + \frac{2 M_T}{S_y}$
# `Beam3D` handles internal shear and moment diagrams efficiently, but it does not natively map those forces back into cross-sectional extremes using section moduli ($S_x, S_y$). You would still have to manually extract the internal forces from `Beam3D` and script the stress math yourself.
#
# ### 3. No Code-Checking Capabilities
#
# The Maple sheet calculates the critical buckling stress ($F_{cr}$) and the AISC interaction ratio ($\frac{P}{P_c} + \frac{8}{9} ...$). `Beam3D` is a purely elastic solver. It does not know what a yield stress ($F_y$) is, nor can it handle empirical code provisions.
#
# ### The Verdict: Stick to the "Raw" Symbolic Script
#
# Using `Beam3D` is fantastic if you are analyzing a solid rectangular or circular pipe frame in 3D where warping is negligible.
#
# However, for this specific Maple Flow port, the **raw symbolic approach** (defining the equations explicitly using `sympy.symbols` and `sympy.subs` as I provided previously) is much better. It allows you to perfectly mirror the exact Lin (1977) warping formulas and AISC code checks that make the original Maple document valuable, rather than trying to force a standard continuum mechanics solver to understand advanced steel design.

# %%
L=sp.Symbol('L', positive=True)
E = Symbol('E', positive=True)
I = Symbol('I', positive=True)

# %%
import os
print(os.getcwd())

import json5
with open("data/AISC_W10x54_wide_flange_steel_section_torsional_lateral_params.json", "r") as f:
    params = json5.load(f)

from sympy import pprint
pprint(params)

# %%
b = Beam3D(params['L'], params['E'], params['G'], params['Ix'], params['A'])

b.apply_moment_load(params['L']/2, params['F'], -1, dir='x')
b.apply_moment_load(params['L']/2, params['T'], -2, dir='x')
# b.apply_moment_load(25, 10, -2, dir='x')
# b.apply_moment_load(-5, 20, -2, dir='x')

print(b._torsion_moment)

b.applied_loads


# %%
plt=b.draw()
plt.show()

# %%
b.solve_for_torsion()


# %%
b.angular_deflection()
splot.plot(b.angular_deflection())

# %%