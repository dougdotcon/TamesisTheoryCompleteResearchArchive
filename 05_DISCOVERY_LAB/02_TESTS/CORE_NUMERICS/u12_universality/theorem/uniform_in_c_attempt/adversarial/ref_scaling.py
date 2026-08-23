"""
Adversarial referee -- item 7: section 7 (the c = gamma n scaling regime),
plus a float64 precision audit and an independent Monte Carlo of the RAW
Definition-1 model.

Randomness: one use only (the Monte Carlo).  Fresh SeedSequence, entropy
recorded below and in the report.
"""

import math
import numpy as np
import mpmath as mp
from fractions import Fraction as F

from ref_engine import chain_phi, chain_phi_float

mp.mp.dps = 30

# ---------------------------------------------------------------- seed
ss = np.random.SeedSequence()
ENTROPY = ss.entropy
print(f"SeedSequence entropy = {ENTROPY}")
rng = np.random.default_rng(ss)

phi_inf = lambda c: float(mp.sqrt(mp.pi) / (2 * mp.sqrt(c)) * mp.erf(mp.sqrt(c))) \
    if c > 0 else 1.0

print()
print("=" * 76)
print("0. Precision audit of the float64 engine against exact Fractions")
print("=" * 76)
worst = 0.0
for n in (5, 10, 20, 40, 80):
    for q in (F(1, 10), F(1, 2), F(1)):
        ex = float(chain_phi(n, q))
        f64 = chain_phi_float(n, q)
        worst = max(worst, abs(ex - f64))
print(f"   max |exact - float64| over n in {{5,10,20,40,80}} x 3 q-values: "
      f"{worst:.3e}")
print("   (backward recursion has all-positive coefficients and values in")
print("    [0,1], so it is forward-stable; float64 is safe at n=4000.)")

print()
print("=" * 76)
print("1. Proposicao 7.1 -- phi(n,n) = Q(n)/n, and the sqrt(2) ratio")
print("=" * 76)
print("""
Re-derivation of the exact identity: at c=n Definition 1's convention gives
q = 1, so every point is rerouted and f(i) = U_i with U iid Uniform[n],
i.e. f is a UNIFORM RANDOM MAPPING.  The orbit of 1 returns to 1 at step j
iff f(1),...,f^{j-1}(1) are j-1 distinct points other than 1 and f^j(1)=1:
   P = [prod_{i=1}^{j-1} (n-i)/n] * (1/n).
Summing over j >= 1 gives (1/n) sum_{m>=0} prod_{i=1}^{m}(1-i/n) = Q(n)/n.
The events are disjoint (the return time is unique).  CORRECT; verified
exactly for n = 1..11 in ref_engine.py (11/11).
""")
print(f"   {'n':>7} {'sqrt(n) phi(n,n)':>18} {'sqrt(pi/2)-1/(3 sqrt n)':>24}")
for n in (100, 400, 1600, 6400):
    v = math.sqrt(n) * chain_phi_float(n, 1.0)
    pred = math.sqrt(math.pi / 2) - 1.0 / (3 * math.sqrt(n))
    print(f"   {n:7d} {v:18.6f} {pred:24.6f}")
print(f"   sqrt(pi/2) = {math.sqrt(math.pi/2):.6f}     "
      f"document's table: 1.220996, 1.236905, 1.245046, 1.249164")
astar = math.sqrt(math.pi) * (1 / math.sqrt(2) - 0.5)
print(f"   a* = sqrt(pi)(1/sqrt2 - 1/2) = {astar:.10f}   "
      f"(document: 0.3670872119)")

print()
print("=" * 76)
print("2. The c = gamma n table of ATTEMPT 7.2, recomputed independently")
print("=" * 76)
n = 4000
print(f"   n = {n} (own float64 (j,R) engine)")
print(f"   {'gamma':>6} {'sqrt(n) phi(n,gn)':>18} {'pred sqrt(pi/(2g(2-g)))':>24}"
      f" {'ratio phi/phi_inf':>18} {'pred sqrt(2/(2-g))':>19}")
for g in (0.05, 0.10, 0.25, 0.50, 0.75, 1.00):
    ph = chain_phi_float(n, g)
    c = g * n
    pi_ = phi_inf(c)
    pred1 = math.sqrt(math.pi / (2 * g * (2 - g)))
    pred2 = math.sqrt(2 / (2 - g))
    print(f"   {g:6.2f} {math.sqrt(n)*ph:18.6f} {pred1:24.6f} "
          f"{ph/pi_:18.6f} {pred2:19.6f}")
print("""
   Document's table (n=4000):
      0.05  4.006055  4.013818  1.010781  1.012739
      0.10  2.867677  2.875300  1.023258  1.025978
      0.25  1.887647  1.894833  1.064991  1.069045
      0.50  1.440789  1.447203  1.149583  1.154701
      0.75  1.288754  1.294417  1.259377  1.264911
      1.00  1.248070  1.253314  1.408296  1.414214
""")

print("=" * 76)
print("3. Re-derivation of the (7.1) heuristic -- is it internally coherent?")
print("=" * 76)
print("""
 With q = gamma fixed and j on scale sqrt(n) (so R ~ gamma j, n-j+R ~ n):
   return hazard  = gamma/n + (1-gamma)/(n-j+R)         -> 1/n
   fatal  hazard  = gamma j/n + (1-gamma) R/(n-j+R)     -> gamma(2-gamma) j/n
 so P(alive at J) ~ exp(-gamma(2-gamma) J^2/(2n)) and
   phi(n,gamma n) ~ (1/n) int_0^inf exp(-gamma(2-gamma)J^2/(2n)) dJ
                  = (1/(2n)) sqrt(2 pi n/(gamma(2-gamma)))
                  = n^{-1/2} sqrt(pi/(2 gamma(2-gamma))).
 Meanwhile phi_inf(gamma n) ~ (1/2)sqrt(pi/(gamma n)) = n^{-1/2} sqrt(pi/(4 gamma)),
 so the ratio -> sqrt(4 gamma/(2 gamma(2-gamma))) = sqrt(2/(2-gamma)).
 Consistency at the two ends: gamma->0 gives 1; gamma=1 gives sqrt2 and
 sqrt(pi/2) n^{-1/2}, reproducing the PROVED Prop 7.1.  Both check.
 c_eff = c(1-c/2n): phi_inf(c_eff)/phi_inf(c) ~ (1-gamma/2)^{-1/2}
                                              = sqrt(2/(2-gamma)).  Consistent.
 Small-gamma expansion: sqrt(2/(2-gamma)) = 1 + gamma/4 + O(gamma^2), i.e.
 relative error c/(4n); and from sec 5, e(c)/phi_inf(c) ~ (sqrt(pi c)/8)/
 (sqrt(pi)/(2 sqrt c)) = c/4, over n.  The two routes agree.  COHERENT.

 What is NOT supplied: concentration of R around gamma j, and a uniform
 Riemann-sum control of (1/n) sum_J prod(.).  The document says exactly
 this and labels the family NUMERICALLY CHARACTERIZED.  HONEST.
""")
print("   Numerical check of the two ingredients the heuristic assumes:")
for g in (0.25, 0.5, 1.0):
    pred = math.sqrt(2 / (2 - g))
    row = []
    for n in (500, 1000, 2000, 4000):
        ph = chain_phi_float(n, g)
        row.append(ph / phi_inf(g * n))
    rich = 2 * row[-1] - row[-2]     # 1/sqrt(n) corrections -> crude
    print(f"     gamma={g:4.2f}  ratios n=500..4000: "
          + " ".join(f"{x:.6f}" for x in row)
          + f"   -> predicted {pred:.6f}")

print()
print("=" * 76)
print("4. Section 7.3 -- where the global sup sits")
print("=" * 76)
print(f"   {'n':>6} {'sup_[0,n]|Delta_n|':>19} {'argmax c*/n':>12} "
      f"{'sqrt(n)*sup':>12}")
for n in (125, 250, 500, 1000, 2000, 4000):
    best, arg = 0.0, 0.0
    for i in range(0, 401):
        c = n * i / 400.0
        d = abs(chain_phi_float(n, min(c / n, 1.0)) - phi_inf(c))
        if d > best:
            best, arg = d, c / n
    print(f"   {n:6d} {best:19.6f} {arg:12.3f} {math.sqrt(n)*best:12.6f}")
print("   Document: 0.030239 0.021909 0.015759 0.011278 0.008043 0.005721,")
print("             argmax 1.000 throughout, sqrt(n)*sup -> a* = 0.3670872")
print()
print("   And the sup over ALL c >= 0 (phi is constant on [n,inf)):")
for n in (500, 2000, 4000):
    print(f"     n={n:5d}   lim_{{c->inf}} Delta_n(c) = phi(n,n) = "
          f"{chain_phi_float(n,1.0):.6f}   sqrt(n)*that = "
          f"{math.sqrt(n)*chain_phi_float(n,1.0):.6f}  (-> sqrt(pi/2)="
          f"{math.sqrt(math.pi/2):.6f})")
print("   -> the GLOBAL sup is ~sqrt(pi/2)/sqrt(n) = 1.2533/sqrt(n), which is")
print("      3.4x larger than sup over [0,n] (a*/sqrt n).  Both -> 0, so")
print("      Teorema C survives; the document says exactly this.  CONSISTENT.")

print()
print("=" * 76)
print("5. Independent Monte Carlo of the RAW Definition-1 model")
print("=" * 76)


def mc_phi(n, c, reps, rng):
    """P(1 cyclic) by simulating pi, xi, U directly.  Vectorised over reps."""
    q = min(c / n, 1.0)
    hits = 0
    B = 20000
    done = 0
    while done < reps:
        m = min(B, reps - done)
        done += m
        # build m independent mappings, but only follow the orbit of 0
        for _ in range(m):
            pi = rng.permutation(n)
            xi = rng.random(n) < q
            U = rng.integers(0, n, size=n)
            x = 0
            for _ in range(n):
                x = U[x] if xi[x] else pi[x]
                if x == 0:
                    hits += 1
                    break
    return hits / reps


print(f"   {'n':>4} {'c':>6} {'MC estimate':>13} {'+- 2 s.e.':>10} "
      f"{'exact chain':>13}  ok")
REPS = 200000
for (n, c) in [(6, 2.0), (10, 3.0), (12, 12.0), (20, 5.0), (30, 30.0)]:
    est = mc_phi(n, c, REPS, rng)
    se = math.sqrt(max(est * (1 - est), 1e-12) / REPS)
    ex = chain_phi_float(n, min(c / n, 1.0))
    ok = abs(est - ex) <= 3 * se + 1e-12
    print(f"   {n:4d} {c:6.1f} {est:13.6f} {2*se:10.6f} {ex:13.6f}  "
          f"{'OK' if ok else '*** DISCREPANT ***'}")
print()
print(f"   (seed entropy for this run: {ENTROPY})")
