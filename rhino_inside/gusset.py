# -*- coding: utf-8 -*-

import rhinoscriptsyntax as rs

# 1. CREATE THE GUSSET PLATE (La Cartela)
# Rhino usually defines a box by its 8 corner points.
# We want a 500 x 14 x 120 mm plate centered on the Y axis.
pt0 = [0, -7, -60]
pt1 = [500, -7, -60]
pt2 = [500, 7, -60]
pt3 = [0, 7, -60]
pt4 = [0, -7, 60]
pt5 = [500, -7, 60]
pt6 = [500, 7, 60]
pt7 = [0, 7, 60]

# Generate the solid box in the Rhino viewport
plate = rs.AddBox([pt0, pt1, pt2, pt3, pt4, pt5, pt6, pt7])

# 2. CREATE A CYLINDER FOR THE BOLT HOLE
# A 22mm hole (11mm radius) going through the plate
hole_start = [40, -20, 0]
hole_end = [40, 20, 0]
hole = rs.AddCylinder(hole_start, hole_end, 11)

# 3. BOOLEAN DIFFERENCE (Subtract the hole from the plate)
# Rhino handles boolean operations incredibly cleanly
final_plate = rs.BooleanDifference(plate, hole, delete_input=True)

print("¡Cartela generada en Rhino con éxito!")