"""
ADVERSARIAL / REFEREE SCRIPT 3 (item 3): independently reproduce the
target's self-disclosed Gosper-differencing discrepancy (ATTEMPT.md
Section 5.4), written completely fresh (different variable-construction
order, different helper structure) to rule out a shared-bug/copy-paste
explanation for the "0 vs None vs None" mismatch.

Also independently reproduces the mandate's literal Step-2 probe
(sympy.summation / gosper_sum on S(K,t) itself, symbolic K) to confirm
the even/odd-t split reported in Section 5.1.
"""
import sympy as sp
from sympy.concrete.gosper import gosper_sum

Ksym, rsym, tsym = sp.symbols('K r t')


def summand(Kv, rv, tv):
    """C(K,r) * W(r,t) / (K+t+r+1)!, W(r,t)=(t+2r+1)(t+r)! -- built via
    sp.binomial, independent expression order from the target's a_binom."""
    W = (tv + 2 * rv + 1) * sp.factorial(tv + rv)
    C = sp.binomial(Kv, rv)
    return W * C / sp.factorial(Kv + tv + rv + 1)


def summand_factorial_form(Kv, rv, tv):
    """Same quantity, binomial written as an explicit factorial ratio."""
    C = sp.factorial(Kv) / (sp.factorial(rv) * sp.factorial(Kv - rv))
    W = (tv + 2 * rv + 1) * sp.factorial(tv + rv)
    return C * W / sp.factorial(Kv + tv + rv + 1)


print("=" * 78)
print("Reproduction A: mandate's literal Step 2 (gosper_sum on S(K,t) summand,")
print("symbolic K), independently, for t=1..8 and symbolic t")
print("=" * 78)
for tv in range(1, 9):
    g = gosper_sum(summand(Ksym, rsym, tv), (rsym, 0, Ksym))
    parity = "even" if tv % 2 == 0 else "odd"
    print(f"  t={tv} ({parity}): gosper_sum = {sp.simplify(g) if g is not None else None}")
g_symbolic = gosper_sum(summand(Ksym, rsym, tsym), (rsym, 0, Ksym))
print(f"  t symbolic: gosper_sum = {g_symbolic}")
print()

print("=" * 78)
print("Reproduction B: the self-caught Gosper-differencing discrepancy,")
print("independently coded (fresh variable order / helper functions),")
print("testing three syntactically different but mathematically IDENTICAL")
print("formulations of h(r) := (t+2K)*a(K,r,t) - 2*a(K-1,r,t)")
print("=" * 78)

# Form 1: binomial objects, no pre-simplification
h1 = (tsym + 2 * Ksym) * summand(Ksym, rsym, tsym) - 2 * summand(Ksym - 1, rsym, tsym)
g1 = gosper_sum(h1, (rsym, 0, Ksym))
print(f"Form 1 (sp.binomial, raw, NOT simplified first):        gosper_sum = {g1}")

# Form 2: same expression, sp.simplify() applied first
h2 = sp.simplify(h1)
g2 = gosper_sum(h2, (rsym, 0, Ksym))
print(f"Form 2 (sp.binomial, sp.simplify() applied first):      gosper_sum = {g2}")

# Form 3: explicit factorial-ratio binomial, sp.together() applied
h3 = sp.together((tsym + 2 * Ksym) * summand_factorial_form(Ksym, rsym, tsym)
                  - 2 * summand_factorial_form(Ksym - 1, rsym, tsym))
g3 = gosper_sum(h3, (rsym, 0, Ksym))
print(f"Form 3 (explicit factorial ratios, sp.together()):      gosper_sum = {g3}")

# Form 4 (extra, not in target's script): sp.expand() instead of simplify()
h4 = sp.expand(h1)
g4 = gosper_sum(h4, (rsym, 0, Ksym))
print(f"Form 4 (sp.binomial, sp.expand() applied first, extra): gosper_sum = {g4}")

print()
results = {"Form1_raw": g1, "Form2_simplify": g2, "Form3_factorial": g3, "Form4_expand": g4}
distinct = set(str(v) for v in results.values())
print(f"Distinct results across the 4 forms: {distinct}")
if g2 == 0 and g1 is None and g3 is None:
    print()
    print("DISCREPANCY INDEPENDENTLY CONFIRMED: sp.simplify()-then-gosper_sum")
    print("(Form 2) returns 0 while the mathematically identical raw form")
    print("(Form 1) and the explicit-factorial form (Form 3) both return None.")
    print("This exactly reproduces the target's self-disclosed finding")
    print("(ATTEMPT.md Section 5.4 / symbolic_K_sum_attempt.log 'Part 3'),")
    print("via completely independently-written code -- confirming this is a")
    print("genuine sympy/Gosper subtlety (simplify() changes the syntactic form")
    print("fed to gosper_sum enough to flip its verdict at this specific")
    print("removable-singularity boundary term), not a mischaracterization or")
    print("a copy-paste artifact.")
else:
    print()
    print("NOTE: exact pattern not reproduced identically in this sympy version")
    print(f"(g1={g1}, g2={g2}, g3={g3}, g4={g4}) -- see values above for what")
    print("actually happened in this environment's sympy install.")

print()
print("=" * 78)
print("Reproduction C: does the SPURIOUS '0' from Form 2 propagate into any")
print("actual usage anywhere else? Sanity check: verify the (t+2K)S(K,t)=")
print("2S(K-1,t) recursion this Gosper-differencing attempt was TRYING to")
print("prove, by DIRECT symbolic substitution of the known-correct closed")
print("forms (NOT via Gosper at all) -- confirms the recursion itself is")
print("true (as it must be, since S(K,t)=Gamma(t/2+1)/Gamma(K+t/2+1) really")
print("does satisfy it), independent of whether Gosper can certify it.")
print("=" * 78)
tv = sp.symbols('t', positive=True)
Kv = sp.symbols('K', positive=True, integer=True)


def S_target(Kv_, tv_):
    return sp.gamma(tv_ / 2 + 1) / sp.gamma(Kv_ + tv_ / 2 + 1)


lhs = (tv + 2 * Kv) * S_target(Kv, tv)
rhs = 2 * S_target(Kv - 1, tv)
diff = sp.simplify(lhs - rhs)
print(f"  (t+2K)*S(K,t) - 2*S(K-1,t), symbolic K,t, via Gamma function directly: {diff}")
print(f"  Recursion holds identically (Gamma-function identity, no Gosper needed): {diff == 0}")
