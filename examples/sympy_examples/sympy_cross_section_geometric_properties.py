#%% setup
import sympy as sp

# region Rectangular Cross-Sectional Properties
#%% 1. Define symbolic variables
x, y = sp.symbols('x y')
b, h = sp.symbols('b h', positive=True)

# We place the origin (0,0) at the centroid of the rectangle.
# The limits of integration are from -b/2 to b/2 for x, and -h/2 to h/2 for y.
x_limits = (x, -b/2, b/2)
y_limits = (y, -h/2, h/2)

#%% 2. Calculate Area
# A = ∫∫ 1 dx dy
Area = sp.integrate(1, y_limits, x_limits)
print(f"Area: {Area}")  # Outputs: b*h

#%% 3. Calculate Moments of Inertia (Strong and Weak axes)
# Iy (about the horizontal z-axis in standard structural notation, or x-axis here) = ∫∫ y^2 dx dy
Iy = sp.integrate(y**2, y_limits, x_limits)
print(f"Moment of Inertia (Iy): {Iy}")  # Outputs: b*h**3/12

# Iz (about the vertical y-axis) = ∫∫ x^2 dx dy
Iz = sp.integrate(x**2, y_limits, x_limits)
print(f"Moment of Inertia (Iz): {Iz}")  # Outputs: b**3*h/12

#%% 4. Calculate Radii of Gyration
# i = sqrt(I / A)
iy = sp.sqrt(Iy / Area)
iz = sp.sqrt(Iz / Area)

print(f"Radius of Gyration (iy): {iy}") # Outputs: sqrt(3)*h/6
print(f"Radius of Gyration (iz): {iz}") # Outputs: sqrt(3)*b/6

# endregion

# region Tube Cross-Sectional Properties
#%% 5. Define symbolic variables
from sympy import Ray, Circle, intersection
c = Circle((0, 1), 1)
intersection(c, c.center)
# []
right = Ray((0, 0), (1, 0))
up = Ray((0, 0), (0, 1))
intersection(c, right, up)
# [Point2D(0, 0)]
intersection(c, right, up, pairwise=True)
# [Point2D(0, 0), Point2D(0, 2)]
left = Ray((1, 0), (0, 0))
intersection(right, left)
# [Segment2D(Point2D(0, 0), Point2D(1, 0))]


r, h = sp.symbols('r h', positive=True)


#endregion

# region Cylinder Cross-Sectional Properties



# endregion