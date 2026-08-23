"""T0 -- sanity check of the exact reduction identity (0.1):
   phi_far(threshold) computed directly == weighted average of phi(ell) over
   fine L-bins, in the SAME run. Seed SeedSequence(20260833000), N=2000.
"""
import sys
sys.path.insert(0, "/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/generalization_u_alpha/mclust_rigor/residual_attempt/aggregation_closure_attempt/global_exclusion_attempt/x0_asymmetry_attempt/elevation_level_attempt/short_cycle_dynamics_attempt")
import numpy as np
import sc_engine as E
import sc_formula as F

n, c, b = 65536, 1000, 1
threshold = 2000
N = 2000

ss = np.random.SeedSequence(20260833000)
children = ss.spawn(N)

# direct measurement
direct_count = 0
direct_cyclic = 0

# fine-bin measurement (bin width 200, from threshold+1 to n)
bin_edges = np.arange(threshold, n + 1, 200)
if bin_edges[-1] != n:
    bin_edges = np.append(bin_edges, n)
bin_counts = np.zeros(len(bin_edges) - 1)
bin_cyclic = np.zeros(len(bin_edges) - 1)

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

    sel = L_all > threshold
    direct_count += sel.sum()
    direct_cyclic += cyc_all[sel].sum()

    idx = np.digitize(L_all, bin_edges) - 1
    for bi in range(len(bin_edges) - 1):
        m = idx == bi
        bin_counts[bi] += m.sum()
        bin_cyclic[bi] += cyc_all[m].sum()

phi_direct = direct_cyclic / direct_count
se_direct = np.sqrt(phi_direct * (1 - phi_direct) / direct_count)

# weighted average via bins (weight = bin_counts, i.e. empirical L-density,
# which should match 1/n uniform up to MC noise -- this cross-checks Fact A too)
total_w = bin_counts.sum()
phi_binned = (bin_cyclic.sum()) / total_w  # equivalent identity check by construction
# a genuinely independent computation: per-bin phat, weighted by UNIFORM
# theoretical density (1/n per ell), i.e. weight ~ bin width, NOT measured count
bin_widths = np.diff(bin_edges)
bin_phat = np.divide(bin_cyclic, bin_counts, out=np.full_like(bin_counts, np.nan), where=bin_counts > 0)
phi_theoretical_weighted = np.nansum(bin_phat * bin_widths) / bin_widths.sum()

print(f"direct: phi_far={phi_direct:.6f} +- {se_direct:.6f}  (n_pts={direct_count})")
print(f"binned (measured-count weighted): phi_far={phi_binned:.6f}  (n_pts={int(total_w)})")
print(f"binned (theoretical uniform-width weighted): phi_far={phi_theoretical_weighted:.6f}")
diff = phi_direct - phi_theoretical_weighted
z = diff / se_direct
print(f"direct - theoretical_weighted = {diff:.6f}  z (vs direct SEM) = {z:.3f}")
print("T0 " + ("PASSED" if abs(z) < 3 else "FAILED"))

print(f"\nphi_U(c) = {F.phi_U(c):.6f}")
