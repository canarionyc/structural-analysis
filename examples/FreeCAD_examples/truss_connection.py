#%% setup

import FreeCAD as App
import Part

#%% 1. Create a new 3D document
doc = App.newDocument("UPN_Connection")

# 2. CREATE THE GUSSET PLATE (La Cartela)
# 14mm thick (Y), 200mm long (X), 120mm high (Z)
plate = Part.makeBox(200, 14, 120)
# Center it exactly on the Y-axis so it goes from -7mm to +7mm
plate.translate(App.Vector(0, -7, -60))
Part.show(plate, "Gusset_Plate_14mm")

#%% 3. CREATE THE UPN 100 (Right Side)
# We make a simplified C-Channel by subtracting a smaller box from a bigger one
# UPN 100 Dimensions: 100mm high, 50mm wide, 6mm web, 8.5mm flanges
upn_outer = Part.makeBox(200, 50, 100)
upn_inner = Part.makeBox(200, 50 - 6, 100 - 2*8.5)
upn_inner.translate(App.Vector(0, 6, 8.5)) # Shift to leave 6mm web and 8.5mm flange
upn_right = upn_outer.cut(upn_inner)

# Move it to the right side of the plate (starts at Y = +7mm)
upn_right.translate(App.Vector(0, 7, -50))
Part.show(upn_right, "UPN_100_Right")

#%% 4. CREATE THE UPN 100 (Left Side)
upn_left = upn_outer.cut(upn_inner)
# Rotate it 180 degrees so it faces the opposite way (back-to-back)
upn_left.rotate(App.Vector(0,0,0), App.Vector(1,0,0), 180)
# Move it to the left side of the plate (starts at Y = -7mm)
upn_left.translate(App.Vector(0, -7, 50))
Part.show(upn_left, "UPN_100_Left")

#%% 5. CREATE THE M20 BOLTS (Tornillos de 20mm)
# Let's place 3 bolts through the web to see how they fit
bolt_X_positions = [50, 100, 150] # Spread them along the beam
bolt_count = 1

for x in bolt_X_positions:
    # Make a cylinder: 10mm radius (20mm diameter), 130mm long
    bolt = Part.makeCylinder(10, 130)
    # Rotate it to point horizontally through the webs
    bolt.rotate(App.Vector(0,0,0), App.Vector(1,0,0), -90)
    # Center the bolt so it sticks out of both sides evenly
    bolt.translate(App.Vector(x, -65, 0))
    Part.show(bolt, f"Bolt_M20_{bolt_count}")
    bolt_count += 1

#%% 6. Refresh the view to show everything
doc.recompute()
App.Gui.SendMsgToActiveView("ViewFit")
App.Gui.activeDocument().activeView().viewAxometric()

#%% Add 3D Dimensions (Drafting)
import Draft
# Measure the 14mm thickness of the gusset plate at the top
p1 = App.Vector(0, -7, 60) # Back face of the plate
p2 = App.Vector(0, 7, 60)  # Front face of the plate
p3 = App.Vector(0, 0, 80)  # Where to place the text floating above

dim1 = Draft.make_dimension(p1, p2, p3)
dim1.ViewObject.FontSize = 5 # Make the text readable
dim1.ViewObject.LineColor = (1.0, 0.0, 0.0) # Red color

App.ActiveDocument.recompute()

#%% 2. Generate 2D Blueprints (TechDraw)

#%% Finite Element Analysis (FEM)

#%%
# Recompute the mathematical model
App.ActiveDocument.recompute()

# Send it to the graphical interface and fit the view
if App.GuiUp:
    App.Gui.ActiveDocument.ActiveView.viewAxometric()
    App.Gui.SendMsgToActiveView("ViewFit")