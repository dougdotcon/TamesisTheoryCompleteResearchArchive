"""Two supplementary, single-execution checks referenced in FINDINGS.md:

  (S1) Finite-n bias TREND for M-WEIB(beta=0.25): re-run the finite-n
       permutation simulator at n=32768 (matching the archive's own
       standard resolution, see ../ualpha_sim.py) and compare the
       tail-slope discrepancy against the n=8192 result already saved in
       finiten_sim_results.json -- tests whether the bias seen there is a
       genuine finite-n effect (shrinks as n grows) or a structural
       failure (would not shrink).

  (S2) beta>1 ("wear-out" hazard) corollary: the SAME M-WEIB(beta)
       continuum mechanism with beta>1 is predicted (FINDINGS.md Sec. 2)
       to give alpha=1/(1+beta) < 1/2, i.e. it should BREAK the alpha>=1/2
       floor that DERIVATIONS.md proves for the constant-rate M-q family
       -- because M-WEIB is definitionally outside M-q (rate is not
       constant). Spot-checked at beta=2,3 against the continuum
       event-driven simulator (already unit-tested against the known-
       correct M-U formula at beta=1 in continuum_sim.py).

Single execution, seeds pre-fixed, foreground.
"""
import json
import math
import os
import time

import numpy as np

from continuum_sim import simulate_one, phi_weib_quad
from finiten_sim import run_cell, phi_weib_quad as phi_weib_quad_fn

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    t0 = time.time()
    log = open(os.path.join(HERE, "supplementary_checks.log"), "w")

    def say(msg):
        print(msg, flush=True)
        log.write(str(msg) + "\n")
        log.flush()

    say("# supplementary checks | started %s"
        % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    out = {}

    # ---------------- S1: finite-n bias trend, beta=0.25, n=8192 -> 32768 ----------------
    say("\n=== S1: finite-n bias trend (beta=0.25), n=8192 vs n=32768 ===")
    beta = 0.25
    C_GRID = [10.0, 40.0, 160.0, 640.0]
    s1 = {"beta": beta, "c_grid": C_GRID, "n_values": {}}
    seed_base = np.random.SeedSequence(2026082230)
    for n, n_real, tag in [(8192, 5000, "n8192(=finiten_sim.py, already saved)"),
                            (32768, 3000, "n32768(new, this script)")]:
        if n == 8192:
            with open(os.path.join(HERE, "finiten_sim_results.json")) as fh:
                prior = json.load(fh)
            rows = prior["cells"][str(beta)]
            slope = prior["slopes"][str(beta)]
            say("[reused from finiten_sim_results.json] n=%d: alpha_hat=%.4f +- %.4f  (target %.4f)"
                % (n, slope["alpha_hat"], slope["sigma"], slope["alpha_target"]))
            s1["n_values"][str(n)] = dict(rows=rows, slope=slope, source="finiten_sim_results.json")
            continue
        spawns = seed_base.spawn(len(C_GRID))
        rows = []
        for ci, c in enumerate(C_GRID):
            p, sem, an = run_cell(n, c, beta, n_real, spawns[ci])
            tgt = phi_weib_quad_fn(c, beta)
            z = (p - tgt) / sem
            rows.append(dict(c=c, phi_mc=p, sem=sem, phi_theory=tgt, z=z, anomalies=an))
            say("[n=%d beta=%.2f] c=%-6g phi_MC=%.6f+-%.6f theory=%.6f z=%+.2f anomalies=%d"
                % (n, beta, c, p, sem, tgt, z, an))
        r_lo, r_hi = rows[0], rows[-1]
        a_hat = math.log(r_lo["phi_mc"] / r_hi["phi_mc"]) / math.log(r_hi["c"] / r_lo["c"])
        sig = math.sqrt((r_lo["sem"] / r_lo["phi_mc"]) ** 2
                        + (r_hi["sem"] / r_hi["phi_mc"]) ** 2) / math.log(r_hi["c"] / r_lo["c"])
        a_target = 1.0 / (1.0 + beta)
        say("[n=%d beta=%.2f] alpha_hat=%.4f +- %.4f  target=%.4f  diff=%.1f sigma"
            % (n, beta, a_hat, sig, a_target, abs(a_hat - a_target) / sig))
        s1["n_values"][str(n)] = dict(rows=rows,
                                       slope=dict(alpha_hat=a_hat, sigma=sig, alpha_target=a_target),
                                       source="this script")
    out["S1_finiten_bias_trend"] = s1

    # ---------------- S2: beta>1 corollary (breaks the alpha>=1/2 floor) ----------------
    say("\n=== S2: beta>1 corollary (wear-out hazard; predicted to break floor alpha>=1/2) ===")
    s2 = {}
    for beta in [2.0, 3.0]:
        rng = np.random.default_rng(np.random.SeedSequence([2026082231, int(beta * 10)]))
        rows = []
        for c in [10.0, 640.0]:
            n_real = 8000
            hits = sum(simulate_one(c, beta, rng) for _ in range(n_real))
            p = hits / n_real
            sem = math.sqrt(p * (1 - p) / n_real)
            tgt = phi_weib_quad(c, beta)
            z = (p - tgt) / sem
            rows.append(dict(c=c, phi_mc=p, sem=sem, phi_theory=tgt, z=z))
            say("[continuum beta=%.1f] c=%-6g phi_MC=%.6f+-%.6f theory=%.6f z=%+.2f"
                % (beta, c, p, sem, tgt, z))
        a_hat = math.log(rows[0]["phi_mc"] / rows[1]["phi_mc"]) / math.log(rows[1]["c"] / rows[0]["c"])
        a_target = 1.0 / (1.0 + beta)
        say("[continuum beta=%.1f] alpha_hat=%.4f  target=%.4f  (floor 1/2 broken: %s)"
            % (beta, a_hat, a_target, a_hat < 0.5))
        s2[str(beta)] = dict(rows=rows, alpha_hat=a_hat, alpha_target=a_target,
                              floor_broken=bool(a_hat < 0.5))
    out["S2_beta_gt1_corollary"] = s2

    say("\n# wall time: %.1f s" % (time.time() - t0))
    with open(os.path.join(HERE, "supplementary_checks_results.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    say("# saved supplementary_checks_results.json")
    log.close()


if __name__ == "__main__":
    main()
