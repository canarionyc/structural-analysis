import FreeCAD as App
import Part

# --- 3D VISUALIZATION: FINAL 8-BOLT CONNECTION ---
print("Generando modelo 3D en FreeCAD...")

# 1. Create a new document
doc = App.newDocument("Final_8_Bolt_Connection")

# 2. NEW DIMENSIONS
# Extended to 500mm to safely fit 8 bolts in a single row
length = 500

# 3. GUSSET PLATE (14mm thick)
plate = Part.makeBox(length, 14, 120)
plate.translate(App.Vector(0, -7, -60))
Part.show(plate, "Gusset_Plate_14mm")

# 4. UPN 100 PROFILES
upn_outer = Part.makeBox(length, 50, 100)
upn_inner = Part.makeBox(length, 50 - 6, 100 - 2 * 8.5)
upn_inner.translate(App.Vector(0, 6, 8.5))

# Right UPN
upn_right = upn_outer.cut(upn_inner)
upn_right.translate(App.Vector(0, 7, -50))
Part.show(upn_right, "UPN_100_Right")

# Left UPN
upn_left = upn_outer.cut(upn_inner)
upn_left.rotate(App.Vector(0, 0, 0), App.Vector(1, 0, 0), 180)
upn_left.translate(App.Vector(0, -7, 50))
Part.show(upn_left, "UPN_100_Left")

# 5. PLACING 8 BOLTS IN A ROW
# Starting 40mm from the edge, spaced by 60mm each
bolt_spacing = 60
start_x = 40

for i in range(8):
    x_pos = start_x + (i * bolt_spacing)
    # Make cylinder: 10mm radius (20mm dia), 130mm long
    bolt = Part.makeCylinder(10, 130)
    # Rotate horizontally through the webs
    bolt.rotate(App.Vector(0, 0, 0), App.Vector(1, 0, 0), -90)
    # Center the bolt
    bolt.translate(App.Vector(x_pos, -65, 0))
    Part.show(bolt, f"Bolt_M20_{i + 1}")

# 6. RECOMPUTE AND VIEW
doc.recompute()
if App.GuiUp:
    App.Gui.SendMsgToActiveView("ViewFit")
    App.Gui.activeDocument().activeView().viewAxometric()

print("Modelo 3D generado con éxito con 8 tornillos.")

# 7. EXPORT GUSSET PLATE TO STEP AND STL
import os
import Mesh
import Import

output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "CAD_output")
os.makedirs(output_dir, exist_ok=True)

plate_obj = doc.getObject("Gusset_Plate_14mm")

step_path = os.path.join(output_dir, "Gusset_Plate_14mm.step")
stl_path  = os.path.join(output_dir, "Gusset_Plate_14mm.stl")

Import.export([plate_obj], step_path)
Mesh.export([plate_obj], stl_path)

print(f"STEP saved: {step_path}")
print(f"STL  saved: {stl_path}")