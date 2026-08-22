"""
Adversarial verification -- own quadrature targets, computed BEFORE
simulation, from formulas re-derived independently in ADVERSARIAL_NOTE.md.
Fresh parameter grid (c, p, b, n) -- none copied from the target front's
predictions.json.
"""
import json
import numpy as np
from scipy import integrate

def phi_U(c):
    f = lambda t: np.exp(-c * t * t)
    val, err = integrate.quad(f, 0, 1)
    return val

def phi_MIX(p, c):
    f = lambda t: np.exp(-c * (p * t + (1 - p) * t * t))
    val, err = integrate.quad(f, 0, 1)
    return val

def phi_PREVSELF(c):
    if c == 0:
        return 1.0
    return (1 - np.exp(-c)) / c

def phi_CLUST_target(c, b, n):
    c_eff = c * (1 - c / n) ** b
    return phi_U(c_eff), c_eff

n1 = 65536
c_grid1 = [0.3, 3.0, 18.0, 70.0, 220.0]
p_mix = 0.3
b_clust = 13

n2 = 65536
c_grid2 = [10.0, 50.0, 150.0, 400.0]
b_clust2 = 50

targets = {"n1": n1, "c_grid1": c_grid1, "p_mix": p_mix, "b_clust": b_clust,
           "n2": n2, "c_grid2": c_grid2, "b_clust2": b_clust2}

targets["M-U"] = {str(c): phi_U(c) for c in c_grid1}
targets["M-MIX_p0.3"] = {str(c): phi_MIX(p_mix, c) for c in c_grid1}
targets["M-PREV"] = {str(c): phi_PREVSELF(c) for c in c_grid1}
clust1 = {}
for c in c_grid1:
    val, ceff = phi_CLUST_target(c, b_clust, n1)
    clust1[str(c)] = {"target": val, "c_eff": ceff, "band_2bc_over_n": 2 * b_clust * c / n1}
targets["M-CLUST13"] = clust1

clust2 = {}
for c in c_grid2:
    val, ceff = phi_CLUST_target(c, b_clust2, n2)
    clust2[str(c)] = {"target": val, "c_eff": ceff, "band_2bc_over_n": 2 * b_clust2 * c / n2}
targets["M-CLUST50_stress"] = clust2

# M-SHARED comparison baselines (no target, exploratory)
c_grid4 = [3.0, 18.0, 70.0]
targets["M-SHARED_baseline_untouched_cycles"] = {str(c): phi_PREVSELF(c) for c in c_grid4}
targets["M-SHARED_comparison_phiU"] = {str(c): phi_U(c) for c in c_grid4}

# M-INTRA heuristic (their formula, evaluated at OUR c grid, for descriptive
# comparison only -- not used as a pass/fail target since it is HEURISTIC)
def phi_INTRA_heuristic(c):
    # phi_INTRA(c) ~= int_0^1 min(1, sqrt(pi/(4 c l))) dl  (their eq., psi(lambda)=sqrt(pi)/(2 sqrt(lambda)))
    def integrand(l):
        lam = c * l
        if lam <= 0:
            return 1.0
        psi = np.sqrt(np.pi) / (2 * np.sqrt(lam))
        return min(1.0, psi)
    val, err = integrate.quad(integrand, 1e-12, 1, limit=200)
    return val

c_grid3 = [20.0, 80.0, 320.0, 1000.0]
targets["M-INTRA_heuristic_descriptive"] = {str(c): phi_INTRA_heuristic(c) for c in c_grid3}
targets["c_grid3_intra"] = c_grid3
targets["n3_intra"] = 131072

with open("/tmp/claude-0/-home-user-TamesisTheoryCompleteResearchArchive/e9ab1ff0-e9f9-5b73-816d-aec417acf7b1/scratchpad/adv_predictions.json", "w") as fh:
    json.dump(targets, fh, indent=2)

print(json.dumps(targets, indent=2))
