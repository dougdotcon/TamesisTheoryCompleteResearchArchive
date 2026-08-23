"""
validate_third_order.py -- error_constant_growth_attempt (DISC-DEC-045, front (b))

Purpose: establish, against the EXACT discrete chain, that the newly-derived
third-order pair (H_r, L_r) is the correct 1/n^2 term -- i.e. that

    n^2 R_r(m,b,n)  ->  H_r(t,b)      uniformly in t = m/n,
    n^2 eps^h_r(a,b,n) -> L_r(s,b)    uniformly in s = a/n,

by checking that the once-more-subtracted residuals

    R^{(3)}_r := R_r - H_r(t,b)/n^2      and     eps^h_r - L_r(s,b)/n^2

are O(1/n^3), i.e. that  n^3 * |R^{(3)}|  stays bounded as n grows.

Everything below is exact fractions.Fraction arithmetic.  Floats appear ONLY in
the printed columns, for human readability of trends.

STEP 0 additionally revalidates my independent Chain simulator against facts
proved ELSEWHERE in the lineage (wave 5's exact psi_n^{(1)}, psi_n^{(2)}), so
that agreement below is not agreement of a script with itself.
"""

from fractions import Fraction as Fr
import core as C


def fmax(vals):
    """max over an iterable of Fractions of |v|, returned exactly."""
    best = Fr(-1)
    arg = None
    for k, v in vals:
        a = abs(v)
        if a > best:
            best, arg = a, k
    return (best if best >= 0 else Fr(0)), arg


print("=" * 78)
print("STEP 0.  Independent validation of my own Chain simulator against")
print("         facts PROVED elsewhere in the lineage (not against this attempt).")
print("=" * 78)
ok = True
for n in range(2, 9):
    ch = C.Chain(n)
    got = ch.g(1, n, 0)                     # psi_n^{(1)} = g_1(n,0)
    want = Fr(4 * n + 1, 6 * n)             # wave 5, PROVED
    m = (got == want)
    ok &= m
    print("  K=1 n=%d : g_1(n,0)=%-14s (4n+1)/(6n)=%-14s match=%s" % (n, got, want, m))
for n in range(3, 9):
    ch = C.Chain(n)
    got = ch.g(2, n, 0)
    want = Fr(8 * n * n + 4 * n + 1, 15 * n * n)   # wave 5, PROVED
    m = (got == want)
    ok &= m
    print("  K=2 n=%d : g_2(n,0)=%-18s (8n^2+4n+1)/(15n^2)=%-18s match=%s" % (n, got, want, m))
# the single independently-brute-forced value quoted by the wave-8 referee
ch = C.Chain(7)
got = ch.g(6, 7, 0)
want = Fr(355081, 823543)
print("  K=6 n=7 : g_6(7,0)=%s   brute-force reference 355081/823543  match=%s"
      % (got, got == want))
ok &= (got == want)
print("  STEP 0 all exact matches:", ok)

print()
print("=" * 78)
print("STEP 1.  n^2 * max_m |R_r(m,b,n)|  vs  max_t |H_r(t,b)| over the grid.")
print("         (exhaustive over every valid m, not a sample)")
print("=" * 78)
for (r, b) in [(2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (3, 1), (4, 1), (5, 1), (4, 2)]:
    print("  r=%d b=%d   H_r(t,b) = %s" % (r, b, C.H(r, b)))
    for n in [40, 80, 160, 320]:
        if n < b + r + 1:
            continue
        ch = C.Chain(n)
        vals = [(m, C.R_resid(ch, r, m, b)) for m in range(b + r + 1, n + 1)]
        best, arg = fmax(vals)
        # grid max of |H_r|
        gh, ghm = fmax([(m, C.H(r, b).eval(Fr(m, n))) for m in range(b + r + 1, n + 1)])
        print("     n=%4d  max_m n^2|R| = %.9f (at t=%.4f)   max_grid|H_r| = %.9f (t=%.4f)"
              % (n, float(best) * n * n, arg / n, float(gh), ghm / n))
    print()

print("=" * 78)
print("STEP 2.  The decisive test: is  R_r - H_r/n^2  really O(1/n^3)?")
print("         If n^3 * max_m |R^(3)| stabilises, the 1/n^2 term is exactly H_r.")
print("=" * 78)
for (r, b) in [(2, 0), (3, 0), (4, 0), (5, 0), (3, 1), (4, 2)]:
    row = []
    for n in [40, 80, 160, 320, 640]:
        if n < b + r + 1:
            continue
        ch = C.Chain(n)
        best, arg = fmax([(m, C.R3_resid(ch, r, m, b)) for m in range(b + r + 1, n + 1)])
        row.append((n, float(best) * n ** 3, arg / n))
    print("  r=%d b=%d :" % (r, b), "  ".join("n=%d: %.6f (t=%.3f)" % x for x in row))

print()
print("=" * 78)
print("STEP 3.  Same for the h-side: is  eps^h_r - L_r/n^2  really O(1/n^3)?")
print("=" * 78)
for (r, b) in [(1, 0), (2, 0), (3, 0), (4, 0), (2, 1), (3, 2)]:
    row = []
    for n in [40, 80, 160, 320]:
        ch = C.Chain(n)
        amax = n - b - r - 1
        best, arg = fmax([(a, C.eps_h3_resid(ch, r, a, b)) for a in range(0, amax + 1)])
        row.append((n, float(best) * n ** 3, arg / n))
    print("  r=%d b=%d :" % (r, b), "  ".join("n=%d: %.6f (s=%.3f)" % x for x in row))

print()
print("=" * 78)
print("STEP 4.  Exact-identity spot checks (not convergence -- exact equality).")
print("=" * 78)
# H_1 == 0 predicts R_1 == 0 exactly; H_2(.,0)=1/15 predicts R_2 = 1/(15 n^2) exactly.
bad = 0
tot = 0
for n in range(3, 30):
    ch = C.Chain(n)
    for b in (0, 1, 2):
        for m in range(b + 2, n + 1):
            tot += 1
            if C.R_resid(ch, 1, m, b) != 0:
                bad += 1
print("  R_1(m,b,n) == 0 exactly:  %d/%d checks, %d failures" % (tot - bad, tot, bad))
bad = 0
tot = 0
for n in range(4, 30):
    ch = C.Chain(n)
    for m in range(3, n + 1):
        tot += 1
        if C.R_resid(ch, 2, m, 0) != Fr(1, 15 * n * n):
            bad += 1
print("  R_2(m,0,n) == 1/(15n^2) exactly:  %d/%d checks, %d failures" % (tot - bad, tot, bad))
# and the general prediction R_2(m,b,n) == H_2(t,b)/n^2 exactly for every b
bad = 0
tot = 0
for n in range(5, 26):
    ch = C.Chain(n)
    for b in (0, 1, 2, 3):
        for m in range(b + 3, n + 1):
            tot += 1
            if C.R_resid(ch, 2, m, b) != C.H(2, b).eval(Fr(m, n)) / (n * n):
                bad += 1
print("  R_2(m,b,n) == H_2(t,b)/n^2 exactly (b=0..3):  %d/%d, %d failures" % (tot - bad, tot, bad))
for b in range(0, 5):
    print("     H_2(t,%d) = %s" % (b, C.H(2, b)))
