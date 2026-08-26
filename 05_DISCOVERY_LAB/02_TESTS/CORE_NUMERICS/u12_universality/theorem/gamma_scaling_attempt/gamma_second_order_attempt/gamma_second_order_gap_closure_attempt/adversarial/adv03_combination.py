"""
Adversarial re-derivation C: the combination step Sum_k e^{-s(k)} Delta-tau(k) = O(n^{-1/2}).
Direct mpmath summation, no closed-form shortcut at all (Delta-tau(k) recomputed
from its own closed form, s(k) from its own definition, no reuse of adv02's sums).
Also checks the bound e^{-s(k)} <= e^{-beta k^2/n} e^{gamma/2} for k<=n.
Written fresh; no .py file of this lineage was read.
"""
import mpmath as mp

mp.mp.dps = 50

def beta_of(gamma):
    return gamma * (2 - gamma) / 2

def s_of_k(k, n, gamma):
    beta = beta_of(gamma)
    return beta * k**2 / n - gamma * k / (2 * n)

def delta_tau(k, n, gamma):
    return (-k**2 * gamma * (1 - gamma)**2 + (mp.mpf(1)/6) * k * gamma * (1 - gamma) * (5 - 4*gamma)) / n**2

def W_n(n, gamma, signed=False):
    n_ = int(n)
    gamma = mp.mpf(gamma)
    s = mp.mpf(0)
    for k in range(1, n_ + 1):
        dt = delta_tau(k, n_, gamma)
        w = mp.e**(-s_of_k(k, n_, gamma))
        s += w * (dt if signed else abs(dt))
    return s

print("=== Bound check: e^{-s(k)} <= e^{-beta k^2/n} * e^{gamma/2} for all k<=n ===")
violations = 0
for gamma in [mp.mpf('0.1'), mp.mpf('0.5'), mp.mpf('0.9'), mp.mpf('0.99')]:
    beta = beta_of(gamma)
    n = 500
    for k in range(1, n + 1):
        lhs = mp.e**(-s_of_k(k, n, gamma))
        rhs = mp.e**(-beta * k**2 / n) * mp.e**(gamma / 2)
        if lhs > rhs:
            violations += 1
print(f"Violations of e^-s(k) <= e^-(beta k^2/n) e^(gamma/2) across gamma in {{0.1,0.5,0.9,0.99}}, k=1..500: {violations}")
assert violations == 0

print()
print("=== W_n(gamma) := Sum_k e^{-s(k)} |Delta-tau(k)|, direct summation, no shortcuts ===")
gammas = [mp.mpf('0.1'), mp.mpf('0.3'), mp.mpf('0.5'), mp.mpf('0.7'), mp.mpf('0.9'), mp.mpf('0.99')]
ns = [1000, 10000, 100000]
Wvals = {}
for gamma in gammas:
    Wvals[gamma] = {}
    for n in ns:
        Wvals[gamma][n] = W_n(n, gamma, signed=False)
    print(f"gamma={float(gamma):<5}  " + "  ".join(f"W_{n}={mp.nstr(Wvals[gamma][n],10)}" for n in ns))

print()
print("=== Ratio test: W_n / W_{10n} should -> sqrt(10) = 3.16227766... if O(n^{-1/2}) ===")
sqrt10 = mp.sqrt(10)
print(f"sqrt(10) = {mp.nstr(sqrt10, 10)}")
for gamma in gammas:
    r1 = Wvals[gamma][1000] / Wvals[gamma][10000]
    r2 = Wvals[gamma][10000] / Wvals[gamma][100000]
    print(f"gamma={float(gamma):<5}  W_1000/W_10000={mp.nstr(r1,8)}  W_10000/W_100000={mp.nstr(r2,8)}")

print()
print("=== Signed sum (the actual correction quantity) -> should shrink toward 0 ===")
for gamma in gammas:
    vals = []
    for n in [1000, 10000, 100000, 1000000]:
        v = W_n(n, gamma, signed=True) * mp.mpf(-1) / 2  # Corr_n(gamma) := sum e^{-s(k)}(-Delta-tau(k)/2)
        vals.append(v)
    print(f"gamma={float(gamma):<5}  Corr_n at n=1e3,1e4,1e5,1e6: " + ", ".join(mp.nstr(v, 8) for v in vals))

print()
print("=== Leading-order closed-form cross-check of W_n's magnitude (no summation, from Lemma G2 + known sums) ===")
# W_n ~ e^{gamma/2} * [ gamma(1-gamma)^2/n^2 * (sqrt(pi)/4)(n/beta)^{3/2}
#                        + gamma(1-gamma)(5-4gamma)/(6n^2) * n/(2beta) ]
# This bound uses the SIGNED Delta-tau(k), which for most k is negative in the k^2
# term (dominant) - the document itself works with the absolute value |Delta-tau(k)|.
# We check here that the *dominant term* alone (the k^2/n^2 piece from Lemma G2)
# already reproduces the O(n^{-1/2}) trend seen in direct W_n above.
for gamma in gammas:
    beta = beta_of(gamma)
    for n in [1000, 10000, 100000]:
        leading = mp.e**(gamma/2) * gamma * (1-gamma)**2 / n**2 * (mp.sqrt(mp.pi)/4) * (mp.mpf(n)/beta)**mp.mpf(1.5)
        actual = Wvals[gamma][n]
        print(f"gamma={float(gamma):<5} n={n:<7} leading-term-estimate={mp.nstr(leading,8)}  actual W_n={mp.nstr(actual,8)}  ratio={mp.nstr(actual/leading,6)}")
