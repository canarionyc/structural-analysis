
# Deflection of a Beam with Distributed and Point Load
# Introduction
# This application will derive an explicit expression for the deflection of a beam with a distributed load and a point load.
# 
# Governing Equations
restart;
# 
# The Euler-Bernoulli equation
de := EI*diff(w(x), x, x, x, x) = q(x);
# 
# Initial and boundary conditions
ibc := w(0) = 0, w(L) = 0, (D@@2)(w)(0) = 0, (D@@2)(w)(L) = 0;
# 
# Distributed load and point load
q := x -> F*Dirac(x - b);
# Solution of the Differential Equation
# Solve the differential equation together with the initial/boundary conditions and the load distribution to get an explicit expression for the beam deflection.
deSol := dsolve({de, ibc}, w(x));
deflection := simplify(rhs(deSol), symbolic);
# 
# Derive the moment and shear distribution.
moment := EI*diff(deflection, x, x);
# 
shear := diff(moment, x);
# Plot the Deflection, Moment, and Shear 
# Assign parameters.
Q := -12;
F := -10;
L := 20;
a := 3;
b := 5;
EI := 10000;
# 
# Plot deflection, moment, and shear.
plot(deflection, x = 0 .. L, size = [1000, 400], axesfont = [Calibri], title = "Deflection", labels = ["Distance along beam", "Deflection"], labeldirections = [horizontal, vertical], labelfont = [Calibri], titlefont = [Calibri, 16, bold], background = ColorTools:-Color("RGB", [218/255, 223/255, 225/255]), axis = [gridlines = [color = ColorTools:-Color("RGB", [1, 1, 1])]]);
# 
plot(moment, x = 0 .. L, size = [1000, 400], axesfont = [Calibri], title = "Moment", labels = ["Distance along beam", "Moment"], labeldirections = [horizontal, vertical], labelfont = [Calibri], titlefont = [Calibri, 16, bold], background = ColorTools:-Color("RGB", [218/255, 223/255, 225/255]), axis = [gridlines = [color = ColorTools:-Color("RGB", [1, 1, 1])]]);
# Shear Distribution
plot(shear, x = 0 .. L, size = [1000, 400], axesfont = [Calibri], title = "Shear", labels = ["Distance along beam", "Shear"], labeldirections = [horizontal, vertical], labelfont = [Calibri], titlefont = [Calibri, 16, bold], background = ColorTools:-Color("RGB", [218/255, 223/255, 225/255]), axis = [gridlines = [color = ColorTools:-Color("RGB", [1, 1, 1])]]);

