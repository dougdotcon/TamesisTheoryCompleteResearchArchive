"""chain.py -- from-scratch exact engines for phi(n,c) and phi_n^{(K)}.

Wave 11 front (a), UNIFORM-IN-C-TEOREMA-3-ATTEMPT (DISC-DEC-047).

Nothing here imports any file from the rest of the archive: the two Markov
chains below were derived independently in this document's SS2 from
Definition 1 of THEOREM.md, and are cross-checked against archive-published
exact values in the self-test at the bottom.

Two engines:

  phi_mixed(n, c)      -- phi(n,c) = P(1 is cyclic for f) under Definition 1,
                          exact if c is a Fraction, float/mpmath otherwise.
  phi_condK(n, K)      -- phi_n^{(K)} of Definition 4 (exactly K reroutes).

Both are backward recursions over the "orbit exploration" state (j, R):
  j = number of steps already taken from x_0 = 1 (so x_0..x_j visited),
  R = how many of those j completed steps were reroute steps.

Derivation (see ATTEMPT.md SS2): standing at x_j, having visited j+1 distinct
points and revealed pi at exactly the j-R permutation-steps (whose images are
{x_{i+1}} subset {x_1..x_j}), the *available* pi-targets are [n] minus those
j-R revealed images, i.e. n-(j-R) points, of which exactly one is x_0 and
exactly R are the visited points reached by a reroute (the x_i, i>=1, whose
predecessor step was a reroute).  Hence, conditionally on the whole history:

  reroute branch (U ~ Unif[n]):   hit x_0 w.p. 1/n            -> cyclic
                                  hit x_1..x_j w.p. j/n       -> never cyclic
                                  fresh w.p. (n-j-1)/n        -> (j+1, R+1)
  permutation branch:             hit x_0 w.p. 1/(n-j+R)      -> cyclic
                                  hit an R-point w.p. R/(n-j+R)-> never cyclic
                                  fresh w.p. (n-j-1)/(n-j+R)  -> (j+1, R)

The branch weight is q=c/n (mixed model) or (K-R)/(n-j) (model conditioned on
exactly K reroute indices in [n], sampling without replacement).
"""

from fractions import Fraction
import numpy as np


# ---------------------------------------------------------------- exact ----

def phi_mixed_exact(n, c):
    """phi(n,c), exact.  c a Fraction/int with 0 <= c <= n."""
    q = Fraction(c, n)
    assert 0 <= q <= 1
    one = Fraction(1)
    # P[R] at level j
    j = n - 1
    P = [q * Fraction(1, n) + (1 - q) * Fraction(1, R + 1) for R in range(j + 1)]
    for j in range(n - 2, -1, -1):
        avail = n - j          # n-j+R for R
        newP = []
        for R in range(j + 1):
            a = n - j + R
            rer = q * (Fraction(1, n) + Fraction(n - j - 1, n) * P[R + 1])
            per = (1 - q) * (Fraction(1, a) + Fraction(n - j - 1, a) * P[R])
            newP.append(rer + per)
        P = newP
    return P[0]


def phi_condK_exact(n, K):
    """phi_n^{(K)}, exact (Definition 4 of THEOREM.md SS7.2)."""
    assert 0 <= K <= n
    j = n - 1
    P = []
    for R in range(j + 1):
        rem = n - j                      # = 1 unexamined index left
        nr = K - R                       # reroute indices left among them
        if nr < 0 or nr > rem:
            P.append(Fraction(0))        # unreachable state
            continue
        pr = Fraction(nr, rem)
        P.append(pr * Fraction(1, n) + (1 - pr) * Fraction(1, R + 1))
    for j in range(n - 2, -1, -1):
        newP = []
        for R in range(j + 1):
            rem = n - j
            nr = K - R
            if nr < 0 or nr > rem:
                newP.append(Fraction(0))
                continue
            pr = Fraction(nr, rem)
            a = n - j + R
            rer = pr * (Fraction(1, n) + Fraction(n - j - 1, n) * P[R + 1])
            per = (1 - pr) * (Fraction(1, a) + Fraction(n - j - 1, a) * P[R])
            newP.append(rer + per)
        P = newP
    return P[0]


# ------------------------------------------------------------ float/fast ----

def phi_mixed_fast(n, c, rmax=None, dtype=np.float64):
    """phi(n,c) in floating point, O(n*rmax).

    rmax truncates the R-index (R ~ Binomial(j, c/n), so R <= rmax holds with
    overwhelming probability when rmax >> c).  rmax=None means exact (no
    truncation): O(n^2).
    """
    q = dtype(c) / dtype(n)
    assert 0.0 <= q <= 1.0
    if rmax is None:
        rmax = n
    rmax = int(min(rmax, n))
    nn = dtype(n)
    j = n - 1
    R = np.arange(0, min(j, rmax) + 1, dtype=dtype)
    P = q / nn + (1 - q) / (R + 1)
    for j in range(n - 2, -1, -1):
        top = min(j, rmax)
        R = np.arange(0, top + 1, dtype=dtype)
        a = nn - j + R
        # P currently indexed by R at level j+1, length min(j+1,rmax)+1
        Pnext_same = P[: top + 1]
        if top + 1 < len(P):
            Pnext_up = P[1: top + 2]
        else:                                   # truncated: reuse last entry
            Pnext_up = np.concatenate([P[1: top + 1], P[top: top + 1]])
        rer = q * (1.0 / nn + (nn - j - 1) / nn * Pnext_up)
        per = (1 - q) * (1.0 / a + (nn - j - 1) / a * Pnext_same)
        P = rer + per
    return float(P[0])


def phi_condK_fast(n, K, dtype=np.float64):
    """phi_n^{(K)} in floating point, O(n*min(K,n))."""
    nn = dtype(n)
    rmax = min(K, n)
    j = n - 1
    top = min(j, rmax)
    R = np.arange(0, top + 1, dtype=dtype)
    rem = dtype(n - j)
    nr = K - R
    pr = np.clip(nr / rem, 0.0, 1.0)
    P = pr / nn + (1 - pr) / (R + 1)
    for j in range(n - 2, -1, -1):
        top = min(j, rmax)
        R = np.arange(0, top + 1, dtype=dtype)
        rem = dtype(n - j)
        pr = np.clip((K - R) / rem, 0.0, 1.0)
        a = nn - j + R
        Pnext_same = P[: top + 1]
        if top + 1 < len(P):
            Pnext_up = P[1: top + 2]
        else:
            Pnext_up = np.concatenate([P[1: top + 1], P[top: top + 1]])
        rer = pr * (1.0 / nn + (nn - j - 1) / nn * Pnext_up)
        per = (1 - pr) * (1.0 / a + (nn - j - 1) / a * Pnext_same)
        P = rer + per
    return float(P[0])


# ------------------------------------------------------------- limit law ----

def phi_inf(c):
    """phi_infty(c) = int_0^1 exp(-c t^2) dt, high precision via mpmath."""
    import mpmath as mp
    c = mp.mpf(c)
    if c == 0:
        return mp.mpf(1)
    return mp.sqrt(mp.pi) / 2 / mp.sqrt(c) * mp.erf(mp.sqrt(c))


def phi_K(K):
    """phi_K = 4^K (K!)^2 / (2K+1)!  (Wallis), exact Fraction."""
    from math import comb
    num = Fraction(4) ** K
    from math import factorial
    return num * Fraction(factorial(K) ** 2, factorial(2 * K + 1))


# ------------------------------------------------------------- self-test ----

if __name__ == "__main__":
    print("=== self-test: chain.py ===")
    ok = True

    # (1) phi_n^{(0)} = 1, phi_n^{(1)} = 2/3 + 1/(3n^2)  (THEOREM.md Prop 4)
    for n in range(1, 13):
        v0 = phi_condK_exact(n, 0)
        v1 = phi_condK_exact(n, 1)
        e1 = Fraction(2, 3) + Fraction(1, 3 * n * n)
        ok &= (v0 == 1) and (v1 == e1)
        if v0 != 1 or v1 != e1:
            print("  MISMATCH K=0/1 at n=%d: %s %s (want 1, %s)" % (n, v0, v1, e1))
    print("  K=0,1 closed forms, n=1..12 :", "OK" if ok else "FAIL")

    # (2) phi_n^{(2)} against THEOREM.md SS7.4's exact enumeration table
    tab2 = {2: Fraction(3, 4), 3: Fraction(17, 27), 4: Fraction(113, 192),
            5: Fraction(356, 625), 6: Fraction(151, 270), 7: Fraction(569, 1029),
            8: Fraction(281, 512)}
    ok2 = all(phi_condK_exact(n, 2) == v for n, v in tab2.items())
    print("  K=2 table n=2..8 (THEOREM.md SS7.4)      :", "OK" if ok2 else "FAIL")
    for n, v in sorted(tab2.items()):
        g = phi_condK_exact(n, 2)
        if g != v:
            print("    n=%d got %s want %s" % (n, g, v))

    # (3) phi_n^{(6)} closed form from k6_attempt/ATTEMPT.md SS1.2
    def phi6(n):
        num = (4096 * n**7 + 2186 * n**6 + 29676 * n**5 + 47655 * n**4
               + 56117 * n**3 + 45424 * n**2 + 22428 * n + 5040)
        return Fraction(num, 12012 * n**7)
    ok3 = all(phi_condK_exact(n, 6) == phi6(n) for n in range(7, 12))
    print("  K=6 closed form n=7..11 (k6_attempt SS1.2):", "OK" if ok3 else "FAIL")
    print("    phi_7^{(6)} =", phi_condK_exact(7, 6), " (archive: 355081/823543)")

    # (4) mixture identity: phi(n,c) = sum_K C(n,K) q^K (1-q)^{n-K} phi_n^{(K)}
    from math import comb
    ok4 = True
    for n in (2, 3, 4, 5, 6, 7):
        for c in (Fraction(1, 2), Fraction(1), min(Fraction(7, 3), Fraction(n)),
                  Fraction(n)):
            q = Fraction(c, n)
            mix = sum(comb(n, K) * q**K * (1 - q)**(n - K) * phi_condK_exact(n, K)
                      for K in range(n + 1))
            direct = phi_mixed_exact(n, c)
            if mix != direct:
                ok4 = False
                print("    MISMATCH n=%d c=%s: %s vs %s" % (n, c, mix, direct))
    print("  mixture identity (7.1) n=2..7            :", "OK" if ok4 else "FAIL")

    # (5) phi(n,0) = 1 exactly; phi(n,n) = Q(n)/n (Ramanujan Q) for random maps
    ok5 = all(phi_mixed_exact(n, 0) == 1 for n in range(1, 10))
    def Qn(n):
        s, term = Fraction(0), Fraction(1)
        for j in range(0, n):
            s += term
            term *= Fraction(n - 1 - j, n)
        return s
    ok5b = all(phi_mixed_exact(n, n) == Qn(n) / n for n in range(1, 12))
    print("  phi(n,0)=1 ; phi(n,n)=Q(n)/n (random map):",
          "OK" if (ok5 and ok5b) else "FAIL")

    # (6) fast engines agree with exact
    ok6 = True
    for n in (5, 20, 60):
        for c in (0.5, 2.0, 5.0):
            a = float(phi_mixed_exact(n, Fraction(c).limit_denominator(1000)))
            b = phi_mixed_fast(n, float(Fraction(c).limit_denominator(1000)))
            if abs(a - b) > 1e-12:
                ok6 = False
                print("    fast mixed mismatch n=%d c=%s: %.15g %.15g" % (n, c, a, b))
        for K in (0, 1, 3, min(n, 8)):
            a = float(phi_condK_exact(n, K))
            b = phi_condK_fast(n, K)
            if abs(a - b) > 1e-12:
                ok6 = False
                print("    fast condK mismatch n=%d K=%d: %.15g %.15g" % (n, K, a, b))
    print("  float engines vs exact                   :", "OK" if ok6 else "FAIL")

    # (7) phi_K Wallis vs limits already known
    print("  phi_K, K=0..6:", [str(phi_K(K)) for K in range(7)])
