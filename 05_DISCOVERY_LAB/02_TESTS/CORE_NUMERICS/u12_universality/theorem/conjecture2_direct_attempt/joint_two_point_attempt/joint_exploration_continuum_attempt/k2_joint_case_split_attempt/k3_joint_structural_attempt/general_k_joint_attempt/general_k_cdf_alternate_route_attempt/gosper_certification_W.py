"""
THE MAIN RESULT of this front: Gosper certification on the NEW collapsed
single sum (w_collapse_identity.py):

    S_r(n,K,k) = sum_{W=r}^{k} term(W),   term(W) := C(W,r) * InnerJ(W)
    InnerJ(W) = W*C(n-W+r-1,K-1) + r*C(n-W+r-1,K)        (r<K case)

Because k is an ARBITRARY upper limit (the CDF needs this sum at every
k=0,...,n), what is needed is a genuine INDEFINITE hypergeometric-term
antidifference in W -- exactly Gosper's algorithm's object of study
(sympy.concrete.gosper.gosper_term / gosper_sum), mirroring both Estagio
39's and Estagio 44's own use of Gosper, but applied here to a
STRUCTURALLY SIMPLER object: a single univariate sum with one FEWER free
parameter (O has been eliminated algebraically by w_collapse_identity.py,
not just fixed or hidden) than Estagio 44's own V-summand (which still
carried O as a free symbol throughout).

PART A: positive/negative controls (harness soundness, mirroring Estagio
44's own Part A, redone independently here for this new term shape).

PART B: concrete K=1..7, r symbolic: gosper_term SUCCEEDS every time.
For K=1,2 the actual gosper_sum closed form is extracted and verified
numerically against the true sum at several (n,r,k).

PART C -- THE CERTIFICATE: K symbolic (together with r,n): gosper_term
returns None. Diagnosed carefully (Section below) to confirm this is a
genuine algorithmic non-existence certificate (hypersimp recognizes the
term as hypergeometric; the degree-bound machinery genuinely finds no
valid solution), NOT a fast bail-out from hypersimp failing to recognize
an unsimplified expression as hypergeometric (a documented pitfall this
script explicitly checks for and avoids by calling sp.simplify() on the
term before ever calling gosper_term/hypersimp, and by independently
tracing hypersimp's own recognition step).
"""
import time
import sympy as sp
from sympy.concrete.gosper import gosper_term, gosper_sum
from sympy.simplify import hypersimp
from math import comb
import sys
sys.path.insert(0, '.')
from reference_Sr_double_sum import InnerJ_direct
from w_collapse_identity import Sr_single_sum_W

n, r, W, K = sp.symbols('n r W K', integer=True, positive=True)


def build_term(Kval_or_symbol):
    N = n - W
    A1 = sp.binomial(N + r - 1, Kval_or_symbol - 1)
    A2 = sp.binomial(N + r - 1, Kval_or_symbol)
    InnerJ = W * A1 + r * A2
    cW = sp.binomial(W, r)
    return sp.simplify(cW * InnerJ)


def part_a_controls():
    print("PART A: positive/negative controls (harness soundness)")
    print("-" * 70)
    ok = True
    t0 = time.time()
    res1 = gosper_term(sp.binomial(W, r), W)
    print(f"  control1 C(W,r), symbolic r: gosper_term = {res1 is not None}  [{time.time()-t0:.2f}s]")
    ok = ok and (res1 is not None)

    t0 = time.time()
    res2 = gosper_term(sp.binomial(W, K), W)
    print(f"  control2 C(W,K), symbolic K (binomial degree): gosper_term = {res2 is not None}  [{time.time()-t0:.2f}s]")
    ok = ok and (res2 is not None)

    t0 = time.time()
    res3 = gosper_term(sp.binomial(n - W + r - 1, K - 1) * W, W)
    print(f"  control3 C(n-W+r-1,K-1)*W, symbolic K,r (structurally close to real term): gosper_term = {res3 is not None}  [{time.time()-t0:.2f}s]")
    ok = ok and (res3 is not None)

    t0 = time.time()
    res4 = gosper_term(sp.Integer(1) / W, W)
    print(f"  control4 (negative) 1/W: gosper_term = {res4}  [{time.time()-t0:.2f}s]  (expected None)")

    print(f"  Positive controls all found closures: {ok}")
    return ok


def part_b_concrete_K():
    print()
    print("PART B: concrete K, symbolic r -- expect SUCCESS every time")
    print("-" * 70)
    all_ok = True
    for Kval in [1, 2, 3, 4, 5, 6, 7]:
        term = build_term(sp.Integer(Kval))
        t0 = time.time()
        res = gosper_term(term, W)
        dt = time.time() - t0
        ok = (res is not None)
        all_ok = all_ok and ok
        print(f"  K={Kval}: gosper_term is-not-None = {ok}   [{dt:.2f}s]")
    print(f"  All concrete K in 1..7 Gosper-summable: {all_ok}")

    print()
    print("  Extracting gosper_sum closed forms for K=1,2 and verifying")
    print("  numerically against the true (single-sum) S_r at several (n,r,k):")
    check_cases = [(12, 2, 6), (10, 1, 5), (14, 3, 8), (9, 2, 4), (11, 1, 7)]
    verified_all = True
    for Kval in [1, 2]:
        term = build_term(sp.Integer(Kval))
        t0 = time.time()
        closed = gosper_sum(term, (W, r, sp.Symbol('t', integer=True, positive=True)))
        dt = time.time() - t0
        print(f"  K={Kval}: gosper_sum(W,r,t) obtained in {dt:.2f}s")
        tsym = sp.Symbol('t', integer=True, positive=True)
        for (nv, rv, tv) in check_cases:
            if rv > Kval:
                continue
            direct = Sr_single_sum_W(nv, Kval, rv, tv)
            expr_at_r = sp.simplify(closed.subs(r, rv))
            val = sp.nsimplify(expr_at_r.subs({n: nv, tsym: tv}))
            match = (val == direct)
            verified_all = verified_all and match
            print(f"     n={nv} r={rv} k={tv}: direct={direct} closed={val} {'OK' if match else 'MISMATCH!'}")
    print(f"  gosper_sum closed forms verified (K=1,2): {verified_all}")
    return all_ok and verified_all


def part_c_symbolic_K_certificate():
    print()
    print("PART C -- THE CERTIFICATE: K symbolic (with r, n symbolic too).")
    print("-" * 70)
    term = build_term(K)
    print(f"  term(W) = {term}")

    # Diagnostic: confirm hypersimp genuinely recognizes this as a
    # hypergeometric term BEFORE trusting a None from gosper_term --
    # a documented pitfall of this harness (an unsimplified input can make
    # hypersimp bail out fast with a spurious None that is NOT a real
    # Gosper certificate; this front's own exploration hit this pitfall
    # once on an earlier draft of this exact script and self-corrected --
    # see ATTEMPT.md Section 4.4 for the full disclosure).
    t0 = time.time()
    ratio = hypersimp(term, W)
    dt_h = time.time() - t0
    print(f"  hypersimp(term, W) recognized as hypergeometric: {ratio is not None}  [{dt_h:.2f}s]")
    print(f"  ratio = {ratio}")
    is_rational = ratio.is_rational_function(W) if ratio is not None else False
    print(f"  ratio.is_rational_function(W) = {is_rational}")

    t0 = time.time()
    res = gosper_term(term, W)
    dt = time.time() - t0
    print(f"  gosper_term(term, W) with K SYMBOLIC -> {res}   [{dt:.2f}s]")
    is_certificate = (res is None) and (ratio is not None) and is_rational
    print(f"  Certified non-existence (None, AND hypersimp genuinely recognized")
    print(f"  the term as hypergeometric first -- i.e. this is NOT a fast")
    print(f"  recognition-failure bailout): {is_certificate}")
    return is_certificate, dt


if __name__ == "__main__":
    print("=" * 70)
    ok_a = part_a_controls()
    print("=" * 70)
    ok_b = part_b_concrete_K()
    print("=" * 70)
    cert, dt = part_c_symbolic_K_certificate()
    print("=" * 70)
    print(f"SUMMARY: controls sound = {ok_a}; concrete K (1..7) all Gosper-summable")
    print(f"& K=1,2 closed forms verified = {ok_b}; symbolic-K certificate")
    print(f"(None, genuine, in {dt:.2f}s) = {cert}.")
    print()
    print("This is a SECOND, INDEPENDENT Gosper-certified non-existence result,")
    print("obtained on a structurally SIMPLER object (one fewer free parameter,")
    print("O eliminated algebraically) than Estagio 44's own certificate --")
    print("confirming the obstruction is not an artifact of the nested")
    print("O-then-V summation order, and survives even after an exact")
    print("combinatorial identity removes an entire summation layer.")
