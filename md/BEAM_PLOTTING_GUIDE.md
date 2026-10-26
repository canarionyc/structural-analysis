# Beam Analysis Plotting Guide

## Overview
The `plot_beam_analysis.py` script provides comprehensive numerical plotting of beam deflection, shear forces, and bending moments for different beam configurations and loading conditions.

## Features

✓ **Shear Force Diagrams** - Visualize internal shear forces along the beam
✓ **Bending Moment Diagrams** - Visualize internal bending moments along the beam  
✓ **Deflection Curves** - Visualize beam deflection under loads
✓ **Multiple Configurations** - Simply supported and cantilever beams included
✓ **Numerical Analysis** - Real-world material properties and loading conditions
✓ **Professional Plots** - Publication-quality figures with proper labeling

## Running the Script

### Basic Usage
```bash
python plot_beam_analysis.py
```

This will:
1. Analyze a simply supported beam with a 1000 N point load
2. Analyze a cantilever beam with a 2000 N point load at the free end
3. Generate shear force, bending moment, and deflection plots for each
4. Save plots as PNG files: `simply_supported_beam.png` and `cantilever_beam.png`

## Customizing Beam Parameters

### Simply Supported Beam with Point Load

Edit the `simply_supported_beam_point_load()` function to modify:

```python
# Beam parameters
L_beam = 10.0  # Length in meters
P_load = 1000  # Point load in N
a_load = 4.0   # Position of load from left support
b_load = L_beam - a_load
E_mod = 210e9  # Young's modulus (Pa) - steel
I_moment = 83e-6  # Moment of inertia (m^4)
```

**Common Material Properties:**
- **Steel**: E = 210 GPa (2.1e11 Pa)
- **Aluminum**: E = 69 GPa (6.9e10 Pa)
- **Concrete**: E = 30-40 GPa (3-4e10 Pa)
- **Wood**: E = 10-13 GPa (1-1.3e10 Pa)

**Moment of Inertia Formulas:**
- Rectangular section: I = b*h³/12 (b = width, h = height)
- Circular section: I = π*d⁴/64 (d = diameter)
- Hollow circular: I = π*(d_o⁴ - d_i⁴)/64

### Cantilever Beam with Point Load

Edit the `cantilever_beam_point_load()` function:

```python
L_beam = 5.0  # Length in meters
P_load = 2000  # Point load in N at free end
E_mod = 210e9  # Young's modulus (Pa)
I_moment = 50e-6  # Moment of inertia (m^4)
```

## Understanding the Output

### 1. Shear Force Diagram
- **Top plot** shows internal shear forces at each position
- **Positive values** indicate upward shear (typically on left face of cut section)
- **Discontinuities** appear where point loads are applied
- **Units**: Newtons (N)

### 2. Bending Moment Diagram
- **Middle plot** shows internal bending moments
- **Positive moments** cause compression on top fiber
- **Peak moment** typically occurs where shear force changes sign
- **Units**: Newton-meters (N⋅m)

### 3. Deflection Curve
- **Bottom plot** shows beam displacement under load
- **Inverted** so downward deflection appears as negative (physics convention)
- **Maximum deflection** often at points of maximum positive moment
- **Units**: Millimeters (mm)
- **Boundary conditions**:
  - Simply supported: zero deflection at both ends
  - Cantilever: zero deflection and zero slope at fixed end

## Key Formulas Used

### Simply Supported Beam with Point Load

**Reactions:**
- R_A = P*b/L
- R_B = P*a/L

**Maximum Moment:**
- M_max = P*a*b/L (occurs at x = a when a < L/2)

**Maximum Deflection:**
- δ_max = P*a²*b²/(3*E*I*L) (for a ≤ b)

### Cantilever Beam with Point Load at Free End

**Reaction at Fixed End:**
- R = P
- M = P*L

**Maximum Deflection:**
- δ_max = P*L³/(3*E*I) (at free end)

## Adding More Load Cases

To add more loading scenarios, create a new function following this template:

```python
def custom_beam_case():
    """Your beam configuration description"""
    
    # Parameters
    L_beam = ...
    E_mod = ...
    I_moment = ...
    
    def shear_force(x):
        """Return shear force at position x"""
        return ...
    
    def bending_moment(x):
        """Return bending moment at position x"""
        return ...
    
    def deflection(x):
        """Return deflection at position x"""
        return ...
    
    return {
        'L': L_beam,
        'P': P_load,  # Primary load for labeling
        'E': E_mod,
        'I': I_moment,
        'shear_force': shear_force,
        'bending_moment': bending_moment,
        'deflection': deflection
    }
```

Then call it from `main()`:
```python
beam_data = custom_beam_case()
fig = plot_combined_view(beam_data, "Your Beam Name")
fig.savefig('output_name.png', dpi=150, bbox_inches='tight')
plt.show()
```

## Plotting Functions

### `plot_beam_diagrams(beam_data, beam_name)`
Creates three separate plots (one per subplot):
- Useful for academic reports
- Clean, focused visualization
- Returns matplotlib figure object

### `plot_combined_view(beam_data, beam_name)`
Creates integrated visualization with:
- Beam diagram with loads and supports
- Shear force diagram
- Bending moment diagram
- Deflection curve
- Better for presentations and design reports

## Physical Interpretation

### Sign Conventions
- **Shear Force**: Positive values act upward on left face of cut
- **Bending Moment**: Positive values cause compression on top fiber (sagging)
- **Deflection**: Negative values indicate downward displacement

### Critical Values to Check
1. **Maximum Moment**: Drives stress calculations (σ = M*c/I)
2. **Maximum Deflection**: Serviceability criterion (typically L/250 or L/360)
3. **Shear Force**: Important at supports and near point loads

### Design Workflow
1. Calculate reactions (shown in console output)
2. Identify maximum moment and shear locations
3. Select appropriate beam section (check moment of inertia)
4. Verify deflection is within allowable limits
5. Check stress: σ = M*y/I ≤ σ_allowable

## Troubleshooting

**Plots don't appear:**
- Check that matplotlib is installed: `pip install matplotlib`
- If running in headless environment, save to files only (plots are already saved)

**Values seem wrong:**
- Verify units are consistent (metric vs imperial)
- Check moment of inertia calculation
- Ensure Young's modulus is correct for material

**Need distributed loads:**
- Edit the function to integrate distributed load effects
- Example: w*L/2 contributes to both shear and moment

## References

- **Classical Beam Theory**: Timoshenko & Young, "Engineering Mechanics"
- **Formula References**: AISC Manual of Steel Construction
- **Mechanics of Materials**: Beer, Johnston & DeWolf

## Example Output Interpretation

For the simply supported beam example:
- **Beam Length**: 10 m
- **Point Load**: 1000 N at 4 m from left
- **Reactions**: R_A = 600 N, R_B = 400 N
- **Max Moment**: 2400 N⋅m (at load location)
- **Max Deflection**: 1.10 mm (at x ≈ 5.77 m)

This represents excellent deflection control (L/9091 << L/250).

---

For more information, see examples in the `examples/` directory and Euler Beam notebooks.
