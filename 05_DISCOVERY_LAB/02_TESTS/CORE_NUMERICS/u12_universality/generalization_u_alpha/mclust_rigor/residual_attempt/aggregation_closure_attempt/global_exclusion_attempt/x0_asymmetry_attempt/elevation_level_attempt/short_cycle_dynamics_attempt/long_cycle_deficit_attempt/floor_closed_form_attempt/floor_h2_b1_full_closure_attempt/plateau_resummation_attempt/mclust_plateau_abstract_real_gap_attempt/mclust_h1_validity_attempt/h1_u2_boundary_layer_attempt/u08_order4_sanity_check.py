"""
u08_order4_sanity_check.py

Sanity check at the KNOWN order (n=4, using gamma_4=17/3 -- already
symbolically PROVED to solve the record's own psi_4 ODE in
u01_symbolic_outer_expansion.py, not a conjecture): does
  resid4(x;eps) := (W_inf_numeric - W_pred3) / eps^4
converge to chi_4(x) = (13/6) R'''(x) as eps -> 0, at every tested point
(bridge x=1, and boundary-layer u=0,1,2,4)? This is the same numerical
data as u06/u07, one order down, testing a NON-speculative prediction --
run BEFORE trusting u07's speculative order-5 comparison against the
record's conjectured gamma_5.
"""
import pickle
from mpmath import mp, mpf, sqrt, pi, erfc, exp

mp.dps = 50


def erfcx(z):
    return exp(z * z) * erfc(z)


with open("u06_results.pkl", "rb") as f:
    raw = pickle.load(f)

results = []
for r0 in raw:
    r = {k: (mpf(v) if k not in ("label",) else v) for k, v in r0.items()}
    r["c"] = int(r0["c"])
    r["label"] = r0["label"]
    results.append(r)

labels = sorted(set(r["label"] for r in results), key=lambda s: (s != "bridge x=1", s))

print("=" * 90)
print("Order-4 check (KNOWN gamma_4=17/3): resid4 -> chi_4(x) = (13/6) R'''(x) ?")
print("=" * 90)

for label in labels:
    rows = sorted([r for r in results if r["label"] == label], key=lambda r: r["c"])
    print(f"\n{label}:")
    for r in rows:
        x = r["x"]
        eps = r["eps"]
        W_inf = r["W_inf"]

        z = x / sqrt(2)
        R0 = sqrt(pi / 2) * erfcx(z)
        R1 = x * R0 - 1
        R2 = x * R1 + R0
        R3 = x * R2 + 2 * R1

        W_pred3 = eps * R0 + eps**2 * R1 + eps**3 * (mpf(3) / 2) * R2
        resid4 = (W_inf - W_pred3) / eps**4
        chi4_pred = (mpf(13) / 6) * R3
        reldiff = (resid4 - chi4_pred) / chi4_pred if chi4_pred != 0 else resid4 - chi4_pred
        print(f"  c={r['c']:6d}  eps={float(eps):.4e}  resid4={float(resid4):.10f}  "
              f"chi4_pred={float(chi4_pred):.10f}  reldiff={float(reldiff):.4e}")
