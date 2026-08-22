"""
Route (i) exploration: extract the FULL two-variable closed forms g_r(m,b), h_r(a,b)
(both m/a and b symbolic, not just specialized at b=0 or a=0) for r=0..5, and examine
their algebraic structure (numerator/denominator degree in m, dependence on b) looking
for a pattern as a function of r.
"""
import sys, time
sys.path.insert(0, '/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/theorem/k2_open_lemma/k3_attempt_2')
import sympy as sp
import markov_transfer as mt

n = mt.n
b = mt.b
m = mt.m
a_sym = mt.a_sym

MAXR = int(sys.argv[1]) if len(sys.argv) > 1 else 5

levels = {}

def h0_func(a_expr, b_expr=b):
    return mt.h_closed_from_g(0, a_expr, b_expr, mt.g0_func, None)

levels[0] = (mt.g0_func, h0_func)
h_prev = h0_func

g_full = {0: mt.g0_func(m, b)}
h_full = {0: sp.simplify(h0_func(a_sym, b))}

for r in range(1, MAXR + 1):
    t0 = time.time()
    g_r, g_of_m_symbolic = mt.g_closed_via_telescoping(r, h_prev)  # b kept symbolic by default
    g_full[r] = sp.simplify(g_of_m_symbolic)  # function of m, b, n
    def make_h(r_=r, g_r_=g_r, h_prev_=h_prev):
        def h_r_func(a_expr, b_expr=b):
            return mt.h_closed_from_g(r_, a_expr, b_expr, g_r_, h_prev_)
        return h_r_func
    h_r = make_h()
    levels[r] = (g_r, h_r)
    h_full[r] = sp.simplify(h_r(a_sym, b))
    h_prev = h_r
    print(f"--- r={r} done in {time.time()-t0:.2f}s ---", flush=True)

print("\n\n===== FULL SYMBOLIC (m,b) FORMS =====\n")
for r in sorted(g_full):
    print(f"g_{r}(m,b) =", g_full[r])
    num, den = sp.fraction(sp.together(g_full[r]))
    print(f"   numerator degree in m: {sp.degree(sp.Poly(num, m)) if num.has(m) else 0}")
    print(f"   denominator degree in m: {sp.degree(sp.Poly(den, m)) if den.has(m) else 0}")
    print(f"   denominator factored: {sp.factor(den)}")
    print()

print()
for r in sorted(h_full):
    print(f"h_{r}(a,b) =", h_full[r])
    num, den = sp.fraction(sp.together(h_full[r]))
    print(f"   denominator factored: {sp.factor(den)}")
    print()

import pickle
with open('/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/theorem/k2_open_lemma/k3_attempt_2/k6_attempt/pattern_data.pkl', 'wb') as f:
    pickle.dump({'g_full': g_full, 'h_full': h_full}, f)

print("DONE")
