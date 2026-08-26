"""
Independent check of Lemma D0 (ATTEMPT.md Sec 3):

  Claim:  S_n^(0) := sum_{k=1}^n exp(-beta k^2/n + gamma k/(2n))
                    = G_n + D_0(gamma) + O(sqrt(n) e^{-c n})     [EXPONENTIALLY small error]
  with    D_0(gamma) = gamma/(4 beta) - 1/2 = (gamma-1)/(2(2-gamma))
          beta = gamma(2-gamma)/2,  G_n = (1/2) sqrt(pi n / beta)

Two things are checked independently, from scratch (no prior-front script read):

  (A) Is the closed form D_0(gamma) = (gamma-1)/(2(2-gamma)) correct?
      -- verified via (i) direct high-precision summation, extrapolated,
         and (ii) an independent "complete the square" re-derivation
         (different from the document's split quadratic+linear-Euler-
         Maclaurin route) done by hand and cross-checked here numerically.

  (B) Is the claimed error order O(sqrt(n) e^{-c n}) (exponentially small)
      correct, or is it actually the much larger O(n^{-1/2}) (polynomial)?
      This is done by looking at r_n := S_n^(0) - G_n - D_0(gamma) across
      a wide range of n and checking:
        - does r_n * sqrt(n) converge to a nonzero constant (=> true rate
          is Theta(n^{-1/2}), NOT exponential)?
        - does that constant match the coefficient predicted by an
          independent "complete the square" analysis:
              r_n ~ (gamma^2 / (16*beta)) * G_n/n
                  = (gamma^2 * sqrt(pi)) / (32 * beta^(3/2)) * n^{-1/2}
        - is r_n itself already far larger, at n=10^4..10^6, than any
          plausible exponentially-small quantity (which would be
          astronomically smaller than float/mpmath precision at these n)?
"""
import mpmath as mp

mp.mp.dps = 50


def beta_of(gamma):
    return mp.mpf(gamma) * (2 - mp.mpf(gamma)) / 2


def D0_closed(gamma):
    g = mp.mpf(gamma)
    return (g - 1) / (2 * (2 - g))


def Gn(n, gamma):
    b = beta_of(gamma)
    return mp.mpf(1) / 2 * mp.sqrt(mp.pi * n / b)


def Sn0_direct(n, gamma):
    """Direct high-precision summation of S_n^(0), no shortcuts."""
    g = mp.mpf(gamma)
    b = beta_of(gamma)
    total = mp.mpf(0)
    for k in range(1, n + 1):
        total += mp.e ** (-b * k * k / n + g * k / (2 * n))
    return total


def predicted_leading_error_coeff(gamma):
    """From the independent 'complete the square' re-derivation:
    r_n ~ (gamma^2 * sqrt(pi)) / (32 * beta^{3/2}) * n^{-1/2}
    i.e.  r_n * sqrt(n) -> gamma^2*sqrt(pi) / (32*beta^{3/2})
    """
    g = mp.mpf(gamma)
    b = beta_of(gamma)
    return g**2 * mp.sqrt(mp.pi) / (32 * b**mp.mpf('1.5'))


print("=" * 100)
print("PART A: closed-form D_0(gamma) value check (high precision, direct summation)")
print("=" * 100)
gammas = [mp.mpf('0.1'), mp.mpf('0.3'), mp.mpf('0.5'), mp.mpf('0.7'), mp.mpf('0.9'), mp.mpf('1.0')]
ns_small = [2000, 4000, 8000]  # keep small enough for a pure-python mpmath loop to be fast

print(f"{'gamma':>6} {'n':>7} {'S_n0':>18} {'G_n':>18} {'S_n0-G_n':>14} {'D0_closed':>14} {'r_n=S-G-D0':>14}")
richardson_rows = {}
for g in gammas:
    vals = []
    for n in ns_small:
        Sn0 = Sn0_direct(n, g)
        G = Gn(n, g)
        D0 = D0_closed(g)
        r = Sn0 - G - D0
        vals.append((n, Sn0, G, D0, r))
        print(f"{float(g):6.2f} {n:7d} {float(Sn0):18.10f} {float(G):18.10f} "
              f"{float(Sn0 - G):14.8f} {float(D0):14.8f} {float(r):14.8e}")
    richardson_rows[g] = vals
    print()

print("=" * 100)
print("PART B: error-order diagnosis -- is r_n*sqrt(n) converging to a nonzero constant?")
print("=" * 100)
print("(If yes: TRUE error order is Theta(n^{-1/2}), directly contradicting the Lemma D0")
print(" claim of O(sqrt(n) e^{-c n}) [exponentially small]. Predicted coefficient from an")
print(" independent 'complete the square' re-derivation is also printed for comparison.)")
print()
print(f"{'gamma':>6} {'n':>8} {'r_n':>16} {'r_n*sqrt(n)':>16} {'predicted coeff':>18}")
for g in gammas:
    pred = predicted_leading_error_coeff(g)
    for n in [1000, 2000, 4000, 8000, 16000, 32000]:
        Sn0 = Sn0_direct(n, g)
        G = Gn(n, g)
        D0 = D0_closed(g)
        r = Sn0 - G - D0
        rsn = r * mp.sqrt(n)
        print(f"{float(g):6.2f} {n:8d} {float(r):16.10e} {float(rsn):16.10f} {float(pred):18.10f}")
    print()
