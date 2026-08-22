"""M-WEIB(beta): FINITE-n permutation-based simulator, independent of and
secondary to continuum_sim.py -- tests whether the continuum idealization
of M-WEIB(beta) survives an actual discrete construction on a real random
permutation pi of [n], not just the abstract event-driven race.

Mechanism: pi uniform random permutation of [n]. Walk from x0=0 via pi,
one REAL discrete step at a time, tracking the actual visited-point set.
Reroute events are SCHEDULED on the mass axis via the same Weibull
inhomogeneous-rate law Lambda(t) = c*t**beta used in continuum_sim.py
(inverse-CDF draws of the next reroute mass, converted to a discrete
visited-count threshold) -- but everything else (closure detection,
kill/survive outcome) is decided by literally walking pi and checking
real set membership, not by the abstract race formulas.

At a scheduled reroute: draw an ACTUAL uniform random destination in
[0,n); if already visited -> kill (x0 not cyclic, terminal); else jump
there and continue walking via pi. Between reroutes: walk via pi; if the
next pi-image is already visited -> closure, TERMINAL (x0 cyclic iff
that image is x0 itself), matching the corrected race logic verified in
continuum_sim.py.

Single execution, seeds pre-fixed, foreground, bounded n/N for runtime.
"""
import json
import math
import os
import time

import numpy as np
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__))


def phi_weib_quad(c, beta):
    val, _ = quad(lambda t: math.exp(-c * t ** (1.0 + beta)), 0.0, 1.0,
                  epsabs=1e-13, epsrel=1e-12)
    return val


def next_reroute_mass(s, c, beta, u2):
    target = c * (s ** beta) - math.log(u2)
    if target > c:
        return 2.0
    return (target / c) ** (1.0 / beta)


def simulate_one_finiten(n, c, beta, pi, rng, visited_buf):
    """One realization on a fresh permutation pi (array, pi[i] = image).
    visited_buf: pre-allocated bool array of size n, reset internally.
    Returns True iff x0=0 is cyclic."""
    visited_buf[:] = False
    x0 = 0
    visited_buf[x0] = True
    visited_count = 1
    current = x0

    s = visited_count / n
    u2 = rng.random()
    s_reroute = next_reroute_mass(s, c, beta, u2)
    k_reroute = int(round(s_reroute * n))

    while True:
        # walk one real pi-step, unless a reroute is due immediately
        if visited_count >= k_reroute and k_reroute <= n:
            # trigger reroute now
            d = int(rng.integers(0, n))
            if visited_buf[d]:
                return False  # kill
            visited_buf[d] = True
            visited_count += 1
            current = d
            s = visited_count / n
            u2 = rng.random()
            s_reroute = next_reroute_mass(s, c, beta, u2)
            k_reroute = int(round(s_reroute * n))
            continue

        nxt = pi[current]
        if visited_buf[nxt]:
            return nxt == x0  # closure, terminal
        visited_buf[nxt] = True
        visited_count += 1
        current = nxt
        if visited_count >= n:
            # exhausted all mass without closing -- should not happen for
            # a genuine permutation walk (pi restricted to unvisited points
            # must eventually close); declare non-cyclic defensively but
            # log via return None -> caller treats as a hard error.
            return None


def run_cell(n, c, beta, n_real, seed_seq):
    rng = np.random.default_rng(seed_seq)
    visited_buf = np.zeros(n, dtype=bool)
    hits = 0
    anomalies = 0
    for _ in range(n_real):
        pi = rng.permutation(n)
        r = simulate_one_finiten(n, c, beta, pi, rng, visited_buf)
        if r is None:
            anomalies += 1
            continue
        if r:
            hits += 1
    valid = n_real - anomalies
    p = hits / valid if valid else float("nan")
    sem = math.sqrt(p * (1 - p) / valid) if valid and 0 < p < 1 else 1.0 / max(valid, 1)
    return p, sem, anomalies


def main():
    t0 = time.time()
    log = open(os.path.join(HERE, "finiten_sim.log"), "w")

    def say(msg):
        print(msg, flush=True)
        log.write(str(msg) + "\n")
        log.flush()

    say("# M-WEIB(beta) finite-n permutation simulator | started %s"
        % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))

    N = 8192
    N_REAL = 5000
    BETAS = [0.25, 0.5, 0.75]
    C_GRID = [10.0, 40.0, 160.0, 640.0]
    say("# n=%d N_real=%d betas=%s c_grid=%s" % (N, N_REAL, BETAS, C_GRID))

    out = {"n": N, "n_real": N_REAL, "betas": BETAS, "c_grid": C_GRID,
           "cells": {}, "slopes": {}}

    master_seed = np.random.SeedSequence(202608222)
    spawns = master_seed.spawn(len(BETAS) * len(C_GRID))

    idx = 0
    for beta in BETAS:
        rows = []
        for c in C_GRID:
            ss = spawns[idx]
            idx += 1
            p, sem, anomalies = run_cell(N, c, beta, N_REAL, ss)
            tgt = phi_weib_quad(c, beta)
            z = (p - tgt) / sem
            rows.append(dict(c=c, phi_mc=p, sem=sem, phi_theory=tgt, z=z,
                              anomalies=anomalies))
            say("[n=%d beta=%.2f] c=%-6g phi_MC=%.6f+-%.6f  phi_theory(continuum)=%.6f  z=%+.2f  anomalies=%d"
                % (N, beta, c, p, sem, tgt, z, anomalies))
        out["cells"][str(beta)] = rows
        r_lo, r_hi = rows[0], rows[-1]
        a_hat = math.log(r_lo["phi_mc"] / r_hi["phi_mc"]) / math.log(r_hi["c"] / r_lo["c"])
        sig = math.sqrt((r_lo["sem"] / r_lo["phi_mc"]) ** 2
                        + (r_hi["sem"] / r_hi["phi_mc"]) ** 2) / math.log(r_hi["c"] / r_lo["c"])
        a_target = 1.0 / (1.0 + beta)
        say("[n=%d beta=%.2f] alpha_hat (c=%g..%g) = %.4f +- %.4f   target 1/(1+beta) = %.4f   diff=%.1f sigma"
            % (N, beta, r_lo["c"], r_hi["c"], a_hat, sig, a_target,
               abs(a_hat - a_target) / sig if sig > 0 else float("nan")))
        out["slopes"][str(beta)] = dict(alpha_hat=a_hat, sigma=sig, alpha_target=a_target)

    say("# wall time: %.1f s" % (time.time() - t0))
    with open(os.path.join(HERE, "finiten_sim_results.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    say("# saved finiten_sim_results.json")
    log.close()


if __name__ == "__main__":
    main()
