"""
sc_batch.py -- batched (vectorized-across-instances) versions of the
cycle-detection step of sc_engine.py, for performance. The mechanism
(build_instance) is unchanged and reused from sc_engine.py -- this module
only speeds up the O(n) cyclic-mask computation by processing many instances'
f-arrays at once with numpy scatter operations instead of a per-instance
Python deque loop.

Correctness of the batched peeling is checked against sc_engine's own
per-instance cyclic_mask_peeling (already cross-checked against brute force
in sc_engine.py selftest) before being trusted for any reported number.
"""

import numpy as np
import sc_engine as eng


def cyclic_mask_peeling_batch(f_batch):
    """f_batch: shape (M, n) int array, each row an independent functional
    graph on [0..n-1]. Returns boolean array (M, n): True iff on a cycle.

    Round-based (level-synchronous) Kahn peeling, vectorized across the whole
    batch with scatter (np.add.at) instead of a per-node Python loop.
    """
    M, n = f_batch.shape
    # global flat index space: instance i, node x  ->  i*n + x
    row_idx = np.repeat(np.arange(M), n)
    flat_targets = (row_idx * n + f_batch.reshape(-1)).astype(np.int64)
    indeg_flat = np.bincount(flat_targets, minlength=M * n).astype(np.int32)
    indeg = indeg_flat.reshape(M, n)
    active = np.ones((M, n), dtype=bool)

    rounds = 0
    while True:
        removable = active & (indeg == 0)
        if not removable.any():
            break
        active &= ~removable
        rows, cols = np.nonzero(removable)
        targets = f_batch[rows, cols]
        global_idx = rows.astype(np.int64) * n + targets
        indeg_flat2 = indeg.reshape(-1)
        np.add.at(indeg_flat2, global_idx, -1)
        indeg = indeg_flat2.reshape(M, n)
        rounds += 1
        if rounds > n:  # safety valve, should never trigger
            raise RuntimeError("peeling did not converge")
    return active, rounds


def build_f_batch(n, b, c, rng, M):
    """Build M independent M-CLUST(b) instances; return f_batch (M,n) and,
    for convenience, the per-instance R-mask (M,n) (needed by callers that
    condition on x0 in/out of R)."""
    f_batch = np.empty((M, n), dtype=np.int64)
    R_batch = np.empty((M, n), dtype=bool)
    for i in range(M):
        inst = eng.build_instance(n, b, c, rng)
        f_batch[i] = inst["f"]
        R_batch[i] = inst["R_mask"]
    return f_batch, R_batch


if __name__ == "__main__":
    import sys
    import time

    print("sc_batch.py selftest -- batched peeling vs sc_engine's per-instance peeling")
    ss = np.random.SeedSequence(20260825900).spawn(3)[2]  # distinct sub-stream, still under the T0 selftest seed
    rng = np.random.default_rng(ss)

    n, b, c, M = 8192, 20, 60, 40
    f_batch, R_batch = build_f_batch(n, b, c, rng, M)

    t0 = time.time()
    active_batch, rounds = cyclic_mask_peeling_batch(f_batch)
    t1 = time.time()
    print(f"  batched peeling: {M} instances, n={n}: {t1-t0:.4f}s total, {rounds} rounds")

    mismatches = 0
    t2 = time.time()
    for i in range(M):
        mask_single = eng.cyclic_mask_peeling(f_batch[i])
        if not np.array_equal(mask_single, active_batch[i]):
            mismatches += 1
    t3 = time.time()
    print(f"  per-instance peeling (cross-check): {t3-t2:.4f}s total")
    print(f"  mismatches: {mismatches} / {M}  {'OK' if mismatches == 0 else 'FAIL'}")

    # timing at production scale
    print("\n(timing) production scale: n=65536, b=100, c=1000, batch M=500")
    rng2 = np.random.default_rng(np.random.SeedSequence(20260825900).spawn(4)[3])
    t0 = time.time()
    f_batch2, R_batch2 = build_f_batch(65536, 100, 1000, rng2, 500)
    t1 = time.time()
    active2, rounds2 = cyclic_mask_peeling_batch(f_batch2)
    t2 = time.time()
    phi_vals = active2.mean(axis=1)
    print(f"  build 500 instances: {t1-t0:.3f}s   batched peel: {t2-t1:.3f}s ({rounds2} rounds)")
    print(f"  phi mean over 500 instances: {phi_vals.mean():.5f} +- {phi_vals.std(ddof=1)/np.sqrt(500):.5f}")

    sys.exit(1 if mismatches else 0)
