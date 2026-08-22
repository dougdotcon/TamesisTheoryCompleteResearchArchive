"""Analyze mclust_walk_diagnostic_results.json: compare empirical q(s)
(reroute kill probability) and empirical closure hazard (normal-step
landing-on-visited probability) against wave 4's assumed forms.

wave 4 assumed:
  q_CLUST(s) = s/(1-rho)                      [chain-kill, sec 3]
  closure hazard at a normal step, at visited-mass s: = s (UNCHANGED
    from M-U -- the master formula's (1-t)/(1-s) survival factor,
    "nao alterada" per sec 4).
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(HERE, "mclust_walk_diagnostic_results.json")) as fh:
    d = json.load(fh)

for row in d["cells"]:
    n, b, c, rho = row["n"], row["b"], row["c"], row["rho"]
    print(f"\n=== n={n} b={b} c={c} rho={rho:.4f} (phi_hat={row['phi_hat']:.5f}+-{row['sem']:.5f}) ===")
    print(f"{'s_mid':>6} | {'q_emp':>8} {'s/(1-rho)':>10} {'diff':>8} | "
          f"{'cont_emp':>9} {'rho':>7} {'diff':>8} | {'clo_emp':>8} {'s':>7} {'diff':>8} | {'n_reroute':>9} {'n_normal':>9}")
    for i, s in enumerate(row["bin_mid"]):
        q_emp = row["q_empirical"][i]
        cont_emp = row["cont_empirical"][i]
        clo_emp = row["closure_hazard_empirical"][i]
        nreroute = row["reroute_total"][i]
        nnormal = row["normal_total"][i]
        q_pred = s / (1 - rho) if rho < 1 else float("nan")
        clo_pred = s
        if nreroute < 20 and nnormal < 20:
            continue
        qs = f"{q_emp:8.4f}" if q_emp == q_emp else "     nan"
        qd = f"{(q_emp - q_pred):+8.4f}" if q_emp == q_emp else "     nan"
        cs = f"{cont_emp:9.4f}" if cont_emp == cont_emp else "      nan"
        cd = f"{(cont_emp - rho):+8.4f}" if cont_emp == cont_emp else "     nan"
        cls = f"{clo_emp:8.4f}" if clo_emp == clo_emp else "     nan"
        cld = f"{(clo_emp - clo_pred):+8.4f}" if clo_emp == clo_emp else "     nan"
        print(f"{s:6.3f} | {qs} {q_pred:10.4f} {qd} | {cs} {rho:7.4f} {cd} | {cls} {clo_pred:7.4f} {cld} | {nreroute:9.0f} {nnormal:9.0f}")
