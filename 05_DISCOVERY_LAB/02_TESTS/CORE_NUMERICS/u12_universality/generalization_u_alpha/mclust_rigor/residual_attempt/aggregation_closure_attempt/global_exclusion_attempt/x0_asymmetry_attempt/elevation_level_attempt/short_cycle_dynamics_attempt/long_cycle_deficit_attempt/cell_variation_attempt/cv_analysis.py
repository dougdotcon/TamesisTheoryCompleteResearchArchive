"""
cv_analysis.py -- deterministic (no RNG) post-hoc analysis of cv_grid.log's
machine-parseable summary block, per DERIVATION_PREREG.md SS4. Computes:
  - H2 share per cell (+ delta-method SEM), with the SS2 exclusion rule
  - Pooled Pearson r (H2share vs rho, log10(c), log10(b)) + t/p
  - Multiple OLS regression H2share ~ 1 + rho + log10(c) + log10(b)
  - Sub-group (G1..G4) ranges and the SS4.3 decision rule, applied verbatim
"""

import sys
import csv
import io
import math
import numpy as np
from scipy import stats

LOG_PATH = sys.argv[1] if len(sys.argv) > 1 else "cv_grid.log"


def load_rows(path):
    with open(path) as f:
        text = f.read()
    marker = "=== MACHINE-PARSEABLE SUMMARY (for cv_analysis.py) ==="
    idx = text.index(marker)
    csv_text = text[idx + len(marker):].strip().split("\n\ncv_grid.py DONE")[0].strip()
    reader = csv.DictReader(io.StringIO(csv_text))
    rows = []
    for r in reader:
        row = {
            "cid": r["cid"], "b": int(r["b"]), "c": int(r["c"]), "group": r["group"],
            "rho": float(r["rho_formula"]),
            "cpp_own": float(r["cpp_own"]), "phiU_own": float(r["phiU_own"]),
            "phi_own": float(r["phi_own"]), "sem_own": float(r["sem_own"]),
            "dev_own": float(r["dev_own"]), "z_own": float(r["z_own"]),
            "cpp_b1": float(r["cpp_b1"]), "phiU_b1": float(r["phiU_b1"]),
            "phi_b1": float(r["phi_b1"]), "sem_b1": float(r["sem_b1"]),
            "dev_b1": float(r["dev_b1"]), "z_b1": float(r["z_b1"]),
        }
        rows.append(row)
    return rows


def sem_dev_pct(sem_phi, phiU):
    """SEM of dev% = 100*SEM_phi/phiU."""
    return 100.0 * sem_phi / phiU


def compute_h2(rows):
    for r in rows:
        r["sem_dev_own"] = sem_dev_pct(r["sem_own"], r["phiU_own"])
        r["sem_dev_b1"] = sem_dev_pct(r["sem_b1"], r["phiU_b1"])
        defined = (r["dev_own"] < 0) and (abs(r["z_own"]) >= 2.0)
        r["h2_defined"] = defined
        if defined:
            r["h2_share"] = r["dev_b1"] / r["dev_own"]
            # delta method, independent samples (own-b and b=1 use disjoint seeds)
            rel_b1 = r["sem_dev_b1"] / r["dev_b1"] if r["dev_b1"] != 0 else float("inf")
            rel_own = r["sem_dev_own"] / r["dev_own"]
            r["h2_share_sem"] = abs(r["h2_share"]) * math.sqrt(rel_b1 ** 2 + rel_own ** 2)
        else:
            r["h2_share"] = float("nan")
            r["h2_share_sem"] = float("nan")
    return rows


def print_table(rows):
    print(f"{'id':>5} {'b':>5} {'c':>6} {'rho':>7} {'dev_own%':>9} {'z_own':>7} "
          f"{'dev_b1%':>9} {'z_b1':>7} {'H2share':>9} {'H2 SEM':>8} {'defined':>8}")
    for r in rows:
        h2s = f"{100*r['h2_share']:+.1f}%" if r["h2_defined"] else "n/a"
        h2sem = f"{100*r['h2_share_sem']:.1f}pp" if r["h2_defined"] else "n/a"
        print(f"{r['cid']:>5} {r['b']:5d} {r['c']:6d} {r['rho']:7.4f} "
              f"{r['dev_own']:+9.3f} {r['z_own']:+7.2f} "
              f"{r['dev_b1']:+9.3f} {r['z_b1']:+7.2f} "
              f"{h2s:>9} {h2sem:>8} {str(r['h2_defined']):>8}")


def pearson_with_stats(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    n = len(x)
    r = float(np.corrcoef(x, y)[0, 1])
    df = n - 2
    if df <= 0 or abs(r) >= 1.0:
        return r, float("nan"), df, float("nan")
    t = r * math.sqrt(df) / math.sqrt(1 - r ** 2)
    p = 2 * stats.t.sf(abs(t), df)
    return r, t, df, p


def ols_with_stats(X, y, names):
    """X: (n,k) design matrix WITHOUT intercept column (added here). Returns
    dict of name -> (coef, se, t, p)."""
    n, k0 = X.shape
    Xd = np.column_stack([np.ones(n), X])
    k = Xd.shape[1]
    beta, residuals, rank, sv = np.linalg.lstsq(Xd, y, rcond=None)
    yhat = Xd @ beta
    resid = y - yhat
    dof = n - k
    if dof <= 0:
        sigma2 = float("nan")
    else:
        sigma2 = float(resid @ resid) / dof
    try:
        XtX_inv = np.linalg.inv(Xd.T @ Xd)
    except np.linalg.LinAlgError:
        XtX_inv = np.linalg.pinv(Xd.T @ Xd)
    se = np.sqrt(np.diag(XtX_inv) * sigma2) if dof > 0 else np.full(k, float("nan"))
    out = {}
    all_names = ["intercept"] + names
    for i, nm in enumerate(all_names):
        b = beta[i]
        s = se[i]
        if dof > 0 and s > 0:
            t = b / s
            p = 2 * stats.t.sf(abs(t), dof)
        else:
            t, p = float("nan"), float("nan")
        out[nm] = (b, s, t, p, dof)
    ss_tot = float(((y - y.mean()) ** 2).sum())
    ss_res = float((resid ** 2).sum())
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    return out, r2


def group_range(rows, group_id):
    members = [r for r in rows if group_id in r["group"].split(";") and r["h2_defined"]]
    if not members:
        return None
    vals = [r["h2_share"] for r in members]
    sems = [r["h2_share_sem"] for r in members]
    cids = [r["cid"] for r in members]
    lo, hi = min(vals), max(vals)
    lo_i, hi_i = vals.index(lo), vals.index(hi)
    sem_lo, sem_hi = sems[lo_i], sems[hi_i]
    combined_se = math.sqrt(sem_hi ** 2 + sem_lo ** 2)
    z_spread = (hi - lo) / combined_se if combined_se > 0 else float("nan")
    return dict(group=group_id, n=len(vals), min=lo, max=hi,
                range_pp=100 * (hi - lo), cids=cids, vals=vals,
                cid_min=cids[lo_i], cid_max=cids[hi_i], z_spread=z_spread)


def classify_range(range_pp):
    if range_pp <= 15.0:
        return "FLAT"
    if range_pp >= 30.0:
        return "VARIES SUBSTANTIALLY"
    return "AMBIGUOUS"


def main():
    rows = load_rows(LOG_PATH)
    rows = compute_h2(rows)

    print(f"Loaded {len(rows)} cells from {LOG_PATH}\n")
    print("=== Per-cell table ===")
    print_table(rows)

    defined_rows = [r for r in rows if r["h2_defined"]]
    excluded = [r for r in rows if not r["h2_defined"]]
    print(f"\n{len(defined_rows)}/{len(rows)} cells have a defined H2 share "
          f"(dev_own<0 and |z_own|>=2).")
    if excluded:
        print("Excluded (undefined H2 share):",
              ", ".join(f"{r['cid']} (dev_own={r['dev_own']:+.2f}%, z_own={r['z_own']:+.2f})"
                        for r in excluded))

    print("\n=== Pooled Pearson correlations (H2share vs covariate) ===")
    h2 = np.array([r["h2_share"] for r in defined_rows])
    rho_arr = np.array([r["rho"] for r in defined_rows])
    logc = np.array([math.log10(r["c"]) for r in defined_rows])
    logb = np.array([math.log10(r["b"]) for r in defined_rows])
    for name, arr in [("rho", rho_arr), ("log10(c)", logc), ("log10(b)", logb)]:
        r, t, df, p = pearson_with_stats(arr, h2)
        sig = "**" if (not math.isnan(p) and p < 0.05) else "  "
        print(f"  H2share vs {name:10s}: r={r:+.3f}  t={t:+.3f}  df={df}  p={p:.4f} {sig}")

    print("\n=== Multiple OLS: H2share ~ 1 + rho + log10(c) + log10(b) ===")
    X = np.column_stack([rho_arr, logc, logb])
    out, r2 = ols_with_stats(X, h2, ["rho", "log10(c)", "log10(b)"])
    print(f"  R^2 = {r2:.4f}   n={len(defined_rows)}")
    for nm, (b, s, t, p, dof) in out.items():
        sig = "**" if (not math.isnan(p) and p < 0.05) else "  "
        print(f"  {nm:10s}: coef={b:+.4f}  se={s:.4f}  t={t:+.3f}  df={dof}  p={p:.4f} {sig}")

    print("\n=== Sub-group range test (PRIMARY discriminator, SS4.3) ===")
    group_results = {}
    for g in ["G1", "G2", "G3", "G4"]:
        res = group_range(rows, g)
        group_results[g] = res
        if res is None:
            print(f"  {g}: no defined cells -- cannot classify")
            continue
        cls = classify_range(res["range_pp"])
        vals_str = ", ".join(f"{cid}={100*v:+.1f}%" for cid, v in zip(res["cids"], res["vals"]))
        print(f"  {g}: n={res['n']}  range={res['range_pp']:.1f}pp "
              f"[{100*res['min']:+.1f}%, {100*res['max']:+.1f}%]  -> {cls}")
        print(f"      cells: {vals_str}")
        print(f"      noise check (delta-method, NOT part of the SS4.3 rule, per SS2's "
              f"stated use): max({res['cid_max']}) vs min({res['cid_min']}) "
              f"spread z={res['z_spread']:+.2f} "
              f"({'exceeds' if abs(res['z_spread']) >= 2 else 'within'} noise at |z|>=2)")

    print("\n=== Decision (SS4.3 rule, applied mechanically) ===")
    def cls(g):
        r = group_results.get(g)
        return classify_range(r["range_pp"]) if r else "N/A"

    c1, c2, c3, c4 = cls("G1"), cls("G2"), cls("G3"), cls("G4")
    print(f"  G1(c fixed, b&rho vary)={c1}  G2(b fixed, c&rho vary)={c2}  "
          f"G3(rho~0.785 fixed)={c3}  G4(rho~0.457 fixed)={c4}")

    rho_fixed_flat = (c3 == "FLAT") and (c4 == "FLAT")
    rho_varying_moves = (c1 == "VARIES SUBSTANTIALLY") or (c2 == "VARIES SUBSTANTIALLY")
    if rho_fixed_flat and rho_varying_moves:
        verdict = ("RHO IS THE DRIVER: both rho-fixed groups (G3,G4) are FLAT while at "
                   "least one rho-varying group (G1/G2) VARIES SUBSTANTIALLY.")
    elif c1 == "FLAT" and (c3 != "FLAT" or c4 != "FLAT"):
        verdict = ("b is not a driver once c is controlled (G1 flat); rho-fixed groups "
                   "did not both come out flat, so this is not attributed to rho cleanly "
                   "-- reported as partial/mixed, see full table.")
    elif c2 == "FLAT" and (c3 != "FLAT" or c4 != "FLAT"):
        verdict = ("c is not a driver once b is controlled (G2 flat); rho-fixed groups "
                   "did not both come out flat -- reported as partial/mixed, see full table.")
    elif all(c == "VARIES SUBSTANTIALLY" for c in [c1, c2, c3, c4] if c != "N/A"):
        verdict = ("HONEST NEGATIVE RESULT: no group is flat -- none of rho, c, b alone "
                   "(holding the other roughly fixed) explains the H2-share variation.")
    else:
        verdict = "PARTIAL / MIXED pattern -- no clean single-covariate verdict; see full table."

    print(f"\n  VERDICT: {verdict}")


if __name__ == "__main__":
    main()
