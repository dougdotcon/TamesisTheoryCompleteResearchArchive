"""
ground_truth.py -- independent, from-scratch implementation of Corollary A3
(all_orders_closed_form_attempt/ATTEMPT.md Sec 4.3, PROVED, cited, not
re-derived):

    D^{*(p)}_r(b) = sum_{j=p}^{r} c_j^{(r)}(b) * c(j+1, j+1-p)

    c_j^{(r)}(b) := r! / [ (r-j)! * prod_{i=1}^{j+1} (r+b+i) ]

    c(N, M) := unsigned Stirling numbers of the first kind.

This is the ground truth every other script in this directory is checked
against. Written fresh for this front (wave 18, GENERAL-P-DSTAR-EXTENSION2
-ATTEMPT) -- no code imported from any predecessor front's scripts, per the
task mandate (predecessor .py files were not even opened).

Own unsigned-Stirling-number recurrence:
    c(0,0) = 1
    c(n,0) = 0            for n >= 1
    c(n,k) = c(n-1,k-1) + (n-1)*c(n-1,k)     for 1 <= k <= n

Exact rational arithmetic throughout (fractions.Fraction). No floating
point anywhere in this file.
"""

from fractions import Fraction
from functools import lru_cache
import math


# ---------------------------------------------------------------------------
# Unsigned Stirling numbers of the first kind, c(n,k), via own recurrence.
# ---------------------------------------------------------------------------

@lru_cache(maxsize=None)
def stirling1_unsigned(n, k):
    """c(n,k), unsigned Stirling number of the first kind."""
    if n == 0 and k == 0:
        return 1
    if n == 0:
        return 0
    if k == 0:
        return 0
    if k > n:
        return 0
    return stirling1_unsigned(n - 1, k - 1) + (n - 1) * stirling1_unsigned(n - 1, k)


# ---------------------------------------------------------------------------
# c_j^{(r)}(b) and D^{*(p)}_r(b)
# ---------------------------------------------------------------------------

def c_j_r_b(j, r, b):
    """c_j^{(r)}(b) = r! / [ (r-j)! * prod_{i=1}^{j+1} (r+b+i) ], exact Fraction.

    Valid for 0 <= j <= r (r!/(r-j)! is the falling factorial r(r-1)...(r-j+1),
    j factors; empty product = 1 at j=0)."""
    if j < 0 or j > r:
        return Fraction(0)
    num = 1
    for t in range(j):
        num *= (r - t)
    den = 1
    for i in range(1, j + 2):
        den *= (r + b + i)
    return Fraction(num, den)


def D_star(p, r, b):
    """D^{*(p)}_r(b), exact Fraction, via Corollary A3 directly.

    The sum over j runs p..r; if r < p the sum is empty and the value is
    exactly 0 (Corollary A3's own vanishing boundary, not a special case)."""
    if r < p:
        return Fraction(0)
    total = Fraction(0)
    for j in range(p, r + 1):
        cj = c_j_r_b(j, r, b)
        if cj == 0:
            continue
        s = stirling1_unsigned(j + 1, j + 1 - p)
        if s == 0:
            continue
        total += cj * s
    return total


@lru_cache(maxsize=None)
def factorial(n):
    """Cached math.factorial -- a pure speed optimization (verified
    identical to math.factorial by construction; also cross-checked in
    self_test() below), since the main verification sweep in assemble.py
    calls factorial-based quantities (phi_r, Phi_b_of_r, w_i) for the
    same small set of r,N values thousands of times across the (p,b)
    grid."""
    return math.factorial(n)


@lru_cache(maxsize=None)
def phi_r(r):
    """phi_r = 4^r (r!)^2 / (2r+1)!, exact Fraction. Cached (see
    factorial() above) -- phi_r(r) does not depend on b, p, so caching
    across the (p,b) sweep avoids recomputing the same large-factorial
    ratio hundreds of times per r value."""
    return Fraction(4 ** r * factorial(r) ** 2, factorial(2 * r + 1))


# ---------------------------------------------------------------------------
# Self-test / calibration against PROVED formulas already in THEOREM.md.
# ---------------------------------------------------------------------------

def _known_p1_b0(r):
    # D^{*(1)}_r(0) = r/4 * phi_r  (Teorema D1 reduction, b=0; cf. Estagio 14
    # table row "p=1,b=0: r/4, remainder 0")
    return Fraction(r, 4) * phi_r(r)


def _known_p2_b0(r):
    # Teorema 3 (Estagio 8): D^*_r(0) = r(3r+1)/32 * phi_r - r/12
    return Fraction(r * (3 * r + 1), 32) * phi_r(r) - Fraction(r, 12)


def _known_p1_b1(r):
    # Estagio 16/closure-attempt calibration table: p=1,b=1: (r+1)/4, -1/4
    return Fraction(r + 1, 4) * phi_r(r) - Fraction(1, 4)


def _known_p2_b1(r):
    # p=2,b=1: (r+1)(3r+8)/32, -(5r+6)/24
    return Fraction((r + 1) * (3 * r + 8), 32) * phi_r(r) - Fraction(5 * r + 6, 24)


def _known_p3_b1(r):
    # p=3,b=1: (r+1)(5r^2+39r+32)/128, -(r+1)(7r+12)/48
    return (Fraction((r + 1) * (5 * r * r + 39 * r + 32), 128) * phi_r(r)
            - Fraction((r + 1) * (7 * r + 12), 48))


def _known_p4_b1(r):
    # p=4,b=1: (r+1)(105r^3+1765r^2+3314r+1536)/6144,
    #          -(45r^3+229r^2+306r+120)/480
    num_coef = 105 * r ** 3 + 1765 * r * r + 3314 * r + 1536
    num_rem = 45 * r ** 3 + 229 * r * r + 306 * r + 120
    return (Fraction((r + 1) * num_coef, 6144) * phi_r(r)
            - Fraction(num_rem, 480))


def _known_p1_b2(r):
    # closure-attempt Theorem D1 instance:
    # D^{*(1)}_r(2) = (r+2)(r+3)/(2(2r+3)) phi_r - (r+2)/(2(r+1))
    return (Fraction((r + 2) * (r + 3), 2 * (2 * r + 3)) * phi_r(r)
            - Fraction(r + 2, 2 * (r + 1)))


def self_test():
    checks = 0
    fails = 0

    # (1) Known PROVED formulas, b=0,1: r = 0..99
    known_b0 = [(1, _known_p1_b0), (2, _known_p2_b0)]
    for p, f in known_b0:
        for r in range(0, 100):
            got = D_star(p, r, 0)
            want = f(r)
            checks += 1
            if got != want:
                fails += 1
                print(f"MISMATCH b0 p={p} r={r}: got {got} want {want}")

    known_b1 = [(1, _known_p1_b1), (2, _known_p2_b1), (3, _known_p3_b1), (4, _known_p4_b1)]
    for p, f in known_b1:
        for r in range(0, 100):
            got = D_star(p, r, 1)
            want = f(r)
            checks += 1
            if got != want:
                fails += 1
                print(f"MISMATCH b1 p={p} r={r}: got {got} want {want}")

    # (2) closure-attempt's printed b=2 instance, p=1
    for r in range(0, 60):
        got = D_star(1, r, 2)
        want = _known_p1_b2(r)
        checks += 1
        if got != want:
            fails += 1
            print(f"MISMATCH b2 p=1 r={r}: got {got} want {want}")

    # (3) r < p vanishing boundary, p = 1..40
    for p in range(1, 41):
        for r in range(0, p):
            for b in (0, 1, 2, 5):
                got = D_star(p, r, b)
                checks += 1
                if got != 0:
                    fails += 1
                    print(f"MISMATCH vanishing p={p} r={r} b={b}: got {got}")

    # (4) D^{*(0)}_r(b) should be Phi_b(r)... actually p=0 means the sum
    # over j=0..r of c_j^{(r)}(b)*c(j+1,j+1) = c_j^{(r)}(b)*1 (since
    # c(N,N)=1 always) -- not independently checked against a named PROVED
    # formula here (p=0 is out of this front's scope; included only as an
    # internal non-negativity/finiteness smoke test, not a calibration
    # target).
    for r in range(0, 20):
        v = D_star(0, r, 0)
        checks += 1
        if v < 0:
            fails += 1
            print(f"UNEXPECTED negative D*(0)_r(0) at r={r}: {v}")

    # (5) cached factorial() matches math.factorial exactly
    for n in range(0, 300):
        checks += 1
        if factorial(n) != math.factorial(n):
            fails += 1
            print(f"MISMATCH factorial cache n={n}")

    print(f"ground_truth.py self_test: {checks} checks, {fails} fails")
    return fails == 0


if __name__ == "__main__":
    ok = self_test()
    print("ground_truth.py: OK" if ok else "ground_truth.py: FAILURES")
