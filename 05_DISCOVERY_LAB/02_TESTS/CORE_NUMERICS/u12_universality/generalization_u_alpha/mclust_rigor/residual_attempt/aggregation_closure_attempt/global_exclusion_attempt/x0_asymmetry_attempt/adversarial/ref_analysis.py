"""REFEREE: analysis of the referee's own Monte-Carlo runs.

Sections
  (1) simulator cross-validation against phi_mc already recorded by TWO
      earlier, unrelated documents of this lineage (mandatory before the new
      measurement is trusted), plus the two other recorded grids.
  (2) eps = P(cyclic | x0 in R): referee measurement vs. the target's
      stage-B measurement, and vs. zero.
  (3) the two channels of eps, measured, against the target's leading-order
      derivation and against the referee's corrected one.
  (4) phi_CAND vs phi_EPS vs phi_EPSR on the referee's own FRESH grid.
  (5) the decisive substitution: phi_CAND + rho * eps_MEASURED.
  (6) seed-to-seed robustness of the chi^2 improvement.
"""
import glob
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ref_formula as R                                        # noqa: E402

LINE = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
RECORDED = {
    "residual(720330339)": os.path.join(LINE, "mclust_residual_validate_results.json"),
    "aggreg(20260822904)": os.path.join(LINE, "aggregation_closure_attempt",
                                        "mclust_aggregation_validate_results.json"),
    "global(20260822911)": os.path.join(LINE, "aggregation_closure_attempt",
                                        "global_exclusion_attempt",
                                        "mclust_global_validate_results.json"),
    "target(20260822943)": os.path.join(LINE, "aggregation_closure_attempt",
                                        "global_exclusion_attempt",
                                        "x0_asymmetry_attempt",
                                        "x0_asym_validate_results.json"),
}


def load(tag):
    out = {}
    for fn in sorted(glob.glob(os.path.join(HERE, "ref_mc_%s_*.json" % tag))):
        for r in json.load(open(fn))["cells"]:
            out[(r["n"], r["b"], r["c"])] = r
    return out


def key(r):
    return (r["n"], r["b"], r["c"])


def sec(t):
    print("\n" + "=" * 100)
    print(t)
    print("=" * 100)


def main():
    A = load("A")
    C = load("C")
    print("# referee grid A: %d cells (seed 20260823701, n_rep=%d)"
          % (len(A), list(A.values())[0]["n_rep"] if A else 0))
    if C:
        print("# referee grid C: %d cells (seed 20260823703, n_rep=%d)"
              % (len(C), list(C.values())[0]["n_rep"]))

    # ------------------------------------------------------------------ (1)
    sec("(1) SIMULATOR CROSS-VALIDATION -- referee phi_mc vs FOUR already-recorded grids")
    rec = {k: {key(r): r for r in json.load(open(p))["cells"]}
           for k, p in RECORDED.items()}
    names = list(rec)
    hdr = "%6s %4s %7s | %-20s" % ("n", "b", "c", "referee phi (sem)")
    for nm in names:
        hdr += " | %-22s" % (nm + " z")
    print(hdr)
    zs = {nm: [] for nm in names}
    for k in sorted(A, key=lambda x: (x[1], x[2])):
        r = A[k]
        line = "%6d %4d %7.1f | %.6f (%.6f)" % (k[0], k[1], k[2], r["phi_mc"], r["sem_phi"])
        for nm in names:
            q = rec[nm].get(k)
            if q is None:
                line += " | %-22s" % "-"
                continue
            z = (r["phi_mc"] - q["phi_mc"]) / math.hypot(r["sem_phi"], q["sem"])
            zs[nm].append(z)
            line += " | %.6f  z=%+5.2f" % (q["phi_mc"], z)
        print(line)
    print()
    for nm in names:
        a = np.array(zs[nm])
        print("   vs %-20s: %d comparisons, |z|max=%.2f, chi2=%.1f/%d, mean z=%+.2f"
              % (nm, a.size, np.abs(a).max(), (a ** 2).sum(), a.size, a.mean()))
    allz = np.concatenate([np.array(zs[nm]) for nm in names])
    print("   POOLED: %d comparisons, |z|max=%.2f, chi2=%.1f/%d, mean z=%+.3f"
          % (allz.size, np.abs(allz).max(), (allz ** 2).sum(), allz.size, allz.mean()))
    print("   (the four recorded grids are NOT independent of each other in the sense")
    print("    that they share cells; the mean z measures a systematic offset of the")
    print("    referee's simulator against the lineage's, which must be ~0.)")

    # ------------------------------------------------------------------ (2)
    sec("(2) eps := P(x0 on a cycle of f | x0 in R)   -- referee vs target stage B")
    tb = {key(r): r for r in json.load(open(os.path.join(
        LINE, "aggregation_closure_attempt", "global_exclusion_attempt",
        "x0_asymmetry_attempt", "x0_asymmetry_walk_measure_B_results.json")))["cells"]}
    print("%6s %4s %7s %7s | %-26s | %-26s | %7s | %-16s"
          % ("n", "b", "c", "rho", "referee eps (events)", "target stage-B eps (events)",
             "z(diff)", "sigma vs zero (ref)"))
    for k in sorted(tb, key=lambda x: (x[1], x[2])):
        r, q = A.get(k), tb[k]
        if r is None:
            continue
        sq = q["phi_sem"]
        z = (r["eps"] - q["phi_hat"]) / math.hypot(r["sem_eps"], sq)
        print("%6d %4d %7.1f %7.4f | %.4e +- %.1e (%7d) | %.4e +- %.1e (%4d) | %+6.2f  | %8.1f"
              % (k[0], k[1], k[2], r["rho_formula"], r["eps"], r["sem_eps"],
                 r["n_cycR_total"], q["phi_hat"], sq,
                 q["n_norm_x0"] + q["n_rr_x0"], z, r["eps"] / r["sem_eps"]))

    sec("(2b) eps on the FULL 18-cell grid (referee), and rho*eps as a share of phi")
    print("%6s %4s %7s %7s | %-24s | %10s | %9s"
          % ("n", "b", "c", "rho", "eps (referee)", "sigma vs 0", "rho*eps/phi"))
    for k in sorted(A, key=lambda x: (x[1], x[2])):
        r = A[k]
        rho = r["rho_formula"]
        print("%6d %4d %7.1f %7.4f | %.4e +- %.2e | %10.1f | %8.2f%%"
              % (k[0], k[1], k[2], rho, r["eps"], r["sem_eps"],
                 r["eps"] / r["sem_eps"], 100 * rho * r["eps"] / r["phi_mc"]))

    # ------------------------------------------------------------------ (3)
    sec("(3) THE TWO CHANNELS OF eps, measured exactly, vs the two derivations")
    print("%6s %4s %7s | %-30s | %-30s"
          % ("n", "b", "c", "RUN-START rate  meas / tgt / ref",
             "F-DRAW rate    meas / tgt / ref"))
    for k in sorted(A, key=lambda x: (x[1], x[2])):
        r = A[k]
        n, b, c = k
        rho = r["rho_formula"]
        rs = R.rho_start_of(c, n, b)
        v4, T = R.phi_V4_and_T(c, n, b)
        prs = R.phi_runstart(c, n, b)
        dA_t = (rs / rho) * v4
        dA_r = (rs / rho) * prs
        dB_t = c * T / ((1.0 - rho) * n)
        dB_r = (1.0 + c * T) / ((1.0 - rho) * n)
        print("%6d %4d %7.1f | %.3e  %.3f  %.3f (+-%.3f) | %.3e  %.3f  %.3f (+-%.3f)"
              % (n, b, c, r["chA"], r["chA"] / dA_t, r["chA"] / dA_r,
                 r["sem_chA"] / dA_r,
                 r["chB"], r["chB"] / dB_t, r["chB"] / dB_r, r["sem_chB"] / dB_r))
    print("\n   (ratios are MEASURED / DERIVED; 1.000 = perfect.  'tgt' = the target's")
    print("    leading order, 'ref' = the referee's corrected leading order.)")

    # ------------------------------------------------------------------ (4)
    sec("(4) phi_CAND vs phi_EPS vs phi_EPSR on the REFEREE's fresh grid (seed 20260823701)")
    run_chi2(A)

    # ------------------------------------------------------------------ (5)
    sec("(5) DECISIVE SUBSTITUTION: phi_CAND + rho * eps_MEASURED  (no model for eps)")
    chi = {"CAND": 0.0, "EPS": 0.0, "MEAS": 0.0}
    print("%6s %4s %7s %7s | %-18s | %-18s | %-18s"
          % ("n", "b", "c", "rho", "CAND dev%(z)", "EPS dev%(z)", "CAND+rho*eps_meas"))
    for k in sorted(A, key=lambda x: (x[1], x[2])):
        r = A[k]
        n, b, c = k
        m, s = r["phi_mc"], r["sem_phi"]
        rho = r["rho_formula"]
        vC = R.phi_CAND(c, n, b)
        vE = R.phi_EPS(c, n, b)
        vM = vC + rho * r["eps"]
        line = "%6d %4d %7.1f %7.4f" % (n, b, c, rho)
        for nm, v in (("CAND", vC), ("EPS", vE), ("MEAS", vM)):
            z = (m - v) / s
            chi[nm] += z * z
            line += " | %+7.3f%% (%+6.2f)" % (100 * (m - v) / v, z)
        print(line)
    print("\n   chi2 (18 cells): CAND=%.1f  EPS=%.1f  CAND+rho*eps_measured=%.1f"
          % (chi["CAND"], chi["EPS"], chi["MEAS"]))

    # ------------------------------------------------------------------ (6)
    if C:
        sec("(6) SEED-TO-SEED ROBUSTNESS: an independent referee grid (seed 20260823703)")
        run_chi2(C)
        print("\n   cell-by-cell agreement between the two referee grids:")
        zz = []
        for k in sorted(A):
            if k not in C:
                continue
            a, c_ = A[k], C[k]
            z = (a["phi_mc"] - c_["phi_mc"]) / math.hypot(a["sem_phi"], c_["sem_phi"])
            zz.append(z)
        zz = np.array(zz)
        print("      %d cells, chi2=%.1f/%d, |z|max=%.2f  -> sem calibration factor"
              " sqrt(chi2/dof)=%.2f" % (zz.size, (zz ** 2).sum(), zz.size,
                                        np.abs(zz).max(),
                                        math.sqrt((zz ** 2).sum() / zz.size / 2) * math.sqrt(2)))
        # eps agreement
        ze = []
        for k in sorted(A):
            if k not in C:
                continue
            a, c_ = A[k], C[k]
            ze.append((a["eps"] - c_["eps"]) / math.hypot(a["sem_eps"], c_["sem_eps"]))
        ze = np.array(ze)
        print("      eps: %d cells, chi2=%.1f/%d, |z|max=%.2f"
              % (ze.size, (ze ** 2).sum(), ze.size, np.abs(ze).max()))


def run_chi2(G):
    chi = {"CAND": 0.0, "EPS": 0.0, "EPSR": 0.0}
    below = {"CAND": 0, "EPS": 0, "EPSR": 0}
    print("%6s %4s %7s %7s | %9s %9s | %-18s %-18s %-18s"
          % ("n", "b", "c", "rho", "phi_mc", "sem",
             "CAND dev%(z)", "EPS dev%(z)", "EPSR dev%(z)"))
    for k in sorted(G, key=lambda x: (x[1], x[2])):
        r = G[k]
        n, b, c = k
        m, s = r["phi_mc"], r["sem_phi"]
        line = "%6d %4d %7.1f %7.4f | %9.6f %9.6f" % (n, b, c, r["rho_formula"], m, s)
        for nm in ("CAND", "EPS", "EPSR"):
            v = R.CANDIDATES[nm](c, n, b)
            z = (m - v) / s
            chi[nm] += z * z
            below[nm] += 1 if v < m else 0
            line += " | %+7.3f%% (%+6.2f)" % (100 * (m - v) / v, z)
        print(line)
    print("\n   chi2 (%d cells): CAND=%.1f  EPS=%.1f  EPSR=%.1f   |  formula below MC in"
          " %d / %d / %d of %d cells"
          % (len(G), chi["CAND"], chi["EPS"], chi["EPSR"],
             below["CAND"], below["EPS"], below["EPSR"], len(G)))
    return chi


if __name__ == "__main__":
    main()
