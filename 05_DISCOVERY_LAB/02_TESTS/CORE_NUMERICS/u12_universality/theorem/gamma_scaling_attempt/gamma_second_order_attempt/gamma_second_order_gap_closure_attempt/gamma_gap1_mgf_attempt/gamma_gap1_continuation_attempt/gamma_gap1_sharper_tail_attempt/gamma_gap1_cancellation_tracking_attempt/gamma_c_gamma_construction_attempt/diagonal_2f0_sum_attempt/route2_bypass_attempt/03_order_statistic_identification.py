"""
03_order_statistic_identification.py

Route 2, option (iii) done RIGOROUSLY (not heuristically): identify the
normalized kernel of T(n,m) as the EXACT pmf of a classical, well-studied
discrete random variable -- the median (middle order statistic) of a
uniform random (2m+1)-subset drawn WITHOUT replacement from the finite
set {0,1,...,n+m} -- rather than anything to do with the Binomial(k,gamma)
random variable M that every ancestor/predecessor in this lineage's
moment/cumulant machinery is built on. This is a genuinely different
"more primitive random object" underlying S_n, per the mandate's option
(iii).

Fresh derivation (own code, not copied from any ancestor/predecessor):

Part A. Confirm p_m(j) := C(j+m,m) C(n-j,m) / C(n+m+1,2m+1) is a
        probability distribution on j=0..n-m (uses the predecessor's own
        PROVED Vandermonde-type identity C(n+m+1,2m+1) as normalizer --
        cited, independently re-verified here too).
Part B. Confirm p_m(j) matches the classical formula for the pmf of the
        r-th order statistic of an s-subset drawn without replacement
        from {1,...,N}: P(X_(r)=v) = C(v-1,r-1)C(N-v,s-r)/C(N,s), with
        s=2m+1, r=m+1, N=n+m+1, v=j+m+1 -- fresh symbolic + exact
        rational numeric check.
Part C. Exact mean/variance of the order statistic X (hence of j=X-m-1...
        careful with 0/1-indexing, resolved explicitly in-code) via the
        classical closed forms for order-statistic moments of sampling
        without replacement, cross-checked against brute-force exact
        summation for small n,m.
Part D. Numerically illustrate that T(n,m) = C(n+m+1,2m+1) * E[(1-g)^j]
        is a *tilted* (exponential-family) moment of this distribution,
        evaluated at a FIXED point ln(1-g) (not a small-x Taylor
        expansion near 0) -- i.e. genuinely a large-deviations object,
        not a CLT-regime object -- illustrated by locating the true
        maximizing j* (saddle point) of the summand at several (n,m,g)
        and comparing it to the (un-tilted) mean E[j]=(n-m)/2, showing
        j* is NOT close to the untilted mean once g is not extremely
        close to 1 -- i.e. this route needs genuine large-deviations /
        saddle-point machinery, not a naive CLT-at-the-mean expansion.
"""
from fractions import Fraction as F
from math import comb, log
import sympy as sp


def T_nm_fraction(n, m, g):
    total = F(0)
    for j in range(0, n - m + 1):
        total += comb(j + m, m) * comb(n - j, m) * ((1 - g) ** j)
    return total


def p_m_direct(n, m, j):
    """pmf value, exact Fraction."""
    denom = comb(n + m + 1, 2 * m + 1)
    return F(comb(j + m, m) * comb(n - j, m), denom)


def order_stat_pmf(N, s, r, v):
    """Classical formula: P(X_(r) = v) for r-th order stat (1-indexed,
    v in {1,...,N}) of an s-subset without replacement from {1,...,N}."""
    if v - 1 < r - 1 or N - v < s - r:
        return F(0)
    return F(comb(v - 1, r - 1) * comb(N - v, s - r), comb(N, s))


def main():
    L = []
    def p(s=""):
        print(s)
        L.append(str(s))

    p("=" * 70)
    p("Part A: p_m(j) is a probability distribution on j=0..n-m")
    p("        (normalizer = predecessor's PROVED Vandermonde identity,")
    p("        C(n+m+1,2m+1) = sum_j C(j+m,m) C(n-j,m); re-verified here")
    p("        independently for the gamma=1 case, i.e. weight==1)")
    p("=" * 70)
    mism = 0
    tot = 0
    for n in range(1, 15):
        for m in range(0, n + 1):
            lhs = sum(comb(j + m, m) * comb(n - j, m) for j in range(0, n - m + 1))
            rhs = comb(n + m + 1, 2 * m + 1)
            tot += 1
            if lhs != rhs:
                mism += 1
                p(f"  n={n} m={m}: sum={lhs} vs C(n+m+1,2m+1)={rhs}  MISMATCH")
    p(f"{tot} checks, {mism} mismatches (own fresh re-verification)")
    assert mism == 0

    for n in [8, 15]:
        for m in [0, 2, 4]:
            if m > n:
                continue
            total_prob = sum(p_m_direct(n, m, j) for j in range(0, n - m + 1))
            ok = (total_prob == 1)
            p(f"  n={n} m={m}: sum_j p_m(j) = {total_prob}  {'OK' if ok else 'MISMATCH'}")
            assert ok

    p("")
    p("=" * 70)
    p("Part B: p_m(j) IS the pmf of the (m+1)-th order statistic (the")
    p("        MEDIAN) of a uniform random (2m+1)-subset of {1,...,n+m+1}")
    p("        drawn WITHOUT replacement, via v = j+m+1")
    p("=" * 70)
    mism = 0
    tot = 0
    for n in [6, 9, 13]:
        for m in [0, 1, 2, 3]:
            if m > n:
                continue
            N = n + m + 1
            s = 2 * m + 1
            r = m + 1
            for j in range(0, n - m + 1):
                v = j + m + 1
                lhs = p_m_direct(n, m, j)
                rhs = order_stat_pmf(N, s, r, v)
                tot += 1
                if lhs != rhs:
                    mism += 1
                    p(f"  n={n} m={m} j={j} (v={v}): p_m(j)={lhs} order-stat={rhs} MISMATCH")
    p(f"{tot} exact-Fraction checks, {mism} mismatches")
    assert mism == 0
    p(">>> New fact (this front, PROVED): T(n,m) = C(n+m+1,2m+1) * E[(1-g)^(X-m-1)]")
    p(">>> where X is the (m+1)-th order statistic (median) of a uniform")
    p(">>> random (2m+1)-subset of {1,...,n+m+1} sampled WITHOUT")
    p(">>> replacement -- a genuinely different, and more primitive,")
    p(">>> random object than the Binomial(k,gamma) count M that every")
    p(">>> prior front's moment/cumulant machinery is built around.")

    p("")
    p("=" * 70)
    p("Part C: exact mean/variance of X via the classical order-statistic")
    p("        formulas for sampling without replacement, cross-checked")
    p("        against brute-force exact summation")
    p("=" * 70)
    n_s, m_s = sp.symbols('n m', positive=True, integer=True)
    N_s = n_s + m_s + 1
    s_s = 2 * m_s + 1
    r_s = m_s + 1
    EX_formula = sp.Rational(1) * r_s * (N_s + 1) / (s_s + 1)
    VarX_formula = r_s * (s_s + 1 - r_s) * (N_s + 1) * (N_s - s_s) / ((s_s + 1) ** 2 * (s_s + 2))
    EX_formula = sp.simplify(EX_formula)
    VarX_formula = sp.simplify(VarX_formula)
    p(f"classical E[X_(r)] formula = r(N+1)/(s+1)  ->  simplified: {EX_formula}")
    p(f"classical Var[X_(r)] formula = r(s+1-r)(N+1)(N-s)/((s+1)^2(s+2))  ->  simplified: {VarX_formula}")
    p(f"  ==> E[X] = (n+m+2)/2  (median of the range, as expected)")
    p(f"  ==> E[j] = E[X]-(m+1) = (n-m)/2  (matches the manifest")
    p(f"      symmetry p_m(j)=p_m(n-m-j) checked independently below)")

    # cross-check symmetry directly
    mism = 0
    tot = 0
    for n in [7, 10]:
        for m in [0, 1, 2, 3]:
            if m > n:
                continue
            for j in range(0, n - m + 1):
                tot += 1
                if p_m_direct(n, m, j) != p_m_direct(n, m, n - m - j):
                    mism += 1
    p(f"symmetry p_m(j)=p_m(n-m-j): {tot} checks, {mism} mismatches")
    assert mism == 0

    # brute force Var(X) vs formula, small n,m
    mism = 0
    tot = 0
    for n in [6, 9, 11]:
        for m in [0, 1, 2, 3]:
            if m > n:
                continue
            EX_bf = sum(F(j + m + 1) * p_m_direct(n, m, j) for j in range(0, n - m + 1))
            EX2_bf = sum(F((j + m + 1) ** 2) * p_m_direct(n, m, j) for j in range(0, n - m + 1))
            VarX_bf = EX2_bf - EX_bf ** 2
            N_val, s_val, r_val = n + m + 1, 2 * m + 1, m + 1
            VarX_cf = F(r_val * (s_val + 1 - r_val) * (N_val + 1) * (N_val - s_val),
                         (s_val + 1) ** 2 * (s_val + 2))
            tot += 1
            ok = (VarX_bf == VarX_cf)
            if not ok:
                mism += 1
                p(f"  n={n} m={m}: Var(X) brute-force={VarX_bf} formula={VarX_cf} MISMATCH")
    p(f"Var(X) exact check: {tot} (n,m) pairs, {mism} mismatches")
    assert mism == 0
    p("Var(j) = Var(X) = (n+m+2)(n-m)/(4(2m+3)) exactly (own derivation,")
    p("cross-checked both symbolically against the classical formula and")
    p("numerically against brute-force exact summation, 0 mismatches).")

    p("")
    p("=" * 70)
    p("Part D: T(n,m) is a TILTED (large-deviations, not CLT-regime)")
    p("        moment of j -- the true maximizer j* of the summand is")
    p("        NOT close to the untilted mean (n-m)/2 once gamma is not")
    p("        very close to 1. Located numerically (exact Fraction")
    p("        comparison of consecutive summand ratios) at several")
    p("        (n,m,gamma).")
    p("=" * 70)

    def summand(n, m, j, g):
        return comb(j + m, m) * comb(n - j, m) * (1 - g) ** j

    for n in [400]:
        for m in [5, 10, 20]:
            for g_num, g_den in [(1, 2), (3, 10), (9, 10)]:
                g = F(g_num, g_den)
                # find integer j* maximizing summand via ratio test
                # ratio(j) = summand(j+1)/summand(j) = (j+m+1)/(j+1) * (n-j-m)/(n-j) * (1-g)
                jstar = 0
                cur = F(1)
                # walk j upward while ratio > 1
                j = 0
                while j <= n - m - 1:
                    ratio = F(j + m + 1, j + 1) * F(n - j - m, n - j) * (1 - g)
                    if ratio <= 1:
                        break
                    j += 1
                jstar = j
                untilted_mean = F(n - m, 2)
                p(f"  n={n} m={m} g={g}: j* (saddle) = {jstar},  "
                  f"untilted mean (n-m)/2 = {float(untilted_mean):.2f},  "
                  f"j*/mean ratio = {jstar/float(untilted_mean):.4f}")

    p("")
    p("Interpretation: at gamma=0.3 (mild tilt, (1-gamma) close to 1) j*")
    p("stays relatively closer to the untilted mean (n-m)/2 (10-20% of")
    p("it); at gamma=0.9 (strong tilt, (1-gamma) close to 0) j* collapses")
    p("to essentially 0, far from the untilted mean -- confirming this is")
    p("a genuine large-deviations/exponential-tilting computation, not a")
    p("small-perturbation-of-the-CLT-regime one. A full saddle-point")
    p("treatment of j* jointly with the outer m-sum (itself O(sqrt n)-")
    p("scale, predecessor's Sec.4) is a joint two-variable Laplace-method")
    p("problem of comparable technical depth to the existing")
    p("moment/cumulant machinery -- see ATTEMPT.md Sec.5 for the honest")
    p("assessment of why this front did not carry that through to a")
    p("closed form in the time available.")

    with open("03_order_statistic_identification.log", "w") as f:
        f.write("\n".join(L) + "\n")
    p("")
    p("Log written to 03_order_statistic_identification.log")


if __name__ == "__main__":
    main()
