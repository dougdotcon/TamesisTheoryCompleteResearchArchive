"""
K5-EXACT-CLOSURE-ATTEMPT, bonus verification.

Runs the fresh, fully exhaustive Definition-4 brute-force engine
(bruteforce_definition4_k5.py) at n=8 -- 1,321,205,760 configurations,
the 5th and largest exhaustive data point -- and cross-checks every k
against Proposicao D5. This completes the "n=8 attempted, not completed
in time" honest disclosure of the main ATTEMPT.md/6.2: the background
run finished (2044.3s, ~34.1 minutes) after this front's main report was
already written, and is folded in here as a genuine bonus confirmation
rather than silently left out now that it is available.
"""
import sympy as sp
from fractions import Fraction
from bruteforce_definition4_k5 import exact_T_distribution
import time

n, k = sp.symbols('n k')
bracket_str = '''
k**8 - 16*k**7 - 5*k**6*n**2 + 30*k**6*n + 106*k**6 + 45*k**5*n**2 - 290*k**5*n - 376*k**5
+ 10*k**4*n**4 - 100*k**4*n**3 + 100*k**4*n**2 + 1100*k**4*n + 769*k**4
- 40*k**3*n**4 + 440*k**3*n**3 - 975*k**3*n**2 - 2074*k**3*n - 904*k**3
- 10*k**2*n**6 + 120*k**2*n**5 - 435*k**2*n**4 + 10*k**2*n**3 + 1885*k**2*n**2 + 2014*k**2*n + 564*k**2
+ 10*k*n**6 - 140*k*n**5 + 635*k*n**4 - 650*k*n**3 - 1410*k*n**2 - 924*k*n - 144*k
+ 5*n**8 - 60*n**7 + 265*n**6 - 490*n**5 + 190*n**4 + 300*n**3 + 360*n**2 + 144*n
'''
bracket = sp.sympify(bracket_str, locals={'n': n, 'k': k})
Dn5 = n**6 * (n - 1) * (n - 2) * (n - 3) * (n - 4)
D5 = k * (k + 1) * bracket / Dn5

if __name__ == "__main__":
    t0 = time.time()
    counts, total = exact_T_distribution(8, 5)
    elapsed = time.time() - t0
    print(f"n=8, K=5: total configs = {total}, elapsed = {elapsed:.1f}s")
    assert total == 1321205760
    cum = 0
    all_ok = True
    for kv in range(0, 8):
        cum += counts[kv]
        bf_val = Fraction(cum, total)
        formula_val = sp.Rational(D5.subs({n: 8, k: kv}))
        formula_frac = Fraction(int(formula_val.p), int(formula_val.q))
        ok = (bf_val == formula_frac)
        all_ok = all_ok and ok
        print(f"  k={kv}: brute={bf_val} formula={formula_frac} MATCH={ok}")
    print("ALL MATCH:", all_ok)
    assert all_ok
    print("PASSED: n=8 exhaustive brute force (1,321,205,760 configurations)")
    print("matches Proposicao D5 exactly at every k.")
