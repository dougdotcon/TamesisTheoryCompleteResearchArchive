"""
H_{2k-1}(r,b), via a route DELIBERATELY DIFFERENT from the target
front's own bivariate (x,y)-reparametrized A_k recursion.

Route used here: the CLOSED-SUM definition of S_{2k-1}(N,m), cited
verbatim from `general_p_dstar_extension2_attempt/adversarial/REFEREE_REPORT.md`
Sec.2.3 (that referee's "fourth, independent definition"):

    S_{2k-1}(N,m) = sum_{i=0}^{m} (N-2i)^{2k-1} * C(N,i)

evaluated by DIRECT SUMMATION at each concrete (N,m) -- no recursion in
k at all, no A_k factorization, no bivariate reparametrization. This is
a genuinely different algorithmic route from the target front's own
(which builds a shared recursive bivariate polynomial table A_k(x,y)
once for all k up to k_max and then specializes).

    H_{2k-1}(r,b) := P_b(r) * S_{2k-1}(N,r),   N = 2r+b+1
    P_b(r) := r! * (r+b)! / N!    (elementary identity, re-derived
              independently in Sec. "P_b(r)" below from the cited
              P_b * C(N,r+1) = 1/(r+1) relation)

fractions.Fraction throughout. No .py file from any front in this
lineage was opened, read, or imported.
"""
from fractions import Fraction
from math import comb, factorial


def P_b_of_r(r, b):
    """
    P_b(r) = r!(r+b)!/N!, N=2r+b+1.

    Re-derivation, independent of the target front's own (its Sec.1):
    the cited identity is P_b * C(N,r+1) = 1/(r+1). Since
    C(N,r+1) = N! / [(r+1)! (N-r-1)!] and N-r-1 = r+b (because
    N=2r+b+1), we get C(N,r+1) = N!/[(r+1)!(r+b)!], so
        P_b = 1/[(r+1) * C(N,r+1)] = (r+1)!(r+b)! / [(r+1) N!]
            = r!(r+b)!/N!.
    Confirmed directly below (self_test) against the cited identity
    itself, at concrete (r,b) pairs, before being trusted for anything.
    """
    N = 2 * r + b + 1
    return Fraction(factorial(r) * factorial(r + b), factorial(N))


def S_odd_closed_sum(twok_minus_1, N, m):
    """
    S_{2k-1}(N,m) = sum_{i=0}^{m} (N-2i)^{2k-1} * C(N,i), direct
    summation, exact integer/Fraction arithmetic. `twok_minus_1` is the
    odd exponent 2k-1 directly (an integer >= 1).
    """
    total = 0
    for i in range(0, m + 1):
        base = N - 2 * i
        total += (base ** twok_minus_1) * comb(N, i)
    return Fraction(total)


def H_odd(k, r, b):
    """H_{2k-1}(r,b) = P_b(r) * S_{2k-1}(N,r), N=2r+b+1."""
    N = 2 * r + b + 1
    return P_b_of_r(r, b) * S_odd_closed_sum(2 * k - 1, N, r)


def build_H_table(r, b, k_max):
    """
    Return {k: H_{2k-1}(r,b)} for k=1,...,k_max, at a FIXED concrete
    (r,b), still via the closed-sum route (S_{2k-1}(N,m) = sum_i
    (N-2i)^{2k-1} C(N,i)) -- genuinely different from the target front's
    bivariate-recursion route -- but with an ELEMENTARY efficiency
    improvement native to this referee: the binomial row C(N,0..r) and
    the base values (N-2i) are shared across all k (previously
    recomputed independently by k separate H_odd() calls, each
    re-invoking math.comb(N,i) for every i -- pure redundant work, not a
    different route, since the mathematical content of S_odd_closed_sum
    is unchanged). This is bookkeeping speed only, exactly analogous in
    spirit (though not in mechanism) to the target front's own Sec.2.3
    engineering note -- verified to agree with the un-shared per-k
    H_odd() route below in self_test before being trusted.
    """
    N = 2 * r + b + 1
    comb_row = [comb(N, i) for i in range(0, r + 1)]
    bases = [N - 2 * i for i in range(0, r + 1)]
    Pb = P_b_of_r(r, b)
    out = {}
    for k in range(1, k_max + 1):
        e = 2 * k - 1
        total = 0
        for i in range(0, r + 1):
            total += (bases[i] ** e) * comb_row[i]
        out[k] = Pb * Fraction(total)
    return out


# ======================================================================
# Self-test
# ======================================================================
def a_k_depth_recursion(k, d, r, b, cache=None):
    """
    Direct (non-bivariate, non-reparametrized) implementation of the
    ORIGINALLY-cited depth-indexed recursion the target document's own
    Sec.2.3 reparametrizes into a bivariate polynomial A_k(x,y):

        a_k^{(d)}(r) = (r-d+1) * [ (beta+d)^{2k-2}
                        + 2 * sum_{s odd, 1<=s<=2k-3} C(2k-2,s) * a_{(s+1)/2}^{(d+1)}(r) ]
        a_1^{(d)}(r) = r-d+1,   H_{2k-1}(r,b) = a_k^{(0)}(r) / (r+1)

    Implemented HERE exactly as stated (per-(r,b) concrete evaluation,
    plain recursion, no (x,y) substitution at all) -- this is the
    reference point the mandate asks to check the front's bivariate
    reparametrization against. The substitution x:=m,y:=N-2m used by the
    target's Sec.2.3 sends a step (N,m)->(N-1,m-1) to (x,y)->(x-1,y+1)
    (elementary: x'=m-1=x-1, y'=(N-1)-2(m-1)=N-2m+1=y+1) -- a pure
    relabeling of the SAME recursion, carrying no new mathematical
    content. Confirmed here by matching VALUES between this literal
    depth-recursion and the closed-sum H_odd() route (self_test below),
    which is mathematically independent of both the target's bivariate
    route and this direct depth-recursion route.
    """
    if cache is None:
        cache = {}
    beta = b + 1
    key = (k, d)
    if key in cache:
        return cache[key]
    if k == 1:
        val = r - d + 1
        cache[key] = val
        return val
    bracket = (beta + d) ** (2 * k - 2)
    s = 1
    total_s = 0
    while s <= 2 * k - 3:
        total_s += comb(2 * k - 2, s) * a_k_depth_recursion((s + 1) // 2, d + 1, r, b, cache)
        s += 2
    bracket += 2 * total_s
    val = (r - d + 1) * bracket
    cache[key] = val
    return val


def H_odd_via_depth_recursion(k, r, b):
    val = a_k_depth_recursion(k, 0, r, b)
    return Fraction(val, r + 1)


def _S_odd_recursion_bruteforce(twok_minus_1, N, m, cache=None):
    """
    Brute-force re-implementation of the ORIGINALLY-cited S_{2k-1}
    recursion (as restated in the target's own Sec.2.3, itself cited
    from wave 15/wave-16's sources), NOT the closed-sum route above --
    an independent third check.

        S_1(N,m) = (m+1) C(N,m+1)
        S_{2k-1}(N,m) = (N-2m)^{2k-2} (m+1) C(N,m+1)
                        + 2N sum_{s odd, 1<=s<=2k-3} C(2k-2,s) S_s(N-1,m-1)
    """
    if cache is None:
        cache = {}
    key = (twok_minus_1, N, m)
    if key in cache:
        return cache[key]
    if twok_minus_1 == 1:
        val = (m + 1) * comb(N, m + 1)
        cache[key] = val
        return val
    k = (twok_minus_1 + 1) // 2
    term1 = (N - 2 * m) ** (2 * k - 2) * (m + 1) * comb(N, m + 1)
    term2 = 0
    if m >= 1:
        for s in range(1, 2 * k - 2, 2):
            term2 += comb(2 * k - 2, s) * _S_odd_recursion_bruteforce(s, N - 1, m - 1, cache)
        term2 *= 2 * N
    val = term1 + term2
    cache[key] = val
    return val


def self_test():
    checks = 0
    fails = 0

    # (0) P_b(r) vs the cited identity P_b * C(N,r+1) = 1/(r+1)
    for r in range(0, 30):
        for b in (0, 1, 2, 5, 8, 30):
            N = 2 * r + b + 1
            checks += 1
            lhs = P_b_of_r(r, b) * comb(N, r + 1)
            if lhs != Fraction(1, r + 1):
                fails += 1
                print("MISMATCH P_b identity", r, b, lhs)

    # (1) closed-sum route vs the brute-force ORIGINAL recursion
    bf_cache = {}
    for k in range(1, 12):
        for r in range(0, 10):
            for b in (0, 1, 2, 5, 8):
                N = 2 * r + b + 1
                checks += 1
                a = S_odd_closed_sum(2 * k - 1, N, r)
                w = _S_odd_recursion_bruteforce(2 * k - 1, N, r, bf_cache)
                if a != w:
                    fails += 1
                    print("MISMATCH S_odd", k, r, b, a, w)

    # (2) printed base cases H_1=1, H_3=(b+1)^2+4r (THEOREM.md "Estagio
    # 16"/"Estagio 21")
    for r in range(0, 15):
        for b in range(0, 6):
            checks += 1
            if H_odd(1, r, b) != 1:
                fails += 1
                print("MISMATCH H_1", r, b, H_odd(1, r, b))
            checks += 1
            want = (b + 1) ** 2 + 4 * r
            got = H_odd(2, r, b)
            if got != want:
                fails += 1
                print("MISMATCH H_3", r, b, got, want)

    # (3) degree bound deg_r H_{2k-1}(r,b) = k-1, leading coeff
    # 4^{k-1}(k-1)!, b-independent -- cited PROVED (wave-16 referee),
    # re-checked here via finite differences at concrete integer points
    # (a route independent of building a symbolic polynomial): sample
    # H_odd(k,r,b) at r=0,...,k+2 for fixed b, fit via Lagrange
    # interpolation (own routine, imported from ingredients.py), check
    # degree and leading coefficient.
    import ingredients as ing
    for k in range(1, 46):
        for b in (0, 1, 3, 7, 30):
            xs = list(range(0, k + 3))
            pts = [(Fraction(r), H_odd(k, r, b)) for r in xs]
            coeffs = ing.lagrange_interpolate(pts)
            deg = 0
            for i, c in enumerate(coeffs):
                if c != 0:
                    deg = i
            checks += 1
            want_deg = k - 1 if k >= 1 else 0
            if deg != want_deg:
                fails += 1
                print("MISMATCH degree bound", k, b, deg, want_deg)
            checks += 1
            want_lead = Fraction(4 ** (k - 1) * factorial(k - 1))
            got_lead = coeffs[deg] if deg < len(coeffs) else Fraction(0)
            if got_lead != want_lead:
                fails += 1
                print("MISMATCH leading coeff", k, b, got_lead, want_lead)

    # (3b) closed-sum H_odd vs the LITERAL depth-indexed a_k^{(d)}(r)
    # recursion (the ORIGINAL, un-reparametrized recursion the target
    # document's bivariate A_k(x,y) route is built from) -- directly
    # addresses whether the (x,y)-reparametrization changes anything
    # (mandate item 10): if it did, this check (independent of that
    # reparametrization entirely) would disagree with the closed-sum
    # route, since both ultimately claim to compute the same H_{2k-1}.
    for k in range(1, 25):
        for r in range(0, 12):
            for b in (0, 1, 2, 5, 8, 30):
                checks += 1
                a = H_odd(k, r, b)
                w = H_odd_via_depth_recursion(k, r, b)
                if a != w:
                    fails += 1
                    print("MISMATCH depth-recursion vs closed-sum", k, r, b, a, w)

    # (4) build_H_table (shared-binomial-row speed path) vs per-k H_odd
    # (the un-shared route) -- confirms the bookkeeping speedup changes
    # nothing mathematically
    for r in (0, 5, 17, 42, 85, 130):
        for b in (0, 3, 15, 30):
            table = build_H_table(r, b, 12)
            for k in range(1, 13):
                checks += 1
                if table[k] != H_odd(k, r, b):
                    fails += 1
                    print("MISMATCH build_H_table vs H_odd", r, b, k)

    print(f"odd_part.py self_test: {checks} checks, {fails} fails")
    return checks, fails


if __name__ == "__main__":
    self_test()
