"""Showcase the eurocodepy.section_properties helper module.

This submodule computes transformed-section properties for cracked and uncracked
RC sections (including prestressing effects), useful for serviceability and
cross-section checks.
"""

import numpy as np

from eurocodepy import section_properties as sp


def demo_rectangular_section() -> None:
    """Compute cracked and uncracked properties for a rectangular RC section."""
    h = 0.6
    b = 0.3
    A_s = np.array([1.5e-4])
    A_sc = np.array([1.0e-4])
    A_p = np.array([0.0])
    ds = np.array([0.52])
    dsc = np.array([0.08])
    dp = np.array([0.00])
    alpha_Es = 15.0
    alpha_Ep = 15.0
    M = 120000.0
    P = 50000.0

    uncracked, cracked = sp.calc_section_rectangular(
        h, b, A_s, A_sc, A_p, ds, dsc, dp, alpha_Es, alpha_Ep, M, P
    )

    print("Rectangular RC section — transformed section properties")
    print(f"  Area (uncracked): {uncracked['Area']:.6f} m²")
    print(f"  Area (cracked):   {cracked['Area']:.6f} m²")
    print(f"  Inertia (uncracked): {uncracked['Inertia']:.6f} m^4")
    print(f"  Inertia (cracked):   {cracked['Inertia']:.6f} m^4")
    print(f"  Neutral axis (uncracked): {uncracked['NeutralAxis']:.6f} m")
    print(f"  Neutral axis (cracked):   {cracked['NeutralAxis']:.6f} m")
    print()


def demo_t_section() -> None:
    """Compute cracked/uncracked T-section properties."""
    h = 0.8
    bw = 0.25
    bf = 0.5
    hf = 0.15
    A_s = np.array([1.8e-4])
    A_sc = np.array([1.1e-4])
    A_p = np.array([2.0e-4])
    ds = np.array([0.72])
    dsc = np.array([0.08])
    dp = np.array([0.60])
    alpha_Es = 15.0
    alpha_Ep = 15.0
    M = 180000.0
    P = 70000.0

    uncracked, cracked = sp.calc_section_T(
        h, bw, bf, hf, A_s, A_sc, A_p, ds, dsc, dp, alpha_Es, alpha_Ep, M, P
    )

    print("T-section — transformed section properties")
    print(f"  Area (uncracked): {uncracked['Area']:.6f} m²")
    print(f"  Area (cracked):   {cracked['Area']:.6f} m²")
    print(f"  Inertia (uncracked): {uncracked['Inertia']:.6f} m^4")
    print(f"  Inertia (cracked):   {cracked['Inertia']:.6f} m^4")
    print(f"  Neutral axis (uncracked): {uncracked['NeutralAxis']:.6f} m")
    print(f"  Neutral axis (cracked):   {cracked['NeutralAxis']:.6f} m")
    print()


if __name__ == "__main__":
    demo_rectangular_section()
    demo_t_section()