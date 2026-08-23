"""
Independent re-derivation of the Abel-summation-by-parts identities I1, I3,
I5, I7 -- AND a from-scratch proof that the underlying mechanism generalises
to EVERY odd power S_{2k-1}, not just k=1,2,3,4.

Everything here is derived by hand (see accompanying prose in the referee
report) and then checked two ways:
  (a) direct brute-force summation (independent ground truth for the
      identity itself, nothing to do with general_b_dstar_attempt's scripts)
  (b) sympy symbolic expansion, to make sure no algebra slip survives.

No file from general_b_dstar_attempt is imported or read here.
"""
from fractions import Fraction
import sympy as sp


def binom_conv(n, k):
    if k < 0 or k > n or n < 0:
        return Fraction(0)
    num = 1
    for i in range(k):
        num *= (n - i)
    den = 1
    for i in range(1, k + 1):
        den *= i
    return Fraction(num, den)


def S_direct(power, N, m):
    """S_power(N,m) := sum_{i=0}^{m} (N-2i)^power * C(N,i), brute force."""
    if m < 0:
        return Fraction(0)
    total = Fraction(0)
    for i in range(0, m + 1):
        total += Fraction((N - 2 * i) ** power) * binom_conv(N, i)
    return total


# ---------------------------------------------------------------------------
# PART A. Hand re-derivation of the general Abel-summation recursion.
#
# Claim (derived from scratch, see referee report prose for the full
# by-hand derivation):
#
#   S_1(N,m) = (m+1) C(N,m+1)                                   [I1, base case]
#
#   For k>=2, writing g(i):=(N-2i)^{2k-2}, A(i):=(i+1)C(N,i+1):
#
#   S_{2k-1}(N,m) = g(m) A(m) - sum_{i=0}^{m-1} A(i) [g(i+1)-g(i)]
#                 = (N-2m)^{2k-2} (m+1) C(N,m+1)
#                   + 2N * sum_{s odd, 1<=s<=2k-3} C(2k-2, s) * S_s(N-1, m-1)
#
# The key sub-step: with y := N-2i-2 (i.e. shifting to j=i+1), w := y+1,
#   g(i+1)-g(i) = y^{2k-2} - (y+2)^{2k-2} = (w-1)^{2k-2} - (w+1)^{2k-2}
#               = -2 * sum_{t odd, 1<=t<=2k-3} C(2k-2,t) w^{2k-2-t}
# which contains ONLY ODD powers of w whenever 2k-2 is even (i.e. for
# EVERY k>=1) -- a one-line consequence of (w-1)^n-(w+1)^n being an odd
# function of w for even n (binomial expansion: the (-1)^t-1 factor kills
# every even-t term, and n-t has parity opposite to t when n is even).
# ---------------------------------------------------------------------------

def S_recursive(power, N, m, memo=None):
    """S_power(N,m) via the general recursion above. power must be odd."""
    assert power % 2 == 1
    if memo is None:
        memo = {}
    key = (power, N, m)
    if key in memo:
        return memo[key]
    if m < 0:
        memo[key] = Fraction(0)
        return memo[key]
    if power == 1:
        val = Fraction(m + 1) * binom_conv(N, m + 1)
        memo[key] = val
        return val
    n_exp = power - 1  # = 2k-2, even
    k = (power + 1) // 2
    val = Fraction((N - 2 * m) ** n_exp) * Fraction(m + 1) * binom_conv(N, m + 1)
    total_tail = Fraction(0)
    for t in range(1, n_exp, 2):  # t odd, 1..2k-3 (n_exp=2k-2, so up to n_exp-1)
        s = n_exp - t  # also odd, ranges 2k-3 downto 1
        coeff = binom_conv(n_exp, t)  # integer binomial C(2k-2, t)
        total_tail += coeff * S_recursive(s, N - 1, m - 1, memo)
    val += 2 * N * total_tail
    memo[key] = val
    return val


def verify_recursion_bruteforce(max_power, N_max):
    """Cross-check S_recursive vs S_direct exhaustively."""
    fails = 0
    checks = 0
    for power in range(1, max_power + 1, 2):
        for N in range(0, N_max + 1):
            for m in range(-1, N + 1):
                a = S_recursive(power, N, m)
                b = S_direct(power, N, m)
                checks += 1
                if a != b:
                    fails += 1
                    print(f"FAIL power={power} N={N} m={m}: recursive={a} direct={b}")
    print(f"verify_recursion_bruteforce(max_power={max_power},N_max={N_max}): "
          f"{checks} checks, {fails} failures")
    return fails


# ---------------------------------------------------------------------------
# PART B. Match the document's I5, I7 closed forms exactly against the
# general recursion (sanity: the document's I5/I7 are just the k=3,4
# instances of the fully general recursion derived above).
# ---------------------------------------------------------------------------

def doc_S5(N, m):
    """Document's claimed closed form for S_5, transcribed EXACTLY as printed
    in ATTEMPT.md sec 3.3 (for cross-checking against my own independent
    S_recursive / S_direct, not as ground truth)."""
    return Fraction((N - 2 * m) ** 4) * Fraction(m + 1) * binom_conv(N, m + 1) \
        + 8 * N * (S_direct(3, N - 1, m - 1) + S_direct(1, N - 1, m - 1))


def doc_S7(N, m):
    """Document's claimed closed form for S_7, transcribed EXACTLY as printed."""
    return Fraction((N - 2 * m) ** 6) * Fraction(m + 1) * binom_conv(N, m + 1) \
        + N * (12 * S_direct(5, N - 1, m - 1) + 40 * S_direct(3, N - 1, m - 1)
               + 12 * S_direct(1, N - 1, m - 1))


def verify_doc_formulas(N_max):
    fails = 0
    checks = 0
    for N in range(0, N_max + 1):
        for m in range(-1, N + 1):
            checks += 1
            if doc_S5(N, m) != S_direct(5, N, m):
                fails += 1
                print("FAIL doc I5", N, m)
            checks += 1
            if doc_S7(N, m) != S_direct(7, N, m):
                fails += 1
                print("FAIL doc I7", N, m)
    print(f"verify_doc_formulas(N_max={N_max}): {checks} checks, {fails} failures")
    return fails


# ---------------------------------------------------------------------------
# PART C. Symbolic (sympy) re-derivation of the (w-1)^n-(w+1)^n parity fact,
# and symbolic expansion of the I5/I7 Delta-f polynomials (redoing the exact
# "checked symbolically" step the document asserts but does not show).
# ---------------------------------------------------------------------------

def symbolic_parity_check(max_n_exp):
    """For every even n_exp = 2,4,...,max_n_exp, confirm symbolically that
    (w-1)^n_exp - (w+1)^n_exp, expanded, has ZERO coefficient on every EVEN
    power of w (including the constant term)."""
    w = sp.symbols('w')
    fails = 0
    for n_exp in range(2, max_n_exp + 1, 2):
        expr = sp.expand((w - 1) ** n_exp - (w + 1) ** n_exp)
        poly = sp.Poly(expr, w)
        for (deg,), coeff in poly.terms():
            if deg % 2 == 0 and coeff != 0:
                fails += 1
                print(f"FAIL parity n_exp={n_exp}: even-degree term w^{deg} "
                      f"has nonzero coeff {coeff}")
    print(f"symbolic_parity_check(max_n_exp={max_n_exp}): "
          f"{max_n_exp // 2} even exponents checked, {fails} failures")
    return fails


def symbolic_I5_I7_deltaf():
    """Symbolically expand y^4-(y+2)^4 and y^6-(y+2)^6 in terms of
    w := y+1, and print the resulting polynomials, matching them against
    the document's printed intermediate results."""
    y, w = sp.symbols('y w')
    d5 = sp.expand((y) ** 4 - (y + 2) ** 4)
    d5w = sp.expand(d5.subs(y, w - 1))
    d7 = sp.expand((y) ** 6 - (y + 2) ** 6)
    d7w = sp.expand(d7.subs(y, w - 1))
    print("y^4-(y+2)^4 in w:", d5w, " -- document claims -8w^3-8w (equiv -(8y^3+24y^2+32y+16) in y)")
    print("y^6-(y+2)^6 in w:", d7w, " -- document claims -12w^5-40w^3-12w")
    ok5 = sp.simplify(d5w - (-8 * w ** 3 - 8 * w)) == 0
    ok7 = sp.simplify(d7w - (-12 * w ** 5 - 40 * w ** 3 - 12 * w)) == 0
    print("I5 delta-f matches document:", ok5)
    print("I7 delta-f matches document:", ok7)
    return ok5 and ok7


if __name__ == "__main__":
    print("=" * 70)
    print("PART A: general recursion vs brute force, powers up to 21 (k up to 11),")
    print("far beyond the document's k=1..4 (I1,I3,I5,I7)")
    f1 = verify_recursion_bruteforce(max_power=21, N_max=27)

    print("=" * 70)
    print("PART B: document's I5,I7 closed forms vs brute force")
    f2 = verify_doc_formulas(N_max=45)

    print("=" * 70)
    print("PART C: symbolic parity check, n_exp up to 40 (k up to 21)")
    f3 = symbolic_parity_check(max_n_exp=40)

    print("=" * 70)
    print("PART C2: symbolic expansion of I5/I7 Delta-f, matching document's")
    print("intermediate polynomials exactly")
    ok = symbolic_I5_I7_deltaf()

    total_fails = f1 + f2 + f3 + (0 if ok else 1)
    print("=" * 70)
    print(f"TOTAL FAILURES: {total_fails}")
