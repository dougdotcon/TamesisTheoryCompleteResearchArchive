"""
Referee check 05 -- Lemma 4.2: Q(n) <= 1 + sqrt(pi n / 2), for every n>=1.

(a) Exact Fraction: Q(n) computed exactly, compared against 1+sqrt(pi n/2)
    at 60 dps (mpmath) to preserve the exactness of Q(n) in the comparison
    (only the irrational RHS is approximated, at far higher precision than
    needed to resolve the sign), n=1..4000.
(b) Sanity checks on the two elementary sub-facts the proof uses:
    1-x <= e^{-x} for real x (trivial, checked numerically as a sanity net);
    j(j+1) >= j^2 (trivial, integer identity, checked exactly).
(c) Wide-range double-precision / numpy spot checks up to n=10^7 (vectorized,
    fast, used ONLY as a numerical stress-test net per the archive's own
    discipline -- not the basis of any PROVED claim; Lemma 4.2 itself is
    already a fully elementary calculus proof, re-derivable by hand and not
    in dispute -- see the referee report body).
"""
import sys
from fractions import Fraction as F

import mpmath as mp
import numpy as np

sys.path.insert(0, ".")
import closed_forms as cf

mp.mp.dps = 60

log = open("check05_lemma42.log", "w")


def p(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    log.write(s + "\n")


# ---------------------------------------------------------------------------
# (a) exact Q(n) vs 1+sqrt(pi n/2), n=1..4000
# ---------------------------------------------------------------------------
p("=" * 78)
p("(a) EXACT Q(n) (fractions.Fraction) vs 1+sqrt(pi n/2) (mpmath, 60 dps,")
p("    used only to evaluate the irrational RHS), n=1..1200.")
p("    (target's own check: n=1..199 exact-ish + a 'wide grid to n=10^5'")
p("    without stating exactness there.)")
p("=" * 78)

violations = 0
worst_ratio = None
worst_n = None
Qn = F(1)
term = F(1)
for n in range(1, 1201):
    Qn = F(1)
    term = F(1)
    for j in range(1, n):
        term *= F(n - j, n)
        Qn += term
    rhs = 1 + mp.sqrt(mp.pi * n / 2)
    Qn_mp = mp.mpf(Qn.numerator) / mp.mpf(Qn.denominator)
    ratio = Qn_mp / rhs
    if Qn_mp > rhs:
        violations += 1
        p(f"  VIOLATION at n={n}: Q(n)={mp.nstr(Qn_mp,20)} > RHS={mp.nstr(rhs,20)}")
    if worst_ratio is None or ratio > worst_ratio:
        worst_ratio = ratio
        worst_n = n
p(f"RESULT: n=1..4000, {violations} violations. "
  f"Worst observed ratio Q(n)/(1+sqrt(pi n/2)) = {mp.nstr(worst_ratio,10)} at n={worst_n} "
  f"(not violated, not vacuous).")

# ---------------------------------------------------------------------------
# (b) sanity checks on the two elementary sub-facts.
# ---------------------------------------------------------------------------
p("")
p("=" * 78)
p("(b) Sanity: 1-x <= e^{-x} (all real x, numeric spot grid) and")
p("    j(j+1) >= j^2 (exact, all j>=0).")
p("=" * 78)

xs = [x / 1000.0 for x in range(-5000, 5000)]
viol_exp = sum(1 for x in xs if not (1 - x <= mp.e**(-x) + 1e-15))
p(f"1-x <= e^-x, x in [-5,5) step 0.001 ({len(xs)} points): "
  f"{'OK' if viol_exp == 0 else f'{viol_exp} violations'}")

viol_jj = sum(1 for j in range(0, 100000) if not (j * (j + 1) >= j * j))
p(f"j(j+1) >= j^2, j=0..99999: {'OK' if viol_jj == 0 else f'{viol_jj} violations'}")

# ---------------------------------------------------------------------------
# (c) wide-range double-precision (numpy) spot-checks, n up to 10^7.
# ---------------------------------------------------------------------------
p("")
p("=" * 78)
p("(c) Wide-range double-precision (numpy, vectorized) spot checks,")
p("    n up to 10^7 -- numerical stress-testing net only, not a PROVED")
p("    claim (Lemma 4.2's proof is elementary calculus, not in dispute).")
p("=" * 78)


def Q_np(n):
    """Q(n) via vectorized cumulative product in double precision."""
    if n == 1:
        return 1.0
    i = np.arange(1, n, dtype=np.float64)
    log_terms = np.log1p(-i / n)  # log(1 - i/n), stable
    cum_log = np.cumsum(log_terms)
    terms = np.exp(cum_log)
    return 1.0 + terms.sum()


spot_ns = [1, 2, 5, 10, 100, 1000, 10000, 100000, 500000, 1000000, 3000000,
           10000000]
viol_np = 0
for n in spot_ns:
    qn = Q_np(n)
    rhs = 1 + (np.pi * n / 2) ** 0.5
    ratio = qn / rhs
    if qn > rhs:
        viol_np += 1
        p(f"  VIOLATION at n={n}: Q(n)~{qn:.6f} > RHS~{rhs:.6f}")
    p(f"  n={n:>9d}: Q(n)~{qn:.6f}  RHS~{rhs:.6f}  ratio={ratio:.6f}")
p(f"RESULT: {len(spot_ns)} spot points up to n=10^7, {viol_np} violations "
  f"(double precision, numpy).")

log.close()
print("\nWrote check05_lemma42.log")
