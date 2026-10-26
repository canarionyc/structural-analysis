# Stepped-Euler-Bernoulli-Beam
Inhomogeneous bending stiffness in Euler-Bernoulli beam modelled with singularity functions.

The live script `examples.mlx` contains examples for the functions `oneFieldBeam.mlx` and `twoFieldBeam.mlx`.

The live function `oneFieldBeam.mlx` calculates the displacement, rotation, curvature and bending moment for a single-span beam with changing bending stiffness. You can choose between pinned and fixed ends.

The live function `twoFieldBeam.mlx` calculates the displacement, rotation, curvature and bending moment for a two-span beam (continuous beam) with changing bending stiffness. You can choose between pinned and fixed ends.

The live functions uses singularity functions to implement the changing bending stiffness in the beam.
Also the load and support forces are modelled with singularity functions.
See reference for detailed explanation.


# Reference
Static, Vibration Analysis and Sensitivity Analysis of Stepped Beams Using Singularity Functions by Peng Cheng, Carla Davila and Gene Hou.


# Acknowledgement
This work is part of the ZEBBRA project, which is funded by the Federal Ministry of Education and Research.
