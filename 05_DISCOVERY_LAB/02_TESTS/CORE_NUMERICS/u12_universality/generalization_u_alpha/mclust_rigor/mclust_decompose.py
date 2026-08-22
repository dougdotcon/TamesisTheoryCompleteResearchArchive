"""Decomposition check (analytic only, reuses MC values already recorded
in mclust_validate_results.json -- no new simulation): isolates the two
corrections identified in DERIVATION_MCLUST_FIXED.md --

  RATE fix alone : phi_U(c)                (drop c_eff, use full rate c)
  CHAIN fix alone: chain-kill formula but with the OLD (wrong) rate c_eff
  BOTH (= phi_NEW): rate c + chain-kill/depletion q_CLUST(s)

against phi_OLD = phi_U(c_eff) and the recorded MC estimate, to show each
correction's independent contribution to closing the gap.
"""
import json
import math
import os

from scipy import integrate

HERE = os.path.dirname(os.path.abspath(__file__))


def phi_U(c):
    v, _ = integrate.quad(lambda t: math.exp(-c * t * t), 0, 1)
    return v


def H_chain(t, rho):
    if rho < 1e-12:
        return t * t
    if t < 1e-13:
        return 0.0
    return t - (1.0 - t) * (t + rho * math.log(1.0 - t)) / (1.0 - rho)


def main():
    d = json.load(open(os.path.join(HERE, "mclust_validate_results.json")))
    print(f"{'n':>7} {'b':>4} {'c':>7} {'rho':>7} | {'MC':>9} | "
          f"{'OLD dev%':>9} | {'RATEfix dev%':>12} | {'CHAINfix dev%':>13} | {'BOTH(NEW) dev%':>14}")
    for r in d["cells"]:
        n, b, c = r["n"], r["b"], r["c"]
        rho = r["rho_formula"]
        mc = r["phi_mc"]
        c_eff = c * (1 - c / n) ** b
        old = phi_U(c_eff)
        rate_fix_only = phi_U(c)
        v, _ = integrate.quad(lambda t: math.exp(-c_eff * H_chain(t, rho)), 0, 1, limit=200)
        chain_fix_only = v
        both = r["phi_new"]
        dev = lambda x: (mc - x) / x * 100
        print(f"{n:7d} {b:4d} {c:7.1f} {rho:7.4f} | {mc:9.6f} | "
              f"{dev(old):9.2f} | {dev(rate_fix_only):12.2f} | {dev(chain_fix_only):13.2f} | {dev(both):14.2f}")


if __name__ == "__main__":
    main()
