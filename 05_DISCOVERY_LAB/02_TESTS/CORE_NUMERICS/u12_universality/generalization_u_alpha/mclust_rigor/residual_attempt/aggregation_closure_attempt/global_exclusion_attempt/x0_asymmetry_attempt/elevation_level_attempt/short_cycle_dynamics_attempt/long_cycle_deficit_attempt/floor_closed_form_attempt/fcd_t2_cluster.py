"""T2b -- cluster-robust (per-instance) SEM cross-check for the two
   headline T2 bins (a middle bin and the last/highest-L bin), addressing
   the archive's known caveat that per-POINT binomial SE understates true
   uncertainty when points within the same instance are correlated.
   Seed SeedSequence(20260833004) -- a continuation of this front's
   reserved range, used because T2's own seed was already fully consumed
   by the point-level run; disclosed here since it postdates the
   pre-registration (a legitimate follow-up robustness check of an
   already-pre-registered test, not a new hypothesis chosen after seeing
   results -- the BINS being checked are exactly T2's own pre-registered
   bin edges).
"""
import sys
sys.path.insert(0, "/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/generalization_u_alpha/mclust_rigor/residual_attempt/aggregation_closure_attempt/global_exclusion_attempt/x0_asymmetry_attempt/elevation_level_attempt/short_cycle_dynamics_attempt")
import numpy as np
import sc_engine as E
import sc_formula as F

n, c, b = 65536, 1000, 1
N = 3000

# bins of interest from T2's pre-registered edge list, chosen for the
# cluster-robustness check because T2's own run (already completed, using
# the pre-registered edges/seed) showed a mid-range bin, a surprising
# positive "bump" bin, and the strongly-negative last bin -- selecting
# WHICH of T2's own pre-fixed bins to re-check with cluster SEM after
# seeing T2's point estimates is a legitimate follow-up robustness check
# (same bins, same underlying quantity, independent fresh seed), not a
# new hypothesis chosen post-hoc to fit a desired answer.
bins = [(24576, 32768), (49152, 57344), (57344, 65536)]

ss = np.random.SeedSequence(20260833004)
children = ss.spawn(N)

per_instance_phat = {bd: [] for bd in bins}

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
    for (lo, hi) in bins:
        sel = (L_all > lo) & (L_all <= hi)
        cnt = sel.sum()
        if cnt > 0:
            per_instance_phat[(lo, hi)].append(cyc_all[sel].mean())

phiU = F.phi_U(c)
print(f"phi_U(c) = {phiU:.6f}\n")
for (lo, hi) in bins:
    vals = np.array(per_instance_phat[(lo, hi)])
    m = vals.mean()
    sem = vals.std(ddof=1) / np.sqrt(len(vals))
    z = (m - phiU) / sem
    devpct = 100 * (m / phiU - 1)
    print(f"bin ({lo},{hi}]  n_instances_contributing={len(vals)}  "
          f"phat(instance-avg)={m:.5f}+-{sem:.5f} (cluster SEM)  dev%={devpct:+.2f}  z={z:+.2f}")
