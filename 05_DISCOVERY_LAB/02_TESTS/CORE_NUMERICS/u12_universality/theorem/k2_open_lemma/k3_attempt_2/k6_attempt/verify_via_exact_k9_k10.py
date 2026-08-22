"""
ATTEMPT.md Sec.3.4: the fully UNCONDITIONAL confirmation of the rate conjecture at the
two highest K values reached by the mechanical extension (Sec.1) -- K=9,10. These
closed forms come entirely from ../markov_transfer.py's exact telescoping-sum method
(extend_frontier.py), independent of the whole continuum-ODE derivation of Sec.2-3;
comparing their own 1/n Taylor coefficient to K*phi_K/4 needs no asymptotic argument
at all, since the closed form itself is exact and finite.
"""
import sympy as sp

n = sp.symbols('n', positive=True)

psi9 = (262144*n**9 + 589824*n**8 + 1371549*n**7 + 2759301*n**6 + 4562055*n**5 + 5967729*n**4 + 5900344*n**3 + 4116636*n**2 + 1792656*n + 362880)/(923780*n**9)
psi10 = (524288*n**10 + 1310720*n**9 + 3462425*n**8 + 8082170*n**7 + 15900584*n**6 + 25576250*n**5 + 32554945*n**4 + 31376020*n**3 + 21389436*n**2 + 9124560*n + 1814400)/(1939938*n**10)


def phiK(K):
    return sp.Rational(4**K * sp.factorial(K)**2, sp.factorial(2*K + 1))


for K, psi in [(9, psi9), (10, psi10)]:
    lim = sp.limit(psi, n, sp.oo)
    rate = sp.limit((psi - lim) * n, n, sp.oo)
    predicted = sp.Rational(K, 4) * phiK(K)
    print(f"K={K}: limit={lim} (phi_{K}={phiK(K)}, match={lim==phiK(K)})")
    print(f"       1/n coeff={rate}  K*phi_K/4={predicted}  match={rate==predicted}")
