#!/usr/bin/env python3
"""
corroborate_finite_n.py  --  wave 9, front (b), RATE-COEFFICIENT-POSITIVITY-ATTEMPT

INDEPENDENT corroboration, from the finite-`n` side, that the number this document
proves positive is really the `1/n` coefficient of `phi_n^{(K)} - phi_K`.

This is deliberately NOT part of the proof.  The identification of that coefficient
with  c_K = K[phi_K/4 + F_{K-1}(1,1) - phi_K]  is an already-PROVED, already
adversarially-refereed upstream result (THEOREM.md Stage 6 items 2-4;
adversarial/REFEREE_REPORT.md A.7).  The purpose here is only to rule out a
TRANSCRIPTION error on this session's part -- i.e. that I read the definition of
c_K wrongly -- by recomputing phi_n^{(K)} from the raw exact transition rules and
extracting its 1/n coefficient numerically.

Sources re-transcribed (already PROVED elsewhere; re-typed here from scratch, no
import from any sibling directory):

  k3_attempt_2/ATTEMPT.md  §2, 'Proposition (exact transition rules, PROVED)':
      m := n - a
      g(a,b,r) = 1/m + (r/m) h(a+1,b,r-1) + ((m-1-r-b)/m) g(a+1,b,r)
      h(a,b,r) = 1/n + (r/n) h(a,b+1,r-1) + ((n-1-a-b-r)/n) g(a,b+1,r)
      psi_n^{(K)}   = g(0,0,K)
      psi_n^{(K),R} = h(0,0,K-1)

  wave 5 ATTEMPT.md, Reduction Lemma A (PROVED, every fixed K>=1), as cited in
  k3_attempt_2/ATTEMPT.md §0:
      phi_n^{(K)} = (K/n) psi_n^{(K),R} + (1 - K/n) psi_n^{(K)}

  THEOREM.md Lemma 2:  phi_K = 4^K (K!)^2 / (2K+1)!

Method: iterative (non-recursive) exact-Fraction evaluation.  Note b <= K always
(b only increments on a source step, and there are at most K source visits), so the
state space is O(n K^2).  Iterate a downward (g at a needs level a+1), and, within
one a, b downward and r upward (h at (a,b,r) needs (a,b+1,*) only).

Richardson: phi_n^{(K)} - phi_K = c/n + d/n^2 + O(1/n^3), so
    A_n := n(phi_n^{(K)} - phi_K) = c + d/n + O(1/n^2)
    R_n := 2 A_{2n} - A_n = c + O(1/n^2)      (exact rational Richardson)
"""

from fractions import Fraction
from math import comb, factorial
import sys

FAIL = []


def check(name, cond, extra=""):
    tag = "OK  " if cond else "FAIL"
    if not cond:
        FAIL.append(name)
    print(f"  [{tag}] {name}{(' :: ' + extra) if extra else ''}")


def phi(K):
    return Fraction(4 ** K * factorial(K) ** 2, factorial(2 * K + 1))


def c_target(K):
    """c_K = (K+2)4^K/(4(2K+1)C(2K,K)) - 1/2  -- this document's closed form,
    proved equal to K[phi_K/4 + F_{K-1}(1,1) - phi_K] in verify_ck_closed_form.py."""
    return Fraction((K + 2) * 4 ** K, 4 * (2 * K + 1) * comb(2 * K, K)) - Fraction(1, 2)


def phi_n_K(n, K):
    """phi_n^{(K)} exactly, from the raw transition rules.  Returns a Fraction."""
    # g[b][r], h[b][r] at the current level a.
    # Level a = n:  m = 0, no non-source step is possible; those states are never
    # reached (the walk terminates by then).  Initialise the a = n level to 0; the
    # coefficient structure makes the values at reachable states independent of it.
    # This is validated END-TO-END in part (A) below against wave 6's already-PROVED
    # closed form for phi_n^{(3)} (n=4..30) and the exact phi_n^{(1)} - phi_1
    # = 1/(3n^2) (n=2..40), so no separate boundary convention is being assumed.
    gn = [[Fraction(0)] * (K + 1) for _ in range(K + 2)]
    hn = [[Fraction(0)] * (K + 1) for _ in range(K + 2)]
    for a in range(n - 1, -1, -1):
        m = n - a
        g = [[Fraction(0)] * (K + 1) for _ in range(K + 2)]
        h = [[Fraction(0)] * (K + 1) for _ in range(K + 2)]
        for b in range(K, -1, -1):
            for r in range(0, K + 1):
                # ---- g(a,b,r) : non-source step, pool size m
                val = Fraction(1, m)
                if r >= 1:
                    val += Fraction(r, m) * gn_h(hn, b, r - 1)
                cont = m - 1 - r - b
                if cont > 0:
                    val += Fraction(cont, m) * gn[b][r]
                g[b][r] = val
                # ---- h(a,b,r) : source step, uniform over all n
                val = Fraction(1, n)
                if r >= 1:
                    val += Fraction(r, n) * h[b + 1][r - 1]
                cont = n - 1 - a - b - r
                if cont > 0:
                    val += Fraction(cont, n) * g[b + 1][r]
                h[b][r] = val
        gn, hn = g, h
    psi = gn[0][K]                      # g(0,0,K)
    psiR = hn[0][K - 1] if K >= 1 else None
    if K == 0:
        return psi
    return Fraction(K, n) * psiR + (1 - Fraction(K, n)) * psi


def gn_h(hn, b, r):
    return hn[b][r]


# ---------------------------------------------------------------------------
# (A) sanity: reproduce the PROVED small-K closed forms of waves 5 / 6
# ---------------------------------------------------------------------------
print("=" * 78)
print("(A) reproduce already-PROVED closed forms (waves 5-6), exact rationals")
print("=" * 78)

# k3_attempt_2/ATTEMPT.md executive summary:
#   psi_n^{(3)} = 16/35 + 12/(35n) + 5/(28n^2) + 3/(70n^3)
#   phi_n^{(3)} = 16/35 + 1/(14n) + 11/(10n^2) + 23/(35n^3) + 6/(35n^4)
def phi3_closed(n):
    return (Fraction(16, 35) + Fraction(1, 14 * n) + Fraction(11, 10 * n ** 2)
            + Fraction(23, 35 * n ** 3) + Fraction(6, 35 * n ** 4))

bad = [n for n in range(4, 31) if phi_n_K(n, 3) != phi3_closed(n)]
check("phi_n^{(3)} from raw transition rules == wave-6's PROVED closed form, n=4..30",
      not bad, f"mismatches: {bad}")

# THEOREM.md / REFEREE_REPORT: phi_n^{(1)} - phi_1 = 1/(3n^2) exactly
bad = [n for n in range(2, 41)
       if phi_n_K(n, 1) - phi(1) != Fraction(1, 3 * n ** 2)]
check("phi_n^{(1)} - phi_1 == 1/(3n^2) exactly, n=2..40 (the K=1 degeneracy)", not bad,
      f"mismatches: {bad}")


# ---------------------------------------------------------------------------
# (B) EXACT extraction of the 1/n coefficient by exact polynomial-in-(1/n) fit
# ---------------------------------------------------------------------------
# Empirically (waves 5-6, PROVED for K<=5) phi_n^{(K)} is, for n large enough, an
# exact finite polynomial in 1/n:  phi_n^{(K)} = sum_{j=0}^{D} alpha_j n^{-j}.
# So: solve exactly for alpha_0..alpha_D from D+1 exact values, then VALIDATE the
# fitted polynomial against further n values it never saw.  If it validates, the
# alpha_j are exact, and alpha_1 is exactly the 1/n coefficient -- a fully exact
# finite-n confirmation, with no extrapolation error at all.

def solve_exact(A, y):
    """Gaussian elimination over Fraction.  A: list of rows, y: rhs."""
    N = len(A)
    M = [list(A[i]) + [y[i]] for i in range(N)]
    for col in range(N):
        p = next(i for i in range(col, N) if M[i][col] != 0)
        M[col], M[p] = M[p], M[col]
        piv = M[col][col]
        M[col] = [v / piv for v in M[col]]
        for i in range(N):
            if i != col and M[i][col] != 0:
                f = M[i][col]
                M[i] = [M[i][j] - f * M[col][j] for j in range(N + 1)]
    return [M[i][N] for i in range(N)]


def fit_1_over_n_polynomial(K, D, n0):
    """Fit phi_n^{(K)} = sum_{j=0}^{D} alpha_j n^{-j} on n = n0..n0+D, then check
    the fit on n = n0+D+1 .. n0+D+6.  Returns (alphas, validated?)."""
    ns = list(range(n0, n0 + D + 1))
    A = [[Fraction(1, n ** j) for j in range(D + 1)] for n in ns]
    y = [phi_n_K(n, K) for n in ns]
    al = solve_exact(A, y)
    ok = all(sum(al[j] / n ** j for j in range(D + 1)) == phi_n_K(n, K)
             for n in range(n0 + D + 1, n0 + D + 7))
    return al, ok


print()
print("=" * 78)
print("(B) EXACT 1/n coefficient of phi_n^{(K)} - phi_K, by exact rational fit")
print("    (fit on D+1 values, then validated on 6 values the fit never saw)")
print("=" * 78)
print(f"  {'K':>3} {'deg D':>6} {'alpha_0':>16} {'= phi_K?':>9} {'alpha_1 (exact)':>20} "
      f"{'= c_K?':>7}")

for K in range(1, 10):
    got = None
    for D in range(2, 3 * K + 6):
        al, ok = fit_1_over_n_polynomial(K, D, max(K + 2, 8))
        if ok and (D == 2 or al[D] != 0):
            got = (D, al)
            break
    if got is None:
        check(f"exact 1/n-polynomial fit found for K={K}", False)
        continue
    D, al = got
    a0_ok = (al[0] == phi(K))
    a1_ok = (al[1] == c_target(K))
    print(f"  {K:>3} {D:>6} {str(al[0]):>16} {'yes' if a0_ok else 'NO':>9} "
          f"{str(al[1]):>20} {'yes' if a1_ok else 'NO':>7}")
    if not (a0_ok and a1_ok):
        FAIL.append(f"exact fit K={K}")

check("for K=1..9: exact fit validates, alpha_0 == phi_K and alpha_1 == c_K, "
      "as EXACT rationals", not any(f.startswith('exact fit') for f in FAIL))

print()
if FAIL:
    print("RESULT:  ***FAILURES***:", FAIL)
    sys.exit(1)
print("RESULT:  the coefficient this document proves positive is confirmed, from")
print("         the raw finite-n transition rules, to be the 1/n coefficient of")
print("         phi_n^{(K)} - phi_K.  No transcription error.")
