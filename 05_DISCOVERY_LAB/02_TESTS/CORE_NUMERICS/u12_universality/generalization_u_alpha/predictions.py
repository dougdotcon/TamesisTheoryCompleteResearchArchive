"""Front C (u12-generalization-u-alpha, wave 3): pre-simulation targets.

Tabulates, by quadrature of the DERIVED formulas of DERIVATIONS.md
(no simulation, no fitting), the comparison targets pre-declared in
METHODOLOGY_NOTE.md:

  - phi_U(c) = int_0^1 exp(-c t^2) dt                    (M-U, M-CLUST limit)
  - phi_CLUST target at n=32768, b=8: phi_U(c*(1-c/n)^b) (finite-n corrected)
  - phi_MIX(p=1/2): int_0^1 exp(-c(pt+(1-p)t^2)) dt
  - phi_PREV = phi_SELF = (1-exp(-c))/c
  - exact K=1 battery: 2/3, 7/12, 1/2, 3/4
  - predicted slopes ln(phi(10)/phi(160))/ln(16) per mechanism
  - M-INTRA heuristic tail sqrt(pi)*c^(-1/2) (report-only, labeled)

Run BEFORE ualpha_sim.py (timestamps verifiable).
"""
import json
import math
import os

from scipy.integrate import quad

N_SIM = 32768
B = 8
P = 0.5
C_GRID = [0.5, 2.0, 10.0, 40.0, 160.0]


def phi_U(c):
    return 0.5 * math.sqrt(math.pi / c) * math.erf(math.sqrt(c)) if c > 0 else 1.0


def phi_MIX(c, p=P):
    val, _ = quad(lambda t: math.exp(-c * (p * t + (1 - p) * t * t)), 0.0, 1.0,
                  epsabs=1e-14, epsrel=1e-13)
    return val


def phi_PREV(c):
    return (1.0 - math.exp(-c)) / c


def slope(f10, f160):
    return math.log(f10 / f160) / math.log(16.0)


def main():
    out = {"n_sim": N_SIM, "b": B, "p": P, "c_grid": C_GRID, "targets": {}}
    t = out["targets"]
    t["M-U"] = {str(c): phi_U(c) for c in C_GRID}
    t["M-CLUST8"] = {str(c): phi_U(c * (1.0 - c / N_SIM) ** B) for c in C_GRID}
    t["M-MIX50"] = {str(c): phi_MIX(c) for c in C_GRID}
    t["M-PREV"] = {str(c): phi_PREV(c) for c in C_GRID}
    t["M-SELF"] = t["M-PREV"]
    out["K1_exact"] = {"M-U": 2.0 / 3.0, "M-MIX50": 7.0 / 12.0,
                       "M-PREV": 0.5, "M-INTRA": 0.75}
    out["slope_targets"] = {
        "M-U": slope(t["M-U"]["10.0"], t["M-U"]["160.0"]),
        "M-CLUST8": slope(t["M-CLUST8"]["10.0"], t["M-CLUST8"]["160.0"]),
        "M-MIX50": slope(t["M-MIX50"]["10.0"], t["M-MIX50"]["160.0"]),
        "M-PREV": slope(t["M-PREV"]["10.0"], t["M-PREV"]["160.0"]),
        "M-INTRA": 0.5,  # heuristic class prediction (DERIVATIONS.md 3.6)
    }
    out["M-INTRA_heuristic_tail_coeff"] = math.sqrt(math.pi)  # report-only
    out["M-INTRA_heuristic_phi"] = {
        str(c): min(1.0, quad(
            lambda l: min(1.0, 0.5 * math.sqrt(math.pi / (c * l))), 0, 1,
            epsabs=1e-12)[0]) for c in C_GRID}  # report-only, labeled heuristic
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "predictions.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    for m in ["M-U", "M-CLUST8", "M-MIX50", "M-PREV"]:
        print(m, {c: round(t[m][str(c)], 6) for c in C_GRID})
    print("slopes", {k: round(v, 4) for k, v in out["slope_targets"].items()})
    print("K1", out["K1_exact"])
    print("intra heuristic phi (report-only)",
          {c: round(out["M-INTRA_heuristic_phi"][str(c)], 4) for c in C_GRID})


if __name__ == "__main__":
    main()
