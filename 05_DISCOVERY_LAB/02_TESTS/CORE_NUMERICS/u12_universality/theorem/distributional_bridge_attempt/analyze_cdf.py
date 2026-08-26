"""
Analyze exact_enumeration_results.json:
  (a) verify the derived closed form F_n^{(1)}(k/n) = k(k+1)/n^2 (ATTEMPT.md
      Proposition D1) against the exact enumerated CDF, for every cell and
      every k;
  (b) for K=2,3, compute the Kolmogorov-type statistic
      D(n,K) := max_{k=0,...,n} |F_n^{(K)}(k/n) - F_K(k/n)|,
      F_K(x) = 1-(1-x^2)^K, and report the trend as n grows (numerical
      evidence only, not a proof, for the still-open K>=2 fixed-K CDF
      bridge).
"""
import json
from fractions import Fraction

with open("exact_enumeration_results.json") as fh:
    results = json.load(fh)

print("=== (a) K=1 closed-form check: F_n^{(1)}(k/n) =?= k(k+1)/n^2 ===")
for r in results:
    if r["K"] != 1:
        continue
    n = r["n"]
    cdf = r["cdf_at_k_over_n"]
    max_abs_diff = Fraction(0)
    for k in range(n + 1):
        actual = Fraction(cdf[str(k)])
        if k == n:
            predicted = Fraction(1)
        else:
            predicted = Fraction(k * (k + 1), n * n)
        d = abs(actual - predicted)
        if d > max_abs_diff:
            max_abs_diff = d
    status = "EXACT MATCH" if max_abs_diff == 0 else f"MISMATCH max|diff|={max_abs_diff}"
    print(f"  n={n:2d}: {status}")

print()
print("=== (b) K=2,3 Kolmogorov-type statistic D(n,K) vs target F_K(x)=1-(1-x^2)^K ===")
for K in (2, 3):
    print(f" K={K}:")
    for r in results:
        if r["K"] != K:
            continue
        n = r["n"]
        cdf = r["cdf_at_k_over_n"]
        worst = 0.0
        worst_k = None
        for k in range(n + 1):
            x = k / n
            actual = float(Fraction(cdf[str(k)]))
            target = 1 - (1 - x ** 2) ** K
            d = abs(actual - target)
            if d > worst:
                worst = d
                worst_k = k
        print(f"   n={n:2d}: D={worst:.5f}  n*D={n*worst:.4f}  (worst at k={worst_k}, x={worst_k/n:.3f})")

print()
print("=== (c) P_nn(n,K) trend vs target 1/(K+1) ===")
for K in (1, 2, 3):
    target = 1.0 / (K + 1)
    print(f" K={K}  target 1/(K+1)={target:.6f}")
    for r in results:
        if r["K"] != K or "P_nn_float" not in r:
            continue
        n = r["n"]
        p = r["P_nn_float"]
        print(f"   n={n:2d}: P_nn={p:.6f}  gap={p-target:+.6f}  n*gap={n*(p-target):+.4f}")

print()
print("=== (d) K=1 exact closed form for P_nn(n,1) check: conjectured 1/2 + 1/(6n) ===")
for r in results:
    if r["K"] != 1 or "P_nn" not in r:
        continue
    n = r["n"]
    actual = Fraction(r["P_nn"])
    predicted = Fraction(1, 2) + Fraction(1, 6 * n)
    status = "EXACT MATCH" if actual == predicted else f"MISMATCH actual={actual} predicted={predicted}"
    print(f"  n={n:2d}: {status}")

print()
print("=== (e) Corollary D1.2: E[(M_n^{(1)})^2] =?= 1/2 + 1/(2n^2) ===")
for r in results:
    if r["K"] != 1:
        continue
    n = r["n"]
    dist = {int(t): Fraction(p) for t, p in r["dist_T"].items()}
    ET2 = sum(Fraction(t) ** 2 * p for t, p in dist.items())
    EM2 = ET2 / (n * n)
    predicted = Fraction(1, 2) + Fraction(1, 2 * n * n)
    status = "EXACT MATCH" if EM2 == predicted else f"MISMATCH actual={EM2} predicted={predicted}"
    print(f"  n={n:2d}: {status}")

print()
print("=== (f) Lemma P2 exact identity: E[(M_n^(K))^2] =?= phi_n^(K)/n + coeff_nn*P_nn + coeff_nr*P_nr + coeff_rr*P_rr ===")
n_checked = 0
n_match = 0
for r in results:
    n, K = r["n"], r["K"]
    if "P_nn" not in r:
        continue
    n_checked += 1
    dist = {int(t): Fraction(p) for t, p in r["dist_T"].items()}
    ET2 = sum(Fraction(t) ** 2 * p for t, p in dist.items())
    EM2_direct = ET2 / (n * n)
    mean = sum(Fraction(t) * p for t, p in dist.items()) / n
    Pnn = Fraction(r["P_nn"])
    Pnr = Fraction(r["P_nr"]) if "P_nr" in r else Fraction(0)
    Prr = Fraction(r["P_rr"]) if "P_rr" in r else Fraction(0)
    coeff_nn = Fraction((n - K) * (n - K - 1), n * n)
    coeff_nr = Fraction(2 * K * (n - K), n * n)
    coeff_rr = Fraction(K * (K - 1), n * n)
    EM2_formula = mean / n + coeff_nn * Pnn + coeff_nr * Pnr + coeff_rr * Prr
    ok = (EM2_direct == EM2_formula)
    n_match += int(ok)
    status = "MATCH" if ok else f"MISMATCH direct={EM2_direct} formula={EM2_formula}"
    print(f"  n={n:2d} K={K}: {status}")
print(f"  -> {n_match}/{n_checked} cells match exactly")
