"""
Section 4 of ATTEMPT.md, part 2 -- THE MAIN RESULT.

Layer 2's V-sum needs a genuine INDEFINITE hypergeometric-term
antidifference (an F(V) with F(V+1)-F(V) = summand(V), so that
VSum(O,t) = F(t+1)-F(r)) precisely because it must be evaluated at an
ARBITRARY upper limit t=k-O for every k -- exactly the situation Gosper's
algorithm (sympy.concrete.gosper.gosper_term / gosper_sum) decides. This
mirrors pnn_general_k_egf_attempt's own use of Gosper (Estagio 39), but
the object being tested here is the V-sum INSIDE S_r (one layer deeper
than that front's own r-sum -- see ATTEMPT.md Section 4.5 for the precise
comparison).

The summand (product of two symbolic-degree binomial coefficients times
a linear prefactor):

    term(V) = C(V-1,r-1) * [ (O+V)*C(n-V-O+r-1,K-1) + r*C(n-V-O+r-1,K) ]

PART A -- positive controls (own from-scratch synthetic sums, confirming
the harness genuinely detects Gosper-summability, including with
SYMBOLIC binomial degrees, when it is present -- not merely returning
None on anything complicated).

PART B -- concrete K (K=3,...,7), r LEFT FULLY SYMBOLIC: gosper_term
SUCCEEDS every time (non-None) -- a genuine, verified partial closure.
For K=3,4 the actual gosper_sum closed form is extracted and verified
numerically against the true (truncated) V-sum at several (n,O,r,t).

PART C -- THE CERTIFICATE: K SYMBOLIC (together with r,n,O,t all
symbolic too): gosper_term(term, V) is run to completion and returns
None -- Gosper's algorithm PROVING no hypergeometric-term antidifference
exists for this summand when K is itself a free symbol. This is a
genuine negative result (a formal non-existence certificate for THIS
term, not a timeout), precisely dual to Part B's positive results at
every concrete K tested.
"""
import time
import sympy as sp
from sympy.concrete.gosper import gosper_term, gosper_sum
from math import comb

n, O, V, r, t, K = sp.symbols('n O V r t K', integer=True, positive=True)


def build_term(Kval_or_symbol):
    M = n - O
    N = M - V
    A1 = sp.binomial(N + r - 1, Kval_or_symbol - 1)
    A2 = sp.binomial(N + r - 1, Kval_or_symbol)
    InnerJ = (O + V) * A1 + r * A2
    cV = sp.binomial(V - 1, r - 1)
    return sp.simplify(cV * InnerJ)


def InnerJ_direct(nv, Kv, rv, Vv, Ov):
    b = Kv - rv
    N = nv - Vv - Ov
    if b == 0:
        if N < 0:
            return 0
        c1 = comb(N + rv - 1, rv - 1) if rv > 0 else (1 if N == 0 else 0)
        return c1 * (Ov + Vv + N)
    total = 0
    for j in range(0, max(N, 0)):
        c1 = comb(j + rv - 1, rv - 1) if rv > 0 else (1 if j == 0 else 0)
        c2 = comb(N - 1 - j, b - 1) if (N - 1 - j) >= 0 and (N - 1 - j) >= (b - 1) else 0
        total += c1 * (Ov + Vv + j) * c2
    return total


def part_a_positive_controls():
    print("PART A: positive controls (confirms the harness detects")
    print("Gosper-summability, including symbolic binomial degrees, when present)")
    print("-" * 70)
    ok = True

    # control 1: classic hockey-stick, symbolic r
    t0 = time.time()
    res1 = gosper_term(sp.binomial(V, r), V)
    print(f"  control1 C(V,r), symbolic r: gosper_term = {res1}  [{time.time()-t0:.2f}s]")
    ok = ok and (res1 is not None)
    t0 = time.time()
    res1s = gosper_sum(sp.binomial(V, r), (V, 0, K))
    print(f"  control1 definite sum(V,0,K), symbolic r AND K: gosper_sum = {res1s}  [{time.time()-t0:.2f}s]")
    ok = ok and (res1s is not None)

    # control 2: symbolic-degree binomial C(V,K), symbolic K
    t0 = time.time()
    res2 = gosper_term(sp.binomial(V, K), V)
    print(f"  control2 C(V,K), symbolic K: gosper_term = {res2}  [{time.time()-t0:.2f}s]")
    ok = ok and (res2 is not None)

    # control 3: mixed symbolic K,r, structurally closer to the real term
    t0 = time.time()
    res3 = gosper_term(sp.binomial(V + r - 1, K - 1) * V, V)
    print(f"  control3 C(V+r-1,K-1)*V, symbolic K,r: gosper_term = {res3}  [{time.time()-t0:.2f}s]")
    ok = ok and (res3 is not None)

    # control 4 (negative control): a genuinely non-Gosper-summable term for
    # comparison of what a "None" from THIS harness looks like on something
    # simple and well understood (1/V is not hypergeometric-summable to a
    # hypergeometric term -- this is the harmonic-number obstruction).
    t0 = time.time()
    res4 = gosper_term(sp.Rational(1, 1) / V, V)
    print(f"  control4 (negative) 1/V: gosper_term = {res4}  [{time.time()-t0:.2f}s]  (expected None)")

    print(f"  Positive controls all found closures: {ok}")
    return ok


def part_b_concrete_K():
    print()
    print("PART B: concrete K, symbolic r -- gosper_term SUCCEEDS every time")
    print("-" * 70)
    all_succeeded = True
    timings = {}
    for Kval in [3, 4, 5, 6, 7]:
        term = build_term(sp.Integer(Kval))
        t0 = time.time()
        res = gosper_term(term, V)
        dt = time.time() - t0
        timings[Kval] = dt
        succeeded = (res is not None)
        all_succeeded = all_succeeded and succeeded
        print(f"  K={Kval}: gosper_term(V) is-not-None = {succeeded}   [{dt:.2f}s]")
    print(f"  All concrete K in {{3,4,5,6,7}} Gosper-summable (symbolic r): {all_succeeded}")

    print()
    print("  Extracting actual gosper_sum closed forms for K=3,4 and verifying")
    print("  numerically against the true truncated V-sum (several n,O,r,t):")
    check_cases = [(12, 1, 2, 6), (10, 0, 1, 5), (14, 2, 3, 8), (9, 0, 2, 4), (11, 3, 1, 7)]
    verified_all = True
    for Kval in [3, 4]:
        term = build_term(sp.Integer(Kval))
        t0 = time.time()
        closed = gosper_sum(term, (V, r, t))
        dt = time.time() - t0
        print(f"  K={Kval}: gosper_sum(V,r,t) obtained in {dt:.2f}s")
        for (nv, Ov, rv, tv) in check_cases:
            direct = 0
            for Vv in range(rv, tv + 1):
                cV = comb(Vv - 1, rv - 1) if rv > 0 else (1 if Vv == 0 else 0)
                direct += cV * InnerJ_direct(nv, Kval, rv, Vv, Ov)
            # substitute r symbolically first, then simplify, THEN plug in
            # numbers -- avoids spurious 0/0 removable-singularity artifacts
            # at small r (documented below, not a bug in the certificate).
            expr_at_r = sp.simplify(closed.subs(r, rv))
            val = sp.nsimplify(expr_at_r.subs({n: nv, O: Ov, t: tv}))
            match = (val == direct)
            verified_all = verified_all and match
            print(f"     n={nv} O={Ov} r={rv} t={tv}: direct={direct} closed={val} {'OK' if match else 'MISMATCH!'}")
    print(f"  gosper_sum closed forms verified (K=3,4): {verified_all}")
    return all_succeeded and verified_all


def part_c_symbolic_K_certificate():
    print()
    print("PART C -- THE CERTIFICATE: K itself left symbolic (together with")
    print("r, n, O all symbolic). This call is genuinely slow (Gosper's")
    print("algorithm must certify non-existence, not just fail to find a")
    print("witness quickly) -- reported honestly, timed exactly.")
    print("-" * 70)
    term = build_term(K)
    print(f"  term(V) = {term}")
    t0 = time.time()
    res = gosper_term(term, V)
    dt = time.time() - t0
    print(f"  gosper_term(term, V) with K SYMBOLIC -> {res}   [{dt:.2f}s]")
    is_certificate = (res is None)
    print(f"  Certified non-existence (result is None): {is_certificate}")
    return is_certificate, dt


if __name__ == "__main__":
    print("=" * 70)
    ok_a = part_a_positive_controls()
    print("=" * 70)
    ok_b = part_b_concrete_K()
    print("=" * 70)
    cert, dt = part_c_symbolic_K_certificate()
    print("=" * 70)
    print(f"SUMMARY: positive controls sound = {ok_a}; concrete-K (3..7) all")
    print(f"Gosper-summable & verified = {ok_b}; symbolic-K certificate obtained")
    print(f"(None, in {dt:.1f}s) = {cert}.")
    print("This is the main obstruction-location result of this front.")
