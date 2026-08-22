"""aggregation_closure_attempt -- stage 3: FRESH full-formula validation.

Independent driver (own implementation; does not import mclust_validate.py,
mclust_walk_diagnostic.py, mclust_residual_validate.py, or
mclust_residual_v5.py's formula code is re-typed here too, not imported --
so this script's correctness does not depend on any earlier file in this
tree) comparing phi_NEW (wave 4), phi_CAND (residual_attempt, the
(1-rho)*phi_V4 candidate with P=1/(1-rho)) and phi_CAND5 (this front, the
(1-rho)*phi_V5 candidate with the DERIVED exact P=(1-c/n)^-(b-1)) against
a FRESH Monte Carlo simulation of the exact M-CLUST(b) mechanism.

Seeds: SeedSequence(20260822904) -- NOT wave 4's SeedSequence(20260822018),
NOT residual_attempt's SeedSequence(918302033) or SeedSequence(720330339),
NOT any seed used elsewhere in aggregation_closure_attempt/.

Grid: reproduces residual_attempt's own 18-cell grid (direct before/after
comparison against its own final validation) plus reuses that same range --
no attempt to push further into more extreme bc/n territory than
residual_attempt already tested, since the question here is specifically
whether phi_CAND5 improves on phi_CAND over the SAME range, not whether the
formula extrapolates further.
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
    v, _ = integrate.quad(lambda t: math.exp(-c * t * t), 0, 1)
    return v


def rho_of(c, n, b):
    return 1.0 - (1.0 - c / n) ** b


def H_NEW(t, rho):
    if rho < 1e-12:
        return t * t
    if t < 1e-13:
        return 0.0
    return t - (1.0 - t) * (t + rho * math.log(1.0 - t)) / (1.0 - rho)


def phi_NEW(c, n, b):
    rho = rho_of(c, n, b)
    v, _ = integrate.quad(lambda t: math.exp(-c * H_NEW(t, rho)), 0, 1, limit=200)
    return v


def q_clust(s, rho):
    return s / (1.0 - rho) if rho > 1e-12 else s


def H_generic(t, rho, P, n_steps=400):
    if rho < 1e-12:
        return t * t
    if t < 1e-13:
        return 0.0
    s_grid = np.linspace(0.0, t, n_steps + 1)
    integrand = (1.0 - q_clust(s_grid, rho)) * np.power(np.clip(1.0 - s_grid, 1e-15, None), -P)
    trapz = getattr(np, "trapezoid", None) or np.trapz
    inner = trapz(integrand, s_grid)
    return t - ((1.0 - t) ** P) * inner


def phi_generic(c, n, b, P, n_outer=400, n_inner=250):
    rho = rho_of(c, n, b)
    if rho < 1e-9:
        return phi_U(c)
    t_grid = np.linspace(0.0, 1.0 - 1e-7, n_outer + 1)
    H_vals = np.array([H_generic(t, rho, P, n_inner) for t in t_grid])
    ES = np.power(np.clip(1.0 - t_grid, 1e-15, None), P) * np.exp(-c * H_vals)
    integrand_phi = ES * P / np.clip(1.0 - t_grid, 1e-15, None)
    trapz = getattr(np, "trapezoid", None) or np.trapz
    return trapz(integrand_phi, t_grid)


def phi_CAND(c, n, b):
    rho = rho_of(c, n, b)
    if rho < 1e-9:
        return phi_U(c)
    return (1.0 - rho) * phi_generic(c, n, b, 1.0 / (1.0 - rho))


def phi_CAND5(c, n, b):
    rho = rho_of(c, n, b)
    if rho < 1e-9:
        return phi_U(c)
    P = (1.0 - c / n) ** (-(b - 1))
    return (1.0 - rho) * phi_generic(c, n, b, P)


# ------------------------------------------------------------- mechanism
def build_f_clust(n, b, c, rng):
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
    return f


def cyclic_fraction(f, n, log2n):
    F = f
    for _ in range(log2n):
        F = F[F]
    mask = np.zeros(n, dtype=bool)
    mask[F] = True
    return mask.sum() / n


def run_cell(n, b, c, n_rep, seed_seq, log2n):
    rng = np.random.default_rng(seed_seq)
    vals = np.empty(n_rep)
    for i in range(n_rep):
        f = build_f_clust(n, b, c, rng)
        vals[i] = cyclic_fraction(f, n, log2n)
    m = vals.mean()
    sem = vals.std(ddof=1) / math.sqrt(n_rep)
    return m, sem


def main():
    t0 = time.time()
    log = open(os.path.join(HERE, "mclust_aggregation_validate.log"), "w")

    def say(msg):
        print(msg, flush=True)
        log.write(msg + "\n")
        log.flush()

    say("# mclust_aggregation FRESH validation | started %s"
        % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    say("# own implementation, SeedSequence(20260822904), fresh (not reused)")

    cells = []
    for c in [10.0, 40.0, 160.0]:
        cells.append((32768, 8, c, 3000))
    for c in [10.0, 50.0, 150.0, 400.0]:
        cells.append((65536, 50, c, 4000))
    for c in [10.0, 50.0, 150.0, 400.0]:
        cells.append((65536, 100, c, 4000))
    for c in [5.0, 20.0, 60.0, 150.0]:
        cells.append((65536, 200, c, 4000))
    cells.append((65536, 300, 150.0, 4000))
    cells.append((65536, 100, 600.0, 4000))
    cells.append((65536, 400, 100.0, 4000))

    seed_root = np.random.SeedSequence(20260822904)
    spawns = seed_root.spawn(len(cells))

    out = {"cells": []}
    for (n, b, c, n_rep), ss in zip(cells, spawns):
        log2n = int(math.ceil(math.log2(n))) + 1
        m, sem = run_cell(n, b, c, n_rep, ss, log2n)
        rho = rho_of(c, n, b)
        new = phi_NEW(c, n, b)
        cand = phi_CAND(c, n, b)
        cand5 = phi_CAND5(c, n, b)
        z_new = (m - new) / sem
        z_cand = (m - cand) / sem
        z_cand5 = (m - cand5) / sem
        dev_new = (m - new) / new * 100
        dev_cand = (m - cand) / cand * 100
        dev_cand5 = (m - cand5) / cand5 * 100
        row = dict(n=n, b=b, c=c, n_rep=n_rep, bcn=b * c / n, phi_mc=m, sem=sem,
                   rho=rho, phi_new=new, phi_cand=cand, phi_cand5=cand5,
                   z_new=z_new, z_cand=z_cand, z_cand5=z_cand5,
                   dev_new_pct=dev_new, dev_cand_pct=dev_cand, dev_cand5_pct=dev_cand5)
        out["cells"].append(row)
        say("n=%6d b=%3d c=%6.1f rho=%.4f bc/n=%.4f | MC=%.6f+-%.6f | "
            "NEW dev=%+7.2f%% (z=%+6.2f) | CAND dev=%+7.2f%% (z=%+6.2f) | "
            "CAND5 dev=%+7.2f%% (z=%+6.2f)"
            % (n, b, c, rho, b * c / n, m, sem, dev_new, z_new,
               dev_cand, z_cand, dev_cand5, z_cand5))

    chi2_new = sum(r["z_new"] ** 2 for r in out["cells"])
    chi2_cand = sum(r["z_cand"] ** 2 for r in out["cells"])
    chi2_cand5 = sum(r["z_cand5"] ** 2 for r in out["cells"])
    say("\n# chi2 (NEW, %d cells): %.2f" % (len(out["cells"]), chi2_new))
    say("# chi2 (CAND, %d cells): %.2f" % (len(out["cells"]), chi2_cand))
    say("# chi2 (CAND5, %d cells): %.2f" % (len(out["cells"]), chi2_cand5))
    say("# wall time: %.1f s" % (time.time() - t0))
    with open(os.path.join(HERE, "mclust_aggregation_validate_results.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    say("# saved mclust_aggregation_validate_results.json")
    log.close()


if __name__ == "__main__":
    main()
