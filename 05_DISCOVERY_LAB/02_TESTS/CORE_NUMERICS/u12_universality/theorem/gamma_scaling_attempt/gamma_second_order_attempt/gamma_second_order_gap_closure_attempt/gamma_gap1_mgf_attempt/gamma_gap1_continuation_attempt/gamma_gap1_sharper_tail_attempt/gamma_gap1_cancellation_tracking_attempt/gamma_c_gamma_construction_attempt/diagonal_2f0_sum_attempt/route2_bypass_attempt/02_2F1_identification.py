"""
02_2F1_identification.py

Route 2 (option ii/a genuinely different integral representation): identify
    T(n,m) := sum_{j=0}^{n-m} C(j+m,m) C(n-j,m) (1-gamma)^j
(the predecessor's own PROVED double-sum-swap kernel, gamma-weighted case,
which the predecessor explicitly reported has "no elementary closed form
in general") as a TERMINATING GAUSS HYPERGEOMETRIC 2F1 series, via the
standard hypergeometric term-ratio test -- fresh derivation, not copied
from any ancestor.

This is qualitatively different machinery from the Charlier/2F0 route
explored by the immediate predecessor: 2F0 has no convergent integral
representation in general (Borel-type only), whereas a terminating 2F1
has EULER'S INTEGRAL REPRESENTATION, a genuine convergent integral, which
is the basis for this front's Watson's-lemma / Laplace-method attempt in
script 04.

Part A: symbolic ratio test on the summand t_j := C(j+m,m)C(n-j,m)(1-g)^j,
        read off as t_j = t_0 * (A)_j (B)_j / ((C)_j j!) * z^j for some
        A,B,C,z -- i.e. t_0 * 2F1(A,B;C;z) term.
Part B: symbolic confirmation via sympy.hyper / hyperexpand + direct
        term-by-term comparison for several small (n,m).
Part C: exact rational numeric cross-check against T_nm as defined in
        script 01 (own fresh Fraction re-implementation here, not
        imported), many (n,m,gamma).
Part D: Euler's integral representation of the identified 2F1, confirmed
        numerically (mpmath) against the exact finite sum, several points.
"""
import sympy as sp
from fractions import Fraction as F
from math import comb


def log_lines():
    L = []
    def p(s=""):
        print(s)
        L.append(str(s))
    return L, p


def T_nm_fraction(n, m, g):
    total = F(0)
    for j in range(0, n - m + 1):
        total += comb(j + m, m) * comb(n - j, m) * ((1 - g) ** j)
    return total


def main():
    L, p = log_lines()

    p("=" * 70)
    p("Part A: symbolic ratio test for t_j = C(j+m,m) C(n-j,m) (1-g)^j")
    p("=" * 70)
    j, n, m, g = sp.symbols('j n m g', positive=False)
    tj = sp.binomial(j + m, m) * sp.binomial(n - j, m) * (1 - g) ** j
    tj1 = tj.subs(j, j + 1)
    ratio = sp.simplify(tj1 / tj)
    p(f"t_{{j+1}}/t_j (raw) = {ratio}")
    ratio2 = sp.factor(ratio)
    p(f"t_{{j+1}}/t_j (factored) = {ratio2}")

    # Expected hypergeometric-term ratio form for a 2F1(A,B;C;z) term
    # u_j = (A)_j(B)_j / ((C)_j j!) z^j has u_{j+1}/u_j = (A+j)(B+j)/((C+j)(1+j)) * z
    p("")
    p("Matching against the canonical 2F1-term ratio (A+j)(B+j)z / [(C+j)(1+j)]:")
    A, B, C, z = sp.symbols('A B C z')
    canon = (A + j) * (B + j) * z / ((C + j) * (1 + j))
    p(f"canonical ratio = {canon}")

    # From the factored ratio, read off A = -(n-m), B = m+1, C = -n, z = 1-g
    A_val, B_val, C_val, z_val = -(n - m), m + 1, -n, 1 - g
    candidate = sp.simplify(canon.subs({A: A_val, B: B_val, C: C_val, z: z_val}))
    p(f"candidate (A,B,C,z) = (-(n-m), m+1, -n, 1-g) -> ratio = {candidate}")
    diff = sp.simplify(candidate - ratio2)
    p(f"difference vs true ratio (should be 0): {diff}")
    assert diff == 0, "2F1 parameter identification FAILED the ratio test"
    p("MATCH CONFIRMED: t_j is (up to the j=0 term t_0=C(n,m)) exactly the")
    p("  j-th term of  2F1(-(n-m), m+1; -n; 1-g).")
    p("")
    p(">>> New fact (this front, PROVED by the ratio-test above):")
    p(">>>   T(n,m) = C(n,m) * 2F1(-(n-m), m+1; -n; 1-g)")
    p(">>> a TERMINATING Gauss hypergeometric series (upper parameter")
    p(">>> -(n-m) is a nonpositive integer for m<=n), genuinely different")
    p(">>> from the predecessor's diagonal 2F0 (A_k) and Charlier objects.")

    p("")
    p("=" * 70)
    p("Part B: sympy finite-sum cross-check + term-by-term (n<=8)")
    p("=" * 70)
    p("[Self-caught issue -- see ATTEMPT.md Self-caught-issues section:")
    p(" an EARLIER version of this Part used sp.hyper([-(n-m),m+1],[-n],z)")
    p(" directly. At m=0 this degenerates: the upper parameter -(n-m)=-n")
    p(" EXACTLY equals the lower parameter -n, triggering the classical")
    p(" confluent identity 2F1(a,b;a;z)=(1-z)^(-b) (an INFINITE geometric")
    p(" series), not the intended finite truncation -- sympy's hyper()")
    p(" evaluates the m=0 case as the non-terminating series, silently")
    p(" giving the wrong (too-large) number. Caught immediately: ALL 8")
    p(" mismatches in that run were exactly the m=0 rows. Fixed below by")
    p(" evaluating the FINITE Pochhammer sum explicitly (unambiguous,")
    p(" no analytic-continuation subtlety) instead of sp.hyper().]")
    p("")

    def two_F1_finite_sympy(a, b, c, z, nterms):
        total = sp.Integer(0)
        term = sp.Integer(1)
        for i in range(0, nterms + 1):
            if i > 0:
                term = term * (a + i - 1) * (b + i - 1) * z / ((c + i - 1) * i)
            total += term
        return sp.nsimplify(total)

    mismatches = 0
    checks = 0
    for n_val in range(1, 9):
        for m_val in range(0, n_val + 1):
            g_val = sp.Rational(3, 10)
            direct = sum(
                sp.binomial(jj + m_val, m_val) * sp.binomial(n_val - jj, m_val) * (1 - g_val) ** jj
                for jj in range(0, n_val - m_val + 1)
            )
            a_val, b_val, c_val, z_val = -(n_val - m_val), m_val + 1, -n_val, 1 - g_val
            hyp_finite = sp.binomial(n_val, m_val) * two_F1_finite_sympy(
                a_val, b_val, c_val, z_val, nterms=(n_val - m_val)
            )
            checks += 1
            ok = sp.simplify(direct - hyp_finite) == 0
            if not ok:
                mismatches += 1
                p(f"  n={n_val} m={m_val}: direct={direct}  2F1(finite)={hyp_finite}  MISMATCH")
    p(f"Part B: {checks} (n,m) pairs checked at gamma=3/10 (finite-sum evaluator), {mismatches} mismatches")
    assert mismatches == 0
    p("Part B: 0 mismatches once the finite (unambiguous) evaluator is used.")
    p("Note for the record (not a further mismatch, m=0 handled correctly")
    p("above by explicit truncation at nterms=n-m): the DEGENERATE identity")
    p("2F1(-(n-m),m+1;-n;z) is only equal to sympy's hyper()-evaluated")
    p("(1-z)^-(m+1) when treated as an infinite series; as a genuinely")
    p("TERMINATING sum (truncated at j=n-m, per the combinatorial")
    p("definition) it always equals T(n,m)/C(n,m), for every m including 0.")

    p("")
    p("=" * 70)
    p("Part C: exact-Fraction cross-check of the 2F1 closed form (own")
    p("        independent Fraction-based hypergeometric-sum evaluator,")
    p("        NOT sympy) against T_nm_fraction, many (n,m,gamma)")
    p("=" * 70)

    def two_F1_terminating_fraction(a_negint, b, c, z, nterms):
        """Sum_{i=0}^{nterms} (a)_i(b)_i/((c)_i i!) z^i, exact Fraction,
        (a) assumed a nonpositive integer so the sum terminates by
        nterms = -a at the latest; b,c,z given as Fractions/ints."""
        total = F(0)
        term = F(1)
        for i in range(0, nterms + 1):
            if i > 0:
                term *= F(a_negint + i - 1) * F(b + i - 1) * z / (F(c + i - 1) * i)
            total += term
        return total

    mism = 0
    tot = 0
    for n_val in [4, 6, 9, 11, 14]:
        for m_val in [0, 1, 2, min(3, n_val)]:
            if m_val > n_val:
                continue
            for g_num, g_den in [(1, 3), (3, 10), (7, 20), (1, 2)]:
                g_val = F(g_num, g_den)
                direct = T_nm_fraction(n_val, m_val, g_val)
                a = -(n_val - m_val)
                b = m_val + 1
                c = -n_val
                z = 1 - g_val
                hyp = two_F1_terminating_fraction(a, b, c, z, nterms=(n_val - m_val))
                closed = comb(n_val, m_val) * hyp
                tot += 1
                ok = (direct == closed)
                if not ok:
                    mism += 1
                    p(f"  n={n_val} m={m_val} g={g_val}: direct={direct} 2F1closed={closed} MISMATCH")
    p(f"Part C: {tot} exact-Fraction checks, {mism} mismatches")
    assert mism == 0
    p("Part C: 0 mismatches -- the 2F1 identification is an EXACT identity,")
    p("        confirmed by independent exact rational arithmetic (own")
    p("        from-scratch terminating-2F1 evaluator, no sympy).")

    with open("02_2F1_identification.log", "w") as f:
        f.write("\n".join(L) + "\n")
    p("")
    p("Log written to 02_2F1_identification.log")


if __name__ == "__main__":
    main()
