"""T2 -- fine ell/n sub-binning, sign-change characterization.
   Seed SeedSequence(20260833002), N=3000.
"""
import sys
sys.path.insert(0, "/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/generalization_u_alpha/mclust_rigor/residual_attempt/aggregation_closure_attempt/global_exclusion_attempt/x0_asymmetry_attempt/elevation_level_attempt/short_cycle_dynamics_attempt")
import numpy as np
import sc_engine as E
import sc_formula as F

n, c, b = 65536, 1000, 1
N = 3000

bin_edges = np.array([2000, 4000, 8000, 16384, 24576, 32768, 40960, 49152, 57344, 65536])
counts = np.zeros(len(bin_edges) - 1)
cyclic = np.zeros(len(bin_edges) - 1)

ss = np.random.SeedSequence(20260833002)
children = ss.spawn(N)
for k in range(N):
    rng = np.random.default_rng(children[k])
    pi = E.build_pi(n, rng)
    seed_mask = E.build_seeds(n, c, rng)
    R_mask = E.build_R_mask(n, b, pi, seed_mask)
    f = E.build_f(n, pi, R_mask, rng)
    cyc_mask = E.cyclic_mask_peeling(f)
    clens = E.pi_cycle_lengths(pi)

    notseed = ~seed_mask
    L_all = clens[notseed]
    cyc_all = cyc_mask[notseed]
    idx = np.digitize(L_all, bin_edges) - 1
    for bi in range(len(bin_edges) - 1):
        sel = idx == bi
        counts[bi] += sel.sum()
        cyclic[bi] += cyc_all[sel].sum()

phiU = F.phi_U(c)
print(f"phi_U(c) = {phiU:.6f}")
print("bin edges:", bin_edges.tolist())
pos_bin_found = False
neg_last_bin = False
for bi in range(len(bin_edges) - 1):
    phat = cyclic[bi] / counts[bi]
    se = np.sqrt(phat * (1 - phat) / counts[bi])
    devpct = 100 * (phat / phiU - 1)
    z = (phat - phiU) / se
    lo_frac = bin_edges[bi] / n
    hi_frac = bin_edges[bi + 1] / n
    print(f"  L/n in ({lo_frac:.3f},{hi_frac:.3f}]  n_pts={int(counts[bi])}  "
          f"phat={phat:.5f}+-{se:.5f}  dev%={devpct:+.2f}  z={z:+.2f}")
    if 0.1 <= lo_frac < 0.6 and z >= 3:
        pos_bin_found = True
    if bi == len(bin_edges) - 2 and lo_frac > 0.875 and z <= -3:
        neg_last_bin = True

print(f"\npositive bin found in [0.1,0.6) with z>=+3: {pos_bin_found}")
print(f"last bin (L/n>0.875) significantly negative, z<=-3: {neg_last_bin}")
print("T2 sign-change pattern " + ("CONFIRMED" if (pos_bin_found and neg_last_bin) else "NOT confirmed by pre-registered criterion"))
