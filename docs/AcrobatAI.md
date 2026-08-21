Let me see how the geometric properties affect beam performance.

Using the HEB wide flange beam tables, we can summarize the key geometric properties needed for sizing under bending, shear, deflection, and stability checks. Values are taken directly from the document; units as listed.
Design-ready properties (selected sizes)
Section h [mm] b [mm] tw [mm] tf [mm] A [cm2] Iy [cm4] Iz [cm4] Wy [cm3] Wz [cm3] G [kg/m] HEB 100 100.0 100.0 6.0 10.0 26.00 450.00 167.00 89.90 33.50 20.4 HEB 200 200.0 200.0 9.0 15.0 78.10 5700.00 2000.00 570.00 200.00 61.3 HEB 300 300.0 300.0 11.0 19.0 149.00 25170.00 8560.00 1680.00 571.00 117.0 HEB 400 400.0 300.0 13.5 24.0 198.00 57680.00 10820.00 2880.00 721.00 155.4 HEB 500 500.0 300.0 14.5 28.0 239.00 107200.00 12620.00 4290.00 842.00 187.6 
Additional radii of gyration (for buckling/slenderness):
HEB 100: iy = 41.6 mm, iz = 25.3 mmHEB 200: iy = 85.4 mm, iz = 50.7 mmHEB 300: iy = 130.0 mm, iz = 75.8 mmHEB 400: iy = 171.0 mm, iz = 74.0 mmHEB 500: iy = 212.0 mm, iz = 72.7 mm
How to use these in design
Bending resistance (about major y-axis): MRd = Wy × fy / γM. Use Wy in cm3 (convert to m3 if using SI base), fy and γM per code.Shear resistance: use Ay or Az (from shear table) with VRd = Av × fy / (√3 × γM) per code axis.Deflection: use EI with Iy (major) or Iz (minor). δ under typical loading from standard beam formulas.Lateral-torsional buckling and torsion: use Wz, It, Iω, and warping constants provided in the tables when required by the code method.
For other HEB sizes (100–1000), the document provides the full set of geometry, bending, shear, torsion, warping, and plasticity properties to plug directly into code checks. This enables rapid selection by comparing required section modulus and inertia against factored demands.