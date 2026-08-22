"""DISC-DEC-018 front (b) -- U-ALPHA-MCLUST-RIGOR.

Independent driver (own implementation, NOT copied from ualpha_sim.py --
the M-CLUST(b) mechanism definition was read from ualpha_sim.py and
DERIVATIONS.md sec 3.5 and reproduced here from that description, with
its own RNG calls, own seeds, own cyclic-detection code path) that
validates the CORRECTED finite-n formula for M-CLUST(b) derived in
DERIVATION_MCLUST_FIXED.md against:
  (a) the OLD published heuristic  phi_U(c_eff),  c_eff = c(1-c/n)^b
  (b) the NEW corrected formula    phi_NEW(c,n,b)  (this front)
  (c) direct Monte Carlo simulation of the actual finite-n mechanism.

Single execution, seeds pre-fixed below, foreground, bounded runtime
(target <= 5 min).
"""
import json
import math
import os
import time

import numpy as np
from scipy import integrate

HERE = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------- formulas
def phi_U(c):
    """phi_U(c) = int_0^1 exp(-c t^2) dt  (M-U closed-form target)."""
    v, _ = integrate.quad(lambda t: math.exp(-c * t * t), 0, 1)
    return v


def rho_of(c, n, b):
    """rho = |R|/n = 1 - (1-c/n)^b  (exact, derived in DERIVATION_MCLUST_FIXED.md sec 1)."""
    return 1.0 - (1.0 - c / n) ** b


def phi_OLD(c, n, b):
    """Published heuristic (RESULTS_SUMMARY.md / DERIVATIONS.md sec 3.5):
    rate depressed to c_eff = c(1-c/n)^b, kill prob unmodified (=t^2 baseline)."""
    c_eff = c * (1.0 - c / n) ** b
    return phi_U(c_eff)


def H_NEW(t, rho):
    """Corrected crowding/kill integrand (DERIVATION_MCLUST_FIXED.md sec 3-4):
    rate STAYS c (walk-conditional encounter rate is c/n unmodified -- the
    (1-c/n)^b factor in c_eff was mis-derived, see sec 2); kill probability
    is amplified by the chain-kill + R-depletion mechanism to
    q_CLUST(s) = s/(1-rho), giving
    H(t) = t - (1-t)*(t + rho*ln(1-t))/(1-rho)."""
    if rho < 1e-12:
        return t * t
    if t < 1e-13:
        return 0.0
    return t - (1.0 - t) * (t + rho * math.log(1.0 - t)) / (1.0 - rho)


def phi_NEW(c, n, b):
    rho = rho_of(c, n, b)
    v, _ = integrate.quad(lambda t: math.exp(-c * H_NEW(t, rho)), 0, 1, limit=200)
    return v


# ------------------------------------------------------------- mechanism
def build_f_clust(n, b, c, rng):
    """M-CLUST(b): seeds marked i.i.d. Bernoulli(c/n); each seed's block =
    {seed, pi(seed), ..., pi^(b-1)(seed)} (own reading of ualpha_sim.py's
    M-CLUST8 construction, generalized to arbitrary b, own implementation)."""
    pi = rng.permutation(n).astype(np.int64)
    in_R = rng.random(n) < c / n
    cur = np.flatnonzero(in_R)
    for _ in range(b - 1):
        cur = pi[cur]
        in_R[cur] = True
    R = np.flatnonzero(in_R)
    f = pi.copy()
    if R.size:
        f[R] = rng.integers(0, n, R.size)
    return f, R.size


def cyclic_fraction(f, n, log2n):
    """#cyclic points of f / n via distinct image of f^(2^log2n), 2^log2n >= 2n."""
    F = f
    for _ in range(log2n):
        F = F[F]
    mask = np.zeros(n, dtype=bool)
    mask[F] = True
    return mask.sum() / n


def run_cell(n, b, c, n_rep, seed_seq, log2n):
    rng = np.random.default_rng(seed_seq)
    vals = np.empty(n_rep)
    rsizes = np.empty(n_rep)
    for i in range(n_rep):
        f, rsize = build_f_clust(n, b, c, rng)
        vals[i] = cyclic_fraction(f, n, log2n)
        rsizes[i] = rsize
    m = vals.mean()
    sem = vals.std(ddof=1) / math.sqrt(n_rep)
    return m, sem, rsizes.mean() / n


# -------------------------------------------------------------------- main
def main():
    t0 = time.time()
    log = open(os.path.join(HERE, "mclust_validate.log"), "w")

    def say(msg):
        print(msg, flush=True)
        log.write(msg + "\n")
        log.flush()

    say("# mclust_rigor validation | started %s"
        % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))

    # cells: (n, b, c, N_rep, log2n)
    # b=8 CONTROL (matches wave-3 validated regime: correction should be
    # tiny here, old and new should both track MC well).
    # b=50 STRESS (matches adversarial's headline finding, reproduced with
    # OWN seeds/n here rather than copied numbers).
    # b=100, b=200: beyond anything previously tested, per task mandate.
    cells = []
    for c in [10.0, 40.0, 160.0]:
        cells.append((32768, 8, c, 3000))
    for c in [10.0, 50.0, 150.0, 400.0]:
        cells.append((65536, 50, c, 4000))
    for c in [10.0, 50.0, 150.0, 400.0]:
        cells.append((65536, 100, c, 4000))
    for c in [5.0, 20.0, 60.0, 150.0]:
        cells.append((65536, 200, c, 4000))

    seed_root = np.random.SeedSequence(20260822018)  # DISC-DEC-018
    spawns = seed_root.spawn(len(cells))

    out = {"cells": []}
    for (n, b, c, n_rep), ss in zip(cells, spawns):
        log2n = int(math.ceil(math.log2(n))) + 1  # 2^log2n >= 2n margin
        m, sem, rho_meas = run_cell(n, b, c, n_rep, ss, log2n)
        rho_formula = rho_of(c, n, b)
        old = phi_OLD(c, n, b)
        new = phi_NEW(c, n, b)
        z_old = (m - old) / sem
        z_new = (m - new) / sem
        dev_old = (m - old) / old * 100
        dev_new = (m - new) / new * 100
        row = dict(n=n, b=b, c=c, n_rep=n_rep, phi_mc=m, sem=sem,
                   rho_formula=rho_formula, rho_measured=rho_meas,
                   phi_old=old, phi_new=new, z_old=z_old, z_new=z_new,
                   dev_old_pct=dev_old, dev_new_pct=dev_new)
        out["cells"].append(row)
        say("n=%6d b=%3d c=%7.1f rho=%.4f | MC=%.6f+-%.6f | "
            "OLD=%.6f (z=%+7.2f, dev=%+7.2f%%) | "
            "NEW=%.6f (z=%+7.2f, dev=%+7.2f%%)"
            % (n, b, c, rho_formula, m, sem, old, z_old, dev_old,
               new, z_new, dev_new))

    say("# wall time: %.1f s" % (time.time() - t0))
    with open(os.path.join(HERE, "mclust_validate_results.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    say("# saved mclust_validate_results.json")
    log.close()


if __name__ == "__main__":
    main()
