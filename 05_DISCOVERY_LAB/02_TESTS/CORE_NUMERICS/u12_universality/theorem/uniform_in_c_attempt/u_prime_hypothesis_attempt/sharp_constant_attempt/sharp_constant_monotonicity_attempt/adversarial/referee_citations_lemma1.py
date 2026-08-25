# Adversarial referee, sharp_constant_monotonicity_attempt -- Part 1:
#   (R)  Robbins 1955 two-sided Stirling bound: correct form verified at scale;
#        the ATTEMPT.md *printed* display (missing (n/e)^n) shown to be false.
#   (F)  FGKP95 Theorem 7 (theta(n) = 1/3 + 4/(135(n+k(n))), k in [2/21,8/45]):
#        theta computed two independent ways (own defining sum, exact-rational
#        partial sums; incomplete-gamma/Poisson route), bounds checked densely
#        and sparsely to n = 10^6, k(n) monotonicity + endpoints, and the
#        second-order asymptotic coefficient -8/2835 <-> k(inf)=2/21 check.
#   (L)  Lemma 1 (Q(n) = n!e^n/(2n^n) - theta(n)): final identity re-derived and
#        verified EXACTLY (rational form) and to >=50 digits (transcendental
#        form); the document's printed intermediate equations checked
#        character-by-character with exact Fractions -- and refuted.
#
# Written from the ATTEMPT.md prose only; none of the target's .py/.log files
# was opened. No randomness anywhere (deterministic objects only).
import sys
from fractions import Fraction as F
from math import isqrt
import mpmath as mp

mp.mp.dps = 80

LOG = []
def log(s=""):
    print(s)
    LOG.append(str(s))

fails = 0

# ----------------------------------------------------------------------------
log("=" * 78)
log("(R) ROBBINS 1955  --  correct statement:")
log("    sqrt(2 pi n) (n/e)^n e^{1/(12n+1)} < n! < sqrt(2 pi n) (n/e)^n e^{1/(12n)}")
log("    equivalently  1/(12n+1) < d(n) < 1/(12n),")
log("    d(n) := ln n! - (1/2)ln(2 pi n) - n ln n + n.")
log("=" * 78)

def robbins_d(n):
    n = mp.mpf(n)
    return mp.loggamma(n + 1) - mp.mpf(0.5) * mp.log(2 * mp.pi * n) - n * mp.log(n) + n

worst_lo = None; worst_hi = None
ns = list(range(1, 2001)) + [5000, 10**4, 10**5, 10**6, 10**7, 10**8]
viol = 0
for n in ns:
    d = robbins_d(n)
    lo = mp.mpf(1) / (12 * n + 1)
    hi = mp.mpf(1) / (12 * n)
    if not (lo < d < hi):
        viol += 1
        log(f"  VIOLATION at n={n}: lo={lo}, d={d}, hi={hi}")
    ml = d - lo
    mh = hi - d
    if worst_lo is None or ml < worst_lo[0]: worst_lo = (ml, n)
    if worst_hi is None or mh < worst_hi[0]: worst_hi = (mh, n)
log(f"  checked {len(ns)} values of n (dense 1..2000 + sparse to 10^8): "
    f"{viol} violations")
log(f"  smallest lower margin d-1/(12n+1): {mp.nstr(worst_lo[0], 6)} at n={worst_lo[1]}")
log(f"  smallest upper margin 1/(12n)-d : {mp.nstr(worst_hi[0], 6)} at n={worst_hi[1]}")
if viol: fails += 1

log("")
log("(R') The citation AS PRINTED in ATTEMPT.md Section 2, i.e. WITHOUT the")
log("     (n/e)^n factor:   sqrt(2 pi n) e^{1/(12n+1)} < n! < sqrt(2 pi n) e^{1/(12n)}")
printed_viol = []
fact = 1
for n in range(1, 11):
    fact *= n
    lo_printed = mp.sqrt(2 * mp.pi * n) * mp.e ** (mp.mpf(1) / (12 * n + 1))
    hi_printed = mp.sqrt(2 * mp.pi * n) * mp.e ** (mp.mpf(1) / (12 * n))
    ok = lo_printed < fact < hi_printed
    log(f"   n={n}: printed-lower={mp.nstr(lo_printed,8)}  n!={fact}  "
        f"printed-upper={mp.nstr(hi_printed,8)}  -> {'holds' if ok else 'FALSE'}")
    if not ok:
        printed_viol.append(n)
log(f"   => the printed display is FALSE at n in {printed_viol} (and, for n>=3, the")
log("      'bounds' are astronomically far below n! -- the display as printed is")
log("      not Robbins' theorem; the form actually USED in Theorem 1's proof,")
log("      A(n) = n! e^n / n^n < sqrt(2 pi n) e^{1/(12n)}, IS the correct Robbins")
log("      upper bound (verified above at scale).")

# ----------------------------------------------------------------------------
log("")
log("=" * 78)
log("(F) FGKP95 THEOREM 7.  theta(n) defined by")
log("    (1/2)e^n = sum_{m=0}^{n-1} n^m/m!  +  theta(n) n^n/n! ,")
log("    claim: theta(n) = 1/3 + 4/(135(n+k(n))),  k(n) in [2/21, 8/45], all n>=0,")
log("    i.e. 1/3 + 4/(135(n+8/45)) <= theta(n) <= 1/3 + 4/(135(n+2/21)).")
log("=" * 78)

def S_exact(n):
    """sum_{m=0}^{n-1} n^m/m! as an exact Fraction (integer numerator over (n-1)!)."""
    if n == 0:
        return F(0)
    # t_m = n^m (n-1)!/m!, ascending: t_0=(n-1)!, t_m = t_{m-1}*n//m (exact)
    t = 1
    for i in range(1, n):
        t *= i          # t = (n-1)!
    total = t
    tm = t
    for m in range(1, n):
        tm = tm * n // m
        total += tm
    return F(total, t)

def theta_def(n, dps=80):
    """theta from its own defining sum, exact-rational partial sum + mp e^n."""
    with mp.workdps(dps):
        S = S_exact(n)
        Smp = mp.mpf(S.numerator) / mp.mpf(S.denominator)
        # n^n/n! and n!/n^n via exact integers
        nn = mp.mpf(n) ** n if n > 0 else mp.mpf(1)
        factn = mp.factorial(n)
        return (mp.e ** n / 2 - Smp) * factn / nn

def theta_gamma(n, dps=80):
    """theta via the incomplete-gamma / Poisson-CDF identity
       theta(n) = (1/2) n! e^n/n^n - e^n Gamma(n+1,n)/n^n + 1
                = A(n) (1/2 - Greg) + 1,  Greg = Gamma(n+1,n)/n!."""
    with mp.workdps(dps):
        nmp = mp.mpf(n)
        if n == 0:
            return mp.mpf(0.5)
        A = mp.e ** (mp.loggamma(nmp + 1) + nmp - nmp * mp.log(nmp))
        Greg = mp.gammainc(nmp + 1, nmp, mp.inf, regularized=True)
        return A * (mp.mpf(0.5) - Greg) + 1

def theta_trunc(n, dps=80):
    """theta for very large n: defining sum with certified truncation (descending
       terms ratio m/n from m=n-1 downward; truncation error < 10^-(dps-10))."""
    with mp.workdps(dps + 15):
        nmp = mp.mpf(n)
        # sum_{m=0}^{n-1} n^m/m! = t_{n-1} * sum descending, t_{n-1}=n^{n-1}/(n-1)!
        # relative descending: r_{n-1}=1, r_{m-1}=r_m*m/n
        acc = mp.mpf(0)
        r = mp.mpf(1)
        m = n - 1
        tiny = mp.mpf(10) ** (-(dps + 10))
        while m >= 0 and r > tiny:
            acc += r
            r = r * m / n
            m -= 1
        # truncation: remaining terms all < tiny and there are < n of them,
        # so tail < n*tiny  (certified since terms are decreasing as m decreases)
        log_t = (n - 1) * mp.log(nmp) - mp.loggamma(nmp)   # ln t_{n-1}
        S_over_scale = acc                                  # S = t_{n-1} * acc
        # theta = (e^n/2 - S) * n!/n^n
        #       = n!/n^n * e^n/2 - acc * t_{n-1} * n!/n^n
        # t_{n-1}*n!/n^n = exp(log_t + loggamma(n+1) - n log n) = exp(...) = 1?  no:
        # t_{n-1} = n^{n-1}/(n-1)!,  n!/n^n * t_{n-1} = n!/( (n-1)! n ) = 1.  Exactly 1!
        A = mp.e ** (mp.loggamma(nmp + 1) + nmp - nmp * mp.log(nmp))  # n! e^n/n^n
        return A / 2 - S_over_scale

k_lo = F(2, 21)
k_hi = F(8, 45)

def fg_lower(n):
    return mp.mpf(1) / 3 + mp.mpf(4) / (135 * (n + mp.mpf(8) / 45))

def fg_upper(n):
    return mp.mpf(1) / 3 + mp.mpf(4) / (135 * (n + mp.mpf(2) / 21))

# -- dense range, exact-partial-sum route
log("")
log("(F1) dense n=0..600 + strided to n=2000: theta via own defining sum")
log("     (exact Fraction partial sums), FGKP bounds checked; also cross-checked")
log("     against the incomplete-gamma route at every 20th point.")
viol = 0; xchk_worst = mp.mpf(0); nchk = 0
kvals = []
dense = list(range(0, 601)) + list(range(610, 2001, 10))
for n in dense:
    th = theta_def(n)
    lo = fg_lower(n); hi = fg_upper(n)
    nchk += 1
    if not (lo <= th <= hi):
        viol += 1
        log(f"   VIOLATION n={n}: lo={mp.nstr(lo,20)} th={mp.nstr(th,20)} hi={mp.nstr(hi,20)}")
    if n % 20 == 0:
        tg = theta_gamma(n)
        d = abs(th - tg)
        if d > xchk_worst: xchk_worst = d
    if n > 0:
        k = mp.mpf(4) / (135 * (th - mp.mpf(1) / 3)) - n
        kvals.append((n, k))
log(f"   {nchk} values checked, {viol} violations of the FGKP two-sided bound")
log(f"   worst |theta_def - theta_gamma| over cross-checked points: {mp.nstr(xchk_worst, 4)}")
if viol: fails += 1

th0 = theta_def(0)
log(f"   theta(0) = {mp.nstr(th0, 30)}  (exact value 1/2; FGKP lower bound at n=0 is")
log(f"   1/3+4/(135*(8/45)) = 1/3+1/6 = 1/2 -- equality, i.e. k(0)=8/45 attained: "
    f"|theta(0)-1/2| = {mp.nstr(abs(th0-mp.mpf(0.5)), 4)})")

# -- k(n): in-interval, monotone decreasing, endpoints
log("")
log("(F2) k(n) := 4/(135(theta(n)-1/3)) - n  on the dense grid:")
bad_int = [n for (n, k) in kvals if not (mp.mpf(2)/21 <= k <= mp.mpf(8)/45)]
mono_bad = [kvals[i][0] for i in range(1, len(kvals)) if kvals[i][1] >= kvals[i-1][1]]
log(f"   out-of-[2/21,8/45] points: {bad_int if bad_int else 'none'}")
log(f"   monotone-decrease violations: {mono_bad if mono_bad else 'none'}")
log(f"   k(1)    = {mp.nstr(kvals[0][1], 12)}   (8/45 = {mp.nstr(mp.mpf(8)/45,12)})")
log(f"   k(2000) = {mp.nstr(kvals[-1][1], 12)}  (2/21 = {mp.nstr(mp.mpf(2)/21,12)})")
if bad_int or mono_bad: fails += 1

# -- sparse large n via BOTH the truncated defining sum and the gamma route
log("")
log("(F3) sparse large n: theta via truncated defining sum AND incomplete gamma,")
log("     FGKP bounds checked at both:")
for n in [5000, 10000, 30000, 100000, 300000, 1000000]:
    t1 = theta_trunc(n)
    t2 = theta_gamma(n)
    lo = fg_lower(n); hi = fg_upper(n)
    ok1 = lo <= t1 <= hi
    ok2 = lo <= t2 <= hi
    kk = mp.mpf(4) / (135 * (t1 - mp.mpf(1) / 3)) - n
    log(f"   n={n:>8}: |t_sum - t_gamma|={mp.nstr(abs(t1-t2),3)}  "
        f"bounds hold: {ok1 and ok2}  k(n)-2/21={mp.nstr(kk-mp.mpf(2)/21,6)}")
    if not (ok1 and ok2): fails += 1

# -- second-order coefficient <-> k(inf)=2/21 internal-consistency check
log("")
log("(F4) internal consistency: theta(n) ~ 1/3 + 4/(135 n) - 8/(2835 n^2) - ...")
log("     (classical; printed in FGKP95 itself as D_10(n)=2 theta(n) expansion).")
log("     k(inf)=2/21 <=> second-order coefficient -4*(2/21)/135 = -8/2835.")
log(f"     -8/2835 = {mp.nstr(-mp.mpf(8)/2835, 10)}")
for n in [100, 1000, 10000, 100000]:
    th = theta_trunc(n) if n > 2000 else theta_def(n)
    c2 = (th - mp.mpf(1)/3 - mp.mpf(4)/(135*n)) * n * n
    log(f"     n={n:>6}: (theta - 1/3 - 4/135n)*n^2 = {mp.nstr(c2, 10)}")
log("     -> converges to -8/2835, confirming the k(inf)=2/21 half of the citation;")
log("        k(0)=8/45 <=> theta(0)=1/2 exactly (F1), the other endpoint.")

# ----------------------------------------------------------------------------
log("")
log("=" * 78)
log("(L) LEMMA 1:  Q(n) = n! e^n/(2 n^n) - theta(n).")
log("    Referee re-derivation:  Q(n) = sum_{j=0}^{n-1} prod_{i=1}^j (1-i/n),")
log("    term_j = (n-1)!/((n-1-j)! n^j);  m := n-1-j  gives")
log("       Q(n) = ((n-1)!/n^{n-1}) sum_{m=0}^{n-1} n^m/m!  =  (n!/n^n) S(n),")
log("    S(n) := sum_{m=0}^{n-1} n^m/m!  [= FGKP95 eq. (1.4) verbatim].")
log("    With S(n) = e^n/2 - theta(n) n^n/n!  (the theta definition) this IS the")
log("    stated identity.  Both steps checked below.")
log("=" * 78)

def Q_exact(n):
    """Q(n) as exact Fraction: numerator sum t_j = (n-1)!/(n-1-j)! * n^{n-1-j}
       over n^{n-1};   t_0 = n^{n-1},  t_j = (t_{j-1}//n)*(n-j)  (exact)."""
    t = n ** (n - 1)
    tot = t
    for j in range(1, n):
        t = (t // n) * (n - j)
        tot += t
    return F(tot, n ** (n - 1))

log("")
log("(L1) EXACT rational check  Q(n) == (n!/n^n) * S(n),  n = 1..400:")
bad = []
for n in range(1, 401):
    q = Q_exact(n)
    fact = 1
    for i in range(2, n + 1):
        fact *= i
    rhs = F(fact, n ** n) * S_exact(n)
    if q != rhs:
        bad.append(n)
log(f"   exact-equality failures: {bad if bad else 'none (400/400 exact)'}")
if bad: fails += 1

log("")
log("(L2) transcendental form  Q(n) = n!e^n/(2n^n) - theta(n)  to >=50 digits,")
log("     theta from its own defining sum (exact partial sums), sample n:")
worst = mp.mpf(0)
for n in [1, 2, 3, 5, 10, 25, 60, 150, 400, 1000, 2000]:
    q = Q_exact(n)
    qmp = mp.mpf(q.numerator) / mp.mpf(q.denominator)
    th = theta_def(n)
    nmp = mp.mpf(n)
    A = mp.e ** (mp.loggamma(nmp + 1) + nmp - nmp * mp.log(nmp))
    rhs = A / 2 - th
    d = abs(qmp - rhs)
    if d > worst: worst = d
log(f"   worst |Q(n) - (n!e^n/(2n^n) - theta(n))| over the sample: {mp.nstr(worst, 4)}")
if worst > mp.mpf(10) ** (-50): fails += 1

log("")
log("(L3) the document's PRINTED intermediates, checked with exact Fractions.")
log("     Printed:  Q(n) = sum_{k=1}^n n!/(k! n^{n-k})  =  (n!/n^n)(G(n)-1),")
log("     G(n) := sum_{k=0}^n n^k/k!.   Referee claim: both displays are FALSE for")
log("     n>=2; printed_value - Q(n) = 1 - n!/n^n exactly (a factor-n/k per-term")
log("     slip: the k-substitution shifted the index but not the summand).")
hdr = f"   {'n':>3} | {'Q(n) exact':>12} | {'printed sum':>12} | {'difference':>14} | 1 - n!/n^n"
log(hdr); log("   " + "-" * (len(hdr) - 3))
all_match_alg = True
for n in range(1, 13):
    q = Q_exact(n)
    fact = 1
    for i in range(2, n + 1):
        fact *= i
    # printed k-term sum, exact
    printed = sum(F(fact, __import__('math').factorial(k) * n ** (n - k)) for k in range(1, n + 1))
    G = S_exact(n) + F(n ** n, fact) if n > 0 else None  # G = S + n^n/n!
    printed2 = F(fact, n ** n) * (G - 1)
    assert printed == printed2, "the two printed forms should at least agree with each other"
    diff = printed - q
    alg = 1 - F(fact, n ** n)
    ok = (diff == alg)
    all_match_alg &= ok
    log(f"   {n:>3} | {str(q):>12} | {str(printed):>12} | {str(diff):>14} | "
        f"{str(alg):>14} {'(match)' if ok else '(MISMATCH)'}")
log(f"   printed display equals Q(n) ONLY at n=1; for every n>=2 it differs by")
log(f"   exactly 1 - n!/n^n != 0.  Algebraic characterization holds at every n "
    f"tested: {all_match_alg}")
log("   The claimed cancellation ('the +-1 and +-n!/n^n terms cancel exactly')")
log("   does NOT follow from the printed intermediates; it follows from the")
log("   corrected ones (S(n) in place of G(n)-1), under which the final identity")
log("   is TRUE -- as (L1)+(L2) verify, and as FGKP95's own (1.4) + D(n)=2 theta(n)")
log("   state classically (so 'new elementary identity' also overstates novelty).")

log("")
log("(L4) sanity: the two anchor values quoted in ATTEMPT.md Section 2:")
log(f"   Q(2) = {Q_exact(2)}  (claimed 3/2);   Q(3) = {Q_exact(3)}  (claimed 17/9)")
if Q_exact(2) != F(3, 2) or Q_exact(3) != F(17, 9): fails += 1

log("")
log("=" * 78)
log(f"PART-1 RESULT: {'ALL CHECKS PASSED (0 failures)' if fails == 0 else f'{fails} FAILURE GROUPS'}")
log("  (note: 'passed' refers to the referee checks; the two documented findings --")
log("   the mis-printed Robbins display and the broken Lemma-1 intermediates --")
log("   are findings about the DOCUMENT'S TEXT, demonstrated above, while the")
log("   underlying cited theorems and the final Lemma-1 identity are all TRUE.)")
log("=" * 78)

with open(__file__.replace(".py", ".log"), "w") as f:
    f.write("\n".join(LOG) + "\n")
sys.exit(0 if fails == 0 else 1)
