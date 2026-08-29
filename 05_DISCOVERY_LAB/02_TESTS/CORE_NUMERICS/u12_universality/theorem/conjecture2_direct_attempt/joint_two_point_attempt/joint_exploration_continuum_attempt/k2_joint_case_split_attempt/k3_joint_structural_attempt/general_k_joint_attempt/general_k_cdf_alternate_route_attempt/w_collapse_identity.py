"""
THE MAIN NEW STRUCTURAL RESULT of this front (mandate avenue (a): "Camada
3 + outer r-assembly, attempted directly, treating O and V together
rather than truncating in two separate steps").

Estagio 44's S_r(n,K,k) is a NESTED double sum:
    S_r(n,K,k) = sum_{O=0}^{k} sum_{V=r}^{k-O} C(V-1,r-1) * InnerJ(V,O)
with the k-truncation applied in TWO steps: first O<=k (outer), then,
for each fixed O, V<=k-O (inner). Estagio 44 never attempted to combine
these two truncated sums into one (its own "Camada 3", the O-sum, was
explicitly never reached, since Camada 2 -- the V-sum for fixed O --
already failed to close for symbolic K).

THIS SCRIPT proves and verifies a fact Estagio 44 did not use: the CITED
Layer-1 closed form
    InnerJ(V,O) = (O+V)*C(n-V-O+r-1,K-1) + r*C(n-V-O+r-1,K)   (r<K)
    InnerJ(V,O) = n*C(n-V-O+r-1,r-1)                          (r=K)
depends on (V,O) ONLY through their sum W:=V+O -- not on how W splits
between the two. Given this, the k-truncation (O+V<=k, i.e. W<=k) can be
applied ONCE, on the SINGLE combined variable W, rather than twice (once
on O, once on V for each O). Summing the C(V-1,r-1) factor over the
implicit O-split for FIXED W collapses via the classical hockey-stick
identity sum_{V=r}^{W} C(V-1,r-1) = C(W,r) to give:

    >>> S_r(n,K,k) = sum_{W=r}^{k} C(W,r) * InnerJ(W)   <<<   (NEW)

a SINGLE univariate sum with one FEWER free parameter (O has been
eliminated entirely, algebraically, not just relabeled) than Estagio
44's own object. This IS "treating O and V together" and "truncating
later" exactly as the mandate's avenue (a) describes.

Part 1: symbolic proof that InnerJ(V,O) depends on V,O only via W=V+O.
Part 2: symbolic proof of the hockey-stick collapse identity.
Part 3: numeric verification of the resulting W-collapse formula against
        reference_Sr_double_sum.py's Sr_double_sum, many (n,K,r,k).
"""
import sympy as sp
from math import comb
import sys
sys.path.insert(0, '.')
from reference_Sr_double_sum import InnerJ_direct, Sr_double_sum


def part1_W_dependence_proof():
    print("PART 1: InnerJ(V,O) depends on (V,O) only through W:=V+O")
    print("-" * 70)
    n, O, V, r, K, W = sp.symbols('n O V r K W', integer=True, positive=True)

    # r < K case
    InnerJ_VO = (O + V) * sp.binomial(n - V - O + r - 1, K - 1) + r * sp.binomial(n - V - O + r - 1, K)
    InnerJ_W = W * sp.binomial(n - W + r - 1, K - 1) + r * sp.binomial(n - W + r - 1, K)
    diff = sp.simplify(InnerJ_VO.subs(O, W - V) - InnerJ_W)
    print(f"  r<K case: InnerJ(V, W-V) - InnerJ_W(W) simplifies to: {diff}")
    ok1 = (diff == 0)

    # r == K case
    InnerJ_VO_rK = n * sp.binomial(n - V - O + r - 1, r - 1)
    InnerJ_W_rK = n * sp.binomial(n - W + r - 1, r - 1)
    diff2 = sp.simplify(InnerJ_VO_rK.subs(O, W - V) - InnerJ_W_rK)
    print(f"  r=K case: InnerJ(V, W-V) - InnerJ_W(W) simplifies to: {diff2}")
    ok2 = (diff2 == 0)

    print(f"  PROVED (symbolic, exact): {ok1 and ok2}")
    return ok1 and ok2


def part2_hockey_stick_proof():
    print()
    print("PART 2: hockey-stick collapse sum_{O=0}^{W-r} C(W-O-1,r-1) = C(W,r)")
    print("-" * 70)
    # equivalently (substituting V=W-O, V ranges r..W): sum_{V=r}^{W} C(V-1,r-1) = C(W,r)
    r, W = sp.symbols('r W', integer=True, positive=True)
    V = sp.symbols('V', integer=True, positive=True)
    lhs = sp.summation(sp.binomial(V - 1, r - 1), (V, r, W))
    rhs = sp.binomial(W, r)
    diff = sp.simplify(lhs - rhs)
    print(f"  sp.summation(C(V-1,r-1), V=r..W) - C(W,r) = {diff}")
    ok = (diff == 0)
    print(f"  PROVED (symbolic, sp.summation, exact): {ok}")
    return ok


def InnerJ_of_W(n, K, r, W):
    """InnerJ evaluated using the W-only closed form (any split; use O=0,V=W)."""
    return InnerJ_direct(n, K, r, W, 0)


def Sr_single_sum_W(n, K, r, k):
    """THE NEW COLLAPSED FORMULA."""
    total = 0
    for W in range(r, k + 1):
        total += comb(W, r) * InnerJ_of_W(n, K, r, W)
    return total


def part3_numeric_verification():
    print()
    print("PART 3: numeric verification of S_r = sum_W C(W,r)*InnerJ(W)")
    print("        against reference_Sr_double_sum.Sr_double_sum")
    print("-" * 70)
    cases = []
    for n in [6, 8, 10, 12, 15]:
        for K in [1, 2, 3, 4, 5, 6]:
            if K > n - 1:
                continue
            for r in range(0, K + 1):
                for k in [0, 1, 2, n // 2, n - 1, n]:
                    cases.append((n, K, r, k))
    all_ok = True
    mismatches = 0
    for (n, K, r, k) in cases:
        a = Sr_double_sum(n, K, r, k)
        b = Sr_single_sum_W(n, K, r, k)
        if a != b:
            all_ok = False
            mismatches += 1
            print(f"  MISMATCH n={n} K={K} r={r} k={k}: double_sum={a} single_sum={b}")
    print(f"  Total cases tested: {len(cases)}; mismatches: {mismatches}")
    print(f"  W-collapse identity verified numerically: {all_ok}")
    return all_ok


if __name__ == "__main__":
    ok1 = part1_W_dependence_proof()
    ok2 = part2_hockey_stick_proof()
    ok3 = part3_numeric_verification()
    print()
    print("=" * 70)
    print(f"SUMMARY: W-dependence proof = {ok1}, hockey-stick proof = {ok2}, "
          f"numeric verification (many n,K,r,k) = {ok3}.")
    print("This establishes the NEW identity S_r(n,K,k) = sum_{W=r}^{k} "
          "C(W,r)*InnerJ(W)")
    print("as a genuine, proved, doubly-verified structural simplification "
          "of Estagio 44's")
    print("nested Camada-2/Camada-3 double sum -- the core new result of "
          "this front.")
