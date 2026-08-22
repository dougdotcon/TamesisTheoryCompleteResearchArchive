"""REFEREE: arithmetic re-check of the target's claim that phi_EPS also
improves chi^2 on the THREE already-recorded validation grids, plus on the
target's own fresh grid (seeds 943).

ATTEMPT.md sec 5.2 claims:
    chi2 73.57 -> 46.59 (seeds 20260822904, aggregation_closure grid)
    chi2 79.99 -> 44.13 (seeds 20260822911, global_exclusion grid)
    chi2 81.54 -> 49.99 (seeds 720330339,  residual_attempt grid)
    chi2 121.69 -> 71.98 (seeds 20260822943, this front's own fresh grid)

Recomputed here with the referee's own high-precision formula module
(closed-form H + adaptive Gauss-Kronrod), reading ONLY the phi_mc/sem
columns out of the predecessors' recorded JSON.  Nothing from the target's
python is used.

Also reports the referee's corrected candidate phi_EPSR.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ref_formula as R                                      # noqa: E402

LINE = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))

GRIDS = [
    ("residual_attempt   (seeds 720330339)",
     os.path.join(LINE, "mclust_residual_validate_results.json")),
    ("aggregation_closure(seeds 20260822904)",
     os.path.join(LINE, "aggregation_closure_attempt",
                  "mclust_aggregation_validate_results.json")),
    ("global_exclusion   (seeds 20260822911)",
     os.path.join(LINE, "aggregation_closure_attempt", "global_exclusion_attempt",
                  "mclust_global_validate_results.json")),
    ("target fresh       (seeds 20260822943)",
     os.path.join(LINE, "aggregation_closure_attempt", "global_exclusion_attempt",
                  "x0_asymmetry_attempt", "x0_asym_validate_results.json")),
]


def main():
    summary = []
    for label, path in GRIDS:
        cells = json.load(open(path))["cells"]
        chi = {"CAND": 0.0, "EPS": 0.0, "EPSR": 0.0}
        nb = {"CAND": 0, "EPS": 0, "EPSR": 0}
        print("\n=== %s   (%d cells, %s)" % (label, len(cells), os.path.basename(path)))
        print("%6s %4s %7s %7s | %9s %9s | %-22s %-22s %-22s"
              % ("n", "b", "c", "rho", "phi_mc", "sem",
                 "CAND dev%(z)", "EPS dev%(z)", "EPSR dev%(z)"))
        for r in cells:
            n, b, c, m, s = r["n"], r["b"], r["c"], r["phi_mc"], r["sem"]
            vals = {k: fn(c, n, b) for k, fn in R.CANDIDATES.items()}
            txt = ""
            for k in ("CAND", "EPS", "EPSR"):
                v = vals[k]
                z = (m - v) / s
                chi[k] += z * z
                nb[k] += 1 if v < m else 0
                txt += " %+7.2f%% (%+5.2f)  " % (100 * (m - v) / v, z)
            print("%6d %4d %7.1f %7.4f | %9.6f %9.6f |%s" % (n, b, c, R.rho_of(c, n, b), m, s, txt))
        print("chi2: CAND=%.2f  EPS=%.2f  EPSR=%.2f   (cells where formula < MC:"
              " %d/%d, %d/%d, %d/%d)"
              % (chi["CAND"], chi["EPS"], chi["EPSR"],
                 nb["CAND"], len(cells), nb["EPS"], len(cells), nb["EPSR"], len(cells)))
        summary.append((label, len(cells), chi["CAND"], chi["EPS"], chi["EPSR"]))

    print("\n\n=== SUMMARY (referee recomputation) ===")
    print("%-42s %5s %10s %10s %10s" % ("grid", "cells", "chi2 CAND", "chi2 EPS", "chi2 EPSR"))
    for label, nc, a, b_, c_ in summary:
        print("%-42s %5d %10.2f %10.2f %10.2f" % (label, nc, a, b_, c_))
    print("\nTarget's claimed numbers, for comparison:")
    print("  residual_attempt    81.54 -> 49.99")
    print("  aggregation_closure 73.57 -> 46.59")
    print("  global_exclusion    79.99 -> 44.13")
    print("  fresh (943)        121.69 -> 71.98")


if __name__ == "__main__":
    main()
