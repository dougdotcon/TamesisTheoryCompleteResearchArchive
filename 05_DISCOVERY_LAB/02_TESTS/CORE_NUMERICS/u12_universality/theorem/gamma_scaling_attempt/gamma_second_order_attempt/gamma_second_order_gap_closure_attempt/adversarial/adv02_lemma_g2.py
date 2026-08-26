"""
Adversarial re-derivation B: Lemma G2 (Sum k^2 e^{-a k^2}) via differentiation
of the Poisson-summation identity, cross-checked numerically at high precision.
Written fresh; no .py file of this lineage was read.
"""
import mpmath as mp

mp.mp.dps = 50

def direct_inf_sum_k2(a, kmax=None):
    a = mp.mpf(a)
    if kmax is None:
        # choose kmax so that a*kmax^2 >> dps*log(10), tail negligible
        kmax = int(mp.sqrt(mp.mpf(mp.mp.dps) * mp.log(10) * 3 / a)) + 50
    s = mp.mpf(0)
    for k in range(1, kmax + 1):
        term = k**2 * mp.e**(-a * k**2)
        s += term
        if term < mp.mpf(10)**(-(mp.mp.dps + 10)) and k > 10:
            break
    return s

def closed_form_inf(a):
    a = mp.mpf(a)
    return (mp.sqrt(mp.pi) / 4) * a**(mp.mpf(-3) / 2)

def direct_finite_sum_k2(n, beta):
    n = int(n)
    beta = mp.mpf(beta)
    s = mp.mpf(0)
    for k in range(1, n + 1):
        s += k**2 * mp.e**(-beta * k**2 / n)
    return s

def closed_form_finite(n, beta):
    n = mp.mpf(n)
    beta = mp.mpf(beta)
    return (mp.sqrt(mp.pi) / 4) * (n / beta) ** (mp.mpf(3) / 2)

print("=== Infinite-sum form: Sum_{k=1}^inf k^2 e^{-a k^2} vs (sqrt(pi)/4) a^{-3/2} ===")
for a in [mp.mpf('0.1'), mp.mpf('0.01'), mp.mpf('0.001'), mp.mpf('0.0001')]:
    direct = direct_inf_sum_k2(a)
    closed = closed_form_inf(a)
    absdiff = abs(direct - closed)
    reldiff = absdiff / abs(closed)
    print(f"a={float(a):<10} direct={mp.nstr(direct,15)}  closed={mp.nstr(closed,15)}  absdiff={mp.nstr(absdiff,6)}  reldiff={mp.nstr(reldiff,6)}")

print()
print("=== Finite-n truncated form: Sum_{k=1}^n k^2 e^{-beta k^2/n} vs (sqrt(pi)/4)(n/beta)^{3/2} ===")
gammas = [mp.mpf('0.1'), mp.mpf('0.3'), mp.mpf('0.5'), mp.mpf('0.7'), mp.mpf('0.9'), mp.mpf('1.0')]
ns = [2000, 20000, 200000]
for gamma in gammas:
    beta = gamma * (2 - gamma) / 2
    for n in ns:
        direct = direct_finite_sum_k2(n, beta)
        closed = closed_form_finite(n, beta)
        reldiff = abs(direct - closed) / abs(closed)
        print(f"gamma={float(gamma):<5} n={n:<8} direct={mp.nstr(direct,15)}  closed={mp.nstr(closed,15)}  reldiff={mp.nstr(reldiff,6)}")

print()
print("=== Sanity: does the crude tail bound for k>n (finite truncation) matter? ===")
# for beta*n large, tail beyond n should be exponentially small relative to the n/beta-scale sum.
for gamma in [mp.mpf('0.1'), mp.mpf('1.0')]:
    beta = gamma*(2-gamma)/2
    n = 2000
    full_inf = direct_inf_sum_k2(beta/n * 1)  # placeholder not used; direct approach below
    # Compare direct_finite_sum_k2(n,beta) to direct infinite sum with a=beta/n (should differ negligibly)
    a = beta / n
    inf_sum = direct_inf_sum_k2(a)
    fin_sum = direct_finite_sum_k2(n, beta)
    tail = inf_sum - fin_sum
    print(f"gamma={float(gamma)} n={n}: inf_sum-fin_sum (tail k>n) = {mp.nstr(tail, 10)}  (should be tiny vs fin_sum={mp.nstr(fin_sum,10)})")
