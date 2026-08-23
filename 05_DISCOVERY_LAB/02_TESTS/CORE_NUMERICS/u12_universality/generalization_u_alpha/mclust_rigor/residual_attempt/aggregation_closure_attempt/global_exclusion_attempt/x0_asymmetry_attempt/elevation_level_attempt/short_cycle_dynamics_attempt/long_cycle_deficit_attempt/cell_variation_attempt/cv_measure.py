"""
cv_measure.py -- shared far-tail measurement function for
CELL-VARIATION-ATTEMPT (DISC-DEC-057 front e). Reuses sc_engine.py /
sc_formula.py from short_cycle_dynamics_attempt/ (two directories up)
UNMODIFIED, by import. No new engine written.

Same measurement logic as long_cycle_deficit_attempt/lcd_bsweep.py's
measure_far_tail (phi(cyclic | x0 in R^c, L>threshold) vs phi_U(c'')), but
authored fresh for this front and parallelized across worker processes for
wall-clock feasibility at 26 measurement runs (DERIVATION_PREREG.md SS5).
Verified bit-identical to single-process on a throwaway seed before use.
"""

import sys
import os
import time
import numpy as np
import multiprocessing as mp

PARENT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
sys.path.insert(0, PARENT)
import sc_engine as eng   # noqa: E402
import sc_formula as fm   # noqa: E402


def _one_instance(args):
    """One M-CLUST(b) instance: build it, peel for cyclic points, compute
    pi-cycle lengths, and return the far-tail (x0 in R^c, L>threshold) counts
    plus the measured rho for this instance."""
    n, b, c, child_seed, threshold = args
    rng = np.random.default_rng(child_seed)
    inst = eng.build_instance(n, b, c, rng)
    pi, R_mask, f = inst["pi"], inst["R_mask"], inst["f"]
    cyclic = eng.cyclic_mask_peeling(f)
    cyc_len = eng.pi_cycle_lengths(pi)

    Rc_mask = ~R_mask
    far_mask = Rc_mask & (cyc_len > threshold)

    n_far = int(far_mask.sum())
    cyc_far = int(cyclic[far_mask].sum())
    rho = float(R_mask.mean())
    return n_far, cyc_far, rho


def measure_far_tail(n, b, c, N, seed_seq, threshold, nworkers=4,
                      log=print, log_every=500, label=""):
    """phi(cyclic | x0 in R^c, L>threshold) at (n,b,c), N instances, against
    phi_U(c''(b,c,n)). threshold is an ABSOLUTE L value (caller-supplied),
    not derived from b here -- callers pass 20*b_original for both the
    own-b and the b=1 companion run, per DERIVATION_PREREG.md SS2-3."""
    ss = np.random.SeedSequence(seed_seq)
    children = ss.spawn(N)
    args = [(n, b, c, ch, threshold) for ch in children]

    t0 = time.time()
    results = []
    if nworkers and nworkers > 1:
        with mp.Pool(nworkers) as pool:
            for i, r in enumerate(pool.imap(_one_instance, args, chunksize=20)):
                results.append(r)
                if log_every and (i + 1) % log_every == 0:
                    log(f"    [{label}] [{i+1}/{N}] elapsed={time.time()-t0:.1f}s")
    else:
        for i, a in enumerate(args):
            results.append(_one_instance(a))
            if log_every and (i + 1) % log_every == 0:
                log(f"    [{label}] [{i+1}/{N}] elapsed={time.time()-t0:.1f}s")

    n_far = np.array([r[0] for r in results], dtype=np.int64)
    cyc_far = np.array([r[1] for r in results], dtype=np.int64)
    rho_meas = np.array([r[2] for r in results], dtype=float)

    with np.errstate(invalid="ignore", divide="ignore"):
        r_far = cyc_far / n_far
    finite = np.isfinite(r_far)
    r_far_f = r_far[finite]
    mean = float(r_far_f.mean())
    sem = float(r_far_f.std(ddof=1) / np.sqrt(len(r_far_f))) if len(r_far_f) > 1 else float("nan")

    cpp = float(fm.c_double_prime(b, c, n))
    phi_U_target = float(fm.phi_U(cpp))
    dev = 100.0 * (mean / phi_U_target - 1.0)
    z = (mean - phi_U_target) / sem if sem > 0 else float("nan")

    return dict(
        n=n, b=b, c=c, N=N, threshold=threshold, seed=seed_seq,
        phi_far=mean, sem=sem, n_far_total=int(n_far.sum()),
        cyc_far_total=int(cyc_far.sum()),
        phi_U_target=phi_U_target, cpp=cpp, dev=dev, z=z,
        rho_meas=float(rho_meas.mean()), rho_formula=float(fm.rho_of(b, c, n)),
        elapsed=time.time() - t0,
    )


def t0_engine_sanity(n=65536, c=1000, ninstances=30, seed_seq=20260839000, log=print):
    """b=1 must reduce R_mask exactly to seed_mask, and rho_measured must
    match c/n. Re-check with a fresh seed before trusting b=1 measurements
    in this front (already established by short_cycle_dynamics_attempt and
    long_cycle_deficit_attempt and their referees; re-verified here per this
    lineage's convention of not silently assuming prior infra)."""
    log(f"cv_measure.py T0 -- b=1 engine sanity, n={n} c={c}, "
        f"{ninstances} instances, seed={seed_seq}")
    ss = np.random.SeedSequence(seed_seq)
    children = ss.spawn(ninstances)
    viol = 0
    rho_vals = []
    for i in range(ninstances):
        rng = np.random.default_rng(children[i])
        pi = eng.build_pi(n, rng)
        seed_mask = eng.build_seeds(n, c, rng)
        R_mask = eng.build_R_mask(n, 1, pi, seed_mask)
        if not np.array_equal(R_mask, seed_mask):
            viol += 1
        rho_vals.append(R_mask.mean())
    rho_meas = np.mean(rho_vals)
    rho_sem = np.std(rho_vals, ddof=1) / np.sqrt(len(rho_vals))
    rho_formula = c / n
    z = (rho_meas - rho_formula) / rho_sem if rho_sem > 0 else 0.0
    ok = (viol == 0) and (abs(z) < 4.0)
    log(f"  R_mask == seed_mask exactly at b=1: violations={viol}/{ninstances}  "
        f"{'OK' if viol == 0 else 'FAIL'}")
    log(f"  rho_formula (=c/n) = {rho_formula:.6f}   rho_meas = {rho_meas:.6f}+-{rho_sem:.6f}  "
        f"z={z:+.2f}  {'OK' if abs(z) < 4.0 else 'FAIL'}")
    log(f"  T0 {'PASSED' if ok else 'FAILED'}")
    return ok
