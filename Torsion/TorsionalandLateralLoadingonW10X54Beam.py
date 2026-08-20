# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.5
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import sympy as sp
import math

# %%
Cw, JT, Sx, Sy, A, Zx, Ix, Iy, d, rx = sp.symbols('Cw JT Sx Sy A Zx Ix Iy d rx')
w, F, T, P, Lx, L, Fy, Lb, Ly, E, G, K = sp.symbols('w F T P Lx L Fy Lb Ly E G K')
Omega = sp.symbols('Omega')

# %%
# Torsional property
lam = sp.sqrt((G * JT) / (E * Cw))

# %%
# Governing Moments
Mx = (w * L**2) / 8
My = (F * L) / 4
M0 = (T * L) / (4 * d)
beta = (4 * sp.sinh(lam * L / 2)**2) / (lam * L * sp.sinh(lam * L))
MT = beta * M0


# %%
# Torsional Capacity Check
xi_bx = (Mx / Sx) + (2 * MT / Sy)
Fnx = Fy / Omega

# %%
# Combined Compression and Bending
Mrx = ((Mx / Sx) + (2 * MT / Sy)) * Sx
Fe = (sp.pi**2 * E) / ((K * L / rx)**2)
# Fcr uses a piecewise logic in actual AISC, but mirroring the document's specific state:
Fcr = (0.658**(Fy / Fe)) * Fy
Pn = Fcr * A
Pc = Pn / Omega

Mn = sp.Min(Fy * Zx, Fy * Sx)
Mcx = Mn / Omega
Mcy = Mn / Omega # Simplified mapping from document

interaction_ratio = (P / Pc) + (8 / 9) * ((Mrx / Mcx) + (My / Mcy))


# %%
# Deflections
phi = (T / (2 * G * JT * lam)) * ((lam * L / 2) - (2 * sp.sinh(lam * L / 2) / sp.sinh(lam * L))) * sp.sinh(lam * L / 2)
I3 = Ix * sp.cos((90 - phi) * sp.pi / 180)**2 + Iy * sp.sin((90 - phi) * sp.pi / 180)**2
I4 = Ix * sp.cos((90 - phi) * sp.pi / 180)**2 + Iy * sp.sin((90 - phi) * sp.pi / 180)**2

Delta_vert = (5 * w * L**4) / (384 * E * I3)
Delta_horiz = (F * L**3) / (48 * E * I4)

# %%
# 3. Parameter Dictionary (Base units: kips, inches)
# Note: Lengths in ft are converted to inches (ft * 12) for consistency.
# params = {
#     Cw: 1.2e3, JT: 1.51, Sx: 60, Sy: 20.6, A: 15.8, # [cite: 14, 16, 18, 20, 22]
#     Zx: 66.6, Ix: 303, Iy: 103, d: 10.1, rx: 4.37,  # [cite: 24, 26, 28, 30, 36]
#     w: 1.15 / 12, # kipf/in (converted from 1.15 kipf/ft) [cite: 33]
#     F: 5, T: 5.1 * 12, P: 96, # [cite: 35, 39, 41]
#     Lx: 15 * 12, L: 25 * 12, Lb: 15 * 12, Ly: 7.5 * 12, # [cite: 43, 48, 50, 54]
#     Fy: 50, E: 29000, G: 11200, # [cite: 49, 55, 56]
#     Omega: 1.67, K: 0.85 # [cite: 63, 77]
# }

import os
print(os.getcwd())
import json5
with open("../data/AISC_W10x54_wide_flange_steel_section_torsional_lateral_params.json", "r") as f:
    params = json5.load(f)


# %%
# 4. Evaluation Engine
def evaluate_symbolic(equation, name="Result"):
    # Substitute parameters and evaluate to a float
    val = equation.subs(params).evalf()
    print(f"{name}: {val:.4f}")

print("--- Torsional & Lateral Loading Analysis ---")
evaluate_symbolic(lam, "Torsional Property (lambda)")
evaluate_symbolic(Mx, "Flexural Moment X (Mx)")
evaluate_symbolic(MT, "Torsional Moment (MT)")
evaluate_symbolic(xi_bx, "Max Combined Normal Stress")
evaluate_symbolic(interaction_ratio, "Interaction Ratio")
evaluate_symbolic(phi, "Max Twist Angle (degrees)")
evaluate_symbolic(Delta_vert, "Vertical Deflection (inches)")
evaluate_symbolic(Delta_horiz, "Horizontal Deflection (inches)")