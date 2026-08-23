"""
ref_mp_worker.py -- multiprocessing worker for real-engine (n=65536) runs.
Each worker handles a batch of instances and returns aggregated per-bin
counts/sums plus the per-instance per-bin means (for cluster-level SEM).
"""
import numpy as np
import ref_common as RC


def run_batch(args):
    n, c, seed_ints, bin_edges = args
    n_bins = len(bin_edges) - 1
    tot_counts = np.zeros(n_bins)
    tot_sums = np.zeros(n_bins)
    inst_means_list = []
    for sv in seed_ints:
        rng = np.random.default_rng(int(sv))
        counts, sums, inst_means = RC.run_one_instance_binned(n, c, rng, bin_edges)
        tot_counts += counts
        tot_sums += sums
        inst_means_list.append(inst_means)
    return tot_counts, tot_sums, np.array(inst_means_list)
