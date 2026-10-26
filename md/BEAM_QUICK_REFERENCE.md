# Quick Reference: Common Beam Configurations

## Formula Summary for Standard Cases

### 1. Simply Supported Beam - Point Load at Center
```
Configuration:  A ----P---- B
                0     L/2    L

Reactions:
  R_A = P/2
  R_B = P/2

Max Moment:
  M_max = P*L/4  (at center)

Max Deflection:
  δ_max = P*L³/(48*E*I)  (at center)
```

### 2. Simply Supported Beam - Point Load at Arbitrary Position
```
Configuration:  A ----P---- B
                0     a    L

Reactions:
  R_A = P*b/L  (where b = L-a)
  R_B = P*a/L

Max Moment:
  M_max = P*a*b/L  (at x = a)

Max Deflection:
  δ_max = P*a²*b²/(3*E*I*L)  (when a < b)
```

### 3. Simply Supported Beam - Uniform Load
```
Configuration:  A --w/length-- B
                0              L

Reactions:
  R_A = w*L/2
  R_B = w*L/2

Max Moment:
  M_max = w*L²/8  (at center)

Max Deflection:
  δ_max = 5*w*L⁴/(384*E*I)  (at center)
```

### 4. Cantilever Beam - Point Load at Free End
```
Configuration:  ■ ----P
                0      L

Reaction at Fixed End:
  R = P
  M = P*L

Max Moment:
  M_max = P*L  (at fixed end)

Max Deflection:
  δ_max = P*L³/(3*E*I)  (at free end)
```

### 5. Cantilever Beam - Uniform Load
```
Configuration:  ■ --w/length--
                0            L

Reaction at Fixed End:
  R = w*L
  M = w*L²/2

Max Moment:
  M_max = w*L²/2  (at fixed end)

Max Deflection:
  δ_max = w*L⁴/(8*E*I)  (at free end)
```

### 6. Fixed-Fixed Beam - Point Load at Center
```
Configuration:  ■ ----P---- ■
                0    L/2    L

Reactions:
  R_A = P/2
  R_B = P/2
  M_A = P*L/8
  M_B = P*L/8

Max Moment:
  M_max = P*L/8  (at ends)

Max Deflection:
  δ_max = P*L³/(192*E*I)  (at center)
```

### 7. Propped Cantilever - Point Load at Free End
```
Configuration:  ■ ----P
                0      L

Reaction at Fixed End:
  R_A = 3*P/2
  M_A = P*L/2

Reaction at Prop:
  R_B = P/2

Max Deflection:
  δ_max = P*L³/(24*E*I)
```

## Common Material Properties (E - Young's Modulus)

| Material | E (GPa) | E (Pa) | Typical Use |
|----------|---------|--------|-------------|
| Steel | 210 | 2.1×10¹¹ | Buildings, bridges |
| Aluminum | 69 | 6.9×10¹⁰ | Lightweight structures |
| Concrete | 30-40 | 3-4×10¹⁰ | Reinforced concrete beams |
| Wood (pine) | 10-13 | 1-1.3×10¹⁰ | Timber structures |
| Timber (avg) | 11 | 1.1×10¹⁰ | Residential construction |
| Composite (FRP) | 40-60 | 4-6×10¹⁰ | Advanced applications |
| Cast Iron | 140 | 1.4×10¹¹ | Historic structures |
| Plastics | 2-4 | 2-4×10⁹ | Non-structural |

## Moment of Inertia (I) - Common Sections

### Rectangular Section
```
    b (width)
  +----------+
  |          | h (height)
  |          |
  +----------+

I = b*h³/12

Example: 200mm × 400mm steel beam
I = 0.2 × 0.4³ / 12 = 1.067×10⁻³ m⁴
```

### Circular Section
```
      d (diameter)
     +---+
     |   |
     +---+

I = π*d⁴/64

Example: 300mm diameter shaft
I = π × 0.3⁴ / 64 = 3.976×10⁻⁴ m⁴
```

### Hollow Circular Section (Pipe)
```
    d_o (outer)
    d_i (inner)

I = π*(d_o⁴ - d_i⁴)/64

Example: 200mm outer, 180mm inner
I = π × (0.2⁴ - 0.18⁴) / 64 = 7.32×10⁻⁵ m⁴
```

### I-Beam (Approximate)
```
  +-----+
  |     | t_f (flange thickness)
+-+-----+-+
| |     | | t_w (web thickness)
| |     | |
+-+-----+-+
  |     |
  +-----+
    b (flange width)
      h (height)

For standard steel I-beams, consult tables.
Common: IPE-200: I ≈ 1.94×10⁻⁵ m⁴
```

## Deflection Allowance Criteria

| Structure Type | Allowable Deflection |
|---|---|
| Floor beams | L/250 to L/360 |
| Roof beams | L/180 to L/250 |
| Cantilever | L/180 (tip) |
| Pedestrian bridge | L/250 |
| Long-span bridge | L/500 to L/1000 |
| Precision machinery support | L/1000 |

## Stress Calculation

**Maximum Bending Stress:**
```
σ = M*c/I

Where:
  M = Bending moment
  c = Distance from neutral axis to extreme fiber
  I = Moment of inertia
  
For rectangular: c = h/2
For circular: c = d/2
```

**Shear Stress:**
```
τ = V*Q/(I*b)

Where:
  V = Shear force
  Q = First moment of area
  I = Moment of inertia
  b = Width at section
```

## Superposition Principle

For linear elastic systems, multiple loads can be analyzed separately and results added:

```
Total deflection = δ₁ + δ₂ + δ₃ + ...
Total moment = M₁ + M₂ + M₃ + ...
Total shear = V₁ + V₂ + V₃ + ...
```

**Example:**
Simply supported beam with both point load P and uniform load w:
```
δ_total = P*a²*b²/(3*E*I*L) + 5*w*L⁴/(384*E*I)
```

## Using Python Script Parameters

### Unit Conversion Factors
```
1 inch = 0.0254 m
1 foot = 0.3048 m
1 kip = 4448.22 N
1 ksi = 6.89476 MPa = 6.89476×10⁶ Pa
1 in⁴ = 4.162×10⁻⁸ m⁴
```

### Common Moment of Inertia Values (Steel I-Beams)
```
UPN/C-Channel 100: I ≈ 2.06×10⁻⁵ m⁴
IPE 200: I ≈ 1.94×10⁻⁵ m⁴
HEA 200: I ≈ 6.92×10⁻⁵ m⁴
HEB 200: I ≈ 1.04×10⁻⁴ m⁴
W12×26 (US): I ≈ 2.45×10⁻⁴ m⁴
```

## Quick Calculation Tips

1. **Double the load → 2× stress and deflection**
2. **Double the span → 8× moment, 16× deflection** (L² and L⁴ dependency)
3. **Double the section height → 8× moment capacity** (I ∝ h³)
4. **Change material E value → inverse proportional to deflection**

## Example Calculation Workflow

```
1. Identify beam type and loads
2. Calculate reactions (equilibrium)
3. Draw/calculate shear force diagram
4. Draw/calculate bending moment diagram
5. Find maximum moment location
6. Estimate required section (try different I values)
7. Calculate maximum deflection
8. Check against allowable deflection criteria
9. Verify maximum stress ≤ allowable stress
10. Finalize design with safety factors
```

---

See `BEAM_PLOTTING_GUIDE.md` for script usage and customization.
See `plot_beam_analysis.py` for implementation details and source code.
