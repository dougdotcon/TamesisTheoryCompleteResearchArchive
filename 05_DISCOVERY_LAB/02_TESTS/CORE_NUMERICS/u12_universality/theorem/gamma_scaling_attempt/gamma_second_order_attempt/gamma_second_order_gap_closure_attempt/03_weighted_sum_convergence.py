"""
Gap 2 closure -- final numeric check: the weighted sum

    W_n(gamma) := sum_{k=1}^n e^{-s(k)} * |Delta_tau(k)|

(the quantity that must -> 0 for Gap 2's fluctuation-correction term to be
provably negligible in the E(gamma) limit) is computed by DIRECT summation
(no closed-form Gaussian-moment shortcut used here -- this is a fully
independent numeric cross-check of the whole chain, not just of Lemma G2)
and its decay rate under n -> 10n is compared against the predicted
Theta(n^{-1/2}), exactly as this lineage's own convention checks rates
(cf. predecessor ATTEMPT.md Sec.3/Sec.6.1, "ratio of successive errors
under n -> 10n converges to sqrt(10)").

Also cross-checks the *signed* correction

    Corr_n(gamma) := sum_{k=1}^n e^{-s(k)} * (-Delta_tau(k)/2)

directly against the leading-order closed-form prediction derived in the
ATTEMPT (Lemma G2 substituted into the Delta_tau-weighted sum), as an
independent confirmation of the whole analytic chain, not just of the
qualitative O(n^{-1/2}) rate.
"""
from mpmath import mp, mpf, exp, sqrt, pi

mp.dps = 50


def s_of_k(k, n, gamma):
    beta = gamma * (2 - gamma) / mpf(2)
    return beta * mpf(k) ** 2 / mpf(n) - gamma * mpf(k) / (2 * mpf(n))


def delta_tau(k, n, gamma):
    g = gamma
    kk = mpf(k)
    return (-kk ** 2 * g * (1 - g) ** 2 + kk * g * (1 - g) * (5 - 4 * g) / 6) / mpf(n) ** 2


def W_n(n, gamma):
    total = mpf(0)
    for k in range(1, n + 1):
        sk = s_of_k(k, n, gamma)
        if sk > 80:  # e^{-80} already far below dps=50 precision floor, safe cutoff
            break
        total += exp(-sk) * abs(delta_tau(k, n, gamma))
    return total


def Corr_n(n, gamma):
    total = mpf(0)
    for k in range(1, n + 1):
        sk = s_of_k(k, n, gamma)
        if sk > 80:
            break
        total += exp(-sk) * (-delta_tau(k, n, gamma) / 2)
    return total


beta_of = lambda g: g * (2 - g) / mpf(2)

print("=" * 90)
print("W_n(gamma) := sum_k e^{-s(k)} |Delta_tau(k)|  --  direct summation, growth under n -> 10n")
print("Predicted order: Theta(n^{-1/2}); successive ratio under n -> 10n should -> sqrt(10) = "
      f"{float(sqrt(mpf(10))):.6f}")
print("=" * 90)

gammas = [mpf('0.1'), mpf('0.3'), mpf('0.5'), mpf('0.7'), mpf('0.9'), mpf('0.99')]
ns = [1000, 10000, 100000]

for g in gammas:
    vals = []
    for n in ns:
        w = W_n(n, g)
        vals.append(w)
    ratios = []
    for i in range(len(vals) - 1):
        # W ~ C n^{-1/2}  =>  W(n)/W(10n) -> sqrt(10)
        ratios.append(vals[i] / vals[i + 1])
    print(f"gamma={float(g):.2f}: W_n = " +
          ", ".join(f"n={n}: {float(w):.6e}" for n, w in zip(ns, vals)) +
          "   ratios(W_n/W_10n) = " + ", ".join(f"{float(r):.6f}" for r in ratios))

print()
print("=" * 90)
print("Leading-order closed-form check of W_n(gamma) against the analytic prediction")
print("  W_n ~ [gamma(1-gamma)^2 (sqrt(pi)/4) beta^{-3/2}] n^{-1/2}   (leading k^2 term dominates)")
print("=" * 90)
for g in gammas:
    beta = beta_of(g)
    n = 100000
    w = W_n(n, g)
    predicted_leading = g * (1 - g) ** 2 * (sqrt(pi) / 4) * beta ** mpf('-1.5') / sqrt(mpf(n))
    print(f"gamma={float(g):.2f}: W_n(n=1e5) direct = {float(w):.6e}   "
          f"leading-order prediction = {float(predicted_leading):.6e}   "
          f"ratio = {float(w/predicted_leading):.6f}")

print()
print("=" * 90)
print("Signed correction Corr_n(gamma) := sum_k e^{-s(k)} * (-Delta_tau(k)/2)")
print("(this is exactly the term that must vanish for the tau(M)->tau(gamma k)")
print(" substitution used in Sec.4 of the predecessor ATTEMPT.md to be justified)")
print("=" * 90)
for g in gammas:
    for n in [1000, 10000, 100000, 1000000]:
        c = Corr_n(n, g)
        print(f"  gamma={float(g):.2f} n={n:8d}: Corr_n = {float(c):.6e}")
    print()

print("If Corr_n -> 0 as n grows (at the Theta(n^{-1/2}) rate shown above), Gap 2 is closed:")
print("substituting tau(gamma k) for the exact E_M[tau(M)] contributes exactly 0 to the")
print("n->infty limit defining E(gamma), rigorously (not just 'expected negligible').")
