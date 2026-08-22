"""
Adversarial check (deterministic, no Monte Carlo): does M-WEIB(beta) sit
"genuinely outside" the M-q family, or is its observable phi(c) exactly
reproducible by SOME valid q(t) in [0,1] within the M-q master formula?

Independently derived (by hand, in ADVERSARIAL_NOTE.md, BEFORE writing
this script) closed form for the q(t) that would reproduce
H_q(t) = t^{1+beta} exactly:

    q(t) = [ (1+beta)*t**beta - beta*t**(1+beta) - t ] / (1 - t)

This script does two independent checks:
  1. Plug this q(t) into the ORIGINAL M-q master formula
     H_q(t) = t - (1-t) * integral_0^t (1-q(s))/(1-s) ds
     (numerically, via quadrature, NOT using the closed form shortcut)
     and confirm it reproduces t^{1+beta} for beta < 1.
  2. Scan q(t) over t in (0,1) for a range of beta (both <1 and >1) and
     report whether it stays inside [0,1] (valid probability) or leaves
     it (invalid -> genuinely outside M-q's reachable set).
"""
import numpy as np
from scipy import integrate
import json

def q_of_t(t, beta):
    t = np.asarray(t, dtype=float)
    with np.errstate(divide='ignore', invalid='ignore'):
        num = (1 + beta) * t**beta - beta * t**(1 + beta) - t
        q = num / (1 - t)
    return q

def q_limits(beta):
    # analytic limits derived by hand in ADVERSARIAL_NOTE.md
    q0 = 0.0 if beta > 0 else 1.0
    q1 = 1.0
    return q0, q1

def H_q_numeric(t, beta, n=20000):
    """H_q(t) = t - (1-t) * int_0^t (1-q(s))/(1-s) ds, via quadrature,
    using q(t) from the closed form above (independent numerical route
    from the closed-form H(t)=t^(1+beta) -- if they disagree, either the
    hand algebra for q(t) or the quadrature is wrong)."""
    if t <= 0:
        return 0.0

    def integrand(s):
        q = q_of_t(s, beta)
        return (1 - q) / (1 - s)

    # integrable end-point behavior: near s=0 integrand -> 1 (since q->0
    # for beta>0); near s=t<1 it's smooth. Use quad with points split.
    val, err = integrate.quad(integrand, 0, t, limit=200, points=None)
    return t - (1 - t) * val

def scan_beta(beta, t_grid):
    q_vals = q_of_t(t_grid, beta)
    q0, q1 = q_limits(beta)
    # replace endpoints (0/0 forms) with analytic limits for reporting
    lo = np.nanmin(q_vals)
    hi = np.nanmax(q_vals)
    valid = bool((np.nanmin(q_vals) >= -1e-9) and (np.nanmax(q_vals) <= 1 + 1e-9))
    return {
        "beta": beta,
        "q_min": float(lo),
        "q_max": float(hi),
        "q_at_0_limit": q0,
        "q_at_1_limit": q1,
        "valid_probability_everywhere": valid,
    }

def main():
    t_grid = np.linspace(1e-6, 1 - 1e-6, 4001)

    results = {"scan": [], "Hq_quadrature_check": []}

    print("=== Part 1: scan q(t) range for beta < 1 and beta > 1 ===")
    for beta in [0.1, 0.25, 0.4, 0.5, 0.6, 0.75, 0.9, 0.99, 1.0, 1.01, 1.1, 1.25, 1.5, 2.0, 3.0]:
        r = scan_beta(beta, t_grid)
        results["scan"].append(r)
        print(f"beta={beta:5.2f}  q_min={r['q_min']:+.6f}  q_max={r['q_max']:+.6f}  "
              f"valid_in_[0,1]={r['valid_probability_everywhere']}")

    print()
    print("=== Part 2: independent quadrature check of H_q(t) vs t^(1+beta) ===")
    print("(plugging closed-form q(t) into the ORIGINAL M-q integral definition,")
    print(" a route independent of the closed-form shortcut H(t)=t^(1+beta))")
    for beta in [0.25, 0.5, 0.75]:
        row = {"beta": beta, "points": []}
        max_abs_err = 0.0
        for t in [0.1, 0.3, 0.5, 0.7, 0.9, 0.99]:
            Hq = H_q_numeric(t, beta)
            target = t ** (1 + beta)
            err = abs(Hq - target)
            max_abs_err = max(max_abs_err, err)
            row["points"].append({"t": t, "H_q_numeric": Hq, "t^(1+beta)": target, "abs_err": err})
            print(f"beta={beta}  t={t:.2f}  H_q(numeric)={Hq:.8f}  t^(1+beta)={target:.8f}  err={err:.2e}")
        row["max_abs_err"] = max_abs_err
        results["Hq_quadrature_check"].append(row)

    with open("mq_equivalence_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nSaved mq_equivalence_results.json")

if __name__ == "__main__":
    main()
