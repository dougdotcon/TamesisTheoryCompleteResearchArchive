"""
ref_identity_check.py -- referee's own quick sanity check, real engine scale.

Not the main focus of this review (the orchestrating session already did an
exact brute-force Fraction-arithmetic verification of Facts A/B and identity
(1.1) at n=5,6). This is just a belt-and-braces check at the real n=65536
engine scale, using code written from scratch (ref_common.py), to confirm:
  (i) b=1 gives R_mask == seed_mask exactly (0 violations)
  (ii) L(x0) is close to uniform on {1..n} among non-seed points (Fact A/B
       jointly, empirically)
  (iii) the identity (1.1): phi_far(threshold) measured directly vs via the
        weighted sum of per-bin phi-hats, same run, must match (near-)exactly.

Seed: SeedSequence(20260834000), reserved referee range per DISC-DEC-057,
confirmed unused elsewhere before use.
"""
import time
import numpy as np
import ref_common as RC

n = 65536
c = 1000
threshold = 2000
N = 400

ss = np.random.SeedSequence(20260834000)
children = ss.spawn(N + 5)

# (i) R_mask == seed_mask exactly at b=1 -- direct code check (not a random test)
import sc_engine as E
rng0 = np.random.default_rng(children[-1])
viol = 0
for _ in range(20):
    pi = E.build_pi(n, rng0)
    seed_mask = E.build_seeds(n, c, rng0)
    R_mask = E.build_R_mask(n, 1, pi, seed_mask)
    viol += int(np.count_nonzero(R_mask != seed_mask))
print(f"(i) b=1 R_mask==seed_mask exactly: violations={viol}/20  {'OK' if viol==0 else 'FAIL'}")

# (ii)+(iii): run N instances, aggregate
bin_edges = np.array([1, 2000, 4000, 8000, 16384, 32768, 65537], dtype=np.float64)
n_bins = len(bin_edges) - 1

t0 = time.time()
total_counts = np.zeros(n_bins)
total_sums = np.zeros(n_bins)
direct_count = 0.0
direct_sum = 0.0

for i in range(N):
    rng = np.random.default_rng(children[i])
    dc, ds, cb, sb = RC.phi_far_direct_and_binned(n, c, rng, threshold, bin_edges)
    direct_count += dc
    direct_sum += ds
    total_counts += cb
    total_sums += sb

t1 = time.time()
print(f"  ({N} instances, {t1-t0:.1f}s)")

phi_far_direct = direct_sum / direct_count
phi_far_via_bins = np.sum(total_sums) / np.sum(total_counts)  # same-count reweight (weighted by measured n_pts)
print(f"(iii) phi_far direct = {phi_far_direct:.6f}  (n_pts={direct_count:.0f})")
print(f"      phi_far via measured-count-weighted per-bin sum = {phi_far_via_bins:.6f}")
print(f"      match: {'EXACT (same underlying sums)' if abs(phi_far_direct-phi_far_via_bins)<1e-12 else 'DIFFERS'}")

# theoretical-width reweighting variant (like the front's disclosed T0 3rd variant)
phi_hat_bins = total_sums / np.maximum(total_counts, 1)
widths = np.diff(bin_edges)
# restrict to only the far-tail bins (edges >= threshold)
far_bin_mask = bin_edges[:-1] >= threshold
w = widths[far_bin_mask]
ph = phi_hat_bins[far_bin_mask]
phi_far_theory_weighted = np.sum(w * ph) / np.sum(w)
print(f"      via theoretical-bin-width-weighted per-bin phi-hat = {phi_far_theory_weighted:.6f}")

# (ii) uniformity of L among non-seed points: chi-square-ish check via coarse deciles
print("\n(ii) L uniformity check (coarse, 10 equal-width bins over [1,n], non-seed points):")
dec_edges = np.linspace(1, n + 1, 11)
n_bins2 = 10
tot2 = np.zeros(n_bins2)
for i in range(min(N, 200)):
    rng = np.random.default_rng(children[i])
    counts, sums, _ = RC.run_one_instance_binned(n, c, rng, dec_edges)
    tot2 += counts
expected = tot2.sum() / n_bins2
chi2 = np.sum((tot2 - expected) ** 2 / expected)
print(f"  decile counts (should be ~equal): {tot2.astype(int)}")
print(f"  chi2({n_bins2-1} dof) = {chi2:.2f}  (uniform expected ~{n_bins2-1})")
