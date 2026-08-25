#!/usr/bin/env python3
"""Machinery-free exact per-r moment surface over the raw 7776 configurations.

Fresh code; no prior front/referee script read or imported.

For EVERY raw redirect map g:{0..4} -> {0..4, OUT} (7776 configs), compute
E[M^p 1{config}] EXACTLY (fractions.Fraction throughout, no floats), using
ONLY the primitive model facts:
  - (m_1..m_5) uniform with density 5! on the simplex (Lemma 1),
  - destination i lands in region j with probability m_j (OUT: 1-sum m),
    landing offset uniform in the region, independent across i,
  - M = (1 - sum m) + sum_{j in C} (m_j - P_j)  =  1 - Q - sum_{j in C} P_j
    (the mechanism formula, itself independently verified per-configuration
    by mechanism_check_k5.py against ground-truth orbit tracing).
NO collapse machinery is used: no forest identity, no W=1-Q, no r-indexed
integral formula, no per-shape grouping — each of the 7776 configs is
integrated on its own, and only afterwards are the results summed by r_on.

Comparison targets (independent route): the exact integrals
int_0^1 x^p f_r(x) dx of the unified closed forms
f_r(x) = C(5,r) x^r (1-x)^4 [5-(5-r)(1-x)], for p = 0..10.
Since deg f_r <= 9, agreement at p = 0..9 pins each polynomial uniquely;
p = 10 is margin.
"""
import itertools
import json
from fractions import Fraction
from math import comb, factorial

K = 5
OUT = K
ok_all = True


def check(label, cond):
    global ok_all
    print(("PASS " if cond else "FAIL ") + label)
    if not cond:
        ok_all = False


def on_cycle_set(g):
    on = []
    for i in range(K):
        v = i
        for _ in range(K + 1):
            if v == OUT:
                break
            v = g[v]
            if v == i:
                on.append(i)
                break
    return tuple(on)


F = [Fraction(factorial(i)) for i in range(60)]


def mixed_integral(e_exp, T, q):
    """Exact  int_{Delta_5} prod m_i^{e_i} (1 - sum_{i in T} m_i)^q dm.

    Two-stage Dirichlet reduction (derived in ATTEMPT.md §5.3):
      = prod_i e_i! * (q + E_U + |U|)! / [ (E_U+|U|)! * (sum e + 5 + q)! ]
    with U = {0..4} \\ T, E_U = sum_{i in U} e_i.
    """
    U = [i for i in range(K) if i not in T]
    EU = sum(e_exp[i] for i in U)
    num = Fraction(1)
    for i in range(K):
        num *= F[e_exp[i]]
    num *= F[q + EU + len(U)]
    den = F[EU + len(U)] * F[sum(e_exp) + K + q]
    return num / den


def expand_out_power(a):
    """(1 - m0-..-m4)^a as list of (coeff Fraction, exponent 5-tuple)."""
    terms = []
    for ks in itertools.product(range(a + 1), repeat=K):
        s = sum(ks)
        if s > a:
            continue
        # multinomial coefficient a!/(k0!..k4!(a-s)!) with sign (-1)^s
        c = F[a]
        for kk in ks:
            c /= F[kk]
        c /= F[a - s]
        terms.append((Fraction((-1) ** s) * c, ks))
    return terms


PMAX = 10
# per-r accumulated moments, raw route
raw_moments = [[Fraction(0)] * (PMAX + 1) for _ in range(K + 1)]

for g in itertools.product(range(K + 1), repeat=K):
    C = on_cycle_set(g)
    r = len(C)
    off = [i for i in range(K) if i not in C]
    # off-target monomial: exponents on m_0..m_4, and OUT-power a
    base_exp = [0] * K
    a_out = 0
    for i in off:
        if g[i] == OUT:
            a_out += 1
        else:
            base_exp[g[i]] += 1
    off_set = frozenset(off)
    for p in range(PMAX + 1):
        # inner P-integration: terms (coeff, T, q) meaning
        # coeff * (1 - sum_{i in T} m_i)^q, starting from (1, off, p)
        terms = [(Fraction(1), off_set, p)]
        for j in C:
            new_terms = []
            for (c, T, q) in terms:
                c2 = c / (q + 1)
                new_terms.append((c2, T, q + 1))
                new_terms.append((-c2, T | {j}, q + 1))
            terms = new_terms
        tot = Fraction(0)
        if a_out == 0:
            for (c, T, q) in terms:
                tot += c * mixed_integral(base_exp, T, q)
        else:
            for (co, ks) in expand_out_power(a_out):
                e2 = [base_exp[i] + ks[i] for i in range(K)]
                # the OUT factor (1-sum_all m)^{...}: expanded into monomials,
                # so no second linear form remains
                for (c, T, q) in terms:
                    tot += co * c * mixed_integral(e2, T, q)
        raw_moments[r][p] += Fraction(factorial(K)) * tot

# ---------------- comparison targets: exact integrals of the unified f_r
# f_r(x) = C(5,r) x^r (1-x)^4 [5 - (5-r)(1-x)]
#        = C(5,r) [ 5 x^r (1-x)^4 - (5-r) x^r (1-x)^5 ]
# int_0^1 x^(p+r) (1-x)^b dx = (p+r)! b! / (p+r+b+1)!
def target_moment(r, p):
    t1 = Fraction(5) * F[p + r] * F[4] / F[p + r + 5]
    t2 = Fraction(5 - r) * F[p + r] * F[5] / F[p + r + 6]
    return Fraction(comb(5, r)) * (t1 - t2)


print("=" * 72)
print("raw-7776 exact moments vs unified-formula integrals, p=0..10, r=0..5")
results = {"per_r": {}, "totals": {}}
all_match = True
for r in range(K + 1):
    row_ok = True
    for p in range(PMAX + 1):
        raw = raw_moments[r][p]
        tgt = target_moment(r, p)
        if raw != tgt:
            row_ok = False
            all_match = False
            print(f"  MISMATCH r={r} p={p}: raw={raw} target={tgt}")
    results["per_r"][str(r)] = {str(p): str(raw_moments[r][p])
                                for p in range(PMAX + 1)}
    check(f"r={r}: all {PMAX+1} raw moments match the f_r integrals exactly",
          row_ok)

# totals vs 2Kx(1-x^2)^(K-1) moments: E[M^p] = K * B(p/2+1, K) — for even p
# rational; compare against sum of per-r raw moments and against the direct
# integral of the target density (as exact fraction via term expansion).
# target density expanded: 10x(1-x^2)^4 = sum_j 10*C(4,j)(-1)^j x^(2j+1)
tot_ok = True
for p in range(PMAX + 1):
    tot_raw = sum(raw_moments[r][p] for r in range(K + 1))
    tgt = Fraction(0)
    for j in range(5):
        tgt += Fraction(10 * comb(4, j) * (-1) ** j, 2 * j + 1 + p + 1)
    if tot_raw != tgt:
        tot_ok = False
        print(f"  TOTAL MISMATCH p={p}: raw={tot_raw} target={tgt}")
    results["totals"][str(p)] = str(tot_raw)
check("totals p=0..10 match the moments of 10x(1-x^2)^4 exactly", tot_ok)

# headline values
check("E[M5] = 256/693 (raw route)",
      sum(raw_moments[r][1] for r in range(K + 1)) == Fraction(256, 693))
check("E[M5^2] = 1/6 (raw route)",
      sum(raw_moments[r][2] for r in range(K + 1)) == Fraction(1, 6))
check("E[M5^3] = 256/3003 (raw route)",
      sum(raw_moments[r][3] for r in range(K + 1)) == Fraction(256, 3003))
check("P(r_on=r) raw = 1/6, 5/14, 25/84, 5/36, 1/28, 1/252",
      [raw_moments[r][0] for r in range(K + 1)] ==
      [Fraction(1, 6), Fraction(5, 14), Fraction(25, 84),
       Fraction(5, 36), Fraction(1, 28), Fraction(1, 252)])

with open("raw7776_exact_moments_k5.json", "w") as fh:
    json.dump(results, fh, indent=1)
print("=" * 72)
print("ALL CHECKS PASSED" if ok_all else "SOME CHECKS FAILED")
