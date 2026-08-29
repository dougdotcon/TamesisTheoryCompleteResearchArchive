"""
K6-EXACT-CLOSURE-ATTEMPT (wave 30, front b).

Derives Proposicao D6 (the exact finite-n CDF of M_n^{(6)}) from scratch,
by instantiating -- at the concrete integer K=6 -- the general-K
machinery PROVED (for every K, symbolic) in two cited, already-proved
ancestor documents (read in full, not re-derived, per this front's
mandate):

  - THEOREM.md Estagio 41 (source: general_k_decomposition_attempt/
    ATTEMPT.md, Sections 2-3): Proposicao S (the law of S, the random
    set of "cyclic" reroute sources among the K reroute sources) and the
    Full Cycle-Count Decomposition Theorem T = O + sum_{s in S} V_s,
    both proved K-free (no dependence on the value of K anywhere in
    their proofs).

  - THEOREM.md Estagio 44 (source: general_k_closed_cdf_attempt/
    ATTEMPT.md, Sections 2-4): the exchangeability reduction of the
    2^K-subset sum to a sum over subset SIZE r = 0,...,K of a quantity
    S_r(n,K,k), and Layer 1's closed form for InnerJ(V,O) -- the result
    of marginalizing the K-r "untouched" reroute sources for a FIXED
    total V among the r touched ones. Both cited as PROVED there,
    symbolic in (n,K,r).

Boxed formulas used (transcribed by hand from the two ATTEMPT.md files
above; both cited as already PROVED, never re-derived here):

    P(T<=k) = (1/C(n,K)) * sum_{r=0}^{K} C(K,r) * r!/n^{r+1} * S_r(n,K,k)

    S_r(n,K,k) = sum_{O=0}^{k} sum_{V=r}^{t} C(V-1,r-1) * InnerJ(V,O),
                 t := k - O

    InnerJ(V,O) = (O+V)*C(N+r-1,K-1) + r*C(N+r-1,K),  N := n-V-O   (r<K)
    InnerJ(V,O) = n * C(N+r-1,r-1),                    N := n-V-O   (r=K)

What THIS script adds, fresh (an observation independently re-verified
below, not merely asserted): once K is a CONCRETE integer, InnerJ(V,O)
is an explicit polynomial in V of bounded degree, so the r=0 special
case aside, both the V-sum and O-sum below are ordinary polynomial
(Faulhaber-type) sums that sp.summation closes exactly and immediately
-- no Gosper machinery needed (the symbolic-K obstruction proved by
Estagio 44/45 lives entirely in InnerJ's degree depending on the free
symbol K; fixing K removes it). This is exactly the route the K=5 front
(the immediate predecessor of this one) used to derive Proposicao D5;
this script uses the identical general recipe, written completely
independently (own variable names, own control flow, own r=0 handling
derived from first principles below -- see `s_r_of` docstring), pushed
one degree further to K=6.

MANDATORY SELF-VALIDATION, done BEFORE trusting the K=6 output: the
identical, unmodified pipeline is run at K=1,2,3,4,5 and checked, via
exact sp.simplify, against the ALREADY-PROVED closed forms Proposicao D1
(Estagio 27), D2 (Estagio 42), D3 (Estagio 40), D4 (Estagio 43) --
transcribed by hand from THEOREM.md -- and Proposicao D5 (the immediate
predecessor front's own new derivation, THEOREM.md Estagio 53 /
k5_exact_closure_attempt/ATTEMPT.md Section 3.3), transcribed by hand
from that ATTEMPT.md and cited, not blindly trusted -- it is itself
being spot-checked here by an independent re-derivation via the same
general machinery.
"""
import time
import sympy as sp

n, k = sp.symbols('n k')


def falling_choose(x, r):
    """Explicit expanded polynomial for C(x, r) with r a concrete
    (possibly negative) integer: the standard combinatorial convention
    C(x, r) = 0 for r < 0, C(x, 0) = 1, C(x, r) = x(x-1)...(x-r+1)/r!
    for r > 0. Building the product by hand (rather than sp.binomial)
    avoids sympy's slow generic symbolic-binomial-inside-summation
    codepath -- the exact performance lesson the predecessor front
    (K=5) disclosed self-catching."""
    if r < 0:
        return sp.Integer(0)
    if r == 0:
        return sp.Integer(1)
    prod = sp.Integer(1)
    for i in range(r):
        prod *= (x - i)
    return sp.expand(prod / sp.factorial(r))


def inner_j(V, O, r, K, n_):
    """InnerJ(V,O), the Layer-1 closed form (Estagio 44, cited)."""
    N = n_ - V - O
    if r < K:
        return sp.expand(
            (O + V) * falling_choose(N + r - 1, K - 1)
            + r * falling_choose(N + r - 1, K)
        )
    # r == K
    return sp.expand(n_ * falling_choose(N + r - 1, r - 1))


def s_r_of(K, r, n_, k_):
    """S_r(n,K,k) (Estagio 44 Section 2-3, cited), for a concrete
    subset size r.

    r=0 special case, derived here from first principles (not merely
    quoted): with r=0 there are no "touched" sources, so the touched
    total V is forced to 0 and Count_0(;t) is the trivial indicator
    1[t>=0] -- always 1 in the range O=0..k used below, since
    t=k-O>=0 there. So S_0(n,K,k) reduces to a single evaluation of
    InnerJ at V=0, summed only over O:
        S_0(n,K,k) = sum_{O=0}^{k} InnerJ(0, O, r=0, K, n)
    which, expanding InnerJ's r<K branch at r=0, V=0, is exactly
    sum_{O=0}^{k} O * C(n-O-1, K-1) -- the elementary "O outside points
    weighted by how many ways the K untouched sources' gaps can fill
    the rest" count. This matches (independently re-derived, not
    copied) the same reduction the K=5 predecessor front reports having
    used.
    """
    O_ = sp.Symbol('O_', integer=True)
    if r == 0:
        summand = inner_j(0, O_, 0, K, n_)
        return sp.factor(sp.expand(sp.summation(summand, (O_, 0, k_))))
    V_ = sp.Symbol('V_', integer=True)
    t_ = k_ - O_
    v_summand = sp.expand(falling_choose(V_ - 1, r - 1) * inner_j(V_, O_, r, K, n_))
    v_summed = sp.expand(sp.summation(v_summand, (V_, r, t_)))
    o_summed = sp.summation(v_summed, (O_, 0, k_))
    return sp.factor(sp.expand(o_summed))


def cdf(K, n_, k_, verbose=False):
    total = sp.Integer(0)
    for r in range(K + 1):
        t0 = time.time()
        Sr = s_r_of(K, r, n_, k_)
        if verbose:
            print(f"    S_{r}(n,{K},k) done in {time.time()-t0:.2f}s", flush=True)
        total += sp.binomial(K, r) * sp.factorial(r) / n_ ** (r + 1) * Sr
    total = total / sp.binomial(n_, K)
    return sp.factor(sp.cancel(sp.together(total)))


if __name__ == "__main__":
    print("=" * 78)
    print("SELF-VALIDATION: reproduce D1, D2, D3, D4, D5 EXACTLY (symbolic)")
    print("=" * 78)
    t_start = time.time()

    D1 = k * (k + 1) / n ** 2
    F1 = cdf(1, n, k)
    assert sp.simplify(F1 - D1) == 0
    print("K=1 vs Proposicao D1 (Estagio 27): EXACT MATCH (diff=0).")

    D2 = k * (k + 1) * (2 * n ** 2 - 3 * n + k - k ** 2) / (n ** 3 * (n - 1))
    F2 = cdf(2, n, k)
    assert sp.simplify(F2 - D2) == 0
    print("K=2 vs Proposicao D2 (Estagio 42): EXACT MATCH (diff=0).")

    D3 = (k * (k + 1) * (
        k ** 4 - 4 * k ** 3 - (3 * n ** 2 - 9 * n - 5) * k ** 2
        + (3 * n ** 2 - 11 * n - 2) * k
        + (3 * n ** 4 - 12 * n ** 3 + 12 * n ** 2 + 2 * n)
    ) / (n ** 4 * (n - 1) * (n - 2)))
    F3 = cdf(3, n, k)
    assert sp.simplify(F3 - D3) == 0
    print("K=3 vs Proposicao D3 (Estagio 40): EXACT MATCH (diff=0).")

    Q4 = (-k ** 6 + 9 * k ** 5 + (4 * n ** 2 - 18 * n - 31) * k ** 4
          + (-16 * n ** 2 + 80 * n + 51) * k ** 3
          + (-6 * n ** 4 + 42 * n ** 3 - 55 * n ** 2 - 120 * n - 40) * k ** 2
          + (6 * n ** 4 - 50 * n ** 3 + 97 * n ** 2 + 70 * n + 12) * k
          + 4 * n ** 6 - 30 * n ** 5 + 74 * n ** 4 - 52 * n ** 3 - 30 * n ** 2 - 12 * n)
    D4 = k * (k + 1) * Q4 / (n ** 5 * (n - 1) * (n - 2) * (n - 3))
    F4 = cdf(4, n, k)
    assert sp.simplify(F4 - D4) == 0
    print("K=4 vs Proposicao D4 (Estagio 43): EXACT MATCH (diff=0).")

    # Proposicao D5, transcribed by hand from k5_exact_closure_attempt/
    # ATTEMPT.md Section 3.3 (the immediate predecessor front's own new
    # result, itself already independently re-derived and confirmed by
    # a hostile referee in adversarial/REFEREE_REPORT.md -- cited here,
    # not re-proved, but spot-checked by this independent re-derivation
    # via the same general machinery before this front trusts D6).
    Bracket5 = (
        k ** 8 - 16 * k ** 7 - 5 * k ** 6 * n ** 2 + 30 * k ** 6 * n + 106 * k ** 6
        + 45 * k ** 5 * n ** 2 - 290 * k ** 5 * n - 376 * k ** 5
        + 10 * k ** 4 * n ** 4 - 100 * k ** 4 * n ** 3 + 100 * k ** 4 * n ** 2
        + 1100 * k ** 4 * n + 769 * k ** 4
        - 40 * k ** 3 * n ** 4 + 440 * k ** 3 * n ** 3 - 975 * k ** 3 * n ** 2
        - 2074 * k ** 3 * n - 904 * k ** 3
        - 10 * k ** 2 * n ** 6 + 120 * k ** 2 * n ** 5 - 435 * k ** 2 * n ** 4
        + 10 * k ** 2 * n ** 3 + 1885 * k ** 2 * n ** 2 + 2014 * k ** 2 * n + 564 * k ** 2
        + 10 * k * n ** 6 - 140 * k * n ** 5 + 635 * k * n ** 4 - 650 * k * n ** 3
        - 1410 * k * n ** 2 - 924 * k * n - 144 * k
        + 5 * n ** 8 - 60 * n ** 7 + 265 * n ** 6 - 490 * n ** 5 + 190 * n ** 4
        + 300 * n ** 3 + 360 * n ** 2 + 144 * n
    )
    D5 = k * (k + 1) * Bracket5 / (n ** 6 * (n - 1) * (n - 2) * (n - 3) * (n - 4))
    F5 = cdf(5, n, k)
    diff5 = sp.simplify(F5 - D5)
    assert diff5 == 0, diff5
    print("K=5 vs Proposicao D5 (Estagio 53, predecessor front, cited): "
          "EXACT MATCH (diff=0).")
    print(f"  (spot-check of the cited D5 formula itself, via this front's "
          f"own independent re-derivation of it from the general machinery "
          f"-- not blind trust.)")

    print(f"\nAll five validations passed in {time.time()-t_start:.2f}s total.")
    print("Pipeline (InnerJ / S_r / final assembly), including BOTH the")
    print("r<K and r=K InnerJ branches and the r=0 edge case, is now")
    print("trusted for K=6.\n")

    print("=" * 78)
    print("PROPOSICAO D6 (K=6, this front's own derivation)")
    print("=" * 78)
    t0 = time.time()
    F6 = cdf(6, n, k, verbose=True)
    print(f"\nTotal elapsed for K=6: {time.time()-t0:.2f}s")
    num6, den6 = sp.fraction(F6)
    num6 = sp.expand(num6)
    den6 = sp.factor(den6)
    print("\nD6(n,k) NUM =")
    print(num6)
    print("\nD6(n,k) DEN =", den6)

    # ---- sanity identities ----
    print()
    print("Sanity checks:")
    PT_n = sp.simplify(1 - F6.subs(k, n - 1))
    print("  1 - D6(n,n-1) [=P(T=n)] =", sp.factor(PT_n))
    assert sp.simplify(PT_n - sp.Rational(720, 1) / n ** 6) == 0
    print("  matches predicted K!/n^K = 6!/n^6 = 720/n^6.  PASSED.")

    assert sp.simplify(F6.subs(k, 0)) == 0
    assert sp.simplify(F6.subs(k, -1)) == 0
    print("  D6(n,0) = D6(n,-1) = 0 (structural k(k+1) factor).  PASSED.")

    for nv in [6, 7, 8, 9, 10, 12]:
        vals = [sp.Rational(F6.subs({n: nv, k: kv})) for kv in range(nv)]
        assert all(vals[i] <= vals[i + 1] for i in range(len(vals) - 1))
    print("  D6(n,.) monotonic non-decreasing in k, n=6..10,12.  PASSED.")

    # degree/denominator pattern check against K=1..5
    print()
    print("Structural pattern check:")
    print("  denominator = n^(K+1)(n-1)...(n-(K-1)) pattern at K=6: "
          "n^7(n-1)(n-2)(n-3)(n-4)(n-5) expected.")
    expected_den = n ** 7 * (n - 1) * (n - 2) * (n - 3) * (n - 4) * (n - 5)
    assert sp.simplify(sp.factor(den6) - sp.factor(expected_den)) == 0
    print("  denominator PASSED.")
    deg_k_full = sp.Poly(num6, k).degree()
    print(f"  full numerator degree in k = {deg_k_full} (predicted 2K = 12, "
          f"matching D3/D4/D5's own num degree 2K pattern before factoring "
          f"out k(k+1)).")
    assert deg_k_full == 12

    Bracket6, rem = sp.div(num6, k * (k + 1), k)
    assert sp.expand(rem) == 0, "k(k+1) must divide the numerator exactly"
    Bracket6 = sp.expand(Bracket6)
    deg_bracket = sp.Poly(Bracket6, k).degree()
    print(f"  Bracket6 = D6-numerator / [k(k+1)], degree in k = {deg_bracket} "
          f"(predicted 2K-2 = 10, matching D3/D4/D5's Bracket_K pattern).")
    assert deg_bracket == 10
    print("\nD6(n,k) = k(k+1)*Bracket6(n,k) / [n^7(n-1)(n-2)(n-3)(n-4)(n-5)]")
    print("Bracket6(n,k) =")
    print(Bracket6)

    print()
    print("DONE. Proposicao D6 derived and self-consistency-checked.")
    print("Independent cross-check against fresh brute-force Definition 4:")
    print("see bruteforce_definition4_k6.py/.log.")
