"""
ADVERSARIAL REFEREE SCRIPT 4 (from scratch).

Two jobs:

(A) Re-compute EVERY cell of the target document's section 3 table
    (phi_K, F_{K-1}(1,1), v_K, c_K for K = 1..16 and 20) with exact
    Fractions, and diff against the transcribed values.

(B) Independently re-do the target's section 6 finite-n corroboration:
    implement the RAW (a,b,r) transition rules of k3_attempt_2/ATTEMPT.md
    section 2 from scratch (memoized exact Fractions), form
        varphi_n^{(K)} = (K/n) psi_n^{(K),R} + (1-K/n) psi_n^{(K)}
                       = (K/n) h(0,0,K-1) + (1-K/n) g(0,0,K)
    (wave 5 Reduction Lemma A), and extract the exact 1/n coefficient by
    an EXACT rational fit of varphi_n^{(K)} as a polynomial in 1/n,
    validated OUT OF SAMPLE on n values the fit never saw.
    Then compare alpha_1 against c_K = [(K+2)phi_K-2]/4.

    This is the only check that the object proved positive is really the
    1/n coefficient of the finite-n quantity, i.e. the transcription guard.
"""

from fractions import Fraction as Fr
from math import factorial
import sys

sys.setrecursionlimit(1000000)


def phi(K):
    return Fr(4 ** K * factorial(K) ** 2, factorial(2 * K + 1))


def F_closed(r, t, b):
    tot = Fr(0)
    for k in range(r + 1):
        den = 1
        for i in range(1, k + 2):
            den *= (r + b + i)
        tot += Fr(factorial(r), factorial(r - k)) * (t ** k) / den
    return tot


def c_thmA(K):
    return ((K + 2) * phi(K) - 2) / 4


# ---------------------------------------------------------------- (A)
print("=" * 104)
print("(A) Re-computation of the target document's section 3 table, cell by cell")
print("=" * 104)

TARGET_TABLE = {
    # K : (phi_K, F_{K-1}(1,1), v_K, c_K)   -- transcribed from ATTEMPT.md section 3
    1:  ("2/3", "1/2", "2", "0"),
    2:  ("8/15", "5/12", "32/15", "1/30"),
    3:  ("16/35", "11/30", "16/7", "1/14"),
    4:  ("128/315", "93/280", "256/105", "23/210"),
    5:  ("256/693", "193/630", "256/99", "29/198"),
    6:  ("1024/3003", "793/2772", "8192/3003", "1093/6006"),
    7:  ("2048/6435", "1619/6006", "2048/715", "309/1430"),
    8:  ("32768/109395", "26333/102960", "65536/21879", "10889/43758"),
    9:  ("65536/230945", "53381/218790", "65536/20995", "11773/41990"),
    10: ("262144/969969", "43191/184756", "1048576/323323", "200965/646646"),
    11: ("524288/2028117", "436109/1939938", "524288/156009", "106135/312018"),
    12: ("4194304/16900975", "1172755/5408312", "8388608/2414425", "1779879/4828850"),
    13: ("8388608/35102025", "7088533/33801950", "8388608/2340135", "1854169/4680270"),
    14: ("33554432/145422675", "28539857/140408100", "536870912/145422675",
         "123012781/290845350"),
    15: ("67108864/300540195", "57414019/290845350", "67108864/17678835",
         "15875597/35357670"),
    16: ("2147483648/9917826435", "1846943453/9617286240", "4294967296/1101980715",
         "1045502933/2203961430"),
    20: ("274877906944/1412926920405", "240416274739/1378465288200",
         "549755813888/128447901855", "146430005089/256895803710"),
}

DECIMALS = {1: 0.000000000, 2: 0.033333333, 3: 0.071428571, 4: 0.109523810,
            5: 0.146464646, 6: 0.181984682, 7: 0.216083916, 8: 0.248845925,
            9: 0.280376280, 10: 0.310780551, 11: 0.340156658, 12: 0.368592729,
            13: 0.396167101, 14: 0.422949107, 15: 0.449000090, 16: 0.474374424,
            20: 0.569997653}

bad_cells = []
for K in sorted(TARGET_TABLE):
    ph_t, F_t, v_t, c_t = (Fr(s) for s in TARGET_TABLE[K])
    ph_m = phi(K)
    F_m = F_closed(K - 1, Fr(1), 1)
    v_m = (K + 2) * ph_m
    c_m = c_thmA(K)
    row_ok = (ph_t == ph_m, F_t == F_m, v_t == v_m, c_t == c_m)
    dec_ok = abs(float(c_m) - DECIMALS[K]) < 5e-9
    if not all(row_ok) or not dec_ok:
        bad_cells.append((K, row_ok, dec_ok, str(c_m), float(c_m)))
    print("  K=%-3d phi:%-5s  F:%-5s  v:%-5s  c:%-5s  decimal(%.9f vs printed %.9f):%s"
          % (K, row_ok[0], row_ok[1], row_ok[2], row_ok[3],
             float(c_m), DECIMALS[K], dec_ok))
print("  BAD CELLS:", bad_cells if bad_cells else "none -- all 17 rows x 5 entries exact")


# ---------------------------------------------------------------- (B)
print()
print("=" * 104)
print("(B) Independent finite-n corroboration from the RAW (a,b,r) transition rules")
print("=" * 104)
print("    g(a,b,r) = 1/m + (r/m) h(a+1,b,r-1) + ((m-1-r-b)/m) g(a+1,b,r),  m = n-a")
print("    h(a,b,r) = 1/n + (r/n) h(a,b+1,r-1) + ((n-1-a-b-r)/n) g(a,b+1,r)")
print("    psi_n^(K) = g(0,0,K);  psi_n^(K),R = h(0,0,K-1)")
print("    varphi_n^(K) = (K/n) psi_n^(K),R + (1-K/n) psi_n^(K)     [Reduction Lemma A]")
print()


def chain(n, K):
    """Exact varphi_n^{(K)} from the raw rules. Memoized recursion, Fractions."""
    gmemo, hmemo = {}, {}

    def g(a, b, r):
        m = n - a
        if m <= 0:
            return Fr(0)
        # the recursion's own coefficient (m-1-r-b)/m vanishes at m = 1+r+b;
        # wave 6's convention g(b+r,b,r) := 0 is what that forces.
        key = (a, b, r)
        if key in gmemo:
            return gmemo[key]
        coef = m - 1 - r - b
        val = Fr(1, m)
        if r > 0:
            val += Fr(r, m) * h(a + 1, b, r - 1)
        if coef > 0:
            val += Fr(coef, m) * g(a + 1, b, r)
        gmemo[key] = val
        return val

    def h(a, b, r):
        key = (a, b, r)
        if key in hmemo:
            return hmemo[key]
        val = Fr(1, n)
        if r > 0:
            val += Fr(r, n) * h(a, b + 1, r - 1)
        coef = n - 1 - a - b - r
        if coef > 0:
            val += Fr(coef, n) * g(a, b + 1, r)
        hmemo[key] = val
        return val

    psi = g(0, 0, K)
    psiR = h(0, 0, K - 1) if K >= 1 else Fr(0)
    return Fr(K, n) * psiR + (1 - Fr(K, n)) * psi


# --- sanity 1: wave 6's PROVED closed form for varphi_n^{(3)}
print("  sanity 1: varphi_n^{(3)} == 16/35 + 1/(14n) + 11/(10n^2) + 23/(35n^3) + 6/(35n^4)")
ok1 = True
for n in range(4, 27):
    lhs = chain(n, 3)
    rhs = (Fr(16, 35) + Fr(1, 14) / n + Fr(11, 10) / n ** 2
           + Fr(23, 35) / n ** 3 + Fr(6, 35) / n ** 4)
    if lhs != rhs:
        ok1 = False
        print("    MISMATCH n=%d: %s vs %s" % (n, lhs, rhs))
print("    n=4..26 exact:", ok1)

# --- sanity 2: the K=1 degeneracy
print("  sanity 2: varphi_n^{(1)} - varphi_1 == 1/(3 n^2)  (the K=1 Theta(1/n^2) case)")
ok2 = all(chain(n, 1) - Fr(2, 3) == Fr(1, 3 * n * n) for n in range(2, 41))
print("    n=2..40 exact:", ok2)
for n in (3, 5, 10, 20):
    print("      n=%-3d varphi_n^(1)=%-10s  diff=%-10s  n^2*diff=%s"
          % (n, chain(n, 1), chain(n, 1) - Fr(2, 3),
             (chain(n, 1) - Fr(2, 3)) * n * n))

# --- exact polynomial-in-1/n fit with out-of-sample validation
def solve_exact(A, rhs):
    """Gaussian elimination over Fraction."""
    N = len(A)
    M = [row[:] + [rhs[i]] for i, row in enumerate(A)]
    for col in range(N):
        piv = next(r for r in range(col, N) if M[r][col] != 0)
        M[col], M[piv] = M[piv], M[col]
        pv = M[col][col]
        M[col] = [x / pv for x in M[col]]
        for r in range(N):
            if r != col and M[r][col] != 0:
                f = M[r][col]
                M[r] = [x - f * y for x, y in zip(M[r], M[col])]
    return [M[i][N] for i in range(N)]


print()
print("  EXACT polynomial-in-1/n fit of varphi_n^{(K)}, validated out of sample:")
print("  %3s %3s %-24s %-8s %-24s %-8s %-6s" %
      ("K", "D", "alpha_0", "=phi_K?", "alpha_1", "=c_K?", "OOS"))
allok = True
for K in range(1, 10):
    D = K + 1                      # degree in 1/n; D+1 unknowns
    nfit = list(range(K + 3, K + 3 + D + 1))
    A = [[Fr(1, n) ** j for j in range(D + 1)] for n in nfit]
    rhs = [chain(n, K) for n in nfit]
    alpha = solve_exact(A, rhs)
    # out-of-sample validation on 6 n values never used in the fit
    noos = list(range(nfit[-1] + 1, nfit[-1] + 7))
    oos = all(sum(alpha[j] * Fr(1, n) ** j for j in range(D + 1)) == chain(n, K)
              for n in noos)
    a0ok = (alpha[0] == phi(K))
    a1ok = (alpha[1] == c_thmA(K))
    if not (oos and a0ok and a1ok):
        allok = False
    print("  %3d %3d %-24s %-8s %-24s %-8s %-6s" %
          (K, D, str(alpha[0]), a0ok, str(alpha[1]), a1ok, oos))

print()
print("  ALL K=1..9: alpha_0==phi_K, alpha_1==c_K, out-of-sample validated:", allok)
print()
print("OVERALL:", "PASS" if (not bad_cells and ok1 and ok2 and allok) else "FAIL")
