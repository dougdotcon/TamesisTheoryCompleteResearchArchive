"""M-WEIB(beta): continuum event-driven simulator for the candidate
mechanism of FINDINGS.md Sec. 2-3.

Directly simulates the INHERITED continuum exploration process (same
process described in DERIVATIONS.md Sec.0: mass s in [0,1), closure
hazard 1/(1-s) per active arc, uniform destination -> kill prob = visited
mass) but with the reroute event clock replaced by an INHOMOGENEOUS
Poisson process of rate density lambda(s) = c*beta*s**(beta-1), i.e.
cumulative mean count Lambda(t) = c*t**beta (a Weibull-shaped, "infant
mortality" decreasing-hazard point process for beta<1 -- standard object
in reliability theory, verified in SEARCH_LOG.md #2/#17).

This is a DIRECT simulation (event-driven, exact inverse-CDF sampling of
both the closure race and the reroute clock), not a discretization of the
derived formula -- it tests the derivation (FINDINGS.md eq. M-WEIB) at
the SAME level of rigor as the rest of this archive treats its inherited
continuum description (empirically controlled, not a finite-n check by
itself; see continuum_sim vs finiten_sim.py).

Single execution, seeds pre-fixed, foreground.
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


def simulate_one(c, beta, rng):
    """One realization of the continuum M-WEIB(beta) exploration of x0.
    Returns True iff x0 is cyclic."""
    s = 0.0
    A = 1  # active arcs; index 0 = x0's own arc (tracked implicitly)
    while True:
        # next closure candidate mass (exact inverse-CDF of
        # P(no closure of ANY of the A arcs in (s,t]) = ((1-t)/(1-s))**A)
        u1 = rng.random()
        s_closure = 1.0 - (1.0 - s) * (u1 ** (1.0 / A))

        # next reroute-event candidate mass via Lambda(t)=c*t**beta
        u2 = rng.random()
        target = c * (s ** beta) - math.log(u2)
        if target > c:  # would need Lambda(t)>Lambda(1)=c -> no more events by mass 1
            s_reroute = 2.0  # sentinel > 1, closure always wins
        else:
            s_reroute = (target / c) ** (1.0 / beta)

        if s_reroute < s_closure:
            # reroute event at s_reroute: kill w.p. q(s)=s (uniform destination)
            if rng.random() < s_reroute:
                return False  # killed -> x0 not cyclic (terminal)
            A += 1
            s = s_reroute
            # survives: NOT terminal, just adds a competing closure target;
            # loop continues (re-race closure vs next reroute from new s,A)
        else:
            # closure event at s_closure: ALWAYS terminal (first terminal
            # event of the whole race), uniform among the A active arcs.
            # x0 cyclic iff ITS OWN arc (index 0) is the one closed into;
            # closure into any OTHER arc also ends the whole race (x0 not
            # cyclic) -- it does NOT just remove that arc and continue.
            idx = rng.integers(0, A)
            return idx == 0


def run_cell(c, beta, n_real, seed_seq):
    rng = np.random.default_rng(seed_seq)
    hits = 0
    for _ in range(n_real):
        if simulate_one(c, beta, rng):
            hits += 1
    p = hits / n_real
    sem = math.sqrt(p * (1 - p) / n_real) if 0 < p < 1 else 1.0 / n_real
    return p, sem


def main():
    t0 = time.time()
    log = open(os.path.join(HERE, "continuum_sim.log"), "w")

    def say(msg):
        print(msg, flush=True)
        log.write(str(msg) + "\n")
        log.flush()

    say("# M-WEIB(beta) continuum event-driven simulator | started %s"
        % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))

    BETAS = [0.25, 0.5, 0.75]
    C_GRID = [2.0, 10.0, 40.0, 160.0, 640.0]
    N_REAL = 8000
    out = {"betas": BETAS, "c_grid": C_GRID, "n_real": N_REAL, "cells": {},
           "slopes": {}}

    master_seed = np.random.SeedSequence(202608221)
    spawns = master_seed.spawn(len(BETAS) * len(C_GRID))

    idx = 0
    for beta in BETAS:
        rows = []
        for c in C_GRID:
            ss = spawns[idx]
            idx += 1
            p, sem = run_cell(c, beta, N_REAL, ss)
            tgt = phi_weib_quad(c, beta)
            z = (p - tgt) / sem
            rows.append(dict(c=c, phi_mc=p, sem=sem, phi_theory=tgt, z=z))
            say("[beta=%.2f] c=%-6g phi_MC=%.6f+-%.6f  phi_theory=%.6f  z=%+.2f"
                % (beta, c, p, sem, tgt, z))
        out["cells"][str(beta)] = rows

        # tail exponent estimate: log-log slope across widest c-pair
        r_lo, r_hi = rows[1], rows[-1]  # c=10 .. c=640
        a_hat = math.log(r_lo["phi_mc"] / r_hi["phi_mc"]) / math.log(r_hi["c"] / r_lo["c"])
        sig = math.sqrt((r_lo["sem"] / r_lo["phi_mc"]) ** 2
                        + (r_hi["sem"] / r_hi["phi_mc"]) ** 2) / math.log(r_hi["c"] / r_lo["c"])
        a_target = 1.0 / (1.0 + beta)
        say("[beta=%.2f] alpha_hat (c=%g..%g) = %.4f +- %.4f   target 1/(1+beta) = %.4f   |diff|=%.4f (%.1f sigma)"
            % (beta, r_lo["c"], r_hi["c"], a_hat, sig, a_target,
               abs(a_hat - a_target), abs(a_hat - a_target) / sig if sig > 0 else float("nan")))
        out["slopes"][str(beta)] = dict(alpha_hat=a_hat, sigma=sig, alpha_target=a_target)

    say("# wall time: %.1f s" % (time.time() - t0))
    with open(os.path.join(HERE, "continuum_sim_results.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    say("# saved continuum_sim_results.json")
    log.close()


if __name__ == "__main__":
    main()
