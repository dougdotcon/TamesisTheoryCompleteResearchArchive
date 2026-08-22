"""residual_attempt -- stage F (DISC-DEC-033): FRESH validation.

Independent driver (own implementation, own RNG calls, NOT importing
ualpha_sim.py, mclust_validate.py, or mclust_walk_diagnostic.py) that
validates the candidate closed-ish-form correction phi_CAND derived in
ATTEMPT.md secs 3-7 against a FRESH Monte Carlo simulation of the exact
M-CLUST(b) mechanism (DERIVATION_MCLUST_FIXED.md sec 1), using seeds
that were NOT used anywhere else in this front (not wave 4's
SeedSequence(20260822018), not this front's own diagnostic
SeedSequence(918302033)).

phi_CAND(c,n,b) = (1-rho) * phi_V4(c,n,b)

  rho = 1-(1-c/n)^b                                          [exact]
  phi_V4 = numeric integral using q_CLUST(s)=s/(1-rho) [wave 4, sec 3,
    independently re-validated in mclust_walk_diagnostic.py] combined
    with a MULTIPLICATIVELY elevated closure hazard 1/[(1-rho)(1-s)]
    (ATTEMPT.md sec 6, motivated by both a conditioned-probability
    argument and the empirical H_true(t) extraction)
  (1-rho) prefactor: dilution for the fact that a uniformly random x0
    has probability rho of itself starting INSIDE R -- overwhelmingly
    (fraction ~(b-1)/b of rho) as a SHADOWED interior block member,
    which (by the same shadowing lemma DERIVATION_MCLUST_FIXED.md sec 1
    already used) can essentially NEVER be closed into via normal
    pi-stepping, only via a rare direct chain-jump landing exactly on
    it (estimated O(c*rho/((1-rho)n)) <= ~0.6% at the most extreme
    grid point -- negligible), hence phi(x0 shadowed) ~= 0 to good
    approximation. The base master formula (DERIVATIONS.md sec 1,
    "nao alterada" per wave 4 sec 4) implicitly assumes x0 starts
    OUTSIDE R (its very first step is normal pi-stepping) -- true
    automatically for every mechanism tested before M-CLUST (rho was
    always O(c/n) there) but not for M-CLUST at large b, where rho can
    be O(1). ATTEMPT.md sec 7 is explicit that this decomposition is
    NOT presented as a fully closed first-principles proof -- see the
    honesty section there for exactly what remains heuristic.

Grid: reproduces wave 4's own 15-cell grid (for direct before/after
comparison) PLUS 3 new cells pushing to larger b*c/n than anything
tested before (b=300, and b=100/c=600 at rho up to ~0.6), to stress-test
whether phi_CAND holds up OUTSIDE the range it was motivated from.
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


def phi_OLD(c, n, b):
    c_eff = c * (1.0 - c / n) ** b
    return phi_U(c_eff)


def phi_NEW(c, n, b):
    rho = rho_of(c, n, b)
    v, _ = integrate.quad(lambda t: math.exp(-c * H_NEW(t, rho)), 0, 1, limit=200)
    return v


def q_clust(s, rho):
    return s / (1.0 - rho) if rho > 1e-12 else s


def H_v4(t, rho, n_steps=400):
    if rho < 1e-12:
        return t * t
    if t < 1e-13:
        return 0.0
    p = 1.0 / (1.0 - rho)
    s_grid = np.linspace(0.0, t, n_steps + 1)
    integrand = (1.0 - q_clust(s_grid, rho)) * np.power(np.clip(1.0 - s_grid, 1e-15, None), -p)
    trapz = getattr(np, "trapezoid", None) or np.trapz
    inner = trapz(integrand, s_grid)
    return t - ((1.0 - t) ** p) * inner


def phi_V4(c, n, b, n_outer=400, n_inner=250):
    rho = rho_of(c, n, b)
    if rho < 1e-9:
        return phi_U(c)
    p = 1.0 / (1.0 - rho)
    t_grid = np.linspace(0.0, 1.0 - 1e-7, n_outer + 1)
    H_vals = np.array([H_v4(t, rho, n_inner) for t in t_grid])
    ES = np.power(np.clip(1.0 - t_grid, 1e-15, None), p) * np.exp(-c * H_vals)
    integrand_phi = ES / ((1.0 - rho) * np.clip(1.0 - t_grid, 1e-15, None))
    trapz = getattr(np, "trapezoid", None) or np.trapz
    return trapz(integrand_phi, t_grid)


def phi_CAND(c, n, b):
    rho = rho_of(c, n, b)
    return (1.0 - rho) * phi_V4(c, n, b)


# ------------------------------------------------------------- mechanism
def build_f_clust(n, b, c, rng):
    """Own implementation, independent of mclust_validate.py / ualpha_sim.py
    (re-read from DERIVATION_MCLUST_FIXED.md sec 1 as instructed)."""
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
    log = open(os.path.join(HERE, "mclust_residual_validate.log"), "w")

    def say(msg):
        print(msg, flush=True)
        log.write(msg + "\n")
        log.flush()

    say("# mclust_residual FRESH validation | started %s"
        % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))

    cells = []
    for c in [10.0, 40.0, 160.0]:
        cells.append((32768, 8, c, 3000))
    for c in [10.0, 50.0, 150.0, 400.0]:
        cells.append((65536, 50, c, 4000))
    for c in [10.0, 50.0, 150.0, 400.0]:
        cells.append((65536, 100, c, 4000))
    for c in [5.0, 20.0, 60.0, 150.0]:
        cells.append((65536, 200, c, 4000))
    # NEW: push beyond anything tested before (larger b, and larger rho)
    cells.append((65536, 300, 150.0, 4000))   # bc/n ~ 0.687
    cells.append((65536, 100, 600.0, 4000))   # rho ~ 0.63, bc/n ~ 0.916
    cells.append((65536, 400, 100.0, 4000))   # bc/n ~ 0.61, different b/c mix

    # Fresh seed, distinct from wave 4's SeedSequence(20260822018) and
    # from this front's own diagnostic SeedSequence(918302033).
    seed_root = np.random.SeedSequence(720330339)  # DISC-DEC-033, fresh validation
    spawns = seed_root.spawn(len(cells))

    out = {"cells": []}
    for (n, b, c, n_rep), ss in zip(cells, spawns):
        log2n = int(math.ceil(math.log2(n))) + 1
        m, sem = run_cell(n, b, c, n_rep, ss, log2n)
        rho = rho_of(c, n, b)
        old = phi_OLD(c, n, b)
        new = phi_NEW(c, n, b)
        cand = phi_CAND(c, n, b)
        z_old = (m - old) / sem
        z_new = (m - new) / sem
        z_cand = (m - cand) / sem
        dev_old = (m - old) / old * 100
        dev_new = (m - new) / new * 100
        dev_cand = (m - cand) / cand * 100
        row = dict(n=n, b=b, c=c, n_rep=n_rep, bcn=b * c / n, phi_mc=m, sem=sem,
                   rho=rho, phi_old=old, phi_new=new, phi_cand=cand,
                   z_old=z_old, z_new=z_new, z_cand=z_cand,
                   dev_old_pct=dev_old, dev_new_pct=dev_new, dev_cand_pct=dev_cand)
        out["cells"].append(row)
        say("n=%6d b=%3d c=%6.1f rho=%.4f bc/n=%.4f | MC=%.6f+-%.6f | "
            "OLD dev=%+7.2f%% (z=%+6.2f) | NEW dev=%+7.2f%% (z=%+6.2f) | "
            "CAND dev=%+7.2f%% (z=%+6.2f)"
            % (n, b, c, rho, b * c / n, m, sem, dev_old, z_old, dev_new, z_new,
               dev_cand, z_cand))

    chi2_new = sum(r["z_new"] ** 2 for r in out["cells"])
    chi2_cand = sum(r["z_cand"] ** 2 for r in out["cells"])
    say("\n# chi2 (NEW, %d cells): %.2f" % (len(out["cells"]), chi2_new))
    say("# chi2 (CAND, %d cells): %.2f" % (len(out["cells"]), chi2_cand))
    say("# wall time: %.1f s" % (time.time() - t0))
    with open(os.path.join(HERE, "mclust_residual_validate_results.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    say("# saved mclust_residual_validate_results.json")
    log.close()


if __name__ == "__main__":
    main()
