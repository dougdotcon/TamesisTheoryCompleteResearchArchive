import sys
sys.path.insert(0, "/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/generalization_u_alpha/mclust_rigor/residual_attempt/aggregation_closure_attempt/global_exclusion_attempt/x0_asymmetry_attempt/elevation_level_attempt/short_cycle_dynamics_attempt")
import numpy as np
import sc_engine as E
import sc_formula as F

# THROWAWAY exploratory seed
ss = np.random.SeedSequence(20260833902)

c = 1000
b = 1

for n, N in [(16384, 600), (65536, 150), (262144, 40)]:
    t_lo, t_hi = 0.25, 0.50
    lo, hi = int(t_lo*n), int(t_hi*n)
    counts = 0
    cyclic = 0
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
        sel = (L_all > lo) & (L_all <= hi)
        counts += sel.sum()
        cyclic += cyc_all[sel].sum()
    phat = cyclic/counts
    se = np.sqrt(phat*(1-phat)/counts)
    print(f"n={n:7d} N={N:4d}  L in ({lo},{hi}]  n_pts={counts:9d}  phat={phat:.5f}+-{se:.5f}  "
          f"phi_U(c)={F.phi_U(c):.5f}  dev%={100*(phat/F.phi_U(c)-1):+.2f}")
