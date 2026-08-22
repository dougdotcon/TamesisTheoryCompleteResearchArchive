"""
PART A, item 1 (adversarial referee, k6_attempt).

Independent re-derivation / re-execution of the K=6 closed form, and (the
task's explicit requirement) an independent SUBSTITUTION check: build the full
ladder g_0,h_0,...,g_6,h_6 (K=6) via the (already independently referee-
verified-sound, k3_attempt_2/adversarial/REFEREE_REPORT.md) markov_transfer.py
machinery, then -- freshly, from the Proposition's stated formulas (typed by
hand here, NOT imported from any script) -- verify that EVERY one of the 13
resulting closed forms satisfies the EXACT defining recursion of
../ATTEMPT.md Sec.2, symbolically (sympy simplify(LHS-RHS)==0), for symbolic
n and b. This is the strong form of check the task requests: not "did the
document's own script run without crashing," but "does the claimed closed
form actually solve the functional equation."

Also independently cross-checks the final psi_n^(6) = g_6(n,0) against the
document's claimed closed form, and its own separate, from-scratch memoized
exact-Fraction direct recursion (not markov_direct.py) for many n.
"""
import sys
sys.path.insert(0, '/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/theorem/k2_open_lemma/k3_attempt_2')
import sympy as sp
import markov_transfer as mt
from fractions import Fraction as F

n_sym = mt.n
b_sym = mt.b

print("=" * 70)
print("STEP 1: build the K=6 ladder via markov_transfer.py's build_levels")
print("        (this module was independently re-derived and found SOUND by")
print("        the k3_attempt_2 adversarial referee via a DIFFERENT method")
print("        [integrating factor vs hockey-stick] -- reused here as a")
print("        validated foundation, not blind trust in THIS document's")
print("        own extend_frontier.py output).")
print("=" * 70)
levels = mt.build_levels(6)

psi6_mine = sp.simplify(levels[6][0](n_sym, 0))
print("psi_n^(6) via my own build_levels(6) call =", psi6_mine)

psi6_claimed = sp.together(
    sp.Rational(2048, 1) * n_sym**6 + 3072 * n_sym**5 + 4293 * n_sym**4
    + 4638 * n_sym**3 + 3529 * n_sym**2 + 1662 * n_sym + 360
) / (6006 * n_sym**6)
print("psi_n^(6) as claimed in ATTEMPT.md               =", psi6_claimed)
diff = sp.simplify(psi6_mine - psi6_claimed)
print("difference (should be 0):", diff)
assert diff == 0, "MISMATCH in psi_n^(6)!"
print("MATCH: my own re-execution of the K=6 ladder reproduces the document's")
print("claimed closed form exactly.")
print()

print("=" * 70)
print("STEP 2: substitute EVERY level's closed form back into the EXACT")
print("        defining recursion (typed fresh from ../ATTEMPT.md Sec.2's")
print("        Proposition, not imported), symbolic n,b -- the task's")
print("        explicit request: 'substituting back into the exact")
print("        recursion', not just 'the solver ran'.")
print("=" * 70)


def check_g_recursion(r, g_r_func, h_prev_func, label):
    """g(a,b,r) = 1/m + (r/m) h_{r-1}(a+1,b,r-1) + ((m-1-r-b)/m) g(a+1,b,r)
    restated in m := n-a form (a+1 <-> m-1):
      g_r(m,b) = 1/m + (r/m) h_{r-1}(n-m+1,b) + ((m-1-r-b)/m) g_r(m-1,b)
    """
    m = sp.Symbol('m', positive=True)
    lhs = g_r_func(m, b_sym)
    term_h = 0
    if r >= 1:
        term_h = sp.Rational(r, 1) / m * h_prev_func(n_sym - m + 1, b_sym)
    term_g = (m - 1 - r - b_sym) / m * g_r_func(m - 1, b_sym)
    rhs = sp.Rational(1, 1) / m + term_h + term_g
    diff = sp.simplify(lhs - rhs)
    print(f"  {label}: LHS-RHS simplify = {diff}   {'OK' if diff == 0 else '*** MISMATCH ***'}")
    return diff == 0


def check_h_recursion(r, h_r_func, h_prev_func, g_r_func, label):
    """h(a,b,r) = 1/n + (r/n) h_{r-1}(a,b+1,r-1) + ((n-1-a-b-r)/n) g_r(a,b+1,r)"""
    a = sp.Symbol('a', positive=True)
    lhs = h_r_func(a, b_sym)
    term_h = 0
    if r >= 1:
        term_h = sp.Rational(r, 1) / n_sym * h_prev_func(a, b_sym + 1)
    term_g = (n_sym - 1 - a - b_sym - r) / n_sym * g_r_func(n_sym - a, b_sym + 1)
    rhs = sp.Rational(1, 1) / n_sym + term_h + term_g
    diff = sp.simplify(lhs - rhs)
    print(f"  {label}: LHS-RHS simplify = {diff}   {'OK' if diff == 0 else '*** MISMATCH ***'}")
    return diff == 0


all_ok = True
g_prev = None
h_prev = None
for r in range(0, 7):
    g_r, h_r = levels[r]
    ok_g = check_g_recursion(r, g_r, h_prev, f"g_{r} recursion (r={r})")
    all_ok = all_ok and ok_g
    ok_h = check_h_recursion(r, h_r, h_prev, g_r, f"h_{r} recursion (r={r})")
    all_ok = all_ok and ok_h
    h_prev = h_r

print()
print("ALL 13 LEVELS (g_0..g_6, h_0..h_6) SATISFY THE EXACT RECURSION:", all_ok)
assert all_ok
print()

print("=" * 70)
print("STEP 3: a SECOND, independent memoized exact-Fraction direct recursion")
print("        (fresh code, NOT markov_direct.py) for K=6, checked against the")
print("        closed form for n=7..40 (well beyond direct_check_k6.py's n=7..25).")
print("=" * 70)


def psi_direct_fresh(n, K):
    """Fresh memoized Fraction implementation of the exact transition rules,
    written independently of markov_direct.py."""
    memo_g = {}
    memo_h = {}

    def g(a, bb, r):
        if r == 0:
            return F(1, bb + 1)
        key = (a, bb, r)
        if key in memo_g:
            return memo_g[key]
        m = n - a
        # Terminal state: m == r+bb+1 makes the "continue" coefficient
        # (m-1-r-bb)/m exactly 0 -- do NOT recurse further (that state,
        # m=r+bb, is outside the valid domain a+b+r<n and must not be
        # evaluated even though its coefficient is zero).
        if m == r + bb + 1:
            val = F(1, m) + F(r, m) * h(a + 1, bb, r - 1)
        else:
            val = F(1, m) + F(r, m) * h(a + 1, bb, r - 1) + F(m - 1 - r - bb, m) * g(a + 1, bb, r)
        memo_g[key] = val
        return val

    def h(a, bb, r):
        if r == 0:
            return F(n - a + 1, n * (bb + 2))
        key = (a, bb, r)
        if key in memo_h:
            return memo_h[key]
        cont_num = n - 1 - a - bb - r
        if cont_num == 0:
            val = F(1, n) + F(r, n) * h(a, bb + 1, r - 1)
        else:
            val = F(1, n) + F(r, n) * h(a, bb + 1, r - 1) + F(cont_num, n) * g(a, bb + 1, r)
        memo_h[key] = val
        return val

    return g(0, 0, K)


mismatch = False
for nv in range(7, 41):
    closed = sp.Rational(psi6_claimed.subs(n_sym, nv))
    direct = psi_direct_fresh(nv, 6)
    direct_frac = F(direct.numerator, direct.denominator)
    ok = (sp.Rational(direct_frac.numerator, direct_frac.denominator) == closed)
    if not ok:
        mismatch = True
        print(f"  n={nv}: direct={direct}  closed={closed}  *** MISMATCH ***")
print(f"n=7..40 (34 values): {'ALL MATCH, 0 mismatches' if not mismatch else 'MISMATCHES FOUND'}")
assert not mismatch

print()
print("=" * 70)
print("STEP 4: sanity -- n->infinity limit and 1/n coefficient of psi_n^(6)")
print("=" * 70)
lim6 = sp.limit(psi6_claimed, n_sym, sp.oo)
phi6 = sp.Rational(4**6 * sp.factorial(6)**2, sp.factorial(13))
rate6 = sp.limit((psi6_claimed - phi6) * n_sym, n_sym, sp.oo)
print(f"lim psi_n^(6) = {lim6}  (phi_6 = {phi6}, match={lim6==phi6})")
print(f"1/n coeff = {rate6}  (6*phi_6/4 = {sp.simplify(sp.Rational(6,4)*phi6)}, match={rate6==sp.simplify(sp.Rational(6,4)*phi6)})")

print()
print("ALL PART-A-ITEM-1 CHECKS PASSED.")
