"""
ADVERSARIAL SCRIPT 2 -- Layer 1's InnerJ closed form: re-derived from
first principles (own combinatorial argument, written up in the referee
report), then checked here numerically:
  (a) InnerJ_direct (raw defining sum over j) vs InnerJ_closed (r<K
      formula) for many (n,K,r,V,O),
  (b) the r=K boundary case, checked both against its OWN direct sum and
      against the r<K formula naively evaluated AT r=K (testing whether
      the two formulas "agree in the limit"),
  (c) S_r itself (the FULL two-layer object: sum over O and V of
      C(V-1,r-1)*InnerJ(V,O)) reconstructed via the closed InnerJ and
      checked against the fully-raw S_r_raw from script 1, for several
      concrete (n,K,r,k).
"""
from math import comb as _comb
import sys


def comb(n, k):
    """Safe binomial coefficient: 0 whenever the standard combinatorial
    convention says 0 (negative n, negative k, or k>n), matching the
    combinatorial meaning of every binomial in these formulas."""
    if n < 0 or k < 0 or k > n:
        return 0
    return _comb(n, k)


sys.path.insert(0, "/tmp/claude-0/-home-user-TamesisTheoryCompleteResearchArchive/e9ab1ff0-e9f9-5b73-816d-aec417acf7b1/scratchpad/adv")
import script1_exchangeability as s1


def compositions_count_p_positive_parts(M, p):
    """Number of ways to write M as a sum of p POSITIVE parts:
      p>=1: standard composition count C(M-1,p-1) (0 if M<p)
      p==0: the empty-sum boundary case -- 1 if M==0, else 0 (NOT
            representable as C(M-1,-1) under the ordinary binomial-
            coefficient convention, which is always 0 there; this is
            exactly the subtlety the target document's own r=K/r<K
            split is about, re-derived independently here from the
            raw definition rather than assumed).
    """
    if p == 0:
        return 1 if M == 0 else 0
    if M < p:
        return 0
    return comb(M - 1, p - 1)


def InnerJ_direct(n, K, r, V, O):
    """Raw defining sum: sum_{j>=0} C(j+r-1,r-1)*(O+V+j)*
    compositions_count_p_positive_parts(n-V-O-j, K-r).
    (Written as C(n-V-O-1-j,K-r-1) in the target document's own
    notation for K-r>=1; here made explicit via the p=0 boundary case
    too, since the naive binomial-coefficient shorthand silently
    returns 0 -- not the correct value 1 at the single point M=0 --
    when K-r=0, which is exactly why a separate r=K formula is needed
    at the level of the RAW definition, not just the closed form.)"""
    total = 0
    j = 0
    while True:
        c1 = comb(j + r - 1, r - 1) if r >= 1 else (1 if j == 0 else 0)
        M = n - V - O - j
        cnt = compositions_count_p_positive_parts(M, K - r)
        term = c1 * (O + V + j) * cnt
        total += term
        j += 1
        if M < 0 or (M == 0 and K - r == 0):
            # once M<0 all further j give cnt=0 too (M strictly
            # decreasing in j); if K-r==0 the only nonzero term was
            # exactly at this j, nothing more can contribute.
            break
        if j > n + 5:
            break
    return total


def InnerJ_closed_sub_K(n, K, r, V, O):
    """r<K closed form: (O+V)*C(N+r-1,K-1) + r*C(N+r-1,K), N:=n-V-O."""
    N = n - V - O
    return (O + V) * comb(N + r - 1, K - 1) + r * comb(N + r - 1, K)


def InnerJ_closed_eq_K(n, K, r, V, O):
    """r=K closed form: n*C(N+r-1,r-1), N:=n-V-O."""
    assert r == K
    N = n - V - O
    return n * comb(N + r - 1, r - 1)


if __name__ == "__main__":
    print("=" * 70)
    print("(a) InnerJ_direct vs InnerJ_closed, r<K, many configurations")
    print("=" * 70)
    ok = True
    configs = []
    for K in (3, 4, 5, 6, 7):
        for r in range(0, K):  # r < K only here
            for n in range(K + 2, K + 6):
                for V in range(r, min(n - K + r, r + 4) + 1):
                    for O in range(0, min(3, n - V) + 1):
                        if n - V - O >= 0:
                            configs.append((n, K, r, V, O))
    print(f"testing {len(configs)} configurations")
    for (n, K, r, V, O) in configs:
        d = InnerJ_direct(n, K, r, V, O)
        c = InnerJ_closed_sub_K(n, K, r, V, O)
        if d != c:
            ok = False
            print(f"  MISMATCH n={n} K={K} r={r} V={V} O={O}: direct={d} closed={c}")
    print("ALL MATCH (r<K):", ok)

    print()
    print("=" * 70)
    print("(b) r=K boundary case: InnerJ_direct vs InnerJ_closed_eq_K,")
    print("    AND vs the r<K formula naively evaluated AT r=K")
    print("    (testing whether the two stated formulas 'agree in the")
    print("    limit' or are genuinely numerically different)")
    print("=" * 70)
    ok2 = True
    agree_in_limit = True
    for K in (2, 3, 4, 5, 6, 7):
        r = K
        for n in range(K + 1, K + 6):
            for V in range(r, n - 0 + 1):
                for O in range(0, n - V + 1):
                    if n - V - O < 0:
                        continue
                    d = InnerJ_direct(n, K, r, V, O)
                    c_eqK = InnerJ_closed_eq_K(n, K, r, V, O)
                    if d != c_eqK:
                        ok2 = False
                        print(f"  MISMATCH (own r=K formula) n={n} K={K} r={r} V={V} O={O}: direct={d} closed={c_eqK}")
                    # naive evaluation of the r<K formula AT r=K:
                    N = n - V - O
                    naive = (O + V) * comb(N + r - 1, K - 1) + r * comb(N + r - 1, K)
                    if naive != c_eqK:
                        agree_in_limit = False
                        print(f"  formulas DISAGREE at r=K: n={n} K={K} V={V} O={O}: naive(r<K formula)={naive} true(r=K formula)={c_eqK}")
    print("r=K formula matches its own direct sum, ALL MATCH:", ok2)
    print("r<K formula, naively evaluated AT r=K, agrees with the r=K formula on EVERY tested config:", agree_in_limit)

    print()
    print("=" * 70)
    print("(c) symbolic algebraic check that the two formulas agree at r=K")
    print("    (n,K,r,V,O symbolic, via sympy, not just numeric spot checks)")
    print("=" * 70)
    import sympy as sp
    n, K_, V_, O_ = sp.symbols('n K V O', positive=True)
    N_ = n - V_ - O_
    r_ = K_
    lhs = (O_ + V_) * sp.binomial(N_ + r_ - 1, K_ - 1) + r_ * sp.binomial(N_ + r_ - 1, K_)
    rhs = n * sp.binomial(N_ + r_ - 1, r_ - 1)
    diff = sp.simplify(lhs - rhs)
    print("symbolic difference (r<K formula at r=K)  -  (r=K formula) =", diff)
    print("Symbolically IDENTICAL:", diff == 0)

    print()
    print("=" * 70)
    print("(d) full S_r reconstruction via closed InnerJ vs raw S_r_raw")
    print("    (script 1), several concrete (n,K,r,k)")
    print("=" * 70)
    ok3 = True
    for K in (3, 4, 5):
        for n in range(K + 2, K + 6):
            for r in range(0, K + 1):
                for k in range(0, n + 1):
                    # S_r(n,K,k) = sum_{O=0}^{k} sum_{V=r}^{t} C(V-1,r-1)*InnerJ(V,O), t=k-O
                    total = 0
                    for O in range(0, k + 1):
                        t = k - O
                        for V in range(r, t + 1):
                            if n - V - O < 0:
                                continue
                            cV = comb(V - 1, r - 1) if r >= 1 else (1 if V == 0 else 0)
                            if r == 0 and V != 0:
                                continue
                            if r == K:
                                inner = InnerJ_closed_eq_K(n, K, r, V, O)
                            else:
                                inner = InnerJ_closed_sub_K(n, K, r, V, O)
                            total += cV * inner
                    raw = s1.S_r_raw(n, K, k, r)
                    if total != raw:
                        ok3 = False
                        print(f"  MISMATCH n={n} K={K} r={r} k={k}: via-InnerJ={total} raw={raw}")
    print("Full S_r reconstruction via closed Layer-1 InnerJ matches raw S_r_raw, ALL MATCH:", ok3)
