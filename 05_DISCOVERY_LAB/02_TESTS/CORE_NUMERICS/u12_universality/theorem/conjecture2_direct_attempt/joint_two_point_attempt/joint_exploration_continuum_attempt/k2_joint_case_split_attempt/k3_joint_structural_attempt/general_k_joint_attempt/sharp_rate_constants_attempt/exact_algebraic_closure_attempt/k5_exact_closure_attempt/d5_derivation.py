"""
K5-EXACT-CLOSURE-ATTEMPT (wave 29, front c).

Derives Proposicao D5 (the exact finite-n CDF of M_n^{(5)}) from scratch,
by instantiating -- at the concrete integer K=5 -- the general-K
machinery PROVED (for every K, symbolic) in:

  - THEOREM.md Estagio 41 (general_k_decomposition_attempt/ATTEMPT.md):
    Proposicao S (the law of S, the random set of "cyclic" reroute
    sources) and the Full Cycle-Count Decomposition Theorem, both K-free.
  - THEOREM.md Estagio 44 (general_k_closed_cdf_attempt/ATTEMPT.md):
    the S_r(n,K,k) reduction by touched-subset size r (Section 2/3 of
    that document) and its Layer-1 "InnerJ" closed form (Section 4.1),
    PROVED symbolic in (n,K,r).

Both of the above are CITED, not re-derived, per this front's mandate
(read-only ancestors). What THIS script adds, fresh: the observation,
verified directly below rather than assumed, that once K is a CONCRETE
integer (rather than a free symbol), InnerJ(V,O) is an explicit
polynomial in V of degree K -- so the S_r inner V-sum and outer O-sum are
classical Faulhaber power sums, closing immediately via sp.summation
with NO Gosper certificate needed (this is the precise, verified reason
Estagio 44's own concrete-K Gosper spot-checks, K=3,...,7, all succeed
trivially: the K-symbolic obstruction lives entirely in InnerJ's degree
being K-dependent, which disappears once K is fixed).

Formulas used (transcribed by hand from general_k_closed_cdf_attempt/
ATTEMPT.md Sec 2-4, both cited as PROVED there):

  P(T<=k) = (1/C(n,K)) * sum_{r=0}^{K} C(K,r) * r!/n^{r+1} * S_r(n,K,k)

  S_r(n,K,k) = sum_{O=0}^{k} sum_{V=r}^{t} C(V-1,r-1) * InnerJ(V,O),
               t:=k-O   (r=0: no V-sum, take V=0 directly -- see below)

  InnerJ(V,O) = (O+V)*C(N+r-1,K-1) + r*C(N+r-1,K),   N:=n-V-O   (r<K)
  InnerJ(V,O) = n * C(N+r-1,r-1),                     N:=n-V-O   (r=K)

r=0 special case (this front's own elementary derivation, checked below
against D1-D4): S_0(n,K,k) = sum_{O=0}^{k} O * C(n-O-1,K-1), which is
literally InnerJ(V=0,O) [r<K branch] evaluated at the single point V=0
(no sum needed since Count_0(;t) in {0,1} is a single indicator, not a
genuine multi-term sum).

MANDATORY SELF-VALIDATION (done BEFORE trusting the K=5 output): the
identical, unmodified pipeline is run at K=1,2,3,4 and its output is
checked, via exact sp.simplify, against the ALREADY-INDEPENDENTLY-PROVED
closed forms Proposicao D1 (Estagio 27), D2 (Estagio 42), D3 (Estagio
40), D4 (Estagio 43), transcribed by hand from THEOREM.md.
"""
import sympy as sp
import time

n, k = sp.symbols('n k')


def binom_poly(x, r):
    """Explicit expanded polynomial for C(x, r), r a concrete nonneg int
    (matches the combinatorial convention C(x,r)=0 for r<0)."""
    if r < 0:
        return sp.Integer(0)
    if r == 0:
        return sp.Integer(1)
    num = sp.Integer(1)
    for i in range(r):
        num *= (x - i)
    return sp.expand(num / sp.factorial(r))


def InnerJ_poly(V, O, r, K, n_):
    N = n_ - V - O
    if r < K:
        expr = (O + V) * binom_poly(N + r - 1, K - 1) + r * binom_poly(N + r - 1, K)
    else:
        expr = n_ * binom_poly(N + r - 1, r - 1)
    return sp.expand(expr)


def S_r(K, r, n_, k_, verbose=False):
    O_ = sp.Symbol('O_', integer=True)
    V_ = sp.Symbol('V_', integer=True)
    t0 = time.time()
    if r == 0:
        expr = sp.expand(O_ * binom_poly(n_ - O_ - 1, K - 1))
        res = sp.summation(expr, (O_, 0, k_))
    else:
        t_ = k_ - O_
        inner = sp.expand(binom_poly(V_ - 1, r - 1) * InnerJ_poly(V_, O_, r, K, n_))
        Vsum = sp.expand(sp.summation(inner, (V_, r, t_)))
        res = sp.summation(Vsum, (O_, 0, k_))
    res = sp.factor(sp.expand(res))
    if verbose:
        print(f"    S_{r}(n,{K},k) computed in {time.time()-t0:.2f}s", flush=True)
    return res


def CDF(K, n_, k_, verbose=False):
    total = sp.Integer(0)
    for r in range(0, K + 1):
        Sr = S_r(K, r, n_, k_, verbose=verbose)
        total += sp.binomial(K, r) * sp.factorial(r) / n_**(r + 1) * Sr
    total = total / sp.binomial(n_, K)
    return sp.factor(sp.cancel(sp.together(total)))


if __name__ == "__main__":
    print("=" * 70)
    print("SELF-VALIDATION: reproduce D1, D2, D3, D4 EXACTLY (symbolic)")
    print("=" * 70)

    t_start = time.time()

    F1 = CDF(1, n, k)
    D1 = k * (k + 1) / n**2
    assert sp.simplify(F1 - D1) == 0
    print("K=1 vs Proposicao D1 (Estagio 27): EXACT MATCH.")

    F2 = CDF(2, n, k)
    D2 = k * (k + 1) * (2 * n**2 - 3 * n + k - k**2) / (n**3 * (n - 1))
    assert sp.simplify(F2 - D2) == 0
    print("K=2 vs Proposicao D2 (Estagio 42): EXACT MATCH.")

    F3 = CDF(3, n, k)
    D3 = (k * (k + 1) * (k**4 - 4*k**3 - (3*n**2 - 9*n - 5)*k**2
          + (3*n**2 - 11*n - 2)*k + (3*n**4 - 12*n**3 + 12*n**2 + 2*n))
          / (n**4 * (n - 1) * (n - 2)))
    assert sp.simplify(F3 - D3) == 0
    print("K=3 vs Proposicao D3 (Estagio 40): EXACT MATCH.")

    F4 = CDF(4, n, k)
    Q4 = (-k**6 + 9*k**5 + (4*n**2 - 18*n - 31)*k**4
          + (-16*n**2 + 80*n + 51)*k**3
          + (-6*n**4 + 42*n**3 - 55*n**2 - 120*n - 40)*k**2
          + (6*n**4 - 50*n**3 + 97*n**2 + 70*n + 12)*k
          + 4*n**6 - 30*n**5 + 74*n**4 - 52*n**3 - 30*n**2 - 12*n)
    D4 = k * (k + 1) * Q4 / (n**5 * (n - 1) * (n - 2) * (n - 3))
    assert sp.simplify(F4 - D4) == 0
    print("K=4 vs Proposicao D4 (Estagio 43): EXACT MATCH.")

    print(f"\nAll four validations passed in {time.time()-t_start:.2f}s total.")
    print("Pipeline (InnerJ / S_r / final assembly), including BOTH the")
    print("r<K and r=K InnerJ branches (both exercised at every K tested,")
    print("even K=1), is now trusted for K=5.\n")

    print("=" * 70)
    print("PROPOSICAO D5 (K=5, this front's own derivation)")
    print("=" * 70)
    t0 = time.time()
    F5 = CDF(5, n, k, verbose=True)
    print(f"\nTotal elapsed for K=5: {time.time()-t0:.2f}s")
    num5, den5 = sp.fraction(F5)
    print("\nD5(n,k) = ")
    print(" NUM =", sp.expand(num5))
    print(" DEN =", sp.factor(den5))

    # ---- sanity identities ----
    print()
    print("Sanity checks:")
    PT_n = sp.simplify(1 - F5.subs(k, n - 1))
    print("  1 - D5(n,n-1) [=P(T=n)] =", sp.factor(PT_n))
    assert sp.simplify(PT_n - sp.Rational(120, 1) / n**5) == 0
    print("  matches predicted K!/n^K = 5!/n^5 = 120/n^5.  PASSED.")

    assert sp.simplify(F5.subs(k, 0)) == 0
    assert sp.simplify(F5.subs(k, -1)) == 0
    print("  D5(n,0) = D5(n,-1) = 0 (structural k(k+1) factor).  PASSED.")

    for nv in [5, 6, 7, 8, 9, 10]:
        vals = [sp.Rational(F5.subs({n: nv, k: kv})) for kv in range(nv)]
        assert all(vals[i] <= vals[i + 1] for i in range(len(vals) - 1))
    print("  D5(n,.) monotonic non-decreasing in k, n=5..10.  PASSED.")

    print()
    print("DONE. Proposicao D5 derived and self-consistency-checked.")
    print("Independent cross-check against fresh brute-force Definition 4")
    print("(n=5,6,7, every k): see bruteforce_crosscheck_D5.py/.log.")
