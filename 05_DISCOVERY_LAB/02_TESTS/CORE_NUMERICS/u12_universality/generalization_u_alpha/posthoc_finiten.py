"""POST-HOC analysis (declared as such) — front C, wave 3.

The pre-registered criteria C1/C3 FAILED for M-MIX50 and M-PREV at
large c (see ualpha_sim.log; that verdict stands as recorded). This
script re-compares the SAME Monte Carlo data (no new simulation, no
fitting) against finite-n targets amended by the O(c/n) additive term
that DERIVATIONS.md HAD identified before the simulations (Sec. 3.2:
"cyclic mass = reroute-free cycle mass + |R|/n"; Sec. 3.4: "+ 2|R|/n"
from the 2-cycles) but which predictions.py failed to carry into the
numeric targets — a pre-registration design deficiency, recorded
honestly in RESULTS_SUMMARY.md.

Amended finite-n targets (zero free parameters, q = c/n):
  M-PREV : phi_n(c) = (1-q)(1-(1-q)^n)/c + 2q(1-q)
           [exact free-cycle mass at finite n + two cyclic points per
            maximal backward run of rerouted points, run bottoms having
            density q(1-q); corrections O(q^2) neglected]
  M-MIX50: phi_n(c) = phi_MIX_inf(c) + p*q
           [self-loop reroutes are fixed points of f, density p*q;
            corrections O(q^2) and finite-n corrections to the main
            curve neglected]
"""
import json
import math
import os

from scipy.integrate import quad
from scipy.stats import chi2

HERE = os.path.dirname(os.path.abspath(__file__))
N = 32768
P = 0.5


def phi_mix_inf(c):
    return quad(lambda t: math.exp(-c * (P * t + (1 - P) * t * t)), 0, 1,
                epsabs=1e-14, epsrel=1e-13)[0]


def target_prev(c):
    q = c / N
    return (1 - q) * (1 - (1 - q) ** N) / c + 2 * q * (1 - q)


def target_mix(c):
    return phi_mix_inf(c) + P * c / N


def main():
    with open(os.path.join(HERE, "ualpha_results.json")) as fh:
        res = json.load(fh)
    out = {"label": "POST-HOC (declared); same MC data as ualpha_results.json",
           "mechanisms": {}}
    for mech, tf in [("M-PREV", target_prev), ("M-MIX50", target_mix)]:
        rows = []
        for r in res["runs"]["B1"][mech]:
            t = tf(r["c"])
            z = (r["phi"] - t) / r["sem"]
            rows.append(dict(c=r["c"], phi=r["phi"], sem=r["sem"],
                             target_amended=t, z=z))
            print("[POSTHOC] %-7s c=%-5g phi=%.6f+-%.6f amended=%.6f z=%+.2f"
                  % (mech, r["c"], r["phi"], r["sem"], t, z))
        chi = sum(x["z"] ** 2 for x in rows)
        pv = float(chi2.sf(chi, len(rows)))
        r10 = next(x for x in rows if x["c"] == 10.0)
        r160 = next(x for x in rows if x["c"] == 160.0)
        a_hat = math.log(r10["phi"] / r160["phi"]) / math.log(16.0)
        sig = math.sqrt((r10["sem"] / r10["phi"]) ** 2
                        + (r160["sem"] / r160["phi"]) ** 2) / math.log(16.0)
        a_tgt = math.log(r10["target_amended"] / r160["target_amended"]) \
            / math.log(16.0)
        print("[POSTHOC] %-7s chi2_5=%.2f p=%.4f | slope %.4f+-%.4f "
              "vs amended-target slope %.4f (dev %.1f sigma)"
              % (mech, chi, pv, a_hat, sig, a_tgt, abs(a_hat - a_tgt) / sig))
        out["mechanisms"][mech] = dict(
            rows=rows, chi2=chi, dof=len(rows), p=pv,
            slope_hat=a_hat, slope_sigma=sig, slope_amended_target=a_tgt)
    # crossover note: additive O(c/n) mass overtakes the ~1/c limit tail
    # when c ~ sqrt(n) ~ 181 at n=32768 — why c=160 exploded for U_1 rows.
    out["crossover_c_sqrt_n"] = math.sqrt(N)
    with open(os.path.join(HERE, "posthoc_finiten.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print("saved posthoc_finiten.json")


if __name__ == "__main__":
    main()
