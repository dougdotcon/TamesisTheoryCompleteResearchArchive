"""
INDEPENDENT REFEREE RE-DERIVATION of Proposicao D5 (K=5 closed-form CDF).

Written from scratch, by the referee, directly from the formulas CITED
(and PROVED elsewhere in the archive) in:
  general_k_decomposition_attempt/ATTEMPT.md  (Proposicao S, general K;
      Full Cycle-Count Decomposition Theorem)
  general_k_closed_cdf_attempt/ATTEMPT.md      (Section 2-4: exchangeability
      reduction to S_r(n,K,k); Layer-1 InnerJ closed form)

The target front's own scripts (d5_derivation.py, k5_exact_closure.py)
were read for their PROSE claims only; none of their CODE was copied or
imported here. This script is typed independently from the boxed
formulas quoted verbatim in both ATTEMPT.md documents:

  P(T<=k) = (1/C(n,K)) * sum_{r=0}^{K} C(K,r) * r!/n^{r+1} * S_r(n,K,k)

  S_r(n,K,k) = sum_{O=0}^{k} sum_{V=r}^{t} C(V-1,r-1) * InnerJ(V,O),
               t := k-O

  InnerJ(V,O) = (O+V)*C(N+r-1,K-1) + r*C(N+r-1,K),   N:=n-V-O   (r<K)
  InnerJ(V,O) = n * C(N+r-1,r-1),                     N:=n-V-O   (r=K)

For r=0 there are no "touched" sources at all (the subset A is empty),
so Sigma_A=0 identically and there is no genuine V-sum; the r=0 term of
S_r reduces, directly from the definition of S_r (before Layer 1 is even
invoked, since Layer-1's V is exactly the touched-subset total which is
vacuous when r=0), to the single value V=0. Consistency check performed
below: this matches the r<K InnerJ branch evaluated at (V,O)=(0,O), which
we verify explicitly is what makes K=1..4 reproduce D1..D4.
"""
import sympy as sp
import time

n, k = sp.symbols('n k')


def binom_poly(x, r):
    """C(x,r) as an explicit expanded polynomial in x, r a concrete
    nonnegative integer (0 for r<0, matching combinatorial convention)."""
    if r < 0:
        return sp.Integer(0)
    if r == 0:
        return sp.Integer(1)
    prod = sp.Integer(1)
    for i in range(r):
        prod *= (x - i)
    return sp.expand(prod / sp.factorial(r))


def InnerJ(Vv, Ov, r, K, nv):
    N = nv - Vv - Ov
    if r < K:
        return sp.expand((Ov + Vv) * binom_poly(N + r - 1, K - 1)
                          + r * binom_poly(N + r - 1, K))
    else:
        return sp.expand(nv * binom_poly(N + r - 1, r - 1))


def S_r(K, r, nv, kv):
    Osym = sp.Symbol('O', integer=True)
    if r == 0:
        # no touched sources: InnerJ(V=0,O) evaluated directly, summed over O
        summand = sp.expand(InnerJ(0, Osym, 0, K, nv))
        return sp.summation(summand, (Osym, 0, kv))
    Vsym = sp.Symbol('V', integer=True)
    tsym = kv - Osym
    inner = sp.expand(binom_poly(Vsym - 1, r - 1) * InnerJ(Vsym, Osym, r, K, nv))
    vsum = sp.expand(sp.summation(inner, (Vsym, r, tsym)))
    return sp.summation(vsum, (Osym, 0, kv))


def CDF(K, nv, kv):
    total = sp.Integer(0)
    for r in range(K + 1):
        Sr = sp.factor(sp.expand(S_r(K, r, nv, kv)))
        total += sp.binomial(K, r) * sp.factorial(r) / nv ** (r + 1) * Sr
    total = total / sp.binomial(nv, K)
    return sp.factor(sp.cancel(sp.together(total)))


if __name__ == "__main__":
    t_start = time.time()
    print("Independent referee re-derivation of D1..D5 from cited general-K formulas")
    print("=" * 78)

    F1 = CDF(1, n, k)
    D1 = k * (k + 1) / n**2
    diff1 = sp.simplify(F1 - D1)
    print("K=1 vs D1 (Estagio 27):  diff =", diff1)
    assert diff1 == 0

    F2 = CDF(2, n, k)
    D2 = k * (k + 1) * (2*n**2 - 3*n + k - k**2) / (n**3 * (n - 1))
    diff2 = sp.simplify(F2 - D2)
    print("K=2 vs D2 (Estagio 42):  diff =", diff2)
    assert diff2 == 0

    F3 = CDF(3, n, k)
    D3 = (k*(k+1)*(k**4 - 4*k**3 - (3*n**2-9*n-5)*k**2 + (3*n**2-11*n-2)*k
          + (3*n**4-12*n**3+12*n**2+2*n)) / (n**4*(n-1)*(n-2)))
    diff3 = sp.simplify(F3 - D3)
    print("K=3 vs D3 (Estagio 40):  diff =", diff3)
    assert diff3 == 0

    F4 = CDF(4, n, k)
    Q4 = (-k**6 + 9*k**5 + (4*n**2 - 18*n - 31)*k**4
          + (-16*n**2 + 80*n + 51)*k**3
          + (-6*n**4 + 42*n**3 - 55*n**2 - 120*n - 40)*k**2
          + (6*n**4 - 50*n**3 + 97*n**2 + 70*n + 12)*k
          + 4*n**6 - 30*n**5 + 74*n**4 - 52*n**3 - 30*n**2 - 12*n)
    D4 = k*(k+1)*Q4 / (n**5*(n-1)*(n-2)*(n-3))
    diff4 = sp.simplify(F4 - D4)
    print("K=4 vs D4 (Estagio 43):  diff =", diff4)
    assert diff4 == 0

    print()
    print("All of D1-D4 independently reproduced EXACTLY from the cited")
    print("general-K formulas (Proposicao S / Decomposition Theorem / InnerJ),")
    print("by a referee-typed, independently-written pipeline.")
    print()
    print("Now computing K=5 (this is the target's OWN new mathematical claim,")
    print("Proposicao D5) ...")
    t0 = time.time()
    F5 = CDF(5, n, k)
    print(f"K=5 computed in {time.time()-t0:.2f}s")

    num5, den5 = sp.fraction(F5)
    num5 = sp.expand(num5)
    den5 = sp.factor(den5)
    print()
    print("Referee-derived D5 NUM =", num5)
    print("Referee-derived D5 DEN =", den5)

    # Compare against the target's claimed Proposicao D5 (transcribed BY
    # HAND from the target's ATTEMPT.md Section 3.3, not copy-pasted from
    # any of the target's .py files):
    bracket_target_str = '''
    k**8 - 16*k**7 - 5*k**6*n**2 + 30*k**6*n + 106*k**6 + 45*k**5*n**2 - 290*k**5*n - 376*k**5
    + 10*k**4*n**4 - 100*k**4*n**3 + 100*k**4*n**2 + 1100*k**4*n + 769*k**4
    - 40*k**3*n**4 + 440*k**3*n**3 - 975*k**3*n**2 - 2074*k**3*n - 904*k**3
    - 10*k**2*n**6 + 120*k**2*n**5 - 435*k**2*n**4 + 10*k**2*n**3 + 1885*k**2*n**2 + 2014*k**2*n + 564*k**2
    + 10*k*n**6 - 140*k*n**5 + 635*k*n**4 - 650*k*n**3 - 1410*k*n**2 - 924*k*n - 144*k
    + 5*n**8 - 60*n**7 + 265*n**6 - 490*n**5 + 190*n**4 + 300*n**3 + 360*n**2 + 144*n
    '''
    bracket_target = sp.sympify(bracket_target_str, locals={'n': n, 'k': k})
    Dn5 = n**6 * (n-1) * (n-2) * (n-3) * (n-4)
    D5_target = k * (k+1) * bracket_target / Dn5

    diff5 = sp.simplify(F5 - D5_target)
    print()
    print("Target's claimed Proposicao D5 vs referee's independently-derived")
    print("D5, symbolic difference:", diff5)
    assert diff5 == 0, "MISMATCH between referee-derived D5 and target's claimed D5!"
    print("EXACT MATCH. The target's Proposicao D5 is independently confirmed.")

    # extra sanity: 1-D5(n,n-1) = 120/n^5
    PTn = sp.simplify(1 - F5.subs(k, n-1))
    print()
    print("1 - D5(n,n-1) [independent check] =", sp.factor(PTn))
    assert sp.simplify(PTn - sp.Rational(120,1)/n**5) == 0
    print("Matches 5!/n^5 = 120/n^5. PASSED (independent).")

    print()
    print(f"Total elapsed: {time.time()-t_start:.2f}s")
