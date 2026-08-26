"""
Follow-up to adv02: the coefficients |c_i(k)| are NOT literally monotone
in k (c1(k) crosses zero for gamma near 1, causing a local dip in |c1(k)|).
This script checks whether the Bulk/Tail Lemma's actual two needed facts
  (i)  g_k(Theta_k) <= g_K(Theta_K)   [bulk piece, uses K's own coeffs on RHS]
  (ii) g_k(K)        <= g_K(K)        [tail piece, uses K's own coeffs on RHS]
still hold for EVERY k=1..K despite the coefficient non-monotonicity, for
the worst offending case found (n=2000, gamma=0.9), and a more extreme one
(gamma=0.99), across the FULL range -- not just a handful of spot points.
"""
import mpmath as mp
mp.mp.dps = 50


def tau_val(m, k, n):
    return (m**3/3 + m**2*(mp.mpf('0.5') - k) + m*(k**2 - k + mp.mpf(1)/6)) / n**2


def tau_prime(m, k, n):
    return (m**2 + m*(1 - 2*k) + k**2 - k + mp.mpf(1)/6) / n**2


def tau_double_prime(m, k, n):
    return (2*m + 1 - 2*k) / n**2


def c_coeffs(k, n, gamma):
    gk = gamma * k
    c0 = tau_val(gk, k, n) / 2
    c1 = k*(1-gamma)/n - mp.mpf(1)/(2*n) + tau_prime(gk, k, n)/2
    c2 = -mp.mpf(1)/(2*n) + tau_double_prime(gk, k, n)/4
    c3 = mp.mpf(1)/(6*n**2)
    return c0, c1, c2, c3


def g_func(t, c0, c1, c2, c3):
    return abs(c0) + abs(c1)*t + abs(c2)*t**2 + abs(c3)*t**3


for (n, gamma, K, C) in [(2000, 0.9, 60, 1.5), (8000, 0.99, 120, 1.5),
                          (32000, 0.99, 240, 1.5), (500, 0.99, 30, 1.5)]:
    nn, gg, KK, CC = mp.mpf(n), mp.mpf(gamma), K, mp.mpf(C)
    c0K, c1K, c2K, c3K = c_coeffs(KK, nn, gg)
    Theta_K = CC * mp.sqrt(KK * mp.log(nn))
    g_ThetaK_atK = g_func(Theta_K, c0K, c1K, c2K, c3K)
    g_K_atK = g_func(KK, c0K, c1K, c2K, c3K)

    fail_bulk = []
    fail_tail = []
    for k in range(1, K+1):
        c0k, c1k, c2k, c3k = c_coeffs(k, nn, gg)
        Theta_k = CC * mp.sqrt(k * mp.log(nn))
        g_k_at_Thetak = g_func(Theta_k, c0k, c1k, c2k, c3k)
        g_k_at_K = g_func(KK, c0k, c1k, c2k, c3k)
        if g_k_at_Thetak > g_ThetaK_atK:
            fail_bulk.append(k)
        if g_k_at_K > g_K_atK:
            fail_tail.append(k)

    print(f"n={n}, gamma={gamma}, K={K}, C={C}:")
    print(f"  g_K(Theta_K) [at k=K] = {float(g_ThetaK_atK):.6e}, "
          f"g_K(K) [at k=K] = {float(g_K_atK):.6e}")
    print(f"  bulk fact g_k(Theta_k) <= g_K(Theta_K): "
          f"{len(fail_bulk)} failures out of {K} tested k values"
          + (f"  -- failing k's: {fail_bulk[:10]}{'...' if len(fail_bulk)>10 else ''}" if fail_bulk else ""))
    print(f"  tail fact g_k(K) <= g_K(K): "
          f"{len(fail_tail)} failures out of {K} tested k values"
          + (f"  -- failing k's: {fail_tail[:10]}{'...' if len(fail_tail)>10 else ''}" if fail_tail else ""))
    print()

print("If zero failures everywhere above: despite the coefficient")
print("non-monotonicity found in adv02 (c1(k) dipping through zero near")
print("gamma~1), the two facts the Bulk/Tail Lemma's proof actually needs")
print("still hold empirically across the full tested ranges -- the")
print("coefficient dip is too small in magnitude to ever flip the final")
print("inequality (other coefficients, esp. c0 and c2, dominate). This")
print("would mean the exposition gap (unstated monotonicity-in-k) is a")
print("genuine gap in the WRITTEN PROOF (an unjustified step), but the")
print("underlying claim itself is not found to be false in the tested range.")
