"""x0_asymmetry_attempt -- stage 2: analysis of the measured split.

Wave 9, DISC-DEC-041 front (a).

Deterministic post-processing of the three measurement stages produced by
`x0_asymmetry_walk_measure.py` (own simulator, SeedSequence(20260822941)),
plus EXPLICITLY LABELLED REUSE of Monte-Carlo means already recorded by the
predecessors (no new simulation is run here):

  ../mclust_global_validate_results.json   -- phi_mc, 18 cells, seeds
                                              20260822911 (global_exclusion)
  ../../mclust_aggregation_validate_results.json -- phi_mc, 18 cells, seeds
                                              20260822904 (aggregation_closure)

Four things are computed:

 (1) SIMULATOR CROSS-CHECK.  Stage U (x0 uniform on [n]) against the
     phi_mc already recorded by two predecessors with independent seeds.
 (2) TOTAL-PROBABILITY CHECK.  phi_mc =? (1-rho)*phi_A + rho*eps, using the
     independently measured stage-A and stage-B numbers.  This is a check
     on the (1-rho) dilution factor of residual_attempt sec 6 -- the ONLY
     place x0 is currently treated asymmetrically at all.
 (3) THE PRE-REGISTERED TEST.  lambda_x0 vs lambda_other, with the
     structure-matched sub-split, against the common constant P that
     phi_CAND / phi_CAND5 / phi_GLOBAL all assume.
 (4) THE DECISIVE TEST (same logic as global_exclusion_attempt sec 4).
     Holding the OTHER arc starts at their measured elevation, solve for
     the x0 elevation P0 that would be needed to reproduce phi_mc, and ask
     whether the DIRECTLY MEASURED lambda_x0 reaches it.  Then evaluate
     phi_ASYM at the measured (lambda_x0, lambda_other, eps) and compare
     to phi_mc and to phi_CAND.
"""
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from x0_asym_formula import (rho_of, P_lead, P_exact, phi_asym, phi_CAND_own,
                             phi_CAND5_own, solve_P0_needed)

GLOB = os.path.join(HERE, "..", "mclust_global_validate_results.json")
AGGR = os.path.join(HERE, "..", "..", "mclust_aggregation_validate_results.json")


def load(path):
    with open(path) as fh:
        return json.load(fh)["cells"]


def key(r):
    return (r["n"], r["b"], float(r["c"]))


def main():
    A = {key(r): r for r in load(os.path.join(HERE, "x0_asymmetry_walk_measure_A_results.json"))}
    B = {key(r): r for r in load(os.path.join(HERE, "x0_asymmetry_walk_measure_B_results.json"))}
    U = {key(r): r for r in load(os.path.join(HERE, "x0_asymmetry_walk_measure_U_results.json"))}
    mcG = {key(r): r for r in load(GLOB)}
    mcA = {key(r): r for r in load(AGGR)}

    out = []
    lines = []

    def say(m):
        print(m)
        lines.append(m)

    say("=" * 100)
    say("(1) SIMULATOR CROSS-CHECK -- stage U (x0 uniform) vs phi_mc already recorded")
    say("=" * 100)
    say(f"{'b':>4} {'c':>7} {'rho':>7} | {'phi_U_hat':>10} {'sem':>9} | "
        f"{'phi_mc(911)':>11} {'sem':>9} {'z':>6} | {'phi_mc(904)':>11} {'sem':>9} {'z':>6}")
    for k in U:
        u = U[k]
        g, a = mcG.get(k), mcA.get(k)
        row = f"{k[1]:4d} {k[2]:7.1f} {u['rho']:7.4f} | {u['phi_hat']:10.6f} {u['phi_sem']:9.6f} |"
        for m in (g, a):
            if m is None:
                row += f" {'-':>11} {'-':>9} {'-':>6} |"
            else:
                z = (u["phi_hat"] - m["phi_mc"]) / math.hypot(u["phi_sem"], m["sem"])
                row += f" {m['phi_mc']:11.6f} {m['sem']:9.6f} {z:+6.2f} |"
        say(row)

    say("")
    say("=" * 100)
    say("(2) TOTAL-PROBABILITY CHECK   phi_mc =? (1-rho)*phi_A + rho*eps")
    say("=" * 100)
    say(f"{'b':>4} {'c':>7} {'rho':>7} | {'phi_A':>9} {'sem':>8} | {'eps':>9} {'sem':>8} | "
        f"{'rho*eps':>9} {'as % of phi':>11} | {'recomb':>9} {'phi_mc':>9} {'z':>6}")
    for k in sorted(A, key=lambda z: -A[z]["rho"]):
        a, b_, g = A[k], B[k], mcG[k]
        rho = a["rho"]
        rec = (1 - rho) * a["phi_hat"] + rho * b_["phi_hat"]
        sem_rec = math.hypot((1 - rho) * a["phi_sem"], rho * b_["phi_sem"])
        z = (rec - g["phi_mc"]) / math.hypot(sem_rec, g["sem"])
        say(f"{k[1]:4d} {k[2]:7.1f} {rho:7.4f} | {a['phi_hat']:9.6f} {a['phi_sem']:8.6f} | "
            f"{b_['phi_hat']:9.6f} {b_['phi_sem']:8.6f} | {rho * b_['phi_hat']:9.6f} "
            f"{100 * rho * b_['phi_hat'] / g['phi_mc']:10.2f}% | {rec:9.6f} {g['phi_mc']:9.6f} {z:+6.2f}")
    say("   same check against THIS front's OWN stage-U run (fully internal, "
        "no predecessor data):")
    say(f"{'b':>4} {'c':>7} {'rho':>7} | {'recomb':>9} {'sem':>8} | {'phi_U_hat':>9} {'sem':>8} | {'z':>6}")
    for k in sorted(A, key=lambda z: -A[z]["rho"]):
        a, b_, u = A[k], B[k], U[k]
        rho = a["rho"]
        rec = (1 - rho) * a["phi_hat"] + rho * b_["phi_hat"]
        sem_rec = math.hypot((1 - rho) * a["phi_sem"], rho * b_["phi_sem"])
        z = (rec - u["phi_hat"]) / math.hypot(sem_rec, u["phi_sem"])
        say(f"{k[1]:4d} {k[2]:7.1f} {rho:7.4f} | {rec:9.6f} {sem_rec:8.6f} | "
            f"{u['phi_hat']:9.6f} {u['phi_sem']:8.6f} | {z:+6.2f}")

    say("")
    say("=" * 100)
    say("(3) PRE-REGISTERED TEST -- lambda_x0 vs lambda_other (x0 drawn from R^c)")
    say("=" * 100)
    say(f"{'b':>4} {'c':>7} {'rho':>7} | {'P_lead':>7} | {'lam_x0':>15} | {'lam_other':>15} | "
        f"{'ratio':>15} | {'z_diff':>7}")
    for k in sorted(A, key=lambda z: -A[z]["rho"]):
        a = A[k]
        pl = P_lead(a["rho"])
        zd = (a["lambda_x0"] - a["lambda_other"]) / a["sem_diff"]
        say(f"{k[1]:4d} {k[2]:7.1f} {a['rho']:7.4f} | {pl:7.4f} | "
            f"{a['lambda_x0']:8.4f}+-{a['sem_lambda_x0']:.4f} | "
            f"{a['lambda_other']:8.4f}+-{a['sem_lambda_other']:.4f} | "
            f"{a['ratio_x0_over_other']:8.4f}+-{a['sem_ratio']:.4f} | {zd:+7.2f}")
    say("")
    say("   structure-matched sub-split (same role on the walk):")
    say(f"{'b':>4} {'c':>7} {'rho':>7} | {'x0 as CURRENT arc start':>26} | "
        f"{'other CURRENT arc start':>26} | {'x0 as OLDER':>20} | {'other OLDER':>20}")
    for k in sorted(A, key=lambda z: -A[z]["rho"]):
        a = A[k]
        say(f"{k[1]:4d} {k[2]:7.1f} {a['rho']:7.4f} | "
            f"{a['lambda_x0_own_arc']:14.4f}+-{a['sem_lambda_x0_own_arc']:.4f} | "
            f"{a['lambda_curr_arc']:14.4f}+-{a['sem_lambda_curr_arc']:.4f} | "
            f"{a['lambda_x0_older']:8.4f}+-{a['sem_lambda_x0_older']:.4f} | "
            f"{a['lambda_older_arcs']:8.4f}+-{a['sem_lambda_older_arcs']:.4f}")

    say("")
    say("=" * 100)
    say("(4) DECISIVE TEST -- is the MEASURED lambda_x0 large enough to close the residual?")
    say("=" * 100)
    need_ratio = []
    say(f"{'b':>4} {'c':>7} {'rho':>7} | {'P1 used':>8} | {'P0 needed':>10} | "
        f"{'lam_x0 meas':>16} | {'shortfall%':>10} | {'z(meas-need)':>12}")
    for k in sorted(A, key=lambda z: -A[z]["rho"]):
        a, b_, g = A[k], B[k], mcG[k]
        n, bb, c = k
        P1 = a["lambda_other"]
        eps = b_["phi_hat"]
        P0need = solve_P0_needed(c, n, bb, P1, g["phi_mc"], eps=eps)
        short = 100.0 * (a["lambda_x0"] - P0need) / P0need
        z = (a["lambda_x0"] - P0need) / a["sem_lambda_x0"]
        say(f"{bb:4d} {c:7.1f} {a['rho']:7.4f} | {P1:8.4f} | {P0need:10.4f} | "
            f"{a['lambda_x0']:9.4f}+-{a['sem_lambda_x0']:.4f} | {short:+9.2f}% | {z:+12.2f}")
        need_ratio.append((bb, c, P0need / P1, a["ratio_x0_over_other"], a["sem_ratio"]))

    say("")
    say("   the SAME test read as a RATIO -- what asymmetry would phi_mc require,")
    say("   given the measured lambda_other and the measured eps?")
    say(f"{'b':>4} {'c':>7} | {'REQUIRED P0/P1':>15} | {'MEASURED ratio':>17}")
    for bb, c, nr, mr, ms in need_ratio:
        say(f"{bb:4d} {c:7.1f} | {nr:15.4f} | {mr:10.4f}+-{ms:.4f}")
    say("   -> the required ratio sits in [%.3f, %.3f]: phi_mc requires x0 and the"
        % (min(x[2] for x in need_ratio), max(x[2] for x in need_ratio)))
    say("      other arc starts to carry essentially the SAME elevation.")
    say("")
    say("   phi evaluated at the MEASURED (lambda_x0, lambda_other, eps):")
    say(f"{'b':>4} {'c':>7} {'rho':>7} | {'phi_mc':>9} {'sem':>8} | {'phi_CAND':>9} {'dev%':>7} "
        f"{'z':>6} | {'phi_ASYM':>9} {'dev%':>7} {'z':>6}")
    chi2_cand = chi2_asym = 0.0
    for k in sorted(A, key=lambda z: -A[z]["rho"]):
        a, b_, g = A[k], B[k], mcG[k]
        n, bb, c = k
        cand = phi_CAND_own(c, n, bb)
        asym = phi_asym(c, n, bb, a["lambda_x0"], a["lambda_other"], eps=b_["phi_hat"])
        dc = 100 * (g["phi_mc"] - cand) / cand
        da = 100 * (g["phi_mc"] - asym) / asym
        zc = (g["phi_mc"] - cand) / g["sem"]
        za = (g["phi_mc"] - asym) / g["sem"]
        chi2_cand += zc * zc
        chi2_asym += za * za
        say(f"{bb:4d} {c:7.1f} {a['rho']:7.4f} | {g['phi_mc']:9.6f} {g['sem']:8.6f} | "
            f"{cand:9.6f} {dc:+6.2f}% {zc:+6.2f} | {asym:9.6f} {da:+6.2f}% {za:+6.2f}")
        out.append(dict(n=n, b=bb, c=c, rho=a["rho"], phi_mc=g["phi_mc"], sem=g["sem"],
                        phi_A=a["phi_hat"], sem_phi_A=a["phi_sem"],
                        eps=b_["phi_hat"], sem_eps=b_["phi_sem"],
                        lambda_x0=a["lambda_x0"], sem_lambda_x0=a["sem_lambda_x0"],
                        lambda_other=a["lambda_other"], sem_lambda_other=a["sem_lambda_other"],
                        ratio=a["ratio_x0_over_other"], sem_ratio=a["sem_ratio"],
                        lambda_x0_own_arc=a["lambda_x0_own_arc"],
                        lambda_curr_arc=a["lambda_curr_arc"],
                        lambda_x0_older=a["lambda_x0_older"],
                        lambda_older_arcs=a["lambda_older_arcs"],
                        P_lead=P_lead(a["rho"]), P_exact=P_exact(c, n, bb),
                        P0_needed=solve_P0_needed(c, n, bb, a["lambda_other"],
                                                  g["phi_mc"], eps=b_["phi_hat"]),
                        phi_CAND=cand, phi_ASYM=asym))
    say(f"   chi2 over these {len(out)} cells: phi_CAND={chi2_cand:.2f}  phi_ASYM={chi2_asym:.2f}")

    say("")
    say("=" * 100)
    say("(5) DECOMPOSITION -- which measured ingredient does the work?")
    say("    CAND      : P0=P1=1/(1-rho),        eps=0        [residual_attempt]")
    say("    +EPS      : P0=P1=1/(1-rho),        eps=measured")
    say("    +LEVEL    : P0=P1=lambda_bar (HT-pooled measured), eps=measured")
    say("    +ASYM     : P0=lambda_x0, P1=lambda_other,        eps=measured")
    say("=" * 100)
    say(f"{'b':>4} {'c':>7} {'rho':>7} | {'lam_bar':>7} | {'CAND':>8} {'+EPS':>8} "
        f"{'+LEVEL':>8} {'+ASYM':>8}   (dev% vs phi_mc)")
    chi2s = dict(CAND=0.0, EPS=0.0, LEVEL=0.0, ASYM=0.0)
    for k in sorted(A, key=lambda z: -A[z]["rho"]):
        a, b_, g = A[k], B[k], mcG[k]
        n, bb, c = k
        rho = a["rho"]
        pl = P_lead(rho)
        eps = b_["phi_hat"]
        # HT-pooled common elevation: (all hits on arc starts)/(all weights)
        lam_bar = ((a["hit_A"] + a["hit_B"] + a["hit_C"])
                   / (a["sum_wA"] + a["sum_wB"] + a["sum_wC"]))
        vals = dict(
            CAND=phi_asym(c, n, bb, pl, pl, eps=0.0),
            EPS=phi_asym(c, n, bb, pl, pl, eps=eps),
            LEVEL=phi_asym(c, n, bb, lam_bar, lam_bar, eps=eps),
            ASYM=phi_asym(c, n, bb, a["lambda_x0"], a["lambda_other"], eps=eps))
        devs = {kk: 100 * (g["phi_mc"] - v) / v for kk, v in vals.items()}
        for kk, v in vals.items():
            chi2s[kk] += ((g["phi_mc"] - v) / g["sem"]) ** 2
        say(f"{bb:4d} {c:7.1f} {rho:7.4f} | {lam_bar:7.4f} | "
            f"{devs['CAND']:+7.2f}% {devs['EPS']:+7.2f}% {devs['LEVEL']:+7.2f}% {devs['ASYM']:+7.2f}%")
        for kk in vals:
            out[[i for i, r in enumerate(out) if (r["n"], r["b"], r["c"]) == k][0]]["phi_" + kk] = vals[kk]
        out[[i for i, r in enumerate(out) if (r["n"], r["b"], r["c"]) == k][0]]["lambda_bar"] = lam_bar
    say("   chi2 (6 cells): " + "  ".join(f"{kk}={vv:.2f}" for kk, vv in chi2s.items()))

    say("")
    say("=" * 100)
    say("(6) POOLED ASYMMETRY AND ITS HOMOGENEITY")
    say("=" * 100)
    r = np.array([A[k]["ratio_x0_over_other"] for k in A])
    s = np.array([A[k]["sem_ratio"] for k in A])
    w = 1.0 / s ** 2
    rbar = float((w * r).sum() / w.sum())
    sbar = float(1.0 / math.sqrt(w.sum()))
    chi2_hom = float((w * (r - rbar) ** 2).sum())
    say(f"   inverse-variance pooled lambda_x0/lambda_other = {rbar:.4f} +- {sbar:.4f}"
        f"   (z vs 1 = {(rbar - 1) / sbar:+.2f})")
    say(f"   homogeneity chi2 = {chi2_hom:.2f} on {len(r) - 1} dof"
        f"  -> the cell-to-cell scatter is {'NOT ' if chi2_hom > 11.07 else ''}"
        f"consistent with a single constant ratio")
    say("   (11.07 = 5%-point of chi2_5; the six ratios and their sems are the "
        "table in section 3)")

    say("")
    say("=" * 100)
    say("(8) INDEPENDENT REPLICATION (stage R, SeedSequence 20260822942) of the")
    say("    three cells where stage A was most interesting: the two with a")
    say("    significant NEGATIVE asymmetry and one null control.")
    say("=" * 100)
    rpath = os.path.join(HERE, "x0_asymmetry_walk_measure_R_results.json")
    R = {}
    if os.path.exists(rpath):
        R = {key(r): r for r in load(rpath)}
    if R:
        say(f"{'b':>4} {'c':>7} {'rho':>7} | {'run1 (941)':>18} | {'run2 (942)':>18} | "
            f"{'z(run1-run2)':>12}")
        for k in sorted(R, key=lambda z: -R[z]["rho"]):
            a, r2 = A[k], R[k]
            zz = ((a["ratio_x0_over_other"] - r2["ratio_x0_over_other"])
                  / math.hypot(a["sem_ratio"], r2["sem_ratio"]))
            say(f"{k[1]:4d} {k[2]:7.1f} {a['rho']:7.4f} | "
                f"{a['ratio_x0_over_other']:9.4f}+-{a['sem_ratio']:.4f} | "
                f"{r2['ratio_x0_over_other']:9.4f}+-{r2['sem_ratio']:.4f} | {zz:+12.2f}")
        rr = np.array([A[k]["ratio_x0_over_other"] for k in A]
                      + [R[k]["ratio_x0_over_other"] for k in R])
        ss = np.array([A[k]["sem_ratio"] for k in A] + [R[k]["sem_ratio"] for k in R])
        ww = 1.0 / ss ** 2
        rb = float((ww * rr).sum() / ww.sum())
        sb_ = float(1.0 / math.sqrt(ww.sum()))
        x2 = float((ww * (rr - rb) ** 2).sum())
        infl = math.sqrt(x2 / (len(rr) - 1))
        say(f"   pooled over all {len(rr)} measurements: {rb:.4f} +- {sb_:.4f} "
            f"(statistical only)")
        say(f"   homogeneity chi2 = {x2:.2f} on {len(rr) - 1} dof -> quoted sems are "
            f"under-dispersed by ~{infl:.2f}x")
        say(f"   pooled with the scatter-inflated error: {rb:.4f} +- {sb_ * infl:.4f} "
            f"(z vs 1 = {(rb - 1) / (sb_ * infl):+.2f})")
        say("   NOTE the sign: a ratio BELOW 1 means x0's elevation is LOWER than")
        say("   the other arc starts'.  Closing the phi_CAND residual would require")
        say("   it to be HIGHER, by +1% to +4% (section 4 / ATTEMPT.md sec 2.3).")

    say("")
    say("=" * 100)
    say("(7) ELEVATION vs VISITED MASS s -- is a CONSTANT P adequate?")
    say("    Stage R only (stage A's four equal-width bins over [0,1] put every")
    say("    event in the first bin; stage R uses bin edges concentrated where")
    say("    the walks actually live).  Poisson errors sqrt(hits)/sum(weights),")
    say("    pooled over instances (no cluster bootstrap) -- indicative only.")
    say("=" * 100)
    for k in sorted(R, key=lambda z: -R[z]["rho"]):
        a = R[k]
        sb = np.array(a["sbin"]).reshape(a["n_sbin"], 6)
        pl = P_lead(a["rho"])
        edges = a.get("s_edges")
        row0, row1 = [], []
        for j in range(a["n_sbin"]):
            wA, wO, hA, hO = sb[j, 0], sb[j, 1], sb[j, 2], sb[j, 3]
            row0.append(f"{hA / wA:5.2f}+-{math.sqrt(max(hA, 1)) / wA:.2f}" if hA > 4 else "   -    ")
            row1.append(f"{hO / wO:5.2f}+-{math.sqrt(max(hO, 1)) / wO:.2f}" if hO > 4 else "   -    ")
        say(f"   b={k[1]:3d} c={k[2]:6.1f} rho={a['rho']:.4f} P_lead={pl:.4f}")
        if edges:
            say("      s bins:                 " + "  ".join(
                f"{edges[j]:.3f}-{edges[j+1]:.3f}"[:8].rjust(8) for j in range(a["n_sbin"])))
        say("      lam_x0    by s bin:     " + "  ".join(row0))
        say("      lam_other by s bin:     " + "  ".join(row1))

    with open(os.path.join(HERE, "x0_asym_analysis_results.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    with open(os.path.join(HERE, "x0_asym_analysis.log"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\nsaved x0_asym_analysis_results.json / .log")


if __name__ == "__main__":
    main()
