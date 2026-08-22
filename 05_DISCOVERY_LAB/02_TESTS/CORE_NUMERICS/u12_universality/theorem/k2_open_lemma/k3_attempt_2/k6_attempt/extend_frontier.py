"""
Extend the K-uniform mechanical ladder (markov_transfer.py's build_levels) as far as
tractable, recording psi_n^{(K)}, psi_n^{(K),R}, phi_n^{(K)} and per-level timing along
the way. Reuses the SAME incremental climb (no re-derivation from scratch per K).
"""
import sys, time
sys.path.insert(0, '/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/theorem/k2_open_lemma/k3_attempt_2')
import sympy as sp
import markov_transfer as mt

n = mt.n
b = mt.b

MAXR = int(sys.argv[1]) if len(sys.argv) > 1 else 9

levels = {}
g_prev = mt.g0_func

def h0_func(a_expr, b_expr=b):
    return mt.h_closed_from_g(0, a_expr, b_expr, mt.g0_func, None)

levels[0] = (mt.g0_func, h0_func)
h_prev = h0_func

results = {}

t_start = time.time()
# record K=0
psi0 = sp.simplify(levels[0][0](n, 0))
results[0] = {'psi': psi0, 't_cum': time.time()-t_start}
print(f"K=0: psi={psi0}  t_cum={results[0]['t_cum']:.2f}s", flush=True)

for r in range(1, MAXR + 1):
    t0 = time.time()
    g_r, g_of_m_symbolic = mt.g_closed_via_telescoping(r, h_prev)
    def make_h(r_=r, g_r_=g_r, h_prev_=h_prev):
        def h_r_func(a_expr, b_expr=b):
            return mt.h_closed_from_g(r_, a_expr, b_expr, g_r_, h_prev_)
        return h_r_func
    h_r = make_h()
    levels[r] = (g_r, h_r)
    h_prev = h_r
    dt = time.time() - t0
    psi_r = sp.simplify(g_r(n, 0))
    t_cum = time.time() - t_start
    results[r] = {'psi': psi_r, 't_level': dt, 't_cum': t_cum, 'g_of_m_b_symbolic': g_of_m_symbolic}
    print(f"K={r}: psi_n^({r}) = {psi_r}", flush=True)
    print(f"       level_time={dt:.2f}s  cum_time={t_cum:.2f}s", flush=True)

import pickle
with open('/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/theorem/k2_open_lemma/k3_attempt_2/k6_attempt/levels_data.pkl', 'wb') as f:
    # can't pickle closures; store only the psi results and symbolic g_of_m (sympy exprs are picklable)
    save = {r: {'psi': v['psi'], 'g_of_m_b_symbolic': v.get('g_of_m_b_symbolic')} for r, v in results.items()}
    pickle.dump(save, f)

print("DONE. Total time:", time.time()-t_start)
