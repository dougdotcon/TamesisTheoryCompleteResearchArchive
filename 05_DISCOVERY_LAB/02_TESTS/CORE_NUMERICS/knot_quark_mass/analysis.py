#!/usr/bin/env python3
"""Frente knot-quark-mass (DISC-CORE-NUMERICS-001).
Implements the pre-declared criteria of METHODOLOGY_NOTE.md:
 (i)   reproduction with the archive's own numbers
 (ii)  refit with independent reference data (ACPR ropelengths, PDG 2025 masses)
 (iii) leave-one-out (failure threshold: |log10(M_pred/M_obs)| > 0.5 dex)
 (iv)  permutation null over knot-to-generation assignments
       (Null A: 100000 sampled injective ordered triples, seed=12345;
        Null B: monotone subset; pass requires claimed R^2 > p95 of Null B
        in EACH sector; full enumeration reported as robustness only)
Model: ln M = c + alpha * x, OLS; R^2 in log space. x convention noted per fit
(affine changes of x leave R^2 invariant).
"""
import json
import numpy as np

rng = np.random.default_rng(12345)
OUT = {}

# ---------------------------------------------------------------- data
# Archive's own numbers (knot_mass_fit.py lines 22, 32, 38)
LD_ARCHIVE = np.array([16.37, 21.17, 23.55])
M_UP_ARCH = np.array([2.2, 1275.0, 173000.0])
M_DN_ARCH = np.array([4.7, 95.0, 4180.0])

# Independent references (see PROVENANCE.md)
KNOTS = json.load(open("data/knot_ropelength_acpr.json"))["ropelength"]
LD_INDEP = np.array([KNOTS["3_1"], KNOTS["4_1"], KNOTS["5_1"]]) / 2.0  # L/D = Rop/2
# PDG 2025 (rpp2025-sum-quarks.pdf): u,d,s MSbar@2GeV; mc(mc); mb(mb); top direct
M_UP_PDG = np.array([2.16, 1273.0, 172560.0])
M_DN_PDG = np.array([4.70, 93.5, 4183.0])
M_TOP_VARIANTS = {"direct": 172560.0, "pole_xsec": 172400.0, "msbar_xsec": 162500.0}


def fit(x, m):
    """OLS of ln m on x. Returns alpha, lnM0, R^2 (log space)."""
    x = np.asarray(x, float)
    y = np.log(np.asarray(m, float))
    alpha, c = np.polyfit(x, y, 1)
    yhat = alpha * x + c
    ss_res = np.sum((y - yhat) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    return float(alpha), float(c), float(1.0 - ss_res / ss_tot)


def r2_vec(X, y):
    """Vectorized 3-point R^2 of ln-mass y (3,) against rows of X (N,3)."""
    y = y - y.mean()
    Xc = X - X.mean(axis=1, keepdims=True)
    sxy = (Xc * y).sum(axis=1)
    sxx = (Xc ** 2).sum(axis=1)
    syy = (y ** 2).sum()
    with np.errstate(divide="ignore", invalid="ignore"):
        r2 = sxy ** 2 / (sxx * syy)
    return np.where(sxx > 0, r2, 0.0)


# ---------------------------------------------------------- (i) reproduction
rep = {}
for sec, m in (("up", M_UP_ARCH), ("down", M_DN_ARCH)):
    a, c, r2 = fit(LD_ARCHIVE, m)
    rep[sec] = {"alpha": round(a, 4), "M0_MeV": float(np.exp(c)), "R2_log": round(r2, 6)}
rep["pass_alpha"] = abs(rep["up"]["alpha"] - 1.53) <= 0.02 and abs(rep["down"]["alpha"] - 0.90) <= 0.02
rep["pass_R2_up_gt_0.99"] = rep["up"]["R2_log"] > 0.99
rep["pass_R2_down_gt_0.99"] = rep["down"]["R2_log"] > 0.99
rep["criterion_pass"] = bool(rep["pass_alpha"] and rep["pass_R2_up_gt_0.99"])
OUT["i_reproduction_archive_numbers"] = rep

# ------------------------------------------------- (ii) independent data refit
indep = {"LD_indep_3_1_4_1_5_1": [round(v, 4) for v in LD_INDEP]}
for sec, m in (("up", M_UP_PDG), ("down", M_DN_PDG)):
    a, c, r2 = fit(LD_INDEP, m)
    indep[sec] = {"alpha": round(a, 4), "M0_MeV": float(np.exp(c)), "R2_log": round(r2, 6)}
top_sens = {}
for name, mt in M_TOP_VARIANTS.items():
    a, c, r2 = fit(LD_INDEP, np.array([M_UP_PDG[0], M_UP_PDG[1], mt]))
    top_sens[name] = {"alpha": round(a, 4), "R2_log": round(r2, 6)}
indep["top_scheme_sensitivity_up"] = top_sens
indep["criterion_pass"] = bool(indep["up"]["R2_log"] > 0.99 and indep["down"]["R2_log"] > 0.99)
OUT["ii_independent_refit"] = indep

# ---------------------------------------------------------- (iii) leave-one-out
def loo(x, m):
    out = []
    for k in range(3):
        idx = [j for j in range(3) if j != k]
        a, c = np.polyfit(np.asarray(x)[idx], np.log(np.asarray(m)[idx]), 1)
        pred = float(np.exp(a * x[k] + c))
        err_dex = float(np.log10(pred / m[k]))
        out.append({"excluded_index": k, "M_obs_MeV": float(m[k]),
                    "M_pred_MeV": pred, "log10_err_dex": round(err_dex, 3),
                    "factor_off": round(10 ** abs(err_dex), 2),
                    "fails_0.5dex": bool(abs(err_dex) > 0.5)})
    return out

loo_res = {}
for tag, x in (("a_archive_numbers", LD_ARCHIVE), ("b_independent", LD_INDEP)):
    masses = (M_UP_ARCH, M_DN_ARCH) if tag.startswith("a") else (M_UP_PDG, M_DN_PDG)
    quarks = (("up", "u c t"), ("down", "d s b"))
    res = {}
    for (sec, names), m in zip(quarks, masses):
        res[sec] = {"quarks": names, "loo": loo(x, m)}
    res["n_failed"] = sum(p["fails_0.5dex"] for s in ("up", "down") for p in res[s]["loo"])
    loo_res[tag] = res
loo_res["criterion_pass"] = bool(loo_res["b_independent"]["n_failed"] == 0)
OUT["iii_leave_one_out"] = loo_res

# ------------------------------------------------------- (iv) permutation null
names = list(KNOTS.keys())
rop = np.array([KNOTS[k] for k in names]) / 2.0  # L/D convention
n = len(names)
claimed_idx = [names.index("3_1"), names.index("4_1"), names.index("5_1")]

N_SAMPLE = 100_000
total = n * (n - 1) * (n - 2)
samp = np.empty((N_SAMPLE, 3), dtype=int)
for r in range(N_SAMPLE):
    samp[r] = rng.choice(n, size=3, replace=False)
X = rop[samp]

y_up = np.log(M_UP_PDG)
y_dn = np.log(M_DN_PDG)
r2_up = r2_vec(X, y_up)
r2_dn = r2_vec(X, y_dn)
mono = (X[:, 0] < X[:, 1]) & (X[:, 1] < X[:, 2])

x_claim = rop[claimed_idx]
_, _, r2c_up = fit(x_claim, M_UP_PDG)
_, _, r2c_dn = fit(x_claim, M_DN_PDG)

def null_stats(r2_null, r2_claim):
    n0 = len(r2_null)
    frac_ge = float(np.mean(r2_null >= r2_claim))
    return {"n": n0, "p95": round(float(np.percentile(r2_null, 95)), 6),
            "median": round(float(np.median(r2_null)), 6),
            "frac_null_ge_claimed": round(frac_ge, 5),
            "claimed_percentile": round(100 * (1 - frac_ge), 2),
            "frac_ge_0.99": round(float(np.mean(r2_null > 0.99)), 5),
            "claimed_beats_p95": bool(r2_claim > np.percentile(r2_null, 95))}

perm = {"table": "84 prime knots 3..9 crossings (ACPR)", "total_ordered_injective_triples": total,
        "sampled": N_SAMPLE, "seed": 12345,
        "claimed_R2_up": round(float(r2c_up), 6), "claimed_R2_down": round(float(r2c_dn), 6),
        "nullA_unrestricted": {"up": null_stats(r2_up, r2c_up), "down": null_stats(r2_dn, r2c_dn)},
        "nullB_monotone": {"n_monotone": int(mono.sum()),
                           "up": null_stats(r2_up[mono], r2c_up),
                           "down": null_stats(r2_dn[mono], r2c_dn)}}
perm["criterion_pass"] = bool(perm["nullB_monotone"]["up"]["claimed_beats_p95"]
                              and perm["nullB_monotone"]["down"]["claimed_beats_p95"])

# robustness only (not the pre-declared criterion): full enumeration
from itertools import permutations, combinations
comb = np.array(list(combinations(range(n), 3)))
Xm = rop[comb]  # combinations come out sorted by index; sort by ropelength value
Xm = np.sort(Xm, axis=1)  # monotone triples, all of them
perm["nullB_full_enumeration_robustness"] = {
    "n": len(Xm),
    "up": null_stats(r2_vec(Xm, y_up), r2c_up),
    "down": null_stats(r2_vec(Xm, y_dn), r2c_dn)}
OUT["iv_permutation_null"] = perm

# ------------------------------------------------------------------- verdict
OUT["verdict"] = {
    "i": rep["criterion_pass"], "ii": indep["criterion_pass"],
    "iii": loo_res["criterion_pass"], "iv": perm["criterion_pass"],
    "survives_as_formulated": bool(rep["criterion_pass"] and indep["criterion_pass"]
                                   and loo_res["criterion_pass"] and perm["criterion_pass"])}

json.dump(OUT, open("results.json", "w"), indent=1)
print(json.dumps(OUT, indent=1))
