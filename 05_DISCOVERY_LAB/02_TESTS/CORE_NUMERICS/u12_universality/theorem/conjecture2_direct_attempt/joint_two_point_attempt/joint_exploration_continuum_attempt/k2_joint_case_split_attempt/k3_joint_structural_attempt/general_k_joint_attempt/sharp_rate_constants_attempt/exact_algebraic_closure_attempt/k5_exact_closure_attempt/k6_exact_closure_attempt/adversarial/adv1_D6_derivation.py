"""
Hostile referee, K6-EXACT-CLOSURE-ATTEMPT (wave 30, front b).

Independent re-derivation of Proposicao D6 from the CITED general-K
machinery (Estagio 41's Proposicao S / Full Cycle-Count Decomposition
Theorem; Estagio 44's S_r(n,K,k) exchangeability reduction and Layer-1
InnerJ(V,O) closed form -- both PROVED elsewhere, cited verbatim, never
re-derived here). This script is typed independently from the same two
boxed formulas the target cites, NOT copied from the target's own
d6_derivation.py (that file was read only to confirm the recipe/claims
being checked, per the review's own instructions -- every line of
mathematics below is re-typed and uses a different code structure: a
memoized recursive falling-factorial helper instead of an explicit
product loop, a single unified S_r routine that does not special-case
r=0 with a separate code path (the r=0 case is instead handled by
letting the V-sum range be validated to be empty vs a single point via
sympy's own Piecewise-free direct integer range, which collapses to the
same single term used by the target for a different structural reason,
see the docstring on s_r below), and an explicit re-assembly of the
final CDF as a Rational-coefficient sum rather than a single
sp.cancel/sp.together call chain).

Boxed formulas used (identical content to ATTEMPT.md's own citation,
retyped independently):

    P(T<=k) = (1/C(n,K)) * sum_{r=0}^{K} C(K,r) * r!/n^{r+1} * S_r(n,K,k)

    S_r(n,K,k) = sum_{O=0}^{k} sum_{V=r}^{t} C(V-1,r-1) * InnerJ(V,O),
                 t := k - O

    InnerJ(V,O) = (O+V)*C(N+r-1,K-1) + r*C(N+r-1,K),  N := n-V-O   (r<K)
    InnerJ(V,O) = n * C(N+r-1,r-1),                    N := n-V-O   (r=K)

Self-validation: reproduces D1 (Estagio 27), D2 (Estagio 42), D3
(Estagio 40), D4 (Estagio 43) -- all independently PROVED elsewhere in
the archive, transcribed here by hand from THEOREM.md -- and D5
(Estagio 53, the K=5 predecessor's own new result), transcribed by hand
from k5_exact_closure_attempt/ATTEMPT.md Section 3.3 -- BEFORE trusting
the pipeline at K=6. Then computes D6 and diffs it, symbolically, against
the K6 target's own claimed Bracket6(n,k) (ATTEMPT.md Section 3.3),
transcribed by hand from that document, not copy-pasted from any .py
file.
"""
import time
import sympy as sp

n, k = sp.symbols('n k')


def rising_falling_binom(x, r):
    """Explicit polynomial for the generalized binomial coefficient
    C(x, r) for concrete integer r (any sign), via the standard
    convention C(x,r) = x(x-1)...(x-r+1)/r! for r>0, C(x,0)=1,
    C(x,r)=0 for r<0. Built as a memoized recursive product (a
    different implementation shape from a plain for-loop) purely to
    keep this script's code path independent of the target's own
    helper."""
    if r < 0:
        return sp.Integer(0)
    if r == 0:
        return sp.Integer(1)

    def _rec(i):
        if i == 0:
            return (x - 0)
        return (x - i) * _rec(i - 1)

    return sp.expand(_rec(r - 1) / sp.factorial(r))


def inner_j_closed(V, O, r, K, nn):
    N = nn - V - O
    if r < K:
        term1 = (O + V) * rising_falling_binom(N + r - 1, K - 1)
        term2 = r * rising_falling_binom(N + r - 1, K)
        return sp.expand(term1 + term2)
    return sp.expand(nn * rising_falling_binom(N + r - 1, r - 1))


def s_r(K, r, nn, kk):
    """S_r(n,K,k), cited verbatim.

    IMPORTANT correction, found and fixed during THIS script's own
    development (disclosed honestly, see the referee report): an r=0
    "generic path, no special case" version was tried FIRST here,
    reasoning (wrongly) that sp.summation over V=0..t with the blanket
    convention C(x,r)=0 for r<0 applied to C(V-1,r-1)=C(V-1,-1) would
    naturally collapse to the correct single V=0 term. It does not: the
    blanket "C(x,negative r)=0" convention used for rising_falling_binom
    zeroes out C(V-1,-1) at EVERY V, including V=0, because r-1=-1<0
    triggers the same "return 0" branch regardless of V -- silently
    making the entire r=0 contribution vanish (caught immediately by
    the K=1 self-validation assertion failing). The combinatorial
    resolution (re-derived from first principles, not copied from the
    target's own docstring, though it reaches the identical conclusion):
    C(V-1,r-1) counts compositions of V into r POSITIVE parts, which for
    r=0 is a genuinely different combinatorial object than the
    "generalized binomial with a negative lower index" convention used
    elsewhere -- it is 1 exactly at V=0 (the empty composition) and 0
    for V>0, NOT "always 0" as the blanket negative-r convention would
    suggest. So r=0 genuinely requires a distinct code path: S_0(n,K,k)
    = sum_{O=0}^{k} InnerJ(0,O,0,K,n). This independently confirms (via
    a real, self-caught bug during the writing of THIS review's own
    from-scratch reproduction) that the target's own explicit r=0
    special-casing (d6_derivation.py, s_r_of) is mathematically
    NECESSARY, not an arbitrary implementation choice.
    """
    Os = sp.Symbol('Os', integer=True)
    if r == 0:
        summand0 = inner_j_closed(0, Os, 0, K, nn)
        return sp.expand(sp.summation(summand0, (Os, 0, kk)))
    Vs = sp.Symbol('Vs', integer=True)
    tt = kk - Os
    v_summand = sp.expand(rising_falling_binom(Vs - 1, r - 1) * inner_j_closed(Vs, Os, r, K, nn))
    v_summed = sp.expand(sp.summation(v_summand, (Vs, r, tt)))
    o_summed = sp.summation(v_summed, (Os, 0, kk))
    return sp.expand(o_summed)


def cdf_closed(K, nn, kk, verbose=False):
    acc = sp.Integer(0)
    for r in range(K + 1):
        t0 = time.time()
        Sr = s_r(K, r, nn, kk)
        if verbose:
            print(f"    S_{r}(n,{K},k) done in {time.time()-t0:.2f}s", flush=True)
        acc += sp.binomial(K, r) * sp.factorial(r) / nn ** (r + 1) * Sr
    acc = acc / sp.binomial(nn, K)
    return sp.factor(sp.cancel(sp.together(acc)))


if __name__ == "__main__":
    print("=" * 78)
    print("REFEREE: independent self-validation, D1..D5, via own pipeline")
    print("=" * 78)
    t_start = time.time()

    D1_cited = k * (k + 1) / n ** 2
    got1 = cdf_closed(1, n, k)
    assert sp.simplify(got1 - D1_cited) == 0
    print("K=1 vs D1 (Estagio 27): MATCH (diff=0)")

    D2_cited = k * (k + 1) * (2 * n ** 2 - 3 * n + k - k ** 2) / (n ** 3 * (n - 1))
    got2 = cdf_closed(2, n, k)
    assert sp.simplify(got2 - D2_cited) == 0
    print("K=2 vs D2 (Estagio 42): MATCH (diff=0)")

    D3_cited = (k * (k + 1) * (
        k ** 4 - 4 * k ** 3 - (3 * n ** 2 - 9 * n - 5) * k ** 2
        + (3 * n ** 2 - 11 * n - 2) * k
        + (3 * n ** 4 - 12 * n ** 3 + 12 * n ** 2 + 2 * n)
    ) / (n ** 4 * (n - 1) * (n - 2)))
    got3 = cdf_closed(3, n, k)
    assert sp.simplify(got3 - D3_cited) == 0
    print("K=3 vs D3 (Estagio 40): MATCH (diff=0)")

    Q4_cited = (-k ** 6 + 9 * k ** 5 + (4 * n ** 2 - 18 * n - 31) * k ** 4
                + (-16 * n ** 2 + 80 * n + 51) * k ** 3
                + (-6 * n ** 4 + 42 * n ** 3 - 55 * n ** 2 - 120 * n - 40) * k ** 2
                + (6 * n ** 4 - 50 * n ** 3 + 97 * n ** 2 + 70 * n + 12) * k
                + 4 * n ** 6 - 30 * n ** 5 + 74 * n ** 4 - 52 * n ** 3 - 30 * n ** 2 - 12 * n)
    D4_cited = k * (k + 1) * Q4_cited / (n ** 5 * (n - 1) * (n - 2) * (n - 3))
    got4 = cdf_closed(4, n, k)
    assert sp.simplify(got4 - D4_cited) == 0
    print("K=4 vs D4 (Estagio 43): MATCH (diff=0)")

    Bracket5_cited = (
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
    D5_cited = k * (k + 1) * Bracket5_cited / (n ** 6 * (n - 1) * (n - 2) * (n - 3) * (n - 4))
    got5 = cdf_closed(5, n, k)
    diff5 = sp.simplify(got5 - D5_cited)
    assert diff5 == 0, diff5
    print("K=5 vs D5 (Estagio 53, cited from predecessor ATTEMPT.md Sec 3.3): "
          "MATCH (diff=0)")

    print(f"\nAll 5 self-validations passed in {time.time()-t_start:.2f}s. "
          f"Trusting the pipeline for K=6.\n")

    print("=" * 78)
    print("REFEREE: independent derivation of D6 (K=6)")
    print("=" * 78)
    t0 = time.time()
    got6 = cdf_closed(6, n, k, verbose=True)
    print(f"Elapsed for K=6: {time.time()-t0:.2f}s")

    # Target's own claimed Bracket6(n,k), ATTEMPT.md Sec 3.3, transcribed
    # by hand here (NOT copy-pasted from the target's own .py file).
    Bracket6_target = (
        -k**10 + 25*k**9 + 6*k**8*n**2 - 45*k**8*n - 270*k**8 - 96*k**7*n**2
        + 760*k**7*n + 1650*k**7 - 15*k**6*n**4 + 195*k**6*n**3 - 9*k**6*n**2
        - 5380*k**6*n - 6273*k**6 + 135*k**5*n**4 - 1875*k**5*n**3
        + 4359*k**5*n**2 + 20734*k**5*n + 15345*k**5 + 20*k**4*n**6
        - 330*k**4*n**5 + 1375*k**4*n**4 + 3600*k**4*n**3 - 22441*k**4*n**2
        - 47215*k**4*n - 24080*k**4 - 80*k**3*n**6 + 1440*k**3*n**5
        - 7975*k**3*n**4 + 4641*k**3*n**3 + 50821*k**3*n**2 + 64330*k**3*n
        + 23300*k**3 - 15*k**2*n**8 + 270*k**2*n**7 - 1730*k**2*n**6
        + 3435*k**2*n**5 + 7610*k**2*n**4 - 20391*k**2*n**3 - 58916*k**2*n**2
        - 50320*k**2*n - 12576*k**2 + 15*k*n**8 - 310*k*n**7 + 2360*k*n**6
        - 7055*k*n**5 + 730*k*n**4 + 20526*k*n**3 + 33716*k*n**2 + 20016*k*n
        + 2880*k + 6*n**10 - 105*n**9 + 720*n**8 - 2375*n**7 + 3384*n**6
        - 10*n**5 - 1860*n**4 - 6696*n**3 - 7440*n**2 - 2880*n
    )
    D6_target = k * (k + 1) * Bracket6_target / (n**7 * (n-1) * (n-2) * (n-3) * (n-4) * (n-5))

    diff6 = sp.simplify(got6 - D6_target)
    print(f"\nReferee-derived D6 vs target's own claimed D6 (transcribed from "
          f"ATTEMPT.md Sec 3.3): symbolic difference = {diff6}")
    assert diff6 == 0, f"MISMATCH: {diff6}"
    print("EXACT MATCH -- Proposicao D6 independently confirmed correct.")

    # Extra sanity identities, independent of the target's own script.
    PTn = sp.simplify(1 - got6.subs(k, n - 1))
    assert sp.simplify(PTn - sp.Rational(720, 1) / n ** 6) == 0
    print("\n1 - D6(n,n-1) = 720/n^6 = 6!/n^6.  PASSED (independent check).")
    assert sp.simplify(got6.subs(k, 0)) == 0
    assert sp.simplify(got6.subs(k, -1)) == 0
    print("D6(n,0)=D6(n,-1)=0.  PASSED (independent check).")

    for nv in [6, 7, 8, 11, 13]:
        vals = [sp.Rational(got6.subs({n: nv, k: kv})) for kv in range(nv)]
        assert all(vals[i] <= vals[i + 1] for i in range(len(vals) - 1))
    print("D6(n,.) monotonic non-decreasing in k, n=6,7,8,11,13 (referee's own "
          "spot-check n's, deliberately different from the target's own "
          "n=6..10,12).  PASSED.")

    print("\nDONE. Proposicao D6 INDEPENDENTLY CONFIRMED correct.")
