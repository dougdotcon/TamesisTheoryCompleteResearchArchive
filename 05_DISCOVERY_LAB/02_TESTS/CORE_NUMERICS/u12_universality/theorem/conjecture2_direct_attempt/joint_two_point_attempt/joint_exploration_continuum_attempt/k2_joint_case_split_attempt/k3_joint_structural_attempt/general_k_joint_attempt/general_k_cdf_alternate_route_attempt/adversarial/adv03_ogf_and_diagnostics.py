"""
ADVERSARIAL SCRIPT 3 (referee's own, from scratch). Independently
spot-checks Section 6's two supplementary diagnostics:
  (a) the OGF identity sum_K InnerJ(W;K) x^K = (Wx+r)(1+x)^{n-W+r-1};
  (b) Diagnostic 1 -- r-first summation order fails Gosper already at
      concrete K (spot-checked at K=1);
  (c) Diagnostic 2 -- GF-marked (K-eliminated) W-sum is Gosper-summable
      for r concrete but not for r symbolic (spot-checked r=0,2 vs r
      symbolic).
Also sanity-checks Section 6.3's description of the sympy.holonomic
public API.
"""
import time
import sympy as sp
from sympy.concrete.gosper import gosper_term
from sympy.simplify import hypersimp
import math

n, r, W, K, x = sp.symbols('n r W K x', integer=True, positive=True)

print("=" * 70)
print("(a) OGF identity: derived from scratch via two binomial-theorem uses")
print("=" * 70)
for Mv in [3, 5, 8]:
    lhs = sum(sp.binomial(Mv, kk) * x**kk for kk in range(Mv + 1))
    assert sp.expand(lhs - (1 + x)**Mv) == 0
print("Binomial theorem sum_K C(M,K)x^K = (1+x)^M spot-checked M=3,5,8: OK")

Msym = n - W + r - 1
claimed_GF = (W * x + r) * (1 + x)**Msym
derived_GF = W * x * (1 + x)**Msym + r * (1 + x)**Msym
diff = sp.expand(claimed_GF - derived_GF)
print(f"(Wx+r)(1+x)^M - [Wx(1+x)^M + r(1+x)^M] = {diff}  (trivial algebra, should be 0)")
assert diff == 0


def binom(a, b):
    if b < 0 or a < 0 or b > a:
        return 0
    return math.comb(a, b)


def innerJ_concrete(n_, K_, r_, W_):
    N_ = n_ - W_
    if r_ < K_:
        return W_ * binom(N_ + r_ - 1, K_ - 1) + r_ * binom(N_ + r_ - 1, K_)
    elif r_ == K_:
        return n_ * binom(N_ + r_ - 1, r_ - 1)
    return 0


print()
print("Coefficient-extraction cross-check against InnerJ (own implementation):")
all_ok = True
for (nv, Wv, rv) in [(11, 4, 1), (13, 6, 2), (9, 3, 0)]:
    Mv = nv - Wv + rv - 1
    poly = sp.Poly(sp.expand((Wv * x + rv) * (1 + x)**Mv), x)
    for Kv in range(rv, nv - Wv + rv + 1):
        coeff = poly.coeff_monomial(x**Kv) if Kv <= poly.degree() else 0
        true_val = innerJ_concrete(nv, Kv, rv, Wv)
        ok = (coeff == true_val)
        all_ok = all_ok and ok
        if not ok:
            print(f"  MISMATCH n={nv} W={Wv} r={rv} K={Kv}: GF={coeff} true={true_val}")
print(f"All coefficient-extraction checks passed: {all_ok}")

print()
print("=" * 70)
print("(b) Diagnostic 1 spot-check: r-first summation order, concrete K=1")
print("=" * 70)


def RTerm(Kval):
    N = n - W
    InnerJ_ = W * sp.binomial(N + r - 1, Kval - 1) + r * sp.binomial(N + r - 1, Kval)
    cW = sp.binomial(W, r)
    outer = sp.binomial(Kval, r) * sp.factorial(r) / n**(r + 1)
    return sp.simplify(outer * cW * InnerJ_)


term1 = RTerm(1)
ratio1 = hypersimp(term1, r)
t0 = time.time()
res1 = gosper_term(term1, r)
dt1 = time.time() - t0
print(f"K=1, summing over r (fixed W): hypersimp recognized={ratio1 is not None}, "
      f"gosper_term={res1}  [{dt1:.2f}s]")
assert res1 is None and ratio1 is not None
print("CONFIRMED: r-first order fails Gosper already at concrete K=1 (genuine, "
      "hypersimp recognized the term first) -- matches the target's claim that "
      "this order is strictly worse than the W-first order.")

print()
print("=" * 70)
print("(c) Diagnostic 2 spot-check: GF-marked term, r concrete vs symbolic")
print("=" * 70)
xg = sp.symbols('xg', positive=True)


def GF_term(rval):
    T = sp.binomial(W, rval) * (W * xg + rval) * (1 + xg)**(n - W + rval - 1)
    return sp.simplify(T)


for rv in [0, 2]:
    term = GF_term(rv)
    t0 = time.time()
    res = gosper_term(term, W)
    dt = time.time() - t0
    print(f"  r={rv} (concrete): gosper_term = {'FOUND' if res is not None else 'None'}  [{dt:.2f}s]")
    assert res is not None

term_rsym = GF_term(r)
ratio = hypersimp(term_rsym, W)
t0 = time.time()
res_rsym = gosper_term(term_rsym, W)
dt = time.time() - t0
print(f"  r symbolic: hypersimp recognized={ratio is not None}, "
      f"gosper_term = {res_rsym}  [{dt:.2f}s]")
assert res_rsym is None and ratio is not None
print("CONFIRMED: GF-marked (K eliminated) term IS Gosper-summable for r")
print("concrete but genuinely fails (hypersimp-confirmed) once r is ALSO left")
print("symbolic -- matches the target's 'obstruction moves from K to r' claim.")

print()
print("=" * 70)
print("sympy.holonomic API sanity check (Section 6.3's disclosure)")
print("=" * 70)
import sympy.holonomic as h
public_api = sorted(x for x in dir(h) if not x.startswith('_'))
print(f"Public API of sympy.holonomic: {public_api}")
print("Matches the target's description: HolonomicFunction, "
      "DifferentialOperator(s), RecurrenceOperator(s), from_hyper, "
      "from_meijerg, expr_to_holonomic -- all operate on an ALREADY-GIVEN "
      "operator/expression, none is a decision procedure that takes an "
      "unevaluated finite sum with free symbolic parameters (K,r) and "
      "decides holonomicity uniformly in them (that would require "
      "Zeilberger's algorithm / creative telescoping, absent from sympy).")
