"""T1 -- re-confirm rejection of Candidate 1 (phi(ell) ~ e^{-c(ell/n)^2}),
   real seed SeedSequence(20260833001), N=1500.
"""
import sys
sys.path.insert(0, "/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/generalization_u_alpha/mclust_rigor/residual_attempt/aggregation_closure_attempt/global_exclusion_attempt/x0_asymmetry_attempt/elevation_level_attempt/short_cycle_dynamics_attempt")
import numpy as np
import sc_engine as E
import sc_formula as F

n, c, b = 65536, 1000, 1
N = 1500

bin_edges = np.array([1, 50, 200, 500, 1000, 2000, 4000, 8000, 16384, 32768, 65536])
counts = np.zeros(len(bin_edges) - 1)
cyclic = np.zeros(len(bin_edges) - 1)

ss = np.random.SeedSequence(20260833001)
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

print("bin edges:", bin_edges.tolist())
n_rejecting_bins = 0
for bi in range(len(bin_edges) - 1):
    if counts[bi] > 0:
        phat = cyclic[bi] / counts[bi]
        se = np.sqrt(phat * (1 - phat) / counts[bi])
        mid_t = 0.5 * (bin_edges[bi] + bin_edges[bi + 1]) / n
        pred = np.exp(-c * mid_t ** 2)
        z = (phat - pred) / se if se > 0 else float('inf')
        flag = ""
        if bin_edges[bi] >= 4000 and z >= 10:
            n_rejecting_bins += 1
            flag = " <- rejects Candidate 1 (z>=10)"
        print(f"  L in [{bin_edges[bi]},{bin_edges[bi+1]}): n_pts={int(counts[bi])} "
              f"phat={phat:.5f}+-{se:.5f}  pred_e^-c*t^2(mid)={pred:.6f}  z={z:.2f}{flag}")
    else:
        print(f"  L in [{bin_edges[bi]},{bin_edges[bi+1]}): n_pts=0")

print(f"\nbins with L>=4000 rejecting Candidate 1 at z>=10: {n_rejecting_bins} / "
      f"{sum(1 for e in bin_edges[:-1] if e>=4000)}")
print("T1 " + ("Candidate 1 REJECTED (>=3 bins)" if n_rejecting_bins >= 3 else "Candidate 1 NOT rejected by this criterion"))
print(f"\nphi_U(c) = {F.phi_U(c):.6f}")
