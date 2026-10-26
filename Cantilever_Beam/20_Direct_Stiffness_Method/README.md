
### Created Files
* [cantilever_dsm_scipy.py](file:///C:/dev/structural-analysis/Cantilever_Beam/20_Direct_Stiffness_Method/cantilever_dsm_scipy.py) & paired Jupytext notebook [cantilever_dsm_scipy.ipynb](file:///C:/dev/structural-analysis/Cantilever_Beam/20_Direct_Stiffness_Method/cantilever_dsm_scipy.ipynb)
* [cantilever_dsm_results.svg](file:///C:/dev/structural-analysis/Cantilever_Beam/20_Direct_Stiffness_Method/cantilever_dsm_results.svg) (Shear, Bending Moment, and Hermite Deflection diagrams exported in SVG format)

### What It Covers
1. **Cross-Section Analysis (`sectionproperties`)**:
   * Meshes an S355 steel I-section ($d = 300\text{ mm}, b = 150\text{ mm}, t_f = 12\text{ mm}, t_w = 8\text{ mm}, r = 10\text{ mm}$) and computes exact axial, flexural, shear, and torsional rigidities ($EA, EI_{xx}, EA_{sy}, EJ, Z_{xx}$).
2. **Direct Stiffness Assembly & `scipy` Solvers**:
   * [`frame2d_local_stiffness`](file:///C:/dev/structural-analysis/Cantilever_Beam/20_Direct_Stiffness_Method/cantilever_dsm_scipy.py#L94-L120): Builds the $6 \times 6$ local 2D frame stiffness matrix supporting both pure **Euler–Bernoulli** ($\Phi = 0$) and **Timoshenko** shear-deformable ($\Phi = \frac{12 EI_{xx}}{GA_{sy}L_e^2}$) formulations using the shear area $A_{sy}$ from `sectionproperties`.
   * [`frame2d_consistent_udl`](file:///C:/dev/structural-analysis/Cantilever_Beam/20_Direct_Stiffness_Method/cantilever_dsm_scipy.py#L123-L132): Assembles work-equivalent nodal loads $\left[0, \frac{qL_e}{2}, \frac{qL_e^2}{12}, 0, \frac{qL_e}{2}, -\frac{qL_e^2}{12}\right]^T$.
   * [`solve_cantilever_dsm`](file:///C:/dev/structural-analysis/Cantilever_Beam/20_Direct_Stiffness_Method/cantilever_dsm_scipy.py#L136-L185): Assembles the global sparse matrix (`scipy.sparse.csc_matrix`), partitions free and fixed DOFs, and solves $\mathbf{K}_{ff}\mathbf{u}_f = \mathbf{F}_f$ using both sparse SuperLU (`scipy.sparse.linalg.spsolve`) and symmetric positive-definite Cholesky factorization (`scipy.linalg.cho_factor` / `cho_solve`).
3. **Analytical Verification & Stress Recovery**:
   * Asserts machine-precision agreement (`rel_tol=1e-12`) against closed-form Euler–Bernoulli and Timoshenko equations for support reactions ($R_y = 45\text{ kN}, M_z = 175\text{ kN}\cdot\text{m}$), tip deflection ($-74.9490\text{ mm}$ Euler–Bernoulli vs. $-75.9394\text{ mm}$ Timoshenko), and tip rotation ($-21.9082\text{ mrad}$).
   * Passes the fixed-end internal forces back into `sec.calculate_stress(mxx=M_root, vy=V_root)` to evaluate root cross-section stress ($290.57\text{ MPa}$, $81.9\%$ of S355 yield).