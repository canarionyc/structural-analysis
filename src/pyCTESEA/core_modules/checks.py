# %% ADVANCED VERIFICATION CLASS
import math
from ..core_modules.constants import BUCKLING_CURVES
from ..core_modules.steel_bar import SteelBar
from ..core_modules.buckling_result import BucklingResult

class DBSEACheck:
    @staticmethod
    def calculate_chi(bar: SteelBar, axis='y'):
        """
        Calculates the buckling reduction factor Chi (χ) per DB SE-A 6.3.2.1.
        Uses explicit naming to prevent confusion between Inertia and Radius of Gyration.
        """
        # 1. Get the buckling curve key and imperfection factor (alpha)
        # Table 6.3 / Table 6.2
        curve_key = bar.section.buckling_curves[axis]
        alpha_imperfection = BUCKLING_CURVES[curve_key]

        # 2. Get the Radius of Gyration (radio de giro) for the specific axis
        # Renamed to avoid 'i' vs 'I' confusion
        if axis == 'y':
            radius_gyration = bar.section.radius_gyration_y
        else:
            radius_gyration = bar.section.radius_gyration_z

        # 3. Get effective length (longitud de pandeo L_cr)
        l_effective = bar.get_effective_length(axis)

        # 4. Mechanical Slenderness (λ = L_cr / i)
        mechanical_slenderness = l_effective / radius_gyration

        # 5. Reference Slenderness (λ1 = π * sqrt(E / fy))
        # Part of the relative slenderness calculation
        slenderness_ref = math.pi * math.sqrt(bar.material.E / bar.material.fy)

        # 6. Relative slenderness (λ_bar = λ / λ1)
        relative_slenderness = mechanical_slenderness / slenderness_ref

        # Buckling doesn't occur for relative_slenderness <= 0.2
        if relative_slenderness <= 0.2:
            return 1.0

        # 7. Calculation of Phi and Reduction Factor Chi (χ)
        # Based on Eq. 6.32
        phi = 0.5 * (1 + alpha_imperfection * (relative_slenderness - 0.2) + relative_slenderness ** 2)

        chi = 1 / (phi + math.sqrt(phi ** 2 - relative_slenderness ** 2))
        return min(chi, 1.0)

    @staticmethod
    def check_buckling(bar: SteelBar, Nd: float, axis='y'):
        """
        Full buckling resistance check (N_b,Rd) per DB SE-A Eq. 6.32.
        """
        reduction_factor_chi = DBSEACheck.calculate_chi(bar, axis)

        # N_b,Rd = (chi * Area * fy) / gamma_M1
        design_resistance_nb_rd = (reduction_factor_chi * bar.section.area * bar.material.fy) / bar.gamma_M1

        utilization_ratio = abs(Nd) / design_resistance_nb_rd

        return BucklingResult(
            ratio=utilization_ratio,
            capacity_N=design_resistance_nb_rd,
            chi=reduction_factor_chi,
            axis=axis
        )