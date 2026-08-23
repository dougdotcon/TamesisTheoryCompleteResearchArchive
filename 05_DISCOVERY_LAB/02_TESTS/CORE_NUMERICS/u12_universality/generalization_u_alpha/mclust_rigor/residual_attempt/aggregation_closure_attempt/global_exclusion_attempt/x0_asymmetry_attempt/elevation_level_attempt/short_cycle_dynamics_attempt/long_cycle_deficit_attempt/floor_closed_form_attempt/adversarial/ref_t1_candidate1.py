"""
ref_t1_candidate1.py -- referee's own independent replication of the
front's T1 (Candidate-1 rejection: phi(ell) ~= exp(-c (ell/n)^2)).

Written from scratch against sc_engine.py/sc_formula.py; fcd_t1.py was not
read or imported. Target cell c=1000, n=65536, b=1 (matches ATTEMPT.md so
the result is directly comparable). Bin edges chosen to match the front's
own T1 bins for direct comparability (choosing bin edges does not bias the
measurement, only interpretability); measurement code is 100% independent.

Seed: SeedSequence(20260834001), referee-reserved range (DISC-DEC-057),
confirmed unused elsewhere before use.
"""
import time
import numpy as np
import ref_common as RC

n = 65536
c = 1000
N = 8000  # >5x the front's own N=1500

bin_edges = np.array([1, 50, 200, 500, 1000, 2000, 4000, 8000, 16384, 32768, 65537], dtype=np.float64)
n_bins = len(bin_edges) - 1

print(f"ref_t1_candidate1: n={n} c={c} N={N} n_bins={n_bins}")
t0 = time.time()
total_counts, total_sums, inst_means = RC.run_parallel(n, c, 20260834001, N, bin_edges, n_workers=4, chunk=250)
t1 = time.time()
print(f"done in {t1-t0:.1f}s")

phi_hat = total_sums / total_counts
sem = np.sqrt(phi_hat * (1 - phi_hat) / total_counts)  # naive point-level SEM, for direct comparability w/ front's table

mids = 0.5 * (bin_edges[:-1] + np.minimum(bin_edges[1:], n))
cand1 = RC.candidate1_pred(mids, c, n)
z = (phi_hat - cand1) / sem

phiU = None
try:
    import sc_formula as F
    phiU = F.phi_U(c)
except Exception:
    pass

print(f"\nphi_U({c}) = {phiU:.6f}" if phiU is not None else "")
print(f"{'bin':>18} {'n_pts':>12} {'phi_hat':>10} {'SEM':>10} {'cand1_pred':>12} {'z':>10}")
for i in range(n_bins):
    lo, hi = bin_edges[i], min(bin_edges[i+1], n)
    label = f"[{int(lo)},{int(hi)})" if hi < n else f"[{int(lo)},{int(hi)}]"
    print(f"{label:>18} {int(total_counts[i]):>12} {phi_hat[i]:>10.5f} {sem[i]:>10.6f} {cand1[i]:>12.6f} {z[i]:>10.1f}")

# pre-registered-style criterion (same bar the front used): >=3 of the L>=4000 bins
# at z>=10 against the Candidate-1 prediction
far_idx = [i for i in range(n_bins) if bin_edges[i] >= 4000]
n_far_pass = sum(1 for i in far_idx if z[i] >= 10)
print(f"\nL>=4000 bins: {len(far_idx)}, at z>=10 against Candidate-1: {n_far_pass}")
print(f"Criterion (>=3 of L>=4000 bins at z>=10): {'MET' if n_far_pass >= 3 else 'NOT MET'}")

# plateau check: does phi_hat for L>=2000 stay within a factor of 2 of its own mean,
# rather than decaying toward 0 like Candidate-1 predicts?
plateau_idx = [i for i in range(n_bins) if bin_edges[i] >= 2000]
plateau_vals = phi_hat[plateau_idx]
print(f"\nphi_hat over L>=2000 bins: {plateau_vals}")
print(f"  max/min ratio = {plateau_vals.max()/plateau_vals.min():.3f} (plateau if close to 1; Candidate-1 predicts orders-of-magnitude decay)")
print(f"  cand1 over same bins: {cand1[plateau_idx]}")
