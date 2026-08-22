"""Invert the empirical survival curve S_emp(t) (from
mclust_walk_diagnostic_results.json) to extract H_true(t) directly from
the mechanism:

    S(t) = (1-t) * exp(-c * H(t))   =>   H_true(t) = -ln(S_emp(t)/(1-t)) / c

and compare against wave 4's H_NEW(t,rho) and the pure-M-U t^2, to
characterize the FUNCTIONAL FORM of the gap (not just its size at the
integrated phi level).
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def H_NEW(t, rho):
    if rho < 1e-12:
        return t * t
    if t < 1e-13:
        return 0.0
    return t - (1.0 - t) * (t + rho * math.log(1.0 - t)) / (1.0 - rho)


with open(os.path.join(HERE, "mclust_walk_diagnostic_results.json")) as fh:
    d = json.load(fh)

results = {"cells": []}
for row in d["cells"]:
    n, b, c, rho = row["n"], row["b"], row["c"], row["rho"]
    nwalks = row["n_walks"]
    print(f"\n=== n={n} b={b} c={c} rho={rho:.4f} bc/n={b*c/n:.4f} ===")
    print(f"{'t':>6} {'S_emp':>8} {'H_true':>9} {'H_NEW':>9} {'t^2':>9} "
          f"{'H_true-H_NEW':>13} {'H_true-t^2':>11} {'ratio_to_rho*t^3':>17}")
    cell_out = []
    for i, t in enumerate(row["t_grid"]):
        s_emp = row["survival_empirical"][i]
        if s_emp <= 1e-6 or t >= 0.999:
            continue
        # SEM-based sanity: only trust bins with enough surviving mass
        n_surv = s_emp * nwalks
        if n_surv < 15:
            continue
        h_true = -math.log(s_emp / (1 - t)) / c
        h_new = H_NEW(t, rho)
        h_u = t * t
        diff_new = h_true - h_new
        diff_u = h_true - h_u
        ratio = diff_new / (rho * t ** 3) if t > 0 and rho > 0 else float("nan")
        print(f"{t:6.3f} {s_emp:8.4f} {h_true:9.5f} {h_new:9.5f} {h_u:9.5f} "
              f"{diff_new:+13.5f} {diff_u:+11.5f} {ratio:17.3f}")
        cell_out.append(dict(t=t, s_emp=s_emp, h_true=h_true, h_new=h_new,
                              h_u=h_u, diff_new=diff_new, diff_u=diff_u))
    results["cells"].append(dict(n=n, b=b, c=c, rho=rho, points=cell_out))

with open(os.path.join(HERE, "H_true_extracted.json"), "w") as fh:
    json.dump(results, fh, indent=2)
print("\nsaved H_true_extracted.json")
