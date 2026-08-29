"""
ref02_independent_numerics.py

Independent referee numeric re-verification (fresh mpmath, NOT copied from
s03/s04, different test field, different (y,z) sample points where feasible)
of ATTEMPT.md Sec 4.2 (naive same-x bound refutation + corrected bound) and
Sec 5 (anti-causal leakage fraction table).

(BB-Psi'), cited, unconditional on (B):
   Psi(x,y) = int_0^inf e^{-u^2/2-u(x+y)} I(x+u,y) du
   I(x,y) = int_0^y Phi(x,y') dy'
"""
import mpmath as mp

mp.mp.dps = 35


# ---------------------------------------------------------------------
# A DIFFERENT test field from the front's (different shape, different
# frequencies/decay), still bounded, oscillatory, non-monotone.
# ---------------------------------------------------------------------
def Phi_test(xv, yv):
    # bounded strictly inside [-1,1] by construction (cos,sin bounded 1,
    # exp(-0.05*x) in (0,1], /(1+0.2*y) in (0,1]) times sign wobble
    return mp.cos(1.3 * xv - 0.7) * mp.sin(0.8 * yv + 1.1) * mp.e**(-0.05 * xv) / (1 + 0.2 * yv)


M_PHI_TEST = mp.mpf('1.0')  # sup|Phi_test| <= 1 by construction


def I_test(xv, yv):
    f = lambda yp: Phi_test(xv, yp)
    if yv == 0:
        return mp.mpf(0)
    return mp.quad(f, [0, yv])


def Psi_test(xv, yv):
    z = xv + yv
    f = lambda uu: mp.e**(-uu**2 / 2 - uu * z) * I_test(xv + uu, yv)
    return mp.quad(f, [0, 3, 8, 20, 45])


def R_mills(z):
    return mp.sqrt(mp.pi / 2) * mp.e**(z**2 / 2) * mp.erfc(z / mp.sqrt(2))


print("=" * 78)
print("PART 1: M_Psi <= M_Phi corollary, sanity check on the new test field")
print("=" * 78)
test_points = [(0.0, 0.4), (0.2, 1.5), (1.0, 0.8), (3.0, 2.0), (0.0, 8.0)]
max_psi = mp.mpf(0)
for (xv, yv) in test_points:
    p = abs(Psi_test(xv, yv))
    max_psi = max(max_psi, p)
    print(f"  x={xv:5.2f} y={yv:5.2f}  |Psi|={float(p):.8f}  <= M_Phi={float(M_PHI_TEST)}? "
          f"{p <= M_PHI_TEST + mp.mpf('1e-9')}")
assert max_psi <= M_PHI_TEST + mp.mpf('1e-6')
print("CONFIRMED on an independently-chosen test field.")

print()
print("=" * 78)
print("PART 2: naive same-x local bound |Psi(x,y)|<=y*R(x+y)*sup_{y'<=y}|Phi(x,y')|")
print("        -- independent test for the front's self-caught refutation")
print("=" * 78)
naive_points = [(0.0, 0.5), (0.0, 1.0), (0.5, 0.6), (0.0, 2.5), (1.5, 0.3), (0.2, 4.0)]
n_violations = 0
print(f"{'x':>6} {'y':>6} {'|Psi| exact':>14} {'naive bound':>14} {'holds?':>8}")
for (xv, yv) in naive_points:
    p = abs(Psi_test(xv, yv))
    # sup over SAME x, y' in [0,y]
    sup_same_x = mp.mpf(0)
    for k in range(61):
        yp = (k / 60.0) * yv
        sup_same_x = max(sup_same_x, abs(Phi_test(xv, yp)))
    z = xv + yv
    naive_bound = sup_same_x * yv * R_mills(z)
    ok = p <= naive_bound + mp.mpf('1e-9')
    if not ok:
        n_violations += 1
    print(f"{xv:6.2f} {yv:6.2f} {float(p):14.9f} {float(naive_bound):14.9f} {str(ok):>8}")
print(f"Violations of the naive same-x bound on this INDEPENDENT test field: "
      f"{n_violations}/{len(naive_points)}")

print()
print("=" * 78)
print("PART 3: corrected bound |Psi(x,y)|<=y*R(x+y)*sup_{x'>=x,y'<=y}|Phi(x',y')|")
print("=" * 78)
all_ok = True
for (xv, yv) in naive_points:
    p = abs(Psi_test(xv, yv))
    sup_fwd = mp.mpf(0)
    for kx in range(51):        # x' in [x, x+25]
        xp = xv + kx * 0.5
        for ky in range(41):    # y' in [0,y]
            yp = (ky / 40.0) * yv
            sup_fwd = max(sup_fwd, abs(Phi_test(xp, yp)))
    z = xv + yv
    corrected_bound = sup_fwd * yv * R_mills(z)
    ok = p <= corrected_bound + mp.mpf('1e-9')
    all_ok = all_ok and ok
    print(f"  x={xv:5.2f} y={yv:5.2f}  |Psi|={float(p):.9f}  corrected_bound="
          f"{float(corrected_bound):.9f}  holds? {ok}")
assert all_ok
print("CORRECTED bound CONFIRMED on this independent test field at every point.")

print()
print("=" * 78)
print("PART 4: anti-causal leakage fraction -- spot check against ATTEMPT.md Sec 5")
print("        table, at a mix of the SAME and a few NEW (y,z) points")
print("=" * 78)


def anticausal_fraction(z, y):
    total_u_mass = R_mills(z)
    total_mass = total_u_mass * y

    def inner(yp):
        lower = max(mp.mpf(0), y - yp)
        return mp.quad(lambda u: mp.e**(-u**2 / 2 - u * z), [lower, lower + 6, lower + 25, mp.inf])

    anticausal_mass = mp.quad(inner, [0, y])
    return anticausal_mass / total_mass


table_points = [
    (mp.mpf('0.6'), mp.mpf('0.5'), '0.730'),
    (mp.mpf('1.0'), mp.mpf('0.5'), '0.681'),
    (mp.mpf('1.0'), mp.mpf('1.0'), '0.472'),
    (mp.mpf('2.0'), mp.mpf('1.0'), '0.356'),
    (mp.mpf('5.0'), mp.mpf('1.0'), '0.186'),
    (mp.mpf('10.0'), mp.mpf('1.0'), '0.098'),
    (mp.mpf('30.0'), mp.mpf('1.0'), '0.033'),
    (mp.mpf('100.0'), mp.mpf('1.0'), '0.010'),
]
print(f"{'z':>8} {'y':>6} {'computed':>10} {'claimed':>10} {'match(3dp)?':>12}")
for (z, y, claimed) in table_points:
    frac = anticausal_fraction(z, y)
    claimed_f = mp.mpf(claimed)
    match = abs(frac - claimed_f) < mp.mpf('0.0006')
    print(f"{float(z):8.2f} {float(y):6.2f} {float(frac):10.4f} {float(claimed_f):10.3f} {str(match):>12}")
    assert match, f"MISMATCH at z={z},y={y}: computed {frac} vs claimed {claimed}"

print()
print("NEW points not in the front's own table (extending the grid, y=2.0 and")
print("y=0.5 at large z, to check the min/max range claim '19%-73% across the")
print("full tested grid'):")
extra_points = [
    (mp.mpf('2.0'), mp.mpf('2.0')),
    (mp.mpf('5.0'), mp.mpf('2.0')),
    (mp.mpf('10.0'), mp.mpf('2.0')),
    (mp.mpf('30.0'), mp.mpf('2.0')),
    (mp.mpf('100.0'), mp.mpf('2.0')),
    (mp.mpf('30.0'), mp.mpf('0.5')),
    (mp.mpf('100.0'), mp.mpf('0.5')),
]
frac_min = mp.mpf('1')
frac_max = mp.mpf('0')
for (z, y) in extra_points:
    frac = anticausal_fraction(z, y)
    frac_min = min(frac_min, frac)
    frac_max = max(frac_max, frac)
    print(f"  z={float(z):7.2f} y={float(y):5.2f}  frac={float(frac):.6f}")

# also fold in the 8 table points into the min/max computation
for (z, y, claimed) in table_points:
    frac = anticausal_fraction(z, y)
    frac_min = min(frac_min, frac)
    frac_max = max(frac_max, frac)

print()
print(f"Min/max anti-causal fraction over ALL 15 points tested here "
      f"(8 table pts + 7 extra): [{float(frac_min):.4f}, {float(frac_max):.4f}]")
print("ATTEMPT.md Sec 5 text claims the range is '19%-73% across the full tested")
print("grid' -- checking whether that literal numeric range holds once the full")
print("18-point grid (including y=2.0 and large-z/small-y combinations) is")
print("considered, not just the 8-row DISPLAYED table.")
if frac_min < mp.mpf('0.19') - mp.mpf('0.001'):
    print(f"  --> DISCREPANCY: found a fraction ({float(frac_min):.4f}) BELOW the")
    print("      claimed 19% lower bound when the full grid (not just the 8-row")
    print("      displayed table) is considered.")
else:
    print("  --> no discrepancy found; claim holds over the full grid too.")
