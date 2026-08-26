"""
Independent high-precision numerical check of the PROVED closed form
    D_0(gamma) := lim_n [ sum_{k=1}^n e^{-s(k)} - G_n ] = (gamma-1)/(2*(2-gamma))
where s(k) = beta*k^2/n - gamma*k/(2n), beta = gamma(2-gamma)/2,
G_n = (1/2)*sqrt(pi*n/beta).

This is the "deterministic half" of the second-order decomposition
S_n = sum_k A_k = sum_k e^{-s(k)} + sum_k [A_k - e^{-s(k)}]
                = (G_n + D_0(gamma) + o(1)) + (the hard, Binomial-averaged half).

Derivation of D_0 (see ATTEMPT.md of this front, Sec 3):
  sum_{k=1}^n e^{-s(k)} = sum_k e^{-beta k^2/n} * e^{gamma k/(2n)}
Poisson summation / Jacobi theta transform gives EXACTLY, with
exponentially small (in n) error:
  sum_{k=1}^infty e^{-a k^2} = (1/2)sqrt(pi/a) - 1/2 + O(sqrt(1/a) e^{-pi^2/a})
applied with a = beta/n (so pi^2/a = pi^2 n / beta -> infinity), giving
  sum_{k=1}^n e^{-beta k^2/n} = G_n - 1/2 + O(n^{1/2} e^{-c n})
and a direct Euler-Maclaurin estimate of the correction from the
e^{gamma k/(2n)} factor (odd part contributes gamma/(4 beta), all
higher terms -> 0) gives D_0(gamma) = gamma/(4 beta) - 1/2
                                     = 1/(2(2-gamma)) - 1/2
                                     = (gamma-1)/(2(2-gamma)).
"""
import mpmath as mp

mp.mp.dps = 50


def beta_of(g):
    return g * (2 - g) / 2


def s(k, n, g):
    b = beta_of(g)
    return b * k * k / n - g * k / (2 * n)


def sum_exp_s(n, g, K=None):
    if K is None:
        K = n
    total = mp.mpf(0)
    for k in range(1, K + 1):
        total += mp.e ** (-s(k, n, g))
    return total


def G(n, g):
    b = beta_of(g)
    return mp.mpf(1) / 2 * mp.sqrt(mp.pi * n / b)


def D0_closed(g):
    return (g - 1) / (2 * (2 - g))


if __name__ == "__main__":
    print("D0(gamma) closed-form vs direct high-precision summation")
    print("=" * 78)
    gammas = [mp.mpf(x) for x in ("0.1", "0.3", "0.5", "0.7", "0.9", "1.0")]
    ns = [10 ** 4, 10 ** 5, 10 ** 6]
    for g in gammas:
        target = D0_closed(g)
        print(f"gamma={float(g):.2f}  D0(gamma) [closed form] = {mp.nstr(target, 12)}")
        prev_err = None
        for n in ns:
            # truncate the k-sum at a generous multiple of the Gaussian
            # scale sqrt(n/beta); e^{-s(k)} is negligible well beyond that.
            b = beta_of(g)
            Kcut = int(mp.sqrt(n / b) * 25) + 50
            Kcut = min(Kcut, n)
            Sn = sum_exp_s(n, g, K=Kcut)
            Gn = G(n, g)
            Dn = Sn - Gn
            err = Dn - target
            ratio = (prev_err / err) if (prev_err is not None and err != 0) else None
            print(f"    n={n:>8}  D_n={mp.nstr(Dn,12)}  D_n-target={mp.nstr(err,6)}"
                  + (f"   err(n/10)/err(n)={mp.nstr(ratio,6)}" if ratio else ""))
            prev_err = err
        print()
