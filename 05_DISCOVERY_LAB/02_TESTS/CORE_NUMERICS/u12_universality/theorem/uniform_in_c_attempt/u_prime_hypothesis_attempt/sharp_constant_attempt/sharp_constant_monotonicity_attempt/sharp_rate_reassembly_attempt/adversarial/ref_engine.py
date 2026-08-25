# ref_engine.py -- HOSTILE REFEREE's independent engine, wave 17 front (b)
# (DISC-DEC-072, SHARP-RATE-REASSEMBLY-ATTEMPT).
#
# INDEPENDENCE: written ONLY from the prose of:
#   THEOREM.md (Definition 1/4, Fact 4.1, Lemma 2, Corolario 4.1/4.2,
#     Estagio 9 Corolario A1),
#   u_prime_hypothesis_attempt/ATTEMPT.md (Lemma A (2.1), Proposicao 2.1,
#     Theorems 1-4, Lemma 4.1/4.2),
#   uniform_in_c_attempt/ATTEMPT.md (Lema 5.1/6.1, Cor. 6.2, Teorema B,
#     Prop. 7.1),
#   sharp_constant_attempt/ATTEMPT.md (Theorem 5/6),
#   sharp_constant_monotonicity_attempt/ATTEMPT.md (Theorem 1/2) and its
#     adversarial/REFEREE_REPORT.md par.8.
# NO .py file of the target front or any prior front was opened.
#
# All load-bearing arithmetic: fractions.Fraction / int. No float trust.

from fractions import Fraction as F
from math import isqrt, comb, factorial

# ---------------------------------------------------------------- constants
# classical rational brackets (CITED, as in the archive's own discipline):
PI_LO = F(314159265358979, 10**14)
PI_HI = F(314159265358980, 10**14)

def sqrt_bracket(x, digits=30):
    """certified rational bracket [lo,hi] with lo <= sqrt(x) <= hi, x=Fraction>=0."""
    x = F(x)
    if x < 0:
        raise ValueError
    p, q = x.numerator, x.denominator
    S = 10**digits
    s = isqrt(p * q * S * S)
    lo = F(s, q * S)
    hi = F(s + 1, q * S)
    assert lo * lo <= x <= hi * hi
    return lo, hi

SQRT_PI_LO = sqrt_bracket(PI_LO)[0]
SQRT_PI_HI = sqrt_bracket(PI_HI)[1]
SQRT2_LO, SQRT2_HI = sqrt_bracket(2)

# a* = sqrt(pi) * (1/sqrt2 - 1/2);  1/sqrt2 in [1/SQRT2_HI, 1/SQRT2_LO]
ASTAR_LO = SQRT_PI_LO * (1 / SQRT2_HI - F(1, 2))
ASTAR_HI = SQRT_PI_HI * (1 / SQRT2_LO - F(1, 2))

# old constant a = 1 + sqrt(pi/2)
A_OLD_LO = 1 + sqrt_bracket(PI_LO / 2)[0]
A_OLD_HI = 1 + sqrt_bracket(PI_HI / 2)[1]

# ---------------------------------------------------------------- phi_K, Q
def phi_K(K):
    """Wallis mean phi_K = 4^K (K!)^2 / (2K+1)!  (THEOREM.md Lemma 2)."""
    return F(4**K * factorial(K)**2, factorial(2 * K + 1))

def Q_exact(n):
    """Ramanujan Q(n) = sum_{j=0}^{n-1} prod_{i=1}^{j} (1 - i/n), exact."""
    tot = F(0)
    term = F(1)
    for j in range(n):
        if j > 0:
            term *= F(n - j, n)
        tot += term
    return tot

def Q_bracket_truncated(n, J=None):
    """certified [lo,hi] for Q(n) summing the first J+1 terms exactly and
    bounding the tail by a geometric series:
      term_{j+1} = term_j * (1-(j+1)/n)  =>  for j>J, term_j <= term_J r^{j-J},
      r = 1-(J+1)/n, tail <= term_J * r/(1-r) = term_J*(n-J-1)/(J+1)."""
    if J is None:
        # aim term_J ~ e^{-J^2/(2n)} ~ 1e-30  =>  J ~ sqrt(138 n)
        J = isqrt(140 * n) + 10
    J = min(J, n - 1)
    # integer arithmetic: S*n^J = sum_j P_j * n^(J-j), P_j = prod_{i<=j}(n-i)
    npow = [1] * (J + 1)
    for t in range(1, J + 1):
        npow[t] = npow[t - 1] * n
    P = 1
    num = 0
    for j in range(J + 1):
        if j > 0:
            P *= (n - j)
        num += P * npow[J - j]
    lo = F(num, npow[J])
    termJ = F(P, npow[J])
    if J >= n - 1:
        return lo, lo
    tail_hi = termJ * F(n - J - 1, J + 1)
    return lo, lo + tail_hi

# ------------------------------------------------- closed-form phi_n^{(K)}
def rising(n, j):
    """(n+1)(n+2)...(n+j) = (n+j)!/n!"""
    p = 1
    for l in range(1, j + 1):
        p *= (n + l)
    return p

def psi_nK(n, K):
    """Estagio 9 Corolario A1:
       psi_n^{(K)} = (phi_K/4^K) * sum_{j=0}^{K} C(2K+1,K-j) (n+j)!/(n! n^j).
       Valid n >= K+1.  phi_K/4^K = (K!)^2/(2K+1)!."""
    pref = F(factorial(K)**2, factorial(2 * K + 1))
    s = F(0)
    for j in range(K + 1):
        s += comb(2 * K + 1, K - j) * F(rising(n, j), n**j)
    return pref * s

def psi_nK_R(n, K):
    """u_prime Proposicao 2.1:
       psi_n^{(K),R} = kappa * sum_{i=1}^{K} C(2K,K-i) g(i;n),
       kappa=(K-1)! K!/(2K)!, g(i;n)=(n+i)!/(n! n^i).  K>=1."""
    kappa = F(factorial(K - 1) * factorial(K), factorial(2 * K))
    s = F(0)
    for i in range(1, K + 1):
        s += comb(2 * K, K - i) * F(rising(n, i), n**i)
    return kappa * s

def phi_nK(n, K):
    """Lemma A (k2_open_lemma, cited in u_prime (2.1)):
       phi_n^{(K)} = (K/n) psi^R + (1-K/n) psi, exact for n > K;
       boundary K=n: phi_n^{(n)} = Q(n)/n (Prop. 7.1);
       K=0: exactly 1."""
    if K == 0:
        return F(1)
    if K == n:
        return Q_exact(n) / n
    if not (0 < K < n):
        raise ValueError((n, K))
    return F(K, n) * psi_nK_R(n, K) + (1 - F(K, n)) * psi_nK(n, K)

def phi_nK_table(n):
    """[phi_n^{(K)} for K=0..n], reusing one pass."""
    return [phi_nK(n, K) for K in range(n + 1)]

# ------------------------------------------------------------- the mixture
def phi_mix(n, c, table=None):
    """Fact 4.1 (7.1): phi(n,c) = sum_K C(n,K)(c/n)^K (1-c/n)^{n-K} phi_n^{(K)},
       exact rational for rational 0 <= c <= n."""
    c = F(c)
    assert 0 <= c <= n
    if table is None:
        table = phi_nK_table(n)
    p, q = c.numerator, c.denominator
    a, b = p, n * q - p          # c/n = a/(nq); 1-c/n = b/(nq)
    D = (n * q)**n
    num = F(0)
    pw_a = [1] * (n + 1)
    pw_b = [1] * (n + 1)
    for t in range(1, n + 1):
        pw_a[t] = pw_a[t - 1] * a
        pw_b[t] = pw_b[t - 1] * b
    for K in range(n + 1):
        w = comb(n, K) * pw_a[K] * pw_b[n - K]
        if w:
            num += w * table[K]
    return num / D

# ------------------------------------------------------------ phi_inf, I2
def phi_inf_bracket(c, extra_terms=25):
    """certified [lo,hi] for phi_inf(c) = int_0^1 e^{-c t^2} dt, rational c>=0.
       c <= 40: exact alternating series sum_k (-c)^k/(k!(2k+1))  (Cor. 4.1),
                remainder bounded by first omitted term once terms decrease
                (|t_{k+1}/t_k| = c(2k+1)/((k+1)(2k+3)) < 1 for k+1 > c).
       c  > 40: tail form (Cor. 4.2): phi_inf = sqrt(pi)/(2 sqrt(c)) - R,
                0 < R < e^{-c}/(2c) < 2^{-floor(c)}/(2c)  (e>2)."""
    c = F(c)
    assert c >= 0
    if c <= 40:
        eps = F(1, 10**45)
        S = F(0)
        term = F(1)          # (-c)^k / k! at k=0
        k = 0
        while k <= int(c) + 2 or abs(term) / (2 * k + 1) > eps:
            S += term / (2 * k + 1)
            k += 1
            term *= -c / k
            assert k < 4000
        rem = abs(term) / (2 * k + 1)
        # ensure remainder-domination hypothesis holds at k
        assert k + 1 > c
        return S - rem, S + rem
    slo, shi = sqrt_bracket(c)
    main_lo = SQRT_PI_LO / (2 * shi)
    main_hi = SQRT_PI_HI / (2 * slo)
    Rhi = F(1, 2**int(c)) / (2 * c)
    return main_lo - Rhi, main_hi

def I2_bracket(c, extra_terms=25):
    """certified [lo,hi] for I2(c)=int_0^1 t^4 e^{-c t^2} dt, rational c>=0,
       exact alternating series sum_k (-c)^k/(k!(2k+5)); same remainder
       control as above (|t_{k+1}/t_k| = c(2k+5)/((k+1)(2k+7)) < 1 for
       k+1 > c). Intended for c <= ~200."""
    c = F(c)
    assert c >= 0
    eps = F(1, 10**45)
    S = F(0)
    term = F(1)
    k = 0
    while k <= int(c) + 2 or abs(term) / (2 * k + 5) > eps:
        S += term / (2 * k + 5)
        k += 1
        term *= -c / k
        assert k < 4000
    rem = abs(term) / (2 * k + 5)
    assert k + 1 > c
    lo, hi = S - rem, S + rem
    if lo < 0:
        lo = F(0)
    return lo, hi

# ------------------------------------------------- brute force Definition 4
def _cyclic_count(f, n):
    """# of cyclic points of mapping f: list of length n, values 0..n-1.
       cyclic set = image of f^n (after n steps every point is on a cycle,
       and f^n restricted to each cycle is a bijection of it)."""
    g = list(range(n))
    for _ in range(n):
        g = [f[x] for x in g]
    return len(set(g))

def phi_nK_bruteforce(n, K):
    """Definition 4 by exhaustive enumeration.
       By the exchangeability stated in Definition 4 the rerouted set may be
       fixed as {0,...,K-1}; enumerate all n! permutations pi and all n^K
       destination vectors; f(i)=U_i for i<K, f(i)=pi(i) otherwise."""
    from itertools import permutations, product
    tot = 0
    cnt = 0
    for pi in permutations(range(n)):
        base = list(pi)
        for dest in product(range(n), repeat=K):
            f = list(dest) + base[K:]
            tot += _cyclic_count(f, n)
            cnt += 1
    return F(tot, cnt * n)
