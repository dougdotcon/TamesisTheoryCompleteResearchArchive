"""Second-pass analysis of mclust_walk_diagnostic_results.json:
  (a) per-DRAW kill probability q_emp(s) vs s (wave 4's per-draw kill
      prob, UNCHANGED from M-U) -- corrects stage-D's first analysis,
      which mistakenly compared q_emp against the CHAIN-AGGREGATE
      s/(1-rho) instead of the per-draw s.
  (b) CHAIN-level (i.e. per reroute EVENT, not per draw) eventual-kill
      probability chain_kill_prob(s) vs wave 4's q_CLUST(s)=s/(1-rho)
      -- the correct comparison for sec 3's derived formula.
  (c) empirical survival curve S(t)=P(final visited mass >= t) vs
      wave 4's E[S(t)] = (1-t) exp(-c H_NEW(t,rho)) -- the single most
      direct test of the whole formula, sidestepping any hazard/hidden-
      hazard bookkeeping subtlety entirely.
"""
import json
import math
import os

from scipy import integrate

HERE = os.path.dirname(os.path.abspath(__file__))


def H_NEW(t, rho):
    if rho < 1e-12:
        return t * t
    if t < 1e-13:
        return 0.0
    return t - (1.0 - t) * (t + rho * math.log(1.0 - t)) / (1.0 - rho)


with open(os.path.join(HERE, "mclust_walk_diagnostic_results.json")) as fh:
    d = json.load(fh)

for row in d["cells"]:
    n, b, c, rho = row["n"], row["b"], row["c"], row["rho"]
    print(f"\n=== n={n} b={b} c={c} rho={rho:.4f} (phi_hat={row['phi_hat']:.5f}+-{row['sem']:.5f}) ===")
    print("-- (a) per-draw kill prob q_emp(s) vs s --")
    print(f"{'s_mid':>6} {'q_emp':>8} {'s':>7} {'diff':>8} {'sigma':>7} {'n':>8}")
    for i, s in enumerate(row["bin_mid"]):
        q_emp = row["q_empirical"][i]
        nreroute = row["reroute_total"][i]
        if nreroute < 30 or q_emp != q_emp:
            continue
        sem_q = math.sqrt(max(q_emp * (1 - q_emp), 1e-9) / nreroute)
        diff = q_emp - s
        print(f"{s:6.3f} {q_emp:8.4f} {s:7.4f} {diff:+8.4f} {diff/sem_q:+7.2f} {nreroute:8.0f}")

    print("-- (b) chain-level eventual-kill prob vs s/(1-rho) [wave-4 q_CLUST] --")
    print(f"{'s_mid':>6} {'chain_kill':>10} {'s/(1-rho)':>10} {'diff':>8} {'sigma':>7} {'n':>8}")
    for i, s in enumerate(row["bin_mid"]):
        ck = row["chain_kill_prob"][i]
        nchain = row["chain_total"][i]
        if nchain < 15 or ck != ck:
            continue
        pred = s / (1 - rho)
        sem_c = math.sqrt(max(ck * (1 - ck), 1e-9) / nchain)
        diff = ck - pred
        print(f"{s:6.3f} {ck:10.4f} {pred:10.4f} {diff:+8.4f} {diff/sem_c:+7.2f} {nchain:8.0f}")

    print("-- (c) survival curve S(t) empirical vs wave-4 phi_NEW's E[S(t)] --")
    print(f"{'t':>6} {'S_emp':>8} {'S_pred(NEW)':>11} {'diff':>8} {'sigma':>7}")
    t_grid = row["t_grid"]
    surv = row["survival_empirical"]
    nwalks = row["n_walks"]
    for i in range(0, len(t_grid), 4):
        t = t_grid[i]
        s_emp = surv[i]
        s_pred = (1 - t) * math.exp(-c * H_NEW(t, rho))
        sem_s = math.sqrt(max(s_emp * (1 - s_emp), 1e-9) / nwalks)
        diff = s_emp - s_pred
        sig = diff / sem_s if sem_s > 0 else float("nan")
        print(f"{t:6.3f} {s_emp:8.4f} {s_pred:11.4f} {diff:+8.4f} {sig:+7.2f}")
