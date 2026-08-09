#!/usr/bin/env python
"""
Beam Analysis Plotting Script
Plot numerical deflection, moments, and shears along a beam.

This script demonstrates plotting for a simply supported beam with point load,
and can be adapted for other boundary conditions and loading.
"""

import sys
import os

import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# from autoimport import import_all
# import_all()

def simply_supported_beam_point_load():
    """
    Analysis of simply supported beam with point load.
    Returns numerical functions for shear, moment, and deflection.
    """
    
    # Beam parameters
    L_beam = 10.0  # Length in meters
    P_load = 1000  # Point load in N
    a_load = 4.0   # Position of load from left support
    b_load = L_beam - a_load
    E_mod = 210e9  # Young's modulus (Pa) - steel
    I_moment = 83e-6  # Moment of inertia (m^4)
    
    # Reactions
    R_A = P_load * b_load / L_beam
    R_B = P_load * a_load / L_beam
    
    print(f"Beam Configuration:")
    print(f"  Length: {L_beam} m")
    print(f"  Point Load: {P_load} N at x = {a_load} m")
    print(f"  Young's Modulus: {E_mod:.2e} Pa")
    print(f"  Moment of Inertia: {I_moment:.2e} m^4")
    print(f"\nReactions:")
    print(f"  R_A (left support): {R_A:.2f} N")
    print(f"  R_B (right support): {R_B:.2f} N")
    
    def shear_force(x):
        """Shear force diagram"""
        if x < a_load:
            return R_A
        else:
            return R_A - P_load
    
    def bending_moment(x):
        """Bending moment diagram"""
        if x <= a_load:
            return R_A * x
        else:
            return R_A * x - P_load * (x - a_load)
    
    def deflection(x):
        """Deflection curve using double integration method"""
        if x <= a_load:
            # First segment: 0 <= x <= a
            term1 = -P_load * b_load * (L_beam**2 - b_load**2) * x / (6 * E_mod * I_moment * L_beam)
            term2 = P_load * b_load * x**3 / (6 * E_mod * I_moment * L_beam)
            return term1 + term2
        else:
            # Second segment: a < x <= L
            term1 = -P_load * b_load * (L_beam**2 - b_load**2) * x / (6 * E_mod * I_moment * L_beam)
            term2 = P_load * a_load * (x - a_load)**3 / (6 * E_mod * I_moment * L_beam)
            term3 = -P_load * (x - a_load) * (L_beam**2 - b_load**2 - (x - a_load)**2) / (6 * E_mod * I_moment * L_beam)
            return term1 + term2 + term3
    
    return {
        'L': L_beam,
        'P': P_load,
        'a': a_load,
        'b': b_load,
        'E': E_mod,
        'I': I_moment,
        'R_A': R_A,
        'R_B': R_B,
        'shear_force': shear_force,
        'bending_moment': bending_moment,
        'deflection': deflection
    }

def cantilever_beam_point_load():
    """
    Analysis of cantilever beam with point load at free end.
    """
    
    # Beam parameters
    L_beam = 5.0  # Length in meters
    P_load = 2000  # Point load in N at free end
    E_mod = 210e9  # Young's modulus (Pa) - steel
    I_moment = 50e-6  # Moment of inertia (m^4)
    
    # Reactions at fixed end
    R_A = P_load
    M_A = P_load * L_beam
    
    print(f"Beam Configuration (Cantilever):")
    print(f"  Length: {L_beam} m")
    print(f"  Point Load: {P_load} N at free end")
    print(f"  Young's Modulus: {E_mod:.2e} Pa")
    print(f"  Moment of Inertia: {I_moment:.2e} m^4")
    print(f"\nReactions (at fixed end):")
    print(f"  Reaction: {R_A:.2f} N")
    print(f"  Moment: {M_A:.2f} N·m")
    
    def shear_force(x):
        """Shear force - constant along beam"""
        return -P_load
    
    def bending_moment(x):
        """Bending moment"""
        return P_load * (L_beam - x)
    
    def deflection(x):
        """Deflection for cantilever with point load at free end"""
        return P_load * x**2 * (3 * L_beam - x) / (6 * E_mod * I_moment)
    
    return {
        'L': L_beam,
        'P': P_load,
        'E': E_mod,
        'I': I_moment,
        'R_A': R_A,
        'M_A': M_A,
        'shear_force': shear_force,
        'bending_moment': bending_moment,
        'deflection': deflection
    }

def plot_beam_diagrams(beam_data, beam_name="Beam Analysis"):
    """
    Create comprehensive plots for shear force, bending moment, and deflection.
    """
    
    L = beam_data['L']
    x_vals = np.linspace(0, L, 200)
    
    # Calculate values along beam
    shear_vals = np.array([beam_data['shear_force'](x) for x in x_vals])
    moment_vals = np.array([beam_data['bending_moment'](x) for x in x_vals])
    defl_vals = np.array([beam_data['deflection'](x) for x in x_vals]) * 1000  # Convert to mm
    
    # Create figure with three subplots
    fig, axes = plt.subplots(3, 1, figsize=(14, 10))
    fig.suptitle(beam_name, fontsize=16, fontweight='bold')
    
    # 1. Shear Force Diagram
    ax1 = axes[0]
    ax1.plot(x_vals, shear_vals, 'b-', linewidth=2.5, label='Shear Force')
    ax1.fill_between(x_vals, shear_vals, 0, alpha=0.3, color='blue')
    ax1.axhline(y=0, color='k', linestyle='-', linewidth=0.8)
    ax1.grid(True, alpha=0.3)
    ax1.set_ylabel('Shear Force (N)', fontsize=11, fontweight='bold')
    ax1.set_title('Shear Force Diagram', fontsize=12, fontweight='bold')
    ax1.legend(loc='best', fontsize=10)
    
    # Add annotations for key values
    max_shear = np.max(np.abs(shear_vals))
    if max_shear > 0:
        ax1.set_ylim(-max_shear * 1.2, max_shear * 1.2)
    
    # 2. Bending Moment Diagram
    ax2 = axes[1]
    ax2.plot(x_vals, moment_vals, 'r-', linewidth=2.5, label='Bending Moment')
    ax2.fill_between(x_vals, moment_vals, 0, alpha=0.3, color='red')
    ax2.axhline(y=0, color='k', linestyle='-', linewidth=0.8)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylabel('Bending Moment (N·m)', fontsize=11, fontweight='bold')
    ax2.set_title('Bending Moment Diagram', fontsize=12, fontweight='bold')
    ax2.legend(loc='best', fontsize=10)
    
    # Add annotations for key values
    max_moment = np.max(np.abs(moment_vals))
    if max_moment > 0:
        ax2.set_ylim(-max_moment * 1.2, max_moment * 1.2)
    
    # 3. Deflection Curve
    ax3 = axes[2]
    ax3.plot(x_vals, defl_vals, 'g-', linewidth=2.5, label='Deflection')
    ax3.fill_between(x_vals, defl_vals, 0, alpha=0.3, color='green')
    ax3.axhline(y=0, color='k', linestyle='-', linewidth=0.8)
    ax3.grid(True, alpha=0.3)
    ax3.set_xlabel('Position along beam (m)', fontsize=11, fontweight='bold')
    ax3.set_ylabel('Deflection (mm)', fontsize=11, fontweight='bold')
    ax3.set_title('Deflection Curve', fontsize=12, fontweight='bold')
    ax3.legend(loc='best', fontsize=10)
    ax3.invert_yaxis()  # Invert to show downward deflection as negative
    
    # Add annotations for key values
    max_defl = np.max(np.abs(defl_vals))
    if max_defl > 0:
        ax3.set_ylim(max_defl * 1.2, -max_defl * 1.2)
    
    plt.tight_layout()
    return fig

def plot_combined_view(beam_data, beam_name="Beam Analysis"):
    """
    Create a combined visualization with beam diagram and analysis plots.
    """
    
    L = beam_data['L']
    x_vals = np.linspace(0, L, 200)
    
    # Calculate values
    shear_vals = np.array([beam_data['shear_force'](x) for x in x_vals])
    moment_vals = np.array([beam_data['bending_moment'](x) for x in x_vals])
    defl_vals = np.array([beam_data['deflection'](x) for x in x_vals]) * 1000
    
    # Create figure
    fig = plt.figure(figsize=(14, 12))
    gs = fig.add_gridspec(4, 1, hspace=0.4)
    
    # 1. Beam diagram (top)
    ax_beam = fig.add_subplot(gs[0])
    beam_height = 0.3
    ax_beam.add_patch(plt.Rectangle((0, -beam_height/2), L, beam_height, 
                                     color='lightgray', ec='black', linewidth=2))
    
    # Add supports
    if 'a' in beam_data:  # Simply supported
        # Left support
        ax_beam.plot(0, -beam_height/2, 'v', color='black', markersize=15, markerfacecolor='black')
        ax_beam.text(0, -beam_height/2 - 0.2, 'A', ha='center', fontsize=10, fontweight='bold')
        # Right support
        ax_beam.plot(L, -beam_height/2, 'v', color='black', markersize=15, markerfacecolor='black')
        ax_beam.text(L, -beam_height/2 - 0.2, 'B', ha='center', fontsize=10, fontweight='bold')
        # Load arrow
        load_pos = beam_data.get('a', L/2)
        ax_beam.arrow(load_pos, beam_height/2 + 0.3, 0, -0.5, 
                     head_width=0.2, head_length=0.1, fc='red', ec='red', linewidth=2)
        ax_beam.text(load_pos, beam_height/2 + 0.6, f"P={beam_data['P']:.0f}N", 
                    ha='center', fontsize=10, fontweight='bold', color='red')
    else:  # Cantilever
        # Fixed support
        for i in range(5):
            ax_beam.plot([0, -0.15], [i*0.15-0.3, i*0.15-0.3], 'k-', linewidth=2)
        ax_beam.text(-0.3, 0, 'Fixed', ha='right', fontsize=10, fontweight='bold')
        # Load arrow
        ax_beam.arrow(L, beam_height/2 + 0.3, 0, -0.5, 
                     head_width=0.2, head_length=0.1, fc='red', ec='red', linewidth=2)
        ax_beam.text(L, beam_height/2 + 0.6, f"P={beam_data['P']:.0f}N", 
                    ha='center', fontsize=10, fontweight='bold', color='red')
    
    ax_beam.set_xlim(-0.5, L + 0.5)
    ax_beam.set_ylim(-1.2, 1.2)
    ax_beam.set_aspect('equal')
    ax_beam.axis('off')
    ax_beam.set_title(f'{beam_name} - Beam Diagram', fontsize=12, fontweight='bold', pad=10)
    
    # 2. Shear Force
    ax_shear = fig.add_subplot(gs[1])
    ax_shear.plot(x_vals, shear_vals, 'b-', linewidth=2.5)
    ax_shear.fill_between(x_vals, shear_vals, 0, alpha=0.3, color='blue')
    ax_shear.axhline(y=0, color='k', linestyle='-', linewidth=0.8)
    ax_shear.grid(True, alpha=0.3)
    ax_shear.set_ylabel('Shear (N)', fontsize=11, fontweight='bold')
    ax_shear.set_title('Shear Force Diagram', fontsize=11, fontweight='bold')
    
    # 3. Moment
    ax_moment = fig.add_subplot(gs[2])
    ax_moment.plot(x_vals, moment_vals, 'r-', linewidth=2.5)
    ax_moment.fill_between(x_vals, moment_vals, 0, alpha=0.3, color='red')
    ax_moment.axhline(y=0, color='k', linestyle='-', linewidth=0.8)
    ax_moment.grid(True, alpha=0.3)
    ax_moment.set_ylabel('Moment (N·m)', fontsize=11, fontweight='bold')
    ax_moment.set_title('Bending Moment Diagram', fontsize=11, fontweight='bold')
    
    # 4. Deflection
    ax_defl = fig.add_subplot(gs[3])
    ax_defl.plot(x_vals, defl_vals, 'g-', linewidth=2.5)
    ax_defl.fill_between(x_vals, defl_vals, 0, alpha=0.3, color='green')
    ax_defl.axhline(y=0, color='k', linestyle='-', linewidth=0.8)
    ax_defl.grid(True, alpha=0.3)
    ax_defl.set_xlabel('Position along beam (m)', fontsize=11, fontweight='bold')
    ax_defl.set_ylabel('Deflection (mm)', fontsize=11, fontweight='bold')
    ax_defl.set_title('Deflection Curve', fontsize=11, fontweight='bold')
    ax_defl.invert_yaxis()
    
    fig.suptitle(f'{beam_name}', fontsize=14, fontweight='bold', y=0.995)
    
    return fig

def main():
    """Main analysis function"""
    
    print("="*60)
    print("BEAM ANALYSIS - Deflection, Moments, and Shears Plotting")
    print("="*60)
    
    # Example 1: Simply Supported Beam
    print("\n" + "="*60)
    print("Example 1: Simply Supported Beam with Point Load")
    print("="*60)
    beam1_data = simply_supported_beam_point_load()
    
    max_defl = beam1_data['deflection'](beam1_data['a'])
    max_moment = beam1_data['bending_moment'](beam1_data['a'])
    
    print(f"\nKey Results:")
    print(f"  Maximum deflection: {max_defl*1000:.4f} mm (at x = {beam1_data['a']} m)")
    print(f"  Maximum bending moment: {max_moment:.2f} N·m (at x = {beam1_data['a']} m)")
    
    fig1 = plot_combined_view(beam1_data, 
                             "Simply Supported Beam - Point Load")
    fig1.savefig('simply_supported_beam.png', dpi=150, bbox_inches='tight')
    print("\n[OK] Plot saved: simply_supported_beam.png")
    
    # Example 2: Cantilever Beam
    print("\n" + "="*60)
    print("Example 2: Cantilever Beam with Point Load")
    print("="*60)
    beam2_data = cantilever_beam_point_load()
    
    max_defl = beam2_data['deflection'](beam2_data['L'])
    max_moment = beam2_data['bending_moment'](0)
    
    print(f"\nKey Results:")
    print(f"  Maximum deflection: {max_defl*1000:.4f} mm (at free end)")
    print(f"  Maximum bending moment: {max_moment:.2f} N·m (at fixed end)")
    
    fig2 = plot_combined_view(beam2_data, 
                             "Cantilever Beam - Point Load")
    fig2.savefig('cantilever_beam.png', dpi=150, bbox_inches='tight')
    print("\n[OK] Plot saved: cantilever_beam.png")
    
    # Show plots
    plt.show()
    
    print("\n" + "="*60)
    print("Analysis Complete!")
    print("="*60)

if __name__ == '__main__':
    main()