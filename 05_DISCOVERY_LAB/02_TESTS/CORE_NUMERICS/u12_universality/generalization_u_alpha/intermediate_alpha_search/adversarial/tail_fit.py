"""Fit the tail exponent alpha from the (bug-fixed) sim_continuum.py
Monte Carlo results (log phi_hat vs log c, large-c points only) and
compare against the claimed alpha = 1/(1+beta)."""
import json
import numpy as np

with open("sim_continuum_results.json") as f:
    data = json.load(f)

rows = data["rows"]
by_beta = {}
for r in rows:
    by_beta.setdefault(r["beta"], []).append(r)

print(f"{'beta':>6} {'alpha_hat':>10} {'alpha_theory':>13} {'diff':>8}")
results = []
for beta, rs in sorted(by_beta.items()):
    rs = sorted(rs, key=lambda r: r["c"])
    # use the top half (largest c) for the tail fit
    n_use = max(3, len(rs) // 2)
    tail = rs[-n_use:]
    logc = np.log(np.array([r["c"] for r in tail]))
    logphi = np.log(np.array([r["phi_hat"] for r in tail]))
    slope, intercept = np.polyfit(logc, logphi, 1)
    alpha_hat = -slope
    alpha_theory = 1.0 / (1.0 + beta)
    diff = alpha_hat - alpha_theory
    print(f"{beta:6.2f} {alpha_hat:10.4f} {alpha_theory:13.4f} {diff:8.4f}")
    results.append(dict(beta=beta, alpha_hat=alpha_hat, alpha_theory=alpha_theory,
                         diff=diff, c_used=[r["c"] for r in tail]))

with open("tail_fit_results.json", "w") as f:
    json.dump(results, f, indent=2)
print("Saved tail_fit_results.json")
