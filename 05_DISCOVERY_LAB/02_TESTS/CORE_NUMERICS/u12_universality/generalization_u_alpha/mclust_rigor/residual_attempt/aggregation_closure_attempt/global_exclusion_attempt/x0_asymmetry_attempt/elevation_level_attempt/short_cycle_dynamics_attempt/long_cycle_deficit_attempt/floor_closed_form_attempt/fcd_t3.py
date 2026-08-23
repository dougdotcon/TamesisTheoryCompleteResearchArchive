"""T3 -- abstract recursive-process mechanism validation, real seed
   SeedSequence(20260833003), N=40000 per t0.
"""
import numpy as np
import sys
sys.path.insert(0, "/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/generalization_u_alpha/mclust_rigor/residual_attempt/aggregation_closure_attempt/global_exclusion_attempt/x0_asymmetry_attempt/elevation_level_attempt/short_cycle_dynamics_attempt")
import sc_formula as F


def simulate_one(t0, c, rng):
    s = 0.0
    g = t0
    mode = 'G'
    for _ in range(200000):
        T = rng.exponential(1.0 / c)
        if mode == 'G':
            if T >= g:
                return True
            s = s + T
            g = g - T
        else:
            s = s + T
        if s >= 1.0:
            return False
        u = rng.random()
        if u < s:
            return False
        elif u < s + g:
            g = g * rng.random()
            mode = 'G'
        else:
            mode = 'E'
    return False


def phi_abstract(t0, c, N, rng):
    succ = 0
    for _ in range(N):
        if simulate_one(t0, c, rng):
            succ += 1
    return succ / N


c = 1000
N = 40000
t0_values = [1e-4, 3e-4, 1e-3, 3e-3, 0.01, 0.03, 0.05, 0.09, 0.18, 0.37, 0.60, 0.90]

ss = np.random.SeedSequence(20260833003)
children = ss.spawn(len(t0_values))

results = []
for t0, child in zip(t0_values, children):
    rng = np.random.default_rng(child)
    p = phi_abstract(t0, c, N, rng)
    se = np.sqrt(p * (1 - p) / N)
    results.append((t0, p, se))
    print(f"t0={t0:.5f}  phi_abstract={p:.5f}+-{se:.5f}")

phiU = F.phi_U(c)
print(f"\nphi_U(c) = {phiU:.5f}")

# plateau criterion: ratio of phi_abstract at two largest t0 to value at t0=0.09
idx_009 = [i for i, (t0, _, _) in enumerate(results) if abs(t0 - 0.09) < 1e-9][0]
base = results[idx_009][1]
last_two = results[-2:]
ratios = [p / base for (_, p, _) in last_two]
print(f"\nbase (t0=0.09) phi_abstract = {base:.5f}")
print(f"ratios at last two t0 values: {ratios}")
plateau_ok = all(0.5 <= r <= 2.0 for r in ratios)
print("T3 plateau criterion " + ("CONFIRMED (stays within 0.5x-2x)" if plateau_ok else "NOT confirmed"))
