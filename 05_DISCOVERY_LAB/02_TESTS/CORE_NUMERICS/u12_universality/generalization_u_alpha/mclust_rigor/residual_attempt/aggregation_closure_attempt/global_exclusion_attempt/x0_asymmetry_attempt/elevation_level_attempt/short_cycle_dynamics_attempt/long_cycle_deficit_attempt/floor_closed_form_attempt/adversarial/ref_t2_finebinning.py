"""
ref_t2_finebinning.py -- referee's own independent replication of the
front's T2/T2b (fine L/n sub-binning of phi(ell), cluster-robust SEM).

Written from scratch against sc_engine.py/sc_formula.py; fcd_t2.py and
fcd_t2_cluster.py were not read or imported. Same target cell as the front
(c=1000, n=65536, b=1); same bin edges as the front's own T2 for direct
comparability (the measurement code, cluster-SEM logic, and seeds are all
independent). Reports BOTH the naive per-point binomial SEM/z AND the
cluster-robust (per-instance) SEM/z from the SAME run, so the inflation
factor is visible directly, plus runs TWO independently-seeded copies
(run A, run B) to check cross-run replication -- this is a properly-powered
design per the mandate (N per run 4-5x the front's own N=3000, and two
independent seeds rather than one plus a smaller follow-up).

Usage: python3 ref_t2_finebinning.py <A|B>
Seeds: SeedSequence(20260834002) for A, SeedSequence(20260834003) for B --
referee-reserved range (DISC-DEC-057), confirmed unused elsewhere before use.
"""
import sys
import time
import numpy as np
import ref_common as RC
import sc_formula as F

run_label = sys.argv[1] if len(sys.argv) > 1 else "A"
seed = 20260834002 if run_label == "A" else 20260834003

n = 65536
c = 1000
N = 15000  # 5x the front's own N=3000 per run

bin_edges = np.array(
    [2000, 4000, 8000, 16384, 24576, 32768, 40960, 49152, 57344, 65537],
    dtype=np.float64,
)
n_bins = len(bin_edges) - 1
phiU = F.phi_U(c)

print(f"ref_t2_finebinning run {run_label}: n={n} c={c} N={N} seed={seed} phi_U={phiU:.6f}")
t0 = time.time()
total_counts, total_sums, inst_means = RC.run_parallel(n, c, seed, N, bin_edges, n_workers=4, chunk=250)
t1 = time.time()
print(f"done in {t1-t0:.1f}s")

phi_hat = total_sums / total_counts
sem_pt = np.sqrt(phi_hat * (1 - phi_hat) / total_counts)
dev_pt = 100.0 * (phi_hat / phiU - 1.0)
z_pt = (phi_hat - phiU) / sem_pt

# cluster-level: for each bin, average over instances that had >=1 point in
# that bin (nan-aware); cluster SEM = std(inst_means, ddof=1)/sqrt(n_inst_with_data)
cluster_mean = np.nanmean(inst_means, axis=0)
n_inst_with_data = np.sum(~np.isnan(inst_means), axis=0)
cluster_std = np.nanstd(inst_means, axis=0, ddof=1)
cluster_sem = cluster_std / np.sqrt(n_inst_with_data)
dev_cl = 100.0 * (cluster_mean / phiU - 1.0)
z_cl = (cluster_mean - phiU) / cluster_sem

print(f"\n{'L bin':>18} {'n_pts':>12} {'n_inst':>7} {'phi_hat_pt':>11} {'dev%_pt':>8} {'z_pt':>8} "
      f"| {'phi_cl':>9} {'dev%_cl':>8} {'clSEM':>8} {'z_cl':>8}")
rows = []
for i in range(n_bins):
    lo, hi = bin_edges[i], min(bin_edges[i + 1], n)
    label = f"({int(lo)},{int(hi)}]"
    print(f"{label:>18} {int(total_counts[i]):>12} {int(n_inst_with_data[i]):>7} "
          f"{phi_hat[i]:>11.5f} {dev_pt[i]:>8.2f} {z_pt[i]:>8.2f} | "
          f"{cluster_mean[i]:>9.5f} {dev_cl[i]:>8.2f} {cluster_sem[i]:>8.5f} {z_cl[i]:>8.2f}")
    rows.append((label, total_counts[i], n_inst_with_data[i], phi_hat[i], dev_pt[i], z_pt[i],
                 cluster_mean[i], dev_cl[i], cluster_sem[i], z_cl[i]))

# save to npz for cross-run comparison
np.savez(f"ref_t2_run{run_label}.npz",
          bin_edges=bin_edges, total_counts=total_counts, total_sums=total_sums,
          phi_hat=phi_hat, cluster_mean=cluster_mean, cluster_sem=cluster_sem,
          n_inst_with_data=n_inst_with_data, dev_cl=dev_cl, z_cl=z_cl)

# does ANY bin show a significant POSITIVE cluster-level deviation?
pos_sig = [(rows[i][0], z_cl[i]) for i in range(n_bins) if z_cl[i] > 3]
neg_sig = [(rows[i][0], z_cl[i]) for i in range(n_bins) if z_cl[i] < -3]
print(f"\nBins with cluster-robust z_cl > +3 (significant POSITIVE deviation): {pos_sig if pos_sig else 'NONE'}")
print(f"Bins with cluster-robust z_cl < -3 (significant NEGATIVE deviation): {neg_sig if neg_sig else 'NONE'}")
print(f"Mean dev%_cl across all bins: {np.mean(dev_cl):.3f}%  (range {dev_cl.min():.2f}% to {dev_cl.max():.2f}%)")
