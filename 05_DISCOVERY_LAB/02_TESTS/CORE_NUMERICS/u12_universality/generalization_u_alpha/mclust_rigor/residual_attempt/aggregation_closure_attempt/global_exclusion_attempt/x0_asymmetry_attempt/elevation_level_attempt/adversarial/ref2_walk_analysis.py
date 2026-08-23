"""ref2_walk_analysis.py -- analysis of the referee's own walk/probe runs.

For every cell it reports, per mass bin:
    lambda_meas   = sum(hit)/sum(w_master)        [measurement]
    lambda_pool   = sum(w_exact)/sum(w_master)    [the PER-STEP pool law,
                                                   hazard = 1/(|U_rem| - #normal
                                                   steps), measured step by step]
    lambda_cf     = sum(w_cf)/sum(w_master)       [the CLOSED FORM (3.1),
                                                   lambda(t) = (1-t)/(A - t_c)
                                                   with A the ENSEMBLE-MEAN pool]
    P_lead        = 1/(1-rho)                     [the constant every formula of
                                                   the lineage uses]
and chi2 of lambda_meas against each of the three, plus the aggregate ratios
  sum(hit)/sum(w_exact)   and   sum(hit)/sum(w_cf).
Errors: cluster bootstrap over the 256/384 independent walk slots.
"""
import glob
import json
import sys

import numpy as np

BOOT = 4000
MIN_HITS = 2000


def analyse(path, rng):
    with open(path) as fh:
        r = json.load(fh)
    n, b, c = r["n"], r["b"], r["c"]
    acc = {k: np.array(v) for k, v in r["acc"].items()}
    G, NB = acc["hit"].shape
    edg = np.array(r["bin_edges"])
    p = c / n
    rho = 1 - (1 - p) ** b
    Plead = 1 / (1 - rho)
    A = (1 - rho) / (1 - p)

    idx = rng.integers(0, G, size=(BOOT, G))

    def ratio(num, den):
        pt = num.sum() / den.sum() if den.sum() > 0 else np.nan
        nb_ = num[idx].sum(axis=1)
        db_ = den[idx].sum(axis=1)
        return pt, float(np.std(nb_ / db_, ddof=1))

    lines = []
    lines.append("cell n=%d b=%d c=%d  rho=%.4f  P_lead=%.4f  "
                 "lambda(0)=P_exact=%.4f" % (n, b, c, rho, Plead, 1 / A))
    t = r["tot"]
    lines.append("  normal steps %d   walks %d   cyclic %d   "
                 "audit(pi(x) in U_rem) fails %d   audit(no re-consumption) "
                 "fails %d" % (t["normal"], t["walks"], t["cyc"],
                               t["audit_U"], t["audit_cons"]))
    lines.append("  terminal landings: on an arc start (R^c) %d, on a visited "
                 "chain point of R %d, other visited %d"
                 % (t["term_arc"], t["term_chainR"], t["term_other"]))
    lines.append("  %-16s %9s %8s %9s %9s %9s %8s %8s"
                 % ("mass bin", "hits", "lam_meas", "+-", "lam_pool",
                    "lam_cf(3.1)", "P_lead", "hit/we"))
    chi = dict(Plead=0.0, pool=0.0, cf=0.0)
    nbin_used = 0
    for j in range(NB):
        h = acc["hit"][:, j]
        if h.sum() < MIN_HITS:
            continue
        nbin_used += 1
        lm, slm = ratio(h, acc["wm"][:, j])
        lp = acc["we"][:, j].sum() / acc["wm"][:, j].sum()
        lc = acc["wc"][:, j].sum() / acc["wm"][:, j].sum()
        chi["Plead"] += ((lm - Plead) / slm) ** 2
        chi["pool"] += ((lm - lp) / slm) ** 2
        chi["cf"] += ((lm - lc) / slm) ** 2
        lines.append("  [%.4f,%.4f] %9.0f %8.4f %9.4f %9.4f %9.4f %8.4f %8.4f"
                     % (edg[j], edg[j + 1], h.sum(), lm, slm, lp, lc, Plead,
                        h.sum() / acc["we"][:, j].sum()))
    ragg, sagg = ratio(acc["hit"].sum(1), acc["we"].sum(1))
    rcf, scf = ratio(acc["hit"].sum(1), acc["wc"].sum(1))
    rT, sT = ratio(acc["hitT"].sum(1), acc["wT"].sum(1))
    lmA, slmA = ratio(acc["hit"].sum(1), acc["wm"].sum(1))
    lines.append("  AGGREGATE  lambda_meas = %.4f +- %.4f   pool law %.4f   "
                 "closed form %.4f   P_lead %.4f"
                 % (lmA, slmA, acc["we"].sum() / acc["wm"].sum(),
                    acc["wc"].sum() / acc["wm"].sum(), Plead))
    lines.append("  ratio hits/sum(w_exact)  [PER-STEP POOL LAW] = %.5f +- %.5f"
                 "  (z vs 1 = %+.2f)" % (ragg, sagg, (ragg - 1) / sagg))
    lines.append("  ratio hits/sum(w_closedform (3.1)) = %.5f +- %.5f"
                 "  (z vs 1 = %+.2f)" % (rcf, scf, (rcf - 1) / scf))
    lines.append("  HT on the walk's OWN live closure targets: "
                 "hits/sum(w) = %.4f +- %.4f  (%d hits)"
                 % (rT, sT, acc["hitT"].sum()))
    lines.append("  chi2 over %d bins:  vs constant P_lead = %.1f | "
                 "vs per-step pool law = %.1f | vs closed form (3.1) = %.1f"
                 % (nbin_used, chi["Plead"], chi["pool"], chi["cf"]))
    return lines, dict(cell=(n, b, c), rho=rho, nbin=nbin_used, chi=chi,
                       ragg=ragg, sagg=sagg, rcf=rcf, scf=scf, rT=rT, sT=sT,
                       lam_agg=lmA, lam_agg_sem=slmA, Plead=Plead,
                       lam_pool=acc["we"].sum() / acc["wm"].sum(),
                       lam_cf=acc["wc"].sum() / acc["wm"].sum(),
                       normal=t["normal"], walks=t["walks"],
                       audit=(t["audit_U"], t["audit_cons"]))


if __name__ == "__main__":
    rng = np.random.default_rng(np.random.SeedSequence(20260824930))
    files = sorted(glob.glob("ref2_walk_*.json"))
    out = []
    summ = []
    for f in files:
        L, s = analyse(f, rng)
        out.extend(L)
        out.append("")
        summ.append(s)
    tot = dict(Plead=0.0, pool=0.0, cf=0.0)
    nb = 0
    for s in summ:
        for k in tot:
            tot[k] += s["chi"][k]
        nb += s["nbin"]
    out.append("=" * 78)
    out.append("POOLED over %d cells, %d mass bins, %d normal steps:"
               % (len(summ), nb, sum(s["normal"] for s in summ)))
    out.append("   chi2 vs CONSTANT elevation P_lead      = %.1f" % tot["Plead"])
    out.append("   chi2 vs PER-STEP pool law 1/(|U|-m)    = %.1f" % tot["pool"])
    out.append("   chi2 vs CLOSED FORM (3.1) lambda(t)    = %.1f" % tot["cf"])
    out.append("   (expected ~%d for a correct hypothesis)" % nb)
    out.append("")
    out.append("   %-22s %10s %10s %10s %10s"
               % ("cell", "rho", "hits/w_pool", "hits/w_cf", "HT own targets"))
    for s in summ:
        out.append("   n=%6d b=%4d c=%5d %7.4f  %.5f+-%.5f  %.5f+-%.5f  "
                   "%.4f+-%.4f"
                   % (s["cell"][0], s["cell"][1], s["cell"][2], s["rho"],
                      s["ragg"], s["sagg"], s["rcf"], s["scf"], s["rT"],
                      s["sT"]))
    txt = "\n".join(out)
    print(txt)
    with open("ref2_walk_analysis.log", "w") as fh:
        fh.write(txt + "\n")
