# engine.py -- fresh exact/certified toolkit for the sharp-rate reassembly
# (wave 17 front (b), DISC-DEC-072).
#
# EVERYTHING here is re-derived from the PROSE of the cited attempt documents
# (Corolario A1 / Teorema B of Estagio 9 as quoted in
# u_prime_hypothesis_attempt/ATTEMPT.md SS2; Lema A reduction; Fact 4.1 mixture;
# phi_K Wallis form; Q(n) definition; Corolario 4.2 tail bracket). No prior
# front's .py script was opened or imported. All certified quantities are
# fractions.Fraction; no floating point enters any certified path.
#
# No randomness anywhere (seed 20260862000+ reserved per DISC-DEC-072, unused).

from fractions import Fraction
from math import isqrt, comb, factorial

# ---------------------------------------------------------------------------
# Certified constant brackets
# ---------------------------------------------------------------------------
# pi in (3.14159265358979, 3.14159265358980)  -- classical, CITED
PI_LO = Fraction(314159265358979, 10**14)
PI_HI = Fraction(314159265358980, 10**14)
# e > 2.718281  -- classical, CITED (used only for exp(-c) upper bounds)
E_LO = Fraction(2718281, 10**6)


def sqrt_lo(x: Fraction, d: int = 12) -> Fraction:
    """Certified rational lower bound on sqrt(x): sqrt(p/q)=sqrt(p*q)/q."""
    if x < 0:
        raise ValueError("negative")
    num, den = x.numerator, x.denominator
    s = isqrt(num * den * 10 ** (2 * d))
    return Fraction(s, den * 10**d)


def sqrt_hi(x: Fraction, d: int = 12) -> Fraction:
    if x < 0:
        raise ValueError("negative")
    num, den = x.numerator, x.denominator
    M = num * den * 10 ** (2 * d)
    s = isqrt(M)
    if s * s < M:
        s += 1
    return Fraction(s, den * 10**d)


# a* = sqrt(pi/2) - sqrt(pi)/2   (sharp constant, Estagio 13/19)
ASTAR_LO = sqrt_lo(PI_LO / 2) - sqrt_hi(PI_HI) / 2
ASTAR_HI = sqrt_hi(PI_HI / 2) - sqrt_lo(PI_LO) / 2
# old (Estagio 12) constant a = 1 + sqrt(pi/2)
AOLD_LO = 1 + sqrt_lo(PI_LO / 2)
AOLD_HI = 1 + sqrt_hi(PI_HI / 2)
# certified lower bound on kappa_B = sup_c c^2 I2(c)  (established in T3,
# verify_kappa_star.py; used by the final-rate check as the conservative RHS)
KAPPA_LO = Fraction(28048, 100000)
KAPPA_HI_DEC = Fraction(2805, 10000)  # the decimal 0.2805 used in the theorem


# ---------------------------------------------------------------------------
# Exact combinatorial objects
# ---------------------------------------------------------------------------
def phi_K(K: int) -> Fraction:
    """Wallis mean phi_K = 4^K (K!)^2/(2K+1)!  (THEOREM.md Lemma 2)."""
    return Fraction(4**K * factorial(K) ** 2, factorial(2 * K + 1))


def Q_exact(n: int) -> Fraction:
    """Ramanujan Q(n) = sum_{j=0}^{n-1} prod_{i=1}^{j}(1-i/n), exact.

    Integer form: Q(n) = ( sum_{j=0}^{n-1} [prod_{i=1}^{j}(n-i)] * n^{n-1-j} ) / n^{n-1}.
    """
    S = 0
    P = 1                      # prod_{i=1}^{j}(n-i), starts at j=0 -> 1
    pw = n ** (n - 1)          # n^{n-1-j}, starts at j=0
    for j in range(n):
        S += P * pw
        P *= (n - 1 - j)       # extend product to i=j+1: factor n-(j+1)
        pw //= n
    return Fraction(S, n ** (n - 1))


def Q_bracket_truncated(n: int) -> tuple:
    """Certified bracket for Q(n) at large n: exact partial sum + tail bound.

    P_j <= e^{-j(j+1)/(2n)} <= e^{-j^2/(2n)} (1-x <= e^{-x}).
    For j >= J: j^2 >= J^2 + 2J(j-J), so
      sum_{j>=J} P_j <= e^{-J^2/(2n)} / (1-e^{-J/n}) <= e^{-8} * (1 + n/J)
    when J >= 4 sqrt(n) (then J^2/(2n) >= 8), using 1/(1-e^{-x}) <= 1 + 1/x.
    e^{-8} < 1/2980 since e > 2.718281 and 2718281^8 > 2980*10^48 (checked).
    """
    assert E_LO**8 > 2980, "e^8 > 2980 certification failed"
    J = isqrt(16 * n) + 1      # J >= 4 sqrt(n)
    S = Fraction(0)
    P = Fraction(1)
    for j in range(J):
        S += P
        P *= Fraction(n - 1 - j, n)
        if P == 0:
            return (S, S)      # n <= J: sum was complete and exact
    tail = Fraction(1, 2980) * (1 + Fraction(n, J))
    return (S, S + tail)


# ---------------------------------------------------------------------------
# phi_n^{(K)} closed form (re-derived from prose: Estagio 9 Corolario A1 +
# Proposicao 2.1 of u_prime_hypothesis_attempt + Lema A reduction)
# ---------------------------------------------------------------------------
def psi(n: int, K: int) -> Fraction:
    """psi_n^{(K)} = (K!)^2/(2K+1)! * sum_{j=0}^{K} C(2K+1,K-j) (n+j)!/(n! n^j)."""
    pref = Fraction(factorial(K) ** 2, factorial(2 * K + 1))
    tot = Fraction(0)
    g = Fraction(1)            # (n+j)!/(n! n^j) at j=0
    for j in range(K + 1):
        tot += comb(2 * K + 1, K - j) * g
        g *= Fraction(n + j + 1, n)
    return pref * tot


def psiR(n: int, K: int) -> Fraction:
    """psi_n^{(K),R} = (K-1)!K!/(2K)! * sum_{i=1}^{K} C(2K,K-i) (n+i)!/(n! n^i)."""
    assert K >= 1
    pref = Fraction(factorial(K - 1) * factorial(K), factorial(2 * K))
    tot = Fraction(0)
    g = Fraction(1)
    for i in range(1, K + 1):
        g *= Fraction(n + i, n)
        tot += comb(2 * K, K - i) * g
    return pref * tot


def phi_nK(n: int, K: int) -> Fraction:
    """phi_n^{(K)}, exact. Lema A for K<n; Proposicao 7.1 (phi_n^{(n)}=Q(n)/n) at K=n."""
    if K == 0:
        return Fraction(1)
    if K == n:
        return Q_exact(n) / n
    return Fraction(K, n) * psiR(n, K) + Fraction(n - K, n) * psi(n, K)


def phi_nK_table(n: int) -> list:
    return [phi_nK(n, K) for K in range(n + 1)]


def phi_finite(n: int, c: Fraction, table=None) -> Fraction:
    """phi(n,c) via the exact mixture identity (7.1), c rational in [0,n]."""
    if table is None:
        table = phi_nK_table(n)
    p = Fraction(c, n)
    q = 1 - p
    tot = Fraction(0)
    for K in range(n + 1):
        w = comb(n, K) * p**K * q ** (n - K)
        if w:
            tot += w * table[K]
    return tot


# ---------------------------------------------------------------------------
# Certified brackets of phi_inf(c) = int_0^1 e^{-c t^2} dt and
# I2(c) = int_0^1 t^4 e^{-c t^2} dt
# ---------------------------------------------------------------------------
def _alt_series_bracket(c: Fraction, denom_off: int, eps=Fraction(1, 10**30)):
    """Bracket sum_{k>=0} (-c)^k / (k! (2k+1+denom_off)).

    Terms t_k = c^k/(k!(2k+1+denom_off)). Once k+1 > c the terms are strictly
    decreasing (ratio < c/(k+1) < 1), so after truncating at index m with
    m+1 > c the remainder is bounded in absolute value by t_{m+1}.
    """
    assert c >= 0
    S = Fraction(0)
    t = Fraction(1, 1 + denom_off)   # k = 0 term
    k = 0
    sign = 1
    while True:
        S += sign * t
        # next term
        tn = t * c / (k + 1) * Fraction(2 * k + 1 + denom_off,
                                        2 * k + 3 + denom_off)
        if k + 1 > c and tn < eps:
            return (S - tn, S + tn)
        t = tn
        sign = -sign
        k += 1


def phi_inf_bracket(c: Fraction):
    """Certified rational bracket for phi_inf(c)=int_0^1 e^{-ct^2}dt.

    c <= 40: alternating series (Corolario 4.1).
    c > 40 : phi_inf(c) = sqrt(pi)/(2 sqrt(c)) - R(c), 0 < R(c) < e^{-c}/(2c)
             (Corolario 4.2, PROVED), with e^{-c} <= E_LO^{-floor(c)}.
    """
    if c == 0:
        return (Fraction(1), Fraction(1))
    if c <= 40:
        return _alt_series_bracket(c, 0)
    lead_lo = sqrt_lo(PI_LO) / (2 * sqrt_hi(c))
    lead_hi = sqrt_hi(PI_HI) / (2 * sqrt_lo(c))
    R_hi = Fraction(1) / (E_LO ** int(c)) / (2 * c)
    return (lead_lo - R_hi, lead_hi)


def I2_bracket(c: Fraction):
    """Certified bracket for I2(c)=int_0^1 t^4 e^{-ct^2}dt = sum (-c)^k/(k!(2k+5))."""
    if c == 0:
        return (Fraction(1, 5), Fraction(1, 5))
    if c <= 200:
        # exact alternating series works fine here with Fraction arithmetic
        return _alt_series_bracket(c, 4)
    # c > 200 (used only for coarse upper bounds):
    # c^2 I2(c) <= (3/8) sqrt(pi/c)  =>  I2(c) <= (3/8) sqrt(pi) c^{-5/2}; lo trivial
    hi = Fraction(3, 8) * sqrt_hi(PI_HI) / (c * c * sqrt_lo(c))
    return (Fraction(0), hi)


# ---------------------------------------------------------------------------
# Brute-force ground truth (independent of every closed form above)
# ---------------------------------------------------------------------------
def _cyclic_count(f):
    """Number of cyclic points of the mapping f: [n]->[n] (0-indexed list)."""
    n = len(f)
    cnt = 0
    for i in range(n):
        x = i
        for _ in range(n):
            x = f[x]
            if x == i:
                cnt += 1
                break
    return cnt


def phi_nK_bruteforce(n: int, K: int) -> Fraction:
    """Exact enumeration: rerouted set {0..K-1} (WLOG by exchangeability),
    pi uniform in S_n, destinations u in [n]^K uniform. From Definition 4."""
    from itertools import permutations, product
    total = 0
    count = 0
    rng = list(range(n))
    for pi in permutations(rng):
        base = list(pi)
        for u in product(rng, repeat=K):
            f = list(u) + base[K:]
            total += _cyclic_count(f)
            count += 1
    return Fraction(total, count * n)
