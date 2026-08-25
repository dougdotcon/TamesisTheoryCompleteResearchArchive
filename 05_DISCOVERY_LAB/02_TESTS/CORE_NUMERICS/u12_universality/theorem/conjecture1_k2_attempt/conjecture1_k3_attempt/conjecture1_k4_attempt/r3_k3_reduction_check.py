"""
R3 -- the K=3 reduction check (this front's own analogue of K=3's own R2,
which reduced ITS method to K=2 and caught a real by-hand miscount in the
process).

Applies THIS document's own general method (Lemma 1 density = r!... i.e.
K!, and the r_on-indexed shape formula f_shape(r,n_off)(x) = K! * C(K,r) *
x^r * Integral W_C(Q) Q^(n_off-1)/(n_off-1)! (1-x-Q)^(r-1)/(r-1)! dQ, with
W_C(Q)=1-Q established by brute-force symbolic enumeration, generalized
here to n_off in {0,1,2} rather than K=4's {0,1,2,3}) with THREE sources
instead of four, and confirms it reproduces the ALREADY-PROVED
`conjecture1_k2_attempt/conjecture1_k3_attempt/ATTEMPT.md` result
`f_{M_3}(x) = 6x(1-x^2)^2`, GROUP BY GROUP (by r_on = 0,1,2,3) against
that document's own T0/T1a/(T1b+T2a)/(T1c+T2b+T3) breakdown, not merely
against the final sum -- exactly mirroring how K=3's own R2 reduction
check was done at the per-group level, which is precisely where that
document caught a real by-hand miscount.

This is a strong sanity check on the derive_step2_k4_symbolic.py machinery
itself (same code pattern, one dimension down, checked against numbers
that are already independently proved and adversarially reviewed) BEFORE
trusting its K=4 output.
"""
import itertools as it

import sympy as sp

x, Q = sp.symbols('x Q', positive=True)
m1, m2, m3 = sp.symbols('m1 m2 m3', positive=True)
M = [m1, m2, m3]
mass_out = 1 - m1 - m2 - m3
KFAC = 6  # 3! -- Lemma 1 density at K=3, already PROVED


def off_cycle_weight(on_labels, off_labels):
    mass = {i: M[i - 1] for i in on_labels + off_labels}
    mass['OUT'] = mass_out
    options_per_node = {
        i: [t for t in (on_labels + off_labels + ['OUT']) if t != i]
        for i in off_labels
    }
    total = sp.Integer(0)
    for combo in it.product(*(options_per_node[i] for i in off_labels)):
        assignment = dict(zip(off_labels, combo))
        has_cycle = False
        for start in off_labels:
            seen = set()
            cur = start
            while True:
                if cur not in assignment:
                    break
                if cur in seen:
                    has_cycle = True
                    break
                seen.add(cur)
                cur = assignment[cur]
            if has_cycle:
                break
        if has_cycle:
            continue
        term = sp.Integer(1)
        for i in off_labels:
            term *= mass[assignment[i]]
        total += term
    return sp.expand(total)


print("=" * 78)
print("R3 -- K=3 reduction check of this document's general K=4 method")
print("=" * 78)

needed = {
    0: ([1, 2, 3], []),
    1: ([1, 2], [3]),
    2: ([1], [2, 3]),
}
for n_off, (on_labels, off_labels) in needed.items():
    if n_off == 0:
        print("n_off=0: W=1 (trivial)")
        continue
    w = off_cycle_weight(on_labels, off_labels)
    off_syms = [M[i - 1] for i in off_labels]
    Qsym = sum(off_syms)
    diff = sp.simplify(sp.expand(w - (1 - Qsym)))
    print(f"n_off={n_off}: W_C = {w}, matches 1-Q: {diff == 0}")
    assert diff == 0


def shape_density_general(r, n_off, K, kfac):
    if n_off == 0:
        f = kfac * x ** r * (1 - x) ** (r - 1) / sp.factorial(r - 1)
        return sp.simplify(f)
    integrand = ((1 - Q) * Q ** (n_off - 1) / sp.factorial(n_off - 1)
                 * (1 - x - Q) ** (r - 1) / sp.factorial(r - 1))
    f = kfac * x ** r * sp.integrate(integrand, (Q, 0, 1 - x))
    return sp.simplify(f)


import math

K = 3
results = {}
for r in (1, 2, 3):
    n_off = K - r
    f_single = shape_density_general(r, n_off, K, KFAC)
    mult = math.comb(K, r)
    f_total = sp.simplify(mult * f_single)
    results[r] = f_total
    print(f"r={r} (n_off={n_off}): C({K},{r})={mult}, f_r={r}_total(x) = {sp.expand(f_total)}")

# r=0 (T0): via complement, brute-force 4^3=64-term sum (same as
# conjecture1_k3_attempt's own derive_step2_k3_symbolic.py already did,
# reproduced here independently from THIS script's own machinery).
def cycles_of3(g):
    found = []
    classified = set()
    for start in [1, 2, 3]:
        if start in classified:
            continue
        path = [start]
        cur = start
        seen_positions = {start: 0}
        while True:
            nxt = g[cur]
            if nxt == 'OUT':
                classified.update(path)
                break
            if nxt in classified:
                classified.update(path)
                break
            if nxt in seen_positions:
                cyc = tuple(path[seen_positions[nxt]:])
                found.append(cyc)
                classified.update(path)
                break
            path.append(nxt)
            seen_positions[nxt] = len(path) - 1
            cur = nxt
    return found


mass = {1: m1, 2: m2, 3: m3, 'OUT': mass_out}
P_T0 = sp.Integer(0)
for cfg in it.product([1, 2, 3, 'OUT'], repeat=3):
    g = {1: cfg[0], 2: cfg[1], 3: cfg[2]}
    if cycles_of3(g) == []:
        P_T0 += mass[cfg[0]] * mass[cfg[1]] * mass[cfg[2]]
P_T0 = sp.expand(P_T0)
print(f"\nP_T0(m1,m2,m3) = {P_T0}")

ell = sp.symbols('ell', positive=True)
a1, a2 = sp.symbols('a1 a2', positive=True)
P_T0_slice = P_T0.subs({m1: a1, m2: a2, m3: ell - a1 - a2})
inner = sp.integrate(P_T0_slice, (a2, 0, ell - a1))
f_L_T0 = KFAC * sp.integrate(inner, (a1, 0, ell))
f_T0 = sp.simplify(f_L_T0.subs(ell, 1 - x))
print(f"f_(r=0)(x) [T0] = {sp.expand(f_T0)}")
results[0] = f_T0

print("\n--- Comparison against conjecture1_k3_attempt/ATTEMPT.md's own"
      " (already-PROVED, adversarially reviewed) per-shape densities ---")
# HONEST PROCESS NOTE (a real bug, caught and fixed, not silently patched):
# the FIRST version of this comparison built `established[0]` via
# `sp.sympify("3*x**3 - 6*x**2 + 3*x")` (a string literal). sympify()
# parses a fresh `Symbol('x')` from the string -- WITHOUT this script's own
# `positive=True` assumption on `x` -- so the resulting expression's `x` is
# a genuinely DIFFERENT sympy symbol from the `x` used everywhere else in
# this script, despite printing identically. `results[0] - established[0]`
# then could never cancel (sympy correctly refuses to equate two distinct
# symbols of the same name/different assumptions), producing a persistent
# false "MISMATCH" that neither sp.simplify() nor sp.expand() resolves --
# both operate correctly on what is, to sympy, genuinely a difference of
# two different variables. Diagnosed via sp.srepr() (showing two distinct
# Symbol('x',...) objects) after the naive fixes did not help. Fixed by
# building every `established[r]` entry as a direct sympy expression using
# THIS script's own `x` symbol (no sympify-from-string anywhere).
established = {
    0: sp.expand(3 * x ** 3 - 6 * x ** 2 + 3 * x),  # f_T0
    1: sp.expand(3 * x * (x - 1) ** 2 * (2 * x + 1)),  # f_T1a
    2: sp.expand(2 * sp.Rational(3, 2) * x ** 2 * (x - 1) ** 2 * (x + 2)),  # f_T1b + f_T2a
    3: sp.expand(x ** 3 * (x - 1) ** 2 + sp.Rational(3, 2) * x ** 3 * (x - 1) ** 2
                  + sp.Rational(1, 2) * x ** 3 * (x - 1) ** 2),  # f_T1c + f_T2b + f_T3
}
all_match = True
for r in range(4):
    diff = sp.expand(results[r] - established[r])
    match = (diff == 0)
    all_match = all_match and match
    print(f"  r={r}: this-document's-method = {sp.expand(results[r])}")
    print(f"        established (K=3 ATTEMPT.md) = {sp.expand(established[r])}")
    print(f"        diff = {diff}  ({'MATCH' if match else 'MISMATCH'})")

total = sp.simplify(sp.expand(sum(results[r] for r in range(4))))
target = sp.expand(6 * x * (1 - x ** 2) ** 2)
print(f"\nSum via this document's method = {sp.expand(total)}")
print(f"Target 6x(1-x^2)^2 = {target}")
diff_total = sp.expand(total - target)
print(f"diff = {diff_total}")

print("\n" + "=" * 78)
if all_match and diff_total == 0:
    print("*** R3 PASSES: this document's own general K-parametrized method, "
          "applied at K=3, reproduces conjecture1_k3_attempt/ATTEMPT.md's "
          "already-PROVED per-shape densities EXACTLY, group by group, and "
          "the total exactly. Strong validation of the K=4 machinery before "
          "trusting its own (new) K=4 output. ***")
else:
    print("*** R3 FAILS -- see mismatches above. This document's K=4 claim "
          "should NOT be trusted until this is resolved. ***")
