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

# %% [markdown]
# # Cantilever Beam — Direct Stiffness Method (DSM) with `scipy` & `sectionproperties`
#
# This script bridges **10_Sympy** (analytical continuum mechanics) and **30_OpenSees** (FEA) by:
# 1. Computing exact cross-sectional properties ($A, I_{xx}, A_{sy}, Z_{xx}, J$) of a steel I-beam using `sectionproperties`.
# 2. Assembling the global stiffness matrix $\mathbf{K}$ and consistent load vector $\mathbf{F}$ from scratch.
# 3. Solving the partitioned linear system $\mathbf{K}_{ff}\mathbf{u}_f = \mathbf{F}_f$ using `scipy.sparse.linalg.spsolve` and `scipy.linalg.cho_solve`.
# 4. Recovering support reactions, Hermite-interpolated displacements, internal forces ($V, M$), and 2D cross-section stresses at the fixed root.

# %% 1. Imports
from math import isclose
import numpy as np
import scipy.linalg as la
import scipy.sparse as sp_sparse
import scipy.sparse.linalg as spla
import matplotlib.pyplot as plt

from sectionproperties.pre import Material
from sectionproperties.pre.library import i_section
from sectionproperties.analysis import Section

# %% 2. Cross-Section Analysis with sectionproperties
# Define structural steel material (S355, SI units: Pa, m, kg/m^3)
E = 200e9          # Young's modulus (Pa)
nu = 0.3           # Poisson's ratio
G = E / (2.0 * (1.0 + nu))  # Shear modulus (Pa)
fy = 355e6         # Yield strength (Pa)
rho = 7850.0       # Density (kg/m^3)

steel = Material(
    name="S355",
    elastic_modulus=E,
    poissons_ratio=nu,
    yield_strength=fy,
    density=rho,
    color="steelblue",
)

# Create an I-section (d = 300 mm, b = 150 mm, tf = 12 mm, tw = 8 mm, r = 10 mm)
geom = i_section(
    d=0.30,
    b=0.15,
    t_f=0.012,
    t_w=0.008,
    r=0.010,
    n_r=8,
    material=steel,
)
geom = geom.create_mesh(mesh_sizes=[0.005])

sec = Section(geometry=geom)
sec.calculate_geometric_properties()
sec.calculate_warping_properties()

A = sec.get_area()
EA = sec.get_ea()
EIxx, EIyy, EIxy = sec.get_eic()
EAsx, EAsy = sec.get_eas()
EJ = sec.get_ej()
Zxx_plus, Zxx_minus, _, _ = sec.get_ez(e_ref=steel)

Ixx = EIxx / E
Asy = EAsy / E
J = EJ / E

print("=== Cross-Section Properties (sectionproperties) ===")
print(f"  Area (A)              = {A * 1e4:.2f} cm^2  ({A:.6e} m^2)")
print(f"  Second Moment (Ixx)   = {Ixx * 1e8:.2f} cm^4  ({Ixx:.6e} m^4)")
print(f"  Shear Area (Asy)      = {Asy * 1e4:.2f} cm^2  ({Asy:.6e} m^2)")
print(f"  Torsion Constant (J)  = {J * 1e8:.2f} cm^4  ({J:.6e} m^4)")
print(f"  Section Modulus (Zxx) = {Zxx_plus * 1e6:.2f} cm^3  ({Zxx_plus:.6e} m^3)")

# %% 3. Problem Definition & Mesh Discretization
L = 5.0            # Cantilever span (m)
P_tip = -25_000.0  # Point load at free end (N, downward)
q_dist = -4_000.0  # Uniformly distributed load along span (N/m, downward)

n_ele = 10         # Number of 2D frame elements
n_nodes = n_ele + 1
dof_per_node = 3   # [ux, uy, theta_z]
n_dof = n_nodes * dof_per_node

x_nodes = np.linspace(0.0, L, n_nodes)


# %% 4. Element Stiffness Matrix & Work-Equivalent Nodal Loads
def frame2d_local_stiffness(EA: float, EI: float, Le: float, GA_s: float | None = None) -> np.ndarray:
    """
    6x6 local stiffness matrix for a 2D frame element with DOFs [ux1, uy1, rz1, ux2, uy2, rz2].
    If GA_s is provided, Timoshenko shear deformation factor phi = 12*EI / (GA_s * Le^2) is included.
    If GA_s is None, pure Euler-Bernoulli beam theory (phi = 0) is used.
    """
    phi = 0.0 if GA_s is None else (12.0 * EI) / (GA_s * Le**2)
    c = EI / ((1.0 + phi) * Le**3)

    k = np.zeros((6, 6), dtype=float)
    # Axial terms (ux1, ux2)
    k[0, 0] = EA / Le
    k[0, 3] = -EA / Le
    k[3, 0] = -EA / Le
    k[3, 3] = EA / Le

    # Bending & shear terms (uy1, rz1, uy2, rz2)
    k_bend = c * np.array([
        [12.0,          6.0 * Le,              -12.0,          6.0 * Le],
        [6.0 * Le,      (4.0 + phi) * Le**2,   -6.0 * Le,      (2.0 - phi) * Le**2],
        [-12.0,         -6.0 * Le,             12.0,           -6.0 * Le],
        [6.0 * Le,      (2.0 - phi) * Le**2,   -6.0 * Le,      (4.0 + phi) * Le**2],
    ])
    bend_idx = np.ix_([1, 2, 4, 5], [1, 2, 4, 5])
    k[bend_idx] = k_bend
    return k


def frame2d_consistent_udl(qy: float, Le: float) -> np.ndarray:
    """Work-equivalent nodal load vector [fx1, fy1, mz1, fx2, fy2, mz2] for uniform load qy."""
    return np.array([
        0.0,
        0.5 * qy * Le,
        (qy * Le**2) / 12.0,
        0.0,
        0.5 * qy * Le,
        -(qy * Le**2) / 12.0,
    ])


# %% 5. Global Assembly & Solution with scipy
def solve_cantilever_dsm(use_timoshenko: bool = False):
    """Assemble and solve the cantilever DSM system using scipy sparse and Cholesky solvers."""
    K_global = sp_sparse.lil_matrix((n_dof, n_dof), dtype=float)
    F_global = np.zeros(n_dof, dtype=float)
    F_eq_global = np.zeros(n_dof, dtype=float)

    GA_s_val = (G * Asy) if use_timoshenko else None

    for e in range(n_ele):
        Le = x_nodes[e + 1] - x_nodes[e]
        dofs = np.array([
            3 * e, 3 * e + 1, 3 * e + 2,
            3 * (e + 1), 3 * (e + 1) + 1, 3 * (e + 1) + 2,
        ])

        ke = frame2d_local_stiffness(E * A, E * Ixx, Le, GA_s=GA_s_val)
        fe_udl = frame2d_consistent_udl(q_dist, Le)

        K_global[np.ix_(dofs, dofs)] += ke
        F_global[dofs] += fe_udl
        F_eq_global[dofs] += fe_udl

    # Add point load at the free tip (last node, vertical DOF)
    tip_uy_dof = 3 * (n_nodes - 1) + 1
    F_global[tip_uy_dof] += P_tip

    # Boundary Conditions: Fixed at Node 0 (DOFs 0, 1, 2 locked)
    fixed_dofs = np.array([0, 1, 2])
    free_dofs = np.setdiff1d(np.arange(n_dof), fixed_dofs)

    K_csc = K_global.tocsc()
    K_ff = K_csc[free_dofs, :][:, free_dofs]
    K_sf = K_csc[fixed_dofs, :][:, free_dofs]
    F_f = F_global[free_dofs]

    # Method A: Sparse direct solver (SuperLU via scipy.sparse.linalg.spsolve)
    u_free_sparse = spla.spsolve(K_ff, F_f)

    # Method B: Dense Symmetric Positive-Definite Cholesky solver (scipy.linalg.cho_solve)
    c_fac, lower = la.cho_factor(K_ff.toarray())
    u_free_chol = la.cho_solve((c_fac, lower), F_f)
    assert np.allclose(u_free_sparse, u_free_chol, rtol=1e-12)

    # Full displacement vector
    U = np.zeros(n_dof, dtype=float)
    U[free_dofs] = u_free_sparse

    # Support reactions: R_s = K_sf * u_f - F_eq_s
    R_fixed = K_sf.dot(u_free_sparse) - F_eq_global[fixed_dofs]

    return U, R_fixed, K_csc


U_eb, R_eb, K_eb = solve_cantilever_dsm(use_timoshenko=False)
U_timo, R_timo, _ = solve_cantilever_dsm(use_timoshenko=True)

# %% 6. Verification Against Analytical Euler-Bernoulli Solutions
# Exact closed-form formulas (superposition of tip load P and uniform load q)
R_y_exact = -(P_tip + q_dist * L)
M_z_exact = -(P_tip * L + 0.5 * q_dist * L**2)
v_tip_exact = (P_tip * L**3) / (3.0 * E * Ixx) + (q_dist * L**4) / (8.0 * E * Ixx)
theta_tip_exact = (P_tip * L**2) / (2.0 * E * Ixx) + (q_dist * L**3) / (6.0 * E * Ixx)

# Timoshenko additional shear deflection at tip: dv_shear = P*L/(G*Asy) + q*L^2/(2*G*Asy)
v_tip_timo_exact = v_tip_exact + (P_tip * L) / (G * Asy) + (q_dist * L**2) / (2.0 * G * Asy)

v_tip_dsm = U_eb[3 * (n_nodes - 1) + 1]
theta_tip_dsm = U_eb[3 * (n_nodes - 1) + 2]
v_tip_timo_dsm = U_timo[3 * (n_nodes - 1) + 1]

assert isclose(R_eb[1], R_y_exact, rel_tol=1e-12)
assert isclose(R_eb[2], M_z_exact, rel_tol=1e-12)
assert isclose(v_tip_dsm, v_tip_exact, rel_tol=1e-12)
assert isclose(theta_tip_dsm, theta_tip_exact, rel_tol=1e-12)
assert isclose(v_tip_timo_dsm, v_tip_timo_exact, rel_tol=1e-12)

print("\n=== Verification: Scipy DSM vs. Exact Analytical Formulas ===")
print(f"  Vertical Reaction Ry : DSM = {R_eb[1] / 1e3:9.3f} kN   | Exact = {R_y_exact / 1e3:9.3f} kN")
print(f"  Root Moment Mz       : DSM = {R_eb[2] / 1e3:9.3f} kN*m | Exact = {M_z_exact / 1e3:9.3f} kN*m")
print(f"  Tip Deflection (E-B) : DSM = {v_tip_dsm * 1e3:9.4f} mm   | Exact = {v_tip_exact * 1e3:9.4f} mm")
print(f"  Tip Deflection (Timo): DSM = {v_tip_timo_dsm * 1e3:9.4f} mm   | Exact = {v_tip_timo_exact * 1e3:9.4f} mm")
print(f"  Tip Rotation   (E-B) : DSM = {theta_tip_dsm * 1e3:9.4f} mrad | Exact = {theta_tip_exact * 1e3:9.4f} mrad")

# %% 7. Cross-Section Stress Recovery at Fixed Support (sectionproperties)
# Pass the DSM reaction shear and bending moment at the fixed support into sectionproperties
V_root = R_eb[1]
M_root = -R_eb[2]  # Internal hogging moment at x = 0

stress_post = sec.calculate_stress(mxx=M_root, vy=V_root)
sigma_navier_max = abs(M_root) / Zxx_plus

print("\n=== Fixed-End Cross-Section Stress Check ===")
print(f"  Max Bending Stress (|M_root| / Zxx) = {sigma_navier_max / 1e6:.2f} MPa (Yield = {fy / 1e6:.0f} MPa)")
print(f"  Utilization Ratio                   = {sigma_navier_max / fy * 100:.1f}%")

# %% 8. Internal Force & Hermite Deflection Diagrams (Saved as SVG)
x_fine = []
v_fine = []
V_fine = []
M_fine = []

for e in range(n_ele):
    x1, x2 = x_nodes[e], x_nodes[e + 1]
    Le = x2 - x1
    dofs = [3 * e, 3 * e + 1, 3 * e + 2, 3 * (e + 1), 3 * (e + 1) + 1, 3 * (e + 1) + 2]
    ue = U_eb[dofs]

    ke = frame2d_local_stiffness(E * A, E * Ixx, Le)
    fe_udl = frame2d_consistent_udl(q_dist, Le)
    f_int = ke @ ue - fe_udl  # [N1, V1, M1, N2, V2, M2]

    V1, M1 = f_int[1], -f_int[2]
    xi = np.linspace(0.0, 1.0, 25)
    x_loc = x1 + xi * Le

    # Exact cubic Hermite shape functions + particular solution for uniform load q_dist
    N1 = 1.0 - 3.0 * xi**2 + 2.0 * xi**3
    N2 = Le * (xi - 2.0 * xi**2 + xi**3)
    N3 = 3.0 * xi**2 - 2.0 * xi**3
    N4 = Le * (-xi**2 + xi**3)
    v_part = (q_dist * Le**4 / (24.0 * E * Ixx)) * (xi**2 * (1.0 - xi)**2)

    v_loc = N1 * ue[1] + N2 * ue[2] + N3 * ue[4] + N4 * ue[5] + v_part
    V_loc = V1 + q_dist * (x_loc - x1)
    M_loc = M1 + V1 * (x_loc - x1) + 0.5 * q_dist * (x_loc - x1)**2

    x_fine.append(x_loc)
    v_fine.append(v_loc)
    V_fine.append(V_loc)
    M_fine.append(M_loc)

x_plot = np.concatenate(x_fine)
v_plot = np.concatenate(v_fine)
V_plot = np.concatenate(V_fine)
M_plot = np.concatenate(M_fine)

fig, axes = plt.subplots(3, 1, figsize=(9, 8), sharex=True)

axes[0].plot(x_plot, V_plot / 1e3, color="#1f77b4", lw=2, label="Shear $V(x)$")
axes[0].fill_between(x_plot, V_plot / 1e3, color="#1f77b4", alpha=0.15)
axes[0].axhline(0, color="k", lw=0.8)
axes[0].set_ylabel("Shear $V$ (kN)")
axes[0].set_title("Cantilever Beam — Direct Stiffness Method (`scipy` + `sectionproperties`)")
axes[0].grid(True, linestyle="--", alpha=0.5)
axes[0].legend(loc="upper right")

axes[1].plot(x_plot, M_plot / 1e3, color="#d62728", lw=2, label="Bending Moment $M(x)$")
axes[1].fill_between(x_plot, M_plot / 1e3, color="#d62728", alpha=0.15)
axes[1].axhline(0, color="k", lw=0.8)
axes[1].set_ylabel("Moment $M$ (kN·m)")
axes[1].grid(True, linestyle="--", alpha=0.5)
axes[1].legend(loc="lower right")

axes[2].plot(x_plot, v_plot * 1e3, color="#2ca02c", lw=2, label="Hermite Deflection $v(x)$")
axes[2].plot(x_nodes, U_eb[1::3] * 1e3, "ko", ms=4, label="DSM Nodal DOFs")
axes[2].axhline(0, color="k", lw=0.8)
axes[2].set_xlabel("Position along beam $x$ (m)")
axes[2].set_ylabel("Deflection $v$ (mm)")
axes[2].grid(True, linestyle="--", alpha=0.5)
axes[2].legend(loc="lower left")

plt.tight_layout()
plt.savefig("cantilever_dsm_results.svg", bbox_inches="tight")
plt.show()
