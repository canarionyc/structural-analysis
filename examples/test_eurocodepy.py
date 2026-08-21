"""A compact showcase of eurocodepy capabilities across Eurocode 1, 2, 3 and 5.

Run this file directly to see representative examples for:
- load combination generation (EC1)
- concrete material and reinforcement handling (EC2)
- steel section resistance checks (EC3)
- timber material properties (EC5)
"""

from eurocodepy.ec1 import Load, LoadType, Loads
from eurocodepy.ec2 import Bar, BarLayout, C30_37
from eurocodepy.ec3 import SectionForces, SectionResistanceInput, Steel, eurocode3_section_check
from eurocodepy.ec5 import Timber


def showcase_ec1() -> None:
    """Generate a simple EC1 ULS load combination."""
    loads = Loads()
    loads.add(Load("Gk", LoadType.PERMANENT, gamma_fav=0.9, gamma_unf=1.35, psi0=0.0, psi1=0.0, psi2=0.0))
    loads.add(Load("Qk", LoadType.LIVE, gamma_fav=0.0, gamma_unf=1.5, psi0=0.7, psi1=0.5, psi2=0.3))

    combos = loads.get_ULS_combos()
    print("EC1 — load combinations")
    for name, combo in combos.items():
        print(f"  {name}: {combo.factors}")
    print()


def showcase_ec2() -> None:
    """Show concrete and reinforcement properties."""
    concrete = C30_37
    bars = [Bar(20, 2), Bar(16, 3)]
    layout = BarLayout(bars)

    print("EC2 — concrete and reinforcement")
    print(f"  Concrete: {concrete.grade} | fck = {concrete.fck} MPa | Ecm = {concrete.Ecm} MPa")
    print(f"  Rebar layout: {[(bar.diameter, bar.number) for bar in layout.bars]}")
    print(f"  Total reinforcement area: {layout.total_area:.1f} mm^2")
    print()


def showcase_ec3() -> None:
    """Run a basic EC3 cross-section check."""
    steel = Steel("S355")
    section = SectionResistanceInput(
        kind="I",
        section_class=1,
        fy=steel.fyk,
        gamma_M0=steel.gamma_M0,
        area=12000.0,
        b=200.0,
        h=400.0,
        tw=8.0,
        tf=15.0,
        hw=370.0,
        eps=0.81,
        wpl_y=1.2e6,
        wpl_z=0.35e6,
        wel_y=1.05e6,
        wel_z=0.31e6,
        wt=0.18e6,
        av_y=2400.0,
        av_z=1800.0,
    )
    forces = SectionForces(n_ed=500.0, my_ed=160.0, mz_ed=25.0, vy_ed=120.0, vz_ed=60.0, t_ed=5.0)
    result = eurocode3_section_check(section, forces)

    print("EC3 — steel section check")
    print(f"  Steel: {steel.ClassType} | fy = {steel.fyk} MPa")
    print(f"  Section check: utilisation = {result.utilization:.3f} | {'PASS' if result.passed else 'FAIL'}")
    summary = str(result).encode("ascii", "replace").decode("ascii")
    print("  " + summary.replace("\n", "\n  "))
    print()


def showcase_ec5() -> None:
    """Inspect a timber material class from EC5."""
    timber = Timber("C24")
    print("EC5 — timber material")
    print(f"  Timber grade: {timber.type_label} | E0,mean = {timber.E0mean} MPa | fmk = {timber.fmk} MPa")
    print(f"  Characteristic values: fc0k={timber.fc0k} MPa, ft0k={timber.ft0k} MPa, fvk={timber.fvk} MPa")
    print()


if __name__ == "__main__":
    showcase_ec1()
    showcase_ec2()
    showcase_ec3()
    showcase_ec5()
