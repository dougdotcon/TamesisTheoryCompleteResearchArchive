"""
06_mpmath_2F1_route_numerics.py

Fresh, independent high-precision (mpmath) numerical evaluation of
S_n(gamma) via THIS FRONT'S OWN new representation (script 02): the
terminating Gauss hypergeometric closed form for T(n,m), fed through the
predecessor's PROVED (independently re-verified in this front's script
01) double-sum-swap identity

    S_n'(g) = 1 + S_n(g) = sum_{m=0}^n (g^m/n^m) m! * C(n,m) * 2F1(-(n-m), m+1; -n; 1-g)

evaluated via mpmath.hyp2f1 -- a genuinely different COMPUTATIONAL
ALGORITHM (calls a hypergeometric-function library routine per term,
not a raw double sum over j) than anything any ancestor/predecessor in
this lineage used, even though it targets the same final quantity.

Part 0: sanity gate -- mpmath.hyp2f1 at the (a=-(n-m), b=m+1, c=-n)
        terminating parameters reproduces exact small-(n,m) values from
        script 01/03 to full precision, at several points, BEFORE
        trusting it for any large-n claim.
Part 1: R_n := phi(n,gamma n)/phi_infty(gamma n) at gamma=0.5, several
        n, cross-checked against the wave-17 ATTEMPT.md's own printed
        table value at n=2^18 (a bit-for-bit-style independent
        reproduction check, using an ENTIRELY different code path: this
        front never opened that front's script, only its printed
        numbers, which are quoted verbatim in THIS front's own required
        reading (ATTEMPT.md Sec.0 item 5) and here re-derived via a
        computational route (2F1 term-by-term via mpmath.hyp2f1) that
        shares no code with either the wave-17 front or the immediate
        predecessor's swap-route script 05).
"""
import mpmath as mp

mp.mp.dps = 40


def phi_infty(c):
    # phi_infty(c) = (sqrt(pi)/2) c^{-1/2} erf(sqrt(c))  [THEOREM.md
    # Theorem 1, cited, PROVED there; re-typed here from the formula
    # quoted in the required-reading ATTEMPT.md's, not imported]
    c = mp.mpf(c)
    return (mp.sqrt(mp.pi) / 2) * c ** mp.mpf('-0.5') * mp.erf(mp.sqrt(c))


def S_n_prime_via_2F1(n, g):
    """S_n' = sum_m (g/n)^m m! C(n,m) 2F1(-(n-m), m+1; -n; 1-g),
    via mpmath.hyp2f1 term by term. n: int, g: mpf in (0,1)."""
    g = mp.mpf(g)
    total = mp.mpf(0)
    for m in range(0, n + 1):
        a = -(n - m)
        b = m + 1
        c = -n
        z = 1 - g
        term_2F1 = mp.hyp2f1(a, b, c, z)
        coeff = (g / n) ** m * mp.factorial(m) * mp.binomial(n, m)
        term = coeff * term_2F1
        total += term
        # early stop once terms are utterly negligible and staying so
        if m > 30 and abs(term) < mp.mpf(10) ** (-int(mp.mp.dps) + 5) * abs(total):
            # confirm with a further look-ahead before stopping
            look_ahead_negligible = True
            for extra in range(1, 6):
                mm = m + extra
                if mm > n:
                    break
                aa, bb, cc = -(n - mm), mm + 1, -n
                t2 = mp.hyp2f1(aa, bb, cc, z)
                coeff2 = (g / n) ** mm * mp.factorial(mm) * mp.binomial(n, mm)
                if abs(coeff2 * t2) > mp.mpf(10) ** (-int(mp.mp.dps) + 5) * abs(total):
                    look_ahead_negligible = False
                    break
            if look_ahead_negligible:
                break
    return total


def main():
    L = []
    def p(s=""):
        print(s)
        L.append(str(s))

    p("=" * 70)
    p("Part 0: sanity gate against exact small-(n,gamma) values from")
    p("        scripts 01/03 (Fraction arithmetic) before trusting")
    p("        mpmath.hyp2f1 for anything larger")
    p("=" * 70)
    from fractions import Fraction as F
    from math import comb

    def S_n_exact(n, g):
        total = F(0)
        for k in range(1, n + 1):
            ak = F(0)
            prod = F(1)
            for m in range(0, k + 1):
                if m > 0:
                    prod *= F(n - k + m, n)
                ak += comb(k, m) * (g ** m) * ((1 - g) ** (k - m)) * prod
            total += ak
        return total

    max_err = mp.mpf(0)
    for n, g_num, g_den in [(5, 1, 4), (8, 2, 9), (12, 3, 10), (15, 1, 2)]:
        g_exact = F(g_num, g_den)
        exact_val = mp.mpf(1) + mp.mpf(S_n_exact(n, g_exact).numerator) / mp.mpf(S_n_exact(n, g_exact).denominator)
        mp_val = S_n_prime_via_2F1(n, mp.mpf(g_num) / mp.mpf(g_den))
        err = abs(exact_val - mp_val)
        max_err = max(max_err, err)
        p(f"  n={n} g={g_num}/{g_den}: exact(1+S_n)={mp.nstr(exact_val,20)}  "
          f"mpmath-2F1={mp.nstr(mp_val,20)}  |err|={mp.nstr(err,5)}")
    p(f"max |err| over gate = {mp.nstr(max_err,5)}")
    assert max_err < mp.mpf('1e-30'), "mpmath.hyp2f1 route FAILED the exact sanity gate"
    p("Gate PASSED -- mpmath.hyp2f1-based evaluator matches exact values.")

    p("")
    p("=" * 70)
    p("Part 1: R_n at gamma=1/2, growing n, compared against the")
    p("        wave-17 ATTEMPT.md's own printed n=2^18 table value")
    p("        (required reading; quoted, not copied code)")
    p("=" * 70)
    g = mp.mpf('0.5')
    target_T = mp.sqrt(mp.mpf(2) / (mp.mpf(2) - g))
    C_gamma_closed = -(mp.mpf(2) / (3 * mp.sqrt(mp.pi))) * mp.sqrt(g) * (6 - 8 * g + 3 * g ** 2) / (2 - g) ** 2
    p(f"target T(0.5) = {mp.nstr(target_T, 15)},  C(0.5) closed form = {mp.nstr(C_gamma_closed, 15)}")
    rows = []
    for n in [2 ** 8, 2 ** 10, 2 ** 12, 2 ** 14, 2 ** 16, 2 ** 18]:
        Sn_prime = S_n_prime_via_2F1(n, g)
        Sn = Sn_prime - 1
        phi_n = Sn / n
        phi_inf = phi_infty(g * n)
        Rn = phi_n / phi_inf
        rows.append((n, Rn))
        p(f"  n={n:>7d}: R_n = {mp.nstr(Rn, 14)}   sqrt(n)(R_n-T) = {mp.nstr(mp.sqrt(n)*(Rn-target_T), 10)}")

    p("")
    p("Cross-check against wave-17 ATTEMPT.md Sec.7.1's OWN printed value")
    p("at n=2^18=262144, gamma=0.5: R(262144,0.5) = 1.1540659874 (quoted)")
    n_final, Rn_final = rows[-1]
    p(f"  This front (2F1/mpmath route): R_n at n={n_final} = {mp.nstr(Rn_final, 12)}")
    diff = abs(Rn_final - mp.mpf('1.1540659874'))
    p(f"  |difference| = {mp.nstr(diff, 5)}")
    assert diff < mp.mpf('1e-9')
    p("MATCH to the quoted digits -- independent confirmation, via a")
    p("computational route (mpmath.hyp2f1 term-by-term on this front's")
    p("own new 2F1 identity for T(n,m)) that shares no code with the")
    p("wave-17 front, the immediate predecessor, or any other ancestor.")

    p("")
    p("Richardson extrapolation (2-point, n=2^16,2^18; model x_n=C+b/sqrt n):")
    n1, R1 = 2 ** 16, dict(rows)[2 ** 16]
    n2, R2 = 2 ** 18, dict(rows)[2 ** 18]
    x1 = mp.sqrt(n1) * (R1 - target_T)
    x2 = mp.sqrt(n2) * (R2 - target_T)
    # x_n = C + b/sqrt(n)  =>  solve 2x2 linear system
    s1 = 1 / mp.sqrt(n1)
    s2 = 1 / mp.sqrt(n2)
    C_extrap = (x1 * s2 - x2 * s1) / (s2 - s1)
    p(f"  C_extrap = {mp.nstr(C_extrap, 10)}   vs closed form C(0.5) = {mp.nstr(C_gamma_closed, 10)}")
    p(f"  |diff| = {mp.nstr(abs(C_extrap - C_gamma_closed), 5)}")

    with open("06_mpmath_2F1_route_numerics.log", "w") as f:
        f.write("\n".join(L) + "\n")
    p("")
    p("Log written to 06_mpmath_2F1_route_numerics.log")


if __name__ == "__main__":
    main()
