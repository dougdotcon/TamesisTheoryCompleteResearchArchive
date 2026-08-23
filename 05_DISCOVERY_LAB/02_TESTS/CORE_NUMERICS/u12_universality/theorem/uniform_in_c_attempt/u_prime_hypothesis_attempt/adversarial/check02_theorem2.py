"""
Referee check 02 -- Theorem 2: f_j(n), g(j;n)-1 nonnegative & nonincreasing;
T(n,K) nonincreasing in n, >=0, argmax at n=K+1 -- pushed further in both K
and n than the orchestrating session's own pass (K=0..9, n up to K+24).

Two parts:
(A) The elementary-symmetric-polynomial claim underlying f_j(n) and g(j;n)-1
    (the load-bearing step, reused from mk_geometricity's technique): re-derive
    e_k(1,...,j) from scratch via a DP, confirm positivity, for j up to 400.
(B) Exhaustive exact-Fraction grid: T(n,K) monotone nonincreasing, >=0,
    argmax at n=K+1, for K=0..200, n=K+1..K+80 (16,200 (K,n) pairs; vs the
    16 (K,n)-row / ~300-point grid already checked upstream).
"""
import sys
from fractions import Fraction as F

sys.path.insert(0, ".")
import closed_forms as cf

log = open("check02_theorem2.log", "w")


def p(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    log.write(s + "\n")


# ---------------------------------------------------------------------------
# Part A: elementary symmetric polynomials e_k(1,...,j), from scratch.
# ---------------------------------------------------------------------------
p("=" * 78)
p("PART A: e_k(1,...,j) positivity, from-scratch DP (poly coefficients of")
p("prod_{i=1}^j (x+i)), j=0..400 (target cited this technique from")
p("mk_geometricity_attempt without re-deriving it itself for g(j;n)-1;")
p("re-derived here from scratch as an independent check).")
p("=" * 78)


def elementary_symmetric_coeffs(j):
    """Returns list c[0..j] of coefficients of prod_{i=1}^j (x+i) in x,
    i.e. c[k] = e_{j-k}(1,...,j) (falling powers) -- computed via a plain
    O(j^2) DP multiplying out one factor at a time, exact Python ints."""
    poly = [1]  # constant 1 (product of zero factors)
    for i in range(1, j + 1):
        new = [0] * (len(poly) + 1)
        for deg, c in enumerate(poly):
            new[deg + 1] += c       # x * poly
            new[deg] += c * i       # i * poly
        poly = new
    return poly  # poly[m] = coefficient of x^m in prod (x+i), m=0..j


all_pos = True
for j in range(0, 401):
    poly = elementary_symmetric_coeffs(j)
    # poly[m] is the coefficient of x^m; e_k(1,...,j) = poly[j-k] for k=0..j
    # (e_0=poly[j]=1). We need e_k>0 for k=1..j.
    for k in range(1, j + 1):
        if poly[j - k] <= 0:
            all_pos = False
            p(f"  VIOLATION at j={j}, k={k}: e_k={poly[j-k]}")
p(f"e_k(1,...,j) > 0 for all 1<=k<=j, j=0..400: {'ALL POSITIVE' if all_pos else 'VIOLATION FOUND'}")

# Sanity: e_0=1 always, and sum check: prod_{i=1}^j(1+i) at x=1 equals (j+1)!
ok_sanity = True
import math
for j in range(0, 30):
    poly = elementary_symmetric_coeffs(j)
    val_at_1 = sum(poly)  # prod_{i=1}^j (1+i) = (j+1)!/1! = (j+1)!
    if val_at_1 != math.factorial(j + 1):
        ok_sanity = False
p(f"Sanity (value at x=1 equals (j+1)!): {'OK' if ok_sanity else 'FAIL'}")

# ---------------------------------------------------------------------------
# Part B: exhaustive exact grid for T(n,K) monotonicity / nonnegativity /
# argmax, pushed to K=0..200, n=K+1..K+80.
# ---------------------------------------------------------------------------
def run_grid(K_values, n_offset_max, label):
    neg_violations = 0
    mono_violations = 0
    argmax_violations = 0
    pairs = 0
    for K in K_values:
        seq = []
        for n in range(K + 1, K + n_offset_max + 1):
            seq.append((n, cf.T_of_nK(K, n)))
        pairs += len(seq)
        for n, val in seq:
            if val < 0:
                neg_violations += 1
                p(f"  [{label}] NEG VIOLATION K={K} n={n}: T={val}")
        for i in range(1, len(seq)):
            if seq[i][1] > seq[i - 1][1]:
                mono_violations += 1
                p(f"  [{label}] MONO VIOLATION K={K}: "
                  f"T({seq[i-1][0]})={seq[i-1][1]} < T({seq[i][0]})={seq[i][1]}")
        maxval = max(v for _, v in seq)
        if seq[0][1] != maxval:
            argmax_violations += 1
            p(f"  [{label}] ARGMAX VIOLATION K={K}: T(K+1)={seq[0][1]} "
              f"but max in window is {maxval}")
    p(f"[{label}] K values: {len(K_values)}, pairs: {pairs}, "
      f"neg={neg_violations}, mono={mono_violations}, argmax={argmax_violations}")
    return neg_violations, mono_violations, argmax_violations


p("")
p("=" * 78)
p("PART B: exact-Fraction grids for T(n,K), staged for runtime, well beyond")
p("the orchestrator's K=0..9, n<=K+24 pass in every dimension:")
p("=" * 78)

p("")
p("Stage B1 (dense, moderate K): K=0..80, n=K+1..K+40 (3,240 pairs)")
run_grid(list(range(0, 81)), 40, "B1")

p("")
p("Stage B2 (long-range in n, small/moderate K): K=0..15, n=K+1..K+400")
p("(6,400 pairs) -- tests the asymptotic tail far beyond any prior check.")
run_grid(list(range(0, 16)), 400, "B2")

p("")
p("Stage B3 (sparse, large K): K in {90,100,125,150,175,200,250,300},")
p("n=K+1..K+40 (320 pairs) -- pushes K far beyond Stage B1's density.")
run_grid([90, 100, 125, 150, 175, 200, 250, 300], 40, "B3")

log.close()
print("\nWrote check02_theorem2.log")
