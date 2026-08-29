"""
Script 04 -- empirical probe of the swapped m-sum's shape.

S_n' = sum_{m=0}^n term_m,  term_m := (gamma^m/n^m) * m! * T(n,m),
T(n,m) = sum_{j=0}^{n-m} C(j+m,m) C(n-j,m) (1-gamma)^j   (script 03).

Question this script answers (numerically, exact rational arithmetic,
fresh code): does term_m decay geometrically fast in m (so only
m = O(1) terms matter, which would make the swapped sum genuinely
EASIER than the original k-sum), or does it retain O(sqrt(n))-scale
structure (so the swap has merely relocated, not reduced, the
difficulty)?
"""
from fractions import Fraction
from math import comb

def T_exact(n_, m_, g: Fraction):
    total = Fraction(0)
    for j_ in range(0, n_ - m_ + 1):
        total += comb(j_ + m_, m_) * comb(n_ - j_, m_) * (1 - g)**j_
    return total

def term_m(n_, m_, g: Fraction):
    fact_m = 1
    for t in range(2, m_ + 1):
        fact_m *= t
    return (g**m_ / Fraction(n_)**m_) * fact_m * T_exact(n_, m_, g)

print("=== term_m profile vs m, several n, gamma=1/2 ===")
for n_val in [50, 200, 800]:
    g = Fraction(1, 2)
    print(f"  n={n_val}, gamma=1/2, sqrt(n)={n_val**0.5:.2f}:")
    vals = []
    for m_val in range(0, min(n_val, 60) + 1):
        tm = term_m(n_val, m_val, g)
        vals.append((m_val, float(tm)))
    # find argmax
    argmax_m, maxval = max(vals, key=lambda p: p[1])
    print(f"    argmax term_m at m={argmax_m}  (value={maxval:.6g})")
    for m_val, v in vals[:3] + vals[max(0,argmax_m-2):argmax_m+3] + vals[-3:]:
        pass
    # print a compact profile: m, term_m, cumulative fraction of total (partial)
    total_partial = sum(v for _, v in vals)
    cum = 0.0
    print(f"    {'m':>4} {'term_m':>14} {'term_m/max':>12}")
    for m_val, v in vals:
        if m_val <= 8 or abs(m_val - argmax_m) <= 3 or m_val >= len(vals) - 4:
            print(f"    {m_val:4d} {v:14.6g} {v/maxval:12.4f}")

print()
print("=== Does argmax(term_m) scale like sqrt(n)? ===")
g = Fraction(1, 2)
for n_val in [50, 100, 200, 400, 800, 1600]:
    best_m, best_v = 0, -1.0
    for m_val in range(0, min(n_val, 400) + 1):
        v = float(term_m(n_val, m_val, g))
        if v > best_v:
            best_v = v
            best_m = m_val
    print(f"  n={n_val:5d}: argmax_m={best_m:4d}   argmax_m/sqrt(n)={best_m/n_val**0.5:.4f}")

print()
print("=== Cross-check: does sum_m term_m (m up to n) match S_n' = S_n+1 "
      "at these n (sanity, small n only, reuse script 03 logic) ===")
def A_k_num(n_, k_, g: Fraction):
    total = Fraction(0)
    for m_ in range(0, k_ + 1):
        prod = Fraction(1)
        for i in range(1, m_ + 1):
            prod *= Fraction(n_ - (k_ - i), n_)
        total += comb(k_, m_) * g**m_ * (1 - g)**(k_ - m_) * prod
    return total

for n_val in [10, 15]:
    g = Fraction(1, 2)
    direct = sum(A_k_num(n_val, k_, g) for k_ in range(1, n_val + 1)) + 1
    swap = sum(term_m(n_val, m_val, g) for m_val in range(0, n_val + 1))
    print(f"  n={n_val}: direct={direct}  swap={swap}  match={direct==swap}")
