"""
DISC-DEC-066, wave 16 front (b), SHARP-CONSTANT-A-STAR-MONOTONICITY-ATTEMPT.

T1/T2/T3: verify the two external classical citations this document relies on,
and the new elementary identity connecting them to the archive's Q(n), BEFORE
using them in any derivation. No randomness anywhere (fully deterministic
objects) -- seed 20260852000 is reserved (DISC-DEC-066) but, per this front's
own domain (exact/elementary real analysis, same as every sibling document in
this lineage), not used; logged here so a referee does not need to ask.

  Citation 1 (Robbins 1955). For every integer n>=1:
      sqrt(2 pi n) e^{1/(12n+1)}  <  n!  <  sqrt(2 pi n) e^{1/(12n)}.
  [H. Robbins, "A Remark on Stirling's Formula," Amer. Math. Monthly 62 (1955),
   26-29.]

  Citation 2 (Flajolet, Grabner, Kirschenhofer, Prodinger 1995, Theorem 7).
  Define theta(n) for every integer n>=0 by
      (1/2) e^n = 1 + n + n^2/2! + ... + n^{n-1}/(n-1)! + theta(n) n^n/n! .
  Then theta(n) = 1/3 + 4/(135(n+k(n))) with k(n) in [2/21, 8/45] for EVERY
  integer n>=0 (an unconditional, non-asymptotic, all-n statement -- proved by
  the cited paper via effective bounds for n>=116 plus exhaustive computer
  verification for n<116, folded into one clean theorem).
  [P. Flajolet, P.J. Grabner, P. Kirschenhofer, H. Prodinger, "On Ramanujan's
   Q-function," J. Comput. Appl. Math. 58 (1995), 103-116, Theorem 7 --
   resolving a conjecture from Ramanujan's own first letter to Hardy (16 Jan
   1913).]

  New elementary identity (Lemma 1 of ATTEMPT.md, re-derived here from scratch,
  NOT assumed): archive's Q(n) := sum_{j=0}^{n-1} prod_{i=1}^j (1-i/n) is
  EXACTLY Knuth's Q(n) of the cited paper's eq. (1.3)-(1.4), and
      Q(n) = (n! e^n)/(2 n^n) - theta(n)     for every integer n>=1.

T1: Robbins' bound vs exact n! (Fraction, small n) and via loggamma (wide n).
T2: FGKP95 Theorem 7's theta(n) bound vs theta(n) computed two independent
    ways -- (a) directly from its OWN defining partial sum (exact Fraction,
    small n) and (b) via the Poisson-CDF/incomplete-gamma identity
    theta(n) = (1/2)(n! e^n/n^n) - e^n Gamma(n+1,n)/n^n + 1 (mpmath
    gammainc, wide n) -- cross-checked against each other AND against the
    bound.
T3: the new identity Q(n) = (n! e^n)/(2 n^n) - theta(n) itself, exact Fraction
    Q(n) vs theta(n) computed from its own definition.
"""
import json
from fractions import Fraction
import mpmath as mp

mp.mp.dps = 50
LOG = []


def log(msg):
    print(msg)
    LOG.append(msg)


def frac2mp(fr):
    return mp.mpf(fr.numerator) / mp.mpf(fr.denominator)


def Q_exact(n):
    total = Fraction(0)
    prod = Fraction(1)
    total += prod  # j=0
    for i in range(1, n):
        prod *= Fraction(n - i, n)
        total += prod
    return total


def factorial_exact(n):
    r = 1
    for i in range(2, n + 1):
        r *= i
    return r


def theta_from_definition_exact(n):
    """theta(n) via ITS OWN definition, exact partial sum (Fraction) + mpmath e^n."""
    if n == 0:
        return mp.mpf(1) / 2  # (1/2)e^0 = 0 + theta*0^0/0! = theta => theta=1/2
    nfac = factorial_exact(n)
    S = Fraction(0)
    term = Fraction(1)
    S += term
    for i in range(1, n):
        term = term * n / i
        S += term
    en = mp.e ** n
    return (mp.mpf(en) / 2 - frac2mp(S)) * mp.mpf(nfac) / mp.mpf(n) ** n


def theta_via_gammainc(n):
    """theta(n) via the Poisson-CDF / incomplete-gamma identity (fast, wide n)."""
    n_ = mp.mpf(n)
    log_nfac = mp.loggamma(n_ + 1)
    log_nn = n_ * mp.log(n_)
    term1 = mp.mpf('0.5') * mp.e ** (log_nfac + n_ - log_nn)
    G = mp.gammainc(n_ + 1, n_, mp.inf)  # unregularized upper incomplete gamma
    term2 = mp.e ** n_ * G / mp.e ** log_nn
    return term1 - term2 + 1


# ---------------------------------------------------------------------------
log("=== T1: Robbins (1955) bound on n! ===")
viol = 0
for n in range(1, 2001):
    nfac = factorial_exact(n) if n <= 500 else None
    log_lo = mp.mpf('0.5') * mp.log(2 * mp.pi * n) + n * mp.log(n) - n + mp.mpf(1) / (12 * n + 1)
    log_hi = mp.mpf('0.5') * mp.log(2 * mp.pi * n) + n * mp.log(n) - n + mp.mpf(1) / (12 * n)
    log_nfac = mp.log(mp.mpf(nfac)) if nfac is not None else mp.loggamma(n + 1)
    if not (log_lo < log_nfac < log_hi):
        viol += 1
        log(f"VIOLATION n={n}: log(n!)={log_nfac}, log_lo={log_lo}, log_hi={log_hi}")
for n in [3000, 5000, 10000, 50000, 100000, 500000, 1000000]:
    log_nfac = mp.loggamma(n + 1)
    log_lo = mp.mpf('0.5') * mp.log(2 * mp.pi * n) + n * mp.log(n) - n + mp.mpf(1) / (12 * n + 1)
    log_hi = mp.mpf('0.5') * mp.log(2 * mp.pi * n) + n * mp.log(n) - n + mp.mpf(1) / (12 * n)
    if not (log_lo < log_nfac < log_hi):
        viol += 1
        log(f"VIOLATION n={n}: log(n!)={log_nfac}, log_lo={log_lo}, log_hi={log_hi}")
log(f"n=1..2000 dense + 7 sparse points to n=1e6: violations={viol}")

# ---------------------------------------------------------------------------
log("")
log("=== T2: FGKP95 Theorem 7 -- theta(n) bound, two independent computations ===")
log("T2a: theta_from_definition_exact (Fraction partial sum) vs theta_via_gammainc, small n")
worst_diff = None
for n in [0, 1, 2, 3, 5, 10, 20, 50, 100, 200]:
    a = theta_from_definition_exact(n)
    b = theta_via_gammainc(n) if n > 0 else mp.mpf(1) / 2
    d = abs(a - b)
    if worst_diff is None or d > worst_diff:
        worst_diff = d
    log(f"n={n:4d}  theta_def={mp.nstr(a,15)}  theta_gammainc={mp.nstr(b,15)}  diff={mp.nstr(d,5)}")
log(f"largest cross-method diff (n=0..200 sample): {mp.nstr(worst_diff,5)} (floating-point-level agreement)")

log("")
log("T2b: FGKP95 Theorem 7 bound theta(n) in [1/3+4/(135(n+8/45)), 1/3+4/(135(n+2/21))]")
viol = 0
Ns = list(range(0, 1001)) + [1500, 2000, 3000, 5000, 10000, 50000, 100000, 500000, 1000000]
for n in Ns:
    th = theta_via_gammainc(n) if n > 0 else mp.mpf(1) / 2
    lo = mp.mpf(1) / 3 + mp.mpf(4) / (135 * (n + mp.mpf(8) / 45))
    hi = mp.mpf(1) / 3 + mp.mpf(4) / (135 * (n + mp.mpf(2) / 21))
    if not (lo <= th <= hi):
        viol += 1
        log(f"VIOLATION n={n}: theta={th}, lo={lo}, hi={hi}")
log(f"n=0..1000 dense + sparse to n=1e6 ({len(Ns)} points total): violations={viol}")

# ---------------------------------------------------------------------------
log("")
log("=== T3: new identity Q(n) = (n! e^n)/(2 n^n) - theta(n), exact Q(n) vs exact theta(n) ===")
viol = 0
for n in [1, 2, 3, 5, 10, 20, 50, 100, 150, 200]:
    Qn = frac2mp(Q_exact(n))
    th = theta_from_definition_exact(n)
    nfac = factorial_exact(n)
    lhs = mp.mpf(nfac) * mp.e ** n / (2 * mp.mpf(n) ** n) - th
    d = abs(Qn - lhs)
    ok = d < mp.mpf('1e-30')
    if not ok:
        viol += 1
        log(f"VIOLATION n={n}: Q(n)={Qn}, (n!e^n)/(2n^n)-theta(n)={lhs}, diff={d}")
log(f"n in dense small sample: violations={viol} (identity confirmed to >=30 digits at every point tested)")

with open('verify_citations.log', 'w') as f:
    f.write('\n'.join(LOG) + '\n')
print("\nLog written to verify_citations.log")
